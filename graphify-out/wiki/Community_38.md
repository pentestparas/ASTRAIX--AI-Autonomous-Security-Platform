# Community 38

> 16 nodes · cohesion 0.17

## Key Concepts

- **ApiKeyRepository** (31 connections) — `backend/app/repositories/organization.py`
- **ApiKey** (6 connections)
- **.create()** (5 connections) — `backend/app/repositories/organization.py`
- **list_api_keys()** (5 connections) — `backend/app/api/v1/auth.py`
- **toggle_api_key()** (5 connections) — `backend/app/api/v1/auth.py`
- **revoke_api_key()** (4 connections) — `backend/app/api/v1/auth.py`
- **.generate_key()** (3 connections) — `backend/app/repositories/organization.py`
- **.get_by_organization()** (3 connections) — `backend/app/repositories/organization.py`
- **.get_by_user()** (3 connections) — `backend/app/repositories/organization.py`
- **get_api_key_repo()** (3 connections) — `backend/app/api/v1/auth.py`
- **.get_by_hash()** (2 connections) — `backend/app/repositories/organization.py`
- **.hash_key()** (2 connections) — `backend/app/repositories/organization.py`
- **.__init__()** (2 connections) — `backend/app/repositories/organization.py`
- **.update()** (2 connections) — `backend/app/repositories/organization.py`
- **List API keys for organization.** (1 connections) — `backend/app/api/v1/auth.py`
- **Enable/disable an API key.** (1 connections) — `backend/app/api/v1/auth.py`

## Relationships

- [[Plugin Schemas]] (13 shared connections)
- [[Projects API]] (10 shared connections)
- [[Organizations API]] (7 shared connections)
- [[Assets & Sessions]] (4 shared connections)
- [[Community 49]] (1 shared connections)
- [[Community 30]] (1 shared connections)

## Source Files

- `backend/app/api/v1/auth.py`
- `backend/app/repositories/organization.py`

## Audit Trail

- EXTRACTED: 70 (90%)
- INFERRED: 8 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*