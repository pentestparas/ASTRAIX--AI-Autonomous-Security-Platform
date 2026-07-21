"""HTTP Probe (httpx) Plugin — normalizer.

Converts raw `httpx` output into canonical `SecurityFinding` instances.

Plugin shape (httpx JSON, see ProjectDiscovery/httpx):
  {
    "host": "example.com",
    "port": 443,
    "scheme": "https",
    "url": "https://example.com:443",
    "title": "Example Domain",
    "status_code": 200,
    "content_type": "text/html",
    "tech": [{"name": "Nginx", "version": "1.21"}, ...],
    "response_time_ms": 142,
    "tls": {"version": "TLSv1.3", "cipher": "TLS_AES_128_GCM_SHA256"},
    "favicon_hash": "-1159395058",
    "cdn_name": "Cloudflare",
    "asn": {"asn": "AS13335", "name": "CLOUDFLARE"},
    "extract_date": "2026-05-15T10:42:00Z",
    "webserver": "nginx/1.21",
    "extract_title": "Example",
    "input": "example.com"
  }

The normalizer maps URL + status_code → a `base` finding.
Each "tech" entry becomes a separate finding (stack detection asset).
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterator, Mapping, Optional
import uuid as _uuid

from ai_secos_core.finding_engine.normalizer import FindingNormalizer
from ai_secos_core.shared.value_objects import (
    FindingEvidence,
    FindingFingerprint,
    SecurityFinding,
    Severity,
)


@dataclass(frozen=True)
class HttpxPluginId:
    """Bundle the httpx plugin id constant."""

    value: str = "scanner/httpx"


class HttpxNormalizer(FindingNormalizer):
    """Normalizer for the httpx plugin."""

    plugin_id = "scanner/httpx"

    def normalize(
        self,
        raw_output: Mapping[str, Any],
        *,
        assessment_id,
        capability_id: str,
        asset_id: str,
    ) -> Iterator[SecurityFinding]:
        items = _extract_items(raw_output)
        for item in items:
            base = _normalize_one(item, assessment_id, capability_id, asset_id)
            yield base
            # Each detected technology produces one additional finding.
            for tech_finding in _normalize_tech(item, base):
                yield tech_finding


def _extract_items(raw_output: Mapping[str, Any]) -> list[dict[str, Any]]:
    if isinstance(raw_output.get("items"), list):
        return raw_output["items"]
    if isinstance(raw_output.get("results"), list):
        return raw_output["results"]
    # Single-item case.
    if "url" in raw_output:
        return [dict(raw_output)]
    return []


def _normalize_one(
    item: Mapping[str, Any],
    assessment_id: str,
    capability_id: str,
    asset_id: str,
) -> SecurityFinding:
    url = item.get("url") or f"{item.get('scheme', 'https')}://{item.get('host', '')}"
    host = item.get("host") or ""
    status_code = item.get("status_code") or 0
    title = item.get("title") or item.get("extract_title") or ""
    severity = _severity_from_status(status_code)
    confidence = _confidence(item)
    tech = ",".join([t.get("name", "") for t in item.get("tech", []) if t.get("name")]).strip(",")

    reference = item.get("cdn_name") or item.get("webserver") or ""
    import urllib.parse
    _ref_is_url = reference and urllib.parse.urlparse(reference).scheme in ("http", "https", "ftp")
    description = (
        f"Service reachable at {url} (status {status_code}). "
        f"Tech: {tech or 'undetected'}."[:600]
    ).strip()

    finding_id = _uuid.uuid4()
    fingerprint = FindingFingerprint(
        hashlib.sha256(
            f"httpx-probe:{host}:{url}:{asset_id}".encode("utf-8")
        ).hexdigest()[:32]
    )

    return SecurityFinding(
        id=finding_id,
        assessment_id=assessment_id or "",
        asset=asset_id,
        capability=capability_id,
        plugin="scanner/httpx",
        category="web-probe",
        title=_title(url, status_code),
        description=description,
        severity=Severity(severity),
        confidence=confidence,
        risk_score=None,
        cvss=None,
        cwe=[],
        cve=[],
        owasp=[],
        references=[reference] if _ref_is_url else [],
        evidence=FindingEvidence(schema_name="httpx", raw=dict(item)),
        tags=["httpx", "liveness"],
        metadata={
            "host": host,
            "url": url,
            "status_code": status_code,
            "title": title,
            "tech": tech,
            "tls": item.get("tls", {}),
        },
        fingerprint=fingerprint,
    )


def _normalize_tech(
    item: Mapping[str, Any],
    base: SecurityFinding,
) -> Iterator[SecurityFinding]:
    """Stack detection → asset_inventory findings."""
    techs = item.get("tech", []) or []
    for entry in techs:
        name = entry.get("name") if isinstance(entry, dict) else None
        if not name:
            continue
        version = entry.get("version") if isinstance(entry, dict) else None
        host = item.get("host", "")
        tech_str = f"{name}/{version}" if version else name
        fingerprint = FindingFingerprint(
            hashlib.sha256(
                f"httpx-tech:{host}:{name}:{version}".encode("utf-8")
            ).hexdigest()[:32]
        )
        yield SecurityFinding(
            id=_uuid.uuid4(),
            assessment_id=base.assessment_id,
            asset=base.asset,
            capability=base.capability,
            plugin="scanner/httpx",
            category="technology-detected",
            title=f"Detected technology: {tech_str}",
            description=f"httpx fingerprinting detected {tech_str} on {host or base.asset}.",
            severity=Severity.INFO,
            confidence=1.0,
            risk_score=None,
            cvss=None,
            cwe=[],
            cve=[],
            owasp=[],
            evidence=FindingEvidence(
                schema_name="httpx-tech",
                raw={"tech": entry, "url": item.get("url"), "host": host},
            ),
            tags=["httpx", "tech", name.lower()],
            metadata={"tech_name": name, "tech_version": version},
            fingerprint=fingerprint,
        )


def _title(url: str, status: int) -> str:
    if status == 0:
        return f"HTTP probe: unreachable {url}"
    if status >= 500:
        return f"HTTP {status} on {url}"
    if status >= 400:
        return f"HTTP {status} on {url}"
    return f"HTTP {status} on {url}"


def _severity_from_status(status: int) -> str:
    if status == 0:
        return "low"
    if status >= 500:
        return "medium"
    if status >= 400:
        return "low"
    return "info"


def _confidence(item: Mapping[str, Any]) -> float:
    score = 0.5
    if item.get("status_code"):
        score += 0.3
    if item.get("title"):
        score += 0.1
    if item.get("tech"):
        score += 0.05
    return min(score, 1.0)


def make_httpx_input(target: str, ports: Optional[list[str]] = None) -> dict[str, Any]:
    """Convenience: build the stdin payload for the httpx executable."""
    return {
        "input": target,
        "ports": ports or ["80", "443"],
        "no_color": True,
        "follow_redirects": True,
    }