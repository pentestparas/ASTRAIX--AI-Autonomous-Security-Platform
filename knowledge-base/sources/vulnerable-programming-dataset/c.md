# Vulnerable Code Samples: C

Secure-code-review training examples (2 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — Buffer Overflow

- **Language**: C
- **Vulnerability**: Buffer Overflow
- **Description**: Unbounded string copy without size checking using strcpy.

```
#include <string.h>
void copy_string(char *input) {
    char buffer[16];
    strcpy(buffer, input);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Buffer_Overflow
- CWE-120: https://cwe.mitre.org/data/definitions/120.html

## Sample 2 — Buffer Overflow

- **Language**: C
- **Vulnerability**: Buffer Overflow
- **Description**: Unbounded string copy without size checking using strcpy.

```
#include <string.h>
void copy_string(char *input) {
    char buffer[16];
    strcpy(buffer, input);
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Buffer_Overflow
- CWE-120: https://cwe.mitre.org/data/definitions/120.html
