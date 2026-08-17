# AstraIX Security Analyst

**AI-Powered Autonomous VAPT (Vulnerability Assessment & Penetration Testing) Platform**

A production-quality AI Security Operating System that autonomously runs real security tools (nmap, nikto, sqlmap, nuclei, gobuster, sslscan) inside Kali containers, parses results into canonical findings, and provides AI-driven prioritization.

---

## Key Features

- **Real VAPT Execution** — Spawns isolated Kali Linux containers via Docker socket to run actual security tools (not simulations)
- **AI-Powered Insights** — Gemini-powered risk analysis, executive summaries, and remediation recommendations
- **End-to-End Pipeline** — Target → Discovery → Scanning → Normalized Findings → Risk Scoring → AI Summary → Executive Report
- **Multi-Tool Coverage** — nmap, nikto, sqlmap, nuclei, gobuster, sslscan pre-installed in custom Kali image
- **Plugin Architecture** — Extensible plugin system for adding new security tools
- **Modern UI** — Next.js 15 dashboard with project management, scan history, and findings triage

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js 14)                   │
│   Dashboard │ Projects │ Scans │ VAPT │ Findings │ Reports    │
└──────────────────────────┬───────────────────────────────────┘
                           │ REST API
                 ┌─────────▼──────────┐
                 │   FastAPI Backend   │
                 │   (uvicorn + SQLAlchemy 2.0 async)         │
                 └─────────┬──────────┘
                           │
        ┌──────────────────┼───────────────────┐
        │                  │                   │
┌───────▼───────┐ ┌────────▼───────┐ ┌────────▼────────┐
│  VAPT Executor │ │  Plugin System │ │    Database      │
│  (Docker socket│ │  (Extensible) │ │  (PostgreSQL)   │
│   → Kali cont.)│ │                │ │  (Redis cache)  │
└────────┬───────┘ └────────────────┘ └─────────────────┘
         │
┌────────▼────────┐
│ astraix-kali     │
│ (nmap, nikto,    │
│  sqlmap, nuclei, │
│  gobuster, etc.) │
└─────────────────┘
```

---

## Quick Start

### Prerequisites

- **Docker Desktop** (Mac ARM support confirmed)
- Docker API version 29.6.1+
- Clone the repository

### 1. Build the Custom Kali Image

```bash
docker build -f docker/kali-tools.Dockerfile -t astraix-kali:latest .
```

### 2. Start All Services

```bash
# Copy and edit environment
cp .env.example .env

# Start PostgreSQL, Redis, Backend, Frontend
docker-compose up -d

# Verify backend is healthy
curl http://localhost:8000/health
```

### 3. Access the Platform

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Login**: Register a new account at `http://localhost:3000/register` or use the API to create an organization and user

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VAPT_USE_DOCKER` | `true` | Enable real Docker-based VAPT execution |
| `VAPT_DEMO_MODE` | `false` | Run with simulated/tool-less results |
| `KALI_IMAGE` | `astraix-kali:latest` | Docker image for VAPT containers |
| `DATABASE_URL` | `postgresql+asyncpg://...` | PostgreSQL connection string |
| `SECRET_KEY` | (required) | JWT signing key |

---

## Project Structure

```
astraix-security-analyst/
├── backend/
│   ├── app/
│   │   ├── api/v1/           # REST API routes (auth, projects, findings, scans, vapt)
│   │   ├── core/             # Config, security, auth
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── repositories/    # Data access layer
│   │   ├── services/         # Business logic
│   │   ├── vapt/             # VAPT execution engine
│   │   │   ├── executor.py   # Docker container management
│   │   │   ├── normalizer.py # Tool output → canonical findings
│   │   │   └── routes.py    # Scan API endpoints
│   │   └── main.py           # FastAPI app entrypoint
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   │   ├── (main)/       # Authenticated pages
│   │   │   │   ├── vapt/      # VAPT scan interface
│   │   │   │   ├── scans/     # Scan history
│   │   │   │   ├── findings/  # Findings triage
│   │   │   │   └── projects/ # Project management
│   │   │   └── login/        # Login page
│   │   ├── components/       # Reusable UI components
│   │   ├── services/         # API client
│   │   └── types/            # TypeScript types
│   └── package.json
├── docker/
│   ├── Dockerfile.backend    # Backend container (root, uvicorn)
│   ├── Dockerfile.frontend  # Frontend container (Node 20)
│   └── kali-tools.Dockerfile# Custom Kali with security tools
├── docker-compose.yml        # Full stack composition
├── docs/                     # Product and platform documentation
├── engineering/              # Architecture, roadmap, coding standards
└── plugins/                  # Extensibility directory
```

---

## VAPT Scan Flow

1. **User selects project** and enters target (IP, hostname, or URL)
2. **Backend spawns Kali container** via Docker socket (`astraix-kali:latest`)
3. **Security tools execute** based on scan type:
   - `network` → nmap port scan + service detection
   - `web` → nikto, sqlmap, gobuster
   - `ssl` → sslscan
   - `full` → all tools
4. **Output normalized** to canonical `SecurityFinding` format
5. **Risk engine** scores findings (0-100)
6. **AI gateway** generates executive summary via Gemini
7. **Results persisted** to PostgreSQL and returned to UI

---

## Technology Stack

### Backend
| Component | Technology |
|-----------|------------|
| Framework | FastAPI 0.110 |
| Language | Python 3.12 |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 (async) |
| Cache | Redis 7 |
| Validation | Pydantic v2 |
| Migrations | Alembic |
| Container Exec | Docker socket ( Kali containers ) |

### Frontend
| Component | Technology |
|-----------|------------|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS + Radix UI |
| State | Zustand + React Query |
| Forms | React Hook Form + Zod |

### Infrastructure
| Component | Technology |
|-----------|------------|
| Containerization | Docker + Docker Compose |
| Base Image | `kalilinux/kali-rolling` → `astraix-kali:latest` |

---

## Development

### Frontend

```bash
cd frontend
npm install
npm run dev        # Development server on :3000
npm run build      # Production build
npm run type-check # TypeScript validation
```

### Backend (local)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing API

```bash
# Login (after registering an account)
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"yourpassword"}'

# Run VAPT scan
curl -X POST http://localhost:8000/api/v1/vapt/scan/quick \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"target":"scanme.nmap.org","scan_type":"network","project_id":"<project-id>"}'
```

---

## Security Tools (in astraix-kali)

| Tool | Purpose |
|------|---------|
| `nmap` | Port scanning, service detection, OS fingerprinting |
| `nikto` | Web server vulnerability scanning |
| `sqlmap` | SQL injection detection and exploitation |
| `nuclei` | Custom vulnerability templates, fast scanning |
| `gobuster` | Directory and DNS brute-forcing |
| `sslscan` | SSL/TLS cipher and certificate analysis |
| `curl` / `wget` | HTTP testing utilities |

---

## API Reference

Once running, access the interactive docs at `http://localhost:8000/docs`.

### Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/auth/login/json` | JSON login (email + password) |
| `POST` | `/api/v1/auth/login` | OAuth2 form login |
| `GET` | `/api/v1/projects` | List projects for org |
| `POST` | `/api/v1/vapt/scan/quick` | Run quick VAPT scan |
| `GET` | `/api/v1/findings` | List findings |
| `GET` | `/api/v1/scans` | List scan history |

---

## Roadmap

See [`engineering/ROADMAP.md`](engineering/ROADMAP.md) for full milestone plan.

| Milestone | Status | Description |
|-----------|--------|-------------|
| M0 — Engineering Foundation | ✅ Complete | Repo skeleton, Docker Compose, docs |
| M1 — AI-SecOS Core | 🔄 In Progress | Plugin system, orchestrator, risk engine |
| M2 — First Plugin (httpx) | 🔄 In Progress | End-to-end validation with real plugin |
| M3 — Discovery Capability | 📋 Planned | Subfinder, Katana, asset inventory |
| M4 — Web Security Assessment | 📋 Planned | Nuclei, AI summary, executive report |
| M5 — Security Analyst UI | ✅ Complete | Dashboard, findings, reports UI |
| M6+ | 📋 Planned | Cloud, K8s, SAST, AI security, compliance |

---

## Documentation

| Document | Description |
|----------|-------------|
| [`engineering/ROADMAP.md`](engineering/ROADMAP.md) | Detailed milestone plan |
| [`engineering/ARCHITECTURE.md`](engineering/ARCHITECTURE.md) | System architecture |
| [`engineering/VISION.md`](engineering/VISION.md) | Product vision and principles |
| [`docs/PRODUCT_OVERVIEW.md`](docs/PRODUCT_OVERVIEW.md) | Product positioning |
| [`docs/ARCHITECTURE_OVERVIEW.md`](docs/ARCHITECTURE_OVERVIEW.md) | Technical architecture |
| [`docs/SECOS_PLATFORM_OVERVIEW.md`](docs/SECOS_PLATFORM_OVERVIEW.md) | AI-SecOS platform guide |

---

## License

Proprietary — All rights reserved.

---

## Contact

Security Engineering Team — [GitHub Issues](https://github.com/pentestparas/ASTRAIX--AI-Autonomous-Security-Platform/issues)