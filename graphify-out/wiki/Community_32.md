# Community 32

> 19 nodes · cohesion 0.15

## Key Concepts

- **MembershipRepository** (35 connections) — `backend/app/repositories/organization.py`
- **Membership** (8 connections)
- **create_organization()** (6 connections) — `backend/app/api/v1/organizations.py`
- **list_memberships()** (5 connections) — `backend/app/api/v1/auth.py`
- **remove_member()** (5 connections) — `backend/app/api/v1/auth.py`
- **.get()** (3 connections) — `backend/app/repositories/organization.py`
- **.get_organization_memberships()** (3 connections) — `backend/app/repositories/organization.py`
- **.get_project_memberships()** (3 connections) — `backend/app/repositories/organization.py`
- **.get_user_membership()** (3 connections) — `backend/app/repositories/organization.py`
- **.get_user_memberships()** (3 connections) — `backend/app/repositories/organization.py`
- **.get_user_project_memberships()** (3 connections) — `backend/app/repositories/organization.py`
- **get_membership_repo()** (3 connections) — `backend/app/api/v1/auth.py`
- **.create()** (2 connections) — `backend/app/repositories/organization.py`
- **.__init__()** (2 connections) — `backend/app/repositories/organization.py`
- **.update()** (2 connections) — `backend/app/repositories/organization.py`
- **OrganizationCreate** (1 connections)
- **List organization or project memberships.** (1 connections) — `backend/app/api/v1/auth.py`
- **Remove a member from organization or project.** (1 connections) — `backend/app/api/v1/auth.py`
- **Create a new organization.** (1 connections) — `backend/app/api/v1/organizations.py`

## Relationships

- [[Plugin Schemas]] (13 shared connections)
- [[Organizations API]] (10 shared connections)
- [[Projects API]] (9 shared connections)
- [[Community 27]] (4 shared connections)
- [[Assets & Sessions]] (4 shared connections)

## Source Files

- `backend/app/api/v1/auth.py`
- `backend/app/api/v1/organizations.py`
- `backend/app/repositories/organization.py`

## Audit Trail

- EXTRACTED: 83 (92%)
- INFERRED: 7 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*