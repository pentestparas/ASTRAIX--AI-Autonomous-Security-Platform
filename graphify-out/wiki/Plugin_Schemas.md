# Plugin Schemas

> 122 nodes · cohesion 0.05

## Key Concepts

- **BaseModel** (69 connections) — `backend/app/models/base.py`
- **RoleName** (55 connections) — `backend/app/domain/models/organization.py`
- **auth.py** (47 connections) — `backend/app/api/v1/auth.py`
- **datetime** (43 connections)
- **ApiKey** (30 connections) — `backend/app/domain/models/organization.py`
- **Membership** (30 connections) — `backend/app/domain/models/organization.py`
- **Organization** (30 connections) — `backend/app/domain/models/organization.py`
- **Project** (30 connections) — `backend/app/domain/models/organization.py`
- **User** (30 connections) — `backend/app/domain/models/organization.py`
- **organization.py** (27 connections) — `backend/app/domain/schemas/organization.py`
- **Base** (16 connections) — `backend/app/database/session.py`
- **UUIDMixin** (14 connections) — `backend/app/models/base.py`
- **RequiresPermission** (14 connections) — `backend/app/core/auth.py`
- **TimestampMixin** (13 connections) — `backend/app/models/base.py`
- **Permission** (13 connections) — `backend/app/core/auth.py`
- **Finding** (13 connections) — `backend/app/domain/models/finding.py`
- **AuditLog** (13 connections) — `backend/app/domain/models/organization.py`
- **organization.py** (10 connections) — `backend/app/domain/models/organization.py`
- **Token** (10 connections) — `backend/app/api/v1/auth.py`
- **TimestampMixin** (9 connections)
- **UUIDMixin** (9 connections)
- **ApiKeyCreate** (9 connections) — `backend/app/api/v1/auth.py`
- **ApiKeyCreateResponse** (9 connections) — `backend/app/api/v1/auth.py`
- **MembershipCreate** (9 connections) — `backend/app/api/v1/auth.py`
- **MembershipUpdate** (9 connections) — `backend/app/api/v1/auth.py`
- *... and 97 more nodes in this community*

## Relationships

- [[Projects API]] (30 shared connections)
- [[Community 27]] (16 shared connections)
- [[Community 38]] (13 shared connections)
- [[Community 32]] (13 shared connections)
- [[Organizations API]] (13 shared connections)
- [[Task & Risk Types]] (10 shared connections)
- [[Assessment API]] (8 shared connections)
- [[Assets & Sessions]] (8 shared connections)
- [[Community 46]] (8 shared connections)
- [[Workflow Engine]] (8 shared connections)
- [[Context Building]] (5 shared connections)
- [[Community 49]] (5 shared connections)

## Source Files

- `backend/ai_secos_core/plugin_system/manifest.py`
- `backend/app/api/v1/auth.py`
- `backend/app/core/auth.py`
- `backend/app/database/session.py`
- `backend/app/domain/models/assessment.py`
- `backend/app/domain/models/asset.py`
- `backend/app/domain/models/base.py`
- `backend/app/domain/models/finding.py`
- `backend/app/domain/models/organization.py`
- `backend/app/domain/schemas/assessment.py`
- `backend/app/domain/schemas/asset.py`
- `backend/app/domain/schemas/finding.py`
- `backend/app/domain/schemas/organization.py`
- `backend/app/models/base.py`
- `backend/app/plugins/manifest.py`

## Audit Trail

- EXTRACTED: 531 (57%)
- INFERRED: 399 (43%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*