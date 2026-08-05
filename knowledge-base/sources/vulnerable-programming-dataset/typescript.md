# Vulnerable Code Samples: TypeScript

Secure-code-review training examples (60 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — Insecure Cryptography

- **Language**: TypeScript
- **Vulnerability**: Insecure Cryptography
- **Description**: Using weak cryptographic algorithm (MD5).

```
import { createHash } from 'crypto';
function hashPassword(password: string): string {
    return createHash('md5').update(password).digest('hex');
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-327: https://cwe.mitre.org/data/definitions/327.html

## Sample 2 — Prototype Pollution

- **Language**: TypeScript
- **Vulnerability**: Prototype Pollution
- **Description**: Modifying object prototypes via user input.

```
function merge(target: any, source: any) {
    for (const key in source) {
        target[key] = source[key];
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Prototype_Pollution
- CWE-1321: https://cwe.mitre.org/data/definitions/1321.html

## Sample 3 — Hardcoded Secrets

- **Language**: TypeScript
- **Vulnerability**: Hardcoded Secrets
- **Description**: Embedding sensitive API keys in code.

```
const API_KEY: string = 'abc123-secret-key';
async function fetchData(): Promise<void> {
    const response = await fetch(`https://api.example.com/data?key=${API_KEY}`);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 4 — SQL Injection

- **Language**: TypeScript
- **Vulnerability**: SQL Injection
- **Description**: Concatenating user input in SQL query.

```
async function getUser(db: any, username: string): Promise<any> {
    return db.query(`SELECT * FROM users WHERE username = '${username}'`);
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 5 — Insecure File Access

- **Language**: TypeScript
- **Vulnerability**: Insecure File Access
- **Description**: Accessing files without path validation.

```
import * as fs from 'fs';
function readFile(path: string): string {
    return fs.readFileSync(path, 'utf8');
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Path_Traversal
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 6 — CSRF

- **Language**: TypeScript
- **Vulnerability**: CSRF
- **Description**: Making POST requests without CSRF tokens.

```
async function updateData(data: any): Promise<void> {
    await fetch('/api/update', { method: 'POST', body: JSON.stringify(data) });
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/csrf
- CWE-352: https://cwe.mitre.org/data/definitions/352.html

## Sample 7 — Insecure Redirect

- **Language**: TypeScript
- **Vulnerability**: Insecure Redirect
- **Description**: Redirecting to user-supplied URL.

```
function redirect(url: string): void {
    window.location.href = url;
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Unvalidated_Redirects_and_Forwards
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 8 — Insecure Randomness

- **Language**: TypeScript
- **Vulnerability**: Insecure Randomness
- **Description**: Using Math.random() for security-sensitive operations.

```
function generateId(): string {
    return Math.random().toString(36).substring(2);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 9 — Insecure Logging

- **Language**: TypeScript
- **Vulnerability**: Insecure Logging
- **Description**: Logging sensitive data without sanitization.

```
function logUser(user: { password: string }): void {
    console.log(`User password: ${user.password}`);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-532: https://cwe.mitre.org/data/definitions/532.html

## Sample 10 — Insecure Session Storage

- **Language**: TypeScript
- **Vulnerability**: Insecure Session Storage
- **Description**: Storing session tokens in localStorage.

```
function storeSession(token: string): void {
    localStorage.setItem('sessionToken', token);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-922: https://cwe.mitre.org/data/definitions/922.html

## Sample 11 — Insecure XML Parsing

- **Language**: TypeScript
- **Vulnerability**: Insecure XML Parsing
- **Description**: Parsing XML with external entity processing enabled.

```
import { DOMParser } from 'xmldom';
function parseXML(xml: string): Document {
    return new DOMParser().parseFromString(xml);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing
- CWE-611: https://cwe.mitre.org/data/definitions/611.html

## Sample 12 — Insecure Cryptography

- **Language**: TypeScript
- **Vulnerability**: Insecure Cryptography
- **Description**: Using weak cryptographic algorithm (MD5).

```
import { createHash } from 'crypto';
function hashPassword(password: string): string {
    return createHash('md5').update(password).digest('hex');
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-327: https://cwe.mitre.org/data/definitions/327.html

## Sample 13 — Prototype Pollution

- **Language**: TypeScript
- **Vulnerability**: Prototype Pollution
- **Description**: Modifying object prototypes via user input.

```
function merge(target: any, source: any) {
    for (const key in source) {
        target[key] = source[key];
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Prototype_Pollution
- CWE-1321: https://cwe.mitre.org/data/definitions/1321.html

## Sample 14 — Hardcoded Secrets

- **Language**: TypeScript
- **Vulnerability**: Hardcoded Secrets
- **Description**: Embedding sensitive API keys in code.

```
const API_KEY: string = 'abc123-secret-key';
async function fetchData(): Promise<void> {
    const response = await fetch(`https://api.example.com/data?key=${API_KEY}`);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 15 — SQL Injection

- **Language**: TypeScript
- **Vulnerability**: SQL Injection
- **Description**: Concatenating user input in SQL query.

```
async function getUser(db: any, username: string): Promise<any> {
    return db.query(`SELECT * FROM users WHERE username = '${username}'`);
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 16 — Insecure File Access

- **Language**: TypeScript
- **Vulnerability**: Insecure File Access
- **Description**: Accessing files without path validation.

```
import * as fs from 'fs';
function readFile(path: string): string {
    return fs.readFileSync(path, 'utf8');
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Path_Traversal
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 17 — CSRF

- **Language**: TypeScript
- **Vulnerability**: CSRF
- **Description**: Making POST requests without CSRF tokens.

```
async function updateData(data: any): Promise<void> {
    await fetch('/api/update', { method: 'POST', body: JSON.stringify(data) });
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/csrf
- CWE-352: https://cwe.mitre.org/data/definitions/352.html

## Sample 18 — Insecure Redirect

- **Language**: TypeScript
- **Vulnerability**: Insecure Redirect
- **Description**: Redirecting to user-supplied URL.

```
function redirect(url: string): void {
    window.location.href = url;
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Unvalidated_Redirects_and_Forwards
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 19 — Insecure Randomness

- **Language**: TypeScript
- **Vulnerability**: Insecure Randomness
- **Description**: Using Math.random() for security-sensitive operations.

```
function generateId(): string {
    return Math.random().toString(36).substring(2);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 20 — Insecure Logging

- **Language**: TypeScript
- **Vulnerability**: Insecure Logging
- **Description**: Logging sensitive data without sanitization.

```
function logUser(user: { password: string }): void {
    console.log(`User password: ${user.password}`);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-532: https://cwe.mitre.org/data/definitions/532.html

## Sample 21 — Insecure Session Storage

- **Language**: TypeScript
- **Vulnerability**: Insecure Session Storage
- **Description**: Storing session tokens in localStorage.

```
function storeSession(token: string): void {
    localStorage.setItem('sessionToken', token);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-922: https://cwe.mitre.org/data/definitions/922.html

## Sample 22 — Insecure XML Parsing

- **Language**: TypeScript
- **Vulnerability**: Insecure XML Parsing
- **Description**: Parsing XML with external entity processing enabled.

```
import { DOMParser } from 'xmldom';
function parseXML(xml: string): Document {
    return new DOMParser().parseFromString(xml);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing
- CWE-611: https://cwe.mitre.org/data/definitions/611.html

## Sample 23 — Insecure WebSocket Handling

- **Language**: TypeScript
- **Vulnerability**: Insecure WebSocket Handling
- **Description**: Accepting unvalidated WebSocket messages.

```
const ws = new WebSocket('ws://example.com');
ws.onmessage = (event) => {
    eval(event.data);
};
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/WebSocket_Injection
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 24 — Insecure Dynamic Import

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Import
- **Description**: Dynamically importing modules based on user input.

```
async function loadModule(name: string): Promise<any> {
    return import(name);
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Code_Injection
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 25 — Insecure API Key Exposure

- **Language**: TypeScript
- **Vulnerability**: Insecure API Key Exposure
- **Description**: Exposing API keys in client-side code.

```
const API_KEY = 'abc123';
fetch(`https://api.example.com?key=${API_KEY}`);
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 26 — Insecure Event Listener

- **Language**: TypeScript
- **Vulnerability**: Insecure Event Listener
- **Description**: Adding event listeners that process untrusted data.

```
window.addEventListener('message', (event) => {
    eval(event.data);
});
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 27 — Insecure Message Passing

- **Language**: TypeScript
- **Vulnerability**: Insecure Message Passing
- **Description**: Processing unvalidated messages in postMessage.

```
window.addEventListener('message', (event) => {
    document.write(event.data);
});
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 28 — Insecure Dynamic Template

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Template
- **Description**: Using user input in template literals without sanitization.

```
function render(data: string): string {
    return `<div>${data}</div>`;
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 29 — Insecure Dynamic Property Access

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Property Access
- **Description**: Accessing object properties dynamically with user input.

```
function getProperty(obj: any, key: string): any {
    return obj[key];
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 30 — Insecure Dependency Injection

- **Language**: TypeScript
- **Vulnerability**: Insecure Dependency Injection
- **Description**: Injecting dependencies without validation.

```
function injectDependency(name: string): any {
    return require(name);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 31 — Insecure Worker Script

- **Language**: TypeScript
- **Vulnerability**: Insecure Worker Script
- **Description**: Loading worker scripts from untrusted sources.

```
const worker = new Worker(userInput);
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 32 — Insecure Dynamic Eval

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Eval
- **Description**: Using eval with dynamic user input.

```
function runCode(code: string): void {
    eval(code);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 33 — Insecure Dynamic URL Construction

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic URL Construction
- **Description**: Constructing URLs with unvalidated user input.

```
function navigate(url: string): void {
    window.location.href = url;
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 34 — Insecure Dynamic CSS

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic CSS
- **Description**: Applying CSS styles dynamically with user input.

```
function applyStyle(element: HTMLElement, css: string): void {
    element.style.cssText = css;
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 35 — Insecure Dynamic Event Dispatch

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Event Dispatch
- **Description**: Dispatching events with user-controlled data.

```
function dispatchEvent(eventName: string, data: any): void {
    window.dispatchEvent(new CustomEvent(eventName, { detail: data }));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 36 — Insecure Dynamic Attribute Injection

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Attribute Injection
- **Description**: Injecting HTML attributes dynamically with user input.

```
function setAttribute(element: HTMLElement, attr: string, value: string): void {
    element.setAttribute(attr, value);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 37 — Insecure Dynamic Module Resolution

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Module Resolution
- **Description**: Resolving modules dynamically with user input.

```
function resolveModule(path: string): any {
    return require(path);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 38 — Insecure Dynamic HTML Injection

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic HTML Injection
- **Description**: Injecting HTML dynamically with untrusted input.

```
function injectHTML(html: string): void {
    document.body.innerHTML = html;
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 39 — Insecure Dynamic JSONP Callback

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic JSONP Callback
- **Description**: Using user-controlled JSONP callbacks.

```
function fetchData(callback: string): void {
    const script = document.createElement('script');
    script.src = `https://api.example.com/data?callback=${callback}`;
    document.head.appendChild(script);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 40 — Insecure Dynamic Storage Access

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Storage Access
- **Description**: Accessing local storage with user-controlled keys.

```
function getStorage(key: string): string | null {
    return localStorage.getItem(key);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 41 — Insecure Dynamic Cookie Access

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Cookie Access
- **Description**: Accessing cookies with user-controlled names.

```
function getCookie(name: string): string | null {
    return document.cookie.split(';').find(c => c.trim().startsWith(name))?.split('=')[1] || null;
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 42 — Insecure Dynamic Form Submission

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Form Submission
- **Description**: Submitting forms with user-controlled actions.

```
function submitForm(action: string): void {
    const form = document.createElement('form');
    form.action = action;
    form.submit();
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 43 — Insecure Dynamic Animation Frame

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Animation Frame
- **Description**: Using requestAnimationFrame with untrusted callbacks.

```
function animate(callback: string): void {
    requestAnimationFrame(() => eval(callback));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 44 — Insecure Dynamic Timeout

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Timeout
- **Description**: Setting timeouts with user-controlled values.

```
function setTimeoutCallback(callback: string, delay: number): void {
    setTimeout(() => eval(callback), delay);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 45 — Insecure Dynamic Location Assignment

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Location Assignment
- **Description**: Assigning window.location with untrusted input.

```
function redirect(url: string): void {
    window.location.assign(url);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 46 — Insecure Dynamic WebGL Shader

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic WebGL Shader
- **Description**: Using WebGL shaders with untrusted code.

```
function createShader(gl: WebGLRenderingContext, code: string): void {
    const shader = gl.createShader(gl.VERTEX_SHADER)!;
    gl.shaderSource(shader, code);
    gl.compileShader(shader);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 47 — Insecure Dynamic Speech Synthesis

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Speech Synthesis
- **Description**: Using speech synthesis with untrusted text.

```
function speak(text: string): void {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 48 — Insecure Dynamic Device Orientation

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Device Orientation
- **Description**: Handling device orientation events with untrusted data.

```
function handleOrientation(event: DeviceOrientationEvent): void {
    console.log(event.alpha, event.beta, event.gamma);
}
window.addEventListener('deviceorientation', handleOrientation);
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 49 — Insecure Dynamic Battery Status

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Battery Status
- **Description**: Accessing battery status without validation.

```
function getBattery(): void {
    navigator.getBattery().then(battery => console.log(battery.level));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 50 — Insecure Dynamic Sensor Access

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Sensor Access
- **Description**: Accessing sensor data without validation.

```
function accessSensor(): void {
    const sensor = new Accelerometer();
    sensor.start();
    sensor.onreading = () => console.log(sensor.x);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 51 — Insecure Dynamic Proximity Sensor

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Proximity Sensor
- **Description**: Accessing proximity sensor data without validation.

```
function accessProximity(): void {
    const sensor = new ProximitySensor();
    sensor.start();
    sensor.onreading = () => console.log(sensor.near);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 52 — Insecure Dynamic Ambient Light Sensor

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Ambient Light Sensor
- **Description**: Accessing ambient light sensor without validation.

```
function accessLight(): void {
    const sensor = new AmbientLightSensor();
    sensor.start();
    sensor.onreading = () => console.log(sensor.illuminance);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 53 — Insecure Dynamic Geolocation Access

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Geolocation Access
- **Description**: Accessing geolocation data without validation.

```
function getLocation(): void {
    navigator.geolocation.getCurrentPosition(pos => console.log(pos.coords.latitude));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 54 — Insecure Dynamic Fullscreen Request

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Fullscreen Request
- **Description**: Requesting fullscreen with untrusted elements.

```
function requestFullscreen(element: string): void {
    document.querySelector(element)?.requestFullscreen();
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 55 — Insecure Dynamic Pointer Lock

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Pointer Lock
- **Description**: Requesting pointer lock with untrusted elements.

```
function lockPointer(element: string): void {
    document.querySelector(element)?.requestPointerLock();
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 56 — Insecure Dynamic Media Capture

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Media Capture
- **Description**: Capturing media with untrusted constraints.

```
function captureMedia(constraints: string): void {
    navigator.mediaDevices.getUserMedia(JSON.parse(constraints));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 57 — Insecure Dynamic Screen Capture

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Screen Capture
- **Description**: Capturing screen with untrusted constraints.

```
function captureScreen(constraints: string): void {
    navigator.mediaDevices.getDisplayMedia(JSON.parse(constraints));
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 58 — Insecure Dynamic Text Track

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Text Track
- **Description**: Adding text tracks with untrusted sources.

```
function addTrack(src: string): void {
    const track = document.createElement('track');
    track.src = src;
    document.querySelector('video')?.appendChild(track);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 59 — Insecure Dynamic Picture-in-Picture

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Picture-in-Picture
- **Description**: Entering picture-in-picture with untrusted elements.

```
function enterPiP(element: string): void {
    document.querySelector(element)?.requestPictureInPicture();
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 60 — Insecure Dynamic Source Map

- **Language**: TypeScript
- **Vulnerability**: Insecure Dynamic Source Map
- **Description**: Loading source maps with untrusted URLs.

```
function loadSourceMap(url: string): void {
    const script = document.createElement('script');
    script.src = url;
    document.head.appendChild(script);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html
