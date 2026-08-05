# Cryptography Attacks Attacks

## Password Brute Force on Web Login Forms

- **Attack Type**: Credential Stuffing / Brute Force via Login Form
- **Target**: Web Applications
- **Vulnerability**: Weak login rate-limiting, no CAPTCHA, guessable credentials
- **MITRE**: T1110 – Brute Force
- **Impact**: Unauthorized access, data theft, account takeover
- **Tools**: Burp Suite, Hydra, cURL, Python (requests), Crunch, SecLists
- **Scenario**: A malicious actor attempts to gain unauthorized access to user accounts by systematically guessing passwords on a login form using either dictionary or pure brute force attack methods. This is done via automation or scripts.
- **Attack Steps**: Step 1: Open your browser and visit the target website (e.g., http://victim.com/login) that contains a login form with two fields: username and password. Make sure it is your own test environment or legal penetration testing target. Step 2: Right-click the login page and click “Inspect” or open DevTools (F12) to identify the name attributes of the form fields. Typically, they will look like name="username" and name="password". Also note the login request method (POST/GET) and URL endpoint. Step 3: Open Burp Suite and set your browser proxy to route through Burp (e.g., 127.0.0.1:8080). Step 4: Try logging in with any random credentials (like admin / 123456) to capture the request in Burp Suite. Step 5: Go to Burp → HTTP History → Find the POST login request. Right-click and send it to “Intruder.” Step 6: In Intruder, set the attack positions by highlighting the password field and clicking "Add §". You can fix the username if you’re targeting a known user. Step 7: Load a password list (use rockyou.txt or SecLists → Passwords → Common-Credentials). Step 8: Start the attack. Burp will attempt each password against the fixed username. Look for anomalies in response length, status code, or error message. For example, if every wrong password returns 401 and one returns 200 or "Welcome," you’ve found a valid credential. Step 9: Alternatively, use hydra: hydra -l admin -P /usr/share/wordlists/rockyou.txt http-post-form "/login:username=^USER^&password=^PASS^:F=Incorrect" (Replace with your target details). Step 10: Once valid credentials are discovered, attacker logs in successfully, potentially escalating further. Step 11: Ethical hackers stop here and report it. Black hat attackers may now steal data or pivot further. Step 12: Defenders should monitor for too many failed logins in a short time to detect such activity.
- **Detection**: Monitor login attempts per IP/user; detect excessive login failures
- **Solution**: Enforce rate-limiting; CAPTCHA; multi-factor auth; use strong passwords; lockout after N attempts
- **Tags**: Brute Force, Login Form, Credential Stuffing

## Dictionary Attack on Login Forms

- **Attack Type**: Online Password Guessing
- **Target**: Web Applications
- **Vulnerability**: Weak password policy, no login rate-limiting
- **MITRE**: T1110.001 – Password Guessing
- **Impact**: Account takeover, unauthorized access
- **Tools**: Burp Suite, Hydra, SecLists, Python (requests)
- **Scenario**: The attacker uses a list of commonly used passwords (a dictionary) and systematically tries each one against a known username on a login form. Unlike brute force, this is limited to realistic password guesses rather than every possible combination.
- **Attack Steps**: Step 1: Set up your own legal testing target or a deliberately vulnerable app like DVWA (Damn Vulnerable Web Application). Step 2: Identify the login form and its POST method, endpoint, and input fields using browser DevTools or Burp Suite. Step 3: Capture a login request in Burp Proxy by submitting dummy credentials. Step 4: Send this request to Burp Intruder. Set the attack position on the password field using § markers. Step 5: Fix the username (e.g., admin) and load a wordlist from SecLists or rockyou.txt. Step 6: Start the attack. Burp will send one login attempt for each password in the list. Step 7: Observe HTTP response length or message changes. A longer response or “Welcome” message indicates a successful login. Step 8: Alternatively, use Hydra: hydra -l admin -P rockyou.txt http-post-form "/login:username=^USER^&password=^PASS^:F=Incorrect" (adjust as needed). Step 9: If successful, the attacker gains access using a weak, guessable password. Step 10: This technique works because users reuse weak passwords.
- **Detection**: Monitor failed login attempts; detect excessive login failures per IP/user
- **Solution**: Enforce strong passwords, use rate-limiting, CAPTCHA, and account lockout after N failures
- **Tags**: Dictionary Attack, Login Forms, Weak Passwords

## Hash Brute Forcing (Offline Cracking)

- **Attack Type**: Offline Hash Cracking Using Brute Force
- **Target**: Database Dumps, Hash Files
- **Vulnerability**: Weak or unsalted password hashes
- **MITRE**: T1110.002 – Password Cracking
- **Impact**: Password exposure, credential reuse on other systems
- **Tools**: Hashcat, John the Ripper, rockyou.txt, Hash-Identifier
- **Scenario**: Attackers obtain leaked or dumped password hashes from a breached database and try to crack them offline using brute force techniques to recover the original plaintext password. This attack doesn't interact with the application directly.
- **Attack Steps**: Step 1: Assume you’ve legally obtained a hash dump from a penetration test, CTF challenge, or test environment. Example: admin:$6$abc123$yq3HwA...... Step 2: Identify the hash type using tools like Hash-Identifier or online sites. Step 3: Install hashcat or john on your system. Example hash: SHA256, bcrypt, MD5, etc. Step 4: Use a wordlist (like rockyou.txt) for a dictionary attack or let the tool try all combinations for brute force. Step 5: Run the cracking tool. For example, with John: john --wordlist=rockyou.txt hashes.txt or with hashcat: hashcat -m 0 -a 0 hashes.txt rockyou.txt. Step 6: The tool tries each password (hashed) and compares it with the dumped hash until a match is found. Step 7: Once a match is found, the password is revealed. Step 8: This process can be slow or fast depending on the hash algorithm and system GPU/CPU power. Step 9: After cracking, the attacker can now use the real password to access user accounts on other platforms if reused.
- **Detection**: Monitor for leaked hashes on forums; analyze hash storage technique; enable canary token traps
- **Solution**: Salted and hashed passwords using bcrypt/scrypt/argon2; avoid storing weak or unhashed passwords
- **Tags**: Offline Cracking, Hashcat, Dictionary, Hash Attack

## SSH Brute Force Attack

- **Attack Type**: Network Protocol Brute Force (Remote Shell Access)
- **Target**: Linux/Unix Servers
- **Vulnerability**: Exposed SSH with weak credentials
- **MITRE**: T1110.003 – SSH Brute Force
- **Impact**: Full system access, server takeover
- **Tools**: Hydra, Ncrack, Medusa, OpenSSH, SecLists
- **Scenario**: Attackers try many username and password combinations to gain unauthorized SSH access to a server, using brute force over port 22. Often done against internet-exposed servers with default or weak credentials.
- **Attack Steps**: Step 1: Identify the target IP address or domain name running an SSH server (e.g., using Nmap: nmap -p 22 -sV target.com). Ensure you’re testing your own machine or have authorization. Step 2: Choose a username (root, admin, or known users). Step 3: Get a wordlist like rockyou.txt or /usr/share/wordlists/nmap.lst. Step 4: Run Hydra: hydra -l root -P rockyou.txt ssh://target.com to start the brute force. Alternatively use Medusa: medusa -h target.com -u root -P rockyou.txt -M ssh. Step 5: These tools will try logging in via SSH using every password in the list for the given user. Step 6: If successful, the tool will display the correct password and user combo (e.g., root:toor123). Step 7: The attacker can now log in via ssh root@target.com and gain remote terminal access. Step 8: From here, attackers may escalate privileges, pivot internally, or exfiltrate data. Step 9: Defenders should detect brute force attempts by monitoring /var/log/auth.log or fail2ban logs.
- **Detection**: Monitor /var/log/auth.log, enable Fail2Ban, alert on excessive login failures from same IP
- **Solution**: Disable root login, enforce key-based auth, rate-limit SSH, block repeated IPs via Fail2Ban
- **Tags**: SSH, Brute Force, Remote Access, Port 22

## HTTP Basic Auth Brute Force

- **Attack Type**: HTTP Authentication Brute Forcing
- **Target**: Web Services (Basic Auth)
- **Vulnerability**: No rate limiting, no MFA, guessable credentials
- **MITRE**: T1110.001 – Password Guessing
- **Impact**: Unauthorized access to internal systems
- **Tools**: Hydra, curl, Burp Suite, Python (requests), Nmap NSE
- **Scenario**: HTTP Basic Authentication prompts for a username/password in the browser. Attackers can brute-force this using automated tools by sending Base64-encoded credentials to the endpoint repeatedly until valid credentials are found.
- **Attack Steps**: Step 1: Identify a URL that uses HTTP Basic Authentication (e.g., http://target.com/protected). You’ll typically see a popup from the browser asking for a username and password. Step 2: Use curl to manually test: curl -u admin:admin http://target.com/protected. Step 3: To automate, use Hydra: hydra -L usernames.txt -P passwords.txt target.com http-get /protected (adjust the endpoint). Step 4: Hydra will send Base64-encoded Authorization: Basic <base64(username:password)> headers repeatedly. Step 5: Look for success responses (e.g., HTTP 200 or different page content). Step 6: If credentials are found, log in with the discovered pair to gain access. Step 7: Defenders can detect brute force by monitoring repeated failed login attempts via logs. Step 8: This attack is effective if no rate-limiting or IP blocking is enforced.
- **Detection**: Monitor access logs for repeated Base64 login attempts; alert on brute-force behavior
- **Solution**: Use digest or token-based auth, add rate-limiting, implement 2FA
- **Tags**: Basic Auth, HTTP Brute Force, Base64

## API Key or Token Brute Force

- **Attack Type**: API Token / Key Guessing
- **Target**: Public or Private APIs
- **Vulnerability**: Predictable or static API tokens
- **MITRE**: T1110.004 – Brute Force Token Guessing
- **Impact**: Unauthorized API access, data exposure
- **Tools**: Burp Suite, curl, Postman, Python, SecLists
- **Scenario**: APIs using static tokens (e.g., ?api_key=XYZ) or bearer tokens in headers can be brute-forced if poorly designed. Attackers attempt many keys to guess a valid one and access protected endpoints.
- **Attack Steps**: Step 1: Identify an API endpoint that uses an API key or token, such as GET /api/data?api_key=XYZ or Authorization: Bearer <token>. Step 2: Try accessing the endpoint with an invalid key to observe the error (e.g., 401 Unauthorized). Step 3: Prepare a wordlist or generate tokens using a pattern if the key is predictable (e.g., APIKEY_001, APIKEY_002, etc.). Step 4: Use a script in Python with requests or Postman’s runner to automate key submission. Loop through your wordlist and send the request. Step 5: Observe the responses. A different HTTP code (e.g., 200 OK or a longer response body) indicates a valid key. Step 6: If successful, attacker now has access to private data or functionality without being authenticated. Step 7: Monitor logs for token trial patterns or repeated token failures. Step 8: APIs are often vulnerable if keys don’t expire or if the token pattern is guessable.
- **Detection**: Monitor failed token use per IP/user-agent; log unusual key lengths or formats
- **Solution**: Use rate-limiting, expire keys, use longer random tokens, monitor access per key
- **Tags**: API Brute Force, Token Abuse, API Security

## CAPTCHA Bypass via Brute Force

- **Attack Type**: CAPTCHA Weakness Exploitation via Automation
- **Target**: Web Apps with CAPTCHA
- **Vulnerability**: Weak or broken CAPTCHA logic
- **MITRE**: T1208 – CAPTCHA Bypass
- **Impact**: Enables further brute force or spam attacks
- **Tools**: Tesseract OCR, Burp Suite, Selenium, Python, curl
- **Scenario**: Attackers attempt to bypass CAPTCHAs by automating form submissions, using OCR, guessing static challenges, or exploiting logic flaws to continue brute force attacks even when CAPTCHA is present.
- **Attack Steps**: Step 1: Identify a CAPTCHA-protected login or form (e.g., login, comment post, registration). Step 2: Test if CAPTCHA is actually enforced on the backend. Submit a form with a wrong CAPTCHA via a browser and see if it rejects it. Step 3: If CAPTCHA is image-based (like distorted letters), use OCR tools (e.g., Tesseract) to try reading the characters. Use Python + Selenium to automate screenshot → image cleanup → OCR → auto-fill. Step 4: If CAPTCHA is logic-based (e.g., "What is 2 + 3?"), write a script to solve the question dynamically. Step 5: Some apps have static CAPTCHA answers (e.g., same image or math puzzle repeatedly). Write a brute force script that tries common answers (captcha=5, captcha=7, etc.). Step 6: Use Burp Suite Intruder to repeat submissions with different CAPTCHA guesses. Step 7: If app lets through invalid CAPTCHA, you found a bypass logic flaw. Step 8: Once CAPTCHA is bypassed, attackers can continue brute-force attacks like password guessing or spam submission.
- **Detection**: Analyze form behavior; monitor for repeated CAPTCHA failures with same IP or timing
- **Solution**: Use modern CAPTCHA (reCAPTCHA v3+); implement rate-limiting even on correct CAPTCHA; log anomaly patterns
- **Tags**: CAPTCHA Bypass, OCR, Brute Force, Form Exploit

## Brute Forcing Cryptographic Keys

- **Attack Type**: Keyspace Exhaustion / Symmetric Key Cracking
- **Target**: Encrypted Files or Data
- **Vulnerability**: Weak encryption or short keys used
- **MITRE**: T1110.005 – Cryptographic Key Brute Force
- **Impact**: Full decryption of confidential data
- **Tools**: Hashcat, John, OpenSSL, Python CryptoLibs
- **Scenario**: Attackers try all possible key combinations to decrypt data encrypted with weak algorithms (e.g., 56-bit DES or short AES keys). This is a pure cryptographic brute-force attack done offline.
- **Attack Steps**: Step 1: Get access to encrypted data (e.g., encrypted file or captured ciphertext). Step 2: Identify the encryption algorithm used (DES, AES-128, etc.) using header bytes or context. Step 3: If key length is short (e.g., DES = 56 bits), calculate keyspace (e.g., 2^56 possible keys). Step 4: Use hashcat or custom scripts to generate all possible keys in that space. For example: DES cracking may take hours/days depending on your CPU/GPU. Step 5: Write a script that tries decrypting the file using each generated key. Example using Python’s PyCrypto or cryptography module. Step 6: Detect successful decryption by checking for readable output or known plaintext headers (e.g., "PDF", "PK", "Salted__"). Step 7: If successful, attacker gains access to encrypted content. Step 8: This technique is only feasible against old or improperly configured encryption (e.g., weak keys or ECB mode). Step 9: Modern encryption like AES-256 is impractical to brute-force due to keyspace size (2^256).
- **Detection**: Monitor encrypted file access; check for high CPU/GPU usage indicating key attempts
- **Solution**: Use strong encryption (AES-256+); never use DES/3DES; enforce long, random keys
- **Tags**: Cryptography, Key Cracking, DES, Offline Brute Force

## Directory or File Name Brute Forcing

- **Attack Type**: Resource Discovery via Forced Browsing
- **Target**: Web Servers
- **Vulnerability**: Accessible but unlinked files/folders
- **MITRE**: T1083 – File and Directory Discovery
- **Impact**: Information leakage, sensitive file exposure
- **Tools**: Dirb, Dirbuster, Gobuster, FFUF, Wfuzz
- **Scenario**: Attackers attempt to discover hidden files, admin panels, config files, or unlisted pages on a web server by brute-forcing common paths or filenames (like /admin, /backup.zip, /test.php, etc.)
- **Attack Steps**: Step 1: Identify a website you are legally allowed to test (like DVWA or a local server). Step 2: Install dirb or gobuster. Example with Gobuster: gobuster dir -u http://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt. Step 3: The tool sends hundreds or thousands of HTTP requests trying different directory or file names. Step 4: Each request checks if the server responds with 200 OK, 403, or 302 redirect — any of which can indicate the file/folder exists. Step 5: Review results and manually visit found URLs to assess exposure. For example, http://target.com/admin/, http://target.com/.git/, or backup.zip. Step 6: Defenders should detect this by monitoring for excessive 404/403 patterns from one IP. Step 7: Attackers often use wordlists like SecLists to maximize discovery. Step 8: This attack finds resources not meant to be public.
- **Detection**: Monitor for high volume 404s; use WAFs to detect scanning
- **Solution**: Use .htaccess, remove sensitive files, monitor access logs, hide backup/config endpoints
- **Tags**: Dirbusting, Gobuster, Hidden File Discovery

## Subdomain Brute Force

- **Attack Type**: DNS Enumeration via Brute Force
- **Target**: DNS Infrastructure
- **Vulnerability**: Forgotten or exposed subdomains
- **MITRE**: T1590 – Gather Subdomain Info
- **Impact**: Exposure of dev portals, admin sites, or internal apps
- **Tools**: Sublist3r, DNSMap, Fierce, Amass, Gobuster (dns mode)
- **Scenario**: Attackers discover subdomains (e.g., admin.target.com, dev.target.com) by trying many common names to see which resolve via DNS. These subdomains may expose internal tools, staging servers, or forgotten deployments.
- **Attack Steps**: Step 1: Choose a legal target domain you own or are authorized to test. Step 2: Install Sublist3r: sublist3r -d target.com. It tries thousands of subdomain names like test., mail., dev. etc. Step 3: Alternatively, use gobuster: gobuster dns -d target.com -w common-subdomains.txt. Step 4: Each tool sends DNS queries for subdomain.target.com. If it resolves (responds), it's marked as valid. Step 5: Valid subdomains are saved for manual inspection. Visit in browser or probe via tools (e.g., curl, nmap). Step 6: Some may lead to forgotten apps, admin panels, or dev portals. Step 7: Attackers use wordlists (e.g., SecLists) for efficient fuzzing. Step 8: Organizations often forget to secure or remove old subdomains. Step 9: Defenders can monitor DNS zone lookups or use canary subdomains to detect enumeration.
- **Detection**: Monitor DNS logs or external recon scans from passive sources
- **Solution**: Use wildcard DNS + monitoring; limit exposed subdomains; regularly audit DNS records
- **Tags**: Subdomain Enumeration, DNS Brute Force, Recon

## CAPTCHA Token Guessing

- **Attack Type**: CAPTCHA Token Prediction or Reuse
- **Target**: Web Apps using CAPTCHA
- **Vulnerability**: Predictable or static CAPTCHA tokens
- **MITRE**: T1208 – CAPTCHA Bypass
- **Impact**: CAPTCHA bypass → brute force, spam, abuse
- **Tools**: Burp Suite, Postman, Browser DevTools, Python
- **Scenario**: Attackers guess or reuse CAPTCHA tokens to bypass form protections, especially when the token is predictable, static, or weakly implemented (e.g., timestamp-based, session-based, or sent in hidden fields).
- **Attack Steps**: Step 1: Find a form that uses a CAPTCHA but passes the CAPTCHA token in a hidden field (captcha_token=abcd1234). Step 2: Submit the form and observe what happens when CAPTCHA is invalid vs valid. Step 3: Use browser tools or Burp to analyze the request payload. Note how the token is generated — if it's short, numeric, timestamp-based, or static. Step 4: Try resubmitting the same valid token multiple times. If it works more than once, the token is reusable — a flaw. Step 5: If tokens are short (e.g., 6-digit numeric), try brute-forcing them: write a script or use Burp Intruder to try captcha_token=000001 to 999999. Step 6: Some sites respond differently when token is valid. Look for anomalies in HTTP response. Step 7: If token values follow patterns (e.g., incrementing IDs or timestamps), you may predict future valid tokens. Step 8: This lets attackers bypass CAPTCHA, spam forms, or resume brute force attacks.
- **Detection**: Check for token reuse, short token formats, token lifetimes
- **Solution**: Use encrypted tokens, server-side validation, expiry, strong randomness
- **Tags**: CAPTCHA Abuse, Token Guessing, Form Exploit

## Session ID Brute Forcing

- **Attack Type**: Session Hijacking via Predictable IDs
- **Target**: Web Apps with Sessions
- **Vulnerability**: Weak/random session token generation
- **MITRE**: T1070 – Session Hijacking
- **Impact**: Unauthorized access, identity theft
- **Tools**: Burp Suite, Python (requests), wfuzz, curl
- **Scenario**: Attackers try to guess or brute-force session IDs to hijack valid user sessions. If session tokens are short, predictable, or improperly implemented (e.g., incremental IDs or encoded usernames), attackers can impersonate users.
- **Attack Steps**: Step 1: Access a login-protected area of your legal test website. After login, capture your session cookie (e.g., sessionid=abc123). Step 2: Analyze the token format. If it's short, numeric, base64-encoded usernames, or timestamp-based, it may be predictable. Step 3: Use Burp Suite Intruder or a custom Python script to send HTTP requests with different session tokens. For example: loop sessionid=abc124, abc125, abc126, etc. Step 4: Check responses — if one of the guessed tokens returns a valid page or redirects to a dashboard, the session is active and the attacker is in. Step 5: If session IDs are generated poorly (e.g., incremented integers, MD5(timestamp)), brute forcing becomes feasible. Step 6: Defenders should detect such attacks by monitoring sessions per IP/device and alerting on abnormal activity. Step 7: This allows full account hijacking without login. Step 8: Attackers can now steal data, impersonate users, or escalate privileges.
- **Detection**: Monitor session anomalies (IP changes, reuse patterns); analyze token entropy
- **Solution**: Use long, random, cryptographically strong session IDs; tie to IP/device; invalidate on logout
- **Tags**: Session Hijack, Predictable ID, Cookie Guessing

## Multi-Factor Code Brute Force

- **Attack Type**: OTP/2FA Brute Forcing via Code Guessing
- **Target**: Web/Mobile Apps using 2FA
- **Vulnerability**: No rate-limiting or CAPTCHA on OTP/2FA
- **MITRE**: T1110.001 – Brute Force Login
- **Impact**: Full 2FA bypass and account compromise
- **Tools**: Burp Suite, Hydra, Custom Python Scripts, SecLists
- **Scenario**: Attackers attempt to guess Time-Based One-Time Passwords (TOTPs) or codes sent via email/SMS in 2FA-enabled systems. This is possible when there is no rate-limiting or lockout on repeated OTP attempts.
- **Attack Steps**: Step 1: Find a web or mobile app that uses OTP or 2FA (e.g., code sent to email or generated by Google Authenticator). Step 2: Try logging in and capture the 2FA submission request using Burp Suite. Step 3: Observe how the code is submitted — usually a POST request like code=123456. Step 4: Send a wrong code and analyze the server’s response (e.g., Invalid code, Try again, etc.). Step 5: Now, use Burp Intruder or a script to automate code submission. Loop from 000000 to 999999. Example in Python: for code in range(1000000): send_request(code). Step 6: Check server responses for successful status (e.g., HTTP 302 redirect or welcome message). Step 7: If there is no CAPTCHA, lockout, or delay, the attacker may guess the correct code within minutes. Step 8: This bypasses 2FA protection and allows full account takeover. Step 9: Works best when OTP is static for a session or not time-bound strictly.
- **Detection**: Monitor OTP failures per IP/device; detect too many attempts on OTP/2FA endpoints
- **Solution**: Enforce lockout after N wrong OTPs, use CAPTCHAs, restrict IPs, use TOTP with strict expiration
- **Tags**: 2FA Bypass, OTP Brute Force, Account Takeover

## Local File Brute Force in Web Apps

- **Attack Type**: File Inclusion/Guessing via Path Brute Force
- **Target**: Web Applications
- **Vulnerability**: Unvalidated file paths or accessible sensitive files
- **MITRE**: T1210 – Exploitation of Remote Services
- **Impact**: Exposure of credentials, DB info, source code
- **Tools**: FFUF, Burp Suite, curl, Dirb, wfuzz
- **Scenario**: Attackers attempt to discover and access local files in a web app (e.g., config.php, .env, backup.bak) by guessing or brute-forcing file names and inclusion parameters. These may expose credentials or source code.
- **Attack Steps**: Step 1: Identify a file download or include functionality (e.g., GET /download?file=report.pdf or include=template.php). Step 2: Change the filename parameter to a common file like config.php and submit the request. Step 3: Observe if the server returns a readable file, an error, or a download prompt. Step 4: Use ffuf to automate this with a wordlist: ffuf -u http://target.com/view?file=FUZZ -w common-files.txt. Step 5: The tool will try hundreds of common file names (.env, db.sqlite, admin.php, etc.). Step 6: If one returns a 200 OK or larger response, download and inspect the contents. Step 7: If file contains credentials or source code, attacker gains internal knowledge or access. Step 8: May be combined with LFI (Local File Inclusion) for deeper access. Step 9: Defenders can detect this via error logs or spikes in 404/500 responses.
- **Detection**: Monitor file access patterns and file-not-found logs
- **Solution**: Validate file inputs, restrict directory access, store configs outside webroot, disable file browsing
- **Tags**: File Disclosure, Path Guessing, Config Leak

## Email/Username Enumeration via Brute Force

- **Attack Type**: Account Discovery through Login Response Testing
- **Target**: Login/Forgot Password Forms
- **Vulnerability**: Different responses for valid/invalid users
- **MITRE**: T1589 – Gather Credentials
- **Impact**: Valid user discovery for brute force or phishing
- **Tools**: Burp Suite, curl, Hydra, Postman, Python (requests)
- **Scenario**: Attackers test login or registration forms repeatedly to find valid email/usernames by analyzing how the application responds differently to valid and invalid inputs. Often used as a pre-step before password brute forcing.
- **Attack Steps**: Step 1: Visit a login or forgot-password form where the user inputs their email/username. Step 2: Try submitting a request with a non-existent email (e.g., test123@email.com) and note the error message (e.g., "User not found"). Step 3: Try again with a known or guessed email (e.g., admin@example.com) and compare the response (e.g., "Code sent" or "Wrong password"). Step 4: If the app shows different messages or status codes, it is vulnerable to enumeration. Step 5: Now use Burp Suite Intruder or a Python script to automate submission of a large list of usernames or emails (rockyou-usernames.txt). Step 6: Analyze the responses — the presence or absence of specific keywords like "not registered" or "try again" reveals valid users. Step 7: With a list of valid usernames, attackers can proceed with brute force or phishing. Step 8: This is often unnoticed unless rate-limiting or alerting is in place. Step 9: Attackers can even use timing differences (response delay) as an indicator of valid users.
- **Detection**: Analyze logs for failed attempts with user enumeration patterns
- **Solution**: Use generic error messages ("Invalid credentials"), add CAPTCHA, rate-limit username checking endpoints
- **Tags**: Enumeration, Brute Force Prep, Info Leak

## Mobile App PIN Brute Force

- **Attack Type**: 4/6-digit App Lock PIN Code Guessing
- **Target**: Mobile Applications
- **Vulnerability**: No lockout or insecure PIN validation
- **MITRE**: T1110.001 – PIN Brute Force
- **Impact**: Bypass app lock, access private user data
- **Tools**: Android Emulator, Frida, ADB, Python, MobSF, Burp
- **Scenario**: Attackers repeatedly guess 4-digit or 6-digit PIN codes on a mobile app (e.g., banking app, crypto wallet) to unlock or gain access. Apps with no attempt limit or weak PIN handling are vulnerable.
- **Attack Steps**: Step 1: Set up an Android emulator or physical test device and install the target app. Ensure testing is legal and authorized. Step 2: Open the app and observe the PIN entry behavior (e.g., 1234, 000000, etc.). Step 3: Try entering several wrong PINs and observe if there’s a lockout. Step 4: If there’s no delay or lockout, write a script (e.g., via ADB or Frida) to automatically submit PINs: 0000 to 9999. Example: adb shell input text 0001 && adb shell input keyevent 66 (submit key). Step 5: Monitor the response or screen to check if access was granted. Step 6: Alternatively, decompile the app using MobSF or jadx to check PIN verification logic in the code. If PIN is stored or statically compared, extract or patch it. Step 7: Tools like Frida can be used to hook PIN comparison functions and force a bypass. Step 8: If successful, attacker unlocks the app without knowing the real PIN. Step 9: This is a major flaw in mobile financial or personal apps.
- **Detection**: Monitor app usage patterns and implement retry/lockout counters
- **Solution**: Enforce retry limits, encrypt and obfuscate PIN logic, use biometric fallback, implement hardware-backed storage (Keystore)
- **Tags**: Mobile Brute Force, PIN Bypass, Android Reverse Engineering

## WEP/WPA/WPA2 Key Brute Forcing

- **Attack Type**: Wi-Fi Password Brute Force Using Packet Capture
- **Target**: Wi-Fi Routers & Access Points
- **Vulnerability**: Weak Wi-Fi password, PSK reuse
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Wi-Fi access, internal network attack entry
- **Tools**: Aircrack-ng, Hashcat, Wireshark, hcxdumptool, wordlists
- **Scenario**: Attackers use captured handshake packets (.cap files) to brute-force pre-shared keys (WPA/WPA2) or exploit weak encryption (WEP). Works when weak or dictionary-based passwords are used on Wi-Fi networks.
- **Attack Steps**: Step 1: Use a Wi-Fi adapter in monitor mode (e.g., Alfa card) and run airodump-ng wlan0mon to view nearby Wi-Fi networks. Step 2: Identify target with WPA/WPA2 encryption. Use airodump-ng -c [channel] --bssid [target-BSSID] -w capture wlan0mon to capture handshake. Step 3: Wait for a client to connect, or force disconnect using aireplay-ng --deauth 10 -a [BSSID] wlan0mon. The reconnect will trigger a handshake. Step 4: After capture, you'll have a .cap file. Step 5: Use aircrack-ng capture.cap -w rockyou.txt to try all passwords in the wordlist. If the password is in the list, it will crack and show the key. Step 6: For faster cracking, convert .cap to .hccapx and use Hashcat: hashcat -m 2500 file.hccapx wordlist.txt. Step 7: If key is found, attacker can join the Wi-Fi network. Step 8: WEP can be broken faster using IV replay; WPA2-PSK relies on dictionary or GPU brute force.
- **Detection**: Monitor for packet captures, MAC spoofing, and unusual connection attempts
- **Solution**: Use long, complex passphrases; upgrade to WPA3; disable WPS; monitor failed auth attempts
- **Tags**: Wi-Fi Cracking, Handshake Capture, Aircrack-ng

## JWT Secret Key Brute Force

- **Attack Type**: HMAC Secret Guessing via JWT Header Abuse
- **Target**: APIs using JWT
- **Vulnerability**: Weak HMAC secret, JWT trust without verification
- **MITRE**: T1606 – Forge Web Credentials
- **Impact**: Admin impersonation, privilege escalation
- **Tools**: jwt_tool.py, jwt-cracker, Python JWT libraries
- **Scenario**: Attackers brute-force the HMAC secret used to sign a JSON Web Token (JWT). If the secret is weak or guessable, they can forge valid tokens and impersonate users (e.g., create admin session tokens).
- **Attack Steps**: Step 1: Capture a JWT token from an API or web application (usually in the Authorization: Bearer header). Step 2: Decode the JWT using any online tool or script (it's base64): header.payload.signature. Check the algorithm (e.g., HS256). Step 3: Use tools like jwt_tool.py to perform brute force: jwt_tool.py -t <token> -d -C -J -w rockyou.txt. Step 4: The tool tries each word in the list as a secret to verify the token signature. If successful, it reveals the secret key. Step 5: Once the secret is found, create your own token with arbitrary claims (e.g., {"role":"admin"}) and sign with the secret. Step 6: Send this forged token to gain unauthorized access to protected API endpoints or dashboards. Step 7: Defenders should monitor token manipulation and verify claims on server-side. Step 8: This attack is possible only if the secret is weak or predictable (e.g., secret123, jwt, admin). Step 9: Works well on insecure dev/staging APIs or legacy applications.
- **Detection**: Monitor claims manipulation; track abnormal JWT use
- **Solution**: Use long, random secrets; switch to asymmetric JWT (RS256); validate claims server-side
- **Tags**: JWT Cracking, Token Forgery, HMAC Abuse

## IoT Device Credential Brute Forcing

- **Attack Type**: Default/Weak Password Exploitation
- **Target**: IoT Devices (Smart Cam, Router)
- **Vulnerability**: Default credentials, no brute-force protection
- **MITRE**: T1110 – Credential Brute Force
- **Impact**: Full control of device, eavesdropping, pivot attack
- **Tools**: Hydra, Medusa, Telnet, Shodan, Python sockets
- **Scenario**: Many IoT devices (cameras, smart bulbs, routers) expose web interfaces, SSH, or telnet ports. Attackers try default or weak passwords (admin:admin, root:1234) via brute force to gain full control of the device.
- **Attack Steps**: Step 1: Identify exposed IoT devices on the network or internet (e.g., via shodan.io or Nmap scan on local network). Look for Telnet (port 23), SSH (port 22), or HTTP (port 80/8080) interfaces. Step 2: Try accessing via browser (http://IP:port) or terminal (telnet IP). Step 3: Use Hydra to automate login attempts: hydra -l admin -P passwords.txt telnet://IP. For web logins, use http-form-post module. Step 4: Try common credentials from SecLists (e.g., root/root, admin/password, etc.). Step 5: If successful, attacker gets shell or admin dashboard access to control camera/mic/router. Step 6: Use gained access to pivot into other parts of the network or exfiltrate data. Step 7: Some IoT devices expose sensitive APIs without authentication (/config, /snapshot). Test those too. Step 8: Defenders should change default credentials and disable unused ports. Step 9: This is one of the most common IoT attack vectors.
- **Detection**: Monitor login attempts, close unused ports, change default credentials
- **Solution**: Change all default passwords, disable Telnet, use firewall, implement strong auth
- **Tags**: IoT Hacking, Telnet Brute Force, Smart Device Exploitation

## Timing Attacks via Brute Force (GraphQL Fields)

- **Attack Type**: Field Guessing via Response Timing Differences
- **Target**: GraphQL APIs
- **Vulnerability**: Lack of rate-limiting or uniform response timing
- **MITRE**: T1592 – Gather Victim Identity Info
- **Impact**: Field enumeration, API abuse, data exposure
- **Tools**: GraphQL Voyager, gql-fuzzer, Burp Suite, Python + time
- **Scenario**: GraphQL APIs often expose many fields. Attackers guess field names or mutations and measure how long the server takes to respond — longer time may indicate partial matches or valid fields, enabling schema discovery.
- **Attack Steps**: Step 1: Access a target GraphQL endpoint (e.g., /graphql). Test manually by submitting { __typename } to confirm it's working. Step 2: Prepare a list of common field names or query templates (query { login }, query { users }, etc.). Step 3: Use a Python script or Burp Intruder to send each query one by one and measure how long it takes to respond. Step 4: Record all response times. If one takes significantly longer than the rest, it may indicate the field exists or partially matches something valid (e.g., usrs → fast fail, users → slower fail or success). Step 5: Narrow down which fields exist by refining guesses. Step 6: Once fields or mutations are confirmed (e.g., resetPassword, createAdmin), craft valid queries to enumerate data or perform actions. Step 7: This is a blind brute force method — relies on subtle timing differences. Step 8: Works even when verbose errors are disabled. Step 9: Defenders should equalize processing time and rate-limit unknown queries.
- **Detection**: Monitor GraphQL introspection and rate of malformed queries
- **Solution**: Rate-limit GraphQL queries, disable introspection, equalize response timing, log brute-like behavior
- **Tags**: GraphQL Timing, Schema Fuzzing, Blind Brute Force

## Login Form Dictionary Attack (Web Login)

- **Attack Type**: Web Login Brute Force with Wordlists
- **Target**: Web Login Pages
- **Vulnerability**: No rate-limiting or CAPTCHA on login
- **MITRE**: T1110 – Brute Force
- **Impact**: Account compromise, credential stuffing
- **Tools**: Burp Suite, Hydra, curl, rockyou.txt
- **Scenario**: Attackers use a dictionary of common passwords against login forms (/login, /admin) to gain access to user accounts, especially when rate-limiting or CAPTCHA protections are missing.
- **Attack Steps**: Step 1: Open the target login page (e.g., example.com/login). Step 2: Capture a login request using Burp Suite (username & password POST request). Step 3: Find the fields used in the login (e.g., username=admin&password=1234). Step 4: Open Burp Intruder and set the POST request as a payload attack. Set one field (e.g., password) as the attack position. Step 5: Load a wordlist like rockyou.txt or top1000.txt from /usr/share/wordlists. Step 6: Start the attack — Burp will try all passwords one by one. Step 7: Look for responses with different length or status code (e.g., 302 redirect or “Welcome back”). This means login succeeded. Step 8: Alternatively, use Hydra: hydra -l admin -P rockyou.txt http-post-form "/login:username=^USER^&password=^PASS^:F=Invalid" — replace placeholders with actual form values. Step 9: If one password works, the attacker gains full user access.
- **Detection**: Monitor failed logins from same IP or unusual username/password combos
- **Solution**: Enforce rate-limiting, CAPTCHA, and account lockout mechanisms
- **Tags**: Web Login, Brute Force, Credential Stuffing

## Password Hash Cracking (Offline)

- **Attack Type**: Offline Dictionary-Based Hash Cracking
- **Target**: Leaked/Dumped Password Hashes
- **Vulnerability**: Weak hash types, reused passwords
- **MITRE**: T1555 – Credentials from Password Store
- **Impact**: Account recovery, lateral movement
- **Tools**: Hashcat, John the Ripper, hash-identifier
- **Scenario**: If an attacker obtains dumped password hashes (from DB or leaks), they can perform offline brute-force using hash-matching techniques to recover plaintext passwords. This enables privilege escalation or lateral movement.
- **Attack Steps**: Step 1: Obtain leaked password hashes — usually from a compromised database (e.g., via SQL injection or dump files). Hashes look like 5f4dcc3b5aa765d61d8327deb882cf99 (MD5) or longer (SHA-256). Step 2: Identify the hash type using hashid or hash-identifier. Step 3: Use John the Ripper: john --format=raw-md5 --wordlist=rockyou.txt hashes.txt or Hashcat: hashcat -m 0 hashes.txt rockyou.txt. Step 4: The tool will hash each word in the list and compare it to the stored hash. Step 5: If a match is found, the tool outputs the plaintext password. Step 6: Cracked passwords can now be used to log in to user accounts, or reused in other systems (password reuse). Step 7: Since this is done offline, there are no logs or alerts on the original server. Step 8: Very effective when users use weak passwords or when hashing algorithms are fast (like MD5 or SHA1). Step 9: To defend, use slow hash algorithms (bcrypt, scrypt) and long random passwords.
- **Detection**: Monitor for hash dumps/leaks, unusual credential reuse
- **Solution**: Store passwords with bcrypt/scrypt, monitor leaks, enforce complex password policies
- **Tags**: Hash Cracking, Offline Brute Force, Password Recovery

## SSH Dictionary Attack

- **Attack Type**: SSH Brute Force via Common Credentials
- **Target**: SSH Services
- **Vulnerability**: Open port 22 with weak credentials
- **MITRE**: T1110.003 – Brute Force Remote Service
- **Impact**: Remote shell access, root takeover
- **Tools**: Hydra, Ncrack, Medusa, wordlists, nmap
- **Scenario**: SSH services on port 22 are often exposed by developers, IoT devices, and misconfigured VMs. Attackers try common usernames and passwords to gain shell access. This can lead to full server control if root access is achieved.
- **Attack Steps**: Step 1: Scan the target using Nmap: nmap -p 22 target.com to confirm SSH is open. Step 2: Use Hydra to start brute-force: hydra -L usernames.txt -P rockyou.txt ssh://target.com. This tests every username with every password. Step 3: Watch for login success in Hydra's output (e.g., [22][ssh] host: target.com login: root password: admin123). Step 4: If one works, log in via SSH: ssh root@target.com and enter the cracked password. Step 5: Once inside, the attacker can browse files, plant malware, or escalate privileges. Step 6: This is very common with default usernames like root, admin, user, or when VMs are cloned with default credentials. Step 7: Ncrack and Medusa work similarly and can be used if Hydra is blocked. Step 8: Attack can be performed from VPS or home system — log review is the only defense unless rate-limiting or 2FA is enforced. Step 9: Defenders must disable password auth, use key-based login, and monitor login attempts closely.
- **Detection**: Log monitoring for multiple failed SSH logins, geo-IP anomalies
- **Solution**: Enforce SSH key auth only, disable password login, use fail2ban and allow only specific IPs
- **Tags**: SSH Brute Force, Remote Access, Hydra

## API Key or Secret Guessing

- **Attack Type**: Token/Key Brute Force for Unauthorized Access
- **Target**: REST APIs or Cloud Services
- **Vulnerability**: Weak or predictable API key format
- **MITRE**: T1110.004 – API Credential Brute Force
- **Impact**: Unauthorized access to internal or admin APIs
- **Tools**: Burp Suite, curl, Python requests, ffuf
- **Scenario**: Many APIs use static API keys or secrets passed via headers (Authorization: Bearer X). Attackers can brute-force these keys to gain unauthorized access, especially when keys are short or use weak entropy (e.g., abc123, apikey1, dev-key).
- **Attack Steps**: Step 1: Identify the target API endpoint that uses key/token auth (e.g., Authorization: Bearer <token> or x-api-key: <value> in headers). Step 2: Try accessing the endpoint with no key and observe the error — typically 401 Unauthorized or Invalid API Key. Step 3: Use curl or Postman to send repeated requests with different API keys from a wordlist. Example curl: curl -H "x-api-key: devkey123" https://api.example.com/endpoint. Step 4: Automate brute force using Python or ffuf. In ffuf: ffuf -w wordlist.txt -H "x-api-key: FUZZ" -u https://api.example.com/endpoint. Step 5: Observe if any request returns 200 OK, data, or success — this means the guessed API key worked. Step 6: Use the valid key to access other endpoints or impersonate users. Step 7: Often works on staging/dev APIs where the same keys are reused or shared among teams. Step 8: Very effective when keys are short and predictable or leaked in public repos. Step 9: Defenders must rotate keys, enforce long key formats, and monitor API logs closely for brute attempts.
- **Detection**: Monitor API gateway for key abuse or repeated failures; enable rate-limiting
- **Solution**: Use long keys, rotate secrets, enforce HMAC or OAuth with strict access policies
- **Tags**: API Security, Token Guessing, Key Abuse

## Basic HTTP Auth / Digest Auth Bypass

- **Attack Type**: HTTP Basic/Digest Brute Force via Dictionary
- **Target**: Web Admin Panels
- **Vulnerability**: Use of HTTP Basic/Digest with no lockout
- **MITRE**: T1110 – Brute Force
- **Impact**: Unauthorized panel access, credential compromise
- **Tools**: curl, Hydra, Burp Suite
- **Scenario**: Web applications or legacy admin panels that rely on HTTP Basic or Digest authentication can be brute-forced by trying a list of common username/password combinations in the Authorization header.
- **Attack Steps**: Step 1: Access the target web page (e.g., http://target.com/admin) and see if the browser prompts for username/password — this is HTTP Basic Auth. Step 2: Open a terminal and use curl: curl -u admin:admin http://target.com/admin — this sends the Authorization header. Step 3: Try different username/password combinations manually or using Hydra: hydra -L usernames.txt -P passwords.txt target.com http-get /admin. Step 4: Observe Hydra output — if a valid pair is found, login is successful. Step 5: Use Burp Suite Repeater to manually test credentials and inspect HTTP responses. Step 6: If authentication succeeds, attacker gains access to sensitive internal pages. Step 7: Works best when there's no rate limiting or login lockout. Step 8: Attack can also be scripted using Python + requests library with Basic Auth header. Step 9: Defenders should avoid using HTTP Auth and move to token-based or form-based auth.
- **Detection**: Monitor Authorization header patterns, repeated failed login attempts
- **Solution**: Implement login rate-limiting, move to more secure auth, disable Basic/Digest Auth where possible
- **Tags**: HTTP Auth, Web Admin, Credential Stuffing

## FTP, Telnet, or SMTP Login Dictionary Attack

- **Attack Type**: Network Protocol Auth Brute Force (Dictionary)
- **Target**: FTP, Telnet, SMTP Servers
- **Vulnerability**: No rate-limit or password brute-force defense
- **MITRE**: T1110.003 – Remote Service Brute Force
- **Impact**: Shell access, file manipulation, email spoofing
- **Tools**: Hydra, Medusa, Ncrack, Telnet, FTP, SMTP clients
- **Scenario**: Network services like FTP (21), Telnet (23), and SMTP (25) may accept authentication and are often poorly secured. Brute-forcing these protocols using username/password dictionaries can lead to shell, email, or file access.
- **Attack Steps**: Step 1: Use Nmap to scan the target for open services: nmap -p 21,23,25 target.com. Step 2: If FTP is open, use Hydra: hydra -L users.txt -P rockyou.txt ftp://target.com. Step 3: If Telnet is open, use: hydra -l admin -P rockyou.txt telnet://target.com. Step 4: For SMTP, use: hydra -L users.txt -P passwords.txt smtp://target.com. Step 5: Observe the response from Hydra — if successful, it will display the working credentials. Step 6: Use FTP or Telnet client (e.g., ftp target.com, telnet target.com) to log in manually with found credentials. Step 7: With FTP access, attacker can upload/download files. With Telnet, attacker may get shell. With SMTP, they might relay emails. Step 8: These services are commonly misconfigured in old systems or IoT devices. Step 9: Defenders must disable unused services and enforce strong password policies.
- **Detection**: Monitor failed login attempts; use IDS/IPS for port-based brute force detection
- **Solution**: Disable unused services, enforce key-based auth, deploy fail2ban and strong authentication
- **Tags**: FTP Brute Force, Telnet Access, SMTP Misuse

## JWT Secret Key Dictionary Attack

- **Attack Type**: JWT HMAC Secret Guessing via Wordlists
- **Target**: Web APIs using JWT
- **Vulnerability**: Weak or reused HMAC secrets
- **MITRE**: T1606.002 – Forge Web Credentials
- **Impact**: Account takeover, unauthorized API access
- **Tools**: jwt_tool.py, jwt-cracker, Python jwt
- **Scenario**: Attackers use a dictionary of common or weak secrets (e.g., mysecret, jwtsecret, 123456) to brute-force the HMAC key used to sign JSON Web Tokens (JWTs), enabling them to forge tokens with elevated privileges.
- **Attack Steps**: Step 1: Capture a JWT token from the target app (usually in HTTP headers or cookies). It will look like header.payload.signature. Step 2: Use jwt_tool.py or jwt-cracker to run a dictionary attack on the JWT signature. Example: jwt_tool.py -t <token> -C -d -J -w rockyou.txt. Step 3: The tool will try every word in the wordlist as the secret key and check if it verifies the JWT signature. Step 4: If the correct secret is found, the tool displays it. Step 5: Create a new forged token with custom payload (e.g., { "role": "admin" }) and sign it using the cracked secret. Step 6: Send the forged token in an API request to test elevated access. Step 7: If access is granted, attacker now impersonates a privileged user. Step 8: This works if developers use guessable secrets like admin, jwt123, or password. Step 9: Defenders must enforce secure, long, random keys for JWTs and use asymmetric signing (e.g., RS256).
- **Detection**: Monitor abnormal JWT claims; validate all JWTs server-side, especially for sensitive endpoints
- **Solution**: Use strong, unique HMAC keys; enforce RS256 asymmetric signing; avoid putting secrets in token payloads
- **Tags**: JWT Cracking, Token Manipulation, Secret Guessing

## PIN/OTP Code Guessing

- **Attack Type**: Brute Forcing Numeric PINs or One-Time Passwords
- **Target**: OTP or PIN-protected apps
- **Vulnerability**: No retry limit, weak randomization
- **MITRE**: T1110.002 – Brute Force Authentication
- **Impact**: 2FA bypass, account hijacking
- **Tools**: Python Scripts, Burp Suite, curl, Custom OTP bots
- **Scenario**: Attackers target PIN-based login (e.g., mobile apps, 2FA) or OTP endpoints (e.g., email/SMS) by trying all numeric combinations (e.g., 0000–9999). Can succeed when there’s no limit on retries or weak token generation logic.
- **Attack Steps**: Step 1: Identify a login or verification endpoint that uses PIN/OTP (e.g., POST /verify-otp or POST /login-pin). Step 2: Use Burp Suite to intercept the request and copy the structure. Example payload: { "otp": "1234" }. Step 3: Use Burp Intruder or a simple Python script to try all possible combinations from 0000 to 9999. For example: for pin in range(0, 10000): send_request(pin). Step 4: Monitor server responses — a different response code (e.g., 200 OK) means the correct code was guessed. Step 5: If the app doesn't implement rate-limiting or lockout after 3–5 attempts, brute force can easily succeed. Step 6: If OTPs are based on predictable logic (e.g., timestamp-based + weak key), they can be predicted rather than guessed. Step 7: Some attackers use multiple phone numbers or IPs to bypass rate-limiting. Step 8: Once the correct PIN/OTP is found, the attacker gains access to the victim’s account or 2FA bypass. Step 9: Defenders must implement retry limits, CAPTCHAs, and time-based OTPs using secure algorithms (e.g., TOTP).
- **Detection**: Monitor failed attempts per account or IP; set thresholds for OTP or PIN inputs
- **Solution**: Limit PIN/OTP retries, use secure TOTP libraries, rate-limit brute attempts, alert on suspicious guess patterns
- **Tags**: OTP Bypass, 2FA Brute Force, Mobile PIN Attack

## Directory/URL Enumeration with Dictionary

- **Attack Type**: Path Brute Force via Common Directory Names
- **Target**: Web Applications
- **Vulnerability**: Lack of access control or hidden path disclosure
- **MITRE**: T1083 – File and Directory Discovery
- **Impact**: Information disclosure, privilege escalation
- **Tools**: Dirsearch, Gobuster, wfuzz, FFUF
- **Scenario**: Attackers use a wordlist of common web directory and file names (like /admin, /config, /phpmyadmin) to discover hidden or unlisted paths on a web server, which may expose sensitive information or admin interfaces.
- **Attack Steps**: Step 1: Identify the base domain of the target website (e.g., https://example.com). Step 2: Use Dirsearch with a built-in or custom wordlist: dirsearch -u https://example.com -e php,html,txt -w /usr/share/wordlists/dirb/common.txt. Step 3: Dirsearch sends HTTP requests for each word in the list appended as a directory (e.g., https://example.com/admin, https://example.com/backup). Step 4: Monitor the responses — status codes like 200 OK or 403 Forbidden suggest the directory exists. Ignore 404s. Step 5: Use Gobuster if preferred: gobuster dir -u https://example.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html. Step 6: If a hidden admin or config page is discovered (e.g., /db/, /wp-login.php), attacker can attempt privilege escalation or look for sensitive files. Step 7: Works well against sites with poor obfuscation of sensitive paths. Step 8: Defender should implement proper access controls, avoid directory listing, and obfuscate URLs.
- **Detection**: Monitor for excessive 404/403 hits; use WAF to detect directory fuzzing
- **Solution**: Hide sensitive paths behind auth, disable directory listing, use randomized endpoint names
- **Tags**: Directory Bruteforce, URL Fuzzing, Reconnaissance

## Subdomain Discovery via Dictionary

- **Attack Type**: DNS Subdomain Brute Force
- **Target**: DNS Infrastructure
- **Vulnerability**: Exposed subdomains without proper controls
- **MITRE**: T1590 – Gather Subdomain Info
- **Impact**: Hidden system discovery, staging access, fingerprinting
- **Tools**: Sublist3r, DNSRecon, amass, gobuster vhost, ffuf
- **Scenario**: Attackers brute-force subdomains using DNS tools and dictionaries to find staging environments, dev instances, or admin panels on separate hosts (e.g., admin.domain.com, test.domain.com) that are not listed on the main website.
- **Attack Steps**: Step 1: Identify the root domain (e.g., example.com). Step 2: Use Sublist3r: sublist3r -d example.com to gather subdomains using passive DNS sources. Step 3: Use a brute-force method: dnsrecon -d example.com -D subdomains-top1000.txt -t brt. Step 4: Try Gobuster with vhost mode: gobuster vhost -u http://example.com -w /usr/share/wordlists/subdomains.txt. This will append subdomain names and send requests like http://dev.example.com. Step 5: Note valid responses (status 200, 403) and verify the subdomain exists via DNS or IP address resolution. Step 6: Once found, access these subdomains in the browser — often, staging sites are poorly secured and may expose backend logic or admin UIs. Step 7: Tools like amass can also combine brute-force and OSINT. Step 8: Defenders should monitor DNS records, use wildcard DNS blocks, and avoid exposing test environments publicly.
- **Detection**: Monitor DNS queries; use security DNS (e.g., DNS RPZ); block unknown hosts
- **Solution**: Use wildcard DNS protections, monitor for public subdomain enumeration, separate dev/test environments from prod
- **Tags**: Subdomain Bruteforce, Recon, DNS Enumeration

## Credential Stuffing (Using Known Dictionaries)

- **Attack Type**: Reuse of Stolen Credentials Across Sites
- **Target**: Web Login Portals
- **Vulnerability**: Credential reuse by users
- **MITRE**: T1110.004 – Credential Stuffing
- **Impact**: Account takeover, identity theft, fraud
- **Tools**: Sentry MBA, OpenBullet, Snipr, proxy chains, combolists
- **Scenario**: Credential stuffing attacks use leaked email/password combos from data breaches and try them against other websites where users may have reused the same password. It's automated using tools like Sentry MBA or OpenBullet.
- **Attack Steps**: Step 1: Obtain a "combolist" — a text file of email:password pairs from public breaches (e.g., found on dark web, Pastebin, or breach forums). Example: user@example.com:password123. Step 2: Identify the target login portal (e.g., https://target.com/login). Step 3: Configure Sentry MBA or OpenBullet with the target URL, request headers, POST parameters, and success indicators (e.g., Welcome, Dashboard). Step 4: Load the combo list into the tool and start the attack — it will send thousands of login attempts in sequence. Step 5: Tool reports which credentials are valid (hit) based on response content. Step 6: Valid credentials allow attacker to log in and take over the account. Step 7: Proxy rotation is used to avoid IP bans. Step 8: Attack success depends on password reuse by users across platforms. Step 9: Defender must implement 2FA, monitor for unusual login behavior, and check credentials against breach databases (e.g., HaveIBeenPwned).
- **Detection**: Monitor login attempts per IP/device, track breached credential use
- **Solution**: Enforce 2FA, use login anomaly detection, compare new logins with breach data
- **Tags**: Credential Stuffing, Breach Reuse, Sentry MBA

## Cryptographic Key Dictionary Attack

- **Attack Type**: Brute Force of Encryption/Signing Keys
- **Target**: Applications, APIs, Tokens
- **Vulnerability**: Weak, hardcoded, or reused cryptographic keys
- **MITRE**: T1110.001 – Brute Force Key Material
- **Impact**: Secret compromise, unauthorized decryption
- **Tools**: Hashcat, John, jwt_tool, brute-force scripts
- **Scenario**: When cryptographic keys (like RSA, API secrets, or AES keys) are chosen poorly or stored insecurely, attackers can use dictionary or known-key lists to guess them, especially if keyspaces are small or predictable.
- **Attack Steps**: Step 1: Identify where cryptographic keys are used — e.g., JWT signing keys, AES encryption keys in local apps, or API keys in requests. Step 2: Obtain a sample encrypted file, JWT token, or request with a signature. Step 3: Use a brute-force tool like Hashcat (hashcat -a 0 -m 11300 hashes.txt wordlist.txt) or jwt_tool.py for JWT. Step 4: Provide a wordlist of possible keys (e.g., jwtsecret, myappkey123, devkey). Step 5: The tool will try all keys from the wordlist to decrypt or verify the data. Step 6: If a match is found, attacker gains the valid key. Step 7: Use the cracked key to decrypt files, generate valid signatures, or forge API requests. Step 8: Works when developers hardcode secrets, reuse keys, or use weak default values. Step 9: Defender should rotate keys often, enforce high-entropy key generation, and store keys securely (e.g., Vault, AWS KMS).
- **Detection**: Analyze key usage, verify entropy, monitor abnormal decryption or key-related access
- **Solution**: Generate keys securely (e.g., using OpenSSL), avoid reuse/hardcode, store in key management systems
- **Tags**: Cryptographic Keys, JWT, Secret Guessing

## Email Login via SMTP Dictionary Attack

- **Attack Type**: Brute Forcing Email Auth via SMTP or IMAP
- **Target**: Mail Servers (SMTP/IMAP)
- **Vulnerability**: Weak passwords, no brute-force detection
- **MITRE**: T1110 – Brute Force
- **Impact**: Email account compromise, internal data exposure
- **Tools**: Medusa, Ncrack, Telnet, custom SMTP clients
- **Scenario**: Email servers often allow login through protocols like SMTP (port 587) or IMAP (143/993). If strong auth or rate-limiting is not enforced, attackers can brute-force credentials using wordlists.
- **Attack Steps**: Step 1: Scan the target for open email ports: use nmap -p 25,465,587,143,993 mail.target.com to detect SMTP/IMAP services. Step 2: Choose SMTP (STARTTLS) or IMAP for attack. Step 3: Use Medusa: medusa -h mail.target.com -U usernames.txt -P passwords.txt -M imap -T 10. This tries all user:pass combinations. Step 4: Monitor output for successful login (it will display a hit). Step 5: If credentials work, use Thunderbird or telnet to login manually and validate email access. Step 6: You can also use openssl s_client -connect mail.target.com:993 to test IMAP manually. Step 7: Brute force can also be automated with Python using smtplib or imaplib. Step 8: Works best against servers without login lockouts, legacy systems, or reused corporate passwords. Step 9: Defenders should use fail2ban, 2FA for email, and monitor brute patterns.
- **Detection**: Monitor failed logins, excessive IMAP/SMTP requests
- **Solution**: Enforce strong passwords, implement rate-limiting, deploy 2FA
- **Tags**: Email Login, SMTP Bruteforce, IMAP Brute Force

## Mobile App Login Dictionary Attack

- **Attack Type**: Brute Forcing Mobile App Login Requests
- **Target**: Mobile App APIs
- **Vulnerability**: Missing lockouts, insecure mobile auth flow
- **MITRE**: T1110.002 – Brute Force Authentication
- **Impact**: Mobile account takeover, data leakage
- **Tools**: Burp Suite, Frida, Postman, mitmproxy, Wordlists
- **Scenario**: Many Android or iOS apps communicate with backend servers via APIs. If login requests are not protected, attackers can capture them and replay with password dictionaries to gain unauthorized access.
- **Attack Steps**: Step 1: Install the mobile app on an Android emulator or real device. Step 2: Set up a proxy tool like Burp Suite or mitmproxy and configure the mobile device to route traffic through it. Step 3: Log in once to capture the login API request (e.g., POST /api/login). Step 4: Inspect headers and body to identify the username and password fields (e.g., {"email":"user@x.com", "pass":"1234"}). Step 5: Use Burp Intruder or Postman Collection Runner to replay the same login request with multiple passwords from a wordlist (e.g., rockyou.txt). Step 6: Observe responses — a 200 OK or success message indicates valid credentials. Step 7: If rate limiting or lockouts are missing, attacker can try thousands of passwords. Step 8: Tools like Frida or Xposed may help bypass client-side restrictions or encryption. Step 9: Defender must use CAPTCHA, 2FA, and secure API authentication to prevent such brute force attacks.
- **Detection**: Analyze API traffic, flag unusual login attempts
- **Solution**: Implement CAPTCHA, rate-limiting, secure API auth (OAuth, TOTP), device fingerprinting
- **Tags**: Mobile Brute Force, App Login API, Credential Replay

## Encrypted Archive File Dictionary Cracking

- **Attack Type**: Password Cracking on Encrypted ZIP/RAR/7z Archives
- **Target**: Encrypted Files (ZIP/RAR)
- **Vulnerability**: Weak archive passwords
- **MITRE**: T1110.005 – Archive Decryption
- **Impact**: Access to sensitive offline data
- **Tools**: John the Ripper, fcrackzip, 7z2hashcat, rar2john
- **Scenario**: Attackers may encounter encrypted archive files (.zip, .rar, .7z) that require a password to extract contents. If the password is weak, it can be brute-forced using wordlists or rule-based dictionary attacks.
- **Attack Steps**: Step 1: Download or obtain the encrypted archive file (e.g., secret.zip, backup.7z, docs.rar). Step 2: Use fcrackzip for zip files: fcrackzip -v -u -D -p rockyou.txt secret.zip. This tries every password in the dictionary. Step 3: For .rar/.zip with John the Ripper, first convert to hash: zip2john secret.zip > hash.txt, then john --wordlist=rockyou.txt hash.txt. Step 4: For 7z, convert using 7z2hashcat and run with Hashcat: hashcat -m 11600 hash.txt rockyou.txt. Step 5: Monitor the tool for successful password discovery. If found, extract contents using unzip, 7z x, or unrar. Step 6: Password-cracked archives may reveal sensitive config files, credentials, or database dumps. Step 7: Defenders should use high-entropy passwords for archives, avoid archiving secrets, and consider AES encryption instead. Step 8: Brute force is CPU-intensive but works well against weak or default passwords.
- **Detection**: Monitor file access and archive extraction attempts
- **Solution**: Use long random archive passwords, encrypt files with secure AES-256, store archives in protected locations
- **Tags**: ZIP Crack, Archive Password Brute, 7z Dictionary

## GPG/PGP Private Key Passphrase Guessing

- **Attack Type**: Brute Forcing GPG/PGP Key Passphrases
- **Target**: Private GPG/PGP Keys
- **Vulnerability**: Weak passphrase on exported key
- **MITRE**: T1110.006 – Private Key Brute Force
- **Impact**: Identity theft, fake commits, encrypted data access
- **Tools**: John the Ripper, GPG2John, Hashcat, gpg
- **Scenario**: GPG/PGP private keys are encrypted with a passphrase. If weak, attackers with the private key file can brute-force it using common passphrases from dictionaries, especially in stolen developer laptops or compromised machines.
- **Attack Steps**: Step 1: Obtain the private key file (e.g., privatekey.asc) from a backup, leak, or compromised host. Step 2: Convert to hash format using gpg2john: gpg2john privatekey.asc > keyhash.txt. Step 3: Run John: john --wordlist=rockyou.txt keyhash.txt. This will attempt every passphrase from the list. Step 4: Alternatively, use Hashcat with hash mode 17000. Step 5: Monitor output — once correct passphrase is found, John will show it. Step 6: Import the key with gpg --import privatekey.asc, then unlock it using the recovered passphrase. Step 7: You can now decrypt files, sign commits, or impersonate the key owner in secure communications. Step 8: This attack is viable only if key was protected with weak or reused passwords. Step 9: Defenders must store private keys in secure vaults and use very strong passphrases (20+ chars, no dictionary words).
- **Detection**: Track key access and file system tampering; audit developer systems
- **Solution**: Use long, random passphrases; store keys in password managers or HSM; disable export or backups of private keys
- **Tags**: GPG Crack, Key Theft, Crypto Key Attack

## MD5 Hash Collision Attack

- **Attack Type**: Hash Collision to Forge File Integrity
- **Target**: Digital Signatures, AV Checkers
- **Vulnerability**: Use of insecure MD5 hash functions
- **MITRE**: T1600 – Hash Collision
- **Impact**: Malware obfuscation, digital signature forgery
- **Tools**: HashClash, FastColl, md5sum, openssl
- **Scenario**: MD5, once used for digital signatures and checksums, is broken. Attackers can create two files with different content but identical MD5 hashes, enabling signature forgery or malware obfuscation (e.g., "benign.pdf" vs "malware.pdf").
- **Attack Steps**: Step 1: Install HashClash (Linux): git clone https://github.com/cr-marcstevens/hashclash.git and build using make. Step 2: Create a controlled prefix or file layout (e.g., PDF file structure). Step 3: Use md5collgen or fastcoll to generate two different files (file1.bin, file2.bin) that produce the same MD5 hash. Example: fastcoll -o file1.bin file2.bin. Step 4: Append malicious code or payload to one of the files (e.g., malware script or fake transaction), but keep the initial collision block the same. Step 5: Verify both files have the same MD5: md5sum file1.bin file2.bin. Step 6: If signed by an insecure system using MD5, the attacker can swap in the malicious file without invalidating the signature. Step 7: Common use: malware that looks benign to antivirus or PDF tampering. Step 8: Defenders should never use MD5 for any security-critical purpose.
- **Detection**: Check for dual-collision blocks in files; hash comparison with SHA-256
- **Solution**: Ban MD5 in all cryptographic operations; use SHA-256+
- **Tags**: MD5 Collision, File Forgery, PDF Exploit

## SHA-1 Collision Attack

- **Attack Type**: Forged File with Matching SHA-1 Digest
- **Target**: File Integrity Systems
- **Vulnerability**: Use of SHA-1 in digital signature contexts
- **MITRE**: T1600 – Hash Collision
- **Impact**: Signed contract forgery, fake updates, data integrity loss
- **Tools**: SHAttered (Google), Git, OpenSSL
- **Scenario**: Like MD5, SHA-1 is vulnerable to collision attacks. Google and CWI showed how to create two different PDFs with the same SHA-1 hash, breaking systems that rely on SHA-1 for document verification.
- **Attack Steps**: Step 1: Understand the SHAttered attack: it exploits SHA-1's internal structure to create two PDFs with the same hash. Visit shattered.io. Step 2: Download SHAttered example files from GitHub (shattered-1.pdf, shattered-2.pdf). Step 3: Run sha1sum shattered-1.pdf shattered-2.pdf — both return the same hash. Step 4: Open the two PDFs and observe they are different visually. Step 5: These files were generated using highly specialized GPU-accelerated collision finding (using differential paths). Step 6: Attackers can use this to create fake software updates, Git commits, or legal contracts with identical SHA-1 signatures. Step 7: SHA-1 should be retired in all crypto applications. Step 8: Git now allows SHA-256 instead of SHA-1 to mitigate this. Step 9: Defenders must audit SHA-1 use in software and migrate to modern hashes.
- **Detection**: Hash comparison reveals identical SHA-1 but different SHA-256
- **Solution**: Stop using SHA-1; upgrade systems and software to SHA-256 or SHA-3
- **Tags**: SHA-1 Collision, Git Attack, File Tampering

## Digital Signature Forgery via MD5/SHA-1

- **Attack Type**: Digital Signature Manipulation via Weak Hash
- **Target**: PDF, Software, Certs
- **Vulnerability**: Weak hash in signature process
- **MITRE**: T1600 – Digital Signature Spoofing
- **Impact**: Contract or certificate forgery, fake signed apps
- **Tools**: OpenSSL, pdfcrack, SHAttered, md5collisiontoolkit
- **Scenario**: In digital signature schemes like X.509 certificates or PDF signing, using MD5 or SHA-1 allows attackers to swap signed documents after creating a collision, without invalidating the signature.
- **Attack Steps**: Step 1: Intercept or obtain a document digitally signed using MD5 or SHA-1 hash (e.g., .p7s, .pdf, .pem). Step 2: Analyze the hash algorithm used in the signature block with openssl asn1parse or a viewer. Step 3: If MD5/SHA-1 is used, extract the digest and document. Step 4: Use collision generation tools like fastcoll, md5collgen, or shattered to produce a second document with same hash but altered content. Step 5: Replace the original document with the crafted one — the digital signature remains valid. Step 6: This is especially dangerous in legal, certificate, or code signing contexts. Step 7: The forged file can impersonate a trusted signature (Adobe PDF, Windows EXE, signed email). Step 8: Defenders must avoid any trust based on MD5/SHA-1 signed documents. Step 9: Modern standards like SHA-256 with PKCS#7 or PSS should be enforced.
- **Detection**: Analyze digital signature metadata; alert on MD5/SHA-1 signed objects
- **Solution**: Enforce SHA-256+ signing in X.509, code signing, and digital docs
- **Tags**: Digital Signature Forgery, PDF Tampering, X.509 Weakness

## Duplicate Hash IDs in Blockchains

- **Attack Type**: Hash Collision Attack in Blockchain
- **Target**: Blockchain, Testnet Chains
- **Vulnerability**: Weak hashing algorithms for block IDs
- **MITRE**: T1600 – Hash Collision
- **Impact**: Blockchain fork, false ledger state, double spending
- **Tools**: Custom PoC, Python, GoLang, fastcoll, modified blockchain clients
- **Scenario**: If a hash function used in a blockchain (e.g., SHA-1 or MD5) is weak, attackers can create multiple blocks with the same hash, leading to transaction tampering, ledger manipulation, or blockchain forks.
- **Attack Steps**: Step 1: Identify or simulate a blockchain that uses a weak hash (e.g., early academic blockchains or testnets using MD5/SHA-1 for block IDs). Step 2: Understand the block structure: a block’s hash depends on its content and previous hash. Step 3: Use fastcoll or hashclash to generate two different payloads that hash to the same MD5/SHA-1 hash. Example: fastcoll -o blockA.dat blockB.dat. Step 4: Create two separate blocks with different transactions but the same block hash. Step 5: Submit one of them to the blockchain (blockA). Let it be validated and accepted. Step 6: Later, introduce blockB (same hash, different data) on a forked chain. Step 7: If the blockchain protocol does not validate block content strictly, the attacker may convince some nodes to accept blockB as valid. Step 8: This can disrupt consensus, mislead explorers, or rewrite history. Step 9: Always use collision-resistant hashes (SHA-256+) in blockchains.
- **Detection**: Chain audit tools, block validation re-checks
- **Solution**: Upgrade blockchain to SHA-256 or SHA-3; reject weak hash blocks; enforce chain integrity with digital signatures
- **Tags**: Blockchain Security, Hash Collision, Fork Exploit

## X.509 Certificate Collision Forgery

- **Attack Type**: Certificate Collision via MD5 or SHA-1
- **Target**: X.509 Certificates
- **Vulnerability**: Use of MD5/SHA-1 in certificate signing
- **MITRE**: T1587 – Trusted Cert Abuse
- **Impact**: Fake SSL/TLS identity, MiTM, phishing
- **Tools**: OpenSSL, md5collgen, hashclash, SHAttered, ASN.1 viewers
- **Scenario**: Using hash collisions (like MD5 or SHA-1), attackers can generate two certificate signing requests (CSRs) with the same hash, allowing them to forge a certificate that appears valid under a trusted CA’s signature.
- **Attack Steps**: Step 1: Understand X.509 certificate signing: a certificate authority (CA) signs the hash of the subject’s certificate. Step 2: Use tools like hashclash to generate two colliding certificate requests (CSRs). Step 3: Submit one CSR to a real or test CA using a weak hash (e.g., MD5, SHA-1). Step 4: Get the valid signed certificate from the CA. Step 5: Replace the original CSR with the second one that has the same hash but modified data (e.g., different public key or subject name). Step 6: Because the hash is the same, the CA's signature remains valid. Step 7: You now have a forged certificate signed by a trusted CA, which could impersonate the original entity. Step 8: This attack was demonstrated in 2008 to forge an SSL cert signed by a root CA. Step 9: Modern CAs have moved to SHA-256, but legacy systems may still trust weak certs.
- **Detection**: Analyze X.509 chain for weak hashes (MD5/SHA-1); check for duplicate serials or public keys
- **Solution**: Ban MD5/SHA-1 signed certs in browsers; use cert pinning; deploy CT logs with collision resistance
- **Tags**: Certificate Forgery, SSL Tampering, PKI Exploit

## Certificate Transparency Log Poisoning

- **Attack Type**: Log Injection via Colliding or Malicious Certs
- **Target**: CT Logs, Browsers, Trust Stores
- **Vulnerability**: Acceptance of fake or poisoned cert entries
- **MITRE**: T1584 – Compromise Infrastructure
- **Impact**: Trust system abuse, phishing, DoS on CT log consumers
- **Tools**: CT log monitors, Merkle tree tools, fake cert generators
- **Scenario**: Certificate Transparency (CT) logs track all certificates issued by CAs. Attackers can poison these logs by injecting malformed or spoofed certificates (e.g., collisions, bogus names), polluting the system of trust.
- **Attack Steps**: Step 1: Understand that CT logs are append-only logs storing all certificates issued by trusted CAs, built on Merkle trees. Step 2: Attackers create malicious or malformed certificates (e.g., via X.509 collision, bogus org names, reserved IPs) and submit them to a participating CA. Step 3: The CA includes the cert in the CT log (intentionally or mistakenly). Step 4: The log now contains a record that looks valid but links to an attacker-controlled certificate. Step 5: Some CT monitors and clients may blindly trust this entry, especially if they use older filters. Step 6: Poisoned CT logs can be used to impersonate sites, flood logs with garbage data, or trigger misconfigurations. Step 7: This is more of a poisoning/data abuse attack than a direct forgery. Step 8: Defenders must validate CT entries before trust, enforce domain validation rules, and use signed exchanges. Step 9: CT poisoning can erode trust in public logs if not mitigated.
- **Detection**: Monitor CT logs for anomalies; validate domain ownership and subject structure
- **Solution**: Harden CT inclusion rules; use domain validation, enforce log filtering; use Gossip protocols to cross-verify logs
- **Tags**: CT Log Poisoning, PKI Trust Abuse, Certificate Monitoring

## TLS Handshake Collision Abuse

- **Attack Type**: Protocol Abuse via Hash Collision in Handshake
- **Target**: TLS 1.0–1.2 Servers
- **Vulnerability**: Use of MD5/SHA-1 in TLS handshake hash
- **MITRE**: T1600 – Protocol Signature Forgery
- **Impact**: Session hijacking, identity spoofing
- **Tools**: OpenSSL, custom TLS client, forged certs, SHAttered
- **Scenario**: During the TLS handshake, cryptographic parameters (e.g., server cert, key exchange info) are hashed and signed. If the hash algorithm is weak (e.g., MD5/SHA-1), attackers can craft two different inputs that hash the same, leading to trust abuse.
- **Attack Steps**: Step 1: Understand that in TLS 1.2 and earlier, the handshake involves signing a hash of all negotiation parameters, including certificates. Step 2: Identify a TLS handshake where weak hashing is used (e.g., MD5 or SHA-1 for handshake hash). Step 3: Use a hash collision tool like SHAttered or fastcoll to create two different sets of handshake data (e.g., two server certificates or key exchange payloads) that generate the same MD5 or SHA-1 hash. Step 4: The attacker then substitutes the malicious payload with a colliding version, while maintaining the same handshake hash. Step 5: The server signs or verifies the handshake hash, which validates both benign and malicious versions. Step 6: The client or server accepts a forged or malicious certificate/key due to hash collision. Step 7: This can lead to trusted connection hijacking or impersonation. Step 8: TLS 1.3 mitigates this by using modern hash functions and strict structure validation.
- **Detection**: Analyze TLS handshake traffic for weak hash use; enable strict TLS audits
- **Solution**: Upgrade to TLS 1.3; disable weak ciphers/hashes in TLS configs; enforce SHA-256+ in handshake negotiations
- **Tags**: TLS Handshake, Hash Collision, Certificate Impersonation

## Checksum Collisions (ZIP/RAR)

- **Attack Type**: File Integrity Bypass via Archive Checksum
- **Target**: ZIP/RAR Archives
- **Vulnerability**: Weak checksums (e.g., CRC32) used as validators
- **MITRE**: T1565 – File or Directory Manipulation
- **Impact**: Malware smuggling, mod distribution hijack
- **Tools**: 7-Zip, WinRAR, zipcrc, collide, Hex editor
- **Scenario**: Attackers create two archive files (ZIP/RAR) with the same CRC32 or weak hash, but different content. This tricks systems relying only on checksums for file integrity (e.g., mod distribution, anti-virus exceptions).
- **Attack Steps**: Step 1: Understand that ZIP files use CRC32, a 32-bit checksum, which is not cryptographically secure. Step 2: Use tools like zipcrc or collide to generate two ZIPs (archive1.zip, archive2.zip) with different content but same CRC. Step 3: One archive contains a clean file (readme.txt), and the other contains malware with the same file name. Step 4: Validate both archives with tools like 7-Zip or antivirus — they report identical checksums. Step 5: Submit archive1.zip for whitelisting or pass it through security gates. Step 6: Later swap in archive2.zip, which bypasses checks due to matching checksum. Step 7: Attackers often use this technique for mod files, installers, or to fool users into executing malicious versions. Step 8: Always use SHA-256+ or digital signatures for file verification.
- **Detection**: Check for same checksums but different binary data; compare with SHA-256
- **Solution**: Never trust CRC32 for validation; enforce hash-based and signed validation of archives
- **Tags**: CRC32 Collision, Archive Bypass, ZIP Malware Injection

## Software Integrity Checks Bypass

- **Attack Type**: Binary Tampering that Bypasses Hash Check
- **Target**: Installers, Firmware, EXEs
- **Vulnerability**: Poor integrity checks, weak hash algorithms
- **MITRE**: T1600 – Binary Subversion
- **Impact**: Backdoor insertion, persistent malware injection
- **Tools**: PE Bear, HashCalc, Hex Editor, Binwalk
- **Scenario**: Attackers modify software binaries or update files without changing their hash (via collision or padding) to bypass integrity checks (e.g., in insecure update mechanisms or runtime verifications).
- **Attack Steps**: Step 1: Obtain a software binary or update file that performs integrity verification using a hash (e.g., MD5/SHA-1 printed in manifest or installer). Step 2: Reverse-engineer or analyze the structure to identify non-hashed regions or padding areas. Step 3: Insert payloads or malicious code into these slack regions, preserving the file size and hash. Step 4: Use tools like Hex Editor or Binwalk to reassemble the binary. Step 5: Recalculate the checksum — if designed improperly, it may remain unchanged. Step 6: The system or user trusts the binary due to matched checksum, even though the logic was altered. Step 7: This is common in embedded devices or legacy Windows software with MD5/SHA-1 checks. Step 8: Validate by running the software and confirming the payload executes despite integrity check success. Step 9: Defenders must hash the full binary and use secure, signed update mechanisms.
- **Detection**: Compare entire binary using secure hash; detect slack space injection
- **Solution**: Use secure boot, digital signing of updates, and validate binary sections cryptographically
- **Tags**: Hash Bypass, Binary Injection, Integrity Check Exploit

## Anti-Virus Signature Collision

- **Attack Type**: AV Evasion by Signature Matching Collision
- **Target**: Antivirus Systems
- **Vulnerability**: Static hash or byte-pattern based AV engines
- **MITRE**: T1204 – Malicious File Execution
- **Impact**: Malware execution without AV detection
- **Tools**: PEStudio, AVScan diffing, Hex editors, Obfuscation tools
- **Scenario**: Attackers craft malware with a payload that avoids detection by mimicking benign files that share the same anti-virus signature hash or byte pattern. This exploits simple AVs relying only on signatures.
- **Attack Steps**: Step 1: Download a known clean executable or document file that is not flagged by anti-virus (e.g., Notepad.exe). Step 2: Use PEStudio or a hex editor to extract the AV signature portion used (e.g., common byte patterns, headers). Step 3: Modify a malware payload so that its critical bytes or header mimic the clean file’s known signature. Use obfuscation or junk code to maintain structure while avoiding detection. Step 4: Save the payload and scan it through common AVs like Windows Defender or ClamAV. Step 5: If the signature matches the clean file’s hash or static signature, the AV will allow it. Step 6: You can refine this by using polymorphic tools or tools that manipulate entropy. Step 7: This is often used in phishing attachments, cracked software, and malware loaders. Step 8: AVs that rely only on static matching are easily bypassed this way. Step 9: Defenders must use behavioral analysis, sandboxing, and heuristic scanning.
- **Detection**: Use dynamic analysis (sandbox), check runtime behavior; compare file entropy and modification timestamps
- **Solution**: Upgrade to behavioral AVs, use YARA + heuristic scanning, and AI-based anomaly detectors
- **Tags**: AV Signature Collision, Malware Evasion, Obfuscation

## Log File Manipulation

- **Attack Type**: Tampering with Logged Events or Signatures
- **Target**: Log Files, App Logs, Audit Trails
- **Vulnerability**: Lack of log file integrity control
- **MITRE**: T1565 – Stored Data Manipulation
- **Impact**: Covering tracks, forensic evasion
- **Tools**: Notepad++, Bash, Log Parser, HashCalc, HxD
- **Scenario**: Attackers modify or forge log files (e.g., access.log, audit.log) to hide malicious activity, replay commands, or confuse incident responders. If logs use weak hashes or none, they can be rewritten undetected.
- **Attack Steps**: Step 1: Identify a system or app that generates log files but does not apply digital signatures, HMAC, or tamper-proof hashing to logs (e.g., /var/log/auth.log, C:\logs\access.txt). Step 2: Gain access to the machine or container (e.g., post-exploitation, insider). Step 3: Open the log file in a text editor (like Notepad++ or Vim) and remove, edit, or insert entries — for example, remove "Failed SSH login" or replace IPs. Step 4: If the log system calculates a checksum (e.g., MD5), recalculate the checksum using md5sum or HashCalc and overwrite the recorded hash (if stored with the log). Step 5: Save the modified file. Step 6: Security tools or auditors reviewing the log will not notice the tampering if no secure logging is enforced. Step 7: You can also insert fake entries to frame others or divert forensic teams. Step 8: Always detect tampering via cryptographic HMACs, digital signatures, or secure logging pipelines (e.g., syslog with TLS, Wazuh).
- **Detection**: Use File Integrity Monitoring (FIM); check hashes, log timestamps, and anomalies
- **Solution**: Use append-only logging; sign logs with HMAC-SHA256; use SIEM tools with secure transfer
- **Tags**: Log Tampering, Forensic Evasion, File Integrity

## Signed PDF Attack

- **Attack Type**: Document Hash Collision and Digital Signature
- **Target**: PDF Files, Digitally Signed Docs
- **Vulnerability**: Hash-based digital signatures using weak hash
- **MITRE**: T1600 – Signature Forgery
- **Impact**: Misleading contracts, invoice fraud, identity abuse
- **Tools**: PDF Tools (Hex Editor, PoC), Hashclash, qpdf, PDFtk
- **Scenario**: Exploit the fact that signed documents use a hash of the file. Attackers generate two PDFs with same hash: one clean (signed), and one malicious — tricking users into trusting unsigned content.
- **Attack Steps**: Step 1: Understand that PDF digital signatures typically sign a hash of the file’s binary data (not the visible text). Step 2: Use hashclash or custom scripts to craft two PDF files that produce the same MD5 or SHA-1 hash. File A looks harmless, File B is malicious. Step 3: Submit File A to a CA or authority for signing (e.g., digital sign with Adobe Acrobat or a smart card). Step 4: Receive the signed version of File A. Step 5: Now replace File A with File B — the hash is the same, so the signature still validates. Step 6: When someone opens File B, it shows malicious content (e.g., altered invoice, instructions). Step 7: This exploits weak signature policies based on MD5/SHA-1. Step 8: Demonstrated in PDF Signature Collision Attack (PDFEx). Step 9: Users must verify PDF signature policies and use SHA-256+.
- **Detection**: Verify signature algorithms in signed PDFs (check for MD5); compare visual vs. signed layer
- **Solution**: Use SHA-256 or stronger in document signing; embed content sealing; use visual diff tools to verify signed PDFs
- **Tags**: PDF Collision, Digital Signature Forgery, PDFEx

## Malware with Same Hash as Clean File

- **Attack Type**: File Hash Collision / AV Evasion
- **Target**: AVs, File Whitelisting Systems
- **Vulnerability**: Use of weak hash (MD5) for trusted lists
- **MITRE**: T1204 – Malicious File Execution
- **Impact**: Execute malware with AV/EDR evasion
- **Tools**: Hashclash, fastcoll, PEStudio, AV tools
- **Scenario**: Attackers create malware that shares the same MD5 hash as a clean file. Used to bypass antivirus, whitelisting systems, or hash-based file approval tools.
- **Attack Steps**: Step 1: Choose a clean file that is trusted in an environment — e.g., notepad.exe, update.dll. Step 2: Use fastcoll or hashclash to generate two files with same MD5: one clean (fileA.exe) and one malicious (fileB.exe) with a payload. Step 3: Submit the clean file’s hash to a whitelist tool or allow it in endpoint protection. Step 4: Replace the file later with the malicious twin that has the same hash. Step 5: System treats the malicious version as safe due to identical hash. Step 6: You can now execute malware with AV bypass. Step 7: This is possible only with weak hashes like MD5. Step 8: Validate both files with SHA-256 or behavior monitoring to reveal tampering.
- **Detection**: Hash comparison with SHA-256; monitor file entropy and behavior
- **Solution**: Avoid MD5/SHA-1; use SHA-256 or digital signing; enforce behavioral scanning
- **Tags**: Hash Collision, Whitelist Evasion, Malware Stealth

## Torrent File Spoofing

- **Attack Type**: Hash Collision in Torrent Info Hash
- **Target**: BitTorrent Clients, P2P Systems
- **Vulnerability**: SHA-1 collisions in torrent infohash
- **MITRE**: T1584 – Content Poisoning
- **Impact**: Malware distribution, media spoofing
- **Tools**: mktorrent, btih tools, torrentforge
- **Scenario**: Torrents rely on infohash (a SHA1 of the .torrent metadata). Attackers create two torrents with same hash but different payloads — users download harmful content while expecting legitimate files.
- **Attack Steps**: Step 1: Understand that a .torrent file includes metadata (e.g., filename, length, piece hashes) hashed into a SHA-1 infohash (used for identification). Step 2: Use a SHA-1 collision attack tool (e.g., hashclash) to craft two .torrent files with same infohash. File A points to legitimate content, File B to malware. Step 3: Share File A with the public and register it on a torrent tracker. Step 4: Peers connect and verify it using infohash. Step 5: Later, attacker seeds File B under the same infohash. Step 6: Users download the torrent, but data comes from malicious seeder with same hash. Step 7: This leads to payload swap or content poisoning. Step 8: Mitigated in BitTorrent v2 which uses SHA-256.
- **Detection**: Verify torrent content with multiple seeders; inspect file hash before use
- **Solution**: Use BitTorrent v2; verify full file hashes before execution; ban known malicious seeders
- **Tags**: Torrent Spoofing, SHA-1 Collision, P2P Attack

## Session Token Collision

- **Attack Type**: Predictable Token or Hash Collision
- **Target**: Web App Sessions
- **Vulnerability**: Weak or predictable session token generation
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Session hijacking, unauthorized access
- **Tools**: Burp Suite, Curl, Hashcat, Python
- **Scenario**: Web apps often assign users session tokens after login. If the token is derived from weak PRNGs or uses MD5/SHA-1 hashes, attackers may generate or guess a token that collides with a valid user’s token.
- **Attack Steps**: Step 1: Find a website that uses token-based sessions (e.g., via cookies or bearer tokens in headers) and does not use strong randomness. Step 2: Register multiple accounts and compare issued tokens (e.g., session=abc123, session=abc124). Step 3: Analyze token structure — see if it's base64, hex, or UUID. Decode base64 to check if user info or timestamps are used. Step 4: If tokens are based on predictable patterns or weak hashes (e.g., MD5 of userID + time), write a script to brute-force or generate similar tokens. Step 5: Try guessed tokens by setting session cookie and accessing user pages. Step 6: If token matches another user's session, you gain unauthorized access. Step 7: This attack is silent and often works against poorly designed auth systems or legacy PHP apps. Step 8: Always use cryptographically secure, random tokens (e.g., 256-bit generated via OpenSSL).
- **Detection**: Monitor token issuance pattern, detect token reuse or time-aligned collisions
- **Solution**: Use secure, unguessable tokens (UUIDv4, 256-bit); avoid MD5/SHA-1; set short expiry with IP/device binding
- **Tags**: Session Hijack, Token Collision, Predictable ID

## JWT ID Collision via HS256

- **Attack Type**: JWT Secret Collision / Forged Token
- **Target**: JWT-based Auth Systems
- **Vulnerability**: Weak JWT secret in HMAC-based tokens
- **MITRE**: T1606 – Forge Web Token
- **Impact**: Privilege escalation, impersonation
- **Tools**: jwt_tool.py, Burp Suite, Hydra, Hashcat
- **Scenario**: JWT tokens signed using HS256 (HMAC + SHA-256) are vulnerable if the secret key is weak or guessable. Attackers forge tokens with valid signatures by brute-forcing the HMAC secret or finding collisions.
- **Attack Steps**: Step 1: Identify a web app that uses JWTs (check for Authorization: Bearer eyJ... headers or jwt cookies). Step 2: Decode JWT using tools like jwt.io or jwt_tool.py to inspect the payload. Step 3: Check the algorithm in header — if it’s HS256, the same secret signs and verifies the token. Step 4: Use a dictionary or brute-force tool like jwt_tool.py -C -d wordlist.txt to find the secret (common values: admin, secret, 123456). Step 5: Once secret is found, modify payload (e.g., change "role":"user" to "role":"admin") and re-sign the token using the discovered key. Step 6: Use this forged token in Authorization header and access admin APIs or dashboards. Step 7: If signature matches, server accepts it as valid. Step 8: This attack is silent and fast against weak JWT secrets. Step 9: Always use asymmetric signing (RS256) or a very strong HMAC key.
- **Detection**: Monitor JWT structure; validate token source and check for key leakage or replay attempts
- **Solution**: Use RS256 asymmetric signing; enforce key rotation; apply short TTL to tokens and validate issuer/audience claims
- **Tags**: JWT Attack, HS256 Collision, HMAC Forgery

## Challenge–Response Protocol Collision

- **Attack Type**: Hash Collision in Auth Challenge-Response
- **Target**: NTLM, FTP, HTTP Auth
- **Vulnerability**: Hash-based challenge response with weak hash
- **MITRE**: T1557 – Adversary in the Middle
- **Impact**: Authentication bypass, lateral movement
- **Tools**: Responder, Hashcat, Python Scripts
- **Scenario**: Some protocols (e.g., NTLM, legacy FTP) rely on hashing a challenge string with a secret. If attackers find two different responses that hash the same (collision), they can bypass authentication.
- **Attack Steps**: Step 1: Identify a system using challenge-response authentication (e.g., NTLM auth in Windows, FTP login). Step 2: Capture a challenge string and corresponding user response (e.g., via packet capture using Wireshark or tools like Responder). Step 3: Analyze the hash function used — common ones include MD4, MD5, SHA-1. Step 4: Using collision generation tools (fastcoll, hashclash), craft an alternative response that hashes to the same value as the legitimate one. Step 5: Send the crafted challenge+response to the server as if you were the user. Step 6: If successful, the server authenticates you without needing the original password. Step 7: This type of attack works best when weak hash algorithms are used and there is no binding to session ID or timestamp. Step 8: For real-world use, red teamers may chain this with SMB relay attacks.
- **Detection**: Log challenge-response hashes and correlate with source IP/device; analyze failed login hash structure
- **Solution**: Use salted, timestamp-bound responses; migrate to Kerberos or TLS-mutual auth; enforce modern cryptographic protocols
- **Tags**: Auth Collision, Legacy Protocol Abuse, NTLM Hash Spoofing

## SSO Token Forgery via Collision

- **Attack Type**: SSO Assertion Hash Collision
- **Target**: SSO Systems (SAML, OAuth2)
- **Vulnerability**: Weak digital signature validation in SSO
- **MITRE**: T1552 – Unsecured Credentials
- **Impact**: Full user impersonation, privilege escalation
- **Tools**: SAML Tracer, Burp Suite, XMLSecTool, jwt_tool.py
- **Scenario**: In SAML or OAuth2 systems, attackers forge an assertion/token that matches the same digest/hash as a valid one, exploiting insecure signing or weak keys to impersonate a user.
- **Attack Steps**: Step 1: Identify a web app or cloud platform using SSO (Single Sign-On) with SAML or OAuth2 JWT tokens. Step 2: Intercept the SAML assertion or JWT token during login using tools like Burp Suite or SAML Tracer. Step 3: Analyze the signature method in the SSO token (e.g., SHA-1 digest or alg: HS256). Step 4: If signature is weak, forge a token with altered claims (e.g., change "email":"attacker@example.com" to "admin@domain.com") and re-sign it using guessed or brute-forced key (HS256) or using hash collision (SAML). Step 5: Send this forged token during login to the relying party (RP). Step 6: If signature validates due to key reuse, weak hash, or absence of signature verification, access is granted as a different user. Step 7: Attackers can pivot to cloud resources, billing, or admin panels. Step 8: Prevent by enforcing asymmetric signatures and proper key validation.
- **Detection**: Audit SSO token signatures; validate issuer and audience fields; enforce certificate pinning
- **Solution**: Enforce asymmetric signing (RSA/DSA); rotate keys regularly; use OAuth2.1+ or SAML2 with strict schema checks
- **Tags**: SSO Bypass, SAML JWT Forgery, Token Replay

## Primary Key Hash Collision

- **Attack Type**: Hash Collision in DB Indexing
- **Target**: NoSQL DBs, Key-Value Stores
- **Vulnerability**: Use of weak hashes as key/index
- **MITRE**: T1555 – Data Manipulation
- **Impact**: Data corruption, lookup errors, denial of access
- **Tools**: Python, MongoDB, Redis, Hashcat
- **Scenario**: Databases or key-value stores using hash-based primary keys (e.g., MD5(key)) may suffer from collision-based overwrites or lookup errors if two keys hash to the same value.
- **Attack Steps**: Step 1: Identify a database that stores or indexes records based on a hash of the primary key — common in NoSQL (e.g., MongoDB _id derived from hash(email), or Redis with hash(username)). Step 2: Determine the hash algorithm used — e.g., MD5, SHA1. Often documented or inferred from code. Step 3: Use a hash collision generator (fastcoll, hashclash) to create two different inputs that produce the same hash (e.g., two usernames that collide under MD5). Step 4: Insert both records into the DB. Step 5: Depending on the DB behavior, one record may overwrite the other, or insertion may be rejected with a duplicate key error. Step 6: You can use this to suppress legitimate records or trick lookups (e.g., login or file retrieval). Step 7: This attack is especially dangerous in distributed hash-based stores. Step 8: Prevent by salting keys or using collision-resistant hashes like SHA-256.
- **Detection**: Monitor insert logs for unexpected duplicates; hash collision scanning
- **Solution**: Avoid MD5/SHA-1 for key derivation; use UUIDs or random IDs; validate insert uniqueness beyond hashes
- **Tags**: Hash Collision, Database Integrity, Key Index Overlap

## User ID or File ID Collision

- **Attack Type**: Identity or Resource Misrouting via Collision
- **Target**: Web Apps, Cloud APIs
- **Vulnerability**: ID derivation via unsalted hash
- **MITRE**: T1595 – Exploit Application IDs
- **Impact**: Access confusion, impersonation, data loss
- **Tools**: Python, curl, Burp Suite, Hash calculators
- **Scenario**: Applications that assign IDs via a hash (e.g., user_id = md5(email)) may allow two different users or files to receive the same ID — leading to impersonation or overwriting files or access controls.
- **Attack Steps**: Step 1: Identify an application that generates user IDs or file IDs using a hash (e.g., file_id = sha1(file_name), user_id = md5(email)). Step 2: Register multiple accounts or upload files and observe their ID format in URLs or API. Step 3: Create two inputs that hash to the same ID using hashclash or fastcoll. For example, two different filenames that hash to same value. Step 4: Upload the second file or register second user with a colliding ID. Step 5: Server may treat it as the same user or overwrite the previous file. Step 6: Now access the resource or impersonate the first user using that ID. Step 7: Very effective in weakly validated storage systems or older APIs. Step 8: Always combine user data with salt/randomness before hashing to avoid collisions.
- **Detection**: Check logs for unexpected ID duplicates; implement collision-resistant auditing
- **Solution**: Use UUIDs instead of hashes for IDs; apply per-user salts when hashing
- **Tags**: Identity Spoofing, File Hijack, Resource Collision

## Email or Message Spoofing via Signed Content

- **Attack Type**: Signature Collision on Emails or Messages
- **Target**: Email Systems, Messaging Apps
- **Vulnerability**: Use of collision-prone hashes in signatures
- **MITRE**: T1585 – Spoof Signed Messages
- **Impact**: Phishing, malware delivery, fake commands
- **Tools**: GPG, DKIM Inspector, fastcoll
- **Scenario**: Digital signature schemes like DKIM or PGP can be tricked if a hash collision allows an attacker to replace a signed message with malicious content without invalidating the signature.
- **Attack Steps**: Step 1: Learn how digital signatures in messages work (e.g., DKIM for emails, PGP for files). They usually compute a hash of the message and then sign the hash. Step 2: Use hash collision tools (fastcoll) to craft two different messages with the same hash — one benign and one malicious. Step 3: Get the benign message signed by a trusted key (e.g., DKIM from a domain). Step 4: Replace the benign message with the malicious one that has the same hash. Step 5: Deliver the forged message via email or API. Step 6: The signature remains valid (hash matches), even though the message was altered. Step 7: Recipients trust the message due to valid signature. Step 8: Always use SHA-256+ and canonicalization to prevent such attacks.
- **Detection**: Use DKIM verification tools; validate hash canonicalization; alert on suspicious identical hash/mail pairs
- **Solution**: Avoid MD5/SHA1 in digital signatures; use SHA-256+; verify email headers and body match expectations
- **Tags**: Signed Email Spoofing, DKIM Collision, Message Injection

## NFT or Smart Contract Data Collision

- **Attack Type**: Hash Collision in Token Metadata or Art Reference
- **Target**: NFT Platforms, IPFS
- **Vulnerability**: Hash-based metadata linking using weak hash
- **MITRE**: T1586 – Content Forgery via Hash
- **Impact**: Buyer fraud, image spoofing, NFT brand damage
- **Tools**: IPFS, Solidity, OpenZeppelin, hashclash
- **Scenario**: In NFT ecosystems, the metadata (e.g., image, name, description) is hashed and linked to the token. Attackers can craft two sets of metadata that hash to same value — tricking systems into treating both as the same token.
- **Attack Steps**: Step 1: Explore an NFT platform that uses IPFS or hash links for referencing token metadata. Many minting contracts link tokens to ipfs://hash. Step 2: Use a collision generation tool (e.g., hashclash) to create two different JSON metadata files (or even images) that hash to the same value under SHA-1 (or MD5). Step 3: Submit the clean version to the platform, and mint an NFT referencing it. Step 4: After token is minted, replace the metadata with the malicious version (e.g., a different image, obscene content). Step 5: When the NFT is viewed, it loads the malicious content despite referencing the same hash. Step 6: Attackers can mislead buyers or spoof ownership. Step 7: Always use SHA-256 or content pinning (immutable references) in NFT contracts.
- **Detection**: Check IPFS object hash vs actual content; monitor for double-pinned content under same hash
- **Solution**: Use SHA-256 and enforce content immutability; verify metadata on-chain or via external validation
- **Tags**: NFT Metadata Forgery, Hash Collision, Web3 Abuse

## Transaction History Spoofing

- **Attack Type**: Collision in Hash-Chained Logs
- **Target**: Blockchain, Ledger Systems
- **Vulnerability**: Hash chaining without tamper detection
- **MITRE**: T1600 – Audit Trail Tampering
- **Impact**: Financial spoofing, double-spend cover-up
- **Tools**: Custom Chain Tools, Hashclash, Blockchain Viewer
- **Scenario**: Some blockchains or internal ledgers link transactions using hash chains. If attackers cause hash collisions, they may replace or hide transactions while keeping the chain valid.
- **Attack Steps**: Step 1: Identify a blockchain, distributed ledger, or audit log system that uses hashes to link transactions or entries (e.g., hash(transaction 1) → transaction 2). Step 2: Determine hash function used — if MD5/SHA1, it's vulnerable. Step 3: Use hash collision tools to generate two different transactions with the same hash (e.g., transaction content A and B). Step 4: Submit the clean version (A) and allow it to be hashed and stored. Step 5: Later, replace the block or log file with the malicious version (B) that produces the same hash. Step 6: The hash chain remains intact, but data is altered. Step 7: This can spoof balances, transactions, or audit trails. Step 8: Prevent by using secure hash functions and including signatures or Merkle proofs.
- **Detection**: Use Merkle proofs; validate chain hash integrity at multiple points; perform periodic audits
- **Solution**: Use SHA-256+ or Merkle trees; sign blocks cryptographically; store checkpoints off-chain
- **Tags**: Ledger Spoofing, Hash Chain Tampering, Blockchain Collision

## Offline Password Cracking (Local DB)

- **Attack Type**: Rainbow Table Hash Lookup
- **Target**: Linux Servers, Local DBs
- **Vulnerability**: Unsalted or weak password hashing
- **MITRE**: T1110 – Brute Force
- **Impact**: Full account compromise, lateral movement
- **Tools**: RainbowCrack, Hashcat, John the Ripper
- **Scenario**: Hashes dumped from password databases (e.g., /etc/shadow on Linux) can be cracked offline using pre-computed rainbow tables.
- **Attack Steps**: Step 1: Gain access to a system and dump the password hash database (e.g., /etc/shadow on Linux). Use cat /etc/shadow or copy the file if you have root access. Step 2: Identify the hashing algorithm used (e.g., MD5, SHA-512, bcrypt). You can usually tell by the prefix: $1$ for MD5, $6$ for SHA-512. Step 3: Install or use rainbow table tools like RainbowCrack. Download relevant rainbow tables (e.g., MD5_hashes.rti/rainbow) or generate custom tables using rtgen. Step 4: Use rcrack to look up the dumped hash in the precomputed rainbow tables: rcrack . -h <hash>. Step 5: If the hash is present in the table, the original password is revealed. Step 6: You can also try tools like John the Ripper with --format set to match the hash type. Step 7: This attack is effective against unsalted or weakly hashed password dumps. Step 8: Protect by using strong hashing like bcrypt, with unique salts.
- **Detection**: Monitor for unusual hash lookups, detect shadow file access
- **Solution**: Use salted hashing (e.g., bcrypt, scrypt); deny read access to sensitive files; rotate credentials regularly
- **Tags**: Rainbow Tables, Password Crack, Shadow File

## Cracking Windows SAM Hashes

- **Attack Type**: Offline Rainbow Table Lookup on SAM
- **Target**: Windows Systems, User Accounts
- **Vulnerability**: Weak NTLM hash without salt
- **MITRE**: T1003 – OS Credential Dumping
- **Impact**: Unauthorized system access, privilege escalation
- **Tools**: Cain & Abel, pwdump7, RainbowCrack, OphCrack
- **Scenario**: NTLM password hashes extracted from Windows SAM files can be matched against rainbow tables to reveal plaintext passwords.
- **Attack Steps**: Step 1: Extract SAM file and SYSTEM hive from a Windows machine. This can be done using tools like pwdump7 or by copying from C:\Windows\System32\Config\SAM and SYSTEM. Step 2: Decrypt the hashes using the SYSTEM hive key. Use Cain & Abel or pwdump to obtain the NTLM hashes. Step 3: Download or generate rainbow tables targeting NTLM hashes. Common ones include "XP free fast" tables or custom NTLMv1 sets. Step 4: Run rcrack . -h <hash> to match the NTLM hash against your table. Step 5: If the hash exists in the rainbow table, the cleartext password will be revealed. Step 6: Tools like OphCrack provide GUI-based lookup using pre-built tables. Step 7: This method is highly effective against weak or reused passwords. Step 8: Use salted hash schemes like Kerberos or strong account lockout policies to mitigate.
- **Detection**: Log NTLM hash access; alert on SAM hive extraction
- **Solution**: Use Kerberos authentication; disable NTLM; enable Credential Guard and LSA protection
- **Tags**: NTLM, Windows Hash Crack, SAM Dump

## Cracking WordPress User Hashes

- **Attack Type**: MySQL Table Password Hash Rainbow Lookup
- **Target**: WordPress Sites, MySQL Databases
- **Vulnerability**: Unsalted MD5 hash for user passwords
- **MITRE**: T1555 – Credential Extraction
- **Impact**: WordPress admin access, full site control
- **Tools**: PhpMyAdmin, Hashcat, John, RainbowCrack
- **Scenario**: WordPress stores MD5 hashes in the wp_users table. These can be cracked using rainbow tables if the hash is unsalted.
- **Attack Steps**: Step 1: Dump the WordPress database using mysqldump, phpMyAdmin, or access wp_users table via SQL injection or admin panel. Step 2: Locate the user_pass field — it stores the hashed password, typically in MD5 format. Step 3: Copy the MD5 hash and search it in online hash databases (e.g., CrackStation) or use rainbow tables locally. Step 4: Download MD5 rainbow tables or generate custom ones with rtgen. Step 5: Use rcrack . -h <hash> to lookup the hash. Step 6: If the password exists in the table (e.g., 123456), it is cracked. Step 7: You can also try john --format=raw-md5 hash.txt. Step 8: Prevent this attack by upgrading to stronger hashing (e.g., bcrypt) using plugins or WordPress functions like wp_hash_password().
- **Detection**: Monitor for DB dump access; alert on sudden multiple user login failures
- **Solution**: Use bcrypt hashing via wp_hash_password(); add salts; restrict DB access
- **Tags**: WordPress, MD5, User Table, Rainbow Crack

## Router Admin Login Cracking

- **Attack Type**: Firmware/Config Hash Crack via Rainbow
- **Target**: Embedded Devices, Routers
- **Vulnerability**: Weak hash in firmware or config
- **MITRE**: T1027 – Obfuscated Files or Info
- **Impact**: Full device takeover, network compromise
- **Tools**: Binwalk, Hashcat, Firmware Mod Kit, RainbowCrack
- **Scenario**: Many routers store hashed admin passwords in firmware or config dumps. These hashes can be cracked offline using rainbow tables if weak algorithms like MD5 are used.
- **Attack Steps**: Step 1: Download router firmware (from manufacturer site or device). Use binwalk to extract file system. Look for config files or /etc/passwd, /etc/shadow equivalents. Step 2: Identify the hash type (e.g., MD5). Tools like file or hash-identifier can help. Step 3: Extract the admin hash and run against rainbow tables using rcrack. Step 4: Generate or download router-specific rainbow tables (some use truncated MD5 or base64 versions). Step 5: If cracked, the password provides full access to web UI or telnet/SSH. Step 6: Test the password by logging into the router. Step 7: For modern devices, try known default passwords as well. Step 8: Prevent by setting complex admin credentials and disabling remote config access.
- **Detection**: Monitor firmware extraction or config download
- **Solution**: Use SHA-256+ hashes with salt; rotate passwords; encrypt stored configs
- **Tags**: IoT, Router Firmware, Admin Crack

## SSH Key Passphrase Hash Cracking

- **Attack Type**: Brute/Rainbow Attack on SSH Key Passphrase
- **Target**: Private SSH Keys
- **Vulnerability**: Weak passphrase or old key encryption format
- **MITRE**: T1552 – Unprotected Credentials
- **Impact**: Remote system access, lateral movement
- **Tools**: ssh2john, John the Ripper, Hashcat, RainbowCrack
- **Scenario**: SSH private keys often use passphrase protection. The encrypted key blob can be attacked using rainbow tables if old key formats or weak encryption is used.
- **Attack Steps**: Step 1: Obtain the private SSH key file (e.g., id_rsa) from target user or server. Use physical access, misconfigured server, or backup dumps. Step 2: Convert the key to a crackable hash using ssh2john: ssh2john id_rsa > hash.txt. Step 3: Load the hash into John the Ripper: john hash.txt --wordlist=rockyou.txt. Step 4: Alternatively, use rainbow tables designed for passphrase hashes if available. These are rarer but can be generated using rtgen with the correct format. Step 5: If cracked, you now have the passphrase to decrypt the SSH key and login to remote servers. Step 6: Attempt login using ssh -i id_rsa user@host. Step 7: Prevent by using strong, unique passphrases and storing keys securely with hardware tokens.
- **Detection**: Alert on unauthorized SSH key uploads or access attempts
- **Solution**: Use modern key formats (ed25519), encrypt keys with strong passphrase; store keys in hardware (YubiKey)
- **Tags**: SSH, Private Key, Rainbow Tables, Key Crack

## Data Breach Dump Decoding

- **Attack Type**: Password Hash Cracking via Rainbow Table
- **Target**: Email-Password Dumps
- **Vulnerability**: Unsalted hash in dumped credential data
- **MITRE**: T1555 – Credential Dumping
- **Impact**: Credential reuse, account takeover
- **Tools**: Hashcat, RainbowCrack, rockyou.txt
- **Scenario**: Leaked email-password hash dumps (e.g., LinkedIn, MySpace breaches) contain MD5/SHA1 hashes. Rainbow tables help decode them to recover original passwords.
- **Attack Steps**: Step 1: Download a public or purchased breach dump (e.g., from Pastebin or dark web leaks). These often contain email:hash combinations. Step 2: Identify the hash algorithm — most older breaches use MD5 or SHA1. Step 3: Use a hash identifier (e.g., hashid) to confirm format. Step 4: Download relevant rainbow tables (e.g., MD5_loweralpha_numeric.rti) from sites like Project RainbowCrack. Step 5: Use rcrack or hashcat -m <mode> with the hash list and rainbow table: rcrack ./tables/ -h <hash>. Step 6: If a match is found, the original password is revealed. Step 7: You can now test reused credentials on other services (credential stuffing). Step 8: Prevent by enforcing strong password policies and using hashing algorithms with salt (e.g., bcrypt).
- **Detection**: Monitor for leaked credentials on the dark web; track breached email login attempts
- **Solution**: Use salted bcrypt or Argon2; perform breach credential checks and reset flows
- **Tags**: Breach Analysis, Rainbow Crack, Credential Reuse

## JWT HMAC Cracking

- **Attack Type**: HMAC Secret Key Crack via Rainbow Table
- **Target**: JWT-based APIs
- **Vulnerability**: Weak HMAC key in token signing
- **MITRE**: T1606 – JWT Key Abuse
- **Impact**: Unauthorized API access, privilege escalation
- **Tools**: jwt_tool.py, jwt-cracker, RainbowCrack
- **Scenario**: JSON Web Tokens (JWT) signed using HMAC (e.g., HS256) with weak or short secrets can be cracked using rainbow tables, allowing attackers to forge valid tokens.
- **Attack Steps**: Step 1: Capture a JWT token (from headers like Authorization: Bearer <JWT>). JWTs have 3 parts: header, payload, signature. Step 2: Decode the JWT using jwt.io or jwt_tool.py to view the algorithm (e.g., HS256) and payload. Step 3: Attempt to guess the signing secret by using a dictionary of weak secrets or rainbow tables. Step 4: Use jwt_tool.py or jwt-cracker to run a rainbow lookup: jwt_tool.py -C -d <jwt> -S rainbow.txt. Step 5: If the HMAC secret is weak and in the table (e.g., admin123, secret), it will be recovered. Step 6: Now, generate a forged JWT with elevated privileges (e.g., change role: user to role: admin) and sign it with the cracked key. Step 7: Submit this forged token in API calls to gain unauthorized access. Step 8: Prevent by using long, random secrets and switching to asymmetric algorithms like RS256.
- **Detection**: Check for repeated JWT forgery attempts; validate key length and entropy
- **Solution**: Use RS256 instead of HS256; rotate secrets regularly; use at least 256-bit keys
- **Tags**: JWT, Token Forgery, Rainbow HMAC, Token Abuse

## API Key Guessing via Hashes

- **Attack Type**: Hashed API Key Cracking via Rainbow
- **Target**: API Gateways, Cloud Services
- **Vulnerability**: Weak hashed API keys in storage
- **MITRE**: T1557 – API Credential Abuse
- **Impact**: Unauthorized data access, quota abuse
- **Tools**: Hashcat, RainbowCrack, Burp Suite
- **Scenario**: If short API keys (e.g., 12345, dev_key) are hashed and stored insecurely, rainbow tables can reverse them, exposing the keys to attackers.
- **Attack Steps**: Step 1: Locate hashed API keys in application code, config files, database dumps, or API responses (some store hash(api_key) instead of plaintext). Step 2: Identify hash algorithm (commonly MD5, SHA-1). Step 3: Use a hash identifier to confirm. Step 4: Prepare or download rainbow tables matching that algorithm. Use rcrack . -h <api_key_hash> or hashcat -m 0 hashes.txt wordlist.txt. Step 5: If the API key is weak (like dev123, key123, test1234), it will match an entry in the rainbow table and be cracked. Step 6: Use the recovered API key to access protected endpoints, impersonate users, or leak data. Step 7: Prevent by storing API keys securely, using environment variables, and never exposing hashes or using weak keys.
- **Detection**: Monitor for abnormal API usage; alert on access from unknown IPs
- **Solution**: Do not hash API keys blindly; use secrets vaults; rate limit API key use; enforce strong key generation
- **Tags**: API Key Brute Force, Hash Reversal, Rainbow Crack

## Authentication Tokens Cracking

- **Attack Type**: Session Token Hash Rainbow Cracking
- **Target**: Web Apps, Mobile APIs
- **Vulnerability**: Predictable or hashed static tokens
- **MITRE**: T1078 – Valid Account Access
- **Impact**: Account hijacking, session replay
- **Tools**: Hashcat, rcrack, Wireshark, Burp Suite
- **Scenario**: Tokens such as auth_token=md5(username+timestamp) can be predicted or reversed via rainbow tables if the generation logic is weak or exposed.
- **Attack Steps**: Step 1: Intercept an authentication token from a browser or mobile app (e.g., using Burp Suite or inspecting network traffic via browser Dev Tools or Wireshark). Step 2: Analyze the token structure — many developers use token = hash(username + time) or similar logic. Step 3: Attempt to guess the token creation logic and reconstruct inputs (e.g., known usernames and approximate timestamp). Step 4: Hash combinations using the same hash function (MD5/SHA1) and match against the token. Step 5: Use hashcat or rcrack to look up common patterns in rainbow tables: rcrack ./ -h <auth_token>. Step 6: If successful, you now have a valid session token and can impersonate a user or reuse a session. Step 7: Some web apps may store hashed tokens in cookies or as headers. Use recovered token to replay session. Step 8: Prevent this by using securely generated, random, and time-expiring tokens with strong entropy.
- **Detection**: Use proper session token libraries; detect replayed tokens; check token structure at server level
- **Solution**: Avoid predictable tokens; use JWTs with expiration; use random UUID tokens
- **Tags**: Token Hijack, Session Replay, Rainbow Table Crack

## LM Hash Cracking (Windows XP/NT)

- **Attack Type**: Legacy LM Hash Rainbow Table Crack
- **Target**: Windows XP/NT Systems
- **Vulnerability**: LM hash design flaw, no salting
- **MITRE**: T1003 – OS Credential Dumping
- **Impact**: Full user account compromise
- **Tools**: OphCrack, RainbowCrack, Cain & Abel
- **Scenario**: LAN Manager (LM) hashes used in older Windows systems (XP/NT) are easily cracked using rainbow tables due to their insecure design (split into 7-char chunks, all uppercase, no salting).
- **Attack Steps**: Step 1: Extract LM hashes from the Windows SAM file using tools like Cain & Abel, pwdump, or samdump2. The LM hash is usually stored alongside NTLM hashes. Step 2: LM hashes split passwords into two 7-character chunks and convert them to uppercase, reducing entropy. Step 3: Download rainbow tables specifically for LM hashes — widely available online, often used in OphCrack. Step 4: Use OphCrack or rcrack to run the hash against the rainbow tables. For example: rcrack ./tables -h <lm_hash>. Step 5: The tool will match the hash and return the plaintext password. Step 6: These hashes are so weak that even strong-looking passwords are easily cracked. Step 7: Prevent by disabling LM hash storage via Group Policy and upgrading to systems using NTLMv2 or Kerberos.
- **Detection**: Alert on legacy SAM access; check for LM hash presence
- **Solution**: Disable LM hash generation (NoLMHash registry flag); migrate to modern Windows versions
- **Tags**: LM Hash, Windows XP, Rainbow Crack

## MD5-based Login Systems

- **Attack Type**: Password Hash Cracking via Rainbow
- **Target**: Web Apps, CMSes, Admin Panels
- **Vulnerability**: Weak hashing without salting
- **MITRE**: T1110 – Brute Force
- **Impact**: Account takeover, privilege escalation
- **Tools**: Hashcat, RainbowCrack, John the Ripper
- **Scenario**: Systems still storing passwords using unsalted MD5 (e.g., in login DBs or legacy CMS platforms) are vulnerable to dictionary or rainbow table attacks.
- **Attack Steps**: Step 1: Gain access to the login database (via dump, SQLi, or backup leak) containing MD5 password hashes. You’ll see a string like 5f4dcc3b5aa765d61d8327deb882cf99. Step 2: Use hashid or hash-identifier to confirm it’s an MD5 hash. Step 3: Download prebuilt MD5 rainbow tables or use a tool like CrackStation.net to lookup hashes online. Step 4: You can also use rcrack or hashcat -m 0 hashes.txt rockyou.txt to brute-force locally with a wordlist. Step 5: If the password is weak or reused, the tool will find a match. Step 6: Log into the target system using the recovered password. Step 7: Protect your apps by upgrading to SHA-256 with salt or bcrypt, and never use MD5 for password hashing.
- **Detection**: Monitor for unusual login attempts; alert on reused hashes
- **Solution**: Upgrade to bcrypt/Argon2; enforce strong password policies; audit legacy CMS software
- **Tags**: MD5, Login Bypass, CMS Crack

## SHA-1 Hashed Password Cracking

- **Attack Type**: Rainbow Crack for SHA-1 Password Hashes
- **Target**: Web Apps, Mobile DBs
- **Vulnerability**: Weak or unsalted SHA-1 storage
- **MITRE**: T1555 – Credential Extraction
- **Impact**: Full credential exposure, session hijacking
- **Tools**: Hashcat, RainbowCrack, CrackStation
- **Scenario**: SHA-1 is stronger than MD5 but still broken. Unsalted SHA-1 password hashes can be cracked via rainbow tables or precomputed lookup lists.
- **Attack Steps**: Step 1: Obtain the SHA-1 hash from a leaked database or memory dump (e.g., 5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8). Step 2: Use hashid to verify it’s SHA-1. Step 3: Check online rainbow table services like CrackStation or Hashes.org for a quick match. Step 4: For offline cracking, download SHA-1 rainbow tables (or generate using rtgen). Step 5: Use rcrack . -h <hash> or hashcat -m 100 for SHA-1. Step 6: If cracked, the original password is revealed. Step 7: Common SHA-1 password hashes (like password, admin) are often precomputed. Step 8: Prevent by using salted SHA-256/bcrypt and updating outdated storage mechanisms.
- **Detection**: Hash lookup detection; monitor for known breached password hashes
- **Solution**: Use salted SHA-256 or bcrypt; disallow SHA-1 in modern applications
- **Tags**: SHA-1, Rainbow Crack, Password Attack

## Cracking Captured Hashes from Network Traffic

- **Attack Type**: Rainbow/Dump Hash Crack from Wire Traffic
- **Target**: Enterprise LANs, Legacy Apps
- **Vulnerability**: Hashes sent in plaintext or weak protocols
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Credential theft, network lateral movement
- **Tools**: Wireshark, Hashcat, Responder, RainbowCrack
- **Scenario**: Some protocols (e.g., NTLM auth, FTP, HTTP Digest) transmit hash digests that can be captured using tools like Wireshark, and later cracked using rainbow tables or brute-force tools.
- **Attack Steps**: Step 1: Set up Wireshark or tcpdump to sniff network traffic between a client and a server. Look for protocols that transmit hashes — NTLM (Windows auth), HTTP Digest, or old FTP logins. Step 2: Capture the relevant authentication handshake or login response. In NTLM, you’ll find hashes inside NTLM_AUTHENTICATE_MESSAGE. Step 3: Extract the hash (e.g., NTLMv1 hash) from the pcap file. Step 4: Use Responder or Hashcat to process the capture and isolate the hash. Step 5: Use rcrack or hashcat with appropriate mode (e.g., -m 5500 for NetNTLMv1) and rainbow tables or wordlists. Step 6: If the password used during login is weak or common, it will be cracked quickly. Step 7: Use cracked credentials for lateral movement or privilege escalation. Step 8: Prevent this by using encrypted protocols (HTTPS, SMBv3, NTLMv2), avoiding hash exposure over the wire.
- **Detection**: Monitor for packet sniffing tools; detect NTLM/FTP plaintext transmission
- **Solution**: Disable legacy auth (NTLMv1, Digest); enforce TLS; encrypt internal traffic
- **Tags**: Network Sniffing, Hash Intercept, Rainbow Crack

## POP3/FTP/IMAP Hash Extraction

- **Attack Type**: Rainbow Table Crack from Legacy Protocols
- **Target**: Email Servers, FTP Hosts
- **Vulnerability**: Insecure auth over plaintext channels
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Credential leakage, unauthorized access
- **Tools**: Wireshark, Hashcat, Responder, RainbowCrack
- **Scenario**: Email and file transfer protocols like POP3, FTP, and IMAP often transmit credentials or challenge-response hashes over plaintext connections, which can be sniffed and cracked.
- **Attack Steps**: Step 1: Launch Wireshark or tcpdump on a network with email/file transfer traffic. Step 2: Filter traffic to capture protocols like POP3, IMAP, or FTP using filters like tcp.port == 110 (POP3). Step 3: Identify authentication handshakes — you'll often find USER and PASS or a base64-encoded login. Step 4: Extract the hash or credentials from the packet data. Step 5: If it's hashed (e.g., using MD5 challenge-response), isolate the hash and use Hashcat with the correct mode or rcrack and prebuilt rainbow tables. Step 6: For example, crack captured FTP MD5 hashes using: hashcat -m 500 ftp_hashes.txt rockyou.txt. Step 7: If cracked, reuse credentials for accessing email inboxes, FTP servers, or performing lateral movement. Step 8: Prevent this by enforcing encrypted protocols like FTPS, IMAPS, or STARTTLS.
- **Detection**: Detect unencrypted protocol usage on internal networks; monitor for sniffing tools
- **Solution**: Disable unencrypted POP3/IMAP/FTP; force TLS or encrypted tunnels
- **Tags**: FTP, IMAP, Rainbow Crack, Packet Sniffing

## Cracking Password Hashes on Stolen Devices

- **Attack Type**: Hash Dump Cracking from Device Storage
- **Target**: Stolen Desktops/Laptops
- **Vulnerability**: Hashes stored in plaintext or unencrypted state
- **MITRE**: T1552 – Credentials in Files
- **Impact**: Total compromise of system/user accounts
- **Tools**: FTK Imager, Hashcat, John the Ripper, rcrack
- **Scenario**: If an attacker steals a laptop or phone, they can extract hashed credentials from disk or memory dumps and use rainbow tables to recover passwords offline.
- **Attack Steps**: Step 1: Attacker gains physical access to a stolen laptop or desktop. Step 2: Boot into a live Linux distro (like Kali or Ubuntu) via USB and mount the system’s hard drive. Step 3: Locate credential stores (e.g., /etc/shadow on Linux, SAM on Windows). Step 4: Use tools like samdump2 or mimikatz to extract password hashes. Step 5: Identify the hash algorithm (e.g., MD5, NTLM, SHA1). Step 6: Download appropriate rainbow tables for those hashes. Step 7: Use rcrack or hashcat to perform the actual cracking. Step 8: Example: hashcat -m 1000 -a 0 hash.txt rockyou.txt for NTLM. Step 9: Once cracked, attacker can impersonate the original user, decrypt files, or access cloud-synced services. Step 10: Prevent by encrypting full disk (BitLocker, LUKS) and enforcing BIOS/boot passwords.
- **Detection**: Monitor for unauthorized disk access or stolen device reports
- **Solution**: Encrypt full disk; secure BIOS; enable remote wipe solutions; use biometric or hardware keys
- **Tags**: Physical Access, Rainbow Crack, Device Theft

## Browser or App Credential Storage Attacks

- **Attack Type**: Rainbow Crack on Local Password Storage
- **Target**: Web Browsers, Apps, Extensions
- **Vulnerability**: Poor credential storage or unsalted hashes
- **MITRE**: T1555 – Credential Dumping
- **Impact**: User account compromise across websites/apps
- **Tools**: Nirsoft Tools, SQLite Viewer, Hashcat, RainbowCrack
- **Scenario**: Many apps and browsers store login credentials or tokens locally — if these are hashed and weak, attackers can extract and crack them.
- **Attack Steps**: Step 1: Attacker gains access to the user's machine or backups (e.g., via stolen phone/laptop or malware). Step 2: Locate browser credential storage (e.g., Login Data in Chrome, a SQLite file). Step 3: Use tools like Nirsoft WebBrowserPassView or inspect SQLite DBs directly. Step 4: Some applications store credentials in custom formats or as hashes (e.g., MD5, SHA1). Step 5: Extract these hashes and determine the hashing algorithm. Step 6: Use rcrack with rainbow tables or hashcat to crack the stored values. Step 7: If credentials are cracked, attacker can access email, cloud accounts, admin panels. Step 8: Prevent by ensuring apps encrypt passwords at rest and browsers are locked with master passwords.
- **Detection**: Alert on unauthorized file or credential DB access
- **Solution**: Use encrypted credential storage (e.g., Keychain, Windows Vault); require device encryption
- **Tags**: Chrome, LocalStorage, Rainbow Tables, SQLite

## Custom App Auth System Bypass

- **Attack Type**: Brute Force or Rainbow Crack of Custom Hash Logic
- **Target**: Custom Web/Mobile Apps
- **Vulnerability**: Custom weak hash-based authentication
- **MITRE**: T1110 – Brute Force
- **Impact**: Full login bypass, elevation of privileges
- **Tools**: Burp Suite, Hashcat, jwt_tool.py, RainbowCrack
- **Scenario**: Apps with homemade or poorly implemented authentication may use weak hashes (e.g., MD5(password+username)), allowing brute force or rainbow attack bypasses.
- **Attack Steps**: Step 1: Identify that the app uses a non-standard or home-grown authentication system. This could be a custom hash scheme stored in DB or signed token with weak HMAC. Step 2: Capture how the app stores or transmits credentials/tokens — use Burp Suite to intercept login request or registration. Step 3: If a hashed password or token is sent, extract it. Step 4: Analyze the pattern — is it md5(user+pass) or just sha1(pass)? Predict structure. Step 5: Create a dictionary of common inputs using wordlists (rockyou.txt, usernames.txt). Step 6: Generate the same hash structure and compare with the intercepted ones. Step 7: Use rcrack or hashcat with custom rules to crack these hashes. Step 8: Use cracked values to forge login tokens or bypass checks. Step 9: Recommend not rolling your own crypto — use industry-tested libraries (bcrypt, Argon2).
- **Detection**: Log tampering with login structures or auth checks
- **Solution**: Use secure, salted password hashing; never roll custom crypto; validate token generation logic
- **Tags**: Weak Auth, Custom Hash, App Login Bypass

## Token Replay Attacks

- **Attack Type**: Predictable Token Brute Force or Replay
- **Target**: Web Applications, APIs
- **Vulnerability**: Weak tokens or predictable session IDs
- **MITRE**: T1070 – Indicator Removal
- **Impact**: Full session takeover, impersonation
- **Tools**: Burp Suite, Postman, Fiddler
- **Scenario**: Applications that use weak, non-expiring, or predictable tokens (session or auth) are vulnerable to replay attacks, allowing attackers to reuse them to impersonate users.
- **Attack Steps**: Step 1: Use Burp Suite or a browser’s developer tools to intercept authentication requests containing tokens (e.g., in cookies, headers like Authorization: Bearer <token>). Step 2: Observe the token pattern – is it base64, JWT, or a custom hash? Determine if it’s short, static, or repeated. Step 3: If the same token is reused across multiple requests or does not expire, it may be replayable. Step 4: Copy and reuse the token in Postman or curl to replicate the original session. Step 5: If the token is a JWT with weak secrets (e.g., “secret” or “admin123”), use jwt_tool.py or jwt-cracker to brute-force it and forge a valid one. Step 6: Reuse or replay the token to hijack the session and perform actions as the user. Step 7: Prevent by enforcing short-lived tokens, rotating secrets, binding tokens to IPs, and signing securely.
- **Detection**: Monitor for replayed tokens from different IPs; detect duplicate token use across sessions
- **Solution**: Use expiring, signed tokens; bind sessions to user/IP/device; log out users after token usage
- **Tags**: Session Hijack, Replay, Token Abuse

## Recon-Based Dictionary Personalization

- **Attack Type**: Targeted Dictionary Brute Force
- **Target**: Any Auth Interface (Login, API)
- **Vulnerability**: Human-generated predictable credentials
- **MITRE**: T1201 – Password Policy Bypass
- **Impact**: Faster credential compromise, social engineering aid
- **Tools**: Sherlock, theHarvester, CUPP, Burp Suite
- **Scenario**: Attackers enhance brute-force success by creating customized wordlists based on personal info like DOBs, pets, hobbies, usernames from public social profiles.
- **Attack Steps**: Step 1: Gather personal info of the target from public sources — social media (Facebook, LinkedIn), data breaches (HaveIBeenPwned), or public profiles. Use tools like Sherlock, theHarvester, or manual Google dorking. Step 2: Input the gathered data into CUPP (Common User Passwords Profiler) to generate a personalized dictionary. For example, pet name + birth year → Tommy1999. Step 3: Use this list with Hydra, Burp Intruder, or Hashcat to target login forms, hashes, or authentication APIs. Step 4: Because the list is based on real-world habits, success rates increase dramatically. Step 5: You can also augment rainbow tables with these custom entries to accelerate offline cracking. Step 6: Prevent this by enforcing password complexity and user awareness against oversharing.
- **Detection**: Alert on targeted brute-force attempts with low-volume patterns
- **Solution**: Enforce complex password policies; train users not to reuse names/DOBs; use MFA
- **Tags**: Dictionary, CUPP, Personal Info Crack

## Credential Stuffing Enhancement

- **Attack Type**: Optimized Credential Stuffing with Known Hashes
- **Target**: Cloud Services, Login Portals
- **Vulnerability**: Reused or leaked credentials
- **MITRE**: T1110.004 – Credential Stuffing
- **Impact**: Unauthorized account access, financial loss
- **Tools**: Sentry MBA, OpenBullet, Hashcat, Pastebin Dumps
- **Scenario**: Attackers use pre-cracked hash:password mappings (from past breaches) to speed up credential stuffing attacks against multiple targets or services.
- **Attack Steps**: Step 1: Attacker obtains a breached database with password hashes (e.g., from Pastebin or breached forums). Step 2: Use rainbow tables or previously cracked hash mappings to get plaintext passwords. Step 3: Combine email/username:password pairs into credential stuffing configs. Step 4: Use automated tools like Sentry MBA or OpenBullet to target login portals (e.g., Netflix, Gmail, Facebook) using known combos. Step 5: The tool automates login attempts and logs successful hits (called “hits” or “valids”). Step 6: Because hashes are already matched, the speed and stealth of attacks increase. Step 7: Prevent this via login rate limiting, anomaly detection, and 2FA enforcement. Step 8: Educate users to avoid reusing credentials across platforms.
- **Detection**: Monitor for rapid login attempts from many IPs; detect login anomalies
- **Solution**: Implement IP throttling, reCAPTCHA, 2FA; check against known credential leaks
- **Tags**: Stuffing, Hash Leak, Pastebin, Automation

## phpBB or Joomla User Hashes Cracked

- **Attack Type**: CMS User Hash Rainbow Table Attack
- **Target**: CMS Databases, Admin Panels
- **Vulnerability**: Weak CMS hash scheme, reused weak passwords
- **MITRE**: T1555 – Credential Dumping
- **Impact**: Admin access, full site compromise
- **Tools**: Hashcat, John the Ripper, Joomla Hash Tools
- **Scenario**: CMS platforms like phpBB or Joomla store user hashes in known formats (e.g., MD5 with salts) that can be cracked using CMS-specific rainbow tables.
- **Attack Steps**: Step 1: Gain access to the CMS database (via SQLi, backup leak, or exposed admin panel). Extract user password hashes — Joomla stores them as md5(password+salt) separated by :. Step 2: Identify hash type using hashid. For Joomla, you’ll see something like 5f4dcc3b5aa765d61d8327deb882cf99:abc123. Step 3: Use CMS-aware hash cracking tools like JohnTheRipper or hashcat -m 400 with the salt provided. Example: hashcat -m 20 -a 0 hashes.txt rockyou.txt. Step 4: If the password is weak or common, it will be cracked using rainbow tables or dictionary. Step 5: Use the cracked password to log into the CMS admin panel or impersonate a user. Step 6: Prevent by enforcing bcrypt-based storage and strong password policies within the CMS.
- **Detection**: Monitor for CMS config exposure or unusual admin login activity
- **Solution**: Upgrade to secure CMS versions; use bcrypt or Argon2 plugins; audit password policy
- **Tags**: Joomla, phpBB, Hash Cracking, CMS Exploit

## Drupal Rainbow Table Exploits

- **Attack Type**: CMS Hash Cracking via Rainbow Tables
- **Target**: Drupal CMS
- **Vulnerability**: Unsalted MD5 password hashes
- **MITRE**: T1555 – Credential Dumping
- **Impact**: Full admin panel takeover, user impersonation
- **Tools**: Hashcat, John the Ripper, rockyou.txt, RainbowCrack
- **Scenario**: Older versions of Drupal (pre-7.x) used weak, unsalted MD5 hashes for user passwords, making them vulnerable to rainbow table attacks.
- **Attack Steps**: Step 1: Attacker gains access to the Drupal database via backup leak, SQLi, or misconfiguration. Step 2: Locate the user table (users) and extract the password hashes. Step 3: Identify hash format — in older versions it will be MD5 (e.g., 5f4dcc3b5aa765d61d8327deb882cf99). Step 4: Use hash identification tool (hashid or hash-identifier) to confirm hash type. Step 5: Use hashcat -m 0 or john --format=raw-md5 with a wordlist like rockyou.txt to brute force the hash. Step 6: Alternatively, use precomputed rainbow tables with rcrack to match the MD5 hash directly. Step 7: If cracked, use the recovered credentials to log in as users or admins on the Drupal site. Step 8: Prevent this by upgrading to a modern Drupal version and using bcrypt or SHA512-based hashing.
- **Detection**: Alert on unusual DB access or config leaks; monitor for outdated CMS usage
- **Solution**: Upgrade to secure Drupal versions; apply salted hash modules or bcrypt plugins
- **Tags**: Drupal, Rainbow, MD5, CMS Exploit

## Cracking License Key Hashes

- **Attack Type**: Hash Brute Force for Licensing Systems
- **Target**: Commercial Software Products
- **Vulnerability**: Weak license key hash storage
- **MITRE**: T1552 – Credentials in Files
- **Impact**: Software piracy, bypass of licensing checks
- **Tools**: IDA Pro, Hashcat, HxD, Reverse Engineering Tools
- **Scenario**: Some commercial software products store license keys as weak, unsalted hashes (e.g., MD5) in local config files or registry, allowing offline cracking.
- **Attack Steps**: Step 1: Attacker installs or accesses a licensed version of the software. Step 2: Use a hex editor (e.g., HxD) or reverse engineering tools like IDA Pro to locate license key storage — often in config files, registry entries, or license.dat files. Step 3: Extract the hash value representing the license (usually MD5 or SHA1). Step 4: Use hashcat with the correct mode (e.g., -m 0 for MD5) and a dictionary like rockyou.txt or generate expected license formats (e.g., ABC-123, LICENSE-XYZ). Step 5: Run brute force or rainbow match until original license key is retrieved. Step 6: Replay the cracked license on a second machine or patch software to bypass checks. Step 7: Prevent this by using encrypted license keys, server-side validation, and stronger hashing schemes with salts.
- **Detection**: Detect tampered software binaries or reused license activations
- **Solution**: Move to server-verified license keys; encrypt license files; use challenge-response validation
- **Tags**: License Crack, MD5, Hash Brute Force

## Proprietary App Credential Recovery

- **Attack Type**: Password Hash Cracking from Enterprise Tools
- **Target**: Legacy Enterprise Applications
- **Vulnerability**: Custom weak password hashing logic
- **MITRE**: T1110 – Brute Force
- **Impact**: Full control of internal dashboard or backend systems
- **Tools**: Burp Suite, Hashcat, RainbowCrack, Fiddler
- **Scenario**: Legacy internal apps often use custom or unsalted hashing (MD5/SHA1) for local admin panels or user logins, vulnerable to dictionary/rainbow attack.
- **Attack Steps**: Step 1: Attacker identifies a legacy internal or proprietary application in use (e.g., old Java/.NET CRM or dashboard). Step 2: Use web proxies like Burp Suite or Fiddler to intercept login traffic and identify if a hashed password is being sent. Step 3: Alternatively, dump config or local database files to extract hash values (e.g., admin:5f4dcc3b5aa765d61d8327deb882cf99). Step 4: Determine the hash type — likely MD5 or SHA1. Step 5: Use hashcat or rcrack with appropriate rainbow tables to reverse the hash. Step 6: Replay credentials to login or elevate privileges inside the app. Step 7: If the password scheme is predictable (e.g., username+123), extend wordlist to reflect that pattern. Step 8: Recommend upgrading to modern password handling libraries and adding salting.
- **Detection**: Alert on outdated application usage or suspicious login patterns
- **Solution**: Refactor apps to use secure auth mechanisms; enforce bcrypt/Argon2; enable 2FA or AD-based login
- **Tags**: Legacy App, Internal Tools, Hash Recovery

## CTF Challenges with Known Hashes

- **Attack Type**: Rainbow Table or Dictionary CTF Cracking
- **Target**: CTF Platforms, HackTheBox Labs
- **Vulnerability**: Unprotected hashed strings without salting
- **MITRE**: T1110 – Brute Force
- **Impact**: Point gain in CTF or hash cracking practice
- **Tools**: Hashcat, John the Ripper, rainbow-tables.com
- **Scenario**: Many CTFs (Capture The Flag) present hash cracking challenges (MD5, SHA1, SHA256) where rainbow tables drastically reduce time-to-crack for scoring.
- **Attack Steps**: Step 1: In a CTF or red team engagement, identify a hash cracking challenge — often you’re given a hash and told it represents a password or flag. Step 2: Determine the hash type using tools like hashid. Step 3: Check if the hash exists in popular rainbow tables (e.g., crackstation.net, hashes.com) before brute forcing. Step 4: If it doesn’t, use hashcat with a large wordlist or build a custom one if there's a hint (e.g., the hash is a month or company name). Step 5: Use the fastest hash mode available (e.g., MD5 or SHA1). Step 6: Submit the cracked string as a flag or use it to access a second level of the challenge. Step 7: Helps in developing real-world password attack skills. Step 8: Always use safe environments when practicing.
- **Detection**: Use hash uniqueness checks in challenges to make guessing harder
- **Solution**: Add salting or use more advanced puzzles; encourage chaining hash + encryption steps
- **Tags**: CTF, CrackStation, Hash Practice

## Key Recovery via Pattern Matching

- **Attack Type**: Chosen Plaintext Attack (CPA) via Patterns
- **Target**: Encrypted Web APIs, Black Box Crypto Oracles
- **Vulnerability**: Deterministic output due to static input
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Key recovery, message structure inference
- **Tools**: Python, Cryptopals Labs, Burp Suite, Custom Encoder
- **Scenario**: Attackers input highly structured plaintexts (e.g., AAAAAAA...) to detect patterns in ciphertext output and use that to deduce or recover parts of the encryption key.
- **Attack Steps**: Step 1: Find an encryption oracle (e.g., login page or encryption API) where you can input plaintext and get back encrypted data. Step 2: Submit highly repetitive input like AAAAAAAAAAAAAAAAAAAAAA or ABABABABABABABAB and record the ciphertext. Step 3: Analyze the ciphertext blocks (usually 16-byte chunks in AES) — if identical patterns in plaintext result in repeating blocks, you know the encryption mode lacks randomness (e.g., ECB). Step 4: Repeat the process with variations to see which byte positions influence the output, which helps in identifying where the key affects the ciphertext. Step 5: If the encryption reuses keys and lacks IVs, these patterns can help leak information about the key or plaintext structure. Step 6: Use offline analysis or Cryptopals tools to try matching ciphertext patterns to guessed key bits or character positions. Step 7: Defenders should always randomize input (IV, nonce) to avoid this leak.
- **Detection**: Monitor encrypted traffic for pattern repetitions; detect abuse of public crypto endpoints
- **Solution**: Use random IVs, avoid ECB mode, implement constant-time encryption for APIs
- **Tags**: Pattern Analysis, CPA, Key Recovery

## ECB Mode Detection

- **Attack Type**: Ciphertext Pattern Recognition
- **Target**: Legacy Systems, Web Token APIs
- **Vulnerability**: Use of ECB mode for encryption
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full plaintext recovery from encrypted messages
- **Tools**: Python, xxd, openssl, GCHQ’s CyberChef
- **Scenario**: When using ECB mode, identical plaintext blocks produce identical ciphertext blocks, allowing attackers to detect the mode and exploit its weaknesses.
- **Attack Steps**: Step 1: Identify a service that encrypts data (e.g., user-uploaded messages or login tokens) and returns ciphertext (e.g., base64 strings or binary blobs). Step 2: Send an input like AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA (32 bytes) — designed to create at least two identical blocks. Step 3: Observe the ciphertext. If ECB is used, you’ll see repeated 16-byte blocks in the ciphertext (e.g., e8a...e8a...) since ECB encrypts each block independently with no IV. Step 4: Confirm ECB use by repeating with various inputs and spotting identical ciphertext regions. Step 5: If confirmed, attacker may attempt pixel/block visualization (for image encryption), brute-force partial blocks, or use block replacement techniques to manipulate messages. Step 6: Defenders must avoid ECB entirely — use CBC, GCM, or other authenticated encryption.
- **Detection**: Analyze ciphertext blocks for patterns; use entropy scanning tools
- **Solution**: Disable ECB mode; enforce GCM or CBC with IV and authenticated encryption
- **Tags**: ECB, Block Cipher, Crypto Visualization

## Padding Oracle + CPA

- **Attack Type**: Chosen Plaintext Attack with Padding Errors
- **Target**: Encrypted Cookies, Tokens, Web Forms
- **Vulnerability**: Improper padding validation in block ciphers
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Plaintext extraction, session hijacking
- **Tools**: PadBuster, Burp Suite, Custom Python Scripts
- **Scenario**: Attackers inject inputs causing decryption errors based on incorrect padding, then use the error behavior to infer plaintext byte-by-byte.
- **Attack Steps**: Step 1: Find an endpoint that decrypts encrypted tokens (e.g., cookies, JWTs) and responds differently when decryption fails due to padding (e.g., 500 error, custom error message). Step 2: Capture the encrypted blob (usually base64 or hex). Step 3: Use a tool like PadBuster to send manipulated versions of the encrypted data with specific byte changes in the last block. Step 4: Observe the server’s response. If an altered padding results in a unique error (e.g., “PaddingException”), it’s vulnerable. Step 5: Use PadBuster or your own script to automate guesses — for each byte, you modify the previous block and look for padding acceptance. Step 6: Recover plaintext byte-by-byte, even without the key. Step 7: Prevent this by using authenticated encryption (e.g., AES-GCM) and ensuring uniform error messages.
- **Detection**: Alert on decryption errors; check for repeated padding errors from same IP
- **Solution**: Use AES-GCM/CCM (authenticated encryption); return generic error messages on failure
- **Tags**: Padding Oracle, CBC, Crypto Side Channel

## CPA to Differential Cryptanalysis

- **Attack Type**: Chosen Plaintext + Statistical Crypto Analysis
- **Target**: Custom Ciphers, Crypto CTF Challenges
- **Vulnerability**: Weak cipher design, deterministic output
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Key schedule exposure, algorithm breaking
- **Tools**: Python, Custom Scripts, Academic Tools (e.g., Sage)
- **Scenario**: Attackers use multiple chosen plaintexts and analyze ciphertext differences to perform differential cryptanalysis and deduce key structure or algorithm properties.
- **Attack Steps**: Step 1: Choose a known or fixed cipher implementation (e.g., custom AES-like system or crypto challenge system). Step 2: Craft several structured plaintext inputs that differ by 1 bit (e.g., 00000001, 00000010, 00000100) and send them to the encryption oracle. Step 3: Record all resulting ciphertexts and compute the XOR difference between each ciphertext pair. Step 4: Plot the patterns — over enough samples, statistical similarities or trails may emerge, revealing characteristics of the key schedule or S-box structure. Step 5: Use this to infer parts of the key, substitute values, or round constants. Step 6: This attack works well on toy ciphers, insecure block cipher variants, or teaching models. Step 7: In real systems, differential cryptanalysis is impractical unless the implementation is extremely weak. Step 8: To defend, ensure cipher design follows NIST recommendations and implement proper randomness and entropy.
- **Detection**: Review encryption function entropy; test implementation under CPA/CCA analysis
- **Solution**: Use secure cipher standards like AES; avoid custom crypto unless audited
- **Tags**: Differential Crypto, Key Schedule Analysis

## S-Box Inversion via CPA

- **Attack Type**: Chosen Plaintext Cryptanalysis (CPA)
- **Target**: Custom Symmetric Ciphers
- **Vulnerability**: Static or weak substitution operations
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: S-Box reverse engineering, partial decryption
- **Tools**: Custom Python scripts, CrypTool, Cryptopals tools
- **Scenario**: Attackers use chosen plaintexts to reverse-engineer the substitution box (S-Box) used in symmetric ciphers like AES or custom encryption functions.
- **Attack Steps**: Step 1: Identify a cipher implementation (e.g., a web API or CTF challenge) that uses a known or suspected S-Box-based block cipher (like AES). Step 2: Submit controlled plaintext inputs where only 1 byte varies across samples (e.g., 00 00 00 00, 01 00 00 00, 02 00 00 00, etc.). Step 3: Capture the ciphertext for each input and analyze how the output bytes change. Step 4: Map how input values relate to output substitutions — this is a leakage of the S-Box mapping. Step 5: Using statistical analysis and repeated samples, reconstruct the S-Box table from the observed output patterns. Step 6: Once the full substitution mapping is known, use it to decrypt or predict future ciphertexts. Step 7: Defend against this by randomizing S-Box usage (if custom), or use well-audited algorithms (e.g., AES) with high diffusion.
- **Detection**: Monitor for high-frequency pattern inputs; entropy testing of encryption responses
- **Solution**: Avoid custom ciphers; rotate or randomize S-Box values if used; use strong diffusion primitives like MixColumns
- **Tags**: CPA, S-Box Mapping, Cryptanalysis

## AES-ECB Block Analysis

- **Attack Type**: ECB Mode Block Reassembly
- **Target**: AES Encryption in ECB Mode
- **Vulnerability**: Identical ciphertext blocks for repeated input
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Data structure leakage, plaintext reconstruction
- **Tools**: Burp Suite, CyberChef, Hex Editors, Python Scripts
- **Scenario**: AES in ECB mode reveals repeating ciphertext blocks when plaintext blocks are identical, allowing attackers to infer structure or reconstruct plaintexts.
- **Attack Steps**: Step 1: Discover a service or function that encrypts data and returns the ciphertext, such as a login form that returns encrypted session data or cookies. Step 2: Submit a plaintext with known repeating patterns (e.g., AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA) that covers multiple AES blocks (16 bytes per block). Step 3: Observe the ciphertext — if repeated plaintext blocks produce identical ciphertext blocks, you confirm ECB mode is in use. Step 4: Break your input into smaller structured chunks (e.g., JSON object fields) and encode one field at a time. Step 5: Reassemble ciphertext blocks into a meaningful structure (such as inferring field values, headers, or plaintext alignment). Step 6: This is especially powerful with predictable data like image files, where ECB leaks structure. Step 7: Prevent this by using secure modes like CBC or GCM with IVs.
- **Detection**: Analyze ciphertext entropy; scan for identical 16-byte blocks
- **Solution**: Never use ECB for encryption; use AES-GCM or AES-CBC with IV
- **Tags**: ECB, AES, Ciphertext Block Mapping

## CBC IV Guessing

- **Attack Type**: Initialization Vector Prediction
- **Target**: Encrypted Cookies / Tokens
- **Vulnerability**: Predictable or reused IV in CBC mode
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Decryption of first block, tampering with values
- **Tools**: Python, Burp Suite, Wireshark
- **Scenario**: If IVs are reused or generated poorly, attackers can choose plaintexts and analyze ciphertexts to infer or guess the IV and decrypt the first block.
- **Attack Steps**: Step 1: Identify a system using CBC (Cipher Block Chaining) mode encryption — often seen in encrypted cookies, session tokens, or custom APIs. Step 2: Send multiple requests with plaintext that starts with a predictable header (e.g., {"user":"guest"}), and capture the resulting ciphertext. Step 3: XOR the known plaintext with the first ciphertext block to recover the IV (since CBC: C1 = E(P1 ⊕ IV)). Step 4: If you can guess or control IV reuse, craft a new plaintext where the first block is XORed with the known IV to produce a desired ciphertext. Step 5: This allows attackers to tamper with encrypted values (e.g., change "guest" to "admin") or replay encrypted content. Step 6: Prevent by generating strong, random IVs per encryption operation and not exposing them insecurely. Step 7: CBC with static IV is considered insecure.
- **Detection**: Log IV generation events; monitor for pattern-based ciphertext inputs
- **Solution**: Use strong random IVs for each message; switch to authenticated encryption like GCM
- **Tags**: CBC IV Guess, Token Replay

## CTR Mode Plaintext Recovery

- **Attack Type**: Stream Cipher XOR Exploitation
- **Target**: AES-CTR Encrypted Streams
- **Vulnerability**: Nonce reuse or weak counter generation
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full plaintext recovery without key
- **Tools**: Wireshark, Python Scripts, Cryptopals Challenges
- **Scenario**: AES-CTR mode turns a block cipher into a stream cipher. If nonces are reused, attackers can XOR ciphertexts to leak plaintext, similar to OTP key reuse.
- **Attack Steps**: Step 1: Identify an encryption system using CTR (Counter) mode — often indicated by length-preserving ciphertext and presence of a nonce or counter value. Step 2: Monitor traffic or obtain multiple ciphertexts encrypted under the same nonce (e.g., due to server bug or misconfiguration). Step 3: XOR the two ciphertexts together — since: C1 ⊕ C2 = P1 ⊕ P2, you get a plaintext XOR (crib-dragging method). Step 4: Guess one part of plaintext (e.g., "username=") and XOR it with the corresponding XOR-ed ciphertext block to get the other plaintext. Step 5: Repeat until full messages are recovered. Step 6: If successful, attacker can reconstruct messages, credentials, or tokens. Step 7: Defend by enforcing unique nonces and random counters, and monitor for nonce reuse errors in logging or traffic capture.
- **Detection**: Analyze encrypted messages for identical prefixes; inspect nonce generation in logs
- **Solution**: Prevent nonce reuse; switch to AEAD modes (GCM); validate counter length and randomness
- **Tags**: AES-CTR, Stream Cipher, Nonce Reuse

## JWT Token Abuse (None/CBC)

- **Attack Type**: JWT Forgery or Token Manipulation
- **Target**: Web Apps Using JWT
- **Vulnerability**: Use of "none" algorithm or weak encryption
- **MITRE**: T1606 – Forge Web Tokens
- **Impact**: Admin access without credentials
- **Tools**: jwt_tool.py, Postman, Burp Suite, jwt.io
- **Scenario**: Some applications accept alg: none or improperly implement AES-CBC encryption of JWT tokens, allowing attackers to forge valid tokens like "admin".
- **Attack Steps**: Step 1: Intercept a valid JWT token from a login session using browser dev tools or Burp Suite (usually looks like eyJhbGci...). Step 2: Decode the token using jwt.io and check the alg field in the header. If it says HS256 or RS256, try changing it to "none" in the header. Step 3: Remove the signature part and re-encode the header and payload (e.g., set payload to "role": "admin" or "user": "admin"). Step 4: Submit the forged token in the Authorization header (Bearer <token>) and check if the system accepts it without verifying the signature. Step 5: If the app uses AES encryption (e.g., alg: A128CBC), look for an encryption oracle (e.g., encrypted cookies returned). Modify the ciphertext to swap roles/IDs, then submit. Step 6: If the token structure is predictable, attackers can brute-force or tamper to escalate privileges.
- **Detection**: Analyze JWT header and signature processing; log invalid signatures
- **Solution**: Disallow "none" alg; verify all JWT signatures; use signed tokens with strong algorithms
- **Tags**: JWT, Token Forgery, CBC Abuse

## Session Cookie Decryption

- **Attack Type**: Encrypted Cookie Decryption
- **Target**: Web App Cookies
- **Vulnerability**: Weak encryption or lack of integrity check
- **MITRE**: T1550 – Use of Alternate Authentication Material
- **Impact**: Account takeover, privilege escalation
- **Tools**: Burp Suite, CyberChef, Python
- **Scenario**: If session cookies are weakly encrypted (e.g., using static keys or ECB mode), attackers can predict structure and decrypt or manipulate them.
- **Attack Steps**: Step 1: Intercept an encrypted session cookie (usually Set-Cookie header in HTTP responses). Copy the encrypted string (base64 or hex). Step 2: Try decoding it in CyberChef using "From Base64" or "From Hex" followed by "ECB Decrypt" (if ECB suspected). Step 3: Observe if the decrypted data reveals structured JSON or readable fields like "role":"user". If yes, attacker now knows the cookie structure. Step 4: Try encrypting a new value with same key (if available or leaked via weak IV), e.g., change "user" to "admin" or escalate session state. Step 5: Send the tampered cookie in a new request and observe if access levels change. Step 6: Defend by using authenticated encryption like AES-GCM and rotating keys regularly.
- **Detection**: Check cookie values for patterns; analyze cookie entropy and decoding
- **Solution**: Use signed + encrypted cookies (JWT, AES-GCM); apply secure flags and cookie rotation policies
- **Tags**: Cookie Manipulation, Encrypted Sessions, CBC

## Encrypted Parameter Rewriting

- **Attack Type**: Encrypted Query or Form Field Manipulation
- **Target**: Encrypted GET/POST Parameters
- **Vulnerability**: Lack of MAC or integrity on encrypted fields
- **MITRE**: T1606 – Manipulate Application State
- **Impact**: Unauthorized action execution
- **Tools**: Burp Suite, CyberChef, Python Crypto Libraries
- **Scenario**: If applications encrypt URL/query/form parameters but do not validate them properly, attackers can tamper with ciphertext to modify behaviors.
- **Attack Steps**: Step 1: Identify encrypted parameters in GET/POST requests, e.g., /submit?token=dkjasdljf= or a hidden form field like <input value="9839fjlsd==">. Step 2: Send multiple requests with controlled values and analyze how the encrypted token changes. Step 3: Try flipping bits in the ciphertext (e.g., change last character of base64) and resend the request. Step 4: Observe error messages or behavior changes — if structure remains intact but function changes (e.g., accessing another user’s data), the encryption is predictable. Step 5: If the app uses ECB or CBC, inject known plaintext (like admin, true) and try padding/ciphertext manipulation techniques. Step 6: Attackers may elevate permissions or manipulate values. Step 7: To defend, validate decrypted data integrity (e.g., using HMAC) and never trust user-modifiable encrypted input.
- **Detection**: Log tampered encrypted field submissions; verify decryption failures
- **Solution**: Use HMAC for encrypted parameters; use AEAD schemes (e.g., AES-GCM) for confidentiality + integrity
- **Tags**: Encrypted Params, AES, Form Hijacking

## Base64 Encrypted ID Abuse

- **Attack Type**: Encoded ID Tampering
- **Target**: Web Apps Using Encoded IDs
- **Vulnerability**: Reliance on encoding instead of encryption
- **MITRE**: T1595 – Active Scanning
- **Impact**: ID tampering, access to unauthorized resources
- **Tools**: Burp Suite, CyberChef, browser dev tools
- **Scenario**: Applications that use Base64 to encode identifiers (user_id, file_id, etc.) without signing or encrypting them can be easily manipulated.
- **Attack Steps**: Step 1: Inspect URLs, requests, or hidden fields containing what looks like encoded values (e.g., /profile?id=YWRtaW4=). Step 2: Copy and decode the value using CyberChef (“From Base64”) — if it reveals something like "admin" or "user_id":123, then the system is only encoding, not encrypting. Step 3: Modify the decoded value (e.g., change "user_id":123 to "user_id":1) and encode it back to base64. Step 4: Replace the original value in the request and resend it. Step 5: If the application doesn’t verify access control, you may be able to access another user's account or file. Step 6: To defend, never rely on encoding for security. All user-controlled IDs must be validated and access-controlled on the server. Also, sign or encrypt sensitive values.
- **Detection**: Alert on mismatched user ID requests; implement strong access control at backend
- **Solution**: Use signed/encrypted ID tokens; verify ID mapping on server side
- **Tags**: Base64 ID, Broken Access Control, Predictable IDs

## Homomorphic Encryption CPA

- **Attack Type**: Chosen Plaintext Attack on Homomorphic Crypto
- **Target**: Encrypted Computation APIs
- **Vulnerability**: Homomorphic computation leakage
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Secret leakage from encrypted computations
- **Tools**: Python (Paillier libs), SEAL, HElib
- **Scenario**: Homomorphic encryption allows computations on ciphertexts. If operations leak patterns, chosen plaintexts can reveal original messages.
- **Attack Steps**: Step 1: Identify a system using homomorphic encryption (e.g., a voting platform or computation API). Step 2: Submit controlled plaintext values (like 1, 2, 4, etc.) encrypted under the public key. Step 3: Observe the resulting ciphertext outputs or computation results returned by the system (e.g., encrypted sums). Step 4: If the system reveals output patterns (e.g., addition of encrypted numbers), infer how values were combined. Step 5: Craft specially designed plaintexts that, when combined homomorphically, reveal properties of secret input (e.g., Enc(5) * Enc(x) = result ⇒ deduce x). Step 6: Repeat with different known values to reverse-engineer unknown inputs. Step 7: Homomorphic CPA attacks exploit algebraic structure — defend by blinding inputs or rate-limiting queries.
- **Detection**: Monitor encrypted computation requests; detect frequent low-entropy input values
- **Solution**: Add noise/blinding to homomorphic operations; limit operations per user or session
- **Tags**: Homomorphic CPA, Privacy Leakage

## LWE-Based CPA

- **Attack Type**: Chosen Plaintext Attack on LWE Schemes
- **Target**: Lattice Crypto Schemes (Kyber)
- **Vulnerability**: Predictable error leakage from crafted inputs
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Secret key recovery, full decryption of ciphertexts
- **Tools**: Python (SageMath), LWE libraries, KyberCPA
- **Scenario**: Lattice-based cryptosystems like Kyber or NTRU may be vulnerable to CPA if crafted plaintext vectors influence output structure.
- **Attack Steps**: Step 1: Study the public key format and ciphertext structure of a lattice-based system like Kyber. Step 2: Choose plaintexts (small binary vectors or low-weight vectors) and encrypt them using the target’s public key. Step 3: Submit multiple such ciphertexts to the system (if a decryption oracle is available) or analyze the system’s behavior/output patterns. Step 4: Observe changes in the noise or returned decryption result — attackers can correlate those with structure of the secret vector. Step 5: Use statistical methods and matrix algebra to solve the underlying LWE (Learning With Errors) problem, which reveals the secret key or plaintext. Step 6: LWE-based CPA attacks require high control and repeated queries — defend by limiting oracle exposure and applying strong padding/noise. Step 7: Always use IND-CCA2 secure lattice schemes in production.
- **Detection**: Monitor repeated vector patterns; validate ciphertext structures
- **Solution**: Use CCA-secure post-quantum algorithms (e.g., Kyber IND-CCA2); avoid raw decryption oracles
- **Tags**: LWE, Kyber, Lattice CPA

## One-Time Pad Reuse

- **Attack Type**: Chosen Plaintext XOR Exploit
- **Target**: OTP or XOR Encrypted Streams
- **Vulnerability**: Reuse of one-time pad keys
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full message reconstruction via XOR
- **Tools**: Python, CyberChef, Wireshark
- **Scenario**: OTP is perfectly secure only if used once. If reused, attacker can XOR ciphertexts to leak full plaintexts or perform crib dragging.
- **Attack Steps**: Step 1: Obtain two ciphertexts encrypted with the same OTP key (e.g., due to developer mistake or logging vulnerability). The ciphertexts must be of same or similar length. Step 2: XOR the two ciphertexts together. Since C1 ⊕ C2 = P1 ⊕ P2, you now have the XOR of two plaintexts. Step 3: Guess a word in one of the plaintexts (like “admin”, “username”), XOR it with the corresponding portion of the XORed result to get the second plaintext’s corresponding text. Step 4: Repeat until one or both plaintexts are fully recovered. Step 5: OTP reuse renders the scheme vulnerable like stream ciphers with reused key. Step 6: Defend by never reusing keys, ensuring fresh entropy per encryption, and avoiding OTP unless managed perfectly.
- **Detection**: Check for ciphertext reuse across messages; monitor length similarities
- **Solution**: Avoid OTP in practical apps; enforce unique random keys per message
- **Tags**: OTP, XOR, Stream Cipher Flaws

## RC4 Bias Exploits

- **Attack Type**: Statistical Bias Exploitation in RC4
- **Target**: Legacy TLS / WEP / SSL Streams
- **Vulnerability**: Inherent statistical biases in RC4 stream cipher
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Plaintext recovery with passive traffic collection
- **Tools**: Wireshark, Aircrack-ng, rc4bias tool
- **Scenario**: RC4 exhibits key-stream biases. By collecting enough ciphertexts, attacker can use known biases (e.g., 2nd byte = 0x00 with high probability) to recover plaintext.
- **Attack Steps**: Step 1: Identify a service or application using RC4 (e.g., legacy SSL/TLS, WEP, or VPN traffic). Step 2: Capture hundreds or thousands of ciphertexts encrypted with the same key or IV (like multiple sessions in WEP). Step 3: Focus on first few bytes of each ciphertext (especially 1st to 256th), as RC4 exhibits biases (e.g., byte 2 tends toward 0x00, byte 3 has non-uniform distribution). Step 4: Use statistical analysis to find likely values of the plaintext by reversing the biased output. Step 5: Repeat with more samples to improve accuracy. Step 6: These flaws were used to break WEP encryption and SSL in real-world attacks. Step 7: Defend by avoiding RC4 entirely and replacing it with secure ciphers like AES-GCM.
- **Detection**: Scan for use of RC4 in TLS handshakes; check WEP/SSL configs
- **Solution**: Deprecate RC4 in all systems; enforce secure cipher suites (AES, ChaCha20)
- **Tags**: RC4 Bias, WEP Cracks, Stream Cipher Flaw

## DES CPA Exploits

- **Attack Type**: Chosen Plaintext Attack on DES
- **Target**: Legacy Apps, Smartcards
- **Vulnerability**: Small key size and predictable structure
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full plaintext and key recovery with moderate effort
- **Tools**: John the Ripper, CrypTool, Python DES libs
- **Scenario**: Data Encryption Standard (DES) is vulnerable to CPA due to its small key size and predictable S-box structure. Attackers use known plaintexts to derive the key.
- **Attack Steps**: Step 1: Identify a system using DES (e.g., legacy web apps, old SSL, smartcards). Step 2: Submit known plaintext blocks (like all-zero 00000000) and record the resulting ciphertexts. Step 3: Repeat the process for multiple plaintexts with single-bit variations to trigger known S-box patterns. Step 4: Use this to recover subkey bits used in specific DES rounds. Step 5: Leverage tools like John the Ripper to brute-force reduced keyspace using gathered plaintext/ciphertext pairs. Step 6: DES's small 56-bit key allows recovery in hours/days with modern GPUs. Step 7: Avoid DES entirely in new systems; replace with AES.
- **Detection**: Monitor for frequent ciphertexts with fixed plaintext patterns
- **Solution**: Replace DES with AES or secure block cipher alternatives; block plaintext reuse
- **Tags**: DES, CPA, Legacy Crypto

## BitLocker CPA (Old Versions)

- **Attack Type**: Cipher Block Chaining + CPA on Disk Volumes
- **Target**: Legacy BitLocker Volumes
- **Vulnerability**: No integrity in CBC encryption used for full-disk
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Volume tampering, bypassed encryption, silent data mods
- **Tools**: Kali Linux, AccessData FTK, WinHex, AES tools
- **Scenario**: Early BitLocker implementations used AES-CBC without integrity protection, allowing attackers with access to disk and chosen plaintexts to manipulate encrypted volumes.
- **Attack Steps**: Step 1: Gain physical access to a BitLocker-encrypted drive using outdated Windows versions (e.g., Windows Vista). Step 2: Collect known plaintexts stored at predictable offsets (like the bootloader or registry hives). Step 3: Analyze the corresponding encrypted sectors using tools like WinHex. Step 4: Inject crafted plaintexts into known sectors and observe ciphertext changes using differential analysis. Step 5: Use this pattern to reverse-engineer keys or tamper with contents without detection. Step 6: These attacks work because CBC mode allows block manipulation and BitLocker did not originally use XTS or authentication tags. Step 7: Modern BitLocker versions (post-Windows 7) use AES-CBC with Elephant Diffuser or AES-XTS.
- **Detection**: Monitor unusual disk sector patterns; check for mismatch between known data and decrypted output
- **Solution**: Upgrade to latest BitLocker using AES-XTS; enforce full-disk encryption policy; never reuse CBC without authentication tag
- **Tags**: Full Disk Encryption, BitLocker, CPA

## Wi-Fi WEP Attacks

- **Attack Type**: IV Collision + CPA (Keystream Recovery)
- **Target**: Wireless Networks Using WEP
- **Vulnerability**: Reused IVs, weak key scheduling in RC4
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Full network access, data sniffing, AP compromise
- **Tools**: Aircrack-ng, Wireshark, Kismet, tcpdump
- **Scenario**: WEP uses RC4 with 24-bit IVs. Due to IV reuse and weak RC4 bias, CPA enables recovery of plaintext or full key with captured packets.
- **Attack Steps**: Step 1: Capture thousands of WEP packets using airodump-ng or tcpdump from a target Wi-Fi network. Step 2: Focus on packets with repeating IVs or small header fields (e.g., ARP requests). Step 3: Use aircrack-ng to analyze these packets, exploiting weak IV reuse and RC4 bias patterns. Step 4: The tool uses a form of chosen-plaintext attack by analyzing known patterns in ARP frames to reverse the RC4 keystream. Step 5: Once enough data is collected (usually 10K–100K packets), aircrack-ng recovers the WEP key. Step 6: You can now decrypt traffic or join the network. Step 7: WEP is entirely broken—avoid its use in any real-world deployments.
- **Detection**: Detect RC4/IV reuse; scan for outdated WEP access points
- **Solution**: Replace WEP with WPA3 or WPA2-AES; disable WEP on all routers
- **Tags**: WEP, RC4, IV Reuse, Wireless Hacking

## TLS CBC Exploits

- **Attack Type**: Chosen Plaintext via CBC Padding Oracle
- **Target**: Web Apps Using TLS 1.0/1.1
- **Vulnerability**: CBC padding error leaks info to attacker
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Token/session hijack, credential theft
- **Tools**: Burp Suite, TLS-Attacker, PadBuster, Wireshark
- **Scenario**: TLS 1.0/1.1 using CBC (e.g., AES-CBC) are vulnerable to padding oracle attacks via crafted messages. Allows plaintext recovery byte by byte.
- **Attack Steps**: Step 1: Identify a web app using TLS 1.0/1.1 with AES-CBC (you can check via browser dev tools or openssl s_client). Step 2: Intercept encrypted request traffic, e.g., login tokens, session cookies encrypted over TLS. Step 3: Use Burp Suite or PadBuster to inject modified ciphertext blocks and observe server response. Step 4: Server behavior like “padding error” or “invalid MAC” reveals how the app handles decryption errors. Step 5: Exploit these differences to perform byte-by-byte decryption of the original plaintext using the padding oracle technique. Step 6: Full session tokens or credentials can be extracted from encrypted TLS traffic. Step 7: Use TLS 1.2/1.3 with AEAD (e.g., AES-GCM) to prevent such attacks.
- **Detection**: Monitor TLS downgrade attempts; scan for CBC ciphers in use
- **Solution**: Disable TLS 1.0/1.1; enforce TLS 1.3 with AEAD ciphers (AES-GCM, ChaCha20-Poly1305)
- **Tags**: TLS, CBC Padding Oracle, Encryption Downgrade

## Model Inference via CPA-like Input Testing

- **Attack Type**: Chosen Input Model Inference
- **Target**: Black-box ML APIs / SaaS Models
- **Vulnerability**: Lack of model hardening against probing
- **MITRE**: T1606 – ML Model Inference
- **Impact**: Intellectual property theft, privacy violation
- **Tools**: Python, PyTorch, TensorFlow, TextAttack, CleverHans
- **Scenario**: By carefully crafting and submitting inputs to an ML model (black-box), an attacker can infer the underlying logic, architecture, weights, or even sensitive training data.
- **Attack Steps**: Step 1: Access a target ML model via an API, web form, or app (e.g., text classification, image analysis). Step 2: Begin submitting controlled inputs with known structure — e.g., gradually changing pixel values in an image or altering one word at a time in a sentence. Step 3: Observe the output probability or classification label returned by the model. Step 4: Use these outputs to map input changes to output behavior, and reverse-engineer how the model was trained or structured. Step 5: Continue using statistical correlation or optimization algorithms to infer weights or training samples, especially if the model leaks confidence scores. Step 6: This mimics CPA: attacker chooses input, sees output, and learns internal secrets. Step 7: Defense includes output obfuscation, differential privacy, and limiting verbose outputs.
- **Detection**: Monitor repetitive input patterns; limit API query rates; detect probing-like patterns
- **Solution**: Obfuscate outputs (no confidence scores); apply differential privacy; rate-limit access; use watermarking
- **Tags**: ML, AI Inference, Membership Probing

## Neural Network Backdoor Detection

- **Attack Type**: Controlled Input CPA (Trigger Testing)
- **Target**: AI Models (NLP, Vision, Audio)
- **Vulnerability**: Backdoor payloads respond to specific inputs
- **MITRE**: T1606 – ML Model Manipulation
- **Impact**: Misclassification, model hijack, system compromise
- **Tools**: Python, Neural Cleanse, DeepInspect, PyTorch
- **Scenario**: Backdoored models behave normally unless triggered by specific input patterns. Attackers or auditors can test inputs to reveal hidden logic.
- **Attack Steps**: Step 1: Obtain access to a suspicious model, e.g., a neural network classifier for images, text, or speech. Step 2: Create and submit structured, unusual inputs — e.g., overlaying a specific pixel pattern or text token ("trigger"). Step 3: Observe whether the model consistently misclassifies these trigger inputs regardless of context. Step 4: Use Neural Cleanse or DeepInspect to analyze neuron activations and check for unusually influential neurons tied to specific input patterns. Step 5: If consistent incorrect predictions occur with minimal triggers, it's a strong sign of a backdoor. Step 6: Repeat with variations of suspected triggers to validate. Step 7: Backdoors are often inserted during training via poisoned data. Step 8: Defend by retraining, input sanitization, and running trojan detection tools.
- **Detection**: Monitor for abnormal input clusters; analyze prediction confidence on rare patterns
- **Solution**: Use trusted training datasets; apply backdoor detection tools (Neural Cleanse, STRIP); perform adversarial validation
- **Tags**: Backdoor Detection, Neural Trojan, AI Threat

## Encryption-as-a-Service Oracle

- **Attack Type**: CPA on Public Encryption-as-a-Service
- **Target**: Cloud Crypto APIs
- **Vulnerability**: CBC/ECB exposure via user-controlled input
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Info leakage, indirect decryption, token abuse
- **Tools**: curl, Burp Suite, Postman, OpenSSL, Python requests
- **Scenario**: Many cloud providers offer encryption APIs. If outputs leak structure or padding behavior, attackers can infer plaintexts via CPA-style tests.
- **Attack Steps**: Step 1: Register for a cloud service offering encryption-as-a-service (e.g., AWS KMS, Azure Key Vault, or custom crypto APIs). Step 2: Submit known plaintexts (e.g., "AAAA", "BBBB", padded patterns) via API requests. Step 3: Collect returned ciphertexts and analyze for repeating blocks, length differences, or padding errors. Step 4: Modify one byte at a time and analyze output structure — this reveals block size, padding scheme, and potentially leaks part of plaintext. Step 5: Repeat to reverse-engineer full encryption logic. Step 6: Advanced attacks may combine this with timing analysis or error codes. Step 7: Cloud APIs with verbose responses or block ciphers in ECB/CBC mode are vulnerable. Step 8: Mitigate with AEAD, error normalization, and strict input validation.
- **Detection**: Analyze ciphertext similarity for different inputs; check for ECB or repeated patterns
- **Solution**: Use AES-GCM (AEAD), normalize error messages, encrypt padding; restrict inputs to well-defined formats
- **Tags**: Cloud Oracle, CBC, Crypto Abuse

## Hardware Security Module (HSM) CPA

- **Attack Type**: CPA on On-prem or Cloud HSMs
- **Target**: HSMs (Cloud or On-Premise)
- **Vulnerability**: ECB/CBC mode, verbose errors, deterministic behavior
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Key recovery, crypto service abuse, plaintext leaks
- **Tools**: HSM SDKs, curl, PKCS#11 tools, YubiHSM, AWS CloudHSM
- **Scenario**: Poorly designed HSMs may return ciphertext for arbitrary plaintexts. If misused, attackers can learn encryption logic or infer keys.
- **Attack Steps**: Step 1: Identify a Hardware Security Module (HSM) available for key management or crypto operations (e.g., local USB HSMs or cloud-based AWS CloudHSM). Step 2: Submit chosen plaintexts using encryption functions (e.g., encrypting "0000", "1111", or predictable headers). Step 3: Collect ciphertexts and analyze for structure — especially useful if HSM uses block cipher modes like ECB or CBC. Step 4: If ciphertexts are deterministic, repeated, or reflect input patterns, use this info to infer key material or encrypted plaintext. Step 5: For cloud HSMs, try padding errors or malformed blocks to trigger error messages revealing decryption behavior. Step 6: Repeat with variations to analyze HSM internal logic. Step 7: Always use AEAD modes like AES-GCM and monitor access.
- **Detection**: Monitor encryption API logs for high-volume or structured input patterns
- **Solution**: Use AEAD encryption modes; enforce usage limits; never expose raw encryption services without strict validation
- **Tags**: HSM, Cloud Key Abuse, Crypto API

## Decryption Oracle Abuse

- **Attack Type**: Decrypt-Through-Oracle via API/Smart Contract
- **Target**: APIs, Web3 Contracts, Cloud Apps
- **Vulnerability**: Public-facing decryptors with no auth or access control
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Data leakage, session hijack, API misuse
- **Tools**: curl, Postman, Web3.py, Metamask, Python Scripts
- **Scenario**: Attackers exploit an API, smart contract, or app feature that reveals plaintext of attacker-supplied ciphertexts — effectively functioning as a decryption oracle.
- **Attack Steps**: Step 1: Identify a target app or smart contract where users can submit ciphertext and receive decrypted outputs (e.g., a decrypt API, blockchain decryption function). Step 2: Confirm if this function provides full plaintext or gives side-channel output (e.g., errors, length, flags). Step 3: Craft ciphertexts using predictable block patterns or known plaintext blocks (e.g., encrypted "AAAA" or "1234"). Step 4: Submit these to the API or function and record responses. Step 5: If you receive plaintext or behavior that varies based on the ciphertext structure, the system acts as a decryption oracle. Step 6: Automate this with scripting to iteratively decrypt sensitive data (e.g., session tokens, user info). Step 7: Mitigate by never exposing decryption logic directly to users, and encrypt with AEAD or authenticated tokens.
- **Detection**: Monitor decryption requests per IP/app; detect patterns indicating brute-force or structured ciphertext usage
- **Solution**: Remove plaintext-returning endpoints; use authenticated encryption (e.g., AES-GCM); enforce strong authorization
- **Tags**: Decryption Oracle, API Exploitation, Blockchain, Crypto

## Padding Oracle Attack (CBC Mode)

- **Attack Type**: Byte-by-Byte Plaintext Decryption via Error Leaks
- **Target**: TLS/SSL, ASP.NET, Custom Crypto
- **Vulnerability**: Distinct padding error messages on decryption
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full plaintext recovery, session hijack
- **Tools**: Burp Suite, PadBuster, TLS-Attacker, Wireshark
- **Scenario**: CBC mode (e.g., in TLS, ASP.NET) is vulnerable to padding oracle attacks when systems return specific error messages for invalid padding during decryption.
- **Attack Steps**: Step 1: Find a system using CBC-mode block cipher (e.g., TLS 1.0/1.1, custom ASP.NET app) that decrypts input ciphertexts and returns errors on failure. Step 2: Send a valid encrypted message and observe the normal server response. Step 3: Begin modifying the last byte of the last ciphertext block and resend to the server. Step 4: If a "padding error" occurs for most values but not all, the server is revealing decryption info. Step 5: Use this error to determine the correct padding byte value. Step 6: Repeat this byte-by-byte until the full block is decrypted. Step 7: Apply this to prior blocks to eventually decrypt the entire ciphertext. Step 8: Tools like PadBuster automate this CBC padding oracle attack. Step 9: Always use AEAD encryption (e.g., AES-GCM) with integrity checks to prevent padding leaks.
- **Detection**: Monitor for high-volume malformed ciphertexts; check error message uniformity
- **Solution**: Implement uniform error responses; use AEAD encryption instead of CBC without integrity
- **Tags**: CBC Padding Oracle, TLS, ASP.NET, Byte-by-Byte Decryption

## Bleichenbacher’s RSA Attack

- **Attack Type**: RSA PKCS#1 Padding Oracle
- **Target**: SSL/TLS (Legacy), RSA Crypto
- **Vulnerability**: Padding validation leaks in RSA v1.5 implementations
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: TLS session decryption, RSA key misuse
- **Tools**: TLS-Attacker, Wireshark, SSL Labs, nmap
- **Scenario**: Legacy SSL implementations using RSA PKCS#1 v1.5 are vulnerable to decryption oracle attacks where the attacker submits ciphertexts and observes if padding is valid.
- **Attack Steps**: Step 1: Identify if the target uses RSA for encrypting pre-master secrets in SSL/TLS handshake (especially SSL 3.0, TLS 1.0/1.1). Step 2: Send encrypted blobs (RSA ciphertexts) to the server during handshake and observe the responses. Step 3: If server responds differently when padding is correct (even if wrong key), it leaks a “valid/invalid” signal. Step 4: Automate ciphertext modifications using a tool like TLS-Attacker to vary the structure of the encrypted message. Step 5: Use binary search and modular arithmetic to narrow down the range of possible plaintext values. Step 6: Eventually, you recover the original plaintext (pre-master secret). Step 7: This can lead to full session key recovery and decryption of TLS sessions. Step 8: Modern TLS (1.2+) avoids this via forward secrecy and AEAD.
- **Detection**: Detect legacy TLS/RSA handshakes in logs; look for malformed RSA payloads
- **Solution**: Disable RSA PKCS#1; enforce ECDHE or DHE with forward secrecy; upgrade to TLS 1.3
- **Tags**: RSA Padding Oracle, SSL, Bleichenbacher

## Manger’s Attack (RSA CCA)

- **Attack Type**: RSA Padding Oracle via Error-Based CCA
- **Target**: APIs using RSA, Legacy Decryption APIs
- **Vulnerability**: Oracle-like RSA decryption with padding feedback
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Private key misuse, session compromise
- **Tools**: Custom Python Script, SageMath, TLS-Attacker
- **Scenario**: Manger’s attack targets RSA encryption with known padding and relies on ciphertext malleability + error messages to recover plaintext.
- **Attack Steps**: Step 1: Identify a target using RSA decryption API or server-side RSA decryption logic with distinguishable error messages. Step 2: Craft a ciphertext C and encrypt it under the public RSA key. Step 3: Send C to the oracle (target API/server) and observe whether the response indicates “correct padding” or a “decryption error.” Step 4: Multiply C by s^e mod n (where s is attacker-controlled scalar) and send the result to the oracle. Step 5: Observe whether the error type changes (padding ok vs. error). Step 6: Use this signal to perform interval narrowing using RSA math until the actual plaintext is fully determined. Step 7: Repeat until all bytes are revealed. Step 8: This attack assumes full control over ciphertext and observability of errors, so it applies mostly to vulnerable APIs or legacy systems.
- **Detection**: Monitor for malformed RSA ciphertext patterns; observe repeated oracle interaction
- **Solution**: Don’t return detailed decryption errors; enforce constant-time decryption; move to hybrid encryption (RSA + AES-GCM)
- **Tags**: Manger Attack, RSA, PKCS Decryption Oracle

## CCA Against Hybrid Encryption

- **Attack Type**: Chosen Ciphertext Attack (CCA) on Hybrid RSA+AES
- **Target**: Web APIs, Secure Email, SSO Apps
- **Vulnerability**: RSA decrypts AES session key, leading to hybrid CCA
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Symmetric key recovery, total message decryption
- **Tools**: OpenSSL, custom Python tools, SageMath
- **Scenario**: Hybrid schemes use RSA to encrypt AES keys. Attackers send malformed ciphertexts to recover parts of symmetric key or plaintext via oracle or timing feedback.
- **Attack Steps**: Step 1: Identify a target that uses hybrid encryption — RSA encrypts AES session key, and AES encrypts actual data. Common in APIs, TLS, or JWT handling. Step 2: Obtain access to the system’s decryption endpoint or backend that processes encrypted requests. Step 3: Create modified RSA ciphertexts that target the AES session key portion (e.g., flip bits or inject math-based mutations). Step 4: Send these crafted ciphertexts and observe server behavior (timing, error messages, or outputs). Step 5: If error responses differ (e.g., padding error vs AES decryption error), infer whether the RSA or AES part failed. Step 6: Use CCA math (e.g., RSA malleability) and binary search techniques to isolate the symmetric key. Step 7: Decrypt the rest of the encrypted message using recovered AES key. Step 8: Defense includes authenticated encryption (AES-GCM) and not exposing raw RSA decryption services.
- **Detection**: Analyze failed decryption request frequency and distinguish RSA/AES error source in logs
- **Solution**: Use hybrid encryption with AEAD only; enforce constant-time decryption for RSA; avoid exposing decryption endpoints
- **Tags**: Hybrid Encryption, RSA+AES, Decryption Oracle

## JWT Decryption via Oracle

- **Attack Type**: Auth Bypass via Decryption Oracle
- **Target**: Web APIs using JWTs
- **Vulnerability**: Leaky encrypted JWT error feedback
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Identity impersonation, session hijack
- **Tools**: jwt_tool.py, Burp Suite, Postman, jwt.io
- **Scenario**: If JWTs use encryption (JWE) and the server leaks errors or decrypts attacker-controlled tokens, it can serve as a decryption oracle.
- **Attack Steps**: Step 1: Identify if the application uses encrypted JWTs (JWE) instead of signed tokens (JWS). You’ll see components like enc, iv, and ciphertext in the token. Step 2: Copy a valid encrypted JWT used by the app and modify the ciphertext or IV slightly (e.g., change 1 character at a time). Step 3: Send the altered JWT to the API (e.g., /profile, /me, /auth) and analyze server response. Step 4: If different responses are returned for invalid vs valid padding, or content-type errors, the app is acting as a decryption oracle. Step 5: Use this behavior to infer parts of the payload, decrypt JWTs, and potentially bypass auth. Step 6: Automate the process with jwt_tool or a Python script. Step 7: Defense includes rejecting all malformed tokens uniformly and using AEAD encryption (e.g., AES-GCM) for token handling.
- **Detection**: Inspect JWT error response diversity and failed token processing frequency
- **Solution**: Always use signed JWTs (JWS); if using encrypted JWTs, enforce strict AEAD and uniform error messages
- **Tags**: JWT Oracle, JWE Abuse, Web API Crypto

## CCA via Password Reset Tokens

- **Attack Type**: Auth Token Decryption via Chosen Ciphertext
- **Target**: Password Reset Workflows
- **Vulnerability**: Predictable encrypted token behavior
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Account takeover via forged reset link
- **Tools**: Burp Suite, Python, curl, Wireshark
- **Scenario**: Reset tokens are often encrypted strings passed via URL or email. If attackers manipulate them and observe behavior, they may decrypt or forge valid tokens.
- **Attack Steps**: Step 1: Trigger a password reset process on a target site and capture the token (usually found in the reset link: example.com/reset?token=abc123...). Step 2: Make small modifications to the token (e.g., change last few characters, truncate, pad). Step 3: Send modified token to the reset endpoint and record server response — observe whether the error changes for different mutations. Step 4: If responses vary (e.g., "token expired" vs "token invalid" vs "decryption failed"), you have an oracle that leaks token structure. Step 5: Use these differences to guide crafting of valid tokens or to infer partial plaintext (e.g., user email or timestamp). Step 6: In cases where CBC is used, padding oracle techniques may apply. Step 7: Prevent this by normalizing all token errors and encrypting tokens using AEAD.
- **Detection**: Monitor token tampering attempts; alert on malformed reset link patterns
- **Solution**: Implement constant error messages; use signed + encrypted (AEAD) tokens only; expire tokens aggressively
- **Tags**: Reset Token Oracle, URL Token Abuse, CBC Attack

## Cloud KMS Decryption Oracle

- **Attack Type**: API Decryption Oracle in Key Management Service
- **Target**: AWS KMS, Azure Key Vault, GCP KMS
- **Vulnerability**: KMS endpoint allows arbitrary decryption
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Secrets exposure, lateral movement
- **Tools**: curl, AWS CLI, gcloud, Azure CLI, Burp Suite
- **Scenario**: Improperly exposed or misconfigured Cloud KMS can let users submit ciphertexts and receive decrypted plaintexts, functioning as a decryption oracle.
- **Attack Steps**: Step 1: Identify a cloud KMS endpoint (e.g., AWS KMS, GCP KMS, Azure Key Vault) exposed via API that supports ciphertext decryption. Step 2: Verify if the decryption operation can be accessed using stolen or misconfigured IAM credentials (e.g., misassigned KMS roles). Step 3: Craft arbitrary ciphertexts or collect encrypted tokens used by the application. Step 4: Submit ciphertexts to the KMS API using decrypt function. Step 5: If the KMS returns decrypted plaintexts without restriction or logging, it is acting as a decryption oracle. Step 6: Use this to decrypt sensitive config values, secrets, or database tokens. Step 7: Detect by logging all KMS requests and enabling key usage auditing. Step 8: Secure by restricting KMS decrypt permissions to minimum required roles and enabling hardware-based key protections.
- **Detection**: Log all KMS decrypt calls; enable detailed audit trails and key usage alerts
- **Solution**: Apply least privilege to KMS roles; disallow raw decryption APIs for apps; use key policies with deny-by-default
- **Tags**: Cloud KMS Oracle, IAM Misuse, Token Decryption

## CCA in OAuth2 Tokens

- **Attack Type**: Chosen Ciphertext on Encrypted OAuth2 Token
- **Target**: OAuth2 APIs, Identity Providers
- **Vulnerability**: Encrypted token decryption feedback loop
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Account takeover, privilege escalation
- **Tools**: Burp Suite, Postman, jwt_tool, TLS-Proxy
- **Scenario**: Some OAuth2 implementations encrypt access tokens (vs signing), and weak crypto or error responses allow attackers to decrypt tokens via CCA or padding oracle-style behavior.
- **Attack Steps**: Step 1: Identify if the OAuth2 server uses encrypted tokens (often base64 encoded, with structure like JWE or custom cipher). Step 2: Use Burp Suite or a proxy to capture and modify tokens used in Authorization headers or cookies. Step 3: Change small parts of the encrypted token (e.g., IV, last bytes of ciphertext). Step 4: Send modified token to an API endpoint and observe differences in server response. Step 5: If server returns different errors (e.g., "Invalid Token", "Malformed", or timeout), then the system leaks decryption behavior. Step 6: Use this feedback loop to mount a CCA or padding oracle attack — eventually recovering parts of the access token. Step 7: Use decoded payload (e.g., user ID, scope) to elevate access or impersonate accounts. Step 8: Defense includes using signed tokens (JWT JWS), AEAD encryption, and uniform error messages.
- **Detection**: Monitor failed token decoding frequency; check if decrypted token validation differs by structure
- **Solution**: Use signed tokens (JWS); encrypt tokens with AEAD only (e.g., AES-GCM); normalize token error messages
- **Tags**: OAuth2 Token CCA, Identity Hijack, Encrypted JWT Abuse

## WebSocket Auth Bypass via CCA

- **Attack Type**: Chosen Ciphertext on Encrypted WS Headers
- **Target**: WebSocket Authenticated Channels
- **Vulnerability**: Decryption oracle in WS handshake headers
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Auth bypass, hijack of real-time sessions
- **Tools**: Burp Suite, browser DevTools, WS Proxy Tool
- **Scenario**: If WebSocket authentication uses encrypted headers or tokens, and decrypts them server-side with error feedback, CCA can be used to reveal or forge auth info.
- **Attack Steps**: Step 1: Identify a WebSocket connection (wss://) that uses encrypted authentication headers (e.g., "x-auth-token" or cookies sent during handshake). Step 2: Capture the full WebSocket handshake using browser DevTools or a proxy. Step 3: Modify encrypted parts of headers — like changing a few base64 characters. Step 4: Re-initiate the WebSocket connection and record the server response (e.g., 401 Unauthorized, 403, or silent drop). Step 5: Compare responses across different modified tokens. If the error type or timing changes, the server may leak decryption state. Step 6: Use this as an oracle to iteratively recover the original plaintext or build a valid encrypted token. Step 7: Automate with scripts to bypass access control in real-time WebSocket apps. Step 8: Use strong crypto (e.g., signed tokens, AEAD) and consistent error handling to prevent this.
- **Detection**: Monitor abnormal handshake failures; alert on repeated WebSocket auth attempts with varying headers
- **Solution**: Use AEAD or signed tokens for WS headers; disable token decoding in handshake and move to secure cookie auth
- **Tags**: WebSocket Auth Bypass, Token Decryption, CCA, Real-Time Hijack

## BEAST Attack (TLS 1.0 CBC)

- **Attack Type**: CBC Chosen-Plaintext Attack via JavaScript
- **Target**: TLS 1.0-enabled Web Servers
- **Vulnerability**: CBC IV reuse in old TLS versions
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Session cookie recovery, HTTPS decryption
- **Tools**: BEAST PoC Script, Wireshark, older browsers
- **Scenario**: A classic CBC-mode chosen plaintext attack that decrypts HTTPS traffic in TLS 1.0/SSL 3.0 by injecting chosen plaintext blocks and observing block decryption alignment via timing.
- **Attack Steps**: Step 1: Target a victim using a vulnerable browser that allows JavaScript to make HTTPS requests (via XHR or iframe). Step 2: Host malicious JS code on a site the victim visits (XSS or third-party ad). Step 3: The JS injects chosen plaintext bytes in HTTPS requests to a known TLS 1.0 server. Step 4: By observing response patterns and using CBC block alignment, attacker can deduce each byte of the secure request (e.g., session cookie). Step 5: Repeat until all sensitive data (e.g., sessionid=...) is decrypted. Step 6: This attack relies on block re-use and predictable IVs in TLS 1.0 CBC. Step 7: Modern TLS (1.2+) with AEAD (e.g., GCM) is immune. Step 8: Always disable TLS 1.0 in server config and browsers.
- **Detection**: Detect browser version; analyze CBC decryption error or CBC padding patterns
- **Solution**: Enforce TLS 1.2+ with AES-GCM or ChaCha20-Poly1305; use HSTS; drop support for SSL3/TLS1.0
- **Tags**: TLS CBC, BEAST Attack, HTTPS Decryption

## Lucky13 TLS Attack

- **Attack Type**: CBC Timing-Based Oracle Attack on TLS
- **Target**: TLS 1.2 CBC-mode Implementations
- **Vulnerability**: TLS CBC decryption reveals padding via timing
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Plaintext recovery over HTTPS, full session decrypt
- **Tools**: TLS-Attacker, Scapy, custom timing tool, Wireshark
- **Scenario**: An advanced timing side-channel attack targeting CBC-mode decryption in TLS implementations that reveals padding errors through response time variations.
- **Attack Steps**: Step 1: Target a server that supports TLS 1.1 or 1.2 with CBC-mode ciphers (not GCM). Step 2: Prepare many TLS records with carefully constructed ciphertexts that differ by one byte or padding. Step 3: Send these records and measure response times — sometimes in milliseconds or microseconds. Step 4: Analyze timing differences between valid and invalid padding responses. Step 5: Use these micro-timing signals as an oracle to guess padding and decrypt one byte at a time. Step 6: This is extremely slow but can work reliably. Step 7: Use Lucky13 PoC tools to automate the attack. Step 8: Hardened TLS libraries (OpenSSL >1.0.1g, BoringSSL) use constant-time padding checks to mitigate this. Step 9: Use AEAD modes (GCM/ChaCha) instead of CBC to eliminate timing leaks.
- **Detection**: Perform timing analysis of encrypted TLS connections under CBC-mode; validate CBC padding time discrepancies
- **Solution**: Upgrade to AEAD ciphers; patch TLS libraries; enforce constant-time decryption logic
- **Tags**: TLS CBC, Lucky13, Timing Oracle, HTTPS Padding Leak

## DROWN Attack (SSLv2 CCA)

- **Attack Type**: SSLv2 Padding Oracle + RSA Key Reuse
- **Target**: Servers supporting SSLv2, TLS, Mail Servers
- **Vulnerability**: Shared RSA key allows legacy padding oracle attack
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full HTTPS session decryption, credential theft
- **Tools**: DROWN Scanner, OpenSSL, Wireshark
- **Scenario**: Decrypts modern TLS traffic by abusing servers supporting legacy SSLv2 with the same RSA key, acting as a padding oracle.
- **Attack Steps**: Step 1: Find a target HTTPS server that still supports SSLv2 or shares an RSA private key with a system that supports it (e.g., SMTP over SSLv2). Step 2: Use a tool like DROWN Scanner or Wireshark to confirm SSLv2 support and key sharing. Step 3: Craft malformed SSLv2 handshake messages using chosen ciphertexts. Step 4: Send them to the SSLv2 service to observe whether decryption succeeds or fails — this acts as a padding oracle. Step 5: Use this feedback to recover the premaster secret for a TLS session encrypted with the same RSA key. Step 6: Decrypt the full TLS session (passwords, cookies, etc.). Step 7: Attack is possible even if only 1 linked service (e.g., mail server) supports SSLv2. Step 8: Disable SSLv2 entirely and use different keys for TLS and legacy services.
- **Detection**: Detect shared private keys across services; monitor SSLv2 handshake attempts
- **Solution**: Completely disable SSLv2; never reuse RSA keys across services; enforce TLS 1.2+ only
- **Tags**: SSLv2, RSA Reuse, Padding Oracle, TLS Downgrade

## ROBOT Attack (Bleichenbacher 2.0)

- **Attack Type**: RSA PKCS#1 v1.5 Padding Oracle in TLS
- **Target**: TLS servers with RSA key exchange support
- **Vulnerability**: PKCS#1 v1.5 padding oracle in TLS RSA decryption
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full session decryption, TLS handshake compromise
- **Tools**: testssl.sh, robot-detect.py, Wireshark
- **Scenario**: Modern Bleichenbacher-style attack against RSA decryption in TLS implementations (especially in load balancers or legacy endpoints).
- **Attack Steps**: Step 1: Identify a TLS server (e.g., website, API, load balancer) that supports RSA key exchange in TLS. Step 2: Use the robot-detect.py tool to test if the server acts as a padding oracle (responds differently to malformed PKCS#1 v1.5 ciphertexts). Step 3: If vulnerable, use the oracle to recover the TLS session’s premaster secret one byte at a time. Step 4: Once premaster secret is known, decrypt the rest of the HTTPS session. Step 5: Attack is fully passive after key recovery. Step 6: Attack also works if RSA key exchange is supported only for fallback/compatibility. Step 7: Mitigate by using Diffie-Hellman key exchange instead of RSA in TLS, and by disabling RSA-based handshakes. Step 8: Patch all TLS libraries (OpenSSL, F5, etc.) to reject PKCS#1 v1.5 oracle behavior.
- **Detection**: Scan TLS configs for RSA key exchange; analyze TLS response timings
- **Solution**: Disable RSA key exchange in TLS; apply latest OpenSSL/F5/NSS patches; prefer forward-secret ciphersuites
- **Tags**: ROBOT Attack, RSA PKCS Oracle, Bleichenbacher Reloaded

## TLS CBC Timing Oracle

- **Attack Type**: CBC Padding Oracle via Response Timing
- **Target**: TLS Web Servers or APIs
- **Vulnerability**: CBC padding checked in non-constant time
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Decrypt HTTPS traffic, credential leakage
- **Tools**: TLS-Attacker, timing.py, Wireshark
- **Scenario**: Exploits timing differences in how TLS decrypts padding in CBC-mode (non-AEAD) ciphers. Works on servers not hardened for constant-time operations.
- **Attack Steps**: Step 1: Target a TLS server that supports CBC-mode ciphers (like AES-CBC-SHA in TLS 1.1 or TLS 1.2). Step 2: Craft TLS ciphertexts with slight padding variations. Step 3: Send many of these ciphertexts to the server and record response times precisely (use Wireshark, custom Python, or Scapy). Step 4: Use statistical analysis to correlate padding correctness with timing differences. Step 5: Build an oracle based on time differences and use it to decrypt ciphertext byte by byte. Step 6: This attack is similar to Lucky13 but applies to broader TLS stacks. Step 7: Hardened TLS libraries avoid this issue using constant-time decryption logic. Step 8: Avoid CBC ciphers in favor of AES-GCM or ChaCha20-Poly1305.
- **Detection**: Perform timing analysis on CBC-mode TLS responses; detect consistent padding error patterns
- **Solution**: Upgrade TLS to only use AEAD ciphers; use hardened libraries like OpenSSL > 1.0.1g; monitor TLS config weekly
- **Tags**: TLS CBC, Padding Oracle, Timing Side-Channel, Lucky13

## PGP Encrypted Email Attack

- **Attack Type**: CCA on PGP Encrypted Multipart Email
- **Target**: PGP Email Clients (Thunderbird, Outlook)
- **Vulnerability**: MIME-based chosen ciphertext leakage
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Exfiltration of encrypted email content
- **Tools**: GPG, Thunderbird, PGP email test suite
- **Scenario**: Exploits how some email clients handle PGP-encrypted messages in multiple MIME parts — chosen ciphertexts can leak decrypted content via CCA logic.
- **Attack Steps**: Step 1: Compose a multipart email (e.g., encrypted text + image attachment) with a known PGP recipient. Step 2: Replace one MIME part (e.g., the text part) with a maliciously crafted PGP-encrypted block. Step 3: Send the email and wait for the target client (e.g., Thunderbird) to attempt decryption. Step 4: If the client leaks partial decrypted content (e.g., error messages, display fragments, or HTML rendering), observe it via reply email, bug report, or shared screen. Step 5: This allows attackers to slowly recover plaintext content of PGP messages by controlling ciphertext inputs. Step 6: Clients that fail to isolate and verify each MIME part separately are vulnerable. Step 7: Modern PGP clients apply decryption only to trusted single-part messages and verify signatures before displaying.
- **Detection**: Monitor mail client errors; check logs for unusual MIME rendering issues
- **Solution**: Decrypt PGP only after verifying all signatures; avoid decrypting multipart messages from unverified sources
- **Tags**: PGP MIME Oracle, Email Decryption Abuse, CCA

## XML Encryption CCA (SOAP APIs)

- **Attack Type**: Chosen Ciphertext via Encrypted XML
- **Target**: SOAP-based Web Services
- **Vulnerability**: XML Encryption with padding oracle errors
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Credential theft, elevation of privileges
- **Tools**: SoapUI, XMLSecTool, Burp Suite XML Plugin
- **Scenario**: SOAP APIs using XML Encryption standards (like WS-Security) often process encrypted blocks that can be manipulated to act as a decryption oracle.
- **Attack Steps**: Step 1: Find a SOAP API that uses XML Encryption — usually evident from <xenc:EncryptedData> tags inside SOAP envelopes. Step 2: Intercept a valid encrypted SOAP request using Burp Suite or SoapUI. Step 3: Modify small parts of the encrypted <CipherValue> (base64-encoded encrypted XML content). Step 4: Send the tampered SOAP message to the server. Step 5: If server returns specific error messages (e.g., “decryption failed,” “invalid padding,” or SOAP faults), use those as oracles. Step 6: Repeat with varying modifications to recover the plaintext or infer structure of the original message. Step 7: Use known CCA techniques (padding oracle, byte flipping) to target specific values like tokens, usernames, or roles. Step 8: Protect by using AES-GCM instead of CBC, and never leak crypto failure reasons.
- **Detection**: Monitor SOAP fault codes; alert on excessive malformed encrypted messages
- **Solution**: Use AEAD for XML Encryption; suppress detailed crypto error responses; validate structure before decrypting
- **Tags**: XMLSec, SOAP Oracle, WS-Security, CBC Oracle

## VPN or IPSec Message Tampering

- **Attack Type**: Encrypted Packet Manipulation / CCA
- **Target**: IPSec VPNs, L2TP, IKEv1 Gateways
- **Vulnerability**: Encrypted packet error response reveals structure
- **MITRE**: T1040 – Network Sniffing
- **Impact**: VPN credential recovery, session hijack
- **Tools**: Wireshark, Scapy, ike-scan, Libreswan Tools
- **Scenario**: Some VPN/IPSec implementations leak padding or integrity errors when malformed encrypted packets are received — enabling oracle-style attacks.
- **Attack Steps**: Step 1: Identify a target IPSec or VPN server (e.g., using IKEv1, ESP, or L2TP/IPSec). Step 2: Capture encrypted VPN traffic (e.g., .pcap using Wireshark). Step 3: Craft modified encrypted packets using Scapy or ike-scan. Step 4: Inject them into the tunnel (e.g., from MITM position or spoofed IP). Step 5: Observe server responses — if certain messages differ based on padding or MAC correctness, you have a side-channel oracle. Step 6: Use this to launch CCA against ESP payloads, recovering secrets like usernames or VPN session keys. Step 7: Older implementations are especially vulnerable (e.g., pre-Libreswan hardening). Step 8: Use IPsec stack hardening, AEAD ciphers, and constant-time validation to prevent this.
- **Detection**: Monitor for malformed ESP/IKE packets; detect repeated padding error responses
- **Solution**: Enforce modern IPsec with AES-GCM; drop IKEv1; monitor for forged packets on external interface
- **Tags**: VPN, IPSec Oracle, Network Crypto CCA

## Secure Messaging App CCA (Signal)

- **Attack Type**: CCA on Messaging Protocols (e.g., Signal, OMEMO)
- **Target**: Encrypted Messaging Apps
- **Vulnerability**: Corrupted ciphertext reveals decryption state
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Metadata leakage, app fingerprinting, content inference
- **Tools**: Signal CLI, WireShark, Frida, custom wrapper apps
- **Scenario**: Secure apps like Signal use encryption but may reveal user behavior (e.g., retries, fallbacks) when presented with corrupted messages, leaking partial content structure.
- **Attack Steps**: Step 1: Set up or intercept a secure messaging app (like Signal, Threema, OMEMO) on test devices. Step 2: Craft and send intentionally corrupted encrypted messages (e.g., flip bits or replace ciphertext blocks). Step 3: Observe recipient device behavior — does the app show a “retry,” “resend,” or “error” notification? Step 4: If yes, use this behavioral feedback as a decryption oracle — different corrupted ciphertexts causing different UI states. Step 5: Automate the process using Signal CLI or a wrapper script with message send + response monitor loop. Step 6: In some cases, this allows inferring metadata like recipient ID, message type, or even parts of plaintext. Step 7: Secure apps mitigate this using message authentication codes (MACs) and uniform response handling.
- **Detection**: Analyze app behavior on message failure; test across app versions
- **Solution**: Always verify MAC before decrypting; normalize error handling across all encryption paths
- **Tags**: Signal, OMEMO, Secure Messaging, Encrypted Messaging Oracle

## Token-based Auth Bypass (CCA)

- **Attack Type**: CCA on Encrypted Tokens or Cookies
- **Target**: Web Apps / APIs
- **Vulnerability**: Encrypted auth tokens expose feedback on tampering
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Session hijacking, account elevation
- **Tools**: Burp Suite, Postman, TLS Proxy, jwt_tool
- **Scenario**: Auth tokens that are encrypted and decrypted on the server may leak information if decrypted errors or behaviors are exposed.
- **Attack Steps**: Step 1: Capture a token or cookie used for authentication — typically sent in headers like Authorization: Bearer <token> or as a cookie (e.g., auth_token). Step 2: Modify the encrypted token slightly (e.g., change a few base64 characters). Step 3: Resend the request to the server and observe the response. Step 4: If server gives different error messages (e.g., “user not found,” “invalid token,” “decryption failed”), this becomes an oracle. Step 5: Use this feedback to recover structure or guess valid tokens. Step 6: In weak setups, you may escalate privilege (e.g., change user ID to admin, re-sign token). Step 7: Always use AEAD modes like AES-GCM for token encryption and do MAC verification before decryption. Step 8: Normalize error messages and enforce secure token parsing logic.
- **Detection**: Alert on repeated token decode errors; monitor token structure parsing
- **Solution**: Encrypt tokens with AEAD (GCM); use signed tokens like JWT with JWS; normalize auth error messages
- **Tags**: Token Oracle, CCA, Auth Bypass, Encrypted Cookies

## GCM Tag Forgery with CCA

- **Attack Type**: GCM Tag Guessing and Forgery via CCA
- **Target**: APIs using AES-GCM, TLS endpoints
- **Vulnerability**: GCM tag validation errors leak feedback
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Message forgery, data tampering, session hijack
- **Tools**: TLS-Attacker, custom Python scripts
- **Scenario**: Galois/Counter Mode (GCM) provides authenticated encryption, but improper implementation may leak info when invalid tags are used — allowing attackers to guess valid tags.
- **Attack Steps**: Step 1: Identify a system (e.g., API, TLS service) using AES-GCM to encrypt and authenticate messages. Step 2: Capture or create an encrypted payload (ciphertext + GCM tag). Step 3: Replace the tag with random values or incrementally generated ones. Step 4: Send the tampered payload to the target. Step 5: If the application leaks different errors (e.g., “invalid MAC” vs. “parse error”), this becomes a decryption oracle. Step 6: Use tag forgery techniques like Bernstein's Distinguisher or bit-flipping to refine the correct tag guess. Step 7: Once a valid tag is discovered, attacker can send forged ciphertexts that pass authentication. Step 8: Prevent this by never revealing tag validation errors and always failing authentication silently.
- **Detection**: Monitor repeated AES-GCM errors; detect excessive invalid tag attempts
- **Solution**: Enforce constant-time MAC check; always fail decryption silently; log anomalies without leaking cause
- **Tags**: AES-GCM, Tag Forgery, CCA, Authenticated Encryption

## JSON Web Encryption (JWE) Exploitation

- **Attack Type**: CCA on Encrypted JWT (JWE)
- **Target**: OAuth Servers, JWE-based Auth APIs
- **Vulnerability**: Encrypted JWT mishandling as CCA oracle
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Token forgery, auth bypass, session impersonation
- **Tools**: jwt_tool, Postman, Burp Suite
- **Scenario**: JWE tokens, used in OAuth and SSO, can leak data or act as decryption oracles when modified ciphertexts are processed incorrectly by the server.
- **Attack Steps**: Step 1: Obtain a valid JWE token from an OAuth server or SSO-based login (it typically looks like 5 base64-encoded segments separated by dots). Step 2: Modify the encrypted payload or CEK (content encryption key) segment. Step 3: Re-submit the tampered token to the server. Step 4: Observe if server errors change (e.g., “decryption failed,” “user not found,” or silent re-auth). Step 5: If response behavior varies with payload structure, this becomes a CCA oracle. Step 6: Use this to brute-force parts of the CEK or determine user ID/role through token crafting. Step 7: In some cases, you can escalate privileges or impersonate users. Step 8: Secure by enforcing strict JWE validation, using AEAD (e.g., AES-GCM) and uniform error messages.
- **Detection**: Monitor JWT/JWE errors; compare frequency of malformed payloads
- **Solution**: Use AEAD only (AES-GCM); implement signature + payload validation; normalize all error responses
- **Tags**: JWE, OAuth, Encrypted JWT, CCA, Token Abuse

## CCA in Identity-Based Encryption

- **Attack Type**: Oracle Exploitation in IBE
- **Target**: IBE-Based Messaging or Email Systems
- **Vulnerability**: Oracle feedback from IBE scheme
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Identity impersonation, plaintext recovery
- **Tools**: OpenABE, Charm-Crypto
- **Scenario**: Identity-Based Encryption (IBE) schemes like Boneh-Franklin allow using public identities as encryption keys. If a decryption oracle exists, attacker can extract plaintext.
- **Attack Steps**: Step 1: Set up or target an Identity-Based Encryption (IBE) system that uses public identity strings as input (e.g., email-based IBE like Boneh-Franklin scheme). Step 2: Obtain a valid IBE-encrypted ciphertext (e.g., from intercepted traffic or simulated test). Step 3: Slightly modify the ciphertext components (e.g., change ephemeral key or ciphertext blocks). Step 4: Submit tampered ciphertext to the IBE server or oracle-based client. Step 5: If server responds with errors that reveal decryption failure (e.g., wrong padding, invalid identity), this becomes a CCA oracle. Step 6: Use this behavior iteratively to reconstruct valid ciphertexts for other users or guess plaintexts. Step 7: Proper IBE systems must use authenticated encryption (like pairing-based AEAD) and constant-time validation.
- **Detection**: Log malformed ciphertexts per identity; audit IBE usage frequency
- **Solution**: Use authenticated encryption in IBE; suppress feedback on failed identity decryption
- **Tags**: Identity-Based Encryption, IBE, Boneh-Franklin, CCA

## CTF Padding Oracle Challenge

- **Attack Type**: Simulated CBC Padding Oracle
- **Target**: CTF Crypto Labs, Learning Platforms
- **Vulnerability**: CBC padding oracle challenge
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Learn to decrypt without keys using padding oracle
- **Tools**: Burp Suite, padbuster, CyberChef
- **Scenario**: Many Capture The Flag (CTF) platforms simulate padding oracle challenges to teach about CBC-based vulnerabilities in crypto systems.
- **Attack Steps**: Step 1: Open the CTF platform and identify a crypto challenge titled "Padding Oracle" or similar. Step 2: The system gives you a ciphertext and an oracle endpoint (e.g., an API or web form) that reveals whether decryption fails due to bad padding. Step 3: Use tools like padbuster, Burp Suite, or write a Python script to modify the last byte of the ciphertext block-by-block. Step 4: Observe the oracle’s error responses. When a correct padding is guessed (e.g., PKCS#7), it behaves differently (e.g., "padding OK"). Step 5: Use this to recover one byte at a time from the plaintext. Step 6: Repeat for each byte until entire message is decrypted. Step 7: This teaches real-world CCA risk. Step 8: The best fix is AEAD mode like GCM.
- **Detection**: Track CTF submission patterns; detect scripted abuse
- **Solution**: Use AEAD like AES-GCM in production; avoid CBC with padding unless validated with MAC first
- **Tags**: CTF, Padding Oracle, CBC Decryption, Labs

## Attacker-in-the-Middle Decryption

- **Attack Type**: MITM-Based CCA on Encrypted Streams
- **Target**: Encrypted HTTP, WebSocket, SSO Tokens
- **Vulnerability**: CBC mode in unprotected channels
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Session hijack, token decryption, confidential data loss
- **Tools**: Wireshark, mitmproxy, sslstrip, custom tools
- **Scenario**: In simulated or insecure setups, a MITM attacker can modify encrypted data in-transit and use server/client error messages to decrypt data block-by-block.
- **Attack Steps**: Step 1: Set up a controlled environment where you act as a man-in-the-middle (MITM) between a client and server (e.g., using ARP spoofing, mitmproxy). Step 2: Intercept and log encrypted traffic — especially encrypted cookies, tokens, or CBC-encrypted payloads. Step 3: Modify the ciphertext slightly in-flight (e.g., flip a byte in a CBC-encrypted HTTP request). Step 4: Let the request go through to the server. Step 5: Observe server error messages or response status — if they change depending on tampered ciphertext, you have a decryption oracle. Step 6: Use padding oracle logic to recover plaintext block-by-block. Step 7: This technique is commonly used in red team assessments. Step 8: Always use TLS 1.3 or encrypt data with AEAD in transit.
- **Detection**: Monitor MITM-like traffic patterns; detect encrypted payload modification
- **Solution**: Use end-to-end encryption (E2EE); authenticate ciphertexts using AEAD; disable TLS downgrade
- **Tags**: MITM, CCA, Web Token, Encrypted Traffic

## Simulation on AES-CBC APIs

- **Attack Type**: CBC Padding Oracle via Encrypted API
- **Target**: API Testing Environments, Demo Servers
- **Vulnerability**: AES-CBC vulnerable to padding oracle attack
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Educational decryption of secrets without keys
- **Tools**: Python CryptoLib, Flask, Postman
- **Scenario**: Simulated test APIs often expose CBC-encrypted tokens or messages that developers can use to experiment with padding oracles in controlled labs.
- **Attack Steps**: Step 1: Use a test lab API that encrypts data using AES-CBC (e.g., /api/encrypt and /api/decrypt). Step 2: Send valid ciphertext through /api/decrypt and observe the API’s behavior on padding errors (e.g., HTTP 500 on bad padding, HTTP 200 on correct). Step 3: Modify ciphertext block by block to exploit padding error timing or status differences. Step 4: Use scripting to automate the decryption of the last byte of each block using trial-and-error until correct padding is identified. Step 5: Once padding length is identified, recover plaintext one byte at a time using XOR tricks. Step 6: This type of lab is used in bug bounty, university coursework, and red team training. Step 7: Best practice is to avoid CBC without MAC.
- **Detection**: Detect CBC use in test APIs; log decryption error types
- **Solution**: Switch to AES-GCM; prevent encryption errors from leaking to response; apply constant-time decryptions
- **Tags**: CBC, API Testing, Crypto Simulations, Oracle Exploit

## Brute-force with Known Plaintext

- **Attack Type**: Keyspace Reduction via Known Plaintext
- **Target**: Weakly Encrypted Files or Transmissions
- **Vulnerability**: Lack of key randomization + predictable plaintext
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Reduced key search space → faster brute-force
- **Tools**: Python CryptoLib, CyberChef, Hashcat
- **Scenario**: When an attacker knows part of the original plaintext and the ciphertext, they can test keys that produce the known part, reducing brute-force complexity.
- **Attack Steps**: Step 1: Identify a target ciphertext where a portion of the original plaintext is known or can be guessed (e.g., headers, common protocol text, "HTTP/1.1"). Step 2: Use a brute-force tool or script to decrypt the ciphertext with all possible keys in the keyspace. Step 3: Compare the result with the known plaintext segment. Step 4: If a match is found, the key is likely correct. Step 5: This technique drastically reduces search effort compared to full brute-force. Step 6: Often used against weak encryption schemes, like ZIP or XOR-based encoding. Step 7: Prevent this by using randomized IVs, strong keys, and authenticated encryption.
- **Detection**: Monitor repeated decryption attempts; flag partial matches
- **Solution**: Use strong ciphers with random IVs and key stretching like PBKDF2
- **Tags**: Known Plaintext, Brute-force, Keyspace Reduction

## Key Deduction via XOR (Stream Ciphers)

- **Attack Type**: XOR Key Recovery
- **Target**: XOR-based Protocols, RC4 Streams
- **Vulnerability**: Keystream reuse, XOR-based encryption
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Partial or full key/keystream recovery
- **Tools**: Python, CyberChef, Wireshark
- **Scenario**: In stream ciphers using XOR (like RC4 or simple XOR schemes), if attacker knows both plaintext and ciphertext, they can recover the exact keystream/key.
- **Attack Steps**: Step 1: Capture a ciphertext encrypted using a stream cipher like XOR or RC4. Step 2: Obtain or guess a portion of the original plaintext (e.g., known headers like "GET", "Host:"). Step 3: Apply XOR between the ciphertext and the known plaintext segment using tools like CyberChef or a custom script: Key = Plaintext ⊕ Ciphertext. Step 4: The result gives you part of the keystream used for encryption. Step 5: Use this partial key to decrypt other parts of the message or predict future messages if the keystream is reused. Step 6: Prevent this by never reusing keystreams and avoiding static keys in XOR-based systems.
- **Detection**: Detect reuse of keystreams; flag repeated XOR behavior
- **Solution**: Never reuse keys or keystreams; switch to modern AEAD encryption
- **Tags**: XOR, RC4, Stream Cipher, Known Plaintext, KPA

## Statistical KPA on Substitution Ciphers

- **Attack Type**: Frequency Analysis via Known Plaintext
- **Target**: Legacy Systems, Educational Ciphers
- **Vulnerability**: Substitution without randomization
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full plaintext recovery with basic analysis
- **Tools**: CrypTool, Paper & Pen
- **Scenario**: Classical substitution ciphers like Caesar or monoalphabetic ones leak info when plaintext stats (e.g., 'e' is most common letter) match ciphertext freq.
- **Attack Steps**: Step 1: Obtain a ciphertext encrypted with a substitution cipher (e.g., Caesar, monoalphabetic). Step 2: Analyze the frequency of each letter or symbol in the ciphertext (e.g., count 'X' appears 14 times). Step 3: Use English language letter frequency (e.g., 'e' most common, then 't', 'a', 'o') as a baseline. Step 4: Map the most frequent ciphertext letters to most common English letters. Step 5: Substitute and refine by comparing guessed decryption with expected structure of known plaintext. Step 6: This approach is part of classical crypto breaking and taught in intro courses. Step 7: Modern systems are safe from this, but legacy data isn't.
- **Detection**: Compare frequency graphs of plaintext vs ciphertext; alert if simple pattern match succeeds
- **Solution**: Avoid substitution-only ciphers; always use randomized keys and modes of operation like AES-GCM
- **Tags**: Classical Cipher, Frequency Attack, Substitution KPA

## Block Replay with Known Headers

- **Attack Type**: Known Block Insertion
- **Target**: Encrypted HTTP/TLS traffic
- **Vulnerability**: CBC mode without integrity protection
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Message injection, request forgery
- **Tools**: Wireshark, TLS-Attacker, Burp Suite
- **Scenario**: In block ciphers, when headers or tokens are predictable, attacker can copy ciphertext blocks from one message into another, bypassing integrity checks.
- **Attack Steps**: Step 1: Observe multiple encrypted messages where the structure is similar (e.g., headers like "POST /login", "User-Agent:"). Step 2: Note that block ciphers like AES-CBC divide the plaintext into fixed-size chunks (e.g., 16 bytes). Step 3: Identify ciphertext blocks corresponding to the known headers. Step 4: Copy those known blocks and insert them into another encrypted request, preserving alignment. Step 5: If the system doesn’t validate integrity or use MAC, the forged request may be accepted. Step 6: Repeat with different blocks to reconstruct or forge valid sessions. Step 7: Prevent this by using authenticated encryption (AEAD) and validating entire ciphertexts.
- **Detection**: Analyze repeated ciphertext block patterns; monitor for replayed message parts
- **Solution**: Use AES-GCM or encrypt-then-MAC schemes; never trust message parts without full authentication
- **Tags**: Block Cipher Replay, CBC, Known Header Injection

## Format-based Decryption (e.g., File Signatures)

- **Attack Type**: Header-Based Known Plaintext Decryption
- **Target**: Encrypted Files with Known Headers
- **Vulnerability**: Predictable file format headers
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Partial file recovery, keystream extraction
- **Tools**: CyberChef, Hex Editor, Python
- **Scenario**: File formats like PDF, ZIP, PNG, etc., have fixed headers (magic bytes) that can be used to recover partial keys or plaintext.
- **Attack Steps**: Step 1: Identify the file type from context or extension (e.g., PDF files start with %PDF, ZIP files with PK). Step 2: Obtain an encrypted version of the file. Step 3: Guess the starting plaintext (e.g., %PDF-1.4 or PK\x03\x04). Step 4: XOR the known header with the corresponding ciphertext bytes to extract part of the key or keystream. Step 5: Use this recovered part to decrypt additional bytes if using stream cipher or XOR-based method. Step 6: If block cipher is used, this may help identify block alignment or structure. Step 7: Extend using pattern or statistical inference. Step 8: Always verify decrypted output to avoid false positives. Step 9: This method is useful in malware analysis, password-protected documents, and steganography.
- **Detection**: Monitor XOR attempts over file headers; analyze decryption guess frequency
- **Solution**: Use random IVs, avoid static headers with weak encryption
- **Tags**: File Signature, Magic Bytes, Format Guessing, XOR Decrypt

## Caesar Cipher KPA

- **Attack Type**: Shift-Based Known Plaintext Recovery
- **Target**: Educational Ciphers, Historical Messages
- **Vulnerability**: Fixed shift + no key randomness
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full decryption using 1-word plaintext guess
- **Tools**: CrypTool, Pen & Paper
- **Scenario**: Caesar Cipher shifts letters by a fixed amount. Knowing part of the plaintext gives away the shift key instantly.
- **Attack Steps**: Step 1: Obtain a ciphertext encrypted using Caesar cipher (e.g., khoor for hello). Step 2: Guess or know part of the plaintext (e.g., the message starts with "hello"). Step 3: Convert both ciphertext and guessed plaintext to ASCII values or alphabets (e.g., h=104, k=107). Step 4: Subtract plaintext char from ciphertext (mod 26 for alphabets) → reveals the shift used. Step 5: Apply this shift to entire ciphertext to get full message. Step 6: Validate if the full message makes sense. Step 7: Caesar is trivially broken with KPA and offers no practical security.
- **Detection**: Detect repeated alphabet patterns; match frequency profiles
- **Solution**: Don't use Caesar cipher; switch to standard cryptography with randomized key and padding
- **Tags**: Caesar, Classical, Educational, Beginner, Shift Cipher

## Vigenère Cipher KPA

- **Attack Type**: Multishift Cipher Key Extraction via KPA
- **Target**: Legacy Educational Ciphers
- **Vulnerability**: Repeating key vulnerability with known text
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full key recovery → message decryption
- **Tools**: CrypTool, Python Script
- **Scenario**: If attacker knows plaintext and ciphertext, they can compute and recover Vigenère key by aligning letter-by-letter.
- **Attack Steps**: Step 1: Obtain ciphertext encrypted with Vigenère cipher (e.g., repeating-key XOR-like cipher). Step 2: Guess or know part of the original plaintext. Step 3: Align known plaintext under ciphertext (letter-by-letter). Step 4: For each character, compute the key: KeyChar = CipherChar – PlainChar (mod 26). Step 5: Recovered key segment = repeating key used in encryption. Step 6: Analyze how often the key repeats to deduce key length. Step 7: Extend attack to entire ciphertext. Step 8: With full key, decrypt the message. Step 9: Vigenère is vulnerable if plaintext is partially known.
- **Detection**: Frequency analysis of cipher shifts; Kasiski test on key lengths
- **Solution**: Use polyalphabetic or randomized encryption modes; do not reuse keys
- **Tags**: Vigenère, Classical Cipher, Known Plaintext

## Enigma Machine KPA (WWII)

- **Attack Type**: WWII-era Mechanical Cipher Broken via KPA
- **Target**: Enigma Machines, WWII Military Encryption
- **Vulnerability**: Daily reused keys + predictable message format
- **MITRE**: Historical Technique
- **Impact**: Full key recovery, strategic wartime advantage
- **Tools**: Bombe (historical), Python emulators
- **Scenario**: During WWII, Allied forces used repeated weather reports and known phrases to deduce German Enigma keys using known plaintexts.
- **Attack Steps**: Step 1: Intercept daily Enigma-encrypted German military messages. Step 2: Use intelligence ("cribs")—known phrases like "weather report" or "Heil Hitler". Step 3: Match these known plaintexts against corresponding ciphertexts. Step 4: Analyze rotor wiring patterns to back-calculate key settings (rotor position, plugboard config). Step 5: Use electro-mechanical "Bombe" machine to test key combinations rapidly. Step 6: Validate decrypted message and extract daily key sheet values. Step 7: Repeat daily; Enigma settings changed every 24 hours. Step 8: Attack relied heavily on known plaintext and repetition. Step 9: Prevented today via secure key exchange and digital crypto.
- **Detection**: Human intelligence, manual decrypt comparisons
- **Solution**: Use modern digital crypto with secure key agreement & randomization
- **Tags**: Enigma, Known Plaintext, Historical Crypto

## One-Time Pad Reuse

- **Attack Type**: XOR Stream Recovery via Known Plaintext
- **Target**: Stream Cipher with reused OTP or keystream
- **Vulnerability**: Key reuse in XOR / OTP schemes
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Complete plaintext recovery with minimal effort
- **Tools**: Python, CyberChef, xorsearch
- **Scenario**: If the same one-time pad or stream key is reused, XOR of two ciphertexts leaks info. Knowing part of one plaintext reveals the other.
- **Attack Steps**: Step 1: Capture two ciphertexts (C1 and C2) that were both encrypted using the same one-time pad or stream key (violating OTP rule). Step 2: XOR the two ciphertexts: C1 ⊕ C2 = P1 ⊕ P2 (this gives XOR of the two plaintexts). Step 3: If attacker knows part or all of one plaintext (e.g., from context or known message formats), they can recover the second plaintext using XOR: P2 = (C1 ⊕ C2) ⊕ P1. Step 4: Even partial knowledge (like greetings, headers) helps recover large parts of the second message. Step 5: This is a textbook violation of OTP usage—never reuse keys. Step 6: This method is fast and doesn’t require brute-force or timing — just algebra.
- **Detection**: Monitor for ciphertexts that XOR cleanly; flag key reuse cases
- **Solution**: Never reuse OTP/keystreams; use AEAD or strong symmetric encryption
- **Tags**: One-Time Pad, XOR Attack, KPA, Stream Ciphers

## Kasiski Examination (Polyalphabetic)

- **Attack Type**: Key Length Recovery in Polyalphabetic Ciphers
- **Target**: Legacy Polyalphabetic Encryption Schemes
- **Vulnerability**: Key reuse in multishift ciphers
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full message recovery via repeating patterns
- **Tools**: CrypTool, Paper & Pencil
- **Scenario**: When ciphers use repeating keys (like Vigenère), repeated plaintext causes repeated ciphertext blocks. Known text helps identify key length.
- **Attack Steps**: Step 1: Intercept a long ciphertext encrypted with a polyalphabetic cipher like Vigenère. Step 2: Look for repeated patterns of ciphertext (e.g., “XBT” repeated multiple times). Step 3: Measure the distance between these repeated sequences (in characters). Step 4: Use common divisors of these distances to estimate key length. Step 5: Once key length is known, split ciphertext into segments where each segment is encrypted with a single Caesar shift. Step 6: Use frequency analysis or known plaintext to solve each Caesar shift. Step 7: Reconstruct full key and decrypt the ciphertext. Step 8: Known phrases can help validate or guess full key. Step 9: This method is historical but still valid in weak proprietary crypto.
- **Detection**: Detect ciphertext patterns and distances between repetitions
- **Solution**: Use randomized keys and initialization vectors; avoid repeating-key schemes
- **Tags**: Vigenère, Classical, Kasiski, Frequency Analysis

## AES ECB Block Reconstruction

- **Attack Type**: Block Mapping with Known Plaintext
- **Target**: AES-ECB Encrypted Messages or Files
- **Vulnerability**: ECB reveals structure, allows oracle-like lookup
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Partial or full message reconstruction
- **Tools**: CyberChef, Burp Suite, Hex Viewer
- **Scenario**: AES in ECB mode encrypts identical plaintext blocks into identical ciphertext blocks. Known blocks help reveal structure.
- **Attack Steps**: Step 1: Observe encrypted messages or files suspected to use AES in ECB mode. Step 2: Look for repeating 16-byte ciphertext blocks — this indicates repeated plaintext. Step 3: Guess common plaintext segments (e.g., padding, "admin=true", fixed headers). Step 4: Encrypt those guessed plaintexts locally using same key (if partially known) or compare against captured ciphertext. Step 5: If ciphertext blocks match, attacker knows which plaintext is where. Step 6: Attackers can build a block dictionary mapping plaintext to ciphertext and vice versa. Step 7: Use this to reconstruct full plaintext messages. Step 8: Attack is possible even without knowing the full key. Step 9: Prevent by avoiding ECB mode altogether.
- **Detection**: Detect repeated ciphertext blocks; pattern frequency analysis
- **Solution**: Never use ECB; switch to AES-GCM or CBC with IV & MAC
- **Tags**: AES, ECB, Block Pattern, Known Plaintext

## CBC IV Recovery with Known P

- **Attack Type**: Initialization Vector Leak via Known Text
- **Target**: AES-CBC and other CBC-mode implementations
- **Vulnerability**: Fixed IVs and known headers
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: IV recovery, pattern replay, injection risk
- **Tools**: CyberChef, Python Script
- **Scenario**: In CBC mode, if attacker knows plaintext and first block of ciphertext, they can recover the IV and use it for other attacks or pattern correlation.
- **Attack Steps**: Step 1: Capture a CBC-encrypted message with known plaintext for the first block (e.g., HTTP header, XML tag). Step 2: Extract the first ciphertext block (C1). Step 3: Use the formula: IV = C1 ⊕ P1 (where P1 is the known plaintext). Step 4: Once the IV is recovered, attacker may infer chaining structure or reuse it in crafted messages if IVs are predictable or reused. Step 5: This helps with block guessing, padding oracle attacks, and pattern injection. Step 6: This attack is common when IV is fixed or sent separately from ciphertext. Step 7: Prevent this by using random, unique IVs for every encryption.
- **Detection**: Monitor IV reuse and static values; check XOR patterns between C1 and expected P1
- **Solution**: Use randomized, per-message IVs; never allow user-supplied IVs
- **Tags**: CBC Mode, IV Recovery, KPA, Known Headers

## KPA in DES Known Weak Keys

- **Attack Type**: Decryption via Weak DES Keys and Known Plaintext
- **Target**: DES-based Systems or Legacy Devices
- **Vulnerability**: Use of known weak keys in DES
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Full decryption using weak key sets
- **Tools**: Hashcat, John the Ripper, DES Cracker Tool
- **Scenario**: DES has known weak keys that produce predictable output. If plaintext is known, attacker can brute-force using only these few weak keys to decrypt ciphertext.
- **Attack Steps**: Step 1: Intercept a ciphertext believed to be encrypted using the DES algorithm. Step 2: Confirm or guess part of the corresponding plaintext (e.g., common headers or known structure). Step 3: Use a predefined list of DES weak keys — there are 16 known weak/semi-weak keys. Step 4: Decrypt the ciphertext using each weak key and check if any result matches the known plaintext. Step 5: If match is found, the weak key is confirmed, allowing decryption of full message. Step 6: Repeat the attack on other ciphertexts encrypted with same or similar configuration. Step 7: This works faster than brute-forcing all 2⁵⁶ DES keys. Step 8: Highlight that DES is outdated and insecure by modern standards.
- **Detection**: Look for repeated weak key IDs; compare decrypted headers with known formats
- **Solution**: Avoid DES; upgrade to AES or 3DES minimum; never allow weak key reuse
- **Tags**: DES, Weak Key, Known Plaintext, Legacy

## Linear Cryptanalysis (KPA-based)

- **Attack Type**: Key Bit Recovery via Linear Approximations
- **Target**: DES, Lightweight Block Ciphers
- **Vulnerability**: Linear bias in cipher structure
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Partial or full key recovery with enough data
- **Tools**: Custom Scripts, CrypTool, Paper Analysis
- **Scenario**: Given enough known plaintext–ciphertext pairs, attacker uses statistical biases in cipher to build linear equations about the key.
- **Attack Steps**: Step 1: Collect a large set (e.g., 1000+) of known plaintext and corresponding ciphertext pairs encrypted with the same key. Step 2: Analyze the cipher (typically block cipher like DES) to identify linear relationships between bits of plaintext, ciphertext, and key. Step 3: Use these patterns to create linear approximations (equations) that are statistically more likely to be true. Step 4: Count how often these approximations hold true across all pairs. Step 5: Use bias to guess key bits—certain equations will leak certain bits. Step 6: Combine guesses to build a partial or full key. Step 7: Validate guesses by encrypting plaintext and comparing to ciphertext. Step 8: Often used on DES and simplified cipher versions. Step 9: Requires a lot of data and mathematical analysis.
- **Detection**: Detect large queries with known input/output pattern analysis
- **Solution**: Use modern block ciphers with no linear leakage; AES is immune to known linear cryptanalysis
- **Tags**: DES, Linear Crypto, Statistical Bias, KPA

## Differential Cryptanalysis (KPA Variant)

- **Attack Type**: Key Recovery via Input Difference Analysis
- **Target**: Block Ciphers with Predictable Structure
- **Vulnerability**: Predictable diffusion of input differences
- **MITRE**: T1600 – Weaken Cryptography
- **Impact**: Partial or full key extraction using math
- **Tools**: Custom Analysis Tools, CrypTool
- **Scenario**: Attacker uses known plaintexts with carefully selected differences to detect how differences propagate in ciphertext, revealing key bits.
- **Attack Steps**: Step 1: Prepare pairs of plaintexts that differ in only a few bits (called plaintext differentials). Step 2: Obtain corresponding ciphertexts by intercepting or observing encrypted messages. Step 3: Analyze how small changes in plaintext affect the resulting ciphertext — this helps find a differential characteristic (a pattern that shows how differences propagate). Step 4: Build hypotheses about key bits that cause these differences. Step 5: Repeat across thousands of pairs to confirm consistent patterns. Step 6: Use the information to guess part or all of the encryption key. Step 7: Works best on block ciphers with insufficient diffusion or poor S-boxes. Step 8: Though a known-plaintext attack, it's often enhanced by chosen plaintext. Step 9: DES is particularly vulnerable in early rounds.
- **Detection**: Check for repeating input/output patterns under small differences
- **Solution**: Use ciphers with high diffusion and nonlinear S-boxes (AES); never reuse keys
- **Tags**: Differential, DES, KPA Variant, Statistical

## JWT with Known Payload

- **Attack Type**: JWT Secret Brute Force via Known Payload
- **Target**: Web apps using HMAC-signed JWTs
- **Vulnerability**: Weak secrets used to sign JWTs
- **MITRE**: T1606 – Forge Web Tokens
- **Impact**: Admin impersonation, unauthorized access
- **Tools**: jwt_tool.py, jwt-cracker, Python, Hashcat
- **Scenario**: If attacker knows the full JWT payload (e.g., {"user":"admin"}), they can guess the secret used to sign the token via HMAC brute force.
- **Attack Steps**: Step 1: Attacker captures a JWT (JSON Web Token) used for user authentication. Example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.... Step 2: Decodes the payload and header using base64 decoding (no secret needed). If payload is something common like { "user": "admin" }, the attacker now knows the original payload. Step 3: Attacker generates HMAC-SHA256 signatures using this known payload and a dictionary of common secrets (e.g., "admin", "1234", "secret", etc.). Step 4: They compute JWTs with each key and compare to the original JWT signature. Step 5: When a match is found, the secret is revealed, allowing the attacker to generate arbitrary JWTs (e.g., give themselves admin access). Step 6: This works only if a weak secret is used for signing.
- **Detection**: Alert on modified token structure; log and monitor auth token mismatches
- **Solution**: Use long, random secrets; consider RS256 (asymmetric signing); validate token signature securely
- **Tags**: JWT, HMAC, Token Brute Force, Known Payload

## Encrypted Cookie Analysis

- **Attack Type**: Compare Known Profile to Encrypted Cookie
- **Target**: Web applications with encrypted cookies
- **Vulnerability**: Static or weak keys; ECB pattern reuse
- **MITRE**: T1606 – Session Token Manipulation
- **Impact**: Session hijacking, role escalation
- **Tools**: CyberChef, Burp Suite, Cookie Editor
- **Scenario**: Web apps often store encrypted cookies like session data; if attacker knows plaintext, they can detect reused keys or patterns.
- **Attack Steps**: Step 1: Attacker signs up and logs into a web application that uses encrypted cookies for session or preference storage. Step 2: They view both the plaintext content (e.g., their username, role, preferences) and the corresponding encrypted cookie in browser dev tools or HTTP headers. Step 3: Using CyberChef or Python, attacker encrypts the same known plaintext with various keys until the output matches the observed cookie. Step 4: If the ciphertext matches using a guessed key, the secret is revealed. Step 5: If cookies are not properly randomized (e.g., ECB mode used), similar patterns may emerge for different users. Step 6: Attackers may forge or tamper with cookies to escalate privileges or impersonate users. Step 7: Helps spot poor crypto implementations.
- **Detection**: Look for duplicate cookie patterns; analyze ciphertext lengths and entropy
- **Solution**: Use randomized IVs, AES-GCM mode; sign cookies; avoid storing sensitive data in client-side cookies
- **Tags**: Encrypted Cookies, Known Content, Brute Force

## SSO Token Matching

- **Attack Type**: Session Token Mapping with Known Data
- **Target**: SSO tokens, identity providers
- **Vulnerability**: Predictable structure and reuse of tokens
- **MITRE**: T1606 – Forge Web Tokens
- **Impact**: SSO impersonation, unauthorized access
- **Tools**: Burp Suite, CyberChef, SAML Tracer
- **Scenario**: If attacker knows user identity and profile data, they can correlate encrypted session tokens (SSO) to plaintext data.
- **Attack Steps**: Step 1: Attacker observes encrypted session tokens from SSO (e.g., JWTs, SAML assertions, cookies) during authentication. Step 2: They also know target user data (e.g., "user=john", email, org ID). Step 3: They guess the structure of token payload (e.g., standard fields like sub, email, exp, iss) and attempt to match it with token structure. Step 4: If attacker can guess encryption scheme (e.g., base64-encoded AES or HMAC JWT), they can recreate token inputs. Step 5: Using guessed keys and known data, attacker generates tokens and checks if signature or structure matches original. Step 6: If successful, attacker may impersonate target users or inject arbitrary sessions. Step 7: This is most effective when tokens use predictable format or weak keys.
- **Detection**: Token signing mismatch; repeated field patterns in token decoding
- **Solution**: Use asymmetric signing (RS256); randomize token fields; validate auth server signatures
- **Tags**: SSO, JWT, SAML, Known Identity, Token Abuse

## OAuth Parameter Guessing

- **Attack Type**: Predict OAuth Payload and Tokens
- **Target**: OAuth-based login or API flows
- **Vulnerability**: Predictable or unvalidated state, code, or tokens
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: Account takeover, session hijacking
- **Tools**: curl, Burp Suite, ffuf, wordlists
- **Scenario**: OAuth state, redirect URIs, and access tokens may follow predictable structure — attackers brute-force to forge or hijack sessions.
- **Attack Steps**: Step 1: Attacker initiates an OAuth authentication flow (e.g., via "Login with Google" button). Step 2: Observes parameters passed like state, redirect_uri, and code. Step 3: If these values follow predictable formats (e.g., UUIDs, base64 strings), attacker builds a wordlist or dictionary of expected values. Step 4: They send automated requests trying guessed tokens or crafted authorization codes to the token endpoint. Step 5: If server accepts a forged or replayed code/state, attacker receives access tokens or user sessions. Step 6: May allow session fixation or full account takeover. Step 7: Especially dangerous if state is not validated or secrets are short.
- **Detection**: Monitor token replays; alert on multiple token attempts from same IP
- **Solution**: Use long, random state values; enforce short lifespans for tokens; never accept reused authorization codes
- **Tags**: OAuth, Session Hijack, Parameter Guess, KPA

## Base64 Encrypted URL Patterns

- **Attack Type**: Correlating Known Plaintext with Encoded URLs
- **Target**: Web applications using encoded URL parameters
- **Vulnerability**: Predictable structure of Base64-encoded strings
- **MITRE**: T1606 – Forge Web Tokens
- **Impact**: URL manipulation, privilege escalation, information leakage
- **Tools**: CyberChef, Burp Suite, Base64 Decoders, Browser DevTools
- **Scenario**: Web apps often use base64 encoding to hide parameters in URLs (e.g., user=admin). If attacker knows structure, they can reverse-engineer original content.
- **Attack Steps**: Step 1: Attacker observes URLs like example.com?id=YWRtaW4= or similar suspicious long strings in GET/POST parameters. Step 2: Decodes the Base64 string using tools like CyberChef or browser console (atob() function). Step 3: If decoded value matches known or guessable plaintext (e.g., admin, user_id=5, role=superuser), attacker confirms encoding pattern. Step 4: Modifies the encoded value (e.g., change admin to root, re-encode with Base64). Step 5: Sends manipulated request to the server. Step 6: If server accepts new request (without validating changes), attacker gains elevated access or reads unauthorized data. Step 7: Helps in identifying insecure data encoding rather than true encryption. Step 8: Repeat with known URL paths or IDs.
- **Detection**: Analyze incoming encoded fields; check for known Base64 patterns
- **Solution**: Never rely on encoding for security; encrypt and sign sensitive parameters
- **Tags**: Base64, URL Tampering, Known Plaintext, KPA

## NTLMv2 Challenge-Response (Windows)

- **Attack Type**: Cracking NTLM Hashes via Known Challenges
- **Target**: Windows authentication systems using NTLMv2
- **Vulnerability**: Known-plaintext reduces entropy of NTLMv2 hash cracking
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: Full credential compromise, lateral movement
- **Tools**: Hashcat, Impacket, responder.py
- **Scenario**: NTLMv2 uses challenge-response for authentication. If the challenge or parts of response are known, keys can be cracked.
- **Attack Steps**: Step 1: Attacker captures an NTLMv2 authentication exchange (e.g., via MITM, responder attack, or SMB relay). Step 2: Extracts the NTLMv2 hash, challenge, and response from the captured network traffic. Step 3: If challenge is standard or guessable (e.g., replayed or predictable), and attacker knows part of plaintext (like domain or username), they can reduce brute-force search space. Step 4: Uses hashcat or john with custom NTLM cracking mode and dictionary to try password guesses. Step 5: Once the password is cracked, attacker can impersonate user across the network (pass-the-hash). Step 6: Effective in environments using SMB, LDAP, or remote desktop with NTLM auth. Step 7: Repeat attack to escalate privileges.
- **Detection**: Monitor NTLM relay attempts, SMB/LDAP anomalies, challenge reuse
- **Solution**: Enforce Kerberos over NTLM; disable SMBv1; rotate passwords frequently
- **Tags**: NTLM, SMB, MITM, Credential Brute Force, KPA

## Kerberos Ticket Decryption

- **Attack Type**: Known Fields Used to Crack Encrypted Tickets
- **Target**: Kerberos auth systems in Windows domains
- **Vulnerability**: Guessable structure in encrypted tickets
- **MITRE**: T1558 – Kerberoasting
- **Impact**: Domain persistence, impersonation of services or users
- **Tools**: Rubeus, Kerbrute, Mimikatz
- **Scenario**: Kerberos tickets encrypt user data. If some plaintext (like username or domain) is known, attackers can guess keys.
- **Attack Steps**: Step 1: Attacker gains access to a Kerberos environment (e.g., internal Active Directory). Step 2: Captures a Kerberos TGT or TGS ticket using tools like Rubeus or Mimikatz. Step 3: Analyzes ticket structure — many fields like timestamp, username, realm are guessable or known. Step 4: Uses these known fields to mount dictionary or brute-force attack against the encrypted part of ticket (e.g., RC4 or AES keys). Step 5: If password or service ticket key is weak, attacker can decrypt ticket and impersonate users or services. Step 6: This is a variant of the known plaintext attack (KPA) because of deterministic structure of Kerberos. Step 7: Can be used in Golden Ticket or Silver Ticket attacks.
- **Detection**: Alert on abnormal TGT/TGS issuance; log analysis for replayed tickets
- **Solution**: Enforce long, random passwords for service accounts; enable AES encryption for Kerberos
- **Tags**: Kerberos, Ticket Cracking, AD, KPA

## Encrypted Email Attachments (PGP)

- **Attack Type**: Guess Structure of Encrypted Email or Attachment
- **Target**: PGP/GPG encrypted email or files
- **Vulnerability**: Known message structure leaks content under encryption
- **MITRE**: T1114 – Email Collection
- **Impact**: Privacy breach, information leakage
- **Tools**: GPGTools, PGPy, MailSniper
- **Scenario**: PGP encrypts attachments. If attacker knows filename or plaintext intro, can test guesses against ciphertext blocks.
- **Attack Steps**: Step 1: Attacker intercepts an encrypted email (e.g., .pgp, .asc, or encrypted attachment). Step 2: If they know what the file likely contains (e.g., "Invoice for July 2025"), they can create plaintext guesses. Step 3: Encrypt those plaintexts using PGP with a guessed key and compare resulting ciphertext blocks with intercepted email. Step 4: If match is found, attacker confirms key or reveals content. Step 5: In some cases, metadata or filenames may also be leaked in cleartext. Step 6: Repeat with different guessed content or templates (e.g., recurring messages). Step 7: May also help brute-force weak passphrases if passphrase-encrypted PGP keys are used.
- **Detection**: Alert on unusual key usage; prevent email leakage via external SMTP
- **Solution**: Use strong passphrases for PGP keys; compress content before encrypting; consider email tokenization for sensitive data
- **Tags**: PGP, Email, Attachment, Brute Force, Known Plaintext

## Secure Messaging App Replay

- **Attack Type**: Known Intro Text Enables Replay or Recovery
- **Target**: Secure messaging apps (Signal, WhatsApp, etc.)
- **Vulnerability**: Predictable intro text leaks encrypted message content
- **MITRE**: T1110.003 – Brute Force: Password Cracking
- **Impact**: Message recovery, impersonation, replay attack
- **Tools**: Burp Suite, Frida, mitmproxy, Mobile Emulator
- **Scenario**: Encrypted messages in apps like Signal or WhatsApp often start with predictable text (e.g., “Hey” or “Hi”), making it easier to correlate with ciphertext blocks.
- **Attack Steps**: Step 1: Attacker intercepts encrypted messages from a secure messaging app via network sniffing, device memory, or storage. Step 2: Analyzes ciphertext patterns and notices repeated ciphertext blocks at the start of multiple messages. Step 3: Based on user behavior (e.g., always starting with "Hey", "Hello", "Meeting at..."), attacker creates a list of probable intro phrases. Step 4: Encodes these into plaintext guesses and observes which ciphertext blocks match intercepted encrypted messages. Step 5: Confirms correct match via ciphertext consistency. Step 6: Uses this information to partially reconstruct message content or perform message replay (resend previous encrypted blocks to manipulate conversation flow). Step 7: May chain with social engineering for full context or session hijack.
- **Detection**: Monitor for repeated encrypted blocks; alert on abnormal message timing and sizes
- **Solution**: Use randomized padding or context-specific intro strings; enforce unique nonces and session keys per message
- **Tags**: Messaging App, Encrypted Replay, Predictable Plaintext

## KPA in Encrypted Cloud Backups

- **Attack Type**: Backup Metadata and Headers Leak Structure
- **Target**: Encrypted personal or enterprise cloud backups
- **Vulnerability**: Metadata patterns and default paths are known
- **MITRE**: T1552.004 – Unsecured Credentials: Cloud Storage
- **Impact**: Sensitive metadata exposure, backup structure leakage
- **Tools**: CyberChef, backup extractor tools, forensic software
- **Scenario**: Encrypted cloud backups often contain known headers, filenames, and folder structures (e.g., “Documents”, “Photos”) that aid KPA.
- **Attack Steps**: Step 1: Attacker obtains access to an encrypted cloud backup (e.g., iCloud, Google Drive, Dropbox backup file). Step 2: Examines the encrypted archive or backup file for recurring patterns or block headers. Step 3: Guesses that default folder names (e.g., Documents/, DCIM/) or common filenames (e.g., resume.pdf, budget.xlsx) are inside. Step 4: Creates local versions of those folders/files, encrypts them using the same backup tool or scheme. Step 5: Compares ciphertext of known structures with encrypted archive blocks. Step 6: Matches are used to derive partial or full structure of the archive without decryption. Step 7: Can leak filenames, paths, even timestamps — leading to sensitive metadata exposure or targeted brute-force attempts on full content.
- **Detection**: Analyze backup uploads for known headers; log repeated block patterns
- **Solution**: Encrypt and compress backups; strip metadata; randomize filenames during archive creation
- **Tags**: Cloud Backup, Metadata KPA, Backup Enumeration

## KPA against IoT Firmware Updates

- **Attack Type**: Predictable Firmware Contents Aid Key Recovery
- **Target**: IoT firmware over-the-air (OTA) updates
- **Vulnerability**: Known strings and static logs reused in firmware
- **MITRE**: T1542.001 – Pre-OS Boot: System Firmware
- **Impact**: Device takeover, firmware tampering, persistence
- **Tools**: Binwalk, firmware dumpers, strings, Ghidra
- **Scenario**: IoT device firmware updates often contain known strings (e.g., boot logs, version headers), helping attackers reverse encryption.
- **Attack Steps**: Step 1: Attacker extracts or intercepts an encrypted firmware update file from an IoT device (e.g., via OTA traffic or SD card). Step 2: Assumes some content in the update is standard — such as “Booting device...”, “Firmware version 1.0.0”, ASCII logos, config file headers, etc. Step 3: Using known plaintexts and observed ciphertext, attacker builds a mapping to infer encryption algorithm (e.g., AES-CBC) and checks block alignment. Step 4: Brute-forces or narrows keyspace using patterns and validates findings against extracted blocks. Step 5: May chain with firmware emulation or modification to implant malicious code. Step 6: Final result enables reverse engineering, key recovery, or firmware tampering. Step 7: Particularly impactful if firmware is signed poorly or stored unencrypted after boot.
- **Detection**: Monitor firmware update delivery; verify firmware cryptographic signatures and content validation
- **Solution**: Use unique keys per device; encrypt firmware with strong AES/GCM or signed updates; compress firmware to reduce known structures
- **Tags**: IoT, Firmware, Encrypted Update KPA

## Encrypted Logs in SIEM Tools

- **Attack Type**: Predictable Log Formats Aid Known Plaintext Recovery
- **Target**: SIEM log storage or encrypted syslog systems
- **Vulnerability**: Standard log formats leak data structure under cipher
- **MITRE**: T1005 – Data from Local System
- **Impact**: Log disclosure, alert evasion, attacker activity masking
- **Tools**: SIEM platform (e.g., Splunk, QRadar), hexdump, regex tools
- **Scenario**: Security logs encrypted before export (e.g., syslog over TLS or archived logs) may contain predictable structures attackers can leverage.
- **Attack Steps**: Step 1: Attacker gains access to archived or transmitted encrypted log files from a SIEM tool. Step 2: Analyzes ciphertext and guesses likely repeated patterns — e.g., timestamps like 2025-07-16 12:00:00, log level indicators (INFO, ERROR), or JSON field headers. Step 3: Encodes known log templates and compares resulting ciphertext with the actual log blocks. Step 4: Confirms match and begins mapping plaintext to ciphertext byte-by-byte. Step 5: Builds a partial decryption model or block matcher to infer additional log lines. Step 6: Repeats attack with other templates or builds dictionary of probable log entries. Step 7: Can reveal sensitive activity logs, PII, or security configuration info.
- **Detection**: Monitor for repeated ciphertext in encrypted logs; validate that padding/random IVs are used
- **Solution**: Use randomized IVs and padding in log encryption; compress logs before encrypting; rotate encryption keys periodically
- **Tags**: SIEM, Logs, KPA, Encrypted Event Logs

## Hardcoded Key KPA in IoT

- **Attack Type**: KPA via Static Key in Firmware
- **Target**: IoT Devices (routers, sensors, smart plugs, etc.)
- **Vulnerability**: Use of static encryption key shared across all devices
- **MITRE**: T1552.001 – Credentials in Files
- **Impact**: Full device decryption, firmware backdoors, data exfiltration
- **Tools**: Binwalk, Ghidra, Hex Fiend, CyberChef
- **Scenario**: Many IoT devices use hardcoded keys inside firmware. If even a part of the message structure is known (e.g., JSON, log strings), the key can often be reverse engineered.
- **Attack Steps**: Step 1: Attacker downloads or extracts firmware from the IoT device (via vendor site, device memory dump, or update interception). Step 2: Analyzes firmware using tools like binwalk or Ghidra to extract embedded strings and binaries. Step 3: Identifies hardcoded keys or repeated constants used for encryption (e.g., AES_KEY = "1234567890abcdef"). Step 4: Observes encrypted traffic or files generated by the IoT device. Step 5: Matches parts of the ciphertext to guessed plaintext formats like JSON headers, fixed phrases ("device started", "temp reading"). Step 6: Using known input-output patterns and the extracted hardcoded key, the attacker confirms correct decryption. Step 7: May use this to decrypt all messages or craft fake firmware updates/data packets.
- **Detection**: Monitor firmware changes; detect shared key usage via key fingerprints
- **Solution**: Use per-device encryption keys; obfuscate and rotate keys regularly in firmware; never embed raw crypto keys
- **Tags**: IoT, KPA, Hardcoded Key, Firmware Reversal

## Scapy with Known Payload Injection

- **Attack Type**: KPA via Network Payload Injection
- **Target**: Encrypted APIs, VPNs, IoT command interfaces
- **Vulnerability**: Weak block cipher usage or repeated patterns
- **MITRE**: T1201 – Input Capture
- **Impact**: Protocol reversal, traffic injection, data leakage
- **Tools**: Scapy, Wireshark, tshark, mitmproxy
- **Scenario**: Security testers send known plaintext network packets to encrypted services and observe if encrypted response contains matching blocks, revealing crypto patterns.
- **Attack Steps**: Step 1: Attacker or security tester sends crafted packets using Scapy, embedding known plaintext strings (e.g., "TEST123", "PING", "USER=admin"). Step 2: Targets services that encrypt responses (like VPN tunnels, TLS-wrapped protocols, IoT command channels). Step 3: Captures the encrypted response and inspects ciphertext blocks via Wireshark or tshark. Step 4: Looks for matching encrypted blocks in response or repeated blocks across multiple attempts. Step 5: If same plaintext leads to same ciphertext (e.g., due to ECB mode or static IV), attacker maps plaintext-ciphertext pairs. Step 6: With enough pairs, attacker can partially decrypt future messages or detect weak cipher usage. Step 7: Helpful in auditing proprietary or unknown encryption protocols.
- **Detection**: Monitor for repeated ciphertext blocks; alert on encrypted traffic anomalies
- **Solution**: Use randomized IVs, secure cipher modes like AES-GCM or ChaCha20-Poly1305
- **Tags**: Scapy, KPA, Encrypted Payload Injection

## CTF Challenges with Oracle Output

- **Attack Type**: Educational KPA via Simulated Crypto Oracle
- **Target**: CTF crypto oracles, simulated web apps
- **Vulnerability**: Predictable output leaks cipher structure
- **MITRE**: T1003 – OS Credential Dumping
- **Impact**: Flag decryption, protocol reversal, attacker training
- **Tools**: netcat, Python, pwntools, custom CTF challenge platforms
- **Scenario**: Capture-the-Flag (CTF) events simulate encryption/decryption oracles where part of the plaintext is known or output is partially revealed.
- **Attack Steps**: Step 1: Attacker connects to a crypto challenge hosted remotely (often via netcat or web interface) where an encrypted value is returned. Step 2: Notices the encrypted value always includes a known prefix or suffix (e.g., "flag{", "Hello user"). Step 3: Builds a dictionary of known plaintexts and their corresponding ciphertexts. Step 4: Exploits this pattern to reverse engineer the cipher or guess the full message. Step 5: May perform byte-at-a-time guessing by brute-forcing single characters until the correct ciphertext match is seen. Step 6: Repeats until full plaintext is recovered. Step 7: This trains attackers in real-world known-plaintext decryption, useful for later pentesting and red teaming.
- **Detection**: In CTFs, not usually detected; in real systems, monitor repeated inputs or timing analysis
- **Solution**: Enforce randomized inputs, unique sessions; in training, use for educational KPA experience only
- **Tags**: CTF, Oracle, KPA, Byte-at-a-time Decryption

## CryptoPal Challenges - KPA Simulations

- **Attack Type**: Known-Plaintext Labs for Cryptanalysis Learning
- **Target**: Student crypto labs, Red Team training, CTF preparation
- **Vulnerability**: Educational simulations with known input-output pairs
- **MITRE**: T1201 – Input Capture
- **Impact**: Cryptographic intuition building, offensive skill training
- **Tools**: Python, OpenSSL CLI, CryptoPal Labs
- **Scenario**: CryptoPal (by Matasano/Trail of Bits) provides step-by-step labs where users attack simple ciphers using known inputs to understand KPA.
- **Attack Steps**: Step 1: Learner downloads CryptoPal challenges (a series of progressive crypto attack labs). Step 2: Starts with simple XOR and ECB challenges where they know plaintext like "AAAAAAAAAAAAAAAA". Step 3: Encrypts this plaintext and observes repeating ciphertext blocks — revealing cipher structure (ECB mode). Step 4: Learner writes code to match known plaintext with ciphertext and brute-force unknown segments. Step 5: Advances to CBC, CTR, padding oracle, and timing attacks with known-message simulation. Step 6: This hands-on KPA training helps users understand cipher weaknesses and how block alignment matters. Step 7: Eventually, user develops scripts and tooling that can be applied in real-world scenarios.
- **Detection**: No detection needed – used for learning in controlled labs
- **Solution**: Use to build red team capability; teaches limits of poor encryption designs
- **Tags**: CryptoPal, KPA Labs, Cryptanalysis Training

## Simple Timing Attack

- **Attack Type**: Basic Timing Analysis for Key Guessing
- **Target**: Login Pages, Decryption APIs
- **Vulnerability**: Operation time leaks internal logic
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Secret key or password recovery
- **Tools**: Python, stopwatch, curl, custom script
- **Scenario**: Timing how long it takes to perform operations (e.g., RSA decryption or login attempt) can reveal information about key bits or password validity.
- **Attack Steps**: Step 1: Choose a cryptographic process that involves conditional logic (e.g., RSA decryption, password check, login page). Step 2: Repeatedly send inputs to the system while measuring response time in milliseconds (e.g., via Python requests, curl + time command). Step 3: Slightly vary input and observe if time increases or decreases (e.g., correct characters cause more operations, thus more time). Step 4: Gradually guess each bit/character of secret value based on response times. Step 5: Use statistical averaging over multiple requests to reduce noise. Step 6: Repeat until full key or password is guessed. Step 7: Use automation to script the attack for accuracy.
- **Detection**: Monitor for repeated timed access patterns; analyze network latency anomalies
- **Solution**: Introduce constant-time operations in code; add random delay; avoid early exit in comparisons
- **Tags**: Timing Attack, RSA, Password Guessing

## RSA Decryption Timing (CRT Leak)

- **Attack Type**: CRT-Based RSA Decryption Timing Side-Channel
- **Target**: RSA Decryption APIs, TLS endpoints
- **Vulnerability**: Poor error handling in CRT operations
- **MITRE**: T1201 – Input Capture
- **Impact**: Full RSA key recovery
- **Tools**: RsaCtfTool, OpenSSL, stopwatch, Python
- **Scenario**: In RSA implementations that use Chinese Remainder Theorem (CRT) for speed, timing differences can reveal d, the private exponent.
- **Attack Steps**: Step 1: Identify a target that uses RSA decryption and supports ciphertext input (e.g., TLS server, JWT decryption API). Step 2: Craft multiple ciphertexts and send them to be decrypted. Step 3: Measure the decryption time for each ciphertext using automation (e.g., time in Linux or Python time.perf_counter()). Step 4: If implementation uses CRT, decryption with faulty ciphertext causes different error handling paths (e.g., divide-by-zero or failed mod inverse). Step 5: Use these timing differences to infer parts of the private exponent d. Step 6: Combine with mathematical methods (e.g., Coppersmith's attack) to fully recover private key.
- **Detection**: Analyze decryption failures and time anomalies
- **Solution**: Validate all RSA inputs; use blinding techniques during decryption; ensure constant time error handling
- **Tags**: RSA, CRT, Side Channel, Timing Leak

## AES Lookup Timing (T-table leak)

- **Attack Type**: Cache Timing in AES Table-based Implementations
- **Target**: Local process, shared hardware
- **Vulnerability**: Memory access reveals AES internal structure
- **MITRE**: T1185 – Man-in-the-Middle
- **Impact**: AES key recovery in shared CPU environments
- **Tools**: flush+reload attack scripts, perf, Valgrind, rdtsc
- **Scenario**: AES implementations using T-tables (lookup tables) can leak key bits via memory/cache access timing.
- **Attack Steps**: Step 1: Target system must use table-based AES (common in older software and embedded systems). Step 2: Attacker runs code (or malware) on same hardware (VM or shared CPU core). Step 3: Use cache timing tools to observe which memory locations (T-table entries) are accessed during AES execution. Step 4: Use flush+reload technique: flush specific cache lines, run encryption, and measure reload time. Step 5: Correlate access patterns to specific key bits (e.g., if T-box index reveals byte of plaintext XORed with key). Step 6: Repeat across many encryptions and inputs to reconstruct full key.
- **Detection**: Use constant-time AES implementations (e.g., AES-NI); prevent cross-VM memory sharing
- **Solution**: Disable T-table based crypto; enforce AES-NI hardware acceleration; isolate VMs by CPU core
- **Tags**: AES, Side Channel, Cache Timing

## Web Timing via JavaScript

- **Attack Type**: JavaScript Timing Side-Channel in Browsers
- **Target**: Browsers, Web Apps, JavaScript Engines
- **Vulnerability**: High-res timers reveal crypto behavior
- **MITRE**: T1185 – Browser-based Side Channel
- **Impact**: Password or token guessing via JS timing
- **Tools**: JS timing APIs (performance.now), Chrome DevTools
- **Scenario**: JavaScript in web pages can measure precise browser execution time to infer behavior of password checks, crypto routines, or CSP enforcement.
- **Attack Steps**: Step 1: Attacker injects or hosts a malicious web page that executes JavaScript in victim's browser (e.g., via phishing or XSS). Step 2: JavaScript uses performance.now() or Date.now() to measure time taken by different operations (e.g., iframe loading, CSP rejection, cookie read attempts). Step 3: If target site includes crypto operations (like verifying a JWT or password) within iframe or web worker, attacker can estimate if operation succeeded based on execution time. Step 4: Attacker repeats with different inputs or conditions and builds timing profile. Step 5: Timing variance reveals logic behind the scenes — such as length of correct password prefix or CSP status.
- **Detection**: Monitor iframe loads, CSP eval times, and JavaScript performance API usage
- **Solution**: Disable high-res timers in sensitive contexts; add noise or delays in client-side crypto or logic checks
- **Tags**: JavaScript, Timing, Browser Exploits

## Password Timing Attack

- **Attack Type**: Timing-Based Password Validation Leak
- **Target**: Web login forms or APIs
- **Vulnerability**: Non-constant-time string comparison
- **MITRE**: T1201 – Input Capture
- **Impact**: Full password recovery
- **Tools**: curl, Burp Suite, custom Python script with time module
- **Scenario**: Web apps often compare passwords character by character, causing longer response times when initial characters are correct.
- **Attack Steps**: Step 1: Identify a web login form or API endpoint that returns faster if the password is wrong and slower if the initial characters are correct. Step 2: Use a script to send password attempts one character at a time, starting with common characters (e.g., ‘a’, ‘b’, …). Step 3: Measure the time taken for each login attempt using tools like time or requests with time.perf_counter() in Python. Step 4: If a password guess with ‘a’ takes longer than one with ‘z’, assume ‘a’ is correct. Step 5: Continue adding one character at a time, measuring response duration at each step. Step 6: Repeat and average results to reduce network noise. Step 7: Eventually reconstruct the entire password using this technique. Step 8: Use rate-limiting or CAPTCHA as a detection bypass method.
- **Detection**: Monitor for repeated timed login attempts and abnormal delay profiles
- **Solution**: Implement constant-time password comparison functions (e.g., hmac.compare_digest()); add response timing randomization
- **Tags**: Timing Attack, Password Guessing, Authentication

## Simple Power Analysis (SPA)

- **Attack Type**: SPA – Direct Power Trace Observation
- **Target**: Smart cards, hardware crypto chips
- **Vulnerability**: Key-dependent power variations
- **MITRE**: T1208 – Hardware Abuse
- **Impact**: Private key extraction from embedded hardware
- **Tools**: Oscilloscope, ChipWhisperer, Smartcard Reader
- **Scenario**: Observes power usage of a crypto device (e.g., smart card or IoT chip) to infer operations such as key bits or branching logic directly from signal peaks.
- **Attack Steps**: Step 1: Connect a power analysis tool (like ChipWhisperer or oscilloscope) to a device that performs cryptographic operations (e.g., smart card, RFID tag, IoT chip). Step 2: Capture power traces during key operations (encryption, signing). Step 3: Look for visible patterns in the power consumption — different instructions (e.g., multiplication vs. addition) use different amounts of power. Step 4: If the device uses branches depending on key bits (e.g., if bit == 1 then multiply), those can be spotted as peaks or valleys in the trace. Step 5: Decode these visual patterns into binary key values manually or using tools. Step 6: Reconstruct the private key over multiple runs. Step 7: Repeat to confirm consistency.
- **Detection**: Analyze physical access logs; monitor device activity under external probes
- **Solution**: Implement constant-power algorithms (e.g., bitsliced AES); use shielding; detect physical tampering
- **Tags**: Power Analysis, Side Channel, Embedded Crypto

## Differential Power Analysis (DPA)

- **Attack Type**: DPA – Statistical Power Trace Correlation
- **Target**: Smartcards, IoT devices, AES hardware
- **Vulnerability**: Tiny key-related power differences
- **MITRE**: T1208 – Hardware Abuse
- **Impact**: AES or RSA key recovery; device clone or impersonation
- **Tools**: ChipWhisperer, Python (NumPy, SciPy), Oscilloscope
- **Scenario**: Uses multiple power consumption traces and statistical methods (correlation, averaging) to extract secret key from slight signal differences caused by key usage.
- **Attack Steps**: Step 1: Collect hundreds or thousands of power consumption traces from a crypto device (e.g., during AES encryption) using a connected oscilloscope or ChipWhisperer. Step 2: Send known inputs to the device while capturing traces (plaintext or ciphertext, depending on attack direction). Step 3: For each trace, record the power consumption over time. Step 4: Use statistical techniques like difference-of-means, correlation power analysis (CPA), or variance clustering to detect tiny variations that depend on key bits. Step 5: Build a model of expected power behavior for different key guesses. Step 6: Compare real traces to predicted traces for each key candidate. Step 7: The candidate with best correlation is likely the correct key. Step 8: Repeat for other key bytes until the full key is recovered. Step 9: Use scripting to automate comparison and filtering of results.
- **Detection**: Detect large trace sampling or USB probing; monitor EM leaks or RF patterns
- **Solution**: Mask cryptographic operations; randomize execution order; add noise in power draw
- **Tags**: DPA, Side Channel, Statistical Crypto Attack

## High-Order Differential Power Analysis (HO-DPA)

- **Attack Type**: HO-DPA – Advanced Multi-Point Analysis
- **Target**: Cryptographic hardware (e.g., HSMs)
- **Vulnerability**: Masked key handling still leaks power info
- **MITRE**: T1211 – Exploitation of User Execution
- **Impact**: Break high-assurance crypto implementations
- **Tools**: ChipWhisperer Pro, MATLAB, ScaLite
- **Scenario**: Targets devices with strong DPA countermeasures by analyzing joint statistical relations across multiple time points in power traces.
- **Attack Steps**: Step 1: Target a hardened crypto device that uses masking (splitting key bits into random shares) to resist standard DPA. Step 2: Capture thousands of power traces while supplying known plaintexts. Step 3: Instead of analyzing a single point, perform joint correlation analysis across multiple points in the trace where shares combine. Step 4: Use multi-variate statistical tools like multivariate linear regression or joint entropy analysis to find weak correlations. Step 5: Look for combinations of time offsets that reduce entropy around a specific key bit. Step 6: Filter and correlate only on high-variance segments across traces. Step 7: Map high-order leaks back to actual key components. Step 8: Iterate over multiple encryption operations to refine guesses. Step 9: Validate recovered keys through encryption test or ciphertext match.
- **Detection**: Monitor external signal capture attempts; EM shielding; trace noise
- **Solution**: Use higher-order masking schemes; shuffle instruction order; monitor signal integrity
- **Tags**: HO-DPA, Advanced Side-Channel, Crypto Forensics

## Correlation Power Analysis (CPA)

- **Attack Type**: CPA – Statistical Side-Channel Attack
- **Target**: Embedded cryptographic hardware
- **Vulnerability**: Key-dependent power variations
- **MITRE**: T1208 – Hardware Abuse
- **Impact**: Full AES key recovery
- **Tools**: ChipWhisperer, Python (SciPy), Oscilloscope
- **Scenario**: Attacker measures correlation between the power usage of a device and hypothetical intermediate values to recover cryptographic keys.
- **Attack Steps**: Step 1: Connect a ChipWhisperer or oscilloscope to a cryptographic device (e.g., smart card or embedded board). Step 2: Provide the device with hundreds of known plaintexts and capture corresponding power traces. Each trace should record the power consumption over time during an encryption operation (e.g., AES). Step 3: For each possible key guess (e.g., for each AES byte), compute the hypothetical intermediate value (e.g., output of S-box). Step 4: Apply a power model like Hamming Weight to estimate the expected power usage for that guess. Step 5: Calculate the Pearson correlation coefficient between the actual power trace and the hypothetical model. Step 6: The key guess with the highest correlation is likely correct. Step 7: Repeat for each byte of the key. Step 8: Validate the full key by encrypting a known plaintext and comparing it to the known ciphertext. Step 9: Optional: Filter traces to reduce noise or align them precisely before analysis.
- **Detection**: Monitor repeated encryption patterns and USB/serial probing
- **Solution**: Use masking, power randomization, or dual-rail logic in hardware
- **Tags**: CPA, Side-Channel, AES, Cryptanalysis

## Template Attacks

- **Attack Type**: High-Precision Profiling Side-Channel
- **Target**: Smartcards, crypto ICs
- **Vulnerability**: Consistent, repeatable power patterns
- **MITRE**: T1211 – User Execution Exploitation
- **Impact**: Extremely accurate key recovery (1-5 traces possible)
- **Tools**: ChipWhisperer, ScaLite, R or Python (SciKit-learn)
- **Scenario**: Attackers collect detailed power measurements for known operations to build statistical "templates," then match unknown traces to these templates.
- **Attack Steps**: Step 1: In a lab setting, obtain a device identical to the target (same crypto chip or smartcard). Step 2: Run many encryption operations on this device with known keys and plaintexts. Step 3: Capture very detailed power traces for each known operation (e.g., AES S-box input/output). Step 4: Analyze these traces to build a profile ("template") of what the power consumption looks like for specific intermediate states (using statistical classifiers like Gaussian mixture models or linear discriminant analysis). Step 5: Once templates are built, target the real device. Step 6: Capture power traces from it during unknown encryption. Step 7: Match these unknown traces against the templates to infer key-dependent operations. Step 8: Piece together full key from matched results. Step 9: Requires advanced statistics knowledge and clean lab setup but is extremely accurate.
- **Detection**: Detect lab-style profiling behavior; monitor for physical access or excessive test cycles
- **Solution**: Add execution randomness; restrict high-precision timing access; use non-deterministic crypto cores
- **Tags**: Side-Channel, Template Attack, Statistical Analysis

## EM Radiation Capture

- **Attack Type**: Electromagnetic Side-Channel Attack
- **Target**: Hardware wallets, smartcards, chips
- **Vulnerability**: EM leakage during computation
- **MITRE**: T1208 – Hardware Abuse
- **Impact**: Full cryptographic key theft via remote EM sniffing
- **Tools**: Software Defined Radio (SDR), H-field probe, ChipWhisperer, RTL-SDR
- **Scenario**: Cryptographic hardware leaks electromagnetic radiation which attackers capture using antennas to extract processed secrets like keys.
- **Attack Steps**: Step 1: Acquire an EM probe or SDR (like HackRF or ChipWhisperer EM board). Step 2: Place the probe close to the target device’s chip (e.g., smartcard, hardware wallet, router SoC). Step 3: Trigger repeated crypto operations (e.g., logging in, encrypting data) while capturing EM emissions. Step 4: Use software tools to analyze recorded EM signal traces. Step 5: Like CPA, correlate known inputs with EM waveforms using Hamming Weight or similar models. Step 6: Isolate signal peaks associated with key-dependent operations. Step 7: Narrow down possible key bytes through correlation. Step 8: If emissions are strong and noise is low, full AES or RSA keys can be recovered in hours. Step 9: Some setups use custom coils or loops for better reception; shielding may reduce effectiveness.
- **Detection**: Monitor for EM probes or wireless spectrum anomalies; physical inspection of devices
- **Solution**: EM shielding, tamper-resistant packaging, signal obfuscation
- **Tags**: Electromagnetic Leakage, Crypto Chips, Remote Side-Channel

## Laptop Screen Emission Leak (Van Eck Phreaking)

- **Attack Type**: EM Leakage from Displays
- **Target**: Laptops, CRT/LCD Monitors
- **Vulnerability**: EM radiation from unshielded hardware
- **MITRE**: T1208 – Hardware Abuse
- **Impact**: Screen information theft, surveillance
- **Tools**: RTL-SDR, EM Probe, Oscilloscope, GNURadio
- **Scenario**: Capture screen content by detecting unintended electromagnetic radiation emitted by a laptop or monitor during display rendering.
- **Attack Steps**: Step 1: Set up an RTL-SDR (software-defined radio) or dedicated EM antenna within ~1–10 meters of the target laptop. Step 2: Use software like GNURadio to tune into the 30 MHz – 1 GHz spectrum where VGA/LCD screens leak EM signals. Step 3: Calibrate to match the display refresh rate and pixel frequency of the target (e.g., 60 Hz refresh × resolution). Step 4: Capture raw EM waveforms and demodulate the signals into visible content. Tools can sometimes reconstruct faint outlines or full screen images. Step 5: Analyze the recovered display content for sensitive information like email addresses, documents, or password fields. Step 6: Repeat and refine tuning if signal is weak. Step 7: Shielding, grounding, and using newer displays may reduce leakage, but unprotected systems remain at risk.
- **Detection**: EM field anomaly detection; monitoring unusual radio spectrum emissions
- **Solution**: Use TEMPEST-grade shielding; apply EM filters; avoid exposing sensitive data on screens near unknown observers
- **Tags**: Van Eck, Screen EM Leak, Laptop Display EM, Side-Channel

## Cache Timing Attacks (Flush+Reload)

- **Attack Type**: CPU Cache Side-Channel
- **Target**: Shared Libraries, OpenSSL
- **Vulnerability**: Shared CPU cache with predictable access
- **MITRE**: T1203 – Exploitation of Client Execution
- **Impact**: Key recovery, process information leakage
- **Tools**: Flush+Reload script, perf, rdtsc, C, Python
- **Scenario**: Attacker measures cache access time to determine which data/code was loaded by victim, leaking key-dependent patterns.
- **Attack Steps**: Step 1: On a shared system (like a multi-user machine or VM), the attacker and victim both access a shared library or data (e.g., OpenSSL). Step 2: The attacker flushes a specific cache line using CPU instructions like clflush. Step 3: Waits for the victim to run their cryptographic function (e.g., AES). Step 4: After execution, attacker reloads the flushed memory location and times how long it takes. Step 5: A fast reload means the victim accessed the memory (it was cached); a slow one means it wasn't. Step 6: Repeat this over multiple operations to infer which lookup tables (like AES S-boxes) the victim used. Step 7: Reconstruct the cryptographic key by analyzing which S-box entries were used. Step 8: Can recover full AES keys in seconds on unprotected systems. Step 9: Requires no admin access, but depends on shared memory or flush capability.
- **Detection**: Monitor cache flushing patterns; detect high-frequency timing checks
- **Solution**: Use constant-time algorithms; disable shared memory; use hardware AES instructions
- **Tags**: Flush+Reload, Cache Attack, OpenSSL AES

## Prime+Probe in Cloud VMs

- **Attack Type**: Cache Side-Channel in Multi-Tenant Clouds
- **Target**: Cloud VMs, Hypervisors
- **Vulnerability**: Shared CPU resources in cloud hardware
- **MITRE**: T1210 – Exploit Shared Compute Resources
- **Impact**: Cloud tenant data leakage, key extraction
- **Tools**: Prime+Probe toolkit, C code, perf, x86 CPU
- **Scenario**: Attacker deduces victim cache use without shared memory, purely by measuring eviction behavior in the last-level cache (LLC).
- **Attack Steps**: Step 1: Attacker rents a virtual machine on a cloud platform that runs on the same physical CPU as the victim. Step 2: Identifies sets of memory addresses that map to the same CPU cache sets as the victim (called "eviction sets"). Step 3: Fills these sets with attacker’s data (prime phase). Step 4: Waits briefly to let the victim process run. Step 5: Measures how long it takes to reload attacker’s data (probe phase). Step 6: Longer reload time means the victim accessed the same cache set, evicting attacker’s data. Step 7: Repeats this across many cache sets and time windows to build a map of victim’s behavior. Step 8: By analyzing which functions or data the victim accessed, attacker can infer key usage or sensitive operations. Step 9: This attack works even without shared memory, making it dangerous in cloud settings.
- **Detection**: Monitor cache usage patterns, anomalous performance counters
- **Solution**: CPU isolation, cache partitioning, tenant-to-core binding, use of constant-time crypto
- **Tags**: Prime+Probe, Cloud Attack, Cache Timing, Cloud Cryptanalysis

## Smartphone EM Side-Channels

- **Attack Type**: EM Leakage from Mobile Devices
- **Target**: Smartphones, Mobile CPUs
- **Vulnerability**: EM leakage due to lack of shielding
- **MITRE**: T1208 – Hardware Abuse
- **Impact**: PIN inference, input recovery, passive spying
- **Tools**: EM probe, RTL-SDR, GNURadio, SDRTouch
- **Scenario**: Capture electromagnetic emissions from smartphone CPUs or touchscreen sensors to infer user input or cryptographic operations.
- **Attack Steps**: Step 1: Set up a sensitive EM receiver (e.g., RTL-SDR dongle or EM probe) close to the target smartphone (usually within 5–30 cm). Step 2: Tune the receiver to EM frequency bands where the device emits radiation during operation (100 MHz–1 GHz range typically). Step 3: Record EM emissions while the target performs sensitive tasks like typing a PIN, logging into apps, or decrypting files. Step 4: Use GNURadio or SDRTouch to visualize and analyze the EM signal patterns. Step 5: Detect spikes or consistent patterns correlated with CPU operations or touchscreen events. Step 6: Train a model (e.g., using machine learning) to associate EM signatures with specific actions (like typing digits). Step 7: Infer the content of PINs, key presses, or even encryption behavior from emissions. Step 8: Shielding or distance is required to mitigate these EM leaks.
- **Detection**: Monitor for unauthorized EM receivers nearby; physical shielding of devices
- **Solution**: Shield devices; randomize or mask EM emissions; detect nearby RF activity
- **Tags**: EM Side-Channel, Mobile, SDR

## Flush+Reload on AES

- **Attack Type**: Cache Side-Channel on AES Implementation
- **Target**: OpenSSL, TLS, Shared Crypto Libs
- **Vulnerability**: Shared cache access on CPU
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Full AES key recovery
- **Tools**: clflush, perf, C, Python, OpenSSL (vulnerable), Flush+Reload tools
- **Scenario**: Attackers determine which S-box table entries are accessed during AES operations by measuring cache access timing.
- **Attack Steps**: Step 1: Ensure attacker and victim processes share a physical CPU and access the same shared AES implementation (e.g., in OpenSSL). Step 2: Use clflush instruction to evict AES S-box table entries from the cache. Step 3: Wait for the victim to perform AES encryption (e.g., HTTPS traffic). Step 4: Measure how long it takes to reload each S-box entry from memory. Step 5: Fast access = the victim used that entry (still cached), slow = not used. Step 6: Correlate which S-box entries were accessed during each round of AES. Step 7: Over many encryptions, deduce key bytes based on statistical patterns of access. Step 8: Reconstruct AES key completely. Step 9: Works against AES-T-table-based implementations and shared libraries. Replace with constant-time versions to avoid this.
- **Detection**: Monitor high-frequency flush patterns; detect statistical anomalies in cache usage
- **Solution**: Use constant-time AES implementations (e.g., AES-NI); disable shared libraries
- **Tags**: AES, Flush+Reload, Cache Timing

## Spectre/Meltdown

- **Attack Type**: Speculative Execution Side-Channel Attacks
- **Target**: CPUs (Intel, AMD, ARM), Browsers
- **Vulnerability**: Speculative execution + cache leakage
- **MITRE**: T1203 – Speculative Execution Exploit
- **Impact**: Data leak, key theft, browser/tab isolation bypass
- **Tools**: Spectre/Meltdown PoC, C code, Browser JS, perf, Linux tools
- **Scenario**: Exploits flaws in CPU speculative execution and caching behavior to read arbitrary memory of another process or kernel.
- **Attack Steps**: Step 1: Attacker crafts code that runs on the same CPU (browser JS, local code, or VM). Step 2: Code performs a bounds check that is skipped due to speculative execution, allowing access to unauthorized memory. Step 3: Accessed data is stored in CPU cache before the CPU realizes the access is invalid. Step 4: Use timing (Flush+Reload or Prime+Probe) to measure which memory/cached value was speculatively accessed. Step 5: Repeat for different addresses to leak data from kernel, process memory, or even browser tabs. Step 6: Can read cryptographic keys, credentials, or secret data. Step 7: Patches now exist (microcode + OS), but old systems or unpatched firmware remain vulnerable. Step 8: This works remotely if JavaScript is not sandboxed properly. Step 9: Hardware-level mitigation is best defense.
- **Detection**: Detect high-resolution timers; detect cache probing behavior in browser/VMs
- **Solution**: Apply CPU firmware patches (Spectre/Meltdown), enable browser sandboxing, disable high-resolution timers
- **Tags**: Spectre, Meltdown, CPU Side-Channel, Memory Leak

## Rowhammer (Bit Flipping)

- **Attack Type**: Physical RAM Fault Injection via Repetition
- **Target**: DRAM (non-ECC), Userland Memory
- **Vulnerability**: Bit flip due to DRAM row interference
- **MITRE**: T1557 – Memory Corruption via Rowhammer
- **Impact**: Arbitrary memory modification, privilege escalation
- **Tools**: Rowhammer.js, RHbitflip, Memtest86, C code, Linux perf
- **Scenario**: Aggressive DRAM row access causes bit flips in adjacent memory rows, which can be exploited to corrupt data or escalate privileges.
- **Attack Steps**: Step 1: Attacker locates a memory region they can access (e.g., via a web page with JavaScript or local program). Step 2: Repeatedly access (“hammer”) the same DRAM row at high speed to induce voltage disturbance in nearby rows. Step 3: Over time, electrical interference causes single-bit flips in adjacent memory (bit flipping). Step 4: These flips can corrupt page tables, credentials, or cryptographic keys. Step 5: In practical attacks, this leads to privilege escalation (e.g., flipping a kernel bit from 0 to 1). Step 6: Requires high DRAM refresh interval or lack of ECC. Step 7: Modern OSes and hardware vendors have added mitigations like ECC RAM, refresh hardening, or TRR (Target Row Refresh). Step 8: Attackers can still find memory regions vulnerable to hammering using reverse engineering or brute force. Step 9: Web-based Rowhammer attacks are possible using JavaScript + timing tricks.
- **Detection**: Detect repetitive row access; use ECC memory; monitor for abnormal memory activity
- **Solution**: ECC RAM, Row refresh rate tuning, software-based defenses like ANVIL
- **Tags**: Rowhammer, Memory Flipping, DRAM Attack

## Keyboard Acoustic Attacks

- **Attack Type**: Acoustic Side-Channel Attack
- **Target**: Physical Keyboards
- **Vulnerability**: Typing acoustics leak keystroke info
- **MITRE**: T1056.004 – Acoustic Keylogging
- **Impact**: Credential theft, PIN guessing
- **Tools**: Microphone, Audacity, ML (SVM, CNN), Python, DeepSound
- **Scenario**: By recording and analyzing keyboard sounds, attackers can infer keystrokes and typed content such as passwords, PINs, or messages.
- **Attack Steps**: Step 1: Place a microphone (e.g., phone mic, webcam mic) near the target keyboard without being noticed. Step 2: Start recording audio while the victim types (e.g., during login or password input). Step 3: Use a tool like Audacity to visualize and segment the waveform into individual keystrokes based on sound spikes. Step 4: Train a machine learning model (e.g., SVM or CNN in Python) using labeled audio of keystrokes for the specific keyboard model. Step 5: Apply this trained model to the captured audio to identify which keys were likely pressed. Step 6: Reconstruct the typed password or input. Step 7: Repeat or refine using multiple recordings or different angles/microphones. Step 8: Prevent this by using on-screen keyboards, white noise, or different input methods (e.g., biometric login).
- **Detection**: Unusual audio input; background recording detection
- **Solution**: Use virtual keyboards, background noise generators, or rubber dome silent keyboards
- **Tags**: Acoustic, Side-Channel, Keylogging

## RSA Key from CPU Fan Noise

- **Attack Type**: Fan-Based Side-Channel Attack
- **Target**: Desktop/Laptop Computers
- **Vulnerability**: Variable CPU load leaks via fan behavior
- **MITRE**: T1496 – Resource Hijacking
- **Impact**: Private key extraction from non-contact observation
- **Tools**: Microphone, Fan monitor (lm-sensors), Python, FFT tools
- **Scenario**: Cryptographic operations generate CPU heat. Fan speed changes (RPM) produce varying sound patterns, which can correlate to private key operations.
- **Attack Steps**: Step 1: Position a microphone near the target system's fan (can be across the room in quiet environments). Step 2: Record fan noise while the system performs RSA decryption or signing. Step 3: Convert audio into frequency spectrum (FFT – Fast Fourier Transform) using Python or MATLAB. Step 4: Measure the frequency shifts and timing of fan RPM changes during cryptographic operations. Step 5: Identify patterns in fan noise that correspond to high or low CPU load, which depends on key size or operation. Step 6: Over repeated observations, deduce parts of the private RSA key used during those operations. Step 7: Apply timing analysis + fan behavior modeling to extract bits of the private key. Step 8: Mitigate using constant-load operations, noise padding, or fixed CPU frequency.
- **Detection**: Monitor for sound-recording devices; analyze fan control logs
- **Solution**: Fix CPU frequency; use constant-time cryptographic operations; acoustic shielding
- **Tags**: Side-Channel, RSA, Fan Acoustics, Physical Leakage

## Thermal Imaging Leak

- **Attack Type**: Heat Signature PIN Extraction
- **Target**: ATM Keypads, Smart Locks
- **Vulnerability**: Thermal residue from recent touch
- **MITRE**: T1056.001 – Input Capture
- **Impact**: PIN/code inference, physical access bypass
- **Tools**: Thermal Camera (FLIR One, Seek Thermal), Image analysis
- **Scenario**: Attackers use infrared cameras to visualize heat left on keypads or touchscreens and infer the last pressed buttons (e.g., ATM PINs or phone unlock patterns).
- **Attack Steps**: Step 1: After a victim enters a PIN on a physical keypad (e.g., ATM or digital lock), attacker approaches the device within 20–30 seconds with a handheld thermal camera. Step 2: Capture a thermal image of the keypad, showing heat residues from the victim’s fingers. Step 3: Use software (provided with camera or Python + OpenCV) to enhance image contrast. Step 4: Identify the pressed keys based on residual heat intensity. Step 5: Guess PIN order based on temperature (recent touches = warmer). Step 6: Apply most probable PINs to target device or relay to attacker. Step 7: Defense: touch random keys after entry to mask real ones; use gloves or styluses. Step 8: On-screen PINs and biometric inputs reduce risk.
- **Detection**: Monitor for nearby thermal cameras; input dummy PINs post-login
- **Solution**: Use touch scrambling, randomized input pads, or non-contact authentication methods
- **Tags**: Thermal Attack, Side-Channel, PIN Inference

## Optical Power LED Leak

- **Attack Type**: LED Flicker-Based Optical Side-Channel
- **Target**: Routers, Smart Cards, Servers
- **Vulnerability**: Blinking LED leaks operational patterns
- **MITRE**: T1110 – Brute Force via Signal Observation
- **Impact**: Side-channel data exposure, operational info leakage
- **Tools**: High-speed camera, Photodiode, Arduino, Oscilloscope
- **Scenario**: Some LEDs (e.g., on routers, servers, network cards) blink at rates proportional to data transfer or operations like encryption/decryption, leaking sensitive patterns.
- **Attack Steps**: Step 1: Set up a camera or photodiode aimed at the power/activity LED on a cryptographic device (e.g., router or smart card reader). Step 2: Record LED flickering patterns during secure operations (e.g., SSH login, VPN handshake, decryption). Step 3: Use high-frame-rate video (1000+ FPS) or connect a photodiode to an oscilloscope to capture LED blinking waveforms. Step 4: Analyze blinking frequencies or timing sequences to correlate with binary operations or crypto activity. Step 5: Extract patterns that reveal bits of data (e.g., key length, timing, buffer size). Step 6: In highly vulnerable implementations, even partial key info or traffic patterns can be leaked. Step 7: Mitigate with constant blinking or removing unnecessary indicators.
- **Detection**: Record blinking patterns or unusual optical emissions
- **Solution**: Shield LEDs, use internal-only indicators, randomize blinking not tied to operation state
- **Tags**: Optical Side-Channel, LED, Flicker-Based Leak

## Voltage Glitching

- **Attack Type**: Power Fault Injection
- **Target**: Smartcards, Secure Chips
- **Vulnerability**: Hardware fails under voltage faults
- **MITRE**: T1600 – Modify System Image
- **Impact**: Bypass authentication, extract keys, disable encryption
- **Tools**: ChipWhisperer, Arduino, Raspberry Pi, Oscilloscope, Power Profiler
- **Scenario**: Attackers momentarily drop voltage supplied to a processor to cause execution faults and skip important crypto security checks like password validation or fuse checks.
- **Attack Steps**: Step 1: Identify a cryptographic hardware target (e.g., a smart card, router, secure microcontroller). Step 2: Connect a power glitching device such as ChipWhisperer or a custom Arduino-based voltage dropper between the power supply and target chip. Step 3: Begin target’s secure operation, such as password check, firmware boot, or signature verification. Step 4: Precisely drop the supply voltage for a few microseconds during the security check phase. Step 5: Observe whether the glitch causes the processor to skip critical operations (e.g., always-true condition, bypass auth). Step 6: Use trial and error (scripting + oscilloscope) to fine-tune timing until successful glitch is repeated reliably. Step 7: Exploit resulting access (e.g., dump firmware, retrieve keys). Step 8: Use power monitors or watchdogs in production to prevent this.
- **Detection**: Use brownout detection, glitch detectors in power supply circuit
- **Solution**: Use tamper-resistant chips, secure boot validation, voltage filtering modules
- **Tags**: Voltage Glitch, Fault Injection, Hardware Crypto

## Clock Glitching

- **Attack Type**: Timing-Based Fault Injection
- **Target**: Microcontrollers, Smartcards
- **Vulnerability**: Unsynchronized logic due to clock faults
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Disable security functions, skip key validation logic
- **Tools**: Clock generator (Glitcher), ChipWhisperer, Oscilloscope
- **Scenario**: By changing the clock input frequency (speeding up or slowing down), attackers can induce logic faults in crypto routines on embedded chips or MCUs.
- **Attack Steps**: Step 1: Choose a target embedded chip (e.g., IoT, payment terminal) that uses a stable clock for operation. Step 2: Connect an external clock source or glitcher to the clock input of the chip. Step 3: Trigger secure crypto operation like boot decryption, PIN verification, or code signature. Step 4: At precise time, inject a faster or slower clock pulse to cause incorrect logical decisions. Step 5: Monitor if the chip skips a key check or reveals sensitive output (like a failed MAC being accepted). Step 6: Repeat with microsecond-level tuning until successful behavior occurs. Step 7: This can bypass secure boot or inject malicious code. Step 8: Protect by using internal clock with redundancy or watchdogs.
- **Detection**: Clock anomaly detection, unexpected frequency monitoring
- **Solution**: Use secure on-chip clock, glitch detectors, or redundant timing verification
- **Tags**: Clock Glitch, Secure Boot Bypass, Timing Fault

## Laser Fault Injection

- **Attack Type**: Physical Fault Injection via Laser
- **Target**: Crypto ICs, Secure Microchips
- **Vulnerability**: Bit-flip or logic jump due to laser pulse
- **MITRE**: T1140 – Deobfuscate/Decode Files or Information
- **Impact**: Key extraction, privilege escalation, data exfiltration
- **Tools**: IR Laser, High-Precision Stage, Oscilloscope, Fume Hood
- **Scenario**: Lasers focused on chip surface can cause localized memory or logic faults during cryptographic processing, allowing bypass of access controls or revealing key bits.
- **Attack Steps**: Step 1: Open the chip package using chemical etching or mechanical decapsulation to expose the silicon die. Step 2: Mount the chip under a high-precision stage with a near-infrared (IR) laser setup. Step 3: Use a camera or microscope to visually map and focus on a specific logic region (e.g., ALU, memory cell). Step 4: Start crypto operation (e.g., RSA decrypt, key comparison) and time the laser pulse to hit the target during sensitive computation. Step 5: Observe resulting behavior—skipped branches, key leaks, crashes, or partial output leakage. Step 6: Refine laser timing, location, and power intensity through repeated trials. Step 7: Successful injection may allow attacker to dump secrets, bypass login, or modify control flow. Step 8: Mitigate using photodetectors, tamper mesh, or epoxy sealants.
- **Detection**: Tamper sensors, die monitoring, failure analysis logs
- **Solution**: Epoxy packaging, active shield mesh, laser detection and shutdown circuitry
- **Tags**: Laser Injection, Hardware Fault, Key Extraction

## EM Fault Injection (EMFI)

- **Attack Type**: Electromagnetic-Based Fault Injection
- **Target**: Smartcards, Crypto ICs
- **Vulnerability**: Sensitive logic disrupted via EM pulses
- **MITRE**: T1600 – Modify System Image
- **Impact**: Logic faults, authentication bypass, firmware manipulation
- **Tools**: EMFI Coil, Pulse Generator, Oscilloscope, Shielding Material
- **Scenario**: Attackers use EM pulses targeted at chips to induce temporary logic faults, bypassing crypto checks, changing memory bits, or altering flow of execution.
- **Attack Steps**: Step 1: Identify a cryptographic hardware target such as a payment chip, IoT device, or TPM module. Step 2: Construct or purchase a small EM coil and connect it to a high-voltage pulse generator. Step 3: Position the coil within a few millimeters of the chip's packaging—ideally over sensitive logic areas (e.g., decryption engine, RAM controller). Step 4: Start cryptographic operation (e.g., secure boot, PIN check) and send a precisely timed electromagnetic pulse to the chip. Step 5: Observe output for incorrect behavior: skipped comparisons, altered outputs, memory corruption. Step 6: Use trial-and-error or side-channel feedback to refine timing and pulse strength. Step 7: Successful fault can allow full control, key leakage, or backdoor injection. Step 8: Mitigate via EM shielding, redundant logic, error detection codes.
- **Detection**: EM field monitoring, firmware checksums, EM shielding
- **Solution**: Metal shielding, internal error correction, hardened IC design
- **Tags**: EMFI, Fault Injection, Hardware Exploitation

## Remote Timing over Network

- **Attack Type**: Remote Timing Side-Channel
- **Target**: Web APIs, Login Pages
- **Vulnerability**: Time difference leaks via sequential comparisons
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Token or password disclosure through timing analysis
- **Tools**: curl, Python, Wireshark, Scapy
- **Scenario**: Infer secret keys or credentials based on how long a web server or API takes to respond to different inputs.
- **Attack Steps**: Step 1: Identify a web service (login API, JWT validator, password reset) that performs crypto operations (e.g., HMAC, token comparison). Step 2: Write a script (e.g., Python + requests) that sends requests with varying input values and records the time taken for each response (using time.time() or response headers). Step 3: Repeatedly send inputs with partial correct guesses (e.g., one character at a time) and measure if the response time increases. Step 4: Look for consistent differences in time that increase with correct character positions (this implies linear time comparison like if guess == secret). Step 5: Continue guessing the next character by testing all possible values and selecting the one with the highest timing delay. Step 6: Repeat until full secret is recovered. Step 7: Mitigate by using constant-time comparison functions and uniform error messages.
- **Detection**: Measure request latency patterns, alert on repeated request patterns
- **Solution**: Use constant-time crypto functions (e.g., hmac.compare_digest), rate limit guessing attempts
- **Tags**: Timing Attack, Remote API Leak, HMAC Abuse

## JavaScript Rowhammer

- **Attack Type**: Memory Bit Flipping via JS
- **Target**: Web Browsers, JS Engines
- **Vulnerability**: DRAM row disturbance via JS access patterns
- **MITRE**: T1110 – Brute Force
- **Impact**: Bit flips enabling data theft or sandbox escape
- **Tools**: Rowhammer.js, Chrome DevTools, Firefox Nightly
- **Scenario**: Use JavaScript to repeatedly access memory in browsers to flip DRAM bits, bypassing same-origin policy or extracting data from other tabs/VMs.
- **Attack Steps**: Step 1: Use a browser (preferably older Firefox or Chrome) with vulnerable memory management. Step 2: Host and open a crafted malicious webpage that includes rowhammer.js or similar script. Step 3: The script allocates large chunks of memory in the browser using ArrayBuffer, SharedArrayBuffer, or TypedArrays. Step 4: It repeatedly accesses ("hammers") specific memory rows using setInterval or while loops to induce disturbance in adjacent memory rows. Step 5: Over time, a bit in an adjacent row may flip, allowing attacker to escalate privileges or extract cross-origin secrets. Step 6: Monitor memory or use speculative access to test if bit flips occurred. Step 7: Mitigate by disabling JS memory primitives or using ECC memory.
- **Detection**: Monitor high-memory access loops; disable JS features
- **Solution**: Use ECC memory; patch browsers; disable SharedArrayBuffer in untrusted contexts
- **Tags**: Rowhammer, JS Exploit, Browser Memory Abuse

## Cache Attacks via Shared Libraries

- **Attack Type**: Flush+Reload via Shared Libraries
- **Target**: Shared-host VMs, Libraries
- **Vulnerability**: Shared cache access leaks victim’s access path
- **MITRE**: T1071 – Application Layer Protocol
- **Impact**: Key recovery across VM or user boundaries
- **Tools**: Flush+Reload script, OpenSSL, Linux Perf Tools
- **Scenario**: Exploit shared memory (e.g., OpenSSL library) to track victim memory access using CPU cache patterns, leaking key bytes.
- **Attack Steps**: Step 1: On a shared system (cloud VM, or multi-user server), locate common cryptographic library used by both attacker and victim (e.g., OpenSSL). Step 2: Attacker uses Flush+Reload attack: flushes a target memory line (e.g., AES S-box) from CPU cache using clflush. Step 3: Waits briefly, then reloads it and times the access. Step 4: If victim used that crypto routine, access is fast (still in cache); if not, it's slow. Step 5: Repeat across many memory locations and over time to recover access patterns, which can reveal secret key bits. Step 6: Automate across thousands of operations to recover full keys. Step 7: Mitigate via cache partitioning, disabling shared memory, or constant-time routines.
- **Detection**: Monitor memory flush patterns; isolate crypto processes
- **Solution**: Use constant-time crypto, CPU cache partitioning (CAT), disable memory deduplication
- **Tags**: Flush+Reload, Cache Side-Channel, Shared Lib Exploit

## Side-Channel in AI/ML Inference

- **Attack Type**: Model Inference via Power/Timing
- **Target**: AI Inference APIs, ML Models
- **Vulnerability**: Timing/power leak reveals model structure/data
- **MITRE**: T1602 – Data from Information Repositories
- **Impact**: Model theft, privacy violation, training set leakage
- **Tools**: ML Model (TensorFlow, PyTorch), Timing script, Power monitor
- **Scenario**: Attackers infer private data or model weights from timing, cache, or memory access patterns during AI model inference or crypto operations.
- **Attack Steps**: Step 1: Identify an AI/ML model that is exposed via API (e.g., model-as-a-service, ML inference endpoint). Step 2: Create input queries that differ slightly in structure or semantics (e.g., similar feature vectors or images). Step 3: Measure response times or memory/cache traces (on local or cloud VM) while model makes inference. Step 4: Observe differences in processing time or power draw which may correlate to specific internal model decisions (e.g., layer activations, decision paths). Step 5: Use collected data to train your own local model or reverse-engineer parts of the original model (e.g., presence of a feature or user trait). Step 6: Can also leak membership of training set, used in privacy attacks. Step 7: Use differential privacy, access noise, and uniform processing time for defense.
- **Detection**: Monitor ML API access frequency; alert on statistical probing
- **Solution**: Apply differential privacy, response padding, add noise to prediction latency
- **Tags**: ML Side-Channel, Model Stealing, Inference Leak

## Radio Leakage from Smart Cards

- **Attack Type**: EM Leakage via Physical Emissions
- **Target**: Smart Cards, Embedded Devices
- **Vulnerability**: Electromagnetic radiation side-channel
- **MITRE**: T1208 – Hardware Side-Channel Attacks
- **Impact**: Extraction of cryptographic keys or PINs from devices
- **Tools**: RTL-SDR, USRP, oscilloscope, EM probe
- **Scenario**: Electromagnetic signals emitted by smart cards during cryptographic operations (like RSA, AES) can be intercepted to recover private keys or data.
- **Attack Steps**: Step 1: Obtain a smart card that performs crypto operations (e.g., payment, authentication, SIM). Step 2: Set up electromagnetic (EM) measurement hardware: place a sensitive EM probe near the card chip while it's performing cryptographic computation. Step 3: Trigger known operations (e.g., card authentication with same plaintext multiple times). Step 4: Use a software-defined radio (like RTL-SDR or USRP) to capture side-channel emissions. Step 5: Analyze collected waveforms for consistent signal patterns that correlate with key-dependent operations (e.g., bit flips, multiplications). Step 6: Perform statistical or differential EM analysis to isolate parts of the key. Step 7: Iterate the process with different plaintexts or clock speeds. Step 8: Use derived EM signal leakage to reconstruct the full secret key. Step 9: Defend using EM shielding, randomized execution, and power masking.
- **Detection**: Monitor for unusual EM emissions (in lab environments); smart card EM audit
- **Solution**: Use metal shielding, power balancing, randomized operations, and secure chip design
- **Tags**: EM Side Channel, Smart Card, RTL-SDR

## RSA Timing Attack

- **Attack Type**: ModExp Timing Analysis
- **Target**: RSA Implementations
- **Vulnerability**: Time-based side channel in modular exponentiation
- **MITRE**: T1040 – Network Sniffing
- **Impact**: RSA private key leakage via timing
- **Tools**: Python, OpenSSL, custom timing scripts
- **Scenario**: Infer RSA private key bits by measuring how long modular exponentiation takes, especially in software libraries without constant-time implementations.
- **Attack Steps**: Step 1: Identify a server, application, or smart card that performs RSA decryption or signing (e.g., TLS handshake, digital signature verification). Step 2: Send crafted ciphertexts that trigger RSA decryption and measure the time taken to respond. Step 3: Vary ciphertexts to target specific operations (e.g., different bits of exponent). Step 4: Collect hundreds or thousands of timing samples. Step 5: Use statistical analysis (e.g., correlation or machine learning) to infer which bits of the private key cause timing variance. Step 6: Reconstruct the RSA key bit-by-bit using observed delays in modular exponentiation steps. Step 7: Refine attack using noise filtering and delay compensation. Step 8: Mitigate by using constant-time exponentiation algorithms (e.g., Montgomery Ladder).
- **Detection**: Time measurements with high granularity and repetition
- **Solution**: Use constant-time modular arithmetic libraries (e.g., OpenSSL with timing mitigation)
- **Tags**: RSA, Timing Attack, ModExp, Side-Channel

## CRT-RSA Fault Timing

- **Attack Type**: CRT Optimization Fault Injection
- **Target**: Smart Cards, Crypto Chips
- **Vulnerability**: Faulty math under CRT allows key recovery
- **MITRE**: T1208 – Hardware Side-Channel Attacks
- **Impact**: Full RSA key recovery with one faulty decryption
- **Tools**: Fault injector (laser, EMFI), Python
- **Scenario**: Exploit RSA decryption errors from Chinese Remainder Theorem (CRT) optimizations to fully recover private RSA keys using only one faulty decryption.
- **Attack Steps**: Step 1: Target an RSA implementation using CRT (often used to speed up decryption). Step 2: Inject a fault (e.g., via EM pulse, clock glitch, or voltage glitch) during the CRT-based RSA decryption process. Step 3: Capture both the faulty signature S_faulty and the correct ciphertext C. Step 4: Compute: S_correct = decrypt(C) using the public key and verify that the fault causes a mismatch. Step 5: Use the Bellcore attack or Lenstra’s method to factor n (RSA modulus) using the difference between faulty and correct signatures. Step 6: Once p and q are recovered, derive the full private key. Step 7: Use key to decrypt any past or future communications. Step 8: Mitigate by using RSA blinding, error detection in CRT steps, and fault-resistant hardware.
- **Detection**: Signature mismatch logging, fault detection in decryption processes
- **Solution**: Use error detection in CRT decryption; enable RSA blinding and tamper-resistant chip design
- **Tags**: CRT Fault, RSA Key Leak, Bellcore

## AES T-table Lookup

- **Attack Type**: AES Cache Timing
- **Target**: AES Libraries, CPUs
- **Vulnerability**: Cache access timing leaks table lookup indices
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: AES key recovery via timing/cache analysis
- **Tools**: Flush+Reload, Prime+Probe, Cachegrind
- **Scenario**: Attacker times access to S-box (lookup table) locations in AES, correlating memory access to key-dependent values.
- **Attack Steps**: Step 1: Identify AES implementation using T-table lookups (common in older OpenSSL, embedded AES libraries). Step 2: Set up a cache timing attack (e.g., Flush+Reload or Prime+Probe) on a system where attacker and victim share cache or memory pages. Step 3: Flush specific cache lines corresponding to S-box entries (T-tables). Step 4: Wait for the victim to perform AES encryption with unknown key. Step 5: Measure which cache lines were reloaded, indicating which S-box values were accessed. Step 6: Over thousands of encryptions, build up correlation between accessed cache lines and specific key bytes. Step 7: Reconstruct AES key byte-by-byte. Step 8: Use constant-time AES implementation (e.g., using AES-NI or table-free software) to prevent leakage.
- **Detection**: Monitor shared memory usage, frequent cache flush patterns
- **Solution**: Use AES-NI hardware instructions; avoid table-based AES implementation
- **Tags**: AES, Cache Side-Channel, Flush+Reload, T-Table Timing

## DSA Timing Leak

- **Attack Type**: Timing Side-Channel on Nonce k
- **Target**: APIs, signing endpoints
- **Vulnerability**: Time leakage in signature nonce k
- **MITRE**: T1208 – Hardware Side-Channel Attacks
- **Impact**: Full DSA key recovery from timing data
- **Tools**: Python, SageMath, side-channel profilers
- **Scenario**: DSA signature generation uses a random number (k). If the implementation leaks timing differences due to operations involving k, attackers can recover the private key.
- **Attack Steps**: Step 1: Target an application or server that uses Digital Signature Algorithm (DSA) for signing messages (e.g., older APIs, firmware updates). Step 2: Send multiple signing requests (if public interface allows) or observe multiple DSA signatures from the same signer. Step 3: Measure the time taken to compute the signatures using high-resolution timers (e.g., nanosecond timers or side-channel profilers). Step 4: Analyze how timing varies with message contents and signature outputs. Step 5: Use timing data to infer the bits of the random number k. Step 6: Apply the Bleichenbacher attack or lattice-based methods to derive the full private key if partial bits of k are recovered. Step 7: Mitigate by ensuring constant-time k generation and using deterministic k (RFC 6979).
- **Detection**: Anomalies in signature timing; repeatable response latencies
- **Solution**: Use RFC 6979 (deterministic k); enforce constant-time crypto routines
- **Tags**: DSA, Timing Leak, Bleichenbacher Attack, RFC 6979

## ECDSA Scalar Leak

- **Attack Type**: Timing on Elliptic Curve Computation
- **Target**: Crypto Wallets, APIs
- **Vulnerability**: Scalar leaks via EC point multiplication timing
- **MITRE**: T1208 – Hardware Side-Channel Attacks
- **Impact**: ECDSA private key recovery via timing side-channels
- **Tools**: SageMath, Riscure Inspector, custom profilers
- **Scenario**: During ECDSA signature, operations on elliptic curve points leak info about the scalar multiplier (private key), especially in non-constant-time implementations.
- **Attack Steps**: Step 1: Identify a service or device using ECDSA for digital signatures (e.g., crypto wallets, firmware updates, TLS certs). Step 2: Trigger ECDSA operations repeatedly with controlled or known messages. Step 3: Use timing instrumentation to measure how long scalar multiplication takes during signing. Step 4: Correlate timing variations with the bits of the scalar (private key) involved in elliptic curve point operations. Step 5: Perform statistical analysis or lattice attacks using partial timing-based key leaks to reconstruct the full ECDSA private key. Step 6: Use recovered key to forge signatures. Step 7: Defend using constant-time ECC libraries (e.g., libsodium, BoringSSL) and side-channel hardened elliptic curve point multiplication.
- **Detection**: Timing analysis of ECDSA signature generation
- **Solution**: Use constant-time ECC libraries; randomize or mask EC computations
- **Tags**: ECC, Scalar Timing, ECDSA Side Channel

## Password Verification Timing

- **Attack Type**: Web/API Login Timing Side Channel
- **Target**: Web Apps, APIs
- **Vulnerability**: Early-exit logic leaks correct character positions
- **MITRE**: T1110 – Brute Force
- **Impact**: Complete password recovery via login timing analysis
- **Tools**: curl, Burp Suite, custom timing script
- **Scenario**: If a login function checks passwords character-by-character and returns early on mismatch, timing measurements can reveal correct characters incrementally.
- **Attack Steps**: Step 1: Identify a login page or authentication API (e.g., /login, /auth/token). Step 2: Start sending login requests with fake usernames and passwords one character at a time. Step 3: Measure how long the server takes to respond for each attempt. Step 4: Look for consistent timing increases when correct characters are guessed (e.g., "a" vs "aa" vs "aaa"). Step 5: Use this info to guess the password one character at a time, testing every position. Step 6: Automate the attack using scripting (e.g., Python + time module) or Burp Suite Pro Intruder with millisecond precision. Step 7: Once the full password is discovered, log in as the target user. Step 8: Mitigate by comparing password hashes in constant-time (e.g., hmac.compare_digest in Python).
- **Detection**: Excessive login attempts; consistent timing variations
- **Solution**: Use constant-time password comparison; introduce artificial timing jitter
- **Tags**: Password Guessing, Timing Attack, API Authentication

## JWT Secret Guess Timing

- **Attack Type**: Token Validation Timing Side Channel
- **Target**: Web APIs, JWT-secured systems
- **Vulnerability**: Weak secrets + timing differences in HMAC validation
- **MITRE**: T1606 – Forge Web Tokens
- **Impact**: Full impersonation by forging valid JWTs
- **Tools**: jwt_tool.py, curl, Python
- **Scenario**: JWT tokens signed with weak secrets (e.g., HS256) may be guessed using timing attacks based on how long the server takes to validate the signature.
- **Attack Steps**: Step 1: Identify an API or endpoint that uses JWT tokens for authentication or session (e.g., Authorization: Bearer <token>). Step 2: Analyze the JWT format (Header.Payload.Signature) and algorithm used (e.g., HS256). Step 3: Start guessing weak secrets (e.g., "admin", "123456") and sign JWTs using those. Step 4: Send signed tokens to the target endpoint and measure the time it takes to respond. Step 5: Detect slight timing differences when the token is partially or fully valid (due to signature check implementation). Step 6: Iterate guesses, tuning payload and measuring delay after each submission. Step 7: Once valid secret is found, generate arbitrary tokens with any user role or permission. Step 8: Mitigate by using constant-time HMAC verification and strong JWT secrets (256-bit or longer).
- **Detection**: Analyze logs for repeated JWT attempts; measure response timing variance
- **Solution**: Use strong JWT secrets; implement constant-time verification; switch to asymmetric JWTs
- **Tags**: JWT, HMAC, Token Guess, Timing Side Channel

## API Key Timing Leak

- **Attack Type**: Timing Side-Channel in Key Validation
- **Target**: Web APIs, Cloud Services
- **Vulnerability**: Early-exit logic in key validation
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: Full API access without authorization
- **Tools**: curl, Burp Suite, Python, Wireshark
- **Scenario**: Some APIs validate API keys character-by-character. If implemented insecurely, attackers can measure how long the server takes to reject, revealing correct prefixes.
- **Attack Steps**: Step 1: Find an API endpoint that requires an API key, typically via Authorization headers or query strings (e.g., GET /api?key=XYZ). Step 2: Send API requests with different key guesses (start with a single character, then two, etc.). Step 3: Measure the response time for each request precisely using tools like curl -w, Burp Suite’s timer, or a Python script with time.time(). Step 4: If the backend checks keys char-by-char, correct guesses result in slightly longer processing time. Step 5: Use timing differences to iteratively build the valid API key one character at a time. Step 6: Once you find the full key, use it to gain full API access or elevate privileges. Step 7: Mitigation includes validating keys in constant time and rate-limiting failed API key attempts.
- **Detection**: Detect rapid, repeated API key probes with increasing delays
- **Solution**: Enforce constant-time key comparison; rate-limit attempts; monitor for abnormal patterns
- **Tags**: API Key Guessing, Timing Attack, Authorization Bypass

## HMAC Timing Attack

- **Attack Type**: HMAC Signature Validation Timing Attack
- **Target**: JWT Systems, Signed APIs
- **Vulnerability**: Non-constant-time HMAC comparison
- **MITRE**: T1606 – Forge Web Tokens
- **Impact**: Message forgery, token forgery, access escalation
- **Tools**: Python, curl, jwt_tool.py, Scapy
- **Scenario**: When applications compare HMAC signatures byte-by-byte, time differences in rejection can help attackers guess correct signature parts.
- **Attack Steps**: Step 1: Identify an endpoint that uses HMAC (Hash-based Message Authentication Code) to verify the integrity of requests or tokens (e.g., JWTs or signed URLs). Step 2: Generate or modify HMAC-protected requests with different keys or messages. Step 3: Send the requests to the server and carefully measure the response times. Step 4: Use precise timing data to detect when some characters of the HMAC are correct (server takes slightly longer to reject). Step 5: Brute-force each byte of the signature based on the response timing and build the correct HMAC signature incrementally. Step 6: Use the recovered signature to forge valid requests or tokens. Step 7: To defend, use constant-time comparison functions such as hmac.compare_digest() in Python or equivalent in other languages.
- **Detection**: Analyze request-response time variance; monitor HMAC verification anomalies
- **Solution**: Use constant-time HMAC comparison methods; avoid exposing response time differences
- **Tags**: HMAC, Timing Leak, API Security, JWT

## 2FA OTP Timing Skew

- **Attack Type**: OTP/2FA Generation Analysis via Skew
- **Target**: Login Forms with 2FA
- **Vulnerability**: Loose time skew acceptance or leakable generation logic
- **MITRE**: T1111 – Multi-Factor Abuse
- **Impact**: Predicting valid OTPs, bypassing 2FA security
- **Tools**: Google Authenticator, oathtool, timing script
- **Scenario**: OTPs (One-Time Passwords) like TOTP or HOTP can be partially predicted or guessed if the attacker can analyze timing skew in OTP validation.
- **Attack Steps**: Step 1: Identify an application or website using Time-based One-Time Password (TOTP) for 2FA (e.g., Google Authenticator). Step 2: Attempt logging in multiple times with OTPs slightly before or after the expected time window. Step 3: Monitor whether the system accepts OTPs with a time skew (e.g., 30s early or late). Step 4: Measure acceptance timing and note the OTPs that succeed vs. fail. Step 5: Use this to infer how the backend generates or verifies OTPs (e.g., which timestamp windows it accepts, which hash method used). Step 6: Brute-force OTPs within the known window to guess future valid OTPs. Step 7: Defend by limiting accepted skew (±1 interval), using encrypted time sync, and enforcing lockout after multiple failures.
- **Detection**: Monitor OTP failures vs. time window; log repeated OTP guesses within same time interval
- **Solution**: Use minimal time window; enforce OTP rate-limits and OTP expiration strictly
- **Tags**: TOTP, 2FA Abuse, Skew Analysis

## Login Page Delay

- **Attack Type**: Timing Side-Channel in Login Verification
- **Target**: Web Login Forms, APIs
- **Vulnerability**: User existence leak through login timing
- **MITRE**: T1589 – Account Discovery
- **Impact**: Username enumeration, aiding credential stuffing
- **Tools**: Burp Suite, curl, Python
- **Scenario**: Applications that return login responses faster for invalid usernames vs. valid ones reveal whether a user exists, aiding enumeration and brute-force attacks.
- **Attack Steps**: Step 1: Access a login page or API (e.g., /login, /auth). Step 2: Send login attempts with fake usernames and passwords using curl or Burp Repeater. Step 3: Measure response times for each combination. Step 4: Identify if response for invalid usernames is faster than for valid ones (even with wrong passwords). Step 5: Use this to confirm whether a username exists in the system. Step 6: Once a valid username is found, proceed to brute-force the password using a wordlist. Step 7: Automate with Burp Intruder or a script. Step 8: Mitigate by returning generic errors and using constant-time username/password validation for all cases.
- **Detection**: Analyze time taken for invalid vs. valid usernames; review auth logic
- **Solution**: Return generic auth errors; use constant-time auth routines; monitor login attempt patterns
- **Tags**: Login Timing, Enumeration, Credential Stuffing

## Session Validation Timing

- **Attack Type**: Side-Channel via Session Validation Timing
- **Target**: Web Applications, APIs
- **Vulnerability**: Session management timing leak
- **MITRE**: T1208 – Side-Channel Attack
- **Impact**: Session enumeration, access escalation
- **Tools**: curl, Burp Suite, Python
- **Scenario**: If validating an invalid vs. valid session token takes noticeably different time, attackers can detect session existence or even privilege level.
- **Attack Steps**: Step 1: Identify an application that uses tokens or session IDs (e.g., via cookies or headers) for user authentication. Step 2: Send multiple requests to a protected resource with different random session tokens. Step 3: Precisely measure how long the server takes to respond to each. Step 4: Observe if valid (or expired) tokens take slightly longer to process than completely invalid ones. Step 5: If so, this timing difference indicates the session ID is real but expired, or belongs to an active user. Step 6: Use this technique to enumerate session validity or guess tokens via brute-force. Step 7: Use discovered valid tokens to access user accounts if session tokens are not protected (e.g., short or predictable). Step 8: Defend by using constant-time session validation and avoiding detailed error messages or differential timing.
- **Detection**: Monitor token validation timing patterns; track anomaly frequency
- **Solution**: Use constant-time session validation; expire tokens securely; log session probing attempts
- **Tags**: Session ID, Timing Leak, Privilege Escalation

## Binary Search Timing on DB

- **Attack Type**: Index Guessing via Response Time
- **Target**: Login APIs, Search Features
- **Vulnerability**: Timing leak from indexed DB lookup
- **MITRE**: T1592 – Gather Victim Identity
- **Impact**: Reveals internal DB structure, usernames
- **Tools**: Burp Suite, sqlmap, custom Python script
- **Scenario**: Databases using indexed lookups (e.g., for username) may show timing differences that hint at internal search behavior (like binary search).
- **Attack Steps**: Step 1: Interact with an application login or search feature backed by a database. Step 2: Observe response times as you try usernames or queries in ascending/descending order (e.g., a–z). Step 3: If the server uses binary search or similar algorithms, items closer to the middle of the index may take longer to reject due to more comparisons. Step 4: Measure time differences using tools like Burp Repeater or Python with time.time() or requests. Step 5: Use this timing to infer internal ordering, locate records faster, or map out possible users. Step 6: Chain with username enumeration or targeted attacks. Step 7: Defend by adding fixed delay on all login failures or randomizing rejection timing. Step 8: Log for high-volume timing attempts.
- **Detection**: Time-based anomaly detection on login or search features
- **Solution**: Use non-deterministic response timing or padding; monitor for search pattern probes
- **Tags**: Database Timing, Index Probing, User Discovery

## File Existence via Timing

- **Attack Type**: File Presence Side-Channel
- **Target**: Web Servers, Web Apps
- **Vulnerability**: Response timing exposes file presence
- **MITRE**: T1595 – Active Scanning
- **Impact**: Information leakage, internal structure mapping
- **Tools**: curl, Burp Suite, ffuf, Python
- **Scenario**: Timing difference between HTTP 403 (forbidden) and 404 (not found) errors can be exploited to detect if a file or directory exists but is restricted.
- **Attack Steps**: Step 1: Choose a web application or server that restricts access to certain files or admin areas (e.g., /admin, /secret.txt). Step 2: Use a tool like curl or Burp Suite to send HTTP GET requests to multiple likely file or folder paths. Step 3: Record the HTTP status code and the time taken for each response. Step 4: Notice that if the file doesn't exist, the response may be a fast 404. If it does exist but is restricted, the server may take longer and respond with 403. Step 5: This timing difference gives away file existence. Step 6: Use this information to identify hidden files or sensitive configuration paths. Step 7: Defend by standardizing error response times and messages across status codes. Step 8: Avoid 403/404 leakage by using generic 404 for all.
- **Detection**: Log repeated 403/404 timing probes; normalize response times
- **Solution**: Use unified error timing and generic error codes (404 for both cases); add WAF rules
- **Tags**: File Enumeration, Timing Side-Channel, 403/404 Leak

## Brute-Force Hashes w/ Delay

- **Attack Type**: Delayed Hash Brute-Forcing Timing Exploit
- **Target**: APIs, Forms, Token Validation
- **Vulnerability**: Delay-based validation gives timing clues
- **MITRE**: T1216 – Input Capture
- **Impact**: Hash discovery, bypassing token protection
- **Tools**: Python, Burp Suite, hashcat
- **Scenario**: Some applications introduce measurable delays in response to incorrect hash input, helping attackers guess hash input by timing.
- **Attack Steps**: Step 1: Interact with a system that checks user input against a hashed value (e.g., OTP, digital signature, or secure form field). Step 2: Use curl, Burp Repeater, or a custom script to send different values, one at a time. Step 3: Carefully record the response time for each input. Step 4: If correct inputs cause longer processing (due to decryption or DB check), use this delay as an oracle. Step 5: Apply brute-force attacks, prioritizing values that cause longer delays. Step 6: Combine with wordlists or hash permutations to narrow possibilities. Step 7: Eventually match the valid hash input. Step 8: Defend by using constant-time hash comparison and rate-limiting high-frequency hash inputs.
- **Detection**: Analyze spikes in request time tied to user inputs
- **Solution**: Use fixed-time comparisons; introduce random jitter to response time for sensitive endpoints
- **Tags**: Timing, Hash Guessing, Brute Force Delay

## Inference Timing

- **Attack Type**: Timing Leak from AI Inference Layers
- **Target**: AI Model APIs, Edge AI Devices
- **Vulnerability**: Inference-time difference reveals model structure
- **MITRE**: T1208 – Side-Channel Attack
- **Impact**: Reveals class, structure, or sensitive features
- **Tools**: Python, Timeit, Torch/TF, Stopwatch tools
- **Scenario**: ML models take more time to process certain classes or data types, revealing structure or class of input based on delay.
- **Attack Steps**: Step 1: Find an exposed ML model (e.g., hosted via Flask, FastAPI, or cloud ML endpoint). Step 2: Send different inputs and time the server's response using Python (time.time() or stopwatch). Step 3: Observe which inputs take longer — this may suggest that more layers or conditional branches are activated. Step 4: Correlate input types with latency to infer model structure or class label (e.g., images of dogs vs. cats may activate different parts of CNN). Step 5: Use this to reverse-engineer model logic or infer sensitive attributes of the input. Step 6: Defend by introducing random delays or enforcing uniform layer paths for public models.
- **Detection**: Measure latency per class or input pattern; detect anomalies
- **Solution**: Normalize inference time; add jitter; avoid class-conditional computation paths
- **Tags**: ML Security, AI Side-Channel, Model Inference Timing

## Transformer Model Delay

- **Attack Type**: Token-by-Token Output Timing Leak
- **Target**: Transformer APIs (GPT etc.)
- **Vulnerability**: Delay patterns in token output
- **MITRE**: T1208 – Side-Channel Attack
- **Impact**: Vocabulary reconstruction, topic leakage
- **Tools**: Stopwatch, curl, Python, LLM APIs
- **Scenario**: Autoregressive transformers (e.g., GPT) generate output token-by-token. Timing between tokens may leak token type or vocabulary path.
- **Attack Steps**: Step 1: Access an LLM endpoint (like GPT, Claude, or a custom model via API). Step 2: Send input prompts and record the time delay between each generated token using a script. Step 3: Observe patterns — e.g., rare or longer tokens take longer to generate. Step 4: Use this timing data to guess next-token prediction probabilities, reconstruct partial vocab trees, or detect sensitive completions. Step 5: An attacker could reverse the prompt class (e.g., detect if it’s medical, legal, or financial) based on token delay. Step 6: Defend by batching token generation timing or padding with fixed delays between token outputs.
- **Detection**: Monitor for precise timing probes or long prompt durations
- **Solution**: Batch token generation timing or add constant delay per output token
- **Tags**: LLM Timing, Side Channel, GPT Delay, Token Leak

## RAG Model Timing

- **Attack Type**: Retrieval Timing Reveals Data Source
- **Target**: RAG Chatbots, Hybrid ML Systems
- **Vulnerability**: Retrieval time reveals internal content
- **MITRE**: T1592 – Gather Information
- **Impact**: Sensitive doc disclosure, backend structure exposure
- **Tools**: Python, HTTP Monitor, Stopwatch
- **Scenario**: Retrieval-Augmented Generation (RAG) models fetch external context before response — longer delays may hint at large documents or specific internal data being fetched.
- **Attack Steps**: Step 1: Identify an application that uses RAG (e.g., a chatbot with knowledge base lookup). Step 2: Send different types of prompts or keywords. Step 3: Record the time between sending input and receiving output. Step 4: Longer delays typically indicate deeper or more complex retrievals (e.g., 10 vs. 1 documents retrieved). Step 5: Use this timing to deduce if certain documents exist in the backend (e.g., internal emails, confidential manuals). Step 6: Combine this with prompt tuning to locate sensitive topics the model has access to. Step 7: Defend by caching responses, padding retrieval latency, or limiting prompt probes.
- **Detection**: Track query latency per user; alert on unusual probing behavior
- **Solution**: Cache responses; equalize document fetch time; restrict probing keywords
- **Tags**: RAG Security, Timing Leak, Doc Retrieval Leak

## Remote Timing via API

- **Attack Type**: Network Timing Side-Channel (Cloud APIs)
- **Target**: Cloud APIs, SaaS Platforms
- **Vulnerability**: Remote timing reveals backend logic
- **MITRE**: T1595 – Active Scanning
- **Impact**: User or resource enumeration, logic mapping
- **Tools**: curl, Burp Suite, ping, Python
- **Scenario**: Cloud APIs may leak info via timing — e.g., failed vs. successful auth, lookup existence, or backend conditions can be inferred remotely.
- **Attack Steps**: Step 1: Target a cloud-based API (e.g., /validate, /getUser, /checkLicense). Step 2: Send requests with variations in parameters (IDs, tokens, usernames). Step 3: Record response time precisely using scripts. Step 4: Note if different parameters produce measurable differences (e.g., 200ms vs 500ms). Step 5: These differences might reflect user existence, permission level, or backend conditions. Step 6: Use these leaks to enumerate users, find valid tokens, or map internal structure. Step 7: Defend by introducing uniform delays on all responses or padding time with randomness. Step 8: Monitor for frequent timing probes and block IPs doing suspicious enumeration.
- **Detection**: API gateway timing analytics; alert on timing probes
- **Solution**: Uniform response time on all status codes; block IPs probing timing differences
- **Tags**: API Security, Timing Oracle, Cloud Enumeration

## TLS Handshake Timing

- **Attack Type**: Cipher Suite Enumeration via Handshake Time
- **Target**: TLS Servers, Web APIs
- **Vulnerability**: Timing difference during handshake
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Cipher enumeration, downgrade to weak algorithms
- **Tools**: openssl s_client, Wireshark, Python
- **Scenario**: Variations in TLS handshake time may indicate which cipher suites a server prefers, supports, or rejects, revealing its configuration and weaknesses.
- **Attack Steps**: Step 1: Identify the target server that supports HTTPS or another TLS-based service (e.g., mail server, API). Step 2: Use openssl s_client or a Python script to connect using different sets of cipher suites. Step 3: Record the time each handshake takes. Step 4: Longer handshakes or failure timeouts help infer whether a cipher suite was accepted, rejected, or negotiated. Step 5: Use this info to map out supported cipher suites, including any legacy or weak algorithms. Step 6: Weak ciphers (like RC4, 3DES) can be targeted for downgrade or MITM attacks. Step 7: Defend by disabling legacy ciphers and enforcing TLS 1.3 where possible. Step 8: Use monitoring tools to detect unusual TLS scanning behavior.
- **Detection**: Log handshake times and detect scan patterns
- **Solution**: Disable legacy ciphers; enforce strong TLS config
- **Tags**: TLS Timing, Cipher Scanning, Handshake Enumeration

## Certificate Validation Delay

- **Attack Type**: OCSP/CA Timing Oracle
- **Target**: Web Apps using HTTPS
- **Vulnerability**: OCSP/CRL response time leaks cert state
- **MITRE**: T1557.002 – Man-in-the-Middle: HTTPS Spoofing
- **Impact**: Reveal revoked certs, CA misconfiguration
- **Tools**: curl, openssl, Burp Suite, Wireshark
- **Scenario**: Delay in validating a certificate via OCSP (Online Certificate Status Protocol) reveals revocation status, CA level, or responder availability, leaking certificate lifecycle details.
- **Attack Steps**: Step 1: Identify a TLS-enabled web application that uses OCSP or CRL for certificate validation. Step 2: Trigger multiple HTTPS requests and monitor how long it takes to complete the handshake. Step 3: Use a network sniffer like Wireshark to analyze OCSP/CRL traffic. Step 4: Noticeably longer or shorter delays may indicate whether a certificate is revoked, near expiry, or issued by an intermediate vs. root CA. Step 5: Use this timing to deduce the internal PKI structure or detect revoked/stale certs. Step 6: Combine with MitM setups or proxying to manipulate OCSP responses. Step 7: Defend by enabling OCSP stapling and short TTLs for revocation responses.
- **Detection**: Monitor for excessive or abnormal revocation checks
- **Solution**: Use OCSP stapling; cache cert status securely; reduce reliance on live OCSP checks
- **Tags**: PKI Timing, OCSP Oracle, Cert Leak

## Shared Cloud VM Timing

- **Attack Type**: Cross-VM Timing Attack
- **Target**: Cloud VM Hosts, Multi-tenant
- **Vulnerability**: Timing + cache reveals tenant behavior
- **MITRE**: T1208 – Side-Channel Attack
- **Impact**: Tenant leakage, key exfiltration, surveillance
- **Tools**: Prime+Probe, Flush+Reload, perf tools
- **Scenario**: On shared cloud infrastructure (e.g., AWS EC2), attackers measure timing and cache access to spy on neighboring VMs running on the same physical machine.
- **Attack Steps**: Step 1: Launch a VM instance in a cloud provider (like AWS EC2 or Azure). Step 2: Try to co-locate on the same physical machine as the target (e.g., via timing-based detection or placement strategy). Step 3: Use side-channel techniques like Prime+Probe or Flush+Reload to measure cache access patterns. Step 4: Identify activity patterns (e.g., SSH logins, app activity, crypto operations) happening in neighboring VMs. Step 5: Use this info to extract cryptographic key usage or sensitive operations timing. Step 6: Defend by isolating tenants (dedicated hosts), disabling simultaneous multithreading (SMT), and adding noise to timing. Step 7: Monitor for unusual cache access or high-resolution timers being invoked.
- **Detection**: Check for side-channel tools or unusual process timing
- **Solution**: Use dedicated VM instances; disable SMT; cache isolation and access auditing
- **Tags**: Cloud Side-Channel, Cross-VM, Cache Timing

## Function-as-a-Service Delay

- **Attack Type**: Serverless Timing Leak
- **Target**: AWS Lambda, Azure Functions
- **Vulnerability**: Response delay leaks logic and permission level
- **MITRE**: T1600 – Weaken Encryption (Timing Leakage)
- **Impact**: Logic enumeration, role escalation inference
- **Tools**: Stopwatch, Python, AWS CLI, Postman
- **Scenario**: Functions (e.g., AWS Lambda, Google Cloud Functions) reveal logic or permission level based on cold-start delays, execution time, or I/O latency.
- **Attack Steps**: Step 1: Identify an exposed Function-as-a-Service (FaaS) endpoint (e.g., via public API or event triggers). Step 2: Send multiple requests with different payloads or paths. Step 3: Record the execution time of each response. Step 4: Cold starts may take longer (~1s), and logic branching or database access may introduce additional delays. Step 5: Analyze timing to infer function behavior — such as permission checks, user existence, or backend integration. Step 6: Repeated probing can map logic pathways and privilege levels. Step 7: Defend by enabling provisioned concurrency (avoid cold start), normalizing output latency, and limiting request rate. Step 8: Use monitoring tools to detect probing patterns or latency analysis attempts.
- **Detection**: Function observability tools; correlate latency to IP or payload
- **Solution**: Use constant-time logic; provisioned concurrency; restrict probing
- **Tags**: Serverless, Cloud Timing, FaaS Info Leak

## Flush+Reload (Timing SCA)

- **Attack Type**: Cache-Based Side-Channel via Timing
- **Target**: Shared Memory Crypto Systems
- **Vulnerability**: Timing-based memory access detection
- **MITRE**: T1208 – Side Channel Attack
- **Impact**: AES key leakage, cryptographic compromise
- **Tools**: perf, rdtsc, custom C code, Flush+Reload PoC
- **Scenario**: Attacker infers if a shared memory location (e.g., crypto table or key) was accessed by timing how long it takes to reload after flush.
- **Attack Steps**: Step 1: The attacker runs code on the same physical CPU core or shared memory region (such as shared libraries) as the victim. Step 2: Use the clflush instruction to flush a specific memory location (e.g., an AES lookup table entry). Step 3: Wait for the victim to perform encryption using a private key. Step 4: Use high-resolution timers (e.g., rdtsc) to measure how long it takes to reload that memory location. Step 5: A fast reload indicates that the victim accessed the memory — revealing key-dependent access patterns. Step 6: Repeat across many keys to reconstruct the full key bit-by-bit. Step 7: Defend by using constant-time cryptography and disabling shared memory for sensitive code.
- **Detection**: Monitor for use of clflush, high-frequency memory access
- **Solution**: Use constant-time libraries; disable shared memory for sensitive functions
- **Tags**: Flush+Reload, Timing, Cache SCA

## Prime+Probe

- **Attack Type**: Cache Line Eviction-Based Inference
- **Target**: CPU Cache on Shared Systems
- **Vulnerability**: Cache eviction reveals memory usage pattern
- **MITRE**: T1208 – Side Channel Attack
- **Impact**: Sensitive data exfiltration via timing cache probes
- **Tools**: perf, Prime+Probe C code, Intel VTune
- **Scenario**: Attacker fills cache sets, waits, and probes them to see if the victim accessed memory in the same set — no shared memory needed.
- **Attack Steps**: Step 1: Attacker identifies a cache set that may be used by the victim's sensitive operation (e.g., crypto key lookup). Step 2: Fill the cache set with attacker’s own data (prime phase). Step 3: Wait for victim to execute — possibly evicting some attacker data from the cache. Step 4: Re-access the same memory (probe phase) and measure access time. Step 5: Slower access = victim used same cache line → attacker infers key-dependent access. Step 6: Repeat over many rounds to leak bits of the cryptographic key. Step 7: Unlike Flush+Reload, this doesn’t require shared memory. Step 8: Defend by using cache isolation (page coloring), disabling simultaneous multithreading (SMT), and employing constant-time crypto code.
- **Detection**: Detect abnormal cache accesses and timing measurements
- **Solution**: Implement constant-time algorithms; disable SMT; isolate sensitive cache pages
- **Tags**: Prime+Probe, Side-Channel, Cache Attack

## Spectre Variant

- **Attack Type**: Speculative Execution Side-Channel
- **Target**: CPU with Speculative Execution
- **Vulnerability**: Speculative access to sensitive memory
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Arbitrary memory leak, sandbox bypass
- **Tools**: Spectre PoC code, C compiler, browser JS
- **Scenario**: Exploits CPU speculative execution to access and leak unauthorized memory via side channels, such as timing-based cache access.
- **Attack Steps**: Step 1: Understand that Spectre abuses speculative execution — the CPU predicts and runs future instructions before they are needed. Step 2: Attacker uses mispredicted branches to trick CPU into executing out-of-bounds memory access during speculation. Step 3: Although the CPU discards the results later, any memory access still loads cache lines. Step 4: Attacker then measures which memory was loaded using a cache timing attack (e.g., Flush+Reload). Step 5: Using this, attacker can infer values from protected memory (like keys or passwords). Step 6: Spectre can work across process boundaries, web browsers (via JS), and even VMs. Step 7: Defend via Spectre mitigations in OS/firmware, using Retpoline, or disabling speculative features. Step 8: Monitor for speculative probing code via CPU counters.
- **Detection**: Monitor use of high-res timers and speculative code sequences
- **Solution**: Use firmware updates; enable OS mitigations like Retpoline, KPTI, Site Isolation in browsers
- **Tags**: Spectre, Cache Timing, Speculative SCA

## Meltdown Exploit

- **Attack Type**: Kernel Memory Side-Channel via Speculation
- **Target**: CPUs without KPTI Isolation
- **Vulnerability**: Speculative access to kernel memory
- **MITRE**: T1208 – Side Channel Attack
- **Impact**: Full kernel memory leak, sandbox escape
- **Tools**: Meltdown PoC, rdtsc, Linux tools
- **Scenario**: Like Spectre, but reads kernel memory directly by executing invalid memory access and measuring which data was cached.
- **Attack Steps**: Step 1: Target a vulnerable CPU (Intel pre-2018) running Linux or Windows. Step 2: Write user-space code that tries to read a kernel-only memory address (normally not permitted). Step 3: The CPU speculatively executes the instruction before realizing it’s illegal. Step 4: The data is loaded into cache before the CPU blocks access. Step 5: Use timing attacks like Flush+Reload to determine which byte value was read. Step 6: Repeat over memory ranges to dump kernel memory, credentials, or secrets. Step 7: Defend by enabling Kernel Page Table Isolation (KPTI) or upgrading CPUs with Meltdown mitigations. Step 8: Monitor system for abnormal access patterns and high-res timers. Step 9: Disable untrusted apps from running on sensitive hosts.
- **Detection**: Enable KPTI; block unprivileged high-resolution timers
- **Solution**: Meltdown, Kernel Memory, Timing SCA
- **Tags**: Intel, USENIX

## JavaScript Timing Attack

- **Attack Type**: Client-Side Timing-Based Side-Channel
- **Target**: Web Login Forms
- **Vulnerability**: Time-based password comparison logic
- **MITRE**: T1208 – Side Channel Attack
- **Impact**: Full password disclosure via web timing
- **Tools**: Browser Dev Tools, performance.now()
- **Scenario**: High-resolution JavaScript timers (e.g., performance.now()) are used to measure how long a page takes to validate each character of a password.
- **Attack Steps**: Step 1: Attacker creates a malicious website with a login form that mimics a target site. Step 2: Using JavaScript's performance.now(), the attacker measures how long it takes for each login attempt to return a response (client or server delay). Step 3: If the password validation is character-by-character, then entering a correct prefix causes a longer delay. Step 4: Attacker uses this delay difference to identify correct characters one at a time. Step 5: By iterating this process, the attacker reconstructs the full password. Step 6: This works best if the validation is done in JavaScript or has client-visible timing. Step 7: Defenders can mitigate by using constant-time comparison functions and limiting precision of JavaScript timers in browsers.
- **Detection**: Monitor for unusual timing APIs usage in browser scripts
- **Solution**: Use constant-time comparisons; limit JS timer resolution using browser settings (e.g., 100ms granularity)
- **Tags**: JS Timing, Side-Channel, Login Guess

## Cross-Site Search Attack

- **Attack Type**: Search-Based Timing Information Leak
- **Target**: Web Apps with Search APIs
- **Vulnerability**: Timing leaks in search result loading
- **MITRE**: T1210 – Exploitation of Remote Services
- **Impact**: Disclosure of personal or account data
- **Tools**: Custom JS, Browser Extensions
- **Scenario**: If a web app autocompletes or filters results based on secret user data, timing attacks can reveal sensitive queries like emails, documents, or history.
- **Attack Steps**: Step 1: Attacker creates a malicious site that causes the victim’s browser (while logged in) to send hidden search requests to a known web app (via image tags or iframes). Step 2: Measure the time taken to load or fail each hidden search request using JS timers or onload/onerror. Step 3: Based on the delay, determine whether a matching result exists on the victim’s account. Step 4: Iterate through common terms (like names, email addresses, keywords) to map out what exists in the victim's search history or account. Step 5: Optionally, exfiltrate results via cross-origin scripts or covert channels. Step 6: Defend by adding CSRF protections, disallowing cross-origin search, and padding response times. Step 7: Disable autofill search features for sensitive user data.
- **Detection**: Observe network traffic for search via non-user interaction; check iframe/image abuse
- **Solution**: Add same-site cookies, use CSRF protection, disable auto-complete for sensitive searches
- **Tags**: Search Leak, Timing, Cross-Site

## CSRF Token Guess

- **Attack Type**: Brute Force on Unpredictable Token
- **Target**: Web Forms, Sessions
- **Vulnerability**: Weak CSRF token randomness
- **MITRE**: T1110 – Brute Force
- **Impact**: Unauthorized actions on behalf of user
- **Tools**: Burp Suite, curl, Custom Scripts
- **Scenario**: Attacker tries to guess valid CSRF tokens if the generation algorithm is weak, predictable, or based on time, allowing unauthorized requests.
- **Attack Steps**: Step 1: Attacker examines the structure of CSRF tokens used in forms or AJAX requests (e.g., base64, hex, JWT). Step 2: Checks if the tokens are derived from weak elements like timestamps, user ID, or short random seeds. Step 3: Attempts to brute-force or predict token values based on known patterns (e.g., if it's a Unix timestamp, try current/previous seconds). Step 4: Sends forged requests using guessed tokens to sensitive endpoints (e.g., change password, transfer funds). Step 5: If the server accepts the request, the token was successfully guessed. Step 6: Repeats the process to escalate privileges or persist in the system. Step 7: To defend, use cryptographically secure, high-entropy CSRF tokens (e.g., 256-bit random values) that expire frequently.
- **Detection**: Monitor CSRF token verification failures; check token entropy
- **Solution**: Use strong CSRF token generators; bind tokens to session/IP; enforce expiration
- **Tags**: CSRF, Token Guess, Web Exploit

## Simple Power Analysis (SPA)

- **Attack Type**: Side-Channel via Power Trace Observation
- **Target**: Smartcards, HSMs
- **Vulnerability**: Power consumption tied to key-dependent ops
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: Full key recovery through physical power trace
- **Tools**: Oscilloscope, ChipWhisperer, Smartcard Reader
- **Scenario**: SPA involves visually analyzing power consumption graphs to find patterns revealing secret keys or operations in devices like smartcards or IoT chips.
- **Attack Steps**: Step 1: Attacker connects a power analysis device (like ChipWhisperer) to the power line of a cryptographic device (smartcard, HSM, or embedded system). Step 2: Initiates the same cryptographic operation (e.g., RSA signature or AES encryption) multiple times to capture consistent power traces. Step 3: Visually inspects the graph of power consumption over time. Step 4: Identifies repetitive spikes or flat regions corresponding to instructions like XOR, multiplication, or conditional branches. Step 5: Recognizes key-dependent variations in timing or amplitude that reveal key bits (e.g., if '1' causes a multiply operation, you'll see a spike). Step 6: Combines these clues to infer the secret key one bit at a time. Step 7: SPA is highly effective against poorly shielded or unbalanced cryptographic routines.
- **Detection**: Analyze power traces for repetition; compare power vs time graphs during encryption
- **Solution**: Balance all key operations; use power noise generation (masking/shuffling)
- **Tags**: SPA, Smartcards, Power Analysis

## Differential Power Analysis (DPA)

- **Attack Type**: Statistical Power Side-Channel
- **Target**: Embedded Crypto Devices
- **Vulnerability**: Key-dependent leakage in power signature
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: AES, RSA, ECC key extraction from physical devices
- **Tools**: ChipWhisperer, Python, Oscilloscope
- **Scenario**: DPA uses hundreds or thousands of power traces and statistical analysis (like difference of means) to recover secret keys in symmetric crypto (e.g., AES).
- **Attack Steps**: Step 1: Connect a power analysis tool to the cryptographic device and run many encryption/decryption operations with known inputs (e.g., chosen plaintexts). Step 2: Record power traces for each operation with high precision (often in nanoseconds). Step 3: For each key guess (e.g., 0-255 for AES subkey), use a model (like Hamming weight of intermediate value) to predict expected power. Step 4: Use statistical correlation (like difference of means) to compare predicted vs actual power. Step 5: The correct key guess will show a strong statistical match. Step 6: Repeat this per key byte (e.g., 16 times for AES-128) to reconstruct the full key. Step 7: DPA works even if individual traces don’t show anything — it relies on aggregate statistics over many runs.
- **Detection**: Use statistical test sets; observe deviation from expected power during known inputs
- **Solution**: Add masking/shuffling; separate sensitive ops from observable power
- **Tags**: DPA, AES, Power Trace, Crypto Chips

## High-Order Differential Power Analysis

- **Attack Type**: Multi-Trace Power Attack
- **Target**: Crypto Co-Processors
- **Vulnerability**: Multi-register leakage across masked operations
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: Bypasses first-order masking protections
- **Tools**: Advanced ChipWhisperer, NumPy/SciPy
- **Scenario**: HO-DPA enhances DPA by targeting leakage in higher-order power moments (e.g., combined influence of multiple registers or masked variables).
- **Attack Steps**: Step 1: Collect a very large number of power traces (typically >10,000) from the device performing cryptographic operations with known inputs. Step 2: Use power model predictions (e.g., Hamming weight) across multiple leakage points and higher-order combinations (e.g., square of trace values, products of multiple trace segments). Step 3: Apply statistical correlation (like covariance or multidimensional correlation) between observed traces and model predictions. Step 4: Identify key guesses that correlate strongly across these higher-order leakages. Step 5: Requires pre-processing to align traces and reduce noise. Step 6: Works especially well against devices using masking (i.e., adding random values to hide operations). Step 7: Once enough correlation is found, attacker reconstructs key bits by combining partial leaks across higher-order samples.
- **Detection**: Use multivariate analysis to detect unexpected patterns in power trace combinations
- **Solution**: Implement higher-order masking; use random delays and reordering
- **Tags**: HO-DPA, High Order Leakage, Power SCA

## Correlation Power Analysis (CPA)

- **Attack Type**: Correlation-Based Side-Channel
- **Target**: AES/DES Crypto Hardware
- **Vulnerability**: Correlation of key-dependent power consumption
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: Full symmetric key extraction
- **Tools**: ChipWhisperer, Python, Jupyter
- **Scenario**: CPA correlates expected power usage (from key guesses) with actual power trace data to statistically extract symmetric keys like AES or DES.
- **Attack Steps**: Step 1: Set up a testbed with a target crypto device and record hundreds or thousands of power traces while providing known inputs (plaintexts or ciphertexts). Step 2: Build a hypothesis: for each possible key byte (e.g., 0-255), compute the intermediate value (e.g., AES S-box output) and its Hamming weight. Step 3: Measure actual power usage per operation using the oscilloscope. Step 4: Calculate the Pearson correlation coefficient between predicted Hamming weight and real power consumption. Step 5: A strong correlation peak indicates the correct key guess. Step 6: Repeat this for each key byte (e.g., 16 bytes for AES-128). Step 7: Combine results to reconstruct full encryption key. Step 8: CPA is more accurate and noise-resistant than SPA and often succeeds even in slightly protected devices.
- **Detection**: Statistical correlation tests between model and trace
- **Solution**: Add noise, insert random delays, implement proper masking
- **Tags**: CPA, Hamming Weight, Side-Channel AES

## Template Attack

- **Attack Type**: Power Side-Channel Template Modeling
- **Target**: Crypto Chips, Smartcards
- **Vulnerability**: Known hardware behavior matched to models
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: Extremely accurate key extraction in very few traces
- **Tools**: ChipWhisperer, Oscilloscope, Python (NumPy)
- **Scenario**: Template Attacks involve building a detailed profile of power consumption for each possible key value and matching them with live measurements to recover keys.
- **Attack Steps**: Step 1: Attacker gains physical access to an identical device (same crypto chip or firmware) and sets it up for controlled experiments. Step 2: For each possible value of the secret key byte (0–255), the attacker runs many encryptions and captures high-resolution power traces. Step 3: Computes average power consumption patterns (templates) for each key byte using statistical tools like mean vectors and covariance matrices. Step 4: When targeting the victim device, attacker captures just one or a few power traces during encryption. Step 5: Compares these unknown traces to the pre-built templates and selects the key byte whose profile matches best. Step 6: Repeats for all key bytes to recover full encryption key. Step 7: This is extremely accurate and works even when countermeasures like noise or masking are used—because the attack uses probabilistic matching and modeling.
- **Detection**: Analyze matching between live trace and templates
- **Solution**: Use constant-time operations, avoid key-dependent branching, add noise/masking
- **Tags**: Power SCA, Template Attack, Modeling, CPA

## AES Power Attack

- **Attack Type**: AES S-Box Power Side-Channel
- **Target**: Embedded AES Devices
- **Vulnerability**: S-box power leakage during SubBytes
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: AES-128/192/256 full key recovery
- **Tools**: ChipWhisperer, Python, Scapy
- **Scenario**: Targets specific operations in AES (especially SubBytes) where power consumption correlates strongly with key-dependent activity.
- **Attack Steps**: Step 1: Connect ChipWhisperer or another oscilloscope to AES-enabled device (e.g., embedded board, smartcard). Step 2: Send a large number of known plaintexts into AES encryption and collect the corresponding power traces. Step 3: For each guess of an AES subkey byte (0–255), compute the intermediate value of the S-box output and its Hamming weight. Step 4: Compare predicted Hamming weights to actual trace samples using correlation (CPA) or differential analysis (DPA). Step 5: Identify the key byte with the highest correlation value. Step 6: Repeat this for all 16 AES key bytes. Step 7: Combine all recovered bytes to get the complete AES key. Step 8: Validate correctness by checking whether AES decryption with this key returns expected plaintext. Step 9: This works even on partially protected AES implementations, especially those without masking or blinding.
- **Detection**: Measure and correlate S-box leakage; match byte-wise traces
- **Solution**: Apply S-box masking and shuffling; equalize power regardless of S-box input/output
- **Tags**: AES, S-box, Power Trace, DPA, CPA

## DES Power Analysis

- **Attack Type**: Side-Channel on Feistel Functions
- **Target**: Legacy DES Hardware
- **Vulnerability**: Weak/no protection of S-box-related leakage
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: Full DES key recovery in embedded systems
- **Tools**: Oscilloscope, ChipWhisperer, Python
- **Scenario**: Uses CPA/DPA on S-boxes and round logic in DES encryption to reconstruct 56-bit DES keys.
- **Attack Steps**: Step 1: Target a device implementing DES (e.g., legacy hardware or older embedded systems). Step 2: Send chosen plaintexts and record power traces during encryption. Step 3: Focus on initial or middle rounds of DES where key and data are mixed via XOR and passed through S-boxes. Step 4: Guess key bits that affect specific S-boxes, compute expected S-box outputs, and their Hamming weights. Step 5: Correlate predicted Hamming weights with power traces to find matching key bits. Step 6: Repeat across all rounds and all 8 S-boxes to recover 56-bit DES key. Step 7: Verify the key using known-plaintext ciphertext pairs. Step 8: Despite being old, many embedded systems (like older card readers or factory systems) still use DES, making them vulnerable.
- **Detection**: Compare Hamming weights of S-box inputs vs power traces
- **Solution**: Migrate away from DES; use AES with proper side-channel protection
- **Tags**: DES, S-box, Legacy, Power Analysis

## RSA Power Timing (Montgomery)

- **Attack Type**: RSA Modular Exponentiation Timing Leak
- **Target**: RSA Software/Hardware
- **Vulnerability**: Key-bit-dependent timing during exponentiation
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: Full RSA private key recovery
- **Tools**: ChipWhisperer, Oscilloscope, Python Timing
- **Scenario**: Exploits timing variations in RSA's Montgomery ladder or square-and-multiply routines to recover bits of the private key.
- **Attack Steps**: Step 1: Set up timing observation on RSA operations (signing or decryption), either through power trace or just wall-clock timing via side channel. Step 2: Focus on modular exponentiation, which is often implemented with square-and-multiply or Montgomery ladder. Step 3: Record many RSA decryptions or signatures and measure the exact timing (or power usage) of each operation. Step 4: Note that depending on the bit value of the private exponent (0 or 1), the algorithm performs either only square or square+multiply, leading to time/power differences. Step 5: Use this to guess one private key bit at a time. Step 6: Repeat for all bits (commonly 1024–4096). Step 7: Rebuild the full RSA private key. Step 8: This works even in software-based crypto libraries if constant-time coding is not enforced.
- **Detection**: Detect timing variation between 0 and 1 bits during exponentiation
- **Solution**: Use constant-time Montgomery Ladder; enforce side-channel hardened crypto libraries
- **Tags**: RSA, Montgomery Ladder, Square-Multiply, Timing

## DSA/ECDSA Leakage via Nonce Use

- **Attack Type**: Side-Channel Attack on Signing Keys
- **Target**: Signing Devices (DSA/ECDSA)
- **Vulnerability**: Leakage of random nonce during signature
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: Complete compromise of signing key; forged signatures
- **Tools**: ChipWhisperer, Oscilloscope, Python (SciPy, NumPy)
- **Scenario**: Attacker uses power analysis to recover the nonce (k) used in DSA/ECDSA signing, allowing full private key recovery.
- **Attack Steps**: Step 1: The attacker targets a cryptographic device or software that performs DSA or ECDSA signing operations (like smartcards, HSMs, or embedded devices). Step 2: Repeatedly trigger signing operations with known messages and record high-resolution power traces during each operation. Step 3: Focus analysis on the part of the signature computation involving the nonce k, often used in scalar multiplication or modular inversion. Step 4: Analyze trace data (via CPA/DPA) to extract information about the value of k. Step 5: Since signature formula is public (r, s), and attacker now knows k, the private signing key x can be computed with simple algebra. Step 6: Validate recovered private key by verifying future signatures. Step 7: This attack breaks full confidentiality of digital signatures and allows forging. Step 8: Even minor leakage (partial k) can be enough to reconstruct full x.
- **Detection**: Monitor power signature of signing process; detect unusual correlations
- **Solution**: Use deterministic nonce (RFC 6979), apply masking and blinding to k, avoid key-dependent power spikes
- **Tags**: DSA, ECDSA, Power Analysis, Signature Forgery

## ECC Scalar Mult Leakage

- **Attack Type**: ECC Scalar Multiplication Power Attack
- **Target**: ECC Crypto Devices
- **Vulnerability**: Scalar multiplication leaks via power signature
- **MITRE**: T1208 – Side-Channel Attacks
- **Impact**: ECC key compromise, session hijack, signature forgery
- **Tools**: ChipWhisperer, Oscilloscope, Python
- **Scenario**: Leakage from point multiplication reveals the ECC private scalar, compromising ECDH and ECDSA schemes.
- **Attack Steps**: Step 1: The attacker gains physical or EM access to a device using ECC (Elliptic Curve Cryptography), such as smartcards, key fobs, or mobile chips. Step 2: Observes power traces while the device performs scalar multiplication (Q = d × G), where d is the secret scalar (private key). Step 3: Identifies operation timing or power variation based on scalar bits (0 or 1). Step 4: Uses Simple Power Analysis (SPA) or Correlation Power Analysis (CPA) to deduce the bit values of d. Step 5: Repeats this across multiple scalar bits until the full private key is reconstructed. Step 6: Validates the private key by performing ECDSA or ECDH operations with it and checking the match. Step 7: Even ECC implementations on modern chips can be vulnerable if scalar multiplication isn't blinded. Step 8: This attack breaks both encryption (ECDH) and authentication (ECDSA) security.
- **Detection**: Track operation-level power variations during point multiplication
- **Solution**: Use constant-time ECC ops; implement scalar randomization (blinding); add dummy operations
- **Tags**: ECC, Scalar Leakage, Curve25519, ECDH, ECDSA

## Differential Fault Analysis (DFA)

- **Attack Type**: Fault Injection + Power Combo
- **Target**: Crypto Chips (AES/RSA)
- **Vulnerability**: Fault propagation reveals internal secrets
- **MITRE**: T1611 – Hardware Fault Injection
- **Impact**: Full AES/RSA key recovery in presence of faults
- **Tools**: ChipSHOUTER, Laser Glitchers, ChipWhisperer, Python
- **Scenario**: Attacker injects faults during encryption (e.g., flipped bits) and combines with power traces to recover internal secrets like AES or RSA keys.
- **Attack Steps**: Step 1: The attacker targets a crypto device performing encryption (AES, RSA, etc.) and repeatedly runs it with the same input. Step 2: During each run, attacker introduces a physical fault—such as voltage glitch, EM pulse, or laser shot—during a specific stage of the encryption (e.g., last round). Step 3: Records the faulty ciphertext output and compares it with correct ciphertext. Step 4: Based on the difference (ΔC), attacker infers what internal data was corrupted. Step 5: Applies differential cryptanalysis techniques to trace the fault back to the original key bits. Step 6: Repeats this over multiple ciphertexts to reconstruct the entire key. Step 7: In AES, a single bit fault in the last round allows full key recovery with ~50 ciphertexts. Step 8: Combines with power analysis to pinpoint round location and confirm key guesses. Step 9: Works on protected devices if fault location is precise.
- **Detection**: Monitor for repeated faults; verify ciphertext integrity
- **Solution**: Use redundancy checks, error-correcting codes, and hardware tamper protection
- **Tags**: DFA, AES, RSA, Fault Injection, Crypto Hardware

## Voltage Glitch + SPA/DPA

- **Attack Type**: Voltage Faults + Power Analysis Combo
- **Target**: Crypto Microcontrollers
- **Vulnerability**: Instruction skipping exposes key operations
- **MITRE**: T1611 – Fault Injection
- **Impact**: Secret key extraction or bypass of secure checks
- **Tools**: ChipSHOUTER, Oscilloscope, ChipWhisperer, Fault Tools
- **Scenario**: Combines voltage fault injection with power analysis to skip operations or leak power-dependent patterns during crypto execution.
- **Attack Steps**: Step 1: The attacker connects a glitching tool like ChipSHOUTER to the voltage supply of a crypto chip (smartcard, MCU, HSM). Step 2: Times the glitch to occur during a specific function, such as password check, key schedule, or AES round loop. Step 3: A successful glitch causes the system to skip an instruction or logic branch (e.g., bypassing a security check or jumping over key masking). Step 4: Meanwhile, the attacker records power traces during the glitched run. Step 5: If key-dependent masking or scrambling is skipped, clean power traces reveal raw key-dependent data. Step 6: Uses SPA or DPA on this glitched trace to extract secret keys. Step 7: Repeats glitching and tracing to isolate exploitable moments. Step 8: Glitching often bypasses both logical and physical protections temporarily, opening up attack vectors.
- **Detection**: Detect glitch attempts via power monitoring or runtime integrity checks
- **Solution**: Add voltage monitors, randomize timing, use secure boot and anti-glitch sensors
- **Tags**: Voltage Glitch, Fault Injection, SPA/DPA, AES, RSA

## Clock Glitch Injection

- **Attack Type**: Fault Injection
- **Target**: Embedded Devices
- **Vulnerability**: Skipped instructions from clock manipulation
- **MITRE**: T1611 – Fault Injection
- **Impact**: Bypass authentication, extract crypto secrets
- **Tools**: ChipWhisperer, FPGA Clock Injector, Logic Analyzer
- **Scenario**: Alters device clock rate temporarily during crypto operations to skip security logic or corrupt internal states.
- **Attack Steps**: Step 1: Connect a glitch injection setup to a device performing cryptographic operations (e.g., AES, secure boot). Step 2: Use high-precision tools to deliver a sudden change (spike or dip) in the device’s clock signal at a critical time—like during key checks or signature validation. Step 3: Monitor device behavior—if the glitch was successful, it might skip an instruction or validate an invalid signature. Step 4: Record the power trace and response (success/failure) to determine timing windows. Step 5: Exploit the glitch repeatedly to extract secrets, bypass authentication, or force the device into insecure states. Step 6: Combine with power analysis (SPA/DPA) to extract key-dependent patterns.
- **Detection**: Clock anomaly monitoring; timing deviation detection
- **Solution**: Use clock monitors; employ constant-time logic; apply glitch filters
- **Tags**: Fault Injection, Clock Glitch, Embedded Crypto

## Electromagnetic Fault Injection (EMFI)

- **Attack Type**: Physical Fault Injection
- **Target**: Secure Chips, Smartcards
- **Vulnerability**: Corrupted crypto ops via EM interference
- **MITRE**: T1611 – Electromagnetic Injection
- **Impact**: Full key recovery or bypass of validation logic
- **Tools**: EM Probe (e.g., Riscure EMFI), ChipSHOUTER, Oscilloscope
- **Scenario**: Use focused EM pulses to flip bits or skip instructions in cryptographic devices during sensitive operations.
- **Attack Steps**: Step 1: Set up a high-precision EM pulse generator aimed at the target chip or area responsible for cryptographic operations. Step 2: Send EM pulses synchronized with crypto execution—like AES S-box computation or RSA modular exponentiation. Step 3: The induced EM fault corrupts data (e.g., flips a byte or skips a branch). Step 4: Capture output or power traces during faulted operations. Step 5: Analyze faulty outputs to trace back to key bytes using Differential Fault Analysis (DFA) or algebraic methods. Step 6: Repeat until enough faults reveal full key or bypass checks. Step 7: Validate attack by testing extracted key or bypass path.
- **Detection**: EM anomaly detection; abnormal operation monitoring
- **Solution**: Use EM shielding; employ fault detection logic; randomize operation timing
- **Tags**: EMFI, Fault Injection, Crypto Hardware, AES, RSA

## Laser-Induced Fault Analysis

- **Attack Type**: Optical Fault Injection
- **Target**: Crypto Microcontrollers
- **Vulnerability**: Instruction/data corruption via laser targeting
- **MITRE**: T1611 – Laser Fault Injection
- **Impact**: Key extraction, privilege escalation
- **Tools**: Infrared Laser Injector, Oscilloscope, Laser Station
- **Scenario**: Targets chips using precise laser pulses to induce computation faults, useful for skipping instructions or leaking key info.
- **Attack Steps**: Step 1: Position a focused laser system over the crypto chip (open-die access often required). Step 2: Fire laser pulses during execution of secure operations—e.g., AES key expansion, RSA decryption loop. Step 3: Laser energy flips bits, causes computation faults, or halts the CPU mid-operation. Step 4: Collect the resulting corrupted output or observe any bypass in protection. Step 5: Repeat pulses at different locations/times to map vulnerable areas of the silicon. Step 6: Combine with power analysis or DFA to deduce the secret key. Step 7: Validate the extracted key or exploit the bypass achieved via induced faults.
- **Detection**: Unexpected operation, optical sensors on chip
- **Solution**: Use laser shields, integrated photodiode detectors, redundancy checks in critical paths
- **Tags**: Laser Fault Injection, AES, RSA, Smartcard Security

## Remote Power Analysis via USB

- **Attack Type**: Remote Side-Channel Analysis
- **Target**: USB-Connected Crypto HW
- **Vulnerability**: Unshielded power channel leaks crypto behavior
- **MITRE**: T1208 – Power Side Channel Attacks
- **Impact**: Key recovery without physical disassembly or access
- **Tools**: USB Analyzer, Oscilloscope, Python, PoC Tools
- **Scenario**: Attackers exploit power fluctuations over USB power lines to perform side-channel analysis on connected crypto-enabled devices.
- **Attack Steps**: Step 1: Connect to a target embedded or IoT device over USB (e.g., USB-powered HSM, crypto dongle). Step 2: Measure power consumption fluctuations via USB power line during crypto operations (e.g., encrypt, sign). Step 3: Record power traces over multiple sessions. Step 4: Use SPA or DPA to analyze differences and identify key-dependent computations. Step 5: Perform statistical correlation to reconstruct keys or data from power variation patterns. Step 6: This attack can be done remotely via a malicious charging port or modified USB hub. Step 7: Optional: Combine with firmware manipulation or known input ciphertexts for more accurate results.
- **Detection**: Abnormal USB power draw patterns; unauthorized USB devices
- **Solution**: Use power filters, constant current regulators, and disable crypto during untrusted USB connection sessions
- **Tags**: USB Power Analysis, SPA, IoT Crypto, Remote Attacks

## Radio Leakage from Power Rails

- **Attack Type**: Electromagnetic Power Side-Channel
- **Target**: Embedded Crypto Hardware
- **Vulnerability**: EM leakage through power rail emissions
- **MITRE**: T1208 – Power/Energy Side Channels
- **Impact**: Secret key leakage via unintended EM emissions
- **Tools**: RF Probe, SDR (e.g., HackRF, USRP), Antennas, GNU Radio
- **Scenario**: Cryptographic chips may unintentionally emit radio frequency (RF) signals modulated by power usage, which attackers can capture.
- **Attack Steps**: Step 1: Set up an RF antenna and SDR receiver near a crypto-enabled device (e.g., smartcard reader, embedded controller). Step 2: Tune SDR to the frequencies emitted by power rail fluctuations (e.g., MHz range). Step 3: Capture emitted signals during known cryptographic activity (like AES encryption). Step 4: Use signal processing tools (e.g., GNU Radio, MATLAB) to extract modulation patterns. Step 5: Correlate RF emissions with expected operation timings to infer key-dependent behavior. Step 6: Perform SPA or DPA on processed RF trace data. Step 7: Validate findings by reproducing known crypto operations.
- **Detection**: RF spectrum anomaly detection; proximity signal analysis
- **Solution**: Shield power rails, use differential signaling, apply EM noise injection
- **Tags**: EM Leakage, RF Side-Channel, Hardware Crypto

## Power Line Monitoring Attack

- **Attack Type**: Infrastructure-Level Power Analysis
- **Target**: Infrastructure & IoT
- **Vulnerability**: Unfiltered crypto power draw visible externally
- **MITRE**: T1208 – Physical Side-Channel Monitoring
- **Impact**: Crypto process fingerprinting or information leakage
- **Tools**: Power Line Probes, High-Speed Oscilloscope, Filters
- **Scenario**: Attacker taps external building power lines to monitor device activity or infer crypto operations based on consumption patterns.
- **Attack Steps**: Step 1: Place current probes or high-frequency sensors on external or internal power lines (e.g., near a wall socket or internal PSU line). Step 2: Measure voltage/current usage across crypto devices, especially when they perform sensitive operations (e.g., key generation, decryption). Step 3: Record power patterns using an oscilloscope or data logger. Step 4: Analyze waveform for operation-specific signatures (e.g., AES spikes, RSA peaks). Step 5: If available, correlate with known input data for power analysis (DPA or SPA). Step 6: Infer crypto behavior and potentially extract timing or key characteristics. Step 7: Can be done externally in multi-tenant buildings or shared labs.
- **Detection**: Power waveform baseline deviation, electrical noise logging
- **Solution**: Use power conditioning, shielding transformers, deploy constant load circuitry
- **Tags**: Power Monitoring, Crypto Leakage, Infrastructure SCA

## Glitch Recovery via Capacitor Behavior

- **Attack Type**: Post-Fault Side-Channel
- **Target**: Smartcards, Crypto Chips
- **Vulnerability**: Power leakage through passive component behavior
- **MITRE**: T1611 – Physical Fault-Based Leakage
- **Impact**: Post-fault key leakage, memory state inference
- **Tools**: Oscilloscope, Capacitor Monitors, Logic Analyzer
- **Scenario**: After a voltage glitch or fault, capacitor discharge curves can reveal memory or register states due to delay in power recovery.
- **Attack Steps**: Step 1: Induce a fault (e.g., voltage drop or clock glitch) while crypto chip is executing sensitive tasks (e.g., decrypting data). Step 2: Immediately monitor on-board capacitors during power recovery—discharge curves may vary based on prior device activity. Step 3: Capture those analog values using a high-resolution oscilloscope. Step 4: Infer partial register or memory contents from voltage behavior (especially if capacitors aren't isolated). Step 5: Combine with known fault location to extract useful state info like keys, nonce, or flags. Step 6: Repeat to build statistical model of internal states during or after faults.
- **Detection**: Capacitor voltage monitoring, real-time fault diagnostics
- **Solution**: Add discharge diodes; isolate memory power domains; zeroize registers after fault
- **Tags**: Fault Injection, Capacitor Leakage, Power Behavior

## Supply Chain Leak via Embedded Power Monitors

- **Attack Type**: Hardware Trojan via Power Sensors
- **Target**: Hardware Devices
- **Vulnerability**: Malicious embedded components in power paths
- **MITRE**: T1584 – Hardware Implant
- **Impact**: Persistent crypto info exfiltration, hardware espionage
- **Tools**: Custom Hardware Trojans, RF Modules, Micro Sensors
- **Scenario**: Adversary installs hidden current sensors inside devices during manufacture to later exfiltrate crypto usage info via side-channels.
- **Attack Steps**: Step 1: Attacker (e.g., rogue employee or vendor) embeds a tiny current sensor or microcontroller in the device PCB during manufacturing. Step 2: The embedded sensor monitors power usage during cryptographic operations. Step 3: Data is stored locally or transmitted via RF/bluetooth/USB backdoors. Step 4: Later, attacker retrieves logged crypto usage—timings, frequency, or even inferred secrets. Step 5: With enough data, attacker performs offline SPA/DPA or reconstructs sensitive keys. Step 6: Detection is hard unless full hardware audit or RF/thermal scans are done. Step 7: Attack persists across firmware updates since it is hardware-based.
- **Detection**: Supply chain audit, thermal scan, RF emission monitoring
- **Solution**: Vet suppliers; implement tamper detection; conduct hardware inspections and EM scanning
- **Tags**: Supply Chain Attack, Hardware Implant, Crypto Leak

## Smartcard DPA Attack

- **Attack Type**: Differential Power Analysis
- **Target**: Smartcards
- **Vulnerability**: Consistent power trace during key use
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Private key or PIN leakage via power variations
- **Tools**: Oscilloscope, Smartcard Reader, ChipWhisperer
- **Scenario**: During PIN verification or crypto routines, smartcards show consistent power patterns that leak key material.
- **Attack Steps**: Step 1: Connect smartcard to a reader and send repeated cryptographic requests (e.g., signing or decryption). Step 2: Measure power usage with a precise oscilloscope during each operation. Step 3: Collect hundreds to thousands of traces. Step 4: Use statistical analysis (e.g., correlation) across the traces to detect power-dependent patterns. Step 5: Identify key bits from different stages of the computation. Step 6: Reconstruct full key with high confidence from the patterns. Step 7: Verify the key by repeating known crypto operations.
- **Detection**: Hardware probes, trace pattern anomaly logging
- **Solution**: Add power masking, randomize computations, reduce instruction determinism
- **Tags**: DPA, Smartcard Hacking, Power Side Channel

## TPM Module Power Timing

- **Attack Type**: Timing + Power Analysis
- **Target**: TPM Chips (TPM 1.2/2.0)
- **Vulnerability**: Observable timing/power variance
- **MITRE**: T1208 – Timing/Power SCA
- **Impact**: Step-level timing of internal crypto actions
- **Tools**: Logic Analyzer, Oscilloscope, TPM Access Script
- **Scenario**: Trusted Platform Modules (TPMs) exhibit measurable delays and power spikes during signing/encryption, leaking processing steps.
- **Attack Steps**: Step 1: Access the TPM via trusted software (e.g., TPM tools in Linux). Step 2: Send a request to sign or encrypt data. Step 3: Record power usage across the TPM pins during crypto operation. Step 4: Identify timing windows that correspond to internal steps (e.g., hashing, modular exponentiation). Step 5: If high-resolution power timing is possible, apply DPA or SPA to infer the used key parts. Step 6: Optionally repeat with slight variations in input to create comparative patterns.
- **Detection**: TPM timing logs, power monitor hardware attached
- **Solution**: Use constant-time cryptographic routines, noise generators
- **Tags**: TPM, Hardware Crypto, Timing Leak

## Crypto Wallet Power Analysis

- **Attack Type**: Power Side Channel
- **Target**: Hardware Wallets
- **Vulnerability**: Predictable power usage on USB or VCC
- **MITRE**: T1208 – Power Consumption
- **Impact**: Leakage of seed phrases, PINs, recovery words
- **Tools**: ChipWhisperer, USB Power Logger, FPGA
- **Scenario**: Hardware crypto wallets (Ledger, Trezor) may leak seed phrases or PINs due to consistent power usage when handling secrets.
- **Attack Steps**: Step 1: Connect the wallet to a host device (USB). Step 2: Begin wallet operations such as entering PIN or confirming transactions. Step 3: Record the power draw or USB current over time. Step 4: Collect multiple samples during key operations. Step 5: Analyze using DPA or template matching to isolate fixed sequences (like seed phrase decryption or PIN validation). Step 6: Infer key content, PIN or seed. Step 7: Use recovered secrets to clone or tamper with wallet.
- **Detection**: Power consumption logging, USB current profiling
- **Solution**: Add dummy power cycles, instruction masking, tamper-resistance
- **Tags**: Hardware Wallets, Seed Recovery, SCA

## IoT Device Crypto Leak

- **Attack Type**: Side Channel (Power/Timing)
- **Target**: IoT Devices (Smart bulbs, Cameras, etc.)
- **Vulnerability**: Minimal crypto shielding & fixed timing
- **MITRE**: T1208 – Embedded Crypto Analysis
- **Impact**: Key recovery, device spoofing, secure channel bypass
- **Tools**: Power Profiler, Logic Analyzer, Oscilloscope
- **Scenario**: Lightweight crypto chips in IoT devices often lack protection, leaking info through power and timing during operations (e.g., authentication).
- **Attack Steps**: Step 1: Identify crypto routines used by the IoT device (e.g., WPA2, TLS handshake, device pairing). Step 2: Place current sensor near power supply or VCC rail. Step 3: Interact with the device while it performs crypto routines. Step 4: Capture the power or timing differences between operations. Step 5: Use simple power analysis (SPA) or template matching to extract key bits or compare outputs. Step 6: Combine with replay or fault attack for full control. Step 7: Use findings for device impersonation or secure channel compromise.
- **Detection**: In-line current probe, side-channel trace collection
- **Solution**: Encrypt outside MCU, use noise-resistance chips, enforce constant power draw
- **Tags**: IoT, Power Attack, Smart Device Hacking

## FPGA-Based Crypto SCA

- **Attack Type**: Power Side Channel Analysis
- **Target**: FPGAs (e.g., Xilinx Spartan)
- **Vulnerability**: Bit-level data-dependent power draw
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full AES key or crypto primitive leakage
- **Tools**: Oscilloscope, ChipWhisperer, FPGA Board
- **Scenario**: FPGAs used for crypto (e.g., AES cores) leak data via measurable power usage during bit-level computation.
- **Attack Steps**: Step 1: Program an FPGA (e.g., Xilinx, Intel) with a known AES core or crypto design. Step 2: Feed input plaintexts repeatedly while monitoring the power trace across the FPGA’s VCC or shunt resistor. Step 3: Collect hundreds/thousands of power traces. Step 4: Apply CPA or DPA to the collected traces using ChipWhisperer or custom scripts. Step 5: Identify subkey bytes from correlation peaks. Step 6: Reconstruct full AES key.
- **Detection**: High-resolution oscilloscope, correlation noise check
- **Solution**: Use dual-rail logic, randomized scheduling, place crypto outside programmable fabric
- **Tags**: FPGA, AES, Side-Channel, SCA

## ChipWhisperer CPA Demo

- **Attack Type**: Correlation Power Analysis
- **Target**: Embedded Devices, Lab FPGA boards
- **Vulnerability**: Standard AES implementation on dev boards
- **MITRE**: T1208 – Lab Power Attack
- **Impact**: Teaching, key recovery in under 500 traces
- **Tools**: ChipWhisperer, Jupyter Notebook
- **Scenario**: Use the ChipWhisperer platform to perform a lab-grade AES-128 CPA attack for learning and testing side-channel resilience.
- **Attack Steps**: Step 1: Set up the ChipWhisperer hardware (CW Nano/Pro). Step 2: Program the target board (e.g., STM32 or CW-lite) to perform AES encryption on fixed/random plaintexts. Step 3: Use the provided Jupyter tutorials to collect traces. Step 4: Run CPA scripts on collected traces. Step 5: View correlation peaks to identify correct subkey values. Step 6: Verify by re-encrypting using recovered keys.
- **Detection**: Trace visualization, correlation logging
- **Solution**: Masking AES operations, using delay slots or hiding techniques
- **Tags**: CPA, AES, ChipWhisperer, Training

## Riscure Inspector Template Attack

- **Attack Type**: Template-Based Power Analysis
- **Target**: Smartcards, HSMs, Terminals
- **Vulnerability**: Reusable power/EM trace templates
- **MITRE**: T1208 – Template Power Attack
- **Impact**: Ultra-fast key extraction with minimal traces
- **Tools**: Riscure Inspector, EM probes
- **Scenario**: Use Riscure’s commercial side-channel suite to build templates of known crypto routines and match observed behavior to extract secrets.
- **Attack Steps**: Step 1: Use a trusted device to build power templates of known operations (e.g., AES SubBytes, RSA Exponentiation). Step 2: Collect side-channel traces from a real target (e.g., payment terminal). Step 3: Use Inspector’s correlation tools to match templates with live trace data. Step 4: Infer key material by locating the best match in the template space. Step 5: Confirm key recovery with crypto validation.
- **Detection**: EM leakage visualization, template match scoring
- **Solution**: Randomized instruction flow, template obfuscation, trace noise injection
- **Tags**: Commercial Tools, Template Attack, HSMs

## Oscilloscope + Matched Filter

- **Attack Type**: Signal Processing Power Attack
- **Target**: IoT Chips, Smartcards
- **Vulnerability**: Repeatable trace shapes per crypto step
- **MITRE**: T1208 – Filtered Signal SCA
- **Impact**: Precise identification of key-related events
- **Tools**: Oscilloscope, Matched Filter Algorithms
- **Scenario**: Use matched filters with oscilloscope-acquired power traces to isolate specific crypto events (e.g., key XOR, S-box access).
- **Attack Steps**: Step 1: Use an oscilloscope to capture precise power traces from a crypto-capable device. Step 2: Design a matched filter that matches expected signal (e.g., S-box computation peak). Step 3: Apply the filter to locate those operations in longer traces. Step 4: Isolate patterns per key byte. Step 5: Compare signal response per key hypothesis and recover the best match. Step 6: Reconstruct full key using multi-step analysis.
- **Detection**: Oscilloscope trace matching, anomaly detection
- **Solution**: Add dummy operations, dynamic instruction ordering
- **Tags**: Oscilloscope, Matched Filter, S-box Analysis

## OpenADC-based SPA/DPA

- **Attack Type**: Power Side-Channel Analysis
- **Target**: Embedded Devices
- **Vulnerability**: No power masking or countermeasures
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Secret key leakage from cryptographic operations
- **Tools**: OpenADC, STM32 Board, Python, USB Scope
- **Scenario**: OpenADC (Open-source Analog-to-Digital Converter) is used with a microcontroller to build an affordable side-channel rig to capture power traces and perform SPA/DPA attacks.
- **Attack Steps**: Step 1: Set up an OpenADC-based board with a target microcontroller (e.g., STM32, ATmega) that performs AES encryption. Step 2: Connect the ADC across the shunt resistor (on the Vcc line) to measure real-time power consumption. Step 3: Upload a program to the target microcontroller that encrypts a block of plaintext (same or random). Step 4: Capture power traces using the ADC during each encryption operation. Step 5: Export the traces to a PC and analyze them using Python scripts. Step 6: For SPA, visually inspect waveforms to identify S-Box or XOR operations. Step 7: For DPA, collect many traces and compute differential power consumption over time. Step 8: Correlate guessed key bits with observed power changes. Step 9: Repeat until the full key is recovered.
- **Detection**: Unusual power fluctuations; correlation analysis
- **Solution**: Use constant-time algorithms; apply power balancing or masking techniques
- **Tags**: OpenADC, SPA, DPA, Microcontroller, SCA

## PowerSpy Mobile App Exploit

- **Attack Type**: Mobile Power Side-Channel
- **Target**: Android Devices
- **Vulnerability**: App-level access to detailed power stats
- **MITRE**: T1602 – Data from Local System
- **Impact**: Behavioral profiling; inference of app usage
- **Tools**: PowerSpy, Android Debug Bridge (ADB)
- **Scenario**: PowerSpy uses mobile device battery consumption data (CPU usage stats) to infer running apps or user activity, leaking sensitive behavior patterns.
- **Attack Steps**: Step 1: Attacker develops or installs a malicious app on the victim’s Android device that requests access to battery stats (a common permission that doesn’t raise suspicion). Step 2: The app records detailed power consumption data (e.g., CPU frequency, battery drain over time) while the device is being used. Step 3: Using PowerSpy techniques, the attacker processes the battery usage logs to identify patterns that correspond to specific app usage (e.g., banking apps, messaging apps). Step 4: For crypto apps (e.g., wallets, secure messengers), the app detects when cryptographic functions are being executed due to a spike in CPU usage. Step 5: The attacker correlates usage times with external observations or user behavior (e.g., password entry times) to mount timing or behavioral attacks. Step 6: Data is exfiltrated to the attacker’s server for aggregation and deeper analysis.
- **Detection**: Power usage logging; behavioral anomaly detection
- **Solution**: Limit access to power stats; sandbox sensitive apps; enforce fine-grained permissions
- **Tags**: Android, PowerSpy, Side-Channel, Mobile

## AES SubBytes DPA Attack

- **Attack Type**: Differential Power Analysis
- **Target**: Embedded AES Devices
- **Vulnerability**: S-box access reveals intermediate values
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full AES key recovery
- **Tools**: ChipWhisperer, OpenADC, Python Scripts
- **Scenario**: Exploit power consumption differences during the AES SubBytes step to recover secret key bits.
- **Attack Steps**: Step 1: Set up a side-channel analysis lab using a development board (e.g., STM32) running AES encryption and a power measurement tool like ChipWhisperer or OpenADC. Step 2: Feed multiple known plaintext inputs to the AES encryption function on the device. Step 3: Capture corresponding power traces during each encryption operation. Focus on capturing the part of the trace where the SubBytes operation (S-box lookup) occurs. Step 4: Hypothesize possible key byte values and predict expected power consumption using the Hamming weight model of the S-box output. Step 5: Perform correlation analysis between predicted power consumption and the actual traces. Step 6: Identify the key byte with the highest correlation. Step 7: Repeat for all 16 bytes to reconstruct the full AES key. Step 8: Confirm key by testing decryption.
- **Detection**: Monitor for correlation anomalies in power traces; check for lab setups
- **Solution**: Apply masking on S-box output; randomize execution order; use constant power implementations
- **Tags**: AES, SCA, DPA, SubBytes, Side-Channel

## DES S-Box DPA Attack

- **Attack Type**: Differential Power Analysis
- **Target**: Smartcards, FPGA
- **Vulnerability**: Unprotected S-box DPA leakage
- **MITRE**: T1208 – Power Side Channels
- **Impact**: DES key recovery via power analysis
- **Tools**: Oscilloscope, FPGA, DES FPGA Core
- **Scenario**: Recover secret DES key bits by targeting the power variations during S-box substitution and expansion permutations.
- **Attack Steps**: Step 1: Use a FPGA or microcontroller-based device running DES encryption. Ensure you have access to input plaintexts and can trigger DES operations. Step 2: Capture multiple power traces of DES encryptions using known plaintexts. Use a high-speed oscilloscope or power side-channel setup. Step 3: Isolate power consumption related to the first round’s S-box operations (where key mixing and substitutions happen). Step 4: Make guesses about the input bits of each S-box using possible key subvalues. Step 5: Predict intermediate values (e.g., S-box output bits) and correlate with measured power traces using DPA techniques. Step 6: Recover subkey bits one S-box at a time. Step 7: Reconstruct full DES key by combining subkeys from each round. Step 8: Test decryption using recovered key.
- **Detection**: Detect high-frequency spikes during S-box ops
- **Solution**: Use masking, pipelining, and power balancing countermeasures
- **Tags**: DES, Side-Channel, S-box, Differential

## RSA Square-Multiply DPA

- **Attack Type**: RSA Power Side-Channel Attack
- **Target**: Smartcards, Embedded
- **Vulnerability**: Unprotected square-multiply algorithm
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full RSA key extraction
- **Tools**: Oscilloscope, ChipWhisperer, Python
- **Scenario**: Exploit the power pattern difference between square and multiply operations during modular exponentiation to extract RSA private exponent.
- **Attack Steps**: Step 1: Use a device that performs RSA decryption or signing using the square-and-multiply algorithm (commonly found in smartcards, HSMs, or embedded systems). Step 2: Trigger RSA operations with known ciphertexts or messages. Step 3: Capture power traces during exponentiation steps using a high-resolution oscilloscope or ChipWhisperer. Step 4: Observe the power waveform and identify repeating patterns corresponding to square and multiply operations. Multiply operations typically consume more power. Step 5: Translate the operation sequence (square-only vs. square+multiply) into bits of the private key (e.g., multiply = 1, square = 0). Step 6: Reconstruct the private exponent bit-by-bit by mapping these power patterns. Step 7: Test recovered private key by decrypting a known message or signing.
- **Detection**: Monitor for unusual power trace signatures
- **Solution**: Use constant-time modular exponentiation (Montgomery Ladder), apply blinding
- **Tags**: RSA, DPA, Square-and-Multiply, SCA

## ECC Scalar DPA Attack

- **Attack Type**: ECC Side-Channel Key Recovery
- **Target**: Crypto Wallets, ECC Chips
- **Vulnerability**: Power reveals scalar multiplication patterns
- **MITRE**: T1208 – Power Side Channels
- **Impact**: ECC private key disclosure
- **Tools**: ChipWhisperer, Oscilloscope, Python
- **Scenario**: Recover private ECC scalar (d) by analyzing power consumption during elliptic curve point multiplication (e.g., d·G).
- **Attack Steps**: Step 1: Use a device (e.g., crypto wallet, embedded secure chip) performing ECC scalar multiplication operations for digital signatures or key exchange. Step 2: Trigger multiple scalar multiplications with controlled public base point (G). Step 3: Use ChipWhisperer or a high-res oscilloscope to measure power traces during scalar multiplication. Step 4: Identify patterns that reflect whether the point addition (conditional on scalar bit = 1) was executed. Step 5: Record when only point doubling occurs (scalar bit = 0) and when both doubling and addition occur (scalar bit = 1). Step 6: Reconstruct scalar bit-by-bit using the observed sequence. Step 7: Repeat to obtain full private scalar d. Step 8: Test by regenerating public key (d·G) and matching with known one.
- **Detection**: Watchpoint analysis; secure scalar mult instrumentation
- **Solution**: Use constant-time point multiplication; scalar blinding; curve randomization
- **Tags**: ECC, Scalar Mult, DPA, Side-Channel

## DSA/ECDSA DPA on Nonce

- **Attack Type**: Differential Power Analysis (DPA)
- **Target**: Crypto wallets, Smartcards
- **Vulnerability**: Power side-channel leaking nonce k
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Private key recovery from leaked signing nonce
- **Tools**: ChipWhisperer, Python, Oscilloscope
- **Scenario**: Attacker recovers DSA/ECDSA signing nonce k using power analysis, then calculates the private key using leaked nonce and signature values.
- **Attack Steps**: Step 1: Choose a device (e.g., smartcard, crypto wallet, embedded chip) performing DSA/ECDSA digital signatures. Step 2: Trigger signing operations multiple times using known messages. Step 3: Measure power consumption during signing, focusing on when nonce k is used in the scalar multiplication or hash computation. Step 4: Correlate power variations to leaked bits of nonce k using statistical DPA methods (e.g., correlation or template attacks). Step 5: Once partial bits of k are recovered, use known signature components (r, s) to compute the private key using: d = ((s * k) - H(m)) / r mod n. Step 6: Verify the private key by signing and matching output. Step 7: Repeat across messages if needed to improve precision.
- **Detection**: Look for consistent k reuse, trace anomalies
- **Solution**: Use deterministic signing (RFC 6979), nonce blinding, or randomized scalar ops
- **Tags**: DSA, ECDSA, SCA, Nonce Leak, Side-Channel

## First-Order DPA

- **Attack Type**: Statistical DPA
- **Target**: Embedded AES chips
- **Vulnerability**: Direct leakage of intermediate values
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full key extraction via statistical correlation
- **Tools**: Python, NumPy, ChipWhisperer
- **Scenario**: Basic form of DPA that correlates raw power traces with predicted intermediate values (e.g., result of an S-box operation).
- **Attack Steps**: Step 1: Set up a device that performs cryptographic operations (e.g., AES). Step 2: Feed known plaintexts into the encryption function. Step 3: Capture power traces using an oscilloscope or ChipWhisperer. Step 4: Predict an intermediate value (e.g., S-box output byte) based on guessed key byte. Step 5: Calculate hypothetical power values using a leakage model like Hamming weight. Step 6: Compute Pearson correlation between predicted and measured power at each time sample. Step 7: Identify the time and key byte with highest correlation, which reveals correct guess. Step 8: Repeat for all key bytes.
- **Detection**: Monitor correlation between ops & power traces
- **Solution**: Masking, balancing, randomization of operations
- **Tags**: DPA, AES, Side-Channel, First Order

## Second-Order DPA

- **Attack Type**: Advanced Differential Power Analysis
- **Target**: Masked AES chips, Smartcards
- **Vulnerability**: Leakage bypassing first-order protections
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Key extraction on masked crypto implementations
- **Tools**: ChipWhisperer, NumPy, Custom Python Scripts
- **Scenario**: Attack devices protected by masking countermeasures by combining two or more power points (e.g., squaring differences) to cancel noise and extract key info.
- **Attack Steps**: Step 1: Use a device that employs first-order masking (splitting sensitive data into shares). Step 2: Capture power traces during cryptographic operation (e.g., AES, ECC). Step 3: Select two time points likely to hold power traces of masked shares. Step 4: Compute second-order leakage: square the difference or multiply the two traces. Step 5: Use statistical correlation techniques (like Pearson correlation) to match predicted leakage to measured second-order signal. Step 6: Identify time offsets with highest correlation, pointing to correct key bytes. Step 7: Iterate across more samples or rounds for full key recovery.
- **Detection**: Check for higher-order signal artifacts in trace data
- **Solution**: Use second-order masking; shuffle execution and hide access patterns
- **Tags**: Second Order, Masked Crypto, DPA

## High-Order DPA (HO-DPA)

- **Attack Type**: High-Order Power Analysis
- **Target**: Highly secured devices
- **Vulnerability**: High-order masking still reveals leakage
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Bypass high-order masking, recover full key
- **Tools**: ChipWhisperer, Riscure, Scikit-learn, Python
- **Scenario**: Combines three or more points of power consumption to break high-order masked cryptographic implementations.
- **Attack Steps**: Step 1: Identify target running high-order masked AES or ECC. Step 2: Use advanced acquisition hardware to capture ultra-precise power traces (many samples, high resolution). Step 3: Choose N+1 sample points suspected to leak individual shares. Step 4: Multiply the leakage points together (e.g., point1 × point2 × point3) to cancel mask effect. Step 5: Apply statistical analysis like multivariate correlation to detect dependency on key bits. Step 6: Iterate using known inputs and recovered shares to reconstruct full sensitive values. Step 7: Use values to recover original key. Step 8: Cross-validate against test vectors.
- **Detection**: Machine learning on side-channel data; power waveform pattern recognition
- **Solution**: High-Order DPA, Masked Crypto, Power Leakage
- **Tags**: COSADE, CHES, Riscure Labs

## Boolean Masked DPA

- **Attack Type**: High-Order DPA / Boolean Masked
- **Target**: Masked crypto chips
- **Vulnerability**: Boolean masking improperly protected
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Partial/full key recovery in masked devices
- **Tools**: ChipWhisperer, NumPy, Jupyter Notebook
- **Scenario**: Attacks cryptographic implementations that use Boolean masking (e.g., XOR-based shares) by observing and combining multiple power traces to cancel the mask.
- **Attack Steps**: Step 1: Identify target using Boolean masking (e.g., AES or ECC in embedded devices). Step 2: Collect many power traces during repeated operations on known inputs. Step 3: Apply preprocessing (mean-centering, alignment) to stabilize noisy signals. Step 4: Combine observations across time or across shares using mathematical operations (e.g., XOR combinations) to cancel the effect of the mask. Step 5: Perform correlation or mutual information analysis on combined traces. Step 6: Isolate key-dependent leakage patterns. Step 7: Extract masked key share and use multiple rounds to reconstruct full key.
- **Detection**: Higher-order analysis on multiple trace segments
- **Solution**: Use higher-order masking, randomized encoding, and leakage-resistant compilers
- **Tags**: DPA, Boolean Mask, Side-Channel, Embedded

## Correlation Power Analysis (CPA)

- **Attack Type**: CPA (Statistical Side-Channel)
- **Target**: Embedded AES/RSA systems
- **Vulnerability**: Key-dependent leakage in intermediate states
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full key extraction from measured power traces
- **Tools**: ChipWhisperer, Python (SciPy, NumPy)
- **Scenario**: Measures Pearson correlation between power trace values and hypothetical key-dependent states to recover keys from cryptographic operations.
- **Attack Steps**: Step 1: Feed known plaintext values into a target device (like AES encryption). Step 2: Capture power traces during each encryption operation. Step 3: Guess a key byte and compute an intermediate value (e.g., output of S-box). Step 4: Estimate power consumption of that intermediate value using a leakage model (e.g., Hamming weight). Step 5: Calculate Pearson correlation coefficient between actual traces and hypothetical leakage. Step 6: Find the key guess with highest correlation. Step 7: Repeat for each key byte and validate by checking decryption matches.
- **Detection**: Detect spikes in correlation during crypto operations
- **Solution**: Insert noise, mask values, randomize execution order
- **Tags**: CPA, AES, Hamming Weight, Side-Channel, Power

## Lookup Table DPA (e.g., AES T-Tables)

- **Attack Type**: Software DPA / Table Lookup
- **Target**: Software AES libraries
- **Vulnerability**: Key leaks via memory-access pattern correlation
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Key recovery from software crypto implementations
- **Tools**: ChipWhisperer, Custom C code AES
- **Scenario**: Exploits table-based implementation of cryptographic algorithms (like AES T-tables) where DPA reveals memory access patterns.
- **Attack Steps**: Step 1: Identify AES implementation using precomputed lookup tables (e.g., T-tables in OpenSSL or C code). Step 2: Feed known plaintext into encryption routine while measuring power. Step 3: Focus on traces around lookup accesses (e.g., S-box lookups in round 1). Step 4: Guess key byte and compute which table index would be accessed. Step 5: Correlate observed power with expected table access. Step 6: Detect peaks in correlation corresponding to correct key guesses. Step 7: Extract all key bytes using this method.
- **Detection**: Monitor table access patterns or variable cache use
- **Solution**: Use constant-time code, remove table lookups, use hardware AES instructions
- **Tags**: Lookup Table, AES, T-Table, Power Leak

## Key Schedule DPA (AES/RSA)

- **Attack Type**: Key Expansion DPA
- **Target**: Embedded AES / RSA chips
- **Vulnerability**: Insecure key expansion / key scheduling
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Root key exposure through key expansion leakage
- **Tools**: ChipWhisperer, ScopeView, Python
- **Scenario**: DPA attacks specifically targeting the key schedule operations of cryptographic algorithms, which are often less protected than round transformations.
- **Attack Steps**: Step 1: Identify cryptographic implementation where key schedule (AES or RSA exponentiation) is computed dynamically. Step 2: Input known plaintexts and record power traces. Step 3: Locate the section of trace where key schedule is performed (typically early in the operation). Step 4: Guess initial key bytes and calculate expected derived key states. Step 5: Apply correlation analysis between guessed state and measured power. Step 6: Recover base key by backtracking from the expanded state. Step 7: Validate by decrypting known ciphertext.
- **Detection**: Find anomalies in early trace window or pre-round patterns
- **Solution**: Harden key schedule, precompute in secure enclave, use masking
- **Tags**: AES, RSA, Key Schedule, Side-Channel, DPA

## Montgomery Ladder RSA DPA

- **Attack Type**: RSA DPA / Ladder Leak
- **Target**: RSA Hardware Modules
- **Vulnerability**: Conditional branching leaks key info
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full private RSA key recovery
- **Tools**: ChipWhisperer, Python, ScopeView
- **Scenario**: Exploits differences in power consumption during square vs multiply steps in Montgomery ladder exponentiation used in RSA implementations.
- **Attack Steps**: Step 1: Identify RSA implementation using Montgomery ladder for modular exponentiation. Step 2: Feed chosen ciphertexts and capture power traces during decryption. Step 3: Observe patterns in power trace for operations (square vs multiply). Step 4: Use statistical analysis to correlate operation type with key bit values. Step 5: Reconstruct key bit-by-bit based on ladder pattern. Step 6: Confirm recovered key by verifying decryption or signature generation.
- **Detection**: Compare timing or power signature of squaring vs multiplication
- **Solution**: Use constant-time and power-balanced ladder implementation
- **Tags**: RSA, Ladder, DPA, Montgomery, Power Leakage

## ECC Ladder DPA

- **Attack Type**: ECC Scalar Mult DPA
- **Target**: ECC Hardware Devices
- **Vulnerability**: Scalar multiplication leaks secret scalars
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full ECDSA/ECDH key compromise
- **Tools**: ChipWhisperer, OpenECC, Python
- **Scenario**: Targets elliptic curve scalar multiplication (ladder-style) to leak private scalar bits via conditional operation patterns in power traces.
- **Attack Steps**: Step 1: Target ECC crypto system using ladder for scalar multiplication (e.g., ECDSA, ECDH). Step 2: Input chosen public points and capture power traces. Step 3: Identify conditional operations in trace (e.g., add vs double). Step 4: Perform correlation analysis to map operation patterns to scalar bits. Step 5: Reconstruct private scalar bit-by-bit. Step 6: Use recovered scalar to forge signatures or compute shared secrets.
- **Detection**: Side-channel EM/power pattern recognition
- **Solution**: Use unified formulas or constant-operation scalar multiplication
- **Tags**: ECC, Ladder, Scalar DPA, Elliptic Curve

## Hybrid DPA + Timing

- **Attack Type**: Power + Timing Fusion
- **Target**: All Crypto Hardware
- **Vulnerability**: Multiple weak leakage points combined
- **MITRE**: T1208, T1210
- **Impact**: More reliable, low-noise key extraction
- **Tools**: ChipWhisperer, Oscilloscope, Python
- **Scenario**: Combines power analysis and timing side-channels for more reliable and low-noise extraction of cryptographic secrets.
- **Attack Steps**: Step 1: Identify cryptographic function with both power and timing variations (e.g., AES, RSA). Step 2: Collect power traces and precise execution timing data. Step 3: Align traces to operation phases (e.g., S-box, modular exponentiation). Step 4: Apply correlation across both domains to amplify signal. Step 5: Combine timing-based leakage (e.g., longer computation = square) with power-based leakage. Step 6: Reconstruct keys using reinforced signals.
- **Detection**: Measure both EM/power and operation duration together
- **Solution**: Harden both timing and power — not just one side channel
- **Tags**: Timing, DPA, Multi-Modal, Power-Timing Fusion

## Smartcard DPA

- **Attack Type**: Device-Specific Power Attack
- **Target**: Smartcards / SIM Cards
- **Vulnerability**: Side-channel leakage in hardware
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full key recovery or cloned smartcards
- **Tools**: ChipWhisperer, Side-Channel Oscilloscope
- **Scenario**: Targets smartcards executing cryptographic functions (e.g., RSA, ECC, DES) and extracts secrets via repeated, identical operations with power capture.
- **Attack Steps**: Step 1: Acquire smartcard with crypto functionality (e.g., signing). Step 2: Send many identical inputs (e.g., same challenge or keygen input). Step 3: Record high-resolution power traces via probe or EM coil. Step 4: Guess intermediate key state (e.g., S-box output). Step 5: Correlate expected vs real power usage. Step 6: Recover full key by repeating this for all bytes. Step 7: Clone or use key for spoofing authentication.
- **Detection**: Monitor card during operation using probes or EM analyzers
- **Solution**: Use certified tamper-resistant smartcards with shielding
- **Tags**: DPA, Smartcard, SIM, Authentication Bypass

## TPM Chip DPA

- **Attack Type**: Differential Power Analysis
- **Target**: TPM Security Chips
- **Vulnerability**: Lack of masking / unbalanced power use
- **MITRE**: T1208 – Power Side Channels
- **Impact**: TPM attestation or key compromise
- **Tools**: Oscilloscope, ChipWhisperer, TPM toolkit
- **Scenario**: Analyze Trusted Platform Module (TPM) operations (e.g., signing, decryption) via power usage to recover keys.
- **Attack Steps**: Step 1: Trigger TPM signing (e.g., signing an OS boot hash). Step 2: Capture multiple power traces during identical operations. Step 3: Align traces with expected crypto stages (e.g., modular exponentiation). Step 4: Apply statistical DPA to recover secret signing key. Step 5: Validate key by forging a valid TPM-signed message.
- **Detection**: Monitor power traces during repeatable crypto operations
- **Solution**: Use constant-power TPM firmware + physical countermeasures
- **Tags**: TPM, Signing, Boot, DPA, Attestation

## Hardware Wallet DPA

- **Attack Type**: Differential Power Analysis
- **Target**: Hardware Wallet Devices
- **Vulnerability**: EM/power leakage from crypto ops
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full seed extraction, account takeover
- **Tools**: Oscilloscope, ChipWhisperer, Ledger Live
- **Scenario**: Attack Ledger, Trezor, or similar wallets to extract mnemonic seed or private keys during transaction signing.
- **Attack Steps**: Step 1: Connect wallet and trigger transaction signing repeatedly. Step 2: Record high-precision power traces during signing. Step 3: Target known crypto algorithm (e.g., ECDSA) and guess intermediate values. Step 4: Apply DPA to recover scalar or private key. Step 5: Use key to derive wallet mnemonic (BIP-39) or seed.
- **Detection**: Power analysis correlation during signature operations
- **Solution**: Use secure chip designs and power noise obfuscation techniques
- **Tags**: Wallet, Mnemonic, BIP-39, Private Key, DPA

## IoT Crypto Module DPA

- **Attack Type**: Differential Power Analysis
- **Target**: IoT Devices / MCU Boards
- **Vulnerability**: Power trace correlation reveals key bits
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Key extraction, firmware tampering
- **Tools**: Oscilloscope, Saleae Logic, STM32 debugger
- **Scenario**: Attack IoT modules with AES or ECC functions via side-channel leaks on low-power MCUs.
- **Attack Steps**: Step 1: Identify crypto operation endpoint (e.g., over UART/SPI). Step 2: Send crafted plaintext and capture power trace from chip. Step 3: Guess key bytes or intermediate values (e.g., AES S-box). Step 4: Apply DPA with hundreds of traces to find correlation. Step 5: Recover encryption key. Step 6: Reuse key to decrypt messages or inject malicious firmware.
- **Detection**: Power trace analysis with known input/output pairs
- **Solution**: Add randomized delays, power line filters, or AES masking
- **Tags**: IoT, STM32, AES, Crypto Module, Smart Sensor

## Bluetooth/WiFi Stack DPA

- **Attack Type**: Wireless Crypto DPA
- **Target**: Wireless SoCs / Modules
- **Vulnerability**: Wireless AES power leakage during ops
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Eavesdropping or MITM of wireless sessions
- **Tools**: ChipWhisperer, SDR, Wireshark, BLE toolkits
- **Scenario**: DPA attack on AES-based encryption used in Bluetooth LE pairing or WPA2 handshake within wireless chipsets.
- **Attack Steps**: Step 1: Trigger repeated encryption (e.g., pairing or handshake). Step 2: Collect EM/power traces using near-field probe or scope. Step 3: Guess intermediate AES rounds (e.g., round keys). Step 4: Correlate with power patterns using CPA or DPA. Step 5: Recover link key or session key. Step 6: Use key to eavesdrop or inject traffic.
- **Detection**: EM probing during AES handshake inside chip
- **Solution**: Harden firmware + add shielding to BT/WiFi modules
- **Tags**: Bluetooth, WPA2, AES, Wireless DPA

## EM + DPA

- **Attack Type**: Electromagnetic DPA
- **Target**: Smartcards, FPGAs, IoT chips
- **Vulnerability**: Radiated EM signals correlate with power use
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Key extraction from external distance
- **Tools**: EM probe, Oscilloscope, Faraday enclosure
- **Scenario**: Combine EM radiation with Differential Power Analysis to capture power leakage without physical contact.
- **Attack Steps**: Step 1: Place EM probe near crypto device (e.g., smartcard, MCU). Step 2: Trigger encryption (e.g., AES) multiple times with known plaintexts. Step 3: Record EM traces corresponding to power fluctuation. Step 4: Apply CPA/DPA to identify key-correlated leakage. Step 5: Recover encryption key or internal state.
- **Detection**: Unusual EM activity near chip
- **Solution**: Shielding, spread-spectrum clocking, and balanced load design
- **Tags**: EM Leak, Power, Smartcard, DPA

## USB Power Line DPA

- **Attack Type**: Remote Power DPA
- **Target**: Laptops, Embedded Devices
- **Vulnerability**: Power drawn during crypto leaks patterns
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Leakage of keys from power-over-USB
- **Tools**: USB analyzer, Oscilloscope, Logic Analyzer
- **Scenario**: Leak cryptographic operations via power fluctuations observable on USB charging or data lines.
- **Attack Steps**: Step 1: Connect target device via USB to controlled power source. Step 2: Start encryption (e.g., TLS handshake, AES-ECB). Step 3: Monitor current draw patterns with high-speed USB power logger. Step 4: Extract power trace and apply CPA/DPA. Step 5: Correlate with guessed plaintext to recover AES keys.
- **Detection**: Logging USB power line activity
- **Solution**: Use hardware with constant power draw or power noise insertion
- **Tags**: USB, DPA, AES, Remote Leak, IoT

## Remote DPA over Power Profiling

- **Attack Type**: Remote / Passive DPA
- **Target**: IoT, Industrial Controllers
- **Vulnerability**: Power profiling over air reveals computation
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Key recovery, algorithm fingerprinting
- **Tools**: RF probes, Remote EM sensors, SDR
- **Scenario**: Monitor power usage from a distance (e.g., via RF sensors, EMI pickup) to infer cryptographic operations.
- **Attack Steps**: Step 1: Identify device power frequency band using SDR or oscilloscope. Step 2: Capture power signature remotely during crypto operation. Step 3: Align and clean traces using filters and FFT. Step 4: Run CPA/DPA on suspected blocks of power usage. Step 5: Infer key bits through correlation.
- **Detection**: Remote EM sniffing / RF monitoring
- **Solution**: Use EMI shielding and detect ambient eavesdropping
- **Tags**: Remote DPA, Industrial IoT, RF

## Capacitor Residual Charge DPA

- **Attack Type**: Physical Power Remanence DPA
- **Target**: Embedded Boards, Smartcards
- **Vulnerability**: Voltage residue retains bit-level info post-op
- **MITRE**: T1602 – Data Remanence
- **Impact**: AES key recovery or memory state reconstruction
- **Tools**: Oscilloscope, Discharge probes, Logic analyzers
- **Scenario**: Analyze leftover voltage on capacitors post-encryption to recover what operations were performed.
- **Attack Steps**: Step 1: Power off the crypto device after key operation. Step 2: Use probes to read voltage levels of capacitors or RAM lines. Step 3: Analyze which lines held ‘high’ or ‘low’ charge (binary guess). Step 4: Reconstruct parts of AES rounds or key schedule. Step 5: Use findings to shorten keyspace or verify correct guesses.
- **Detection**: Post-shutdown capacitor charge probing
- **Solution**: Clear sensitive memory/caps before shutdown; add decay resistors
- **Tags**: Residual Power, Side-Channel, Remanence

## Glitch-Triggered DPA

- **Attack Type**: Voltage Glitch + Power Analysis
- **Target**: Embedded systems, MCUs
- **Vulnerability**: Glitch alters state, improves leakage
- **MITRE**: T1208 + T1602
- **Impact**: Faster key recovery, bypass secure processing
- **Tools**: ChipWhisperer, Crowbar, Oscilloscope
- **Scenario**: Use induced glitches to desynchronize or amplify leakages for better DPA precision.
- **Attack Steps**: Step 1: Inject voltage glitch (short spike/drop) during encryption (e.g., AES). Step 2: Collect power trace during the corrupted computation. Step 3: Use DPA/CPA to correlate altered trace with key guesses. Step 4: Identify successful glitch windows that increase SNR (signal-to-noise). Step 5: Extract key or S-box values more easily due to instability.
- **Detection**: Voltage fluctuation patterns
- **Solution**: Use voltage regulators, watchdogs, redundant computation
- **Tags**: Glitch, DPA, AES, Embedded

## ChipWhisperer CPA Lab Attack

- **Attack Type**: CPA Lab-Based
- **Target**: Educational boards (CW-Lite)
- **Vulnerability**: Power usage correlates with Hamming weight
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Full AES key recovery in controlled lab
- **Tools**: ChipWhisperer, PC, Python/Jupyter
- **Scenario**: Use ChipWhisperer to perform CPA on AES with known plaintexts.
- **Attack Steps**: Step 1: Flash AES encryption firmware on target (e.g., CW-Lite). Step 2: Send 200+ known plaintexts and collect power traces. Step 3: Run CPA script in Python using HW traces. Step 4: Identify correlation peaks that match key guesses. Step 5: Recover full AES-128 key in minutes.
- **Detection**: Power trace correlation plots
- **Solution**: Instruction-level masking, random delay insertion
- **Tags**: ChipWhisperer, Lab, AES, CPA

## Oscilloscope-Based DPA

- **Attack Type**: Manual Oscilloscope DPA
- **Target**: Smartcards, secure MCUs
- **Vulnerability**: Manual waveform leakage from crypto functions
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Key leakage through analog observation
- **Tools**: Tektronix/Keysight Scope, Target board
- **Scenario**: Capture power traces manually using a high-speed oscilloscope for DPA.
- **Attack Steps**: Step 1: Connect oscilloscope probes to power line (shunt resistor) of crypto chip. Step 2: Trigger scope on encryption start (via GPIO). Step 3: Send multiple known plaintexts to device. Step 4: Record power waveforms and export as CSV. Step 5: Process traces in Python/Matlab to correlate activity with AES key bytes.
- **Detection**: Oscilloscope waveform inspection
- **Solution**: Shielded board design, constant power draw
- **Tags**: Manual DPA, Oscilloscope, AES, Embedded

## Matlab/Python DPA Simulation

- **Attack Type**: Simulated DPA
- **Target**: Educational / research use
- **Vulnerability**: Synthetic trace reveals model-leakage relationship
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Training in side-channel theory & key extraction
- **Tools**: Python (Numpy, Scipy), Matlab, Jupyter
- **Scenario**: Perform simulated power analysis using virtual AES traces and correlation in Python/Matlab.
- **Attack Steps**: Step 1: Simulate AES encryption using known keys and plaintexts. Step 2: Generate synthetic power traces using Hamming weight model. Step 3: Add noise to mimic real-world side-channels. Step 4: Perform correlation analysis (CPA) on traces. Step 5: Visualize and extract key based on correlation peaks.
- **Detection**: N/A (simulation-based)
- **Solution**: Not applicable in real targets but useful for training
- **Tags**: DPA, Simulation, Python, Matlab, CPA

## DPA Contest Targets (DPAC)

- **Attack Type**: Public DPA Challenge
- **Target**: Academic/test devices
- **Vulnerability**: Known AES implementations with measurable leakage
- **MITRE**: T1208 – Power Side Channels
- **Impact**: Validate DPA skills & tools
- **Tools**: DPAC AES Boards, ChipWhisperer, Python
- **Scenario**: Run power analysis on standardized AES targets with known leakage profiles for benchmarking or training.
- **Attack Steps**: Step 1: Get official DPAC boards (or emulate). Step 2: Capture traces of AES with known key + known plaintext. Step 3: Analyze using CPA/DPA in Python. Step 4: Compare success metrics with official benchmarks. Step 5: Repeat with varying trace numbers and noise levels.
- **Detection**: Trace comparison with known expected leakage patterns
- **Solution**: Improve algorithm or countermeasure efficiency tracking
- **Tags**: AES, DPAC, Benchmark, Research

## Side-Channel Attack Frameworks

- **Attack Type**: Toolkits & Commercial Frameworks
- **Target**: Embedded, smartcards, FPGAs
- **Vulnerability**: Observable data-dependent power/caching behavior
- **MITRE**: T1602 – Hardware Side Channels
- **Impact**: Commercial-strength automated crypto auditing
- **Tools**: Riscure Inspector, SCARED, ChipWhisperer Studio
- **Scenario**: Use powerful suites like Riscure Inspector, SCARED, or ChipWhisperer Studio to automate and scale SCA/DPA testing.
- **Attack Steps**: Step 1: Configure test case (e.g., AES or RSA on target device). Step 2: Collect traces using automated capture. Step 3: Define leakage model (Hamming weight, distance, etc.). Step 4: Use GUI or scripting to run DPA/CPA. Step 5: Visualize leak points, extract keys, generate reports.
- **Detection**: Internal trace models, visual leakage mapping
- **Solution**: Use certified hardened devices, masking, noise injection
- **Tags**: SCA, DPA, Toolkits, Auditor, Riscure

## Voltage Glitching to Bypass Authentication in Secure Devices

- **Attack Type**: Fault Injection via Voltage Glitching (Hardware)
- **Target**: Embedded Devices, Secure ICs
- **Vulnerability**: Timing-sensitive hardware fault injection
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Bypass cryptographic authentication, access locked firmware
- **Tools**: ChipWhisperer, Smartcard Reader, Oscilloscope, Target Microcontroller (e.g., STM32), Glitch Amplifier, UART Sniffer
- **Scenario**: Voltage glitching is used to momentarily destabilize the power supply of a secure microcontroller (e.g., smartcard, IoT chip, TPM) to skip over authentication or password checks.
- **Attack Steps**: Step 1: Purchase or set up a voltage glitching lab environment. Start with tools like ChipWhisperer-Lite or a custom voltage glitcher circuit using a MOSFET controlled by a microcontroller like Arduino. Step 2: Choose a target device that performs some kind of cryptographic authentication, such as a smartcard, IoT board, or even a consumer device with a boot password. Example: STM32 board that runs password protection code. Step 3: Connect the device to the ChipWhisperer or glitcher. You need to intercept its power supply lines (VCC and GND). The glitcher will inject short power disruptions. Step 4: Attach a serial console reader (like PuTTY or minicom) or UART sniffer to monitor logs from the device during boot or authentication. This lets you see what happens after the glitch. Step 5: Identify the exact timing window in which the authentication or cryptographic check happens. Use the oscilloscope or trigger pin from the device (like an LED that turns on when auth is checked) to sync the glitch pulse. Step 6: Start experimenting with glitch parameters. This includes glitch offset (how many cycles after trigger to glitch), width (how long the glitch lasts), and voltage drop amount. You automate this process using ChipWhisperer scripts or manually adjust if doing DIY. Step 7: Watch for behavior change: if the device suddenly bypasses password/auth check or outputs “Access Granted” without valid credentials, the glitch worked. You may have skipped the conditional branch or error handler. Step 8: Once you find successful glitch timing and parameters, record them. You can now repeatedly bypass security every time the device runs using the same glitch settings. Step 9: In real-world usage, attackers might combine this with memory dumping or access hidden firmware areas (e.g., bypassing secure boot to dump secrets). Step 10: For safety, ensure proper insulation, avoid power spikes that could damage components, and always test on legally owned and lab-approved hardware. NOTE: Glitching is physical-layer fault injection and requires patience and lab tuning. It is real and reproducible but depends heavily on your hardware timing and target code behavior.
- **Detection**: Monitor for abnormal voltage levels, logging failed auth bypass events
- **Solution**: Add voltage and frequency tamper detection, use glitch-hardened chips, introduce random delays in critical checks
- **Tags**: Voltage Glitching, Fault Injection, Smartcard, Embedded Hacking

## Voltage Glitching Attack

- **Attack Type**: Fault Injection via Voltage Glitching
- **Target**: Embedded Devices, Smartcards
- **Vulnerability**: Power supply manipulation
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Authentication bypass, secure boot bypass
- **Tools**: ChipWhisperer, Power Supply, Oscilloscope, Arduino, UART Sniffer
- **Scenario**: Momentarily lowering or interrupting the power supply causes the chip to misbehave, bypassing security like bootloaders, PIN checks, or secure boots.
- **Attack Steps**: Step 1: Choose a secure microcontroller or embedded device as the target (e.g., STM32). Step 2: Connect the device to a glitching platform like ChipWhisperer. Attach probes to the power supply (VCC and GND). Step 3: Identify the exact timing window where the device checks for authentication (e.g., password comparison). This can be guessed using a trigger signal (like an LED or UART message). Step 4: Configure glitch parameters: delay (when to glitch), width (how long), and voltage drop. Step 5: Begin running the attack by booting the target and injecting a power glitch during the authentication step. Step 6: Observe output through serial terminal – if the device skips password checks or outputs a debug shell, glitching succeeded. Step 7: Fine-tune glitching parameters for consistency. Step 8: Use the gained access to dump memory, read firmware, or escalate privileges.
- **Detection**: Monitor power line anomalies; voltage deviation logging
- **Solution**: Use glitch detectors, tamper detection circuits, and redundant authentication checks
- **Tags**: Voltage Glitching, Power Fault, Secure Bypass

## Clock Glitching Attack

- **Attack Type**: Fault Injection via Clock Manipulation
- **Target**: Crypto MCUs, Smartcards, Secure Boot ROMs
- **Vulnerability**: Clock line tampering
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Logic corruption, password skip, faulty encryption
- **Tools**: ChipWhisperer, External Clock Generator, Oscilloscope, Logic Analyzer
- **Scenario**: Modifying clock frequency or pulse timing causes timing errors in logic circuits, potentially bypassing checks or injecting faults into cryptographic routines.
- **Attack Steps**: Step 1: Choose a target embedded system (e.g., MCU or crypto-enabled IoT board). Step 2: Disconnect the onboard clock (or override it via debug mode) and inject your own controlled clock signal using an external clock generator or ChipWhisperer. Step 3: Use a serial console or LED to identify when security-critical operations (e.g., login, encryption) take place. Step 4: Gradually increase or decrease clock frequency, or inject malformed pulses (e.g., very short/long clock cycles) during these operations. Step 5: Observe device behavior — it may crash, skip instructions, or bypass security. Step 6: Fine-tune clock fault timing to target specific instructions (e.g., jump not taken, branch skipped). Step 7: Confirm success if you get access to protected resources or faulted cryptographic outputs. Step 8: Document your working frequency and glitch profile. Use this to repeatedly exploit the vulnerability.
- **Detection**: Monitor clock consistency; use clock jitter analysis
- **Solution**: Harden clock input pins, use watchdogs, and redundant logic paths
- **Tags**: Clock Glitch, Timing Violation, Crypto Fault

## Laser Fault Injection

- **Attack Type**: Optical Fault Injection
- **Target**: Smartcards, Secure Microcontrollers
- **Vulnerability**: Localized transistor-level interference
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Disable security logic, force faults in crypto engines
- **Tools**: IR Laser, XYZ Positioner, Chip Decapsulation Tool, Oscilloscope
- **Scenario**: Focused laser beams inject faults into transistors or flip bits in microcontrollers by physically targeting silicon layers.
- **Attack Steps**: Step 1: Decapsulate the chip package using fuming nitric acid or laser ablation to expose the silicon die. (⚠️ Dangerous – must be done in lab with proper protection.) Step 2: Place the chip under a microscope on a precise XYZ stage. Focus an infrared laser (e.g., 1064nm) on the region of interest (e.g., ALU or crypto block). Step 3: Set up the chip to perform a secure operation (e.g., check password or compute AES). Step 4: Fire the laser at precise timing (based on external trigger) during instruction execution. The laser disrupts the silicon logic or SRAM cell. Step 5: Monitor output – if the chip skips a security check or produces a faulty crypto output, the attack worked. Step 6: Iterate over chip regions to map vulnerable spots. Step 7: Repeat until stable fault model is found (e.g., always flips a register or disables a comparison).
- **Detection**: Detect decapsulation or laser tampering (e.g., photodiodes)
- **Solution**: Use laser sensors, active shields, and randomized logic placement
- **Tags**: Laser Fault, Silicon-Level Attack, Optical Injection

## Electromagnetic (EM) Fault Injection

- **Attack Type**: EM-Based Fault Injection
- **Target**: IoT Devices, Secure Chips
- **Vulnerability**: Susceptibility to electromagnetic noise
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Firmware bypass, authentication logic failure
- **Tools**: EM Pulse Injector (Riscure EMFI, DIY Coil), Power Amplifier, Probe Coil, Oscilloscope
- **Scenario**: High-frequency EM pulses induce current in chips, causing faults such as corrupted memory or altered instruction execution.
- **Attack Steps**: Step 1: Choose a device with known or suspected vulnerability (e.g., IoT chip with firmware check). Step 2: Build or buy an EM pulse injector (e.g., DIY Tesla coil probe or commercial EMFI tool). Step 3: Position the probe coil very close to the chip (within mm range) and align it to the chip's CPU or memory bus. Step 4: Use a scope to trigger EM pulses during specific operations (e.g., when signature is being checked or encryption key is being used). Step 5: Inject pulses of varying intensity and width while monitoring output via serial. Step 6: Observe the device response – if it crashes, reboots, skips checks, or leaks memory, the EM glitch worked. Step 7: Document timing, power, and coil position for repeatability. Step 8: Repeat for other operations or components (e.g., boot ROM or flash checks).
- **Detection**: EM shielding, side-channel EM monitoring
- **Solution**: Add metal shielding, randomize logic timing, use EM-tolerant layouts
- **Tags**: EM Fault Injection, Electromagnetic Glitching, IoT Hacking

## Thermal Fault Injection

- **Attack Type**: Thermal Manipulation Fault Injection
- **Target**: Low-cost Crypto Chips, EEPROMs
- **Vulnerability**: Temperature-sensitive circuit behavior
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Skipped security logic, corrupted crypto state
- **Tools**: Heat Gun, Freezer Spray, Thermal Camera, Oscilloscope, Logic Analyzer
- **Scenario**: Sudden temperature changes (hot or cold) can destabilize hardware behavior, causing miscomputations or security logic failures.
- **Attack Steps**: Step 1: Select a chip or device with known temperature sensitivity (e.g., EEPROM or low-cost MCU with crypto routines). Step 2: Expose device to normal secure operation (e.g., asking for PIN, boot process). Step 3: Use a freezer spray or heat gun to rapidly change temperature of the device or chip area while it's processing. Focus especially on crypto modules or security logic. Step 4: Observe whether authentication logic or encryption routines misbehave — this might manifest as bypassed password checks, corrupted keys, or failed firmware verification. Step 5: Use a logic analyzer or serial monitor to confirm success. Step 6: Repeat temperature changes during different operation points to find fault-prone areas. Step 7: Document specific temperatures, timing, and outcomes for repeatable attacks.
- **Detection**: Monitor device temperatures and unusual behavior patterns
- **Solution**: Use temperature sensors, thermal shutdown protections, and hardened ICs
- **Tags**: Thermal Faults, Temperature Attack, Crypto Chips

## RSA Fault Attack (Bellcore Attack)

- **Attack Type**: Fault Injection via CRT Decryption Fault
- **Target**: Smartcards, TPMs, Crypto Libraries
- **Vulnerability**: Fault during CRT optimization
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Full RSA private key extraction via single fault
- **Tools**: ChipWhisperer, Power Glitcher, Oscilloscope, Python (SageMath), Target Device using RSA-CRT
- **Scenario**: Induce fault during RSA decryption using CRT (Chinese Remainder Theorem) to obtain faulty signature. Then, use math to recover full private key using correct+faulty sigs.
- **Attack Steps**: Step 1: Identify a target device (e.g., smartcard, HSM, TPM) that uses RSA with CRT optimization (common for performance). Step 2: Connect a glitching tool like ChipWhisperer to the device’s power or clock input. Use an oscilloscope or logic trigger to monitor when RSA decryption starts. Step 3: Send a known plaintext for the device to decrypt or sign. At the right moment, inject a glitch to cause a fault only during the CRT calculation (mod p or mod q). The device should return a faulty signature S'. Step 4: Repeat the operation without a glitch to get a correct signature S. Step 5: Using S and S', apply Bellcore’s formula: compute gcd(S - S', N) where N is the RSA modulus. The result gives one of the primes (p or q), breaking RSA key. Step 6: Once p and q are recovered, compute the private exponent d using standard RSA math. You now have full access to the private key. Step 7: This attack works even on one single faulty signature. You can automate the math using SageMath or Python.
- **Detection**: Monitor for faulty RSA signatures; fault detection logic during cryptographic ops
- **Solution**: Avoid CRT optimization or implement consistency checks (e.g., check if recomposed output is correct)
- **Tags**: RSA Fault Injection, CRT, Bellcore, Private Key Recovery

## AES Key Recovery via Faulty Rounds

- **Attack Type**: Differential Fault Analysis on AES
- **Target**: AES-Enabled IoT Devices, Smartcards
- **Vulnerability**: AES S-box corruption, last round faults
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Complete AES key recovery
- **Tools**: ChipWhisperer, EMFI Tool or Glitcher, Known Plaintexts, Python Script (DFA Solver)
- **Scenario**: Inject faults during 1 or 2 AES rounds. Compare faulty vs correct ciphertexts. Use known differential analysis techniques to recover AES key step-by-step.
- **Attack Steps**: Step 1: Choose a device performing AES encryption (e.g., IoT device, secure bootloader). You must have the ability to send plaintexts and receive ciphertexts. Step 2: Set up fault injection tools (voltage glitcher, EM pulse injector, or laser). Time your glitch to affect a specific AES round (e.g., round 9 or 10 of AES-128). Step 3: Send a known plaintext and receive correct ciphertext. Then, send the same plaintext but glitch the device just before the final AES round. Step 4: Capture the faulty ciphertext. Repeat this several times to get different faulty outputs for the same input. Step 5: Use AES Differential Fault Analysis (DFA) tools like phoenixAES or a custom Python script. These tools compare correct vs faulty ciphertexts to infer key bytes. Step 6: Run the DFA algorithm; with just a few faulty ciphertexts, you can fully recover the AES key. Step 7: Validate the key by encrypting plaintexts with it and checking match. This method is real and used in practice to extract keys from smartcards and boot ROMs.
- **Detection**: Monitor for unusual output patterns; use fault-resistant AES S-boxes
- **Solution**: Use fault-tolerant AES implementations, validate encryption output consistency
- **Tags**: AES DFA, Key Extraction, EM Fault, Side-Channel

## ECC Fault Analysis

- **Attack Type**: Fault Injection on ECC Scalar Multiplication
- **Target**: ECC-Based Crypto Devices
- **Vulnerability**: Fault during scalar multiplication loop
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: ECC private key recovery, signature forgery
- **Tools**: EMFI / Voltage Glitch Tool, ECC Test Target (e.g., microcontroller with ECDSA), Python
- **Scenario**: Inject faults during elliptic curve scalar multiplication. Observe output points and apply fault equations to extract private scalar (private key).
- **Attack Steps**: Step 1: Target a device using ECC (e.g., for digital signatures or secure handshake like ECDSA or ECDH). The ECC operation involves scalar multiplication: Q = kP. Step 2: Use an EM or voltage glitch injector to disturb the scalar multiplication loop (often implemented as double-and-add). Step 3: Choose or intercept input point P, and induce a fault in one intermediate doubling or addition operation. Capture the resulting faulty output Q'. Step 4: Repeat the same operation without glitch to get correct Q. Step 5: Analyze the difference between Q and Q' using known ECC fault attack equations. This reveals bits or chunks of the secret scalar k. Step 6: Repeat multiple times, each time glitching different bits of k. Combine all recovered bits to reconstruct the full ECC private key. Step 7: Use the recovered key to forge signatures, decrypt messages, or impersonate the owner.
- **Detection**: Trace abnormal output points or failed ECC ops
- **Solution**: Implement scalar multiplication checks; constant-time and fault-resistant ECC logic
- **Tags**: ECC DFA, Scalar Fault, Curve Attack, Key Recovery

## DSA Nonce Fault Attack

- **Attack Type**: DSA Nonce Recovery via Fault Injection
- **Target**: Devices using DSA (e.g., routers)
- **Vulnerability**: Faulty nonce k during DSA signing
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Private key recovery, unauthorized signing
- **Tools**: Glitching Tool, DSA Test System, Python (SymPy/Sage), Known Signatures
- **Scenario**: DSA uses random nonce k for each signature. Faults or reuse in k reveals private key. Attack injects faults in k generation or reading.
- **Attack Steps**: Step 1: Select a system using DSA signatures (e.g., old firmware updates, embedded devices, Linux kernel modules). You need multiple signatures from the same device. Step 2: Inject a glitch into the DSA nonce generation or read step. For example, skip entropy fetching or memory update. This may cause the same or similar k values across different signatures. Step 3: Capture two signatures with same or partially faulted k. DSA signatures are tuples (r, s). Use the DSA formula s = (k⁻¹ * (H(m) + xr)) mod q. If two signatures share k, private key x can be solved algebraically. Step 4: Use Python or Sage to automate solving for x given two signatures and the hash of messages. Step 5: Once x is recovered, verify by checking future signatures or using it to sign messages yourself. Step 6: Attack success depends on forcing reused k or biased k, which can be done via timing or power faults during k generation.
- **Detection**: Analyze signature patterns for repeated r values
- **Solution**: Use deterministic DSA (RFC 6979), validate randomness sources, entropy checkers
- **Tags**: DSA Nonce Fault, Randomness Attack, Signature Forge

## DES S-box Fault Attack

- **Attack Type**: Fault Injection in S-box Lookup
- **Target**: Smartcards, Legacy Embedded Crypto Devices
- **Vulnerability**: Faulty S-box logic in DES rounds
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Partial or full DES key extraction
- **Tools**: ChipWhisperer, EM Pulse Tool, FPGA or MCU running DES, Python for analysis
- **Scenario**: A fault injected during a DES round (specifically S-box substitution) results in incorrect ciphertext. Analyzing this difference can leak key information.
- **Attack Steps**: Step 1: Set up a target system running DES encryption (e.g., an old smartcard, embedded system, or emulated DES core on FPGA/MCU). Step 2: Choose a known plaintext and observe the correct ciphertext from the device. Step 3: Use an EM pulse injector or voltage glitcher to inject a fault during a specific DES round, ideally just before or during the S-box substitution step. Step 4: Send the same plaintext again during fault injection and collect the faulty ciphertext. Step 5: Repeat this for several different plaintexts to gather a set of correct and faulty ciphertext pairs. Step 6: Analyze differences using S-box differential properties. Since DES is sensitive to S-box outputs, faults in them reveal information about specific bits of the key. Step 7: Use known differential fault analysis tools or scripts to compute potential key values based on the fault model. Step 8: Iterate through multiple S-box faults to eventually recover the full DES key. Step 9: Validate recovered key by decrypting encrypted messages or matching encryption results.
- **Detection**: Monitor logic integrity during DES rounds; verify output randomness
- **Solution**: Use modern crypto (AES), add redundancy/S-box parity checks in implementation
- **Tags**: DES Fault Injection, Crypto Key Recovery, EMFI, Legacy Crypto

## Smartcard Fault Injection

- **Attack Type**: Voltage / EM Fault Injection on Smartcards
- **Target**: SIM Cards, Payment Smartcards
- **Vulnerability**: Authentication check bypass via fault
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: PIN bypass, credential leakage, data theft
- **Tools**: Smartcard Reader, ChipWhisperer, EM Glitch Tool, Python/PyAPDU
- **Scenario**: Smartcards are vulnerable to low-level faults which allow attackers to bypass authentication, skip PIN checks, or extract stored secrets.
- **Attack Steps**: Step 1: Choose a smartcard model (SIM, payment, or access card) and connect it to a smartcard reader using USB or serial interface. Use PyAPDU tools to interact with it. Step 2: Identify a critical command like VERIFY (PIN), READ BINARY (file access), or signature generation. Step 3: Use ChipWhisperer or EM glitch injector to inject a fault (timed pulse) just as the smartcard verifies a PIN or generates a response. This can skip an authentication check or corrupt memory access. Step 4: Monitor card responses and logs—success is often shown when a normally restricted command now completes without valid auth. Step 5: Repeatedly refine glitch timing using serial response triggers or LED indicators until you achieve bypass. Step 6: Once bypass is achieved, use APDU commands to read protected files or extract key material stored in EEPROM. Step 7: Combine this with side-channel analysis for deeper key extraction. Step 8: Repeat under different PINs or authentication contexts to gain persistent access.
- **Detection**: Smartcard anomaly detection; verify retries or auth bypass patterns
- **Solution**: Add PIN retry counters, glitch-resistant validation routines, active tamper response
- **Tags**: Smartcard Hack, PIN Bypass, EM Glitch, EEPROM Dump

## TPM Fault Glitch

- **Attack Type**: TPM Fault Injection for Secure Boot Bypass
- **Target**: Trusted Platform Modules (TPMs)
- **Vulnerability**: Fault in measurement validation or sealing
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Secret leakage, secure boot bypass
- **Tools**: TPM-equipped System (e.g., laptop), Logic Analyzer, Voltage Glitcher, Linux TPM Tools
- **Scenario**: Trusted Platform Modules (TPMs) handle secure boot and credential sealing. Fault injection may allow attackers to bypass integrity checks or retrieve sealed secrets.
- **Attack Steps**: Step 1: Identify a system using TPM for sealed secrets or secure boot (e.g., BitLocker on Windows or tpm2-tools on Linux). Step 2: Access TPM SPI/I2C communication lines using a logic analyzer or interposer clip. Step 3: Power cycle the system and observe when the TPM verifies system measurements (PCRs). Step 4: Inject a glitch during this verification or during secret unsealing using a voltage drop or EM pulse. Step 5: Observe if the TPM returns sealed secrets or accepts tampered boot measurements. Step 6: If successful, you can extract BitLocker keys, BIOS passwords, or load unsigned OS images. Step 7: Optionally, use tpm2_unseal or tpm2_getrandom to test if the TPM responds abnormally. Step 8: Repeat attack to dump keys or extract firmware from TPM flash.
- **Detection**: TPM attestation failure, abnormal measurement registers
- **Solution**: Harden SPI/I2C lines, use TPM 2.0 with fault resistance, add PCR integrity checks
- **Tags**: TPM Glitching, BitLocker Key Extraction, Secure Boot Bypass

## Secure Boot Fault Injection

- **Attack Type**: Secure Boot Chain Fault Injection
- **Target**: IoT Devices, Embedded Systems
- **Vulnerability**: Fault in bootloader signature check
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Load unauthorized firmware, permanent backdoor
- **Tools**: Bootable IoT Device, Oscilloscope, EMFI Tool, UART Debug Cable, Firmware Dumper
- **Scenario**: Devices using Secure Boot rely on integrity checking. Glitching during signature verification or hash comparison may allow unsigned firmware to boot.
- **Attack Steps**: Step 1: Obtain a target embedded system that uses Secure Boot (e.g., routers, automotive ECUs, or IoT appliances). Step 2: Access the device's UART/debug port to observe boot logs and status messages. Step 3: Use an oscilloscope to locate when secure boot verification takes place (e.g., "Verifying signature..." line). Step 4: Inject a glitch during this signature or hash verification window using an EM pulse or power drop. Step 5: If successful, the system may skip the verification check and boot an unsigned or modified image. Step 6: Load a tampered image (e.g., with root shell or logging enabled) and observe if it boots successfully. Step 7: Once bypass is consistent, flash modified firmware to permanently disable security features. Step 8: Extract or dump original firmware for reverse engineering or analysis.
- **Detection**: Compare boot hash logs, monitor auth failures
- **Solution**: Use dual-stage signature validation, OTP fuses, and response delay obfuscation
- **Tags**: Secure Boot Bypass, Firmware Injection, EMFI, IoT Exploit

## Hardware Wallet Fault Attack

- **Attack Type**: Fault Injection on Signing
- **Target**: Hardware Wallets (Ledger, Trezor)
- **Vulnerability**: Fault during ECDSA or key schedule logic
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Private key recovery, crypto wallet theft
- **Tools**: Target Wallet (e.g., Trezor, Ledger), EMFI Tool, Serial Monitor, Logic Analyzer, Python/Sage
- **Scenario**: Hardware wallets store private keys securely. Injecting faults during signing (e.g., ECDSA) can leak key info via faulty signature outputs.
- **Attack Steps**: Step 1: Select a hardware wallet device (like Trezor One or Ledger Nano S) that performs ECDSA signatures internally. Ensure you have firmware that allows UART/debug logging. Step 2: Set up a voltage glitcher or EMFI injector. Connect to wallet’s power or clock line. Monitor output via UART or USB interface to capture signatures. Step 3: Trigger a fault at the moment the wallet performs scalar multiplication or modular inverse during ECDSA signing. This requires timing the glitch using screen feedback or debug serial messages (e.g., "Signing..."). Step 4: Collect faulty signature (r', s') and correct signature (r, s) for same or known messages. Step 5: Use SageMath to analyze faulted signature: if fault affects nonce k, you can compute private key via known algebraic relations. Step 6: Repeat faults with different messages to improve success rate. Step 7: Once private key is recovered, test it by signing messages manually or checking against blockchain transactions.
- **Detection**: Monitor signing anomalies; check signature validity before broadcasting
- **Solution**: Use redundant computations and signature verification checks internally
- **Tags**: ECDSA Fault, Hardware Wallet Attack, Private Key Extraction

## ARM SoC Bypass via Glitch

- **Attack Type**: Fault Injection to Bypass MPU
- **Target**: ARM Cortex-M SoCs, Embedded Devices
- **Vulnerability**: Glitch skipping critical memory checks
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Access control bypass, credential dump
- **Tools**: ARM Cortex-M Board (e.g., STM32), ChipWhisperer, Oscilloscope, UART Debug Cable
- **Scenario**: ARM Cortex-M SoCs have MPU (Memory Protection Units). Glitching during permission checks can allow illegal memory access or code execution.
- **Attack Steps**: Step 1: Set up an ARM-based dev board (e.g., STM32F4) with firmware that restricts access to specific memory regions using the MPU. Ensure UART debug logging is available. Step 2: Connect ChipWhisperer to control glitching. Use the serial output to monitor program flow and timing (e.g., “Checking memory access…”). Step 3: Trigger a voltage glitch just before the memory protection check or access violation handler executes. This may cause the CPU to skip the permission check entirely. Step 4: Write code to attempt reading a protected region (e.g., flash with secrets). If glitch is successful, UART or serial console will show leaked memory contents. Step 5: Repeat attack with different glitch delays and widths to improve success consistency. Step 6: Once access is achieved, dump all memory and extract any credentials or firmware.
- **Detection**: Use MPU logs and privilege violation interrupts
- **Solution**: Implement double-check memory accesses; monitor and reset on abnormal privilege escalation
- **Tags**: ARM Glitching, MPU Bypass, Secure Boot Exploit

## DFA (Differential Fault Analysis)

- **Attack Type**: Fault-Driven Differential Key Recovery
- **Target**: Symmetric Crypto Devices (AES, DES)
- **Vulnerability**: Bit-level fault in crypto round logic
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Full key extraction from symmetric encryption
- **Tools**: ChipWhisperer, Target Device (AES chip), Known Plaintexts, Python DFA Solver
- **Scenario**: DFA uses multiple faulty outputs and compares them with correct ones to reveal key bits, often on symmetric crypto like AES, DES, or RSA.
- **Attack Steps**: Step 1: Set up a target device performing AES encryption with known plaintexts. Ensure consistent operation and observable output (e.g., via serial terminal). Step 2: Use ChipWhisperer or EM injector to inject a glitch during a specific AES round (usually last or second-last). The fault should alter only a few bits in the output. Step 3: Send the same plaintext multiple times – once without glitch (get correct ciphertext), and multiple times with glitch (get faulty ciphertexts). Step 4: Input these ciphertext pairs into a DFA tool (like phoenixAES or Python DFA scripts). These tools analyze the fault pattern using mathematical properties of AES S-boxes to back-calculate key bytes. Step 5: Collect enough faulty pairs to recover all bytes of the AES key. Usually, 2–5 faulty outputs are sufficient. Step 6: Verify recovered key by encrypting/decrypting and comparing with the device’s results.
- **Detection**: Check for output deviation; monitor S-box hits
- **Solution**: Use fault-resistant crypto implementation, dual-processing validation
- **Tags**: AES DFA, Fault Crypto, Symmetric Key Recovery

## FIA + DPA Combo

- **Attack Type**: Hybrid Fault and Power Side-Channel Attack
- **Target**: AES Smartcards, Crypto ICs
- **Vulnerability**: Combined leakage from faults and side-channel
- **MITRE**: T1602 – Side Channel Analysis + T1601 Faults
- **Impact**: Full AES key in <100 traces using fault-assisted DPA
- **Tools**: ChipWhisperer Pro, EMFI Probe, Oscilloscope, Python (DPA toolkits), Smartcard Target
- **Scenario**: Combine Fault Injection (FIA) and Differential Power Analysis (DPA) to break crypto faster – faults simplify the secret, DPA reveals remaining unknown bits.
- **Attack Steps**: Step 1: Select a cryptographic device (smartcard, HSM, TPM) running symmetric encryption like AES. The goal is to use fault injection to reduce key entropy, then DPA to finish recovery. Step 2: Set up EMFI or voltage glitch to target specific AES operations (e.g., S-box lookup or MixColumns). Inject faults to force specific outputs to 0 or corrupt partial results. Step 3: Capture multiple power traces while encryption occurs under controlled input. Use glitch to ensure the same faulty behavior persists. Step 4: Perform DPA on the power traces. Because faults simplified parts of the internal state, DPA becomes easier (less noise, fewer traces needed). Step 5: Use correlation-based DPA tools (like ChipWhisperer Analyzer) to correlate hypothetical key bits with measured power. Step 6: Combine results from faulted ciphertexts and power trace analysis to recover the full AES key. Step 7: Validate by encrypting a known plaintext and comparing result. This method significantly reduces attack time and is very powerful in constrained targets.
- **Detection**: Monitor power profile anomalies; unexpected faults
- **Solution**: Mask key computations, inject noise, use fault detection logic
- **Tags**: Side-Channel + Fault, Hybrid Attack, Advanced DFA + DPA

## ROP Chain Injection via Faults

- **Attack Type**: Fault-Assisted ROP Injection
- **Target**: Embedded Firmware, IoT Binaries
- **Vulnerability**: Control flow hijack via fault-induced crash
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Remote code execution, control flow hijack
- **Tools**: Glitching Tool (EMFI or voltage), Testboard (e.g., STM32), GDB Debugger, Python
- **Scenario**: By causing a crash or fault at the right time in a program, attacker redirects control flow to small reusable instruction sequences (gadgets) → creates ROP chain.
- **Attack Steps**: Step 1: Set up a test system with a simple C-based firmware that reads input from UART and has a small memory buffer for passwords or commands. Ensure you have debug access via UART or JTAG. Step 2: Load a firmware that includes typical library calls like strcpy, printf, etc. These usually have ROP gadgets already present. Step 3: Use an EM glitch injector to crash the firmware right after input is received but before it is processed. This can disturb the return address or crash into an attacker-controlled buffer. Step 4: Craft an input that ends with a fake return address pointing to a "gadget" like pop r0; ret. Step 5: When the crash happens, control flow jumps to that gadget. Continue chaining gadgets in your payload to perform malicious actions like reading memory, changing variables, or calling secret functions. Step 6: Once chain is validated, you can extract data or bypass logic like authentication.
- **Detection**: Unexpected crash logs or call stack jumps
- **Solution**: Use stack canaries, ASLR, DEP, firmware integrity checks
- **Tags**: ROP, Fault Injection, Stack Hijack

## Fault-Based Instruction Skipping

- **Attack Type**: Skipping Security Logic with Glitch
- **Target**: Password Checks, Auth Logic
- **Vulnerability**: Instruction skipping at runtime
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Bypass of authentication or logic checks
- **Tools**: ChipWhisperer, EMFI Tool, Power Glitcher, UART Logger
- **Scenario**: Skip key security logic (e.g., PIN check, password match, user verification) by injecting glitch at the exact CPU cycle of comparison.
- **Attack Steps**: Step 1: Use a device or firmware with a function that verifies a password or PIN (e.g., “if (input == secret)” condition). You must be able to send data and observe response. Step 2: Observe serial/debug output to find when this check occurs — usually a short delay between “enter password:” and “access granted/denied”. Step 3: Send the wrong password intentionally while injecting a glitch using EMFI or voltage drop exactly at the CPU instruction executing the check. Step 4: If timed correctly, the check will be skipped, and execution will continue as if the password was correct. Step 5: System now responds with “Access Granted” even though password was wrong. Step 6: Repeat multiple times to fine-tune glitch timing and make the bypass consistent. Step 7: Once stable, use this method to gain unauthorized access every time.
- **Detection**: Monitor unexpected state transitions after auth attempts
- **Solution**: Redundant checks, dual-execution logic, timeout validation
- **Tags**: Logic Bypass, Fault-Glitch Auth, Secure Bypass

## Fault-Induced Buffer Overflow

- **Attack Type**: Fault Causes Memory Layout Corruption
- **Target**: Embedded Firmware, C-based Systems
- **Vulnerability**: Memory layout corruption via fault
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Arbitrary code execution, memory dump
- **Tools**: Embedded Board (C/C++ Firmware), Voltage Glitcher, Python Input Tool, GDB Debugger
- **Scenario**: A glitch corrupts internal stack layout, allowing overflow of a buffer into return address or sensitive variables → attacker hijacks execution.
- **Attack Steps**: Step 1: Prepare a C-based program (e.g., on STM32 or AVR) that has a vulnerable function like gets() or a simple scanf("%s", buf). Ensure the program is compiled without stack protection. Step 2: Normally, the function only allows a small number of characters. But due to glitch, memory size check can fail. Step 3: Inject a fault during memory length calculation or copy operation. This makes the device believe more memory is available than really exists. Step 4: Send a payload that includes extra characters after the buffer – those characters can overwrite saved registers or return address. Step 5: Include a ROP gadget or return address pointing to system("/bin/sh") or equivalent command. Step 6: When function returns, it uses the overwritten address, executing attacker payload. Step 7: Now you control the system or can dump sensitive data.
- **Detection**: Use address sanitizer; stack overflow detection tools
- **Solution**: Enable stack protection, bounds checking, ASLR, firmware integrity
- **Tags**: Buffer Overflow, Fault-Based Exploit, Stack Smash

## EM Pulse Injection (Non-contact)

- **Attack Type**: Covert Electromagnetic Glitching
- **Target**: Consumer Electronics, IoT, Embedded
- **Vulnerability**: Electromagnetic interference (EMI/EMC)
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Bypass of security checks, silent system compromise
- **Tools**: EM Pulse Gun (DIY or Pro), Oscilloscope, Antenna Coil, Laptop w/Control Scripts
- **Scenario**: EM pulses can be sent wirelessly to flip bits, skip instructions, or cause security violations in unshielded devices – without physical contact.
- **Attack Steps**: Step 1: Build or buy a basic EM pulse gun – can be made using a coil of copper wire, MOSFET driver, and capacitor bank. Alternatively, buy an EMFI tool like PicoEMP or FIRED. Step 2: Choose a target device (e.g., RFID reader, smart lock, or IoT camera) with plastic casing or weak EM shielding. Step 3: Position the EM injector 1–3 cm away from the device’s processor or board. No need to open or modify the device. Step 4: Power the device normally and observe its output (via LED, sound, display, or UART debug). Step 5: Trigger EM pulse during known sensitive operation like firmware boot, login check, encryption, or PIN entry. Use oscilloscope or logic analyzer to measure timing if needed. Step 6: Monitor for anomalies: reboots, skipped checks, corrupted output, debug shell. These indicate a successful fault. Step 7: Repeat under controlled lab settings to fine-tune pulse strength and frequency for consistent effect. Step 8: You now have a non-invasive way to glitch and compromise hardware.
- **Detection**: Use RF shielding, EM detectors, anomalous reset tracking
- **Solution**: Metal shielding, EM filters, ferrite beads on critical lines, secure housing
- **Tags**: EMFI, Wireless Fault Injection, IoT Exploit

## Power Line Glitch Attack

- **Attack Type**: Shared Power Line Voltage Manipulation
- **Target**: IoT Networks, Smart Home Devices
- **Vulnerability**: Shared power line interference
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Mass glitching, data corruption, cross-device instability
- **Tools**: Power Supply Controller (e.g., Arduino Relay, Variac), Oscilloscope, Smart Plugs/IoT Devices
- **Scenario**: By tampering with the power line shared by IoT devices (e.g., smart home), attackers induce unpredictable faults across multiple targets simultaneously.
- **Attack Steps**: Step 1: Set up a test environment with multiple IoT or embedded devices powered by the same source (e.g., USB hub, power strip). Step 2: Connect a power relay (Arduino-controlled or physical switch) between the power supply and the line going to devices. Use an oscilloscope to monitor the voltage stability. Step 3: Time your glitch during a sensitive operation (e.g., OTA update, password check, encrypted communication). Inject a short power dip (a millisecond or less) using the relay or a programmable power controller. Step 4: Observe device behavior: common faults include random reboots, corrupted memory, or authentication bypass. Step 5: Repeat the glitch during multiple boot phases or operations. Step 6: If a device enters debug mode, crashes, or skips validation, you've successfully induced a fault. Step 7: Optionally, log serial output or LED indicators to correlate faults with specific device actions.
- **Detection**: Monitor voltage fluctuations, boot log mismatches
- **Solution**: Power isolation per device, power conditioning filters, watchdog timers
- **Tags**: Power Glitching, Multi-Device Faults, Home IoT Attacks

## Rowhammer-style Fault Injection

- **Attack Type**: DRAM Row Activation Bit Flip Attack
- **Target**: Laptops, Desktops, Cloud VMs (DDR3)
- **Vulnerability**: DRAM charge leakage via frequent access
- **MITRE**: T1499.001 – Rowhammer
- **Impact**: Privilege escalation, memory corruption
- **Tools**: PC with vulnerable DRAM (DDR3 preferred), Rowhammer tool (e.g., hammer.py, RHX), Linux OS
- **Scenario**: Repeatedly accessing DRAM rows rapidly causes nearby bits to flip. This can be used to alter memory and gain unauthorized control without physical contact.
- **Attack Steps**: Step 1: Use a PC or laptop with DDR3 RAM (as newer DDR4/DDR5 are more resistant). Install Linux OS (Ubuntu preferred). Step 2: Download Rowhammer exploit tools like hammer.py or use browser-based PoCs (Google Project Zero). Step 3: Run a memory profiling tool to detect which rows are physically adjacent (e.g., by analyzing page frame numbers). Step 4: Run the Rowhammer tool to hammer specific rows (called aggressor rows) by repeatedly reading from them. This causes electrical interference to nearby victim rows. Step 5: After millions of accesses, adjacent bits in victim rows may flip from 1→0 or 0→1. Step 6: Check if bit flips occurred in page tables, memory buffers, or kernel space. Step 7: Craft the attack to flip bits in a way that elevates privileges (e.g., from user to root). Step 8: Use flipped memory region to inject code or alter access controls.
- **Detection**: ECC logging, bit flip detection, memory error logs
- **Solution**: Use ECC RAM, memory refresh hardening, software rowhammer mitigations
- **Tags**: Rowhammer, DRAM Attack, Memory Flip Exploit

## Remote USB Power Fault

- **Attack Type**: USB Power Fluctuation-Based Fault Attack
- **Target**: USB Devices, Mobile Devices, IoT Boards
- **Vulnerability**: Lack of power stability handling
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Boot bypass, firmware crash, credential loss
- **Tools**: USB Kill Cable (with switch), USB Power Meter, Device with USB Boot or Charging Port
- **Scenario**: By modifying USB power flow using cables or remote tools, attacker induces faults in connected devices (e.g., reboot, crash, bypass of firmware checks).
- **Attack Steps**: Step 1: Choose a device that charges or boots via USB (e.g., smartphone, dev board, Raspberry Pi). Ensure debug logs are visible via UART or screen. Step 2: Use a USB cable with power control features (e.g., USB Kill Switch Cable or DIY relay cable). Optionally monitor using USB power meter (e.g., PortaPow or USB Doctor). Step 3: Power the device and wait for a critical operation (e.g., password prompt, boot process). Step 4: Briefly cut power (100–500ms) using the kill switch. Then immediately restore power. Step 5: Observe if the system boots into recovery, skips authentication, or crashes into a debug shell. Step 6: Repeat multiple times with different timing to find vulnerable windows. Step 7: You can use this to bypass secure boot or trigger memory faults.
- **Detection**: Monitor USB connection resets, serial debug output
- **Solution**: Harden USB firmware, detect power dips, boot watchdog mechanisms
- **Tags**: USB Fault, Boot Glitch, Power Exploit

## Cache Poisoning via Faults

- **Attack Type**: Cache Corruption via Fault Injection
- **Target**: Embedded CPUs, Mobile CPUs, Caches
- **Vulnerability**: Cache line corruption, tag collision
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Unauthorized data reuse, logic bypass
- **Tools**: SoC (e.g., ARM Cortex), EM Glitch Tool, Cache Profiler, Custom Firmware with Logging
- **Scenario**: By glitching CPU operations or cache memory access, attacker injects or corrupts cache lines → causes incorrect data reuse or privileged data exposure.
- **Attack Steps**: Step 1: Use a device with known caching system (e.g., Cortex-A SoC) and loggable memory access. Firmware should read/write sensitive values (e.g., auth tokens) from cache. Step 2: Set up EM glitch tool to target specific memory access regions, preferably while cache is being filled. Step 3: Time your glitch when CPU performs cache refill or instruction fetch from memory. Step 4: The fault may flip cache tag bits or cause incorrect line refill, loading wrong data. Step 5: Inject fake data into cache during glitch (e.g., via attacker-controlled peripheral or buffer) to replace valid auth or config. Step 6: Allow CPU to continue using corrupted cache line for logic (e.g., to skip login, load wrong permissions). Step 7: Log output and behavior – success is usually shown by unauthorized access or corrupted display. Step 8: Repeat to create persistent logic bugs or escalate privileges.
- **Detection**: Compare cache vs memory mismatch logs, abnormal exec flow
- **Solution**: Flush cache after critical ops, use ECC caches, cache partitioning
- **Tags**: Cache Attack, CPU Glitch, Memory Poisoning

## ChipWhisperer with Glitch Module

- **Attack Type**: Clock/Voltage Glitch for Key Extraction
- **Target**: AES Encryption Chips, Embedded Auth Boards
- **Vulnerability**: Voltage/clock instability vulnerability
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Private key leak, auth bypass, secure boot defeat
- **Tools**: ChipWhisperer-Lite, Target Board (e.g., XMEGA or STM32), CW Analyzer, Python
- **Scenario**: ChipWhisperer is a powerful open-source tool used to perform clock and voltage glitches to extract cryptographic keys from embedded devices via fault analysis.
- **Attack Steps**: Step 1: Connect your ChipWhisperer board to your computer via USB. Plug the glitch cable into the target microcontroller (e.g., XMEGA or STM32 board) using provided headers. Step 2: Flash the victim board with known vulnerable AES or password-check firmware (provided in ChipWhisperer tutorials). Step 3: Open the ChipWhisperer Analyzer GUI or use the Python Jupyter notebook interface. Step 4: Set the glitch parameters: define clock frequency, glitch offset (timing), and width (how long the glitch lasts). Step 5: Trigger the encryption or check function on the target board. ChipWhisperer will time the glitch to occur during a sensitive part (e.g., S-box lookup or conditional check). Step 6: Record output. If the glitch succeeded, you’ll see faulty ciphertext or unauthorized access. Step 7: Repeat and tune parameters to find consistent success. Step 8: Use ChipWhisperer’s scripts to compare faulted outputs and infer private keys using DFA or CPA methods.
- **Detection**: Side-channel monitoring, fault logging
- **Solution**: Secure boot checks, dual-register validation, clock jitter countermeasures
- **Tags**: ChipWhisperer, Glitching, Side-Channel Faults

## Riscure Fault Injection Platform

- **Attack Type**: Commercial Fault Injection (EM, Laser, Volt)
- **Target**: Smartcards, HSMs, Secure ICs
- **Vulnerability**: Instruction timing glitches via advanced tools
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Professional-level chip attack, cert bypass, signature faults
- **Tools**: Riscure Inspector, Glitch Amplifier, EM Probe, DUT (Device Under Test), Control Software
- **Scenario**: Riscure's platform enables extremely precise EM, clock, and voltage glitching on chips, often used by professional researchers or certification labs to break cryptographic chips.
- **Attack Steps**: Step 1: Place your DUT (e.g., secure element or smartcard chip) into the EM-glitch testbed provided with Riscure. Connect the EM coil and power lines per instructions. Step 2: Use Riscure Inspector’s GUI to map the chip’s operation cycles (e.g., decryption, signing, etc.). The system will help visualize instruction timing. Step 3: Select a fault injection method: clock glitch, voltage dip, or EM pulse. Define the exact moment for the glitch using Inspector’s cycle-accurate triggers. Step 4: Trigger the glitch during critical operations, such as when a cryptographic key is being used or a secure check is being performed. Step 5: Log faulty results, observe device reaction (e.g., faulted signature, logic bypass). Step 6: Use built-in analysis tools or export the output to Python for key recovery. Step 7: Iterate on glitch strength, angle (for laser/EM), and timing until you reach consistent results.
- **Detection**: Fault alert logs, response time analysis
- **Solution**: Circuit-level protection, glitch resistance, redundant execution paths
- **Tags**: Riscure, EM Glitch, Certification Testing

## DIAMOND Laser Fault Injector

- **Attack Type**: Transistor-Level Laser Glitching
- **Target**: ASICs, Secure Crypto Chips
- **Vulnerability**: Faults at silicon via light energy
- **MITRE**: T1601.002 – Hardware Fault Injection
- **Impact**: Transistor flips, permanent data corruption
- **Tools**: DIAMOND Laser Injector, Optical Bench, Oscilloscope, DUT Chip
- **Scenario**: The DIAMOND platform emits precisely controlled laser pulses to flip individual bits or fault registers in cryptographic chips at the silicon level (used in high-end labs).
- **Attack Steps**: Step 1: Mount the DUT (chip with cryptographic functions) under the laser injector on an optical bench. Carefully remove any packaging if the chip isn’t laser-transparent. Step 2: Use a camera to align the laser on the exact silicon region that corresponds to the part of the chip you want to attack (e.g., ALU, registers, memory controller). Step 3: Supply power and I/O to the chip and initialize a cryptographic operation like RSA signing or AES encryption. Step 4: Trigger the laser pulse at nanosecond precision during a sensitive instruction cycle (e.g., modular inverse). Step 5: Monitor changes in chip output (e.g., incorrect signature, corrupted ciphertext). Step 6: Repeat and fine-tune the pulse timing, duration, and intensity to target specific logic. Step 7: Use faulted outputs in key recovery analysis (e.g., Bellcore RSA fault attack).
- **Detection**: Use logic self-checking, photonic sensors inside chips
- **Solution**: Optical shielding, tamper-detection fuses, self-reset after unknown behavior
- **Tags**: Laser Fault, Bit Flip, Transistor Glitching

## OpenSCA Framework + Glitch Kit

- **Attack Type**: Open-Source Fault + Side-Channel Framework
- **Target**: STM32, AVR, XMEGA Boards
- **Vulnerability**: Fault during SCA trace acquisition
- **MITRE**: T1602 + T1601.002 – SCA + Fault Injection
- **Impact**: AES/DES key recovery, combined leakage exploitation
- **Tools**: OpenSCA Toolkit, Arduino/STM32 Target, Glitch Injector (DIY or ChipSHOUTER), Jupyter/Python
- **Scenario**: OpenSCA combines side-channel analysis (like DPA) with voltage glitching tools, allowing community researchers to break crypto systems on embedded targets.
- **Attack Steps**: Step 1: Set up OpenSCA environment by installing it on your Linux or Windows machine (available from GitHub). Connect your target device (e.g., STM32 dev board) to the glitch module and a logic analyzer. Step 2: Flash the board with vulnerable cryptographic firmware (available from OpenSCA labs). Step 3: Launch OpenSCA’s GUI or use its Python API to start capturing side-channel traces while performing AES encryption. Step 4: While traces are captured, apply a voltage glitch during specific AES rounds (e.g., round 9). Use OpenSCA’s timing control tools to sync this. Step 5: Collect faulty ciphertexts and analyze the power traces together. This helps in conducting fault-augmented DPA attacks (combining physical and logical leakage). Step 6: Use the statistical correlation methods provided by OpenSCA to guess key bytes. Repeat until full key is recovered. Step 7: Validate by re-encrypting known plaintexts with guessed key and comparing with real device output.
- **Detection**: Abnormal correlation spikes, high entropy in trace groups
- **Solution**: Hardware masking, shuffling, input blinding, and noise generators
- **Tags**: SCA + Glitch, Open-Source Crypto Hacking

## PulseView + Custom Probe

- **Attack Type**: Signal Monitoring & Side-Channel Logging
- **Target**: Embedded Devices, Smartcards, IoT
- **Vulnerability**: Exposed serial protocols, observable key traffic
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Secret key leakage, replay attacks, crypto data exposure
- **Tools**: PulseView (open-source), Saleae/FX2LA logic analyzer, Custom Probe (crocodile clips or PCB hooks)
- **Scenario**: Use PulseView with a logic analyzer and hand-made probe to capture serial (UART/SPI) communication, observe key exchanges, or replay messages.
- **Attack Steps**: Step 1: Download and install PulseView from Sigrok.org on your laptop. Connect a USB logic analyzer like FX2LA or compatible device. Step 2: Identify exposed communication lines on your device (e.g., RX/TX pins of UART or CLK/MOSI/MISO of SPI). If unsure, use a multimeter or datasheet to find pin functions. Step 3: Create a custom probe using jumper wires or small test clips to tap into the signal lines (non-invasive). Connect them to the logic analyzer. Step 4: Open PulseView and configure the sample rate (2–4 MHz is usually good for UART/SPI). Set proper protocol decoder (e.g., UART, SPI) from the toolbar. Step 5: Start the capture while interacting with the device (e.g., sending password, performing login, decrypting). Step 6: Analyze the waveform and decode packets to observe secret data, keys, or protocol exchanges. Save the captured data as .sr file. Step 7: Use decoded data to analyze patterns or extract challenge-response values for replay or brute force attempts.
- **Detection**: Monitor serial traffic for eavesdropping devices
- **Solution**: Masking, encrypted protocols, hardware-layer obfuscation
- **Tags**: Side-Channel, UART Tapping, Open Hardware SCA

## Replay Attack on Challenge-Response Auth

- **Attack Type**: Replay of Previously Valid Response
- **Target**: RFID, Smartcards, Authentication Devices
- **Vulnerability**: Missing nonce/freshness check
- **MITRE**: T1110.003 – Credential Stuffing
- **Impact**: Unauthorized access, impersonation
- **Tools**: Proxmark3, Flipper Zero, Logic Analyzer, PulseView
- **Scenario**: In weak challenge-response systems (e.g., RFID cards), attackers record a valid authentication session and replay it later without solving the challenge.
- **Attack Steps**: Step 1: Use a sniffing tool like Proxmark3 or Flipper Zero to record a successful authentication session between the client (e.g., RFID card or token) and the server (reader). Step 2: Save the raw signal (or packet dump) from that session using the tool’s memory or log system. Step 3: Wait for a later time when you want unauthorized access (e.g., to a door or device). Step 4: Replay the exact recorded signal using the same tool, pretending to be the original client. Step 5: If the system does not validate freshness or use cryptographic nonces, it will accept the replayed response as valid. Step 6: You gain unauthorized access without breaking encryption. Step 7: This can be repeated until the system adds anti-replay features like timestamps or rotating keys.
- **Detection**: Replay alerting, timestamp logging
- **Solution**: Add nonce, timestamp, rolling keys, and challenge integrity
- **Tags**: RFID, Replay, Challenge Response, Token Abuse

## TLS/SSL Session Replay

- **Attack Type**: Session ID Reuse Attack
- **Target**: Web Servers, TLS Apps, HTTPS Clients
- **Vulnerability**: Weak session ID validation, long ticket life
- **MITRE**: T1557.002 – Man-in-the-Middle
- **Impact**: Session hijack, unauthorized encrypted access
- **Tools**: Wireshark, SSL Labs Scanner, Burp Suite, Scapy
- **Scenario**: Exploiting reused or unexpired TLS session IDs or session tickets to re-establish connections without credentials.
- **Attack Steps**: Step 1: Monitor a client-server TLS handshake using Wireshark or a similar sniffer. Focus on “ClientHello” and “ServerHello” messages and identify Session IDs or Session Tickets. Step 2: Note if the server supports session resumption and does not enforce expiration or uniqueness. Step 3: Reuse the Session ID or Ticket in a new connection from the same client or spoofed IP using Burp Suite or Scapy. Step 4: Server accepts the session and resumes encrypted communication without a fresh handshake. Step 5: If attacker previously hijacked a valid session or stole the session ID, they can replay it to gain encrypted access or hijack login. Step 6: Attack is successful if the server does not properly bind session ID to client IP, or if session tickets are not securely encrypted.
- **Detection**: Monitor duplicate session IDs or unusual resumption events
- **Solution**: Enforce short ticket lifetime, bind session to IP, disable reuse
- **Tags**: TLS, SSL, Session Replay, MITM

## Token Replay in OAuth2 / JWT

- **Attack Type**: Replay of Access Tokens
- **Target**: OAuth2 APIs, Mobile Apps, Web Services
- **Vulnerability**: Lack of token binding or short expiry
- **MITRE**: T1529 – Access Token Manipulation
- **Impact**: API takeover, session hijack, privilege misuse
- **Tools**: Postman, JWT.io, Burp Suite, Mitmproxy
- **Scenario**: Attackers reuse valid access tokens (JWTs) to access APIs repeatedly, especially if tokens are not bound to client/IP or lack short expiry.
- **Attack Steps**: Step 1: Intercept an HTTP request with an Authorization: Bearer <token> header using Burp Suite or Mitmproxy while user is logged in. Step 2: Copy the full token (usually a JWT), and decode it at jwt.io to understand its expiry and claims. Step 3: Reuse this token in Postman or curl to make the same API call (e.g., user info or file access). Step 4: If the server does not validate token origin or expiry, the API responds with valid data. Step 5: Repeat this request multiple times or from a different machine to test whether the token is truly bound to a user session or client device. Step 6: If allowed, attacker gains unauthorized access or performs actions on behalf of the victim. Step 7: Attack succeeds when tokens are long-lived and not bound to context (e.g., device fingerprint, IP, or time).
- **Detection**: Audit access logs for reused tokens from unusual IPs
- **Solution**: Use short token lifetimes, refresh tokens, bind tokens to context (IP/device)
- **Tags**: JWT, OAuth2, Token Replay, API Abuse

## Certificate Replay Attack

- **Attack Type**: TLS/SSL Certificate Reuse Attack
- **Target**: TLS Systems, Mutual TLS APIs
- **Vulnerability**: Misconfigured cert validation / no binding
- **MITRE**: T1586 – Compromise Valid Accounts
- **Impact**: Client impersonation, secure channel hijack
- **Tools**: Wireshark, OpenSSL, Burp Suite, Expired or Leaked Certificates
- **Scenario**: In rare and misconfigured TLS setups, an attacker reuses a valid digital certificate across devices or sessions, bypassing identity validation.
- **Attack Steps**: Step 1: Intercept a TLS handshake from a client using Wireshark or Burp Suite and capture the certificate presented to the server. Step 2: Analyze whether the certificate uses client-auth (e.g., in mutual TLS). If it’s not bound to IP/device and has a long expiry, it may be reusable. Step 3: Attempt to replay that certificate in another session using tools like OpenSSL (openssl s_client) or via browser with certificate injection (in some dev setups). Step 4: If the server only checks the certificate validity and not binding (e.g., subject name/IP/certificate pinning), it may accept the replayed certificate. Step 5: This results in authentication bypass, especially in internal networks or IoT systems using client certs. Step 6: Success depends on server misconfig, lack of revocation check, and poor client binding.
- **Detection**: Cert reuse from unknown device/IP, TLS handshake logs
- **Solution**: Pin certificate to device fingerprint, use short-lived certs, enforce CRL/OCSP
- **Tags**: TLS, Certificate Replay, Mutual Auth

## Payment Replay Attack

- **Attack Type**: Transaction Replay Attack
- **Target**: E-commerce, Payment APIs, Mobile Wallets
- **Vulnerability**: Missing idempotency check or nonce
- **MITRE**: T1646 – Transaction Fraud
- **Impact**: Double payments, fraud, monetary loss
- **Tools**: Burp Suite, Postman, Wireshark, Payment Gateway Test Environment
- **Scenario**: Attackers resend a valid payment request multiple times to cause duplicate charges if the server lacks transaction ID uniqueness or timestamp validation.
- **Attack Steps**: Step 1: Make a legitimate payment (e.g., $1) on a test e-commerce website while capturing the request using Burp Suite or Wireshark. Step 2: Identify the payment request (typically POST with JSON/XML containing order ID, amount, and signature). Step 3: Save the entire request with headers, body, and auth token. Step 4: Replay the exact same request multiple times using Postman or Burp Suite's repeater tab. Step 5: If the backend does not validate uniqueness of transaction ID or timestamp, it will process the same payment multiple times. Step 6: You’ll see the same order charged again, or multiple confirmations generated. Step 7: In real-world cases, attackers automate this to siphon money or game discounts.
- **Detection**: Monitor repeated identical transactions in short time
- **Solution**: Enforce nonce, unique order ID per request, timestamp validation
- **Tags**: Payment API, Idempotency, Replay, Fraud

## Login Replay

- **Attack Type**: Credential Replay via API or Session
- **Target**: Web Logins, APIs, SSO Systems
- **Vulnerability**: Long-lived sessions, lack of binding
- **MITRE**: T1078 – Valid Account Abuse
- **Impact**: Account takeover, unauthorized access
- **Tools**: Burp Suite, Fiddler, Wireshark, Mitmproxy
- **Scenario**: Reuses captured login requests to simulate a real user login, especially where tokens are long-lived or sessions don’t require full re-authentication.
- **Attack Steps**: Step 1: Intercept a successful login HTTP request using Burp Suite. Copy all headers, body, and most importantly the session cookie or Authorization: Bearer token. Step 2: Log out of the session to simulate that it’s closed. Step 3: Paste the copied request into Postman or Burp Repeater and resend it. Step 4: If the session hasn’t been invalidated, or if the server doesn't tie the session to IP/device/browser, you’ll be logged in again without credentials. Step 5: Repeat this from different networks or devices. Step 6: This simulates a session hijack or token misuse scenario. Step 7: The attack is successful when login is accepted based only on replayed token or session without rechecking credentials.
- **Detection**: Log session reuse from new IP/device
- **Solution**: Bind sessions to device/IP/user-agent, enable re-authentication triggers
- **Tags**: Session Replay, Token Misuse, Identity Hijack

## CSRF + Replay

- **Attack Type**: Combined Cross-Site + Replay Attack
- **Target**: Web Forms, Banking Apps, Control Panels
- **Vulnerability**: Missing CSRF token or token reuse
- **MITRE**: T1190 + T1110.003 – Injection + Replay
- **Impact**: Money transfer, password/email change
- **Tools**: Burp Suite, Browser Dev Tools, BeEF, CSRF PoC Template
- **Scenario**: Combines Cross-Site Request Forgery with replay of a valid user request to repeat actions like transfer funds, reset password, or change email.
- **Attack Steps**: Step 1: Create a malicious HTML/JavaScript page that sends a request (e.g., fund transfer) using a previously known URL and parameters (e.g., POST /transfer?to=attacker&amount=100). Step 2: Host this page on your server or GitHub. Trick the target user into clicking the link while logged into the victim site. Step 3: If the site does not use anti-CSRF tokens or validates origin headers, the request is accepted as if coming from the user. Step 4: The request is processed (e.g., transfer happens), and the user remains unaware. Step 5: Now replay the same CSRF request again using tools like Burp Repeater, as it does not expire or is not unique. Step 6: You repeat malicious actions multiple times, combining CSRF with replay logic. Step 7: The attack succeeds when the site trusts all POSTs and does not validate CSRF token freshness.
- **Detection**: Detect repeated POSTs from unknown origins
- **Solution**: Use unique per-request CSRF tokens, verify Origin and Referer headers
- **Tags**: CSRF, Session Replay, Browser-Based Attack

## Signed URL Replay

- **Attack Type**: File Access Replay
- **Target**: Cloud Storage, SaaS Portals
- **Vulnerability**: Weak signed URL enforcement
- **MITRE**: T1530 – Data from Cloud Storage
- **Impact**: Unauthorized file download, data leak
- **Tools**: Burp Suite, Postman, AWS CLI, Browser Dev Tools
- **Scenario**: Attackers reuse signed URLs (e.g., from AWS S3, Azure Blob, GCP) for downloading protected files if servers don’t enforce expiration or origin checks.
- **Attack Steps**: Step 1: Intercept a signed URL used for file download from an S3 bucket or Azure blob (e.g., https://bucket.s3.amazonaws.com/file.txt?AWSAccessKeyId=...). Step 2: Note the expiration timestamp and policy in the query string. If the expiry time is far into the future, or not validated server-side, it can be reused. Step 3: Copy the full URL and test access from another browser/device/IP to confirm if it works. Step 4: Reuse this URL later (e.g., share with others or trigger downloads from scripts). Step 5: If the backend does not verify IP, device, or expiration time strictly, the file remains accessible without re-signing. Step 6: This exposes sensitive files like invoices, logs, or internal backups via uncontrolled sharing.
- **Detection**: Access logs from unknown locations or expired timestamps
- **Solution**: Bind signed URL to IP/device; use short expiry (e.g., 5–10 mins); validate expiry strictly server-side
- **Tags**: S3, Azure Blob, Signed URL, Link Replay

## Webhook Replay

- **Attack Type**: Event Trigger Replay
- **Target**: SaaS Webhooks, CI/CD Hooks, Payment Systems
- **Vulnerability**: Missing signature verification or timestamp check
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: False order confirmation, duplicate events
- **Tools**: Burp Suite, ngrok, Postman, Webhook.site, Mitmproxy
- **Scenario**: Re-sending previously captured webhook payloads to re-trigger actions like order creation, user signup, or alerting.
- **Attack Steps**: Step 1: Intercept an incoming webhook using ngrok, webhook.site, or Burp Collaborator. Save the full payload and headers. Step 2: Copy the captured payload (e.g., JSON for order update or alert trigger). Step 3: Use Postman to resend the same webhook to the target server endpoint. Step 4: If the server does not use replay protection (e.g., HMAC timestamp check, nonce), it will accept and process the request again. Step 5: The same action (e.g., payment marked complete, SMS alert sent) gets triggered multiple times. Step 6: Attack is successful when the webhook receiver does not validate signature freshness or duplication. Step 7: Advanced setups automate this replay to manipulate order status or billing repeatedly.
- **Detection**: Monitor event frequency and validate timestamp/IP
- **Solution**: Enforce webhook HMAC signature with nonce and expiry; log replayed webhooks
- **Tags**: Webhooks, Signed Replay, CI/CD, API

## 802.11 Wireless Replay Attack

- **Attack Type**: WPA 4-Way Handshake Replay
- **Target**: WPA/WPA2 Routers, Wi-Fi Clients
- **Vulnerability**: Unprotected handshake replay
- **MITRE**: T1430 – Wireless Protocol Exploitation
- **Impact**: Wireless DoS, WPA cracking, auth disruption
- **Tools**: aircrack-ng, Wireshark, hcxpcaptool, Scapy
- **Scenario**: Replaying captured WPA handshake messages to cause re-authentication, disassociation, or facilitate key cracking (WPA/WPA2).
- **Attack Steps**: Step 1: Use a Wi-Fi adapter in monitor mode (e.g., Alfa USB adapter) and start capturing WPA traffic with airodump-ng. Step 2: Capture the 4-way handshake from a target client joining the Wi-Fi. This consists of EAPOL packets used during WPA authentication. Step 3: Use aircrack-ng or hcxpcaptool to save and analyze the handshake. Step 4: Replay the captured handshake packets using aireplay-ng or Scapy, simulating the target client. Step 5: Depending on access point behavior, this can cause session reset, deauth, or help in cracking the Pre-Shared Key (PSK) using dictionary attacks. Step 6: This attack is effective when the handshake is reused or unverified properly by routers. Step 7: You may use the captured handshake with wordlists to brute-force the Wi-Fi password offline.
- **Detection**: Track repeated EAPOLs from spoofed MACs or IPs
- **Solution**: Enforce anti-replay on router, use WPA3, rotate session keys frequently
- **Tags**: Wi-Fi, WPA, Handshake Replay, Wireless DoS

## VoIP Replay

- **Attack Type**: RTP Stream Replay Attack
- **Target**: VoIP Systems, IP Phones, SIP Servers
- **Vulnerability**: No RTP/SRTP replay protection
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Fake calls, message playback, call log manipulation
- **Tools**: Wireshark, SIPp, RTPReplay, Asterisk PBX
- **Scenario**: Replay of previously recorded VoIP (SIP/RTP) packet streams to regenerate calls or fake conversations on VoIP systems.
- **Attack Steps**: Step 1: Set up a packet sniffer like Wireshark on a network with VoIP traffic (e.g., using SIP over RTP). Filter for SIP and RTP protocols. Step 2: Record a full VoIP session (SIP negotiation + RTP audio packets). Save the .pcap file. Step 3: Use rtpbreak or RTPReplay to extract and replay the RTP stream to the original destination or fake endpoint. Step 4: The receiving device or system (e.g., IP phone, PBX) may accept the audio stream as valid, depending on its replay protection. Step 5: Use SIPp or Scapy to simulate the SIP session and replay both control and media. Step 6: The attack is successful when the replayed stream is accepted and generates audio or triggers call-related events.
- **Detection**: Monitor RTP/SIP stream duplication, log media flow timestamps
- **Solution**: Use SRTP with anti-replay, session tokens, and time-bound call metadata
- **Tags**: VoIP, RTP Replay, SIP Attack, Network Media Hijack

## MITM + Replay

- **Attack Type**: Man-in-the-Middle Replay Attack
- **Target**: Web Apps, APIs, Network Services
- **Vulnerability**: Lack of anti-replay validation
- **MITRE**: T1557 – Man-in-the-Middle
- **Impact**: Unauthorized access, duplicate action execution
- **Tools**: Wireshark, Burp Suite, Scapy, mitmproxy
- **Scenario**: Attacker captures valid data in transit using MITM and replays it at a different time to gain access or trigger actions.
- **Attack Steps**: Step 1: Set up a proxy or sniffer using mitmproxy or Burp Suite to intercept traffic between a user and the target application (e.g., login requests, session tokens, API calls). Step 2: Capture a valid request (like login, data submission, or payment) during a real session. Step 3: Save the full request including all headers, body, cookies, and tokens. Step 4: Disconnect or wait for the original session to end. Step 5: Replay the exact captured request from a different IP or at a different time using curl, Postman, or Burp Repeater. Step 6: If the server accepts it without validating freshness, source, or session context, the attacker can successfully replay it to access user data, impersonate a user, or trigger functions. Step 7: This works best when the application lacks nonce, timestamp, or proper session management.
- **Detection**: Detect repeated request patterns or replayed session tokens
- **Solution**: Use nonces, timestamps, and strict session context binding
- **Tags**: MITM, Replay, Token Theft, Credential Hijack

## ICMP Packet Replay

- **Attack Type**: ICMP Echo Replay / Scanning Spoof
- **Target**: Networks, Servers, IDS Systems
- **Vulnerability**: Blind trust in ICMP traffic
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Network evasion, false positive alerts
- **Tools**: Scapy, tcpdump, Wireshark, hping3
- **Scenario**: Replaying captured ICMP (ping) requests to simulate activity, bypass firewall rules, or confuse intrusion detection systems (IDS).
- **Attack Steps**: Step 1: Capture legitimate ICMP echo request packets (pings) on the network using tcpdump or Wireshark. Save the pcap file containing these packets. Step 2: Analyze the timestamps, source IP, and destination. Step 3: Use Scapy or hping3 to craft and send identical ICMP packets from a spoofed IP address. Step 4: Replay them to the same or different host to simulate real communication or test if firewall/IDS allows pings from known devices. Step 5: In some scenarios, IDS or monitoring tools will treat these as real traffic, causing confusion or alert fatigue. Step 6: This technique can also help hide malicious traffic within what appears to be normal ping activity.
- **Detection**: Log anomalies in ICMP timestamps or replayed payloads
- **Solution**: Rate-limit ICMP; verify timing/IP pattern of echo requests
- **Tags**: ICMP, Replay, Firewall Bypass, Scapy

## Replay in VPN Tunnels (IPsec)

- **Attack Type**: IPsec Tunnel Replay
- **Target**: IPsec VPNs, Site-to-Site Tunnels
- **Vulnerability**: Disabled or misconfigured anti-replay window
- **MITRE**: T1497 – Network Denial-of-Service
- **Impact**: Tunnel reset, data corruption, degraded VPN security
- **Tools**: Wireshark, StrongSwan, Libreswan, Scapy
- **Scenario**: Exploiting VPNs that don’t use anti-replay windows to inject repeated encrypted packets and disrupt secure channels.
- **Attack Steps**: Step 1: Set up a VPN tunnel using IPsec between two endpoints (e.g., StrongSwan client and server). Step 2: Capture VPN traffic during a secure transmission using Wireshark, focusing on ESP (Encapsulating Security Payload) packets. Step 3: Save the .pcap and identify ESP SPI (Security Parameters Index). Step 4: Use Scapy to re-inject these ESP packets into the network at different times. Step 5: If the VPN implementation does not enforce anti-replay windows (sliding sequence validation), the receiving system may accept and process the old packets. Step 6: This can break integrity checks, trigger session resets, or cause data leakage or denial-of-service. Step 7: Attack is more likely to succeed in legacy or self-hosted VPN systems with lax IPsec configuration.
- **Detection**: Log duplicate ESP sequences or non-monotonic SPI values
- **Solution**: Always enable anti-replay protection; monitor ESP sequence integrity
- **Tags**: VPN, IPsec, Replay Attack, ESP

## Bluetooth Low Energy (BLE) Replay

- **Attack Type**: Wireless BLE Replay Attack
- **Target**: BLE Devices, Smart Locks, IoT Sensors
- **Vulnerability**: No encryption or pairing replay protection
- **MITRE**: T1477 – Hardware Protocol Exploitation
- **Impact**: Unauthorized device control, smart lock bypass
- **Tools**: GATTacker, BtleJack, Ubertooth, Wireshark, nRF Connect
- **Scenario**: Replaying captured BLE pairing or control messages to impersonate a device, unlock smart locks, or trigger commands.
- **Attack Steps**: Step 1: Use Ubertooth or BtleJack to scan for active BLE devices (e.g., smart lock, fitness band). Step 2: Record BLE pairing or control packets (like unlock, notify, or write commands) using sniffer mode. Step 3: Save this capture (e.g., from Wireshark or btmon) to a file. Step 4: Use tools like GATTacker or BtleJack to replay those captured packets to the same device at a later time. Step 5: If the BLE device does not use rolling keys or proper encryption for each session, it will accept the replayed commands. Step 6: For example, a door lock might unlock without needing a real phone if the unlock command is replayed. Step 7: Repeat the attack near the target BLE device and verify if response is triggered.
- **Detection**: Monitor for repeated BLE packets with same UUID/handle
- **Solution**: Use encrypted BLE pairing (LE Secure Connections), implement freshness tokens
- **Tags**: BLE, Wireless Replay, IoT Exploit, Bluetooth Attack

## NFC Replay

- **Attack Type**: Contactless Payment Replay
- **Target**: NFC Payment Terminals, Access Readers
- **Vulnerability**: Lack of nonce/timestamp validation
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: Unauthorized payments or access
- **Tools**: Proxmark3, Android NFC Reader Apps, ChameleonMini
- **Scenario**: Capturing and replaying NFC-based mobile payment or access card communication to impersonate a user’s device.
- **Attack Steps**: Step 1: Use a tool like Proxmark3 or an NFC-enabled Android phone with specialized reader apps (like NFC Tools Pro) to scan and log NFC transaction data from a contactless card or mobile wallet. Step 2: Capture the communication when the user taps their card or device on a reader (e.g., at a transit gate or payment terminal). Step 3: Save the full data exchange (UID, payloads, APDU commands) using your reader. Step 4: Replay the exact same sequence using a device that can emulate NFC (e.g., ChameleonMini or even another Android with emulation support). Step 5: The reader may accept the replayed data if it does not validate transaction freshness (timestamp, nonce, or session binding). Step 6: If successful, the attacker gets unauthorized access (e.g., free transit, fake payment) or impersonates a device.
- **Detection**: Monitor for repeated UID access; use dynamic credentials
- **Solution**: Use per-transaction signatures or rotating UIDs with crypto verification
- **Tags**: NFC, Contactless Payment, Transit Exploit

## RFID Replay

- **Attack Type**: Radio Frequency Authentication Replay
- **Target**: RFID Doors, Keycards, Access Control
- **Vulnerability**: Static UIDs or lack of challenge-response
- **MITRE**: T1110.003 – Credential Stuffing
- **Impact**: Physical unauthorized entry
- **Tools**: Proxmark3, RFIDler, ChameleonMini, Flipper Zero
- **Scenario**: Replaying RFID badge codes or keycard data to gain physical access to buildings, hotel rooms, or vehicles.
- **Attack Steps**: Step 1: Stand near a target user who is scanning their RFID card (e.g., building entry badge). Use a device like Proxmark3, Flipper Zero, or RFIDler in sniffing mode to capture the radio signal. Step 2: Save the UID and signal timing of the RFID packet. Step 3: Switch to emulation mode on the device and replay the same UID or full payload while standing near the RFID reader. Step 4: If the system does not use rolling codes or challenge-response validation, the door or gate will unlock as if the original card was used. Step 5: Repeat at different times of day or from a cloned badge for persistent access. Step 6: Advanced attackers can automate this using badge-copy hardware and looped replays.
- **Detection**: Log repeated UID access attempts; track by time/location
- **Solution**: Use challenge-response-based RFID (e.g., MIFARE DESFire or iCLASS SE)
- **Tags**: RFID, Access Card, Physical Intrusion

## Smart Lock Replay

- **Attack Type**: BLE/NFC Command Replay
- **Target**: Smart Home Locks, BLE/NFC Devices
- **Vulnerability**: Lack of freshness tokens, static app commands
- **MITRE**: T1477 – Hardware Protocol Exploitation
- **Impact**: Remote or proximity-based door unlock
- **Tools**: BtleJack, GATTacker, Wireshark, Android Debug Bridge (ADB), Flipper Zero
- **Scenario**: Replay previously captured app-to-smart lock communication (BLE, Wi-Fi, or NFC) to unlock doors without authorization.
- **Attack Steps**: Step 1: Monitor Bluetooth or NFC traffic between a smartphone and a smart lock using a tool like BtleJack (for BLE), or NFC Tools Pro (for NFC locks). Step 2: Trigger a real unlock command from a paired mobile app while sniffing traffic. Save the command UUID, GATT characteristics, and raw packets. Step 3: Replay the same payload using GATTacker, ADB scripts, or hardware like Flipper Zero. Step 4: If the lock doesn’t require session binding or freshness validation, it will respond and unlock. Step 5: This works best when pairing and transmission are insecure or if the app uses static commands. Step 6: Some locks also respond to Wi-Fi-based replays where cloud API commands can be mimicked.
- **Detection**: Monitor repeated command packets or unauthorized unlock logs
- **Solution**: Use encrypted session tokens with freshness; bind command to session/device
- **Tags**: Smart Lock, BLE Replay, Physical IoT Exploit

## Vehicle Key Fob Replay

- **Attack Type**: Wireless RF Replay
- **Target**: Keyless Cars, Garage Doors, IoT Locks
- **Vulnerability**: Static code or weak rolling code implementation
- **MITRE**: T1557.001 – Wireless Sniffing
- **Impact**: Car theft, unauthorized vehicle access
- **Tools**: SDR (Software Defined Radio), HackRF, Flipper Zero, Yard Stick One
- **Scenario**: Replay of key fob signals (lock/unlock/start) captured via RF sniffer to unlock or start a vehicle without the original key.
- **Attack Steps**: Step 1: Set up an SDR device (like HackRF or Flipper Zero) to listen for RF signals in the 300–500 MHz range (typical for car fobs). Step 2: Stand near a user while they lock or unlock their vehicle. Record the RF packet that gets transmitted. Step 3: Save the waveform or decoded data. Step 4: Replay the captured signal using the same SDR device while near the target vehicle. Step 5: If the vehicle uses static codes or poor rolling code implementation, the door will unlock or engine may start. Step 6: Modern cars use rolling codes (Keeloq, etc.), so advanced attacks involve jamming + relay to block the original code and store it for replay. Step 7: Successful attacks bypass physical key requirement entirely.
- **Detection**: Log remote unlock attempts; use physical key audit logs
- **Solution**: Enforce strong rolling code (e.g., rolling + nonce); detect repeated RF patterns
- **Tags**: Vehicle Hacking, RF Replay, Remote Key Attack

## Zero-Nonce Blockchain Replay

- **Attack Type**: Cross-Chain Transaction Replay
- **Target**: Ethereum / EVM Blockchains
- **Vulnerability**: Lack of replay protection via chain ID or used nonce
- **MITRE**: T1557.002 – Replay via Alternate Path
- **Impact**: Double-spending, duplicate transactions
- **Tools**: MetaMask, Hardhat, Remix, Ganache, Tenderly
- **Scenario**: Reusing a valid blockchain transaction on another chain or fork where the nonce hasn’t been used, enabling double-spending or duplicated execution.
- **Attack Steps**: Step 1: Deploy or identify a smart contract on a testnet or forked mainnet (e.g., using Hardhat fork mode). Step 2: Prepare a valid transaction (e.g., token transfer or contract call) from your account with nonce 0. Step 3: Broadcast this transaction to Chain A (e.g., Ethereum Mainnet or testnet). Step 4: On Chain B (a fork or cloned chain), reuse the exact same transaction (including sender, nonce, and signature). Step 5: If Chain B has no record of this nonce being used, it will accept and process the transaction as new. Step 6: This allows an attacker to replay one transaction across multiple blockchains or forks, potentially causing financial discrepancies, double-spending, or logic failures in contracts. Step 7: Works best on cloned networks where nonce tracking isn’t global or smart contracts don’t verify chain ID.
- **Detection**: Compare transaction hash history across chains
- **Solution**: Use EIP-155 chain ID and require contract-side replay protection logic
- **Tags**: Blockchain, Ethereum, Fork Replay, Smart Contract Security

## SAML Token Replay

- **Attack Type**: Identity Token Replay
- **Target**: SSO-Enabled Web Apps
- **Vulnerability**: Weak SAML expiration or replay controls
- **MITRE**: T1557 – Man-in-the-Middle
- **Impact**: Session hijack, unauthorized login
- **Tools**: SAML Tracer, Burp Suite, mitmproxy, Postman
- **Scenario**: Replaying a previously captured SAML token assertion to log in as a user without credentials.
- **Attack Steps**: Step 1: Use a browser extension like SAML Tracer or intercept proxy (mitmproxy or Burp Suite) to capture SAML assertions during login to an SSO-enabled app. Step 2: After successful login, save the captured Base64 SAML assertion (the XML blob) from the HTTP POST or Redirect. Step 3: Copy and resend the same request to the Identity Provider (IdP) or Service Provider (SP) using tools like Postman or curl. Step 4: If the application does not validate assertion expiration time (NotOnOrAfter), destination audience, or replays, it will accept the old assertion. Step 5: This gives unauthorized access to the user’s session. Step 6: SAML assertions signed but not time-bound or audience-validated are most vulnerable.
- **Detection**: Analyze SAML timestamps, audience mismatch, replayed assertions
- **Solution**: Enforce strict SAML expiration validation and one-time token use
- **Tags**: SSO, SAML, Identity Replay, Token Abuse

## MQTT IoT Replay

- **Attack Type**: MQTT Publish Replay
- **Target**: Smart Home Devices, IoT Hubs
- **Vulnerability**: MQTT lacks freshness and replay validation
- **MITRE**: T1496 – Resource Hijacking
- **Impact**: IoT control manipulation, alarm bypass
- **Tools**: MQTT.fx, Mosquitto, Wireshark, Node-RED, Burp Collaborator
- **Scenario**: Attacker replays MQTT publish messages to an IoT device, re-triggering actions like door unlock, alerts, or data logging.
- **Attack Steps**: Step 1: Connect to an MQTT broker (e.g., mosquitto) and subscribe to topics being used by IoT devices (e.g., /home/lock/unlock or /device/alarm/on). Step 2: Capture and log published messages, especially those controlling hardware or cloud state. Step 3: Save one or more payloads (like JSON unlock commands). Step 4: Replay those same messages using MQTT.fx or Node-RED. Step 5: If the IoT device accepts commands without validating session or time (QoS 0, no TLS), it will perform the action again (e.g., unlock the door, trigger alarm). Step 6: Advanced attacks can be performed silently using Wi-Fi sniffers on open MQTT brokers or over unsecured TLS. Step 7: This enables repeated unauthorized access or manipulation of devices.
- **Detection**: Monitor duplicate messages on sensitive topics
- **Solution**: Use MQTT with TLS, validate session timestamps, restrict topic publishing
- **Tags**: MQTT, IoT Replay, Smart Device Exploitation

## Cloud API Key Replay

- **Attack Type**: Credential Replay
- **Target**: Public/Private Cloud APIs
- **Vulnerability**: Static API keys with no expiration or validation
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Data exfiltration, persistent cloud access
- **Tools**: curl, Postman, Wireshark, API Gateway Logs
- **Scenario**: Using a previously leaked or intercepted API key to access cloud APIs repeatedly without detection or revocation.
- **Attack Steps**: Step 1: Obtain an API key (e.g., leaked from a GitHub repo, intercepted over HTTP, or dumped from browser memory). Step 2: Use Postman or curl to issue the same API request repeatedly using the stolen key (e.g., data fetch, delete, upload). Step 3: Since most APIs do not tie keys to sessions or expiration unless explicitly configured, the key may remain valid indefinitely. Step 4: Replay the same request over time to extract data or modify cloud state. Step 5: If API lacks rate limits or IP whitelisting, this can be done silently. Step 6: Some APIs even allow admin-level access through replayed keys with elevated scopes. Step 7: Continue exploitation until key is revoked or rotated manually.
- **Detection**: Monitor API call frequency, detect IP/device anomalies
- **Solution**: Rotate keys frequently, scope them narrowly, bind to IP or short-lived tokens
- **Tags**: API Key Abuse, Cloud Security, Access Replay

## Authentication Cookie Replay

- **Attack Type**: Session Hijacking via Cookie Replay
- **Target**: Web Applications, APIs
- **Vulnerability**: Insecure cookie transmission (no HTTPS or no expiration)
- **MITRE**: T1070.006 – Indicator Removal on Host
- **Impact**: Account takeover, data theft, unauthorized access
- **Tools**: Burp Suite, Wireshark, Chrome DevTools, curl, mitmproxy
- **Scenario**: Attacker captures a valid authentication cookie from a user and reuses (replays) it to impersonate them without needing login credentials.
- **Attack Steps**: Step 1: Attacker sets up a man-in-the-middle environment using tools like Burp Suite or mitmproxy, or intercepts unsecured Wi-Fi (public hotspots). Step 2: Victim logs in to a web application over HTTP or weak HTTPS. During login, the server responds with a Set-Cookie header containing the user’s session ID (e.g., sessionid=abc123). Step 3: Attacker captures the HTTP response or request that includes this authentication cookie. Step 4: The attacker saves the session cookie value. Step 5: On their own browser or using curl/Postman, attacker crafts a request to the same site and adds the stolen cookie in the Cookie header. For example: Cookie: sessionid=abc123. Step 6: The server now sees the attacker as the original user and grants full access (bypassing username/password). Step 7: Attacker can now access the account, view sensitive data, perform actions like fund transfers, or change settings. Step 8: The replayed session may stay valid until logout, timeout, or manual session reset.
- **Detection**: Monitor for same cookie used from different IPs/devices
- **Solution**: Use HttpOnly, Secure, and SameSite flags; bind sessions to IP/device; enable 2FA
- **Tags**: Cookie Hijack, Session Replay, MITM

## CBC Mode Padding Oracle

- **Attack Type**: Classic CBC Padding Oracle
- **Target**: Web App, API, File Decryption Endpoint
- **Vulnerability**: CBC mode padding validation error leaks
- **MITRE**: T1600 – Data Decryption
- **Impact**: Full plaintext exposure, authentication bypass
- **Tools**: PadBuster, Burp Suite, Python (requests), Wireshark
- **Scenario**: Attacker decrypts encrypted messages byte-by-byte by sending modified ciphertexts and observing padding error responses from the server.
- **Attack Steps**: Step 1: Attacker identifies a system using AES (or DES) in CBC mode where encrypted data is sent from client to server (e.g., session cookies or encrypted JWTs). Step 2: They observe that when submitting tampered ciphertexts, the server responds differently if padding is valid (e.g., 200 OK) vs invalid (e.g., 500 Error). Step 3: The attacker captures a valid ciphertext and separates it into blocks (16 bytes each for AES). Step 4: They then modify the last byte of the second-to-last block (block N-1) while keeping the last block (block N) intact. Step 5: They resend the modified ciphertext and check if the padding is correct. Step 6: By adjusting bytes and observing server responses, the attacker learns valid padding values. Step 7: Using XOR math, the attacker recovers the plaintext one byte at a time. Step 8: Repeating this process across blocks allows full decryption without the key. Step 9: This is a padding oracle attack exploiting feedback from decryption errors.
- **Detection**: Analyze server error codes, HTTP responses, or timing patterns
- **Solution**: Use AEAD (authenticated encryption), ensure uniform error messages, avoid CBC
- **Tags**: AES-CBC, Oracle Attack, Byte-by-Byte Decryption

## PKCS#7 Padding Oracle

- **Attack Type**: PKCS#7-Specific Padding Oracle
- **Target**: APIs, Legacy Encrypted Tokens
- **Vulnerability**: Order of MAC/padding check leaks oracle info
- **MITRE**: T1600 – Data Decryption
- **Impact**: Plaintext recovery, user session hijack
- **Tools**: Custom Python Scripts, Wireshark, Burp Repeater
- **Scenario**: Similar to CBC oracle, but targets improper error handling in PKCS#7 padding verification—revealing whether the padding or MAC failed.
- **Attack Steps**: Step 1: Attacker finds a system encrypting data in CBC mode with PKCS#7 padding (most common scheme). Step 2: They observe that the server leaks error detail differences—for example, "Invalid Padding" vs "MAC Mismatch". Step 3: The attacker sends encrypted data, modifying it byte-by-byte (typically the IV or second-last block). Step 4: They look for which responses generate a "Padding Error", and which generate a "MAC Error" or success. Step 5: Based on response type, they infer if their byte change resulted in valid PKCS#7 padding. Step 6: Valid padding allows decryption of a byte of plaintext using XOR reversal. Step 7: Repeating the process across all bytes and blocks reveals the full original message without access to the key. Step 8: These issues usually occur when padding is checked before verifying MAC signatures.
- **Detection**: Log discrepancies in crypto failure messages
- **Solution**: MAC-then-encrypt scheme; constant-time failure handling; switch to AEAD modes
- **Tags**: PKCS#7, CBC Mode, MAC vs Padding Error

## TLS CBC Padding Oracle (POODLE)

- **Attack Type**: SSL/TLS Padding Oracle Exploitation (POODLE)
- **Target**: Web Apps using SSL 3.0 / CBC-mode TLS
- **Vulnerability**: CBC padding checked before MAC in SSL 3.0
- **MITRE**: T1557.001 – TLS Downgrade + Padding Oracle
- **Impact**: Decrypt HTTPS traffic, steal cookies
- **Tools**: SSLStrip, Wireshark, testssl.sh, POODLE.py
- **Scenario**: Exploits how SSL 3.0 and some TLS implementations process CBC-mode padding, allowing attackers to decrypt HTTPS traffic one byte at a time.
- **Attack Steps**: Step 1: Attacker positions themselves in a man-in-the-middle setup between a client and a server (e.g., in a public Wi-Fi). Step 2: They force a downgrade from TLS to SSL 3.0 using tools like SSLStrip or downgrade attacks. Step 3: Once the session uses CBC-mode SSL 3.0, attacker captures encrypted HTTPS traffic. Step 4: Attacker injects malicious JavaScript or data blocks that manipulate the ciphertext structure. Step 5: Using POODLE logic, they observe which payloads result in successful server responses vs errors (due to incorrect padding). Step 6: With repeated attempts (multiple connections), they deduce plaintext bytes byte-by-byte. Step 7: This breaks confidentiality of cookies, credentials, or sensitive API traffic. Step 8: POODLE is specific to SSL 3.0 and poorly configured TLS CBC implementations.
- **Detection**: Detect TLS downgrade attempts, analyze CBC padding anomalies
- **Solution**: Disable SSL 3.0, patch TLS CBC padding handling, use TLS 1.3 or AEAD ciphers
- **Tags**: POODLE, TLS CBC, SSL Downgrade, HTTPS Decryption

## Encrypted JWT Padding Oracle

- **Attack Type**: JWT Decryption Oracle
- **Target**: JWT-Based Auth APIs, Encrypted Sessions
- **Vulnerability**: Encrypted JWTs using CBC with poor error control
- **MITRE**: T1600 – Token Decryption Oracle
- **Impact**: Admin impersonation, privilege escalation
- **Tools**: jwt.io, Postman, Burp Suite, Python PyJWT, Wireshark
- **Scenario**: Attacker exploits encrypted JSON Web Tokens (JWE) that use AES-CBC to decrypt and modify claims by observing padding or MAC error differences.
- **Attack Steps**: Step 1: Attacker identifies that a web application uses encrypted JWTs (JWE) in Bearer headers or cookies. These use CBC-mode AES with PKCS#7 padding. Step 2: Attacker captures a valid JWE from browser requests and decodes it (though contents are still encrypted). Step 3: They modify bytes in the ciphertext part of the token and resend it to the API or server. Step 4: If the server provides detailed error messages (e.g., "Invalid Padding" vs "Signature Failed"), the attacker uses that to infer correct padding. Step 5: Using padding oracle logic, attacker decrypts part or all of the JWE token’s content (e.g., user role = "admin"). Step 6: Once decrypted, attacker may re-encrypt a forged token with "admin" role and send it back. Step 7: Server accepts the forged token if integrity checks are bypassed, giving unauthorized access. Step 8: This breaks the promise of encrypted JWTs where weak crypto handling leaks secrets.
- **Detection**: Analyze response differences, monitor malformed JWT access
- **Solution**: Use AES-GCM (AEAD) in JWT, constant-time failure response, avoid CBC-mode JWE
- **Tags**: JWT, JWE Oracle, Bearer Token Exploits

## XML Encryption Padding Oracle

- **Attack Type**: SOAP XML Padding Oracle
- **Target**: SOAP APIs, WS-Security Apps
- **Vulnerability**: CBC-mode XML encryption with padding leak
- **MITRE**: T1600 – Data Decryption
- **Impact**: Sensitive data leak (SSNs, credit card, auth tokens)
- **Tools**: SOAP-UI, Burp Suite, XMLSecTool, Wireshark
- **Scenario**: Attack decrypts sensitive XML data in SOAP/WS-Security encrypted messages by abusing padding error feedback in XML encryption validation.
- **Attack Steps**: Step 1: Attacker observes that the application or SOAP API uses encrypted XML blocks via WS-Security (e.g., EncryptedData tags in SOAP). Step 2: They capture a valid encrypted SOAP message, e.g., using Burp or Wireshark. Step 3: They start modifying one byte at a time at the end of a ciphertext block (block N-1), while keeping block N intact. Step 4: They resend the manipulated SOAP message to the server. Step 5: If the server responds with a distinct error for padding vs decryption (e.g., "Decryption failed" vs "Padding invalid"), attacker notes which inputs cause different behavior. Step 6: Using this error oracle, the attacker uses the classic padding oracle method to decrypt the message block-by-block. Step 7: With enough repetitions, they recover plaintext such as session tokens, credentials, or payment details embedded in the XML. Step 8: This is particularly dangerous if SOAP-based APIs are used in financial or healthcare systems.
- **Detection**: Analyze SOAP faults, exception traces, and response codes
- **Solution**: Use AES-GCM in WS-Security, uniform error messages, avoid CBC-mode XML encryption
- **Tags**: SOAP, XMLSec, CBC Oracle, WS-Attack

## HTTP Cookie Decryption via Oracle

- **Attack Type**: CBC Cookie Oracle Decryption
- **Target**: Web Apps with Encrypted Cookies
- **Vulnerability**: Different response on invalid padding
- **MITRE**: T1557.002 – Session Hijacking
- **Impact**: Account takeover, session impersonation
- **Tools**: PadBuster, Burp Suite, custom Python (requests), browser DevTools
- **Scenario**: A session cookie encrypted with CBC (e.g., auth=encrypted_value) can be decrypted byte-by-byte by manipulating blocks and analyzing error responses.
- **Attack Steps**: Step 1: Attacker captures an encrypted session cookie (e.g., auth=...) issued by a vulnerable web app. Step 2: They test whether the app shows different behaviors when the cookie is tampered (e.g., 403 vs 500 errors depending on padding). Step 3: The attacker isolates blocks of the encrypted cookie (each block = 16 bytes for AES-CBC). Step 4: They manipulate the last byte of the second-to-last block and resend the cookie in a request. Step 5: If valid padding occurs, the app may return a different response code. Step 6: Using the classic padding oracle attack, the attacker systematically decrypts each block by guessing valid padding bytes and applying XOR operations. Step 7: Once full plaintext is recovered, it may reveal username, role, or token. Step 8: The attacker can even re-encrypt forged cookies if IV is guessable or predictable.
- **Detection**: Compare server responses for cookie tampering
- **Solution**: Switch to HMAC + encrypted token (MAC-then-Encrypt); or use JWT with AEAD
- **Tags**: Session Cookie, CBC Oracle, Padding Hijack

## CSRF Token Oracle Attack

- **Attack Type**: CSRF Token Padding Oracle Bypass
- **Target**: Web Forms, Authenticated Panels
- **Vulnerability**: Encrypted CSRF tokens with padding errors
- **MITRE**: T1110.003 – Token Forgery
- **Impact**: CSRF bypass, account modification
- **Tools**: Burp Suite Repeater, DevTools, PadBuster, Python Scripts
- **Scenario**: Attacker forges valid CSRF tokens by manipulating encrypted CBC-mode tokens and analyzing app responses for padding errors.
- **Attack Steps**: Step 1: Attacker identifies a web application using encrypted CSRF tokens (e.g., hidden fields or headers) and notices they are in ciphertext form (likely AES-CBC). Step 2: They capture a valid CSRF token from a request. Step 3: They manipulate the ciphertext (especially block N-1) and submit the form with the forged token. Step 4: If the app responds differently based on valid or invalid tokens (e.g., "403 Forbidden" vs "Invalid token padding"), attacker uses that as an oracle. Step 5: They try values one byte at a time and record which ones yield different server behavior. Step 6: Once they decrypt the token fully, they can alter values (e.g., user_id, form_action) and re-encrypt them to forge valid tokens. Step 7: This bypasses CSRF protection entirely and allows actions like changing passwords or emails.
- **Detection**: Monitor frequent token replays and form misuse patterns
- **Solution**: Use stateless CSRF protection (double submit cookie) or signed HMACs, not encrypted values
- **Tags**: CSRF, Padding Oracle, Encrypted Forms

## Session Hijacking via Cookie Forgery

- **Attack Type**: Auth Cookie Oracle → Privilege Escalation
- **Target**: Session-Based Web Apps
- **Vulnerability**: CBC-mode session cookie without integrity checks
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Privilege escalation, dashboard takeover
- **Tools**: Burp Suite, PadBuster, CyberChef, Postman
- **Scenario**: Attacker decrypts and re-encrypts session cookies to elevate privileges (e.g., change role from user to admin) using padding oracle.
- **Attack Steps**: Step 1: Attacker logs into a demo account and obtains a session cookie that is encrypted (e.g., Set-Cookie: session=ENCRYPTED_STRING). Step 2: Using padding oracle techniques (described above), attacker decrypts the cookie byte-by-byte. Step 3: Once full plaintext is recovered, attacker observes sensitive key-value pairs like "username":"bob","role":"user". Step 4: They modify the decrypted value to set "role":"admin" and re-encrypt it using the same padding oracle in reverse (if IV and cipher logic is known). Step 5: The forged cookie is sent in a browser session. Step 6: The web app reads it and grants access to admin dashboard, bypassing normal access control. Step 7: This attack is only possible when cookies are encrypted with CBC-mode AES and decrypted insecurely without MAC protection.
- **Detection**: Compare cookie patterns from different roles; session anomalies
- **Solution**: Use AES-GCM or add HMAC to cookie value (Encrypt-then-MAC)
- **Tags**: Cookie Forgery, Auth Hijack, CBC Encryption Abuse

## Remote File Download with Oracle

- **Attack Type**: Encrypted Filename Oracle
- **Target**: Web Apps with Encrypted Download Links
- **Vulnerability**: CBC-mode parameter leaks padding vs logic error
- **MITRE**: T1600 – Data Decryption
- **Impact**: Unauthorized file access, sensitive document exposure
- **Tools**: Burp Suite, curl, custom Python (requests, XOR logic), browser dev tools
- **Scenario**: Attacker guesses filenames or content in an encrypted file download URL (e.g., download?id=ENCRYPTED) by observing differences in server error or file existence responses.
- **Attack Steps**: Step 1: Attacker finds a file download feature that uses encrypted file references (e.g., download.php?id=ENCRYPTED_STRING). Step 2: The server uses AES-CBC encryption and may leak padding or file existence differences. Step 3: Attacker captures a valid encrypted URL and modifies the last byte of the penultimate block (block N-1). Step 4: They repeatedly send modified ciphertexts and note response types — e.g., "Invalid file" vs "Decryption failed". Step 5: Using CBC padding oracle logic, attacker reveals the decrypted content of the ID byte-by-byte. Step 6: Once fully decrypted, attacker may reveal the internal file path (e.g., /secure/files/report.pdf). Step 7: With this info, attacker may forge new encrypted IDs and download other files. Step 8: This breaks confidentiality of file storage and may expose sensitive records.
- **Detection**: Log pattern of malformed download requests and analyze error type
- **Solution**: Use authenticated encryption (AEAD) and bind encrypted ID to user/session
- **Tags**: File Download, CBC Oracle, Encrypted Parameters

## Web Service Decryption (SOAP/REST)

- **Attack Type**: Oracle Decryption via Encrypted API Calls
- **Target**: SOAP/REST APIs with encrypted data
- **Vulnerability**: CBC-mode input without padding blinding
- **MITRE**: T1040 – Decrypt Network Messages
- **Impact**: API abuse, user impersonation, data leakage
- **Tools**: SOAP-UI, Postman, Wireshark, Burp Suite, Python requests
- **Scenario**: Attacker targets encrypted REST or SOAP APIs using CBC encryption to decrypt payloads like user IDs or actions using padding oracle behavior.
- **Attack Steps**: Step 1: Attacker identifies that the API uses encrypted body fields (e.g., userID, action) in CBC-mode (e.g., in a <User> XML or JSON blob). Step 2: They capture a valid encrypted API request. Step 3: They begin manipulating the ciphertext, starting from block N-1 to modify the adjacent block N. Step 4: Attacker repeatedly sends manipulated requests to the API and observes differences: for example, “Invalid Padding” vs “User Not Found”. Step 5: These subtle differences reveal which bytes yield valid padding. Step 6: Using byte-by-byte padding oracle logic, attacker decrypts full message payloads like user identity or request type. Step 7: With decrypted data, they can impersonate other users or craft custom encrypted requests for unauthorized actions.
- **Detection**: Look for abnormal repeated API calls with malformed inputs
- **Solution**: Use constant-time error responses; AES-GCM or secure channels with mutual TLS
- **Tags**: API Oracle, CBC REST Decryption, SOAP API Exploits

## Padding Oracle in CMS Systems

- **Attack Type**: CMS Encrypted Cookie Exploit
- **Target**: CMS Platforms (Joomla, Drupal, etc.)
- **Vulnerability**: Insecure encrypted cookie handling
- **MITRE**: T1557 – Session Hijack / Role Escalation
- **Impact**: Admin panel takeover, website defacement
- **Tools**: Joomla/JCE plugin, Drupal exploit kits, Burp Suite, PadBuster
- **Scenario**: Padding oracle exploit targeting Joomla, Drupal, or custom CMSs that use encrypted cookies or tokens to store user info.
- **Attack Steps**: Step 1: Attacker signs up or accesses a low-privilege account on a CMS like Joomla or Drupal that issues encrypted cookies/tokens with role info (e.g., auth_token=ENCRYPTED). Step 2: They capture the encrypted token/cookie using browser dev tools. Step 3: By manipulating bytes in block N-1, attacker sends the modified token to the server. Step 4: If server responds differently to malformed vs valid tokens (e.g., “Invalid Padding” vs redirect), this acts as a padding oracle. Step 5: Using standard padding oracle techniques, attacker decrypts the full token to read values like "username":"guest","role":"user". Step 6: They alter decrypted values to elevate role (e.g., "role":"admin"), re-encrypt the forged token, and resend it. Step 7: The CMS accepts it and grants access to the admin panel. Step 8: If no MAC or signature is used, attacker can maintain persistent access.
- **Detection**: Look for cookies reused across sessions or weird token replays
- **Solution**: Use signed tokens (JWT with HMAC); do not encrypt role data unless authenticated
- **Tags**: CMS, CBC Cookie, Role Escalation

## Encrypted SAML Assertion Attack

- **Attack Type**: CBC Oracle in Federated Auth Tokens
- **Target**: Federated Login Systems (SSO, SAML)
- **Vulnerability**: SAML assertions encrypted with CBC and no HMAC
- **MITRE**: T1600 + T1606.003 – Token Forgery
- **Impact**: User impersonation, SSO compromise
- **Tools**: SAML Tracer, Burp Suite, Samlify, XMLSecTool, Wireshark
- **Scenario**: Exploits CBC-encrypted SAML assertions passed between identity providers and service providers by observing padding error behavior.
- **Attack Steps**: Step 1: Attacker captures a SAML Assertion from a federated login flow (e.g., using SAML Tracer browser plugin or Burp Suite). These are often base64-encoded XML documents containing encrypted elements. Step 2: They decode the base64-encoded string and analyze the ciphertext. Step 3: Attacker manipulates one byte at a time in a CBC-encrypted block and resends it through the federated login process. Step 4: If the service provider returns different error messages (e.g., “Decryption failed” vs “Signature invalid”), the attacker uses this as a padding oracle. Step 5: Using oracle logic, attacker decrypts the SAML payload, revealing assertions like username, role, or organization. Step 6: In some cases, attacker can forge or replay assertions to login as other users if signature checks are bypassed. Step 7: This attack breaks SSO systems if proper encryption/signature separation isn't followed.
- **Detection**: Monitor for frequent login failures on modified SAMLs
- **Solution**: Always sign + encrypt SAML; use AES-GCM and strict XML signature validation
- **Tags**: SAML Assertion, SSO Abuse, Federated Oracle Exploit

## Oracle via Timing Side-Channel

- **Attack Type**: Timing-Based Padding Oracle
- **Target**: Web Apps, APIs with uniform error responses
- **Vulnerability**: CBC-mode + early return on padding failure
- **MITRE**: T1201 – Timing Side Channel
- **Impact**: Information disclosure, token forgery
- **Tools**: curl, time command, Python with requests and time, Burp Suite with timer
- **Scenario**: Exploits differences in server response times to infer padding correctness — even if responses are identical in content.
- **Attack Steps**: Step 1: Attacker finds a web app or API that uses CBC encryption (e.g., encrypted cookies, tokens, or parameters). The app doesn’t give different error messages but takes slightly longer to respond if the padding is valid. Step 2: The attacker captures a valid encrypted token. Step 3: They write a script that sends modified tokens by changing the last byte of a CBC block and measuring response time precisely (e.g., using time module in Python). Step 4: When padding is valid, the server spends extra time verifying HMAC, reading user info, etc., causing a longer response time. Invalid padding fails fast. Step 5: The attacker uses statistical averaging over multiple requests to distinguish valid vs invalid padding guesses. Step 6: They repeat this byte-by-byte to decrypt the entire ciphertext. Step 7: Using the decrypted token or cookie, attacker may forge a new one with elevated privileges.
- **Detection**: Analyze timing variance across requests (especially malformed ones)
- **Solution**: Ensure constant-time decryption paths; reject all malformed tokens uniformly
- **Tags**: Timing Oracle, Padding Attack, CBC Tokens

## JWT Auth Replay via Padding Oracle

- **Attack Type**: Encrypted JWT Oracle Abuse
- **Target**: Web Apps using encrypted JWTs (not signed)
- **Vulnerability**: CBC-mode JWT without HMAC or signature validation
- **MITRE**: T1557.002 – Token Replay
- **Impact**: Privilege escalation, session takeover
- **Tools**: Burp Suite, JWT Debugger, jwt.io, PadBuster, browser DevTools
- **Scenario**: Exploits CBC-encrypted JWTs (vs signed ones) to decrypt and replay/forge authentication tokens.
- **Attack Steps**: Step 1: Attacker finds an application using encrypted (not signed) JWTs for authentication or session management. The JWT payload appears as gibberish (e.g., AES-CBC encrypted base64). Step 2: They capture a valid JWT token (e.g., from the Authorization header). Step 3: They begin modifying one byte at a time in the previous block (Block N-1) of the encrypted JWT and send requests with modified tokens. Step 4: If server returns different responses based on padding validity, attacker uses this feedback as an oracle. Step 5: Using padding oracle logic, they decrypt the JWT payload to reveal claims like sub, role, or user_id. Step 6: Once decrypted, attacker modifies the payload to forge elevated privileges (e.g., admin) and re-encrypts it if possible. Step 7: They replay the forged JWT token to access admin features or other user accounts.
- **Detection**: Compare JWT replays and validate claims integrity
- **Solution**: Use signed JWT (RS256/HMAC) instead of encrypted JWTs, apply token expiration policies
- **Tags**: JWT Oracle, Auth Token Abuse, CBC Token Reuse

## Encrypted Query Param Manipulation

- **Attack Type**: Oracle via Encrypted GET Parameters
- **Target**: Web apps using encrypted URLs or GET params
- **Vulnerability**: CBC-mode encrypted query param with feedback
- **MITRE**: T1557 – Input Tampering
- **Impact**: Data leakage or privilege bypass using encrypted URLs
- **Tools**: Burp Suite, Python requests, URL decoder/encoder, CyberChef
- **Scenario**: Encrypted query parameters in URLs are modified byte-by-byte using padding oracle to decrypt or forge input (e.g., ?q=ENCRYPTED).
- **Attack Steps**: Step 1: Attacker finds a URL with an encrypted parameter, such as https://example.com/search?q=ENCRYPTED_STRING. The q parameter likely contains search term, user ID, or role encrypted using CBC. Step 2: They capture the ciphertext and break it into 16-byte blocks (if AES-CBC is used). Step 3: They modify the last byte of the second-to-last block and encode the modified query string back into the URL. Step 4: They send the modified request and observe response types — if padding is correct, app might process further and return a “not found” or partial result; if not, it errors out. Step 5: They repeat this for every byte and use padding oracle logic to reveal the plaintext of the query parameter. Step 6: Once full plaintext is known (e.g., "role=user"), attacker changes it to "role=admin" and re-encrypts it (if IV is predictable or known). Step 7: Replaying forged URLs gives unauthorized access to restricted data or actions.
- **Detection**: Monitor malformed encrypted query requests
- **Solution**: Avoid using encrypted GET params; use HMAC or switch to POST with secure session ID
- **Tags**: Encrypted URL Exploit, CBC GET Forgery

## MAC-then-Encrypt Oracle

- **Attack Type**: Oracle via MAC-then-Encrypt Validation Timing
- **Target**: Any system using MAC-then-Encrypt (not AEAD)
- **Vulnerability**: Use of MtE + CBC with no timing protection
- **MITRE**: T1600 – Cryptographic Message Decryption
- **Impact**: Secret leakage, token manipulation, message forgery
- **Tools**: Python with hmac, Burp Suite, Postman, CyberChef
- **Scenario**: Applications that encrypt HMAC’d data (instead of HMAC’ing ciphertext) may leak MAC correctness via timing or padding error behavior.
- **Attack Steps**: Step 1: Attacker identifies a system using MAC-then-Encrypt (MtE), meaning the message is HMAC’d and then the full result is encrypted using CBC. Step 2: The system decrypts the ciphertext first, then verifies the MAC in plaintext. Step 3: Attacker captures a valid encrypted token, file, or message. Step 4: They modify bytes in the second-to-last block and replay the message. Step 5: If padding is wrong, the app errors early. If padding is valid but MAC fails, app may return a slightly different message or take longer to respond. Step 6: Attacker uses this difference in behavior or timing to determine which values produced valid padding. Step 7: They repeat this process block-by-block to recover the plaintext, including the embedded MAC. Step 8: This approach allows full plaintext recovery even without knowing the MAC key — a classic weakness of MAC-then-Encrypt.
- **Detection**: Time behavior variance and MAC mismatch logs
- **Solution**: Switch to Encrypt-then-MAC or authenticated encryption (e.g., AES-GCM or ChaCha20-Poly1305)
- **Tags**: MAC-then-Encrypt Flaw, CBC, Timing Oracle

## Encrypted CSRF in Mobile APIs

- **Attack Type**: Oracle on Encrypted CSRF Tokens
- **Target**: Mobile APIs, Encrypted API tokens
- **Vulnerability**: Encrypted CSRF tokens leak padding correctness
- **MITRE**: T1557 – Input Manipulation
- **Impact**: API misuse, unauthorized actions
- **Tools**: Burp Suite Mobile Proxy, Frida, Charles Proxy, Python requests
- **Scenario**: Mobile apps use encrypted CSRF tokens in API calls (e.g., POST/PUT), which leak padding correctness via subtle error messages or timings, enabling token forgery.
- **Attack Steps**: Step 1: Attacker intercepts mobile API traffic using proxy tools (e.g., Burp Mobile Proxy). They identify encrypted CSRF tokens in request headers or bodies (often AES-CBC). Step 2: Capture a valid encrypted CSRF token sent with API calls. Step 3: Modify the ciphertext blocks byte-by-byte, especially the second last block, and resend the request. Step 4: Observe server responses for subtle differences like error codes, timings, or behavior (e.g., 403 Forbidden vs 400 Bad Request). These differences reveal valid/invalid padding. Step 5: Use padding oracle logic to decrypt the CSRF token payload byte-by-byte. Step 6: With decrypted tokens, attacker can forge valid CSRF tokens and perform unauthorized state-changing API actions (e.g., fund transfers, account changes). Step 7: This breaks the CSRF protection and allows API misuse or privilege escalation.
- **Detection**: Monitor for repeated API failures or anomalies with invalid tokens
- **Solution**: Use signed tokens; AEAD encryption modes (AES-GCM); avoid predictable tokens
- **Tags**: Mobile Security, CSRF, API Oracle

## Oracle via HTTP 500/403 Response Codes

- **Attack Type**: Oracle via Differing HTTP Status Codes
- **Target**: Web Apps with encrypted inputs/tokens
- **Vulnerability**: HTTP error code leak on padding validation
- **MITRE**: T1557 – Input Validation
- **Impact**: Token forgery, data leakage
- **Tools**: Burp Suite, curl, Postman, Fiddler
- **Scenario**: Server returns HTTP 500 for padding errors and 403/400 for other validation errors, leaking padding correctness via HTTP codes.
- **Attack Steps**: Step 1: Attacker identifies a web application that uses encrypted parameters or tokens validated on server-side. Step 2: They notice server returns HTTP 500 Internal Server Error on padding failure but HTTP 403 Forbidden or 400 Bad Request for other errors. Step 3: Capture a valid ciphertext/token and modify one byte in the penultimate block. Step 4: Send the modified ciphertext to the server and observe the HTTP response code. Step 5: If HTTP 500, padding was invalid; if 403 or 400, padding was valid but some other validation failed. Step 6: Using this oracle, attacker iteratively modifies ciphertext bytes and narrows down valid padding bytes byte-by-byte. Step 7: After recovering full plaintext, attacker may forge tokens or manipulate encrypted inputs.
- **Detection**: Monitor unusual spikes in HTTP 500 vs 403 responses in encrypted endpoints
- **Solution**: Normalize error codes; send generic error messages; consistent error handling
- **Tags**: HTTP Error Oracle, Padding Oracle, Status Code Leak

## Padding Oracle over UDP

- **Attack Type**: Oracle via UDP Error Responses
- **Target**: UDP Encrypted Protocols (VPN, DNS, IoT)
- **Vulnerability**: Detailed error codes on UDP responses
- **MITRE**: T1201 – Network Traffic Decryption
- **Impact**: Decryption of encrypted UDP payloads, replay attacks
- **Tools**: Wireshark, Scapy, custom UDP fuzzers
- **Scenario**: UDP-based protocols returning detailed error codes (e.g., 0x01 padding fail vs 0x02 MAC fail) enable padding oracle even over unreliable transport.
- **Attack Steps**: Step 1: Attacker targets a UDP-based encrypted protocol (e.g., IPsec, DNS-over-HTTPS, custom VPN). Step 2: They observe that the UDP server responds with distinct error codes for padding vs MAC errors, despite UDP’s unreliable nature. Step 3: Attacker sends crafted UDP packets with modified ciphertext bytes and captures responses. Step 4: By analyzing which error code returns, attacker determines valid padding guesses. Step 5: Due to UDP’s unreliability, attacker repeats packets multiple times for statistical accuracy. Step 6: Using this oracle, attacker decrypts ciphertext block-by-block and byte-by-byte. Step 7: Once decrypted, attacker can replay, manipulate, or forge encrypted UDP messages.
- **Detection**: Monitor UDP error codes frequency and anomalies
- **Solution**: Use authenticated encryption (AEAD) and uniform error messages
- **Tags**: UDP Oracle, Encrypted UDP Traffic

## Composite Oracle (Padding + Compression)

- **Attack Type**: Combined Padding Oracle + Compression Leak
- **Target**: HTTP(S) Web apps with compression + encryption
- **Vulnerability**: Compression before encryption + padding oracle leaks
- **MITRE**: T1552 – Data from Information Repositories
- **Impact**: Secret leakage, session hijack
- **Tools**: Burp Suite, Zlib, Python, Wireshark
- **Scenario**: Attack leverages padding oracle leaks combined with compression side-channels (CRIME/BREACH style) to recover encrypted secrets.
- **Attack Steps**: Step 1: Attacker identifies an application using compressed and then encrypted HTTP responses or tokens (e.g., compress-then-encrypt or encrypt-then-compress misconfigurations). Step 2: They capture encrypted compressed data like cookies or tokens. Step 3: By sending modified ciphertexts, attacker uses padding oracle leaks to test correctness of guesses byte-by-byte. Step 4: At the same time, they observe the size of compressed responses — small variations leak info about plaintext bytes (compression side-channel). Step 5: Combining padding oracle feedback with compression length differences, attacker statistically recovers secrets (e.g., CSRF tokens, session IDs). Step 6: Attacker repeats this over multiple requests, refining guesses until full secret is decrypted. Step 7: Exploitation leads to full token forgery and session hijacking.
- **Detection**: Analyze response size variability correlated with errors
- **Solution**: Avoid compress-then-encrypt; prefer AEAD ciphers; disable compression for secrets
- **Tags**: Composite Oracle, CRIME, BREACH, Padding Oracle

## Classic Bleichenbacher RSA PKCS#1 v1.5 Oracle Attack

- **Attack Type**: Padding Oracle Exploit on RSA PKCS#1 v1.5
- **Target**: TLS/SSL servers using RSA PKCS#1 v1.5 encryption
- **Vulnerability**: Padding oracle leak in RSA implementations
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Data disclosure, key recovery
- **Tools**: OpenSSL, Wireshark, Burp Suite, Python scripts
- **Scenario**: Attacker exploits differences in server error responses when RSA ciphertexts have incorrect padding to decrypt messages.
- **Attack Steps**: Step 1: Attacker captures an RSA-encrypted message/ciphertext sent to the server (e.g., SSL handshake, encrypted session key). Step 2: The attacker submits the captured ciphertext to the server and observes whether the padding is accepted or rejected based on error messages or timing. Step 3: Using this oracle, attacker modifies the ciphertext by multiplying it with a chosen value modulo RSA modulus and sends it again. Step 4: By repeating this adaptive querying and observing padding validity, the attacker gradually narrows the range of the plaintext message. Step 5: This iterative process continues until the attacker fully recovers the original plaintext without the private key. Step 6: The attacker can now decrypt sensitive data or impersonate users.
- **Detection**: Monitor error messages for padding failures; anomaly detection for malformed ciphertexts
- **Solution**: Migrate to RSA-OAEP padding; implement constant-time padding checks; patch TLS libraries
- **Tags**: RSA Oracle, PKCS#1 v1.5, Padding Oracle

## Oracle-based Adaptive Attack

- **Attack Type**: Iterative Oracle Queries to Narrow Plaintext
- **Target**: RSA-based encrypted systems
- **Vulnerability**: RSA padding oracle allowing adaptive queries
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Secret key or plaintext recovery
- **Tools**: Python scripts, Burp Suite, OpenSSL
- **Scenario**: A refined attack that repeatedly queries the oracle to iteratively narrow plaintext range until full decryption is achieved.
- **Attack Steps**: Step 1: Starting with an intercepted ciphertext, attacker initializes a search interval for the possible plaintext space. Step 2: The attacker picks a multiplier s and modifies the ciphertext to c' = (c * s^e) mod n and sends it to the oracle. Step 3: Oracle response indicates whether padding is valid or invalid. Step 4: If valid, attacker uses the multiplier to update the interval bounds narrowing down the plaintext. Step 5: This process is repeated, carefully selecting s values to converge on the exact plaintext value. Step 6: After sufficient iterations, the attacker fully recovers the plaintext without decrypting the ciphertext traditionally. Step 7: The recovered plaintext can contain session keys, passwords, or sensitive tokens.
- **Detection**: Detect repeated invalid padding requests; monitor query rates to crypto services
- **Solution**: Use secure padding schemes (RSA-OAEP); rate-limit oracle queries; enforce uniform errors
- **Tags**: Adaptive Oracle, RSA Attack, Ciphertext Manipulation

## TLS Bleichenbacher Attack

- **Attack Type**: RSA PKCS#1 v1.5 Oracle Exploit in TLS
- **Target**: TLS servers using RSA PKCS#1 v1.5
- **Vulnerability**: Oracle vulnerability in TLS RSA key exchange
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Session key compromise; traffic decryption
- **Tools**: Wireshark, OpenSSL test tools, Burp Suite, TLS libraries
- **Scenario**: Exploits RSA key exchange in TLS handshakes with PKCS#1 v1.5 padding; famous variants include Lucky Thirteen and ROBOT attacks.
- **Attack Steps**: Step 1: Attacker intercepts an active TLS handshake using RSA key exchange with PKCS#1 v1.5 padding. Step 2: They replay or modify the encrypted premaster secret and send it to the server. Step 3: Server’s error messages or timing differences reveal if padding is correct. Step 4: Attacker uses adaptive oracle techniques to gradually decrypt the premaster secret used for session key derivation. Step 5: Once the premaster secret is known, attacker decrypts session traffic or impersonates users. Step 6: Variants like Lucky Thirteen leverage timing side-channels; ROBOT exploits improper error handling in TLS libraries. Step 7: The attack requires numerous handshake attempts and is typically mitigated in modern TLS versions.
- **Detection**: Monitor handshake error patterns; TLS anomaly detection
- **Solution**: Use ephemeral Diffie-Hellman key exchange; upgrade to TLS 1.3; patch TLS libraries
- **Tags**: TLS Oracle, ROBOT, Lucky Thirteen

## SSL Bleichenbacher Attack

- **Attack Type**: Classic RSA Padding Oracle on SSL
- **Target**: SSLv3 or TLS 1.0 servers
- **Vulnerability**: Padding oracle vulnerability in legacy SSL/TLS
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Session hijacking; traffic decryption
- **Tools**: OpenSSL, SSL test suites, Burp Suite
- **Scenario**: Exploits padding oracle weaknesses in SSLv3/TLS 1.0 implementations using RSA PKCS#1 v1.5 for key exchange.
- **Attack Steps**: Step 1: Attacker captures SSL handshake encrypted premaster secret. Step 2: Sends modified ciphertext to server during handshake. Step 3: Observes server’s error or behavior indicating padding validity. Step 4: Performs iterative adaptive querying, multiplying ciphertexts and narrowing plaintext range. Step 5: Fully recovers premaster secret to decrypt SSL session traffic. Step 6: This attack helped demonstrate insecurity of older SSL/TLS versions and led to patching and migration to safer protocols.
- **Detection**: Detect abnormal handshake failures; monitor TLS version usage
- **Solution**: Disable SSLv3/TLS 1.0; prefer TLS 1.2+ with secure ciphers
- **Tags**: SSL Oracle, RSA Padding Attack

## ROBOT (Return Of Bleichenbacher’s Oracle Threat)

- **Attack Type**: Modern TLS RSA PKCS#1 v1.5 Padding Oracle
- **Target**: TLS Servers (TLS 1.2 or older)
- **Vulnerability**: RSA PKCS#1 v1.5 padding oracle
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Session key compromise; full TLS decryption
- **Tools**: TLS test tools (e.g., testssl.sh), Burp Suite, Wireshark, Python scripts
- **Scenario**: A modern, practical padding oracle attack against TLS servers still supporting RSA key exchange with PKCS#1 v1.5, exploiting subtle oracle leaks.
- **Attack Steps**: Step 1: Identify TLS servers supporting RSA key exchange with PKCS#1 v1.5 padding (commonly TLS 1.2 or older). Step 2: Capture the encrypted premaster secret during a TLS handshake. Step 3: Send modified versions of the captured ciphertext to the server and observe responses (timeouts, error messages, or connection resets) as an oracle indicating padding validity. Step 4: Using automated scripts, iteratively modify ciphertext blocks and monitor oracle feedback to narrow down valid padding bytes. Step 5: Gradually recover the premaster secret byte-by-byte through adaptive querying, without access to private key. Step 6: Decrypt the TLS session and potentially impersonate clients or decrypt traffic. Step 7: Use mitigations like restricting RSA support or patching TLS libraries to prevent exploitation.
- **Detection**: Detect TLS handshake anomalies; monitor RSA usage and error patterns
- **Solution**: Disable RSA key exchange; upgrade to TLS 1.3; patch TLS libraries
- **Tags**: ROBOT, TLS Oracle, RSA Padding Attack

## Bleichenbacher Padding Oracle in S/MIME

- **Attack Type**: Oracle Attack on RSA PKCS#1 v1.5 in Emails
- **Target**: Email clients/gateways using S/MIME
- **Vulnerability**: RSA PKCS#1 v1.5 padding oracle in email encryption
- **MITRE**: T1552 – Data from Information Repositories
- **Impact**: Email content disclosure; signature forgery
- **Tools**: Email clients (e.g., Outlook), OpenSSL, Wireshark
- **Scenario**: Exploits RSA PKCS#1 v1.5 padding oracle in S/MIME encrypted emails to decrypt messages or forge signatures.
- **Attack Steps**: Step 1: Attacker intercepts an encrypted S/MIME email message encrypted with RSA PKCS#1 v1.5 padding. Step 2: Sends modified ciphertext blocks to the S/MIME processing client or gateway. Step 3: Observes whether the client accepts or rejects the message based on padding correctness (via error dialogs or log entries). Step 4: Uses adaptive querying to iteratively narrow down plaintext byte values by changing ciphertext multipliers and observing acceptance/rejection. Step 5: After sufficient queries, fully decrypts the email content or forges signatures. Step 6: Gains access to confidential email data or can impersonate the sender.
- **Detection**: Monitor email client error logs for padding failures; audit S/MIME processing behaviors
- **Solution**: Upgrade to RSA-OAEP for email encryption; patch mail clients to uniform error handling
- **Tags**: S/MIME Oracle, Email Decryption Attack

## Bleichenbacher Attack on XML Encryption

- **Attack Type**: Oracle on RSA Encrypted Keys in XML Signatures
- **Target**: Web services using XML Encryption
- **Vulnerability**: RSA PKCS#1 v1.5 padding oracle in XML encryption
- **MITRE**: T1552 – Data from Information Repositories
- **Impact**: Confidentiality and integrity compromise
- **Tools**: XML tools, Burp Suite, SOAP UI, Wireshark
- **Scenario**: Attacker exploits padding oracle leaks in XML Encryption using RSA PKCS#1 v1.5 to decrypt session keys or signatures.
- **Attack Steps**: Step 1: Identify an XML web service using RSA PKCS#1 v1.5 for encrypting keys in XML Encryption or XML Signature. Step 2: Capture an encrypted key element (ciphertext) from the XML payload. Step 3: Modify ciphertext blocks and resend the XML to the service. Step 4: Observe server’s response or SOAP faults indicating valid or invalid padding. Step 5: Use adaptive querying to narrow the plaintext range of the encrypted key byte-by-byte. Step 6: Once the session or signing key is recovered, attacker can decrypt XML messages or forge digital signatures. Step 7: This compromises confidentiality and integrity of XML-based communications.
- **Detection**: Monitor SOAP fault patterns and error responses for padding clues
- **Solution**: Use RSA-OAEP or modern key wrapping schemes; patch XML libraries
- **Tags**: XML Oracle, RSA Attack, SOAP Exploit

## PKCS#1 v1.5 Padding Oracle in Smart Cards

- **Attack Type**: Hardware Padding Oracle on RSA in Smart Cards
- **Target**: Smart cards, Hardware Security Modules
- **Vulnerability**: Timing and padding oracle on RSA PKCS#1 v1.5
- **MITRE**: T1600 – Cryptographic Key Extraction
- **Impact**: Private key compromise; full device cloning
- **Tools**: Smart card readers, ChipWhisperer, timing analysis tools
- **Scenario**: Exploits timing or error differences in smart cards performing RSA decryption with PKCS#1 v1.5 padding to extract private keys.
- **Attack Steps**: Step 1: Attacker interacts with a smart card performing RSA PKCS#1 v1.5 decryptions (e.g., for digital signatures or authentication). Step 2: Sends carefully crafted ciphertexts and measures smart card’s response times or error messages. Step 3: Differences in decryption time or error codes reveal if padding was valid. Step 4: Uses adaptive querying, modifying ciphertexts to gradually learn plaintext bytes and deduce private key bits. Step 5: Combining side-channel timing info with padding oracle leaks, attacker reconstructs the full private key. Step 6: Once private key is recovered, attacker can clone the card, forge signatures, or impersonate the user. Step 7: Countermeasures include constant-time padding checks and hardware mitigations.
- **Detection**: Monitor timing side-channel anomalies; enforce rate limiting on operations
- **Solution**: Implement constant-time crypto routines; use RSA-OAEP; shield hardware side-channels
- **Tags**: Smart Card Oracle, Hardware Crypto Attack

## Oracle Attack on SSH RSA Key Exchange

- **Attack Type**: Padding Oracle in SSH RSA Key Exchange
- **Target**: SSH servers using RSA key exchange
- **Vulnerability**: RSA PKCS#1 v1.5 padding oracle leak
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Session key compromise; unauthorized SSH access
- **Tools**: OpenSSH debug logs, Wireshark, custom scripts
- **Scenario**: Exploits RSA PKCS#1 v1.5 padding oracle leaks during SSH handshake key exchange to decrypt session keys or impersonate clients.
- **Attack Steps**: Step 1: Attacker captures RSA-encrypted session key during SSH handshake. Step 2: Sends modified ciphertexts back to SSH server in handshake attempts. Step 3: Observes server responses for differences (error messages, disconnects, timing) indicating padding validity. Step 4: Uses these oracle responses to iteratively modify ciphertext bytes and narrow plaintext possibilities. Step 5: Through repeated queries, attacker recovers the plaintext session key without the private key. Step 6: With session key known, attacker decrypts SSH traffic or impersonates clients. Step 7: Attack requires many handshake attempts; defenses include disabling RSA key exchange or padding oracle leaks in SSH server implementations.
- **Detection**: Monitor SSH handshake errors and anomalies; audit error messaging patterns
- **Solution**: Disable RSA key exchange in SSH; patch OpenSSH for uniform error handling
- **Tags**: SSH Oracle, RSA Key Exchange Attack

## Bleichenbacher Timing Attack

- **Attack Type**: Timing Side-Channel as Padding Oracle Indicator
- **Target**: RSA decryption services and devices
- **Vulnerability**: Timing side-channel leaks on RSA PKCS#1 v1.5 padding
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Data leakage without explicit oracle errors
- **Tools**: Timing analysis tools, ChipWhisperer, Wireshark
- **Scenario**: Uses subtle timing differences in RSA decryption to infer padding validity and decrypt ciphertexts without explicit error messages.
- **Attack Steps**: Step 1: Attacker sends RSA ciphertexts to a target server or device performing RSA PKCS#1 v1.5 decryption. Step 2: Measures response time for each decryption attempt with high precision. Step 3: Detects that valid padding attempts take different time than invalid padding due to conditional branches or error handling. Step 4: Uses timing oracle to classify ciphertext validity without explicit error messages. Step 5: Applies adaptive querying to iteratively narrow plaintext byte values by correlating timing differences with padding correctness. Step 6: After many measurements and statistical analysis, fully recovers plaintext message. Step 7: Enables decryption of sensitive data or session keys without needing explicit padding errors, bypassing some mitigations.
- **Detection**: Monitor timing anomalies; use constant-time crypto implementations
- **Solution**: Use constant-time crypto; add random delays; migrate to RSA-OAEP padding
- **Tags**: Timing Oracle, Side-Channel Attack

## Bleichenbacher Attack combined with Bleichenbacher’s Chosen Ciphertext Attack

- **Attack Type**: Hybrid Adaptive and Chosen Ciphertext Oracle Attack
- **Target**: RSA encryption systems
- **Vulnerability**: Padding oracle with chosen ciphertext acceptance
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Faster or stealthier plaintext/key recovery
- **Tools**: Custom scripts, OpenSSL, Burp Suite
- **Scenario**: Combines adaptive querying oracle with chosen ciphertext techniques to amplify attack efficiency and bypass protections.
- **Attack Steps**: Step 1: Attacker obtains access to an oracle that responds to ciphertext validity and accepts chosen ciphertexts for decryption. Step 2: Uses Bleichenbacher adaptive queries to iteratively refine plaintext intervals. Step 3: Employs chosen ciphertext queries to inject crafted ciphertexts exploiting oracle responses in complex ways (e.g., invalid ciphertexts accepted, chaining errors). Step 4: Amplifies oracle information to recover plaintext or keys faster and with fewer queries. Step 5: Exploits gaps in server validation or error handling to bypass mitigations that prevent basic oracle attacks. Step 6: Can lead to full plaintext/key recovery in scenarios previously considered safe.
- **Detection**: Monitor unusual ciphertext acceptance or oracle query patterns
- **Solution**: Disallow chosen ciphertext decryption; patch oracle leaks; use RSA-OAEP
- **Tags**: Hybrid Oracle Attack, Chosen Ciphertext Attack

## Multi-Protocol Bleichenbacher Exploits

- **Attack Type**: Cross-Protocol Oracle Attacks Using RSA Padding Oracle
- **Target**: Multi-protocol systems with RSA PKCS#1 v1.5
- **Vulnerability**: Cross-protocol padding oracle leaks
- **MITRE**: T1552 – Data from Information Repositories
- **Impact**: Cross-protocol key recovery; data leakage
- **Tools**: Burp Suite, Wireshark, Protocol fuzzers
- **Scenario**: Leverages RSA padding oracle leaks across multiple protocols (e.g., TLS, S/MIME, XML Encryption) to recover keys or plaintext.
- **Attack Steps**: Step 1: Attacker identifies multiple protocols on a target system using RSA PKCS#1 v1.5 padding (e.g., TLS and email encryption). Step 2: Collects ciphertexts from different protocols but same RSA keys. Step 3: Uses oracle queries from one protocol to gain oracle responses that leak padding info relevant to others. Step 4: Combines oracle data cross-protocol to accelerate plaintext or key recovery. Step 5: Exploits server implementations sharing key material or common libraries vulnerable across protocols. Step 6: This cross-protocol leakage amplifies risk, enabling attacks even if individual protocol oracle is limited or mitigated. Step 7: After recovery, attacker decrypts traffic or forges messages in multiple protocols.
- **Detection**: Monitor cross-protocol traffic and oracle queries; audit shared cryptographic keys
- **Solution**: Use distinct keys per protocol; migrate all to RSA-OAEP; patch all protocol implementations
- **Tags**: Cross-Protocol Oracle, Multi-Protocol Attack

## TLS 1.2 RSA Bleichenbacher with Side-channel Leakage

- **Attack Type**: Padding Oracle + Side-Channel Hybrid Attack
- **Target**: TLS 1.2 servers using RSA PKCS#1 v1.5
- **Vulnerability**: Oracle + side-channel leakage on RSA padding
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Session key compromise; TLS traffic decryption
- **Tools**: TLS test suites, timing analyzers, cache probes
- **Scenario**: Combines classical Bleichenbacher oracle responses with timing or cache side-channels to speed up or enable attacks on TLS 1.2.
- **Attack Steps**: Step 1: Attacker captures encrypted premaster secrets during TLS 1.2 handshake using RSA PKCS#1 v1.5 padding. Step 2: Sends modified ciphertexts to the server and monitors classical padding oracle responses (error messages, alerts). Step 3: Simultaneously performs timing or cache side-channel analysis to gather additional info about RSA decryption internals. Step 4: Combines oracle feedback with side-channel leakage to reduce the number of queries and improve plaintext recovery speed. Step 5: Iteratively narrows plaintext guesses by adaptive queries enhanced with side-channel data. Step 6: Fully recovers premaster secret, enabling decryption of TLS traffic or impersonation of clients. Step 7: Attack exploits implementation flaws leaking both oracle info and side-channel data.
- **Detection**: Monitor error patterns and timing anomalies; side-channel detection
- **Solution**: Disable RSA key exchange; patch TLS libraries; implement constant-time RSA
- **Tags**: TLS Hybrid Oracle, Side-Channel Attack

## Blind Bleichenbacher Attack

- **Attack Type**: Indirect or Noisy Oracle Responses
- **Target**: RSA PKCS#1 v1.5 systems
- **Vulnerability**: Noisy or indirect padding oracle leakage
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Data disclosure despite mitigations
- **Tools**: Statistical analysis tools, Python scripts
- **Scenario**: Attacker uses statistical methods when oracle feedback is noisy, indirect, or partially obscured, e.g., network delays.
- **Attack Steps**: Step 1: Attacker sends ciphertexts to a server with a noisy or delayed oracle response that doesn't clearly indicate padding validity. Step 2: Collects large numbers of responses and measures indirect indicators such as response time, error rates, or subtle differences. Step 3: Applies statistical inference methods (e.g., Bayesian analysis) to classify ciphertexts as likely valid or invalid padding. Step 4: Uses these probabilistic oracle results to iteratively refine guesses about plaintext values. Step 5: After sufficient queries and analysis, recovers plaintext with high confidence despite noisy feedback. Step 6: Attack requires more queries and computation but bypasses mitigations hiding explicit oracle errors. Step 7: Enables decrypting RSA-encrypted data even in hardened environments.
- **Detection**: Monitor statistical anomalies in response patterns; audit error uniformity
- **Solution**: Enforce strict uniform error handling; use RSA-OAEP; add random delays
- **Tags**: Blind Oracle, Statistical Oracle Attack

## Partial Oracle Attack

- **Attack Type**: Oracle Reveals Partial Padding Correctness
- **Target**: RSA PKCS#1 v1.5 systems
- **Vulnerability**: Partial padding oracle leakage
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Partial or full plaintext recovery
- **Tools**: Burp Suite, custom scripts
- **Scenario**: Oracle leaks partial information, e.g., only about some padding bytes, enabling partial plaintext recovery over many queries.
- **Attack Steps**: Step 1: Attacker sends ciphertexts to a target that reveals partial padding info (e.g., indicates if some bytes are valid but not full padding correctness). Step 2: Records oracle responses and uses partial feedback to reduce possible plaintext ranges. Step 3: Iteratively crafts ciphertexts that manipulate different padding bytes and observes changes in partial oracle outputs. Step 4: Combines partial info over many queries to reconstruct the full padding structure gradually. Step 5: Once padding is understood, attacker decrypts plaintext step-by-step by adaptive querying. Step 6: This attack can bypass mitigations that obfuscate full oracle responses but leak partial info. Step 7: Useful against implementations that leak subtle error states rather than binary valid/invalid responses.
- **Detection**: Detect partial error info in logs; monitor partial failure patterns
- **Solution**: Uniform error messaging; patch implementations; migrate to RSA-OAEP
- **Tags**: Partial Oracle, Padding Leak

## Bleichenbacher Attack on Hardware Security Modules (HSMs)

- **Attack Type**: Hardware-based Oracle and Side-Channel Attack
- **Target**: Hardware Security Modules (HSMs)
- **Vulnerability**: Oracle and side-channel leakage on RSA PKCS#1 v1.5
- **MITRE**: T1600 – Cryptographic Key Extraction
- **Impact**: Full private key compromise; hardware cloning risk
- **Tools**: Hardware analyzers (ChipWhisperer), HSM interfaces
- **Scenario**: Targets HSMs performing RSA PKCS#1 v1.5 decryption that leak oracle info and side-channels like power or timing to extract keys.
- **Attack Steps**: Step 1: Attacker sends specially crafted ciphertexts to the HSM performing RSA PKCS#1 v1.5 decryption. Step 2: Measures side-channel info such as power consumption, electromagnetic emissions, or response timing to infer padding validity indirectly. Step 3: Uses side-channel combined with oracle responses (error messages or operation aborts) to classify ciphertexts. Step 4: Applies adaptive querying to gradually narrow down plaintext bytes or key bits using side-channel signals as an enhanced oracle. Step 5: Collects extensive side-channel traces and statistically analyzes them to reconstruct private key material. Step 6: Successfully extracting private key enables full system compromise including cryptographic signing, authentication bypass. Step 7: Defense requires hardware hardening, constant-time operations, and error uniformity.
- **Detection**: Monitor side-channel anomalies; audit error messages; implement rate limiting
- **Solution**: Use hardware hardened against side-channels; constant-time RSA; disable oracle errors
- **Tags**: HSM Oracle Attack, Side-Channel Key Extraction

## Bleichenbacher Attack on Cloud Cryptographic APIs

- **Attack Type**: Cloud API Padding Oracle Exploit
- **Target**: Cloud Cryptographic APIs (AWS, Azure, GCP)
- **Vulnerability**: Padding oracle leaks in cloud RSA decryption APIs
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Key/session compromise; cloud data exposure
- **Tools**: Cloud API testing tools, Burp Suite, Python scripts
- **Scenario**: Exploits cloud cryptographic APIs (e.g., AWS KMS, Azure Key Vault) that perform RSA PKCS#1 v1.5 decryptions and leak padding errors.
- **Attack Steps**: Step 1: Attacker gains access to a cloud cryptographic API offering RSA PKCS#1 v1.5 decryption or signing. Step 2: Sends encrypted ciphertexts to the API and observes error responses or status codes indicating padding validity. Step 3: Modifies ciphertext adaptively based on oracle feedback to iteratively narrow down plaintext guesses. Step 4: Uses automated scripts to repeat adaptive queries, collecting oracle responses to fully recover plaintext or session keys. Step 5: Exploits recovered keys to decrypt sensitive data or impersonate clients using cloud API credentials. Step 6: Continues querying carefully to avoid rate limits or detection. Step 7: Attack highlights risks of exposing raw crypto primitives via cloud APIs without proper error handling.
- **Detection**: Monitor API error codes and rates; audit cloud logs for padding-related errors
- **Solution**: Enforce uniform error responses; use RSA-OAEP padding; limit API exposure
- **Tags**: Cloud Oracle, RSA API Attack

## Bleichenbacher Attack with Fault Injection

- **Attack Type**: Induce Faults to Trigger Padding Oracle Behavior
- **Target**: Hardware/Software RSA implementations
- **Vulnerability**: Fault-induced padding oracle leakage
- **MITRE**: T1499 – Hardware Fault Injection
- **Impact**: Accelerated plaintext/key recovery; bypass mitigations
- **Tools**: Fault injection hardware (ChipWhisperer), EM glitchers
- **Scenario**: Injects faults (e.g., voltage, clock glitches) into RSA decryption hardware/software to force padding errors and leak info.
- **Attack Steps**: Step 1: Attacker gains physical or remote fault injection access to the target system performing RSA PKCS#1 v1.5 decryption. Step 2: Injects voltage or clock glitches during decryption to cause faults affecting padding checks. Step 3: Monitors system responses (error messages, crashes) that now reveal padding correctness due to fault-induced abnormal behavior. Step 4: Uses fault-induced oracle responses to perform adaptive queries similar to classical Bleichenbacher attacks. Step 5: Iteratively refines ciphertexts exploiting fault-triggered oracle to recover plaintext or keys faster or where standard oracle is unavailable. Step 6: Combines fault injection and oracle leaks to bypass hardened cryptographic implementations. Step 7: Requires precise timing and setup, often performed in hardware labs or physical attack scenarios.
- **Detection**: Detect unusual fault events or crashes; monitor error consistency
- **Solution**: Harden hardware; detect and respond to faults; use hardened crypto routines
- **Tags**: Fault Injection, Hardware Oracle Attack

## Combined Bleichenbacher and Padding Oracle on Hybrid Encryption

- **Attack Type**: Attack on RSA + Symmetric Hybrid Schemes
- **Target**: Hybrid Encryption Systems (RSA + Symmetric)
- **Vulnerability**: RSA and/or symmetric padding oracle leakage
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Full plaintext compromise; key recovery
- **Tools**: Burp Suite, crypto libraries, custom scripts
- **Scenario**: Exploits RSA PKCS#1 v1.5 oracle leaks combined with symmetric cipher padding oracles to fully decrypt hybrid encrypted data.
- **Attack Steps**: Step 1: Attacker obtains ciphertext encrypted with hybrid scheme: RSA encrypts symmetric session key, symmetric cipher encrypts data. Step 2: Performs Bleichenbacher adaptive queries against RSA portion (encrypted session key), obtaining oracle feedback about padding correctness. Step 3: Recovers session key via RSA oracle attack. Step 4: Uses recovered key to decrypt symmetric ciphertext part. Step 5: If symmetric padding oracle (e.g., CBC padding oracle) exists, attacker further uses padding oracle techniques on symmetric data for full plaintext recovery. Step 6: Exploits combined vulnerabilities for complete message compromise, even if only one oracle is partial. Step 7: Demonstrates need for end-to-end secure padding and encryption schemes.
- **Detection**: Monitor multi-stage oracle queries; audit error leaks on both crypto layers
- **Solution**: Use RSA-OAEP; avoid symmetric padding oracles; implement authenticated encryption (AEAD)
- **Tags**: Hybrid Oracle Attack, RSA + Symmetric Padding Oracle

## Bleichenbacher Attack on TLS Handshake Resumption

- **Attack Type**: Oracle Attack via TLS Session Resumption
- **Target**: TLS 1.2 servers with session resumption
- **Vulnerability**: RSA PKCS#1 v1.5 padding oracle in resumption tickets
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Session impersonation; traffic decryption
- **Tools**: Wireshark, TLS test suites, Burp Suite
- **Scenario**: Exploits RSA padding oracle leaks in TLS 1.2 session resumption where encrypted tickets are reused.
- **Attack Steps**: Step 1: Attacker captures TLS session resumption ticket encrypted with RSA PKCS#1 v1.5 padding during a resumed handshake. Step 2: Modifies ciphertext of the ticket and resubmits to server. Step 3: Observes server’s oracle responses (e.g., error alerts) about padding correctness. Step 4: Uses adaptive queries to iteratively recover plaintext of session ticket. Step 5: With recovered ticket data, attacker resumes sessions as victim, impersonating them or decrypting traffic. Step 6: Exploits weak error handling in resumption protocol to mount padding oracle attack despite shorter tickets. Step 7: Attack reduces session security and enables impersonation without full handshake compromise.
- **Detection**: Monitor TLS alert messages and resumption failures; log suspicious ticket errors
- **Solution**: Use session tickets with AEAD encryption; patch TLS libraries; disable vulnerable resumption modes
- **Tags**: TLS Oracle, Session Resumption Attack

## Misconfigured Error Handling Enabling Oracle

- **Attack Type**: Padding Oracle via Detailed Error Leakage
- **Target**: Web Apps, APIs, Crypto Services
- **Vulnerability**: Detailed padding error messages leaked
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Full plaintext/key recovery; data leakage
- **Tools**: Burp Suite, Proxy tools, HTTP interceptors
- **Scenario**: Applications leak detailed RSA padding error messages rather than generic failure responses, allowing oracle attacks.
- **Attack Steps**: Step 1: Attacker interacts with the target application or API that performs RSA PKCS#1 v1.5 decryption (e.g., login, payment processing). Step 2: Sends malformed ciphertexts to trigger padding errors. Step 3: Observes that the server returns distinct, detailed error messages indicating padding check failures rather than generic errors. Step 4: Uses these distinct error messages as an oracle to classify ciphertexts as valid or invalid padding. Step 5: Crafts new ciphertexts adaptively based on oracle feedback to narrow down the plaintext space. Step 6: Repeats the process iteratively to fully recover the plaintext or private keys. Step 7: Exploits this vulnerability to decrypt sensitive data or impersonate users without needing private keys. Step 8: To prevent detection, attacker may throttle requests or mimic normal traffic patterns.
- **Detection**: Monitor application error messages; audit logs for padding error specifics
- **Solution**: Replace detailed errors with generic ones; use RSA-OAEP padding; patch cryptolibs
- **Tags**: Oracle Attack, Error Leakage

## Incorrect PKCS#1 Padding Validation

- **Attack Type**: Faulty or Missing Strict Padding Checks
- **Target**: Crypto Libraries, Secure Services
- **Vulnerability**: Weak or incorrect padding validation logic
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Accelerated plaintext recovery
- **Tools**: Static code analysis, Crypto fuzzers
- **Scenario**: Crypto implementations incorrectly validate PKCS#1 padding, enabling oracle attacks or direct plaintext recovery.
- **Attack Steps**: Step 1: Attacker identifies a system using RSA PKCS#1 v1.5 padding with weak or incorrect padding validation logic (e.g., accepts malformed paddings). Step 2: Crafts ciphertexts with subtle padding format errors that bypass the validation checks. Step 3: Sends these ciphertexts to the target service and monitors responses. Step 4: Uses responses to infer partial padding correctness or plaintext structure. Step 5: Combines multiple queries to gradually recover plaintext or infer key bits. Step 6: Exploits this lax validation to break cryptographic guarantees faster than classical attacks. Step 7: Highlights importance of strict adherence to PKCS#1 standards in implementations.
- **Detection**: Code audit for padding validation; fuzz testing of crypto implementations
- **Solution**: Strictly follow PKCS#1 specs; patch libraries; use hardened crypto implementations
- **Tags**: Padding Validation, Crypto Bugs

## Bleichenbacher Attack via Side-Channel Timing on Web Servers

- **Attack Type**: Timing Side-Channel on RSA Padding Checks
- **Target**: Web Servers, TLS Servers
- **Vulnerability**: Timing side-channel during padding validation
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Data leakage without explicit oracle errors
- **Tools**: Timing measurement tools, Wireshark, ChipWhisperer
- **Scenario**: Timing differences during RSA PKCS#1 v1.5 decryption enable attackers to distinguish padding validity and decrypt ciphertexts.
- **Attack Steps**: Step 1: Attacker sends a series of RSA ciphertexts to the web server performing RSA PKCS#1 v1.5 decryption. Step 2: Measures response times with high precision for each ciphertext. Step 3: Observes that valid padding decryption attempts take different time than invalid padding due to branching or error handling. Step 4: Uses timing info as a side-channel oracle to classify ciphertext padding validity without explicit error messages. Step 5: Iteratively modifies ciphertext based on timing feedback to narrow plaintext bytes. Step 6: Applies statistical analysis over many queries to reliably recover plaintext. Step 7: Attack bypasses defenses that hide explicit padding errors but leak timing info. Step 8: Enables decryption of sensitive data or session keys.
- **Detection**: Monitor server timing behavior; implement timing anomaly detection
- **Solution**: Use constant-time padding checks; add jitter/random delays; migrate to RSA-OAEP
- **Tags**: Timing Oracle, Side-Channel Attack

## Bleichenbacher Attack exploiting Padding vs. MAC error distinctions

- **Attack Type**: Oracle Differentiates Padding Errors vs MAC Errors
- **Target**: TLS Servers, Crypto APIs
- **Vulnerability**: Distinct error responses for padding vs MAC errors
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Full plaintext/key compromise; session hijacking
- **Tools**: Burp Suite, Web proxies, Fuzzers
- **Scenario**: Attack exploits differences in server responses between padding errors and MAC verification failures to leak oracle info.
- **Attack Steps**: Step 1: Attacker sends ciphertexts to a target system that performs RSA decryption followed by MAC verification (e.g., TLS). Step 2: Observes that the server returns different error messages or response codes when padding is invalid vs when MAC verification fails. Step 3: Uses this error difference as an oracle to classify ciphertext padding validity. Step 4: Adapts ciphertexts based on oracle feedback to iteratively recover plaintext or session keys. Step 5: Repeats adaptive queries to exploit the distinct error signals to full recovery. Step 6: Exploits implementation flaws that do not mask or unify error handling between padding and MAC failures. Step 7: Enables decryption or impersonation attacks on protocols like TLS or encrypted messaging.
- **Detection**: Audit error messaging consistency; monitor protocol error types
- **Solution**: Use unified error handling; patch crypto libs; migrate to RSA-OAEP; constant-time checks
- **Tags**: Padding vs MAC Oracle, Crypto Implementation Flaws

## Replay Attack using Bleichenbacher Oracle

- **Attack Type**: Replay combined with Padding Oracle Exploit
- **Target**: Web Apps, APIs, Network Services
- **Vulnerability**: Padding oracle vulnerability + replay possibility
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Authentication bypass; session hijacking
- **Tools**: Network sniffers (Wireshark), Burp Suite
- **Scenario**: Attacker replays previously captured ciphertexts and uses Bleichenbacher oracle responses to bypass authentication or decrypt data.
- **Attack Steps**: Step 1: Attacker captures encrypted RSA ciphertexts (e.g., login tokens, session keys) from network traffic. Step 2: Sends the captured ciphertexts back to the target system as replayed requests. Step 3: Observes if the system responds with detailed padding error messages or uses an RSA padding oracle. Step 4: Uses the oracle feedback to adaptively modify and resend ciphertexts, iteratively decrypting or validating parts of the plaintext. Step 5: Leverages decrypted data to bypass authentication or replay valid sessions. Step 6: Continues replaying and refining ciphertexts while monitoring oracle responses to maintain unauthorized access. Step 7: May automate the process with scripts to speed up decryption or impersonation. Step 8: Highlights risks of combining replay and oracle attacks in insecure cryptographic implementations.
- **Detection**: Monitor repeated ciphertext usage; anomaly detection on repeated requests
- **Solution**: Use nonce or timestamp protections; patch padding oracle leaks; enforce session uniqueness
- **Tags**: Replay Attack, Padding Oracle

## Bleichenbacher Attack on Legacy Systems

- **Attack Type**: Classical Oracle Attack on Old RSA Systems
- **Target**: Legacy Servers, Embedded Devices
- **Vulnerability**: Lack of padding oracle mitigation on RSA PKCS#1 v1.5
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Data leakage; authentication bypass
- **Tools**: Burp Suite, Crypto analyzers
- **Scenario**: Legacy systems still using RSA PKCS#1 v1.5 without mitigations remain vulnerable to classical Bleichenbacher attacks.
- **Attack Steps**: Step 1: Attacker identifies legacy systems using RSA PKCS#1 v1.5 for encryption or signing without OAEP or mitigations. Step 2: Sends adaptive ciphertexts to the system to test for distinct padding error responses. Step 3: Uses error-based oracle feedback to iteratively decrypt ciphertexts by narrowing plaintext bytes. Step 4: Fully recovers plaintext such as session keys or credentials. Step 5: Exploits recovered data to access protected resources or impersonate users. Step 6: Often no rate limiting or uniform errors make attack faster on legacy devices. Step 7: Attack emphasizes the critical need for migration to secure padding schemes in old infrastructure.
- **Detection**: Scan for error messages typical of Bleichenbacher oracles
- **Solution**: Upgrade to RSA-OAEP; patch legacy systems; deploy web application firewalls
- **Tags**: Legacy Crypto, RSA Padding Oracle

## Bleichenbacher Attack on VPNs using RSA Key Exchange

- **Attack Type**: Padding Oracle Attack on VPN RSA Handshake
- **Target**: VPN Servers, Enterprise Networks
- **Vulnerability**: RSA padding oracle in VPN handshake
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: VPN session compromise; traffic interception
- **Tools**: VPN client/server tools, Wireshark, Burp Suite
- **Scenario**: VPN servers using RSA PKCS#1 v1.5 for key exchange leak padding errors, enabling session key recovery and traffic decryption.
- **Attack Steps**: Step 1: Attacker monitors VPN handshake messages involving RSA-encrypted premaster secrets using PKCS#1 v1.5 padding. Step 2: Sends modified handshake messages with altered ciphertexts to the VPN server. Step 3: Observes server responses for padding errors or handshake failure details indicating padding oracle. Step 4: Uses oracle feedback to iteratively decrypt the premaster secret used to derive VPN session keys. Step 5: Recovers session keys allowing decryption of VPN traffic or impersonation of VPN clients. Step 6: Exploits these vulnerabilities to intercept confidential VPN communications. Step 7: Attack may require multiple handshake attempts and adaptive queries to fully recover keys. Step 8: Highlights critical VPN infrastructure risks from unpatched cryptographic implementations.
- **Detection**: Monitor VPN handshake errors; alert on multiple handshake failures
- **Solution**: Patch VPN software; migrate to forward-secure ciphers like ECDHE; disable RSA key exchange
- **Tags**: VPN Attack, RSA Oracle

## Bleichenbacher Attack on IoT Devices

- **Attack Type**: Oracle Attack on IoT Devices using RSA PKCS#1 v1.5
- **Target**: IoT Devices, Embedded Systems
- **Vulnerability**: RSA padding oracle due to poor error handling
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Device compromise; data leakage; command injection
- **Tools**: Network sniffers, IoT testbeds, Burp Suite
- **Scenario**: IoT devices with constrained resources use vulnerable RSA implementations leaking padding errors exploitable via network.
- **Attack Steps**: Step 1: Attacker scans IoT device communication channels that use RSA PKCS#1 v1.5 encryption for data or key exchange. Step 2: Sends crafted ciphertexts to IoT devices and observes error messages or responses indicating padding failure. Step 3: Uses the oracle to adaptively modify ciphertexts to decrypt session keys or sensitive data. Step 4: Exploits recovered plaintext to bypass authentication or inject malicious commands. Step 5: Repeats attack until full control or data access is obtained. Step 6: Often IoT devices lack rate limiting or secure padding checks, making them highly vulnerable. Step 7: Emphasizes IoT risks from weak cryptographic implementations and lack of secure update mechanisms.
- **Detection**: Monitor device error logs and abnormal command execution
- **Solution**: Secure firmware updates; use RSA-OAEP or ECC; implement uniform error handling
- **Tags**: IoT Crypto Vulnerability, RSA Oracle

## Adaptive Bleichenbacher Attack with Network Latency Analysis

- **Attack Type**: Timing Oracle using Network Delays
- **Target**: Web Servers, Crypto APIs
- **Vulnerability**: Network timing side-channel during padding checks
- **MITRE**: T1201 – Cryptographic Decryption
- **Impact**: Data leakage without explicit oracle errors
- **Tools**: Wireshark, Timing analysis tools, Python scripts
- **Scenario**: Uses subtle differences in network response times as oracle feedback to distinguish valid vs invalid padding during RSA decryption.
- **Attack Steps**: Step 1: Attacker sends RSA ciphertexts to the target server for decryption over the network. Step 2: Measures response times precisely for each ciphertext request using timing tools or scripts. Step 3: Observes that valid padding decryption requests respond with slightly different latency than invalid ones due to internal processing differences. Step 4: Uses these timing differences as oracle feedback to classify ciphertexts without explicit error messages. Step 5: Crafts adaptive ciphertexts modifying parts based on timing oracle responses. Step 6: Repeats the process iteratively, statistically analyzing latency data to recover plaintext bytes. Step 7: Automates queries to reduce noise and increase accuracy. Step 8: Exploits the attack to decrypt sensitive data or session keys even if error messages are uniform.
- **Detection**: Monitor network latency anomalies; detect abnormal response timing patterns
- **Solution**: Implement constant-time cryptographic routines; add random delays; use RSA-OAEP padding
- **Tags**: Timing Oracle, Network Side-Channel

## Bleichenbacher Attack combined with Key Extraction via Fault Analysis

- **Attack Type**: Combined Fault Injection and Padding Oracle
- **Target**: Hardware Security Modules, Crypto Chips
- **Vulnerability**: Fault injection enabling padding oracle leaks
- **MITRE**: T1499 – Hardware Fault Injection
- **Impact**: Full private key extraction; total system compromise
- **Tools**: Fault injection hardware (ChipWhisperer), EM glitchers
- **Scenario**: Combines fault injection (glitches, voltage spikes) with Bleichenbacher oracle to speed up RSA private key extraction.
- **Attack Steps**: Step 1: Attacker gains access to the target hardware or environment performing RSA PKCS#1 v1.5 decryptions. Step 2: Uses fault injection tools to induce errors during RSA computations, causing faulty decryptions or padding checks. Step 3: Observes system responses or error messages acting as a padding oracle that now includes faulty outputs. Step 4: Uses these fault-induced oracles combined with classical Bleichenbacher adaptive queries to reduce the key search space. Step 5: Collects multiple faulty decryptions and oracle outputs. Step 6: Applies differential fault analysis (DFA) techniques to infer private key bits from faulty ciphertexts. Step 7: Combines the data to reconstruct the entire RSA private key more efficiently than classical attacks. Step 8: Uses recovered private key to decrypt all communications and impersonate the device or user.
- **Detection**: Monitor fault injection attempts; detect abnormal error patterns
- **Solution**: Harden hardware; add fault detection; use RSA-OAEP; constant-time checks
- **Tags**: Fault Injection, Padding Oracle, Key Extraction

## Linear Cryptanalysis

- **Attack Type**: Linear Approximation Attack
- **Target**: Block ciphers
- **Vulnerability**: Bias in linear relations of cipher
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Secret key recovery
- **Tools**: Statistical analysis tools
- **Scenario**: Uses linear approximations to describe block cipher operations and exploit correlations to recover secret keys.
- **Attack Steps**: Step 1: Attacker collects a large set of plaintext-ciphertext pairs from the target cipher. Step 2: Identifies linear expressions (linear approximations) that relate plaintext, ciphertext, and key bits with some bias. Step 3: Computes the correlation between these linear approximations and observed ciphertexts. Step 4: Uses statistical methods to find which key bits produce the highest correlation. Step 5: Narrows down the possible key space by excluding unlikely key bits. Step 6: Iterates and combines results from multiple approximations to recover the full key or key parts. Step 7: Finalizes key recovery by exhaustive search or further analysis. Step 8: Uses recovered key to decrypt all intercepted ciphertexts.
- **Detection**: Analyze cipher input/output statistics
- **Solution**: Use ciphers resistant to linear cryptanalysis (e.g., AES)
- **Tags**: Linear Cryptanalysis, Statistical Attack

## Differential Cryptanalysis

- **Attack Type**: Chosen Plaintext Difference Attack
- **Target**: Block ciphers
- **Vulnerability**: Predictable difference propagation
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key recovery, data compromise
- **Tools**: Chosen plaintext oracle, Crypto libraries
- **Scenario**: Exploits how specific input differences affect ciphertext differences to deduce key bits in block ciphers.
- **Attack Steps**: Step 1: Attacker chooses pairs of plaintexts with a fixed difference pattern and encrypts them under the unknown key. Step 2: Collects corresponding ciphertext pairs from the encryption oracle. Step 3: Analyzes how input differences propagate through cipher rounds by observing ciphertext differences. Step 4: Identifies key bits that cause expected differential patterns with higher probability. Step 5: Filters out incorrect key guesses by comparing predicted and actual ciphertext differences. Step 6: Repeats the process over multiple rounds and pairs to gradually recover the secret key bits. Step 7: Combines partial key bits to reconstruct the full key. Step 8: Uses the key to decrypt or forge ciphertexts.
- **Detection**: Monitor unusual encryption patterns
- **Solution**: Use cipher designs with strong differential resistance
- **Tags**: Differential Cryptanalysis

## Integral Cryptanalysis

- **Attack Type**: Sums over Sets Attack
- **Target**: Block ciphers
- **Vulnerability**: Cipher exhibits integral properties
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key leakage, data exposure
- **Tools**: Statistical tools, Cipher oracle
- **Scenario**: Uses sums of plaintexts/ciphertexts over structured sets to expose key bits in substitution-permutation ciphers.
- **Attack Steps**: Step 1: Attacker selects sets of plaintexts where certain bits vary over all possible values (e.g., all possible values in some bytes). Step 2: Encrypts all plaintexts in the set and collects ciphertexts. Step 3: Computes the sum (XOR or addition) of ciphertext values over the set. Step 4: Observes patterns where sums become constant or zero, revealing invariants. Step 5: Uses these invariants to deduce information about key bits or internal states. Step 6: Applies analysis iteratively to reduce key space. Step 7: Recovers partial or full keys by combining integral properties across rounds. Step 8: Decrypts ciphertexts or forges valid encryptions using recovered key bits.
- **Detection**: Analyze sums over plaintext/ciphertext sets
- **Solution**: Use ciphers designed to resist integral cryptanalysis
- **Tags**: Integral Cryptanalysis

## Slide Attack

- **Attack Type**: Related-key or Identical-round Attack
- **Target**: Block ciphers
- **Vulnerability**: Identical or related round keys
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key recovery, cipher breakage
- **Tools**: Cipher oracle, Statistical tools
- **Scenario**: Exploits cipher structures with identical or related round keys to find slide pairs and recover keys.
- **Attack Steps**: Step 1: Attacker identifies ciphers with repeated identical round functions or related round keys. Step 2: Collects ciphertexts from plaintexts encrypted under the cipher. Step 3: Searches for plaintext-ciphertext pairs that form "slide pairs" — pairs where one ciphertext equals the other after shifting rounds. Step 4: Uses slide pairs to cancel out rounds and recover key material or internal states. Step 5: Applies algebraic or statistical techniques on slide pairs to deduce the secret key. Step 6: Verifies recovered key parts by testing against encryption oracle. Step 7: Combines recovered key parts to reconstruct the full key. Step 8: Uses key for decryption and encryption forgery.
- **Detection**: Look for repeated patterns in ciphertexts
- **Solution**: Design ciphers with independent round keys or use key schedules
- **Tags**: Slide Attack

## Related-Key Attack

- **Attack Type**: Key Relation Exploitation
- **Target**: Symmetric block ciphers
- **Vulnerability**: Poor key scheduling, predictable key relations
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Secret key recovery; data decryption
- **Tools**: Chosen plaintexts, crypto simulation tools
- **Scenario**: Attacker knows how two or more keys relate (e.g., XOR difference) and uses this knowledge to attack the cipher more easily.
- **Attack Steps**: Step 1: Attacker identifies a cryptographic implementation where multiple keys are related (e.g., due to bad key derivation). Step 2: Selects or obtains ciphertexts encrypted under keys with known mathematical relation (e.g., Key2 = Key1 ⊕ constant). Step 3: Analyzes how the key relation affects the cipher’s internal state or output using multiple chosen plaintexts. Step 4: Compares the output patterns under both keys to cancel out parts of the cipher. Step 5: Deduces internal key-dependent data or key schedule properties. Step 6: Narrows key guesses using observed patterns. Step 7: Recovers full or partial key. Step 8: Uses recovered key to decrypt or forge valid ciphertexts. Note: This attack becomes easier if a system allows multiple related keys to encrypt the same data set.
- **Detection**: Look for related key usage or repeated structures
- **Solution**: Use strong key schedule algorithms and unique key derivation
- **Tags**: Related-Key, Symmetric Crypto

## Boomerang Attack

- **Attack Type**: Advanced Differential Attack
- **Target**: Block ciphers
- **Vulnerability**: Differentially weak middle rounds
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key recovery; bypass encryption strength
- **Tools**: Cipher simulator, chosen plaintexts
- **Scenario**: Extends differential cryptanalysis by combining differential paths forwards and backwards, allowing attack on more cipher rounds.
- **Attack Steps**: Step 1: Attacker selects a pair of plaintexts with a specific difference and observes how they transform through the cipher (forward differential trail). Step 2: Selects a second differential trail for ciphertexts with a known difference going backward (reverse trail). Step 3: Applies both forward and backward trails, creating a “boomerang” where two differentials connect in the middle rounds of the cipher. Step 4: Observes if both trails hold with a high enough probability for certain key bits. Step 5: Uses collisions or matches in the middle to filter possible key values. Step 6: Repeats the process with multiple input pairs to gather enough data. Step 7: Recovers key bits used in affected rounds. Step 8: Chains analysis across rounds until enough key material is recovered.
- **Detection**: Detect anomalous repeated patterns across partial rounds
- **Solution**: Strengthen middle rounds; design ciphers with boomerang resistance
- **Tags**: Boomerang, Differential, Block Cipher

## Meet-in-the-Middle Attack

- **Attack Type**: Time–Memory Trade-off Attack
- **Target**: Double/Triple encryption
- **Vulnerability**: Independent multi-key encryption schemes
- **MITRE**: T1110.003 – MITM Brute Force
- **Impact**: Breaks double encryption; key recovery
- **Tools**: Encryption/decryption tools, custom scripts
- **Scenario**: Breaks double encryption schemes by encrypting from one end and decrypting from the other, then matching in the middle.
- **Attack Steps**: Step 1: Attacker targets a cipher using multiple rounds of encryption with independent keys (e.g., double DES = E_K1(E_K2(plaintext))). Step 2: Chooses a known plaintext and its corresponding ciphertext. Step 3: Encrypts the plaintext using all possible values for the first key (K1), storing the intermediate values (midpoint) in a table. Step 4: Decrypts the ciphertext using all possible values for the second key (K2), generating midpoint values. Step 5: Matches values from both encryption and decryption steps (i.e., meeting in the middle). Step 6: When a match is found, the associated key pairs are likely candidates. Step 7: Tests candidate keys on other plaintext/ciphertext pairs to confirm. Step 8: Once confirmed, uses keys to decrypt or forge data.
- **Detection**: Monitor large amounts of key/ciphertext correlation attempts
- **Solution**: Avoid multiple encryptions with similar structures (use AES instead of 2DES)
- **Tags**: Meet-in-the-Middle, Brute Force

## Impossible Differential Attack

- **Attack Type**: Improbable Difference Exploit
- **Target**: Block ciphers
- **Vulnerability**: Existence of provably impossible differences
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Secret key recovery with high precision
- **Tools**: Chosen plaintext attack tools
- **Scenario**: Exploits input/output differences that should never occur in a correct cipher, filtering incorrect key guesses based on contradictions.
- **Attack Steps**: Step 1: Attacker studies the cipher to find input/output difference pairs that are mathematically impossible (i.e., input difference X can never become output difference Y under any key). Step 2: Chooses plaintexts with the required input difference and obtains their ciphertexts. Step 3: Compares ciphertexts to see if the impossible differential ever occurs. Step 4: If the impossible differential occurs, attacker eliminates the current key guess. Step 5: Repeats the process over many plaintext pairs and key guesses. Step 6: Gradually eliminates invalid key guesses by ruling out contradictions. Step 7: Left with only key candidates that never violate impossible differentials. Step 8: Confirms correct key from final set using extra data. Step 9: Decrypts ciphertexts or impersonates system.
- **Detection**: Identify improbable differential paths in cryptographic execution
- **Solution**: Design ciphers with uniform diffusion to prevent impossible differences
- **Tags**: Impossible Differential, Block Cipher

## Slide-and-XOR Attack

- **Attack Type**: Variant of Slide Attack + XOR Property
- **Target**: Block ciphers
- **Vulnerability**: Identical rounds, XOR predictable structure
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Partial or full key recovery
- **Tools**: Cipher implementation, Python or SageMath tools
- **Scenario**: An enhanced version of the Slide Attack, it leverages XOR operations to find slide pairs more efficiently and recover cipher key bits from repeating round logic.
- **Attack Steps**: Step 1: Attacker targets a block cipher that uses identical or related functions in each round (e.g., same operations repeated without unique round keys). Step 2: Collects many plaintext-ciphertext pairs from the target cipher. Step 3: Tries to find “slide pairs” where one plaintext (P1) encrypts into a ciphertext (C1), and another plaintext (P2) leads to ciphertext (C2) such that P2 = F(P1) and C2 = F(C1), where F is one cipher round. Step 4: Applies XOR to the plaintext and ciphertext pairs (P1 ⊕ P2, C1 ⊕ C2), looking for pairs with consistent differences. Step 5: The consistent XOR pattern helps eliminate randomness and focus on the underlying function F. Step 6: Using this XOR relationship, attacker reconstructs the round function and deduces key material. Step 7: Refines guesses by checking them against new plaintext-ciphertext pairs. Step 8: Once key bits are derived, uses them to decrypt other data or impersonate users.
- **Detection**: Monitor patterns in encrypted outputs, rate-limit mass encryption queries
- **Solution**: Use key-dependent rounds and randomness in encryption rounds
- **Tags**: Slide Attack, XOR, Block Cipher

## Algebraic Cryptanalysis

- **Attack Type**: Equation-Based Cipher Breaking
- **Target**: Symmetric Ciphers, Stream Ciphers
- **Vulnerability**: Weak algebraic structure or low-degree equations
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Full key recovery, cipher compromise
- **Tools**: SageMath, CryptoMiniSat, SAT solvers
- **Scenario**: Expresses encryption/decryption operations as algebraic equations and solves them to recover secret keys or internal state.
- **Attack Steps**: Step 1: Attacker models the cipher’s internal operations (S-boxes, permutations, XOR, modular additions) as a set of algebraic equations over finite fields (typically GF(2)). Step 2: Chooses several known plaintext-ciphertext pairs to substitute into the equations. Step 3: As equations accumulate, constructs a full system of nonlinear multivariate equations representing the encryption process with unknown key bits. Step 4: Uses SAT solvers, Gröbner basis algorithms, or other algebraic tools to solve the system and recover the key variables. Step 5: If the system is overdetermined or sparse enough, attacker can recover part or all of the cipher key. Step 6: Validates the result by encrypting/decrypting test data using the derived key. Step 7: Can generalize attack to recover keys from similar implementations or other users of the same weak cipher. Step 8: This method is especially effective against ciphers with simple algebraic structure or poor S-box design.
- **Detection**: Monitor high-frequency equation modeling attempts on cryptographic functions
- **Solution**: Use ciphers with proven algebraic complexity and high-degree non-linear operations
- **Tags**: Algebraic Attack, SAT Solver

## Weak DES Key Exploitation

- **Attack Type**: Predictable DES Key Exploitation
- **Target**: Legacy systems using DES
- **Vulnerability**: Use of static or weak key material
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Decryption of sensitive data; impersonation
- **Tools**: OpenSSL, Python DES libraries
- **Scenario**: Exploits weak or semi-weak DES keys that result in repeating or inverse encryptions, making brute force easier.
- **Attack Steps**: Step 1: Attacker targets a system using Data Encryption Standard (DES) with improperly chosen or static keys. Step 2: Identifies or suspects that one of the 16 known weak/semi-weak DES key pairs is in use. These keys either encrypt plaintext to the same ciphertext, decrypt back to the original, or generate the same subkeys in all rounds. Step 3: Collects plaintext-ciphertext pairs via eavesdropping or known plaintext analysis. Step 4: Tests these against known weak key pairs to check if they generate the observed ciphertexts. Step 5: When a match is found, attacker identifies the weak key in use. Step 6: Uses it to decrypt all other messages, forge data, or impersonate a user. Step 7: If needed, brute forces remaining keys among weak pairs (total 4–6 pairs only). Step 8: Exploits system until key is changed or crypto upgraded.
- **Detection**: Analyze encryption consistency; alert on known DES key usage
- **Solution**: Avoid DES; use AES or modern crypto with key randomness
- **Tags**: DES, Weak Keys, Legacy Crypto

## Weak RC4 Key Bias Exploitation

- **Attack Type**: Key Stream Bias Attack
- **Target**: RC4 encryption (WEP, SSL)
- **Vulnerability**: Predictable keystream output due to design flaw
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key exposure, session hijacking
- **Tools**: Wireshark, Scapy, rc4bias tool, Python
- **Scenario**: Exploits biases in the RC4 key stream output (especially first bytes), leading to key recovery or plaintext decryption.
- **Attack Steps**: Step 1: Attacker captures many ciphertexts encrypted with the RC4 algorithm, ideally all encrypted under the same key or predictable session keys. Step 2: Analyzes the first 256 bytes of each keystream to detect statistical biases. For example, the 2nd output byte in RC4 is significantly biased toward certain values depending on key bytes. Step 3: Uses this information to build a probability distribution over possible key bytes. Step 4: Applies statistical techniques (like Fluhrer–Mantin–Shamir attack) to guess the actual key with high confidence. Step 5: Decrypts ciphertexts using recovered key. Step 6: If plaintexts are known (e.g., HTTP headers), improves accuracy by filtering incorrect key guesses. Step 7: Repeats to fully reconstruct session keys or the master key. Step 8: Exploits compromised communications or sessions.
- **Detection**: Monitor excessive RC4 use, detect known bias patterns
- **Solution**: Stop using RC4; use TLS 1.3, AES-GCM, or ChaCha20
- **Tags**: RC4, Stream Cipher, Keystream Bias

## WEP Weakness Exploitation

- **Attack Type**: Wireless Key Recovery via RC4 & IV Reuse
- **Target**: WEP Wi-Fi networks
- **Vulnerability**: IV collisions; weak RC4 implementation
- **MITRE**: T1557.002 – Wireless Sniffing
- **Impact**: Full Wi-Fi key recovery; unauthorized access
- **Tools**: Aircrack-ng, Wireshark, Airodump-ng
- **Scenario**: Exploits key reuse and weak IV management in WEP to decrypt wireless traffic or recover the shared Wi-Fi key.
- **Attack Steps**: Step 1: Attacker uses a wireless sniffer (e.g., Airodump-ng) to capture many WEP-encrypted packets from the target Wi-Fi network. Step 2: Analyzes the Initialization Vectors (IVs) used in each packet. WEP combines a static shared key with a 24-bit IV, which repeats quickly in practice. Step 3: Waits for a large number of packets (100K–1M) to be captured. Step 4: Uses Aircrack-ng or similar tools to apply the Fluhrer–Mantin–Shamir (FMS) algorithm that leverages weak IVs to guess key bytes. Step 5: Eventually reconstructs the full WEP key (typically 40 or 104 bits). Step 6: Uses it to decrypt all traffic, inject packets, or hijack network sessions. Step 7: Maintains access until key changes. Step 8: WEP is vulnerable even without user activity, so passive sniffing is often enough.
- **Detection**: Detect WEP; monitor IV repetition and traffic anomalies
- **Solution**: Replace WEP with WPA2/WPA3; use EAP with dynamic key exchange
- **Tags**: Wi-Fi, WEP, RC4, Wireless Hacking

## CBC Padding Weakness Attack

- **Attack Type**: Padding Oracle on CBC-mode Block Cipher
- **Target**: Web apps, TLS endpoints
- **Vulnerability**: Distinct padding vs MAC error responses
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Session hijack, decryption without key
- **Tools**: Burp Suite, Python (requests, pycryptodome)
- **Scenario**: Exploits how padding errors in CBC mode block ciphers (like in TLS) reveal information to decrypt ciphertext byte-by-byte.
- **Attack Steps**: Step 1: Attacker captures a CBC-mode encrypted message (e.g., login token, session cookie). Step 2: Sends modified versions of the ciphertext to the target application. Step 3: Observes the application’s response. If the app distinguishes between valid padding vs. MAC errors (e.g., HTTP 500 vs 403), this leak is used as an oracle. Step 4: Changes the last byte of the ciphertext and retries until valid padding is found, revealing the last plaintext byte via XOR with padding value. Step 5: Repeats this for each byte, working backwards block-by-block. Step 6: Eventually reconstructs the entire plaintext. Step 7: May use the decrypted value (e.g., JWT) to forge session data. Step 8: This attack only works if padding/MAC error messages are distinct. Step 9: Attacker may automate this in Burp Suite or custom scripts.
- **Detection**: Inspect padding/MAC error responses; fuzz encrypted inputs
- **Solution**: Ensure constant-time error responses; authenticate before decrypting
- **Tags**: CBC, Padding Oracle, Web App Crypto

## Weak Key Schedule Attack

- **Attack Type**: Key Recovery via Predictable Key Expansion
- **Target**: Block ciphers, Stream ciphers
- **Vulnerability**: Weak or linear key schedule generation
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key recovery, full decryption
- **Tools**: Crypto libraries, Python, key schedule analyzers
- **Scenario**: Exploits poor key schedule designs where round keys are easily predicted or partially repeated, weakening encryption strength.
- **Attack Steps**: Step 1: Attacker targets a cipher (e.g., DES, RC4, or custom) known for having a weak or linear key schedule. Step 2: Observes or guesses how the key schedule expands a small key into many round keys (e.g., same round key every 2 rounds). Step 3: Collects ciphertexts encrypted under different inputs but the same weak key schedule. Step 4: Analyzes encryption patterns to detect when identical subkeys are reused in different rounds. Step 5: Uses differential or linear cryptanalysis to filter possible key bytes using known plaintext–ciphertext pairs. Step 6: Recovers partial or full master key. Step 7: Uses recovered key to decrypt, impersonate, or forge encrypted traffic. Step 8: This attack is particularly effective on ciphers with linear, non-random, or deterministic key expansion logic.
- **Detection**: Analyze round key patterns; fuzz input–output to detect key overlaps
- **Solution**: Use ciphers with cryptographically secure key expansion logic (e.g., AES)
- **Tags**: Key Schedule, Weak Key Expansion

## Birthday Attack on Block Ciphers

- **Attack Type**: Collision-Based Key or Message Forgery
- **Target**: Block ciphers, MACs
- **Vulnerability**: Small block size (e.g., 64-bit); short MACs
- **MITRE**: T1600 – Predictable Key Collisions
- **Impact**: Collision forgery, MAC bypass
- **Tools**: Python, Hash collision simulators, Hashcat
- **Scenario**: Uses the birthday paradox to find two inputs that produce the same ciphertext or MAC, breaking security of block ciphers and hash functions.
- **Attack Steps**: Step 1: Attacker targets a block cipher or hash-based authentication system where limited output size makes collisions likely (e.g., 64-bit block ciphers like DES). Step 2: Understands that if you generate about √(2^n) ciphertexts (where n = block size), there is a 50% chance of a collision. Step 3: Encrypts many chosen plaintexts under the same key and stores their ciphertexts. Step 4: Searches for two distinct plaintexts that result in the same ciphertext (collision). Step 5: If found, attacker may use one of these plaintexts to forge valid encrypted messages or authentication tokens. Step 6: This attack is more efficient than brute force and is often applied to block ciphers, CBC-MACs, or short-length hash outputs. Step 7: Attack can also be used to find weak keys that generate similar encryption patterns. Step 8: Preventing this requires longer key sizes and bigger blocks.
- **Detection**: Monitor for ciphertext or MAC collisions across large datasets
- **Solution**: Use ciphers with larger block size (≥128-bit); upgrade to SHA-256 or AES
- **Tags**: Birthday Paradox, MAC Forgery, DES

## Meet-in-the-Middle Attack on Double DES

- **Attack Type**: Time-Memory Trade-off Key Recovery
- **Target**: Double encryption systems
- **Vulnerability**: Use of 2-key DES (Double DES)
- **MITRE**: T1110.003 – MITM Brute Force
- **Impact**: Effective break of double encryption
- **Tools**: Python DES module, Hash tables, OpenSSL
- **Scenario**: Exploits double encryption by performing two-direction brute force (forward and backward) and meeting at the shared middle value to reduce key search space.
- **Attack Steps**: Step 1: Attacker targets a system using double DES encryption: C = E_K1(E_K2(P)). Step 2: Obtains a known plaintext–ciphertext pair from the system (e.g., login challenge). Step 3: Brute-forces all possible values for K1 and encrypts the plaintext under each, storing the resulting intermediate values in a table. Step 4: Brute-forces all values of K2 in reverse, decrypting the ciphertext under each and checking if the result matches any intermediate value in the table. Step 5: When a match is found, it’s highly likely that the K1 and K2 pair are valid. Step 6: Verifies key pair on another plaintext–ciphertext pair. Step 7: Attack requires 2^56 + 2^56 = ~2^57 operations, which is much less than brute-forcing full 2^112 keyspace. Step 8: Once keys are recovered, attacker can decrypt all messages, forge valid ciphertexts, or hijack sessions.
- **Detection**: Monitor encryption frequency and timing; alert on massive pair analysis
- **Solution**: Use 3DES or AES; Double DES is insecure against this attack
- **Tags**: Double DES, Brute Force, MITM

## Cryptanalysis of DES S-boxes

- **Attack Type**: S-box Structure Exploitation
- **Target**: DES block cipher
- **Vulnerability**: Weak S-box design; predictable substitution behavior
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key recovery; cipher compromise
- **Tools**: DES simulation tools, S-box analyzers
- **Scenario**: Explores weaknesses in DES substitution boxes (S-boxes), using their mathematical properties to enhance linear/differential cryptanalysis.
- **Attack Steps**: Step 1: Attacker targets the Data Encryption Standard (DES), which uses 8 different S-boxes to introduce non-linearity. Step 2: Analyzes the S-box substitution tables to identify biases, patterns, or mathematical weaknesses (e.g., linear approximations). Step 3: Uses these patterns to perform linear cryptanalysis — where attacker finds linear equations that approximate the S-box behavior with known probability. Step 4: Alternatively, applies differential cryptanalysis to find input differences that result in known output differences across S-boxes. Step 5: Collects many known plaintext–ciphertext pairs. Step 6: Uses statistical analysis to isolate key bits that influence specific S-boxes. Step 7: Narrows down key guesses and tests against other pairs. Step 8: Gradually reconstructs full DES key. Step 9: This method is possible due to historical weaknesses in the S-boxes’ original design.
- **Detection**: Track unusual decryption patterns; monitor for mass analysis
- **Solution**: Replace DES; use AES with robust S-boxes or ciphers with proven S-box strength
- **Tags**: DES, S-box, Linear/Diff Cryptanalysis

## Downgrade Attack to Weak Cipher Suites

- **Attack Type**: TLS/SSL Protocol Downgrade
- **Target**: Web servers, VPNs, APIs
- **Vulnerability**: Lack of enforcement for strong ciphers; protocol fallback
- **MITRE**: T1584.001 – Protocol Downgrade
- **Impact**: Full traffic decryption; session hijack
- **Tools**: Wireshark, mitmproxy, SSLStrip, OpenSSL
- **Scenario**: Forces client-server communication to use outdated or insecure encryption algorithms (e.g., SSL 2.0, RC4), allowing easier interception or decryption.
- **Attack Steps**: Step 1: Attacker positions themselves as a Man-in-the-Middle (MITM) between a client (e.g., browser) and a server (e.g., website). Step 2: Intercepts the initial TLS handshake, where the client proposes a list of supported cipher suites. Step 3: Alters the handshake messages to remove secure cipher suites (like AES-GCM, ChaCha20), leaving only insecure ones (like RC4, DES, or EXPORT suites). Step 4: Server, unaware of the tampering, selects a weak suite for the connection. Step 5: Client accepts the weak suite, thinking the server only supports that. Step 6: Now the attacker can decrypt traffic using known weaknesses (e.g., RC4 bias attacks) or collect data for offline brute-force. Step 7: This breaks the confidentiality and integrity of communication. Step 8: Attack often succeeds if legacy cipher support is enabled on server.
- **Detection**: Inspect TLS handshakes for weak cipher negotiation
- **Solution**: Enforce TLS 1.2+ only; disable SSLv2/3 and weak suites on servers
- **Tags**: TLS Downgrade, RC4, MITM, SSLStrip

## Hash Collision Attacks on Weak Hashes

- **Attack Type**: Collision Attack on MD5/SHA1
- **Target**: File servers, Signing apps
- **Vulnerability**: Use of broken hash functions (MD5, SHA1)
- **MITRE**: T1600 – Predictable Hash Collisions
- **Impact**: Forgery of files or digital signatures
- **Tools**: Hashclash, md5collider, SHAttered tools
- **Scenario**: Exploits cryptographic hash functions like MD5 or SHA-1 which allow two different inputs to produce the same hash, breaking data integrity.
- **Attack Steps**: Step 1: Attacker identifies a system or protocol that still uses a weak hash function (e.g., MD5 or SHA-1) for file integrity, digital signatures, or certificate validation. Step 2: Crafts two files that differ in content but produce the same hash (i.e., collision). Tools like "Hashclash" or "SHAttered" automate this. Step 3: One file contains benign content (e.g., a contract or PDF), which is reviewed and accepted by a victim. Step 4: The second file contains malicious code (e.g., a malware loader), but has the same hash. Step 5: Attacker swaps the benign file with the malicious one in storage or transmission. Step 6: Recipient verifies the hash (e.g., via MD5), sees it matches, and assumes the file is legitimate. Step 7: The malicious file is executed or trusted, enabling full compromise. Step 8: This breaks digital signatures, checksums, and any integrity protection using weak hashes.
- **Detection**: Log file hash mismatches; monitor legacy hash function usage
- **Solution**: Stop using MD5/SHA1; switch to SHA-256+ or SHA-3
- **Tags**: Hash Collision, MD5, SHA1, Signature Spoof

## RC2 Weakness Exploitation

- **Attack Type**: Key Size and Round Reduction Attacks
- **Target**: Legacy apps, S/MIME email
- **Vulnerability**: Small key sizes; reduction of cipher rounds
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key recovery; message decryption
- **Tools**: Python cryptography, OpenSSL, RC2 test suites
- **Scenario**: Exploits weaknesses in RC2 cipher such as its small key size and the possibility to reduce rounds, making it vulnerable to brute-force and cryptoanalysis.
- **Attack Steps**: Step 1: Attacker targets a system or app using RC2 encryption (often found in legacy Windows applications or S/MIME email encryption). Step 2: Identifies the key length in use (often 40, 64, or 128 bits). Many implementations only use 40-bit keys due to export restrictions. Step 3: Uses brute-force tools to test all 2^40 possible keys (trivial with modern GPUs or cloud compute). Step 4: Alternatively, captures ciphertext and applies known-plaintext or chosen-plaintext attacks exploiting reduced rounds (fewer than 18). Step 5: Recovers the encryption key or internal cipher state. Step 6: Uses key to decrypt sensitive files or messages, or tamper with encrypted communications. Step 7: The attack is silent and often undetectable. Step 8: RC2 is no longer considered secure and should not be used in any cryptographic setup.
- **Detection**: Monitor for RC2 usage; flag 40-bit/64-bit keys in legacy systems
- **Solution**: Replace RC2 with AES-256 or modern block cipher
- **Tags**: RC2, S/MIME, Legacy Crypto, Key Brute

## KASUMI Weaknesses in 3G/4G Protocols

- **Attack Type**: Cellular Key Derivation Exploitation
- **Target**: 3G/4G cellular networks
- **Vulnerability**: Inherent flaws in KASUMI block cipher design
- **MITRE**: T1584 – Cellular Eavesdropping
- **Impact**: SIM impersonation, decrypted comms
- **Tools**: SIMtrace, USRP, SRS-LTE, Cryptanalysis papers
- **Scenario**: Exploits design flaws in the KASUMI cipher used in 3G/UMTS/4G networks for key derivation, enabling SIM cloning, IMSI tracking, or ciphertext decryption.
- **Attack Steps**: Step 1: Attacker targets mobile network communication (e.g., 3G, UMTS) using the KASUMI block cipher for confidentiality and integrity protection. Step 2: Uses SDR (Software Defined Radio) tools like USRP or SIMtrace to capture encrypted over-the-air communication between mobile device and base station. Step 3: Focuses on known flaws in KASUMI (e.g., related-key attack, differential-linear hybrid analysis) that reduce attack complexity significantly. Step 4: Applies cryptanalysis to deduce session keys or long-term secret keys (e.g., Kc). Step 5: With recovered keys, decrypts call/SMS traffic or impersonates victim. Step 6: Advanced attacks allow full IMSI tracking, SIM cloning, or call injection. Step 7: This attack is highly technical but feasible with public tools and research knowledge. Step 8: Affects millions of 3G users in insecure configurations.
- **Detection**: Monitor radio signal anomalies; analyze SIM provisioning logs
- **Solution**: Switch to LTE-A with SNOW 3G/ZUC; phase out KASUMI-based networks
- **Tags**: KASUMI, 3G, SIM Cloning, Crypto Flaws

## Cryptanalysis of TEA/XTEA

- **Attack Type**: Key Schedule & Round Weakness Exploitation
- **Target**: Embedded systems, IoT
- **Vulnerability**: Poor key diffusion and insufficient rounds
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Device cloning, firmware theft
- **Tools**: Python scripts, CryptoCrack, custom TEA tools
- **Scenario**: Exploits the weak key schedule and limited rounds in Tiny Encryption Algorithm (TEA) and its extended version XTEA, used in embedded systems and IoT devices.
- **Attack Steps**: Step 1: Attacker identifies a device or protocol using TEA or XTEA (e.g., firmware updates, IoT messages, or custom file encryption). Step 2: Uses known plaintext–ciphertext pairs or obtains ciphertext from firmware dumps or network captures. Step 3: Understands that TEA/XTEA use a small number of rounds (typically 32) and a static key schedule that doesn’t diffuse entropy well. Step 4: Applies differential cryptanalysis by observing how input differences propagate to output. Step 5: For XTEA, attacks often focus on the ‘delta’ constant and how it affects round operations. Step 6: With enough known ciphertext pairs, performs statistical analysis to recover key bits or decrypt content. Step 7: Alternatively, if weak key is used (e.g., all-zero or predictable), brute force is practical due to small 64-bit keyspace. Step 8: Recovers firmware or messages and uses that to modify or clone device.
- **Detection**: Monitor firmware for encryption type; inspect traffic for TEA/XTEA patterns
- **Solution**: Replace TEA/XTEA with AES-128 or stronger ciphers
- **Tags**: TEA, XTEA, IoT Crypto, Weak Key Schedule

## Attacks on Reduced-Round AES Variants

- **Attack Type**: Truncated, Differential, or Integral Attacks
- **Target**: Embedded AES variants
- **Vulnerability**: Reduced-round implementations weaken security
- **MITRE**: T1600 – Predictable Encryption
- **Impact**: Key recovery, impersonation
- **Tools**: Python, PyCrypto, SageMath
- **Scenario**: Targets versions of AES used with fewer than standard rounds (e.g., 6 or 8 instead of 10–14), often found in lightweight apps, tests, or faulty configs.
- **Attack Steps**: Step 1: Attacker targets a system or implementation that uses AES but with fewer rounds than required (e.g., 6 instead of 10 for AES-128). This may be due to custom software, performance tweaks, or coding mistakes. Step 2: Captures several plaintext–ciphertext pairs via logging, API requests, or known input/output examples. Step 3: Applies differential cryptanalysis to analyze how differences in input plaintext affect output. Fewer rounds reduce diffusion, making this analysis easier. Step 4: Uses tools like SageMath to automate searching for differential trails or integral properties. Step 5: Recovers partial subkeys and reconstructs the master key by combining round keys. Step 6: Verifies results by decrypting new ciphertexts or generating valid ones. Step 7: This allows the attacker to impersonate, decrypt, or modify AES-encrypted data. Step 8: Vulnerability often unnoticed unless crypto config is audited.
- **Detection**: Review crypto configs; detect unusually fast AES encryption
- **Solution**: Always use AES with full rounds (AES-128 = 10, AES-192 = 12, AES-256 = 14)
- **Tags**: AES, Reduced Rounds, Key Recovery

## Cryptanalysis of Lightweight Ciphers (PRESENT)

- **Attack Type**: Algebraic/Differential Analysis of Small Ciphers
- **Target**: RFID, IoT, Smartcards
- **Vulnerability**: Fewer rounds; small S-boxes; simple SP networks
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key recovery, device spoofing
- **Tools**: SageMath, LWC toolkit, CryptoMiniSat
- **Scenario**: Targets low-power ciphers like PRESENT (used in RFID, IoT) that trade off performance for security by using fewer rounds and simpler S-boxes.
- **Attack Steps**: Step 1: Attacker identifies lightweight cryptographic algorithms in use (e.g., in RFID tags, smartcards, microcontrollers). Step 2: PRESENT is a 64-bit block cipher with 80/128-bit key options and is optimized for hardware — but uses a simple substitution-permutation network. Step 3: Using plaintext–ciphertext pairs, attacker performs differential cryptanalysis — looks at how specific bit changes in plaintext affect ciphertext. Step 4: Tools like CryptoMiniSat model the cipher as Boolean equations and solve for key bits using SAT solvers. Step 5: Due to fewer rounds (31 in PRESENT), attacker can reduce the attack complexity and recover partial key. Step 6: If weak key or few rounds are used, full key recovery may be possible. Step 7: Recovered keys allow cloning or spoofing of embedded devices. Step 8: Often, these devices lack logging or alerting.
- **Detection**: Analyze firmware; check for known lightweight cipher signatures
- **Solution**: Use newer lightweight ciphers with higher security margins (e.g., Ascon)
- **Tags**: Lightweight Crypto, PRESENT, IoT Attacks

## Weak PRNG Attacks (Pseudorandom Number Generators)

- **Attack Type**: Predictable Randomness Exploitation
- **Target**: Web apps, Crypto keygens
- **Vulnerability**: Predictable seed/init value in PRNG
- **MITRE**: T1600 – Predictable Key Material
- **Impact**: Session hijack, key compromise
- **Tools**: PRNG testers, Python, RANlim, randomness analyzers
- **Scenario**: Exploits poor or predictable randomness used in key generation, session tokens, or crypto challenges, often due to weak seeding or flawed algorithms.
- **Attack Steps**: Step 1: Attacker identifies a system that relies on PRNG for sensitive functions — like key generation (RSA, ECC), password reset tokens, or session IDs. Step 2: Monitors system output (e.g., generated tokens or keys) over multiple runs to analyze entropy and pattern. Step 3: If PRNG uses low-entropy seed (e.g., system time, PID), attacker guesses the seed value based on observed timing or behavior. Step 4: Reconstructs PRNG state or simulates it forward to predict future values. Step 5: For example, if session tokens are predictable, attacker can hijack other sessions. Step 6: In crypto applications, weak PRNG can lead to full RSA/ECC key recovery. Step 7: Attack often silent — system continues functioning normally while security is broken. Step 8: Easily exploitable in IoT, mobile apps, and legacy systems with custom or insecure PRNGs.
- **Detection**: Test entropy of tokens/keys; monitor for repeated or similar outputs
- **Solution**: Use cryptographically secure PRNGs like /dev/urandom, CSPRNG libraries
- **Tags**: PRNG, Key Prediction, Session Hijack

## Cryptanalysis of RC5

- **Attack Type**: Block Cipher Key Schedule & Parameter Weakness
- **Target**: Legacy encryption tools
- **Vulnerability**: Weak key schedule; insecure small parameter choices
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Decryption, data forgery
- **Tools**: Custom RC5 cracker, Python scripts, CryptoCrack
- **Scenario**: Exploits weaknesses in RC5’s flexible parameters—such as small word sizes, short keys, or weak key expansion—to recover keys or decrypt messages.
- **Attack Steps**: Step 1: Attacker finds that the target system uses RC5 for encryption (common in legacy systems or academic environments). Step 2: Identifies the specific RC5 configuration (word size, number of rounds, and key length). Weak configurations include: short keys (e.g., 40-bit), low rounds (e.g., 8), or small word sizes (e.g., 16-bit). Step 3: Gathers known plaintext-ciphertext pairs from logs, intercepted messages, or known file formats. Step 4: Exploits RC5’s simple key expansion process to mount differential or linear cryptanalysis. Step 5: If key is small (≤ 40 bits), brute-force attacks are feasible on modern machines. Step 6: If few rounds are used, attacker uses known attack paths (e.g., Biryukov-Demirci attacks) to reduce key space further. Step 7: Once key is recovered, attacker decrypts confidential data or modifies encrypted content silently. Step 8: Most RC5 attacks are undetectable unless key rotation or parameter auditing is in place.
- **Detection**: Monitor encryption config files; analyze entropy of encrypted outputs
- **Solution**: Use AES instead of RC5; if RC5 used, enforce ≥12 rounds and 128-bit key
- **Tags**: RC5, Weak Rounds, Legacy Ciphers

## Weaknesses in Stream Cipher Key/IV Management

- **Attack Type**: IV Reuse / Poor Initialization Exploitation
- **Target**: Stream cipher protocols
- **Vulnerability**: Keystream reuse due to poor key/IV initialization
- **MITRE**: T1600 – Predictable Encryption
- **Impact**: Plaintext recovery; session hijack
- **Tools**: Wireshark, Scapy, custom sniffers
- **Scenario**: Exploits stream cipher designs (e.g., RC4, Salsa20) where reusing Initialization Vectors (IVs) or keys allows key recovery or plaintext leakage.
- **Attack Steps**: Step 1: Attacker monitors traffic encrypted using stream ciphers (e.g., WEP with RC4, or TLS using ChaCha20). Step 2: Identifies reuse of Initialization Vectors (IVs) or the same key-IV pairs (known as keystream reuse). Step 3: Extracts two or more ciphertexts encrypted under same key/IV. Step 4: XORs the ciphertexts together—this removes the keystream and exposes XOR of plaintexts. Step 5: Uses known-plaintext attack: if one plaintext is known or guessed (e.g., HTTP headers), recovers both plaintexts fully. Step 6: If IV is predictable (e.g., counter starting from 0), attacker waits until collision occurs. Step 7: In many stream ciphers, this can lead to full key recovery with enough ciphertexts. Step 8: Exploits are fast and silent, especially in IoT and low-end embedded systems with limited randomness or no IV management.
- **Detection**: Monitor for IV collisions; audit randomness in firmware
- **Solution**: Enforce unique IV per session; avoid static key-IV pairs
- **Tags**: RC4, Salsa20, IV Reuse, Stream Cipher

## Attacks Exploiting Small Key Sizes

- **Attack Type**: Brute Force & Cryptanalysis on Short Keys
- **Target**: Weak crypto implementations
- **Vulnerability**: Small keyspace enables full key enumeration
- **MITRE**: T1600 – Brute Force
- **Impact**: Full message decryption; key recovery
- **Tools**: hashcat, JohnTheRipper, cloud GPU clusters
- **Scenario**: Exploits systems using cryptographic keys that are too short (e.g., 40-bit, 56-bit DES) and thus susceptible to complete brute-force or known-key attacks.
- **Attack Steps**: Step 1: Attacker identifies system using symmetric encryption with a key size below modern standards (e.g., 40-bit for export-grade RC2, or 56-bit DES). Step 2: Captures encrypted traffic or files protected by the weak cipher. Step 3: Uses a GPU-accelerated brute-force tool (e.g., Hashcat or JohnTheRipper) to try every possible key in the keyspace. Step 4: For 40-bit key, only 2^40 = ~1 trillion possibilities, which can be searched in under a day on modern hardware. Step 5: Once correct key is found (validated by known plaintext), decrypts all communications or files. Step 6: Can also modify or re-encrypt tampered content with the recovered key. Step 7: These attacks are practical and have been demonstrated in public competitions and research since 1990s. Step 8: Even with strong ciphers like AES, if the key size is too short, the entire algorithm becomes insecure.
- **Detection**: Check key length in crypto libraries; flag legacy cipher usage
- **Solution**: Use ≥128-bit keys; deprecate DES/RC2/40-bit modes
- **Tags**: Short Keys, Brute Force, Legacy Ciphers

## Related-Key Attacks on Symmetric Ciphers

- **Attack Type**: Key Recovery Using Key Relationship Patterns
- **Target**: Block ciphers, APIs, IoT firmware
- **Vulnerability**: Key schedule leaking correlations between keys
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Key recovery; mass decryption across devices
- **Tools**: Custom C/C++ cryptanalysis tools, SageMath
- **Scenario**: Exploits ciphers (e.g., AES, IDEA, RC5) where internal structures leak info if attacker controls related keys with known differences.
- **Attack Steps**: Step 1: Attacker targets an encryption system where they can influence or observe encryption under multiple related keys (e.g., K1, K2 where K2 = K1 ⊕ 0x01). Step 2: Collects ciphertext outputs for same plaintext under related keys. Step 3: Analyzes how the difference in keys affects the ciphertexts. Step 4: In ciphers with poor key schedule (e.g., IDEA, RC5), attackers can track these differences across rounds. Step 5: Applies related-key differential attacks to recover round keys. Step 6: Combines round key info to reverse-engineer master key. Step 7: If keys are generated from user passwords or predictable logic (e.g., device serial), attack is easier. Step 8: The system may never detect this, as individual key sessions appear valid. Step 9: Related-key attacks are powerful in cloud/embedded scenarios where key derivation logic is shared.
- **Detection**: Detect reuse of related keys; audit key derivation logic
- **Solution**: Use strong key expansion logic; prevent attacker influence over multiple keys
- **Tags**: Related Key, Key Schedule, Differential Attacks

## Shor’s Algorithm on Elliptic Curve (ECC)

- **Attack Type**: Quantum Attack on ECDLP
- **Target**: ECC-based Crypto (ECDSA, ECDH)
- **Vulnerability**: Elliptic Curve Discrete Logarithm (ECDLP)
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Total ECC key compromise
- **Tools**: IBM Qiskit, Q#, Simulators, Quantum Dev Kits
- **Scenario**: Shor’s algorithm breaks the Elliptic Curve Discrete Logarithm Problem (ECDLP), compromising ECC systems like ECDSA (signatures) and ECDH (key exchange).
- **Attack Steps**: Step 1: Understand that ECC security is based on the difficulty of solving the elliptic curve discrete logarithm problem (ECDLP). Classical algorithms can't solve it efficiently. Step 2: Shor’s algorithm can solve the ECDLP in polynomial time using a quantum computer. Step 3: Use a quantum simulator (e.g., IBM Qiskit or Microsoft's Q#) or real quantum hardware to model the ECC group and operations. Step 4: Implement or use a built-in Shor's algorithm module that takes a base point (G) and public point (Q = dG), and outputs the private key d. Step 5: The quantum circuit finds the period of a hidden function related to ECC point multiplication using quantum Fourier transform (QFT). Step 6: Once period is extracted, attacker solves for d, fully breaking ECC. Step 7: This exposes encrypted messages, fake digital signatures, and allows full impersonation. Step 8: Requires a fault-tolerant quantum computer with millions of logical qubits for real-world 256-bit ECC. Step 9: Currently simulated only; but future hardware will enable this attack.
- **Detection**: Monitor for quantum-era threats; audit ECC key reuse
- **Solution**: Transition to post-quantum algorithms (e.g., CRYSTALS-Kyber, Dilithium)
- **Tags**: Quantum, ECC, Shor's, ECDSA, ECDH

## Shor’s Algorithm on DSA / Diffie-Hellman

- **Attack Type**: Quantum Attack on Discrete Logarithm Problem
- **Target**: DSA, DH-based Protocols
- **Vulnerability**: Discrete Logarithm Problem (DLP)
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Break DSA signatures, decrypt DH exchanges
- **Tools**: IBM Qiskit, Microsoft QDK, Rigetti Forest
- **Scenario**: Shor’s algorithm can solve the standard Discrete Logarithm Problem (DLP), breaking protocols based on DSA and classic DH key exchange (common in SSH, VPNs, etc.).
- **Attack Steps**: Step 1: Recognize that DSA and DH are based on the difficulty of solving the DLP in cyclic groups (e.g., modulo a large prime). Classical methods (e.g., Pollard’s rho) are exponential. Step 2: Shor’s quantum algorithm efficiently solves DLP in polynomial time. Step 3: Simulate a DH key exchange between Alice and Bob where each has public values g^a mod p, g^b mod p. Step 4: Use quantum simulator or hardware to run Shor’s algorithm and retrieve a or b directly by solving for the exponent. Step 5: If DSA signatures are used, the attacker uses the algorithm to recover the private key used to generate valid signatures. Step 6: Once key is recovered, attacker can decrypt past DH-encrypted messages, impersonate users, or forge digital signatures. Step 7: Current threat is theoretical until quantum computers reach required scale (thousands of logical qubits). Step 8: Still critical to migrate in advance due to stored encrypted data that could be decrypted in future. Step 9: Long-term confidentiality is broken once quantum hardware becomes available.
- **Detection**: Monitor cryptographic protocols in use; inventory DSA/DH keys
- **Solution**: Replace with post-quantum key exchange (e.g., Kyber) and digital signature schemes
- **Tags**: Quantum, DH, DSA, Shor, Discrete Log

## RSA-1024/2048 Key Recovery via Shor’s Algorithm

- **Attack Type**: Quantum Integer Factorization
- **Target**: RSA encryption/signature systems
- **Vulnerability**: Integer Factorization Problem (IFP)
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Complete RSA key recovery
- **Tools**: Qiskit, Cirq, Quantum Simulators
- **Scenario**: Uses Shor’s algorithm to factor RSA public keys (modulus n = pq) into p and q, fully recovering private key in polynomial time, breaking encryption and signing.
- **Attack Steps**: Step 1: Attacker obtains a target RSA public key (typically 1024-bit or 2048-bit modulus n). Step 2: Understand that the public key includes n and e, and the private key is d, which depends on p and q. Step 3: Shor’s algorithm factors n = p*q using quantum order-finding and quantum Fourier transform (QFT). Step 4: Use a quantum simulator or cloud-accessible hardware to model the algorithm. Step 5: Feed the public modulus n to Shor’s routine and retrieve p and q. Step 6: Use those to compute the private key d using modular inverse: d = e⁻¹ mod φ(n). Step 7: Once d is known, attacker can decrypt RSA messages, sign forged messages, and impersonate the user. Step 8: RSA-1024 is especially vulnerable due to small key space; RSA-2048 is still at risk with future scalable quantum hardware. Step 9: Migration to post-quantum public-key cryptography is essential for long-term confidentiality.
- **Detection**: RSA key length audit; flag 1024/2048-bit keys
- **Solution**: Migrate to lattice-based or code-based post-quantum cryptography
- **Tags**: RSA, Shor’s Algorithm, Integer Factorization

## Quantum Discrete Logarithm Attack on DLP Schemes

- **Attack Type**: Quantum Discrete Logarithm Solving
- **Target**: All DLP-based systems
- **Vulnerability**: Quantum Solvability of Discrete Logarithms
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: Break all DLP-dependent cryptography
- **Tools**: Qiskit, Ocean SDK, Braket
- **Scenario**: Exploits Shor’s algorithm to solve discrete logarithms across all schemes relying on finite cyclic group exponentiation, breaking encryption/signature systems.
- **Attack Steps**: Step 1: Understand that many cryptosystems like DH, DSA, and ECC rely on hard discrete logarithm problems over finite groups. Step 2: Classical attacks take exponential time; quantum computing using Shor’s algorithm solves these problems in polynomial time. Step 3: Implement Shor’s algorithm using a quantum computing toolkit or cloud provider (e.g., IBM Q, Amazon Braket). Step 4: Input the group generator g, target value g^x mod p and modulus p to the quantum algorithm. Step 5: The algorithm finds x such that g^x = h mod p. Step 6: With x, attacker has full access to the original private key or secret exponent. Step 7: Attack works across DH, DSA, and ECC with appropriate changes. Step 8: While full-scale quantum computers don’t yet exist, simulations confirm the feasibility and scaling laws. Step 9: Risk is long-term but real—data encrypted today can be stored and decrypted years later once hardware is ready. Organizations must prepare now.
- **Detection**: Classify crypto systems by quantum resistance
- **Solution**: Replace with lattice, multivariate, hash-based post-quantum systems
- **Tags**: Shor, Quantum DLP, PQC, DH, DSA

## Quantum Break of TLS Handshakes

- **Attack Type**: Post-Quantum Decryption of TLS Handshake
- **Target**: TLS 1.2 Key Exchange
- **Vulnerability**: RSA or ECDHE handshake vulnerable to quantum attack
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Complete TLS session decryption
- **Tools**: Wireshark, Qiskit, Quantum Simulators
- **Scenario**: Quantum computers can retroactively decrypt TLS 1.2 sessions using RSA/ECDHE by breaking key exchange mechanisms through Shor’s algorithm.
- **Attack Steps**: Step 1: An attacker captures a TLS 1.2 handshake using tools like Wireshark, storing the encrypted session including the certificate exchange and pre-master secret (RSA or ECDHE). Step 2: If RSA is used for key exchange (common in legacy setups), attacker extracts the public key and modulus (n, e) from the certificate. Step 3: Using Shor’s algorithm in a quantum simulator (or quantum computer in the future), attacker factors the RSA modulus to retrieve private key d. Step 4: Attacker uses d to decrypt the pre-master secret. Step 5: If ECDHE is used, attacker solves ECDLP using Shor’s algorithm to recover the ephemeral private key. Step 6: With the pre-master secret obtained, attacker regenerates the TLS session keys and decrypts the entire encrypted traffic. Step 7: The process allows retrospective decryption of any previously recorded HTTPS session. Step 8: Impact: banking, medical, and confidential data previously thought to be secure may be decrypted years later.
- **Detection**: Monitor for legacy cipher usage; audit archived traffic
- **Solution**: Use TLS 1.3 with PQC; adopt hybrid post-quantum handshake methods
- **Tags**: TLS, HTTPS, RSA, ECDHE, Post-Quantum, Shor

## Quantum Break of SSH Key Exchange

- **Attack Type**: Post-Quantum Decryption of SSH Sessions
- **Target**: SSH Connections
- **Vulnerability**: DH or ECDH key exchange with quantum-exploitable math
- **MITRE**: T1499 – Cryptanalysis
- **Impact**: SSH confidentiality fully compromised
- **Tools**: Wireshark, Paramiko, Qiskit
- **Scenario**: SSH sessions using DH or ECDH for key exchange can be decrypted retroactively once quantum computers can solve discrete log or ECDLP problems.
- **Attack Steps**: Step 1: Attacker records an SSH handshake session (DH or ECDH based) including all exchanged public parameters. Step 2: For DH-based exchanges, the attacker retrieves values like g, p, and g^x mod p. Step 3: They run Shor’s algorithm on a quantum computer to solve for x (private exponent) from g^x. Step 4: If ECDH is used, Shor’s algorithm is applied to solve the ECC scalar multiplication Q = dG to recover private key d. Step 5: Once attacker has the private key, they compute the shared secret between client and server. Step 6: Using the shared secret and session key derivation steps, attacker reconstructs the SSH encryption and MAC keys. Step 7: Entire recorded SSH session (commands, data) can now be decrypted. Step 8: Critical for systems using long-lived keys or re-used ephemeral keys. Step 9: Real-time decryption is not currently feasible; however, stored sessions are future targets for decryption when quantum machines scale.
- **Detection**: Log protocol versions; monitor legacy key reuse
- **Solution**: Adopt post-quantum SSH (e.g., NTRU-HRSS hybrid exchange); don’t reuse ephemeral keys
- **Tags**: SSH, ECDH, DH, Quantum, Session Decryption

## PKI Infrastructure Compromise via RSA Break

- **Attack Type**: Digital Signature Forgery via RSA Factorization
- **Target**: PKI, CA Certificates, Code Signing
- **Vulnerability**: RSA digital signatures vulnerable to factorization
- **MITRE**: T1586 – Code Signing Abuse
- **Impact**: Complete PKI and trust model breakdown
- **Tools**: X.509 Viewer, OpenSSL, Qiskit
- **Scenario**: Quantum computers can break RSA-signed certificates in PKI (X.509), enabling attackers to forge valid signatures and impersonate trusted services.
- **Attack Steps**: Step 1: Attacker downloads an X.509 certificate (e.g., from a TLS-enabled website or email-signed message). Step 2: Extracts the RSA public key n and exponent e from the certificate. Step 3: Uses Shor’s algorithm on quantum computer or simulator to factor n and retrieve p and q. Step 4: Computes private key d using modular inverse with φ(n). Step 5: With d, attacker can sign arbitrary data (e.g., fake TLS certificate, fake code update, email, or software package) that will validate against the original certificate issuer. Step 6: Forge a fake certificate for any domain that appears to be signed by a trusted root CA (e.g., Google, Microsoft). Step 7: Distribute the fake certificate in phishing sites or malware delivery infrastructure. Step 8: Since browser trust chains are based on signature validation, victim browser or OS trusts the forged certificate. Step 9: Enables full man-in-the-middle (MITM) or malware trust bypass.
- **Detection**: Certificate transparency monitoring; signature algorithm auditing
- **Solution**: Use PQ-safe signatures (Dilithium, Falcon); sunset RSA certificates
- **Tags**: RSA, PKI, Certificates, Forgery, TLS, MITM

## Quantum Break of Bitcoin/Ethereum Wallets

- **Attack Type**: ECC Key Recovery in Cryptocurrency Wallets
- **Target**: Cryptocurrency Wallets
- **Vulnerability**: ECC-based wallet keys visible on public blockchain
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Theft of crypto assets; irreversible fund loss
- **Tools**: MetaMask, Etherscan, Qiskit, Electrum
- **Scenario**: Cryptocurrency wallets using ECC (e.g., secp256k1) are vulnerable to Shor’s algorithm, allowing quantum attackers to steal funds from exposed public keys.
- **Attack Steps**: Step 1: Understand that Bitcoin, Ethereum, and most cryptocurrencies use ECC (typically secp256k1) to generate key pairs. Public keys are used to derive wallet addresses. Step 2: As long as the private key is not exposed, the wallet is safe — but if a public key appears on-chain (e.g., during a transaction), it's visible. Step 3: Attacker monitors public ledgers for any wallet with known public key. Step 4: Uses Shor’s algorithm on a quantum computer to solve the ECDLP: recover the private key d from the public key Q = dG. Step 5: With private key, attacker can create transactions from that wallet, draining the funds. Step 6: In Bitcoin, change addresses or old-style non-P2SH scripts often expose public keys. Step 7: Ethereum exposes public keys with every transaction. Step 8: Attacker can queue attacks on high-value wallets for future quantum-era theft. Step 9: Mitigation is to move funds to PQ-safe or multi-signature contracts before quantum threat matures.
- **Detection**: Monitor transactions for public key reuse
- **Solution**: Use PQ-safe wallets or threshold/multi-sig smart contracts
- **Tags**: Blockchain, Wallet, ECC, Cryptocurrency, Shor’s

## Grover’s Algorithm on AES-128

- **Attack Type**: Quantum Speedup of Brute-Force Symmetric Attack
- **Target**: AES Encryption Algorithms
- **Vulnerability**: Symmetric key size vulnerable to quantum brute force
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Decryption of AES-128 secured communications
- **Tools**: Qiskit, IBM Q Experience, AES Lab Scripts
- **Scenario**: Grover’s algorithm allows a quantum computer to perform brute-force key search on AES-128 with only ~2^64 steps instead of 2^128, effectively halving its security level.
- **Attack Steps**: Step 1: Understand that AES-128 has 128-bit key space, requiring 2^128 attempts for a classical brute-force attack. Step 2: In a quantum setting, Grover’s algorithm can quadratically reduce this to about 2^64 steps. Step 3: Attacker programs Grover's oracle to identify the correct AES key by comparing output ciphertext against known plaintext. Step 4: The quantum oracle is designed to return ‘true’ when a key produces the correct ciphertext. Step 5: The attacker runs Grover’s iterative amplitude amplification circuit ~2^64 times. Step 6: When the quantum circuit converges, it collapses into the correct AES key with high probability. Step 7: The attacker now decrypts the full ciphertext using the recovered AES-128 key. Step 8: This attack is theoretical but will become feasible once large-scale fault-tolerant quantum computers exist. Step 9: Until then, data encrypted today with AES-128 may be vulnerable to future quantum recovery.
- **Detection**: Monitor for use of short symmetric key lengths
- **Solution**: Switch to AES-256 or use post-quantum symmetric ciphers
- **Tags**: AES, Grover’s Algorithm, Quantum, Symmetric Attack

## Grover’s Algorithm on Hash Functions (SHA-2)

- **Attack Type**: Collision & Preimage Reduction via Quantum Search
- **Target**: SHA-2, SHA-256 Hashing
- **Vulnerability**: Preimage and collision resistance weakened
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Signature forgery, data integrity compromise
- **Tools**: Qiskit, SHA256 Implementations, Python Hashlib
- **Scenario**: Grover’s algorithm halves the effective security of hash functions like SHA-256, reducing collision resistance and preimage resistance from 256 to 128 bits.
- **Attack Steps**: Step 1: Normally, finding a preimage (input that hashes to a known output) using SHA-256 requires 2^256 attempts. Step 2: Grover’s algorithm reduces this to approximately 2^128 quantum steps. Step 3: The attacker defines a Grover oracle that returns ‘true’ when a hash function produces the target hash. Step 4: They use a quantum circuit to iterate over possible inputs with amplitude amplification until it collapses to the input that matches the target hash. Step 5: In case of finding a collision (two different inputs with same hash), Grover’s reduces the work from 2^128 to ~2^64 steps. Step 6: Once a match is found, attacker can impersonate or forge data that passes hash-based integrity checks. Step 7: In digital signatures and data storage, this weakens trust if stronger hashing algorithms are not used. Step 8: Defender must assume SHA-2 is only 128-bit secure in the quantum age and upgrade accordingly. Step 9: Modern security standards will likely transition to SHA-3 or post-quantum hash functions.
- **Detection**: Audit hashing algorithm strength; measure hash length
- **Solution**: Use SHA-3, longer output (SHA-512), or post-quantum hashes
- **Tags**: SHA-2, Grover, Hash Attacks, Quantum Hashing

## Grover’s Algorithm on HMAC

- **Attack Type**: Quantum Brute-Force Reduction of HMAC Key Search
- **Target**: HMAC-SHA256, HMAC-SHA1
- **Vulnerability**: Brute-force attack on short HMAC key lengths
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Forgery of tokens, messages, or API requests
- **Tools**: Python HMAC Modules, Qiskit, HMAC Analyzer
- **Scenario**: HMACs (Hash-based Message Authentication Codes) using SHA-1 or SHA-2 are weakened by Grover’s algorithm, reducing their effective brute-force resistance by half.
- **Attack Steps**: Step 1: HMACs use a secret key and hash function to provide integrity/authentication. Step 2: In a classical setting, brute-forcing a correct HMAC key takes 2^k where k is key length. Step 3: Using Grover’s algorithm, attacker can reduce this to ~2^(k/2) attempts. Step 4: Attacker builds a Grover oracle that checks if an input key produces a known HMAC output for a specific message. Step 5: Quantum circuit iteratively amplifies the amplitude of the correct key’s probability. Step 6: After ~2^(k/2) steps, the correct key can be measured from the quantum state. Step 7: With this key, the attacker can forge valid HMACs for any message. Step 8: This breaks message integrity checks, token verification, or authentication schemes relying on HMAC. Step 9: Defenders must increase HMAC key size or switch to PQ-safe MACs.
- **Detection**: Monitor for fixed/short key usage in HMACs
- **Solution**: Use 256+ bit keys; adopt PQ-safe alternatives like KMAC
- **Tags**: HMAC, Grover, Integrity Attack, Quantum MAC

## Quantum Key Search on 3DES

- **Attack Type**: Grover Speedup Against Triple DES
- **Target**: 3DES, Legacy Systems
- **Vulnerability**: Quantum brute force reduces effective key strength
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Recovery of encryption key; legacy system compromise
- **Tools**: Qiskit, OpenSSL 3DES Suite, Cryptol
- **Scenario**: Triple DES (3DES), while once a standard, is vulnerable to quantum attacks since Grover’s algorithm reduces its 168-bit security to ~84-bit effort, which is insecure today.
- **Attack Steps**: Step 1: Triple DES encrypts data using three successive DES operations with either 2 or 3 keys. Step 2: The effective classical key space for 3DES with 3 keys is 2^168. Step 3: Grover’s algorithm reduces this to 2^84 quantum steps. Step 4: Attacker creates an oracle that tests possible keys against known ciphertext-plaintext pairs. Step 5: The quantum computer amplifies the state of the correct key candidate with each Grover iteration. Step 6: After ~2^84 steps, attacker collapses quantum state to retrieve the correct key. Step 7: With this key, full decryption is possible. Step 8: While 2^84 still exceeds current capabilities, this is below modern standards and vulnerable in future quantum scenarios. Step 9: Use of 3DES is already deprecated by NIST and should be eliminated in all systems.
- **Detection**: Scan systems for legacy cipher suites and outdated libraries
- **Solution**: Replace 3DES with AES-256 or post-quantum symmetric ciphers
- **Tags**: 3DES, Grover’s Attack, Key Search, Quantum Legacy

## Quantum Search on Symmetric PRFs/PRPs

- **Attack Type**: Grover-Based PRF/PRP Key Recovery
- **Target**: AES, DES, Custom PRFs/PRPs
- **Vulnerability**: Symmetric key space reduced by Grover’s search
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Full recovery of secret key, message decryption
- **Tools**: Qiskit, AES Test Vectors, PRF Models
- **Scenario**: Quantum attackers can use Grover’s algorithm to recover keys from symmetric cryptographic primitives like Pseudorandom Functions (PRFs) or Pseudorandom Permutations (PRPs).
- **Attack Steps**: Step 1: Understand that PRFs and PRPs (e.g., AES, block ciphers) use a secret key to map inputs to seemingly random outputs. Step 2: In a classical brute-force setting, recovering the key requires 2^n operations (n = key size). Step 3: A quantum adversary uses Grover’s algorithm to reduce key recovery complexity to ~2^(n/2). Step 4: The attacker defines a Grover oracle that outputs True only for the correct key that maps a known input to a known output. Step 5: The quantum circuit performs amplitude amplification iterations to focus probability on the correct key. Step 6: After ~2^(n/2) iterations, the quantum system collapses into the correct key state. Step 7: This attack breaks confidentiality and is especially dangerous against legacy PRFs/PRPs using short keys. Step 8: To prevent this, symmetric primitives must use at least 256-bit keys in the post-quantum era.
- **Detection**: Monitor use of deprecated PRFs and short keys
- **Solution**: Upgrade to AES-256 or use post-quantum secure symmetric primitives
- **Tags**: PRF, PRP, Quantum, Grover, Symmetric Cryptanalysis

## Quantum Pre-Image Attacks on Weak Hashes

- **Attack Type**: Grover Speedup for Pre-Image Discovery
- **Target**: MD5, SHA-1, Legacy Hashes
- **Vulnerability**: Pre-image resistance weakened by Grover
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Signature forgery, authentication bypass
- **Tools**: Qiskit, Hashing Libraries, Oracle Circuit Builder
- **Scenario**: Weak hash functions like MD5/SHA-1 allow attackers to find an input that produces a specific hash output with only ~2^(n/2) steps using Grover’s algorithm.
- **Attack Steps**: Step 1: The attacker starts with a target hash value (e.g., an encrypted password or digital signature hash). Step 2: The goal is to find any input that hashes to this target (pre-image). Step 3: In a classical setting, this takes 2^n time (n = hash output size). Step 4: Grover’s algorithm reduces this to ~2^(n/2) with a quantum computer. Step 5: Attacker builds a Grover oracle that returns True when the hash of an input equals the target hash. Step 6: The oracle is embedded in a quantum circuit that searches the input space. Step 7: After ~2^(n/2) steps, the quantum state collapses to a valid pre-image. Step 8: The attacker now possesses a fake input that validates as original, enabling authentication bypass or forged signatures. Step 9: Hashes like MD5 (128-bit) can be broken in real-time with future quantum computers, while even SHA-1 is unsafe. Step 10: Defenders must phase out weak hash functions in favor of SHA-3 or post-quantum alternatives.
- **Detection**: Scan for legacy hash use in code and protocols
- **Solution**: Enforce SHA-3, extend hash lengths, adopt PQC hash-based schemes
- **Tags**: Pre-image, Grover, Quantum Hashing, Forgery

## Quantum Birthday Collision Attack

- **Attack Type**: Quantum Collision Discovery on Hash Functions
- **Target**: Digital Signatures, Hashing
- **Vulnerability**: Collision resistance degraded to 2^(n/3)
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Fake identities, forged signatures, blockchain fraud
- **Tools**: Qiskit, Collision Oracles, Python Hash Simulator
- **Scenario**: A quantum computer reduces the complexity of finding two different inputs with the same hash value from 2^(n/2) to approximately 2^(n/3) using birthday-based quantum attacks.
- **Attack Steps**: Step 1: The classical birthday paradox implies that for an n-bit hash, a collision (two inputs with the same hash) can be found in 2^(n/2) attempts. Step 2: In a quantum setting, the Brassard-Høyer-Tapp (BHT) algorithm improves this to 2^(n/3) steps. Step 3: The attacker sets up two quantum registers: one for random input generation and another to monitor hash outputs. Step 4: A Grover-like quantum circuit samples the space and checks for repeating hashes among different inputs. Step 5: After enough iterations, a collision is statistically likely to occur and is captured in the measurement process. Step 6: The attacker now has two different messages with the same hash — useful in signature forgery, blockchain spoofing, or certificate manipulation. Step 7: This reduces trust in short hash digests (e.g., 160-bit SHA-1), making them unsafe. Step 8: Quantum-aware developers must design systems assuming only n/3 bits of security when considering collisions.
- **Detection**: Identify weak digests in digital signature chains
- **Solution**: Use hash functions with ≥384-bit output (e.g., SHA-3-384), adopt PQ standards
- **Tags**: Hash Collision, Quantum BHT, Birthday Attack

## Quantum Side-Channel Assisted Cryptanalysis

- **Attack Type**: Quantum-Aided Classical Side-Channel Analysis
- **Target**: Smartcards, Embedded Devices
- **Vulnerability**: Combined leakage and Grover-based speedup
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Cryptographic key recovery in real-time
- **Tools**: ChipWhisperer, Qiskit, Side-Channel Traces
- **Scenario**: Combines classical side-channel data (timing, EM leaks) with quantum search techniques (Grover/BHT) to drastically reduce cryptanalysis effort.
- **Attack Steps**: Step 1: Attacker collects physical side-channel data (e.g., power traces, EM emissions, timing logs) from a device performing cryptographic operations (AES, RSA, ECC). Step 2: These leak partial key bits or intermediate state values. Step 3: Normally, this leakage reduces the brute-force effort (e.g., 128-bit AES key space might narrow down to 2^40 candidates). Step 4: Grover’s algorithm is then applied to the reduced key space (e.g., 2^40 → 2^20 quantum effort). Step 5: The attacker builds a Grover oracle that tests key guesses using leaked intermediate states as validation points. Step 6: After ~2^(reduced/2) iterations, the correct key is recovered. Step 7: The fusion of classical and quantum attacks drastically accelerates cryptanalysis. Step 8: These attacks are practical once quantum computers can process larger input sizes. Step 9: Defenders must consider both physical hardening and quantum-resistant crypto.
- **Detection**: Monitor EM/Power emissions; audit for side-channel weaknesses
- **Solution**: Use hardened hardware, implement constant-time algorithms, migrate to PQC
- **Tags**: Side-Channel, Grover, Hybrid Quantum Cryptanalysis

## Quantum Speed-up of SAT Solvers for Cryptanalysis

- **Attack Type**: Quantum-enhanced Logic Solving for Ciphers
- **Target**: Lightweight Block Ciphers
- **Vulnerability**: Logic formula solvability via quantum-enhanced SAT solvers
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Cipher key recovery, breaking encrypted communication
- **Tools**: Qiskit, Quantum SAT Solver (qsat), CryptoMiniSat
- **Scenario**: Symmetric block ciphers can be modeled as logic formulas; quantum-enhanced SAT solvers reduce solving time, making full key recovery feasible on medium-sized ciphers.
- **Attack Steps**: Step 1: Understand that block ciphers (like AES, PRESENT) can be expressed as a Boolean satisfiability problem (SAT), where constraints represent encryption logic. Step 2: Normally, solving these constraints for the secret key is computationally intensive. Step 3: Quantum SAT solvers use quantum parallelism to evaluate large numbers of truth assignments simultaneously. Step 4: The attacker writes SAT clauses representing known plaintext-ciphertext pairs and the cipher's internal logic. Step 5: A Grover-style quantum circuit searches for satisfying assignments (key guesses) that satisfy all constraints. Step 6: The attack drastically reduces the time to solve the key compared to classical SAT solving. Step 7: The attacker uses real hardware (or simulator) to extract full or partial keys. Step 8: This is still experimental but represents a big threat once quantum hardware scales. Step 9: Ciphers with smaller rounds or linearity are more vulnerable.
- **Detection**: Analyze time complexity in SAT-modelable cipher use
- **Solution**: Increase cipher complexity, adopt non-linear/more rounds or PQC-safe schemes
- **Tags**: SAT Solvers, Grover, Logic Modeling, Quantum Cryptanalysis

## Quantum Attacks on Lattice-based Crypto (Heuristic)

- **Attack Type**: Heuristic/Hybrid Attacks on LWE, NTRU, Ring-LWE
- **Target**: NTRU, Kyber, Dilithium
- **Vulnerability**: Early-stage quantum attacks on lattice crypto
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Future possibility of breaking post-quantum encryption
- **Tools**: FPLLL, LWE Estimator, Qiskit
- **Scenario**: Lattice-based post-quantum schemes (e.g., NTRU, Kyber, Dilithium) rely on hard lattice problems; current research explores possible quantum speed-ups or vulnerabilities in corner cases.
- **Attack Steps**: Step 1: Understand that schemes like Kyber, NTRU, and Dilithium rely on the hardness of the Learning With Errors (LWE) or Ring-LWE problems. Step 2: Quantum computers are known to offer no exponential speedup for lattice problems — but some polynomial or hybrid advantage might exist. Step 3: The attacker applies lattice reduction techniques (e.g., BKZ, LLL) on intercepted public keys or ciphertexts. Step 4: A quantum computer may aid in either (a) speeding up discrete steps in reduction algorithms or (b) solving small instances of Shortest Vector Problem (SVP). Step 5: The attacker estimates complexity using tools like the LWE estimator. Step 6: Currently, no fully feasible quantum attack exists on strong lattice schemes — but research is ongoing into NTRU encryption variants or parameter weaknesses. Step 7: Developers should monitor parameter changes and only use vetted NIST PQC finalists.
- **Detection**: Check implementation parameters and audit usage of lattice crypto
- **Solution**: Use NIST-recommended parameter sets and track ongoing lattice cryptanalysis research
- **Tags**: Lattice, LWE, Ring-LWE, Quantum Research, NTRU, PQC

## Attacks on Supersingular Isogeny Crypto (SIDH/SIKE)

- **Attack Type**: Structural Attacks on Supersingular Isogeny Schemes
- **Target**: SIDH/SIKE Cryptosystems
- **Vulnerability**: Auxiliary point leakage in SIDH/SIKE
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Total key recovery, complete system compromise
- **Tools**: Magma, SageMath, SIDH Implementations
- **Scenario**: SIDH/SIKE used elliptic curve isogenies to build encryption/key exchange; recent classical attacks broke them entirely by using auxiliary points and torsion structure leakage.
- **Attack Steps**: Step 1: SIDH (Supersingular Isogeny Diffie-Hellman) uses operations between elliptic curves (isogenies) for key exchange. Step 2: A recent classical cryptanalysis by Castryck-Decru showed that SIDH can be broken by exploiting additional auxiliary points required for key validation. Step 3: The attacker uses known public parameters and cleverly manipulates the torsion structure of elliptic curves to compute the private isogeny path. Step 4: This removes the need for quantum resources — SIDH is considered broken even classically. Step 5: SIKE (a variant of SIDH) was a NIST PQC candidate, but it was withdrawn after this attack. Step 6: Quantum computers would have likely broken SIDH anyway, but the classical attack accelerated its retirement. Step 7: Organizations using SIDH must now immediately migrate to lattice or code-based post-quantum alternatives.
- **Detection**: Check for usage of SIDH/SIKE-based implementations
- **Solution**: Avoid supersingular isogeny cryptography for future use
- **Tags**: SIDH, SIKE, Isogeny, ECC, NIST-PQC, Broken Algorithms

## Harvest Now, Decrypt Later (HN-DL)

- **Attack Type**: Passive Post-Quantum Decryption of Archived Data
- **Target**: VPN, TLS, Email, SSH Archives
- **Vulnerability**: Long-term encrypted data at risk from future decryption
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Future exposure of sensitive communications or secrets
- **Tools**: Wireshark, Tcpdump, TLS Interceptors, HDD Arrays
- **Scenario**: Adversaries with access to encrypted traffic (VPN, TLS, SSH, emails) today can store it, and once quantum computers become viable, decrypt it retroactively if weak crypto was used.
- **Attack Steps**: Step 1: The attacker captures encrypted traffic (VPN tunnels, HTTPS sessions, SSH communications, etc.) using network sniffers like Wireshark or tcpdump. Step 2: The data is stored securely, waiting for a future date when quantum computers can break the encryption (e.g., RSA-2048, ECC P-256). Step 3: Once quantum hardware is available, the attacker applies Shor’s algorithm to decrypt RSA/ECC-based session keys. Step 4: The attacker replays the captured data, now decrypting the full content (messages, credentials, API keys, etc.). Step 5: This can expose years of stored emails, financial records, or communications. Step 6: Even encrypted backups using classical crypto are at risk. Step 7: This is why “quantum-safe today” is critical — attackers may already be harvesting your encrypted data. Step 8: To prevent future breaches, encrypted systems must adopt post-quantum algorithms now. Step 9: Forward secrecy protocols (e.g., TLS 1.3) help mitigate some risk but are still vulnerable if underlying algorithms are broken.
- **Detection**: Track legacy encrypted storage, encrypted traffic flow
- **Solution**: Use hybrid crypto (PQC + classic), move to quantum-safe encryption today
- **Tags**: Harvest-Decrypt, Passive Attack, Long-Term PQC Risk

## Quantum Chosen-Ciphertext Attack (CCA) Enhancements

- **Attack Type**: Quantum-Oriented Adaptive CCA
- **Target**: Lattice-based KEMs, PQ Encryption
- **Vulnerability**: Lack of QROM-secure CCA resilience
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Decryption of ciphertexts, key recovery, signature forgery
- **Tools**: Qiskit, Lattice KEM Simulators, Hybrid Oracle Models
- **Scenario**: Classical CCA attacks can be enhanced by quantum query access to decryption oracles, enabling attackers to forge ciphertexts or decrypt messages with fewer queries. This especially affects lattice- or code-based encryption under improper CCA security.
- **Attack Steps**: Step 1: Understand the traditional Chosen-Ciphertext Attack (CCA), where an attacker can submit crafted ciphertexts to a decryption oracle to learn about the plaintext or keys. Step 2: In a post-quantum context, an attacker with access to a quantum computer can query a quantum decryption oracle — meaning it can submit and receive a superposition of ciphertexts. Step 3: This enables massively parallel testing of ciphertext validity or patterns. Step 4: With structured schemes (like some lattice-based KEMs), the attacker may gain enough distinguishing power to forge ciphertexts that pass verification or retrieve key bits. Step 5: The attack is more efficient than classical adaptive CCA and can be mounted with fewer queries. Step 6: This highlights that cryptosystems must be secure in the quantum Random Oracle Model (QROM) and not just classical CCA-secure. Step 7: This is theoretical but highly important when designing post-quantum secure protocols. Step 8: Cryptographers model such oracles to simulate this attack and test future-safe schemes.
- **Detection**: Evaluate CCA robustness using quantum oracle simulation tools
- **Solution**: Use QROM-secure lattice schemes (e.g., Kyber-CCA-secure variants)
- **Tags**: CCA, QROM, Quantum Forgery, PQC

## Quantum-enhanced Brute Force for Password Cracking

- **Attack Type**: Grover-Based Brute Forcing
- **Target**: Password Hashes, API Keys
- **Vulnerability**: Reduced hash security due to Grover’s algorithm
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Password/key recovery with fewer operations
- **Tools**: Qiskit, Hashcat (conceptual), Grover Simulators
- **Scenario**: Grover's algorithm allows attackers to search for the correct password/hash pre-image in roughly √N time, halving the effective key or hash strength (e.g., 128-bit hash → 64-bit security).
- **Attack Steps**: Step 1: Traditional password cracking involves hashing a guessed password and checking if it matches the stored hash. This is time-consuming and requires checking all possible combinations (e.g., millions or billions). Step 2: Quantum computing introduces Grover's algorithm, which provides a quadratic speedup. Step 3: The attacker expresses the hash checking logic as a quantum oracle (i.e., a circuit that returns 1 if a password guess is correct). Step 4: Grover's algorithm iteratively amplifies the probability amplitude of the correct password over wrong guesses. Step 5: This allows the correct password to be guessed in approximately √N steps instead of N (e.g., 2⁶⁴ steps instead of 2¹²⁸). Step 6: This weakens common hash algorithms (SHA-256, bcrypt) used in password databases. Step 7: The attack assumes the attacker has access to a quantum computer and hash logic of the system. Step 8: Defenders must now consider passwords with entropy ≥256 bits to stay safe. Step 9: This applies to not just passwords but any brute-forceable secrets (like API keys, license keys, etc.).
- **Detection**: Monitor login attempts and unusual timing characteristics
- **Solution**: Use password hashing with memory-hard functions (Argon2), and longer passwords
- **Tags**: Grover, Brute Force, Hash Cracking, Quantum Speedup

## Quantum State Cloning in QKD Attacks

- **Attack Type**: Quantum Key Distribution Protocol Exploits
- **Target**: Quantum Key Distribution Devices
- **Vulnerability**: Device-level QKD protocol imperfections
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Partial or full recovery of supposedly quantum-safe keys
- **Tools**: QKD Simulator, Optics Toolkit, Quantum Probe Devices
- **Scenario**: QKD (e.g., BB84) claims unconditional security using quantum physics (no-cloning theorem), but experimental side-channel or cloning-like attacks try to extract key bits during transmission or measurement.
- **Attack Steps**: Step 1: Understand that Quantum Key Distribution (QKD) relies on quantum principles like the no-cloning theorem — meaning an attacker cannot copy a quantum bit (qubit) without disturbing it. Step 2: In BB84, two parties exchange qubits over a quantum channel and use classical communication to finalize a shared key. Step 3: An attacker (Eve) may try to extract information using imperfect cloning techniques or measurement-device-dependent vulnerabilities. Step 4: Eve uses advanced optical devices (e.g., quantum probes) to measure certain qubits during transmission and reconstruct possible bits. Step 5: Even though perfect cloning isn't possible, partial measurements can give her statistical knowledge. Step 6: Eve waits for the public reconciliation phase to align her guesses. Step 7: If the QKD protocol isn't authenticated or the devices are flawed, Eve may succeed in partial or full key reconstruction. Step 8: This is an area of active research and a real concern for future QKD networks. Step 9: Experimental attacks like photon-number-splitting or time-shift can also bypass no-cloning in certain setups.
- **Detection**: Analyze quantum channel for error rates and external interference
- **Solution**: Use measurement-device-independent QKD and secure implementation validation
- **Tags**: QKD, No-Cloning, BB84, Quantum Cryptography, Photon Attacks

## Quantum Random Oracle Model Breaks

- **Attack Type**: Oracle-Based Cryptanalysis Under Quantum Model
- **Target**: ROM-based Signature and KEM Schemes
- **Vulnerability**: Lack of resistance to quantum oracle superposition queries
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Signature forgery, encryption/key exchange compromise
- **Tools**: CryptoLibs, QROM Proof Simulators
- **Scenario**: Some classical security proofs assume the Random Oracle Model (ROM); quantum adversaries can break schemes not secure under the Quantum ROM (QROM), leading to real-world crypto vulnerabilities.
- **Attack Steps**: Step 1: Many classical cryptographic proofs assume a Random Oracle Model (ROM), where a hash function is treated as a black box giving random outputs. Step 2: However, quantum attackers can query the oracle in superposition, which breaks the assumptions of classical ROM. Step 3: This affects cryptographic protocols that assume random oracle behavior remains unchanged in a quantum world. Step 4: The attacker leverages this to break commitments, signatures, or key exchanges that rely on classical ROM assumptions. Step 5: Using tools like the QROM security models, cryptanalysts can simulate and prove whether a scheme is still secure under quantum oracle queries. Step 6: If not, the attacker can perform attacks such as forgery or decryption by using amplitude amplification and quantum structure. Step 7: This highlights that classical proofs are not enough — even PQC algorithms must be proven under QROM security. Step 8: Many older schemes fail this and are vulnerable. Step 9: Ongoing work focuses on creating QROM-secure versions of classical protocols.
- **Detection**: Validate QROM assumptions in all cryptographic scheme deployments
- **Solution**: Use only QROM-secure KEMs/signatures (e.g., Dilithium, Kyber)
- **Tags**: QROM, Signature Forgery, Oracle Models, Grover Variant

## Quantum Attacks on Blockchain Consensus

- **Attack Type**: Consensus Manipulation via Quantum Forgery or Mining Bias
- **Target**: PoW/PoS Blockchain Nodes
- **Vulnerability**: Quantum breaking of ECDSA, Grover-aided mining advantage
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: 51% attacks, block manipulation, double spending
- **Tools**: Qiskit, Simulated Blockchain, PoW Hash Testing
- **Scenario**: Quantum computing can affect Proof-of-Work (PoW) and Proof-of-Stake (PoS) consensus mechanisms by providing unfair mining advantages (Grover) or exploiting cryptographic vulnerabilities (e.g., ECDSA in signing).
- **Attack Steps**: Step 1: Understand that blockchains rely on distributed consensus—miners or validators must solve puzzles (e.g., SHA-256 PoW) or stake tokens to verify transactions. Step 2: In a PoW blockchain (e.g., Bitcoin), Grover’s algorithm allows a quadratic speedup in mining by reducing the effort to solve the hash puzzle. Step 3: This gives quantum miners an advantage over classical nodes, threatening fair competition and decentralization. Step 4: In PoS blockchains using ECDSA signatures (e.g., Ethereum 1.0), Shor’s algorithm can break elliptic curve cryptography if a quantum adversary observes signatures over time. Step 5: The attacker recovers private validator keys, allowing them to forge blocks, double spend, or manipulate consensus. Step 6: If multiple validators are compromised, the attacker may launch a 51% attack. Step 7: In hybrid protocols, the attacker could combine Grover-based mining and ECDSA key recovery for multi-pronged consensus compromise. Step 8: Defenders must prepare for post-quantum cryptographic upgrades in consensus-critical layers.
- **Detection**: Detect hash solving time anomalies and check stake validator signature patterns
- **Solution**: Upgrade blockchain signing algorithms to post-quantum (e.g., Falcon, Dilithium); use PQ-friendly consensus models
- **Tags**: Blockchain, PoW, PoS, Grover, ECDSA, Shor, PQ Upgrade

## Quantum Bias Exploitation in PRNGs

- **Attack Type**: Exploiting PRNG Bias via Quantum Algorithms
- **Target**: Session Tokens, API Keys, IoT Devices
- **Vulnerability**: Low-entropy or biased PRNGs
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Predictable secrets, replay, session hijack
- **Tools**: Qiskit, Entropy Estimators, Custom PRNG Code
- **Scenario**: Poorly seeded or biased pseudorandom number generators (PRNGs) can be analyzed more efficiently using quantum algorithms to extract entropy, deduce keys, or recover session tokens.
- **Attack Steps**: Step 1: Understand that PRNGs generate "random-looking" numbers from an internal state (seed). If the seed or algorithm is weak, an attacker can predict or narrow down future outputs. Step 2: Classical attackers brute-force the seed space or reverse-engineer the PRNG using statistical analysis. Step 3: Quantum attackers use advanced quantum state analysis or Grover’s algorithm to find biases and collapse the space of likely outputs much faster. Step 4: For example, if the PRNG uses a timestamp as a seed (common in IoT or embedded devices), the attacker guesses timestamp ranges and applies Grover’s search to discover likely seeds. Step 5: With known or partial outputs, the attacker uses quantum-enhanced SAT solvers or amplitude amplification to reconstruct PRNG internals. Step 6: This reveals session tokens, encryption keys, or API secrets. Step 7: Devices using unverified custom PRNGs or not using proper entropy sources are especially vulnerable. Step 8: Developers must follow standards like NIST DRBG or hardware TRNGs for cryptographic use.
- **Detection**: Monitor token issuance patterns and entropy usage in crypto modules
- **Solution**: Use only FIPS-approved PRNGs (e.g., NIST DRBG); avoid custom PRNGs
- **Tags**: PRNG, Grover, Entropy Leak, Token Prediction

## Quantum Tampering with QKD Infrastructure

- **Attack Type**: Hardware/Protocol Tampering in QKD Setups
- **Target**: QKD Devices, Telecom Fiber Links
- **Vulnerability**: Side-channel leakage in QKD hardware/protocol layers
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Partial or full leakage of QKD-generated keys
- **Tools**: Fiber QKD Systems, Side-Channel Probes, Timing Analyzers
- **Scenario**: Though QKD promises theoretical security, quantum side-channels and physical-layer attacks (e.g., timing, power, optical) can tamper with key generation or leak key material in real-world QKD setups.
- **Attack Steps**: Step 1: QKD systems (like BB84 protocol) use physical quantum properties (e.g., polarization) to exchange secure keys. Step 2: Real-world devices, however, suffer from side-channels (e.g., photon timing, optical reflections). Step 3: The attacker may position a passive tap or optical splitter on the fiber line to analyze photon timing and match bit choices. Step 4: Alternatively, the attacker may inject light pulses or introduce delay/noise to interfere with the photon reception process. Step 5: Using fast detectors and quantum state comparison techniques, the attacker attempts to extract partial key bits without triggering alarms. Step 6: Many attacks exploit the mismatch in detector efficiency or rely on injecting extra photons to trick the receiving side. Step 7: Some hardware allows manipulation of basis choice or measurement settings due to firmware flaws. Step 8: If the attacker can stay below the QBER (quantum bit error rate) detection threshold, they can exfiltrate bits over time. Step 9: Hardware certification, shielding, and strict entropy auditing are essential.
- **Detection**: Analyze QBER for unexplained variations; use side-channel detection hardware
- **Solution**: Use measurement-device-independent QKD; conduct regular side-channel audits
- **Tags**: QKD, Side-Channel, Fiber Tampering, Quantum Infra Threat

## Quantum Assisted Message Forgery (e.g., MACs)

- **Attack Type**: Forging MACs Using Quantum Techniques
- **Target**: HMAC-SHA MACs, Firmware Auth Systems
- **Vulnerability**: Short MACs vulnerable to quantum brute-force search
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Message spoofing, firmware injection, data manipulation
- **Tools**: Qiskit, HMAC Libraries, Hash Simulators
- **Scenario**: Quantum computing can help attackers forge Message Authentication Codes (MACs) by exploiting algebraic structure or performing fast search using Grover’s algorithm, compromising data integrity.
- **Attack Steps**: Step 1: MACs (Message Authentication Codes) are used to verify data integrity and authenticity. Common forms include HMAC-SHA256. Step 2: In classical brute-force, forging a MAC requires trying 2^128 combinations for a 128-bit tag. Step 3: With Grover’s algorithm, the search space shrinks to √(2^128) = 2^64, making brute-force plausible on quantum hardware. Step 4: The attacker encodes the MAC verification function as a quantum oracle that returns 1 if the guess is a valid MAC for a known message. Step 5: Grover’s loop amplifies the probability of the correct tag being returned over time. Step 6: After sufficient iterations, the attacker finds a valid MAC, allowing them to forge a message that appears authentic. Step 7: This undermines data integrity, especially in systems that rely solely on short MACs or fail to rotate keys often. Step 8: This attack becomes more feasible when message contents are known or predictable (e.g., in IoT APIs, firmware updates). Step 9: Organizations must ensure cryptographic primitives have post-quantum security levels or increase key/MAC lengths accordingly.
- **Detection**: Watch for mismatched MAC-tagging patterns or repeated MAC guessing attempts
- **Solution**: Use longer MACs (e.g., 256-bit), PQ-safe alternatives like KMAC or Keccak with larger output sizes
- **Tags**: MAC Forgery, Grover, HMAC, Quantum Brute Force

## Classical Hash Collision Attack

- **Attack Type**: Hash Function Collision
- **Target**: MD5, SHA-1 systems
- **Vulnerability**: Broken collision resistance
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Forgery, data tampering, digital signature bypass
- **Tools**: HashClash, OpenSSL, Python hashlib
- **Scenario**: A hash function generates the same output for two different inputs (collision), violating its core property. Known in MD5, SHA-1.
- **Attack Steps**: Step 1: Choose a vulnerable hash function such as MD5 or SHA-1, both of which are cryptographically broken. Step 2: Install tools like HashClash, which allows you to generate hash collisions for chosen inputs. Step 3: Prepare two distinct input files or messages. Step 4: Use the tool to create small binary differences between the inputs while still producing the same hash output. Step 5: Verify using a hashing tool (e.g., openssl dgst -md5 file1 file2) and confirm both files return the same hash. Step 6: This attack shows how two entirely different files (e.g., PDF contracts) can appear "unchanged" by comparing only their hashes. Step 7: Useful in digital forgery or signature spoofing if hashes are blindly trusted. Step 8: To avoid detection, attackers often embed malicious logic in one file and safe content in another while keeping the hash identical.
- **Detection**: Monitor use of legacy hash functions like MD5 or SHA-1 in signing or validation systems
- **Solution**: Migrate to SHA-256 or SHA-3; enforce hash length ≥ 256-bit
- **Tags**: MD5, SHA-1, Hash Collision, Forgery

## Birthday Attack

- **Attack Type**: Collision Attack Using Birthday Paradox
- **Target**: Weak checksum systems
- **Vulnerability**: Short/truncated hash use
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Token forgery, duplicate detection evasion
- **Tools**: Python, Hashcat, Custom Scripts
- **Scenario**: Exploits the math behind birthday paradox to find collisions in hash functions faster than brute force (about 2^(n/2) attempts).
- **Attack Steps**: Step 1: Understand that a 64-bit hash function doesn't require 2^64 attempts for a collision—only about 2^32 (due to birthday paradox). Step 2: Create a program that generates a large number of random inputs and hashes them using the target hash algorithm (e.g., SHA-1). Step 3: Store these hashes and compare them in real-time. Step 4: Continue until a match is found (two inputs generating the same hash). Step 5: For longer hash lengths (128, 160 bits), use GPU-based hash collision generators like Hashcat or write parallel scripts. Step 6: This attack is practical for lower-bit hashes or truncated outputs (e.g., 64-bit checksums). Step 7: Once a collision is found, demonstrate how both inputs produce the same hash output even though they are different. Step 8: This is a probabilistic attack and highlights why all secure systems must avoid short or truncated hash outputs.
- **Detection**: Monitor large-scale hash attempts; detect multiple inputs with same hash
- **Solution**: Increase hash size to 256-bit or more; disallow short output-based verification
- **Tags**: Birthday Paradox, Hash Collision, Token Bypass

## Chosen-Prefix Collision Attack

- **Attack Type**: Targeted Hash Collision (Controlled Prefix)
- **Target**: SHA-1 digital signatures
- **Vulnerability**: Predictable hash inputs in weak hash schemes
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Forgery of legally binding or signed documents
- **Tools**: SHA1CLASH, SLOTH tool
- **Scenario**: Attacker crafts two distinct messages with attacker-chosen prefixes that still produce the same hash (e.g., in SHA-1).
- **Attack Steps**: Step 1: Understand that chosen-prefix attacks go beyond finding any collision—they allow you to define the start of each input (the prefix). Step 2: Install SHA1CLASH (available on GitHub), a tool designed to generate chosen-prefix collisions in SHA-1. Step 3: Prepare two prefix messages (e.g., contract_A and contract_B) and use the tool to generate suffixes that collide. Step 4: Combine each prefix with its respective generated suffix. Both full messages will now produce the same SHA-1 hash. Step 5: Use sha1sum or similar tool to verify the hashes match. Step 6: This is useful in real-world forgery, such as crafting fake certificates or legal documents where the visible prefix differs but hash matches. Step 7: Because the attacker can choose both prefixes, they have more flexibility than classical attacks. Step 8: This attack works only on weak hash functions like SHA-1. Modern SHA-2 and SHA-3 resist this.
- **Detection**: Detect multiple signature verifications using SHA-1 with different message content
- **Solution**: Ban use of SHA-1 in signing schemes; adopt SHA-3, HMAC, or PQ-safe hashes
- **Tags**: SHA-1, Prefix Collision, Digital Forgery

## Identical-Prefix Collision Attack

- **Attack Type**: Same Prefix, Colliding Suffix
- **Target**: File validation systems
- **Vulnerability**: Hash validation based on prefix-only format
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Document tampering, file substitution
- **Tools**: FastColl, HashClash
- **Scenario**: Exploits the same hash output for inputs with identical prefixes but different suffixes. Known for MD5 and early SHA-1.
- **Attack Steps**: Step 1: In this attack, both inputs start with the same prefix (e.g., header of a PDF or JPEG) but differ in the suffix. Step 2: Use tools like FastColl or HashClash to generate these collisions. Step 3: Supply the shared prefix (e.g., PDF-Header-Template) and allow the tool to generate two suffixes that when appended still hash to the same MD5/SHA-1 value. Step 4: The result is two valid files with shared header and different content, but they hash identically. Step 5: Confirm using md5sum file1 file2 or Python hashlib. Step 6: This technique is ideal for attacks where format constraints exist (e.g., same file format), but suffixes can vary. Step 7: Attackers may hide malicious payloads in one file while presenting a clean copy for validation. Step 8: Works in systems that validate files or messages only based on their hash, not actual content. Step 9: Often used in digital contract manipulation, malware evasion, or tricking signature verification tools.
- **Detection**: Inspect suffix content of identically hashed files with same prefix
- **Solution**: Use contextual file/content validation beyond hashes; migrate to SHA-256 or SHA-3
- **Tags**: Prefix Collision, MD5, File Forgery

## Appendable Collision

- **Attack Type**: Post-Collision Extension in Iterative Hashes
- **Target**: Legacy MD5-based systems
- **Vulnerability**: Iterative structure allowing length extension
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Digital signature spoofing, stealth tampering
- **Tools**: HashClash, Python, OpenSSL
- **Scenario**: Some hash functions (like MD5) allow attackers to extend collided messages with additional data while retaining same hash output.
- **Attack Steps**: Step 1: Understand that MD5 and similar iterative hash functions allow for "length extension" — meaning you can append data to already-colliding inputs and keep the hash collision intact. Step 2: Use HashClash to generate two colliding inputs, say input1 and input2, that hash to the same value. Step 3: Append arbitrary new data (e.g., .exe payload, malicious JS, or alternate document content) to both inputs. Step 4: Because of the Merkle–Damgård construction used by MD5, the final state remains compatible if crafted carefully. Step 5: This trick is especially powerful when the original message is signed or verified using only a hash. Step 6: Verify by hashing both appended files using md5sum and confirm they still produce identical hashes. Step 7: This method enables attackers to sign one message and later append malicious content without invalidating the signature. Step 8: These attacks require understanding padding, so use toolkits like md5collgen or HashClash which handle it for you.
- **Detection**: Monitor use of MD5 in signing schemes; inspect appended content beyond the hash
- **Solution**: Avoid MD5; use hash constructions immune to extension (e.g., HMAC, SHA-3)
- **Tags**: Appendable Collision, MD5, Forged Signatures

## Multicollision Attack

- **Attack Type**: Generating Multiple Inputs with Same Hash
- **Target**: MD5, SHA-1 systems
- **Vulnerability**: Structural weaknesses in hash chaining
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Massive hash collisions, system confusion
- **Tools**: HashClash, Python Scripts
- **Scenario**: Instead of just 2 collisions, attackers create many different inputs (e.g., 8, 16) that all hash to the same output. Used to amplify attacks on systems.
- **Attack Steps**: Step 1: Multicollision attacks build on regular collision attacks, but the attacker creates many inputs (more than 2) that hash to the same value. Step 2: Start with a collision generator like HashClash and use its multicollision modules. Step 3: Generate an initial collision pair — msg1 and msg2. Step 4: Now treat those two as base blocks and repeat the collision process on each branch. Step 5: In two more rounds, you'll have 4 and then 8 messages all with the same hash. Step 6: Each message looks different, but due to internal structure and padding manipulation, they produce the same hash (like MD5). Step 7: Use these in exploit scenarios like document forgery, malware evasion, or digital signature ambiguity. Step 8: Verify using md5sum file1 file2 … file8 — all return identical hashes. Step 9: This is highly effective in systems that depend solely on hash uniqueness for file or transaction integrity.
- **Detection**: Detect same hashes for different content; log multi-match hash events
- **Solution**: Migrate to SHA-3 or collision-resistant functions; validate full content
- **Tags**: Multicollision, MD5, SHA-1, Forgery, Hash Abuse

## Expanded Collision (k-way Collision)

- **Attack Type**: Create k Inputs (k>2) with Same Hash
- **Target**: Antivirus, patching systems
- **Vulnerability**: Multiple input collisions per hash
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Bypass of integrity verification, AV evasion
- **Tools**: Custom Python Toolkit, HashClash
- **Scenario**: Advanced form of multicollision where attacker creates k messages that collide (e.g., 16, 32) — useful in software integrity subversion.
- **Attack Steps**: Step 1: Understand that while most hash collisions involve 2 messages, attackers can scale this to many more (k > 2) using tree-based chaining of collisions. Step 2: Begin with a single pair of colliding inputs using a known attack (e.g., HashClash). Step 3: Use recursive techniques to apply new collisions to both branches, forming a binary tree of hash collisions. Step 4: For every round, the number of colliding messages doubles: 2 → 4 → 8 → 16 → k. Step 5: Ensure that the padding and length fields are preserved between rounds to maintain valid collisions. Step 6: After generating the k-way collision, verify using hash tools like openssl dgst or hashlib. Step 7: This technique can be used to create sets of malware samples that evade hash-based detection or commit replay in systems that rely solely on hash checks. Step 8: This is a powerful tool for subverting integrity validation in software packages, containers, or update systems using MD5/SHA-1.
- **Detection**: Track excessive hash reuse; flag k-match cases
- **Solution**: Use stronger hashes with random salt or MACs (e.g., SHA-3, HMAC)
- **Tags**: Multicollision, MD5, Hash Evasion, Binary Tree Attack

## Near-Collision Attack

- **Attack Type**: Hash Outputs Differing by Few Bits
- **Target**: Weak hash-based detection
- **Vulnerability**: Weak diffusion in hash function
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Anti-virus evasion, fuzzy hash spoofing
- **Tools**: Python, Crypto++, Custom Scripts
- **Scenario**: Attackers find two inputs whose hashes differ by only a few bits — useful in breaking hash function diffusion or AV fuzzing.
- **Attack Steps**: Step 1: Understand that a "near-collision" is when two different inputs produce hashes that differ by only a small number of bits (e.g., 1-4). Step 2: Write a Python script that hashes many pairs of inputs using hashlib (e.g., SHA-1, MD5) and compares the bit difference of each result. Step 3: Use bin() to convert hash digests into binary and xor() to measure how many bits differ. Step 4: After several thousand tests, identify input pairs with the smallest bit difference. Step 5: This shows how diffusion (a key cryptographic property) fails in weak hash algorithms, since small input changes should produce totally different outputs. Step 6: Near-collisions may indicate potential for full collision or predictability. Step 7: These are useful in evading filters (e.g., AV or IDS) that allow small hash variation or use fuzzy hashing. Step 8: Can also be used to reverse-engineer how a hash affects classification models or ML integrity checks.
- **Detection**: Analyze Hamming distance in suspicious hashes; monitor bitwise differences
- **Solution**: Choose hash functions with avalanche effect and strong diffusion (e.g., BLAKE2, SHA-3)
- **Tags**: Near-Collision, Weak Hash, AV Evasion, Fuzzy Hashing

## Partial Collision Attack

- **Attack Type**: Hash Subset Collision
- **Target**: Shortened-hash systems
- **Vulnerability**: Short-hash comparison leading to weak integrity
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Cache poisoning, weak signature bypass
- **Tools**: Python, Hashcat, Custom Script
- **Scenario**: Instead of full collision, attacker matches a subset (e.g., first 16 or 24 bits) of the hash. Still effective in systems with shortened or truncated hash use.
- **Attack Steps**: Step 1: Understand that some systems store or compare only a portion of the hash (e.g., first 4 or 6 hex characters). This drastically reduces collision resistance. Step 2: Write a script in Python using hashlib to continuously hash different inputs and check if the first N bits/hex characters match a target value. Step 3: For example, try to find inputs with the same first 24 bits (3 bytes) using a brute-force loop. Step 4: Use hash slicing, like hashlib.sha256(data).hexdigest()[:6], to compare. Step 5: When a match is found, you've achieved a partial collision. This can be used in URL shortening, commit IDs, or systems using short hash representations. Step 6: This is also useful for cache poisoning, API key lookups, or fuzzing signature checks. Step 7: You can speed this up using Hashcat with custom masks. Step 8: Partial collisions can still be devastating when misused in places expecting full security.
- **Detection**: Detect short-hash comparisons; monitor repeated input attempts
- **Solution**: Always use full hash comparisons; never truncate cryptographic hashes
- **Tags**: Short Hash, Partial Collision, Hash Truncation

## Second Preimage Collision Attack

- **Attack Type**: Alternate Input Same Hash
- **Target**: MD5/SHA-0/Truncated hashes
- **Vulnerability**: Weak resistance to second preimage attempts
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Signature forgery, message substitution
- **Tools**: Hashcat, OpenSSL, John the Ripper
- **Scenario**: Attacker generates a new input that matches the hash of a known original input, useful when attacker cannot choose original message.
- **Attack Steps**: Step 1: Second preimage attacks aim to find a different message (M2) that produces the same hash as a given message (M1). This is more difficult than generating two random collisions. Step 2: Use weak hash algorithms like MD5, SHA-0, or truncated hashes (e.g., 64-bit SHA-1) to attempt this. Step 3: Input the known original message (M1) and compute its hash using md5sum or hashlib. Step 4: Use a brute-force tool like Hashcat with a dictionary or mask attack to try different M2 inputs. Step 5: For each candidate, hash it and compare with the original hash. Step 6: If a match is found, you've created a second preimage — a different message with the same hash. Step 7: This attack is mostly feasible against older hashes and short hash lengths. Step 8: Applications: document forgeries, commit tampering, or hash-based signature bypass. Step 9: Modern hashes like SHA-3 are resistant; focus on legacy systems for this attack.
- **Detection**: Log when two different files produce same hash; detect suspicious duplicate hashes
- **Solution**: Use preimage-resistant hash functions (SHA-2+, SHA-3); include salt or key in hash generation
- **Tags**: Second Preimage, Legacy Hash, MD5 Forgery

## MD5 Collision Attack

- **Attack Type**: MD5 Collisions for Forged Files
- **Target**: SSL certs, signed files, AV
- **Vulnerability**: Predictable hash collisions in MD5
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Code signing bypass, fake certs, malware undetection
- **Tools**: HashClash, FastColl, OpenSSL, Linux Tools
- **Scenario**: MD5 allows generation of two distinct messages with the same hash. Attackers exploit this to forge SSL certificates, sign malware, or tamper documents undetected.
- **Attack Steps**: Step 1: Use FastColl or HashClash tools to generate two different files (or binaries) that hash to the same MD5 value. These are typically crafted PDF, EXE, or image files. Step 2: Prepare two different messages (e.g., benign vs malicious) with common structure. Step 3: Use the tools to inject collision blocks into the files. Step 4: Verify both files produce identical MD5 hashes using md5sum file1 file2. Step 5: You can now submit the benign file for digital signing or AV approval. Step 6: Later replace it with the malicious version, as the hash is identical. Step 7: This was famously used in real-world certificate forgery attacks. Step 8: This attack is reliable, documented, and requires only basic command-line usage. Step 9: Try examples available in HashClash GitHub for hands-on testing. Step 10: Avoid running malicious payloads outside a VM or sandbox.
- **Detection**: Scan for duplicate hashes; flag MD5 use in digital signatures
- **Solution**: Ban MD5 in signing, AV, and certificate infrastructure; replace with SHA-2 or SHA-3
- **Tags**: MD5 Collision, Signed Malware, SSL Certificate Forgery

## SHA-1 Collision Attack (SHAttered)

- **Attack Type**: Forged PDFs and Files using SHA-1 Collision
- **Target**: PDF, Git, software signing
- **Vulnerability**: Practical SHA-1 collision feasibility
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Digital forgery, patch manipulation, false trust
- **Tools**: SHAttered Toolkit, Python, PDF tools
- **Scenario**: First publicly known SHA-1 collision attack (SHAttered) generated two PDFs with same hash but different content, showing practical collision viability.
- **Attack Steps**: Step 1: Understand that SHA-1 was once widely used in certificates, Git, and digital signatures. Step 2: Google and CWI Amsterdam published a real-world collision attack called SHAttered. Step 3: Download the official SHAttered toolkit or example PDFs from https://shattered.io. Step 4: Examine both files — one is benign, one is malicious, yet both produce the same SHA-1 hash. Step 5: Use sha1sum to confirm that doc1.pdf and doc2.pdf return the same hash value. Step 6: This attack leveraged advanced GPU computing but can now be reproduced using pre-generated collision blocks. Step 7: Attackers can use this to trick systems validating signed documents or patches using SHA-1. Step 8: Try inserting SHA-1 collision blocks into your own documents using PDF tools. Step 9: Practical use: forge a software update file or PDF that appears trusted by its hash. Step 10: This marks the deprecation of SHA-1 for security-critical applications.
- **Detection**: Detect SHA-1 usage in signed content; hash duplication tracking
- **Solution**: Fully deprecate SHA-1 in software signing, certs, and Git; migrate to SHA-256+
- **Tags**: SHA-1, SHAttered, Forged Documents, Git Spoof

## GIT Collision Vulnerability (SHA-1)

- **Attack Type**: Git SHA-1 Collision
- **Target**: Git Repositories
- **Vulnerability**: SHA-1 hash collision risk
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Malicious commits, repo integrity compromise
- **Tools**: Git CLI, shattered.io PDF, Python Scripts
- **Scenario**: Git originally used SHA-1 to identify commits and objects. SHA-1 collisions pose a serious risk, allowing attackers to create fake commits or objects.
- **Attack Steps**: Step 1: Understand that Git uses SHA-1 hashes to track versions of files and commits. A hash collision means two different files or commits can produce the same SHA-1. Step 2: Download the two PDF files from shattered.io that have the same SHA-1 hash but different content. Step 3: Run git hash-object on both files. Git will treat them as identical objects even though their contents differ. Step 4: Imagine an attacker creates a malicious file and a benign-looking file with the same SHA-1. The benign one is reviewed and signed; the malicious one is then swapped in using the same hash. Step 5: This could be used to smuggle malicious code into trusted Git repositories. Step 6: Git later introduced SHA-256 support, but older repos are still SHA-1 dependent. Step 7: Try a local Git repo with both collision files and explore how Git responds. Step 8: Be careful — this is a known, proven vulnerability that changes how we trust hashes in version control.
- **Detection**: Check for duplicate SHA-1 objects; flag suspicious object histories
- **Solution**: Upgrade to Git SHA-256; verify commit contents and sign tags with GPG
- **Tags**: Git, SHA-1 Collision, Repo Spoofing

## Signed Executable Tampering via MD5

- **Attack Type**: MD5 Signature Forgery
- **Target**: Windows Executables
- **Vulnerability**: MD5 collision-based tampering
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Malware execution with trusted hash
- **Tools**: HashClash, md5sum, EXE tools, PE-bear
- **Scenario**: MD5 collisions allow creation of malicious executables that share the same hash as clean ones, bypassing signature-based defenses.
- **Attack Steps**: Step 1: Understand that many legacy AV or software systems used MD5 for file integrity or signing. Step 2: Using tools like HashClash or FastColl, create two Windows executables (EXEs) — one clean and one malicious — that have identical MD5 hashes. Step 3: Start with a benign executable and clone its structure. Insert a collision block that modifies internal behavior without affecting the hash. Step 4: Confirm using md5sum file1.exe file2.exe — they must match exactly. Step 5: You can now submit the clean one to be signed or whitelisted, and then later replace it with the malicious one. Step 6: Many older AV systems will treat both files the same due to hash match. Step 7: You can test this in a VM — run the clean EXE and see expected behavior, then run the malicious one with identical MD5. Step 8: Always test this inside a sandbox or malware lab. This technique mimics real-world malware signing abuses.
- **Detection**: Monitor for matching hashes with differing behavior; flag MD5-based signatures
- **Solution**: Ban MD5 in signature workflows; use Authenticode and SHA-256 signing
- **Tags**: Signed Malware, Executable Forgery, MD5 Collision

## SSL Certificate Spoofing (MD5)

- **Attack Type**: CA Certificate Chain Forgery via Collision
- **Target**: SSL/TLS Certificate Chains
- **Vulnerability**: CA signing with vulnerable MD5 hashes
- **MITRE**: T1584 – Compromise Infrastructure
- **Impact**: Impersonation of any HTTPS website
- **Tools**: OpenSSL, HashClash, X.509 Tools
- **Scenario**: Attackers generated a fake CA certificate using MD5 collisions, allowing them to impersonate any HTTPS site.
- **Attack Steps**: Step 1: Understand that Certificate Authorities (CAs) used to sign SSL certs using MD5. Step 2: Using a technique demonstrated by researchers in 2008, create two certificate requests — one for a legitimate domain (e.g., www.bank.com) and another for a malicious CA cert with altered fields. Step 3: Insert a collision block that causes both certs to hash to the same MD5 value. Step 4: Submit the benign cert for signing by a real CA that still uses MD5. Step 5: Once the legit cert is signed, the malicious cert (with same hash) becomes valid too. Step 6: You can now use the spoofed CA cert to issue fraudulent HTTPS certs for any domain. Step 7: This technique allowed full HTTPS MITM attacks. Step 8: You can recreate a simplified version using test CAs in a lab setup with OpenSSL. Step 9: This attack ended widespread MD5 use in CAs. Step 10: NEVER try this on production sites — use it in labs only.
- **Detection**: Scan for MD5-based cert chains; use CRL/OCSP to flag fake certs
- **Solution**: All certs must use SHA-256+ for digital signing; revoke MD5-signed root and intermediate certs
- **Tags**: HTTPS Spoofing, CA Forgery, MD5 TLS Attack

## Document Forgery (e.g., PDFs)

- **Attack Type**: PDF Collisions for Content Manipulation
- **Target**: Signed PDFs, Documents
- **Vulnerability**: Collision in document hash verification
- **MITRE**: T1600 – Cryptanalysis
- **Impact**: Signed document forgery, legal tampering
- **Tools**: PDFToolkit, HashClash, qpdf, Python
- **Scenario**: Two PDF files crafted to have the same hash but different visible contents can be used to sign and later swap sensitive documents.
- **Attack Steps**: Step 1: Prepare two versions of a PDF file — one benign (e.g., "Payment Approved") and one altered (e.g., "Payment Rejected"). Step 2: Use HashClash or similar to insert collision blocks into both versions so they share the same hash (e.g., MD5). Step 3: Use qpdf or PDFToolkit to repackage the files without changing their structure. Step 4: Confirm both files return the same hash with md5sum. Step 5: Submit the benign version for signing by an authority or auditor. Step 6: After signing, replace the file with the malicious one. Signature validation checks only the hash, so the forgery passes. Step 7: Try this in a test signing setup with self-signed certificates or Adobe Acrobat validation. Step 8: This can also be used to fool file integrity systems or DMS software. Step 9: Always validate PDF signatures with content-aware tools. Step 10: Hash-based signing alone is not secure against crafted collisions.
- **Detection**: Use visual document inspection + full hash chain validation
- **Solution**: Embed content hashes inside signature metadata; avoid pure hash-based document signing
- **Tags**: PDF Collision, Signed Document Forgery, Hash Bypass

## Software Update Abuse

- **Attack Type**: Hash Collision for Malicious Update Injection
- **Target**: Auto-Updaters, Software Installers
- **Vulnerability**: MD5/SHA-1 based update verification
- **MITRE**: T1600 – Cryptographic Attack
- **Impact**: Remote code execution, malware installation
- **Tools**: HashClash, sha1sum, Python Scripting
- **Scenario**: A malicious software update is crafted to produce the same hash as a legitimate update. The updater trusts the hash and installs malware.
- **Attack Steps**: Step 1: Understand that some software updaters use static hashes (e.g., MD5 or SHA-1) to verify downloaded update packages. Step 2: Download a legitimate software update package and analyze its structure. Step 3: Use HashClash or a similar tool to craft a malicious version of the update with a hash collision. Step 4: Insert a collision block so the malicious update has the same MD5/SHA-1 hash as the clean one. Step 5: Host the malicious file or intercept the updater's connection using tools like mitmproxy, or redirect DNS to your server. Step 6: When the software checks the update hash and finds it matches the expected value, it installs the malware-laced version. Step 7: The user may never realize the update was malicious. Step 8: Test this safely in a virtual machine with an open-source software updater. Step 9: Observe how the integrity check fails to detect the forgery due to hash collision. Step 10: Real-world examples include Flame malware which used hash collision to spoof Microsoft updates.
- **Detection**: Use digital signatures, not static hashes; verify update origin certificates
- **Solution**: Require signed update manifests; avoid weak hash algorithms like MD5 or SHA-1
- **Tags**: Update Abuse, Hash Collision, MD5, SHA-1

## Signed Email Manipulation (S/MIME)

- **Attack Type**: S/MIME Email Forgery via Hash Collision
- **Target**: Email Clients (Outlook, Thunderbird)
- **Vulnerability**: S/MIME signing with weak hash (MD5)
- **MITRE**: T1585 – Email Forgery
- **Impact**: Social engineering, fraud, false email trust
- **Tools**: Mutt, OpenSSL, HashClash
- **Scenario**: Create two different email messages with the same hash. Sign one, then swap it for the other to forge a trusted email.
- **Attack Steps**: Step 1: Compose two versions of an email — one harmless and one malicious. Use identical headers and layout except for the content difference. Step 2: Use a collision generator like HashClash to create two S/MIME email bodies that hash to the same MD5 value. Step 3: Sign the harmless version using your or a test certificate with S/MIME tools like OpenSSL or Mutt. Step 4: Swap in the malicious version which shares the same MD5 hash. Step 5: Email clients will validate the signature because the hash matches, even though the content is different. Step 6: This can fool recipients into trusting altered content or fake financial requests. Step 7: Run this test in a secure environment using dummy email infrastructure. Step 8: Validate that both emails show the same signature status despite different contents. Step 9: This is possible only because S/MIME used to rely on MD5. Step 10: S/MIME is still used in corporate settings — always ensure your email system disallows outdated signing methods.
- **Detection**: Validate content length and byte hash; flag MD5-signed messages
- **Solution**: Block MD5 in signing certs; use SHA-2+ and enforce MIME consistency
- **Tags**: Email Forgery, S/MIME, MD5, Signed Message Swap

## Blockchain Forking Attack (Weak Hash)

- **Attack Type**: Hash Collision in Block Header Chain
- **Target**: Blockchain Networks, Altcoins
- **Vulnerability**: Weak or custom hash functions in block headers
- **MITRE**: T1587 – Blockchain Exploit
- **Impact**: Forking, consensus confusion, double-spend risk
- **Tools**: Custom Blockchain Fork Tools, HashCracker
- **Scenario**: Exploiting weak hashes in blockchain protocols can allow attackers to create alternate chains or forks that share the same block hash.
- **Attack Steps**: Step 1: Study how block headers are created in the target blockchain — this includes hash of the previous block, timestamp, Merkle root, nonce. Step 2: Identify if the blockchain still uses weak hashes like SHA-1 or custom insecure functions. Step 3: Using brute force or pre-image attack techniques, generate two blocks with different transaction contents but the same block hash. Step 4: Submit one legitimate block to the network and mine it normally. Step 5: Hold the second (colliding) block and later broadcast it to induce a chain fork or overwrite. Step 6: The network may treat both blocks as valid and begin a forked chain. Step 7: You can potentially double-spend or confuse consensus algorithms. Step 8: This has been theorized in altcoins or academic blockchain designs with poor hash usage. Step 9: Always test this in a private blockchain or testnet setup, never on live chains. Step 10: Proper blockchains like Bitcoin use SHA-256, which resists these attacks.
- **Detection**: Monitor for multiple blocks with identical hashes; hash-chain validation failures
- **Solution**: Enforce collision-resistant hashing (e.g., SHA-256, BLAKE3); include randomness or strong salt in headers
- **Tags**: Blockchain, Weak Hash, Forking, Double Spend

## Password Hash Collisions

- **Attack Type**: Same Hash for Different Passwords
- **Target**: Legacy Web Apps, Firmware Logins
- **Vulnerability**: MD5/SHA-1 password hashing without salt
- **MITRE**: T1110 – Brute Force / Credential Stuffing
- **Impact**: Unauthorized access, user impersonation
- **Tools**: Hashcat, md5sum, Collision Gen Tools
- **Scenario**: Different passwords can hash to the same MD5/SHA-1 output, allowing login bypass if only hashes are verified.
- **Attack Steps**: Step 1: Understand that a password hash is what gets stored in the database — not the password itself. If two passwords have the same hash, they are treated as equivalent. Step 2: Use collision generators to find two distinct passwords (e.g., “p@ssword1” and “badInput”) that produce the same MD5 hash. Step 3: In older systems using MD5, test this by registering one password and then logging in with the colliding one. Step 4: If the hash function is weak or unsalted, the system may allow login. Step 5: Alternatively, attackers may replace the hash in the database with a known-colliding hash. Step 6: This only works if the application blindly compares hashes without salt or slow key derivation functions like bcrypt or Argon2. Step 7: Test in a local app or lab server with plain MD5 password storage. Step 8: Login as another user using a crafted password that hits the same hash. Step 9: Older firmware and legacy devices often store passwords this way. Step 10: Modern apps should never use MD5/SHA-1 without salt + stretching.
- **Detection**: Look for duplicate hashes in DB; flag identical hashes across users
- **Solution**: Use salted, stretched password hashing (e.g., bcrypt, Argon2); retire MD5/SHA-1 completely
- **Tags**: Password Collision, Weak Hash, Login Bypass

## Herding Attack

- **Attack Type**: Chosen-Prefix Hash Collision
- **Target**: Timestamping Services, Digital Commitments
- **Vulnerability**: Preimage + collision attacks in hash chaining
- **MITRE**: T1600 – Cryptographic Attack
- **Impact**: Document forgery, timestamp fraud, fake commitments
- **Tools**: HashClash, Python, Hash Mapping Tools
- **Scenario**: Attacker creates many hash collision paths and later generates a message prefix that leads to the pre-committed hash output, enabling document forgery or fake evidence.
- **Attack Steps**: Step 1: Understand that a herding attack lets an attacker pre-commit to a hash value and later find a prefix that leads to it. This is useful in scenarios like digital time-stamping or committing to a contract before revealing full details. Step 2: Use a hash collision tool like HashClash to generate many different intermediate message blocks that all hash to a common value (the final commitment hash). Step 3: Store these intermediate blocks in a structure called a "diamond structure" — it allows you to later choose a path through them. Step 4: Publish the final hash publicly (e.g., as part of a document or timestamp service). Step 5: Later, after seeing the context or competitor’s decision, craft a custom prefix that links into your diamond structure, resulting in the same final hash. Step 6: The result is that it appears you had committed to the final document earlier, when in fact you chose it later. Step 7: Test this by generating a collision tree and crafting fake contract variants leading to the same commitment hash. Step 8: Herding is possible on MD5 and theoretical on SHA-1. Step 9: This attack breaks immutability guarantees where weak hashes are used. Step 10: Defenses include using strong hash functions (SHA-2, SHA-3) and digital signatures.
- **Detection**: Monitor for commitment hash reuse; flag unrealistic message-to-hash linking
- **Solution**: Use digital signatures and secure hash algorithms (SHA-256+); validate full message history
- **Tags**: Herding, MD5, Commitment Fraud, Hash Chaining

## Zerologon-style Hash Collision Exploit

- **Attack Type**: Null Input Leading to Hash Collisions
- **Target**: Windows Active Directory, Netlogon
- **Vulnerability**: Poor cryptographic implementation in auth protocols
- **MITRE**: T1212 – Exploitation for Privilege Escalation
- **Impact**: Full domain takeover, credential reset
- **Tools**: Python, Impacket (zerologon_tester.py), Wireshark
- **Scenario**: Attackers exploit protocols using weak hashing on zero or null values, causing collisions that break authentication and gain system access (e.g., Netlogon Zerologon flaw).
- **Attack Steps**: Step 1: Understand that the Zerologon vulnerability exploited a flaw in how Microsoft's Netlogon protocol computed session keys using AES-CFB8 with all-zero IV and plaintext. Step 2: The client credential is generated via hash-like computation — but with zeroed inputs, this produces predictable or identical values. Step 3: Attacker floods the Netlogon authentication mechanism with repeated zeroed authentication attempts. Step 4: Due to implementation flaw, some attempts bypass authentication and set the machine account password to blank. Step 5: Use the zerologon_tester.py script from Impacket to test if a domain controller is vulnerable. Step 6: If vulnerable, use the exploit to reset the domain controller’s machine account password to null. Step 7: This grants full control over the domain. Step 8: Safely test this on a virtualized AD lab environment to observe success conditions. Step 9: Microsoft patched this in 2020 (CVE-2020-1472), but unpatched DCs still exist in legacy setups. Step 10: Always test this only on non-production test systems.
- **Detection**: Monitor Netlogon RPC traffic; check for repeated null authentication attempts
- **Solution**: Patch systems with CVE-2020-1472 fix; disable vulnerable Netlogon behavior
- **Tags**: Zerologon, Hash Collision, AD Exploit, Null Auth

## Hash-Comparison Bypass (Type Confusion)

- **Attack Type**: Type Confusion Bypass in Hash Checks
- **Target**: Web Logins, CMS Platforms (PHP)
- **Vulnerability**: Weak comparison logic with type coercion
- **MITRE**: T1589 – Credential Access
- **Impact**: Auth bypass, account takeover
- **Tools**: PHP CLI, Burp Suite, Custom Scripts
- **Scenario**: Exploits weak language-level type coercion or timing to bypass hash comparison checks (e.g., PHP’s == treating 0e... as scientific notation).
- **Attack Steps**: Step 1: Understand that some hash outputs (e.g., MD5(“QNKCDZO”) = “0e830400451993494058024219903391”) resemble scientific notation and are interpreted as zero (0e...) by weak languages like PHP. Step 2: Find two inputs that hash to values like 0e123456..., which are treated as zero when loosely compared with ==. Step 3: In PHP, submit a login form or hash verification request with one of these inputs. Step 4: If the backend uses == instead of ===, the comparison returns true because both hash values are treated as 0e+something (scientific notation = 0). Step 5: Try this in a PHP test app using if (md5($input) == $stored_hash) and submit a magic hash input. Step 6: If it succeeds, you bypass authentication. Step 7: Several known strings produce “magic hashes” that begin with 0e... and work in this way. Step 8: Use Burp Suite to automate form submission with candidate values. Step 9: This attack doesn’t break the hash itself, but exploits poor comparison logic. Step 10: Always use strict comparison (===) to prevent this issue.
- **Detection**: Check for == usage in hash validation code; audit for loose comparisons
- **Solution**: Use strict comparison (=== in PHP/JS); avoid MD5 as login verifier
- **Tags**: Magic Hash, Type Confusion, PHP, Auth Bypass

## Hash Table Collision Denial-of-Service

- **Attack Type**: Hash-Flooding DoS Attack
- **Target**: Web APIs, Application Servers
- **Vulnerability**: Predictable hash function without DoS mitigation
- **MITRE**: T1499 – Endpoint DoS
- **Impact**: Resource exhaustion, unresponsive app/API
- **Tools**: Burp Suite, Python, HashPump
- **Scenario**: Attackers send many inputs that hash to the same value, creating collisions in backend hash tables, degrading performance or crashing systems.
- **Attack Steps**: Step 1: Understand that many languages (e.g., Java, PHP, Python) use hash tables (dictionaries, maps) that rely on unique hashes for fast lookup. Step 2: If many items share the same hash, performance drops from O(1) to O(n). This is hash-flooding. Step 3: Use known colliding inputs (e.g., long string patterns) that produce same hash in the target system. Tools like Burp Intruder or custom Python scripts can generate such inputs. Step 4: Target a form field or API endpoint that stores or validates user input (e.g., username map, session token list). Step 5: Send 10,000+ crafted inputs that collide in hash table. Step 6: Server becomes slow, unresponsive, or crashes. Step 7: To test, use a Flask or PHP test app, insert 1,000+ colliding keys into a dict/map, and measure response time. Step 8: This technique was shown in 2011 against PHP, Java, ASP.NET. Step 9: This is a DoS attack — it doesn’t steal data but affects availability. Step 10: Mitigation includes using hash randomization (e.g., SipHash), request rate limiting, and input length controls.
- **Detection**: Monitor sudden spike in request parsing time or hash lookup delay
- **Solution**: Use hash randomization (e.g., SipHash); limit user-submitted key values and length
- **Tags**: Hash DoS, Flooding, Collision, Denial-of-Service

## Combining Collision & Timing Side-Channels

- **Attack Type**: Side-Channel + Hash Collision Hybrid Attack
- **Target**: Web Auth Systems, APIs, IoT Devices
- **Vulnerability**: Byte-by-byte hash compare with time leakage
- **MITRE**: T1595 – Active Scanning
- **Impact**: Auth bypass, timing leak, forged token
- **Tools**: Python, Burp Suite Repeater, Wireshark
- **Scenario**: Attackers exploit subtle time delays in hash comparison functions to guess input and confirm hash collisions, enabling login bypass or MAC forgery.
- **Attack Steps**: Step 1: Learn that some systems compare hashes or MACs byte-by-byte. When using insecure comparison like memcmp, comparison may exit early if bytes don't match. Step 2: This creates a time difference — more matching bytes cause longer checks. Step 3: Attacker sends multiple guesses for a MAC or password hash, changing one byte at a time. Step 4: Measures how long each response takes. Step 5: The request that takes slightly longer indicates correct byte guess. Step 6: Repeat this process to leak entire hash or MAC character-by-character. Step 7: Now attacker uses this information to construct or identify a hash collision or forge authentication tokens. Step 8: Tools like Burp Repeater or custom Python with timing logic can automate this. Step 9: This hybrid attack bypasses login/auth systems or verifies partial collisions. Step 10: Prevent by using constant-time comparison (e.g., hmac.compare_digest() in Python).
- **Detection**: Analyze login or MAC verification timing per byte; check for linear timing increase
- **Solution**: Use constant-time comparison functions; pad and normalize all input before hashing
- **Tags**: Timing Side-Channel, MAC Leak, Hash Comparison

## Collision via Hash Chaining Manipulation

- **Attack Type**: Hash Chain Integrity Bypass
- **Target**: Blockchain, Logs, Digital Ledger
- **Vulnerability**: MD5/SHA-1 collisions in hash-chained systems
- **MITRE**: T1600 – Cryptographic Attack
- **Impact**: Log manipulation, tampering, forged records
- **Tools**: Python, HashClash, Custom Scripts
- **Scenario**: In systems using chained hashes (like blockchain logs), attackers exploit collisions to inject or alter messages without breaking the final hash.
- **Attack Steps**: Step 1: Understand how hash chains work: each block’s hash includes previous block’s hash, forming an integrity chain. If one block is altered, the chain breaks. Step 2: Attackers aim to generate a collision for a specific hash output of a block, then replace or append malicious data with matching hash. Step 3: Use a tool like HashClash to find two different messages that produce the same hash (collision). Step 4: Insert the fake message into the hash chain and recalculate the rest of the chain if feasible. Step 5: If system doesn't verify content internally (only hashes), the malicious message is accepted as valid. Step 6: Example: in a log system where each entry hashes the previous, you can forge fake logs with colliding blocks. Step 7: This attack is mainly theoretical for modern hashes, but practical on MD5 and SHA-1. Step 8: Use a logging system that doesn't allow reordering or appending without full-chain revalidation. Step 9: Blockchain forks and digital records are vulnerable to this if legacy hashing is used. Step 10: Use SHA-256+ and digital signatures for each block to ensure full message integrity.
- **Detection**: Verify block content, not just hashes; check chain consistency at all stages
- **Solution**: Use collision-resistant hash functions; add digital signatures per block
- **Tags**: Blockchain Log Bypass, Hash Chain Tampering

## Collision Attack in Digital Voting Systems

- **Attack Type**: Hash-Based Ballot Tampering
- **Target**: Digital Voting, Blockchain Voting
- **Vulnerability**: Weak hash used to verify votes
- **MITRE**: T1585 – Data Manipulation
- **Impact**: Voter fraud, ballot tampering, trust collapse
- **Tools**: HashClash, OpenVote, Ballot Auditing Tools
- **Scenario**: Attackers generate two vote messages with same hash. Submit benign one, later reveal malicious one with same hash to change vote retrospectively.
- **Attack Steps**: Step 1: In some electronic voting systems, a vote is hashed and sent for verification/storage. Attacker crafts two ballot messages that hash to the same value using MD5 or SHA-1 (collision). Step 2: One ballot is benign (e.g., vote for Candidate A), the other is malicious (e.g., Candidate B). Step 3: Attacker submits benign one to system. Step 4: Later, they present the malicious one, and due to hash collision, system treats it as same valid ballot. Step 5: In end-to-end verifiable systems where voter checks hash receipt, the two messages are indistinguishable. Step 6: Use HashClash or FastColl to generate two colliding ballot messages. Step 7: This attack undermines trust and integrity of vote, especially when only hashes are verified. Step 8: Recreate a test system using OpenVote-like hash-based verification to experiment. Step 9: This is preventable by using SHA-256+ and binding hash to voter identity or timestamp. Step 10: Enforce non-malleable signatures and append-only logs to prevent ballot replacement.
- **Detection**: Audit duplicate hashes; require voter ID binding; track submission history
- **Solution**: Use collision-resistant hashing and signatures; bind vote hash to voter and time
- **Tags**: Vote Tampering, Hash Collision, Digital Election Fraud

## Certificate Pinning Bypass via Collision

- **Attack Type**: TLS Certificate Trust Exploit
- **Target**: Mobile Apps, Browsers, APIs
- **Vulnerability**: Hash-based certificate trust bypass
- **MITRE**: T1587.006 – Trusted Relationship Abuse
- **Impact**: HTTPS MITM, certificate forgery, data theft
- **Tools**: HashClash, OpenSSL, Burp Suite, Frida
- **Scenario**: Attackers generate a forged certificate with the same hash as a pinned cert, bypassing client-side trust checks in apps or browsers that rely on hash pinning.
- **Attack Steps**: Step 1: Understand how certificate pinning works: the app stores a hash (often SHA-1/SHA-256) of the server’s SSL certificate. During a connection, it compares the server’s certificate hash to the stored hash. If it matches, the connection is allowed. Step 2: Attacker creates a fake certificate (self-signed or forged via compromised CA) with slightly modified fields. Step 3: Use a collision tool like HashClash to adjust fields in the certificate (e.g., subjectAltName, padding) until the fake certificate produces the same SHA-1 hash as the pinned real one. Step 4: Set up a proxy server (Burp or mitmproxy) and serve the fake cert. Step 5: When the app or browser connects, it checks the hash, sees it matches, and allows the connection — attacker now acts as a MITM. Step 6: For mobile apps using pinning, tools like Frida can help bypass dynamic pinning checks or allow cert injection for testing. Step 7: Test this in controlled environment (e.g., Android app with known pinned cert). Step 8: If SHA-1 is used (still found in old systems), this attack is feasible in practice. Step 9: Replace weak hash pinning with full cert public key validation or CA pinning. Step 10: Never rely solely on hash of cert — hashes can collide.
- **Detection**: Monitor for unexpected certs; analyze TLS traffic; look for mismatched cert chains
- **Solution**: Use public key or SPKI pinning; never use SHA-1 for cert validation; implement cert transparency
- **Tags**: Certificate Forgery, Hash Collision, TLS Bypass

## Malware Obfuscation with Hash Collisions

- **Attack Type**: Evasion via Hash Matching
- **Target**: Antivirus Engines, Endpoint Detection
- **Vulnerability**: Weak hash in allowlist/detection systems
- **MITRE**: T1036 – Masquerading
- **Impact**: Malware bypassing AV, persistent infection
- **Tools**: HashClash, PEfile, Antivirus Emulators
- **Scenario**: Malware authors craft files with same hash as benign files to fool antivirus hash detection systems or whitelist enforcement.
- **Attack Steps**: Step 1: Understand that many security products use hashes (e.g., MD5, SHA-1) to detect known malware. If a file has the same hash as a known safe file, it may bypass detection. Step 2: Malware author takes a benign executable (e.g., a known clean Windows utility) and copies its header or basic structure. Step 3: Using tools like HashClash, attacker tweaks the malicious binary content (e.g., adds encrypted payload, uses data padding) to produce a collision — i.e., same hash output as clean file. Step 4: Verify that both the benign and malicious files now produce the same hash using sha1sum or md5sum. Step 5: Malware is deployed to a target system or cloud platform where hashes are used for allowlisting (e.g., by admins or antivirus). Step 6: Because hash matches the known clean file, the system allows the malicious file to execute or skip scanning. Step 7: In advanced cases, malware also evades digital signature checks by injecting code into non-signed areas or using hash-aligned segments. Step 8: Test in isolated lab with AV emulators or Windows AppLocker using hash rules. Step 9: Defenders should use multiple detection methods (heuristics, behavior analysis) instead of only hashes. Step 10: Replace MD5/SHA-1 based whitelisting with SHA-256+ and code signing enforcement.
- **Detection**: Monitor for multiple binaries sharing same hash; verify full file integrity with digital signatures
- **Solution**: Use SHA-256 or better; verify code signatures; use behavior-based detection engines
- **Tags**: Malware Evasion, Hash Collision, AV Bypass

## Classical Preimage Attack

- **Attack Type**: Preimage Cryptanalysis
- **Target**: Weak Hash Functions
- **Vulnerability**: Short output space, poor resistance to brute force
- **MITRE**: T1110.003 – Hash Cracking
- **Impact**: Loss of integrity, forgery of messages
- **Tools**: Hashcat, Python, Custom Scripts
- **Scenario**: Attackers attempt to find any message that hashes to a specific target hash value, breaking the one-way nature of the hash function.
- **Attack Steps**: Step 1: Understand what a preimage attack is: the goal is to find any input that, when hashed, results in a specific given hash output (e.g., e3b0c442...). Step 2: Choose a target hash function that is weak (e.g., MD4, CRC32, or truncated SHA-1). Strong hashes like SHA-256 are currently impractical to attack. Step 3: Use brute-force by generating many inputs and hashing them one by one using a script or a hash cracking tool like Hashcat. Step 4: Compare each output hash to the target hash. If one matches, you’ve found a preimage. Step 5: For demonstration, try attacking CRC32 (32-bit hash) which is easily brute-forced using a few billion attempts — doable on modern laptops. Step 6: To speed up, you can use GPUs or parallel threads with Hashcat. Step 7: Log the found preimage and verify that it reproduces the exact same hash. Step 8: Note that this attack is not finding the original message — just a message that matches the hash. Step 9: This attack highlights why short hashes are insecure against brute-force or lookup table attacks.
- **Detection**: Monitor for repetitive hash attempts; detect hashing at scale
- **Solution**: Use long hashes (≥256 bits); switch to SHA-256 or SHA-3
- **Tags**: Preimage, Brute Force, Hash Reversal

## Second Preimage Attack

- **Attack Type**: Preimage Cryptanalysis
- **Target**: Weak Hash Functions
- **Vulnerability**: Weak second preimage resistance in legacy hashes
- **MITRE**: T1110.003 – Hash Cracking
- **Impact**: Integrity violation, digital signature spoofing
- **Tools**: Hashcat, Python hashlib, Collision Search Tools
- **Scenario**: Given a known input and its hash, attacker attempts to find a different input that produces the exact same hash — a second preimage.
- **Attack Steps**: Step 1: Understand the difference: unlike basic preimage attack, here you're given an input and its hash, and must find another input (not equal) with the same hash. Step 2: Choose a vulnerable hash like MD4, MD5, or truncated SHA-1 where second preimage resistance is weak due to design flaws. Step 3: Take a known input — for example, a file or message string like original = "HelloWorld". Step 4: Hash it using a weak function like MD4 to get a target hash. Step 5: Write a script or use tools to generate and test alternate messages to check if any produce the same hash. Step 6: Because the second preimage attack avoids matching the same input, the tool must avoid repeating the original input. Step 7: This may require billions or trillions of attempts for longer hashes, but for short or older hashes, it can be feasible. Step 8: Verify when another distinct input yields the same hash — that’s your second preimage. Step 9: These are particularly dangerous in digital signatures and blockchain integrity schemes using weak hash functions.
- **Detection**: Hash consistency checks; monitor excessive hash generation attempts
- **Solution**: Deprecate MD5/MD4/weak hashes; enforce SHA-2 or SHA-3
- **Tags**: Preimage, Collision, Digital Signature Forgery

## Preimage Attack on Short Hashes (e.g., CRC, SHA-1)

- **Attack Type**: Brute-Force Preimage Attack
- **Target**: Short Hash Implementations
- **Vulnerability**: Limited entropy in hash output space
- **MITRE**: T1110 – Brute Force
- **Impact**: Hash forgery, message tampering
- **Tools**: Hashcat, Python, Hash Verification Scripts
- **Scenario**: Short hash functions like CRC32 or truncated SHA-1 are vulnerable to brute-force preimage recovery due to their limited hash output size.
- **Attack Steps**: Step 1: Understand that short hashes like CRC32 (32-bit) can only represent ~4 billion unique values, making brute-force attacks practical. Step 2: Choose a known hash output (e.g., abcd1234 CRC value) and attempt to recover a valid input that produces it. Step 3: Use a brute-force script that repeatedly generates strings, computes their CRC32 or SHA-1-80 hash, and compares it to the target. Step 4: On modern systems, CRC32 values can be brute-forced in a matter of seconds to minutes. Step 5: For SHA-1 truncated to 64–80 bits, preimage recovery takes longer but is still feasible with distributed computing or GPUs. Step 6: Optionally, build a rainbow table (precomputed hash-input pairs) for quick reverse lookups. Step 7: Once you find a match, verify the input generates the same hash. Step 8: Demonstrates why short/truncated hashes are not safe for cryptographic applications. Step 9: Many legacy systems (e.g., embedded or IoT firmware) still use CRC/short hashes and are vulnerable to tampering via this method.
- **Detection**: Static analysis of firmware; detect known weak hash usage
- **Solution**: Replace CRC with SHA-256 or Blake3; use cryptographic hashes for any security-sensitive operation
- **Tags**: CRC, SHA-1, Brute Force, Legacy Systems

## MD4 Preimage Attack

- **Attack Type**: Targeted Preimage Attack
- **Target**: NTLM Hashes, Legacy Systems
- **Vulnerability**: Outdated hash function (broken structure)
- **MITRE**: T1606.002 – Malicious File
- **Impact**: Password cracking, hash reversal, file spoofing
- **Tools**: HashClash, Custom MD4 Tools, Python
- **Scenario**: MD4 is an obsolete hash function with critical vulnerabilities that allow preimages to be found with far less than brute-force effort.
- **Attack Steps**: Step 1: Understand MD4 was designed in 1990 and is extremely fast but cryptographically broken. It produces 128-bit hashes but has known weaknesses that reduce attack complexity. Step 2: Choose a target MD4 hash value — e.g., one you want to reverse to a message. Step 3: Use the HashClash framework or a custom Python script implementing known differential attacks against MD4 to find messages that hash to this target. Step 4: These attacks do not require checking all 2^128 values — many shortcuts exist that reduce search space to around 2^64 or lower. Step 5: Alternatively, use meet-in-the-middle or differential cryptanalysis to exploit MD4’s internal structure (e.g., chaining values or block operations). Step 6: Once a matching input is found, confirm its MD4 hash matches the target. Step 7: Demonstrates the dangers of using outdated algorithms — MD4 is still sometimes found in NTLM hashes or legacy applications. Step 8: Never use MD4 for any form of authentication or integrity checks. Step 9: Replace it immediately with SHA-2, SHA-3, or modern alternatives.
- **Detection**: Monitor for MD4 usage in authentication; alert on NTLMv1 or legacy hash activity
- **Solution**: Replace MD4/NTLM with bcrypt, SHA-512, or Argon2
- **Tags**: MD4, Preimage, NTLM Hash, Legacy Systems

## MD5 Preimage Attack (Partial)

- **Attack Type**: Preimage Cryptanalysis
- **Target**: MD5-based Authentication or Hashing Systems
- **Vulnerability**: Weak internal structure in MD5
- **MITRE**: T1110.003 – Hash Cracking
- **Impact**: Digital signature forgery (future risk), legacy protocol compromise
- **Tools**: HashClash, Custom C/Assembly scripts
- **Scenario**: Cryptanalysts have demonstrated partial preimage attacks on MD5 by targeting reduced rounds or exploiting internal weaknesses, though full preimages remain infeasible.
- **Attack Steps**: Step 1: Understand that MD5 produces a 128-bit hash. Full preimage attacks (finding any input matching a hash) are computationally infeasible today. However, partial preimage attacks work on "reduced rounds" (e.g., 45 out of 64 steps in MD5). Step 2: Use academic tools like HashClash or scripts replicating published cryptanalysis papers. Step 3: Choose a known hash (from reduced-round MD5), and configure the tool to target that version of the algorithm. Step 4: Run differential or meet-in-the-middle strategies to find inputs that match specific hash prefixes or internal values. Step 5: While this won’t match the full hash in real-world MD5, it proves that MD5’s structure is weak. Step 6: This attack is mainly theoretical and used in research, but it shows why MD5 should not be used in any secure system. Step 7: Demonstrates progress toward eventually practical full preimage attacks.
- **Detection**: Monitor for MD5 usage in digital signing or auth systems
- **Solution**: Replace MD5 with SHA-2 or SHA-3; enforce digital signature algorithms to avoid MD5 usage
- **Tags**: MD5, Preimage, Weak Hash, Cryptanalysis

## SHA-1 Preimage Attack (Theoretical)

- **Attack Type**: Theoretical Preimage Cryptanalysis
- **Target**: SHA-1-based Signing or Validation Systems
- **Vulnerability**: Partial-round vulnerability in SHA-1 design
- **MITRE**: T1110.003 – Hash Cracking
- **Impact**: Future risk to integrity, digital certificates
- **Tools**: Custom Python Scripts, C Implementations
- **Scenario**: Research has demonstrated preimage attacks on reduced-round SHA-1 (e.g., 63 of 80 rounds), indicating feasibility of breaking SHA-1 in future with better hardware.
- **Attack Steps**: Step 1: Understand that SHA-1 has 80 rounds; full SHA-1 preimages are still not feasible, but attacks on reduced-round SHA-1 have lowered the bar. Step 2: Implement attacks from cryptanalysis papers (e.g., by Stevens et al.) using C or Python-based hash simulators. Step 3: Configure the script to simulate SHA-1 with, for example, only 63 rounds. Step 4: Choose a hash output from this reduced-round SHA-1 and begin searching for a preimage using known weaknesses in message expansion and differential paths. Step 5: If successful, the tool returns an input that produces the same hash — proving that under reduced strength, SHA-1 can be broken. Step 6: Although this isn’t practical for full SHA-1 yet, the work shows SHA-1 is no longer secure and shouldn't be used. Step 7: This technique is research-focused but informs industry deprecation of SHA-1 (e.g., browsers no longer accept SHA-1 certificates).
- **Detection**: Warn on use of SHA-1 in signatures; log deprecated API usage
- **Solution**: Deprecate SHA-1 fully; enforce SHA-256+ in PKI and file signing
- **Tags**: SHA-1, Cryptanalysis, Preimage, Research Attack

## Preimage with Rainbow Tables

- **Attack Type**: Precomputed Hash Inversion
- **Target**: Password Hashes, File Integrity Checks
- **Vulnerability**: Lack of salt, use of weak hash functions
- **MITRE**: T1110.003 – Hash Cracking
- **Impact**: Password theft, reverse engineering of hashes
- **Tools**: RainbowCrack, ophCrack, Cain & Abel
- **Scenario**: Rainbow tables allow attackers to reverse hashes without brute-forcing, using large precomputed databases to find original input matching known hashes.
- **Attack Steps**: Step 1: Understand that a rainbow table is a large database of precomputed hash-input pairs, usually generated using weak hash functions like MD5 or NTLM. Step 2: Download or generate a rainbow table for your hash function (e.g., MD5). Step 3: Obtain a target hash value (e.g., from a stolen password database or captured session). Step 4: Use a tool like RainbowCrack to search the table for a matching hash. Step 5: If found, the table returns the original input that was used to create that hash — essentially reversing it without brute-force. Step 6: This works best for common inputs like dictionary words, usernames, or default passwords. Step 7: This technique is often used in cracking Windows NTLM hashes or leaked MD5 password dumps. Step 8: For large tables, ensure enough storage (tables can be 100GB+). Step 9: If hash is salted, this method fails unless rainbow tables are built for that exact salt — making salting a key defense.
- **Detection**: Detect table-based lookups via timing anomalies; monitor for hash database access
- **Solution**: Use salted hashes with bcrypt/scrypt/Argon2; prevent reuse of unsalted MD5/NTLM hashes
- **Tags**: Rainbow Tables, Hash Reversal, Password Cracking

## Lookup Table Preimage Attack

- **Attack Type**: Static Hash Reversal via Lookup Table
- **Target**: Hash-Based Authentication Systems
- **Vulnerability**: Unsalted, predictable input hashes
- **MITRE**: T1555.003 – Credentials from Password Stores
- **Impact**: Credential recovery, login spoofing
- **Tools**: Python Dictionary, SQL DB, Hashcat
- **Scenario**: Similar to rainbow tables, lookup tables are simpler precomputed hash-input pairs stored in a dictionary or database for fast hash cracking.
- **Attack Steps**: Step 1: Lookup tables are simple hash maps: you hash a huge number of possible inputs (e.g., passwords, file names) and store their hash values in a dictionary or database. Step 2: Prepare your lookup table by generating and storing hashes (e.g., using Python: hashlib.md5(p.encode()).hexdigest() for each word in a dictionary). Step 3: When you get a target hash, search the table for a match. Step 4: If the hash is in the table, return the original input — this gives you the preimage. Step 5: Lookup tables can be customized by the attacker to target a specific system (e.g., default device credentials). Step 6: Lookup tables are smaller and faster to query than rainbow tables but don’t use reduction functions, so storage is larger per match. Step 7: This method is often used in CTFs, malware analysis, or reverse engineering tasks. Step 8: Limitation: works only on unsalted hashes, as salted hashes change for every user. Step 9: Regularly rotating passwords and hashing algorithms defeats lookup-based attacks.
- **Detection**: Detect use of shared/unsalted passwords; check for bulk hash queries
- **Solution**: Use salted hashes and stretchers like bcrypt/PBKDF2; regularly rotate secrets
- **Tags**: Lookup Table, Hash Crack, Password Recovery

## Online Preimage Search on Hash Leaks

- **Attack Type**: Online Hash Lookup (Public Database)
- **Target**: Password databases, leaked hash sets
- **Vulnerability**: Use of unsalted or common hashes
- **MITRE**: T1555 – Credentials from Password Stores
- **Impact**: Account compromise, lateral movement
- **Tools**: CrackStation, Hashes.org, OnlineHashCrack
- **Scenario**: Attackers use leaked hashes (e.g., from database breaches) and match them against public hash databases (like CrackStation) to find the original input.
- **Attack Steps**: Step 1: Attacker obtains a list of hashed passwords or credentials, usually from a data breach (e.g., hash: 5f4dcc3b5aa765d61d8327deb882cf99). Step 2: They go to public hash databases like CrackStation.net, which contain millions of common hash–input pairs. Step 3: The attacker pastes the hash into the lookup field and searches. Step 4: If the hash corresponds to a known weak password (like “password” or “123456”), the site returns the original string. Step 5: They can now use this recovered password to log into accounts or escalate access. Step 6: If multiple accounts use the same weak password, the attacker can reuse it. Step 7: This is fast, free, and very common in real-world breaches. No hacking tools needed — just access to a browser.
- **Detection**: Monitor login attempts after public breaches; detect mass credential reuse
- **Solution**: Always salt and hash passwords; disallow common passwords; enable 2FA wherever possible
- **Tags**: Online hash cracking, breach analysis, credential reuse

## Salting Bypass for Preimage Attack

- **Attack Type**: Weak Salt Handling Exploitation
- **Target**: Poorly implemented password storage
- **Vulnerability**: Predictable or reused salt
- **MITRE**: T1110.003 – Hash Cracking
- **Impact**: Password recovery, authentication bypass
- **Tools**: Python, Hashcat, RockYou.txt
- **Scenario**: Attackers bypass salt-based protections when salts are predictable, reused, or leaked alongside hashes.
- **Attack Steps**: Step 1: Understand that salting adds a unique value to each password before hashing (e.g., hash(password + salt)), making it harder to crack using rainbow tables. Step 2: However, if the salt is weak (e.g., the username or a fixed string like "123"), or if the system uses the same salt for all users, attackers can bypass this protection. Step 3: Attacker finds the salt (e.g., from a database field like salt_column) or guesses it if it’s trivial. Step 4: Using a tool like Hashcat, they append the known or guessed salt to dictionary words from RockYou.txt and hash each combination. Step 5: They compare each hash against the stolen hash to find a match. Step 6: Once matched, the original password is revealed. Step 7: This shows that using salt is not enough — the salt must be unique and random per user. Step 8: Reused or weak salts make hash cracking feasible.
- **Detection**: Inspect password storage code for salt reuse; check salt randomness
- **Solution**: Generate cryptographically strong random salt per user; store salt securely
- **Tags**: Salting, Hash Reuse, Authentication Attack

## Chosen Hash Preimage Attack

- **Attack Type**: Input Forgery for Chosen Hash
- **Target**: File uploads, APIs, integrity checks
- **Vulnerability**: Weak hash validation (e.g., MD5, SHA-1)
- **MITRE**: T1600 – Forge Data or Protocol
- **Impact**: File tampering, fake updates, code injection
- **Tools**: Hash Extender, Python hash libraries
- **Scenario**: The attacker crafts an input that produces a hash of their choosing, enabling spoofed files, bypassed integrity checks, or unauthorized data uploads.
- **Attack Steps**: Step 1: Attacker wants to submit a file, message, or request that must match a known hash value — but they don’t have the original input (e.g., file checksum validation). Step 2: They choose a target hash they want to match (e.g., 2c1743a391305fbf367df8e4f069f9f9). Step 3: Using tools like hash_extender, they craft a new input with appended data that results in the exact same hash — this uses length extension or other preimage methods depending on the hash algorithm. Step 4: They now submit this forged input (e.g., fake firmware, update file, or API payload), and it passes validation because it matches the original hash. Step 5: This works mostly against insecure hash schemes (like MD5, SHA-1) or naive validation checks. Step 6: If used for file uploads or integrity checks, the system accepts tampered data.
- **Detection**: Detect use of weak hashing algorithms for input validation; log hash mismatches
- **Solution**: Use HMACs or digital signatures instead of raw hashes; never trust user-provided hashes
- **Tags**: Input forgery, checksum spoof, hash matching

## Targeted Preimage for Hash Collisions

- **Attack Type**: Tailored Hash Collision Exploit
- **Target**: File repositories, Document storage systems
- **Vulnerability**: Hash collision acceptance
- **MITRE**: T1600 – Forge Data or Protocol
- **Impact**: Document replacement, code smuggling
- **Tools**: FastColl, HashClash, Custom C scripts
- **Scenario**: The attacker crafts two distinct inputs that produce the same hash (collision) and controls one input to be accepted, the other to trigger malicious behavior.
- **Attack Steps**: Step 1: Understand that in a collision attack, two inputs hash to the same value — but the attacker needs both to be structurally valid and meaningful. Step 2: Attacker creates a benign-looking input (e.g., a PDF, XML, or ZIP file) and a malicious version that collides with it. Step 3: Using HashClash or FastColl, they generate input pairs that produce the same MD5 or SHA-1 hash. Step 4: They upload the benign version to the system, which stores and verifies the hash. Step 5: Later, they replace the file with the malicious one, which has the same hash and is accepted as legitimate. Step 6: This can lead to malicious payload execution, data overwrites, or bypassing approval workflows. Step 7: This method is especially dangerous in digital signatures, file storage, and patching systems that rely only on hashes.
- **Detection**: Monitor for file hash re-use patterns; warn if binary differences exist in same-hash files
- **Solution**: Use SHA-256+ or SHA-3; avoid relying on hashes for security unless signed
- **Tags**: MD5 collision, Document forgery, File hijack

## Preimage Attacks in Blockchain (Nonce Guessing)

- **Attack Type**: Mining & Nonce Guess Prediction
- **Target**: Blockchain miners, testnets, forks
- **Vulnerability**: Predictable or reused nonce values
- **MITRE**: T1496 – Resource Hijacking
- **Impact**: Block forging, double-spend, mining abuse
- **Tools**: Blockchain nodes, Python web3 libs, GPUs
- **Scenario**: Miners or attackers attempt to guess or calculate valid nonces that produce a hash under the target threshold, exploiting deterministic or narrow nonce ranges.
- **Attack Steps**: Step 1: In blockchains like Bitcoin or Ethereum, miners must find a nonce value such that hash(block + nonce) falls below a specific difficulty target. Step 2: Normally this is a brute-force process, but attackers try to reduce effort by guessing likely nonce values based on known patterns, bugs, or misconfigured randomness (e.g., reused block headers, unrandomized timestamps). Step 3: Using GPU miners or custom code, they calculate SHA256(block_data + nonce) repeatedly for millions of nonce values. Step 4: If a valid nonce is found that meets the difficulty target, the attacker can broadcast their forged block and collect rewards or manipulate the chain. Step 5: In some altcoins or testnets, predictable nonce ranges or timestamp tricks make this easier. Step 6: This is called a preimage attack because you’re finding an input (block + nonce) for a target hash. Step 7: Defenses rely on randomness and properly chosen difficulty.
- **Detection**: Monitor miner hash rate anomalies; detect invalid timestamp ranges
- **Solution**: Ensure miner nonce space is wide and random; validate block structure stringently
- **Tags**: Blockchain, mining attack, SHA256 preimage

## File Hash Preimage Attack for Malware Injection

- **Attack Type**: Hash Preimage with File Forgery
- **Target**: Antivirus systems, digital signing tools
- **Vulnerability**: Use of weak hash function for trust
- **MITRE**: T1600 – Forge Data or Protocol
- **Impact**: Malware execution, bypass security filtering
- **Tools**: HashClash, Custom hash collision generators
- **Scenario**: Attacker creates a malicious file with the same hash as a known safe file, bypassing whitelisting or security systems.
- **Attack Steps**: Step 1: Security software uses file hashes to determine if a file is safe (e.g., MD5 hash of clean.exe). Step 2: Attacker downloads the original clean file and calculates its hash (e.g., e99a18c428cb38d5f260853678922e03). Step 3: They now modify a malicious file and use collision tools to force it to have the same hash. Step 4: This usually works on MD5 or SHA-1 which are weak to collision attacks. Step 5: The attacker uploads or distributes the malicious file. Step 6: Since the hash matches a trusted file, it passes the integrity check. Step 7: The malware executes undetected. Step 8: This can be used in software updates, file hosting, email attachments, or code repositories.
- **Detection**: Monitor for multiple files with identical hash but differing binary contents
- **Solution**: Use SHA-256+ for all integrity validation; avoid MD5/SHA1; consider using digital signatures
- **Tags**: Hash forgery, MD5 collision, malware injection

## Firmware Integrity Bypass using Preimage

- **Attack Type**: Firmware Forgery via Preimage
- **Target**: IoT devices, embedded systems, bootloaders
- **Vulnerability**: Firmware validated via weak hash
- **MITRE**: T1542.001 – Pre-OS Boot
- **Impact**: Persistent malware, firmware compromise
- **Tools**: binwalk, firmware modkit, HashClash
- **Scenario**: Attacker crafts malicious firmware that matches the hash of a trusted firmware image to bypass device update protections.
- **Attack Steps**: Step 1: Many embedded devices only accept firmware that matches a known hash (e.g., SHA1(firmware.bin) == trusted_hash). Step 2: Attacker extracts the original firmware using tools like binwalk. Step 3: They inject malicious code into the firmware (e.g., a hidden backdoor or altered config). Step 4: Using hash collision techniques, they modify parts of the binary to keep the final hash the same. Step 5: This is easier with SHA-1 or MD5 but nearly impossible with SHA-256 without quantum tools. Step 6: The malicious firmware is uploaded and accepted by the device. Step 7: The device now runs attacker code, believing it to be genuine. Step 8: This could allow root access, backdoor creation, or data theft.
- **Detection**: Check if firmware binary hash differs from known clean sample; look for unauthorized code segments
- **Solution**: Require signed firmware updates using asymmetric crypto (e.g., RSA/ECDSA signatures); reject hash-only integrity checks
- **Tags**: Embedded, firmware backdoor, IoT attack

## Digital Signature Spoofing (Hash Preimage)

- **Attack Type**: Signature Forgery using Preimage
- **Target**: Digital documents, signed messages
- **Vulnerability**: Use of weak hash functions in digital signing
- **MITRE**: T1588.002 – Code Signing Certificates
- **Impact**: Forged messages, financial/legal damage
- **Tools**: Custom preimage tools, Python scripts
- **Scenario**: Exploit where attacker finds a preimage that matches the hash of signed content, allowing signature reuse on forged data.
- **Attack Steps**: Step 1: Digital signatures work by signing the hash of a document, not the document itself. If attacker can find another input with the same hash, they can reuse the signature. Step 2: Suppose an attacker gets a signed document and its digital signature (e.g., from a public email or PDF). Step 3: They compute its hash and attempt to generate new forged content with the same hash using a preimage attack. Step 4: With this crafted content, they apply the original signature. Step 5: The verification passes, even though the content is malicious. Step 6: This is only feasible with weak hash functions (e.g., MD5 or SHA1). Step 7: It’s particularly dangerous in financial contracts, secure emails, or legal PDFs.
- **Detection**: Verify document contents match original; inspect signature generation algorithms for weak hashes
- **Solution**: Upgrade to SHA-2/3 family; use secure signature schemes; never use MD5/SHA1 in cryptographic signing
- **Tags**: Digital signature spoofing, MD5, SHA1, legal doc

## Token/Session ID Reversal via Preimage

- **Attack Type**: Session Hijacking via Preimage
- **Target**: Web apps, authentication systems
- **Vulnerability**: Predictable token hashing scheme
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Account hijacking, unauthorized session access
- **Tools**: Burp Suite, Hashcat, Python
- **Scenario**: Attempt to recover original token/session ID input by guessing values that hash to the same output, used for unauthorized access.
- **Attack Steps**: Step 1: A web application uses hashed tokens or session IDs to authenticate users (e.g., session_token = SHA1(user_id + timestamp)). Step 2: If the attacker gets a token and suspects how it’s generated, they try reversing it. Step 3: They guess combinations of user IDs and timestamps (or other parameters) and hash them. Step 4: If a guessed combination matches the token, they’ve reversed the process. Step 5: They can now generate valid tokens for other users or hijack sessions. Step 6: This is feasible only if token generation is predictable or short (e.g., usernames + simple timestamps). Step 7: This is a preimage attack because they are finding input values for a known hash. Step 8: Often used alongside brute force or social engineering.
- **Detection**: Detect anomalies in token structure or reused sessions; rate-limit failed session validations
- **Solution**: Use long, random session tokens; avoid predictable input combinations; use HMAC with secret key for token generation
- **Tags**: Session hijack, predictable hash, preimage attack

## Hash-based License Bypass

- **Attack Type**: Software License Preimage Forgery
- **Target**: Software with local license validation
- **Vulnerability**: Weak or unsalted hash-based key check
- **MITRE**: T1600 – Forge Data or Protocol
- **Impact**: Bypasses licensing; revenue loss; software piracy
- **Tools**: Python, Hashcat, Custom keygen tools
- **Scenario**: Software uses hashed license keys (e.g., MD5 or SHA1 of serial number) to validate users. Attackers reverse-engineer or brute force inputs that match valid hashes.
- **Attack Steps**: Step 1: Many commercial software products use license validation that compares user-provided license input to a stored or computed hash (e.g., hash(input) == stored_hash). Step 2: Attacker obtains a legitimate license hash (from trial software, leaked keys, or reverse engineering). Step 3: Using knowledge of the hash algorithm (e.g., MD5), attacker writes a script or uses tools like Hashcat to brute-force possible input strings until a matching hash is produced. Step 4: Once the input (license key) that matches the known hash is found, the attacker now has a fake key that passes validation. Step 5: Some systems are weak due to short key lengths (e.g., 6–10 characters), predictable inputs, or use MD5/SHA1 hashes without salt. Step 6: This allows software to be unlocked without a real license.
- **Detection**: Detect unauthorized keys by logging hash inputs and license activations; look for abnormal license reuse
- **Solution**: Use asymmetric crypto (e.g., RSA-signed licenses); avoid raw hash comparisons; validate on server side
- **Tags**: Software piracy, license cracking, hash bypass

## Credential Recovery via Preimage (e.g., LM Hashes)

- **Attack Type**: Legacy Hash Preimage Recovery
- **Target**: Windows systems using LM/NTLM hashes
- **Vulnerability**: Use of outdated hash functions without salt
- **MITRE**: T1003.001 – OS Credential Dumping
- **Impact**: Credential theft, privilege escalation
- **Tools**: Hashcat, JohnTheRipper, Rainbow Tables
- **Scenario**: Attacker uses preimage techniques on outdated hash algorithms (e.g., LM/NTLM) to recover plaintext passwords and gain unauthorized access.
- **Attack Steps**: Step 1: In older Windows systems, passwords are stored using LM (LAN Manager) or NTLM hashes. LM is especially weak — it splits passwords into 7-character chunks and hashes them independently. Step 2: Attacker obtains password hashes by dumping SAM database or capturing credentials during network authentication. Step 3: They load the LM hash into Hashcat or John the Ripper and use rainbow tables or brute force to recover the original password. Step 4: Since LM uses limited charset and uppercase-only hashing, it can be cracked within seconds to minutes. Step 5: Once password is recovered, attacker logs in or escalates privileges. Step 6: NTLM is better but still weak against dictionary/rainbow table attacks unless long passwords and salting are enforced. Step 7: This is a classic real-world preimage attack.
- **Detection**: Alert on use of LM hashes in systems; monitor for hash cracking activity; enforce password change policies
- **Solution**: Disable LM hashes in registry; enforce long complex passwords; switch to modern hashing with salt (e.g., bcrypt, scrypt)
- **Tags**: NTLM, LM, password cracking, legacy hash

## Preimage Exploit on Blockchain Smart Contracts

- **Attack Type**: Smart Contract Hash Preimage Leak
- **Target**: Ethereum Smart Contracts
- **Vulnerability**: Weak preimage-protected contract logic
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: Token theft, unauthorized smart contract access
- **Tools**: Remix IDE, Ethers.js, Custom hash brute force
- **Scenario**: Exploiting use of preimage-based conditions (e.g., require(hash(x)==y)) in smart contracts to find x and steal funds or trigger logic.
- **Attack Steps**: Step 1: Many Ethereum smart contracts store hashed values (e.g., SHA-256 or keccak256) and later compare user input x with a stored hash y using require(hash(x) == y). Step 2: If an attacker knows y but x is weak (e.g., short secret code, predictable string), they try to find x such that hash(x) == y. Step 3: Using brute force tools or scripts, attacker iterates over possible values until a match is found. Step 4: Once the preimage x is found, attacker can call the smart contract with this input and pass validation. Step 5: This could allow access to locked funds, trigger admin-only functions, or bypass authentication gates. Step 6: This attack works if the original hashed secret was poorly chosen (e.g., small number or string like “admin123”). Step 7: Strong secrets (32+ random bytes) mitigate this risk.
- **Detection**: Monitor failed contract calls; check for repeated calls to hash-verified functions; log brute attempts
- **Solution**: Never store only a hash for critical access; use asymmetric signatures or zero-knowledge proofs for verification
- **Tags**: Smart Contract, Blockchain, Ethereum, SHA3

## Length Extension with Preimage Context

- **Attack Type**: Hash Length Extension + Preimage Knowledge
- **Target**: APIs, signed URLs, cookies
- **Vulnerability**: Use of vulnerable hash in unkeyed HMAC-like constructs
- **MITRE**: T1600 – Forge Data or Protocol
- **Impact**: Signature forgery, data injection, API manipulation
- **Tools**: Python, Hash Extender, Hashpump, Burp Suite
- **Scenario**: Exploits length extension flaw in hash functions like MD5/SHA1 when attacker knows the hash of a message and wants to forge a longer version without knowing the original secret.
- **Attack Steps**: Step 1: Many APIs or systems use hash(message + secret) for validation. If attacker knows hash(secret + message), and the hash algorithm is vulnerable to length extension (e.g., MD5, SHA1), they can add data to the message without knowing the secret. Step 2: Attacker uses tools like hashpump or hash_extender to forge a new message and valid hash by guessing the length of the unknown secret. Step 3: Inputs: original message, known hash, data to append, guessed length of secret. Step 4: Tool generates valid new hash and forged extended message like: original_message + padding + attacker_data. Step 5: Attacker sends this to the server/system. If the system recalculates the hash in the same way, it will accept the new message as valid. Step 6: Preimage knowledge (e.g., if attacker knows likely format of original message or prefix) makes this attack easier. Step 7: Success leads to data injection, signature forgery, or access bypass.
- **Detection**: Monitor message lengths and padding patterns; flag unusual hash values; log repeated API calls with varied message lengths
- **Solution**: Use HMAC instead of raw hashes; never use hash(secret + message) for auth; use modern MACs like HMAC-SHA256 or BLAKE2
- **Tags**: Length Extension, MD5, SHA1, API Bypass

## HMAC Forgery via Preimage Guessing

- **Attack Type**: HMAC Key Guessing / Preimage
- **Target**: APIs, signed tokens, message auth
- **Vulnerability**: Weak or predictable HMAC secret keys
- **MITRE**: T1606.001 – Forge Authentication Token
- **Impact**: Authentication bypass, data tampering
- **Tools**: Hashcat, Python HMAC libs, RockYou.txt
- **Scenario**: If the HMAC secret key is short, weak, or reused across messages, attacker can guess it and use preimage techniques to forge valid HMACs and bypass authentication.
- **Attack Steps**: Step 1: HMAC is widely used for message authentication: HMAC(secret, message). Security depends entirely on secrecy and strength of the key. Step 2: If attacker knows a valid message-HMAC pair and suspects weak keys are used (e.g., admin, 123456, companyname2022), they can brute-force the HMAC key using preimage attack. Step 3: Attacker loads known (message, HMAC) pairs into a script and brute-forces potential keys using a wordlist like rockyou.txt. Step 4: For each guess, script computes HMAC(guess, message) and compares to known HMAC. Step 5: If a match is found, attacker now knows the secret and can forge new messages with valid HMACs. Step 6: With this forged HMAC, attacker can bypass signature checks, impersonate users, or inject commands. Step 7: This is real-world threat where developers hardcode predictable or short keys.
- **Detection**: Monitor HMAC generation patterns; alert on brute attempts; analyze repeated failed HMAC verifications
- **Solution**: Use strong random secrets (≥256 bits); rotate keys often; enforce HMAC key entropy with validators
- **Tags**: HMAC, Preimage, Weak Key, Brute Force, Forgery

## PDF Document Manipulation using Preimage Tricks

- **Attack Type**: PDF Hash Preimage Forgery
- **Target**: Digitally signed PDF documents
- **Vulnerability**: Hash-only validation of partial file content
- **MITRE**: T1600 – Forge Data or Protocol
- **Impact**: Tampering of official documents, fraud
- **Tools**: PDFtk, Hash collision tools, PDF Exploits
- **Scenario**: Some PDF signing systems only verify file hashes (not full content). Attackers use preimage knowledge to craft malicious PDFs that hash to same value as signed ones.
- **Attack Steps**: Step 1: Digital signatures in PDF often rely on computing a hash of the file’s content, then signing it. Some systems naïvely sign only part of the PDF or allow dynamic fields (like form data). Step 2: Attacker gets a legitimate signed PDF and its hash or signature. Step 3: By analyzing the structure of the PDF (which is flexible and can have multiple segments, objects, or padding), attacker appends or modifies parts outside the signed portion (e.g., form fields, hidden layers). Step 4: Using known structure and hash knowledge, attacker crafts a new PDF that preserves the signed hash but has altered content — like swapping values, changing recipient, or inserting malicious content. Step 5: This is possible if signature verification checks only the hash, not the full PDF byte-by-byte. Step 6: Victim opens the forged PDF and assumes it is valid and signed, but attacker content is injected. Step 7: This attack abuses poor hash handling and weak verification logic.
- **Detection**: Use forensic tools to analyze signed PDF structure; check for appended segments or altered metadata
- **Solution**: Use cryptographic signatures covering the entire file byte-by-byte; validate signature format; disallow post-sign edits
- **Tags**: PDF tampering, digital signature bypass, document forgery

