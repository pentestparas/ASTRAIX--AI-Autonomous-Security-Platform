#!/usr/bin/env python3
"""API / endpoint surface discovery scanner for the VAPT executor.

Probes a curated list of REST API endpoints and hidden paths on the target
(common REST patterns plus OWASP Juice Shop's complete route map extracted
from the application build) and reports every reachable endpoint. Sensitive
endpoints (admin, user data, file servers, order history) are flagged with
higher severity since they expand the attack surface.

Emits findings as JSON Lines on stdout:

    {"title": "...", "description": "...", "severity": "medium",
     "path": "...", "evidence": "...", "category": "API01",
     "remediation": "...", "reference": "...", "cwe": "..."}

Usage: api_surface_scanner.py <base_url>
"""
import json
import re
import sys
import urllib.error
import urllib.request

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost"
TIMEOUT = 15
UA = {"User-Agent": "astraix-vapt-scanner"}

# ---------------------------------------------------------------------------
# Endpoint wordlist: generic REST resource paths + OWASP Juice Shop route map
# (extracted from lib/server.ts app.use/app.get/app.post/... registrations).
# ":param" placeholders are expanded below.
# ---------------------------------------------------------------------------
JUICESHOP_ROUTES = [
    "/api/Users", "/api/Users/:id",
    "/api/Products", "/api/Products/:id",
    "/api/Challenges", "/api/Challenges/:id",
    "/api/Hints", "/api/Hints/:id",
    "/api/Complaints", "/api/Complaints/:id",
    "/api/Recycles", "/api/Recycles/:id",
    "/api/SecurityQuestions", "/api/SecurityQuestions/:id",
    "/api/SecurityAnswers", "/api/SecurityAnswers/:id",
    "/api/Feedbacks", "/api/Feedbacks/:id",
    "/api/BasketItems", "/api/BasketItems/:id",
    "/api/Quantitys", "/api/Quantitys/:id",
    "/api/Cards", "/api/Cards/:id",
    "/api/PrivacyRequests", "/api/PrivacyRequests/:id",
    "/api/Addresss", "/api/Addresss/:id",
    "/api/Deliverys", "/api/Deliverys/:id",
    "/b2b/v2", "/b2b/v2/orders",
    "/rest/2fa/verify", "/rest/2fa/status", "/rest/2fa/setup", "/rest/2fa/disable",
    "/rest/user/login", "/rest/user/change-password", "/rest/user/reset-password",
    "/rest/user/security-question", "/rest/user/whoami", "/rest/user/authentication-details",
    "/rest/user/data-export",
    "/rest/products/search", "/rest/products/reviews",
    "/rest/products/:id/reviews",
    "/rest/basket", "/rest/basket/:id", "/rest/basket/:id/checkout",
    "/rest/basket/:id/coupon/:coupon", "/rest/basket/:id/order",
    "/rest/admin/application-version", "/rest/admin/application-configuration",
    "/rest/repeat-notification", "/rest/continue-code", "/rest/continue-code-findIt",
    "/rest/continue-code-fixIt", "/rest/continue-code/apply/:continueCode",
    "/rest/continue-code-findIt/apply/:continueCode", "/rest/continue-code-fixIt/apply/:continueCode",
    "/rest/captcha", "/rest/image-captcha", "/rest/track-order/:id",
    "/rest/country-mapping", "/rest/saveLoginIp", "/rest/languages",
    "/rest/order-history", "/rest/order-history/orders",
    "/rest/order-history/:id/delivery-status",
    "/rest/wallet/balance", "/rest/deluxe-membership", "/rest/memories",
    "/rest/chat",
    "/rest/web3/submitKey", "/rest/web3/nftUnlocked", "/rest/web3/nftMintListen",
    "/rest/web3/walletNFTVerify", "/rest/web3/walletExploitAddress",
    "/ftp", "/ftp/acquisitions.md", "/ftp/legal.md",
    "/ftp/quarantine", "/ftp/quarantine/:file",
    "/profile", "/profile/image/file", "/profile/image/url",
    "/file-upload", "/redirect", "/promotion", "/video",
    "/metrics", "/api-docs", "/api-docs/", "/swagger.json", "/swagger.yaml",
    "/.well-known/security.txt", "/security.txt", "/robots.txt", "/sitemap.xml",
    "/encryptionkeys", "/encryptionkeys/:file",
    "/support/logs", "/support/logs/:file",
    "/assets/i18n/de.json", "/assets/i18n/en.json",
    "/snippets/:challenge", "/snippets/verdict", "/snippets/fixes",
    "/solve/challenges/server-side",
    "/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg",
    "/this/page/is/hidden/behind/an/incredibly/high/paywall/that/could/only/be/unlocked/by/sending/1btc/to/us",
    "/we/may/also/instruct/you/to/refuse/all/reasonably/necessary/responsibility",
]

# Generic REST API surface (any web framework).
GENERIC_ENDPOINTS = [
    "/api", "/api/", "/api/v1", "/api/v2", "/api/v3",
    "/api/health", "/api/status", "/api/version", "/api/healthz", "/api/ping",
    "/api/users", "/api/user", "/api/users/me", "/api/me", "/api/profile",
    "/api/login", "/api/auth", "/api/auth/login", "/api/auth/token",
    "/api/register", "/api/signup", "/api/logout", "/api/session",
    "/api/tokens", "/api/refresh", "/api/verify",
    "/api/admin", "/api/admin/users", "/api/admin/config", "/api/admin/settings",
    "/api/orders", "/api/orders/1", "/api/payments", "/api/billing",
    "/api/products", "/api/items", "/api/inventory", "/api/catalog",
    "/api/search", "/api/upload", "/api/files", "/api/download",
    "/api/config", "/api/settings", "/api/preferences",
    "/api/notifications", "/api/messages", "/api/reviews", "/api/comments",
    "/api/feedbacks", "/api/feedback", "/api/support", "/api/tickets",
    "/api/coupons", "/api/codes", "/api/rewards", "/api/bonuses",
    "/api/wallet", "/api/balance", "/api/transactions",
    "/api/logs", "/api/debug", "/api/internal", "/api/private",
    "/api/webhook", "/api/webhooks", "/api/export", "/api/import",
    "/api/swagger", "/api/docs", "/api/openapi.json",
    "/actuator", "/actuator/health", "/actuator/env", "/actuator/beans",
    "/actuator/mappings", "/actuator/threaddump", "/actuator/heapdump",
    "/v1", "/v2", "/v3", "/graphql", "/graphiql", "/gql",
    "/rest", "/rest/v1", "/rest/v2",
    "/admin", "/admin/", "/admin/login", "/admin/dashboard", "/admin/users",
    "/console", "/manager", "/manage", "/dashboard", "/status",
    "/debug", "/internal", "/private", "/secret", "/backup", "/uploads",
    "/downloads", "/files", "/static", "/public", "/assets", "/images",
    "/config.json", "/package.json", "/.env", "/.git/config", "/.git/HEAD",
    "/backup.zip", "/dump.sql", "/database.sql", "/db.sqlite3",
    "/server-status", "/server-info", "/phpinfo.php", "/info.php",
    "/health", "/healthz", "/readyz", "/version", "/info", "/env",
    "/metrics", "/prometheus", "/debug/pprof/", "/trace", "/profiler",
    "/swagger-ui", "/swagger-ui.html", "/api-docs/swagger.json",
    "/openapi.json", "/redoc", "/favicon.ico",
]

# Route path parameters to expand (kept small and safe).
SAMPLE_IDS = ["1", "2", "3", "4", "5", "1000"]

# Sensitive endpoints get a higher severity because they expand attack surface.
SENSITIVE_MARKERS = [
    "/admin", "/users", "/user", "/password", "/2fa", "/token", "/auth",
    "/data-export", "/authentication", "/secret", "/security",
    "/config", "/env", "/actuator", "/console", "/manager",
    "/backup", "/dump", "/upload", "/ftp", "/encryptionkeys",
    "/logs", "/wallet", "/balance", "/order-history", "/payments",
    "/web3", "/key", "/private", "/internal",
]


def expand(path):
    """Replace :param tokens with sample values."""
    if ":" not in path:
        return [path]
    parts = path.split("/")
    results = [[]]
    for part in parts:
        if part.startswith(":"):
            results = [r + [sid] for r in results for sid in SAMPLE_IDS[:2]]
        else:
            results = [r + [part] for r in results]
    return ["/".join(r) for r in results]


def http(path, method="GET", data=None):
    url = BASE + path
    headers = {**UA}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, method=method, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read().decode("utf-8", "ignore")
            return r.status, body[:2000]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        return e.code, body[:2000]
    except Exception as e:
        return 0, str(e)


def is_content(body):
    """Heuristic: non-trivial body content that is not the SPA shell."""
    if not body or len(body) < 40:
        return False
    stripped = body.strip()
    if stripped in ("{}", "[]", "null", "true", "false", "Not Found", "Not found", "404"):
        return False
    if stripped.lower().startswith(("<html", "<!doctype html")):
        return False
    return True


def severity_for(path):
    low = path.count("/") <= 2
    return "info" if low else "medium"


def main():
    seen = set()
    found = []

    # SPA fallback fingerprint: single-page apps answer HTTP 200 with the same
    # index.html shell for every unknown route. Sniff it once and treat any
    # equal response as a 404-equivalent (path not actually served).
    _, index_body = http("/")
    index_sig = re.sub(r"\s+", " ", index_body or "").strip()

    routes = sorted(set(JUICESHOP_ROUTES) | set(GENERIC_ENDPOINTS))
    for route in routes:
        for path in expand(route):
            if path in seen:
                continue
            seen.add(path)
            st, body = http(path)
            if st == 0 or st in (404, 405):
                continue
            if st in (401, 403):
                found.append({
                    "path": path,
                    "status": st,
                    "auth_required": True,
                    "body": "",
                })
                continue
            if not is_content(body):
                continue
            sig = re.sub(r"\s+", " ", body or "").strip()
            if index_sig and (sig == index_sig or sig.startswith(index_sig[:80])):
                continue
            sensitive = any(m in path for m in SENSITIVE_MARKERS)
            found.append({
                "path": path,
                "status": st,
                "auth_required": False,
                "body": body[:200],
                "sensitive": sensitive,
            })

    if not found:
        print(json.dumps({
            "title": "API Endpoint Discovery - No Exposed Endpoints Found",
            "description": f"No reachable API endpoints were found on {BASE} "
                           f"across {len(seen)} probed paths.",
            "severity": "info",
            "path": BASE,
            "evidence": f"{len(seen)} paths probed; none returned content",
            "category": "API01",
            "remediation": "Ensure all API endpoints require authentication and are rate limited.",
            "reference": "https://owasp.org/API-Security/editions/2023/en/0x11-t10/",
            "cwe": "CWE-200",
        }))
        return

    # One summary finding per reachable endpoint (keeps findings list readable).
    for f in found:
        severity = "medium" if f.get("sensitive") else "info"
        if f.get("auth_required"):
            title = "API Endpoint Requires Authentication"
            description = (
                f"Endpoint {f['path']} on {BASE} is registered but requires "
                f"authentication (HTTP {f['status']}). Not directly exploitable "
                "without credentials, but expands the attack surface for "
                "credential-stuffing and session attacks."
            )
        else:
            title = "Exposed API Endpoint"
            description = (
                f"Endpoint {f['path']} on {BASE} is reachable (HTTP {f['status']}) "
                "without authentication and returned application content. "
                "Verify it performs proper authorization, validation and rate limiting."
            )
        evidence = f"HTTP {f['status']} on {BASE}{f['path']}"
        if f.get("body"):
            clean = re.sub(r"\s+", " ", f["body"]).strip()
            if len(clean) > 120:
                clean = clean[:120] + "..."
            evidence += f" -> {clean}"
        print(json.dumps({
            "title": title,
            "description": description,
            "severity": severity,
            "path": BASE + f["path"],
            "evidence": evidence,
            "category": "API01",
            "remediation": (
                "Restrict access to sensitive API endpoints (auth, role-based "
                "access control, rate limiting); remove or protect debug and "
                "administrative routes."
            ),
            "reference": "https://owasp.org/API-Security/editions/2023/en/0x11-t10/",
            "cwe": "CWE-200",
        }))


if __name__ == "__main__":
    main()
