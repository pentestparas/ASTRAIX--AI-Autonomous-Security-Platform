# Browser Security → Browser Extension Abuse Attacks

## Keylogger Extension Captures Passwords Across All Sites

- **Attack Type**: Malicious Extension
- **Target**: End users via Chrome Web Store
- **Vulnerability**: Excessive extension permissions + script injection
- **MITRE**: T1056.001
- **Impact**: Credential theft from trusted web platforms
- **Tools**: Chrome Extension API, JavaScript, Web Console
- **Scenario**: A fake productivity extension logs all keystrokes entered by the user, including passwords typed into secure fields
- **Attack Steps**: 1. The attacker builds a Chrome extension that claims to enhance typing speed analysis, asking for “read and modify all data on all websites” permissions. 2. Once installed, the extension uses content_scripts to inject JavaScript into every visited tab. 3. This injected script listens to all keystrokes using document.addEventListener('keydown'), and captures typed input regardless of the webpage. 4. When users log in to banking portals, Gmail, or any secure site, the extension silently captures their usernames and passwords. 5. Captured data is buffered and periodically exfiltrated to a remote C2 server using HTTPS POST requests. 6. No visual indication is presented to the user, and the extension behaves innocuously on the surface. 7. Over time, the attacker accumulates credentials to high-value accounts and may sell them or use them for fraud. 8. Users remain unaware until unauthorized access occurs.
- **Detection**: Monitor network activity of extensions and check for excessive permissions
- **Solution**: Enforce minimum required permissions and use browser extension review tools
- **Tags**: #keylogger #browserextension #credentialtheft

## Fake Ad Blocker Harvests Login Cookies

- **Attack Type**: Malicious Extension
- **Target**: Users installing popular-looking extensions
- **Vulnerability**: Over-permissive cookie access
- **MITRE**: T1539
- **Impact**: Session hijack and account takeover
- **Tools**: Chrome DevTools, Cookie API
- **Scenario**: An ad blocker clone steals cookies from popular sites and bypasses 2FA protections
- **Attack Steps**: 1. A malicious actor uploads a Chrome extension imitating a popular ad blocker with minor branding differences. 2. Once installed, the extension injects scripts via content_scripts and requests cookies API access. 3. When users visit popular websites like Facebook or Gmail, the extension silently accesses session cookies using chrome.cookies.getAll(). 4. These cookies, especially those with long expiration and auth tokens, are sent to the attacker's remote server. 5. The attacker then imports these cookies into their browser sessions using tools like EditThisCookie or Puppeteer. 6. This allows them to bypass traditional password-based logins and even 2FA sessions if tokens are still active. 7. The user remains logged in and unaware, with no login alert triggered. 8. The attacker now fully impersonates the victim.
- **Detection**: Monitor extension traffic for unauthorized cookie access
- **Solution**: Block cookie access unless required and enforce integrity checks
- **Tags**: #cookiehijack #fakeadblocker #sessiontheft

## Screenshot Stealer Using Extension API

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Banking portals, webmail, SaaS dashboards
- **Vulnerability**: Abuse of desktop/screen capture APIs
- **MITRE**: T1113
- **Impact**: Data exfiltration via screen capture
- **Tools**: Chrome Extension API, screenshots API
- **Scenario**: Malicious extension captures screen images of sensitive sessions like banking or email
- **Attack Steps**: 1. An extension masquerading as a “visual note-taker” asks for the activeTab, tabs, and desktopCapture permissions. 2. When the user visits sensitive sites, the extension programmatically activates screenshot functionality using chrome.tabCapture.capture() or chrome.desktopCapture.chooseDesktopMedia(). 3. These APIs return a media stream which is then drawn onto a hidden canvas. 4. The canvas image is converted to base64 and transmitted to a remote attacker-controlled server. 5. The attacker accumulates screenshots from banking portals, OTP screens, crypto wallets, and other sensitive interfaces. 6. These images can be processed with OCR to extract details like balances, account numbers, or transaction data. 7. Since the extension appears to provide useful features, the user does not suspect foul play. 8. The entire attack is stealthy and persistent.
- **Detection**: Check installed extension permissions and inspect background activity
- **Solution**: Restrict sensitive APIs and prompt explicit user consent each time
- **Tags**: #screensniff #extensionapi #visualdataexfil

## MITB Attack via Trojanized Extension Alters Transaction Amounts

- **Attack Type**: Man-in-the-Browser
- **Target**: Banking and financial portals
- **Vulnerability**: DOM manipulation of financial forms
- **MITRE**: T1557.002
- **Impact**: Silent financial fraud
- **Tools**: Web Traffic Sniffer, MITB Toolkit
- **Scenario**: A trojanized browser extension manipulates the values in online banking transfers after user input
- **Attack Steps**: 1. A user installs a finance-related browser extension from an unverified source that promises budgeting assistance. 2. Once active, the extension injects a content script into banking portals via matches rules in the manifest. 3. The script monitors DOM elements related to fund transfer fields, like recipient name and amount. 4. After the user enters legitimate transfer details and clicks “Submit,” the extension intercepts the form submission event. 5. It modifies the transfer amount and destination account in-flight via JavaScript, replacing it with attacker-controlled data. 6. The user sees the original values during confirmation, but the final payload sent to the bank has altered data. 7. Funds are transferred to attacker’s mule account while the user believes the transfer was successful. 8. The extension deletes all logs and hides traces in browser history.
- **Detection**: Inspect JavaScript injection and mutation of DOM values in real time
- **Solution**: Restrict extensions on sensitive domains; use transaction confirmation tokens
- **Tags**: #mitb #bankfraud #transactionhijack

## Bookmark Access via Extension API to Profile Victim

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Individual user browsers
- **Vulnerability**: Abused bookmarks API permissions
- **MITRE**: T1205
- **Impact**: OSINT-style profiling and phishing prep
- **Tools**: Chrome Extension API, bookmarks API
- **Scenario**: Extension reads user’s bookmarks to infer their browsing history, interests, and logins
- **Attack Steps**: 1. The attacker uploads a “Bookmark Manager Enhancer” extension that requests access to bookmarks API. 2. Once installed, the extension crawls the user’s bookmarks tree using chrome.bookmarks.getTree(). 3. It identifies patterns in saved links — such as banking sites, healthcare portals, or internal company dashboards. 4. These links reveal personal interests, services used, and professional affiliations. 5. The data is sent to the attacker’s server and analyzed to build a social engineering profile. 6. The attacker uses this information for targeted phishing, credential stuffing, or business email compromise (BEC). 7. The user is unaware, as no active behavior or UI changes are made by the extension.
- **Detection**: Monitor extension access to bookmarks and log outbound traffic
- **Solution**: Block unnecessary API access and review extension manifest rigorously
- **Tags**: #bookmarksnoop #osint #apiabuse

## Clipboard Hijack via Extension in Cryptocurrency Sites

- **Attack Type**: Malicious Extension
- **Target**: Crypto wallets, exchanges
- **Vulnerability**: Clipboard hijack via regex detection
- **MITRE**: T1112
- **Impact**: Financial loss via wallet redirection
- **Tools**: Clipboard Event Monitor, JS Console
- **Scenario**: An extension changes copied crypto wallet addresses to attacker’s address in real time
- **Attack Steps**: 1. The attacker builds a “Clipboard Optimizer” Chrome extension claiming to enhance clipboard formatting. 2. It requests permissions for clipboardRead and clipboardWrite. 3. The extension uses document.execCommand('paste') or navigator.clipboard.readText() to monitor clipboard data. 4. When the user copies a cryptocurrency address (e.g., BTC, ETH), the extension detects the pattern via regex. 5. It replaces the clipboard content with an attacker-controlled address before the user pastes it. 6. The user unknowingly pastes the wrong address into a withdrawal form and sends funds to the attacker. 7. Since the address structure looks similar, users rarely notice the swap. 8. The extension performs this silently without UI changes.
- **Detection**: Inspect clipboard access via devtools and analyze regex filters
- **Solution**: Block clipboard access or restrict via feature flags
- **Tags**: #clipboardattack #cryptoheist #walletswap

## Extension Adds Fake Login Modal to Capture Credentials

- **Attack Type**: Malicious Extension
- **Target**: Popular platforms like Gmail or Facebook
- **Vulnerability**: UI spoofing via injected modals
- **MITRE**: T1204.002
- **Impact**: Credential harvesting via fake overlays
- **Tools**: Chrome Extension, DOM Observer
- **Scenario**: Injected modal overlays mimic Gmail/Facebook login and steal user credentials
- **Attack Steps**: 1. A malicious extension is installed claiming to add dark mode to websites. 2. The extension injects a script that uses MutationObserver to detect when users visit Gmail or Facebook. 3. After a few seconds of user inactivity, it injects a fake login modal on top of the existing content. 4. The modal mimics the legitimate UI using cloned HTML/CSS from the site. 5. When users enter their email and password, the form submission is intercepted and sent to a remote C2 server. 6. A fake “Session expired” message is displayed, and the modal disappears to avoid suspicion. 7. Users assume they mistyped or were logged out and retry login — often now going to the real site. 8. By then, credentials have already been compromised.
- **Detection**: Detect overlays in DOM and inspect network calls from extensions
- **Solution**: Use two-factor auth and prevent overlays using CSP and iframe sandboxing
- **Tags**: #loginphish #modalscam #sessiontheft

## Inter-Tab Surveillance via Chrome Messaging API

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Users with many browser tabs open
- **Vulnerability**: Overuse of tabs API + injection
- **MITRE**: T1114
- **Impact**: Privacy invasion and tracking
- **Tools**: Chrome API, Messaging Framework
- **Scenario**: Extension spies on all open tabs to learn user browsing patterns and session states
- **Attack Steps**: 1. An extension poses as a tab grouping utility and requests tabs and storage permissions. 2. It sets up a background script that uses chrome.tabs.query({}) to enumerate all active tabs. 3. Each tab’s URL, title, and favicon is logged in real time. 4. The extension also injects a script into open tabs using chrome.scripting.executeScript(). 5. These scripts can monitor session variables, cookies (if accessible), and login statuses via page DOM. 6. Data is collected and sent periodically to the attacker for session tracking or phishing campaign targeting. 7. This also allows them to detect when a user is on specific pages (like “checkout” or “OTP”) for timing attacks.
- **Detection**: Inspect tab permissions and monitor JS execution across tabs
- **Solution**: Restrict tabs API access and block script injection on sensitive sites
- **Tags**: #tabmonitoring #sessiontracking #apiabuse

## Fake Extension Auto-Updates to Malicious Version

- **Attack Type**: Malicious Extension
- **Target**: Any browser users
- **Vulnerability**: Auto-update trust chain exploit
- **MITRE**: T1204
- **Impact**: Persistent spyware via trust decay
- **Tools**: Chrome Web Store, CRX Repo
- **Scenario**: A benign extension later updates to a version that injects spyware
- **Attack Steps**: 1. The attacker uploads a useful extension with clean code and minor functionality. 2. It gains 1000s of users and earns positive reviews. 3. Later, the attacker pushes an auto-update through the extension’s update_url in the manifest. 4. The new version adds malicious behavior like DOM spying, credential logging, and ad injection. 5. Users’ browsers update silently, since extension updates are auto-applied in the background. 6. New code injects scripts into banking and shopping sites to extract credentials and payment data. 7. Victims are unaware as UI behavior remains similar to the earlier version. 8. The attacker now owns a trusted spyware platform.
- **Detection**: Monitor version diffs of installed extensions
- **Solution**: Use permission warnings on update and enforce manual review
- **Tags**: #extensionupdate #spyware #supplychain

## MITB via JavaScript Hooking in Online Payment Portals

- **Attack Type**: Man-in-the-Browser (MITB)
- **Target**: E-commerce and checkout pages
- **Vulnerability**: Script hooking and MITB injection
- **MITRE**: T1557.002
- **Impact**: Payment card theft without user awareness
- **Tools**: JS Hook Tools, Web Console
- **Scenario**: Script-injected extension hooks into checkout page to steal card details
- **Attack Steps**: 1. A trojan extension poses as a shopping helper and injects JavaScript into checkout pages of known e-commerce platforms. 2. It hooks into the onsubmit event of forms where users enter card data. 3. When the form is about to be submitted, it clones all input values (card number, expiry, CVV) and sends them to the attacker's endpoint. 4. The original form is then submitted as normal, so transactions still complete. 5. The user receives confirmation and sees nothing suspicious. 6. The attacker collects real-time card data from thousands of users across platforms. 7. Stolen data is then resold or used in automated carding attacks. 8. All this happens in the user’s browser without any phishing site.
- **Detection**: Monitor form hooks and audit scripts from extensions
- **Solution**: Use payment overlays (e.g., iframe vaults) that isolate card inputs
- **Tags**: #mitb #cardtheft #checkoutspy

## Extension Bypasses CSP to Inject Malicious Script

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Sites with strong CSP like Gmail, banking
- **Vulnerability**: CSP circumvention via extension privileges
- **MITRE**: T1204.002
- **Impact**: Script injection bypassing browser defenses
- **Tools**: Chrome Extension API, DevTools
- **Scenario**: Extension injects scripts even on sites with strict CSP
- **Attack Steps**: 1. The attacker builds an extension with content_scripts targeting common websites. 2. When installed, the extension injects JavaScript into pages even if CSP headers block external scripts. 3. This is possible because extensions execute in a privileged context outside the page’s CSP enforcement. 4. The script collects sensitive DOM data, like autofilled emails or addresses. 5. It also inserts new elements (e.g., phishing links or ads) into secure portals. 6. The malicious activity is concealed by mimicking native design and namespacing CSS. 7. All stolen data is sent silently to the attacker's backend over HTTPS. 8. Users and developers fail to notice since CSP audit tools don’t track extension scripts.
- **Detection**: Use browser devtools to detect unexpected DOM mutations
- **Solution**: Monitor and isolate extension privileges; apply Manifest V3 restrictions
- **Tags**: #cspbypass #scriptexecution #apiabuse

## Extension Hijacks Omnibox Input for Phishing

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Web browser omnibox users
- **Vulnerability**: Misuse of omnibox redirection feature
- **MITRE**: T1176
- **Impact**: Search poisoning and phishing redirection
- **Tools**: Chrome Omnibox API
- **Scenario**: A browser extension captures search bar input to redirect users to malicious search results
- **Attack Steps**: 1. A fake "Smart Search" extension requests omnibox permission during installation. 2. It registers a custom keyword to intercept all search queries from the address bar. 3. When users type a search term, the extension redirects the query to a rogue search engine. 4. The rogue site displays manipulated ads and malicious links near the top. 5. Some links lead to phishing pages or malware downloads. 6. Users think they’re just using a faster search provider. 7. Over time, this also profiles user interests for targeted fraud. 8. Since no page is visibly altered, users remain unaware.
- **Detection**: Analyze installed extensions and monitor DNS logs
- **Solution**: Disallow unnecessary omnibox access; prefer default engines
- **Tags**: #omniboxhijack #searchredirect #extensionabuse

## Malicious Extension Records Audio via Microphone API

- **Attack Type**: Malicious Extension
- **Target**: Any user with browser mic permissions
- **Vulnerability**: Stealthy audio recording via mediaDevices API
- **MITRE**: T1123
- **Impact**: Surveillance, corporate espionage
- **Tools**: Chrome Media API, Mic Monitor
- **Scenario**: A malicious browser extension records audio from the user’s mic in the background
- **Attack Steps**: 1. A voice-activated task manager extension is published with mic permissions in its manifest. 2. After install, the background script activates mic recording when the browser is open using navigator.mediaDevices.getUserMedia. 3. Audio streams are collected and buffered via WebRTC or local blobs. 4. The data is sent to the attacker’s server during idle times to avoid suspicion. 5. Even when the user is not actively using the extension, it runs in the background silently. 6. Sensitive private conversations or meetings can be recorded. 7. No browser-level mic indicator is shown for some environments. 8. Victims realize only after forensic investigation.
- **Detection**: Check for mic permissions in installed extensions
- **Solution**: Enforce runtime prompts for all media access
- **Tags**: #micspy #extensioneavesdrop #privacybreach

## Browser Extension Spoofs Web3 Wallet to Steal Crypto

- **Attack Type**: Malicious Extension
- **Target**: Crypto users installing wallet extensions
- **Vulnerability**: Fake UI & Web3 API misuse
- **MITRE**: T1566.001
- **Impact**: Full crypto asset theft
- **Tools**: Browser Console, Ethereum JS Libs
- **Scenario**: Fake crypto wallet extension mimics MetaMask and intercepts transactions
- **Attack Steps**: 1. The attacker builds a browser extension mimicking MetaMask UI and branding. 2. Once installed, the extension asks for wallet seed phrase or private key. 3. It then displays a fake balance and transaction history, syncing only with attacker’s backend. 4. When the user tries to send ETH or tokens, the extension reroutes the transaction to attacker-controlled addresses. 5. Real blockchain confirmations are mimicked using dummy data. 6. The extension also blocks access to legitimate MetaMask or Web3 providers to avoid detection. 7. User’s entire wallet is drained while believing funds are being processed.
- **Detection**: Analyze source and signer of Web3 transactions
- **Solution**: Only install wallets from official vendor domains
- **Tags**: #web3phish #walletspoof #cryptoextension

## Extension Hooks DOM to Capture One-Time Passwords (OTP)

- **Attack Type**: Man-in-the-Browser (MITB)
- **Target**: 2FA-enabled platforms
- **Vulnerability**: DOM spying and field hooking
- **MITRE**: T1557.002
- **Impact**: Full account compromise despite OTP
- **Tools**: DevTools, DOM Monitor
- **Scenario**: Extension monitors OTP fields in banking/2FA flows
- **Attack Steps**: 1. The extension injects code into login pages of major websites. 2. It hooks into input fields that match patterns like “otp”, “2fa”, or “code”. 3. When users receive and type OTPs into these fields, the values are captured. 4. The script relays OTPs to the attacker’s server in real-time. 5. Simultaneously, it may auto-submit forms to ensure the OTP remains valid. 6. This allows the attacker to perform complete login from a different location. 7. Users never realize the OTP was intercepted mid-session.
- **Detection**: Monitor JavaScript listeners on sensitive fields
- **Solution**: Block extension injection on login flows via CSP
- **Tags**: #otpsteal #mitb #extensionhooking

## Extension Creates Fake Download Prompts for Malware

- **Attack Type**: Malicious Extension
- **Target**: File-sharing or email download sites
- **Vulnerability**: UI spoofing of download prompts
- **MITRE**: T1204.001
- **Impact**: Initial malware infection vector
- **Tools**: JavaScript UI Toolkit, CSS spoofing
- **Scenario**: Extension mimics native browser download UI to trick users into installing malware
- **Attack Steps**: 1. An extension claims to enhance download speeds and displays a fake download manager panel. 2. It injects UI elements that look identical to Chrome’s native download prompts. 3. When users visit specific file-sharing or email services, it overlays a “Click to save” button. 4. Clicking the button downloads a malicious .exe or .apk file. 5. Since the prompt looks native, users are more likely to trust it. 6. The malware is executed outside browser scope and persists.
- **Detection**: Watch for fake UI layers and monitor download events
- **Solution**: Enforce signature checks and content filters
- **Tags**: #malwareprompt #downloadspoof #extensionmalware

## Extension Reads Browser History for Targeted Ads

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Any browser user
- **Vulnerability**: Over-privileged access to browser history
- **MITRE**: T1114
- **Impact**: Privacy breach and profiling
- **Tools**: Chrome API, Browser History
- **Scenario**: Reads and sells user browsing history to third parties
- **Attack Steps**: 1. The extension asks for access to chrome.history API during install. 2. It periodically scans history entries using chrome.history.search(). 3. The data is categorized based on shopping, finance, or adult content. 4. These insights are sold to ad networks or used for custom phishing campaigns. 5. Users receive ads matching sensitive searches, which also leaks intent.
- **Detection**: Monitor API usage patterns and outgoing network calls
- **Solution**: Prevent history access unless app functionality requires it
- **Tags**: #historyleak #adprofiling #privacyabuse

## Stealthy Update of Extension with Encrypted Payloads

- **Attack Type**: Malicious Extension
- **Target**: Chrome Web Store
- **Vulnerability**: Encrypted payload fetch after install
- **MITRE**: T1027
- **Impact**: Dynamic behavior shift post-review
- **Tools**: CRX Analyzer, Encrypted Payload Sniffer
- **Scenario**: Extension fetches encrypted malicious code from C2 server post-review
- **Attack Steps**: 1. The extension passes Web Store review with clean source code. 2. Upon install, it fetches a config file from attacker’s server. 3. The file contains encrypted JavaScript blobs disguised as harmless JSON. 4. A background script decrypts and dynamically injects it into visited pages. 5. This allows on-the-fly updates of malicious logic without triggering detection. 6. The payloads perform credential harvesting and ad injection based on domain.
- **Detection**: Scan runtime network calls and decrypt blobs
- **Solution**: Enforce static manifest behavior post-publish
- **Tags**: #extensionevade #encryption #malwaredelivery

## Extension Adds Keylogger to Webmail Interfaces

- **Attack Type**: Man-in-the-Browser (MITB)
- **Target**: Webmail portals
- **Vulnerability**: DOM listeners in compose editors
- **MITRE**: T1056.001
- **Impact**: Sensitive data leakage
- **Tools**: JS Injector, Webmail Sniffer
- **Scenario**: Captures typed content in Gmail, Outlook, etc.
- **Attack Steps**: 1. Once installed, the extension injects a script into webmail interfaces. 2. It attaches keypress listeners to compose windows. 3. All typed messages, including drafts, passwords, and sensitive text, are captured. 4. Even messages not sent yet are logged and exfiltrated.
- **Detection**: Monitor for JS injection in compose UIs
- **Solution**: Isolate editors via shadow DOM
- **Tags**: #keylogger #webmailspy #mitb

## Extension Adds Malicious Context Menu to Execute Commands

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: General websites
- **Vulnerability**: Malicious use of context menu API
- **MITRE**: T1202
- **Impact**: Social engineering trigger for JS payload
- **Tools**: Context Menu API, JS Executor
- **Scenario**: Adds right-click option to execute harmful JS in browser
- **Attack Steps**: 1. Extension requests contextMenus permission and adds a suspicious entry like “Run Cleaner”. 2. When clicked, it executes JavaScript using chrome.scripting.executeScript(). 3. The script may exfiltrate data, redirect the user, or manipulate local storage.
- **Detection**: Monitor menu creation APIs in extensions
- **Solution**: Block dynamic JS execution from menus
- **Tags**: #contextmenu #extensioninject #jsabuse

## Extension Modifies E-Commerce Prices for Phishing

- **Attack Type**: Man-in-the-Browser (MITB)
- **Target**: Online shopping websites
- **Vulnerability**: Content manipulation via DOM injection
- **MITRE**: T1557.002
- **Impact**: Payment credential theft
- **Tools**: DOM Inspector, JavaScript Injector
- **Scenario**: Malicious extension changes product prices to lure users into fake checkout pages
- **Attack Steps**: 1. The attacker builds a browser extension claiming to offer coupons or price comparisons. 2. On visiting a shopping website, the extension injects JavaScript to alter displayed product prices (e.g., lowering expensive items). 3. When users try to purchase, the "Buy Now" button is redirected to a fake checkout page that mimics the original site. 4. Users input payment details into this fake page. 5. The credentials are harvested and sent to the attacker. 6. A fake error message appears to prevent actual payment processing, keeping users unaware. 7. Users believe the site had an issue, while data has already been stolen. 8. The extension clears local storage to remove traces of manipulation.
- **Detection**: Check DOM diff between trusted and rendered HTML
- **Solution**: Use isolated payment iFrames and domain verification
- **Tags**: #phishing #checkoutspoof #mitb

## Extension With Hidden Torrent Tracker Monitor

- **Attack Type**: Malicious Extension
- **Target**: Torrent users
- **Vulnerability**: Background port scanning via WebRTC
- **MITRE**: T1040
- **Impact**: Privacy violation & legal risk
- **Tools**: JavaScript, WebRTC Leak Detector
- **Scenario**: Browser plugin secretly monitors torrent traffic and reports back to attacker
- **Attack Steps**: 1. The extension claims to “accelerate downloads” but silently monitors torrent activity via WebRTC leaks. 2. It checks if certain ports are active or common trackers are in use. 3. On detection, it logs the file name, size, and source IP. 4. The data is encrypted and periodically uploaded to the attacker’s server. 5. Over time, the attacker builds a database of what files the user shares or downloads. 6. This info can be used for blackmail or DMCAs.
- **Detection**: Block background WebRTC use and scan for suspicious ports
- **Solution**: Disable WebRTC unless needed; monitor DNS leak tools
- **Tags**: #webrtcspy #torrenttracking #extensionleak

## Bookmark-Based Persistence via Extension

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Browser bookmarks
- **Vulnerability**: Persistent payload injection via bookmarklets
- **MITRE**: T1053.005
- **Impact**: Post-uninstall attack continuation
- **Tools**: Chrome API, Bookmarklet Injector
- **Scenario**: Extension adds malicious bookmarklets that can execute code on demand
- **Attack Steps**: 1. A malicious extension quietly adds several hidden bookmarklets to the user's bookmarks folder. 2. These bookmarklets contain JavaScript payloads that run when clicked. 3. Even if the extension is removed, the bookmarklets persist. 4. When clicked by accident or on purpose, these can reinject backdoors or redirect to attacker-controlled pages. 5. Bookmarks often go unchecked, making it an overlooked persistence method.
- **Detection**: Monitor bookmark creation events in extensions
- **Solution**: Block JS-based bookmarklets in corporate environments
- **Tags**: #bookmarkbackdoor #persistence #extensionabuse

## Fake Extension Auto-Adds Proxy Settings

- **Attack Type**: Malicious Extension
- **Target**: General browser users
- **Vulnerability**: Proxy hijack via extension config
- **MITRE**: T1557.001
- **Impact**: MITM via browser-level proxy
- **Tools**: ProxySwitch API, Chrome DevTools
- **Scenario**: Extension silently sets proxy config to redirect traffic through attacker server
- **Attack Steps**: 1. An extension requests proxy permission and silently sets a custom proxy route. 2. All browser traffic is now routed through the attacker’s controlled server. 3. The attacker inspects and logs all HTTP(S) requests, even modifying responses. 4. The user experiences only slightly slower browsing and remains unaware. 5. This allows full MITM interception of unencrypted traffic and metadata leakage from HTTPS.
- **Detection**: Monitor system proxy settings & browser overrides
- **Solution**: Block proxy configuration unless explicitly needed
- **Tags**: #proxyabuse #browsermitm #trafficintercept

## Extension Tracks Password Resets and Logs New Passwords

- **Attack Type**: Man-in-the-Browser (MITB)
- **Target**: Password reset flows
- **Vulnerability**: DOM interception of password change forms
- **MITRE**: T1056.001
- **Impact**: Persistent account access after recovery
- **Tools**: JavaScript DOM Hooks, Event Listener Tracker
- **Scenario**: Hooks password reset forms and logs newly set passwords silently
- **Attack Steps**: 1. Extension injects script on known password reset pages. 2. It tracks input[type=password] fields labeled “new password” or “confirm password”. 3. On form submission, the script captures both the old and new passwords. 4. This allows attackers to monitor which accounts were recently changed and update their own access. 5. It’s especially useful in cases where users reset passwords after compromise.
- **Detection**: Monitor password field behavior on critical flows
- **Solution**: Use server-side confirmation and anomaly detection
- **Tags**: #passwordresetspy #formhook #mitb

## Extension Uses Browser Storage for Hidden C2 Communication

- **Attack Type**: Malicious Extension
- **Target**: Chrome-based browsers
- **Vulnerability**: Storage abuse for C2 command delivery
- **MITRE**: T1027
- **Impact**: Covert persistence & evasion
- **Tools**: Chrome Storage API, JS Obfuscator
- **Scenario**: Uses localStorage or chrome.storage to fetch & execute encoded payloads
- **Attack Steps**: 1. The extension fetches encoded command payloads from a C2 server periodically. 2. Instead of direct script injection, it stores them in localStorage or chrome.storage.local. 3. Content scripts read and evaluate these payloads at runtime. 4. Since network activity is minimal, it avoids triggering detection systems.
- **Detection**: Monitor abnormal use of storage APIs
- **Solution**: Block eval() and dynamic script execution in sensitive environments
- **Tags**: #stealthc2 #storagemisuse #extensionevade

## Fake News Reader Extension Injects Cryptojacking Script

- **Attack Type**: Malicious Extension
- **Target**: End-user browsers
- **Vulnerability**: Background mining via iframe injection
- **MITRE**: T1496
- **Impact**: Device slowdown, battery drain, abuse of hardware
- **Tools**: CoinHive JS, Chrome Task Monitor
- **Scenario**: Extension uses CPU power to mine cryptocurrency in background
- **Attack Steps**: 1. The user installs a "news aggregator" extension that loads CoinHive or other mining scripts in background. 2. On each page visit, a content script adds a hidden iframe running the mining script. 3. CPU usage spikes subtly during browsing sessions. 4. Multiple tabs result in more resource consumption. 5. User notices device slowdown but can't trace the cause.
- **Detection**: Monitor CPU usage and inspect background processes
- **Solution**: Block known cryptojacking scripts and enforce energy-aware browsing
- **Tags**: #cryptojack #extensionabuse #covertmining

## Clipboard Logger Extension in Medical Portals

- **Attack Type**: Malicious Extension
- **Target**: Medical and HR web apps
- **Vulnerability**: Clipboard event listener abuse
- **MITRE**: T1112
- **Impact**: PII exfiltration without user input
- **Tools**: Clipboard Event Logger, Regex Filters
- **Scenario**: Monitors clipboard copy-paste events in medical or HR web apps
- **Attack Steps**: 1. Extension listens to clipboard copy events on pages matching health portals. 2. It detects when users copy data matching regex like SSNs, diagnosis codes, or employee IDs. 3. This data is logged and exfiltrated to the attacker. 4. Extremely stealthy, as no UI is manipulated.
- **Detection**: Block clipboard listeners in sensitive environments
- **Solution**: Apply copy-paste event whitelists
- **Tags**: #healthspy #piileak #extensionclipboard

## Extension Disables Other Extensions for Persistence

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Browsers with multiple extensions
- **Vulnerability**: Extension-level privilege conflict
- **MITRE**: T1562.001
- **Impact**: Disable security controls via internal attack
- **Tools**: Chrome Management API
- **Scenario**: Tries to programmatically disable competing security extensions
- **Attack Steps**: 1. The attacker’s extension uses the management API to list all installed extensions. 2. It checks for known security/privacy extensions. 3. Attempts to disable them or hide from UI by modifying enable state. 4. Ensures only attacker extension remains active and unmonitored.
- **Detection**: Monitor logs of extension enable/disable actions
- **Solution**: Prevent management access unless truly needed
- **Tags**: #extensionkill #persistence #securitydisable

## Extension Renders Fake Security Warnings to Bait Clicks

- **Attack Type**: Malicious Extension
- **Target**: Any site (esp. banking, email)
- **Vulnerability**: UI redressing with false alerts
- **MITRE**: T1204.002
- **Impact**: Phishing via fake warning overlays
- **Tools**: Fake UI Panels, DOM Injection
- **Scenario**: Displays fake alerts like “Your account is at risk” to redirect users
- **Attack Steps**: 1. Extension injects a red warning banner at the top of popular sites. 2. The message urges the user to “click to verify your identity.” 3. Redirects them to phishing login or malware page. 4. The alert mimics real browser/system warnings.
- **Detection**: Inspect injected DOM overlays; use CSP header validation
- **Solution**: Educate users on trusted alert formats; limit visual modification
- **Tags**: #phishingbanner #browserfake #extensiontrap

## Extension Modifies E-Commerce Prices for Phishing

- **Attack Type**: Man-in-the-Browser (MITB)
- **Target**: Online shopping websites
- **Vulnerability**: Content manipulation via DOM injection
- **MITRE**: T1557.002
- **Impact**: Payment credential theft
- **Tools**: DOM Inspector, JavaScript Injector
- **Scenario**: Malicious extension changes product prices to lure users into fake checkout pages
- **Attack Steps**: 1. The attacker builds a browser extension claiming to offer coupons or price comparisons. 2. On visiting a shopping website, the extension injects JavaScript to alter displayed product prices (e.g., lowering expensive items). 3. When users try to purchase, the "Buy Now" button is redirected to a fake checkout page that mimics the original site. 4. Users input payment details into this fake page. 5. The credentials are harvested and sent to the attacker. 6. A fake error message appears to prevent actual payment processing, keeping users unaware. 7. Users believe the site had an issue, while data has already been stolen. 8. The extension clears local storage to remove traces of manipulation.
- **Detection**: Check DOM diff between trusted and rendered HTML
- **Solution**: Use isolated payment iFrames and domain verification
- **Tags**: #phishing #checkoutspoof #mitb

## Extension With Hidden Torrent Tracker Monitor

- **Attack Type**: Malicious Extension
- **Target**: Torrent users
- **Vulnerability**: Background port scanning via WebRTC
- **MITRE**: T1040
- **Impact**: Privacy violation & legal risk
- **Tools**: JavaScript, WebRTC Leak Detector
- **Scenario**: Browser plugin secretly monitors torrent traffic and reports back to attacker
- **Attack Steps**: 1. The extension claims to “accelerate downloads” but silently monitors torrent activity via WebRTC leaks. 2. It checks if certain ports are active or common trackers are in use. 3. On detection, it logs the file name, size, and source IP. 4. The data is encrypted and periodically uploaded to the attacker’s server. 5. Over time, the attacker builds a database of what files the user shares or downloads. 6. This info can be used for blackmail or DMCAs.
- **Detection**: Block background WebRTC use and scan for suspicious ports
- **Solution**: Disable WebRTC unless needed; monitor DNS leak tools
- **Tags**: #webrtcspy #torrenttracking #extensionleak

## Bookmark-Based Persistence via Extension

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Browser bookmarks
- **Vulnerability**: Persistent payload injection via bookmarklets
- **MITRE**: T1053.005
- **Impact**: Post-uninstall attack continuation
- **Tools**: Chrome API, Bookmarklet Injector
- **Scenario**: Extension adds malicious bookmarklets that can execute code on demand
- **Attack Steps**: 1. A malicious extension quietly adds several hidden bookmarklets to the user's bookmarks folder. 2. These bookmarklets contain JavaScript payloads that run when clicked. 3. Even if the extension is removed, the bookmarklets persist. 4. When clicked by accident or on purpose, these can reinject backdoors or redirect to attacker-controlled pages. 5. Bookmarks often go unchecked, making it an overlooked persistence method.
- **Detection**: Monitor bookmark creation events in extensions
- **Solution**: Block JS-based bookmarklets in corporate environments
- **Tags**: #bookmarkbackdoor #persistence #extensionabuse

## Fake Extension Auto-Adds Proxy Settings

- **Attack Type**: Malicious Extension
- **Target**: General browser users
- **Vulnerability**: Proxy hijack via extension config
- **MITRE**: T1557.001
- **Impact**: MITM via browser-level proxy
- **Tools**: ProxySwitch API, Chrome DevTools
- **Scenario**: Extension silently sets proxy config to redirect traffic through attacker server
- **Attack Steps**: 1. An extension requests proxy permission and silently sets a custom proxy route. 2. All browser traffic is now routed through the attacker’s controlled server. 3. The attacker inspects and logs all HTTP(S) requests, even modifying responses. 4. The user experiences only slightly slower browsing and remains unaware. 5. This allows full MITM interception of unencrypted traffic and metadata leakage from HTTPS.
- **Detection**: Monitor system proxy settings & browser overrides
- **Solution**: Block proxy configuration unless explicitly needed
- **Tags**: #proxyabuse #browsermitm #trafficintercept

## Extension Tracks Password Resets and Logs New Passwords

- **Attack Type**: Man-in-the-Browser (MITB)
- **Target**: Password reset flows
- **Vulnerability**: DOM interception of password change forms
- **MITRE**: T1056.001
- **Impact**: Persistent account access after recovery
- **Tools**: JavaScript DOM Hooks, Event Listener Tracker
- **Scenario**: Hooks password reset forms and logs newly set passwords silently
- **Attack Steps**: 1. Extension injects script on known password reset pages. 2. It tracks input[type=password] fields labeled “new password” or “confirm password”. 3. On form submission, the script captures both the old and new passwords. 4. This allows attackers to monitor which accounts were recently changed and update their own access. 5. It’s especially useful in cases where users reset passwords after compromise.
- **Detection**: Monitor password field behavior on critical flows
- **Solution**: Use server-side confirmation and anomaly detection
- **Tags**: #passwordresetspy #formhook #mitb

## Extension Uses Browser Storage for Hidden C2 Communication

- **Attack Type**: Malicious Extension
- **Target**: Chrome-based browsers
- **Vulnerability**: Storage abuse for C2 command delivery
- **MITRE**: T1027
- **Impact**: Covert persistence & evasion
- **Tools**: Chrome Storage API, JS Obfuscator
- **Scenario**: Uses localStorage or chrome.storage to fetch & execute encoded payloads
- **Attack Steps**: 1. The extension fetches encoded command payloads from a C2 server periodically. 2. Instead of direct script injection, it stores them in localStorage or chrome.storage.local. 3. Content scripts read and evaluate these payloads at runtime. 4. Since network activity is minimal, it avoids triggering detection systems.
- **Detection**: Monitor abnormal use of storage APIs
- **Solution**: Block eval() and dynamic script execution in sensitive environments
- **Tags**: #stealthc2 #storagemisuse #extensionevade

## Fake News Reader Extension Injects Cryptojacking Script

- **Attack Type**: Malicious Extension
- **Target**: End-user browsers
- **Vulnerability**: Background mining via iframe injection
- **MITRE**: T1496
- **Impact**: Device slowdown, battery drain, abuse of hardware
- **Tools**: CoinHive JS, Chrome Task Monitor
- **Scenario**: Extension uses CPU power to mine cryptocurrency in background
- **Attack Steps**: 1. The user installs a "news aggregator" extension that loads CoinHive or other mining scripts in background. 2. On each page visit, a content script adds a hidden iframe running the mining script. 3. CPU usage spikes subtly during browsing sessions. 4. Multiple tabs result in more resource consumption. 5. User notices device slowdown but can't trace the cause.
- **Detection**: Monitor CPU usage and inspect background processes
- **Solution**: Block known cryptojacking scripts and enforce energy-aware browsing
- **Tags**: #cryptojack #extensionabuse #covertmining

## Clipboard Logger Extension in Medical Portals

- **Attack Type**: Malicious Extension
- **Target**: Medical and HR web apps
- **Vulnerability**: Clipboard event listener abuse
- **MITRE**: T1112
- **Impact**: PII exfiltration without user input
- **Tools**: Clipboard Event Logger, Regex Filters
- **Scenario**: Monitors clipboard copy-paste events in medical or HR web apps
- **Attack Steps**: 1. Extension listens to clipboard copy events on pages matching health portals. 2. It detects when users copy data matching regex like SSNs, diagnosis codes, or employee IDs. 3. This data is logged and exfiltrated to the attacker. 4. Extremely stealthy, as no UI is manipulated.
- **Detection**: Block clipboard listeners in sensitive environments
- **Solution**: Apply copy-paste event whitelists
- **Tags**: #healthspy #piileak #extensionclipboard

## Extension Disables Other Extensions for Persistence

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Browsers with multiple extensions
- **Vulnerability**: Extension-level privilege conflict
- **MITRE**: T1562.001
- **Impact**: Disable security controls via internal attack
- **Tools**: Chrome Management API
- **Scenario**: Tries to programmatically disable competing security extensions
- **Attack Steps**: 1. The attacker’s extension uses the management API to list all installed extensions. 2. It checks for known security/privacy extensions. 3. Attempts to disable them or hide from UI by modifying enable state. 4. Ensures only attacker extension remains active and unmonitored.
- **Detection**: Monitor logs of extension enable/disable actions
- **Solution**: Prevent management access unless truly needed
- **Tags**: #extensionkill #persistence #securitydisable

## Extension Renders Fake Security Warnings to Bait Clicks

- **Attack Type**: Malicious Extension
- **Target**: Any site (esp. banking, email)
- **Vulnerability**: UI redressing with false alerts
- **MITRE**: T1204.002
- **Impact**: Phishing via fake warning overlays
- **Tools**: Fake UI Panels, DOM Injection
- **Scenario**: Displays fake alerts like “Your account is at risk” to redirect users
- **Attack Steps**: 1. Extension injects a red warning banner at the top of popular sites. 2. The message urges the user to “click to verify your identity.” 3. Redirects them to phishing login or malware page. 4. The alert mimics real browser/system warnings.
- **Detection**: Inspect injected DOM overlays; use CSP header validation
- **Solution**: Educate users on trusted alert formats; limit visual modification
- **Tags**: #phishingbanner #browserfake #extensiontrap

## Extension Spoofs 2FA Prompt for Token Harvesting

- **Attack Type**: Man-in-the-Browser (MITB)
- **Target**: Banking and email platforms
- **Vulnerability**: UI spoofing of authentication flows
- **MITRE**: T1110.002
- **Impact**: Bypass of MFA protections
- **Tools**: DOM Cloner, JS Hooker
- **Scenario**: Fakes browser-based 2FA prompt to capture OTPs before real submission
- **Attack Steps**: 1. The attacker designs an extension that activates only on banking or email websites. 2. Once login is detected, the extension instantly overlays a fake 2FA prompt using a modal popup. 3. The user, believing it's from the original site, enters their OTP or token into this prompt. 4. The extension intercepts and stores the OTP. 5. Immediately, the real login page is triggered in the background using the correct credentials and OTP. 6. This allows the attacker to piggyback into the user session undetected. 7. It also disables subsequent OTP prompts, ensuring one-time access. 8. The user is redirected normally, believing the process was legitimate.
- **Detection**: Monitor for overlay injections and modal rendering
- **Solution**: Enforce WebAuthn or hardware-based MFA
- **Tags**: #2faspam #otpsteal #mitb

## Extension Records Voice via Permissions Abuse

- **Attack Type**: Malicious Extension
- **Target**: Remote workers, enterprise users
- **Vulnerability**: Misuse of browser microphone APIs
- **MITRE**: T1123
- **Impact**: Voice surveillance and privacy breach
- **Tools**: WebRTC, Speech-to-Text API
- **Scenario**: Misuses granted microphone access to record conversations from browser tabs
- **Attack Steps**: 1. An extension offers a “voice note” feature and requests microphone permissions. 2. After install, it continuously records audio in browser background without alerting the user. 3. The audio is streamed to a cloud server, where speech-to-text APIs transcribe it. 4. This data can contain sensitive meetings, conversations, or passwords spoken aloud. 5. Since the extension operates inside the browser, it avoids OS-level recording alerts. 6. Users believe mic access is used only when actively recording — not passively. 7. Long-form conversations may be indexed and stored indefinitely. 8. All of this happens while the extension appears idle.
- **Detection**: Monitor mic usage per tab and alert on continuous access
- **Solution**: Prompt user on every audio start or set time limits
- **Tags**: #voiceabuse #micspy #extensionleak

## Extension Injects Keylogger on Cloud IDE Platforms

- **Attack Type**: Malicious Extension
- **Target**: Developers using cloud IDEs
- **Vulnerability**: Input hijack inside embedded editors
- **MITRE**: T1056.001
- **Impact**: Credential and intellectual property theft
- **Tools**: Keypress JS, DOM Hooks
- **Scenario**: Steals code, API tokens, and credentials by logging keystrokes in online IDEs
- **Attack Steps**: 1. A developer utility extension is promoted as a productivity tool for coders. 2. When users visit cloud IDEs like Replit, GitHub Codespaces, or JSFiddle, the extension injects listeners. 3. These listeners track every keystroke typed in the code editor and console windows. 4. This includes environment variables, hardcoded secrets, and access tokens. 5. Captured data is base64 encoded and sent to the attacker server at regular intervals. 6. The extension hides this behavior inside innocuous scripts or obfuscated payloads. 7. Developers lose credentials and codebase access silently. 8. The extension may also record clipboard copy events.
- **Detection**: Monitor outbound network traffic from extensions
- **Solution**: Use endpoint hardening to block external script injection
- **Tags**: #devkeylogger #idehijack #extensionbackdoor

## Extension Adds Phishing Overlays to Webmail

- **Attack Type**: Man-in-the-Browser (MITB)
- **Target**: Webmail portals
- **Vulnerability**: Fake alerts inserted above legitimate UI
- **MITRE**: T1204.002
- **Impact**: Credential theft via impersonated warnings
- **Tools**: DOM Modifier, Fake Alerts
- **Scenario**: Places fake "password expired" banners in Gmail/Outlook to collect passwords
- **Attack Steps**: 1. A browser extension advertised as a theme customizer for email services is installed. 2. When users access Gmail or Outlook, a red alert banner is injected via the DOM. 3. It says “Your password has expired — click here to reset.” 4. Clicking the link takes users to a phishing page mimicking the email provider’s reset flow. 5. Entered passwords are logged and used for further access. 6. The phishing banner is styled to look like a native Gmail warning, including fonts and iconography. 7. Once data is harvested, the banner disappears. 8. The extension deletes its own logs and clears console messages.
- **Detection**: Compare DOM trees with known baseline; detect new banners
- **Solution**: Educate users on official reset protocols and UI format
- **Tags**: #webmailphish #alertspoof #mitb

## Extension Monitors Browser History for Reconnaissance

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Any browser user
- **Vulnerability**: Surveillance via browsing history APIs
- **MITRE**: T1087.001
- **Impact**: Behavioral profiling and reconnaissance
- **Tools**: chrome.history API, JSON Logger
- **Scenario**: Reads and logs all URLs visited, mapping user behavior and platform use
- **Attack Steps**: 1. A browser extension marketed as a "productivity tracker" is downloaded by users. 2. It requests access to the chrome.history API. 3. The extension silently logs all URLs visited over time. 4. It tags them by domain category — banking, coding, health, social media, etc. 5. These logs are exfiltrated and used to build user profiles or blackmail materials. 6. In advanced cases, this data is cross-referenced with cookies and browser tabs to detect logins. 7. Over time, full user behavior is reconstructed. 8. This information can be sold or used for targeted phishing.
- **Detection**: Audit extension permissions regularly; check domain targets
- **Solution**: Restrict access to history APIs unless critical
- **Tags**: #historyleak #reconabuse #extensionspy

## Extension Auto-Injects Ads Into Social Media Feeds

- **Attack Type**: Malicious Extension
- **Target**: Social media users
- **Vulnerability**: Feed rewriting to insert malicious ads
- **MITRE**: T1566.002
- **Impact**: Scams, malware, and click fraud
- **Tools**: Ad Rewriter, CSS Injection
- **Scenario**: Modifies Twitter/Instagram feeds to include promoted content from attackers
- **Attack Steps**: 1. A “Feed Cleaner” extension claims to remove ads and trends from social media. 2. Instead, it rewrites the DOM of Twitter/Instagram feeds and injects new “promoted” posts. 3. These posts look native, mimicking font and post structure. 4. The promoted links lead to scam sites, crypto frauds, or malware downloaders. 5. The extension tracks which injected posts were clicked for analytics. 6. Over time, it adapts to user preferences to push more targeted scams. 7. Users believe it’s part of the official platform feed. 8. Monetization happens via affiliate fraud or malware installs.
- **Detection**: Detect DOM rewrites in authenticated feeds
- **Solution**: Use CSP and client-side integrity checks
- **Tags**: #adinject #scamlink #socialspoof

## Extension Locks Browser Tab and Renders Ransom Message

- **Attack Type**: Malicious Extension
- **Target**: Any user visiting arbitrary site
- **Vulnerability**: Abuse of fullscreen and modal APIs
- **MITRE**: T1499
- **Impact**: Browser-level ransomware attack
- **Tools**: Fullscreen JS, Modal Loops
- **Scenario**: Uses fullscreen API and modal loop to trap user until ransom is paid
- **Attack Steps**: 1. A seemingly harmless extension is installed for UI tweaks. 2. Once triggered, it redirects the tab to a ransom page, requests fullscreen access, and disables escape keys. 3. Using modal loops and keyboard event trapping, the user can’t close or navigate away. 4. The screen shows a ransom message — “Your browser is locked. Pay to unlock.” 5. It may simulate webcam access or display fake “law enforcement” notices. 6. Even closing and reopening the browser restores the locked tab via session restore. 7. Only clearing browser profile or using recovery flags breaks the loop. 8. The ransom may be demanded in cryptocurrency with a short countdown timer.
- **Detection**: Watch for fullscreen + modal trap combo
- **Solution**: Disable fullscreen auto-approve and modal chaining
- **Tags**: #browserveransom #tablock #extensionransom

## Extension Modifies Online Exam Submissions

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Online exam systems
- **Vulnerability**: Pre-submission data injection
- **MITRE**: T1565.001
- **Impact**: Academic fraud and unauthorized test manipulation
- **Tools**: JS Event Hijack, Mutation Observers
- **Scenario**: Tamper with form data before submission in academic platforms
- **Attack Steps**: 1. An academic “exam helper” extension is installed before an online test. 2. As the user fills out exam answers in textboxes and radio buttons, the extension monitors input changes. 3. Before submission, it replaces certain answers with pre-fed ones or alters scores subtly. 4. This is done just before the final submission, so the user doesn’t notice. 5. On the server side, tampered answers are accepted. 6. The extension hides mutation observers to avoid debugging exposure. 7. It can be updated remotely to adapt to new exam platforms. 8. Schools or platforms are unaware unless comparing raw vs. submitted data.
- **Detection**: Hash answers pre-submission; compare on server-side
- **Solution**: Lock down browser environment with proctoring tools
- **Tags**: #examhack #formtamper #extensionexploit

## Extension Steals Crypto Wallet Seed Phrases

- **Attack Type**: Malicious Extension
- **Target**: Crypto users
- **Vulnerability**: Mnemonic phrase detection and theft
- **MITRE**: T1552.001
- **Impact**: Total crypto asset loss
- **Tools**: Regex Matchers, Clipboard Hooks
- **Scenario**: Watches for mnemonic/seed phrase patterns and stores them
- **Attack Steps**: 1. A crypto-themed extension offers “wallet management features.” 2. It hooks into clipboard and input fields using regex to detect 12 or 24-word seed phrases. 3. These are logged silently and sent to the attacker's cold storage. 4. On detection of a valid phrase, it triggers an alert to immediately empty the wallet. 5. The extension may fake a wallet backup operation to trick users into pasting their phrase. 6. It deletes logs and obfuscates network activity via data chunks. 7. Victims often lose funds without even realizing where the leak occurred. 8. High-value targets may be prioritized via balance-check APIs.
- **Detection**: Detect clipboard pattern sniffing in extension JS
- **Solution**: Use hardware wallets; never paste seeds online
- **Tags**: #walletsteal #seedlogger #cryptoextension

## Extension Spoofs Extension Removal Dialog to Persist

- **Attack Type**: Privilege Escalation via Extension APIs
- **Target**: Browser extensions page
- **Vulnerability**: Fake UI to prevent removal
- **MITRE**: T1546.001
- **Impact**: Extension persistence through deception
- **Tools**: Fake Modal, Uninstall Hook
- **Scenario**: Overrides the uninstall dialog to scare or confuse users
- **Attack Steps**: 1. A persistent extension overrides the native removal process by intercepting the uninstall click. 2. It renders a fake warning: “Uninstalling may damage your browser.” 3. The dialog includes misleading buttons like “Cancel” or “Keep Safe Mode.” 4. It may trigger multiple popups to frustrate removal attempts. 5. Logs are faked to show the extension is essential to browser security. 6. In some versions, uninstall is silently blocked via JavaScript event handlers. 7. Only through safe mode or manual extension removal is it stopped. 8. This allows the extension to persist longer and continue its malicious actions.
- **Detection**: Check for JS override on uninstall flows
- **Solution**: Use enterprise policies to lock down extensions
- **Tags**: #uninstallspoof #extensionpersist #removalabuse

