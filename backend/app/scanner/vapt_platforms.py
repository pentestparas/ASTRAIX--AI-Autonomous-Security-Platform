"""
VAPT Platform Integration Module

Integrates with external AI-powered VAPT platforms for enhanced security testing.
Supports: Dark-Moon, PentAGI, and direct Kali Linux tool execution.

Enterprise Features:
- Docker container isolation for tool execution
- AI Agent orchestration (multi-agent systems)
- Knowledge graph integration
- Parallel tool execution
- Comprehensive output parsing
"""

import asyncio
import json
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from uuid import UUID, uuid4

import httpx

from app.scanner.models import (
    Finding,
    ScanRequest,
    ScanResult,
    ScanStatus,
    Severity,
    ToolCapability,
    ToolResult,
)


class PlatformType(str, Enum):
    """Supported VAPT platforms."""
    KALI_DIRECT = "kali_direct"  # Direct Kali Linux tool execution
    DARK_MOON = "dark_moon"  # AI-powered autonomous pentesting (739 stars)
    PENTAGI = "pentagi"  # Multi-agent pentesting AGI (20.8k stars)
    LYRIE = "lyrie"  # Autonomous security agent with ATP (371 stars)
    CUSTOM = "custom"  # Custom platform integration


@dataclass
class PlatformConfig:
    """Configuration for VAPT platform integration."""
    platform_type: PlatformType
    name: str
    base_url: str = ""
    api_key: Optional[str] = None
    timeout: int = 3600  # 1 hour default for AI platforms
    max_retries: int = 3
    enabled: bool = True

    # Docker settings (for Kali direct execution)
    docker_image: str = "kalilinux/kali-rolling:latest"
    docker_network: str = "bridge"
    container_timeout: int = 1800  # 30 minutes

    # Tool execution settings
    parallel_execution: bool = True
    max_concurrent_tools: int = 5

    # AI settings
    use_ai_orchestration: bool = False
    ai_model: Optional[str] = None
    ai_provider: Optional[str] = None  # openai, anthropic, ollama, etc.


@dataclass
class ExternalTool:
    """External tool integration definition."""
    name: str
    command: str
    args: List[str] = field(default_factory=list)
    output_format: str = "text"  # text, json, xml, csv
    parse_method: str = "default"  # default, nmap, nikto, sqlmap, nuclei, etc.
    timeout: int = 300
    needs_root: bool = False
    containerized: bool = True  # Run in isolated container
    env_vars: Dict[str, str] = field(default_factory=dict)


class VAPTOutputParser:
    """Parser for various VAPT tool output formats."""

    @staticmethod
    def parse_nmap(xml_output: str) -> List[Finding]:
        """Parse Nmap XML output to findings."""
        findings = []
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_output)

            for host in root.findall(".//host"):
                addr = host.find(".//address[@addrtype='ipv4']")
                if addr is None:
                    addr = host.find(".//address")
                host_addr = addr.get("addr", "unknown") if addr is not None else "unknown"

                for port in host.findall(".//port"):
                    port_id = port.get("portid", "")
                    protocol = port.get("protocol", "tcp")
                    state = port.find("state")
                    service = port.find("service")

                    if state is not None and state.get("state") == "open":
                        finding = Finding(
                            title=f"Open Port {port_id}/{protocol}",
                            description=f"Service: {service.get('name', 'unknown') if service is not None else 'unknown'}",
                            severity=Severity.MEDIUM,
                            tool_name="nmap",
                            plugin_id="tools/nmap",
                            target=host_addr,
                            port=int(port_id) if port_id.isdigit() else None,
                            protocol=protocol,
                            service=service.get("name") if service is not None else None,
                            host=host_addr,
                            details={
                                "hostnames": [
                                    h.get("name", "")
                                    for h in host.findall(".//hostname")
                                    if h.get("name")
                                ],
                                "os_fingerprint": (
                                    host.find(".//osmatch/@name")
                                    if host.find(".//osmatch") is not None
                                    else None
                                ),
                                "service_version": service.get("version") if service is not None else None,
                            },
                            remediation=f"Close port {port_id}/{protocol} if not required, or restrict access via firewall",
                            reference="https://nmap.org/book/man-port-specification.html",
                        )
                        findings.append(finding)
        except Exception as e:
            # Fallback: parse text output
            findings.extend(VAPTOutputParser._parse_nmap_text(xml_output))

        return findings

    @staticmethod
    def _parse_nmap_text(text_output: str) -> List[Finding]:
        """Parse Nmap text output as fallback."""
        findings = []
        for line in text_output.splitlines():
            if "/open/" in line and "tcp" in line:
                parts = line.split()
                if len(parts) >= 3:
                    port_proto = parts[0].split("/")
                    if len(port_proto) >= 2:
                        port, protocol = port_proto[0], port_proto[1]
                        service = parts[2] if len(parts) > 2 else "unknown"
                        finding = Finding(
                            title=f"Open Port {port}/{protocol}",
                            description=f"Service: {service}",
                            severity=Severity.MEDIUM,
                            tool_name="nmap",
                            plugin_id="tools/nmap",
                            target="",
                            port=int(port) if port.isdigit() else None,
                            protocol=protocol,
                            service=service,
                            details={"raw_line": line},
                            remediation=f"Review if port {port}/{protocol} is required",
                        )
                        findings.append(finding)
        return findings

    @staticmethod
    def parse_nikto(xml_output: str) -> List[Finding]:
        """Parse Nikto XML output to findings."""
        findings = []
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_output)

            for item in root.findall(".//item"):
                finding = Finding(
                    id=uuid4(),
                    title=item.get("name", "Nikto Finding"),
                    description=item.get("description", ""),
                    severity=VAPTOutputParser._nikto_severity(item.get("osvdbid", "")),
                    tool_name="nikto",
                    plugin_id="tools/nikto",
                    target=root.get("target", ""),
                    details={
                        "osvdb": item.get("osvdbid"),
                        "site": item.get("site"),
                        "type": item.get("type"),
                    },
                    remediation="Review and apply security hardening to address the finding",
                )
                findings.append(finding)
        except Exception:
            pass
        return findings

    @staticmethod
    def _nikto_severity(osvdb_id: str) -> Severity:
        """Map Nikto OSVDB ID to severity."""
        if not osvdb_id:
            return Severity.MEDIUM
        return Severity.HIGH

    @staticmethod
    def parse_nuclei(json_output: str) -> List[Finding]:
        """Parse Nuclei JSON output to findings."""
        findings = []
        try:
            for line in json_output.strip().splitlines():
                if not line.strip():
                    continue
                data = json.loads(line)

                if data.get("type") != "vulnerability":
                    continue

                info = data.get("info", {})
                matched = data.get("matched-at", "")

                # Extract CVSS if available
                cvss = None
                reference_links = []
                for ref in info.get("reference", []):
                    if "cvss" in ref.lower():
                        try:
                            cvss = float(ref.split("=")[1])
                        except (ValueError, IndexError):
                            pass
                    reference_links.append(ref)

                # Map severity
                severity_str = info.get("severity", "medium").lower()
                severity = VAPTOutputParser._map_severity(severity_str)

                finding = Finding(
                    id=uuid4(),
                    title=info.get("name", "Nuclei Finding"),
                    description=info.get("description", ""),
                    severity=severity,
                    cvss_score=cvss,
                    tool_name="nuclei",
                    plugin_id="tools/nuclei",
                    target=matched,
                    vulnerability_type=info.get("classification", {}).get("cwe-id"),
                    details={
                        "matched_at": matched,
                        "template": data.get("template-id"),
                        "template_url": data.get("template-url"),
                        "Matcher": data.get("matcher-name"),
                    },
                    remediation=info.get("solution", "No remediation provided"),
                    reference="; ".join(reference_links) if reference_links else None,
                )
                findings.append(finding)
        except json.JSONDecodeError:
            pass
        return findings

    @staticmethod
    def parse_sqlmap(json_output: str) -> List[Finding]:
        """Parse SQLMap JSON output to findings."""
        findings = []
        try:
            data = json.loads(json_output)

            if data.get("success", False):
                # SQL injection confirmed
                for target in data.get("data", []):
                    for injection in target.get("injectable", []):
                        finding = Finding(
                            id=uuid4(),
                            title=f"SQL Injection - {injection.get('type', 'Unknown type')}",
                            description=f"Parameter: {injection.get('parameter')}, Type: {injection.get('type')}",
                            severity=Severity.CRITICAL,
                            cvss_score=9.8,
                            tool_name="sqlmap",
                            plugin_id="tools/sqlmap",
                            target=data.get("url", ""),
                            parameter=injection.get("parameter"),
                            vulnerability_type="SQL Injection",
                            payload=injection.get("payload"),
                            details=injection,
                            remediation="Use parameterized queries or prepared statements",
                            reference="https://owasp.org/www-community/attacks/SQL_Injection",
                        )
                        findings.append(finding)
            else:
                # Check for errors indicating potential injection points
                for target in data.get("data", []):
                    for error in target.get("errors", []):
                        if "sql" in error.lower():
                            finding = Finding(
                                id=uuid4(),
                                title="Potential SQL Injection",
                                description=error,
                                severity=Severity.HIGH,
                                tool_name="sqlmap",
                                plugin_id="tools/sqlmap",
                                target=data.get("url", ""),
                                vulnerability_type="SQL Injection",
                                details={"raw_error": error},
                                remediation="Investigate parameter for SQL injection vulnerability",
                            )
                            findings.append(finding)
        except json.JSONDecodeError:
            pass
        return findings

    @staticmethod
    def _map_severity(severity_str: str) -> Severity:
        """Map tool-specific severity string to Severity enum."""
        severity_map = {
            "critical": Severity.CRITICAL,
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
            "info": Severity.INFO,
            "informational": Severity.INFO,
            "unknown": Severity.UNKNOWN,
        }
        return severity_map.get(severity_str, Severity.MEDIUM)

    @staticmethod
    def parse_gobuster(json_output: str) -> List[Finding]:
        """Parse Gobuster JSON output to findings."""
        findings = []
        try:
            data = json.loads(json_output)

            for result in data.get("result", {}).get("findings", []):
                if result.get("status") >= 200 and result.get("status") < 400:
                    severity = Severity.INFO
                elif result.get("status") >= 400 and result.get("status") < 500:
                    severity = Severity.LOW
                else:
                    severity = Severity.MEDIUM

                finding = Finding(
                    id=uuid4(),
                    title=f"Directory Found: {result.get('url')}",
                    description=f"Status: {result.get('status')}, Length: {result.get('length')}",
                    severity=severity,
                    tool_name="gobuster",
                    plugin_id="tools/gobuster",
                    target=result.get("url", ""),
                    path=result.get("url"),
                    details={
                        "status_code": result.get("status"),
                        "content_length": result.get("length"),
                        "content_type": result.get("type"),
                    },
                    remediation="If this is an unintended exposure, restrict access to sensitive paths",
                )
                findings.append(finding)
        except json.JSONDecodeError:
            pass
        return findings

    @staticmethod
    def parse_ffuf(json_output: str) -> List[Finding]:
        """Parse FFUF JSON output to findings."""
        findings = []
        try:
            data = json.loads(json_output)

            for result in data.get("results", []):
                status = result.get("status", 0)
                if status >= 200 and status < 400:
                    severity = Severity.INFO
                elif status >= 400 and status < 500:
                    severity = Severity.LOW
                else:
                    severity = Severity.MEDIUM

                finding = Finding(
                    id=uuid4(),
                    title=f"Path Discovered: {result.get('url')}",
                    description=f"Status: {status}, Words: {result.get('words')}, Lines: {result.get('lines')}",
                    severity=severity,
                    tool_name="ffuf",
                    plugin_id="tools/ffuf",
                    target=result.get("url", ""),
                    path=result.get("url"),
                    details={
                        "status_code": status,
                        "words": result.get("words"),
                        "lines": result.get("lines"),
                        "content_length": result.get("length"),
                    },
                    remediation="Verify this path is intentionally exposed",
                )
                findings.append(finding)
        except json.JSONDecodeError:
            pass
        return findings

    @staticmethod
    def parse_trivy(json_output: str) -> List[Finding]:
        """Parse Trivy JSON output to findings."""
        findings = []
        try:
            data = json.loads(json_output)
            results = data.get("Results", [])

            for result in results:
                for vuln in result.get("Vulnerabilities", []) or []:
                    severity_str = vuln.get("Severity", "UNKNOWN").lower()
                    severity = VAPTOutputParser._map_severity(severity_str)

                    # Calculate CVSS from available data
                    cvss = None
                    if vuln.get("CVSS"):
                        for source, cvss_data in vuln.get("CVSS", {}).items():
                            if isinstance(cvss_data, dict):
                                cvss = cvss_data.get("V3Score") or cvss_data.get("V2Score")
                                break

                    finding = Finding(
                        id=uuid4(),
                        title=f"{vuln.get('PkgName', 'Unknown')} - {vuln.get('VulnerabilityID', 'Unknown')}",
                        description=vuln.get("Description", ""),
                        severity=severity,
                        cvss_score=cvss,
                        tool_name="trivy",
                        plugin_id="tools/trivy",
                        target=result.get("Target", ""),
                        details={
                            "package_name": vuln.get("PkgName"),
                            "installed_version": vuln.get("InstalledVersion"),
                            "fixed_version": vuln.get("FixedVersion"),
                            "layer": result.get("Layer"),
                        },
                        cve=vuln.get("VulnerabilityID"),
                        cwe=vuln.get("CWEIDs"),
                        remediation=vuln.get("Title"),
                        reference=vuln.get("References"),
                    )
                    findings.append(finding)
        except json.JSONDecodeError:
            pass
        return findings

    @staticmethod
    def parse_semgrep(json_output: str) -> List[Finding]:
        """Parse Semgrep JSON output to findings."""
        findings = []
        try:
            data = json.loads(json_output)
            results = data.get("results", [])

            for result in results:
                severity_str = result.get("severity", "INFO").lower()
                severity = VAPTOutputParser._map_severity(severity_str)

                extra = result.get("extra", {})
                metadata = extra.get("metadata", {})

                finding = Finding(
                    id=uuid4(),
                    title=result.get("check", result.get("title", "Semgrep Finding")),
                    description=extra.get("message", ""),
                    severity=severity,
                    tool_name="semgrep",
                    plugin_id="tools/semgrep",
                    target=f"{result.get('path')}:{result.get('start', {}).get('line')}",
                    details={
                        "file": result.get("path"),
                        "line": result.get("start", {}).get("line"),
                        "column": result.get("start", {}).get("col"),
                        "end_line": result.get("end", {}).get("line"),
                    },
                    remediation=extra.get("fix"),
                    reference=metadata.get("references"),
                )
                findings.append(finding)
        except json.JSONDecodeError:
            pass
        return findings

    @staticmethod
    def parse_sslscan(xml_output: str) -> List[Finding]:
        """Parse SSLyze XML output to findings."""
        findings = []
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(xml_output)

            for target in root.findall(".//target"):
                target_host = target.get("host", "")

                # Check for certificate issues
                for cert in target.findall(".//certificate"):
                    expiry = cert.find(".//validity")
                    if expiry is not None:
                        not_after = expiry.get("notAfter", "")
                        try:
                            exp_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                            if exp_date < datetime.now():
                                findings.append(Finding(
                                    title="SSL Certificate Expired",
                                    description=f"Certificate expired on {not_after}",
                                    severity=Severity.CRITICAL,
                                    tool_name="sslscan",
                                    plugin_id="tools/sslscan",
                                    target=target_host,
                                    remediation="Renew SSL certificate immediately",
                                ))
                        except ValueError:
                            pass

                # Check for weak ciphers
                for cipher in target.findall(".//cipher"):
                    cipher_name = cipher.get("cipher", "")
                    if any(weak in cipher_name.lower() for weak in ["exp", "rc4", "md5", "sha1"]):
                        findings.append(Finding(
                            title=f"Weak Cipher: {cipher_name}",
                            description="This cipher is considered weak and should be disabled",
                            severity=Severity.HIGH,
                            tool_name="sslscan",
                            plugin_id="tools/sslscan",
                            target=target_host,
                            details={"cipher": cipher_name},
                            remediation="Disable weak ciphers in SSL/TLS configuration",
                        ))
        except Exception:
            pass
        return findings

    @staticmethod
    def parse_default(text_output: str, tool_name: str = "unknown") -> List[Finding]:
        """Default text parser for tools without specific parsers."""
        findings = []
        # Generic pattern matching for common vulnerability indicators
        patterns = [
            (r"sql\s*injection", Severity.CRITICAL, "SQL Injection"),
            (r"xss|cross[- ]site", Severity.HIGH, "Cross-Site Scripting"),
            (r"remote\s*code\s*execution|rce", Severity.CRITICAL, "Remote Code Execution"),
            (r"path\s*traversal", Severity.HIGH, "Path Traversal"),
            (r"ssrf", Severity.HIGH, "Server-Side Request Forgery"),
            (r"csrf", Severity.MEDIUM, "CSRF"),
            (r"idor", Severity.MEDIUM, "Insecure Direct Object Reference"),
            (r"open\s*redirect", Severity.LOW, "Open Redirect"),
            (r"information\s*disclosure", Severity.INFO, "Information Disclosure"),
            (r"default\s*credential|weak\s*password", Severity.CRITICAL, "Default Credentials"),
        ]

        for line in text_output.splitlines():
            for pattern, severity, vuln_type in patterns:
                import re
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(Finding(
                        title=f"Potential {vuln_type}",
                        description=line.strip()[:500],
                        severity=severity,
                        tool_name=tool_name,
                        plugin_id=f"tools/{tool_name}",
                        target="",
                        details={"matched_line": line},
                        remediation=f"Investigate potential {vuln_type} vulnerability",
                    ))
                    break

        return findings


class VAPTExecutor:
    """
    Enterprise VAPT Execution Engine

    Features:
    - Multi-platform support (Kali, Dark-Moon, PentAGI)
    - Docker container isolation
    - Parallel tool execution
    - Intelligent output parsing
    - Async/await support
    """

    def __init__(self, config: PlatformConfig):
        self.config = config
        self._parsers = {
            "nmap": VAPTOutputParser.parse_nmap,
            "nikto": VAPTOutputParser.parse_nikto,
            "nuclei": VAPTOutputParser.parse_nuclei,
            "sqlmap": VAPTOutputParser.parse_sqlmap,
            "gobuster": VAPTOutputParser.parse_gobuster,
            "ffuf": VAPTOutputParser.parse_ffuf,
            "trivy": VAPTOutputParser.parse_trivy,
            "semgrep": VAPTOutputParser.parse_semgrep,
            "sslscan": VAPTOutputParser.parse_sslscan,
        }

    async def execute_tool(
        self,
        tool: ExternalTool,
        target: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ToolResult:
        """Execute a single tool and return parsed findings."""
        started_at = datetime.utcnow()
        tool_id = f"tools/{tool.name}"

        try:
            # Build command
            cmd = self._build_command(tool, target)

            # Execute based on platform
            if self.config.platform_type == PlatformType.KALI_DIRECT:
                stdout, stderr, return_code = await self._execute_in_container(cmd, tool)
            elif self.config.platform_type == PlatformType.DARK_MOON:
                stdout, stderr, return_code = await self._execute_dark_moon(tool, target, context)
            elif self.config.platform_type == PlatformType.PENTAGI:
                stdout, stderr, return_code = await self._execute_pentagi(tool, target, context)
            else:
                stdout, stderr, return_code = await self._execute_direct(cmd, tool)

            # Parse output
            findings = self._parse_output(stdout, tool)

            return ToolResult(
                tool_id=tool_id,
                tool_name=tool.name,
                success=return_code == 0 and len(findings) >= 0,
                duration=(datetime.utcnow() - started_at).total_seconds(),
                started_at=started_at,
                completed_at=datetime.utcnow(),
                stdout=stdout,
                stderr=stderr,
                return_code=return_code,
                findings=findings,
                errors=[stderr] if stderr else [],
            )

        except Exception as e:
            return ToolResult(
                tool_id=tool_id,
                tool_name=tool.name,
                success=False,
                duration=(datetime.utcnow() - started_at).total_seconds(),
                started_at=started_at,
                completed_at=datetime.utcnow(),
                findings=[],
                errors=[str(e)],
            )

    async def execute_tools_parallel(
        self,
        tools: List[ExternalTool],
        target: str,
        context: Optional[Dict[str, Any]] = None
    ) -> List[ToolResult]:
        """Execute multiple tools in parallel."""
        tasks = [self.execute_tool(tool, target, context) for tool in tools]
        return await asyncio.gather(*tasks)

    def _build_command(self, tool: ExternalTool, target: str) -> List[str]:
        """Build command list for tool execution."""
        cmd = [tool.command] + tool.args

        # Add target based on tool type
        if tool.name in ["nmap", "masscan", "netdiscover"]:
            cmd.append(target)
        elif tool.name in ["nikto", "sqlmap", "xsstrike", "nuclei", "gobuster", "ffuf"]:
            if tool.name == "nikto":
                cmd.extend(["-host", target])
            elif tool.name == "sqlmap":
                cmd.extend(["--url", target, "--batch"])
            elif tool.name == "nuclei":
                cmd.extend(["-u", target])
            elif tool.name == "gobuster":
                cmd.extend(["-u", target])
            elif tool.name == "ffuf":
                cmd.extend(["-u", target])
            else:
                cmd.append(target)
        elif tool.name == "trivy":
            cmd.extend(["image", "--severity", "CRITICAL,HIGH,MEDIUM", target])
        elif tool.name == "semgrep":
            cmd.extend(["--json", "--quiet", target])

        return cmd

    async def _execute_direct(
        self,
        cmd: List[str],
        tool: ExternalTool
    ) -> tuple:
        """Execute command directly on host."""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=tool.env_vars or None,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=tool.timeout
                )
                return (
                    stdout.decode("utf-8", errors="ignore"),
                    stderr.decode("utf-8", errors="ignore"),
                    process.returncode or 0
                )
            except asyncio.TimeoutError:
                process.kill()
                return "", f"Tool execution timed out after {tool.timeout}s", -1

        except FileNotFoundError:
            return "", f"Tool not found: {cmd[0]}", -1
        except Exception as e:
            return "", str(e), -1

    async def _execute_in_container(
        self,
        cmd: List[str],
        tool: ExternalTool
    ) -> tuple:
        """Execute command in isolated Docker container."""
        container_name = f"astraix-{tool.name}-{uuid4().hex[:8]}"

        docker_cmd = [
            "docker", "run",
            "--rm",
            "--name", container_name,
            "--network", self.config.docker_network,
            "--memory", "512m",
            "--cpus", "1",
            "-i",
            self.config.docker_image,
            "sh", "-c",
            " ".join(cmd)
        ]

        try:
            process = await asyncio.create_subprocess_exec(
                *docker_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=min(tool.timeout, self.config.container_timeout)
                )
                return (
                    stdout.decode("utf-8", errors="ignore"),
                    stderr.decode("utf-8", errors="ignore"),
                    process.returncode or 0
                )
            except asyncio.TimeoutError:
                # Kill container
                subprocess.run(["docker", "kill", container_name], capture_output=True)
                return "", f"Container execution timed out", -1

        except FileNotFoundError:
            # Docker not available, fall back to direct execution
            return await self._execute_direct(cmd, tool)
        except Exception as e:
            return "", str(e), -1

    async def _execute_dark_moon(
        self,
        tool: ExternalTool,
        target: str,
        context: Optional[Dict[str, Any]]
    ) -> tuple:
        """Execute via Dark-Moon AI platform."""
        # Dark-Moon uses MCP for tool execution
        # For now, use direct execution via Docker toolbox
        return await self._execute_in_container(
            self._build_command(tool, target),
            tool
        )

    async def _execute_pentagi(
        self,
        tool: ExternalTool,
        target: str,
        context: Optional[Dict[str, Any]]
    ) -> tuple:
        """Execute via PentAGI platform."""
        # PentAGI has its own agent system
        # For now, use direct execution
        return await self._execute_in_container(
            self._build_command(tool, target),
            tool
        )

    def _parse_output(self, output: str, tool: ExternalTool) -> List[Finding]:
        """Parse tool output using appropriate parser."""
        parser = self._parsers.get(tool.name, VAPTOutputParser.parse_default)
        return parser(output, tool.name)


# Predefined tool configurations for common VAPT tools
KALI_TOOLS = {
    "nmap": ExternalTool(
        name="nmap",
        command="nmap",
        args=["-sV", "-oX", "-"],  # XML output to stdout
        output_format="xml",
        parse_method="nmap",
        timeout=600,
        needs_root=True,
    ),
    "masscan": ExternalTool(
        name="masscan",
        command="masscan",
        args=["--rate", "10000", "-oJ", "-"],  # JSON output
        output_format="json",
        parse_method="masscan",
        timeout=300,
        needs_root=True,
    ),
    "nikto": ExternalTool(
        name="nikto",
        command="nikto",
        args=["-Format", "xml", "-output", "-"],
        output_format="xml",
        parse_method="nikto",
        timeout=600,
    ),
    "sqlmap": ExternalTool(
        name="sqlmap",
        command="sqlmap",
        args=["--batch", "--json-output", "--output-dir=/tmp"],
        output_format="json",
        parse_method="sqlmap",
        timeout=1800,
    ),
    "xsstrike": ExternalTool(
        name="xsstrike",
        command="xsstrike",
        args=["--json"],
        output_format="json",
        parse_method="xsstrike",
        timeout=600,
    ),
    "dalfox": ExternalTool(
        name="dalfox",
        command="dalfox",
        args=["--json", "output.json"],
        output_format="json",
        parse_method="dalfox",
        timeout=600,
    ),
    "nuclei": ExternalTool(
        name="nuclei",
        command="nuclei",
        args=["-json-export", "-", "-silent"],
        output_format="json",
        parse_method="nuclei",
        timeout=1800,
    ),
    "gobuster": ExternalTool(
        name="gobuster",
        command="gobuster",
        args=["dir", "-o", "-", "-f", "-j", "-q"],
        output_format="json",
        parse_method="gobuster",
        timeout=600,
    ),
    "ffuf": ExternalTool(
        name="ffuf",
        command="ffuf",
        args=["-json", "-u"],
        output_format="json",
        parse_method="ffuf",
        timeout=600,
    ),
    "dirb": ExternalTool(
        name="dirb",
        command="dirb",
        args=["-o", "-"],
        output_format="text",
        parse_method="default",
        timeout=600,
    ),
    "commix": ExternalTool(
        name="commix",
        command="commix",
        args=["--batch", "--output-dir=/tmp"],
        output_format="json",
        parse_method="commix",
        timeout=600,
    ),
    "sslscan": ExternalTool(
        name="sslscan",
        command="sslscan",
        args=["--xml=-"],
        output_format="xml",
        parse_method="sslscan",
        timeout=300,
    ),
    "testssl": ExternalTool(
        name="testssl",
        command="testssl",
        args=["--jsonfile=-", "--pretty"],
        output_format="json",
        parse_method="testssl",
        timeout=600,
    ),
    "trivy": ExternalTool(
        name="trivy",
        command="trivy",
        args=["--format", "json", "--security-checks", "vuln,config", "--quiet"],
        output_format="json",
        parse_method="trivy",
        timeout=600,
    ),
    "semgrep": ExternalTool(
        name="semgrep",
        command="semgrep",
        args=["--json", "--quiet"],
        output_format="json",
        parse_method="semgrep",
        timeout=600,
    ),
    "bandit": ExternalTool(
        name="bandit",
        command="bandit",
        args=["-f", "json", "-r"],
        output_format="json",
        parse_method="bandit",
        timeout=300,
    ),
    "dnsrecon": ExternalTool(
        name="dnsrecon",
        command="dnsrecon",
        args=["--json", "-z"],
        output_format="json",
        parse_method="dnsrecon",
        timeout=300,
    ),
    "theHarvester": ExternalTool(
        name="theHarvester",
        command="theHarvester",
        args=["-j", "-b", "all"],
        output_format="json",
        parse_method="theHarvester",
        timeout=300,
    ),
    "recon-ng": ExternalTool(
        name="recon-ng",
        command="recon-ng",
        args=["--no-check"],
        output_format="json",
        parse_method="recon-ng",
        timeout=600,
    ),
    "hydra": ExternalTool(
        name="hydra",
        command="hydra",
        args=["-V", "-f"],
        output_format="text",
        parse_method="default",
        timeout=3600,
        needs_root=True,
    ),
    "prowler": ExternalTool(
        name="prowler",
        command="prowler",
        args=["-F", "json", "-M", "json"],
        output_format="json",
        parse_method="prowler",
        timeout=1800,
    ),
    "scoutsuite": ExternalTool(
        name="scoutsuite",
        command="scout",
        args=["--json"],
        output_format="json",
        parse_method="scoutsuite",
        timeout=1800,
    ),
}


class ScanOrchestrator:
    """
    Orchestrates scans across multiple tools and platforms.

    Supports:
    - Sequential tool execution
    - Parallel tool execution
    - Platform-specific execution
    - Result aggregation
    """

    def __init__(self, config: PlatformConfig):
        self.executor = VAPTExecutor(config)
        self.config = config

    async def run_scan(self, scan_request: ScanRequest) -> ScanResult:
        """Execute a complete security scan."""
        started_at = datetime.utcnow()
        result = ScanResult(
            id=uuid4(),
            status=ScanStatus.RUNNING,
            target=scan_request.target,
            capability=scan_request.capability,
            started_at=started_at,
        )

        try:
            # Map capability to tools
            tools = self._get_tools_for_capability(scan_request.capability, scan_request.tools)

            if not tools:
                result.finalize(ScanStatus.FAILED, "No tools available for scan")
                return result

            # Execute tools
            if self.config.parallel_execution:
                tool_results = await self.executor.execute_tools_parallel(
                    tools,
                    scan_request.target,
                    {
                        "deep": scan_request.deep,
                        "aggressive": scan_request.aggressive,
                        "organization_id": str(scan_request.organization_id) if scan_request.organization_id else None,
                        "project_id": str(scan_request.project_id) if scan_request.project_id else None,
                    }
                )
            else:
                # Sequential execution
                tool_results = []
                for tool in tools:
                    tr = await self.executor.execute_tool(
                        tool,
                        scan_request.target,
                        {"deep": scan_request.deep}
                    )
                    tool_results.append(tr)

            # Aggregate results
            for tr in tool_results:
                result.add_tool_result(tr)

            # Determine final status
            if result.errors and not result.findings:
                result.finalize(ScanStatus.PARTIAL, "Some tools failed")
            else:
                result.finalize(ScanStatus.COMPLETED, f"Found {result.findings_count} findings")

        except Exception as e:
            result.errors.append(str(e))
            result.finalize(ScanStatus.FAILED, str(e))

        return result

    def _get_tools_for_capability(
        self,
        capability: ToolCapability,
        requested_tools: List[str]
    ) -> List[ExternalTool]:
        """Get tools for a given capability."""
        tools = []

        # Add explicitly requested tools
        for tool_id in requested_tools:
            if tool_id in KALI_TOOLS:
                tools.append(KALI_TOOLS[tool_id])

        # If no tools specified, add defaults for capability
        if not tools:
            defaults = {
                ToolCapability.NETWORK_VAPT: ["nmap", "masscan", "dnsrecon"],
                ToolCapability.WEB_VAPT: ["nikto", "sqlmap", "nuclei", "gobuster"],
                ToolCapability.CLOUD_SECURITY: ["prowler", "scoutsuite"],
                ToolCapability.CODE_AUDIT: ["semgrep", "bandit"],
                ToolCapability.CONTAINER_SECURITY: ["trivy"],
                ToolCapability.SSL_SECURITY: ["sslscan", "testssl"],
            }
            tool_ids = defaults.get(capability, [])
            for tool_id in tool_ids:
                if tool_id in KALI_TOOLS:
                    tools.append(KALI_TOOLS[tool_id])

        return tools


def create_kali_executor() -> VAPTExecutor:
    """Create executor for direct Kali Linux tool execution."""
    config = PlatformConfig(
        platform_type=PlatformType.KALI_DIRECT,
        name="Kali Linux",
        docker_image="kalilinux/kali-rolling:latest",
        parallel_execution=True,
        max_concurrent_tools=5,
    )
    return VAPTExecutor(config)


def create_dark_moon_executor(base_url: str, api_key: str) -> VAPTExecutor:
    """Create executor for Dark-Moon AI platform."""
    config = PlatformConfig(
        platform_type=PlatformType.DARK_MOON,
        name="Dark-Moon",
        base_url=base_url,
        api_key=api_key,
        use_ai_orchestration=True,
        timeout=7200,  # 2 hours for AI-powered scans
    )
    return VAPTExecutor(config)


def create_pentagi_executor(base_url: str, api_key: str) -> VAPTExecutor:
    """Create executor for PentAGI platform."""
    config = PlatformConfig(
        platform_type=PlatformType.PENTAGI,
        name="PentAGI",
        base_url=base_url,
        api_key=api_key,
        use_ai_orchestration=True,
        timeout=7200,
    )
    return VAPTExecutor(config)


def create_lyrie_executor(base_url: str = "http://localhost:8080", api_key: str = "") -> VAPTExecutor:
    """
    Create executor for Lyrie AI platform.

    Lyrie is an autonomous security agent with:
    - 7-phase autonomous pentesting (recon → exploit → report)
    - Agent Trust Protocol (ATP) for AI agent identity
    - AI red-teaming for LLM endpoints
    - SMT-based exploit feasibility analysis
    - CVSS v3.1 scoring

    Installation: pip install lyrie-omega
    Commands: lyrie hack <target>, lyrie scan <url>, lyrie redteam <endpoint>

    Args:
        base_url: Lyrie API endpoint (for remote execution)
        api_key: Lyrie API key

    Returns:
        VAPTExecutor configured for Lyrie
    """
    config = PlatformConfig(
        platform_type=PlatformType.LYRIE,
        name="Lyrie AI",
        base_url=base_url,
        api_key=api_key,
        use_ai_orchestration=True,
        timeout=7200,  # Lyrie can take up to 2 hours for full pentest
    )
    return VAPTExecutor(config)


class LyrieAIAgent:
    """
    Lyrie AI Agent executor for autonomous security operations.

    Features:
    - 7-phase pentesting: recon → fingerprint → scan → exploit → PoC → report
    - ATP (Agent Trust Protocol) support
    - CVSS v3.1 vector parsing and scoring
    - SMT solver integration
    - AI red-teaming

    Example:
        agent = LyrieAIAgent()
        result = await agent.hack("https://example.com")
        result = await agent.scan("https://example.com")
        result = await agent.redteam("https://api.openai.com/v1/chat")
        cvss_score = await agent.cvss("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
    """

    def __init__(self, lyrie_path: str = "lyrie"):
        self.lyrie_path = lyrie_path
        self._atp_enabled = True

    async def hack(self, target: str, stage: str = None, output: str = None, **kwargs) -> dict:
        """
        Run 7-phase autonomous pentest.

        Args:
            target: URL or local path to pentest
            stage: Specific stage (scan, exploit, etc.)
            output: Output file path (JSON, SARIF)
            **kwargs: Additional lyrie hack options

        Returns:
            dict with pentest results and findings
        """
        cmd = [self.lyrie_path, "hack", target]

        if stage:
            cmd.extend(["--stage", stage])
        if output:
            cmd.extend(["--output", output])

        for key, value in kwargs.items():
            cmd.extend([f"--{key}", str(value)])

        return await self._run_command(cmd)

    async def scan(self, target: str, **kwargs) -> dict:
        """
        Scan URL or file for security issues.

        Checks:
        - Security headers (CSP, HSTS, X-Frame-Options)
        - TLS version and cert expiry
        - Common exposed paths (.env, .git/config)
        - Server version disclosure

        Returns:
            dict with scan results
        """
        cmd = [self.lyrie_path, "scan", target]

        for key, value in kwargs.items():
            cmd.extend([f"--{key}", str(value)])

        return await self._run_command(cmd)

    async def redteam(self, endpoint: str, strategy: str = "crescendo", **kwargs) -> dict:
        """
        AI red-team an LLM endpoint.

        Strategies:
        - crescendo: gradual escalation
        - tap: tree-of-attacks-with-pruning
        - pair: prompt automatic iterative refinement
        - gcg: gradient-based suffix attack (H200 required)
        - autodan: genetic algorithm black-box (GPU required)

        Returns:
            dict with red-team results
        """
        cmd = [self.lyrie_path, "redteam", endpoint, "--strategy", strategy]

        for key, value in kwargs.items():
            cmd.extend([f"--{key}", str(value)])

        return await self._run_command(cmd)

    async def cvss(self, vector: str) -> dict:
        """
        Calculate CVSS v3.1 score from vector.

        Args:
            vector: CVSS vector string (e.g., "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")

        Returns:
            dict with CVSS score and severity
        """
        cmd = [self.lyrie_path, "cvss", vector]
        result = await self._run_command(cmd)

        # Parse CVSS output
        if "result" in result:
            # Extract score from output
            output = result.get("stdout", "")
            # Lyrie outputs formatted CVSS results
            return {
                "vector": vector,
                "score": self._extract_cvss_score(output),
                "severity": self._extract_severity(output),
                "output": output,
            }
        return result

    async def atp_verify(self, agent_id: str) -> dict:
        """
        Verify agent identity using Agent Trust Protocol.

        Args:
            agent_id: Agent identifier to verify

        Returns:
            dict with verification result and certificate details
        """
        cmd = [self.lyrie_path, "atp", "verify", agent_id]
        return await self._run_command(cmd)

    async def atp_badge(self) -> dict:
        """
        Display ATP compliance badge.

        Returns:
            dict with badge information
        """
        cmd = [self.lyrie_path, "atp", "badge", "--show"]
        return await self._run_command(cmd)

    async def doctor(self) -> dict:
        """
        Run self-diagnostic to verify Lyrie installation.

        Checks:
        - Environment setup
        - Dependencies
        - API keys
        - Network connectivity

        Returns:
            dict with health check results
        """
        cmd = [self.lyrie_path, "doctor"]
        return await self._run_command(cmd)

    async def _run_command(self, cmd: List[str]) -> dict:
        """Execute lyrie command and return parsed output."""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=3600  # 1 hour timeout
            )

            return {
                "success": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": stdout.decode("utf-8", errors="ignore"),
                "stderr": stderr.decode("utf-8", errors="ignore"),
            }

        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "Command timed out",
                "returncode": -1,
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"Lyrie not found at {self.lyrie_path}. Install with: pip install lyrie-omega",
                "returncode": -1,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "returncode": -1,
            }

    def _extract_cvss_score(self, output: str) -> float:
        """Extract CVSS score from lyrie output."""
        import re
        match = re.search(r"([0-9.]+)/10", output)
        if match:
            return float(match.group(1))
        return 0.0

    def _extract_severity(self, output: str) -> str:
        """Extract severity from lyrie output."""
        output_lower = output.lower()
        if "critical" in output_lower:
            return "critical"
        elif "high" in output_lower:
            return "high"
        elif "medium" in output_lower:
            return "medium"
        elif "low" in output_lower:
            return "low"
        return "info"

    def parse_hack_output(self, output: str) -> List[Finding]:
        """
        Parse lyrie hack output to findings.

        Lyrie outputs JSON or SARIF format.

        Returns:
            List of Finding objects
        """
        findings = []

        try:
            # Try JSON parsing
            data = json.loads(output)

            # Handle different output formats
            if isinstance(data, dict):
                if "findings" in data:
                    findings_data = data["findings"]
                elif "vulnerabilities" in data:
                    findings_data = data["vulnerabilities"]
                elif "results" in data:
                    findings_data = data["results"]
                else:
                    findings_data = [data]
            elif isinstance(data, list):
                findings_data = data
            else:
                return findings

            for item in findings_data:
                severity_str = item.get("severity", "medium").lower()
                severity = self._map_severity(severity_str)

                finding = Finding(
                    title=item.get("title", item.get("name", "Lyrie Finding")),
                    description=item.get("description", item.get("message", "")),
                    severity=severity,
                    cvss_score=item.get("cvss_score") or item.get("cvss"),
                    tool_name="lyrie",
                    plugin_id="lyrie/hack",
                    target=item.get("target", item.get("url", "")),
                    details=item,
                    remediation=item.get("remediation") or item.get("solution"),
                    reference=item.get("reference") or item.get("references"),
                )
                findings.append(finding)

        except json.JSONDecodeError:
            # Try SARIF parsing
            findings.extend(self._parse_sarif(output))

        return findings

    def _parse_sarif(self, sarif_output: str) -> List[Finding]:
        """Parse SARIF format output from lyrie."""
        findings = []

        try:
            data = json.loads(sarif_output)
            runs = data.get("runs", [])

            for run in runs:
                results = run.get("results", [])
                for result in results:
                    rule_id = result.get("ruleId", "")
                    level = result.get("level", "warning")

                    severity_map = {
                        "error": Severity.HIGH,
                        "warning": Severity.MEDIUM,
                        "note": Severity.LOW,
                    }

                    message = result.get("message", {}).get("text", "")
                    locations = result.get("locations", [])

                    target = ""
                    if locations:
                        loc = locations[0]
                        target = loc.get("physicalLocation", {}).get(
                            "artifactLocation", {}
                        ).get("uri", "")

                    finding = Finding(
                        title=f"[SARIF] {rule_id}",
                        description=message,
                        severity=severity_map.get(level, Severity.MEDIUM),
                        tool_name="lyrie",
                        plugin_id="lyrie/sarif",
                        target=target,
                        details={"rule_id": rule_id, "result": result},
                        remediation="Review and remediate according to SARIF rule",
                    )
                    findings.append(finding)

        except (json.JSONDecodeError, Exception):
            pass

        return findings

    def _map_severity(self, severity_str: str) -> Severity:
        """Map lyrie severity string to Severity enum."""
        severity_map = {
            "critical": Severity.CRITICAL,
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
            "info": Severity.INFO,
            "informational": Severity.INFO,
        }
        return severity_map.get(severity_str, Severity.MEDIUM)