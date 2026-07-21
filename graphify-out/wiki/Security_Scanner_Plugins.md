# Security Scanner Plugins

> 25 nodes · cohesion 0.14

## Key Concepts

- **Finding Engine** (6 connections) — `backend/ai_secos_core/workflows/asset_discovery/asset_discovery.yml`
- **Report Engine** (6 connections) — `backend/ai_secos_core/workflows/asset_discovery/asset_discovery.yml`
- **Network VAPT Workflow** (6 connections) — `backend/ai_secos_core/workflows/network_vapt/network_vapt.yml`
- **Web Application VAPT Workflow** (6 connections) — `backend/ai_secos_core/workflows/web_vapt/web_vapt.yml`
- **network/recon capability** (5 connections) — `backend/ai_secos_core/plugins/nmap/plugin.yml`
- **network/vuln-scan capability** (5 connections) — `backend/ai_secos_core/plugins/nmap/plugin.yml`
- **Nuclei Vulnerability Scanner Plugin** (5 connections) — `backend/ai_secos_core/plugins/nuclei/plugin.yml`
- **External Asset Discovery Workflow** (5 connections) — `backend/ai_secos_core/workflows/asset_discovery/asset_discovery.yml`
- **HTTP Probe (httpx) Plugin** (4 connections) — `backend/ai_secos_core/plugins/httpx/plugin.yml`
- **Trivy Security Scanner Plugin** (4 connections) — `backend/ai_secos_core/plugins/trivy/plugin.yml`
- **Web Discovery Workflow** (4 connections) — `backend/ai_secos_core/workflows/discovery/discovery.yml`
- **web/discovery capability** (3 connections) — `backend/ai_secos_core/plugins/httpx/plugin.yml`
- **Nmap Port Scanner Plugin** (3 connections) — `backend/ai_secos_core/plugins/nmap/plugin.yml`
- **Semgrep SAST Scanner Plugin** (3 connections) — `backend/ai_secos_core/plugins/semgrep/plugin.yml`
- **Subfinder Subdomain Enumeration Plugin** (3 connections) — `backend/ai_secos_core/plugins/subfinder/plugin.yml`
- **Cloud Posture Assessment Workflow** (3 connections) — `backend/ai_secos_core/workflows/cloud_posture/cloud_posture.yml`
- **Code Security Audit Workflow** (3 connections) — `backend/ai_secos_core/workflows/code_audit/code_audit.yml`
- **web/vuln-scan capability** (2 connections) — `backend/ai_secos_core/plugins/nuclei/plugin.yml`
- **osint/asset-discovery capability** (2 connections) — `backend/ai_secos_core/plugins/subfinder/plugin.yml`
- **api/security capability** (1 connections) — `backend/ai_secos_core/plugins/nuclei/plugin.yml`
- **code/audit capability** (1 connections) — `backend/ai_secos_core/plugins/semgrep/plugin.yml`
- **sast/security capability** (1 connections) — `backend/ai_secos_core/plugins/semgrep/plugin.yml`
- **cloud/posture capability** (1 connections) — `backend/ai_secos_core/plugins/trivy/plugin.yml`
- **container/security capability** (1 connections) — `backend/ai_secos_core/plugins/trivy/plugin.yml`
- **iac/security capability** (1 connections) — `backend/ai_secos_core/plugins/trivy/plugin.yml`

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend/ai_secos_core/plugins/httpx/plugin.yml`
- `backend/ai_secos_core/plugins/nmap/plugin.yml`
- `backend/ai_secos_core/plugins/nuclei/plugin.yml`
- `backend/ai_secos_core/plugins/semgrep/plugin.yml`
- `backend/ai_secos_core/plugins/subfinder/plugin.yml`
- `backend/ai_secos_core/plugins/trivy/plugin.yml`
- `backend/ai_secos_core/workflows/asset_discovery/asset_discovery.yml`
- `backend/ai_secos_core/workflows/cloud_posture/cloud_posture.yml`
- `backend/ai_secos_core/workflows/code_audit/code_audit.yml`
- `backend/ai_secos_core/workflows/discovery/discovery.yml`
- `backend/ai_secos_core/workflows/network_vapt/network_vapt.yml`
- `backend/ai_secos_core/workflows/web_vapt/web_vapt.yml`

## Audit Trail

- EXTRACTED: 80 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*