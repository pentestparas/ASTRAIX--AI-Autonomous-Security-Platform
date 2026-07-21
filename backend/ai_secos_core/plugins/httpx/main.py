#!/usr/bin/env python3
"""httpx Plugin — live HTTP/HTTPS probe + technology fingerprinting.

Reads JSON from stdin: {"target": "example.com", "ports": [80, 443], "follow_redirects": true}
Outputs structured JSON matching the HttpxNormalizer schema.
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any

import httpx


def probe_target(
    target: str,
    ports: list[int] | None = None,
    follow_redirects: bool = True,
) -> list[dict[str, Any]]:
    """Probe target host on specified ports using real httpx."""
    ports = ports or [80, 443]
    results: list[dict[str, Any]] = []

    for port in ports:
        item: dict[str, Any] = {
            "input": target,
            "host": target,
            "port": port,
        }
        try:
            scheme = "https" if port == 443 else "http"
            url = f"{scheme}://{target}:{port}"
            item["scheme"] = scheme
            item["url"] = url

            with httpx.Client(
                timeout=httpx.Timeout(10.0, connect=5.0),
                follow_redirects=follow_redirects,
                verify=True,
                http2=False,
            ) as client:
                start = time.monotonic()
                response = client.get(url)
                elapsed_ms = int((time.monotonic() - start) * 1_000_000 / 1_000)

                item["status_code"] = response.status_code
                item["content_length"] = int(response.headers.get("content-length", 0))
                item["content_type"] = response.headers.get("content-type", "")
                item["response_time_ms"] = elapsed_ms
                item["tech"] = _detect_technologies(response.headers)
                item["url"] = str(response.url)

                server = response.headers.get("server", "")
                if server:
                    item["webserver"] = server

                cdn_name = _detect_cdn(response.headers)
                if cdn_name:
                    item["cdn_name"] = cdn_name

                try:
                    item["title"] = _extract_title(response.text)
                except Exception:
                    item["title"] = ""

                if port == 443 or scheme == "https":
                    try:
                        transport = response.extensions.get("http_version")
                        if transport:
                            item["tls"] = {"version": "TLSv1.2+", "cipher": "detected"}
                    except Exception:
                        pass

            results.append(item)

        except httpx.TimeoutException:
            item["error"] = "timeout"
            item["status_code"] = 0
            results.append(item)
        except httpx.ConnectError as exc:
            item["error"] = f"connect_error: {exc}"
            item["status_code"] = 0
            results.append(item)
        except Exception as exc:
            item["error"] = str(exc)
            item["status_code"] = 0
            results.append(item)

    return results


def _detect_technologies(headers: httpx.Headers) -> list[dict[str, str]]:
    """Detect technologies from HTTP response headers."""
    tech: list[dict[str, str]] = []
    seen: set[str] = set()

    for hk, hv in headers.items():
        hk_l, hv_l = hk.lower(), hv.lower()

        if hk_l == "cf-ray":
            _add(tech, seen, "Cloudflare", "")
        elif hk_l in ("x-amz-cf-id", "x-amz-id-2"):
            _add(tech, seen, "CloudFront", "")
        elif hk_l == "x-vercel-cache":
            _add(tech, seen, "Vercel", "")
        elif hk_l == "x-nf-request-id":
            _add(tech, seen, "Netlify", "")
        elif hk_l == "x-served-by":
            _add(tech, seen, "AWS", "")
        elif hk_l == "x-github-request-id":
            _add(tech, seen, "GitHub Pages", "")
        elif hk_l == "server":
            if "cloudflare" in hv_l:
                _add(tech, seen, "Cloudflare", _ver(hv_l, "cloudflare"))
            if "nginx" in hv_l:
                _add(tech, seen, "Nginx", _ver(hv_l, "nginx"))
            elif "apache" in hv_l:
                _add(tech, seen, "Apache", _ver(hv_l, "apache"))
            elif "microsoft-iis" in hv_l:
                _add(tech, seen, "IIS", _ver(hv_l, "microsoft-iis"))
            elif "caddy" in hv_l:
                _add(tech, seen, "Caddy", _ver(hv_l, "caddy"))
        elif hk_l == "x-powered-by":
            if "next.js" in hv_l:
                _add(tech, seen, "Next.js", _ver(hv_l, "next.js"))
            elif "express" in hv_l:
                _add(tech, seen, "Express", _ver(hv_l, "express"))
            elif "php" in hv_l:
                _add(tech, seen, "PHP", _ver(hv_l, "php"))
        elif hk_l == "x-react-version":
            _add(tech, seen, "React", hv)

    return tech


def _add(
    tech: list[dict[str, str]],
    seen: set[str],
    name: str,
    version: str,
) -> None:
    if name not in seen:
        seen.add(name)
        tech.append({"name": name, "version": version})


def _ver(text: str, name: str) -> str:
    """Extract version from header like 'nginx/1.21.6'."""
    if name not in text:
        return ""
    try:
        return text.split(f"{name}/")[1].split()[0].rstrip(",;")
    except (IndexError, ValueError):
        return ""


def _detect_cdn(headers: httpx.Headers) -> str:
    """Return CDN name if detected from headers."""
    if "cf-ray" in headers:
        return "Cloudflare"
    if "x-amz-cf-id" in headers or "x-amz-id-2" in headers:
        return "CloudFront"
    if "x-vercel-cache" in headers:
        return "Vercel"
    if "x-nf-request-id" in headers:
        return "Netlify"
    if "x-served-by" in headers:
        return "AWS"
    return ""


def _extract_title(html: str) -> str:
    """Basic HTML <title> extraction."""
    match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        params: dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError:
        params = {}

    target = params.get("target") or params.get("input") or ""
    if not target:
        print(json.dumps({"items": []}))
        return 0

    target = target.strip()
    if target.startswith("http://") or target.startswith("https://"):
        from urllib.parse import urlparse
        target = urlparse(target).netloc or target

    ports_raw = params.get("ports", [80, 443])
    ports = [int(p) for p in ports_raw]
    follow_redirects = bool(params.get("follow_redirects", True))

    items = probe_target(target, ports, follow_redirects)

    out: dict[str, Any] = {
        "items": items,
        "schema_version": "1.0.0",
        "scanned_at": datetime.now(timezone.utc).isoformat(),
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())