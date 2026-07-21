"""Nuclei Plugin — normalizer.

Converts raw `nuclei` output into canonical `SecurityFinding` instances.

Plugin shape (nuclei JSON output):
  {
    "target": "https://example.com",
    "findings": [
      {
        "type": "http",
        "template": "cves/2021/CVE-2021-44228.yaml",
        "template-id": "CVE-2021-44228",
        "info": {
          "name": "Log4j Remote Code Execution",
          "severity": "critical",
          "classification": {"cve-id": ["CVE-2021-44228"]},
          "tags": ["cve","rce","log4j"]
        },
        "matched-at": "https://example.com:8443/",
        "extracted-results": ["log4j.rce.detected"]
      }
    ]
  }
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Iterator, Mapping
import uuid as _uuid

from ai_secos_core.finding_engine.normalizer import FindingNormalizer
from ai_secos_core.shared.value_objects import (
    FindingEvidence,
    FindingFingerprint,
    SecurityFinding,
    Severity,
)

SEVERITY_MAP = {
    "info": Severity.INFO,
    "low": Severity.LOW,
    "medium": Severity.MEDIUM,
    "high": Severity.HIGH,
    "critical": Severity.CRITICAL,
}


class NucleiNormalizer(FindingNormalizer):
    """Normalizer for the nuclei plugin."""

    plugin_id = "scanner/nuclei"

    def normalize(
        self,
        raw_output: Mapping[str, Any],
        *,
        assessment_id,
        capability_id: str,
        asset_id: str,
    ) -> Iterator[SecurityFinding]:
        findings = raw_output.get("findings", [])
        for finding in findings:
            yield _normalize_one(finding, assessment_id, capability_id, asset_id)


def _normalize_one(
    finding: Mapping[str, Any],
    assessment_id: str,
    capability_id: str,
    asset_id: str,
) -> SecurityFinding:
    """Normalize a single nuclei finding."""
    info = finding.get("info", {})
    template_id = finding.get("template-id", "")
    template = finding.get("template", "")
    matched_at = finding.get("matched-at", "")
    extracted = finding.get("extracted-results", [])

    name = info.get("name", "Unknown Finding")
    raw_severity = info.get("severity", "info").lower()
    severity = SEVERITY_MAP.get(raw_severity, Severity.INFO)
    cve_ids = info.get("classification", {}).get("cve-id", [])
    tags = info.get("tags", [])
    description = info.get("description", "")

    matched_url = matched_at.split(":")[0] if matched_at else asset_id

    fingerprint_str = f"nuclei:{template_id}:{matched_at}:{asset_id}"
    fingerprint = FindingFingerprint(
        hashlib.sha256(fingerprint_str.encode("utf-8")).hexdigest()[:32]
    )

    title = name
    if template_id:
        title = f"[{template_id}] {name}"

    finding_desc = description or f"Nuclei template {template} detected at {matched_at}"
    if extracted:
        finding_desc += f"\nEvidence: {'; '.join(extracted[:5])}"

    references = info.get("reference", [])
    if isinstance(references, str):
        references = [references]

    return SecurityFinding(
        id=_uuid.uuid4(),
        assessment_id=assessment_id,
        asset=asset_id,
        capability=capability_id,
        plugin="scanner/nuclei",
        category=_categorize(tags),
        title=title[:512],
        description=finding_desc[:600],
        severity=severity,
        confidence=0.95,
        risk_score=None,
        cvss=info.get("cvss-score"),
        cwe=[f"CWE-{c}" for c in info.get("classification", {}).get("cwe-id", [])],
        cve=[cve.upper() for cve in cve_ids],
        owasp=[],
        references=references[:10],
        evidence=FindingEvidence(
            schema_name="nuclei",
            raw={
                "template": template,
                "template_id": template_id,
                "matched_at": matched_at,
                "extracted_results": extracted,
                "type": finding.get("type", "http"),
            },
        ),
        tags=["nuclei"] + [t for t in tags if t],
        metadata={
            "template": template,
            "template_id": template_id,
            "matched_at": matched_at,
            "type": finding.get("type", "http"),
            "extracted_results": extracted,
        },
        fingerprint=fingerprint,
    )


def _categorize(tags: list[str]) -> str:
    """Map nuclei tags to finding category."""
    tag_str = " ".join(tags).lower()

    if "sqli" in tag_str or "sql" in tag_str:
        return "sql-injection"
    if "xss" in tag_str or "cross-site" in tag_str:
        return "xss"
    if "rce" in tag_str or "remote-code" in tag_str:
        return "rce"
    if "lfi" in tag_str or "local-file" in tag_str:
        return "lfi"
    if "ssrf" in tag_str:
        return "ssrf"
    if "csrf" in tag_str:
        return "csrf"
    if "xxe" in tag_str:
        return "xxe"
    if "ssti" in tag_str or "template-injection" in tag_str:
        return "ssti"
    if "idor" in tag_str:
        return "idor"
    if "auth" in tag_str or "bypass" in tag_str:
        return "auth-bypass"
    if "exposure" in tag_str or "misconfig" in tag_str:
        return "misconfiguration"
    if "cve" in tag_str:
        return "vulnerability"
    if "fingerprint" in tag_str or "detection" in tag_str:
        return "information-disclosure"

    return "vulnerability"