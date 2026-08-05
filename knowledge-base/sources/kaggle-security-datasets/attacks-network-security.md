# Network security Attacks

## DNS Rebinding Attack

- **Attack Type**: Bypass Same-Origin Policy to Access Internal Hosts
- **Target**: Browsers behind NAT or internal net
- **Vulnerability**: Same-origin policy + dynamic DNS trickery
- **MITRE**: T1565.001 – DNS Rebinding
- **Impact**: Internal network access, credential leakage
- **Tools**: DNSRebind, Burp, custom DNS server, rebind-toolkit
- **Scenario**: Attacker tricks the browser into thinking an internal service is part of an external trusted site using dynamic DNS IP changes.
- **Attack Steps**: Step 1: Attacker hosts a malicious webpage or ad that loads in the victim’s browser.Step 2: This page references a subdomain like rebind.attacker.com which points to the attacker’s DNS server.Step 3: When the victim’s browser loads the page, it resolves rebind.attacker.com to an external IP (initially attacker-controlled).Step 4: After initial connection, the attacker changes DNS to point rebind.attacker.com to an internal IP (e.g., 127.0.0.1, 192.168.1.1).Step 5: Browser now thinks the internal IP is the same-origin as attacker site, allowing JavaScript access.Step 6: JavaScript in the page scans internal services (e.g., router admin panel, API server) and sends data back to attacker.Step 7: May expose AWS credentials, NAS dashboards, or printer controls.Step 8: Detection includes watching for internal requests made by browsers to external domains.Step 9: Defend by blocking DNS rebinding via router settings or using DNS servers that validate responses (e.g., Google DNS blocks private IPs).Step 10: Use firewall rules to prevent browser access to local IPs from external domains.
- **Detection**: Watch for external domain loading internal IPs; browser logs and DNS queries
- **Solution**: Disable DNS rebinding in router; enforce internal-only IP access; validate DNS responses
- **Tags**: Web Exploit, DNS Abuse, Internal Discovery

## Redirect to Exploit Server

- **Attack Type**: HTTP Redirect to Malicious Payload Server
- **Target**: Web browsers or auto-update clients
- **Vulnerability**: Trusting HTTP redirect chains or DNS injection
- **MITRE**: T1071.001 – Web Protocol for C2
- **Impact**: Malware delivery, remote access, system compromise
- **Tools**: Bettercap, Responder, custom proxy, Evilgrade, msfvenom
- **Scenario**: Attacker intercepts or injects HTTP redirect responses, pointing victims to exploit servers that deliver malware or browser-based RCE.
- **Attack Steps**: Step 1: Attacker sets up an HTTP server (or proxy) hosting malicious content (e.g., JavaScript, macro payload, Java applet, browser exploit).Step 2: Launches a MITM attack using ARP/DNS spoofing or compromise of an upstream server.Step 3: Modifies the HTTP response headers to include HTTP 302 Redirect pointing to the malicious server (e.g., Location: http://malicious.evil.com or IP address).Step 4: Victim browser follows the redirect automatically and loads the exploit.Step 5: Exploit delivers payload like meterpreter reverse shell, macro-laced document, or browser zero-day.Step 6: Attacker now controls the victim system remotely.Step 7: Can also target update servers, replacing legitimate updates with malware using tools like Evilgrade.Step 8: Detection involves inspecting unexpected HTTP redirects, odd domains in logs, or certificate mismatches.Step 9: Use HTTPS and strict transport security to prevent redirection manipulation.Step 10: Apply egress filtering and browser hardening policies to block access to known bad hosts.
- **Detection**: Monitor DNS and HTTP logs for 302 redirects; inspect for malware servers
- **Solution**: Force HTTPS; block malicious domains; implement DNS filtering and traffic validation
- **Tags**: HTTP Hijack, Redirect, Exploit Delivery

