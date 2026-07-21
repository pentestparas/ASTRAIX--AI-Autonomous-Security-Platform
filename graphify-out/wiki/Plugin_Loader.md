# Plugin Loader

> 42 nodes · cohesion 0.06

## Key Concepts

- **PluginRegistry** (11 connections) — `backend/ai_secos_core/plugin_system/registry.py`
- **PluginRecord** (9 connections) — `backend/ai_secos_core/plugin_system/registry.py`
- **PluginValidator** (9 connections) — `backend/ai_secos_core/plugin_system/validator.py`
- **PluginError** (8 connections)
- **PluginManifest** (7 connections)
- **.load_one()** (6 connections) — `backend/ai_secos_core/plugin_system/loader.py`
- **._parse_one()** (6 connections) — `backend/ai_secos_core/plugin_system/loader.py`
- **PluginLoaderError** (5 connections) — `backend/ai_secos_core/plugin_system/loader.py`
- **registry.py** (5 connections) — `backend/ai_secos_core/plugin_system/registry.py`
- **validator.py** (5 connections) — `backend/ai_secos_core/plugin_system/validator.py`
- **.validate_invocation()** (5 connections) — `backend/ai_secos_core/plugin_system/validator.py`
- **ValidationResult** (5 connections) — `backend/ai_secos_core/plugin_system/validator.py`
- **loader.py** (4 connections) — `backend/ai_secos_core/plugin_system/loader.py`
- **.discover()** (4 connections) — `backend/ai_secos_core/plugin_system/loader.py`
- **PluginAlreadyRegisteredError** (4 connections) — `backend/ai_secos_core/plugin_system/registry.py`
- **PluginNotFoundError** (4 connections) — `backend/ai_secos_core/plugin_system/registry.py`
- **_type_match()** (4 connections) — `backend/ai_secos_core/plugin_system/validator.py`
- **LoadedPlugin** (3 connections) — `backend/ai_secos_core/plugin_system/loader.py`
- **.get()** (3 connections) — `backend/ai_secos_core/plugin_system/registry.py`
- **.register()** (3 connections) — `backend/ai_secos_core/plugin_system/registry.py`
- **PluginValidationError** (3 connections) — `backend/ai_secos_core/plugin_system/validator.py`
- **.validate_manifest()** (3 connections) — `backend/ai_secos_core/plugin_system/validator.py`
- **.list_plugins()** (3 connections) — `backend/app/plugins/registry.py`
- **.list()** (2 connections) — `backend/ai_secos_core/plugin_system/registry.py`
- **Plugin Loader: read manifests from disk → PluginRecords.  The Loader is the *onl** (1 connections) — `backend/ai_secos_core/plugin_system/loader.py`
- *... and 17 more nodes in this community*

## Relationships

- [[Metrics System]] (13 shared connections)
- [[App Factory & Null Providers]] (7 shared connections)
- [[Community 69]] (2 shared connections)
- [[Community 33]] (2 shared connections)
- [[Community 34]] (2 shared connections)
- [[Community 35]] (2 shared connections)
- [[Community 51]] (1 shared connections)

## Source Files

- `backend/ai_secos_core/plugin_system/loader.py`
- `backend/ai_secos_core/plugin_system/registry.py`
- `backend/ai_secos_core/plugin_system/validator.py`
- `backend/app/plugins/registry.py`

## Audit Trail

- EXTRACTED: 127 (91%)
- INFERRED: 12 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*