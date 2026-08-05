# Browser Security → SOP (Same-Origin Policy) Bypass Attacks

## Exploiting Trust with PostMessage in OAuth Flow

- **Attack Type**: PostMessage Exploitation
- **Target**: OAuth-Integrated Web Apps
- **Vulnerability**: Lack of origin check in postMessage
- **MITRE**: T1557.001
- **Impact**: Account takeover via stolen token
- **Tools**: JavaScript, Burp Suite
- **Scenario**: Attacker sends malicious postMessage from iframe to parent OAuth login window, capturing tokens
- **Attack Steps**: 1. Attacker builds a phishing page that embeds the real OAuth provider (e.g., Google Sign-In) in an iframe. 2. The phishing site listens for postMessage events from the iframe. 3. The legitimate OAuth page sends a postMessage event after authentication (like access_token or code). 4. The attacker’s script captures that message if the OAuth flow doesn't validate message origin. 5. Token is stolen without the user realizing. 6. Attacker uses it to impersonate victim on downstream apps.
- **Detection**: Use CSP and verify event.origin before processing
- **Solution**: Always validate origin and source in postMessage
- **Tags**: #postmessage #oauth #tokenhijack

## Abusing Wildcard CORS on API to Steal User Data

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Web APIs with auth
- **Vulnerability**: Overly permissive CORS with credentials
- **MITRE**: T1190
- **Impact**: Sensitive data theft
- **Tools**: Burp Suite, curl
- **Scenario**: Attacker reads sensitive API data because Access-Control-Allow-Origin: * is used with credentials
- **Attack Steps**: 1. A web app hosts an internal API endpoint (e.g., /api/profile). 2. The server has Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true in response headers. 3. Attacker lures user to malicious site and uses JavaScript to make a fetch() call to /api/profile from the victim’s browser. 4. Because of the bad CORS policy, the browser sends cookies, and the attacker’s JS reads the JSON response. 5. User’s profile data (email, tokens, etc.) is leaked cross-origin.
- **Detection**: Analyze CORS headers with tools like CORS Misconfig Scanner
- **Solution**: Never use * with Access-Control-Allow-Credentials
- **Tags**: #cors #dataleak #crossorigin

## Subdomain Takeover to Inject Malicious Scripts

- **Attack Type**: Subdomain Takeover
- **Target**: Enterprises with many subdomains
- **Vulnerability**: Orphaned DNS records for subdomains
- **MITRE**: T1584.005
- **Impact**: Full site compromise, internal data access
- **Tools**: GitHub Pages, DNS, Amass
- **Scenario**: Unused subdomain pointing to GitHub Pages allows attacker to inject JS and bypass SOP
- **Attack Steps**: 1. Organization has a subdomain like dev.site.com pointing to GitHub Pages but no content. 2. Attacker finds the domain unclaimed and registers a GitHub repo with same name. 3. Because DNS still points to GitHub Pages, attacker now controls dev.site.com. 4. They host malicious scripts there that get trusted as same-origin by site.com. 5. Scripts access cookies, localStorage, or perform DOM injection via shared trust.
- **Detection**: Monitor for dangling subdomains via automated scanners
- **Solution**: Remove or update unused DNS entries
- **Tags**: #subdomaintakeover #dns #trustabuse

## Reading Cross-Site Webmail Using CORS Misconfig

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Webmail Users
- **Vulnerability**: Unrestricted cross-origin read
- **MITRE**: T1557.002
- **Impact**: Private communication leak
- **Tools**: curl, Burp Suite, XSStrike
- **Scenario**: Email client leaks inbox content due to CORS allowing any origin
- **Attack Steps**: 1. A web-based mail client (webmail.example.com) offers an inbox API endpoint. 2. The server incorrectly allows Access-Control-Allow-Origin: * for all endpoints. 3. Attacker lures user to a malicious site. 4. JavaScript on the attacker's site sends XMLHttpRequest to inbox API. 5. With cookies automatically sent, response containing emails is leaked to attacker.
- **Detection**: Use dynamic origin whitelisting and audit CORS
- **Solution**: Validate CORS headers don’t leak sensitive routes
- **Tags**: #webmailhack #corsleak #emailtheft

## Stealing JWT Tokens via Iframe PostMessage Trap

- **Attack Type**: PostMessage Exploitation
- **Target**: Authenticated Web Apps
- **Vulnerability**: Unvalidated postMessage source
- **MITRE**: T1557.001
- **Impact**: Account session hijack
- **Tools**: JavaScript, iframe, Token Sniffer
- **Scenario**: Attacker embeds trusted app in iframe and steals auth token from message event
- **Attack Steps**: 1. Attacker sets up a malicious site that loads app.trusted.com in an iframe. 2. Victim is logged into the trusted app and the iframe loads with session. 3. App inside iframe uses postMessage to send token to parent window (for cross-tab auth). 4. Malicious parent window captures message without validating source. 5. Token is used by attacker to log in as victim. 6. No alert or visual cue given to user.
- **Detection**: Inspect message handlers for origin validation
- **Solution**: Restrict postMessage to known origins only
- **Tags**: #tokensteal #iframe #postmessageabuse

## Subdomain Hijack for Cookie Harvesting

- **Attack Type**: Subdomain Takeover
- **Target**: Large orgs with abandoned subdomains
- **Vulnerability**: Unclaimed assets under primary domain
- **MITRE**: T1584
- **Impact**: Cookie theft, session impersonation
- **Tools**: DNSDumpster, Hostile HTML
- **Scenario**: Controlled subdomain reads cookies and localStorage via shared origin
- **Attack Steps**: 1. An old marketing subdomain promo.site.com is unused but still resolves. 2. Attacker claims it via Netlify or S3. 3. They host a script that reads cookies/localStorage assuming shared origin with site.com. 4. Because both share *.site.com, some cookies may have Domain=.site.com and be accessible. 5. Data is sent to attacker server for session theft.
- **Detection**: Scan for unclaimed CNAMEs or buckets
- **Solution**: Set cookie flags: Secure, HttpOnly, avoid wide-domain cookies
- **Tags**: #sessiontheft #cookiesteal #subdomainrisk

## Cross-Site Script Injection via JSONP & CORS

- **Attack Type**: JSONP + Misconfigured CORS
- **Target**: APIs using JSONP
- **Vulnerability**: Cross-site data leakage + code execution
- **MITRE**: T1190
- **Impact**: XSS + SOP bypass combo
- **Tools**: Burp Suite, Chrome DevTools
- **Scenario**: Legacy API supports JSONP, attacker abuses it for cross-site injection
- **Attack Steps**: 1. A legacy API provides JSONP responses (e.g., /data?callback=cb). 2. Attacker crafts URL with custom callback and embeds malicious JavaScript in response. 3. Because CORS allows *, the attacker can make this request from any domain. 4. The response is parsed and executed as JS in attacker’s site, bypassing SOP. 5. Victim’s browser runs script in context of trusted site.
- **Detection**: Remove JSONP support unless absolutely needed
- **Solution**: Use CORS + CSP strictly
- **Tags**: #jsonp #corsmisconfig #xss

## Trusted Widget Loads Malicious Data from Attacker Subdomain

- **Attack Type**: Subdomain Takeover
- **Target**: Sites using legacy assets
- **Vulnerability**: Insecure dependency from abandoned subdomain
- **MITRE**: T1195.002
- **Impact**: Full DOM compromise
- **Tools**: JS, Subdomain Scanner
- **Scenario**: Embedded analytics widget loads JS from compromised subdomain
- **Attack Steps**: 1. Trusted app loads <script src="static.site.com/widget.js">. 2. static.site.com was once used, now unclaimed. 3. Attacker registers and uploads malicious widget JS. 4. On page load, it runs with same privileges as main site. 5. Can modify DOM, steal tokens, send phishing popups.
- **Detection**: Monitor third-party JS origins, use integrity hashes
- **Solution**: Remove stale references to third-party domains
- **Tags**: #supplychain #subdomaintakeover #widgetattack

## Silent Data Harvesting with Misconfigured Preflight

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Cross-Origin APIs
- **Vulnerability**: Permissive preflight headers + credential sharing
- **MITRE**: T1189
- **Impact**: PII exposure
- **Tools**: HTTP, DevTools
- **Scenario**: API allows OPTIONS preflight from any origin with sensitive GET data
- **Attack Steps**: 1. API endpoint returns sensitive data on GET /userinfo. 2. Preflight requests (OPTIONS) are loosely configured. 3. Attacker sets custom headers (X-Auth) and sends cross-origin request. 4. Browser incorrectly allows it due to Access-Control-Allow-Headers: *. 5. Victim’s browser sends cookies, attacker reads response.
- **Detection**: Restrict headers and allowed methods
- **Solution**: Do not allow wildcard in sensitive endpoints
- **Tags**: #corspreflight #databreach #headerleak

## Capturing Sensitive Messages from Embedded Iframe

- **Attack Type**: PostMessage Exploitation
- **Target**: SaaS Embedded Widgets
- **Vulnerability**: Unrestricted data exposure via iframe messaging
- **MITRE**: T1557.001
- **Impact**: Session hijack or impersonation
- **Tools**: iframe, JS
- **Scenario**: Iframe sends postMessage with session info to attacker-controlled parent
- **Attack Steps**: 1. A third-party app embeds a widget (e.g., calendar) via iframe. 2. Widget sends session data to parent using postMessage. 3. Attacker sets up malicious parent frame that loads the widget. 4. It captures the postMessage and logs sensitive info (user ID, tokens). 5. Because widget doesn’t check targetOrigin, data is leaked to attacker.
- **Detection**: Always set targetOrigin in postMessage
- **Solution**: Use message signing or auth handshake
- **Tags**: #iframeleak #postmessage #sessionexfil

## Stealing Auth Data via Insecure PostMessage in Single Page App

- **Attack Type**: PostMessage Exploitation
- **Target**: Single Page Applications
- **Vulnerability**: Lack of origin validation in postMessage
- **MITRE**: T1557.001
- **Impact**: Unauthorized access to session/token
- **Tools**: Browser DevTools, Burp Suite
- **Scenario**: SPA app transmits user token via postMessage without origin validation
- **Attack Steps**: 1. A modern single-page application (SPA) uses a child iframe to perform token-based authentication. 2. Once the iframe loads and authentication completes, it sends a postMessage event to the parent window to share the session token (e.g., JWT). 3. Unfortunately, the SPA does not validate the event.origin in the message listener, so any origin is accepted. 4. An attacker hosts a malicious parent page and embeds the original SPA iframe. 5. After a successful login inside the iframe, the iframe sends a postMessage containing the token to the parent, assuming it’s the original app. 6. The attacker’s malicious parent captures the token and logs it. 7. They use this token to impersonate the user on the real application, gaining access to personal dashboards, data, or initiating actions on behalf of the victim.
- **Detection**: Monitor message events, check event.origin, event.source
- **Solution**: Always validate origin and source of messages explicitly
- **Tags**: #spa #postmessage #sessionhijack

## Exploiting Overly Permissive CORS on Sensitive Banking API

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Banking Sites / APIs
- **Vulnerability**: Wildcard CORS with credentials allowed
- **MITRE**: T1190
- **Impact**: Exposure of financial and personal data
- **Tools**: curl, Postman, XSStrike
- **Scenario**: Banking site allows all origins and exposes user data via API
- **Attack Steps**: 1. A banking website has a backend endpoint /api/account-details that returns sensitive user information like account numbers, balance, and personal details. 2. This endpoint is meant to be used only by the official web frontend, but its CORS policy allows Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true. 3. An attacker creates a malicious web page that silently runs JavaScript on a victim’s browser. 4. When the victim (already logged in) visits the attacker’s site, the script sends a fetch() request to the banking API. 5. Because the CORS policy is too permissive, the browser sends cookies/session tokens and receives the full JSON response. 6. The attacker reads the response and logs the victim’s financial information without ever needing to break into their account directly.
- **Detection**: CORS scanner, browser devtools
- **Solution**: Never combine Access-Control-Allow-Origin: * with credentials, use strict whitelisting
- **Tags**: #cors #bankingbreach #apiinsecure

## Hijacking Abandoned Subdomain to Inject Scripts on Main App

- **Attack Type**: Subdomain Takeover
- **Target**: Corporate Web Apps
- **Vulnerability**: DNS record points to unclaimed resource
- **MITRE**: T1584.005
- **Impact**: Full site compromise via same-origin trust
- **Tools**: DNSDumpster, GitHub Pages, Amass
- **Scenario**: An unused dev subdomain is hijacked and used to inject scripts
- **Attack Steps**: 1. A company previously used dev.company.com for staging, hosted via GitHub Pages. 2. The DNS CNAME still points to GitHub Pages, but the GitHub repository has been deleted. 3. An attacker discovers this unclaimed subdomain using a reconnaissance tool like Amass. 4. They create a GitHub repo named dev.company.com and GitHub Pages activates. 5. Now, dev.company.com is serving content from attacker’s GitHub page. 6. The attacker hosts JavaScript that calls APIs on company.com, which treats it as same-origin due to SOP trust. 7. Cookies, localStorage, and tokens scoped to *.company.com may be accessible from the malicious subdomain. 8. This enables full takeover, script injection, and privilege escalation via script chaining.
- **Detection**: Regularly audit DNS and hosting configurations
- **Solution**: Remove stale subdomains or use wildcard DNS sinkholes
- **Tags**: #subdomaintakeover #dns #trustbypass

## Harvesting Medical Records via Misconfigured CORS on Health Portal

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Healthcare Web Portals
- **Vulnerability**: Sensitive data exposed via CORS
- **MITRE**: T1189
- **Impact**: Privacy violations, HIPAA breach
- **Tools**: XSStrike, curl, HTTP Toolkit
- **Scenario**: Health portal exposes patient data to cross-origin scripts
- **Attack Steps**: 1. A health services platform provides lab results via an internal API endpoint (/api/lab-results). 2. Its CORS policy includes Access-Control-Allow-Origin: * without proper preflight validation. 3. An attacker’s page silently runs a JavaScript fetch() to the endpoint when a logged-in user visits. 4. Because session cookies are sent and response is accessible due to CORS, the attacker steals confidential health records. 5. This could include test results, prescriptions, and even diagnoses — violating HIPAA and patient privacy. 6. Users remain unaware as no visual indicators are shown.
- **Detection**: CORS security scanners, manual curl tests
- **Solution**: Strictly scope CORS origin per endpoint; no wildcard usage on sensitive data
- **Tags**: #healthdataleak #corsmisconfig #privacybreach

## Bypassing SOP with Open Redirect and Message Passing

- **Attack Type**: PostMessage Exploitation
- **Target**: Web Apps with Messaging + Redirects
- **Vulnerability**: Poor validation of postMessage + redirects
- **MITRE**: T1557.001
- **Impact**: Logic manipulation, token injection
- **Tools**: JavaScript, Redirect Inspector
- **Scenario**: Chained redirect + postMessage trick fools web app into trusting malicious tab
- **Attack Steps**: 1. Attacker discovers that a website uses window.postMessage in combination with open redirects. 2. They find a link like app.com/redirect?target=https://malicious.com which doesn’t validate destinations. 3. Victim clicks a link to app.com, gets redirected to malicious.com which is now loaded in the same tab. 4. The malicious page sends a postMessage back to the parent app with fake “login success” or token. 5. Because the receiving page (e.g., dashboard) only checks for message content, not origin, it accepts the data. 6. Attacker now controls session context or is able to inject scripts/data into the app flow.
- **Detection**: Validate postMessage sender AND sanitize redirect URLs
- **Solution**: Always use allowlist + cryptographic message signing
- **Tags**: #redirectchain #postmessage #originconfusion

## Cookie Theft via Wildcard Domain Trust in Subdomain

- **Attack Type**: Subdomain Takeover
- **Target**: E-commerce Sites
- **Vulnerability**: Wildcard cookie scope + subdomain exposure
- **MITRE**: T1557
- **Impact**: Session hijacking, cart manipulation
- **Tools**: DNS tools, Browser DevTools
- **Scenario**: Cookies with Domain=.example.com leaked via hijacked subdomain
- **Attack Steps**: 1. shop.example.com is a forgotten subdomain previously used for promotions. 2. Still resolves via DNS but the app is gone. 3. Attacker claims the domain via Netlify or similar and hosts a script that reads document.cookie. 4. Because cookies are set with Domain=.example.com, the attacker-controlled subdomain receives them. 5. These may include session tokens, CSRF secrets, and user data. 6. Attacker uses this to impersonate users across the real site.
- **Detection**: Set cookies with SameSite=Strict and avoid broad domain scope
- **Solution**: Periodic DNS + cookie audits
- **Tags**: #cookiehijack #subdomainrisk #samesitefix

## Abuse of Malicious iframe with Auto-Reply Listener

- **Attack Type**: PostMessage Exploitation
- **Target**: Online Payment Portals
- **Vulnerability**: Trusting reply postMessage without verifying origin
- **MITRE**: T1557.001
- **Impact**: Fake identity, session injection
- **Tools**: JS, iframe, Burp Suite
- **Scenario**: Malicious iframe responds to trusted postMessage sender with forged credentials
- **Attack Steps**: 1. Trusted site loads a payment widget in an iframe. 2. This widget sends a postMessage asking for authentication. 3. Malicious iframe intercepts this and sends a fake response containing attacker-controlled credentials. 4. The main page accepts the fake data assuming it's from the legit widget. 5. Attacker then uses the session or injected data to bypass validations.
- **Detection**: Add strict origin checks and message signing
- **Solution**: Never assume iframe source by content alone
- **Tags**: #widgetspoof #paymentbypass #postmessageexploit

## Exfiltrating Internal Docs via CORS Misconfig + Blob URLs

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Internal Document Systems
- **Vulnerability**: CORS on blob files, unrestricted access
- **MITRE**: T1189
- **Impact**: Data theft, internal leakage
- **Tools**: Chrome DevTools, Burp Suite
- **Scenario**: Blob URLs leaked via CORS misconfigured internal docs viewer
- **Attack Steps**: 1. Internal company wiki serves files via a document viewer app. 2. CORS allows all origins, and files are loaded using Blob URLs. 3. Attacker’s page embeds iframe to internal viewer. 4. JavaScript extracts blob URL, fetches content via XHR thanks to wildcard CORS. 5. Internal sensitive documents are silently leaked outside.
- **Detection**: Block blob URL access from external origins
- **Solution**: Harden viewer app with origin checks
- **Tags**: #corsleak #blobexfil #internaldocs

## SOP Confusion Attack via Alias Domain

- **Attack Type**: DNS-Based SOP Confusion
- **Target**: Multi-domain Sites
- **Vulnerability**: DNS aliasing not segmented
- **MITRE**: T1584
- **Impact**: Full SOP bypass and impersonation
- **Tools**: DNS tools, DevTools
- **Scenario**: Alias domain tricks browser into treating attacker as same-origin
- **Attack Steps**: 1. Attacker registers mirror.example.com, which resolves to same IP as app.example.com. 2. DNS-based same-origin assumptions allow attacker’s site to access content as if from original app. 3. With loose CORS or cookie settings, attacker performs requests and steals data.
- **Detection**: Use hostname checks at server-side, not just origin
- **Solution**: Harden cookies with origin scoping
- **Tags**: #dnsalias #sopconfusion #originabuse

## Misconfigured CDN Cache Leads to SOP Abuse

- **Attack Type**: Subdomain Takeover
- **Target**: High-Traffic Sites
- **Vulnerability**: Stale CDN alias allows JS injection
- **MITRE**: T1190
- **Impact**: Client-side takeover, persistent threat
- **Tools**: CDN tools, S3 buckets
- **Scenario**: CDN cached scripts load attacker’s JS due to stale origin trust
- **Attack Steps**: 1. A site uses CDN to cache scripts from cdn.example.com. 2. cdn.example.com is no longer managed but still active. 3. Attacker hosts JS on old endpoint, and browsers treat it as trusted origin. 4. Scripts access parent domain’s APIs and manipulate DOM/data. 5. All content is cached and loaded without suspicion.
- **Detection**: Regular audit of CDN configs and assets
- **Solution**: Use Subresource Integrity (SRI) and Content-Security-Policy
- **Tags**: #cdninject #stalescript #trustbypass

## Stealing Tokens via Insecure postMessage from OAuth Popup

- **Attack Type**: PostMessage Exploitation
- **Target**: OAuth-enabled Single Page Applications
- **Vulnerability**: Lack of origin/source validation in postMessage
- **MITRE**: T1557.001
- **Impact**: Session token theft and unauthorized access
- **Tools**: Chrome DevTools, JavaScript Console
- **Scenario**: OAuth login popup uses postMessage to send tokens back to the main window, but origin is not validated
- **Attack Steps**: 1. The attacker identifies a web app that allows users to log in using Google OAuth. 2. The login process involves a popup window where the user authenticates. After successful login, the popup uses window.opener.postMessage() to send the JWT back to the main app. 3. The main app has a message event listener that simply accepts any incoming postMessage and stores the token in localStorage without verifying the message origin. 4. The attacker creates a malicious webpage and embeds the original site using an iframe. 5. Once the user logs in through the legitimate popup, the attacker’s page — acting as the opener — also receives the token. 6. This is possible because the app did not verify event.origin and event.source before trusting the message. 7. The attacker uses the stolen JWT to authenticate as the victim and gain full access to their dashboard. 8. The user remains unaware because all activity happened in the background.
- **Detection**: Analyze JavaScript event listeners in DevTools for unsafe postMessage handling
- **Solution**: Always validate event.origin and event.source and implement signed token exchange
- **Tags**: #postmessage #jwtsteal #oauthabuse

## CORS-Based Data Exfiltration in Online Banking Portal

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Banking web applications
- **Vulnerability**: Wildcard origin and credentials flag in CORS
- **MITRE**: T1189
- **Impact**: Financial data theft and PII leakage
- **Tools**: curl, Burp Suite, DevTools
- **Scenario**: API leaks bank balance and transaction history due to wildcard origin and credentialed CORS
- **Attack Steps**: 1. The attacker targets an online banking app that has an endpoint /api/account/summary which returns user’s bank balance and recent transactions. 2. The backend API is configured to allow all origins by using Access-Control-Allow-Origin: * and also sets Access-Control-Allow-Credentials: true. 3. The attacker lures logged-in banking users to visit a malicious site (e.g., fake finance blog). 4. JavaScript on the attacker's page sends a fetch() request to the bank's API endpoint from the victim’s browser. 5. Because the user is logged in and CORS is misconfigured, the browser sends the session cookie along with the request. 6. The API responds with sensitive account information directly into the attacker's page context. 7. The attacker collects and forwards this data to their own server, gaining insight into financial activity. 8. The user sees no warnings, popups, or errors, making this a silent and dangerous exfiltration technique.
- **Detection**: Use curl and browser DevTools to test cross-origin API access
- **Solution**: Use exact trusted origin list in CORS and never combine * with credentials
- **Tags**: #corsmisconfig #bankingbreach #dataexfiltration

## Subdomain Takeover Leading to Trusted JS Injection

- **Attack Type**: Subdomain Takeover
- **Target**: Organizations with many subdomains
- **Vulnerability**: DNS mismanagement and orphaned CNAME
- **MITRE**: T1584.005
- **Impact**: Credential theft, script injection, session hijack
- **Tools**: GitHub Pages, Amass, nslookup
- **Scenario**: An old subdomain pointing to GitHub Pages is taken over and used to serve malicious JS under trusted domain
- **Attack Steps**: 1. A company had previously hosted a documentation site at docs.company.com via GitHub Pages. 2. They deleted the GitHub repo but forgot to remove the DNS CNAME entry. 3. The attacker scans the company’s subdomains and finds docs.company.com is pointing to GitHub Pages but unclaimed. 4. They register a GitHub repo named docs, link it to GitHub Pages, and take control of docs.company.com. 5. The attacker hosts a page that loads malicious JavaScript under the company’s trusted domain. 6. Because the browser sees this as same-origin (*.company.com), cookies, localStorage, and any same-origin access rules still apply. 7. If any sensitive data or session cookies are accessible to *.company.com, they can be read or exploited. 8. Users who trust the company may visit this subdomain and unknowingly expose their credentials or allow malware injection.
- **Detection**: Run automated subdomain takeover scans using Amass or Subjack
- **Solution**: Reclaim or sinkhole all unused subdomains; set cookie scope only to required subdomains
- **Tags**: #subdomaintakeover #dnsmisconfig #sessionhijack

## Health App Leaks Medical Reports via Insecure CORS

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Healthcare platforms
- **Vulnerability**: Dangerous mix of wildcard origin and credentials in CORS
- **MITRE**: T1189
- **Impact**: HIPAA breach, patient data leakage
- **Tools**: XSStrike, Postman, Chrome DevTools
- **Scenario**: Endpoint returns sensitive health records to any origin due to wildcard CORS + credentials
- **Attack Steps**: 1. A health app allows users to download their diagnostic reports through /api/reports/latest. 2. The API sends responses with Access-Control-Allow-Origin: * and includes Access-Control-Allow-Credentials: true. 3. The attacker creates a malicious site disguised as a health blog and shares it in fitness groups. 4. Logged-in users who visit this site unknowingly trigger a background fetch() request to the /api/reports/latest endpoint. 5. The victim’s browser includes authentication cookies, and the misconfigured CORS headers allow the response. 6. The attacker’s page reads the confidential lab reports including patient ID, diagnosis, and timestamps. 7. The attacker forwards this information to their own server for blackmail or resale. 8. The user never knows their health privacy was violated because everything happened silently.
- **Detection**: Simulate cross-origin requests using browser DevTools and inspect response headers
- **Solution**: Avoid wildcard origins; use token-based auth and limit CORS to trusted origins
- **Tags**: #medicalleak #corsvulnerability #hipaaviolation

## Login Token Forgery via Open Redirect and Fake postMessage

- **Attack Type**: PostMessage Exploitation
- **Target**: OAuth-integrated web platforms
- **Vulnerability**: Open redirect and no postMessage origin check
- **MITRE**: T1557.001
- **Impact**: Authentication bypass, session forgery
- **Tools**: Redirect Scanner, JS Debugger
- **Scenario**: Redirect to attacker’s page sends fake login confirmation using postMessage
- **Attack Steps**: 1. A website uses an OAuth login flow that redirects users to /oauth/complete?redirect=https://app.com/dashboard. 2. The redirect parameter is not validated properly and can point to attacker-controlled domains. 3. The attacker crafts a malicious URL that uses the open redirect to land the user on their own phishing site (https://evil.com/fake-dashboard). 4. The attacker mimics the legitimate post-login behavior by sending a postMessage to the parent window with a fake access token. 5. The main web app receives this message and, due to lack of origin validation, accepts the token and logs the user in. 6. The attacker now impersonates the user with a forged token, bypassing the actual login. 7. This method works without any need to phish the real credentials — it abuses trust in message origin and redirect behavior. 8. Users think they’re logging in securely, but never actually interacted with the real login provider.
- **Detection**: Audit all login-related postMessage handlers and redirect parameters
- **Solution**: Enforce strict redirect whitelists and validate message origin
- **Tags**: #redirectattack #tokenforgery #oauthmisuse

## Reading Cookies via Forgotten Subdomain in CDN

- **Attack Type**: Subdomain Takeover
- **Target**: CDN-hosted websites
- **Vulnerability**: Cookie scope misconfiguration
- **MITRE**: T1557
- **Impact**: Credential theft, session hijacking
- **Tools**: DNSDumpster, Netlify, DevTools
- **Scenario**: Attacker hosts malicious content on cdn.site.com and steals cookies scoped to .site.com
- **Attack Steps**: 1. A company previously served static files from cdn.site.com. 2. The subdomain was decommissioned, but its DNS still points to a CDN provider (like Netlify or Vercel). 3. The attacker finds the dangling subdomain and claims it by creating a new project with the same hostname. 4. They upload malicious JavaScript to the CDN, which uses document.cookie to read cookies scoped to .site.com. 5. When a victim visits the malicious subdomain, the attacker captures their session cookie. 6. This gives access to protected services if cookie-based auth is used. 7. The browser considers it same-origin due to cookie domain .site.com. 8. This is a silent but high-impact breach vector.
- **Detection**: Use Subjack to detect CDN-based subdomain takeovers
- **Solution**: Set cookies with SameSite=Strict and limit domain scope to specific services
- **Tags**: #cdnleak #cookiesteal #dnsdanger

## Forged Authentication via Fake iframe and Message Spoof

- **Attack Type**: PostMessage Exploitation
- **Target**: Sites with embedded login or payment widgets
- **Vulnerability**: No postMessage origin validation
- **MITRE**: T1557.001
- **Impact**: Fake login, account takeover
- **Tools**: iframe, DevTools
- **Scenario**: Fake iframe sends “login success” message accepted by app without validation
- **Attack Steps**: 1. The web application uses an iframe-based login widget that communicates back via postMessage. 2. Upon successful login, the iframe sends a message containing the user’s info or token. 3. The main site listens for message events but does not verify the sender’s origin. 4. The attacker embeds the app in a malicious page with a fake iframe designed to look like the real login widget. 5. This fake iframe immediately sends a forged message saying “Login successful” with fake user data. 6. The parent app, seeing the message, processes it and considers the user logged in. 7. The attacker now gains unauthorized access without real credentials. 8. All of this happens in-browser with no server-side checks.
- **Detection**: Validate both origin and content structure of received messages
- **Solution**: Use secure tokens and time-bound authentication flows
- **Tags**: #iframeabuse #spoofedlogin #originforgery

## Cross-Origin Blob File Exfiltration via Relaxed CORS

- **Attack Type**: Misconfigured CORS Headers
- **Target**: File preview systems
- **Vulnerability**: Public blob access with wildcard CORS
- **MITRE**: T1189
- **Impact**: Document theft, IP leak
- **Tools**: Chrome DevTools, curl
- **Scenario**: Blob-hosted file content is leaked due to loose CORS and unauthenticated access
- **Attack Steps**: 1. A web app allows users to preview uploaded documents via blob URLs. 2. These blob URLs are accessible via an endpoint like /preview/blob/xyz.pdf. 3. The server sends CORS headers allowing * as origin. 4. The attacker’s site runs JavaScript that loads this document via fetch() and reads the response. 5. If the user is logged in and the document is scoped to their session, it still gets served due to relaxed access control. 6. The attacker logs the PDF content and sends it to their server. 7. The user never sees any download prompt or warning.
- **Detection**: Enable auth and origin filtering for all document endpoints
- **Solution**: Use signed URLs and enforce token checks before file load
- **Tags**: #blobleak #fileexfiltration #corsflaw

## Domain Alias SOP Confusion via CDN-Mirrored Content

- **Attack Type**: DNS Confusion
- **Target**: Shared-IP domains
- **Vulnerability**: Misused DNS and domain scoping
- **MITRE**: T1584
- **Impact**: SOP bypass and origin spoofing
- **Tools**: DNS Checker, Host Tools
- **Scenario**: Alternate domain mirrors same content and tricks browser into accepting it as trusted
- **Attack Steps**: 1. A developer sets up mirror.site.com pointing to the same IP as main.site.com. 2. The browser treats both domains as separate origins, but server returns identical content. 3. Cookies scoped to .site.com are sent to both if the site structure overlaps. 4. Attacker hosts altered JS on mirror domain to abuse trust. 5. SOP is bypassed as site logic trusts all *.site.com.
- **Detection**: Harden DNS setup and verify domain handling logic
- **Solution**: Never share cookies or APIs across sibling domains
- **Tags**: #dnspoof #cdnabuse #originconfusion

## Script Injection via Forgotten CDN JS Endpoint

- **Attack Type**: Subdomain Takeover
- **Target**: Static asset subdomains
- **Vulnerability**: CDN-hosted JS without monitoring
- **MITRE**: T1190
- **Impact**: Persistent XSS and user compromise
- **Tools**: CDN Tools, JS Scanner
- **Scenario**: JS file loaded from inactive CDN subdomain gets replaced with malicious one
- **Attack Steps**: 1. The main site includes <script src="https://static.site.com/app.js">. 2. static.site.com was previously used for serving JS but is no longer monitored. 3. The attacker takes over this subdomain via a vulnerable CDN config. 4. They host a malicious app.js file that logs keystrokes and sends data to attacker’s server. 5. Every site user downloads this compromised file silently.
- **Detection**: Use Subresource Integrity (SRI) and monitor CDN domains
- **Solution**: Audit DNS for abandoned subdomains
- **Tags**: #cdninject #xss #sopbypass

## Abusing window.opener to Replace Parent Tab with Fake Login

- **Attack Type**: window.opener Abuse
- **Target**: Sites opened via window.open()
- **Vulnerability**: window.opener not nullified
- **MITRE**: T1204
- **Impact**: Credential theft via phishing tab swap
- **Tools**: Browser Console, JavaScript, DevTools
- **Scenario**: An attacker uses window.opener to redirect the original tab to a phishing login page
- **Attack Steps**: 1. The attacker builds a phishing site that mimics a news platform and includes links to the legitimate banking site. 2. When the user clicks the link, the bank's site opens in a new tab via window.open(). 3. Most browsers allow the newly opened tab to retain access to window.opener, meaning it can modify the original page. 4. In the newly opened (legitimate) tab, the attacker immediately redirects the opener (original tab) to a fake login page using window.opener.location = 'https://fakebank.com/login.html'. 5. The user is focused on the real banking page in the new tab but, when they switch back to the original tab (expecting news), they see what appears to be their banking login. 6. Thinking their session expired, they re-enter credentials. 7. The fake login form captures the username and password and sends them to the attacker. 8. This technique is stealthy and successful even without injecting any malicious scripts into the bank's page, as it exploits trust in tab flow.
- **Detection**: Analyze tab behavior using browser DevTools and test redirection via opener
- **Solution**: Always set rel="noopener noreferrer" on external links
- **Tags**: #windowopener #tabnabbing #phishing

## Reading Sensitive Cookies via Misconfigured document.domain

- **Attack Type**: document.domain Abuse
- **Target**: Cross-subdomain web apps
- **Vulnerability**: SOP relaxation via document.domain
- **MITRE**: T1189
- **Impact**: Session hijack and cross-app data leak
- **Tools**: JavaScript Console, Browser DevTools
- **Scenario**: Two sibling subdomains improperly set document.domain, enabling unauthorized access
- **Attack Steps**: 1. A company operates two apps: admin.company.com and profile.company.com. 2. For cross-subdomain communication, both apps set document.domain = 'company.com', which relaxes the SOP boundary. 3. The attacker identifies this behavior and gains control of a forgotten subdomain like blog.company.com. 4. They host malicious JavaScript on it and also set document.domain = 'company.com'. 5. Now, all three subdomains are considered the same origin. 6. The malicious script uses window.parent.frames or direct DOM access to read cookies, sessionStorage, or even sensitive HTML elements from admin.company.com. 7. This allows data theft, credential exfiltration, or content injection without breaching each subdomain individually. 8. Users remain unaware since the interaction occurs silently through same-origin logic.
- **Detection**: Inspect DOM access between frames and check for document.domain manipulation
- **Solution**: Avoid setting document.domain unless absolutely necessary; isolate sessions per subdomain
- **Tags**: #documentdomain #sopbypass #subdomainattack

## Exploiting Insecure CORS with Wildcard + Credentials in E-Commerce Site

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Online stores and marketplaces
- **Vulnerability**: CORS policy allows * + credentials
- **MITRE**: T1189
- **Impact**: Personal info leakage and customer profiling
- **Tools**: Burp Suite, curl, Postman
- **Scenario**: An e-commerce API allows any origin while sending cookies, exposing order and address data
- **Attack Steps**: 1. An e-commerce platform allows logged-in users to access their order history and shipping info through /api/orders/history. 2. The backend includes CORS headers like Access-Control-Allow-Origin: * and Access-Control-Allow-Credentials: true, which is a critical misconfiguration. 3. The attacker builds a fake product review blog and embeds malicious JavaScript on the page. 4. When a victim (logged-in customer) visits this site, the JavaScript silently issues a cross-origin fetch() to the e-commerce API. 5. The browser sends cookies along with the request since it’s a credentialed call. 6. The server responds with full order history, including item names, delivery addresses, and contact numbers. 7. The attacker’s script reads this data and sends it to a remote server. 8. The victim is unaware, as no alert or visible action occurs. This can lead to blackmail, resale of personal info, or physical stalking.
- **Detection**: Test API endpoints via cross-origin requests and inspect CORS headers
- **Solution**: Never combine Access-Control-Allow-Origin: * with credentialed requests; allow-list known origins
- **Tags**: #cors #ecommerce #infotheft

## Token Leakage via OAuth Flow and Open Redirect

- **Attack Type**: Open Redirect + PostMessage Exploitation
- **Target**: OAuth-integrated platforms
- **Vulnerability**: Unsafe redirect parameters + postMessage mishandling
- **MITRE**: T1557.001
- **Impact**: Account impersonation without password phishing
- **Tools**: OAuth Tester, Chrome DevTools, Redirect Scanner
- **Scenario**: Malicious redirect steals access tokens after OAuth login via manipulated postMessage
- **Attack Steps**: 1. A web app integrates OAuth login using a URL like /auth/callback?next=https://app.com/dashboard. 2. The app does not validate the next parameter, allowing any arbitrary URL. 3. The attacker creates a URL: https://site.com/auth/callback?next=https://attacker.com/fake-page. 4. The victim logs in normally, and after authentication, is redirected to the attacker’s controlled page. 5. The attacker’s fake page mimics a legitimate one and uses JavaScript to send a fake postMessage to the main site, including a forged token. 6. The main app, failing to verify the event.origin, accepts the message and uses the provided token for authentication. 7. Meanwhile, the attacker now possesses the real token as well — logged via the redirect chain. 8. The user is now impersonated silently without noticing anything wrong.
- **Detection**: Trace login flows and audit redirect destinations; inspect event listener code
- **Solution**: Enforce strict redirect whitelists and validate postMessage origin and structure
- **Tags**: #oauth #redirectabuse #tokensteal

## PDF Viewer Exploitation via Blob and Wildcard CORS

- **Attack Type**: Misconfigured CORS + Blob Access
- **Target**: Government or legal portals
- **Vulnerability**: CORS wildcard with blob + credentials
- **MITRE**: T1189
- **Impact**: Government record leakage and impersonation
- **Tools**: curl, Chrome DevTools
- **Scenario**: Web-based document viewer leaks confidential PDFs across origins
- **Attack Steps**: 1. A government portal allows users to preview PDFs through blob-based URLs (blob:https://govportal.com/abc123). 2. These blob URLs are accessed via an API endpoint /documents/preview with CORS set to * and credentials enabled. 3. The attacker creates a malicious blog and attracts logged-in users. 4. When a victim visits the site, JavaScript fetches the blob preview endpoint. 5. Since the user is authenticated and the browser sends cookies, and the response allows wildcard origin, the content is returned. 6. The attacker’s script accesses and logs the full content of the document. 7. This might include scanned IDs, court notices, or other sensitive government documents. 8. The data is silently sent to the attacker’s infrastructure.
- **Detection**: Simulate cross-origin requests and validate blob access
- **Solution**: Protect blob URLs using signed URLs or tokens, and avoid wildcard origin with auth
- **Tags**: #pdfleak #blobaccess #corsfail

## SOP Bypass via Unused Subdomain and Shared Cookie Scope

- **Attack Type**: Subdomain Takeover
- **Target**: Large orgs with multiple subdomains
- **Vulnerability**: Cookie scope mismanagement + orphaned DNS
- **MITRE**: T1557
- **Impact**: Silent account takeover
- **Tools**: Subjack, Amass, Netlify
- **Scenario**: A decommissioned subdomain still accepts cookies scoped to .example.com, leading to session theft
- **Attack Steps**: 1. The main site sets cookies like session_id=abc123; Domain=example.com. 2. An old analytics dashboard previously hosted on metrics.example.com is now unclaimed but still has an active DNS record pointing to Netlify. 3. The attacker registers the Netlify subdomain and takes control of metrics.example.com. 4. They host JavaScript that reads document.cookie and sends it to a remote server. 5. Since the browser sends .example.com scoped cookies to all subdomains, the attacker receives the active session token. 6. They use it to authenticate as the user on www.example.com. 7. The attack works without phishing or XSS — just bad subdomain hygiene. 8. The user is unaware as everything looks normal.
- **Detection**: Scan DNS for dangling subdomains and audit cookie domain scoping
- **Solution**: Scope cookies to exact domains and regularly clean unused subdomains
- **Tags**: #cookiesteal #subdomainattack #netlify

## Hijacking PostMessage Between Payment Iframe and Host Site

- **Attack Type**: PostMessage Exploitation
- **Target**: Stores using iframe-based payments
- **Vulnerability**: Unverified postMessage origin
- **MITRE**: T1557.001
- **Impact**: Free product fraud and order abuse
- **Tools**: iframe, Browser Console
- **Scenario**: A fake iframe mimics a payment gateway and sends forged “success” message
- **Attack Steps**: 1. An e-commerce site uses an embedded iframe to load a payment provider. 2. After payment, the provider sends a postMessage back to the main page indicating success. 3. The host site listens for this message but fails to validate the origin. 4. The attacker embeds the store in their own page, replaces the payment iframe with a fake one, and sends a forged message stating “Payment Completed.” 5. The store accepts the message, marks the order as paid, and proceeds with shipping. 6. The attacker receives items for free by bypassing actual payment. 7. This logic can be automated to exploit thousands of transactions. 8. No server communication was compromised — only SOP misuse in client messaging.
- **Detection**: Test message interception with fake iframes and analyze event listeners
- **Solution**: Accept messages only from strict origin whitelist and validate payload integrity
- **Tags**: #paymentspoof #iframeabuse #messageforgery

## SOP Bypass Using IP Alias Domain and Content Mirror

- **Attack Type**: DNS SOP Confusion
- **Target**: Sites with public mirrors or shared IP setups
- **Vulnerability**: SOP confusion via DNS/IP overlap
- **MITRE**: T1584
- **Impact**: Stealthy data access or interaction spoof
- **Tools**: Host Header Tools, DNS Checker
- **Scenario**: A mirrored IP domain tricks the browser into leaking data meant for the main site
- **Attack Steps**: 1. The attacker registers mirror.site.com and points it to the same IP as main.site.com. 2. Since the content is mirrored and no Host header check is enforced, the attacker serves a clone of the original site. 3. The browser sees both domains serving identical pages, giving the illusion of trust. 4. If cookies or storage data are scoped to .site.com, the attacker’s domain might receive those via cookie injection or confused DOM logic. 5. JS hosted on the mirror site can then access this data or trigger API calls using user sessions. 6. The attacker can now act on behalf of the victim or trick them into interacting with the fake copy. 7. Users assume they’re on a legitimate domain due to content familiarity. 8. No alert or SSL error occurs since HTTPS and certs still validate.
- **Detection**: Monitor domain mapping and validate Host headers server-side
- **Solution**: Enforce strict domain checks and avoid cookie sharing across mirrors
- **Tags**: #sopconfusion #dnsbypass #ipmirror

## Token Theft via Abused Subresource on External CDN

- **Attack Type**: Subdomain Takeover + Script Injection
- **Target**: Apps using CDN-hosted scripts
- **Vulnerability**: Unmonitored JS endpoint on orphaned subdomain
- **MITRE**: T1190
- **Impact**: Silent token exfiltration
- **Tools**: CDN Scanner, SRI Tester, DevTools
- **Scenario**: External JS loaded from forgotten CDN subdomain steals active tokens
- **Attack Steps**: 1. The main app includes JS from cdn.example.com/app.js with no Subresource Integrity (SRI). 2. The subdomain was used for hosting assets years ago and is now unclaimed. 3. The attacker registers the CDN subdomain and serves a malicious app.js containing token-stealing code. 4. All users visiting example.com unknowingly download and execute this JS. 5. The malicious script uses localStorage.getItem('token') and document.cookie to extract auth data. 6. The data is exfiltrated silently to the attacker's backend. 7. The attack bypasses SOP because the JS is served under same-origin and trusted path. 8. Without SRI or CSP, no detection or restriction stops the malicious payload.
- **Detection**: Use SRI in script tags and monitor asset loads via DevTools
- **Solution**: Enforce CSP and audit CDN ownership
- **Tags**: #cdnattack #srileak #tokentheft

## SOP Bypass via Malicious Message Origin Spoofing

- **Attack Type**: PostMessage Exploitation
- **Target**: Web apps with modular iframe architecture
- **Vulnerability**: Improper origin validation
- **MITRE**: T1557.001
- **Impact**: Privilege escalation, UI tampering
- **Tools**: Browser DevTools, JS Sniffer
- **Scenario**: A fake message origin bypasses weak validation logic and hijacks control flow
- **Attack Steps**: 1. A dashboard app uses iframe communication for modular UI. 2. It listens to postMessage events from child iframes but only checks event.origin partially (e.g., endsWith('.trusted.com')). 3. The attacker sets up evil.trusted.com.evil.com which passes the origin check. 4. The iframe sends a message that looks legitimate — like {action: 'updatePermissions', role: 'admin'}. 5. The parent app receives this, matches the suffix in origin, and applies it. 6. The attacker now elevates their privileges or disables key features. 7. This bypass works silently unless logs are monitored carefully. 8. The user sees nothing wrong on the frontend.
- **Detection**: Inspect postMessage logic for flawed origin checks
- **Solution**: Use exact match checks and signed messages
- **Tags**: #originspoof #iframesecurity #adminbypass

## Stealing Session via open Redirect with window.opener

- **Attack Type**: window.opener Abuse
- **Target**: Sites using window.open() without noopener
- **Vulnerability**: opener-based tab manipulation
- **MITRE**: T1204
- **Impact**: Phishing and session theft
- **Tools**: Browser DevTools, Redirect Scanner
- **Scenario**: Redirect chain leverages window.opener to replace tab with malicious phishing page
- **Attack Steps**: 1. The attacker finds a legitimate website that opens third-party links using window.open() and fails to set rel="noopener". 2. The attacker creates a page that opens the legitimate site in a new tab while keeping control over the opener. 3. Once opened, the attacker script modifies the parent window’s location using window.opener.location = 'https://fake-login.com'. 4. When the user clicks back to the original tab, they’re shown a fake login page that mimics the original site. 5. Believing they’ve been logged out, the user enters credentials. 6. The attacker captures and stores these credentials silently.
- **Detection**: Monitor referrer and tab-opening behavior with DevTools
- **Solution**: Use rel="noopener noreferrer" in all external links
- **Tags**: #tabnabbing #openerattack #phishing

## Data Leakage via Misconfigured Cross-Origin iframe Access

- **Attack Type**: iframe Content Access
- **Target**: Internal dashboards exposed via iframe
- **Vulnerability**: Improper iframe origin isolation
- **MITRE**: T1189
- **Impact**: Credential or config theft
- **Tools**: iframe Inspector, JS Console
- **Scenario**: Unrestricted iframe reads allow unauthorized access to cross-origin form data
- **Attack Steps**: 1. A marketing site embeds its internal admin dashboard in an iframe using a hardcoded URL. 2. It fails to use the sandbox or X-Frame-Options headers. 3. An attacker clones the marketing page and embeds the iframe too, making it appear genuine. 4. The attacker’s JavaScript accesses the iframe using DOM methods like contentWindow.document. 5. Due to same-origin misconfiguration (both subdomains set document.domain to base domain), access is allowed. 6. The attacker reads form input values like admin username or sensitive content being edited. 7. This works seamlessly if the user is already authenticated. 8. The attacker silently steals this information without triggering any alerts.
- **Detection**: Test iframe content access via JavaScript
- **Solution**: Use X-Frame-Options, CSP, and don’t relax SOP via document.domain
- **Tags**: #iframe #sopviolation #xframeoptions

## Exploiting Misconfigured CORS on Dev Environment APIs

- **Attack Type**: Misconfigured CORS Headers
- **Target**: Internal APIs on staging/dev subdomains
- **Vulnerability**: Wildcard CORS with credentials
- **MITRE**: T1189
- **Impact**: Internal user data leak
- **Tools**: curl, Subdomain Finder, Postman
- **Scenario**: Dev subdomain API exposes sensitive endpoints with overly permissive CORS
- **Attack Steps**: 1. A company hosts its staging APIs at api-dev.site.com. 2. This environment uses Access-Control-Allow-Origin: * and allows credentials during testing. 3. An attacker lures internal employees to visit a malicious domain while logged in to the dev app. 4. JavaScript on the attacker’s site makes a request to api-dev.site.com/user/profile. 5. The browser includes the session cookie since the dev API allows credentials. 6. The API responds with full user profile information — name, email, role, internal notes. 7. This data is read and forwarded to the attacker’s server. 8. The dev environment inadvertently becomes a source of leakage.
- **Detection**: Inspect response headers from dev APIs
- **Solution**: Restrict CORS and avoid credentials on non-production APIs
- **Tags**: #cors #devexposure #stagingleak

## Cross-Origin Popup Hijack Using Referer Trust

- **Attack Type**: Cross-Origin Leakage
- **Target**: SaaS platforms using popup flows
- **Vulnerability**: Trusting spoofable headers like Referer
- **MITRE**: T1557.001
- **Impact**: Account manipulation via spoofed messages
- **Tools**: Burp Suite, JS Sniffer
- **Scenario**: Application trusts Referer to validate origin, enabling spoofed access
- **Attack Steps**: 1. A SaaS platform opens sensitive functionality (like billing) in a popup and expects a message from the popup for confirmation. 2. The parent page checks only the Referer header to ensure it originated from a known domain. 3. The attacker crafts a page with a hidden iframe that mimics the expected Referer. 4. They open the real billing popup and send forged data using postMessage. 5. Since the parent trusts the Referer and doesn’t validate origin, it accepts the data. 6. Actions like billing approval or plan changes occur without user input. 7. This logic flaw leads to account abuse, upgrade fraud, or financial loss.
- **Detection**: Analyze origin validation logic and Referer reliance
- **Solution**: Enforce strict origin checks; avoid trusting headers like Referer
- **Tags**: #postmessage #refererflaw #popupbypass

## Cross-Site Printing via CORS-Enabled PDF Renderers

- **Attack Type**: CORS Abuse
- **Target**: Legal tech platforms
- **Vulnerability**: Open preview endpoints with wild CORS
- **MITRE**: T1189
- **Impact**: Confidential document leakage
- **Tools**: Chrome DevTools, curl, PDF.js
- **Scenario**: PDF preview endpoints allow cross-origin access, leaking sensitive contracts
- **Attack Steps**: 1. A legal platform allows users to preview PDF contracts stored under /pdf/view/contract.pdf. 2. These endpoints are CORS-enabled with Access-Control-Allow-Origin: *. 3. An attacker hosts a fake site and embeds a script that requests this PDF via fetch() from a victim’s browser. 4. If the victim is authenticated, the session cookie is sent and access granted. 5. The attacker’s script reads the content of the PDF and exfiltrates it. 6. Since previews are silent and CORS is too relaxed, the user doesn’t see anything. 7. This is especially risky when PDF contains names, signatures, and timestamps.
- **Detection**: Analyze CORS and token access on document endpoints
- **Solution**: Use signed URLs and limit CORS to verified frontends
- **Tags**: #cors #pdfpreview #infodump

## Trusted Subdomain Serves Malicious JavaScript

- **Attack Type**: Subdomain Takeover
- **Target**: Sites loading JS from unmonitored subdomains
- **Vulnerability**: CDN/asset subdomain hijack
- **MITRE**: T1190
- **Impact**: Persistent backdoor and credential theft
- **Tools**: Subjack, NS Lookup, GitHub Pages
- **Scenario**: Forgotten assets.site.com subdomain hosts attacker’s malicious JS used on main site
- **Attack Steps**: 1. A website loads https://assets.site.com/app.js in its <head> section. 2. This subdomain used to host images and scripts but is no longer monitored. 3. The attacker finds it pointing to a decommissioned S3/GitHub Pages bucket. 4. They claim the bucket, host their own malicious app.js, and match the original path. 5. Now every visitor to site.com loads the attacker’s JavaScript. 6. The malicious code captures localStorage tokens, cookies, and sends them out. 7. This results in silent takeover of user sessions across the main site.
- **Detection**: Scan for unused DNS records and JS loading paths
- **Solution**: Use Subresource Integrity (SRI) and monitor asset domains
- **Tags**: #cdnabuse #sribypass #subdomaintakeover

## Bypassing SOP Using IP Aliases and Misconfigured Host Headers

- **Attack Type**: Host Header Manipulation
- **Target**: Sites sharing IPs across aliases
- **Vulnerability**: Misused domain/IP structure
- **MITRE**: T1584
- **Impact**: Origin confusion and unauthorized access
- **Tools**: Host Header Scanner, DNS Map
- **Scenario**: Same IP used by multiple domains creates cross-origin illusion
- **Attack Steps**: 1. A site example.com shares an IP with api.example.com. 2. A third alias domain legacy.example.org points to the same IP but isn’t monitored. 3. The attacker hosts a clone of the original site on legacy.example.org. 4. Because of shared IP and missing Host header checks, cookies and localStorage are sent across both. 5. The attacker’s domain now acts as a drop-in replacement to access sensitive endpoints. 6. SOP fails as browser recognizes content as valid despite different origins. 7. The attacker leverages this to make background API calls or inject malicious payloads.
- **Detection**: Review host header handling and IP binding
- **Solution**: Isolate apps by IP and enforce Host header checks
- **Tags**: #hostspoof #aliasdomain #soptrick

## Stealing Auth Tokens via postMessage Replay in SPA

- **Attack Type**: PostMessage Exploitation
- **Target**: SPAs with token-based login
- **Vulnerability**: Insecure message origin/timing checks
- **MITRE**: T1557.001
- **Impact**: Token replay and impersonation
- **Tools**: JS Debugger, DevTools, XSStrike
- **Scenario**: SPA reads token from postMessage but doesn’t verify source or replay
- **Attack Steps**: 1. A Single Page Application receives auth tokens from a login popup using postMessage. 2. It lacks proper checks for message origin or timing. 3. The attacker opens the app in an iframe, captures a valid postMessage from earlier via JS. 4. The attacker replays the message with a modified token or copies the real one. 5. The app accepts the message, and session begins with the forged/stolen token. 6. This bypass works even after login popup is closed — due to poor state management. 7. The attacker now impersonates the victim and performs actions silently.
- **Detection**: Test postMessage listeners and message replay attempts
- **Solution**: Validate origin, enforce one-time tokens, and bind tokens to session
- **Tags**: #spa #tokenreplay #messagehijack

## Token Injection via CORS Misconfiguration in Mobile Webview

- **Attack Type**: CORS Headers + WebView
- **Target**: Hybrid mobile apps with embedded browsers
- **Vulnerability**: Unverified tokens and open CORS
- **MITRE**: T1189
- **Impact**: Data leakage and impersonation
- **Tools**: Mobile Emulator, DevTools
- **Scenario**: Mobile app loads CORS-enabled web content that accepts injected tokens
- **Attack Steps**: 1. A mobile app includes a webview that loads mobile.site.com. 2. This site accepts CORS from any origin, trusting all token values passed in requests. 3. The attacker builds a malicious app that embeds the same webview and preloads a forged token via JavaScript. 4. The webview treats the token as valid and displays personalized user data. 5. The attacker now has access to user info, recent activity, or transaction history. 6. This method exploits CORS misconfig plus insecure mobile integration.
- **Detection**: Inspect webview token flow and CORS headers
- **Solution**: Avoid wildcard origins and validate tokens against session
- **Tags**: #webview #tokeninjection #corsmobile

## Cross-Origin DOM Access via Relaxed SOP in Ad Widgets

- **Attack Type**: iframe SOP Relaxation
- **Target**: News sites with ad iframe integrations
- **Vulnerability**: SOP relaxation using document.domain
- **MITRE**: T1189
- **Impact**: Content spying and draft theft
- **Tools**: Browser Console, DOM Inspector
- **Scenario**: Embedded ad widget uses document.domain to access parent window DOM
- **Attack Steps**: 1. An advertising script loads via iframe on a news site. 2. Both iframe and parent set document.domain = 'newsnetwork.com'. 3. This relaxes SOP, allowing iframe to read or write parent DOM. 4. The attacker buys ad space and serves a malicious iframe that grabs content like email or comment drafts. 5. The attacker then exfiltrates this data. 6. Because both pages share the same base domain, the browser allows this behavior. 7. The attack goes unnoticed as it runs as part of an ad script.
- **Detection**: Monitor iframe interactions and domain settings
- **Solution**: Avoid using document.domain; sandbox untrusted frames
- **Tags**: #adabuse #soprelax #iframeattack

