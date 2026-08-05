# Vulnerable Code Samples: Go

Secure-code-review training examples (60 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — Path Traversal

- **Language**: Go
- **Vulnerability**: Path Traversal
- **Description**: Allowing user input to access unauthorized files without validation.

```
package main
import "os"
func readFile(path string) {
    content, _ := os.ReadFile(path)
    return content
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Path_Traversal
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 2 — SQL Injection

- **Language**: Go
- **Vulnerability**: SQL Injection
- **Description**: Building SQL queries with string concatenation.

```
package main
import "database/sql"
func queryUser(db *sql.DB, name string) {
    db.Query("SELECT * FROM users WHERE name = '" + name + "'")
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 3 — Insecure HTTP Headers

- **Language**: Go
- **Vulnerability**: Insecure HTTP Headers
- **Description**: Missing security headers in HTTP response.

```
package main
import "net/http"
func handler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Hello"))
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-693: https://cwe.mitre.org/data/definitions/693.html

## Sample 4 — Insecure TLS Configuration

- **Language**: Go
- **Vulnerability**: Insecure TLS Configuration
- **Description**: Using outdated TLS version.

```
package main
import "crypto/tls"
func getTLSConfig() *tls.Config {
    return &tls.Config{MinVersion: tls.VersionTLS10}
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-326: https://cwe.mitre.org/data/definitions/326.html

## Sample 5 — Hardcoded Secrets

- **Language**: Go
- **Vulnerability**: Hardcoded Secrets
- **Description**: Embedding sensitive credentials in code.

```
package main
const apiKey = "secret-api-key"
func main() {
    // Use apiKey
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 6 — Insecure Randomness

- **Language**: Go
- **Vulnerability**: Insecure Randomness
- **Description**: Using math/rand for cryptographic purposes.

```
package main
import "math/rand"
func generateKey() int {
    return rand.Int()
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 7 — Insecure Logging

- **Language**: Go
- **Vulnerability**: Insecure Logging
- **Description**: Logging sensitive data without sanitization.

```
package main
import "log"
func logData(data string) {
    log.Println("Data: ", data)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-532: https://cwe.mitre.org/data/definitions/532.html

## Sample 8 — Insecure Cookie Handling

- **Language**: Go
- **Vulnerability**: Insecure Cookie Handling
- **Description**: Setting cookies without Secure flag.

```
package main
import "net/http"
func setCookie(w http.ResponseWriter) {
    http.SetCookie(w, &http.Cookie{Name: "session", Value: "12345"})
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-614: https://cwe.mitre.org/data/definitions/614.html

## Sample 9 — Insecure Deserialization

- **Language**: Go
- **Vulnerability**: Insecure Deserialization
- **Description**: Deserializing untrusted data with gob.

```
package main
import "encoding/gob"
func decode(data []byte) interface{} {
    var result interface{}
    gob.NewDecoder(bytes.NewReader(data)).Decode(&result)
    return result
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 10 — Insecure File Permissions

- **Language**: Go
- **Vulnerability**: Insecure File Permissions
- **Description**: Creating files with permissive permissions.

```
package main
import "os"
func createFile(name, data string) {
    os.WriteFile(name, []byte(data), 0777)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 11 — Insecure JSON Parsing

- **Language**: Go
- **Vulnerability**: Insecure JSON Parsing
- **Description**: Parsing JSON without validation.

```
package main
import "encoding/json"
func parseJSON(data []byte) interface{} {
    var result interface{}
    json.Unmarshal(data, &result)
    return result
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 12 — Path Traversal

- **Language**: Go
- **Vulnerability**: Path Traversal
- **Description**: Allowing user input to access unauthorized files without validation.

```
package main
import "os"
func readFile(path string) {
    content, _ := os.ReadFile(path)
    return content
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Path_Traversal
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 13 — SQL Injection

- **Language**: Go
- **Vulnerability**: SQL Injection
- **Description**: Building SQL queries with string concatenation.

```
package main
import "database/sql"
func queryUser(db *sql.DB, name string) {
    db.Query("SELECT * FROM users WHERE name = '" + name + "'")
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 14 — Insecure HTTP Headers

- **Language**: Go
- **Vulnerability**: Insecure HTTP Headers
- **Description**: Missing security headers in HTTP response.

```
package main
import "net/http"
func handler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Hello"))
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-693: https://cwe.mitre.org/data/definitions/693.html

## Sample 15 — Insecure TLS Configuration

- **Language**: Go
- **Vulnerability**: Insecure TLS Configuration
- **Description**: Using outdated TLS version.

```
package main
import "crypto/tls"
func getTLSConfig() *tls.Config {
    return &tls.Config{MinVersion: tls.VersionTLS10}
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-326: https://cwe.mitre.org/data/definitions/326.html

## Sample 16 — Hardcoded Secrets

- **Language**: Go
- **Vulnerability**: Hardcoded Secrets
- **Description**: Embedding sensitive credentials in code.

```
package main
const apiKey = "secret-api-key"
func main() {
    // Use apiKey
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 17 — Insecure Randomness

- **Language**: Go
- **Vulnerability**: Insecure Randomness
- **Description**: Using math/rand for cryptographic purposes.

```
package main
import "math/rand"
func generateKey() int {
    return rand.Int()
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 18 — Insecure Logging

- **Language**: Go
- **Vulnerability**: Insecure Logging
- **Description**: Logging sensitive data without sanitization.

```
package main
import "log"
func logData(data string) {
    log.Println("Data: ", data)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-532: https://cwe.mitre.org/data/definitions/532.html

## Sample 19 — Insecure Cookie Handling

- **Language**: Go
- **Vulnerability**: Insecure Cookie Handling
- **Description**: Setting cookies without Secure flag.

```
package main
import "net/http"
func setCookie(w http.ResponseWriter) {
    http.SetCookie(w, &http.Cookie{Name: "session", Value: "12345"})
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-614: https://cwe.mitre.org/data/definitions/614.html

## Sample 20 — Insecure Deserialization

- **Language**: Go
- **Vulnerability**: Insecure Deserialization
- **Description**: Deserializing untrusted data with gob.

```
package main
import "encoding/gob"
func decode(data []byte) interface{} {
    var result interface{}
    gob.NewDecoder(bytes.NewReader(data)).Decode(&result)
    return result
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 21 — Insecure File Permissions

- **Language**: Go
- **Vulnerability**: Insecure File Permissions
- **Description**: Creating files with permissive permissions.

```
package main
import "os"
func createFile(name, data string) {
    os.WriteFile(name, []byte(data), 0777)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 22 — Insecure JSON Parsing

- **Language**: Go
- **Vulnerability**: Insecure JSON Parsing
- **Description**: Parsing JSON without validation.

```
package main
import "encoding/json"
func parseJSON(data []byte) interface{} {
    var result interface{}
    json.Unmarshal(data, &result)
    return result
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 23 — Environment Variable Exposure

- **Language**: Go
- **Vulnerability**: Environment Variable Exposure
- **Description**: Exposing sensitive environment variables in error messages.

```
package main
import "os"
func getConfig() string {
    key := os.Getenv("API_KEY")
    if key == "" {
        panic("API_KEY not set: " + key)
    }
    return key
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-497: https://cwe.mitre.org/data/definitions/497.html

## Sample 24 — Insecure Mutex Usage

- **Language**: Go
- **Vulnerability**: Insecure Mutex Usage
- **Description**: Improper mutex locking leading to race conditions.

```
package main
import "sync"
var counter int
var mu sync.Mutex
func increment() {
    counter++
}
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 25 — Insecure Error Exposure

- **Language**: Go
- **Vulnerability**: Insecure Error Exposure
- **Description**: Returning detailed error messages to clients.

```
package main
import "net/http"
func handler(w http.ResponseWriter, r *http.Request) {
    _, err := os.Open("file.txt")
    if err != nil {
        http.Error(w, err.Error(), 500)
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-209: https://cwe.mitre.org/data/definitions/209.html

## Sample 26 — Insecure Dependency Pinning

- **Language**: Go
- **Vulnerability**: Insecure Dependency Pinning
- **Description**: Using unpinned dependencies in go.mod, risking supply chain attacks.

```
module example
go 1.18
require github.com/vulnerable/package v0.0.0
```

**References**:
- OWASP: https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 27 — Insecure HTTP Method Handling

- **Language**: Go
- **Vulnerability**: Insecure HTTP Method Handling
- **Description**: Allowing unintended HTTP methods on sensitive endpoints.

```
package main
import "net/http"
func handler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("OK"))
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-285: https://cwe.mitre.org/data/definitions/285.html

## Sample 28 — Insecure Context Handling

- **Language**: Go
- **Vulnerability**: Insecure Context Handling
- **Description**: Failing to cancel long-running operations with context.

```
package main
import "context"
func process(ctx context.Context) {
    // No ctx.Done() check
    time.Sleep(time.Hour)
}
```

**References**:
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 29 — Insecure File Descriptor Handling

- **Language**: Go
- **Vulnerability**: Insecure File Descriptor Handling
- **Description**: Using file descriptors without validation.

```
package main
import "os"
func read_fd(fd int) {
    f := os.NewFile(uintptr(fd), "file")
    f.Read(make([]byte, 1024))
}
```

**References**:
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 30 — Insecure Signal Handling

- **Language**: Go
- **Vulnerability**: Insecure Signal Handling
- **Description**: Handling OS signals without proper validation.

```
package main
import "os/signal"
func setup() {
    c := make(chan os.Signal, 1)
    signal.Notify(c)
    <-c
}
```

**References**:
- CWE-479: https://cwe.mitre.org/data/definitions/479.html

## Sample 31 — Insecure Goroutine Safety

- **Language**: Go
- **Vulnerability**: Insecure Goroutine Safety
- **Description**: Accessing shared resources without synchronization.

```
package main
var counter int
func increment() {
    counter++
}
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 32 — Insecure Timeout Configuration

- **Language**: Go
- **Vulnerability**: Insecure Timeout Configuration
- **Description**: Setting infinite timeouts for HTTP clients.

```
package main
import "net/http"
func client() *http.Client {
    return &http.Client{Timeout: 0}
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 33 — Insecure Panic Recovery

- **Language**: Go
- **Vulnerability**: Insecure Panic Recovery
- **Description**: Recovering from panics without proper validation.

```
package main
func process() {
    defer func() { recover() }()
    panic("error")
}
```

**References**:
- CWE-696: https://cwe.mitre.org/data/definitions/696.html

## Sample 34 — Insecure Channel Communication

- **Language**: Go
- **Vulnerability**: Insecure Channel Communication
- **Description**: Using unbuffered channels without proper synchronization.

```
package main
func process(ch chan int) {
    ch <- 42
}
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 35 — Insecure Dynamic Template

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Template
- **Description**: Rendering templates with untrusted input.

```
package main
import "html/template"
func render(tmpl string) {
    template.Parse(tmpl).Execute(os.Stdout, nil)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 36 — Insecure Dynamic Reflection

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Reflection
- **Description**: Using reflection with untrusted input.

```
package main
import "reflect"
func callMethod(obj interface{}, name string) {
    reflect.ValueOf(obj).MethodByName(name).Call([]reflect.Value{})
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-470: https://cwe.mitre.org/data/definitions/470.html

## Sample 37 — Insecure Dynamic Plugin Loading

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Plugin Loading
- **Description**: Loading plugins dynamically with untrusted input.

```
package main
import "plugin"
func loadPlugin(path string) {
    plugin.Open(path)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 38 — Insecure Dynamic Handler Registration

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Handler Registration
- **Description**: Registering HTTP handlers dynamically with user input.

```
package main
import "net/http"
func register(path string) {
    http.HandleFunc(path, func(w http.ResponseWriter, r *http.Request) {})
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 39 — Insecure Dynamic Middleware

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Middleware
- **Description**: Applying middleware dynamically with untrusted handlers.

```
package main
import "net/http"
func applyMiddleware(handler http.HandlerFunc, middleware string) {
    middlewareFunc := reflect.ValueOf(middleware).Call([]reflect.Value{})[0].Interface().(func(http.HandlerFunc) http.HandlerFunc)
    http.HandleFunc("/", middlewareFunc(handler))
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-470: https://cwe.mitre.org/data/definitions/470.html

## Sample 40 — Insecure Dynamic Log Configuration

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Log Configuration
- **Description**: Configuring logging dynamically with untrusted input.

```
package main
import "log"
func setLogOutput(path string) {
    f, _ := os.OpenFile(path, os.O_APPEND, 0644)
    log.SetOutput(f)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html

## Sample 41 — Insecure Dynamic Metric Registration

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Metric Registration
- **Description**: Registering metrics with user-controlled names.

```
package main
import "github.com/prometheus/client_golang/prometheus"
func registerMetric(name string) {
    prometheus.NewCounter(prometheus.CounterOpts{Name: name})
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 42 — Insecure Dynamic Rate Limiter

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Rate Limiter
- **Description**: Configuring rate limiters with user-controlled values.

```
package main
import "golang.org/x/time/rate"
func setLimiter(limit int) {
    rate.NewLimiter(rate.Limit(limit), limit)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-770: https://cwe.mitre.org/data/definitions/770.html

## Sample 43 — Insecure Dynamic Timeout Setting

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Timeout Setting
- **Description**: Setting timeouts dynamically with user-controlled values.

```
package main
import "time"
func setTimeout(d string) time.Duration {
    duration, _ := time.ParseDuration(d)
    return duration
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 44 — Insecure Dynamic Error Handling

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Error Handling
- **Description**: Handling errors with user-controlled logic.

```
package main
import "errors"
func handleError(err string) error {
    return errors.New(err)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-209: https://cwe.mitre.org/data/definitions/209.html

## Sample 45 — Insecure Dynamic Context Propagation

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Context Propagation
- **Description**: Propagating contexts with untrusted values.

```
package main
import "context"
func propagate(ctx context.Context, key, value string) context.Context {
    return context.WithValue(ctx, key, value)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 46 — Insecure Dynamic Cache Configuration

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Cache Configuration
- **Description**: Configuring caches with user-controlled sizes.

```
package main
import "github.com/patrickmn/go-cache"
func setCache(size string) {
    cache.New(time.Duration(size))
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 47 — Insecure Dynamic Tracing

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Tracing
- **Description**: Enabling tracing with user-controlled settings.

```
package main
import "runtime/trace"
func startTrace(path string) {
    f, _ := os.Create(path)
    trace.Start(f)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html

## Sample 48 — Insecure Dynamic Pprof Exposure

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Pprof Exposure
- **Description**: Exposing pprof endpoints without access controls.

```
package main
import "net/http/pprof"
func exposePprof() {
    http.HandleFunc("/debug/pprof/", pprof.Index)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 49 — Insecure Dynamic Health Check

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Health Check
- **Description**: Exposing health check endpoints without access controls.

```
package main
import "net/http"
func healthCheck(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("OK"))
}
func init() {
    http.HandleFunc("/health", healthCheck)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 50 — Insecure Dynamic Expvar Exposure

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Expvar Exposure
- **Description**: Exposing expvar endpoints without access controls.

```
package main
import "expvar"
func exposeExpvar() {
    expvar.Publish("vars", expvar.NewInt("counter"))
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 51 — Insecure Dynamic File Server

- **Language**: Go
- **Vulnerability**: Insecure Dynamic File Server
- **Description**: Serving files with user-controlled paths.

```
package main
import "net/http"
func serveFile(path string) {
    http.FileServer(http.Dir(path))
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 52 — Insecure Dynamic Debug Endpoint

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Debug Endpoint
- **Description**: Exposing debug endpoints without access controls.

```
package main
import "net/http"
func debug(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Debug info"))
}
func init() {
    http.HandleFunc("/debug", debug)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-200: https://cwe.mitre.org/data/definitions/200.html

## Sample 53 — Insecure Dynamic Template Execution

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Template Execution
- **Description**: Executing templates with untrusted input.

```
package main
import "text/template"
func executeTemplate(data string) {
    t, _ := template.New("t").Parse(data)
    t.Execute(os.Stdout, nil)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 54 — Insecure Dynamic File Permission

- **Language**: Go
- **Vulnerability**: Insecure Dynamic File Permission
- **Description**: Setting file permissions with user-controlled values.

```
package main
import "os"
func setPerm(path string, perm string) {
    os.Chmod(path, os.FileMode(perm))
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 55 — Insecure Dynamic HTTP Header

- **Language**: Go
- **Vulnerability**: Insecure Dynamic HTTP Header
- **Description**: Setting HTTP headers with user-controlled values.

```
package main
import "net/http"
func setHeader(w http.ResponseWriter, name, value string) {
    w.Header().Set(name, value)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-113: https://cwe.mitre.org/data/definitions/113.html

## Sample 56 — Insecure Dynamic Signal Handling

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Signal Handling
- **Description**: Handling OS signals with untrusted logic.

```
package main
import "os/signal"
func handleSignal(sig os.Signal, handler func()) {
    c := make(chan os.Signal, 1)
    signal.Notify(c, sig)
    go handler()
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-479: https://cwe.mitre.org/data/definitions/479.html

## Sample 57 — Insecure Dynamic Mutex Creation

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Mutex Creation
- **Description**: Creating mutexes with untrusted initialization.

```
package main
import "sync"
func createMutex() *sync.Mutex {
    return new(sync.Mutex)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A04_2021-Insecure_Design/
- CWE-667: https://cwe.mitre.org/data/definitions/667.html

## Sample 58 — Insecure Dynamic Wait Group

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Wait Group
- **Description**: Using wait groups with untrusted counters.

```
package main
import "sync"
func wait(count int) {
    wg := sync.WaitGroup{}
    wg.Add(count)
    wg.Wait()
}
```

**References**:
- OWASP: https://owasp.org/Top10/A04_2021-Insecure_Design/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 59 — Insecure Dynamic Channel Creation

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Channel Creation
- **Description**: Creating channels with untrusted sizes.

```
package main
func createChannel(size int) chan int {
    return make(chan int, size)
}
```

**References**:
- OWASP: https://owasp.org/Top10/A04_2021-Insecure_Design/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 60 — Insecure Dynamic Pool Creation

- **Language**: Go
- **Vulnerability**: Insecure Dynamic Pool Creation
- **Description**: Creating sync pools with untrusted sizes.

```
package main
import "sync"
func createPool(size int) *sync.Pool {
    return &sync.Pool{New: func() interface{} { return make([]byte, size) }}
}
```

**References**:
- OWASP: https://owasp.org/Top10/A04_2021-Insecure_Design/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html
