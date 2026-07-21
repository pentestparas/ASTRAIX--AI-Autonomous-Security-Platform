from enum import Enum
from typing import Optional, List, Dict, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, validator


class PluginType(str, Enum):
    SCANNER = "scanner"
    ANALYZER = "analyzer"
    REPORTER = "reporter"
    INTEGRATOR = "integrator"
    ENRICHER = "enricher"


class PluginManifest(BaseModel):
    id: str
    name: str
    description: str
    version: str
    author: str
    type: PluginType
    runtime: str
    entrypoint: str
    schema: Dict
    limits: Dict[str, Union[str, int]]

    @validator("id")
    def id_validator(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("plugin.id: non-empty string")
        return v


class FindingOut(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str
    severity: str
    asset_id: Optional[str]
    plugin_id: Optional[str]
    details: dict = {}
    remediation: Optional[str] = None
    reference: Optional[str] = None
    recorded_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class PluginOutput(BaseModel):
    findings: List[FindingOut] = []
    stats: Optional[Dict] = None
    logs: List[dict] = []


class PluginError(BaseModel):
    error: str
    details: Optional[Dict] = None
    logs: List[dict] = []


class PluginStatus(BaseModel):
    plugin_id: str
    enabled: bool
    last_run: Optional[str] = None
    last_run_success: Optional[bool] = None
    last_error: Optional[str] = None