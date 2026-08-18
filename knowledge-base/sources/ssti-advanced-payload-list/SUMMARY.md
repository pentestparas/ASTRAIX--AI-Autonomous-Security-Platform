# SSTI Advanced Payload List - Project Summary

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Total Payloads** | 2,198+ |
| **Template Engines** | 10+ |
| **Payload Files** | 11 |
| **Categories** | 6 |
| **Languages Covered** | Python, PHP, Java, Ruby, JavaScript |
| **Last Updated** | 2024 |
| **License** | MIT |

---

## 📁 Repository Structure

```
ssti-advanced-payload-list/
├── README.md                    # Main documentation (English)
├── CONTRIBUTING.md              # Contribution guidelines (English)
├── LICENSE                      # MIT License
├── SUMMARY.md                   # This file
├── .gitignore                   # Git ignore rules
│
├── Intruder/                    # Burp Suite Intruder payloads
│   ├── jinja2-flask.txt        # 132 payloads - Python/Jinja2
│   ├── twig.txt                # 158 payloads - PHP/Twig
│   ├── smarty.txt              # 238 payloads - PHP/Smarty
│   ├── thymeleaf.txt           # 164 payloads - Java/Thymeleaf
│   ├── freemarker.txt          # 161 payloads - Java/FreeMarker
│   ├── velocity.txt            # 269 payloads - Java/Velocity
│   ├── erb-ruby.txt            # 184 payloads - Ruby/ERB
│   ├── pug-jade.txt            # 226 payloads - JavaScript/Pug
│   ├── ejs.txt                 # 200 payloads - JavaScript/EJS
│   ├── polyglot.txt            # 171 payloads - Multi-engine
│   └── all-payloads.txt        # 295 payloads - All engines
│
└── Payloads/                    # Additional payload resources
```

---

## 🎯 Payload Distribution

### By Template Engine

| Template Engine | File | Payload Count | Language |
|----------------|------|---------------|----------|
| Velocity | velocity.txt | 269 | Java |
| Smarty | smarty.txt | 238 | PHP |
| Pug/Jade | pug-jade.txt | 226 | JavaScript |
| EJS | ejs.txt | 200 | JavaScript |
| ERB | erb-ruby.txt | 184 | Ruby |
| Polyglot | polyglot.txt | 171 | Multi |
| Thymeleaf | thymeleaf.txt | 164 | Java |
| FreeMarker | freemarker.txt | 161 | Java |
| Twig | twig.txt | 158 | PHP |
| Jinja2 | jinja2-flask.txt | 132 | Python |
| All-in-One | all-payloads.txt | 295 | Mixed |

### By Category

- **Detection Payloads**: ~200 payloads
- **Information Gathering**: ~350 payloads
- **File Read**: ~400 payloads
- **Remote Code Execution (RCE)**: ~800 payloads
- **WAF Bypass**: ~250 payloads
- **Polyglot/Cross-platform**: ~198 payloads

---

## 🚀 Quick Start Guide

### For Penetration Testers

1. **Identify the template engine** used by target application
2. **Select appropriate payload file** from `Intruder/` directory
3. **Load into Burp Suite Intruder** or your preferred tool
4. **Start testing** vulnerable parameters
5. **Analyze responses** for successful exploitation

### For Security Researchers

1. Clone repository: `git clone https://github.com/payload-box/ssti-advanced-payload-list.git`
2. Browse payload files in `Intruder/` directory
3. Use payloads for security research and testing
4. Contribute new findings back to the project

### For Developers

1. Review payloads to understand SSTI attack vectors
2. Implement proper input validation and sanitization
3. Use template engines securely
4. Test your applications against these payloads

---

## 🎨 Supported Template Engines

### Python-Based
- ✅ **Jinja2** (Flask, Django) - 132 payloads
  - RCE via `__globals__`
  - File read operations
  - Filter bypass techniques

### PHP-Based
- ✅ **Twig** (Symfony) - 158 payloads
  - System command execution
  - Filter abuse
  - File manipulation
  
- ✅ **Smarty** - 238 payloads
  - PHP code execution via `{php}` tags
  - Function callbacks
  - Variable manipulation

### Java-Based
- ✅ **Thymeleaf** (Spring Boot) - 164 payloads
  - `Runtime.exec()` exploitation
  - `ProcessBuilder` techniques
  - Expression language injection
  
- ✅ **FreeMarker** - 161 payloads
  - `Execute` utility exploitation
  - `ObjectConstructor` abuse
  - Jython runtime execution
  
- ✅ **Velocity** (Apache) - 269 payloads
  - ClassLoader manipulation
  - Reflection-based RCE
  - Method invocation

### Ruby-Based
- ✅ **ERB** (Ruby on Rails) - 184 payloads
  - System command execution
  - File I/O operations
  - Eval-based techniques

### JavaScript-Based
- ✅ **Pug/Jade** (Node.js) - 226 payloads
  - `child_process` exploitation
  - `require()` abuse
  - Process manipulation
  
- ✅ **EJS** (Express.js) - 200 payloads
  - Template string injection
  - Module loading
  - File system access

### Multi-Engine
- ✅ **Polyglot** - 171 payloads
  - Cross-platform compatibility
  - Multiple engine support
  - Universal detection payloads

---

## 📚 Payload Categories

### 1. Detection Payloads
Basic mathematical operations to detect SSTI:
- `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`, `{7*7}`
- Template-specific syntax testing
- Error-based detection

### 2. Information Gathering
System and application information disclosure:
- Configuration objects
- Environment variables
- System properties
- Module/package information

### 3. File Read
Reading sensitive files:
- `/etc/passwd`
- Configuration files
- Application source code
- Flag files (CTF)

### 4. Remote Code Execution (RCE)
Executing arbitrary commands:
- Command execution (`id`, `whoami`, `ls`)
- Reverse shells
- File uploads
- Privilege escalation

### 5. WAF Bypass
Techniques to bypass security filters:
- Unicode encoding
- Hex encoding
- Filter evasion
- Obfuscation techniques

### 6. Polyglot Payloads
Work across multiple template engines:
- Universal detection
- Cross-platform exploitation
- Framework-agnostic techniques

---

## 🔧 Tool Integration

### Burp Suite
- Load payloads into Intruder
- Use with Repeater for manual testing
- Integrate with Scanner for automation

### OWASP ZAP
- Import payloads as fuzzing lists
- Use in active scan
- Custom script integration

### Custom Scripts
- Python automation
- Bash one-liners
- PowerShell scripts
- API testing frameworks

---

## 🎓 Use Cases

### Penetration Testing
- Web application security assessments
- Vulnerability discovery
- Exploitation and proof-of-concept
- Security report generation

### Bug Bounty Hunting
- Finding SSTI vulnerabilities
- Crafting exploitation chains
- Responsible disclosure
- Bounty maximization

### Security Research
- Template engine analysis
- New payload development
- Bypass technique research
- CVE discovery

### Education and Training
- Learning SSTI concepts
- Hands-on practice
- CTF competitions
- Security awareness

---

## ⚠️ Important Notes

### Legal and Ethical Use
- **Only test systems you own or have permission to test**
- Obtain written authorization before testing
- Follow responsible disclosure practices
- Respect local laws and regulations

### Testing Best Practices
- Test in isolated environments first
- Back up target systems
- Document findings thoroughly
- Report vulnerabilities responsibly

### Security Considerations
- Keep payloads updated
- Test in safe environments
- Understand impact before execution
- Follow ethical hacking principles

---

## 📈 Project Metrics

### Payload Coverage
- **Detection**: ████████████████░░░░ 80%
- **Information Gathering**: ███████████████░░░░░ 75%
- **File Operations**: ██████████████████░░ 90%
- **Code Execution**: ███████████████████░ 95%
- **Bypass Techniques**: ████████████░░░░░░░░ 60%
- **Multi-Engine**: ███████████████░░░░░ 75%

### Template Engine Coverage
- **Python**: ████████████████████ 100%
- **PHP**: ████████████████████ 100%
- **Java**: ████████████████████ 100%
- **Ruby**: ████████████████████ 100%
- **JavaScript**: ████████████████████ 100%

---

## 🔗 Quick Links

- **GitHub Repository**: https://github.com/payload-box/ssti-advanced-payload-list
- **Issues**: https://github.com/payload-box/ssti-advanced-payload-list/issues
- **Pull Requests**: https://github.com/payload-box/ssti-advanced-payload-list/pulls
- **Discussions**: https://github.com/payload-box/ssti-advanced-payload-list/discussions

---

## 📝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Ways to Contribute
- Add new payloads
- Improve documentation
- Report bugs
- Add template engine support
- Share bypass techniques
- Translate documentation

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Thanks to the security research community, penetration testers, bug bounty hunters, and all contributors who make this project possible.

---

**Last Updated**: 2024
**Maintained By**: Payload Box Community
**Status**: ✅ Active Development

---

*Stay Legal • Stay Ethical • Stay Secure* 🔒