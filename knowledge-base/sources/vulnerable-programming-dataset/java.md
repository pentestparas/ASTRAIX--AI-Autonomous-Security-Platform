# Vulnerable Code Samples: Java

Secure-code-review training examples (61 samples). Each sample is vulnerable code, the vulnerability class, and references.

## Sample 1 — Insecure Deserialization

- **Language**: Java
- **Vulnerability**: Insecure Deserialization
- **Description**: Deserializing untrusted user input without validation.

```
import java.io.*;
public class Deserialize {
    public Object deserialize(byte[] data) throws Exception {
        ByteArrayInputStream bis = new ByteArrayInputStream(data);
        ObjectInputStream ois = new ObjectInputStream(bis);
        return ois.readObject();
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 2 — Hardcoded Secrets

- **Language**: Java
- **Vulnerability**: Hardcoded Secrets
- **Description**: Embedding API keys directly in source code.

```
public class ApiClient {
    private String apiKey = "12345-abcde-secret";
    public void makeRequest() {}
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 3 — SQL Injection

- **Language**: Java
- **Vulnerability**: SQL Injection
- **Description**: Using string concatenation in SQL queries.

```
import java.sql.*;
public class DbQuery {
    public ResultSet query(Connection conn, String name) throws SQLException {
        Statement stmt = conn.createStatement();
        return stmt.executeQuery("SELECT * FROM users WHERE name = '" + name + "'
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 4 — Insecure Logging

- **Language**: Java
- **Vulnerability**: Insecure Logging
- **Description**: Logging sensitive information without sanitization.

```
import java.util.logging.Logger;
public class LogData {
    private static final Logger LOGGER = Logger.getLogger(LogData.class.getName());
    public void logCredentials(String password) {
        LOGGER.info("Password: " + password);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-532: https://cwe.mitre.org/data/definitions/532.html

## Sample 5 — Command Injection

- **Language**: Java
- **Vulnerability**: Command Injection
- **Description**: Executing system commands with unsanitized input.

```
public class Exec {
    public void run(String cmd) throws Exception {
        Runtime.getRuntime().exec(cmd);
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Command_Injection
- CWE-77: https://cwe.mitre.org/data/definitions/77.html

## Sample 6 — Insecure Randomness

- **Language**: Java
- **Vulnerability**: Insecure Randomness
- **Description**: Using Random class for cryptographic purposes.

```
import java.util.Random;
public class TokenGenerator {
    public int generateToken() {
        return new Random().nextInt();
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 7 — Insecure File Permissions

- **Language**: Java
- **Vulnerability**: Insecure File Permissions
- **Description**: Writing files with permissive permissions.

```
import java.nio.file.*;
public class FileWriter {
    public void writeFile(String path, String data) throws Exception {
        Files.write(Paths.get(path), data.getBytes(), StandardOpenOption.CREATE);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 8 — Insecure TLS Configuration

- **Language**: Java
- **Vulnerability**: Insecure TLS Configuration
- **Description**: Using outdated SSL protocol.

```
import javax.net.ssl.*;
public class SSLConfig {
    public SSLContext getContext() throws Exception {
        return SSLContext.getInstance("SSLv3");
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-326: https://cwe.mitre.org/data/definitions/326.html

## Sample 9 — Insecure XML Parsing

- **Language**: Java
- **Vulnerability**: Insecure XML Parsing
- **Description**: Parsing XML with external entity processing enabled.

```
import javax.xml.parsers.*;
public class XmlParser {
    public Document parse(String xml) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        return dbf.newDocumentBuilder().parse(new InputSource(new StringReader(xml)));
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing
- CWE-611: https://cwe.mitre.org/data/definitions/611.html

## Sample 10 — Insecure Session Management

- **Language**: Java
- **Vulnerability**: Insecure Session Management
- **Description**: Not invalidating session after logout.

```
public class SessionManager {
    public void logout(HttpSession session) {
        // No session.invalidate()
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-613: https://cwe.mitre.org/data/definitions/613.html

## Sample 11 — Insecure File Upload

- **Language**: Java
- **Vulnerability**: Insecure File Upload
- **Description**: Uploading files without validation.

```
import java.io.*;
public class FileUpload {
    public void saveFile(InputStream is, String path) throws IOException {
        Files.copy(is, Paths.get(path));
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- CWE-434: https://cwe.mitre.org/data/definitions/434.html

## Sample 12 — Insecure Deserialization

- **Language**: Java
- **Vulnerability**: Insecure Deserialization
- **Description**: Deserializing untrusted user input without validation.

```
import java.io.*;
public class Deserialize {
    public Object deserialize(byte[] data) throws Exception {
        ByteArrayInputStream bis = new ByteArrayInputStream(data);
        ObjectInputStream ois = new ObjectInputStream(bis);
        return ois.readObject();
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Deserialization_of_untrusted_data
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 13 — Hardcoded Secrets

- **Language**: Java
- **Vulnerability**: Hardcoded Secrets
- **Description**: Embedding API keys directly in source code.

```
public class ApiClient {
    private String apiKey = "12345-abcde-secret";
    public void makeRequest() {}
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-798: https://cwe.mitre.org/data/definitions/798.html

## Sample 14 — SQL Injection

- **Language**: Java
- **Vulnerability**: SQL Injection
- **Description**: Using string concatenation in SQL queries.

```
import java.sql.*;
public class DbQuery {
    public ResultSet query(Connection conn, String name) throws SQLException {
        Statement stmt = conn.createStatement();
        return stmt.executeQuery("SELECT * FROM users WHERE name = '" + name + "'");
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html

## Sample 15 — Insecure Logging

- **Language**: Java
- **Vulnerability**: Insecure Logging
- **Description**: Logging sensitive information without sanitization.

```
import java.util.logging.Logger;
public class LogData {
    private static final Logger LOGGER = Logger.getLogger(LogData.class.getName());
    public void logCredentials(String password) {
        LOGGER.info("Password: " + password);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-532: https://cwe.mitre.org/data/definitions/532.html

## Sample 16 — Command Injection

- **Language**: Java
- **Vulnerability**: Command Injection
- **Description**: Executing system commands with unsanitized input.

```
public class Exec {
    public void run(String cmd) throws Exception {
        Runtime.getRuntime().exec(cmd);
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Command_Injection
- CWE-77: https://cwe.mitre.org/data/definitions/77.html

## Sample 17 — Insecure Randomness

- **Language**: Java
- **Vulnerability**: Insecure Randomness
- **Description**: Using Random class for cryptographic purposes.

```
import java.util.Random;
public class TokenGenerator {
    public int generateToken() {
        return new Random().nextInt();
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-330: https://cwe.mitre.org/data/definitions/330.html

## Sample 18 — Insecure File Permissions

- **Language**: Java
- **Vulnerability**: Insecure File Permissions
- **Description**: Writing files with permissive permissions.

```
import java.nio.file.*;
public class FileWriter {
    public void writeFile(String path, String data) throws Exception {
        Files.write(Paths.get(path), data.getBytes(), StandardOpenOption.CREATE);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-732: https://cwe.mitre.org/data/definitions/732.html

## Sample 19 — Insecure TLS Configuration

- **Language**: Java
- **Vulnerability**: Insecure TLS Configuration
- **Description**: Using outdated SSL protocol.

```
import javax.net.ssl.*;
public class SSLConfig {
    public SSLContext getContext() throws Exception {
        return SSLContext.getInstance("SSLv3");
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-326: https://cwe.mitre.org/data/definitions/326.html

## Sample 20 — Insecure XML Parsing

- **Language**: Java
- **Vulnerability**: Insecure XML Parsing
- **Description**: Parsing XML with external entity processing enabled.

```
import javax.xml.parsers.*;
public class XmlParser {
    public Document parse(String xml) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        return dbf.newDocumentBuilder().parse(new InputSource(new StringReader(xml)));
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing
- CWE-611: https://cwe.mitre.org/data/definitions/611.html

## Sample 21 — Insecure Session Management

- **Language**: Java
- **Vulnerability**: Insecure Session Management
- **Description**: Not invalidating session after logout.

```
public class SessionManager {
    public void logout(HttpSession session) {
        // No session.invalidate()
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
- CWE-613: https://cwe.mitre.org/data/definitions/613.html

## Sample 22 — Insecure File Upload

- **Language**: Java
- **Vulnerability**: Insecure File Upload
- **Description**: Uploading files without validation.

```
import java.io.*;
public class FileUpload {
    public void saveFile(InputStream is, String path) throws IOException {
        Files.copy(is, Paths.get(path));
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
- CWE-434: https://cwe.mitre.org/data/definitions/434.html

## Sample 23 — Insecure Reflection

- **Language**: Java
- **Vulnerability**: Insecure Reflection
- **Description**: Using reflection with unvalidated input.

```
import java.lang.reflect.*;
public class Reflector {
    public void invokeMethod(String methodName, Object obj) throws Exception {
        Method method = obj.getClass().getMethod(methodName);
        method.invoke(obj);
    }
}
```

**References**:
- OWASP: https://owasp.org/www-community/attacks/Reflected_Code_Injection
- CWE-470: https://cwe.mitre.org/data/definitions/470.html

## Sample 24 — Insecure Thread Safety

- **Language**: Java
- **Vulnerability**: Insecure Thread Safety
- **Description**: Using non-thread-safe collection in concurrent environment.

```
import java.util.ArrayList;
public class SharedData {
    private ArrayList<String> list = new ArrayList<>();
    public void add(String item) {
        list.add(item);
    }
}
```

**References**:
- CWE-362: https://cwe.mitre.org/data/definitions/362.html

## Sample 25 — Insecure Resource Access

- **Language**: Java
- **Vulnerability**: Insecure Resource Access
- **Description**: Accessing resources without proper authorization checks.

```
public class ResourceAccess {
    public String getResource(String id) {
        return loadResource(id);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 26 — Insecure JNI Usage

- **Language**: Java
- **Vulnerability**: Insecure JNI Usage
- **Description**: Calling native code without proper validation, risking memory corruption.

```
public class NativeCall {
    static { System.loadLibrary('native'); }
    public native void process(String input);
}
```

**References**:
- OWASP: https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/
- CWE-111: https://cwe.mitre.org/data/definitions/111.html

## Sample 27 — Insecure Object Cloning

- **Language**: Java
- **Vulnerability**: Insecure Object Cloning
- **Description**: Cloning objects without validating contents.

```
public class Cloner implements Cloneable {
    public Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/
- CWE-494: https://cwe.mitre.org/data/definitions/494.html

## Sample 28 — Insecure Class Loading

- **Language**: Java
- **Vulnerability**: Insecure Class Loading
- **Description**: Loading classes dynamically from untrusted sources.

```
public class Loader {
    public Class<?> load(String name) throws Exception {
        return Class.forName(name);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-470: https://cwe.mitre.org/data/definitions/470.html

## Sample 29 — Insecure Resource Locking

- **Language**: Java
- **Vulnerability**: Insecure Resource Locking
- **Description**: Using locks without proper timeout, risking deadlocks.

```
import java.util.concurrent.locks.*;
public class Locker {
    private ReentrantLock lock = new ReentrantLock();
    public void process() {
        lock.lock();
        // No timeout
    }
}
```

**References**:
- CWE-833: https://cwe.mitre.org/data/definitions/833.html

## Sample 30 — Insecure Dynamic Proxy

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Proxy
- **Description**: Creating dynamic proxies with unvalidated handlers.

```
import java.lang.reflect.*;
public class ProxyCreator {
    public Object createProxy(Object target, InvocationHandler handler) {
        return Proxy.newProxyInstance(target.getClass().getClassLoader(), target.getClass().getInterfaces(), handler);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-470: https://cwe.mitre.org/data/definitions/470.html

## Sample 31 — Insecure Object Serialization

- **Language**: Java
- **Vulnerability**: Insecure Object Serialization
- **Description**: Serializing objects without restricting types.

```
import java.io.*;
public class Serializer {
    public byte[] serialize(Object obj) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(obj);
        return baos.toByteArray();
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/
- CWE-502: https://cwe.mitre.org/data/definitions/502.html

## Sample 32 — Insecure Security Manager

- **Language**: Java
- **Vulnerability**: Insecure Security Manager
- **Description**: Disabling security manager, bypassing checks.

```
public class App {
    public void disableSecurity() {
        System.setSecurityManager(null);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 33 — Insecure Thread Pool Configuration

- **Language**: Java
- **Vulnerability**: Insecure Thread Pool Configuration
- **Description**: Using unbounded thread pool, risking resource exhaustion.

```
import java.util.concurrent.*;
public class ThreadPool {
    public ExecutorService createPool() {
        return Executors.newCachedThreadPool();
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 34 — Insecure Dynamic Annotation

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Annotation
- **Description**: Applying annotations dynamically with user input.

```
import java.lang.annotation.*;
public class Annotator {
    public void apply(String annotation) throws Exception {
        Class.forName(annotation).getAnnotation(Annotation.class);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-470: https://cwe.mitre.org/data/definitions/470.html

## Sample 35 — Insecure Dynamic Permissions

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Permissions
- **Description**: Granting permissions dynamically without validation.

```
import java.security.*;
public class Permissions {
    public void grant(String perm) {
        Permissions p = new Permissions();
        p.add(new Permission(perm) {});
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 36 — Insecure Dynamic Resource Loading

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Resource Loading
- **Description**: Loading resources dynamically with untrusted input.

```
public class ResourceLoader {
    public InputStream load(String path) throws Exception {
        return getClass().getResourceAsStream(path);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 37 — Insecure Dynamic Method Invocation

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Method Invocation
- **Description**: Invoking methods dynamically with untrusted input.

```
import java.lang.reflect.*;
public class Invoker {
    public void invoke(Object obj, String method) throws Exception {
        obj.getClass().getMethod(method).invoke(obj);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-470: https://cwe.mitre.org/data/definitions/470.html

## Sample 38 — Insecure Dynamic Logging Configuration

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Logging Configuration
- **Description**: Configuring logging dynamically with untrusted input.

```
import java.util.logging.*;
public class LoggerConfig {
    public void setLevel(String level) {
        Logger.getLogger('').setLevel(Level.parse(level));
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html

## Sample 39 — Insecure Dynamic Class Path

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Class Path
- **Description**: Modifying classpath dynamically with untrusted input.

```
public class ClassPath {
    public void addPath(String path) throws Exception {
        System.setProperty('java.class.path', path);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 40 — Insecure Dynamic Trust Manager

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Trust Manager
- **Description**: Using custom trust manager without certificate validation.

```
import javax.net.ssl.*;
public class TrustAll implements X509TrustManager {
    public void checkClientTrusted(X509Certificate[] chain, String authType) {}
    public void checkServerTrusted(X509Certificate[] chain, String authType) {}
    public X509Certificate[] getAcceptedIssuers() { return null; }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
- CWE-295: https://cwe.mitre.org/data/definitions/295.html

## Sample 41 — Insecure Dynamic Policy Setting

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Policy Setting
- **Description**: Setting security policies dynamically with untrusted input.

```
import java.security.*;
public class PolicySetter {
    public void setPolicy(String policy) throws Exception {
        Policy.setPolicy((Policy) Class.forName(policy).getDeclaredConstructor().newInstance());
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 42 — Insecure Dynamic Socket Creation

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Socket Creation
- **Description**: Creating sockets with unvalidated hosts.

```
import java.net.*;
public class SocketCreator {
    public Socket create(String host) throws Exception {
        return new Socket(host, 80);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 43 — Insecure Dynamic JMX Registration

- **Language**: Java
- **Vulnerability**: Insecure Dynamic JMX Registration
- **Description**: Registering JMX beans with untrusted input.

```
import javax.management.*;
public class JMXRegistrar {
    public void register(String name, Object bean) throws Exception {
        MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();
        mbs.registerMBean(bean, new ObjectName(name));
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 44 — Insecure Dynamic Executor Service

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Executor Service
- **Description**: Creating executor services with unbounded queues.

```
import java.util.concurrent.*;
public class ExecutorCreator {
    public ExecutorService create() {
        return Executors.newFixedThreadPool(Integer.MAX_VALUE);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-400: https://cwe.mitre.org/data/definitions/400.html

## Sample 45 — Insecure Dynamic URL Connection

- **Language**: Java
- **Vulnerability**: Insecure Dynamic URL Connection
- **Description**: Opening URL connections with untrusted URLs.

```
import java.net.*;
public class URLConnector {
    public void connect(String url) throws Exception {
        new URL(url).openConnection().connect();
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-601: https://cwe.mitre.org/data/definitions/601.html

## Sample 46 — Insecure Dynamic File Handler

- **Language**: Java
- **Vulnerability**: Insecure Dynamic File Handler
- **Description**: Handling files with untrusted paths.

```
import java.io.*;
public class FileHandler {
    public void read(String path) throws Exception {
        new FileInputStream(path).read();
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-22: https://cwe.mitre.org/data/definitions/22.html

## Sample 47 — Insecure Dynamic Class Loader

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Class Loader
- **Description**: Using custom class loaders with untrusted paths.

```
import java.net.*;
public class CustomLoader extends URLClassLoader {
    public CustomLoader(String path) throws Exception {
        super(new URL[]{new URL(path)});
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 48 — Insecure Dynamic RMI Binding

- **Language**: Java
- **Vulnerability**: Insecure Dynamic RMI Binding
- **Description**: Binding RMI objects with untrusted names.

```
import java.rmi.*;
public class RMIBinder {
    public void bind(String name, Remote obj) throws Exception {
        Naming.bind(name, obj);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 49 — Insecure Dynamic LDAP Query

- **Language**: Java
- **Vulnerability**: Insecure Dynamic LDAP Query
- **Description**: Executing LDAP queries with untrusted input.

```
import javax.naming.directory.*;
public class LDAPQuery {
    public void query(String filter) throws Exception {
        DirContext ctx = new InitialDirContext();
        ctx.search("", filter, null);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-90: https://cwe.mitre.org/data/definitions/90.html

## Sample 50 — Insecure Dynamic JNDI Lookup

- **Language**: Java
- **Vulnerability**: Insecure Dynamic JNDI Lookup
- **Description**: Performing JNDI lookups with untrusted input.

```
import javax.naming.*;
public class JNDILookup {
    public Object lookup(String name) throws Exception {
        return new InitialContext().lookup(name);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-91: https://cwe.mitre.org/data/definitions/91.html

## Sample 51 — Insecure Dynamic CORBA Invocation

- **Language**: Java
- **Vulnerability**: Insecure Dynamic CORBA Invocation
- **Description**: Invoking CORBA methods with untrusted input.

```
import org.omg.CORBA.*;
public class CORBAInvoker {
    public void invoke(String method, ORB orb) throws Exception {
        orb.string_to_object(method).invoke(null);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 52 — Insecure Dynamic SAX Parsing

- **Language**: Java
- **Vulnerability**: Insecure Dynamic SAX Parsing
- **Description**: Parsing XML with SAX without validation.

```
import javax.xml.parsers.*;
public class SAXParser {
    public void parse(String xml) throws Exception {
        SAXParserFactory.newInstance().newSAXParser().parse(xml, new DefaultHandler());
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A04_2021-Insecure_Design/
- CWE-611: https://cwe.mitre.org/data/definitions/611.html

## Sample 53 — Insecure Dynamic DOM Parsing

- **Language**: Java
- **Vulnerability**: Insecure Dynamic DOM Parsing
- **Description**: Parsing DOM with untrusted input.

```
import javax.xml.parsers.*;
public class DOMParser {
    public void parse(String xml) throws Exception {
        DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(xml);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A04_2021-Insecure_Design/
- CWE-611: https://cwe.mitre.org/data/definitions/611.html

## Sample 54 — Insecure Dynamic XPath Evaluation

- **Language**: Java
- **Vulnerability**: Insecure Dynamic XPath Evaluation
- **Description**: Evaluating XPath expressions with untrusted input.

```
import javax.xml.xpath.*;
public class XPathEvaluator {
    public Object evaluate(String expr) throws Exception {
        return XPathFactory.newInstance().newXPath().evaluate(expr, doc);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-643: https://cwe.mitre.org/data/definitions/643.html

## Sample 55 — Insecure Dynamic Proxy Creation

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Proxy Creation
- **Description**: Creating proxies with untrusted handlers.

```
import java.lang.reflect.*;
public class ProxyCreator {
    public Object create(Object handler) {
        return Proxy.newProxyInstance(getClass().getClassLoader(), new Class[]{Runnable.class}, (proxy, method, args) -> null);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 56 — Insecure Dynamic JNI Invocation

- **Language**: Java
- **Vulnerability**: Insecure Dynamic JNI Invocation
- **Description**: Invoking JNI methods with untrusted input.

```
public class JNIInvoker {
    public native void invoke(String method);
    static {
        System.loadLibrary("native");
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 57 — Insecure Dynamic Security Manager

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Security Manager
- **Description**: Setting security manager with untrusted policy.

```
public class SecuritySetter {
    public void set(String policy) {
        System.setSecurityManager(new SecurityManager() {
            @Override
            public void checkPermission(Permission perm) {}
        });
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 58 — Insecure Dynamic JMX Invocation

- **Language**: Java
- **Vulnerability**: Insecure Dynamic JMX Invocation
- **Description**: Invoking JMX methods with untrusted input.

```
import javax.management.*;
public class JMXInvoker {
    public void invoke(String name, String method) throws Exception {
        MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();
        mbs.invoke(new ObjectName(name), method, null, null);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-94: https://cwe.mitre.org/data/definitions/94.html

## Sample 59 — Insecure Dynamic Thread Group

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Thread Group
- **Description**: Creating thread groups with untrusted names.

```
public class ThreadGroupCreator {
    public ThreadGroup create(String name) {
        return new ThreadGroup(name);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- CWE-284: https://cwe.mitre.org/data/definitions/284.html

## Sample 60 — Insecure Dynamic Resource Bundle

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Resource Bundle
- **Description**: Loading resource bundles with untrusted names.

```
import java.util.*;
public class BundleLoader {
    public ResourceBundle load(String name) {
        return ResourceBundle.getBundle(name);
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE-829: https://cwe.mitre.org/data/definitions/829.html

## Sample 61 — Insecure Dynamic Log Manager

- **Language**: Java
- **Vulnerability**: Insecure Dynamic Log Manager
- **Description**: Configuring log managers with untrusted settings.

```
import java.util.logging.*;
public class LogConfigurer {
    public void configure(String config) {
        LogManager.getLogManager().readConfiguration(new ByteArrayInputStream(config.getBytes()));
    }
}
```

**References**:
- OWASP: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
- CWE-778: https://cwe.mitre.org/data/definitions/778.html
