# Community 34

> 17 nodes · cohesion 0.21

## Key Concepts

- **Orchestrator** (14 connections) — `backend/app/domain/services/orchestrator.py`
- **Assessment** (12 connections)
- **._process_results()** (10 connections) — `backend/app/domain/services/orchestrator.py`
- **.run_assessment()** (8 connections) — `backend/app/domain/services/orchestrator.py`
- **._run_plugin()** (7 connections) — `backend/app/domain/services/orchestrator.py`
- **._fingerprint_finding()** (5 connections) — `backend/app/domain/services/orchestrator.py`
- **._resolve_plugins()** (5 connections) — `backend/app/domain/services/orchestrator.py`
- **._auto_select_plugins()** (4 connections) — `backend/app/domain/services/orchestrator.py`
- **._build_params()** (4 connections) — `backend/app/domain/services/orchestrator.py`
- **Finding** (2 connections)
- **Build plugin invocation params from assessment.** (1 connections) — `backend/app/domain/services/orchestrator.py`
- **Persist plugins' findings.** (1 connections) — `backend/app/domain/services/orchestrator.py`
- **Generate fingerprint: title + asset + plugin + severity.** (1 connections) — `backend/app/domain/services/orchestrator.py`
- **Sequences assessment execution: plugins → findings.** (1 connections) — `backend/app/domain/services/orchestrator.py`
- **Execute an assessment by ID.** (1 connections) — `backend/app/domain/services/orchestrator.py`
- **Resolve plugins based on assessment metadata.** (1 connections) — `backend/app/domain/services/orchestrator.py`
- **Default plugin selection.** (1 connections) — `backend/app/domain/services/orchestrator.py`

## Relationships

- [[Community 40]] (5 shared connections)
- [[Community 46]] (3 shared connections)
- [[Community 29]] (2 shared connections)
- [[Plugin Loader]] (2 shared connections)
- [[Assets & Sessions]] (2 shared connections)
- [[Community 51]] (2 shared connections)
- [[Assessment API]] (1 shared connections)
- [[Plugin Schemas]] (1 shared connections)
- [[Community 39]] (1 shared connections)
- [[Projects API]] (1 shared connections)

## Source Files

- `backend/app/domain/services/orchestrator.py`

## Audit Trail

- EXTRACTED: 74 (95%)
- INFERRED: 4 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*