"""
Scanner Models

Enterprise-grade data models for security scanning operations.
All timestamps in UTC. All UUIDs are v4.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict


class Severity(str, Enum):
    """CVSS-based severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"
    UNKNOWN = "unknown"


class ScanStatus(str, Enum):
    """Scan lifecycle status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIAL = "partial"  # Some tools failed


class ToolCapability(str, Enum):
    """Security tool categories/capabilities."""
    NETWORK_VAPT = "network_vapt"
    WEB_VAPT = "web_vapt"
    CLOUD_SECURITY = "cloud_security"
    CODE_AUDIT = "code_audit"
    API_SECURITY = "api_security"
    CONTAINER_SECURITY = "container_security"
    SSL_SECURITY = "ssl_security"
    DNS_RECON = "dns_recon"


class ToolResult(BaseModel):
    """Result from a single security tool execution."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tool_id: str
    tool_name: str
    success: bool
    duration: float = Field(description="Execution time in seconds")
    started_at: datetime
    completed_at: datetime
    stdout: str = Field(default="", description="Tool raw output")
    stderr: str = Field(default="", description="Tool error output")
    return_code: int = Field(default=0, description="Process exit code")
    findings: List["Finding"] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def has_findings(self) -> bool:
        return len(self.findings) > 0


class Finding(BaseModel):
    """Standardized security finding from any tool."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    severity: Severity
    cvss_score: Optional[float] = Field(default=None, description="CVSS v3 score (0-10)")
    cvss_vector: Optional[str] = Field(default=None, description="CVSS vector string")

    # Finding metadata
    tool_name: str
    plugin_id: str
    target: str

    # Technical details
    port: Optional[int] = None
    protocol: Optional[str] = None
    service: Optional[str] = None
    host: Optional[str] = None
    path: Optional[str] = None
    parameter: Optional[str] = None
    vulnerability_type: Optional[str] = None

    # Finding context
    details: Dict[str, Any] = Field(default_factory=dict)
    remediation: Optional[str] = None
    reference: Optional[str] = None
    cve: Optional[str] = None
    cwe: Optional[str] = None
    payload: Optional[str] = None

    # Status
    status: str = "open"
    false_positive: bool = False
    confirmed: bool = False

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def from_severity(cls, severity: str) -> "Finding":
        """Map severity string to Severity enum."""
        severity_map = {
            "critical": Severity.CRITICAL,
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
            "info": Severity.INFO,
            "informational": Severity.INFO,
        }
        return cls(severity=severity_map.get(severity.lower(), Severity.UNKNOWN))


class ScanRequest(BaseModel):
    """Request to execute one or more security tools against a target."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    target: str = Field(..., description="Target IP, URL, domain, or asset identifier")
    tools: List[str] = Field(..., description="List of tool IDs to execute")
    capability: ToolCapability = Field(..., description="Primary capability/category")

    # Scan parameters
    deep: bool = Field(default=False, description="Enable deep/intensive scanning")
    aggressive: bool = Field(default=False, description="Enable aggressive mode")

    # Tool-specific config
    tool_config: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Per-tool configuration overrides"
    )

    # Timing
    timeout: int = Field(default=3600, description="Overall scan timeout in seconds")
    rate_limit: Optional[int] = Field(default=None, description="Requests per second limit")

    # Context
    organization_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    assessment_id: Optional[UUID] = None

    def get_tool_config(self, tool_id: str) -> Dict[str, Any]:
        """Get merged config for a specific tool."""
        base = {
            "target": self.target,
            "deep": self.deep,
            "aggressive": self.aggressive,
            "timeout": self.timeout,
        }
        tool_override = self.tool_config.get(tool_id, {})
        return {**base, **tool_override}


class ScanResult(BaseModel):
    """Result from executing a scan with one or more tools."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = Field(default_factory=uuid4)
    status: ScanStatus
    target: str
    capability: ToolCapability

    # Timing
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration: float = Field(default=0.0, description="Total scan duration in seconds")

    # Tool results
    tool_results: List[ToolResult] = Field(default_factory=list)

    # Aggregated findings
    findings: List[Finding] = Field(default_factory=list)
    findings_count: int = 0
    severity_counts: Dict[Severity, int] = Field(default_factory=dict)

    # Metadata
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Status
    success: bool = True
    message: str = ""

    def add_tool_result(self, result: ToolResult) -> None:
        """Add a tool result and update aggregated findings."""
        self.tool_results.append(result)
        if result.success:
            self.findings.extend(result.findings)
        else:
            self.errors.extend(result.errors)

        # Update severity counts
        for finding in result.findings:
            current = self.severity_counts.get(finding.severity, 0)
            self.severity_counts[finding.severity] = current + 1

        self.findings_count = len(self.findings)

    def finalize(self, status: ScanStatus, message: str = "") -> None:
        """Finalize the scan result."""
        self.status = status
        self.completed_at = datetime.utcnow()
        self.message = message
        self.success = status == ScanStatus.COMPLETED

        if self.started_at and self.completed_at:
            self.duration = (self.completed_at - self.started_at).total_seconds()

        # Update status based on results
        if not self.tool_results:
            self.status = ScanStatus.FAILED
            self.success = False
        elif self.errors and not self.findings:
            self.status = ScanStatus.PARTIAL


class ScanQueueItem(BaseModel):
    """Item in the scan execution queue."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: UUID = Field(default_factory=uuid4)
    scan_request: ScanRequest
    priority: int = Field(default=0, description="Higher = more priority")
    status: ScanStatus = ScanStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[ScanResult] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3


# Update forward references
Finding.model_rebuild()
ToolResult.model_rebuild()