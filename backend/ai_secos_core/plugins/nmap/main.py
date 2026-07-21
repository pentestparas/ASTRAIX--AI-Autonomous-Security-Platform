#!/usr/bin/env python3
"""Nmap Plugin — network reconnaissance and port scanning.

Reads JSON from stdin: {"target": "192.168.1.1", "ports": "1-1000", ...}
Outputs structured JSON matching the NmapNormalizer schema.
"""

from __future__ import annotations

import json
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any


def build_nmap_command(
    target: str,
    ports: str = "1-1000",
    scan_type: str = "SYN",
    timing: int = 4,
    service_detection: bool = True,
    os_detection: bool = True,
    script_scan: bool = True,
    vuln_scripts: bool = False,
) -> list[str]:
    """Build nmap command arguments."""
    cmd = ["nmap"]

    # Scan type
    if scan_type == "SYN":
        cmd.append("-sS")
    elif scan_type == "connect":
        cmd.append("-sT")
    elif scan_type == "UDP":
        cmd.append("-sU")
    elif scan_type == "all":
        cmd.append("-sS")

    # Timing
    cmd.extend(["-T", str(timing)])

    # Port specification
    cmd.extend(["-p", ports])

    # Service detection
    if service_detection:
        cmd.append("-sV")

    # OS detection
    if os_detection:
        cmd.append("-O")

    # Script scan
    if script_scan:
        cmd.extend(["--script", "default"])

    # Vulnerability scripts
    if vuln_scripts:
        cmd.extend(["--script", "vuln"])

    # Output formats
    cmd.extend(["-oX", "-"])  # XML output to stdout
    cmd.extend(["-oG", "-"])  # Grepable output to stdout

    # Performance
    cmd.extend(["--max-retries", "2"])
    cmd.append("--max-scan-delay 50ms")

    # Add target
    cmd.append(target)

    return cmd


def parse_nmap_xml(xml_output: str, target: str) -> dict[str, Any]:
    """Parse nmap XML output to structured dict."""
    results: dict[str, Any] = {
        "target": target,
        "schema_version": "1.0.0",
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "hosts": [],
        "summary": {
            "hosts_up": 0,
            "hosts_down": 0,
            "open_ports": 0,
            "filtered_ports": 0,
        },
    }

    try:
        root = ET.fromstring(xml_output)
    except ET.ParseError as exc:
        results["error"] = f"XML parse error: {exc}"
        return results

    run_stats = root.find(".//runstats/finished")
    if run_stats is not None:
        results["summary"]["elapsed"] = float(run_stats.attrib.get("elapsed", 0))
        results["summary"]["hosts_up"] = int(run_stats.attrib.get("hosts", 0).split()[0]) if run_stats.attrib.get("hosts") else 0

    for host in root.findall(".//host"):
        host_data = _parse_host(host)
        results["hosts"].append(host_data)

        if host_data["status"] == "up":
            results["summary"]["hosts_up"] += 1
            for port in host_data.get("ports", []):
                if port["state"] == "open":
                    results["summary"]["open_ports"] += 1
                elif port["state"] == "filtered":
                    results["summary"]["filtered_ports"] += 1
        else:
            results["summary"]["hosts_down"] += 1

    return results


def _parse_host(host_elem: ET.Element) -> dict[str, Any]:
    """Parse a single host element."""
    host: dict[str, Any] = {
        "ip": None,
        "ipv4": None,
        "ipv6": None,
        "hostname": None,
        "status": "unknown",
        "os": None,
        "ports": [],
        "services": [],
        "scripts": [],
    }

    # Status
    status_elem = host_elem.find("status")
    if status_elem is not None:
        host["status"] = status_elem.attrib.get("state", "unknown")

    # Addresses
    for addr_elem in host_elem.findall("address"):
        addr_type = addr_elem.attrib.get("addrtype", "")
        addr = addr_elem.attrib.get("addr", "")
        if addr_type == "ipv4":
            host["ipv4"] = addr
            host["ip"] = addr
        elif addr_type == "ipv6":
            host["ipv6"] = addr
            if not host["ip"]:
                host["ip"] = addr
        elif addr_type == "mac":
            host["mac"] = addr

    # Hostnames
    hostnames_elem = host_elem.find("hostnames")
    if hostnames_elem is not None:
        for hostname_elem in hostnames_elem.findall("hostname"):
            host["hostname"] = hostname_elem.attrib.get("name", "")
            break

    # OS fingerprint
    os_elem = host_elem.find("os")
    if os_elem is not None:
        osmatch = os_elem.find("osmatch")
        if osmatch is not None:
            host["os"] = osmatch.attrib.get("name", "")

    # Ports
    ports_elem = host_elem.find("ports")
    if ports_elem is not None:
        for port_elem in ports_elem.findall("port"):
            port_data = _parse_port(port_elem)
            host["ports"].append(port_data)

    # Scripts
    for port_elem in ports_elem.findall("port") if ports_elem else []:
        for script_elem in port_elem.findall("script"):
            script_data = {
                "id": script_elem.attrib.get("id", ""),
                "output": script_elem.attrib.get("output", ""),
            }
            host["scripts"].append(script_data)

    return host


def _parse_port(port_elem: ET.Element) -> dict[str, Any]:
    """Parse a port element."""
    port_id = port_elem.attrib.get("portid", "")
    protocol = port_elem.attrib.get("protocol", "tcp")

    state_elem = port_elem.find("state")
    state = state_elem.attrib.get("state", "unknown") if state_elem else "unknown"

    service_elem = port_elem.find("service")
    service: dict[str, Any] = {}
    if service_elem is not None:
        service = {
            "name": service_elem.attrib.get("name", ""),
            "product": service_elem.attrib.get("product", ""),
            "version": service_elem.attrib.get("version", ""),
            "extrainfo": service_elem.attrib.get("extrainfo", ""),
            "ostype": service_elem.attrib.get("ostype", ""),
            "method": service_elem.attrib.get("method", ""),
            "conf": service_elem.attrib.get("conf", "10"),
        }

    return {
        "port": int(port_id),
        "protocol": protocol,
        "state": state,
        "service": service if service else None,
    }


def run_nmap_scan(
    target: str,
    ports: str = "1-1000",
    scan_type: str = "SYN",
    timing: int = 4,
    service_detection: bool = True,
    os_detection: bool = True,
    script_scan: bool = True,
    vuln_scripts: bool = False,
) -> dict[str, Any]:
    """Execute nmap and return parsed results."""
    cmd = build_nmap_command(
        target=target,
        ports=ports,
        scan_type=scan_type,
        timing=timing,
        service_detection=service_detection,
        os_detection=os_detection,
        script_scan=script_scan,
        vuln_scripts=vuln_scripts,
    )

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode != 0:
            return {
                "target": target,
                "error": f"Nmap exited with code {result.returncode}: {result.stderr}",
                "hosts": [],
            }

        return parse_nmap_xml(result.stdout, target)

    except subprocess.TimeoutExpired:
        return {
            "target": target,
            "error": "Nmap scan timed out after 300 seconds",
            "hosts": [],
        }
    except FileNotFoundError:
        return {
            "target": target,
            "error": "Nmap not found. Please install nmap.",
            "hosts": [],
        }
    except Exception as exc:
        return {
            "target": target,
            "error": str(exc),
            "hosts": [],
        }


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        params: dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError:
        params = {}

    target = params.get("target") or params.get("input") or ""
    if not target:
        print(json.dumps({"hosts": [], "error": "No target specified"}))
        return 0

    result = run_nmap_scan(
        target=target,
        ports=params.get("ports", "1-1000"),
        scan_type=params.get("scan_type", "SYN"),
        timing=int(params.get("timing", 4)),
        service_detection=bool(params.get("service_detection", True)),
        os_detection=bool(params.get("os_detection", True)),
        script_scan=bool(params.get("script_scan", True)),
        vuln_scripts=bool(params.get("vuln_scripts", False)),
    )

    print(json.dumps(result, indent=2))
    return 0


import sys

if __name__ == "__main__":
    sys.exit(main())