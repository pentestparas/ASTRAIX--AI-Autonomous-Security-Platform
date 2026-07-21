# Community 25

> 21 nodes · cohesion 0.13

## Key Concepts

- **CancellationToken** (19 connections) — `backend/ai_secos_core/runtime/cancellation.py`
- **PlannedExecution** (14 connections) — `backend/ai_secos_core/runtime/task_planner.py`
- **CancelledError** (6 connections) — `backend/ai_secos_core/runtime/cancellation.py`
- **TaskRunResult** (6 connections) — `backend/ai_secos_core/runtime/executor.py`
- **NoopTaskExecutor** (5 connections) — `backend/ai_secos_core/runtime/executor.py`
- **.run()** (5 connections) — `backend/ai_secos_core/runtime/executor.py`
- **TaskExecutor** (5 connections) — `backend/ai_secos_core/runtime/executor.py`
- **.run()** (5 connections) — `backend/ai_secos_core/runtime/executor.py`
- **.run()** (5 connections) — `backend/ai_secos_core/runtime/task_planner.py`
- **executor.py** (4 connections) — `backend/ai_secos_core/runtime/executor.py`
- **cancellation.py** (3 connections) — `backend/ai_secos_core/runtime/cancellation.py`
- **.cancel()** (1 connections) — `backend/ai_secos_core/runtime/cancellation.py`
- **.is_cancelled()** (1 connections) — `backend/ai_secos_core/runtime/cancellation.py`
- **.wait()** (1 connections) — `backend/ai_secos_core/runtime/cancellation.py`
- **Cancellation token for running tasks/plans.  The platform-wide cancellation cont** (1 connections) — `backend/ai_secos_core/runtime/cancellation.py`
- **A typed alias for cancellation that originates from the platform.** (1 connections) — `backend/ai_secos_core/runtime/cancellation.py`
- **Lightweight, async-friendly cancellation.** (1 connections) — `backend/ai_secos_core/runtime/cancellation.py`
- **Task Executor — runs a Task.  A planner produces Tasks; the executor is what run** (1 connections) — `backend/ai_secos_core/runtime/executor.py`
- **Run a single Task and emit a result.** (1 connections) — `backend/ai_secos_core/runtime/executor.py`
- **Default at Milestone 1.      The executor performs the bare minimum: a `result`-** (1 connections) — `backend/ai_secos_core/runtime/executor.py`
- **Outcome of one full plan run.** (1 connections) — `backend/ai_secos_core/runtime/task_planner.py`

## Relationships

- [[Community 36]] (14 shared connections)
- [[Metrics System]] (11 shared connections)
- [[Community 33]] (3 shared connections)
- [[Workflow Engine]] (2 shared connections)
- [[Task & Risk Types]] (1 shared connections)

## Source Files

- `backend/ai_secos_core/runtime/cancellation.py`
- `backend/ai_secos_core/runtime/executor.py`
- `backend/ai_secos_core/runtime/task_planner.py`

## Audit Trail

- EXTRACTED: 60 (69%)
- INFERRED: 27 (31%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*