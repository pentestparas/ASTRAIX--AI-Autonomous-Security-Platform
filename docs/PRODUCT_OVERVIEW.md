# ASTRAIX - Product Overview & Technical Architecture

> **"The Weapon for All 9 Domains of Cybersecurity"**

---

## Executive Summary

**ASTRAIX** (Astra + IX) is an **AI-Native Security Engineering Platform** designed for comprehensive vulnerability assessment and penetration testing (VAPT). The name derives from:
- **ASTRA** (Sanskrit): Weapon/Instrument of defense and attack
- **IX** (Roman numeral): Nine - representing the 9 core cybersecurity domains

**Current Status**: ✅ VAPT Module Operational, Demo Mode Active

---

## Product Vision

### Core Philosophy
```
Traditional Security:  Tools + AI = "AI-Powered"
ASTRAIX:               AI Core + 9 Domains = "AI-Native"

AI is NOT what ASTRAIX DOES.  AI is HOW ASTRAIX WORKS.
```

### Target Market
- Enterprise security teams
- Managed Security Service Providers (MSSPs)
- Penetration testing firms
- DevSecOps organizations

---

## Architecture Overview

### Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14.1.0, React, TypeScript |
| **Backend** | FastAPI (Python 3.12), SQLAlchemy 2.0 |
| **Database** | PostgreSQL 16 (Async) |
| **Cache** | Redis 7 |
| **Container** | Docker, Docker Compose |
| **AI** | OpenAI, Anthropic, Ollama (configurable) |

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           ASTRAIX PLATFORM                           │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                    FRONTEND (Next.js)                      │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │    │
│  │  │Dashboard │  │ Projects │  │  VAPT    │  │Findings  │   │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │    │
│  └──────────────────────────────────────────────────────────┘    │
│                              │                                     │
│                              ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                    API GATEWAY (FastAPI)                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │    │
│  │  │  Auth    │  │ Projects │  │  VAPT    │  │Findings  │   │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │    │
│  └──────────────────────────────────────────────────────────┘    │
│                              │                                     │
│              ┌───────────────┼───────────────┐                   │
│              ▼               ▼               ▼                     │
│  ┌────────────────┐ ┌────────────┐ ┌────────────────┐           │
│  │   PostgreSQL    │ │    Redis   │ │   NeuralSec AI  │           │
│  │   (Storage)     │ │   (Cache)  │ │   (Orchestrator)│           │
│  └────────────────┘ └────────────┘ └────────────────┘           │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                    VAPT EXECUTION ENGINE                  │    │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │    │
│  │  │  nmap  │  │ nikto  │  │ sqlmap │  │ nuclei │  ...  │    │
│  │  └────────┘  └────────┘  └────────┘  └────────┘        │    │
│  │  (Docker Container Isolation for tool execution)         │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Features & Capabilities

### Current Implementation (Phase 1 - VAPT)

| Feature | Status | Description |
|---------|--------|-------------|
| **User Authentication** | ✅ | JWT-based login/register with organization management |
| **Project Management** | ✅ | Create, view, delete projects within organizations |
| **VAPT Scanning** | ✅ | AI-orchestrated vulnerability scanning |
| **Findings Tracking** | ✅ | Severity-based findings with remediation |
| **Scan Persistence** | ✅ | All scans saved to database with findings |
| **Demo Mode** | ✅ | Realistic sample findings for testing |

### VAPT Tools Integrated

| Tool | Category | Status |
|------|----------|--------|
| **nmap** | Network scanning | ✅ Demo |
| **nikto** | Web server scanning | ✅ Demo |
| **sqlmap** | SQL injection | ✅ Demo |
| **nuclei** | Vulnerability templates | ✅ Demo |
| **gobuster** | Directory enumeration | ✅ Demo |
| **sslscan** | SSL/TLS analysis | ✅ Demo |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/vapt/scan` | POST | Run VAPT scan with target |
| `/api/v1/vapt/tools` | GET | List available tools |
| `/api/v1/vapt/tools/health` | GET | Tool health status |
| `/api/v1/assessments` | GET | List assessments |
| `/api/v1/findings` | GET | List findings |
| `/api/v1/projects` | GET/POST | Manage projects |

---

## Security Domains (9 Core Areas)

| Domain | Coverage | Status |
|--------|---------|--------|
| 1. **Offensive Security** (VAPT) | ✅ | Implemented |
| 2. **Defensive Security** | 🔜 | Roadmap |
| 3. **Cloud Security** | 🔜 | Roadmap |
| 4. **Application Security** | 🔜 | Roadmap |
| 5. **Identity Security** | 🔜 | Roadmap |
| 6. **Data Security** | 🔜 | Roadmap |
| 7. **Threat Intelligence** | 🔜 | Roadmap |
| 8. **Security Operations** | 🔜 | Roadmap |
| 9. **GRC & Compliance** | 🔜 | Roadmap |

---

## Database Schema

### Core Tables

```
organizations
├── id (UUID)
├── name
├── created_at, updated_at
├── users (relationship)
└── projects (relationship)

projects
├── id (UUID)
├── organization_id (FK)
├── name, description
├── created_at, updated_at
└── assessments (relationship)

assets
├── id (UUID)
├── organization_id (FK)
├── project_id (FK)
├── name, type, identifier
├── metadata_json
└── assessments (relationship)

assessments
├── id (UUID)
├── organization_id (FK)
├── project_id (FK)
├── asset_id (FK)
├── status (pending/running/completed/failed)
├── type (vapt, etc.)
├── findings_count
├── started_at, completed_at
└── findings (relationship)

findings
├── id (UUID)
├── organization_id (FK)
├── project_id (FK)
├── asset_id (FK)
├── assessment_id (FK)
├── severity (critical/high/medium/low/info)
├── title, description
├── cvss_score
├── remediation
├── fingerprint (unique)
├── status (open/resolved/false_positive)
└── created_at, updated_at
```

---

## Deployment Architecture

### Docker Containers

| Container | Image | Port | Purpose |
|-----------|-------|------|---------|
| **frontend** | Custom (Next.js) | 3000 | Web UI |
| **backend** | Custom (FastAPI) | 8000 | API Server |
| **postgres** | postgres:16-alpine | 5432 | Database |
| **redis** | redis:7-alpine | 6379 | Cache |

### Quick Start
```bash
cd astraix-security-analyst
docker compose up -d
```

Access:
- **UI**: http://localhost:3000
- **API**: http://localhost:8000/api/v1
- **Docs**: http://localhost:8000/docs

**Demo Credentials**: `demo@astraix.com` / `demo123456`

---

## Roadmap

### Phase 1: Foundation (COMPLETED - Q3 2026)
- [x] User authentication & organization management
- [x] Project management
- [x] VAPT scanning with AI orchestration
- [x] Findings tracking
- [x] Demo mode for testing

### Phase 2: VAPT Enhancement (Q4 2026)
- [ ] Real tool execution (Kali Linux containers)
- [ ] Dark-Moon integration
- [ ] PentAGI integration
- [ ] Advanced reporting

### Phase 3-5: Full Platform (Q1-Q4 2027)
- [ ] SIEM/SOAR capabilities
- [ ] Cloud security modules
- [ ] All 9 domains implementation
- [ ] Full AI-native autonomous operations

---

## Integration Ecosystem

### External VAPT Platforms

| Platform | GitHub | Stars | Integration |
|----------|--------|-------|-------------|
| **PentAGI** | vxcontrol/pentagi | 20.8k | Ready |
| **Dark-Moon** | ASCIT31/Dark-Moon | 739 | Ready |
| **RedAmon** | samugit83/redamon | 2.2k | Ready |
| **Xalgorix** | xalgord/xalgorix | 770 | Ready |
| **Lyrie AI** | OTT-Cybersecurity-LLC/lyrie-ai | 371 | Ready |

---

## Key Differentiators

1. **AI-First Architecture**: AI is not an add-on but the core operating principle
2. **9 Domain Coverage**: Complete cybersecurity coverage, not just point solutions
3. **Modern Tech Stack**: Next.js 14, FastAPI, PostgreSQL, Redis
4. **Docker-Based**: Easy deployment and scaling
5. **Extensible**: Plugin system for custom tools and integrations

---

## Technical Debt & Notes

### Known Issues
1. Tools are running in **demo mode** (not real execution)
2. CORS may need adjustment for production domains

### To Enable Real Tool Execution
1. Set `VAPT_DEMO_MODE=false` in docker-compose.yml
2. Set `VAPT_USE_DOCKER=true` to use Kali containers
3. Install Kali Linux Docker image: `docker pull kalilinux/kali-rolling:latest`

---

## Support & Documentation

| Resource | Location |
|----------|----------|
| **API Docs** | http://localhost:8000/docs |
| **Architecture** | docs/ARCHITECTURE_OVERVIEW.md |
| **Branding** | docs/ASTRAIX_BRANDING.md |
| **This Document** | docs/PRODUCT_OVERVIEW.md |

---

*ASTRAIX - The Weapon for All 9 Domains of Cybersecurity*
*Version 1.0 | July 2026*