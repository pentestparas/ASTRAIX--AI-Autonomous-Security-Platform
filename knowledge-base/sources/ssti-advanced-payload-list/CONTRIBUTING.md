# Contributing Guide

First of all, thank you for considering contributing to this project! 🎉

This guide will help you understand how to contribute to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Adding Payloads](#adding-payloads)
- [Bug Reporting](#bug-reporting)
- [Feature Requests](#feature-requests)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)

## 📜 Code of Conduct

This project is governed by a code of conduct. By contributing, you agree to follow these rules.

### Core Principles

- Be respectful and professional
- Provide constructive criticism
- Accept different perspectives
- Think community-oriented
- Stay within ethical and legal boundaries

## 🤝 How Can I Contribute?

There are many ways to contribute:

### 1. Adding New Payloads
- If you've discovered new SSTI payloads
- If you've developed variations of existing payloads
- If you've found bypass techniques

### 2. Documentation
- README improvements
- New usage examples
- Translation contributions
- Typo corrections

### 3. Bug Fixes
- Reporting non-working payloads
- Template engine compatibility issues
- Format corrections

### 4. New Features
- New template engine support
- Automated test scripts
- Tool integrations

## 🎯 Adding Payloads

### Prerequisites

Before adding a payload:

1. **Test It**: Make sure the payload actually works
2. **Research**: Check if a similar payload already exists
3. **Document**: Explain what the payload does

### Payload Criteria

✅ **Acceptable Payloads:**
- Tested and verified
- Optimized for a specific template engine
- Clear and understandable
- Unique or significantly contributing to existing payloads
- Within ethical boundaries

❌ **Unacceptable Payloads:**
- Untested or non-working
- Exact copy of existing payloads
- Harmful or destructive (data deletion, system damage, etc.)
- Contains malicious code
- Exceeds legal boundaries

### Steps to Add Payloads

1. **Choose the Correct File**
   ```
   Intruder/jinja2-flask.txt    → Jinja2/Flask payloads
   Intruder/twig.txt            → Twig payloads
   Intruder/thymeleaf.txt       → Thymeleaf payloads
   Intruder/polyglot.txt        → Multi-engine payloads
   ```

2. **Payload Format**
   - Each payload should be on a single line
   - No leading/trailing whitespace
   - If URL encoding is needed for special characters, specify
   - No comment lines (payload only)

3. **Example Payload Addition**
   ```
   # WRONG ❌
   {{config}}  # Configuration object
   
   # CORRECT ✅
   {{config}}
   ```

4. **Add Test Scenario** (Optional)
   
   If your payload requires a special scenario, add a test scenario in the `examples/` folder:
   
   ```
   examples/jinja2-custom-filter.md
   ```

### Payload Test Checklist

- [ ] Payload was tested in a lab/test environment
- [ ] Payload produced expected result
- [ ] Similar payload has not been added before
- [ ] Added to correct category file
- [ ] Syntax is correct and error-free

## 🐛 Bug Reporting

### Creating a Bug Report

1. Go to **Issues** tab
2. Click **New Issue** button
3. Select appropriate template

### Bug Report Template

```markdown
**Bug Description**
A clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click '....'
3. See '....'

**Expected Behavior**
What did you expect to happen?

**Actual Behavior**
What actually happened?

**Payload**
Which payload did you encounter this with?

**Template Engine**
- Engine: [e.g. Jinja2]
- Version: [e.g. 3.1.2]
- Framework: [e.g. Flask 2.0]

**Screenshots**
Add if available.

**Additional Information**
Other important details.
```

## 💡 Feature Requests

### Creating a Feature Request

```markdown
**Feature Request**
Describe what the feature is.

**Motivation**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives**
Other solutions you've considered?

**Additional Context**
Relevant links, references, examples.
```

## 🔄 Pull Request Process

### 1. Fork and Clone

```bash
# Fork the project (from GitHub web interface)

# Clone your fork
git clone https://github.com/YOUR-USERNAME/ssti-advanced-payload-list.git
cd ssti-advanced-payload-list

# Add upstream
git remote add upstream https://github.com/payload-box/ssti-advanced-payload-list.git
```

### 2. Creating a Branch

```bash
# Create a new branch
git checkout -b feature/amazing-payloads

# or
git checkout -b fix/broken-payload

# or
git checkout -b docs/update-readme
```

**Branch Naming Conventions:**
- `feature/` - For new features
- `fix/` - For bug fixes
- `docs/` - For documentation
- `refactor/` - For code improvements

### 3. Making Changes

```bash
# Edit files
nano Intruder/jinja2-flask.txt

# Stage changes
git add Intruder/jinja2-flask.txt

# Commit
git commit -m "feat: add advanced Jinja2 RCE payloads"
```

### 4. Push and PR

```bash
# Push branch
git push origin feature/amazing-payloads

# Create Pull Request on GitHub
```

### PR Checklist

Before creating a Pull Request:

- [ ] Code works and has been tested
- [ ] Commit messages are clear and meaningful
- [ ] README updated (if needed)
- [ ] No conflicts
- [ ] Branch is up to date (`git pull upstream main`)

### PR Description Template

```markdown
## Changes

What changed in this PR?

## Motivation

Why were these changes made?

## Testing

How was it tested?

## Checklist

- [ ] Changes have been tested
- [ ] Documentation updated
- [ ] Commit messages are proper
- [ ] No conflicts

## Related Issue

Closes #123
```

## 📝 Coding Standards

### Payload Format

```
# Single line, clean format
{{lipsum.__globals__['os'].popen('id').read()}}

# For complex payloads, maintain readability
{%for c in [].__class__.__base__.__subclasses__()%}{%if c.__name__=='catch_warnings'%}{{c.__init__.__globals__['__builtins__'].__import__('os').popen('id').read()}}{%endif%}{%endfor%}
```

### File Organization

```
Intruder/
├── jinja2-flask.txt       # For Jinja2/Flask
├── twig.txt               # For Twig
├── thymeleaf.txt          # For Thymeleaf
├── freemarker.txt         # For FreeMarker
├── velocity.txt           # For Velocity
├── smarty.txt             # For Smarty
├── erb-ruby.txt           # For ERB/Ruby
├── pug-jade.txt           # For Pug/Jade
├── ejs.txt                # For EJS
├── polyglot.txt           # Polyglot payloads
└── all-payloads.txt       # All payloads
```

### Comments and Documentation

Do not use comment lines in payload files. Explanations should be in README.

## 💬 Commit Messages

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code improvement
- `test`: Adding tests
- `chore`: Other changes

### Examples

```bash
# Good examples ✅
git commit -m "feat(jinja2): add bypass payloads for WAF"
git commit -m "fix(twig): correct system command execution payload"
git commit -m "docs(readme): update installation instructions"
git commit -m "feat(polyglot): add cross-platform RCE payloads"

# Bad examples ❌
git commit -m "update"
git commit -m "fix stuff"
git commit -m "added new payloads"
```

### Detailed Commit Message

```bash
git commit -m "feat(thymeleaf): add ProcessBuilder exploitation payloads

- Added 15 new payloads using ProcessBuilder
- Included Windows-specific command execution
- Added bypass techniques for input validation

Closes #45"
```

## 🧪 Testing

### Payload Test Environment

To test payloads:

1. **Use Docker** (Recommended)
   ```bash
   docker run -it vulnerables/web-dvwa
   ```

2. **Local Lab Environment**
   - DVWA
   - bWAPP
   - WebGoat
   - Juice Shop

3. **Online Labs**
   - PortSwigger Academy
   - HackTheBox
   - TryHackMe

### Test Checklist

- [ ] Payload tested on correct template engine
- [ ] Expected result obtained
- [ ] No side effects
- [ ] Tested on different versions (if possible)

## 📞 Contact

For questions:

- **Issues**: For general questions and discussions
- **Email**: Contact maintainer for private matters
- **Discussions**: GitHub Discussions for community discussions

## 🎓 Resources

Useful resources for contributing:

- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## 📜 License

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE).

---

## 🙏 Thank You

Thank you for taking the time to consider contributing to this project!

Every contribution, no matter how small, is valuable. 💖

---

**Happy Hacking! 🔥**

*Stay Legal • Stay Ethical • Stay Secure*