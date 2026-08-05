# Vulnerable Code Samples: Python

Secure-code-review training examples (63 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — SQL Injection

- **Language**: Python
- **Vulnerability**: SQL Injection
- **Description**: Concatenating user input directly into SQL query without parameterization.

```
import sqlite3
def get_user(username):
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor = conn.execute(query)
    return cursor.fetchall()
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 2 — Insecure File Handling

- **Language**: Python
- **Vulnerability**: Insecure File Handling
- **Description**: Reading files without validating paths, allowing unauthorized access.

```
def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Path_Traversal
- CWE-73: https://cwe.mitre.org/data/definitions/73.html

## Sample 3 — Insecure Deserialization

- **Language**: Python
- **Vulnerability**: Insecure Deserialization
- **Description**: Using pickle to deserialize untrusted data.

```
import pickle
def load_data(data):
    return pickle.loads(data)
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 4 — Command Injection

- **Language**: Python
- **Vulnerability**: Command Injection
- **Description**: Using unsanitized input in subprocess call.

```
import subprocess
def run_script(script):
    subprocess.run(script, shell=True)
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Command_Injection
- CWE-77: https://cwe.mitre.org/data/definitions/77.html

## Sample 5 — Insecure Regex

- **Language**: Python
- **Vulnerability**: Insecure Regex
- **Description**: Using regex vulnerable to ReDoS.

```
import re
def check_input(input):
    return re.match('(a+)+b', input)

```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 6 — Insecure HTTP Request

- **Language**: Python
- **Vulnerability**: Insecure HTTP Request
- **Description**: Making HTTP requests without certificate validation.

```
import requests
def fetch_data(url):
    response = requests.get(url, verify=False)
    return response.text
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-295: https://cwe.mitre.org/data/definitions/295.html

## Sample 7 — Insecure YAML Parsing

- **Language**: Python
- **Vulnerability**: Insecure YAML Parsing
- **Description**: Using unsafe YAML loading.

```
import yaml
def parse_yaml(data):
    return yaml.load(data, Loader=yaml.Loader)
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 8 — Insecure XML Parsing

- **Language**: Python
- **Vulnerability**: Insecure XML Parsing
- **Description**: Parsing XML without disabling external entities.

```
import xml.etree.ElementTree as ET
def parse_xml(data):
    return ET.fromstring(data)
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing
- CWE-611: https://cwe.mitre.org/data/definitions/611.html

## Sample 9 — Insecure Eval

- **Language**: Python
- **Vulnerability**: Insecure Eval
- **Description**: Using exec() with user input.

```
def execute_code(code):
    exec(code)
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Eval_Injection
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 10 — Insecure Password Storage

- **Language**: Python
- **Vulnerability**: Insecure Password Storage
- **Description**: Storing passwords in plain text.

```
def save_password(password):
    with open('passwords.txt', 'a') as f:
        f.write(password + '\n')
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-257: https://cwe.mitre.org/data/definitions/257.html

## Sample 11 — Insecure Redirect

- **Language**: Python
- **Vulnerability**: Insecure Redirect
- **Description**: Redirecting to user-supplied URL.

```
from flask import redirect, request
def redirect_user():
    return redirect(request.args.get('url'))
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Unvalidated_Redirects_and_Forwards
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 12 — SQL Injection

- **Language**: Python
- **Vulnerability**: SQL Injection
- **Description**: Concatenating user input directly into SQL query without parameterization.

```
import sqlite3
def get_user(username):
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor = conn.execute(query)
    return cursor.fetchall()
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 13 — Insecure File Handling

- **Language**: Python
- **Vulnerability**: Insecure File Handling
- **Description**: Reading files without validating paths, allowing unauthorized access.

```
def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Path_Traversal
- CWE-73: https://cwe.mitre.org/data/definitions/73.html

## Sample 14 — Insecure Deserialization

- **Language**: Python
- **Vulnerability**: Insecure Deserialization
- **Description**: Using pickle to deserialize untrusted data.

```
import pickle
def load_data(data):
    return pickle.loads(data)
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 15 — Command Injection

- **Language**: Python
- **Vulnerability**: Command Injection
- **Description**: Using unsanitized input in subprocess call.

```
import subprocess
def run_script(script):
    subprocess.run(script, shell=True)
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Command_Injection
- CWE-77: https://cwe.mitre.org/data/definitions/77.html

## Sample 16 — Insecure Regex

- **Language**: Python
- **Vulnerability**: Insecure Regex
- **Description**: Using regex vulnerable to ReDoS.

```
import re
def check_input(input):
    return re.match('(a+)+b', input)

```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 17 — Insecure HTTP Request

- **Language**: Python
- **Vulnerability**: Insecure HTTP Request
- **Description**: Making HTTP requests without certificate validation.

```
import requests
def fetch_data(url):
    response = requests.get(url, verify=False)
    return response.text
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-295: https://cwe.mitre.org/data/definitions/295.html

## Sample 18 — Insecure YAML Parsing

- **Language**: Python
- **Vulnerability**: Insecure YAML Parsing
- **Description**: Using unsafe YAML loading.

```
import yaml
def parse_yaml(data):
    return yaml.load(data, Loader=yaml.Loader)
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 19 — Insecure XML Parsing

- **Language**: Python
- **Vulnerability**: Insecure XML Parsing
- **Description**: Parsing XML without disabling external entities.

```
import xml.etree.ElementTree as ET
def parse_xml(data):
    return ET.fromstring(data)
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing
- CWE-611: https://cwe.mitre.org/data/definitions/611.html

## Sample 20 — Insecure Eval

- **Language**: Python
- **Vulnerability**: Insecure Eval
- **Description**: Using exec() with user input.

```
def execute_code(code):
    exec(code)
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Eval_Injection
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 21 — Insecure Password Storage

- **Language**: Python
- **Vulnerability**: Insecure Password Storage
- **Description**: Storing passwords in plain text.

```
def save_password(password):
    with open('passwords.txt', 'a') as f:
        f.write(password + '\n')
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-257: https://cwe.mitre.org/data/definitions/257.html

## Sample 22 — Insecure Redirect

- **Language**: Python
- **Vulnerability**: Insecure Redirect
- **Description**: Redirecting to user-supplied URL.

```
from flask import redirect, request
def redirect_user():
    return redirect(request.args.get('url'))
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Unvalidated_Redirects_and_Forwards
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 23 — Insecure Third-Party Library

- **Language**: Python
- **Vulnerability**: Insecure Third-Party Library
- **Description**: Using a deprecated and vulnerable version of a library (e.g., requests v2.19.0 with known CVE).

```
import requests
def fetch_data(url):
    response = requests.get(url)  # Vulnerable version <2.20.0
    return response.text
```

**References**:
- OWASP: https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/
- CVE-2018-18074: https://nvd.nist.gov/vuln/detail/CVE-2018-18074

## Sample 24 — Insecure Dynamic Import

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Import
- **Description**: Importing modules dynamically based on user input.

```
def load_module(name):
    module = __import__(name)
    return module
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Code_Injection
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 25 — Insecure Dynamic Attribute

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Attribute
- **Description**: Setting object attributes dynamically from user input.

```
def set_attribute(obj, name, value):
    setattr(obj, name, value)
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Code_Injection
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 26 — Insecure Threading

- **Language**: Python
- **Vulnerability**: Insecure Threading
- **Description**: Accessing shared resources without locks.

```
counter = 0
def increment():
    global counter
    counter += 1
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 27 — Insecure Interprocess Communication

- **Language**: Python
- **Vulnerability**: Insecure Interprocess Communication
- **Description**: Using unencrypted pipes for interprocess communication, exposing sensitive data.

```
import subprocess
def communicate(data):
    proc = subprocess.Popen(['process'], stdin=subprocess.PIPE)
    proc.communicate(input=data.encode())
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-319: https://cwe.mitre.org/data/definitions/319.html

## Sample 28 — Insecure Monkey Patching

- **Language**: Python
- **Vulnerability**: Insecure Monkey Patching
- **Description**: Dynamically modifying runtime behavior with untrusted code.

```
import types
def patch_function(obj, name, code):
    setattr(obj, name, types.MethodType(code, obj))
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 29 — Insecure Dynamic Code Execution

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Code Execution
- **Description**: Executing dynamically generated code from untrusted sources.

```
def run_code(code):
    compile(code, '<string>', 'exec')
    exec(code)
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 30 — Insecure Signal Handling

- **Language**: Python
- **Vulnerability**: Insecure Signal Handling
- **Description**: Handling signals without validating context.

```
import signal
def handler(sig, frame):
    print('Signal received')
signal.signal(signal.SIGINT, handler)
```

**References**:
- CWE-479: https://cwe.mitre.org/data/definitions/479.html

## Sample 31 — Insecure Dynamic Module Loading

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Module Loading
- **Description**: Loading modules dynamically based on user input.

```
import importlib
def load_module(name):
    return importlib.import_module(name)
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 32 — Insecure Dynamic Class Creation

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Class Creation
- **Description**: Creating classes dynamically with untrusted input.

```
def create_class(name):
    return type(name, (), {})

```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 33 — Insecure Dynamic Object Creation

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Object Creation
- **Description**: Creating objects dynamically from untrusted input.

```
def create_object(class_name):
    return globals()[class_name]()
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 34 — Insecure Dynamic Function Definition

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Function Definition
- **Description**: Defining functions dynamically with user input.

```
def create_function(name, code):
    globals()[name] = lambda x: eval(code)
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 35 — Insecure Dynamic Attribute Deletion

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Attribute Deletion
- **Description**: Deleting object attributes dynamically with user input.

```
def delete_attribute(obj, name):
    delattr(obj, name)
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 36 — Insecure Dynamic Method Binding

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Method Binding
- **Description**: Binding methods dynamically with untrusted input.

```
def bind_method(obj, name, func):
    setattr(obj, name, func)
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 37 — Insecure Dynamic Package Installation

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Package Installation
- **Description**: Installing packages dynamically with user input.

```
import pip
def install_package(name):
    pip.main(['install', name])
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 38 — Insecure Dynamic Property Injection

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Property Injection
- **Description**: Injecting properties dynamically with untrusted input.

```
def inject_property(obj, name, value):
    obj.__dict__[name] = value
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 39 — Insecure Dynamic Code Compilation

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Code Compilation
- **Description**: Compiling code dynamically with untrusted input.

```
def compile_code(code):
    return compile(code, '<string>', 'exec')
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 40 — Insecure Dynamic Resource Import

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Resource Import
- **Description**: Importing resources dynamically with untrusted input.

```
def import_resource(path):
    with open(path, 'r') as f:
        return f.read()
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 41 — Insecure Dynamic Signal Registration

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Signal Registration
- **Description**: Registering signal handlers with unvalidated callbacks.

```
import signal
def register_signal(sig, callback):
    signal.signal(sig, callback)
```

**References**:
- CWE-479: https://cwe.mitre.org/data/definitions/479.html

## Sample 42 — Insecure Dynamic Thread Creation

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Thread Creation
- **Description**: Creating threads with unvalidated target functions.

```
import threading
def create_thread(target):
    threading.Thread(target=target).start()
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 43 — Insecure Dynamic Context Manager

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Context Manager
- **Description**: Using context managers with untrusted input.

```
from contextlib import contextmanager
def create_context(name):
    return contextmanager(lambda: globals()[name]())
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 44 — Insecure Dynamic Event Loop

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Event Loop
- **Description**: Creating event loops with untrusted tasks.

```
import asyncio
def run_task(task):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task())
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 45 — Insecure Dynamic Decorator

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Decorator
- **Description**: Applying decorators dynamically with untrusted input.

```
def apply_decorator(func, decorator):
    return globals()[decorator](func)
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 46 — Insecure Dynamic Process Spawning

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Process Spawning
- **Description**: Spawning processes with untrusted commands.

```
import os
def spawn_process(cmd):
    os.system(cmd)
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-78: https://cwe.mitre.org/data/definitions/78.html

## Sample 47 — Insecure Dynamic Logging Handler

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Logging Handler
- **Description**: Configuring logging handlers with untrusted input.

```
import logging
def set_handler(handler):
    logging.getLogger().addHandler(handler())
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html

## Sample 48 — Insecure Dynamic Resource Fork

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Resource Fork
- **Description**: Accessing resource forks with untrusted paths.

```
import resource
def access_fork(path):
    resource.open(path, 'r')
    return resource.getresource(path)
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 49 — Insecure Dynamic File Descriptor

- **Language**: Python
- **Vulnerability**: Insecure Dynamic File Descriptor
- **Description**: Using file descriptors with untrusted input.

```
import os
def open_fd(fd):
    return os.fdopen(fd, 'r')
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 50 — Insecure Dynamic Traceback Handling

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Traceback Handling
- **Description**: Handling tracebacks with untrusted formatting.

```
import traceback
def format_traceback(fmt):
    return traceback.format_exc(fmt)
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-209: https://cwe.mitre.org/data/definitions/209.html

## Sample 51 — Insecure Dynamic Metaclass

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Metaclass
- **Description**: Using metaclasses with untrusted input.

```
def create_metaclass(name):
    return type(name, (type,), {})
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 52 — Insecure Dynamic Generator

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Generator
- **Description**: Creating generators with untrusted input.

```
def create_generator(code):
    return (eval(code) for _ in range(10))
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 53 — Insecure Dynamic Weak Reference

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Weak Reference
- **Description**: Creating weak references with untrusted objects.

```
import weakref
def create_weakref(obj):
    return weakref.ref(obj)
```

**References**:
- OWASP: https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/
- CWE-672: https://cwe.mitre.org/data/definitions/672.html

## Sample 54 — Insecure Dynamic Profiler

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Profiler
- **Description**: Enabling profiling with user-controlled settings.

```
import cProfile
def profile_code(code):
    cProfile.run(code)
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 55 — Insecure Dynamic AST Manipulation

- **Language**: Python
- **Vulnerability**: Insecure Dynamic AST Manipulation
- **Description**: Manipulating AST with untrusted input.

```
import ast
def modify_ast(code):
    return ast.parse(code)
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 56 — Insecure Dynamic Code Compilation

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Code Compilation
- **Description**: Compiling code dynamically with untrusted input.

```
def compile_code(code):
    return compile(code, '<string>', 'exec')
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 57 — Insecure Dynamic Import Hook

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Import Hook
- **Description**: Implementing import hooks with untrusted input.

```
import importlib
class CustomFinder:
    def find_spec(self, name, path, target=None):
        return importlib.util.spec_from_loader(name, None)
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 58 — Insecure Dynamic Memory Cache

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Memory Cache
- **Description**: Using memory cache with user-controlled keys.

```
from cachetools import LRUCache
def cache_data(key):
    cache = LRUCache(maxsize=100)
    cache[key] = 'data'
    return cache[key]
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 59 — Insecure Dynamic Property Descriptor

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Property Descriptor
- **Description**: Defining property descriptors with untrusted input.

```
def define_property(obj, name, desc):
    return type(obj).__setattr__(obj, name, property(**desc))
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 60 — Insecure Dynamic Frame Injection

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Frame Injection
- **Description**: Injecting frames with untrusted input.

```
import sys
def inject_frame(frame):
    sys._current_frames()[0] = frame
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 61 — Insecure Dynamic Module Reload

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Module Reload
- **Description**: Reloading modules with untrusted names.

```
import importlib
def reload_module(name):
    importlib.reload(importlib.import_module(name))
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 62 — Insecure Dynamic Context Var

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Context Var
- **Description**: Using context variables with untrusted keys.

```
import contextvars
def set_context(key, value):
    var = contextvars.ContextVar(key)
    var.set(value)
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 63 — Insecure Dynamic Signal Dispatch

- **Language**: Python
- **Vulnerability**: Insecure Dynamic Signal Dispatch
- **Description**: Dispatching signals with untrusted handlers.

```
import signal
def dispatch_signal(sig, handler):
    signal.signal(sig, lambda s, f: handler())
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-479: https://cwe.mitre.org/data/definitions/479.html
