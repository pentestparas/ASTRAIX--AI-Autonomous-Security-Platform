# Automotive / CPS Attacks

## Dumping ECU Firmware via UART

- **Attack Type**: Firmware Extraction
- **Target**: Vehicle ECU
- **Vulnerability**: Unprotected debug UART access
- **MITRE**: T1608
- **Impact**: Raw firmware access, enabling reverse engineering and vulnerability discovery
- **Tools**: UART Cable, Logic Analyzer, Minicom
- **Scenario**: Attacker gains access to an ECU physically and locates UART pins to extract firmware using a serial connection
- **Attack Steps**: 1. Identify test points on the ECU board using a multimeter and inspect silkscreen labels for TX/RX/GND.2. Connect a USB-to-UART converter to the ECU’s pins and open a terminal emulator (e.g., Minicom) at standard baud rates.3. Power on the ECU and monitor boot logs or console access.4. Use bootloader commands to dump the memory or redirect logs to extract the firmware.5. Save and clean the binary image for later analysis.
- **Detection**: Anomalous serial communication logs; unauthorized physical access events
- **Solution**: Disable UART in production; epoxy/debug pin obfuscation
- **Tags**: ECU, UART, Firmware, Reverse Engineering

## Extracting ECU Firmware Using SPI Flash Reader

- **Attack Type**: Hardware-Based Firmware Dump
- **Target**: Vehicle ECU
- **Vulnerability**: Exposed SPI flash chip without encryption
- **MITRE**: T1608
- **Impact**: Full firmware access, enabling attacker to bypass logic or modify behavior
- **Tools**: CH341A, Flashrom, SOIC8 Clip
- **Scenario**: Attacker uses physical access to connect to SPI flash chip on ECU and dump memory directly
- **Attack Steps**: 1. Disassemble ECU to expose PCB and locate the SPI flash chip using datasheet markings.2. Connect SOIC8 clip to the chip and link it to the CH341A programmer.3. Use Flashrom to identify and dump the chip content.4. Repeat the dump multiple times to ensure image consistency.5. Save binary and analyze using tools like Ghidra for reverse engineering.
- **Detection**: Physical access logs; anomaly in boot checksums
- **Solution**: Encrypt flash content; epoxy over chip; secure bootloader
- **Tags**: SPI Flash, Dumping, ECU Hacking

## Static Analysis of Extracted Firmware in Ghidra

- **Attack Type**: Reverse Engineering
- **Target**: ECU Firmware
- **Vulnerability**: Lack of obfuscation or insecure logic
- **MITRE**: T1518.001
- **Impact**: Discovery of insecure logic or debug paths
- **Tools**: Ghidra, Binwalk
- **Scenario**: Reverse engineer dumped ECU firmware using Ghidra to find vulnerabilities
- **Attack Steps**: 1. Open dumped firmware binary in Binwalk to locate partitions and extract file systems.2. Load the relevant executable region into Ghidra and define processor architecture (e.g., ARM Cortex-M, PPC).3. Identify main functions and CAN handlers by analyzing strings and function references.4. Look for insecure routines, such as hardcoded authentication bypasses or debug modes.5. Document findings and determine exploitable logic.
- **Detection**: Firmware tampering detection tools
- **Solution**: Obfuscate code, audit logic during development
- **Tags**: Ghidra, Firmware Analysis

## Locating Debug Interfaces on ECU PCB

- **Attack Type**: Hardware Reconnaissance
- **Target**: ECU PCB
- **Vulnerability**: Exposed and undocumented debug ports
- **MITRE**: T1595.001
- **Impact**: Entry point for firmware readout or device unlocking
- **Tools**: Multimeter, Datasheet, Oscilloscope
- **Scenario**: Attacker performs board-level inspection to locate possible JTAG/SWD or UART ports for firmware access
- **Attack Steps**: 1. Disassemble the ECU and visually inspect for unpopulated headers or labeled debug pads.2. Use multimeter continuity checks to trace connections from test pads to known microcontroller pins.3. Cross-reference chip datasheets to confirm debug functionality (e.g., JTAG TMS, TCK).4. Use oscilloscope to detect signal activity during ECU boot, verifying port functionality.5. Prepare for future attacks like firmware dumping or live debugging.
- **Detection**: Physical inspection indicators
- **Solution**: Remove test pads post-manufacture; use epoxy
- **Tags**: PCB, Debug Port, Recon

## Dumping Firmware via Bootloader Interface

- **Attack Type**: Firmware Dump
- **Target**: ECU
- **Vulnerability**: Insecure bootloader access without auth
- **MITRE**: T1040
- **Impact**: Gaining full control of firmware logic
- **Tools**: UDS Sender, CANalyzer, UART tools
- **Scenario**: Attacker uses vendor-specific bootloader access mode (e.g., via CAN or UART) to request firmware readout
- **Attack Steps**: 1. Identify the ECU's processor type and its supported bootloader protocol (e.g., ST Bootloader via UART or CAN).2. Enter bootloader mode by triggering a specific pin combo during power-on.3. Use software like Flash Loader Demonstrator or custom UDS sender to request memory read commands.4. Dump the entire firmware over the interface and save it for analysis.5. Exit bootloader mode and optionally test image on a simulated ECU.
- **Detection**: Logging of bootloader entry events
- **Solution**: Restrict bootloader access; enforce auth
- **Tags**: Bootloader, Dump, UDS

## Extracting Code from NAND Flash in Infotainment Unit

- **Attack Type**: Memory Dump
- **Target**: Infotainment System
- **Vulnerability**: Lack of encryption or secure boot
- **MITRE**: T1608
- **Impact**: Extraction of sensitive files, keys, and firmware
- **Tools**: NAND Reader, TSOP Adapter, Flash Extractor
- **Scenario**: NAND flash is removed from infotainment board and dumped using chip reader for full filesystem access
- **Attack Steps**: 1. Desolder NAND flash chip (e.g., Samsung K9F1G08U0C) from the infotainment system PCB.2. Place the chip into a TSOP adapter compatible with the NAND reader.3. Use Flash Extractor or similar tool to read out the NAND memory.4. Extract file system (e.g., YAFFS2, UBIFS) and locate applications, configurations, keys.5. Analyze boot process and check for exploitable services or hardcoded credentials.
- **Detection**: Boot integrity check failures
- **Solution**: Enforce NAND encryption, secure boot
- **Tags**: NAND, Flash Dumping, Infotainment

## Fingerprinting Firmware Architecture via Strings

- **Attack Type**: Reconnaissance
- **Target**: ECU Firmware
- **Vulnerability**: Easily fingerprinted codebase
- **MITRE**: T1592
- **Impact**: Easier exploitation based on known firmware base
- **Tools**: Binwalk, Strings, Ghidra
- **Scenario**: Attacker uses strings analysis and magic bytes to determine target firmware architecture for reverse engineering
- **Attack Steps**: 1. Run strings on the dumped firmware to identify version info, toolchain identifiers, or logs.2. Use Binwalk to carve out partition types and identify format (e.g., squashfs, uImage, ELF).3. Correlate strings with specific platforms (e.g., GCC for ARM, VxWorks, QNX, etc.).4. Use these clues to configure the disassembler for accurate reverse engineering.5. This helps streamline exploitation by targeting known OS-specific weaknesses.
- **Detection**: Unusual log strings or config values
- **Solution**: Remove debug/log strings in release firmware
- **Tags**: Firmware, Fingerprinting

## Identifying CAN Message Handlers in Firmware

- **Attack Type**: Static Analysis
- **Target**: ECU Firmware
- **Vulnerability**: Insecure or weak message parsing
- **MITRE**: T1589
- **Impact**: Enables crafting of malicious CAN messages
- **Tools**: Ghidra, IDA Pro
- **Scenario**: Attacker analyzes firmware binary to locate and understand CAN message parsing functions
- **Attack Steps**: 1. Open binary in Ghidra and locate vector tables and entry points.2. Search for message IDs and compare with known CAN IDs (e.g., 0x7DF, 0x123).3. Identify message processing logic using switch-case patterns or look-up tables.4. Trace handlers to understand how data is parsed and responded to.5. Look for lack of validation or exploitable parsing bugs.
- **Detection**: Firmware behavior profiling
- **Solution**: Validate and sanitize CAN input
- **Tags**: Ghidra, CAN Reverse Engineering

## Discovering Backdoor Passwords in ECU Firmware

- **Attack Type**: Credential Discovery
- **Target**: ECU
- **Vulnerability**: Hardcoded passwords or debug bypass
- **MITRE**: T1552.001
- **Impact**: Unauthorized control over ECU via hidden creds
- **Tools**: Ghidra, Strings
- **Scenario**: Analyze firmware strings and functions to find embedded credentials or backdoors
- **Attack Steps**: 1. Use strings on firmware to find any embedded user credentials, PINs, or diagnostic passwords.2. In Ghidra, locate hardcoded comparisons or authentication functions.3. Trace through these routines to dump default credentials or authentication bypass logic.4. Test these credentials on physical or simulated ECU.5. Report or use in further exploitation scenarios.
- **Detection**: Logging of diag command use
- **Solution**: Avoid static passwords, use challenge-response
- **Tags**: Firmware, Backdoor, Hardcoded Key

## Extracting Symbol Information from Debug Builds

- **Attack Type**: Reverse Engineering
- **Target**: ECU
- **Vulnerability**: Symbols leaked in production build
- **MITRE**: T1592
- **Impact**: Eases analysis and exploitation
- **Tools**: Ghidra, ELF Parser, IDA
- **Scenario**: Attacker finds debug firmware image containing symbol info that helps reverse engineering
- **Attack Steps**: 1. Check firmware headers for debug builds (e.g., presence of .symtab, .debug_str).2. Use ELF parsers to list all function names and variables.3. Load symbolized binary into Ghidra — automatic function labeling makes reversing much faster.4. Review annotated code paths and locate sensitive logic like diagnostics or OTA.5. Use this info to craft precise exploit paths.
- **Detection**: Larger binary sizes, verbose strings
- **Solution**: Strip symbols before release
- **Tags**: ELF, Symbol Info, Debug Build

