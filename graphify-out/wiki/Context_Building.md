# Context Building

> 70 nodes · cohesion 0.05

## Key Concepts

- **SecurityFinding** (75 connections) — `backend/ai_secos_core/shared/value_objects.py`
- **DefaultFindingDeduplicator** (19 connections) — `backend/ai_secos_core/finding_engine/deduplicator.py`
- **FindingDeduplicator** (16 connections) — `backend/ai_secos_core/finding_engine/deduplicator.py`
- **DefaultFindingFingerprinter** (12 connections) — `backend/ai_secos_core/finding_engine/fingerprint.py`
- **FindingFingerprint** (11 connections)
- **ContextBuilder** (9 connections) — `backend/ai_secos_core/ai_gateway/context.py`
- **FindingFingerprinter** (9 connections) — `backend/ai_secos_core/finding_engine/fingerprint.py`
- **_normalize_vulnerability()** (8 connections) — `backend/ai_secos_core/finding_engine/normalizers/trivy.py`
- **deduplicator.py** (7 connections) — `backend/ai_secos_core/finding_engine/deduplicator.py`
- **_create_os_finding()** (7 connections) — `backend/ai_secos_core/finding_engine/normalizers/nmap.py`
- **_normalize_host()** (7 connections) — `backend/ai_secos_core/finding_engine/normalizers/nmap.py`
- **_normalize_one()** (7 connections) — `backend/ai_secos_core/finding_engine/normalizers/subfinder.py`
- **trivy.py** (7 connections) — `backend/ai_secos_core/finding_engine/normalizers/trivy.py`
- **_normalize_misconfiguration()** (7 connections) — `backend/ai_secos_core/finding_engine/normalizers/trivy.py`
- **FindingContextPayload** (6 connections) — `backend/ai_secos_core/ai_gateway/context.py`
- **_merge()** (6 connections) — `backend/ai_secos_core/finding_engine/deduplicator.py`
- **nmap.py** (6 connections) — `backend/ai_secos_core/finding_engine/normalizers/nmap.py`
- **.build()** (5 connections) — `backend/ai_secos_core/ai_gateway/context.py`
- **.build()** (5 connections) — `backend/ai_secos_core/ai_gateway/context.py`
- **.fingerprint()** (5 connections) — `backend/ai_secos_core/finding_engine/fingerprint.py`
- **.normalize()** (5 connections) — `backend/ai_secos_core/finding_engine/normalizers/nmap.py`
- **subfinder.py** (5 connections) — `backend/ai_secos_core/finding_engine/normalizers/subfinder.py`
- **.normalize()** (5 connections) — `backend/ai_secos_core/finding_engine/normalizers/trivy.py`
- **context.py** (4 connections) — `backend/ai_secos_core/ai_gateway/context.py`
- **.normalize()** (4 connections) — `backend/ai_secos_core/finding_engine/normalizers/subfinder.py`
- *... and 45 more nodes in this community*

## Relationships

- [[App Factory & Null Providers]] (34 shared connections)
- [[Assessment API]] (23 shared connections)
- [[Community 33]] (18 shared connections)
- [[Risk Engine]] (10 shared connections)
- [[Community 45]] (6 shared connections)
- [[Plugin Schemas]] (5 shared connections)
- [[Community 65]] (3 shared connections)
- [[Community 53]] (3 shared connections)
- [[Projects API]] (3 shared connections)
- [[Community 28]] (3 shared connections)
- [[Community 22]] (2 shared connections)
- [[Community 41]] (1 shared connections)

## Source Files

- `backend/ai_secos_core/ai_gateway/context.py`
- `backend/ai_secos_core/finding_engine/correlator.py`
- `backend/ai_secos_core/finding_engine/deduplicator.py`
- `backend/ai_secos_core/finding_engine/enricher.py`
- `backend/ai_secos_core/finding_engine/fingerprint.py`
- `backend/ai_secos_core/finding_engine/normalizers/nmap.py`
- `backend/ai_secos_core/finding_engine/normalizers/subfinder.py`
- `backend/ai_secos_core/finding_engine/normalizers/trivy.py`
- `backend/ai_secos_core/shared/value_objects.py`

## Audit Trail

- EXTRACTED: 237 (72%)
- INFERRED: 94 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*