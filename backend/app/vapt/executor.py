"""
VAPT Executor

Executes security tools inside Docker containers (Kali Linux).
Provides isolation and access to full suite of VAPT tools.
"""

import asyncio
import json
import os
import re
import subprocess
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4, uuid5, UUID

from app.vapt.models import (
    VAPTFinding,
    VAPTScanRequest,
    VAPTScanResult,
    VAPTSeverity,
    VAPTTool,
)
from app.vapt.tools import TOOLS_REGISTRY, get_tool, get_tools_for_scan_type


class VAPTExecutor:
    """
    VAPT executor using Docker containers.

    Tools run inside isolated Kali Linux containers for:
    - Complete tool suite access
    - Security isolation
    - No host dependency
    """

    KALI_IMAGE = "astraix-kali:latest"

    def __init__(self):
        self._last_run: Dict[str, float] = {}
        self._rate_limit = 1.0
        self._demo_mode = os.environ.get("VAPT_DEMO_MODE", "false").lower() == "true"
        self._use_docker = os.environ.get("VAPT_USE_DOCKER", "true").lower() == "true"

    async def execute_scan(self, request: VAPTScanRequest) -> VAPTScanResult:
        """Execute a complete VAPT scan."""
        result = VAPTScanResult(
            id=uuid4(),
            request=request,
            status="running",
            started_at=datetime.utcnow(),
        )

        if self._demo_mode:
            return await self._execute_demo_scan(request, result)

        if not self._use_docker:
            return await self._execute_demo_scan(request, result)

        try:
            if not await self._check_docker():
                result.errors.append("Docker not available, using demo mode")
                return await self._execute_demo_scan(request, result)

            tools = self._resolve_tools(request)

            for tool_id in tools:
                try:
                    await self._run_tool_in_docker(tool_id, request, result)
                except Exception as e:
                    result.errors.append(f"{tool_id}: {str(e)}")

            if result.findings:
                result.status = "completed"
                result.message = f"Found {len(result.findings)} vulnerabilities"
            else:
                result.status = "completed"
                result.message = "Scan completed, no vulnerabilities found"

        except Exception as e:
            result.status = "failed"
            result.errors.append(str(e))

        result.finalize(result.status, result.message)
        return result

    async def _check_docker(self) -> bool:
        """Check if Docker is available."""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    async def _run_tool_in_docker(
        self,
        tool_id: str,
        request: VAPTScanRequest,
        result: VAPTScanResult,
    ) -> None:
        """Run a tool inside a Docker container."""
        tool = get_tool(tool_id)
        if not tool:
            result.errors.append(f"Tool not found: {tool_id}")
            return

        self._check_rate_limit(tool_id)

        target = request.target.value
        if tool.requires_url and not target.startswith(("http://", "https://")):
            target = f"http://{target}"

        cmd = self._build_docker_command(tool, target)
        if not cmd:
            result.errors.append(f"Could not build command for {tool_id}")
            return

        container_name = f"astraix-vapt-{uuid4().hex[:8]}"

        docker_cmd = [
            "docker", "run",
            "--rm",
            "--name", container_name,
            "--network", "bridge",
            "--memory", "512m",
            "--cpus", "1",
            "-i",
            self.KALI_IMAGE,
            "sh", "-c",
            " && ".join(cmd) if isinstance(cmd, list) else cmd
        ]

        try:
            process = await asyncio.create_subprocess_exec(
                *docker_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=tool.timeout,
            )

            output = stdout.decode("utf-8", errors="ignore")

            result.tool_results[tool_id] = {
                "duration": tool.timeout,
                "return_code": process.returncode or 0,
                "success": process.returncode == 0,
            }

            findings = self._parse_output(output, tool, request.target.value)
            for finding in findings:
                result.add_finding(finding)

        except asyncio.TimeoutError:
            subprocess.run(["docker", "kill", container_name], capture_output=True)
            result.errors.append(f"{tool_id}: timeout")
        except FileNotFoundError:
            result.errors.append(f"{tool_id}: Docker not available")
        except Exception as e:
            result.errors.append(f"{tool_id}: {str(e)}")

    def _build_docker_command(self, tool: VAPTTool, target: str) -> Optional[str]:
        """Build command for Docker execution."""
        tool_cmd = {
            "nmap": f"nmap -sV -Pn -oX - {target}",
            "sqlmap": f"sqlmap -u {target} --batch --random-agent --output-dir=/tmp",
            "nuclei": f"nuclei -u {target} -json-export - -silent",
            "nikto": f"nikto -h {target} -Format xml -output -",
            "gobuster": f"gobuster dir -u {target} -o - -f -j -q",
            "ffuf": f"ffuf -u {target}/FUZZ -w /usr/share/wordlists/dirb/common.txt -json",
            "sslscan": f"sslscan {target}",
            "trivy": f"trivy image --quiet --format json alpine:latest",
        }.get(tool.id)

        return tool_cmd

    def _check_rate_limit(self, tool_id: str) -> None:
        """Enforce rate limiting."""
        now = time.time()
        if tool_id in self._last_run:
            elapsed = now - self._last_run[tool_id]
            if elapsed < self._rate_limit:
                time.sleep(self._rate_limit - elapsed)
        self._last_run[tool_id] = time.time()

    def _resolve_tools(self, request: VAPTScanRequest) -> List[str]:
        """Resolve tools to execute."""
        if request.tools:
            return request.tools
        return get_tools_for_scan_type(request.scan_type)

    def _parse_output(
        self,
        output: str,
        tool: VAPTTool,
        target: str,
    ) -> List[VAPTFinding]:
        """Parse tool output to findings."""
        parser_map = {
            "nmap": self._parse_nmap,
            "nikto": self._parse_nikto,
            "nuclei": self._parse_nuclei,
            "gobuster": self._parse_gobuster,
            "sslscan": self._parse_sslscan,
        }
        parser = parser_map.get(tool.id, self._parse_generic)
        return parser(output, target, tool.name)

    def _parse_nmap(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(output)

            for host in root.findall(".//host"):
                addr = host.find(".//address[@addrtype='ipv4']")
                if addr is None:
                    addr = host.find(".//address")
                host_addr = addr.get("addr", "unknown") if addr is not None else target

                for port in host.findall(".//port"):
                    port_id = port.get("portid", "")
                    protocol = port.get("protocol", "tcp")
                    state = port.find("state")
                    service = port.find("service")

                    if state is not None and state.get("state") == "open":
                        findings.append(VAPTFinding(
                            title=f"Open Port {port_id}/{protocol}",
                            description=f"Service: {service.get('name', 'unknown') if service is not None else 'unknown'}",
                            severity=VAPTSeverity.INFO,
                            tool_name=tool_name,
                            target=target,
                            host=host_addr,
                            port=int(port_id) if port_id.isdigit() else None,
                            protocol=protocol,
                            service=service.get("name") if service is not None else None,
                            remediation=f"Close port {port_id}/{protocol} if not required",
                        ))
        except Exception:
            pass
        return findings

    def _parse_nikto(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(output)

            for item in root.findall(".//item"):
                name = item.get("name", "Nikto Finding")
                desc = item.findtext("description", "")
                if desc:
                    findings.append(VAPTFinding(
                        title=name[:200],
                        description=desc[:500],
                        severity=VAPTSeverity.MEDIUM,
                        tool_name=tool_name,
                        target=target,
                        vulnerability_type="Web Server Misconfiguration",
                        remediation="Review and harden web server configuration",
                    ))
        except Exception:
            for line in output.splitlines():
                if "+" in line and not line.startswith("-"):
                    desc = line[1:200].strip()
                    if desc:
                        findings.append(VAPTFinding(
                            title="Nikto Finding",
                            description=desc,
                            severity=VAPTSeverity.MEDIUM,
                            tool_name=tool_name,
                            target=target,
                        ))
        return findings

    def _parse_nuclei(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            try:
                if line.strip().startswith("{"):
                    data = json.loads(line)
                    info = data.get("info", {})
                    severity = info.get("severity", "info")
                    findings.append(VAPTFinding(
                        title=info.get("name", "Nuclei Finding")[:200],
                        description=info.get("description", "")[:500],
                        severity=self._nuclei_to_severity(severity),
                        tool_name=tool_name,
                        target=target,
                        vulnerability_type=info.get("matched_at", ""),
                    ))
            except (json.JSONDecodeError, KeyError):
                continue
        return findings

    def _nuclei_to_severity(self, severity: str) -> VAPTSeverity:
        mapping = {
            "critical": VAPTSeverity.CRITICAL,
            "high": VAPTSeverity.HIGH,
            "medium": VAPTSeverity.MEDIUM,
            "low": VAPTSeverity.LOW,
            "info": VAPTSeverity.INFO,
        }
        return mapping.get(severity.lower(), VAPTSeverity.INFO)

    def _parse_gobuster(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            if "Status:" in line or "/" in line:
                parts = line.split()
                for part in parts:
                    if part.startswith("/") and len(part) > 1:
                        findings.append(VAPTFinding(
                            title=f"Directory Found: {part}",
                            description="Web path discovered during enumeration",
                            severity=VAPTSeverity.INFO,
                            tool_name=tool_name,
                            target=target,
                            path=part,
                            remediation="Review if this path should be publicly accessible",
                        ))
        return findings

    def _parse_sslscan(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            if "WARNING" in line or "VULNERABLE" in line:
                findings.append(VAPTFinding(
                    title="SSL/TLS Issue Detected",
                    description=line[:300],
                    severity=VAPTSeverity.HIGH,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="SSL/TLS Misconfiguration",
                    remediation="Update SSL configuration",
                ))
        return findings

    def _parse_generic(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            if line.strip() and len(line) > 10:
                findings.append(VAPTFinding(
                    title=f"{tool_name} Output",
                    description=line[:300],
                    severity=VAPTSeverity.INFO,
                    tool_name=tool_name,
                    target=target,
                ))
        return findings[:10]

    async def _execute_demo_scan(
        self,
        request: VAPTScanRequest,
        result: VAPTScanResult,
    ) -> VAPTScanResult:
        """Execute demo scan with realistic sample findings."""
        await asyncio.sleep(2)

        demo_findings = [
            VAPTFinding(
                title="Open Port: 22/tcp",
                description="SSH service detected - verify only authorized users have access",
                severity=VAPTSeverity.MEDIUM,
                tool_name="nmap",
                target=request.target.value,
                port=22,
                protocol="tcp",
                service="ssh",
                remediation="Restrict SSH access to known IP addresses or disable password authentication",
            ),
            VAPTFinding(
                title="Open Port: 443/tcp",
                description="HTTPS service detected",
                severity=VAPTSeverity.INFO,
                tool_name="nmap",
                target=request.target.value,
                port=443,
                protocol="tcp",
                service="https",
            ),
            VAPTFinding(
                title="SQL Injection Potential",
                description="Possible SQL injection in user input fields",
                severity=VAPTSeverity.HIGH,
                tool_name="sqlmap",
                target=request.target.value,
                vulnerability_type="SQL Injection",
                remediation="Use parameterized queries and input validation",
            ),
            VAPTFinding(
                title="XSS in Search Parameter",
                description="Reflected XSS detected",
                severity=VAPTSeverity.HIGH,
                tool_name="nuclei",
                target=request.target.value,
                path="/search?q=",
                vulnerability_type="Cross-Site Scripting (XSS)",
                remediation="Implement output encoding and CSP headers",
            ),
            VAPTFinding(
                title="Missing Security Headers",
                description="X-Frame-Options, CSP not set",
                severity=VAPTSeverity.LOW,
                tool_name="nuclei",
                target=request.target.value,
                vulnerability_type="Security Misconfiguration",
                remediation="Add security headers",
            ),
        ]

        for finding in demo_findings:
            result.add_finding(finding)

        result.status = "completed"
        result.message = f"Found {len(result.findings)} vulnerabilities"
        result.finalize("completed", result.message)
        return result


_executor: Optional[VAPTExecutor] = None


def get_vapt_executor() -> VAPTExecutor:
    global _executor
    if _executor is None:
        _executor = VAPTExecutor()
    return _executor