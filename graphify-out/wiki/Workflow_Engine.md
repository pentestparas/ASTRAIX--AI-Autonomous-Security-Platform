# Workflow Engine

> 51 nodes · cohesion 0.06

## Key Concepts

- **Workflow** (24 connections) — `backend/ai_secos_core/shared/value_objects.py`
- **value_objects.py** (17 connections) — `backend/ai_secos_core/shared/value_objects.py`
- **WorkflowRecord** (11 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **WorkflowEngine** (9 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **WorkflowStep** (9 connections) — `backend/ai_secos_core/shared/value_objects.py`
- **load_workflow_from_yaml()** (8 connections) — `backend/ai_secos_core/runtime/workflow.py`
- **Capability** (7 connections) — `backend/ai_secos_core/shared/value_objects.py`
- **test_diamond_workflow()** (5 connections) — `backend/ai_secos_core/tests/runtime/test_task_planner.py`
- **test_linear_workflow()** (5 connections) — `backend/ai_secos_core/tests/runtime/test_task_planner.py`
- **workflow_engine.py** (5 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **.get()** (5 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **WorkflowResolutionError** (5 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **WorkflowLoaderError** (5 connections) — `backend/ai_secos_core/runtime/workflow.py`
- **WorkflowId** (5 connections)
- **test_task_planner.py** (4 connections) — `backend/ai_secos_core/tests/runtime/test_task_planner.py`
- **workflow.py** (4 connections) — `backend/ai_secos_core/runtime/workflow.py`
- **CapabilityVersion** (4 connections) — `backend/ai_secos_core/shared/value_objects.py`
- **Confidence** (4 connections) — `backend/ai_secos_core/shared/value_objects.py`
- **.list()** (3 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **.register()** (3 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **.register_capability()** (3 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **.get()** (3 connections) — `backend/ai_secos_core/runtime/workflow_engine.py`
- **_YamlBundle** (3 connections) — `backend/ai_secos_core/runtime/workflow.py`
- **ComplianceTag** (3 connections) — `backend/ai_secos_core/shared/value_objects.py`
- **RequiredPlugin** (3 connections) — `backend/ai_secos_core/shared/value_objects.py`
- *... and 26 more nodes in this community*

## Relationships

- [[Assessment API]] (14 shared connections)
- [[Plugin Schemas]] (8 shared connections)
- [[Metrics System]] (4 shared connections)
- [[Community 42]] (4 shared connections)
- [[App Factory & Null Providers]] (2 shared connections)
- [[Community 48]] (2 shared connections)
- [[Task & Risk Types]] (2 shared connections)
- [[Community 25]] (2 shared connections)
- [[Community 36]] (2 shared connections)
- [[Community 31]] (1 shared connections)
- [[Community 69]] (1 shared connections)
- [[Context Building]] (1 shared connections)

## Source Files

- `backend/ai_secos_core/runtime/workflow.py`
- `backend/ai_secos_core/runtime/workflow_engine.py`
- `backend/ai_secos_core/shared/value_objects.py`
- `backend/ai_secos_core/tests/runtime/test_task_planner.py`

## Audit Trail

- EXTRACTED: 143 (76%)
- INFERRED: 46 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*