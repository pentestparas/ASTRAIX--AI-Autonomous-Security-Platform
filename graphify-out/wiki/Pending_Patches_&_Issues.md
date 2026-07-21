# Pending Patches & Issues

## Overview
This document tracks all known issues, pending patches, and future enhancement ideas for the AstraIX Security Analyst platform.

---

## Recently Patched Issues

### 1. Project 3-Dot Menu (RESOLVED)
- **Issue**: Project cards had a 3-dot menu button with no functionality
- **File**: `frontend/src/app/(main)/projects/page.tsx`
- **Fix**: Added DropdownMenu with View Project and Delete Project options
- **Status**: RESOLVED

### 2. Scan Details Not Persisting After Refresh (RESOLVED)
- **Issue**: Scans were stored in local state only and disappeared on page refresh
- **File**: `backend/app/api/v1/__init__.py`
- **Fix**: Updated `/assess` endpoint to actually persist Asset and Assessment records to database
- **Status**: RESOLVED

### 3. Project Detail Page Not Showing Scans (RESOLVED)
- **Issue**: Project detail page at `/projects/[id]` couldn't fetch scans for the project
- **File**: `backend/app/api/v1/assessments.py`
- **Fix**: Added `project_id` and `organization_id` query parameters to `list_assessments` endpoint
- **Status**: RESOLVED

### 4. Project Delete API Missing organization_id (RESOLVED)
- **Issue**: `projectsApi.delete()` in frontend only passed `id`, missing `organization_id`
- **File**: `frontend/src/services/api.ts`
- **Fix**: Updated to pass both `organization_id` and `id`
- **Status**: RESOLVED

### 5. UUID Type Mismatch in /assess Endpoint (RESOLVED)
- **Issue**: `/assess` endpoint was passing string UUIDs directly to SQLAlchemy models
- **File**: `backend/app/api/v1/__init__.py`
- **Fix**: Added proper UUID conversion using `UUIDType(org_id_str)` before creating models
- **Status**: RESOLVED

### 6. Scans Page Response Handling (RESOLVED)
- **Issue**: Scans page expected `{success, data}` wrapper but `/assess` returned raw response
- **File**: `frontend/src/app/(main)/scans/page.tsx`
- **Fix**: Updated to handle both wrapped and unwrapped responses
- **Status**: RESOLVED

---

## VAPT Platform Integration (Enterprise-Grade Scanner)

### Integrated Platforms

#### 1. Kali Linux (Direct Tool Execution)
- **Status**: ✅ Implemented in `app/scanner/`
- **Tools**: 50+ security tools (nmap, masscan, nikto, sqlmap, nuclei, gobuster, ffuf, trivy, semgrep, etc.)
- **Execution**: Docker container isolation
- **Parsers**: XML, JSON, text output parsing for all major tools

#### 2. Dark-Moon (AI-Powered Autonomous Pentesting)
- **URL**: https://github.com/ASCIT31/Dark-Moon (739 stars)
- **Status**: 🔄 Integration Ready
- **Features**:
  - AI agent orchestration (web, cloud, AD, Kubernetes)
  - MCP security gateway
  - Privacy gateway with reversible tokenization
  - 50+ integrated tools
  - CI/CD integration
- **Integration**: `create_dark_moon_executor()` in `app/scanner/vapt_platforms.py`

#### 3. PentAGI (Multi-Agent Security AGI)
- **URL**: https://github.com/vxcontrol/pentagi (20.8k stars)
- **Status**: 🔄 Integration Ready
- **Features**:
  - Multi-agent system (researcher, developer, executor)
  - Knowledge graph (Graphiti + Neo4j)
  - Memory system (long-term, working, episodic)
  - 20+ professional security tools
  - Langfuse + Grafana observability
- **Integration**: `create_pentagi_executor()` in `app/scanner/vapt_platforms.py`

#### 4. Lyrie AI (Autonomous Security Agent)
- **URL**: https://github.com/OTT-Cybersecurity-LLC/lyrie-ai (371 stars)
- **Status**: 🔄 Integration Ready
- **Features**:
  - 7-phase autonomous pentesting (recon → exploit → report)
  - Agent Trust Protocol (ATP) - cryptographic agent identity
  - AI red-teaming for LLM endpoints
  - SMT-based exploit feasibility analysis
  - CVSS v3.1 scoring
  - 1,737+ tests
- **Installation**: `pip install lyrie-omega`
- **Commands**: `lyrie hack <target>`, `lyrie scan <url>`, `lyrie redteam <endpoint>`

### Scanner Module Architecture

```
backend/app/scanner/
├── __init__.py           # Module exports
├── models.py             # ScanRequest, ScanResult, Finding, Severity
├── tools.py              # ToolRegistry with 50+ Kali tools
├── vapt_platforms.py      # VAPTExecutor, platform integrations
├── vapt_platforms_integration.py  # Documentation & integration guide
├── parsers.py             # Output parsers for all tools
└── executor.py            # ScannerExecutor service
```

### Execution Flow

```
POST /assess
    ↓
create ScanRequest (target, tools, capability)
    ↓
ScannerExecutor.run_scan()
    ↓
┌─────────────────────────────────────┐
│  VAPT Platform Selection           │
│                                     │
│  VAPT_PLATFORM=kali      → Kali Executor
│  VAPT_PLATFORM=dark-moon → Dark-Moon
│  VAPT_PLATFORM=pentagi   → PentAGI
│  VAPT_PLATFORM=lyrie     → Lyrie AI
└─────────────────────────────────────┘
    ↓
Execute Tools (parallel/sequential)
    ↓
Parse Output (nmap, nikto, nuclei, sqlmap, etc.)
    ↓
Deduplicate Findings
    ↓
Persist to Database
    ↓
Return ScanResult with findings
```

---

## Pending Issues & Future Enhancements

### HIGH PRIORITY

#### 1. Lyrie AI Integration
- **Issue**: Lyrie AI is not yet integrated as a VAPT platform option
- **File**: `backend/app/scanner/vapt_platforms.py`
- **Required Changes**:
  - [ ] Add `create_lyrie_executor()` function
  - [ ] Implement Lyrie CLI subprocess execution
  - [ ] Parse Lyrie JSON output to findings
  - [ ] Add Lyrie ATP agent identity verification
- **Status**: PENDING

#### 2. Scans Page Doesn't Load Existing Scans on Mount
- **Issue**: When navigating to `/scans`, existing scans from database are not loaded
- **File**: `frontend/src/app/(main)/scans/page.tsx`
- **Required Changes**:
  - [ ] On mount, fetch assessments from API
  - [ ] Merge with local state
- **Status**: PENDING

#### 3. Dashboard Stats Endpoint Returns Hardcoded Values
- **Issue**: `/dashboard/stats` returns fake static data
- **File**: `backend/app/api/v1/__init__.py`
- **Required Changes**:
  - [ ] Query actual counts from database
  - [ ] Return real-time statistics
- **Status**: PENDING

#### 4. Real Tool Execution in Orchestrator
- **Issue**: Orchestrator uses `_use_vapt_executor` but tools may not be installed
- **File**: `backend/app/orchestrator/service.py`
- **Required Changes**:
  - [ ] Check tool availability before execution
  - [ ] Fall back to plugin system if tools unavailable
  - [ ] Show clear error messages
- **Status**: PENDING

---

### MEDIUM PRIORITY

#### 5. Asset Management UI
- **Issue**: Cannot create/view assets, only auto-created during scans
- **Required Changes**:
  - [ ] Create asset creation dialog
  - [ ] Add asset listing/management UI
  - [ ] Link scans to existing assets
- **Status**: PENDING

#### 6. Findings Not Being Created
- **Issue**: Scans return 0 findings because output parsing may fail
- **Required Changes**:
  - [ ] Verify all parsers work correctly
  - [ ] Add fallback text parsing
  - [ ] Test with real tool output
- **Status**: PENDING

#### 7. Signout Token Invalidation
- **Issue**: Frontend clears localStorage but doesn't invalidate JWT
- **Required Changes**:
  - [ ] Implement token blacklist
  - [ ] Add `/auth/logout` endpoint
- **Status**: PENDING

#### 8. API Key Management UI
- **Issue**: Cannot create/view/revoke API keys from UI
- **Required Changes**:
  - [ ] Create API key management page
  - [ ] Show key only once on creation
  - [ ] Allow revoking keys
- **Status**: PENDING

---

### LOW PRIORITY (NICE TO HAVE)

#### 9. Membership/Team Management UI
- **Issue**: Cannot invite users or manage roles
- **Status**: PENDING

#### 10. Audit Logs UI
- **Issue**: AuditLog model exists but no UI
- **Status**: PENDING

#### 11. Webhook/Notification System
- **Issue**: No notifications when scans complete
- **Status**: PENDING

---

## VAPT Platform Integration Roadmap

### Phase 1: Core Scanner (COMPLETED)
- [x] Scanner module architecture
- [x] Tool registry (50+ Kali tools)
- [x] Output parsers (nmap, nikto, nuclei, sqlmap, etc.)
- [x] Docker container execution
- [x] Orchestrator integration

### Phase 2: Platform Integration (IN PROGRESS)
- [x] Kali Linux executor
- [x] Dark-Moon integration ready
- [x] PentAGI integration ready
- [ ] Lyrie AI integration
- [ ] Platform-agnostic scan interface

### Phase 3: AI Orchestration (PLANNED)
- [ ] Multi-agent orchestration
- [ ] Knowledge graph integration
- [ ] AI-powered finding prioritization
- [ ] Natural language report generation
- [ ] False positive reduction with ML

### Phase 4: Enterprise Features (PLANNED)
- [ ] ATP (Agent Trust Protocol) for multi-agent identity
- [ ] Distributed scanning (worker nodes)
- [ ] Compliance reporting (NIST, ISO 27001)
- [ ] Custom tool support
- [ ] CI/CD integrations

---

## Technical Debt

### Frontend
- `scans/page.tsx` - 406 lines, should be broken into smaller components
- `projects/page.tsx` - 244 lines, should split into project card component
- No loading skeletons for some pages
- No error boundaries

### Backend
- No input validation layer (use Pydantic schemas consistently)
- No rate limiting
- No request ID tracking
- Logging could be more structured
- Scanner needs health check endpoint

---

## API Endpoint Issues

| Endpoint | Issue | Status |
|----------|-------|--------|
| `POST /assess` | Returns raw object | FIXED |
| `GET /assessments` | Doesn't filter by project_id properly | FIXED |
| `DELETE /projects/{id}` | Requires organization_id but not validated | FIXED |
| `GET /dashboard/stats` | Returns hardcoded fake data | PENDING |

---

## Database Schema Notes

- All UUID primary keys use `uuid4()` generation
- Cascading deletes are set up for most relationships
- AuditLog table exists but not populated
- API keys use SHA-256 hashing
- User passwords use bcrypt (4.0.1)
- Findings table ready for scan results

---

## Environment & Deployment

- Docker stack: frontend (3000), backend (8000), postgres (5432), redis (6379)
- Working credentials: `demo@astraix.com` / `demo123456`
- Next.js 14.1.0 (downgraded from 15.0.0)
- bcrypt 4.0.1 (pinned for compatibility)

### Environment Variables for VAPT

```bash
# VAPT Platform Selection
VAPT_PLATFORM=kali  # Options: kali, dark-moon, pentagi, lyrie

# Dark-Moon (if using)
DARK_MOON_URL=http://localhost:8080
DARK_MOON_API_KEY=your_api_key

# PentAGI (if using)
PENTAGI_URL=http://localhost:8443
PENTAGI_API_KEY=your_api_key

# Lyrie AI (if using)
LYRIE_PATH=/usr/local/bin/lyrie  # Path to lyrie executable
```

---

Last Updated: 2026-07-17