<div align="center">

# Cybersecurity Knowledge Base

**Notes · Labs · Projects · Research**

Built across TryHackMe, Hack The Box, TCM Security, zSecurity, and independent lab work.
Covers the full spectrum from blue team operations to red team exploitation to GRC consulting.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-kayShahbaaz-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kayShahbaaz)
[![GitHub](https://img.shields.io/badge/GitHub-kayShahbaaz-181717?style=flat&logo=github)](https://github.com/kayShahbaaz)
[![Alias](https://img.shields.io/badge/Alias-kayn0x-00bfff?style=flat)](#)
[![Repos](https://img.shields.io/badge/34%20Repositories-555?style=flat)](#)

</div>

---

## What's Here

| # | Domain | Repos |
|---|---|---|
| 1 | [Foundations](#1-foundations) | 3 repos — networking, OS, web basics |
| 2 | [SOC & Blue Team](#2-soc--blue-team) | 4 repos — notes + 3 live SOC projects |
| 3 | [OSINT & Password Cracking](#3-osint--password-cracking) | 1 repo — recon tools, hash cracking |
| 4 | [Penetration Testing](#4-penetration-testing) | 8 repos — notes + 2 live pentest projects |
| 5 | [Web Hacking & Bug Bounty](#5-web-hacking--bug-bounty) | 8 repos — web vulns + 2 live web pentest projects |
| 6 | [GRC — Governance, Risk & Compliance](#6-grc--governance-risk--compliance) | 8 repos — study notes + 6 live GRC projects |

---

## 1. Foundations

The starting point — networking, operating systems, Linux, Windows, and web infrastructure. Everything else in this repo builds on these.

| Repository | What's covered |
|---|---|
| [thm-Pre-Security](https://github.com/kayShahbaaz/thm-Pre-Security) | OSI model, TCP/IP, subnetting, DNS, DHCP, Linux terminal, Windows internals, HTTP/HTTPS |
| [thm-Cyber-Security101](https://github.com/kayShahbaaz/thm-Cyber-Security101) | Offensive + defensive security, Active Directory, PowerShell, Wireshark, Nmap, Metasploit intro, cryptography, SIEM basics |
| [thm-WebFundamentals](https://github.com/kayShahbaaz/thm-WebFundamentals) | HTTP lifecycle, DNS resolution, cookies, sessions, web servers, Burp Suite intro |

---

## 2. SOC & Blue Team

Four repos — one study path and three hands-on lab projects that are **intentionally interconnected**: `packet-capture-analyser` and `log-monitor-dashboard` both feed data upstream into `splunk-siem`, simulating a real SOC pipeline end-to-end on Kali Linux.

| Repository | What's covered |
|---|---|
| [thm-SOCL1](https://github.com/kayShahbaaz/thm-SOCL1) | Alert triage, DFIR, SIEM correlation rules, threat intelligence, MITRE ATT&CK mapping |
| [log-monitor-dashboard](https://github.com/kayShahbaaz/log-monitor-dashboard) | Real-time `auth.log` parser (Bash + Python), brute-force detection, privilege escalation tracking, live browser SOC dashboard, Splunk ingestion config |
| [packet-capture-analyser](https://github.com/kayShahbaaz/packet-capture-analyser) | Live capture with `tcpdump`, protocol dissection with `tshark` + Wireshark, SYN flood and port scan detection, FTP cleartext credential exposure, CSV export to Splunk |
| [splunk-siem](https://github.com/kayShahbaaz/splunk-siem) | Splunk Free on Kali — SPL detection queries, cross-project threat correlation, saved alert rules, full SOC dashboard with timelines and event graphs |

---

## 3. OSINT & Password Cracking

| Repository | What's covered |
|---|---|
| [OSINT-and-Password-Cracking](https://github.com/kayShahbaaz/OSINT-and-Password-Cracking) | Maltego, Shodan, theHarvester, Recon-ng, WHOIS, sock puppet persona lab, Hashcat (wordlist / rule / mask / hybrid attacks), John the Ripper, rockyou.txt, legal practice platforms |

---

## 4. Penetration Testing

Study notes covering the full offensive security methodology — from networking basics through Active Directory compromise — followed by two black-box penetration testing projects conducted in isolated lab environments with formal reports.

### Study Notes

| Repository | What's covered |
|---|---|
| [thm-jrPenTester](https://github.com/kayShahbaaz/thm-jrPenTester) | Pentest methodology, Nmap, Metasploit, web vulns, Linux + Windows privilege escalation, post-exploitation |
| [htb-pentest-in-a-nutshell](https://github.com/kayShahbaaz/htb-pentest-in-a-nutshell) | Full engagement lifecycle — pre-engagement, scoping, legal auth, info gathering, assessment, professional reporting |
| [tcm-PEH-practical-ethical-hacking](https://github.com/kayShahbaaz/tcm-PEH-practical-ethical-hacking) | Networking, Linux, Bash scripting, Active Directory attacks (Kerberoasting, Pass-the-Hash, Golden Ticket), exploit development, capstone machine walkthroughs |
| [thm-wifi-hacking101](https://github.com/kayShahbaaz/thm-wifi-hacking101) | WPA/WPA2 internals, 4-way handshake capture, `aircrack-ng` suite, Hashcat modes 2500 and 22000 |
| [thm-android-hacking101](https://github.com/kayShahbaaz/thm-android-hacking101) | APK structure, DEX/Smali, `jadx`, `apktool`, `dex2jar`, static analysis — hardcoded secrets, weak crypto, exported components, Firebase misconfigs |
| [zSecurity-ethical-hacking-from-scratch](https://github.com/kayShahbaaz/zSecurity-ethical-hacking-from-scratch) | Recon, scanning, network sniffing, MITM attacks, exploitation, post-exploitation, covering tracks |
| [zSecurity-cloud-based-hacking](https://github.com/kayShahbaaz/zSecurity-cloud-based-hacking) | Cloud attack infrastructure, phishing campaigns, 2FA bypass, C2 framework setup, browser exploitation, trojan delivery and evasion |

### Projects

> Full black-box engagements in isolated lab environments. Each follows a real pentest structure and includes a formal PDF report.

**[ghost-in-the-network](https://github.com/kayShahbaaz/ghost-in-the-network) — Network Penetration Test**
Target: Metasploitable2. Zero prior knowledge → full root compromise via host discovery, Nmap enumeration, SMB analysis, CVE research, and exploitation. Formal report in `/report/`.

**[broken-trust](https://github.com/kayShahbaaz/broken-trust) — Active Directory Penetration Test**
Target: Windows Server 2019 domain `corp.local`. No CVEs used — entire chain via AD misconfigurations and Kerberos weaknesses only: enumeration → Kerberoasting → AS-REP Roasting → credential dumping → Pass-the-Hash → Domain Admin. Formal report in `/report/`.

---

## 5. Web Hacking & Bug Bounty

Study notes covering the full web application attack surface — from HTTP fundamentals through HTTP request smuggling — followed by two web application penetration testing projects with formal reports.

### Study Notes

| Repository | What's covered |
|---|---|
| [thm-webapp-pentesting](https://github.com/kayShahbaaz/thm-webapp-pentesting) | Auth attacks, SQLi, XSS, IDOR, SSRF, XXE, LFI/RFI, path traversal, HTTP request smuggling — full TryHackMe web path |
| [zSecurity-web-hacking](https://github.com/kayShahbaaz/zSecurity-web-hacking) | File upload bypass, LFI/RFI, SQLi, XSS, CSRF, brute force with Hydra + Burp Intruder, Nikto, OWASP ZAP |
| [ranakhalil-webhacking](https://github.com/kayShahbaaz/ranakhalil-webhacking) | 30-day structured roadmap — Rana Khalil playlists, PortSwigger Web Security Academy labs mapped to each vuln class, HTB challenges |
| [zSecurity-social-engineering](https://github.com/kayShahbaaz/zSecurity-social-engineering) | OSINT profiling, Windows/macOS/Linux malware creation, phishing, USB drops, delivery methods, post-exploitation, defences |
| [zSecurity-dark-web-anonymity-privacy](https://github.com/kayShahbaaz/zSecurity-dark-web-anonymity-privacy) | TOR internals, TAILS OS, dark net navigation, PGP encryption, Signal/ProtonMail, file encryption, Qubes OS, cryptocurrency anonymization |
| [zSecurity-bug-bounty-hunting](https://github.com/kayShahbaaz/zSecurity-bug-bounty-hunting) | IDOR, CSRF, path traversal, OAuth 2.0 flaws, OS command injection, XSS (all variants + CSP bypass), SQLi, SSRF, XXE, live hunting methodology, professional report writing |
| [htb-bug-bounty-hunting](https://github.com/kayShahbaaz/htb-bug-bounty-hunting) | Web app architecture, HTTP/HTTPS internals, REST APIs, CRUD, OWASP vuln categories, responsible disclosure, bug bounty program rules |

### Projects

> Full black-box web application engagements in isolated lab environments. Each includes a formal PDF report.

**[insider-threat](https://github.com/kayShahbaaz/insider-threat) — Web Application Penetration Test**
Target: DVWA modelling a corporate HR app with internal attacker access. Five vulnerabilities exploited — SQLi (full DB dump + all credentials), command injection (OS-level RCE), LFI, brute force, stored/reflected XSS. Full admin access achieved. Formal report in `/report/`.

**[invisible-shadow](https://github.com/kayShahbaaz/invisible-shadow) — XSS, Session Hijacking & Credential Interception**
Complete multi-stage attack chain: XSS discovery → cookie security analysis (HttpOnly/Secure/SameSite) → session token theft → session hijack → full account takeover. No password cracking at any stage. Formal report in `/report/`.

---

## 6. GRC — Governance, Risk & Compliance

Study notes and a growing portfolio of live GRC projects spanning professional advisory work, compliance tooling, IAM auditing, Islamic fintech governance, and AI governance — covering Indian, Saudi Arabian, and Gulf regulatory frameworks.

### Study Notes

| Repository | What's covered |
|---|---|
| [grc-notes](https://github.com/kayShahbaaz/grc-notes) | GRC Analyst fundamentals — governance structures, risk registers, compliance mapping, ISO 27001, NIST CSF, NIST SP 800-53, ISO 31000, COBIT, GDPR, HIPAA, PCI-DSS, SOX, security policy development |
| [thm-governance-and-regulation](https://github.com/kayShahbaaz/thm-governance-and-regulation) | GDPR (data subject rights, breach notification), PCI-DSS (12 requirements, SAQ types), HIPAA (PHI, safeguard categories), ISO 27001 (ISMS, Annex A), NIST CSF (identify/protect/detect/respond/recover) |

### Projects

---

**[resolute-compliance-advisory](https://github.com/kayShahbaaz/resolute-compliance-advisory) — GRC Advisory Portfolio**
Four client engagements across two years at a boutique GRC advisory firm, demonstrating full role progression from GRC Analyst to GRC Auditor. Frameworks: ISO 27001:2022, SOC 2, GDPR, India DPDP Act 2023, NCA ECC-1:2018, NCA ECC-2:2024, SAMA CSF, Saudi PDPL.

First engagement snapshot — Brightpath (IT Services, Bengaluru): ISO 27001 gap assessment returned 37.6% conformance (35/93 controls); SOC 2 Security Partially Ready; live critical risk flagged — former employee credentials still active. Deliverables: engagement letter, gap reports, Statement of Applicability (93 controls), risk register (27 risks, 9 domains), remediation roadmap (34 actions, Gantt, dashboard), executive summary. All client names anonymised.

---

**[pdpl-pii-scanner](https://github.com/kayShahbaaz/pdpl-pii-scanner) — Saudi PDPL Compliance Tool**
Python tool that scans CSV and Excel files for Saudi PII, classifies every finding into PDPL's actual legal tiers, risk-scores each one, checks for governance gaps, and produces redacted file copies. Output: bilingual EN/AR interactive HTML dashboard + CSV/console reports.

Detects 8 PII types. Classifies into three PDPL tiers: Personal Data, Credit Data (PDPL Article 24), and Sensitive Data (PDPL Article 1(11)) — each carrying different consent and DPIA obligations. Confidence scoring is layered (High/Medium/Low), not a flat yes/no. Flags missing consent tracking and cross-border transfer signals. Built on PDPL Article 1 defined terms and SDAIA public guidance.
[Live demo](https://kayshahbaaz.github.io/pdpl-pii-scanner/)

---

**[iam-risk-assurance](https://github.com/kayShahbaaz/iam-risk-assurance) — IAM Audit Engagement**
SQL-based IAM audit for Najm Financial Services Co. (~400 staff, Riyadh) — a SAMA-regulated firm subject to NCA ECC mandatory controls. July–November 2025. Seven checks across the full IAM lifecycle, 203 findings, all mapped to ISO 27001 Annex A.9 / SAMA CSF / NCA ECC. Audit database and all detection queries built from scratch. Bilingual EN/AR interactive dashboard with RTL toggle. Formal report delivered in both languages.
[Live dashboard](https://kayshahbaaz.github.io/iam-risk-assurance/)

---

**[al-mizan](https://github.com/kayShahbaaz/al-mizan) — Shariah & Regulatory GRC Framework for Islamic Fintech**
Most fintech and Islamic finance organisations run two disconnected compliance reviews — one for government regulation, one for Shariah board approval. Al-Mizan runs both in a single unified workflow. Built for the Saudi market under Vision 2030.

Three modules: (1) Governance maturity self-assessment scored against both regulatory and Shariah dimensions; (2) Gharar Risk Matrix — product-by-product uncertainty scoring per AAOIFI Standard No. 31 with a product category selector and mitigation guidance; (3) Dual-aspect audit checklist covering SAMA/CMA and Shariah board requirements simultaneously. Frameworks: SAMA CSF, CMA, Saudi PDPL, AAOIFI Shariah Standards. Fully interactive bilingual EN/AR dashboard with RTL switching. Runs entirely in the browser.

---

**[aigrc-imf](https://github.com/kayShahbaaz/aigrc-imf) — AI Governance Compliance Checker**
Research and tooling addressing a documented governance gap: organisations across regulated Gulf industries are deploying AI in GRC functions — fraud detection, compliance monitoring, risk scoring — faster than the governance architectures meant to control them.

Contains two things: (1) an academic paper proposing the AI-GRC Integrated Management Framework (AI-GRC IMF) — a five-phase lifecycle governance model grounded in ISO/IEC 27001:2022 and ISO/IEC 42001:2023, cross-referenced against Saudi PDPL, SDAIA AI Ethics Principles, NCA ECC-1:2018, SAMA CSF, and the EU AI Act; (2) an interactive compliance checker that lets organisations self-assess against the AI-GRC IMF and receive an AI-generated remediation report mapped to Saudi regulatory obligations. Open `index.html` — no installation, no server.

---

**[aigrc-audit-suite](https://github.com/kayShahbaaz/aigrc-audit-suite) — AI GRC Audit Suite**
Work in progress. Details will be added on completion.

---

## Platforms & and offcial link

| Prefix | Platform |
|---|---|
| `thm-` | [TryHackMe](https://tryhackme.com) |
| `htb-` | [Hack The Box Academy](https://academy.hackthebox.com) |
| `tcm-` | [TCM Security](https://tcm-sec.com) |
| `zSecurity-` | [zSecurity](https://zsecurity.org) |

---

<div align="center">

Actively maintained — connect on [GitHub](https://github.com/kayShahbaaz)

</div>
