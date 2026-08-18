# Project Summary

## 📊 Command Injection Payload List - Complete Overview

This repository contains a comprehensive collection of **1,836 command injection payloads** organized across **11 specialized payload files** designed for security testing and penetration testing.

## 🎯 Project Structure

```
command-injection-payload-list/
├── Intruder/                                    # Payload files directory
│   ├── command-injection-basic.txt              # 105 payloads
│   ├── command-injection-time-based.txt         # 130 payloads
│   ├── command-injection-encoded.txt            # 99 payloads
│   ├── command-injection-obfuscated.txt         # 138 payloads
│   ├── command-injection-windows.txt            # 179 payloads
│   ├── command-injection-linux.txt              # 220 payloads
│   ├── command-injection-data-exfiltration.txt  # 150 payloads
│   ├── command-injection-bypass.txt             # 202 payloads
│   ├── command-injection-out-of-band.txt        # 203 payloads
│   ├── command-injection-special-chars.txt      # 187 payloads
│   └── command-injection-polyglot.txt           # 223 payloads
├── README.md                                     # Main documentation
├── CHEAT_SHEET.md                               # Quick reference guide
├── CONTRIBUTING.md                              # Contribution guidelines
├── SUMMARY.md                                   # This file
└── LICENSE                                      # MIT License

Total Payloads: 1,836
```

## 📦 Payload Categories Breakdown

### 1. Basic Command Injection (105 payloads)
- Common injection operators: `;`, `|`, `||`, `&`, `&&`
- Command substitution: backticks and `$()`
- Basic system commands across all operators

### 2. Time-Based Detection (130 payloads)
- Sleep commands with various durations
- Ping commands (Linux `-c` and Windows `-n` flags)
- Timeout commands
- Useful for blind command injection detection

### 3. Encoded Payloads (99 payloads)
- URL-encoded characters
- Hex-encoded commands
- Special character encoding
- Newline and carriage return variations

### 4. Obfuscated Commands (138 payloads)
- Shell variable manipulation (`${IFS}`, `$PATH`)
- Wildcard usage (`?`, `*`)
- Brace expansion
- Input redirection techniques
- Command substitution variations

### 5. Windows-Specific (179 payloads)
- CMD commands (dir, whoami, systeminfo, net user)
- PowerShell commands and encoded commands
- WMIC queries
- Windows file paths and registry queries
- Scheduled tasks and certutil
- Bitsadmin for file transfers

### 6. Linux/Unix-Specific (220 payloads)
- System information commands (uname, hostname, id)
- File reading (cat, grep, find)
- Network commands (ifconfig, netstat, nc)
- Process listing (ps, top)
- Reverse shells using bash, nc, telnet
- Scripting language execution (perl, python, ruby, php, awk)

### 7. Data Exfiltration (150 payloads)
- HTTP exfiltration using curl and wget
- DNS exfiltration using nslookup and dig
- Base64 encoding for data transfer
- POST requests with sensitive data
- Network-based data leakage
- SSH keys and credential extraction

### 8. Filter Bypass Techniques (202 payloads)
- Space character alternatives
- Null byte injection
- Quote manipulation
- Backslash escaping
- Multiple delimiter variations
- Comment character abuse
- Wildcard and globbing patterns

### 9. Out-of-Band Detection (203 payloads)
- External HTTP callbacks
- DNS lookups to attacker-controlled domains
- Reverse shell connections
- TCP/UDP callbacks
- Data exfiltration via headers
- Python, Perl, Ruby, and PHP reverse shells

### 10. Special Characters (187 payloads)
- Edge case delimiters
- Whitespace variations (tabs, newlines)
- Multiple operator combinations
- Null byte positions
- Comment characters in various positions
- Input/output redirection symbols

### 11. Polyglot & Context-Breaking (223 payloads)
- Quote-wrapped injections
- SQL injection combinations
- XSS-style wrappers
- Template injection patterns
- Multiple encoding layers
- Context escape sequences
- Language-agnostic patterns

## 🎓 Use Cases

### For Penetration Testers
- Comprehensive payload library for web application testing
- Ready-to-use with Burp Suite Intruder
- Organized by technique for systematic testing
- Time-saving with pre-built payload sets

### For Bug Bounty Hunters
- Complete arsenal for command injection hunting
- Platform-specific payloads for better coverage
- Bypass techniques for WAF evasion
- Out-of-band detection for blind vulnerabilities

### For Security Researchers
- Reference implementation of various techniques
- Educational resource for understanding injection methods
- Baseline for developing detection signatures
- Research material for WAF/IDS testing

### For Developers
- Examples of dangerous patterns to avoid
- Understanding attack vectors for secure coding
- Testing defensive code implementations
- Security awareness and training material

## 🔧 Integration Support

### Burp Suite
- Direct payload file loading into Intruder
- Compatible with Burp Collaborator for OOB testing
- Suitable for active scanning customization

### OWASP ZAP
- Fuzzer-compatible format
- Can be imported as custom payloads
- Works with ZAP's active scan rules

### Custom Scripts
- Simple text format for easy parsing
- One payload per line for script integration
- Suitable for automation frameworks

### Manual Testing
- Human-readable format
- Copy-paste friendly
- Well-organized for selective testing

## 📈 Statistics

| Metric | Value |
|--------|-------|
| Total Payloads | 1,836 |
| Payload Files | 11 |
| Documentation Files | 4 |
| Supported Platforms | Windows, Linux, Unix, macOS |
| Injection Operators | 7+ (`;`, `|`, `||`, `&`, `&&`, `` ` ``, `$()`) |
| Testing Techniques | Direct, Time-based, OOB, Error-based |

## 🛡️ Security & Ethics

### Important Notice
This repository is created exclusively for:
- **Authorized security testing**
- **Educational purposes**
- **Security research**
- **Defensive security improvements**

### Prohibited Uses
- Unauthorized system access
- Malicious attacks
- Illegal activities
- Privacy violations
- Any unethical behavior

### Legal Compliance
Users must:
- Obtain written authorization before testing
- Comply with all applicable laws
- Follow responsible disclosure practices
- Respect system owners and data privacy

## 🎯 Key Features

✅ **Comprehensive Coverage**: 1,836+ tested payloads  
✅ **Well-Organized**: 11 categorized payload files  
✅ **Platform-Specific**: Separate Windows and Linux payloads  
✅ **Bypass Techniques**: Advanced filter evasion methods  
✅ **Detection Methods**: Direct, time-based, and OOB  
✅ **Tool-Ready**: Compatible with Burp Suite, ZAP, and custom tools  
✅ **Documentation**: Complete guides and cheat sheets  
✅ **Open Source**: MIT License for community use  
✅ **Maintained**: Active development and updates  
✅ **Ethical**: Clear guidelines and responsible use policy  

## 📚 Documentation

- **README.md**: Main documentation with usage instructions
- **CHEAT_SHEET.md**: Quick reference guide for common techniques
- **CONTRIBUTING.md**: Guidelines for contributing to the project
- **SUMMARY.md**: This comprehensive overview

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/payload-box/command-injection-payload-list.git

# Navigate to payload directory
cd command-injection-payload-list/Intruder

# Use with Burp Suite Intruder or your preferred tool
# Load the appropriate payload file for your test case
```

## 🤝 Community

- **Contributors Welcome**: See CONTRIBUTING.md
- **Issue Tracking**: GitHub Issues for bugs and features
- **Continuous Improvement**: Regular updates and additions
- **Community-Driven**: Built for and by security professionals

## 📄 License

MIT License - Free for personal and commercial use with attribution.

## 🙏 Acknowledgments

This project builds upon the knowledge and research of:
- OWASP Testing Guide contributors
- PortSwigger Web Security Academy
- HackTricks community
- PayloadsAllTheThings project
- Global security research community

---

**Version**: 1.0  
**Last Updated**: 2024  
**Maintained by**: payload-box organization  
**Status**: ✅ Active Development

**Remember**: With great power comes great responsibility. Use ethically! 🛡️