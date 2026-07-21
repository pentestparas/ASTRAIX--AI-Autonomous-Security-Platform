# Community 40

> 15 nodes · cohesion 0.18

## Key Concepts

- **Orchestrator** (12 connections) — `backend/app/orchestrator/service.py`
- **.run_assessment()** (8 connections) — `backend/app/orchestrator/service.py`
- **._persist_findings()** (7 connections) — `backend/app/orchestrator/service.py`
- **._run_plugins()** (6 connections) — `backend/app/orchestrator/service.py`
- **._resolve_plugins()** (5 connections) — `backend/app/orchestrator/service.py`
- **get_orchestrator()** (4 connections) — `backend/app/orchestrator/service.py`
- **._fingerprint()** (4 connections) — `backend/app/orchestrator/service.py`
- **Asset** (2 connections)
- **Resolve plugins for an assessment.** (1 connections) — `backend/app/orchestrator/service.py`
- **Run plugins in parallel.** (1 connections) — `backend/app/orchestrator/service.py`
- **Process plugin findings, dedupe, persist.** (1 connections) — `backend/app/orchestrator/service.py`
- **Stable identifier: title + asset.** (1 connections) — `backend/app/orchestrator/service.py`
- **Singleton orchestrator.** (1 connections) — `backend/app/orchestrator/service.py`
- **Coordinator: schedules + runs assessments.** (1 connections) — `backend/app/orchestrator/service.py`
- **Run an assessment by ID. Updates state as we progress.** (1 connections) — `backend/app/orchestrator/service.py`

## Relationships

- [[Community 34]] (5 shared connections)
- [[Task & Risk Types]] (3 shared connections)
- [[Assets & Sessions]] (2 shared connections)
- [[Community 46]] (2 shared connections)
- [[Community 35]] (1 shared connections)
- [[Assessment API]] (1 shared connections)
- [[Plugin Schemas]] (1 shared connections)
- [[Community 39]] (1 shared connections)
- [[Projects API]] (1 shared connections)

## Source Files

- `backend/app/orchestrator/service.py`

## Audit Trail

- EXTRACTED: 51 (93%)
- INFERRED: 4 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*