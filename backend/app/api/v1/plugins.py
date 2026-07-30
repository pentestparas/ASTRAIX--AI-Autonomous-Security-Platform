from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from app.plugins import PluginRegistry, get_plugin_registry
from app.plugins.registry import PluginRunResult
from app.schemas.base import ResponseSchema
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("", response_model=ResponseSchema[List[dict]])
async def list_plugins(
    registry: PluginRegistry = Depends(get_plugin_registry),
):
    """List all registered plugins."""
    plugins = registry.list_plugins()
    payload = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "version": p.version,
            "type": p.type,
            "author": p.author,
            "enabled": registry.get_plugin(p.id).enabled if registry.get_plugin(p.id) else True,
        }
        for p in plugins
    ]
    return ResponseSchema(data=payload)


@router.get("/{plugin_id}", response_model=ResponseSchema[dict])
async def get_plugin(
    plugin_id: str,
    registry: PluginRegistry = Depends(get_plugin_registry),
):
    """Get plugin details by ID."""
    plugin = registry.get_plugin(plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return ResponseSchema(data={
        **plugin.manifest.model_dump(),
        "enabled": plugin.enabled,
    })


@router.post("/{plugin_id}/enable", response_model=ResponseSchema[dict])
async def enable_plugin(
    plugin_id: str,
    registry: PluginRegistry = Depends(get_plugin_registry),
):
    """Enable a plugin."""
    if not registry.enable_plugin(plugin_id):
        raise HTTPException(status_code=404, detail="Plugin not found")
    return ResponseSchema(message=f"Plugin {plugin_id} enabled")


@router.post("/{plugin_id}/disable", response_model=ResponseSchema[dict])
async def disable_plugin(
    plugin_id: str,
    registry: PluginRegistry = Depends(get_plugin_registry),
):
    """Disable a plugin."""
    if not registry.disable_plugin(plugin_id):
        raise HTTPException(status_code=404, detail="Plugin not found")
    return ResponseSchema(message=f"Plugin {plugin_id} disabled")


@router.post("/{plugin_id}/run", response_model=ResponseSchema[dict])
async def run_plugin(
    plugin_id: str,
    params: Optional[Dict[str, Any]] = None,
    registry: PluginRegistry = Depends(get_plugin_registry),
):
    """Run a plugin with given parameters."""
    result = await registry.run_plugin(plugin_id, params or {})
    return ResponseSchema(
        data={
            "success": result.success,
            "duration": result.duration,
            "output": result.output.model_dump() if result.output else None,
            "error": result.error.model_dump() if result.error else None,
        }
    )


@router.get("/info", response_model=ResponseSchema[dict])
async def plugins_info(
    registry: PluginRegistry = Depends(get_plugin_registry),
):
    """Get plugin system info and stats."""
    plugins = registry.list_plugins()
    return ResponseSchema(
        data={
            "total": len(plugins),
            "by_type": _count_by_type(plugins),
            "by_capability": _count_by_capability(plugins),
        }
    )


def _count_by_type(plugins: list) -> dict:
    """Group plugin counts by type."""
    counts = {}
    for p in plugins:
        counts[p.type] = counts.get(p.type, 0) + 1
    return counts


def _count_by_capability(plugins: list) -> dict:
    """Count capabilities across all plugins."""
    counts = {}
    for p in plugins:
        for cap in p.capabilities:
            counts[cap] = counts.get(cap, 0) + 1
    return counts