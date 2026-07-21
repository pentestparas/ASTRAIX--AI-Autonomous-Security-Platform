# Rules Directory

This directory contains operational rules for the AstraIX Security Analyst platform.

## Rule Types

### Detection Rules
Detection rules define patterns used by security plugins to identify vulnerabilities.

### Compliance Rules
Compliance rules map findings to frameworks (SOC 2, ISO 27001, NIST, CIS).

### Response Rules
Response rules define automated actions for findings (alert, ticket, auto-remediate).

### Architecture Rules
Architecture rules describe architectural patterns (plugin contracts, plugin manifests).

## Rule Format

```yaml
# rule.yml

id: SEC-001
name: Public SSH Port
description: |
  Alert when SSH is exposed on port 22 to public networks.

severity: high

scope:
  - asset.type == "ipv4"

conditions:
  - port == 22
  - state == "open"
  - scope in ["public", "0.0.0.0/0"]

remediation:
  description: |
    Restrict access via SecurityGroup or firewall rules.
  steps:
    - Block 22/tcp on public-facing firewalls
    - Move SSH to non-standard port or use bastion

references:
  - https://owasp.org/...
```

## Adding a New Rule

1. Create a new YAML file in `rules/`
2. Follow the rule format above
3. Add tests in `tests/rules/`
4. Document the rule's purpose