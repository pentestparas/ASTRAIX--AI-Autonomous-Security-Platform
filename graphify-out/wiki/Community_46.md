# Community 46

> 13 nodes · cohesion 0.19

## Key Concepts

- **PluginRunResult** (10 connections) — `backend/app/plugins/registry.py`
- **plugin.py** (8 connections) — `backend/app/domain/models/plugin.py`
- **PluginError** (7 connections) — `backend/app/domain/models/plugin.py`
- **PluginOutput** (7 connections) — `backend/app/domain/models/plugin.py`
- **AssessmentStatus** (6 connections) — `backend/app/domain/services/orchestrator.py`
- **FindingOut** (5 connections) — `backend/app/domain/models/plugin.py`
- **orchestrator.py** (5 connections) — `backend/app/domain/services/orchestrator.py`
- **PluginManifest** (3 connections) — `backend/app/domain/models/plugin.py`
- **PluginStatus** (2 connections) — `backend/app/domain/models/plugin.py`
- **.id_validator()** (1 connections) — `backend/app/domain/models/plugin.py`
- **Result of running a plugin.** (1 connections) — `backend/app/plugins/registry.py`
- **Orchestrator Service  The orchestrator runs assessments via the plugin system:** (1 connections) — `backend/app/domain/services/orchestrator.py`
- **Assessment lifecycle states.** (1 connections) — `backend/app/domain/services/orchestrator.py`

## Relationships

- [[Plugin Schemas]] (8 shared connections)
- [[Community 35]] (8 shared connections)
- [[Community 34]] (3 shared connections)
- [[Task & Risk Types]] (2 shared connections)
- [[Projects API]] (2 shared connections)
- [[Community 40]] (2 shared connections)
- [[Metrics System]] (1 shared connections)
- [[Assessment API]] (1 shared connections)

## Source Files

- `backend/app/domain/models/plugin.py`
- `backend/app/domain/services/orchestrator.py`
- `backend/app/plugins/registry.py`

## Audit Trail

- EXTRACTED: 36 (63%)
- INFERRED: 21 (37%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*