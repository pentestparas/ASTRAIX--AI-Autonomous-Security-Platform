"""Finding Engine — the truth about what's been discovered.

Responsibilities (per ARCHITECTURE.md):
  - normalization (raw plugin output → SecurityFinding)
  - deduplication (deterministic fingerprint)
  - enrichment (asset context, intel) — interfaces only at M1
  - correlation (cross-plugin, cross-asset) — interfaces only at M1
  - confidence adjustment
  - tagging / mapping (MITRE, OWASP, CWE)
  - CVE enrichment

A clean separation of concerns:

  - `fingerprint.py`:    deterministic fingerprinting.
  - `normalizer.py`:     Normalizer interface + reference impl contract.
  - `deduplicator.py`:   Deduplicator interface + reference impl contract.
  - `enricher.py`:       Enricher *interface* (default no-op at M1).
  - `correlator.py`:     Correlator *interface* (default no-op at M1).
  - `engine.py`:         Pipeline orchestrating the above.
"""

from ai_secos_core.finding_engine.fingerprint import (
    FindingFingerprinter,
    DefaultFindingFingerprinter,
)
from ai_secos_core.finding_engine.normalizer import (
    FindingNormalizer,
    NormalizerRegistry,
    NormalizationError,
)
from ai_secos_core.finding_engine.deduplicator import (
    FindingDeduplicator,
    DefaultFindingDeduplicator,
)
from ai_secos_core.finding_engine.enricher import (
    FindingEnricher,
    NoopFindingEnricher,
)
from ai_secos_core.finding_engine.correlator import (
    FindingCorrelator,
    NoopFindingCorrelator,
)
from ai_secos_core.finding_engine.engine import (
    FindingEngine,
    FindingEngineConfig,
    FindingEngineContext,
    DefaultFindingEngine,
)

__all__ = [
    "FindingFingerprinter",
    "DefaultFindingFingerprinter",
    "FindingNormalizer",
    "NormalizerRegistry",
    "NormalizationError",
    "FindingDeduplicator",
    "DefaultFindingDeduplicator",
    "FindingEnricher",
    "NoopFindingEnricher",
    "FindingCorrelator",
    "NoopFindingCorrelator",
    "FindingEngine",
    "FindingEngineConfig",
    "FindingEngineContext",
    "DefaultFindingEngine",
]
