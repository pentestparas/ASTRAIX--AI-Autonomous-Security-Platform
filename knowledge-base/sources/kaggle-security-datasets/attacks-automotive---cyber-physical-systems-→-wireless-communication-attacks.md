# Automotive / Cyber-Physical Systems → Wireless Communication Attacks Attacks

## V2X Message Replay to Trigger Emergency Braking

- **Attack Type**: Message Replay
- **Target**: V2X-enabled vehicle
- **Vulnerability**: Lack of message authentication and freshness checks in V2X
- **MITRE**: T1071.001
- **Impact**: Induce unnecessary emergency maneuvers
- **Tools**: USRP, GNURadio, Wireshark
- **Scenario**: An attacker replays legitimate V2X packets to make a vehicle believe there is a collision threat, causing false braking.
- **Attack Steps**: 1. Use a software-defined radio (e.g., USRP) with GNURadio to capture V2X messages from a moving vehicle at an intersection.2. Identify DENM (Decentralized Environmental Notification Messages) or CAM (Cooperative Awareness Messages) packets signaling a high-risk event.3. At a later time, rebroadcast the same packet sequence at a spoofed location.4. The victim vehicle receives the spoofed messages and assumes there is an obstacle or emergency, initiating automated braking.5. Observe the behavior or log messages from the vehicle’s ADAS.
- **Detection**: V2X message integrity check, anomaly logs
- **Solution**: Use certificate-based signing and sequence validation in V2X stack
- **Tags**: V2X, SDR, Replay Attack, Safety

## Bluetooth L2CAP Exploitation on IVI

- **Attack Type**: Bluetooth Protocol Exploit
- **Target**: Infotainment System
- **Vulnerability**: Vulnerable Bluetooth stack (L2CAP)
- **MITRE**: T1210
- **Impact**: Remote crash or RCE in IVI system
- **Tools**: btstack, gatttool, BlueZ
- **Scenario**: Exploiting unpatched vulnerabilities in the L2CAP layer of a car’s Bluetooth stack to crash or inject code into infotainment system.
- **Attack Steps**: 1. Scan for nearby Bluetooth-enabled infotainment units using hcitool scan.2. Identify open ports and services using sdptool.3. Send malformed L2CAP packets targeting known CVEs (e.g., CVE-2017-0781) using a fuzzing script or crafted pcap.4. Monitor infotainment screen for reboots, freezes, or arbitrary behavior.5. If successful, exploit can be escalated to execute commands within IVI OS.
- **Detection**: Bluetooth logs, crash dumps, kernel panic
- **Solution**: Patch BT stack, disable classic BT if unused
- **Tags**: Bluetooth, IVI, L2CAP, CVE

## Rogue 5G Tower for Telematics Hijack

- **Attack Type**: IMSI Catcher / Rogue Cell
- **Target**: Telematics Unit
- **Vulnerability**: Lack of network binding or encryption
- **MITRE**: T1583.003
- **Impact**: Full takeover of remote commands
- **Tools**: srsRAN, Amarisoft, USRP
- **Scenario**: Attacker sets up a rogue 5G cell to force nearby vehicle to connect and intercept telematics commands.
- **Attack Steps**: 1. Set up a rogue gNodeB using srsRAN or Amarisoft configured to mimic a trusted carrier PLMN.2. Transmit with higher power so vehicle connects to it instead of real cell tower.3. Intercept or inject telematics traffic going to backend APIs, especially SIM-based MQTT or HTTPS traffic.4. If unencrypted, attacker can send fake commands (e.g., unlock car, start engine).5. Log vehicle's IMSI, session ID, and payloads for further exploitation.
- **Detection**: Baseband logging, abnormal carrier lock
- **Solution**: Use end-to-end encryption and carrier pinning
- **Tags**: Rogue Tower, 5G, IMSI Catcher

## BLE MitM on Mobile-App Pairing

- **Attack Type**: BLE Interception
- **Target**: Bluetooth Low Energy Pairing
- **Vulnerability**: Unauthenticated BLE pairing
- **MITRE**: T1557.002
- **Impact**: Unauthorized control or data access
- **Tools**: btproxy, gattacker, Ubertooth
- **Scenario**: Attacker performs a man-in-the-middle on BLE pairing between smartphone and vehicle to capture or alter commands.
- **Attack Steps**: 1. Position attacker between smartphone and vehicle during BLE pairing process.2. Use btproxy or gattacker to intercept and relay BLE packets.3. Capture characteristics like unlock or start engine and modify responses.4. Relay malicious commands while faking legitimate connection to both ends.5. Monitor packet flow to ensure vehicle accepts spoofed data.
- **Detection**: BLE connection logs, unexpected pairing attempts
- **Solution**: Enforce BLE bonding, whitelist MACs
- **Tags**: BLE, MitM, Ubertooth

## DSRC Beacon Injection for Traffic Congestion

- **Attack Type**: Protocol Abuse
- **Target**: Autonomous Navigation Stack
- **Vulnerability**: No filtering or validation of message origin
- **MITRE**: T1557
- **Impact**: Navigation delays or unsafe reroutes
- **Tools**: GNURadio, DSRC Stack Sim
- **Scenario**: Attackers spam false congestion or traffic hazard beacons to misguide autonomous driving decisions.
- **Attack Steps**: 1. Configure GNURadio to simulate DSRC messages on 5.9GHz.2. Craft CAM messages that report slow-moving or stopped vehicles at specific GPS coordinates.3. Send multiple beacons from spoofed MACs to simulate traffic density.4. Target navigation modules to force alternate routing or delays.5. Monitor reaction of autonomous driving system or navigation reroutes.
- **Detection**: V2X map overlays, logging unusual beacons
- **Solution**: DSRC authentication & origin validation
- **Tags**: DSRC, Beacon Flood, GNURadio

## Telematics Backend Fuzzing

- **Attack Type**: API Fuzzing
- **Target**: Telematics Backend
- **Vulnerability**: Poor input validation in cloud APIs
- **MITRE**: T1190
- **Impact**: Unauthorized backend access
- **Tools**: Postman, Burp Suite, ffuf
- **Scenario**: Discovering vulnerabilities in cloud APIs linked to car via LTE by fuzzing their inputs.
- **Attack Steps**: 1. Analyze mobile app traffic using a proxy (Burp Suite) to enumerate backend APIs.2. Identify endpoints controlling start, lock/unlock, vehicle location, etc.3. Use ffuf or custom fuzzers to send malformed data, long parameters, or missing headers.4. Check responses for status codes, information leakage, or unintended behavior.5. Attempt to escalate to command injection or bypass checks (e.g., vehicle VIN auth).
- **Detection**: WAF logs, backend API monitoring
- **Solution**: Rate limiting, parameter sanitization
- **Tags**: Telematics, API Security

## Bluetooth Stack Null Pointer Dereference

- **Attack Type**: DoS via Null Dereference
- **Target**: IVI Bluetooth Daemon
- **Vulnerability**: Vulnerable SDP handler
- **MITRE**: T1499.004
- **Impact**: Denial of service to user
- **Tools**: CVE PoC, btcrash
- **Scenario**: Crashing the Bluetooth process in IVI by triggering a known null pointer dereference in classic Bluetooth stack.
- **Attack Steps**: 1. Find target IVI system using Bluetooth discovery.2. Send malformed SDP (Service Discovery Protocol) packets triggering CVE-2021-20090.3. Observe IVI system crash or reboot due to unhandled null dereference.4. Loop the packet every few seconds to cause persistent DoS.5. Optional: monitor system log dumps via UART/debug cable.
- **Detection**: Crash logs, kernel panic analysis
- **Solution**: Patch Bluetooth stack, filter malformed packets
- **Tags**: DoS, Bluetooth, CVE

## LTE SIM Swap Attack on Vehicle

- **Attack Type**: SIM Swap
- **Target**: Telematics SIM
- **Vulnerability**: Social engineering + identity theft
- **MITRE**: T1586
- **Impact**: Remote access takeover
- **Tools**: Social Engineering, Telco Tools
- **Scenario**: Attacker fraudulently ports telematics SIM to gain control of backend-connected vehicle.
- **Attack Steps**: 1. Gather personal information of vehicle owner (via phishing, leaks).2. Call the mobile provider impersonating the user and request a SIM replacement.3. Gain control of the telematics SIM and receive all traffic.4. Use it to authenticate to cloud APIs and control vehicle remotely.5. Monitor mobile app to confirm command execution works on hijacked SIM.
- **Detection**: SIM provisioning logs, user report
- **Solution**: Use multi-factor SIM protection
- **Tags**: SIM Swap, Telematics, LTE

## BLE Buffer Overflow in IVI Pairing

- **Attack Type**: Memory Corruption
- **Target**: IVI Bluetooth Stack
- **Vulnerability**: No bounds checking in BLE stack
- **MITRE**: T1203
- **Impact**: Arbitrary code execution
- **Tools**: BLEFuzz, Gattacker
- **Scenario**: Exploiting buffer overflows in BLE stack of IVI system to execute arbitrary code.
- **Attack Steps**: 1. Use BLEFuzz to send oversized GATT responses during IVI pairing handshake.2. Monitor BLE response parsing in IVI logs.3. Crash or gain code execution if IVI firmware does not perform length validation.4. Escalate to OS-level access if attack lands in privileged stack.5. Extract memory dumps if possible to verify code execution.
- **Detection**: Crash dumps, firmware integrity alerts
- **Solution**: Harden BLE stack, use watchdog
- **Tags**: BLE, Overflow, IVI Exploit

## LTE Jamming for Telematics Blindness

- **Attack Type**: Wireless Jamming
- **Target**: Telematics Unit
- **Vulnerability**: No fallback comms channel
- **MITRE**: T1602
- **Impact**: Loss of remote tracking/control
- **Tools**: HackRF, LTEjam, BladeRF
- **Scenario**: Jam LTE signals around vehicle to blind it from backend and disable remote tracking.
- **Attack Steps**: 1. Set up HackRF with LTEjam tool tuned to carrier frequency of vehicle's SIM.2. Begin transmitting high power noise bursts on LTE band (e.g., Band 3, Band 7).3. Observe vehicle app shows it as offline or unreachable.4. Confirm vehicle can’t receive remote commands (e.g., via mobile app).5. Maintain jammer range for as long as needed.
- **Detection**: Signal loss alerts, SIM status logs
- **Solution**: Use multiband fallback, RF anomaly detection
- **Tags**: LTE, Jamming, HackRF

## Intercept DSRC V2V Messages with SDR

- **Attack Type**: Communication Interception
- **Target**: Vehicle DSRC Module
- **Vulnerability**: Lack of Encryption / Auth in DSRC
- **MITRE**: T1430
- **Impact**: Privacy Violation, Target Tracking
- **Tools**: GNU Radio, HackRF, DSRC stack, Wireshark
- **Scenario**: Exploit Dedicated Short Range Communication (DSRC) channels between vehicles to sniff location and telemetry data.
- **Attack Steps**: 1. Begin by studying the DSRC protocol (IEEE 802.11p) to understand how V2V messages are formatted and broadcast.2. Set up a software-defined radio like HackRF or USRP with a compatible antenna tuned to the DSRC frequency (5.9 GHz band).3. Use GNU Radio to demodulate the DSRC signals and capture raw packet streams.4. Integrate DSRC decoding modules or plugins into Wireshark to interpret vehicle broadcast messages (e.g., Basic Safety Messages - BSMs).5. Analyze captured data to reveal vehicle location, speed, and direction in near-real time.
- **Detection**: Monitor RF spectrum activity, analyze signal strength anomalies
- **Solution**: Encrypt or authenticate DSRC messages; limit broadcast range
- **Tags**: wireless, DSRC, SDR, privacy, sniffing

## Replay Injected DSRC Alerts

- **Attack Type**: Communication Injection
- **Target**: V2V Communication Stack
- **Vulnerability**: No verification of DSRC message origin
- **MITRE**: T1200
- **Impact**: False safety alerts, driver confusion
- **Tools**: HackRF, GNU Radio, DSRC packet replayer
- **Scenario**: Inject false road hazard alerts (e.g., icy road, emergency vehicle nearby) via spoofed DSRC broadcasts.
- **Attack Steps**: 1. Capture real DSRC messages using HackRF and record the I/Q samples for later reuse.2. Analyze message structure using Wireshark or DSRC protocol parsers to identify alert types (like Event Hazard Warnings).3. Modify the contents of the replayed packet to simulate a different hazard or location.4. Re-transmit the altered message using the HackRF in transmit mode.5. Observe affected vehicles’ responses—infotainment alerts, braking events, or route changes.
- **Detection**: Signal triangulation, BSM validity checks
- **Solution**: Require certificate-based validation for V2X messages
- **Tags**: dsrc, replay attack, v2v spoofing, alerts

## Exploit Cloud Telematics Endpoint via API Abuse

- **Attack Type**: Telematics API Abuse
- **Target**: Telematics Cloud API
- **Vulnerability**: Insecure API Auth / Logic Flaws
- **MITRE**: T1110.003
- **Impact**: Remote takeover, stalking, theft
- **Tools**: Postman, Burp Suite, Cloud API docs
- **Scenario**: Abusing cloud backend APIs to remotely control vehicle features like door lock or engine start.
- **Attack Steps**: 1. Register an official companion app for the target vehicle make and model.2. Intercept traffic between the app and backend using a proxy (e.g., Burp Suite) to identify REST endpoints.3. Test the endpoints for missing or broken authentication mechanisms.4. Attempt to reuse session tokens, spoof VIN numbers, or change user-agent headers.5. Invoke sensitive functions like /remote-start, /lock, /vehicle-status on another vehicle via crafted API requests.
- **Detection**: Monitor backend logs, rate limits, IP flags
- **Solution**: Harden auth logic, enforce strict VIN binding
- **Tags**: telematics, API, cloud, remote control

## Bluetooth DoS via L2CAP Flooding

- **Attack Type**: Wireless DoS
- **Target**: IVI Bluetooth Stack
- **Vulnerability**: Lack of Flood Protection
- **MITRE**: T1499
- **Impact**: Service interruption
- **Tools**: btstack, hcitool, l2ping
- **Scenario**: Overwhelm the in-vehicle infotainment system’s Bluetooth stack by sending L2CAP packets at high rate.
- **Attack Steps**: 1. Use hcitool or l2ping to discover nearby Bluetooth devices broadcasting the IVI’s MAC address.2. Connect to the IVI’s Bluetooth stack using a Bluetooth adapter on a Linux system.3. Use a custom tool or l2ping in rapid-fire mode to send a flood of L2CAP echo requests.4. Monitor IVI system for lag, crash, or Bluetooth disconnection.5. Modify packet size and rate to evade basic rate-limiting defenses.
- **Detection**: Monitor Bluetooth logs for rapid L2CAP traffic
- **Solution**: Rate-limit, buffer control, firmware patches
- **Tags**: bluetooth, IVI, flooding, DoS

## Exploit Bluetooth Audio Stack Buffer Overflow

- **Attack Type**: Stack Exploitation
- **Target**: IVI Bluetooth Stack
- **Vulnerability**: Improper bounds checking in audio codec
- **MITRE**: T1203
- **Impact**: Crash, possible RCE
- **Tools**: BlueZ, GDB, Audio Fuzzer
- **Scenario**: Trigger buffer overflow in the audio processing stack of the infotainment unit over Bluetooth.
- **Attack Steps**: 1. Research infotainment system specs and OS (Linux, QNX, Android Auto).2. Analyze the Bluetooth audio streaming protocol stack used (e.g., A2DP, SBC decoding).3. Use fuzzing frameworks to generate malformed audio metadata (e.g., very long SBC header fields).4. Pair with the target IVI over Bluetooth and send the crafted audio payload.5. If overflow succeeds, attach debugger to observe crash and memory corruption.6. Validate potential for remote code execution.
- **Detection**: Monitor system logs, abnormal memory usage
- **Solution**: Patch decoder libraries, fuzz test all input
- **Tags**: bluetooth, IVI, fuzzing, overflow, RCE

## Bluetooth Pairing Attack via Forced PIN Reuse

- **Attack Type**: Authentication Bypass
- **Target**: IVI Bluetooth Stack
- **Vulnerability**: Weak or fixed pairing codes
- **MITRE**: T1110.001
- **Impact**: Media control, privacy risk
- **Tools**: Ubertooth, Bluetooth Sniffer, Blue Hydra
- **Scenario**: Force IVI systems to re-pair with known PINs or reuse previously paired credentials.
- **Attack Steps**: 1. Use Bluetooth sniffing tools (e.g., Ubertooth) to detect and capture pairing attempts.2. Identify reused or hardcoded PINs for legacy pairing modes (0000, 1234).3. Trigger device unpair and re-pair sequences on IVI through repeated connection requests.4. Exploit fallback pairing modes where manual confirmation is bypassed.5. Upon success, gain unauthorized Bluetooth access to stream audio or issue media commands.
- **Detection**: Monitor for frequent pairing events
- **Solution**: Use secure pairing (LE Secure Connections)
- **Tags**: bluetooth, pairing, weak auth

## LTE Telematics SIM Hijack

- **Attack Type**: SIM Cloning / Identity Hijack
- **Target**: Telematics Control Unit
- **Vulnerability**: Physical SIM access, lack of binding
- **MITRE**: T1141
- **Impact**: Backend spoofing, tracking
- **Tools**: SIM Cloner, Card Reader, USB UART
- **Scenario**: Clone or swap SIM inside telematics unit to reroute traffic or impersonate vehicle.
- **Attack Steps**: 1. Locate the telematics control unit (TCU) and access the embedded SIM (eSIM) or removable SIM.2. If removable, extract SIM card and use a SIM reader to dump IMSI and Ki (authentication key).3. Clone this data onto a programmable SIM using cloning hardware.4. Insert cloned SIM into a separate GSM modem and attempt to authenticate to vehicle backend.5. Monitor for successful API responses or SIM ban events.
- **Detection**: Monitor SIM changes and usage anomalies
- **Solution**: Bind SIM to vehicle ECU ID and secure TCU
- **Tags**: SIM clone, GSM, backend abuse

## Inject V2X Warnings with SDR

- **Attack Type**: Spoofed Broadcast
- **Target**: V2X Stack
- **Vulnerability**: Lack of origin validation
- **MITRE**: T1557.002
- **Impact**: Traffic disruption, driver panic
- **Tools**: HackRF, OpenV2X, SDRplay
- **Scenario**: Broadcast false emergency or infrastructure warnings to trigger braking or driver panic.
- **Attack Steps**: 1. Record legitimate V2X messages from nearby RSUs (roadside units) or OBUs.2. Modify message fields to simulate wrong-way vehicle, pedestrian alert, or speed zone changes.3. Broadcast the spoofed messages over 5.9 GHz using an SDR.4. Vehicles nearby may respond based on ADAS logic: braking, alerting, or re-routing.5. Capture responses on camera or diagnostics bus.
- **Detection**: Deploy V2X certificate validation
- **Solution**: digital signatures, alert thresholding
- **Tags**: v2x, spoofing, safety alerts

## Exploit BLE GATT Service on IVI App

- **Attack Type**: GATT Misconfiguration Exploit
- **Target**: BLE Interface on Mobile App
- **Vulnerability**: Unprotected writeable BLE characteristics
- **MITRE**: T1516
- **Impact**: IVI manipulation
- **Tools**: nRF Connect, BLEah, Android
- **Scenario**: Abuse poorly secured BLE service exposed by a companion IVI mobile app.
- **Attack Steps**: 1. Identify BLE device and enumerate available GATT services using nRF Connect or similar tools.2. Target writable characteristics that control system parameters or playback.3. Attempt to write arbitrary values (e.g., switch media source, change volume).4. If authentication isn’t required, commands are accepted instantly.5. Explore hidden services undocumented by manufacturer for deeper access.
- **Detection**: BLE traffic inspection and logging
- **Solution**: Enforce pairing, whitelist GATT UUIDs
- **Tags**: BLE, GATT, Android Auto

## Bluetooth Stack Info Leak via SDP Abuse

- **Attack Type**: Reconnaissance
- **Target**: IVI Bluetooth Stack
- **Vulnerability**: Excessively exposed service details
- **MITRE**: T1592
- **Impact**: Information leakage
- **Tools**: sdptool, hcitool, BlueZ
- **Scenario**: Abuse Service Discovery Protocol (SDP) to query detailed IVI capabilities remotely.
- **Attack Steps**: 1. Use hcitool to scan for the IVI's Bluetooth address.2. Invoke sdptool browse [BT_ADDR] to dump available services.3. Extract UUIDs, channel mappings, and firmware fingerprints.4. Correlate known vulnerable services with CVE databases.5. Use this data to craft targeted attacks like media control or fuzzing payloads.
- **Detection**: Restrict SDP access, log scans
- **Solution**: Limit SDP response, apply ACLs
- **Tags**: SDP, BTInfoLeak, fingerprinting

## DSRC Injection via SDR

- **Attack Type**: Data Injection
- **Target**: V2V-capable Vehicles
- **Vulnerability**: Lack of DSRC message validation
- **MITRE**: T0846
- **Impact**: False collision alerts, sudden braking
- **Tools**: GNURadio, HackRF, DSRC Decoders
- **Scenario**: Inject false V2V alerts into the DSRC channel using Software Defined Radio to trigger unnecessary braking in nearby vehicles.
- **Attack Steps**: 1. Set up a HackRF SDR device with GNURadio. 2. Record legitimate DSRC packets between two V2V-enabled vehicles. 3. Modify message contents (e.g., inject false collision alerts). 4. Re-transmit the crafted packets on the DSRC frequency. 5. Observe if nearby vehicles respond (brake, alert driver). 6. Repeat with different fake scenarios (e.g., wrong intersection warning). 7. Document safety-critical misbehavior due to spoofed alerts.
- **Detection**: V2X logging, anomaly correlation
- **Solution**: Secure DSRC stack with cryptographic message validation
- **Tags**: DSRC, GNURadio, V2X

## Reverse Engineering V2X Stack

- **Attack Type**: Reverse Engineering
- **Target**: V2X Modules
- **Vulnerability**: Poor input validation in message parser
- **MITRE**: T1609.001
- **Impact**: V2X service crash or remote code execution
- **Tools**: Binwalk, Ghidra, QEMU
- **Scenario**: Dissect the firmware of the V2X communication module to locate insecure parsing or buffer overflows.
- **Attack Steps**: 1. Obtain firmware image of the V2X module (from OTA updates or extracted flash). 2. Use Binwalk to extract filesystem contents and binaries. 3. Load main binaries into Ghidra and analyze parsing logic for message handling. 4. Identify insecure memcpy or sscanf usage. 5. Emulate the firmware with QEMU (if possible) to observe behavior on crafted inputs. 6. Design V2X packets that trigger crashes or overflow buffers. 7. Confirm exploitability in real-world test bench.
- **Detection**: Monitor V2X daemon logs and memory
- **Solution**: Harden message parsing logic, use stack canaries
- **Tags**: Firmware, Ghidra, RE

## LTE Telematics Replay Attack

- **Attack Type**: Replay Attack
- **Target**: Smart Cars with LTE
- **Vulnerability**: No nonce or replay protection on telematics API
- **MITRE**: T1636.001
- **Impact**: Unauthorized entry without credentials
- **Tools**: Burp Suite, mitmproxy, Wireshark
- **Scenario**: Replay valid LTE-based API requests to repeatedly unlock vehicle doors via the cloud interface.
- **Attack Steps**: 1. Intercept communication between mobile app and telematics backend using mitmproxy. 2. Capture a legitimate unlock command and its associated headers. 3. Observe if tokens or signatures are reused or weakly validated. 4. Resend the captured request multiple times via Burp Repeater. 5. Confirm if the car keeps unlocking on each replay. 6. Attempt minor modifications (e.g., replay after 30 mins) to test expiration limits. 7. Record success and identify poor session design.
- **Detection**: Telematics API logs
- **Solution**: Add nonce/timestamp validation to API backend
- **Tags**: LTE, Replay, Telematics

## Bluetooth L2CAP Flood

- **Attack Type**: Denial of Service
- **Target**: IVI System
- **Vulnerability**: Bluetooth stack mishandles malformed L2CAP
- **MITRE**: T1499
- **Impact**: Infotainment system crash
- **Tools**: btproxy, Btlejuice, Android Debug Bridge
- **Scenario**: Send malformed L2CAP frames over Bluetooth Classic to crash IVI system.
- **Attack Steps**: 1. Scan for the vehicle’s IVI Bluetooth MAC address. 2. Use btproxy to connect and start injecting malformed L2CAP segments. 3. Send oversized frames or boundary edge cases repeatedly. 4. Observe if the IVI system becomes unresponsive or crashes. 5. Try across multiple vehicles/models to test reproducibility. 6. Review system logs via ADB or syslog (if accessible). 7. Document the vulnerable stack or vendor.
- **Detection**: Crash logs, Bluetooth daemon logs
- **Solution**: Patch IVI OS, filter malformed frames
- **Tags**: Bluetooth, L2CAP, IVI

## Remote Engine Start via Telematics API

- **Attack Type**: API Abuse
- **Target**: Connected Cars
- **Vulnerability**: IDOR / Weak authorization on backend API
- **MITRE**: T1595.002
- **Impact**: Unauthorized control over engine functions
- **Tools**: Postman, Burp Suite, Telematics Docs
- **Scenario**: Bypass access controls on a poorly secured telematics API to start a vehicle remotely.
- **Attack Steps**: 1. Discover the endpoint for remote start in the car manufacturer’s telematics API. 2. Use Postman or Burp to enumerate request headers and parameters. 3. Fuzz the Authorization token field to identify IDOR or weak token validation. 4. Try valid tokens from one vehicle to control another (cross-vehicle control). 5. Once successful, send the crafted POST request to remotely start the engine. 6. Monitor actual engine start through physical camera or logs. 7. Report the broken access control issue.
- **Detection**: Telematics API logs
- **Solution**: Enforce strict authentication and scoping
- **Tags**: API, IDOR, Engine

## Bluetooth File Injection

- **Attack Type**: Data Injection
- **Target**: Android IVI
- **Vulnerability**: No filtering on received Bluetooth file types
- **MITRE**: T1203
- **Impact**: Potential code execution in IVI
- **Tools**: obexftp, Bluetoothctl, APKTool
- **Scenario**: Inject malicious APK file via Bluetooth OBEX protocol to install on Android-based IVI system.
- **Attack Steps**: 1. Pair with the IVI system over Bluetooth using bluetoothctl. 2. Use obexftp to attempt file transfer to system’s user folder. 3. Craft a signed malicious APK file that auto-triggers install prompts. 4. Send file repeatedly and monitor if the IVI prompts the user to install. 5. Explore privilege escalation via content providers inside APK. 6. Use APKTool to analyze existing trusted apps to mimic signing behavior. 7. Confirm install success and potential code execution.
- **Detection**: File transfer logs, install events
- **Solution**: Disable OBEX auto-accept or sandbox APK installs
- **Tags**: Bluetooth, APK, OBEX

## Fake Traffic Alert via V2X

- **Attack Type**: Message Spoofing
- **Target**: V2X / ADAS
- **Vulnerability**: Lack of authentication on V2X alerts
- **MITRE**: T1557.003
- **Impact**: Navigation manipulation, traffic diversion
- **Tools**: SDRplay, DSRC encoder, V2X Simulator
- **Scenario**: Emit fake accident or congestion messages via V2X to reroute vehicles.
- **Attack Steps**: 1. Use SDRplay with DSRC encoder to craft fake traffic alert packets. 2. Modify the "event type" field to simulate accidents or roadblocks. 3. Set geolocation to target area (interstate highway, city junction). 4. Transmit from roadside or bridge using directional antenna. 5. Observe nearby V2X-aware vehicles rerouting via ADAS. 6. Log ADAS behavior and visual alerts on dashboards. 7. Evaluate if attackers can steer traffic away from chosen areas.
- **Detection**: V2X event correlation logs
- **Solution**: Cryptographically verify alert sources
- **Tags**: V2X, DSRC, SDR

## BLE Device Spoofing

- **Attack Type**: Device Impersonation
- **Target**: BLE Smart Key
- **Vulnerability**: Weak pairing, static identifiers
- **MITRE**: T1557.002
- **Impact**: Unauthorized vehicle access
- **Tools**: btlejack, BlueZ, BLE Sniffer
- **Scenario**: Spoof BLE device identity to impersonate driver’s smartphone key.
- **Attack Steps**: 1. Use btlejack to scan for BLE advertisements from user’s phone key. 2. Clone the advertisement and GATT profile. 3. Re-broadcast the identity as attacker-controlled device. 4. Attempt vehicle unlock/start without the real device nearby. 5. Time attack when user leaves the car but within BLE range. 6. Observe vehicle behavior and log successful impersonations. 7. Confirm if manufacturer uses secure BLE pairing (Just Works vs Passkey).
- **Detection**: BLE pairing logs
- **Solution**: Use LE Secure Connections, rotate keys
- **Tags**: BLE, Spoofing, Unlock

## LTE SIM Swap Abuse

- **Attack Type**: Identity Hijack
- **Target**: Telematics Unit
- **Vulnerability**: SIM-based identity, carrier flaws
- **MITRE**: T1586.004
- **Impact**: Full remote control of vehicle
- **Tools**: Social Engineering, Carrier Portal, IMSI Catcher
- **Scenario**: Perform SIM swap attack on car's embedded SIM to hijack cloud control.
- **Attack Steps**: 1. Gather vehicle owner's personal info (via OSINT/social media). 2. Contact mobile carrier pretending to be user and request SIM replacement. 3. Activate a duplicate SIM with same IMSI/ICCID. 4. Insert attacker SIM into custom LTE modem and send telematics commands. 5. Confirm control over remote unlock/start via duplicated backend identity. 6. Optionally sniff encrypted traffic to clone tokens. 7. Document success and notify affected vendor.
- **Detection**: Telematics traffic, SIM logs
- **Solution**: Lock SIM to hardware UUID, MFA for carrier updates
- **Tags**: SIM Swap, LTE, Telematics

## V2X Firmware Downgrade

- **Attack Type**: Firmware Exploit
- **Target**: V2X Unit
- **Vulnerability**: No strict anti-downgrade policy
- **MITRE**: T1600
- **Impact**: Persistent access via vulnerable firmware
- **Tools**: Firmware Toolkit, OTA Spoofer, HTTP MITM Proxy
- **Scenario**: Force a downgrade of V2X firmware to a known vulnerable version via OTA.
- **Attack Steps**: 1. Monitor OTA update traffic from V2X unit using proxy tools. 2. Observe version check and firmware download URLs. 3. Intercept the firmware request and redirect to old vulnerable firmware. 4. Re-sign (or spoof validation if weak) and send to device. 5. Confirm downgrade via debug output or UI. 6. Use known exploit on the downgraded version (e.g., buffer overflow). 7. Document path to persistent backdoor or root.
- **Detection**: Firmware version tracking, hash mismatch alerts
- **Solution**: Enforce firmware rollback protection
- **Tags**: OTA, Firmware, Exploit

## Inject False Emergency Braking via V2X

- **Attack Type**: Injection
- **Target**: Vehicle ECU
- **Vulnerability**: Lack of DSRC message integrity/authentication
- **MITRE**: T1557
- **Impact**: Unintended braking or driver panic
- **Tools**: Ettus SDR, GNURadio, DSRC libraries
- **Scenario**: Adversary injects V2X messages simulating a crash ahead, causing the vehicle to brake suddenly.
- **Attack Steps**: 1. Set up an SDR device configured to broadcast DSRC messages. 2. Craft a CAM or DENM packet that signals an imminent crash or emergency braking ahead. 3. Transmit this crafted message on the DSRC band within range of a vehicle’s V2X module. 4. Observe if the vehicle triggers emergency braking or driver warnings due to the false alert. 5. Modify timing and repetition rate to test different scenarios.
- **Detection**: V2X message integrity check, time/correlation analysis
- **Solution**: Cryptographic signing of V2X messages, filtering based on vehicle proximity and velocity context
- **Tags**: V2X, DSRC, CAN, safety, injection

## Replay Previous V2V Warning

- **Attack Type**: Replay
- **Target**: V2X Module
- **Vulnerability**: No anti-replay mechanism in V2X protocol
- **MITRE**: T1001
- **Impact**: Safety mechanisms falsely triggered
- **Tools**: USRP B210, GNURadio, DSRC analyzer
- **Scenario**: Attacker replays a recorded V2V warning to create repeated false alarms.
- **Attack Steps**: 1. Use an SDR sniffer to record a genuine V2X safety alert between vehicles (e.g., sharp brake warning). 2. Save the radio waveform or extract the raw payload. 3. Later, rebroadcast the same message at a different location or time using the SDR. 4. Observe if nearby vehicles incorrectly respond to the outdated alert. 5. Repeat with slight timing offsets or altered signal strength.
- **Detection**: Analyze timestamp and signature freshness in V2X traffic
- **Solution**: Implement anti-replay counters, secure timestamps
- **Tags**: V2V, DSRC, replay attack, spoofing

## Exploiting Unencrypted Bluetooth OBD-II Dongle

- **Attack Type**: Bluetooth Exploitation
- **Target**: OBD-II Dongle
- **Vulnerability**: Weak Bluetooth authentication
- **MITRE**: T1421
- **Impact**: Unauthorized diagnostics or engine manipulation
- **Tools**: Bluetooth Scanner, Android Phone with Torque Pro, bt-obd
- **Scenario**: Attacker connects to a third-party Bluetooth OBD-II dongle that lacks pairing or encryption, and issues malicious commands.
- **Attack Steps**: 1. Discover nearby Bluetooth OBD-II dongles using a mobile app or hcitool. 2. Identify devices with no pairing or simple PINs. 3. Connect to the dongle using a diagnostic app or custom scripts. 4. Issue commands like reset DTCs, send RPM spoofing, or alter fuel mix data. 5. Monitor car behavior or onboard display changes.
- **Detection**: Bluetooth traffic sniffing, unexpected PID requests
- **Solution**: Use secure Bluetooth pairing, whitelist authorized devices
- **Tags**: Bluetooth, OBD-II, diagnostics

## Exploit Telematics API to Locate Vehicle

- **Attack Type**: API Enumeration
- **Target**: Telematics Server
- **Vulnerability**: Insecure backend API
- **MITRE**: T1071
- **Impact**: Privacy breach or targeted stalking
- **Tools**: Burp Suite, Postman, MITMProxy
- **Scenario**: Adversary accesses backend APIs (e.g., find my car) via stolen token or session.
- **Attack Steps**: 1. Obtain a valid session or API token via phishing, leaked logs, or insecure apps. 2. Explore the mobile app’s API using a proxy tool. 3. Enumerate endpoints like /location, /vehicle-status, or /control. 4. Send a request to fetch GPS coordinates of the target’s vehicle. 5. Monitor backend response and log live location.
- **Detection**: Telematics traffic logs, location access frequency
- **Solution**: Implement strong API auth, rate-limiting, logging
- **Tags**: Telematics, GPS, privacy

## BlueBorne Attack on Head Unit

- **Attack Type**: Remote Code Execution
- **Target**: IVI System
- **Vulnerability**: Bluetooth stack vulnerability (e.g., BlueZ, Android BT)
- **MITRE**: T1203
- **Impact**: Remote control of infotainment or deeper pivot
- **Tools**: BlueBorne Exploit Toolkit, Kali Linux
- **Scenario**: Adversary exploits Bluetooth stack flaw to gain code execution on the IVI system.
- **Attack Steps**: 1. Scan for nearby infotainment systems with Bluetooth enabled. 2. Identify vulnerable Bluetooth stack versions using fingerprinting. 3. Launch the BlueBorne exploit remotely using a pre-crafted payload targeting the IVI’s OS. 4. Upon successful execution, open a reverse shell or deploy a backdoor. 5. Use access to pivot into CAN bus if IVI has connectivity.
- **Detection**: Bluetooth audit, abnormal memory use
- **Solution**: Apply latest Bluetooth stack updates, restrict BT roles
- **Tags**: BlueBorne, IVI, RCE, Bluetooth

## LTE/5G Vehicle SIM Hijack via SS7

- **Attack Type**: Cellular Attack
- **Target**: Telematics Unit
- **Vulnerability**: Weak mobile backend security
- **MITRE**: T1429
- **Impact**: Remote control, privacy violations
- **Tools**: SS7 Exploitation Toolkit, Simjacker tools
- **Scenario**: Attacker manipulates mobile core to intercept vehicle SIM data or commands.
- **Attack Steps**: 1. Gain access to SS7 network (via rogue provider or partner abuse). 2. Use SS7 messages to track location of vehicle SIM based on IMSI. 3. Send silent SMS or intercept telematics commands if not encrypted. 4. Monitor API triggers sent over LTE (e.g., remote unlock, engine start). 5. Exploit misconfigured SMS-based APIs to issue unauthorized actions.
- **Detection**: SS7 monitoring, API audit logs
- **Solution**: Use end-to-end encrypted LTE backends, SIM hardening
- **Tags**: SS7, LTE, vehicle tracking

## Malicious Bluetooth Firmware Update

- **Attack Type**: Supply Chain Compromise
- **Target**: IVI System
- **Vulnerability**: Inadequate firmware signature validation
- **MITRE**: T1554
- **Impact**: Persistent access or BT spying
- **Tools**: Ghidra, Custom Update Tool
- **Scenario**: Attacker delivers malicious Bluetooth firmware to IVI system via OTA or USB update.
- **Attack Steps**: 1. Reverse engineer the firmware format of the vehicle’s Bluetooth chip (via teardown or dump). 2. Modify the firmware to insert a backdoor or packet sniffer. 3. Package the modified firmware in the official update format. 4. Deliver it via USB update or exploit OTA validation flaws. 5. After update, use compromised Bluetooth stack for persistent attack.
- **Detection**: Firmware integrity monitoring, OTA hash check
- **Solution**: Enforce firmware signing and secure boot
- **Tags**: Bluetooth, firmware, IVI, supply chain

## Exploit Wi-Fi-based Vehicle Tethering

- **Attack Type**: Wi-Fi Intrusion
- **Target**: Onboard Wi-Fi
- **Vulnerability**: Weak Wi-Fi password or open interface
- **MITRE**: T1040
- **Impact**: Browser compromise, potential CAN access
- **Tools**: Wireshark, Aircrack-ng, EvilAP
- **Scenario**: Attacker targets vehicle’s Wi-Fi hotspot to inject traffic or attack devices.
- **Attack Steps**: 1. Detect and fingerprint car’s onboard Wi-Fi network (e.g., TeslaAP). 2. Attempt to crack WPA key using weak passphrase or WPS flaw. 3. Upon access, scan connected internal services or devices (e.g., port 8080 for IVI). 4. Inject malicious JS into content loaded by the IVI browser. 5. Try pivoting into CAN-connected systems if exploitable interface exists.
- **Detection**: Network scan logs, unexpected HTTP traffic
- **Solution**: Use WPA3, strong passphrases, isolate IVI from Wi-Fi clients
- **Tags**: Wi-Fi, tethering, infotainment

## DSRC Flooding to Disrupt Traffic Comm

- **Attack Type**: Denial-of-Service
- **Target**: DSRC Receiver
- **Vulnerability**: No rate-limiting or validation of V2X input
- **MITRE**: T1499
- **Impact**: Denial of safety alerts
- **Tools**: GNURadio, Custom DSRC Flood Script
- **Scenario**: Flood V2X channel with junk messages to disrupt real-time alerts.
- **Attack Steps**: 1. Configure SDR to broadcast at high rate on DSRC band. 2. Generate dummy CAM messages with random positions and speeds. 3. Transmit hundreds of these per second to saturate the receiver buffer. 4. Observe nearby vehicles discarding real alerts or experiencing lag. 5. Test jamming resilience of specific V2X implementations.
- **Detection**: DSRC throughput metrics, flood detection logic
- **Solution**: Implement rate-limiting, input filtering, DSRC firewalls
- **Tags**: DSRC, DoS, traffic safety

## BLE Connection Spoofing Attack

- **Attack Type**: Spoofing
- **Target**: BLE Module
- **Vulnerability**: Weak pairing verification or static MAC
- **MITRE**: T1586
- **Impact**: Unauthorized vehicle unlock/start
- **Tools**: BLE Spoofing Toolkit, btproxy, Android BLE tools
- **Scenario**: Attacker pretends to be a trusted BLE device (e.g., phone) to gain access.
- **Attack Steps**: 1. Observe BLE advertisements from the legitimate phone paired with the car. 2. Clone MAC address and emulate characteristics using a BLE emulator. 3. Attempt to connect to the vehicle’s BLE service as a trusted phone. 4. If accepted, issue unlock or start commands. 5. Log whether replay protection or authentication mechanisms trigger.
- **Detection**: BLE logs, auth failure alerts
- **Solution**: Use rolling codes, BLE bonding with dynamic IDs
- **Tags**: BLE, spoofing, mobile key

