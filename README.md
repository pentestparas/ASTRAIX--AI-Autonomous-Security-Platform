# AstraIX Security Analyst

**AI-Powered Autonomous Security Assessment Platform**

A production-quality Proof of Concept for an AI Security Operating System.

---

## Overview

AstraIX Security Analyst is an autonomous security assessment platform that leverages AI to continuously assess, prioritize, and remediate security vulnerabilities across infrastructure and applications.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js 15)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │Dashboard │ │ Assessments│ │ Findings │ │  Plugin Market  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   API Gateway     │
                    │   (FastAPI)       │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼───────┐    ┌────────▼────────┐    ┌──────▼──────┐
│  Orchestrator │    │  Plugin System  │    │  Database   │
│  (Workflow)   │    │  (Extensibility)│    │  (PostgreSQL)│
└───────┬───────┘    └────────┬────────┘    └──────┬──────┘
        │                     │                     │
┌───────▼───────┐    ┌────────▼────────┐    ┌──────▼──────┐
│ Security Tools│    │   AI Engine     │    │   Cache     │
│ (Nmap, Nuclei)│    │   (LLMs)        │    │   (Redis)   │
└───────────────┘    └─────────────────┘    └─────────────┘
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Make (optional, for convenience commands)
- Python 3.12+ (for local development)
- Node.js 20+ (for local development)

### Using Docker (Recommended)

```bash
# Clone the repository
cd astraix-security-analyst

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Project Structure

```
astraix-security-analyst/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── config/         # Configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── repositories/   # Data access
│   │   ├── plugins/        # Plugin system
│   │   ├── orchestrator/   # Workflow orchestration
│   │   ├── database/       # Database setup
│   │   └── utils/          # Utilities
│   └── tests/              # Backend tests
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Next.js pages
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── styles/         # Global styles
│   └── public/             # Static assets
├── engineering/            # Documentation
│   ├── PROJECT.md
│   ├── VISION.md
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   ├── TECH_STACK.md
│   ├── CODING_STANDARDS.md
│   ├── rules/
│   └── prompts/
├── plugins/                # Plugin directory
├── docker/                 # Docker configurations
├── docker-compose.yml
├── Makefile
├── .env.example
└── .gitignore
```

## API Documentation

Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Frontend

- Dashboard: http://localhost:3000

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.12
- **Database**: PostgreSQL + SQLAlchemy 2.0 (async)
- **Cache**: Redis
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **Testing**: pytest + pytest-asyncio

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: React Query / Zustand
- **Testing**: Vitest + React Testing Library

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions (planned)
- **Monitoring**: Prometheus + Grafana (planned)

## Development

### Code Style

```bash
# Backend
make lint-backend
make format-backend

# Frontend
make lint-frontend
make format-frontend
make format-frontend
```

### Testing

```bash
# All tests
make test

# Backend only
make test-backend

# Frontend only
make test-frontend
```

## Plugin Development

See [PLUGIN_DEVELOPMENT.md](docs/PLUGIN_DEVELOPMENT.md) for creating custom security tools and AI analyzers.

## License

Proprietary - All rights reserved.

## Contact

Security Engineering Team