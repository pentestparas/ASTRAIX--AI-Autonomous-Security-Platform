"""
Kali Linux Security Tool Registry

Comprehensive registry of security tools available in Kali Linux.
Organized by category with metadata about each tool.

All tools listed here are available in Kali Linux by default.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum

from app.scanner.models import ToolCapability


class ToolCategory(str, Enum):
    """Tool categories matching VAPT workflow."""
    RECONNAISSANCE = "reconnaissance"
    NETWORK_SCANNING = "network_scanning"
    VULNERABILITY_SCANNING = "vulnerability_scanning"
    WEB_APPLICATION = "web_application"
    WEB_ATTACKS = "web_attacks"
    DATABASE = "database"
    PASSWORD = "password"
    WIRELESS = "wireless"
    REVERSE_ENGINEERING = "reverse_engineering"
    EXPLOITATION = "exploitation"
    SNIFFING_SPOOFING = "sniffing_spoofing"
    POST_EXPLOITATION = "post_exploitation"
    FORENSICS = "forensics"
    CLOUD = "cloud"
    CONTAINER = "container"
    CODE_QUALITY = "code_quality"


@dataclass
class ToolInfo:
    """Metadata about a security tool."""
    id: str
    name: str
    description: str
    category: ToolCategory
    capabilities: List[ToolCapability]
    command: str
    install_check: str  # Command to verify tool is installed

    # Tool behavior
    supports_deep_scan: bool = True
    supports_aggressive: bool = False
    supports_rate_limit: bool = False

    # Performance
    default_timeout: int = 300  # seconds
    memory_requirement: str = "low"  # low, medium, high
    cpu_intensive: bool = False

    # Output
    output_format: str = "text"  # text, xml, json, csv
    needs_root: bool = False

    # Web-specific
    target_type: str = "ip"  # ip, url, domain, file

    @property
    def tool_id(self) -> str:
        return f"tools/{self.id}"


@dataclass
class ToolConfig:
    """Default configuration for a tool."""
    base_command: str
    args: List[str] = field(default_factory=list)
    env_vars: Dict[str, str] = field(default_factory=dict)


# Tool Registry
TOOLS: Dict[str, ToolInfo] = {}

# ============================================================================
# NETWORK SCANNING & RECONNAISSANCE
# ============================================================================

TOOLS["nmap"] = ToolInfo(
    id="nmap",
    name="Nmap",
    description="Network discovery and security auditing tool. Maps network topology, identifies live hosts, and detects services/versions.",
    category=ToolCategory.NETWORK_SCANNING,
    capabilities=[ToolCapability.NETWORK_VAPT],
    command="nmap",
    install_check="nmap --version",
    supports_deep_scan=True,
    supports_aggressive=True,
    supports_rate_limit=True,
    default_timeout=600,
    cpu_intensive=True,
    output_format="xml",
    needs_root=True,
    target_type="ip",
)

TOOLS["masscan"] = ToolInfo(
    id="masscan",
    name="Masscan",
    description="Fast TCP port scanner. Can scan entire internet in under 6 minutes.",
    category=ToolCategory.NETWORK_SCANNING,
    capabilities=[ToolCapability.NETWORK_VAPT],
    command="masscan",
    install_check="masscan --version",
    supports_deep_scan=False,
    supports_rate_limit=True,
    default_timeout=300,
    cpu_intensive=True,
    output_format="json",
    needs_root=True,
    target_type="ip",
)

TOOLS["netdiscover"] = ToolInfo(
    id="netdiscover",
    name="Netdiscover",
    description="Active/passive ARP reconnaissance tool for discovering hosts.",
    category=ToolCategory.RECONNAISSANCE,
    capabilities=[ToolCapability.NETWORK_VAPT],
    command="netdiscover",
    install_check="netdiscover -h",
    supports_deep_scan=False,
    default_timeout=120,
    needs_root=True,
    target_type="ip",
)

TOOLS["unicornscan"] = ToolInfo(
    id="unicornscan",
    name="Unicornscan",
    description="Asynchronous TCP/UDP port scanner with accurate OS fingerprinting.",
    category=ToolCategory.NETWORK_SCANNING,
    capabilities=[ToolCapability.NETWORK_VAPT],
    command="unicornscan",
    install_check="unicornscan -h",
    supports_deep_scan=False,
    supports_rate_limit=True,
    default_timeout=300,
    cpu_intensive=True,
    needs_root=True,
    target_type="ip",
)

TOOLS["recon-ng"] = ToolInfo(
    id="recon-ng",
    name="Recon-ng",
    description="Full-featured web reconnaissance framework.",
    category=ToolCategory.RECONNAISSANCE,
    capabilities=[ToolCapability.NETWORK_VAPT, ToolCapability.WEB_VAPT],
    command="recon-ng",
    install_check="recon-ng --version",
    supports_deep_scan=True,
    default_timeout=600,
    target_type="domain",
)

TOOLS["theHarvester"] = ToolInfo(
    id="theHarvester",
    name="theHarvester",
    description="Email, subdomain, and personnel harvester from public sources.",
    category=ToolCategory.RECONNAISSANCE,
    capabilities=[ToolCapability.NETWORK_VAPT],
    command="theHarvester",
    install_check="theHarvester -h",
    supports_deep_scan=True,
    default_timeout=300,
    target_type="domain",
)

# ============================================================================
# VULNERABILITY SCANNING
# ============================================================================

TOOLS["nikto"] = ToolInfo(
    id="nikto",
    name="Nikto",
    description="Web server scanner for vulnerabilities, outdated software, and misconfigurations.",
    category=ToolCategory.VULNERABILITY_SCANNING,
    capabilities=[ToolCapability.WEB_VAPT, ToolCapability.NETWORK_VAPT],
    command="nikto",
    install_check="nikto -Version",
    supports_deep_scan=True,
    supports_aggressive=True,
    default_timeout=600,
    cpu_intensive=True,
    output_format="xml",
    target_type="url",
)

TOOLS["nuclei"] = ToolInfo(
    id="nuclei",
    name="Nuclei",
    description="Fast, customizable vulnerability scanner based on YAML templates.",
    category=ToolCategory.VULNERABILITY_SCANNING,
    capabilities=[ToolCapability.WEB_VAPT, ToolCapability.NETWORK_VAPT],
    command="nuclei",
    install_check="nuclei -version",
    supports_deep_scan=True,
    supports_rate_limit=True,
    default_timeout=1800,
    cpu_intensive=True,
    output_format="json",
    target_type="url",
)

TOOLS["openvas"] = ToolInfo(
    id="openvas",
    name="OpenVAS",
    description="Full-featured vulnerability scanner with comprehensive CVE coverage.",
    category=ToolCategory.VULNERABILITY_SCANNING,
    capabilities=[ToolCapability.NETWORK_VAPT, ToolCapability.WEB_VAPT],
    command="omp",
    install_check="omp --version",
    supports_deep_scan=True,
    default_timeout=3600,
    cpu_intensive=True,
    memory_requirement="high",
    target_type="ip",
)

TOOLS["nessus"] = ToolInfo(
    id="nessus",
    name="Nessus",
    description="Enterprise vulnerability scanner (requires license).",
    category=ToolCategory.VULNERABILITY_SCANNING,
    capabilities=[ToolCapability.NETWORK_VAPT, ToolCapability.WEB_VAPT],
    command="nessus",
    install_check="nessus --version",
    supports_deep_scan=True,
    default_timeout=3600,
    cpu_intensive=True,
    memory_requirement="high",
    target_type="ip",
)

# ============================================================================
# WEB APPLICATION TESTING
# ============================================================================

TOOLS["sqlmap"] = ToolInfo(
    id="sqlmap",
    name="SQLMap",
    description="Automated SQL injection and database takeover tool.",
    category=ToolCategory.WEB_ATTACKS,
    capabilities=[ToolCapability.WEB_VAPT, ToolCapability.API_SECURITY],
    command="sqlmap",
    install_check="sqlmap --version",
    supports_deep_scan=True,
    supports_aggressive=True,
    default_timeout=1800,
    cpu_intensive=True,
    output_format="json",
    target_type="url",
)

TOOLS["xsstrike"] = ToolInfo(
    id="xsstrike",
    name="XSStrike",
    description="Advanced XSS detection and exploitation suite.",
    category=ToolCategory.WEB_ATTACKS,
    capabilities=[ToolCapability.WEB_VAPT],
    command="xsstrike",
    install_check="xsstrike --version",
    supports_deep_scan=True,
    supports_aggressive=True,
    default_timeout=600,
    output_format="json",
    target_type="url",
)

TOOLS["dalfox"] = ToolInfo(
    id="dalfox",
    name="Dalfox",
    description="Fast, accurate XSS scanner with mining and analysis features.",
    category=ToolCategory.WEB_ATTACKS,
    capabilities=[ToolCapability.WEB_VAPT],
    command="dalfox",
    install_check="dalfox version",
    supports_deep_scan=True,
    supports_aggressive=True,
    default_timeout=600,
    output_format="json",
    target_type="url",
)

TOOLS["ffuf"] = ToolInfo(
    id="ffuf",
    name="FFUF",
    description="Fast web fuzzer for directory, vhost, and parameter fuzzing.",
    category=ToolCategory.WEB_APPLICATION,
    capabilities=[ToolCapability.WEB_VAPT],
    command="ffuf",
    install_check="ffuf --version",
    supports_deep_scan=False,
    supports_rate_limit=True,
    default_timeout=600,
    cpu_intensive=True,
    output_format="json",
    target_type="url",
)

TOOLS["gobuster"] = ToolInfo(
    id="gobuster",
    name="Gobuster",
    description="Directory/file/dns/vhost busting tool.",
    category=ToolCategory.WEB_APPLICATION,
    capabilities=[ToolCapability.WEB_VAPT],
    command="gobuster",
    install_check="gobuster version",
    supports_deep_scan=False,
    supports_rate_limit=True,
    default_timeout=600,
    output_format="json",
    target_type="url",
)

TOOLS["dirb"] = ToolInfo(
    id="dirb",
    name="DIRB",
    description="Web content scanner for discovering hidden directories.",
    category=ToolCategory.WEB_APPLICATION,
    capabilities=[ToolCapability.WEB_VAPT],
    command="dirb",
    install_check="dirb",
    supports_deep_scan=False,
    default_timeout=600,
    output_format="text",
    target_type="url",
)

TOOLS["dirbuster"] = ToolInfo(
    id="dirbuster",
    name="DirBuster",
    description="Multi-threaded Java-based web directory/file brute-forcing tool.",
    category=ToolCategory.WEB_APPLICATION,
    capabilities=[ToolCapability.WEB_VAPT],
    command="dirbuster",
    install_check="dirbuster",
    supports_deep_scan=False,
    default_timeout=600,
    target_type="url",
)

TOOLS["wfuzz"] = ToolInfo(
    id="wfuzz",
    name="WFuzz",
    description="Flexible web application fuzzer for parameter and injection testing.",
    category=ToolCategory.WEB_APPLICATION,
    capabilities=[ToolCapability.WEB_VAPT],
    command="wfuzz",
    install_check="wfuzz --version",
    supports_deep_scan=True,
    supports_rate_limit=True,
    default_timeout=600,
    output_format="json",
    target_type="url",
)

TOOLS["commix"] = ToolInfo(
    id="commix",
    name="Commix",
    description="Automated command injection exploit tool.",
    category=ToolCategory.WEB_ATTACKS,
    capabilities=[ToolCapability.WEB_VAPT],
    command="commix",
    install_check="commix --version",
    supports_deep_scan=True,
    supports_aggressive=True,
    default_timeout=600,
    output_format="json",
    target_type="url",
)

# ============================================================================
# API SECURITY
# ============================================================================

TOOLS["restful-api-tools"] = ToolInfo(
    id="restful-api-tools",
    name="RESTful API Tools",
    description="Collection of tools for API security testing.",
    category=ToolCategory.WEB_APPLICATION,
    capabilities=[ToolCapability.API_SECURITY],
    command="http",
    install_check="curl --version",
    supports_deep_scan=True,
    default_timeout=300,
    target_type="url",
)

# ============================================================================
# SSL/TLS TESTING
# ============================================================================

TOOLS["sslscan"] = ToolInfo(
    id="sslscan",
    name="SSLyze",
    description="Fast, full-featured SSL/TLS scanner for vulnerabilities.",
    category=ToolCategory.VULNERABILITY_SCANNING,
    capabilities=[ToolCapability.SSL_SECURITY, ToolCapability.NETWORK_VAPT],
    command="sslscan",
    install_check="sslscan --version",
    supports_deep_scan=True,
    default_timeout=300,
    output_format="xml",
    target_type="ip",
)

TOOLS["testssl"] = ToolInfo(
    id="testssl",
    name="testssl.sh",
    description="Comprehensive TLS/SSL testing tool for vulnerabilities.",
    category=ToolCategory.VULNERABILITY_SCANNING,
    capabilities=[ToolCapability.SSL_SECURITY, ToolCapability.NETWORK_VAPT],
    command="testssl",
    install_check="testssl.sh --version",
    supports_deep_scan=True,
    default_timeout=600,
    cpu_intensive=True,
    output_format="json",
    target_type="url",
)

TOOLS["nmap-ssl"] = ToolInfo(
    id="nmap-ssl",
    name="Nmap SSL Enum",
    description="Nmap NSE scripts for SSL/TLS enumeration and vulnerability detection.",
    category=ToolCategory.VULNERABILITY_SCANNING,
    capabilities=[ToolCapability.SSL_SECURITY, ToolCapability.NETWORK_VAPT],
    command="nmap",
    install_check="nmap --version",
    supports_deep_scan=True,
    default_timeout=300,
    output_format="xml",
    needs_root=True,
    target_type="ip",
)

# ============================================================================
# CLOUD SECURITY
# ============================================================================

TOOLS["prowler"] = ToolInfo(
    id="prowler",
    name="Prowler",
    description="AWS security best practices assessment, auditing, and hardening.",
    category=ToolCategory.CLOUD,
    capabilities=[ToolCapability.CLOUD_SECURITY],
    command="prowler",
    install_check="prowler --version",
    supports_deep_scan=True,
    default_timeout=1800,
    cpu_intensive=True,
    output_format="json",
    target_type="domain",
)

TOOLS["scoutsuite"] = ToolInfo(
    id="scoutsuite",
    name="Scout Suite",
    description="Multi-cloud security auditing tool for AWS, Azure, GCP.",
    category=ToolCategory.CLOUD,
    capabilities=[ToolCapability.CLOUD_SECURITY],
    command="scout",
    install_check="scout --version",
    supports_deep_scan=True,
    default_timeout=1800,
    cpu_intensive=True,
    memory_requirement="medium",
    output_format="json",
    target_type="domain",
)

TOOLS["cloudsploit"] = ToolInfo(
    id="cloudsploit",
    name="CloudSploit",
    description="Cloud infrastructure security scanner for AWS, Azure, GCP.",
    category=ToolCategory.CLOUD,
    capabilities=[ToolCapability.CLOUD_SECURITY],
    command="cloudsploit",
    install_check="cloudsploit --version",
    supports_deep_scan=True,
    default_timeout=1800,
    cpu_intensive=True,
    output_format="json",
    target_type="domain",
)

TOOLS["cartography"] = ToolInfo(
    id="cartography",
    name="Cartography",
    description="Cyber security exploration tool for AWS, GCP, Azure.",
    category=ToolCategory.CLOUD,
    capabilities=[ToolCapability.CLOUD_SECURITY],
    command="cartography",
    install_check="cartography --version",
    supports_deep_scan=True,
    default_timeout=1800,
    memory_requirement="medium",
    output_format="json",
    target_type="domain",
)

# ============================================================================
# CONTAINER SECURITY
# ============================================================================

TOOLS["trivy"] = ToolInfo(
    id="trivy",
    name="Trivy",
    description="Comprehensive vulnerability scanner for containers and Kubernetes.",
    category=ToolCategory.CONTAINER,
    capabilities=[ToolCapability.CONTAINER_SECURITY],
    command="trivy",
    install_check="trivy --version",
    supports_deep_scan=True,
    default_timeout=600,
    memory_requirement="medium",
    output_format="json",
    target_type="file",
)

TOOLS["anchore"] = ToolInfo(
    id="anchore",
    name="Anchore",
    description="Deep image analysis for vulnerabilities and policy violations.",
    category=ToolCategory.CONTAINER,
    capabilities=[ToolCapability.CONTAINER_SECURITY],
    command="anchore-cli",
    install_check="anchore-cli --version",
    supports_deep_scan=True,
    default_timeout=600,
    memory_requirement="medium",
    output_format="json",
    target_type="file",
)

# ============================================================================
# CODE QUALITY / STATIC ANALYSIS
# ============================================================================

TOOLS["semgrep"] = ToolInfo(
    id="semgrep",
    name="Semgrep",
    description="Fast, powerful static analysis tool for security and correctness.",
    category=ToolCategory.CODE_QUALITY,
    capabilities=[ToolCapability.CODE_AUDIT],
    command="semgrep",
    install_check="semgrep --version",
    supports_deep_scan=True,
    default_timeout=600,
    cpu_intensive=True,
    output_format="json",
    target_type="file",
)

TOOLS["bandit"] = ToolInfo(
    id="bandit",
    name="Bandit",
    description="Python security issue detector by finding common security issues.",
    category=ToolCategory.CODE_QUALITY,
    capabilities=[ToolCapability.CODE_AUDIT],
    command="bandit",
    install_check="bandit --version",
    supports_deep_scan=True,
    default_timeout=300,
    output_format="json",
    target_type="file",
)

TOOLS["sonarqube"] = ToolInfo(
    id="sonarqube",
    name="SonarQube",
    description="Code quality and security analyzer (requires server).",
    category=ToolCategory.CODE_QUALITY,
    capabilities=[ToolCapability.CODE_AUDIT],
    command="sonar-scanner",
    install_check="sonar-scanner --version",
    supports_deep_scan=True,
    default_timeout=1800,
    cpu_intensive=True,
    memory_requirement="high",
    output_format="json",
    target_type="file",
)

TOOLS["checkov"] = ToolInfo(
    id="checkov",
    name="Checkov",
    description="Infrastructure as code security scanner for Terraform, CloudFormation.",
    category=ToolCategory.CODE_QUALITY,
    capabilities=[ToolCapability.CODE_AUDIT, ToolCapability.CLOUD_SECURITY],
    command="checkov",
    install_check="checkov --version",
    supports_deep_scan=True,
    default_timeout=600,
    output_format="json",
    target_type="file",
)

# ============================================================================
# PASSWORD ATTACKS
# ============================================================================

TOOLS["hydra"] = ToolInfo(
    id="hydra",
    name="Hydra",
    description="Parallelized login cracker supporting 50+ protocols.",
    category=ToolCategory.PASSWORD,
    capabilities=[ToolCapability.NETWORK_VAPT],
    command="hydra",
    install_check="hydra -h",
    supports_deep_scan=True,
    supports_rate_limit=True,
    default_timeout=3600,
    cpu_intensive=True,
    needs_root=True,
    target_type="ip",
)

TOOLS["hashcat"] = ToolInfo(
    id="hashcat",
    name="Hashcat",
    description="Fast password recovery tool and hash cracker.",
    category=ToolCategory.PASSWORD,
    capabilities=[ToolCapability.CODE_AUDIT],
    command="hashcat",
    install_check="hashcat --version",
    supports_deep_scan=True,
    default_timeout=3600,
    cpu_intensive=True,
    memory_requirement="high",
    target_type="file",
)

TOOLS["john"] = ToolInfo(
    id="john",
    name="John the Ripper",
    description="Fast password cracker supporting hundreds of hash types.",
    category=ToolCategory.PASSWORD,
    capabilities=[ToolCapability.CODE_AUDIT],
    command="john",
    install_check="john --version",
    supports_deep_scan=True,
    default_timeout=3600,
    cpu_intensive=True,
    target_type="file",
)

# ============================================================================
# WIRELESS SECURITY
# ============================================================================

TOOLS["aircrack-ng"] = ToolInfo(
    id="aircrack-ng",
    name="Aircrack-ng",
    description="Complete suite for wireless network security assessment.",
    category=ToolCategory.WIRELESS,
    capabilities=[ToolCapability.NETWORK_VAPT],
    command="aircrack-ng",
    install_check="aircrack-ng --help",
    supports_deep_scan=True,
    default_timeout=3600,
    cpu_intensive=True,
    memory_requirement="medium",
    needs_root=True,
    target_type="file",
)

TOOLS["kismet"] = ToolInfo(
    id="kismet",
    name="Kismet",
    description="Wireless network detector, sniffer, and IDS.",
    category=ToolCategory.WIRELESS,
    capabilities=[ToolCapability.NETWORK_VAPT],
    command="kismet",
    install_check="kismet --version",
    supports_deep_scan=True,
    default_timeout=3600,
    cpu_intensive=True,
    memory_requirement="medium",
    needs_root=True,
    target_type="domain",
)

# ============================================================================
# DNS RECONNAISSANCE
# ============================================================================

TOOLS["dnsenum"] = ToolInfo(
    id="dnsenum",
    name="DNS Enum",
    description="Perl script for DNS enumeration and zone transfer testing.",
    category=ToolCategory.RECONNAISSANCE,
    capabilities=[ToolCapability.DNS_RECON, ToolCapability.NETWORK_VAPT],
    command="dnsenum",
    install_check="dnsenum",
    supports_deep_scan=True,
    default_timeout=300,
    target_type="domain",
)

TOOLS["dnsrecon"] = ToolInfo(
    id="dnsrecon",
    name="DNS Recon",
    description="Powerful DNS enumeration and zone transfer tool.",
    category=ToolCategory.RECONNAISSANCE,
    capabilities=[ToolCapability.DNS_RECON, ToolCapability.NETWORK_VAPT],
    command="dnsrecon",
    install_check="dnsrecon --version",
    supports_deep_scan=True,
    default_timeout=300,
    output_format="json",
    target_type="domain",
)

TOOLS["fierce"] = ToolInfo(
    id="fierce",
    name="Fierce",
    description="DNS reconnaissance tool for locating non-contiguous IP space.",
    category=ToolCategory.RECONNAISSANCE,
    capabilities=[ToolCapability.DNS_RECON, ToolCapability.NETWORK_VAPT],
    command="fierce",
    install_check="fierce --version",
    supports_deep_scan=True,
    default_timeout=300,
    target_type="domain",
)


# Tool Categories for UI grouping
TOOL_CATEGORIES = {
    "Network VAPT": ["nmap", "masscan", "netdiscover", "unicornscan", "nikto", "nuclei", "hydra", "dnsrecon", "dnsenum"],
    "Web App VAPT": ["nikto", "sqlmap", "xsstrike", "dalfox", "ffuf", "gobuster", "dirb", "wfuzz", "commix"],
    "Cloud Security": ["prowler", "scoutsuite", "cloudsploit", "cartography"],
    "Code Audit": ["semgrep", "bandit", "sonarqube", "checkov"],
    "Container Security": ["trivy", "anchore"],
    "SSL Security": ["sslscan", "testssl", "nmap-ssl"],
    "Password Attacks": ["hydra", "hashcat", "john"],
    "Wireless": ["aircrack-ng", "kismet"],
}


# Tools by capability
NETWORK_SCANNERS = ["nmap", "masscan", "netdiscover", "unicornscan", "recon-ng", "theHarvester"]
WEB_SCANNERS = ["nikto", "sqlmap", "xsstrike", "dalfox", "ffuf", "gobuster", "dirb", "wfuzz", "commix", "nuclei"]
CLOUD_SCANNERS = ["prowler", "scoutsuite", "cloudsploit", "cartography"]
CODE_SCANNERS = ["semgrep", "bandit", "sonarqube", "checkov"]
CONTAINER_SCANNERS = ["trivy", "anchore"]


class ToolRegistry:
    """Registry for managing security tools."""

    def __init__(self):
        self._tools: Dict[str, ToolInfo] = TOOLS.copy()
        self._tool_configs: Dict[str, ToolConfig] = {}

    def get(self, tool_id: str) -> Optional[ToolInfo]:
        """Get tool info by ID."""
        # Handle both "nmap" and "tools/nmap" formats
        clean_id = tool_id.replace("tools/", "")
        return self._tools.get(clean_id)

    def list_all(self) -> List[ToolInfo]:
        """List all registered tools."""
        return list(self._tools.values())

    def list_by_category(self, category: ToolCategory) -> List[ToolInfo]:
        """List tools in a specific category."""
        return [t for t in self._tools.values() if t.category == category]

    def list_by_capability(self, capability: ToolCapability) -> List[ToolInfo]:
        """List tools supporting a specific capability."""
        return [t for t in self._tools.values() if capability in t.capabilities]

    def list_by_ids(self, tool_ids: List[str]) -> List[ToolInfo]:
        """Get multiple tools by their IDs."""
        return [self.get(tid) for tid in tool_ids if self.get(tid)]

    def is_installed(self, tool_id: str) -> bool:
        """Check if a tool is installed on the system."""
        import subprocess
        tool = self.get(tool_id)
        if not tool:
            return False
        try:
            result = subprocess.run(
                tool.install_check.split(),
                capture_output=True,
                timeout=5,
                check=False,
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_installed_tools(self) -> List[ToolInfo]:
        """Get list of all installed tools."""
        return [t for t in self._tools.values() if self.is_installed(t.id)]

    def get_command(self, tool_id: str, target: str, deep: bool = False,
                    aggressive: bool = False, **kwargs) -> str:
        """Build command line for a tool."""
        tool = self.get(tool_id)
        if not tool:
            raise ValueError(f"Unknown tool: {tool_id}")

        cmd_parts = [tool.command]

        # Add target based on tool's target type
        if tool.target_type == "url" and not target.startswith(("http://", "https://")):
            target = f"http://{target}"

        # Build command based on tool-specific logic
        if tool_id == "nmap":
            cmd_parts.append("-sV")  # Version detection
            if deep:
                cmd_parts.extend(["-O", "-sC"])  # OS detection, default scripts
            if aggressive:
                cmd_parts.append("-A")  # Aggressive scan
            cmd_parts.extend(["-oX", "-"])  # XML output to stdout
            cmd_parts.append(target)

        elif tool_id == "masscan":
            cmd_parts.extend(["--rate", str(kwargs.get("rate_limit", 10000))])
            cmd_parts.extend(["-oJ", "-"])  # JSON output to stdout
            cmd_parts.append(target)

        elif tool_id == "nikto":
            cmd_parts.extend(["-Format", "xml", "-output", "-"])
            if deep:
                cmd_parts.extend(["-Tuning", "1,2,3,4,5,6,7,8,9"])
            cmd_parts.extend(["-host", target])

        elif tool_id == "sqlmap":
            cmd_parts.extend(["--batch", "--json-output", "--output-dir=/tmp"])
            if deep:
                cmd_parts.append("--level=5")
                cmd_parts.append("--risk=3")
            else:
                cmd_parts.append("--level=2")
                cmd_parts.append("--risk=2")
            cmd_parts.extend(["--url", target])

        elif tool_id == "nuclei":
            cmd_parts.extend(["-json-export", "-"])
            if deep:
                cmd_parts.append("-severity", "info,low,medium,high,critical")
            else:
                cmd_parts.append("-severity", "medium,high,critical")
            cmd_parts.extend(["-u", target])

        elif tool_id == "gobuster":
            cmd_parts.extend(["-o", "-", "-f", "-j"])
            if deep:
                cmd_parts.extend(["-w", "/usr/share/wordlists/dirb/big.txt"])
            else:
                cmd_parts.extend(["-w", "/usr/share/wordlists/dirb/common.txt"])
            cmd_parts.extend(["-u", target])

        elif tool_id == "sslscan":
            cmd_parts.extend(["--xml=-"])
            cmd_parts.append(target)

        elif tool_id == "testssl":
            cmd_parts.extend(["--jsonfile=-", "--pretty"])
            cmd_parts.append(target)

        elif tool_id == "trivy":
            cmd_parts.extend(["--format", "json", "--security-checks", "vulnerabilities"])
            cmd_parts.append(target)

        elif tool_id == "semgrep":
            cmd_parts.extend(["--json", "--quiet"])
            cmd_parts.append(target)

        elif tool_id == "dnsrecon":
            cmd_parts.extend(["--json", "-z"])  # DNSSEC
            cmd_parts.extend(["-d", target])

        else:
            # Default: just append target
            cmd_parts.append(target)

        return " ".join(cmd_parts)


# Global registry instance
_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """Get the global tool registry instance."""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry