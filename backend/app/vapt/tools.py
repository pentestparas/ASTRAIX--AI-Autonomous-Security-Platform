"""
VAPT Tools Registry

Direct integration with host-installed security tools.
Fast execution without container overhead.
"""

import subprocess
from typing import Dict, List, Optional
from app.vapt.models import VAPTTool, VAPTScanType

TOOLS_REGISTRY: Dict[str, VAPTTool] = {
    "nmap": VAPTTool(
        id="nmap",
        name="Nmap",
        command="nmap",
        description="Network scanner - discovers hosts, ports, services",
        category=VAPTScanType.NETWORK,
        args=["-sV", "-Pn", "-oX", "-"],
        timeout=600,
        requires_ip=True,
        output_format="xml",
    ),
    "nikto": VAPTTool(
        id="nikto",
        name="Nikto",
        command="nikto",
        description="Web server scanner - finds vulnerabilities, misconfigs",
        category=VAPTScanType.WEB,
        args=["-Format", "xml", "-output", "-"],
        timeout=900,
        requires_url=True,
        output_format="xml",
    ),
    "sqlmap": VAPTTool(
        id="sqlmap",
        name="SQLMap",
        command="sqlmap",
        description="SQL injection detector and exploiter",
        category=VAPTScanType.WEB,
        args=["--batch", "--random-agent", "--output-dir=/tmp"],
        timeout=1800,
        requires_url=True,
        output_format="json",
    ),
    "nuclei": VAPTTool(
        id="nuclei",
        name="Nuclei",
        command="nuclei",
        description="Template-based vulnerability scanner",
        category=VAPTScanType.WEB,
        args=["-json-export", "-", "-silent", "-rate-limit", "150"],
        timeout=1800,
        requires_url=True,
        output_format="json",
    ),
    "gobuster": VAPTTool(
        id="gobuster",
        name="Gobuster",
        command="gobuster",
        description="Directory/file DNS and web brute-forcer",
        category=VAPTScanType.WEB,
        args=["dir", "-o", "-", "-f", "-j", "-q", "-t", "10"],
        timeout=600,
        requires_url=True,
        output_format="text",
    ),
    "ffuf": VAPTTool(
        id="ffuf",
        name="Ffuf",
        command="ffuf",
        description="Fast web fuzzer for discovery",
        category=VAPTScanType.WEB,
        args=["-json", "-u"],
        timeout=600,
        requires_url=True,
        output_format="json",
    ),
    "trivy": VAPTTool(
        id="trivy",
        name="Trivy",
        command="trivy",
        description="Container and VM vulnerability scanner",
        category=VAPTScanType.CONTAINER,
        args=["--quiet", "--format", "json", "--output", "-"],
        timeout=600,
        output_format="json",
    ),
    "sslscan": VAPTTool(
        id="sslscan",
        name="SSLscan",
        command="sslscan",
        description="SSL/TLS vulnerability scanner",
        category=VAPTScanType.SSL,
        args=["--xml=-", "--no-failed"],
        timeout=300,
        requires_hostname=True,
        output_format="xml",
    ),
}

TOOLS_BY_CATEGORY: Dict[VAPTScanType, List[str]] = {
    VAPTScanType.NETWORK: ["nmap"],
    VAPTScanType.WEB: ["nikto", "nuclei", "gobuster"],
    VAPTScanType.API: ["nuclei", "ffuf"],
    VAPTScanType.SSL: ["sslscan"],
    VAPTScanType.CONTAINER: ["trivy"],
    VAPTScanType.FULL: ["nmap", "nikto", "nuclei", "gobuster", "sslscan"],
}

DEFAULT_TOOLS: Dict[VAPTScanType, List[str]] = {
    VAPTScanType.NETWORK: ["nmap"],
    VAPTScanType.WEB: ["nikto", "nuclei", "gobuster"],
    VAPTScanType.API: ["nuclei", "ffuf"],
    VAPTScanType.SSL: ["sslscan"],
    VAPTScanType.CONTAINER: ["trivy"],
    VAPTScanType.FULL: ["nmap", "nikto", "nuclei", "gobuster"],
}


def get_tool(tool_id: str) -> Optional[VAPTTool]:
    return TOOLS_REGISTRY.get(tool_id)


def get_tools_for_scan_type(scan_type: VAPTScanType) -> List[VAPTTool]:
    tool_ids = DEFAULT_TOOLS.get(scan_type, ["nmap"])
    return [TOOLS_REGISTRY[tid] for tid in tool_ids if tid in TOOLS_REGISTRY]


def check_tool_availability() -> Dict[str, bool]:
    available = {}
    for tool_id, tool in TOOLS_REGISTRY.items():
        try:
            result = subprocess.run(
                ["which", tool.command],
                capture_output=True,
                timeout=5,
            )
            available[tool_id] = result.returncode == 0
        except Exception:
            available[tool_id] = False
    return available


def get_available_tools() -> List[str]:
    avail = check_tool_availability()
    return [tid for tid, is_avail in avail.items() if is_avail]