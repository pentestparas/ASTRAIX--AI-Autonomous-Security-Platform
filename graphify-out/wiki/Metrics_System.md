# Metrics System

> 74 nodes · cohesion 0.06

## Key Concepts

- **PluginManifest** (26 connections) — `backend/ai_secos_core/plugin_system/manifest.py`
- **EventDispatcher** (22 connections) — `backend/ai_secos_core/shared/events.py`
- **PluginExecutionRequest** (21 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **PluginExecutor** (21 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **PluginSandbox** (21 connections) — `backend/ai_secos_core/plugin_system/sandbox.py`
- **TaskPlanner** (18 connections) — `backend/ai_secos_core/runtime/task_planner.py`
- **MetricsRegistry** (17 connections) — `backend/ai_secos_core/infrastructure/metrics.py`
- **TaskExecutor** (17 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **Counter** (16 connections) — `backend/ai_secos_core/infrastructure/metrics.py`
- **Histogram** (16 connections) — `backend/ai_secos_core/infrastructure/metrics.py`
- **PluginExecutionResult** (15 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **TaskPlannerConfig** (15 connections) — `backend/ai_secos_core/runtime/task_planner.py`
- **NoopTaskExecutor** (13 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **PluginExecutionStatus** (13 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **SandboxDecision** (13 connections) — `backend/ai_secos_core/plugin_system/sandbox.py`
- **SandboxViolation** (12 connections) — `backend/ai_secos_core/plugin_system/sandbox.py`
- **executor.py** (10 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **._run_subprocess()** (9 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **ProgressTicker** (9 connections) — `backend/ai_secos_core/runtime/plugin_streaming.py`
- **StreamingPluginExecutor** (9 connections) — `backend/ai_secos_core/runtime/plugin_streaming.py`
- **metrics.py** (7 connections) — `backend/ai_secos_core/infrastructure/metrics.py`
- **.execute()** (7 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **.execute()** (6 connections) — `backend/ai_secos_core/runtime/plugin_streaming.py`
- **._emit_event()** (5 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- **.__init__()** (5 connections) — `backend/ai_secos_core/plugin_system/executor.py`
- *... and 49 more nodes in this community*

## Relationships

- [[Assessment API]] (25 shared connections)
- [[App Factory & Null Providers]] (16 shared connections)
- [[Plugin Loader]] (13 shared connections)
- [[Community 25]] (11 shared connections)
- [[Community 36]] (8 shared connections)
- [[Community 26]] (7 shared connections)
- [[Task & Risk Types]] (5 shared connections)
- [[Workflow Engine]] (4 shared connections)
- [[Community 59]] (3 shared connections)
- [[Plugin Schemas]] (2 shared connections)
- [[Community 35]] (2 shared connections)
- [[Community 39]] (1 shared connections)

## Source Files

- `backend/ai_secos_core/infrastructure/metrics.py`
- `backend/ai_secos_core/plugin_system/executor.py`
- `backend/ai_secos_core/plugin_system/manifest.py`
- `backend/ai_secos_core/plugin_system/sandbox.py`
- `backend/ai_secos_core/runtime/plugin_streaming.py`
- `backend/ai_secos_core/runtime/task_planner.py`
- `backend/ai_secos_core/shared/events.py`

## Audit Trail

- EXTRACTED: 219 (51%)
- INFERRED: 212 (49%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*