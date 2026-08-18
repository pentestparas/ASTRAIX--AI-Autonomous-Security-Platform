# Protocol Injection Payload List

<p align="center">
  <img src="https://img.shields.io/badge/payloads-7+-brightgreen.svg" alt="Payload Categories">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/maintained-yes-success.svg" alt="Maintained">
  <img src="https://img.shields.io/badge/PRs-welcome-orange.svg" alt="PRs Welcome">
</p>

A comprehensive collection of protocol injection payloads for security testing and vulnerability assessment. This repository contains carefully curated payloads for various protocol-level injection attacks that can be used with tools like Burp Suite Intruder.

## 📋 Table of Contents

- [Overview](#overview)
- [Vulnerability Types](#vulnerability-types)
- [Repository Structure](#repository-structure)
- [Payload Categories](#payload-categories)
- [Usage](#usage)
- [Testing Tools](#testing-tools)
- [Disclaimer](#disclaimer)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Protocol injection vulnerabilities occur when untrusted data is sent to an interpreter as part of a command or query. Attackers can exploit these vulnerabilities to execute unintended commands, access unauthorized data, or compromise system security.

This repository provides an extensive collection of injection payloads organized by protocol type, designed to help security professionals:

- Identify and test for protocol injection vulnerabilities
- Perform comprehensive security assessments
- Understand attack vectors and payload construction
- Validate security controls and input sanitization

## 🔍 Vulnerability Types

Protocol injection attacks can manifest in various forms:

- **HTTP Protocol Injection**: CRLF injection, HTTP request smuggling, header injection
- **SMTP Injection**: Email header injection, mail relay abuse
- **LDAP Injection**: Authentication bypass, filter manipulation
- **SQL Injection**: Database manipulation, authentication bypass
- **XPath Injection**: XML data extraction, authentication bypass
- **SSRF**: Server-side request forgery, internal network access
- **Command Injection**: OS command execution, remote code execution
- **XXE**: XML external entity injection, file disclosure

## 📁 Repository Structure

```
protocol-injection-payload-list/
│
├── README.md                          # Documentation
├── LICENSE                            # License information
│
├── Intruder/                          # Burp Suite Intruder payload files
│   ├── http-injection.txt             # HTTP protocol injection payloads
│   ├── smtp-injection.txt             # SMTP protocol injection payloads
│   ├── ldap-injection.txt             # LDAP injection payloads
│   ├── sql-injection.txt              # SQL injection payloads
│   ├── xpath-injection.txt            # XPath injection payloads
│   ├── ssrf-injection.txt             # SSRF payloads
│   ├── command-injection.txt          # OS command injection payloads
│   └── xxe-injection.txt              # XXE injection payloads
│
└── payloads/                          # Additional payload resources
```

## 🎯 Payload Categories

### 1. HTTP Protocol Injection (166 payloads)

HTTP protocol injection payloads target web applications and servers to manipulate HTTP requests and responses.

**Includes:**
- CRLF injection variants (URL encoded, Unicode, double encoded)
- HTTP request smuggling (CL.TE, TE.CL, TE.TE)
- Header injection (X-Forwarded-For, Host, Cookie)
- Response splitting and cache poisoning
- Transfer-Encoding obfuscation
- Protocol downgrade attacks

**File:** `Intruder/http-injection.txt`

### 2. SMTP Protocol Injection (233 payloads)

Email protocol injection payloads for testing mail servers and email processing systems.

**Includes:**
- Email header injection (Bcc, Cc, From, Subject)
- SMTP command injection
- MIME header manipulation
- Email relay exploitation
- SPF/DKIM bypass attempts
- Mail loop creation

**File:** `Intruder/smtp-injection.txt`

### 3. LDAP Injection (315 payloads)

LDAP injection payloads for directory service authentication and query manipulation.

**Includes:**
- Authentication bypass techniques
- Boolean-based blind injection
- Filter manipulation (OR, AND, NOT logic)
- Wildcard attacks
- Attribute enumeration
- Active Directory specific payloads

**File:** `Intruder/ldap-injection.txt`

### 4. SQL Injection (346 payloads)

Comprehensive SQL injection payloads supporting multiple database systems.

**Includes:**
- Authentication bypass
- Union-based injection
- Boolean-based blind injection
- Time-based blind injection
- Error-based injection
- Stacked queries
- Database enumeration (MySQL, PostgreSQL, MSSQL, Oracle, SQLite)
- WAF bypass techniques

**File:** `Intruder/sql-injection.txt`

### 5. XPath Injection (332 payloads)

XPath injection payloads for XML data extraction and manipulation.

**Includes:**
- Authentication bypass
- Boolean-based injection
- Blind injection techniques
- Node traversal
- Function-based injection
- String manipulation
- Encoding bypass methods

**File:** `Intruder/xpath-injection.txt`

### 6. SSRF Injection (447 payloads)

Server-Side Request Forgery payloads for internal network access and metadata exploitation.

**Includes:**
- Localhost and loopback variations
- Cloud metadata endpoints (AWS, GCP, Azure, Digital Ocean)
- Private network ranges
- Alternative IP representations (decimal, octal, hex)
- Protocol wrappers (file, gopher, dict, ldap)
- URL parser bypass techniques
- Port scanning payloads

**File:** `Intruder/ssrf-injection.txt`

### 7. Command Injection (539 payloads)

OS command injection payloads for Linux, Unix, and Windows systems.

**Includes:**
- Command separators and chaining
- Shell command substitution
- Reverse shell payloads (Bash, Netcat, Python, Perl, PHP, Ruby)
- Filter bypass techniques
- Obfuscation methods
- Data exfiltration
- Encoding variations

**File:** `Intruder/command-injection.txt`

### 8. XXE Injection (223 payloads)

XML External Entity injection payloads for file disclosure and SSRF.

**Includes:**
- Basic file disclosure
- PHP wrapper exploitation
- Blind out-of-band XXE
- Error-based data exfiltration
- XXE via file uploads (SVG, DOCX, XLSX)
- DoS attacks (Billion Laughs)
- XInclude attacks
- Multiple protocol exploitation

**File:** `Intruder/xxe-injection.txt`

## 💻 Usage

### Burp Suite Intruder

1. **Load Payloads:**
   - Navigate to Intruder → Positions
   - Configure injection points
   - Go to Payloads tab
   - Select "Simple list" as payload type
   - Click "Load" and select desired payload file from `Intruder/` directory

2. **Configure Options:**
   - Set appropriate encoding if needed
   - Configure grep match for success indicators
   - Adjust throttling based on target

3. **Start Attack:**
   - Click "Start attack"
   - Analyze responses for vulnerabilities

### Command Line Tools

```bash
# Using with ffuf
ffuf -u https://target.com/api?param=FUZZ -w Intruder/sql-injection.txt

# Using with wfuzz
wfuzz -c -z file,Intruder/command-injection.txt https://target.com/exec?cmd=FUZZ

# Using with curl
while IFS= read -r payload; do
    curl "https://target.com/search?q=$payload"
done < Intruder/xss-injection.txt
```

### Custom Scripts

```python
# Python example
import requests

with open('Intruder/sql-injection.txt', 'r') as f:
    payloads = f.readlines()

for payload in payloads:
    payload = payload.strip()
    if payload and not payload.startswith('#'):
        response = requests.get(f'https://target.com/api?id={payload}')
        # Analyze response
```

## 🛠️ Testing Tools

These payloads are compatible with various security testing tools:

- **Burp Suite** - Web application security testing
- **OWASP ZAP** - Automated security scanning
- **SQLmap** - SQL injection automation
- **Commix** - Command injection exploitation
- **ffuf** - Fast web fuzzer
- **wfuzz** - Web application fuzzer
- **Nuclei** - Vulnerability scanner
- **Custom Scripts** - Python, Bash, PowerShell

## ⚠️ Disclaimer

**IMPORTANT: FOR AUTHORIZED TESTING ONLY**

This repository is intended for:
- Authorized security testing and penetration testing
- Educational purposes and security research
- Vulnerability assessment with proper authorization
- Security tool development and testing

**You must:**
- ✅ Obtain explicit written permission before testing any system
- ✅ Only test systems you own or have authorization to test
- ✅ Comply with all applicable laws and regulations
- ✅ Follow responsible disclosure practices

**You must not:**
- ❌ Use these payloads against systems without authorization
- ❌ Perform testing that could cause harm or disruption
- ❌ Violate any laws, regulations, or terms of service
- ❌ Use for malicious purposes

The authors and contributors of this repository are not responsible for any misuse or damage caused by these payloads. Users are solely responsible for their actions.

## 🤝 Contributing

Contributions are welcome! If you have additional payloads, improvements, or corrections:

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/new-payloads
   ```
3. **Add your payloads** following the existing format:
   - One payload per line
   - Include descriptive comments with `#`
   - Group related payloads together
   - Test payloads before submitting
4. **Commit your changes:**
   ```bash
   git commit -am 'Add new XXE payloads'
   ```
5. **Push to the branch:**
   ```bash
   git push origin feature/new-payloads
   ```
6. **Create a Pull Request**

### Contribution Guidelines

- Ensure payloads are unique and not duplicates
- Provide clear descriptions and context
- Follow the existing file structure
- Test payloads in controlled environments
- Document any special requirements or dependencies

## 📚 Resources

### Learning Materials

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTricks - Pentesting Methodology](https://book.hacktricks.xyz/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

### Related Projects

- [SecLists](https://github.com/danielmiessler/SecLists)
- [FuzzDB](https://github.com/fuzzdb-project/fuzzdb)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)

## 📊 Statistics

- **Total Payload Categories:** 8
- **Total Payloads:** 2,600+
- **File Formats:** Plain text (.txt)
- **Encoding:** UTF-8
- **Last Updated:** 2024

## 📖 References

- OWASP Testing Guide
- CWE (Common Weakness Enumeration)
- CVE (Common Vulnerabilities and Exposures)
- MITRE ATT&CK Framework
- Bug Bounty Platforms (HackerOne, Bugcrowd, Intigriti)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

Special thanks to the security research community for their continuous contributions to vulnerability research and payload development.

---

<p align="center">
  <b>⚡ Happy Hunting! ⚡</b><br>
  <sub>Remember: With great power comes great responsibility. Test ethically.</sub>
</p>

<p align="center">
  <a href="#top">⬆️ Back to Top</a>
</p>