"""
VAPT Tools Registry

Direct integration with host-installed security tools.
Fast execution without container overhead.
"""

import subprocess
import time
from typing import Any, Dict, List, Optional
from app.vapt.models import VAPTTool, VAPTScanType

AVAILABILITY_TTL = 300

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
    "dalfox": VAPTTool(
        id="dalfox",
        name="Dalfox",
        command="dalfox",
        description="XSS vulnerability scanner (reflected/DOM/blind)",
        category=VAPTScanType.WEB,
        args=["--format", "json", "--silence"],
        timeout=900,
        requires_url=True,
        output_format="json",
    ),
    "katana": VAPTTool(
        id="katana",
        name="Katana",
        command="katana",
        description="Crawler - discovers endpoints, forms, API routes",
        category=VAPTScanType.WEB,
        args=["-json", "-silent"],
        timeout=600,
        requires_url=True,
        output_format="json",
    ),
    "feroxbuster": VAPTTool(
        id="feroxbuster",
        name="Feroxbuster",
        command="feroxbuster",
        description="Content discovery fuzzer",
        category=VAPTScanType.WEB,
        args=["-q", "-t", "10", "--json"],
        timeout=900,
        requires_url=True,
        output_format="json",
    ),
    "dirsearch": VAPTTool(
        id="dirsearch",
        name="Dirsearch",
        command="dirsearch",
        description="Web path scanner",
        category=VAPTScanType.WEB,
        args=["--format=json", "-o", "/tmp/ds.json"],
        timeout=900,
        requires_url=True,
        output_format="json",
    ),
    "xsstrike": VAPTTool(
        id="xsstrike",
        name="XSStrike",
        command="xsstrike",
        description="Advanced XSS detection (payload + fuzzing engine)",
        category=VAPTScanType.WEB,
        args=["--skip-ba", "--skip-dom"],
        timeout=900,
        requires_url=True,
        output_format="text",
    ),
    "graphqlmap": VAPTTool(
        id="graphqlmap",
        name="GraphQLMap",
        command="graphqlmap",
        description="GraphQL endpoint scanner - introspection, injection",
        category=VAPTScanType.API,
        args=["-v", "1"],
        timeout=900,
        requires_url=True,
        output_format="text",
    ),
    "forms": VAPTTool(
        id="forms",
        name="Web Form & API Scanner",
        command="forms",
        description=(
            "Form, API and AI chatbot scanner - probes REST/API endpoints, "
            "tests query params for SQLi, JSON bodies for NoSQLi, form fields "
            "for reflected XSS, and chatbot inputs for prompt/SQL injection"
        ),
        category=VAPTScanType.WEB,
        args=[],
        timeout=900,
        requires_url=True,
        output_format="jsonl",
    ),
    "smuggler": VAPTTool(
        id="smuggler",
        name="Smuggler",
        command="smuggler",
        description="HTTP request smuggling detector (H2C, CL.TE, TE.CL)",
        category=VAPTScanType.WEB,
        args=[],
        timeout=600,
        requires_url=True,
        output_format="text",
    ),
    "kiterunner": VAPTTool(
        id="kiterunner",
        name="Kiterunner",
        command="kr",
        description="API/route content discovery using compiled route lists",
        category=VAPTScanType.API,
        args=["--json"],
        timeout=900,
        requires_url=True,
        output_format="json",
    ),
    "gitleaks": VAPTTool(
        id="gitleaks",
        name="Gitleaks",
        command="gitleaks",
        description="Secret detection in source code (git repo URL as target)",
        category=VAPTScanType.API,
        args=["--report-format", "json", "--redact"],
        timeout=900,
        output_format="json",
    ),
    "trufflehog": VAPTTool(
        id="trufflehog",
        name="TruffleHog",
        command="trufflehog",
        description="Credential/secret scanning in git repos and filesystems",
        category=VAPTScanType.API,
        args=["--json", "--no-update"],
        timeout=900,
        output_format="json",
    ),
    "semgrep": VAPTTool(
        id="semgrep",
        name="Semgrep",
        command="semgrep",
        description="Static analysis - OWASP Top 10 rule pack on source (git repo URL as target)",
        category=VAPTScanType.API,
        args=["--config=auto", "--json"],
        timeout=900,
        output_format="json",
    ),
    "metasploit": VAPTTool(
        id="metasploit",
        name="Metasploit",
        command="msfconsole",
        description="Auxiliary scanner battery: HTTP version/options/TRACE/PUT, robots.txt, directory listing, TLS/SSL",
        category=VAPTScanType.WEB,
        args=[],
        timeout=1200,
        requires_url=True,
        output_format="text",
    ),
    "searchsploit": VAPTTool(
        id="searchsploit",
        name="SearchSploit",
        command="searchsploit",
        description="Exploit-DB lookup for known exploits of discovered software",
        category=VAPTScanType.WEB,
        args=["--json"],
        timeout=300,
        output_format="json",
    ),
    "bandit": VAPTTool(
        id="bandit",
        name="Bandit",
        command="bandit",
        description="Python SAST - security issues in python source (git repo URL as target)",
        category=VAPTScanType.API,
        args=["-r", "-f", "json"],
        timeout=600,
        output_format="json",
    ),
    "zap": VAPTTool(
        id="zap",
        name="OWASP ZAP",
        command="zap",
        description="Headless active scanner - spider + full active scan via REST API (Burp-style)",
        category=VAPTScanType.WEB,
        args=[],
        timeout=1500,
        requires_url=True,
        output_format="json",
    ),
    "garak": VAPTTool(
        id="garak",
        name="Garak",
        command="garak",
        description=(
            "AI/LLM security scanner - OWASP LLM Top 10 probes: prompt injection, "
            "jailbreaks (dan/encoding), data leak replay, misdirection"
        ),
        category=VAPTScanType.LLM,
        args=[],
        timeout=1500,
        requires_url=True,
        output_format="jsonl",
    ),
    "api-surface": VAPTTool(
        id="api-surface",
        name="API Surface Discovery",
        command="api_surface_scanner",
        description=(
            "Endpoint surface discovery - probes REST API routes and hidden "
            "paths (generic + OWASP Juice Shop route map) and reports every "
            "reachable endpoint, flagging sensitive ones"
        ),
        category=VAPTScanType.API,
        args=[],
        timeout=600,
        requires_url=True,
        output_format="jsonl",
    ),
    "code-review": VAPTTool(
        id="code-review",
        name="Secure Code Review",
        command="code_review_scanner",
        description=(
            "Static source review - fingerprints the app, clones its public "
            "repository, runs semgrep/CodeQL/bandit/gitleaks/trivy on the code "
            "to find code-review level vulnerabilities (SQLi sinks, JWT alg "
            "confusion, hardcoded secrets, dependency CVEs, unsafe middleware)"
        ),
        category=VAPTScanType.API,
        args=[],
        timeout=900,
        requires_url=True,
        output_format="jsonl",
    ),
    "flows": VAPTTool(
        id="flows",
        name="API Flow Security",
        command="flows_engine",
        description=(
            "Business-logic API flows - registers/logs in, then probes for "
            "broken object-level authorization (BOLA), broken function-level "
            "authorization, JWT alg:none forgery, login SQL injection and "
            "price tampering via multi-step flows"
        ),
        category=VAPTScanType.API,
        args=[],
        timeout=600,
        requires_url=True,
        output_format="jsonl",
    ),
    "dom-xss": VAPTTool(
        id="dom-xss",
        name="DOM XSS Probe",
        command="dom_xss_scanner",
        description=(
            "Client-side security - headless Chromium renders pages with XSS "
            "payloads in query/hash/params and checks the DOM for execution, "
            "plus static analysis of client JS bundles for dangerous sinks "
            "fed by location.hash/search"
        ),
        category=VAPTScanType.WEB,
        args=[],
        timeout=600,
        requires_url=True,
        output_format="jsonl",
    ),
}

TOOLS_BY_CATEGORY: Dict[VAPTScanType, List[str]] = {
    VAPTScanType.NETWORK: ["nmap", "masscan", "dnsrecon", "subfinder"],
    VAPTScanType.WEB: ["nikto", "nuclei", "gobuster", "ffuf", "whatweb", "httpx", "api-surface"],
    VAPTScanType.API: ["nuclei", "ffuf", "arjun", "api-surface"],
    VAPTScanType.SSL: ["sslscan", "testssl"],
    VAPTScanType.CONTAINER: ["trivy"],
    VAPTScanType.LLM: ["garak"],
    VAPTScanType.CODE_REVIEW: ["code-review", "gitleaks", "trufflehog", "semgrep", "bandit"],
    # FULL = every agent-visible tool (all scan types: network, web, API,
    # SSL/TLS, container, AI/LLM security).
    VAPTScanType.FULL: sorted(
        tid for tid, tool in TOOLS_REGISTRY.items() if tool.agent_visible
    ),
}

DEFAULT_TOOLS: Dict[VAPTScanType, List[str]] = {
    VAPTScanType.NETWORK: ["nmap", "dnsrecon"],
    VAPTScanType.WEB: ["nikto", "nuclei", "gobuster"],
    VAPTScanType.API: ["nuclei", "ffuf"],
    VAPTScanType.SSL: ["sslscan"],
    VAPTScanType.CONTAINER: ["trivy"],
    VAPTScanType.LLM: ["garak"],
    VAPTScanType.CODE_REVIEW: ["code-review"],
    # FULL = every agent-visible tool (all scan types: network, web, API,
    # SSL/TLS, container, AI/LLM security).
    VAPTScanType.FULL: sorted(
        tid for tid, tool in TOOLS_REGISTRY.items() if tool.agent_visible
    ),
}

# =============================================================================
# AGENT GATING (Phase 1 - autonomous agent loop)
# phase:     recon | web | deep  (mirrors ReconOrchestrator.TOOL_PHASES)
# dangerous: requires manual operator approval before execution (RedAmon-style)
# =============================================================================
TOOL_GATING: Dict[str, Dict[str, Any]] = {
    "nmap": {"phase": "recon"},
    "masscan": {"phase": "recon", "dangerous": True},
    "dnsrecon": {"phase": "recon"},
    "subfinder": {"phase": "recon"},
    "httpx": {"phase": "web"},
    "nikto": {"phase": "web"},
    "whatweb": {"phase": "web"},
    "wafw00f": {"phase": "web"},
    "gobuster": {"phase": "web", "dangerous": True},
    "ffuf": {"phase": "web", "dangerous": True},
    "wfuzz": {"phase": "web", "dangerous": True},
    "arjun": {"phase": "web"},
    "katana": {"phase": "web"},
    "feroxbuster": {"phase": "web", "dangerous": True},
    "dirsearch": {"phase": "web"},
    "forms": {"phase": "web", "dangerous": True},
    "nuclei": {"phase": "web", "dangerous": True},
    "graphqlmap": {"phase": "web"},
    "smuggler": {"phase": "web", "dangerous": True},
    "kiterunner": {"phase": "web", "dangerous": True},
    "sqlmap": {"phase": "deep", "dangerous": True},
    "commix": {"phase": "deep", "dangerous": True},
    "dalfox": {"phase": "deep", "dangerous": True},
    "xsstrike": {"phase": "deep", "dangerous": True},
    "hydra": {"phase": "deep", "dangerous": True},
    "metasploit": {"phase": "deep", "dangerous": True},
    "sslscan": {"phase": "deep"},
    "testssl": {"phase": "deep"},
    "trivy": {"phase": "deep"},
    "gitleaks": {"phase": "deep", "dangerous": True},
    "trufflehog": {"phase": "deep", "dangerous": True},
    "semgrep": {"phase": "deep"},
    "bandit": {"phase": "deep"},
    "searchsploit": {"phase": "deep"},
    "zap": {"phase": "deep", "dangerous": True},
    "garak": {"phase": "deep"},
    "api-surface": {"phase": "web"},
    "code-review": {"phase": "deep"},
    "flows": {"phase": "deep"},
    "dom-xss": {"phase": "deep"},
}

for _tid, _gate in TOOL_GATING.items():
    _tool = TOOLS_REGISTRY.get(_tid)
    if _tool:
        _tool.dangerous = bool(_gate.get("dangerous", False))
        _tool.phase = _gate.get("phase", "recon")

PHASE_ORDER = ["recon", "web", "deep"]

PHASE_LABELS = {
    "recon": "Reconnaissance",
    "web": "Web Enumeration & Vulnerability Testing",
    "deep": "Deep Exploitation & Verification",
}

# Container-only scans have no web/network target for the agent loop; the
# orchestrator falls back to the classic pipeline for them.
AGENT_LOOP_CATEGORIES = {
    VAPTScanType.NETWORK,
    VAPTScanType.WEB,
    VAPTScanType.API,
    VAPTScanType.SSL,
    VAPTScanType.CODE_REVIEW,
    VAPTScanType.FULL,
}


def get_agent_pool(scan_type: VAPTScanType) -> List[VAPTTool]:
    """Tools the autonomous agent may call for a scan type (phase-gated)."""
    if scan_type == VAPTScanType.CONTAINER:
        return []
    pool = [
        TOOLS_REGISTRY[tid]
        for tid, tool in TOOLS_REGISTRY.items()
        if tool.agent_visible
    ]
    if scan_type == VAPTScanType.SSL:
        pool = [t for t in pool if t.phase in ("recon", "deep")]
    elif scan_type == VAPTScanType.NETWORK:
        pool = [t for t in pool if t.phase != "web"]
    elif scan_type == VAPTScanType.API:
        pool = [t for t in pool if t.phase in ("recon", "web")]
    elif scan_type == VAPTScanType.CODE_REVIEW:
        pool = [t for t in pool if t.id in (
            "code-review", "gitleaks", "trufflehog", "semgrep", "bandit", "flows",
        )]
    return pool


def get_tools_by_phase() -> Dict[str, List[str]]:
    by_phase: Dict[str, List[str]] = {p: [] for p in PHASE_ORDER}
    for tid, tool in TOOLS_REGISTRY.items():
        if tool.agent_visible:
            by_phase.setdefault(tool.phase, []).append(tid)
    return by_phase


def tool_openai_schema(tool: VAPTTool) -> Dict[str, Any]:
    """OpenAI function-calling schema for an agent-visible tool."""
    description = tool.description
    if tool.dangerous:
        description += " [REQUIRES OPERATOR APPROVAL BEFORE EXECUTION]"
    return {
        "type": "function",
        "function": {
            "name": tool.id,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "The scan target (host, IP or URL).",
                    },
                    "extra_args": {
                        "type": "string",
                        "description": (
                            "Optional extra command-line arguments for the tool. "
                            "Alphanumerics, spaces, -_.=,/ and : only."
                        ),
                    },
                },
                "required": ["target"],
            },
        },
    }


def validate_extra_args(extra_args: str) -> bool:
    """Reject shell metacharacters in agent-supplied tool arguments."""
    if not extra_args:
        return True
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_.=,/:'\"")
    return all(c in allowed for c in extra_args) and "&&" not in extra_args


def get_tool(tool_id: str) -> Optional[VAPTTool]:
    return TOOLS_REGISTRY.get(tool_id)


def get_tools_for_scan_type(scan_type: VAPTScanType) -> List[VAPTTool]:
    tool_ids = DEFAULT_TOOLS.get(scan_type, ["nmap"])
    return [TOOLS_REGISTRY[tid] for tid in tool_ids if tid in TOOLS_REGISTRY]


def check_tool_availability() -> Dict[str, bool]:
    """Tools run inside the astraix-kali container, not the backend process.

    Probes the actual binaries in the image with a single container run;
    falls back to host `which` checks only when the image is missing.
    Cached for AVAILABILITY_TTL seconds - the probe launches a container
    run (~18s) and the planner calls this once per scan plan.
    """
    from app.vapt.executor import VAPTExecutor

    cached = getattr(check_tool_availability, "_cached", None)
    cached_at = getattr(check_tool_availability, "_cached_at", 0.0)
    if cached is not None and time.time() - cached_at < AVAILABILITY_TTL:
        return cached

    def _store(result: Dict[str, bool]) -> Dict[str, bool]:
        check_tool_availability._cached = result
        check_tool_availability._cached_at = time.time()
        return result

    def _probe_cmd(tool_id: str, tool: VAPTTool) -> str:
        # Scanner scripts live in /opt/vapt inside the Kali image (not PATH).
        script_file = {
            "forms": "web_form_scanner.py",
            "api-surface": "api_surface_scanner.py",
            "garak": "garak_scanner.py",
        }.get(tool_id)
        if script_file:
            return f"test -f /opt/vapt/{script_file} && echo 'OK {tool_id}' || echo 'MISS {tool_id}'"
        return f"command -v {tool.command} >/dev/null 2>&1 && echo 'OK {tool_id}' || echo 'MISS {tool_id}'"

    try:
        result = subprocess.run(
            ["docker", "image", "inspect", VAPTExecutor.KALI_IMAGE],
            capture_output=True,
            timeout=10,
        )
        if result.returncode == 0:
            script = "; ".join(
                _probe_cmd(tool_id, tool)
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
            return _store(availability)
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
    return _store(available)


def get_available_tools() -> List[str]:
    avail = check_tool_availability()
    return [tid for tid, is_avail in avail.items() if is_avail]