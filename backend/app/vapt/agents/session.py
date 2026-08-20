"""
Session Acquisition Agent

Tries to obtain an authenticated session against the target (default
credentials on discovered login endpoints) so later exploitation probes
(XXE, IDOR, admin API, CSRF) run WITH a valid session instead of
unauthorized-only. Mirrors the manual step where a pentester logs in
with vendor default credentials before testing authenticated
functionality.

The acquired header (Bearer token or cookie) is stored per-scan in a
registry and attached to matrix probe commands. Findings never leak the
token - only the login endpoint + credential pair (which is exactly what
the customer needs to remediate).
"""

import asyncio
import json
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlsplit

from app.core.logging import get_logger
from app.vapt.agents.recon import remap_loopback_target

logger = get_logger(__name__)

# Default / vendor credential pairs (top of the ladder - cheap and legal
# to try on an authorized engagement; brute-force dictionaries belong to
# hydra which is already wired for that). Email-form defaults include
# common lab/demo domains; host-derived domains are appended at runtime.
DEFAULT_CREDS: List[tuple] = [
    ("admin", "admin"),
    ("admin", "password"),
    ("admin", "admin123"),
    ("admin", "administrator"),
    ("admin", "P@ssw0rd"),
    ("admin", "Password123"),
    ("root", "toor"),
    ("root", "root"),
    ("test", "test"),
    ("test", "test123"),
    ("user", "user"),
    ("guest", "guest"),
    ("admin@example.com", "admin"),
    ("admin@example.com", "admin123"),
    ("admin@demo.com", "demo123"),
    ("admin@test.com", "test"),
]

_EMAIL_SUFFIX_DOMAINS = ("juice-sh.op", "example.com", "demo.com", "test.com", "acme.test")

_LOGIN_PATH_RE = re.compile(
    r"(login|signin|sign-in|auth|session|token|authenticate|password)", re.IGNORECASE
)

# Common login endpoints tried even if the surface miner did not see them.
_COMMON_LOGIN_PATHS = [
    "/login", "/signin", "/api/login", "/api/auth/login", "/auth/login",
    "/rest/user/login", "/rest/auth/login", "/api/v1/auth/login", "/login/authenticate",
    "/user/login", "/api/user/login", "/account/login", "/identity/login",
]

_SESSION_TOKEN_RE = re.compile(
    r'"(?:token|access_token|jwt|session_token|id_token|authentication[^"]*)":\s*"([^"]{10,})"',
    re.IGNORECASE,
)

_session_registry: Dict[str, Dict[str, Any]] = {}


def get_session(scan_id: str) -> Optional[Dict[str, Any]]:
    """Return the acquired session for a scan, if any."""
    return _session_registry.get(scan_id)


async def try_acquire_session(
    base_url: str,
    endpoints: List[str],
    scan_id: str = "",
    timeout: float = 30.0,
) -> Optional[Dict[str, Any]]:
    """Attempt to authenticate against the target with default credentials.

    Returns ``None`` when no session could be established, else a dict::

        {
          "kind": "default-credentials",
          "endpoint": "/rest/user/login",
          "credential": "admin / admin123",
          "header": "Authorization: Bearer eyJ...",
          "evidence": "response snippet (token truncated)",
        }
    """
    import logging

    import httpx

    # Probe traffic is op-discipline bookkeeping, not application logs.
    logging.getLogger("httpx").setLevel(logging.WARNING)

    base = remap_loopback_target(base_url)

    # Candidate login endpoints: discovered hints first, common paths after.
    candidates: List[str] = []
    for ep in endpoints:
        if _LOGIN_PATH_RE.search(ep):
            candidates.append(ep)
    for p in _COMMON_LOGIN_PATHS:
        if p not in candidates:
            candidates.append(p)

    # Email-address forms for bare usernames: admin -> admin@<suffix>.
    host = re.sub(r":\d+$", "", (urlsplit(base).hostname or ""))
    creds: List[tuple] = []
    for email, password in DEFAULT_CREDS:
        creds.append((email, password))
        if "@" not in email:
            for suffix in _EMAIL_SUFFIX_DOMAINS:
                creds.append((f"{email}@{suffix}", password))
            if host:
                creds.append((f"{email}@{host}", password))

    headers = {"User-Agent": "Mozilla/5.0 AstraIX-VAPT/1.0"}

    async with httpx.AsyncClient(
        timeout=10.0, follow_redirects=True, verify=False, headers=headers
    ) as client:
        for endpoint in candidates[:6]:
            url = urljoin(base.rstrip("/") + "/", endpoint.lstrip("/"))
            for email, password in creds:
                bodies = [
                    {"email": email, "password": password},
                    {"username": email, "password": password},
                    {"user": email, "password": password},
                ]
                for body in bodies:
                    try:
                        async with client.stream(
                            "POST", url, json=body
                        ) as resp:
                            status = resp.status_code
                            set_cookie = resp.headers.get("set-cookie") or ""
                            body_text = await resp.aread()
                            body_snippet = body_text.decode("utf-8", errors="ignore")[:800]
                        if status >= 400:
                            continue
                    except Exception as e:
                        logger.debug("Session login probe %s failed: %s", url, e)
                        continue

                    # Form-encoded variant for classic HTML login forms.
                    if status >= 400 or "token" not in body_snippet.lower():
                        try:
                            r2 = await client.post(
                                url, data={"username": email, "password": password}
                            )
                            status = r2.status_code
                            set_cookie = r2.headers.get("set-cookie") or ""
                            body_snippet = r2.text[:800]
                        except Exception as e:
                            logger.debug("Session form probe %s failed: %s", url, e)
                            continue
                        if status >= 400:
                            continue

                    # Success indicators: session token / cookie / auth-zone redirect.
                    m = _SESSION_TOKEN_RE.search(body_snippet)
                    token = m.group(1) if m else None
                    has_cookie = bool(set_cookie)
                    if token:
                        header_value = f"Bearer {token[:300]}"
                    elif has_cookie:
                        header_value = set_cookie.split(";")[0]
                    else:
                        continue

                    session: Dict[str, Any] = {
                        "kind": "default-credentials",
                        "endpoint": endpoint,
                        "credential": f"{email} / {password}",
                        "header": f"Authorization: {header_value}"
                        if header_value.startswith("Bearer")
                        else f"Cookie: {header_value}",
                        "evidence": (
                            f"status {status}; token prefix {token[:12]}..."
                            if token
                            else f"status {status}; cookie set"
                        ),
                    }
                    if scan_id:
                        _session_registry[scan_id] = session
                    return session
    return None