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

def remap_loopback_target(target: str) -> str:
    """Map loopback targets to the Docker gateway host.

    The backend runs inside Docker where 'localhost' / '127.0.0.1'
    points at the container itself, not the host. Rewrite loopback
    hosts to host.docker.internal so host-published services (e.g.
    localhost:3002) are reachable from in-container HTTP fetches and
    tool containers alike.
    """
    loopback = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "[::1]"}
    scheme, _, after = target.partition("://")
    if after:
        hostport, _, path = after.partition("/")
    else:
        scheme = ""
        hostport, _, path = target.partition("/")
    h, _, p = hostport.rpartition(":")
    host = h if (h and p.isdigit()) else hostport
    if host in loopback:
        new = f"host.docker.internal:{p}" if (h and p.isdigit()) else "host.docker.internal"
        resolved = f"{scheme}://{new}" if scheme else new
        if path:
            resolved = f"{resolved}/{path}"
        return resolved
    return target


_SCRIPT_SRC_RE = re.compile(r'<script[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
# Route tokens appear BOTH as string literals ('/rest/basket/X') and as
# template-literal fragments (`${hostServer}/rest/basket/${e}`) in bundles.
# The token itself (rest/api/b2b/...) is distinctive enough to extract
# without requiring a leading quote.
_ENDPOINT_RE = re.compile(r'/(?:rest|api|b2b|v2|chat|ws|socket\.io|admin|graphql)[a-zA-Z0-9_\-/{}.:?=&]*')
_HINT_RE = re.compile(r'(webpack|angular|react|vue|next|express|django|rails|flask|nuxt|svelte|vite|socket\.io)',
                      re.IGNORECASE)
# SPA route tables chunk the app: lazy modules (basket, checkout, admin...)
# are hashed chunk files NOT linked from index.html but referenced inside
# the bootstrap bundle as module.loadChildren / dynamic import specifiers.
_LAZY_CHUNK_RE = re.compile(r'["\']([a-zA-Z0-9_.-]+\.js)["\']')

# Bundle files commonly referenced by SPAs (Angular-style hashed names
# fall back to a full scrape of <script src> from the index).
COMMON_BUNDLES = ["main.js", "runtime.js", "polyfills.js", "vendor.js", "app.js", "index.js"]

# Discovery documents that expose the full route table of an app without
# any guest interaction (OpenAPI/Swagger specs, framework docs).
DISCOVERY_DOCS = [
    "/openapi.json",
    "/api-docs/swagger.json",
    "/swagger.json",
    "/api/swagger.json",
    "/api-docs.json",
    "/api/v1/openapi.json",
    "/api-docs",
    "/swagger-ui/index.html?url=/swagger.json",
    "/docs",
    "/redoc",
    "/openapi.yaml",
    "/api/swagger.yaml",
]

_OPENAPI_PATH_RE = re.compile(r'^\s*/[a-zA-Z0-9_\-/{}.:]+:\s*$', re.MULTILINE)


def _mine_openapi_doc(text: str, base_url: str) -> List[str]:
    """Extract route paths from an OpenAPI/Swagger JSON or YAML doc."""
    found: List[str] = []
    try:
        data = json.loads(text)
        paths = (data or {}).get("paths") or {}
        for path in paths:
            if path.startswith("/") and path not in found:
                found.append(path)
    except (json.JSONDecodeError, TypeError, AttributeError):
        # YAML fallback: strip comments/formatting and keep path stanzas.
        fallback = re.sub(r"(?m)^\s*#.*$", "", text)
        for m in _OPENAPI_PATH_RE.finditer(fallback or ""):
            p = m.group(0).strip().rstrip(":")
            if p.startswith("/") and p not in found:
                found.append(p)
    # Never let a discovery doc exceed the budget - sample generously.
    return found[:60]


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
        ep = m.group(0)
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
    target = remap_loopback_target(target)
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
    if index_text:
        mined = _mine_text(index_text, base)
        all_endpoints.extend(mined["endpoints"])
        all_hints.extend(mined["hints"])

    # Discovery documents: OpenAPI/Swagger specs are the highest-signal
    # hidden-route source for modern apps (SPAs ship them even when no UI
    # links to them).
    doc_tasks = [
        asyncio.to_thread(_fetch_text, urljoin(base, doc), 5.0)
        for doc in DISCOVERY_DOCS
    ]
    doc_results = await asyncio.gather(*doc_tasks, return_exceptions=True)
    for text in doc_results:
        if isinstance(text, str) and len(text) > 80:
            all_endpoints.extend(_mine_openapi_doc(text, base))

    # Fetch the bootstrap bundle(s) FIRST, then chase lazy chunk references:
    # route tables for basket/checkout/admin/faucet modules live in those
    # hashed chunks, not in index.html.
    chunk_scripts: List[str] = []
    tasks = [asyncio.to_thread(_fetch_text, s, 6.0) for s in scripts[:8]]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for text in results:
        if isinstance(text, str):
            mined = _mine_text(text, base)
            all_endpoints.extend(mined["endpoints"])
            all_hints.extend(mined["hints"])
            for m in _LAZY_CHUNK_RE.finditer(text):
                name = m.group(1)
                if name in ("main.js", "runtime.js", "polyfills.js", "vendor.js") or ".js" not in name:
                    continue
                full = urljoin(base, name)
                if full not in scripts and full not in chunk_scripts:
                    chunk_scripts.append(full)

    if chunk_scripts:
        chunk_results = await asyncio.gather(
            *[asyncio.to_thread(_fetch_text, s, 5.0) for s in chunk_scripts[:12]],
            return_exceptions=True,
        )
        for text in chunk_results:
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
        "endpoints": dedup[:120],
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
