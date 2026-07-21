"""
VAPT Data Models

Core data structures for VAPT operations.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, field_validator


class VAPTScanType(str, Enum):
    """Types of VAPT scans."""
    NETWORK = "network"
    WEB = "web"
    API = "api"
    SSL = "ssl"
    CONTAINER = "container"
    FULL = "full"


class VAPTToolStatus(str, Enum):
    """Tool execution status."""
    AVAILABLE = "available"
    INSTALLED = "installed"
    MISSING = "missing"
    ERROR = "error"


class VAPTSeverity(str, Enum):
    """Finding severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class VAPTTarget(BaseModel):
    """VAPT scan target."""
    value: str = Field(..., description="Target IP, URL, domain, or hostname")
    type: str = Field(..., description="Target type: ip, url, domain, hostname")

    @field_validator("value")
    @classmethod
    def validate_target(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("Target cannot be empty")
        return v.strip()

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "type": self.type}


class VAPTTool(BaseModel):
    """Security tool definition."""
    id: str
    name: str
    command: str
    description: str
    category: VAPTScanType
    args: List[str] = Field(default_factory=list)
    timeout: int = 300
    needs_root: bool = False
    requires_url: bool = False
    requires_ip: bool = False
    output_format: str = "text"

    def build_command(self, target: str, extra_args: List[str] = None) -> List[str]:
        """Build full command with target."""
        cmd = [self.command]
        cmd.extend(self.args)
        if extra_args:
            cmd.extend(extra_args)
        cmd.append(target)
        return cmd


class VAPTFinding(BaseModel):
    """A security finding from VAPT scan."""
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    severity: VAPTSeverity
    cvss_score: Optional[float] = None
    tool_name: str
    target: str
    host: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[str] = None
    service: Optional[str] = None
    path: Optional[str] = None
    vulnerability_type: Optional[str] = None
    remediation: Optional[str] = None
    reference: Optional[str] = None
    cve: Optional[str] = None
    cwe: Optional[str] = None
    payload: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    status: str = "open"
    confidence: str = "confirmed"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "cvss_score": self.cvss_score,
            "tool_name": self.tool_name,
            "target": self.target,
            "host": self.host,
            "port": self.port,
            "remediation": self.remediation,
            "created_at": self.created_at.isoformat(),
        }


class VAPTScanRequest(BaseModel):
    """Request for a VAPT scan."""
    id: UUID = Field(default_factory=uuid4)
    target: VAPTTarget
    scan_type: VAPTScanType
    tools: List[str] = Field(default_factory=list, description="Tool IDs to use, empty = auto")
    deep: bool = Field(default=False, description="Enable deep scanning")
    aggressive: bool = Field(default=False, description="Enable aggressive mode")
    organization_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    assessment_id: Optional[UUID] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VAPTScanResult(BaseModel):
    """Result from a VAPT scan."""
    id: UUID = Field(default_factory=uuid4)
    request: VAPTScanRequest
    status: str = "pending"
    findings: List[VAPTFinding] = Field(default_factory=list)
    tool_results: Dict[str, Any] = Field(default_factory=dict)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    duration: float = 0.0
    errors: List[str] = Field(default_factory=list)
    success: bool = False
    message: str = ""

    def add_finding(self, finding: VAPTFinding) -> None:
        self.findings.append(finding)

    def get_severity_counts(self) -> Dict[VAPTSeverity, int]:
        counts = {sev: 0 for sev in VAPTSeverity}
        for f in self.findings:
            counts[f.severity] += 1
        return counts

    def finalize(self, status: str, message: str = "") -> None:
        self.status = status
        self.completed_at = datetime.utcnow()
        self.duration = (self.completed_at - self.started_at).total_seconds()
        self.message = message
        self.success = status == "completed"


class ToolHealth(BaseModel):
    """Health status of a VAPT tool."""
    id: str
    name: str
    installed: bool
    path: Optional[str] = None
    version: Optional[str] = None
    status: VAPTToolStatus = VAPTToolStatus.MISSING