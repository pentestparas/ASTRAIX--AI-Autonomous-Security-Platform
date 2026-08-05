# Browser Security → Browser Fingerprinting / Tracking Attacks

## Canvas-Based Fingerprinting via toDataURL

- **Attack Type**: Canvas Fingerprinting
- **Target**: Web browsers
- **Vulnerability**: Unrestricted canvas access
- **MITRE**: T1606
- **Impact**: Cross-site user tracking without consent
- **Tools**: JavaScript, HTML5 Canvas
- **Scenario**: Generates unique hash by rendering hidden canvas and reading pixel data
- **Attack Steps**: 1. An attacker-controlled website embeds a hidden <canvas> element and renders specific shapes, colors, and text using custom fonts and transformations. 2. The script calls toDataURL() or getImageData() to read raw pixel values from the canvas. 3. Because rendering differs slightly between OS, GPU, font libraries, and browser versions, the returned data forms a near-unique fingerprint. 4. This fingerprint is hashed (e.g., SHA-256) and stored in a tracking database. 5. Even without cookies or localStorage, the fingerprint can re-identify users on return visits. 6. The canvas is hidden with CSS to prevent user awareness. 7. Multiple renderings may be combined to increase uniqueness. 8. Most browsers do not block canvas access by default.
- **Detection**: Monitor toDataURL() and getImageData() usage
- **Solution**: Ask for user consent before canvas readout
- **Tags**: #canvas #fingerprinting #browsertracking

## AudioContext Fingerprinting

- **Attack Type**: AudioContext / WebGL Tracking
- **Target**: Any modern browser with Web Audio
- **Vulnerability**: Timing artifacts in audio graph
- **MITRE**: T1606
- **Impact**: Silent user tracking and profiling
- **Tools**: Web Audio API
- **Scenario**: Uses sound processing APIs to derive unique timing, oscillator, and system behavior
- **Attack Steps**: 1. The attacker’s webpage creates an AudioContext and a minimal audio graph using oscillators and gain nodes. 2. It triggers the audio graph to generate silent sounds and analyzes the waveform via AnalyserNode or ScriptProcessorNode. 3. Subtle timing differences, rounding errors, and frequency responses vary by device, OS, and browser. 4. These values are collected, normalized, and used to generate a fingerprint. 5. The user hears no sound, and the process is silent in background. 6. When combined with canvas or font data, fingerprint reliability increases. 7. No explicit permission is required to access AudioContext. 8. Difficult to block without degrading legitimate audio functionality.
- **Detection**: Audit use of AudioContext in scripts
- **Solution**: Add noise or delay to fingerprinting calls
- **Tags**: #audiocontext #acousticfingerprint #silenttracking

## WebGL Renderer Identification

- **Attack Type**: WebGL Hardware Detection
- **Target**: Systems with discrete GPU
- **Vulnerability**: Exposed GPU ID via WebGL
- **MITRE**: T1606
- **Impact**: Hardware-level fingerprinting
- **Tools**: WebGL, JavaScript
- **Scenario**: Uses getParameter() on WebGL context to detect GPU and drivers
- **Attack Steps**: 1. Attacker creates a WebGL rendering context in a hidden <canvas> element. 2. They call gl.getParameter() with UNMASKED_VENDOR_WEBGL and UNMASKED_RENDERER_WEBGL. 3. These return detailed GPU info, including vendor and graphics driver used. 4. The site combines this with screen resolution, timezone, and canvas fingerprint to form a high-entropy identifier. 5. The WebGL call is silent and invisible to the user. 6. Some users may reveal very specific GPU models or even driver versions. 7. The fingerprint remains valid across sessions unless hardware changes. 8. Sites log this to re-identify or correlate users.
- **Detection**: Log fingerprinting attempts to WebGL params
- **Solution**: Return generic vendor strings or use privacy sandboxing
- **Tags**: #webgl #hardwarefingerprint #gpuabuse

## Font Enumeration via Width Probing

- **Attack Type**: Font Metrics Fingerprinting
- **Target**: Browser with custom fonts installed
- **Vulnerability**: No sandboxing of font measurements
- **MITRE**: T1606
- **Impact**: Inferred OS, region, or user environment
- **Tools**: CSS, JS, HTML
- **Scenario**: Detect installed fonts by measuring rendered text dimensions
- **Attack Steps**: 1. The script creates hidden <span> elements with sample text and applies different font-family names. 2. It sets fallback fonts like monospace, serif, and sans-serif. 3. JavaScript measures each span’s rendered width and height using offsetWidth and offsetHeight. 4. If a font is installed, the rendered dimensions differ from the fallback. 5. A unique map of available fonts is built per system. 6. Combining font list with canvas and WebGL increases accuracy. 7. This technique works without needing to render visible UI. 8. Browser inconsistencies help amplify fingerprint uniqueness.
- **Detection**: Detect repeated DOM reads for size tests
- **Solution**: Standardize font rendering or isolate via containers
- **Tags**: #fontfingerprint #textwidthhack #privacybypass

## Evercookie via ETag Header

- **Attack Type**: Evercookie / Supercookie Attacks
- **Target**: Any browser with persistent cache
- **Vulnerability**: Tracking via HTTP headers
- **MITRE**: T1606
- **Impact**: Cross-session re-identification
- **Tools**: Server-side, ETag, JS
- **Scenario**: Stores user ID in HTTP ETag so it survives clearing cookies
- **Attack Steps**: 1. A malicious site serves a resource (e.g., image or JS) with an ETag header like ETag: "user123" in the response. 2. When the user revisits, the browser includes If-None-Match: "user123" in the request header. 3. The server reads the value and identifies the user. 4. Even if the user clears cookies and localStorage, ETag headers remain in the browser cache. 5. The attacker detects this by comparing conditional requests. 6. This technique bypasses traditional storage mechanisms. 7. Users have no indication that they are being persistently tracked. 8. Only full cache clearing can remove this identifier.
- **Detection**: Inspect and flag unusual ETag patterns
- **Solution**: Disable ETag or use randomized headers
- **Tags**: #etag #evercookie #stealthstorage

## Supercookie via Flash Local Shared Object

- **Attack Type**: Evercookie / Supercookie Attacks
- **Target**: Browsers with Flash plugin
- **Vulnerability**: Hidden cross-storage in Flash
- **MITRE**: T1606
- **Impact**: Persistent cross-browser user tracking
- **Tools**: Adobe Flash, JS Bridge
- **Scenario**: Flash stores data in .sol files that survive cookie clears
- **Attack Steps**: 1. A site embeds a Flash object (or SWF file) that writes user ID to a Local Shared Object (LSO) like /#app/settings.sol. 2. When user clears browser cookies, the LSO remains untouched. 3. On next visit, Flash reads the LSO and repopulates the cookie or localStorage via JS bridge. 4. Flash can store 100KB per domain by default, much larger than cookies. 5. Even using incognito mode won't prevent LSO persistence unless explicitly blocked. 6. This technique enables near-permanent tracking. 7. Flash LSOs can be cross-browser as long as Flash plugin is shared. 8. Disabling Flash blocks this, but legacy systems remain vulnerable.
- **Detection**: Scan for .sol objects or Flash content
- **Solution**: Disable Flash and audit plugin permissions
- **Tags**: #flashsupercookie #LSO #legacytracking

## IndexedDB-Based Persistent ID

- **Attack Type**: Evercookie / Supercookie Attacks
- **Target**: Browsers supporting HTML5 storage
- **Vulnerability**: Hidden long-term key-value storage
- **MITRE**: T1606
- **Impact**: Near-permanent fingerprint recovery
- **Tools**: IndexedDB API
- **Scenario**: Writes fingerprint data to IndexedDB for long-term storage
- **Attack Steps**: 1. An attacker-controlled page creates an IndexedDB store named "trackerDB". 2. On first visit, it stores a unique fingerprint or UUID into the database. 3. Even if the user clears cookies or cache, the IndexedDB entry survives. 4. On future visits, the site reads the stored value and re-identifies the user. 5. Modern browsers allow IndexedDB without permissions and with generous storage. 6. This is combined with other vectors like ETag to rebuild full user profile. 7. Fingerprint persistence can last for months unless specifically cleared. 8. Many users are unaware of IndexedDB and cannot easily view contents.
- **Detection**: Monitor IndexedDB reads and writes
- **Solution**: Periodically purge IndexedDB or sandbox access
- **Tags**: #indexeddb #evercookie #storageabuse

## Battery API Fingerprinting

- **Attack Type**: System Metrics Fingerprinting
- **Target**: Mobile and laptop devices
- **Vulnerability**: Access to device charge state
- **MITRE**: T1606
- **Impact**: User/session correlation without cookies
- **Tools**: Battery Status API
- **Scenario**: Reads device battery level and charging state for user profiling
- **Attack Steps**: 1. A malicious site queries navigator.getBattery() to retrieve battery percentage, charging time, and discharging time. 2. These values vary by device usage and hardware, providing a soft signal for tracking. 3. Combined with other APIs, this creates a unique session signature. 4. For example, a partially charged MacBook on battery vs. Windows on charger yield different profiles. 5. Sites use this to re-link sessions after cookie clears. 6. No permissions are required to access battery stats on some browsers. 7. Browser vendors have deprecated or restricted this API due to abuse. 8. Legacy versions may still expose battery info without controls.
- **Detection**: Block navigator.getBattery() via CSP
- **Solution**: Use browser that limits battery fingerprinting
- **Tags**: #batteryapi #systemmetrics #fingerprinting

## Screen Resolution & Timezone Fingerprint

- **Attack Type**: System Metrics Fingerprinting
- **Target**: Browsers without anti-fingerprinting
- **Vulnerability**: Revealed system characteristics
- **MITRE**: T1606
- **Impact**: Passive user identification
- **Tools**: JavaScript
- **Scenario**: Collects screen size, color depth, timezone offset for identification
- **Attack Steps**: 1. A script queries screen.width, screen.height, screen.colorDepth, and Intl.DateTimeFormat().resolvedOptions().timeZone. 2. These values may seem generic but their combination narrows the pool of possible users. 3. For example, "1920x1080, 32-bit, Asia/Kolkata" is common, but not universal. 4. Added with OS language and plugin info, it becomes quite specific. 5. The attacker generates a fingerprint hash of this combined data. 6. No user permission or interaction is needed. 7. This is often the first layer of passive fingerprinting. 8. It contributes to tracking even if other APIs are blocked.
- **Detection**: Normalize display resolution or timezones
- **Solution**: Enable anti-fingerprint features in browser
- **Tags**: #screenfp #timezoneabuse #localeleak

## Cookie Respawning via Cache & LocalStorage Sync

- **Attack Type**: Evercookie / Supercookie Attacks
- **Target**: Any JS-enabled browser
- **Vulnerability**: Split-state tracking logic
- **MITRE**: T1606
- **Impact**: Cookie resurrection after user clears
- **Tools**: JS, HTML5 Storage
- **Scenario**: Regenerates deleted cookies by syncing from localStorage
- **Attack Steps**: 1. On first visit, the attacker sets both a regular cookie and a localStorage key with the same value. 2. If the user deletes cookies, but not localStorage, the script detects the missing cookie. 3. It reads the localStorage copy and reassigns it to document.cookie. 4. This process can happen silently on page load. 5. The result is a “respawned” cookie, making deletion ineffective. 6. Variants include using sessionStorage, ETags, and IndexedDB to maintain backup. 7. This multi-channel strategy defeats common privacy tools. 8. Full browser data wipe is needed to stop this method.
- **Detection**: Watch for cookie-localStorage sync scripts
- **Solution**: Clear all storage types together or isolate state
- **Tags**: #evercookie #cookiezombie #respawntracking

## Browser UUID via Audio + Canvas Fusion

- **Attack Type**: Combined Fingerprinting
- **Target**: Browser with JS-enabled environment
- **Vulnerability**: Multi-vector fingerprinting without consent
- **MITRE**: T1606
- **Impact**: Cross-session persistent tracking
- **Tools**: JS, Canvas, AudioContext
- **Scenario**: Builds a high-entropy ID using both canvas and audio artifacts
- **Attack Steps**: 1. A malicious script renders a specific canvas with shaped text and geometric paths. 2. Simultaneously, it creates an AudioContext with known oscillators and renders silent audio output. 3. Both canvas pixel data and audio sample responses are read and hashed into a combined fingerprint. 4. This fused ID is far more unique than either signal alone. 5. It survives across private browsing sessions and does not require cookies. 6. The data is stored in memory, localStorage, or sent to a remote server for correlation. 7. Many users are unaware this activity occurred, as it's silent and runs instantly. 8. Even changing browsers often results in near-identical fusion fingerprints unless OS or hardware change.
- **Detection**: Monitor combined canvas/audio usage
- **Solution**: Randomize entropy sources or require user opt-in
- **Tags**: #canvas #audiomix #hybridfingerprint

## Passive OS Detection via Font Rendering Differences

- **Attack Type**: Font Metrics Fingerprinting
- **Target**: Browsers using native font rendering
- **Vulnerability**: Font smoothing and metrics exposure
- **MITRE**: T1606
- **Impact**: OS-level user tracking
- **Tools**: CSS, JS, Hidden Spans
- **Scenario**: Identifies OS based on how specific fonts are displayed
- **Attack Steps**: 1. An attacker injects several invisible <div>s styled with fonts common across different OSes, like 'Segoe UI', 'Lucida Grande', 'Ubuntu'. 2. It measures the rendered dimensions of text samples via offsetWidth and offsetHeight. 3. The rendering subtlely differs due to font smoothing, kerning, and hinting at OS-level. 4. These measurement patterns are mapped to specific operating systems. 5. Even in the same browser, the attacker can deduce whether user is on Windows, macOS, or Linux. 6. The data feeds into broader fingerprinting models to reduce anonymity sets. 7. This technique requires no user input and executes immediately on load. 8. Font rendering differences are nearly impossible to spoof accurately.
- **Detection**: Detect bulk font span insertions
- **Solution**: Limit font enumeration, normalize rendering
- **Tags**: #fontmetrics #osdetection #passivefp

## WebGL Shader Timing Side-Channel

- **Attack Type**: WebGL Fingerprinting
- **Target**: Browsers with WebGL support
- **Vulnerability**: GPU compile time as fingerprint
- **MITRE**: T1606
- **Impact**: Hardware detection bypassing user controls
- **Tools**: WebGL, JS
- **Scenario**: Exploits time taken to compile shaders as a fingerprinting signal
- **Attack Steps**: 1. Attacker compiles multiple complex WebGL shaders via gl.createShader and gl.compileShader. 2. They measure the compilation time using high-resolution timers like performance.now(). 3. The GPU model and driver affect the timing significantly. 4. The attacker logs this timing as a high-fidelity signal of hardware fingerprinting. 5. It is combined with renderer info and screen resolution for robust ID. 6. This technique does not rely on pixel output, just GPU behavior. 7. Difficult to detect in client-side logs, as no rendering occurs. 8. Can work in headless or sandboxed environments too.
- **Detection**: Profile timing anomalies on shader ops
- **Solution**: Add noise or delay to shader APIs
- **Tags**: #webgl #gpu #shadersidechannel

## Audio-Based Location Approximation

- **Attack Type**: AudioContext Fingerprinting
- **Target**: Browsers with system-level audio
- **Vulnerability**: Audio timing artifacts
- **MITRE**: T1606
- **Impact**: Location or device inference via sound
- **Tools**: JS, Audio API
- **Scenario**: Uses oscillator and output latency to infer region or system setup
- **Attack Steps**: 1. Site loads oscillator tones at precise frequencies (e.g., 440Hz, 1000Hz) using AudioContext. 2. Measures the phase delay, jitter, and playback latency of the tones. 3. These behaviors vary by device firmware, sound card, and driver optimizations. 4. The attacker correlates this with common location/device patterns from known samples. 5. Even without IP or GPS, attacker can narrow location or device type with 80–90% confidence. 6. This technique is silent and produces no audible output. 7. Fingerprints are combined with screen and canvas traits to enhance profiling. 8. Mitigations are complex due to native differences in system sound stack.
- **Detection**: Block precise frequency audio graphs
- **Solution**: Introduce jitter or quantize latency in browser
- **Tags**: #acousticfp #latencyfingerprint #covertgeo

## Evercookie via HTML5 SessionStorage

- **Attack Type**: Evercookie / Supercookie Attacks
- **Target**: HTML5-capable browsers
- **Vulnerability**: Session + local storage redundancy
- **MITRE**: T1606
- **Impact**: Inescapable identity regeneration
- **Tools**: JS, sessionStorage API
- **Scenario**: Uses sessionStorage as backup ID that repopulates localStorage
- **Attack Steps**: 1. On initial visit, the script sets both localStorage and sessionStorage with the same tracking ID. 2. On subsequent visits, if localStorage is missing but sessionStorage exists, the script copies the value back. 3. This process happens during page load, silently. 4. Combined with URL fragments or ETag, the attacker can rebuild the complete tracking state. 5. Because sessionStorage is scoped per-tab, it's harder to detect using standard privacy tools. 6. This redundancy ensures users can't easily reset their fingerprint without killing all browser states. 7. Cookies are merely the frontend — real tracking lives in sessionStorage. 8. Most users are unaware this behavior even exists.
- **Detection**: Monitor same-value use in both storages
- **Solution**: Clear both storage types and isolate sessions
- **Tags**: #evercookie #sessionStorage #storageabuse

## Flash LSOs Sync to HSTS Cache

- **Attack Type**: Evercookie / Supercookie Attacks
- **Target**: Legacy browsers with Flash
- **Vulnerability**: HSTS + LSO sync bypass
- **MITRE**: T1606
- **Impact**: Undeletable stateful identifier
- **Tools**: Flash + HTTPS, HSTS
- **Scenario**: Repopulates state via a forced HTTPS HSTS cache hit
- **Attack Steps**: 1. Attacker sets a value in Flash LSO (e.g., user ID 54321). 2. Later, they force the browser to load an HTTP URL like http://track.com/pixel, knowing HSTS will redirect to HTTPS. 3. Server reads the request and correlates with HTTPS-only HSTS policy to identify user. 4. This coupling of Flash LSO and HSTS cache becomes a covert storage mechanism. 5. Even when clearing cookies, users don’t clear HSTS entries. 6. The attacker uses this persistence vector for cross-session fingerprinting. 7. This is highly persistent unless the HSTS policy is wiped manually. 8. Few users know how to clear HSTS entries directly.
- **Detection**: Analyze forced HTTPS redirects post-LSO
- **Solution**: Disable Flash and auto-expiring HSTS
- **Tags**: #hstsabuse #flashtracking #supercookie

## Bluetooth Device UUID Fingerprinting

- **Attack Type**: Hardware Fingerprinting
- **Target**: Browsers with Bluetooth enabled
- **Vulnerability**: Exposure of unique hardware IDs
- **MITRE**: T1606
- **Impact**: Physical location tracking
- **Tools**: Web Bluetooth API
- **Scenario**: Uses navigator.bluetooth to probe nearby device UUIDs
- **Attack Steps**: 1. A malicious site calls navigator.bluetooth.requestDevice() with generic filters. 2. User is prompted to allow access, often without knowing the privacy implications. 3. Once granted, the page lists nearby Bluetooth device UUIDs, which are often globally unique. 4. Attacker stores this device info to fingerprint the user or location. 5. This data is nearly impossible to spoof and persists across visits. 6. If multiple users are fingerprinted near the same device, correlation becomes trivial. 7. A mix of device + fingerprint traits creates strong tracking map. 8. Repeating device signals = location-specific beacon.
- **Detection**: Restrict Web Bluetooth permissions
- **Solution**: Strip UUIDs or prompt contextual warnings
- **Tags**: #bluetoothfp #deviceid #locationleak

## Audio Buffer Hashing

- **Attack Type**: AudioContext Fingerprinting
- **Target**: All audio-enabled browsers
- **Vulnerability**: Audio processing micro-differences
- **MITRE**: T1606
- **Impact**: Unseen sound-based profiling
- **Tools**: Web Audio API, JS
- **Scenario**: Creates hash from sound buffer processing output
- **Attack Steps**: 1. The page builds an audio processing chain using createBuffer, analyserNode, and scriptProcessorNode. 2. It fills the buffer with pseudo-random waveform data and captures the output using JS. 3. The precise shape and values of output waveforms vary by browser, OS, and CPU architecture. 4. Hash of the output is used as a fingerprint. 5. Multiple rounds of this process are averaged to smooth noise. 6. Results are fed into tracking systems to re-identify repeat visitors. 7. This signal is difficult to detect since no sound is played. 8. Legitimate apps may use same APIs, making filtering hard.
- **Detection**: Watch for sound buffer reads in JS
- **Solution**: Introduce noise or randomization in waveform
- **Tags**: #audiobuffer #soundfp #coverttracking

## Device Memory + CPU Threads Entropy

- **Attack Type**: System Metrics Fingerprinting
- **Target**: Browsers with HW APIs enabled
- **Vulnerability**: Leaked hardware spec info
- **MITRE**: T1606
- **Impact**: Passive profiling and session relink
- **Tools**: JavaScript API
- **Scenario**: Combines navigator.hardwareConcurrency and deviceMemory to segment users
- **Attack Steps**: 1. The attacker script queries navigator.deviceMemory (e.g., 4GB) and navigator.hardwareConcurrency (e.g., 8 threads). 2. This data segments the user pool by hardware profile. 3. Combined with screen size, timezone, and language, it forms a highly unique tuple. 4. These values are gathered passively on load without consent. 5. This is especially useful for tracking across incognito sessions. 6. Even mobile vs desktop inference becomes trivial using this method. 7. Most browsers expose this data via JS with no user awareness. 8. It’s logged and stored for cross-visit matching.
- **Detection**: Block or spoof hardware API values
- **Solution**: Use privacy sandbox or strict anti-fp mode
- **Tags**: #hardwarefp #devicememory #cpuentropy

## CSS Media Query-Based Fingerprinting

- **Attack Type**: Layout/Style Fingerprinting
- **Target**: CSS-capable browsers
- **Vulnerability**: Exposed layout and preference traits
- **MITRE**: T1606
- **Impact**: Silent profiling via style prefs
- **Tools**: CSS, JS
- **Scenario**: Detects device traits using matchMedia() and media queries
- **Attack Steps**: 1. Attacker script uses window.matchMedia() to evaluate dozens of CSS media queries. 2. Queries include things like prefers-color-scheme, screen dimensions, and pointer precision. 3. Based on true/false answers, attacker builds a style profile of user’s device. 4. Some features — like reduced motion, dark mode, or hover capability — vary subtly across devices. 5. These are collected to refine the user’s unique fingerprint. 6. Does not rely on cookies or visual DOM, making it stealthy. 7. This form of fingerprinting is near-impossible to detect from the user’s side. 8. Results are stored and used for cross-site correlation.
- **Detection**: Monitor excessive media query usage
- **Solution**: Randomize or flatten layout signals
- **Tags**: #cssfp #mediatracking #stealthfp

## Canvas Noise Tolerance Analysis

- **Attack Type**: Canvas Fingerprinting
- **Target**: JS-enabled browsers
- **Vulnerability**: Pixel-level rendering leakage
- **MITRE**: T1606
- **Impact**: Highly persistent fingerprinting
- **Tools**: HTML5 Canvas, JS
- **Scenario**: Uses subtle rendering noise to differentiate hardware + OS
- **Attack Steps**: 1. Attacker site renders complex canvas drawings including gradients, text, curves, and anti-aliased lines using various fonts and color styles. 2. It then reads the raw pixel data using getImageData() and runs a noise profile analysis to measure small imperfections caused by sub-pixel rendering. 3. These variations in rendering — especially around edges or transparent overlays — vary significantly across GPUs, OS, and browser engines. 4. Attacker builds a rendering “noise profile” as part of a fingerprint hash. 5. When the same user returns on a different session or even in incognito mode, the attacker matches this noise signature. 6. No visible elements or user interaction is needed; rendering is hidden with CSS. 7. The approach is resilient to font blocking since it measures rendering patterns, not font names. 8. The fingerprint is stored locally or sent to a remote server for correlation.
- **Detection**: Monitor getImageData() usage and hidden canvas elements
- **Solution**: Randomize canvas rendering output or block access
- **Tags**: #canvas #rendernoise #pixelprofile

## DOM Object Enumeration via Script Order

- **Attack Type**: JS Object Fingerprinting
- **Target**: All browsers
- **Vulnerability**: Engine-level API exposure
- **MITRE**: T1606
- **Impact**: Stealth browser version detection
- **Tools**: JavaScript
- **Scenario**: Identifies browser version via DOM object order and availability
- **Attack Steps**: 1. An attacker script queries hundreds of DOM properties and objects in a fixed order (e.g., window, document, navigator, Intl, etc.). 2. It checks for presence, default values, or structure of each object and their sub-properties. 3. Different browser engines expose slightly different object trees and object order. 4. For example, Intl.DisplayNames might exist in Chromium but not in older Firefox. 5. The script builds a binary feature vector from available APIs and object types. 6. This vector is hashed and used as a unique browser version signature. 7. It’s especially effective for detecting headless browsers and automation tools. 8. This passive JS probing technique runs fast and invisibly.
- **Detection**: Analyze JS object enumeration rates
- **Solution**: Randomize feature exposure or limit probing
- **Tags**: #domfp #jsengine #stealthtracking

## WebGL Texture Rendering Variation

- **Attack Type**: WebGL Fingerprinting
- **Target**: Browsers with GPU/WebGL
- **Vulnerability**: Texture processing discrepancies
- **MITRE**: T1606
- **Impact**: GPU-specific fingerprinting
- **Tools**: WebGL, Shader Code
- **Scenario**: Fingerprints user via differences in GPU texture rendering
- **Attack Steps**: 1. Site creates a WebGL canvas and uploads custom textures and shaders using images with varying color gradients. 2. It reads rendered output via readPixels() and compares it to known reference hashes. 3. Subtle GPU behaviors — like floating-point rounding, dithering, and color-space conversion — cause minute differences. 4. These output differences form a reliable fingerprint when hashed. 5. Attacker stores this hash and combines it with canvas or screen metrics. 6. Variations are strong enough to distinguish between GPU models, even among same OS/browser. 7. This process occurs off-screen and without interaction. 8. Data is exfiltrated silently as telemetry to tracking server.
- **Detection**: Log usage of readPixels() in WebGL
- **Solution**: Add noise or degrade texture precision
- **Tags**: #webgltexture #gpuid #graphicsfp

## Plugin-Based Fingerprinting via Navigator.plugins

- **Attack Type**: JS Object Fingerprinting
- **Target**: Legacy/older browsers
- **Vulnerability**: Plugin enumeration without consent
- **MITRE**: T1606
- **Impact**: Persistent legacy tracking
- **Tools**: JS, DOM API
- **Scenario**: Uses navigator.plugins to identify installed browser plugins
- **Attack Steps**: 1. Malicious JS inspects navigator.plugins array which lists enabled browser plugins. 2. It iterates through each plugin and extracts name, description, and filename fields. 3. Legacy or rare plugins (e.g., Foxit Reader, Silverlight, Java) offer unique tracking signals. 4. Plugin order and presence are stable across visits, forming a consistent fingerprint. 5. This technique works even in incognito unless plugins are disabled. 6. The plugin list is logged and hashed into a browser identity string. 7. Combined with user-agent and screen size, uniqueness increases drastically. 8. Many privacy-focused browsers now mask or disable plugin enumeration to mitigate this.
- **Detection**: Monitor access to navigator.plugins
- **Solution**: Disable or fake plugin lists
- **Tags**: #pluginfp #legacytracking #navigatorabuse

## Fingerprinting via CPU Architecture Guessing

- **Attack Type**: System Metrics Fingerprinting
- **Target**: Browsers with JS timing APIs
- **Vulnerability**: Hardware leakage via math profiling
- **MITRE**: T1606
- **Impact**: Silent device class detection
- **Tools**: JS, Web Workers
- **Scenario**: Detects x86 vs ARM via math ops and timing
- **Attack Steps**: 1. Page runs complex math operations (FFT, matrix transforms) via JS and Web Workers. 2. Measures microsecond-level differences in completion time for integer vs floating-point ops. 3. Performance deltas between architectures (x86_64 vs ARM64) are measurable. 4. Based on timing profiles, attacker guesses CPU architecture, which narrows user pool. 5. Combining this with OS, resolution, and language creates near-unique profiles. 6. Results are stored as hashable features per session. 7. Can work across multiple browsers as timing remains hardware-linked. 8. Timing variations are silent and hard to spoof unless throttled.
- **Detection**: Delay or normalize JS timing resolution
- **Solution**: Restrict high-res timers like performance.now()
- **Tags**: #cpuarch #timingfp #fingerprint

## Canvas Font Smoothing Detection

- **Attack Type**: Canvas Fingerprinting
- **Target**: All modern browsers
- **Vulnerability**: Font rendering variance
- **MITRE**: T1606
- **Impact**: OS/display fingerprinting
- **Tools**: Canvas, CSS, JS
- **Scenario**: Detects OS or display type based on font antialiasing
- **Attack Steps**: 1. Attacker renders identical text on canvas with different font weights and styles (bold, italic, etc.). 2. Reads raw pixel data to evaluate how edges are smoothed (antialiased). 3. The degree and method of smoothing differs by OS (e.g., macOS vs Windows ClearType). 4. The results are stored as binary features and hashed for fingerprinting. 5. Even font smoothing modes (subpixel, grayscale, none) impact fingerprint uniqueness. 6. The test is done in hidden canvas layers invisible to the user. 7. Attacker does not need to identify font names—only rendering artifacts. 8. Combined with device pixel ratio, this creates resilient ID.
- **Detection**: Block canvas pixel access or fuzz rendering
- **Solution**: Force grayscale font rendering
- **Tags**: #fontsmoothing #canvasfp #osdisplay

## IndexedDB Quota Estimation

- **Attack Type**: Storage Fingerprinting
- **Target**: Browsers supporting IndexedDB
- **Vulnerability**: Storage quota differences
- **MITRE**: T1606
- **Impact**: Browser/env detection via limits
- **Tools**: IndexedDB API, JS
- **Scenario**: Probes IndexedDB storage limits to infer environment
- **Attack Steps**: 1. Script repeatedly writes blobs into IndexedDB store in increasing size chunks. 2. When quota is reached, an exception is thrown. 3. The maximum capacity allowed varies by device, browser, and incognito mode. 4. Attacker logs max quota and correlates it with known device profiles. 5. For example, Firefox allows 2GB, while Safari allows 50MB in private mode. 6. These differences are used as fingerprinting dimensions. 7. User may notice no slowdown as writes are done in memory. 8. Results help infer browser and privacy mode indirectly.
- **Detection**: Rate-limit DB writes or throw fake quota
- **Solution**: Standardize quotas across modes
- **Tags**: #indexeddbfp #storagequota #covertfp

## CSS-Based Scrollbar Width Fingerprinting

- **Attack Type**: UI Metrics Fingerprinting
- **Target**: JS-enabled browsers
- **Vulnerability**: Exposed layout differences
- **MITRE**: T1606
- **Impact**: System/UI fingerprinting
- **Tools**: CSS, JS
- **Scenario**: Measures default scrollbar width as system-specific trait
- **Attack Steps**: 1. Page creates a hidden div with overflow scroll enabled. 2. Measures difference between offsetWidth and clientWidth to detect scrollbar width. 3. This width varies across OS, browser engine, zoom level, and user settings. 4. The attacker records the width and combines it with other metrics. 5. For example, 15px vs 17px scrollbar gives hint about OS or theme. 6. This technique requires no permissions and runs silently. 7. Users cannot easily detect or spoof their scrollbar width. 8. It's often used in conjunction with font and screen metrics.
- **Detection**: Normalize scrollbar rendering via CSS
- **Solution**: Force overlay scrollbars where possible
- **Tags**: #scrollbarfp #cssmetrics #uifp

## LocalStorage Cross-Page Persistence Abuse

- **Attack Type**: Evercookie / Supercookie Attacks
- **Target**: Any JS-enabled browser
- **Vulnerability**: Unmonitored long-term storage
- **MITRE**: T1606
- **Impact**: Covert identity storage
- **Tools**: LocalStorage API, JS
- **Scenario**: Tracks users by persisting ID across unrelated paths or domains
- **Attack Steps**: 1. Malicious scripts inject identical localStorage.setItem("uid", "abc123") on multiple subdomains or paths. 2. Because localStorage is scoped per origin, attackers use wildcard subdomains or redirections to share ID. 3. On revisit, scripts on any page under the same origin retrieve the ID. 4. Users who clear cookies but not localStorage are reidentified. 5. Advanced variants involve iframe postMessage to copy ID across domains. 6. Persistent storage survives even browser restarts. 7. Users typically don’t inspect localStorage manually. 8. Combined with fingerprinting, this results in near-total reidentification.
- **Detection**: Auto-clear localStorage on session close
- **Solution**: Use browser containers or strict mode
- **Tags**: #localstorage #evercookie #tracking

## Device Pixel Ratio Enumeration

- **Attack Type**: System Metrics Fingerprinting
- **Target**: JS-capable browsers
- **Vulnerability**: Exposed DPI ratio
- **MITRE**: T1606
- **Impact**: Display-based profiling
- **Tools**: JavaScript
- **Scenario**: Measures screen DPI and zoom level via devicePixelRatio
- **Attack Steps**: 1. Page queries window.devicePixelRatio and stores the returned float (e.g., 1.25). 2. This value indicates zoom level and screen DPI scaling. 3. Combined with screen width and height, it forms a near-unique display fingerprint. 4. On retina or high-DPI screens, ratios like 2.0 or 1.5 are common. 5. The attacker uses this to distinguish between devices and even between display configurations on the same device. 6. Works silently and immediately upon page load. 7. When tracked over time, can detect hardware changes or OS upgrades. 8. It’s used in tandem with canvas and font metrics to refine uniqueness.
- **Detection**: Quantize or spoof pixel ratio value
- **Solution**: Enable privacy-respecting DPI reporting
- **Tags**: #devicepixelratio #dpi #displayfp

## AudioContext Buffer Timing Profiling

- **Attack Type**: AudioContext Fingerprinting
- **Target**: Audio-capable browsers
- **Vulnerability**: Timing side-channel on audio processing
- **MITRE**: T1606
- **Impact**: Hardware/browser fingerprinting
- **Tools**: Web Audio API
- **Scenario**: Detects timing discrepancies in audio buffer playback
- **Attack Steps**: 1. The attacker script creates a buffer with random audio samples and processes it through an OfflineAudioContext, which allows audio to be rendered without playback. 2. It then measures the time taken to process these samples using high-resolution timers like performance.now(). 3. Hardware, browser implementation, and OS audio stack introduce subtle but measurable delays. 4. These timing patterns are hashed into a unique profile. 5. Repeated tests show consistent timing signatures, even across sessions or tabs. 6. The results can be used to identify browser version, OS version, and even CPU/GPU model. 7. No audio is played, so the user remains unaware. 8. The fingerprint is silently exfiltrated to a backend server for tracking or correlation.
- **Detection**: Monitor access to OfflineAudioContext and frequent performance.now() calls
- **Solution**: Introduce timing jitter or noise
- **Tags**: #audiotiming #offlineaudio #covertfp

## Screen Orientation & Rotation API Abuse

- **Attack Type**: UI Metrics Fingerprinting
- **Target**: Mobile and hybrid devices
- **Vulnerability**: Rotation sensor behavior leakage
- **MITRE**: T1606
- **Impact**: Device class identification
- **Tools**: Screen.orientation, JS
- **Scenario**: Detects device class and environment via rotation behavior
- **Attack Steps**: 1. The script uses screen.orientation.angle and type to determine the device orientation (e.g., landscape-primary, portrait-secondary). 2. It listens for orientation changes using event listeners to detect hardware responsiveness. 3. These values can distinguish between mobile devices, tablets, desktops, and even smart TVs. 4. The presence and responsiveness of rotation events also hint at device sensor configuration. 5. Combined with resolution and touch support, a detailed fingerprint is built. 6. The behavior remains consistent across sessions and is invisible to users. 7. Device traits are logged and correlated with known device profiles. 8. The data helps identify user device category even without user-agent strings.
- **Detection**: Disable or spoof screen.orientation data
- **Solution**: Use browser profiles that limit sensor access
- **Tags**: #orientationfp #sensors #deviceid

## Battery Status API Fingerprinting

- **Attack Type**: JS API Fingerprinting
- **Target**: Browsers exposing battery API
- **Vulnerability**: Exposure of live power metrics
- **MITRE**: T1606
- **Impact**: Cross-tab and session correlation
- **Tools**: Battery Status API
- **Scenario**: Reads battery info to correlate session state
- **Attack Steps**: 1. Script accesses navigator.getBattery() to retrieve battery charge level, charging status, and estimated discharge/charge times. 2. These values fluctuate per device, but the charge percentage and time estimates are often highly stable for short windows. 3. The attacker logs this info to create a temporary fingerprint. 4. When users open the same site in another tab or incognito mode, matching battery stats can link sessions. 5. Especially effective for laptop users who remain on battery power over long periods. 6. The API data is gathered silently and does not alert the user. 7. Although not unique alone, when combined with resolution, canvas, or fonts, it boosts fingerprint accuracy. 8. Battery data has been deprecated in many browsers due to abuse, but some still support it.
- **Detection**: Disable navigator.getBattery() or return static values
- **Solution**: Block battery API in privacy mode
- **Tags**: #batteryfp #powerstatus #crosssession

## Audio Buffer Underrun Signature

- **Attack Type**: AudioContext Fingerprinting
- **Target**: Browsers supporting real-time audio
- **Vulnerability**: CPU latency exposed via audio underruns
- **MITRE**: T1606
- **Impact**: Detects multitasking & device quality
- **Tools**: Web Audio API
- **Scenario**: Detects CPU load and system latency via underrun
- **Attack Steps**: 1. Script creates a real-time audio buffer stream and processes continuous audio in small chunks using a ScriptProcessorNode. 2. It logs the number of underruns (missed frames) due to CPU latency or scheduling delay. 3. Underrun behavior is unique to device type, load, and OS. 4. It’s especially distinct in low-end hardware or background-tab environments. 5. The script hashes the underrun pattern and adds it to an existing fingerprint profile. 6. Can also reveal whether user is multitasking or has performance throttling enabled. 7. No sound is required for fingerprinting to work. 8. This method is resilient to incognito mode due to hardware consistency.
- **Detection**: Prevent JS from accessing real-time audio analysis
- **Solution**: Use AudioWorklet with throttled timing
- **Tags**: #underrunfp #cpuaudio #soundleak

## Evercookie via ETag + LocalStorage

- **Attack Type**: Evercookie / Supercookie
- **Target**: Browsers that allow ETag caching
- **Vulnerability**: Dual-channel ID persistence
- **MITRE**: T1606
- **Impact**: Resilient reidentification
- **Tools**: ETag headers, LocalStorage
- **Scenario**: Combines HTTP headers + JS storage to re-identify
- **Attack Steps**: 1. When a user visits the site, a unique identifier is sent in the HTTP response header using ETag. 2. Browser caches this identifier in its internal cache. 3. At the same time, JS writes the same ID to localStorage. 4. On future visits, the site compares the ETag and localStorage ID. If one is missing, it restores it from the other. 5. Even if users clear cookies, the ID persists unless cache and localStorage are both cleared. 6. This creates a self-healing tracking method. 7. Works across subdomains or iframes if not sandboxed. 8. Difficult for most users to detect or block effectively.
- **Detection**: Block ETag-based tracking and disable localStorage
- **Solution**: Use anti-evercookie browser plugins
- **Tags**: #etagfp #evercookie #resilientid

## Audio Buffer Sample Entropy Analysis

- **Attack Type**: AudioContext Fingerprinting
- **Target**: Browsers with mic access or audio simulation
- **Vulnerability**: Entropy leakage via noise pattern
- **MITRE**: T1606
- **Impact**: Unique hardware identification
- **Tools**: Web Audio API
- **Scenario**: Analyzes entropy of noise floor from mic or sample
- **Attack Steps**: 1. Site requests mic input (or simulates background noise using AudioBufferSourceNode). 2. Reads waveform data at very low amplitude. 3. Entropy levels in the noise floor differ between microphones, OS audio stacks, and environments. 4. These tiny inconsistencies provide unique device signatures. 5. Results are passed through a hash and combined with timing and sampling rate data. 6. Even devices of same model may show slight variation. 7. No need for audio playback or visible elements. 8. Strong privacy concern as users typically don’t expect mic use without prompts.
- **Detection**: Block mic access or add noise floor jitter
- **Solution**: Enforce user permission on all audio APIs
- **Tags**: #micentropy #soundfp #noiseleak

## Font Metric Probing via getBoundingClientRect

- **Attack Type**: Font Metrics Fingerprinting
- **Target**: All browsers with standard font stack
- **Vulnerability**: Font dimension leakage
- **MITRE**: T1606
- **Impact**: OS/font stack fingerprinting
- **Tools**: DOM API, JS
- **Scenario**: Measures font dimensions for OS and font stack
- **Attack Steps**: 1. Script creates invisible <span> elements with specific font styles (e.g., "Times", "Courier", "Arial", etc.). 2. Measures their width/height using getBoundingClientRect(). 3. Font rendering engines differ in how they calculate glyph spacing and kerning. 4. These measurements are consistent for the same OS, browser, and font stack. 5. A full profile is built by measuring many fonts in sequence. 6. Combined with canvas output, this creates a powerful fingerprint. 7. Method does not require user interaction. 8. Runs on page load and results are sent silently to attacker server.
- **Detection**: Use generic fonts and normalize metrics
- **Solution**: Block repeated DOM probing via span+metrics
- **Tags**: #fontfp #glyphwidth #kerning

## AudioContext Latency Compensation Abuse

- **Attack Type**: AudioContext Fingerprinting
- **Target**: Audio-capable browsers
- **Vulnerability**: OS/hardware latency leakage
- **MITRE**: T1606
- **Impact**: Device category inference
- **Tools**: Web Audio API
- **Scenario**: Uses baseLatency to detect device and driver stack
- **Attack Steps**: 1. Script creates a new AudioContext and reads the baseLatency property. 2. This reflects the minimum latency introduced by audio pipeline and drivers. 3. Most modern browsers expose this value, which varies by OS and hardware. 4. The script logs and hashes this value as part of a browser fingerprint. 5. Results can distinguish laptop vs desktop vs mobile environments. 6. Execution is silent and invisible to the user. 7. Combined with sample rate, this increases fingerprint entropy. 8. Many users are unaware this detail is even available.
- **Detection**: Return fixed or rounded latency values
- **Solution**: Disable baseLatency or randomize output
- **Tags**: #audiolatency #driverfp #latencyfp

## Screen Color Depth Fingerprinting

- **Attack Type**: Display Fingerprinting
- **Target**: Browsers exposing screen metrics
- **Vulnerability**: Leaked display characteristics
- **MITRE**: T1606
- **Impact**: Screen hardware fingerprinting
- **Tools**: JS API
- **Scenario**: Uses screen.colorDepth and pixelDepth for profiling
- **Attack Steps**: 1. Script reads screen.colorDepth and screen.pixelDepth values on load. 2. These indicate how many bits are used per color channel (e.g., 24, 30, 32). 3. Older monitors and some Linux systems expose different values than modern macOS/Windows. 4. The combination helps narrow down hardware type. 5. Used alongside resolution and ratio data to improve uniqueness. 6. Data is logged into a fingerprint hash. 7. Works silently and consistently. 8. Few privacy extensions block this API access.
- **Detection**: Return fixed values like 24-bit
- **Solution**: Randomize or spoof color depth reports
- **Tags**: #colordepthfp #displayfp #screenmetrics

## Canvas EMF Font Rendering

- **Attack Type**: Canvas Fingerprinting
- **Target**: Windows browsers with canvas support
- **Vulnerability**: EMF rendering leakage
- **MITRE**: T1606
- **Impact**: OS-level fingerprinting
- **Tools**: Canvas API, Windows OS
- **Scenario**: Detects Windows EMF font rendering quirks
- **Attack Steps**: 1. Script draws text in exotic fonts (e.g., Batang, PMingLiU) onto canvas. 2. It reads pixel-level output and analyzes vector rendering via Enhanced Metafile (EMF) mode. 3. Windows-specific EMF behavior introduces signature antialiasing or spacing differences. 4. These traits are consistent across Windows systems and vary by font fallback settings. 5. Attacker builds a fingerprint unique to Windows font subsystems. 6. The process is silent, runs in background, and doesn’t affect visible content. 7. Combined with fallback order detection, it boosts accuracy. 8. Particularly useful for distinguishing Windows environments from macOS/Linux.
- **Detection**: Restrict use of rare fonts in canvas
- **Solution**: Add rendering noise to obscure spacing
- **Tags**: #emffp #windowsfontfp #canvasleak

