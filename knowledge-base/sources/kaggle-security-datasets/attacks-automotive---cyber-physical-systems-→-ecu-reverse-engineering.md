# Automotive / Cyber-Physical Systems → ECU Reverse Engineering Attacks

## Brute-Force Security Access Seed-Key Algorithm

- **Attack Type**: Brute Force
- **Target**: ECU
- **Vulnerability**: Weak seed-key algorithm
- **MITRE**: T1110 (Brute Force)
- **Impact**: Unlocks hidden ECU functions
- **Tools**: CANtact, Python Script, UDS Toolkit
- **Scenario**: Reverse engineer or brute-force the seed-key mechanism used by UDS to unlock secure ECU functions
- **Attack Steps**: 1. Send 0x27 (Security Access) request to target ECU. 2. Receive seed response and analyze format. 3. Apply known seed-key algorithms (if public). 4. If unknown, generate key guesses in real-time. 5. Attempt responses until ECU unlocks secure level (e.g., level 3 for full control). 6. Monitor for temporary lockouts and reset cycle if needed.
- **Detection**: Monitor repeated key attempts, rate limit
- **Solution**: Strong challenge-response or asymmetric crypto
- **Tags**: uds, seedkey, brute force, authentication

## Exploiting Incomplete Firmware Update Checks

- **Attack Type**: Update Process Abuse
- **Target**: ECU Firmware
- **Vulnerability**: Weak firmware integrity validation
- **MITRE**: T1601 (Modify System Firmware)
- **Impact**: Persistent control or stealthy behavior
- **Tools**: Binwalk, Firmware Update Tools
- **Scenario**: Flashing a partially modified firmware by bypassing checksum or authenticity checks
- **Attack Steps**: 1. Dump original firmware via diagnostic protocol or chip-off. 2. Modify a specific section (e.g., disable DTC logging). 3. Repack firmware using tools like Binwalk and pad to expected size. 4. Bypass or spoof CRC/checksum expected by ECU. 5. Flash altered firmware via official update mechanism (e.g., via UDS 0x34). 6. Monitor ECU behavior for success.
- **Detection**: Compare CRCs, validate signed firmware
- **Solution**: Enforce digital signature verification
- **Tags**: firmware, ECU, checksum bypass

## Diagnostic Service Abuse to Disable Safety Features

- **Attack Type**: Protocol Misuse
- **Target**: ECU
- **Vulnerability**: UDS Services Exposed Without Auth
- **MITRE**: T1562.001 (Disable or Modify Tools)
- **Impact**: Safety features disabled silently
- **Tools**: UDS Toolkit, CAN Utilities
- **Scenario**: Use UDS diagnostic services (e.g., 0x85 for DTC control) to turn off error reporting or active safety controls
- **Attack Steps**: 1. Access CAN network physically or remotely. 2. Identify ECU address and enter diagnostic session using 0x10. 3. Use service 0x85 (Control DTC Settings) to disable diagnostic codes. 4. Follow up with service 0x2F to disable actuator logic (e.g., airbags). 5. Test changes and confirm via absence of DTCs or alerts.
- **Detection**: Monitor DTC command traffic
- **Solution**: Enforce authenticated access to critical UDS services
- **Tags**: uds, dtc, disable, diagnostics

## Hardware-Based ECU Dump via BDM Interface

- **Attack Type**: Hardware Access
- **Target**: ECU Hardware
- **Vulnerability**: Accessible debug interfaces
- **MITRE**: T1121 (Hardware Additions)
- **Impact**: Full firmware and memory compromise
- **Tools**: BDM Adapter, Oscilloscope, IDA Pro
- **Scenario**: Using BDM or JTAG interface on PCB to extract raw memory and firmware
- **Attack Steps**: 1. Disassemble ECU and locate debug/test pads. 2. Use datasheets to identify BDM/JTAG pinout. 3. Connect BDM adapter (e.g., USB BDM interface). 4. Power ECU via bench setup and initiate dump process. 5. Save full memory dump and load into IDA or Ghidra. 6. Analyze memory regions and firmware logic.
- **Detection**: Physical inspection and epoxy/lockdown
- **Solution**: Remove test pads and secure interfaces
- **Tags**: bdm, jtag, hardware, ecu reverse engineering

## Reverse Engineering Flash Loader to Build Custom Uploader

- **Attack Type**: Custom Tooling
- **Target**: ECU Firmware
- **Vulnerability**: Reusable flash routines
- **MITRE**: T1587.002 (Develop Capabilities - Malware)
- **Impact**: Enables stealth or backdoor firmware upload
- **Tools**: Ghidra, IDA Pro, Custom Firmware Tools
- **Scenario**: Analyze ECU flash routines and build a custom reprogramming loader
- **Attack Steps**: 1. Identify the flash routine section in dumped firmware. 2. Trace function call graph to understand memory erasure and writing sequence. 3. Extract function signatures and create loader shell in C/Python. 4. Embed loader in a CAN injector or firmware flasher. 5. Test custom loader on test ECU or emulator before deploying.
- **Detection**: Firmware diffing and loader fingerprinting
- **Solution**: Use non-reusable encrypted flash routines
- **Tags**: loader, custom tools, firmware, reverse engineering

## Extracting EEPROM Secrets from ECU

- **Attack Type**: EEPROM Extraction
- **Target**: ECU Hardware
- **Vulnerability**: Unencrypted stored secrets
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Credential or config data theft
- **Tools**: EEPROM Programmer, Chip Clip, EEPROM Reader
- **Scenario**: Dump EEPROM to retrieve stored PINs, keys, or config data
- **Attack Steps**: 1. Locate EEPROM chip on ECU board (e.g., 93C66). 2. Connect EEPROM reader with chip clip without desoldering. 3. Power ECU and initiate EEPROM read. 4. Save dump and analyze with hex editor or decode tools. 5. Look for ASCII strings, key patterns, or PINs. 6. Use retrieved secrets for authentication or further access.
- **Detection**: EEPROM checksum or encryption
- **Solution**: Encrypt and obfuscate stored data
- **Tags**: eeprom, secrets, pin dump

## UDS Service Discovery for Attack Surface Mapping

- **Attack Type**: Reconnaissance
- **Target**: ECU
- **Vulnerability**: Excessive services exposed
- **MITRE**: T1592 (Gather Victim Host Information)
- **Impact**: Discovery of exploit paths
- **Tools**: UDS Scanner Script, CAN Interface
- **Scenario**: Probe ECU for supported UDS services and subfunctions to plan exploitation
- **Attack Steps**: 1. Scan ECU with 0x10 (diagnostic session control) to establish session. 2. Send 0x11–0x3E to enumerate supported services. 3. For each supported service, try various subfunctions and record response codes. 4. Analyze positive responses to discover enabled or misconfigured services. 5. Use information to plan privilege escalation or manipulation via valid commands.
- **Detection**: Monitor abnormal UDS scan behavior
- **Solution**: Limit services to minimum required
- **Tags**: uds, reconnaissance, ecu probing

