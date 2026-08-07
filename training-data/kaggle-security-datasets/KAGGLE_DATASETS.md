# Kaggle Datasets Batch — Manifest

Curated list of **20+ Kaggle cybersecurity / NLP / AI-security datasets** to expand the 3 datasets already ingested in commit `c23535c` (`training-data/kaggle-security-datasets/`).

## Already ingested (existing 3 — DO NOT re-download)

| # | Slug | Used as | Source rows |
|---|------|---------|-------------|
| 1 | `tannubarot/cybersecurity-attack-and-defence-dataset` | KB + SFT | 14,180 |
| 2 | `chuneeb/ai-agent-cybersecurity-dataset-2026` | KB + SFT | 147 + 21 aux CSVs |
| 3 | `hussainsheikh03/nlp-based-cyber-security-dataset` | KB | 1,100 |

## New batch (curated — 22 datasets)

> Format: `<slug>` — `<what it produces>` — `<theme>` — `<rough size>`

### A. Vulnerabilities & CVE / exploit data

1. **`sujaykapadnis/cybersecurity-cve-dataset`** — CVE records → KB docs (per-CWE category)
2. **`asad7an/cve-mitre-attack-mapping`** — CVE ↔ MITRE mapping → KB docs + SFT Q&A
3. **`aymane200/cve-vulnerabilities-dataset-2014-2024`** — 10y CVE history → KB timeline docs
4. **`ravikumarmn/cve-dataset-2002-2024`** — extended CVE dump → KB
5. **`manavyadav25/cve-vulnerability-records`** — alternate CVE source → KB
6. **`davidcampos/cve-database`** — CVE descriptions → KB docs

### B. Network intrusion & malware traffic

7. **`sampadab17/network-intrusion-detection`** — KDD-style features → KB + SFT (anomaly classification)
8. **`chethuhn/network-intrusion-detection`** — UNSW-NB15 → KB + SFT
9. **`mrwells/cicids2017`** — CICIDS2017 PCAP labels → KB + SFT
10. **`mnassrib/cicids2017`** — alternate CICIDS2017 source → KB
11. **`ahmedhamdy0/network-intrusion-dataset`** — additional IDS dataset → KB
12. **`rohitgupta24/network-malware-detection`** — malware traffic → KB
13. **`sgk1590/malware-detection`** — PE/malware features → KB + SFT
14. **`danielcompetition/cybersecurity-attacks`** — additional attack dataset → KB

### C. Phishing / URL / email security

15. **`shantanudhakadd/email-spam-dataset`** — phishing email features → KB + SFT
16. **`akashkr/phishing-url-detection`** — phishing URL features → KB + SFT
17. **`eswarchandt/phishing-website-detector`** — phishing website features → KB
18. **`naserabdullah079/phishing-email-detection`** — phishing email dataset → KB

### D. Threat intel / SIEM / logs

19. **`casperriboe/siem-data`** — synthetic SIEM logs → KB + SFT
20. **`mkalimer/loghub-windows-event-log`** — Windows event logs → KB docs
21. **`mvonsteinkirch/loghub-zeek-http-logs`** — Zeek HTTP logs → KB docs

### E. AI / LLM security

22. **`deepakcode21/llm-jailbreak-prompts`** — jailbreak corpus → KB + SFT (already partly in #2)
23. **`deepakcode21/prompt-injection-attacks`** — prompt injection patterns → KB + SFT
24. **`noahsiegel/prompt-injection-dataset`** — additional injection samples → KB

> All slugs above should be verified on kaggle.com before downloading (a slug may be renamed or deleted). Use `kagglehub.dataset_download("<slug>")` and inspect the resulting directory.

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
