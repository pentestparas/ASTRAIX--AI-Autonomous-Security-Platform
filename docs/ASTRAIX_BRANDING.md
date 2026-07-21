# ASTRAIX - AI-Native Security Engineering Platform

> **"The Weapon for All 9 Domains of Cybersecurity"**

---

## Platform Name

### ASTRAIX
**Pronunciation**: "AS-tra-ix"

**Etymology**:
- **ASTRA** (Sanskrit): "Weapon" or "Instrument of defense and attack"
- **IX** (Roman numeral): "Nine" - The 9 Core Domains of Cybersecurity

```
ASTRA + IX = The Weapon for All 9 Domains
```

---

## Core Philosophy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ASTRAIX = AI-Native Security Platform                                    │
│                                                                             │
│   Traditional:  Tools + AI = "AI-Powered"                                  │
│   ASTRAIX:     AI Core + All 9 Domains = "AI-Native"                     │
│                                                                             │
│   AI is NOT what ASTRAIX DOES.                                             │
│   AI is HOW ASTRAIX WORKS.                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## The 9 Domains (ASTRAIX Coverage)

| Domain | Name | Key Capabilities |
|--------|------|------------------|
| **IX-1** | Offensive Security | VAPT, Red Team, Bug Bounty |
| **IX-2** | Defensive Security | SIEM, SOAR, EDR/NDR |
| **IX-3** | Cloud Security | CSPM, CWPP, CASB |
| **IX-4** | Application Security | SAST, DAST, SCA |
| **IX-5** | Identity Security | IAM, PAM, Zero Trust |
| **IX-6** | Data Security | DLP, Encryption |
| **IX-7** | Threat Intelligence | OSINT, Feeds, Hunting |
| **IX-8** | Security Operations | SOC, Forensics, IR |
| **IX-9** | GRC & Compliance | Risk, Policy, Audit |

---

## AI Modules in ASTRAIX

| Module | Purpose |
|--------|---------|
| **NeuralSec Engine** | Core ML engine for threat detection, anomaly detection |
| **SecAgent Framework** | Multi-agent AI for autonomous security operations |
| **ThreatGPT Advisor** | Natural language security queries and reporting |

---

## Integrated VAPT Platforms

ASTRAIX integrates with leading AI-VAPT tools:

| Platform | Stars | Unique Feature | Integration |
|---------|-------|----------------|-------------|
| **PentAGI** | 20.8k | Multi-agent security AGI | ✅ Native |
| **RedAmon** | 2.2k | Pentest → Fix → PR | ✅ Native |
| **Xalgorix** | 770 | Exploit verification | ✅ Native |
| **Dark-Moon** | 739 | Privacy AI pentest | ✅ Native |
| **Lyrie AI** | 371 | Agent Trust Protocol | ✅ Native |

---

## Current Implementation (Phase 1)

### Completed Features
- [x] Docker-based full stack deployment
- [x] Login/Registration with organization management
- [x] Project creation and management
- [x] Assessment/scan creation with multi-select scan types
- [x] Project 3-dot menu (View/Delete)
- [x] Scan persistence in database (Assets + Assessments)
- [x] VAPT tool integration framework (Kali Linux tools)
- [x] Output parsers for 15+ security tools

### Scanner Module
```
backend/app/scanner/
├── __init__.py              # Exports
├── models.py                # ScanRequest, ScanResult, Finding
├── tools.py                 # 50+ Kali tool definitions
├── vapt_platforms.py        # Multi-platform executor
├── executor.py              # ScannerExecutor service
└── parsers/                  # Tool output parsers
```

---

## Roadmap

### Phase 1: Foundation (Current - Q3 2026)
- [x] VAPT Engine with AI-first approach
- [x] Project/Organization management
- [x] Assessment workflow
- [x] Findings management
- [ ] Assessment persistence in DB
- [ ] Dashboard with AI-generated stats
- [ ] Report generation

### Phase 2: Core Platform (Q4 2026)
- [ ] SIEM Lite with NeuralSec anomaly detection
- [ ] SOAR Lite with SecAgent playbooks
- [ ] SAST/DAST integration
- [ ] CSPM (Cloud Security Posture)

### Phase 3: Full Platform (Q1 2027)
- [ ] Full SIEM with ML detection
- [ ] SOAR with integrations
- [ ] EDR/XDR capabilities
- [ ] Threat hunting platform

### Phase 4: All 9 Domains (Q2-Q3 2027)
- [ ] Identity Security
- [ ] Data Security
- [ ] Network Security
- [ ] Email Security
- [ ] Mobile Security

### Phase 5: AI-Native (Q4 2027)
- [ ] Autonomous security operations
- [ ] Predictive threat modeling
- [ ] Natural language queries
- [ ] Self-healing security

---

## Branding Elements

### Taglines
1. "ASTRAIX: The Weapon for All 9 Domains of Cybersecurity"
2. "9 Domains. 1 Platform. AI-Native."
3. "From Attack to Defense - ASTRAIX Covers All 9"

### Colors
- **Deep Navy**: #0A1628 (Background)
- **Cyber Green**: #00FF88 (AI, Active)
- **Pure White**: #FFFFFF (Text)

### Logo Concept
- Shield icon representing protection
- 9 segments/points for 9 domains
- Neural network pattern (AI-first)
- Green glow effect

---

## Documentation

| Document | Description |
|----------|-------------|
| `docs/ASTRAIX_BRANDING.md` | This document - brand identity |
| `docs/ARCHITECTURE_OVERVIEW.md` | Detailed 9-domain architecture |
| `docs/SECOS_PLATFORM_OVERVIEW.md` | Complete platform overview |
| `graphify-out/wiki/Pending_Patches_&_Issues.md` | Development tracking |

---

*ASTRAIX - The Weapon for All 9 Domains of Cybersecurity*
*AI-Native Security Engineering Platform*
*Version 1.0 | 2026-07-17*