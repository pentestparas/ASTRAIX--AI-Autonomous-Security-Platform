#!/usr/bin/env python3
"""Secure code review scanner for the VAPT executor.

Fingerprints the live web app, clones its public source repository, and
runs SAST/secret scanning on the code: semgrep --config=auto, CodeQL
(security-and-quality query packs), bandit, gitleaks and trivy fs
(dependency CVEs, IaC misconfig, secrets). Catches the class of issues that
black-box HTTP scanning cannot see (secure-code-review style: SQLi string
building, JWT alg confusion, hardcoded credentials, vulnerable dependencies,
unsafe middleware chains, ...).

Emits findings as JSON Lines on stdout:

    {"title": "...", "description": "...", "severity": "high",
     "path": "src/foo.js:12", "evidence": "...", "category": "code-review",
     "cwe": "CWE-89", "reference": "..."}

Usage: code_review_scanner.py <base_url>
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost"
UA = {"User-Agent": "astraix-vapt-scanner"}
TIMEOUTS = {"clone": 180, "semgrep": 660, "bandit": 300, "gitleaks": 180,
            "trivy": 900, "codeql_db": 420, "codeql_analyze": 900}

# Known apps -> public source repos (fingerprint markers on the live app).
REPO_FINGERPRINTS = [
    (r"juice[ _-]?shop", "https://github.com/juice-shop/juice-shop.git"),
    (r"dvwa", "https://github.com/digininja/DVWA.git"),
    (r"webgoat", "https://github.com/WebGoat/WebGoat.git"),
    (r"wordpress", None),  # closed-ish ecosystem, no single repo
]

SEVERITY_MAP = {
    "ERROR": "high", "WARNING": "medium", "INFO": "low",
}

findings = []


def add(title, description, severity, path, evidence=None, cwe=None, reference=None,
        category="code-review"):
    entry = {
        "title": title,
        "description": description,
        "severity": severity,
        "path": path,
        "evidence": (evidence or "")[:400],
    }
    if cwe:
        entry["cwe"] = cwe
    if reference:
        entry["reference"] = reference
    if category:
        entry["category"] = category
    findings.append(entry)


def http_get(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers={**UA, "Accept": "text/html"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except Exception:
        return 0, ""


def fingerprint_repo():
    _, body = http_get(BASE)
    for pattern, repo in REPO_FINGERPRINTS:
        if re.search(pattern, (body or "")[:200000], re.IGNORECASE):
            return repo, pattern
    st, head = http_get(BASE + "/.git/HEAD")
    if st == 200 and ("ref:" in head or "sha1" in head.lower()):
        return BASE.rstrip("/") + "/.git", ".git"
    return None, None


def run(cmd, timeout):
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              env={**os.environ, "PYTHONUNBUFFERED": "1"})
        return (proc.stdout or "") + (proc.stderr or "")
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return f"__ERROR__ {e.__class__.__name__}: {e}"


def scan_source(src):
    files = [os.path.join(dp, f) for dp, _, fs in os.walk(src)
             for f in fs if not dp.startswith((src + "/.git", src + "/node_modules", src + "/frontend"))]
    has_js = any(f.endswith((".js", ".ts", ".jsx", ".tsx")) for f in files)
    has_py = any(f.endswith(".py") for f in files)

    if has_js:
        out = run(["semgrep", "--config=auto", "--json", "-q", src], TIMEOUTS["semgrep"])
        _parse_semgrep(out)
    if has_py:
        out = run(["bandit", "-r", "-f", "json", src], TIMEOUTS["bandit"])
        _parse_bandit(out)

    _scan_codeql(src, has_js, has_py)
    _scan_trivy(src)

    out = run(["gitleaks", "dir", src, "--report-format", "json", "--redact",
               "--no-banner"], TIMEOUTS["gitleaks"])
    _parse_gitleaks(out)


def _scan_codeql(src, has_js, has_py):
    """CodeQL (GitHub's SAST engine) - security-extended query packs."""
    if not has_js and not has_py:
        return
    languages = []
    if has_js:
        languages.append("javascript")
    if has_py:
        languages.append("python")
    db = tempfile.mkdtemp(prefix="codeql-") + "/db"
    for lang in languages:
        out = run(["codeql", "database", "create", db + "-" + lang,
                   f"--language={lang}", "--quiet", src], TIMEOUTS["codeql_db"])
        if "__ERROR__" in out:
            continue
        sarif = db + "-" + lang + ".sarif"
        out = run(["codeql", "database", "analyze", db + "-" + lang,
                   "codeql/security-and-quality",
                   f"--format=sarif-latest", f"--output={sarif}", "--threads=2"],
                  TIMEOUTS["codeql_analyze"])
        if "__ERROR__" in out or not os.path.exists(sarif):
            continue
        _parse_codeql(sarif)
    import shutil
    shutil.rmtree(os.path.dirname(db), ignore_errors=True)


def _scan_trivy(src):
    """Trivy fs - dependency vulnerabilities + secrets + IaC misconfig
    (Snyk equivalent, fully offline after its first DB download)."""
    out = run(["trivy", "fs", "--format", "json", "--quiet",
               "--scanners", "vuln,secret,misconfig", src], TIMEOUTS["trivy"])
    _parse_trivy(out)


def _parse_trivy(out):
    if "__ERROR__" in out or not out.strip():
        return
    try:
        data = json.loads(out)
    except (json.JSONDecodeError, TypeError):
        return
    for result in data.get("Results", []):
        target = result.get("Target", "")
        for vuln in result.get("Vulnerabilities", [])[:40]:
            add(
                f"Dependency Vulnerability: {vuln.get('VulnerabilityID', '')} in {vuln.get('PkgName', '')}",
                f"{vuln.get('Title', vuln.get('VulnerabilityID', ''))} "
                f"(installed {vuln.get('InstalledVersion', '?')}, fixed {vuln.get('FixedVersion', 'none')})",
                str(vuln.get("Severity", "medium")).lower(),
                target,
                evidence=f"{vuln.get('VulnerabilityID')}: {vuln.get('Description', '')[:150]}",
                cwe=next(iter(vuln.get("CweIDs") or []), None),
                reference=vuln.get("PrimaryURL"),
            )
        for sec in result.get("Secrets", [])[:10]:
            add(
                f"Secret in Source: {sec.get('RuleID', '')}",
                "Hardcoded secret/credential pattern found in repository files.",
                "high", f"{target}:{sec.get('LineNumber', '')}",
                evidence=f"{sec.get('Title', '')} -> {sec.get('Match', '')[:80]}",
                cwe="CWE-798", category="code-review",
                reference="https://aquasecurity.github.io/trivy/",
            )


def _parse_codeql(sarif_path):
    try:
        with open(sarif_path, encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError, TypeError):
        return
    level_map = {"error": "high", "warning": "medium", "note": "low"}
    for run in data.get("runs", []):
        for res in run.get("results", [])[:60]:
            loc = (res.get("locations") or [{}])[0].get("physicalLocation", {})
            uri = (loc.get("artifactLocation", {}).get("uri") or "unknown").lstrip("file://")
            line = (loc.get("region", {}) or {}).get("startLine", "")
            add(
                f"CodeQL: {res.get('ruleId', '')}",
                f"CodeQL security query flagged: {res.get('message', {}).get('text', '')[:200]}",
                level_map.get(str(res.get("level", "warning")).lower(), "medium"),
                f"{uri}:{line}",
                evidence=(res.get("message", {}).get("text") or "")[:250],
                cwe=next(iter((res.get("properties", {}) or {}).get("tags") or []), None),
                reference="https://codeql.github.com/",
            )


def _parse_semgrep(out):
    if "__ERROR__" in out or not out.strip():
        return
    try:
        data = json.loads(out)
    except (json.JSONDecodeError, TypeError):
        return
    for res in data.get("results", [])[:60]:
        sev = (res.get("extra", {}).get("severity") or "WARNING").upper()
        rule = (res.get("check_id") or "").rsplit(".", 1)[-1]
        add(
            f"Code Review: {rule}",
            "Static analysis on cloned source flagged a vulnerable code pattern: "
            f"{rule} ({rule.split('.')[-1] if '.' in rule else rule}).",
            SEVERITY_MAP.get(sev, "medium"),
            f"{res.get('path', '')}:{res.get('start', {}).get('line', '')}",
            evidence=(res.get("extra", {}).get("lines") or "").strip()[:200] or rule,
            cwe=next(iter((res.get("extra", {}).get("metadata", {}).get("cwe") or [])), None),
            reference="https://semgrep.dev/docs/writing-rules/rule-syntax/",
        )


def _parse_bandit(out):
    if "__ERROR__" in out or not out.strip():
        return
    try:
        data = json.loads(out)
    except (json.JSONDecodeError, TypeError):
        return
    for issue in data.get("results", [])[:60]:
        add(
            f"Code Review: {issue.get('test_id', 'B')} {issue.get('test_name', '')}".strip(),
            f"Bandit flags Python code issue at {issue.get('filename', '')}:"
            f"{issue.get('line_number', '')} - {issue.get('issue_text', '')}",
            ("high" if issue.get("issue_severity") == "HIGH" else
             "medium" if issue.get("issue_severity") == "MEDIUM" else "low"),
            f"{issue.get('filename', '')}:{issue.get('line_number', '')}",
            evidence=(issue.get("code") or "")[:200],
            cwe="CWE-94" if issue.get("test_id") in ("B602", "B604", "B608") else None,
            reference="https://bandit.readthedocs.io/",
        )


def _parse_gitleaks(out):
    if "__ERROR__" in out or not out.strip():
        return
    try:
        data = json.loads(out)
    except (json.JSONDecodeError, TypeError):
        return
    for leak in data[:40] if isinstance(data, list) else []:
        add(
            f"Code Review: Exposed Secret ({leak.get('RuleID', '')})",
            "Secret (API key / token / password) committed to the source repository.",
            "high",
            f"{leak.get('File', '')}:{leak.get('StartLine', '')}",
            evidence=f"rule={leak.get('RuleID', '')} match={leak.get('Match', '')[:80]}",
            cwe="CWE-798",
            reference="https://github.com/gitleaks/gitleaks",
        )


def main():
    repo, matched = fingerprint_repo()
    if not repo:
        add(
            "Code Review: Source Repository Not Available",
            "No public source repository could be identified for this target "
            "(no fingerprint match, no exposed /.git). Static code review skipped.",
            "info", BASE, evidence=f"fingerprint={matched}",
            category="code-review", cwe="CWE-20",
        )
        return _emit()
    if repo.endswith("/.git"):
        add(
            "Code Review: Exposed .git Repository",
            "The target serves its raw .git metadata over HTTP - source code "
            "leakage. Full repository dump may be possible.",
            "high", repo, evidence="/.git/HEAD is publicly readable",
            category="code-review", cwe="CWE-540",
        )
        return _emit()

    tmp = tempfile.mkdtemp(prefix="code-review-")
    src = os.path.join(tmp, "src")
    output = run(["git", "clone", "--depth", "1", "--quiet", repo, src],
                 TIMEOUTS["clone"])
    if "__ERROR__" in output or not os.path.exists(os.path.join(src, ".git")):
        add(
            "Code Review: Clone Failed",
            f"Source clone from {repo} failed; static review skipped. {output[:120]}",
            "info", repo, evidence=output[:200], category="code-review",
        )
        return _emit()

    scan_source(src)

    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    _emit()


def _emit():
    for f in sorted(findings, key=lambda x: {"high": 0, "medium": 1, "low": 2, "info": 3}.get(x["severity"], 4)):
        print(json.dumps(f))


if __name__ == "__main__":
    main()