# Testing Scripts

This directory contains automated testing scripts for detecting Open Redirect vulnerabilities.

## Available Scripts

### 1. Python Testing Script (`test_open_redirect.py`)

A comprehensive, multi-threaded Python script for automated Open Redirect vulnerability detection.

#### Features

- ✅ Multi-threaded concurrent testing
- ✅ Custom parameter specification
- ✅ Configurable timeout and thread count
- ✅ Colored terminal output
- ✅ JSON export for results
- ✅ Verbose debugging mode
- ✅ Automatic vulnerability detection

#### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

#### Usage

**Basic Usage:**
```bash
python test_open_redirect.py -u https://example.com/redirect
```

**With Custom Parameters:**
```bash
python test_open_redirect.py -u https://example.com/redirect -p url,next,return
```

**With Output File:**
```bash
python test_open_redirect.py -u https://example.com/redirect -o results.json
```

**With Custom Settings:**
```bash
python test_open_redirect.py -u https://example.com/redirect -t 20 --timeout 10 -v
```

#### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-u, --url` | Target URL to test (required) | - |
| `-f, --file` | Payloads file path | `../payloads.txt` |
| `-p, --params` | Comma-separated parameter list | `url,redirect,next,return,returnTo,redir,redirect_uri` |
| `-t, --threads` | Number of concurrent threads | `10` |
| `--timeout` | Request timeout in seconds | `5` |
| `-o, --output` | Output file for results (JSON) | - |
| `-v, --verbose` | Enable verbose output | `False` |

#### Examples

**Test with multiple parameters:**
```bash
python test_open_redirect.py \
  -u "https://example.com/auth/callback" \
  -p "redirect_uri,return_url,next,continue" \
  -t 15
```

**Test with verbose output and save results:**
```bash
python test_open_redirect.py \
  -u "https://example.com/redirect" \
  -v \
  -o vulnerability_report.json
```

**Test with increased timeout:**
```bash
python test_open_redirect.py \
  -u "https://slow-site.com/redirect" \
  --timeout 15 \
  -t 5
```

---

### 2. Bash Quick Testing Script (`quick_test.sh`)

A lightweight, fast Bash script for quick Open Redirect testing without external dependencies.

#### Features

- ✅ Fast and lightweight
- ✅ No Python dependencies (only curl required)
- ✅ Real-time progress updates
- ✅ Simple text output
- ✅ Easy to integrate with other tools

#### Installation

```bash
# Make the script executable
chmod +x quick_test.sh
```

#### Usage

**Basic Usage:**
```bash
./quick_test.sh -u https://example.com/redirect
```

**With Custom Parameter:**
```bash
./quick_test.sh -u https://example.com/redirect -p next
```

**With Output File:**
```bash
./quick_test.sh -u https://example.com/redirect -o results.txt
```

**With Verbose Mode:**
```bash
./quick_test.sh -u https://example.com/redirect -v
```

#### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-u, --url` | Target URL to test (required) | - |
| `-p, --param` | Parameter name to test | `url` |
| `-f, --file` | Payloads file path | `../payloads.txt` |
| `-t, --timeout` | Request timeout in seconds | `5` |
| `-o, --output` | Output file for results | - |
| `-v, --verbose` | Enable verbose output | `False` |
| `-h, --help` | Show help message | - |

#### Examples

**Test OAuth redirect_uri parameter:**
```bash
./quick_test.sh \
  -u "https://example.com/oauth/authorize" \
  -p "redirect_uri"
```

**Test with custom timeout and save results:**
```bash
./quick_test.sh \
  -u "https://example.com/redirect" \
  -t 10 \
  -o scan_results.txt
```

**Verbose testing:**
```bash
./quick_test.sh \
  -u "https://example.com/redirect" \
  -p "next" \
  -v
```

---

## Comparison

| Feature | Python Script | Bash Script |
|---------|--------------|-------------|
| **Speed** | Fast (multi-threaded) | Fast (sequential) |
| **Dependencies** | Python + requests | curl only |
| **Output Format** | JSON + colored text | Plain text |
| **Concurrency** | Yes (configurable) | No |
| **Cross-platform** | Yes | Unix/Linux/macOS |
| **Resource Usage** | Medium | Low |
| **Best For** | Comprehensive testing | Quick checks |

---

## Requirements

### Python Script Requirements

- Python 3.6 or higher
- `requests` library
- `urllib3` library
- `colorama` library (for colored output)

Install all requirements:
```bash
pip install -r requirements.txt
```

### Bash Script Requirements

- Bash shell
- `curl` command-line tool

Check if curl is installed:
```bash
curl --version
```

---

## Output Examples

### Python Script Output

```
============================================================
    Open Redirect Vulnerability Scanner
============================================================
[*] Target URL: https://example.com/redirect
[*] Parameters: url, redirect, next
[*] Threads: 10
[*] Timeout: 5s

[+] Loaded 411 payloads
[+] Total test cases: 1233
[+] Starting scan...

[VULNERABLE] https://example.com/redirect?url=//evil.com
[REDIRECT TO] //evil.com

[*] Progress: 50/1233
[*] Progress: 100/1233

============================================================
    Scan Results
============================================================

[!] Found 3 potential vulnerabilities:

Vulnerability #1:
  URL: https://example.com/redirect?url=//evil.com
  Parameter: url
  Payload: //evil.com
  Status Code: 302
  Redirect To: //evil.com
  Timestamp: 2024-01-15T10:30:45.123456

[+] Results saved to results.json
```

### Bash Script Output

```
==========================================
  Quick Open Redirect Testing Script
==========================================

[*] Target URL: https://example.com/redirect
[*] Parameter: url
[*] Payloads: 411
[*] Timeout: 5s

[+] Starting test...

[VULNERABLE] https://example.com/redirect?url=//evil.com
[REDIRECT TO] //evil.com

[*] Progress: 50/411
[*] Progress: 100/411

==========================================
  Scan Results
==========================================

[*] Total payloads tested: 411
[!] Potential vulnerabilities found: 3
[+] Results saved to: results.txt
```

---

## Tips for Effective Testing

### 1. Start with Single Parameter
Test one parameter at a time to identify vulnerable endpoints:
```bash
python test_open_redirect.py -u "https://example.com/redirect" -p "url"
```

### 2. Use Verbose Mode for Debugging
Enable verbose mode to see all tested payloads:
```bash
python test_open_redirect.py -u "https://example.com/redirect" -v
```

### 3. Adjust Thread Count
For rate-limited sites, reduce threads:
```bash
python test_open_redirect.py -u "https://example.com/redirect" -t 3
```

### 4. Increase Timeout for Slow Sites
If you're getting many timeouts:
```bash
python test_open_redirect.py -u "https://slow-site.com/redirect" --timeout 15
```

### 5. Export Results for Reporting
Always save results for documentation:
```bash
python test_open_redirect.py -u "https://example.com/redirect" -o report.json
```

### 6. Test Multiple Parameters
Test all common redirect parameters:
```bash
python test_open_redirect.py \
  -u "https://example.com/redirect" \
  -p "url,redirect,next,return,returnTo,redir,redirect_uri,continue,destination,return_to"
```

---

## Troubleshooting

### Python Script Issues

**Issue: ModuleNotFoundError**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: SSL Certificate Errors**
```bash
# The script automatically disables SSL verification warnings
# If you still have issues, update requests library:
pip install --upgrade requests urllib3
```

**Issue: Too Many Timeouts**
```bash
# Increase timeout and reduce threads:
python test_open_redirect.py -u "URL" --timeout 15 -t 3
```

### Bash Script Issues

**Issue: curl: command not found**
```bash
# Install curl
# On Ubuntu/Debian:
sudo apt-get install curl

# On macOS:
brew install curl
```

**Issue: Permission Denied**
```bash
# Make script executable:
chmod +x quick_test.sh
```

**Issue: Slow Performance**
```bash
# Reduce payloads or increase timeout:
./quick_test.sh -u "URL" -t 10
```

---

## Integration with Other Tools

### Burp Suite Integration

Use scripts to identify vulnerable parameters, then test manually with Burp:

1. Run script to find vulnerable endpoints
2. Configure Burp to intercept requests
3. Use Intruder with `payloads.txt` for detailed testing

### CI/CD Integration

Add to your security testing pipeline:

```yaml
# Example GitHub Actions workflow
- name: Test for Open Redirects
  run: |
    python scripts/test_open_redirect.py \
      -u "$TARGET_URL" \
      -o security-report.json
```

### OWASP ZAP Integration

Use script findings to configure ZAP active scan:

```bash
# Find vulnerabilities first
python test_open_redirect.py -u "https://example.com" -o findings.json

# Then configure ZAP based on findings
```

---

## Best Practices

1. **Always Get Permission**: Only test applications you're authorized to test
2. **Respect Rate Limits**: Use appropriate thread counts and timeouts
3. **Document Findings**: Always export results for proper reporting
4. **Test Responsibly**: Don't overwhelm target servers
5. **Verify Results**: Manually verify automated findings
6. **Use Safely**: Replace `evil.com` with your own test domain

---

## Contributing

Found a bug or want to improve these scripts? See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## License

These scripts are part of the Open Redirect Payload List project and are licensed under the MIT License.