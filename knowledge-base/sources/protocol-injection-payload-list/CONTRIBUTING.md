# Contributing to Protocol Injection Payload List

Thank you for your interest in contributing to this project! This guide will help you understand how to contribute effectively.

## 🎯 How to Contribute

There are several ways you can contribute to this project:

1. **Add new payloads** - Submit new injection payloads
2. **Improve existing payloads** - Enhance or optimize current payloads
3. **Fix errors** - Correct mistakes or outdated information
4. **Improve documentation** - Enhance README, guides, and comments
5. **Report issues** - Report bugs or suggest improvements

## 📝 Contribution Guidelines

### General Rules

- **Authorization Only**: All payloads must be intended for authorized security testing
- **Quality over Quantity**: Submit well-tested, unique payloads
- **Clear Documentation**: Include comments explaining payload purpose and usage
- **Ethical Use**: Ensure contributions align with ethical security practices

### Payload Guidelines

#### Format Requirements

1. **One payload per line**
2. **Use comments** starting with `#` for explanations
3. **Group related payloads** with descriptive comment headers
4. **No trailing whitespace**
5. **UTF-8 encoding**

#### Example Format

```
# Category Description
# Brief explanation of the payload type

# Basic Payload
payload_here

# Advanced Payload with encoding
%encoded%payload%here

# Payload with special characters
payload;with;separators
```

### File Structure

Payloads should be added to the appropriate file in the `Intruder/` directory:

- `http-injection.txt` - HTTP protocol injection
- `smtp-injection.txt` - SMTP/email injection
- `ldap-injection.txt` - LDAP injection
- `sql-injection.txt` - SQL injection
- `xpath-injection.txt` - XPath injection
- `ssrf-injection.txt` - SSRF payloads
- `command-injection.txt` - OS command injection
- `xxe-injection.txt` - XXE injection

### Testing Requirements

Before submitting payloads:

1. **Test in a controlled environment**
   - Use local test servers
   - Set up vulnerable applications (DVWA, WebGoat, etc.)
   - Never test on production systems without authorization

2. **Verify uniqueness**
   - Check if the payload already exists
   - Ensure it provides value over existing payloads

3. **Document behavior**
   - Note which systems/versions the payload works on
   - Document any special requirements or conditions

### Code of Conduct

- Be respectful and professional
- Provide constructive feedback
- Help others learn and improve
- Follow ethical security practices
- Respect intellectual property

## 🚀 Step-by-Step Contribution Process

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/protocol-injection-payload-list.git
cd protocol-injection-payload-list
```

### 3. Create a Branch

```bash
git checkout -b feature/add-new-payloads
```

Use descriptive branch names:
- `feature/add-xxe-payloads`
- `fix/sql-injection-typos`
- `docs/improve-readme`

### 4. Make Your Changes

#### Adding New Payloads

1. Open the appropriate file in the `Intruder/` directory
2. Add your payloads following the format guidelines
3. Include clear comments and descriptions

Example:

```
# New XSS Bypass Technique - 2024
# Bypasses modern WAFs using Unicode normalization
%u003Cscript%u003Ealert(1)%u003C/script%u003E

# Alternative encoding
\u003Cscript\u003Ealert(1)\u003C/script\u003E
```

#### Improving Documentation

- Update README.md with new information
- Add examples and use cases
- Improve clarity and readability

### 5. Test Your Changes

1. **Validate formatting**
   ```bash
   # Check for trailing whitespace
   grep -n '[[:space:]]$' Intruder/*.txt
   
   # Check file encoding
   file -i Intruder/*.txt
   ```

2. **Test payloads** in your controlled environment

3. **Review for duplicates**
   ```bash
   # Check for duplicate lines
   sort Intruder/sql-injection.txt | uniq -d
   ```

### 6. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add Intruder/sql-injection.txt
git commit -m "Add SQL injection payloads for PostgreSQL JSON operators

- Add JSON operator injection payloads
- Include error-based injection variants
- Add bypass techniques for parameterized queries"
```

#### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature or payloads
- `fix`: Bug fix or correction
- `docs`: Documentation changes
- `style`: Formatting changes
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

### 7. Push to Your Fork

```bash
git push origin feature/add-new-payloads
```

### 8. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Fill in the PR template with:
   - Clear title describing the change
   - Detailed description of what was added/changed
   - Testing performed
   - Any special considerations

#### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New payloads
- [ ] Bug fix
- [ ] Documentation update
- [ ] Payload improvement

## Payload Category
- [ ] HTTP Injection
- [ ] SMTP Injection
- [ ] LDAP Injection
- [ ] SQL Injection
- [ ] XPath Injection
- [ ] SSRF
- [ ] Command Injection
- [ ] XXE

## Testing
Describe testing performed:
- Environment used
- Results obtained
- Systems tested against

## Checklist
- [ ] Payloads are unique
- [ ] Format guidelines followed
- [ ] Comments included
- [ ] Tested in controlled environment
- [ ] No trailing whitespace
- [ ] Appropriate file updated
```

## 🔍 Review Process

### What We Look For

1. **Effectiveness** - Does the payload work as intended?
2. **Uniqueness** - Is it different from existing payloads?
3. **Documentation** - Are comments clear and helpful?
4. **Format** - Does it follow style guidelines?
5. **Safety** - Is it appropriate for ethical testing?

### Review Timeline

- Initial review: 3-7 days
- Feedback provided for improvements
- Merged after approval

### Feedback and Revisions

- Address reviewer comments promptly
- Make requested changes in your branch
- Push updates to your PR branch

## 🎓 Learning Resources

### Testing Environments

- [DVWA](http://www.dvwa.co.uk/) - Damn Vulnerable Web Application
- [WebGoat](https://owasp.org/www-project-webgoat/) - OWASP WebGoat
- [bWAPP](http://www.itsecgames.com/) - buggy Web Application
- [HackTheBox](https://www.hackthebox.eu/) - Penetration testing labs
- [TryHackMe](https://tryhackme.com/) - Security learning platform

### Payload Development

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger Academy](https://portswigger.net/web-security)
- [HackTricks](https://book.hacktricks.xyz/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

## 🐛 Reporting Issues

### Bug Reports

Include:
- Description of the issue
- Expected behavior
- Actual behavior
- Steps to reproduce
- Environment details

### Payload Issues

If a payload doesn't work:
- Describe the target system
- Share error messages
- Suggest improvements or alternatives

## 💡 Suggestions

Have ideas for improvement?
- Open an issue describing your suggestion
- Explain the benefit and use case
- Provide examples if applicable

## ❓ Questions

Need help?
- Open a discussion on GitHub
- Check existing issues for answers
- Review documentation

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

All contributors will be recognized in the project. Significant contributions may be highlighted in release notes.

---

Thank you for helping make this project better! Your contributions help the security community stay safer.