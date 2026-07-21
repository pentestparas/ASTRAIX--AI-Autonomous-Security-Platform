# Community 35

> 17 nodes · cohesion 0.16

## Key Concepts

- **PluginRegistry** (14 connections) — `backend/app/plugins/registry.py`
- **PluginInstance** (10 connections) — `backend/app/plugins/registry.py`
- **registry.py** (6 connections) — `backend/app/plugins/registry.py`
- **get_plugin_registry()** (6 connections) — `backend/app/plugins/registry.py`
- **.run_plugin()** (6 connections) — `backend/app/plugins/registry.py`
- **._execute()** (5 connections) — `backend/app/plugins/registry.py`
- **.load_plugins()** (5 connections) — `backend/app/plugins/registry.py`
- **.get_plugin()** (2 connections) — `backend/app/plugins/registry.py`
- **._run_subprocess()** (2 connections) — `backend/app/plugins/registry.py`
- **.__init__()** (1 connections) — `backend/app/plugins/registry.py`
- **Execute plugin subprocess. Returns (output, error).** (1 connections) — `backend/app/plugins/registry.py`
- **Run subprocess synchronously. Returns (stdout, stderr).** (1 connections) — `backend/app/plugins/registry.py`
- **Singleton plugin registry.** (1 connections) — `backend/app/plugins/registry.py`
- **Loaded plugin: metadata + path.** (1 connections) — `backend/app/plugins/registry.py`
- **Lifecycle: discover → load → run → results.      Plugins are subprocesses:** (1 connections) — `backend/app/plugins/registry.py`
- **Discover plugins and validate manifests.          Returns: list of plugin IDs.** (1 connections) — `backend/app/plugins/registry.py`
- **Run plugin as subprocess.          Args:             plugin_id: Plugin identifie** (1 connections) — `backend/app/plugins/registry.py`

## Relationships

- [[Community 46]] (8 shared connections)
- [[Plugin Schemas]] (3 shared connections)
- [[Metrics System]] (2 shared connections)
- [[Plugin Loader]] (2 shared connections)
- [[Community 33]] (2 shared connections)
- [[Projects API]] (1 shared connections)
- [[FastAPI Dependencies]] (1 shared connections)
- [[Community 40]] (1 shared connections)

## Source Files

- `backend/app/plugins/registry.py`

## Audit Trail

- EXTRACTED: 53 (83%)
- INFERRED: 11 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*