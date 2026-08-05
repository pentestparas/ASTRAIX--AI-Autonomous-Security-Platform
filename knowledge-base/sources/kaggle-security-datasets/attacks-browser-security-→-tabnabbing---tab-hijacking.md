# Browser Security → Tabnabbing / Tab Hijacking Attacks

## Idle Tab Replaced with Fake Gmail Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Email Users
- **Vulnerability**: Trust in idle browser tab state
- **MITRE**: T1189
- **Impact**: Credential theft
- **Tools**: HTML, JavaScript
- **Scenario**: When user switches tabs, the inactive one changes to mimic Gmail login
- **Attack Steps**: 1. The attacker creates a legitimate-looking site such as a blog or news article to encourage users to keep it open. 2. A JavaScript function tracks user activity with the blur event (when tab loses focus) and uses setTimeout to wait for inactivity. 3. After a delay (e.g., 30 seconds), the script dynamically rewrites the page’s document.body.innerHTML to display a perfect replica of the Gmail login page. 4. When the user returns to the tab and sees the login form, they assume they were logged out due to inactivity. 5. They re-enter their credentials, which are then captured by the attacker and sent to a malicious endpoint using fetch() or XMLHttpRequest. 6. The attacker displays a fake error like “Incorrect password. Please try again” to cover tracks. 7. Meanwhile, the attacker logs into the real Gmail account using the stolen credentials.
- **Detection**: Detect script changes to DOM after inactivity
- **Solution**: Use visual browser indicators and enforce login URL validation
- **Tags**: #tabnabbing #gmailphishing #jsreplacetab

## Banking Tab Changes to Phishing Page

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Online Banking Users
- **Vulnerability**: Tab-based phishing via idle tab replacement
- **MITRE**: T1189
- **Impact**: Financial account compromise
- **Tools**: HTML, JS
- **Scenario**: Inactive bank tab replaced with cloned login to trick re-login
- **Attack Steps**: 1. A site mimicking a financial article or calculator is used to lure users into opening and switching tabs. 2. Once the user shifts focus, JavaScript triggers a timer using setTimeout and document.hidden. 3. After about 1 minute of inactivity, the entire DOM is overwritten to display a fake banking login (e.g., “Session timed out. Please log in again”). 4. The page design, logos, and domain spoof (via Unicode or similar) resemble the bank’s actual login interface. 5. The victim, thinking it’s the same site, enters their credentials. 6. Data is exfiltrated instantly, and the tab either refreshes or shows a fake “Try again later” message. 7. Meanwhile, the attacker uses those credentials for real-time fraudulent transactions.
- **Detection**: Heuristic scan for idle tab manipulation
- **Solution**: Use two-factor login and anti-phishing login pages
- **Tags**: #banktabnabbing #sessionfake #domhijack

## Fake Social Media Re-login via Tab Swap

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Social Media Users
- **Vulnerability**: Inactive tab swapped with phishing clone
- **MITRE**: T1189
- **Impact**: Identity theft, phishing spread
- **Tools**: HTML, JavaScript
- **Scenario**: Idle tab reloaded as Facebook login to steal credentials
- **Attack Steps**: 1. The attacker builds a fake news site embedded with JavaScript that waits for tab inactivity using document.hidden. 2. When the user switches tabs for a few seconds, the script replaces the DOM with a cloned Facebook login page. 3. It includes a fake URL using Unicode or special characters (e.g., “faceb00k.com” with double zeroes) in the address bar. 4. The form accepts username/password and submits to the attacker’s server. 5. A fake login error is shown to avoid suspicion. 6. The attacker logs into the victim’s real Facebook and performs actions such as sending malicious messages to friends.
- **Detection**: Monitor tab change + suspicious DOM events
- **Solution**: Educate users about address bar validation
- **Tags**: #facebookphish #unicodeurl #clicktheft

## Developer Tool Site Turns into GitHub Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Developers
- **Vulnerability**: Developer trust in idle site tabs
- **MITRE**: T1189
- **Impact**: Source code or token leakage
- **Tools**: HTML, JS
- **Scenario**: Code snippet site hijacks tab after idle to collect GitHub credentials
- **Attack Steps**: 1. The user visits a developer site that hosts code snippets and copy/paste tools. 2. The attacker places a script that activates on tab switch (blur event). 3. After 20–30 seconds, the page is replaced with a GitHub login prompt claiming the session expired. 4. This cloned login box is styled exactly like GitHub, but posts credentials to the attacker’s server. 5. Upon submission, the page may show “Incorrect password” and reset the form. 6. The attacker uses the stolen GitHub credentials to steal code, tokens, or modify CI pipelines.
- **Detection**: Track GitHub credential submission from non-github.com
- **Solution**: Enable SSO and FIDO2 for GitHub login
- **Tags**: #devphishing #githijack #idletabattack

## Online Store Tab Becomes PayPal Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: E-commerce Shoppers
- **Vulnerability**: False login prompt on idle shopping tabs
- **MITRE**: T1189
- **Impact**: Payment fraud, account takeover
- **Tools**: JS, HTML, Fake Form
- **Scenario**: Idle shopping tab replaced with fake PayPal login
- **Attack Steps**: 1. A fake online store is set up offering heavy discounts. 2. While shopping, users often switch tabs to compare prices. 3. JavaScript detects visibilitychange and blur, and starts a timer. 4. Once the user leaves the tab for 45+ seconds, the page content is replaced with a fake PayPal login window. 5. The design mimics PayPal’s branding and asks the user to re-login to complete payment. 6. Entered credentials are sent to the attacker. 7. Victims think payment failed and move on, unaware their credentials are stolen. 8. The attacker later uses the credentials for unauthorized purchases.
- **Detection**: Monitor repeated DOM rewrites and form submission after blur
- **Solution**: Implement PayPal’s anti-iframe and CSP protections
- **Tags**: #paypalphish #clicktheft #fakesession

## window.opener Used to Redirect Original Tab

- **Attack Type**: window.opener Abuse
- **Target**: Webmail Users
- **Vulnerability**: Unrestricted access via opener object
- **MITRE**: T1189
- **Impact**: Email phishing, session theft
- **Tools**: JavaScript window.opener
- **Scenario**: Attacker-controlled tab modifies parent tab to show phishing content
- **Attack Steps**: 1. A phishing email links to a seemingly legit blog site that opens in a new tab (target="_blank"). 2. Once opened, the new tab runs a script using window.opener.location.replace() to change the original tab to a fake login page. 3. The parent tab (from where the link was clicked) now displays a cloned login screen (e.g., Office365). 4. Since the user originally clicked from their email inbox, the context matches. 5. Victim enters credentials, believing it’s part of login flow. 6. Credentials are sent to the attacker’s server, who then hijacks the email account.
- **Detection**: Detect opener-based redirects
- **Solution**: Use rel="noopener noreferrer" on all target="_blank" links
- **Tags**: #windowopener #parenthijack #emailphishing

## Job Portal Tab Swaps to LinkedIn Clone

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Job Seekers
- **Vulnerability**: Idle tab transformed into trusted social login
- **MITRE**: T1189
- **Impact**: Identity theft, job fraud
- **Tools**: JavaScript, CSS
- **Scenario**: Idle job site tab changes to a LinkedIn login screen
- **Attack Steps**: 1. An attacker clones a legitimate-looking job search site with listings and resume tools. 2. Once users switch tabs, JavaScript uses document.hidden to monitor tab inactivity. 3. After delay, tab content changes to a LinkedIn login page with realistic styling. 4. Victims think the session expired and re-enter their login. 5. Attackers use the credentials to scrape private contacts, job applications, or spam messages. 6. Sometimes, attackers offer job scams using victim’s LinkedIn account.
- **Detection**: Monitor multiple login attempts from fake domains
- **Solution**: Encourage password managers that validate URLs
- **Tags**: #linkedinphish #tabclone #jobscam

## Inactive Browser Game Tab Loads Steam Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Gamers
- **Vulnerability**: Tab content swap with familiar game login
- **MITRE**: T1189
- **Impact**: Account hijack, virtual goods theft
- **Tools**: HTML, Steam Assets
- **Scenario**: Fake gaming tab shows Steam login to steal credentials
- **Attack Steps**: 1. A casual browser game invites users to register and play. 2. After playing briefly, user switches tab. 3. Tab detects loss of focus and delays 60 seconds. 4. DOM is replaced with a Steam login page — styled using Steam’s public CSS assets. 5. The message “Your session expired, please re-authenticate” is shown. 6. User re-enters their credentials, which are exfiltrated. 7. Attacker sells Steam accounts on black markets or steals in-game assets.
- **Detection**: Audit Steam login referrers
- **Solution**: Use Steam Guard 2FA and allowlist login domains
- **Tags**: #steamphish #gamertargeting #tabnabbing

## Cryptocurrency News Tab Replaces with Wallet Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Crypto Investors
- **Vulnerability**: Wallet UI swapped after tab blur
- **MITRE**: T1189
- **Impact**: Wallet theft, asset drain
- **Tools**: MetaMask, HTML, JS
- **Scenario**: Tab with DeFi news replaced by Web3 wallet login
- **Attack Steps**: 1. The user opens a page offering “DeFi Yield Tips” and switches tabs. 2. A script tracks inactivity using visibilitychange. 3. The content is replaced with a fake MetaMask unlock screen. 4. Victim enters seed phrase or password, thinking their session timed out. 5. Credentials are sent to attacker, who imports the wallet and drains funds. 6. Many users confuse tab switching with session timeout, especially in DeFi interfaces.
- **Detection**: Block wallet UI outside trusted extensions
- **Solution**: Educate users never to type seed in browser
- **Tags**: #web3phishing #walletdrain #cryptotrap

## Online Class Tab Transforms into Zoom Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Students, Teachers
- **Vulnerability**: Idle tab trust exploited in edu context
- **MITRE**: T1189
- **Impact**: Privacy breach, credential reuse
- **Tools**: HTML, Zoom UI Clone
- **Scenario**: Inactive education tab replaced with Zoom login clone
- **Attack Steps**: 1. A fake e-learning page provides video links to recorded lectures. 2. Students often multitask, switching tabs to take notes. 3. Script waits for blur and swaps content with a Zoom login screen. 4. Message says: “Your Zoom session expired, please re-login.” 5. Victim enters their Zoom credentials which are sent to attacker. 6. Attacker may enter classes to spy or record meetings, or pivot to other accounts.
- **Detection**: Heuristic scanning for fake Zoom logins
- **Solution**: Enforce SSO and phishing warnings in Zoom
- **Tags**: #zoomphishing #edusecurity #sessiontrap

## News Site Tab Morphs into Outlook Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Webmail Users
- **Vulnerability**: Idle tab turns into Microsoft phishing page
- **MITRE**: T1189
- **Impact**: Email compromise, MFA bypass attempt
- **Tools**: HTML, JavaScript
- **Scenario**: News blog tab replaced with Outlook phishing page after inactivity
- **Attack Steps**: 1. A user visits a “Breaking News” website with a sensational headline to keep them interested. 2. The attacker’s JavaScript code monitors tab visibility using the document.hidden API. 3. As soon as the user switches tabs or minimizes the window, a timer is triggered. 4. After 40–60 seconds, the script completely replaces the DOM with a cloned Outlook login page. 5. The fake page says, “Your session expired. Please re-login to continue reading.” 6. The victim, seeing the Microsoft design and URL spoof (like out1ook-security.com), assumes it's valid and enters their credentials. 7. Credentials are captured and sent to the attacker's server. 8. A fake “Login error” message is shown to prevent suspicion, while the attacker logs in to the actual Outlook account.
- **Detection**: Monitor tab content replacement patterns
- **Solution**: Train users to validate domain spelling and logos
- **Tags**: #outlookphish #tabtrap #mfaevade

## Cloud Storage Tab Swaps to Dropbox Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Cloud Storage Users
- **Vulnerability**: Inactive tab made to appear as session timeout
- **MITRE**: T1189
- **Impact**: Document theft, data exposure
- **Tools**: HTML, Dropbox Clone
- **Scenario**: Tab changes into fake Dropbox login when user returns
- **Attack Steps**: 1. The attacker hosts a fake tech support forum where users leave tabs open for solutions. 2. When the user shifts to another tab, the site uses visibilitychange and blur to detect inactivity. 3. After 90 seconds, the page is changed into a fake Dropbox login using accurate styling and branding. 4. The victim, thinking they’ve been logged out, types in their Dropbox email and password. 5. Credentials are sent to a malicious server. 6. The attacker then accesses the Dropbox account to download sensitive files. 7. The user is shown a fake “Wrong password” alert or redirected to the real Dropbox to reduce suspicion.
- **Detection**: Audit Dropbox login activity and IP addresses
- **Solution**: Enforce time-limited session tokens and 2FA
- **Tags**: #dropboxphishing #tabnabbing #clickfraud

## window.opener Used to Redirect Crypto Site

- **Attack Type**: window.opener Abuse
- **Target**: Crypto Users
- **Vulnerability**: Original tab compromised via opener object
- **MITRE**: T1189
- **Impact**: Wallet hijack, DeFi fraud
- **Tools**: JavaScript
- **Scenario**: Attacker opens tab and changes original crypto tab to fake wallet login
- **Attack Steps**: 1. User visits a crypto news aggregator that links to many external crypto tools. 2. Clicking a link to an external site opens in a new tab (target="_blank"). 3. The attacker site uses window.opener.location to silently redirect the original tab to a fake MetaMask login page. 4. The new tab remains idle while the user focuses on the original tab, now changed. 5. Thinking they’ve returned to the login page, the victim enters wallet credentials or seed phrase. 6. These are sent to the attacker who instantly drains tokens or NFTs. 7. This attack leverages trust in the original site to redirect and deceive the user.
- **Detection**: Enforce rel="noopener" on external links
- **Solution**: Block MetaMask login on non-extension interfaces
- **Tags**: #metamaskhijack #cryptoattack #tabpoisoning

## Blog Comment Tab Changes to WordPress Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: WordPress Admins
- **Vulnerability**: Phishing via tab replacement on content pages
- **MITRE**: T1189
- **Impact**: Site compromise, SEO malware
- **Tools**: HTML, JavaScript
- **Scenario**: Fake WordPress login shown after user switches tabs from blog
- **Attack Steps**: 1. The user is reading a blog post and switches to another tab. 2. A script detects the user’s absence via document.hidden. 3. After 1 minute, the blog content is dynamically changed to a WordPress login interface. 4. The message “Please log in to comment” appears. 5. The user types their credentials, unaware it’s a fake form. 6. The attacker collects the credentials and attempts access on the real WordPress admin. 7. If successful, the attacker injects malware or SEO spam into the site. 8. This method is especially common on niche forums or personal blogs.
- **Detection**: Use strict domain verification on login actions
- **Solution**: Alert admin on suspicious login attempts
- **Tags**: #wordpressphishing #tabspoof #cmsattack

## Idle Tab Pretends to Be Apple ID Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Apple Users
- **Vulnerability**: Deceptive tab change to familiar brand
- **MITRE**: T1189
- **Impact**: iCloud account theft
- **Tools**: HTML, Apple UI Clone
- **Scenario**: Tab switches to fake Apple login to steal iCloud credentials
- **Attack Steps**: 1. The user opens a tech news article and switches tabs. 2. After 45 seconds of inactivity, the attacker’s JavaScript swaps the tab’s content with a cloned Apple ID login page. 3. It says, “Your session expired due to inactivity. Please log back into your Apple ID.” 4. The user, believing this is legitimate, enters their credentials. 5. These are captured and sent to the attacker. 6. The attacker attempts to log into iCloud or purchase via Apple services. 7. The tab may then show a fake “login failed” error to buy time.
- **Detection**: Monitor sudden DOM changes in content tabs
- **Solution**: Use Apple device 2FA and login alerts
- **Tags**: #appleidphish #icloudfraud #tabmanipulation

## Documentation Tab Changes to Jira Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Developers
- **Vulnerability**: Idle tab exploited to steal DevOps credentials
- **MITRE**: T1189
- **Impact**: CI/CD compromise, internal leaks
- **Tools**: JavaScript, HTML
- **Scenario**: Dev doc site morphs into fake Jira login after idle
- **Attack Steps**: 1. A developer opens API documentation and gets distracted. 2. The page detects inactivity and swaps the DOM with a Jira login interface. 3. “Session expired” is shown to encourage re-authentication. 4. The user enters their Jira credentials, which are exfiltrated. 5. Attacker uses them to access project tickets, credentials, or deploy malware in pipelines. 6. The user only sees a loading spinner or timeout message.
- **Detection**: Log Jira login events from untrusted sources
- **Solution**: Add domain validation before credential entry
- **Tags**: #jiraphishing #devopsattack #tabtrap

## Online Class Material Tab Becomes Google Classroom Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Students
- **Vulnerability**: Educational tabs spoofed into login prompts
- **MITRE**: T1189
- **Impact**: Education system abuse
- **Tools**: JS, Google Classroom UI
- **Scenario**: Class note tab changes to fake Google login
- **Attack Steps**: 1. A student opens a PDF of notes from a school portal. 2. After tab inactivity, the attacker script changes the page to Google Classroom login. 3. “Session timed out” appears, prompting a re-login. 4. Victim enters credentials, which are sent to attacker. 5. Attacker uses them to impersonate student or download sensitive class content.
- **Detection**: Audit Google login from non-classroom.google.com URLs
- **Solution**: Train students in domain awareness
- **Tags**: #studentphishing #googlescam #tabspoof

## Coupon Site Tab Turns Into Amazon Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Shoppers
- **Vulnerability**: Trust in familiar branding post-idle
- **MITRE**: T1189
- **Impact**: Unauthorized purchases
- **Tools**: HTML, CSS, JS
- **Scenario**: Shopping tab morphs into fake Amazon login
- **Attack Steps**: 1. A user clicks into a coupon site for Amazon discounts. 2. After 60 seconds of inactivity, the tab changes to look like Amazon login. 3. Fake domain (amaz0n-deals.com) is used. 4. User enters credentials, attacker logs in and places orders using stored card.
- **Detection**: Monitor fake login attempts, warn on new IP
- **Solution**: Use OTP login on new devices
- **Tags**: #amazonphish #dealbait #credentialfraud

## window.opener Hijack Redirects to Fake Login

- **Attack Type**: window.opener Abuse
- **Target**: Web Users
- **Vulnerability**: Original tab hijacked silently
- **MITRE**: T1189
- **Impact**: Phishing, account compromise
- **Tools**: JavaScript, target="_blank"
- **Scenario**: New tab hijacks and rewrites original tab’s URL
- **Attack Steps**: 1. Clicking a blog’s link opens a new tab. 2. The attacker’s new tab modifies the blog tab using window.opener.location.replace. 3. The old tab becomes a login page for a bank or email service. 4. User retypes password unknowingly.
- **Detection**: Use rel=noopener on all links
- **Solution**: Avoid allowing opener-based redirects
- **Tags**: #openerphish #redirectattack #tabtrap

## Online Forum Tab Replaced with Twitter Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Forum Users
- **Vulnerability**: Familiar UI triggers misplaced trust
- **MITRE**: T1189
- **Impact**: Social media account abuse
- **Tools**: HTML, Twitter UI
- **Scenario**: Tab with forum content turns into Twitter login
- **Attack Steps**: 1. User visits a tech forum and switches tabs. 2. The idle tab is swapped to a Twitter login screen. 3. Victim logs in thinking session expired. 4. Credentials sent to attacker to access or abuse Twitter account.
- **Detection**: Track fake logins from external referrers
- **Solution**: Warn users on suspicious login attempts
- **Tags**: #twitterphish #forummalware #socialspoof

## History API Abuse to Fake Legit Page

- **Attack Type**: History API Abuse
- **Target**: Webmail / Social Users
- **Vulnerability**: Misused browser history functions to mask phishing
- **MITRE**: T1189
- **Impact**: Credential theft
- **Tools**: JavaScript history.pushState
- **Scenario**: Attacker uses JavaScript to modify browser history and show fake login page when tab is revisited
- **Attack Steps**: 1. A legitimate-looking article site uses JavaScript to dynamically load content. 2. After the user reads and switches to another tab, the attacker script calls history.pushState() to change the URL shown in the address bar without reloading the page. 3. Simultaneously, the page content is replaced with a fake login page (e.g., Gmail or Facebook). 4. When the user returns to the tab, they see a familiar-looking URL and a login prompt. 5. Thinking the session expired, they enter credentials. 6. Credentials are sent to attacker-controlled server. 7. A “login failed” message or redirection to the real site hides the attack.
- **Detection**: Monitor use of pushState + DOM changes
- **Solution**: Disable client-side login pages where unnecessary
- **Tags**: #historyAPI #addressspoof #tabtrap

## window.opener Hijack to Steal Bank Credentials

- **Attack Type**: window.opener Exploitation
- **Target**: Banking Users
- **Vulnerability**: Tab context misuse to steal sensitive info
- **MITRE**: T1189
- **Impact**: Financial fraud
- **Tools**: JavaScript, browser tabs
- **Scenario**: Malicious site uses window.opener to redirect original banking tab to phishing page
- **Attack Steps**: 1. A user is logged into their bank in one tab. 2. While browsing another site, a malicious ad or link opens a new tab. 3. The new tab uses window.opener.location.replace() to silently redirect the original bank tab to a fake login form. 4. The fake login page looks like the original and even maintains the same tab title and favicon. 5. The user, returning to the tab, sees the familiar site asking for re-login. 6. They type credentials which are sent to the attacker. 7. The attacker immediately accesses the account or sets up wire transfers.
- **Detection**: Detect unexpected opener usage
- **Solution**: Always use rel="noopener noreferrer"
- **Tags**: #bankphish #windowopener #redirectattack

## Fake Timeout Message Leads to Tabnabbing

- **Attack Type**: Fake Session Timeout
- **Target**: SaaS Users
- **Vulnerability**: Fake timeout flow to simulate legitimacy
- **MITRE**: T1189
- **Impact**: Credential compromise
- **Tools**: HTML, JS
- **Scenario**: Page pretends session expired, encouraging re-login to phishing page
- **Attack Steps**: 1. The attacker sets up a fake news or productivity site. 2. After a set period (e.g., 2 minutes), regardless of user action, a pop-up appears stating: “Your session has timed out. Please log in again.” 3. The entire page refreshes with a phishing login interface, using styles of popular platforms (e.g., Outlook, Slack). 4. The user is convinced it’s a security feature. 5. On entering credentials, they’re harvested and optionally followed by a redirect to the actual login page to avoid suspicion.
- **Detection**: Alert on DOM mutation following inactivity
- **Solution**: Add inactivity detection on server-side, not client
- **Tags**: #faketimeout #phishingsession #tabspoof

## DOM-Based Tab Hijack in Markdown Preview App

- **Attack Type**: DOM Manipulation & UI Spoofing
- **Target**: DevTools Users
- **Vulnerability**: Insecure content rendering in preview tools
- **MITRE**: T1189
- **Impact**: Credential theft, code repo compromise
- **Tools**: Markdown Renderer, JS
- **Scenario**: JavaScript inside markdown injection rewrites page into login screen
- **Attack Steps**: 1. A markdown editor site allows preview of user input. 2. A malicious comment/post includes <script> tags hidden in HTML comments. 3. When the preview is opened, JS is executed, waiting for tab inactivity. 4. The DOM is fully rewritten into a Google or GitHub login clone. 5. Victim enters credentials assuming it’s a session timeout. 6. Attacker collects the credentials and uses them for unauthorized access.
- **Detection**: Sanitize markdown previews
- **Solution**: Disable script execution in rendered content
- **Tags**: #markdownxss #domspoof #previewphish

## Z-Index Overlay for Invisible Tabnabbing

- **Attack Type**: Visual Deception / UI Redressing
- **Target**: General Users
- **Vulnerability**: UI redressing using CSS layer tricks
- **MITRE**: T1202
- **Impact**: UI deception, phishing
- **Tools**: HTML, CSS
- **Scenario**: Fake login UI layered over original page using high z-index
- **Attack Steps**: 1. Attacker creates a blog or utility site that seems harmless. 2. After a few minutes or tab switch, a full-page div is added using CSS with z-index: 9999. 3. This overlay contains a cloned login interface for a popular site (e.g., Dropbox). 4. Although the real site is underneath, the user only sees the phishing UI. 5. They enter their credentials into the top layer form. 6. Form submission sends data to attacker, then removes the overlay.
- **Detection**: Use CSP to prevent untrusted UI overlays
- **Solution**: Warn users when re-login is unexpected
- **Tags**: #zindexphish #overlayattack #uiduplication

## Iframe-Based Credential Stealing via Tab Swap

- **Attack Type**: Iframe-Based Tabnabbing
- **Target**: Any Web User
- **Vulnerability**: Dynamic iframe visibility to simulate re-login
- **MITRE**: T1189
- **Impact**: Credential exfiltration
- **Tools**: HTML, iframe, JS
- **Scenario**: Hidden iframe loads phishing login after inactivity
- **Attack Steps**: 1. A site loads a hidden iframe that points to a phishing page. 2. Initially, this iframe is invisible or off-screen. 3. After user switches tabs or is inactive for 45 seconds, the iframe is styled to appear as the main content. 4. The visible content says “Please reauthenticate,” simulating a timeout. 5. Victim enters credentials in the iframe, which are submitted to a malicious server. 6. Iframe is hidden again to avoid suspicion.
- **Detection**: Block mixed-origin iframe overlays
- **Solution**: Disable credential entry in third-party iframes
- **Tags**: #iframephish #cssswap #phishingtrick

## JavaScript Timer Triggered Click Simulation

- **Attack Type**: Click Simulation via JS
- **Target**: All Internet Users
- **Vulnerability**: Automated click event mimics user action
- **MITRE**: T1204
- **Impact**: Phishing via forced navigation
- **Tools**: JavaScript
- **Scenario**: JS simulates user clicking a phishing link after inactivity
- **Attack Steps**: 1. Attacker site sets a setTimeout() after detecting tab blur or inactivity. 2. After 60 seconds, JavaScript simulates a click (element.click()) on a hidden link to a phishing page. 3. This opens a new tab or redirects current tab to fake login. 4. The user, thinking they returned to the site, logs in again. 5. Attackers capture and misuse the credentials in real time.
- **Detection**: Use Content-Security-Policy and tab activity restrictions
- **Solution**: Block JS-triggered navigation to login pages
- **Tags**: #jsphish #clicksimulation #usertrick

## Unicode Domain Spoof on Idle Tab Reload

- **Attack Type**: URL Bar Spoofing
- **Target**: Financial Users
- **Vulnerability**: Unicode-based visual URL deception
- **MITRE**: T1189
- **Impact**: Account hijack
- **Tools**: Unicode Domains, HTML, JS
- **Scenario**: Fake domain using Unicode characters appears identical to original
- **Attack Steps**: 1. User opens tab to a site like paypal.com. 2. Attacker creates a spoofed domain like раураӏ.com using Cyrillic characters that look identical in browser. 3. After tab blur, script redirects to the fake domain with cloned UI. 4. Victim doesn’t notice URL difference and enters credentials. 5. These are stolen and used immediately.
- **Detection**: Use browser anti-spoofing plugins and DNS checks
- **Solution**: Educate on copycat domains and character warnings
- **Tags**: #idnhomoglyph #urlspoofing #visualfraud

## Fake Chat App Asks Re-Login After Tab Idle

- **Attack Type**: DOM Manipulation & UI Spoofing
- **Target**: Chat App Users
- **Vulnerability**: Misleading reauthentication modals
- **MITRE**: T1189
- **Impact**: Support account theft
- **Tools**: JS, HTML
- **Scenario**: Simulated chat session times out and presents phishing login
- **Attack Steps**: 1. User opens a fake support chat or productivity app. 2. After tab inactivity, chat UI is replaced with a login modal. 3. The modal says “Session expired. Please log back in.” 4. The form submits credentials to the attacker’s server. 5. Afterwards, user sees “Login failed” to avoid suspicion.
- **Detection**: Monitor unexpected DOM mutations
- **Solution**: Require server-validated login only
- **Tags**: #fakechatlogin #phishingchat #domabuse

## Online CV Builder Hijacks Idle Tab to Mimic LinkedIn

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Job Seekers
- **Vulnerability**: LinkedIn trust exploited during resume creation
- **MITRE**: T1189
- **Impact**: Social engineering, impersonation
- **Tools**: JS, HTML, LinkedIn UI
- **Scenario**: Resume builder site fakes LinkedIn login screen after idle
- **Attack Steps**: 1. User opens an online resume builder with embedded LinkedIn logo. 2. Once the user switches tabs, script waits for 45 seconds. 3. Then the page content changes to look like a LinkedIn login, simulating re-authentication. 4. The victim, thinking the integration requires login, enters LinkedIn credentials. 5. Data is sent to attacker, who later abuses profile or messages contacts. 6. Fake error shown post-login to reduce suspicion.
- **Detection**: Track LinkedIn logins from non-linkedin.com origins
- **Solution**: Verify third-party integrations with OAuth
- **Tags**: #resumetrap #linkedinhijack #tabattack

## Public Wi-Fi Login Redirect via Tab Swap

- **Attack Type**: Network-Based Tab Replacement
- **Target**: Public Wi-Fi Users
- **Vulnerability**: Captive portal + idle tab redirection
- **MITRE**: T1189
- **Impact**: Credential theft, network-level phishing
- **Tools**: Public Wi-Fi, HTML, JS
- **Scenario**: Fake Wi-Fi login screen appears via idle tab manipulation on captive portal
- **Attack Steps**: 1. A user connects to a public Wi-Fi hotspot in a coffee shop. 2. The network operator (or attacker) redirects the initial browser session to a captive portal asking for agreement to terms. 3. After the user clicks “Agree,” a seemingly legit page loads (like a news site), which they keep open and switch to another tab. 4. After 60 seconds of inactivity, embedded JavaScript rewrites the entire page into a fake "Login Required" screen using the branding of Gmail, Facebook, or Instagram. 5. The user, thinking the network session expired, re-enters their login credentials. 6. These credentials are exfiltrated to the attacker’s server. 7. The tab then shows a generic error or reloads to conceal the trick.
- **Detection**: Monitor captive portals for unauthorized page rewrites
- **Solution**: Use VPN on public Wi-Fi and avoid entering login info after captive portal
- **Tags**: #wifiattack #tabspoof #captiveportal

## Online Resume Editor Swaps to Outlook Login

- **Attack Type**: UI Overlay with Delayed Swap
- **Target**: Job Seekers
- **Vulnerability**: UI trust abuse via session timeout mimicry
- **MITRE**: T1189
- **Impact**: Email compromise, lateral phishing
- **Tools**: HTML, JavaScript
- **Scenario**: Resume editor replaces form with fake Outlook login after tab idle
- **Attack Steps**: 1. The victim opens an online CV or resume editor to create a professional profile. 2. While switching to other tabs (maybe to search for job titles), a background JavaScript timer is triggered via blur and setTimeout. 3. After 60–90 seconds, the editing interface is replaced with a professional-looking Outlook login form, claiming that the session timed out due to inactivity. 4. Since users associate resume tools with email integration, they assume this login prompt is genuine. 5. The attacker collects the email credentials silently and logs into the account, looking for sensitive resume data or contacts to phish further. 6. The page may then display a “Login failed. Try again later” message or reload the original editor.
- **Detection**: Monitor login forms that appear without user action
- **Solution**: Avoid embedding login pages in 3rd-party forms
- **Tags**: #outlookphish #resumetrap #socialengineering

## Blog Post Tab Reloads as Fake GitHub Login

- **Attack Type**: JavaScript-Based Content Rewrite
- **Target**: Developers
- **Vulnerability**: Developer site trust + fake sync prompt
- **MITRE**: T1189
- **Impact**: GitHub account compromise
- **Tools**: HTML, GitHub Clone, JS
- **Scenario**: Developer blog uses DOM rewrite to load GitHub login after idle
- **Attack Steps**: 1. A user visits a programming blog with a helpful code snippet. 2. The tab is left open while the user copies the code into their IDE. 3. JavaScript listens for inactivity using document.hidden or blur. 4. After 2 minutes, the page’s content is rewritten using document.body.innerHTML to show a GitHub login clone. 5. A message like “Login again to sync Gists” is shown. 6. Victim enters GitHub credentials, which are silently posted to the attacker’s backend. 7. Attacker accesses private repos, secrets, or API tokens.
- **Detection**: Track user-agent strings on GitHub logins
- **Solution**: Use passwordless or SSO for GitHub access
- **Tags**: #devphish #githubspoof #tabrewrite

## Browser Extension Misuses Tabs API to Hijack Original Tab

- **Attack Type**: Extension-Based Tab Hijack
- **Target**: General Users
- **Vulnerability**: Abuse of browser extension APIs
- **MITRE**: T1176
- **Impact**: Stealthy phishing using browser privileges
- **Tools**: Malicious Extension, Chrome API
- **Scenario**: Malicious browser extension rewrites tab content silently using Tabs API
- **Attack Steps**: 1. User installs a browser extension that claims to boost productivity (e.g., to-do list or screenshot tool). 2. The extension requests tabs permissions. 3. When the user visits email or banking sites, the extension monitors tab events. 4. On detecting a blur event (tab switch), it rewrites the DOM or navigates the tab to a phishing page (e.g., fake bank login). 5. The user thinks their session expired and retypes credentials. 6. The extension exfiltrates this data silently to attacker servers.
- **Detection**: Detect suspicious tab rewrites by extensions
- **Solution**: Audit permissions and avoid installing unknown extensions
- **Tags**: #browserextensionabuse #chrometabapi #phishingaddon

## Simulated “Session Expired” Modal Overlays Fake Login

- **Attack Type**: Visual Modal Injection
- **Target**: SaaS Users
- **Vulnerability**: Fake modal simulating session logic
- **MITRE**: T1202
- **Impact**: UI deception, account compromise
- **Tools**: HTML, CSS, JS
- **Scenario**: Fake modal on top of page claims session expired, collects credentials
- **Attack Steps**: 1. The attacker’s page appears as a secure site, such as an online editor or cloud portal. 2. After a few minutes of idle or tab switching, a modal box is injected using JavaScript. 3. The modal dims the background with a transparent overlay and displays a login prompt in the center. 4. It contains brand logos and a message like “Session timed out for security. Please login again.” 5. Victim believes this is part of session management, enters credentials, and the data is sent to the attacker. 6. Modal closes, and a generic loading spinner is shown.
- **Detection**: Detect modals injected without server signals
- **Solution**: Implement modal triggers only from backend sessions
- **Tags**: #fakeoverlay #modalphishing #visualtrick

## window.opener Used to Redirect to Corporate SSO Page Clone

- **Attack Type**: window.opener Exploitation
- **Target**: Corporate Users
- **Vulnerability**: Trust in SSO re-login prompts inside trusted tools
- **MITRE**: T1189
- **Impact**: Enterprise compromise
- **Tools**: JavaScript, target="_blank"
- **Scenario**: Tab opened from Slack modifies opener to spoof SSO login
- **Attack Steps**: 1. A malicious message in Slack includes a link to “updated policy” page. 2. It opens in a new tab and uses window.opener.location.replace() to modify the original Slack tab. 3. The original tab is changed to a fake corporate SSO login screen. 4. The user sees the login prompt in the same Slack tab and believes re-authentication is required. 5. Credentials are captured and used to infiltrate internal systems.
- **Detection**: Enforce opener restrictions in internal tools
- **Solution**: Add login banners with verified domain checks
- **Tags**: #ssohijack #windowopener #slackphish

## Cryptocurrency Wallet Tab Redirects to Unicode Lookalike Site

- **Attack Type**: Unicode Homoglyph Attack
- **Target**: Crypto Users
- **Vulnerability**: Unicode trickery in tab domain display
- **MITRE**: T1189
- **Impact**: Wallet takeover, financial theft
- **Tools**: Punycode, HTML, JS
- **Scenario**: Idle tab redirects to a spoofed wallet domain using Cyrillic characters
- **Attack Steps**: 1. A user opens a DeFi site and gets distracted. 2. Attacker’s tab uses window.location.replace() after delay to redirect to metamаsk.com (with Cyrillic “а”). 3. The cloned site appears identical, complete with MetaMask branding. 4. User enters seed phrase thinking their wallet session expired. 5. Wallet is compromised and drained.
- **Detection**: Use anti-homoglyph plugins in browsers
- **Solution**: Never enter seed phrases in browser windows
- **Tags**: #punycodeattack #metamaskphish #walletdrain

## JavaScript Click Trap Forces Navigation to Phishing Page

- **Attack Type**: Click Hijack via Inactivity Timer
- **Target**: Workspace Users
- **Vulnerability**: Simulated click deception post-idle
- **MITRE**: T1204
- **Impact**: Credential phishing, session trap
- **Tools**: JS, CSS
- **Scenario**: Simulated user click redirects tab after inactivity
- **Attack Steps**: 1. Page uses setTimeout() to wait 2 minutes after tab becomes inactive. 2. Then it simulates a click event on a hidden anchor tag using JS (link.click()), redirecting to a phishing site. 3. Target is shown a fake login page (e.g., Google Workspace). 4. Credentials entered are stolen.
- **Detection**: Block JS click auto-triggers in login flows
- **Solution**: Browser extensions can detect fake interactions
- **Tags**: #clicktrap #autonavigate #phishredirect

## PDF Viewer Web Tab Hijacked into Microsoft 365 Login

- **Attack Type**: DOM Rewrite on Viewer
- **Target**: Document Users
- **Vulnerability**: Viewer UI reused for login spoof
- **MITRE**: T1189
- **Impact**: Account compromise, file theft
- **Tools**: PDF.js, HTML, JS
- **Scenario**: Document preview tab swaps to fake 365 login
- **Attack Steps**: 1. A user opens a resume or contract using a web-based PDF viewer. 2. Script detects inactivity, and after 1 minute, replaces DOM with Microsoft 365 login screen. 3. “To continue viewing, please login” is shown. 4. Credentials entered are sent to attacker, used to infiltrate organization.
- **Detection**: Track login page creation in viewer environments
- **Solution**: Disable login in front-end-only viewers
- **Tags**: #pdfspoof #viewerphishing #ms365fake

## Online Learning Platform Tab Mimics Zoom Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Students, Teachers
- **Vulnerability**: Fake Zoom login via trusted platform integration
- **MITRE**: T1189
- **Impact**: Privacy breach, impersonation
- **Tools**: LMS, HTML, JS
- **Scenario**: LMS tab loads fake Zoom login after user switches
- **Attack Steps**: 1. A student is logged into a learning platform that integrates Zoom. 2. While attending a recorded class, they switch tabs. 3. After 45 seconds, the platform’s tab reloads with a fake Zoom login screen. 4. Message: “Zoom session expired, please log in to continue.” 5. Victim enters Zoom credentials, which are phished. 6. Attacker may join live classes, impersonate user.
- **Detection**: Audit login source URLs and referrers
- **Solution**: Educate users on app-based login vs in-browser prompts
- **Tags**: #zoomphish #eduhack #tabtrick

## Academic Site Replaces Tab with Fake Google Login

- **Attack Type**: JavaScript-Based Tab Replacement
- **Target**: Students
- **Vulnerability**: Inactivity-triggered full-page login swap
- **MITRE**: T1189
- **Impact**: Google Workspace account breach
- **Tools**: JS, HTML
- **Scenario**: University portal shows fake Google login after tab idle
- **Attack Steps**: 1. A student logs into a university portal to access academic resources. 2. They open a lecture in a tab and switch to another to check emails. 3. The portal uses JavaScript to detect inactivity using document.hidden. 4. After a delay of 60 seconds, the page is fully replaced with a replica Google login. 5. Message shown: "Re-authenticate with your university-linked Google account." 6. Victim enters their credentials assuming session expired. 7. Credentials are exfiltrated silently. 8. Attacker uses them to access Google Workspace or Gmail to further phish or spread malware.
- **Detection**: Logins from university domain should match original referrer
- **Solution**: Train users to verify URLs before entering credentials
- **Tags**: #googlereauth #tabspoof #universityphish

## Job Portal Hijacks Tab with LinkedIn Clone

- **Attack Type**: DOM Rewrite on Idle
- **Target**: Job Seekers
- **Vulnerability**: Trust in LinkedIn branding + job site
- **MITRE**: T1189
- **Impact**: Profile takeover, reputation damage
- **Tools**: JS, CSS, HTML
- **Scenario**: Job search tab is rewritten with LinkedIn login clone
- **Attack Steps**: 1. User browses a job board and views listings. 2. When switching tabs to research a company, a background script detects tab switch via blur. 3. After 90 seconds, the tab’s DOM is overwritten to show a LinkedIn login screen. 4. It appears to be a re-auth prompt for syncing applications. 5. Victim enters credentials. 6. Data is sent to attacker, who may hijack the profile or scrape contacts. 7. A “login failed” alert or redirect to the real LinkedIn hides traces.
- **Detection**: Detect unexpected LinkedIn logins from referrer domains
- **Solution**: Enable 2FA and SSO logins on professional accounts
- **Tags**: #linkedinphish #careertrap #domreplace

## Iframe Overlay Spoofs Instagram Login

- **Attack Type**: Iframe-Based Credential Theft
- **Target**: Social Media Users
- **Vulnerability**: Overlay with real-looking login in iframe
- **MITRE**: T1204
- **Impact**: Credential theft
- **Tools**: HTML, iframe, JS
- **Scenario**: Hidden iframe becomes visible after inactivity, mimicking Instagram
- **Attack Steps**: 1. Victim opens a meme gallery that embeds an invisible iframe. 2. The iframe initially points to a blank page but is later redirected to a phishing version of Instagram. 3. After 1 minute of tab inactivity, a script changes the iframe to visible with CSS styles mimicking the real site. 4. Victim returns and is told: "Session expired. Login to continue scrolling." 5. Login credentials are collected silently from the iframe and sent to attacker. 6. The frame is hidden again, and user is redirected to the actual Instagram.
- **Detection**: Disable iframe login prompts using CSP headers
- **Solution**: Use app-based login where possible
- **Tags**: #iframephish #instalure #overlaytrap

## Email Link Opens Tab That Hijacks Back to SSO

- **Attack Type**: window.opener Exploitation
- **Target**: Employees
- **Vulnerability**: Trust in email origin, opener misuse
- **MITRE**: T1189
- **Impact**: Internal system compromise
- **Tools**: JS, target="_blank"
- **Scenario**: Email phishing link changes original tab to spoofed SSO
- **Attack Steps**: 1. An employee clicks a newsletter link promising a benefits update. 2. The link opens a new tab that uses window.opener.location.replace() to hijack the original tab (likely intranet or SSO session). 3. Original tab now shows a fake SSO login portal with company branding. 4. Victim thinks re-authentication is needed and enters credentials. 5. Attacker captures them and gains access to internal systems.
- **Detection**: Email security tools should inspect link targets and behaviors
- **Solution**: Use rel="noopener noreferrer" for all links
- **Tags**: #windowspoof #emailbait #openertrap

## Browser Extension Swaps Tabs for Dropbox Login

- **Attack Type**: Malicious Extension Tab Rewrite
- **Target**: Cloud Storage Users
- **Vulnerability**: Abuse of extension privileges
- **MITRE**: T1176
- **Impact**: Cloud storage breach
- **Tools**: Chrome Extension, JS
- **Scenario**: Extension changes tab content post-installation
- **Attack Steps**: 1. User installs a browser extension for file conversion. 2. The extension asks for tab permissions and silently monitors browsing. 3. When a Dropbox tab is detected, the extension waits until the tab is inactive. 4. After 30 seconds of inactivity, the extension replaces the tab’s content with a Dropbox login page. 5. User re-authenticates, thinking the session expired. 6. Credentials are stolen, and Dropbox files are accessed. 7. Attack remains undetected unless permissions are reviewed.
- **Detection**: Enforce extension permission reviews in browsers
- **Solution**: Use signed extensions from trusted vendors only
- **Tags**: #dropboxhack #extphish #chromeabuse

## Conference Portal Tab Swaps to Zoom Login Clone

- **Attack Type**: JavaScript Tab Replacement
- **Target**: Attendees
- **Vulnerability**: Exploiting event platform trust
- **MITRE**: T1189
- **Impact**: Meeting hijack, impersonation
- **Tools**: HTML, JS, Zoom UI
- **Scenario**: Fake Zoom login after inactivity during virtual event
- **Attack Steps**: 1. User joins an online tech conference via browser. 2. Session stream is embedded in a tab, and user switches tabs to multitask. 3. JavaScript listens for inactivity and swaps content after 2 minutes. 4. A fake Zoom login screen appears, mimicking session timeout. 5. Victim enters Zoom credentials, assuming it's needed to rejoin. 6. Credentials are exfiltrated in real time to attacker.
- **Detection**: Log Zoom logins during virtual events for audit
- **Solution**: Embed Zoom via app-only for login workflows
- **Tags**: #zoomspoof #eventhack #tabmanip

## Video Site Tab Uses Click Simulation to Redirect to PayPal Clone

- **Attack Type**: Click Simulation via JavaScript
- **Target**: Shoppers
- **Vulnerability**: Idle state + fake transaction lure
- **MITRE**: T1204
- **Impact**: Account compromise, purchase fraud
- **Tools**: JS, fake PayPal
- **Scenario**: Idle video tab simulates click to phishing page
- **Attack Steps**: 1. A user plays a video from a random free site. 2. While paused and idle, the page uses setTimeout() and JavaScript to simulate a click on a hidden link. 3. This opens a fake PayPal login page. 4. Victim assumes it's part of some embedded payment process. 5. Enters PayPal credentials, which are logged and abused for purchases.
- **Detection**: Disable click simulations in inactive tabs
- **Solution**: Use app-based 2FA to validate payments
- **Tags**: #paypalfake #clickphish #videotrap

## Unicode Spoof Redirect in Travel Booking Tab

- **Attack Type**: Punycode/Unicode URL Swap
- **Target**: Travelers
- **Vulnerability**: Visual domain deception via Unicode
- **MITRE**: T1189
- **Impact**: Identity theft, financial abuse
- **Tools**: HTML, JS
- **Scenario**: Idle booking tab changes to domain like trаvelsite.com
- **Attack Steps**: 1. User browses hotel deals on a known travel site. 2. After 1 minute of inactivity, tab is redirected to trаvelsite.com (with Cyrillic 'а'). 3. Same branding and UI as real site. 4. Victim re-enters login or payment info. 5. Attacker uses it for travel fraud or credit card theft.
- **Detection**: Use anti-homoglyph browser extensions
- **Solution**: Educate users about Unicode phishing
- **Tags**: #punycodephish #travelhack #visuallure

## Developer Tool Tab Swaps to GitHub 2FA Prompt

- **Attack Type**: DOM Replacement Post-Idle
- **Target**: Developers
- **Vulnerability**: Trust in GitHub, 2FA deception
- **MITRE**: T1111
- **Impact**: DevOps token theft
- **Tools**: HTML, JS
- **Scenario**: Dev tool tab changes to fake GitHub 2FA request
- **Attack Steps**: 1. User opens a dev tool for API testing. 2. After 90 seconds idle, tab DOM changes to GitHub 2FA screen with QR scan or OTP prompt. 3. Victim inputs token assuming it’s a security update. 4. Attacker steals token, initiates login.
- **Detection**: Log suspicious OTP logins
- **Solution**: Require biometric authentication if possible
- **Tags**: #github2fa #tokensteal #devphish

## LMS Tab Rewrites to Fake Google Classroom Login

- **Attack Type**: JavaScript DOM Spoofing
- **Target**: Students
- **Vulnerability**: Trusted LMS portal spoofed
- **MITRE**: T1189
- **Impact**: Credential loss, data breach
- **Tools**: HTML, CSS, JS
- **Scenario**: Learning site tab becomes Google Classroom login screen
- **Attack Steps**: 1. A student logs into LMS to review homework. 2. Switches tabs for a while. 3. After 2 minutes, JS replaces tab content with Google Classroom login. 4. User enters email and password, which are sent to attacker. 5. Tab resets to original LMS to hide trick.
- **Detection**: Enforce login only via app-based portals
- **Solution**: Train students on URL verification
- **Tags**: #classroomphish #eduattack #tabnabbing

