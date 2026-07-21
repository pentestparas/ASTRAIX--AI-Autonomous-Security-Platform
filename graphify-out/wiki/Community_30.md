# Community 30

> 19 nodes · cohesion 0.18

## Key Concepts

- **auth.py** (17 connections) — `backend/app/core/auth.py`
- **get_current_user()** (13 connections) — `backend/app/core/auth.py`
- **get_current_active_user()** (8 connections) — `backend/app/core/auth.py`
- **get_user_projects()** (8 connections) — `backend/app/core/auth.py`
- **.__call__()** (8 connections) — `backend/app/core/auth.py`
- **get_user_organizations()** (7 connections) — `backend/app/core/auth.py`
- **Depends** (6 connections)
- **get_current_superuser()** (4 connections) — `backend/app/core/auth.py`
- **has_permission()** (4 connections) — `backend/app/core/auth.py`
- **get_role_permissions()** (3 connections) — `backend/app/core/auth.py`
- **decode_token()** (2 connections) — `backend/app/core/auth.py`
- **api_key_header** (1 connections)
- **Get permissions for a role.** (1 connections) — `backend/app/core/auth.py`
- **Check if a role has a specific permission.** (1 connections) — `backend/app/core/auth.py`
- **Get all organizations the current user is a member of.** (1 connections) — `backend/app/core/auth.py`
- **Get all projects in an organization the user has access to.** (1 connections) — `backend/app/core/auth.py`
- **Get current user from JWT token or API key.** (1 connections) — `backend/app/core/auth.py`
- **http_bearer** (1 connections)
- **HTTPAuthorizationCredentials** (1 connections)

## Relationships

- [[Organizations API]] (7 shared connections)
- [[Projects API]] (5 shared connections)
- [[Plugin Schemas]] (4 shared connections)
- [[Assets & Sessions]] (4 shared connections)
- [[Community 49]] (3 shared connections)
- [[FastAPI Dependencies]] (2 shared connections)
- [[Community 27]] (2 shared connections)
- [[Community 38]] (1 shared connections)

## Source Files

- `backend/app/core/auth.py`

## Audit Trail

- EXTRACTED: 86 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*