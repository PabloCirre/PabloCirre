#!/usr/bin/env python3
import sys
import json
import argparse
import re
import xml.etree.ElementTree as ET
from collections import Counter, deque
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Set
from urllib.parse import urljoin, urlparse, urlunparse
import datetime
import os

import requests
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 10
DEFAULT_MAX_PAGES = 10
USER_AGENT = "Pablo-Cirre-SEO-Audit/1.0 (+https://pablocirre.es)"


@dataclass
class SEOIssue:
    code: str           # e.g. TITLE_TOO_LONG
    severity: str       # error | warning | info
    category: str       # meta | headings | content | links | images | social | structured_data | indexing | accessibility | technical | http | hreflang
    value: Optional[Any] = None
    limit: Optional[Any] = None
    extra: Optional[Dict[str, Any]] = None


@dataclass
class SEOPageResult:
    url: str
    status: int
    metrics: Dict[str, Any]
    issues: List[SEOIssue]


class SEOAuditor:
    """
    Auditor SEO on-page centrado SOLO en HTML, estructura y señales SEO clásicas.
    Nada de PageSpeed: todo se basa en el HTML que devuelve cada URL.
    """

    def __init__(
        self,
        base_url: str,
        max_pages: int = DEFAULT_MAX_PAGES,
        timeout: int = DEFAULT_TIMEOUT,
        use_sitemap: bool = False,
        sitemap_url: Optional[str] = None,
        check_links: bool = False,
    ):
        self.base_url = self._normalize_base_url(base_url)
        self.max_pages = max_pages
        self.timeout = timeout
        self.use_sitemap = use_sitemap
        self.sitemap_url = sitemap_url
        self.check_links = check_links

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

        parsed = urlparse(self.base_url)
        self.scheme = parsed.scheme
        self.domain = parsed.netloc

        self.visited: Set[str] = set()
        self.results: List[SEOPageResult] = []

        # robots.txt cache
        self.robots_status: Optional[int] = None
        self.robots_content: Optional[str] = None

        # cache de estado de enlaces (para enlaces rotos)
        self.link_status_cache: Dict[str, int] = {}

        # inbound links (enlaces internos entrantes por URL normalizada)
        self.inbound_link_counts: Counter = Counter()

    # ---------------------------
    # Utilidades
    # ---------------------------
    @staticmethod
    def _normalize_base_url(url: str) -> str:
        url = url.strip()
        if not re.match(r"^https?://", url):
            url = "https://" + url
        parsed = urlparse(url)
        cleaned = parsed._replace(fragment="")
        return urlunparse(cleaned).rstrip("/")

    def _normalize_for_visit(self, url: str) -> str:
        parsed = urlparse(url)
        parsed = parsed._replace(fragment="", query="")
        path = parsed.path or "/"
        if path != "/" and path.endswith("/"):
            path = path.rstrip("/")
        parsed = parsed._replace(path=path)
        return urlunparse(parsed)

    def _is_internal(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
        except Exception:
            return False
        if not parsed.netloc:
            return True
        return parsed.netloc == self.domain

    # ---------------------------
    # Descubrimiento de URLs
    # ---------------------------
    def _get_urls_from_sitemap(self) -> List[str]:
        candidates = []
        if self.sitemap_url:
            candidates.append(self.sitemap_url)
        candidates.extend(
            [
                f"{self.base_url}/sitemap.xml",
                f"{self.base_url}/sitemap_index.xml",
                f"{self.base_url}/sitemap.php",
            ]
        )

        root = None
        for url in candidates:
            try:
                resp = self.session.get(url, timeout=self.timeout)
                if resp.status_code != 200:
                    continue
                try:
                    root = ET.fromstring(resp.content)
                    break
                except ET.ParseError:
                    continue
            except requests.RequestException:
                continue

        if not root:
            return [self.base_url]

        namespaces = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls: List[str] = []

        sitemap_tags = root.findall(".//ns:sitemap", namespaces) or root.findall(".//sitemap")
        if sitemap_tags:
            # sitemap index
            for sm in sitemap_tags:
                loc = sm.find("ns:loc", namespaces) or sm.find("loc")
                if loc is None or not (loc.text or "").strip():
                    continue
                sub_url = loc.text.strip()
                try:
                    sub_resp = self.session.get(sub_url, timeout=self.timeout)
                    if sub_resp.status_code != 200:
                        continue
                    sub_root = ET.fromstring(sub_resp.content)
                    url_tags = sub_root.findall(".//ns:url/ns:loc", namespaces) or sub_root.findall(".//url/loc")
                    for u in url_tags:
                        if u.text:
                            urls.append(u.text.strip())
                except (requests.RequestException, ET.ParseError):
                    continue
        else:
            # sitemap simple
            url_tags = root.findall(".//ns:url/ns:loc", namespaces) or root.findall(".//url/loc")
            for u in url_tags:
                if u.text:
                    urls.append(u.text.strip())

        clean_urls: List[str] = []
        seen: Set[str] = set()
        for u in urls:
            parsed_u = urlparse(u)
            if parsed_u.netloc and parsed_u.netloc != self.domain:
                continue
            norm = self._normalize_for_visit(u)
            if norm not in seen:
                seen.add(norm)
                clean_urls.append(norm)

        if self.max_pages:
            clean_urls = clean_urls[: self.max_pages]
        return clean_urls or [self.base_url]

    def _crawl_site_bfs(self) -> List[str]:
        urls: List[str] = []
        queue = deque([self.base_url])

        while queue and len(urls) < self.max_pages:
            current = queue.popleft()
            norm = self._normalize_for_visit(current)
            if norm in self.visited:
                continue
            self.visited.add(norm)
            urls.append(current)

            try:
                resp = self.session.get(current, timeout=self.timeout)
            except requests.RequestException:
                continue

            if resp.status_code != 200 or "text/html" not in resp.headers.get("Content-Type", ""):
                continue

            soup = BeautifulSoup(resp.content, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a.get("href", "").strip()
                if not href:
                    continue
                if href.startswith(("#", "javascript:", "mailto:", "tel:")):
                    continue
                full = urljoin(current, href)
                if not self._is_internal(full):
                    continue
                norm_full = self._normalize_for_visit(full)
                if norm_full not in self.visited:
                    queue.append(full)

        return urls

    # ---------------------------
    # Robots.txt
    # ---------------------------
    def _fetch_robots(self) -> None:
        if self.robots_status is not None:
            return
        robots_url = f"{self.scheme}://{self.domain}/robots.txt"
        try:
            resp = self.session.get(robots_url, timeout=self.timeout)
            self.robots_status = resp.status_code
            self.robots_content = resp.text if resp.status_code == 200 else None
        except requests.RequestException:
            self.robots_status = 0
            self.robots_content = None

    def _check_robots_all_disallowed(self) -> bool:
        if not self.robots_content:
            return False
        lines = [l.strip() for l in self.robots_content.splitlines() if l.strip()]
        ua_star = False
        for line in lines:
            if line.lower().startswith("user-agent:"):
                ua = line.split(":", 1)[1].strip()
                ua_star = ua == "*"
            elif ua_star and line.lower().startswith("disallow:"):
                rule = line.split(":", 1)[1].strip()
                if rule in ("/", "/*"):
                    return True
        return False

    # ---------------------------
    # Helpers para SEO
    # ---------------------------
    def _extract_focus_keywords(self, title: str, max_keywords: int = 3) -> List[str]:
        if not title:
            return []
        text = title.lower()
        text = re.sub(r"[^\wáéíóúñü]+", " ", text)
        tokens = [t for t in text.split() if len(t) > 3]
        stopwords = {
            "the", "and", "for", "with", "from", "that", "this", "your", "free", "bulk",
            "para", "con", "las", "los", "una", "unos", "unas", "del", "por", "sus",
            "tu", "esta", "estos", "estas", "ser", "como", "sobre"
        }
        filtered = [t for t in tokens if t not in stopwords]
        if not filtered:
            filtered = tokens
        seen = set()
        focus = []
        for t in filtered:
            if t not in seen:
                seen.add(t)
                focus.append(t)
                if len(focus) >= max_keywords:
                    break
        return focus

    def _check_link_status(self, url: str) -> Optional[int]:
        if url in self.link_status_cache:
            return self.link_status_cache[url]
        try:
            resp = self.session.head(url, allow_redirects=True, timeout=self.timeout)
            if resp.status_code >= 400 or resp.status_code < 200:
                resp_get = self.session.get(url, allow_redirects=True, timeout=self.timeout)
                status = resp_get.status_code
            else:
                status = resp.status_code
        except requests.RequestException:
            status = 0
        self.link_status_cache[url] = status
        return status

    @staticmethod
    def _parse_robots_directives(value: Optional[str]) -> Set[str]:
        directives: Set[str] = set()
        if not value:
            return directives
        for part in value.split(","):
            d = part.strip().lower()
            if d:
                directives.add(d)
        return directives

    # ---------------------------
    # Auditoría de una URL
    # ---------------------------
    def audit_url(self, url: str) -> SEOPageResult:
        issues: List[SEOIssue] = []
        metrics: Dict[str, Any] = {}

        try:
            resp = self.session.get(url, timeout=self.timeout)
            status = resp.status_code
            metrics["status"] = status

            if status != 200:
                issues.append(
                    SEOIssue(
                        code="HTTP_ERROR",
                        severity="error",
                        category="http",
                        value=status,
                        extra={"message": f"Non-200 HTTP status for URL {url}"},
                    )
                )
                return SEOPageResult(url=url, status=status, metrics=metrics, issues=issues)

            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                issues.append(
                    SEOIssue(
                        code="NON_HTML_CONTENT",
                        severity="info",
                        category="technical",
                        value=content_type,
                        extra={"message": "URL does not return HTML; SEO on-page checks limited."},
                    )
                )
                return SEOPageResult(url=url, status=status, metrics=metrics, issues=issues)

            soup = BeautifulSoup(resp.content, "html.parser")

            # HTML básico
            html_tag = soup.find("html")
            html_lang = html_tag.get("lang") if html_tag else None
            metrics["html_lang"] = html_lang
            if not html_lang:
                issues.append(
                    SEOIssue(
                        code="HTML_LANG_MISSING",
                        severity="warning",
                        category="accessibility",
                        extra={"message": "<html lang=\"...\"> is missing; affects accessibility and SEO."},
                    )
                )

            head_tag = soup.find("head")
            metrics["has_head"] = head_tag is not None

            raw_text = resp.text.lstrip()
            metrics["has_doctype"] = raw_text.lower().startswith("<!doctype html")

            charset_tag = soup.find("meta", charset=True) or soup.find(
                "meta", attrs={"http-equiv": lambda v: v and v.lower() == "content-type"}
            )
            metrics["has_meta_charset"] = charset_tag is not None

            viewport_tag = soup.find("meta", attrs={"name": lambda v: v and v.lower() == "viewport"})
            metrics["has_meta_viewport"] = viewport_tag is not None
            if not viewport_tag:
                issues.append(
                    SEOIssue(
                        code="VIEWPORT_MISSING",
                        severity="warning",
                        category="technical",
                        extra={"message": "Missing <meta name=\"viewport\">; page may not be mobile-friendly."},
                    )
                )

            # URL, slug y profundidad
            parsed_url = urlparse(url)
            path = parsed_url.path or "/"
            metrics["url_path"] = path
            slug = path.strip("/").split("/")[-1] if path not in ("", "/") else ""
            metrics["url_slug"] = slug
            depth = len([s for s in path.split("/") if s])
            metrics["url_path_depth"] = depth
            if slug and len(slug) > 80:
                issues.append(
                    SEOIssue(
                        code="SLUG_TOO_LONG",
                        severity="info",
                        category="technical",
                        value=len(slug),
                        limit=80,
                        extra={"message": "URL slug is very long; short, descriptive slugs are preferred."},
                    )
                )
            if depth > 5:
                issues.append(
                    SEOIssue(
                        code="URL_DEPTH_HIGH",
                        severity="info",
                        category="technical",
                        value=depth,
                        limit=5,
                        extra={"message": "URL path depth is high; flatter structures are usually better for SEO."},
                    )
                )

            # TEXT & WORD COUNT (quitando ruido básico)
            soup_for_text = soup.__copy__()
            for tag_name in ["script", "style", "noscript"]:
                for t in soup_for_text.find_all(tag_name):
                    t.extract()
            for t in soup_for_text.find_all(["nav", "footer"]):
                t.extract()

            visible_text = soup_for_text.get_text(separator=" ", strip=True)
            tokens = re.findall(r"\w+", visible_text, flags=re.UNICODE)
            word_count = len(tokens)
            metrics["word_count"] = word_count
            if word_count < 300:
                issues.append(
                    SEOIssue(
                        code="CONTENT_THIN",
                        severity="warning",
                        category="content",
                        value=word_count,
                        limit=300,
                        extra={"message": "Very low word count; aim for 300+ words for most pages."},
                    )
                )
            elif word_count < 500:
                issues.append(
                    SEOIssue(
                        code="CONTENT_LOW",
                        severity="info",
                        category="content",
                        value=word_count,
                        limit=500,
                        extra={"message": "Content could be more in-depth; many competitive pages use 500+ words."},
                    )
                )

            # Primer párrafo (focus keyword en primeras líneas)
            first_paragraph_tag = soup.find("p")
            first_paragraph_text = first_paragraph_tag.get_text(" ", strip=True) if first_paragraph_tag else ""
            metrics["first_paragraph_length"] = len(first_paragraph_text)

            # TITLE
            title_tags = soup.find_all("title")
            if len(title_tags) > 1:
                issues.append(
                    SEOIssue(
                        code="TITLE_MULTIPLE",
                        severity="warning",
                        category="meta",
                        value=len(title_tags),
                        extra={"message": "Multiple <title> tags found; only one should exist."},
                    )
                )

            title_text = ""
            if soup.title and soup.title.string:
                title_text = soup.title.string.strip()
            metrics["title"] = title_text
            metrics["title_length"] = len(title_text)

            if not title_text:
                issues.append(
                    SEOIssue(
                        code="TITLE_MISSING",
                        severity="error",
                        category="meta",
                        extra={"message": "<title> is missing or empty."},
                    )
                )
            else:
                if len(title_text) < 30:
                    issues.append(
                        SEOIssue(
                            code="TITLE_TOO_SHORT",
                            severity="warning",
                            category="meta",
                            value=len(title_text),
                            limit=30,
                            extra={"message": "Title is very short; consider ~50–60 characters when possible."},
                        )
                    )
                if len(title_text) > 60:
                    issues.append(
                        SEOIssue(
                            code="TITLE_TOO_LONG",
                            severity="warning",
                            category="meta",
                            value=len(title_text),
                            limit=60,
                            extra={"message": "Title is long; >60 chars may be truncated or rewritten in SERPs."},
                        )
                    )

            # META DESCRIPTION (múltiples + longitud)
            desc_tags = soup.find_all("meta", attrs={"name": lambda v: v and v.lower() == "description"})
            if len(desc_tags) > 1:
                issues.append(
                    SEOIssue(
                        code="META_DESC_MULTIPLE",
                        severity="warning",
                        category="meta",
                        value=len(desc_tags),
                        extra={"message": "Multiple meta description tags found; only one is recommended."},
                    )
                )

            meta_desc = ""
            if desc_tags:
                meta_desc = desc_tags[0].get("content", "").strip()
            metrics["meta_description"] = meta_desc
            metrics["meta_description_length"] = len(meta_desc)

            if not meta_desc:
                issues.append(
                    SEOIssue(
                        code="META_DESC_MISSING",
                        severity="warning",
                        category="meta",
                        extra={"message": "Meta description is missing or empty."},
                    )
                )
            else:
                if len(meta_desc) < 80:
                    issues.append(
                        SEOIssue(
                            code="META_DESC_TOO_SHORT",
                            severity="info",
                            category="meta",
                            value=len(meta_desc),
                            limit=80,
                            extra={"message": "Meta description is quite short; usually 120–160 characters works well."},
                        )
                    )
                if len(meta_desc) > 180:
                    issues.append(
                        SEOIssue(
                            code="META_DESC_TOO_LONG",
                            severity="info",
                            category="meta",
                            value=len(meta_desc),
                            limit=180,
                            extra={"message": "Meta description is long; snippets are commonly truncated around 150–160 chars."},
                        )
                    )

            # META KEYWORDS
            meta_kw_tag = soup.find("meta", attrs={"name": lambda v: v and v.lower() == "keywords"})
            meta_keywords_list: List[str] = []
            if meta_kw_tag:
                meta_keywords_content = meta_kw_tag.get("content", "") or ""
                parts = [p.strip() for p in meta_keywords_content.split(",") if p.strip()]
                meta_keywords_list = parts
                metrics["meta_keywords_present"] = True
                metrics["meta_keywords_count"] = len(parts)
                metrics["meta_keywords_length"] = len(meta_keywords_content)

                issues.append(
                    SEOIssue(
                        code="META_KEYWORDS_IGNORED",
                        severity="info",
                        category="meta",
                        value=len(parts),
                        extra={"message": "Meta keywords are largely ignored by modern search engines; avoid over-optimizing here."},
                    )
                )
                if len(parts) > 10:
                    issues.append(
                        SEOIssue(
                            code="META_KEYWORDS_TOO_MANY",
                            severity="warning",
                            category="meta",
                            value=len(parts),
                            limit=10,
                            extra={"message": "Too many meta keywords; can be seen as keyword stuffing."},
                        )
                    )
                if len(meta_keywords_content) > 255:
                    issues.append(
                        SEOIssue(
                            code="META_KEYWORDS_TOO_LONG",
                            severity="warning",
                            category="meta",
                            value=len(meta_keywords_content),
                            limit=255,
                            extra={"message": "Meta keywords string is very long; usually unnecessary."},
                        )
                    )
            else:
                metrics["meta_keywords_present"] = False

            # FOCUS KEYWORDS
            focus_keywords = self._extract_focus_keywords(title_text)
            metrics["focus_keywords_from_title"] = focus_keywords

            # keyword en meta description
            meta_desc_lower = meta_desc.lower()
            if focus_keywords and meta_desc:
                missing_in_desc = [kw for kw in focus_keywords if kw not in meta_desc_lower]
                if missing_in_desc:
                    issues.append(
                        SEOIssue(
                            code="META_DESC_MISSING_FOCUS_KEYWORDS",
                            severity="info",
                            category="meta",
                            value=missing_in_desc,
                            extra={"message": "Some focus keywords from title do not appear in meta description."},
                        )
                    )

            # keyword en slug
            if slug and focus_keywords:
                slug_lower = slug.lower()
                has_kw_in_slug = any(kw in slug_lower for kw in focus_keywords)
                metrics["slug_has_focus_keyword"] = has_kw_in_slug
                if not has_kw_in_slug:
                    issues.append(
                        SEOIssue(
                            code="SLUG_MISSING_FOCUS_KEYWORD",
                            severity="info",
                            category="technical",
                            value={"slug": slug, "focus_keywords": focus_keywords},
                            extra={"message": "URL slug does not contain any focus keyword from title."},
                        )
                    )
            else:
                metrics["slug_has_focus_keyword"] = False

            # keyword en primer párrafo
            fp_lower = first_paragraph_text.lower()
            if focus_keywords and first_paragraph_text:
                has_kw_first_p = any(kw in fp_lower for kw in focus_keywords)
                metrics["first_paragraph_has_focus_keyword"] = has_kw_first_p
                if not has_kw_first_p:
                    issues.append(
                        SEOIssue(
                            code="FIRST_PARAGRAPH_MISSING_FOCUS_KEYWORDS",
                            severity="info",
                            category="content",
                            value=focus_keywords,
                            extra={"message": "First paragraph does not contain any focus keyword from title."},
                        )
                    )
            else:
                metrics["first_paragraph_has_focus_keyword"] = False

            # HEADINGS
            h1_tags = soup.find_all("h1")
            h2_tags = soup.find_all("h2")
            metrics["h1_count"] = len(h1_tags)
            metrics["h2_count"] = len(h2_tags)

            if len(h1_tags) == 0:
                issues.append(
                    SEOIssue(
                        code="H1_MISSING",
                        severity="error",
                        category="headings",
                        extra={"message": "Page has no <h1>; important for structure and relevance."},
                    )
                )
            elif len(h1_tags) > 1:
                issues.append(
                    SEOIssue(
                        code="H1_MULTIPLE",
                        severity="warning",
                        category="headings",
                        value=len(h1_tags),
                        extra={"message": "Page has multiple <h1> tags; consider using a single primary heading."},
                    )
                )

            h1_texts = [h.get_text(" ", strip=True) for h in h1_tags]
            h2_texts = [h.get_text(" ", strip=True) for h in h2_tags]
            metrics["h1_texts"] = h1_texts
            metrics["h2_texts"] = h2_texts

            for idx, text in enumerate(h1_texts):
                if not text:
                    issues.append(
                        SEOIssue(
                            code="H1_EMPTY",
                            severity="error",
                            category="headings",
                            extra={"message": f"H1 #{idx+1} is empty."},
                        )
                    )
                elif len(text) > 120:
                    issues.append(
                        SEOIssue(
                            code="H1_TOO_LONG",
                            severity="info",
                            category="headings",
                            value=len(text),
                            limit=120,
                            extra={"message": "H1 is very long; shorter, focused headings are usually better."},
                        )
                    )

            # jerarquía de headings
            headings_sequence = soup.find_all(re.compile(r"^h[1-6]$", re.I))
            last_level = None
            for h in headings_sequence:
                try:
                    level = int(h.name[1])
                except Exception:
                    continue
                if last_level is None:
                    if level != 1:
                        issues.append(
                            SEOIssue(
                                code="FIRST_HEADING_NOT_H1",
                                severity="info",
                                category="headings",
                                value=level,
                                extra={"message": "First heading is not <h1>; consider starting hierarchy with H1."},
                            )
                        )
                else:
                    if level > last_level + 1:
                        issues.append(
                            SEOIssue(
                                code="HEADING_LEVEL_SKIP",
                                severity="info",
                                category="headings",
                                value={"from": last_level, "to": level},
                                extra={"message": "Heading levels jump (e.g., H2 -> H4); might hurt structure."},
                            )
                        )
                last_level = level

            # concordancia title / H1 / H2
            title_lower = title_text.lower()
            h1_join = " ".join(h1_texts).lower()
            h2_join = " ".join(h2_texts).lower()

            if focus_keywords:
                missing_in_h1 = [kw for kw in focus_keywords if kw not in h1_join]
                if missing_in_h1:
                    issues.append(
                        SEOIssue(
                            code="H1_MISSING_FOCUS_KEYWORDS",
                            severity="info",
                            category="headings",
                            value=missing_in_h1,
                            extra={"message": "Some focus keywords from title do not appear in any H1."},
                        )
                    )
                missing_in_h2 = [kw for kw in focus_keywords if kw not in h2_join]
                if missing_in_h2:
                    issues.append(
                        SEOIssue(
                            code="H2_MISSING_FOCUS_KEYWORDS",
                            severity="info",
                            category="headings",
                            value=missing_in_h2,
                            extra={"message": "Some focus keywords from title do not appear in any H2."},
                        )
                    )

            # CANONICAL
            canonical_tags = soup.find_all("link", rel=lambda v: v and "canonical" in str(v).lower())
            canonical_href = None
            if len(canonical_tags) > 1:
                issues.append(
                    SEOIssue(
                        code="CANONICAL_MULTIPLE",
                        severity="warning",
                        category="indexing",
                        value=len(canonical_tags),
                        extra={"message": "Multiple canonical tags found; only one should exist."},
                    )
                )
            if canonical_tags:
                canonical_href = canonical_tags[0].get("href")
            metrics["canonical_url"] = canonical_href

            requested_norm = self._normalize_for_visit(url)
            if canonical_href:
                canon_abs = urljoin(url, canonical_href)
                canon_norm = self._normalize_for_visit(canon_abs)
                if canon_norm != requested_norm:
                    issues.append(
                        SEOIssue(
                            code="CANONICAL_DIFFERENT_URL",
                            severity="info",
                            category="indexing",
                            value={"requested": requested_norm, "canonical": canon_norm},
                            extra={"message": "Canonical URL differs from requested URL; ensure no unwanted duplication."},
                        )
                    )
                parsed_canon = urlparse(canon_abs)
                if parsed_canon.netloc and parsed_canon.netloc != self.domain:
                    issues.append(
                        SEOIssue(
                            code="CANONICAL_EXTERNAL",
                            severity="warning",
                            category="indexing",
                            value=canonical_href,
                            extra={"message": "Canonical points to external domain; ensure this is intentional."},
                        )
                    )
            else:
                issues.append(
                    SEOIssue(
                        code="CANONICAL_MISSING",
                        severity="info",
                        category="indexing",
                        extra={"message": "Canonical link is missing; not always critical but recommended."},
                    )
                )

            # META ROBOTS / X-ROBOTS-TAG
            robots_tag = soup.find("meta", attrs={"name": lambda v: v and v.lower() == "robots"})
            meta_robots = robots_tag.get("content") if robots_tag else None
            metrics["meta_robots"] = meta_robots

            x_robots = resp.headers.get("X-Robots-Tag")
            metrics["x_robots_tag"] = x_robots

            meta_directives = self._parse_robots_directives(meta_robots)
            header_directives = self._parse_robots_directives(x_robots)
            all_directives = meta_directives.union(header_directives)
            metrics["robots_directives"] = sorted(all_directives)

            if "noindex" in all_directives:
                sev = "error" if url == self.base_url else "warning"
                issues.append(
                    SEOIssue(
                        code="PAGE_NOINDEX",
                        severity=sev,
                        category="indexing",
                        extra={"message": "Page is set to noindex; verify this is intentional."},
                    )
                )
            if "nosnippet" in all_directives or any(d.startswith("max-snippet") for d in all_directives):
                issues.append(
                    SEOIssue(
                        code="PAGE_NOSNIPPET",
                        severity="info",
                        category="indexing",
                        extra={"message": "nosnippet/max-snippet directive limits visible snippet; check if desired."},
                    )
                )
            if "noarchive" in all_directives:
                issues.append(
                    SEOIssue(
                        code="PAGE_NOARCHIVE",
                        severity="info",
                        category="indexing",
                        extra={"message": "noarchive directive prevents cached copy from appearing in SERPs."},
                    )
                )

            # HREFLANG
            hreflang_links = []
            for link in soup.find_all("link", href=True):
                rel_val = link.get("rel")
                rels = []
                if isinstance(rel_val, (list, tuple)):
                    rels = [str(r).lower() for r in rel_val]
                elif rel_val:
                    rels = [str(rel_val).lower()]
                if "alternate" in rels and link.get("hreflang"):
                    hreflang_links.append(link)

            hreflang_codes: List[str] = []
            hreflang_relative_count = 0
            href_by_code: Dict[str, List[str]] = {}

            for link in hreflang_links:
                code = (link.get("hreflang") or "").strip()
                href = link.get("href") or ""
                hreflang_codes.append(code)
                href_by_code.setdefault(code, []).append(href)
                if not href.startswith("http"):
                    hreflang_relative_count += 1

            metrics["hreflang_count"] = len(hreflang_links)
            metrics["hreflang_codes"] = hreflang_codes
            metrics["hreflang_relative_urls"] = hreflang_relative_count
            metrics["hreflang_has_x_default"] = "x-default" in [c.lower() for c in hreflang_codes]

            if hreflang_links:
                # duplicados por código
                for code, hrefs in href_by_code.items():
                    if len(hrefs) > 1:
                        issues.append(
                            SEOIssue(
                                code="HREFLANG_DUPLICATE_CODE",
                                severity="info",
                                category="hreflang",
                                value={"code": code, "urls": hrefs},
                                extra={"message": "Multiple hreflang entries for same code."},
                            )
                        )
                if hreflang_relative_count:
                    issues.append(
                        SEOIssue(
                            code="HREFLANG_RELATIVE_URL",
                            severity="info",
                            category="hreflang",
                            value=hreflang_relative_count,
                            extra={"message": "Some hreflang links use relative URLs; absolute URLs are recommended."},
                        )
                    )
                # self reference con lang HTML
                if html_lang:
                    lang_lower = html_lang.lower()
                    codes_lower = [c.lower() for c in hreflang_codes]
                    # aceptar coincidencia exacta o prefijo (es vs es-es)
                    has_self = any(
                        c == lang_lower or c.split("-")[0] == lang_lower.split("-")[0]
                        for c in codes_lower
                    )
                    metrics["hreflang_has_self_reference"] = has_self
                    if not has_self:
                        issues.append(
                            SEOIssue(
                                code="HREFLANG_MISSING_SELF_REFERENCE",
                                severity="info",
                                category="hreflang",
                                value={"html_lang": html_lang, "codes": hreflang_codes},
                                extra={"message": "No hreflang entry matches the page's html[lang]."},
                            )
                        )
                else:
                    metrics["hreflang_has_self_reference"] = False
            else:
                metrics["hreflang_has_self_reference"] = False

            # SOCIAL / OG / Twitter
            og_tags = soup.find_all("meta", property=lambda v: v and v.startswith("og:"))
            twitter_tags = soup.find_all("meta", attrs={"name": lambda v: v and v.startswith("twitter:")})
            metrics["og_tags_count"] = len(og_tags)
            metrics["twitter_tags_count"] = len(twitter_tags)

            if len(og_tags) == 0:
                issues.append(
                    SEOIssue(
                        code="OG_TAGS_MISSING",
                        severity="info",
                        category="social",
                        extra={"message": "No Open Graph tags found; social previews may be suboptimal."},
                    )
                )

            og_required = ["og:title", "og:description", "og:image", "og:url"]
            for prop in og_required:
                if not soup.find("meta", property=prop):
                    issues.append(
                        SEOIssue(
                            code=f"OG_{prop.split(':')[1].upper()}_MISSING",
                            severity="info",
                            category="social",
                            extra={"message": f"Missing {prop} for optimal social sharing."},
                        )
                    )

            og_type = None
            og_type_tag = soup.find("meta", property="og:type")
            if og_type_tag:
                og_type = og_type_tag.get("content")
            metrics["og_type"] = og_type

            fb_app_id = None
            fb_app_tag = soup.find("meta", property="fb:app_id")
            if fb_app_tag:
                fb_app_id = fb_app_id_tag.get("content")
            metrics["fb_app_id"] = fb_app_id

            if len(twitter_tags) == 0:
                issues.append(
                    SEOIssue(
                        code="TWITTER_TAGS_MISSING",
                        severity="info",
                        category="social",
                        extra={"message": "No Twitter Card tags found; previews on X/Twitter will be generic."},
                    )
                )

            # ENLACES
            a_tags = soup.find_all("a")
            internal_links = 0
            external_links = 0
            nofollow_links = 0
            empty_anchor_text = 0
            generic_anchor_text = 0
            broken_internal_links = 0

            generic_phrases = {"click here", "here", "más info", "leer más", "read more"}

            for a in a_tags:
                href = (a.get("href") or "").strip()
                if not href:
                    continue
                if href.startswith(("#", "javascript:", "mailto:", "tel:")):
                    continue
                full_url = urljoin(url, href)
                text = a.get_text(" ", strip=True)
                text_lower = text.lower()

                rel_val = a.get("rel") or []
                rel_str = " ".join(rel_val).lower() if isinstance(rel_val, (list, tuple)) else str(rel_val).lower()
                is_nofollow = "nofollow" in rel_str
                if is_nofollow:
                    nofollow_links += 1

                norm_link = self._normalize_for_visit(full_url)

                if self._is_internal(full_url):
                    internal_links += 1
                    # registrar inbound link
                    self.inbound_link_counts[norm_link] += 1

                    if self.check_links:
                        status_link = self._check_link_status(full_url)
                        if not status_link or status_link >= 400:
                            broken_internal_links += 1
                            issues.append(
                                SEOIssue(
                                    code="BROKEN_INTERNAL_LINK",
                                    severity="warning",
                                    category="links",
                                    value={"href": href, "status": status_link},
                                    extra={"message": f"Internal link appears broken: {href} (status {status_link})."},
                                )
                            )
                else:
                    external_links += 1

                if not text:
                    empty_anchor_text += 1
                elif text_lower in generic_phrases:
                    generic_anchor_text += 1

            metrics["internal_links"] = internal_links
            metrics["external_links"] = external_links
            metrics["nofollow_links"] = nofollow_links
            metrics["empty_anchor_text_count"] = empty_anchor_text
            metrics["generic_anchor_text_count"] = generic_anchor_text
            metrics["broken_internal_links"] = broken_internal_links

            if empty_anchor_text:
                issues.append(
                    SEOIssue(
                        code="EMPTY_ANCHOR_TEXT",
                        severity="warning",
                        category="links",
                        value=empty_anchor_text,
                        extra={"message": "Some links have empty anchor text; hurts accessibility and SEO context."},
                    )
                )
            if generic_anchor_text:
                issues.append(
                    SEOIssue(
                        code="GENERIC_ANCHOR_TEXT",
                        severity="info",
                        category="links",
                        value=generic_anchor_text,
                        extra={"message": "Some links use generic anchor text like 'click here'; use more descriptive anchors."},
                    )
                )

            if internal_links == 0 and url != self.base_url:
                issues.append(
                    SEOIssue(
                        code="NO_INTERNAL_OUTLINKS",
                        severity="info",
                        category="links",
                        extra={"message": "Page has no internal outgoing links; consider linking to relevant pages."},
                    )
                )

            # IMÁGENES
            img_tags = soup.find_all("img")
            img_total = len(img_tags)
            img_missing_alt = 0
            img_empty_alt = 0
            img_alt_with_focus = 0

            for img in img_tags:
                alt_val = img.get("alt")
                if alt_val is None:
                    img_missing_alt += 1
                else:
                    alt_str = alt_val.strip()
                    if not alt_str:
                        img_empty_alt += 1
                    if focus_keywords:
                        alt_low = alt_str.lower()
                        if any(kw in alt_low for kw in focus_keywords):
                            img_alt_with_focus += 1

            metrics["images_total"] = img_total
            metrics["images_missing_alt"] = img_missing_alt
            metrics["images_empty_alt"] = img_empty_alt
            metrics["images_alt_with_focus_keyword"] = img_alt_with_focus

            if img_missing_alt:
                issues.append(
                    SEOIssue(
                        code="IMAGES_MISSING_ALT",
                        severity="warning",
                        category="images",
                        value=img_missing_alt,
                        extra={"message": "Images without alt attribute; affects accessibility and image SEO."},
                    )
                )
            if img_empty_alt:
                issues.append(
                    SEOIssue(
                        code="IMAGES_EMPTY_ALT",
                        severity="info",
                        category="images",
                        value=img_empty_alt,
                        extra={"message": "Images with empty alt text; check if they should describe content."},
                    )
                )
            if focus_keywords and img_total > 0 and img_alt_with_focus == 0:
                issues.append(
                    SEOIssue(
                        code="IMAGES_ALT_MISSING_FOCUS_KEYWORDS",
                        severity="info",
                        category="images",
                        value=focus_keywords,
                        extra={"message": "No image alt text contains focus keywords; consider optimizing main visuals."},
                    )
                )

            # STRUCTURED DATA / SCHEMA.ORG
            structured_blocks = 0
            structured_types: Counter = Counter()
            rating_values: List[float] = []
            rating_counts: List[int] = []
            schema_errors = 0
            social_profiles: Set[str] = set()
            has_website_schema = False
            has_org_schema = False

            for script in soup.find_all("script", type="application/ld+json"):
                if not script.string:
                    continue
                structured_blocks += 1
                try:
                    data = json.loads(script.string)
                except Exception:
                    schema_errors += 1
                    issues.append(
                        SEOIssue(
                            code="STRUCTURED_DATA_INVALID_JSON",
                            severity="error",
                            category="structured_data",
                            extra={"message": "Invalid JSON-LD block; fix syntax errors."},
                        )
                    )
                    continue

                if isinstance(data, list):
                    items = data
                else:
                    items = [data]

                for item in items:
                    if not isinstance(item, dict):
                        continue
                    t = item.get("@type")
                    types_here: List[str] = []
                    if isinstance(t, list):
                        for tt in t:
                            structured_types[str(tt)] += 1
                            types_here.append(str(tt))
                    elif isinstance(t, str):
                        structured_types[t] += 1
                        types_here.append(t)

                    if "WebSite" in types_here:
                        has_website_schema = True
                    if any(tt in ("Organization", "LocalBusiness") for tt in types_here):
                        has_org_schema = True

                    same_as = item.get("sameAs")
                    if isinstance(same_as, list):
                        for url_sa in same_as:
                            if isinstance(url_sa, str):
                                social_profiles.add(url_sa)
                    elif isinstance(same_as, str):
                        social_profiles.add(same_as)

                    agg = item.get("aggregateRating")
                    if isinstance(agg, dict):
                        rv = agg.get("ratingValue")
                        rc = agg.get("reviewCount") or agg.get("ratingCount")
                        try:
                            if rv is not None:
                                rating_values.append(float(rv))
                        except (TypeError, ValueError):
                            pass
                        try:
                            if rc is not None:
                                rating_counts.append(int(rc))
                        except (TypeError, ValueError):
                            pass

            metrics["structured_data_blocks"] = structured_blocks
            metrics["structured_data_types"] = dict(structured_types)
            metrics["structured_data_errors"] = schema_errors
            metrics["rating_values"] = rating_values
            metrics["rating_counts"] = rating_counts
            metrics["rating_value_avg"] = sum(rating_values) / len(rating_values) if rating_values else None
            metrics["rating_count_sum"] = sum(rating_counts) if rating_counts else 0
            metrics["social_profiles_sameAs"] = sorted(social_profiles)
            metrics["has_website_schema"] = has_website_schema
            metrics["has_organization_schema"] = has_org_schema

            if structured_blocks == 0:
                issues.append(
                    SEOIssue(
                        code="STRUCTURED_DATA_MISSING",
                        severity="info",
                        category="structured_data",
                        extra={"message": "No JSON-LD structured data found; consider schema.org for key entities."},
                    )
                )

            # Breadcrumbs
            has_breadcrumb_schema = "BreadcrumbList" in structured_types
            has_breadcrumb_markup = bool(soup.find(attrs={"itemtype": re.compile("BreadcrumbList", re.I)}))
            metrics["has_breadcrumbs"] = has_breadcrumb_schema or has_breadcrumb_markup

            # Formularios / labels
            form_inputs = soup.find_all(["input", "textarea"])
            inputs_without_label = 0
            for inp in form_inputs:
                if inp.get("type") in ("hidden", "submit", "button", "image", "reset"):
                    continue
                has_label = False
                inp_id = inp.get("id")
                if inp_id:
                    label = soup.find("label", attrs={"for": inp_id})
                    if label:
                        has_label = True
                if not has_label:
                    parent = inp.parent
                    while parent is not None and parent != soup:
                        if parent.name == "label":
                            has_label = True
                            break
                        parent = parent.parent
                if not has_label:
                    if inp.get("aria-label") or inp.get("aria-labelledby"):
                        has_label = True
                if not has_label:
                    inputs_without_label += 1

            metrics["form_inputs_without_label"] = inputs_without_label
            if inputs_without_label:
                issues.append(
                    SEOIssue(
                        code="FORM_INPUTS_WITHOUT_LABEL",
                        severity="info",
                        category="accessibility",
                        value=inputs_without_label,
                        extra={"message": "Form fields without label or aria-label; hurts accessibility."},
                    )
                )

        except Exception as e:
            issues.append(
                SEOIssue(
                    code="EXCEPTION",
                    severity="error",
                    category="technical",
                    value=str(e),
                    extra={"message": "Unexpected exception while auditing URL."},
                )
            )
            status = 0
            metrics["status"] = status

        return SEOPageResult(url=url, status=status, metrics=metrics, issues=issues)

    # ---------------------------
    # Ejecución
    # ---------------------------
    def run(self) -> Dict[str, Any]:
        self._fetch_robots()
        global_issues: List[SEOIssue] = []

        if self.robots_status is None or self.robots_status == 0:
            global_issues.append(
                SEOIssue(
                    code="ROBOTS_TXT_UNREACHABLE",
                    severity="info",
                    category="technical",
                    extra={"message": "robots.txt not reachable or error fetching it."},
                )
            )
        elif self.robots_status == 404:
            global_issues.append(
                SEOIssue(
                    code="ROBOTS_TXT_MISSING",
                    severity="info",
                    category="technical",
                    extra={"message": "robots.txt not found; recommended to have one even if mostly empty."},
                )
            )
        elif self._check_robots_all_disallowed():
            global_issues.append(
                SEOIssue(
                    code="ROBOTS_ALL_DISALLOWED",
                    severity="error",
                    category="indexing",
                    extra={"message": "robots.txt disallows all crawling for User-agent: *."},
                )
            )

        if self.use_sitemap:
            urls = self._get_urls_from_sitemap()
        else:
            urls = self._crawl_site_bfs()

        pages_results: List[SEOPageResult] = []
        for url in urls:
            result = self.audit_url(url)
            pages_results.append(result)

        # Duplicados de title y meta description entre páginas
        title_map: Dict[str, List[SEOPageResult]] = {}
        desc_map: Dict[str, List[SEOPageResult]] = {}

        for r in pages_results:
            title = (r.metrics.get("title") or "").strip()
            if title:
                title_map.setdefault(title, []).append(r)
            desc = (r.metrics.get("meta_description") or "").strip()
            if desc:
                desc_map.setdefault(desc, []).append(r)

        for title, plist in title_map.items():
            if len(plist) > 1:
                urls_dup = [p.url for p in plist]
                global_issues.append(
                    SEOIssue(
                        code="DUPLICATE_TITLE_GROUP",
                        severity="warning",
                        category="meta",
                        value=title,
                        extra={"urls": urls_dup},
                    )
                )
                for p in plist:
                    p.issues.append(
                        SEOIssue(
                            code="TITLE_DUPLICATED",
                            severity="warning",
                            category="meta",
                            value=title,
                            extra={"urls_same_title": urls_dup},
                        )
                    )

        for desc, plist in desc_map.items():
            if len(plist) > 1:
                urls_dup = [p.url for p in plist]
                global_issues.append(
                    SEOIssue(
                        code="DUPLICATE_META_DESC_GROUP",
                        severity="warning",
                        category="meta",
                        value=desc[:120] + ("..." if len(desc) > 120 else ""),
                        extra={"urls": urls_dup},
                    )
                )
                for p in plist:
                    p.issues.append(
                        SEOIssue(
                            code="META_DESC_DUPLICATED",
                            severity="warning",
                            category="meta",
                            value=desc[:120] + ("..." if len(desc) > 120 else ""),
                            extra={"urls_same_meta_desc": urls_dup},
                        )
                    )

        # Enlaces entrantes (orphan pages aproximadas)
        for r in pages_results:
            norm = self._normalize_for_visit(r.url)
            inbound = self.inbound_link_counts.get(norm, 0)
            r.metrics["inbound_internal_links"] = int(inbound)
            if inbound == 0 and r.url != self.base_url:
                r.issues.append(
                    SEOIssue(
                        code="POSSIBLE_ORPHAN_PAGE",
                        severity="info",
                        category="links",
                        extra={"message": "No internal links pointing to this URL within crawled pages."},
                    )
                )

        # Conteo global de errores/avisos
        total_errors = 0
        total_warnings = 0
        for i in global_issues:
            if i.severity == "error":
                total_errors += 1
            elif i.severity == "warning":
                total_warnings += 1
        for r in pages_results:
            for i in r.issues:
                if i.severity == "error":
                    total_errors += 1
                elif i.severity == "warning":
                    total_warnings += 1

        report = {
            "base_url": self.base_url,
            "total_pages": len(pages_results),
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "global_issues": [asdict(i) for i in global_issues],
            "pages": [
                {
                    "url": r.url,
                    "status": r.status,
                    "metrics": r.metrics,
                    "issues": [asdict(i) for i in r.issues],
                }
                for r in pages_results
            ],
        }
        return report


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Maximized HTML/SEO on-page auditor (sin PageSpeed).")
    parser.add_argument("url", help="Base URL (e.g. https://pablocirre.es)")
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES, help="Máximo de páginas a auditar.")
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Timeout HTTP en segundos (por defecto 10).",
    )
    parser.add_argument(
        "--use-sitemap",
        action="store_true",
        help="Usar sitemap.xml (si existe) en vez de rastreo BFS.",
    )
    parser.add_argument(
        "--sitemap-url",
        help="URL específica de sitemap (opcional). Si se indica, fuerza su uso.",
    )
    parser.add_argument(
        "--check-links",
        action="store_true",
        help="Comprobar si los enlaces internos están rotos (requiere peticiones extra).",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args(sys.argv[1:])

    auditor = SEOAuditor(
        base_url=args.url,
        max_pages=args.max_pages,
        timeout=args.timeout,
        use_sitemap=args.use_sitemap,
        sitemap_url=args.sitemap_url,
        check_links=args.check_links,
    )
    report = auditor.run()
    
    # Save to Reports directory
    # .../Tools/seo/audit.py -> .../Tools/seo -> .../Tools -> .../Root
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    reports_dir = os.path.join(root_dir, "Reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"seo_report_{timestamp}.json"
    filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"Report saved to: {filepath}")


if __name__ == "__main__":
    main()
