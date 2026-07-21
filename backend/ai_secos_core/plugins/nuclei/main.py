#!/usr/bin/env python3
"""Nuclei Plugin — vulnerability scanning with templates.

Reads JSON from stdin: {"target": "https://example.com", "tags": ["cve"], ...}
Outputs structured JSON matching the NucleiNormalizer schema.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from typing import Any


def build_nuclei_command(
    target: str,
    templates: list[str] | None = None,
    template_dirs: list[str] | None = None,
    severities: list[str] | None = None,
    tags: list[str] | None = None,
    rate_limit: int = 150,
    bulk_size: int = 25,
    timeout: int = 10,
    retries: int = 1,
    follow_redirects: bool = False,
    max_redirects: int = 5,
) -> list[str]:
    """Build nuclei command arguments."""
    cmd = ["nuclei", "-json", "-json-export", "/dev/stdout"]

    # Target
    cmd.extend(["-u", target])

    # Templates
    if templates:
        cmd.extend(["-t", ",".join(templates)])

    if template_dirs:
        for td in template_dirs:
            cmd.extend(["-t", f"templates/{td}"])

    # Severity filter
    if severities:
        cmd.extend(["-severity", ",".join(severities)])

    # Tags filter
    if tags:
        cmd.extend(["-tags", ",".join(tags)])

    # Rate limiting
    cmd.extend(["-rl", str(rate_limit)])

    # Bulk size
    cmd.extend(["-bs", str(bulk_size)])

    # Timeout
    cmd.extend(["-timeout", str(timeout)])

    # Retries
    cmd.extend(["-retries", str(retries)])

    # Redirects
    if follow_redirects:
        cmd.append("-fof")
    cmd.extend(["-max-redirects", str(max_redirects)])

    # Update templates
    cmd.append("-update")

    # Silent mode (less noise)
    cmd.append("-silent")

    return cmd


def parse_nuclei_json(output: str) -> list[dict[str, Any]]:
    """Parse nuclei JSON output lines."""
    findings = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            finding = json.loads(line)
            findings.append(finding)
        except json.JSONDecodeError:
            continue
    return findings


def run_nuclei_scan(
    target: str,
    templates: list[str] | None = None,
    template_dirs: list[str] | None = None,
    severities: list[str] | None = None,
    tags: list[str] | None = None,
    rate_limit: int = 150,
    bulk_size: int = 25,
    timeout: int = 10,
    retries: int = 1,
    follow_redirects: bool = False,
    max_redirects: int = 5,
) -> dict[str, Any]:
    """Execute nuclei and return parsed results."""
    cmd = build_nuclei_command(
        target=target,
        templates=templates,
        template_dirs=template_dirs,
        severities=severities,
        tags=tags,
        rate_limit=rate_limit,
        bulk_size=bulk_size,
        timeout=timeout,
        retries=retries,
        follow_redirects=follow_redirects,
        max_redirects=max_redirects,
    )

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,
        )

        if result.returncode not in (0, 1):  # 0=success, 1=low findings
            return {
                "target": target,
                "error": f"Nuclei exited with code {result.returncode}: {result.stderr[:500]}",
                "findings": [],
            }

        findings = parse_nuclei_json(result.stdout)

        return {
            "target": target,
            "schema_version": "1.0.0",
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "findings_count": len(findings),
            "findings": findings,
        }

    except subprocess.TimeoutExpired:
        return {
            "target": target,
            "error": "Nuclei scan timed out after 600 seconds",
            "findings": [],
        }
    except FileNotFoundError:
        return {
            "target": target,
            "error": "Nuclei not found. Please install nuclei.",
            "findings": [],
        }
    except Exception as exc:
        return {
            "target": target,
            "error": str(exc),
            "findings": [],
        }


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        params: dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError:
        params = {}

    target = params.get("target") or params.get("input") or ""
    if not target:
        print(json.dumps({"findings": [], "error": "No target specified"}))
        return 0

    result = run_nuclei_scan(
        target=target,
        templates=params.get("templates"),
        template_dirs=params.get("template_dirs", ["vulnerabilities"]),
        severities=params.get("severities"),
        tags=params.get("tags"),
        rate_limit=int(params.get("rate_limit", 150)),
        bulk_size=int(params.get("bulk_size", 25)),
        timeout=int(params.get("timeout", 10)),
        retries=int(params.get("retries", 1)),
        follow_redirects=bool(params.get("follow_redirects", False)),
        max_redirects=int(params.get("max_redirects", 5)),
    )

    print(json.dumps(result, indent=2))
    return 0


import sys

if __name__ == "__main__":
    sys.exit(main())