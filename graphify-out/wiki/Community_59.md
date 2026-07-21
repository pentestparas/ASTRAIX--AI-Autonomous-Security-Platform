# Community 59

> 8 nodes · cohesion 0.36

## Key Concepts

- **get_correlation_id()** (9 connections) — `backend/ai_secos_core/shared/correlation.py`
- **new_correlation_id()** (6 connections) — `backend/ai_secos_core/shared/correlation.py`
- **CorrelationId** (5 connections)
- **correlation.py** (5 connections) — `backend/ai_secos_core/shared/correlation.py`
- **set_correlation_id()** (2 connections) — `backend/ai_secos_core/shared/correlation.py`
- **Correlation id context.  Every critical action (workflow, plugin exec, AI call)** (1 connections) — `backend/ai_secos_core/shared/correlation.py`
- **Produce a new opaque correlation id (UUID4 hex).** (1 connections) — `backend/ai_secos_core/shared/correlation.py`
- **Return the current correlation id, creating one if absent.      Use only at entr** (1 connections) — `backend/ai_secos_core/shared/correlation.py`

## Relationships

- [[Metrics System]] (3 shared connections)
- [[Platform Settings]] (2 shared connections)
- [[Assessment API]] (2 shared connections)
- [[Projects API]] (1 shared connections)
- [[FastAPI Dependencies]] (1 shared connections)
- [[Community 72]] (1 shared connections)

## Source Files

- `backend/ai_secos_core/shared/correlation.py`

## Audit Trail

- EXTRACTED: 23 (77%)
- INFERRED: 7 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*