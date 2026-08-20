# AstraIX — Product Capabilities, Tools & Resources

> Compiled for executive (VP) review. List of security tools integrated into
> the AstraIX autonomous VAPT platform, the AI models and providers used, and
> the knowledge resources the platform operates on.

## 1. Security Tooling (Integrated & Executed)

All tools run in real, disposable **Kali Linux containers** (spawned on demand
via the Docker socket) against the authorized target. 40 tools in the
registry; 35 shipped/available in the current build.

### Reconnaissance & Discovery
| Tool | Purpose |
|------|---------|
| Nmap | Network host/port/service discovery |
| Masscan | High-speed internet-wide port scanning |
| DNSRecon | DNS enumeration (records, zone transfer checks) |
| Subfinder | Passive subdomain enumeration |
| HTTPx | HTTP service probing / web fingerprinting |
| WhatWeb | Web technology fingerprinting |
| Katana | Crawler for endpoint/route discovery |
| Feroxbuster | Content brute-forcing / directory discovery |
| Gobuster | Directory/DNS/vhost brute-forcing |
| Dirsearch | Web path discovery |
| API Surface (custom) | API endpoint discovery from JS bundles |
| WAFW00F | WAF detection fingerprint |
| Forms (custom) | Web form discovery & parameter mapping |
| DOM-XSS (custom) | DOM-based XSS probe |

### Vulnerability Scanning & Exploitation
| Tool | Purpose |
|------|---------|
| Nikto | Web server vulnerability scanner |
| Nuclei | Template-driven vulnerability scanner (YAML templates) |
| Trivy | Container/image & filesystem vulnerability scanner |
| SQLMap | Automated SQL injection detection/exploitation |
| Commix | Command injection detection/exploitation |
| Dalfox | XSS scanner |
| XSStrike | Advanced XSS detection |
| Hydra | Online password brute-forcing (services/login) |
| Metasploit | Exploit framework (manual/agent driven) |
| SearchSploit | Exploit-DB lookup |
| ZAP (OWASP) | Intercepting proxy & web scanner (dedicated container) |
| GraphQLMap | GraphQL endpoint testing |
| Smuggler | HTTP request smuggling detection |
| Kiterunner | API/content route discovery |
| WFuzz | Web fuzzer (parameters/directories) |
| Arjun | HTTP parameter discovery |
| Ffuf | Fast web fuzzer |

### Code / Cloud / LLM-Security
| Tool | Purpose |
|------|---------|
| Garak | LLM vulnerability scanner (prompt injection, data leakage) |
| PromptFoo | LLM red-teaming / prompt-evaluation harness |
| Gitleaks | Secrets/credential scanning in repos |
| TruffleHog | Secrets scanning (depth-first) |
| Semgrep | Static analysis / custom rules |
| Bandit | Python security static analysis |
| Code Review (custom) | AI-assisted source review |
| Flows (custom) | Auth/state-flow analysis |

### TLS / Crypto
| Tool | Purpose |
|------|---------|
| SSLScan | TLS/SSL cipher & certificate inspection |
| TestSSL | TLS/SSL server configuration audit |

## 2. AI Layer

The agent pipeline is LLM-driven (planning, tool selection, test-matrix
generation, finding verification, executive summary). Providers are used in
priority order with automatic failover:

| Provider | Models | Role |
|----------|--------|------|
| NVIDIA NIM (API) | `deepseek-ai/deepseek-v4-flash-0731` (matrix model / fallback), `minimaxai/minimax-m3` (primary) | Test-matrix generation, agent reasoning, verification |
| Ollama (local) | `huihui_ai/qwen3-abliterated:14b-v2` | Local fallback for planning/agent turns |

AI capabilities in the pipeline:
- **AI Planner** — builds the engagement plan (recon → web → deep phases)
- **Agent Loop** — autonomous tool selection and execution (up to 40 steps)
- **Test Matrix Agent** — LLM-generated exploitation probes with real payloads
- **Verifier Agent** — re-exploits to confirm/downgrade findings (eliminates FPs)
- **Researcher Agent** — knowledge-base enrichment (CVEs, remediation, context)
- **Executive Summary / Risk scoring** — risk level + severity breakdown + remediation
- **AI Transparency** — live "AI Reasoning" console (LLM calls, verdicts, matrix)

## 3. Knowledge Base (Resources)

360+ curated cybersecurity sources with TF-IDF + semantic embeddings (FAISS),
served over an HTTP search API consumed by the planner/researcher/verifier.

### Upstream repos (baked into the image from `docker/kb-repos.txt`)
- AI/LLM security: AI-agents-for-cybersecurity, awesome-ai-cybersecurity,
  awesome-ai-security, owasp-llm-top10-project (OWASP LLM Top 10),
  microsoft-mcp-for-beginners, microsoft-ai-red-teaming-labs,
  ai-red-teaming-guide, anmolksachan-AI-ML-Free-Resources,
  awesome-MLSecOps, agent-opfor, emilia-protocol
- Payload libraries: PayloadsAllTheThings, sql/xss/xxe/command/crlf/csv/
  directory/open-redirect/server-side-template-injection/ssti/waf-bypass/
  web-cache-poisoning/http-request-smuggling payload lists,
  business-logic-exploitation-playbook
- Curricula/cheat sheets: OWASP CheatSheetSeries, Web-Security-Academy-Series,
  Dojo-101, paulveillard-cybersecurity, Cybersecurity-Resources,
  Cyber_and_Information_Security_Knowledge_Base, Cyber_Security_Reference,
  cybersecurity-knowledge-base-kayShahbaaz, awesome-soc-cyb3rxp,
  awesome-cyber-security, Berkanktk-CyberSecurity, CAI-aliasrobotics
- Web docs: OWASP GenAI / LLM Top-10 pages, Medium AI-repos roundup, MCP
  server security (semgrep)

### Infrastructure
| Component | Purpose |
|-----------|---------|
| Kali Linux (custom image) | Tool execution runtime (all shell tools) |
| OWASP ZAP container | Proxy/web scanner service |
| PostgreSQL | Findings, assessments, org/project/asset persistence |
| Redis | Scan progress bus (live event streaming) |
| Neo4j | Cybersecurity knowledge graph / attack-surface graphing |
| FastAPI (Python 3.12) | Backend API |
| Next.js 14 (TypeScript) | Frontend console |