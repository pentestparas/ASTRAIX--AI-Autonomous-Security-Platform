# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional NoSQL injection payloads (MongoDB, CouchDB)
- Template injection payloads (SSTI)
- GraphQL injection payloads
- JWT manipulation payloads
- API-specific injection vectors
- Payload effectiveness tracking
- Automated testing scripts

## [1.0.0] - 2024-01-15

### Added

#### Payload Collections
- **HTTP Protocol Injection** (166 payloads)
  - CRLF injection variants (URL encoded, Unicode, double encoded)
  - HTTP request smuggling (CL.TE, TE.CL, TE.TE)
  - Header injection techniques
  - Response splitting attacks
  - Cache poisoning vectors
  - Transfer-Encoding obfuscation
  - Protocol downgrade attacks
  - WebSocket upgrade injection

- **SMTP Protocol Injection** (233 payloads)
  - Email header injection (Bcc, Cc, From, Subject)
  - SMTP command injection
  - MIME header manipulation
  - Mail relay exploitation
  - SPF/DKIM bypass attempts
  - Attachment injection
  - Auto-reply manipulation
  - Mail loop creation

- **LDAP Injection** (315 payloads)
  - Authentication bypass techniques
  - Boolean-based blind injection
  - Filter manipulation (OR, AND, NOT logic)
  - Wildcard attacks
  - Attribute enumeration
  - Active Directory specific payloads
  - Group membership testing
  - Distinguished Name injection

- **SQL Injection** (346 payloads)
  - Authentication bypass
  - Union-based injection
  - Boolean-based blind injection
  - Time-based blind injection
  - Error-based injection
  - Stacked queries
  - Database enumeration (MySQL, PostgreSQL, MSSQL, Oracle, SQLite)
  - WAF bypass techniques
  - Second-order injection
  - Polyglot payloads

- **XPath Injection** (332 payloads)
  - Authentication bypass
  - Boolean-based injection
  - Blind injection techniques
  - Node traversal
  - Function-based injection
  - String manipulation
  - Encoding bypass methods
  - Error-based injection
  - Out-of-band data extraction

- **SSRF Injection** (447 payloads)
  - Localhost and loopback variations
  - Cloud metadata endpoints (AWS, GCP, Azure, Digital Ocean, Oracle, Alibaba)
  - Private network ranges (Class A, B, C)
  - Alternative IP representations (decimal, octal, hexadecimal, mixed)
  - Protocol wrappers (file, gopher, dict, ldap, ftp, tftp, sftp)
  - URL parser bypass techniques
  - DNS rebinding payloads
  - Port scanning payloads
  - Service-specific endpoints (Redis, MongoDB, Elasticsearch, Docker, Kubernetes)

- **Command Injection** (539 payloads)
  - Command separators and chaining (Unix/Linux and Windows)
  - Shell command substitution (backticks, $())
  - Reverse shell payloads (Bash, Netcat, Python, Perl, PHP, Ruby, Node.js)
  - Filter bypass techniques
  - Obfuscation methods (encoding, concatenation, wildcards)
  - Data exfiltration (DNS, HTTP)
  - Space bypass techniques
  - Alternative execution methods

- **XXE Injection** (223 payloads)
  - Basic file disclosure (Linux and Windows)
  - PHP wrapper exploitation
  - Blind out-of-band XXE
  - Error-based data exfiltration
  - XXE via file uploads (SVG, DOCX, XLSX, RSS, Sitemap)
  - DoS attacks (Billion Laughs, Quadratic Blowup)
  - XInclude attacks
  - Multiple protocol exploitation
  - Local DTD exploitation

#### Documentation
- Comprehensive README.md with detailed usage instructions
- CONTRIBUTING.md with contribution guidelines
- SECURITY.md with responsible disclosure policy
- QUICK_START.md for rapid deployment
- LICENSE file (MIT License)
- Inline comments for all payload categories
- Usage examples for multiple tools (Burp Suite, ffuf, wfuzz, curl)

#### Features
- Organized payload structure in Intruder/ directory
- Compatible with Burp Suite Intruder
- Plain text format for universal tool compatibility
- UTF-8 encoding for international character support
- Commented payloads for context and learning
- Categorized by protocol and attack type
- Ready-to-use with popular security testing tools

#### Testing Support
- Python script examples
- Command-line tool integration examples
- Burp Suite configuration guidance
- Bash scripting examples
- Payload filtering and manipulation examples

### Documentation Improvements
- Added detailed vulnerability type descriptions
- Included 2,600+ total payloads across 8 categories
- Provided testing tool compatibility list
- Added legal disclaimer and responsible use guidelines
- Included learning resources and references
- Added contribution recognition framework

### Repository Structure
- Created organized directory structure
- Implemented clear naming conventions
- Added comprehensive metadata
- Established version control practices

## [0.1.0] - 2024-01-01

### Added
- Initial repository setup
- Basic project structure
- MIT License
- Initial README

---

## Legend

- `Added` - New features or payloads
- `Changed` - Changes to existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security-related changes

## Links

- [Repository](https://github.com/payload-box/protocol-injection-payload-list)
- [Issues](https://github.com/payload-box/protocol-injection-payload-list/issues)
- [Pull Requests](https://github.com/payload-box/protocol-injection-payload-list/pulls)

## Notes

### Version Numbering

- **Major version** (X.0.0) - Incompatible changes, major restructuring
- **Minor version** (0.X.0) - New payloads, backward-compatible features
- **Patch version** (0.0.X) - Bug fixes, documentation updates

### Contribution

To contribute to this changelog:
1. Add your changes under the [Unreleased] section
2. Follow the existing format and categories
3. Include payload counts if adding new payloads
4. Reference issue/PR numbers where applicable

---

**Last Updated**: 2024-01-15