# Community 37

> 16 nodes · cohesion 0.19

## Key Concepts

- **ProviderManager** (20 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **AIProvider** (10 connections) — `backend/ai_secos_core/ai_gateway/provider.py`
- **.register()** (5 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **manager.py** (4 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **ProviderAlreadyRegisteredError** (4 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **ProviderNotFoundError** (4 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **.get()** (3 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **.__init__()** (3 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **.clear()** (1 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **.has()** (1 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **.ids()** (1 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **.unregister()** (1 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **Provider Manager.  The Manager owns the lifecycle of providers. Applications nev** (1 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **Thread-safe registry of providers.      The Manager is the *only* place provider** (1 connections) — `backend/ai_secos_core/ai_gateway/manager.py`
- **.health()** (1 connections) — `backend/ai_secos_core/ai_gateway/provider.py`
- **Concrete providers (OpenAI/Anthropic/...) implement this.** (1 connections) — `backend/ai_secos_core/ai_gateway/provider.py`

## Relationships

- [[Community 41]] (5 shared connections)
- [[Community 48]] (3 shared connections)
- [[App Factory & Null Providers]] (3 shared connections)
- [[Community 22]] (2 shared connections)
- [[Community 55]] (2 shared connections)

## Source Files

- `backend/ai_secos_core/ai_gateway/manager.py`
- `backend/ai_secos_core/ai_gateway/provider.py`

## Audit Trail

- EXTRACTED: 47 (77%)
- INFERRED: 14 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*