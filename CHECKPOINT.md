# CHECKPOINT — AstraIX continuation point

> Created 2026-08-14. Read this first after any system update/restart to resume work.
> Last commit: `c87c533` (pushed to GitHub master).

## 1. System state after restart

Stack is brought up with:

```bash
cd /Users/paras.patil/AI-native Security Engineering Platform/astraix-security-analyst
docker compose up -d        # starts postgres, redis, neo4j, backend, frontend, nginx, zap, juice-shop
```

Verify health:

```bash
curl http://localhost:8000/health          # backend 200
curl http://localhost:3000                 # frontend 200
```

- Login: `demo@astraix.com` / `demo123456`
- Auth token: `/tmp/astraix_token.txt` (re-login on 401 via `/api/v1/auth/login/json`)
- Backend code is bind-mounted → restarts pick up changes; frontend is a baked image → `docker compose build frontend && docker compose up -d --no-deps frontend` after FE changes.
- Kali tool image: `astraix-kali:latest` (includes `/opt/vapt/web_form_scanner.py` — forms tool).
- Postgres data persists in named volumes (data verified post-restart: 124 findings, 8 assessments, 6 completed).

## 2. Product features live right now

1. **Approval UI works** — backend publishes `tool_approval_resolved` events + 300s TTL on pending approvals; frontend clears approved/rejected cards immediately (scan page).
2. **Vulnerabilities (true positives only)** — findings API excludes `false_positive` by default; `GET /api/v1/findings?status=false_positive` shows them. Main `/findings` page + project detail Findings tab show proper Severity/Title/Asset/CVSS/Age columns; click a row → full finding detail dialog (description, remediation, references, evidence JSON, status changer).
3. **Attack surface graph** (`/graph`) — layouts: Radial (default) + Force only (dagre LR/TB removed).
4. **forms tool** — probes API endpoints, SQLi/NoSQLi params + bodies, XSS forms, chatbot injection; normalized titles (SQL Injection (SQLi), NoSQL Injection, …) + CVSS via `backend/app/vapt/normalizer.py`.
5. **Loopback target resolution** — `localhost`/`127.0.0.1` targets rewritten to `host.docker.internal` in `executor._resolve_target()`.

## 3. Scan history (validated)

| Scan | Target | Result |
|------|--------|--------|
| #11 `4d5e6f7a…` | http://localhost:3002 | completed, 4 raw findings (pre-normalizer), persisted |
| #12 `5e6f7a8b…` | http://localhost:3002 | completed, 6 findings, HIGH risk, normalized + persisted, CVSS set |

DB truth: 124 findings (112 false_positive noise backfill, 12 true positives), 8 assessments (6 completed).

## 4. Known issues / gotchas

- **juice-shop** crashes on NoSQLi `$ne` payloads (node 0-exit); restart policy brings it back — `docker start juice-shop`.
- Backend restart kills in-flight scans (scan state is in-process). Approvals must be answered manually via UI (no auto-approve poller running).
- `graphify-out/` is gitignored; graph artifacts (graph.json, GRAPH_REPORT.md, graph.html, manifest.json, wiki/) are force-added on commit. `graphify update .` refreshes the code graph.
- Redis scan event keys are lowercase scan ids: `scan:progress:{scan_id}:events` / `:status`.
- Uncommitted leftovers (not ours): `training-data/kaggle-security-datasets/*` whitespace changes; dirty git submodules `knowledge-base/sources/*`.

## 5. Next steps (when resuming)

1. Run a fresh scan (e.g. target `http://localhost:3002`) and verify: approvals appear → Approve/Reject from UI works live; findings land as true positives with canonical titles/CVSS.
2. Any commit of new work: `graphify update .` → stage code + `git add -f graphify-out/{graph.json,graph.html,GRAPH_REPORT.md,manifest.json}` → commit → push.
3. Suggested: verify Neo4j graph ingestion after scan (`graph_ready` event) and reports page with scan12 data.
