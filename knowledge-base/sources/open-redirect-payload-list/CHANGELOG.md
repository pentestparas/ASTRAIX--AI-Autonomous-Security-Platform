# Changelog

All notable changes to the Open Redirect Payload List project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional bypass techniques for WAF evasion
- Integration with popular security testing frameworks
- Web interface for payload testing
- Mobile app payload variations
- Cloud platform specific payloads

---

## [1.0.0] - 2024-01-15

### Added
- Initial release of Open Redirect Payload List
- **400+ comprehensive payloads** covering various bypass techniques
- Main payload file (`payloads.txt`) ready for Burp Suite Intruder
- Professional README with extensive documentation
- Python testing script (`scripts/test_open_redirect.py`)
  - Multi-threaded payload testing
  - Automatic vulnerability detection
  - JSON output support
  - Colored terminal output
- Bash testing script (`scripts/quick_test.sh`)
  - Fast command-line testing
  - Progress tracking
  - Results export
- Vulnerable PHP examples (`examples/vulnerable.php`)
  - 7 different vulnerability patterns
  - Educational demonstrations
  - Secure coding examples
- Contributing guidelines (`CONTRIBUTING.md`)
- MIT License

### Payload Categories
- Protocol-based redirects (`//evil.com`, `https://evil.com`)
- URL encoding variations (`%2F%2F`, `%5C%5C`)
- Backslash tricks (`\/\/`, `\evil.com`)
- @ symbol abuse (`@evil.com`, domain confusion)
- Hash and semicolon bypasses (`#@evil.com`, `;@evil.com`)
- Parameter pollution techniques
- JavaScript & Data URI schemes
- Unicode and alternative characters
- IP address variants (decimal, hex, IPv6)
- Double encoding techniques
- Whitespace and null byte variations
- Port specification bypasses
- Path traversal combinations

### Documentation
- Comprehensive README with:
  - Installation instructions
  - Usage examples for multiple tools
  - Payload categorization
  - Prevention best practices
  - Security recommendations
- Detailed contribution guidelines
- Code examples in multiple languages
- Testing methodology documentation

### Tools & Scripts
- Python script features:
  - Concurrent testing with configurable threads
  - Custom parameter specification
  - Timeout configuration
  - Verbose mode for debugging
  - Result export to JSON
- Bash script features:
  - Lightweight and fast
  - No external dependencies (only curl)
  - Real-time progress updates
  - Simple text output

### Testing
- Tested against common web frameworks:
  - PHP applications
  - Node.js/Express
  - Python/Django
  - Ruby on Rails
  - Java/Spring
- Verified compatibility with:
  - Burp Suite Professional/Community
  - OWASP ZAP
  - FFuf
  - curl

---

## Version History

### [1.0.0] - 2024-01-15
- Initial public release

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute payloads, improvements, or bug fixes.

## Reporting Issues

Found a bug or have a suggestion? Please open an issue on our [GitHub Issues](https://github.com/payload-box/open-redirect-payload-list/issues) page.

---

## Legend

- **Added**: New features, payloads, or documentation
- **Changed**: Changes to existing functionality
- **Deprecated**: Features that will be removed in future versions
- **Removed**: Removed features or payloads
- **Fixed**: Bug fixes
- **Security**: Security-related changes

---

**Note**: For detailed information about each payload and technique, please refer to the [README.md](README.md) file.