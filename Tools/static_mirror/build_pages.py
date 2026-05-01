#!/usr/bin/env python3
"""Build a static GitHub Pages mirror from the public PHP site.

The source site stays PHP-based. This tool starts a temporary local PHP server,
renders every public URL listed in the sitemap index, rewrites dynamic/internal
URLs to static GitHub Pages paths, and copies only static public assets.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_BASE_URL = "https://pablocirre.es"
SOURCE_HOSTS = {"pablocirre.es", "www.pablocirre.es"}
LOCAL_BASE_PREFIX = "/PabloCirre"
DEFAULT_OUTPUT = ROOT.parent / "PabloCirre.github.io"
TEXT_FILE_EXTENSIONS = {".css", ".html", ".js", ".json", ".svg", ".txt", ".xml"}
COPY_DIRS = ("assets",)
ROOT_TEXT_FILES = (
    "google64a9eb2298feecce.html",
    "llms-full.txt",
    "llms.txt",
    "robots.txt",
    "y84ksrzioy4v54orbq50vy4qxnq6wpi1.txt",
)
PUBLIC_SITEMAP_RE = re.compile(r"^/sitemap(?:_[a-z0-9-]+)?\.xml$", re.IGNORECASE)
ABSOLUTE_SOURCE_URL_RE = re.compile(
    r"https?://(?:www\.)?pablocirre\.es(?:/[^\s\"'<>)]*)?",
    re.IGNORECASE,
)
LOCAL_SERVER_URL_RE = re.compile(
    r"https?://127\.0\.0\.1:\d+(?:/PabloCirre)?(?:/[^\s\"'<>)]*)?",
    re.IGNORECASE,
)
HTML_ATTR_URL_RE = re.compile(
    r"\b(?P<attr>href|src|action|poster)\s*=\s*(?P<quote>[\"'])(?P<value>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
QUOTED_INTERNAL_PATH_RE = re.compile(
    r"(?P<quote>[\"'`])(?P<value>/(?:PabloCirre/)?(?:paginas|en|assets|vocalware|labs|sitemap)[^\"'`]*)"
    r"(?P=quote)",
    re.IGNORECASE,
)
CONTACT_EMAIL = "pablo@centraldecomunicacion.es"
HIGH_RISK_PERSONAL_MARKERS = (
    "pablo cirre ha muerto",
    "pablo cirre fallecido",
    "pablo cirre ha fallecido",
    "fallecimiento de pablo cirre",
    "in memoriam pablo cirre",
    "obituario pablo cirre",
    "memorial pablo cirre",
)
GENERIC_DEATH_MARKERS = (
    "muerto",
    "muerte",
    "fallecid",
    "fallecimiento",
    "memorial",
    "obituario",
    "dead",
    "death",
    "deceased",
    "obituary",
)


@dataclass(frozen=True)
class Route:
    source_url: str
    local_url: str
    static_path: str
    output_file: Path


def normalize_base_url(value: str) -> str:
    parsed = urllib.parse.urlparse(value)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("--base-url must be an absolute URL, for example https://pablocirre.github.io")
    return value.rstrip("/")


def base_url_path(base_url: str) -> str:
    path = urllib.parse.urlparse(base_url).path.rstrip("/")
    return "" if path == "/" else path


def join_base_path(base_url: str, path: str) -> str:
    prefix = base_url_path(base_url)
    if not path.startswith("/"):
        path = "/" + path
    return prefix + path


def absolute_static_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + join_base_path(base_url, path)


def is_probably_asset_path(path: str) -> bool:
    suffix = Path(urllib.parse.urlparse(path).path).suffix.lower()
    return bool(suffix and suffix not in {".php"})


def strip_runtime_prefix(path: str) -> str:
    if path == LOCAL_BASE_PREFIX:
        return "/"
    if path.lower().startswith(LOCAL_BASE_PREFIX.lower() + "/"):
        return path[len(LOCAL_BASE_PREFIX) :]
    return path


def slug_from_query(query: str) -> str:
    values = urllib.parse.parse_qs(query).get("slug", [])
    if not values:
        return ""
    slug = values[0].strip().lower()
    slug = re.sub(r"[^a-z0-9-]+", "-", slug)
    return slug.strip("-")


def page_path_from_url(url_or_path: str) -> str:
    """Return the canonical static URL path for a public page URL."""
    parsed = urllib.parse.urlparse(html.unescape(url_or_path))
    path = urllib.parse.unquote(parsed.path or "/")
    query = parsed.query
    path = re.sub(r"/+", "/", strip_runtime_prefix(path)) or "/"

    lang_prefix = ""
    route_path = path
    if route_path.lower() == "/en":
        route_path = "/en/"
    if route_path.lower().startswith("/en/"):
        lang_prefix = "/en"
        route_path = route_path[3:] or "/"

    route_lower = route_path.lower()
    project_slug = slug_from_query(query)
    if route_lower == "/paginas/projects/project.php" and project_slug:
        return f"{lang_prefix}/paginas/projects/{project_slug}/"

    if route_lower.endswith("/index.php"):
        route_path = route_path[: -len("index.php")]
    elif route_lower.endswith(".php"):
        route_path = route_path[:-4]

    if route_path == "":
        route_path = "/"
    if not route_path.startswith("/"):
        route_path = "/" + route_path

    if not is_probably_asset_path(route_path) and route_path != "/" and not route_path.endswith("/"):
        route_path += "/"

    combined = lang_prefix + (route_path if route_path.startswith("/") else "/" + route_path)
    combined = re.sub(r"/+", "/", combined)
    if combined.lower().startswith(("/paginas/", "/en/paginas/", "/vocalware/", "/en/vocalware/")):
        combined = combined.lower()
    return combined


def output_file_for_path(output_dir: Path, static_path: str) -> Path:
    path = static_path.strip("/")
    if static_path == "/":
        return output_dir / "index.html"
    if Path(path).suffix:
        return output_dir / path
    return output_dir / path / "index.html"


def local_url_for_source(source_url: str, port: int) -> str:
    parsed = urllib.parse.urlparse(source_url)
    return urllib.parse.urlunparse(
        ("http", f"127.0.0.1:{port}", parsed.path or "/", "", parsed.query, parsed.fragment)
    )


def route_for_source(source_url: str, output_dir: Path, port: int) -> Route:
    static_path = page_path_from_url(source_url)
    return Route(
        source_url=source_url,
        local_url=local_url_for_source(source_url, port),
        static_path=static_path,
        output_file=output_file_for_path(output_dir, static_path),
    )


def local_sitemap_path_from_url(loc: str) -> Path | None:
    parsed = urllib.parse.urlparse(loc)
    if parsed.netloc and parsed.netloc.lower() not in SOURCE_HOSTS:
        return None
    path = urllib.parse.unquote(parsed.path or "").lstrip("/")
    if not path:
        return None
    candidate = (ROOT / path).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def collect_sitemap_files(index_path: Path) -> list[Path]:
    visited: set[Path] = set()
    ordered: list[Path] = []

    def visit(path: Path) -> None:
        resolved = path.resolve()
        if resolved in visited:
            return
        visited.add(resolved)
        ordered.append(resolved)
        root = ET.parse(resolved).getroot()
        if root.tag.endswith("sitemapindex"):
            for loc in root.findall(".//{*}sitemap/{*}loc"):
                if not loc.text:
                    continue
                child = local_sitemap_path_from_url(loc.text.strip())
                if child:
                    visit(child)

    visit(index_path)
    return ordered


def collect_public_urls(index_path: Path) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for sitemap_path in collect_sitemap_files(index_path):
        root = ET.parse(sitemap_path).getroot()
        if not root.tag.endswith("urlset"):
            continue
        for loc in root.findall(".//{*}url/{*}loc"):
            if not loc.text:
                continue
            url = loc.text.strip()
            if url not in seen:
                urls.append(url)
                seen.add(url)
    return urls


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def router_php_source() -> str:
    root_json = json.dumps(str(ROOT).replace("\\", "/"))
    return f"""<?php
$root = {root_json};
chdir($root);

function pc_static_resolve_case_path(string $root, string $path): string {{
    $path = '/' . ltrim($path, '/');
    $parts = array_values(array_filter(explode('/', $path), 'strlen'));
    $current = rtrim($root, '/');
    foreach ($parts as $part) {{
        if (!is_dir($current)) {{
            return $current . '/' . $part;
        }}
        $matched = null;
        foreach (scandir($current) ?: [] as $entry) {{
            if ($entry === '.' || $entry === '..') {{
                continue;
            }}
            if (strcasecmp($entry, $part) === 0) {{
                $matched = $entry;
                break;
            }}
        }}
        $current .= '/' . ($matched ?? $part);
    }}
    return $current;
}}

$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = parse_url($uri, PHP_URL_PATH) ?: '/';
$path = rawurldecode($path);
$path = preg_replace('#/+#', '/', $path) ?: '/';

if (stripos($path, '/PabloCirre/') === 0) {{
    $path = substr($path, strlen('/PabloCirre'));
}} elseif (strcasecmp($path, '/PabloCirre') === 0) {{
    $path = '/';
}}

$dispatchPath = $path;
if (preg_match('#^/en(?:/|$)#i', $dispatchPath)) {{
    $dispatchPath = substr($dispatchPath, 3);
    if ($dispatchPath === '') {{
        $dispatchPath = '/';
    }}
    $_GET['__lang'] = 'en';
    $_REQUEST['__lang'] = 'en';
}}

if ($dispatchPath === '/') {{
    $target = $root . '/index.php';
}} else {{
    $candidate = pc_static_resolve_case_path($root, $dispatchPath);
    if (is_file($candidate) && strtolower(pathinfo($candidate, PATHINFO_EXTENSION)) !== 'php') {{
        return false;
    }}
    if (is_dir($candidate) && is_file($candidate . '/index.php')) {{
        $target = $candidate . '/index.php';
    }} elseif (is_file($candidate) && strtolower(pathinfo($candidate, PATHINFO_EXTENSION)) === 'php') {{
        $target = $candidate;
    }} else {{
        $target = $root . '/404.php';
    }}
}}

$_SERVER['SCRIPT_FILENAME'] = $target;
$_SERVER['SCRIPT_NAME'] = str_replace($root, '', $target);
$_SERVER['PHP_SELF'] = $_SERVER['SCRIPT_NAME'];
$previousCwd = getcwd();
chdir(dirname($target));
include $target;
if ($previousCwd !== false) {{
    chdir($previousCwd);
}}
return true;
"""


def start_php_server(port: int, router_path: Path) -> subprocess.Popen:
    proc = subprocess.Popen(
        ["php", "-S", f"127.0.0.1:{port}", str(router_path)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    deadline = time.time() + 10
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError("PHP server exited early")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return proc
        time.sleep(0.1)
    proc.terminate()
    raise RuntimeError("Timed out waiting for PHP development server")


def stop_php_server(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)


def fetch_url(url: str, timeout: int) -> tuple[int, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "PabloCirreStaticMirror/1.0",
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            content_type = response.headers.get("content-type", "")
            charset = response.headers.get_content_charset() or "utf-8"
            return int(response.status), body.decode(charset, errors="replace"), content_type
    except urllib.error.HTTPError as exc:
        body = exc.read()
        content_type = exc.headers.get("content-type", "") if exc.headers else ""
        charset = exc.headers.get_content_charset() if exc.headers else None
        return int(exc.code), body.decode(charset or "utf-8", errors="replace"), content_type
    except (TimeoutError, urllib.error.URLError, OSError) as exc:
        return 0, str(exc), "error"


def parse_internal_url(value: str) -> tuple[bool, urllib.parse.ParseResult]:
    decoded = html.unescape(value.strip())
    if not decoded or decoded.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return False, urllib.parse.urlparse(decoded)
    if decoded.startswith("//"):
        return False, urllib.parse.urlparse(decoded)
    parsed = urllib.parse.urlparse(decoded)
    if parsed.scheme in {"http", "https"}:
        host = parsed.netloc.split("@")[-1].split(":")[0].lower()
        return host in SOURCE_HOSTS or host in {"127.0.0.1", "localhost"} or host == "pablocirre.github.io", parsed
    if decoded.startswith("/"):
        return True, parsed
    return False, parsed


def static_url_for_value(value: str, base_url: str, force_absolute: bool | None = None) -> str:
    decoded = html.unescape(value.strip())
    is_internal, parsed = parse_internal_url(decoded)
    if not is_internal:
        return value

    path = urllib.parse.unquote(parsed.path or "/")
    query = parsed.query
    fragment = ("#" + parsed.fragment) if parsed.fragment else ""
    path = re.sub(r"/+", "/", strip_runtime_prefix(path)) or "/"
    lower_path = path.lower()

    original_was_absolute = parsed.scheme in {"http", "https"}
    absolute = original_was_absolute if force_absolute is None else force_absolute

    if lower_path.startswith("/labs/"):
        suffix = urllib.parse.urlunparse(("", "", path, "", query, parsed.fragment))
        return SOURCE_BASE_URL + suffix

    if lower_path.startswith("/assets/"):
        static_path = path + (("?" + query) if query else "") + fragment
        return absolute_static_url(base_url, static_path) if absolute else join_base_path(base_url, static_path)

    if lower_path == "/robots.txt" or PUBLIC_SITEMAP_RE.match(lower_path):
        static_path = lower_path
        return absolute_static_url(base_url, static_path) if absolute else join_base_path(base_url, static_path)

    static_path = page_path_from_url(urllib.parse.urlunparse(("", "", path, "", query, parsed.fragment)))
    static_path += fragment
    return absolute_static_url(base_url, static_path) if absolute else join_base_path(base_url, static_path)


def rewrite_absolute_source_urls(text: str, base_url: str) -> str:
    text = ABSOLUTE_SOURCE_URL_RE.sub(lambda m: static_url_for_value(m.group(0), base_url, True), text)
    return LOCAL_SERVER_URL_RE.sub(lambda m: static_url_for_value(m.group(0), base_url, True), text)


def rewrite_html_attrs(text: str, base_url: str) -> str:
    def replace(match: re.Match) -> str:
        attr = match.group("attr")
        quote = match.group("quote")
        value = match.group("value")
        rewritten = static_url_for_value(value, base_url)
        return f"{attr}={quote}{html.escape(rewritten, quote=True)}{quote}"

    return HTML_ATTR_URL_RE.sub(replace, text)


def rewrite_quoted_internal_paths(text: str, base_url: str) -> str:
    def replace(match: re.Match) -> str:
        quote = match.group("quote")
        value = match.group("value")
        rewritten = static_url_for_value(value, base_url, False)
        return f"{quote}{rewritten}{quote}"

    return QUOTED_INTERNAL_PATH_RE.sub(replace, text)


def rewrite_common_dynamic_paths(text: str, base_url: str) -> str:
    replacements = {
        "/paginas/legal/aviso-legal.php": join_base_path(base_url, "/paginas/legal/aviso-legal/"),
        "/paginas/legal/privacidad.php": join_base_path(base_url, "/paginas/legal/privacidad/"),
        "/paginas/legal/cookies.php": join_base_path(base_url, "/paginas/legal/cookies/"),
        "/PabloCirre/paginas/legal/aviso-legal.php": join_base_path(base_url, "/paginas/legal/aviso-legal/"),
        "/PabloCirre/paginas/legal/privacidad.php": join_base_path(base_url, "/paginas/legal/privacidad/"),
        "/PabloCirre/paginas/legal/cookies.php": join_base_path(base_url, "/paginas/legal/cookies/"),
    }
    for source, target in replacements.items():
        text = text.replace(source, target)

    def project_slug_replace(match: re.Match) -> str:
        prefix = "/en" if match.group("lang") else ""
        slug = match.group("slug").lower()
        return join_base_path(base_url, f"{prefix}/paginas/projects/{slug}/")

    return re.sub(
        r"(?P<lang>/en)?/paginas/projects/project\.php\?slug=(?P<slug>[a-z0-9-]+)",
        project_slug_replace,
        text,
        flags=re.IGNORECASE,
    )


def clean_i18n_artifacts(text: str) -> str:
    text = re.sub(r"@@PC_I18N_PROTECTED_\d+@@", "", text)
    # The legacy output-level translator can over-translate this project brand.
    return text.replace("Clinicmefis", "Clinicamefis")


def adapt_static_contact_page(text: str) -> str:
    mailto = f"mailto:{CONTACT_EMAIL}"
    text = re.sub(
        r'<form\s+action=""\s+method="POST"\s+class="contact-terminal">',
        f'<form action="{mailto}" method="get" class="contact-terminal static-contact-form">',
        text,
        flags=re.IGNORECASE,
    )
    return text


def remove_local_debug_links(text: str) -> str:
    text = re.sub(
        r'\s*<a\s+href=["\'][^"\']*raw_mode=(?:on|off)[^"\']*["\'][^>]*>\[(?:Raw|Normal)\]</a>',
        "",
        text,
        flags=re.IGNORECASE,
    )
    return re.sub(
        r'\s*<a\b(?=[^>]*\brel=["\']nofollow["\'])(?=[^>]*\bhref=["\'][^"\']*["\'])[^>]*>\[(?:Raw|Normal)\]</a>',
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )


def extract_first_h1(text: str) -> str:
    match = re.search(r"<h1\b[^>]*>(.*?)</h1>", text, re.IGNORECASE | re.DOTALL)
    if not match:
        return "Proyecto"
    raw = re.sub(r"<[^>]+>", " ", match.group(1))
    raw = html.unescape(re.sub(r"\s+", " ", raw)).strip()
    return raw or "Proyecto"


def fix_project_breadcrumb_jsonld(text: str, route: Route, base_url: str) -> str:
    if "/paginas/projects/" not in route.static_path or route.static_path.endswith("/paginas/projects/"):
        return text
    if "/project.php" not in text:
        return text

    title = extract_first_h1(text)
    escaped_title = json.dumps(title, ensure_ascii=False)[1:-1]
    lang_prefix = "/en" if route.static_path.startswith("/en/") else ""
    old_abs = absolute_static_url(base_url, f"{lang_prefix}/paginas/projects/project.php/")
    new_abs = absolute_static_url(base_url, route.static_path)
    text = text.replace(old_abs, new_abs)
    text = text.replace('"name":"Project.php"', f'"name":"{escaped_title}"')
    text = text.replace('"name":"Project"', f'"name":"{escaped_title}"')
    return text


def postprocess_html(text: str, route: Route, base_url: str) -> str:
    text = rewrite_absolute_source_urls(text, base_url)
    text = rewrite_html_attrs(text, base_url)
    text = rewrite_quoted_internal_paths(text, base_url)
    text = rewrite_common_dynamic_paths(text, base_url)
    text = fix_project_breadcrumb_jsonld(text, route, base_url)
    text = remove_local_debug_links(text)
    text = clean_i18n_artifacts(text)
    text = text.replace(f"const BASE_URL = '{LOCAL_BASE_PREFIX}';", f"const BASE_URL = '{base_url_path(base_url)}';")
    if route.static_path in {"/paginas/contact/", "/en/paginas/contact/"}:
        text = adapt_static_contact_page(text)
    return text


def postprocess_text_asset(text: str, base_url: str) -> str:
    text = rewrite_absolute_source_urls(text, base_url)
    text = rewrite_quoted_internal_paths(text, base_url)
    text = rewrite_common_dynamic_paths(text, base_url)
    text = clean_i18n_artifacts(text)
    text = text.replace(f"const BASE_URL = '{LOCAL_BASE_PREFIX}';", f"const BASE_URL = '{base_url_path(base_url)}';")
    return text


def safe_clean_output_dir(output_dir: Path) -> None:
    output_dir = output_dir.resolve()
    root = ROOT.resolve()
    if output_dir == root:
        raise ValueError("Refusing to clean the source repository root")
    if output_dir == root.parent:
        raise ValueError("Refusing to clean the source repository parent")
    if output_dir.anchor == str(output_dir):
        raise ValueError("Refusing to clean a filesystem root")
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in output_dir.iterdir():
        if item.name == ".git":
            continue
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()


def copy_public_assets(output_dir: Path, base_url: str) -> list[str]:
    copied: list[str] = []
    for dirname in COPY_DIRS:
        source = ROOT / dirname
        target = output_dir / dirname
        if not source.exists():
            continue
        shutil.copytree(
            source,
            target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            dirs_exist_ok=True,
        )
        copied.append(dirname)

    for rel in ROOT_TEXT_FILES:
        source = ROOT / rel
        if not source.is_file():
            continue
        target = output_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() in TEXT_FILE_EXTENSIONS:
            target.write_text(postprocess_text_asset(source.read_text(encoding="utf-8", errors="ignore"), base_url), encoding="utf-8")
        else:
            shutil.copy2(source, target)
        copied.append(rel)

    for sitemap_path in collect_sitemap_files(ROOT / "sitemap_index.xml"):
        target = output_dir / sitemap_path.name
        target.write_text(
            postprocess_text_asset(sitemap_path.read_text(encoding="utf-8", errors="ignore"), base_url),
            encoding="utf-8",
        )
        copied.append(sitemap_path.name)

    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    copied.append(".nojekyll")
    return copied


def rewrite_copied_text_files(output_dir: Path, base_url: str) -> None:
    for path in output_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_FILE_EXTENSIONS:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rewritten = postprocess_text_asset(content, base_url)
        if rewritten != content:
            path.write_text(rewritten, encoding="utf-8")


def write_route(route: Route, timeout: int, base_url: str) -> dict:
    status, body, content_type = fetch_url(route.local_url, timeout)
    ok = 200 <= status < 300 and "html" in content_type.lower()
    result = {
        "source_url": route.source_url,
        "local_url": route.local_url,
        "static_path": route.static_path,
        "output_file": str(route.output_file),
        "status": status,
        "content_type": content_type,
        "ok": ok,
    }
    if not ok:
        result["error"] = f"Expected HTML 2xx, got status={status} content_type={content_type!r}"
        return result
    route.output_file.parent.mkdir(parents=True, exist_ok=True)
    route.output_file.write_text(postprocess_html(body, route, base_url), encoding="utf-8")
    return result


def write_404(output_dir: Path, port: int, timeout: int, base_url: str) -> dict:
    local_url = f"http://127.0.0.1:{port}/__static_mirror_missing__/"
    route = Route(
        source_url=SOURCE_BASE_URL + "/__static_mirror_missing__/",
        local_url=local_url,
        static_path="/404.html",
        output_file=output_dir / "404.html",
    )
    status, body, content_type = fetch_url(local_url, timeout)
    route.output_file.write_text(postprocess_html(body, route, base_url), encoding="utf-8")
    return {"status": status, "content_type": content_type, "ok": status == 404}


def validate_output(output_dir: Path, routes: list[Route], build_results: list[dict], base_url: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    failed_fetches = [item for item in build_results if not item.get("ok")]
    if failed_fetches:
        errors.append(f"{len(failed_fetches)} page fetches failed")

    expected_outputs = {route.output_file.resolve() for route in routes}
    html_outputs = {path.resolve() for path in output_dir.rglob("*.html") if path.name != "404.html"}
    missing = sorted(str(path.relative_to(output_dir)) for path in expected_outputs if not path.exists())
    allowed_extra_html = {
        (output_dir / rel).resolve()
        for rel in ROOT_TEXT_FILES
        if Path(rel).suffix.lower() == ".html"
    }
    extra_or_derived = html_outputs - expected_outputs - allowed_extra_html
    if missing:
        errors.append(f"Missing generated HTML files: {missing[:8]}")
    if len(expected_outputs) != len(routes):
        errors.append("Multiple source URLs map to the same static output path")
    if extra_or_derived:
        warnings.append(f"{len(extra_or_derived)} HTML files are copied/generated outside sitemap routes")

    forbidden_segments = {".git", "secrets", ".secrets", "Reports", "tmp", "__pycache__"}
    copied_forbidden = [
        str(path.relative_to(output_dir))
        for path in output_dir.rglob("*")
        if any(part in forbidden_segments for part in path.relative_to(output_dir).parts)
    ]
    if copied_forbidden:
        errors.append(f"Forbidden local/private paths copied: {copied_forbidden[:8]}")

    canonical_original = []
    internal_php_links = []
    php_runtime_errors = []
    i18n_artifacts = []
    high_risk_hits = []
    generic_marker_hits = []
    for path in output_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_FILE_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = str(path.relative_to(output_dir))
        if re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']https://pablocirre\.es', text, re.IGNORECASE):
            canonical_original.append(rel)
        if re.search(
            r'(?:\b(?:href|src|action)=["\'][^"\']*|https://pablocirre\.github\.io/|["\']/?)(?:en/)?paginas/[^"\'<>\s]*\.php',
            text,
            re.IGNORECASE,
        ):
            internal_php_links.append(rel)
        if re.search(r"\b(?:Warning|Fatal error|Parse error|Notice):|undefined function|Undefined constant", text, re.IGNORECASE):
            php_runtime_errors.append(rel)
        if "@@PC_I18N_PROTECTED_" in text:
            i18n_artifacts.append(rel)
        lowered = text.lower()
        for marker in HIGH_RISK_PERSONAL_MARKERS:
            if marker in lowered:
                high_risk_hits.append({"file": rel, "marker": marker})
        for marker in GENERIC_DEATH_MARKERS:
            if marker in lowered:
                generic_marker_hits.append({"file": rel, "marker": marker})
                break

    if canonical_original:
        errors.append(f"Canonical tags still point at pablocirre.es: {canonical_original[:8]}")
    if internal_php_links:
        errors.append(f"Internal .php links remain in generated output: {internal_php_links[:8]}")
    if php_runtime_errors:
        errors.append(f"PHP warnings/errors leaked into generated output: {php_runtime_errors[:8]}")
    if i18n_artifacts:
        errors.append(f"i18n placeholder artifacts leaked into generated output: {i18n_artifacts[:8]}")
    if high_risk_hits:
        errors.append(f"Personal death/memorial markers found: {high_risk_hits[:8]}")
    if generic_marker_hits:
        warnings.append(
            "Generic death-related words exist in source content, but not personal memorial markers: "
            + ", ".join(sorted({item["file"] for item in generic_marker_hits})[:8])
        )

    sitemap_index = output_dir / "sitemap_index.xml"
    robots = output_dir / "robots.txt"
    if sitemap_index.exists() and base_url.rstrip("/") not in sitemap_index.read_text(encoding="utf-8", errors="ignore"):
        errors.append("sitemap_index.xml does not reference the target base URL")
    if robots.exists() and f"Sitemap: {base_url.rstrip()}/sitemap_index.xml" not in robots.read_text(encoding="utf-8", errors="ignore"):
        errors.append("robots.txt does not reference the target sitemap index")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "expected_route_count": len(routes),
        "generated_html_count": len(expected_outputs),
    }


def build(args: argparse.Namespace) -> int:
    base_url = normalize_base_url(args.base_url)
    output_dir = Path(args.output).resolve()
    safe_clean_output_dir(output_dir)

    public_urls = collect_public_urls(ROOT / args.sitemap_index)
    port = args.port or find_free_port()

    with tempfile.TemporaryDirectory(prefix="pc-static-router-") as temp_dir:
        router_path = Path(temp_dir) / "router.php"
        router_path.write_text(router_php_source(), encoding="utf-8")
        proc = start_php_server(port, router_path)
        try:
            routes = [route_for_source(url, output_dir, port) for url in public_urls]
            copied = copy_public_assets(output_dir, base_url)
            results = []
            for index, route in enumerate(routes, start=1):
                print(f"[{index:03d}/{len(routes):03d}] {route.source_url} -> {route.static_path}")
                results.append(write_route(route, args.timeout, base_url))
            not_found = write_404(output_dir, port, args.timeout, base_url)
        finally:
            stop_php_server(proc)

    rewrite_copied_text_files(output_dir, base_url)
    validation = validate_output(output_dir, routes, results, base_url)
    report = {
        "base_url": base_url,
        "output_dir": str(output_dir),
        "source_url_count": len(public_urls),
        "copied": copied,
        "routes": results,
        "not_found": not_found,
        "validation": validation,
    }
    report_path = output_dir / "static-mirror-report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(validation, indent=2, ensure_ascii=False))
    if not validation["ok"]:
        print(f"Build completed with validation errors. Report: {report_path}", file=sys.stderr)
        return 1
    print(f"Static mirror ready: {output_dir}")
    print(f"Report: {report_path}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the static GitHub Pages mirror.")
    parser.add_argument("--base-url", default="https://pablocirre.github.io", help="Public base URL for the mirror.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output directory. Existing contents are replaced except .git.")
    parser.add_argument("--sitemap-index", default="sitemap_index.xml", help="Sitemap index path relative to the repo root.")
    parser.add_argument("--timeout", type=int, default=20, help="Per-page fetch timeout in seconds.")
    parser.add_argument("--port", type=int, default=0, help="Optional local PHP server port.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    return build(parse_args(argv or sys.argv[1:]))


if __name__ == "__main__":
    raise SystemExit(main())
