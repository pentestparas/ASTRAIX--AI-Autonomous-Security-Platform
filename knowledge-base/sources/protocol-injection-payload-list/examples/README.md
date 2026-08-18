# Examples Directory

This directory contains example scripts demonstrating how to use the protocol injection payloads from this repository for authorized security testing.

## 📋 Available Examples

### 1. Python SQL Injection Tester
**File:** `test_sql_injection.py`

A comprehensive Python script for testing SQL injection vulnerabilities using payloads from this repository.

**Features:**
- Loads payloads from repository files
- Automated testing with configurable delays
- SQL error pattern detection
- Detailed logging and reporting
- Authorization confirmation
- Progress tracking

**Requirements:**
```bash
pip install requests
```

**Usage:**
```bash
# Basic usage
python test_sql_injection.py -u https://target.com/search -p q

# With custom settings
python test_sql_injection.py \
    -u https://target.com/api \
    -p id \
    -f ../Intruder/sql-injection.txt \
    -d 1.0 \
    -m 100 \
    -o report.txt

# Show help
python test_sql_injection.py --help
```

**Arguments:**
- `-u, --url` - Target URL (required)
- `-p, --param` - Parameter name to test (required)
- `-f, --file` - Payload file path (default: ../Intruder/sql-injection.txt)
- `-d, --delay` - Delay between requests in seconds (default: 0.5)
- `-m, --max-payloads` - Maximum payloads to test (default: all)
- `-o, --output` - Output report file (default: sql_injection_report.txt)
- `--skip-auth-check` - Skip authorization confirmation (use with caution)

### 2. Bash Command Injection Tester
**File:** `test_command_injection.sh`

A Bash script for testing command injection vulnerabilities using repository payloads.

**Features:**
- URL encoding support
- Command execution indicator detection
- Progress tracking
- Detailed reporting
- Authorization confirmation
- Colored terminal output

**Requirements:**
- bash 4.0+
- curl
- grep, sed, awk
- jq or python3 (for URL encoding)

**Usage:**
```bash
# Make script executable
chmod +x test_command_injection.sh

# Basic usage
./test_command_injection.sh -u "https://target.com/ping" -p "host"

# With custom settings
./test_command_injection.sh \
    -u "https://target.com/exec" \
    -p "cmd" \
    -f ../Intruder/command-injection.txt \
    -d 1.0 \
    -m 50 \
    -o results

# Show help
./test_command_injection.sh --help
```

**Arguments:**
- `-u, --url` - Target URL (required)
- `-p, --param` - Parameter name to test (required)
- `-f, --file` - Payload file path (default: ../Intruder/command-injection.txt)
- `-d, --delay` - Delay between requests (default: 0.5)
- `-m, --max` - Maximum payloads to test (default: all)
- `-o, --output` - Output directory (default: test_results)
- `--skip-auth` - Skip authorization check (use with caution)

## 🚀 Quick Start

### Python Example

```bash
# Clone the repository
git clone https://github.com/payload-box/protocol-injection-payload-list.git
cd protocol-injection-payload-list/examples

# Install dependencies
pip install requests

# Run test (with authorization)
python test_sql_injection.py \
    -u "http://testphp.vulnweb.com/artists.php" \
    -p "artist" \
    -m 50
```

### Bash Example

```bash
# Navigate to examples directory
cd protocol-injection-payload-list/examples

# Make script executable
chmod +x test_command_injection.sh

# Run test (with authorization)
./test_command_injection.sh \
    -u "http://target.local/ping" \
    -p "ip" \
    -m 50
```

## 📖 Understanding the Scripts

### Script Workflow

Both scripts follow a similar workflow:

1. **Argument Parsing** - Parse command-line arguments
2. **Authorization Check** - Confirm user has permission to test
3. **Payload Loading** - Load payloads from repository files
4. **Testing Loop** - Test each payload against the target
5. **Detection** - Look for vulnerability indicators
6. **Reporting** - Generate detailed reports
7. **Summary** - Display test results

### Detection Methods

**SQL Injection (Python Script):**
- Database error message detection
- Response length analysis
- Status code monitoring
- Time-based detection (for time-based payloads)

**Command Injection (Bash Script):**
- Command output indicators (uid=, gid=, groups=)
- System information disclosure
- File system paths
- Directory listings

## 🛠️ Customization

### Modifying Detection Patterns

**Python - SQL Injection:**
```python
# Edit the error_patterns list in SQLInjectionTester class
self.error_patterns = [
    'mysql', 'sql syntax', 'mysqli',
    'postgresql', 'pg_query',
    # Add your custom patterns here
    'custom_error_pattern'
]
```

**Bash - Command Injection:**
```bash
# Edit the indicators array in check_command_indicators function
local indicators=(
    "uid="
    "gid="
    # Add your custom indicators here
    "custom_indicator"
)
```

### Adding New Features

You can extend these scripts with:
- Cookie handling
- Custom headers
- Authentication support
- Proxy configuration
- Multiple injection points
- Advanced reporting formats
- Integration with other tools

## 📊 Output Files

### Python Script Outputs

**Log File:** `sql_injection_test.log`
- Timestamped events
- Test progress
- Errors and warnings
- Summary statistics

**Report File:** `sql_injection_report.txt`
- Test configuration
- Vulnerable payloads
- Error types found
- Recommendations

### Bash Script Outputs

**Log File:** `test_results/command_injection_test.log`
- Detailed testing log
- Timestamps
- Payload results

**Report File:** `test_results/command_injection_report.txt`
- Vulnerability findings
- Response previews
- Status codes
- Time taken per payload

## ⚠️ Important Warnings

### Legal Considerations

```
⚠️  THESE SCRIPTS ARE FOR AUTHORIZED TESTING ONLY ⚠️

You MUST have explicit written permission before testing any system.
Unauthorized testing is ILLEGAL and may result in:
  • Criminal prosecution
  • Civil liability
  • Imprisonment
  • Fines

Always:
  ✓ Obtain written authorization
  ✓ Define scope and boundaries
  ✓ Follow responsible disclosure
  ✓ Document all activities
  ✓ Comply with all laws
```

### Technical Considerations

- **Rate Limiting:** Use appropriate delays to avoid overwhelming servers
- **False Positives:** Verify all findings manually
- **Log Everything:** Maintain detailed logs of all testing
- **Clean Up:** Remove any test artifacts after testing
- **Be Careful:** These scripts can cause service disruption if misused

## 🎓 Educational Use

These examples are designed to help you:

1. **Learn** - Understand how payload testing works
2. **Practice** - Test in safe, controlled environments
3. **Develop** - Create your own custom testing tools
4. **Automate** - Build efficient security testing workflows

### Recommended Practice Environments

- [DVWA](http://www.dvwa.co.uk/) - Damn Vulnerable Web Application
- [WebGoat](https://owasp.org/www-project-webgoat/) - OWASP WebGoat
- [bWAPP](http://www.itsecgames.com/) - buggy Web Application
- [Juice Shop](https://owasp.org/www-project-juice-shop/) - OWASP Juice Shop
- [VulnHub](https://www.vulnhub.com/) - Vulnerable VMs
- [HackTheBox](https://www.hackthebox.eu/) - Penetration testing labs

## 🔧 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'requests'`
```bash
# Solution: Install Python requests library
pip install requests
```

**Issue:** `Permission denied` when running bash script
```bash
# Solution: Make script executable
chmod +x test_command_injection.sh
```

**Issue:** Payloads not loading
```bash
# Solution: Check payload file path
# Ensure you're in the examples directory or adjust the path
python test_sql_injection.py -u URL -p PARAM -f ../Intruder/sql-injection.txt
```

**Issue:** All requests return errors
- Check your internet connection
- Verify the target URL is accessible
- Check if you're being blocked by WAF/firewall
- Reduce request rate with higher delay

## 📚 Additional Resources

### Documentation
- [Main README](../README.md) - Repository overview
- [Quick Start Guide](../QUICK_START.md) - Getting started
- [Contributing Guidelines](../CONTRIBUTING.md) - How to contribute

### Learning Resources
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger Academy](https://portswigger.net/web-security)
- [HackTricks](https://book.hacktricks.xyz/)

### Similar Tools
- [SQLmap](http://sqlmap.org/) - Automated SQL injection tool
- [Commix](https://github.com/commixproject/commix) - Command injection tool
- [NoSQLMap](https://github.com/codingo/NoSQLMap) - NoSQL injection tool

## 💡 Contributing

Have improvements or new examples?

1. Test your script thoroughly
2. Document usage clearly
3. Follow coding best practices
4. Include authorization checks
5. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## 📄 License

These example scripts are licensed under the MIT License, same as the main repository.

## 🤝 Support

- **Issues:** Report bugs via GitHub Issues
- **Discussions:** Ask questions in GitHub Discussions
- **Security:** See [SECURITY.md](../SECURITY.md) for security concerns

---

**Remember:** Always test ethically and legally! 🔒