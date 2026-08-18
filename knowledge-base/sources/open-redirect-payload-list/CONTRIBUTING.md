# Contributing to Open Redirect Payload List

Thank you for your interest in contributing to the Open Redirect Payload List! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Contribution Guidelines](#contribution-guidelines)
- [Payload Submission Guidelines](#payload-submission-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Style Guide](#style-guide)

---

## Code of Conduct

By participating in this project, you agree to maintain a respectful and professional environment. We are committed to providing a welcoming and inclusive experience for everyone.

### Our Standards

- Be respectful and considerate
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members
- Use welcoming and inclusive language

---

## How Can I Contribute?

There are several ways you can contribute to this project:

### 1. **Submit New Payloads**
- Discover and submit new Open Redirect payloads
- Contribute bypass techniques
- Add encoding variations

### 2. **Improve Documentation**
- Fix typos or clarify existing documentation
- Add usage examples
- Translate documentation
- Write tutorials or guides

### 3. **Report Issues**
- Report bugs in scripts or tools
- Suggest enhancements
- Report invalid or outdated payloads

### 4. **Improve Testing Tools**
- Enhance existing scripts
- Fix bugs in automation tools
- Add new features

### 5. **Share Knowledge**
- Write blog posts or articles
- Create video tutorials
- Share your testing experiences

---

## Getting Started

### Fork and Clone

1. **Fork the repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/open-redirect-payload-list.git
   cd open-redirect-payload-list
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/payload-box/open-redirect-payload-list.git
   ```

### Keep Your Fork Updated

Before making changes, sync your fork with the upstream repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

---

## Contribution Guidelines

### General Guidelines

1. **One payload per line** in `payloads.txt`
2. **No duplicates** - Check if the payload already exists
3. **Test your payloads** before submitting
4. **Provide context** - Explain why the payload is useful
5. **Follow the format** - Maintain consistency with existing payloads
6. **Be ethical** - Only contribute legitimate security research

### What We Accept

✅ **Accepted Contributions:**
- New and unique Open Redirect payloads
- Bypass techniques for common filters
- Encoding variations (URL encoding, Unicode, etc.)
- Well-tested payloads with proof of concept
- Improvements to existing tools and scripts
- Documentation improvements
- Bug fixes

❌ **Not Accepted:**
- Duplicate payloads
- Malicious code or actual exploits
- Untested payloads
- Spam or irrelevant content
- Payloads specific to a single application (unless widely applicable)

---

## Payload Submission Guidelines

### Before Submitting

1. **Research**: Ensure your payload is unique
2. **Test**: Verify the payload works in real-world scenarios
3. **Document**: If the payload requires special conditions, document them
4. **Categorize**: Consider which category your payload belongs to

### Payload Quality Checklist

- [ ] Payload is unique and not already in the list
- [ ] Payload has been tested successfully
- [ ] Payload follows URL encoding standards
- [ ] Payload is generalized (not application-specific)
- [ ] Payload description/comment is clear (if needed)
- [ ] No trailing whitespace or special characters

### Payload Format

**Basic Format:**
```
//evil.com
https://evil.com
```

**With Comments (for complex payloads):**
```
# Description of technique or bypass method
//evil.com%E3%80%82com
```

### Categories to Consider

When adding payloads, consider these categories:
- Protocol-based redirects
- URL encoding variations
- Backslash tricks
- @ symbol abuse
- Hash and semicolon bypasses
- Parameter pollution
- JavaScript & Data URIs
- Unicode and alternative characters
- IP address variants
- Double encoding techniques

---

## Pull Request Process

### 1. Create a Branch

Create a descriptive branch name:

```bash
git checkout -b add-unicode-payloads
```

or

```bash
git checkout -b fix-python-script-bug
```

### 2. Make Your Changes

- Add your payloads to `payloads.txt`
- Update documentation if needed
- Test your changes

### 3. Commit Your Changes

Write clear and descriptive commit messages:

```bash
git add payloads.txt
git commit -m "Add Unicode bypass payloads for domain validation"
```

**Good Commit Messages:**
- ✅ "Add 15 new double-encoded bypass payloads"
- ✅ "Fix timeout issue in Python testing script"
- ✅ "Update README with new usage examples"

**Bad Commit Messages:**
- ❌ "Update file"
- ❌ "Fixed stuff"
- ❌ "Changes"

### 4. Push to Your Fork

```bash
git push origin add-unicode-payloads
```

### 5. Submit a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template with:
   - **Title**: Clear and descriptive
   - **Description**: What you changed and why
   - **Testing**: How you tested your changes
   - **Screenshots**: If applicable

### 6. Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] New payloads
- [ ] Bug fix
- [ ] Documentation update
- [ ] New feature
- [ ] Script improvement

## Payloads Added
Number of payloads: X
Categories:
- Category 1
- Category 2

## Testing
Describe how you tested these payloads:
- Tested against: [application/tool name]
- Results: [successful bypasses, etc.]

## Checklist
- [ ] I have tested my changes
- [ ] My changes follow the project style guidelines
- [ ] I have updated documentation accordingly
- [ ] No duplicate payloads
- [ ] All tests pass
```

### 7. Review Process

- Maintainers will review your PR
- You may receive feedback or change requests
- Make requested changes and push to the same branch
- Once approved, your PR will be merged

---

## Reporting Issues

### Before Opening an Issue

1. **Search existing issues** to avoid duplicates
2. **Verify the problem** - Make sure it's reproducible
3. **Gather information** - Collect relevant details

### Issue Types

#### Bug Report

```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happened

**Environment:**
- OS: [e.g., Windows 10, macOS 12]
- Tool: [e.g., Burp Suite, Python script]
- Version: [e.g., 1.0.0]

**Additional Context:**
Any other relevant information
```

#### Feature Request

```markdown
**Problem:**
What problem does this feature solve?

**Proposed Solution:**
How should it work?

**Alternatives Considered:**
What other solutions did you consider?

**Additional Context:**
Any other relevant information
```

#### Payload Suggestion

```markdown
**Payload:**
```
//example.payload
```

**Technique:**
Describe the bypass technique

**Tested On:**
Where have you successfully used this?

**References:**
Links to related research or documentation
```

---

## Style Guide

### Payload File (`payloads.txt`)

- One payload per line
- No trailing whitespace
- No empty lines between payloads
- Comments start with `#` (sparingly used)
- Keep payloads sorted by category when possible

### Python Code

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def test_payload(url, payload):
    """Test a single payload against a URL"""
    response = requests.get(url)
    return response.status_code

# Bad
def testPayload(URL,payload):
    Response=requests.get(URL)
    return Response.status_code
```

### Shell Scripts

```bash
# Good
test_payload() {
    local url="$1"
    local payload="$2"
    curl -s "$url?redirect=$payload"
}

# Bad
testpayload(){
URL=$1
PAYLOAD=$2
curl -s $URL?redirect=$PAYLOAD
}
```

### Markdown

- Use proper heading hierarchy
- Include code blocks with language specification
- Keep lines under 100 characters when possible
- Use lists for multiple items
- Include examples where helpful

---

## Recognition

Contributors will be recognized in several ways:

- Listed in the project's contributors section
- Mentioned in release notes for significant contributions
- GitHub's automatic contributor tracking

---

## Questions?

If you have questions about contributing:

1. Check the [README](README.md) first
2. Search [existing issues](https://github.com/payload-box/open-redirect-payload-list/issues)
3. Open a new issue with the `question` label

---

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

## Thank You!

Thank you for taking the time to contribute! Every contribution, no matter how small, helps make this project better for the security community.

**Happy Contributing! 🚀**