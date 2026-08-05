# Vulnerable Code Samples: PHP

Secure-code-review training examples (61 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — File Inclusion

- **Language**: PHP
- **Vulnerability**: File Inclusion
- **Description**: Dynamic file inclusion based on unsanitized user input.

```
<?php
$page = $_GET['page'];
include($page);
?>
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- CWE-98: https://cwe.mitre.org/data/definitions/98.html

## Sample 2 — Session Fixation

- **Language**: PHP
- **Vulnerability**: Session Fixation
- **Description**: Not regenerating session ID after login.

```
<?php
session_start();
$_SESSION['user'] = $_GET['user'];
?>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Session_fixation
- CWE-384: https://cwe.mitre.org/data/definitions/384.html

## Sample 3 — Insecure File Upload

- **Language**: PHP
- **Vulnerability**: Insecure File Upload
- **Description**: Allowing file uploads without validation of file type or content.

```
<?php
move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $_FILES['file']['name']);
?>
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- CWE-434: https://cwe.mitre.org/data/definitions/434.html

## Sample 4 — Insecure Randomness

- **Language**: PHP
- **Vulnerability**: Insecure Randomness
- **Description**: Using mt_rand() for cryptographic purposes.

```
<?php
$token = mt_rand(1000, 9999);
echo $token;
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 5 — Insecure Serialization

- **Language**: PHP
- **Vulnerability**: Insecure Serialization
- **Description**: Unserializing untrusted data.

```
<?php
$data = unserialize($_POST['data']);
?>
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 6 — XSS

- **Language**: PHP
- **Vulnerability**: XSS
- **Description**: Echoing user input without escaping.

```
<?php
echo $_GET['input'];
?>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/xss/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 7 — Insecure Redirect

- **Language**: PHP
- **Vulnerability**: Insecure Redirect
- **Description**: Redirecting to user-controlled URL.

```
<?php
header('Location: ' . $_GET['url']);
?>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Unvalidated_Redirects_and_Forwards
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 8 — Insecure Password Storage

- **Language**: PHP
- **Vulnerability**: Insecure Password Storage
- **Description**: Storing passwords in plain text.

```
<?php
$password = $_POST['password'];
mysql_query("INSERT INTO users (password) VALUES ('$password')");
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-257: https://cwe.mitre.org/data/definitions/257.html

## Sample 9 — Insecure Session Handling

- **Language**: PHP
- **Vulnerability**: Insecure Session Handling
- **Description**: Using default session settings without security flags.

```
<?php
session_start();
$_SESSION['user_id'] = 123;
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 10 — Insecure Database Connection

- **Language**: PHP
- **Vulnerability**: Insecure Database Connection
- **Description**: Using unencrypted database connection.

```
<?php
$conn = new mysqli('localhost', 'user', 'pass', 'db');
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-311: https://cwe.mitre.org/data/definitions/311.html

## Sample 11 — Insecure Error Handling

- **Language**: PHP
- **Vulnerability**: Insecure Error Handling
- **Description**: Exposing sensitive information in error messages.

```
<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-209: https://cwe.mitre.org/data/definitions/209.html

## Sample 12 — File Inclusion

- **Language**: PHP
- **Vulnerability**: File Inclusion
- **Description**: Dynamic file inclusion based on unsanitized user input.

```
<?php
$page = $_GET['page'];
include($page);
?>
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- CWE-98: https://cwe.mitre.org/data/definitions/98.html

## Sample 13 — Session Fixation

- **Language**: PHP
- **Vulnerability**: Session Fixation
- **Description**: Not regenerating session ID after login.

```
<?php
session_start();
$_SESSION['user'] = $_GET['user'];
?>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Session_fixation
- CWE-384: https://cwe.mitre.org/data/definitions/384.html

## Sample 14 — Insecure File Upload

- **Language**: PHP
- **Vulnerability**: Insecure File Upload
- **Description**: Allowing file uploads without validation of file type or content.

```
<?php
move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $_FILES['file']['name']);
?>
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- CWE-434: https://cwe.mitre.org/data/definitions/434.html

## Sample 15 — Insecure Randomness

- **Language**: PHP
- **Vulnerability**: Insecure Randomness
- **Description**: Using mt_rand() for cryptographic purposes.

```
<?php
$token = mt_rand(1000, 9999);
echo $token;
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 16 — Insecure Serialization

- **Language**: PHP
- **Vulnerability**: Insecure Serialization
- **Description**: Unserializing untrusted data.

```
<?php
$data = unserialize($_POST['data']);
?>
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 17 — XSS

- **Language**: PHP
- **Vulnerability**: XSS
- **Description**: Echoing user input without escaping.

```
<?php
echo $_GET['input'];
?>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/xss/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 18 — Insecure Redirect

- **Language**: PHP
- **Vulnerability**: Insecure Redirect
- **Description**: Redirecting to user-controlled URL.

```
<?php
header('Location: ' . $_GET['url']);
?>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Unvalidated_Redirects_and_Forwards
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 19 — Insecure Password Storage

- **Language**: PHP
- **Vulnerability**: Insecure Password Storage
- **Description**: Storing passwords in plain text.

```
<?php
$password = $_POST['password'];
mysql_query("INSERT INTO users (password) VALUES ('$password')");
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-257: https://cwe.mitre.org/data/definitions/257.html

## Sample 20 — Insecure Session Handling

- **Language**: PHP
- **Vulnerability**: Insecure Session Handling
- **Description**: Using default session settings without security flags.

```
<?php
session_start();
$_SESSION['user_id'] = 123;
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 21 — Insecure Database Connection

- **Language**: PHP
- **Vulnerability**: Insecure Database Connection
- **Description**: Using unencrypted database connection.

```
<?php
$conn = new mysqli('localhost', 'user', 'pass', 'db');
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-311: https://cwe.mitre.org/data/definitions/311.html

## Sample 22 — Insecure Error Handling

- **Language**: PHP
- **Vulnerability**: Insecure Error Handling
- **Description**: Exposing sensitive information in error messages.

```
<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-209: https://cwe.mitre.org/data/definitions/209.html

## Sample 23 — Insecure API Endpoint

- **Language**: PHP
- **Vulnerability**: Insecure API Endpoint
- **Description**: Exposing sensitive data through unprotected API endpoint.

```
<?php
echo json_encode(['api_key' => 'secret123']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 24 — Insecure Dynamic Variable

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Variable
- **Description**: Using variable variables with unvalidated input.

```
<?php
$var = $_GET['var'];
$$var = 'value';
?>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Variable_and_Function_Injection
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 25 — Insecure Dynamic Include

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Include
- **Description**: Including files dynamically based on user input.

```
<?php
require $_GET['module'] . '.php';
?>
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- CWE-98: https://cwe.mitre.org/data/definitions/98.html

## Sample 26 — Logic Flaw in Password Reset

- **Language**: PHP
- **Vulnerability**: Logic Flaw in Password Reset
- **Description**: Allowing password reset without verifying user identity.

```
<?php
if (isset($_POST['email'])) {
    resetPassword($_POST['email']);
}
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-840: https://cwe.mitre.org/data/definitions/840.html

## Sample 27 — Insecure Dynamic Class Loading

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Class Loading
- **Description**: Instantiating classes dynamically based on user input.

```
<?php
$class = $_GET['class'];
$obj = new $class();
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 28 — Insecure Regex Evaluation

- **Language**: PHP
- **Vulnerability**: Insecure Regex Evaluation
- **Description**: Using user input in regex patterns, risking ReDoS.

```
<?php
preg_match($_GET['pattern'], 'data');
?>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 29 — Insecure Dynamic Function Call

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Function Call
- **Description**: Calling functions dynamically based on user input.

```
<?php
$func = $_GET['func'];
$func();
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 30 — Insecure Session Regeneration

- **Language**: PHP
- **Vulnerability**: Insecure Session Regeneration
- **Description**: Failing to regenerate session ID on privilege escalation.

```
<?php
session_start();
$_SESSION['role'] = 'admin';
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-384: https://cwe.mitre.org/data/definitions/384.html

## Sample 31 — Insecure Dynamic SQL Function

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic SQL Function
- **Description**: Calling SQL functions dynamically with user input.

```
<?php
mysql_query('CALL ' . $_GET['func'] . '()');
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 32 — Insecure Dynamic Property Setting

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Property Setting
- **Description**: Setting object properties dynamically with user input.

```
<?php
class User {
    public function set($key, $value) {
        $this->$key = $value;
    }
}
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 33 — Insecure Dynamic Table Creation

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Table Creation
- **Description**: Creating tables dynamically with user input.

```
<?php
mysql_query('CREATE TABLE ' . $_GET['table'] . ' (id INT)');
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 34 — Insecure Dynamic Config Setting

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Config Setting
- **Description**: Setting PHP configuration dynamically with user input.

```
<?php
ini_set($_GET['setting'], $_GET['value']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 35 — Insecure Dynamic Header Injection

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Header Injection
- **Description**: Setting HTTP headers with user input.

```
<?php
header($_GET['header']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-113: https://cwe.mitre.org/data/definitions/113.html

## Sample 36 — Insecure Dynamic Database Selection

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Database Selection
- **Description**: Selecting databases dynamically with user input.

```
<?php
mysqli_select_db($conn, $_GET['db']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 37 — Insecure Dynamic Object Instantiation

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Object Instantiation
- **Description**: Instantiating objects dynamically with user input.

```
<?php
$class = $_GET['class'];
new $class($_GET['arg']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 38 — Insecure Dynamic Error Reporting

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Error Reporting
- **Description**: Setting error reporting level with user input.

```
<?php
error_reporting($_GET['level']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-209: https://cwe.mitre.org/data/definitions/209.html

## Sample 39 — Insecure Dynamic File Inclusion

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic File Inclusion
- **Description**: Including files dynamically with untrusted input.

```
<?php
include $_GET['file'];
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-98: https://cwe.mitre.org/data/definitions/98.html

## Sample 40 — Insecure Dynamic Session Storage

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Session Storage
- **Description**: Storing sessions in user-controlled storage paths.

```
<?php
session_save_path($_GET['path']);
session_start();
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 41 — Insecure Dynamic Cookie Setting

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Cookie Setting
- **Description**: Setting cookies with user-controlled attributes.

```
<?php
setcookie($_GET['name'], $_GET['value'], $_GET['expire']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 42 — Insecure Dynamic Timezone Setting

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Timezone Setting
- **Description**: Setting timezone dynamically with user input.

```
<?php
date_default_timezone_set($_GET['timezone']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 43 — Insecure Dynamic Resource Limit

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Resource Limit
- **Description**: Setting resource limits with user input.

```
<?php
set_time_limit($_GET['limit']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 44 — Insecure Dynamic File Deletion

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic File Deletion
- **Description**: Deleting files based on user input.

```
<?php
unlink($_GET['file']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 45 — Insecure Dynamic Output Buffering

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Output Buffering
- **Description**: Configuring output buffering with user-controlled settings.

```
<?php
ob_start($_GET['handler']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 46 — Insecure Dynamic Charset Setting

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Charset Setting
- **Description**: Setting charset with user-controlled values.

```
<?php
header('Content-Type: text/html; charset=' . $_GET['charset']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 47 — Insecure Dynamic Memory Limit

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Memory Limit
- **Description**: Setting memory limits with user input.

```
<?php
ini_set('memory_limit', $_GET['limit']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 48 — Insecure Dynamic Locale Setting

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Locale Setting
- **Description**: Setting locale with user-controlled values.

```
<?php
setlocale(LC_ALL, $_GET['locale']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 49 — Insecure Dynamic Upload Path

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Upload Path
- **Description**: Setting upload paths with user input.

```
<?php
move_uploaded_file($_FILES['file']['tmp_name'], $_GET['path']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 50 — Insecure Dynamic Stream Wrapper

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Stream Wrapper
- **Description**: Registering stream wrappers with user input.

```
<?php
stream_wrapper_register($_GET['protocol'], $_GET['class']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 51 — Insecure Dynamic Error Handler

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Error Handler
- **Description**: Setting error handlers with user input.

```
<?php
set_error_handler($_GET['handler']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-209: https://cwe.mitre.org/data/definitions/209.html

## Sample 52 — Insecure Dynamic Filter Registration

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Filter Registration
- **Description**: Registering filters with user input.

```
<?php
stream_filter_register($_GET['filter'], $_GET['class']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 53 — Insecure Dynamic Opcode Cache

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Opcode Cache
- **Description**: Configuring opcode cache with user input.

```
<?php
opcache_compile_file($_GET['file']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 54 — Insecure Dynamic Autoload Path

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Autoload Path
- **Description**: Setting autoload paths with user input.

```
<?php
spl_autoload_register(function($class) { include $_GET['path'] . $class . '.php'; });
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 55 — Insecure Dynamic Include Path

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Include Path
- **Description**: Setting include paths with user input.

```
<?php
set_include_path($_GET['path']);
include 'file.php';
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 56 — Insecure Dynamic Session Handler

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Session Handler
- **Description**: Setting session handlers with user input.

```
<?php
session_set_save_handler(new $_GET['handler']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 57 — Insecure Dynamic Reflection Call

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Reflection Call
- **Description**: Calling methods dynamically with user input.

```
<?php
$reflector = new ReflectionClass($_GET['class']);
$reflector->getMethod($_GET['method'])->invoke(null);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 58 — Insecure Dynamic Stream Context

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Stream Context
- **Description**: Creating stream contexts with user-controlled options.

```
<?php
$context = stream_context_create($_GET['options']);
fopen('file.txt', 'r', false, $context);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 59 — Insecure Dynamic Soap Client

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic Soap Client
- **Description**: Creating SOAP clients with user-controlled WSDL.

```
<?php
$client = new SoapClient($_GET['wsdl']);
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 60 — Insecure Dynamic XML Parsing

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic XML Parsing
- **Description**: Parsing XML with user-controlled input.

```
<?php
$xml = simplexml_load_string($_GET['xml']);
echo $xml;
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A04_2021-Insecure_Design/
- CWE-611: https://cwe.mitre.org/data/definitions/611.html

## Sample 61 — Insecure Dynamic YAML Parsing

- **Language**: PHP
- **Vulnerability**: Insecure Dynamic YAML Parsing
- **Description**: Parsing YAML with user-controlled input.

```
<?php
$yaml = yaml_parse($_GET['yaml']);
echo $yaml;
?>
```

**References**:
- OWASP: https://owasp.org/Top10/A04_2021-Insecure_Design/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html
