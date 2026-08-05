"""Adapter registry - discovery, enablement and health aggregation."""

from typing import Dict, List

from app.vapt.adapters.base import AdapterStatus, VAPTAdapter
from app.vapt.adapters.kali_tool import LyrieAdapter, RaccoonAdapter
from app.vapt.adapters.xalgorix import XalgorixAdapter
from app.vapt.adapters.external import DarkMoonAdapter, PentagiAdapter, RedamonAdapter, ZenAiAdapter


def _build_adapters() -> List[VAPTAdapter]:
    return [
        RaccoonAdapter(),
        LyrieAdapter(),
        XalgorixAdapter(),
        DarkMoonAdapter(),
        PentagiAdapter(),
        RedamonAdapter(),
        ZenAiAdapter(),
    ]


_ADAPTERS: List[VAPTAdapter] = []
_ADAPTER_MAP: Dict[str, VAPTAdapter] = {}


def _ensure_init() -> None:
    global _ADAPTERS, _ADAPTER_MAP
    if not _ADAPTERS:
        _ADAPTERS = _build_adapters()
        _ADAPTER_MAP = {a.id: a for a in _ADAPTERS}


def get_all_adapters() -> List[VAPTAdapter]:
    _ensure_init()
    return list(_ADAPTERS)


def get_adapter(adapter_id: str) -> VAPTAdapter:
    _ensure_init()
    return _ADAPTER_MAP.get(adapter_id)


def get_enabled_adapters() -> List[VAPTAdapter]:
    _ensure_init()
    return [a for a in _ADAPTERS if a.enabled()]


async def adapter_health() -> List[AdapterStatus]:
    _ensure_init()
    return [await a.health() for a in _ADAPTERS]
