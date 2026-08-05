# Vulnerable Code Samples: JavaScript

Secure-code-review training examples (62 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — Cross-Site Scripting (XSS)

- **Language**: JavaScript
- **Vulnerability**: Cross-Site Scripting (XSS)
- **Description**: Directly injecting user input into DOM without sanitization.

```
function displayComment(comment) {
    document.getElementById('output').innerHTML = comment;
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/xss/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 2 — CSRF

- **Language**: JavaScript
- **Vulnerability**: CSRF
- **Description**: Making HTTP requests without CSRF token validation.

```
function updateUser(data) {
    fetch('/update', { method: 'POST', body: JSON.stringify(data) });
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/csrf
- CWE-352: https://cwe.mitre.org/data/definitions/352.html

## Sample 3 — Insecure Randomness

- **Language**: JavaScript
- **Vulnerability**: Insecure Randomness
- **Description**: Using Math.random() for cryptographic purposes.

```
function generateToken() {
    return Math.random().toString(36).substring(2);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 4 — Insecure Cookie Handling

- **Language**: JavaScript
- **Vulnerability**: Insecure Cookie Handling
- **Description**: Setting cookies without Secure and HttpOnly flags.

```
document.cookie = 'session=12345; expires=Wed, 24 May 2025 12:00:00 UTC;';
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-614: https://cwe.mitre.org/data/definitions/614.html

## Sample 5 — Prototype Pollution

- **Language**: JavaScript
- **Vulnerability**: Prototype Pollution
- **Description**: Allowing user input to modify object prototypes.

```
function setValue(obj, key, value) {
    obj[key] = value;
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Prototype_Pollution
- CWE-1321: https://cwe.mitre.org/data/definitions/1321.html

## Sample 6 — Eval Injection

- **Language**: JavaScript
- **Vulnerability**: Eval Injection
- **Description**: Using eval() with user input.

```
function runCode(code) {
    eval(code);
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Eval_Injection
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 7 — Insecure JSON Parsing

- **Language**: JavaScript
- **Vulnerability**: Insecure JSON Parsing
- **Description**: Parsing JSON without validation.

```
function parseData(data) {
    return JSON.parse(data);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 8 — Insecure Storage

- **Language**: JavaScript
- **Vulnerability**: Insecure Storage
- **Description**: Storing sensitive data in localStorage.

```
function saveToken(token) {
    localStorage.setItem('token', token);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-922: https://cwe.mitre.org/data/definitions/922.html

## Sample 9 — Insecure File Access

- **Language**: JavaScript
- **Vulnerability**: Insecure File Access
- **Description**: Accessing files without path validation.

```
const fs = require('fs');
function readFile(path) {
    return fs.readFileSync(path, 'utf8');
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Path_Traversal
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 10 — Insecure CORS Configuration

- **Language**: JavaScript
- **Vulnerability**: Insecure CORS Configuration
- **Description**: Allowing all origins in CORS policy.

```
const express = require('express');
const app = express();
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    next();
});
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-942: https://cwe.mitre.org/data/definitions/942.html

## Sample 11 — Insecure Regex

- **Language**: JavaScript
- **Vulnerability**: Insecure Regex
- **Description**: Using regex vulnerable to ReDoS.

```
function validate(str) {
    return /(a+)+b/.test(str);
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 12 — Cross-Site Scripting (XSS)

- **Language**: JavaScript
- **Vulnerability**: Cross-Site Scripting (XSS)
- **Description**: Directly injecting user input into DOM without sanitization.

```
function displayComment(comment) {
    document.getElementById('output').innerHTML = comment;
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/xss/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 13 — CSRF

- **Language**: JavaScript
- **Vulnerability**: CSRF
- **Description**: Making HTTP requests without CSRF token validation.

```
function updateUser(data) {
    fetch('/update', { method: 'POST', body: JSON.stringify(data) });
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/csrf
- CWE-352: https://cwe.mitre.org/data/definitions/352.html

## Sample 14 — Insecure Randomness

- **Language**: JavaScript
- **Vulnerability**: Insecure Randomness
- **Description**: Using Math.random() for cryptographic purposes.

```
function generateToken() {
    return Math.random().toString(36).substring(2);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 15 — Insecure Cookie Handling

- **Language**: JavaScript
- **Vulnerability**: Insecure Cookie Handling
- **Description**: Setting cookies without Secure and HttpOnly flags.

```
document.cookie = 'session=12345; expires=Wed, 24 May 2025 12:00:00 UTC;';
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-614: https://cwe.mitre.org/data/definitions/614.html

## Sample 16 — Prototype Pollution

- **Language**: JavaScript
- **Vulnerability**: Prototype Pollution
- **Description**: Allowing user input to modify object prototypes.

```
function setValue(obj, key, value) {
    obj[key] = value;
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Prototype_Pollution
- CWE-1321: https://cwe.mitre.org/data/definitions/1321.html

## Sample 17 — Eval Injection

- **Language**: JavaScript
- **Vulnerability**: Eval Injection
- **Description**: Using eval() with user input.

```
function runCode(code) {
    eval(code);
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Eval_Injection
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 18 — Insecure JSON Parsing

- **Language**: JavaScript
- **Vulnerability**: Insecure JSON Parsing
- **Description**: Parsing JSON without validation.

```
function parseData(data) {
    return JSON.parse(data);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 19 — Insecure Storage

- **Language**: JavaScript
- **Vulnerability**: Insecure Storage
- **Description**: Storing sensitive data in localStorage.

```
function saveToken(token) {
    localStorage.setItem('token', token);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-922: https://cwe.mitre.org/data/definitions/922.html

## Sample 20 — Insecure File Access

- **Language**: JavaScript
- **Vulnerability**: Insecure File Access
- **Description**: Accessing files without path validation.

```
const fs = require('fs');
function readFile(path) {
    return fs.readFileSync(path, 'utf8');
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Path_Traversal
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 21 — Insecure CORS Configuration

- **Language**: JavaScript
- **Vulnerability**: Insecure CORS Configuration
- **Description**: Allowing all origins in CORS policy.

```
const express = require('express');
const app = express();
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    next();
});
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-942: https://cwe.mitre.org/data/definitions/942.html

## Sample 22 — Insecure Regex

- **Language**: JavaScript
- **Vulnerability**: Insecure Regex
- **Description**: Using regex vulnerable to ReDoS.

```
function validate(str) {
    return /(a+)+b/.test(str);
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 23 — Logic Flaw in Authentication

- **Language**: JavaScript
- **Vulnerability**: Logic Flaw in Authentication
- **Description**: Bypassing authentication by manipulating boolean checks.

```
function isAuthenticated(user) {
    return user.isAdmin == true || user.role == 'admin';
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-840: https://cwe.mitre.org/data/definitions/840.html

## Sample 24 — Insecure Dynamic Function

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Function
- **Description**: Creating functions dynamically from user input.

```
function createFunction(code) {
    return new Function(code);
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Code_Injection
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 25 — Insecure Worker Thread

- **Language**: JavaScript
- **Vulnerability**: Insecure Worker Thread
- **Description**: Passing unvalidated data to Web Worker.

```
const worker = new Worker('worker.js');
worker.postMessage(userInput);
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Code_Injection
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 26 — Misconfigured Rate Limiting

- **Language**: JavaScript
- **Vulnerability**: Misconfigured Rate Limiting
- **Description**: Failing to enforce rate limits on API endpoints, allowing brute force attacks.

```
const express = require('express');
const app = express();
app.post('/login', (req, res) => {
    authenticate(req.body);
});
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-770: https://cwe.mitre.org/data/definitions/770.html

## Sample 27 — Insecure Service Worker

- **Language**: JavaScript
- **Vulnerability**: Insecure Service Worker
- **Description**: Registering service worker with unvalidated scope.

```
navigator.serviceWorker.register(userInput + '/sw.js');
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 28 — Insecure WebRTC Configuration

- **Language**: JavaScript
- **Vulnerability**: Insecure WebRTC Configuration
- **Description**: Using WebRTC without proper ICE server validation.

```
const pc = new RTCPeerConnection({ iceServers: [{ urls: userInput }] });
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-295: https://cwe.mitre.org/data/definitions/295.html

## Sample 29 — Insecure Clipboard Access

- **Language**: JavaScript
- **Vulnerability**: Insecure Clipboard Access
- **Description**: Reading clipboard data without user consent.

```
navigator.clipboard.readText().then(data => console.log(data));
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 30 — Insecure Geolocation Access

- **Language**: JavaScript
- **Vulnerability**: Insecure Geolocation Access
- **Description**: Accessing geolocation without user consent.

```
navigator.geolocation.getCurrentPosition(pos => console.log(pos));
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 31 — Insecure Dynamic Import

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Import
- **Description**: Importing modules dynamically with user input.

```
async function loadModule(name) {
    return import(name);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 32 — Insecure Notification API

- **Language**: JavaScript
- **Vulnerability**: Insecure Notification API
- **Description**: Using Notification API without permission checks.

```
new Notification(userInput);
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 33 — Insecure Broadcast Channel

- **Language**: JavaScript
- **Vulnerability**: Insecure Broadcast Channel
- **Description**: Using BroadcastChannel without validating messages.

```
const bc = new BroadcastChannel('channel');
bc.onmessage = (event) => eval(event.data);
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 34 — Insecure Shared Array Buffer

- **Language**: JavaScript
- **Vulnerability**: Insecure Shared Array Buffer
- **Description**: Using SharedArrayBuffer without security headers.

```
const sab = new SharedArrayBuffer(1024);
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-693: https://cwe.mitre.org/data/definitions/693.html

## Sample 35 — Insecure WebAssembly

- **Language**: JavaScript
- **Vulnerability**: Insecure WebAssembly
- **Description**: Loading WebAssembly modules from untrusted sources.

```
WebAssembly.instantiateStreaming(fetch(userInput));
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 36 — Insecure Dynamic Script Injection

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Script Injection
- **Description**: Injecting scripts dynamically with user input.

```
function injectScript(src) {
    const script = document.createElement('script');
    script.src = src;
    document.head.appendChild(script);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 37 — Insecure Dynamic Event Listener

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Event Listener
- **Description**: Adding event listeners dynamically with user input.

```
function addListener(element, event, handler) {
    element.addEventListener(event, () => eval(handler));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 38 — Insecure Dynamic Style Injection

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Style Injection
- **Description**: Injecting styles dynamically with user input.

```
function injectStyle(css) {
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 39 — Insecure Dynamic Worker Creation

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Worker Creation
- **Description**: Creating web workers dynamically with untrusted input.

```
function createWorker(script) {
    return new Worker(script);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 40 — Insecure WebSocket Origin

- **Language**: JavaScript
- **Vulnerability**: Insecure WebSocket Origin
- **Description**: Accepting WebSocket connections without origin validation.

```
const ws = new WebSocket(userInput);
ws.onopen = () => ws.send('data');
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-346: https://cwe.mitre.org/data/definitions/346.html

## Sample 41 — Insecure Dynamic Canvas Rendering

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Canvas Rendering
- **Description**: Rendering canvas content with untrusted data.

```
function renderCanvas(data) {
    const ctx = document.getElementById('canvas').getContext('2d');
    ctx.fillText(data, 10, 10);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 42 — Insecure Dynamic Meta Tag Injection

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Meta Tag Injection
- **Description**: Injecting meta tags dynamically with user input.

```
function injectMeta(content) {
    const meta = document.createElement('meta');
    meta.content = content;
    document.head.appendChild(meta);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 43 — Insecure Dynamic Audio Processing

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Audio Processing
- **Description**: Processing audio with untrusted data.

```
function processAudio(data) {
    const ctx = new AudioContext();
    ctx.decodeAudioData(data);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 44 — Insecure Dynamic Fetch Request

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Fetch Request
- **Description**: Making fetch requests with user-controlled URLs.

```
function fetchData(url) {
    fetch(url).then(res => res.json());
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 45 — Insecure Dynamic Beacon API

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Beacon API
- **Description**: Using navigator.sendBeacon with untrusted URLs.

```
function sendBeacon(url) {
    navigator.sendBeacon(url, 'data');
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 46 — Insecure Dynamic History Manipulation

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic History Manipulation
- **Description**: Manipulating browser history with untrusted input.

```
function updateHistory(url) {
    history.pushState({}, '', url);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 47 — Insecure Dynamic Service Worker Cache

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Service Worker Cache
- **Description**: Caching resources with untrusted URLs in service workers.

```
self.addEventListener('install', event => {
    event.waitUntil(caches.open('cache').then(cache => cache.add(userInput)));
});
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 48 — Insecure Dynamic Push Subscription

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Push Subscription
- **Description**: Subscribing to push notifications with untrusted endpoints.

```
function subscribePush(endpoint) {
    navigator.serviceWorker.ready.then(reg => reg.pushManager.subscribe({userVisibleOnly: true, applicationServerKey: endpoint}));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 49 — Insecure Dynamic Vibration API

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Vibration API
- **Description**: Using Vibration API with untrusted patterns.

```
function vibrate(pattern) {
    navigator.vibrate(pattern);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 50 — Insecure Dynamic Gamepad API

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Gamepad API
- **Description**: Using Gamepad API with untrusted input.

```
function handleGamepad() {
    const gamepads = navigator.getGamepads();
    console.log(gamepads[0].buttons);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 51 — Insecure Dynamic MIDI Access

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic MIDI Access
- **Description**: Accessing MIDI devices without validation.

```
function accessMIDI() {
    navigator.requestMIDIAccess().then(midi => console.log(midi.inputs));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 52 — Insecure Dynamic Presentation Request

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Presentation Request
- **Description**: Initiating presentation requests with untrusted URLs.

```
function startPresentation(url) {
    navigator.presentation.requestSession(url);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 53 — Insecure Dynamic Credential Manager

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Credential Manager
- **Description**: Using Credential Manager with untrusted input.

```
function storeCredentials(cred) {
    navigator.credentials.store(cred);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 54 — Insecure Dynamic Payment Request

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Payment Request
- **Description**: Initiating payment requests with untrusted details.

```
function requestPayment(details) {
    new PaymentRequest([{supportedMethods: 'basic-card'}], details).show();
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 55 — Insecure Dynamic Clipboard Access

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Clipboard Access
- **Description**: Accessing clipboard data without validation.

```
function readClipboard() {
    navigator.clipboard.readText().then(text => console.log(text));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 56 — Insecure Dynamic Worker Creation

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Worker Creation
- **Description**: Creating web workers with untrusted scripts.

```
function createWorker(url) {
    new Worker(url);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 57 — Insecure Dynamic Shared Array Buffer

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Shared Array Buffer
- **Description**: Using SharedArrayBuffer with untrusted data.

```
function shareBuffer(data) {
    const sab = new SharedArrayBuffer(data.length);
    const arr = new Uint8Array(sab);
    arr.set(data);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 58 — Insecure Dynamic Broadcast Channel

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Broadcast Channel
- **Description**: Using BroadcastChannel with untrusted messages.

```
function broadcast(name, message) {
    new BroadcastChannel(name).postMessage(message);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 59 — Insecure Dynamic Message Channel

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Message Channel
- **Description**: Using MessageChannel with untrusted messages.

```
function sendMessage(message) {
    const channel = new MessageChannel();
    channel.port1.postMessage(message);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 60 — Insecure Dynamic Intersection Observer

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Intersection Observer
- **Description**: Using IntersectionObserver with untrusted callbacks.

```
function observe(element, callback) {
    new IntersectionObserver(entries => eval(callback)).observe(document.querySelector(element));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 61 — Insecure Dynamic Resize Observer

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Resize Observer
- **Description**: Using ResizeObserver with untrusted callbacks.

```
function observeResize(element, callback) {
    new ResizeObserver(entries => eval(callback)).observe(document.querySelector(element));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 62 — Insecure Dynamic Performance Mark

- **Language**: JavaScript
- **Vulnerability**: Insecure Dynamic Performance Mark
- **Description**: Creating performance marks with untrusted names.

```
function markPerformance(name) {
    performance.mark(name);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html
