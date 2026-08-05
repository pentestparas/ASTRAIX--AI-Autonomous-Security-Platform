# Browser Security → WebAssembly (WASM) Abuse Attacks

## Obfuscated Malware Loader via WebAssembly

- **Attack Type**: Obfuscation of Payloads
- **Target**: End users visiting malicious sites
- **Vulnerability**: WASM as payload wrapper
- **MITRE**: T1027
- **Impact**: Undetected malware delivery
- **Tools**: WASM Compiler, Browser DevTools
- **Scenario**: WASM module used to hide malware logic from static scanners
- **Attack Steps**: 1. The attacker writes a simple malware payload in C or Rust that includes beaconing and fileless execution logic. 2. They compile this code to WebAssembly using tools like Emscripten or Rust’s wasm32 target. 3. The resulting .wasm file contains the main malicious logic in a binary format that can’t be analyzed easily with plain text search. 4. A small JavaScript stub is written to load and instantiate the WASM module inside a web page. 5. The stub hides behind a legitimate-looking app like a file converter or speed test. 6. When a user opens the site, the WASM module executes, and malicious behavior begins (e.g., communicating with a command-and-control server or dropping in-memory shellcode). 7. Antivirus and static detection tools scanning the HTML and JavaScript do not flag the .wasm code because it is opaque. 8. This evades typical client-side scanning and allows payloads to persist on delivery servers without signature-based blocks.
- **Detection**: Behavior analysis of WASM runtime
- **Solution**: Analyze WASM modules in sandboxes
- **Tags**: #wasmloader #payloadobfuscation #evadingdetection

## Hidden Crypto Miner Using WASM in Background Tab

- **Attack Type**: Browser Crypto Mining
- **Target**: General browser users
- **Vulnerability**: Idle tab abuse + WASM miner
- **MITRE**: T1496
- **Impact**: Device slowdown, battery drain
- **Tools**: CoinHive Clone, Chrome Task Manager
- **Scenario**: Background tab executes CPU-heavy miner after user becomes idle
- **Attack Steps**: 1. The attacker clones or modifies a crypto mining script that uses WASM for fast math operations (e.g., XMRig compiled to WASM). 2. The script checks if the current tab is not in focus using the document.hidden property. 3. When the user switches tabs, the miner activates quietly using requestAnimationFrame or setInterval. 4. It uses WebAssembly to run high-speed hash computations, consuming the user’s CPU. 5. If the user returns to the tab, the mining activity stops instantly to avoid suspicion. 6. The CPU drain can go unnoticed for hours or days, especially on laptops or mobile devices. 7. The attacker receives steady cryptocurrency rewards from many affected users. 8. This abuse leverages the efficiency of WASM and browser event APIs to hide in plain sight.
- **Detection**: Monitor CPU spikes in hidden tabs
- **Solution**: Block WASM mining with extensions
- **Tags**: #wasmmining #cryptojacking #browsertiming

## WASM Heap Spray for JavaScript Engine Exploit

- **Attack Type**: WASM Heap Spraying
- **Target**: JavaScript engines in browsers
- **Vulnerability**: Weak memory isolation in WASM
- **MITRE**: T1203
- **Impact**: Potential RCE via browser
- **Tools**: Web Fuzzer, JSHeapSpray
- **Scenario**: Fill WASM linear memory with crafted payloads to exploit JIT issues
- **Attack Steps**: 1. The attacker targets a vulnerability in a JavaScript engine (e.g., V8) known to mishandle certain memory layouts. 2. They write a script that allocates a large WebAssembly linear memory buffer (e.g., 16MB). 3. This memory is filled with repeating patterns designed to overwrite adjacent objects or confuse the browser’s JIT compiler. 4. Through carefully placed markers, they hope to trigger memory corruption or control flow hijacking. 5. If successful, this can lead to arbitrary code execution in the browser context. 6. Although experimental and not always successful, this technique is being actively researched. 7. Such heap sprays using WASM can evade some mitigations applied to JavaScript-based attacks. 8. The payload stays under the radar due to WASM’s binary nature.
- **Detection**: Monitor large memory allocs from WASM
- **Solution**: Harden engine memory boundaries
- **Tags**: #heapspray #wasmexploit #jitbypass

## Obfuscated WASM Command Beacon in Game Widget

- **Attack Type**: Obfuscation of Payloads
- **Target**: Websites embedding widgets
- **Vulnerability**: Hidden C2 beacon inside WASM
- **MITRE**: T1071.001
- **Impact**: Covert communication from browser
- **Tools**: Burp Suite, DevTools, Wireshark
- **Scenario**: Malicious WASM hidden inside a web game widget silently beacons C2
- **Attack Steps**: 1. The attacker creates a web-based mini-game (e.g., pong, puzzle) hosted on a popular blog widget platform. 2. Inside the game's logic, they load a small .wasm file that is compiled from a C module containing a network beacon routine. 3. The WASM module, once initialized, periodically sends encrypted pings to the attacker’s C2 server. 4. These pings are disguised as score updates or analytics packets. 5. The game functions normally and serves as a distraction to the malicious communication. 6. Since the logic is inside WASM, static analysis tools looking at the HTML or JavaScript don’t catch it. 7. The attacker receives silent updates whenever users load or interact with the widget. 8. This demonstrates WASM being abused for stealthy persistence and outbound traffic.
- **Detection**: Monitor C2 endpoints in network logs
- **Solution**: Block unknown WASM outbound calls
- **Tags**: #wasmbeacon #c2browser #maliciouswidget

## CPU Abuse via Ad-Based Crypto Miner in WASM

- **Attack Type**: Browser Crypto Mining
- **Target**: Websites running ad scripts
- **Vulnerability**: Hidden iframe + WASM miner
- **MITRE**: T1496
- **Impact**: CPU exhaustion, user impact
- **Tools**: Fake AdScript, Wireshark
- **Scenario**: WASM-based miner embedded in fake ad iframe
- **Attack Steps**: 1. A fake ad company provides a script that site owners embed for monetization. 2. The script injects a hidden iframe that loads a miner compiled into WASM. 3. When the page loads, the iframe starts a crypto mining loop that consumes CPU, even when not visible. 4. The iframe uses Web Workers to parallelize mining tasks, increasing CPU usage. 5. The user sees a regular ad placeholder, but their device performance drops. 6. No direct interaction is needed for mining to begin. 7. The attacker profits off thousands of users unknowingly mining coins for them. 8. Since the miner is WASM-compiled, it bypasses most traditional browser ad filters.
- **Detection**: Monitor CPU via browser dev tools
- **Solution**: Block suspicious ad domains
- **Tags**: #admining #iframeabuse #wasmminer

## WASM Obfuscated Payload Loaded from GitHub CDN

- **Attack Type**: Obfuscation of Payloads
- **Target**: Public CDNs, open source projects
- **Vulnerability**: Hosting malicious WASM on trusted infra
- **MITRE**: T1105
- **Impact**: Trusted platform used for malware
- **Tools**: GitHub Pages, WASM Viewer
- **Scenario**: Malware hosted as a .wasm file on GitHub Pages/CDN
- **Attack Steps**: 1. The attacker compiles malicious logic into a .wasm file and uploads it to a GitHub Pages-hosted project. 2. The WASM file appears to be part of a UI framework or utility. 3. Their main phishing or malware site includes this file via a <script> or fetch() call. 4. When the file is loaded, the embedded payload executes and begins malicious behavior (e.g., fingerprinting, beaconing, memory read). 5. Since it’s hosted on GitHub, traffic appears legitimate and secure. 6. The file is rarely scanned, as .wasm is not a common extension for AV. 7. The attacker benefits from free hosting and HTTPS protection from GitHub. 8. This showcases how trusted CDNs can be abused for WASM malware delivery.
- **Detection**: Scan WASM from public sources
- **Solution**: Vet 3rd-party CDN dependencies
- **Tags**: #cdnabuse #githubwasm #wasmloader

## Stealth Miner via WebAssembly + Web Workers

- **Attack Type**: Browser Crypto Mining
- **Target**: Browsers supporting multi-threaded JS
- **Vulnerability**: Web Workers used with WASM
- **MITRE**: T1496
- **Impact**: Extended resource hijack
- **Tools**: Chrome Profiler, CoinHive Clone
- **Scenario**: Web Worker threads used to parallelize WASM mining
- **Attack Steps**: 1. The attacker writes a WASM-based crypto miner and wraps it inside multiple Web Worker threads. 2. When the page loads, each worker initializes the WASM module independently. 3. This allows CPU-bound operations to run in parallel, maximizing mining output. 4. The mining begins automatically, hidden behind a website offering streaming or tools. 5. To evade detection, the script limits CPU usage to 50% and pauses during user interaction. 6. Dev tools show threads but users may not notice the pattern unless CPU usage is analyzed. 7. The attacker receives earnings through their mining pool account. 8. This method improves efficiency and stealth using standard browser features.
- **Detection**: Inspect thread count in dev tools
- **Solution**: Disable worker-based mining
- **Tags**: #webworkers #threadedminer #wasmefficiency

## Heap Spray via WASM to Achieve JS Object Overwrite

- **Attack Type**: WASM Heap Spraying
- **Target**: Browsers with JS/WASM integration
- **Vulnerability**: Engine allowing memory overlap
- **MITRE**: T1203
- **Impact**: Memory corruption → RCE
- **Tools**: Custom Fuzzer, Heap Viewer
- **Scenario**: WASM memory used to corrupt adjacent JS objects
- **Attack Steps**: 1. A vulnerability in object allocation in JS engines allows overwriting neighboring memory. 2. The attacker creates a large WebAssembly memory buffer and fills it with crafted data patterns. 3. They use JS to allocate adjacent objects that the WASM memory will overwrite. 4. When the spray is successful, object pointers or internal values are modified. 5. This could lead to logic manipulation, crash, or arbitrary code execution. 6. The entire attack is done from within the browser context. 7. It relies on heap layout predictions and extensive testing. 8. While difficult, this represents real-world WASM abuse in exploit chains.
- **Detection**: Monitor abnormal object behavior
- **Solution**: Patch JS engine memory rules
- **Tags**: #heapspray #objectoverwrite #wasmbug

## Fileless Persistence Using WASM Memory

- **Attack Type**: Obfuscation of Payloads
- **Target**: Browsers with WASM support
- **Vulnerability**: Fileless in-browser execution
- **MITRE**: T1055
- **Impact**: In-memory persistence
- **Tools**: DevTools, Volatility
- **Scenario**: Payload executes entirely in-memory using WASM, no file drops
- **Attack Steps**: 1. The attacker writes a payload in C that performs some malicious logic (e.g., download & exec, shell). 2. This code is compiled into WASM and hosted on a website. 3. A user visits the site, and JS loads the .wasm module into browser memory. 4. The code runs entirely in memory — nothing is downloaded or written to disk. 5. This avoids triggering file-based antivirus scanners. 6. Once executed, the WASM can create hidden DOM elements or backdoor browser storage. 7. When the page is closed, traces are minimal. 8. This tactic is ideal for temporary, stealthy attacks.
- **Detection**: Analyze browser memory dumps
- **Solution**: Use runtime memory protection
- **Tags**: #fileless #wasmmemory #nodropattack

## Obfuscated Credential Stealer via WASM Module

- **Attack Type**: Obfuscation of Payloads
- **Target**: Malicious phishing pages
- **Vulnerability**: JS-WASM combo for keylogging
- **MITRE**: T1056.001
- **Impact**: Credential theft via browser
- **Tools**: Emscripten, Browser DevTools
- **Scenario**: Keylogging logic hidden in WASM and triggered via JS events
- **Attack Steps**: 1. The attacker writes a keylogger in C or Rust and compiles it to WASM. 2. This WASM module listens for keystroke events passed from JS. 3. The attacker embeds this in a malicious login page (e.g., fake bank site). 4. JS captures keypresses and forwards them to the WASM function, which encodes and buffers the data. 5. At intervals, the WASM module sends the keystroke logs to an attacker-controlled server. 6. All logic is hidden in .wasm, making static analysis of JS useless. 7. The site appears clean in most scanners, but credentials are being exfiltrated. 8. This demonstrates WASM’s use in real-time data theft.
- **Detection**: Watch outbound WASM calls
- **Solution**: Prevent WASM execution on login pages
- **Tags**: #wasmkeylogger #obfuscation #phishing

## WASM Miner Triggered by User Scroll

- **Attack Type**: Browser Crypto Mining
- **Target**: Users visiting shady blog sites
- **Vulnerability**: Scroll-triggered WASM execution
- **MITRE**: T1496
- **Impact**: Resource abuse without suspicion
- **Tools**: JS Event API, XMRig-WASM
- **Scenario**: Hidden miner begins only when user scrolls the page to avoid early detection
- **Attack Steps**: 1. The attacker writes a crypto miner compiled to WebAssembly (e.g., using XMRig with Emscripten). 2. They embed the script on a malicious blog or fake news site. 3. The script waits for the user to interact—specifically, for a scroll event. 4. Once triggered, the miner starts in the background using WebAssembly, avoiding CPU spikes during page load. 5. The script uses Web Workers to distribute the mining task across threads and caps CPU usage to remain stealthy. 6. Users are unaware as the site appears static and trustworthy. 7. The longer the user stays on the page, the more cryptocurrency is mined for the attacker. 8. This attack cleverly ties miner activity to natural user behavior.
- **Detection**: Analyze site behavior on interaction
- **Solution**: Disable JS/WASM on untrusted sites
- **Tags**: #wasmining #scrolltrigger #stealthcrypto

## WASM Payload Encoded Inside Image File

- **Attack Type**: Obfuscation of Payloads
- **Target**: Users loading media-heavy pages
- **Vulnerability**: Hidden WASM in image via steganography
- **MITRE**: T1027
- **Impact**: Evades static scanners and firewalls
- **Tools**: StegoWASM, DevTools
- **Scenario**: Malware .wasm payload embedded in an image file and extracted via JavaScript
- **Attack Steps**: 1. The attacker hides a compiled .wasm binary inside the pixel data of a .png file. 2. JavaScript code on a web page loads the image via <img> and reads the binary data using Canvas API. 3. It decodes the WASM module from pixel values and passes it to WebAssembly.instantiate(). 4. The payload executes in memory without ever appearing as a standalone file. 5. Since the image looks harmless and is served from a trusted CDN, it bypasses basic detection. 6. The actual script tag on the page is only a few lines long, appearing benign. 7. Once loaded, the WASM module performs fingerprinting or drops other in-memory modules. 8. This demonstrates advanced payload obfuscation leveraging multimedia APIs.
- **Detection**: Monitor image decoding logic in JS
- **Solution**: Restrict use of image-to-binary conversion
- **Tags**: #steganography #wasmhidden #evadedetection

## Heap Spray with WASM Memory Overflow on Mobile Browser

- **Attack Type**: WASM Heap Spraying
- **Target**: Mobile JS/WASM engines
- **Vulnerability**: Poor bounds check on linear memory
- **MITRE**: T1203
- **Impact**: Potential RCE or DoS on mobile
- **Tools**: Mobile Browser, Custom WASM Code
- **Scenario**: Overfills linear memory on mobile JS engine to cause crash or exploitation
- **Attack Steps**: 1. The attacker crafts a WASM module with linear memory exceeding the typical buffer (e.g., 64MB). 2. The module allocates structures that fill and overflow the memory buffer intentionally. 3. This is run inside a mobile-optimized web app or PWA, where memory protections are often weaker. 4. The JS glue code surrounding WASM suppresses errors using try/catch, hiding the overflow from the user. 5. If the browser doesn’t enforce strict bounds checking, adjacent objects or function pointers may get overwritten. 6. This can result in crashes, memory leaks, or exploitation depending on the engine. 7. Mobile platforms often lag behind in WASM patching, making this more potent. 8. This attack is a known experimental technique in exploit dev circles.
- **Detection**: Analyze crash dumps from mobile sites
- **Solution**: Enforce stricter heap boundaries
- **Tags**: #wasmmobile #heapspray #overflow

## Fake Chrome Extension Mining WASM in Background

- **Attack Type**: Browser Crypto Mining
- **Target**: Users installing shady extensions
- **Vulnerability**: WASM miner in background script
- **MITRE**: T1496
- **Impact**: High CPU use, hidden mining
- **Tools**: Chrome Extension, Task Manager
- **Scenario**: Extension pretends to be productivity tool but runs WASM miner silently
- **Attack Steps**: 1. The attacker creates a Chrome extension branded as a PDF viewer or VPN tool. 2. Inside the extension’s background script, they load a .wasm file compiled from a crypto miner. 3. The WASM module runs continuously even if the browser is minimized, consuming CPU. 4. The miner activates once per session or based on idle events to avoid immediate detection. 5. No permissions are requested beyond background and tabs, making the extension appear safe. 6. Chrome users see high CPU usage but may not associate it with the extension. 7. Thousands of installations mean the attacker profits significantly. 8. Google only removes the extension after user reports or review.
- **Detection**: Review Chrome extension CPU usage
- **Solution**: Block unverified Chrome extensions
- **Tags**: #extensionmining #wasmchrome #cryptojack

## WASM Executable Loaded via Content Delivery API

- **Attack Type**: Obfuscation of Payloads
- **Target**: CDN-hosted APIs or 3rd-party plugins
- **Vulnerability**: WASM file fetched as fake content
- **MITRE**: T1105
- **Impact**: Remote code via dynamic WASM loading
- **Tools**: REST API, JS Fetch, WASM
- **Scenario**: Payload is dynamically fetched via REST API disguised as content
- **Attack Steps**: 1. A WASM binary is hosted on an API endpoint that mimics a content or translation API. 2. The page fetches it via fetch("api.translator.com/phrase?id=xyz"). 3. The response, though labeled JSON or text, actually contains raw WASM bytes. 4. JS code uses .arrayBuffer() to parse it, then instantiates it using WebAssembly.instantiate(). 5. The payload executes silently once loaded. 6. Since the file is fetched from an “API,” firewalls and proxies often let it through. 7. The loader is part of a widget embedded across multiple sites. 8. The attacker receives global reach using a single C2 disguised as a service.
- **Detection**: Monitor MIME types of loaded data
- **Solution**: Block unknown WASM origins
- **Tags**: #cdnpayload #dynamicwasm #wasmapi

## WASM Payload Delivery via WebSocket Tunnel

- **Attack Type**: Obfuscation of Payloads
- **Target**: Browsers supporting WebSockets
- **Vulnerability**: Dynamic WASM delivery without file
- **MITRE**: T1105
- **Impact**: Covert payload injection
- **Tools**: Browser WebSocket Tool, Dev Console
- **Scenario**: WASM module streamed live through WebSocket instead of direct file
- **Attack Steps**: 1. The attacker establishes a persistent WebSocket connection between client and server. 2. Instead of serving a full .wasm file, they break it into small chunks and stream it over the socket. 3. The client reassembles the binary in memory and uses WebAssembly.instantiate() to execute it. 4. Since it bypasses HTTP and file URLs, it's harder to trace in network logs. 5. The script never writes the payload to disk or triggers standard download warnings. 6. The WebSocket server may change its IP or domain frequently to avoid detection. 7. The attacker gains in-memory execution, stealth, and flexibility with this technique. 8. It’s an advanced method of using WASM for live attack delivery.
- **Detection**: Inspect WebSocket content types
- **Solution**: Filter binary data on WebSocket traffic
- **Tags**: #wasmsocket #inmemoryloader #websocketabuse

## Heap Corruption via Overlapping WASM Arrays

- **Attack Type**: WASM Heap Spraying
- **Target**: WASM-enabled JS engines
- **Vulnerability**: Weak memory view isolation
- **MITRE**: T1203
- **Impact**: Potential memory hijack or crash
- **Tools**: Heap Exploit Fuzzer, WASM Tools
- **Scenario**: Use multiple array views on shared memory to trigger corruption
- **Attack Steps**: 1. The attacker creates a shared linear memory buffer in WASM (e.g., 64MB). 2. They use JavaScript to create multiple typed array views over the same buffer. 3. These views are misused to write out-of-bounds values into adjacent memory. 4. The overlapping writes can lead to object corruption or browser instability. 5. A vulnerable browser JIT may incorrectly optimize this behavior, opening a window for exploitation. 6. The attacker may gain arbitrary read/write primitives. 7. This technique is experimental but has shown promise in bypassing sandbox restrictions. 8. It requires deep knowledge of engine internals but can lead to serious exploits.
- **Detection**: Monitor unusual memory view activity
- **Solution**: Patch array boundary logic
- **Tags**: #heapcorrupt #wasmarrays #jsengineflaw

## Browser Lock-Up via WASM Mining Bomb

- **Attack Type**: Browser Crypto Mining
- **Target**: General user browsers
- **Vulnerability**: Unrestricted loop execution in WASM
- **MITRE**: T1499
- **Impact**: Browser freeze or crash
- **Tools**: WASM Profiler, Chrome Task Manager
- **Scenario**: Malicious site runs high-loop WASM miner locking up the UI
- **Attack Steps**: 1. The attacker creates a WASM miner using nested hash computation loops. 2. They embed it into a webpage without any throttling or sleep intervals. 3. When the user loads the page, the miner instantly begins heavy CPU usage. 4. The browser UI becomes unresponsive due to 100% core usage. 5. The page includes no visible elements, tricking users into staying while CPU cycles are burned. 6. Users may be forced to close the entire browser or reboot. 7. This denial-of-service variant is useful in targeted disruption campaigns. 8. It exploits the raw performance advantages of WASM.
- **Detection**: Monitor CPU behavior on new sites
- **Solution**: Limit WASM performance on unknown tabs
- **Tags**: #wasmdos #browserfreeze #miningbomb

## WASM File Packed Inside Data URI to Evade Scanning

- **Attack Type**: Obfuscation of Payloads
- **Target**: Web apps using loose CSP
- **Vulnerability**: Embedded WASM in base64 URI
- **MITRE**: T1027
- **Impact**: Undetected in-file payload
- **Tools**: Base64 Tool, Dev Console
- **Scenario**: Base64-encoded WASM file embedded in page using data URI
- **Attack Steps**: 1. The attacker encodes a .wasm binary into a long base64 string. 2. They embed this string directly in the webpage using a data: URI. 3. JavaScript fetches and decodes the string into a binary array. 4. The WASM module is instantiated and executed in memory. 5. There is no external file to download, making it invisible to firewalls or scanners watching for .wasm extensions. 6. Many CSP rules don’t block data URIs, allowing the attack to succeed even on hardened pages. 7. This technique hides malicious modules in plain sight. 8. It is effective against weak CSP and simple scanning tools.
- **Detection**: Enforce CSP to block data URIs
- **Solution**: Disallow inline WASM instantiation
- **Tags**: #datauri #base64wasm #hiddenscript

## WASM Module with Encrypted Payload Triggered via Event

- **Attack Type**: Obfuscation of Payloads
- **Target**: Interactive web apps
- **Vulnerability**: Event-based hidden WASM logic
- **MITRE**: T1204.002
- **Impact**: Conditional in-memory attack
- **Tools**: AES Module, JS-WASM Bridge
- **Scenario**: WASM is decrypted and executed only after user clicks a button
- **Attack Steps**: 1. The .wasm payload is stored in the site as an encrypted blob using AES. 2. A JS decryption routine waits until the user clicks a specific element (e.g., “Start Quiz”). 3. Upon event trigger, the payload is decrypted in memory and instantiated as a WebAssembly module. 4. No .wasm file is fetched — all logic is handled in obfuscated JS. 5. The module may perform tracking, exfiltration, or hidden beaconing. 6. Because the payload only appears after user interaction, scanners miss it. 7. The attacker uses this to bypass behavioral analysis. 8. It’s an advanced example of conditional WASM payload execution.
- **Detection**: Analyze JS event handlers in pages
- **Solution**: Block inline WASM with CSP + sandboxing
- **Tags**: #conditionalwasm #eventtriggered #aeswasm

## WASM Malware Loader Triggered by Geolocation

- **Attack Type**: Obfuscation of Payloads
- **Target**: Regional users
- **Vulnerability**: Geolocation-based conditional WASM
- **MITRE**: T1036.004
- **Impact**: Evasion from sandbox environments
- **Tools**: JS Geolocation API, WASM Viewer
- **Scenario**: WASM executes only for visitors from specific regions
- **Attack Steps**: 1. The attacker writes a malicious payload in C/C++ and compiles it into WASM. 2. They host it on a fake website posing as a free tool. 3. A JavaScript snippet uses the Intl API and time zone heuristics to determine the user’s location. 4. Only if the user appears to be from a specific country (e.g., U.S. or Europe), the site loads and executes the .wasm file. 5. This prevents sandboxes and honeypots (usually from other regions) from detecting the payload. 6. The WASM module performs in-memory tasks such as beaconing, fingerprinting, or running shellcode. 7. Since the check is done client-side and no network requests reveal intent unless triggered, it's hard to catch. 8. This selective execution tactic enhances evasion and targeting.
- **Detection**: Monitor conditional logic in JS
- **Solution**: Enforce region-agnostic security policies
- **Tags**: #wasmloader #geotargeting #evasivetactics

## WebAssembly Cryptojacking via Online Code Editor

- **Attack Type**: Browser Crypto Mining
- **Target**: Developer-focused web apps
- **Vulnerability**: Trusted UI with hidden WASM miner
- **MITRE**: T1496
- **Impact**: Crypto theft using long session times
- **Tools**: Monaco Editor, WASM Compiler
- **Scenario**: Malicious miner hidden inside a browser-based coding tool
- **Attack Steps**: 1. The attacker builds a fake online coding environment that mimics popular IDEs. 2. A WASM miner is hidden inside the core editor initialization code. 3. Once the user starts editing code or loading templates, WebAssembly modules are fetched and executed. 4. The miner runs using a Web Worker that processes math-heavy mining operations in the background. 5. The editor interface looks authentic, so users stay on the page for long periods. 6. Meanwhile, their CPU is silently used to generate crypto profits for the attacker. 7. Since coding tools require high CPU, spikes aren’t seen as suspicious. 8. The attack demonstrates how WASM can hide in expected places to maximize dwell time.
- **Detection**: Profile CPU under expected workloads
- **Solution**: Vet 3rd-party tools before integration
- **Tags**: #wasmeditor #stealthcrypto #codingtrap

## WASM Heap Spray Using Dynamic Allocation in Loops

- **Attack Type**: WASM Heap Spraying
- **Target**: JS engines with WASM support
- **Vulnerability**: Incorrect memory growth handling
- **MITRE**: T1203
- **Impact**: Heap corruption, browser instability
- **Tools**: JS Heap Profiler, Custom Debugger
- **Scenario**: Use nested allocations to fill heap and trigger vulnerability
- **Attack Steps**: 1. The attacker creates a .wasm module that dynamically allocates memory in a loop using memory.grow(). 2. The WASM memory is filled with a crafted pattern designed to overwrite neighboring memory objects. 3. The module is executed inside a loop in JavaScript that gradually increases buffer size. 4. At some threshold, the JS engine miscalculates the available space, leading to a potential overflow. 5. This may result in object corruption or execution flow redirection. 6. The attack is timed so the memory grows slowly to avoid triggering alarms. 7. Debugging and fuzzing are used to fine-tune memory offset hits. 8. This is an experimental but realistic method of exploring memory abuse using WASM.
- **Detection**: Track repeated memory grow calls
- **Solution**: Limit dynamic WASM memory behavior
- **Tags**: #heapabuse #memoryoverflow #wasmloop

## WASM Trojan Delivered via QR Code Landing Page

- **Attack Type**: Obfuscation of Payloads
- **Target**: Smartphone and desktop browsers
- **Vulnerability**: WASM hidden behind QR delivery
- **MITRE**: T1204.001
- **Impact**: In-memory data exfiltration
- **Tools**: QR Generator, Browser DevTools
- **Scenario**: Victim scans QR and lands on WASM page acting as malware dropper
- **Attack Steps**: 1. The attacker generates a QR code that points to a phishing site hosted with HTTPS. 2. The site mimics a legitimate brand login page. 3. Hidden in the page is a .wasm file that executes upon page load using JavaScript’s fetch() API. 4. This WASM file contains logic to fingerprint the browser and silently load a second-stage payload. 5. The page shows a fake login form while WASM runs in the background. 6. Once the victim enters data, it is exfiltrated while the attacker gains info from the WASM probe. 7. QR-based delivery increases stealth, especially in phishing campaigns using print or physical media. 8. This blends traditional phishing with WASM-based execution.
- **Detection**: Block unknown WASM on first visit
- **Solution**: Educate users on QR phishing
- **Tags**: #qrwasm #trojandelivery #stealthphish

## WASM Miner in Browser Game UI Skins

- **Attack Type**: Browser Crypto Mining
- **Target**: Gamers using custom mods
- **Vulnerability**: WASM miner inside legitimate addon
- **MITRE**: T1496
- **Impact**: Mining disguised as cosmetic mod
- **Tools**: Game Framework + WebAssembly
- **Scenario**: Miner is disguised as a skin customization loader in game UIs
- **Attack Steps**: 1. The attacker releases a free UI skin library for a popular browser-based game. 2. The skin loader includes a .wasm file claimed to contain rendering logic. 3. In reality, the WASM module contains a crypto miner that begins execution during UI load. 4. Players assume lag or performance drops are due to skins being graphically intense. 5. The mining continues in the background as long as the player uses the skin. 6. Thousands of players can unknowingly contribute CPU cycles to mining. 7. This scenario abuses user trust in mods and UI enhancements. 8. WASM’s performance makes it ideal for long-running tasks like mining in game mods.
- **Detection**: Analyze WASM origin in browser games
- **Solution**: Block third-party WASM mods
- **Tags**: #wasmgaming #cryptominer #skinabuse

## WASM Shellcode Obfuscation via Control Flow Flattening

- **Attack Type**: Obfuscation of Payloads
- **Target**: Web apps loading WASM blobs
- **Vulnerability**: Control flow obfuscation in bytecode
- **MITRE**: T1027
- **Impact**: Obfuscation hides malicious logic
- **Tools**: Obfuscator-LLVM, WASM Binary Tools
- **Scenario**: Attacker flattens control logic to confuse static tools
- **Attack Steps**: 1. The attacker writes a malicious function in C containing shellcode logic. 2. They compile it to WASM using LLVM with control flow flattening (CFF) enabled. 3. This transforms the function into a state machine with many branches and opaque switch statements. 4. Static tools cannot easily trace logic paths due to removed structure. 5. The flattened .wasm is loaded using a small JS wrapper, which calls obfuscated entry points. 6. The real payload is triggered only when multiple conditions are met (e.g., time-based logic). 7. This confuses reverse engineers and bypasses simple sandbox automation. 8. The method is commonly used in malware hiding inside compiled executables, now applied in WASM.
- **Detection**: Use dynamic analysis of WASM modules
- **Solution**: Disallow unknown WASM execution
- **Tags**: #wasmobfuscation #CFF #staticbypass

## WASM Heap Spray Targeting Edge-Specific Bug

- **Attack Type**: WASM Heap Spraying
- **Target**: Edge browser (targeted version)
- **Vulnerability**: Memory zero-init flaw in WASM engine
- **MITRE**: T1203
- **Impact**: RCE in affected browser
- **Tools**: Edge DevTools, JS Fuzzer
- **Scenario**: Exploit chain targeting memory flaw in Microsoft Edge’s WASM engine
- **Attack Steps**: 1. An attacker identifies a version-specific memory flaw in Edge’s WASM engine related to how memory is zero-initialized. 2. They construct a .wasm module that abuses this flaw by rapidly allocating memory and filling it with crafted data. 3. JS code initializes multiple WASM instances that interact with vulnerable structures. 4. When the browser tries to optimize memory access, it miscalculates offset boundaries. 5. This causes memory corruption, which is used to leak pointers or trigger further exploit stages. 6. The chain is effective only in affected versions of Edge. 7. WASM heap spraying makes the exploit more reliable by shaping memory layout predictably. 8. Such targeted attacks are seen in nation-state and APT operations.
- **Detection**: Monitor WASM behavior in Edge
- **Solution**: Update Edge to latest version
- **Tags**: #edgeexploit #wasmheap #targetedattack

## WASM Loader Cloaked as JS Compression Library

- **Attack Type**: Obfuscation of Payloads
- **Target**: Site builders, CMS theme users
- **Vulnerability**: Fake utility library loads WASM
- **MITRE**: T1195.002
- **Impact**: Third-party WASM module exfiltration
- **Tools**: CompressionJS, WASM Tools
- **Scenario**: Attacker mimics a utility library to hide WASM module
- **Attack Steps**: 1. The attacker creates a library called fastCompress.js claimed to be a compression tool. 2. Instead of actual compression code, the library contains a WASM loader that fetches and executes a hidden .wasm file. 3. The .wasm file is described as a “core compression engine.” 4. The real purpose is fingerprinting and data exfiltration. 5. The library is published on open package repositories and used in multiple blogs or CMS themes. 6. Site admins unknowingly include it, thinking it’s for faster performance. 7. When the site loads, the WASM payload runs without suspicion. 8. This supply chain-style deception abuses trust in utility packages.
- **Detection**: Audit JS/WASM libraries for intent
- **Solution**: Validate dependencies from NPM/CDN
- **Tags**: #wasmloader #supplychain #fakeutils

## Multi-Stage Crypto Mining with Obfuscated WASM Chain

- **Attack Type**: Browser Crypto Mining
- **Target**: Browsers with idle user sessions
- **Vulnerability**: Conditional WASM chain execution
- **MITRE**: T1496
- **Impact**: Long-term crypto theft via layers
- **Tools**: JS Loader, XMRig-WASM Chain
- **Scenario**: Miner uses several layers of WASM modules, each loaded after validation
- **Attack Steps**: 1. The attacker creates a multi-stage miner split across several .wasm modules. 2. Initial loader verifies system resources using JavaScript (e.g., cores, battery). 3. If conditions match (e.g., high CPU, plugged-in), next WASM module is fetched and instantiated. 4. Each stage adds new capabilities like parallelism, throttling, or anti-debugging. 5. The modules use dynamic imports or decryption to prevent full payload analysis in one go. 6. All stages run in memory and clean up after execution. 7. This layered approach complicates reverse engineering. 8. It enables adaptive mining across systems with different specs.
- **Detection**: Analyze conditional imports of WASM
- **Solution**: Block sequential WASM loaders
- **Tags**: #multistage #cryptochain #wasmminer

## WASM Beacon Hidden in Web Chat Widget

- **Attack Type**: Obfuscation of Payloads
- **Target**: Websites using 3rd-party widgets
- **Vulnerability**: WASM beacon disguised in widget
- **MITRE**: T1071.001
- **Impact**: Stealth data exfiltration
- **Tools**: LiveChat API, WASM Module
- **Scenario**: Malicious chat widget loads WASM beacon for tracking users
- **Attack Steps**: 1. A free chat widget script is distributed via GitHub or self-hosted page. 2. The widget injects a hidden iframe with an embedded .wasm file. 3. This WASM file periodically beacons out to a C2 server with device info (screen size, user agent, battery). 4. The beacon is encrypted and appears as a simple POST request. 5. Users see no UI changes, assuming the chat widget is idle. 6. Many websites using the widget unknowingly leak user info. 7. Since the WASM is part of the widget, most site owners don’t inspect it. 8. The attack is a passive exfiltration using a trusted-looking asset.
- **Detection**: Monitor outbound POSTs from widgets
- **Solution**: Inspect and validate chat widgets
- **Tags**: #wasmtracking #widgetabuse #c2beacon

## WASM Obfuscation via Indirect Call Tables

- **Attack Type**: Obfuscation of Payloads
- **Target**: Any browser that supports WASM
- **Vulnerability**: Indirect call table abuse
- **MITRE**: T1027
- **Impact**: Malware hidden in complex control flow
- **Tools**: Binaryen, WebAssembly Studio
- **Scenario**: WASM uses complex indirect calls to hide real execution path
- **Attack Steps**: 1. The attacker writes a malicious C program and compiles it into WebAssembly. 2. During compilation, they introduce multiple function pointers and use indirect function calls via tables. 3. This structure obscures the control flow and hides which function is actually executed at runtime. 4. The attacker ensures that the actual malicious logic is split across multiple small functions. 5. These are randomly called via a large table that appears like legitimate dispatch logic. 6. The JS glue code simply calls a single “main” function without revealing complexity. 7. Static analysis tools struggle to trace the call path through the table. 8. This technique is widely used to hide payloads from automated scanners or analysts.
- **Detection**: Analyze dynamic behavior with call traces
- **Solution**: Block WASM with opaque table logic
- **Tags**: #indirectcalls #wasmobfuscation

## Multi-Tab Crypto Mining via SharedWorker and WASM

- **Attack Type**: Browser Crypto Mining
- **Target**: Browsers supporting SharedWorker
- **Vulnerability**: Persistent miner across tabs
- **MITRE**: T1496
- **Impact**: Extended CPU theft with minimal signs
- **Tools**: SharedWorker, WASM Miner
- **Scenario**: WASM miner runs once and controls all tabs using SharedWorker
- **Attack Steps**: 1. The attacker creates a site that includes a SharedWorker script running a WASM-based miner. 2. When a user opens the site in multiple tabs, the SharedWorker ensures the miner runs only once. 3. Each tab connects to the same mining session, reducing suspicion and avoiding performance spikes. 4. The miner continues running even if individual tabs are closed, until all are terminated. 5. This creates persistent background mining that adapts to tab behavior. 6. The miner throttles itself based on CPU usage to remain under detection thresholds. 7. The user is unaware as they continue browsing with multiple tabs open. 8. This technique maximizes efficiency of WASM miners across browsing sessions.
- **Detection**: Monitor SharedWorker scripts and CPU usage
- **Solution**: Block mining behavior in worker threads
- **Tags**: #wasmminer #sharedworker #cryptojacking

## WebAssembly Heap Spray via Oversized Image Decoding

- **Attack Type**: WASM Heap Spraying
- **Target**: Browsers using Canvas + WASM
- **Vulnerability**: Memory exhaustion via legit APIs
- **MITRE**: T1203
- **Impact**: Heap state manipulation, potential RCE
- **Tools**: Canvas API, WASM Module
- **Scenario**: Attack chains WASM with large image decoding logic
- **Attack Steps**: 1. The attacker creates a large PNG/JPEG image that, when decoded using Canvas, allocates massive memory. 2. In parallel, a WASM module begins filling memory buffers with predictable patterns. 3. The image and WASM allocations together exhaust the browser’s memory pool. 4. If the JS engine has faulty bounds-checking logic, this can lead to overflows. 5. The crafted WASM module tries to spray heap segments with specific markers. 6. Once the heap is in a predictable state, follow-up JavaScript attempts to exploit corrupted objects. 7. This combo of WASM + Canvas is difficult to detect, as both appear legitimate. 8. Successful exploitation could lead to memory disclosure or browser crashes.
- **Detection**: Track memory usage during media parsing
- **Solution**: Throttle large WASM memory + image loads
- **Tags**: #heapattack #canvaswasm #overflowcombo

## Encrypted WASM Loader Using XOR Obfuscation

- **Attack Type**: Obfuscation of Payloads
- **Target**: Browser with JS + WASM enabled
- **Vulnerability**: XOR + JS decryption trick
- **MITRE**: T1140
- **Impact**: In-memory malware loading
- **Tools**: XOR Script, JS Decoder, WASM
- **Scenario**: Attacker encrypts .wasm file with XOR and decrypts in browser
- **Attack Steps**: 1. A .wasm binary is XOR-encrypted and stored as a text blob in a JS file. 2. When the web page loads, the JavaScript uses a predefined key to decrypt the blob. 3. The decrypted result is converted to binary and passed to WebAssembly.instantiate(). 4. There is no file fetch or external network request — all data is local. 5. This bypasses static scanners looking for .wasm or .wasm.gz signatures. 6. The decryption function is lightly obfuscated using variable renaming and dummy code. 7. This allows the attacker to hide payload logic inside the page with minimal suspicion. 8. The resulting WebAssembly code can perform tracking, data theft, or even prepare for further code execution.
- **Detection**: Monitor JS blob usage and instantiate calls
- **Solution**: Disallow suspicious WASM inside inline JS
- **Tags**: #xorloader #wasmdecrypt #payloadhiding

## WASM Miner Triggered After User Form Submit

- **Attack Type**: Browser Crypto Mining
- **Target**: Browsers submitting user data
- **Vulnerability**: Delayed miner based on user interaction
- **MITRE**: T1204.002
- **Impact**: Prolonged crypto theft with consent illusion
- **Tools**: JS Event Listener, WASM Module
- **Scenario**: Miner runs only after user completes a form to avoid suspicion
- **Attack Steps**: 1. The attacker creates a webpage with a survey or registration form. 2. A WASM module containing a miner is embedded, but doesn’t activate on load. 3. JavaScript listens for the submit event from the form. 4. Once the user submits their information, the miner starts silently in the background. 5. Since the user willingly performed an action, CPU usage post-submission is less suspicious. 6. The miner is throttled to use only 30-40% of CPU, avoiding performance spikes. 7. Users often leave the confirmation page open, extending mining time. 8. This technique uses user trust and natural interactions to hide mining activity.
- **Detection**: Monitor post-submit CPU spikes
- **Solution**: Limit resource use on confirmation pages
- **Tags**: #formtrigger #cryptominer #wasmlurk

## WASM Execution Hidden in External Markdown Renderer

- **Attack Type**: Obfuscation of Payloads
- **Target**: Developers and doc sites
- **Vulnerability**: WASM beacon in dev pipeline
- **MITRE**: T1195.002
- **Impact**: Profiling via passive execution
- **Tools**: MarkdownJS, Custom Renderer
- **Scenario**: Attacker modifies markdown parser to load WASM
- **Attack Steps**: 1. A malicious markdown parser is published that supports “advanced rendering.” 2. Internally, it loads a WASM file to render custom charts or diagrams. 3. This WASM module is never needed for most documents but runs regardless. 4. The WASM code performs system profiling and sends beacon data to an attacker. 5. The markdown tool is bundled in several documentation platforms. 6. Many users unknowingly execute WASM every time docs are rendered. 7. Because markdown rendering is trusted, admins often skip inspection. 8. This is a classic supply-chain misuse of benign dev tools.
- **Detection**: Audit render plugins in markdown chains
- **Solution**: Ban unverified rendering tools
- **Tags**: #markdownattack #wasmbeacon #supplychainabuse

## Multi-Site WASM Loader via CDN Abuses

- **Attack Type**: Obfuscation of Payloads
- **Target**: Global blog readers
- **Vulnerability**: CDN-trusted WASM hosting
- **MITRE**: T1102.002
- **Impact**: Global delivery of malicious modules
- **Tools**: Free CDN, WASM Loader, JS
- **Scenario**: Attacker abuses CDN caching to deploy WASM globally
- **Attack Steps**: 1. The attacker hosts a WASM module disguised as a utils.min.js on a free CDN. 2. They inject references to this file across multiple small blog sites or ad networks. 3. When users visit any of these sites, the loader fetches and executes the WASM payload. 4. CDN cache ensures fast and global delivery, bypassing many domain-based filters. 5. The JS loader is often only a few lines and doesn’t reveal malicious logic. 6. WASM modules may perform fingerprinting, beaconing, or load stage-2 shellcode. 7. The attacker avoids detection by rotating CDN URLs or updating payloads dynamically. 8. This method takes advantage of the trust in major CDNs and low inspection of static assets.
- **Detection**: Inspect WASM loaded via trusted CDNs
- **Solution**: Restrict access to unverified static assets
- **Tags**: #cdnabuse #wasmcdn #globalloader

## WASM Heap Spray via Memory Grow Race Condition

- **Attack Type**: WASM Heap Spraying
- **Target**: Multi-threaded browser environments
- **Vulnerability**: Race condition in memory growth
- **MITRE**: T1203
- **Impact**: Memory corruption with heap control
- **Tools**: JS Race Tester, WASM Engine
- **Scenario**: Exploits async timing in memory.grow for spraying
- **Attack Steps**: 1. The attacker writes a WASM module that rapidly calls memory.grow() while simultaneously accessing unaligned memory. 2. JS code races the execution between different threads (using Web Workers) to create desynchronized memory states. 3. This leads to use-after-grow conditions where a memory segment is assumed valid but has been altered. 4. The corrupted memory state allows heap spraying patterns to take effect in unpredictable ways. 5. Exploit developers use this for experimental fuzzing and sandbox escape attempts. 6. The race condition depends on browser architecture and CPU thread handling. 7. Advanced attackers test this in isolated VMs to tune exploit conditions. 8. It represents a modern adaptation of memory corruption in WebAssembly.
- **Detection**: Detect fast memory.grow() calls in workers
- **Solution**: Throttle high-rate WASM memory changes
- **Tags**: #racewasm #heapgrow #timingflaw

## WASM Miner Running via ServiceWorker on Offline Mode

- **Attack Type**: Browser Crypto Mining
- **Target**: PWAs, offline-ready apps
- **Vulnerability**: Miner hidden in background cache
- **MITRE**: T1496
- **Impact**: CPU theft even without internet
- **Tools**: WASM Miner, Chrome Dev Console
- **Scenario**: Crypto miner runs even offline using ServiceWorker
- **Attack Steps**: 1. The attacker creates a PWA or site with offline support using a ServiceWorker. 2. A .wasm miner is cached during initial visit. 3. When the user revisits or remains offline, the ServiceWorker loads and executes the WASM miner. 4. Since it's offline, no network activity gives away the attack. 5. Users may browse cached content while unknowingly mining crypto. 6. The miner continues until the user closes the browser or clears cache. 7. This technique is highly persistent due to offline storage and background nature of ServiceWorkers. 8. Few users inspect background scripts during offline access.
- **Detection**: Inspect cached ServiceWorker assets
- **Solution**: Restrict WASM inside offline handlers
- **Tags**: #offlinecrypto #pwaexploit #serviceminers

## WASM Fingerprinting via Audio Worklet Analysis

- **Attack Type**: Obfuscation of Payloads
- **Target**: Audio-capable browsers
- **Vulnerability**: Device fingerprint via audio WASM
- **MITRE**: T1082
- **Impact**: Hardware-level user tracking
- **Tools**: Web Audio API, WASM Module
- **Scenario**: WASM module analyzes soundcard behavior to fingerprint user
- **Attack Steps**: 1. A WASM file is loaded as part of a streaming or audio utility site. 2. It connects to the AudioWorkletProcessor via JavaScript and processes silent audio. 3. The subtle timing differences and frequency responses from the user’s hardware are captured. 4. This unique signal is used to generate a device-specific fingerprint. 5. Unlike normal fingerprinting, it doesn’t rely on canvas or fonts and is harder to block. 6. The WASM module processes raw audio samples for efficiency and accuracy. 7. The fingerprint is sent back to the attacker’s server via AJAX or beacon API. 8. This is a stealthy and advanced tracking mechanism used in targeted profiling.
- **Detection**: Monitor AudioWorklet API usage
- **Solution**: Restrict WASM in audio contexts
- **Tags**: #wasmfingerprint #audioattack #browsertracking

## WASM Obfuscation via Custom Binary Encoding

- **Attack Type**: Obfuscation of Payloads
- **Target**: WASM-enabled browsers
- **Vulnerability**: Malformed binary layout
- **MITRE**: T1027
- **Impact**: Static analysis evasion
- **Tools**: WASM-Decoder, Hex Editor
- **Scenario**: Attacker modifies WASM binary header for evasion
- **Attack Steps**: 1. The attacker takes a compiled .wasm file and manually edits the binary header and section names using a hex editor. 2. Instead of typical section tags (like “code” or “data”), custom non-standard markers are inserted. 3. The payload is still valid and executable by modern browsers but becomes unreadable to common scanners and static analysis tools. 4. Obfuscated WASM code is then hosted on a web page and loaded with a minimal JS stub. 5. When the user visits the page, the WASM executes malicious logic (e.g., tracking, beaconing). 6. Because section names are modified, automated detection tools fail to parse and analyze the binary. 7. This technique enhances stealth in long-running campaigns. 8. It’s effective in environments where WASM analysis relies on known binary layouts.
- **Detection**: Use behavioral detection instead of signature-based
- **Solution**: Validate binary structure before WASM execution
- **Tags**: #binaryobfuscation #wasmheader #staticbypass

## Browser Game Injects WASM Miner via Ad Engine

- **Attack Type**: Browser Crypto Mining
- **Target**: Gamers on ad-based platforms
- **Vulnerability**: WASM miner via ad iframe
- **MITRE**: T1195.002
- **Impact**: Long-duration cryptojacking
- **Tools**: AdScript Injector, WASM Miner
- **Scenario**: Malicious ads trigger WebAssembly miner in gaming platform
- **Attack Steps**: 1. A browser game integrates a third-party ad network that unknowingly serves a malicious ad. 2. The ad includes a hidden iframe with a loader script. 3. This script fetches a .wasm miner and runs it in the background while the user plays the game. 4. Since gamers often stay on the site for long sessions, mining is profitable. 5. The miner uses Web Workers to avoid blocking the main UI thread. 6. CPU usage is capped to avoid user suspicion or device fan noise. 7. The attacker updates ads regularly to avoid signature-based detection. 8. This scenario highlights how ad supply chains can inject WASM without developer awareness.
- **Detection**: Analyze Web Workers in ad containers
- **Solution**: Vet ad networks and WASM usage
- **Tags**: #admining #cryptojack #wasmgames

## WASM Heap Spray in Image Gallery Plugin

- **Attack Type**: WASM Heap Spraying
- **Target**: Photo gallery websites
- **Vulnerability**: WASM heap spray inside visual tool
- **MITRE**: T1203
- **Impact**: Precursor to browser memory attacks
- **Tools**: JS Gallery Lib, WASM Engine
- **Scenario**: Memory abuse hidden inside photo gallery transitions
- **Attack Steps**: 1. The attacker modifies a popular image gallery plugin to include a .wasm module. 2. This WASM code is called during fancy slide transitions or when rendering large image grids. 3. The WASM memory buffer grows during each image load and release cycle. 4. Hidden inside is logic to allocate memory with crafted patterns (heap spray). 5. Over time, the heap becomes shaped for potential memory corruption attacks. 6. The plugin works flawlessly, keeping the user unaware. 7. This turns a UI enhancement into a potential memory exploit vehicle. 8. It showcases how visual plugins can be weaponized silently.
- **Detection**: Monitor large WASM memory calls during render
- **Solution**: Only use verified plugins
- **Tags**: #heapgallery #visualexploit #wasmplugin

## WASM-Based Keystroke Capture via Canvas Overlay

- **Attack Type**: Obfuscation of Payloads
- **Target**: Login or feedback forms
- **Vulnerability**: WASM-based keylogging via canvas
- **MITRE**: T1056.001
- **Impact**: Credential theft
- **Tools**: WASM Keylogger, Canvas API
- **Scenario**: Captures typed input via invisible canvas trick
- **Attack Steps**: 1. The attacker creates a fake form with a canvas overlay that appears transparent. 2. A WASM module is loaded that binds to the keyboard input listener. 3. Instead of using normal JavaScript keyloggers, input is parsed via compiled logic in WASM. 4. This allows the attacker to avoid standard browser protections or script auditing tools. 5. Captured input is rendered into the canvas in a hidden layer, then extracted via toDataURL() API. 6. The base64-encoded data is periodically sent to a remote server. 7. The attack is difficult to detect as it doesn’t use classic JS-based logging. 8. WASM makes the keylogger nearly invisible to static inspection.
- **Detection**: Detect abnormal canvas + WASM use
- **Solution**: Disable untrusted WASM forms
- **Tags**: #wasmlogger #canvasattack #keycapture

## Obfuscated Crypto Mining Using Compressed WASM Blobs

- **Attack Type**: Browser Crypto Mining
- **Target**: Any WASM-capable browser
- **Vulnerability**: In-memory decompression of WASM
- **MITRE**: T1140
- **Impact**: Diskless cryptojacking
- **Tools**: Gzip Loader, WASM Binary
- **Scenario**: WASM miner packed as compressed blob in JS
- **Attack Steps**: 1. The attacker stores a .wasm miner as a base64 GZIP-encoded blob in a JavaScript variable. 2. On page load, the script decompresses it using a client-side decompression library. 3. The decompressed WASM is passed directly into the WebAssembly.instantiate() API. 4. This allows malware to run entirely in memory, without ever touching disk or triggering network fetches. 5. Compression reduces file size and also prevents signature scanning. 6. CPU usage is throttled to avoid drawing attention. 7. The miner auto-starts after a delay to bypass behavior analytics. 8. This is a stealthy form of in-memory crypto exploitation.
- **Detection**: Analyze WASM decoding behavior in memory
- **Solution**: Block large inlined WASM blobs
- **Tags**: #wasminmemory #gzipminer #payloadcompression

## WASM Obfuscation via Dead Code Injection

- **Attack Type**: Obfuscation of Payloads
- **Target**: Analysts inspecting WASM
- **Vulnerability**: Overload with meaningless routines
- **MITRE**: T1027
- **Impact**: Reverse engineering resistance
- **Tools**: Obfuscator Tool, WASM Studio
- **Scenario**: Useless WASM functions added to mislead analysts
- **Attack Steps**: 1. The attacker adds dozens of fake, non-functional routines into the .wasm file. 2. These “dead” functions appear legitimate but are never called. 3. Actual malicious logic is hidden deep among the noise. 4. Static analysis tools or analysts get overwhelmed by volume. 5. The JS wrapper executes only a small subset of the entire module. 6. The size of the WASM module and presence of API-like names distract investigators. 7. Obfuscation also includes renaming of functions to random strings. 8. This makes reverse-engineering difficult and resource-intensive.
- **Detection**: Focus on executed logic paths, not size
- **Solution**: Flag excessive unused WASM functions
- **Tags**: #wasmdeadcode #staticnoise #reversebypass

## Browser Extension Injects WASM from External C2

- **Attack Type**: Obfuscation of Payloads
- **Target**: Browser extension users
- **Vulnerability**: Dynamic WASM execution via extension
- **MITRE**: T1176
- **Impact**: Persistent surveillance tool
- **Tools**: Malicious Extension, Remote WASM
- **Scenario**: Malicious browser addon fetches WASM remotely
- **Attack Steps**: 1. A rogue browser extension is uploaded to an extension store disguised as a theme or shopping tool. 2. Once installed, the extension periodically contacts a remote C2 server. 3. When triggered, it fetches a .wasm file containing obfuscated logic. 4. This WASM may include spyware, fingerprinting tools, or loaders. 5. The extension executes the WASM using minimal JavaScript, hiding real behavior. 6. Since the payload is hosted externally, it can be updated without reinstalling the addon. 7. This technique blends persistent access with dynamic payloads. 8. Such extensions are often part of long-term surveillance or monetization campaigns.
- **Detection**: Monitor extension traffic to external C2s
- **Solution**: Restrict WASM usage in unverified addons
- **Tags**: #extensionabuse #wasmfetch #persistentaddon

## Social Engineering Page Uses WASM to Profile Devices

- **Attack Type**: Obfuscation of Payloads
- **Target**: End-users on fake sites
- **Vulnerability**: WASM-based profiling on click
- **MITRE**: T1082
- **Impact**: Enhanced phishing & targeting
- **Tools**: WASM Profiler, JS Device API
- **Scenario**: Site pretending to offer free downloads profiles user
- **Attack Steps**: 1. A phishing site claims to offer free wallpapers, eBooks, or premium content. 2. When the user clicks “download,” a WASM module is silently loaded. 3. The module reads entropy sources like CPU info, thread timing, memory access delays, etc. 4. This data is compiled into a unique device fingerprint. 5. WASM is used to bypass traditional JS-based detection tools. 6. Collected data is sent to the attacker’s backend, where it's indexed by user and location. 7. This allows attackers to personalize future phishing or bypass fingerprint-based defenses. 8. Users are unaware since no download actually occurs.
- **Detection**: Monitor timing APIs + WASM usage
- **Solution**: Flag deceptive download flows
- **Tags**: #phishprofiler #wasmdeviceid #socialbait

## WASM Shellcode Obfuscated with Memory Chunks

- **Attack Type**: Obfuscation of Payloads
- **Target**: Any runtime with WASM + JS
- **Vulnerability**: Obfuscated chunked shellcode
- **MITRE**: T1027
- **Impact**: AV evasion via memory trick
- **Tools**: Memory Segmenter, JS Assembler
- **Scenario**: Shellcode split into memory chunks for reassembly
- **Attack Steps**: 1. Instead of placing shellcode directly, the attacker splits it into chunks across memory segments. 2. WASM module contains code that reassembles the chunks into executable form at runtime. 3. This avoids detection by tools that search for known byte sequences. 4. JS passes each chunk using an encoded format and stores them in temporary buffers. 5. Once enough chunks are gathered, the WASM code executes them in a hidden loop. 6. This approach bypasses basic memory scanning, even at runtime. 7. Obfuscation is layered using randomized chunk order. 8. Effective for hiding known malware variants.
- **Detection**: Monitor memory access patterns in WASM
- **Solution**: Flag unusual memory reassembly logic
- **Tags**: #chunkobfuscation #shellcodewasm #runtimeevasion

## Heap Spraying via Video Player Buffer Abuse

- **Attack Type**: WASM Heap Spraying
- **Target**: Users watching embedded videos
- **Vulnerability**: Exploit hidden inside buffer logic
- **MITRE**: T1203
- **Impact**: Memory corruption, browser crash
- **Tools**: VideoJS, WASM Module
- **Scenario**: Exploit embedded in custom video player
- **Attack Steps**: 1. A video player plugin is created with support for high-res buffering. 2. The attacker modifies the buffer handling logic to load a .wasm module during playback. 3. The WASM code gradually grows memory by simulating buffering logic. 4. At peak memory usage, crafted spray patterns are inserted into memory. 5. The module includes routines to overwrite specific byte offsets. 6. This triggers subtle memory inconsistencies in the browser’s engine. 7. Over time, this can lead to use-after-free or race conditions. 8. The exploit chain is effective during long video sessions.
- **Detection**: Monitor memory spike during video playback
- **Solution**: Restrict WASM in custom players
- **Tags**: #heapexploit #wasmvideo #videohack

