#!/usr/bin/env python3
import sys
import os
import json
import argparse
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from urllib.parse import urlparse

import datetime

PAGESPEED_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
DEFAULT_TIMEOUT = 60


@dataclass
class Issue:
    code: str               # e.g. PERFORMANCE_SCORE_VERY_LOW
    severity: str           # "error" | "warning" | "info"
    category: str           # "api" | "performance" | "ux" | "core_web_vitals" | "lighthouse"
    value: Optional[Any] = None
    limit: Optional[Any] = None
    extra: Optional[Dict[str, Any]] = None  # incluye "solution" y contexto


@dataclass
class AuditSummary:
    id: str
    title: Optional[str]
    score: Optional[float]
    score_display_mode: Optional[str]
    numeric_value: Optional[float]
    numeric_unit: Optional[str]
    display_value: Optional[str]
    description: Optional[str]
    warnings: Optional[Any]
    details_type: Optional[str]
    group: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "score": self.score,
            "score_display_mode": self.score_display_mode,
            "numeric_value": self.numeric_value,
            "numeric_unit": self.numeric_unit,
            "display_value": self.display_value,
            "description": self.description,
            "warnings": self.warnings,
            "details_type": self.details_type,
            "group": self.group,
        }


@dataclass
class PageResult:
    url: str
    strategy: str           # "mobile" | "desktop"
    status_code: Optional[int]
    metrics: Dict[str, Any]
    issues: List[Issue]
    audits: Dict[str, List[AuditSummary]]  # failed, passed, not_applicable, manual, informative, opportunities, diagnostics

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "strategy": self.strategy,
            "status": self.status_code,
            "metrics": self.metrics,
            "issues": [asdict(i) for i in self.issues],
            "audits": {k: [a.to_dict() for a in v] for k, v in self.audits.items()},
        }


class PageSpeedAuditor:
    """
    Auditor 'maximizado' basado SOLO en PageSpeed Insights / Lighthouse.
    No hace checks manuales de SEO/HTML: todo viene de la API.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        sitemap_url: Optional[str] = None,
        max_pages: Optional[int] = None,
        timeout: int = DEFAULT_TIMEOUT,
        workers: int = 4,
        include_raw: bool = False,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.sitemap_url = sitemap_url
        self.max_pages = max_pages
        self.timeout = timeout
        self.workers = max(1, workers)
        self.include_raw = include_raw

        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "PageSpeed-Audit/3.0 (+https://example.com)"}
        )

        self.domain = self._extract_domain(self.base_url)
        self.results: List[PageResult] = []
        self.global_issues: List[Issue] = []

    # ---------------------------
    # Utilities
    # ---------------------------
    @staticmethod
    def load_local_key() -> Optional[str]:
        """Load key from local file python/PageSpeed/PageSpeedInsightAP1.txt"""
        try:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PageSpeedInsightAP1.txt")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read().strip()
        except Exception:
            pass
        return None

    @staticmethod
    def _extract_domain(url: str) -> Optional[str]:
        try:
            return urlparse(url).netloc
        except Exception:
            return None

    def _add_issue(
        self,
        issues: List[Issue],
        code: str,
        severity: str,
        category: str,
        value: Any = None,
        limit: Any = None,
        solution: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        extra_data = extra.copy() if extra else {}
        if solution:
            extra_data.setdefault("solution", solution)
        issues.append(
            Issue(
                code=code,
                severity=severity,
                category=category,
                value=value,
                limit=limit,
                extra=extra_data or None,
            )
        )

    # ---------------------------
    # Sitemap discovery
    # ---------------------------
    def get_sitemap_urls(self) -> List[str]:
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
            # No sitemap → solo la URL base
            return [self.base_url]

        namespaces = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls: List[str] = []

        # sitemap index
        sitemap_tags = root.findall(".//ns:sitemap", namespaces) or root.findall(".//sitemap")
        if sitemap_tags:
            for sm in sitemap_tags:
                loc = sm.find("ns:loc", namespaces) or sm.find("loc")
                if loc is None or not loc.text:
                    continue
                sub_url = loc.text.strip()
                try:
                    resp = self.session.get(sub_url, timeout=self.timeout)
                    if resp.status_code != 200:
                        continue
                    sub_root = ET.fromstring(resp.content)
                    url_tags = sub_root.findall(".//ns:url/ns:loc", namespaces) or sub_root.findall(
                        ".//url/loc"
                    )
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

        # Filtra dominio y deduplica
        clean_urls: List[str] = []
        seen: Set[str] = set()
        for u in urls:
            parsed = urlparse(u)
            if parsed.netloc and self.domain and parsed.netloc != self.domain:
                continue
            if u not in seen:
                seen.add(u)
                clean_urls.append(u)

        if self.max_pages:
            clean_urls = clean_urls[: self.max_pages]
        return clean_urls or [self.base_url]

    # ---------------------------
    # PageSpeed API call
    # ---------------------------
    def call_pagespeed(self, url: str, strategy: str) -> PageResult:
        params: Dict[str, Any] = {
            "url": url,
            "strategy": strategy,
            "category": [
                "performance",
                "accessibility",
                "best-practices",
                "seo",
                "pwa",
            ],
        }
        if self.api_key:
            params["key"] = self.api_key

        metrics: Dict[str, Any] = {
            "strategy": strategy,
            "requested_url": url,
        }
        issues: List[Issue] = []
        audits_result: Dict[str, List[AuditSummary]] = {
            "failed": [],
            "passed": [],
            "not_applicable": [],
            "manual": [],
            "informative": [],
            "opportunities": [],
            "diagnostics": [],
        }

        # Llamada a la API
        try:
            resp = self.session.get(PAGESPEED_ENDPOINT, params=params, timeout=self.timeout)
        except requests.RequestException as e:
            self._add_issue(
                issues,
                code="REQUEST_EXCEPTION",
                severity="error",
                category="api",
                value=str(e),
                solution=(
                    "Revisa la conexión a Internet del servidor que ejecuta el script, "
                    "el firewall y cualquier proxy. Asegúrate de que se permite tráfico HTTPS "
                    "hacia las APIs de Google."
                ),
            )
            return PageResult(url=url, strategy=strategy, status_code=None, metrics=metrics, issues=issues, audits=audits_result)

        status_code = resp.status_code

        # Parse JSON incluso si no es 200
        try:
            data = resp.json()
        except Exception as e:
            self._add_issue(
                issues,
                code="INVALID_JSON_RESPONSE",
                severity="error",
                category="api",
                value={"status_code": status_code, "message": str(e)},
                solution=(
                    "La API ha devuelto una respuesta no válida. Vuelve a intentarlo. "
                    "Si persiste, revisa cambios recientes en PageSpeed Insights API o en los parámetros enviados."
                ),
            )
            return PageResult(url=url, strategy=strategy, status_code=status_code, metrics=metrics, issues=issues, audits=audits_result)

        # Error de API (4xx/5xx o campo error)
        if status_code != 200 or "error" in data:
            self._handle_api_error(data, status_code, issues)
            return PageResult(url=url, strategy=strategy, status_code=status_code, metrics=metrics, issues=issues, audits=audits_result)

        lighthouse = data.get("lighthouseResult") or {}
        if not lighthouse:
            self._add_issue(
                issues,
                code="LIGHTHOUSE_RESULT_MISSING",
                severity="error",
                category="api",
                value={"status_code": status_code},
                solution=(
                    "La API ha respondido pero sin resultados de Lighthouse. "
                    "Vuelve a lanzar el análisis y, si persiste, revisa el endpoint y parámetros usados."
                ),
            )
            return PageResult(url=url, strategy=strategy, status_code=status_code, metrics=metrics, issues=issues, audits=audits_result)

        # Runtime error interno de Lighthouse
        runtime_error = lighthouse.get("runtimeError")
        if runtime_error:
            self._add_issue(
                issues,
                code="LIGHTHOUSE_RUNTIME_ERROR",
                severity="error",
                category="api",
                value={"code": runtime_error.get("code"), "message": runtime_error.get("message")},
                solution=(
                    "Lighthouse no ha podido completar el análisis. Comprueba que la URL es accesible sin bloqueos, "
                    "sin redirecciones infinitas ni errores de JS críticos, y vuelve a lanzar PageSpeed Insights."
                ),
            )

        # Meta básica
        metrics["final_url"] = lighthouse.get("finalUrl")
        metrics["lighthouse_version"] = lighthouse.get("lighthouseVersion")
        metrics["analysis_timestamp"] = lighthouse.get("fetchTime")
        metrics["user_agent"] = lighthouse.get("userAgent")
        metrics["config_settings"] = lighthouse.get("configSettings")

        # Raw opcional (muy pesado)
        if self.include_raw:
            metrics["raw"] = {
                "lighthouseResult": lighthouse,
                "loadingExperience": data.get("loadingExperience"),
                "originLoadingExperience": data.get("originLoadingExperience"),
                "analysisUTCTimestamp": data.get("analysisUTCTimestamp"),
            }

        # ---- Scores por categoría (0–100) ----
        categories_obj = lighthouse.get("categories") or {}
        scores: Dict[str, Optional[float]] = {}

        def get_cat_score(cat_id: str) -> Optional[float]:
            cat = categories_obj.get(cat_id)
            if isinstance(cat, dict):
                val = cat.get("score")
                if isinstance(val, (int, float)):
                    return round(val * 100, 1)
            return None

        scores["performance"] = get_cat_score("performance")
        scores["accessibility"] = get_cat_score("accessibility")
        scores["best_practices"] = get_cat_score("best-practices")
        scores["seo"] = get_cat_score("seo")
        scores["pwa"] = get_cat_score("pwa")
        metrics["scores"] = scores

        audits = lighthouse.get("audits") or {}

        # ---- Métricas de laboratorio ----
        def get_numeric(audit_id: str) -> Optional[float]:
            audit = audits.get(audit_id)
            if not isinstance(audit, dict):
                return None
            val = audit.get("numericValue")
            return float(val) if isinstance(val, (int, float)) else None

        lab: Dict[str, Optional[float]] = {
            "first_contentful_paint_ms": get_numeric("first-contentful-paint"),
            "largest_contentful_paint_ms": get_numeric("largest-contentful-paint"),
            "speed_index_ms": get_numeric("speed-index"),
            "total_blocking_time_ms": get_numeric("total-blocking-time"),
            "time_to_interactive_ms": get_numeric("interactive"),
            "cumulative_layout_shift": get_numeric("cumulative-layout-shift"),
            "dom_nodes": get_numeric("dom-size"),
            "total_byte_weight_kb": None,
            "mainthread_work_ms": get_numeric("mainthread-work-breakdown"),
            "bootup_time_ms": get_numeric("bootup-time"),
        }

        # total-byte-weight (bytes → KB)
        total_byte_weight_audit = audits.get("total-byte-weight")
        if isinstance(total_byte_weight_audit, dict):
            val = total_byte_weight_audit.get("numericValue")
            if isinstance(val, (int, float)):
                lab["total_byte_weight_kb"] = round(val / 1024.0, 1)

        # network-requests → nº de peticiones
        requests_audit = audits.get("network-requests")
        if isinstance(requests_audit, dict):
            details = requests_audit.get("details") or {}
            items = details.get("items") or []
            lab["requests_count"] = len(items)

        metrics["lab_metrics"] = lab

        # ---- Core Web Vitals de campo (CrUX) ----
        loading = data.get("loadingExperience", {}).get("metrics", {}) or {}

        def get_percentile(metric_name: str) -> Optional[float]:
            m = loading.get(metric_name)
            if not isinstance(m, dict):
                return None
            val = m.get("percentile")
            return float(val) if isinstance(val, (int, float)) else None

        cwv: Dict[str, Optional[float]] = {
            "FCP_ms": get_percentile("FIRST_CONTENTFUL_PAINT_MS"),
            "LCP_ms": get_percentile("LARGEST_CONTENTFUL_PAINT_MS"),
            "CLS": get_percentile("CUMULATIVE_LAYOUT_SHIFT_SCORE"),
            "INP_ms": get_percentile("INTERACTION_TO_NEXT_PAINT_MS"),
            "FID_ms": get_percentile("FIRST_INPUT_DELAY_MS"),
        }
        metrics["core_web_vitals"] = cwv

        # ---- Scores & CWV → Issues ----
        self._evaluate_category_scores(scores, issues)
        if not any(v is not None for v in cwv.values()):
            self._add_issue(
                issues,
                code="FIELD_CORE_WEB_VITALS_MISSING",
                severity="warning",
                category="core_web_vitals",
                solution=(
                    "No hay suficientes datos de campo (CrUX) para esta URL. "
                    "Aumenta el tráfico real para que Google pueda calcular Core Web Vitals de usuario."
                ),
            )
        else:
            self._evaluate_cwv(cwv, issues)

        # ---- Clasificar audits (failed/passed/...) ----
        self._classify_audits(lighthouse, audits, audits_result)

        # ---- Opportunities & Diagnostics → Issues + resúmenes ----
        self._evaluate_audits_opportunities(audits, issues, audits_result)
        self._evaluate_audits_diagnostics(audits, issues, audits_result)

        return PageResult(
            url=url,
            strategy=strategy,
            status_code=status_code,
            metrics=metrics,
            issues=issues,
            audits=audits_result,
        )

    # ---------------------------
    # Manejo de errores API
    # ---------------------------
    def _handle_api_error(self, data: Dict[str, Any], status_code: int, issues: List[Issue]) -> None:
        api_error = data.get("error", {})
        base_solution = (
            "Comprueba que la API key es correcta, que la PageSpeed Insights API está habilitada en "
            "Google Cloud Console y que no has superado la cuota. Revisa también las restricciones "
            "de la clave (IP, HTTP referrers) y vuelve a ejecutar el análisis."
        )

        self._add_issue(
            issues,
            code="PAGESPEED_API_ERROR",
            severity="error",
            category="api",
            value={"status_code": status_code, "api_error": api_error},
            solution=base_solution,
        )

        errors_list = api_error.get("errors", [])
        if isinstance(errors_list, list):
            for e in errors_list:
                reason = e.get("reason")
                message = e.get("message")
                suggested = base_solution

                if reason == "keyInvalid":
                    suggested = (
                        "La API key es inválida. Entra en Google Cloud Console, crea una nueva clave para "
                        "PageSpeed Insights y configúrala en el script."
                    )
                elif reason in ("accessNotConfigured", "ipRefererBlocked"):
                    suggested = (
                        "La API no está habilitada o la clave está restringida. "
                        "Activa la PageSpeed Insights API y revisa que las restricciones de la clave "
                        "permiten este tipo de llamadas."
                    )
                elif reason in ("dailyLimitExceeded", "rateLimitExceeded", "userRateLimitExceeded"):
                    suggested = (
                        "Has superado la cuota de PageSpeed Insights. Reduce la frecuencia de peticiones, "
                        "limita el número de URLs o aumenta la cuota en Google Cloud Console."
                    )

                self._add_issue(
                    issues,
                    code="PAGESPEED_API_ERROR_DETAIL",
                    severity="error",
                    category="api",
                    value={"reason": reason, "message": message},
                    solution=suggested,
                )

    # ---------------------------
    # Reglas de score
    # ---------------------------
    def _evaluate_category_scores(self, scores: Dict[str, Optional[float]], issues: List[Issue]) -> None:
        # Umbrales típicos: <50 rojo, 50–89 ámbar, 90–100 verde
        for cat, score in scores.items():
            if score is None:
                self._add_issue(
                    issues,
                    code=f"{cat.upper()}_SCORE_MISSING",
                    severity="warning",
                    category="lighthouse",
                    solution=(
                        "Lighthouse no ha devuelto score para esta categoría. Abre el informe completo "
                        "en la interfaz de PageSpeed Insights para revisar qué ha ocurrido."
                    ),
                )
                continue

            if score < 50:
                self._add_issue(
                    issues,
                    code=f"{cat.upper()}_SCORE_VERY_LOW",
                    severity="error",
                    category="performance" if cat == "performance" else "lighthouse",
                    value=score,
                    limit=50,
                    solution=self._score_solution(cat, "very_low"),
                )
            elif score < 90:
                self._add_issue(
                    issues,
                    code=f"{cat.upper()}_SCORE_LOW",
                    severity="warning",
                    category="performance" if cat == "performance" else "lighthouse",
                    value=score,
                    limit=90,
                    solution=self._score_solution(cat, "low"),
                )

    @staticmethod
    def _score_solution(category: str, level: str) -> str:
        cat_label = category.replace("_", " ").title()
        if category == "performance":
            if level == "very_low":
                return (
                    f"El score de {cat_label} es muy bajo. Optimiza imágenes, activa compresión (gzip/brotli), "
                    "usa caché, minimiza CSS/JS y reduce JavaScript bloqueante. Revisa las 'Oportunidades' del informe."
                )
            else:
                return (
                    f"El score de {cat_label} es mejorable. Apunta a 90+ reduciendo peso de recursos, "
                    "mejorando el TTFB y eliminando scripts innecesarios."
                )
        if category == "accessibility":
            return (
                "Mejora la accesibilidad: textos alternativos, roles ARIA correctos, contraste suficiente "
                "y formularios con etiquetas claras."
            )
        if category == "best_practices":
            return (
                "Revisa las 'Best Practices': librerías seguras, HTTPS en todos los recursos, "
                "evitar APIs obsoletas y corregir avisos de seguridad."
            )
        if category == "seo":
            return (
                "Mejora el SEO técnico según Lighthouse: estructura correcta, contenido indexable "
                "y etiquetas meta coherentes."
            )
        if category == "pwa":
            return (
                "Para cumplir criterios PWA, revisa manifest.json, service worker, "
                "funcionamiento offline y criterios de instalabilidad."
            )
        return "Revisa las recomendaciones detalladas de Lighthouse para esta categoría."

    # ---------------------------
    # Reglas Core Web Vitals
    # ---------------------------
    def _evaluate_cwv(self, cwv: Dict[str, Optional[float]], issues: List[Issue]) -> None:
        # LCP: <=2500 good, 2500–4000 NI, >4000 poor
        lcp = cwv.get("LCP_ms")
        if lcp is not None:
            if lcp > 4000:
                self._add_issue(
                    issues,
                    code="LCP_POOR",
                    severity="error",
                    category="core_web_vitals",
                    value=lcp,
                    limit=2500,
                    solution=(
                        "LCP es pobre (>4000 ms). Optimiza el elemento principal above-the-fold (imagen o bloque), "
                        "aplaza recursos no críticos, reduce CSS/JS bloqueante y mejora el tiempo de respuesta del servidor."
                    ),
                )
            elif lcp > 2500:
                self._add_issue(
                    issues,
                    code="LCP_NEEDS_IMPROVEMENT",
                    severity="warning",
                    category="core_web_vitals",
                    value=lcp,
                    limit=2500,
                    solution=(
                        "LCP necesita mejorar (2500–4000 ms). Recorta el peso de recursos críticos, "
                        "usa preloading para fuentes/estilos clave y optimiza imágenes above-the-fold."
                    ),
                )

        # CLS: <=0.1 good, 0.1–0.25 NI, >0.25 poor
        cls = cwv.get("CLS")
        if cls is not None:
            if cls > 0.25:
                self._add_issue(
                    issues,
                    code="CLS_POOR",
                    severity="error",
                    category="core_web_vitals",
                    value=cls,
                    limit=0.1,
                    solution=(
                        "CLS es pobre (>0.25). Fija width/height de imágenes e iframes, "
                        "reserva espacio para banners y evita insertar contenido por encima del contenido ya renderizado."
                    ),
                )
            elif cls > 0.1:
                self._add_issue(
                    issues,
                    code="CLS_NEEDS_IMPROVEMENT",
                    severity="warning",
                    category="core_web_vitals",
                    value=cls,
                    limit=0.1,
                    solution=(
                        "CLS necesita mejorar (0.1–0.25). Revisa cambios de layout provocados por anuncios, "
                        "elementos cargados tarde y fuentes sin espacio reservado."
                    ),
                )

        # INP: <=200 good, 200–500 NI, >500 poor
        inp = cwv.get("INP_ms")
        if inp is not None:
            if inp > 500:
                self._add_issue(
                    issues,
                    code="INP_POOR",
                    severity="error",
                    category="core_web_vitals",
                    value=inp,
                    limit=200,
                    solution=(
                        "INP es pobre (>500 ms). Reduce el trabajo JavaScript en handlers de eventos, "
                        "divide tareas largas, usa web workers donde tenga sentido y elimina scripts innecesarios."
                    ),
                )
            elif inp > 200:
                self._add_issue(
                    issues,
                    code="INP_NEEDS_IMPROVEMENT",
                    severity="warning",
                    category="core_web_vitals",
                    value=inp,
                    limit=200,
                    solution=(
                        "INP necesita mejorar (200–500 ms). Optimiza la lógica asociada a las interacciones del usuario "
                        "y evita bloqueos en el hilo principal durante clics y cambios de campo."
                    ),
                )

        # FID: <=100 good, 100–300 NI, >300 poor
        fid = cwv.get("FID_ms")
        if fid is not None:
            if fid > 300:
                self._add_issue(
                    issues,
                    code="FID_POOR",
                    severity="error",
                    category="core_web_vitals",
                    value=fid,
                    limit=100,
                    solution=(
                        "FID es pobre (>300 ms). Minimiza JS cargado en el inicio, usa 'defer'/'async', "
                        "haz code-splitting y limita tareas largas que bloqueen la interacción inicial."
                    ),
                )
            elif fid > 100:
                self._add_issue(
                    issues,
                    code="FID_NEEDS_IMPROVEMENT",
                    severity="warning",
                    category="core_web_vitals",
                    value=fid,
                    limit=100,
                    solution=(
                        "FID necesita mejorar (100–300 ms). Reduce scripts críticos, "
                        "limita el trabajo inicial del hilo principal y evita plugins pesados."
                    ),
                )

        # FCP: <=2000 good, 2000–4000 NI, >4000 poor
        fcp = cwv.get("FCP_ms")
        if fcp is not None:
            if fcp > 4000:
                self._add_issue(
                    issues,
                    code="FCP_POOR",
                    severity="error",
                    category="core_web_vitals",
                    value=fcp,
                    limit=2000,
                    solution=(
                        "FCP es muy alto (>4000 ms). Mejora el TTFB, reduce redirecciones, minimiza CSS/JS "
                        "y optimiza recursos críticos para que la primera pintura ocurra antes."
                    ),
                )
            elif fcp > 2000:
                self._add_issue(
                    issues,
                    code="FCP_NEEDS_IMPROVEMENT",
                    severity="warning",
                    category="core_web_vitals",
                    value=fcp,
                    limit=2000,
                    solution=(
                        "FCP podría mejorar (2000–4000 ms). Acelera el backend, añade caché, "
                        "y evita cargar recursos innecesarios antes del contenido visible."
                    ),
                )

    # ---------------------------
    # Clasificación de audits
    # ---------------------------
    def _summarize_audit(self, audit_id: str, audit: Dict[str, Any]) -> AuditSummary:
        details = audit.get("details") or {}
        return AuditSummary(
            id=audit_id,
            title=audit.get("title"),
            score=audit.get("score"),
            score_display_mode=audit.get("scoreDisplayMode"),
            numeric_value=audit.get("numericValue"),
            numeric_unit=audit.get("numericUnit"),
            display_value=audit.get("displayValue"),
            description=audit.get("description"),
            warnings=audit.get("warnings"),
            details_type=details.get("type"),
            group=audit.get("group"),
        )

    def _classify_audits(
        self,
        lighthouse: Dict[str, Any],
        audits: Dict[str, Any],
        audits_result: Dict[str, List[AuditSummary]],
    ) -> None:
        for audit_id, audit in audits.items():
            if not isinstance(audit, dict):
                continue
            summary = self._summarize_audit(audit_id, audit)
            sdm = audit.get("scoreDisplayMode")
            score = audit.get("score")

            if sdm == "notApplicable":
                audits_result["not_applicable"].append(summary)
            elif sdm in ("manual", "manual-base"):
                audits_result["manual"].append(summary)
            elif sdm in ("informative", "numeric"):
                # Métricas informativas / numéricas
                audits_result["informative"].append(summary)
            else:
                # binario pass/fail
                if isinstance(score, (int, float)) and score < 1.0:
                    audits_result["failed"].append(summary)
                else:
                    audits_result["passed"].append(summary)

    # ---------------------------
    # Opportunities & diagnostics
    # ---------------------------
    def _audit_hint(self, audit_id: str) -> Tuple[str, str]:
        """
        Devuelve (category, base_solution) para un audit de Lighthouse.
        category: performance | ux | lighthouse.
        """
        mapping: Dict[str, Tuple[str, str]] = {
            "render-blocking-resources": (
                "performance",
                "Elimina o aplaza CSS/JS que bloquea el render para que el contenido above-the-fold aparezca antes.",
            ),
            "unused-css-rules": (
                "performance",
                "Elimina CSS no utilizado o divide las hojas de estilo para reducir peso y mejorar la carga.",
            ),
            "unused-javascript": (
                "performance",
                "Elimina JavaScript no utilizado, aplica code-splitting y carga diferida para reducir el trabajo en el hilo principal.",
            ),
            "server-response-time": (
                "performance",
                "Reduce el tiempo de respuesta del servidor optimizando consultas, caché y configuración del hosting.",
            ),
            "uses-text-compression": (
                "performance",
                "Activa compresión (gzip o brotli) en el servidor para CSS, JS y HTML.",
            ),
            "uses-optimized-images": (
                "performance",
                "Optimiza y comprime imágenes, usa tamaños adecuados y formatos modernos para reducir peso.",
            ),
            "uses-responsive-images": (
                "performance",
                "Define 'srcset' y tamaños responsive para las imágenes, evitando servir archivos enormes en móviles.",
            ),
            "offscreen-images": (
                "performance",
                "Aplica lazy loading a imágenes fuera de pantalla para que no bloqueen la carga inicial.",
            ),
            "efficient-animated-content": (
                "performance",
                "Evita GIFs pesados; usa vídeo o animaciones más eficientes para reducir el impacto en la carga.",
            ),
            "uses-rel-preload": (
                "performance",
                "Usa 'rel=preload' para recursos críticos (fuentes, CSS) y mejora su carga anticipada.",
            ),
            "font-display": (
                "ux",
                "Configura 'font-display: swap' o similar para evitar flashes de texto invisible (FOIT).",
            ),
            "total-byte-weight": (
                "performance",
                "Reduce el peso total de la página optimizando imágenes, CSS, JS y fuentes.",
            ),
            "dom-size": (
                "performance",
                "Simplifica el DOM eliminando nodos innecesarios y componentes redundantes para mejorar rendimiento.",
            ),
            "modern-image-formats": (
                "performance",
                "Usa formatos de imagen modernos (WebP/AVIF) para reducir el peso de los recursos gráficos.",
            ),
            "mainthread-work-breakdown": (
                "performance",
                "Reduce el trabajo del hilo principal dividiendo tareas largas y eliminando JS innecesario.",
            ),
            "bootup-time": (
                "performance",
                "Reduce el tiempo de arranque optimizando la cantidad y tamaño de scripts cargados.",
            ),
        }
        return mapping.get(
            audit_id,
            (
                "lighthouse",
                "Revisa las recomendaciones específicas de este audit en el informe de Lighthouse y aplica las optimizaciones sugeridas.",
            ),
        )

    def _evaluate_audits_opportunities(
        self,
        audits: Dict[str, Any],
        issues: List[Issue],
        audits_result: Dict[str, List[AuditSummary]],
    ) -> None:
        for audit_id, audit in audits.items():
            if not isinstance(audit, dict):
                continue
            details = audit.get("details") or {}
            if details.get("type") != "opportunity":
                continue

            summary = self._summarize_audit(audit_id, audit)
            audits_result["opportunities"].append(summary)

            title = audit.get("title")
            score = audit.get("score")
            overall_savings_ms = details.get("overallSavingsMs")
            overall_savings_bytes = details.get("overallSavingsBytes")

            severity = "warning"
            if isinstance(overall_savings_ms, (int, float)):
                if overall_savings_ms >= 2000:
                    severity = "error"
                elif overall_savings_ms < 500:
                    severity = "warning"

            category, base_solution = self._audit_hint(audit_id)
            code = f"OPPORTUNITY_{audit_id.upper().replace('-', '_')}"

            extra = {
                "title": title,
                "overall_savings_ms": overall_savings_ms,
                "overall_savings_bytes": overall_savings_bytes,
                "score": score,
            }

            solution = base_solution
            if isinstance(overall_savings_ms, (int, float)):
                solution += f" Lighthouse estima un ahorro potencial de ~{int(overall_savings_ms)} ms si aplicas esta mejora."

            self._add_issue(
                issues,
                code=code,
                severity=severity,
                category=category,
                value=score,
                limit=None,
                solution=solution,
                extra=extra,
            )

    def _evaluate_audits_diagnostics(
        self,
        audits: Dict[str, Any],
        issues: List[Issue],
        audits_result: Dict[str, List[AuditSummary]],
    ) -> None:
        important_diagnostics = [
            "total-byte-weight",
            "dom-size",
            "mainthread-work-breakdown",
            "bootup-time",
        ]

        for audit_id in important_diagnostics:
            audit = audits.get(audit_id)
            if not isinstance(audit, dict):
                continue
            summary = self._summarize_audit(audit_id, audit)
            audits_result["diagnostics"].append(summary)

            score = audit.get("score")
            details = audit.get("details") or {}
            numeric_value = audit.get("numericValue")
            title = audit.get("title")

            category, base_solution = self._audit_hint(audit_id)
            if score is None and numeric_value is None:
                continue

            severity: Optional[str] = None
            # Basado en score
            if isinstance(score, (int, float)):
                if score < 0.5:
                    severity = "error"
                elif score < 0.9:
                    severity = "warning"

            # Fallback: umbrales numéricos
            if severity is None and isinstance(numeric_value, (int, float)):
                if audit_id == "total-byte-weight":
                    if numeric_value > 2_500_000:
                        severity = "error"
                    elif numeric_value > 1_500_000:
                        severity = "warning"
                elif audit_id == "dom-size":
                    if numeric_value > 3000:
                        severity = "error"
                    elif numeric_value > 1500:
                        severity = "warning"
                elif audit_id in ("mainthread-work-breakdown", "bootup-time"):
                    if numeric_value > 4000:
                        severity = "error"
                    elif numeric_value > 2000:
                        severity = "warning"

            if severity is None:
                continue

            code = f"DIAGNOSTIC_{audit_id.upper().replace('-', '_')}"
            extra = {
                "title": title,
                "numeric_value": numeric_value,
                "details_type": details.get("type"),
                "score": score,
            }
            solution = base_solution

            self._add_issue(
                issues,
                code=code,
                severity=severity,
                category=category,
                value=numeric_value,
                limit=None,
                solution=solution,
                extra=extra,
            )

    # ---------------------------
    # Run
    # ---------------------------
    def run(self) -> None:
        urls = self.get_sitemap_urls()
        tasks = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            for u in urls:
                for strategy in ("mobile", "desktop"):
                    tasks.append(executor.submit(self.call_pagespeed, u, strategy))

            for fut in as_completed(tasks):
                result = fut.result()
                self.results.append(result)

    def to_json(self) -> Dict[str, Any]:
        total_errors = 0
        total_warnings = 0

        score_aggr: Dict[str, Dict[str, Any]] = {}
        cwv_aggr: Dict[str, Dict[str, Any]] = {}
        audit_aggr: Dict[str, Dict[str, Any]] = {}

        for r in self.results:
            # Contar issues
            for i in r.issues:
                if i.severity == "error":
                    total_errors += 1
                elif i.severity == "warning":
                    total_warnings += 1

            # Agregar scores
            scores = r.metrics.get("scores") or {}
            for cat, val in scores.items():
                if val is None:
                    continue
                ag = score_aggr.setdefault(cat, {"sum": 0.0, "count": 0, "min": None, "max": None})
                ag["sum"] += float(val)
                ag["count"] += 1
                ag["min"] = val if ag["min"] is None else min(ag["min"], val)
                ag["max"] = val if ag["max"] is None else max(ag["max"], val)

            # Agregar CWV
            cwv = r.metrics.get("core_web_vitals") or {}
            for name, val in cwv.items():
                if val is None:
                    continue
                ag = cwv_aggr.setdefault(name, {"sum": 0.0, "count": 0, "min": None, "max": None})
                ag["sum"] += float(val)
                ag["count"] += 1
                ag["min"] = val if ag["min"] is None else min(ag["min"], val)
                ag["max"] = val if ag["max"] is None else max(ag["max"], val)

            # Agregar audits: peores scores / valor numérico máximo por audit id
            for list_name, audit_list in r.audits.items():
                for a in audit_list:
                    ag = audit_aggr.setdefault(
                        a.id,
                        {
                            "id": a.id,
                            "title": a.title,
                            "count": 0,
                            "min_score": None,
                            "max_score": None,
                            "max_numeric_value": None,
                        },
                    )
                    ag["count"] += 1
                    if a.score is not None:
                        ag["min_score"] = (
                            a.score if ag["min_score"] is None else min(ag["min_score"], a.score)
                        )
                        ag["max_score"] = (
                            a.score if ag["max_score"] is None else max(ag["max_score"], a.score)
                        )
                    if a.numeric_value is not None:
                        ag["max_numeric_value"] = (
                            a.numeric_value
                            if ag["max_numeric_value"] is None
                            else max(ag["max_numeric_value"], a.numeric_value)
                        )

        global_scores: Dict[str, Dict[str, Optional[float]]] = {}
        for cat, ag in score_aggr.items():
            if ag["count"] == 0:
                continue
            global_scores[cat] = {
                "avg": round(ag["sum"] / ag["count"], 1),
                "min": ag["min"],
                "max": ag["max"],
            }

        global_cwv: Dict[str, Dict[str, Optional[float]]] = {}
        for name, ag in cwv_aggr.items():
            if ag["count"] == 0:
                continue
            global_cwv[name] = {
                "avg": round(ag["sum"] / ag["count"], 1),
                "min": ag["min"],
                "max": ag["max"],
            }

        global_audits = list(audit_aggr.values())

        return {
            "base_url": self.base_url,
            "total_results": len(self.results),
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "global_issues": [asdict(i) for i in self.global_issues],
            "global_metrics": {
                "scores": global_scores,
                "core_web_vitals": global_cwv,
            },
            "global_audits": global_audits,
            "pages": [r.to_dict() for r in self.results],
        }


# ---------------------------
# CLI
# ---------------------------
def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Auditor maximizado PageSpeed Insights (mobile+desktop) solo con datos de Lighthouse."
    )
    parser.add_argument("url", help="URL base (ej. https://pablocirre.es)")
    parser.add_argument(
        "--sitemap",
        help="URL de sitemap explícito; si no se indica, intenta /sitemap.xml, /sitemap_index.xml, etc.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Máximo de páginas del sitemap a analizar (por defecto todas).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Timeout HTTP en segundos (por defecto 60).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Número máximo de peticiones concurrentes (ojo con la cuota de la API).",
    )
    parser.add_argument(
        "--api-key",
        help="PageSpeed Insights API key. Si se omite, usa la variable de entorno PAGESPEED_API_KEY.",
    )
    parser.add_argument(
        "--include-raw",
        action="store_true",
        help="Incluir el bloque raw con lighthouseResult completo y loadingExperience (puede ser muy pesado).",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv)

    api_key = args.api_key or os.environ.get("PAGESPEED_API_KEY") or PageSpeedAuditor.load_local_key() or ""
    if not api_key:
        payload = {
            "base_url": args.url,
            "total_results": 0,
            "total_errors": 1,
            "total_warnings": 0,
            "global_issues": [
                asdict(
                    Issue(
                        code="MISSING_API_KEY",
                        severity="error",
                        category="api",
                        value=None,
                        limit=None,
                        extra={
                            "solution": (
                                "No se ha proporcionado API key. Pasa la clave con --api-key "
                                "o define la variable de entorno PAGESPEED_API_KEY "
                                "con una clave válida de PageSpeed Insights."
                            )
                        },
                    )
                )
            ],
            "global_metrics": {
                "scores": {},
                "core_web_vitals": {},
            },
            "global_audits": [],
            "pages": [],
        }
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    auditor = PageSpeedAuditor(
        base_url=args.url,
        api_key=api_key,
        sitemap_url=args.sitemap,
        max_pages=args.max_pages,
        timeout=args.timeout,
        workers=args.workers,
        include_raw=args.include_raw,
    )
    auditor.run()
    report = auditor.to_json()

    # Save to Reports directory
    # .../Tools/PageSpeed/PageSpeed.py -> .../Tools/PageSpeed -> .../Tools -> .../Root
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    reports_dir = os.path.join(root_dir, "Reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"pagespeed_report_{timestamp}.json"
    filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"Report saved to: {filepath}")


if __name__ == "__main__":
    main(sys.argv[1:])
