"""Base classes and contracts for VAPT external adapters."""

import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.vapt.models import VAPTFinding, VAPTSeverity, VAPTScanType


SEVERITY_MAP = {
    "critical": VAPTSeverity.CRITICAL,
    "high": VAPTSeverity.HIGH,
    "medium": VAPTSeverity.MEDIUM,
    "moderate": VAPTSeverity.MEDIUM,
    "low": VAPTSeverity.LOW,
    "info": VAPTSeverity.INFO,
    "informational": VAPTSeverity.INFO,
    "note": VAPTSeverity.INFO,
    "unknown": VAPTSeverity.INFO,
}


def to_severity(value: Any, default: VAPTSeverity = VAPTSeverity.INFO) -> VAPTSeverity:
    """Map arbitrary severity strings from external tools to VAPTSeverity."""
    if value is None:
        return default
    if isinstance(value, VAPTSeverity):
        return value
    return SEVERITY_MAP.get(str(value).strip().lower(), default)


@dataclass
class AdapterStatus:
    """Health/availability status of an adapter."""

    id: str
    name: str
    enabled: bool
    configured: bool
    available: bool
    description: str = ""
    error: Optional[str] = None
    version: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "configured": self.configured,
            "available": self.available,
            "error": self.error,
            "version": self.version,
        }


@dataclass
class AdapterScanResult:
    """Result of an adapter-run scan phase."""

    adapter_id: str
    findings: List[VAPTFinding] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    duration: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "findings": len(self.findings),
            "errors": self.errors,
            "duration": round(self.duration, 1),
            "raw": self.raw,
        }


class VAPTAdapter(ABC):
    """Contract implemented by every external VAPT integration.

    Lifecycle during a scan:
      1. ``configured()`` - env config present?
      2. ``enabled()``   - env flag allows execution?
      3. ``health()``    - can we actually reach/execute it?
      4. ``run_scan()``  - execute against target, return canonical findings.
    """

    id: str = "base"
    name: str = "Base Adapter"
    description: str = ""

    # ------------------------------------------------------------------ config

    def _env(self, key: str, default: str = "") -> str:
        return os.environ.get(key, default).strip()

    def _env_flag(self, key: str, default: bool = True) -> bool:
        raw = os.environ.get(key, "true" if default else "false").strip().lower()
        return raw in ("1", "true", "yes", "on")

    @abstractmethod
    def configured(self) -> bool:
        """True when the environment contains everything needed to attempt a run."""

    def enabled(self) -> bool:
        """True when the adapter should participate in scans."""
        return self.configured()

    def allow_for(self, scan_type: VAPTScanType, target_info: Dict[str, Any]) -> bool:
        """Adapters are skipped for targets they cannot meaningfully test."""
        return True

    # ------------------------------------------------------------------ health

    @abstractmethod
    async def health(self) -> AdapterStatus:
        """Return current availability status (should not raise)."""

    # ------------------------------------------------------------------ run

    @abstractmethod
    async def run_scan(
        self,
        target: str,
        scan_id: str,
        scan_type: VAPTScanType,
        target_info: Dict[str, Any],
    ) -> AdapterScanResult:
        """Execute the adapter against ``target``.

        Must never raise - errors are captured in ``AdapterScanResult.errors``
        so a failing external platform never aborts the whole scan.
        """

    # ------------------------------------------------------------- helpers

    def _new_finding(
        self,
        title: str,
        description: str,
        target: str,
        severity: Any,
        *,
        tool_name: Optional[str] = None,
        vulnerability_type: Optional[str] = None,
        remediation: Optional[str] = None,
        reference: Optional[str] = None,
        cve: Optional[str] = None,
        cwe: Optional[str] = None,
        payload: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        path: Optional[str] = None,
        protocol: Optional[str] = None,
        service: Optional[str] = None,
        cvss_score: Optional[float] = None,
        confidence: str = "confirmed",
        details: Optional[Dict[str, Any]] = None,
    ) -> VAPTFinding:
        details = details or {}
        details.setdefault("source_platform", self.id)
        return VAPTFinding(
            title=str(title)[:200],
            description=str(description)[:500] if description else "",
            severity=to_severity(severity),
            cvss_score=cvss_score,
            tool_name=tool_name or self.id,
            target=target,
            host=host,
            port=port,
            protocol=protocol,
            service=service,
            path=path,
            vulnerability_type=vulnerability_type,
            remediation=remediation,
            reference=reference,
            cve=cve,
            cwe=cwe,
            payload=payload,
            confidence=confidence,
            details=details,
        )

    @staticmethod
    def _run_duration(started: float) -> float:
        return round(time.time() - started, 1)
