"""
External VAPT Platform Integration Hub

Integrates with leading AI-powered security platforms for enhanced capabilities.
Each platform brings unique strengths to the AstraIX security ecosystem.

Platform Support:
-----------------

1. KALI LINUX (Direct Tool Execution)
   - 50+ security tools (nmap, nikto, sqlmap, nuclei, etc.)
   - Docker container isolation for safe execution
   - Best for: Direct vulnerability scanning, container security

2. DARK-MOON (AI-Powered Autonomous Pentesting)
   - URL: https://github.com/ASCIT31/Dark-Moon (739 stars)
   - AI agents for web, cloud, AD, Kubernetes security
   - MCP (Model Context Protocol) security gateway
   - Privacy gateway with reversible tokenization
   - Best for: Full-scope autonomous penetration testing

3. PENTAGI (Multi-Agent Security AGI)
   - URL: https://github.com/vxcontrol/pentagi (20.8k stars)
   - Multi-agent system with specialized roles
   - Knowledge graph integration (Graphiti + Neo4j)
   - 20+ professional security tools
   - Best for: Complex multi-target security assessments

4. LYRIE AI (Autonomous Security Agent)
   - URL: https://github.com/OTT-Cybersecurity-LLC/lyrie-ai (371 stars)
   - 7-phase autonomous pentesting (recon → exploit → report)
   - Agent Trust Protocol (ATP) for AI agent identity
   - AI red-teaming for LLM endpoints
   - SMT-based exploit feasibility analysis
   - Best for: AI security research, LLM red-teaming, agent identity

Integration Architecture:
--------------------------

┌─────────────────────────────────────────────────────────────────┐
│                    AstraIX Security Platform                      │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Frontend  │  │   Backend   │  │    AI/ML    │             │
│  │   (Next.js) │  │   (FastAPI) │  │  Orchestrator│             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          │                                      │
│                   ┌──────▼──────┐                               │
│                   │  VAPT Hub   │                               │
│                   │  (Unified   │                               │
│                   │  Interface) │                               │
│                   └──────┬──────┘                               │
│                          │                                      │
│    ┌──────────┬──────────┼──────────┬──────────┐               │
│    │          │          │          │          │               │
│    ▼          ▼          ▼          ▼          ▼               │
│ ┌──────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────┐             │
│ │ Kali │ │  Dark  │ │ PentAGI│ │  Lyrie │ │Custom │             │
│ │Linux │ │-Moon   │ │        │ │   AI   │ │ Tools │             │
│ └──────┘ └────────┘ └────────┘ └────────┘ └──────┘             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

Usage Examples:
---------------

1. Kali Linux (Direct):
   >>> from app.scanner.vapt_platforms import create_kali_executor
   >>> executor = create_kali_executor()
   >>> result = await executor.execute_tool(KALI_TOOLS["nmap"], "192.168.1.1")

2. Dark-Moon (AI-Powered):
   >>> executor = create_dark_moon_executor("http://localhost:8080", api_key)
   >>> # Uses MCP interface for secure tool execution

3. PentAGI (Multi-Agent):
   >>> executor = create_pentagi_executor("http://localhost:8443", api_key)
   >>> # Multi-agent orchestration with knowledge graph

4. Lyrie (Autonomous Agent):
   >>> # Install: pip install lyrie-omega
   >>> # Commands: lyrie hack <target>, lyrie scan <url>, lyrie redteam <endpoint>
   >>> # ATP integration for agent identity verification

Key Features by Platform:
-------------------------

KALI LINUX:
- Port scanning: nmap, masscan, unicornscan
- Web scanning: nikto, sqlmap, nuclei, gobuster, ffuf
- Vulnerability scanning: openvas, nessus
- SSL testing: sslscan, testssl
- Cloud security: prowler, scoutsuite, cloudsploit
- Code analysis: semgrep, bandit, sonarqube
- Container scanning: trivy, anchore

DARK-MOON:
- AI agent orchestration (web, AD, Kubernetes agents)
- MCP security gateway
- Privacy-preserving tokenization (sensitive data never leaves perimeter)
- 50+ integrated tools
- CI/CD integration
- Automated report generation

PENTAGI:
- Autonomous AI agents (researcher, developer, executor)
- Knowledge graph (Graphiti + Neo4j)
- Memory system (long-term, working, episodic)
- Langfuse integration for LLM observability
- Grafana/Prometheus monitoring
- 10+ LLM provider support

LYRIE AI:
- 7-phase pentest: recon → fingerprint → scan → exploit → PoC → report
- ATP (Agent Trust Protocol) - cryptographic agent identity
- AI red-teaming (crescendo, tap, pair, gcg, autodan strategies)
- CVSS v3.1 scoring
- SMT solver integration
- Binary analysis (ROP, SMT constraints)
- 1,737+ tests

Security Considerations:
-------------------------

1. CONTAINER ISOLATION
   - All tool execution runs in Docker containers
   - Resource limits (memory, CPU, network)
   - No direct host access

2. AGENT TRUST (Lyrie ATP)
   - Ed25519 signatures for agent identity
   - Delegation chains
   - Revocation lists
   - Multisig support

3. DATA PRIVACY (Dark-Moon)
   - Sensitive data replaced with placeholders
   - Local rehydration before tool execution
   - Nothing leaves the perimeter to LLM

4. NETWORK ISOLATION
   - Separate Docker networks
   - No cross-contamination between scans
"""

from app.scanner.vapt_platforms import (
    PlatformType,
    PlatformConfig,
    KALI_TOOLS,
    VAPTExecutor,
    ScanOrchestrator,
    create_kali_executor,
    create_dark_moon_executor,
    create_pentagi_executor,
)

__all__ = [
    "PlatformType",
    "PlatformConfig",
    "KALI_TOOLS",
    "VAPTExecutor",
    "ScanOrchestrator",
    "create_kali_executor",
    "create_dark_moon_executor",
    "create_pentagi_executor",
]