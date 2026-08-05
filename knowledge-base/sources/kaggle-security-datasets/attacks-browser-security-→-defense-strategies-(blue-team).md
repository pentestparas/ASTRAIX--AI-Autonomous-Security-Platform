# Browser Security → Defense Strategies (Blue Team) Attacks

## Enforcing Strict CSP to Block Inline Scripts

- **Attack Type**: CSP
- **Target**: Web Applications
- **Vulnerability**: Inline script execution
- **MITRE**: T1203
- **Impact**: Prevents inline XSS payloads
- **Tools**: Browser DevTools, CSP Evaluator
- **Scenario**: A website implements a strict Content Security Policy to block all inline JavaScript, reducing XSS risk
- **Attack Steps**: 1. The security team writes a CSP header like Content-Security-Policy: script-src 'self'; object-src 'none'. 2. This configuration only allows scripts from the same origin and blocks eval, inline <script> tags, and event handler attributes. 3. When an attacker tries to inject an inline script (via XSS), it silently fails due to the browser’s policy enforcement. 4. Admins test it using CSP Evaluator and by simulating XSS payloads in URL parameters and comment boxes. 5. Browser console shows CSP violation errors confirming it's working. 6. Logs are reviewed regularly to track any CSP violations that indicate attempted exploits.
- **Detection**: Monitor browser console for CSP violations
- **Solution**: Set script-src without 'unsafe-inline'
- **Tags**: #CSP #XSSPrevention #BlueTeam

## Using SRI for CDN Libraries

- **Attack Type**: Subresource Integrity
- **Target**: Web Applications
- **Vulnerability**: Script tampering from third-party sources
- **MITRE**: T1554
- **Impact**: Prevents modified CDN scripts
- **Tools**: SRI Hash Generator, CDN, HTML
- **Scenario**: Protect against tampered third-party scripts by verifying hash
- **Attack Steps**: 1. The dev team includes a script from a CDN like <script src="https://cdn.example.com/lib.js" integrity="sha384-xyz" crossorigin="anonymous">. 2. The integrity attribute ensures the browser verifies the hash of the fetched script. 3. If the CDN is compromised and the script content changes, the browser blocks it. 4. This mitigates risks of supply chain attacks from CDN libraries. 5. Developers generate the hash using trusted tools and lock it in the HTML. 6. Logs are configured to capture blocked resource attempts. 7. Regular updates to libraries are followed by hash regeneration and retesting.
- **Detection**: Monitor blocked resource loading via browser devtools
- **Solution**: Use integrity and crossorigin attributes properly
- **Tags**: #SRI #CDNSecurity #ScriptIntegrity

## Blocking Mixed Content with CSP

- **Attack Type**: CSP
- **Target**: HTTPS-enabled websites
- **Vulnerability**: Loading insecure resources
- **MITRE**: T1071.001
- **Impact**: Prevents mixed content injection
- **Tools**: Browser DevTools, HTTPSCheck
- **Scenario**: Prevent insecure (HTTP) resources from loading on HTTPS sites
- **Attack Steps**: 1. Admins implement a CSP header like Content-Security-Policy: upgrade-insecure-requests; or block-all-mixed-content. 2. This prevents loading of insecure HTTP scripts, images, or styles on secure (HTTPS) pages. 3. Attackers attempting to inject HTTP payloads will be blocked at the browser level. 4. Security teams test by embedding <img src="http://attacker.com/test.jpg"> and seeing if the browser blocks it. 5. Browser console logs mixed content violation. 6. Admins periodically audit third-party resources to ensure they use HTTPS. 7. Logs are forwarded to SIEM to correlate with possible MITM attempts.
- **Detection**: Use browser devtools to monitor network requests
- **Solution**: Enforce upgrade-insecure-requests in CSP
- **Tags**: #MixedContent #CSP #HTTPSOnly

## DOMPurify Integration to Sanitize User Inputs

- **Attack Type**: Input Sanitization
- **Target**: Web forms accepting user input
- **Vulnerability**: Reflected/stored XSS injection
- **MITRE**: T1059.007
- **Impact**: Stops client-side script injection
- **Tools**: DOMPurify, JS Console
- **Scenario**: Neutralizes potentially malicious HTML or JS input from users
- **Attack Steps**: 1. Developers import DOMPurify into the web app and pass all user-supplied input through DOMPurify.sanitize(input). 2. Whether users submit rich text (e.g., comments or profile bios), all tags are scanned for unsafe content. 3. Payloads like <script>alert(1)</script> or <img src=x onerror=alert(1)> are cleaned before rendering. 4. The original input is preserved in DB but only sanitized output is shown. 5. The system also escapes dangerous characters like <, >, ", and &. 6. Developers test with known XSS payloads from XSS Cheat Sheet. 7. Automated scanners confirm nothing bypasses DOMPurify.
- **Detection**: Use dynamic JS sanitization on render
- **Solution**: Apply DOMPurify before inserting HTML
- **Tags**: #XSSDefense #Sanitization #DOMPurify

## Disabling Inline Event Handlers via CSP

- **Attack Type**: CSP
- **Target**: HTML applications with JS
- **Vulnerability**: Inline JS event execution
- **MITRE**: T1059
- **Impact**: Neutralizes script handler abuse
- **Tools**: CSP Header, Browser Inspector
- **Scenario**: Prevents scripts like onclick="..." from executing
- **Attack Steps**: 1. Security team applies Content-Security-Policy: script-src 'self'; to disable inline handlers like onclick, onload, etc. 2. Attempts to inject payloads like <button onclick="alert(1)"> are rendered inert. 3. Application replaces inline handlers with JS-bound event listeners. 4. Security testing confirms that CSP blocks all inline-style scripting. 5. Developers check violation reports for any attempts to break policy. 6. Browser console provides real-time feedback during test payloads. 7. Hardening this way reduces XSS vectors from both DOM and template injections.
- **Detection**: Use listener-based JS binding, not inline
- **Solution**: Disallow 'unsafe-inline' in CSP header
- **Tags**: #InlineBlock #CSP #SecureHandlers

## XSS Filter Bypass Prevention with Output Escaping

- **Attack Type**: Input Escaping
- **Target**: Server-side and template-based apps
- **Vulnerability**: Interpreted malicious characters
- **MITRE**: T1059.007
- **Impact**: Stops encoded payload execution
- **Tools**: OWASP Cheat Sheet, Dev Console
- **Scenario**: Escapes output to stop browsers from interpreting HTML tags
- **Attack Steps**: 1. Backend or frontend escapes all dynamic content using encoding libraries. 2. Inputs like <script>alert(1)</script> are stored as &lt;script&gt;alert(1)&lt;/script&gt;. 3. This ensures browser renders them as plain text, not executable code. 4. Libraries like htmlspecialchars() (PHP), encodeForHTML() (Java), or {{ }} (JS templates) are used. 5. Teams perform black-box testing with common payloads. 6. No scripts fire in preview or final render. 7. This approach complements sanitization and covers templating engines.
- **Detection**: Scan all rendered outputs in browser view
- **Solution**: Encode special characters in untrusted input
- **Tags**: #EscapeOutput #XSSFilter #HTMLEncode

## Restricting Frame Embedding with CSP Frame Ancestors

- **Attack Type**: CSP
- **Target**: Sites vulnerable to iframe embedding
- **Vulnerability**: Clickjacking via framing
- **MITRE**: T1110.003
- **Impact**: Stops unauthorized framing
- **Tools**: Framebuster Test Tool, CSP
- **Scenario**: Prevents clickjacking via frame restrictions
- **Attack Steps**: 1. Security team configures CSP like Content-Security-Policy: frame-ancestors 'self'; in the HTTP response. 2. This restricts the site from being embedded in iframes by other domains. 3. When an attacker tries to frame the site in a phishing page, the browser refuses to render it. 4. Admins simulate iframe attacks using tools or test pages to verify the block. 5. This policy thwarts clickjacking and UI redress attacks. 6. Reports of blocked framing attempts are reviewed for trends. 7. Additional headers like X-Frame-Options are added for backward compatibility.
- **Detection**: Test frame rendering in multiple origins
- **Solution**: Use frame-ancestors and X-Frame-Options
- **Tags**: #CSP #ClickjackingDefense #IframeBlock

## Automated CSP Violation Reporting

- **Attack Type**: CSP
- **Target**: CSP-enabled sites
- **Vulnerability**: Silent script execution attempts
- **MITRE**: T1082
- **Impact**: Detects policy bypass attempts
- **Tools**: CSP Reporter, HTTP Endpoint
- **Scenario**: Sends browser reports on policy violations
- **Attack Steps**: 1. Site implements report-uri or report-to in CSP: Content-Security-Policy: script-src 'self'; report-uri /csp-report. 2. If any script is blocked by the CSP (e.g., injected by an attacker), the browser sends a JSON report to /csp-report. 3. Security team stores and reviews these logs via ELK stack or SIEM. 4. Real-time alerts are triggered on excessive violations or specific sources. 5. This provides early warning for attempted XSS or policy misconfigurations. 6. Admins adjust rules based on violation frequency. 7. Helps in enforcing strict CSP gradually with monitor mode.
- **Detection**: Monitor /csp-report endpoint logs
- **Solution**: Use Content-Security-Policy-Report-Only first
- **Tags**: #CSPReporting #MonitorMode #SecurityLogs

## Subresource Integrity on CSS Files

- **Attack Type**: Subresource Integrity
- **Target**: Public-facing sites
- **Vulnerability**: Tampered CSS injection
- **MITRE**: T1554
- **Impact**: Stops external style hijack
- **Tools**: SRI Hash Generator, CDN
- **Scenario**: Applies SRI to external CSS to avoid injection
- **Attack Steps**: 1. Devs include third-party CSS using: <link rel="stylesheet" href="..." integrity="sha384-..." crossorigin="anonymous">. 2. The hash ensures CSS hasn’t been modified on the CDN. 3. If tampered, the browser blocks the file and logs error in console. 4. Prevents attackers from injecting malicious font-face or style rules. 5. Combined with a CSP, this secures third-party resources. 6. Admins audit all external resources and regenerate SRI hashes after updates. 7. Broken styles alert the team to possible compromise.
- **Detection**: Inspect devtools for blocked CSS
- **Solution**: Use SRI with version-pinned CSS
- **Tags**: #SRICSS #CDNDefense #StyleSecurity

## CSP for Blocking Eval and Dynamic Code

- **Attack Type**: CSP
- **Target**: JS-heavy apps or SPAs
- **Vulnerability**: Dynamic code execution
- **MITRE**: T1059.007
- **Impact**: Blocks DOM-based script injection
- **Tools**: JS Console, CSP
- **Scenario**: Disables dangerous functions like eval() or Function()
- **Attack Steps**: 1. Team adds Content-Security-Policy: script-src 'self'; or unsafe-eval is excluded. 2. Attempts to execute dynamic JS with eval("alert(1)") are blocked. 3. Attackers trying DOM-based XSS using eval() are stopped by browser. 4. Security team tests common gadgets like Function("return alert(1)") and confirms they fail. 5. Logs capture blocked eval attempts. 6. This protects from both internal misuse and malicious user inputs. 7. JS libraries relying on eval are audited and replaced.
- **Detection**: Check console for eval() blocks
- **Solution**: Disallow unsafe-eval in CSP
- **Tags**: #EvalBlock #CSP #DOMXSSDefense

## Applying CSP Nonce for Script Whitelisting

- **Attack Type**: CSP
- **Target**: Dynamic content apps
- **Vulnerability**: XSS via script injection
- **MITRE**: T1203
- **Impact**: Blocks unauthorized scripts from executing
- **Tools**: CSP Nonce Generator, Browser Dev Console
- **Scenario**: Allows only scripts with server-generated nonce to run
- **Attack Steps**: 1. The server dynamically generates a cryptographic nonce value (e.g., abcdef1234) on every HTTP response. 2. This nonce is embedded in both the CSP header (Content-Security-Policy: script-src 'nonce-abcdef1234') and applied to script tags (<script nonce="abcdef1234">). 3. Only these whitelisted scripts are allowed to execute in the browser. 4. Attempts to inject scripts without the nonce (via XSS, URL parameters, comment fields) are blocked. 5. Security team uses CSP violation logs to verify attacks are stopped. 6. Randomized nonce ensures even if one payload is leaked, it won't work in future sessions. 7. Nonce implementation is tested across templating engines and JS frameworks.
- **Detection**: CSP logs, browser console error reports
- **Solution**: Generate new nonce per request and enforce server-side
- **Tags**: #CSP #Nonce #ScriptWhitelisting

## SRI for Custom JavaScript Libraries

- **Attack Type**: Subresource Integrity
- **Target**: base64). 2. The HTML is updated to include: `. 3. This ensures that even if the internal server is compromised, modified scripts won’t run unless hashes match. 4. QA team validates hash enforcement in staging. 5. Security tools monitor for blocked script loads or content mismatches. 6. DevOps includes hash generation in CI/CD process. 7. Helps defend against insider threat or build pipeline compromise.
- **Vulnerability**: Internally hosted web apps
- **MITRE**: Internal script tampering
- **Impact**: T1554
- **Tools**: SHA384 Generator, Dev Console
- **Scenario**: Protects integrity of self-hosted or internal JS libraries
- **Attack Steps**: 1. The team hashes their internal JS file using SHA-384 (`openssl dgst -sha384 -binary file.js
- **Detection**: Prevents unauthorized JS execution
- **Solution**: Browser blocks mismatched hashes
- **Tags**: Automate hash generation & integrity tags

## Escaping Untrusted Input in React with JSX

- **Attack Type**: Input Escaping
- **Target**: React apps
- **Vulnerability**: HTML injection in component render
- **MITRE**: T1059.007
- **Impact**: Prevents stored and reflected XSS
- **Tools**: React, ESLint
- **Scenario**: Prevents XSS in React by safely rendering user content
- **Attack Steps**: 1. React escapes all JSX expressions by default, rendering user input as text, not HTML. 2. Example: <div>{userInput}</div> automatically encodes characters like <, >, and &. 3. Only when dangerouslySetInnerHTML is used, raw HTML is injected — this is avoided unless absolutely needed. 4. Developers are trained to use JSX expressions over raw HTML rendering. 5. ESLint rules warn when dangerouslySetInnerHTML is used without sanitization. 6. Common payloads (<script>, onerror=alert) are tested and shown as plain text. 7. Framework’s escaping ensures no script execution unless explicitly allowed.
- **Detection**: Dev console, rendered output inspection
- **Solution**: Avoid dangerouslySetInnerHTML; use JSX expressions
- **Tags**: #ReactXSS #JSXEscape #FrontendSecurity

## CSP Sandbox Directive for Isolating Widgets

- **Attack Type**: CSP
- **Target**: Websites with embedded third-party widgets
- **Vulnerability**: Privilege escalation via iframe
- **MITRE**: T1110.003
- **Impact**: Containment of untrusted content
- **Tools**: Browser Dev Console, CSP Sandbox
- **Scenario**: Limits embedded scripts and form submission within iframe
- **Attack Steps**: 1. CSP is configured as Content-Security-Policy: sandbox allow-scripts allow-forms;. 2. Embedded content (like third-party widgets) is placed in an <iframe> that inherits this policy. 3. This restricts the iframe from executing top-level navigation, submitting forms to external URLs, or executing untrusted code. 4. Even if malicious content loads inside iframe, it cannot affect the parent page. 5. CSP violation reports track restricted behavior. 6. Developers test iframe behavior to ensure core features still work within sandbox. 7. This is used for comment systems, ads, or analytics.
- **Detection**: Use browser iframe sandbox inspection tools
- **Solution**: Add sandbox directive to CSP + iframe tag
- **Tags**: #CSPSandbox #IframeIsolation #WidgetSecurity

## Auto-Escaping Templates in Django

- **Attack Type**: Input Escaping
- **Target**: safefilter unless content is explicitly trusted. 4. QA team tests XSS payloads like`, confirming they are displayed as text. 5. Framework ensures that database-stored payloads don’t execute on future renders. 6. The team uses Django security middleware for extra protections. 7. Static analyzers ensure unsafe filters aren't used.
- **Vulnerability**: Python-based web apps
- **MITRE**: Unsanitized user input
- **Impact**: T1059.007
- **Tools**: Django Templating Engine
- **Scenario**: Renders dynamic content with safe output encoding
- **Attack Steps**: 1. Django templates escape variables by default using HTML encoding. 2. Example: {{ user_input }} renders as &lt;script&gt;alert(1)&lt;/script&gt; in browser. 3. Devs are trained not to use `
- **Detection**: Prevents auto-executing payloads
- **Solution**: Template render inspection and XSS test cases
- **Tags**: Stick to default escaping and avoid unsafe filters

## Combining CSP + SRI for Defense-in-Depth

- **Attack Type**: CSP + SRI
- **Target**: Web apps using third-party CDNs
- **Vulnerability**: Combined supply chain & XSS vectors
- **MITRE**: T1554, T1059
- **Impact**: Hardened script execution path
- **Tools**: CSP Header, SRI Hash, Dev Console
- **Scenario**: Dual defense against injection and CDN tampering
- **Attack Steps**: 1. Site applies CSP (script-src 'self' https://cdn.example.com) alongside SRI integrity tags for each external script. 2. If attacker compromises CDN but the hash doesn’t match, the browser blocks the script. 3. If attacker injects new scripts, CSP prevents execution as it's not in allowed sources. 4. This combo ensures script source + content are both verified. 5. Logs are monitored for blocked executions. 6. Red teamers test bypasses to validate hardening. 7. This layered approach addresses both delivery and execution vectors.
- **Detection**: Browser network console, integrity failure logs
- **Solution**: Implement both CSP and SRI in tandem
- **Tags**: #DefenseInDepth #CSPplusSRI #SecureScripts

## Logging CSP Violations to SIEM

- **Attack Type**: CSP
- **Target**: Enterprise-grade web apps
- **Vulnerability**: Silent CSP policy probing
- **MITRE**: T1082
- **Impact**: Proactive policy enforcement visibility
- **Tools**: ELK, Splunk, Report-Only Mode
- **Scenario**: CSP reports sent to SIEM for threat visibility
- **Attack Steps**: 1. CSP header includes report-uri /csp-report or report-to. 2. Browser sends JSON logs for blocked scripts, styles, or frames. 3. These are forwarded to ELK/Splunk for centralized monitoring. 4. Analysts correlate reports with user agents and timestamps to detect targeted attacks. 5. Spike in reports from one IP can indicate probing. 6. Reports are used to refine policies and add new domain whitelists. 7. Helps teams migrate from Report-Only to strict CSP over time.
- **Detection**: Monitor CSP report endpoint in SIEM
- **Solution**: Review logs and adjust CSP rules accordingly
- **Tags**: #CSPReporting #SIEM #BrowserSecurity

## Sanitizing JSON Responses with Escaping

- **Attack Type**: Input Escaping
- **Target**: APIs serving dynamic content
- **Vulnerability**: Unsafe rendering of JSON keys
- **MITRE**: T1059.007
- **Impact**: Prevents DOM-based API injection
- **Tools**: JSON Formatter, API Tester
- **Scenario**: Prevents JSON-based XSS in APIs returning HTML
- **Attack Steps**: 1. APIs returning HTML inside JSON (e.g., {"bio": "<script>...</script>"}) are risky if directly rendered. 2. Backend escapes all HTML tags in JSON values before sending. 3. Frontend ensures content from JSON is treated as text, not HTML. 4. Libraries like lodash.escape or custom sanitizers are used. 5. QA team tests endpoint with XSS payloads. 6. Rendering output shows plain text, no execution. 7. Protects against DOM-based and reflected attacks from JSON APIs.
- **Detection**: Test response rendering in browser context
- **Solution**: Sanitize and escape API output
- **Tags**: #JSONSanitization #APIHardening #EscapeHTML

## Preventing Script Injection via Markdown Parsing

- **Attack Type**: Input Sanitization
- **Target**: Blogs, forums, user-generated content
- **Vulnerability**: Script tags in markdown
- **MITRE**: T1059.007
- **Impact**: Sanitized rich content rendering
- **Tools**: MarkdownIt + DOMPurify
- **Scenario**: Stops embedded script tags in user Markdown input
- **Attack Steps**: 1. Web app allows users to write Markdown (e.g., forum posts, bios). 2. Markdown parser (e.g., MarkdownIt) is used in safe mode with HTML disabled. 3. For added safety, output is passed through DOMPurify.sanitize() before rendering. 4. Payloads like <script>alert(1)</script> or [xss](javascript:alert(1)) are neutralized. 5. Rendering tests show harmless HTML or text. 6. Security regression tests are automated. 7. Markdown remains rich, but safe.
- **Detection**: Render markdown and inspect resulting DOM
- **Solution**: Disable raw HTML + use sanitizer
- **Tags**: #MarkdownXSS #SafeRender #ContentSecurity

## Limiting Dangerous HTML Tags in CMS Editors

- **Attack Type**: Input Sanitization
- **Target**: CMS Platforms
- **Vulnerability**: Dangerous tag injection via rich editor
- **MITRE**: T1059.007
- **Impact**: Blocks rich content XSS
- **Tools**: CKEditor, TinyMCE, HTML Sanitizer
- **Scenario**: Disallows <iframe>, <script>, <object> tags from editors
- **Attack Steps**: 1. Admins configure WYSIWYG editors to whitelist only safe tags (<b>, <i>, <ul>, etc.). 2. Tags like <script>, <iframe>, <embed>, and onerror attributes are stripped automatically. 3. Users attempting to inject these see them removed on save or preview. 4. Backend also sanitizes submitted HTML as a second layer. 5. Security team confirms payloads like <iframe src="attacker.com"> are never rendered. 6. Periodic audits ensure config remains strict after updates. 7. This prevents stored XSS via CMS.
- **Detection**: Use preview + raw mode to verify saved content
- **Solution**: Configure tag whitelist and sanitize backend
- **Tags**: #CMSXSS #EditorHardening #InputSanitize

## Preventing Inline Styles with CSP Style Restrictions

- **Attack Type**: CSP
- **Target**: Web Applications
- **Vulnerability**: Inline CSS injection
- **MITRE**: T1203
- **Impact**: Prevents CSS-based phishing or UI attacks
- **Tools**: CSP Evaluator, Dev Console
- **Scenario**: Blocks style attributes that could hide phishing UI or enable UI redress
- **Attack Steps**: 1. A CSP header is configured to block inline styles: Content-Security-Policy: style-src 'self';. 2. This prevents style injection such as hiding login buttons or tricking users with misleading UI via CSS. 3. Phishing attempts using style="display:none" or position overlays are blocked. 4. The team tests form fields with malicious style attributes to verify enforcement. 5. The browser logs CSP violations in the console when such attempts occur. 6. All styles must now be served from secure external stylesheets. 7. This mitigates several visual-based attacks, including clickjacking.
- **Detection**: CSP console error reports
- **Solution**: Disallow 'unsafe-inline' in style-src directive
- **Tags**: #CSP #StyleSecurity #InlinePrevention

## Escaping HTML Output in Node.js Templates

- **Attack Type**: Input Escaping
- **Target**: Node.js based websites
- **Vulnerability**: Script tag injection
- **MITRE**: T1059.007
- **Impact**: Eliminates client-side script injection
- **Tools**: Node.js, EJS, Pug
- **Scenario**: Avoids script execution by escaping output in EJS, Pug templates
- **Attack Steps**: 1. Developers use EJS or Pug templating engines for server-side rendering. 2. They output variables using syntax like <%= userInput %> (escaped) instead of <%- userInput %> (unescaped). 3. This ensures characters like <, > and " are encoded before rendering. 4. Test cases with <script>alert(1)</script> show script tags are neutralized. 5. Static code analysis helps detect instances where raw output is used. 6. QA and security teams validate escaping behavior before production deployment. 7. Ensures XSS is mitigated at render time.
- **Detection**: Manual inspection & automated testing
- **Solution**: Use safe template syntax (<%= %>) by default
- **Tags**: #NodeSecurity #TemplateEscape #XSSMitigation

## Using Trusted Types to Prevent DOM-Based XSS

- **Attack Type**: CSP + Browser Policy
- **Target**: JavaScript-heavy applications
- **Vulnerability**: DOM injection points like innerHTML
- **MITRE**: T1059.007
- **Impact**: Blocks unsafe DOM-based assignments
- **Tools**: Chrome Trusted Types, JavaScript
- **Scenario**: Enforces safe handling of DOM sinks like innerHTML
- **Attack Steps**: 1. Developers enable Trusted Types in the CSP: Content-Security-Policy: require-trusted-types-for 'script';. 2. This prevents functions like element.innerHTML = userInput unless the input is explicitly trusted. 3. Developers define and register a Trusted Type policy using TrustedTypes.createPolicy. 4. Any unsafe DOM manipulation throws an error unless wrapped in approved sanitization. 5. This mitigates DOM-based XSS even in complex single-page apps. 6. Logging tools capture violations to detect legacy or unsafe JS behavior. 7. Over time, code is refactored to comply with Trusted Types policies.
- **Detection**: Monitor browser policy violation logs
- **Solution**: Require Trusted Types in CSP and refactor JS
- **Tags**: #TrustedTypes #DOMXSS #CSPAdvanced

## Restricting iframe Embeds with X-Frame-Options

- **Attack Type**: Clickjacking Prevention
- **Target**: Login or financial portals
- **Vulnerability**: UI redress via framing
- **MITRE**: T1110.003
- **Impact**: Stops clickjacking completely
- **Tools**: HTTP Headers, Browser Testing
- **Scenario**: Prevents the site from being framed by other domains
- **Attack Steps**: 1. Admins configure web server headers with X-Frame-Options: SAMEORIGIN or DENY. 2. This prevents clickjacking attacks where the site is embedded into another site invisibly. 3. Users can’t be tricked into clicking on elements that perform sensitive actions. 4. Red teamers attempt to embed the site into another using <iframe> and are blocked. 5. CSP headers like frame-ancestors are also added for modern protection. 6. Browser dev tools show the rejection clearly. 7. Ensures UI redressing attacks are effectively mitigated.
- **Detection**: Monitor iframe loading behavior
- **Solution**: Add X-Frame-Options + frame-ancestors
- **Tags**: #Clickjacking #UIRedress #SecureHeaders

## Verifying Subresource Integrity Violations in CI/CD

- **Attack Type**: SRI
- **Target**: Static website deployments
- **Vulnerability**: Script or style compromise during CI/CD
- **MITRE**: T1554
- **Impact**: Prevents vulnerable third-party resource injection
- **Tools**: GitHub Actions, Jenkins, SRI Checker
- **Scenario**: Integrate script integrity checks in deployment pipeline
- **Attack Steps**: 1. DevSecOps adds integrity verification step to the CI/CD pipeline. 2. Each script or CSS file fetched from CDN is hashed during build and validated. 3. Hash is injected into production HTML via templating or static generation tools. 4. If file content changes without updating the hash, the build fails. 5. Tests ensure that tampered or unapproved versions of libraries are rejected. 6. SRI checking tools scan the HTML for missing or invalid hashes. 7. Promotes secure release practices and tamper-proof deployment.
- **Detection**: CI job logs and browser console
- **Solution**: Enforce integrity validation in build steps
- **Tags**: #DevSecOps #SRIAutomation #CDNDefense

## Defusing URL-based XSS in Search Parameters

- **Attack Type**: Input Escaping
- **Target**: Search results pages
- **Vulnerability**: Reflected XSS via URL params
- **MITRE**: T1059.007
- **Impact**: Eliminates reflected script execution
- **Tools**: JavaScript, Encoding Libraries
- **Scenario**: Prevents reflected XSS from search query params
- **Attack Steps**: 1. Search functionality on the site takes ?q=term and displays it in the results page. 2. Without proper escaping, attackers can inject ?q=<script>alert(1)</script>. 3. Developers use textContent or escape libraries to render search queries. 4. For example, document.getElementById("output").textContent = userQuery avoids dangerous interpretation. 5. Pen testers attempt known payloads but nothing executes. 6. Escaped characters render as visible text. 7. All query params are encoded before render using consistent utilities.
- **Detection**: Use browser dev tools to inspect rendered HTML
- **Solution**: Use .textContent, not .innerHTML
- **Tags**: #URLXSS #QueryEscape #ReflectedXSSDefense

## Sanitizing Third-Party Comments with Back-End Filters

- **Attack Type**: Input Sanitization
- **Target**: User comment systems
- **Vulnerability**: Stored XSS via rich input
- **MITRE**: T1059.007
- **Impact**: Blocks persistent XSS
- **Tools**: Backend Filters, HTMLPurifier, DOMPurify
- **Scenario**: Removes script injections from third-party comments before render
- **Attack Steps**: 1. The site allows users to post comments using rich text. 2. Input is passed through a backend sanitizer like HTMLPurifier or DOMPurify before storing in DB. 3. Tags such as <script>, onload, javascript: in hrefs are removed or neutralized. 4. Stored values are verified before rendering in the browser. 5. Comment display is tested with common XSS payloads to ensure they are filtered. 6. Edge case payloads using Unicode obfuscation are also tested. 7. Logs are analyzed to monitor sanitized vs rejected payloads.
- **Detection**: Inspect raw stored data and rendering output
- **Solution**: Apply sanitization pre-storage and pre-render
- **Tags**: #CommentXSS #InputFilter #SafeRender

## CSP Report-Only Mode for Safe Testing

- **Attack Type**: CSP
- **Target**: Any production site
- **Vulnerability**: Breaking functionality with new CSP
- **MITRE**: T1082
- **Impact**: Smooth rollout of secure policies
- **Tools**: CSP Report Viewer, SIEM
- **Scenario**: Deploys CSP in non-enforcing mode to monitor violations
- **Attack Steps**: 1. Site begins by implementing Content-Security-Policy-Report-Only header. 2. Browser logs CSP violations without enforcing blocking behavior. 3. Allows teams to collect violation data from users in real time. 4. Common issues like missing sources or inline script usage are identified. 5. Based on reports, the team updates the policy iteratively. 6. Once all legit violations are fixed, the site switches to enforcing mode. 7. This prevents downtime or broken UI due to overly strict policies.
- **Detection**: Analyze CSP reports via /csp-report endpoint
- **Solution**: Use Report-Only mode for test phase
- **Tags**: #CSPTest #PolicyHardening #SafeRollout

## Preventing Inline JavaScript in CMS Templates

- **Attack Type**: Input Sanitization
- **Target**: CMS platforms
- **Vulnerability**: Script injection via editable fields
- **MITRE**: T1059.007
- **Impact**: Eliminates author-based XSS vectors
- **Tools**: CMS Config, JS Sanitizer
- **Scenario**: Blocks editors from injecting inline scripts in CMS templates
- **Attack Steps**: 1. CMS admin disables JS execution in rich text editors used for page templates. 2. Fields are configured to remove <script>, onerror, and javascript: entries automatically. 3. Sanitization is enforced on both save and render. 4. If any script sneaks through, the frontend still applies CSP to block execution. 5. Test entries with embedded scripts fail silently. 6. Logs show attempts to inject disallowed tags. 7. CMS is patched regularly to fix any new injection vectors.
- **Detection**: Inspect saved template content
- **Solution**: Sanitize and validate template HTML
- **Tags**: #CMSHardened #EditorSanitize #BlueTeamDefenses

## CSP Whitelisting for Secure External Resources

- **Attack Type**: CSP
- **Target**: Sites with third-party content
- **Vulnerability**: Malicious script loads
- **MITRE**: T1554
- **Impact**: Stops unapproved external JS/CSS
- **Tools**: HTTP Headers, CSP Validator
- **Scenario**: Limits JS/CSS loads to vetted external sources only
- **Attack Steps**: 1. A strict script-src and style-src directive is applied in CSP to allow only trusted CDNs (e.g., script-src 'self' https://trusted.cdn.com). 2. Scripts from unknown or malicious sources are blocked immediately. 3. CSP is tested by loading scripts from other domains, which the browser denies. 4. The team monitors CSP violations via reports. 5. Whitelist is regularly updated with security-reviewed CDNs only. 6. Any deviation triggers alerts and is treated as potential tampering. 7. This blocks supply chain attacks involving shady external resources.
- **Detection**: Monitor blocked script logs
- **Solution**: Maintain strict source whitelist in CSP
- **Tags**: #ScriptSrcWhitelist #CDNSecurity #CSPHardening

## Deploying SRI for External Analytics Scripts

- **Attack Type**: SRI
- **Target**: Marketing or analytics-enabled websites
- **Vulnerability**: Tampered third-party script
- **MITRE**: T1554
- **Impact**: Blocks unauthorized external code
- **Tools**: SRI Generator, DevTools
- **Scenario**: Ensures external analytics scripts are not tampered
- **Attack Steps**: 1. A marketing script is loaded from an external analytics provider. 2. Security team hashes the script using SHA-384 and adds it to the HTML tag: <script src="..." integrity="sha384-XYZ">. 3. The hash ensures the browser verifies the file hasn't been altered. 4. If the file changes, the browser blocks it instead of running unknown code. 5. Red team tests CDN manipulation and observes it fails due to mismatched integrity. 6. CI pipeline enforces integrity regeneration if versions change. 7. Monitoring includes alerts on integrity violations during browsing sessions.
- **Detection**: Browser console & blocked requests
- **Solution**: Enforce SRI hash with each third-party inclusion
- **Tags**: #AnalyticsSecurity #SRI #IntegrityCheck

## Implementing Output Encoding in Java-Based Web Apps

- **Attack Type**: Input Escaping
- **Target**: Java-based enterprise apps
- **Vulnerability**: Script injection in templates
- **MITRE**: T1059.007
- **Impact**: Prevents client-side payload execution
- **Tools**: OWASP Java Encoder, JSP
- **Scenario**: Avoids XSS in Java JSP or Thymeleaf templates
- **Attack Steps**: 1. Developers output user-provided data in Java templates using encoding libraries (<c:out> or @{htmlEscape} in Thymeleaf). 2. Output encoding ensures <script> is shown as &lt;script&gt;, neutralizing execution. 3. Legacy code using direct variable output is replaced with encoding-aware helpers. 4. QA team injects payloads like <img src=x onerror=alert(1)> to verify it's shown as plain text. 5. Automated tests check common XSS vectors across the app. 6. Encoders are integrated into build pipeline for enforcement. 7. Backend rendering sanitizes all outbound HTML content.
- **Detection**: HTML output inspection & automated test cases
- **Solution**: Apply encoding for all untrusted output
- **Tags**: #JavaSecurity #JSPXSS #EscapeOutput

## Using CSP with frame-ancestors to Prevent Embedding

- **Attack Type**: CSP
- **Target**: Financial or profile settings pages
- **Vulnerability**: Clickjacking via framing
- **MITRE**: T1110.003
- **Impact**: Eliminates hidden UI attack surfaces
- **Tools**: CSP Policy, Browser Dev Tools
- **Scenario**: Stops clickjacking by preventing iframe embedding
- **Attack Steps**: 1. The CSP header includes frame-ancestors 'none'; which overrides older X-Frame-Options. 2. This directive blocks all attempts to embed the site in iframes—even from the same origin. 3. Security tests attempt clickjacking via hidden <iframe> layers but browser blocks rendering. 4. The policy applies to all sensitive pages (e.g., profile, payments, admin). 5. CSP logs are monitored to detect framing attempts. 6. CSP is validated in staging before production deployment. 7. Hardens framing restrictions against UI redress attacks.
- **Detection**: Browser developer tools, error reports
- **Solution**: Use frame-ancestors CSP for strong embedding rules
- **Tags**: #CSP #Clickjacking #IframeProtection

## HTML Sanitization in React via DOMPurify

- **Attack Type**: Input Sanitization
- **Target**: React apps with rich input
- **Vulnerability**: Rich text script injection
- **MITRE**: T1059.007
- **Impact**: Prevents stored or reflected XSS
- **Tools**: DOMPurify, React
- **Scenario**: Removes dangerous HTML from content-rich inputs
- **Attack Steps**: 1. The app allows rich text input using WYSIWYG editors. 2. Before rendering, HTML is passed through DOMPurify.sanitize() to remove malicious tags. 3. Payloads like <script>, onerror, javascript: are stripped out. 4. React then safely renders the sanitized HTML using dangerouslySetInnerHTML. 5. Red teamers validate by submitting test payloads to verify nothing executes. 6. The sanitizer is updated regularly to prevent bypasses. 7. Protection works across comment sections, profiles, and blogs.
- **Detection**: Rendered output and DOM comparison
- **Solution**: Sanitize input before render using DOMPurify
- **Tags**: #DOMPurify #ReactXSS #RichTextSecurity

## Blocking Untrusted Scripts via Strict CSP

- **Attack Type**: CSP
- **Target**: All web applications
- **Vulnerability**: Unauthorized external script execution
- **MITRE**: T1554
- **Impact**: Enforces strict source policy
- **Tools**: CSP Evaluator, HTTP Headers
- **Scenario**: Allows only self-hosted and verified scripts
- **Attack Steps**: 1. Security team sets a strict CSP header: script-src 'self'; or includes whitelisted CDNs only. 2. This blocks third-party scripts injected via browser extensions, MITM, or malicious plugins. 3. Payloads hosted on attacker-controlled domains fail to execute. 4. Team confirms enforcement by injecting scripts in URL parameters and HTML fields. 5. CSP violations are logged via report-uri. 6. Over time, domains are audited to avoid overly permissive policies. 7. Prevents cross-domain and drive-by script attacks.
- **Detection**: Monitor browser logs & report-uri endpoint
- **Solution**: Allow only whitelisted script-src in CSP
- **Tags**: #StrictCSP #ScriptHardening #SourceControl

## CSP for Blocking Inline Event Handlers

- **Attack Type**: CSP
- **Target**: Web apps with user-submitted content
- **Vulnerability**: Inline event-driven script injection
- **MITRE**: T1059.007
- **Impact**: Blocks multiple entry points for XSS
- **Tools**: Dev Console, CSP Policy
- **Scenario**: Blocks inline JavaScript like onclick, onerror, etc.
- **Attack Steps**: 1. CSP is configured to disallow inline event handlers: script-src 'self'; object-src 'none';. 2. Attackers try to inject <img src=x onerror=alert(1)> but execution fails. 3. Scripts with event-based triggers (onclick, onload) are rendered inert. 4. Frontend is refactored to use external JS handlers or addEventListener. 5. CSP violations are logged and reviewed for persistent injection attempts. 6. Developers test fallback UI with strict policy to ensure usability. 7. This locks down event-driven XSS vectors.
- **Detection**: Observe CSP error logs and failed event triggers
- **Solution**: Avoid inline event attributes; use listeners
- **Tags**: #InlineBlocking #EventSecurity #NoOnclick

## Rejecting Tainted JavaScript via Trusted Types

- **Attack Type**: Browser Policy
- **Target**: JavaScript SPAs
- **Vulnerability**: DOM sink exploitation
- **MITRE**: T1059.007
- **Impact**: Browser enforces JS origin checks
- **Tools**: Chrome Trusted Types
- **Scenario**: Browser-level policy preventing untrusted dynamic JS
- **Attack Steps**: 1. Trusted Types are enabled in the browser via CSP. 2. Legacy JS functions like innerHTML, document.write, or eval() are wrapped with enforcement. 3. Only values created by a registered Trusted Types policy can be assigned to DOM sinks. 4. If a malicious payload reaches innerHTML without sanitization, the browser blocks it. 5. Teams refactor risky assignments into approved wrappers using DOMPurify or custom policies. 6. Any unregistered sink usage throws runtime errors. 7. Trusted Types add a strong client-side defense layer against DOM-based XSS.
- **Detection**: Browser dev console & policy violations
- **Solution**: Register and enforce trusted policies
- **Tags**: #TrustedTypes #DOMEnforcement #BrowserPolicy

## Logging and Monitoring SRI Failures

- **Attack Type**: SRI
- **Target**: Sites with CDNs
- **Vulnerability**: Script modification or outdated hash
- **MITRE**: T1554
- **Impact**: Detects silent tampering of libraries
- **Tools**: Browser Logs, SIEM
- **Scenario**: Detects tampering or failure in loading third-party resources
- **Attack Steps**: 1. SRI is configured on all CDN-loaded scripts and styles. 2. When an integrity hash mismatch occurs, the browser blocks the resource and logs an error. 3. Browser logs are sent to a central SIEM platform like Splunk. 4. Frequent SRI failures are investigated for potential CDN compromise or outdated hashes. 5. Security team receives alerts when resources fail to load due to mismatches. 6. Developers test intentional mismatches in staging to verify logging. 7. This proactive alerting helps detect JS supply chain tampering.
- **Detection**: Monitor console and alert via SIEM
- **Solution**: Set up alerts for integrity errors
- **Tags**: #SRIAlerts #ScriptMonitoring #SupplyChainSecurity

## Escaping Dynamic Content in AngularJS Safely

- **Attack Type**: Input Escaping
- **Target**: Angular web apps
- **Vulnerability**: Template injection in dynamic views
- **MITRE**: T1059.007
- **Impact**: Prevents stored or DOM-based XSS
- **Tools**: AngularJS, BypassSecurityTrust
- **Scenario**: Avoids untrusted HTML injection in dynamic Angular views
- **Attack Steps**: 1. Angular automatically escapes data binding values using {{ value }} syntax. 2. Developers avoid unsafe directives like ng-bind-html unless sanitized with DomSanitizer. 3. HTML input is passed through bypassSecurityTrustHtml() only when verified safe. 4. Red teamers test payloads in templates and observe they are shown as text, not rendered. 5. Template injection vulnerabilities are tested and blocked. 6. Secure coding guidelines enforced across team. 7. Legacy code is migrated to use safe binding.
- **Detection**: Render checks & Angular warnings
- **Solution**: Avoid unsafe binding unless sanitized
- **Tags**: #AngularXSS #DomSanitizer #TemplateSecurity

## Combining Input Validation and Output Encoding

- **Attack Type**: Input Sanitization + Output Escaping
- **Target**: Full-stack apps
- **Vulnerability**: Incomplete sanitization at either end
- **MITRE**: T1059.007
- **Impact**: Comprehensive input-output security
- **Tools**: Server Validator, JS Escape Libraries
- **Scenario**: Ensures safe handling of user input throughout pipeline
- **Attack Steps**: 1. Input validation occurs on server side using schema (e.g., username max 30 chars, no script tags). 2. Validated input is still considered untrusted at output time. 3. Before rendering to browser, input is passed through encoding libraries (htmlEncode, .textContent, etc.). 4. XSS payloads like <script>alert(1)</script> are both blocked at input and encoded at output. 5. Double-layer approach covers both trusted and untrusted input paths. 6. QA team verifies scenarios where filters fail — encoded outputs still prevent harm. 7. Input/output defense strategy ensures robust front-back XSS protection.
- **Detection**: Functional testing & code review
- **Solution**: Always validate + encode user inputs
- **Tags**: #EncodeEscapeValidate #DefenseInDepth

## Limiting Script Execution with Nonce-Based CSP

- **Attack Type**: CSP
- **Target**: Web applications with dynamic scripts
- **Vulnerability**: Inline script injection
- **MITRE**: T1059.007
- **Impact**: Blocks injected scripts in inline tags
- **Tools**: Secure CSP Config, Browser Dev Tools
- **Scenario**: Uses dynamically generated nonces to authorize inline scripts
- **Attack Steps**: 1. The CSP is configured with script-src 'nonce-xyz'; where xyz is a unique, random value generated per request. 2. Inline scripts are only allowed if they contain a matching nonce attribute (e.g., <script nonce="xyz">...). 3. This prevents attackers from injecting unauthorized scripts even via inline tags. 4. Web server dynamically injects the nonce into both headers and script tags. 5. Red team attempts injection without the nonce and fails. 6. Security monitors CSP violation reports for any unauthorized script attempts. 7. This mechanism reduces the reliance on 'unsafe-inline' and tightens script execution policies.
- **Detection**: Monitor CSP violations and test nonce mismatches
- **Solution**: Apply per-request nonce headers to authorize scripts
- **Tags**: #NonceCSP #InlineSecurity #DynamicCSP

## Sanitizing Query Parameters in React Router

- **Attack Type**: Input Sanitization
- **Target**: Single-page applications
- **Vulnerability**: Script injection via query string
- **MITRE**: T1059.007
- **Impact**: Prevents dynamic XSS via URLs
- **Tools**: React Router, DOMPurify
- **Scenario**: Ensures untrusted query params don’t affect rendering or logic
- **Attack Steps**: 1. The app reads query parameters for filters and navigation in React Router. 2. Malicious users attempt to inject payloads like <script> or JavaScript code via URL. 3. Developers sanitize parameters using utilities like DOMPurify or simple character escaping before usage. 4. Any dynamic rendering based on query strings is wrapped in dangerouslySetInnerHTML only after sanitization. 5. Red team injects complex XSS vectors; all are displayed as harmless text. 6. Automated tests validate that rendering logic does not reflect scripts. 7. Combined input handling and sanitization prevent XSS via URLs.
- **Detection**: Manual and automated XSS tests
- **Solution**: Sanitize all query-derived content
- **Tags**: #ReactSanitize #QuerySecurity #SPAXSS

## Defending Against Evercookie Using Storage Isolation

- **Attack Type**: Tracking Defense
- **Target**: Browsers and web apps
- **Vulnerability**: Evercookie-based persistent tracking
- **MITRE**: T1606
- **Impact**: Eliminates tracking data redundancy
- **Tools**: Privacy Badger, Browser Dev Settings
- **Scenario**: Stops persistent tracking by clearing and isolating all storage
- **Attack Steps**: 1. Browsers can be configured or extended to block Evercookie techniques that store identifiers in multiple locations (cookies, ETags, localStorage, Flash). 2. Privacy-focused browsers (Brave, Firefox) isolate storage per origin and clear on session end. 3. Admins ensure storage APIs like localStorage and IndexedDB are cleared via logout hooks. 4. Sites use Cache-Control: no-store headers to avoid ETag-based tracking. 5. Security team tests persistence by logging in and refreshing across sessions. 6. No identifiers remain when storage is cleared manually or automatically. 7. Prevents cross-site tracking by fingerprint-resistant policies.
- **Detection**: Inspect dev tools for residual data
- **Solution**: Implement full storage isolation & clearing
- **Tags**: #TrackingDefense #EvercookieMitigation #BrowserPrivacy

## CSP Violation Alerting via SIEM Integration

- **Attack Type**: CSP
- **Target**: Corporate apps with user inputs
- **Vulnerability**: CSP-bypassing attempts
- **MITRE**: T1203
- **Impact**: Detects script abuse in real time
- **Tools**: SIEM (Splunk, ELK), CSP Reporting
- **Scenario**: Centralized logging of CSP policy breaches
- **Attack Steps**: 1. Security team configures the CSP header with a report-uri or report-to directive pointing to an internal logging service. 2. When a script or resource violates policy, the browser sends a JSON report to that endpoint. 3. Logs include blocked URI, violated directive, and user agent details. 4. SIEM tools ingest the data and visualize patterns or repeated attack attempts. 5. Alerts are triggered on spikes in violation counts. 6. Analysts investigate violation trends and patch CSP or app behavior. 7. This setup enhances visibility into client-side enforcement of security policies.
- **Detection**: SIEM dashboards, CSP report logs
- **Solution**: Forward browser CSP reports to logging infra
- **Tags**: #SIEMCSP #CSPAlerting #WebLogging

## Validating and Escaping Usernames in Web Forms

- **Attack Type**: Input Validation + Escaping
- **Target**: Authentication forms
- **Vulnerability**: Unsafe user-provided input
- **MITRE**: T1059.007
- **Impact**: Blocks harmful content in identity fields
- **Tools**: Express.js, Validator.js, DOM Encoder
- **Scenario**: Prevents XSS by validating username fields server-side and escaping client-side
- **Attack Steps**: 1. Usernames submitted in registration and login forms are validated using length and allowed character rules. 2. Backend rejects input containing tags or suspicious characters. 3. During rendering, usernames are encoded using HTML escaping (&lt;, &gt;, etc.). 4. A user attempting to sign up with "><script>alert(1)</script> gets blocked at validation. 5. QA runs fuzz tests to attempt bypassing filters. 6. The frontend escape layer ensures nothing harmful renders even if validation is weak. 7. This layered approach defends against stored and reflected XSS.
- **Detection**: Manual review & auto-fuzzing
- **Solution**: Validate + encode input on both ends
- **Tags**: #FormSecurity #UsernameSanitization #XSSHardening

## Enforcing HTTPS with HSTS Header Deployment

- **Attack Type**: Header Hardening
- **Target**: Public-facing websites
- **Vulnerability**: SSL stripping & downgrade attacks
- **MITRE**: T1573
- **Impact**: Forces secure channel use
- **Tools**: SecurityHeaders.io, curl
- **Scenario**: Forces all future traffic over HTTPS to prevent downgrade attacks
- **Attack Steps**: 1. Admin adds Strict-Transport-Security: max-age=63072000; includeSubDomains; preload to response headers. 2. This instructs the browser to always access the site via HTTPS—even if user types http://. 3. This protects against SSL stripping attacks on public Wi-Fi or MITM proxies. 4. The domain is submitted to HSTS preload list for major browsers. 5. QA checks header presence via curl and browser dev tools. 6. Red team tests downgrade attempts and all fail. 7. This enforces encrypted traffic and eliminates accidental insecure access.
- **Detection**: Inspect headers via tools
- **Solution**: Add HSTS header with long expiry
- **Tags**: #HSTS #HeaderSecurity #HTTPSOnly

## Disabling Inline Scripts via Meta Tag CSP

- **Attack Type**: CSP
- **Target**: Legacy or static sites
- **Vulnerability**: Inline JS injection
- **MITRE**: T1059.007
- **Impact**: Blocks injected inline JS
- **Tools**: Meta CSP Tag, Browser Inspector
- **Scenario**: Prevents inline script execution through <meta> tags
- **Attack Steps**: 1. Some legacy apps can’t modify server headers easily, so developers use <meta http-equiv="Content-Security-Policy" content="script-src 'self'">. 2. This enforces a CSP directly from within HTML. 3. Any attempt to insert inline <script> without CSP exception will be blocked. 4. Testers inject javascript: URLs and observe failures. 5. Browser logs show CSP enforcement from the meta tag. 6. Frontend team avoids unsafe patterns and uses external scripts only. 7. Works best for static HTML environments.
- **Detection**: Browser dev tools console
- **Solution**: Use <meta> CSP when headers unavailable
- **Tags**: #MetaCSP #InlinePrevention #StaticSiteSecurity

## Real-Time Script Block Alert via Browser Extension

- **Attack Type**: Browser Extension Defense
- **Target**: Client-side apps
- **Vulnerability**: CSP or SRI bypass attempts
- **MITRE**: T1554
- **Impact**: Confirms script rejection at runtime
- **Tools**: uBlock Origin, CSP Logger
- **Scenario**: Detects and logs scripts blocked by CSP or SRI at runtime
- **Attack Steps**: 1. Teams deploy browser extensions like CSP Logger or privacy plugins during testing. 2. These tools notify when any inline, external, or eval-based script is blocked. 3. Developers identify policy violations or overblocking by analyzing extension logs. 4. Red team simulates attacks to verify whether CSP or SRI kicks in. 5. Alerts include blocked script URLs and directive violated. 6. The data helps refine CSP rules without breaking functionality. 7. Security analysts incorporate logs into policy audits.
- **Detection**: Browser extensions for monitoring
- **Solution**: Use extensions to test/adjust policy enforcement
- **Tags**: #BrowserDefense #CSPMonitor #ClientPolicyAudit

## Hardening <iframe> Sandbox for Embedded Widgets

- **Attack Type**: HTML Hardening
- **Target**: Sites with third-party embeds
- **Vulnerability**: Privilege escalation via iframe
- **MITRE**: T1548
- **Impact**: Blocks widget-based malicious actions
- **Tools**: HTML sandbox attribute, Dev Console
- **Scenario**: Restricts capabilities of embedded third-party widgets
- **Attack Steps**: 1. Widgets embedded via <iframe> (e.g., chat boxes, ads) use sandbox attributes to limit actions. 2. Attributes like sandbox="allow-scripts allow-same-origin" can be fine-tuned. 3. Developers remove permissions such as allow-forms, allow-top-navigation, etc. to reduce risk. 4. Attacks attempting to break out of iframe or redirect parent window are blocked. 5. Tests show embedded content fails to execute unwanted behaviors. 6. Security team monitors if any widget attempts privilege escalation. 7. Strong sandboxing protects site even when embedding unknown sources.
- **Detection**: Inspect iframe behavior in dev tools
- **Solution**: Use strict iframe sandbox attributes
- **Tags**: #IframeSecurity #Sandboxing #WidgetDefense

## Enforcing JavaScript MIME Type Checks

- **Attack Type**: Header Hardening
- **Target**: Static and dynamic JS servers
- **Vulnerability**: Content-type sniffing bypass
- **MITRE**: T1203
- **Impact**: Blocks MIME mismatch execution
- **Tools**: HTTP Headers, MIME Testers
- **Scenario**: Prevents execution of files not served with correct Content-Type
- **Attack Steps**: 1. Web servers are configured to serve JS files with Content-Type: application/javascript. 2. Browsers are prevented from executing files with mismatched MIME types via X-Content-Type-Options: nosniff. 3. This defends against files disguised as scripts. 4. Testers serve .jpg file containing JS and observe it fails to execute. 5. Sites using content from untrusted sources are double-checked. 6. CI/CD pipelines verify MIME headers before deploying assets. 7. This hardening step neutralizes content-type confusion attacks.
- **Detection**: Curl headers, browser dev tools
- **Solution**: Enforce MIME headers + nosniff option
- **Tags**: #MIMESecurity #Nosniff #TypeValidation

