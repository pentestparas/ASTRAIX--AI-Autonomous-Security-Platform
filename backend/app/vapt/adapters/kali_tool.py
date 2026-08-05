"""Adapters that run tools inside the astraix-kali container.

raccoon  - recon/info-gathering CLI (DNS, WHOIS, TLS, WAF, subdomains, dirs)
lyrie    - autonomous 7-phase pentest CLI (lyrie-omega, SARIF output)
"""

import asyncio
import json
import os
import re
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.vapt.adapters.base import AdapterScanResult, AdapterStatus, VAPTAdapter
from app.vapt.models import VAPTSeverity, VAPTScanType
from app.core.logging import get_logger

logger = get_logger(__name__)

KALI_IMAGE = "astraix-kali:latest"


class _ContainerRunner:
    """Minimal Docker-socket runner for one-shot commands in the Kali image."""

    @staticmethod
    def run_sync(cmd_string: str, timeout: int, container_name: str) -> str:
        import docker
        from docker.errors import NotFound

        client = docker.from_env()
        container = None
        try:
            container = client.containers.run(
                image=KALI_IMAGE,
                command=["sh", "-c", cmd_string],
                name=container_name,
                network_mode="bridge",
                mem_limit="1024m",
                nano_cpus=int(1 * 1e9),
                detach=True,
                auto_remove=False,
            )
            result = container.wait(timeout=timeout)
            logs = container.logs(stdout=True, stderr=True).decode("utf-8", errors="ignore")
            if result.get("StatusCode", 0) != 0:
                logs += f"\n[exit={result.get('StatusCode')}]"
            return logs
        except Exception as e:  # noqa: BLE001
            if type(e).__name__ in ("TimeoutError", "ReadTimeout", "ReadTimeoutError"):
                raise asyncio.TimeoutError() from e
            return f"ERROR: {e}"
        finally:
            if container:
                try:
                    container.remove(force=True)
                except Exception:  # noqa: BLE001
                    pass

    @staticmethod
    async def run(cmd_string: str, timeout: int, container_name: str) -> str:
        try:
            return await asyncio.wait_for(
                asyncio.to_thread(
                    _ContainerRunner.run_sync, cmd_string, timeout, container_name
                ),
                timeout=timeout + 30,
            )
        except asyncio.TimeoutError:
            # Cancelling the thread does NOT kill it - it stays blocked in
            # docker wait. Force-remove the container so the daemon's wait
            # returns immediately and the thread can wind down.
            _ContainerRunner._force_remove(container_name)
            return "ERROR: container timeout"

    @staticmethod
    def _force_remove(container_name: str) -> None:
        try:
            import docker

            client = docker.from_env()
            try:
                c = client.containers.get(container_name)
                c.remove(force=True)
            finally:
                client.close()
        except Exception:  # noqa: BLE001
            pass


class _KaliToolAdapter(VAPTAdapter):
    """Base for tools installed inside the Kali image."""

    binary: str = ""

    def __init__(self) -> None:
        self._image_checked: Optional[bool] = None
        self._binaries: Dict[str, bool] = {}

    # ------------------------------------------------------------ config

    def configured(self) -> bool:
        return True

    # ------------------------------------------------------------ health

    def _image_exists(self) -> bool:
        if self._image_checked is not None:
            return self._image_checked
        try:
            import docker

            client = docker.from_env()
            try:
                images = client.images.list(name=KALI_IMAGE)
                self._image_checked = len(images) > 0
            finally:
                client.close()
        except Exception:  # noqa: BLE001
            self._image_checked = False
        return self._image_checked

    def _binary_installed(self) -> bool:
        if not self._image_exists():
            return False
        if self.binary in self._binaries:
            return self._binaries[self.binary]
        out = _ContainerRunner.run_sync(
            f"command -v {self.binary} || true", 30, f"astraix-adapt-{uuid4().hex[:8]}"
        )
        ok = self.binary in out and "ERROR:" not in out
        self._binaries[self.binary] = ok
        return ok

    async def health(self) -> AdapterStatus:
        if not self._image_exists():
            return AdapterStatus(
                id=self.id, name=self.name, enabled=self.enabled(),
                configured=True, available=False,
                description=self.description,
                error=f"Kali image {KALI_IMAGE} not present - run docker build -f docker/kali-tools.Dockerfile -t {KALI_IMAGE} .",
            )
        if not self._binary_installed():
            return AdapterStatus(
                id=self.id, name=self.name, enabled=self.enabled(),
                configured=True, available=False,
                description=self.description,
                error=f"'{self.binary}' not installed in {KALI_IMAGE} - add it to docker/kali-tools.Dockerfile and rebuild",
            )
        return AdapterStatus(
            id=self.id, name=self.name, enabled=self.enabled(),
            configured=True, available=True, description=self.description,
        )

    async def run_scan(
        self,
        target: str,
        scan_id: str,
        scan_type: VAPTScanType,
        target_info: Dict[str, Any],
    ) -> AdapterScanResult:
        result = AdapterScanResult(adapter_id=self.id)
        started = self._now()
        try:
            if not self._binary_installed():
                result.errors.append(f"{self.binary} not installed in {KALI_IMAGE}")
                return result
            cmd = self._build_command(target, target_info)
            out = await _ContainerRunner.run(
                cmd, timeout=self.timeout, container_name=f"astraix-adapt-{uuid4().hex[:8]}"
            )
            if out.startswith("ERROR:"):
                result.errors.append(out)
                return result
            result.raw["output"] = out[-4000:]
            result.findings = self._parse(out, target)
            if not result.findings:
                result.errors.append("No findings parsed from output")
        except Exception as e:  # noqa: BLE001
            logger.exception("Adapter %s failed", self.id)
            result.errors.append(f"{type(e).__name__}: {e}")
        result.duration = self._run_duration(started)
        return result

    @staticmethod
    def _now() -> float:
        import time

        return time.time()

    def _build_command(self, target: str, target_info: Dict[str, Any]) -> str:
        raise NotImplementedError

    def _parse(self, output: str, target: str):
        raise NotImplementedError

    @property
    def timeout(self) -> int:
        return 600


class RaccoonAdapter(_KaliToolAdapter):
    """Raccoon recon scanner (DNS/WHOIS/TLS/WAF/subdomains/dir-busting)."""

    id = "raccoon"
    name = "Raccoon"
    description = "Recon & information gathering (DNS, WHOIS, TLS, WAF, subdomains, directories)"
    binary = "raccoon"
    timeout = 600

    def configured(self) -> bool:
        return self._env_flag("VAPT_ADAPTER_RACCOON", default=True)

    def enabled(self) -> bool:
        return self.configured()

    def allow_for(self, scan_type: VAPTScanType, target_info: Dict[str, Any]) -> bool:
        # Raccoon needs a resolvable hostname/domain to be useful
        return scan_type in (VAPTScanType.NETWORK, VAPTScanType.WEB, VAPTScanType.API, VAPTScanType.FULL) and not target_info.get("is_ip", False)

    def _build_command(self, target: str, target_info: Dict[str, Any]) -> str:
        return (
            f"mkdir -p /tmp/raccoon-out && raccoon -d A,MX,NS,SOA,TXT,CNAME "
            f"--skip-health-check {target} -o /tmp/raccoon-out > /tmp/raccoon.log 2>&1; "
            f"cat /tmp/raccoon-out/*/*.txt 2>/dev/null; echo '---STDOUT---'; tail -n 120 /tmp/raccoon.log"
        )

    def _parse(self, output: str, target: str):
        findings = []
        sections = {}
        current = "general"
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            low = line.lower()
            if self._is_noise(line):
                continue
            if line.endswith(":") or (re.match(r"^[a-z\s]+:\s*$", line) and len(line) < 40):
                current = line[:-1].lower()
                sections.setdefault(current, [])
                continue
            sections.setdefault(current, []).append(line)

        def add(title: str, lines: List[str], sev: VAPTSeverity, vuln_type: str) -> None:
            joined = "; ".join(l for l in lines if l)
            if joined and joined != "-":
                findings.append(self._new_finding(
                    title=f"{title}: {target}",
                    description=joined[:500],
                    severity=sev,
                    target=target,
                    vulnerability_type=vuln_type,
                    confidence="observed",
                ))

        for section, lines in sections.items():
            s = section.lower()
            if "dns" in s:
                add("DNS Records", lines, VAPTSeverity.INFO, "Information Disclosure")
            elif "whois" in s or "registrar" in s:
                add("WHOIS Data", lines, VAPTSeverity.INFO, "Information Disclosure")
            elif "tls" in s or "ssl" in s:
                add("TLS Configuration", lines, VAPTSeverity.MEDIUM, "SSL/TLS Misconfiguration")
            elif "waf" in s:
                add("WAF Detected", lines, VAPTSeverity.INFO, "WAF Fingerprint")
            elif "subdomain" in s:
                add("Subdomains Discovered", lines, VAPTSeverity.INFO, "Subdomain Enumeration")
            elif "dir" in s or "bust" in s or "url" in s:
                add("Discovered Paths", lines, VAPTSeverity.INFO, "Content Discovery")
            elif "port" in s:
                add("Open Ports (raccoon)", lines, VAPTSeverity.INFO, "Open Ports")
            else:
                add(f"Raccoon {section.title()}", lines, VAPTSeverity.INFO, "Reconnaissance")
        return findings[:40]

    @staticmethod
    def _is_noise(line: str) -> bool:
        """Filter crash/traceback/banner noise out of tool output before parsing."""
        clean = re.sub(r"\x1b\[[0-9;]*[mGKH]", "", line).strip()
        return (
            "traceback" in clean.lower()
            or clean.startswith(("File \"", "  ^", "~~~", "~~~~"))
            or "TypeError:" in clean
            or "AttributeError:" in clean
            or "ModuleNotFoundError:" in clean
            or clean.startswith("---STDOUT---")
            or "raccoon scan" in clean.lower()
            or "trying to gather information" in clean.lower()
            or "github.com/evyatarmeged" in clean.lower()
            or (len(clean) == 40 and all(c in "0123456789abcdef" for c in clean))
            or not any(c.isalnum() for c in clean)
        )


class LyrieAdapter(_KaliToolAdapter):
    """Lyrie autonomous pentest CLI (lyrie scan -> SARIF findings)."""

    id = "lyrie"
    name = "Lyrie"
    description = "Autonomous 7-phase pentest agent (recon -> exploit -> PoC -> report, SARIF output)"
    binary = "lyrie"
    timeout = 1800

    def configured(self) -> bool:
        # Lyrie needs an LLM key configured at runtime
        has_key = any(
            os.environ.get(k)
            for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "LYRIE_LICENSE_KEY", "GEMINI_API_KEY")
        )
        return self._env_flag("VAPT_ADAPTER_LYRIE", default=False) and has_key

    def enabled(self) -> bool:
        return self.configured()

    def allow_for(self, scan_type: VAPTScanType, target_info: Dict[str, Any]) -> bool:
        return scan_type in (VAPTScanType.WEB, VAPTScanType.API, VAPTScanType.FULL)

    def _build_command(self, target: str, target_info: Dict[str, Any]) -> str:
        tgt = target if target.startswith(("http://", "https://")) else f"https://{target}"
        return (
            f"lyrie scan {tgt} --output /tmp/lyrie.json --format sarif > /tmp/lyrie.log 2>&1 || true; "
            f"cat /tmp/lyrie.json 2>/dev/null || tail -n 200 /tmp/lyrie.log"
        )

    def _parse(self, output: str, target: str):
        findings = []
        try:
            sarif = json.loads(output)
            runs = sarif.get("runs", [])
            for run in runs:
                for r in run.get("results", []):
                    rule = {}
                    for rd in run.get("tool", {}).get("driver", {}).get("rules", []):
                        if rd.get("id") == r.get("ruleId"):
                            rule = rd
                            break
                    msg = r.get("message", {}).get("text", "")
                    locs = r.get("locations", [])
                    loc = locs[0].get("physicalLocation", {}) if locs else {}
                    region = loc.get("region", {})
                    details = {
                        "sarif_rule": r.get("ruleId"),
                        "line": region.get("startLine"),
                        "sarif_level": r.get("level"),
                    }
                    findings.append(self._new_finding(
                        title=(rule.get("shortDescription", {}).get("text") or rule.get("name") or r.get("ruleId") or "Lyrie Finding")[:200],
                        description=(rule.get("fullDescription", {}).get("text") or msg)[:500],
                        severity=r.get("level"),
                        target=target,
                        vulnerability_type=r.get("ruleId"),
                        remediation=msg[:400],
                        host=loc.get("uri"),
                        path=loc.get("uri"),
                        confidence="confirmed",
                        details=details,
                    ))
        except (json.JSONDecodeError, ValueError):
            for line in output.splitlines():
                line = line.strip()
                if line and not line.startswith(("INFO", "WARN", "DEBUG", "[")):
                    findings.append(self._new_finding(
                        title="Lyrie Output",
                        description=line[:300],
                        severity=VAPTSeverity.INFO,
                        target=target,
                        confidence="observed",
                    ))
        return findings[:50]
