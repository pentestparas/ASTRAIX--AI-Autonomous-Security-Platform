#!/usr/bin/env python3
"""Subfinder Plugin — passive subdomain enumeration.

Reads JSON from stdin: {"target": "example.com", "sources": [...], ...}
Outputs structured JSON matching the SubfinderNormalizer schema.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from typing import Any


def build_subfinder_command(
    target: str,
    sources: list[str] | None = None,
    threads: int = 10,
    max_time: int = 300,
    silent: bool = True,
    verify: bool = False,
) -> list[str]:
    """Build subfinder command arguments."""
    cmd = ["subfinder", "-json"]

    # Target
    cmd.extend(["-d", target])

    # Sources
    if sources:
        cmd.extend(["-s", ",".join(sources)])

    # Threads
    cmd.extend(["-t", str(threads)])

    # Max time
    cmd.extend(["-max-time", str(max_time)])

    # Silent mode
    if silent:
        cmd.append("-silent")

    # Verify
    if verify:
        cmd.append("-verify")

    # No color
    cmd.append("-nc")

    return cmd


def parse_subfinder_json(output: str) -> list[dict[str, Any]]:
    """Parse subfinder JSON output lines."""
    results = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            result = json.loads(line)
            results.append(result)
        except json.JSONDecodeError:
            continue
    return results


def run_subfinder(
    target: str,
    sources: list[str] | None = None,
    threads: int = 10,
    max_time: int = 300,
    silent: bool = True,
    verify: bool = False,
) -> dict[str, Any]:
    """Execute subfinder and return parsed results."""
    cmd = build_subfinder_command(
        target=target,
        sources=sources,
        threads=threads,
        max_time=max_time,
        silent=silent,
        verify=verify,
    )

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=max_time + 30,
        )

        if result.returncode != 0:
            return {
                "target": target,
                "error": f"Subfinder exited with code {result.returncode}: {result.stderr[:500]}",
                "subdomains": [],
            }

        subdomains = parse_subfinder_json(result.stdout)

        return {
            "target": target,
            "schema_version": "1.0.0",
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "subdomains_count": len(subdomains),
            "subdomains": subdomains,
        }

    except subprocess.TimeoutExpired:
        return {
            "target": target,
            "error": f"Subfinder timed out after {max_time} seconds",
            "subdomains": [],
        }
    except FileNotFoundError:
        return {
            "target": target,
            "error": "Subfinder not found. Please install subfinder.",
            "subdomains": [],
        }
    except Exception as exc:
        return {
            "target": target,
            "error": str(exc),
            "subdomains": [],
        }


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        params: dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError:
        params = {}

    target = params.get("target") or params.get("input") or ""
    if not target:
        print(json.dumps({"subdomains": [], "error": "No target specified"}))
        return 0

    result = run_subfinder(
        target=target,
        sources=params.get("sources"),
        threads=int(params.get("threads", 10)),
        max_time=int(params.get("max_time", 300)),
        silent=bool(params.get("silent", True)),
        verify=bool(params.get("verify", False)),
    )

    print(json.dumps(result, indent=2))
    return 0


import sys

if __name__ == "__main__":
    sys.exit(main())