#!/usr/bin/env python3
"""Semgrep Plugin — static application security testing (SAST).

Reads JSON from stdin: {"target": "/path/to/code", "config": ["p/security-audit"], ...}
Outputs structured JSON matching the SemgrepNormalizer schema.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from typing import Any


def build_semgrep_command(
    target: str,
    config: list[str] | None = None,
    langs: list[str] | None = None,
    max_memory: int = 0,
    timeout: int = 30,
    no_git_ignore: bool = False,
    baseline_commit: str | None = None,
) -> list[str]:
    """Build semgrep command arguments."""
    cmd = ["semgrep", "--json", "--no-git-ignore"]

    # Target
    cmd.append(target)

    # Config/rules
    if config:
        cmd.extend(["--config", ",".join(config)])
    else:
        cmd.extend(["--config", "auto"])

    # Languages
    if langs:
        cmd.extend(["--langs", ",".join(langs)])

    # Max memory
    if max_memory > 0:
        cmd.extend(["--max-memory", str(max_memory)])

    # Timeout
    cmd.extend(["--timeout", str(timeout)])

    # No git ignore
    if no_git_ignore:
        cmd.append("--no-gitignore")

    # Baseline commit
    if baseline_commit:
        cmd.extend(["--baseline-commit", baseline_commit])

    # Quiet (fewer logs)
    cmd.append("--quiet")

    return cmd


def parse_semgrep_results(output: str) -> dict[str, Any]:
    """Parse semgrep JSON output."""
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return {"error": "Failed to parse semgrep output", "results": []}


def run_semgrep_scan(
    target: str,
    config: list[str] | None = None,
    langs: list[str] | None = None,
    max_memory: int = 0,
    timeout: int = 30,
    no_git_ignore: bool = False,
    baseline_commit: str | None = None,
) -> dict[str, Any]:
    """Execute semgrep and return parsed results."""
    cmd = build_semgrep_command(
        target=target,
        config=config,
        langs=langs,
        max_memory=max_memory,
        timeout=timeout,
        no_git_ignore=no_git_ignore,
        baseline_commit=baseline_commit,
    )

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 60,
        )

        # Semgrep returns 0 for success, 1 for findings, 2+ for errors
        if result.returncode >= 2:
            return {
                "target": target,
                "error": f"Semgrep exited with code {result.returncode}: {result.stderr[:500]}",
                "results": [],
            }

        semgrep_results = parse_semgrep_results(result.stdout)

        return {
            "target": target,
            "schema_version": "1.0.0",
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "results": semgrep_results,
        }

    except subprocess.TimeoutExpired:
        return {
            "target": target,
            "error": f"Semgrep timed out after {timeout} seconds",
            "results": [],
        }
    except FileNotFoundError:
        return {
            "target": target,
            "error": "Semgrep not found. Please install semgrep.",
            "results": [],
        }
    except Exception as exc:
        return {
            "target": target,
            "error": str(exc),
            "results": [],
        }


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        params: dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError:
        params = {}

    target = params.get("target") or params.get("input") or ""
    if not target:
        print(json.dumps({"results": [], "error": "No target specified"}))
        return 0

    result = run_semgrep_scan(
        target=target,
        config=params.get("config", ["p/security-audit"]),
        langs=params.get("lang"),
        max_memory=int(params.get("max_memory", 0)),
        timeout=int(params.get("timeout", 30)),
        no_git_ignore=bool(params.get("no_git_ignore", False)),
        baseline_commit=params.get("baseline_commit"),
    )

    print(json.dumps(result, indent=2))
    return 0


import sys

if __name__ == "__main__":
    sys.exit(main())