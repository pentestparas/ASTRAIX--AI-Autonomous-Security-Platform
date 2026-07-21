# App Factory & Null Providers

> 62 nodes · cohesion 0.06

## Key Concepts

- **Container** (47 connections) — `backend/ai_secos_core/api_platform/container.py`
- **_MutableContainer** (44 connections) — `backend/ai_secos_core/api_platform/container.py`
- **build_default_container()** (34 connections) — `backend/ai_secos_core/api_platform/container.py`
- **NormalizerRegistry** (21 connections) — `backend/ai_secos_core/finding_engine/normalizer.py`
- **DefaultFindingEngine** (20 connections) — `backend/ai_secos_core/finding_engine/engine.py`
- **FindingEngineContext** (17 connections) — `backend/ai_secos_core/finding_engine/engine.py`
- **FindingEngine** (13 connections) — `backend/ai_secos_core/finding_engine/engine.py`
- **NoopFindingCorrelator** (12 connections) — `backend/ai_secos_core/finding_engine/correlator.py`
- **NoopFindingEnricher** (12 connections) — `backend/ai_secos_core/finding_engine/enricher.py`
- **PluginLoader** (12 connections) — `backend/ai_secos_core/plugin_system/loader.py`
- **FindingEngineConfig** (11 connections) — `backend/ai_secos_core/finding_engine/engine.py`
- **NullContextBuilder** (10 connections) — `backend/ai_secos_core/ai_gateway/context.py`
- **FindingCorrelator** (10 connections) — `backend/ai_secos_core/finding_engine/correlator.py`
- **FindingEnricher** (10 connections) — `backend/ai_secos_core/finding_engine/enricher.py`
- **NullProvider** (6 connections) — `backend/ai_secos_core/ai_gateway/provider.py`
- **build_app()** (6 connections) — `backend/ai_secos_core/api_platform/app_factory.py`
- **lifespan()** (5 connections) — `backend/ai_secos_core/api_platform/app_factory.py`
- **container.py** (5 connections) — `backend/ai_secos_core/api_platform/container.py`
- **.freeze()** (5 connections) — `backend/ai_secos_core/api_platform/container.py`
- **engine.py** (5 connections) — `backend/ai_secos_core/finding_engine/engine.py`
- **app_factory.py** (4 connections) — `backend/ai_secos_core/api_platform/app_factory.py`
- **.mutate()** (4 connections) — `backend/ai_secos_core/api_platform/container.py`
- **.__post_init__()** (4 connections) — `backend/ai_secos_core/finding_engine/engine.py`
- **.process()** (4 connections) — `backend/ai_secos_core/finding_engine/engine.py`
- **test_container.py** (4 connections) — `backend/ai_secos_core/tests/platform/test_container.py`
- *... and 37 more nodes in this community*

## Relationships

- [[Context Building]] (34 shared connections)
- [[Assessment API]] (26 shared connections)
- [[Metrics System]] (16 shared connections)
- [[Community 22]] (12 shared connections)
- [[Community 45]] (11 shared connections)
- [[Plugin Loader]] (7 shared connections)
- [[Community 41]] (6 shared connections)
- [[FastAPI Dependencies]] (5 shared connections)
- [[Platform Settings]] (4 shared connections)
- [[Risk Engine]] (4 shared connections)
- [[Community 37]] (3 shared connections)
- [[Community 36]] (3 shared connections)

## Source Files

- `backend/ai_secos_core/ai_gateway/context.py`
- `backend/ai_secos_core/ai_gateway/provider.py`
- `backend/ai_secos_core/api_platform/app_factory.py`
- `backend/ai_secos_core/api_platform/container.py`
- `backend/ai_secos_core/finding_engine/correlator.py`
- `backend/ai_secos_core/finding_engine/engine.py`
- `backend/ai_secos_core/finding_engine/enricher.py`
- `backend/ai_secos_core/finding_engine/normalizer.py`
- `backend/ai_secos_core/plugin_system/loader.py`
- `backend/ai_secos_core/tests/platform/test_container.py`

## Audit Trail

- EXTRACTED: 153 (41%)
- INFERRED: 221 (59%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*