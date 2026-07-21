# BasePlugin interface for AstraIX plugins.
# Plugins are isolated processes (Python, Go, etc.) that run inside the orchestrator.
# 
# For Python plugins:
#   inherit BasePlugin, implement required methods.
# 
# For non-Python plugins:
#   implement `plugin.yml`, process stdin/stdout as described.

import abc
import json
from typing import Dict, Any, Optional, Union, List
from pydantic import BaseModel, ValidationError


class PluginSchema(BaseModel):
    """Schema for plugin I/O, described in plugin.yml."""
    input: dict
    output: dict


class FindingOut(BaseModel):
    """Output schema for a finding (partial)."""
    title: str
    description: Optional[str] = None
    severity: str
    asset: str
    details: Optional[dict] = None
    remediation: Optional[str] = None
    reference: Optional[str] = None


class PluginOutput(BaseModel):
    """Schema for successful plugin output."""
    findings: List[FindingOut] = []
    stats: Optional[dict] = None


class PluginError(BaseModel):
    """Schema for reporting plugin errors."""
    error: str
    details: Optional[dict] = None


class BasePlugin(abc.ABC):
    """
    Abstract base class every plugin must implement.

    Plugins run as subprocesses.
    Input/output via stdin/json → stdout/json.
    """

    # --- Plugin info (provided in `plugin.yml`) ---
    PLUGIN_ID: str
    PLUGIN_NAME: str
    PLUGIN_TYPE: str  # scanner, analyzer, reporter
    PLUGIN_AUTHOR: str = "AstraIX"
    PLUGIN_VERSION: str = "0.1.0"
    PLUGIN_SCHEMA: PluginSchema

    def __init__(self, schema=None):
        if schema:
            self.PLUGIN_SCHEMA = PluginSchema.parse_obj(schema)

    # --- Plugin I/O: main() ---

    def run(self, stdin: Union[str, dict, None] = None) -> Union[PluginOutput, PluginError]:
        """Entry point: run plugin."""
        try:
            input_data = self._parse_input(stdin) if stdin else {}
            input_data = self.validate_input(input_data)
            result = self._run(input_data)
            return self.validate_output(result)
        except ValidationError as exc:
            return PluginError(error="Invalid input/output schema", details=exc.errors())
        except Exception as exc:
            return PluginError(error=str(exc))

    @classmethod
    def main(cls) -> None:
        """Run as CLI: read stdin, run plugin, write stdout."""
        raw_input = sys.stdin.read() or "{}"
        instance = cls()
        result = instance.run(raw_input)
        print(json.dumps(result.dict(), indent=2))

    # --- Methods for plugin authors ---

    @abc.abstractmethod
    def _run(self, input_data: dict) -> PluginOutput:
        """Subclasses MUST override: run plugin logic."""
        raise NotImplementedError("_run() must be implemented")

    def validate_input(self, input_data: dict) -> dict:
        """Validate input against schema."""
        return self.PLUGIN_SCHEMA.input.parse_obj(input_data).dict()

    def validate_output(self, output_data: dict) -> PluginOutput:
        """Validate output against schema."""
        if "error" in output_data:
            return PluginError.parse_obj(output_data)
        return PluginOutput.parse_obj(output_data)

    # --- Helper methods ---

    @classmethod
    def _parse_input(cls, raw_input: Union[str, dict]) -> dict:
        """Parse stdin: str → dict."""
        if isinstance(raw_input, str):
            return json.loads(raw_input)
        return raw_input

    def log(self, message: str, level: str = "info", **kwargs) -> None:
        """Structured logging accessible to orchestrator."""
        log_entry = {
            "plugin": self.PLUGIN_ID,
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **kwargs,
        }
        print(json.dumps(log_entry), file=sys.stderr)