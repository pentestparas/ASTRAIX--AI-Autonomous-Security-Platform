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
| `backend/app/api/v1/auth.py` | Login at `/login` (OAuth2 form) and `/login/json` (JSON) |
| `frontend/src/app/(main)/vapt/page.tsx` | VAPT scan UI (uses `projectsApi.list()` for auth'd project fetch) |
| `docker/kali-tools.Dockerfile` | Custom Kali image with nmap, nikto, sqlmap, nuclei, gobuster, sslscan |
| `docker-compose.yml` | Full stack: postgres, redis, backend, frontend |

## Demo Credentials

- **Email**: `demo@astraix.com`
- **Password**: `demo123456`

## Docker Environment

- Backend container runs as **root** (no gosu, no USER directive)
- Docker socket mounted at `/var/run/docker.sock`
- `VAPT_USE_DOCKER=true`, `VAPT_DEMO_MODE=false`
- Kali image: `astraix-kali:latest` (NOT `kalilinux/kali-rolling:latest` which has zero tools)

## Known Issues (Fixed)

1. **Project dropdown empty** — Fixed by changing VAPT page from plain `fetch()` to `projectsApi.list()` (includes auth header). See `frontend/src/app/(main)/vapt/page.tsx:116-138`.
2. **gosu crash** — Removed `USER appuser` and gosu from backend Dockerfile; uvicorn runs as root directly.

## VAPT API Flow

```
POST /api/v1/vapt/scan/quick
  → backend/app/vapt/routes.py:scan_quick()
    → executor.py: execute_scan() → docker run astraix-kali:latest nmap/nikto/sqlmap/nuclei/gobuster/sslscan
    → normalizer.py: tool_output → SecurityFinding[]
    → risk_engine: score findings
    → ai_gateway: Gemini summary
    → DB persist → return ScanResult
```

## Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `VAPT_USE_DOCKER` | `true` | Real Docker exec (not demo mode) |
| `VAPT_DEMO_MODE` | `false` | Set `true` for simulated results |
| `KALI_IMAGE` | `astraix-kali:latest` | Custom image with tools |

## Running the Stack

```bash
docker-compose up -d
curl http://localhost:8000/health
# Login at http://localhost:3000 (demo@astraix.com / demo123456)
```

## Build Custom Kali Image

```bash
docker build -f docker/kali-tools.Dockerfile -t astraix-kali:latest .
```

## Lint & Type Check

```bash
# Frontend
cd frontend && npm run type-check && npm run build

# Backend (in container or venv)
cd backend && pip install -r requirements.txt && python -c "import app.main"
```

## Recent Commits

1. `c62512e` — Add VAPT Docker executor with custom Kali image
2. `73d735e` — Fix VAPT project dropdown auth - use projectsApi instead of plain fetch