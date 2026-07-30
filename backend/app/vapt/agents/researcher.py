import os
import sys
from typing import List, Optional
from app.vapt.models import VAPTFinding
from app.core.logging import get_logger

logger = get_logger(__name__)

KB_PATH = "/app/knowledge-base"
_kb = None


def _load_kb():
    global _kb
    if _kb is not None:
        return
    try:
        sys.path.insert(0, KB_PATH)
        from search import get_knowledge_base
        _kb = get_knowledge_base()
        logger.info("ResearcherAgent: knowledge base loaded (%s sources)", _kb.stats()["total_sources"])
    except Exception as e:
        logger.warning("ResearcherAgent: knowledge base unavailable: %s", e)


class ResearcherAgent:
    def __init__(self):
        _load_kb()

    async def enrich_finding(self, finding: VAPTFinding) -> VAPTFinding:
        if _kb is None:
            return finding

        query = f"{finding.title} {finding.description[:200]} {finding.vulnerability_type or ''}"
        results = _kb.search(query, top_k=3)
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

    async def enrich_findings(self, findings: List[VAPTFinding]) -> List[VAPTFinding]:
        enriched = []
        for f in findings:
            enriched.append(await self.enrich_finding(f))
        return enriched

    def _extract_cves(self, text: str) -> List[str]:
        import re
        return re.findall(r"CVE-\d{4}-\d{4,7}", text, re.IGNORECASE)
