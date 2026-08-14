"""Finding normalization: canonical vulnerability names + CVSS scores.

Raw tool parsers emit scanner-flavored titles (e.g. "SQL injection
candidate in q on /rest/products/search?q=test"). The normalizer maps
them onto standard vulnerability names and attaches a CVSS base score
so reports and the findings UI show consistent, comparable data.
"""
import re
from typing import Optional

from app.vapt.models import VAPTFinding, VAPTSeverity

# (regex, canonical name) - first match wins. Both title and
# vulnerability_type are searched.
VULN_PATTERNS: list[tuple[str, str]] = [
    (r"nosql", "NoSQL Injection"),
    (r"(?<!no)sql\s*injection|sqli|sqlite|near \"|unterminated", "SQL Injection (SQLi)"),
    (r"prompt injection", "Prompt Injection"),
    (r"cross[- ]site scripting|xss|onerror|alert\(", "Cross-Site Scripting (XSS)"),
    (r"path traversal|directory traversal|\.\./", "Path Traversal"),
    (r"ssrf|server-side request", "Server-Side Request Forgery (SSRF)"),
    (r"command injection|rce|remote code", "Command Injection / RCE"),
    (r"open redirect", "Open Redirect"),
    (r"csrf", "Cross-Site Request Forgery (CSRF)"),
    (r"file upload|unrestricted upload", "Unrestricted File Upload"),
    (r"authentication bypass|auth bypass|login admin", "Authentication Bypass"),
    (r"default credential|weak password|brute[- ]force|hydra", "Weak / Brute-Forced Credentials"),
    (r"broken access|idor|unauthorized access", "Broken Access Control (IDOR)"),
    (r"open port", "Open Port Exposure"),
    (r"robots[_.]?txt", "Information Disclosure — robots.txt"),
    (r"directory listing", "Directory Listing Enabled"),
    (r"security header|missing.*header|x-frame|hsts|content-security", "Missing Security Headers"),
    (r"cors", "CORS Misconfiguration"),
    (r"tls|cipher|ssl certificate|ssl3|pooodle|beast|heartbleed", "Weak TLS / SSL Configuration"),
    (r"cleartext|unencrypted|http traffic", "Cleartext Traffic"),
    (r"denial of service|dos\b|slowloris", "Denial of Service (DoS)"),
    (r"error disclosure|unhandled exception|error-prone|stack trace|error handling", "Sensitive Error Disclosure"),
    (r"information disclosure|exposed|leak", "Information Disclosure"),
    (r"outdated|old version|legacy|deprecated", "Outdated Software / Component"),
    (r"misconfiguration|misconfig", "Security Misconfiguration"),
    (r"web server|server header", "Web Server Misconfiguration"),
    (r"known exploit|exploit-db", "Known Exploit Available"),
    (r"metasploit", "Metasploit Module Finding"),
]

# Severity -> CVSSv3 base score (common representative vectors).
CVSS_BY_SEVERITY: dict[VAPTSeverity, float] = {
    VAPTSeverity.CRITICAL: 9.8,
    VAPTSeverity.HIGH: 8.1,
    VAPTSeverity.MEDIUM: 5.3,
    VAPTSeverity.LOW: 2.6,
    VAPTSeverity.INFO: 0.0,
}


def canonical_vuln_name(finding: VAPTFinding) -> Optional[str]:
    """Map a raw finding title/type onto a standard vulnerability name."""
    haystack = " ".join([
        finding.title or "",
        finding.vulnerability_type or "",
    ]).lower()
    for pattern, name in VULN_PATTERNS:
        if re.search(pattern, haystack):
            return name
    return None


def cvss_for_severity(severity: VAPTSeverity) -> float:
    return CVSS_BY_SEVERITY.get(severity, 0.0)


def normalize_finding(finding: VAPTFinding) -> VAPTFinding:
    """Return the finding with a canonical title/type and a CVSS score."""
    name = canonical_vuln_name(finding)
    if name:
        finding.title = name
        finding.vulnerability_type = name
    if finding.cvss_score is None:
        finding.cvss_score = cvss_for_severity(finding.severity)
    return finding


def normalize_findings(findings: list[VAPTFinding]) -> list[VAPTFinding]:
    return [normalize_finding(f) for f in findings]
