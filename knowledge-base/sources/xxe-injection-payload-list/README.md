# XXE Injection Payload List

<p align="center">
  <img src="https://img.shields.io/github/license/payload-box/xxe-injection-payload-list?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/payload-box/xxe-injection-payload-list?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/forks/payload-box/xxe-injection-payload-list?style=flat-square" alt="Forks">
  <img src="https://img.shields.io/github/issues/payload-box/xxe-injection-payload-list?style=flat-square" alt="Issues">
</p>

A comprehensive collection of **XML External Entity (XXE) Injection** payloads for penetration testing and security research. This repository contains carefully crafted payloads designed to test and exploit XXE vulnerabilities in web applications.

## 📋 Table of Contents

- [About XXE Injection](#about-xxe-injection)
- [Payload Categories](#payload-categories)
- [Installation](#installation)
- [Usage](#usage)
  - [Burp Suite Intruder](#burp-suite-intruder)
  - [Manual Testing](#manual-testing)
- [Payload Structure](#payload-structure)
- [Detection Techniques](#detection-techniques)
- [Prevention](#prevention)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [References](#references)
- [License](#license)

## 🎯 About XXE Injection

XML External Entity (XXE) injection is a web security vulnerability that allows an attacker to interfere with an application's processing of XML data. XXE vulnerabilities arise when an XML parser is configured to process external entities, allowing attackers to:

- **Read arbitrary files** from the server's filesystem
- **Perform Server-Side Request Forgery (SSRF)** attacks
- **Execute Denial of Service (DoS)** attacks
- **Scan internal network** infrastructure
- **Exfiltrate sensitive data**

### Impact Levels

- **Critical**: Arbitrary file reading, remote code execution
- **High**: Internal network scanning, SSRF
- **Medium**: Information disclosure, DoS

## 📦 Payload Categories

This repository contains the following payload categories:

| Category | File | Description |
|----------|------|-------------|
| **Basic XXE** | `Intruder/xxe-basic.txt` | Simple XXE payloads for file disclosure |
| **File Disclosure** | `Intruder/xxe-file-disclosure.txt` | Comprehensive file reading payloads |
| **SSRF via XXE** | `Intruder/xxe-ssrf.txt` | Server-Side Request Forgery payloads |
| **Blind/Out-of-Band XXE** | `Intruder/xxe-blind-oob.txt` | Out-of-band data exfiltration |
| **Error-Based XXE** | `Intruder/xxe-error-based.txt` | Error message exploitation |
| **DoS/XML Bomb** | `Intruder/xxe-dos.txt` | Denial of Service payloads |
| **XML Bomb** | `Intruder/xxe-xml-bomb.txt` | Billion laughs attack variants |
| **XInclude XXE** | `Intruder/xxe-xinclude.txt` | XInclude-based payloads |
| **SVG XXE** | `Intruder/xxe-svg.txt` | SVG file upload exploitation |
| **SOAP XXE** | `Intruder/xxe-soap.txt` | SOAP protocol exploitation |
| **PHP Wrappers** | `Intruder/xxe-php-wrappers.txt` | PHP filter wrapper payloads |
| **UTF-7 Encoded** | `Intruder/xxe-utf7-encoded.txt` | UTF-7 encoded payloads |
| **Parameter Entities** | `Intruder/xxe-parameter-entities.txt` | Parameter entity payloads |
| **Exotic Protocols** | `Intruder/xxe-exotic-protocols.txt` | Uncommon protocol exploitation |
| **Cloud Metadata** | `Intruder/xxe-cloud-metadata.txt` | Cloud provider metadata endpoints |

## 🚀 Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/payload-box/xxe-injection-payload-list.git
cd xxe-injection-payload-list
```

## 💻 Usage

### Burp Suite Intruder

1. **Capture the request** containing XML data in Burp Suite Proxy
2. **Send to Intruder** (Right-click → Send to Intruder)
3. **Position the payload markers** around the XML content or specific injection points
4. **Load payloads**:
   - Go to the "Payloads" tab
   - Click "Load" button
   - Select the appropriate payload file from the `Intruder/` directory
5. **Configure payload processing** if needed (encoding, etc.)
6. **Start the attack** and analyze responses

### Manual Testing

You can manually test individual payloads by:

1. Copying a payload from the appropriate file
2. Replacing placeholders (e.g., `ATTACKER_SERVER`, `FILE_PATH`)
3. Injecting into the target application's XML input
4. Monitoring the application's response

### Example Usage

```xml
<!-- Basic File Reading -->
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>
```

## 📊 Payload Structure

Each payload file in the `Intruder/` directory contains:

- **One payload per line** for easy integration with Burp Suite Intruder
- **Comments** (where applicable) explaining the payload purpose
- **Variations** of similar attacks for maximum coverage
- **Placeholders** that need to be customized:
  - `ATTACKER_SERVER` - Your server/IP for out-of-band attacks
  - `FILE_PATH` - Target file path to read
  - `PORT` - Port number for SSRF attacks

## 🔍 Detection Techniques

### Identifying XXE Vulnerabilities

1. **Input Analysis**: Look for XML processing endpoints
2. **File Upload**: Test with SVG, DOCX, XLSX files
3. **API Testing**: SOAP, REST APIs accepting XML
4. **Error Messages**: Verbose error messages may reveal parser details
5. **Response Time**: Delayed responses may indicate blind XXE
6. **Out-of-Band**: Monitor DNS/HTTP callbacks

### Tools for Detection

- Burp Suite Professional (Collaborator)
- OWASP ZAP
- XMLStarlet
- interactsh.com (for OOB detection)

## 🛡️ Prevention

### For Developers

1. **Disable External Entities**:
   ```java
   // Java
   factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
   ```

2. **Use Less Complex Data Formats**: Consider JSON instead of XML

3. **Update XML Processors**: Keep libraries up-to-date

4. **Input Validation**: Validate and sanitize XML input

5. **Disable DTD Processing**:
   ```python
   # Python
   from defusedxml import ElementTree as ET
   ```

6. **Whitelist-based Filtering**: Only allow expected XML structures

### Framework-Specific Prevention

- **PHP**: Use `libxml_disable_entity_loader(true)`
- **.NET**: Set `XmlReaderSettings.DtdProcessing = DtdProcessing.Prohibit`
- **Python**: Use `defusedxml` library
- **Java**: Configure SAXParserFactory/DocumentBuilderFactory securely

## 🤝 Contributing

Contributions are welcome! If you have additional XXE payloads or improvements:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-payload`)
3. Add your payloads to the appropriate Intruder file
4. Update README.md if necessary
5. Commit your changes (`git commit -am 'Add new XXE payload'`)
6. Push to the branch (`git push origin feature/new-payload`)
7. Create a Pull Request

### Contribution Guidelines

- One payload per line in Intruder files
- Include comments for complex payloads
- Test payloads before submitting
- Ensure payloads are ethical and legal to use in authorized testing
- Follow the existing format and structure

## ⚠️ Disclaimer

**IMPORTANT**: This repository is intended for **authorized security testing and educational purposes only**.

- ✅ Use these payloads only on systems you own or have explicit permission to test
- ✅ Obtain proper authorization before conducting any security assessments
- ❌ The authors are not responsible for any misuse or damage caused by these payloads
- ❌ Unauthorized access to computer systems is illegal

**By using this repository, you agree to use it responsibly and legally.**

## 📚 References

### Official Documentation

- [OWASP - XML External Entity (XXE) Processing](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing)
- [PortSwigger Web Security Academy - XXE Injection](https://portswigger.net/web-security/xxe)
- [CWE-611: Improper Restriction of XML External Entity Reference](https://cwe.mitre.org/data/definitions/611.html)

### Research Papers & Articles

- [XML External Entity (XXE) Injection Attacks](https://www.acunetix.com/blog/articles/xml-external-entity-xxe-vulnerabilities/)
- [Exploiting XXE Vulnerabilities in File Upload Functionality](https://www.blackhat.com/docs/us-15/materials/us-15-Vandevanter-Exploiting-XXE-Vulnerabilities-In-File-Parsing-Functionality.pdf)
- [Advanced XXE Exploitation Techniques](https://mohemiv.com/all/exploiting-xxe-with-local-dtd-files/)

### Tools

- [Burp Suite](https://portswigger.net/burp)
- [XXEinjector](https://github.com/enjoiz/XXEinjector)
- [OWASP ZAP](https://www.zaproxy.org/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>Made with ❤️ for the Security Community</b><br>
  <i>Happy (Ethical) Hunting! 🎯</i>
</p>

<p align="center">
  <a href="https://github.com/payload-box">More Payload Collections</a> •
  <a href="https://github.com/payload-box/xxe-injection-payload-list/issues">Report Bug</a> •
  <a href="https://github.com/payload-box/xxe-injection-payload-list/issues">Request Feature</a>
</p>