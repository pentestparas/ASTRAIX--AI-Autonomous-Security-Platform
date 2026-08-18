# Contributing to Command Injection Payload List

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Contribution Guidelines](#contribution-guidelines)
- [Payload Submission Standards](#payload-submission-standards)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [Testing Your Payloads](#testing-your-payloads)

## 📜 Code of Conduct

### Our Pledge

This project is dedicated to providing a harassment-free experience for everyone. We pledge to:

- Use welcoming and inclusive language
- Respect differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Our Standards

**Acceptable behavior:**
- Being respectful of differing opinions
- Providing constructive feedback
- Focusing on collaboration
- Demonstrating professionalism

**Unacceptable behavior:**
- Trolling or insulting comments
- Personal or political attacks
- Harassment of any kind
- Publishing others' private information
- Any conduct that could be considered inappropriate

## 🤝 How Can I Contribute?

### Reporting Issues

If you find a problem with existing payloads or documentation:

1. Check if the issue already exists in [GitHub Issues](https://github.com/payload-box/command-injection-payload-list/issues)
2. If not, create a new issue with:
   - Clear and descriptive title
   - Detailed description of the problem
   - Steps to reproduce (if applicable)
   - Expected vs actual behavior
   - Any relevant screenshots or logs

### Suggesting Enhancements

We welcome suggestions for new features or improvements:

1. Check existing issues and pull requests first
2. Create a new issue with the "enhancement" label
3. Provide:
   - Clear description of the enhancement
   - Use cases and examples
   - Potential implementation approach
   - Any relevant references or resources

### Contributing Payloads

We're always looking for new and effective payloads:

1. Fork the repository
2. Create a feature branch
3. Add your payloads following our standards
4. Test your payloads thoroughly
5. Submit a pull request

### Improving Documentation

Documentation improvements are highly valued:

- Fix typos or grammatical errors
- Improve clarity of existing documentation
- Add examples or explanations
- Update outdated information
- Translate documentation (future feature)

## 📝 Contribution Guidelines

### Before You Start

1. **Fork and Clone**: Fork the repository and clone it locally
2. **Create a Branch**: Use descriptive branch names
   ```bash
   git checkout -b feature/add-powershell-payloads
   git checkout -b fix/typo-in-readme
   git checkout -b docs/improve-usage-section
   ```
3. **Stay Updated**: Sync your fork regularly with the upstream repository

### General Guidelines

- **One feature per PR**: Keep pull requests focused on a single feature or fix
- **Test your changes**: Ensure all payloads are tested and functional
- **Update documentation**: If you add new payloads, update README.md
- **Follow existing patterns**: Match the style and format of existing files
- **Be ethical**: Only contribute payloads for legitimate security testing

## 🎯 Payload Submission Standards

### File Format

- **One payload per line**: Each line should contain a single payload
- **No blank lines**: Avoid empty lines between payloads
- **No comments**: Keep payload files clean (documentation goes in README)
- **UTF-8 encoding**: All files must use UTF-8 encoding
- **Unix line endings**: Use LF (\n) not CRLF (\r\n)

### Payload Requirements

1. **Functional**: Payloads must be tested and working
2. **Unique**: Avoid exact duplicates of existing payloads
3. **Documented**: Explain unusual or complex payloads in PR description
4. **Categorized**: Place payloads in the appropriate file
5. **Safe**: Avoid destructive commands in examples (no `rm -rf`, `format`, etc.)

### Naming Conventions

When creating new payload files:

- Use lowercase with hyphens: `command-injection-category.txt`
- Be descriptive: `command-injection-docker-escape.txt`
- Follow existing naming patterns

### Example Payload Submission

**Good submissions:**
```
; whoami
| id
&& cat /etc/passwd
; cat${IFS}/etc/hosts
```

**Bad submissions:**
```
; whoami       # Comment in payload file (don't do this)

; whoami       # Extra blank line above (avoid)
;whoami;id;pwd # Multiple commands in one line (split into separate lines)
; rm -rf /     # Destructive command (never include)
```

## 🔄 Pull Request Process

### 1. Prepare Your Changes

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# Add new payloads or make improvements

# Stage changes
git add Intruder/your-file.txt
git add README.md

# Commit with descriptive message
git commit -m "Add SQL injection in command parameters payloads"
```

### 2. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:

- **Clear title**: Describe what the PR does
- **Detailed description**: Explain the changes and their purpose
- **Testing information**: How you tested the payloads
- **Related issues**: Link any related issues

### 3. PR Template

```markdown
## Description
Brief description of changes made

## Type of Change
- [ ] New payloads
- [ ] Bug fix
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Payloads Added/Modified
- File: `command-injection-xxx.txt`
- Count: X new payloads
- Category: [Basic/Advanced/Platform-specific/etc.]

## Testing
- [ ] Tested payloads in a controlled environment
- [ ] Verified no duplicates exist
- [ ] Checked file formatting (one per line, UTF-8, LF)
- [ ] Updated documentation if needed

## Testing Environment
- OS: [e.g., Ubuntu 22.04, Windows 11]
- Target: [e.g., Custom vulnerable app, DVWA]
- Results: [Brief description of test results]

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] Any dependent changes have been merged

## Additional Notes
Any additional information, concerns, or questions
```

### 4. Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged
- Thank you for your contribution! 🎉

## 🎨 Style Guide

### File Organization

```
command-injection-payload-list/
├── Intruder/
│   ├── command-injection-basic.txt
│   ├── command-injection-advanced.txt
│   └── ...
├── README.md
├── CHEAT_SHEET.md
├── CONTRIBUTING.md
└── LICENSE
```

### Markdown Style

- Use ATX-style headers (`#`, `##`, `###`)
- Include emoji in headers for visual appeal (optional)
- Use code blocks with language specification
- Keep lines under 120 characters when possible
- Use relative links for internal references

### Code Examples

Always specify the language for code blocks:

```bash
# Good
echo "Hello, World!"
```

```python
# Good
print("Hello, World!")
```

### Commit Messages

Follow conventional commit format:

- `feat: Add new obfuscation techniques`
- `fix: Correct typo in README`
- `docs: Update installation instructions`
- `refactor: Reorganize Linux payloads`
- `test: Add validation scripts`
- `chore: Update dependencies`

## 🧪 Testing Your Payloads

### Setup Test Environment

1. **Use a VM or Container**: Never test on production systems
2. **Create Vulnerable Application**: Use existing vulnerable apps (DVWA, bWAPP) or create your own
3. **Document Results**: Keep notes on what works and what doesn't

### Testing Checklist

- [ ] Test in isolated environment only
- [ ] Verify payload executes intended command
- [ ] Check for false positives
- [ ] Test on multiple platforms (if applicable)
- [ ] Document any prerequisites or specific conditions
- [ ] Ensure no destructive operations

### Recommended Test Environments

- **DVWA** (Damn Vulnerable Web Application)
- **bWAPP** (Buggy Web Application)
- **WebGoat**
- **Custom Docker containers**
- **Local VMs with vulnerable applications**

### Example Test Script

```bash
#!/bin/bash
# Simple test script for command injection

PAYLOAD_FILE="Intruder/command-injection-basic.txt"
TEST_PARAM="127.0.0.1"

echo "Testing payloads from: $PAYLOAD_FILE"

while IFS= read -r payload; do
    echo "Testing: $payload"
    # Add your test logic here
    # Example: curl "http://localhost/vulnerable?ip=$TEST_PARAM$payload"
done < "$PAYLOAD_FILE"
```

## 🔒 Security and Ethics

### Responsible Disclosure

- Only test systems you own or have explicit permission to test
- Report vulnerabilities through proper channels
- Never use these payloads for malicious purposes
- Follow local laws and regulations

### What NOT to Contribute

- Destructive payloads (`rm -rf /`, `format C:`, etc.)
- Payloads designed to harm systems
- Malware or backdoors
- Real credentials or sensitive information
- Illegal content

### Ethical Guidelines

1. **Authorization**: Always get written permission before testing
2. **No Harm**: Avoid payloads that could cause damage
3. **Privacy**: Respect privacy and confidentiality
4. **Disclosure**: Follow responsible disclosure practices
5. **Education**: Use knowledge to improve security, not break it

## 📞 Getting Help

If you need help with your contribution:

- **GitHub Issues**: Ask questions in issues
- **Discussions**: Use GitHub Discussions for general questions
- **Documentation**: Check existing documentation first
- **Examples**: Look at merged PRs for examples

## 🏆 Recognition

Contributors will be:

- Listed in project acknowledgments
- Credited in relevant documentation
- Recognized in release notes

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Command Injection Payload List! Your efforts help make the security community stronger. 🛡️