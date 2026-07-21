# Risk Engine

> 41 nodes · cohesion 0.08

## Key Concepts

- **StaticRiskSignalProvider** (16 connections) — `backend/ai_secos_core/risk_engine/providers.py`
- **DefaultRiskEngine** (12 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **RiskSignals** (11 connections) — `backend/ai_secos_core/risk_engine/types.py`
- **RiskEngineResult** (9 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **RiskFactor** (9 connections) — `backend/ai_secos_core/risk_engine/types.py`
- **engine.py** (7 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **NoopRiskEngine** (7 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **RiskEngine** (7 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **RiskSignalProvider** (7 connections) — `backend/ai_secos_core/risk_engine/providers.py`
- **.score()** (6 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **.score()** (6 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **types.py** (6 connections) — `backend/ai_secos_core/risk_engine/types.py`
- **RiskScore** (6 connections) — `backend/ai_secos_core/risk_engine/types.py`
- **._evaluate()** (4 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **._to_signals()** (4 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **.score()** (4 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **.evaluate()** (4 connections) — `backend/ai_secos_core/risk_engine/providers.py`
- **.build()** (4 connections) — `backend/ai_secos_core/risk_engine/types.py`
- **_noop_severity_to_score()** (3 connections) — `backend/ai_secos_core/risk_engine/engine.py`
- **providers.py** (3 connections) — `backend/ai_secos_core/risk_engine/providers.py`
- **.evaluate()** (3 connections) — `backend/ai_secos_core/risk_engine/providers.py`
- **._business_context()** (2 connections) — `backend/ai_secos_core/risk_engine/providers.py`
- **._exploitability()** (2 connections) — `backend/ai_secos_core/risk_engine/providers.py`
- **._impact()** (2 connections) — `backend/ai_secos_core/risk_engine/providers.py`
- **._likelihood()** (2 connections) — `backend/ai_secos_core/risk_engine/providers.py`
- *... and 16 more nodes in this community*

## Relationships

- [[Context Building]] (10 shared connections)
- [[Community 45]] (8 shared connections)
- [[App Factory & Null Providers]] (4 shared connections)
- [[Assessment API]] (3 shared connections)
- [[Task & Risk Types]] (3 shared connections)

## Source Files

- `backend/ai_secos_core/risk_engine/engine.py`
- `backend/ai_secos_core/risk_engine/providers.py`
- `backend/ai_secos_core/risk_engine/types.py`

## Audit Trail

- EXTRACTED: 130 (80%)
- INFERRED: 32 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*