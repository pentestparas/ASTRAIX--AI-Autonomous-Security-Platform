# AstraIX Security Analyst

**AI-Native Autonomous VAPT & Security Operations Platform**

AstraIX is an enterprise-grade vulnerability assessment and penetration testing (VAPT) platform that combines real security tooling, agentic AI reasoning, and a curated security knowledge base to deliver consistent, verifiable, and explainable security assessment at scale.

**Paras Patil — Founder & AI Platform Architect (Product Security Engineer)**

---

## Overview

Traditional penetration testing is manual, slow, and inconsistent. AstraIX addresses this by codifying the full assessment lifecycle — from target discovery through tool execution, finding normalization, risk scoring, and executive reporting — into an autonomous, repeatable pipeline. The platform executes actual security tooling in isolated containers (never simulations), enriches results with AI-driven context, and validates findings through re-exploitation to eliminate false positives before they reach stakeholders.

### Key Differentiators

| Capability | AstraIX |
|-----------|---------|
| Tool execution | Real tooling (nmap, nikto, sqlmap, nuclei, gobuster, sslscan, OWASP ZAP) in isolated Kali containers |
| Finding validation | Agentic re-exploitation and severity downgrade for unverifiable findings |
| Context enrichment | 360+ source cybersecurity knowledge base with TF-IDF/FAISS semantic search |
| Risk methodology | Deterministic 0–100 risk scoring engine |
| Reporting | AI-generated executive summaries and standardized report templates |
| Extensibility | Plugin architecture for adding new tools and capabilities |
| Multi-tenancy | Organizations, role-based memberships, and API-key access |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js, App Router)                │
│   Dashboard │ Scans │ Findings │ Projects │ Reports │ Graph │ ... │
└───────────────────────────────┬──────────────────────────────────┘
                                │ REST API  (nginx reverse proxy)
                     ┌──────────▼─────────────────────────┐
                     │          FastAPI Backend            │
                     │  (uvicorn + SQLAlchemy 2.0 async)    │
                     └──────┬────────────┬────────────┬─────┘
                            │            │            │
            ┌───────────────▼──┐  ┌──────▼─────┐  ┌───▼──────────────┐
            │  AI Security Core │  │ VAPT Engine │  │   Data Stores    │
            │  (capabilities,   │  │ (Docker     │  │  PostgreSQL      │
            │  plugins, risk,   │  │  socket →   │  │  Redis           │
            │  AI gateway)      │  │  Kali + ZAP │  │  Neo4j (graph)   │
            └──────────┬────────┘  └──────┬──────┘  └──────────────────┘
                       │                  │
             ┌─────────▼──────────────────▼─────────┐
             │  Knowledge Base (360+ sources)        │
             │  TF-IDF + FAISS search                │
             │  container-isolated storage           │
             └───────────────────────────────────────┘
```

---

## How It Works

### Autonomous Assessment Pipeline

| Stage | Description |
|-------|-------------|
| 1. Targeting | Analyst selects a project and defines a target (IP, hostname, or URL) |
| 2. Orchestrated Recon | Parallel three-phase reconnaissance (recon → web → deep) across spawned Kali containers and ZAP |
| 3. Normalization | Raw tool output is transformed into a canonical `SecurityFinding` model |
| 4. AI Enrichment | Researcher agent augments findings with knowledge-base context (CVEs, remediation guidance) |
| 5. Verification | Verifier agent re-exploits findings; unverifiable findings are downgraded or removed |
| 6. Risk Scoring | Findings are scored 0–100 by a deterministic risk engine |
| 7. Reporting | AI gateway generates executive summaries; report engine produces standardized deliverables |
| 8. Persistence | Results are stored in PostgreSQL and Neo4j for analysis, triage, and graph visualization |

---

## Security Posture

AstraIX is designed with operational safety and data integrity as first-class requirements:

- **Execution isolation** — All security tooling runs in short-lived, disposable Kali containers managed through the Docker socket; no tooling executes on the host
- **Knowledge base integrity** — The knowledge base is built into the container image and seeded into an isolated volume at first boot. Upstream sources are never staged on the host filesystem, and application access to knowledge is HTTP-only with path-traversal protection
- **Authentication & access control** — JWT-based authentication, organization-scoped multi-tenancy, role-based memberships, and API-key access for programmatic use
- **Responsible use** — AstraIX is intended for authorized security assessments only. Users are responsible for obtaining explicit permission to test any target system

---

## Quick Start

### Prerequisites

- Docker Desktop (macOS ARM supported)
- Git

### Deployment

```bash
# 1. Clone the repository
git clone https://github.com/pentestparas/ASTRAIX--AI-Autonomous-Security-Platform.git

# 2. Build the custom Kali tool image
docker build -f docker/kali-tools.Dockerfile -t astraix-kali:latest .

# 3. Configure environment
cp .env.example .env   # set SECRET_KEY and database credentials

# 4. Start the full stack (PostgreSQL, Redis, Neo4j, ZAP, nginx, backend, frontend)
docker-compose up -d

# 5. Verify health
curl http://localhost:8000/health
```

### Access

| Resource | URL |
|----------|-----|
| Web Application | http://localhost:3000 |
| Interactive API Documentation | http://localhost:8000/docs |

Register an account at `http://localhost:3000/register` to begin.

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VAPT_USE_DOCKER` | `true` | Enables real Docker-based VAPT execution |
| `VAPT_DEMO_MODE` | `false` | Runs with simulated results (no tool execution) |
| `KALI_IMAGE` | `astraix-kali:latest` | Container image for VAPT execution |
| `DATABASE_URL` | `postgresql+asyncpg://...` | PostgreSQL connection string |
| `SECRET_KEY` | *(required)* | JWT signing key |

> **Security note:** Secrets (e.g., `SECRET_KEY`) must only be set in the gitignored `.env` file. The tracked `.env.example` template must remain free of real secrets.

---

## Technology Stack

### Backend

| Component | Technology |
|-----------|------------|
| Framework | FastAPI 0.110 |
| Language | Python 3.12 |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 (async) |
| Graph Database | Neo4j 5 |
| Cache | Redis 7 |
| Validation | Pydantic v2 |
| Migrations | Alembic |
| Tool Execution | Docker socket → Kali containers + OWASP ZAP |
| AI | Gemini via AI gateway |

### Frontend

| Component | Technology |
|-----------|------------|
| Framework | Next.js (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS + Radix UI |
| State Management | Zustand + React Query |
| Forms | React Hook Form + Zod |

### Infrastructure

| Component | Technology |
|-----------|------------|
| Containerization | Docker + Docker Compose |
| Tooling Base Image | `kalilinux/kali-rolling` → `astraix-kali:latest` |
| Reverse Proxy | nginx |
| Web Assessment | OWASP ZAP |

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

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Engineering Roadmap](engineering/ROADMAP.md) | Milestone plan (M0–M6) |
| [System Architecture](engineering/ARCHITECTURE.md) | Technical architecture deep-dive |
| [Product Vision](engineering/VISION.md) | Vision and principles |
| [Product Overview](docs/PRODUCT_OVERVIEW.md) | Product positioning |
| [Architecture Overview](docs/ARCHITECTURE_OVERVIEW.md) | Technical architecture summary |
| [AI-SecOS Platform Guide](docs/SECOS_PLATFORM_OVERVIEW.md) | Platform capabilities walkthrough |

---

## Support

Founder & AI Platform Architect: **Paras Patil** (Product Security Engineer).

For issues, feature requests, or security concerns, please open a GitHub issue:  
[https://github.com/pentestparas/ASTRAIX--AI-Autonomous-Security-Platform/issues](https://github.com/pentestparas/ASTRAIX--AI-Autonomous-Security-Platform/issues)

---

## License

Proprietary — All rights reserved. Unauthorized use, reproduction, or distribution is prohibited.

© Paras Patil — Founder & AI Platform Architect (Product Security Engineer)