# AstraIX Knowledge Base — Source URLs

Canonical track of every external source used in the knowledge base. Updated 2026-08-04.
All content was cloned/fetched from these URLs. Internal file contents are NOT part of the graph corpus — these URLs are the audit trail.

## Cloned GitHub Repositories

| Repo | URL | Used for |
|------|-----|----------|
| Anthropic Cybersecurity Skills | `https://github.com/mukul975/Anthropic-Cybersecurity-Skills` | AI + security skills, 2288 md files |
| awesome-soc | `https://github.com/cyb3rxp/awesome-soc` | SOC/blue team, SIEM, DFIR |
| CAI (Cybersecurity AI) | `https://github.com/aliasrobotics/CAI` | Cybersecurity AI research |
| cybersecurity-knowledge-base | `https://github.com/kayShahbaaz/cybersecurity-knowledge-base` | Vulnerability guides |
| Cybersecurity-Resources | `https://github.com/Striving-to-learn/Cybersecurity-Resources` | Learning paths |
| paulveillard/cybersecurity | `https://github.com/paulveillard/cybersecurity` | Curated security guides |
| Berkanktk/CyberSecurity | `https://github.com/Berkanktk/CyberSecurity` | CTF guides, tools, techniques |

## Crawled Websites

| Site | URL(s) | Used for |
|------|--------|----------|
| PortSwigger Web Security Academy | `https://portswigger.net/web-security` (via `https://portswigger.net/sitemap.xml`, ~418 `/web-security/` URLs) | 132 topic/sub-topic teaching pages (labs excluded) |
| OWASP | `https://owasp.org/projects/`, `https://owasp.org/www-project-top-ten/`, `https://owasp.org/www-project-web-security-testing-guide/`, `https://owasp.org/www-project-api-security/` | OWASP Top 10, WSTG, API Security Top 10 |

## Docker/KB Architecture

- KB baked into backend image at `/opt/astraix-kb` (via `COPY knowledge-base` in `docker/Dockerfile.backend`)
- Seeded on first boot by `docker/entrypoint.sh` into named volume `kb-data` mounted at `/app/knowledge-base`
- Seed condition: `/app/knowledge-base/embeddings/chunks.json` missing → reseed
- HTTP access: `GET /api/v1/knowledge/search?q=...`, `/knowledge/stats`, `/knowledge/sources`, `/knowledge/source?path=sources/...`
- Index: FAISS, 7008 chunks, dim 384, vocab 92455 (build with `parallel=None` — `parallel=0` spawns all cores → OOM)

## Known Content Stats (2026-08-04)

- 3542 files on disk in volume, 3177 indexed sources, 7008 chunks, 92455 vocab
- 15 source directories under `knowledge-base/sources/` (+ PortSwigger_Web_Security_Academy 133 md, OWASP_Projects 5 md)
