# Kaggle Datasets Batch — Manifest

Curated list of **20+ Kaggle cybersecurity / NLP / AI-security datasets** to expand the 3 datasets already ingested in commit `c23535c` (`training-data/kaggle-security-datasets/`).

## Already ingested (existing 3 — DO NOT re-download)

| # | Slug | Used as | Source rows |
|---|------|---------|-------------|
| 1 | `tannubarot/cybersecurity-attack-and-defence-dataset` | KB + SFT | 14,180 |
| 2 | `chuneeb/ai-agent-cybersecurity-dataset-2026` | KB + SFT | 147 + 21 aux CSVs |
| 3 | `hussainsheikh03/nlp-based-cyber-security-dataset` | KB | 1,100 |

## New batch (curated + API-verified — 22 datasets)

> Every slug below was verified against `GET /api/v1/datasets/view/<slug>` (HTTP 200) on 2026-08-10.
> Format: `<slug>` — `<what it produces>` — `<theme>` — `<rough size>`

### A. Vulnerabilities & CVE / exploit data

1. **`krooz0/cve-and-cwe-mapping-dataset`** — CVE ↔ CWE mapping (2021) → KB docs + SFT Q&A — 32.6 MB
2. **`andrewkronser/cve-common-vulnerabilities-and-exposures`** — NIST CVE records → KB docs — 9.4 MB
3. **`um3rfar00q/2021-2025-all-cves-cleaned-dataset`** — NVD CVE (2004–2025) cleaned → KB + SFT — 47.4 MB
4. **`stanislavvinokur/cve-and-cwe-dataset-1999-2025`** — 26y CVE & CWE history → KB timeline docs — 22.9 MB
5. **`junaidmohammad9248/cisa-cve-vulnrichment`** — CISA CVE Vulnrichment → KB + SFT — 7.4 MB

### B. Network intrusion & malware traffic

6. **`dhoogla/unswnb15`** — UNSW-NB15 (AUNSW official) → KB + SFT — 12.3 MB
7. **`dhoogla/nslkdd`** — NSL-KDD → KB + SFT (anomaly classification) — 2.0 MB
8. **`dhoogla/cicddos2019`** — CIC-DDoS2019 → KB + SFT — 30.1 MB
9. **`sampadab17/network-intrusion-detection`** — network intrusion features → KB + SFT — 0.8 MB
10. **`arnobbhowmik/ton-iot-network-dataset`** — TON_IoT telemetry → KB docs — 1.8 MB

### C. Malware

11. **`subhajournal/malware-detection-from-memory-dump`** — memory dump features → KB + SFT — 4.0 MB
12. **`luccagodoy/obfuscated-malware-memory-2022-cic`** — CIC-MalMem-2022 → KB + SFT — 4.0 MB
13. **`amdj3dax/ransomware-detection-data-set`** — ransomware detection → KB + SFT — 2.2 MB

### D. Phishing / URL / email security

14. **`subhajournal/phishingemails`** — phishing email detection → KB + SFT — 18.9 MB
15. **`shashwatwork/web-page-phishing-detection-dataset`** — web page phishing features → KB — 1.1 MB
16. **`hasibur013/phishing-data`** — phishing URL detection → KB + SFT — 0.3 MB
17. **`eswarchandt/phishing-website-detector`** — phishing website features → KB — 0.2 MB

### E. Threat intel / SIEM / logs

18. **`rawaldelhi/secureops-security-incident-logs-dataset`** — security incident logs → KB + SFT — 0.1 MB
19. **`jacobvs/ddos-attack-network-logs`** — DDoS attack network logs → KB docs — 94.7 MB
20. **`solvedinfoam/2022-04-20-emotet-epoch4-zeek-logs`** — Zeek logs (Emotet) → KB docs — 0.1 MB

### F. AI / LLM security

21. **`awwdudee/llm-safety-dataset-for-chatbot-applications`** — LLM jailbreak + safety data → KB + SFT — 0.7 MB
22. **`krishnayadav456wrsty/prompt-injection-and-jailbreak-detection-dataset`** — prompt injection & jailbreak → KB + SFT — 1.8 MB
23. **`shreyashautomation/llm-jailbreak-prompt-dataset`** — LLM jailbreak prompt corpus → KB + SFT — 7.4 MB
24. **`cyberprince/prompt-injection-and-benign-prompt-dataset`** — prompt injection vs benign → KB + SFT — 0.1 MB

---

## Expected totals (rough estimate)

| Theme | New KB docs | New SFT rows |
|-------|-------------|--------------|
| A. CVE / exploit | 200–600 | 5,000–15,000 |
| B. Intrusion / malware | 50–150 | 30,000–80,000 |
| C. Phishing | 20–80 | 3,000–10,000 |
| D. Threat intel / SIEM | 30–100 | 1,000–5,000 |
| E. AI / LLM security | 30–100 | 1,000–3,000 |
| **Total** | **~330–1,030 docs** | **~40,000–110,000 SFT rows** |

Combined with the existing **85 KB docs** and **14,280 SFT rows**, this batch should push the KB toward ~3,700–4,400 sources and the SFT corpus toward ~55,000–125,000 rows — well within the GPU/CPU budget for FAISS rebuild (~5–15 min) and SFT tokenization (~30s).

## How to use this list

See `download.sh` (one-command downloader) and `build.py` (per-dataset converter).
Run order: `download.sh` → `build.py` → `re-ingest KB` → `rebuild FAISS` → `commit`.
