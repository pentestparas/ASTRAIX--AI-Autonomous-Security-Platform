# Contributing to XXE Injection Payload List

Thank you for your interest in contributing to the XXE Injection Payload List! This document provides guidelines for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Payload Submission Guidelines](#payload-submission-guidelines)
- [Pull Request Process](#pull-request-process)
- [Payload Quality Standards](#payload-quality-standards)
- [Testing Requirements](#testing-requirements)
- [Style Guide](#style-guide)

## Code of Conduct

### Our Pledge

This repository is dedicated to **authorized security testing and educational purposes only**. By contributing, you agree that:

- All payloads are for **legitimate security testing** with proper authorization
- You will **not** use or encourage the use of these payloads for malicious purposes
- You will follow **responsible disclosure** practices
- You respect the **ethical hacking** community standards

### Expected Behavior

- Be respectful and professional
- Provide constructive feedback
- Accept constructive criticism gracefully
- Focus on what is best for the security community
- Show empathy towards other contributors

## How Can I Contribute?

### Reporting Bugs

If you find an issue with existing payloads:

1. Check if the issue already exists in [Issues](../../issues)
2. If not, create a new issue with:
   - Clear title describing the problem
   - Detailed description of the issue
   - Steps to reproduce (if applicable)
   - Expected vs actual behavior
   - Environment details (if relevant)

### Suggesting Enhancements

We welcome suggestions for:

- New payload categories
- Improved documentation
- Better organization
- Additional examples
- Tool integrations

### Adding New Payloads

This is the most common contribution! See [Payload Submission Guidelines](#payload-submission-guidelines) below.

## Payload Submission Guidelines

### Before Submitting

1. **Verify the payload works** in a controlled test environment
2. **Check for duplicates** - ensure the payload isn't already in the repository
3. **Test compatibility** - verify the payload syntax is valid XML
4. **Document the purpose** - understand what the payload does

### Payload Categories

Add your payload to the appropriate file in the `Intruder/` directory:

| File | Purpose |
|------|---------|
| `xxe-basic.txt` | Simple, direct XXE payloads |
| `xxe-file-disclosure.txt` | File reading payloads |
| `xxe-blind-oob.txt` | Out-of-band/blind XXE |
| `xxe-ssrf.txt` | Server-Side Request Forgery |
| `xxe-dos.txt` | Denial of Service attacks |
| `xxe-error-based.txt` | Error-based exploitation |
| `xxe-xinclude.txt` | XInclude attacks |
| `xxe-svg.txt` | SVG file upload exploitation |
| `xxe-soap.txt` | SOAP protocol attacks |
| `xxe-parameter-entities.txt` | Parameter entity tricks |
| `xxe-php-wrappers.txt` | PHP wrapper protocols |
| `xxe-exotic-protocols.txt` | Uncommon protocol exploitation |
| `xxe-utf7-encoded.txt` | UTF-7 encoded payloads |
| `xxe-xml-bomb.txt` | XML bomb/billion laughs |
| `xxe-cloud-metadata.txt` | Cloud metadata SSRF |

If your payload doesn't fit any category, suggest a new one in your pull request.

### Payload Format

**One payload per line:**
```xml
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>
```

**No comments in payload files** - Comments can break Burp Suite Intruder imports.

**Use placeholders for customizable values:**
- `ATTACKER-SERVER.com` - Attacker's server
- `FILE_PATH` - Target file path
- `PORT` - Port numbers

### What Makes a Good Payload?

✅ **Good Payloads:**
- Valid XML syntax
- Clear purpose
- Tested and verified
- Properly categorized
- Uses standard placeholders
- No trailing whitespace

❌ **Avoid:**
- Broken/invalid XML
- Duplicate payloads
- Payloads with hardcoded IPs/domains
- Overly complex variations of existing payloads
- Malicious intent beyond testing

## Pull Request Process

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR-USERNAME/xxe-injection-payload-list.git
cd xxe-injection-payload-list
```

### 2. Create a Branch

```bash
git checkout -b add-new-payloads
```

Use descriptive branch names:
- `add-docx-xxe-payloads`
- `fix-soap-payload-syntax`
- `update-readme-examples`

### 3. Make Your Changes

- Add payloads to appropriate files
- Update documentation if needed
- Follow the style guide

### 4. Test Your Changes

- Verify XML syntax
- Check for duplicates
- Test in Burp Suite Intruder (if possible)
- Ensure files end with a newline

### 5. Commit Your Changes

```bash
git add .
git commit -m "Add DOCX XXE exploitation payloads"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues if applicable (#123)

Examples:
```
Add XXE payloads for DOCX file exploitation
Fix syntax error in SOAP XXE payloads
Update README with cloud metadata examples
Add example DTD files for blind XXE attacks
```

### 6. Push and Create Pull Request

```bash
git push origin add-new-payloads
```

Then create a pull request on GitHub with:

**Title:** Clear, concise description
```
Add 25 new XXE payloads for Office document exploitation
```

**Description:** Should include:
```markdown
## Description
Brief description of what you're adding/changing

## Type of Change
- [ ] New payloads
- [ ] Bug fix
- [ ] Documentation update
- [ ] New feature

## Payload Category
Which file(s) did you modify?

## Testing
- [ ] Payloads are valid XML
- [ ] Tested in controlled environment
- [ ] No duplicates
- [ ] Follows style guide

## Additional Notes
Any additional context or screenshots
```

### 7. Code Review

- Maintainers will review your PR
- Address any requested changes
- Be patient and responsive

## Payload Quality Standards

### Syntax Validation

All payloads must be valid XML. Test with:

```bash
# Using xmllint
echo 'YOUR_PAYLOAD' | xmllint --noout -

# Using Python
python3 -c "import xml.etree.ElementTree as ET; ET.fromstring('YOUR_PAYLOAD')"
```

### Testing Requirements

Before submitting, verify:

1. **XML is well-formed** - No syntax errors
2. **Payload is functional** - Test in a lab environment
3. **No duplicates** - Search existing payloads
4. **Proper categorization** - In the right file
5. **Placeholder usage** - Use standard placeholders

### Documentation Updates

If adding a new payload category or significant feature, update:

- `README.md` - Add to payload categories table
- `Examples/USAGE.md` - Add usage examples (optional)
- Category description (if creating new file)

## Style Guide

### File Naming

- Use lowercase with hyphens: `xxe-new-category.txt`
- Prefix with `xxe-`
- Use descriptive names

### Payload Structure

**Standard format:**
```xml
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "PROTOCOL://TARGET">]><foo>&xxe;</foo>
```

**Consistency:**
- Use double quotes for attributes
- Use `foo` as standard DOCTYPE name (unless specific to payload type)
- Use `xxe` as standard entity name
- Use `&xxe;` for entity reference

### Placeholder Standards

| Placeholder | Usage |
|------------|-------|
| `ATTACKER-SERVER.com` | Your callback server |
| `burpcollaborator.net` | Burp Collaborator (generic) |
| `FILE_PATH` | Generic file path |
| `PORT` | Port number |
| `YOUR-SERVER.com` | Alternative callback server |

### Line Endings

- Use LF (Unix) line endings
- One payload per line
- File must end with a newline character
- No trailing whitespace

### Encoding

- UTF-8 encoding
- No BOM (Byte Order Mark)

## Testing Checklist

Before submitting your PR, verify:

- [ ] All payloads use valid XML syntax
- [ ] Tested payloads in a safe, authorized environment
- [ ] No duplicate payloads
- [ ] Proper file categorization
- [ ] Standard placeholders used
- [ ] No trailing whitespace
- [ ] Files end with newline
- [ ] UTF-8 encoding
- [ ] LF line endings
- [ ] Updated documentation (if needed)
- [ ] Commit messages are clear
- [ ] PR description is complete

## Questions?

If you have questions or need help:

1. Check existing [Issues](../../issues)
2. Review the [README.md](README.md)
3. Read the [Usage Guide](Examples/USAGE.md)
4. Create a new issue with your question

## Recognition

Contributors will be recognized in:
- Git commit history
- GitHub contributors page
- Project documentation (for significant contributions)

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

**Thank you for contributing to the security community! 🙏**

Your contributions help security professionals identify and fix vulnerabilities, making the internet safer for everyone.