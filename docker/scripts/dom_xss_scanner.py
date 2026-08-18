#!/usr/bin/env python3
"""DOM XSS / client-side scanner for the VAPT executor.

Two passes:

1. Headless Chromium: render each discovered same-origin URL with XSS
   payloads injected into the query string, URL fragment and common
   reflectable parameters; grep the rendered DOM for a unique marker
   (payload lands in a sink such as innerHTML/insertAdjacentHTML -> DOM XSS).

2. Static client-JS analysis: fetch same-origin script bundles and flag
   dangerous sink patterns that read user-controlled sources
   (location.hash, location.search, document.referrer).

Emits findings as JSON Lines on stdout:

    {"title": "...", "description": "...", "severity": "medium",
     "path": "/#/search?q=x", "evidence": "...", "category": "DOM-XSS",
     "cwe": "CWE-79", "reference": "..."}

Usage: dom_xss_scanner.py <base_url>
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost"
UA = {"User-Agent": "astraix-vapt-scanner"}
MARKER = "PXSS-7f3a-42"
HEADLESS_TIMEOUT = 60
MAX_URLS = 12
MAX_JS_BYTES = 3 * 1024 * 1024

# payload -> marker must appear in the RENDERED DOM if the payload executes.
PAYLOADS = [
    ("query", f"?q=<img src=x onerror=document.title='{MARKER}'>"),
    ("hash", f"#<iframe src=\"javascript:document.title='{MARKER}'\"></iframe>"),
    ("hash2", f"#<svg onload=document.title='{MARKER}'>"),
    ("param", f"?name=</textarea><script>document.title='{MARKER}'</script>"),
]

SINK_RE = re.compile(
    r"(innerHTML|outerHTML|insertAdjacentHTML|document\.write|"
    r"eval\s*\(|setAttribute\s*\(\s*['\"]?(?:src|href|srcdoc)|"
    r"location\.(?:hash|search)|location\.replace|location=)", re.I
)
SOURCE_RE = re.compile(
    r"(location\.(?:hash|search|href)|document\.referrer|URLSearchParams|"
    r"getElementById\s*\([^)]*\)\.value)", re.I
)

findings = []


def add(title, description, severity, path, evidence=None, category="DOM-XSS",
        cwe="CWE-79", reference=None):
    entry = {
        "title": title,
        "description": description,
        "severity": severity,
        "path": path,
        "evidence": (evidence or "")[:400],
        "category": category,
        "cwe": cwe,
    }
    if reference:
        entry["reference"] = reference
    findings.append(entry)


def http_get(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except Exception as e:
        return 0, str(e)[:80]


def chromium_available():
    paths = ["chromium", "chromium-browser", "google-chrome"]
    for p in paths:
        try:
            subprocess.run([p, "--version"], capture_output=True, timeout=10)
            return p
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue
    return None


def render_dom(url):
    chrome = chromium_available()
    if not chrome:
        return None
    try:
        proc = subprocess.run(
            [chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
             "--disable-dev-shm-usage", "--dump-dom",
             f"--virtual-time-budget=8000", url],
            capture_output=True, text=True, timeout=HEADLESS_TIMEOUT,
        )
        return (proc.stdout or "") + (proc.stderr or "")
    except (subprocess.TimeoutExpired, OSError):
        return None


def discover_urls():
    urls = [BASE + "/"]
    st, body = http_get(BASE + "/")
    if not body:
        return urls
    for m in re.finditer(r'(?:href|src)="(/[^"#?]*)"', body):
        path = m.group(1)
        if not path.startswith(("//", "http")):
            urls.append(BASE + path)
    for m in re.finditer(r'(?:href|src)="(https?://[^"]+)"', body):
        full = m.group(1)
        if urllib.parse.urlsplit(full).netloc == urllib.parse.urlsplit(BASE).netloc:
            urls.append(full)
    seen = set()
    out = []
    for u in urls:
        key = u.split("#")[0]
        if key not in seen:
            seen.add(key)
            out.append(u)
    return out[:MAX_URLS]


def collect_scripts(urls):
    scripts = []
    for u in urls[:6]:
        st, body = http_get(u)
        if not body:
            continue
        for m in re.finditer(r'<script[^>]+src="([^"]+)"', body):
            src = m.group(1)
            if src.startswith("//"):
                src = urllib.parse.urlsplit(BASE).scheme + ":" + src
            elif src.startswith("/"):
                src = BASE + src
            if urllib.parse.urlsplit(src).netloc == urllib.parse.urlsplit(BASE).netloc:
                scripts.append(src)
    return list(dict.fromkeys(scripts))[:8]


def scan_client_js(urls):
    scripts = collect_scripts(urls)
    mini = min(scripts, key=len) if scripts else None
    for src in scripts:
        st, body = http_get(src, timeout=30)
        if st != 200 or not body or len(body) > MAX_JS_BYTES:
            continue
        snippets = []
        for km in SINK_RE.finditer(body):
            snippet = body[max(0, km.start() - 160): km.end() + 160]
            if SOURCE_RE.search(snippet):
                snippets.append(snippet)
        if snippets:
            floored = [s for s in snippets if re.search(r"(location\.(hash|search)|document\.referrer)", s, re.I)]
            add(
                "DOM XSS Sink (client-side JS)",
                f"Script {src} contains a dangerous sink ({'data flow from user-controlled source' if floored else 'possible sink'}) "
                "reachable from user input (location.hash/search / referrer).",
                "high" if floored else "medium", src,
                evidence=floored[0][:240] if floored else snippet[:240],
                reference="https://portswigger.net/web-security/dom-based/xss",
            )


def main():
    urls = discover_urls()
    chrome = chromium_available()
    if not chrome:
        add(
            "DOM XSS: Headless Browser Unavailable",
            "No headless Chromium in the scan container; rendered-DOM payload "
            "tests skipped (client-side JS static analysis still attempted).",
            "info", BASE, category="DOM-XSS", cwe="CWE-79",
        )
    scan_client_js(urls)

    if chrome:
        seen_keys = set()
        for u in urls:
            for label, payload in PAYLOADS:
                sep = "&" if "?" in u.split("#", 1)[0] else "?"
                base = u.split("#", 1)[0]
                probe = base + sep + payload if label == "param" else base + "?" + payload.lstrip("?") if label == "query" else u.split("#", 1)[0] + "#" + payload.lstrip("#")
                key = (probe.split("#", 1)[0], label)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                dom = render_dom(probe)
                if dom and MARKER in dom:
                    add(
                        "DOM XSS (rendered, payload executed)",
                        f"Payload executed in the page and injected the marker "
                        f"into the DOM via {label} injection point.",
                        "high", probe,
                        evidence=f"payload={payload[:80]} rendered-marker={MARKER}",
                        reference="https://portswigger.net/web-security/dom-based/xss",
                    )
                    break

    for f in sorted(findings, key=lambda x: {"high": 0, "medium": 1, "low": 2, "info": 3}.get(x["severity"], 4)):
        print(json.dumps(f))


if __name__ == "__main__":
    main()