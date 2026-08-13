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

    def _host_port_target(self, target: str) -> str:
        """Reduce a URL target to bare host[:port] for host-oriented tools."""
        host = target.split("://")[-1].split("/")[0]
        return host

    def _target_port(self, target: str) -> str:
        """Extract an explicit port from a URL target, else the scheme default."""
        host = target.split("://")[-1].split("/")[0]
        if ":" in host:
            port = host.rsplit(":", 1)[-1]
            if port.isdigit():
                return port
        return "443" if target.startswith("https") else "80"

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
            "sqlmap": f"sqlmap -u {target} --batch --random-agent --crawl=1 --output-dir=/tmp",
            "nuclei": f"nuclei -u {target} -json-export - -silent -rate-limit 150",
            "nikto": f"nikto -h {target} -Format xml -output -",
            "gobuster": f"gobuster dir -u {target} -w {wl_dirs} -o - -f -q -t 10",
            "ffuf": f"ffuf -u {target}/FUZZ -w {wl_dirs_medium} -json -rate 100",
            "sslscan": f"sslscan --xml=- --no-failed {target}",
            "trivy": f"trivy image --quiet --format json alpine:latest",
            "hydra": f"hydra -L {wl_users} -P {wl_rockyou} -t 4 -w 10 {self._host_port_target(target)} -s {self._target_port(target)}",
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
            "katana": f"katana -u {target} -json -silent -o /tmp/katana.json > /dev/null 2>&1; cat /tmp/katana.json 2>/dev/null",
            "feroxbuster": f"feroxbuster -u {target} -w {wl_dirs} -q -t 10 --json 2>/dev/null",
            "dirsearch": f"dirsearch -u {target} -w {wl_dirs} --format=json -o /tmp/ds.json -q 2>/dev/null; cat /tmp/ds.json 2>/dev/null",
            "xsstrike": f"xsstrike -u {target} --skip-ba --skip-dom 2>/dev/null",
            "graphqlmap": f"graphqlmap -u {target} -v 1 2>/dev/null",
            "smuggler": f"smuggler -u {target} 2>/dev/null",
            "kiterunner": f"kr scan {target} -w /opt/wordlists/content/routes.krl --json 2>/dev/null",
            "gitleaks": f"git clone --depth 1 -q {target} /tmp/src 2>/dev/null; gitleaks dir /tmp/src --report-format json --redact --no-banner 2>/dev/null; rm -rf /tmp/src",
            "trufflehog": f"git clone --depth 1 -q {target} /tmp/src 2>/dev/null; trufflehog filesystem /tmp/src --json --no-update 2>/dev/null; rm -rf /tmp/src",
            "semgrep": f"git clone --depth 1 -q {target} /tmp/src 2>/dev/null; semgrep --config=auto --json /tmp/src 2>/dev/null; rm -rf /tmp/src",
            "bandit": f"git clone --depth 1 -q {target} /tmp/src 2>/dev/null; bandit -r -f json /tmp/src 2>/dev/null; rm -rf /tmp/src",
            "searchsploit": f"searchsploit --json {target} 2>/dev/null",
            "metasploit": (
                'H=$(echo ' + target + ' | sed -E "s#https?://([^/:]+).*#\\1#"); '
                'P=$(echo ' + target + ' | sed -E "s#.*:([0-9]+).*#\\1#"); '
                'echo "$P" | grep -qE "^[0-9]+$" || P=80; '
                'printf "use auxiliary/scanner/http/http_version\\nset RHOSTS %s\\nset RPORT %s\\nrun\\n'
                'use auxiliary/scanner/http/http_title\\nset RHOSTS %s\\nset RPORT %s\\nrun\\n'
                'use auxiliary/scanner/http/robots_txt\\nset RHOSTS %s\\nset RPORT %s\\nrun\\n'
                'use auxiliary/scanner/http/options\\nset RHOSTS %s\\nset RPORT %s\\nrun\\n'
                'use auxiliary/scanner/http/trace\\nset RHOSTS %s\\nset RPORT %s\\nrun\\n'
                'use auxiliary/scanner/http/http_put\\nset RHOSTS %s\\nset RPORT %s\\nrun\\n'
                'use auxiliary/scanner/http/dir_listing\\nset RHOSTS %s\\nset RPORT %s\\nrun\\n'
                'exit -y\\n" "$H" "$P" "$H" "$P" "$H" "$P" "$H" "$P" "$H" "$P" "$H" "$P" "$H" "$P" > /tmp/msf.rc; '
                'msfconsole -q -r /tmp/msf.rc 2>/dev/null'
            ),
            "zap": (
                'Z=http://zap:8080; A=astraixzap; '
                'curl -s "$Z/JSON/core/action/newSession?name=scan&overwrite=true&apikey=$A" >/dev/null; '
                'curl -s "$Z/JSON/core/action/accessUrl?url=' + target + '&followRedirects=true&apikey=$A" >/dev/null; '
                'SID=$(curl -s "$Z/JSON/spider/action/scan?url=' + target + '&maxChildren=10&apikey=$A" | jq -r .scan); '
                'for i in $(seq 1 75); do '
                'P=$(curl -s "$Z/JSON/spider/view/status?scanId=$SID&apikey=$A" | jq -r .status); '
                '[ "$P" = "100" ] && break; sleep 2; done; '
                'ASID=$(curl -s "$Z/JSON/ascan/action/scan?url=' + target + '&recurse=true&apikey=$A" | jq -r .scan); '
                'for i in $(seq 1 250); do '
                'P=$(curl -s "$Z/JSON/ascan/view/status?scanId=$ASID&apikey=$A" | jq -r .status); '
                '[ "$P" = "100" ] && break; sleep 2; done; '
                'curl -s "$Z/JSON/core/view/alerts?baseurl=' + target + '&start=0&count=100&apikey=$A" 2>/dev/null'
            ),
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
            "sqlmap": self._parse_sqlmap,
            "katana": self._parse_katana,
            "feroxbuster": self._parse_feroxbuster,
            "dirsearch": self._parse_dirsearch,
            "xsstrike": self._parse_xsstrike,
            "graphqlmap": self._parse_graphqlmap,
            "smuggler": self._parse_smuggler,
            "kiterunner": self._parse_kiterunner,
            "gitleaks": self._parse_gitleaks,
            "trufflehog": self._parse_trufflehog,
            "semgrep": self._parse_semgrep,
            "bandit": self._parse_bandit,
            "metasploit": self._parse_metasploit,
            "searchsploit": self._parse_searchsploit,
            "zap": self._parse_zap,
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
            import re
            import xml.etree.ElementTree as ET

            clean = re.sub(r"\x1b\[[0-9;]*m", "", output)
            root = ET.fromstring(clean)

            for item in root.findall(".//item"):
                name = (item.get("name") or "Nikto Finding")[:200]
                desc = (item.findtext("description", "") or "").strip()
                # Nikto emits ERROR nodes for tool-level failures
                # (TLS fingerprinting, update checks, host giving up).
                # They are NOT vulnerabilities - never surface them.
                if "ERROR" in name.upper() or "ERROR" in desc.upper():
                    continue
                if not desc:
                    continue
                # Nikto config/CLI noise: default "Nikto Finding" name with a
                # short or directive-style description is not a vulnerability.
                if (
                    name == "Nikto Finding"
                    and (
                        len(desc) < 30
                        or "requires a value" in desc.lower()
                        or desc.lower().startswith(("-usage", "usage:"))
                    )
                ):
                    continue
                findings.append(VAPTFinding(
                    title=name,
                    description=desc[:500],
                    severity=VAPTSeverity.MEDIUM,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="Web Server Misconfiguration",
                    remediation="Review and harden web server configuration",
                ))
        except Exception:
            for line in output.splitlines():
                stripped = line.strip()
                if "+" in stripped and not stripped.startswith("-"):
                    desc = stripped[1:200].strip()
                    if desc and "ERROR" not in desc.upper():
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

    def _parse_sqlmap(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        """Emit findings ONLY when sqlmap confirms an injection point.

        sqlmap banners/status lines (ASCII art, disclaimers, INFO/WARNING
        logs, output-dir notes) are noise and must never become findings.
        """
        import re

        clean = re.sub(r"\x1b\[[0-9;]*m", "", output)
        lines = clean.splitlines()
        findings = []
        # Parameter blocks look like:
        #   Parameter: q (GET)
        #       Type: boolean-based blind
        #       Title: AND boolean-based blind - WHERE or HAVING clause
        seen: set[str] = set()
        current_param = ""
        for i, line in enumerate(lines):
            s = line.strip()
            pm = re.match(r"Parameter:\s*(\S+)\s*\((GET|POST|Cookie|URI|Header)\)", s)
            if pm:
                current_param = f"{pm.group(1)} ({pm.group(2)})"
                # Find the following Type/Title/Technique block
                block = "\n".join(lines[i:i + 15])
                tm = re.search(r"Type:\s*(.+)$", block, re.MULTILINE)
                if tm:
                    title = f"SQL Injection in parameter {pm.group(1)} ({pm.group(2)})"
                    vuln_type = tm.group(1).strip()
                    key = f"{title}:{vuln_type}"
                    if key in seen:
                        continue
                    seen.add(key)
                    findings.append(VAPTFinding(
                        title=title,
                        description=(
                            f"sqlmap confirmed {vuln_type} injection in parameter "
                            f"{pm.group(1)} ({pm.group(2)}) on {target}."
                        ),
                        severity=VAPTSeverity.HIGH,
                        tool_name=tool_name,
                        target=target,
                        vulnerability_type="SQL Injection",
                        remediation=(
                            "Use parameterized queries / prepared statements, "
                            "validate and sanitize all user input, and apply the "
                            "principle of least privilege to the DB account."
                        ),
                    ))
                continue
            # Direct confirmation without a Parameter line
            vm = re.search(
                r"parameter\s+['\"]?(\w+)['\"]?\s+is vulnerable",
                s,
                re.IGNORECASE,
            )
            if vm:
                title = f"SQL Injection in parameter {vm.group(1)}"
                key = f"{title}"
                if key in seen:
                    continue
                seen.add(key)
                findings.append(VAPTFinding(
                    title=title,
                    description=f"sqlmap confirmed the parameter {vm.group(1)} is vulnerable on {target}.",
                    severity=VAPTSeverity.HIGH,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="SQL Injection",
                    remediation=(
                        "Use parameterized queries / prepared statements, "
                        "validate and sanitize all user input, and apply the "
                        "principle of least privilege to the DB account."
                    ),
                ))
        return findings[:10]

    def _parse_katana(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        seen: set[str] = set()
        for line in output.splitlines():
            try:
                data = json.loads(line)
                req = data.get("request", {})
                endpoint = req.get("endpoint", "")
                method = req.get("method", "GET")
                key = f"{method} {endpoint}"
                if key in seen or not endpoint:
                    continue
                seen.add(key)
                findings.append(VAPTFinding(
                    title=f"Endpoint Discovered: {endpoint[:180]}",
                    description=f"Crawler discovered {method} endpoint (depth {data.get('depth', '?')})",
                    severity=VAPTSeverity.INFO,
                    tool_name=tool_name,
                    target=target,
                    path=endpoint,
                    remediation="Review if this endpoint should be publicly reachable",
                ))
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
        return findings[:15]

    def _parse_feroxbuster(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        seen: set[str] = set()
        interesting = (200, 201, 204, 301, 302, 307, 401, 403, 405)
        for line in output.splitlines():
            try:
                data = json.loads(line)
                url = data.get("url", "")
                status = int(data.get("status") or 0)
                if url in seen or status not in interesting:
                    continue
                seen.add(url)
                findings.append(VAPTFinding(
                    title=f"Content Found: {url[:180]}",
                    description=f"Feroxbuster: status {status}, size {data.get('content_length', 0)}",
                    severity=VAPTSeverity.INFO,
                    tool_name=tool_name,
                    target=target,
                    path=url,
                    remediation="Review if this resource should be publicly accessible",
                ))
            except (json.JSONDecodeError, ValueError, TypeError):
                continue
        return findings[:15]

    def _parse_dirsearch(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            data = json.loads(output)
        except (json.JSONDecodeError, TypeError):
            return findings
        for path, meta in (data.get("results") or {}).items():
            status = int(meta.get("status") or 0)
            if status in (200, 201, 204, 301, 302, 307, 401, 403):
                findings.append(VAPTFinding(
                    title=f"Path Found: {path[:180]}",
                    description=f"Dirsearch: status {status}, size {meta.get('content-length', 0)}",
                    severity=VAPTSeverity.INFO,
                    tool_name=tool_name,
                    target=target,
                    path=path,
                    remediation="Review if this path should be publicly accessible",
                ))
        return findings[:15]

    def _parse_xsstrike(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        block: List[str] = []
        for line in output.splitlines():
            s = line.strip()
            if s.startswith("[+]"):
                block.append(s[3:200])
            elif "payload" in s.lower() and block:
                block.append(s[:200])
        if block:
            findings.append(VAPTFinding(
                title="XSS Vector Detected",
                description="XSStrike reported a potential XSS vector: " + " | ".join(block)[:500],
                severity=VAPTSeverity.MEDIUM,
                tool_name=tool_name,
                target=target,
                vulnerability_type="Cross-Site Scripting (XSS)",
                remediation="Sanitize/encode output, implement CSP, validate input",
            ))
        return findings

    def _parse_graphqlmap(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            s = line.strip()
            if s.startswith("[+]") or "vulnerable" in s.lower() or "injectable" in s.lower():
                findings.append(VAPTFinding(
                    title="GraphQL Issue",
                    description=s[:400],
                    severity=VAPTSeverity.MEDIUM,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="GraphQL Misconfiguration",
                    remediation="Disable introspection in production, add rate limiting and auth",
                ))
        return findings[:8]

    def _parse_smuggler(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            s = line.strip()
            if any(k in s.lower() for k in ("smuggle", "vulnerable", "possible h2c", "cl.te", "te.cl")):
                findings.append(VAPTFinding(
                    title="HTTP Request Smuggling",
                    description=s[:400],
                    severity=VAPTSeverity.HIGH,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="HTTP Request Smuggling",
                    remediation="Normalize content-length/transfer-encoding handling at the edge",
                ))
        return findings[:8]

    def _parse_kiterunner(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        seen: set[str] = set()
        interesting = (200, 201, 204, 301, 302, 307, 401, 403)
        for line in output.splitlines():
            try:
                data = json.loads(line)
                path = data.get("path", "")
                status = int(data.get("statusCode") or 0)
                key = f"{status} {path}"
                if key in seen or status not in interesting or not path:
                    continue
                seen.add(key)
                findings.append(VAPTFinding(
                    title=f"API Route Found: {path[:160]}",
                    description=f"Kiterunner: status {status}, length {data.get('length', 0)}",
                    severity=VAPTSeverity.INFO,
                    tool_name=tool_name,
                    target=target,
                    path=path,
                    remediation="Review if this route should be publicly accessible",
                ))
            except (json.JSONDecodeError, ValueError, TypeError):
                continue
        return findings[:15]

    def _parse_gitleaks(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            data = json.loads(output)
        except (json.JSONDecodeError, TypeError):
            return findings
        for f in (data.get("Findings") or [])[:20]:
            findings.append(VAPTFinding(
                title=f"Leaked Secret: {f.get('RuleID', 'secret')[:120]}",
                description=(
                    f"Secret {f.get('Description', '')[:200]} in {f.get('File', '')[:160]}"
                    f" line {f.get('StartLine', '?')}"
                ),
                severity=VAPTSeverity.HIGH,
                tool_name=tool_name,
                target=target,
                vulnerability_type="Exposed Secret",
                remediation="Rotate the exposed credential immediately and purge it from history",
            ))
        return findings

    def _parse_trufflehog(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        for line in output.splitlines():
            try:
                data = json.loads(line)
                if not data.get("DetectorName"):
                    continue
                verified = "VERIFIED" if data.get("Verified") else "possible"
                findings.append(VAPTFinding(
                    title=f"{verified} Secret: {data['DetectorName'][:120]}",
                    description=(
                        f"Raw match: {str(data.get('Raw', ''))[:120]} in "
                        f"{str(data.get('SourceMetadata', {}).get('Data', {}).get('Filesystem', {}).get('file', ''))[:160]}"
                    ),
                    severity=VAPTSeverity.HIGH if data.get("Verified") else VAPTSeverity.MEDIUM,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="Exposed Secret",
                    remediation="Rotate the exposed credential immediately and purge it from history",
                ))
            except (json.JSONDecodeError, TypeError):
                continue
        return findings[:20]

    def _parse_semgrep(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            data = json.loads(output)
        except (json.JSONDecodeError, TypeError):
            return findings
        sev_map = {"ERROR": VAPTSeverity.HIGH, "WARNING": VAPTSeverity.MEDIUM, "INFO": VAPTSeverity.LOW}
        for r in (data.get("results") or [])[:20]:
            if r.get("path", "").startswith("/tmp"):
                continue
            sev = sev_map.get((r.get("extra") or {}).get("severity", "INFO"), VAPTSeverity.MEDIUM)
            findings.append(VAPTFinding(
                title=f"SAST: {str(r.get('check_id', 'rule'))[:120]}",
                description=(
                    f"{str((r.get('extra') or {}).get('message', ''))[:400]} in "
                    f"{str(r.get('path'))[:160]}:{r.get('start', {}).get('line', '?')}"
                ),
                severity=sev,
                tool_name=tool_name,
                target=target,
                vulnerability_type="Static Analysis Finding",
                remediation="Fix the flagged pattern; add tests to prevent regression",
            ))
        return findings

    def _parse_bandit(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            data = json.loads(output)
        except (json.JSONDecodeError, TypeError):
            return findings
        sev_map = {"HIGH": VAPTSeverity.HIGH, "MEDIUM": VAPTSeverity.MEDIUM, "LOW": VAPTSeverity.LOW}
        for r in (data.get("results") or [])[:20]:
            sev = sev_map.get(r.get("issue_severity", "LOW"), VAPTSeverity.LOW)
            findings.append(VAPTFinding(
                title=f"Bandit: {r.get('test_id', 'issue')[:60]}",
                description=(
                    f"{r.get('issue_text', '')[:350]} in "
                    f"{r.get('filename', '')[:160]}:{r.get('line_number', '?')}"
                ),
                severity=sev,
                tool_name=tool_name,
                target=target,
                vulnerability_type="Static Analysis Finding",
                remediation="Fix the flagged pattern; add tests to prevent regression",
            ))
        return findings

    def _parse_metasploit(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        current_module = "msf"
        for line in output.splitlines():
            s = line.strip()
            m = re.match(r"\[\*\]\s+([\w:/_]+)\s*=\s*(.+)", s)
            if m and m.group(1) in ("Module", "Auxiliary", "Exploit"):
                current_module = m.group(2)
            # msfconsole -q -r prints "[*] <module> is running..." per module
            m2 = re.match(r"\[\*\]\s+([\w_-]+)\s+is running", s)
            if m2:
                current_module = m2.group(1)
            m3 = re.match(r"\[\*\]\s+Running\s+([\w/]+)", s)
            if m3:
                current_module = m3.group(1)
            if s.startswith("[+]"):
                findings.append(VAPTFinding(
                    title=f"Metasploit: {current_module.split('/')[-1][:120]}",
                    description=s[3:400],
                    severity=VAPTSeverity.MEDIUM,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="Metasploit Module Finding",
                    remediation="Investigate and remediate the identified issue",
                ))
            elif "is vulnerable" in s.lower() and s.startswith(("[*]", "[+]")):
                findings.append(VAPTFinding(
                    title=f"Metasploit: vulnerable service on {target[:120]}",
                    description=s[:400],
                    severity=VAPTSeverity.HIGH,
                    tool_name=tool_name,
                    target=target,
                    vulnerability_type="Service Vulnerability",
                    remediation="Apply vendor patches/updates",
                ))
        return findings[:12]

    def _parse_zap(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            data = json.loads(output)
        except (json.JSONDecodeError, TypeError):
            return findings
        risk_map = {"0": VAPTSeverity.INFO, "1": VAPTSeverity.LOW,
                    "2": VAPTSeverity.MEDIUM, "3": VAPTSeverity.HIGH}
        seen: set[str] = set()
        for alert in data.get("alerts") or []:
            name = alert.get("alert", "ZAP Alert")
            url = alert.get("url", target)
            key = f"{name}:{url}"
            if key in seen:
                continue
            seen.add(key)
            findings.append(VAPTFinding(
                title=f"ZAP: {name[:180]}",
                description=(
                    f"{alert.get('description', '')[:400]} | Confidence: {alert.get('confidence', '?')} | "
                    f"{alert.get('solution', '')[:200]}"
                ),
                severity=risk_map.get(str(alert.get("risk")), VAPTSeverity.MEDIUM),
                tool_name=tool_name,
                target=target,
                path=url,
                vulnerability_type=str(alert.get("cweid") or "ZAP Active Scan Alert"),
                remediation=alert.get("solution", "Review and remediate per ZAP recommendation")[:500],
                reference="https://www.zaproxy.org/docs/desktop/addons/active-scan-rules/",
            ))
        return findings[:25]

    def _parse_searchsploit(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        try:
            data = json.loads(output)
        except (json.JSONDecodeError, TypeError):
            return findings
        for e in (data.get("RESULTS_EXPLOIT") or [])[:10]:
            title = e.get("Title", "exploit")
            path = e.get("Path", "")
            findings.append(VAPTFinding(
                title=f"Exploit Available: {title[:180]}",
                description=f"Exploit-DB entry matches query; file: {path[:200]}",
                severity=VAPTSeverity.LOW,
                tool_name=tool_name,
                target=target,
                vulnerability_type="Known Exploit",
                remediation="Patch the underlying software; monitor exploit activity",
            ))
        return findings

    def _parse_ffuf(self, output: str, target: str, tool_name: str) -> List[VAPTFinding]:
        findings = []
        seen: set = set()
        for line in output.splitlines():
            try:
                data = json.loads(line)
                if data.get("status") in (200, 301, 302, 401, 403):
                    url = data.get("url") or data.get("input", {}).get("FUZZ", "")
                    if url in seen:
                        continue
                    seen.add(url)
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
            if len(findings) >= 40:
                break
        return findings[:40]

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
            # A genuine hydra success is a [port][module] line carrying BOTH
            # login: and password:. [ERROR] lines, progress bars and other
            # [..] noise are NOT credentials - never surface them.
            if not line.strip().startswith("["):
                continue
            if "[error]" in line.lower():
                continue
            if "login:" not in line.lower() or "password:" not in line.lower():
                continue
            findings.append(VAPTFinding(
                title="Valid Credentials Found",
                description=line[:300],
                severity=VAPTSeverity.CRITICAL,
                tool_name=tool_name,
                target=target,
                vulnerability_type="Weak Credentials",
                remediation="Enforce strong password policy and rate-limit login attempts",
            ))
        # Deduplicate identical credential lines
        seen: set = set()
        unique = []
        for f in findings:
            key = (f.description, f.target)
            if key in seen:
                continue
            seen.add(key)
            unique.append(f)
        return unique

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
