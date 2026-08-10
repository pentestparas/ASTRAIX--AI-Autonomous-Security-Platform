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
    "masscan": VAPTTool(
        id="masscan",
        name="Masscan",
        command="masscan",
        description="High-speed asynchronous port scanner",
        category=VAPTScanType.NETWORK,
        args=["-oX", "-", "--rate", "1000"],
        timeout=600,
        requires_ip=True,
        output_format="xml",
    ),
    "dnsrecon": VAPTTool(
        id="dnsrecon",
        name="DNSRecon",
        command="dnsrecon",
        description="DNS enumeration - records, zone transfer, brute force",
        category=VAPTScanType.NETWORK,
        args=["-j", "-", "-t", "std"],
        timeout=600,
        requires_hostname=True,
        output_format="json",
    ),
    "subfinder": VAPTTool(
        id="subfinder",
        name="Subfinder",
        command="subfinder",
        description="Passive subdomain discovery",
        category=VAPTScanType.NETWORK,
        args=["-jsonl", "-", "-silent"],
        timeout=600,
        requires_hostname=True,
        output_format="json",
    ),
    "httpx": VAPTTool(
        id="httpx",
        name="HTTPx",
        command="httpx",
        description="HTTP probing - status, title, tech fingerprint",
        category=VAPTScanType.WEB,
        args=["-json", "-silent"],
        timeout=600,
        requires_hostname=True,
        output_format="json",
    ),
    "whatweb": VAPTTool(
        id="whatweb",
        name="WhatWeb",
        command="whatweb",
        description="Web technology fingerprinting",
        category=VAPTScanType.WEB,
        args=["--log-json=-"],
        timeout=300,
        requires_url=True,
        output_format="json",
    ),
    "wafw00f": VAPTTool(
        id="wafw00f",
        name="WAFW00F",
        command="wafw00f",
        description="WAF detection and fingerprinting",
        category=VAPTScanType.WEB,
        args=["-o", "-", "-f", "json"],
        timeout=300,
        requires_url=True,
        output_format="json",
    ),
    "arjun": VAPTTool(
        id="arjun",
        name="Arjun",
        command="arjun",
        description="HTTP parameter discovery",
        category=VAPTScanType.WEB,
        args=["-oJ", "-", "-q"],
        timeout=600,
        requires_url=True,
        output_format="json",
    ),
    "wfuzz": VAPTTool(
        id="wfuzz",
        name="WFuzz",
        command="wfuzz",
        description="Web fuzzer for content and parameter fuzzing",
        category=VAPTScanType.WEB,
        args=["--oF", "-", "--json"],
        timeout=600,
        requires_url=True,
        output_format="json",
    ),
    "commix": VAPTTool(
        id="commix",
        name="Commix",
        command="commix",
        description="OS command injection detector and exploiter",
        category=VAPTScanType.WEB,
        args=["--batch", "--output-dir=/tmp"],
        timeout=900,
        requires_url=True,
        output_format="text",
    ),
    "hydra": VAPTTool(
        id="hydra",
        name="Hydra",
        command="hydra",
        description="Network login brute-forcer (ssh, http, rdp, ftp)",
        category=VAPTScanType.NETWORK,
        args=["-L", "-P", "-t", "4", "-w", "10"],
        timeout=1200,
        requires_hostname=True,
        output_format="text",
    ),
    "testssl": VAPTTool(
        id="testssl",
        name="TestSSL",
        command="testssl",
        description="Deep TLS/SSL configuration audit",
        category=VAPTScanType.SSL,
        args=["--jsonfile", "-"],
        timeout=600,
        requires_hostname=True,
        output_format="json",
    ),
}

TOOLS_BY_CATEGORY: Dict[VAPTScanType, List[str]] = {
    VAPTScanType.NETWORK: ["nmap", "masscan", "dnsrecon", "subfinder"],
    VAPTScanType.WEB: ["nikto", "nuclei", "gobuster", "ffuf", "whatweb", "httpx"],
    VAPTScanType.API: ["nuclei", "ffuf", "arjun"],
    VAPTScanType.SSL: ["sslscan", "testssl"],
    VAPTScanType.CONTAINER: ["trivy"],
    VAPTScanType.FULL: ["nmap", "nikto", "nuclei", "gobuster", "sslscan", "masscan", "ffuf", "hydra"],
}

DEFAULT_TOOLS: Dict[VAPTScanType, List[str]] = {
    VAPTScanType.NETWORK: ["nmap", "dnsrecon"],
    VAPTScanType.WEB: ["nikto", "nuclei", "gobuster"],
    VAPTScanType.API: ["nuclei", "ffuf"],
    VAPTScanType.SSL: ["sslscan"],
    VAPTScanType.CONTAINER: ["trivy"],
    VAPTScanType.FULL: ["nmap", "nikto", "nuclei", "gobuster"],
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
    """Tools run inside the astraix-kali container, not the backend process.

    Probes the actual binaries in the image with a single container run;
    falls back to host `which` checks only when the image is missing.
    """
    from app.vapt.executor import VAPTExecutor

    try:
        result = subprocess.run(
            ["docker", "image", "inspect", VAPTExecutor.KALI_IMAGE],
            capture_output=True,
            timeout=10,
        )
        if result.returncode == 0:
            script = "; ".join(
                f"command -v {tool.command} >/dev/null 2>&1 && echo 'OK {tool_id}' || echo 'MISS {tool_id}'"
                for tool_id, tool in TOOLS_REGISTRY.items()
            )
            probe = subprocess.run(
                [
                    "docker", "run", "--rm", VAPTExecutor.KALI_IMAGE,
                    "bash", "-c", script,
                ],
                capture_output=True,
                timeout=120,
            )
            availability: Dict[str, bool] = {tid: False for tid in TOOLS_REGISTRY}
            for line in (probe.stdout or b"").decode("utf-8", errors="ignore").splitlines():
                parts = line.split()
                if len(parts) == 2 and parts[0] in ("OK", "MISS"):
                    availability[parts[1]] = parts[0] == "OK"
            return availability
    except Exception:
        pass

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