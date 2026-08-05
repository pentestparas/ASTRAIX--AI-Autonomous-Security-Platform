"""Adapters for externally-deployed AI pentest platforms.

These integrations target stacks that are deployed independently of AstraIX:

  - darkmoon  (ASCIT31/Dark-Moon)  - CLI-driven autonomous pentest stack
  - pentagi   (vxcontrol/pentagi)  - REST/GraphQL API at :8443
  - redamon   (samugit83/redamon)  - webapp REST API at :3000
  - zenai     (zen-ai-pentest)     - GitHub Actions workflow

All adapters are env-gated: unless the operator configures the matching
environment variables, the adapter reports as disabled and never runs.
They are best-effort integrations - failures are captured per-adapter and
never abort the overall scan.
"""

import asyncio
import json
import os
import shutil
import time
from typing import Any, Dict, List, Optional

import httpx

from app.vapt.adapters.base import AdapterScanResult, AdapterStatus, VAPTAdapter, to_severity
from app.vapt.models import VAPTSeverity, VAPTScanType
from app.core.logging import get_logger

logger = get_logger(__name__)


class _HttpAdapter(VAPTAdapter):
    """Base for adapters that talk to an external HTTP API."""

    base_url_env = ""
    enabled_env = ""
    api_key_env = ""

    def _base_url(self) -> str:
        return self._env(self.base_url_env, "").rstrip("/")

    def configured(self) -> bool:
        return bool(self._base_url()) and self._env_flag(self.enabled_env, default=False)

    def enabled(self) -> bool:
        return self.configured()

    def allow_for(self, scan_type: VAPTScanType, target_info: Dict[str, Any]) -> bool:
        return scan_type in (VAPTScanType.WEB, VAPTScanType.API, VAPTScanType.FULL)

    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        key = self._env(self.api_key_env, "")
        if key:
            headers["Authorization"] = f"Bearer {key}"
        return headers

    async def health(self) -> AdapterStatus:
        if not self.configured():
            return AdapterStatus(
                id=self.id, name=self.name, enabled=False, configured=False,
                available=False, description=self.description,
                error=f"Set {self.enabled_env}=true and {self.base_url_env} to enable",
            )
        ok, err = await self._ping()
        return AdapterStatus(
            id=self.id, name=self.name, enabled=True, configured=True,
            available=ok, description=self.description, error=err,
        )

    async def _ping(self) -> tuple:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(self._base_url(), headers=self._headers())
                if r.status_code < 500:
                    return True, None
                return False, f"HTTP {r.status_code} from {self._base_url()}"
        except Exception as e:  # noqa: BLE001
            return False, f"{type(e).__name__}: {e}"


class DarkMoonAdapter(_HttpAdapter):
    """Dark-Moon autonomous pentest platform.

    Mode A (HTTP): DARKMOON_BASE_URL + DARKMOON_API_KEY.
    Mode B (CLI):  DARKMOON_PATH points at the repo's darkmoon.sh wrapper;
                   the stack is launched via the CLI and its structured
                   report output (reports/*.json) is parsed.
    """

    id = "darkmoon"
    name = "Dark-Moon"
    description = "Autonomous AI pentest engine (MCP-gatekept tool execution, proof-based findings)"
    base_url_env = "DARKMOON_BASE_URL"
    enabled_env = "VAPT_ADAPTER_DARKMOON"
    api_key_env = "DARKMOON_API_KEY"

    def configured(self) -> bool:
        if not self._env_flag(self.enabled_env, default=False):
            return False
        return bool(self._base_url() and self._env(self.api_key_env)) or bool(
            self._env("DARKMOON_PATH")
        )

    async def run_scan(
        self,
        target: str,
        scan_id: str,
        scan_type: VAPTScanType,
        target_info: Dict[str, Any],
    ) -> AdapterScanResult:
        result = AdapterScanResult(adapter_id=self.id)
        started = time.time()
        try:
            cli = self._env("DARKMOON_PATH", "")
            if cli:
                await self._run_cli(cli, target, result)
            else:
                await self._run_http(target, result)
        except Exception as e:  # noqa: BLE001
            logger.exception("DarkMoon adapter failed")
            result.errors.append(f"{type(e).__name__}: {e}")
        result.duration = self._run_duration(started)
        return result

    async def _run_cli(self, cli: str, target: str, result: AdapterScanResult) -> None:
        workdir = self._env("DARKMOON_WORKDIR", "/tmp/darkmoon")
        os.makedirs(workdir, exist_ok=True)
        proc = await asyncio.create_subprocess_exec(
            cli, f"TARGET: {target}",
            cwd=workdir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        try:
            out, _ = await asyncio.wait_for(proc.communicate(), timeout=self._env_int("DARKMOON_TIMEOUT", 1800))
            result.raw["output"] = out.decode("utf-8", errors="ignore")[-4000:]
        except asyncio.TimeoutError:
            proc.kill()
            result.errors.append("darkmoon.sh timed out")
            return
        result.findings = await asyncio.to_thread(self._parse_report_files, workdir, target)

    async def _run_http(self, target: str, result: AdapterScanResult) -> None:
        base = self._base_url()
        async with httpx.AsyncClient(timeout=60, headers=self._headers()) as client:
            r = await client.post(f"{base}/assessments", json={"target": target})
            if r.status_code not in (200, 201):
                result.errors.append(f"DarkMoon start failed: HTTP {r.status_code} {r.text[:200]}")
                return
            data = r.json()
        result.raw["assessment"] = data
        # Best-effort: no stable public REST contract - surface raw result
        # as a single finding so the operator can review it.
        if isinstance(data, dict) and data:
            result.findings.append(self._new_finding(
                title=f"Dark-Moon assessment started for {target}",
                description=json.dumps(data)[:500],
                severity=VAPTSeverity.INFO,
                target=target,
                vulnerability_type="External Platform Result",
                confidence="observed",
            ))

    @staticmethod
    def _parse_report_files(workdir: str, target: str) -> List[Any]:
        findings = []
        report_dirs = [os.path.join(workdir, "reports")]
        for d in report_dirs:
            if not os.path.isdir(d):
                continue
            for fname in os.listdir(d):
                if not fname.endswith(".json"):
                    continue
                try:
                    with open(os.path.join(d, fname), encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:  # noqa: BLE001
                    continue
                items = data if isinstance(data, list) else data.get("findings", data.get("results", []))
                if isinstance(items, dict):
                    items = items.get("items", [])
                for item in items if isinstance(items, list) else []:
                    if not isinstance(item, dict):
                        continue
                    findings.append({
                        "title": item.get("title") or item.get("name") or "Dark-Moon Finding",
                        "description": item.get("description") or "",
                        "severity": item.get("severity") or "info",
                        "remediation": item.get("remediation"),
                        "reference": item.get("reference"),
                        "cve": item.get("cve"),
                        "cwe": item.get("cwe"),
                        "details": item,
                    })
        return findings[:50]

    def _env_int(self, key: str, default: int) -> int:
        try:
            return int(self._env(key, str(default)))
        except ValueError:
            return default


class PentagiAdapter(_HttpAdapter):
    """PentAGI - fully autonomous pentesting agent (Go backend, REST API)."""

    id = "pentagi"
    name = "PentAGI"
    description = "Autonomous pentest AGI (terminal + browser agents, sandboxed Docker execution)"
    base_url_env = "PENTAGI_BASE_URL"
    enabled_env = "VAPT_ADAPTER_PENTAGI"
    api_key_env = "PENTAGI_API_KEY"

    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        user = self._env("PENTAGI_USER", "")
        pwd = self._env("PENTAGI_PASSWORD", "")
        if user and pwd:
            import base64

            token = base64.b64encode(f"{user}:{pwd}".encode()).decode()
            headers["Authorization"] = f"Basic {token}"
        elif self._env(self.api_key_env):
            headers["Authorization"] = f"Bearer {self._env(self.api_key_env)}"
        return headers

    async def run_scan(
        self,
        target: str,
        scan_id: str,
        scan_type: VAPTScanType,
        target_info: Dict[str, Any],
    ) -> AdapterScanResult:
        result = AdapterScanResult(adapter_id=self.id)
        started = time.time()
        base = self._base_url()
        try:
            async with httpx.AsyncClient(timeout=60, headers=self._headers()) as client:
                r = await client.post(
                    f"{base}/api/v1/assessments",
                    json={"target": target, "name": f"astraix-{scan_id[:8]}"},
                )
                if r.status_code not in (200, 201):
                    result.errors.append(f"PentAGI start failed: HTTP {r.status_code} {r.text[:200]}")
                    return
                data = r.json()
            result.raw["assessment"] = data
            await asyncio.sleep(self._env_int("PENTAGI_POLL_SECONDS", 30))
            result.findings = await self._poll_findings(base, target)
            if not result.findings:
                result.errors.append("PentAGI finished with no structured findings (check stack logs)")
        except Exception as e:  # noqa: BLE001
            logger.exception("Pentagi adapter failed")
            result.errors.append(f"{type(e).__name__}: {e}")
        result.duration = self._run_duration(started)
        return result

    async def _poll_findings(self, base: str, target: str) -> List[Any]:
        findings = []
        try:
            async with httpx.AsyncClient(timeout=30, headers=self._headers()) as client:
                r = await client.get(f"{base}/api/v1/findings")
                if r.status_code != 200:
                    return findings
                data = r.json()
        except Exception as e:  # noqa: BLE001
            logger.warning("PentAGI findings fetch failed: %s", e)
            return findings
        items = data if isinstance(data, list) else data.get("findings", data.get("data", []))
        if isinstance(items, dict):
            items = items.get("items", [])
        for item in items if isinstance(items, list) else []:
            if not isinstance(item, dict):
                continue
            findings.append(self._new_finding(
                title=item.get("title") or item.get("name") or "PentAGI Finding",
                description=item.get("description") or "",
                severity=item.get("severity"),
                target=target,
                vulnerability_type=item.get("category") or item.get("vulnerability_type"),
                remediation=item.get("remediation"),
                reference=item.get("reference"),
                cve=item.get("cve"),
                cwe=item.get("cwe"),
                confidence=item.get("status") or "observed",
            ))
        return findings[:50]

    def _env_int(self, key: str, default: int) -> int:
        try:
            return int(self._env(key, str(default)))
        except ValueError:
            return default


class RedamonAdapter(_HttpAdapter):
    """RedAmon - agentic red team framework (graph-powered, webapp API)."""

    id = "redamon"
    name = "RedAmon"
    description = "Agentic red-team framework (recon pipeline + LangGraph agents over Neo4j attack graph)"
    base_url_env = "REDAMON_BASE_URL"
    enabled_env = "VAPT_ADAPTER_REDAMON"
    api_key_env = "REDAMON_API_KEY"

    async def run_scan(
        self,
        target: str,
        scan_id: str,
        scan_type: VAPTScanType,
        target_info: Dict[str, Any],
    ) -> AdapterScanResult:
        result = AdapterScanResult(adapter_id=self.id)
        started = time.time()
        base = self._base_url()
        try:
            async with httpx.AsyncClient(timeout=60, headers=self._headers()) as client:
                r = await client.post(
                    f"{base}/api/projects",
                    json={"name": f"astraix-{scan_id[:8]}", "targets": [target]},
                )
                if r.status_code not in (200, 201):
                    result.errors.append(f"RedAmon start failed: HTTP {r.status_code} {r.text[:200]}")
                    return
                data = r.json()
            result.raw["project"] = data
            await asyncio.sleep(self._env_int("REDAMON_POLL_SECONDS", 60))
            result.findings = await self._poll_findings(base, target)
            if not result.findings:
                result.errors.append("RedAmon returned no structured findings (check stack logs)")
        except Exception as e:  # noqa: BLE001
            logger.exception("Redamon adapter failed")
            result.errors.append(f"{type(e).__name__}: {e}")
        result.duration = self._run_duration(started)
        return result

    async def _poll_findings(self, base: str, target: str) -> List[Any]:
        findings = []
        for endpoint in ("/api/findings", "/api/v1/findings", "/api/vulnerabilities"):
            try:
                async with httpx.AsyncClient(timeout=30, headers=self._headers()) as client:
                    r = await client.get(f"{base}{endpoint}")
                if r.status_code != 200:
                    continue
                data = r.json()
                items = data if isinstance(data, list) else data.get("findings", data.get("data", data.get("vulnerabilities", [])))
                if isinstance(items, dict):
                    items = items.get("items", [])
                for item in items if isinstance(items, list) else []:
                    if not isinstance(item, dict):
                        continue
                    findings.append(self._new_finding(
                        title=item.get("title") or item.get("name") or "RedAmon Finding",
                        description=item.get("description") or item.get("summary") or "",
                        severity=item.get("severity") or item.get("risk"),
                        target=target,
                        vulnerability_type=item.get("category") or item.get("vulnerability_type"),
                        remediation=item.get("remediation") or item.get("fix"),
                        reference=item.get("reference") or item.get("url"),
                        cve=item.get("cve"),
                        cwe=item.get("cwe"),
                        cvss_score=self._to_float(item.get("cvss", item.get("cvss_score"))),
                        confidence=item.get("status") or "observed",
                    ))
                if findings:
                    break
            except Exception as e:  # noqa: BLE001
                logger.warning("RedAmon endpoint %s failed: %s", endpoint, e)
        return findings[:50]

    @staticmethod
    def _to_float(value: Any) -> Optional[float]:
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    def _env_int(self, key: str, default: int) -> int:
        try:
            return int(self._env(key, str(default)))
        except ValueError:
            return default


class ZenAiAdapter(VAPTAdapter):
    """zen-ai-pentest GitHub Action adapter (CI/CD).

    Requires a GitHub repo with the action workflow installed, plus `gh` CLI
    auth. Triggered via `gh workflow run`, results polled through `gh run`.
    """

    id = "zenai"
    name = "Zen AI Pentest"
    description = "Zen AI pentest GitHub Action - CI/CD-driven security testing (triggered per scan)"

    def configured(self) -> bool:
        if not self._env_flag("VAPT_ADAPTER_ZENAI", default=False):
            return False
        return bool(self._env("ZENAI_REPO")) and shutil.which("gh") is not None

    def enabled(self) -> bool:
        return self.configured()

    def allow_for(self, scan_type: VAPTScanType, target_info: Dict[str, Any]) -> bool:
        return scan_type in (VAPTScanType.WEB, VAPTScanType.API, VAPTScanType.FULL)

    async def health(self) -> AdapterStatus:
        if not self.configured():
            return AdapterStatus(
                id=self.id, name=self.name, enabled=False, configured=False,
                available=False, description=self.description,
                error="Set VAPT_ADAPTER_ZENAI=true and ZENAI_REPO=owner/repo with gh CLI authenticated",
            )
        ok, err = await self._gh_auth_ok()
        return AdapterStatus(
            id=self.id, name=self.name, enabled=True, configured=True,
            available=ok, description=self.description, error=err,
        )

    async def _gh_auth_ok(self) -> tuple:
        proc = await asyncio.create_subprocess_exec(
            "gh", "auth", "status",
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
        )
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=15)
        text = out.decode("utf-8", errors="ignore")
        return ("Logged in" in text), (text[-300:] if "Logged in" not in text else None)

    async def run_scan(
        self,
        target: str,
        scan_id: str,
        scan_type: VAPTScanType,
        target_info: Dict[str, Any],
    ) -> AdapterScanResult:
        result = AdapterScanResult(adapter_id=self.id)
        started = time.time()
        repo = self._env("ZENAI_REPO", "")
        workflow = self._env("ZENAI_WORKFLOW", "zen-ai-pentest.yml")
        try:
            proc = await asyncio.create_subprocess_exec(
                "gh", "workflow", "run", workflow,
                "--repo", repo,
                "-f", f"target={target}",
                "-f", f"astraix_scan_id={scan_id}",
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            )
            out, _ = await asyncio.wait_for(proc.communicate(), timeout=60)
            text = out.decode("utf-8", errors="ignore")
            if proc.returncode != 0:
                result.errors.append(f"gh workflow run failed: {text[-300:]}")
                return result
            result.raw["run_triggered"] = True
            result.raw["gh_output"] = text[-300:]
            await asyncio.sleep(self._env_int("ZENAI_WAIT_SECONDS", 30))
            result.findings = await self._fetch_run_findings(repo, result)
        except asyncio.TimeoutError:
            result.errors.append("gh workflow run timed out")
        except Exception as e:  # noqa: BLE001
            logger.exception("ZenAI adapter failed")
            result.errors.append(f"{type(e).__name__}: {e}")
        result.duration = self._run_duration(started)
        return result

    async def _fetch_run_findings(self, repo: str, result: AdapterScanResult) -> List[Any]:
        findings = []
        try:
            proc = await asyncio.create_subprocess_exec(
                "gh", "run", "list", "--repo", repo, "--limit", "1", "--json", "databaseId,status,conclusion",
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            )
            out, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
            runs = json.loads(out.decode() or "[]")
            if not runs:
                return findings
            run_id = runs[0]["databaseId"]
            proc = await asyncio.create_subprocess_exec(
                "gh", "run", "view", str(run_id), "--repo", repo, "--json", "jobs",
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            )
            out, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
            data = json.loads(out.decode() or "{}")
            result.raw["run_id"] = run_id
            for job in data.get("jobs", []):
                for step in job.get("steps", []):
                    if step.get("conclusion") == "failure" and step.get("name"):
                        findings.append(self._new_finding(
                            title=f"Zen AI Pentest: {step['name']}",
                            description=f"GitHub Actions run #{run_id} failed at step '{step['name']}' - review the workflow logs for findings.",
                            severity=VAPTSeverity.MEDIUM,
                            target=repo,
                            vulnerability_type="CI/CD Security Finding",
                            confidence="observed",
                            details={"job": job.get("name"), "run_id": run_id},
                        ))
        except Exception as e:  # noqa: BLE001
            logger.warning("ZenAI run fetch failed: %s", e)
        return findings

    def _env_int(self, key: str, default: int) -> int:
        try:
            return int(self._env(key, str(default)))
        except ValueError:
            return default
