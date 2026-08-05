# Zero-Day Research / Fuzzing → Target Reconnaissance & Environment Setup Attacks

## Fuzzing Android System Daemon in Emulator

- **Attack Type**: Environment Setup
- **Target**: Android Emulator
- **Vulnerability**: IPC Handling
- **MITRE**: T1499.004
- **Impact**: Remote code execution or service crash
- **Tools**: AOSP, Android Emulator, AFL++, Frida
- **Scenario**: Researcher sets up Android emulator with system daemons to fuzz Binder IPC calls
- **Attack Steps**: 1. Download AOSP source and sync with Android build tools.2. Build a userdebug image of a specific Android version that includes system daemons like netd, vold, etc.3. Launch Android Emulator in a host-only network mode.4. Attach Frida to hook Binder IPC transactions.5. Use AFL++ or a custom IPC fuzzer to send malformed or edge-case data to daemon endpoints.6. Capture crashes and triage crash dumps using logcat and tombstone logs.7. Reboot emulator snapshot after crash for persistent fuzzing.
- **Detection**: Emulator crash logs, tombstone entries
- **Solution**: Patch daemon IPC handler and validate input types
- **Tags**: android, aosp, binder, ipc, emulator

## Docker-Based Setup for Media Player Fuzzing

- **Attack Type**: Container-Based Fuzzing
- **Target**: Docker Container
- **Vulnerability**: File Parsing
- **MITRE**: T1203
- **Impact**: Code execution on media parsing
- **Tools**: Docker, mpv, AFL++, GDB
- **Scenario**: Researcher wants to fuzz a Linux media player using malformed audio files inside a Docker container
- **Attack Steps**: 1. Choose a media player (e.g., mpv) and get its source code.2. Write a Dockerfile with required dependencies (libav, ffmpeg).3. Compile with AFL++ instrumentation (CC=afl-clang-fast).4. Copy a seed corpus of valid .mp3 and .flac files into /input in container.5. Configure AFL++ in persistent mode to reduce forkserver overhead.6. Mount /output as a persistent volume to extract crashes.7. Enable GDB inside container to automate crash triage post-fuzzing.8. Roll back container on crash and relaunch fuzz loop.
- **Detection**: AFL crash logs, strace, GDB analysis
- **Solution**: Validate file parsing logic and sanitize third-party libs
- **Tags**: docker, afl, mpv, file parser, container

## Setting Up QEMU VM for Kernel Driver Fuzzing

- **Attack Type**: Kernel Fuzzing Setup
- **Target**: QEMU VM
- **Vulnerability**: Kernel Driver
- **MITRE**: T1068
- **Impact**: Privilege escalation via kernel bug
- **Tools**: QEMU, syzkaller, Linux Kernel, KASAN
- **Scenario**: Researcher targets a Linux kernel module (.ko) for fuzzing using QEMU and syzkaller
- **Attack Steps**: 1. Clone Linux kernel source and configure for fuzzing (make defconfig && enable KASAN).2. Compile kernel with debugging symbols and build the specific .ko module.3. Set up a minimal rootfs with SSH for interaction.4. Launch QEMU with the kernel and connect via serial.5. Install and configure syzkaller to interact with QEMU kernel.6. Provide syscall descriptions for the target module to syzkaller.7. Monitor KASAN crash reports and extract reproducers.8. Use snapshotting to persist state across crashes.
- **Detection**: KASAN logs, QEMU serial output
- **Solution**: Patch kernel or remove unsafe syscall exposure
- **Tags**: kernel, qemu, syzkaller, linux, fuzz

## Identifying Fuzz Targets in Open Source PDF Readers

- **Attack Type**: Target Recon
- **Target**: Linux Application
- **Vulnerability**: PDF Parsing
- **MITRE**: T1203
- **Impact**: Memory corruption in PDF input
- **Tools**: MuPDF, Evince, Poppler
- **Scenario**: Researcher looks for vulnerable open-source PDF readers with parsing complexity
- **Attack Steps**: 1. Search GitHub/GitLab for PDF libraries used in Linux environments (Evince, MuPDF).2. Audit source code for parsing modules (e.g., pdf_parser.c, pdf_validate.c).3. Check file input handling for parser logic.4. Note file formats supported (PDF/A, hybrid PDF, compressed streams).5. Choose parser with fewer fuzzing attempts in the past.6. Clone source and list fuzzable entry points (e.g., pdf_open_document).7. Check build compatibility with sanitizers (ASAN, UBSAN).8. Document which readers rely on outdated or custom parsing code.
- **Detection**: ASAN/UBSAN crash logs
- **Solution**: Harden parsing routines and fuzz input validation
- **Tags**: pdf, parser, mupdf, evince, open source

## AFL++ Instrumentation of Custom Protocol Daemon

- **Attack Type**: Binary Instrumentation
- **Target**: Linux Server
- **Vulnerability**: Custom Protocol
- **MITRE**: T1071
- **Impact**: Memory or logic flaw in server daemon
- **Tools**: AFL++, TCP server, GDB, netcat
- **Scenario**: Researcher builds a Linux daemon that uses a custom TCP protocol and prepares it for fuzzing
- **Attack Steps**: 1. Identify or create a C-based TCP server daemon handling structured messages.2. Modify Makefile to compile with CC=afl-clang-fast.3. Write a harness program that accepts input via stdin and sends it to the daemon logic.4. Compile the harness statically for easy AFL use.5. Create initial test cases representing real-world TCP messages.6. Run AFL++ in dumb mode to begin basic mutation.7. Capture crashes and use GDB for triage.8. Add grammar-aware fuzzing later for protocol coverage.
- **Detection**: AFL crash dir, core dumps
- **Solution**: Rewrite protocol logic or apply bounds checking
- **Tags**: custom, protocol, tcp, afl++, daemon

## Fuzzing a Windows Service Using WinAFL

- **Attack Type**: Windows Service Fuzzing
- **Target**: Windows Service
- **Vulnerability**: Binary Protocol
- **MITRE**: T1211
- **Impact**: Denial of service or code execution
- **Tools**: WinAFL, DynamoRIO, IDA Pro
- **Scenario**: Researcher fuzzes a closed-source Windows service using WinAFL and DynamoRIO
- **Attack Steps**: 1. Identify Windows service executable (.exe or .dll) to be fuzzed.2. Use IDA Pro or Ghidra to reverse engineer the entry point and identify input handlers.3. Write a minimal wrapper harness that launches the service and injects input.4. Attach WinAFL and use DynamoRIO to begin fuzzing target functions.5. Provide sample inputs and minimize them to form a seed corpus.6. Monitor system for BSOD, service crashes, and memory leaks.7. Use VM snapshot to restore Windows after each crash.8. Analyze minidumps using WinDbg to locate crash cause.
- **Detection**: WinDbg, event viewer, WinAFL stats
- **Solution**: Harden service input checks or refactor input loop
- **Tags**: windows, winafl, reverse engineering, dynrio

## Setting Up Persistent Loop for Embedded Fuzzing

- **Attack Type**: Embedded System Setup
- **Target**: Embedded System
- **Vulnerability**: Binary Fuzzing
- **MITRE**: T1203
- **Impact**: RCE on embedded firmware
- **Tools**: QEMU ARM, Binwalk, AFL++, Firmadyne
- **Scenario**: Researcher sets up fuzzing loop on emulated ARM firmware image
- **Attack Steps**: 1. Extract ARM firmware image using Binwalk.2. Emulate using QEMU-user or full-system mode with Firmadyne.3. Identify fuzzable binaries (e.g., web servers, CGI scripts, daemons).4. Compile AFL++ with cross-compilation support (arm-linux-gnueabi-gcc).5. Write a harness or wrapper to feed input to the binary.6. Set up snapshot mechanism to revert filesystem after crash.7. Run fuzzing in headless mode and monitor logs.8. Dump core files and analyze with GDB-multiarch.
- **Detection**: syslog, core dumps, AFL stats
- **Solution**: Patch vulnerable binary or update firmware
- **Tags**: embedded, qemu, firmadyne, afl

## Isolating Sandboxed Chrome Renderer for Fuzzing

- **Attack Type**: Browser Fuzzing
- **Target**: Chrome Browser
- **Vulnerability**: Rendering Engine
- **MITRE**: T1203
- **Impact**: Code execution via HTML rendering
- **Tools**: Chrome Canary, AFL++, GDB, Linux VM
- **Scenario**: Researcher isolates Chrome renderer process in a VM to fuzz with targeted inputs
- **Attack Steps**: 1. Download and install Chrome Canary build with debug symbols.2. Launch browser in Linux VM with --single-process or --no-sandbox flags.3. Use command line to feed input HTML to render engine.4. Set up AFL++ to fuzz the rendering engine via command-line calls.5. Capture crash dumps using ulimit -c unlimited and GDB.6. Revert VM snapshot after crash to maintain fuzz loop.7. Trace call stack and identify affected components (blink, v8).8. Patch crash logic and rerun fuzzer.
- **Detection**: core dumps, GDB, VM logs
- **Solution**: Patch vulnerable rendering function
- **Tags**: chrome, browser, fuzz, renderer

## Running LLVM’s LibFuzzer on Open Source Audio Library

- **Attack Type**: Library Fuzzing
- **Target**: Audio Library
- **Vulnerability**: File Parsing
- **MITRE**: T1203
- **Impact**: Heap overflow in decoder
- **Tools**: LibFuzzer, CMake, AudioLib
- **Scenario**: Researcher uses LibFuzzer to test an open-source audio decoder library
- **Attack Steps**: 1. Select an audio library (e.g., libmad, libopus).2. Clone source and inspect audio decoding functions.3. Write a fuzz target that passes input to decoder entry point.4. Compile using clang with -fsanitize=fuzzer,address.5. Provide initial .mp3 samples for corpus.6. Run fuzzer and monitor for out-of-bound reads, leaks.7. Save crash inputs and triage using GDB.8. Report bugs upstream or fork and patch.
- **Detection**: sanitizer logs, crash files
- **Solution**: Fix decoding logic or restrict input bounds
- **Tags**: libfuzzer, audio, decoder, open source

## Reproducing and Isolating a Kernel Crash Found During Fuzzing

- **Attack Type**: Crash Isolation
- **Target**: Linux Kernel
- **Vulnerability**: Kernel Interface
- **MITRE**: T1068
- **Impact**: Local privilege escalation or panic
- **Tools**: syzkaller, QEMU, KASAN, repro-scripts
- **Scenario**: Researcher isolates a syzkaller-triggered kernel crash and prepares PoC
- **Attack Steps**: 1. Review syzkaller logs and extract crashing syscall sequence.2. Copy repro C program and compile with debug symbols.3. Launch QEMU kernel with same config used in fuzzing.4. Run repro repeatedly and check for consistent crash.5. Enable dmesg, klogd, and KASAN to monitor memory violations.6. Patch one input param at a time to narrow root cause.7. Trace crash location via GDB kernel debugging.8. Write a PoC report and submit responsibly.
- **Detection**: KASAN, klogd, syslog
- **Solution**: Fix faulty syscall logic and sanitize args
- **Tags**: syzkaller, kernel, crash triage

## Recon & Setup: Reverse-Engineering a Mobile App Parser

- **Attack Type**: Reconnaissance + Setup
- **Target**: Mobile App Parser
- **Vulnerability**: Memory corruption via malformed file parsing
- **MITRE**: T1588.006
- **Impact**: Discovery of unknown parsing vulnerabilities
- **Tools**: Ghidra, Frida, AFL++, Docker
- **Scenario**: Researcher aims to fuzz the parsing function of a closed-source mobile app that handles encrypted documents.
- **Attack Steps**: 1. Identify the APK of the target Android app and decompile it using JADX or apktool. 2. Use Ghidra to reverse engineer the native library (.so file) responsible for document parsing. 3. Isolate the parsing function (e.g., parseEncryptedFile) by tracing JNI calls. 4. Create a minimal harness in C that wraps the target function. 5. Use Frida to monitor real-time function calls and confirm parameter structure. 6. Build the harness with AFL++ instrumentation using afl-clang-fast. 7. Set up an Ubuntu Docker container with Android NDK and emulator if needed. 8. Run initial dry-run fuzzing to ensure input is correctly processed. 9. Create a crash triage setup using ASAN builds. 10. Start fuzzing with a corpus of mutated encrypted files.
- **Detection**: Use of Frida hooks and dynamic analysis during fuzzing
- **Solution**: Secure coding, hardened parsing libraries, post-analysis triage
- **Tags**: mobile, reverse engineering, JNI, encrypted files

## Recon & Setup: Building and Fuzzing Samba Daemon on Linux

- **Attack Type**: Environment Setup
- **Target**: Network Daemon
- **Vulnerability**: Heap buffer overflows in network protocol handler
- **MITRE**: T1046
- **Impact**: Remote code execution or denial of service
- **Tools**: Samba, AFL++, QEMU, ASAN
- **Scenario**: Researcher prepares to fuzz the Samba SMB server component on a Linux system.
- **Attack Steps**: 1. Identify target function in Samba source handling SMB1 requests. 2. Clone Samba from official Git and checkout a known stable version. 3. Modify configure script to include AFL++ instrumentation (e.g., set CC=afl-clang-fast). 4. Enable --enable-debug and --enable-developer flags. 5. Compile with -fsanitize=address for runtime visibility. 6. Set up input harness targeting smbd/server.c. 7. Create a basic corpus of malformed SMB packets using Wireshark exports. 8. Set up a QEMU-based Debian Linux image with port forwarding. 9. Run smbd inside QEMU with AFL in forkserver mode. 10. Monitor for crashes and log inputs for triage.
- **Detection**: ASAN logs, AFL crash stats
- **Solution**: Secure network protocol parsing and bounds checking
- **Tags**: samba, SMB, qemu, AFL++, server fuzzing

## Recon & Setup: Fuzzing an Open-Source Torrent Client

- **Attack Type**: Target Discovery + Setup
- **Target**: Desktop App
- **Vulnerability**: Parsing logic error via malformed .torrent
- **MITRE**: T1203
- **Impact**: Application crash or DoS
- **Tools**: qBittorrent, AFL++, UBSAN, Docker
- **Scenario**: Researcher investigates input handling in a torrent client’s .torrent file parser.
- **Attack Steps**: 1. Identify .torrent parser function in qBittorrent by browsing source and Doxygen docs. 2. Clone repo and configure for AFL++: CC=afl-clang-fast CXX=afl-clang-fast++. 3. Add UBSAN flags for undefined behavior detection. 4. Create a standalone harness that wraps parseTorrentFile() function. 5. Prepare mutated .torrent files as initial corpus. 6. Use Docker to create a reproducible Ubuntu fuzzing environment with libtorrent-rasterbar dependencies. 7. Install AFL++, mount harness and corpus. 8. Run afl-fuzz in persistent mode. 9. Monitor sanitizer logs for subtle integer overflows. 10. On crash, triage inputs and record findings for later CVE submission.
- **Detection**: UBSAN + AFL logs
- **Solution**: Input validation and parser hardening
- **Tags**: qbittorrent, torrent, file fuzzing, parser

## Recon & Setup: Snapshot-Based Fuzzing of a Custom Windows Driver

- **Attack Type**: Environment Setup
- **Target**: Kernel Driver
- **Vulnerability**: Improper IOCTL input validation
- **MITRE**: T1068
- **Impact**: Privilege escalation or BSOD
- **Tools**: WinDbg, VM Snapshot Manager, Syzkaller, VirtualBox
- **Scenario**: Security engineer aims to fuzz a custom kernel-mode driver on Windows using VM snapshots.
- **Attack Steps**: 1. Acquire driver sample and install it on a Windows 10 test VM. 2. Use WinDbg to attach to kernel and identify target IOCTL handlers. 3. Write a user-mode fuzzer that communicates with the driver via DeviceIoControl. 4. Snapshot VM in clean state using VirtualBox or Checkpoint Manager. 5. Launch fuzzing, monitor with WinDbg logs. 6. On crash, rollback VM to clean snapshot automatically. 7. Modify fuzzer to mutate input structures used in IOCTL calls. 8. Use Syzkaller to guide fuzzing if driver is exposed via syscall interface. 9. Re-enable snapshot and repeat for multiple handler targets. 10. Maintain crash corpus for later debugging and CVE submission.
- **Detection**: WinDbg crash trace, memory dump
- **Solution**: Harden IOCTL interface and sanitize input buffers
- **Tags**: kernel, windows driver, snapshot fuzzing

## Recon & Setup: Headless Build and Fuzz of WebKit for macOS

- **Attack Type**: Target Setup
- **Target**: Browser Engine
- **Vulnerability**: Memory corruption via HTML parser
- **MITRE**: T1203
- **Impact**: RCE via web content
- **Tools**: WebKit, Xcode, AFL++, ASAN, CMake
- **Scenario**: Researcher targets WebKit's HTML parser using macOS headless build.
- **Attack Steps**: 1. Clone WebKit repo and follow headless build instructions for macOS. 2. Configure build with AFL++ instrumentation using Xcode generator and CMAKE_C_COMPILER. 3. Focus on HTMLTreeBuilder.cpp and isolate processToken() function. 4. Build a harness using main() that mimics HTML input loading. 5. Compile with ASAN for crash visibility. 6. Use AFL++ with pre-seeded HTML test cases. 7. Run fuzzing on a dedicated macOS VM to avoid host instability. 8. On crashes, use atos for symbolication and backtrace. 9. Iterate harness improvements and input validation. 10. Export findings for browser security team disclosure.
- **Detection**: ASAN backtrace and logs
- **Solution**: Patch and sandbox affected parser logic
- **Tags**: webkit, macos, browser, AFL++, HTML

## Recon & Setup: Static Binary Fuzzing of Firmware Dump

- **Attack Type**: Environment Setup
- **Target**: Embedded Firmware
- **Vulnerability**: Stack overflow in config parser
- **MITRE**: T1499
- **Impact**: System crash or device reboot
- **Tools**: binwalk, AFL++, QEMU, radare2
- **Scenario**: Researcher attempts to fuzz a statically compiled binary from a router firmware image.
- **Attack Steps**: 1. Extract firmware using binwalk -e firmware.bin. 2. Locate binaries using file and readelf. 3. Use radare2 to analyze the entry point and understand the parsing function. 4. Build an emulated environment using QEMU (e.g., mipsel-linux). 5. Patch binary to skip firmware checks if needed. 6. Set up AFL++ with QEMU mode (afl-qemu-trace) for binary-only fuzzing. 7. Prepare a corpus of config files and request payloads. 8. Run afl-fuzz in deterministic mode for initial rounds. 9. Monitor QEMU output and logs for faults. 10. On crash, extract inputs and examine behavior using GDB inside QEMU.
- **Detection**: QEMU logs and crash reproduction
- **Solution**: Harden parser and isolate crash point
- **Tags**: firmware, binary fuzzing, router, embedded

## Recon & Setup: Dockerized Fuzzing of an Email MIME Parser

- **Attack Type**: Recon + Setup
- **Target**: Email Parser
- **Vulnerability**: Heap misuse on malformed MIME parts
- **MITRE**: T1033
- **Impact**: Email filter bypass or crash
- **Tools**: AFL++, Docker, Valgrind, Clang
- **Scenario**: Security researcher sets up fuzzing for a C-based MIME parser used in email filters.
- **Attack Steps**: 1. Identify and clone the open-source MIME parser project. 2. Build with Clang and ASAN using CFLAGS="-fsanitize=address". 3. Write a minimal harness that feeds test MIME strings into parseMIME() function. 4. Use Docker to build isolated container with all dependencies. 5. Mount input corpus of .eml files. 6. Run afl-fuzz in persistent mode, monitoring container logs. 7. On crash, validate using Valgrind to confirm memory issue. 8. Snapshot container state for reproducibility. 9. Test mutated inputs against production variant of filter. 10. Record unique crashes for CVE triage.
- **Detection**: Valgrind logs, container monitoring
- **Solution**: Harden MIME parsing and normalize inputs
- **Tags**: mime, email filter, fuzzing, docker

## Recon & Setup: Snapshot Loop for Linux SUID Fuzzing

- **Attack Type**: Environment Setup
- **Target**: SUID Binary
- **Vulnerability**: Privilege escalation via unchecked input
- **MITRE**: T1068
- **Impact**: Local root access
- **Tools**: AFL++, ASAN, KVM snapshot tool, GDB
- **Scenario**: Researcher fuzzes a SUID binary for local privilege escalation using snapshot rollback.
- **Attack Steps**: 1. Identify SUID binary with known input entry point. 2. Build ASAN-instrumented variant with debug symbols. 3. Configure fuzzing VM with KVM snapshot and rollback support. 4. Write test harness feeding input via stdin to binary. 5. Enable snapshot loop using virt-snapshot. 6. Start AFL++ in fork mode, configured to resume on reboot. 7. Log crashes and triage input using ASAN stack trace. 8. Debug crash cases using GDB within VM. 9. Monitor for privilege escalation via setuid mishandling. 10. Document vulnerability and sandbox suggestion.
- **Detection**: ASAN + crash triage via VM logs
- **Solution**: Remove SUID flag or refactor logic
- **Tags**: linux, SUID, snapshot loop, fuzzing

## Recon & Setup: Fuzzing a Legacy XML Library

- **Attack Type**: Target Reconnaissance
- **Target**: XML Library
- **Vulnerability**: Parsing flaws in XML tree handling
- **MITRE**: T1203
- **Impact**: App DoS or memory corruption
- **Tools**: libxml2, AFL++, UBSAN, Docker
- **Scenario**: Researcher targets a legacy C XML parser used in legacy web apps.
- **Attack Steps**: 1. Identify legacy version of libxml2 with parsing bugs. 2. Clone and checkout older commit. 3. Compile with -fsanitize=undefined and AFL instrumentation. 4. Isolate target function xmlParseDocument() in harness. 5. Prepare corpus of malformed XML files. 6. Run fuzzing inside Docker to isolate host. 7. Monitor UBSAN logs for integer overflow and memory issues. 8. On crash, reproduce and confirm with standalone harness. 9. Log CVE candidate and report upstream. 10. Suggest patch and contribution to community.
- **Detection**: UBSAN + fuzzer logs
- **Solution**: Use latest XML libs or harden input paths
- **Tags**: xml, legacy, parser, AFL++

## Recon & Setup: Testing a Proprietary Protocol Handler via Black-Box Fuzzing

- **Attack Type**: Recon + Setup
- **Target**: Network Protocol Handler
- **Vulnerability**: Overflow on malformed TCP message
- **MITRE**: T1040
- **Impact**: DoS or unauthenticated remote code execution
- **Tools**: Scapy, Boofuzz, Docker, Wireshark
- **Scenario**: Researcher black-box fuzzes a proprietary protocol running over TCP.
- **Attack Steps**: 1. Reverse engineer protocol using packet captures from Wireshark. 2. Write Scapy scripts to craft synthetic protocol packets. 3. Create Boofuzz harness to automate input generation. 4. Build Docker test container with network isolation. 5. Deploy target application inside container. 6. Fuzz TCP service using Boofuzz-generated malformed packets. 7. Log crash behavior using container logs and Wireshark. 8. Identify possible buffer overflows or parsing crashes. 9. Iterate mutation logic based on observed feedback. 10. Document crash pattern for protocol patching.
- **Detection**: Crash logs, packet inspection
- **Solution**: Add protocol state validation and bounds checks
- **Tags**: TCP, protocol, boofuzz, black-box

