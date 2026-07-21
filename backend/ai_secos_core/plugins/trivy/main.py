#!/usr/bin/env python3
"""Trivy Plugin — container and IaC security scanning.

Reads JSON from stdin: {"target": "myimage:tag", "scanners": ["vuln", "misconfig"], ...}
Outputs structured JSON matching the TrivyNormalizer schema.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from typing import Any


def build_trivy_command(
    target: str,
    scan_type: str = "image",
    scanners: list[str] | None = None,
    severities: list[str] | None = None,
    vuln_types: list[str] | None = None,
    security_checks: list[str] | None = None,
    format: str = "json",
    timeout: int = 300,
) -> list[str]:
    """Build trivy command arguments."""
    cmd = ["trivy", scan_type, "--format", "json", "--output", "/dev/stdout"]

    # Target
    cmd.append(target)

    # Scanners
    if scanners:
        cmd.extend(["--scanners", ",".join(scanners)])

    # Severity
    if severities:
        cmd.extend(["--severity", ",".join(severities)])

    # Vulnerability types
    if vuln_types:
        cmd.extend(["--vuln-type", ",".join(vuln_types)])

    # Security checks (IaC)
    if security_checks:
        cmd.extend(["--security-checks", ",".join(security_checks)])

    # Timeout
    cmd.extend(["--timeout", f"{timeout}s"])

    # Quiet (less noise)
    cmd.append("--quiet")

    # No progress
    cmd.append("--no-progress")

    return cmd


def parse_trivy_results(output: str) -> dict[str, Any]:
    """Parse trivy JSON output."""
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {"error": "Failed to parse trivy output", "Results": []}


def run_trivy_scan(
    target: str,
    scan_type: str = "image",
    scanners: list[str] | None = None,
    severities: list[str] | None = None,
    vuln_types: list[str] | None = None,
    security_checks: list[str] | None = None,
    format: str = "json",
    timeout: int = 300,
) -> dict[str, Any]:
    """Execute trivy and return parsed results."""
    cmd = build_trivy_command(
        target=target,
        scan_type=scan_type,
        scanners=scanners,
        severities=severities,
        vuln_types=vuln_types,
        security_checks=security_checks,
        format=format,
        timeout=timeout,
    )

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 30,
        )

        if result.returncode not in (0, 1):  # 0=success, 1=some vulnerabilities found
            return {
                "target": target,
                "error": f"Trivy exited with code {result.returncode}: {result.stderr[:500]}",
                "Results": [],
            }

        trivy_results = parse_trivy_results(result.stdout)

        return {
            "target": target,
            "schema_version": "1.0.0",
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "scan_type": scan_type,
            "results": trivy_results,
        }

    except subprocess.TimeoutExpired:
        return {
            "target": target,
            "error": f"Trivy timed out after {timeout} seconds",
            "Results": [],
        }
    except FileNotFoundError:
        return {
            "target": target,
            "error": "Trivy not found. Please install trivy.",
            "Results": [],
        }
    except Exception as exc:
        return {
            "target": target,
            "error": str(exc),
            "Results": [],
        }


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        params: dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError:
        params = {}

    target = params.get("target") or params.get("input") or ""
    if not target:
        print(json.dumps({"Results": [], "error": "No target specified"}))
        return 0

    result = run_trivy_scan(
        target=target,
        scan_type=params.get("scan_type", "image"),
        scanners=params.get("scanners", ["vuln", "misconfig", "secret"]),
        severities=params.get("severities", ["UNKNOWN", "LOW", "MEDIUM", "HIGH", "CRITICAL"]),
        vuln_types=params.get("vuln_type", ["os", "library"]),
        security_checks=params.get("security_checks"),
        timeout=int(params.get("timeout", 300)),
    )

    print(json.dumps(result, indent=2))
    return 0


import sys

if __name__ == "__main__":
    sys.exit(main())