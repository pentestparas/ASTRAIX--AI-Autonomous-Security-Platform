# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-07-23

### Added

- **Real VAPT Pipeline** — Docker-based Kali container execution for actual security scanning (not simulations)
- **Custom Kali Image** (`astraix-kali:latest`) — Pre-installed with nmap, nikto, sqlmap, nuclei, gobuster, sslscan
- **VAPT API** — `POST /api/v1/vapt/scan/quick` endpoint for quick security assessments
- **AI Summaries** — Gemini-powered executive summaries and risk recommendations
- **Risk Scoring Engine** — 0-100 risk scores for canonical security findings
- **Normalized Findings** — Tool output converted to canonical `SecurityFinding` format
- **Frontend Dashboard** — Next.js 14 with project management, scan history, findings triage
- **Auth Fix** — VAPT page project dropdown now uses authenticated API client
- **Docker Compose Stack** — PostgreSQL, Redis, Backend, Frontend with health checks
- **Plugin Architecture** — Extensible system for adding security tools

### Changed

- **KALI_IMAGE** updated from `kalilinux/kali-rolling:latest` → `astraix-kali:latest`
- **Backend Dockerfile** — Removed `gosu` and `USER appuser` directive; uvicorn runs as root
- **README.md** — Complete rewrite with architecture, quick start, and API reference
- **Frontend TypeScript** — VAPT page uses `projectsApi.list()` instead of plain `fetch()`

### Security

- Backend container runs as root with Docker socket access for container execution
- API authentication required for all project and scan endpoints

### Infrastructure

- Docker API 29.6.1+ compatible
- macOS ARM (Apple Silicon) Docker Desktop support confirmed
- Custom Kali image ~4GB with full toolchain

## [0.0.1] - 2024

### Added (Initial MVP)

- Repository skeleton with FastAPI backend and Next.js frontend
- Docker Compose setup with PostgreSQL and Redis
- Engineering documents (ROADMAP, ARCHITECTURE, CODING_STANDARDS)
- Initial UI pages (Dashboard, Projects, Scans, Findings, Reports, Settings)
- Auth system with JWT tokens and demo user
- Basic project and membership models