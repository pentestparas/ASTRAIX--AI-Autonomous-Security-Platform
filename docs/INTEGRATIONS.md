# External VAPT Platform Adapters

AstraIX ships a pluggable adapter framework (`backend/app/vapt/adapters/`) that
lets scans execute through external VAPT platforms in addition to the built-in
Kali toolchain (`nmap/nikto/sqlmap/nuclei/gobuster/sslscan`).

Adapters run **after** the built-in recon phase and **before** the
researcher/verifier agents, so their findings flow through the same
enrichment → re-exploit → risk-scoring → report pipeline as native findings.

## How it works

```
analyze_and_scan()                    (orchestrator.py)
 ├─ recon.execute_scan()              built-in Kali tools
 ├─ _run_adapters()                   parallel external platforms   <-- NEW
 │    └─ for each enabled adapter:    allow_for(scan_type, target_info)
 │         run_scan(target, scan_id, ...) → AdapterScanResult
 │         result.add_finding(...)    merged into ScanResult
 │         result.tool_results[id]    status/findings/duration/errors
 ├─ researcher.enrich_findings()
 ├─ verifier.verify_findings()
 └─ risk_engine + ai_gateway → persist
```

One failing adapter never aborts a scan — its errors are captured in
`tool_results[adapter_id].errors` and surfaced in scan events/progress.

## Adapters

| Adapter ID | Platform | Mode | Requires |
|------------|----------|------|----------|
| `raccoon` | raccoon-scanner | Kali container (pip) | none — enabled by default |
| `lyrie` | lyrie-ai | Kali container (pip) | `VAPT_ADAPTER_LYRIE=true` + an LLM key (`ANTHROPIC_API_KEY`/`OPENAI_API_KEY`/`LYRIE_LICENSE_KEY`/`GEMINI_API_KEY`) |
| `xalgorix` | xalgorix | sidecar container + REST :9137 | `VAPT_ADAPTER_XALGORIX=true` + `XALGORIX_API_KEY` + `XALGORIX_LLM` |
| `darkmoon` | Dark-Moon | HTTP or CLI (`darkmoon.sh`) | `VAPT_ADAPTER_DARKMOON=true` + `DARKMOON_BASE_URL`/`DARKMOON_API_KEY` (HTTP) or `DARKMOON_PATH` (CLI) |
| `pentagi` | PentAGI | HTTP | `VAPT_ADAPTER_PENTAGI=true` + `PENTAGI_BASE_URL` (+ key or basic auth) |
| `redamon` | redamon | HTTP | `VAPT_ADAPTER_REDAMON=true` + `REDAMON_BASE_URL` (+ optional `REDAMON_API_KEY`) |
| `zenai` | zen-ai-pentest | GitHub Actions | `VAPT_ADAPTER_ZENAI=true` + `ZENAI_REPO=owner/repo` + authenticated `gh` CLI |

## Configuration

All adapters are off by default except `raccoon`. Set the flag envs in
`docker-compose.yml` (backend service) or your `.env` — see `.env.example`.

Default limits: per-adapter scan timeout **3600 s** (raccoon/lyrie 600 s),
poll intervals 15-60 s. `allow_for()` restricts web-only platforms
(lyrie/xalgorix/darkmoon/pentagi) to web targets; raccoon/redamon/zenai run
for any target.

## Deploying an external platform

Heavy platforms (darkmoon, pentagi, redamon) must be deployed separately —
they are not part of `docker-compose.yml` by design (separate LLM keys, RAM
and disk requirements). Point `*_BASE_URL` at your deployment and restart the
backend.

- **xalgorix**: `docker run --privileged -p 9137:9137 xalgord/xalgorix:latest`
  (bring your own LLM: set `XALGORIX_API_KEY`, `XALGORIX_LLM`, optional
  `XALGORIX_API_BASE`). The adapter spawns the container itself when `XALGORIX_API_BASE`
  is unset — it needs Docker socket access (already granted to the backend).
- **Dark-Moon**: clone `ASCIT31/Dark-Moon`, `docker compose up -d` its stack,
  expose its API at `DARKMOON_BASE_URL`; or mount the repo and set
  `DARKMOON_PATH` for CLI mode (`darkmoon.sh "TARGET: <host>"`, reports read
  from `DARKMOON_WORKDIR/reports/`, default `/tmp/darkmoon`).
- **PentAGI**: `vxcontrol/pentagi`, `docker compose up -d` → complete the
  setup wizard at `:8080`, then set `PENTAGI_BASE_URL`.
- **redamon**: `samugit83/redamon` — note it is disk-hungry (~70-95 GB stacks,
  up to 250 GB always-on) and brings its own Neo4j/LangGraph runtime.
- **zen-ai-pentest**: GitHub Action; the adapter triggers
  `gh workflow run <ZENAI_WORKFLOW> -f target=... -f astraix_scan_id=...` and
  polls for completion. Requires `gh` authenticated inside the backend
  container.

## Health

`GET /api/v1/vapt/adapters` → per-adapter `enabled/available/error` plus
aggregate `status` (`healthy` if any adapter available). Findings carry
`source_platform` set to the adapter id so you can trace provenance in
reports and the UI.
