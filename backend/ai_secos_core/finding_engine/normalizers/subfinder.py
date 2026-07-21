"""Subfinder Plugin — normalizer.

Converts raw `subfinder` output into canonical `SecurityFinding` instances.

Plugin shape (subfinder JSON output):
  {
    "target": "example.com",
    "subdomains": [
      {"host": "api.example.com", "source": "dnsdumpster"},
      {"host": "www.example.com", "source": "crtsh"}
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


class SubfinderNormalizer(FindingNormalizer):
    """Normalizer for the subfinder plugin."""

    plugin_id = "scanner/subfinder"

    def normalize(
        self,
        raw_output: Mapping[str, Any],
        *,
        assessment_id,
        capability_id: str,
        asset_id: str,
    ) -> Iterator[SecurityFinding]:
        subdomains = raw_output.get("subdomains", [])
        for subdomain in subdomains:
            yield _normalize_one(subdomain, assessment_id, capability_id, asset_id, raw_output.get("target", ""))


def _normalize_one(
    subdomain: Mapping[str, Any],
    assessment_id: str,
    capability_id: str,
    asset_id: str,
    base_domain: str,
) -> SecurityFinding:
    """Normalize a single subdomain."""
    host = subdomain.get("host", "")
    source = subdomain.get("source", "unknown")

    if not host:
        raise ValueError("Subfinder result missing 'host' field")

    fingerprint = FindingFingerprint(
        hashlib.sha256(f"subfinder:{host}:{asset_id}".encode("utf-8")).hexdigest()[:32]
    )

    return SecurityFinding(
        id=_uuid.uuid4(),
        assessment_id=assessment_id,
        asset=asset_id,
        capability=capability_id,
        plugin="scanner/subfinder",
        category="subdomain",
        title=f"Discovered Subdomain: {host}",
        description=f"Subdomain {host} discovered via {source} during reconnaissance of {base_domain}.",
        severity=Severity.INFO,
        confidence=0.8,
        risk_score=None,
        cvss=None,
        cwe=[],
        cve=[],
        owasp=[],
        references=[],
        evidence=FindingEvidence(
            schema_name="subfinder",
            raw={"host": host, "source": source},
        ),
        tags=["subfinder", "recon", "subdomain", source],
        metadata={
            "host": host,
            "source": source,
            "base_domain": base_domain,
        },
        fingerprint=fingerprint,
    )