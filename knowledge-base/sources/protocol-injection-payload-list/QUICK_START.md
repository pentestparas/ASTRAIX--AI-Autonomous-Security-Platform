# Quick Start Guide

Get started with Protocol Injection Payload List in 5 minutes!

## 🚀 Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/payload-box/protocol-injection-payload-list.git
cd protocol-injection-payload-list
```

### 2. Browse Available Payloads

```bash
ls Intruder/
```

You'll see:
- `http-injection.txt` - HTTP protocol injection
- `smtp-injection.txt` - Email injection
- `ldap-injection.txt` - LDAP injection
- `sql-injection.txt` - SQL injection
- `xpath-injection.txt` - XPath injection
- `ssrf-injection.txt` - SSRF payloads
- `command-injection.txt` - Command injection
- `xxe-injection.txt` - XXE injection

## 💻 Using with Burp Suite

### Step 1: Configure Intruder

1. Send a request to Burp Intruder (Right-click → Send to Intruder)
2. Go to **Intruder** tab
3. Click **Positions** and mark injection points with `§`

Example:
```
GET /search?q=§test§ HTTP/1.1
Host: target.com
```

### Step 2: Load Payloads

1. Go to **Payloads** tab
2. Payload type: **Simple list**
3. Click **Load...**
4. Select a payload file from `Intruder/` directory
5. Click **Start attack**

### Step 3: Analyze Results

Look for:
- Different response lengths
- Error messages
- Time delays
- HTTP status code changes

## 🎯 Common Use Cases

### SQL Injection Testing

```bash
# Load SQL injection payloads
Burp Intruder → Payloads → Load → sql-injection.txt
```

Test parameter:
```
https://target.com/product?id=§1§
```

### Command Injection Testing

```bash
# Load command injection payloads
Burp Intruder → Payloads → Load → command-injection.txt
```

Test parameter:
```
https://target.com/ping?host=§127.0.0.1§
```

### XSS Testing

Test in various contexts:
- URL parameters: `?search=§test§`
- Form inputs: `username=§admin§`
- Headers: `User-Agent: §Mozilla§`

## 🔧 Using with Command Line Tools

### ffuf (Fast Web Fuzzer)

```bash
# SQL injection fuzzing
ffuf -u https://target.com/api?id=FUZZ \
     -w Intruder/sql-injection.txt \
     -mc all -fc 404

# Command injection fuzzing
ffuf -u https://target.com/exec?cmd=FUZZ \
     -w Intruder/command-injection.txt \
     -t 10
```

### wfuzz

```bash
# HTTP header injection
wfuzz -c -z file,Intruder/http-injection.txt \
      -H "X-Custom: FUZZ" \
      https://target.com/

# SSRF testing
wfuzz -c -z file,Intruder/ssrf-injection.txt \
      https://target.com/fetch?url=FUZZ
```

### curl with loop

```bash
# Test each payload
while IFS= read -r payload; do
    if [[ ! $payload =~ ^# ]] && [[ -n $payload ]]; then
        curl -s "https://target.com/search?q=${payload}" \
             -o /dev/null -w "Payload: ${payload} | Status: %{http_code}\n"
    fi
done < Intruder/sql-injection.txt
```

## 🐍 Python Script Example

```python
import requests
from urllib.parse import quote

# Load payloads
with open('Intruder/sql-injection.txt', 'r') as f:
    payloads = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Test endpoint
url = "https://target.com/api"

for payload in payloads:
    try:
        response = requests.get(f"{url}?id={quote(payload)}", timeout=5)
        
        # Check for SQL errors
        sql_errors = ['mysql', 'syntax', 'postgresql', 'oracle', 'sql']
        if any(error in response.text.lower() for error in sql_errors):
            print(f"[!] Potential SQL injection: {payload[:50]}")
            print(f"    Status: {response.status_code}")
            
    except Exception as e:
        print(f"[x] Error with payload: {payload[:30]}... - {e}")
```

## 🎯 Quick Testing Checklist

### Before You Start
- [ ] Get written authorization
- [ ] Identify scope and boundaries
- [ ] Set up logging
- [ ] Use VPN/proxy if required
- [ ] Configure rate limiting

### During Testing
- [ ] Start with passive reconnaissance
- [ ] Begin with least invasive payloads
- [ ] Monitor application behavior
- [ ] Document all findings
- [ ] Take screenshots/evidence

### After Testing
- [ ] Verify all findings
- [ ] Clean up test artifacts
- [ ] Prepare detailed report
- [ ] Follow responsible disclosure
- [ ] Store evidence securely

## 💡 Pro Tips

### 1. Filter Out Comments

```bash
# Remove comments and empty lines
grep -v '^#' Intruder/sql-injection.txt | grep -v '^$' > clean-payloads.txt
```

### 2. Combine Multiple Payload Lists

```bash
# Merge SQL and command injection
cat Intruder/sql-injection.txt Intruder/command-injection.txt > combined.txt
```

### 3. Extract Specific Payload Types

```bash
# Get only UNION-based SQL injection
grep -i "union" Intruder/sql-injection.txt > union-payloads.txt

# Get time-based blind payloads
grep -i "sleep\|waitfor" Intruder/sql-injection.txt > time-based.txt
```

### 4. Random Payload Selection

```bash
# Pick 10 random payloads for quick test
shuf -n 10 Intruder/sql-injection.txt
```

### 5. URL Encode Payloads

```bash
# Encode payloads for URL parameters
while read line; do
    echo "$line" | jq -sRr @uri
done < Intruder/sql-injection.txt
```

## 🔍 Identifying Vulnerabilities

### SQL Injection Indicators

- Database error messages
- Different response times (5+ seconds for SLEEP)
- Changes in response content
- Boolean-based differences (true/false responses)

### Command Injection Indicators

- OS command output in response
- Time delays (sleep/ping commands)
- DNS lookups to your domain
- HTTP requests to your server

### SSRF Indicators

- Internal IP address disclosure
- Cloud metadata in response
- Different response for valid/invalid internal hosts
- Timing differences

### XXE Indicators

- File contents in response
- External DTD fetched (check your logs)
- SSRF to internal services
- Error messages with file paths

## 🚨 Troubleshooting

### Payloads Not Working?

1. **Check encoding**: Some applications expect different encoding
2. **WAF blocking**: Try obfuscation techniques
3. **Context matters**: Adjust payload to injection point
4. **Rate limiting**: Slow down your requests
5. **Session handling**: Ensure valid session cookies

### Common Issues

**Issue**: All requests return 403 Forbidden
- **Solution**: You're likely blocked by WAF. Try fewer requests, use proxies, or different payloads

**Issue**: No error messages displayed
- **Solution**: Try blind injection techniques (time-based, boolean-based)

**Issue**: Application crashes
- **Solution**: Immediately stop testing and report to the owner

## 📚 Next Steps

1. **Read Full Documentation**: Check [README.md](README.md) for detailed info
2. **Learn Injection Techniques**: Visit [PortSwigger Academy](https://portswigger.net/web-security)
3. **Practice Safely**: Use [DVWA](http://www.dvwa.co.uk/) or [WebGoat](https://owasp.org/www-project-webgoat/)
4. **Contribute**: Found new payloads? See [CONTRIBUTING.md](CONTRIBUTING.md)
5. **Stay Updated**: Watch repository for new payloads

## ⚖️ Legal Reminder

```
⚠️  ALWAYS obtain explicit written permission before testing
⚠️  NEVER test systems you don't own or lack authorization for
⚠️  COMPLY with all applicable laws and regulations
⚠️  FOLLOW responsible disclosure practices
```

## 📞 Need Help?

- **Documentation**: Read [README.md](README.md)
- **Issues**: Check GitHub issues
- **Questions**: Open a discussion
- **Security**: See [SECURITY.md](SECURITY.md)

---

**Ready to start testing? Remember: Authorization first, testing second!**

Happy hunting! 🎯