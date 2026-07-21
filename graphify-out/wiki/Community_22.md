# Community 22

> 22 nodes · cohesion 0.16

## Key Concepts

- **DefaultAIGateway** (17 connections) — `backend/ai_secos_core/ai_gateway/gateway.py`
- **AIGateway** (15 connections) — `backend/ai_secos_core/ai_gateway/gateway.py`
- **NoopResponseParser** (10 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **AIResponse** (9 connections) — `backend/ai_secos_core/ai_gateway/provider.py`
- **ParsedAIResponse** (9 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **ResponseParser** (9 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **.complete()** (5 connections) — `backend/ai_secos_core/ai_gateway/gateway.py`
- **.complete()** (4 connections) — `backend/ai_secos_core/ai_gateway/gateway.py`
- **response.py** (4 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **.parse()** (4 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **gateway.py** (3 connections) — `backend/ai_secos_core/ai_gateway/gateway.py`
- **.from_text()** (3 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **.parse()** (3 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **TokenBudget** (2 connections)
- **AI Gateway — composed pipeline.  Pipeline order (matches Architecture):    1. Ro** (1 connections) — `backend/ai_secos_core/ai_gateway/gateway.py`
- **Single entry point for AI reasoning tasks.      Implementations are responsible** (1 connections) — `backend/ai_secos_core/ai_gateway/gateway.py`
- **Default wired pipeline.** (1 connections) — `backend/ai_secos_core/ai_gateway/gateway.py`
- **A provider's structured response.** (1 connections) — `backend/ai_secos_core/ai_gateway/provider.py`
- **Response Parser — safe parsing of provider output back to types.  The Gateway em** (1 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **Factory: try JSON parse; fall back to a `{"text": ...}` envelope.** (1 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **Parse a `AIResponse` into a typed `ParsedAIResponse`.** (1 connections) — `backend/ai_secos_core/ai_gateway/response.py`
- **Default at Milestone 1.      Just delegates to `ParsedAIResponse.from_text`.** (1 connections) — `backend/ai_secos_core/ai_gateway/response.py`

## Relationships

- [[App Factory & Null Providers]] (12 shared connections)
- [[Community 41]] (7 shared connections)
- [[Community 55]] (6 shared connections)
- [[Context Building]] (2 shared connections)
- [[Community 37]] (2 shared connections)
- [[Community 29]] (2 shared connections)
- [[Community 33]] (2 shared connections)

## Source Files

- `backend/ai_secos_core/ai_gateway/gateway.py`
- `backend/ai_secos_core/ai_gateway/provider.py`
- `backend/ai_secos_core/ai_gateway/response.py`

## Audit Trail

- EXTRACTED: 61 (58%)
- INFERRED: 44 (42%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*