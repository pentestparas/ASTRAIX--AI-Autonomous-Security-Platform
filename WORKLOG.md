# AstraIX Worklog — Latest Track (2026-08-04)

Persistent session state for AI agents. This file is part of the graphify corpus so every session starts from the latest graph state.

## Objective

Deliver the AI-first scan experience: live scan console (phases, tools, commands, findings, timestamps) fed by the KB-grounded planner with Ollama-first LLM refinement, stall protection, and scan-under-project persistence.

## Current Status

- **KB-in-Docker: DONE** — knowledge base baked into backend image at `/opt/astraix-kb`, seeded on first boot by `docker/entrypoint.sh` into named volume `kb-data` mounted at `/app/knowledge-base` (host NOT bind-mounted — Bitdefender can't delete it). Seed condition: `/app/knowledge-base/embeddings/chunks.json` missing → reseed.
- **KB content: DONE** — 7 repos cloned into `knowledge-base/sources/` (3206 md files: Anthropic-Cybersecurity-Skills 2288, CAI-aliasrobotics 206, Berkanktk-CyberSecurity 130, others), PortSwigger Web Security Academy crawled (132 pages), OWASP projects fetched (5 files). Total on-disk sources: 3542.
- **FAISS index: DONE** — 7008 chunks, dim 384, vocab 92455. **CRITICAL fix**: fastembed `parallel=0` means "use ALL cores" → N ONNX workers → OOM/SIGKILL. Must pass `parallel=None` (single process). Verified ~9 chunks/s, ~13 min for 7008 chunks. Semantic search verified working (sqlmap → PortSwigger union attacks, cache poisoning → web-cache-poisoning).
- **KB HTTP access: DONE** — `GET /api/v1/knowledge/search?q=`, `/knowledge/stats`, `/knowledge/sources`, `/knowledge/source?path=...` (path-traversal safe, verified 400). Verifier does best-effort `_kb_exploit_context` on confirmed findings.

## Dashboard Work — IN PROGRESS

Todo list (ordered):

1. Backend `/dashboard/stats` real values — **IN PROGRESS** (total_projects from Project model count, active_scans from progress bus, scans_this_week/month from Assessment.started_at). Edit done in `backend/app/api/v1/__init__.py`, awaiting backend restart verification.
2. `GET /api/v1/system/status` with real component checks (Postgres, Redis, Neo4j `KnowledgeGraph._enabled`, Docker/Kali image, KB `search.stats()`), NOT fake Celery/MinIO/RabbitMQ.
3. `run_scan` (`backend/app/vapt/routes.py` ~lines 105-178): persist Assessment row at START (status running, under project), update on completion with everything (insights, plan, tool_results); `failed` status on error.
4. Frontend: `api.ts` — `systemApi.status()` + `vaptScanApi.detail()`.
5. Rewrite `SystemStatus.tsx` with real health components; remove fake CPU 34/RAM 67/RabbitMQ "High latency" rows.
6. Active-scan store (localStorage + events) so scan survives navigation; wire into scans page + Sidebar badge.
7. RecentAssessments auto-refresh while scan running.
8. Verify: backend import + curl stats/status, frontend tsc + build, run a scan to confirm project-scoped persistence.

## Environment Facts

- NGINX `:3001` → backend:8000; Next.js `:3000`; Redis 7 `:6379`; Postgres 16 `:5432` (db `astraix`, IDs varchar(36)); Neo4j 5.
- Backend code volume-mounted (`./backend:/app`, NO `--reload` → container restart required after backend edits). Frontend: `docker-compose up -d --build frontend`.
- Auth: `POST /api/v1/auth/login/json` with registered credentials → Bearer access_token.
- LLM: default `LLM_PROVIDER=ollama` (host.docker.internal:11434, huihui_ai/qwen2.5-abliterate:7b-instruct); NVIDIA NIM fallback deepseek-ai/deepseek-v4-pro (key in gitignored .env).
- Stage caps: `VAPT_PLAN_TIMEOUT=60`, `VAPT_RESEARCH_TIMEOUT=90`, `VAPT_VERIFY_ALL_TIMEOUT=240`, `VAPT_REPORT_TIMEOUT=60`, `VAPT_STALL_SECONDS=300`, `KB_EMBEDDER_TIMEOUT=25`. Verifier: Semaphore(3), 60s/tool, VAPT_VERIFY_TIMEOUT=75, HIGH/CRITICAL only.
- docker-py 7.2.0 removed `docker.errors.TimeoutError` → executor catches Exception, re-raises asyncio.TimeoutError when type name in (TimeoutError, ReadTimeout, ReadTimeoutError).
- Tool availability: `check_tool_availability()` checks Kali image `astraix-kali:latest` first, then host `which`.
- `GET /api/v1/vapt/scan/{id}/progress` via next.config.js rewrites. redis==5.0.0, openai==2.52.0 in image.
- Assessment row created only at scan completion → history empty for running scans (the persistence constraint for dashboard work).
- Git: prior commit `fef0e52` pushed. New KB work NOT yet committed (knowledge-base/, docker/Dockerfile.backend, docker/entrypoint.sh, docker-compose.yml, backend/app/api/v1/knowledge.py, backend/app/vapt/agents/verifier.py, AGENTS.md).

## Key Files

- `backend/app/vapt/routes.py`: run_scan — client_scan_id, progress endpoint, assessment created only at completion (~105-178).
- `backend/app/vapt/agents/verifier.py`: `_kb_exploit_context` on confirmed findings.
- `backend/app/vapt/agents/planner.py`: multi-provider `_llm_refine` (Ollama→NIM), KB-grounded plan_scan.
- `backend/app/vapt/orchestrator.py` watchdog + stage timeouts; `backend/app/vapt/progress.py` Redis/in-memory bus with `active_scans()`; `backend/app/vapt/executor.py` docker-py7 timeout handling; `backend/app/vapt/tools.py` Kali-image availability.
- `backend/app/api/v1/knowledge.py`: search/stats/rebuild + sources/source endpoints.
- `backend/app/api/v1/__init__.py`: `/dashboard/stats` (JUST EDITED — real values), `/dashboard/activity`.
- `backend/app/domain/models/organization.py:75`: Project model (organization_id, slug, is_active). Note: NOT `project.py` — model lives in organization.py.
- `knowledge-base/`: 15 source dirs, `PortSwigger_Web_Security_Academy/`, `OWASP_Projects/`, `embeddings/chunks.json` (7008), `build_faiss_index.py` (parallel=None).
- `docker/Dockerfile.backend` (baked KB), `docker/entrypoint.sh` (volume seed), `docker-compose.yml` (kb-data volume).
- Frontend dashboard files: `frontend/src/components/dashboard/SystemStatus.tsx`, `StatsCards.tsx`, `RecentAssessments.tsx`, `frontend/src/app/(main)/dashboard/page.tsx`, `frontend/src/components/layout/Sidebar.tsx`, `frontend/src/services/api.ts`, `frontend/src/types/index.ts`.
- `frontend/src/app/(main)/projects/[id]/page.tsx`: lists assessments by project_id (persistence gap is run_scan only writing at end).

## Completed History (recent)

1. Multi-agent pipeline: Researcher + Verifier agents (commit 8308141).
2. Cybersecurity knowledge base 360+ sources TF-IDF (commit 32e20ac).
3. Neo4j knowledge graph, parallel recon orchestrator, attack surface graph UI (commit ae00dbd).
4. KB-in-Docker seed architecture + volume (kb-data) — verified: "Seeded 917 KB files", 3542 disk sources.
5. New KB endpoints sources/source + path-traversal guard.
6. KB content expansion (repos + PortSwigger + OWASP) + re-index 7008 chunks + FAISS.
7. fastembed OOM fix: parallel=0 → parallel=None.
8. Verifier KB exploit context.
9. Image rebuilt so baked seed includes new content; running container restarted to load fresh in-memory KB.
10. /dashboard/stats real values edit (IN PROGRESS — syntax fix applied: `period_count` → async def).
