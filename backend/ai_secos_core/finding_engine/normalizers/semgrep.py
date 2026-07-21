"""Semgrep Plugin — normalizer.

Converts raw `semgrep` output into canonical `SecurityFinding` instances.

Plugin shape (semgrep JSON output):
  {
    "results": [
      {
        "check_id": "python.lang.security.audit.insecure-hash.insecure-hash-sha1",
        "path": "src/utils.py",
        "start": {"line": 42, "col": 0},
        "end": {"line": 42, "col": 50},
        "extra": {
          "severity": "WARNING",
          "message": "Detected use of insecure hash function sha1",
          "metadata": {
            "cwe": "CWE-328",
            "owasp": "A3:2017-Sensitive Data Exposure"
          }
        }
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
    "ERROR": Severity.HIGH,
    "WARNING": Severity.MEDIUM,
    "INFO": Severity.INFO,
}


class SemgrepNormalizer(FindingNormalizer):
    """Normalizer for the semgrep plugin."""

    plugin_id = "scanner/semgrep"

    def normalize(
        self,
        raw_output: Mapping[str, Any],
        *,
        assessment_id,
        capability_id: str,
        asset_id: str,
    ) -> Iterator[SecurityFinding]:
        results = raw_output.get("results", []) or []
        for result in results:
            yield _normalize_one(result, assessment_id, capability_id, asset_id)


def _normalize_one(
    result: Mapping[str, Any],
    assessment_id: str,
    capability_id: str,
    asset_id: str,
) -> SecurityFinding:
    """Normalize a single semgrep finding."""
    check_id = result.get("check_id", "unknown")
    path = result.get("path", "unknown")
    start_line = result.get("start", {}).get("line", 0)
    end_line = result.get("end", {}).get("line", 0)

    extra = result.get("extra", {})
    severity_raw = extra.get("severity", "WARNING").upper()
    severity = SEVERITY_MAP.get(severity_raw, Severity.MEDIUM)
    message = extra.get("message", "")
    metadata = extra.get("metadata", {})

    cwe_ids = metadata.get("cwe", [])
    if isinstance(cwe_ids, str):
        cwe_ids = [cwe_ids]

    owasp = metadata.get("owasp", [])

    fingerprint_str = f"semgrep:{check_id}:{path}:{start_line}:{asset_id}"
    fingerprint = FindingFingerprint(
        hashlib.sha256(fingerprint_str.encode("utf-8")).hexdigest()[:32]
    )

    title = f"[{check_id}] {message.split('.')[0]}" if message else f"Code Issue: {check_id}"

    lines = extra.get("lines", "")
    code_context = f"**File:** {path}:{start_line}\n```\n{lines}\n```" if lines else f"**File:** {path}:{start_line}"

    return SecurityFinding(
        id=_uuid.uuid4(),
        assessment_id=assessment_id,
        asset=asset_id,
        capability=capability_id,
        plugin="scanner/semgrep",
        category=_categorize_semgrep(check_id, metadata),
        title=title[:512],
        description=f"{message}\n\n{code_context}"[:600],
        severity=severity,
        confidence=0.85,
        risk_score=None,
        cvss=metadata.get("cvss-score"),
        cwe=[f"CWE-{c}" for c in cwe_ids] if cwe_ids else [],
        cve=[],
        owasp=[o for o in owasp] if owasp else [],
        references=metadata.get("references", [])[:5],
        evidence=FindingEvidence(
            schema_name="semgrep",
            raw={
                "check_id": check_id,
                "path": path,
                "start": result.get("start"),
                "end": result.get("end"),
                "extra": extra,
            },
        ),
        tags=["semgrep", "sast", "code"] + _extract_tags(metadata),
        metadata={
            "check_id": check_id,
            "path": path,
            "start_line": start_line,
            "end_line": end_line,
            "metadata": metadata,
        },
        fingerprint=fingerprint,
        remediation=metadata.get("fix", f"Review and fix the code issue at {path}:{start_line}"),
    )


def _categorize_semgrep(check_id: str, metadata: dict) -> str:
    """Categorize semgrep finding based on check_id and metadata."""
    check_lower = check_id.lower()

    if ".injection" in check_lower or "sql" in check_lower:
        return "injection"
    if "xss" in check_lower or "html" in check_lower:
        return "xss"
    if "rce" in check_lower or "exec" in check_lower:
        return "rce"
    if "path" in check_lower and ("traversal" in check_lower or "injection" in check_lower):
        return "path-traversal"
    if "crypto" in check_lower or "hash" in check_lower:
        return "cryptographic-weakness"
    if "auth" in check_lower or "credential" in check_lower:
        return "auth-issue"
    if "sql" in check_lower:
        return "sql-injection"
    if "secret" in check_lower or "api" in check_lower:
        return "secret-exposure"

    category = metadata.get("category", "")
    if category:
        return category.lower().replace(" ", "-")

    return "code-issue"


def _extract_tags(metadata: dict) -> list[str]:
    """Extract tags from semgrep metadata."""
    tags = []

    if "technology" in metadata:
        tech = metadata["technology"]
        if isinstance(tech, list):
            tags.extend([t.lower() for t in tech])
        elif isinstance(tech, str):
            tags.append(tech.lower())

    if "confidence" in metadata:
        tags.append(f"confidence-{metadata['confidence'].lower()}")

    return tags