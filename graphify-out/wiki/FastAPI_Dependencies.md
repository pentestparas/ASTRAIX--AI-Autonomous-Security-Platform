# FastAPI Dependencies

> 44 nodes · cohesion 0.05

## Key Concepts

- **FastAPI** (19 connections)
- **get_container()** (7 connections) — `backend/ai_secos_core/api_platform/dependencies.py`
- **main.py** (7 connections) — `backend/app/main.py`
- **_map_error()** (6 connections) — `backend/ai_secos_core/api_platform/error_handlers.py`
- **lifespan()** (6 connections) — `backend/app/main.py`
- **error_handlers.py** (5 connections) — `backend/ai_secos_core/api_platform/error_handlers.py`
- **routes.py** (5 connections) — `backend/ai_secos_core/api_platform/routes.py`
- **dependencies.py** (4 connections) — `backend/ai_secos_core/api_platform/dependencies.py`
- **health()** (4 connections) — `backend/ai_secos_core/api_platform/routes.py`
- **ready()** (4 connections) — `backend/ai_secos_core/api_platform/routes.py`
- **session.py** (4 connections) — `backend/app/database/session.py`
- **test_health.py** (4 connections) — `backend/tests/test_health.py`
- **get_settings()** (3 connections) — `backend/ai_secos_core/api_platform/dependencies.py`
- **register_exception_handlers()** (3 connections) — `backend/ai_secos_core/api_platform/error_handlers.py`
- **_safe()** (3 connections) — `backend/ai_secos_core/api_platform/error_handlers.py`
- **version()** (3 connections) — `backend/ai_secos_core/api_platform/routes.py`
- **AsyncClient** (3 connections)
- **__init__.py** (3 connections) — `backend/app/api/v1/__init__.py`
- **health_check()** (2 connections) — `backend/app/main.py`
- **readiness_check()** (2 connections) — `backend/app/main.py`
- **root()** (2 connections) — `backend/app/main.py`
- **close_db()** (2 connections) — `backend/app/database/session.py`
- **get_session()** (2 connections) — `backend/app/database/session.py`
- **init_db()** (2 connections) — `backend/app/database/session.py`
- **Request** (2 connections)
- *... and 19 more nodes in this community*

## Relationships

- [[App Factory & Null Providers]] (5 shared connections)
- [[Community 33]] (5 shared connections)
- [[Assets & Sessions]] (3 shared connections)
- [[Plugin Schemas]] (2 shared connections)
- [[Community 30]] (2 shared connections)
- [[Community 59]] (1 shared connections)
- [[Community 48]] (1 shared connections)
- [[Community 35]] (1 shared connections)
- [[Assessment API]] (1 shared connections)
- [[Community 50]] (1 shared connections)
- [[Community 54]] (1 shared connections)
- [[Organizations API]] (1 shared connections)

## Source Files

- `backend/ai_secos_core/api_platform/dependencies.py`
- `backend/ai_secos_core/api_platform/error_handlers.py`
- `backend/ai_secos_core/api_platform/routes.py`
- `backend/app/api/v1/__init__.py`
- `backend/app/database/session.py`
- `backend/app/main.py`
- `backend/tests/test_health.py`

## Audit Trail

- EXTRACTED: 117 (91%)
- INFERRED: 12 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*