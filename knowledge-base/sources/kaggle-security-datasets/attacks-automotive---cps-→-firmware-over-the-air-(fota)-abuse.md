# Automotive / CPS → Firmware Over-The-Air (FOTA) Abuse Attacks

## Injecting Malicious Bootloader via FOTA Proxy

- **Attack Type**: Supply Chain Compromise
- **Target**: IVI Unit / ECU
- **Vulnerability**: Lack of secure boot, firmware signing missing
- **MITRE**: T1557.002
- **Impact**: Persistent backdoor across future updates
- **Tools**: Burp Suite, mitmproxy, Binwalk, Firmware Mod Kit
- **Scenario**: Adversary intercepts FOTA and replaces bootloader firmware with backdoored version to persist across updates.
- **Attack Steps**: 1. Set up a network proxy using mitmproxy to intercept FOTA update traffic from vehicle. 2. Wait for legitimate bootloader update request. 3. Capture firmware and unpack using Binwalk. 4. Modify the bootloader to insert a backdoor shell trigger. 5. Repack firmware and inject it back into the update stream. 6. Allow the vehicle to install the modified bootloader silently.
- **Detection**: Check integrity of bootloaders, monitor FOTA hashes
- **Solution**: Enforce secure boot chain and signed updates
- **Tags**: firmware, mitm, ota, bootloader

## Downgrade-to-Exploit on Infotainment System via OTA

- **Attack Type**: Downgrade Attack
- **Target**: IVI Head Unit
- **Vulnerability**: Weak OTA validation and rollback protection
- **MITRE**: T1609
- **Impact**: RCE on IVI system, user tracking
- **Tools**: curl, CANalyzer, Wireshark
- **Scenario**: Attacker forces OTA system to install older version of infotainment firmware with known RCE flaw.
- **Attack Steps**: 1. Identify current infotainment firmware version and check public CVEs. 2. Intercept OTA request using CANalyzer and redirect to fake server. 3. Serve an older vulnerable firmware version via local HTTP server. 4. Exploit infotainment RCE once downgraded. 5. Maintain control via remote shell or hidden app.
- **Detection**: Monitor firmware version changes, check hash mismatch
- **Solution**: Block downgrades, validate update chains
- **Tags**: downgrade, infotainment, ota, rce

## Exploiting OTA Configuration Server Leak

- **Attack Type**: API Abuse
- **Target**: Telematics Cloud / OTA Backend
- **Vulnerability**: Misconfigured OTA API
- **MITRE**: T1190
- **Impact**: Remote firmware overwrite
- **Tools**: Postman, nmap, VIN decoder
- **Scenario**: Cloud OTA config server exposes unsecured endpoints, allowing attacker to push updates to targeted VINs.
- **Attack Steps**: 1. Discover OTA configuration server via recon or leaked docs. 2. Use nmap to identify open APIs. 3. Query vehicle configuration using VIN through exposed endpoint. 4. Craft custom update manifest pointing to attacker-controlled firmware. 5. Trigger update on target vehicle remotely.
- **Detection**: API access logs, VIN-specific tracking
- **Solution**: Lock down OTA backend endpoints, authenticate VIN update requests
- **Tags**: ota-cloud, api, vin, firmware-injection

## Exploiting Lack of Signature Validation in Emergency ECUs

- **Attack Type**: Firmware Tampering
- **Target**: Emergency Control Units
- **Vulnerability**: No signature check in critical ECUs
- **MITRE**: T1556.001
- **Impact**: Compromised passenger safety systems
- **Tools**: Ghidra, Binwalk, UDS Tools
- **Scenario**: Attackers modify emergency ECU (e.g., airbag or brake module) firmware during FOTA due to lack of cryptographic signatures.
- **Attack Steps**: 1. Capture firmware update destined for safety-critical ECU using diagnostic tap. 2. Unpack and analyze using Binwalk/Ghidra. 3. Modify logic to disable functions (e.g., airbag deployment trigger). 4. Repackage and push through a fake OTA update channel. 5. Wait for in-vehicle installation and observe safety system disabled.
- **Detection**: CRC mismatch alert if implemented, CAN traffic drop
- **Solution**: Mandate signed updates on all ECUs
- **Tags**: uds, airbag-ecu, ota-abuse, ghidra

## Simulating Fake OTA Update Notifications via IVI

- **Attack Type**: Social Engineering
- **Target**: IVI Interface
- **Vulnerability**: Weak UI validation, USB auto-run enabled
- **MITRE**: T1204.002
- **Impact**: Firmware override via driver interaction
- **Tools**: Qt Creator, Android Auto Exploit Kit
- **Scenario**: Fake OTA pop-up is rendered on the infotainment system to trick the driver into allowing rogue firmware installation via USB.
- **Attack Steps**: 1. Reverse-engineer IVI system's UI rendering using Qt-based frameworks. 2. Craft a fake "Update Now" pop-up that mimics OEM design. 3. Deliver payload through Android Auto connection or USB drive. 4. Wait for driver to click update. 5. Execute malicious firmware update logic from connected drive.
- **Detection**: Monitor user-triggered updates, block unsigned USB updates
- **Solution**: Disable USB firmware flashing by default
- **Tags**: infotainment, usb-hack, social-engineering, fota

