"""
Per-scan LLM usage tracking for the AI transparency panel.

Thread-safe in-memory counters keyed by scan_id. The orchestrator reads
snapshots and publishes them as ``llm_stats`` events; the agent loop and
matrix agent additionally publish live ``llm_call`` events so the scan
console can show provider / model / latency / token insight without any
new storage. All counters are best-effort visibility, never correctness.
"""

import threading
import time
from typing import Any, Dict, Optional


def _blank() -> Dict[str, Any]:
    return {
        "calls": 0,
        "ok_calls": 0,
        "tokens_in": 0,
        "tokens_out": 0,
        "elapsed_ms": 0.0,
        "providers": {},
        "purposes": {},
    }


class _LlmUsageTracker:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._scans: Dict[str, Dict[str, Any]] = {}

    def record(
        self,
        scan_id: str,
        provider: str,
        model: str,
        purpose: str = "agent",
        tokens_in: int = 0,
        tokens_out: int = 0,
        ms: float = 0.0,
        ok: bool = True,
    ) -> None:
        with self._lock:
            st = self._scans.setdefault(scan_id, _blank())
            st["calls"] += 1
            if ok:
                st["ok_calls"] += 1
            st["elapsed_ms"] += ms
            if tokens_in:
                st["tokens_in"] += int(tokens_in)
            if tokens_out:
                st["tokens_out"] += int(tokens_out)
            prov = st["providers"].setdefault(provider, {"calls": 0, "tokens": 0, "models": {}})
            prov["calls"] += 1
            prov["tokens"] += int(tokens_in or 0) + int(tokens_out or 0)
            prov["models"][model] = prov["models"].get(model, 0) + 1
            st["purposes"][purpose] = st["purposes"].get(purpose, 0) + 1
            if len(self._scans) > 64:
                self._scans.pop(next(iter(self._scans)), None)

    def snapshot(self, scan_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            st = self._scans.get(scan_id)
            if not st:
                return None
            return {
                "calls": st["calls"],
                "ok_calls": st["ok_calls"],
                "tokens_in": st["tokens_in"],
                "tokens_out": st["tokens_out"],
                "total_tokens": st["tokens_in"] + st["tokens_out"],
                "elapsed_ms": round(st["elapsed_ms"], 1),
                "providers": st["providers"],
                "purposes": st["purposes"],
            }

    def reset(self, scan_id: str) -> None:
        with self._lock:
            self._scans.pop(scan_id, None)


_tracker = _LlmUsageTracker()


def record_llm_call(
    scan_id: str,
    provider: str,
    model: str,
    purpose: str = "agent",
    tokens_in: int = 0,
    tokens_out: int = 0,
    ms: float = 0.0,
    ok: bool = True,
) -> None:
    """Best-effort token estimate fallback when providers omit usage data."""
    if not scan_id:
        return
    _tracker.record(scan_id, provider, model, purpose, tokens_in, tokens_out, ms, ok)


def llm_usage_snapshot(scan_id: str) -> Optional[Dict[str, Any]]:
    return _tracker.snapshot(scan_id)


def reset_llm_usage(scan_id: str) -> None:
    _tracker.reset(scan_id)


def estimate_tokens(text: Optional[str]) -> int:
    """Rough 4-char-per-token estimate for providers without usage fields."""
    return len(text or "") // 4


def time_tracked(t0: float) -> float:
    return round((time.time() - t0) * 1000.0, 1)