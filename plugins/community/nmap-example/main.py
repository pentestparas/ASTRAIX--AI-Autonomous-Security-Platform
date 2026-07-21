#!/usr/bin/env python
"""
Nmap Scanner Plugin
--------------------
Input: {
  "target": "192.168.1.1",
  "deep": false,
}

Output: {
  "findings": [...],
  "stats": {...},
}

Run: pluginctl run scanners/nmap-ipv4 --param target=192.168.1.1
"""

import json
import os
import subprocess
import sys
from typing import Dict, Union
from datetime import datetime
from pydantic import ValidationError

from api import FindingOut, PluginOutput, PluginError


class NmapScanner:
    PLUGIN_ID = "scanners/nmap-ipv4"

    def __init__(self):
        self.nmap_path = os.environ.get("NMAP_PATH", "nmap")

    def run(self, stdin: Union[str, Dict] = "{}") -> Union[PluginOutput, PluginError]:
        """Run as process: stdin → scan → stdout"""
        try:
            input_data = json.loads(stdin) if isinstance(stdin, str) else stdin
            result = self._run_scan(**input_data)
            return PluginOutput(**result)
        except ValidationError as exc:
            return PluginError(error="Schema validation failed", details=exc.errors())
        except Exception as exc:
            return PluginError(error=str(exc))

    def _run_scan(
        self,
        target: str,
        deep: bool = False,
        flags: str = "-sV",
    ) -> Dict:
        """Run nmap, parse output, return findings."""
        cmd = [self.nmap_path, *flags.split()]
        if deep:
            cmd.append("-O")
        cmd.append(target)

        start = datetime.now()
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        duration = (datetime.now() - start).total_seconds()

        if proc.returncode != 0:
            raise RuntimeError(f"Nmap failed: {proc.stderr}")

        findings = self._parse_nmap(proc.stdout)
        return {
            "findings": findings,
            "stats": {
                "duration": duration,
                "target": target,
                "hosts_up": len(findings) // 3,  # heuristic
                "services_scanned": len(findings),
            },
        }

    def _parse_nmap(self, output: str) -> list:
        """Parse Nmap XML/text → findings."""
        findings = []
        # Stripped parsing: real code uses `python-nmap`
        for line in output.splitlines():
            if "/open/" in line:
                parts = line.strip().split()
                port_proto, service = parts[0], parts[2]
                port, proto = port_proto.split("/")
                finding = {
                    "title": f"Open port {port}/{proto}",
                    "description": f"Service {service}",
                    "severity": "medium",
                    "asset": "",  # target filled by orchestrator
                    "details": {
                        "port": int(port),
                        "protocol": proto,
                        "service": service,
                    },
                }
                findings.append(finding)
        return findings


if __name__ == "__main__":
    scanner = NmapScanner()
    result = scanner.run(sys.stdin.read())
    print(result.json(indent=2))