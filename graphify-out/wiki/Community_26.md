# Community 26

> 21 nodes · cohesion 0.15

## Key Concepts

- **stream.py** (11 connections) — `backend/ai_secos_core/runtime/stream.py`
- **DomainEvent** (11 connections) — `backend/ai_secos_core/shared/events.py`
- **make_event()** (10 connections) — `backend/ai_secos_core/shared/events.py`
- **events.py** (6 connections) — `backend/ai_secos_core/shared/events.py`
- **emit_plugin_started()** (5 connections) — `backend/ai_secos_core/runtime/stream.py`
- **emit_plugin_completed()** (4 connections) — `backend/ai_secos_core/runtime/stream.py`
- **emit_plugin_finding()** (4 connections) — `backend/ai_secos_core/runtime/stream.py`
- **emit_plugin_progress()** (3 connections) — `backend/ai_secos_core/runtime/stream.py`
- **PluginCompletedPayload** (3 connections) — `backend/ai_secos_core/runtime/stream.py`
- **PluginFindingPayload** (3 connections) — `backend/ai_secos_core/runtime/stream.py`
- **PluginProgressPayload** (3 connections) — `backend/ai_secos_core/runtime/stream.py`
- **PluginStartedPayload** (3 connections) — `backend/ai_secos_core/runtime/stream.py`
- **.publish()** (2 connections) — `backend/ai_secos_core/shared/events.py`
- **.subscribe()** (2 connections) — `backend/ai_secos_core/shared/events.py`
- **.publish()** (2 connections) — `backend/ai_secos_core/shared/events.py`
- **.subscribe()** (2 connections) — `backend/ai_secos_core/shared/events.py`
- **Streaming contracts — typed event types for live plugin output.  M2 only defines** (1 connections) — `backend/ai_secos_core/runtime/stream.py`
- **Emit (and await the publish) for plugin.started.** (1 connections) — `backend/ai_secos_core/runtime/stream.py`
- **In-process event dispatcher protocol.  Application code (Workflow Engine, Plugin** (1 connections) — `backend/ai_secos_core/shared/events.py`
- **Base shape of every platform event.      Concrete events extend this with module** (1 connections) — `backend/ai_secos_core/shared/events.py`
- **Factory that stamps occurred_at and correlation id automatically.** (1 connections) — `backend/ai_secos_core/shared/events.py`

## Relationships

- [[Metrics System]] (7 shared connections)
- [[Assessment API]] (3 shared connections)
- [[Plugin Schemas]] (2 shared connections)
- [[Projects API]] (1 shared connections)
- [[Community 33]] (1 shared connections)
- [[Community 36]] (1 shared connections)

## Source Files

- `backend/ai_secos_core/runtime/stream.py`
- `backend/ai_secos_core/shared/events.py`

## Audit Trail

- EXTRACTED: 58 (73%)
- INFERRED: 21 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*