# AGENTS.md — AstraIX Security Analyst

## Project Overview

**AstraIX** is an AI-powered autonomous VAPT (Vulnerability Assessment & Penetration Testing) platform. It spawns real Kali Linux containers via Docker socket to execute actual security tools (nmap, nikto, sqlmap, nuclei, gobuster, sslscan), normalizes findings, scores risk, and provides AI-generated executive summaries.

**GitHub**: https://github.com/pentestparas/ASTRAIX--AI-Autonomous-Security-Platform

## Architecture

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Radix UI, Zustand
- **Backend**: FastAPI 0.110, Python 3.12, SQLAlchemy 2.0 (async), PostgreSQL, Redis
- **Container Exec**: Docker socket → `astraix-kali:latest` (custom Kali with tools pre-installed)
- **AI**: Gemini via AI gateway for risk analysis and executive summaries

## Key Files

| Path | Purpose |
|------|---------|
| `backend/app/vapt/executor.py` | Spawns Kali containers, runs security tools via Docker |
| `backend/app/vapt/normalizer.py` | Converts tool output → canonical SecurityFinding |
| `backend/app/vapt/routes.py` | API endpoints: `/scan/quick`, `/scans`, etc. |
| `backend/app/api/v1/auth.py` | Login at `/api/v1/auth/login` (OAuth2 form) and `/api/v1/auth/login/json` (JSON) |
| `frontend/src/app/(main)/vapt/page.tsx` | Redirect stub → `/scans` |
| `frontend/src/app/(main)/scans/page.tsx` | Unified scans page (quick scan + history + findings) |
| `frontend/src/app/api/v1/vapt/scan/route.ts` | Route handler proxy for VAPT scan (180s timeout, bypasses Next.js rewrite proxy) |
| `docker/kali-tools.Dockerfile` | Custom Kali image with nmap, nikto, sqlmap, nuclei, gobuster, sslscan |
| `docker-compose.yml` | Full stack: postgres, redis, neo4j, backend, frontend |
| `knowledge-base/` | Cybersecurity knowledge base (360+ sources, TF-IDF search) |
| `docker/kb-repos.txt` | Manifest of upstream KB repos fetched inside the Docker build (AV immunity) |
| `docker/fetch-kb.sh` | Build-time fetcher: clones manifest repos into `/opt/astraix-kb/sources` |
| `docker/kb-pull.sh` | Runtime helper: `docker exec astraix-backend kb-pull <url> [name]` — clones new KB sources straight into the container volume, never the host |
| `backend/app/vapt/agents/researcher.py` | Researcher Agent — enriches findings via knowledge base |
| `backend/app/vapt/agents/verifier.py` | Verifier Agent — re-exploits findings to eliminate FPs |

## Docker Environment

- Backend container runs as **root** (no gosu, no USER directive)
- Docker socket mounted at `/var/run/docker.sock`
- `VAPT_USE_DOCKER=true`
- Kali image: `astraix-kali:latest` (NOT `kalilinux/kali-rolling:latest` which has zero tools)
- **Knowledge base lives INSIDE Docker**: baked into the image at `/opt/astraix-kb` (via `COPY knowledge-base` in `docker/Dockerfile.backend`) and seeded on first boot by `docker/entrypoint.sh` into the named volume `kb-data` mounted at `/app/knowledge-base`. The host folder is NOT bind-mounted — host AV (Bitdefender) cannot delete/quarantine it. Seed condition: `/app/knowledge-base/embeddings/chunks.json` missing → reseed (edit sources inside the volume with `docker cp` or remove `kb-data` volume + restart to reseed from image).
- Knowledge base is accessible over HTTP (no direct FS access needed): `GET /api/v1/knowledge/search?q=...`, `/knowledge/stats`, `/knowledge/sources`, `/knowledge/source?path=sources/...` (path-traversal safe). AI agents consume it: planner (`KB_PATH=/app/knowledge-base`, TF-IDF/FAISS grounding), researcher (enrichment), verifier (best-effort `kb_exploit_context` on confirmed findings).

## Knowledge Base — NO HOST STORAGE RULE (AV immunity)

Host AV (Bitdefender) quarantines offensive-content KB files (reverse shells,
XSS payloads, CSV formulas → EPERM on read, breaks `git add`/`docker build`).
Therefore:

- **Upstream repo sources never live on the host**: they are excluded from the
  Docker build context via `.dockerignore` (`knowledge-base/sources/*`) and
  cloned INSIDE the build by `fetch-kb` from `docker/kb-repos.txt` into
  `/opt/astraix-kb/sources/<name>`; the entrypoint seeds them into the
  `kb-data` volume on first boot like the rest of the KB.
- **Adding NEW KB data → go straight into Docker**, never stage it on the host:
  ```bash
  docker exec astraix-backend kb-pull https://github.com/owner/repo [dir-name]
  ```
  Clones directly into `/app/knowledge-base/sources/<dir-name>` in the container
  volume. For many repos at once, add a `name=https://github.com/owner/repo`
  line to `docker/kb-repos.txt` and set `KB_SYNC_REPOS=true` in compose (rebuild
  image to bake it in permanently).
- Rebuild recipe: `docker-compose build backend && docker-compose up -d`
  (reset the `kb-data` volume to force a full reseed).

## Known Issues (Fixed)

1. **Project dropdown empty** — Fixed by changing VAPT page from plain `fetch()` to `projectsApi.list()` (includes auth header). See `frontend/src/app/(main)/vapt/page.tsx:116-138`.
2. **gosu crash** — Removed `USER appuser` and gosu from backend Dockerfile; uvicorn runs as root directly.
3. **VAPT scan proxy timeout (ECONNRESET)** — Next.js rewrite proxy had a ~30s timeout that killed long-running (~44s) VAPT scans. Fixed by creating `frontend/src/app/api/v1/vapt/scan/route.ts`, a Route Handler that proxies to the backend server-side with a configurable 180s AbortController timeout. Route Handlers in `app/api/` take precedence over `afterFiles` rewrites, so the Route Handler intercepts `POST /api/v1/vapt/scan` before the rewrite rule in `next.config.js` kicks in.

## VAPT API Flow

```
POST /api/v1/vapt/scan/quick
  → backend/app/vapt/routes.py:scan_quick()
    → orchestrator.py: analyze_and_scan()
      → recon.execute_scan() → executor.py: docker run astraix-kali:latest nmap/nikto/sqlmap/nuclei/gobuster/sslscan
      → researcher.enrich_findings() → knowledge base CVE lookup + context
      → verifier.verify_findings() → re-run tools to confirm findings
    → risk_engine: score findings
    → ai_gateway: Gemini summary
    → DB persist → return ScanResult
```

Multi-agent pipeline:
1. **ReconOrchestrator** — parallel tool execution (3 phases: recon → web → deep)
2. **ResearcherAgent** — enriches findings via 360-source knowledge base (CVEs, remediation, context)
3. **VerifierAgent** — re-exploits findings; unverifiable findings get downgraded severity
```

## Environment Variables

> **Secrets policy**: Never hardcode secrets. Real values live only in the
> gitignored `.env` (compose reads it automatically). `.env.example` is the
> tracked template — keep secrets blank there. Generate keys with
> `openssl rand -hex 32` (SECRET_KEY) or `openssl rand -base64 24` (passwords).
> Git credentials are stored via `git credential-helper osxkeychain` (no
> tokens in remote URLs / `.git/config`). GitHub Push Protection is enforced
> on this repo — a blocked push means a real secret is in the diff; find it
> before retrying.

| Variable | Value | Notes |
|----------|-------|-------|
| `VAPT_USE_DOCKER` | `true` | Real Docker exec |
| `KALI_IMAGE` | `astraix-kali:latest` | Custom image with tools |

## Running the Stack

```bash
docker-compose up -d
curl http://localhost:8000/health
# Register at http://localhost:3000/register then login
```

## Build Custom Kali Image

```bash
docker build -f docker/kali-tools.Dockerfile -t astraix-kali:latest .
```

## AI Transparency Panel (scan console)

The live scan console renders an "AI Reasoning — how the model worked" panel fed by four event types on the ScanProgressBus:

| Event | Emitted by | Payload |
|-------|-----------|---------|
| `llm_call` | `agent_loop._llm_turn`, `matrix._llm_json` | provider, model, purpose (`agent`/`matrix`/`chain`), ms, ok |
| `llm_stats` | orchestrator (after matrix phase, agent loop, and at scan end) | phase, calls, ok_calls, total_tokens, elapsed_ms, providers, purposes |
| `verdict` | `verifier.verify_findings` (per re-exploited finding) | finding, vulnerability_type, tool, verdict (`confirmed`/`downgraded`/`timed_out`/`unverified`), severity_before/after, confidence, detail, kb_context |
| `matrix_entry_done` | `orchestrator._run_matrix_phase` | id, endpoint, attack_type, suspicious, status, reason (LLM classification), poc_preview, tool, error |

Usage is tracked per scan by `backend/app/vapt/agents/llm_usage.py` (thread-safe, in-memory; `reset_llm_usage(scan_id)` is called at scan start). Token counts are real provider usage when available, else a 4-char/token estimate. All counters are visibility only — a failing tracker never fails the scan.

## Lint & Type Check

```bash
# Frontend
cd frontend && npm run type-check && npm run build

# Backend (in container or venv)
cd backend && pip install -r requirements.txt && python -c "import app.main"
```

## Recent Commits

1. `8308141` — Multi-agent pipeline: Researcher + Verifier agents (PentAGI/Xalgorix patterns)
2. `32e20ac` — Cybersecurity knowledge base (360+ sources, TF-IDF search API)
3. `ae00dbd` — Neo4j knowledge graph, parallel recon orchestrator, attack surface graph UI