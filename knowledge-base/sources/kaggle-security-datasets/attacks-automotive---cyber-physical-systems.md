# Automotive / Cyber-Physical Systems Attacks

## Physical OBD-II Port Sniffing

- **Attack Type**: Physical Access
- **Target**: Car/ECU
- **Vulnerability**: Unauthenticated diagnostic port access
- **MITRE**: TA0001: Initial Access
- **Impact**: Full visibility into in-vehicle network traffic
- **Tools**: CANtact, SavvyCAN, USB2CAN, ELM327
- **Scenario**: The attacker gains physical access to a parked vehicle and connects a CAN bus sniffing device via the OBD-II port to capture traffic.
- **Attack Steps**: 1. Locate the vehicle's OBD-II port (usually under the steering wheel). 2. Plug in a CAN interface device (e.g., CANtact, USB2CAN). 3. Connect to a laptop and launch SavvyCAN. 4. Select the interface and start capturing CAN frames. 5. Let the capture run during normal vehicle operation. 6. Identify repeating IDs and correlate to functions. 7. Save logs for offline analysis. 8. Analyze to discover diagnostic or control commands.
- **Detection**: Detection of foreign devices on OBD-II port
- **Solution**: Lock OBD port or require ignition authentication
- **Tags**: OBD-II, CAN sniffing, physical access

## Inject CAN Frames via OBD-II

- **Attack Type**: Physical Access
- **Target**: Car systems
- **Vulnerability**: Unfiltered CAN injection
- **MITRE**: T1543.003: Create or Modify System Process
- **Impact**: Unauthorized vehicle manipulation
- **Tools**: USB2CAN, SavvyCAN, cansend
- **Scenario**: The attacker injects crafted CAN messages into the vehicle's network through the OBD-II port to control specific vehicle functions.
- **Attack Steps**: 1. Connect USB2CAN to the OBD-II port. 2. Launch a Linux terminal and bring up the CAN interface. 3. Use cansend to transmit a known frame (e.g., door unlock message). 4. Observe changes in the vehicle (e.g., lights blink, doors unlock). 5. Repeat with other IDs found from prior sniffing. 6. Log reactions to identify control surfaces. 7. Modify timing or payload to bypass basic IDS. 8. Save script for automation.
- **Detection**: Logging of unauthorized frame activity
- **Solution**: Use CAN filters, gateway segmentation
- **Tags**: CAN injection, OBD, USB2CAN

## Replay Attack via OBD-II Port

- **Attack Type**: Physical Access
- **Target**: Car electronics
- **Vulnerability**: Replayable traffic without nonce/timestamp
- **MITRE**: T1003.003: Credential Dumping via Traffic Capture
- **Impact**: Unauthorized control of doors, lights, trunk
- **Tools**: CANtact, SavvyCAN, canplayer
- **Scenario**: The attacker replays previously captured CAN traffic from a prior session to trigger vehicle functions.
- **Attack Steps**: 1. Connect to vehicle and capture CAN traffic during normal use. 2. Save captured logs (e.g., opening trunk). 3. Disconnect and prepare replay using canplayer. 4. Reconnect to OBD-II port later. 5. Launch canplayer and transmit saved logs. 6. Observe vehicle behavior (e.g., trunk opens). 7. Adjust timing if replay is inconsistent. 8. Automate with scripting for stealth execution.
- **Detection**: Detect repeated frames with identical timing
- **Solution**: Use nonce/timestamp-based message validation
- **Tags**: replay, OBD-II, canplayer, offline capture

## ELM327 Bluetooth Exploit

- **Attack Type**: Wireless Entry (Bluetooth)
- **Target**: Vehicle ECU
- **Vulnerability**: Unsecured Bluetooth diagnostic dongle
- **MITRE**: T1059.001: Command-Line Interface
- **Impact**: Remote ECU data access and potential abuse
- **Tools**: Android, Torque app, ELM327
- **Scenario**: A cheap ELM327 Bluetooth OBD-II dongle is left in the car, and the attacker connects to it remotely to issue diagnostic commands.
- **Attack Steps**: 1. Scan for nearby Bluetooth devices in parking lot. 2. Detect unsecured ELM327 dongle (often "OBDII"). 3. Pair using default or no passcode. 4. Launch Torque app or custom script. 5. Issue diagnostic command (e.g., read DTCs). 6. Attempt live ECU commands (e.g., RPM, speed). 7. Log results and explore data access scope. 8. Optionally flash firmware or reset module.
- **Detection**: Monitor Bluetooth pairing logs
- **Solution**: Use encrypted dongles with secure pairing
- **Tags**: ELM327, bluetooth exploit, ECU

## Wi-Fi Access Point Exploit (Infotainment)

- **Attack Type**: Wireless Entry (Wi-Fi)
- **Target**: Infotainment head unit
- **Vulnerability**: Default credentials on exposed services
- **MITRE**: T1078: Valid Accounts
- **Impact**: Lateral pivot or media-based payload injection
- **Tools**: Kali Linux, Wireshark, hydra
- **Scenario**: The attacker targets an infotainment system that exposes a Wi-Fi access point for media sharing, using default credentials to gain access.
- **Attack Steps**: 1. Scan for open SSIDs from car infotainment system. 2. Attempt connection using default or weak passphrases. 3. Use hydra to brute-force login to exposed services (e.g., Samba, FTP). 4. Once inside, inspect shared directories. 5. Upload payload or modified media files. 6. Restart infotainment system to trigger execution. 7. Monitor impact via local observation or logs. 8. Log findings and persistence vector.
- **Detection**: Monitor for unauthorized Wi-Fi connections
- **Solution**: Harden infotainment OS, disable exposed services
- **Tags**: infotainment, Wi-Fi, weak creds

## Media File Exploit via USB

- **Attack Type**: Physical Access
- **Target**: Infotainment system
- **Vulnerability**: File parser vulnerability in media player
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Potential code execution in infotainment
- **Tools**: Hex Editor, ffmpeg, custom fuzzed files
- **Scenario**: The attacker prepares a malformed MP4 file that exploits a parsing bug in the infotainment media player when inserted via USB.
- **Attack Steps**: 1. Research CVEs for infotainment media player vulnerabilities. 2. Craft malformed MP4 or AVI using ffmpeg and hex editor. 3. Load exploit media onto USB drive. 4. Insert USB into car’s infotainment port. 5. Media player attempts playback and crashes or triggers vulnerability. 6. Gain code execution or system crash. 7. Observe CAN connection or crash logs. 8. Document version affected.
- **Detection**: Monitor USB insertion events and crashes
- **Solution**: Patch media player and block unknown file types
- **Tags**: USB, infotainment, media bug

## Remote Telematics API Token Abuse

- **Attack Type**: Remote Exploitation
- **Target**: Telematics backend
- **Vulnerability**: Exposed tokens / weak API auth
- **MITRE**: T1552.001: Credentials in Files
- **Impact**: Remote control via unauthorized API access
- **Tools**: Burp Suite, Frida, apktool
- **Scenario**: The attacker reverse engineers a mobile app and extracts API tokens to control vehicle functions remotely.
- **Attack Steps**: 1. Download and decompile vehicle’s mobile app using apktool. 2. Inspect source code for hardcoded API endpoints and tokens. 3. Use Burp Suite to intercept mobile app traffic. 4. Reuse tokens or endpoints from another session. 5. Attempt API requests (e.g., unlock doors, locate car). 6. Confirm if access works without 2FA. 7. Test rate limits and log responses. 8. Report scope of vulnerable endpoints.
- **Detection**: API request logging and rate-limiting
- **Solution**: Secure mobile app, rotate tokens, enforce 2FA
- **Tags**: telematics, mobile app, API tokens

## CAN Bus Brute Force via OBD-II

- **Attack Type**: Physical Access
- **Target**: Vehicle control modules
- **Vulnerability**: Lack of CAN filtering or validation
- **MITRE**: T1211: Exploitation for Privilege Escalation
- **Impact**: Discovery of undocumented vehicle functions
- **Tools**: python-can, USB2CAN, carloop
- **Scenario**: The attacker uses a brute-force approach to discover undocumented CAN messages by iteratively injecting IDs and observing effects.
- **Attack Steps**: 1. Connect USB2CAN to vehicle's OBD-II. 2. Launch Python script using python-can. 3. Send messages incrementally from 0x000 to 0x7FF. 4. Monitor for physical responses (e.g., light flicker, wiper move). 5. Log IDs that trigger reactions. 6. Refine with payload fuzzing for each ID. 7. Correlate IDs to potential functions. 8. Save discovered mapping for future attacks.
- **Detection**: Alert on abnormal ID/message frequency
- **Solution**: Implement CAN segmentation and monitoring
- **Tags**: CAN brute force, OBD injection

## Infotainment Update Manipulation

- **Attack Type**: Wireless or Physical
- **Target**: Infotainment firmware
- **Vulnerability**: Insecure firmware update validation
- **MITRE**: T1542.001: Pre-OS Boot
- **Impact**: Persistence on head unit, lateral access
- **Tools**: USB stick, custom firmware, Binwalk
- **Scenario**: The attacker exploits an unverified firmware update mechanism to upload a malicious infotainment update.
- **Attack Steps**: 1. Download official infotainment firmware from vendor website. 2. Unpack firmware using Binwalk. 3. Modify init scripts or binaries with payload. 4. Repackage firmware in same structure. 5. Load onto USB and insert into vehicle. 6. Trigger update via infotainment menu. 7. Observe successful install of trojaned firmware. 8. Use new code to interact with CAN or pivot.
- **Detection**: Firmware hash verification, USB monitoring
- **Solution**: Digitally sign and validate update packages
- **Tags**: infotainment, firmware, USB update

## LTE Telematics SIM Swap

- **Attack Type**: Remote Exploitation
- **Target**: Vehicle Telematics Unit
- **Vulnerability**: SIM linked commands without auth
- **MITRE**: T1585.001: SIM Card Swap
- **Impact**: Remote takeover of car commands
- **Tools**: Social engineering, phone carrier access
- **Scenario**: Attacker performs SIM swap on victim's telematics number, gaining control of SMS/GSM vehicle commands.
- **Attack Steps**: 1. Identify the vehicle’s phone number tied to telematics SIM. 2. Gather victim PII (email, DOB) via OSINT. 3. Call mobile provider and impersonate owner. 4. Request SIM replacement due to “lost phone.” 5. Insert new SIM in attacker’s GSM modem. 6. Receive OTA commands intended for car. 7. Send spoofed control SMS messages. 8. Monitor for success via response codes.
- **Detection**: Monitor for duplicate SIM or control changes
- **Solution**: Require strong 2FA for SIM access
- **Tags**: telematics, GSM, SIM swap

## Persistent Backdoor via OBD-II Dongle

- **Attack Type**: Physical Access
- **Target**: Vehicle CAN bus
- **Vulnerability**: Constant power from OBD-II + no runtime verification
- **MITRE**: T1098: Account Manipulation (physical backdoor variant)
- **Impact**: Long-term backdoor into vehicle systems
- **Tools**: Custom OBD-II dongle, Raspberry Pi Zero, CANable
- **Scenario**: The attacker places a maliciously modified OBD-II dongle inside the vehicle to act as a persistent CAN interface and backdoor.
- **Attack Steps**: 1. Flash a Raspberry Pi Zero W with a lightweight Linux image and enable CAN interface via CANable. 2. Develop a startup script that injects a specific CAN frame every few minutes (e.g., unlocking doors or disabling alarms). 3. Configure the device to auto-connect to Wi-Fi hotspot or act as an AP. 4. Plug the device into the OBD-II port in a concealed manner (e.g., under dash or inside plastic trim). 5. Leave the car and allow the device to remain powered by the car’s internal battery. 6. Return days later and connect to it wirelessly to send control commands. 7. Monitor CAN responses via SSH remotely. 8. Use cronjob or watchdogs for persistence even after reboots.
- **Detection**: Scan OBD-II port for continuous device activity
- **Solution**: Install port locks, power cutoff relays, or monitor draw
- **Tags**: persistent OBD, backdoor, Raspberry Pi

## Exploiting Tethered Wi-Fi on Infotainment

- **Attack Type**: Wireless Entry
- **Target**: Infotainment head unit
- **Vulnerability**: Weak Wi-Fi passphrase and exposed services
- **MITRE**: T1078: Valid Accounts
- **Impact**: Remote access to internal vehicle services
- **Tools**: Kali Linux, Wireshark, wifite, hydra
- **Scenario**: The attacker exploits an infotainment unit that shares a Wi-Fi hotspot with weak WPA2 credentials, gaining access to internal services.
- **Attack Steps**: 1. Use wifite or Kismet to passively scan for vehicle Wi-Fi SSIDs in parking lots. 2. Target infotainment hotspots that advertise manufacturer names. 3. Attempt WPA2 handshake capture via deauth attacks. 4. Use hashcat to brute-force weak passphrases (e.g., VIN-based passwords). 5. Connect to the vehicle Wi-Fi and scan the internal IP range. 6. Identify exposed services like HTTP config panels, FTP shares, or diagnostic APIs. 7. Use hydra to brute-force login or access services using default creds. 8. Maintain access by deploying hidden payloads or redirecting DNS locally.
- **Detection**: Monitor vehicle Wi-Fi associations and failed login attempts
- **Solution**: Enforce strong passphrases and firewall internal network
- **Tags**: infotainment, Wi-Fi, tethering, WPA2

## Mobile App Certificate Pinning Bypass

- **Attack Type**: Remote Exploitation
- **Target**: Mobile App → Telematics Server
- **Vulnerability**: Lack of token validation + pinning bypass
- **MITRE**: T1557.003: Adversary-in-the-Middle
- **Impact**: Full control of car through API manipulation
- **Tools**: Frida, Objection, Burp Suite, apktool
- **Scenario**: The attacker bypasses SSL pinning in a vehicle control app to intercept and modify traffic between the app and telematics server.
- **Attack Steps**: 1. Download the mobile app (APK) for the car control system from Play Store. 2. Use apktool to decompile and inspect for security features. 3. Use Frida or Objection to hook SSL pinning checks at runtime. 4. Run app inside emulator or rooted phone. 5. Intercept HTTPS traffic via Burp Suite to examine API calls. 6. Modify HTTP requests to simulate unauthorized access (e.g., unlock, locate, remote start). 7. Test various endpoints to assess scope of commands. 8. Record responses and validate if vehicle acts on them.
- **Detection**: Analyze app connections and inspect API traffic
- **Solution**: Enforce token validation and secure pinning libraries
- **Tags**: SSL bypass, mobile, Frida, Burp Suite

## Firmware Downgrade Attack via USB

- **Attack Type**: Physical Access
- **Target**: Infotainment firmware
- **Vulnerability**: Downgrade without signature or version check
- **MITRE**: T1542.001: Pre-OS Boot
- **Impact**: Restoration of known vulnerabilities for later attack
- **Tools**: USB drive, legacy firmware image, Binwalk
- **Scenario**: The attacker uses a USB update process to downgrade infotainment firmware to a vulnerable version and then exploits known bugs.
- **Attack Steps**: 1. Locate archived versions of infotainment firmware online or via forums. 2. Verify older version contains known vulnerabilities using release notes or reverse engineering. 3. Load legacy firmware onto a USB drive in the format expected by the infotainment unit. 4. Insert USB and enter the update menu manually. 5. Choose downgrade (if system permits) or force using bootloader override keys. 6. After successful downgrade, insert new USB with crafted payload to exploit bug. 7. Trigger execution and monitor for root access or system crash. 8. Log version info and behavior for reporting.
- **Detection**: Track firmware version changes and update behavior
- **Solution**: Disable downgrades, enforce signature & anti-rollback
- **Tags**: firmware, downgrade, infotainment

## CAN Gateway Misconfiguration Pivot

- **Attack Type**: Physical Access
- **Target**: In-vehicle network gateway
- **Vulnerability**: Improper isolation between CAN segments
- **MITRE**: T1021: Remote Services
- **Impact**: Lateral movement from infotainment to critical ECUs
- **Tools**: CANalyzer, UDS Toolbox, python-can
- **Scenario**: An attacker exploits misconfigured CAN gateways to pivot from infotainment network to drive-critical ECUs.
- **Attack Steps**: 1. Identify the gateway module connecting the infotainment to powertrain CAN. 2. Use physical access to connect via OBD-II or infotainment debug port. 3. Send diagnostic UDS requests to test if gateway forwards unauthorized frames. 4. Attempt to access ECUs on different CAN branches (e.g., ABS, engine). 5. Inject crafted messages using python-can or UDS scripts. 6. Monitor responses from control ECUs for unauthorized commands. 7. Test for persistence, reboot survivability, and state changes. 8. Use this as a stepping stone for lateral attacks.
- **Detection**: Gateway traffic pattern analysis
- **Solution**: Use secure gateways with access control lists
- **Tags**: CAN pivot, gateway, UDS, infotainment

## Remote Control via Compromised Cloud Portal

- **Attack Type**: Remote Exploitation
- **Target**: Cloud Telematics Interface
- **Vulnerability**: Poor authentication and exposed admin panels
- **MITRE**: T1530: Data from Cloud Storage
- **Impact**: Remote control over multiple vehicles
- **Tools**: Shodan, Burp Suite, credential stuffing tools
- **Scenario**: The attacker compromises a third-party vendor’s cloud fleet management portal to gain access to multiple connected vehicles.
- **Attack Steps**: 1. Identify fleet management service used by automotive OEM or enterprise clients. 2. Scan for internet-exposed login panels using Shodan. 3. Perform credential stuffing using leaked credentials to gain access. 4. Browse dashboard to locate connected vehicles and control panel. 5. Attempt actions like remote unlock, track GPS, or disable engine remotely. 6. Extract API endpoints and test outside of portal. 7. Pivot to individual vehicle sessions. 8. Document scope of access and escalate with privilege misuse.
- **Detection**: Monitor for suspicious logins and API anomalies
- **Solution**: Implement SSO, 2FA, and IP whitelisting
- **Tags**: cloud, fleet, telematics, portal

## CVE Exploitation in Infotainment Stack

- **Attack Type**: Physical or Wireless
- **Target**: Infotainment stack
- **Vulnerability**: Unpatched CVE in embedded OS
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Code execution in car OS, potential CAN pivot
- **Tools**: CVE database, Metasploit, USB or Bluetooth
- **Scenario**: The attacker leverages a known CVE in the infotainment OS (e.g., QNX or Linux-based) to gain shell access.
- **Attack Steps**: 1. Identify CVEs affecting infotainment OS version. 2. Validate vulnerable services or ports exposed (e.g., media parsing, SSH, dbus). 3. Craft exploit using Metasploit or PoC script. 4. Deliver payload via USB, Bluetooth, or over-the-air channel depending on vector. 5. Observe infotainment behavior and check for code execution. 6. Spawn reverse shell or drop backdoor on successful exploit. 7. Elevate privileges and inspect CAN interface availability. 8. Maintain access or wipe traces post-test.
- **Detection**: CVE scanning and log inspection
- **Solution**: Patch CVEs, isolate infotainment from drive CAN
- **Tags**: infotainment, CVE, QNX, exploit

## Rogue Wi-Fi Tethering Device

- **Attack Type**: Wireless Entry
- **Target**: Infotainment head unit
- **Vulnerability**: Trusts SSID without certificate validation
- **MITRE**: T1557.002: Rogue Wi-Fi
- **Impact**: Redirect or payload delivery via fake Wi-Fi
- **Tools**: hostapd, airgeddon, Wireshark
- **Scenario**: The attacker sets up a rogue Wi-Fi access point mimicking the car owner’s phone to trick infotainment into auto-connecting.
- **Attack Steps**: 1. Identify the SSID previously used by the infotainment unit (e.g., “John’s iPhone”). 2. Create rogue AP with same SSID and MAC address using hostapd. 3. Increase signal strength to outcompete real device. 4. Wait for vehicle to connect automatically. 5. Monitor DHCP and DNS traffic to identify infotainment OS activity. 6. Redirect traffic to MITM proxy for payload injection. 7. Deliver exploit or fake firmware update over network. 8. Log success and extract infotainment info.
- **Detection**: Detect SSID collisions or duplicate MACs
- **Solution**: Enable certificate pinning and SSID whitelisting
- **Tags**: rogue AP, infotainment, wireless

## Infotainment via Serial Debug Port

- **Attack Type**: Physical Access
- **Target**: Infotainment internals
- **Vulnerability**: Exposed debug interface on PCB
- **MITRE**: T1055: Process Injection (via physical shell)
- **Impact**: Root-level shell on embedded infotainment
- **Tools**: UART adapter, screen/minicom, screwdriver kit
- **Scenario**: The attacker disassembles the infotainment unit to access a UART serial port and retrieve root shell access.
- **Attack Steps**: 1. Remove infotainment unit from vehicle dashboard. 2. Locate test pads or labeled UART pins on PCB. 3. Solder jumper wires or use clip connectors. 4. Connect to UART interface using USB-to-Serial adapter. 5. Launch minicom/screen at expected baud rate (e.g., 115200). 6. Observe boot logs and interrupt for root shell if console access allowed. 7. Dump filesystem or insert backdoor. 8. Reinstall unit and monitor access persistence.
- **Detection**: Detect tamper on head unit housing
- **Solution**: Remove UART in production or disable login prompt
- **Tags**: UART, serial debug, infotainment

## Exploit via Automotive Companion App

- **Attack Type**: Remote Exploitation
- **Target**: Telematics backend
- **Vulnerability**: Missing authorization on backend APIs
- **MITRE**: T1020: Automated Exfiltration
- **Impact**: Control or access to other users’ vehicles
- **Tools**: apktool, Postman, Burp Suite
- **Scenario**: The attacker targets flaws in an automotive companion app’s backend API, bypassing VIN verification to control arbitrary vehicles.
- **Attack Steps**: 1. Decompile the app using apktool to inspect source code. 2. Identify VIN or userID validation logic for vehicle control endpoints. 3. Test backend APIs directly using Postman and Burp Suite. 4. Replace VIN with other known values and send requests. 5. Observe if unauthorized vehicle control functions (e.g., lock/unlock) are executed. 6. Exploit by scripting mass requests to different VINs. 7. Log vehicle behaviors and response patterns. 8. Report vulnerable endpoints.
- **Detection**: API gateway rate monitoring and audit logs
- **Solution**: Add strict VIN-owner binding on backend
- **Tags**: companion app, VIN injection, API

## Exploiting OBD-II Firmware Update Routine

- **Attack Type**: Physical Access
- **Target**: ECU / CAN bus
- **Vulnerability**: Lack of authentication in firmware updates
- **MITRE**: TA0001: Initial Access
- **Impact**: Persistent modification of ECU behavior
- **Tools**: OBD-II flasher tools, Python, CANdevStudio
- **Scenario**: An attacker exploits insecure firmware update mechanisms through OBD-II to flash malicious firmware onto ECUs.
- **Attack Steps**: 1. Gain physical access to the vehicle and plug into the OBD-II port using a CAN flasher tool. 2. Identify the specific ECU using broadcast requests over CAN. 3. Analyze manufacturer-specific firmware update commands (may require reverse engineering or leaked documentation). 4. Begin firmware update handshake with the ECU and enter reprogramming mode. 5. Craft and send malicious firmware payload in chunks over CAN. 6. Monitor ECU response and finalize the update. 7. Restart the ECU and verify altered behavior (e.g., disabled safety mechanisms). 8. Disconnect tool and leave no visible trace.
- **Detection**: Check firmware integrity and version hash
- **Solution**: Secure boot and signed firmware enforcement
- **Tags**: firmware update, ECU reflash, OBD-II

## Spoofing TPMS Sensors to Trick Infotainment

- **Attack Type**: Wireless
- **Target**: Infotainment / Dashboard
- **Vulnerability**: Unauthenticated wireless sensor communication
- **MITRE**: T1562: Impair Defenses
- **Impact**: Cause distraction, disable features, manipulate UI
- **Tools**: HackRF, GNU Radio, TPMS scripts
- **Scenario**: Attackers simulate Tire Pressure Monitoring System (TPMS) data to confuse infotainment or alert systems.
- **Attack Steps**: 1. Identify target vehicle’s TPMS frequency (commonly 315MHz or 433MHz). 2. Use SDR software (like GNU Radio) to record valid TPMS transmissions near a vehicle. 3. Replay modified data to mimic extremely low tire pressure or other faults. 4. Monitor infotainment system and dashboard responses. 5. Continuously change fake sensor IDs to avoid detection. 6. Use multiple fake packets to trigger multiple alerts simultaneously. 7. Observe driver behavior and potential misdirection. 8. Optionally automate spoofing via Python SDR scripts.
- **Detection**: Signal anomaly detection, abnormal TPMS activity
- **Solution**: Strong authentication and encryption in TPMS
- **Tags**: TPMS, spoofing, RF attack, SDR

## Gaining Telematics Root Shell via Serial UART

- **Attack Type**: Physical Access
- **Target**: Telematics Module
- **Vulnerability**: Exposed debug interfaces
- **MITRE**: TA0001: Initial Access
- **Impact**: Root-level access to telematics and network modules
- **Tools**: UART cable, minicom, screwdriver
- **Scenario**: Attacker opens the telematics control unit (TCU) and accesses a serial debug port to get root shell.
- **Attack Steps**: 1. Disconnect battery and remove dashboard cover to access the TCU. 2. Open the TCU casing carefully to expose internal board. 3. Identify UART pins using multimeter and online schematics. 4. Connect a USB-UART adapter to the TX, RX, and GND pins. 5. Launch minicom or PuTTY with correct baud rate (e.g., 115200). 6. Reconnect vehicle power and observe serial boot logs. 7. Press keys during bootloader to stop autoboot. 8. Access root shell or drop to maintenance shell. 9. Browse filesystem and retrieve configs or sensitive data.
- **Detection**: Monitor internal console access
- **Solution**: Remove/debug port hardening, epoxy cover
- **Tags**: UART, serial console, root access

## Replay Attack on Remote Keyless Entry

- **Attack Type**: Wireless
- **Target**: Central Locking System
- **Vulnerability**: Insecure RF protocol / no rolling codes
- **MITRE**: T1071: Application Layer Protocol
- **Impact**: Unauthorized entry into vehicle
- **Tools**: SDR, HackRF, GNU Radio
- **Scenario**: Capturing and replaying key fob RF signals to unlock doors later.
- **Attack Steps**: 1. Set up SDR (e.g., HackRF) to monitor the 315/433 MHz band. 2. Wait near a parked car and capture the unlock signal when the user opens the door. 3. Save the signal as a binary waveform. 4. Use replay attack tools or scripts to resend the waveform later when the car is unattended. 5. Analyze the signal type (rolling code or static) — older models may not use rolling code. 6. Replay multiple times to confirm effectiveness. 7. Retrieve vehicle data or enter cabin for further attacks.
- **Detection**: Monitor RF activity and unusual unlocking
- **Solution**: Use encrypted rolling code key systems
- **Tags**: key fob, replay, SDR

## Remote Exploit of Infotainment Web Interface

- **Attack Type**: Remote
- **Target**: Infotainment OS
- **Vulnerability**: Web interface with poor input validation
- **MITRE**: T1190: Exploit Public-Facing Application
- **Impact**: Infotainment system takeover, data theft
- **Tools**: Browser, Burp Suite, Metasploit
- **Scenario**: A vulnerable infotainment web interface is exploited via browser on mobile tethered to vehicle Wi-Fi.
- **Attack Steps**: 1. Connect to the car’s Wi-Fi hotspot (e.g., provided by infotainment). 2. Browse to local admin panel or web interface IP (e.g., 192.168.0.1). 3. Identify web application vulnerabilities using Burp Suite (e.g., command injection, XSS). 4. Try default credentials or brute-force weak passwords. 5. Inject commands via vulnerable form fields. 6. Gain shell access to the underlying Linux system. 7. Use system commands to scan the internal CAN bridge or retrieve credentials. 8. Set up persistence or reverse shell.
- **Detection**: Log anomalies, failed login bursts
- **Solution**: Harden web interface, patch firmware
- **Tags**: infotainment, web attack, command injection

## Bluetooth Stack Overflow on Infotainment

- **Attack Type**: Wireless
- **Target**: Infotainment Bluetooth Stack
- **Vulnerability**: Vulnerable GATT/SDP stack handling
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Memory corruption, DoS, or remote shell
- **Tools**: Bluetooth fuzzers, GATTacker, Python scripts
- **Scenario**: Exploiting vulnerable Bluetooth stack on infotainment system via crafted pairing request.
- **Attack Steps**: 1. Enable Bluetooth on attack laptop and scan for car’s Bluetooth. 2. Identify the infotainment device name and MAC address. 3. Use a Bluetooth fuzzing tool to craft malformed pairing requests. 4. Repeatedly send malformed SDP or GATT packets to crash or destabilize the service. 5. If system crashes, reboot and attempt privilege escalation using memory leaks. 6. Attempt DoS or code execution on the infotainment system if vulnerable. 7. Record logs for crash triage or persistence strategy.
- **Detection**: Monitor pairing logs, check crash traces
- **Solution**: Patch stack, restrict pairing permissions
- **Tags**: bluetooth, buffer overflow, car hack

## Access Vehicle CAN via Compromised Android Auto App

- **Attack Type**: App Exploit
- **Target**: Android Auto Middleware
- **Vulnerability**: Lack of app-level sandboxing in car integration
- **MITRE**: T1555: Credentials from Password Stores
- **Impact**: Data manipulation, possible DoS
- **Tools**: Android Studio, Frida, APKTool
- **Scenario**: A malicious app running with Android Auto privileges abuses debugging APIs to access CAN functions.
- **Attack Steps**: 1. Create or repack a malicious Android Auto-compatible app with debugging permissions. 2. Ask victim to install the app or sideload it during phone sync. 3. Once connected via USB, the app interfaces with car’s middleware API. 4. Inject Java hooks using Frida to modify CAN-related function calls. 5. Send forged speed or navigation messages to confuse systems. 6. Optionally pivot to infotainment or GPS modules. 7. Log all intercepted CAN activity for future use.
- **Detection**: Log device connection history
- **Solution**: Use allowlist for trusted Android Auto apps
- **Tags**: Android Auto, Frida, app abuse

## Man-in-the-Middle via Malicious Charging Station

- **Attack Type**: Hardware Exploit
- **Target**: EV / Charger
- **Vulnerability**: Trust in physical infrastructure
- **MITRE**: T1021: Remote Services
- **Impact**: Data theft, firmware overwrite, ECU control
- **Tools**: Raspberry Pi, USB-to-CAN, Wireshark
- **Scenario**: Attacker installs backdoor on EV charging station to sniff CAN or Ethernet during charging.
- **Attack Steps**: 1. Set up a Raspberry Pi with a CAN interface or Ethernet sniffer. 2. Place the device inside a modified charging station. 3. When the EV plugs in, capture traffic between EV and charger. 4. Extract diagnostics, VIN, and potentially reprogramming commands. 5. Try injecting forged messages or manipulate charging rate. 6. Store all data for later analysis. 7. Monitor for ECU behavior changes.
- **Detection**: Monitor for altered station firmware
- **Solution**: Secure firmware + endpoint hardening
- **Tags**: EV charging, CAN sniffing, Raspberry Pi

## Exploiting GSM-based Telematics API

- **Attack Type**: Remote
- **Target**: Telematics Backend
- **Vulnerability**: Insecure API auth/token leakage
- **MITRE**: T1133: External Remote Services
- **Impact**: Remote control of vehicle features
- **Tools**: Burp Suite, curl, JSON API scripts
- **Scenario**: The attacker queries unsecured or leaked APIs tied to a car’s GSM/LTE-based telematics service.
- **Attack Steps**: 1. Research telematics provider and identify known API endpoints (e.g., /lock, /start). 2. Use leaked API keys or default tokens to make requests. 3. Query VINs or license plates from paste sites or social engineering. 4. Send crafted requests to perform remote start, unlock, or track location. 5. Modify headers or spoof device IDs if authentication is token-based. 6. Test for rate-limiting or IP blacklisting. 7. Pivot into car’s network if accessible from backend.
- **Detection**: Monitor abnormal API usage
- **Solution**: Enforce strong auth, rotate tokens, log IPs
- **Tags**: telematics, GSM, API abuse

## CAN Message Injection from Malicious Aftermarket Device

- **Attack Type**: Physical Access
- **Target**: Vehicle CAN via accessory
- **Vulnerability**: Supply chain / 3rd-party accessory
- **MITRE**: T1200: Hardware Additions
- **Impact**: Covert, long-term compromise
- **Tools**: Custom CAN device, ESP32, Arduino
- **Scenario**: Attacker installs a malicious dashcam that injects CAN messages over time.
- **Attack Steps**: 1. Program an ESP32-based device to send specific CAN messages (e.g., unlock, disable brakes). 2. Conceal the device in an aftermarket accessory like a dashcam. 3. Connect it to the OBD-II port or CAN wires behind dashboard. 4. Ensure it runs quietly in background and transmits messages at safe intervals. 5. Activate behavior remotely via hidden triggers (e.g., SMS or radio packet). 6. Log data locally and exfiltrate via Wi-Fi when near home network.
- **Detection**: Inspect CAN traffic for anomalies
- **Solution**: Approve only verified accessories
- **Tags**: aftermarket, ESP32, stealth CAN injection

## Exploiting Head Unit Browser

- **Attack Type**: Remote Exploitation
- **Target**: Infotainment Head Unit
- **Vulnerability**: Browser engine with exposed attack surface
- **MITRE**: TA0001: Initial Access
- **Impact**: Infotainment compromise can lead to full vehicular control if no isolation
- **Tools**: Burp Suite, Wireshark, Firefox Dev Tools
- **Scenario**: The attacker exploits a browser-based vulnerability in the infotainment system’s built-in web view engine to gain access to the CAN bus.
- **Attack Steps**: 1. Identify that the head unit has an embedded browser or renders external content (e.g., HTML5 via Wi-Fi hotspot or USB). 2. Deliver malicious JavaScript via a USB drive or QR-code linked phishing page rendered on the car display. 3. Exploit a DOM-based XSS vulnerability or browser RCE flaw in the infotainment system. 4. Use JavaScript to interact with system-level interfaces if exposed (e.g., XMLHttpRequest to local services). 5. Pivot to internal infotainment services exposed via loopback or hardcoded IP. 6. From infotainment, interact with CAN transceivers if they are directly mapped or accessible. 7. Try injecting CAN messages or activating services (e.g., unlocking doors).
- **Detection**: Monitor logs of web activity and malformed requests
- **Solution**: Use browser sandboxing and update engines with secure policies
- **Tags**: infotainment, browser, XSS, CAN, head unit

## Abuse of Diagnostic Firmware Upload

- **Attack Type**: Physical Access
- **Target**: Engine Control Unit (ECU)
- **Vulnerability**: Insecure diagnostic protocols and weak firmware validation
- **MITRE**: TA0005: Defense Evasion
- **Impact**: Attacker can run custom code with ECU privileges
- **Tools**: UDS software, CANoe, custom firmware injector
- **Scenario**: The attacker uses diagnostic mode to upload malicious firmware via OBD-II.
- **Attack Steps**: 1. Gain physical access to the vehicle’s OBD-II port. 2. Use a tool like CANoe or UDS-compatible injector to enter Diagnostic Session Control. 3. Authenticate using a security seed/key handshake (can be reverse engineered or brute-forced). 4. Enter the firmware update mode (e.g., via UDS service 0x34). 5. Upload a malicious firmware blob that includes backdoor code or disables secure boot. 6. Send routine control messages to reboot the ECU and start the new firmware. 7. Confirm that new firmware accepts attacker commands via CAN messages. 8. Maintain persistence via write-once memory or disabling further updates.
- **Detection**: Check firmware hash and update logs periodically
- **Solution**: Implement signed firmware enforcement and authentication
- **Tags**: ECU, firmware injection, UDS, diagnostic abuse

## Bluetooth Stack Overflow in Infotainment

- **Attack Type**: Wireless Access
- **Target**: Infotainment System
- **Vulnerability**: Vulnerable Bluetooth stack with remote execution flaw
- **MITRE**: TA0001: Initial Access
- **Impact**: Remote access without pairing or user interaction
- **Tools**: Ubertooth One, Wireshark Bluetooth, gatttool
- **Scenario**: The attacker connects to the infotainment Bluetooth stack and exploits a buffer overflow to inject code.
- **Attack Steps**: 1. Conduct Bluetooth scanning using Ubertooth One to identify vehicle’s active devices. 2. Enumerate Bluetooth services and supported profiles using gatttool. 3. Identify a known vulnerability in the infotainment’s Bluetooth stack (e.g., unpatched BlueBorne). 4. Send a malformed SDP or L2CAP packet that triggers a buffer overflow. 5. Use return-oriented programming (ROP) techniques to execute shellcode in the infotainment processor. 6. If successful, gain root or system access and pivot toward other interfaces like CAN transceivers. 7. Maintain Bluetooth session and issue commands via Bluetooth audio or diagnostic interface.
- **Detection**: Monitor Bluetooth pairing attempts and malformed traffic
- **Solution**: Patch Bluetooth firmware; disable unused profiles
- **Tags**: bluetooth, BlueBorne, RCE, wireless access

## Exploiting Wi-Fi Tethered Device Trust

- **Attack Type**: Wireless Access
- **Target**: Infotainment OS
- **Vulnerability**: Implicit trust in tethered connections
- **MITRE**: TA0006: Credential Access
- **Impact**: Initial foothold can escalate into control access
- **Tools**: Karma attack tools, EvilAP, Metasploit
- **Scenario**: An attacker hijacks trust between the infotainment unit and a tethered smartphone over Wi-Fi to inject malicious payloads.
- **Attack Steps**: 1. Launch a rogue Wi-Fi access point using EvilAP with same SSID as the user’s phone. 2. Trick the infotainment system into connecting to rogue AP if phone disconnects temporarily. 3. Intercept traffic between infotainment and fake smartphone tethering service. 4. Inject JavaScript or binary payloads via simulated tethered device updates or media sync. 5. Exploit the infotainment OS to escalate privileges using embedded content handlers. 6. Once on the infotainment, explore CAN access points or connected USB devices. 7. Use this access to control minor functions or map internal networks.
- **Detection**: Monitor AP associations and use of rogue SSIDs
- **Solution**: Enforce cert pinning and use authenticated pairing
- **Tags**: tethering, infotainment, rogue AP, Wi-Fi attack

## Remote Telematics Over GSM Injection

- **Attack Type**: Remote Exploitation
- **Target**: Telematics Unit
- **Vulnerability**: Poor SMS/GSM authentication or lack of input sanitization
- **MITRE**: TA0011: Command and Control
- **Impact**: Remote attacker gains access to GPS, start/stop, and diagnostics
- **Tools**: GSM modem, AT command tool, SDR
- **Scenario**: Using exposed GSM APIs or debug services, the attacker sends crafted SMS or GSM data to interact with telematics.
- **Attack Steps**: 1. Use an SDR (Software Defined Radio) tool to monitor GSM network and identify backend phone numbers of vehicle telematics units. 2. Prepare malicious SMS payloads formatted with AT commands or diagnostic triggers. 3. Use a GSM modem to deliver specially crafted SMS or USSD code to the car’s GSM receiver. 4. If the backend API does not authenticate well, the car may respond or execute actions like location ping, remote start, or diagnostics. 5. Attempt to extract or overwrite configuration using these messages. 6. Confirm access by checking vehicle behavior (horn, lights, response). 7. Replay or escalate access via OTA update endpoints if reachable.
- **Detection**: Monitor GSM communication logs and abnormal SMS traffic
- **Solution**: Require encryption and proper command validation
- **Tags**: GSM, OTA, remote start, SMS attack

## Wired Ethernet Port Exposure

- **Attack Type**: Physical Access
- **Target**: Ethernet Gateway
- **Vulnerability**: Hidden physical interface with full access
- **MITRE**: TA0001: Initial Access
- **Impact**: Allows direct OS-level access to embedded Linux systems
- **Tools**: LAN tap, Wireshark, nmap, Metasploit
- **Scenario**: Attackers exploit exposed maintenance Ethernet ports in EVs or luxury vehicles to connect to internal systems.
- **Attack Steps**: 1. Locate hidden Ethernet maintenance port often used by dealerships (behind dashboard or center console). 2. Use a LAN tap or laptop with auto-negotiation enabled to connect. 3. Scan available IPs using nmap and enumerate services (e.g., SSH, HTTP). 4. Discover internal maintenance APIs or file servers exposed. 5. Exploit unprotected endpoints to download config or upload shell scripts. 6. Escalate privileges by using default service credentials. 7. Map CAN gateway bridges or try pivoting into main ECUs.
- **Detection**: Monitor vehicle for open Ethernet ports or unknown traffic
- **Solution**: Disable exposed Ethernet ports or limit by MAC whitelist
- **Tags**: ethernet, dealership port, luxury vehicle, LAN hacking

## NFC Key Emulation Bypass

- **Attack Type**: Wireless Access
- **Target**: Vehicle NFC Receiver
- **Vulnerability**: Weak or replayable NFC authentication
- **MITRE**: TA0006: Credential Access
- **Impact**: Full vehicle unlock and ignition without real key
- **Tools**: Proxmark3, ChameleonMini, Android NFC tools
- **Scenario**: The attacker clones NFC keys or uses an emulator to spoof the presence of a key fob near the vehicle.
- **Attack Steps**: 1. Approach the target user and perform NFC skimming using Proxmark3 in sniff mode. 2. Capture authentication sequences used by the vehicle’s NFC entry system. 3. Emulate the captured key using a device like ChameleonMini or NFC-enabled phone with modded firmware. 4. Approach the vehicle with the cloned key. 5. Test unlock and push-start functionalities if proximity unlock is supported. 6. Optionally pair with infotainment system as a new device.
- **Detection**: Monitor NFC unlock attempts and proximity triggers
- **Solution**: Use rolling codes and challenge-response authentication
- **Tags**: NFC, keyless entry, cloning, replay

## Android Auto Privilege Escalation

- **Attack Type**: Wireless Access
- **Target**: Infotainment OS
- **Vulnerability**: Over-permissive trust in mobile connections
- **MITRE**: TA0005: Defense Evasion
- **Impact**: Escalation into car system via mobile app
- **Tools**: ADB, Frida, custom APK
- **Scenario**: The attacker modifies Android Auto to exploit the trust placed in mobile apps by the head unit.
- **Attack Steps**: 1. Reverse engineer Android Auto app to identify permissions used during handshake. 2. Patch the APK to include elevated permissions or malicious intents. 3. Re-sign and install the APK on a rooted Android device. 4. Connect the phone to the infotainment unit via USB or Wi-Fi. 5. During pairing, send custom intents to access media manager, file system, or diagnostics. 6. Use Frida to inject runtime hooks if necessary. 7. Attempt to pivot from infotainment to internal CAN interface if accessible.
- **Detection**: Monitor for unknown or sideloaded apps
- **Solution**: Use app whitelisting and connection whitelists
- **Tags**: Android Auto, mobile bridge, app escalation

## Malicious Firmware Update over USB

- **Attack Type**: Physical Access
- **Target**: Infotainment Head Unit
- **Vulnerability**: Unauthenticated firmware update process
- **MITRE**: TA0040: Impact
- **Impact**: Code execution on infotainment for further pivoting
- **Tools**: Binwalk, USB stick, firmware mod kit
- **Scenario**: The attacker uses the USB firmware update process to load custom payloads into the infotainment system.
- **Attack Steps**: 1. Obtain an original firmware update file from manufacturer website or a dealership USB. 2. Extract the update image using binwalk to analyze structure. 3. Inject a malicious script or binary into the update’s file system (e.g., add reverse shell). 4. Repack and checksum the update if validation is weak or absent. 5. Load the malicious firmware onto a USB and plug into the car’s USB port. 6. The head unit auto-detects the update and installs it. 7. Verify persistence and run post-exploit commands from infotainment console.
- **Detection**: Log firmware install attempts and verify hashes
- **Solution**: Enforce signed update verification
- **Tags**: USB, firmware injection, infotainment

## Voice Assistant Exploitation

- **Attack Type**: Wireless Access
- **Target**: Voice Assistant Module
- **Vulnerability**: Poor input validation and audio spoofing protection
- **MITRE**: TA0001: Initial Access
- **Impact**: Social engineering or hidden command injection
- **Tools**: GQRX SDR, audio emitter, ultrasonic generator
- **Scenario**: The attacker issues malicious voice commands using social engineering or ultrasonic injection to trigger actions.
- **Attack Steps**: 1. Record common voice commands accepted by the vehicle (e.g., "call home", "navigate to"). 2. Craft audio payloads that sound benign to humans but include hidden ultrasonic triggers. 3. Transmit payloads via speaker outside the vehicle using high-gain audio. 4. The vehicle’s assistant interprets commands and may trigger calls, SMS, or location services. 5. Use exposed services like Bluetooth or cellular tether to extract data or pivot further.
- **Detection**: Monitor voice command usage and anomalies
- **Solution**: Limit voice control to confirmed user profiles
- **Tags**: voice control, ultrasonic, social engineering

## OBD-II Based ECU Configuration Dump

- **Attack Type**: Physical Access
- **Target**: ECU
- **Vulnerability**: Lack of authentication on diagnostic sessions
- **MITRE**: TA0001: Initial Access
- **Impact**: Enables deep understanding of firmware and configurations
- **Tools**: CANtact, Kayak, python-can
- **Scenario**: Attacker accesses vehicle via OBD-II to dump ECU configurations for reverse engineering
- **Attack Steps**: 1. Connect the CAN interface device (e.g., CANtact) to the vehicle’s OBD-II port. 2. Launch Kayak or a Python script using python-can to enumerate available ECU addresses. 3. Send diagnostic session initiation commands to each detected ECU (e.g., UDS 0x10 0x03). 4. Query DIDs (Data Identifier codes) for configuration data (e.g., 0x22 0xF190 for VIN). 5. Capture responses and extract meaningful configuration data like part numbers, firmware versions, and capabilities. 6. Save the logs for offline analysis and potential replay. 7. Use this knowledge to find modifiable fields or vulnerabilities.
- **Detection**: Detect unusual diagnostic session initiation patterns
- **Solution**: Secure diagnostic channels with access control and session limits
- **Tags**: OBD-II, ECU, diagnostics, reverse engineering

## Telematics API Credential Reuse

- **Attack Type**: Remote Exploitation
- **Target**: Telematics Server
- **Vulnerability**: Token reuse, missing expiration
- **MITRE**: TA0001: Initial Access
- **Impact**: Full remote vehicle access with no physical proximity
- **Tools**: Burp Suite, Postman
- **Scenario**: Attacker uses leaked or reused telematics API credentials to access vehicle remotely
- **Attack Steps**: 1. Find a leaked or shared API key/token from previous incidents or poor credential hygiene. 2. Open Postman and configure the request headers with the stolen credential. 3. Test endpoints such as /vehicle/status or /vehicle/unlock. 4. Capture successful responses indicating that the credential is still valid. 5. Attempt further remote control actions via exposed commands like start engine or unlock doors. 6. Log every action for forensic and PoC purposes. 7. Validate full access and maintain access until tokens are revoked.
- **Detection**: Monitor usage of known API credentials from multiple IPs
- **Solution**: Enforce token expiration and rate-limit API endpoints
- **Tags**: telematics, API, credential reuse, remote

## Reverse Tethering via Infotainment USB Debug

- **Attack Type**: Local Exploitation
- **Target**: Infotainment System
- **Vulnerability**: Lack of debug access control
- **MITRE**: TA0005: Defense Evasion
- **Impact**: Attacker can modify behavior of infotainment unit
- **Tools**: ADB, Android Auto exploit tools
- **Scenario**: Attacker enables USB debug mode via infotainment system to push payloads
- **Attack Steps**: 1. Plug in an Android device to the infotainment system’s USB port. 2. Attempt to trigger developer/debugging mode using known key sequences or Android Auto handshake flaws. 3. Once USB debugging is accepted, run ADB commands to enumerate devices and check access level. 4. Use adb shell to explore internal infotainment filesystem. 5. Push payload scripts to initiate CAN or media manipulation. 6. Capture logs from system processes and USB events. 7. Maintain local persistence if allowed by the OS.
- **Detection**: Monitor for ADB connection events
- **Solution**: Disable USB debug in production firmware
- **Tags**: infotainment, USB, ADB, tethering, debug

## GSM Backdoor via SMS Trigger

- **Attack Type**: Remote Exploitation
- **Target**: Telematics Unit
- **Vulnerability**: Poor SMS parsing and lack of validation
- **MITRE**: TA0001: Initial Access
- **Impact**: Enables remote commands without authentication
- **Tools**: USB SIM gateway, GSM modem
- **Scenario**: Attacker sends specially crafted SMS to GSM module in telematics unit to trigger command
- **Attack Steps**: 1. Identify the vehicle’s GSM-enabled telematics module’s phone number via prior network scans or SIM leaks. 2. Craft a binary SMS or UDH (User Data Header) message that exploits known parsing flaws. 3. Use a USB GSM modem to send the SMS to the target vehicle. 4. Monitor response using SDR or backchannel logs if possible. 5. Trigger hidden diagnostic or control interfaces via the message payload. 6. Validate changes such as engine status or GPS position update. 7. Document and clean up forensic traces if needed.
- **Detection**: Monitor GSM traffic for binary SMS patterns
- **Solution**: Use input validation and GSM firewalling
- **Tags**: SMS, telematics, GSM, binary exploit

## Wi-Fi SSID Spoofing for Infotainment Hijack

- **Attack Type**: Wireless Entry
- **Target**: Infotainment System
- **Vulnerability**: Trusting known SSIDs, no cert pinning
- **MITRE**: TA0001: Initial Access
- **Impact**: Allows attacker to control Wi-Fi sessions
- **Tools**: WiFi Pineapple, Airbase-ng
- **Scenario**: Attacker spoofs a known SSID to hijack infotainment connectivity
- **Attack Steps**: 1. Monitor for Wi-Fi probe requests from vehicle infotainment system. 2. Identify previously connected SSIDs (e.g., "HomeNet123"). 3. Use Airbase-ng or WiFi Pineapple to spoof the SSID and respond to the probe. 4. Intercept infotainment’s connection attempt and offer captive portal. 5. Use portal to trick system into installing a malicious media file or configuration. 6. Maintain connection long enough to push payload. 7. Disconnect to avoid further detection.
- **Detection**: Monitor for rogue access points
- **Solution**: Enforce SSID whitelisting or VPN tunnels
- **Tags**: wifi spoofing, infotainment, wireless

## OBD-II Based Replay Attack for Remote Start

- **Attack Type**: Physical Access
- **Target**: ECU
- **Vulnerability**: Lack of frame authentication and anti-replay
- **MITRE**: TA0001: Initial Access
- **Impact**: Enables remote starting, potential theft
- **Tools**: CAN Logger, SavvyCAN
- **Scenario**: Attacker replays previously recorded CAN messages to trigger engine start
- **Attack Steps**: 1. Previously record the CAN frames while starting the vehicle using a CAN logger. 2. Connect to the OBD-II port using same tool and load recorded frames. 3. Replay start sequence when ignition is off. 4. Confirm if engine starts remotely without key presence. 5. Vary timing and retry multiple times to bypass time-based anti-replay defenses. 6. Log results and vehicle response for PoC. 7. Remove logger to avoid detection.
- **Detection**: Detect replayed identical CAN frames
- **Solution**: Use message authentication codes (MACs)
- **Tags**: CAN replay, OBD-II, ignition spoof

## Bluetooth Stack Overflow in Infotainment

- **Attack Type**: Wireless Entry
- **Target**: Infotainment System
- **Vulnerability**: Buffer overflow in Bluetooth stack
- **MITRE**: TA0001: Initial Access
- **Impact**: Crash or full compromise of infotainment
- **Tools**: Custom BT fuzzers
- **Scenario**: Attacker exploits buffer overflow in infotainment’s Bluetooth module to crash or gain control
- **Attack Steps**: 1. Scan for the vehicle’s Bluetooth interface from a short distance. 2. Use a Bluetooth fuzzer to send malformed SDP/L2CAP packets. 3. Monitor infotainment response and look for crashes or reboots. 4. Once vulnerable function is discovered, refine payload for shellcode delivery. 5. Retry with reduced malformed packet until successful buffer overflow. 6. Maintain session and extract infotainment details via injected code. 7. Document crash logs and behavior.
- **Detection**: Detect malformed Bluetooth traffic
- **Solution**: Patch firmware to sanitize BT input
- **Tags**: bluetooth, overflow, infotainment, fuzzing

## CAN Bus Bridge via Head Unit to ECU

- **Attack Type**: Local Exploitation
- **Target**: ECU via Infotainment
- **Vulnerability**: Unfiltered internal CAN bridge
- **MITRE**: TA0001: Initial Access
- **Impact**: Allows indirect control of driving functions
- **Tools**: Custom CAN scripts, Raspberry Pi
- **Scenario**: Attacker exploits head unit CAN access to bridge to ECU commands
- **Attack Steps**: 1. Connect to infotainment head unit’s debug port (e.g., via serial or USB). 2. Explore filesystem and detect CAN socket or interface. 3. Bridge the CAN interface using a tool like socketcan-utils. 4. Send control messages such as gear or throttle commands to CAN. 5. Monitor for ECU response and behavior. 6. Log all actions and changes in vehicle state. 7. Remove scripts and logs if necessary.
- **Detection**: Audit infotainment firmware interfaces
- **Solution**: Segment CAN network zones by trust level
- **Tags**: CAN, head unit, ECU bridge

## Infotainment Firmware Downgrade Abuse

- **Attack Type**: Local Exploitation
- **Target**: Infotainment System
- **Vulnerability**: Firmware downgrade without verification
- **MITRE**: TA0001: Initial Access
- **Impact**: Brings back exploitable flaws for attacker
- **Tools**: Firmware image, USB drive
- **Scenario**: Attacker downgrades firmware to vulnerable version via USB update
- **Attack Steps**: 1. Obtain an older, vulnerable version of infotainment firmware. 2. Format USB as required and place update files on root. 3. Plug USB into vehicle’s media port. 4. Trigger manual update via settings menu or key sequence. 5. Downgrade proceeds without signature validation. 6. Exploit the known flaw (e.g., directory traversal or RCE). 7. Clean up update files after use.
- **Detection**: Detect firmware mismatch and manual updates
- **Solution**: Enforce signed updates and rollback protection
- **Tags**: firmware downgrade, infotainment, update hack

## Telematics SIM Swap for Location Spoof

- **Attack Type**: Physical Access
- **Target**: Telematics Unit
- **Vulnerability**: No SIM binding, no backend validation
- **MITRE**: TA0001: Initial Access
- **Impact**: Spoofed vehicle telemetry for fraud or theft
- **Tools**: SIM card tools, SDR
- **Scenario**: Attacker swaps out vehicle’s SIM to hijack connection and send fake data
- **Attack Steps**: 1. Access telematics unit physically and extract embedded SIM. 2. Replace with attacker-controlled SIM that connects to rogue backend. 3. Send GPS/location or telemetry spoofing data via alternate network. 4. Vehicle backend receives fake data, misleading remote apps. 5. Maintain fake backend server for interaction. 6. Capture and forward logs to mislead detection tools. 7. Reinsert original SIM if needed to avoid suspicion.
- **Detection**: Monitor SIM ICCID and backend IP changes
- **Solution**: Bind SIM to device IMEI, enforce IP filtering
- **Tags**: sim swap, telematics, spoofing, GPS

## Replay Attack to Open Doors

- **Attack Type**: CAN Bus Injection
- **Target**: Car ECU (Body Control Module)
- **Vulnerability**: Lack of authentication in CAN messaging
- **MITRE**: T1611 (Replay Attack)
- **Impact**: Unauthorized physical access
- **Tools**: CANSniffer, ICSim, USB2CAN
- **Scenario**: Attacker replays previously captured CAN messages to unlock the doors of a vehicle without needing the original key fob.
- **Attack Steps**: 1. Connect to the vehicle’s CAN bus via OBD-II port using USB2CAN adapter. 2. Use CANSniffer or ICSim to monitor CAN traffic while a user unlocks the car with a remote. 3. Identify and isolate the exact message responsible for unlocking. 4. Save this message and replay it while the car is off and no key fob is nearby. 5. Observe the doors unlock, proving the replay was successful.
- **Detection**: Monitor for repeated identical CAN messages
- **Solution**: Implement message counters or rolling codes
- **Tags**: replay, CAN injection, physical access

## Engine Start via Replay

- **Attack Type**: CAN Bus Injection
- **Target**: Vehicle Powertrain ECU
- **Vulnerability**: No encryption or authentication of engine start messages
- **MITRE**: T1611
- **Impact**: Unauthorized engine start
- **Tools**: SavvyCAN, USB2CAN, ICSim
- **Scenario**: Replay of engine start CAN frames to remotely start a vehicle's engine without a key.
- **Attack Steps**: 1. Tap into CAN bus using a USB2CAN adapter. 2. Monitor CAN traffic using SavvyCAN while someone starts the engine. 3. Log the engine start sequence. 4. Later, replay the captured message using the same tool. 5. Observe engine ignition without the physical key present.
- **Detection**: Monitor ignition status against driver presence
- **Solution**: Require encrypted key fob handshake
- **Tags**: engine spoofing, replay, CAN start

## Fuzz Brake System

- **Attack Type**: CAN Bus Fuzzing
- **Target**: Brake ECU
- **Vulnerability**: Poor input validation in CAN parser
- **MITRE**: T1499 (Endpoint DoS)
- **Impact**: Vehicle safety disruption
- **Tools**: CANFuzz, CANToolz, ICSim
- **Scenario**: Random CAN messages are injected to cause erratic brake system behavior or ECU crash.
- **Attack Steps**: 1. Set up ICSim virtual car environment or use a test vehicle. 2. Use CANFuzz to inject randomized CAN messages into the brake-related CAN ID range. 3. Monitor the response—e.g., sudden braking, system error, or no reaction. 4. Log crashes or malfunctions and correlate them to specific message formats. 5. Repeat and refine fuzzing to target weaknesses.
- **Detection**: Log CAN errors or invalid CRCs
- **Solution**: Harden input parsing, rate-limit input
- **Tags**: fuzzing, safety-critical, CAN brute

## Throttle Spoofing Attack

- **Attack Type**: CAN Bus Spoofing
- **Target**: Engine ECU
- **Vulnerability**: Trusts unauthenticated throttle inputs
- **MITRE**: T1565.001
- **Impact**: Acceleration without driver input
- **Tools**: ICSim, CANalyzer
- **Scenario**: Spoofed CAN messages simulate throttle input, causing vehicle acceleration without driver action.
- **Attack Steps**: 1. Analyze throttle input CAN messages using ICSim while a driver accelerates. 2. Replicate the message structure and frequency. 3. Disconnect actual throttle sensor input (if safe/testing). 4. Inject spoofed throttle messages at the correct CAN ID. 5. Observe vehicle acceleration despite no driver input.
- **Detection**: Compare physical input to CAN message data
- **Solution**: Secure CAN IDs with authentication layers
- **Tags**: spoofing, acceleration, throttle spoof

## Disable Airbag System

- **Attack Type**: CAN Bus Injection
- **Target**: Safety ECU
- **Vulnerability**: No integrity check of airbag messages
- **MITRE**: T1562.001
- **Impact**: Safety system failure
- **Tools**: CANtact, Wireshark, ICSim
- **Scenario**: Injection of specific messages disables airbag module, preventing deployment in crash.
- **Attack Steps**: 1. Identify CAN ID and data format related to airbag status using diagnostic tools. 2. Craft a message that sets the airbag state to "off" or "malfunction." 3. Inject it repeatedly using CANtact or compatible hardware. 4. Simulate crash scenario or use scan tool to verify airbag is now disabled.
- **Detection**: Compare expected vs actual module status
- **Solution**: Enforce digital signatures for safety-critical CAN IDs
- **Tags**: airbag attack, safety bypass

## Overwrite Gear Position

- **Attack Type**: CAN Bus Spoofing
- **Target**: Transmission ECU
- **Vulnerability**: Blind trust in gear input messages
- **MITRE**: T1620
- **Impact**: Disorientation, potential driver confusion
- **Tools**: CANBus Triple, ICSim
- **Scenario**: Attacker sends spoofed gear position signals to simulate shift into reverse while in drive.
- **Attack Steps**: 1. Monitor gear selection messages while shifting between gears. 2. Identify gear position CAN ID and structure. 3. Craft a spoofed message indicating a different gear (e.g., reverse). 4. Inject during drive and observe display/confusion. 5. Optionally, combine with camera activation for visual manipulation.
- **Detection**: Detect implausible gear shifts in logs
- **Solution**: Validate signal via sensor fusion
- **Tags**: gear spoof, driver confusion, sensor spoofing

## Crash Telematics ECU via Fuzz

- **Attack Type**: CAN Bus Fuzzing
- **Target**: Telematics ECU
- **Vulnerability**: Poorly handled malformed CAN input
- **MITRE**: T1499
- **Impact**: DoS on tracking or communication system
- **Tools**: CANToolz, CANFuzz
- **Scenario**: Send malformed CAN messages targeting telematics unit to cause denial of service.
- **Attack Steps**: 1. Connect to the CAN bus connected to the telematics module. 2. Use CANFuzz to send malformed or incomplete frames at high frequency. 3. Observe if the telematics system stops responding or reboots. 4. Log the response and identify threshold conditions.
- **Detection**: Monitor uptime/heartbeat of module
- **Solution**: Input sanitization, watchdog timers
- **Tags**: fuzzing, DoS, telematics

## ECU Fingerprinting via Response Timing

- **Attack Type**: CAN Bus Reconnaissance
- **Target**: All ECUs
- **Vulnerability**: Leaky diagnostic response timing
- **MITRE**: T1592
- **Impact**: Precision targeting of known vulnerable modules
- **Tools**: python-can, ICSim
- **Scenario**: Measure ECU response time to crafted queries to fingerprint vehicle model or software version.
- **Attack Steps**: 1. Send diagnostic queries (e.g., UDS requests) to specific ECUs. 2. Measure the response latency using timestamped logs. 3. Use this timing to identify ECU model or firmware version. 4. Craft attack payloads targeting known vulnerabilities.
- **Detection**: Track ECU response profiles
- **Solution**: Standardize response handling across models
- **Tags**: ECU fingerprint, info leak

## Brake Message Flooding

- **Attack Type**: CAN Bus DoS
- **Target**: Brake ECU
- **Vulnerability**: CAN arbitration abuse, message flooding
- **MITRE**: T1499
- **Impact**: Brake failure or input lag
- **Tools**: CANBus Triple, SavvyCAN
- **Scenario**: Flood the CAN bus with fake brake messages, delaying or suppressing real ones.
- **Attack Steps**: 1. Identify CAN ID for brake pressure or application. 2. Craft messages that mimic real brake data. 3. Flood the CAN bus at high frequency, overwhelming the queue. 4. Monitor for delayed or dropped legitimate brake messages.
- **Detection**: Monitor message frequency and CRC errors
- **Solution**: Enforce bus prioritization and filters
- **Tags**: flood, brake DoS, denial-of-brake

## Immobilizer Bypass with Fake Start Message

- **Attack Type**: CAN Bus Spoofing
- **Target**: Immobilizer Module
- **Vulnerability**: Weak or no encryption on start approval
- **MITRE**: T1557.002
- **Impact**: Unauthorized vehicle operation
- **Tools**: ICSim, USB2CAN
- **Scenario**: Send fake start approval messages to bypass vehicle’s immobilizer system.
- **Attack Steps**: 1. Log CAN messages during a valid engine start to locate immobilizer handshake. 2. Replay or spoof the message using USB2CAN. 3. Attempt engine ignition without a valid key. 4. Observe engine cranking despite lack of authentication.
- **Detection**: Detect start command inconsistencies
- **Solution**: Require strong crypto handshake
- **Tags**: keyless start spoof, immobilizer bypass

## Door Unlock Replay via CAN Bus

- **Attack Type**: Replay Attack
- **Target**: Car Door ECU
- **Vulnerability**: Lack of authentication on CAN messages
- **MITRE**: T1636.002
- **Impact**: Unauthorized access to vehicle
- **Tools**: CANSniffer, ICSim, CAN-utils
- **Scenario**: Attacker records CAN messages related to door unlocking and replays them later to gain unauthorized access
- **Attack Steps**: 1. Physically connect to the vehicle’s OBD-II port using a USB2CAN device. 2. Launch a CAN message sniffer (e.g., candump) and observe traffic while the legitimate user unlocks the door using a key fob. 3. Identify the CAN ID and payload responsible for the unlock action. 4. Store the message for replay. 5. Re-inject the same CAN frame using canplayer while standing near the vehicle. 6. Observe the door unlocking without the key fob, demonstrating a successful replay attack.
- **Detection**: Monitor for repeated identical CAN frames
- **Solution**: Introduce message authentication codes (MAC) or counters
- **Tags**: canbus, replay, physical-access, OBD-II

## Fuzzing CAN Bus for Crash Conditions

- **Attack Type**: Message Fuzzing
- **Target**: Vehicle ECU
- **Vulnerability**: No input validation in ECU firmware
- **MITRE**: T0810
- **Impact**: ECU instability or denial-of-service
- **Tools**: CANFuzz, ICSim, Python-can
- **Scenario**: Attacker sends malformed/random CAN frames to identify vulnerabilities in ECUs
- **Attack Steps**: 1. Connect to the CAN bus via OBD-II using a CAN interface. 2. Use CANFuzz or write a fuzzing script to randomly mutate known message formats and IDs. 3. Inject fuzzed messages at a high rate for a fixed duration. 4. Monitor for abnormal behavior like warning lights, ECU reboots, or unresponsiveness. 5. Log which fuzzed messages led to disruptions for deeper analysis.
- **Detection**: Compare baseline behavior with anomalies
- **Solution**: Harden ECU firmware with strict CAN frame validation
- **Tags**: fuzzing, canbus, crash-testing

## Spoof Brake Command to Cause Sudden Stop

- **Attack Type**: Spoofing
- **Target**: Brake Control ECU
- **Vulnerability**: CAN lacks authentication or source validation
- **MITRE**: T1582
- **Impact**: Unsafe driving, potential crash
- **Tools**: CANtact Pro, Scapy-can
- **Scenario**: Attacker injects false braking commands by impersonating the brake control ECU
- **Attack Steps**: 1. Connect CANtact Pro to the vehicle’s internal CAN bus. 2. Analyze traffic to isolate brake command messages based on IDs and behavior. 3. Craft spoofed CAN frames mimicking the brake ECU's structure but modifying payloads to simulate hard braking. 4. Transmit spoofed frames at regular intervals. 5. Observe vehicle slowing or stopping even if brakes weren't pressed.
- **Detection**: Look for out-of-context braking without pedal press
- **Solution**: Use CAN intrusion detection systems (IDS)
- **Tags**: spoofing, brake, ecu, critical-safety

## Replay Throttle Acceleration via Recorded Frame

- **Attack Type**: Replay Attack
- **Target**: Engine ECU
- **Vulnerability**: No verification of command origin
- **MITRE**: T1496
- **Impact**: Vehicle moves without driver input
- **Tools**: CAN-utils, ICSim
- **Scenario**: Throttle-up CAN frame is recorded during acceleration and replayed to induce unintended vehicle acceleration
- **Attack Steps**: 1. Use USB2CAN and candump to record traffic while stepping on the accelerator. 2. Isolate throttle-related messages by comparing idle vs. active acceleration states. 3. Save message and timestamp data. 4. Re-inject the acceleration frame using canplayer. 5. Confirm whether the engine revs or vehicle moves forward without driver input.
- **Detection**: Baseline throttle patterns + anomaly detection
- **Solution**: Secure ECUs with origin verification logic
- **Tags**: replay, throttle, unsafe-action

## Fuzzing Gear Shift Messages to Induce Gear Drop

- **Attack Type**: Message Fuzzing
- **Target**: Transmission ECU
- **Vulnerability**: Lack of boundary checks in firmware
- **MITRE**: T0810
- **Impact**: Unsafe gear behavior or failure
- **Tools**: Python-can, ICSim
- **Scenario**: Fuzzed messages targeting gear control lead to unexpected shifts or ECU crash
- **Attack Steps**: 1. Tap into the CAN network through OBD-II port using CANable. 2. Identify gear-related frames by logging traffic during normal gear changes. 3. Create a fuzzer that randomizes payloads for gear message IDs. 4. Inject mutated messages and observe transmission behavior. 5. Detect anomalies like gear slipping, refusal to engage, or dashboard errors.
- **Detection**: Compare transmission logs with expected patterns
- **Solution**: Implement CAN input sanitization in firmware
- **Tags**: gear, fuzzing, transmission, icssim

## ECU Impersonation via ID Collision

- **Attack Type**: Spoofing
- **Target**: Steering ECU
- **Vulnerability**: CAN arbitration not sufficient for identity
- **MITRE**: T1582
- **Impact**: Dangerous override of legitimate ECU
- **Tools**: Scapy, CANtact, ICSim
- **Scenario**: Attacker impersonates an existing ECU by transmitting messages with same CAN ID
- **Attack Steps**: 1. Log all active CAN IDs to identify frequently used ones. 2. Choose a high-priority ID (e.g., steering or throttle). 3. Construct spoof messages with identical ID but custom payloads. 4. Inject spoofed messages at high frequency to override legitimate data. 5. Monitor for overridden behavior like changed steering angle.
- **Detection**: Use CAN bus entropy monitoring
- **Solution**: Employ message signing or ID filtering
- **Tags**: spoofing, ecu-id, collision

## CAN Frame Injection via Bluetooth Exploit

- **Attack Type**: Remote Injection
- **Target**: Infotainment ECU
- **Vulnerability**: Bluetooth stack RCE enables lateral movement
- **MITRE**: T1476
- **Impact**: Remote vehicle manipulation
- **Tools**: Custom Bluetooth exploit, BlueBorne POC
- **Scenario**: Exploit a Bluetooth flaw in infotainment to inject CAN frames
- **Attack Steps**: 1. Scan vehicle for discoverable Bluetooth interfaces. 2. Exploit known vulnerability (e.g., BlueBorne) in infotainment system. 3. Escalate privileges to gain access to internal bus bridge. 4. Craft and transmit CAN messages targeting critical ECUs. 5. Confirm actions like horn honk, unlock, or display change occur.
- **Detection**: Bluetooth logs + CAN injection detection
- **Solution**: Patch Bluetooth vulnerabilities, network segmentation
- **Tags**: bluetooth, rce, remote-injection

## Door Lock Denial Using Repeated CAN Flood

- **Attack Type**: DoS via CAN Flood
- **Target**: Door Lock ECU
- **Vulnerability**: Bus bandwidth exhaustion
- **MITRE**: T1499
- **Impact**: Loss of control over door locks
- **Tools**: CAN-utils, bash loop script
- **Scenario**: Repeated door lock/unlock messages flood the bus and prevent valid operation
- **Attack Steps**: 1. Capture a door unlock message with candump. 2. Use a shell script or Python loop to replay it repeatedly using cansend. 3. Overload the CAN bus so no new messages can be processed. 4. Observe door lock mechanism becoming unresponsive or erratic.
- **Detection**: Monitor for high frame frequency per ID
- **Solution**: Rate-limit or drop excessive identical frames
- **Tags**: denial, flood, canbus, unlock-loop

## Speedometer Spoof for False Readings

- **Attack Type**: Spoofing
- **Target**: Instrument Cluster
- **Vulnerability**: Lack of data authenticity
- **MITRE**: T1582
- **Impact**: Misleading speed, confusion
- **Tools**: ICSim, Scapy
- **Scenario**: Fake speed CAN frames sent to cluster to manipulate speed reading
- **Attack Steps**: 1. Record CAN messages during different speeds. 2. Isolate speed-related messages using ICSim. 3. Craft spoofed speed frames (e.g., 120 km/h) and send via USB2CAN. 4. Observe manipulated readings on instrument cluster.
- **Detection**: Cross-check real wheel sensor output
- **Solution**: Sign or cross-verify messages from known source
- **Tags**: spoof, speedo, instrument-hack

## Critical ECU Overwrite via Continuous Injection

- **Attack Type**: Persistent Spoofing
- **Target**: Safety-Critical ECUs
- **Vulnerability**: Lack of message source enforcement
- **MITRE**: T1582
- **Impact**: Loss of safety-critical function
- **Tools**: CANtact, Python-can
- **Scenario**: Overwrite critical ECU decisions (e.g., airbag, brakes) by flooding spoofed high-priority messages
- **Attack Steps**: 1. Determine CAN IDs used by critical safety ECUs. 2. Craft spoofed messages that take precedence due to arbitration. 3. Continuously inject spoofed messages with high-priority timing. 4. Observe legitimate ECU behavior being overridden.
- **Detection**: Monitor arbitration abuse or spoof detection
- **Solution**: Add source-auth checks & watchdog logic
- **Tags**: spoof, safety, critical-ecu

## Replay Attack to Unlock Vehicle Doors

- **Attack Type**: CAN Bus Injection (Replay)
- **Target**: Vehicle CAN Bus
- **Vulnerability**: Lack of encryption and replay protection in CAN frames
- **MITRE**: T1210 (Exploitation of Remote Services)
- **Impact**: Unauthorized door unlock
- **Tools**: CANtact, Wireshark, ICSim
- **Scenario**: Attacker replays a captured CAN frame that unlocks car doors
- **Attack Steps**: 1. Connect CANtact to the vehicle’s OBD-II port.2. Start candump to monitor live CAN traffic.3. Press the unlock button and capture the related CAN ID and data.4. Save the packet using can-utils.5. Re-inject the same packet with cansend while the key fob is far away.6. Observe that the car unlocks without original key interaction.7. Repeat to verify replayability.
- **Detection**: Monitor for repeated identical CAN messages from unknown tools
- **Solution**: Use rolling codes or frame counters in CAN architecture
- **Tags**: CAN Injection, Replay, Remote Unlock, Physical Access

## Spoofing Brake Message While Moving

- **Attack Type**: CAN Bus Injection (Spoofing)
- **Target**: Brake ECU
- **Vulnerability**: Lack of authentication and validation on CAN IDs
- **MITRE**: T1562.001 (Input Injection)
- **Impact**: Potentially unsafe emergency braking
- **Tools**: CANToolz, ICSim, SocketCAN
- **Scenario**: Attacker spoofs a message to falsely trigger brakes during vehicle motion
- **Attack Steps**: 1. Attach an interface like USB2CAN to the vehicle’s CAN port.2. Use ICSim or Wireshark to monitor live CAN traffic while braking.3. Identify the CAN ID related to braking actions.4. Craft a new CAN frame with same ID and altered data payload.5. Replay the spoofed message while the vehicle is moving.6. ECU may interpret the spoofed command and attempt braking action.
- **Detection**: Look for brake commands without matching pedal sensor data
- **Solution**: Implement message authentication and sanity-check sensors
- **Tags**: Brake Spoofing, ECU, Unsafe Commands, CAN Spoofing

## Fuzzing Random CAN IDs to Crash ECUs

- **Attack Type**: CAN Bus Injection (Fuzzing)
- **Target**: Vehicle CAN Network
- **Vulnerability**: Lack of input validation on CAN IDs
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: ECU Crash or Faulty Behavior
- **Tools**: CANFuzz, Scapy, ICSim
- **Scenario**: Sending random CAN IDs/data causes ECU misbehavior or crash
- **Attack Steps**: 1. Connect to CAN bus using CANtact or USB2CAN.2. Run CANFuzz or custom Scapy scripts.3. Generate randomized CAN IDs and payload data.4. Continuously send the fuzzed messages into the vehicle network.5. Observe if any ECU enters error state or unresponsive behavior.6. Log which ID and payload caused abnormal response for further triage.
- **Detection**: Monitor CAN network for malformed or invalid ID bursts
- **Solution**: Harden ECU firmware to reject malformed or unknown IDs
- **Tags**: CAN Fuzzing, Crash, Scapy, Randomized Packets

## Replay Throttle Signal to Accelerate

- **Attack Type**: CAN Bus Injection (Replay)
- **Target**: Throttle Control ECU
- **Vulnerability**: No cryptographic validation of control messages
- **MITRE**: T1609.002 (Command and Control Protocol)
- **Impact**: Unsafe acceleration without driver input
- **Tools**: ICSim, can-utils, USB2CAN
- **Scenario**: Replay of a captured throttle signal results in vehicle acceleration
- **Attack Steps**: 1. Record CAN traffic during throttle pedal press using candump.2. Identify and extract throttle-related messages.3. Save them using log2asc or candump -l.4. Re-inject these messages using cansend or a loop script.5. Observe vehicle acceleration behavior in simulation or actual ECU.6. Repeat in controlled lab to validate risk.
- **Detection**: Watch for throttle changes without pedal sensor agreement
- **Solution**: Apply secure ECU communication via authentication
- **Tags**: Throttle, Replay, Unsafe Acceleration, ICSim

## Spoof Gear Shift to Neutral

- **Attack Type**: CAN Bus Injection (Spoofing)
- **Target**: Transmission ECU
- **Vulnerability**: Unauthenticated control signal transmission
- **MITRE**: T1562.004 (Disable or Modify System)
- **Impact**: Loss of propulsion during drive
- **Tools**: ICSim, CANtact, Python
- **Scenario**: Gear spoofing during movement can disengage engine power unexpectedly
- **Attack Steps**: 1. Use ICSim to observe the gear shift CAN IDs.2. Simulate gear changes and correlate which ID controls it.3. Construct a spoofed CAN frame that forces gear into ‘N’ (neutral).4. Inject this spoofed frame during acceleration.5. Monitor if ECU reacts and engine disengages.6. Repeat test on bench setup before road trial.
- **Detection**: Anomalous gear shift without driver interaction
- **Solution**: Add gear position sensor integrity checks
- **Tags**: Gear Spoofing, Transmission, ECU Hijack

## Frame Injection Loop for Persistent Unlock

- **Attack Type**: CAN Bus Injection (Replay)
- **Target**: Door Locking System
- **Vulnerability**: No timeout or sequence validation for commands
- **MITRE**: T1210
- **Impact**: Persistent unauthorized access to vehicle
- **Tools**: can-utils, bash script
- **Scenario**: Replay unlock message in loop to repeatedly open doors every few seconds
- **Attack Steps**: 1. Capture the unlock message with candump.2. Create a bash script to replay it every few seconds using cansend.3. Run the script and observe doors unlocking repeatedly.4. Let the user move away with keys.5. Use this to prevent the car from staying locked.6. Stop the script and verify normal locking resumes.
- **Detection**: Monitor CAN for periodic identical frames with no driver presence
- **Solution**: Add sequence numbers or challenge-response to commands
- **Tags**: Loop Injection, Unlock Persistence, Replay

## Flood CAN Bus to Deny ECU Communication

- **Attack Type**: CAN Bus Injection (Fuzzing)
- **Target**: Entire CAN Network
- **Vulnerability**: No rate limiting or bandwidth control
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Temporary system-wide ECU failure
- **Tools**: Scapy, SocketCAN, CANFlood
- **Scenario**: Flooding CAN traffic prevents legitimate ECU communication
- **Attack Steps**: 1. Setup CAN interface with ip link set can0 up type can bitrate 500000.2. Use CANFlood tool or Scapy to send a high rate of random messages.3. Monitor ECU logs for timeout errors.4. Confirm loss of vehicle function like lights or speedometer.5. Note any DTCs generated due to communication timeout.6. Stop flood and observe recovery.
- **Detection**: Monitor CAN bus load and detect over-saturation
- **Solution**: Add watchdog timeouts and rate control logic in ECUs
- **Tags**: CAN DoS, Flooding, Bus Saturation

## Message Injection to Disable Headlights

- **Attack Type**: CAN Bus Injection (Spoofing)
- **Target**: Lighting Control ECU
- **Vulnerability**: Lack of validation for lighting commands
- **MITRE**: T1565.001 (Data Manipulation)
- **Impact**: Headlights disabled while driving at night
- **Tools**: ICSim, CANtact, Python
- **Scenario**: Attacker disables vehicle headlights via crafted CAN messages
- **Attack Steps**: 1. Turn headlights on and capture related CAN frames.2. Identify the ID controlling headlight state.3. Create spoofed frame with ‘off’ payload.4. Inject it into CAN repeatedly.5. Observe headlight shutdown.6. Test in lab and simulate nighttime conditions.7. Add logging to catch repeated headlight command spoofing.
- **Detection**: Unexpected headlight state transitions
- **Solution**: Require physical switch validation before CAN override
- **Tags**: Headlight Spoof, Lighting ECU, Unsafe Night Drive

## Override Steering Input via Spoofing

- **Attack Type**: CAN Bus Injection (Spoofing)
- **Target**: Steering ECU
- **Vulnerability**: Trust-based message handling without integrity checks
- **MITRE**: T1562
- **Impact**: Erratic or overridden steering behavior
- **Tools**: CANtact, ICSim, CANard
- **Scenario**: Send spoofed steering commands to override or interfere with driver input
- **Attack Steps**: 1. Identify steering CAN ID using ICSim trace.2. Simulate left/right turn and log related messages.3. Craft spoofed steering frame while maintaining same ID.4. Inject during driving (simulated).5. ECU may get confused if real and spoofed data conflict.6. Observe any erratic or ignored inputs.7. Use CANard for advanced collision analysis.
- **Detection**: Conflict detection between wheel sensor and CAN traffic
- **Solution**: Implement secure steering ECUs with data fusion
- **Tags**: Steering Spoofing, CAN Injection, Safety Risk

## CAN Bus Collision with Conflicting IDs

- **Attack Type**: CAN Bus Injection (Fuzzing)
- **Target**: Multiple ECUs
- **Vulnerability**: Exploitable arbitration logic in CAN
- **MITRE**: T1499
- **Impact**: ECU delays, message loss, potential unsafe behavior
- **Tools**: ICSim, CANalyzer, Python
- **Scenario**: Send messages with duplicate high-priority IDs to cause message collision
- **Attack Steps**: 1. Connect to CAN using CANtact and ICSim.2. Identify high-priority arbitration IDs (lower value = higher priority).3. Send conflicting messages with same ID but different payloads.4. Observe which wins arbitration.5. Repeat rapidly to saturate the bus.6. Record ECU confusion or delays.7. Use CANalyzer to visualize collisions.
- **Detection**: Analyze arbitration fairness and timing in the logs
- **Solution**: Move to CAN FD with authentication and bus segmentation
- **Tags**: CAN Collision, Arbitration Abuse, Bus Hijack

## Malicious MP4 Exploit in Car Player

- **Attack Type**: Media File Exploit
- **Target**: Infotainment System
- **Vulnerability**: Media decoding vulnerability
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Remote Code Execution, System Crash
- **Tools**: Custom FFMPEG payload, USB
- **Scenario**: An attacker sends a maliciously crafted MP4 video to the vehicle owner via Bluetooth or USB. Playing it triggers a buffer overflow in the media engine.
- **Attack Steps**: 1. Craft a malicious MP4 file using a known CVE in the car’s media decoder. 2. Embed shellcode to attempt arbitrary code execution. 3. Load file via USB, SD card, or Bluetooth media transfer. 4. Victim opens the media file on the infotainment screen. 5. Code executes in the context of the media player, enabling remote access or crash.
- **Detection**: Log monitoring, crash dumps
- **Solution**: Patch vulnerable codecs; enable strict input validation
- **Tags**: infotainment, mp4, media exploit

## JPEG Parsing Bug to Freeze Infotainment

- **Attack Type**: Media File Exploit
- **Target**: Infotainment System
- **Vulnerability**: JPEG image parsing bug
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Infotainment DoS, degraded UX
- **Tools**: Hex editor, AFL, CANsniffer
- **Scenario**: Malformed JPEG images exploit memory parsing issues in the car's image viewer module.
- **Attack Steps**: 1. Use fuzzing to discover JPEG structures that crash the parser. 2. Create a crafted image that leads to a NULL pointer dereference. 3. Send it over Bluetooth or USB as a wallpaper or gallery file. 4. When the user views the image, the infotainment OS freezes. 5. The vehicle reboots or becomes unresponsive until a reset.
- **Detection**: Watchdog logs, memory crash traces
- **Solution**: Apply input sanitization; validate JPEG formats
- **Tags**: jpeg, dos, fuzzing

## USB Firmware Dropper Attack

- **Attack Type**: USB Firmware Attack
- **Target**: Infotainment System
- **Vulnerability**: Lack of firmware integrity checks
- **MITRE**: T1542.001 (Firmware)
- **Impact**: Full control over infotainment unit
- **Tools**: USB Rubber Ducky, Custom firmware blob
- **Scenario**: Malicious firmware dropped via USB impersonates a legitimate infotainment update.
- **Attack Steps**: 1. Clone legitimate firmware update structure. 2. Insert shellcode/payload in a rarely validated section. 3. Rename and sign the firmware with spoofed keys (if not verified). 4. Place it on a USB labeled “System Update”. 5. Insert into car’s USB slot. 6. If the infotainment lacks proper validation, it installs the malicious update.
- **Detection**: USB access logs, firmware hash diff
- **Solution**: Enforce cryptographic signature validation for firmware
- **Tags**: usb, firmware, update bypass

## Reverse Shell via MP3 Metadata

- **Attack Type**: Media File Exploit
- **Target**: Infotainment System
- **Vulnerability**: Buffer overflow in ID3 parser
- **MITRE**: T1203
- **Impact**: Remote access, unauthorized control
- **Tools**: MP3TagTool, ExploitDB payload
- **Scenario**: MP3 file contains malicious metadata (ID3 tag) causing buffer overflow.
- **Attack Steps**: 1. Create MP3 file with an overlong ID3v2 tag. 2. Insert shellcode in the tag field using a hex editor. 3. Deliver via USB or Bluetooth media sync. 4. On playback, the media parser overflows and hijacks execution. 5. Attacker gains remote shell or access to CAN bus.
- **Detection**: Heap overflow traces, parser logs
- **Solution**: Harden media parser, enforce max-length constraints
- **Tags**: mp3, infotainment, reverse shell

## Exploit CarPlay App Debug Flag

- **Attack Type**: App Exploitation
- **Target**: Infotainment System
- **Vulnerability**: Enabled debug interfaces in production
- **MITRE**: T1525 (Implant Internal Image)
- **Impact**: App compromise, system breach
- **Tools**: iOS Dev Tools, Burp Suite
- **Scenario**: CarPlay-based custom app includes debug hooks not disabled in production.
- **Attack Steps**: 1. Analyze custom CarPlay app for exposed debug endpoints. 2. Use an iOS device to sideload modified CarPlay apps. 3. Exploit the debug interface to read memory or execute shell commands. 4. Relay commands to the infotainment system backend.
- **Detection**: App behavior analysis, network logs
- **Solution**: Strip debug builds, perform code review
- **Tags**: ios, carplay, debug

## Android Auto App Hijacking

- **Attack Type**: App Exploitation
- **Target**: Infotainment System
- **Vulnerability**: Weak app verification
- **MITRE**: T1078.001 (Valid Accounts: Default Accounts)
- **Impact**: Command injection, data theft
- **Tools**: Apktool, Android Studio
- **Scenario**: Attacker installs a malicious Android Auto app that mimics a trusted one.
- **Attack Steps**: 1. Clone a legitimate Android Auto app using Apktool. 2. Modify manifest to request elevated permissions. 3. Insert malicious code to interface with infotainment head unit. 4. Distribute app via phishing or fake APK site. 5. Once installed, it sends commands to infotainment over USB tethering.
- **Detection**: App installation records, USB comms
- **Solution**: Restrict app sync to verified apps only
- **Tags**: android, auto, apk, reverse engineering

## Firmware Backdoor in Update Package

- **Attack Type**: USB Firmware Attack
- **Target**: Infotainment System
- **Vulnerability**: Firmware modification with hidden backdoor
- **MITRE**: T1542.001
- **Impact**: Persistent remote control
- **Tools**: Ghidra, USB Toolkit
- **Scenario**: Backdoored infotainment update package with hidden command listener.
- **Attack Steps**: 1. Reverse engineer the existing firmware with Ghidra. 2. Add a listening socket and payload dropper in the idle loop. 3. Repack and checksum to match the original format. 4. Deliver over USB as a routine update. 5. Once installed, attacker can connect over Wi-Fi or LTE to issue commands.
- **Detection**: Network traffic anomalies
- **Solution**: Sign and verify firmware at boot
- **Tags**: infotainment, backdoor, ghidra

## Video Subtitle Attack

- **Attack Type**: Media File Exploit
- **Target**: Infotainment System
- **Vulnerability**: Subtitle parsing vulnerability
- **MITRE**: T1203
- **Impact**: Code execution on playback
- **Tools**: VLC exploit mod, SubtitleEdit
- **Scenario**: Subtitles in video files (e.g., .srt) used to exploit parsing bug in video player.
- **Attack Steps**: 1. Craft a malicious .srt subtitle file with malformed tags. 2. Bind it to a movie file. 3. Share it with the target via USB drive. 4. When video plays, subtitle parser crashes or runs shellcode. 5. May allow for privilege escalation or remote shell.
- **Detection**: Media logs, subtitle load failure
- **Solution**: Patch subtitle engines; validate syntax
- **Tags**: subtitle, srt, buffer overflow

## Exploit via Malicious USB-C Android Connection

- **Attack Type**: App Exploitation
- **Target**: Infotainment System
- **Vulnerability**: Debug mode via USB Android Auto
- **MITRE**: T1543
- **Impact**: Infotainment reconfiguration, potential RCE
- **Tools**: Android Debug Bridge, USB HID Spoofer
- **Scenario**: Android device impersonates a dev/debug unit, bypasses controls.
- **Attack Steps**: 1. Create a modified Android OS build with a debug key. 2. Enable USB Host Debugging and HID injection. 3. Connect to vehicle via Android Auto. 4. Issue raw commands to the infotainment over USB. 5. Attempt command execution or configuration change.
- **Detection**: USB transport logs, Android pairing logs
- **Solution**: Enforce trusted pairing and ADB restrictions
- **Tags**: android auto, debug, usb spoof

## Android Auto Log File Leak

- **Attack Type**: App Exploitation
- **Target**: Infotainment System
- **Vulnerability**: Poor log hygiene in mobile app
- **MITRE**: T1552.003 (Unprotected Logs)
- **Impact**: Credential exposure, data leakage
- **Tools**: Logcat, Frida, Apktool
- **Scenario**: A poorly coded Android Auto app logs sensitive data like tokens or GPS to readable logs.
- **Attack Steps**: 1. Decompile app and inspect for Log.d and Log.e usage. 2. Find hardcoded GPS, tokens, or auth data. 3. Install and launch app in car-connected state. 4. Extract logs using ADB or Frida on-device. 5. Leak credentials or gain user insight.
- **Detection**: ADB log dump, Frida memory access
- **Solution**: Secure code audit, remove logging in release
- **Tags**: logging, android, infotainment

## JPEG-Based Infotainment Crash

- **Attack Type**: Media File Exploit
- **Target**: Infotainment System
- **Vulnerability**: Input validation bug in image parsing engine
- **MITRE**: T1203
- **Impact**: DoS or crash of infotainment interface
- **Tools**: Hex Fiend, AFL++, ImageMagick
- **Scenario**: An attacker targets the vehicle's infotainment system by embedding a malformed JPEG image into a USB-loaded photo album, crashing the image parser.
- **Attack Steps**: 1. Create a malformed JPEG image using tools like AFL++ or manually corrupting bytes using Hex Fiend. 2. Place the image in a folder on a USB drive. 3. Insert the USB into the car's infotainment system. 4. When the image is rendered by the media viewer, observe the crash or hang. 5. Monitor infotainment reboot or diagnostic messages via serial port or screen logs.
- **Detection**: Logging USB activity, crash logs
- **Solution**: Patch the image rendering engine, add file format validation layer
- **Tags**: jpeg, crash, media exploit, usb injection

## MP4 Subtitle Overflow Attack

- **Attack Type**: Media File Exploit
- **Target**: Infotainment System
- **Vulnerability**: Buffer overflow in subtitle parsing module
- **MITRE**: T1203
- **Impact**: System instability or crash
- **Tools**: MP4Box, SubtitleEdit, ffmpeg
- **Scenario**: A specially crafted MP4 video file with a malicious subtitle file crashes the infotainment player during rendering.
- **Attack Steps**: 1. Use SubtitleEdit to craft a subtitle file with extremely long lines or corrupt time stamps. 2. Embed the subtitle in an MP4 container using MP4Box or ffmpeg. 3. Load the video onto a USB or stream it via Bluetooth. 4. Play the video in the vehicle's media player. 5. Observe unexpected behavior such as crashing, freezing, or looping.
- **Detection**: Crash dump analysis, infotainment logs
- **Solution**: Implement bounds checks, sanitize subtitle inputs
- **Tags**: subtitle bug, overflow, mp4, infotainment exploit

## USB Firmware Side-Loading

- **Attack Type**: USB Firmware Attack
- **Target**: Infotainment System
- **Vulnerability**: Insecure firmware validation or absence of cryptographic signing
- **MITRE**: T1542.001
- **Impact**: Persistent compromise of infotainment
- **Tools**: Binwalk, USBRubberDucky, USBImager
- **Scenario**: Malicious firmware update file is dropped into a USB which the user unknowingly uses for infotainment system upgrade.
- **Attack Steps**: 1. Extract a valid infotainment firmware image and reverse it using Binwalk. 2. Modify the firmware with a backdoor or harmful code. 3. Repackage and sign it (or leave unsigned if verification is weak). 4. Place on USB with matching update filename. 5. Plug USB into vehicle and follow standard update process. 6. Monitor system for unexpected network traffic or behavior.
- **Detection**: Monitor for unsigned firmware installs
- **Solution**: Enforce digital signature checks and secure boot
- **Tags**: firmware, usb attack, backdoor

## Android Auto Debug Interface Abuse

- **Attack Type**: App Exploitation
- **Target**: Infotainment Interface (Android-based)
- **Vulnerability**: Exposed debug interfaces and lack of permission checks
- **MITRE**: T1518.001
- **Impact**: Potential control over infotainment features
- **Tools**: ADB, Frida, Termux
- **Scenario**: Attacker gains access to Android Auto’s debug interface via USB and injects commands.
- **Attack Steps**: 1. Connect Android device to vehicle via USB and enable Developer Mode. 2. Use adb shell to enumerate running processes in the Android Auto sandbox. 3. Deploy Frida or custom scripts to hook into infotainment-related functions. 4. Attempt to bypass security checks or gain unauthorized access to vehicle functions exposed via the app. 5. Log results and identify any exploitable surface.
- **Detection**: USB debugging alerts, process monitoring
- **Solution**: Restrict debug access, app hardening
- **Tags**: androidauto, usb debug, frida, infotainment hack

## CarPlay URL Handler Exploit

- **Attack Type**: App Exploitation
- **Target**: CarPlay Interface
- **Vulnerability**: Unvalidated input in CarPlay’s custom URL handler
- **MITRE**: T1071.001
- **Impact**: Execution of unintended functions or abuse of trusted interface
- **Tools**: Burp Suite, Custom iOS App, CarPlay Test Mode
- **Scenario**: A vulnerability in CarPlay’s custom URL handler is used to invoke unauthorized actions when a specially crafted link is opened via SMS or app.
- **Attack Steps**: 1. Develop or use a test iOS app that generates deep links compatible with CarPlay. 2. Embed parameters that call unintended behavior (e.g., opening navigation, injecting system commands). 3. Deliver the link via messaging app or QR code. 4. When opened in CarPlay-enabled mode, observe misbehavior or command execution.
- **Detection**: Monitor CarPlay logs, input logs
- **Solution**: Implement strict input sanitization for URL handlers
- **Tags**: ios exploit, carplay, deeplink

## JPEG-Based Exploit on Car Display

- **Attack Type**: Media File Exploit
- **Target**: Infotainment System
- **Vulnerability**: Image Parsing Bug
- **MITRE**: T1203
- **Impact**: Remote code execution or crash
- **Tools**: Hex Editor, AFL++, IDA Pro
- **Scenario**: Maliciously crafted JPEG triggers a vulnerability in the infotainment’s image decoder when viewed.
- **Attack Steps**: 1. Research image decoding libraries used in the infotainment system.2. Identify known bugs or fuzz with AFL++ for new ones.3. Craft malformed JPEG files with corrupted headers or segments.4. Load the file onto USB or Bluetooth transfer.5. Display image as wallpaper or album art.6. Infotainment crashes or executes arbitrary code.7. Monitor logs or debugger outputs for confirmation.
- **Detection**: Crash logs, USB activity logs
- **Solution**: Patch libraries, enforce input validation
- **Tags**: jpeg exploit, image fuzzing, infotainment

## MP4 Payload via Video Playback

- **Attack Type**: Media File Exploit
- **Target**: Infotainment Media Player
- **Vulnerability**: Video Decoding Vulnerability
- **MITRE**: T1203
- **Impact**: Remote code execution or denial of service
- **Tools**: FFmpeg Exploit Pack, Payload Builder
- **Scenario**: Crafted MP4 file exploits vulnerabilities in the video playback module causing remote code execution.
- **Attack Steps**: 1. Analyze infotainment media player and decoding stack.2. Create malicious MP4 with buffer overflow payloads.3. Transfer file via USB or network.4. Play video; trigger buffer overflow.5. Gain unauthorized access or crash service.6. Extract logs to confirm exploitation.7. Persist or clean traces depending on attack goals.
- **Detection**: Playback logs, crash dumps
- **Solution**: Update firmware, disable autoplay
- **Tags**: mp4 exploit, media player hack

## Malicious Firmware via USB

- **Attack Type**: USB Firmware Attack
- **Target**: Infotainment Firmware System
- **Vulnerability**: Firmware Validation Bypass
- **MITRE**: T1203.001
- **Impact**: Persistent system compromise
- **Tools**: Binwalk, USB Rubber Ducky, Firmware Mod Kit
- **Scenario**: Fake infotainment firmware update applied via USB injects malicious code into system.
- **Attack Steps**: 1. Extract legitimate firmware with Binwalk.2. Insert backdoor or malicious payload.3. Repack firmware, bypass signature if possible.4. Place firmware on USB drive named “Update”.5. User applies update unknowingly.6. Malicious code runs persistently.7. Monitor network or system behavior for malicious activity.
- **Detection**: USB insertion logs, firmware integrity checks
- **Solution**: Enforce cryptographic signing
- **Tags**: usb attack, fake update, firmware hack

## Wi-Fi APK Delivery for Android Auto

- **Attack Type**: App Exploitation
- **Target**: Connected Smartphone
- **Vulnerability**: App Integrity Bypass
- **MITRE**: T1476
- **Impact**: Data leak or control over infotainment
- **Tools**: Bettercap, Rogue AP, Custom APK
- **Scenario**: Rogue APK delivered via Wi-Fi hotspot to Android Auto app on tethered device.
- **Attack Steps**: 1. Set up rogue Wi-Fi AP imitating known hotspot.2. Intercept app update requests.3. Serve malicious APK disguised as update.4. Victim installs APK on phone.5. Malicious app communicates with infotainment.6. Exfiltrate data or manipulate functions.7. Cover tracks by uninstall or obfuscation.
- **Detection**: App install logs, network analysis
- **Solution**: Google Play enforcement, SEPolicy
- **Tags**: wifi attack, apk delivery

## Bluetooth Audio Stream Overflow

- **Attack Type**: Media File Exploit
- **Target**: Audio Decoder
- **Vulnerability**: Codec Parsing Bug
- **MITRE**: T1499
- **Impact**: DoS or remote code execution
- **Tools**: Bluetooth Sniffer, SoX, MP3 Exploit Tools
- **Scenario**: Malformed audio streamed over Bluetooth triggers buffer overflow in infotainment codec.
- **Attack Steps**: 1. Create malformed MP3 targeting vulnerable codec.2. Stream audio over Bluetooth from attacker device.3. Audio parser crashes or executes payload.4. Gain code execution or DoS.5. Analyze Bluetooth logs for anomalies.6. Patch codec or sandbox audio process.7. Prevent via updated Bluetooth stack.
- **Detection**: Bluetooth stack logs, crash reports
- **Solution**: Firmware updates, sandboxing
- **Tags**: bluetooth exploit, audio overflow

## Drive-By Exploit via Radio Broadcast

- **Attack Type**: Media File Exploit
- **Target**: Radio Subsystem
- **Vulnerability**: Metadata Parsing Bug
- **MITRE**: T1203.003
- **Impact**: Temporary or persistent control
- **Tools**: HackRF, Raspberry Pi TX, SDR Tools
- **Scenario**: Rogue FM station sends crafted metadata that exploits infotainment parser bugs.
- **Attack Steps**: 1. Set up rogue FM broadcast transmitting malicious RDS data.2. Target vehicle tuned to that frequency.3. Infotainment parses crafted metadata.4. Trigger overflow or memory corruption.5. Cause crash or gain control.6. Detect via tuner logs.7. Filter metadata or block rogue stations.
- **Detection**: Radio logs, system crash dumps
- **Solution**: Metadata sanitization
- **Tags**: rds exploit, fm broadcast hack

## Firmware Dump via Debug Port

- **Attack Type**: USB Firmware Attack
- **Target**: Infotainment Board
- **Vulnerability**: Unprotected Debug Interfaces
- **MITRE**: T1601
- **Impact**: Persistent backdoor access
- **Tools**: UART-USB Adapter, Ghidra, Logic Analyzer
- **Scenario**: Attacker accesses debug port to dump and modify firmware.
- **Attack Steps**: 1. Locate and connect to debug UART port.2. Dump firmware using serial tools.3. Analyze and patch firmware with Ghidra.4. Reflash modified firmware via update.5. Execute payloads for backdoor or data theft.6. Hide traces by clearing logs.7. Disable debug port to mitigate.
- **Detection**: Physical port monitoring, firmware verification
- **Solution**: Secure boot, debug port disablement
- **Tags**: uart attack, firmware modding

## Jailbroken CarPlay App Abuse

- **Attack Type**: App Exploitation
- **Target**: CarPlay Interface
- **Vulnerability**: Sandbox Escape
- **MITRE**: T1647
- **Impact**: Privacy breach, unauthorized control
- **Tools**: Jailbroken iPhone, Frida, Xcode
- **Scenario**: Jailbroken iOS app abuses CarPlay interface to inject commands.
- **Attack Steps**: 1. Jailbreak device and sideload app.2. Hook CarPlay APIs via Frida.3. Spoof commands to control media/navigation.4. Access private data.5. Evade detection via obfuscation.6. Monitor CarPlay logs.7. Enforce whitelist of apps to prevent.
- **Detection**: App behavior monitoring
- **Solution**: Whitelist enforcement, jailbreak detection
- **Tags**: carplay hack, ios exploit

## OTA Exploit via Manufacturer API

- **Attack Type**: Firmware Exploit
- **Target**: OTA Update System
- **Vulnerability**: Weak API Authentication
- **MITRE**: T1190
- **Impact**: Remote compromise without access
- **Tools**: Postman, Burp Suite, Reverse Engineering
- **Scenario**: Poorly secured OTA API abused to push malicious firmware remotely.
- **Attack Steps**: 1. Reverse engineer mobile app APIs.2. Find unprotected firmware upload endpoint.3. Upload malicious firmware.4. Vehicle applies update unknowingly.5. Attacker gains remote code execution.6. Detect via API logs.7. Secure API with auth and signing.
- **Detection**: API monitoring, firmware validation
- **Solution**: Multi-factor auth, code signing
- **Tags**: ota exploit, api abuse

## Voice Assistant Command Injection

- **Attack Type**: Audio-Based Exploit
- **Target**: Voice Assistant Module
- **Vulnerability**: Microphone Input Injection
- **MITRE**: T1566.002
- **Impact**: Unauthorized command execution
- **Tools**: Ultrasonic Generator, Text-to-Speech Tools
- **Scenario**: Ultrasonic signals inject commands into infotainment voice assistant.
- **Attack Steps**: 1. Create ultrasonic audio with embedded voice commands.2. Emit near parked or running car.3. Infotainment processes commands silently.4. Trigger actions like calling or navigation.5. Difficult for users to detect.6. Analyze microphone inputs for anomalies.7. Implement voice authentication.
- **Detection**: Audio logs, anomaly detection
- **Solution**: Voice biometrics, frequency filtering
- **Tags**: ultrasonic attack, voice injection

## Malicious MP3 Metadata Attack

- **Attack Type**: Media File Exploit
- **Target**: Infotainment Media Engine
- **Vulnerability**: Tag Parsing Vulnerability
- **MITRE**: T1203.003
- **Impact**: Crash or code execution
- **Tools**: MP3Tag, Python Scripts, EyeD3
- **Scenario**: Malicious code hidden in MP3 ID3 tags triggers crash or exploit in infotainment.
- **Attack Steps**: 1. Edit ID3 tags with overly long or malformed data.2. Transfer MP3 to vehicle via USB or Bluetooth.3. Infotainment parses tags unsafely.4. Crash or remote code execution occurs.5. Monitor logs and playback failures.6. Patch tag parsers.7. Limit metadata lengths.
- **Detection**: Log monitoring, playback errors
- **Solution**: Metadata sanitization
- **Tags**: mp3 exploit, id3 tags

## Captive Portal Redirect to Malicious App

- **Attack Type**: App Exploitation
- **Target**: Infotainment Browser & Apps
- **Vulnerability**: Captive Portal Abuse
- **MITRE**: T1557
- **Impact**: Unauthorized app installation
- **Tools**: WiFi Pineapple, MITM Proxy
- **Scenario**: Rogue captive portal redirects infotainment browser to attacker-controlled app download page.
- **Attack Steps**: 1. Create fake Wi-Fi hotspot with captive portal.2. Redirect infotainment browser to malicious app.3. User installs or launches app.4. App gains bridge access to infotainment.5. Exfiltrates data or controls device.6. Detect unusual Wi-Fi connections.7. Disable captive portals or restrict app installs.
- **Detection**: Network monitoring, app logs
- **Solution**: Disable captive portal support
- **Tags**: captive portal, rogue wifi

## Subtitle Parsing Buffer Overflow

- **Attack Type**: Media File Exploit
- **Target**: Infotainment Media Player
- **Vulnerability**: Subtitle Parsing Bug
- **MITRE**: T1499
- **Impact**: DoS or RCE
- **Tools**: Subtitle Edit, VLC, Exploit Generators
- **Scenario**: Malformed subtitle files cause buffer overflow in media player.
- **Attack Steps**: 1. Craft malicious .srt file with malformed entries.2. Pair with video file on USB.3. Play video on infotainment.4. Buffer overflow triggers crash or code execution.5. Confirm via crash dumps.6. Patch subtitle parser.7. Disable subtitle support if unused.
- **Detection**: Crash logs, playback failure
- **Solution**: Patch or disable subtitle parsing
- **Tags**: subtitle exploit, buffer overflow

## DNS Rebinding Attack on Mobile Bridge

- **Attack Type**: App Exploitation
- **Target**: Infotainment + Mobile Bridge
- **Vulnerability**: Origin Check Weakness
- **MITRE**: T1185
- **Impact**: App spoofing, unauthorized access
- **Tools**: Burp Suite, DNS Rebind Toolkit
- **Scenario**: Use DNS rebinding via tethered device to access local infotainment services.
- **Attack Steps**: 1. Connect mobile device to malicious DNS server.2. Rebind trusted domains to attacker IP.3. Access local admin APIs on infotainment.4. Extract info or send commands.5. Detect DNS anomalies.6. Implement host checking and DNS pinning.7. Harden network stack.
- **Detection**: DNS logs, network anomaly detection
- **Solution**: Host validation, DNS pinning
- **Tags**: dns rebinding, mobile bridge

## APK Side-Load via QR Scanner

- **Attack Type**: App Exploitation
- **Target**: Infotainment Android App
- **Vulnerability**: Source Validation Lacking
- **MITRE**: T1553.002
- **Impact**: Backdoor installation on device
- **Tools**: QR Code Generator, APK Builder
- **Scenario**: Malicious APK linked via QR code scanned by infotainment app leads to compromise.
- **Attack Steps**: 1. Build malicious APK with backdoor.2. Host APK on attacker server.3. Generate QR code linking to APK.4. Place QR where user scans with infotainment.5. User installs APK unknowingly.6. APK compromises phone and infotainment link.7. Monitor QR scan logs.
- **Detection**: QR scan monitoring, URL filtering
- **Solution**: Whitelist QR domains, block APK installs
- **Tags**: qr attack, apk side-load

## Extracting Firmware from ECU via JTAG

- **Attack Type**: Firmware Dump & Analysis
- **Target**: ECU
- **Vulnerability**: Exposed debug interface (JTAG/SWD)
- **MITRE**: T1609 – Firmware Extraction
- **Impact**: Enables deep understanding of firmware logic and weaknesses
- **Tools**: OpenOCD, Bus Pirate, JTAGulator
- **Scenario**: Using physical access to read ECU firmware via JTAG interface
- **Attack Steps**: 1. Remove the ECU from the vehicle and identify test points using a multimeter or datasheets. 2. Connect JTAGulator to the ECU to identify active JTAG pins. 3. Use OpenOCD to initiate communication and dump the memory of the ECU. 4. Save the dumped firmware to a local machine for analysis. 5. Open the binary in tools like Ghidra or IDA Pro for static reverse engineering.
- **Detection**: Monitor ECU port access, detect unauthorized debugging hardware
- **Solution**: Disable unused debug interfaces in production firmware
- **Tags**: firmware-reverse, JTAG, OpenOCD, Ghidra

## Analyzing ECU Firmware with Ghidra

- **Attack Type**: Static Code Analysis
- **Target**: ECU
- **Vulnerability**: Lack of firmware obfuscation
- **MITRE**: T1609 – Firmware Extraction
- **Impact**: May expose undocumented diagnostic commands
- **Tools**: Ghidra, Binwalk, Hex-Rays
- **Scenario**: Perform static reverse engineering of extracted ECU firmware
- **Attack Steps**: 1. Load dumped firmware into Binwalk to identify partitions and code sections. 2. Extract relevant binary blobs (e.g., ARM ELF files). 3. Load them into Ghidra to reconstruct function trees and strings. 4. Explore functions related to diagnostic commands or memory protection. 5. Document suspicious routines or insecure memory operations.
- **Detection**: Static binary diffing, look for known opcode patterns
- **Solution**: Use binary obfuscation or encrypt firmware sections
- **Tags**: Ghidra, static-analysis, firmware-exploit

## UDS 0x27 Access Attempt

- **Attack Type**: Protocol Abuse
- **Target**: ECU
- **Vulnerability**: Weak challenge-response implementation
- **MITRE**: T1622 – Component Identification
- **Impact**: Unlocks protected ECU features, allows firmware writing
- **Tools**: UDSExplorer, CANalyze, SavvyCAN
- **Scenario**: Try accessing secure ECU functions using UDS SecurityAccess (0x27)
- **Attack Steps**: 1. Connect to vehicle via OBD-II using a CAN interface. 2. Send UDS 0x27 "SecurityAccess Request Seed" to the target ECU. 3. Capture the returned seed. 4. Attempt to calculate or brute-force the key. 5. Send the calculated key in a 0x27 response. 6. If successful, ECU enters unlocked mode, allowing advanced diagnostics.
- **Detection**: Log and monitor 0x27 request rates from non-authorized sources
- **Solution**: Implement rate limiting and proper cryptographic challenge
- **Tags**: UDS, diagnostic-access, ECU, brute-force

## Brute Forcing ECU Security Key

- **Attack Type**: PIN Guessing / Key Guessing
- **Target**: ECU
- **Vulnerability**: Predictable key algorithms
- **MITRE**: T1055 – Process Injection
- **Impact**: Could allow firmware tampering or critical parameter changes
- **Tools**: UDS Security Tool, Python script
- **Scenario**: Attempting to guess ECU access key used in diagnostic protocols
- **Attack Steps**: 1. Send repeated 0x27 seed requests to obtain seeds. 2. Create a custom brute-forcer to iterate possible key values using known seed/key algorithms. 3. After each guess, send response to ECU and observe acceptance or rejection. 4. Log successful key if found. 5. Gain elevated ECU access.
- **Detection**: ECU logs repeated failures, trigger alerts on failed auth
- **Solution**: Use non-deterministic seed/key generation, lockout mechanism
- **Tags**: PIN-bypass, brute-force, diagnostic-unlock

## Spoofing 0x10 Diagnostic Session

- **Attack Type**: Diagnostic Abuse
- **Target**: ECU
- **Vulnerability**: Lack of session authentication
- **MITRE**: T1609 – Firmware Extraction
- **Impact**: Enables preparation for flashing or unauthorized functions
- **Tools**: CANtact, ICSim
- **Scenario**: Send 0x10 to switch ECU into a diagnostic session allowing further actions
- **Attack Steps**: 1. Connect to vehicle CAN bus using a USB-to-CAN interface. 2. Identify the target ECU address using CAN scanning. 3. Send UDS service 0x10 (Diagnostic Session Control) request to initiate Extended Diagnostic session. 4. ECU replies confirming mode change. 5. Now the attacker can attempt 0x27, 0x31, or 0x34 for unlocking or reflashing.
- **Detection**: ECU should log session requests; verify source device
- **Solution**: Require pre-authentication for session transitions
- **Tags**: UDS, 0x10, CANbus, session-hijack

## Reverse Engineering Hyundai ECU Firmware

- **Attack Type**: Static Firmware Analysis
- **Target**: Automotive ECU
- **Vulnerability**: Lack of firmware obfuscation
- **MITRE**: T1609 - Container Administration Command
- **Impact**: Enables attacker knowledge of ECU logic
- **Tools**: Binwalk, Ghidra, strings
- **Scenario**: Firmware image of a Hyundai vehicle's ECU is obtained for offline reverse engineering.
- **Attack Steps**: 1. Extract the firmware image from the ECU using SPI or UDS download method.2. Use binwalk to analyze the image and carve out known file systems or compressed binaries.3. Load the main binary into Ghidra and analyze the function structure and strings.4. Identify any debugging strings, unsafe functions (e.g., strcpy), and potential authentication bypass routines.5. Cross-reference against known ECU architecture to understand control flows and patch behavior.
- **Detection**: Unusual firmware reads or flashes
- **Solution**: Implement code obfuscation, encrypt firmware
- **Tags**: ECU, Reverse Engineering, Ghidra, Binwalk

## Brute Force ECU Security Access Mode

- **Attack Type**: Brute Force Protocol Abuse
- **Target**: Automotive ECU
- **Vulnerability**: Insecure UDS access authentication
- **MITRE**: T1027 - Obfuscated Files or Info
- **Impact**: Full ECU diagnostic or firmware access
- **Tools**: CANtact, UDSpy, custom script
- **Scenario**: Attacker attempts to gain Security Access via repeated UDS 0x27 requests to unlock ECU functions.
- **Attack Steps**: 1. Connect to the vehicle's CAN bus using CANtact.2. Monitor diagnostic messages and identify UDS responses from the ECU.3. Send repeated 0x27 requests with incremented keys or known weak default seeds.4. If ECU accepts a key, gain access to advanced diagnostic or flash modes.5. Log the successful seed-key pair for reuse across models.6. Optionally patch the ECU firmware once access is granted.
- **Detection**: Monitor excessive 0x27 UDS traffic on CAN
- **Solution**: Rate-limit UDS requests, require secure key derivation
- **Tags**: ECU, Brute Force, Diagnostic, UDS, Access

## UDS Routine Control Abuse

- **Attack Type**: Protocol Exploitation
- **Target**: Automotive ECU
- **Vulnerability**: Lack of access control on routines
- **MITRE**: T1490 - Inhibit System Recovery
- **Impact**: May bypass safety checks or protections
- **Tools**: CANalyzer, python-can, ICSim
- **Scenario**: Use of UDS 0x31 routineControl to enable hidden debugging or calibration routines in ECU.
- **Attack Steps**: 1. Interface with the CAN bus using tools like python-can or ICSim.2. Identify ECUs that respond to UDS 0x22 (read data) and 0x10 (diagnostic session control).3. Transition ECU into ExtendedDiagnosticSession with 0x10 0x03.4. Send crafted 0x31 messages with known routine IDs to activate hidden modes (e.g., bypass immobilizer, disable safety checks).5. Analyze ECU behavior and log the effect of each routine.6. Use firmware knowledge to infer what each routine ID does.
- **Detection**: Log UDS routineControl messages
- **Solution**: Authenticate routine use, validate session level
- **Tags**: ECU, UDS, 0x31, RoutineControl, CAN

## Exploiting ECU Buffer Overflow via UDS Write

- **Attack Type**: Memory Corruption
- **Target**: Automotive ECU
- **Vulnerability**: Lack of bounds checking in UDS handler
- **MITRE**: T1203 - Exploitation for Client Exec
- **Impact**: ECU crash or arbitrary code execution possible
- **Tools**: CANoe, custom CAN scripts
- **Scenario**: Buffer overflow is triggered via oversized UDS 0x2E WriteDataByIdentifier payload.
- **Attack Steps**: 1. Analyze the firmware to identify how the ECU handles WriteDataByIdentifier (0x2E).2. Identify a vulnerable DID that lacks proper bounds checking.3. Craft a UDS message with an oversized payload for that DID.4. Send the message and monitor ECU for crash or altered behavior.5. Attempt to redirect execution if successful (e.g., jump to shellcode or overwrite return address).6. Repeat with slight variations to stabilize the exploit.
- **Detection**: Monitor unexpected resets or memory faults
- **Solution**: Patch firmware, validate payload lengths
- **Tags**: ECU, Exploit, Overflow, WriteDataByIdentifier

## Patch Analysis to Identify Hardcoded Secrets

- **Attack Type**: Firmware Secret Extraction
- **Target**: Automotive ECU
- **Vulnerability**: Hardcoded credentials in firmware
- **MITRE**: T1552.001 - Credentials in Files
- **Impact**: Compromises ECU access control
- **Tools**: Ghidra, Hex-Rays, strings
- **Scenario**: Analyze ECU firmware image to find embedded hardcoded PINs or keys.
- **Attack Steps**: 1. Load the ECU binary into Ghidra and search for known memory regions like .rodata.2. Extract all ASCII strings, look for sequences resembling keys, tokens, or PINs.3. Use XREF feature to identify where those values are used in code.4. If values are passed to crypto or validation functions, they are likely security credentials.5. Note down and test the secrets using diagnostic tools or scripts.6. Use recovered secrets to bypass security mechanisms (e.g., seed-key access).
- **Detection**: Scan firmware images for secrets
- **Solution**: Use dynamic key generation, avoid hardcoded secrets
- **Tags**: ECU, Secrets, Firmware, Reverse, Ghidra

## Reverse Engineering Throttle Control Firmware

- **Attack Type**: Safety-Critical Analysis
- **Target**: Automotive ECU
- **Vulnerability**: Logic flaws in actuator response
- **MITRE**: T1565.001 - Data Manipulation
- **Impact**: May allow remote acceleration control
- **Tools**: Ghidra, CANape, IDA Pro
- **Scenario**: Analyze firmware section responsible for throttle actuator behavior.
- **Attack Steps**: 1. Identify which ECU handles throttle control via documentation or CAN traffic.2. Dump the firmware from that ECU.3. Use Ghidra or IDA Pro to analyze interrupt vectors and main function flow.4. Look for throttle-related terms and feedback loops (e.g., PID control).5. Simulate logic and assess what happens if sensor values are spoofed.6. Create PoC inputs that mimic unsafe conditions (e.g., forced throttle open).
- **Detection**: Detect unusual CAN values vs sensor data
- **Solution**: Validate all sensor input logic in firmware
- **Tags**: ECU, Safety, Throttle, Analysis, Firmware

## Custom Diagnostic Session Creation

- **Attack Type**: Protocol Abuse
- **Target**: Automotive ECU
- **Vulnerability**: Poor validation of session values
- **MITRE**: T1071.001 - Application Layer Protocol
- **Impact**: Unlocks hidden ECU functions
- **Tools**: CANtact, UDSpy, custom tool
- **Scenario**: Create undocumented diagnostic session types to access restricted ECU functionality.
- **Attack Steps**: 1. Scan existing ECU responses to known session control messages (0x10).2. Try undocumented session values like 0x04, 0x06, 0x85 and monitor responses.3. If ECU accepts one, attempt to issue higher-privileged commands like 0x2F (InputOutputControl).4. Log access to features not available in standard sessions.5. Reverse engineer firmware logic around session control.6. Document the undocumented session behavior for re-use across same vendor ECUs.
- **Detection**: Monitor for non-standard session requests
- **Solution**: Whitelist allowed session types
- **Tags**: ECU, UDS, Diagnostic Sessions, Reverse

## Analyzing OTA Update Binary

- **Attack Type**: OTA Firmware Inspection
- **Target**: Automotive ECU
- **Vulnerability**: Weak signature validation
- **MITRE**: T1601 - Modify System Image
- **Impact**: Allows loading of rogue firmware
- **Tools**: Binwalk, Ghidra, xxd
- **Scenario**: Examine an Over-the-Air ECU update binary to find tampering or exploitable entry points.
- **Attack Steps**: 1. Obtain the OTA binary file from update package or internet leaks.2. Use binwalk to dissect it and locate the actual firmware blobs.3. Look for embedded metadata or validation routines.4. Load main executable into Ghidra and check how digital signatures or versions are verified.5. Identify bypasses or incomplete checks that allow modified firmware to be flashed.6. Test in simulation before attempting live flash.
- **Detection**: Monitor OTA update logs and signatures
- **Solution**: Enforce signed updates, verify firmware hashes
- **Tags**: ECU, OTA, Update, Reverse, Tampering

## Replay Factory Diagnostic Unlock

- **Attack Type**: Replay Attack
- **Target**: Automotive ECU
- **Vulnerability**: Replayable diagnostic authentication
- **MITRE**: T1078.003 - Valid Accounts
- **Impact**: Grants unauthorized access to vehicle systems
- **Tools**: CANSniffer, CANplayer
- **Scenario**: Reuse of legitimate diagnostic unlock messages captured during servicing.
- **Attack Steps**: 1. During a legitimate service session, capture UDS messages on CAN using CANSniffer.2. Look for 0x27 challenge-response sequences that lead to access.3. Save the successful message stream and timing.4. Replay the same sequence to the ECU using CANplayer.5. If ECU lacks proper nonce-based challenge, it will grant access.6. Use access to modify configuration or firmware.
- **Detection**: Compare session nonce and response behavior
- **Solution**: Use dynamic nonces, session invalidation
- **Tags**: ECU, Replay, Diagnostic, Servicing

## Reverse Engineering Gearbox ECU

- **Attack Type**: Safety Control Analysis
- **Target**: Automotive ECU
- **Vulnerability**: Insufficient validation in shift logic
- **MITRE**: T1491 - Resource Hijacking
- **Impact**: Unsafe gear transitions or damage
- **Tools**: Ghidra, Hex Editor, Trace32
- **Scenario**: Disassemble transmission ECU firmware to locate gear shift control logic.
- **Attack Steps**: 1. Identify and dump firmware from the Transmission Control Module (TCM).2. Use Ghidra to locate control functions responsible for shift timing and actuator logic.3. Trace inputs from speed and torque sensors.4. Modify shift logic in emulated environment to test shift-at-redline or in-reverse cases.5. Validate how the ECU handles illegal transitions.6. Analyze potential abuse scenarios where manipulated inputs could cause mechanical damage.
- **Detection**: Monitor gear logic via live sensor replay
- **Solution**: Add sanity checks for shift logic
- **Tags**: ECU, Transmission, Gearbox, Reverse

## UDS Routine Control to Force ECU Mode Switch

- **Attack Type**: Protocol Misuse
- **Target**: ECU
- **Vulnerability**: Unauthenticated UDS Routine Control
- **MITRE**: T0886 (Exploitation for Privilege Escalation)
- **Impact**: Enables reprogramming or deactivation of ECU logic
- **Tools**: UDS Sender, CANtact, Scapy, custom Python script
- **Scenario**: Adversary sends crafted UDS messages (e.g., 0x31) to start/stop certain routines on the ECU to force it into special modes
- **Attack Steps**: 1. Connect to the CAN bus using a tool like CANtact. 2. Identify the ECU's address via active scanning. 3. Craft UDS message with service 0x31 (Routine Control). 4. Use routine ID that maps to security-sensitive behavior (e.g., enable programming mode). 5. Send the payload and observe ECU behavior. 6. Analyze response (positive/negative) and attempt replay or chaining with other commands.
- **Detection**: Monitor CAN traffic for abnormal routine control commands
- **Solution**: Implement UDS filtering and restrict unauthorized routine control
- **Tags**: uds, protocol abuse, routinecontrol, automotive, ECU

## Ghidra-Based Analysis of Unprotected Bootloader

- **Attack Type**: Static Firmware Analysis
- **Target**: ECU Firmware
- **Vulnerability**: Insecure Bootloader Signature Checks
- **MITRE**: T1609 (Container Administration Command)
- **Impact**: Allows attacker to flash arbitrary firmware
- **Tools**: Ghidra, Binwalk, CANdump
- **Scenario**: Attacker dumps ECU firmware and analyzes bootloader logic to identify insecure update processes
- **Attack Steps**: 1. Extract ECU firmware using chip-off or via OBD-II if possible. 2. Use Binwalk to unpack the binary and isolate the bootloader section. 3. Load binary into Ghidra, configure processor architecture. 4. Analyze startup code for authentication checks or update logic. 5. Identify routines that validate firmware signatures. 6. Spot areas where checks can be bypassed or always return true. 7. Document findings and attempt reflash with modified firmware.
- **Detection**: Firmware diffing, secure bootloader validation
- **Solution**: Use secure boot & signed firmware validation
- **Tags**: firmware, bootloader, ghidra, reverse engineering

## Diagnostic Session Hijack During Service Mode

- **Attack Type**: Session Manipulation
- **Target**: ECU
- **Vulnerability**: Lack of session integrity & arbitration
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Unauthorized access during maintenance
- **Tools**: UDS Tools, CANalyzer
- **Scenario**: Exploiting ECU behavior during diagnostic service sessions to escalate access or interfere with commands
- **Attack Steps**: 1. Wait until a legitimate service session is initiated (e.g., at a garage). 2. Eavesdrop on diagnostic session traffic. 3. Inject a diagnostic session start (0x10) request mid-session. 4. Attempt to overwrite ongoing commands by racing or injecting UDS messages. 5. Leverage temporary elevated access (e.g., programming session) to issue unauthorized commands.
- **Detection**: Session logging and anomaly detection
- **Solution**: Enforce diagnostic session authentication
- **Tags**: uds, session, mitm, diagnostics, automotive

## Static ECU Firmware Analysis with Ghidra

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Lack of firmware obfuscation
- **MITRE**: T1049 - System Network Connections Discovery
- **Impact**: Find security flaws for ECU control
- **Tools**: Ghidra, Binwalk
- **Scenario**: Reverse engineer raw ECU firmware to locate authentication logic and insecure functions
- **Attack Steps**: 1. Obtain firmware dump from ECU using JTAG or SPI flash extraction.2. Use Binwalk to carve out known formats from the binary.3. Load firmware into Ghidra and analyze function names and cross-references.4. Identify areas like authentication checks, diagnostic functions.5. Annotate and reverse logic to understand where protections can be bypassed or flaws exploited.
- **Detection**: Monitor firmware extraction attempts and USB/JTAG access.
- **Solution**: Enforce firmware encryption and hardware protections.
- **Tags**: ECU, Reverse Engineering, Ghidra, Firmware

## UDS Service 0x27 Exploitation for Unlock

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Weak or predictable access key
- **MITRE**: T1056.001 - Input Capture
- **Impact**: Full ECU access, unsafe config manipulation
- **Tools**: UDS Sniffer, CANalyzer, UDS Bruteforce Tools
- **Scenario**: Abuse the security access control mechanism in UDS protocol to unlock ECUs and gain higher privileges
- **Attack Steps**: 1. Send 0x10 to initiate diagnostic session.2. Send 0x27 to request security access.3. Receive seed from ECU and try to compute or brute-force key.4. Upon successful match, gain access to restricted diagnostic functions like 0x31 (write memory).5. Modify behavior, overwrite config or disable safety features.
- **Detection**: Log UDS request patterns, alert repeated 0x27 attempts.
- **Solution**: Use strong key generation algorithms and rolling seeds.
- **Tags**: UDS, Diagnostic, Access Control, CANbus

## Dumping Flash via JTAG

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Exposed JTAG interface
- **MITRE**: T1600 - Hardware Additions
- **Impact**: Full firmware exposure, offline exploitation
- **Tools**: JTAGulator, OpenOCD, Ghidra
- **Scenario**: Use JTAG to connect to ECU hardware and dump the flash memory for offline analysis
- **Attack Steps**: 1. Identify JTAG pinout on ECU PCB using JTAGulator or datasheets.2. Connect JTAG to debugger like OpenOCD.3. Dump entire firmware memory using JTAG interface.4. Analyze dumped binary using Ghidra or IDA Pro.5. Look for bootloaders, debug strings, or hardcoded credentials that can be misused.
- **Detection**: Monitor unauthorized physical access attempts.
- **Solution**: Physically disable or epoxy over JTAG/debug ports after manufacturing.
- **Tags**: Firmware Dump, Hardware Access, ECU, Reverse

## CAN Injection after ECU Unlock

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Unsecured post-authentication state
- **MITRE**: T1609 - Container Administration Command
- **Impact**: CAN manipulation, safety risk
- **Tools**: CANBus Triple, ICSim
- **Scenario**: Inject arbitrary CAN frames after unlocking the ECU to control vehicle behavior
- **Attack Steps**: 1. Gain access to CAN bus via OBD-II or physical tap.2. Use diagnostic sequence (e.g., UDS 0x27, 0x10) to unlock the ECU.3. Replay or craft CAN messages such as engine RPM or brake control.4. Observe how the vehicle or ICSim responds.5. Iterate message IDs and data payloads to explore undocumented functionality or cause erratic behavior.
- **Detection**: Monitor CAN bus for unexpected message IDs or frequency anomalies.
- **Solution**: Enforce message whitelisting and restrict post-auth write access.
- **Tags**: CAN Injection, ECU Unlock, Diagnostics

## Identifying Debug Strings in ECU Firmware

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Lack of string obfuscation
- **MITRE**: T1083 - File and Directory Discovery
- **Impact**: Faster reverse engineering of firmware
- **Tools**: Ghidra, strings, grep
- **Scenario**: Locate debug strings in firmware to understand code flow or find hints about internal operations
- **Attack Steps**: 1. Dump ECU firmware using JTAG or USB update leak.2. Use strings or Ghidra's string analysis to extract readable ASCII content.3. Search for debug logs, error messages, or function traces.4. Map these strings to code locations in Ghidra.5. Use these markers to reverse logic paths like password checks or hardware initialization.
- **Detection**: Alert if debug strings are present in release builds.
- **Solution**: Strip debug symbols and strings from production firmware.
- **Tags**: Strings, Debug Logs, Firmware Analysis

## Exploiting Memory Write UDS Services

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Insecure write access to memory region
- **MITRE**: T1105 - Ingress Tool Transfer
- **Impact**: Arbitrary ECU code execution
- **Tools**: UDS Tools, CANcat, ICSim
- **Scenario**: Use diagnostic service 0x31 (routine control) or 0x34 (memory write) to write arbitrary code to ECU memory
- **Attack Steps**: 1. Authenticate using UDS 0x27 to gain programming access.2. Identify target memory region via 0x23 (read memory by address).3. Use 0x34 to write shellcode or patches.4. Trigger via 0x31 or reboot.5. Achieve arbitrary behavior change such as bypassing speed limits or changing CAN filters.
- **Detection**: Monitor diagnostic message use and sequence.
- **Solution**: Enforce memory protection and block unsafe diagnostic services.
- **Tags**: UDS Write, ECU Flash, Code Injection

## Binary Diffing of ECU Firmware Versions

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Poor version management
- **MITRE**: T1601 - Modify System Image
- **Impact**: Uncover regression bugs or missed patches
- **Tools**: BinDiff, Diaphora, Ghidra
- **Scenario**: Compare multiple versions of ECU firmware to identify security patches or introduced vulnerabilities
- **Attack Steps**: 1. Obtain two different firmware versions (e.g., update vs. factory dump).2. Load both in Ghidra and use Diaphora or BinDiff.3. Identify changed functions, patched vulnerabilities, or added logic.4. Focus on authentication routines, cryptographic sections, or access checks.5. Document differences and look for potential backdoors or mistakes.
- **Detection**: Track firmware hashes and changelogs during updates.
- **Solution**: Maintain secure firmware lifecycle and audit diffs.
- **Tags**: Firmware Diffing, Patch Analysis, Binary Reverse

## Password Brute Force via Diagnostic Protocols

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Weak or guessable password logic
- **MITRE**: T1110 - Brute Force
- **Impact**: Unauthorized privileged access to ECU
- **Tools**: UDS Brute Tool, ICSim
- **Scenario**: Attempt to brute-force password-based diagnostic access using repeated 0x27 requests
- **Attack Steps**: 1. Interact with ECU using UDS service 0x27.2. Automate sending seeds and testing possible keys or passwords.3. Exploit weak protection algorithms or static passwords.4. Gain programming or service-level access.5. Use this access to modify behavior or further reverse firmware.
- **Detection**: Monitor UDS requests, rate limit access attempts.
- **Solution**: Use dynamic, rotating keys and lockout mechanisms.
- **Tags**: ECU Brute Force, Diagnostic Abuse, UDS Protocol

## Analyzing Bootloaders for Insecure Code

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Insecure boot process
- **MITRE**: T1542 - Pre-OS Boot
- **Impact**: Full control during system startup
- **Tools**: Ghidra, Binwalk, strings
- **Scenario**: Reverse engineer ECU bootloader code to find insecure verification or authentication logic
- **Attack Steps**: 1. Extract firmware and isolate bootloader section (e.g., first 0x10000 bytes).2. Analyze using Ghidra for init routines.3. Look for insecure signature checks or always-true conditions.4. Check for UART/serial debug access.5. Document vulnerabilities that could allow unsigned firmware uploads.
- **Detection**: Validate firmware signatures during boot process.
- **Solution**: Implement secure boot and code signing enforcement.
- **Tags**: Bootloader, Secure Boot, ECU Analysis

## Reverse Engineering Infotainment-to-ECU Links

- **Attack Type**: ECU Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Poor segregation between infotainment & ECUs
- **MITRE**: T1008 - Fallback Channels
- **Impact**: Attack ECUs via infotainment interface
- **Tools**: Wireshark, ICSim, CAN tools
- **Scenario**: Analyze how infotainment messages are routed to ECU over CAN or Ethernet, potentially allowing indirect exploitation
- **Attack Steps**: 1. Use packet sniffers (Wireshark or CANalyzer) between infotainment and ECUs.2. Reverse CAN message flow and understand which messages trigger which ECU functions.3. Correlate infotainment functions with changes in ECU behavior.4. Identify possible attack paths like sending a malformed media file that results in a CAN command to an ECU.5. Use this for chaining multi-stage exploits.
- **Detection**: Monitor infotainment CAN/ethernet traffic patterns.
- **Solution**: Segment infotainment and critical ECUs; firewall messages.
- **Tags**: Infotainment, CAN, Message Routing, ECU Mapping

## Extracting Bootloaders from ECU Firmware

- **Attack Type**: ECU Firmware Extraction
- **Target**: Embedded System
- **Vulnerability**: Insecure firmware verification
- **MITRE**: T1552
- **Impact**: May allow unsigned firmware loading
- **Tools**: Ghidra, Binwalk, Hex-Rays
- **Scenario**: Reverse engineer the bootloader code from ECU dumps to understand firmware upgrade paths or protections
- **Attack Steps**: 1. Connect to the ECU and extract firmware using UDS 0x23 (ReadMemoryByAddress) or direct chip access via JTAG/SWD. 2. Use Binwalk to identify sections like bootloader, main code, or data areas. 3. Isolate and extract the bootloader binary. 4. Load into Ghidra and analyze init routines, memory map usage, and upgrade checks. 5. Identify any insecure firmware validation or downgrade possibilities.
- **Detection**: Monitor firmware version changes; hash validation at update time
- **Solution**: Implement cryptographic checks and signed firmware verification
- **Tags**: ECU, Firmware, Reverse Engineering, Bootloader

## Reverse Engineering CAN Message Handlers

- **Attack Type**: Static Binary Analysis
- **Target**: Embedded System
- **Vulnerability**: Insecure CAN parsing logic
- **MITRE**: T1203
- **Impact**: Potential code execution or manipulation
- **Tools**: Ghidra, IDA Pro, Vector CANalyzer
- **Scenario**: Disassemble the firmware to understand how specific CAN messages are processed
- **Attack Steps**: 1. Extract firmware from ECU. 2. Load into Ghidra or IDA Pro and identify functions that handle CAN message parsing. 3. Follow references to CAN receive interrupt or buffer handling code. 4. Trace logic handling standard IDs or functional IDs. 5. Document message parsing patterns and potential for buffer overflows or insecure deserialization. 6. Correlate message patterns with real bus traffic using CANalyzer.
- **Detection**: Analyze ECU behavior with unexpected or malformed messages
- **Solution**: Harden message parsing, bounds checks in firmware
- **Tags**: CAN Bus, Reverse Engineering, Firmware, CAN Protocol

## Detecting Debug Interfaces Left Enabled

- **Attack Type**: Hardware Debug Analysis
- **Target**: Embedded System
- **Vulnerability**: Debug access left open in production
- **MITRE**: T1518.001
- **Impact**: May give raw memory access or firmware dumps
- **Tools**: OpenOCD, JTAGulator, UART tools
- **Scenario**: Identify if production ECUs still have JTAG or UART interfaces active
- **Attack Steps**: 1. Open the ECU casing carefully. 2. Use JTAGulator or a multimeter to map out pins on the board. 3. Try to identify standard JTAG or UART pinouts. 4. Use tools like OpenOCD to connect and check for active debug interfaces. 5. If accessible, dump memory or read registers. 6. Check if debug was left enabled in production models, which could expose sensitive data or root access.
- **Detection**: Detect unexpected debug communications on manufacturing units
- **Solution**: Disable debug interfaces in firmware before final build
- **Tags**: Hardware, ECU, Debugging, Reverse Engineering

## Identifying Hardcoded Backdoor Service Modes

- **Attack Type**: UDS Abuse
- **Target**: Embedded System
- **Vulnerability**: Hidden diagnostic entry points
- **MITRE**: T1211
- **Impact**: Unauthorized control of vehicle components
- **Tools**: Ghidra, Wireshark, CANalyzer
- **Scenario**: Discover undocumented service modes used by manufacturers for development or servicing
- **Attack Steps**: 1. Analyze extracted ECU firmware with Ghidra to locate handlers for UDS Service IDs (e.g., 0x10, 0x27, 0x31). 2. Look for branches or switch-case logic indicating secret service IDs not publicly documented. 3. Compare with UDS standards to find non-standard behavior. 4. Replay those IDs over CAN using CANalyzer or Python scripts. 5. Confirm any secret diagnostic or control modes activated by undocumented IDs.
- **Detection**: Monitor for rare or undocumented UDS service ID usage on bus
- **Solution**: Validate UDS ID access control strictly in ECU firmware
- **Tags**: Diagnostic, UDS, Reverse Engineering, Backdoors

## Firmware Logic Extraction for Authentication Bypass

- **Attack Type**: Reverse Engineering
- **Target**: Embedded System
- **Vulnerability**: Weak or reversible authentication
- **MITRE**: T1140
- **Impact**: Allows bypass of secure ECU services
- **Tools**: Ghidra, Hex-Rays, Binwalk
- **Scenario**: Analyze the authentication routines in ECU firmware to find bypass opportunities
- **Attack Steps**: 1. Dump the firmware image from the ECU using diagnostic tools or flash programmer. 2. Load into Ghidra or Hex-Rays decompiler. 3. Locate the function responsible for handling UDS 0x27 (SecurityAccess). 4. Analyze the seed-key generation logic. 5. Try to reconstruct or reverse the algorithm used to verify the key. 6. If successful, write a script to generate valid keys without brute-force or having OEM seed-key DB.
- **Detection**: Monitor for rapid UDS SecurityAccess requests or seed-key failures
- **Solution**: Use asymmetric cryptography or stronger key algorithms in authentication logic
- **Tags**: ECU, SecurityAccess, Seed-Key, Reverse Engineering

## GPS Spoofing to Mislead Navigation

- **Attack Type**: GPS Signal Injection
- **Target**: Vehicle
- **Vulnerability**: Lack of GNSS signal validation
- **MITRE**: T8030 – GPS Spoofing
- **Impact**: Navigation errors, ADAS manipulation
- **Tools**: SDR (HackRF), GPS-SDR-SIM, GNSS-SDR
- **Scenario**: Attackers spoof GPS signals to trick the vehicle’s navigation into false location tracking.
- **Attack Steps**: 1. Set up a software-defined radio (SDR) like HackRF and install GPS-SDR-SIM. 2. Generate fake GPS coordinates based on your target destination (e.g., make vehicle think it is heading to the airport). 3. Transmit the fake GPS signal using HackRF near the vehicle. 4. Observe the in-vehicle navigation rerouting or ADAS behavior changes. 5. Monitor vehicle’s response (e.g., lane assist, autopilot decisions) for signs of spoofed location reliance.
- **Detection**: Check NMEA checksum mismatches, dual-band GPS comparison
- **Solution**: Use GNSS authentication, integrate inertial navigation fallback
- **Tags**: gps, spoofing, hackrf, automotive, SDR

## GPS Jamming to Disrupt Navigation

- **Attack Type**: RF Jamming
- **Target**: Vehicle
- **Vulnerability**: Absence of jamming detection systems
- **MITRE**: T8031 – GPS Jamming
- **Impact**: Navigation loss, ADAS fallback
- **Tools**: RF Jammer, SDR, Signal Generator
- **Scenario**: Disrupting vehicle GPS modules by transmitting high-powered noise on GNSS frequencies.
- **Attack Steps**: 1. Use a signal generator or GPS jammer to emit noise centered at GPS L1 frequency (1.575 GHz). 2. Power the jammer and ensure proximity to the vehicle (ideally within 5–10 meters). 3. Monitor the navigation system—signal loss or “searching for satellites” should occur. 4. In ADAS-enabled cars, observe autopilot or lane assist fallback due to GPS loss. 5. Note any safety warnings or driver alerts triggered due to GPS absence.
- **Detection**: Monitor signal strength, GNSS health metrics
- **Solution**: Integrate jamming detection, fallback to inertial nav
- **Tags**: gps, jamming, RF, vehicle

## LIDAR Spoofing with False Obstacle

- **Attack Type**: Optical Spoofing
- **Target**: ADAS Sensor
- **Vulnerability**: Lack of return signal validation
- **MITRE**: T8042 – Optical Sensor Spoofing
- **Impact**: False braking, accident risks
- **Tools**: IR Laser Diodes, LIDAR testing kit, Oscilloscope
- **Scenario**: Projecting fake returns into LIDAR to trick vehicle into detecting ghost obstacles.
- **Attack Steps**: 1. Identify the target vehicle's LIDAR model (e.g., Velodyne). 2. Use an IR laser modulated to match LIDAR return pulse signature. 3. Aim the laser in sync with the LIDAR scanning pattern. 4. Emit pulses at a distance corresponding to fake obstacle (e.g., 3m in front). 5. Observe vehicle braking or obstacle alerts due to spoofed LIDAR data.
- **Detection**: Analyze LIDAR frame inconsistencies
- **Solution**: Multi-sensor fusion (camera + LIDAR)
- **Tags**: lidar, spoofing, sensor-attack

## Radar Ghost Vehicle Creation

- **Attack Type**: RF Reflection Spoofing
- **Target**: Radar-based Vehicle System
- **Vulnerability**: Poor radar object verification
- **MITRE**: T8040 – Radar Spoofing
- **Impact**: False detection, sudden braking
- **Tools**: Corner Reflectors, Radar Simulators
- **Scenario**: Use corner reflectors or active radar emitters to simulate phantom vehicles.
- **Attack Steps**: 1. Set up a corner reflector or a programmable radar simulator device. 2. Position the spoofing tool near the roadway ahead of the vehicle. 3. Adjust the range and speed values in the simulator to mimic a moving object. 4. Observe whether the radar-based ACC or AEB system reacts (e.g., slows down or brakes). 5. Record the vehicle’s behavior to assess safety implications.
- **Detection**: Use Doppler pattern analysis
- **Solution**: Sensor fusion, radar-CV cross-check
- **Tags**: radar, spoofing, automotive

## Ultrasonic Sensor Spoofing

- **Attack Type**: Echo Injection
- **Target**: Ultrasonic Sensor
- **Vulnerability**: Echo-based validation missing
- **MITRE**: T8043 – Ultrasonic Sensor Interference
- **Impact**: False obstacle warnings
- **Tools**: Ultrasonic Transmitter, Signal Generator
- **Scenario**: Mimic parking or blind-spot sensor returns to cause false proximity alerts.
- **Attack Steps**: 1. Identify frequency range of vehicle’s ultrasonic sensors (typically 40 kHz). 2. Use a signal generator and speaker to emit brief ultrasonic bursts at matching frequencies. 3. Time the emissions to simulate echo returns from nonexistent obstacles. 4. Observe driver assist systems triggering parking or collision warnings. 5. Optionally, target blind spot monitors for highway driving confusion.
- **Detection**: Audio signal fingerprinting
- **Solution**: Improved echo matching, sensor fusion
- **Tags**: ultrasonic, spoofing, sensor-hack

## TPMS Spoofing to Cause Driver Distraction

- **Attack Type**: RF Injection
- **Target**: Tire Pressure Sensor
- **Vulnerability**: Lack of authentication in TPMS
- **MITRE**: T8050 – RF Injection
- **Impact**: Driver distraction, false maintenance
- **Tools**: Universal TPMS Transmitter, SDR (YardStick One)
- **Scenario**: Inject false low-pressure alerts via cloned TPMS sensor IDs.
- **Attack Steps**: 1. Capture TPMS packets using an SDR and identify the sensor IDs. 2. Recreate valid packets using a universal TPMS transmitter. 3. Modify the pressure value to a dangerously low value (e.g., 18 PSI). 4. Broadcast the spoofed packet near the vehicle while it's idle or moving. 5. Observe dashboard warnings and potential driver reactions.
- **Detection**: Monitor for inconsistent tire pressure sensors
- **Solution**: Secure TPMS with cryptographic auth
- **Tags**: tpms, rf-injection, automotive

## GPS Time Drift Spoofing

- **Attack Type**: Time Signal Manipulation
- **Target**: Vehicle Logging System
- **Vulnerability**: Reliance on unauthenticated time
- **MITRE**: T8032 – Time Spoofing
- **Impact**: Log desync, task malfunction
- **Tools**: GPS Simulator, HackRF
- **Scenario**: Skew GPS time signals to confuse system logs or time-based actions.
- **Attack Steps**: 1. Use GPS-SDR-SIM to generate spoofed GPS signals with altered time parameters. 2. Set system time offset to a few minutes or hours. 3. Transmit spoofed signal near vehicle to cause GPS module to update system clock. 4. Evaluate system logging (e.g., dashcam timestamps, trip log errors). 5. Observe any scheduled task misbehavior due to time inconsistency.
- **Detection**: Time delta monitoring
- **Solution**: Trusted NTP fallback
- **Tags**: gps, time spoofing, timestamp

## Directional GPS Spoofing with Beam Antenna

- **Attack Type**: RF Directional Injection
- **Target**: Single Vehicle in Fleet
- **Vulnerability**: Directional RF targeting vulnerability
- **MITRE**: T8030
- **Impact**: Isolated misrouting
- **Tools**: Yagi Antenna, GPS SDR Kit
- **Scenario**: Spoof only one vehicle in a fleet by using narrow beam GPS injection.
- **Attack Steps**: 1. Attach Yagi antenna to SDR transmitting GPS spoof signals. 2. Align beam to focus energy toward specific vehicle’s GPS receiver. 3. Transmit fake position, limiting impact to only that vehicle. 4. Monitor target’s movement, ensuring no impact on nearby GPS users. 5. Confirm attacker can manipulate position-based decisions without triggering fleet-wide alerts.
- **Detection**: Signal triangulation, audit GPS logs
- **Solution**: Directional jamming detection
- **Tags**: gps, narrow-beam, spoofing

## TPMS Denial-of-Service via Flooding

- **Attack Type**: RF DoS
- **Target**: TPMS ECU
- **Vulnerability**: No packet rate limiting
- **MITRE**: T8051 – RF DoS
- **Impact**: System failure, confusion
- **Tools**: YardStick One, RF Flooding Script
- **Scenario**: Overload TPMS receiver by transmitting continuous malformed packets.
- **Attack Steps**: 1. Program SDR to broadcast fake TPMS packets in rapid succession. 2. Target all four TPMS sensor ID ranges. 3. Monitor vehicle dashboard for sensor errors, unresponsive TPMS system. 4. Optionally target TPMS ECU reboot logic if observed in firmware. 5. Document system’s fault tolerance and driver-facing errors.
- **Detection**: Log packet spikes
- **Solution**: Add rate control, anomaly filtering
- **Tags**: rf, tpms, dos

## Reflective Radar Spoofing with Aluminum Panels

- **Attack Type**: Passive Radar Trick
- **Target**: Vehicle Radar System
- **Vulnerability**: Poor angular filtering
- **MITRE**: T8041 – Passive Radar Spoofing
- **Impact**: False braking, traffic slowdowns
- **Tools**: Aluminum Sheets, Reflector Frame
- **Scenario**: Use aluminum panels to reflect vehicle’s radar back at specific angles.
- **Attack Steps**: 1. Position aluminum reflector to bounce radar pulses toward vehicle. 2. Angle it to create false reading at a chosen distance (e.g., 20m ahead). 3. Observe vehicle’s adaptive cruise control slowing down for phantom object. 4. Adjust angle and distance to create dynamic spoofing profiles. 5. Record radar logs if accessible for evidence of spoofing.
- **Detection**: Radar Doppler inconsistency check
- **Solution**: 3D radar mapping, vision assist
- **Tags**: radar, spoofing, aluminum

## GPS Jamming via SDR

- **Attack Type**: Physical Layer Disruption
- **Target**: GPS Receiver Module
- **Vulnerability**: Unprotected GPS reception
- **MITRE**: T1496
- **Impact**: Navigation failure
- **Tools**: HackRF One, GNURadio
- **Scenario**: The attacker uses a software-defined radio to jam GPS signals received by the vehicle, disrupting navigation and ADAS
- **Attack Steps**: 1. Acquire a HackRF One or similar SDR. 2. Install GNURadio and build a GPS jamming flowgraph. 3. Transmit noise or blank signals on GPS L1 frequency (1575.42 MHz). 4. Place device near vehicle to cause GPS loss. 5. Observe loss of navigation or map freezing.
- **Detection**: GPS signal loss alerts, NMEA monitoring
- **Solution**: Use GPS modules with anti-jamming detection and inertial backup
- **Tags**: GPS, SDR, Signal Interference

## GPS Coordinate Spoofing

- **Attack Type**: Signal Spoofing
- **Target**: GPS Module
- **Vulnerability**: Trusting unverified GPS input
- **MITRE**: T1631
- **Impact**: Location falsification
- **Tools**: gps-sdr-sim, HackRF
- **Scenario**: Send fake GPS data to mislead vehicle’s location systems
- **Attack Steps**: 1. Collect valid GPS data or generate spoofed ones using gps-sdr-sim. 2. Connect HackRF and configure for L1 frequency output. 3. Transmit fake GPS packets simulating another route. 4. Observe in-vehicle navigation redirecting based on fake coordinates.
- **Detection**: Compare GPS vs. inertial dead-reckoning data
- **Solution**: Cross-check sensors, install spoof-resistant GPS
- **Tags**: GPS, Spoofing, Navigation

## TPMS Replay Attack

- **Attack Type**: Wireless Replay Attack
- **Target**: TPMS Receiver
- **Vulnerability**: Unencrypted wireless signals
- **MITRE**: T1611
- **Impact**: Driver distraction
- **Tools**: RTL-SDR, TPMS Replay Scripts
- **Scenario**: Attacker captures valid TPMS packets and replays them to create false alerts
- **Attack Steps**: 1. Use RTL-SDR to sniff unencrypted TPMS data (433 MHz or 315 MHz). 2. Record packets from one tire sensor. 3. Replay using a transmitter to fake low pressure alert. 4. Vehicle displays warning despite normal tire pressure.
- **Detection**: Monitor pressure via manual tools vs. TPMS
- **Solution**: Encrypt TPMS messages, use rolling codes
- **Tags**: TPMS, Wireless, RF

## Custom LIDAR Spoofer Using IR LED

- **Attack Type**: LIDAR Spoofing
- **Target**: LIDAR Sensor
- **Vulnerability**: No validation of reflections
- **MITRE**: T1204
- **Impact**: Sensor hallucination
- **Tools**: Arduino, IR LEDs
- **Scenario**: Emit fake LIDAR reflections using IR LEDs to simulate objects
- **Attack Steps**: 1. Set up IR LED array with Arduino to emit pulses at LIDAR detection frequency. 2. Mount near vehicle's LIDAR unit. 3. Pulse LEDs to simulate objects (walls, cars). 4. Vehicle slows or avoids non-existent objects.
- **Detection**: LIDAR event logs, visual confirmation
- **Solution**: Filter based on reflection intensity and angle
- **Tags**: LIDAR, Sensor Spoof, IR

## Radar Ghost Injection

- **Attack Type**: Radar Spoofing
- **Target**: Radar Module
- **Vulnerability**: Lack of signal origin verification
- **MITRE**: T1204
- **Impact**: Phantom object detection
- **Tools**: mmWave signal emitter
- **Scenario**: Trick vehicle radar into detecting a ghost object (car)
- **Attack Steps**: 1. Design a mmWave emitter matching automotive radar frequency. 2. Pulse radar patterns to simulate an approaching vehicle. 3. Position device near target car. 4. Car automatically brakes or slows down.
- **Detection**: Radar echo pattern analysis
- **Solution**: Use Doppler shift filtering and directional radar arrays
- **Tags**: Radar, Ghost Car, mmWave

## GPS Overwrite via Internal Serial

- **Attack Type**: Sensor Manipulation
- **Target**: GPS Chipset
- **Vulnerability**: Exposed hardware interface
- **MITRE**: T1610
- **Impact**: Internal spoofing
- **Tools**: USB to TTL Cable, GPS Emulator
- **Scenario**: Internally access GPS UART and inject spoofed NMEA strings
- **Attack Steps**: 1. Gain access to infotainment board with exposed GPS serial interface. 2. Connect via USB-to-TTL cable. 3. Send fake NMEA strings mimicking movement. 4. Navigation software believes spoofed location.
- **Detection**: Monitor serial GPS input stream
- **Solution**: Secure firmware, obfuscate UART access
- **Tags**: Serial, GPS, Hardware Hack

## TPMS Fuzzer

- **Attack Type**: RF Fuzzing
- **Target**: TPMS System
- **Vulnerability**: Lack of input validation
- **MITRE**: T1609
- **Impact**: TPMS reliability degradation
- **Tools**: Scapy-radio, HackRF
- **Scenario**: Send malformed or extreme values in TPMS messages to trigger abnormal behavior
- **Attack Steps**: 1. Use scapy-radio to craft malformed TPMS messages (extreme PSI, wrong sensor ID). 2. Send messages over 433 MHz. 3. Observe vehicle behavior (e.g., failure to alert, wrong tire alert).
- **Detection**: Log TPMS values and source IDs
- **Solution**: Validate sensor ID and PSI range
- **Tags**: TPMS, RF, Fuzzing

## GPS Drift Loop Attack

- **Attack Type**: Signal Spoofing
- **Target**: GPS
- **Vulnerability**: Subtle spoofing
- **MITRE**: T1631
- **Impact**: Stealthy misrouting
- **Tools**: gps-sdr-sim
- **Scenario**: Gradually shift vehicle GPS location over time to cause unnoticed misrouting
- **Attack Steps**: 1. Modify gps-sdr-sim GPS path to slowly drift away from true location. 2. Broadcast spoofed signal via SDR. 3. Navigation shifts by small increments, unnoticed at first. 4. Eventually, the car is far off track.
- **Detection**: Compare GPS to accelerometer
- **Solution**: Set drift detection thresholds
- **Tags**: GPS, Drift, Subtle Attack

## Radar Denial via Noise Emitter

- **Attack Type**: Sensor Denial
- **Target**: Radar
- **Vulnerability**: No interference mitigation
- **MITRE**: T1496
- **Impact**: Radar blindness
- **Tools**: SDR Jammer
- **Scenario**: Overwhelm radar sensor with broad-spectrum noise
- **Attack Steps**: 1. Identify radar frequency band used (e.g., 76-77 GHz). 2. Emit wideband noise with sufficient power. 3. Radar sensor cannot detect valid returns, disables ADAS.
- **Detection**: Radar fault logs
- **Solution**: Use narrow beam + frequency hopping radar
- **Tags**: Radar, Jamming, ADAS

## TPMS Clone Injection

- **Attack Type**: Sensor Spoofing
- **Target**: TPMS Receiver
- **Vulnerability**: No uniqueness validation
- **MITRE**: T1609
- **Impact**: False maintenance alerts
- **Tools**: TPMS Cloner Tool
- **Scenario**: Clone a valid TPMS sensor ID and transmit fake alerts
- **Attack Steps**: 1. Identify TPMS ID using sniffing tools. 2. Program TPMS cloner to mimic same ID. 3. Transmit low-pressure message with cloned ID. 4. Car receives spoofed alert as if it’s from a real tire.
- **Detection**: Cross-check with physical readings
- **Solution**: Use encrypted sensor IDs
- **Tags**: TPMS, Clone, Spoof

## DSRC Packet Injection for Fake Hazard Alerts

- **Attack Type**: Wireless Injection
- **Target**: V2V Communication Systems
- **Vulnerability**: Lack of integrity/authentication in DSRC messages
- **MITRE**: T1620
- **Impact**: Causes driver confusion, unexpected auto-braking
- **Tools**: GNU Radio, USRP, Wireshark
- **Scenario**: Attacker injects fake emergency brake alerts using DSRC protocol to manipulate nearby vehicle responses.
- **Attack Steps**: 1. Understand the DSRC (Dedicated Short-Range Communications) stack and how BSM (Basic Safety Messages) are structured. 2. Use a Software-Defined Radio (SDR) such as USRP with GNU Radio to capture legitimate BSMs. 3. Modify or craft a fake emergency brake alert (BSM with high deceleration) using the same format. 4. Replay this packet using the SDR at an appropriate interval and power level to reach nearby vehicles. 5. Monitor nearby cars for sudden braking or driver alerts.
- **Detection**: Monitor BSM frequency, check for malformed or excessive emergency flags
- **Solution**: Use authenticated DSRC stacks and message verification
- **Tags**: DSRC, SDR, V2X, Wireless, Injection

## LTE Telematics API Abuse to Start Vehicle Remotely

- **Attack Type**: API Abuse
- **Target**: Telematics Cloud API
- **Vulnerability**: Insecure API endpoints, token reuse
- **MITRE**: T1589
- **Impact**: Remote engine start without user consent
- **Tools**: Burp Suite, Postman, LTE modem
- **Scenario**: Attacker exploits poorly authenticated telematics backend API to remotely start vehicle engine.
- **Attack Steps**: 1. Identify the mobile app used by a specific vehicle brand (e.g., NissanConnect, MyChevrolet). 2. Intercept communication between app and backend using Burp Suite or MITM proxy. 3. Observe the API request to remotely start engine. 4. Replay or manipulate the request using Postman or curl, bypassing authentication if possible (e.g., using leaked token). 5. Confirm engine startup via telematics command success response.
- **Detection**: Monitor for irregular API access logs
- **Solution**: Enforce strict API authentication, rate limits
- **Tags**: LTE, Telematics, API, Remote Start

## Bluetooth Classic Attack via BlueBorne Vulnerability

- **Attack Type**: Wireless Exploit
- **Target**: Infotainment Head Unit
- **Vulnerability**: Unpatched Bluetooth stack (e.g., BlueZ)
- **MITRE**: T1203
- **Impact**: Remote code execution or DoS
- **Tools**: BlueBorne Scanner, Linux, Metasploit
- **Scenario**: Attacker uses a BlueBorne vulnerability to compromise infotainment system via Bluetooth.
- **Attack Steps**: 1. Ensure the infotainment system supports Classic Bluetooth and has it enabled/discoverable. 2. Use a mobile device or Kali Linux to scan for Bluetooth-enabled car systems. 3. Identify vulnerable stack (e.g., BlueZ) using BlueBorne scanner. 4. Launch a Metasploit BlueBorne exploit against the identified target. 5. Gain code execution or crash the infotainment system.
- **Detection**: Bluetooth traffic anomaly detection
- **Solution**: Patch vulnerable Bluetooth stacks, disable unused profiles
- **Tags**: Bluetooth, BlueBorne, RCE, IVI

## LTE Telematics SIM Card Enumeration

- **Attack Type**: SIM Enumeration
- **Target**: Telematics Unit
- **Vulnerability**: SIM cloning, lack of SIM-based auth protections
- **MITRE**: T1606
- **Impact**: Account hijack, command replay
- **Tools**: SDR, SIM Cloning Tools, Osmocom
- **Scenario**: Attacker discovers IMSI/ICCID of vehicle telematics unit to hijack data plan or impersonate device.
- **Attack Steps**: 1. Use SDR (e.g., HackRF) to monitor LTE spectrum around target vehicle. 2. Identify the telematics module's IMSI by observing connection attempts. 3. Clone the SIM using tools like SIMCloner or SIMTester. 4. Insert cloned SIM into attacker modem to impersonate the vehicle. 5. Connect to the same backend services as the car, potentially controlling vehicle commands.
- **Detection**: Monitor IMSI reuse or rogue SIM usage
- **Solution**: Lock SIM to IMEI, monitor unexpected IMSI behavior
- **Tags**: LTE, SIM Attack, Telematics, IMSI

## Bluetooth Low Energy (BLE) Replay for Keyless Entry

- **Attack Type**: Wireless Replay
- **Target**: Keyless Entry System
- **Vulnerability**: Weak BLE pairing or static UUIDs
- **MITRE**: T1212
- **Impact**: Unauthorized vehicle entry
- **Tools**: NRF52 Sniffer, gatttool
- **Scenario**: Attacker captures BLE key fob packets and replays to unlock car.
- **Attack Steps**: 1. Use an NRF52 dongle to sniff BLE advertisement and connection packets from a key fob. 2. Identify the UUID and characteristics used by the keyless entry app. 3. Replay the connection and GATT writes to the car using gatttool or similar tools. 4. Monitor vehicle response (e.g., door unlock or light flash). 5. Test if session replay or nonce reuse is possible.
- **Detection**: BLE traffic replay detection
- **Solution**: Implement BLE bonding with encryption
- **Tags**: BLE, Replay Attack, Keyless

## DSRC MAC Flood to Deny Legitimate Messages

- **Attack Type**: DoS
- **Target**: V2V Communication
- **Vulnerability**: DSRC lacks source filtering
- **MITRE**: T1499
- **Impact**: V2V communication degraded
- **Tools**: GNU Radio, Custom Script
- **Scenario**: Attacker floods V2V channel with random MACs to overwhelm DSRC stack.
- **Attack Steps**: 1. Understand the DSRC MAC-layer packet structure. 2. Use GNU Radio to generate large volumes of malformed BSMs with randomized MAC addresses. 3. Transmit these packets continuously via SDR. 4. Nearby vehicles’ DSRC modules spend CPU filtering and may ignore legit messages. 5. Observe message processing delays or failures.
- **Detection**: Unusual DSRC traffic patterns
- **Solution**: Rate-limit DSRC reception, validate MACs
- **Tags**: DoS, DSRC, V2X

## Remote Climate Control Abuse via Telematics

- **Attack Type**: API Misuse
- **Target**: Telematics API
- **Vulnerability**: Session fixation, token reuse
- **MITRE**: T1550
- **Impact**: Energy drain, user confusion
- **Tools**: Mitmproxy, Postman
- **Scenario**: Exploit open APIs to toggle HVAC system remotely without owner consent.
- **Attack Steps**: 1. Intercept vehicle mobile app traffic using Mitmproxy. 2. Identify the endpoint responsible for toggling A/C or heater. 3. Copy the API request and analyze auth tokens or session cookies. 4. Use Postman to replay the request with token reuse or impersonation. 5. Confirm successful remote HVAC activation.
- **Detection**: Detect unusual HVAC toggles
- **Solution**: Expire tokens quickly, require 2FA
- **Tags**: HVAC, API Abuse, Telematics

## V2X Certificate Abuse for Message Injection

- **Attack Type**: Cryptographic Abuse
- **Target**: V2X Devices
- **Vulnerability**: Acceptance of non-production certs
- **MITRE**: T1588
- **Impact**: Trust deception, fake warnings
- **Tools**: SCMS Emulator, DSRC Stack
- **Scenario**: Attacker uses test certificates to inject trusted DSRC messages.
- **Attack Steps**: 1. Obtain a sample or test V2X certificate used for development. 2. Build a compatible message using the DSRC stack. 3. Sign it with the valid (test) certificate. 4. Inject message over the air via SDR. 5. Watch if vehicles treat it as trusted despite improper cert lineage.
- **Detection**: Certificate chain validation
- **Solution**: Accept only production-signed messages
- **Tags**: V2X, Certificate Abuse, SCMS

## Bluetooth Stack Overflows on IVI System

- **Attack Type**: Memory Corruption
- **Target**: Infotainment Bluetooth Daemon
- **Vulnerability**: Lack of boundary checks in SDP parser
- **MITRE**: T1203
- **Impact**: DoS or code execution
- **Tools**: Custom Python SDP Fuzzer
- **Scenario**: Overflow Bluetooth daemon buffers via malformed SDP packets.
- **Attack Steps**: 1. Identify the Bluetooth daemon on the IVI system (e.g., BlueZ). 2. Build malformed SDP packets using a custom fuzzer. 3. Send the packets from a nearby device over Bluetooth. 4. Monitor the IVI system for crashes or odd behavior. 5. Analyze system logs for buffer overflow indicators.
- **Detection**: Monitor syslogs and crash dumps
- **Solution**: Patch daemon, fuzz pre-deployment
- **Tags**: Bluetooth, SDP, Overflow

## GSM Interception of Telematics via Fake BTS

- **Attack Type**: GSM MITM
- **Target**: Telematics over GSM
- **Vulnerability**: Use of 2G without encryption
- **MITRE**: T1630
- **Impact**: Data leakage or remote control
- **Tools**: OpenBTS, BladeRF
- **Scenario**: Use fake BTS to intercept 2G telematics communication.
- **Attack Steps**: 1. Deploy OpenBTS using BladeRF or LimeSDR configured to broadcast as a nearby tower. 2. Wait for telematics module fallback to 2G GSM. 3. Intercept traffic such as SMS-based commands or data payloads. 4. Log messages and analyze backend communication formats. 5. Attempt command injection via intercepted channels.
- **Detection**: IMSI catcher detection tools
- **Solution**: Disable 2G fallback, enforce LTE-only
- **Tags**: GSM, MITM, BTS

## DSRC Message Injection to Spoof Emergency Vehicle

- **Attack Type**: Wireless Communication Attacks
- **Target**: Smart Vehicle
- **Vulnerability**: DSRC packet trust without authentication
- **MITRE**: T0866 – Transmit Fake Traffic
- **Impact**: Traffic disruption
- **Tools**: GNU Radio, DSRC transceiver, Wireshark
- **Scenario**: An attacker injects DSRC packets to make nearby cars think an emergency vehicle is approaching.
- **Attack Steps**: 1. Set up a DSRC-capable transceiver (e.g., using GNU Radio + SDR hardware). 2. Capture legitimate DSRC packets from emergency vehicles. 3. Analyze the structure and contents of the emergency vehicle broadcast. 4. Create a custom crafted DSRC message mimicking emergency vehicle alert. 5. Transmit the spoofed message in a controlled environment. 6. Observe if nearby vehicles slow down or yield. 7. Repeat and log any abnormal reactions.
- **Detection**: Monitoring unusual DSRC broadcast patterns
- **Solution**: Implement DSRC authentication & PKI
- **Tags**: DSRC spoofing, emergency message injection, spoofed V2X

## Remote Car Unlock via Telematics API Abuse

- **Attack Type**: Wireless Communication Attacks
- **Target**: Telematics Cloud
- **Vulnerability**: Insecure API authorization
- **MITRE**: T1586 – Compromise Application API
- **Impact**: Remote access to vehicle functions
- **Tools**: Burp Suite, Postman, Telematics API docs
- **Scenario**: Attacker exploits poorly secured telematics backend to remotely unlock target vehicle.
- **Attack Steps**: 1. Discover target automaker’s mobile app and analyze traffic between app and backend server. 2. Use Burp Suite to intercept API calls. 3. Check for authentication headers and identify if tokens can be reused or guessed. 4. Enumerate vehicle VINs or IDs via fuzzing. 5. Send a crafted POST request to unlock door API endpoint with a victim's VIN. 6. Monitor response and physical confirmation (if in lab). 7. Repeat across multiple endpoints for engine start, honk, etc.
- **Detection**: API access log correlation; unusual IPs
- **Solution**: Enforce proper API authentication and input validation
- **Tags**: Telematics abuse, remote unlock, API fuzzing

## Classic Bluetooth Pairing Attack on Infotainment

- **Attack Type**: Wireless Communication Attacks
- **Target**: IVI System
- **Vulnerability**: Weak or default PIN in pairing
- **MITRE**: T1476 – Exploit Bluetooth
- **Impact**: Privacy breach or media system compromise
- **Tools**: Ubertooth One, hcitool, btmon
- **Scenario**: Exploiting insecure pairing mechanism to gain access to vehicle IVI system.
- **Attack Steps**: 1. Scan for nearby vehicles broadcasting Bluetooth devices. 2. Identify vehicle name, MAC address, and pairing mode (e.g., PIN-based or SSP). 3. Use hcitool and btmon to capture pairing attempts. 4. Attempt brute-force pairing using common PINs (0000, 1234). 5. Once paired, test commands like contact sync, media access, or code execution. 6. If vulnerable, persist Bluetooth connection or install malicious app via OBEX. 7. Analyze post-connection services for possible data leaks.
- **Detection**: Monitor unauthorized pairing attempts
- **Solution**: Enforce secure pairing mechanisms & limit pairing time window
- **Tags**: Bluetooth spoofing, media control, PIN brute-force

## V2X Beacon Flood to Disrupt Nearby Vehicles

- **Attack Type**: Wireless Communication Attacks
- **Target**: V2V Module
- **Vulnerability**: Lack of beacon message validation
- **MITRE**: T1583 – Transmit Corrupt Data
- **Impact**: Safety function degradation
- **Tools**: DSRC transceiver, Scapy, GNURadio
- **Scenario**: The attacker sends a flood of fake V2X beacon messages to jam the processing of legitimate traffic.
- **Attack Steps**: 1. Set up a DSRC transceiver to operate in the same band as V2X. 2. Write a custom script to generate hundreds of fake V2X beacons using Scapy. 3. Each beacon contains random or spoofed vehicle locations. 4. Transmit these beacons rapidly using GNU Radio. 5. Observe if real vehicles begin to slow down or act erratically due to beacon overload. 6. Measure CPU and bandwidth usage on victim vehicle. 7. Repeat test in simulation if real-world is unavailable.
- **Detection**: DSRC spectrum usage monitoring
- **Solution**: Message signature validation and rate limiting
- **Tags**: V2X flooding, DSRC denial-of-service, beacon spoof

## Remote Engine Start via VIN Guessing and API Abuse

- **Attack Type**: Wireless Communication Attacks
- **Target**: Telematics Cloud
- **Vulnerability**: Insecure API design and predictable IDs
- **MITRE**: T1586 – Exploit Public-Facing API
- **Impact**: Unauthorized remote control
- **Tools**: Postman, Burp Suite, VIN pattern docs
- **Scenario**: Attacker remotely starts engines by guessing VINs and abusing backend APIs without authentication.
- **Attack Steps**: 1. Observe vehicle VIN structure (WMI + serials). 2. Use Postman to enumerate VINs via the automaker’s remote API. 3. Identify insecure endpoints like /start_engine that lack proper authorization. 4. Send engine start requests using guessed VINs. 5. If successful, attacker can perform remote starts anonymously. 6. Log successful commands and time. 7. Use API rate limits and telemetry to avoid detection.
- **Detection**: Log-based anomaly detection; VIN abuse monitoring
- **Solution**: VIN-based auth should be tied to user identity
- **Tags**: API abuse, remote start, VIN guessing

## BLE-Based Location Tracking of Vehicle Owner

- **Attack Type**: Wireless Communication Attacks
- **Target**: Key Fob
- **Vulnerability**: BLE broadcasts are often unauthenticated
- **MITRE**: T1410 – Eavesdropping via BLE
- **Impact**: Privacy violation and stalking
- **Tools**: BLE Scanner, btmon, Android BLE tools
- **Scenario**: Using passive BLE scanning to track when/where vehicle owners come near their car.
- **Attack Steps**: 1. Monitor BLE advertisement packets in parking lots or public locations. 2. Identify repeating BLE UUIDs or MAC addresses tied to car brands (e.g., key fob broadcasts). 3. Log timestamps and locations when device appears. 4. Build pattern of when target arrives or leaves. 5. Cross-reference with surveillance for owner identity. 6. Use BLE spoofing to trigger vehicle wake-ups. 7. Demonstrate tracking potential over time.
- **Detection**: BLE traffic analysis; physical surveillance integration
- **Solution**: Use MAC randomization and limit BLE advertisement
- **Tags**: BLE tracking, privacy risk, passive scan

## LTE Baseband Attack via Malformed Paging Message

- **Attack Type**: Wireless Communication Attacks
- **Target**: Telematics Unit
- **Vulnerability**: LTE baseband lacks robust message validation
- **MITRE**: T1602 – Radio Protocol Exploit
- **Impact**: Denial of telemetry / control
- **Tools**: srsLTE, USRP, Wireshark
- **Scenario**: Malformed LTE paging message crashes or hijacks modem in telematics control unit (TCU).
- **Attack Steps**: 1. Deploy LTE SDR environment using srsLTE and USRP. 2. Identify the IMSI of the vehicle’s TCU via passive sniffing. 3. Craft a malformed paging message targeting that IMSI. 4. Transmit the message on LTE band. 5. Observe if the TCU crashes, reboots, or accepts attacker control. 6. Use this to potentially prevent telemetry uploads or eCall responses. 7. Document crash or exploitation behavior.
- **Detection**: Modem health telemetry monitoring
- **Solution**: Apply baseband firmware patches & validate LTE stack
- **Tags**: LTE attack, baseband bug, TCU denial, malformed paging

## App Exploit via Unvalidated OTA Infotainment Update

- **Attack Type**: Wireless Communication Attacks
- **Target**: IVI Android OS
- **Vulnerability**: Lack of update signature verification
- **MITRE**: T1622 – Forge Firmware / App Package
- **Impact**: Full control of infotainment system
- **Tools**: Android SDK, APKTool, Custom OTA package
- **Scenario**: Attacker crafts malicious OTA update that installs rogue app on IVI system bypassing validation.
- **Attack Steps**: 1. Reverse engineer existing IVI Android apps using APKTool. 2. Create a repackaged version with embedded malware. 3. Forge an OTA update ZIP following same structure as OEM update. 4. Inject the APK into update and resign with fake cert. 5. Upload OTA file to infotainment system via USB, Wi-Fi, or Bluetooth if unprotected. 6. Observe if installation proceeds without signature checks. 7. Test malicious functionality in IVI (e.g., keylogging, media spying).
- **Detection**: File hash mismatch detection; OTA server logs
- **Solution**: Enforce digital signature validation on updates
- **Tags**: Android Auto exploit, rogue APK, OTA abuse

## Vehicle Wake-Up via Bluetooth HCI Command Injection

- **Attack Type**: Wireless Communication Attacks
- **Target**: IVI System
- **Vulnerability**: Improper HCI command validation
- **MITRE**: T1476 – Exploit Bluetooth Stack
- **Impact**: System crash or Bluetooth stack exploit
- **Tools**: HCI Logger, btmon, custom firmware
- **Scenario**: Using malformed HCI command via Bluetooth to wake or crash car’s IVI system.
- **Attack Steps**: 1. Connect to vehicle’s Bluetooth interface using supported tools. 2. Send malformed HCI (Host Controller Interface) command that triggers buffer overflow or parsing bug. 3. Observe crash or reboot in IVI system. 4. Repeat injection with different HCI codes to test behaviors. 5. Test for permanent crash (DoS) or privilege escalation. 6. Document firmware version and Bluetooth chipset used. 7. Develop PoC for known vulnerable stack.
- **Detection**: Crash dump from infotainment logs
- **Solution**: Harden Bluetooth firmware and reject malformed commands
- **Tags**: HCI injection, DoS via Bluetooth, IVI crash

## Spoofed Cloud Command to Disable Vehicle Alarm

- **Attack Type**: Wireless Communication Attacks
- **Target**: Cloud Backend
- **Vulnerability**: Insecure cloud command processing
- **MITRE**: T1609 – Remote Command Injection
- **Impact**: Silent intrusion without owner knowledge
- **Tools**: Mitmproxy, Burp Suite, API docs
- **Scenario**: Attacker sends spoofed cloud message to disable alarm and open doors silently.
- **Attack Steps**: 1. Intercept traffic from vehicle app to backend using Mitmproxy. 2. Replay cloud commands using Burp Suite. 3. Craft a spoofed disable-alarm command with correct headers. 4. Identify target vehicle ID via fuzzing or social engineering. 5. Test if the command disables alarm without notifying the owner. 6. If successful, perform silent unlock and entry. 7. Log request/response pairs and time delays for future use.
- **Detection**: Audit command history; log unknown device sources
- **Solution**: Require strong auth and geo-checks for sensitive commands
- **Tags**: Cloud spoofing, silent car unlock, backend command abuse

## Basic Relay Attack Using Commercial Toolkits

- **Attack Type**: Relay Attack
- **Target**: Modern cars with passive entry
- **Vulnerability**: Keyless system trusts proximity
- **MITRE**: T1648 (Compromise Client Software Binary)
- **Impact**: Unauthorized car access
- **Tools**: Keyless repeater kits, SDR, battery packs
- **Scenario**: Attacker uses an off-the-shelf relay toolkit to unlock a car parked near a house by relaying the signal from the key inside.
- **Attack Steps**: 1. Identify a vehicle that uses passive entry (keyless unlock). 2. Use a two-part relay system: one attacker near the house, another near the car. 3. Activate the relay device to sniff for the key's RF signal inside the house. 4. Relay the signal to the second device near the vehicle. 5. The car detects a valid key and unlocks automatically. 6. Open the vehicle and optionally start the engine using push-button ignition.
- **Detection**: Unusual unlock patterns or time/location mismatches
- **Solution**: Use Faraday pouches, motion-detecting key fobs
- **Tags**: relay, keyless, RF, physical access

## Passive Relay Attack in Apartment Parking Lot

- **Attack Type**: Relay Attack
- **Target**: Keyless-enabled vehicles
- **Vulnerability**: Key proximity logic exploited
- **MITRE**: T1133 (External Remote Services)
- **Impact**: Stealthy vehicle unlocking
- **Tools**: RF amplifiers, antenna rigs
- **Scenario**: Attacker waits in a residential parking lot and uses passive equipment to amplify the signal from a key inside the apartment above.
- **Attack Steps**: 1. Scout apartment buildings with ground-level parking. 2. Target vehicles with keyless entry parked directly below apartments. 3. Use a high-gain antenna to passively sniff signals from above. 4. Amplify and relay the captured signal toward the target vehicle. 5. Vehicle unlocks assuming the key is nearby. 6. Attacker enters vehicle and may connect diagnostics to start engine.
- **Detection**: Signal strength anomalies
- **Solution**: Relocate parking away from apartments
- **Tags**: passive relay, RF, apartment

## Garage Relay with Close-Proximity Amplifier

- **Attack Type**: Relay Attack
- **Target**: Residential keyless cars
- **Vulnerability**: Signal strength trust in design
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Silent drive-off theft
- **Tools**: RF repeater + antenna, SDR
- **Scenario**: Attacker targets vehicles parked in attached garages while the key is near the front door inside.
- **Attack Steps**: 1. Find houses with garages and key fob storage close to entryway. 2. Position relay receiver near front door to pick up key fob signal. 3. Relay transmission to a transmitter placed in the garage. 4. Vehicle unlocks and may start if push-to-start. 5. Car is driven out quietly, especially with electric vehicles.
- **Detection**: No alerts from traditional alarms
- **Solution**: Move keys away from entry points
- **Tags**: garage, home relay, quiet theft

## Entry and Engine Start via Relay Loop

- **Attack Type**: Relay Attack
- **Target**: Push-start vehicles
- **Vulnerability**: Trust boundary flaw
- **MITRE**: T1556 (Modify Authentication Process)
- **Impact**: Full vehicle theft
- **Tools**: Key repeater toolkits, Li-ion batteries
- **Scenario**: Full relay cycle including unlock and engine start, performed from outside the victim’s property.
- **Attack Steps**: 1. Use battery-powered relay tools to simulate proximity to both key and car. 2. Place one device near the house window or door to capture the fob signal. 3. Relay signal to a second device near the vehicle. 4. Unlock the car and press the start button while the relay is active. 5. Engine starts, and the vehicle can be driven away immediately.
- **Detection**: Logs may show start without physical key
- **Solution**: Re-auth challenge when key leaves proximity
- **Tags**: full relay, engine start, push-to-go

## Relay with Delayed Disconnect to Bypass Anti-Relay Firmware

- **Attack Type**: Relay Attack
- **Target**: Cars with basic relay detection
- **Vulnerability**: Firmware doesn’t check full session
- **MITRE**: T1557.001 (Bluetooth)
- **Impact**: Defeats updated anti-relay tech
- **Tools**: Advanced relay tools
- **Scenario**: Attacker maintains relay for 30+ seconds to bypass newer anti-relay mechanisms.
- **Attack Steps**: 1. Scan for vehicles that unlock via proximity but resist rapid relays. 2. Use devices with stable RF buffering and delay features. 3. Maintain continuous signal from house to car for longer periods. 4. Allow car to verify signal stability and unlock. 5. Start engine before system detects anomaly or signal drop.
- **Detection**: Device duration logs
- **Solution**: RF jitter detection or timeout limits
- **Tags**: bypass, long relay, anti-detection

## Relay Theft in Underground Parking

- **Attack Type**: Relay Attack
- **Target**: Apartment-based targets
- **Vulnerability**: Lack of RF shielding in walls
- **MITRE**: T1562 (Impair Defenses)
- **Impact**: Car theft without breach
- **Tools**: Long-range relay system, antennas
- **Scenario**: Attacker steals a car from underground parking using relayed key signals from apartments above.
- **Attack Steps**: 1. Identify vehicles parked in basement or underground lots. 2. Locate apartments above with likely key locations near windows. 3. Use high-power directional antenna to find signal hotspots. 4. Activate relay to unlock car. 5. Start car and drive out without any physical access to the apartment.
- **Detection**: No camera evidence of access
- **Solution**: Educate residents to store keys deep inside
- **Tags**: underground, relay, key fob

## Low-Cost DIY Relay Toolkit Attack

- **Attack Type**: Relay Attack
- **Target**: Any RF-based key system
- **Vulnerability**: No encryption on proximity unlock
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Makes attacks accessible to amateurs
- **Tools**: HackRF One, Yagi antenna, power banks
- **Scenario**: Using budget SDRs and antennas to build a low-cost key relay system.
- **Attack Steps**: 1. Build two HackRF-based relay devices with Linux. 2. Program software to capture and replay 315/433/868 MHz signals. 3. Use portable batteries to keep gear stealthy. 4. Perform standard relay steps: key sniffing, signal forwarding, unlock. 5. Demonstrates how affordable relay attacks can be.
- **Detection**: N/A
- **Solution**: Hardware token pairing, encryption
- **Tags**: cheap relay, SDR hack, open-source

## Relay Chain Across Large Parking Lot

- **Attack Type**: Relay Attack
- **Target**: Public parking environments
- **Vulnerability**: Distance range limitations
- **MITRE**: T1071.001 (Application Layer Protocol: Web Protocols)
- **Impact**: Theft without confrontation
- **Tools**: RF extenders, long-range Wi-Fi links
- **Scenario**: Team of two attackers bridges a signal across a wide area in a mall parking lot.
- **Attack Steps**: 1. One attacker near the store where victim is shopping with key in pocket. 2. Second attacker near the car in the lot. 3. Relay devices link across several hundred meters. 4. Car unlocks and engine starts. 5. Car is stolen while victim is distracted in store.
- **Detection**: Motion logs or alarms if tampered
- **Solution**: Limit RF range on keys or timeout
- **Tags**: long range, mall, distraction

## Relay Attack During Restaurant Visit

- **Attack Type**: Relay Attack
- **Target**: Vehicles near public venues
- **Vulnerability**: Human distraction + RF exploit
- **MITRE**: T1176 (Browser Extensions)
- **Impact**: Real-time, low-risk car theft
- **Tools**: Commercial RF repeater kits
- **Scenario**: Attackers target key signal while victim dines nearby, using proximity relay.
- **Attack Steps**: 1. Target popular dining locations with outdoor seating. 2. Attacker 1 walks by tables sniffing for key signals. 3. Attacker 2 stands near the car in the lot. 4. Relay starts instantly; car unlocks and theft occurs. 5. Victim is unaware while distracted.
- **Detection**: Parking logs or entry alerts
- **Solution**: Inform public about RF shielding
- **Tags**: restaurant, ambient theft, relay

## Combined Relay + Jam for Faster Access

- **Attack Type**: Relay Attack
- **Target**: All keyless vehicles
- **Vulnerability**: Unlock signal is not confirmed visually
- **MITRE**: T1496 (Resource Hijacking)
- **Impact**: Fast theft, no lock occurred
- **Tools**: RF jammer, relay kit
- **Scenario**: Attacker jams unlock signal to prevent locking, then uses relay to enter and start vehicle.
- **Attack Steps**: 1. Observe victim locking car and jam unlock signal to prevent actual locking. 2. Victim walks away assuming car is locked. 3. Activate relay device to simulate key proximity. 4. Open door and start car immediately. 5. Vehicle taken in under 2 minutes.
- **Detection**: Jam detection tools, door relock logic
- **Solution**: Confirm visual lock, add motion alert
- **Tags**: relay + jam, combo, fast theft

## MiTM-Based Fake Firmware Injection via Rogue Wi-Fi

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: Embedded Systems
- **Vulnerability**: No TLS validation on OTA update channel
- **MITRE**: T1557
- **Impact**: Remote compromise of ECU firmware
- **Tools**: Wireshark, Bettercap, FakeDNS
- **Scenario**: Attacker sets up rogue Wi-Fi hotspot to spoof OEM server and deliver malicious OTA
- **Attack Steps**: 1. Set up a rogue Wi-Fi AP mimicking the vehicle’s known OTA update network name (SSID).2. Redirect DNS queries to a fake OTA server controlled by the attacker.3. Host malicious firmware mimicking OEM update format.4. Intercept the update request from the vehicle and respond with the fake firmware.5. Wait for vehicle to download and install malicious update.
- **Detection**: Monitor network traffic for unauthorized OTA traffic
- **Solution**: Enforce HTTPS, server certificate pinning
- **Tags**: FOTA, MiTM, Fake Updates, OTA

## OTA Server Spoofing via DNS Hijack

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: Vehicle Telematics
- **Vulnerability**: DNS spoofing & lack of source validation
- **MITRE**: T1565
- **Impact**: Unauthorized code injection
- **Tools**: Responder, DNSChef, Ghidra
- **Scenario**: Hijack DNS to redirect firmware update checks to a malicious server
- **Attack Steps**: 1. Gain access to local network or upstream DNS.2. Use DNSChef or Responder to hijack DNS queries for the legitimate OTA server.3. Set up fake OTA server with forged firmware.4. When the vehicle queries for updates, respond with the malicious firmware payload.5. Ensure firmware passes basic integrity checks to be accepted.
- **Detection**: Passive DNS monitoring, integrity check of firmware
- **Solution**: DNSSEC, enforce cryptographic firmware validation
- **Tags**: DNS Hijacking, OTA Attack, Automotive Security

## Downgrade Attack to Reintroduce Known Exploit

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: ECU
- **Vulnerability**: Weak downgrade protection & version logic
- **MITRE**: T1601
- **Impact**: Re-enable deprecated vulnerabilities
- **Tools**: Ghidra, Binwalk, UDS Tool
- **Scenario**: Push an older firmware version that still contains known vulnerabilities
- **Attack Steps**: 1. Identify an older firmware version vulnerable to a known bug.2. Use MiTM, USB-based flashing, or spoofed OTA server to provide this older firmware to the vehicle.3. Trick the system into accepting the downgrade (e.g., by bypassing version check or exploiting flaws in update logic).4. Once installed, exploit the known bug in the older firmware for full control.
- **Detection**: Monitor for firmware version rollbacks
- **Solution**: Enforce anti-downgrade checks, rollback prevention
- **Tags**: Downgrade Attack, FOTA Exploits, Legacy Bugs

## Exploiting USB-based FOTA Process

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: Embedded Devices
- **Vulnerability**: No integrity validation on USB firmware
- **MITRE**: T1200
- **Impact**: Backdoor in ECU firmware
- **Tools**: USB analyzer, Ghidra, Modified ISO
- **Scenario**: Tamper with USB firmware update to inject malicious code
- **Attack Steps**: 1. Reverse-engineer the USB-based firmware update structure using Ghidra.2. Modify firmware payload with injected shellcode or reverse shell.3. Repack the update in a valid-looking format.4. Provide it to the vehicle via USB during maintenance.5. Firmware installs malicious payload unknowingly.
- **Detection**: Check USB firmware hash and signature
- **Solution**: Use signed updates, verify authenticity
- **Tags**: USB FOTA, Physical Access, Firmware Tampering

## OTA Update Brute-Force Timing Analysis

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: Vehicle Telematics
- **Vulnerability**: Predictable OTA timing behavior
- **MITRE**: T1595
- **Impact**: High stealth injection of rogue firmware
- **Tools**: Network Monitor, Wireshark
- **Scenario**: Guess or brute-force the OTA scheduling logic to launch spoofed updates
- **Attack Steps**: 1. Monitor OTA update intervals and patterns (e.g., time of day, week, idle state).2. Build a model of when vehicles typically poll OTA servers.3. Time the delivery of spoofed firmware to align with this window.4. Reduce chance of detection by mimicking normal update behavior.5. Use fake OTA server to supply malicious firmware.
- **Detection**: Correlate OTA request timing anomalies
- **Solution**: Add randomness to OTA polling times, log all update events
- **Tags**: FOTA, Brute Force Timing, OTA Attack

## Targeting Insecure FOTA APIs

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: Cloud / Backend
- **Vulnerability**: Poor access control in OTA backend APIs
- **MITRE**: T1190
- **Impact**: Backend API abuse → vehicle compromise
- **Tools**: Postman, Burp Suite, Shodan
- **Scenario**: Exploit vulnerable cloud API to push unauthorized updates
- **Attack Steps**: 1. Discover exposed OTA update management APIs via Shodan or recon.2. Use tools like Burp Suite to inspect the endpoints and test auth mechanisms.3. If auth is weak (e.g., hardcoded token), use the API to upload custom firmware.4. Vehicle polls update and installs attacker-supplied image.5. Maintain access or disable vehicle functionality.
- **Detection**: Audit cloud API logs, enforce role-based access control
- **Solution**: Secure OTA backend with token expiration, mTLS, and RBAC
- **Tags**: API Hacking, FOTA Injection, Backend Abuse

## Reverse Engineering Firmware Signing Check

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: ECU Firmware
- **Vulnerability**: Insecure or absent digital signature checks
- **MITRE**: T1542
- **Impact**: Permanent backdoor via custom firmware
- **Tools**: Ghidra, IDA Pro, JTAG interface
- **Scenario**: Bypass or disable firmware signature check in ECU bootloader
- **Attack Steps**: 1. Dump ECU firmware using JTAG or bootloader access.2. Reverse engineer the signature verification function using Ghidra or IDA.3. Identify check logic and remove or NOP it.4. Repack firmware with attacker’s payload.5. Flash firmware via OTA or USB update and gain full ECU control.
- **Detection**: Compare known-good firmware binaries with current version
- **Solution**: Implement strong, enforced cryptographic checks at bootloader
- **Tags**: ECU Hacking, Ghidra, Firmware Bypass

## Compromising Firmware Update Distribution Chain

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: Cloud/CDN Infra
- **Vulnerability**: Weak distribution security, mirror tampering
- **MITRE**: T1195
- **Impact**: Mass firmware compromise via CDN
- **Tools**: CDN Scanner, Ghidra, Custom Payload
- **Scenario**: Inject malicious firmware at the CDN or mirror used for update delivery
- **Attack Steps**: 1. Identify CDN/mirror infrastructure used for OTA updates.2. Exploit misconfigurations or use stolen credentials to upload modified firmware.3. Replace legitimate image with attacker-controlled version.4. Wait for vehicle to download from the compromised mirror.5. Observe malicious code execution during boot or driving.
- **Detection**: Monitor hash mismatches of downloaded firmware
- **Solution**: Signed hashes, strict CDN access control
- **Tags**: FOTA Supply Chain, CDN Exploit, OTA Risk

## Rogue Insider Uploads Fake Firmware via Internal Portal

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: Corporate Insider
- **Vulnerability**: Insider threat, weak firmware approval
- **MITRE**: T1203
- **Impact**: Insider-triggered persistent compromise
- **Tools**: Internal Admin Panel, Ghidra
- **Scenario**: Insider misuses internal OTA upload portal to inject unauthorized firmware
- **Attack Steps**: 1. Insider with access to OEM’s OTA admin portal prepares a firmware containing a stealthy backdoor.2. Uses portal credentials to upload firmware image to OTA system.3. Flags firmware for deployment to a test fleet or vehicles in the field.4. Vehicles install firmware assuming it’s valid.5. Attacker maintains persistence.
- **Detection**: Log access to OTA deployment tools, require multi-signature
- **Solution**: Use change control, enforce multi-party approval for firmware
- **Tags**: Insider Threat, OTA Portal Abuse

## FOTA Update Replay via Traffic Capture

- **Attack Type**: Firmware Over-The-Air Abuse
- **Target**: Vehicle Systems
- **Vulnerability**: No freshness or replay protection on updates
- **MITRE**: T1211
- **Impact**: Installation of outdated/compromised firmware
- **Tools**: Wireshark, tcpreplay, Ghidra
- **Scenario**: Replay old captured firmware update traffic to re-trigger installation
- **Attack Steps**: 1. Capture a real OTA update session using Wireshark.2. Extract the firmware and observe HTTP/HTTPS structure.3. Reuse the captured packets or mimic their structure using tcpreplay or crafted scripts.4. Send the replayed update to a vehicle expecting OTA.5. Vehicle accepts firmware assuming it’s a valid retry.
- **Detection**: Detect redundant update attempts with same hash/version
- **Solution**: Implement replay protection using timestamps and update counters
- **Tags**: Replay Attacks, FOTA Security, Network Exploit

## CAN Injection for Brake Override

- **Attack Type**: Braking Spoofing
- **Target**: In-Vehicle CAN Network
- **Vulnerability**: Lack of message authentication on CAN bus
- **MITRE**: T1430
- **Impact**: Sudden braking, accident potential
- **Tools**: CANtact, SavvyCAN
- **Scenario**: Attacker injects crafted CAN messages to activate braking even when the driver is not applying the brake
- **Attack Steps**: 1. Connect to the vehicle’s OBD-II port using a CAN interface like CANtact.2. Use a sniffer tool (e.g., SavvyCAN) to identify brake signal messages during actual brake pedal press.3. Record and replay the brake signal repeatedly while the vehicle is in motion.4. The vehicle may start braking autonomously, confusing the driver and creating safety risks.5. In advanced versions, modify the message timing to appear more legitimate.
- **Detection**: Monitor for anomalous braking messages during operation
- **Solution**: Use cryptographic authentication for CAN messages
- **Tags**: brake spoofing, CAN injection, safety

## Spoofed Throttle Input to Force Acceleration

- **Attack Type**: Acceleration Spoofing
- **Target**: ECU / Powertrain
- **Vulnerability**: CAN messages not verified for authenticity
- **MITRE**: T1441
- **Impact**: Dangerous unintended acceleration
- **Tools**: CANalyzat0r, UDS tools
- **Scenario**: Adversary sends false throttle position messages to the ECU
- **Attack Steps**: 1. Establish connection to the vehicle’s CAN bus.2. Observe CAN traffic while pressing and releasing the accelerator.3. Identify the PID associated with throttle position.4. Send repeated messages simulating high throttle input.5. Engine RPM and acceleration increase without driver input.
- **Detection**: Unexpected RPM rise or throttle value in logs
- **Solution**: Implement secure gateway for control messages
- **Tags**: throttle, spoofing, ECU

## Induced Gear Shift While Driving

- **Attack Type**: Gear Manipulation
- **Target**: Transmission Control Module (TCM)
- **Vulnerability**: Unauthenticated control signals
- **MITRE**: T1496
- **Impact**: Loss of drivetrain control
- **Tools**: UDS exploit tools, CANoe
- **Scenario**: Tricking automatic transmission into shifting to neutral or reverse
- **Attack Steps**: 1. Identify the gear shift control signals by logging data while shifting manually.2. Inject commands via CAN to change the gear to neutral or reverse while the car is moving.3. Monitor vehicle response — sudden disengagement of drive mode may occur.4. In worst-case scenarios, forced reverse at speed damages transmission.
- **Detection**: Gear status logs and event-based telemetry
- **Solution**: Firmware validation and intrusion detection
- **Tags**: TCM, gear spoof, reverse injection

## Cluster Display Spoof – Fake Speedometer

- **Attack Type**: Display Manipulation
- **Target**: Instrument Cluster
- **Vulnerability**: Unprotected cluster input
- **MITRE**: T1397
- **Impact**: Safety risk due to driver misjudgment
- **Tools**: UDS, CAN Bus Analyzer
- **Scenario**: Adversary modifies speedometer readings to show false speed
- **Attack Steps**: 1. Use reverse engineering to identify CAN messages for vehicle speed display.2. While the vehicle is in motion, inject messages that show speed as 0 or lower than actual.3. Driver believes vehicle is slow and may over-accelerate.4. Combine with brake spoofing to confuse driver response further.
- **Detection**: Compare GPS speed with cluster reading
- **Solution**: Validate display data via secondary sensors
- **Tags**: cluster spoof, speed hack, CAN

## Fuel Gauge Manipulation

- **Attack Type**: Display Manipulation
- **Target**: Instrument Cluster
- **Vulnerability**: Insecure display input from CAN
- **MITRE**: T1387
- **Impact**: Vehicle may stop unexpectedly
- **Tools**: SavvyCAN, CANBus Triple
- **Scenario**: Mislead driver by showing false fuel levels to cause breakdown
- **Attack Steps**: 1. Tap into CAN bus and find the message controlling fuel level.2. Modify the value to full or empty, regardless of true level.3. Causes confusion during long trips or leads to intentional stalling.4. In fleet vehicles, may disrupt logistic operations.
- **Detection**: Correlation of fuel readings with actual consumption
- **Solution**: Sensor fusion and integrity checks
- **Tags**: fuel level spoof, fleet attack

## ABS Override via CAN Spoofing

- **Attack Type**: Braking Spoofing
- **Target**: ABS ECU
- **Vulnerability**: Insecure sensor signal verification
- **MITRE**: T1486
- **Impact**: Increased braking distance, accident
- **Tools**: CANalyzer, custom script
- **Scenario**: Disable or confuse Anti-lock Braking System (ABS) signals
- **Attack Steps**: 1. Capture ABS activation signals while applying hard brakes.2. Re-inject modified messages that show wheels as not locked.3. ABS system does not activate in a real skid, causing possible loss of control.4. Useful in icy or wet road scenarios to induce accidents.
- **Detection**: ABS activation logs, wheel speed sensor comparison
- **Solution**: Validate sensor state redundancy
- **Tags**: ABS spoof, CAN fuzz, safety

## Fake Engine Temperature Alert

- **Attack Type**: Cluster Display Manipulation
- **Target**: Dashboard / ECU
- **Vulnerability**: Lack of validation for temp signals
- **MITRE**: T1565
- **Impact**: Vehicle performance impacted
- **Tools**: CANBus Hack Kit
- **Scenario**: Attack shows fake overheat warning, forcing driver to stop
- **Attack Steps**: 1. Capture engine temperature CAN messages under normal operating conditions.2. Re-inject messages indicating extreme temperature (e.g., 120°C+).3. Dashboard shows overheating alert, possibly triggering emergency mode.4. Driver may pull over or limit engine power.
- **Detection**: Compare with OBD-II live telemetry
- **Solution**: Filter unrealistic temp values
- **Tags**: engine temp spoof, ECU fault

## Disabling Dashboard Warning Lights

- **Attack Type**: Display Manipulation
- **Target**: Instrument Cluster
- **Vulnerability**: Unverified alert state in dashboard
- **MITRE**: T1553
- **Impact**: Undetected mechanical issues
- **Tools**: Vector CANoe, spoofing script
- **Scenario**: Hide real warnings by disabling dashboard alert LEDs via CAN
- **Attack Steps**: 1. Reverse-engineer signals that trigger warning lights (e.g., check engine, airbag).2. Continuously inject a message that turns those lights off.3. Underlying faults (like misfiring engine or airbag failure) are hidden.4. Undermines driver trust and road safety.
- **Detection**: Compare with OBD-II DTC scan
- **Solution**: Isolate cluster display from critical DTCs
- **Tags**: airbag spoof, safety critical

## Hill Assist Spoofing on Incline

- **Attack Type**: Braking Spoofing
- **Target**: Braking Subsystem
- **Vulnerability**: Spoofable hill assist logic
- **MITRE**: T1491
- **Impact**: Driver confusion or minor accidents
- **Tools**: CAN injection, diagnostic tools
- **Scenario**: Adversary triggers hill assist unexpectedly on flat surface
- **Attack Steps**: 1. Identify the CAN message responsible for hill assist activation.2. Inject that message on flat ground or during low-speed turns.3. Brakes engage momentarily, driver may panic or lose control.4. Can also be used to disrupt parking maneuvers.
- **Detection**: Unusual hill assist activation logs
- **Solution**: Context-aware control verification
- **Tags**: hill hold spoof, brake trick

## Tampering with Cruise Control Speeds

- **Attack Type**: Acceleration Spoofing
- **Target**: Cruise Control Module
- **Vulnerability**: Unprotected setpoint injection
- **MITRE**: T1406
- **Impact**: Over-speeding or collisions
- **Tools**: CAN Interface, firmware toolkit
- **Scenario**: Attack increases or decreases cruise control speed silently
- **Attack Steps**: 1. Observe cruise control CAN frames while activating and setting speeds.2. Modify speed value mid-drive via injection (e.g., from 80 km/h to 120 km/h).3. The vehicle accelerates without user awareness.4. Can cause overspeeding tickets or safety risks.
- **Detection**: Speed sensor vs cruise setpoint comparison
- **Solution**: Secure ECU parameter changes
- **Tags**: cruise hijack, speed spoof

## Spoof Brake Commands via CAN Injection

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Insecure CAN message authentication
- **MITRE**: T869: CAN Bus Traffic Injection
- **Impact**: Safety hazard, vehicle crash risk
- **Tools**: SavvyCAN, CANtact, Wireshark
- **Scenario**: Attacker sends fake brake commands over CAN, causing unintended emergency braking.
- **Attack Steps**: 1. Identify the CAN ID responsible for brake actuation using tools like SavvyCAN.2. Capture legitimate brake signal frames by logging while braking.3. Reconstruct these frames and inject them via CANtact into the bus while the vehicle is in motion.4. Observe unintended sudden braking initiated by the ECU receiving spoofed signals.
- **Detection**: Monitor brake command frequency and timing
- **Solution**: Implement message authentication on CAN brake signals
- **Tags**: CAN Injection, Safety Override, Braking Spoof

## Acceleration Signal Injection

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of validation on accelerator inputs
- **MITRE**: T869: CAN Bus Traffic Injection
- **Impact**: May cause unintended speed increase
- **Tools**: CANBus Triple, SocketCAN
- **Scenario**: Fake accelerator signals are sent over CAN to make vehicle rev unexpectedly.
- **Attack Steps**: 1. Use SocketCAN to listen for acceleration signal messages while driving normally.2. Decode the payload format using DBC or trial and error.3. Craft spoofed acceleration frames and send them repeatedly.4. Vehicle will rev or accelerate unexpectedly even without pressing pedal, simulating throttle tampering.
- **Detection**: RPM and throttle telemetry cross-correlation
- **Solution**: ECU firmware updates with signal plausibility checks
- **Tags**: CAN Bus, Acceleration, Throttle Injection

## Gear Shift Override via CAN

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Insufficient validation of gear shift signals
- **MITRE**: T869: CAN Bus Traffic Injection
- **Impact**: Dangerous gear shift during motion
- **Tools**: BusMaster, ICSim
- **Scenario**: Attacker forces vehicle into Neutral or Reverse via gear spoofing on CAN.
- **Attack Steps**: 1. Record gear shift CAN messages when the driver manually changes gears.2. Inject known “Neutral” or “Reverse” gear messages while vehicle is moving.3. Transmission accepts spoofed input if no verification logic exists.4. Vehicle enters incorrect gear state, potentially causing mechanical damage or safety risk.
- **Detection**: Log and alert on gear change without driver input
- **Solution**: Add safety interlocks in TCU to reject unexpected shifts
- **Tags**: Gear Spoofing, Safety Violation, Transmission Control

## Cluster Warning Light Manipulation

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Unsecured instrument cluster communication
- **MITRE**: T869: CAN Bus Traffic Injection
- **Impact**: False alarms or ignored real alerts
- **Tools**: CANToolz, CANalyze
- **Scenario**: Spoof cluster warning lights to distract or mislead driver.
- **Attack Steps**: 1. Determine the CAN messages controlling the instrument cluster warning lights.2. Inject messages that trigger ABS, engine check, or airbag warnings.3. Monitor driver confusion or unnecessary servicing.4. Use this attack to distract from real issues or mask actual faults.
- **Detection**: Cross-verify warning state with diagnostic system
- **Solution**: Secure communication channel between ECUs and cluster
- **Tags**: Instrument Cluster, CAN Injection, Driver Distraction

## Spoofed Fuel Level Sensor

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of fuel level authentication
- **MITRE**: T869: CAN Bus Traffic Injection
- **Impact**: Mismanagement of fuel or unexpected stops
- **Tools**: Arduino + CAN shield
- **Scenario**: Mislead driver by faking fuel level to full or empty.
- **Attack Steps**: 1. Identify the CAN ID related to fuel level using sniffing during refueling.2. Inject packets showing a full tank while it's empty or vice versa.3. This may mislead fleet managers or drivers relying on fuel metrics.4. Can be used for gas theft masking or operational sabotage.
- **Detection**: Fuel telemetry discrepancy analysis
- **Solution**: Fuel sensor should report via authenticated sensors
- **Tags**: Fleet Sabotage, Fuel Spoofing, CAN-based Manipulation

## Spoofed RPM Display on Cluster

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: No signal validation from ECU
- **MITRE**: T869: CAN Bus Traffic Injection
- **Impact**: Engine abuse or delayed maintenance
- **Tools**: CANalyze, ICSim, SocketCAN
- **Scenario**: Show incorrect engine RPM to confuse or mislead driver.
- **Attack Steps**: 1. Analyze RPM-related CAN frames using ICSim and CAN logs.2. Send high-RPM messages even when the engine is idle.3. Cluster displays wrong RPM, leading to potential misjudgment.4. Attack may lead to missed maintenance schedules or reckless driving decisions.
- **Detection**: Compare OBD-II diagnostics with cluster readouts
- **Solution**: Display values should be derived directly from verified engine sensor data
- **Tags**: RPM Spoofing, Cluster Manipulation, Vehicle Safety

## Disable Gear Indicator Display

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of redundancy in display communication
- **MITRE**: T868: CAN Bus Message Blocking
- **Impact**: Safety risk in gear misinterpretation
- **Tools**: CANDevStudio
- **Scenario**: Hide current gear state on display to confuse driver or mechanic.
- **Attack Steps**: 1. Intercept and block messages showing gear state to cluster.2. Cluster remains blank or shows incorrect gear.3. Confusion may arise during critical operations like towing or parking.4. Could also be used to cover up unauthorized test drives or misuse.
- **Detection**: Monitor and alert on missing or delayed CAN gear state messages
- **Solution**: Redundant gear state from multiple ECUs
- **Tags**: Gear Display, Cluster Hiding, CAN Message Drop

## Sudden Steering Adjustment Injection

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: No torque plausibility checks
- **MITRE**: T869: CAN Bus Traffic Injection
- **Impact**: Driver instability or crash risk
- **Tools**: CANtact Pro, Scapy
- **Scenario**: Spoof signals to make EPS (Electric Power Steering) behave erratically.
- **Attack Steps**: 1. Identify EPS-related messages (usually on a separate high-speed CAN line).2. Craft subtle changes to steering torque inputs.3. Inject messages causing unexpected slight steering shifts.4. Attack could lead to driver mistrust or loss of vehicle control in critical moments.
- **Detection**: EPS ECU monitoring of expected input change rates
- **Solution**: Implement torque-based sanity checks and secure messaging
- **Tags**: EPS Attack, Steering Spoofing, CAN Physical Layer

## Tire Pressure Falsification via CAN

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: TPMS data spoofing or injection
- **MITRE**: T1595.002: Sensor Manipulation
- **Impact**: Distracts or delays vehicle usage
- **Tools**: TPMS simulator, CANTact
- **Scenario**: Send fake TPMS readings via CAN to cause warning or distraction.
- **Attack Steps**: 1. Simulate TPMS sensor broadcasts using RF or inject CAN-level data if routed there.2. Broadcast readings indicating a flat tire.3. Driver receives alerts and may stop unnecessarily.4. Attack may be used as part of a broader social engineering scenario.
- **Detection**: RF and CAN TPMS telemetry mismatch alerts
- **Solution**: Bind TPMS readings to encrypted and authenticated IDs
- **Tags**: TPMS, Sensor Spoofing, Distraction

## Falsified Check Engine Light (CEL)

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: No secure validation of warning signals
- **MITRE**: T869: CAN Bus Traffic Injection
- **Impact**: Driver confusion, unnecessary service
- **Tools**: CANalyse, SavvyCAN
- **Scenario**: Show fake engine fault to trick driver or technician.
- **Attack Steps**: 1. Determine the frame responsible for toggling CEL.2. Inject signal to trigger engine fault indicator.3. Can delay vehicle usage, fake diagnostic issues, or impact resale value.4. Can also be used as a psychological tactic in targeted harassment scenarios.
- **Detection**: Compare DTCs with physical signal conditions
- **Solution**: Ensure CEL is only activated via authenticated ECU-level faults
- **Tags**: Cluster Spoofing, CEL Attack, Vehicle Diagnostic Manipulation

## CAN-Based Brake Injection via Arduino

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of CAN authentication
- **MITRE**: T1609
- **Impact**: Vehicle stops unexpectedly; risk of crash
- **Tools**: Arduino, CAN-BUS Shield
- **Scenario**: Use Arduino with CAN shield to inject fake brake signals causing car to stop unexpectedly
- **Attack Steps**: 1. Connect Arduino to the OBD-II port using a CAN-BUS shield. 2. Capture normal CAN traffic to identify brake signal pattern. 3. Modify sketch to inject “brake applied” signals. 4. Replay these messages continuously while the vehicle is in motion. 5. Monitor vehicle reaction as it forcefully brakes despite driver input.
- **Detection**: Monitor abnormal brake command frequency via IDS
- **Solution**: Use secure CAN architecture with authentication tokens
- **Tags**: CAN Bus, Arduino, Safety, Braking

## Remote Gear Shift Override via CAN Flood

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Unauthenticated gear control over CAN
- **MITRE**: T1609
- **Impact**: May cause transmission damage or accidents
- **Tools**: CANalyzer, SocketCAN
- **Scenario**: Trick car into changing to reverse or neutral by spamming CAN with gear change messages
- **Attack Steps**: 1. Gain access to internal vehicle network. 2. Use CANalyzer or SocketCAN to flood network with spoofed gear-shift commands. 3. Override actual gear input by injecting more frequent spoofed messages. 4. Observe shift to undesired gear like reverse while driving forward. 5. Record DTCs or system logs to trace disruption source.
- **Detection**: Gear position mismatches in vehicle log
- **Solution**: Secure gearshift modules with ECU integrity checks
- **Tags**: Transmission, CAN, Flooding, Remote Injection

## Dashboard Warning Light Spoof

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of dashboard message validation
- **MITRE**: T1609
- **Impact**: Misleads driver and disrupts usage
- **Tools**: Scapy, CANoe
- **Scenario**: Inject fake “Check Engine” or ABS fault messages to mislead or scare drivers
- **Attack Steps**: 1. Connect to CAN network via diagnostic port. 2. Use Scapy to craft spoofed diagnostic trouble codes (DTCs). 3. Inject messages that simulate ABS or engine errors. 4. Observe dashboard displaying false warnings. 5. Log vehicle behavior and check if driver takes unnecessary action like stopping or towing the vehicle.
- **Detection**: Monitor for invalid diagnostic messages
- **Solution**: Authenticate dashboard communications
- **Tags**: Instrument Cluster, Spoofing, Dashboard

## Throttle Manipulation with Rogue ECU

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: ECU tampering, lack of firmware checks
- **MITRE**: T1609
- **Impact**: Causes dangerous unintended acceleration
- **Tools**: Custom ECU board
- **Scenario**: Replace legitimate ECU with a rogue one that sends unsafe throttle commands
- **Attack Steps**: 1. Remove legitimate throttle ECU in a lab or attack scenario. 2. Deploy custom ECU programmed to send out 100% throttle signal. 3. Connect to vehicle and test acceleration behavior. 4. Log data to prove command was issued by rogue ECU. 5. Monitor how vehicle responds (e.g., rapid uncommanded acceleration).
- **Detection**: Physical inspection or ECU fingerprint mismatch
- **Solution**: Secure ECU pairing with hardware-based auth
- **Tags**: ECU Swap, Acceleration, Tampering

## Speedometer Spoofing via CAN Messages

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: No authentication of speed signal
- **MITRE**: T1609
- **Impact**: May confuse driver or bypass speed-based limits
- **Tools**: CANtact, Python-CAN
- **Scenario**: Show false high or low speeds on instrument cluster
- **Attack Steps**: 1. Connect CANtact interface to OBD-II port. 2. Record speed signal CAN IDs while driving. 3. Write Python script to send fake speed data (e.g., 200 km/h while parked). 4. Inject messages periodically to override real values. 5. Confirm speedometer reflects false readings.
- **Detection**: Compare wheel sensor data vs cluster reading
- **Solution**: Use secure instrumentation protocols
- **Tags**: Cluster Spoofing, Speed Injection, CAN

## Cluster Tampering: Fuel & Temp Misreport

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Diagnostic access not restricted
- **MITRE**: T1609
- **Impact**: Leads to driver inaction on real problems
- **Tools**: UDS Tool, CANoe
- **Scenario**: Modify fuel gauge and temperature readings to mislead driver
- **Attack Steps**: 1. Connect to the diagnostic interface and initiate UDS session. 2. Use diagnostic service 0x2E to write false data to memory locations controlling fuel and temperature. 3. Refresh cluster values to reflect false readings (e.g., full tank when empty). 4. Observe driver confusion or failure to refuel.
- **Detection**: Correlate cluster and sensor values via telemetry
- **Solution**: Restrict write access via diagnostic gateway
- **Tags**: UDS, False Display, Fuel, Temp

## Hill Assist Spoof for Rolling Attack

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: No validation of hill status signal
- **MITRE**: T1609
- **Impact**: Vehicle rollback on slopes
- **Tools**: CANable, Python
- **Scenario**: Fake uphill condition to disable hill-hold assist, causing rollback on slope
- **Attack Steps**: 1. Capture CAN signals related to incline detection and brake hold via CANable. 2. Replay signals simulating flat ground. 3. Hill assist doesn't engage due to spoofed input. 4. Car rolls backward unintentionally. 5. Confirm via driver reaction and event log.
- **Detection**: Check real-time slope sensor vs message data
- **Solution**: Sensor validation and input redundancy
- **Tags**: Hill Hold, Safety, CAN Spoofing

## Uncommanded Downshift Exploit

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of input arbitration in ECU
- **MITRE**: T1609
- **Impact**: Causes drivetrain stress or engine damage
- **Tools**: Vector Toolset, CAN-ID Map
- **Scenario**: Force a sudden downshift in automatic transmission via CAN injections
- **Attack Steps**: 1. Identify CAN ID controlling transmission logic via reverse engineering. 2. Use Vector tools to inject downshift message while at high speed. 3. Monitor RPM spike and engine braking. 4. Confirm that driver's input did not cause shift. 5. Evaluate stress on drivetrain components.
- **Detection**: Analyze shift logs vs CAN injections
- **Solution**: Validate gear shift only on physical lever input
- **Tags**: Transmission, CAN Injection, Downshift

## Ignoring Brake Pedal: Sensor Override

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Sensor spoofing vulnerability
- **MITRE**: T1609
- **Impact**: Brake pedal input ignored in critical moment
- **Tools**: CANSniffer, Arduino
- **Scenario**: Suppress brake pedal input by spoofing zero-pressure messages
- **Attack Steps**: 1. Capture real brake pedal pressure signals using CANSniffer. 2. Replay spoofed zero-pressure values frequently to override real pedal input. 3. During emergency braking, system may not register driver pressing brake. 4. Observe delay or failure in deceleration. 5. Log for forensic analysis.
- **Detection**: Compare driver input sensor vs CAN values
- **Solution**: Secure sensor-to-ECU communication
- **Tags**: Brake Sensor Spoof, Safety

## Eco Mode Lock-in via CAN Control

- **Attack Type**: Vehicle Control Manipulation
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of control mode authentication
- **MITRE**: T1609
- **Impact**: Affects drivability and performance
- **Tools**: CANutils, Linux
- **Scenario**: Force vehicle to stay in low-power “Eco” mode, limiting performance
- **Attack Steps**: 1. Connect to CAN bus with CANutils on Linux. 2. Send message to activate “Eco Mode” continuously. 3. Override attempts to switch mode using dashboard controls. 4. Vehicle becomes underpowered in traffic scenarios. 5. Driver loses control over mode switching.
- **Detection**: Monitor repeated Eco mode toggles
- **Solution**: Mode switch control logic hardening
- **Tags**: CAN Override, Eco Mode, Drive Limiting

## Real-Time CAN Bus Monitoring Using CANShield

- **Attack Type**: Defensive Monitoring
- **Target**: Vehicle CAN Bus
- **Vulnerability**: Lack of anomaly detection on CAN
- **MITRE**: T0829
- **Impact**: Early detection of CAN-based attacks
- **Tools**: CANShield, SocketCAN
- **Scenario**: Use CANShield to monitor in-vehicle CAN traffic for anomalies like replay or spoofed messages.
- **Attack Steps**: 1. Deploy the CANShield hardware between the vehicle’s OBD-II port and diagnostic tool. 2. Enable logging of incoming and outgoing CAN frames. 3. Train the device with baseline traffic patterns during normal vehicle operation. 4. Once trained, put the device into “active monitoring” mode. 5. Simulate an attack such as replaying a diagnostic frame. 6. Observe the alert triggered by unexpected timing or invalid message structure. 7. Log and export alert details to the central SIEM or dashboard.
- **Detection**: Real-time anomaly alerts
- **Solution**: Continuous CAN IDS
- **Tags**: can, ids, canShield, anomaly-detection, realtime

## OTA Firmware Checksum Verification Routine

- **Attack Type**: Firmware Integrity
- **Target**: Telematics/IVI System
- **Vulnerability**: Missing firmware verification
- **MITRE**: T1601
- **Impact**: Prevent firmware tampering
- **Tools**: Python (hashlib), OTA Framework
- **Scenario**: Implement checksum or hash checks for verifying OTA firmware integrity before installation.
- **Attack Steps**: 1. Modify the OTA firmware update system to include a SHA-256 hash for each firmware release. 2. Embed the expected hash into the update manifest file. 3. Before allowing installation, compute the hash of the received firmware image. 4. Compare it to the expected hash in the manifest. 5. If mismatched, log the event, alert the vehicle system, and reject the update. 6. Perform logging for future forensic review and alert fleet management system.
- **Detection**: Hash mismatch detection
- **Solution**: Sign-and-verify all firmware
- **Tags**: fota, integrity-check, hash, sha256, update-security

## Detect Invalid ECU ID Spoofing with Frame Whitelist

- **Attack Type**: CAN IDS
- **Target**: ECU over CAN
- **Vulnerability**: Lack of ID enforcement
- **MITRE**: T0838
- **Impact**: Detect rogue ECU messages
- **Tools**: CANalyzer, ECU ID maps
- **Scenario**: Define and enforce a list of valid ECU IDs per vehicle model to block or log unknown messages.
- **Attack Steps**: 1. Collect known good CAN IDs from vehicle manufacturer or during clean captures. 2. Configure a monitoring tool like CANalyzer or custom script to whitelist those IDs. 3. Monitor the bus in real-time for any unexpected or unknown CAN IDs. 4. When an unrecognized ID appears, raise an alert with timestamp and payload. 5. Cross-reference the unknown ID with known attacks or rogue ECUs. 6. Optionally block communication from untrusted sources using hardware filters.
- **Detection**: Unknown ID detection
- **Solution**: Implement strict ECU ID whitelisting
- **Tags**: ecu, spoof-detection, whitelist, can-id, anomaly

## Fleet-Wide SIEM Alerts for Brake Spoofing Patterns

- **Attack Type**: Fleet Defense
- **Target**: Vehicle Fleets
- **Vulnerability**: No behavioral correlation across units
- **MITRE**: T0889
- **Impact**: Detect spoofed control frames
- **Tools**: Splunk, KQL, CAN Parsers
- **Scenario**: Correlate data from multiple vehicles to detect brake input spoofing anomalies.
- **Attack Steps**: 1. Stream CAN data from each vehicle to a central SIEM platform. 2. Normalize brake input and speed data using a KQL or custom parser. 3. Set detection rule for condition: “brake input = 100% but speed doesn't decrease.” 4. Apply this rule across logs from all vehicles to find suspicious patterns. 5. If repeated or observed in unusual location/time, escalate the alert. 6. Visualize the event chain for analysts and trigger incident response.
- **Detection**: Behavioral SIEM alert
- **Solution**: Behavioral fleet-wide rules
- **Tags**: siem, splunk, brake-anomaly, fleet-monitoring, rules

## Validate Firmware Boot Hash via TPM on Startup

- **Attack Type**: Firmware Integrity
- **Target**: IVI or Telematics
- **Vulnerability**: No trusted boot mechanism
- **MITRE**: T1542.003
- **Impact**: Firmware tampering prevention
- **Tools**: TPM 2.0, UEFI Boot
- **Scenario**: Use Trusted Platform Module (TPM) to verify the integrity of loaded firmware at boot time.
- **Attack Steps**: 1. Integrate TPM with the vehicle's bootloader and firmware storage. 2. On firmware write, store a signed hash of the firmware inside the TPM. 3. Modify the bootloader to rehash firmware at each boot and compare with TPM-stored value. 4. If hash matches, continue boot; if not, halt boot and trigger tamper alert. 5. Log failed hash verifications and alert security dashboard. 6. Periodically rotate and re-sign firmware on update cycles.
- **Detection**: Boot-time hash mismatch
- **Solution**: Secure boot + TPM
- **Tags**: firmware-check, tpm, trusted-boot, integrity, secureboot

## Detect Gear Shift Spoof Attempts with Logical Model

- **Attack Type**: Behavior Monitoring
- **Target**: Vehicle Transmission
- **Vulnerability**: Unsafe state change detection missing
- **MITRE**: T0851
- **Impact**: Prevent unsafe gear spoofing
- **Tools**: MATLAB Simulink, Python Models
- **Scenario**: Use a logic model to detect gear shifts that contradict speed or brake conditions.
- **Attack Steps**: 1. Build a logic model that correlates gear shift inputs, vehicle speed, and brake status. 2. For example, shifting into “Reverse” should only happen below 5 km/h with full brake. 3. Stream live telemetry into the model during driving. 4. Detect any anomalies such as reverse gear engagement at highway speeds. 5. Raise alerts, log incident, and notify central SOC or fleet dashboard. 6. Confirm false positives using historic data.
- **Detection**: Gear-speed mismatch
- **Solution**: Behavioral logic-based IDS
- **Tags**: gear, spoofing, model-check, anomaly, transmission

## Detection of Jamming Attacks on Key Fob Signals

- **Attack Type**: Wireless Defense
- **Target**: Key Fob Receiver
- **Vulnerability**: Lack of RF anomaly detection
- **MITRE**: T1420
- **Impact**: Detect unlock jamming
- **Tools**: SDR, GNU Radio, RF Analyzer
- **Scenario**: Identify possible RF jamming used to block key fob signals during theft attempts.
- **Attack Steps**: 1. Deploy an SDR-based monitor in the vehicle capable of logging RF spectrum around 315/433/868 MHz. 2. Create a baseline RF profile when the vehicle is idle. 3. Monitor for unusually strong, sustained transmissions in key fob bands. 4. If consistent high signal blocks normal unlock attempts, raise alert. 5. Log the time, signal strength, and duration. 6. Alert the vehicle security system and save logs for investigation.
- **Detection**: RF signal pattern match
- **Solution**: RF IDS or fob jamming alert
- **Tags**: rf-jam, fob, unlock-theft, wireless-ids, sdr

## Telematics Threat Hunting with NetFlow Baselines

- **Attack Type**: Fleet Monitoring
- **Target**: Telematics Modules
- **Vulnerability**: Blind to network-layer anomalies
- **MITRE**: T1040
- **Impact**: Detect malicious cloud commands
- **Tools**: NetFlow, Wireshark, Zeek
- **Scenario**: Use NetFlow data to detect unexpected comms from vehicle telematics modules.
- **Attack Steps**: 1. Capture NetFlow logs from all vehicle telematics modules over time. 2. Establish a baseline of regular connections (e.g., to OEM servers). 3. Look for new external IPs, high data volumes, or odd timings. 4. Flag anomalies such as comms with unknown IPs or command/control domains. 5. Correlate with time of use and vehicle state (e.g., parked vs active). 6. Trigger alerts and begin forensic triage if suspicious flow is observed.
- **Detection**: Flow-based anomaly
- **Solution**: NetFlow baseline + alerts
- **Tags**: netflow, telematics, threat-hunting, network-visibility

## Detect Fake Warning Light Injection on Instrument Cluster

- **Attack Type**: Instrument Cluster Monitoring
- **Target**: Instrument Cluster
- **Vulnerability**: CAN spoofing of dash signals
- **MITRE**: T0810
- **Impact**: Driver deception via UI
- **Tools**: CAN Loggers, Cluster Decoder
- **Scenario**: Identify false warning lights injected via CAN by rogue ECUs or attackers.
- **Attack Steps**: 1. Capture CAN traffic during known-good states (no engine warning, no brake light, etc.). 2. Log the exact IDs and payloads that control dashboard indicators. 3. Create detection logic to flag sudden warning light messages when engine state is normal. 4. If, for example, a brake light comes on with no physical brake applied, alert the driver. 5. Log the rogue message ID and source timestamp. 6. Investigate further for spoofing attempts.
- **Detection**: False indicator trigger detection
- **Solution**: Decode & filter fake CAN messages
- **Tags**: cluster, warning-light, dash-spoof, deception, ui-fraud

## Correlate Acceleration Data with CAN Inputs for Spoofing

- **Attack Type**: Sensor Fusion Defense
- **Target**: Powertrain / CAN
- **Vulnerability**: Data spoofing without validation
- **MITRE**: T0850
- **Impact**: Detect fake throttle/brake inputs
- **Tools**: IMU Sensor, CAN Sniffer
- **Scenario**: Use IMU (accelerometer) data to validate if CAN acceleration frames are legitimate.
- **Attack Steps**: 1. Equip the vehicle with an IMU to measure physical acceleration. 2. Ingest CAN messages showing throttle or acceleration frames. 3. Compare the acceleration reported over CAN with actual IMU readings. 4. If CAN shows hard acceleration but IMU does not match, raise a spoofing alert. 5. Record and timestamp discrepancies. 6. Alert driver and flag event for SOC review.
- **Detection**: CAN vs IMU mismatch
- **Solution**: Cross-sensor validation
- **Tags**: imu, acceleration, spoofing-detection, sensor-fusion

