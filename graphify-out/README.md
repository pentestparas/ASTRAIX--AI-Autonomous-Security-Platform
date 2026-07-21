# AstraIX Security Analyst - Knowledge Graph

## Overview

This directory contains a structured knowledge graph of the AstraIX Security Analyst codebase.
This serves as the **authoritative source of truth** for AI development assistance.

## Files

- **`KNOWLEDGE_BASE.md`** - Comprehensive markdown documentation of all concepts, architecture, and relationships
- **`graph.json`** - Structured JSON version of the knowledge graph for programmatic access
- **`GRAPH_REPORT.md`** - Analysis report (when generated via graphify tool)

## Purpose

This knowledge base exists to:

1. **Prevent AI/LLM hallucinations** - Provides accurate context about the project
2. **Ensure architectural alignment** - All AI assistants work from the same understanding
3. **Accelerate development** - Rich context reduces time spent on basic understanding
4. **Maintain consistency** - Single source of truth for the project's architecture

## How AI Assistants Should Use This

### For Code Questions

1. Read `KNOWLEDGE_BASE.md` for architectural context
2. Check `graph.json` for component relationships
3. Reference the engineering docs for specific details

### For New Features

1. Check if the feature aligns with the **Five Principles**
2. Verify it fits the **abstraction levels** (Application → Capability → Workflow → Plugin)
3. Ensure it doesn't violate **non-goals**

### For Bug Fixes

1. Identify which layer the bug exists in
2. Understand the data flow through the pipeline
3. Check if the issue violates any architectural principles

## Key Concepts

### Three-Layer Architecture

```
AI-SecOS Core         ← Reusable runtime
Applications          ← Security Analyst (first product)
Plugins               ← Isolated security tools
```

### Four Abstraction Levels

```
Application → Capability → Workflow → Plugin
```

### Finding Engine Pipeline

```
Raw Plugin Output → Normalize → Dedupe → Enrich → Correlate → Canonical Finding
```

## Updating the Knowledge Base

When significant changes are made:

1. Update `graph.json` with new components
2. Add relationships to maintain accuracy
3. Update `KNOWLEDGE_BASE.md` with new documentation
4. Update milestone status

## Quick Reference

### Mission
Build the world's most extensible AI-native cybersecurity platform.

### Vision
AI-SecOS is the runtime. AstraIX Security Analyst is the first application.

### Architecture
```
AstraIX Platform
├── AI-SecOS Core         (reusable runtime)
├── Applications
│   └── Security Analyst  (first product)
└── Plugins               (isolated subprocesses)
```

### Current Focus
Backend M1-M4 (AI-SecOS Core + First Plugin + Discovery + Web Security Assessment)
Frontend M5 is not yet started.

### API Base URL
`http://localhost:8000/api/v1`

### Important Ports
- Backend: 8000
- Frontend: 3000
- Swagger UI: 8000/docs
- PostgreSQL: 5432
- Redis: 6379

---

**Last Updated:** 2026-07-15
**Status:** Active Development
