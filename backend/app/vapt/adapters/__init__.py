"""
VAPT External Adapter Framework

Pluggable adapters that let the platform execute security testing through
external AI-powered VAPT tools/platforms in addition to the built-in Kali
toolchain:

  - raccoon   (evyatarmeged/Raccoon)      - recon/info-gathering CLI (Kali image)
  - lyrie     (OTT-Cybersecurity-LLC/lyrie-ai) - autonomous pentest CLI (Kali image)
  - xalgorix  (xalgord/xalgorix)          - autonomous pentest engine (Docker sidecar + REST API)
  - darkmoon  (ASCIT31/Dark-Moon)         - autonomous pentest platform (external CLI/stack)
  - pentagi   (vxcontrol/pentagi)         - autonomous pentest AGI (external stack + API)
  - redamon   (samugit83/redamon)         - agentic red-team framework (external stack + API)
  - zenai     (zen-ai-pentest Action)     - GitHub Actions pentest (CI/CD)

Each adapter implements :class:`VAPTAdapter` and is registered in
:mod:`app.vapt.adapters.registry`. Adapters are enabled via environment
variables; only enabled+configured adapters run during scans and report
health through `GET /api/v1/vapt/adapters`.
"""

from app.vapt.adapters.base import AdapterScanResult, AdapterStatus, VAPTAdapter
from app.vapt.adapters.registry import (
    get_adapter,
    get_all_adapters,
    get_enabled_adapters,
    adapter_health,
)

__all__ = [
    "AdapterScanResult",
    "AdapterStatus",
    "VAPTAdapter",
    "get_adapter",
    "get_all_adapters",
    "get_enabled_adapters",
    "adapter_health",
]
