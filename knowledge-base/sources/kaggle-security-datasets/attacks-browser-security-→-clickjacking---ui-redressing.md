# Browser Security → Clickjacking / UI Redressing Attacks

## Account Deletion via Transparent Iframe

- **Attack Type**: Hidden Iframe Clickjacking
- **Target**: Social Media / Account Settings
- **Vulnerability**: No X-Frame-Options or CSP headers
- **MITRE**: T1189 (Drive-by Compromise)
- **Impact**: Unauthorized account action
- **Tools**: Browser DevTools, Iframe Loader
- **Scenario**: Trick user into deleting their own account by overlaying a transparent iframe containing the “Delete Account” button.
- **Attack Steps**: 1. The attacker creates a fake webpage — for example, a contest page promising a free gift card. 2. On this fake page, they embed a fully transparent iframe that loads the real target site (e.g., a user's account settings page from a banking or social media website). 3. They carefully position this iframe so that the target site's "Delete Account" button aligns perfectly with the visible "Click here to claim prize" button. 4. The user thinks they are clicking a harmless prize button but actually triggers the “Delete Account” action underneath in the hidden frame. 5. The attack works because the user is already logged into the target website in another tab. 6. The attacker needs no access to credentials — just tricks the user into clicking once in the right place. 7. After the click, the account gets deleted without warning, and the user is unaware until it's too late.
- **Detection**: Monitor iframe usage, detect suspicious click alignments
- **Solution**: Add X-Frame-Options: DENY or Content-Security-Policy: frame-ancestors 'none'
- **Tags**: #clickjacking #transparentiframe #accountdeletion

## Fake Like Button Overlays YouTube Subscribe

- **Attack Type**: Hidden Frame + CSS Overlay
- **Target**: Video Streaming (YouTube)
- **Vulnerability**: No frame-ancestors restrictions, iframe allowed
- **MITRE**: T1189
- **Impact**: Forced subscription, spam growth
- **Tools**: Browser DevTools, HTML Overlay
- **Scenario**: Overlay a fake “Like” button that triggers YouTube subscription click underneath.
- **Attack Steps**: 1. Attacker builds a fake article titled “You won’t believe this cat video!”. 2. They place a big “Like” button in the center, designed with CSS. 3. Directly underneath it — but invisible — is a transparent iframe pointing to a real YouTube channel’s subscribe button. 4. The iframe is set with opacity: 0 and precise z-index so that only the attacker’s design is seen. 5. When the user clicks “Like”, they unknowingly subscribe to a YouTube channel. 6. This increases the attacker’s subscriber count through trickery. 7. Users have no idea they’ve subscribed, since no confirmation message is shown.
- **Detection**: Detect iframe overlays on critical UI buttons
- **Solution**: Enforce Content-Security-Policy to disallow embedding
- **Tags**: #clickfraud #youtubeoverlay #clickjacking

## Stealth Donation via Hidden Paypal Button

- **Attack Type**: Hidden Frame Trick
- **Target**: Payment Gateways
- **Vulnerability**: Iframes allowed with no interaction checks
- **MITRE**: T1189
- **Impact**: Unintended donations, financial loss
- **Tools**: HTML + CSS + PayPal Sandbox
- **Scenario**: Trick users into clicking a hidden PayPal donation button placed under a fake game.
- **Attack Steps**: 1. Attacker builds a mini-browser game (like "Pop the Balloon"). 2. On the surface, it looks like a fun interactive game. 3. But under the clickable game area, they embed a fully transparent iframe that loads a PayPal “Donate” button to their account. 4. The iframe is precisely aligned using position:absolute; opacity:0; z-index:1. 5. Every time the user clicks a balloon, they are actually triggering a payment. 6. The attacker gets small amounts of money from each click — like $1 per action. 7. The user thinks they’re playing a game, while behind the scenes a financial transaction is happening. 8. Since the iframe is from PayPal’s real domain, the user may not suspect anything unusual unless they carefully check their account.
- **Detection**: Monitor unexpected clicks triggering payments
- **Solution**: Implement X-Frame-Options, enable CAPTCHA for payment actions
- **Tags**: #paypaljacking #clickscam #iframeabuse

## Z-index UI Trap Over Social Media Buttons

- **Attack Type**: CSS Z-index Manipulation
- **Target**: Social Media Sites
- **Vulnerability**: Improper iframe layering protections
- **MITRE**: T1189
- **Impact**: Unauthorized content sharing
- **Tools**: DevTools, Z-index Exploit Kit
- **Scenario**: Use layered divs to mislead the user into interacting with hidden elements.
- **Attack Steps**: 1. The attacker builds a web page with layered elements: visible ones for distraction and hidden ones with real actions. 2. A fake "Next" or “Continue” button is visible on screen. 3. Underneath it, they place the real “Share to Facebook” or “Tweet” button from a third-party iframe. 4. CSS z-index ensures the top layer shows only the fake UI, but the real clickable button is just beneath. 5. When the user clicks the fake button, they’re actually sharing or tweeting content on their own profile. 6. This is used to spread malicious links or promotions without consent. 7. The user remains unaware unless they visit their social media profile later.
- **Detection**: Detect overlap of clickable and invisible elements
- **Solution**: Restrict framing and implement click confirmation
- **Tags**: #zindexabuse #socialmediahijack #uiredress

## Mouse Movement Tracking + Delayed Click Trap

- **Attack Type**: Mouse Tracking Attack
- **Target**: Any Website with Clickable UI
- **Vulnerability**: Click triggers not locked to visible elements
- **MITRE**: T1189
- **Impact**: Forced consent, account manipulation
- **Tools**: JS MouseEvent, Heatmap Tools
- **Scenario**: Monitor mouse movement to predict clicks, then overlay iframe milliseconds before click.
- **Attack Steps**: 1. Attacker embeds JavaScript code to constantly monitor the mouse position on a webpage. 2. When the mouse is near a key location (e.g., top right corner), it prepares an iframe. 3. Just as the user is about to click a visible button, it instantly overlays a transparent iframe with a malicious button in the same position. 4. This sudden overlay tricks the user into clicking the hidden button. 5. The attacker may use this to submit forms, enable push notifications, or perform account changes. 6. The iframe disappears immediately after click, making it very hard to detect. 7. Because of the timing and speed, even careful users are fooled. 8. Mouse tracking makes it context-aware and harder to prevent.
- **Detection**: Detect JS monitoring mouse position with suspicious iframe injection
- **Solution**: Prevent sudden DOM changes near click zones
- **Tags**: #clicktrap #mousetracking #invisibleiframe

## Transparent Frame Triggers Browser Permission

- **Attack Type**: Hidden Iframe + Permission Abuse
- **Target**: Camera/Mic Access Web Apps
- **Vulnerability**: Overlay on browser permission popups
- **MITRE**: T1189
- **Impact**: Webcam/mic spying
- **Tools**: HTML Iframe, Webcam Tester
- **Scenario**: Fake button overlays browser's camera/mic permission dialog, tricking user into allowing it.
- **Attack Steps**: 1. Attacker creates a webpage offering a "Try Webcam Filter" experience. 2. The page has a large “Allow Camera Access” button in the center. 3. Under this fake button, a transparent iframe from the target site is embedded. 4. That iframe triggers the real browser camera permission prompt, where clicking in the right spot actually clicks “Allow”. 5. User believes they are clicking the attacker’s button, but they are enabling access to their camera/mic. 6. Once granted, attacker’s app gains real-time media access via browser APIs. 7. This can be used to eavesdrop or record users unknowingly. 8. It’s a privacy violation that feels like a single innocent click.
- **Detection**: Watch for permission prompts tied to hidden overlays
- **Solution**: Use browser’s UI isolation protections
- **Tags**: #camaccess #iframeclickjacking #permissiontrap

## Clickjacking via Embedded Bank Transfer Button

- **Attack Type**: Hidden Frame Fraud
- **Target**: Banking Portals
- **Vulnerability**: Framing of banking UI allowed, no CSRF token enforcement
- **MITRE**: T1189
- **Impact**: Unauthorized fund transfer
- **Tools**: Burp Suite, Transparent Iframe
- **Scenario**: Trick user into confirming a bank transfer by masking the confirmation frame under game UI.
- **Attack Steps**: 1. Attacker creates a puzzle game with multiple on-screen buttons. 2. Under one of the clickable elements, they embed a transparent iframe that loads a bank’s “Confirm Transfer” button. 3. If the victim is logged into their online bank in another tab, the click is authenticated using their session. 4. When they click the puzzle element, they actually approve a transaction. 5. Attackers often use small transfer amounts to avoid suspicion. 6. Victims don’t realize money has been transferred until they check balances manually. 7. Since the transfer uses a legitimate session, there’s no alert raised by the bank’s system.
- **Detection**: Heuristics for same-origin framing and invisible input areas
- **Solution**: Enforce SameSite cookies and frame-ancestors
- **Tags**: #bankingfraud #clickjacking #moneytransfer

## UI Redressing in Survey Completion Page

- **Attack Type**: CSS Z-index Trick
- **Target**: Marketing Surveys
- **Vulnerability**: Layered UI with misleading positioning
- **MITRE**: T1189
- **Impact**: Forced newsletter subscription
- **Tools**: DevTools, SurveyClone Template
- **Scenario**: Style fake “Submit Survey” button to hover over newsletter opt-in checkbox.
- **Attack Steps**: 1. Survey platform has a checkbox like “Sign me up for marketing emails”. 2. Attacker copies this survey layout and overlays a fake “Submit” button using CSS. 3. They position it with z-index: 999 directly above the opt-in checkbox. 4. When the user clicks the button, they actually check the box below. 5. The real survey submission is triggered automatically with the opt-in now selected. 6. Victim unknowingly subscribes to spam newsletters or other programs. 7. It’s often used for lead generation scams or affiliate marketing abuse.
- **Detection**: Compare click position with checkbox state
- **Solution**: Enforce visible checkbox labels, add opt-in confirmation
- **Tags**: #uihack #surveyxss #zindextrap

## Framing Login Page to Steal Clicks

- **Attack Type**: Hidden Iframe
- **Target**: OAuth Login Providers
- **Vulnerability**: Framed login dialogs without control
- **MITRE**: T1189
- **Impact**: OAuth session hijack
- **Tools**: Burp Suite, Hidden Frame Builder
- **Scenario**: Trick user into clicking “Login with Google” button from another site.
- **Attack Steps**: 1. Attacker builds a fake website that offers early access to trending software. 2. The site includes a “Continue with Google” button. 3. But beneath it lies a hidden iframe loading a real login page from a third-party service. 4. When clicked, it initiates a login session to a malicious app or phishing account. 5. User is unknowingly granting OAuth access. 6. This trick is common in scam promotions or fake sign-up flows. 7. It can lead to attackers gaining access to Google Drive, Gmail, or other linked services.
- **Detection**: Detect off-domain iframe loading on login pages
- **Solution**: Add OAuth confirmation screens and framing controls
- **Tags**: #loginoverlay #oauthabuse #clickjacking

## Invisible Poll Voting Trick

- **Attack Type**: Transparent Iframe
- **Target**: Polling Platforms
- **Vulnerability**: Framing allowed, no click verification
- **MITRE**: T1189
- **Impact**: Vote manipulation, opinion bias
- **Tools**: Burp Suite, Custom HTML
- **Scenario**: User thinks they’re rating an article but actually votes in a rigged poll underneath.
- **Attack Steps**: 1. A fake news site encourages users to rate a story with thumbs up/down icons. 2. Beneath these visible icons, a transparent iframe loads a real voting page with radio buttons. 3. When the user clicks “Thumbs Up”, it selects a specific poll option like “Option C = Best Candidate”. 4. Victim’s vote is submitted silently. 5. This skews public opinion or social poll results for manipulation. 6. It’s especially used around elections, product reviews, or controversial topics.
- **Detection**: Look for polling actions triggered via offscreen frames
- **Solution**: Require double-confirmation on votes
- **Tags**: #polljacking #clickfraud #votemanipulation

## Click-to-Claim Contest Exploits Email Settings

- **Attack Type**: Transparent Iframe
- **Target**: Webmail Accounts (Gmail, Outlook)
- **Vulnerability**: Email preference buttons exposed via frame
- **MITRE**: T1189
- **Impact**: Loss of security visibility, missed alerts
- **Tools**: HTML/CSS, Browser DevTools
- **Scenario**: Clickbait page hides real “Unsubscribe All” button behind fake contest interaction
- **Attack Steps**: 1. Attacker designs a fake webpage that advertises a fake sweepstakes or giveaway — e.g., “Click here to claim your ₹5,000 shopping voucher!” 2. The visible “Claim Now” button is just a decoy designed with HTML/CSS. 3. Behind it, the attacker embeds a transparent iframe that loads the user’s real email account settings page — specifically the “Unsubscribe All” or “Disable Notifications” option. 4. The attacker aligns the hidden button exactly behind the fake one using absolute positioning. 5. When the user clicks the “Claim” button, they unknowingly change their email settings — disabling alerts or unsubscribing from security notifications. 6. If already logged in (e.g., Gmail, Outlook), the change happens instantly. 7. The attacker may then continue phishing or malicious activity while the victim stays unaware due to disabled alerts.
- **Detection**: Monitor critical preference changes after non-auth UI events
- **Solution**: Block iframe embedding, enforce frame-ancestors CSP
- **Tags**: #clickjacking #emailmanipulation #frameoverlay

## Mouse Hover Triggers Hidden Consent Click

- **Attack Type**: Mouse Tracking Attack
- **Target**: Websites offering downloads or freebies
- **Vulnerability**: Mouse-triggered DOM manipulation
- **MITRE**: T1189
- **Impact**: Forced consent, subscription fraud
- **Tools**: JavaScript MouseEvent, Heatmap Tools
- **Scenario**: Track mouse movement and inject a hidden “Accept Terms” click right before user’s own click
- **Attack Steps**: 1. A shady website pretends to offer a free resource — say, downloadable study material or a game. 2. JavaScript running in the background constantly tracks the position of the mouse using mousemove events. 3. When the user’s cursor moves close to a prominent button (e.g., “Download Now”), a transparent iframe is quickly injected and placed right over that area. 4. The iframe points to another site’s “Accept Terms” or “Subscribe to Premium” button. 5. As the user clicks the “Download” button, they actually activate the hidden iframe button. 6. The iframe disappears instantly after the click, making it nearly impossible for the user to notice what happened. 7. In the background, the attacker may gain premium access, enable paid services, or silently opt-in the user to subscriptions. 8. All of this happens without any explicit consent from the user — just via deceptive click hijacking.
- **Detection**: Detect sudden DOM injection near click zones
- **Solution**: Add interaction confirmation or CAPTCHA for consent
- **Tags**: #mousetracking #clicktrap #invisibleiframe

## Z-index Overlay Hides Dangerous Checkbox

- **Attack Type**: CSS Z-index Manipulation
- **Target**: Backup Management Portals
- **Vulnerability**: Overlaid checkboxes with destructive actions
- **MITRE**: T1189
- **Impact**: Data loss, backup deletion
- **Tools**: DevTools, CSS Inspector
- **Scenario**: A fake “Continue” button overlays a real checkbox like “Delete all backups”
- **Attack Steps**: 1. The attacker replicates a real-looking settings or installation page. 2. On this page, they place a “Continue Setup” button with attractive styling and positioning. 3. Right underneath this visible button, using absolute positioning, they place a real checkbox labeled “Delete all previous backups” that belongs to the actual software or service. 4. The checkbox is fully visible in code, but visually hidden using z-index layering and transparency. 5. When the user clicks “Continue Setup,” they actually check the dangerous checkbox without knowing. 6. Upon final submission, this action may delete all previously saved data or backups. 7. This is particularly dangerous in cloud backup services or system setup wizards. 8. The user has no way of knowing the checkbox was ticked unless they manually inspect HTML or use assistive tools.
- **Detection**: Detect layering of invisible input fields
- **Solution**: Require confirmation dialogs for destructive options
- **Tags**: #uiredress #zindextrick #databreach

## Transparent Frame Approves Cookie Harvesting

- **Attack Type**: Transparent Iframe + Privacy Manipulation
- **Target**: Consent Popups / Ad Networks
- **Vulnerability**: Consent iframe can be framed and misused
- **MITRE**: T1189
- **Impact**: Privacy violation, data sale
- **Tools**: Burp Suite, Iframe Toolkit
- **Scenario**: Trick users into agreeing to third-party cookie sharing by masking consent form
- **Attack Steps**: 1. The attacker creates a fake “Watch Video” page. 2. The visible button says “Click to Start” and sits prominently in the center of the page. 3. Underneath it, the attacker places a fully transparent iframe that loads a real consent form from a third-party tracking service. 4. This iframe is positioned so the real “Agree to Share My Data” button lies directly behind the visible play button. 5. When the user clicks “Click to Start,” they unknowingly give consent to third-party tracking or cookie sharing. 6. After the click, the iframe disappears, and the attacker loads a random video to keep the illusion going. 7. In the background, third-party services can now legally collect user data. 8. This is especially concerning with GDPR/CCPA rules, where false consent tricks still result in data harvesting.
- **Detection**: Monitor iframe origin during consent interactions
- **Solution**: Implement iframe sandboxing and frame-ancestors
- **Tags**: #gdprabuse #clickconsent #iframehack

## UI Redressing During Video Pause Modal

- **Attack Type**: Z-index Layering + Trick Modal
- **Target**: Video Platforms
- **Vulnerability**: Fake modals triggering unintended clicks
- **MITRE**: T1189
- **Impact**: Extension install, user deception
- **Tools**: HTML/CSS, DevTools
- **Scenario**: Overlay fake pause screen to hide malicious iframe with real interactions
- **Attack Steps**: 1. User watches a legitimate video on a known platform. 2. At a point where the video naturally pauses (like buffering or ad start), a modal appears — usually saying “Resume playback?” 3. The attacker mimics this behavior by building a fake modal that looks exactly like the video platform’s UI. 4. Underneath this fake modal, they place an iframe pointing to a third-party page with a “Sign Up Now” or “Install Extension” button. 5. The fake modal shows a “Resume” button, but clicking it actually installs a browser extension or subscribes to an email list. 6. This tactic is especially powerful on embedded video platforms where modals are expected behavior. 7. Because the fake UI looks natural, the user doesn’t realize they’ve triggered an unrelated action. 8. This can lead to malware installs, adware injection, or silent subscriptions.
- **Detection**: Check modal sources and z-index manipulation
- **Solution**: Lock high-privilege actions behind native confirmations
- **Tags**: #videohack #uiredressing #maliciousmodal

## Invisible Facebook Like Farming

- **Attack Type**: Hidden Iframe
- **Target**: Social Networks (Facebook)
- **Vulnerability**: Framed Like buttons with no user awareness
- **MITRE**: T1189
- **Impact**: Artificial engagement boosting
- **Tools**: Facebook DevTools, Burp
- **Scenario**: Trick users into “Liking” a page on Facebook by clicking a fake image or video
- **Attack Steps**: 1. Attacker builds a meme-sharing page that shows viral content like funny GIFs. 2. The visible image is interactive, prompting users to click “Play” or “React”. 3. Under the image, the attacker embeds a transparent iframe pointing to a Facebook “Like Page” button. 4. The iframe is perfectly aligned so clicking the image performs the Facebook like action. 5. Victims unknowingly boost the popularity of spam pages, bot-run groups, or fake products. 6. The attacker repeats this across many sites to increase reach. 7. Because the iframe uses Facebook’s real Like widget, browsers don’t block the request. 8. User remains unaware unless they visit their profile and see unwanted likes.
- **Detection**: Detect iframe usage over visual elements
- **Solution**: Restrict framing, show Like preview overlays
- **Tags**: #facebooklikejacking #clickmanipulation

## Transparent Frame Hijacks Browser Extension Install

- **Attack Type**: Iframe Click Hijack
- **Target**: Browser Extensions
- **Vulnerability**: Browser install actions not protected by click validation
- **MITRE**: T1189
- **Impact**: Extension hijack, ad injection
- **Tools**: Browser Extension Test, Dev Console
- **Scenario**: Force user to install a malicious extension via click trap in web game
- **Attack Steps**: 1. Attacker builds a simple browser game with flashy elements. 2. They embed a transparent iframe beneath the “Next Level” button. 3. This iframe points to the browser’s extension install page for a malicious add-on. 4. When the player clicks to go to the next level, they trigger an extension installation instead. 5. Since extension prompts often don’t require confirmation, the install begins immediately. 6. The extension may contain spyware or inject ads. 7. User may not notice the add-on has been installed unless they check browser settings. 8. This tactic has been used in rogue app stores and sketchy game portals.
- **Detection**: Monitor extension prompts after unexpected clicks
- **Solution**: Require confirmation before enabling extensions
- **Tags**: #extensionclickjacking #browserexploit

## Misused CSS Hover Triggers Hidden Action

- **Attack Type**: CSS Z-index + Hover Trick
- **Target**: Any UI-Based Webpage
- **Vulnerability**: CSS hover areas interacting with hidden iframes
- **MITRE**: T1189
- **Impact**: UI deception, unintended feature activation
- **Tools**: HTML, CSS
- **Scenario**: Fake hover popup triggers mouse click over hidden action button
- **Attack Steps**: 1. A website pretends to show a tooltip or popup when hovering over an image or link. 2. The CSS is manipulated so the hover effect activates a hidden iframe containing a sensitive action. 3. The popup appears normal, but clicking it actually presses a button inside the iframe below — like “Enable Notifications” or “Add to Cart”. 4. The attacker uses z-index, opacity, and hover transitions to deceive users. 5. User thinks they’re dismissing the popup or clicking to “Read more” — but trigger a hidden backend action. 6. This tactic exploits natural UI behavior and timing. 7. Hover + click-based combos are harder to detect via static scanning. 8. Victims unknowingly activate offers, notifications, or permissions.
- **Detection**: Inspect hover CSS behavior and click handlers
- **Solution**: Confirm clicks before taking sensitive actions
- **Tags**: #hovertrap #cssclickjacking

## Game Leaderboard Clickjacking

- **Attack Type**: Transparent Iframe + Game UI Trick
- **Target**: Online Games, Web3 Wallets
- **Vulnerability**: Framed UI tricking score submissions
- **MITRE**: T1189
- **Impact**: Web3 wallet drain, smart contract abuse
- **Tools**: Game UI Frameworks, Burp Suite
- **Scenario**: Game leaderboard embeds hidden iframe under “Submit Score” button
- **Attack Steps**: 1. A fake browser-based game shows a leaderboard screen when a user finishes a level. 2. On the screen, the “Submit Score” button appears in the center. 3. Under this button, the attacker embeds a transparent iframe pointing to a form submission on a third-party app. 4. When clicked, the form sends the victim’s session token or approval to a malicious site. 5. Because it’s disguised under a game UI, users never suspect foul play. 6. The iframe may also trigger a webhook or sign a smart contract if connected to wallets. 7. The attacker earns money or access by leveraging the victim’s session trust. 8. This method is effective in Web3 games, NFTs, and crypto contests.
- **Detection**: Monitor third-party form requests inside game context
- **Solution**: Add CAPTCHA or click confirmation to forms
- **Tags**: #gameclickjacking #web3hack

## “Click to Zoom” Masks Biometric Consent

- **Attack Type**: Transparent Iframe
- **Target**: Biometric Login Interfaces
- **Vulnerability**: Framing of browser-native biometric prompts
- **MITRE**: T1189
- **Impact**: Biometric abuse, identity fraud
- **Tools**: HTML5, Iframe API
- **Scenario**: Fake image zoom click covers real fingerprint or face scan consent
- **Attack Steps**: 1. A fake job application or ticket booking site displays an image preview (e.g., ID proof). 2. Users are prompted to “Click to Zoom” to view the full image. 3. Behind this button, a transparent iframe loads a browser-native biometric consent dialog. 4. Clicking the fake button actually activates face scan or fingerprint approval. 5. If the user’s system has biometric authentication enabled, it may proceed silently. 6. The attacker gets authentication tokens or session access. 7. Biometric info is misused to validate malicious logins. 8. This form of clickjacking abuses built-in browser APIs to perform stealthy actions.
- **Detection**: Detect biometric prompts invoked by non-visible UIs
- **Solution**: Disallow programmatic triggering of biometric flows
- **Tags**: #biometricclickjacking #zoomtrap #invisibleauth

## Invisible Frame Grants App Permissions

- **Attack Type**: Hidden Iframe
- **Target**: Google Accounts, Microsoft Services
- **Vulnerability**: Transparent OAuth prompts
- **MITRE**: T1189
- **Impact**: Unauthorized data access
- **Tools**: HTML, CSS, OAuth Playground
- **Scenario**: Deceptive interface tricks user into granting app access to personal data
- **Attack Steps**: 1. The attacker builds a fake typing test page that looks fun and legitimate to attract users. 2. On the page, a large “Start Typing Test” button is prominently placed in the center. 3. Behind this visible button, the attacker inserts a transparent iframe (opacity: 0; position: absolute;) which loads an actual OAuth consent screen (e.g., “Allow access to Google Drive?”). 4. The attacker aligns the iframe button perfectly underneath the visible "Start Test" button using CSS. 5. When the user clicks to start the test, their action actually clicks the “Allow” button inside the iframe, unknowingly authorizing access. 6. The attacker now receives a valid OAuth token, giving them access to the victim's data such as files, contacts, or calendar entries. 7. The user sees the typing test begin normally and assumes everything is fine, unaware of the background access. 8. The malicious app can now silently exfiltrate data, perform operations, or maintain persistent access until manually revoked.
- **Detection**: Monitor unexpected app authorizations in audit logs
- **Solution**: Enforce frame busting with CSP and OAuth domain restrictions
- **Tags**: #clickjacking #oauthabuse #iframeattack

## Fake Quiz Triggers Paid Subscription

- **Attack Type**: Transparent Iframe
- **Target**: Email Platforms, Paid Services
- **Vulnerability**: Invisible multi-step iframe forms
- **MITRE**: T1189
- **Impact**: Financial loss, inbox flooding
- **Tools**: HTML/CSS, JS, Browser Console
- **Scenario**: Users tricked into subscribing to a paid mailing list during a fake quiz
- **Attack Steps**: 1. An attacker creates a light-hearted online quiz (e.g., “What fruit matches your personality?”) to lure users into participation. 2. The quiz interface includes large answer buttons for each question. 3. Under each visible answer button, the attacker embeds a transparent iframe with a subscription confirmation form that submits the victim's email address (collected earlier) to premium services. 4. The iframe is aligned so that when users click on each answer, they unknowingly trigger steps like agreeing to terms, confirming a plan, and submitting payment information. 5. After the last question, the user is shown their “results” to maintain the illusion. 6. In the background, the victim has been subscribed to paid services and newsletters without explicit consent. 7. They start receiving spam or even billing charges depending on the service. 8. The attacker monetizes this by affiliating with ad networks or email campaign tools.
- **Detection**: Check for POST requests during UI interaction
- **Solution**: Add CAPTCHA and visible multi-step confirmation
- **Tags**: #subscriptionfraud #quizclickjacking #darkpattern

## Reaction Game Hijacks Push Notifications

- **Attack Type**: Mouse Tracking + Hidden Frame
- **Target**: Browsers with Push API (Chrome, Firefox)
- **Vulnerability**: In-browser permission hijack
- **MITRE**: T1189
- **Impact**: Persistent phishing via notifications
- **Tools**: JavaScript, DOM Inspector, Burp Suite
- **Scenario**: Fake reaction game tricks user into enabling malicious push notifications
- **Attack Steps**: 1. The attacker hosts a simple browser game that asks users to “Click when the circle turns green.” 2. The attacker uses mousemove events in JavaScript to track the position of the cursor in real-time. 3. As the user hovers near the clickable circle, a transparent iframe is injected and placed directly over the expected click area. 4. This iframe contains a legitimate browser permission popup requesting notification access. 5. The user, seeing the circle turn green, clicks expecting to play the game, but instead they unknowingly approve push notification access for the attacker’s domain. 6. Now, the attacker can send the victim fake alerts — like “Your bank account was accessed! Click here to secure it.” — leading to phishing pages. 7. The user is unaware that the permission was granted during gameplay. 8. This tactic leads to ongoing abuse through deceptive notifications that appear system-level.
- **Detection**: Analyze when and how push permissions are granted
- **Solution**: Delay notification prompts until post-interaction or use full-page modals
- **Tags**: #pushabuse #clicktrap #gamebait

## Overlay Navigation Menu Triggers Bank Transfer

- **Attack Type**: CSS Z-index Overlay
- **Target**: Online Banking Portals
- **Vulnerability**: UI layers exposing sensitive action buttons
- **MITRE**: T1189
- **Impact**: Unauthorized fund transfers
- **Tools**: HTML/CSS, DevTools
- **Scenario**: Attacker masks a real “Transfer Funds” button with fake website navigation
- **Attack Steps**: 1. The attacker creates a fake website that mimics a tech company’s homepage with a navbar. 2. The site includes a menu bar with links like “Home,” “Pricing,” “Support,” etc. 3. Underneath one of the menu items (e.g., “Support”), a transparent iframe is embedded pointing to the victim’s online banking dashboard. 4. The iframe is aligned to the “Transfer Now” button on the legitimate site, which the attacker predicts is already authenticated in the user’s session. 5. When the user clicks “Support,” their action passes through the transparent layer, activating the bank transfer. 6. No confirmation is shown as the banking site processes the click immediately. 7. The user continues browsing, unaware that their funds were transferred to the attacker’s account. 8. This technique is dangerous due to the mix of CSS trickery and session abuse.
- **Detection**: Monitor high-value actions from third-party origins
- **Solution**: Use CSRF tokens and frame-busting headers
- **Tags**: #bankingfraud #zindexattack #uiredressing

## Meme Page Steals Social Media Engagement

- **Attack Type**: Hidden Iframe + Widget Abuse
- **Target**: Facebook, Twitter, Instagram
- **Vulnerability**: Framing of native social engagement widgets
- **MITRE**: T1189
- **Impact**: False popularity metrics, phishing prep
- **Tools**: HTML iframes, Social Media Widgets
- **Scenario**: Click on memes actually likes or follows attacker-controlled accounts
- **Attack Steps**: 1. The attacker hosts a meme website with viral images and short videos. 2. A “Like this meme?” button is shown underneath each post. 3. Under that button, a transparent iframe is embedded pointing to a “Like Page” button from Facebook or “Follow” on Twitter. 4. When the user clicks to like the meme, they actually interact with the social widget in the iframe. 5. The attacker uses this to artificially inflate the follower count of a fake influencer account or promote scam pages. 6. Over time, this account may be used to launch phishing or ad fraud campaigns. 7. Victims typically never realize they've liked or followed anything — unless they view their own profile later. 8. The attacker can replicate this on multiple platforms to maximize engagement hijacking.
- **Detection**: Log iframe embeds of social buttons from third-party hosts
- **Solution**: Require origin validation and preview modals
- **Tags**: #likejacking #followscam #socialfraud

## Friend Request Confirmed via Hidden Frame

- **Attack Type**: Transparent Iframe
- **Target**: Facebook and Social Media Platforms
- **Vulnerability**: Friend approval pages without click validation
- **MITRE**: T1189
- **Impact**: Privacy exposure, trust abuse
- **Tools**: HTML/CSS, Facebook Dev Console
- **Scenario**: Tricked into confirming a malicious friend request with one click
- **Attack Steps**: 1. The attacker builds a website that looks like a dating platform or friend-finder app. 2. It includes a “Say Hi!” button as part of its interaction interface. 3. Directly under this button, an iframe is embedded (fully invisible) that loads a real Facebook friend request confirmation page. 4. The iframe is positioned so that the confirm button on Facebook lines up exactly behind the fake button. 5. When the user clicks “Say Hi!”, they instead confirm a friend request from a fake attacker-controlled profile. 6. The attacker now has social graph access to the victim’s timeline, posts, and possibly personal details like email or phone number. 7. This information is used in future scams or spear-phishing campaigns. 8. Because the interaction seems harmless, the user rarely notices unless they later check their Facebook connections.
- **Detection**: Use confirmation modals before accepting requests
- **Solution**: Disallow cross-domain framing for friend actions
- **Tags**: #friendjacking #socialengineering #clicktrap

## Fake Media Player Installs Malicious Extension

- **Attack Type**: Transparent Iframe
- **Target**: Chrome, Firefox Extensions
- **Vulnerability**: UI masking of install triggers
- **MITRE**: T1189
- **Impact**: Browser compromise, session hijacking
- **Tools**: HTML, Browser Extension APIs
- **Scenario**: Fake “Play” button hides a browser extension install request
- **Attack Steps**: 1. The attacker creates a website that advertises free access to movies or sports streams. 2. Users are shown a large “Play Now” button on the landing page. 3. A transparent iframe is placed underneath, targeting a browser extension install page (Chrome Web Store, Mozilla Add-ons). 4. Clicking the play button instead initiates an extension installation. 5. The user thinks the video failed to load due to buffering or delay — not realizing a malicious plugin was silently added. 6. The extension may ask for powerful permissions: “Read and change all your data on websites you visit.” 7. These permissions enable the attacker to steal credentials, inject ads, or monitor all browsing activity. 8. The attacker profits through ad revenue or stolen session cookies.
- **Detection**: Enforce user-facing warnings for extension actions
- **Solution**: Add delay-based user intent validation
- **Tags**: #extensiontrap #browserexploit #clickjacking

## Tooltip Overlay Authorizes Payment

- **Attack Type**: CSS Z-index Trick
- **Target**: E-commerce / SaaS Payment Pages
- **Vulnerability**: Invisible charge triggers
- **MITRE**: T1189
- **Impact**: Silent financial charge
- **Tools**: HTML/CSS, Payment Test Environments
- **Scenario**: Fake tooltip overlaps real payment confirmation button
- **Attack Steps**: 1. The attacker creates a pricing table with multiple subscription tiers. 2. Next to one of the plans is a small “?” icon that is supposed to show a tooltip explaining the plan. 3. The attacker creates a fake tooltip popup which actually overlays a real “Authorize Payment” button. 4. The tooltip looks like part of the page design but is placed using z-index: 9999 and transparent layering. 5. When a user clicks to close the tooltip or interact with the pricing box, they instead click the hidden payment authorization. 6. This is particularly effective with saved credit card or auto-pay features. 7. The attacker completes a one-time or recurring payment without victim knowledge. 8. The victim realizes the charge only after checking transaction logs.
- **Detection**: Inspect overlays for clickable finance elements
- **Solution**: Implement confirmation modals for all payments
- **Tags**: #paymentfraud #uiredress #zindextrap

## Collaboration Invite Trick via Frame

- **Attack Type**: JS Injection + Iframe Overlay
- **Target**: Cloud Docs (Google, Microsoft)
- **Vulnerability**: Collaboration invites without click validation
- **MITRE**: T1189
- **Impact**: Internal compromise via shared docs
- **Tools**: DOM Tools, JS Frameworks
- **Scenario**: Fake tool interface tricks user into joining infected doc
- **Attack Steps**: 1. A fake online whiteboard or note-taking app invites users to “Join a Shared Board.” 2. The visible “Join Board” button overlays a transparent iframe pointing to a legitimate Google Docs or Microsoft Office 365 document. 3. That document is controlled by the attacker and contains malicious macros, trackers, or phishing links. 4. The iframe is aligned so that the click registers on the “Accept Invitation” button below. 5. The user believes they’ve joined the shared workspace but instead granted access to a malicious actor. 6. The attacker gains a foothold to conduct internal phishing or drop malware. 7. This is often used in BEC (Business Email Compromise) operations. 8. Because the collaboration UI seems natural, the user doesn’t suspect foul play.
- **Detection**: Track invite acceptance from untrusted domains
- **Solution**: Require email confirmation before document access
- **Tags**: #collabhijack #clickjacking #phishingentry

## Hidden 2FA Push Approval via Continue Button

- **Attack Type**: Transparent Iframe
- **Target**: MFA Platforms (Okta, Duo)
- **Vulnerability**: Overlaying push approval with decoy UI
- **MITRE**: T1189
- **Impact**: Complete account takeover
- **Tools**: HTML/CSS, MFA Platform
- **Scenario**: “Continue” button hides a frame that approves 2FA push request
- **Attack Steps**: 1. A user logs into a fake company portal clone made by the attacker. 2. After entering credentials, they’re shown a “Continue to Dashboard” button. 3. Under this button lies a transparent iframe that has loaded the 2FA push approval screen (e.g., Okta Verify, Duo Push). 4. The attacker, simultaneously trying to log in to the real system using stolen credentials, triggers a real 2FA push request. 5. When the user clicks “Continue,” they unknowingly approve the push notification. 6. The attacker is instantly granted access and completes the login. 7. The victim thinks they’re being taken to their dashboard, unaware their 2FA just approved someone else’s session. 8. This technique is extremely effective when users are trained to approve MFA push prompts quickly.
- **Detection**: Alert on mismatched timing of login + push
- **Solution**: Require biometric or pin confirmation for push approvals
- **Tags**: #push2faabuse #mfaexploitation #clickhijack

## Video Site Tricks User to Share Location

- **Attack Type**: Hidden Iframe
- **Target**: Chrome, Firefox
- **Vulnerability**: Abuse of permission prompts via invisible layering
- **MITRE**: T1189
- **Impact**: Location leakage and user tracking
- **Tools**: HTML, JS, CSS
- **Scenario**: A fake video site places location permission request under a play button
- **Attack Steps**: 1. An attacker creates a fake video-streaming website offering “Exclusive Leaks” or “Behind the Scenes Footage.” 2. On the homepage is a large, enticing “Play Video” button. 3. The attacker embeds a hidden iframe exactly beneath the play button, loading the browser’s location-sharing prompt (e.g., navigator.geolocation) from a legitimate request. 4. Using absolute positioning and opacity set to zero, the iframe becomes invisible but still clickable. 5. When the user clicks “Play”, they unknowingly grant location access to the attacker’s domain. 6. Once granted, the attacker’s script can continually retrieve precise geolocation using the browser API. 7. The attacker may then use this information for stalking, targeted ads, or geo-specific phishing. 8. Most users won’t realize this until they inspect browser settings or receive odd content based on their location.
- **Detection**: Monitor for invisible permission requests during clicks
- **Solution**: Require user-initiated visible prompts for geolocation
- **Tags**: #locationjacking #geopermission #uiredressing

## Online Poll Triggers GitHub Star Action

- **Attack Type**: Transparent Iframe
- **Target**: GitHub Buttons, iframe overlays
- **Vulnerability**: Third-party widget framing without validation
- **MITRE**: T1189
- **Impact**: Social trust abuse, malicious reputation
- **Tools**: GitHub Buttons, HTML, CSS
- **Scenario**: Poll UI used to trick user into starring attacker’s repo
- **Attack Steps**: 1. A fake web page invites users to vote on “Which coding language is best in 2025?” 2. Each voting option (“Python”, “JavaScript”, “Rust”) is a button styled with HTML/CSS. 3. Hidden beneath each of these buttons is an iframe containing GitHub’s “Star Repository” widget. 4. The iframe is aligned so the user’s vote simultaneously stars a repository controlled by the attacker. 5. Each vote is mapped to a different project, inflating stars and boosting project visibility artificially. 6. This method can help attackers push malicious packages (e.g., typo-squatting packages) by making them appear popular. 7. The user never knows they starred anything — the click seems part of voting. 8. The attacker gains fake credibility, which may be used to deceive developers in the open-source community.
- **Detection**: Inspect click behavior on widgets during voting interactions
- **Solution**: Prevent widgets from being embedded in cross-origin iframes
- **Tags**: #clickjacking #socialmanipulation #opensourceabuse

## Survey Page Accepts Calendar Invite

- **Attack Type**: Hidden Frame + OAuth
- **Target**: Google Calendar
- **Vulnerability**: Calendar invitation with malicious intent
- **MITRE**: T1189
- **Impact**: Delayed phishing attack
- **Tools**: Google Calendar, HTML/CSS
- **Scenario**: Fake survey trick makes user add malicious calendar event
- **Attack Steps**: 1. The attacker hosts a fake customer feedback page promising a gift card after completion. 2. One of the final steps includes a big “Submit and Claim Reward” button. 3. A hidden iframe lies behind this button, aligned to click a “Yes” on a Google Calendar invite for a malicious event. 4. This event includes a phishing link or Zoom session impersonating HR or tech support. 5. Once clicked, the invite is added to the user’s Google Calendar silently. 6. Many users rely on mobile calendar notifications and may later click the phishing link without suspicion. 7. This technique builds a timed attack vector — triggering the final payload days later. 8. Attackers exploit trust in calendar notifications and the illusion of consent from the initial “claim” step.
- **Detection**: Monitor unusual calendar invite additions from unknown sources
- **Solution**: Enforce confirmation before adding calendar events
- **Tags**: #calendarjacking #oauthclick #socialengineering

## Profile Picture Upload Triggers Like Action

- **Attack Type**: CSS Z-index Trick
- **Target**: Instagram, Social Widgets
- **Vulnerability**: Misuse of engagement UI under decoy button
- **MITRE**: T1189
- **Impact**: Fake social signals, brand reputation abuse
- **Tools**: HTML/CSS, Instagram Widget
- **Scenario**: Fake profile update interface masks a “Like” button from attacker’s post
- **Attack Steps**: 1. A website claiming to offer professional headshot AI editing asks users to upload a photo. 2. The “Upload & Preview” button is large and centered on the page. 3. Behind it is a transparent iframe that loads an Instagram “Like” button for an attacker’s spammy influencer account. 4. The iframe is positioned with precise z-index layering so the user’s click gets intercepted. 5. While users think they’re uploading, they’re actually boosting the engagement on a malicious social media post. 6. Attackers can monetize this via fake sponsors, scam giveaways, or pyramid schemes. 7. The user receives a generic “Success” message to mask any suspicion. 8. Later, users may discover odd activity in their social profiles but not associate it with this interaction.
- **Detection**: Log UI interactions with hidden widget positions
- **Solution**: Prevent social buttons from being embedded cross-origin
- **Tags**: #engagementfraud #instascam #zindexabuse

## Crypto Wallet Connect via Clickbait Link

- **Attack Type**: Transparent Iframe + Web3 Abuse
- **Target**: Ethereum, MetaMask, Web3.js
- **Vulnerability**: Misleading wallet connection via iframe
- **MITRE**: T1189
- **Impact**: Wallet compromise, crypto theft
- **Tools**: MetaMask, Web3.js
- **Scenario**: Fake “Claim Airdrop” button triggers wallet connection
- **Attack Steps**: 1. The attacker builds a fake promotional page advertising a new cryptocurrency airdrop. 2. The page includes a large button that says “Claim Your Free $50 Now.” 3. Under this button, a hidden iframe loads a legitimate Web3 eth_requestAccounts prompt to connect the victim’s wallet. 4. When the user clicks, the attacker’s dApp receives wallet access and potentially requests signature permissions. 5. If the user has MetaMask auto-approve enabled or clicks again blindly, they might authorize a malicious transaction. 6. The attacker can now drain assets, deploy malicious smart contracts, or phish for seed phrases. 7. Users often blame the wallet or token platform without realizing they were misled at the interface level. 8. The attacker’s address is now linked to multiple drained wallets for laundering.
- **Detection**: Track unsolicited wallet connection prompts
- **Solution**: Display full prompt context before dApp connection
- **Tags**: #web3jacking #cryptoclick #airdrophack

## Decoy Support Chat Submits 2FA Token

- **Attack Type**: Hidden Field + Overlay
- **Target**: MFA Services (Google, Duo, Okta)
- **Vulnerability**: Social engineering to harvest tokens
- **MITRE**: T1189
- **Impact**: MFA bypass, session hijack
- **Tools**: HTML, JS, CSS, MFA Platforms
- **Scenario**: Fake support chat field submits active 2FA code to attacker
- **Attack Steps**: 1. A fake customer support page shows a live chat window asking the user for assistance. 2. Below the chat box is a message: “To help you better, please paste your 2FA code.” 3. The visible text field is a fake input, while behind it, a hidden iframe submits the content directly to a backend server or another service (e.g., Google form, Telegram bot). 4. When the user pastes their active code and presses enter, it gets sent in real-time. 5. The attacker simultaneously logs into the real account, using that 2FA token to bypass MFA protection. 6. Once successful, the attacker gains full account access. 7. The user gets a “Thanks, our support team will be with you shortly” message, hiding the damage. 8. This is especially effective against users who recently received legitimate 2FA prompts.
- **Detection**: Log backend submissions for tokens
- **Solution**: Train users to never share OTPs in plaintext
- **Tags**: #2fastealing #supportfraud #mfabypass

## Fake Error Page Triggers OAuth Approval

- **Attack Type**: CSS Overlay + OAuth Abuse
- **Target**: Gmail, Outlook
- **Vulnerability**: Misleading re-login page hides approval action
- **MITRE**: T1189
- **Impact**: Persistent unauthorized app access
- **Tools**: HTML/CSS/JS, Google OAuth
- **Scenario**: Tricked into approving third-party app access via fake error page
- **Attack Steps**: 1. A phishing site shows a “Session Timed Out” screen that looks identical to Gmail or Outlook. 2. The user is shown a “Click here to re-login” button styled to match the service. 3. Behind that button is a transparent iframe that loads an OAuth consent screen to authorize a malicious app. 4. Because the user is expecting to log back in, they click and unknowingly approve the app. 5. The attacker gains persistent access to emails, drive content, or calendar. 6. This method is used heavily in business email compromise (BEC) attacks. 7. The fake session timeout gives urgency and a sense of legitimacy. 8. Victims don’t realize until attackers start sending or reading emails from their account.
- **Detection**: Monitor OAuth approvals from unexpected sites
- **Solution**: Always use browser address bar validation before clicking
- **Tags**: #oauthfraud #sessionhijack #emailbreach

## Click-to-Close Banner Loads Drive Malware

- **Attack Type**: Iframe Injection
- **Target**: Google Drive, Dropbox, OneDrive
- **Vulnerability**: Malicious file download via deceptive close button
- **MITRE**: T1189
- **Impact**: Malware deployment, endpoint compromise
- **Tools**: HTML, Google Drive API
- **Scenario**: “Close Ad” button overlays malicious download trigger
- **Attack Steps**: 1. A user visits a shady site filled with ads, including one fake pop-up styled like an alert. 2. The ad includes a red “X” button or “Close Ad” link in the corner. 3. Under this close button, an invisible iframe points to a malicious file stored on Google Drive, Dropbox, or OneDrive. 4. When the user clicks to close the ad, the download is silently initiated. 5. This file might contain trojans, password stealers, or PDF exploits. 6. Many browsers will auto-download without user interaction depending on settings. 7. Victims assume the ad was closed — unaware malware just entered their Downloads folder. 8. The attacker relies on poor visibility and common habits of closing annoying pop-ups.
- **Detection**: Alert on downloads triggered from hidden layers
- **Solution**: Enforce download confirmations with origin validation
- **Tags**: #malwareclick #driveexploit #hiddenframe

## Spoofed Notification Opt-In via Quiz Prize

- **Attack Type**: Notification Hijack
- **Target**: Push Notification APIs
- **Vulnerability**: Misused alerting through click hijack
- **MITRE**: T1189
- **Impact**: Persistent phishing, user manipulation
- **Tools**: Push API, JavaScript
- **Scenario**: "Claim Your Prize" button grants notification access
- **Attack Steps**: 1. A fake “Congratulations! You’ve won!” banner appears at the end of a quiz. 2. The “Claim Now” button sits atop an invisible iframe that triggers the browser’s Notification.requestPermission() call. 3. Clicking the button registers the attacker’s domain for push notifications. 4. Over the next few days, the attacker sends misleading alerts like “You’ve been hacked!” or “Free antivirus expired — click to fix.” 5. Each alert links to a phishing or malware domain. 6. Victims think they’re system notifications and often fall for urgent messages. 7. Push notifications work even when the browser isn’t open, increasing risk. 8. This attack abuses users’ willingness to click exciting prompts.
- **Detection**: Log sudden notification permissions granted
- **Solution**: Require full-screen opt-in prompts with domain shown
- **Tags**: #pushspam #fakealert #clickjacking

## Mouse Hover Triggers Donation Action

- **Attack Type**: Mouse Tracking + Overlay
- **Target**: Stripe, PayPal
- **Vulnerability**: Hover-based clickjacking on payment forms
- **MITRE**: T1189
- **Impact**: Small unauthorized payments at scale
- **Tools**: HTML/CSS/JS
- **Scenario**: Hovering mouse accidentally donates via hidden iframe
- **Attack Steps**: 1. A user visits a donation campaign or charity-style website. 2. The page tracks mouse movement and waits for the cursor to hover near the “Learn More” section. 3. When hovering is detected, a hidden iframe appears briefly under the cursor, aligned to a real donation form’s “Confirm” button. 4. A timed delay makes the button visible only for a split-second — enough to register the hover as a click if user is clicking rapidly. 5. The form submits a micro-donation or preloaded value using saved payment details. 6. Victims only find out when checking their payment transaction emails. 7. This technique uses anticipation and mouse momentum to force accidental consent. 8. The attacker can automate the same technique across multiple campaigns to accumulate money.
- **Detection**: Monitor donation patterns for short interval clicks
- **Solution**: Require visible confirmation steps before payment
- **Tags**: #hoverclick #microfraud #overlaytrap

## Free eBook Button Triggers YouTube Subscription

- **Attack Type**: Transparent Iframe
- **Target**: YouTube Subscribe Widget
- **Vulnerability**: Invisible widget subscription
- **MITRE**: T1189
- **Impact**: Artificial trust building, social abuse
- **Tools**: HTML, CSS, YouTube Subscribe Widget
- **Scenario**: Trick user into subscribing to malicious YouTube channel
- **Attack Steps**: 1. The attacker creates a website offering “Free eBook downloads” for tech guides, productivity hacks, or academic prep. 2. On the page, a large “Download eBook” button is presented. 3. Beneath this button, the attacker embeds a transparent iframe that loads the official YouTube Subscribe button for their own malicious or scammy channel. 4. The iframe is styled with zero opacity and absolutely positioned to align perfectly under the visible button. 5. When the user clicks to download the book, they are unknowingly subscribing to the attacker’s channel. 6. The attacker then pushes scammy live streams, crypto giveaways, or phishing via YouTube community posts to their growing fake subscriber base. 7. The user may never realize the subscription unless they visit their own YouTube account and check subscriptions. 8. The attacker builds credibility to later abuse platform algorithms and push misinformation or scams.
- **Detection**: Monitor invisible widget interactions
- **Solution**: Disallow iframe embedding for critical UI actions
- **Tags**: #youtubefraud #clickjacking #subtrap

## Job Application Button Triggers Login to Attacker Account

- **Attack Type**: Overlay + Session Hijack
- **Target**: Job Portals, Hidden Frames
- **Vulnerability**: Form hijack using account context
- **MITRE**: T1189
- **Impact**: Session misattribution, identity misuse
- **Tools**: HTML, JavaScript, Browser Autofill
- **Scenario**: Fake job portal button logs user into attacker's account
- **Attack Steps**: 1. The attacker creates a fake job portal that mimics a popular hiring platform UI. 2. The “Apply Now” button appears above a hidden iframe containing a login page for a legitimate job site. 3. The iframe is pre-loaded with the attacker’s credentials via browser autofill or preset cookies. 4. When the user clicks “Apply Now,” the iframe registers a form submission logging the user into the attacker's account instead of their own. 5. Now, any job applied for, resume uploaded, or message sent will appear under the attacker’s identity. 6. The attacker can later harvest this activity, intercept recruiter communications, or redirect interviews. 7. This tactic allows identity misuse without the victim even knowing they were logged into the wrong account. 8. It's commonly used in career scams or fake employer phishing attempts.
- **Detection**: Track unexpected session activity
- **Solution**: Bind sessions to IP/device fingerprinting
- **Tags**: #sessionhijack #identityabuse #clickfraud

## Fake File Upload Triggers OAuth Consent

- **Attack Type**: Hidden Frame
- **Target**: Google OAuth API
- **Vulnerability**: Misused file upload interface
- **MITRE**: T1189
- **Impact**: Unauthorized document access
- **Tools**: HTML, Google Drive OAuth
- **Scenario**: Deceptive file upload grants cloud access
- **Attack Steps**: 1. A webpage pretends to be an “online PDF compressor” or “resume optimizer.” 2. When users click “Upload File”, a transparent iframe triggers an OAuth approval dialog requesting access to the user’s Google Drive. 3. The iframe is aligned behind the upload button using CSS positioning. 4. The unsuspecting user, thinking they’ve uploaded a document, actually clicks “Allow” on the consent screen. 5. Now, the attacker’s app has persistent access to the user’s Google Drive files, including confidential resumes, IDs, contracts, etc. 6. The webpage then shows a fake progress bar and says “Optimization complete” to mask the background data theft. 7. The user believes everything worked, having no idea their entire drive was compromised. 8. The attacker silently scrapes and exfiltrates data for fraud or resale.
- **Detection**: Log unexpected OAuth consents tied to uploads
- **Solution**: Isolate OAuth from upload workflows
- **Tags**: #driveabuse #oauthclick #clickjacking

## Fake Profile Customizer Sends Message from Victim Account

- **Attack Type**: Overlay + Message Send
- **Target**: Facebook, Instagram, X APIs
- **Vulnerability**: UI masking of communication actions
- **MITRE**: T1189
- **Impact**: Social spread of phishing via victim identity
- **Tools**: Social Platform APIs, JS
- **Scenario**: Trick users into messaging contacts
- **Attack Steps**: 1. The attacker builds a page that mimics a “Profile Skin Customizer” for a popular social app. 2. Users click “Apply New Look” expecting a design change. 3. A hidden iframe behind the button triggers a "Send Message" action via the platform’s API, pre-filled with a phishing link or scam invite. 4. The victim unknowingly sends this message to a friend, increasing legitimacy and reach. 5. Friends receive the link, thinking it’s a recommendation or genuine message. 6. The attacker repeats the process across more users via chain attacks. 7. The victim is unaware they initiated any message and blames account hacking later. 8. This clickjacking variation exploits both UI deception and contact trust.
- **Detection**: Log spontaneous message actions
- **Solution**: Implement multi-step message confirmations
- **Tags**: #messagestealing #socialspread #clickfraud

## Transparent Overlay Triggers Cryptocurrency Payment

- **Attack Type**: Iframe Payment Abuse
- **Target**: MetaMask, Smart Contracts
- **Vulnerability**: Click-to-pay hijack using iframe
- **MITRE**: T1189
- **Impact**: Micro theft, financial abuse
- **Tools**: Web3.js, MetaMask
- **Scenario**: Malicious page triggers small ETH/USDT payment via hidden interface
- **Attack Steps**: 1. The attacker builds a “Donate to Support Open Source” webpage. 2. The donation button hides a smart contract interaction beneath it via iframe. 3. When clicked, the user unknowingly signs a transaction from their MetaMask wallet. 4. The transaction sends a small amount of ETH or USDT to the attacker’s address. 5. The site then says “Thank you for your donation!” making the user feel they took a harmless action. 6. Attackers automate this at scale to gather hundreds of small payments daily. 7. Victims don’t realize until reviewing wallet transaction history. 8. This type of micro-theft is hard to detect due to low amounts and legitimate-appearing front.
- **Detection**: Track wallet triggers from untrusted domains
- **Solution**: Add full-screen confirmation for crypto tx
- **Tags**: #cryptojacking #micropaymenttheft

## Captcha Button Approves Browser Notification

- **Attack Type**: Notification Hijack
- **Target**: Browser Notification API
- **Vulnerability**: Fake CAPTCHA triggers permission
- **MITRE**: T1189
- **Impact**: Persistent user manipulation
- **Tools**: HTML, JS
- **Scenario**: “I am not a robot” triggers notification permission grant
- **Attack Steps**: 1. A fake site displays a CAPTCHA-style prompt with a checkbox that says “I’m not a robot.” 2. Beneath this checkbox is a hidden iframe that executes Notification.requestPermission() on click. 3. Users clicking the checkbox unknowingly allow browser notifications from attacker’s domain. 4. Attackers then push scammy alerts: “Antivirus expired,” “You’ve won,” or “Click to fix hacked account.” 5. These alerts mimic native OS notifications and run persistently. 6. Victims often click without realizing the source is a rogue site visited earlier. 7. Attackers rotate domains and payloads to maintain reach. 8. This method abuses the trust of CAPTCHA interfaces and users' habituation to clicking them.
- **Detection**: Detect unexpected notification prompts during CAPTCHA
- **Solution**: Restrict notification prompts to visible user-initiated flows
- **Tags**: #captchaabuse #notifjacking #clickfraud

## Survey Page Click Sends Email on Behalf of Victim

- **Attack Type**: Overlay + Email API
- **Target**: Email.js, Google Mail API
- **Vulnerability**: Click-based auto-email trigger
- **MITRE**: T1189
- **Impact**: Mass spam from trusted identities
- **Tools**: Email JS, CSS
- **Scenario**: User is tricked into emailing their entire contact list
- **Attack Steps**: 1. A fake personality survey asks fun questions like “What kind of animal are you?” 2. The final page includes a “See My Result” button that appears to load a shareable result. 3. Behind this button, an iframe triggers a call to an email API that sends templated messages from the user’s account. 4. The message says something like “Check out this quiz! I scored as a Tiger!” with a link to the attack site. 5. It sends this to all contacts using autofilled or authorized email access. 6. Recipients think it's genuine and take the bait, causing a chain effect. 7. The user sees a fake result page, unaware they just spammed dozens of friends. 8. The attacker scales this tactic across multiple fake surveys for viral spread.
- **Detection**: Analyze bulk emails from quiz-type domains
- **Solution**: Require multi-step email sharing workflows
- **Tags**: #socialspam #emailclickjacking #autospam

## Fake Image Editor Triggers Social Media Share

- **Attack Type**: Hidden Widget Share
- **Target**: Facebook, Twitter Widgets
- **Vulnerability**: Unconsented social share
- **MITRE**: T1189
- **Impact**: Social hijack, viral phishing
- **Tools**: HTML, Twitter/FB Share Widgets
- **Scenario**: Trick users into sharing attacker link via masked image edit interface
- **Attack Steps**: 1. A website poses as an AI-based meme or image generator. 2. After editing or uploading an image, users are prompted to click “Download & Share.” 3. Behind this button, a hidden widget is triggered that shares a link to the attacker’s page on Twitter or Facebook. 4. The share post contains custom text like “Try this new AI editor!” with a referral or phishing link. 5. The user may be logged into the social platform in the background, so the share executes silently. 6. Their profile posts the message, tricking friends and followers. 7. The attacker monitors social shares for reach and virality. 8. The user continues editing, never realizing a post was made on their behalf.
- **Detection**: Track one-click widget triggers in upload workflows
- **Solution**: Require previews before posting via share widgets
- **Tags**: #socialclickbait #autoshare #clickjacking

## Fake Support Form Initiates Password Reset

- **Attack Type**: Hidden Form Submission
- **Target**: Gmail, Twitter, Webmail Providers
- **Vulnerability**: Form click triggers password recovery
- **MITRE**: T1189
- **Impact**: Disruption, phishing pivot
- **Tools**: HTML, Password Reset API
- **Scenario**: Victim clicks “Submit” and triggers account reset flow
- **Attack Steps**: 1. A user visits a fake customer support page claiming to help with email problems. 2. The “Submit” button supposedly sends a support ticket. 3. Behind it, a hidden form submits a password reset request for a popular account (e.g., Gmail, Twitter) using the victim’s email. 4. The attacker simultaneously tries to guess security questions or intercept reset emails via phishing. 5. Even if the reset fails, the attacker causes confusion and spams the user. 6. In best case for attacker, victim is phished and the reset link intercepted. 7. The victim gets a “You requested password reset” email but didn’t realize it was triggered during a click. 8. This can disrupt account access or serve as part of a larger takeover attempt.
- **Detection**: Monitor for reset triggers from unusual origins
- **Solution**: Add CAPTCHA and alert reset flows with detailed logs
- **Tags**: #accounttakeover #resetspam #clicktrap

## “Check Weather” Button Grants Webcam Access

- **Attack Type**: Media Permission Abuse
- **Target**: MediaDevices API, WebRTC
- **Vulnerability**: Misused permission under weather tool
- **MITRE**: T1189
- **Impact**: Privacy breach, surveillance
- **Tools**: HTML, MediaDevices API
- **Scenario**: Fake weather tool triggers camera permission
- **Attack Steps**: 1. A weather forecast site shows a big “Check Weather Near You” button. 2. Clicking the button is expected to give regional forecast data. 3. Hidden behind the button is a browser permission request for webcam access, triggered via iframe. 4. If allowed, attacker’s script captures webcam feed silently. 5. User sees a radar map or generic weather chart while their camera is live. 6. Attackers record footage, screenshots, or use motion detection for further intrusion. 7. This invasion is possible due to abuse of device permissions and misleading UIs. 8. Many users click without reading permission prompts, especially if they appear legitimate.
- **Detection**: Monitor and log webcam permission grants
- **Solution**: Only allow media access after explicit user consent
- **Tags**: #webcamhijack #privacyleak #clickjacking

