# Community 31

> 19 nodes · cohesion 0.16

## Key Concepts

- **CapabilityRegistry** (23 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **CapabilityAlreadyRegisteredError** (8 connections) — `backend/ai_secos_core/capabilities/errors.py`
- **CapabilityNotFoundError** (8 connections) — `backend/ai_secos_core/capabilities/errors.py`
- **Capability** (7 connections)
- **.register()** (5 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **errors.py** (4 connections) — `backend/ai_secos_core/capabilities/errors.py`
- **.get()** (4 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **.register_from_manifest()** (4 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **.__init__()** (3 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **.list()** (3 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **registry.py** (2 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **Capability-specific error types.** (1 connections) — `backend/ai_secos_core/capabilities/errors.py`
- **Raised when attempting to register a duplicate capability.** (1 connections) — `backend/ai_secos_core/capabilities/errors.py`
- **Raised when a capability is not found in the registry.** (1 connections) — `backend/ai_secos_core/capabilities/errors.py`
- **.clear()** (1 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **.has()** (1 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **.ids()** (1 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **Capability Registry — typed lookup and lifecycle.  Thread-safe in-memory registr** (1 connections) — `backend/ai_secos_core/capabilities/registry.py`
- **Thread-safe registry of `Capability` instances keyed by id+version.      Capabil** (1 connections) — `backend/ai_secos_core/capabilities/registry.py`

## Relationships

- [[Capability Loader]] (8 shared connections)
- [[Assessment API]] (6 shared connections)
- [[Community 42]] (4 shared connections)
- [[Community 48]] (2 shared connections)
- [[Community 70]] (1 shared connections)
- [[Community 57]] (1 shared connections)
- [[Workflow Engine]] (1 shared connections)

## Source Files

- `backend/ai_secos_core/capabilities/errors.py`
- `backend/ai_secos_core/capabilities/registry.py`

## Audit Trail

- EXTRACTED: 54 (68%)
- INFERRED: 25 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*