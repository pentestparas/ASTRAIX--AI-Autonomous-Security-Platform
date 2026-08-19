import asyncio
import os
from typing import Any, Awaitable, Callable, Dict, List, Optional
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
                finding.confidence = "confirmed"
                finding.details["verification"] = "Confirmed via re-check"
                logger.info("Verifier: %s confirmed on %s", finding.title, target)
                kb_context = await self._kb_exploit_context(finding)
                if kb_context:
                    finding.details["kb_exploit_context"] = kb_context
        except Exception as e:
            finding.details["verification_error"] = str(e)
            logger.warning("Verifier: error checking %s: %s", finding.title, e)

        return finding

    async def _kb_exploit_context(self, finding: VAPTFinding) -> Optional[str]:
        """Best-effort lookup of exploitation/technique guidance in the
        knowledge base for a confirmed finding. Runs KB search off the event
        loop; never fails the verification step."""
        return await asyncio.to_thread(self._kb_exploit_sync, finding)

    def _kb_exploit_sync(self, finding: VAPTFinding) -> Optional[str]:
        try:
            from app.vapt.agents.kb import search_kb, sanitize_finding_query, apply_finding_relevance_floor

            query = sanitize_finding_query(finding.title)
            if finding.tool_name:
                query = f"{query} {finding.tool_name}".strip()
            if not query:
                return None
            hits = apply_finding_relevance_floor(
                search_kb(f"{query} exploit technique CVE", top_k=3)
            )
            if hits:
                return " | ".join(
                    str(h.get("source", "") or h.get("title", "")) for h in hits
                )
        except Exception:
            pass
        return None

    async def verify_findings(
        self,
        findings: List[VAPTFinding],
        scan_id: Optional[str] = None,
        publish: Optional[Callable[[str, str, Dict[str, Any]], Awaitable[None]]] = None,
    ) -> List[VAPTFinding]:
        """Verify findings concurrently (bounded) so long-running re-exploits
        (e.g. sqlmap) do not stall the scan for minutes.

        Only HIGH/CRITICAL findings are re-exploited, and duplicate
        (title, target) findings are verified once. This keeps the total
        verification time in the low minutes instead of tens of minutes.

        When a ``publish`` callback and ``scan_id`` are provided, every
        verdict is emitted as a live ``verdict`` event so the scan console
        can show the AI's per-finding decision (confirmed / downgraded).
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
            severity_before = finding.severity.value
            confidence_before = finding.confidence
            async with sem:
                try:
                    res = await asyncio.wait_for(self.verify_finding(finding), timeout=cap)
                except asyncio.TimeoutError:
                    finding.details["verification"] = "Timed out during re-check"
                    res = finding
                if seq % 5 == 0:
                    logger.info("Verifier progress: %d/%d", seq + 1, len(to_verify))
            if publish and scan_id:
                await publish(scan_id, "verdict", self._verdict_event(
                    res, severity_before, confidence_before
                ))
            return res

        await asyncio.gather(*(bounded(f, i) for i, f in enumerate(to_verify)))
        return findings

    def _verdict_event(
        self,
        finding: VAPTFinding,
        severity_before: str,
        confidence_before: str,
    ) -> Dict[str, Any]:
        detail = (
            finding.details.get("verification")
            or finding.details.get("verification_error")
            or ""
        )
        if finding.confidence == "confirmed":
            verdict = "confirmed"
        elif confidence_before != "unverified" and finding.confidence == "unverified":
            verdict = "downgraded"
        elif "Timed out" in str(detail):
            verdict = "timed_out"
        else:
            verdict = "unverified"
        return {
            "finding": finding.title[:160],
            "vulnerability_type": finding.vulnerability_type or "",
            "tool": self._pick_verify_tool(finding) or "",
            "verdict": verdict,
            "severity_before": severity_before,
            "severity_after": finding.severity.value,
            "confidence": finding.confidence,
            "detail": str(detail)[:300],
            "kb_context": (finding.details.get("kb_exploit_context") or "")[:300],
        }

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
