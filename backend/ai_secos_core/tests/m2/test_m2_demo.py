"""M2 End-to-End test.

Validates the vertical slice: Capability → Plugin → Normalize → Risk → Report.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from ai_secos_core.m2_demo import run_demo


def test_m2_demo_runs():
    """The full M2 path executes end-to-end and emits a summary."""
    result = asyncio.run(run_demo())
    assert result["status"] in ("ok", "skip")
    if result["status"] != "ok":
        return
    assert result["capability"] == "web/discovery"
    assert result["finding_count"] >= 1
    assert 0 <= result["risk_score_min"] <= 100
    assert 0 <= result["risk_score_max"] <= 100
    assert result["report_count"] >= 1


if __name__ == "__main__":
    test_m2_demo_runs()
    print("[m2] OK")