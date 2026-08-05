# Automotive / Cyber-Physical Systems → Firmware Over-The-Air (FOTA) Abuse Attacks

## Fake FOTA Update via MiTM

- **Attack Type**: Man-in-the-Middle (MitM)
- **Target**: ECU / Telematics Control Unit
- **Vulnerability**: Insecure communication channel, lack of integrity checks
- **MITRE**: T1557
- **Impact**: ECU compromise, remote control, persistence
- **Tools**: mitmproxy, Burp Suite, Scapy
- **Scenario**: Attacker intercepts FOTA traffic between cloud server and car ECU to inject a fake firmware update.
- **Attack Steps**: 1. Set up a rogue Wi-Fi or cellular base station to force the vehicle to connect.2. Capture and analyze OTA update request from the vehicle to the cloud.3. Create a malicious firmware binary mimicking a legitimate update structure.4. Use mitmproxy or custom script to intercept and replace the firmware update payload during transit.5. Observe the ECU applying the fake firmware, which now contains backdoors.
- **Detection**: Network traffic anomalies, checksum mismatch
- **Solution**: Enforce TLS with cert pinning, sign firmware updates
- **Tags**: mitm, OTA, ECU, FOTA

## Exploiting Unsigned OTA Update

- **Attack Type**: Firmware Injection
- **Target**: ECU
- **Vulnerability**: Lack of firmware signature enforcement
- **MITRE**: T1601
- **Impact**: Root access on ECU, long-term persistence
- **Tools**: Ghidra, Binwalk, Custom CAN tools
- **Scenario**: An adversary pushes a firmware image without signature validation onto the ECU.
- **Attack Steps**: 1. Reverse engineer the firmware update format using Ghidra and Binwalk.2. Repack a modified firmware payload (e.g., with debug shell enabled).3. Connect to vehicle’s telematics system using diagnostic port or remote channel.4. Push the modified firmware via standard update method.5. The ECU accepts and installs the unsigned payload, enabling further exploitation.
- **Detection**: No cryptographic validation logs
- **Solution**: Mandate digital signature checks pre-installation
- **Tags**: unsigned update, reverse engineering

## Downgrade Attack on FOTA System

- **Attack Type**: Downgrade Exploitation
- **Target**: ECU / Gateway
- **Vulnerability**: No version control or downgrade protection
- **MITRE**: T1600
- **Impact**: Allows known exploits, disables patches
- **Tools**: Custom CAN tools, PyUds
- **Scenario**: Pushes an outdated firmware version known to be vulnerable, bypassing new security mechanisms.
- **Attack Steps**: 1. Identify a previously leaked or downloaded older firmware version.2. Check for unpatched vulnerabilities in that version.3. Prepare OTA delivery mechanism via UDS or network interface.4. Push the downgrade package by mimicking a valid update signal.5. Post-downgrade, exploit the known CVEs or backdoors.
- **Detection**: Compare firmware hashes, monitor update logs
- **Solution**: Block older version installations at bootloader
- **Tags**: downgrade attack, CVE replay

## OTA via Fake Telematics Server

- **Attack Type**: Server Spoofing
- **Target**: Telematics Unit / ECU
- **Vulnerability**: DNS spoofing, server impersonation
- **MITRE**: T1557.001
- **Impact**: Full ECU takeover via fake OTA path
- **Tools**: DNS Spoofing, FakeAP, Flask
- **Scenario**: Emulates the cloud update server to push arbitrary firmware
- **Attack Steps**: 1. Use DNS spoofing to resolve vehicle’s update request to fake server IP.2. Spin up a fake OTA server using Flask to respond with malicious firmware.3. Craft firmware to match expected checksum but contain malware.4. Vehicle accepts and installs update believing it came from original server.5. Malicious firmware activates backdoor or modifies CAN logic.
- **Detection**: DNS logs, firmware checksums
- **Solution**: Enforce cert pinning and update source verification
- **Tags**: OTA spoofing, server mimicry

## Manipulating OTA Schedule via Diagnostic Commands

- **Attack Type**: Diagnostic Misuse
- **Target**: ECU / TCU
- **Vulnerability**: UDS abuse, config manipulation
- **MITRE**: T1601.001
- **Impact**: Remote code execution, configuration hijack
- **Tools**: PyUds, CANoe
- **Scenario**: Attacker uses UDS to force immediate OTA pull from rogue endpoint.
- **Attack Steps**: 1. Gain local or remote access to vehicle’s diagnostics.2. Send UDS 0x31 command to trigger manual OTA pull.3. Modify internal config to set update server URL to malicious one.4. ECU pulls update from rogue server and installs malicious firmware.5. Attacker gains root shell or persistence mechanism.
- **Detection**: Audit UDS commands, config changes
- **Solution**: Restrict UDS write access, audit firmware sources
- **Tags**: OTA config, UDS, diagnostics

## Exploiting OTA Delta Patch Merging

- **Attack Type**: Patch Injection
- **Target**: Firmware Merge Utility
- **Vulnerability**: Insecure merge logic
- **MITRE**: T1565
- **Impact**: Logic tampering, bypassing security
- **Tools**: DiffTools, Ghidra
- **Scenario**: Modify OTA delta patch to alter functions during merge.
- **Attack Steps**: 1. Download original firmware and recent OTA delta patch.2. Analyze delta structure and how merging occurs on device.3. Inject new logic into delta file (e.g., disable auth check).4. Upload the manipulated delta patch during OTA cycle.5. ECU applies delta and incorporates attacker’s logic.
- **Detection**: Monitor function changes during OTA
- **Solution**: Use strong delta signing and verification
- **Tags**: delta patch, FOTA merge

## OTA URL Injection via Mobile App API

- **Attack Type**: API Exploitation
- **Target**: Mobile Telematics App / ECU
- **Vulnerability**: Weak API validation
- **MITRE**: T1601.003
- **Impact**: Compromised firmware via API abuse
- **Tools**: Burp Suite, Postman
- **Scenario**: Mobile app APIs allow attacker to alter the firmware update source.
- **Attack Steps**: 1. Intercept traffic between mobile app and backend using Burp.2. Locate firmwareUpdate endpoint and parameters.3. Modify the update source field to attacker-controlled URL.4. Backend accepts change and relays new firmware source to vehicle.5. Vehicle fetches and installs attacker’s firmware.
- **Detection**: Monitor unusual update sources
- **Solution**: Harden APIs, block arbitrary URLs
- **Tags**: mobile API abuse, OTA

## Local USB-Based Firmware Override

- **Attack Type**: Physical Exploitation
- **Target**: Infotainment / TCU
- **Vulnerability**: Unrestricted USB update logic
- **MITRE**: T1200
- **Impact**: Firmware hijack via physical media
- **Tools**: USB Analyzer, Binwalk
- **Scenario**: Physically connected USB allows OTA override and firmware replacement.
- **Attack Steps**: 1. Access vehicle infotainment or TCU USB port.2. Insert specially crafted USB containing firmware override.3. File structure mimics OTA update.4. Device auto-triggers firmware loading via USB.5. Compromised firmware installs without cloud check.
- **Detection**: Monitor USB logs, restrict bootloader mode
- **Solution**: Require signed USB updates, whitelist media
- **Tags**: USB OTA, physical attack

## FOTA Abuse Using SIM Swap Attack

- **Attack Type**: SIM Swap
- **Target**: TCU / SIM Card
- **Vulnerability**: Cellular identity abuse
- **MITRE**: T1657
- **Impact**: OTA identity spoofing, remote persistence
- **Tools**: SIM Cloning Tools
- **Scenario**: Replace SIM tied to vehicle, register rogue OTA service.
- **Attack Steps**: 1. Clone vehicle’s SIM or perform social engineering to port number.2. Register vehicle to attacker’s OTA backend via cellular channel.3. Vehicle receives firmware update notifications from fake OTA.4. Install malicious firmware remotely.5. Use firmware to enable CAN remote access.
- **Detection**: SIM change alerts, IMSI tracking
- **Solution**: Use eSIM with certificate locking
- **Tags**: SIM OTA abuse, cellular

## Race Condition in OTA Installer

- **Attack Type**: Race Condition
- **Target**: OTA Firmware Installer
- **Vulnerability**: Race condition in write flow
- **MITRE**: T1203
- **Impact**: Bypasses integrity check, stealth firmware
- **Tools**: Reverse Engineering Tools
- **Scenario**: Exploit timing issues in installer to overwrite post-verification
- **Attack Steps**: 1. Analyze how firmware is stored and verified before install.2. Introduce race condition by timing payload overwrite during storage.3. Verification passes, but overwritten segment installs post-check.4. Inject malicious logic in the race window.5. Achieve stealth firmware tampering.
- **Detection**: Compare written vs verified hash
- **Solution**: Lock firmware storage between verification and write
- **Tags**: OTA logic bug, race

## Rogue FOTA Server Setup

- **Attack Type**: Fake Update Injection
- **Target**: Telematics Unit
- **Vulnerability**: Lack of server authentication
- **MITRE**: T1557.002
- **Impact**: Full remote control, long-term persistence
- **Tools**: mitmproxy, Burp Suite, custom FOTA emulator
- **Scenario**: Attacker spins up a malicious OTA server to deliver trojaned updates
- **Attack Steps**: 1. Identify the FOTA update mechanism used by the target vehicle (e.g., over HTTPS, MQTT, or proprietary TCP protocols). 2. Set up a rogue server mimicking the legitimate OEM FOTA backend with the same domain structure and expected endpoints. 3. Use DNS spoofing or ARP poisoning to redirect traffic from the real update server to the attacker-controlled one. 4. Host a modified firmware with a backdoor or malicious payload. 5. Allow the update process to complete successfully from the rogue server. 6. The malicious firmware is now installed, allowing attacker control or telemetry leak.
- **Detection**: Monitor DNS requests and validate firmware origin
- **Solution**: Use mutual TLS, hardcoded server pins, and update signature validation
- **Tags**: FOTA, Telematics, MiTM, Rogue Server

## API Key Abuse in OTA Backend

- **Attack Type**: Unsigned Update Deployment
- **Target**: Backend OTA System
- **Vulnerability**: Insecure API, No signing check
- **MITRE**: T1552.001
- **Impact**: Widespread fleet compromise
- **Tools**: Postman, HTTP Toolkit
- **Scenario**: Attacker gains leaked API credentials for backend
- **Attack Steps**: 1. Search for exposed API keys via GitHub dorks or through reverse engineering mobile companion apps. 2. Use the stolen API key to access OTA endpoints without proper authorization. 3. Prepare a modified firmware file and upload it via the API. 4. Push update notifications to enrolled vehicles. 5. The vehicles begin downloading and installing the unsigned, malicious firmware.
- **Detection**: Monitor update logs and API access patterns
- **Solution**: Rotate API keys, enforce firmware signature checks
- **Tags**: OTA Abuse, API Misuse, Key Theft

## Outdated Bootloader Trick

- **Attack Type**: Firmware Downgrade Attack
- **Target**: ECU / Infotainment
- **Vulnerability**: No rollback protection
- **MITRE**: T1601.001
- **Impact**: Re-opened old exploits
- **Tools**: CANape, JTAG debugger
- **Scenario**: Older bootloaders don’t verify signatures
- **Attack Steps**: 1. Reverse engineer the firmware or access leaked documentation to learn the bootloader's version behavior. 2. Prepare an older, known-vulnerable firmware version. 3. Modify OTA manifest to claim higher compatibility. 4. Upload to car using standard OTA method or via SD card/USB interface. 5. Bootloader loads the old firmware without proper validation. 6. Exploit known vulnerability in that version.
- **Detection**: Audit bootloader versions, hash diff of updates
- **Solution**: Enforce rollback protection and fuse burning
- **Tags**: Downgrade, Bootloader, FOTA, Legacy

## Signed Firmware Staging Exploit

- **Attack Type**: Unsigned Update Deployment
- **Target**: IVI / Gateway ECU
- **Vulnerability**: Delayed integrity verification
- **MITRE**: T1601.002
- **Impact**: Execution of tampered firmware
- **Tools**: Firmware unpacker, Static analysis tools
- **Scenario**: Firmware check is deferred till post-install
- **Attack Steps**: 1. Analyze OEM firmware update logic to locate at which point signature verification occurs. 2. Identify systems where the validation occurs after flash (not pre-verify). 3. Push a malicious firmware that passes structural checks but includes payloads that modify system post-install. 4. System installs firmware and boots into the compromised environment.
- **Detection**: Inspect logs during and after updates
- **Solution**: Move signature check before install, add runtime attestation
- **Tags**: Firmware, Validation Bypass, Logic Flaw

## Compromised Companion App Updates

- **Attack Type**: Fake Update Injection
- **Target**: Mobile app + Cloud + Car
- **Vulnerability**: No validation of firmware origin
- **MITRE**: T1554
- **Impact**: Attack via mobile-to-car path
- **Tools**: Apktool, Frida, Burp Suite
- **Scenario**: Mobile app delivers firmware indirectly
- **Attack Steps**: 1. Decompile the vehicle's companion mobile app using Apktool or jadx. 2. Identify the endpoint or API that triggers firmware update requests from the phone to the cloud. 3. Modify the APK to reroute this request to an attacker-controlled firmware server. 4. Sign and distribute the trojaned app (e.g., via phishing or 3rd party stores). 5. Victim installs the app, which now pushes malicious firmware to their vehicle.
- **Detection**: Check APK hashes and app permissions
- **Solution**: Use Play Protect, validate firmware chain in backend
- **Tags**: Mobile-OTA Chain, APK Injection, FOTA

## Firmware Pre-Image Tampering

- **Attack Type**: Fake Update Injection
- **Target**: IVI / TCU
- **Vulnerability**: Weak crypto boundaries
- **MITRE**: T1553.003
- **Impact**: Malicious firmware execution
- **Tools**: openssl, Firmware packer
- **Scenario**: Malicious image built with correct signature
- **Attack Steps**: 1. Capture the legitimate signed firmware update file. 2. Understand the file format and its cryptographic structure. 3. Reconstruct the image with manipulated content but preserving header and checksum data. 4. Send this image via spoofed OTA process. 5. Because signature is calculated on header, malicious code in payload bypasses check.
- **Detection**: Binary diffing of firmware pre-post
- **Solution**: Cryptographic fix, full-image hashing
- **Tags**: FOTA, Cryptographic Abuse, Signing

## Overwrite-Only Update Abuse

- **Attack Type**: Unsigned Update Deployment
- **Target**: Flash Partition
- **Vulnerability**: Misuse of delta/partial updates
- **MITRE**: T1601
- **Impact**: Persistent system alteration
- **Tools**: Flash memory toolkits, Reverse engineering
- **Scenario**: Partial updates overwrite security checks
- **Attack Steps**: 1. Reverse the firmware’s update process and file system format. 2. Create a payload that targets only certain regions of flash (e.g., overwrite config or startup scripts). 3. Deploy this partial update during an official OTA session. 4. Bypass signature validation due to segment-only targeting. 5. Modify boot behavior or telemetry logic.
- **Detection**: Monitor flash diff at binary level
- **Solution**: Secure delta update logic with hashing
- **Tags**: OTA, Flash Patch, Config Tamper

## Firmware Swap Attack via SD Slot

- **Attack Type**: Fake Update Injection
- **Target**: Infotainment System
- **Vulnerability**: User-initiated SD updates unvalidated
- **MITRE**: T1204
- **Impact**: Privilege gain, malware install
- **Tools**: Binwalk, Custom Firmware Builder
- **Scenario**: User loads attacker firmware via SD
- **Attack Steps**: 1. Social engineer the target into inserting an SD card with "urgent firmware patch." 2. The SD contains malicious firmware that appears visually identical to OEM. 3. System auto-loads or prompts user to update. 4. Car accepts firmware due to weak or no signature check. 5. Upon reboot, attacker gains persistent control.
- **Detection**: Monitor manual update actions
- **Solution**: Restrict SD-based updates, require signed hashes
- **Tags**: FOTA, SD Injection, User Trickery

## Reuse of Signed Test Firmware

- **Attack Type**: Unsigned Update Deployment
- **Target**: Internal Test Firmware
- **Vulnerability**: Reuse of insecure builds
- **MITRE**: T1555
- **Impact**: Debug mode activation
- **Tools**: Ghidra, Firmware extractor
- **Scenario**: Test builds signed but not secure
- **Attack Steps**: 1. Leak or access a signed internal test firmware used during vehicle QA. 2. Identify vulnerabilities or debug backdoors left in place. 3. Upload it to a production car via update service. 4. Since it is signed, the car accepts it without question. 5. Attacker gains debug shell or control access.
- **Detection**: Monitor firmware versioning & origins
- **Solution**: Never sign test builds with production keys
- **Tags**: Dev Backdoors, Debug Firmware, QA Lapses

## Multi-Firmware Chain Hijack

- **Attack Type**: Firmware Downgrade Attack
- **Target**: Modular Firmware Stack
- **Vulnerability**: Weak version dependency validation
- **MITRE**: T1601
- **Impact**: Persistence through version misalignment
- **Tools**: Hex editor, Version Spoofing Tool
- **Scenario**: Multiple chained firmwares allow nested exploit
- **Attack Steps**: 1. Analyze the firmware hierarchy (e.g., base, middleware, apps). 2. Downgrade only one component (e.g., the base firmware), keeping others updated. 3. Exploit the now mismatched compatibility and known bug in downgraded version. 4. Achieve arbitrary behavior or persistence. 5. Other components function normally, hiding the exploit.
- **Detection**: Audit firmware dependency trees
- **Solution**: Use strong versioning and inter-signature chaining
- **Tags**: FOTA, Modular Downgrade, Layered Attack

## Tampering OTA Proxy Server

- **Attack Type**: Fake Update Injection
- **Target**: Connected Cars
- **Vulnerability**: Insecure OTA infrastructure
- **MITRE**: T1557.001 (Man-in-the-Middle: DNS)
- **Impact**: Persistent control over vehicle ECUs
- **Tools**: Burp Suite, DNSChef, FakeDNS
- **Scenario**: An attacker compromises the OTA proxy or CDN cache server to distribute malicious firmware updates to multiple cars.
- **Attack Steps**: 1. Identify the OTA proxy or CDN server used for firmware distribution by analyzing vehicle network traffic.2. Set up a rogue DNS server to redirect OTA requests to an attacker-controlled server.3. Clone the legitimate update page structure and host a fake firmware update containing malware.4. When the car checks for updates, it fetches and installs the malicious firmware, believing it's genuine.5. This grants persistent backdoor access to critical ECUs.
- **Detection**: Monitor DNS resolution and OTA sources
- **Solution**: Use pinned certificates, DNSSEC, and integrity checks
- **Tags**: FOTA, MiTM, OTA Proxy

## Intercepting Firmware via Public Wi-Fi

- **Attack Type**: Fake Update Injection
- **Target**: IVI / Telematics
- **Vulnerability**: Lack of encrypted OTA transport
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Covert access via rogue firmware
- **Tools**: EvilAP, SSLstrip, Wireshark
- **Scenario**: A vehicle connected to free Wi-Fi at a dealership is fed a spoofed firmware update via a fake captive portal.
- **Attack Steps**: 1. Set up a fake Wi-Fi hotspot near the dealership with the same SSID as the real network.2. Capture the OTA update traffic using SSLstrip or DNS spoofing tools.3. Replace the firmware binary in transit with a malicious payload.4. The vehicle unknowingly downloads and installs the backdoored firmware.5. Attacker gains hidden remote access to infotainment or telematics systems.
- **Detection**: Detect rogue APs, validate firmware hash
- **Solution**: Always use HTTPS and pinned certs for OTA
- **Tags**: Wi-Fi Spoof, OTA, SSLstrip

## Exploiting Weak Firmware Storage Paths

- **Attack Type**: Unsigned Update Deployment
- **Target**: IVI Systems
- **Vulnerability**: No validation of file integrity
- **MITRE**: T1601.001 (Modify System Partition)
- **Impact**: Silent compromise of infotainment
- **Tools**: Android Debug Bridge, File Explorer
- **Scenario**: The vehicle stores update files in unprotected local storage that can be tampered with before installation.
- **Attack Steps**: 1. Use physical access or ADB to browse the filesystem of the IVI unit.2. Locate where OTA firmware packages are temporarily stored.3. Replace the legit update with a tampered one that mimics the same filename and metadata.4. When the update process is triggered, the malicious firmware is installed without signature validation.5. Malicious modules now persist across reboots.
- **Detection**: Audit firmware file paths and hashes
- **Solution**: Enforce signature check before execution
- **Tags**: Local Abuse, Firmware Path

## Replay of Signed But Expired Updates

- **Attack Type**: Firmware Downgrade
- **Target**: Engine ECU
- **Vulnerability**: No anti-downgrade protection
- **MITRE**: T1601 (Modify System Image)
- **Impact**: Reintroduce known vulnerabilities
- **Tools**: mitmproxy, Archive.org, Custom Scripts
- **Scenario**: The attacker replays an old signed firmware update which contains known vulnerabilities.
- **Attack Steps**: 1. Capture an old signed firmware update from OTA logs or backups.2. Use mitmproxy to intercept the car's update request and serve the archived version.3. Since the firmware is signed but outdated, the vehicle may accept and downgrade.4. Attacker now re-introduces known CVEs into the system.5. Exploits those bugs to gain full control over the ECU.
- **Detection**: Log firmware versioning and verify timestamps
- **Solution**: Use monotonic version counters and anti-rollback
- **Tags**: Downgrade, CVE Reuse

## Over-The-Air Bootloader Corruption

- **Attack Type**: Fake Update Injection
- **Target**: ECUs
- **Vulnerability**: Bootloader trust not validated
- **MITRE**: T1495 (Firmware Corruption)
- **Impact**: Permanent bricking or debug access
- **Tools**: Custom Bootloader Exploits, JTAG Debuggers
- **Scenario**: The attacker injects a malicious firmware that also corrupts the bootloader logic, preventing recovery.
- **Attack Steps**: 1. Reverse engineer the firmware update format and embed code to corrupt bootloader flags.2. Craft the update to pass format checks but cause logical damage.3. Inject via MiTM or rogue update server.4. After installation, the ECU fails to boot or is stuck in an insecure debug mode.5. Attacker gains low-level access or causes permanent DoS.
- **Detection**: Monitor boot flags and update logs
- **Solution**: Use secure bootloader with rollback protection
- **Tags**: ECU DoS, Bootloader Hack

## Cloud API Overwrite of Firmware Schedule

- **Attack Type**: Unsigned Update Deployment
- **Target**: Fleet Vehicles
- **Vulnerability**: Poor cloud auth, missing firmware validation
- **MITRE**: T1585.002 (Compromise Software Dependencies)
- **Impact**: Supply chain takeover of firmware delivery
- **Tools**: Burp Suite, Postman, JWT Cracker
- **Scenario**: Abusing misconfigured telematics backend to overwrite scheduled firmware jobs with attacker-supplied ones.
- **Attack Steps**: 1. Enumerate cloud API calls using a valid account token (ex: from mobile app).2. Identify endpoints that schedule firmware deployment jobs to fleets.3. Craft a POST request with attacker-supplied firmware URL.4. Submit it with forged or expired JWTs due to missing validation.5. The OTA scheduler now deploys malicious firmware to the vehicle(s).
- **Detection**: Audit cloud logs and API authValidate OTA sources
- **Solution**: Harden API auth and verify firmware at endpoint
- **Tags**: Telematics, API Abuse

## Embedded Backdoor in OTA Loader App

- **Attack Type**: Fake Update Injection
- **Target**: Maintenance Tools
- **Vulnerability**: Unverified binaries in supply chain
- **MITRE**: T1195.002 (Compromise Software Supply Chain)
- **Impact**: Remote backdoor via trusted tools
- **Tools**: Binary Ninja, Ghidra, Compiler
- **Scenario**: The attacker backdoors a third-party firmware loader binary distributed as part of the vehicle's toolchain.
- **Attack Steps**: 1. Download the official OTA loader tool used by service centers.2. Inject a backdoor that executes shell commands when a specific flag is present.3. Replace the loader binary on an insecure distribution channel (ex: FTP or email).4. When used by a technician or tester, the loader uploads firmware but also opens backdoor.5. Attacker now gets remote shell access on service interfaces.
- **Detection**: Hash validate tools, monitor behavior
- **Solution**: Use secure software distribution practices
- **Tags**: Loader, Service Abuse

## Malicious Firmware in Open Source Repo

- **Attack Type**: Unsigned Update Deployment
- **Target**: Open Source IVI
- **Vulnerability**: Poor code review practices
- **MITRE**: T1195 (Supply Chain Compromise)
- **Impact**: Rootkit via upstream firmware
- **Tools**: Git, CI/CD, Static Analyzer
- **Scenario**: Attacker sneaks malicious code into an open-source firmware repo forked by Tier-1 supplier.
- **Attack Steps**: 1. Identify popular open-source firmware repo used for IVI systems (e.g., AGL Linux).2. Submit a pull request with malicious payload disguised as optimization.3. If accepted without review, it gets built and distributed via OTA in production.4. Firmware now contains rootkits or data exfiltration modules.5. Attacker abuses this insider-style supply chain weakness.
- **Detection**: Conduct secure code reviewsAudit firmware binaries
- **Solution**: Verify every firmware release before deployment
- **Tags**: OSS Supply Chain

## Exploiting Test OTA Endpoint Left Exposed

- **Attack Type**: Unsigned Update Deployment
- **Target**: Developer Cloud Infra
- **Vulnerability**: Forgotten test endpoints
- **MITRE**: T1190 (Exploit Public-Facing Application)
- **Impact**: Silent compromise of production vehicles
- **Tools**: Shodan, curl, OTA API Docs
- **Scenario**: Developers forget to disable a test OTA firmware endpoint that lacks authentication.
- **Attack Steps**: 1. Scan IP ranges for exposed OTA dev/test endpoints using Shodan.2. Send a crafted request with a custom firmware blob.3. Due to lack of authentication, the firmware is accepted and queued for install.4. Targeted vehicles pull from this test endpoint and install backdoored firmware.5. Attacker gains persistent and stealthy control.
- **Detection**: Endpoint scans and API key enforcement
- **Solution**: Remove all non-prod endpoints from public view
- **Tags**: Shodan, Dev Test

## Hash Collision in Firmware Validation

- **Attack Type**: Fake Update Injection
- **Target**: All ECUs
- **Vulnerability**: Use of weak hashing algorithms
- **MITRE**: T1600 (Weaken Integrity Checking)
- **Impact**: Undetected firmware replacement
- **Tools**: HashClash, Custom Collision Tools
- **Scenario**: Malicious firmware is crafted to generate the same hash as legitimate one using hash collision attacks.
- **Attack Steps**: 1. Analyze the firmware update process and determine the hash function used (e.g., MD5/SHA-1).2. Use collision generation tools to create a malicious firmware file with the same hash as the original.3. Replace the original update with the crafted one during OTA transmission.4. The hash check passes, and the vehicle installs the malicious firmware.5. Attacker bypasses basic integrity verification.
- **Detection**: Use strong hash (SHA-256+), enforce signature
- **Solution**: Deprecate MD5/SHA-1 in OTA workflows
- **Tags**: Hash Collisions, Cryptography

