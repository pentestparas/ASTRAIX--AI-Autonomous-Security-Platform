# CODING_STANDARDS.md

> How the code is written.
> Loaded when a coding-style or convention question arises.

---

## Hard invariants (non-negotiable)

1. **Strong typing everywhere.** No `Any` in public signatures; no silent `Optional`; no untyped dicts in plugin I/O.
2. **No global mutable state.** All state is passed through DI.
3. **Composition over inheritance.** Use ports (Protocol/ABCs) + adapters, not deep class hierarchies.
4. **No duplicated logic.** Two places doing the same thing is a bug to fix.
5. **No hardcoded values.** Configuration is loaded from `settings`. Constants live in one place.
6. **Async-first.** All I/O is async. CPU-bound work is offloaded with `asyncio.to_thread`.
7. **Validate every input; escape every output.** Pydantic v2 for input; never render raw plugin strings into HTML/SQL.
8. **Secrets only from env.** Never in code, never logged.
9. **Production-ready code only.** No TODO business logic, no mocked-out core flows, no commented-out features.

---

## Python — Backend

### Toolchain

- **Python:** 3.12. ``type`` system: PEP 695 generics where helpful.
- **Formatter:** Black (line-length 100). Ruff for import sort and lint.
- **Type checker:** `mypy --strict`.
- **Tests:** `pytest`, `pytest-asyncio`, `httpx` for in-process API tests, `freezegun` for time.
- **Coverage target:** ≥ 90% for `ai_secos_core/platform/`, `ai_secos_core/plugin_system/`, `ai_secos_core/normalizer/`, `ai_secos_core/risk_engine/`, `ai_secos_core/ai_gateway/`.

### Style

- Function signatures fit on one line when possible; otherwise one param per line.
- Imports sorted by `ruff` (isort + re-export).
- No `*` imports; no relative imports across packages.
- `from typing import ...` only for stdlib types; prefer `X | None` over `Optional[X]`.
- No bare `except:`; no silent `pass` in except blocks.

### Dependency Injection

- No service locator anti-pattern. All wiring is done in `ai_secos_core/platform/container.py`.
- FastAPI dependencies are thin wrappers around the container.
- Tests override implementations by passing them to the container directly.

### Async I/O

- All I/O functions are `async def`.
- DB sessions use AsyncSession.
- Subprocess plugin execution is run via `asyncio.create_subprocess_exec`, awaited, with a hard timeout.
- Retry logic is a single helper (`tenacity`); not reinvented per call site.

### Errors

- A single error hierarchy in `ai_secos_core/shared/errors.py`:
  - `PlatformError` (base)
  - `PluginError`
  - `WorkflowError`
  - `AIError`
  - `NormalizerError`
  - `RiskEngineError`
- HTTP layer maps `PlatformError` to status codes (1:1 in `platform/error_handlers.py`).
- Never raise `Exception`; never `return None` for an error path.

### Observability

- Every public function takes a `correlation_id` parameter or reads it from `contextvars`.
- Logs are structured (JSON) at info level for lifecycle; debug level for diagnostics.
- Every plugin execution emits one log line on enter/complete with: `plugin_id`, `capability_id`, `workflow_id`, `correlation_id`, `latency_ms`, `result_count`.

### Configuration

- All values via `pydantic-settings` (case-sensitive, env-first).
- `ai_secos_core/config/settings.py` is the single source.
- Fail fast on startup if a required value is missing — never at first use.

### Tests

- One test file per module; colocation optional.
- Naming: `test_module.py::TestBehavior::test_edge_xyz`.
- No real network calls in unit tests. Plugin subprocesses are mocked at the executor interface boundary.
- One deterministic test asset under `tests/fixtures/` per capability.

---

## TypeScript / Next.js — Frontend

### Toolchain

- **TypeScript:** strictest possible (`strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`).
- **Formatter:** Prettier (matches repo config).
- **Linter:** ESLint + `eslint-config-next` + `@typescript-eslint/strict-type-checked`.
- **Tests:** Vitest + React Testing Library. Coverage target ≥ 80%.

### Layering

- `frontend/core/` is **domain-agnostic.** It does not know the words "asset", "finding", "cve", "severity".
- `frontend/applications/<product>/` injects *typed objects* into core primitives.
- Mocks live in `applications/.../mocks/`, never in `core/`.
- Adapters are the only place that shapes backend JSON into frontend types.

### Components

- Function components by default; TypeScript signatures explicit.
- Props are typed; no `React.FC`; children typed as `React.ReactNode`.
- Hooks start with `use`. Lifted state only when necessary.
- No inline business logic — any logic that touches domain data lives in `applications/` adapters or hooks.

### State

- Server state: TanStack Query (`@tanstack/react-query`).
- Local UI state: `useState` / `useReducer`. Cross-page UI state: Zustand.
- Form state: `react-hook-form` + zod resolvers.

### API

- One base HTTP client in `core/services/http.ts` (typed return, retries, correlation ids).
- Endpoint functions live in `applications/<product>/services/` and are typed top-to-bottom.

### Tests

- Components are tested at the boundary: by passing typed props, asserting rendered output.
- Adapters are tested with table-driven cases.
- No snapshot tests.

---

## Repo hygiene

- No commit to `main`. PR-based, at least one approval, CI green.
- Branch names: `<milestone>/<scope>-<short-title>` (e.g., `m1/pdk-plugin-interface`).
- Conventional commits; PRs link the milestone.
- Every PR has a "verification" section listing exact commands run.

---

## What this document does NOT cover

- The architecture itself — see `ARCHITECTURE.md`.
- Scope decisions (build-now vs later) — see `MVP_SCOPE.md`.
- Sequence / milestones — see `ROADMAP.md`.
- Behavioral rules for AI engineer sessions — see `rules/00_MASTER_RULES.md`.