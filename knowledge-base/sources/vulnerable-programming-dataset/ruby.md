# Vulnerable Code Samples: Ruby

Secure-code-review training examples (61 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — Command Injection

- **Language**: Ruby
- **Vulnerability**: Command Injection
- **Description**: Executing unsanitized user input as a system command.

```
def execute_command(user_input)
  system("ls #{user_input}")
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Command_Injection
- CWE-77: https://cwe.mitre.org/data/definitions/77.html

## Sample 2 — Insecure Regular Expression

- **Language**: Ruby
- **Vulnerability**: Insecure Regular Expression
- **Description**: Using regex vulnerable to ReDoS (Regular Expression Denial of Service).

```
def validate_email(email)
  email =~ /(a+)+b/
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 3 — XSS

- **Language**: Ruby
- **Vulnerability**: XSS
- **Description**: Outputting user input without proper escaping.

```
<%= params[:input] %>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/xss/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 4 — Insecure File Permissions

- **Language**: Ruby
- **Vulnerability**: Insecure File Permissions
- **Description**: Writing files with overly permissive permissions.

```
File.write('data.txt', user_input, mode: 0777)
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 5 — Insecure Cookie Handling

- **Language**: Ruby
- **Vulnerability**: Insecure Cookie Handling
- **Description**: Setting cookies without Secure flag.

```
cookies[:session] = { value: '12345', expires: 1.day.from_now }
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-614: https://cwe.mitre.org/data/definitions/614.html

## Sample 6 — SQL Injection

- **Language**: Ruby
- **Vulnerability**: SQL Injection
- **Description**: Using string interpolation in SQL queries.

```
def find_user(name)
  ActiveRecord::Base.connection.execute("SELECT * FROM users WHERE name = '#{name}'")
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 7 — Insecure Eval

- **Language**: Ruby
- **Vulnerability**: Insecure Eval
- **Description**: Using eval with user input.

```
def run_code(code)
  eval(code)
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Eval_Injection
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 8 — Insecure File Upload

- **Language**: Ruby
- **Vulnerability**: Insecure File Upload
- **Description**: Uploading files without type validation.

```
def upload_file
  File.write("uploads/#{params[:file].original_filename}", params[:file].read)
end
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- CWE-434: https://cwe.mitre.org/data/definitions/434.html

## Sample 9 — Insecure Redirect

- **Language**: Ruby
- **Vulnerability**: Insecure Redirect
- **Description**: Redirecting to user-controlled URL.

```
def redirect
  redirect_to params[:url]
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Unvalidated_Redirects_and_Forwards
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 10 — Insecure TLS Configuration

- **Language**: Ruby
- **Vulnerability**: Insecure TLS Configuration
- **Description**: Using outdated TLS version.

```
require 'net/http'
http = Net::HTTP.new('example.com', 443)
http.use_ssl = true
http.ssl_version = :TLSv1
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-326: https://cwe.mitre.org/data/definitions/326.html

## Sample 11 — Insecure Database Connection

- **Language**: Ruby
- **Vulnerability**: Insecure Database Connection
- **Description**: Using unencrypted database connection.

```
ActiveRecord::Base.establish_connection(
  adapter: 'mysql2',
  host: 'localhost',
  username: 'user',
  password: 'pass',
  database: 'db'
)
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-311: https://cwe.mitre.org/data/definitions/311.html

## Sample 12 — Command Injection

- **Language**: Ruby
- **Vulnerability**: Command Injection
- **Description**: Executing unsanitized user input as a system command.

```
def execute_command(user_input)
  system("ls #{user_input}")
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Command_Injection
- CWE-77: https://cwe.mitre.org/data/definitions/77.html

## Sample 13 — Insecure Regular Expression

- **Language**: Ruby
- **Vulnerability**: Insecure Regular Expression
- **Description**: Using regex vulnerable to ReDoS (Regular Expression Denial of Service).

```
def validate_email(email)
  email =~ /(a+)+b/
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 14 — XSS

- **Language**: Ruby
- **Vulnerability**: XSS
- **Description**: Outputting user input without proper escaping.

```
<%= params[:input] %>
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/xss/
- CWE-79: https://cwe.mitre.org/data/definitions/79.html

## Sample 15 — Insecure File Permissions

- **Language**: Ruby
- **Vulnerability**: Insecure File Permissions
- **Description**: Writing files with overly permissive permissions.

```
File.write('data.txt', user_input, mode: 0777)
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 16 — Insecure Cookie Handling

- **Language**: Ruby
- **Vulnerability**: Insecure Cookie Handling
- **Description**: Setting cookies without Secure flag.

```
cookies[:session] = { value: '12345', expires: 1.day.from_now }
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-614: https://cwe.mitre.org/data/definitions/614.html

## Sample 17 — SQL Injection

- **Language**: Ruby
- **Vulnerability**: SQL Injection
- **Description**: Using string interpolation in SQL queries.

```
def find_user(name)
  ActiveRecord::Base.connection.execute("SELECT * FROM users WHERE name = '#{name}'")
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 18 — Insecure Eval

- **Language**: Ruby
- **Vulnerability**: Insecure Eval
- **Description**: Using eval with user input.

```
def run_code(code)
  eval(code)
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Eval_Injection
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 19 — Insecure File Upload

- **Language**: Ruby
- **Vulnerability**: Insecure File Upload
- **Description**: Uploading files without type validation.

```
def upload_file
  File.write("uploads/#{params[:file].original_filename}", params[:file].read)
end
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- CWE-434: https://cwe.mitre.org/data/definitions/434.html

## Sample 20 — Insecure Redirect

- **Language**: Ruby
- **Vulnerability**: Insecure Redirect
- **Description**: Redirecting to user-controlled URL.

```
def redirect
  redirect_to params[:url]
end
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Unvalidated_Redirects_and_Forwards
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 21 — Insecure TLS Configuration

- **Language**: Ruby
- **Vulnerability**: Insecure TLS Configuration
- **Description**: Using outdated TLS version.

```
require 'net/http'
http = Net::HTTP.new('example.com', 443)
http.use_ssl = true
http.ssl_version = :TLSv1
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-326: https://cwe.mitre.org/data/definitions/326.html

## Sample 22 — Insecure Database Connection

- **Language**: Ruby
- **Vulnerability**: Insecure Database Connection
- **Description**: Using unencrypted database connection.

```
ActiveRecord::Base.establish_connection(
  adapter: 'mysql2',
  host: 'localhost',
  username: 'user',
  password: 'pass',
  database: 'db'
)
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-311: https://cwe.mitre.org/data/definitions/311.html

## Sample 23 — Insecure Mass Assignment

- **Language**: Ruby
- **Vulnerability**: Insecure Mass Assignment
- **Description**: Allowing user input to update protected attributes.

```
def update
  @user.update_attributes(params[:user])
end
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-915: https://cwe.mitre.org/data/definitions/915.html

## Sample 24 — Insecure Tempfile Creation

- **Language**: Ruby
- **Vulnerability**: Insecure Tempfile Creation
- **Description**: Creating temporary files without secure naming.

```
require 'tempfile'
file = Tempfile.new('myapp')
file.write('data')
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-377: https://cwe.mitre.org/data/definitions/377.html

## Sample 25 — Insecure Session Timeout

- **Language**: Ruby
- **Vulnerability**: Insecure Session Timeout
- **Description**: Not setting session expiration.

```
session[:user_id] = user.id
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-613: https://cwe.mitre.org/data/definitions/613.html

## Sample 26 — Insecure Queue Processing

- **Language**: Ruby
- **Vulnerability**: Insecure Queue Processing
- **Description**: Processing unvalidated messages from a queue, allowing code execution.

```
require 'sidekiq'
class Worker
  include Sidekiq::Worker
  def perform(message)
    eval(message)
  end
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-95: https://cwe.mitre.org/data/definitions/95.html

## Sample 27 — Insecure YAML Serialization

- **Language**: Ruby
- **Vulnerability**: Insecure YAML Serialization
- **Description**: Serializing objects to YAML without restricting types.

```
require 'yaml'
def serialize(obj)
  YAML.dump(obj)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 28 — Insecure Session Storage

- **Language**: Ruby
- **Vulnerability**: Insecure Session Storage
- **Description**: Storing sessions in unencrypted cookies.

```
cookies[:session] = Base64.encode64(user.to_json)
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-311: https://cwe.mitre.org/data/definitions/311.html

## Sample 29 — Insecure Dynamic Routing

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Routing
- **Description**: Defining routes based on user input.

```
get "/#{params[:path]}" do
  'OK'
end
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 30 — Insecure Dynamic Method Call

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Method Call
- **Description**: Calling methods dynamically based on user input.

```
def call_method(obj, method)
  obj.send(method)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 31 — Insecure API Token Exposure

- **Language**: Ruby
- **Vulnerability**: Insecure API Token Exposure
- **Description**: Exposing API tokens in client-side code.

```
<script>
  const token = '<%= api_token %>';
</script>
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 32 — Insecure Dynamic Constant

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Constant
- **Description**: Defining constants dynamically with user input.

```
def set_constant(name, value)
  Object.const_set(name, value)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 33 — Insecure Dynamic Template Rendering

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Template Rendering
- **Description**: Rendering templates with untrusted input.

```
ERB.new(params[:template]).result
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 34 — Insecure Dynamic Module Inclusion

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Module Inclusion
- **Description**: Including modules dynamically with user input.

```
def include_module(name)
  include Object.const_get(name)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 35 — Insecure Dynamic Logger

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Logger
- **Description**: Configuring logger with user-controlled settings.

```
require 'logger'
def set_logger(level)
  Logger.new(STDOUT).level = level
end
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html

## Sample 36 — Insecure Dynamic Job Scheduling

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Job Scheduling
- **Description**: Scheduling jobs with unvalidated input.

```
require 'sidekiq'
Sidekiq::Cron::Job.create(name: params[:name], cron: params[:cron], class: params[:class])
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 37 — Insecure Dynamic Class Definition

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Class Definition
- **Description**: Defining classes dynamically with user input.

```
def define_class(name)
  Class.new { define_method(:run) { puts name } }
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 38 — Insecure Dynamic Resource Access

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Resource Access
- **Description**: Accessing resources dynamically with untrusted input.

```
def access_resource(path)
  File.read(path)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 39 — Insecure Dynamic File Access

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic File Access
- **Description**: Accessing files dynamically with untrusted input.

```
def read_file(path)
  File.read(path)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 40 — Insecure Dynamic Gem Loading

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Gem Loading
- **Description**: Loading gems dynamically based on user input.

```
def load_gem(name)
  require name
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 41 — Insecure Dynamic Cache Storage

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Cache Storage
- **Description**: Storing cache data in user-controlled paths.

```
require 'redis'
def cache_data(key, value)
  Redis.new.set(params[:path] + key, value)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 42 — Insecure Dynamic Queue Creation

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Queue Creation
- **Description**: Creating message queues with user-controlled names.

```
require 'bunny'
def create_queue(name)
  Bunny.new.create_channel.queue(name)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 43 — Insecure Dynamic Database Connection

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Database Connection
- **Description**: Establishing database connections with user-controlled parameters.

```
require 'active_record'
def connect(db)
  ActiveRecord::Base.establish_connection(db)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 44 — Insecure Dynamic HTTP Method

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic HTTP Method
- **Description**: Executing HTTP methods based on user input.

```
require 'net/http'
def send_request(method)
  Net::HTTP.const_get(method.capitalize).new('/').request
end
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 45 — Insecure Dynamic Template Engine

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Template Engine
- **Description**: Using template engines with untrusted templates.

```
require 'erb'
def render_template(tmpl)
  ERB.new(tmpl).result
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 46 — Insecure Dynamic Worker Configuration

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Worker Configuration
- **Description**: Configuring workers with user-controlled settings.

```
require 'sidekiq'
def configure_worker(options)
  Sidekiq.configure_server { |config| config.redis = options }
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 47 — Insecure Dynamic Email Sending

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Email Sending
- **Description**: Sending emails with user-controlled headers.

```
require 'mail'
def send_email(headers)
  Mail.deliver do
    headers headers
    to 'user@example.com'
    from 'sender@example.com'
    subject 'Test'
    body 'Content'
  end
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-113: https://cwe.mitre.org/data/definitions/113.html

## Sample 48 — Insecure Dynamic Asset Compilation

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Asset Compilation
- **Description**: Compiling assets with user-controlled paths.

```
require 'sprockets'
def compile_asset(path)
  Sprockets::Environment.new.append_path(path)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 49 — Insecure Dynamic OAuth Configuration

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic OAuth Configuration
- **Description**: Configuring OAuth with user-controlled parameters.

```
require 'oauth2'
def configure_oauth(params)
  OAuth2::Client.new(params[:id], params[:secret], site: params[:site])
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 50 — Insecure Dynamic SMTP Configuration

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic SMTP Configuration
- **Description**: Configuring SMTP with user-controlled settings.

```
require 'mail'
def configure_smtp(settings)
  Mail.defaults { delivery_method :smtp, settings }
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 51 — Insecure Dynamic Memcache Configuration

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Memcache Configuration
- **Description**: Configuring memcache with user-controlled settings.

```
require 'dalli'
def configure_cache(options)
  Dalli::Client.new(options[:host])
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 52 — Insecure Dynamic GraphQL Query

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic GraphQL Query
- **Description**: Executing GraphQL queries with user-controlled input.

```
require 'graphql'
def execute_query(query)
  Schema.execute(query)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 53 — Insecure Dynamic WebSocket Configuration

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic WebSocket Configuration
- **Description**: Configuring WebSocket with user-controlled settings.

```
require 'faye/websocket'
def configure_ws(url)
  Faye::WebSocket::Client.new(url)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-346: https://cwe.mitre.org/data/definitions/346.html

## Sample 54 — Insecure Dynamic LDAP Configuration

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic LDAP Configuration
- **Description**: Configuring LDAP connections with user-controlled parameters.

```
require 'net/ldap'
def configure_ldap(params)
  Net::LDAP.new(host: params[:host], port: params[:port])
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 55 — Insecure Dynamic Logger Configuration

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Logger Configuration
- **Description**: Configuring loggers with user-controlled settings.

```
require 'logger'
def configure_logger(path)
  Logger.new(path)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html

## Sample 56 — Insecure Dynamic Rack Middleware

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Rack Middleware
- **Description**: Applying Rack middleware with untrusted input.

```
require 'rack'
def apply_middleware(app, middleware)
  Rack::Builder.new { use Object.const_get(middleware); run app }
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 57 — Insecure Dynamic File Compression

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic File Compression
- **Description**: Compressing files with user-controlled paths.

```
require 'zlib'
def compress_file(path)
  Zlib::GzipWriter.open(path) { |gz| gz.write('data') }
end
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 58 — Insecure Dynamic Tempfile Creation

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic Tempfile Creation
- **Description**: Creating temporary files with user-controlled paths.

```
require 'tempfile'
def create_tempfile(path)
  Tempfile.new(path)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 59 — Insecure Dynamic JSON Parsing

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic JSON Parsing
- **Description**: Parsing JSON with untrusted input.

```
require 'json'
def parse_json(data)
  JSON.parse(data)
end
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 60 — Insecure Dynamic HTTP Client

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic HTTP Client
- **Description**: Configuring HTTP clients with user-controlled settings.

```
require 'httparty'
def configure_client(options)
  HTTParty.get(options[:url])
end
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 61 — Insecure Dynamic File Encryption

- **Language**: Ruby
- **Vulnerability**: Insecure Dynamic File Encryption
- **Description**: Encrypting files with user-controlled keys.

```
require 'openssl'
def encrypt_file(path, key)
  cipher = OpenSSL::Cipher.new('AES-256-CBC')
  cipher.encrypt
  cipher.key = key
end
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-326: https://cwe.mitre.org/data/definitions/326.html
