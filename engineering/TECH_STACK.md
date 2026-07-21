# TECH_STACK.md

## Core Technology Stack

| Category | Technology | Version | Reasoning | Responsible Team |
|----------|------------|---------|-----------|-------------------|
| **Backend** | FastAPI | ^0.110 | Async, OpenAPI native, Pydantic schema | Backend |
| **Framework** | Uvicorn | ^0.29 | High-performance ASGI server | Backend |
| **Language** | Python | 3.12 | Async ecosystem, typing | Backend |

| **Frontend** | Next.js | ^15.0 | App router, SSR | Frontend |
| **UI Toolkit** | Tailwind CSS | ^3.4 | Utility-first CSS | Frontend |
| **UI Primitives** | Radix UI | ^1.0 | Headless, accessible | Frontend |
| **Language** | TypeScript | ^5.4 | Type safety | Frontend |

| **Database** | PostgreSQL | ^16 | JSON, scalable, extendable | Backend |
| **Cache** | Redis | ^7 | Async support, JSON | Backend |

| **DevOps** | Docker | ^26 | Container runtime | Ops |
| **Orchestration** | Docker Compose | ^3.8 | Local dev, demo | Ops |

| **AI** | LangChain | ^0.1 | LLM orchestration | AI Team |
| **LLM** | Anthropic/OpenAI/Ollama | * | Model flexibility | AI Team |

---

## Backend Deep Dive

### API
- **Rest**: FastAPI REST endpoints
- **Schema**: Pydantic v2 schemas
- **Async**: `async def` everywhere
- **OpenAPI**: Auto-generated `/docs`, `/openapi.json`

Setup:
```bash
fastapi==0.110.1
uvicorn[standard]==0.29.0
pydantic==2.7.1
```

### Database
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Schema**: Pydantic + SQLAlchemy hybrid

```bash
sqlalchemy==2.0.30
asyncpg==0.29.0
alembic==1.13.1
```

### Plugins
- **Interface**: `BasePlugin` ABC
- **Discovery**: filesystem crawler (`plugin.yml`)
- **Execution**: `asyncio.subprocess`
- **Schema**: JSON Schema + Pydantic validation

```python
class BasePlugin:
    async def run(self, input: dict) -> dict:
        raise NotImplementedError

    @property
    def schema(self) -> dict:
        return json.load(open("plugin.yml"))
```

---

## Frontend Deep Dive

### Framework
- **Next.js App Router**: app/(dashboard)
- **Styling**: Tailwind CSS
- **Components**: Radix UI + cva

```bash
next==15.0.0
react==18.3.1
react-dom==18.3.1
tailwindcss==3.4.1
```

### State & Data
| Purpose | Tool |
|---------|------|
| API Client | axios |
| Data Fetching | React Query / SWR |
| State | Zustand |
| Form Validation | react-hook-form + zod |

```bash
@tanstack/react-query==5.28.0
zustand==4.5.2
axios==1.7.0
```

### Testing
- **Unit**: Vitest
- **Component**: React Testing Library
- **E2E**: Playwright

```bash
vitest==1.5.0
@testing-library/react==14.2.0
@testing-library/jest-dom==6.4.0
```

### UI
- **Color Mode**: CSS variables + context
- **Icons**: Lucide
- **Theming**: clsx + cva

```bash
lucide-react==0.378.0
```

---

## DevOps Deep Dive

### Local Dev
- **Docker Compose**: All-in-one orchestrator
- **Makefile**: Convenience commands
- **Linting**: Ruff + ESLint
- **Formatting**: Ruff format + Prettier

Commands:
```bash
make up         # all-in-one
make down       # clean
make dev        # dev servers

make lint       # lint
make format     # auto-format
```

### CI/CD
Planned:
```yaml
# .github/workflows/ci.yml

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r backend/requirements.txt
      - run: make lint-backend
      - run: make test-backend

  frontend:
    runs-on: ubuntu-latest
    needs: backend
    steps:
      - run: npm install
      - run: npm run lint
      - run: npm run test
```

### Observability
| Layer | Tool |
|-------|------|
| Runtime | Prometheus + Grafana |
| Distributed Tracing | OpenTelemetry |
| Logs | ELK (Elasticsearch, Logstash, Kibana) |

---

## AI Stack

### Short Term
- **LangChain**: LLM orchestration
- **Local Models**: Ollama (local Llama, Mistral)
- **Commercial APIs**: Anthropic OpenAI

### Long Term
- **Fine-tuning**: domain-specific findings
- **VectorDB**: embed findings patterns
- **Agents**: automate triage/reports

```python
# ai_engine.py
class FindingGenerator:
    def __init__(self, model="ollama/llama2"):
        self.model = model
    
    async def generate(self, finding: Finding) -> Finding:
        prompt = template.format(finding.title)
        return await self.model.generate(prompt)
```

---

## Plugin Stack

Each plugin:
- Has a `plugin.yml` manifest
- Runs via subprocess
- Produces JSON: `{findings: [...]}`
- Lives in `/plugins/{plugin-id}/`

Example: npm scan plugin
```yaml
# plugin.yml

name: npm-audit
id: npm-audit-scan
type: scanner
description: Run npm audit on target directory
author: AstraIX
schema:
  input:
    directory: string
  output:
    vulnerabilities: array
```

```bash
plugins/
  npm-audit/
    plugin.yml
    npm-audit.js
    Dockerfile
```

---

## Engineering Infrastructure

### Repo Structure
```
.
├── .github/          # CI/CD
├── docker/          # Compose + Dockerfiles
│   ├── app.Dockerfile
│   └── plugin.Dockerfile
├── backend/          # FastAPI
├── frontend/         # Next.js
├── engineering/      # Docs
├── plugins/          # Plugin workspace
│   ├── core/
│   │   └── plugin-sdk/
│   └── community/
└── tests/           # E2E
```

### Stack Evolution Plan

| Timeline | Stack Augmentation | Purpose |
|----------|--------------------|---------|
| PoC      | Core + Docker       | Demo |
| v0.2     | Plugin SDK          | Ecosystem |
| v0.3     | AI + ReactQuery     | Production |
| v0.5     | gRPC + WASM         | Performance |
| >v0.7    | Microservices       | Scale |

---

## Principles

### Backend
- Async by default
- Type-annotated
- Pydantic schema-validated
- Alembic migrations
- `.env` separation

### Frontend
- TypeScript by default
- Tailwind for styling
- Radix UI for primitives
- Server components > client
- Query keys = URLs

### DevOps
- Everything runs in containers
- Production parity in development
- Health checks & `livenessProbe`
- Ephemeral storage

### AI
- Model-agnostic: OpenAI ↔ Anthropic ↔ Ollama
- Augment, don't replace
- Fallback to deterministic
- Embeddings for patterns

---

## Why This Stack?

| Decision | Reason |
|----------|--------|
| FastAPI + Next.js | Lean, async, single language (Python + JS), ecosystem |
| Async-first | Scale to 1000+ scans |
| Tailwind CSS | Consistency, developer experience |
| Radix UI | Accessibility baked-in |
| Postgres + Redis | Balance scale + flexibility |
| Subprocess plugins | Isolation, portability |

---

## Hiring & Onboarding

| Role | Stack Familiarity Required | Nice-to-Have |
|------|----------------------------|--------------|
| Backend Engineer | Python 3.12+, FastAPI, asyncio | SQLAlchemy, Alembic |
| Frontend Engineer | TypeScript, Next.js 15, TailwindCSS | ReactQuery, Zustand |
| DevSecOps | Docker, CI/CD | Kubernetes |
| Security Engineer | Plugin interfaces | Security tools |

Onboarding: run `make up`, follow **CONTRIBUTING.md**