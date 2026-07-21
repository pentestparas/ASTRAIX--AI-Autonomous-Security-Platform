"""Trivy Plugin — normalizer.

Converts raw `trivy` output into canonical `SecurityFinding` instances.

Plugin shape (trivy JSON output):
  {
    "target": "myimage:tag",
    "results": {
      "Results": [
        {
          "Target": "Python==3.11.0",
          "Vulnerabilities": [
            {
              "VulnerabilityID": "CVE-2023-44487",
              "PkgName": "http2",
              "InstalledVersion": "1.0.0",
              "FixedVersion": "1.0.1",
              "Severity": "HIGH",
              "Title": "HTTP/2 Rapid Reset Attack",
              "Description": "...",
              "References": [...]
            }
          ]
        }
      ]
    }
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
    "UNKNOWN": Severity.INFO,
    "LOW": Severity.LOW,
    "MEDIUM": Severity.MEDIUM,
    "HIGH": Severity.HIGH,
    "CRITICAL": Severity.CRITICAL,
}


class TrivyNormalizer(FindingNormalizer):
    """Normalizer for the trivy plugin."""

    plugin_id = "scanner/trivy"

    def normalize(
        self,
        raw_output: Mapping[str, Any],
        *,
        assessment_id,
        capability_id: str,
        asset_id: str,
    ) -> Iterator[SecurityFinding]:
        results = raw_output.get("results", {})
        trivy_results = results.get("Results", []) if isinstance(results, dict) else results

        for result in trivy_results:
            target = result.get("Target", "unknown")

            # Handle vulnerabilities
            vulns = result.get("Vulnerabilities", []) or []
            for vuln in vulns:
                yield _normalize_vulnerability(vuln, target, assessment_id, capability_id, asset_id, raw_output)

            # Handle misconfigurations
            misconfigs = result.get("Misconfigurations", []) or []
            for misconfig in misconfigs:
                yield _normalize_misconfiguration(misconfig, target, assessment_id, capability_id, asset_id, raw_output)


def _normalize_vulnerability(
    vuln: Mapping[str, Any],
    target: str,
    assessment_id: str,
    capability_id: str,
    asset_id: str,
    raw_output: Mapping[str, Any],
) -> SecurityFinding:
    """Normalize a single vulnerability finding."""
    vuln_id = vuln.get("VulnerabilityID", "UNKNOWN")
    pkg_name = vuln.get("PkgName", "unknown")
    installed = vuln.get("InstalledVersion", "")
    fixed = vuln.get("FixedVersion", "")
    severity_raw = vuln.get("Severity", "UNKNOWN").upper()
    severity = SEVERITY_MAP.get(severity_raw, Severity.INFO)
    title = vuln.get("Title", f"{vuln_id} in {pkg_name}")
    description = vuln.get("Description", "")
    cve_refs = [vuln_id] if vuln_id.startswith("CVE-") else []

    fingerprint = FindingFingerprint(
        hashlib.sha256(f"trivy:{vuln_id}:{pkg_name}:{asset_id}".encode("utf-8")).hexdigest()[:32]
    )

    remediation = f"Update {pkg_name} to version {fixed}" if fixed else f"Patch or remediate {pkg_name}"
    if not fixed:
        remediation += f"\nNo fixed version available. Consider replacing {pkg_name} with a secure alternative."

    return SecurityFinding(
        id=_uuid.uuid4(),
        assessment_id=assessment_id,
        asset=asset_id,
        capability=capability_id,
        plugin="scanner/trivy",
        category="vulnerability",
        title=f"[{vuln_id}] {title}"[:512],
        description=f"**Package:** {pkg_name} ({installed})\n**Fixed:** {fixed or 'N/A'}\n\n{description}"[:600],
        severity=severity,
        confidence=0.95,
        risk_score=None,
        cvss=_extract_cvss(vuln),
        cwe=[],
        cve=cve_refs,
        owasp=[],
        references=vuln.get("References", [])[:10],
        evidence=FindingEvidence(
            schema_name="trivy-vuln",
            raw={
                "target": target,
                "vulnerability": vuln,
            },
        ),
        tags=["trivy", "vulnerability", pkg_name.lower().replace(".", "-")],
        metadata={
            "vuln_id": vuln_id,
            "package": pkg_name,
            "installed_version": installed,
            "fixed_version": fixed,
            "target": target,
            "raw_severity": severity_raw,
        },
        fingerprint=fingerprint,
        remediation=remediation,
    )


def _normalize_misconfiguration(
    misconfig: Mapping[str, Any],
    target: str,
    assessment_id: str,
    capability_id: str,
    asset_id: str,
    raw_output: Mapping[str, Any],
) -> SecurityFinding:
    """Normalize a single misconfiguration finding."""
    misconfig_id = misconfig.get("ID", "UNKNOWN")
    title = misconfig.get("Title", f"Misconfiguration: {misconfig_id}")
    severity_raw = misconfig.get("Severity", "UNKNOWN").upper()
    severity = SEVERITY_MAP.get(severity_raw, Severity.INFO)
    description = misconfig.get("Message", "")
    status = misconfig.get("Status", "")

    is_compliant = status.upper() == "PASS"

    if is_compliant:
        return

    fingerprint = FindingFingerprint(
        hashlib.sha256(f"trivy-misconfig:{misconfig_id}:{target}:{asset_id}".encode("utf-8")).hexdigest()[:32]
    )

    return SecurityFinding(
        id=_uuid.uuid4(),
        assessment_id=assessment_id,
        asset=asset_id,
        capability=capability_id,
        plugin="scanner/trivy",
        category="misconfiguration",
        title=f"[{misconfig_id}] {title}"[:512],
        description=f"**Target:** {target}\n**Status:** {status}\n\n{description}"[:600],
        severity=severity,
        confidence=0.9,
        risk_score=None,
        cvss=None,
        cwe=[],
        cve=[],
        owasp=[],
        references=misconfig.get("References", [])[:10],
        evidence=FindingEvidence(
            schema_name="trivy-misconfig",
            raw={
                "target": target,
                "misconfiguration": misconfig,
            },
        ),
        tags=["trivy", "misconfiguration", misconfig_id.lower().replace(".", "-")],
        metadata={
            "misconfig_id": misconfig_id,
            "target": target,
            "status": status,
            "type": misconfig.get("Type", "IaC"),
        },
        fingerprint=fingerprint,
        remediation=misconfig.get("Resolution", "Fix the misconfiguration per the security best practices"),
    )


def _extract_cvss(vuln: Mapping[str, Any]) -> float | None:
    """Extract CVSS score from trivy vulnerability data."""
    cvss = vuln.get("CVSS")
    if cvss:
        if isinstance(cvss, dict):
            for vendor, score_data in cvss.items():
                if isinstance(score_data, dict) and "V3Score" in score_data:
                    return float(score_data["V3Score"])
        elif isinstance(cvss, (int, float)):
            return float(cvss)
    return None