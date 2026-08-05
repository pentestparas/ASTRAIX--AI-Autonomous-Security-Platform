"""Xalgorix adapter - autonomous pentest engine as a Docker sidecar.

Spawns the `xalgord/xalgorix:latest` container (batteries-included toolset +
LLM agent, 22-phase methodology), talks to its REST API on :9137, starts a
scan for the target, polls until completion and pulls findings.

Requires (env):
  XALGORIX_API_KEY   - LLM provider API key
  XALGORIX_LLM       - model id, e.g. "anthropic/claude-sonnet-4-5"
  VAPT_ADAPTER_XALGORIX - "true" (default false)
Optional:
  XALGORIX_API_BASE  - custom OpenAI-compatible base URL
  XALGORIX_IMAGE     - image tag (default xalgord/xalgorix:latest)
  XALGORIX_USERNAME / XALGORIX_PASSWORD - dashboard auth
"""

import asyncio
import json
import os
import re
import time
from typing import Any, Dict, List, Optional
from uuid import uuid4

import httpx

from app.vapt.adapters.base import AdapterScanResult, AdapterStatus, VAPTAdapter, to_severity
from app.vapt.models import VAPTSeverity, VAPTScanType
from app.core.logging import get_logger

logger = get_logger(__name__)

XALGORIX_IMAGE_DEFAULT = "xalgord/xalgorix:latest"


class XalgorixAdapter(VAPTAdapter):
    id = "xalgorix"
    name = "Xalgorix"
    description = "Autonomous AI pentest engine (22-phase, exploit-verified findings) via Docker sidecar"

    def __init__(self) -> None:
        self._container_name: Optional[str] = None

    # ------------------------------------------------------------ config

    def _image(self) -> str:
        return self._env("XALGORIX_IMAGE", XALGORIX_IMAGE_DEFAULT)

    def configured(self) -> bool:
        has_key = bool(self._env("XALGORIX_API_KEY")) or bool(
            self._env("XALGORIX_LLM_PROVIDER", self._env("XALGORIX_LLM"))
        )
        return self._env_flag("VAPT_ADAPTER_XALGORIX", default=False) and has_key

    def enabled(self) -> bool:
        return self.configured()

    def allow_for(self, scan_type: VAPTScanType, target_info: Dict[str, Any]) -> bool:
        return scan_type in (VAPTScanType.WEB, VAPTScanType.API, VAPTScanType.FULL)

    # ------------------------------------------------------------ health

    async def health(self) -> AdapterStatus:
        if not self.configured():
            return AdapterStatus(
                id=self.id, name=self.name, enabled=False, configured=False,
                available=False, description=self.description,
                error="Set VAPT_ADAPTER_XALGORIX=true and XALGORIX_API_KEY/XALGORIX_LLM to enable",
            )
        image_ok = await self._image_present()
        if not image_ok:
            return AdapterStatus(
                id=self.id, name=self.name, enabled=True, configured=True,
                available=False, description=self.description,
                error=f"Image {self._image()} not present - run: docker pull {self._image()}",
            )
        return AdapterStatus(
            id=self.id, name=self.name, enabled=True, configured=True,
            available=True, description=self.description,
        )

    async def _image_present(self) -> bool:
        try:
            import docker

            client = docker.from_env()
            try:
                return len(client.images.list(name=self._image().split(":")[0])) > 0
            finally:
                client.close()
        except Exception:  # noqa: BLE001
            return False

    # ------------------------------------------------------------ run

    async def run_scan(
        self,
        target: str,
        scan_id: str,
        scan_type: VAPTScanType,
        target_info: Dict[str, Any],
    ) -> AdapterScanResult:
        result = AdapterScanResult(adapter_id=self.id)
        started = time.time()
        container = None
        try:
            if not await self._image_present():
                result.errors.append(f"Image {self._image()} not present - docker pull it first")
                return result

            container, port = await self._spawn_sidecar()
            self._container_name = container
            base = f"http://127.0.0.1:{port}"

            if not await self._wait_ready(base, timeout=120):
                result.errors.append("Xalgorix API did not become ready in 120s")
                return result

            scan_resp = await self._start_scan(base, target)
            if not scan_resp:
                result.errors.append("Failed to start scan via Xalgorix API")
                return result

            scan_id_remote = scan_resp.get("id") or scan_resp.get("scan_id")
            await self._poll_scan(base, scan_id_remote, result)

            findings = await self._fetch_findings(base, target)
            result.findings = findings
            result.raw["remote_scan_id"] = scan_id_remote
            result.raw["api"] = base
            if not findings:
                result.errors.append("Scan finished but no findings were returned")
        except Exception as e:  # noqa: BLE001
            logger.exception("Xalgorix adapter failed")
            result.errors.append(f"{type(e).__name__}: {e}")
        finally:
            if container:
                await asyncio.to_thread(self._teardown_container, container)
                self._container_name = None
        result.duration = self._run_duration(started)
        return result

    # ------------------------------------------------------------ docker

    async def _spawn_sidecar(self) -> tuple:
        import docker

        client = docker.from_env()
        name = f"astraix-xalgorix-{uuid4().hex[:8]}"
        env = {
            "XALGORIX_LLM": self._env("XALGORIX_LLM", ""),
            "XALGORIX_API_KEY": self._env("XALGORIX_API_KEY", ""),
            "XALGORIX_API_BASE": self._env("XALGORIX_API_BASE", ""),
            "XALGORIX_ALLOW_LOCAL_TARGETS": "true",
            "XALGORIX_USERNAME": self._env("XALGORIX_USERNAME", "astraix"),
            "XALGORIX_PASSWORD": self._env("XALGORIX_PASSWORD", os.environ.get("SECRET_KEY", "astraix-pentest")[:24]),
            "XALGORIX_NO_AUTO_UPDATE": "1",
        }
        env = {k: v for k, v in env.items() if v}

        loop = asyncio.get_running_loop()
        try:
            container = await loop.run_in_executor(
                None,
                lambda: client.containers.run(
                    image=self._image(),
                    name=name,
                    detach=True,
                    auto_remove=False,
                    privileged=True,
                    environment=env,
                    ports={"9137/tcp": None},
                    network_mode="bridge",
                ),
            )
            port = await loop.run_in_executor(
                None,
                lambda: self._get_host_port(container),
            )
            if not port:
                raise RuntimeError("Could not determine mapped port for Xalgorix container")
            return name, port
        except Exception:
            await asyncio.to_thread(self._teardown_container, name)
            raise

    @staticmethod
    def _get_host_port(container) -> Optional[int]:
        for _ in range(30):
            container.reload()
            ports = container.attrs.get("NetworkSettings", {}).get("Ports", {}) or {}
            bindings = ports.get("9137/tcp") or []
            if bindings and bindings[0].get("HostPort"):
                return int(bindings[0]["HostPort"])
            time.sleep(1)
        return None

    @staticmethod
    def _teardown_container(name: str) -> None:
        import docker

        from docker.errors import NotFound

        client = docker.from_env()
        try:
            c = client.containers.get(name)
            c.remove(force=True)
        except NotFound:
            pass
        except Exception:  # noqa: BLE001
            pass
        finally:
            client.close()

    # ------------------------------------------------------------ api

    async def _wait_ready(self, base: str, timeout: int = 120) -> bool:
        deadline = time.time() + timeout
        async with httpx.AsyncClient(timeout=10) as client:
            while time.time() < deadline:
                try:
                    r = await client.get(f"{base}/api/status")
                    if r.status_code == 200:
                        return True
                except Exception:  # noqa: BLE001
                    pass
                await asyncio.sleep(3)
        return False

    async def _start_scan(self, base: str, target: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                r = await client.post(
                    f"{base}/api/scan",
                    json={
                        "target": target,
                        "mode": "single",
                        "instruction": "Run the full 22-phase methodology. Report verified findings only.",
                    },
                )
                if r.status_code in (200, 201):
                    try:
                        return r.json()
                    except json.JSONDecodeError:
                        return {"id": None}
            except Exception as e:  # noqa: BLE001
                logger.warning("Xalgorix scan start failed: %s", e)
        return None

    async def _poll_scan(self, base: str, scan_id: Optional[str], result: AdapterScanResult) -> None:
        deadline = time.time() + 3600
        async with httpx.AsyncClient(timeout=30) as client:
            while time.time() < deadline:
                await asyncio.sleep(15)
                try:
                    if scan_id:
                        r = await client.get(f"{base}/api/scans/{scan_id}")
                    else:
                        r = await client.get(f"{base}/api/scans")
                    if r.status_code != 200:
                        continue
                    data = r.json()
                    status = self._scan_status(data)
                    if status == "completed":
                        return
                    if status in ("failed", "error", "stopped"):
                        result.errors.append(f"Xalgorix scan ended with status: {status}")
                        return
                except Exception:  # noqa: BLE001
                    continue
        result.errors.append("Xalgorix scan did not finish within 60 minutes")

    @staticmethod
    def _scan_status(data: Any) -> str:
        if isinstance(data, dict):
            if data.get("status"):
                return str(data["status"]).lower()
            if isinstance(data.get("scans"), list) and data["scans"]:
                return str(data["scans"][0].get("status", "")).lower()
        return "running"

    async def _fetch_findings(self, base: str, target: str) -> list:
        findings = []
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                r = await client.get(f"{base}/api/findings")
                if r.status_code != 200:
                    return findings
                data = r.json()
            except Exception as e:  # noqa: BLE001
                logger.warning("Xalgorix findings fetch failed: %s", e)
                return findings

        items = data if isinstance(data, list) else data.get("findings", data.get("data", []))
        if isinstance(items, dict):
            items = items.get("items", [])
        for item in items if isinstance(items, list) else []:
            if not isinstance(item, dict):
                continue
            info = item.get("info", {}) if isinstance(item.get("info"), dict) else {}
            findings.append(self._new_finding(
                title=item.get("title") or info.get("name") or item.get("name") or "Xalgorix Finding",
                description=item.get("description") or info.get("description") or "",
                severity=item.get("severity", info.get("severity")),
                target=target,
                vulnerability_type=item.get("type") or item.get("category") or info.get("category"),
                remediation=item.get("remediation") or info.get("remediation"),
                reference=item.get("reference") or info.get("reference"),
                cve=item.get("cve") or info.get("cve"),
                cwe=item.get("cwe") or info.get("cwe"),
                payload=item.get("payload") or item.get("proof_of_concept") or item.get("poc"),
                cvss_score=self._to_float(item.get("cvss", item.get("cvss_score"))),
                confidence=item.get("verified", "confirmed") if item.get("verified") else "confirmed",
                details={
                    "evidence": item.get("evidence"),
                    "verified": item.get("verified"),
                    "steps": item.get("steps") or item.get("reproduction_steps"),
                },
            ))
        return findings[:50]

    @staticmethod
    def _to_float(value: Any) -> Optional[float]:
        try:
            if value is None:
                return None
            return float(value)
        except (TypeError, ValueError):
            return None
