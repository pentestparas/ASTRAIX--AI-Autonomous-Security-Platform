"""Capability-specific error types."""

from ai_secos_core.shared.errors import PlatformError


class CapabilityNotFoundError(PlatformError):
    """Raised when a capability is not found in the registry."""

    code = "capability_not_found"
    http_status = 404


class CapabilityAlreadyRegisteredError(PlatformError):
    """Raised when attempting to register a duplicate capability."""

    code = "capability_already_registered"
    http_status = 409


class CapabilityResolverError(PlatformError):
    """Raised when capability resolution fails (missing workflow, etc.)."""

    code = "capability_resolver_error"
    http_status = 422