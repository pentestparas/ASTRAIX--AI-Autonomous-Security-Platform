"""Capability Registry — first-class Capability abstraction.

Applications request a Capability; the Core resolves it to one or more
Workflows, which fan out to Plugins. This decouples Applications from
specific tools and enables composable, reusable security capabilities.
"""

from ai_secos_core.capabilities.models import (
    Capability,
    CapabilityManifest,
    CapabilityVersion,
    CapabilityInputSchema,
    CapabilityOutputSchema,
    SupportedAssetType,
    RequiredPlugin,
    ComplianceTag,
)
from ai_secos_core.capabilities.registry import (
    CapabilityRegistry,
    CapabilityNotFoundError,
    CapabilityAlreadyRegisteredError,
)
from ai_secos_core.capabilities.loader import (
    CapabilityLoader,
    CapabilityLoaderError,
)
from ai_secos_core.capabilities.resolver import (
    CapabilityResolver,
    ResolutionError,
    ResolvedCapability,
)

__all__ = [
    "Capability",
    "CapabilityManifest",
    "CapabilityVersion",
    "CapabilityInputSchema",
    "CapabilityOutputSchema",
    "SupportedAssetType",
    "RequiredPlugin",
    "ComplianceTag",
    "CapabilityRegistry",
    "CapabilityNotFoundError",
    "CapabilityAlreadyRegisteredError",
    "CapabilityLoader",
    "CapabilityLoaderError",
    "CapabilityResolver",
    "ResolutionError",
    "ResolvedCapability",
]