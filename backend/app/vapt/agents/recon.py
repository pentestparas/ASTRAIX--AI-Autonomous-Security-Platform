"""
Web Surface Miner (recon)

Mines the target's HTML + JS bundles to extract the API/application
endpoint surface (/rest/..., /api/..., websockets, absolute URLs) before
the test-matrix agent plans exploitation. Mirrors the manual bundle
mining step of a full engagement so the LLM matrix is grounded in the
REAL endpoints of the target instead of generic guesses.

CPU-bound HTTP is delegated to a thread; total time is bounded.
"""

import asyncio
import json
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse, urljoin

from app.core.logging import get_logger

logger = get_logger(__name__)

_SCRIPT_SRC_RE = re.compile(r'<script[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
_ENDPOINT_RE = re.compile(r'["\'`]((?:/(?:rest|api|chat|ws|socket\.io|admin|graphql)[a-zA-Z0-9_\-/{}.:?=&]*))["\'`]')
_HINT_RE = re.compile(r'(webpack|angular|react|vue|next|express|django|rails|flask|nuxt|svelte|vite|socket\.io)',
                      re.IGNORECASE)

# Bundle files commonly referenced by SPAs (Angular-style hashed names
# fall back to a full scrape of <script src> from the index).
COMMON_BUNDLES = ["main.js", "runtime.js", "polyfills.js", "vendor.js", "app.js", "index.js"]


def _fetch_text(url: str, timeout: float = 8.0) -> Optional[str]:
    import httpx

    try:
        resp = httpx.get(url, timeout=timeout, follow_redirects=True, verify=False)
        if resp.status_code == 200:
            ctype = resp.headers.get("content-type", "")
            if "javascript" in ctype or "html" in ctype or not ctype:
                return resp.text[:2_000_000]
    except Exception as e:
        logger.warning("Surface miner fetch failed for %s: %s", url, e)
    return None


def _mine_text(text: str, base_url: str) -> Dict[str, Any]:
    endpoints: List[str] = []
    for m in _ENDPOINT_RE.finditer(text or ""):
        ep = m.group(1)
        if ep not in endpoints:
            endpoints.append(ep)
    hints = sorted(set(_HINT_RE.findall((text or "").lower())))
    return {"endpoints": endpoints, "hints": hints}


async def mine_web_surface(target: str, timeout: float = 25.0) -> Dict[str, Any]:
    """Fetch the target index + JS bundles and return the mined surface.

    Returns::

        {
          "base_url": target,
          "scripts": ["/main.js", ...],
          "endpoints": ["/rest/products/search", ...],
          "hints": ["webpack", "angular"],
        }
    """
    parsed = urlparse(target if "://" in target else f"http://{target}")
    base = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else target

    scripts: List[str] = []
    index_text = await asyncio.to_thread(_fetch_text, base, 8.0)
    if index_text:
        for m in _SCRIPT_SRC_RE.finditer(index_text):
            src = m.group(1)
            full = urljoin(base, src)
            if full not in scripts:
                scripts.append(full)
        for b in COMMON_BUNDLES:
            if not any(s.endswith(b) for s in scripts):
                scripts.append(urljoin(base, b))

    if not scripts:
        scripts = [urljoin(base, b) for b in COMMON_BUNDLES]

    all_endpoints: List[str] = []
    all_hints: List[str] = []
    tasks = [asyncio.to_thread(_fetch_text, s, 6.0) for s in scripts[:8]]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for text in results:
        if isinstance(text, str):
            mined = _mine_text(text, base)
            all_endpoints.extend(mined["endpoints"])
            all_hints.extend(mined["hints"])

    seen = set()
    dedup = []
    for ep in all_endpoints:
        if ep not in seen:
            seen.add(ep)
            dedup.append(ep)

    return {
        "base_url": base,
        "scripts": scripts,
        "endpoints": dedup[:80],
        "hints": sorted(set(all_hints))[:20],
        "endpoint_count": len(dedup),
    }


async def summarize_surface(target: str, timeout: float = 25.0) -> str:
    """Short human/LLM-readable summary of the mined surface."""
    surface = await mine_web_surface(target, timeout=timeout)
    lines = [f"Base URL: {surface['base_url']}"]
    if surface["hints"]:
        lines.append("Tech hints: " + ", ".join(surface["hints"]))
    lines.append(f"Endpoints ({surface['endpoint_count']}): " + ", ".join(surface["endpoints"][:40]))
    return "\n".join(lines)
