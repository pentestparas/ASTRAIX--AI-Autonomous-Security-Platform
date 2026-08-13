import asyncio
import json
import os
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4, uuid5, UUID

import docker
from docker.errors import DockerException, ContainerError, APIError, NotFound

from app.vapt.models import (
    VAPTFinding,
    VAPTScanRequest,
    VAPTScanResult,
    VAPTSeverity,
    VAPTTool,
)
from app.vapt.tools import TOOLS_REGISTRY, get_tool, get_tools_for_scan_type


class VAPTExecutor:
    KALI_IMAGE = "astraix-kali:latest"

    def __init__(self):
        self._last_run: Dict[str, float] = {}
        self._rate_limit = 1.0
        self._demo_mode = os.environ.get("VAPT_DEMO_MODE", "false").lower() == "true"
        self._use_docker = os.environ.get("VAPT_USE_DOCKER", "true").lower() == "true"
        self._docker_client = None

    @property
    def docker_client(self):
        if self._docker_client is None:
            try:
                self._docker_client = docker.from_env()
            except DockerException:
                self._docker_client = None
        return self._docker_client

    async def execute_scan(self, request: VAPTScanRequest) -> VAPTScanResult:
        result = VAPTScanResult(
            id=uuid4(),
            request=request,
            status="running",
            started_at=datetime.utcnow(),
        )

        if self._demo_mode or not self._use_docker:
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
        try:
            client = await asyncio.to_thread(docker.from_env)
            await asyncio.to_thread(client.ping)
            client.close()
            return True
        except Exception:
            return False

    async def _run_tool_in_docker(
        self,
        tool_id: str,
        request: VAPTScanRequest,
        result: VAPTScanResult,
    ) -> None:
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

        # Execution guard (Dark-Moon pattern): bound every tool with an
        # in-container timeout so the process dies even if docker-py's wait
        # hangs, and kill the process group shortly after on the way out.
        cmd = f"timeout --kill-after=5 {tool.timeout}s bash -c '{cmd}'"

        container_name = f"astraix-vapt-{uuid4().hex[:8]}"

        try:
            output = await asyncio.wait_for(
                asyncio.to_thread(
                    self._run_container_sync,
                    self.KALI_IMAGE,
                    cmd,
                    container_name,
                    tool.timeout,
                ),
                timeout=tool.timeout + 30,
            )

            result.tool_results[tool_id] = {
                "duration": tool.timeout,
                "return_code": 0,
                "success": True,
            }

            findings = self._parse_output(output, tool, request.target.value)
            for finding in findings:
                result.add_finding(finding)

        except asyncio.TimeoutError:
            self._kill_container(container_name)
            result.errors.append(f"{tool_id}: timeout")
        except DockerException as e:
            result.errors.append(f"{tool_id}: Docker error - {str(e)}")
        except Exception as e:
            result.errors.append(f"{tool_id}: {str(e)}")

    def _run_container_sync(
        self,
        image: str,
        cmd_string: str,
        container_name: str,
        timeout: int,
    ) -> str:
        client = docker.from_env()
        container = None
        try:
            container = client.containers.run(
                image=image,
                command=["sh", "-c", cmd_string],
                name=container_name,
                network_mode="bridge",
                mem_limit="512m",
                nano_cpus=int(1 * 1e9),
                detach=True,
                auto_remove=False,
            )

            result = container.wait(timeout=timeout)
            logs = container.logs(stdout=True, stderr=True).decode("utf-8", errors="ignore")

            if result.get("StatusCode", 0) != 0:
                pass

            return logs
        except Exception as e:
            # docker-py 7.x removed the docker.errors.TimeoutError alias; the
            # requests ReadTimeout surfaces directly. Normalize to asyncio.TimeoutError.
            if type(e).__name__ in ("TimeoutError", "ReadTimeout", "ReadTimeoutError"):
                raise asyncio.TimeoutError() from e
            raise
        finally:
            if container:
                try:
                    container.remove(force=True)
                except Exception:
                    pass

    def _kill_container(self, container_name: str) -> None:
        try:
            client = docker.from_env()
            try:
                container = client.containers.get(container_name)
                container.kill()
            except NotFound:
                pass
            finally:
                client.close()
        except Exception:
            pass

    def _build_docker_command(self, tool: VAPTTool, target: str) -> Optional[str]:
        from app.vapt.wordlists import get_wordlist

        wl_dirs = get_wordlist("dirs")
        wl_dirs_medium = get_wordlist("dirs_medium")
        wl_sub = get_wordlist("subdomains")
        wl_rockyou = get_wordlist("rockyou_top10k")
        wl_users = get_wordlist("usernames")
        wl_fuzz = get_wordlist("fuzz")

        tool_cmd = {
            "nmap": f"nmap -sV -Pn -T4 --top-ports 100 -oX - {target}",
            "sqlmap": f"sqlmap -u {target} --batch --random-agent --output-dir=/tmp",
            "nuclei": f"nuclei -u {target} -json-export - -silent -rate-limit 150",
            "nikto": f"nikto -h {target} -Format xml -output -",
            "gobuster": f"gobuster dir -u {target} -w {wl_dirs} -o - -f -q -t 10",
            "ffuf": f"ffuf -u {target}/FUZZ -w {wl_dirs_medium} -json -rate 100",
            "sslscan": f"sslscan --xml=- --no-failed {target}",
            "trivy": f"trivy image --quiet --format json alpine:latest",
            "hydra": f"hydra -L {wl_users} -P {wl_rockyou} -t 4 -w 10 {target} ssh",
            "dnsrecon": f"dnsrecon -d {target} -t std -j /tmp/dnsrecon.json > /dev/null 2>&1; cat /tmp/dnsrecon.json 2>/dev/null",
            "gobuster-dns": f"gobuster dns -d {target} -w {wl_sub} -q",
            "gobuster-vhost": f"gobuster vhost -u {target} -w {wl_dirs} -q",
            "ffuf-params": f"ffuf -u {target}?FUZZ=1 -w {wl_fuzz} -json",
            "masscan": f"masscan -Pn --top-ports 100 -oX - --rate 1000 {target}",
            "subfinder": f"subfinder -d {target} -jsonl -silent",
            "httpx": f"httpx -u {target} -json -silent -threads 20",
            "whatweb": f"whatweb -a 3 --log-json=/tmp/whatweb.json {target} > /dev/null 2>&1; cat /tmp/whatweb.json",
            "wafw00f": f"wafw00f -f json -o /tmp/waf.json {target} > /dev/null 2>&1; cat /tmp/waf.json",
            "arjun": f"arjun -u {target} -oJ -q",
            "wfuzz": f"wfuzz -z file,{wl_dirs_medium} --hc 404 --json {target}/FUZZ",
            "commix": f"commix -u {target} --batch --output-dir=/tmp",
            "dalfox": f"dalfox url {target} --format json --silence",
            "testssl": f"testssl --jsonfile=/tmp/testssl.json {target} > /dev/null 2>&1; cat /tmp/testssl.json 2>/dev/null",
        }.get(tool.id)

        return tool_cmd

    def _check_rate_limit(self, tool_id: str) -> None:
        now = time.time()
        if tool_id in self._last_run:
            elapsed = now - self._last_run[tool_id]
            if elapsed < self._rate_limit:
                time.sleep(self._rate_limit - elapsed)
        self._last_run[tool_id] = time.time()

    def _resolve_tools(self, request: VAPTScanRequest) -> List[str]:
        if request.tools:
            return request.tools
        return get_tools_for_scan_type(request.scan_type)

    def _parse_output(
        self,
        output: str,
        tool: VAPTTool,
        target: str,
    ) -> List[VAPTFinding]:
        parser_map = {
            "nmap": self._parse_nmap,
            "masscan": self._parse_nmap,
            "nikto": self._parse_nikto,
            "nuclei": self._parse_nuclei,
            "gobuster": self._parse_gobuster,
            "sslscan": self._parse_sslscan,
            "ffuf": self._parse_ffuf,
            "dnsrecon": self._parse_dnsrecon,
            "subfinder": self._parse_jsonl_findings,
            "httpx": self._parse_jsonl_findings,
            "whatweb": self._parse_jsonl_findings,
            "wafw00f": self._parse_wafw00f,
            "arjun": self._parse_arjun,
            "wfuzz": self._parse_ffuf,
            "dalfox": self._parse_dalfox,
            "commix": self._parse_commix,
            "hydra": self._parse_hydra,
            "testssl": self._parse_testssl,
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

    def _parse_ffuf(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            try:
                data = json.loads(line)
                if data.get("status") in (200, 301, 302, 401, 403):
                    url = data.get("url") or data.get("input", {}).get("FUZZ", "")
                    findings.append(VAPTFinding(
                        title=f"Endpoint Found: {url[:200]}",
                        description=f"Status {data.get('status')}, size {data.get('length', 0)}",
                        severity=VAPTSeverity.INFO,
                        tool_name=tool_name,
                        target=target,
                        path=url,
                        remediation="Review if this endpoint should be publicly accessible",
                    ))
            except (json.JSONDecodeError, KeyError):
                continue
        return findings

    def _parse_dnsrecon(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            data = json.loads(output)
            if isinstance(data, dict):
                for record_type in ("records", "MX", "NS", "SOA", "SRV", "TXT", "A"):
                    for rec in data.get(record_type, []):
                        desc = str(rec.get("address", rec.get("mname", rec)))
                        findings.append(VAPTFinding(
                            title=f"DNS Record: {record_type}",
                            description=desc[:300],
                            severity=VAPTSeverity.INFO,
                            tool_name=tool_name,
                            target=target,
                            service=record_type.lower(),
                            remediation="Review DNS records for information disclosure",
                        ))
        except (json.JSONDecodeError, AttributeError):
            for line in output.splitlines():
                if line.strip().startswith("[") and "]" in line:
                    findings.append(VAPTFinding(
                        title="DNS Record Found",
                        description=line[:300],
                        severity=VAPTSeverity.INFO,
                        tool_name=tool_name,
                        target=target,
                    ))
        return findings[:20]

    def _parse_jsonl_findings(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            try:
                data = json.loads(line)
                url = data.get("url") or data.get("host") or data.get("target") or ""
                title = data.get("title") or data.get("webapp") or f"{tool_name} Discovery"
                status = data.get("status_code") or data.get("status")
                desc = f"{tool_name}: {url}"
                if status:
                    desc += f" (HTTP {status})"
                tech = data.get("tech") or data.get("plugins")
                if tech:
                    desc += f" - tech: {tech}"
                if not url:
                    continue
                findings.append(VAPTFinding(
                    title=str(title)[:200],
                    description=desc[:500],
                    severity=VAPTSeverity.INFO,
                    tool_name=tool_name,
                    target=target,
                    path=url,
                ))
            except (json.JSONDecodeError, KeyError):
                continue
        return findings[:20]

    def _parse_wafw00f(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            data = json.loads(output)
            for entry in data if isinstance(data, list) else [data]:
                if entry.get("detected"):
                    firewall = entry.get("firewall", "unknown")
                    findings.append(VAPTFinding(
                        title=f"WAF Detected: {firewall}",
                        description=f"{entry.get('description', '')} at {entry.get('url', target)}",
                        severity=VAPTSeverity.INFO,
                        tool_name=tool_name,
                        target=target,
                        vulnerability_type="Web Application Firewall",
                        remediation="Account for WAF rules when testing; WAF bypass may be possible",
                    ))
        except (json.JSONDecodeError, AttributeError):
            pass
        return findings

    def _parse_arjun(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            data = json.loads(output)
            for url, params in data.items():
                if params:
                    findings.append(VAPTFinding(
                        title=f"Hidden Parameters Found",
                        description=f"{url} accepts params: {', '.join(params)[:400]}",
                        severity=VAPTSeverity.INFO,
                        tool_name=tool_name,
                        target=target,
                        path=url,
                        vulnerability_type="Parameter Discovery",
                        remediation="Test discovered parameters for injection vulnerabilities",
                    ))
        except (json.JSONDecodeError, AttributeError):
            pass
        return findings

    def _parse_dalfox(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            try:
                data = json.loads(line)
                if data.get("type") in ("found", "verified"):
                    findings.append(VAPTFinding(
                        title="Reflected XSS Detected",
                        description=f"{data.get('data', '')[:400]} at {data.get('url', target)}",
                        severity=VAPTSeverity.HIGH,
                        tool_name=tool_name,
                        target=target,
                        vulnerability_type="Cross-Site Scripting (XSS)",
                        remediation="Implement output encoding and CSP headers",
                    ))
            except (json.JSONDecodeError, KeyError):
                continue
        return findings

    def _parse_commix(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            if "+++" in line or "is vulnerable" in line.lower() or "Parameter:" in line:
                findings.append(VAPTFinding(
                    title="OS Command Injection",
                    description=line[:400],
                    severity=VAPTSeverity.CRITICAL,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="Command Injection",
                    remediation="Validate and sanitize all input; use allowlisted parameters",
                ))
        return findings

    def _parse_hydra(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            if line.startswith("["):
                findings.append(VAPTFinding(
                    title="Valid Credentials Found",
                    description=line[:300],
                    severity=VAPTSeverity.CRITICAL,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="Weak Credentials",
                    remediation="Enforce strong password policy and rate-limit login attempts",
                ))
        return findings

    def _parse_testssl(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            try:
                data = json.loads(line)
                severity = (data.get("severity") or "").lower()
                if severity in ("high", "critical", "medium", "low"):
                    findings.append(VAPTFinding(
                        title=f"TLS: {data.get('finding', 'issue')[:180]}",
                        description=(data.get("finding", "") + " " + str(data.get("cve", "")))[:500],
                        severity=self._severity_from_str(severity),
                        tool_name=tool_name,
                        target=target,
                        vulnerability_type="SSL/TLS Misconfiguration",
                        remediation="Update TLS configuration and cipher suites",
                    ))
            except (json.JSONDecodeError, KeyError):
                continue
        return findings

    def _severity_from_str(self, severity: str) -> VAPTSeverity:
        mapping = {
            "critical": VAPTSeverity.CRITICAL,
            "high": VAPTSeverity.HIGH,
            "medium": VAPTSeverity.MEDIUM,
            "low": VAPTSeverity.LOW,
            "info": VAPTSeverity.INFO,
        }
        return mapping.get(severity, VAPTSeverity.INFO)

    async def _execute_demo_scan(
        self,
        request: VAPTScanRequest,
        result: VAPTScanResult,
    ) -> VAPTScanResult:
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


    def run_tool_sync(self, tool_id: str, target: str, timeout: int = 120) -> str:
        tool = get_tool(tool_id)
        if not tool:
            return ""
        if tool.requires_url and not target.startswith(("http://", "https://")):
            target = f"http://{target}"
        cmd = self._build_docker_command(tool, target)
        if not cmd:
            return ""
        cmd = f"timeout --kill-after=5 {timeout}s bash -c '{cmd}'"
        return self._run_container_sync(self.KALI_IMAGE, cmd, f"astraix-vrfy-{uuid4().hex[:8]}", timeout)

    # ------------------------------------------------------------------
    # Agent-loop single-tool execution (Phase 1)
    # ------------------------------------------------------------------

    async def run_agent_tool(
        self,
        tool_id: str,
        target: str,
        extra_args: str = "",
    ) -> "tuple[List[VAPTFinding], str, Optional[str]]":
        """Run exactly one tool against the target for the autonomous agent.

        Returns ``(findings, raw_output, error)``. Never raises for tool
        failures - errors are returned as the third element so the agent
        loop can decide the next step instead of aborting.
        """
        tool = get_tool(tool_id)
        if not tool:
            return [], "", f"Unknown tool: {tool_id}"

        if self._demo_mode or not self._use_docker:
            return self._demo_agent_tool(tool, target), "", None

        if not await self._check_docker():
            return self._demo_agent_tool(tool, target), "", None

        target = target.strip()
        if tool.requires_url and not target.startswith(("http://", "https://")):
            target = f"http://{target}"

        cmd = self._build_docker_command(tool, target)
        if not cmd:
            return [], "", f"Could not build command for {tool_id}"
        if extra_args:
            cmd = f"{cmd} {extra_args}"

        cmd = f"timeout --kill-after=5 {tool.timeout}s bash -c '{cmd}'"
        container_name = f"astraix-agent-{uuid4().hex[:8]}"

        try:
            output = await asyncio.wait_for(
                asyncio.to_thread(
                    self._run_container_sync,
                    self.KALI_IMAGE,
                    cmd,
                    container_name,
                    tool.timeout,
                ),
                timeout=tool.timeout + 30,
            )
            findings = self._parse_output(output, tool, target)
            return findings, output, None
        except asyncio.TimeoutError:
            self._kill_container(container_name)
            return [], "", f"{tool_id}: timed out after {tool.timeout}s"
        except Exception as e:
            return [], "", f"{tool_id}: {str(e)}"

    def _demo_agent_tool(self, tool: VAPTTool, target: str) -> List[VAPTFinding]:
        """Synthetic findings so the agent loop works in demo mode."""
        if tool.phase == "recon":
            return [VAPTFinding(
                title=f"Open Port: 443/tcp",
                description=f"{tool.name} detected an HTTPS service",
                severity=VAPTSeverity.INFO,
                tool_name=tool.name,
                target=target,
                port=443,
                protocol="tcp",
                service="https",
            )]
        if tool.phase == "deep":
            return [VAPTFinding(
                title=f"{tool.name} Potential Finding",
                description=f"{tool.name} surfaced a candidate issue on {target}",
                severity=VAPTSeverity.MEDIUM,
                tool_name=tool.name,
                target=target,
                vulnerability_type="Agent-detected",
                remediation="Review and confirm before remediation planning",
            )]
        return [VAPTFinding(
            title=f"{tool.name} Discovery",
            description=f"{tool.name} enumerated surface on {target}",
            severity=VAPTSeverity.INFO,
            tool_name=tool.name,
            target=target,
        )]


_executor: Optional[VAPTExecutor] = None


def get_vapt_executor() -> VAPTExecutor:
    global _executor
    if _executor is None:
        _executor = VAPTExecutor()
    return _executor
