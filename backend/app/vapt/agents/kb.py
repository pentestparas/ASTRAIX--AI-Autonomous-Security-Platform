"""
Shared knowledge-base client for the whole VAPT AI pipeline.

The AstraIX cybersecurity KB (FAISS semantic + TF-IDF search over 34k+
chunks from 3k+ sources) grounds every AI stage - target analysis,
planning, the autonomous agent loop, research enrichment, verification,
risk scoring and the executive summary - so all decisions cite the same
KB evidence.

Search is CPU-bound and blocks the event loop; async callers MUST wrap
these helpers in ``asyncio.to_thread``.
"""

import re
import sys
import threading
from typing import Any, Dict, List, Optional

from app.core.logging import get_logger

logger = get_logger(__name__)

KB_PATH = "/app/knowledge-base"

# FAISS returns normalized cosine similarity (bge-small-en-v1.5). Observed
# calibration on 34k chunks: genuine vulnerability matches score >= 0.78,
# while lexical/query-poisoning hits (e.g. a hostname token like "docker"
# dragging in container-hardening docs for a web finding) score ~0.71-0.75.
# Only enforced when semantic search is active; TF-IDF fallback scores are
# unbounded term-frequency sums, so no floor applies there.
FINDING_RELEVANCE_FLOOR = 0.78

# Finding titles/descriptions embed raw target strings (http://host:port/path).
# Those tokens poison KB matching (the "docker" in host.docker.internal is
# lexically identical to Docker-container keywords). Strip URL / host / IP /
# port fragments before composing any KB query derived from finding text.
_URL_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s]+")
_HOST_RE = re.compile(r"(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d{1,5})?(?:/[^\s]*)?")
_LOCALHOST_RE = re.compile(r"localhost(?::\d{1,5})?(?:/[^\s]*)?")
_IP_RE = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})?(?:/[^\s]*)?")
_PORT_RE = re.compile(r"(?<![\w.]):\d{1,5}\b")
_NON_WORD_RE = re.compile(r"[^a-zA-Z0-9 ]+")

_lock = threading.Lock()
_kb: Any = None
_kb_tried = False


def sanitize_finding_query(title: str, description: str = "", vuln_type: str = "") -> str:
    """Reduce finding text to KB-safe query tokens.

    Strips scheme://URLs, bare hostnames (FQDN, ``localhost``, IP:port) and
    stray ports so target strings cannot dominate or poison TF-IDF/FAISS
    matching, then collapses interpunctured fragments to whitespace-separated
    words. Returns an empty string when nothing meaningful remains.
    """
    parts = [title or "", (description or "")[:200], vuln_type or ""]
    text = " ".join(parts)
    text = _URL_RE.sub(" ", text)
    text = _HOST_RE.sub(" ", text)
    text = _LOCALHOST_RE.sub(" ", text)
    text = _IP_RE.sub(" ", text)
    text = _PORT_RE.sub(" ", text)
    text = _NON_WORD_RE.sub(" ", text)
    return " ".join(text.split())


def is_semantic_kb() -> bool:
    """True when the loaded KB serves FAISS cosine relevance scores."""
    kb = get_kb()
    if not kb:
        return False
    try:
        return bool(kb.stats().get("semantic_search"))
    except Exception:
        return False


def apply_finding_relevance_floor(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Drop matches below the calibrated floor (FAISS only).

    TF-IDF fallback relevance values are raw score sums and incomparable, so
    when semantic search is unavailable the list passes through unchanged.
    """
    if not is_semantic_kb():
        return results
    return [
        r for r in results
        if float(r.get("relevance", 0) or 0) >= FINDING_RELEVANCE_FLOOR
    ]


def get_kb() -> Any:
    """Lazily load the KB search index exactly once (thread-safe)."""
    global _kb, _kb_tried
    if _kb_tried:
        return _kb
    with _lock:
        if _kb_tried:
            return _kb
        try:
            if KB_PATH not in sys.path:
                sys.path.insert(0, KB_PATH)
            from search import get_knowledge_base

            _kb = get_knowledge_base()
            logger.info("KB client ready: %s", _kb.stats())
        except Exception as e:
            _kb = None
            logger.warning("KB client unavailable: %s", e)
        _kb_tried = True
        return _kb


def kb_ready() -> bool:
    return get_kb() is not None


def kb_stats() -> Optional[Dict[str, Any]]:
    kb = get_kb()
    if not kb:
        return None
    try:
        return kb.stats()
    except Exception as e:
        logger.warning("KB stats failed: %s", e)
        return None


def search_kb(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Raw KB search results (title/source/text/relevance)."""
    kb = get_kb()
    if not kb:
        return []
    try:
        return kb.search(query, top_k=top_k)
    except Exception as e:
        logger.warning("KB search failed: %s", e)
        return []


def kb_snippets(query: str, top_k: int = 3, max_len: int = 220) -> List[str]:
    """Formatted KB snippets, e.g. ``[source/title] text``, for prompts."""
    snippets = []
    for r in search_kb(query, top_k=top_k):
        title = r.get("title") or r.get("source") or "source"
        text = (r.get("text") or r.get("content") or r.get("snippet") or "")[:max_len]
        if text:
            snippets.append(f"[{title}] {text}")
    return snippets


def kb_sources_for(query: str, top_k: int = 3) -> List[str]:
    """Distinct source paths returned for a query."""
    return list(dict.fromkeys(str(r.get("source", "")) for r in search_kb(query, top_k=top_k) if r.get("source")))


def kb_context_for_finding(
    title: str,
    description: str,
    vuln_type: str = "",
    severity: str = "",
    top_k: int = 2,
) -> List[Dict[str, Any]]:
    """KB evidence search for a single finding (used by risk engine).

    Info-level discovery findings carry no CVE/exploitation signal, so they
    are skipped entirely. Query text is sanitized of target URLs/hostnames to
    keep lexical tokens from poisoning the match, and hits below the semantic
    relevance floor are discarded.
    """
    if severity and severity.lower() in ("info", "informational"):
        return []
    query = sanitize_finding_query(title, description, vuln_type)
    if not query:
        return []
    query = f"{query} CVSS CVE exploit"
    results = search_kb(query, top_k=top_k)
    return apply_finding_relevance_floor(results)
