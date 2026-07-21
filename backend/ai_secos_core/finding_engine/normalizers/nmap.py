"""Nmap Plugin — normalizer.

Converts raw `nmap` output into canonical `SecurityFinding` instances.

Plugin shape (nmap JSON output via -oX -):
  {
    "target": "192.168.1.1",
    "hosts": [
      {
        "ip": "192.168.1.1",
        "hostname": "server.local",
        "status": "up",
        "os": "Linux 5.4",
        "ports": [
          {"port": 22, "protocol": "tcp", "state": "open", "service": {"name": "ssh", "product": "OpenSSH", "version": "8.2"}},
          {"port": 80, "protocol": "tcp", "state": "open", "service": {"name": "http", "product": "nginx"}},
          {"port": 443, "protocol": "tcp", "state": "open", "service": {"name": "https", "product": "nginx"}}
        ],
        "scripts": [
          {"id": "http-title", "output": "Welcome to nginx"}
        ]
      }
    ],
    "summary": {"hosts_up": 1, "open_ports": 3}
  }
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Iterator, Mapping
import uuid as _uuid

from ai_secos_core.finding_engine.normalizer import FindingNormalizer
from ai_secos_core.shared.value_objects import (
    FindingEvidence,
    FindingFingerprint,
    SecurityFinding,
    Severity,
)


class NmapNormalizer(FindingNormalizer):
    """Normalizer for the nmap plugin."""

    plugin_id = "scanner/nmap"

    def normalize(
        self,
        raw_output: Mapping[str, Any],
        *,
        assessment_id,
        capability_id: str,
        asset_id: str,
    ) -> Iterator[SecurityFinding]:
        hosts = raw_output.get("hosts", [])
        for host in hosts:
            for port_finding in _normalize_host(host, assessment_id, capability_id, asset_id):
                yield port_finding
            # OS detection finding
            os = host.get("os")
            if os:
                yield _create_os_finding(host, assessment_id, capability_id, asset_id)


def _normalize_host(
    host: Mapping[str, Any],
    assessment_id: str,
    capability_id: str,
    asset_id: str,
) -> Iterator[SecurityFinding]:
    """Normalize all open ports from a host into findings."""
    ip = host.get("ip") or host.get("ipv4") or host.get("ipv6", "unknown")
    hostname = host.get("hostname") or ""
    status = host.get("status", "unknown")

    if status != "up":
        return

    ports = host.get("ports", [])
    for port_entry in ports:
        port = port_entry.get("port", 0)
        protocol = port_entry.get("protocol", "tcp")
        state = port_entry.get("state", "unknown")
        service = port_entry.get("service") or {}

        if state != "open":
            continue

        service_name = service.get("name", "unknown")
        service_product = service.get("product", "")
        service_version = service.get("version", "")
        service_extrainfo = service.get("extrainfo", "")

        title = f"Open {service_name} on {protocol}/{port}"
        if service_product:
            title = f"Open {service_product} {service_version} on {protocol}/{port}".rstrip()

        description = f"Service: {service_name}"
        if service_product:
            description += f" ({service_product} {service_version})".rstrip()
        if service_extrainfo:
            description += f" - {service_extrainfo}"
        if hostname:
            description += f" | Hostname: {hostname}"

        fingerprint = FindingFingerprint(
            hashlib.sha256(
                f"nmap-port:{ip}:{port}:{service_name}:{asset_id}".encode("utf-8")
            ).hexdigest()[:32]
        )

        yield SecurityFinding(
            id=_uuid.uuid4(),
            assessment_id=assessment_id,
            asset=asset_id,
            capability=capability_id,
            plugin="scanner/nmap",
            category="open-port",
            title=title,
            description=description[:600],
            severity=Severity.INFO,
            confidence=0.9,
            risk_score=None,
            cvss=None,
            cwe=[],
            cve=[],
            owasp=[],
            references=[],
            evidence=FindingEvidence(
                schema_name="nmap",
                raw={
                    "ip": ip,
                    "hostname": hostname,
                    "port": port,
                    "protocol": protocol,
                    "service": service,
                    "scripts": port_entry.get("scripts", []),
                },
            ),
            tags=["nmap", "port-scan", f"port-{port}", service_name],
            metadata={
                "ip": ip,
                "hostname": hostname,
                "port": port,
                "protocol": protocol,
                "service_name": service_name,
                "service_product": service_product,
                "service_version": service_version,
            },
            fingerprint=fingerprint,
        )


def _create_os_finding(
    host: Mapping[str, Any],
    assessment_id: str,
    capability_id: str,
    asset_id: str,
) -> SecurityFinding:
    """Create a finding for detected OS."""
    ip = host.get("ip") or host.get("ipv4", "unknown")
    hostname = host.get("hostname") or ""
    os = host.get("os", "unknown")

    fingerprint = FindingFingerprint(
        hashlib.sha256(f"nmap-os:{ip}:{os}:{asset_id}".encode("utf-8")).hexdigest()[:32]
    )

    description = f"Operating System detected: {os}"
    if hostname:
        description += f" (Host: {hostname})"

    return SecurityFinding(
        id=_uuid.uuid4(),
        assessment_id=assessment_id,
        asset=asset_id,
        capability=capability_id,
        plugin="scanner/nmap",
        category="os-detection",
        title=f"OS Detected: {os}",
        description=description[:600],
        severity=Severity.INFO,
        confidence=0.7,
        risk_score=None,
        cvss=None,
        cwe=[],
        cve=[],
        owasp=[],
        references=[],
        evidence=FindingEvidence(schema_name="nmap-os", raw={"ip": ip, "hostname": hostname, "os": os}),
        tags=["nmap", "os-detection", os.lower().replace(" ", "-")],
        metadata={"ip": ip, "hostname": hostname, "os": os},
        fingerprint=fingerprint,
    )