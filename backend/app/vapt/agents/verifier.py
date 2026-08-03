import asyncio
import os
from typing import List, Optional
from app.vapt.models import VAPTFinding, VAPTSeverity, VAPTTarget, VAPTScanRequest, VAPTScanType
from app.vapt.executor import get_vapt_executor
from app.core.logging import get_logger

logger = get_logger(__name__)


class VerifierAgent:
    def __init__(self):
        self.executor = get_vapt_executor()

    async def verify_finding(self, finding: VAPTFinding) -> VAPTFinding:
        if finding.confidence == "unverified":
            return finding

        target = finding.target or finding.host
        if not target:
            return finding

        tool_id = self._pick_verify_tool(finding)
        if tool_id is None:
            return finding

        try:
            raw = await asyncio.to_thread(
                self.executor.run_tool_sync, tool_id, target, timeout=60
            )
            if not raw or len(raw.strip()) < 10:
                finding.confidence = "unverified"
                finding.severity = self._downgrade_severity(finding.severity)
                finding.details["verification"] = "Could not reproduce"
                logger.info("Verifier: %s not reproducible on %s", finding.title, target)
            else:
                finding.details["verification"] = "Confirmed via re-check"
                logger.info("Verifier: %s confirmed on %s", finding.title, target)
        except Exception as e:
            finding.details["verification_error"] = str(e)
            logger.warning("Verifier: error checking %s: %s", finding.title, e)

        return finding

    async def verify_findings(self, findings: List[VAPTFinding]) -> List[VAPTFinding]:
        """Verify findings concurrently (bounded) so long-running re-exploits
        (e.g. sqlmap) do not stall the scan for minutes.

        Only HIGH/CRITICAL findings are re-exploited, and duplicate
        (title, target) findings are verified once. This keeps the total
        verification time in the low minutes instead of tens of minutes.
        """
        if not findings:
            return findings

        seen = set()
        to_verify: List[VAPTFinding] = []
        for f in findings:
            if f.confidence == "unverified":
                continue
            key = (f.title, f.target or f.host)
            if key in seen:
                continue
            seen.add(key)
            if f.severity not in (VAPTSeverity.HIGH, VAPTSeverity.CRITICAL):
                continue
            to_verify.append(f)

        if not to_verify:
            return findings

        sem = asyncio.Semaphore(3)
        cap = int(os.environ.get("VAPT_VERIFY_TIMEOUT", "75"))

        async def bounded(finding: VAPTFinding, seq: int) -> VAPTFinding:
            async with sem:
                try:
                    res = await asyncio.wait_for(self.verify_finding(finding), timeout=cap)
                except asyncio.TimeoutError:
                    finding.details["verification"] = "Timed out during re-check"
                    res = finding
                if seq % 5 == 0:
                    logger.info("Verifier progress: %d/%d", seq + 1, len(to_verify))
                return res

        await asyncio.gather(*(bounded(f, i) for i, f in enumerate(to_verify)))
        return findings

    def _pick_verify_tool(self, finding: VAPTFinding) -> Optional[str]:
        title_lower = finding.title.lower()
        if "sql" in title_lower or "sql injection" in title_lower:
            return "sqlmap"
        if "xss" in title_lower or "cross-site" in title_lower:
            return "nuclei"
        if "open port" in title_lower:
            return "nmap"
        if "ssl" in title_lower or "tls" in title_lower or "certificate" in title_lower:
            return "sslscan"
        if "dir" in title_lower or "directory" in title_lower:
            return "gobuster"
        if finding.port and finding.service:
            return "nmap"
        return None

    def _downgrade_severity(self, severity: VAPTSeverity) -> VAPTSeverity:
        mapping = {
            VAPTSeverity.CRITICAL: VAPTSeverity.HIGH,
            VAPTSeverity.HIGH: VAPTSeverity.MEDIUM,
            VAPTSeverity.MEDIUM: VAPTSeverity.LOW,
            VAPTSeverity.LOW: VAPTSeverity.INFO,
            VAPTSeverity.INFO: VAPTSeverity.INFO,
        }
        return mapping.get(severity, severity)
