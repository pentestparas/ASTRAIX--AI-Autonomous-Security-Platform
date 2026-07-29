# ADR-001: Cybersecurity Knowledge Base (CSKB) as a Sibling Docker Image

> **Status:** Proposed — awaiting human approval.
> **Date:** 2026-07-27
> **Author:** AI engineer (auto-drafted per 00_MASTER_RULES.md §6)

---

## 1. Context

AstraIX Security Analyst's AI Gateway currently reasons over `SecurityFinding` objects produced by tools. To make AstraIX **the most expertise-rich AI-first cybersecurity platform**, the AI Gateway must reason over a deep, curated, **external** corpus of cybersecurity knowledge — not just the findings from a single scan.

The user has requested that we ingest several GitHub sources into a reusable knowledge base, packaged as a Docker image, so that:

1. The AstraIX AI Gateway has a **Cybersecurity Context** available before reasoning over any assessment.
2. Other AI agents, fine-tuning pipelines, and LLM components in our ecosystem can reuse the same KB.
3. AstraIX becomes the **AI-first platform for cybersecurity** — knowledgeable beyond any single product.

### Sources (per user)

**Tier 1 — Curated cybersecurity knowledge bases**

| # | Source | Type | URL |
|---|---|---|---|
| 1 | tomwechsler/Cyber_and_Information_Security_Knowledge_Base | personal study notes | https://github.com/tomwechsler/Cyber_and_Information_Security_Knowledge_Base |
| 2 | paulveillard/cybersecurity | awesome-list mega-index | https://github.com/paulveillard/cybersecurity |
| 3 | okhosting/awesome-cyber-security | awesome-list | https://github.com/okhosting/awesome-cyber-security |
| 4 | cyb3rxp/awesome-soc | awesome-list (SOC focus) | https://github.com/cyb3rxp/awesome-soc |
| 5 | mukul975/Anthropic-Cybersecurity-Skills | AI-cyber skill library | https://github.com/mukul975/Anthropic-Cybersecurity-Skills |
| 6 | Aif4thah/Dojo-101 | training dojo with labs | https://github.com/Aif4thah/Dojo-101 |
| 7 | Berkanktk/CyberSecurity | curated knowledge base | https://github.com/Berkanktk/CyberSecurity |
| 8 | Striving-to-learn/Cybersecurity-Resources | resource aggregator | https://github.com/Striving-to-learn/Cybersecurity-Resources |
| 9 | kayShahbaaz/cybersecurity-knowledge-base | knowledge base | https://github.com/kayShahbaaz/cybersecurity-knowledge-base |
| 10 | naveen-98/Cyber_Security_Reference | reference | https://github.com/naveen-98/Cyber_Security_Reference |

**Tier 2 — AI-for-cybersecurity (directly relevant to AstraIX)**

| # | Source | Type | URL |
|---|---|---|---|
| 11 | santosomar/AI-agents-for-cybersecurity | AI agent library | https://github.com/santosomar/AI-agents-for-cybersecurity |
| 12 | ElNiak/awesome-ai-cybersecurity | awesome-list (AI-cyber) | https://github.com/ElNiak/awesome-ai-cybersecurity |
| 13 | aliasrobotics/CAI | Cybersecurity AI framework | https://github.com/aliasrobotics/CAI |

**Tier 3 — Standards bodies**

| # | Source | Type | URL |
|---|---|---|---|
| 14 | OWASP Projects | standards + tools | https://owasp.org/projects/ |
| 15 | GitHub topic: cybersecurity-education | curated topic | https://github.com/topics/cybersecurity-education |
| 16 | GitHub topic: cybersecurity | curated topic | https://github.com/topics/cybersecurity |

The `awesome-*` indexes and OWASP alone reference **tens of thousands** of tools, frameworks, courses, papers, and CVEs. The AI-for-cybersecurity tier is directly relevant to AstraIX's AI Gateway and agent design.

---

## 2. Decision (Proposed)

Add a new sibling component to AstraIX:

```
astraix-security-analyst/
├── backend/                    # unchanged
├── frontend/                   # unchanged
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── kali-tools.Dockerfile
│   └── cybersec-kb.Dockerfile  # NEW — Knowledge Base image
├── cybersec_kb/                # NEW — Python package (ingest, retriever, CLI, SDK)
│   ├── __init__.py
│   ├── ingest/
│   ├── retriever/
│   ├── api/
│   ├── cli.py
│   └── sdk.py
├── docker-compose.yml          # + cybersec-kb service
└── engineering/adr/001-cskb.md
```

### 2.1 What the image ships with

- **Storage:** SQLite (single file, FTS5 + sqlite-vec vector index). One DB file = one KB.
- **Embedding model:** `BAAI/bge-small-en-v1.5` (33M params, ~130 MB) by default; pluggable via `CSKB_EMBEDDING_MODEL` env var.
- **Training stack:** `torch`, `transformers`, `peft`, `datasets`, `accelerate` so the image is also a fine-tuning environment (per user's "Full training pipeline" choice).
- **RAG API:** FastAPI on port `8400` (matches port range used by backend `8000`, frontend `3000`).
- **CLI:** `cs kb ingest`, `cs kb query "..."`, `cs kb export-dataset`, `cs kb refresh`.
- **SDK:** `from cybersec_kb import Retriever` consumable by `ai_gateway/`.

### 2.2 Ingestion pipeline

For each source repo, on first run:

1. `git clone --depth 1 <repo>` → `sources/<owner>__<repo>/`
2. Capture: commit SHA, license (parsed from `LICENSE`/`README`), default branch.
3. Walk all `*.md`, `*.mdx`, `*.txt`, `*.yaml`, `*.yml` files (skip `node_modules/`, `.git/`, `dist/`, `vendor/`).
4. For awesome-* repos: extract links from markdown, optionally clone **one hop deep** (configurable depth, default 0 = README only).
5. Chunk: 800 tokens, 100 overlap, respecting markdown headers.
6. Embed each chunk with the configured embedding model.
7. Store with provenance: `source_repo`, `source_path`, `source_url`, `license`, `commit_sha`, `ingested_at`.

### 2.3 Integration with AI Gateway

`ai_secos_core/ai_gateway/context.py` gains a new input source:

```python
class ContextBuilder:
    def build(self, request: AIRequest) -> FindingContextPayload:
        findings = self._gather_findings(request)
        asset_ctx = self._gather_asset(request)
        kb_ctx = self.kb_retriever.search(
            query=build_kb_query(findings, asset_ctx),
            top_k=request.kb_top_k or 8,
        )  # NEW — optional, off by default in M1
        return FindingContextPayload(..., kb_excerpts=kb_ctx)
```

The KB retriever is **opt-in per AI call** (`request.use_kb: bool`) so cost stays predictable.

### 2.4 Training pipeline usage

The same image can export curated datasets:

```bash
cs kb export-dataset --format jsonl --split qa --output cyber-qa.jsonl
```

Each row is `{prompt, response, source_repo, source_url}` — safe for instruction fine-tuning. Optional filtering by license, repo, category.

---

## 3. Trade-offs

| Pro | Con |
|---|---|
| Massive expertise boost for the AI Gateway | Larger Docker image (target ~4 GB) |
| Reusable across all AstraIX apps and any external AI agent | License attribution required per source (added complexity) |
| Single-binary SQLite = trivial to ship and back up | Re-ingestion on schema change requires re-embed (cost) |
| Pluggable embedding = users can swap to OpenAI, Cohere, etc. | First-run ingest is slow (5-15 min for ~10k chunks) |
| Local-first = no data leaks to third-party vector DBs | One hop deep ingestion can balloon size; default is 0 |
| Also doubles as a fine-tuning environment | Adds a new service to docker-compose |
| SQLite + sqlite-vec means zero external services to run | No multi-tenant isolation — single-user DB |

---

## 4. Alternatives Considered

- **ChromaDB / Qdrant / Weaviate**: rejected as default (extra service). Pluggable as alternative store via `CSKB_STORE=chroma`.
- **Postgres + pgvector**: rejected — adds a heavyweight DB for what is essentially one vector table.
- **Neo4j**: rejected — overlaps with `graphify-out/`; keep that for the local code graph, use vector for the external KB.
- **Cloud-only (Pinecone / Weaviate Cloud)**: rejected — breaks the local-first promise and adds monthly cost.
- **Fine-tuning only (no RAG)**: rejected — RAG gives current, citable, per-scan grounding; training alone goes stale.

---

## 5. Compliance with Platform Principles

| Principle | How this proposal complies |
|---|---|
| AI reasons. Tools execute. | KB is consumed by the AI Gateway (reasoning layer). Ingestion is a build-time tool, not runtime. |
| Capabilities orchestrate plugins. | KB is exposed as a **port** (`KBSearch` capability), not a direct plugin call from any application. |
| Plugins return structured data only. | KB chunks are typed `KBChunk` objects, not raw text blobs. |
| All output must normalize. | KB chunks become `KBContextExcerpt` with declared fields; raw text is opaque. |
| Apps never call plugins directly. | Apps call the KB via `ContextBuilder` only; never directly. |

---

## 6. Open Questions for Human Sponsor

1. **License acceptance.** Some awesome-* repos are CC-BY-SA, some MIT, some unspecified. Confirm we can ingest + redistribute excerpts under their terms (we will only embed chunks; full files stay in their original repos).
2. **KB size budget.** Default target: ≤ 50,000 chunks. Want to set a hard cap?
3. **One-hop deep on links.** Default OFF. Confirm?
4. **First-class integration with the AI Gateway.** Default OFF (`use_kb=False`). Confirm we should ship the integration but leave it off?
5. **Naming.** Working name: `astraix/cskb:latest` for the image and `cybersec_kb` for the Python package. Confirm or rename.

---

## 7. Implementation Plan (Pending Approval)

Once approved, this becomes the execution order:

1. Scaffold `cybersec_kb/` Python package with `Retriever`, `KBStore`, `Ingestor`, `API`, `CLI`, `SDK`.
2. Write `docker/cybersec-kb.Dockerfile`.
3. Write ingestion script (clones, parses, chunks, embeds).
4. Write FastAPI retriever endpoint.
5. Write CLI.
6. Wire KB retriever into `ai_secos_core/ai_gateway/context.py`.
7. Update `docker-compose.yml`.
8. Update `AGENTS.md`, `CHANGELOG.md`, `README.md`.
9. Test with `docker compose up -d` and a real ingestion run.
10. Commit.

Each step **stops and waits** for review per `00_MASTER_RULES.md` §18.

---

## 8. What This Document Does NOT Cover

- Modifications to existing engineering documents (`ROADMAP.md`, `MVP_SCOPE.md`, `ARCHITECTURE.md`, `PROJECT_MANIFEST.md`, `00_MASTER_RULES.md`) — those remain frozen per §17.
- A new milestone for the CSKB in `ROADMAP.md` — proposed as **M5.5 — Cybersecurity Knowledge Base**, after M5 (UI) completes.
- Pricing, hosting, or distribution decisions — out of scope here.
