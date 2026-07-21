"""
AstraIX Security Scanner Module

Enterprise-grade security scanning engine that integrates with Kali Linux tools
and AI-powered VAPT platforms (Dark-Moon, PentAGI, Lyrie AI).

Modules:
    - tools: Tool registry with all supported security tools
    - executor: Tool execution engine with resource management
    - models: Scanner request/response models
    - parsers: Tool output parsers (nmap, nikto, sqlmap, nuclei, etc.)
    - vapt_platforms: Multi-platform VAPT integration (Kali, Dark-Moon, PentAGI, Lyrie)
"""

from app.scanner.models import (
    ScanRequest,
    ScanResult,
    ToolResult,
    Finding,
    Severity,
    ScanStatus,
    ToolCapability,
)
from app.scanner.executor import ScannerExecutor, get_scanner_executor
from app.scanner.tools import (
    ToolRegistry,
    get_tool_registry,
    TOOL_CATEGORIES,
    NETWORK_SCANNERS,
    WEB_SCANNERS,
    CODE_SCANNERS,
    CLOUD_SCANNERS,
)
from app.scanner.vapt_platforms import (
    PlatformType,
    PlatformConfig,
    KALI_TOOLS,
    ExternalTool,
    VAPTExecutor,
    VAPTOutputParser,
    ScanOrchestrator,
    create_kali_executor,
    create_dark_moon_executor,
    create_pentagi_executor,
    create_lyrie_executor,
    LyrieAIAgent,
)

__all__ = [
    # Models
    "ScanRequest",
    "ScanResult",
    "ToolResult",
    "Finding",
    "Severity",
    "ScanStatus",
    "ToolCapability",
    # Executor
    "ScannerExecutor",
    "get_scanner_executor",
    # Tools
    "ToolRegistry",
    "get_tool_registry",
    "TOOL_CATEGORIES",
    "NETWORK_SCANNERS",
    "WEB_SCANNERS",
    "CODE_SCANNERS",
    "CLOUD_SCANNERS",
    # VAPT Platforms
    "PlatformType",
    "PlatformConfig",
    "KALI_TOOLS",
    "ExternalTool",
    "VAPTExecutor",
    "VAPTOutputParser",
    "ScanOrchestrator",
    "create_kali_executor",
    "create_dark_moon_executor",
    "create_pentagi_executor",
    "create_lyrie_executor",
    # Lyrie AI
    "LyrieAIAgent",
]