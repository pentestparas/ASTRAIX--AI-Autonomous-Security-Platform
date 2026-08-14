import asyncio
from typing import List
from app.vapt.models import VAPTFinding
from app.vapt.agents.kb import (
    get_kb,
    apply_finding_relevance_floor,
    sanitize_finding_query,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


class ResearcherAgent:
    async def enrich_findings(self, findings: List[VAPTFinding]) -> List[VAPTFinding]:
        # KB search is CPU-bound (TF-IDF over 30k+ chunks) and would block the
        # event loop (and defeat asyncio.wait_for timeouts) if awaited inline.
        return await asyncio.to_thread(self._enrich_sync, findings)

    def _enrich_sync(self, findings: List[VAPTFinding]) -> List[VAPTFinding]:
        enriched = []
        for f in findings:
            enriched.append(self._enrich_one(f))
        return enriched

    def _enrich_one(self, finding: VAPTFinding) -> VAPTFinding:
        kb = get_kb()
        if kb is None:
            return finding

        # Discovery noise (endpoint enumeration, tech fingerprinting) carries
        # no CVE/exploitation signal and only drags in unrelated sources.
        if finding.severity is not None and finding.severity.value in ("info", "informational"):
            return finding

        query = sanitize_finding_query(
            finding.title, finding.description or "", finding.vulnerability_type or ""
        )
        if not query:
            return finding
        results = apply_finding_relevance_floor(kb.search(query, top_k=3))
        if not results:
            return finding

        context_parts = []
        cves = set()
        for r in results:
            text = r["text"][:500]
            context_parts.append(f"[{r['source']}] {text}")
            cve_matches = self._extract_cves(text)
            cves.update(cve_matches)

        context = "\n\n".join(context_parts)
        finding.details["kb_context"] = context
        finding.details["kb_sources"] = list(set(r["source"] for r in results))

        if cves:
            finding.details["related_cves"] = sorted(cves)
            finding.cve = list(cves)[0]

        return finding

    def _extract_cves(self, text: str) -> List[str]:
        import re
        return re.findall(r"CVE-\d{4}-\d{4,7}", text, re.IGNORECASE)
