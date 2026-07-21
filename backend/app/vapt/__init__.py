"""
ASTRAIX VAPT Module

AI-Orchestrated Vulnerability Assessment & Penetration Testing.

Architecture:
    NeuralSec AI → VAPT Orchestrator → Tool Executor → Security Controls → Tools → Findings

Tools integrated directly (host-installed):
- nmap, nikto, sqlmap, nuclei, gobuster, ffuf, trivy, sslscan

Security controls:
- Input sanitization
- Rate limiting
- Target validation
- Container isolation (optional)
"""

from app.vapt.executor import VAPTExecutor, get_vapt_executor
from app.vapt.models import (
    VAPTTarget,
    VAPTScanType,
    VAPTTool,
    VAPTFinding,
    VAPTScanRequest,
    VAPTScanResult,
)

__all__ = [
    "VAPTExecutor",
    "get_vapt_executor",
    "VAPTTarget",
    "VAPTScanType",
    "VAPTTool",
    "VAPTFinding",
    "VAPTScanRequest",
    "VAPTScanResult",
]