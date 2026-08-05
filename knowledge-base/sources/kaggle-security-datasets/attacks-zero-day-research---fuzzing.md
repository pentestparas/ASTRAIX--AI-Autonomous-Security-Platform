# Zero-Day Research / Fuzzing Attacks

## Fuzzing Setup for Open-Source PDF Parser

- **Attack Type**: Environment Preparation
- **Target**: File Parser
- **Vulnerability**: Memory Corruption
- **MITRE**: T1595
- **Impact**: Potential code execution via malformed files
- **Tools**: Git, AFL++, clang, ASAN, Ubuntu VM
- **Scenario**: A researcher wants to find memory corruption vulnerabilities in a lightweight open-source PDF parsing library.
- **Attack Steps**: 1. Search GitHub for open-source PDF parsers with C/C++ codebase.2. Clone the repo and inspect build system (Makefile/CMake).3. Modify build settings to use clang and compile with -fsanitize=address and -fsanitize=undefined flags.4. Compile using AFL’s afl-clang-fast to add instrumentation.5. Set up Ubuntu VM with a snapshot.6. Install AFL++ and test instrumented binary with a few seed PDFs.7. Ensure ASAN logs are captured.8. Validate crash reports to prepare for fuzzing.
- **Detection**: Monitor ASAN logs, use AFL’s crash minimizer
- **Solution**: Use hardened memory-safe parsers
- **Tags**: fuzzing, ASAN, PDF, Ubuntu, open-source

## Kernel Driver Recon & Build with KASAN

- **Attack Type**: Target Identification
- **Target**: Kernel
- **Vulnerability**: Heap Use-After-Free
- **MITRE**: T1587
- **Impact**: Kernel-level crash or elevation
- **Tools**: Linux Kernel Source, KASAN, QEMU
- **Scenario**: Researcher is targeting a Linux kernel driver for fuzzing using kernel address sanitizer (KASAN).
- **Attack Steps**: 1. Identify a kernel driver with frequent bug reports (e.g., USB or Wi-Fi driver).2. Download Linux source matching the driver version.3. Configure kernel with CONFIG_KASAN=y.4. Compile kernel with KASAN enabled using make bzImage.5. Set up QEMU with the compiled kernel.6. Add snapshot support in QEMU.7. Trigger driver functionality manually to observe behavior.8. Prepare KASAN logs to capture invalid memory access.
- **Detection**: KASAN logs, syslog analysis
- **Solution**: Patch affected driver, refactor unsafe code
- **Tags**: KASAN, kernel, QEMU, fuzzing, heap

## Browser Fuzz Target Scouting

- **Attack Type**: Target Discovery
- **Target**: Browser
- **Vulnerability**: Input Validation Flaws
- **MITRE**: T1592
- **Impact**: Remote code execution via crafted input
- **Tools**: Chromium source, git, fuzzdb, Ghidra
- **Scenario**: Analyst is selecting a fuzz target from popular browser forks with minimal hardening.
- **Attack Steps**: 1. Search for less-known Chromium forks (e.g., Kiwi, Ungoogled).2. Review commit history to assess activity.3. Download source and analyze sandbox model.4. Use Ghidra to inspect binary interfaces of PDF or image handling components.5. Select one with large attack surface and weak sandboxing.6. Document all exposed file handlers or IPC endpoints.7. Prepare fuzzing plan based on exposed modules.8. Identify fuzzable entry points with AFL or libFuzzer.
- **Detection**: Static binary diff, IPC fuzzing
- **Solution**: Enforce sandboxing, input validation
- **Tags**: browser, chromium, fuzz target, reverse engineering

## Dockerized Environment for Network Daemon Fuzzing

- **Attack Type**: Controlled Fuzzing Setup
- **Target**: Network Daemon
- **Vulnerability**: Buffer Overflow
- **MITRE**: T1210
- **Impact**: Denial of service or RCE via crafted packets
- **Tools**: Docker, AFL++, netcat, iptables
- **Scenario**: Researcher sets up an isolated Docker container for fuzzing a network service.
- **Attack Steps**: 1. Choose a lightweight open-source daemon (e.g., FTP server written in C).2. Create Dockerfile with AFL, sanitizer-enabled build.3. Add iptables rules to block external communication.4. Configure container to expose daemon on a local port.5. Create snapshot using docker commit.6. Generate seed corpus using netcat.7. Run AFL++ with TCP mode input.8. Use crash triage scripts inside container.
- **Detection**: AFL logs, network fuzz metrics
- **Solution**: Harden parsing code, validate inputs
- **Tags**: Docker, daemon, AFL, container, fuzzing

## Snapshot Loop for Windows Media Player Fuzzing

- **Attack Type**: VM-based Fuzzing
- **Target**: Media Player
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203
- **Impact**: Exploitable crash on malformed media file
- **Tools**: VMware/VirtualBox, AFLWin, WinDbg, Sysinternals
- **Scenario**: Security researcher targets Windows Media Player codec handler in a VM loop.
- **Attack Steps**: 1. Install Windows VM with media player version to be fuzzed.2. Enable snapshot support and configure quick restore.3. Prepare media files with corrupted metadata.4. Automate execution of files on media player.5. Set up WinDbg with script to attach and log crashes.6. Restore snapshot after each test.7. Save crash dumps and check logs for access violations.8. Repeat with mutated file samples.
- **Detection**: WinDbg logs, event logs
- **Solution**: Update codec handler, input filtering
- **Tags**: Windows, media, fuzzing, snapshot, codec

## Fuzzing Android Kernel via Emulator

- **Attack Type**: Mobile Kernel Fuzzing
- **Target**: Mobile Kernel
- **Vulnerability**: Race Condition
- **MITRE**: T1547
- **Impact**: Kernel crash or privilege escalation
- **Tools**: Android Emulator, KASAN, AFL++, AOSP
- **Scenario**: Analyst fuzzes Android kernel drivers using emulator with modified system image.
- **Attack Steps**: 1. Download AOSP source for compatible Android version.2. Enable CONFIG_KASAN=y and build the kernel.3. Repackage system.img with fuzzable kernel module.4. Launch Android Emulator with new image.5. Attach AFL++ to driver communication interface.6. Send malformed packets to device interface.7. Capture KASAN logs from kernel console.8. Isolate crashing input and trace cause.
- **Detection**: KASAN logs, kernel console
- **Solution**: Patch driver logic, lock handling
- **Tags**: Android, kernel, emulator, fuzzing

## Preparing LibJPEG for Fuzzing

- **Attack Type**: Source Compilation
- **Target**: Image Parser
- **Vulnerability**: Integer Overflow
- **MITRE**: T1203
- **Impact**: Memory corruption via malformed image
- **Tools**: clang, libFuzzer, LibJPEG source, ASAN
- **Scenario**: Engineer wants to fuzz LibJPEG for image parsing bugs using libFuzzer and sanitizers.
- **Attack Steps**: 1. Download LibJPEG source code.2. Modify CMakeLists.txt to enable -fsanitize=address,undefined.3. Add a libFuzzer-compatible main harness.4. Compile with clang and -fsanitize flags.5. Generate valid seed JPEG files.6. Run libFuzzer with a short timeout.7. Observe crashes or ASAN output.8. Isolate crashing image and trigger path.
- **Detection**: ASAN traces, core dumps
- **Solution**: Harden parsing code, check boundaries
- **Tags**: libjpeg, image, libfuzzer, build

## QEMU VM for IoT Device Fuzzing

- **Attack Type**: Emulated Target Setup
- **Target**: IoT Device
- **Vulnerability**: Stack Overflow
- **MITRE**: T1200
- **Impact**: Remote crash or command injection
- **Tools**: QEMU, binwalk, AFL++, FirmAE, netcat
- **Scenario**: Researcher wants to emulate an ARM-based IoT firmware to fuzz TCP services.
- **Attack Steps**: 1. Extract firmware using binwalk.2. Use FirmAE to emulate in QEMU.3. Identify TCP daemon binaries.4. Recompile extracted binary with AFL instrumentation.5. Generate seed TCP payloads using netcat.6. Run AFL in QEMU guest via SSH.7. Capture logs and triage crashes.8. Reset QEMU VM periodically.
- **Detection**: AFL logs, binary analysis
- **Solution**: Use secure code in IoT stack
- **Tags**: IoT, QEMU, firmware, fuzzing, ARM

## Comparative Recon on Audio Decoders

- **Attack Type**: Reconnaissance
- **Target**: Audio Decoder
- **Vulnerability**: Buffer Overread
- **MITRE**: T1203
- **Impact**: Audio corruption or crash via malformed file
- **Tools**: GitHub, Ghidra, AFL++, Google FuzzBench
- **Scenario**: Analyst compares open-source audio decoders for fuzzing suitability.
- **Attack Steps**: 1. List audio decoders like libsndfile, mpg123, ffmpeg audio modules.2. Download each repo and inspect parser complexity.3. Use Ghidra to check memory handling practices.4. Evaluate test coverage and fuzzability.5. Run basic AFL fuzz with 3-5 input seeds.6. Record initial crashes or sanitizer hits.7. Choose the decoder with highest crash yield.8. Document architecture and input format.
- **Detection**: Sanitizer output, test logs
- **Solution**: Input boundary checks, stricter parsing
- **Tags**: audio, recon, fuzzbench, Ghidra

## Setting Up Fuzzing Infrastructure in CI

- **Attack Type**: Fuzzing Pipeline Setup
- **Target**: Any Application
- **Vulnerability**: Undefined Behavior
- **MITRE**: T1499
- **Impact**: Continuous discovery of edge-case crashes
- **Tools**: GitHub Actions, AFL++, clang, Docker
- **Scenario**: Engineer integrates sanitizer builds and fuzzing into CI pipeline for nightly testing.
- **Attack Steps**: 1. Fork target project repo (e.g., file parser).2. Add GitHub Action to build with clang -fsanitize=address,undefined.3. Create a fuzz harness and run AFL in headless mode.4. Use Docker container to isolate fuzzing runs.5. Store crashing inputs as GitHub artifacts.6. Add schedule trigger for nightly builds.7. Monitor crash count via logs.8. Add triage script to summarize new findings.
- **Detection**: CI build logs, sanitizer crash outputs
- **Solution**: Triage crashes, fix bugs early
- **Tags**: CI/CD, fuzzing, GitHub, ASAN

## Instrumenting Exiv2 Image Parser for Fuzzing

- **Attack Type**: Source Preparation
- **Target**: Image Parser
- **Vulnerability**: Metadata Parsing
- **MITRE**: T1203
- **Impact**: Triggering memory corruption via crafted EXIF data
- **Tools**: clang, libFuzzer, ASAN, Exiv2 source
- **Scenario**: Researcher selects Exiv2, an open-source image metadata parser, as a fuzz target. Needs to build it with sanitizers and prepare input corpus.
- **Attack Steps**: 1. Search GitHub for "Exiv2" repository and clone it locally.2. Review documentation to understand dependencies and build system (CMake-based).3. Install all dependencies using apt install cmake build-essential zlib1g-dev.4. Add -fsanitize=address,undefined and -g -O1 to the CMake build flags.5. Insert a basic fuzzing harness (main.cpp) using libFuzzer's interface targeting metadata parsing.6. Use clang++ to build the project with libFuzzer linked in (-fsanitize=fuzzer).7. Generate a few valid sample images with EXIF metadata for the seed corpus.8. Test the binary with ./fuzzer_corpus/ as input and verify ASAN triggers on malformed metadata.9. Adjust the harness and flags if crashes are not reported.10. Document the fuzzing setup and snapshot the environment.
- **Detection**: ASAN error output, libFuzzer stats
- **Solution**: Harden EXIF field parsing and sanitize buffer sizes
- **Tags**: CMake, EXIF, image parsing, libFuzzer

## Preparing Firefox with Custom Fuzz Hooks

- **Attack Type**: Browser Target Build
- **Target**: Browser
- **Vulnerability**: Memory Mismanagement
- **MITRE**: T1203
- **Impact**: Browser crash or sandbox escape
- **Tools**: Mozilla Firefox source, GYP, clang, libFuzzer
- **Scenario**: Engineer builds a custom version of Firefox with fuzzable hooks in the image decoding module.
- **Attack Steps**: 1. Download the Firefox source using Mozilla's ./mach bootstrap script.2. Use a powerful Linux machine or cloud build system due to Firefox's size.3. Modify the image decoding component (e.g., PNG decoder) to expose an entry point.4. Write a new fuzzer class that takes raw PNG bytes and invokes the decode function directly.5. Add libFuzzer-compatible harness around it.6. Build the project using ./mach build with --enable-fuzzing and --enable-address-sanitizer flags.7. Collect a seed corpus of PNG files from image datasets.8. Run the binary on sample files using libFuzzer and observe if ASAN detects heap or stack issues.9. Use logs from /tmp and error traces to isolate crashes.10. Validate that fuzzing targets only the modified decoder module and not the full browser runtime.
- **Detection**: ASAN logs, Firefox crash reporter
- **Solution**: Restrict memory allocation bounds, sanitize input
- **Tags**: browser, firefox, decoder, libFuzzer

## Isolating OpenSSH Daemon for Fuzzing

- **Attack Type**: Network Target Setup
- **Target**: Network Daemon
- **Vulnerability**: Protocol Parsing
- **MITRE**: T1210
- **Impact**: Triggering crash in packet parser
- **Tools**: Docker, OpenSSH, AFL++, clang, strace
- **Scenario**: Researcher aims to fuzz the OpenSSH daemon’s packet parser using an isolated fuzzing container.
- **Attack Steps**: 1. Clone the OpenSSH GitHub repo or download a clean tarball of the latest version.2. Study the protocol handling code inside packet.c and dispatch.c.3. Set up a Docker container running Ubuntu, install build dependencies like zlib1g-dev, libssl-dev, and clang.4. Modify Makefile to replace cc with afl-clang-fast.5. Create a test harness that feeds crafted binary SSH packets into the sshd_input logic.6. Mount /fuzzdata to store inputs and outputs persistently inside the container.7. Use strace to monitor system calls and ensure the fuzzer doesn’t fork excessively.8. Run AFL in persistent mode with -t 5000 to avoid timeout crashes.9. Track crashes using afl-cmin and afl-tmin.10. Collect triage data and logs after every 5000 iterations.
- **Detection**: AFL logs, core dumps
- **Solution**: Refactor packet parsing to handle edge cases
- **Tags**: OpenSSH, AFL, sshd, packet parser

## Building VLC Media Player with Sanitizers

- **Attack Type**: Source Compilation
- **Target**: Media Player
- **Vulnerability**: Decoder Bugs
- **MITRE**: T1203
- **Impact**: Exploitable crash during media playback
- **Tools**: VLC source, clang, ASAN, MSAN, FFmpeg
- **Scenario**: Researcher wants to fuzz VLC's audio decoder modules, requiring a successful sanitizer build.
- **Attack Steps**: 1. Clone the VLC source from the official repo.2. Read the build docs to identify dependencies like FFmpeg, libvorbis, libflac, and configure them.3. Install required packages: sudo apt install libtool automake pkg-config yasm clang.4. Run ./bootstrap and configure VLC with --enable-debug --enable-fuzzing.5. Modify decoder module to include a fuzz entry point.6. Add clang sanitizer flags to configure: CFLAGS="-fsanitize=address,undefined" CXXFLAGS="-fsanitize=address,undefined".7. Build the fuzzing target using make and validate that binary executes with test data.8. Run test corpus of valid .mp3, .ogg files.9. Observe sanitizer output on malformed metadata or variable-length encoding.10. Store all crash artifacts and generate a triage spreadsheet.
- **Detection**: ASAN/MSAN logs, debugger output
- **Solution**: Rewrite decoder boundary checks
- **Tags**: VLC, decoder, ASAN, media

## Setting Up KVM Snapshots for Persistent Fuzzing

- **Attack Type**: Virtual Machine Setup
- **Target**: Linux App
- **Vulnerability**: Input Validation
- **MITRE**: T1499
- **Impact**: Continuous fuzzing without VM corruption
- **Tools**: KVM, qemu-img, AFL++, Linux
- **Scenario**: Researcher uses KVM and snapshots for looping persistent fuzz tests on a Linux app.
- **Attack Steps**: 1. Create a new Linux VM using KVM with a lightweight distro like Alpine or Ubuntu Server.2. Install AFL++ and dependencies in the guest machine.3. Compile the target binary with AFL instrumentation.4. Prepare seed inputs and mount them inside the guest.5. Create a snapshot of the clean fuzzing state using qemu-img snapshot -c clean-state.6. Write a host-side script that reverts the VM state after each crash using virsh snapshot-revert.7. Run AFL inside the guest, capturing outputs to a mounted drive.8. Detect crashes and use AFL's crash parser to validate them.9. Automate the snapshot restore loop via cron or systemd timer.10. Run fuzzing overnight and collect new crashes the next day.
- **Detection**: Crash logs, AFL stats
- **Solution**: Maintain snapshot integrity, auto-clean input dirs
- **Tags**: snapshot, qemu, AFL, persistent fuzzing

## Creating Minimal Docker Image for Fuzzing LibXML2

- **Attack Type**: Environment Optimization
- **Target**: File Parser
- **Vulnerability**: XML Entity Bugs
- **MITRE**: T1203
- **Impact**: Crash or logic bug in XML parser
- **Tools**: Docker, clang, AFL++, LibXML2
- **Scenario**: Engineer wants to run fuzzing efficiently using a small Docker image targeting LibXML2.
- **Attack Steps**: 1. Start with alpine:latest as the base image.2. Install build tools: apk add build-base clang git libxml2-dev.3. Clone LibXML2 and patch its parser to support a simple AFL harness.4. Add instrumentation with afl-clang-fast in the Dockerfile build phase.5. Copy seed XML samples into /corpus inside the image.6. Use Docker volumes to persist crashes outside the container.7. Build the image with docker build -t xmlfuzzer .8. Run AFL in the container using CPU limit flags to avoid runaway processes.9. Parse crashes with afl-analyze.10. Export mutated inputs and logs using docker cp.
- **Detection**: AFL logs, XML parsing errors
- **Solution**: Sanitize XML entity handling
- **Tags**: XML, docker, libxml2, AFL

## Target Discovery in IoT Firmware Blob

- **Attack Type**: Firmware Recon
- **Target**: IoT Firmware
- **Vulnerability**: Config File Parsing
- **MITRE**: T1200
- **Impact**: Fuzzing of hidden embedded binaries
- **Tools**: binwalk, Ghidra, QEMU, AFL++
- **Scenario**: Analyst analyzes a binary firmware dump to locate fuzzable components.
- **Attack Steps**: 1. Obtain a firmware blob (e.g., router firmware) from vendor site.2. Run binwalk -e firmware.bin to extract the filesystem and binaries.3. Use Ghidra to analyze extracted ELF binaries for interesting I/O interfaces (e.g., web admin, config parser).4. Identify statically linked binary for a config daemon.5. Transfer it to a Linux test box and run AFL instrumentation via recompilation or binary rewriting.6. Set up a basic harness to feed fake config files.7. Use QEMU if needed for architecture emulation (ARM/MIPS).8. Launch fuzzing using a few real config files as input.9. Monitor AFL coverage and crashes.10. Document candidate CVEs and reproduce any discovered crashes.
- **Detection**: QEMU logs, binary inspection
- **Solution**: Patch embedded services, validate input format
- **Tags**: firmware, config, binwalk, embedded

## Static Recon of Media Libraries Using Fuzz Introspector

- **Attack Type**: Static Analysis
- **Target**: Media Library
- **Vulnerability**: Unfuzzed Code Paths
- **MITRE**: T1595
- **Impact**: Missed bugs in non-fuzzed logic
- **Tools**: Fuzz Introspector, Clang, LLVM
- **Scenario**: Security engineer uses Fuzz Introspector to analyze which library functions are fuzzed.
- **Attack Steps**: 1. Choose a media processing library (e.g., libpng, libtiff).2. Compile the project using clang with Fuzz Introspector instrumentation flags.3. Run Fuzz Introspector to generate a heatmap of functions touched by existing fuzzers.4. Review the report to find uncovered but high-complexity functions.5. Write new fuzz harnesses for uncovered code paths.6. Recompile and run a coverage test using libFuzzer.7. Observe which parts of the code are now reached.8. Use report diff to track improvement.9. Export coverage diff as HTML or JSON for report inclusion.10. Plan next round of harnesses based on results.
- **Detection**: Fuzz Introspector reports
- **Solution**: Add new fuzz harnesses, expand coverage
- **Tags**: coverage, introspector, libpng, harness

## Ubuntu VM Setup for AFLNet-Based Network Fuzzing

- **Attack Type**: Network Protocol Fuzzing
- **Target**: Network Daemon
- **Vulnerability**: Packet Parsing
- **MITRE**: T1210
- **Impact**: Protocol crash, memory leak
- **Tools**: AFLNet, Ubuntu, clang, tcpdump
- **Scenario**: Researcher wants to set up Ubuntu for running AFLNet on a networked binary target.
- **Attack Steps**: 1. Install Ubuntu in VirtualBox or KVM with bridge networking.2. Clone AFLNet and compile using make.3. Choose a network protocol daemon (e.g., HTTP, FTP) from open source projects.4. Modify the daemon build to use afl-clang-fast.5. Compile the target and validate it listens on a known port.6. Prepare packet-format seed corpus.7. Configure AFLNet to replay TCP payloads via fuzz loop.8. Monitor packet flows using tcpdump or Wireshark.9. Collect and isolate crashes caused by malformed packets.10. Restart target after each crash using AFLNet’s reset mechanism.
- **Detection**: AFLNet logs, tcpdump output
- **Solution**: Harden packet parsing, validate lengths
- **Tags**: AFLNet, TCP, Ubuntu, network fuzz

## Using Syzkaller for Linux Syscall Fuzzing

- **Attack Type**: Kernel Environment Setup
- **Target**: Linux Kernel
- **Vulnerability**: Syscall Exploits
- **MITRE**: T1587
- **Impact**: Kernel crashes, privilege escalation
- **Tools**: Syzkaller, KASAN, QEMU, Linux Kernel
- **Scenario**: Researcher uses Syzkaller to fuzz Linux syscalls on a VM with KASAN.
- **Attack Steps**: 1. Download a compatible Linux kernel source tree.2. Configure it with make menuconfig to enable CONFIG_KASAN=y and CONFIG_DEBUG_INFO=y.3. Build the kernel and rootfs, and launch a QEMU VM with it.4. Clone Syzkaller and configure it with paths to QEMU, kernel image, and rootfs.5. Use the example config to create a fuzzing setup for x86_64 architecture.6. Run Syzkaller and observe the dashboard for coverage and crashes.7. Wait for the system to generate valid programs using the syscall descriptions.8. Collect crash logs and minimized reproducers.9. Validate bugs using GDB and kernel logs.10. Patch issues and rerun fuzzing for regression detection.
- **Detection**: KASAN logs, syzkaller output
- **Solution**: Patch syscall handlers, validate inputs
- **Tags**: syzkaller, kernel, syscall, fuzzing

## Building Custom Harness for libTIFF

- **Attack Type**: Source Instrumentation
- **Target**: File Parser
- **Vulnerability**: Buffer Overflow
- **MITRE**: T1203
- **Impact**: Heap corruption in TIFF parsing logic
- **Tools**: libTIFF source, clang, libFuzzer, ASAN
- **Scenario**: Researcher targets libTIFF for image parsing vulnerabilities by building a custom fuzzing harness.
- **Attack Steps**: 1. Download libTIFF source from the official GitHub repository.2. Study the TIFF image decoding API, especially TIFFReadEncodedStrip and TIFFOpen.3. Write a C++ fuzzing harness that reads bytes into a memory buffer and passes them to the TIFF API.4. Add -fsanitize=address,undefined -fno-omit-frame-pointer to compiler flags.5. Compile the harness using clang++ -fsanitize=fuzzer.6. Prepare seed corpus with real .tiff files for maximum code coverage.7. Run libFuzzer with verbose mode enabled to observe path exploration.8. Capture crash logs, backtraces, and coverage stats.9. Use llvm-cov to identify uncovered functions.10. Refine harness and repeat until all image parsing code is exercised.
- **Detection**: ASAN stack traces
- **Solution**: Harden field size checks, fuzz-safe decompression
- **Tags**: libTIFF, harness, ASAN, fuzzing

## Snapshot-Enabled AFL Fuzzing for FTP Server

- **Attack Type**: Network Service Looping
- **Target**: Network Daemon
- **Vulnerability**: Heap Overflows
- **MITRE**: T1210
- **Impact**: Remote crash or code execution over FTP
- **Tools**: AFL++, qemu, VirtualBox, lftp, Ubuntu
- **Scenario**: Security team configures AFL in a snapshot-enabled environment to repeatedly fuzz an FTP daemon.
- **Attack Steps**: 1. Identify and download an open-source FTP daemon like pure-ftpd or vsftpd.2. Install Ubuntu VM in VirtualBox with snapshot functionality enabled.3. Instrument the daemon binary using afl-clang-fast with ASAN support.4. Place seed .txt and .bin files in /input directory.5. Install AFL++ inside VM and script it to start the daemon in debug mode.6. Write a host script to auto-revert the VM using VBoxManage snapshot commands after every crash.7. Fuzz FTP commands (e.g., STOR, RETR, LIST) using a simulated FTP client like lftp.8. Enable AFL logging to /output/crashes and /output/queue.9. Review crash results daily and triage unique inputs.10. Patch FTP daemon with stronger length checks and restart fuzzing.
- **Detection**: AFL crash logs, netstat tracing
- **Solution**: Add FTP command parsing filters
- **Tags**: FTP, AFL, snapshot, network fuzzing

## QEMU-Emulated MIPS IoT Stack Fuzzing

- **Attack Type**: Emulated Firmware Setup
- **Target**: IoT Firmware
- **Vulnerability**: Stack Overflow
- **MITRE**: T1200
- **Impact**: Remote execution via crafted config or request
- **Tools**: binwalk, QEMU, AFL++, Firmadyne, Ghidra
- **Scenario**: Analyst uses QEMU to emulate a MIPS-based IoT firmware image and fuzz embedded binaries.
- **Attack Steps**: 1. Obtain firmware from an IoT router vendor (e.g., D-Link, TP-Link).2. Extract filesystem using binwalk -e and locate userland binaries like /bin/configd.3. Use Firmadyne or manually configure QEMU with the extracted rootfs.4. Identify fuzzable services like HTTP handlers or config daemons.5. Instrument statically-linked binaries using binary rewriting or source recompilation (if available).6. Feed corpus of real device config files or HTTP requests.7. Run fuzzing in QEMU guest via SSH and monitor outputs.8. Log syscalls and memory crashes with Ghidra symbol mapping.9. Analyze unique crashes using afl-plot and afl-whatsup.10. Document CVE candidates for vendor disclosure.
- **Detection**: QEMU logs, AFL, syscalls
- **Solution**: Use safer parsing libraries, remove legacy code
- **Tags**: MIPS, IoT, firmware, QEMU

## AFLNet Fuzzing Setup for HTTP Server

- **Attack Type**: Network Protocol Fuzzing
- **Target**: Web Server
- **Vulnerability**: Protocol State Bugs
- **MITRE**: T1210
- **Impact**: HTTP daemon crash or RCE via malformed request
- **Tools**: AFLNet, Ubuntu, tcpdump, Wireshark
- **Scenario**: Researcher fuzzes a basic HTTP server using AFLNet in a controlled virtual environment.
- **Attack Steps**: 1. Download lightweight open-source HTTP server (e.g., mongoose, httpd).2. Modify the build system to use afl-clang-fast with -fsanitize=address.3. Build and validate the binary works with sample HTTP GET requests.4. Prepare a corpus of valid HTTP request samples in a structured directory.5. Install AFLNet and configure it to fuzz over TCP (-D TCP) with proper input format.6. Use Wireshark/tcpdump to verify TCP connection handling.7. Launch AFLNet with timeout parameters and monitor coverage.8. Review crash logs and triage malformed HTTP requests.9. Isolate input that causes segmentation faults or memory leaks.10. Report issues and re-run with mutated versions of crashing packets.
- **Detection**: AFLNet TCP fuzzing logs
- **Solution**: Improve state handling logic, use RFC parser
- **Tags**: HTTP, AFLNet, TCP fuzzing, daemon

## Isolating File Format Parser in Media App

- **Attack Type**: Component Isolation
- **Target**: Media Parser
- **Vulnerability**: Memory Corruption
- **MITRE**: T1203
- **Impact**: Crashes during audio decoding from malformed FLAC
- **Tools**: clang, GDB, libFuzzer, ffmpeg, ASAN
- **Scenario**: Engineer isolates the FLAC parser in an open-source media app to fuzz it independently.
- **Attack Steps**: 1. Clone open-source media tool like ffmpeg or Audacity.2. Locate the module that parses .flac files, typically libavcodec/flacdec.c.3. Write a minimal test harness that includes only the decoding logic, linked against static libraries.4. Build with clang -fsanitize=address,undefined,fuzzer.5. Prepare FLAC samples and place them in a corpus/ folder.6. Run the fuzzer and observe sanitizer output.7. Use GDB to attach to fuzzer for precise fault isolation.8. Map stack traces back to vulnerable input samples.9. Harden the parser with size checks and retry.10. Repeat until fuzzer hits >90% function coverage.
- **Detection**: ASAN logs, debugger output
- **Solution**: Add size/format validation on FLAC header
- **Tags**: FLAC, audio, media, libFuzzer

## Containerized Setup for Fuzzing PDFium

- **Attack Type**: Docker Environment Setup
- **Target**: File Renderer
- **Vulnerability**: Input Validation
- **MITRE**: T1203
- **Impact**: Crashes in PDF rendering engine
- **Tools**: Docker, clang, PDFium, ASAN, libFuzzer
- **Scenario**: Researcher builds a Dockerized fuzzing environment for Chrome’s PDF rendering engine.
- **Attack Steps**: 1. Clone PDFium repo and follow build instructions for Linux.2. Create a Dockerfile using ubuntu:20.04 and install depot_tools, ninja, clang, and dependencies.3. Enable AddressSanitizer and Fuzzer flags in the GN config: is_debug=true, use_custom_libcxx=false, is_asan=true.4. Add a harness that feeds PDF byte buffers into PDFium render interface.5. Compile using autoninja -C out/asan pdfium_fuzz.6. Generate a corpus of valid PDFs with varying layout features.7. Run fuzzing with large timeout and volume mount for logs.8. Track crashes and generate minimized reproducers.9. Periodically rebuild the container for clean-state replays.10. Export triaged bugs for bug bounty submission.
- **Detection**: ASAN stack trace, minimized PDF inputs
- **Solution**: Harden rendering paths and check input structure
- **Tags**: PDFium, docker, chrome, ASAN

## LLDPE Executable Fuzzing on Linux

- **Attack Type**: Executable Format Testing
- **Target**: Executable Loader
- **Vulnerability**: Header Parsing Flaw
- **MITRE**: T1204
- **Impact**: Remote loader crash from malformed ELF
- **Tools**: Linux, LLDPE, elfutils, AFL++, GDB
- **Scenario**: Analyst targets LLDPE (Linux Loader) for malformed executable handling bugs.
- **Attack Steps**: 1. Choose LLDPE-based target like ELF loaders or custom loaders in IoT firmware.2. Write harness to load malformed .elf files into a stripped-down loader interface.3. Build using clang -fsanitize=address -static.4. Use elfutils to create and mutate ELF header fields.5. Create fuzz corpus with varied .text, .data, .bss segment values.6. Launch AFL with memory watch mode enabled.7. Track crash reports and validate with GDB.8. Observe behavior on invalid program headers.9. Triage corrupt inputs and report ELF parser bugs.10. Patch with boundary checks and rebuild.
- **Detection**: AFL logs, GDB stack trace
- **Solution**: Add parser boundary validations
- **Tags**: ELF, loader, AFL, binary

## Automating VM Reset Loop via Cron

- **Attack Type**: Snapshot Fuzzing Loop
- **Target**: Any Application
- **Vulnerability**: Resource Exhaustion
- **MITRE**: T1499
- **Impact**: Long-term fuzzing automation, better coverage
- **Tools**: VirtualBox, cron, AFL++, rsync
- **Scenario**: Researcher automates VM resets to run long-term fuzzing with state preservation.
- **Attack Steps**: 1. Set up VirtualBox VM with the fuzz target and snapshot tools installed.2. Take a snapshot post-install and pre-fuzz (vboxmanage snapshot save).3. Write a script to monitor AFL crash directory (/out/crashes) and trigger VM restore if populated.4. Schedule the script using cron to run every 30 minutes.5. Rsync crash artifacts to host for persistent storage.6. Restart AFL inside VM on reboot with a shell auto-start.7. Monitor logs and validate recovery routine.8. Run for multiple days and accumulate crash coverage.9. Use deduplication tools to group similar crashes.10. Report issues upstream or submit to fuzzing leaderboards.
- **Detection**: Cron logs, AFL stats, system reboot logs
- **Solution**: Automated reset, deduplicate test cases
- **Tags**: snapshot, VM, automation, cron

## Configuring Kernel for User-Space Fuzzing Hooks

- **Attack Type**: Kernel Debugging Prep
- **Target**: Kernel
- **Vulnerability**: Custom Syscall Bugs
- **MITRE**: T1587
- **Impact**: Kernel crash via malformed syscall structure
- **Tools**: Linux kernel source, KASAN, GDB, Syzkaller
- **Scenario**: Engineer configures Linux kernel with KASAN and custom syscall hooks for fuzzing syscalls.
- **Attack Steps**: 1. Clone the Linux source for version 5.x.2. Enable CONFIG_KASAN, CONFIG_DEBUG_INFO, and CONFIG_FAULT_INJECTION.3. Build kernel using make bzImage with Clang.4. Modify syscall table to include a dummy syscall interface that can take fuzzer-generated input.5. Write userland program that calls this syscall with randomized input.6. Launch system in QEMU and load modified kernel.7. Attach GDB stub for kernel debugging and break on syscall_handler.8. Observe syscall behavior and detect illegal access patterns.9. Use Syzkaller to generate inputs matching this interface.10. Review logs and patch vulnerabilities triggered during fuzz tests.
- **Detection**: KASAN logs, GDB debug sessions
- **Solution**: Harden syscall validation and type checking
- **Tags**: kernel, syscall, KASAN, QEMU

## Minimal Alpine Build for Embedded Fuzz Targets

- **Attack Type**: Lightweight Fuzzing Setup
- **Target**: Embedded Parser
- **Vulnerability**: Config File Bugs
- **MITRE**: T1200
- **Impact**: Crash on small IoT config input
- **Tools**: Alpine Linux, musl, clang, AFL++, docker
- **Scenario**: Researcher creates minimal fuzz-ready OS image to test embedded parsers.
- **Attack Steps**: 1. Start from Alpine ISO and install in a VM with 1 CPU/512MB RAM.2. Install clang, cmake, musl-dev, and afl packages.3. Choose a lightweight parsing binary such as libucl or inih.4. Build with afl-clang-fast and sanitize flags.5. Install AFL and test compiled binary with seed config files.6. Write a shell script to restart fuzzing on reboot.7. Schedule the fuzzer to run in a screen session.8. Monitor /proc/meminfo and /tmp/crashes.9. Export crash data over SSH nightly.10. Backup system image weekly using dd for reproducibility.
- **Detection**: AFL crash directory, system logs
- **Solution**: Harden input length and format parser
- **Tags**: Alpine, embedded, AFL, tiny fuzz env

## Honggfuzz for Network Socket-Based Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Network Daemon
- **Vulnerability**: Improper Input Validation
- **MITRE**: T1046
- **Impact**: Remote Crash or Code Execution
- **Tools**: Honggfuzz, netcat, tcpdump
- **Scenario**: Configure Honggfuzz to fuzz a custom TCP server via network socket communication.
- **Attack Steps**: 1. Identify a custom network daemon or lightweight TCP server written in C. 2. Review the source to find how it accepts input (e.g., recv on a socket). 3. Compile the server with ASAN or MSAN for crash detection. 4. Use tcpdump or Wireshark to observe basic communication format. 5. Create a basic fuzz wrapper using Honggfuzz’s --input and --socketFuzzer options. 6. Prepare an initial corpus with a few valid requests (stored in binary or hex). 7. Run Honggfuzz using the network fuzzing mode and log the output. 8. Monitor the server's behavior, inspect crash logs, and review ASAN traces.
- **Detection**: tcpdump, syslog, crash dump review
- **Solution**: Harden input validation, apply firewall rules
- **Tags**: honggfuzz, network, TCP, corpus, ASAN

## WinAFL Setup for Closed-Source Windows Binary

- **Attack Type**: Fuzzer Configuration
- **Target**: Windows Application
- **Vulnerability**: Unchecked Image Parsing
- **MITRE**: T1203
- **Impact**: Application DoS or Exploitation
- **Tools**: WinAFL, DynamoRIO, VirtualBox
- **Scenario**: Configure WinAFL for black-box fuzzing of a proprietary image viewer.
- **Attack Steps**: 1. Select a closed-source Windows image viewer executable (e.g., IrfanView). 2. Set up a Windows 10 VM in VirtualBox with snapshot and rollback enabled. 3. Install WinAFL and its dependencies including DynamoRIO and Visual Studio. 4. Create a small corpus of sample JPEG and PNG files for the fuzzer. 5. Use WinAFL’s winafl.dll and attach it to the binary using DynamoRIO. 6. Choose appropriate instrumentation mode (static or dynamic). 7. Start the fuzzing campaign with input redirection or file drop automation. 8. Revert VM snapshot on crash and collect logs for crash triage.
- **Detection**: Crash dumps, Event Viewer, procmon
- **Solution**: Patch or sandbox the binary
- **Tags**: winafl, closed-source, VirtualBox, corpus

## Dictionary-Based Fuzzing of HTML Parser

- **Attack Type**: Fuzzer Configuration
- **Target**: Parser Library
- **Vulnerability**: HTML Injection Flaws
- **MITRE**: T1592
- **Impact**: Parser Instability or XSS
- **Tools**: AFL++, HTML dictionaries
- **Scenario**: Inject a custom dictionary to improve fuzzing efficiency on HTML parsers.
- **Attack Steps**: 1. Choose an open-source HTML parser (e.g., Gumbo). 2. Compile the target with AFL++ instrumentation (use afl-clang-fast). 3. Collect a small seed corpus with simple HTML files. 4. Create a dictionary file with common HTML tags (<html>, <script>, <body>, etc.). 5. Launch AFL++ with the -x flag to load the dictionary. 6. Monitor input mutation quality and mutation frequency of tag-based payloads. 7. Review crashes and validate if the dictionary improved coverage. 8. Optimize dictionary by removing unused tokens or adding more rare tags.
- **Detection**: AFL coverage maps, crash logs
- **Solution**: Sanitize HTML inputs and validate structure
- **Tags**: afl++, dictionary, html, tags, corpus

## libFuzzer with Argument-Based Fuzzing on CLI Tool

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI Tool
- **Vulnerability**: Argument Parsing Issues
- **MITRE**: T1543
- **Impact**: Incorrect Behavior, DoS
- **Tools**: libFuzzer, LLVM
- **Scenario**: Configure libFuzzer to fuzz command-line arguments passed to a CLI parser.
- **Attack Steps**: 1. Pick a CLI tool (e.g., one that parses flags like --file or --mode). 2. Refactor the entry point into a fuzzable function receiving a char buffer. 3. Compile the code using Clang with libFuzzer support (-fsanitize=fuzzer,address). 4. Write a fuzz target that feeds the buffer into the command parser logic. 5. Create a sample corpus with realistic command-line flag combinations. 6. Launch libFuzzer and pass the corpus directory. 7. Monitor crash output and sanitize argument parsing logic. 8. Repeat with malformed or nested flags.
- **Detection**: Sanitizer logs, fuzz logs
- **Solution**: Harden argument parsing logic
- **Tags**: libfuzzer, cli, arguments, sanitizers

## Fuzzing Image Parser with AFL++ Persistent Mode

- **Attack Type**: Fuzzer Configuration
- **Target**: Image Parser
- **Vulnerability**: Memory Corruption
- **MITRE**: T1203
- **Impact**: Crashes on Malformed Input
- **Tools**: AFL++, libpng
- **Scenario**: Use AFL++ persistent mode to fuzz an image decoding function repeatedly.
- **Attack Steps**: 1. Choose a lightweight image parser (e.g., libpng). 2. Modify the main function to a loop that accepts fuzzed inputs via stdin. 3. Enable persistent mode with __AFL_LOOP(N) in the fuzzing loop. 4. Compile with AFL++ instrumentation. 5. Seed the input folder with a few minimal PNG files. 6. Start AFL++ using afl-fuzz -i in -o out -- ./target. 7. Monitor execution speed and crash detection performance. 8. Analyze if persistent mode yields faster coverage growth.
- **Detection**: AFL stats, sanitizers
- **Solution**: Patch memory access violations
- **Tags**: afl++, persistent, libpng, stdin

## Custom TCP Daemon Fuzzing with libFuzzer

- **Attack Type**: Fuzzer Configuration
- **Target**: Network Service
- **Vulnerability**: Improper Packet Handling
- **MITRE**: T1046
- **Impact**: Input Rejection, Crash
- **Tools**: libFuzzer, TCP server
- **Scenario**: Modify a TCP server to accept fuzzing input via stdin and test with libFuzzer.
- **Attack Steps**: 1. Build a simple TCP daemon that processes input from clients. 2. Refactor the handler function to accept input directly from stdin. 3. Wrap the handler inside a LLVMFuzzerTestOneInput() entry. 4. Compile with Clang and libFuzzer instrumentation. 5. Create a basic corpus of valid TCP packet contents. 6. Run libFuzzer on the binary and monitor crashes. 7. Analyze invalid packet handling logic and log ASAN traces. 8. Improve the input handler to guard against malformed content.
- **Detection**: ASAN, logs, coverage data
- **Solution**: Secure packet parsing routines
- **Tags**: libfuzzer, tcp, stdin, corpus

## Honggfuzz Stdin-Based Mode on Compression Tool

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI Utility
- **Vulnerability**: Memory Exhaustion
- **MITRE**: T1499
- **Impact**: Compression DoS or Corruption
- **Tools**: Honggfuzz, gzip clone
- **Scenario**: Use stdin-based fuzzing on a CLI compression tool using Honggfuzz.
- **Attack Steps**: 1. Select an open-source compression utility that accepts input from stdin. 2. Instrument it with Honggfuzz or recompile for ASAN. 3. Prepare input corpus with common text files and edge cases. 4. Run Honggfuzz with --stdin_input and set crash threshold. 5. Observe crashes and use stack traces to pinpoint logic issues. 6. Examine how special sequences (e.g., 0xFF, 0x00) affect decompression logic. 7. Expand corpus with rare byte sequences to test stability. 8. Triage crashes to eliminate duplicates and confirm exploitability.
- **Detection**: Honggfuzz output, ASAN
- **Solution**: Input length checks, memory limits
- **Tags**: honggfuzz, compression, stdin

## File-Based Dictionary Injection on Media Parser

- **Attack Type**: Fuzzer Configuration
- **Target**: Media Processor
- **Vulnerability**: File Header Issues
- **MITRE**: T1203
- **Impact**: Corrupted Decoding, DoS
- **Tools**: AFL++, ffmpeg
- **Scenario**: Create a dictionary for a media parser (e.g., MP4) and run AFL++.
- **Attack Steps**: 1. Select a media processing tool such as ffmpeg. 2. Compile it with AFL++ instrumentation enabled. 3. Collect a small media corpus (MP4 files with minimal content). 4. Create a dictionary with media-specific bytes (ftyp, moov, mdat). 5. Launch AFL++ using the dictionary with the -x flag. 6. Observe mutation frequency and token effectiveness. 7. Use afl-whatsup to assess progress in coverage. 8. Correlate dictionary use with improved crash discovery.
- **Detection**: AFL++, sanitizer crash reports
- **Solution**: File validation and header checks
- **Tags**: afl++, media, mp4, dictionary

## Network Socket Fuzzing via AFL++ and Proxy

- **Attack Type**: Fuzzer Configuration
- **Target**: Network Binary
- **Vulnerability**: Protocol Parsing Bugs
- **MITRE**: T1046
- **Impact**: Remote Memory Corruption
- **Tools**: AFL++, socat, custom proxy
- **Scenario**: Use AFL++ with a proxy wrapper to fuzz a network binary.
- **Attack Steps**: 1. Identify a network-based program that listens on a port. 2. Create a proxy script or tool (e.g., using socat) to redirect AFL inputs to the target. 3. Configure AFL++ to write mutated inputs to a temp file. 4. The proxy reads that file and sends it to the network binary. 5. Use sanitizers to catch remote crashes on the binary. 6. Log socket responses and crash conditions. 7. Repeat with extended or malformed payloads. 8. Triage logs to identify crash trends.
- **Detection**: socket logs, sanitizer output
- **Solution**: Harden protocol parsing, rate limit
- **Tags**: afl++, network, proxy, socat

## Argument-Based WinAFL on GUI Image Tool

- **Attack Type**: Fuzzer Configuration
- **Target**: Windows GUI Tool
- **Vulnerability**: Input Path Exploits
- **MITRE**: T1203
- **Impact**: Application Crash, Memory Leak
- **Tools**: WinAFL, GUI automation
- **Scenario**: Adapt WinAFL to fuzz GUI image tool via command-line arguments.
- **Attack Steps**: 1. Choose a GUI tool that can also be run with CLI args (e.g., GIMP CLI mode). 2. Wrap the image parsing functionality into a fuzzable driver. 3. Instrument with WinAFL and use DynamoRIO. 4. Create argument templates (e.g., gimp -i --file test.jpg). 5. Generate corpus of malformed image paths or filenames. 6. Use automation script to restart the app between crashes. 7. Monitor Event Viewer and crash logs. 8. Refine argument structures for improved code coverage.
- **Detection**: WinAFL logs, Windows crash logs
- **Solution**: Input path validation
- **Tags**: winafl, gui, arguments, corpus

## Fuzzing PDF Reader with AFL++ Persistent Mode

- **Attack Type**: Fuzzer Configuration
- **Target**: Desktop App
- **Vulnerability**: Input Parsing (PDF)
- **MITRE**: T1203
- **Impact**: App crash, DoS
- **Tools**: AFL++, pdftohtml, qpdf
- **Scenario**: Use AFL++ with persistent mode to fuzz a lightweight PDF reader for crashes.
- **Attack Steps**: 1. Choose a lightweight open-source PDF reader like mupdf. 2. Build the target with AFL++ instrumentation (afl-clang-fast). 3. Enable persistent mode in main loop to avoid process restart overhead. 4. Use afl-cmin to reduce initial seed PDF corpus from fuzzdb. 5. Run fuzzing with afl-fuzz -i seeds -o output -m none -- ./mupdf_afl @@. 6. Monitor crashes in the output/crashes folder. 7. Use qpdf to validate malformed PDFs and isolate root cause. 8. Save VM snapshot before fuzzing.
- **Detection**: Monitor crash count, ASAN output
- **Solution**: Input validation, patch bug
- **Tags**: fuzzer, pdf, afl++, persistent-mode

## Dictionary-Assisted Fuzzing of HTML Parser

- **Attack Type**: Fuzzer Configuration
- **Target**: Web App
- **Vulnerability**: Input Validation
- **MITRE**: T1203
- **Impact**: Unexpected tag injection
- **Tools**: AFL++, lynx, html corpus
- **Scenario**: Use custom dictionary entries to assist AFL++ fuzzing of an HTML parser.
- **Attack Steps**: 1. Select a CLI HTML parser like lynx or a homegrown HTML validator. 2. Compile with afl-clang-fast and ASAN enabled. 3. Prepare a seed corpus of valid HTML files from the W3C or fuzzdb. 4. Create a custom dictionary file containing tags like <script>, <!--, <!DOCTYPE, <img src=, etc. 5. Run AFL++ with dictionary using afl-fuzz -i inputs -o findings -x html.dict -- ./lynx_afl @@. 6. Observe if dictionary helps trigger deeper logic paths. 7. Validate crashes with ASAN output or HTML debug tools.
- **Detection**: HTML structure anomalies
- **Solution**: Harden parser logic
- **Tags**: dictionary, html, afl++, asan

## Network Socket-Based Fuzzing of Custom Daemon

- **Attack Type**: Fuzzer Configuration
- **Target**: Network Daemon
- **Vulnerability**: Socket Input Handling
- **MITRE**: T1210
- **Impact**: Denial of Service, memory corruption
- **Tools**: AFL++, netcat, socat
- **Scenario**: Fuzz a simple TCP daemon by wrapping its stdin with AFL++ input via netcat.
- **Attack Steps**: 1. Create or use an existing simple TCP daemon that reads line-based commands. 2. Refactor the daemon to optionally accept stdin input (for fuzzability). 3. Build the daemon with AFL++ (afl-clang-fast) and enable ASAN. 4. Launch the daemon in forkserver mode or wrap with socat to redirect socket to stdin. 5. Prepare a seed corpus of known commands. 6. Start fuzzing using afl-fuzz -i seeds -o results -- ./fuzzed_daemon @@. 7. Log output using netcat redirection for monitoring. 8. Analyze crash logs with debugger like GDB or gcore.
- **Detection**: Network packet logs, core dump
- **Solution**: Refactor input handler
- **Tags**: network, socket-fuzz, daemon, afl++

## libFuzzer Argument-Based Fuzzing of Image Converter

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI Tool
- **Vulnerability**: Arg Parsing Logic
- **MITRE**: T1203
- **Impact**: CLI tool crash
- **Tools**: libFuzzer, imagemagick-lite
- **Scenario**: Configure libFuzzer to fuzz an image converter tool via argument parsing logic.
- **Attack Steps**: 1. Choose a simple image converter or write one that takes input via command line arguments. 2. Build it with clang -fsanitize=fuzzer,address to integrate libFuzzer. 3. Write a fuzzing harness that calls the parser directly with mutated args. 4. Create a set of argument templates like --resize=WxH --format=png. 5. Run libFuzzer with generated corpus. 6. Investigate output on crash: stack trace and input args. 7. Fine-tune harness to ensure proper code coverage.
- **Detection**: Sanitizer output
- **Solution**: Patch input logic
- **Tags**: libfuzzer, args, image-conversion

## Honggfuzz on Stdin-Based Base64 Decoder

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI App
- **Vulnerability**: Input Decoding
- **MITRE**: T1203
- **Impact**: Base64 parsing failure
- **Tools**: honggfuzz, base64, ASAN
- **Scenario**: Use honggfuzz to fuzz a simple base64 decoder that reads from stdin.
- **Attack Steps**: 1. Write or use an existing base64 decoder that takes stdin as input. 2. Compile with hfuzz-clang with ASAN or MSAN enabled. 3. Prepare a small set of valid base64 strings. 4. Start fuzzing with honggfuzz -f base64_inputs -P -e -n 4 -- ./decoder. 5. Enable persistent mode if supported. 6. Use crash sanitizer logs to identify root cause of any overflow or logic flaw. 7. Optionally use honggfuzz’s built-in crash triage output.
- **Detection**: ASAN/MSAN logs
- **Solution**: Harden decoding function
- **Tags**: honggfuzz, base64, stdin

## Fuzzing with WinAFL on Closed-Source Windows App

- **Attack Type**: Fuzzer Configuration
- **Target**: Windows App
- **Vulnerability**: File Parsing
- **MITRE**: T1203
- **Impact**: Image viewer crash
- **Tools**: WinAFL, DynamoRIO, Windows 10
- **Scenario**: Use WinAFL with DynamoRIO to fuzz a closed-source Windows image viewer.
- **Attack Steps**: 1. Choose a closed-source image viewer with a known file input function. 2. Instrument the application using DynamoRIO and identify the fuzzable function. 3. Prepare a harness DLL that invokes the image decoding logic. 4. Prepare a corpus of small PNG files. 5. Run WinAFL using winafl-fuzz.exe -target_module app.exe -target_method DecodeImage -nargs 1 -fuzz_iterations 100000. 6. Monitor crash logs and stack trace dumps from the Windows Event Viewer or debugger. 7. Use VirtualBox snapshot to roll back VM between crashes.
- **Detection**: Event logs, crash dumps
- **Solution**: Patch decode function
- **Tags**: winafl, windows, closed-source

## Preparing Seed Corpus from Public Dataset

- **Attack Type**: Fuzzer Configuration
- **Target**: Desktop App
- **Vulnerability**: Input Validation
- **MITRE**: T1203
- **Impact**: Parser crash or coverage spike
- **Tools**: AFL++, Open Images, pngtools
- **Scenario**: Build a seed corpus from real-world input files (e.g., PNGs from Open Images dataset).
- **Attack Steps**: 1. Download a small subset of PNG files from Open Images dataset. 2. Use tools like file or pngcheck to verify integrity. 3. Run AFL++’s afl-cmin and afl-tmin to minimize coverage while retaining variety. 4. Ensure each file triggers different code paths in the target parser. 5. Use corpus as -i inputs for AFL++ run. 6. Optionally combine with handcrafted malformed PNGs.
- **Detection**: Fuzzer coverage feedback
- **Solution**: Curate diverse corpus
- **Tags**: png, afl++, dataset, seed-corpus

## Fuzzing Argument-Based PDF to Text Converter

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI Tool
- **Vulnerability**: Arg Parsing & File Handling
- **MITRE**: T1203
- **Impact**: CLI crash on malformed args
- **Tools**: libFuzzer, pdftotext
- **Scenario**: Use argument-based fuzzing to test robustness of a CLI PDF-to-text converter.
- **Attack Steps**: 1. Use or write a wrapper for pdftotext CLI that reads PDF filenames from command-line args. 2. Create a libFuzzer harness that calls the conversion logic with argument strings. 3. Compile with clang -fsanitize=fuzzer,address. 4. Seed with a small corpus of valid filenames and flags like -layout -raw. 5. Run fuzzing and inspect crashes using ASAN and GDB. 6. Modify harness as needed to reach deeper logic branches.
- **Detection**: ASAN log, command error
- **Solution**: Improve CLI parsing
- **Tags**: libfuzzer, pdf, arg-fuzz

## Adding Custom Dictionary for Network Fuzzer

- **Attack Type**: Fuzzer Configuration
- **Target**: Network Daemon
- **Vulnerability**: Protocol Handling
- **MITRE**: T1210
- **Impact**: Logic flaw, bypass auth
- **Tools**: AFL++, FTP fuzzer, custom dict
- **Scenario**: Improve mutation depth in a network protocol fuzzer by adding known keywords.
- **Attack Steps**: 1. Identify common FTP command tokens like USER, PASS, LIST, RETR, etc. 2. Add these as dictionary entries in a ftp.dict file. 3. Use a CLI or socket-based FTP command parser as the fuzz target. 4. Compile with AFL++. 5. Launch fuzzing with afl-fuzz -i seeds -o results -x ftp.dict -- ./ftp_target @@. 6. Check if keyword reuse triggers deeper logic or malformed command bugs.
- **Detection**: Protocol parser logs
- **Solution**: Add strict token checks
- **Tags**: ftp, dictionary, protocol-fuzz

## Headless Fuzzing of CLI Audio Tool with AFL++

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI Tool
- **Vulnerability**: Audio Format Handling
- **MITRE**: T1203
- **Impact**: Crash or data loss
- **Tools**: AFL++, ffmpeg-lite, ogg corpus
- **Scenario**: Use AFL++ in headless mode to fuzz an audio file converter without GUI overhead.
- **Attack Steps**: 1. Choose or compile a version of ffmpeg without GUI dependencies. 2. Prepare a seed corpus of small .ogg files. 3. Run in headless mode using afl-fuzz -i ogg_inputs -o findings -- ./ffmpeg_afl -i @@ -f wav out.wav. 4. Use ASAN and MSAN for memory bug detection. 5. Record crashes and correlate with audio parsing routines.
- **Detection**: MSAN trace, audio diff
- **Solution**: Improve decoder validation
- **Tags**: ffmpeg, audio, afl++, headless

## AFL++ Fuzzing of Windows PE File Parser with Custom Dictionary

- **Attack Type**: Fuzzer Configuration
- **Target**: Windows Binary
- **Vulnerability**: File parsing bug
- **MITRE**: T1203
- **Impact**: Application crash, memory corruption
- **Tools**: AFL++, Windows PE tools
- **Scenario**: Using AFL++ to fuzz a Windows Portable Executable (PE) file parser with dictionary support for common PE headers.
- **Attack Steps**: 1. Select or build a PE file parser on Windows. 2. Compile with AFL++ instrumentation and ASAN enabled. 3. Create a dictionary with PE-specific byte patterns such as MZ, PE\0\0, and section headers. 4. Prepare a seed corpus of minimal valid PE files. 5. Launch AFL++ with dictionary support via -x flag. 6. Monitor mutation effectiveness on PE structure. 7. Collect crash inputs for triage and root cause analysis. 8. Patch memory handling or header validation bugs found.
- **Detection**: Crash dump analysis, ASAN logs
- **Solution**: Harden PE parsing routines
- **Tags**: afl++, PE, dictionary, windows

## libFuzzer-Based Fuzzing of JSON Parser Arguments

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI Tool
- **Vulnerability**: Arg parsing vulnerability
- **MITRE**: T1203
- **Impact**: Memory crash, incorrect parsing
- **Tools**: libFuzzer, JSON parser
- **Scenario**: Configuring libFuzzer to fuzz argument parsing in a JSON command-line tool.
- **Attack Steps**: 1. Use a JSON parser tool accepting arguments or config files. 2. Wrap argument parsing logic in a libFuzzer test harness. 3. Compile with -fsanitize=fuzzer,address. 4. Create seed inputs with valid JSON command-line options. 5. Run libFuzzer to mutate argument values. 6. Detect crashes or memory corruption from invalid inputs. 7. Debug issues using sanitizer outputs. 8. Update parser logic to better validate inputs.
- **Detection**: Sanitizer logs, fuzz outputs
- **Solution**: Harden argument validation
- **Tags**: libfuzzer, JSON, argument fuzzing

## Using AFLnet to Fuzz FTP Server Commands with Custom Seed Corpus

- **Attack Type**: Fuzzer Configuration
- **Target**: Network Service
- **Vulnerability**: Protocol parsing
- **MITRE**: T1210
- **Impact**: Server crash or DoS
- **Tools**: AFLnet, FTP server
- **Scenario**: Fuzzing FTP server by sending mutated commands with AFLnet’s network fuzzing capabilities.
- **Attack Steps**: 1. Deploy an FTP server supporting basic commands. 2. Prepare a corpus of valid FTP commands (USER, PASS, LIST, etc.). 3. Setup AFLnet with appropriate protocol state machine configuration. 4. Enable AFLnet’s persistent fuzzing mode to reuse connections. 5. Launch AFLnet with corpus and monitor network traffic via Wireshark. 6. Record any server crashes or memory leaks during fuzzing. 7. Analyze crash logs and attempt to reproduce with minimal input. 8. Apply fixes to command parsing routines.
- **Detection**: Network logs, crash dump
- **Solution**: Harden FTP command parser
- **Tags**: AFLnet, FTP, network fuzzing

## Dictionary-Enhanced Fuzzing of Audio Metadata Parser

- **Attack Type**: Fuzzer Configuration
- **Target**: Media Processor
- **Vulnerability**: Metadata parsing flaws
- **MITRE**: T1203
- **Impact**: Audio tool crashes
- **Tools**: AFL++, FFmpeg
- **Scenario**: Use dictionaries with AFL++ to fuzz audio metadata parsing code for bugs.
- **Attack Steps**: 1. Select audio metadata parser (e.g., FFmpeg). 2. Build with AFL++ instrumentation. 3. Create a dictionary including common audio tags (ID3, TIT2, TPE1). 4. Seed with valid audio files with minimal metadata. 5. Launch AFL++ with dictionary enabled. 6. Monitor for crashes caused by malformed metadata. 7. Triage crashes and isolate vulnerable code paths. 8. Fix parsing issues in metadata handlers.
- **Detection**: ASAN logs, AFL++ stats
- **Solution**: Validate metadata fields
- **Tags**: afl++, audio, dictionary

## Network Fuzzing of Custom IoT Protocol Using AFLnet

- **Attack Type**: Fuzzer Configuration
- **Target**: Network Service
- **Vulnerability**: Protocol fuzzing
- **MITRE**: T1046
- **Impact**: Device DoS or takeover
- **Tools**: AFLnet, IoT device simulator
- **Scenario**: Fuzzing an IoT device’s proprietary TCP protocol using AFLnet.
- **Attack Steps**: 1. Develop a TCP server simulating an IoT device. 2. Define protocol messages and commands. 3. Prepare AFLnet with proper setup for protocol state. 4. Use seed corpus with minimal valid commands. 5. Run AFLnet with network replay and fuzzing enabled. 6. Monitor device simulator for crashes or hangs. 7. Analyze memory dumps and debug crashes. 8. Patch protocol parser vulnerabilities.
- **Detection**: Device logs, AFLnet crash data
- **Solution**: Harden protocol parsing
- **Tags**: AFLnet, IoT, network fuzzing

## Persistent Mode Fuzzing of Linux Kernel Module Using Syzkaller

- **Attack Type**: Kernel Fuzzing
- **Target**: Kernel
- **Vulnerability**: Memory corruption in kernel
- **MITRE**: T1211
- **Impact**: Kernel panic or escalation
- **Tools**: Syzkaller, QEMU, Kernel module
- **Scenario**: Using Syzkaller to fuzz a custom Linux kernel module in persistent mode.
- **Attack Steps**: 1. Setup QEMU VM with Linux kernel including target module. 2. Build kernel with debugging and fuzzer instrumentation. 3. Configure Syzkaller with syscall descriptions for module APIs. 4. Prepare Syzkaller with persistent fuzzing enabled. 5. Launch fuzzing campaign with persistent mode active. 6. Monitor kernel logs and OOPS reports. 7. Capture and triage crashes caused by malformed syscalls. 8. Fix memory corruption or privilege escalation bugs.
- **Detection**: Kernel logs, OOPS reports
- **Solution**: Patch kernel module
- **Tags**: Syzkaller, kernel, persistent

## Setting up AFL++ with Dictionary for File Format Fuzzing

- **Attack Type**: File Format Fuzzing
- **Target**: File Parser
- **Vulnerability**: XML parsing flaws
- **MITRE**: T1203
- **Impact**: Application crashes
- **Tools**: AFL++, DOCX tools
- **Scenario**: Using a dictionary to improve AFL++ fuzzing for complex file formats like DOCX.
- **Attack Steps**: 1. Choose a DOCX parser as target. 2. Build with AFL++ instrumentation and sanitizers. 3. Analyze DOCX XML structure to extract tokens and tags. 4. Create a dictionary file with XML tags, attributes, and common keywords. 5. Prepare a seed corpus of minimal DOCX files. 6. Launch AFL++ with dictionary enabled via -x flag. 7. Track mutation effectiveness and crashes. 8. Triage any bugs related to XML parsing.
- **Detection**: ASAN logs, AFL stats
- **Solution**: Harden XML parser
- **Tags**: afl++, docx, dictionary

## libFuzzer Argument-Based Fuzzing of Network Configuration CLI

- **Attack Type**: CLI Argument Fuzzing
- **Target**: CLI Tool
- **Vulnerability**: Arg parsing vulnerability
- **MITRE**: T1203
- **Impact**: Crash, DoS
- **Tools**: libFuzzer, CLI tools
- **Scenario**: Using libFuzzer to fuzz argument parsing in network configuration tools.
- **Attack Steps**: 1. Select a network CLI tool accepting complex arguments. 2. Extract argument parsing code into a fuzzable function. 3. Compile with libFuzzer and address sanitizer. 4. Seed with common network config arguments (e.g., IP, subnet masks). 5. Run libFuzzer to mutate arguments and flags. 6. Monitor for parsing errors or memory faults. 7. Debug crashes using sanitizer outputs. 8. Harden argument parsing to reject malformed inputs.
- **Detection**: Crash logs, sanitizer reports
- **Solution**: Improve input validation
- **Tags**: libFuzzer, CLI, argument fuzzing

## AFLnet Fuzzing of Custom HTTP Server

- **Attack Type**: Protocol Fuzzing
- **Target**: Network Service
- **Vulnerability**: HTTP request parsing
- **MITRE**: T1203
- **Impact**: Server crash or injection
- **Tools**: AFLnet, HTTP server
- **Scenario**: Fuzzing an HTTP server’s request parser with AFLnet protocol-aware fuzzing.
- **Attack Steps**: 1. Develop or select an HTTP server for fuzzing. 2. Setup AFLnet with HTTP protocol state machine. 3. Prepare seed corpus of minimal valid HTTP requests. 4. Run AFLnet to fuzz headers and payloads. 5. Monitor server for crashes or protocol misinterpretation. 6. Log crash inputs and stack traces. 7. Analyze input fields causing failure. 8. Patch HTTP parser vulnerabilities.
- **Detection**: Network logs, crash dumps
- **Solution**: Harden HTTP parser
- **Tags**: AFLnet, HTTP, fuzzing

## Using honggfuzz on Image Decoder with Corpus Minimization

- **Attack Type**: Corpus Minimization
- **Target**: Desktop App
- **Vulnerability**: Memory corruption
- **MITRE**: T1203
- **Impact**: Crash, DoS
- **Tools**: honggfuzz, image decoder
- **Scenario**: Running honggfuzz on an image decoder with minimized corpus for efficient fuzzing.
- **Attack Steps**: 1. Select an image decoding library or tool. 2. Prepare a seed corpus of diverse image files. 3. Use honggfuzz’s corpus minimization utilities to reduce corpus size while maintaining coverage. 4. Compile decoder with honggfuzz instrumentation and sanitizers. 5. Launch fuzzing with minimized corpus. 6. Monitor crash rates and coverage metrics. 7. Triage crashing inputs with sanitizer logs. 8. Fix issues in image decoding routines.
- **Detection**: Sanitizer logs, honggfuzz output
- **Solution**: Harden decoding logic
- **Tags**: honggfuzz, corpus, minimization

## Custom Dictionary for Video File Fuzzing with AFL++

- **Attack Type**: Dictionary Fuzzing
- **Target**: Media Parser
- **Vulnerability**: File format vulnerability
- **MITRE**: T1203
- **Impact**: Crash or DoS
- **Tools**: AFL++, video parser
- **Scenario**: Enhancing AFL++ fuzzing on video file parsers with a video-specific dictionary.
- **Attack Steps**: 1. Choose a video parser such as for MP4 or AVI. 2. Analyze file format headers and metadata keys. 3. Create a dictionary file with common tokens (mdat, moov, trak). 4. Build the parser with AFL++ instrumentation. 5. Seed with minimal valid video files. 6. Run AFL++ with dictionary support. 7. Monitor for crashes caused by malformed headers. 8. Patch input handling vulnerabilities.
- **Detection**: AFL crash logs, sanitizer output
- **Solution**: Validate file headers
- **Tags**: afl++, video, dictionary

## libFuzzer Argument Fuzzing on Audio CLI Tool

- **Attack Type**: Argument-Based Fuzzing
- **Target**: CLI Tool
- **Vulnerability**: Argument parsing
- **MITRE**: T1203
- **Impact**: Crash or incorrect parsing
- **Tools**: libFuzzer, audio tool
- **Scenario**: Using libFuzzer to fuzz CLI audio conversion tool argument parsing.
- **Attack Steps**: 1. Select an audio CLI tool (e.g., SoX). 2. Refactor argument parsing to expose fuzz target. 3. Compile with libFuzzer and address sanitizer. 4. Create seed corpus of common argument combinations. 5. Launch fuzzing campaign. 6. Monitor for invalid argument handling or crashes. 7. Debug with sanitizer output. 8. Harden parsing logic for edge cases.
- **Detection**: Sanitizer logs, fuzz logs
- **Solution**: Improve argument validation
- **Tags**: libFuzzer, audio, argument fuzzing

## AFL++ Fuzzing of Network Daemon with Socket Replay

- **Attack Type**: Network Fuzzing
- **Target**: Network Daemon
- **Vulnerability**: Input validation flaw
- **MITRE**: T1046
- **Impact**: DoS or memory corruption
- **Tools**: AFL++, socat, network daemon
- **Scenario**: Using AFL++ with socket replay proxy to fuzz a network daemon.
- **Attack Steps**: 1. Identify a network daemon with socket input. 2. Create a proxy script to relay AFL mutated inputs to socket. 3. Compile daemon with AFL++ instrumentation and sanitizers. 4. Prepare corpus of valid network packets. 5. Run AFL++ with proxy setup. 6. Monitor for crashes and analyze logs. 7. Replay crashing inputs manually for debugging. 8. Fix input validation flaws in daemon.
- **Detection**: Crash dumps, sanitizer logs
- **Solution**: Harden network input handling
- **Tags**: afl++, network, proxy

## Honggfuzz Fuzzing of Compression Utility Stdin

- **Attack Type**: Stdin-Based Fuzzing
- **Target**: CLI Utility
- **Vulnerability**: Memory corruption
- **MITRE**: T1203
- **Impact**: Crash or data loss
- **Tools**: honggfuzz, compression utility
- **Scenario**: Using honggfuzz to fuzz stdin input of a compression CLI tool.
- **Attack Steps**: 1. Select a compression utility supporting stdin input. 2. Instrument the binary with honggfuzz. 3. Prepare seed corpus with minimal valid compressed data. 4. Launch honggfuzz in stdin mode. 5. Monitor crashes caused by malformed compression streams. 6. Analyze sanitizer and debug logs. 7. Reproduce crashes and isolate root cause. 8. Harden decompression logic.
- **Detection**: Sanitizer logs, crash reports
- **Solution**: Improve decompression safety
- **Tags**: honggfuzz, compression, stdin

## Dictionary-Driven Fuzzing of XML Parsers

- **Attack Type**: Dictionary Fuzzing
- **Target**: File Parser
- **Vulnerability**: XML parsing vulnerability
- **MITRE**: T1203
- **Impact**: Crash or injection
- **Tools**: AFL++, XML parser
- **Scenario**: Enhancing AFL++ fuzzing of XML parsers by injecting common XML tokens.
- **Attack Steps**: 1. Choose an XML parser as target (e.g., libxml2). 2. Instrument with AFL++ and compile with sanitizers. 3. Create dictionary with XML tags (<tag>, </tag>, xmlns). 4. Prepare seed corpus with minimal XML files. 5. Run AFL++ with dictionary enabled. 6. Monitor crashes and coverage. 7. Triage crashing inputs and patch parser flaws. 8. Harden XML parsing logic.
- **Detection**: AFL stats, sanitizer logs
- **Solution**: Input validation
- **Tags**: afl++, xml, dictionary

## libFuzzer Argument-Based Fuzzing on JSON CLI Tool

- **Attack Type**: Argument Parsing
- **Target**: CLI Tool
- **Vulnerability**: Argument parsing flaw
- **MITRE**: T1203
- **Impact**: Crash or unexpected output
- **Tools**: libFuzzer, JSON parser
- **Scenario**: Using libFuzzer to fuzz arguments of JSON CLI utility.
- **Attack Steps**: 1. Select a JSON CLI tool with argument-based parsing. 2. Expose argument parser to fuzz target. 3. Compile with libFuzzer and address sanitizer. 4. Seed corpus with JSON configs and options. 5. Launch fuzzing campaign. 6. Monitor for crashes or misbehaviors. 7. Analyze sanitizer logs for input errors. 8. Harden parser logic for malformed args.
- **Detection**: Sanitizer reports
- **Solution**: Input validation
- **Tags**: libFuzzer, JSON, arguments

## AFLnet Fuzzing of SMTP Server Protocol Commands

- **Attack Type**: Protocol Fuzzing
- **Target**: Network Service
- **Vulnerability**: Protocol handling flaw
- **MITRE**: T1210
- **Impact**: Server crash or message injection
- **Tools**: AFLnet, SMTP server
- **Scenario**: Using AFLnet to fuzz SMTP server command handling and state machine.
- **Attack Steps**: 1. Setup a minimal SMTP server supporting basic commands. 2. Prepare seed corpus of SMTP commands (HELO, MAIL FROM, RCPT TO). 3. Configure AFLnet with SMTP state machine. 4. Enable persistent fuzzing and retries. 5. Launch fuzzing and monitor logs for crashes or hangs. 6. Capture inputs causing protocol errors. 7. Analyze server crash dumps. 8. Patch protocol parser for robustness.
- **Detection**: Crash logs, network captures
- **Solution**: Harden SMTP parser
- **Tags**: AFLnet, SMTP, protocol fuzzing

## Using honggfuzz Corpus Minimization on Audio Decoder

- **Attack Type**: Corpus Minimization
- **Target**: Desktop App
- **Vulnerability**: Memory corruption
- **MITRE**: T1203
- **Impact**: Crash, DoS
- **Tools**: honggfuzz, audio decoder
- **Scenario**: Minimizing corpus size while fuzzing audio decoder using honggfuzz tools.
- **Attack Steps**: 1. Select audio decoder as target. 2. Prepare large seed corpus of audio files. 3. Use honggfuzz corpus minimization utility. 4. Compile decoder with honggfuzz instrumentation. 5. Run fuzzing with minimized corpus. 6. Monitor coverage and crashes. 7. Triage crash-inducing inputs. 8. Patch decoding bugs.
- **Detection**: Sanitizer logs
- **Solution**: Harden decoding routines
- **Tags**: honggfuzz, corpus minimization

## Dictionary-Assisted Fuzzing of Video Container Parsers

- **Attack Type**: Dictionary Fuzzing
- **Target**: Media Parser
- **Vulnerability**: File format bug
- **MITRE**: T1203
- **Impact**: Crash or corruption
- **Tools**: AFL++, MKV parser
- **Scenario**: Using dictionaries to improve fuzzing of video container parsers like MKV.
- **Attack Steps**: 1. Select MKV parser as target. 2. Create dictionary with EBML tags common to MKV files. 3. Seed corpus with minimal MKV files. 4. Compile with AFL++ instrumentation. 5. Launch AFL++ with dictionary support. 6. Monitor for crashes in header parsing. 7. Triage and fix input handling bugs. 8. Harden file header parsing logic.
- **Detection**: AFL logs, sanitizer reports
- **Solution**: Input validation
- **Tags**: afl++, video, dictionary

## libFuzzer Argument-Based Fuzzing on Network Config CLI Tool

- **Attack Type**: Argument Fuzzing
- **Target**: CLI Tool
- **Vulnerability**: Arg parsing flaw
- **MITRE**: T1203
- **Impact**: Crash or incorrect config
- **Tools**: libFuzzer, CLI tool
- **Scenario**: Using libFuzzer to fuzz argument parsing in network configuration tools.
- **Attack Steps**: 1. Select network CLI with complex argument parsing. 2. Extract argument parser for fuzzing. 3. Compile with libFuzzer and ASAN. 4. Seed with common network configs. 5. Launch fuzzing campaign. 6. Detect crashes and invalid parsing. 7. Debug sanitizer outputs. 8. Harden argument validation.
- **Detection**: Sanitizer logs
- **Solution**: Improve input validation
- **Tags**: libFuzzer, CLI, argument fuzzing

## Configuring AFL++ for File-Based Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: File parsers
- **Vulnerability**: Memory corruption, buffer overflow
- **MITRE**: T1201 (Input Capture)
- **Impact**: Potential crash or RCE from malformed files
- **Tools**: AFL++
- **Scenario**: Setting up AFL++ to fuzz file input parsers by preparing seed corpus and tuning instrumentation for improved coverage.
- **Attack Steps**: 1. Install AFL++ on your fuzzing environment (Linux recommended). 2. Prepare a seed corpus by collecting valid sample input files (e.g., PDFs, images). 3. Compile the target binary with AFL++ instrumentation enabled using afl-gcc or afl-clang-fast. 4. Configure AFL++ to run in file-based fuzzing mode, specifying input and output directories. 5. Optionally, enable persistent mode to reduce overhead. 6. Start AFL++ and monitor code coverage to ensure instrumentation is effective. 7. Review AFL++ logs and crashes found for further analysis. 8. Adjust fuzzing parameters such as timeout and mutation ratio as needed to improve fuzzing efficiency.
- **Detection**: AFL++ coverage reports, crash logs
- **Solution**: Patch vulnerable code, sanitize inputs
- **Tags**: fuzzing, AFL++, instrumentation, file-based

## Setting up libFuzzer for Argument-Based Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI applications
- **Vulnerability**: Input validation flaws
- **MITRE**: T1201
- **Impact**: Denial of Service, crash, or RCE
- **Tools**: libFuzzer
- **Scenario**: Configuring libFuzzer to fuzz functions receiving command-line arguments by preparing custom harness and seed inputs.
- **Attack Steps**: 1. Integrate libFuzzer into the target application’s codebase by adding fuzz targets as function wrappers. 2. Write a fuzzing harness that converts fuzzer input into command-line arguments. 3. Prepare a seed corpus of typical command-line argument combinations. 4. Compile the application with sanitizer support (ASAN) and libFuzzer enabled. 5. Run the fuzzer and monitor for crashes, hangs, or unexpected behavior. 6. Analyze sanitizer output to identify root cause of detected bugs. 7. Refine fuzz target and corpus based on initial findings. 8. Iterate fuzzing to increase code coverage and discover additional bugs.
- **Detection**: Sanitizer reports, libFuzzer logs
- **Solution**: Fix input parsing logic, add validation
- **Tags**: fuzzing, libFuzzer, command-line, sanitizers

## Using Honggfuzz with Stdin-Based Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI tools
- **Vulnerability**: Buffer overflow, use-after-free
- **MITRE**: T1201
- **Impact**: Application crash or memory corruption
- **Tools**: Honggfuzz
- **Scenario**: Configuring Honggfuzz to fuzz applications reading input from standard input by preparing stdin seeds and adjusting timeout parameters.
- **Attack Steps**: 1. Download and install Honggfuzz on your system. 2. Identify the target application’s input mode (stdin). 3. Collect valid stdin input samples as seed corpus. 4. Prepare dictionary file if specific tokens or magic bytes are needed. 5. Launch Honggfuzz specifying the stdin fuzzing mode and providing the corpus directory. 6. Configure timeout, memory limits, and crash logging options. 7. Monitor execution and coverage stats using built-in dashboards or logs. 8. Triage crashes and analyze with debugger or sanitizer tools. 9. Refine corpus and dictionary to focus on critical input areas.
- **Detection**: Honggfuzz logs, sanitizer alerts
- **Solution**: Apply patches, enhance input validation
- **Tags**: fuzzing, honggfuzz, stdin, instrumentation

## Configuring WinAFL for Network Socket-Based Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Network services
- **Vulnerability**: Protocol parsing flaws
- **MITRE**: T1574 (Hijack Execution Flow)
- **Impact**: Service crash, memory corruption, RCE
- **Tools**: WinAFL
- **Scenario**: Setting up WinAFL to fuzz network services by instrumenting binaries and configuring socket communication fuzzing mode.
- **Attack Steps**: 1. Install WinAFL on a Windows system with debugger support (e.g., WinDbg). 2. Instrument the target network service executable with DynamoRIO and WinAFL. 3. Identify the network socket interface and protocol used. 4. Create or capture valid network packets to form the seed corpus. 5. Configure WinAFL to fuzz via socket-based input delivery, specifying target address and port. 6. Set fuzzing parameters including timeout and mutator options. 7. Start fuzzing and monitor coverage and crash output logs. 8. Use debugger integration to analyze crashes in real-time. 9. Iterate corpus based on findings to increase coverage.
- **Detection**: WinAFL crash logs, debugger output
- **Solution**: Patch parsing code, validate network input
- **Tags**: fuzzing, WinAFL, network sockets, Windows

## Preparing Seed Corpus for Image File Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Image parsers
- **Vulnerability**: Memory corruption, integer overflow
- **MITRE**: T1201
- **Impact**: Improved fuzzing efficiency, higher code coverage
- **Tools**: AFL++, libFuzzer
- **Scenario**: Collecting and curating a diverse seed corpus of valid image files to maximize mutation effectiveness during fuzzing.
- **Attack Steps**: 1. Identify image formats supported by the target application (JPEG, PNG, BMP). 2. Gather a large set of valid images covering diverse properties (sizes, compression levels). 3. Remove any corrupted or invalid files from the corpus. 4. Organize corpus into folders accessible by the fuzzer. 5. Optionally preprocess images to standardize metadata or format variations. 6. Test the corpus by running a short fuzzing session and verifying no crashes from valid inputs. 7. Update corpus continuously by adding newly discovered valid inputs. 8. Use corpus minimization tools to reduce redundancy without losing coverage. 9. Document corpus preparation process for reproducibility.
- **Detection**: Fuzzer coverage reports
- **Solution**: Ensure corpus validity, patch parsing bugs
- **Tags**: fuzzing, seed corpus, image formats

## Creating Custom Dictionary for PDF Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: PDF parsers
- **Vulnerability**: Input validation flaws
- **MITRE**: T1201
- **Impact**: Increased crash discovery rate and coverage
- **Tools**: AFL++, libFuzzer
- **Scenario**: Building a dictionary containing PDF-specific tokens and magic bytes to improve fuzzing efficiency and trigger deeper code paths.
- **Attack Steps**: 1. Analyze the PDF file format specification and common PDF tokens. 2. Extract commonly used keywords and magic bytes (e.g., %PDF-, /Obj, /Length). 3. Format these tokens into dictionary entries per fuzzer requirements. 4. Integrate dictionary file into fuzzer configuration. 5. Run fuzzing with dictionary enabled to observe increased mutation relevance. 6. Monitor code coverage and crashes to assess dictionary impact. 7. Refine dictionary by adding or removing tokens based on fuzzing results. 8. Share dictionary for community reuse and improvement. 9. Repeat dictionary updates as new PDF features are targeted.
- **Detection**: Fuzzer logs, coverage reports
- **Solution**: Patch parser logic, validate inputs thoroughly
- **Tags**: fuzzing, dictionary, PDF, magic bytes

## Selecting Fuzzing Mode for Multimedia Applications

- **Attack Type**: Fuzzer Configuration
- **Target**: Multimedia apps
- **Vulnerability**: Buffer overflow, use-after-free
- **MITRE**: T1201
- **Impact**: Discovery of input handling bugs
- **Tools**: AFL++, libFuzzer, Honggfuzz
- **Scenario**: Choosing appropriate fuzzing mode (file, argument, stdin) based on multimedia app input mechanisms to maximize fuzzing impact.
- **Attack Steps**: 1. Analyze target multimedia application’s input interfaces (file open dialogs, command line options, streaming input). 2. Identify the most accessible and controllable input method for fuzzing. 3. Configure the fuzzer to operate in the selected mode. 4. Prepare seed corpus or arguments matching input format. 5. Test initial fuzzing runs to validate mode selection. 6. Monitor coverage and crashes to confirm efficacy. 7. Switch fuzzing mode if necessary based on findings. 8. Document mode choice rationale and configuration settings.
- **Detection**: Fuzzer logs, coverage stats
- **Solution**: Patch vulnerable input handlers
- **Tags**: fuzzing, mode selection, multimedia

## Using Dictionary Setup to Fuzz Protocol Parsers

- **Attack Type**: Fuzzer Configuration
- **Target**: Network parsers
- **Vulnerability**: Protocol parsing flaws
- **MITRE**: T1574
- **Impact**: Protocol handler crashes, memory corruption
- **Tools**: AFL++, Honggfuzz
- **Scenario**: Enhancing fuzzing of protocol parsers by creating dictionaries with protocol keywords and command patterns.
- **Attack Steps**: 1. Study the target network protocol specification to identify keywords and command tokens. 2. Extract these tokens into dictionary entries compatible with your fuzzer. 3. Include known magic bytes or delimiter sequences. 4. Add the dictionary to the fuzzing configuration. 5. Launch the fuzzer targeting the protocol parser with the dictionary enabled. 6. Monitor fuzzing progress for increased code coverage and bug discovery. 7. Analyze crashes and refine dictionary entries based on fuzzing feedback. 8. Repeat the process to keep dictionary updated as protocol evolves.
- **Detection**: Fuzzer crash logs, network traces
- **Solution**: Patch parsing routines, validate input data
- **Tags**: fuzzing, dictionary, protocol, network

## Preparing Seed Corpus for HTML Parsers

- **Attack Type**: Fuzzer Configuration
- **Target**: HTML parsers
- **Vulnerability**: Memory corruption, input validation flaws
- **MITRE**: T1201
- **Impact**: Higher mutation effectiveness and crash discovery
- **Tools**: libFuzzer, AFL++
- **Scenario**: Collecting a variety of valid HTML files with different tags and structures to serve as a seed corpus for fuzzing HTML parsers.
- **Attack Steps**: 1. Gather HTML files from diverse sources with varied complexity. 2. Validate collected HTML files to ensure they parse without errors. 3. Remove duplicates or corrupted files. 4. Organize corpus for easy fuzzer access. 5. Run a short fuzzing session to confirm seed corpus validity. 6. Enhance corpus by adding edge cases such as malformed tags or unusual attribute values. 7. Continuously update corpus with newly found valid inputs. 8. Utilize corpus minimization to reduce size while maintaining coverage.
- **Detection**: Fuzzer coverage reports
- **Solution**: Patch vulnerabilities, improve parser resilience
- **Tags**: fuzzing, seed corpus, HTML, web

## Configuring Timeout and Memory Limits in Fuzzers

- **Attack Type**: Fuzzer Configuration
- **Target**: Any fuzz target
- **Vulnerability**: Denial of Service, infinite loop
- **MITRE**: T1499
- **Impact**: Improved fuzzing efficiency and stability
- **Tools**: AFL++, libFuzzer, Honggfuzz
- **Scenario**: Optimizing fuzzing runs by adjusting timeout and memory usage limits to prevent hangs and crashes unrelated to target bugs.
- **Attack Steps**: 1. Identify resource constraints of the fuzzing environment. 2. Configure per-test-case timeout to avoid infinite loops or hangs. 3. Set memory limits to prevent excessive resource consumption. 4. Run test fuzzing sessions to observe resource usage and stability. 5. Adjust limits iteratively based on performance and crash analysis. 6. Monitor fuzzing dashboard to detect timeouts or out-of-memory errors. 7. Use sanitizer tools to confirm crashes are due to genuine bugs. 8. Document configuration parameters for repeatability.
- **Detection**: Fuzzer logs, resource monitoring tools
- **Solution**: Refine code to avoid resource exhaustion
- **Tags**: fuzzing, performance tuning, timeout, memory

## Integrating Sanitizers with AFL++

- **Attack Type**: Fuzzer Configuration
- **Target**: Application binaries
- **Vulnerability**: Use-after-free, buffer overflow
- **MITRE**: T1201
- **Impact**: Memory corruption leading to crash or exploit
- **Tools**: AFL++, ASAN
- **Scenario**: Enhancing AFL++ fuzzing by combining AddressSanitizer (ASAN) to detect memory errors during fuzz runs.
- **Attack Steps**: 1. Install and configure AddressSanitizer with your compiler toolchain. 2. Compile the target application with both AFL++ instrumentation and ASAN enabled. 3. Prepare the seed corpus with valid inputs relevant to the target. 4. Start AFL++ fuzzing with ASAN monitoring runtime memory safety errors. 5. Analyze ASAN reports for use-after-free, buffer overflow, and other memory bugs. 6. Investigate crashes reported by AFL++ for detailed bug triage. 7. Refine seed corpus and dictionary for focused fuzzing. 8. Repeat fuzzing to discover additional vulnerabilities.
- **Detection**: ASAN error reports, AFL++ logs
- **Solution**: Patch memory management issues, improve validation
- **Tags**: fuzzing, AFL++, ASAN, memory safety

## Preparing Network Packet Seeds for WinAFL

- **Attack Type**: Fuzzer Configuration
- **Target**: Network services
- **Vulnerability**: Protocol parsing errors
- **MITRE**: T1574
- **Impact**: Service crashes or remote code execution
- **Tools**: WinAFL
- **Scenario**: Creating and capturing valid network packet sequences as seeds for fuzzing a network service with WinAFL.
- **Attack Steps**: 1. Identify the protocol used by the target network service. 2. Use packet capture tools (Wireshark, tcpdump) to record valid traffic sessions. 3. Extract relevant packet payloads and store them as seed inputs. 4. Validate extracted packets for correctness and protocol compliance. 5. Format seeds in a directory accessible by WinAFL. 6. Configure WinAFL with these seeds and specify network socket fuzzing mode. 7. Begin fuzzing and monitor for crashes and coverage improvements. 8. Use debugger or sanitizer tools to analyze crashes. 9. Update seed corpus with new packets discovered or crafted.
- **Detection**: Packet capture analysis, debugger output
- **Solution**: Fix parser bugs, enforce protocol validation
- **Tags**: fuzzing, WinAFL, network packets, protocol

## Automated Seed Corpus Minimization

- **Attack Type**: Fuzzer Configuration
- **Target**: Any fuzz target
- **Vulnerability**: Input validation flaws
- **MITRE**: T1201
- **Impact**: Faster fuzzing cycles with retained bug detection
- **Tools**: AFL++, libFuzzer
- **Scenario**: Using corpus minimization tools to reduce seed corpus size without losing code coverage and fuzzing effectiveness.
- **Attack Steps**: 1. Collect a large initial seed corpus of valid inputs. 2. Run fuzzing sessions to identify seeds that trigger unique code paths. 3. Use tools like afl-cmin or libFuzzer’s corpus reduction features to remove redundant seeds. 4. Verify minimized corpus still achieves required coverage. 5. Document minimization steps for reproducibility. 6. Periodically re-run minimization as corpus grows. 7. Maintain balance between corpus size and coverage for optimal fuzzing speed. 8. Backup original corpus before minimization for fallback.
- **Detection**: Coverage reports, fuzzing logs
- **Solution**: Maintain corpus quality, update seeds regularly
- **Tags**: fuzzing, corpus minimization, seed optimization

## Creating Custom Seed Generators for libFuzzer

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI applications
- **Vulnerability**: Input parsing errors
- **MITRE**: T1201
- **Impact**: Increased mutation diversity and bug coverage
- **Tools**: libFuzzer
- **Scenario**: Writing code to generate seed inputs dynamically for libFuzzer, focusing on argument-based fuzzing scenarios.
- **Attack Steps**: 1. Understand the target function’s input structure. 2. Write a custom seed generator in the fuzz target code to produce valid inputs programmatically. 3. Integrate generator with libFuzzer harness. 4. Compile the target with sanitizer and fuzzing support. 5. Run libFuzzer to test seed generator efficacy. 6. Analyze crashes and refine seed generator logic. 7. Expand seed variety to cover edge cases. 8. Document generator code and usage for reuse.
- **Detection**: Fuzzer output, sanitizer logs
- **Solution**: Fix parsing bugs, improve input validation
- **Tags**: fuzzing, libFuzzer, seed generator, dynamic input

## Dictionary Creation for Network Protocol Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Network parsers
- **Vulnerability**: Protocol parsing flaws
- **MITRE**: T1574
- **Impact**: Enhanced fuzzing discovery of protocol bugs
- **Tools**: AFL++, Honggfuzz
- **Scenario**: Building dictionaries containing protocol commands and control sequences for network protocol fuzzers.
- **Attack Steps**: 1. Study the protocol RFC or specification to extract commands and control characters. 2. Format these as dictionary entries for the fuzzer. 3. Include frequently used magic bytes or delimiters. 4. Integrate dictionary file into the fuzzing setup. 5. Start fuzzing and observe improved mutation effectiveness. 6. Triage crashes and analyze protocol parsing bugs. 7. Update dictionary based on fuzzing feedback. 8. Share dictionary for community use and improvement.
- **Detection**: Fuzzer logs, crash reports
- **Solution**: Patch input validation, protocol parsing
- **Tags**: fuzzing, dictionary, protocol, network

## Using Persistent Mode in AFL++

- **Attack Type**: Fuzzer Configuration
- **Target**: Application binaries
- **Vulnerability**: Performance bottlenecks
- **MITRE**: T1499
- **Impact**: Faster fuzzing runs leading to more bugs found
- **Tools**: AFL++
- **Scenario**: Enabling AFL++ persistent mode to reduce overhead and increase fuzzing speed on applications with repeated input processing.
- **Attack Steps**: 1. Compile target binary with AFL++ instrumentation. 2. Modify the target application to support persistent mode by looping input processing. 3. Configure AFL++ with -p flag to enable persistent mode. 4. Prepare seed corpus for input mutation. 5. Run AFL++ and monitor increased fuzzing speed and coverage. 6. Analyze crashes and logs for vulnerabilities. 7. Tune persistent mode parameters to balance speed and stability. 8. Document persistent mode setup and troubleshooting tips.
- **Detection**: AFL++ logs, crash reports
- **Solution**: Patch discovered bugs, optimize input handling
- **Tags**: fuzzing, AFL++, performance, persistent mode

## Seed Corpus Curation for HTML5 Video Players

- **Attack Type**: Fuzzer Configuration
- **Target**: Multimedia browsers
- **Vulnerability**: Buffer overflow, memory corruption
- **MITRE**: T1201
- **Impact**: Discovery of crashes or remote code execution
- **Tools**: AFL++, libFuzzer
- **Scenario**: Collecting and preparing valid HTML5 video files and metadata to fuzz multimedia browser components effectively.
- **Attack Steps**: 1. Identify target HTML5 video player components. 2. Gather a diverse set of video files with different codecs and metadata. 3. Validate files for compatibility. 4. Organize seed corpus for fuzzer access. 5. Run preliminary fuzzing to confirm corpus validity. 6. Add edge cases with malformed metadata or unusual codec flags. 7. Monitor fuzzing progress and crashes. 8. Refine corpus based on results to improve coverage.
- **Detection**: Fuzzer logs, crash analysis
- **Solution**: Patch multimedia parsing code, validate inputs
- **Tags**: fuzzing, seed corpus, multimedia, HTML5 video

## Fine-Tuning Timeout for libFuzzer Sessions

- **Attack Type**: Fuzzer Configuration
- **Target**: Any fuzz target
- **Vulnerability**: Denial of service, infinite loop
- **MITRE**: T1499
- **Impact**: Reduced false positives and improved fuzzing stability
- **Tools**: libFuzzer
- **Scenario**: Adjusting libFuzzer timeout settings to avoid false positives caused by long-running test cases or hangs during fuzzing.
- **Attack Steps**: 1. Identify the maximum acceptable test case execution time. 2. Use the -timeout flag in libFuzzer to set the timeout limit. 3. Monitor fuzzing sessions for test cases terminated due to timeout. 4. Analyze aborted test cases to determine if they represent true hangs or complex processing. 5. Adjust timeout settings to balance fuzzing speed and accuracy. 6. Use sanitizer tools to verify genuine hangs. 7. Document timeout settings for reproducibility.
- **Detection**: Fuzzer logs, sanitizer output
- **Solution**: Fix code paths causing infinite loops or hangs
- **Tags**: fuzzing, timeout tuning, libFuzzer

## Creating Hybrid Fuzzing Strategies

- **Attack Type**: Fuzzer Configuration
- **Target**: Complex apps
- **Vulnerability**: Input validation and parsing errors
- **MITRE**: T1201
- **Impact**: Comprehensive bug discovery across input channels
- **Tools**: AFL++, WinAFL
- **Scenario**: Combining file-based and network socket fuzzing modes to target complex applications with multiple input channels.
- **Attack Steps**: 1. Analyze the target application’s input interfaces (files, network sockets). 2. Prepare separate seed corpora for each input channel. 3. Configure AFL++ for file-based fuzzing and WinAFL for socket-based fuzzing. 4. Run both fuzzers in parallel or sequence. 5. Monitor coverage and crashes from both fuzzers. 6. Correlate findings to discover multi-channel vulnerabilities. 7. Adjust fuzzing parameters for each input mode as needed. 8. Document hybrid fuzzing methodology for repeatability.
- **Detection**: Combined fuzzer logs, debugger output
- **Solution**: Patch all input handlers, ensure robust validation
- **Tags**: fuzzing, hybrid fuzzing, multi-input, network

## Leveraging Code Coverage Feedback in Honggfuzz

- **Attack Type**: Fuzzer Configuration
- **Target**: Application binaries
- **Vulnerability**: Code execution flaws
- **MITRE**: T1201
- **Impact**: Increased bug detection through targeted fuzzing
- **Tools**: Honggfuzz
- **Scenario**: Using code coverage feedback mechanisms in Honggfuzz to guide input mutations and improve fuzzing effectiveness.
- **Attack Steps**: 1. Install Honggfuzz with coverage tracking enabled. 2. Instrument the target binary for coverage collection. 3. Run Honggfuzz with coverage feedback enabled. 4. Observe fuzzing progress through coverage dashboards. 5. Use coverage data to guide mutation strategies toward unexplored code paths. 6. Analyze crash reports and identify vulnerable code sections. 7. Refine corpus and mutation settings based on coverage insights. 8. Document coverage feedback integration process.
- **Detection**: Honggfuzz coverage reports, crash logs
- **Solution**: Fix code paths revealed by coverage-guided fuzzing
- **Tags**: fuzzing, Honggfuzz, code coverage, instrumentation

## Setting Up Seed Corpus for Network Protocol Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Network parsers
- **Vulnerability**: Protocol parsing flaws
- **MITRE**: T1574
- **Impact**: Crashes or remote code execution in protocol handling
- **Tools**: Wireshark, tcpdump, WinAFL
- **Scenario**: Collecting and preparing network packet captures to form an effective seed corpus for fuzzing protocol parsers.
- **Attack Steps**: 1. Identify the protocol and network interface to monitor. 2. Use Wireshark or tcpdump to capture valid traffic between communicating endpoints. 3. Filter relevant packets to extract payload data matching the protocol. 4. Validate and sanitize captured packets to remove malformed or irrelevant data. 5. Store extracted packets in a directory structured for easy fuzzer access. 6. Integrate the seed corpus with WinAFL’s socket fuzzing configuration. 7. Start fuzzing and monitor for crashes and increased code coverage. 8. Update the seed corpus continuously by capturing new valid packets during fuzzing. 9. Analyze fuzzing logs and crashes for further refinement of corpus and fuzzing parameters.
- **Detection**: Network packet logs, fuzzing output
- **Solution**: Patch protocol parsing logic, validate inputs properly
- **Tags**: fuzzing, seed corpus, network, protocol

## Configuring libFuzzer for Multi-Input Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Complex applications
- **Vulnerability**: Input parsing errors
- **MITRE**: T1201
- **Impact**: Denial of service, crash, or remote code execution
- **Tools**: libFuzzer
- **Scenario**: Setting up libFuzzer to fuzz applications that accept multiple inputs (files, arguments) by designing custom harnesses for complex input structures.
- **Attack Steps**: 1. Analyze the target application to understand multiple input parameters and their formats. 2. Develop a custom fuzzing harness that accepts and parses multiple inputs from fuzzer-generated byte streams. 3. Prepare initial seed inputs representing valid combinations of inputs. 4. Compile the target application with sanitizer and libFuzzer instrumentation. 5. Run libFuzzer, feeding it the combined input data. 6. Monitor sanitizer reports for memory safety violations and crashes. 7. Refine the fuzzing harness to better parse complex inputs and avoid false positives. 8. Iterate fuzzing to improve code coverage and bug discovery.
- **Detection**: Sanitizer outputs, libFuzzer logs
- **Solution**: Patch input parsing routines, improve validation
- **Tags**: fuzzing, libFuzzer, multi-input, sanitizer

## Building a Dictionary for Multimedia File Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Multimedia parsers
- **Vulnerability**: Buffer overflow, use-after-free
- **MITRE**: T1201
- **Impact**: Increased bug discovery rate and coverage
- **Tools**: AFL++, libFuzzer
- **Scenario**: Creating a dictionary tailored to multimedia file formats (e.g., MP4, AVI) containing codec identifiers and header tokens for enhanced fuzzing.
- **Attack Steps**: 1. Research multimedia container and codec specifications to identify critical tokens and headers. 2. Extract frequently occurring magic bytes and identifiers. 3. Format these tokens into a dictionary file compliant with fuzzer syntax. 4. Integrate the dictionary with the fuzzer’s configuration. 5. Run fuzzing sessions and monitor increased code coverage and crash discovery. 6. Analyze crashes to verify the dictionary’s effectiveness in triggering vulnerabilities. 7. Refine the dictionary based on fuzzing feedback and new format versions. 8. Share the dictionary with the research community for collaborative improvement.
- **Detection**: Fuzzer logs, crash reports
- **Solution**: Patch multimedia parsing bugs, enhance input validation
- **Tags**: fuzzing, dictionary, multimedia, codecs

## Selecting Optimal Seed Corpus for File-Based Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: File parsers
- **Vulnerability**: Memory corruption, integer overflow
- **MITRE**: T1201
- **Impact**: Higher code coverage and bug discovery
- **Tools**: AFL++, libFuzzer
- **Scenario**: Choosing a representative and diverse seed corpus to maximize fuzzing effectiveness against file input handlers.
- **Attack Steps**: 1. Identify all supported file formats and variants processed by the target. 2. Collect a wide variety of valid files across these formats, covering different sizes and complexities. 3. Filter out corrupted or invalid files to prevent false positives. 4. Use corpus minimization tools to reduce redundant seeds without sacrificing coverage. 5. Organize seed files in directories readable by fuzzing tools. 6. Test initial fuzzing runs to confirm seed corpus coverage and fuzzing stability. 7. Update and expand corpus regularly with new files. 8. Document corpus selection criteria and preparation process.
- **Detection**: Coverage reports, fuzzing logs
- **Solution**: Maintain corpus quality, patch vulnerable file parsers
- **Tags**: fuzzing, seed corpus, file formats

## Configuring Timeout and Retry Parameters in WinAFL

- **Attack Type**: Fuzzer Configuration
- **Target**: Network or file targets
- **Vulnerability**: Denial of Service, infinite loop
- **MITRE**: T1499
- **Impact**: Improved fuzzing efficiency and accuracy
- **Tools**: WinAFL
- **Scenario**: Adjusting WinAFL’s timeout and retry settings to improve fuzzing stability and prevent hangs or false crashes.
- **Attack Steps**: 1. Understand the target application’s normal execution time and failure modes. 2. Configure timeout parameters in WinAFL to prevent premature test case termination. 3. Set retry count for test cases that trigger hangs or crashes to avoid false positives. 4. Run fuzzing sessions while monitoring for timeouts and retries. 5. Analyze logs to identify real bugs versus resource exhaustion. 6. Adjust timeout and retry values iteratively for optimal fuzzing efficiency. 7. Document settings for reproducibility. 8. Use debugging tools to verify genuine hangs or crashes.
- **Detection**: WinAFL logs, debugger output
- **Solution**: Fix code paths causing hangs, patch input handlers
- **Tags**: fuzzing, WinAFL, timeout, retries

## Preparing Corpus for HTML5 Web Application Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Web browsers
- **Vulnerability**: Memory corruption, input validation flaws
- **MITRE**: T1201
- **Impact**: Enhanced fuzzing effectiveness and bug detection
- **Tools**: AFL++, libFuzzer
- **Scenario**: Gathering valid HTML5 files, scripts, and assets as seed corpus for fuzzing browser parsing engines and web app components.
- **Attack Steps**: 1. Collect a wide range of valid HTML5 documents including scripts and multimedia elements. 2. Validate files using web validators to ensure correctness. 3. Remove duplicates and corrupted files. 4. Organize corpus in accessible directories. 5. Run test fuzzing sessions to verify corpus integrity. 6. Add edge cases and malformed elements to improve fuzzing coverage. 7. Update corpus continuously based on fuzzing feedback. 8. Document corpus preparation methods and quality assurance steps.
- **Detection**: Fuzzer coverage reports, crash analysis
- **Solution**: Patch parsing bugs, improve input sanitization
- **Tags**: fuzzing, seed corpus, HTML5, web

## Dictionary Setup for File Format Parsers

- **Attack Type**: Fuzzer Configuration
- **Target**: File parsers
- **Vulnerability**: Input validation flaws
- **MITRE**: T1201
- **Impact**: Improved code coverage and vulnerability discovery
- **Tools**: AFL++, libFuzzer
- **Scenario**: Creating dictionaries containing key tokens and magic bytes for common file formats to guide fuzzers toward relevant input mutations.
- **Attack Steps**: 1. Identify key tokens and magic bytes for target file formats (e.g., ZIP, PNG, PDF). 2. Extract and format these into dictionary files compatible with fuzzers. 3. Integrate dictionaries into fuzzing configuration files. 4. Start fuzzing and monitor for improved mutation effectiveness. 5. Analyze crash patterns to evaluate dictionary effectiveness. 6. Refine dictionaries by adding new tokens discovered during fuzzing. 7. Share dictionaries for community collaboration.
- **Detection**: Fuzzer logs, crash reports
- **Solution**: Patch parser bugs, improve input validation
- **Tags**: fuzzing, dictionary, file formats

## Configuring AFL++ for Persistent Mode

- **Attack Type**: Fuzzer Configuration
- **Target**: Application binaries
- **Vulnerability**: Performance and stability issues
- **MITRE**: T1499
- **Impact**: Faster fuzzing with increased bug discovery
- **Tools**: AFL++
- **Scenario**: Enabling persistent mode in AFL++ to reduce fork overhead and speed up fuzzing of target applications with repeated input loops.
- **Attack Steps**: 1. Ensure the target application supports persistent mode loops. 2. Compile the target with AFL++ instrumentation and persistent mode enabled. 3. Configure AFL++ with the -p flag for persistent fuzzing. 4. Prepare seed corpus of valid inputs. 5. Run AFL++ and monitor for faster fuzzing cycles. 6. Analyze crash logs and coverage reports. 7. Tune persistent mode parameters such as iteration counts for stability. 8. Document configuration for reproducibility.
- **Detection**: AFL++ logs, crash reports
- **Solution**: Patch bugs, optimize input handling
- **Tags**: fuzzing, AFL++, persistent mode, performance

## Seed Corpus Validation Techniques

- **Attack Type**: Fuzzer Configuration
- **Target**: Any fuzz target
- **Vulnerability**: Input validation and crash prevention
- **MITRE**: T1201
- **Impact**: Higher fuzzing quality and reduced false positives
- **Tools**: AFL++, libFuzzer
- **Scenario**: Techniques to verify the validity and diversity of seed corpus files to prevent fuzzing false positives and improve effectiveness.
- **Attack Steps**: 1. Run all seed files through the target application to ensure no crashes or unexpected behavior. 2. Use hash functions to detect and remove duplicate seeds. 3. Analyze file diversity using format-specific metrics (e.g., metadata, size). 4. Perform corpus minimization to keep only unique and relevant seeds. 5. Regularly update corpus with new valid inputs. 6. Document validation steps and maintain corpus quality control logs.
- **Detection**: Fuzzer stability logs, application logs
- **Solution**: Maintain corpus quality, patch false positive triggers
- **Tags**: fuzzing, seed corpus, validation, quality assurance

## Configuring Timeout and Resource Limits in Honggfuzz

- **Attack Type**: Fuzzer Configuration
- **Target**: Any fuzz target
- **Vulnerability**: Denial of service, infinite loops
- **MITRE**: T1499
- **Impact**: Improved fuzzing stability and accuracy
- **Tools**: Honggfuzz
- **Scenario**: Adjusting Honggfuzz’s timeout and memory limits to optimize fuzzing performance and prevent false crash reports.
- **Attack Steps**: 1. Analyze target application’s resource requirements and execution time. 2. Set timeout values in Honggfuzz configuration to avoid long hangs. 3. Adjust memory limits to prevent excessive consumption. 4. Run fuzzing sessions monitoring for timeout or OOM errors. 5. Distinguish between genuine bugs and resource exhaustion issues. 6. Tune parameters iteratively based on fuzzing results. 7. Document configuration for repeatability and sharing.
- **Detection**: Honggfuzz logs, resource monitoring tools
- **Solution**: Patch infinite loops and optimize memory management
- **Tags**: fuzzing, Honggfuzz, timeout, memory limits

## Dictionary Setup for Network Socket Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Network services
- **Vulnerability**: Protocol parsing flaws
- **MITRE**: T1574
- **Impact**: Improved fuzzing efficiency and discovery of remote exploits
- **Tools**: WinAFL, Honggfuzz
- **Scenario**: Creating and configuring dictionaries with protocol commands and magic bytes for use in socket-based fuzzing tools like WinAFL and Honggfuzz.
- **Attack Steps**: 1. Analyze target network protocol specifications for commands, headers, and control sequences. 2. Extract magic bytes, opcodes, and protocol-specific tokens. 3. Format these as dictionary entries compatible with WinAFL and Honggfuzz. 4. Integrate the dictionary into fuzzing configurations. 5. Run fuzzing with the dictionary enabled and observe mutation efficiency improvements. 6. Monitor crashes and logs for protocol parsing vulnerabilities. 7. Refine dictionary based on fuzzing feedback and newly discovered tokens. 8. Document dictionary creation and usage for repeatability.
- **Detection**: Fuzzer logs, crash reports
- **Solution**: Patch input validation and protocol parsing
- **Tags**: fuzzing, dictionary, network, socket

## Seed Corpus Generation Using Automated Crawlers

- **Attack Type**: Fuzzer Configuration
- **Target**: Web apps, file parsers
- **Vulnerability**: Input validation flaws
- **MITRE**: T1201
- **Impact**: Increased coverage and bug discovery in fuzz targets
- **Tools**: Custom scripts, wget, curl
- **Scenario**: Using automated web crawlers and file scanners to collect diverse seed inputs for fuzzing web applications and file parsers.
- **Attack Steps**: 1. Define target web application or file repository URLs. 2. Develop or use existing crawlers to systematically download files and resources. 3. Filter and validate downloaded files to ensure compatibility with the fuzz target. 4. Organize collected files into structured seed corpus directories. 5. Run fuzzing sessions using the collected corpus as seed inputs. 6. Monitor fuzzing coverage and crash discovery. 7. Continuously update corpus with new downloads and findings. 8. Document crawling strategy and corpus maintenance.
- **Detection**: Fuzzer logs, crash reports
- **Solution**: Maintain corpus quality and update crawling scripts
- **Tags**: fuzzing, seed corpus, web crawling

## Fine-Tuning Memory Limits for WinAFL

- **Attack Type**: Fuzzer Configuration
- **Target**: Network/file targets
- **Vulnerability**: Denial of service, resource exhaustion
- **MITRE**: T1499
- **Impact**: Improved fuzzing stability and accuracy
- **Tools**: WinAFL
- **Scenario**: Adjusting memory limits and process isolation parameters in WinAFL to prevent resource exhaustion and false crash reports.
- **Attack Steps**: 1. Analyze typical memory consumption of the target application during fuzzing. 2. Configure WinAFL with memory limits appropriate to the target. 3. Use process isolation features to contain crashes. 4. Run fuzzing and monitor for out-of-memory errors or premature crashes. 5. Adjust memory parameters to balance fuzzing throughput and stability. 6. Document settings and provide recommendations for similar targets.
- **Detection**: WinAFL logs, system monitoring
- **Solution**: Optimize memory management in target application
- **Tags**: fuzzing, WinAFL, memory management

## Creating Custom Corpus Mutators for AFL++

- **Attack Type**: Fuzzer Configuration
- **Target**: Specialized file parsers
- **Vulnerability**: Input validation and logic bugs
- **MITRE**: T1201
- **Impact**: Enhanced fuzzing depth and vulnerability detection
- **Tools**: AFL++
- **Scenario**: Developing custom mutator modules to extend AFL++ with domain-specific mutations for enhanced fuzzing of specialized file formats.
- **Attack Steps**: 1. Identify domain-specific structures and data formats in the target inputs. 2. Develop custom mutator code in C/C++ that modifies these structures intelligently. 3. Integrate the mutator with AFL++ using its custom mutator API. 4. Compile and run AFL++ with the custom mutator enabled. 5. Monitor fuzzing coverage and bug discovery improvements. 6. Iterate mutator development based on fuzzing feedback and crash analysis. 7. Document the custom mutator’s design and integration process.
- **Detection**: AFL++ logs, coverage reports
- **Solution**: Patch discovered bugs, improve input handling
- **Tags**: fuzzing, AFL++, custom mutators

## Corpus Minimization for libFuzzer

- **Attack Type**: Fuzzer Configuration
- **Target**: Any fuzz target
- **Vulnerability**: Input validation and crash prevention
- **MITRE**: T1201
- **Impact**: Reduced fuzzing overhead and improved efficiency
- **Tools**: libFuzzer
- **Scenario**: Using libFuzzer’s corpus minimization tools to remove redundant inputs while preserving coverage for efficient fuzzing.
- **Attack Steps**: 1. Gather the existing seed corpus used in fuzzing campaigns. 2. Run libFuzzer with the -merge=1 and -minimize_crash options to minimize corpus size. 3. Validate that minimized corpus retains original coverage and crash triggers. 4. Replace original corpus with minimized corpus for future fuzzing runs. 5. Document corpus minimization results and procedures.
- **Detection**: libFuzzer logs, coverage reports
- **Solution**: Maintain corpus quality and prevent false positives
- **Tags**: fuzzing, corpus minimization, libFuzzer

## Using AFL++ Persistent Mode with Network Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Network protocol parsers
- **Vulnerability**: Performance bottlenecks and parsing errors
- **MITRE**: T1499
- **Impact**: Increased fuzzing throughput and vulnerability detection
- **Tools**: AFL++, WinAFL
- **Scenario**: Combining AFL++ persistent mode with network socket fuzzing to improve fuzzing speed for network protocol parsers.
- **Attack Steps**: 1. Modify target application to support persistent mode in network input handling. 2. Compile with AFL++ instrumentation and persistent mode enabled. 3. Configure AFL++ for network socket fuzzing with persistent mode. 4. Prepare seed corpus with valid network packets. 5. Run fuzzing campaigns monitoring performance improvements and crash discovery. 6. Tune persistent mode parameters for stability. 7. Analyze crashes and coverage logs for fuzzing efficacy. 8. Document setup for reproducibility.
- **Detection**: AFL++ logs, network traffic analysis
- **Solution**: Patch parsing bugs and optimize input handling
- **Tags**: fuzzing, AFL++, persistent mode, network

## Creating Seed Corpus for Image Format Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Image parsers
- **Vulnerability**: Buffer overflows, memory corruption
- **MITRE**: T1201
- **Impact**: Enhanced fuzzing coverage and bug discovery
- **Tools**: AFL++, libFuzzer
- **Scenario**: Collecting and validating image files (PNG, JPEG, BMP) as seed corpus to fuzz image parsing libraries effectively.
- **Attack Steps**: 1. Collect diverse valid image files from various sources. 2. Validate images with format-specific tools and libraries. 3. Remove corrupted or invalid files. 4. Organize seed corpus for easy access by fuzzers. 5. Run preliminary fuzzing to confirm corpus compatibility. 6. Add edge case images with unusual metadata or compression settings. 7. Update corpus with new files based on fuzzing feedback. 8. Document corpus collection and validation process.
- **Detection**: Fuzzer logs, crash reports
- **Solution**: Patch vulnerabilities in image parsing code
- **Tags**: fuzzing, seed corpus, images

## Configuring libFuzzer for Input-Dependent Code Paths

- **Attack Type**: Fuzzer Configuration
- **Target**: Complex applications
- **Vulnerability**: Logic errors, input validation
- **MITRE**: T1201
- **Impact**: Increased discovery of subtle logic and validation bugs
- **Tools**: libFuzzer
- **Scenario**: Designing fuzzing harnesses to expose input-dependent code paths for maximum coverage during fuzzing sessions.
- **Attack Steps**: 1. Analyze application code for input-dependent branches. 2. Write fuzzing harnesses that cover diverse input cases triggering these branches. 3. Prepare initial seed inputs reflecting these cases. 4. Compile with libFuzzer instrumentation and sanitizers. 5. Run fuzzing and monitor coverage increases. 6. Refine harnesses to reduce false positives and improve mutation impact. 7. Document harness design and fuzzing results.
- **Detection**: Sanitizer outputs, libFuzzer coverage reports
- **Solution**: Patch logic errors and improve input validation
- **Tags**: fuzzing, libFuzzer, code coverage

## Automating Dictionary Updates with Fuzzer Feedback

- **Attack Type**: Fuzzer Configuration
- **Target**: Any fuzz target
- **Vulnerability**: Input validation flaws
- **MITRE**: T1201
- **Impact**: Increased fuzzing efficiency and bug discovery
- **Tools**: AFL++, Honggfuzz
- **Scenario**: Using crash and coverage data to automate updates of fuzzer dictionaries for improved mutation effectiveness over time.
- **Attack Steps**: 1. Collect crash and coverage logs from fuzzing runs. 2. Extract new tokens, magic bytes, or interesting input patterns from logs. 3. Update dictionary files automatically or semi-automatically. 4. Integrate updated dictionaries into subsequent fuzzing sessions. 5. Monitor fuzzing improvements and adjust automation scripts as needed. 6. Document automation workflow and tools used.
- **Detection**: Fuzzer logs, dictionary change logs
- **Solution**: Patch vulnerabilities discovered through improved fuzzing
- **Tags**: fuzzing, dictionary, automation

## Preparing Seed Corpus for PDF Metadata Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: PDF parsers
- **Vulnerability**: Memory corruption, integer overflow
- **MITRE**: T1201
- **Impact**: Discovery of vulnerabilities in metadata parsing
- **Tools**: AFL++, libFuzzer
- **Scenario**: Extracting and collecting PDF metadata samples to fuzz PDF readers’ metadata parsers for hidden vulnerabilities.
- **Attack Steps**: 1. Identify metadata fields in PDF specification. 2. Extract metadata from a variety of valid PDF files. 3. Validate extracted metadata for format correctness. 4. Organize metadata samples as seed corpus for fuzzing. 5. Run fuzzing campaigns targeting metadata parsing code. 6. Monitor crashes and analyze logs. 7. Update metadata corpus with fuzzing feedback and new file samples. 8. Document extraction and corpus preparation processes.
- **Detection**: Fuzzer logs, sanitizer reports
- **Solution**: Patch PDF metadata parsing vulnerabilities
- **Tags**: fuzzing, seed corpus, PDF, metadata

## Fuzzing IoT Device Firmware Using File-Based Mode

- **Attack Type**: Fuzzer Configuration
- **Target**: Embedded Firmware
- **Vulnerability**: Improper input validation
- **MITRE**: T1203
- **Impact**: Remote code execution or crash in firmware
- **Tools**: AFL++, QEMU
- **Scenario**: The researcher configures AFL++ in file-based mode to fuzz IoT firmware's input handling routines.
- **Attack Steps**: 1. Identify the firmware binary of the IoT device (e.g., router firmware). 2. Set up a QEMU user-mode emulation environment to simulate firmware execution. 3. Extract the binary that handles file input (e.g., config loader). 4. Collect valid configuration files as seed corpus. 5. Configure AFL++ with QEMU mode and file-based input delivery. 6. Start the fuzzing campaign and monitor for crashes. 7. Analyze the crashes using GDB or crash triage tools to discover vulnerabilities.
- **Detection**: QEMU logs, crash dumps, code coverage stats
- **Solution**: Input validation hardening in firmware
- **Tags**: iot, firmware, fuzzing, qemu, afl++

## Fuzzing PDF Reader via Magic Byte Dictionary

- **Attack Type**: Fuzzer Configuration
- **Target**: Desktop Application
- **Vulnerability**: File parsing errors
- **MITRE**: T1203
- **Impact**: Memory corruption or code execution
- **Tools**: AFL++, pdfid
- **Scenario**: Researcher enhances fuzzing precision by adding PDF-specific magic bytes to the dictionary.
- **Attack Steps**: 1. Choose a PDF reader as the target application. 2. Collect a small set of valid PDF files as the initial seed corpus. 3. Use tools like pdfid to extract file signatures and structural markers. 4. Create a dictionary with PDF-specific tokens like %PDF, stream, obj, /Catalog. 5. Configure AFL++ to use the dictionary file and run in file-based mode. 6. Begin fuzzing with dictionary-based mutation. 7. Monitor for abnormal behavior or crashes during rendering. 8. Analyze inputs that cause memory corruption.
- **Detection**: Application logs, crash popups, memory dump
- **Solution**: Patch parser, improve PDF syntax handling
- **Tags**: dictionary, pdf, file-fuzzing

## WinAFL Network Socket-Based Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: Windows Server App
- **Vulnerability**: Socket input parsing flaws
- **MITRE**: T1210
- **Impact**: Server crash or remote RCE
- **Tools**: WinAFL, DynamoRIO
- **Scenario**: Configuring WinAFL to fuzz a Windows application that listens for commands over TCP.
- **Attack Steps**: 1. Identify a target Windows app that accepts data over a network socket (e.g., chat server). 2. Use WinAFL's instrumentation (via DynamoRIO) to trace function coverage. 3. Set up a harness that connects to the target's TCP port and feeds fuzzed data. 4. Choose network-based mode and integrate input injection in the harness. 5. Launch WinAFL with custom harness to send fuzzed payloads to the socket. 6. Monitor logs and check crash signals. 7. Capture and triage crashes using WinDbg.
- **Detection**: WinDbg analysis, socket logs
- **Solution**: Harden protocol handler, sanitize socket inputs
- **Tags**: windows, winafl, socket-fuzzing

## Fuzzing Browser Extension Argument Handling

- **Attack Type**: Fuzzer Configuration
- **Target**: Web Browser Extension
- **Vulnerability**: Improper argument sanitization
- **MITRE**: T1203
- **Impact**: Arbitrary script execution
- **Tools**: libFuzzer, Chrome Extension Loader
- **Scenario**: Researcher targets a Chrome extension by fuzzing how it processes URL or script arguments.
- **Attack Steps**: 1. Locate the extension's argument processing logic (e.g., background.js). 2. Create a fuzzing harness that sends various arguments (URLs, script paths). 3. Instrument the logic using libFuzzer-compatible bindings. 4. Create a dictionary of known command-line switches/extensions API calls. 5. Run libFuzzer in argument-based mode with a valid seed corpus of known arguments. 6. Monitor browser logs and JS engine crash logs. 7. Analyze the payloads that cause crashes in argument processing.
- **Detection**: JS console errors, crash logs
- **Solution**: Validate and sanitize extension inputs
- **Tags**: browser, extension, fuzzing, libfuzzer

## Mutational Fuzzing with Custom Corpus for Media Files

- **Attack Type**: Fuzzer Configuration
- **Target**: Media Player
- **Vulnerability**: Memory corruption in decoders
- **MITRE**: T1203
- **Impact**: Player crash, code exec on file open
- **Tools**: Honggfuzz, ffmpeg
- **Scenario**: Researcher prepares a custom seed corpus of video files to fuzz a media player.
- **Attack Steps**: 1. Choose a media player or decoding library (e.g., FFmpeg). 2. Gather a variety of video files (MP4, MKV, AVI) with valid encodings. 3. Prepare the seed corpus from these files. 4. Launch Honggfuzz in file fuzzing mode, targeting the player or decoder binary. 5. Monitor for exceptions like out-of-bounds reads, heap corruption. 6. Use sanitizers or crash tools to analyze vulnerable code paths. 7. Document the bug and responsible codec/parser.
- **Detection**: ASAN logs, segmentation faults
- **Solution**: Patch decoder, add bounds checks
- **Tags**: honggfuzz, media, file-fuzzing

## Testing XML Parser via Dictionary-Aided Fuzzing

- **Attack Type**: Fuzzer Configuration
- **Target**: XML Parser
- **Vulnerability**: XML parsing errors, XXE
- **MITRE**: T1210
- **Impact**: Arbitrary file read or crash
- **Tools**: AFL++, xmllint
- **Scenario**: Researcher creates XML-specific dictionary to fuzz an XML parsing library.
- **Attack Steps**: 1. Identify an XML parser like libxml2. 2. Prepare valid XML files with common patterns as seeds. 3. Build a dictionary with XML keywords: <tag>, </tag>, <!DOCTYPE>, &entity;. 4. Run AFL++ in file mode using the dictionary. 5. Launch the target parser with AFL++ instrumentation. 6. Observe coverage feedback and crash signals. 7. Investigate crashes for potential XXE or parsing bugs.
- **Detection**: Parser logs, AFL++ crash reports
- **Solution**: Disable risky features, patch parser
- **Tags**: xml, dictionary, file-fuzzing

## Fuzzing a Proprietary File Format

- **Attack Type**: Fuzzer Configuration
- **Target**: Custom Application
- **Vulnerability**: Unknown parser flaws
- **MITRE**: T1203
- **Impact**: Application crash, RCE
- **Tools**: AFL++, Ghidra
- **Scenario**: Researcher targets a custom app using its proprietary file format by reverse engineering it and building fuzz input.
- **Attack Steps**: 1. Identify the proprietary file format and application. 2. Use Ghidra to reverse engineer file parsing logic. 3. Manually craft a few seed files from known samples. 4. Identify recurring header structures and magic bytes. 5. Add them to a custom AFL++ dictionary. 6. Fuzz the parser using AFL++ in file mode. 7. Triage crashes using logs and memory dumps.
- **Detection**: Memory access violations, log files
- **Solution**: Secure custom format handling
- **Tags**: reverse, proprietary, fuzzing, afl++

## AFL++ Persistent Mode Optimization

- **Attack Type**: Fuzzer Configuration
- **Target**: JSON Parser
- **Vulnerability**: Input validation flaws
- **MITRE**: T1203
- **Impact**: Faster discovery of parsing bugs
- **Tools**: AFL++
- **Scenario**: Fuzzer is optimized using AFL++ persistent mode to reduce overhead per test case.
- **Attack Steps**: 1. Choose a target with a clear input-handling loop (e.g., JSON parser). 2. Modify the target so it does not exit after each input — instead, reset state and read next input (persistent loop). 3. Compile with AFL++ instrumentation and persistent mode flags. 4. Feed a set of valid JSON files as seed corpus. 5. Start AFL++ fuzzing and observe faster exec/s. 6. Monitor crashes or hangs. 7. Analyze issues in parser logic.
- **Detection**: Execution stats, crash reports
- **Solution**: Use persistent mode for speed gains
- **Tags**: afl++, persistent, speed

## Fuzzing Command-Line Parser with Stdin Input

- **Attack Type**: Fuzzer Configuration
- **Target**: CLI Utility
- **Vulnerability**: Improper command parsing
- **MITRE**: T1059
- **Impact**: Command injection or crash
- **Tools**: libFuzzer
- **Scenario**: Researcher configures a stdin-based fuzzer for a binary accepting structured CLI input.
- **Attack Steps**: 1. Identify a binary that reads commands via stdin (e.g., shell interface). 2. Prepare seed corpus of valid commands. 3. Configure libFuzzer to deliver input via stdin. 4. Run fuzzer with input coverage feedback enabled. 5. Observe for improper parsing or command injection possibilities. 6. If a crash occurs, log the stdin input that caused it. 7. Investigate parser code for bugs.
- **Detection**: stdin logs, crash handler
- **Solution**: Sanitize CLI input
- **Tags**: cli, stdin, libfuzzer

## Fuzzing Linux Syscalls with Custom Harness

- **Attack Type**: Fuzzer Configuration
- **Target**: Linux Kernel
- **Vulnerability**: Syscall handling bugs
- **MITRE**: T1499
- **Impact**: Kernel panic or LPE
- **Tools**: syzkaller, AFL++
- **Scenario**: Researcher targets Linux system calls using a custom harness for syscall wrappers.
- **Attack Steps**: 1. Identify system calls with complex parameters (e.g., ioctl, sendmsg). 2. Write a harness that wraps these syscalls with user-controlled arguments. 3. Integrate with AFL++ or syzkaller as the fuzzing engine. 4. Generate a corpus of realistic syscall input structures. 5. Launch the fuzzer and monitor kernel logs. 6. Use KASAN or dmesg to analyze kernel crashes. 7. Report and reproduce issues with syscall input sanitization.
- **Detection**: KASAN reports, dmesg, crash output
- **Solution**: Harden syscall input checks
- **Tags**: syscall, kernel, harness, fuzzing

## Launch AFL++ Fuzzing on Command-Line Tool

- **Attack Type**: Fuzzing Execution
- **Target**: CLI tool
- **Vulnerability**: Input parsing flaw
- **MITRE**: T1203
- **Impact**: Application crash, potential RCE
- **Tools**: AFL++, afl-fuzz
- **Scenario**: The analyst executes AFL++ against a custom CLI application that accepts a file as input. The goal is to identify crashes through fuzzing and record all findings.
- **Attack Steps**: 1. Compile the target binary with AFL++’s afl-gcc or afl-clang-fast to enable instrumentation. 2. Prepare a small set of valid input files (e.g., .conf or .txt) to serve as the seed corpus. 3. Create an input directory and place the seed files inside. 4. Run AFL++ using afl-fuzz -i input_dir -o output_dir -- ./target_app @@. 5. Monitor the execution queue and crash stats from the AFL UI. 6. Wait until new paths and crashes are discovered. 7. Explore output_dir/crashes for crash samples.
- **Detection**: Crash logs, AFL stats UI
- **Solution**: Patch the input parser, validate input before processing
- **Tags**: afl++, fuzzing, binary analysis

## Resource-Aware Fuzzing with libFuzzer

- **Attack Type**: Fuzzing Execution
- **Target**: Image parser
- **Vulnerability**: Heap overflow
- **MITRE**: T1203
- **Impact**: Memory exhaustion, crash
- **Tools**: libFuzzer, htop
- **Scenario**: A researcher executes libFuzzer on a memory-hungry image parser and monitors memory usage to avoid false positives due to OOM.
- **Attack Steps**: 1. Compile the target with clang and link against libFuzzer using -fsanitize=fuzzer,address. 2. Run the fuzzer using ./target_fuzz -runs=0 -max_total_time=3600 corpus_dir. 3. Use htop to monitor memory usage of the process. 4. Set a memory limit using -rss_limit_mb=2048 to prevent exceeding physical memory. 5. Let the fuzzer run for 1 hour. 6. Examine the crash-* files generated in the corpus directory. 7. Use AddressSanitizer output to interpret crash details.
- **Detection**: htop, memory stats, sanitizer reports
- **Solution**: Optimize memory allocation, apply input validation
- **Tags**: libfuzzer, memory, oomsafety

## Crash Corpus Management with afl-cmin

- **Attack Type**: Fuzzing Execution
- **Target**: File parser
- **Vulnerability**: Input fuzzing bugs
- **MITRE**: T1203
- **Impact**: Reduced analysis overhead
- **Tools**: AFL++, afl-cmin
- **Scenario**: After collecting many crashes from a 24h fuzzing session, the analyst uses afl-cmin to minimize inputs while preserving crash behavior.
- **Attack Steps**: 1. Run AFL++ normally for 24 hours against the target binary. 2. Save all crashes from output_dir/crashes. 3. Create a new directory for crash triage. 4. Use the command afl-cmin -i crashes -o min_crashes -- ./target @@. 5. Let afl-cmin identify the minimal set of inputs that still trigger crashes. 6. Store minimized crashes separately and document crash types. 7. Use these reduced cases for debugging and reporting.
- **Detection**: Output folder diff, crash behavior retained
- **Solution**: Use minimized crash set in triage
- **Tags**: fuzzing, minimization, afl-cmin

## Fuzzing Execution with Timeout Configuration

- **Attack Type**: Fuzzing Execution
- **Target**: Userland app
- **Vulnerability**: Infinite loop, hang
- **MITRE**: T1499
- **Impact**: App unresponsive
- **Tools**: AFL++, libFuzzer
- **Scenario**: A fuzzing engineer configures timeout settings to detect hangs in the target application and speed up test case rejection.
- **Attack Steps**: 1. Compile target with instrumentation (afl-gcc or afl-clang-fast). 2. Use -t 2000+ option in AFL to set per-execution timeout to 2 seconds. 3. Execute AFL with the timeout flag enabled. 4. For libFuzzer, use -timeout=2 in command line. 5. Let fuzzing run and observe if any inputs consistently cause timeouts. 6. Save timeout-related crash files separately. 7. Investigate if timeouts indicate logic bugs or loops.
- **Detection**: AFL stats, libFuzzer logs
- **Solution**: Add watchdogs, loop detection, code optimization
- **Tags**: timeout, infinite loop, AFL

## Multi-Core Fuzzing Execution with AFL++

- **Attack Type**: Fuzzing Execution
- **Target**: Parser binary
- **Vulnerability**: Memory corruption
- **MITRE**: T1203
- **Impact**: Faster fuzzing coverage
- **Tools**: AFL++, tmux
- **Scenario**: The team parallelizes AFL++ fuzzing across multiple CPU cores to improve fuzzing throughput and crash discovery rate.
- **Attack Steps**: 1. Compile the target using AFL++'s instrumentation tools. 2. Prepare seed corpus and shared output directory. 3. Start one AFL++ master session: afl-fuzz -i in -o out -M master -- ./target @@. 4. In separate terminals, start secondary slaves using -S slave1, -S slave2, etc. 5. Monitor each session using tmux panes. 6. Crashes and coverage will be shared across all workers. 7. Periodically review crash directory.
- **Detection**: Shared crash folders, AFL stats
- **Solution**: Scalable fuzzing setup, bug detection
- **Tags**: afl++, multicore, scalability

## Live Crash Logging during Honggfuzz Campaign

- **Attack Type**: Fuzzing Execution
- **Target**: System binary
- **Vulnerability**: Buffer overflow
- **MITRE**: T1203
- **Impact**: Privilege escalation risk
- **Tools**: Honggfuzz, dmesg
- **Scenario**: A security analyst runs Honggfuzz against a target and captures live crash logs for immediate triage.
- **Attack Steps**: 1. Compile the binary with Honggfuzz's hfuzz-clang or hfuzz-gcc. 2. Prepare input seed corpus and create input/ directory. 3. Start fuzzing using honggfuzz -i input -o output -- ./target @@. 4. Monitor real-time logs displayed by Honggfuzz. 5. When a crash occurs, check /var/log/syslog or use dmesg to observe system-level crash information. 6. Use hfuzz_cc/crash/ to find the crash-inducing test case. 7. Move logs and crash files to a triage folder.
- **Detection**: System logs, crash outputs
- **Solution**: Add bounds checking, fix overflow logic
- **Tags**: honggfuzz, crash logs, triage

## Network-based Fuzzing with Socket Target

- **Attack Type**: Fuzzing Execution
- **Target**: Network service
- **Vulnerability**: Protocol parsing bugs
- **MITRE**: T1210
- **Impact**: Remote crash, DoS
- **Tools**: AFL++, netcat
- **Scenario**: Fuzzing is launched against a network service that receives binary messages via TCP, with a monitor to track service stability.
- **Attack Steps**: 1. Write a fuzzing harness that connects to the service and sends @@ as input. 2. Instrument the harness using afl-clang-fast. 3. Use afl-fuzz -i inputs -o out -- ./fuzz_harness @@. 4. Start the target network service in a separate terminal. 5. Redirect AFL’s input to the TCP socket via harness. 6. Monitor the network service log for crashes. 7. Review AFL’s output for detected crashes or timeouts.
- **Detection**: Service logs, socket disconnects
- **Solution**: Harden protocol parser, input filter
- **Tags**: fuzzing, socket, tcp service

## Disk Monitoring During Long Fuzzing Runs

- **Attack Type**: Fuzzing Execution
- **Target**: System binary
- **Vulnerability**: Resource overuse
- **MITRE**: T1499
- **Impact**: Disk full, fuzzing failure
- **Tools**: AFL++, iostat
- **Scenario**: To ensure long fuzzing runs don’t fill up disk space, the analyst uses disk monitoring alongside fuzzing campaigns.
- **Attack Steps**: 1. Run AFL fuzzing as usual with afl-fuzz. 2. Open a parallel terminal and run iostat -xm 2 to monitor disk I/O. 3. Check for abnormal write rates from AFL’s output directory. 4. Periodically check du -sh output/ to review disk usage. 5. Clean up any redundant queue entries or backup old crashes. 6. If needed, move crash samples to external storage. 7. Resume fuzzing after ensuring space availability.
- **Detection**: Disk I/O stats, iostat, du
- **Solution**: Manage disk quota, archive old data
- **Tags**: disk, fuzzing, resource management

## Seed Corpus Growth During Execution

- **Attack Type**: Fuzzing Execution
- **Target**: Command-line tool
- **Vulnerability**: Logic bugs
- **MITRE**: T1203
- **Impact**: Higher code coverage
- **Tools**: libFuzzer
- **Scenario**: The fuzzer is configured to continuously grow the seed corpus using discovered interesting paths, improving coverage over time.
- **Attack Steps**: 1. Compile the target with -fsanitize=fuzzer for libFuzzer support. 2. Prepare a small seed corpus. 3. Launch libFuzzer with -max_len=1024 -merge=1 corpus_dir. 4. Let it fuzz continuously; libFuzzer will append new interesting inputs to the corpus. 5. Stop execution after some hours. 6. Review the expanded corpus and validate inputs. 7. Use saved crashes and compare with original seeds.
- **Detection**: Corpus size inspection
- **Solution**: Grow corpus, expand path coverage
- **Tags**: corpus, libfuzzer, path discovery

## Automatic Crash Triage with GDB Script

- **Attack Type**: Fuzzing Execution
- **Target**: Any binary
- **Vulnerability**: Invalid memory access
- **MITRE**: T1203
- **Impact**: Debug-ready triage data
- **Tools**: AFL++, GDB
- **Scenario**: Crashes from a fuzzing campaign are passed through a GDB script to automate debugging and extraction of crash context.
- **Attack Steps**: 1. Collect crash samples from AFL’s crash folder. 2. Create a GDB script (e.g., analyze_crash.gdb) that loads the crash input and breaks on fault. 3. Use gdb -q -x analyze_crash.gdb --args ./target crash_input. 4. Extract faulting instruction, register state, and backtrace. 5. Save analysis logs in structured folders. 6. Repeat for each crash in the queue. 7. Identify crash patterns or duplicates.
- **Detection**: GDB logs, registers
- **Solution**: Triage automation, crash comparison
- **Tags**: fuzzing, crash triage, gdb

## Fuzzing a PDF Parser with AFL++

- **Attack Type**: Fuzzing Execution
- **Target**: File Parser
- **Vulnerability**: Input handling flaw
- **MITRE**: T1203
- **Impact**: Potential memory corruption or DoS
- **Tools**: AFL++, afl-cmin, afl-fuzz
- **Scenario**: Launch a fuzzing campaign against an open-source PDF parser, monitoring resources and crash handling.
- **Attack Steps**: 1. Download and compile a lightweight open-source PDF parser with AFL++ instrumentation. 2. Prepare a seed corpus of valid PDF files. 3. Run afl-fuzz in file input mode with the PDF corpus. 4. Monitor CPU and memory with htop and redirect crash outputs. 5. As crashes are found, collect them from the crashes/ folder. 6. Use afl-cmin to reduce the corpus size. 7. Optionally, analyze crashes using gdb.
- **Detection**: CPU logs, crash folders, GDB triage
- **Solution**: Add input validation in PDF reader
- **Tags**: fuzzing, PDF, AFL++, crash-handling, instrumentation

## Launching Persistent Fuzzing on Command-line App

- **Attack Type**: Fuzzing Execution
- **Target**: CLI Utility
- **Vulnerability**: Input validation failure
- **MITRE**: T1203
- **Impact**: Denial of service or buffer issues
- **Tools**: AFL++, afl-persistent, htop
- **Scenario**: Execute fuzzing in persistent mode for higher performance on command-line utilities.
- **Attack Steps**: 1. Choose a small command-line utility (e.g., image converter). 2. Modify source code to support persistent mode with AFL++. 3. Instrument and compile using afl-clang-fast. 4. Create a directory of seed image files. 5. Start fuzzing using afl-fuzz -P for persistent mode. 6. Continuously monitor system usage via htop. 7. Collect and log any generated crashes. 8. Use afl-tmin to minimize input causing the crash. 9. Analyze crash behavior using a debugger.
- **Detection**: System usage stats, crash repro via debugger
- **Solution**: Implement bounds checking
- **Tags**: fuzzing, persistent-mode, AFL++, resource-monitoring

## Crash Monitoring During libFuzzer Campaign

- **Attack Type**: Fuzzing Execution
- **Target**: Parser Library
- **Vulnerability**: Heap overflow, bad input
- **MITRE**: T1203
- **Impact**: Memory corruption, denial of service
- **Tools**: libFuzzer, AddressSanitizer, lldb
- **Scenario**: Use libFuzzer to monitor and minimize crashes on a vulnerable string parser.
- **Attack Steps**: 1. Select a small C/C++ target with string input handling. 2. Compile with -fsanitize=address -fsanitize-coverage=trace-pc-guard for libFuzzer. 3. Launch the fuzzing campaign using ./fuzzer -max_total_time=3600. 4. Log crashes in a separate directory. 5. Automatically deduplicate crashes using libFuzzer’s built-in features. 6. Run llvm-symbolizer to generate readable stack traces. 7. Use lldb to analyze minimized crashing input. 8. Store unique crash samples separately for triage.
- **Detection**: AddressSanitizer logs, minimized corpus
- **Solution**: Harden input sanitization routines
- **Tags**: libFuzzer, crash-analysis, memory-issues, sanitizer

## Fuzzing Win32 DLL via WinAFL

- **Attack Type**: Fuzzing Execution
- **Target**: Windows DLL
- **Vulnerability**: Input parsing flaw
- **MITRE**: T1218
- **Impact**: RCE or application crash
- **Tools**: WinAFL, DynamoRIO, Process Monitor
- **Scenario**: Launch fuzzing on a Windows DLL using WinAFL and monitor system for crashes and slow executions.
- **Attack Steps**: 1. Identify the Windows DLL and export function to fuzz. 2. Write a harness that loads the DLL and feeds input. 3. Set up WinAFL with DynamoRIO. 4. Provide a seed input directory. 5. Start WinAFL campaign with afl-fuzz.exe. 6. Use Process Monitor to detect anomalies during fuzzing. 7. Monitor CPU/disk usage via Resource Monitor. 8. Save crash inputs and logs. 9. Use afl-cmin to shrink crash set. 10. Triage crash samples in WinDbg.
- **Detection**: Process Monitor logs, crash dumps
- **Solution**: Patch DLL logic and validate input
- **Tags**: winafl, windows, dll-fuzzing, resource-tracking

## Running Honggfuzz in Linux Binary Mode

- **Attack Type**: Fuzzing Execution
- **Target**: Linux binary
- **Vulnerability**: Buffer overflow, heap issues
- **MITRE**: T1203
- **Impact**: Memory corruption, application crash
- **Tools**: Honggfuzz, perf, gdb, sanitizer
- **Scenario**: Run Honggfuzz in binary mode and analyze discovered crashes and unique inputs.
- **Attack Steps**: 1. Choose a Linux binary with stdin or file input. 2. Compile it with sanitizer and Honggfuzz instrumentation. 3. Prepare a sample input file directory. 4. Launch fuzzing with honggfuzz --input corpus/ --output crashes/ -- ./binary. 5. Track CPU/mem usage via perf stat. 6. Honggfuzz will log crashes with stack traces. 7. Use gdb or crash-analyzer.py to investigate crashes. 8. Save all unique crash samples for further review.
- **Detection**: Honggfuzz crash stats, sanitizer output
- **Solution**: Improve bounds checks, patch vulnerable logic
- **Tags**: honggfuzz, linux, fuzzing, crash-logging, binary-mode

## Multi-Stage Campaign with Seed Minimization

- **Attack Type**: Fuzzing Execution
- **Target**: File Processor
- **Vulnerability**: Unchecked input size
- **MITRE**: T1203
- **Impact**: Performance optimization, faster bug discovery
- **Tools**: AFL++, afl-cmin, afl-tmin
- **Scenario**: Execute a multi-stage campaign by starting with large seed input then minimizing during run.
- **Attack Steps**: 1. Start with a large, varied seed corpus (e.g., mixed PDFs). 2. Run AFL++ fuzzing on the target with this large set. 3. Let it run for several hours while observing system performance. 4. After some time, run afl-cmin to remove redundant seeds. 5. Use afl-tmin on crashing inputs to reduce them to minimal form. 6. Continue fuzzing with this optimized corpus. 7. Track crash rate and CPU utilization to confirm stability.
- **Detection**: Fuzzer stats, minimized crash counts
- **Solution**: Apply minimized crashes in regression test suite
- **Tags**: multi-stage, seed-reduction, afl-cmin, optimization

## Monitoring Fuzzing Campaigns on Remote Servers

- **Attack Type**: Fuzzing Execution
- **Target**: Remote Server
- **Vulnerability**: Input overflows
- **MITRE**: T1203
- **Impact**: Hard-to-detect bugs, resource issues
- **Tools**: AFL++, tmux, Netdata, htop
- **Scenario**: Monitor a fuzzing campaign running on a remote VM using terminal-based and web monitoring tools.
- **Attack Steps**: 1. SSH into remote fuzzing VM and launch AFL++ in tmux. 2. Set up Netdata for real-time CPU/disk monitoring. 3. Regularly check htop inside the tmux session. 4. Configure AFL++ to store all crashes and hang inputs. 5. Periodically scp the crash folder to local system. 6. Use web dashboard (Netdata) to identify any CPU throttling or memory overflows. 7. After run, analyze crashes locally.
- **Detection**: Netdata charts, ssh logs, local triage
- **Solution**: Harden input logic, optimize remote monitoring
- **Tags**: remote-fuzzing, monitoring, tmux, netdata, afl++

## Resource Isolation During Fuzzing

- **Attack Type**: Fuzzing Execution
- **Target**: Local Host
- **Vulnerability**: Resource exhaustion
- **MITRE**: T1496
- **Impact**: More stable fuzzing, fewer false positives
- **Tools**: taskset, cgroups, AFL++, libFuzzer
- **Scenario**: Isolate CPU cores and memory resources to stabilize fuzzing environments.
- **Attack Steps**: 1. Assign specific CPU cores using taskset to AFL/libFuzzer. 2. Create a memory-limited cgroup for the fuzzing process. 3. Launch fuzzing campaign as usual. 4. Monitor usage with top, free, and dmesg for any OOM errors. 5. Ensure fuzzer doesn't starve other system processes. 6. Review crash output for signs of resource starvation. 7. Log performance stability and compare to baseline without isolation.
- **Detection**: cgroup stats, dmesg, top output
- **Solution**: Enforce limits via OS-level tools
- **Tags**: resource-control, taskset, cgroups, fuzz-stability

## Logging Unique Crashes from libFuzzer

- **Attack Type**: Fuzzing Execution
- **Target**: CLI Tool
- **Vulnerability**: Heap buffer overflow
- **MITRE**: T1203
- **Impact**: Unique bug identification
- **Tools**: libFuzzer, crash_logger.py
- **Scenario**: Set up a logging and deduplication pipeline for libFuzzer crash samples.
- **Attack Steps**: 1. Set up libFuzzer with -use_value_profile=1 -max_total_time=7200. 2. Run fuzzer on a vulnerable binary. 3. Log output and stderr to a file. 4. Write or use an existing script (e.g., crash_logger.py) to parse and hash crashes. 5. Store unique crashing inputs in separate directory. 6. Use symbolizer output to correlate crash location. 7. Count frequency of recurring crashes and prioritize.
- **Detection**: Custom crash logs, input hashing
- **Solution**: Deduplicate input, log crash metadata
- **Tags**: libfuzzer, crash-logging, deduplication, triage

## Automated Crash Minimization with afl-tmin

- **Attack Type**: Fuzzing Execution
- **Target**: Application Binary
- **Vulnerability**: Inadequate input validation
- **MITRE**: T1203
- **Impact**: Easier debugging and patching
- **Tools**: AFL++, afl-tmin
- **Scenario**: Use afl-tmin to reduce crashing inputs to the minimal form for effective triage and debugging.
- **Attack Steps**: 1. Run a fuzzing campaign with AFL++. 2. Collect crash samples from crashes/ directory. 3. For each crashing input, run afl-tmin -i crash_sample -o minimized_sample. 4. Confirm minimized sample still crashes the target. 5. Compare size and content of original vs. minimized crash. 6. Document minimization stats. 7. Feed minimized crashes to debugger for faster triage. 8. Store all minimized crashes separately for review.
- **Detection**: Minimization report, debugger confirmation
- **Solution**: Use minimized input in patching and regression test
- **Tags**: afl-tmin, crash-reduction, input-shrinking, triage

## Running AFL++ on a Multimedia Parser

- **Attack Type**: Fuzzing Execution
- **Target**: Media parser binary
- **Vulnerability**: Input validation flaws
- **MITRE**: T1203
- **Impact**: Media playback crashes, DoS
- **Tools**: AFL++, ffmpeg
- **Scenario**: AFL++ is launched on a media parser binary to discover crash-causing input files.
- **Attack Steps**: 1. Instrument the ffmpeg parser with AFL++'s afl-clang-fast.2. Compile ffmpeg with --disable-network to focus on local parsing.3. Create a seed corpus of valid MP4 and AVI files.4. Launch AFL++ using afl-fuzz -i seeds -o findings -- ./ffmpeg @@.5. Monitor CPU and memory usage using htop.6. Enable crash detection via AFL++’s crashes/ folder.7. Collect crash samples and log timestamps.8. Use afl-cmin to minimize crash corpus.9. Categorize crashes by signal type (e.g., SIGSEGV).10. Triage using gdb or asan.
- **Detection**: Monitor AFL++ logs, check crash directories
- **Solution**: Patch parser logic, add input format verification
- **Tags**: afl++, ffmpeg, fuzzing, crash logging

## Fuzzing with libFuzzer on a Compression Library

- **Attack Type**: Fuzzing Execution
- **Target**: Compression library
- **Vulnerability**: Buffer overflows
- **MITRE**: T1203
- **Impact**: Memory corruption, decompression failure
- **Tools**: libFuzzer, zlib
- **Scenario**: Execute libFuzzer against zlib to detect crashes from malformed compressed files.
- **Attack Steps**: 1. Write a fuzz target function in C/C++ that calls uncompress() on input data.2. Compile with clang -fsanitize=fuzzer,address -o fuzz_target fuzz_target.c.3. Prepare seed corpus with small .gz files.4. Run libFuzzer using ./fuzz_target corpus/.5. Observe CPU and memory usage.6. LibFuzzer auto-detects crashes and logs them with stack trace.7. Use AddressSanitizer output to understand memory corruption.8. Minimize crash corpus using llvm-reduce.9. Compare crashes by hash/signature.10. Fix input buffer handling.
- **Detection**: AddressSanitizer traces, libFuzzer crash outputs
- **Solution**: Harden input validation logic
- **Tags**: libFuzzer, zlib, crash reproduction, ASan

## Monitoring Honggfuzz Resource Usage on Server Fuzzing

- **Attack Type**: Fuzzing Execution
- **Target**: grep.<br>8. After run, analyze unique crashes with gdb.<br>9. Use honggfuzz/scripts` to minimize.10. Refactor code based on faults.
- **Vulnerability**: Network daemon
- **MITRE**: Stack overflows, logic bugs
- **Impact**: T1203
- **Tools**: Honggfuzz, htop
- **Scenario**: Honggfuzz is launched on a daemon, while resource use is monitored for stability.
- **Attack Steps**: 1. Instrument a vulnerable server binary using hfuzz-clang.2. Configure honggfuzz with --input corpus/ --output output/ -- ./vuln_server @@.3. Set timeout and memory limits via --rlimit_as.4. Run htop in a separate terminal to monitor CPU and RAM usage.5. Use --threads flag to control load.6. Observe logs for crash entries under output/crashes/.7. Check for zombie processes using `ps aux
- **Detection**: DoS, crash during fuzzing run
- **Solution**: Log files, crash folders, system performance metrics
- **Tags**: Optimize resource control in code

## Minimizing Unique Crashes with afl-cmin

- **Attack Type**: Fuzzing Execution
- **Target**: Any binary
- **Vulnerability**: Input fuzzing edge cases
- **MITRE**: T1203
- **Impact**: Easier triage, reduced triage noise
- **Tools**: AFL++, afl-cmin
- **Scenario**: Use afl-cmin to reduce duplicated crashes discovered during fuzzing.
- **Attack Steps**: 1. Run AFL++ to generate crash corpus in crashes/ folder.2. Identify large number of duplicate inputs.3. Use afl-cmin -i crashes -o minimized -- ./target @@.4. Let the tool determine minimal set of unique inputs causing bugs.5. Validate that minimized inputs still trigger the bug.6. Run sha256sum on all files to confirm uniqueness.7. Open each minimized input in hex editor for analysis.8. Categorize them by signal type (SIGABRT, SIGSEGV).9. Use afl-tmin for even further shrinking.10. Store in triage-ready crash corpus.
- **Detection**: Crash diffing, AFL++ hashes, file size diffs
- **Solution**: Integrate crash minimization into fuzzing pipeline
- **Tags**: afl++, crash minimization, triage

## Executing libFuzzer with Timeout Configuration

- **Attack Type**: Fuzzing Execution
- **Target**: Parsing logic
- **Vulnerability**: Infinite loops, performance bugs
- **MITRE**: T1499
- **Impact**: System hang, CPU hog, resource wastage
- **Tools**: libFuzzer
- **Scenario**: libFuzzer is configured with execution timeout to prevent infinite loops.
- **Attack Steps**: 1. Write fuzz target to test a parsing loop.2. Compile with ASan and fuzzing enabled: clang -fsanitize=fuzzer,address -o fuzzer fuzzer.c.3. Use seed corpus to start: ./fuzzer corpus/.4. Add -timeout=10 to ensure each input is limited to 10 seconds.5. Observe crashes caused by hanging inputs.6. Use gdb to debug whether loop is infinite or long-running.7. Add input validation to reduce parsing loops.8. Log and categorize slow inputs.9. Use libFuzzer stats output to see execution time.10. Re-run minimized inputs with higher timeout.
- **Detection**: Fuzzer timeout messages, logs, ASan stack traces
- **Solution**: Fix infinite loop, add input length checks
- **Tags**: libFuzzer, timeout, crash isolation

## Fuzzing WinAFL on Closed-Source Windows Application

- **Attack Type**: Fuzzing Execution
- **Target**: Windows EXE
- **Vulnerability**: Memory corruption, logic flaws
- **MITRE**: T1218
- **Impact**: Crashes in closed-source software
- **Tools**: WinAFL, DynamoRIO
- **Scenario**: WinAFL is used to fuzz a closed-source EXE by attaching via DynamoRIO.
- **Attack Steps**: 1. Identify target EXE and entry point for fuzzing.2. Install DynamoRIO and configure WinAFL environment.3. Use winafl.dll with afl-fuzz.exe and point to target.exe.4. Provide sample inputs via file or stdin.5. Launch fuzzing with CPU affinity set using -C.6. Observe fuzzer_stats and crash folders.7. Use Process Explorer to monitor memory.8. Configure timeout with -t parameter.9. Save crash samples with .dmp extensions.10. Reproduce crash with WinDbg for triage.
- **Detection**: Debugger logs, memory dumps, WinAFL stats
- **Solution**: Patch binary or mitigate with sandboxing
- **Tags**: winafl, windows, dynamorio, closed-source

## Crash Logging Automation using Custom Bash Script

- **Attack Type**: Fuzzing Execution
- **Target**: Linux binary
- **Vulnerability**: Crash management inefficiency
- **MITRE**: T1203
- **Impact**: Reliable alerting during fuzzing
- **Tools**: AFL++, bash scripting
- **Scenario**: A bash script automates logging of crash events during long fuzz runs.
- **Attack Steps**: 1. Create a script log_crashes.sh.2. Inside, check for new files in AFL++'s crashes/ folder.3. Use inotifywait or find to watch folder every few seconds.4. On detection, copy crash file to logs/ and append timestamp.5. Log crash type using file command.6. Extract signal type from AFL++ metadata.7. Add SHA hash to identify uniqueness.8. Send email or Slack alert using sendmail or webhook.9. Schedule script in cron.10. Review logs daily for triage readiness.
- **Detection**: Crash folder watcher, alert logs
- **Solution**: Use logging tools or integrate into CI pipeline
- **Tags**: crash logging, automation, bash

## Running Fuzzing Campaign in Docker Container

- **Attack Type**: Fuzzing Execution
- **Target**: Any target
- **Vulnerability**: Environment instability
- **MITRE**: T1203
- **Impact**: Safer fuzzing, reproducibility
- **Tools**: Docker, AFL++, libFuzzer
- **Scenario**: Fuzzing is launched in isolated container to prevent host interference.
- **Attack Steps**: 1. Create Dockerfile with base image (e.g., Ubuntu).2. Install dependencies: clang, AFL++, target software.3. Add fuzzing binary and seed corpus into container.4. Expose logs folder to host via -v volume.5. Launch container with docker run -it fuzz-container.6. Start fuzzing via AFL++ or libFuzzer inside.7. Monitor container resource usage using docker stats.8. Collect crashes via mounted volume.9. Tear down after run and archive logs.10. Repeat with varied configurations.
- **Detection**: Docker stats, crash folder mounting
- **Solution**: Isolate fuzzing runs in reproducible containers
- **Tags**: docker, container fuzzing, isolation

## Using afl-whatsup to Track Fuzzer Progress

- **Attack Type**: Fuzzing Execution
- **Target**: Any binary
- **Vulnerability**: Lack of visibility
- **MITRE**: T1203
- **Impact**: Track fuzzing health and coverage
- **Tools**: AFL++, afl-whatsup
- **Scenario**: afl-whatsup gives real-time insight into fuzzing progress and pending crashes.
- **Attack Steps**: 1. Launch AFL++ with multi-instance parallel fuzzing.2. Run afl-whatsup -s out_dir/ to see shared stats.3. Observe execs/sec, pending crashes, hangs.4. Compare which instance is more productive.5. Use afl-plot for visualization.6. Schedule afl-whatsup in cron to record progress.7. Identify when performance dips.8. Restart hung instances manually.9. Correlate crash spikes with test case sets.10. Take snapshot for reporting and sharing.
- **Detection**: Fuzzer stat logs, afl-whatsup terminal output
- **Solution**: Add periodic checks into CI/CD or monitoring tools
- **Tags**: afl++, monitoring, stats, whatsup

## Manual Crash Reproduction for libFuzzer Findings

- **Attack Type**: Fuzzing Execution
- **Target**: C/C++ binary
- **Vulnerability**: Memory read/write issues
- **MITRE**: T1203
- **Impact**: Validation of bug and patch
- **Tools**: libFuzzer, gdb
- **Scenario**: Re-execute crashing inputs from libFuzzer manually for debugging and validation.
- **Attack Steps**: 1. Locate crashing inputs in crash-* files.2. Launch fuzz target with crash input as argument: ./fuzz_target crash-123.3. Attach gdb to observe crash point.4. Use bt for backtrace and info locals.5. Add debug prints or logs to isolate input length or type.6. Run with valgrind to catch memory leaks.7. Check for out-of-bound reads.8. Use llvm-symbolizer for better trace mapping.9. Fix root cause in source code.10. Retest to confirm fix prevents crash.
- **Detection**: Manual execution, gdb, valgrind
- **Solution**: Triage, debugging, libFuzzer, crash reproduction
- **Tags**: https://llvm.org/docs/LibFuzzer.html

## Fuzzing PDF Reader with AFL++ and Crash Logging

- **Attack Type**: Fuzzing Execution
- **Target**: Application
- **Vulnerability**: File Parsing
- **MITRE**: T1203
- **Impact**: Application crash
- **Tools**: AFL++, pdftotext
- **Scenario**: A PDF reader is fuzzed using AFL++ to identify crash-prone input sequences.
- **Attack Steps**: 1. Install AFL++ on the test system. 2. Download a simple PDF reader such as pdftotext. 3. Compile it using afl-gcc to instrument the binary. 4. Create a seed corpus of valid PDF files. 5. Start the fuzzing campaign with AFL++ using the command afl-fuzz -i input_pdfs -o output -m none -- ./pdftotext @@. 6. Monitor CPU and RAM using htop. 7. Observe the output/crashes directory for crashing samples. 8. Use afl-cmin and afl-tmin to minimize input. 9. Debug crashes using gdb. 10. Document crash reports.
- **Detection**: AFL logs, debugger
- **Solution**: Input validation & patching
- **Tags**: fuzzing, AFL++, PDF, crash minimization

## Network Daemon Fuzzing with Honggfuzz

- **Attack Type**: Fuzzing Execution
- **Target**: Server Daemon
- **Vulnerability**: Input overflow, memory corruption
- **MITRE**: T1203
- **Impact**: DoS, RCE
- **Tools**: Honggfuzz
- **Scenario**: Honggfuzz is used to fuzz a custom TCP server to detect memory corruption or crashes.
- **Attack Steps**: 1. Build the target network daemon with hfuzz-clang. 2. Set up a valid seed if applicable. 3. Use honggfuzz -f seeds/ -- ./daemon @@ to begin fuzzing. 4. Monitor CPU and network load with nload, top. 5. Enable Honggfuzz crash logging. 6. Review honggfuzz.log for crash signatures. 7. Use built-in crash minimizer. 8. Re-run minimized samples for reproducibility. 9. Use ASAN to identify memory errors. 10. Patch and document the bug.
- **Detection**: Honggfuzz logs, syslog
- **Solution**: Patch, sanitize input
- **Tags**: honggfuzz, network fuzzing, daemon, crash

## Continuous Fuzzing Campaign using Cron

- **Attack Type**: Fuzzing Execution
- **Target**: CLI Binary
- **Vulnerability**: Input handling flaws
- **MITRE**: T1203
- **Impact**: Consistent crash identification
- **Tools**: AFL++, cron
- **Scenario**: Automating long-running fuzzing using cron and log rotation.
- **Attack Steps**: 1. Create a script to run afl-fuzz with desired arguments. 2. Use cron to run the script daily. 3. Ensure output is redirected to timestamped log files. 4. Monitor disk usage with du and set alerts. 5. Periodically run afl-whatsup to check campaign stats. 6. Archive old crash files automatically. 7. Use logrotate for AFL logs. 8. Periodically use afl-cmin on accumulated crashes. 9. Summarize findings weekly. 10. Clean up unused data.
- **Detection**: Log rotation, campaign stats
- **Solution**: Monitoring, deduplication
- **Tags**: automation, cron, fuzzing loop

## Visual Fuzzing Dashboard for libFuzzer Campaign

- **Attack Type**: Fuzzing Execution
- **Target**: Application
- **Vulnerability**: Memory bugs
- **MITRE**: T1203
- **Impact**: Easier triage and visibility
- **Tools**: libFuzzer, Prometheus, Grafana
- **Scenario**: Creating a visual dashboard to track progress of libFuzzer over time.
- **Attack Steps**: 1. Set up libFuzzer campaign with verbose output. 2. Redirect output to logs. 3. Use a script to parse logs and expose metrics to Prometheus. 4. Install Prometheus and Grafana. 5. Create dashboards with charts for crashes, execs/sec, coverage. 6. Keep track of CPU and memory utilization. 7. Schedule automatic crash triage using crash-min. 8. Use alerts for excessive crashes. 9. Archive all findings with timestamped records. 10. Evaluate crash input quality weekly.
- **Detection**: Grafana charts, alerts
- **Solution**: Dashboard, log metrics
- **Tags**: libFuzzer, visualization, Prometheus

## Fuzzing IoT Device Firmware Emulation

- **Attack Type**: Fuzzing Execution
- **Target**: Embedded firmware
- **Vulnerability**: Input overflow
- **MITRE**: T1203
- **Impact**: Remote access or crash
- **Tools**: AFL++, QEMU
- **Scenario**: QEMU emulation of IoT firmware is fuzzed using AFL++ to discover memory vulnerabilities.
- **Attack Steps**: 1. Extract firmware from IoT device using binwalk. 2. Emulate firmware using QEMU. 3. Identify the binary to fuzz (e.g., httpd). 4. Recompile or wrap it using AFL’s QEMU mode. 5. Create sample corpus for HTTP requests. 6. Launch fuzzing with afl-fuzz -Q. 7. Monitor QEMU memory usage. 8. Analyze crashes using GDB. 9. Use afl-cmin for crash input reduction. 10. Report and patch vulnerable code.
- **Detection**: QEMU logs, AFL stats
- **Solution**: Firmware update, memory fix
- **Tags**: iot, QEMU, firmware fuzzing, crash

## Fuzzing Multimedia Codecs in FFmpeg

- **Attack Type**: Fuzzing Execution
- **Target**: Media application
- **Vulnerability**: Codec parser flaw
- **MITRE**: T1203
- **Impact**: Media playback crash, RCE
- **Tools**: libFuzzer, FFmpeg
- **Scenario**: Fuzzing MP4/AVI codecs in FFmpeg using libFuzzer integration.
- **Attack Steps**: 1. Clone FFmpeg and compile with libFuzzer. 2. Use ./configure --enable-libfuzzer. 3. Create corpus of MP4 and AVI files. 4. Launch with ./fuzzer target_dir. 5. Monitor crash outputs in logs. 6. Use ASAN to capture memory leaks. 7. Triage crash files for minimal reproductions. 8. Use llvm-reduce on inputs. 9. Debug crashes with lldb. 10. Patch codec logic.
- **Detection**: ASAN output, debug logs
- **Solution**: Patch codec, sanitize input
- **Tags**: media fuzzing, codec, libFuzzer

## Remote Fuzzing Setup over SSH

- **Attack Type**: Fuzzing Execution
- **Target**: Remote Linux target
- **Vulnerability**: Input corruption
- **MITRE**: T1203
- **Impact**: Remote crash detection
- **Tools**: AFL++, SSH
- **Scenario**: AFL++ campaign is executed remotely via SSH to utilize cloud CPU.
- **Attack Steps**: 1. Set up a remote Linux server. 2. Install AFL++ remotely. 3. Use SSH keys for password-less login. 4. Transfer target binary and corpus to server. 5. Start fuzzing with screen or tmux. 6. Monitor via SSH tunnel and log sync. 7. Download crash files securely. 8. Use remote debugger to analyze. 9. Use afl-cmin locally. 10. Sync findings with main repo.
- **Detection**: SSH logs, AFL output
- **Solution**: Secure sync, firewall monitoring
- **Tags**: ssh, remote fuzzing, afl++

## Fuzzing CLI Tools Using stdin Mode

- **Attack Type**: Fuzzing Execution
- **Target**: CLI utilities
- **Vulnerability**: Input overflow
- **MITRE**: T1059
- **Impact**: Tool crash or misuse
- **Tools**: AFL++, echo, cat, sort
- **Scenario**: CLI utilities that take input from stdin are fuzzed via AFL’s stdin mode.
- **Attack Steps**: 1. Identify CLI tool that reads from stdin. 2. Instrument using AFL++. 3. Create seed inputs. 4. Launch AFL using afl-fuzz -i in -o out -- ./tool. 5. Use echo piping (echo @@) to simulate input. 6. Monitor CPU and file writes. 7. Analyze output/crashes folder. 8. Use afl-showmap to visualize code coverage. 9. Minimize crashing inputs. 10. Record findings.
- **Detection**: Coverage analysis
- **Solution**: Update CLI input parsing
- **Tags**: afl, cli, stdin fuzzing

## Timeout Management in Long Fuzzing Runs

- **Attack Type**: Fuzzing Execution
- **Target**: Application
- **Vulnerability**: Infinite loops
- **MITRE**: T1499
- **Impact**: Hang, DoS
- **Tools**: AFL++, libFuzzer
- **Scenario**: Use of timeout flags and signal handling to avoid stalling inputs.
- **Attack Steps**: 1. Enable timeout in AFL with -t 5000+. 2. Set per-input timeout in libFuzzer with -timeout=5. 3. Monitor logs for timeouts. 4. Review slow inputs separately. 5. Use afl-tmin to reduce such inputs. 6. Add signal handling in target binary. 7. Restart fuzzing on timeout bursts. 8. Archive hanging cases. 9. Identify infinite loops. 10. Patch accordingly.
- **Detection**: Timeout logs, debugger
- **Solution**: Add timeout protection
- **Tags**: timeout, afl++, libFuzzer

## Multi-Core Fuzzing Campaign with TMUX Sessions

- **Attack Type**: Fuzzing Execution
- **Target**: Multi-core system
- **Vulnerability**: Input parsing
- **MITRE**: T1203
- **Impact**: Higher fuzz throughput
- **Tools**: AFL++, TMUX
- **Scenario**: TMUX is used to manage multi-core fuzzing sessions for improved throughput.
- **Attack Steps**: 1. Start multiple TMUX panes. 2. Launch afl-fuzz on different CPU cores. 3. Use same corpus folder. 4. Monitor each session independently. 5. Rotate input files across cores. 6. Merge findings with afl-cmin. 7. Use afl-whatsup for overview. 8. Backup all crashes daily. 9. Analyze with afl-analyze. 10. Conclude and report campaign.
- **Detection**: TMUX logs, afl-whatsup
- **Solution**: Core utilization and analysis
- **Tags**: multi-core, tmux, afl++

## Fuzzing C++ PDF Parser with Persistent Mode

- **Attack Type**: Fuzzing Execution
- **Target**: Document Parser
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203
- **Impact**: Memory corruption, possible RCE
- **Tools**: libFuzzer, Clang, LLVM, PDF corpus
- **Scenario**: A developer wants to fuzz a PDF parser library written in C++ using libFuzzer’s persistent mode to increase fuzzing throughput.
- **Attack Steps**: 1. Download the PDF parser source code and review its input handling. 2. Compile it using clang++ -fsanitize=fuzzer,address with persistent entry point logic. 3. Create a seed corpus of valid PDFs in a folder. 4. Run the binary with libFuzzer and enable persistent mode. 5. Monitor CPU and RAM using htop or top. 6. Let it run for several hours to allow coverage increase. 7. Collect crashes and use libFuzzer’s automatic minimizer. 8. Analyze crash content using debugger (e.g., lldb).
- **Detection**: Fuzzer logs, sanitizer output
- **Solution**: Harden memory access, update PDF parsing logic
- **Tags**: libFuzzer, persistent, pdf, crash

## Running Multiple AFL++ Instances in Parallel

- **Attack Type**: Fuzzing Execution
- **Target**: Media Decoder
- **Vulnerability**: File Parsing Flaws
- **MITRE**: T1203
- **Impact**: DoS or execution via malformed audio files
- **Tools**: AFL++, afl-multicore
- **Scenario**: To maximize coverage, a researcher runs AFL++ in parallel mode with multiple instances targeting an audio decoder.
- **Attack Steps**: 1. Install AFL++ with multicore support. 2. Set up the target audio decoder and compile with AFL instrumentation. 3. Create a valid audio file corpus (e.g., WAV). 4. Start a master instance using AFL_MASTER=1 afl-fuzz -i in -o out -M master ./decoder. 5. Start slave instances using -S slave1, -S slave2, etc. 6. Let them sync via shared output folder. 7. Periodically check crashes in the out/crashes folder. 8. Use afl-cmin to minimize corpus. 9. Review CPU usage to avoid overload.
- **Detection**: AFL crash dir, sync folder analysis
- **Solution**: Fix file parsing bounds and size checks
- **Tags**: afl++, parallel fuzzing, wav

## Network Protocol Fuzzing via Honggfuzz

- **Attack Type**: Fuzzing Execution
- **Target**: Network Daemon
- **Vulnerability**: Input validation over network
- **MITRE**: T1203
- **Impact**: Network DoS or crash
- **Tools**: Honggfuzz, netcat, custom server
- **Scenario**: Fuzzing a custom TCP protocol implemented in a server binary by piping mutated inputs into a socket.
- **Attack Steps**: 1. Instrument the server binary with honggfuzz compiler wrappers. 2. Create a simple client script that connects to the TCP port and sends fuzzed input. 3. Set Honggfuzz to run in persistent network mode. 4. Point it to the binary with --fuzz_mode NETDRIVER. 5. Define target port and input length. 6. Run the fuzzer and monitor open sockets. 7. Check logs for server-side crashes. 8. Capture crash inputs and replay them using netcat. 9. Use Wireshark to analyze malformed packets.
- **Detection**: Wireshark, server logs, Honggfuzz crashes
- **Solution**: Patch protocol parser logic
- **Tags**: honggfuzz, network fuzzing, tcp

## Crash Minimization with afl-tmin

- **Attack Type**: Fuzzing Execution
- **Target**: Native Binary
- **Vulnerability**: Malformed file input
- **MITRE**: T1203
- **Impact**: Easier bug triage and patching
- **Tools**: afl-tmin, AFL++, crashing input
- **Scenario**: After finding multiple crash cases, a researcher uses afl-tmin to reduce a crashing input to the minimal necessary payload.
- **Attack Steps**: 1. Identify a crashing input sample from the AFL crashes directory. 2. Copy it to a separate folder. 3. Run afl-tmin -i crash_input -o minimized -t 2000 -- ./target_binary. 4. Let afl-tmin attempt reduction while preserving crash. 5. Compare file sizes before and after. 6. Analyze minimized input in hex editor. 7. Validate it still causes the same crash. 8. Use minimized input for reproducibility and debugging.
- **Detection**: Manual reproduction of crash
- **Solution**: Keep minimized corpus and triage crashes
- **Tags**: crash minimization, afl, tmin

## Fuzzing Command Line Apps via stdin

- **Attack Type**: Fuzzing Execution
- **Target**: CLI Tool
- **Vulnerability**: Input handling over stdin
- **MITRE**: T1203
- **Impact**: Viewer crash or DoS
- **Tools**: AFL++, stdin mode
- **Scenario**: A CLI image viewer reads from stdin. The researcher uses AFL++ to fuzz it by piping inputs.
- **Attack Steps**: 1. Download the CLI app and review how it reads input. 2. Compile with AFL++ instrumentation. 3. Create seed image files (e.g., BMP). 4. Use afl-fuzz -i inputs -o findings -- ./viewer and pipe data to stdin. 5. Monitor CPU and memory to prevent overload. 6. Let the fuzzer run for several hours. 7. Collect crash files. 8. Use debugger to analyze segfault. 9. Save minimized crash-inducing inputs.
- **Detection**: stderr logs, dmesg, afl output
- **Solution**: Harden stdin input handling
- **Tags**: stdin, afl++, viewer, bmp

## Scheduling Fuzzing on a Cluster

- **Attack Type**: Fuzzing Execution
- **Target**: Windows Application
- **Vulnerability**: Memory corruption
- **MITRE**: T1218
- **Impact**: Remote execution or crash
- **Tools**: WinAFL, PsExec, Windows Task Scheduler
- **Scenario**: A researcher schedules distributed fuzzing across multiple VMs using WinAFL and batch jobs.
- **Attack Steps**: 1. Prepare target binary with DynamoRIO instrumentation. 2. Set up WinAFL on each VM. 3. Share seed corpus and configure AFL folder sharing. 4. Write a batch script to launch WinAFL instances on each VM. 5. Use PsExec or Task Scheduler to trigger scripts remotely. 6. Monitor fuzzing logs for each instance. 7. Collect crashes from shared folder. 8. Merge results into centralized report. 9. Triage top crashes using debugger.
- **Detection**: Debug logs, Windows crash dump
- **Solution**: Fix buffer and input errors
- **Tags**: winafl, distributed, windows

## CPU Usage Bottleneck While Fuzzing

- **Attack Type**: Fuzzing Execution
- **Target**: System Optimization
- **Vulnerability**: CPU throttling
- **MITRE**: T1496
- **Impact**: Slow fuzzing speed
- **Tools**: AFL++, htop, system tuning
- **Scenario**: Fuzzing slows down due to CPU bottlenecks; user identifies and fixes it for optimal performance.
- **Attack Steps**: 1. Launch fuzzer and observe slow progress. 2. Open htop and notice CPU pinned or high context switches. 3. Confirm turbo boost or power saving is limiting cores. 4. Tune /etc/default/grub to enable full performance. 5. Restart system. 6. Use taskset to bind fuzzer to specific core. 7. Relaunch AFL++ and monitor execution speed. 8. Notice improved exec/sec. 9. Maintain high-performance profile for future fuzzing.
- **Detection**: Execution rate monitoring
- **Solution**: CPU tuning, disable power saving
- **Tags**: afl++, cpu, htop, tuning

## Fuzzing Large Inputs with libFuzzer

- **Attack Type**: Fuzzing Execution
- **Target**: Video Transcoder
- **Vulnerability**: Buffer overflow from large input
- **MITRE**: T1203
- **Impact**: OOM or heap corruption
- **Tools**: libFuzzer, video encoder
- **Scenario**: A researcher tests a video transcoder that reads large input buffers. libFuzzer is configured to handle 5MB+ inputs.
- **Attack Steps**: 1. Download video transcoder source. 2. Instrument with -fsanitize=fuzzer,address. 3. Create initial corpus with large MP4/MKV files. 4. Set max_len=5242880 in fuzz target. 5. Run libFuzzer with -max_total_time=3600. 6. Ensure system has enough RAM. 7. Let fuzzer mutate large files. 8. Watch for OOM crashes or slowdowns. 9. Analyze crash logs using ASAN.
- **Detection**: Crash logs, sanitizer output
- **Solution**: Limit input length, fix bounds
- **Tags**: libfuzzer, large input, video

## Using afl-cmin to Minimize Corpus

- **Attack Type**: Fuzzing Execution
- **Target**: Binary App
- **Vulnerability**: Input bloat
- **MITRE**: T1499
- **Impact**: Reduced performance, storage issues
- **Tools**: AFL++, afl-cmin
- **Scenario**: After corpus bloating, researcher uses afl-cmin to reduce input set for faster re-runs.
- **Attack Steps**: 1. Run fuzzer for several hours. 2. Observe input corpus grows too large. 3. Run afl-cmin -i inputs -o min_corpus -- ./target_binary. 4. Let cmin deduplicate and minimize files. 5. Validate that new corpus still triggers coverage. 6. Use reduced corpus for faster re-runs. 7. Track which inputs cover which paths. 8. Periodically re-minimize as corpus grows again.
- **Detection**: File count, size stats
- **Solution**: Use minimized corpus
- **Tags**: afl++, corpus, cmin, trim

## Logging Crashes with Custom Scripts

- **Attack Type**: Fuzzing Execution
- **Target**: Any Binary
- **Vulnerability**: Crash variety
- **MITRE**: T1005
- **Impact**: Improved triage and organization
- **Tools**: AFL++, Python
- **Scenario**: A researcher writes a Python script to organize crash logs from AFL output.
- **Attack Steps**: 1. Write a Python script to scan out/crashes. 2. Parse crash filenames for IDs and timestamps. 3. Group crashes by signal or hash. 4. Save metadata to CSV. 5. Optionally launch debugger automatically. 6. Visualize crash types using matplotlib. 7. Schedule script as cron job during fuzzing. 8. Sync logs to backup server. 9. Use crash info for bug triage.
- **Detection**: Custom crash reports
- **Solution**: Automate crash tracking
- **Tags**: afl++, crash script, triage

## Debugging a Heap Overflow Crash with GDB

- **Attack Type**: Crash Reproduction
- **Target**: Linux Binary
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203.001
- **Impact**: Application crash, DoS
- **Tools**: AFL++, GDB, libc debug symbols
- **Scenario**: A Linux binary fuzzed with AFL++ crashes due to a heap overflow.
- **Attack Steps**: 1. Launch the target binary manually with the crash-inducing input.2. Start GDB with the target: gdb ./vulnerable_app.3. Use run < crash_input to load the crash input.4. Observe where the crash occurs (e.g., in free() or memcpy).5. Use backtrace to identify the exact crash location.6. Analyze variables and memory using print, x, or info. 7. Note any abnormal pointer behavior that could indicate overflow.8. Isolate the function responsible for allocation and misuse.9. Document crash location and root cause.10. Prepare a crash report.
- **Detection**: GDB crash logs, system logs
- **Solution**: Patch memory allocation routines
- **Tags**: fuzzing, GDB, heap overflow, debug, triage

## Triage Use-After-Free Bug with ASan Output

- **Attack Type**: Fault Injection
- **Target**: C++ Program
- **Vulnerability**: Use-After-Free
- **MITRE**: T1203
- **Impact**: Potential RCE, Memory Corruption
- **Tools**: libFuzzer, AddressSanitizer, Clang
- **Scenario**: A libFuzzer test triggers a UAF, reported by AddressSanitizer.
- **Attack Steps**: 1. Compile the binary with ASan flags: -fsanitize=address.2. Run the libFuzzer target with crash input: ./fuzzer < crash_input.3. Observe ASan output in terminal—it will show the error type and backtrace.4. Note heap location and where memory was freed.5. Use the stack trace to find functions involved.6. Trace the object lifetime manually.7. If needed, attach GDB and re-run the input for step-through analysis.8. Confirm if dangling pointer is used post-free.9. Generate a minimal reproduction input.10. Document analysis.
- **Detection**: ASan output with stack trace
- **Solution**: Fix object lifetime, add smart pointers
- **Tags**: ASan, use-after-free, sanitizer, fuzzing

## Exploitability Check in WinDbg

- **Attack Type**: Exploitability Check
- **Target**: Windows App
- **Vulnerability**: NULL Pointer Dereference
- **MITRE**: T1003.005
- **Impact**: Denial of Service or code execution
- **Tools**: WinDbg, !exploitable, MiniDump
- **Scenario**: A Windows crash dump needs analysis to check if it's exploitable.
- **Attack Steps**: 1. Open WinDbg and load the crash dump file: File > Open Crash Dump.2. Wait for symbols to load fully.3. Type !analyze -v to see crash details.4. Use !exploitable to get a verdict: Exploitable, Probably Exploitable, etc.5. Navigate the stack trace for source of crash.6. Set breakpoints and re-run if live process is available.7. Look for corrupt return addresses or EIP control.8. Note user-mode vs kernel-mode location.9. Document exploitability score and call site.10. Store report with annotated dump.
- **Detection**: WinDbg + !exploitable analysis
- **Solution**: Patch input validation or pointer safety
- **Tags**: WinDbg, !exploitable, triage, crash

## Minimizing Crash Input with afl-cmin

- **Attack Type**: Crash Minimization
- **Target**: Linux Binary
- **Vulnerability**: Input Handling Bug
- **MITRE**: T1203
- **Impact**: Faster reproduction and testing
- **Tools**: afl-cmin, AFL++, bash tools
- **Scenario**: A crash input is too large; researcher wants to minimize it for fast reproduction.
- **Attack Steps**: 1. Place the crashing input in a directory, e.g., crashes/.2. Run: afl-cmin -i crashes -o minimized -t 5000 -- ./target_app @@.3. afl-cmin will remove unneeded parts while retaining the crash behavior.4. Run the minimized input against the binary to confirm it still crashes.5. Use tools like hexdump or diff to compare original vs minimized input.6. Attach debugger for faster triage with smaller input.7. Store minimized input for future testing.8. Document difference in execution time.9. Add to corpus if still useful.10. Backup original and minimized inputs.
- **Detection**: Manual testing + minimized input result
- **Solution**: Reduce test input while retaining crash trigger
- **Tags**: afl-cmin, crash input, fuzzing, triage

## Reproducing Stack Buffer Overflow in LLDB

- **Attack Type**: Crash Reproduction
- **Target**: macOS Binary
- **Vulnerability**: Stack Buffer Overflow
- **MITRE**: T1068
- **Impact**: Possible EIP/RIP control, shell access
- **Tools**: LLDB, ASan, afl-tmin
- **Scenario**: Fuzzer found a stack overflow; analysis is done using LLDB on macOS.
- **Attack Steps**: 1. Open the app in LLDB: lldb ./app.2. Use run < crash_input to trigger the crash.3. Use bt to examine the backtrace.4. Use frame variable to inspect buffer values.5. Identify overwritten return address or corrupted stack.6. Use disassemble to analyze instructions at crash point.7. Compare input data with memory layout.8. Minimize input using afl-tmin for faster iteration.9. Document the exact location and instruction that crashed.10. Save LLDB session log.
- **Detection**: LLDB + ASan + input replay
- **Solution**: Fix buffer sizes, use safe string APIs
- **Tags**: LLDB, stack overflow, macOS, fuzzing

## Undefined Behavior via UBSan Log

- **Attack Type**: Fault Injection
- **Target**: C++ App
- **Vulnerability**: Type Mismatch, Integer Wrap
- **MITRE**: T1203.003
- **Impact**: Logic bugs, unintentional behavior
- **Tools**: UBSan, Clang, libFuzzer
- **Scenario**: An input triggers undefined behavior detected by UBSan.
- **Attack Steps**: 1. Compile target with -fsanitize=undefined.2. Run the fuzzing binary with problematic input.3. UBSan prints detailed output of undefined behavior (e.g., shift by negative, type confusion).4. Note file, line number, and faulty expression from logs.5. Trace the code path using debugger.6. Confirm input path that leads to undefined behavior.7. Generate a PoC or minimized sample.8. Assess potential for memory corruption or logic flaw.9. Fix using stronger typing or logic correction.10. Store log for audit trail.
- **Detection**: UBSan logs + code audit
- **Solution**: Fix code with better type checks
- **Tags**: UBSan, undefined behavior, crash, sanitizer

## Categorizing Crashes by Stack Hashing

- **Attack Type**: Crash Deduplication
- **Target**: Linux Binaries
- **Vulnerability**: Multiple
- **MITRE**: T1595.002
- **Impact**: Efficient triage, faster debugging
- **Tools**: afl-collect, stack hashing script
- **Scenario**: 100s of crash samples need grouping into unique categories.
- **Attack Steps**: 1. Collect crash inputs from AFL’s crashes/ directory.2. Use afl-collect or a script to batch-test all crashes.3. For each crash, generate a stack trace using GDB or ASan.4. Compute a hash based on top N stack frames.5. Group inputs with identical stack hashes.6. Verify crash location remains consistent.7. Select representative input per group.8. Minimize crash set to unique bugs.9. Update internal bug tracker with grouped entries.10. Delete redundant inputs to save space.
- **Detection**: Stack trace comparison
- **Solution**: Group similar crashes into families
- **Tags**: deduplication, crash analysis, fuzzing

## Identifying Heap Leak via Valgrind

- **Attack Type**: Memory Leak Analysis
- **Target**: C/C++ App
- **Vulnerability**: Memory Leak
- **MITRE**: T1203.004
- **Impact**: Resource exhaustion, DoS
- **Tools**: Valgrind, Memcheck, crash input
- **Scenario**: Fuzzing leads to memory leaks; need to find exact location.
- **Attack Steps**: 1. Install Valgrind and run the binary with crash input: valgrind ./app < crash_input.2. Observe any memory leaks or invalid writes.3. Note stack trace and allocation location.4. Cross-reference with source code if available.5. Identify whether it's a leak, double free, or UAF.6. Confirm using multiple inputs.7. If persistent across fuzzing runs, classify as a bug.8. Fix memory deallocation logic.9. Retest with Valgrind.10. Document findings in bug report.
- **Detection**: Valgrind memory leak report
- **Solution**: Fix faulty allocation/deallocation paths
- **Tags**: valgrind, memory leak, triage, debug

## Exploit Potential via RIP Overwrite

- **Attack Type**: Exploitability Check
- **Target**: Linux App
- **Vulnerability**: Instruction Pointer Overwrite
- **MITRE**: T1055.012
- **Impact**: Code Execution, Privilege Escalation
- **Tools**: GDB, EIP overwrite input, debugger script
- **Scenario**: A crash shows overwritten RIP/EIP; check if attacker can control it.
- **Attack Steps**: 1. Load binary in GDB with input: gdb ./vuln.2. Use run < input and observe if crash occurs.3. Check if RIP register is overwritten by input data.4. Use x/20x $rsp to inspect stack contents.5. Find pattern offset using pattern_create and pattern_offset (Metasploit tools).6. Confirm attacker control over instruction pointer.7. Document if shellcode can be injected.8. Prepare report with control-flow hijack diagram.9. If exploit chain is feasible, note preconditions.10. Mark as high severity in bug tracker.
- **Detection**: Register analysis, crash pattern analysis
- **Solution**: Input bounds check, stack canary, ASLR
- **Tags**: exploitability, RIP overwrite, debug, crash

## Visualizing Crash Graphs via Timesketch

- **Attack Type**: Triage Visualization
- **Target**: Binary Corpus
- **Vulnerability**: Multiple
- **MITRE**: T1592
- **Impact**: Faster insight into fuzzing performance
- **Tools**: Timesketch, custom script, logs
- **Scenario**: Want to visualize crash timelines or patterns across time and binaries.
- **Attack Steps**: 1. Export crash timestamps and metadata to CSV.2. Include fields like filename, crash time, hash, binary version.3. Upload to Timesketch.4. Create timeline and tag types of crashes (heap, stack, logic).5. Use filters to analyze spike patterns.6. Identify bursts of crashes indicating vulnerable states.7. Correlate with fuzzer configuration or changes.8. Export graphs for reports.9. Use clustering to isolate unique behaviors.10. Archive visual data as part of triage.
- **Detection**: Crash timeline correlation
- **Solution**: Improve fuzzer path discovery or input generation
- **Tags**: crash analysis, timeline, visualization, triage

## Reproducing a Heap Overflow in PDF Parser

- **Attack Type**: Heap-Based Crash
- **Target**: PDF Parser Tool
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203
- **Impact**: Possible Arbitrary Code Execution
- **Tools**: GDB, AddressSanitizer, afl-tmin
- **Scenario**: A fuzzed PDF parser crashes due to heap overflow in object reference handling.
- **Attack Steps**: 1. Locate crash-inducing PDF sample in AFL's crashes directory.2. Launch target PDF parser inside GDB: gdb --args ./pdf_parser crash_sample.pdf.3. Run the sample to trigger the crash and inspect output.4. Use bt to view backtrace and identify the exact vulnerable function.5. Enable AddressSanitizer to observe memory violation logs.6. Use afl-tmin to minimize the crashing PDF.7. Document function and line where the heap overwrite occurred.8. Evaluate whether controlled data influences control flow.
- **Detection**: ASan logs, GDB trace, crash consistency
- **Solution**: Add bounds check for object array size
- **Tags**: fuzzing, heap, crash-reproduction, ASan

## ASan Analysis of Use-After-Free Crash

- **Attack Type**: Use-After-Free
- **Target**: Desktop App
- **Vulnerability**: Use-After-Free
- **MITRE**: T1203
- **Impact**: Memory corruption
- **Tools**: AddressSanitizer, GDB
- **Scenario**: Application crashes on dynamic object reallocation detected by ASan.
- **Attack Steps**: 1. Execute the crashing input using the target binary compiled with -fsanitize=address.2. ASan logs reveal heap-use-after-free at specific memory offset.3. Open debugger (GDB) and run the same input to observe where freed memory is accessed.4. Use watch to track the pointer's lifecycle.5. Identify how a stale pointer is reused after deletion.6. Confirm trigger condition is repeatable.7. Generate PoC steps in a reproducible format.8. Document vulnerable code block and patch it to nullify or reallocate pointers post-delete.
- **Detection**: ASan backtrace and GDB live tracking
- **Solution**: Reuse pointer only post-validation
- **Tags**: memory, sanitizer, use-after-free, root-cause

## WinDbg Triage of Windows Media Player RCE

- **Attack Type**: Media File Exploit
- **Target**: Windows Media Player
- **Vulnerability**: Malformed Media Header
- **MITRE**: T1203
- **Impact**: Remote Code Execution
- **Tools**: WinDbg, !exploitable, WinAFL
- **Scenario**: Windows media player crashes on malformed audio header in MP3.
- **Attack Steps**: 1. Launch Windows Media Player in WinDbg with crashing MP3 sample: windbg wmplayer.exe crash.mp3.2. Let playback initiate and wait for crash to occur.3. Run !exploitable -v to check crash exploitability rating.4. Review exception info and disassembly window to find crashing instruction.5. Use u and kb to walk the call stack and locate faulting routine.6. Log potential attacker-controlled offsets.7. Reduce MP3 to smallest crashing header using manual byte editing.8. Cross-reference bytes to official MP3 header spec for patching guidance.
- **Detection**: WinDbg exception and exploitability plugin
- **Solution**: Validate input header length before parsing
- **Tags**: RCE, WinDbg, audio crash, PoC

## LLDB Debug of iOS Binary Crash

- **Attack Type**: Mobile App Crash
- **Target**: iOS Mobile App
- **Vulnerability**: Input Parsing Flaw
- **MITRE**: T1621
- **Impact**: App crash or data exposure
- **Tools**: LLDB, Honggfuzz, iOS crash logs
- **Scenario**: An iOS application fuzzed with honggfuzz crashes on malformed image input.
- **Attack Steps**: 1. Identify crashing input image generated by honggfuzz.2. Transfer it to test device or emulator.3. Attach LLDB to the app using lldb attach <PID>.4. Reproduce crash and log the crashing instruction.5. Use thread backtrace all to trace the origin function.6. Extract device crash logs to correlate with fuzzing report.7. Analyze if user-controlled image header triggers bad memory dereference.8. Document memory layout and suggest validation for header fields.
- **Detection**: LLDB trace, iOS crash log
- **Solution**: Harden image parsing function
- **Tags**: fuzzing, iOS, LLDB, mobile, crash triage

## Triaging Stack Overflow in Image Library

- **Attack Type**: Stack Overflow
- **Target**: Image Processing App
- **Vulnerability**: Stack Overflow (Recursion)
- **MITRE**: T1203
- **Impact**: DoS or potential RCE
- **Tools**: libFuzzer, ASan, GDB
- **Scenario**: Crashing input causes uncontrolled recursion in image decoding.
- **Attack Steps**: 1. Compile image decoder with -fsanitize=address and -g flags.2. Use libFuzzer to generate crash-inducing image file.3. Run in GDB: gdb ./image_decoder crash.jpg.4. Crash occurs deep in recursive image parsing loop.5. ASan indicates stack exhaustion before return boundary.6. View function call tree and determine base recursion condition.7. Refactor image parser to include recursion depth check.8. Document function, input byte patterns, and failure reason.
- **Detection**: ASan logs, GDB stack depth analysis
- **Solution**: Add max recursion depth limit
- **Tags**: fuzzing, image, stack overflow, sanitizer

## Use of gdb-exploitable Plugin for Linux

- **Attack Type**: Null Pointer Dereference
- **Target**: Linux Binary
- **Vulnerability**: Null Pointer Dereference
- **MITRE**: T1203
- **Impact**: Low severity crash
- **Tools**: GDB, gdb-exploitable, afl-cmin
- **Scenario**: Linux binary crashes on invalid pointer dereference.
- **Attack Steps**: 1. Load crashing sample into GDB: gdb ./vuln_binary.2. Run input until segmentation fault triggers.3. Install and use exploitable.py plugin:source exploitable.py, then run exploitable.4. Output shows "PROBABLY_NOT_EXPLOITABLE" for null dereference.5. Backtrace confirms null pointer used without validation.6. Use afl-cmin to minimize input for easier triage.7. Fix input validation before dereferencing.8. Log vulnerability type and non-exploitability tag.
- **Detection**: GDB + gdb-exploitable classification
- **Solution**: Check for null before pointer dereference
- **Tags**: triage, null deref, Linux, fuzzing

## Crash Minimization with afl-tmin

- **Attack Type**: Crash Minimization
- **Target**: CLI Application
- **Vulnerability**: Redundant Fuzzed Input
- **MITRE**: T1203
- **Impact**: Efficient triage workflow
- **Tools**: afl-tmin, GDB, AddressSanitizer
- **Scenario**: AFL crash sample has redundant bytes; must be minimized for root cause focus.
- **Attack Steps**: 1. Select large crash sample file from AFL’s crashes directory.2. Use afl-tmin with correct binary: afl-tmin -i crash_input -o min_input -- ./target_binary @@.3. afl-tmin reduces input to bare-minimum bytes required to trigger crash.4. Validate minimized input in GDB with ASan enabled.5. Observe whether crash location changes — if not, minimization successful.6. Store minimized input as PoC.7. Use hex editor to inspect which bytes were trimmed.8. Use this input for patch testing or further exploit analysis.
- **Detection**: Output comparison pre/post minimization
- **Solution**: Integrate minimized test cases into CI triage
- **Tags**: crash-reduction, PoC, afl-tmin, triage

## Logging and Reproducing Repeated Hangs

- **Attack Type**: Resource Starvation
- **Target**: Desktop Application
- **Vulnerability**: Infinite Loop / Hang
- **MITRE**: T1499
- **Impact**: Denial of Service (Hang)
- **Tools**: GDB, Timeout Logger, afl-fuzz
- **Scenario**: Fuzzed input leads to infinite loop causing app to hang instead of crash.
- **Attack Steps**: 1. Review AFL logs showing timeouts for specific test case.2. Manually run the test case in GDB.3. App enters infinite loop, using 100% CPU with no crash.4. Use Ctrl+C in GDB to interrupt and analyze loop logic.5. Set breakpoints to observe conditions being checked.6. Identify logic flaw (e.g., improper loop exit condition).7. Mark this sample as logic flaw vs memory bug.8. Patch code to break or timeout on long iterations.
- **Detection**: Fuzzer timeouts, GDB loop inspection
- **Solution**: Add loop guards or timeouts
- **Tags**: hang, DoS, fuzzing, infinite-loop

## LLDB with Sanitizer Integration on macOS

- **Attack Type**: Memory Corruption
- **Target**: macOS Binary
- **Vulnerability**: Undefined Behavior (Shift)
- **MITRE**: T1203
- **Impact**: Logic corruption, crash
- **Tools**: LLDB, UBSan, Clang
- **Scenario**: macOS app compiled with UBSan crashes due to undefined shift operation.
- **Attack Steps**: 1. Compile binary with -fsanitize=undefined.2. Fuzz app until crash occurs.3. Attach LLDB to running app or launch it with minimized input.4. UBSan log flags a shift of negative value on signed integer.5. Use LLDB thread backtrace to trace the call chain.6. Review variable causing shift issue.7. Reproduce using reduced input to confirm crash.8. Fix involves using unsigned variable or adding bounds check before shift.
- **Detection**: UBSan logs, LLDB backtrace
- **Solution**: Sanitize shift operations
- **Tags**: macOS, UBSan, LLDB, fuzzing

## Tracking Crash Origin with Valgrind

- **Attack Type**: Memory Leak / Crash
- **Target**: Parser Binary
- **Vulnerability**: Memory Leak + Dangling Pointer
- **MITRE**: T1203
- **Impact**: Stability + Security Impact
- **Tools**: Valgrind, GDB, afl-fuzz
- **Scenario**: Crashing app leaks memory and crashes during large input parsing.
- **Attack Steps**: 1. Run target binary with Valgrind: valgrind ./target crash_input.2. Observe memory errors including invalid writes and leaks.3. Use --leak-check=full and --track-origins=yes flags.4. Combine with GDB to run step-by-step and locate offending function.5. Confirm whether freed memory is being reused.6. Patch to fix ownership and reuse tracking.7. Mark crash as potentially exploitable if write crosses boundaries.8. Generate full repro steps with minimal input.
- **Detection**: Valgrind output, heap trace
- **Solution**: Resolve memory leaks and reuse issues
- **Tags**: memory-leak, valgrind, crash-reproduction

## Reproducing Heap Overflow with GDB

- **Attack Type**: Crash Reproduction
- **Target**: Linux Binary
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203
- **Impact**: Application crash, potential RCE
- **Tools**: GDB, AFL, ASan
- **Scenario**: A researcher needs to reproduce a heap overflow found by AFL in a Linux application.
- **Attack Steps**: 1. Identify the crashing input file in AFL's crashes/ directory. 2. Open the target binary with GDB using gdb --args ./target input_file. 3. Run the program inside GDB and observe the crash location. 4. Enable ASan to get detailed memory violation logs. 5. Examine the call stack to trace the heap buffer overflow. 6. Set breakpoints on malloc/free to inspect heap behavior. 7. Record crash logs for documentation. 8. Re-run the input multiple times to confirm reproducibility. 9. Save debugger output and ASan trace. 10. Label the crash severity and pass to triage team.
- **Detection**: ASan logs, GDB crash output
- **Solution**: Validate heap operations, patch input parsing
- **Tags**: crash-triage, heap-overflow, gdb, ASan

## Use-After-Free Reproduction in WinDbg

- **Attack Type**: Memory Corruption
- **Target**: Windows App
- **Vulnerability**: Use-After-Free
- **MITRE**: T1621
- **Impact**: Memory corruption
- **Tools**: WinDbg, !heap, !exploitable
- **Scenario**: A crash involving use-after-free is identified on a Windows desktop app via fuzzing.
- **Attack Steps**: 1. Load the target application in WinDbg with windbg.exe target.exe. 2. Open the crash input via File → Open or command line. 3. Let the program crash and observe access violations. 4. Use !analyze -v to review the crash context. 5. Use !heap -p and !heap -stat to inspect freed memory allocations. 6. Confirm dangling pointer access to freed memory. 7. Cross-reference with crash report timestamps. 8. Run the input multiple times to confirm behavior. 9. Export logs and mark PoC as reproducible. 10. Forward details to developers for patching.
- **Detection**: WinDbg crash trace, !exploitable plugin
- **Solution**: Fix memory lifecycle bugs, add bounds checks
- **Tags**: crash-debugging, uaf, windbg, windows

## Triaging Null Pointer Dereference Crash

- **Attack Type**: Fault Injection
- **Target**: Linux Binary
- **Vulnerability**: Null Pointer Dereference
- **MITRE**: T1499
- **Impact**: Denial of Service
- **Tools**: GDB, LLDB, ASan
- **Scenario**: Fuzzer triggers a null pointer dereference in a parser application.
- **Attack Steps**: 1. Run the target application with crashing input using gdb --args. 2. Observe the SIGSEGV or invalid memory read. 3. Use backtrace and info locals to analyze pointer state. 4. Confirm if the pointer was never initialized or was freed early. 5. Enable AddressSanitizer to log detailed trace. 6. Compare execution with and without input file. 7. Save ASan logs and GDB backtrace. 8. Classify the issue severity (DoS vs RCE). 9. Submit PoC along with stack trace. 10. Recommend null checks in sensitive code paths.
- **Detection**: ASan logs, segmentation fault
- **Solution**: Add pointer checks, fix memory init patterns
- **Tags**: null-pointer, crash-triage, debug-analysis

## Minimizing Fuzzer Input with afl-tmin

- **Attack Type**: Crash Minimization
- **Target**: Application Binary
- **Vulnerability**: Input Handling Flaw
- **MITRE**: T1595
- **Impact**: DoS, Exploit Proof Creation
- **Tools**: afl-tmin, AFL++, GDB
- **Scenario**: A large crashing input is reduced to its essential bytes to isolate root cause.
- **Attack Steps**: 1. Copy the crashing input from AFL's crashes/ directory. 2. Run afl-tmin -i crash_file -o minimized_file -- ./target @@. 3. Allow the minimization to complete — it will reduce the file to smallest form that still crashes. 4. Test minimized file in GDB or LLDB to ensure it reproduces the crash. 5. Compare minimized vs original input to understand crash trigger. 6. Use hex editors to observe key payloads. 7. Save minimized file as final PoC. 8. Document the crash condition and code path triggered. 9. Correlate with logs from earlier fuzzing campaign. 10. Tag the file with metadata for triage.
- **Detection**: Fuzzer crash consistency, minimized PoC
- **Solution**: Use stricter input validation, patch logic
- **Tags**: input-minimization, afl, PoC, triage

## Identifying Format String Bug in Logs

- **Attack Type**: Crash Reproduction
- **Target**: Linux App
- **Vulnerability**: Format String Vulnerability
- **MITRE**: T1203
- **Impact**: Memory leak, potential RCE
- **Tools**: GDB, LLDB, printf logs, ASan
- **Scenario**: Crash due to unescaped user input used in printf-style logging system.
- **Attack Steps**: 1. Use GDB to launch the crashing binary with crafted input. 2. Observe crash location inside a printf() call. 3. Check if user input contains %x, %s, or %n specifiers. 4. Enable ASan or Valgrind to confirm memory access issues. 5. Use info registers to inspect register corruption. 6. Isolate the exact input that caused format string injection. 7. Re-run the input with debugger watchpoints. 8. Save ASan/Valgrind output. 9. Document how attacker-controlled format string corrupted execution. 10. Recommend format-safe logging techniques.
- **Detection**: ASan logs, control-flow corruption
- **Solution**: Use snprintf-style safe formatting
- **Tags**: format-bug, debug, printf, crash-analysis

## Validating Exploitability with GDB Plugin

- **Attack Type**: Exploitability Check
- **Target**: Linux Binary
- **Vulnerability**: Heap Overflow, UAF
- **MITRE**: T1588
- **Impact**: Exploit risk determination
- **Tools**: GDB, gdb-exploitable plugin
- **Scenario**: Fuzzer crash needs analysis to determine if it’s exploitable or just a DoS.
- **Attack Steps**: 1. Open the binary with crashing input in GDB. 2. Load exploitable plugin using source exploitable.py. 3. Run the input until crash occurs. 4. Use exploitable command to classify the crash (EXPLOITABLE, PROBABLY_EXPLOITABLE, UNKNOWN, etc.). 5. Correlate output with memory access details. 6. Repeat the test with and without ASan enabled. 7. Log results and compare with multiple test runs. 8. Save debugger session output. 9. Tag crash samples based on severity. 10. Forward high-severity cases to exploit dev team.
- **Detection**: Exploitability plugin output
- **Solution**: Prioritize patching exploitable bugs
- **Tags**: gdb, exploit-check, crash-triage

## LLDB-Based Reproduction of Logic Flaw

- **Attack Type**: Fault Injection
- **Target**: macOS Binary
- **Vulnerability**: Logic Error
- **MITRE**: T1611
- **Impact**: Unexpected behavior, DoS
- **Tools**: LLDB, ASan, lldb scripts
- **Scenario**: A crash involving unexpected code paths due to logic errors is debugged via LLDB.
- **Attack Steps**: 1. Launch the app in LLDB with lldb -- ./target input_file. 2. Set breakpoints on suspected functions. 3. Run the program and monitor variable values. 4. Identify unexpected branching or loop behavior. 5. Use frame variable to inspect logic states. 6. Enable AddressSanitizer for runtime violations. 7. Step through the crash path and compare with valid inputs. 8. Document flawed condition checks or assumptions. 9. Save LLDB command history and logs. 10. Share results with developers to improve condition validation.
- **Detection**: LLDB logs, ASan crash reports
- **Solution**: Add sanity checks, redesign logic blocks
- **Tags**: lldb, logic-bug, debug-triage, macOS

## Use of Dr. Memory for Heap Issue Triage

- **Attack Type**: Memory Leak
- **Target**: Windows App
- **Vulnerability**: Heap Memory Leak
- **MITRE**: T1135
- **Impact**: Memory exhaustion, performance loss
- **Tools**: Dr. Memory, WinDbg
- **Scenario**: Reproducing a heap memory leak discovered during fuzzing of a GUI app.
- **Attack Steps**: 1. Launch the Windows GUI app using Dr. Memory instrumentation. 2. Feed the crashing input and let it run. 3. Dr. Memory will automatically report leaks or misuses. 4. Cross-reference leak report with crash location in debugger. 5. Reproduce issue multiple times to validate findings. 6. Record call stacks from leak origin. 7. Analyze allocation and free patterns. 8. Classify whether it’s a leak or double free. 9. Save session logs. 10. Document remediation steps in source code.
- **Detection**: Dr. Memory logs, debugger inspection
- **Solution**: Patch memory lifecycle, prevent untracked allocs
- **Tags**: memory-leak, windows, DrMemory, heap-debugging

## Triage of Input Length Handling Crash

- **Attack Type**: Buffer Overflow
- **Target**: Linux App
- **Vulnerability**: Stack Buffer Overflow
- **MITRE**: T1204
- **Impact**: Crash, potential RCE
- **Tools**: GDB, ASan, afl-cmin
- **Scenario**: A long input causes crash in string parser — suspected stack overflow.
- **Attack Steps**: 1. Identify crashing input with excessive string length. 2. Open the binary with GDB and run with input. 3. Observe stack trace and size of the buffer involved. 4. Use ASan to confirm overflow beyond allocated bounds. 5. Use info frame to monitor stack growth. 6. Reduce input size using afl-cmin to minimal crashing PoC. 7. Compare good vs bad inputs in hex viewer. 8. Document length threshold and crash trigger point. 9. Test patched version for mitigation. 10. Share minimized input with devs for unit testing.
- **Detection**: ASan trace, crash logs
- **Solution**: Enforce length limits, stack canary checks
- **Tags**: buffer-overflow, fuzzing-crash, triage

## Batch Reproduction of Multiple Crashes

- **Attack Type**: Crash Automation
- **Target**: Linux Binary
- **Vulnerability**: Multiple (Heap, Logic, UAF)
- **MITRE**: T1588
- **Impact**: Mass crash validation, triage
- **Tools**: Bash, GDB, Python
- **Scenario**: Automating reproduction of 50+ AFL crashes using a script and debugger interface.
- **Attack Steps**: 1. Write a script to loop over all files in AFL's crashes/ folder. 2. For each file, launch target binary inside GDB. 3. Automatically log if crash occurs, with signal code and address. 4. Filter out duplicate crashes using AFL crash hash. 5. Store output logs in per-file directories. 6. Generate CSV summary of crash stats. 7. Identify high-impact crash samples for deeper analysis. 8. Integrate GDB with Python script for auto triage. 9. Share reproducible crash stats with bug tracking system. 10. Maintain reproducibility index for future fuzzing iterations.
- **Detection**: Scripted crash validation + debugger output
- **Solution**: Create automated crash validation pipelines
- **Tags**: batch-repro, fuzz-triage, automation

## Analyze Crash Using GDB + AddressSanitizer Logs

- **Attack Type**: Crash Triage
- **Target**: Linux Binary
- **Vulnerability**: Heap corruption
- **MITRE**: T1595.002
- **Impact**: Heap overwrite, potential RCE
- **Tools**: GDB, AddressSanitizer
- **Scenario**: Researcher triages heap corruption bug using GDB and ASan report
- **Attack Steps**: 1. Launch the target binary in GDB using gdb --args ./target input_file. 2. When the program crashes, note the exact signal (e.g., SIGSEGV). 3. Re-run with ASan (ASAN_OPTIONS=abort_on_error=1 ./target input_file) to generate a stack trace. 4. Compare GDB backtrace with ASan log. 5. Use bt in GDB to trace call history. 6. Identify which input data corrupted heap using hexdump on input_file. 7. Conclude if it’s use-after-free or buffer overflow. 8. Save reproduction command and crash input for documentation.
- **Detection**: GDB trace, ASan log
- **Solution**: Input validation, memory boundary checks
- **Tags**: gdb, asan, crash triage, heap corruption

## WinDbg Exploitability Check on Windows Crash

- **Attack Type**: Crash Reproduction
- **Target**: Windows App
- **Vulnerability**: NULL deref, control hijack
- **MITRE**: T1595.003
- **Impact**: Potential remote code exec
- **Tools**: WinDbg, !exploitable plugin
- **Scenario**: Researcher uses WinDbg and !exploitable plugin to judge severity of crash
- **Attack Steps**: 1. Open crash dump in WinDbg: windbg -z crash.dmp. 2. Load symbols: .symfix; .reload. 3. Run !analyze -v for detailed exception. 4. Use !exploitable to auto-classify crash (e.g., HIGH). 5. Check faulting instruction via u (unassemble). 6. Navigate stack via kb and !stack. 7. Match stack trace to source if available. 8. Document crash as potentially exploitable if classified as such. 9. Export session logs and minimize crash input. 10. Share PoC for internal review.
- **Detection**: WinDbg plugin, exception record
- **Solution**: Fix instruction pointer checks, sanitize data
- **Tags**: windbg, exploitable, windows fuzzing, crash triage

## Triage Segfault in LLDB for macOS App

- **Attack Type**: Fault Injection
- **Target**: macOS Binary
- **Vulnerability**: Stack buffer overflow
- **MITRE**: T1203
- **Impact**: Memory corruption, crash
- **Tools**: LLDB, macOS crash logs
- **Scenario**: Crash in macOS binary reproduced and analyzed with LLDB
- **Attack Steps**: 1. Run lldb ./target and input run < crash_input. 2. On crash, use bt to get the backtrace. 3. Use frame variable to inspect stack variables. 4. Use memory read to examine corrupted region. 5. Map crash address back to source if compiled with debug symbols. 6. Check whether invalid pointer, corrupted structure, or logic flaw caused the crash. 7. Save input and crash state. 8. Re-run several times to ensure reproducibility. 9. Log crash signature and function name for triage dashboard.
- **Detection**: LLDB debug trace, crash logs
- **Solution**: Enable stack protections, patch overflow
- **Tags**: lldb, crash debug, macOS, triage

## Cluster Crashes Using AFL’s Crash Minimization

- **Attack Type**: Crash Minimization
- **Target**: Linux App
- **Vulnerability**: Various memory faults
- **MITRE**: T1203
- **Impact**: Unique PoC clustering
- **Tools**: AFL++, afl-cmin, afl-showmap
- **Scenario**: Multiple AFL crashes are de-duplicated and minimized
- **Attack Steps**: 1. Collect all crashes from AFL output crashes/. 2. Run afl-cmin to minimize set: afl-cmin -i crashes -o min_crashes -- ./target @@. 3. Use afl-showmap to ensure code coverage of minimized inputs. 4. Categorize crashes by signal type (e.g., SIGSEGV vs SIGABRT). 5. Generate hashes of stack traces to group unique crashes. 6. Select top few for detailed triage. 7. Load selected cases into GDB or ASan for analysis. 8. Log crash clusters for tracking.
- **Detection**: Stack trace hash, afl-cmin stats
- **Solution**: Reduce fuzzing noise, isolate PoCs
- **Tags**: afl++, crash triage, deduplication, stack hash

## Compare ASan and UBSan Logs for Undefined Behavior

- **Attack Type**: Sanitizer Detection
- **Target**: Linux App
- **Vulnerability**: Undefined behavior
- **MITRE**: T1595
- **Impact**: Subtle logic vulnerabilities
- **Tools**: ASan, UBSan, Clang
- **Scenario**: Researcher evaluates crashes via AddressSanitizer and UndefinedBehaviorSanitizer
- **Attack Steps**: 1. Compile target with -fsanitize=address,undefined -g. 2. Run binary with test cases. 3. On crash, review output for both ASan and UBSan warnings. 4. Check undefined operations (e.g., integer overflow, shift by negative). 5. Use backtrace() or debugger to locate root cause. 6. Determine which crash is severe or exploitable. 7. Store crash input and logs for reporting. 8. Use asan_symbolize to map raw addresses to function names.
- **Detection**: ASan/UBSan output, debug symbols
- **Solution**: Enforce type safety, integer range checks
- **Tags**: ubsan, asan, sanitizer analysis, fuzz output

## Triage File Parser Crash from Fuzzer

- **Attack Type**: Input Mutation
- **Target**: File Parser
- **Vulnerability**: Out-of-bounds read
- **MITRE**: T1203
- **Impact**: Denial of service, info leak
- **Tools**: GDB, AFL++, file-format fuzzer
- **Scenario**: File format fuzzing crash reproduced and analyzed in debugger
- **Attack Steps**: 1. Use AFL++ to fuzz image parser binary. 2. Upon crash, save input file (e.g., corrupted JPEG). 3. Launch in GDB: gdb --args ./parser crash.jpg. 4. Run until crash and examine cause with bt. 5. Use x/s to inspect malformed input fields. 6. Map structure offset back to crash line. 7. Determine if malformed length or pointer caused issue. 8. Save minimal PoC using afl-tmin. 9. Document crash path and affected function.
- **Detection**: Fuzzer input, debugger trace
- **Solution**: Fix bounds check, update parser logic
- **Tags**: file parsing, afl++, gdb, oob read

## Evaluate Exploitability with GEF Plugin in GDB

- **Attack Type**: Exploitability Check
- **Target**: Linux Binary
- **Vulnerability**: Stack corruption
- **MITRE**: T1592
- **Impact**: Potential control hijack
- **Tools**: GDB, GEF plugin
- **Scenario**: Use GEF plugin in GDB to automatically assess crash exploitability
- **Attack Steps**: 1. Install GEF plugin in GDB. 2. Run binary with crash input: gdb ./target crash_input. 3. After crash, use context and exploitable commands. 4. Review GEF’s classification (EXPLOITABLE, UNKNOWN, etc). 5. Inspect control flow, registers, and corrupted stack. 6. Use info registers to track EIP/RIP value. 7. Document findings and reproduction commands. 8. Save crash environment with core dumps.
- **Detection**: GEF classification, register corruption
- **Solution**: Add canaries, patch stack overflow
- **Tags**: gef, gdb, exploit check, stack overwrite

## Analyze Heap Metadata Corruption in Debugger

- **Attack Type**: Memory Fault
- **Target**: Linux App
- **Vulnerability**: Heap metadata overwrite
- **MITRE**: T1595
- **Impact**: Memory corruption
- **Tools**: GDB, glibc debug, heap tracing tools
- **Scenario**: Debugger used to detect corrupted heap metadata in glibc malloc
- **Attack Steps**: 1. Trigger crash using fuzzer-generated input. 2. Launch with GDB and break at free(). 3. Use heap bins command (if pwndbg/gef) to view allocator state. 4. Observe corruption in free list or chunk headers. 5. Analyze overwrite cause and control flow impact. 6. Use ASan to verify heap corruption type. 7. Document crash, allocator state, and payload input.
- **Detection**: GDB heap trace, ASan output
- **Solution**: Harden malloc/free, validate chunk metadata
- **Tags**: heap corruption, malloc, glibc, fuzz

## Differential Fuzzing Triage

- **Attack Type**: Fault Injection
- **Target**: Linux Binary
- **Vulnerability**: Logic divergence
- **MITRE**: T1203
- **Impact**: Inconsistent behavior
- **Tools**: DiffFuzz, custom oracles
- **Scenario**: Use differential fuzzing to trigger inconsistencies across builds
- **Attack Steps**: 1. Run fuzzing on two compiled versions of the target binary. 2. Feed same mutated input to both. 3. Detect mismatch in behavior or crashes. 4. For crash case, use GDB or WinDbg for deeper analysis. 5. Compare memory layout and behavior divergence. 6. Use logs or sanitizer output to identify fault type. 7. Determine which build is more secure. 8. Create issue report with input, command line, and output differences.
- **Detection**: Output diff logs, sanitizer trace
- **Solution**: Fix undefined behavior or compiler bugs
- **Tags**: differential fuzzing, comparison, logic diff

## Reproduce Race Condition Triggered by Fuzzer

- **Attack Type**: Race Condition
- **Target**: Multi-threaded App
- **Vulnerability**: Race condition
- **MITRE**: T1648
- **Impact**: Deadlocks, crashes
- **Tools**: ThreadSanitizer, GDB, AFL++
- **Scenario**: Fuzzing identified a race condition; reproduced and analyzed in debugger
- **Attack Steps**: 1. Compile target with -fsanitize=thread -g. 2. Run input through AFL++. 3. On crash, re-run binary with same input and TSAN_OPTIONS. 4. Review thread sanitizer log for conflicting accesses. 5. Use GDB to observe threads (info threads) and step through functions. 6. Identify shared resource mismanagement. 7. Use thread apply all bt for per-thread backtraces. 8. Document concurrency issue, affected function, and triggering input. 9. Patch using locks or atomic operations.
- **Detection**: TSAN logs, GDB thread inspection
- **Solution**: Use locks, thread-safe functions
- **Tags**: thread sanitizer, race detection, tsan, fuzz

## Triage a Crash from LibFuzzer with GDB

- **Attack Type**: Crash Reproduction
- **Target**: Linux Binary
- **Vulnerability**: Heap corruption
- **MITRE**: T1595
- **Impact**: Arbitrary code execution
- **Tools**: libFuzzer, GDB
- **Scenario**: After a libFuzzer campaign, a unique crash file is found. The analyst wants to step through it using GDB.
- **Attack Steps**: 1. Identify the crashing input file saved by libFuzzer (in crash-*). 2. Launch GDB with the target binary: gdb ./target_binary. 3. Use the crash input as an argument: run < crash_input. 4. Observe where the crash occurs and note the signal (e.g., SIGSEGV). 5. Use backtrace to understand the call stack. 6. Investigate values of key registers and memory around crash point. 7. Use info locals or print var_name to understand variable state. 8. Mark the exact function and input length that caused the crash. 9. Re-run with breakpoints set earlier to understand how execution reached crash point. 10. Document root cause and suspected vulnerability type.
- **Detection**: GDB crash output, ASan logs
- **Solution**: Add bounds checks, fix unsafe memory handling
- **Tags**: gdb, linux, fuzzing, crash-analysis, reproduction

## Assess Exploitability using WinDbg

- **Attack Type**: Exploitability Check
- **Target**: Windows App
- **Vulnerability**: Use-after-free
- **MITRE**: T1203
- **Impact**: Remote code execution
- **Tools**: WinDbg, !exploitable plugin
- **Scenario**: A Windows target crashes under fuzzing. The goal is to know if it’s exploitable.
- **Attack Steps**: 1. Open WinDbg and attach the crashing application: windbg -c ".open crash.dmp". 2. Load the crash dump and wait for initial analysis. 3. Run !analyze -v to get verbose crash details. 4. Use !exploitable to assess whether the crash is exploitable. 5. Review the exception code, instruction pointer, and stack trace. 6. Examine memory contents around ESP and EIP. 7. Use dd, dps, u commands to understand flow and parameters. 8. Mark crash class (e.g., read AV, write AV). 9. Note control over registers or instruction pointer. 10. Decide if bug warrants deeper root cause analysis or exploit dev.
- **Detection**: !exploitable plugin, crash dump analysis
- **Solution**: Code hardening, memory sanitizer
- **Tags**: windbg, crash-triage, windows, exploitability

## Analyze ASan Logs for Heap Overflow

- **Attack Type**: Sanitizer Inspection
- **Target**: Linux Binary
- **Vulnerability**: Heap buffer overflow
- **MITRE**: T1203
- **Impact**: Application crash or RCE
- **Tools**: GCC/Clang with -fsanitize=address
- **Scenario**: A crash is caught with AddressSanitizer enabled, and the developer needs to analyze its logs.
- **Attack Steps**: 1. Compile the target with -fsanitize=address -g. 2. Run the binary with the crash-inducing input. 3. When the crash occurs, ASan outputs a detailed log. 4. Identify the type (heap-buffer-overflow, stack-use-after-return, etc.). 5. Note the faulting address and offset. 6. Look for "READ of size X" or "WRITE of size X". 7. Trace the origin of the faulty memory allocation (new, malloc, etc.). 8. Use backtrace provided by ASan to trace to source code. 9. Validate if input causes incorrect loop or unchecked allocation. 10. Patch the vulnerability and recompile for re-validation.
- **Detection**: ASan runtime logs
- **Solution**: Fix indexing logic, validate buffer usage
- **Tags**: asan, sanitizer, linux, heap-overflow, triage

## Minimize Fuzzing Crash using afl-tmin

- **Attack Type**: Crash Minimization
- **Target**: Linux Binary
- **Vulnerability**: Input parsing flaw
- **MITRE**: T1588.006
- **Impact**: Easier triage, reproducibility
- **Tools**: AFL, afl-tmin
- **Scenario**: After fuzzing with AFL, the input is too large. Analyst wants to shrink it to the minimal crashing input.
- **Attack Steps**: 1. Identify the crashing input file from crashes/. 2. Run afl-tmin -i crash_input -o min_crash -- ./target_binary @@. 3. afl-tmin iteratively removes bytes to find smallest input that still crashes. 4. Monitor the progress bar — AFL automatically tests with different slices. 5. After completion, the min_crash file contains minimized data. 6. Validate crash still occurs using the new input. 7. Document difference between full and minimal inputs. 8. Use minimal input for reproduction or sharing PoC. 9. Reduce manual effort in triage by simplifying input space. 10. Feed minimized inputs into crash de-duplication pipelines.
- **Detection**: Crash reproduction after minimization
- **Solution**: Use minimized inputs for reproducible testing
- **Tags**: afl, crash-minimization, fuzzing, triage

## Debug Undefined Behavior with UBSan

- **Attack Type**: Sanitizer Analysis
- **Target**: Linux App
- **Vulnerability**: Integer conversion flaw
- **MITRE**: T1203
- **Impact**: Unpredictable behavior, RCE
- **Tools**: UBSan, Clang
- **Scenario**: Binary built with UndefinedBehaviorSanitizer logs strange values. Analyst investigates the root cause.
- **Attack Steps**: 1. Compile the binary with -fsanitize=undefined -g. 2. Run it using a crash file found during fuzzing. 3. UBSan logs indicate the type of undefined behavior: shift overflow, null dereference, etc. 4. Carefully read file path and line number where issue occurs. 5. Look at operands involved in the UB. 6. Check if input size or type causes mismatch (e.g., int vs unsigned). 7. Use debugger (GDB) to inspect values and source code. 8. Validate whether this UB is exploitable. 9. Fix type mismatch or logic flaw. 10. Recompile and re-test with same input.
- **Detection**: UBSan output logs, crash with sanitizer
- **Solution**: Correct type usage and value bounds
- **Tags**: ubsan, undefined-behavior, sanitizer, analysis

## Use LLDB for Triage of macOS Crash

- **Attack Type**: Reproduction & Triage
- **Target**: macOS Binary
- **Vulnerability**: Null pointer dereference
- **MITRE**: T1595
- **Impact**: Denial of service or code exec
- **Tools**: LLDB
- **Scenario**: A crash occurs in a macOS target during fuzzing. Analyst reproduces it using LLDB.
- **Attack Steps**: 1. Open Terminal and launch LLDB with target: lldb ./target_binary. 2. Set input file via settings set target.input-path crash_input. 3. Run the binary using run. 4. When it crashes, observe signal (SIGSEGV, SIGABRT, etc.). 5. Use bt to view backtrace. 6. Use frame variable or register read to inspect memory. 7. Track control flow using thread step-in and disassemble. 8. Trace the crash to a specific line and variable. 9. Determine whether crash is logic error, memory error, or UB. 10. Use minimal PoC for consistent crash reproduction.
- **Detection**: LLDB stack trace, runtime signal
- **Solution**: Patch null checks, validate object references
- **Tags**: lldb, macos, crash-triage, debugging

## Analyze Crash Inputs for Stack Smashing

- **Attack Type**: Crash Reproduction
- **Target**: Linux Binary
- **Vulnerability**: Stack buffer overflow
- **MITRE**: T1203
- **Impact**: Potential code execution
- **Tools**: GDB, objdump
- **Scenario**: A binary crashes with overwritten return addresses. Triage determines if this is a stack overflow.
- **Attack Steps**: 1. Load target binary into GDB: gdb ./binary. 2. Run with crash input: run < crashfile. 3. When it crashes, check EIP/RIP — if it's overwritten, suspect stack smashing. 4. Use info registers and x/x $esp to examine stack. 5. Disassemble vulnerable function: disassemble func_name. 6. Check if local buffers are used unsafely (e.g., char buf[64] + gets). 7. Use pattern_create and pattern_offset to identify overwrite location. 8. Confirm whether input length causes overflow. 9. Mark it as a candidate for control flow hijack. 10. Notify dev team with proof and PoC.
- **Detection**: Instruction pointer corruption in crash trace
- **Solution**: Add stack canaries, use safer functions
- **Tags**: stack-overflow, gdb, fuzzing, reproduction

## Use !heap in WinDbg to Analyze Heap Corruption

- **Attack Type**: Heap Analysis
- **Target**: Windows App
- **Vulnerability**: Heap overflow
- **MITRE**: T1203
- **Impact**: Memory corruption, code execution
- **Tools**: WinDbg
- **Scenario**: A crash due to heap corruption is observed. Analyst uses WinDbg’s heap commands to triage.
- **Attack Steps**: 1. Load crash dump in WinDbg. 2. Run !analyze -v to get initial insight. 3. Run !heap -p -a [address] to analyze heap block. 4. Observe if the crash occurred during free or allocation. 5. Use !heap -s to view summary of heap stats. 6. Check whether crash was caused by buffer overflow into adjacent heap chunks. 7. Look at freelist and allocations surrounding the target. 8. Examine stack trace of allocation via gflag settings. 9. Confirm whether overwritten values match user input pattern. 10. Report as exploitable if attacker controls heap metadata.
- **Detection**: WinDbg heap analysis
- **Solution**: Harden heap allocations, add pool integrity checks
- **Tags**: heap-corruption, windbg, analysis, memory

## Use GDB Exploitable Plugin for Crash Triage

- **Attack Type**: Exploitability Rating
- **Target**: Linux App
- **Vulnerability**: Memory corruption, logic error
- **MITRE**: T1595
- **Impact**: Vulnerability classification
- **Tools**: GDB, exploitable plugin
- **Scenario**: A crash is found, and the analyst uses the GDB-exploitable plugin to classify it.
- **Attack Steps**: 1. Install GDB-exploitable plugin via pip or GitHub. 2. Load binary into GDB: gdb ./target. 3. Run with crash file and let it crash. 4. Use exploitability command to automatically classify crash. 5. Plugin returns categories: EXPLOITABLE, PROBABLY_EXPLOITABLE, etc. 6. Review classification reasons and stack trace. 7. Match exploitability tag with input control. 8. If EXPLOITABLE, prepare report for patching and PoC creation. 9. If not exploitable, still report for completeness. 10. Use this triage for prioritizing fuzzing results.
- **Detection**: GDB plugin automated tags
- **Solution**: Prioritize critical crashes, ignore low-impact ones
- **Tags**: gdb, exploitable, triage, crash-classification

## Extract Crash Signature Using Stack Hashing

- **Attack Type**: Crash Categorization
- **Target**: Cross-platform
- **Vulnerability**: Multiple input validation flaws
- **MITRE**: T1595
- **Impact**: Crash de-duplication, triage ease
- **Tools**: GDB, Python script
- **Scenario**: After collecting many crashes, analyst groups them using stack hash.
- **Attack Steps**: 1. Load each crash individually into GDB. 2. Use bt to extract the backtrace. 3. Convert the function addresses to a normalized call stack. 4. Hash this stack using a script (e.g., SHA-256 of frame names). 5. Assign each crash to a hash bucket. 6. Count how many times each hash occurs — high frequency = common bug. 7. Identify unique hashes that may indicate new bugs. 8. Use this categorization to prioritize patching. 9. Feed these into bug tracker or fuzzer dashboard. 10. Automate future grouping with crash hash fingerprints.
- **Detection**: Stack trace comparison, hash generation
- **Solution**: Automate crash grouping for triage
- **Tags**: crash-hashing, deduplication, fuzzing, triage

## Reverse Engineering a Media Player Crash

- **Attack Type**: File Parsing Exploit
- **Target**: Application
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203 – Exploitation for Client Execution
- **Impact**: Possible Remote Code Execution
- **Tools**: Ghidra, ffmpeg, AFL++, ASan
- **Scenario**: A media player crashes while parsing a corrupted MP4 file.
- **Attack Steps**: 1. Load the media player binary into Ghidra.2. Identify the file parsing entry point using main() and its calls.3. Follow the call stack until you reach the MP4 parsing logic.4. Use AFL++ to regenerate crashing input.5. Use AddressSanitizer to confirm heap overflow.6. Identify that buffer copy from header field causes overflow.7. Trace memory allocation routines before and after the copy.8. Understand that unchecked header field size causes the crash.9. Document vulnerability with crash PoC.10. Suggest bounds checking fix.
- **Detection**: Memory sanitizer output + crash traces
- **Solution**: Validate buffer length before copy operations
- **Tags**: reverse engineering, file parser, ghidra, mp4

## Investigating Faulty PNG Parser

- **Attack Type**: Crash Investigation
- **Target**: Application
- **Vulnerability**: Memory Misallocation
- **MITRE**: T1203
- **Impact**: Denial of service or memory corruption
- **Tools**: IDA Pro, libFuzzer, pngcheck
- **Scenario**: A PNG parser in an image viewer crashes on malformed IHDR chunk.
- **Attack Steps**: 1. Load the binary into IDA Pro.2. Navigate to IHDR processing function using symbol references.3. Analyze the structure read from file input.4. Compare it with the PNG file format specs.5. Identify invalid width value causes heap misallocation.6. Use libFuzzer to regenerate the crash.7. Enable ASan to observe heap-buffer-overflow on image decode.8. Analyze object initialization logic in source.9. Document function chain and invalid assumptions.10. Propose size validation in IHDR processing code.
- **Detection**: ASan output and crash offset trace
- **Solution**: Add integer boundary checks on IHDR parsing
- **Tags**: reverse, png, image processing, heap

## Understanding a Crash in a JSON Config Loader

- **Attack Type**: Input Parsing Bug
- **Target**: Application
- **Vulnerability**: Stack Exhaustion
- **MITRE**: T1499 – Endpoint Denial of Service
- **Impact**: DoS via stack overflow
- **Tools**: Binary Ninja, afl-tmin, jq
- **Scenario**: A JSON config loader crashes when deeply nested JSON is parsed.
- **Attack Steps**: 1. Use Binary Ninja to disassemble the config loader binary.2. Locate the JSON parsing library call.3. Trace recursive function for depth-based parsing.4. Observe memory exhaustion during deep recursion.5. Use afl-tmin to minimize the crashing JSON.6. Confirm that stack exhaustion is causing segmentation fault.7. Use GDB to breakpoint on crash point.8. Document recursion path and missing depth limit.9. Highlight exploit potential for DoS.10. Recommend maximum recursion depth for JSON parser.
- **Detection**: Trace logs, debugger, crash reproduction
- **Solution**: Add recursion depth check in parser logic
- **Tags**: json, parser, crash, reverse

## Crash Triage in Custom Archive Unpacker

- **Attack Type**: Crash Injection
- **Target**: Application
- **Vulnerability**: Buffer Overflow
- **MITRE**: T1203
- **Impact**: Possible control hijack via overflow
- **Tools**: Ghidra, afl-cmin, Valgrind
- **Scenario**: A crash occurs when unpacking a specially crafted archive file.
- **Attack Steps**: 1. Load unpacker binary into Ghidra.2. Identify the code responsible for file decompression.3. Use Valgrind to monitor memory use during execution.4. Find that filename parsing logic causes buffer overflow.5. Use afl-cmin to reduce crashing archive sample.6. Follow call stack to vulnerable strcpy() use.7. Document lack of bounds checking on file name.8. Assess exploitability due to control flow corruption.9. Create PoC archive with overflowed file name.10. Suggest migration to safer APIs like strncpy.
- **Detection**: Valgrind and crash reproduction
- **Solution**: Replace strcpy with size-limited operations
- **Tags**: archive, reverse, triage, memory

## Reverse Engineering a Network Protocol Handler

- **Attack Type**: Protocol Parsing Bug
- **Target**: Network Daemon
- **Vulnerability**: Null Pointer Dereference
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Crash leading to potential DoS
- **Tools**: Ghidra, Wireshark, LLDB
- **Scenario**: Network daemon crashes on malformed TCP message during session init.
- **Attack Steps**: 1. Capture traffic causing crash using Wireshark.2. Load daemon into Ghidra and find protocol handling functions.3. Reconstruct crash-inducing packet structure.4. Use LLDB to step through receive function.5. Identify null pointer dereference on unexpected handshake field.6. Confirm with multiple packets.7. Document the misbehavior and trace root cause.8. Highlight that field existence was not verified.9. Write minimal packet for PoC.10. Recommend handshake field checks in message parsing.
- **Detection**: LLDB trace and network packet analysis
- **Solution**: Validate expected field existence in TCP session init
- **Tags**: protocol, network, binary analysis, reverse

## Reverse Tracing Image Decompression Vulnerability

- **Attack Type**: Fault Injection
- **Target**: Application
- **Vulnerability**: NULL Dereference on Allocation Fail
- **MITRE**: T1499
- **Impact**: Crash / resource exhaustion
- **Tools**: IDA Pro, WinDbg, Process Monitor
- **Scenario**: An image decompressor crashes on large BMP input due to allocation failure.
- **Attack Steps**: 1. Load decompressor binary into IDA.2. Identify the decompression entry logic.3. Use Process Monitor to observe system resource allocations.4. Debug in WinDbg and reproduce crash with large BMP.5. Trace function where malloc fails.6. Discover unchecked malloc result is later dereferenced.7. Document missing null pointer check.8. Write BMP image with inflated header dimensions.9. Confirm reproducibility.10. Recommend defensive null-checking and limits on input dimensions.
- **Detection**: Debugger and resource monitoring tools
- **Solution**: Add validation for malloc return, restrict file size
- **Tags**: bmp, decompression, crash triage

## Analyzing Macro Parser Crash in Office Tool

- **Attack Type**: Input Validation Failure
- **Target**: Application
- **Vulnerability**: Integer Underflow
- **MITRE**: T1203
- **Impact**: Arbitrary memory overwrite possible
- **Tools**: Binary Ninja, AFL++, DocxEditor
- **Scenario**: Office tool crashes on a macro-enabled document with malformed macro block.
- **Attack Steps**: 1. Open the crash-inducing document.2. Load binary into Binary Ninja and identify macro parsing logic.3. Use AFL++ to regenerate the faulty input.4. Trace parsing logic via data flow.5. Observe corrupted memory when macro length field is negative.6. Confirm integer underflow and misallocation.7. Generate minimal crash sample with afl-tmin.8. Document memory corruption path.9. Suggest length validation before memory operations.10. Report crash details with annotated PoC.
- **Detection**: Disassembler trace and fuzzing logs
- **Solution**: Validate integer ranges on macro field parsing
- **Tags**: office, macro, reverse, parsing

## Triaging XML Parser Crash in Embedded Device

- **Attack Type**: Coverage Bypass
- **Target**: Embedded Device
- **Vulnerability**: Loop Overrun via Long Attribute
- **MITRE**: T1203
- **Impact**: Firmware crash via parser overrun
- **Tools**: Ghidra, Serial Monitor, GDB
- **Scenario**: Embedded device crashes when parsing malformed XML over UART.
- **Attack Steps**: 1. Capture XML sent to device over UART.2. Load device firmware binary into Ghidra.3. Identify XML parsing logic.4. Observe lack of attribute length checks.5. Use GDB on test hardware to step through crash.6. Trigger crash with crafted XML.7. Identify loop over unbounded attribute name.8. Document flow to crash point.9. Create repeatable PoC for UART fuzzing.10. Suggest attribute name length limitation and parser bounds checks.
- **Detection**: GDB and physical device observation
- **Solution**: Add parser safeguards for attribute lengths
- **Tags**: embedded, xml, reverse

## Reversing Buffer Over-read in Text Processor

- **Attack Type**: Memory Disclosure
- **Target**: Application
- **Vulnerability**: Buffer Over-read
- **MITRE**: T1082 – System Information Discovery
- **Impact**: Sensitive memory disclosure
- **Tools**: IDA Pro, Valgrind, AFL++
- **Scenario**: Text processor reveals memory content after reading beyond buffer due to malformed input encoding.
- **Attack Steps**: 1. Disassemble binary in IDA.2. Trace encoding handling logic.3. Recreate crash with malformed UTF-8 sequences.4. Use Valgrind to confirm buffer over-read.5. Observe that decoding loop reads past buffer boundary.6. Confirm sensitive data from adjacent memory is printed.7. Create minimized input using afl-cmin.8. Document affected buffer and root cause.9. Propose safe encoding validation routine.10. Recommend bounds enforcement before decode operations.
- **Detection**: Valgrind, trace logs
- **Solution**: Add decoding validation and buffer bounds checks
- **Tags**: text processing, utf-8, memory leak

## Debugging Faulty Error Handler in Web Server

- **Attack Type**: Exception Handling Flaw
- **Target**: Web Server
- **Vulnerability**: Faulty Error Handler Initialization
- **MITRE**: T1499
- **Impact**: DoS via error handling failure
- **Tools**: Ghidra, GDB, curl
- **Scenario**: Web server crashes when invalid input triggers faulty error handler path.
- **Attack Steps**: 1. Recreate crash by sending malformed HTTP request with curl.2. Load web server binary into Ghidra.3. Trace request processing function.4. Identify logic that jumps to error handler.5. Use GDB to observe control flow.6. Discover null pointer used in error path due to improper object initialization.7. Confirm crash consistency.8. Propose fix by initializing error handler context.9. Document error path and PoC request.10. Suggest better exception handling.
- **Detection**: GDB trace + error path analysis
- **Solution**: Initialize error paths and sanitize input routing logic
- **Tags**: web server, http, crash path

## DEP Bypass via ROP in Windows Calculator

- **Attack Type**: Exploit Development
- **Target**: Windows App
- **Vulnerability**: Stack Buffer Overflow
- **MITRE**: T1203 - Exploitation for Client Execution
- **Impact**: Remote Code Execution
- **Tools**: Immunity Debugger, Mona.py, Windows Calculator
- **Scenario**: Exploiting a buffer overflow in a vulnerable Windows app and bypassing DEP using Return-Oriented Programming
- **Attack Steps**: 1. Identify a vulnerable application with a known buffer overflow (e.g., a vulnerable input in a GUI textbox).2. Launch the app in Immunity Debugger and trigger the crash with a long string input.3. Use !mona findmsp to determine offset and control EIP.4. Use !mona rop to generate a list of gadgets.5. Construct a ROP chain to call VirtualProtect and mark the shellcode as executable.6. Append shellcode (calc.exe or reverse shell) after the ROP chain.7. Save the PoC as a Python script or .bat file.8. Run it and verify code execution bypassing DEP.
- **Detection**: Monitor unexpected process launches or memory protection changes
- **Solution**: Patch the vulnerable app and enable CFG (Control Flow Guard)
- **Tags**: rop, dep-bypass, exploit-dev, calc.exe

## Bypass ASLR using Module Base Leakage

- **Attack Type**: Exploit Development
- **Target**: Windows
- **Vulnerability**: Info Leak + ROP
- **MITRE**: T1211 - Exploitation for Defense Evasion
- **Impact**: Execution despite ASLR
- **Tools**: WinDbg, Windows DLL Viewer
- **Scenario**: Using an infoleak to defeat ASLR by leaking the base address of a loaded DLL
- **Attack Steps**: 1. Find a vulnerable application that references a DLL with a predictable offset (like kernel32.dll).2. Analyze crash logs or memory dump using WinDbg to find leaked pointers.3. Use the leaked address to calculate base of the module.4. Use this base to construct absolute addresses in a ROP chain.5. Develop exploit script with ROP gadgets using fixed offsets from the base.6. Validate exploit runs consistently across reboots (ASLR bypassed).7. Deliver the exploit as a .bat or network payload.8. Ensure shell or calculator launch.
- **Detection**: Memory analysis of leaked addresses
- **Solution**: Enable ASLR and stack canaries
- **Tags**: aslr-bypass, infoleak, win32, exploit-dev

## SMEP Bypass via ROP in Kernel Driver

- **Attack Type**: Exploit Development
- **Target**: Kernel Driver
- **Vulnerability**: Kernel Buffer Overflow + SMEP
- **MITRE**: T1068 - Exploitation for Privilege Escalation
- **Impact**: Privilege Escalation
- **Tools**: WinDbg, IDA Pro, ROPgadget
- **Scenario**: Exploiting kernel vulnerability to execute user-mode shellcode despite SMEP
- **Attack Steps**: 1. Identify a vulnerable kernel driver (e.g., with ioctl buffer overflow).2. Analyze driver in IDA Pro to identify functions and calling conventions.3. Load system in WinDbg with test VM.4. Use fuzzing or crafted input to gain EIP/RIP control.5. Use ROP gadgets to disable SMEP (e.g., manipulate CR4 register).6. Redirect flow to user-mode shellcode that spawns calc.exe.7. Craft full exploit payload with ROP + shellcode.8. Test in VM, verify local SYSTEM privilege escalation.
- **Detection**: Monitor CR4 write attempts or invalid kernel access
- **Solution**: Harden driver code and enforce SMEP globally
- **Tags**: kernel-exploit, smep, rop, local-priv-esc

## WinDbg Scripted Exploit for Buffer Overflow

- **Attack Type**: Exploit Automation
- **Target**: Windows (C App)
- **Vulnerability**: Stack Buffer Overflow
- **MITRE**: T1587 - Develop Capabilities
- **Impact**: Proof of Concept Automation
- **Tools**: WinDbg, JavaScript Debug Scripts
- **Scenario**: Using WinDbg scripts to automate testing and crafting a simple overflow exploit
- **Attack Steps**: 1. Create a small C program with a deliberate buffer overflow.2. Compile it and load in WinDbg.3. Create a .script file in JavaScript or NatVis for automating overflow tests.4. Use script to feed inputs, monitor registers, and catch EIP control.5. Once EIP is controlled, script appends shellcode after pattern.6. Set breakpoints and script shellcode validation.7. Automate the testing and final payload delivery using .cmdtree.8. Run script repeatedly to simulate automation.
- **Detection**: Scripted debugger tracing
- **Solution**: Add stack protections and enable modern compiler flags
- **Tags**: windbg, scripting, buffer-overflow, automation

## Exploiting Use-After-Free via Type Confusion in C++

- **Attack Type**: Exploit Development
- **Target**: Linux App
- **Vulnerability**: Use-After-Free, Type Confusion
- **MITRE**: T1546.001 - Event Triggered Execution
- **Impact**: Arbitrary Code Execution
- **Tools**: GDB, GCC, LibFuzzer, ASan
- **Scenario**: Exploiting use-after-free condition due to incorrect object type reuse
- **Attack Steps**: 1. Write a vulnerable C++ app with a base and derived class and trigger type confusion.2. Use fuzzer (libFuzzer) to cause memory reuse and invalid method call.3. Identify crash and reproduce in GDB.4. Analyze vtable and object reuse.5. Inject fake vtable and redirect function pointer.6. Use it to call system("calc") or similar.7. Recompile PoC with debug symbols and verify full control.8. Deliver PoC in test file or input stream.
- **Detection**: Use ASan output and vtable corruption traces
- **Solution**: Fix type safety and memory deallocation rules
- **Tags**: uaf, c++, vtable, type-confusion, exploit-dev

## Exploit with Fake File Header in PDF Parser

- **Attack Type**: File Format Exploit
- **Target**: PDF Parser
- **Vulnerability**: Input Validation Failure
- **MITRE**: T1203 - Exploitation for Client Execution
- **Impact**: File Parser Exploitation
- **Tools**: Hex Editor, PDFBox, AFL++
- **Scenario**: Delivering exploit via malformed PDF header to crash or control parser
- **Attack Steps**: 1. Select a vulnerable PDF parser (e.g., older open-source one).2. Use AFL++ with valid PDF corpus to generate malformed headers.3. Analyze crashes caused by invalid magic bytes or embedded JS.4. Use hex editor to reproduce crash manually.5. Locate offset in file that causes parsing logic failure.6. Inject small shellcode or function redirect in structure.7. Save as minimal PoC PDF.8. Run in debugger to confirm crash location and path to execution.
- **Detection**: Monitor PDF parsing behavior and logging
- **Solution**: Enforce strict file validation rules
- **Tags**: pdf-exploit, file-format, header-manipulation

## Automated Exploit Generation with angr

- **Attack Type**: Symbolic Execution
- **Target**: ELF Binary
- **Vulnerability**: Logic Bug / Insecure Comparison
- **MITRE**: T1587 - Develop Capabilities
- **Impact**: Automated Exploit Discovery
- **Tools**: angr, Python3, Z3 Solver
- **Scenario**: Using symbolic execution engine to auto-generate path to vulnerable code
- **Attack Steps**: 1. Select a binary with known logic bug (e.g., password checker).2. Load binary into angr and define entry and success state.3. Use symbolic bit vectors to simulate input bytes.4. Let angr traverse program logic using explore().5. Capture input string that reaches crash or logic bypass.6. Save exploit input and verify execution.7. Integrate with PoC delivery wrapper.8. Extend angr scripts to include logging and coverage.
- **Detection**: Binary instrumentation with symbolic logic
- **Solution**: Strengthen conditional logic and input verification
- **Tags**: angr, symbolic-exec, exploit-generation

## Constructing ROP Chain for calc.exe in Linux

- **Attack Type**: ROP Exploit
- **Target**: Linux Binary
- **Vulnerability**: Stack Buffer Overflow
- **MITRE**: T1203 - Exploitation for Client Execution
- **Impact**: Code Execution via ROP
- **Tools**: ROPgadget, pwndbg, gdb
- **Scenario**: Manually constructing a ROP chain on a vulnerable Linux binary to spawn calculator
- **Attack Steps**: 1. Compile a Linux binary with -fno-stack-protector and vulnerable strcpy() usage.2. Run in gdb and overflow buffer to gain RIP control.3. Use ROPgadget to search for execve or /bin/sh gadgets.4. Construct ROP chain on paper.5. Embed ROP payload in input.6. Launch binary with crafted input.7. Verify shell or GUI calculator opens (gnome-calculator).8. Refine payload to make it minimal and stable.
- **Detection**: Instruction tracing and GDB watchpoints
- **Solution**: Enable ASLR and stack protections
- **Tags**: rop, linux, gdb, shell-spawn

## PoC Trigger for Heap Overflow in Image Parser

- **Attack Type**: Heap Exploitation
- **Target**: Image Parser
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203 - Exploitation for Client Execution
- **Impact**: Heap Memory Corruption
- **Tools**: AFL++, ASan, GDB
- **Scenario**: Triggering a crash and controlling flow via heap metadata overwrite in image parsing tool
- **Attack Steps**: 1. Choose an open-source image parser with known heap bug.2. Fuzz input corpus with AFL++ targeting image dimensions.3. Catch crash with ASan (heap buffer overflow).4. Analyze heap layout and overflow path in GDB.5. Overwrite heap chunk metadata to trigger crash or redirection.6. Build minimal PoC image with bad chunk.7. Launch parser with crafted image.8. Confirm crash log, use for exploit prototype.
- **Detection**: ASan logs and fuzz crash buckets
- **Solution**: Use hardened memory allocators
- **Tags**: heap-overflow, image-parser, afl, crash-triage

## Use !exploitable in WinDbg for Exploitability Scoring

- **Attack Type**: Crash Triage & Exploit Dev
- **Target**: Windows App
- **Vulnerability**: Varies (Access Violation, etc.)
- **MITRE**: T1592 - Gather Victim Host Information
- **Impact**: Prioritize High Exploitability Crashes
- **Tools**: WinDbg, !exploitable plugin
- **Scenario**: Use WinDbg’s !exploitable plugin to analyze crash’s exploitability
- **Attack Steps**: 1. Open crash dump from fuzzing campaign in WinDbg.2. Run !analyze -v to get basic crash info.3. Use !exploitable to classify severity and exploitability (HIGH/MEDIUM/LOW).4. Review crash reason and instruction pointer at crash.5. If HIGH, begin exploring for control over EIP.6. Document crash signature and confidence score.7. Use PoC input from fuzzer for replay and triage.8. Begin exploit development if control is possible.
- **Detection**: Dump Analysis with Plugins
- **Solution**: Review crash triage workflow and fix root cause
- **Tags**: windbg, exploitability, crash-triage, triage

## ROP Chain Exploit on Disabled DEP Binary

- **Attack Type**: Return-Oriented Programming
- **Target**: Windows
- **Vulnerability**: DEP Bypass
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Shell or reverse shell spawned
- **Tools**: Immunity Debugger, Mona.py, Kali Linux
- **Scenario**: Target binary has DEP disabled, allowing attacker to construct ROP chain for code execution
- **Attack Steps**: 1. Identify a crash using a fuzzed input. 2. Load the binary into Immunity Debugger with Mona plugin. 3. Use Mona to search for gadgets (!mona rop -cpb "\x00"). 4. Find a "jmp esp" gadget and align shellcode. 5. Build the payload: padding + return address + ROP chain + shellcode. 6. Test payload in debugger to ensure shellcode reaches execution. 7. Deliver payload via vulnerable vector (file, command-line arg). 8. Confirm shell or calc.exe triggered.
- **Detection**: Monitor process behavior for abnormal DLL calls and shell spawns
- **Solution**: Enable DEP and ASLR, patch buffer overflow
- **Tags**: ROP, DEP Bypass, Shellcode, Exploit Dev

## Bypass SMEP on 64-bit Kernel

- **Attack Type**: SMEP Bypass
- **Target**: Windows
- **Vulnerability**: SMEP Protection Bypass
- **MITRE**: T1068: Exploitation for Privilege Escalation
- **Impact**: System-level code execution
- **Tools**: WinDbg, VMware, KDMapper
- **Scenario**: Exploiting a kernel driver bug with shellcode that needs SMEP bypass
- **Attack Steps**: 1. Find a kernel bug (e.g., vulnerable IOCTL). 2. Disable SMEP temporarily via CR4 control in ROP chain. 3. Construct ROP chain with mov cr4, eax gadget. 4. Inject shellcode in user-mode memory. 5. Trigger vulnerability, redirect execution to ROP chain. 6. ROP disables SMEP and jumps to shellcode. 7. Achieve privilege escalation or code execution. 8. Validate with WinDbg kernel debugger.
- **Detection**: Monitor kernel memory writes and CR4 manipulation
- **Solution**: Block unsigned drivers, use HVCI
- **Tags**: Kernel Exploitation, SMEP, ROP, PrivEsc

## Exploit Using CFG Bypass with Indirect Calls

- **Attack Type**: CFG Bypass
- **Target**: Windows
- **Vulnerability**: CFG Evasion
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Code execution under CFG
- **Tools**: WinDbg, IDA Pro, ROPgadget
- **Scenario**: Application with Control Flow Guard (CFG) enabled is exploited via indirect call targeting gadgets
- **Attack Steps**: 1. Identify indirect call in the application binary. 2. Use IDA Pro to inspect function pointer targets. 3. Find a legal CFG target in a loaded DLL with needed gadget. 4. Construct a payload redirecting control to that legal CFG target. 5. Use ROP chain to achieve desired behavior. 6. Validate in debugger and refine. 7. Deliver exploit to target (file, packet, etc.). 8. Confirm bypass and code execution.
- **Detection**: Log use of legitimate CFG targets with unexpected parameters
- **Solution**: Use CFG with fine-tuned policies and return address checks
- **Tags**: CFG, Indirect Call, Windows Exploitation

## Heap Spray with JavaScript in Browser

- **Attack Type**: Memory Corruption
- **Target**: Windows
- **Vulnerability**: Use-After-Free
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Browser shell or persistence
- **Tools**: Firefox, JavaScript, JIT Debugger
- **Scenario**: Exploit browser heap via JS spray to gain code execution through use-after-free
- **Attack Steps**: 1. Analyze vulnerability in browser (e.g., UAF). 2. Build JavaScript heap spray using typed arrays. 3. Trigger UAF condition and reuse freed object. 4. Replace freed object with controlled memory. 5. Redirect control flow to sprayed shellcode. 6. Launch exploit in browser sandbox. 7. If successful, achieve code execution in browser process. 8. Validate in debugger and analyze crash dump.
- **Detection**: Analyze browser crash telemetry, monitor JIT behavior
- **Solution**: Patch vulnerable browser version, enforce sandboxing
- **Tags**: Heap Spray, JavaScript, Browser Exploit

## ROP Exploit on Embedded ARM Binary

- **Attack Type**: Return-Oriented Programming
- **Target**: Embedded
- **Vulnerability**: Stack Overflow
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Full control on device firmware
- **Tools**: Ghidra, QEMU, Ropper
- **Scenario**: Exploiting an embedded device binary (ARM architecture) with custom ROP chain
- **Attack Steps**: 1. Load ARM binary into Ghidra. 2. Identify overflow point and map stack. 3. Use Ropper to extract usable gadgets. 4. Create ROP chain that manipulates system registers. 5. Inject shellcode and verify gadget execution. 6. Test payload in QEMU emulated device. 7. Trigger exploit and monitor output. 8. If successful, gain shell or code execution on device.
- **Detection**: Static analysis of firmware updates and stack usage
- **Solution**: ASLR + Stack Canaries, patch input validation
- **Tags**: ARM, ROP, Embedded Exploit, Reverse Engineering

## Use Return-to-libc for Legacy Linux Binaries

- **Attack Type**: Return-to-libc
- **Target**: Linux
- **Vulnerability**: Stack Overflow
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Shell via system() call
- **Tools**: GDB, Libc-database, pwntools
- **Scenario**: Exploiting vulnerable Linux binaries without shellcode by returning to libc functions
- **Attack Steps**: 1. Fuzz and find stack overflow. 2. Leak libc address (via format string or memory leak). 3. Calculate base of libc using leaked pointer. 4. Build payload: overflow + return address pointing to system() + argument string (/bin/sh). 5. Test payload in GDB. 6. Confirm shell access is obtained. 7. Deliver payload to target process.
- **Detection**: Audit of classic C functions and absence of stack protections
- **Solution**: Use ASLR, stack canaries, and secure libc
- **Tags**: ret2libc, Linux, Buffer Overflow

## Exploiting Type Confusion in V8 Engine

- **Attack Type**: Type Confusion
- **Target**: Browser
- **Vulnerability**: Type Confusion
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Sandbox escape or shell
- **Tools**: Chrome Canary, d8, gdb, GDB dashboard
- **Scenario**: Trigger a type confusion in Chrome’s V8 JS engine to escalate to code execution
- **Attack Steps**: 1. Identify vulnerable type cast in V8. 2. Write JS snippet that triggers confusion. 3. Use %DebugPrint to inspect object structure. 4. Use crafted object to corrupt memory (e.g., fake object). 5. Hijack code execution via overwritten pointer. 6. Debug with d8 and GDB to analyze control flow. 7. Achieve shell or arbitrary memory write.
- **Detection**: JS behavior monitoring, detect confusion-based corruptions
- **Solution**: Regular browser updates, enable Control Flow Integrity (CFI)
- **Tags**: Type Confusion, JS Engine, Chrome

## Bypass ASLR Using Memory Leak

- **Attack Type**: ASLR Bypass
- **Target**: Linux
- **Vulnerability**: Info Disclosure + ASLR
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Bypass of memory randomization
- **Tools**: GDB, pwndbg, Leak primitives
- **Scenario**: Use memory disclosure to defeat ASLR on target process
- **Attack Steps**: 1. Trigger information disclosure (format string or bug). 2. Leak memory addresses from binary or libc. 3. Compute ASLR slide by subtracting known offset. 4. Craft exploit using calculated address. 5. Redirect flow to shellcode or system call. 6. Validate success via debugger. 7. Monitor behavior of successful bypass (e.g., shell).
- **Detection**: Monitor for abnormal read syscalls or leaked memory regions
- **Solution**: Prevent leaks, enable RELRO, stack canaries, and PIE
- **Tags**: ASLR Bypass, Info Leak, Memory Disclosure

## Automating Exploit with Python ROP Chain Builder

- **Attack Type**: Exploit Automation
- **Target**: Linux
- **Vulnerability**: Stack Overflow
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Consistent shell via automation
- **Tools**: pwntools, Ropper, Python
- **Scenario**: Building an automated script to generate ROP chains and payloads
- **Attack Steps**: 1. Analyze binary and discover overflow. 2. Use Ropper to dump gadgets. 3. Script ROP chain creation using Python. 4. Integrate payload builder with input mechanism. 5. Add logic to auto-select shellcode, return address. 6. Deliver exploit in loop for stability testing. 7. Record crash logs, success rates. 8. Adjust offsets and logic dynamically.
- **Detection**: Detect repeated malformed inputs or abnormal process spawning patterns
- **Solution**: Use stack protections, fuzz input buffers
- **Tags**: Python, Automation, ROP Builder

## Bypassing Stack Canaries with Format String Bug

- **Attack Type**: Canary Bypass
- **Target**: Linux
- **Vulnerability**: Format String
- **MITRE**: T1203: Exploitation for Client Execution
- **Impact**: Shell with stack protection bypass
- **Tools**: GDB, pwndbg, Linux binary
- **Scenario**: Use format string bug to leak and overwrite stack canary, bypassing protection
- **Attack Steps**: 1. Identify a format string vulnerability (printf(user_input)). 2. Use %x specifiers to leak stack values. 3. Locate stack canary in leaked output. 4. Build payload: padding + correct canary + shellcode. 5. Ensure stack alignment to avoid detection. 6. Test in GDB to confirm successful overwrite and execution. 7. Exploit in live environment.
- **Detection**: Audit printf usage and monitor memory dumps for format string anomalies
- **Solution**: Format string mitigation, stack cookies, compiler flags
- **Tags**: Canary Bypass, Format String, Memory Exploit

## Fuzzing in Parallel using Docker and AFL++

- **Attack Type**: Automation
- **Target**: Linux binary
- **Vulnerability**: Memory corruption
- **MITRE**: T1595.002 (Data Staging: Transfer Tools)
- **Impact**: Enhanced coverage and faster bug discovery
- **Tools**: Docker, AFL++
- **Scenario**: Set up AFL++ in multiple Docker containers to run parallel fuzzers.
- **Attack Steps**: 1. Install Docker and pull an Ubuntu image.2. Install AFL++ in a Dockerfile with the target binary.3. Build a Docker image for fuzzing.4. Start multiple Docker containers with AFL++ running in each.5. Mount a shared volume for input/output corpus and crashes.6. Monitor each instance using docker stats or custom scripts.7. Use CPU affinity to ensure containers don’t compete for the same cores.8. Periodically sync findings across all containers.9. Review crashes and minimize using afl-cmin.10. Shut down containers and collect final logs.
- **Detection**: Container monitoring + AFL logs
- **Solution**: Use CI/CD integration for persistent fuzzing
- **Tags**: afl++, docker, automation, fuzz-parallel

## Launching Syzkaller in a GCP Cluster

- **Attack Type**: Scalable Fuzzing
- **Target**: Linux kernel
- **Vulnerability**: Kernel memory issues
- **MITRE**: T1609 (Container Administration)
- **Impact**: Discover kernel zero-days
- **Tools**: Syzkaller, Google Cloud
- **Scenario**: Deploy Syzkaller on Google Cloud for continuous kernel fuzzing across multiple instances.
- **Attack Steps**: 1. Set up a GCP project and enable Compute Engine API.2. Clone the Syzkaller repository.3. Build the kernel image and syzkaller binaries.4. Define manager.cfg to distribute workloads across VMs.5. Use startup scripts to automatically begin fuzzing on VM boot.6. Schedule regular snapshots and crash reporting to GCS.7. Monitor syz-manager output and crash logs.8. Add triage scripts to automatically tag or rank bugs.9. Use preemptible instances to save cost.10. Generate reports for crash clusters using built-in tooling.
- **Detection**: Cloud usage + syzkaller crash logs
- **Solution**: Harden kernels + track exploitability in CI
- **Tags**: kernel, syzkaller, automation, gcp

## Automated triage with ClusterFuzzLite on GitHub

- **Attack Type**: CI/CD Crash Triage
- **Target**: Open-source app
- **Vulnerability**: Stack overflow, use-after-free
- **MITRE**: T1601.001 (Modify System Binary)
- **Impact**: Immediate triage with PoC available
- **Tools**: ClusterFuzzLite, GitHub Actions
- **Scenario**: Triage crashes automatically from fuzzers using ClusterFuzzLite integrated into GitHub Actions.
- **Attack Steps**: 1. Configure GitHub repository with Dockerfile and build script.2. Install ClusterFuzzLite GitHub Action workflows.3. Build your target binary with sanitizers.4. Add fuzz target corpus and dictionary.5. Push changes and trigger fuzzing via GitHub Action.6. Crashes will automatically be logged and displayed.7. Use the reproduce_crash.sh script to confirm locally.8. Define CVSS criteria to prioritize bugs.9. Triage output is saved as GitHub artifacts.10. Review coverage metrics in CI dashboard.
- **Detection**: GitHub Action results + sanitizer output
- **Solution**: Enforce fuzzing in pull requests for all commits
- **Tags**: clusterfuzzlite, ci/cd, github, automation

## Monitoring Fuzzing Campaign with Prometheus + Grafana

- **Attack Type**: Metric Collection
- **Target**: Any
- **Vulnerability**: Input validation failures
- **MITRE**: T1589.002 (Gather Victim Network Info)
- **Impact**: Informed resource scaling & optimization
- **Tools**: Prometheus, Grafana, AFL++
- **Scenario**: Visualize AFL++ fuzzing campaign stats in real-time using Prometheus and Grafana.
- **Attack Steps**: 1. Set up Prometheus on the host running AFL++.2. Configure AFL++ to expose stats using AFL's afl-statsd exporter.3. Link the exporter to Prometheus using the scrape config.4. Launch Grafana and connect it to Prometheus.5. Use dashboard templates to monitor execs/sec, unique paths, and crashes.6. Configure alerts for stall detection or high crash frequency.7. Export time series data for analysis.8. Optionally integrate with Slack or email for alerts.9. Use tags to track fuzzing campaigns.10. Analyze which mutations yielded the most bugs.
- **Detection**: Grafana dashboards + Prometheus metrics
- **Solution**: Scale fuzzing efficiently with real-time visibility
- **Tags**: grafana, prometheus, fuzz monitoring

## Using tmux to Run Multiple Fuzzers Simultaneously

- **Attack Type**: Multi-instance Fuzzing
- **Target**: Linux app
- **Vulnerability**: Buffer overflow, heap overflow
- **MITRE**: T1606.001 (Scheduled Task/Job: At)
- **Impact**: Maximize resource usage in standalone setup
- **Tools**: tmux, AFL++, screen
- **Scenario**: Use tmux to launch and manage multiple fuzzing instances from a single terminal session.
- **Attack Steps**: 1. Install tmux and launch a new session.2. Split the tmux window into panes for each fuzzer.3. In each pane, run afl-fuzz with different seeds or dictionaries.4. Redirect logs to unique files per instance.5. Periodically check each pane for anomalies or crashes.6. Sync shared crashes folder for deduplication.7. Use afl-whatsup to get summary reports.8. Detach and reattach tmux as needed.9. Customize tmux.conf to improve UI.10. Backup all logs post-run.
- **Detection**: tmux logs + afl-whatsup stats
- **Solution**: Batch fuzzing for single-user research sessions
- **Tags**: tmux, afl, fuzz scaling

## Scalable Fuzzing with Kubernetes and AFL++

- **Attack Type**: Container Orchestration
- **Target**: Linux binary
- **Vulnerability**: Memory corruption
- **MITRE**: T1057 (Process Discovery)
- **Impact**: Elastic and cost-effective fuzzing at scale
- **Tools**: Kubernetes, AFL++, Minikube
- **Scenario**: Use Kubernetes to deploy, scale, and manage dozens of AFL++ fuzzers in a managed cluster.
- **Attack Steps**: 1. Set up a Kubernetes cluster using Minikube or GKE.2. Build Docker containers with AFL++ and target binaries.3. Create Kubernetes deployment manifests with replicas > 1.4. Define shared persistent volume for crashes.5. Apply resource quotas and CPU/memory limits.6. Use kubectl to monitor pod logs.7. Auto-scale pods using Horizontal Pod Autoscaler.8. Collect logs using kubetail or fluentd.9. Sync crash artifacts to external storage.10. Teardown cluster when complete and store reports.
- **Detection**: K8s pod logs + storage sync + afl stats
- **Solution**: Integrate fuzzing into DevSecOps pipeline
- **Tags**: kubernetes, afl++, fuzz orchestration

## Using RQ (Redis Queue) for Distributed Fuzzing Tasks

- **Attack Type**: Task Queue Scaling
- **Target**: Linux app
- **Vulnerability**: Heap buffer overflows
- **MITRE**: T1070.004 (Indicator Removal on Host)
- **Impact**: Reliable distributed job execution
- **Tools**: Redis, RQ, Python, AFL++
- **Scenario**: Distribute fuzzing jobs across multiple machines using RQ and Redis as a backend.
- **Attack Steps**: 1. Set up a Redis server accessible to all nodes.2. Install rq and define Python workers to run afl-fuzz.3. Enqueue different fuzzing configs as jobs (seed, dictionary).4. Run workers on multiple VMs or containers.5. Collect output into a shared folder or object storage.6. Monitor Redis job queue and worker status.7. Use retry mechanisms for failed jobs.8. Periodically check results and unique crashes.9. Add metadata to jobs for traceability.10. Export job success/failure metrics for analysis.
- **Detection**: Redis dashboard + job return logs
- **Solution**: Create reusable distributed fuzzing pipelines
- **Tags**: redis, queue, python, automation

## Crash Deduplication Automation with GDB Scripts

- **Attack Type**: Triage Automation
- **Target**: Linux binary
- **Vulnerability**: Instruction pointer overwrite
- **MITRE**: T1614.001 (System Location Discovery)
- **Impact**: Speeds up triage by eliminating noise
- **Tools**: GDB, Bash, Python
- **Scenario**: Automate crash deduplication by scripting backtrace and register checks in GDB.
- **Attack Steps**: 1. Write a GDB Python script to log EIP/RIP, stack trace, and crash address.2. Use the script to process every crash from afl-crashes.3. Save crash hashes based on unique backtrace.4. Filter out duplicates by comparing these hashes.5. Create an HTML or CSV report of unique crashes.6. Tag crashes with function name and offset.7. Integrate the script into a nightly cron job.8. Archive non-unique crashes for storage savings.9. Visualize crash histogram with matplotlib.10. Review high-value crashes for exploit potential.
- **Detection**: Backtrace hashes + custom crash report script
- **Solution**: Use it before human triage to remove duplicates
- **Tags**: gdb, automation, crash triage

## Fuzzing Metrics with InfluxDB and Telegraf

- **Attack Type**: Fuzzing Analytics
- **Target**: Linux binary
- **Vulnerability**: Unvalidated inputs
- **MITRE**: T1082 (System Information Discovery)
- **Impact**: Smarter resource and campaign tuning
- **Tools**: InfluxDB, Telegraf, AFL++
- **Scenario**: Collect and visualize fuzzing campaign metrics using InfluxDB and Telegraf agents.
- **Attack Steps**: 1. Install InfluxDB and Telegraf on the fuzzing system.2. Configure Telegraf to collect system and AFL stats.3. Create AFL++ metrics exporter script to feed into Telegraf.4. Define InfluxDB database for fuzzing.5. Visualize with Chronograf or Grafana.6. Track performance over time: execs/sec, crashes/day, coverage.7. Schedule alerts if metrics fall below thresholds.8. Export reports as JSON/CSV.9. Use metrics to guide campaign decisions.10. Back up InfluxDB nightly.
- **Detection**: InfluxDB dashboards + Telegraf logs
- **Solution**: Centralize metrics for long-running fuzzers
- **Tags**: influxdb, telegraf, fuzz metrics

## Orchestrating Fuzzing with Jenkins Pipelines

- **Attack Type**: CI/CD Integration
- **Target**: Any
- **Vulnerability**: File parsing vulnerabilities
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Automate + unify fuzzing workflows
- **Tools**: Jenkins, Bash, AFL++, Docker
- **Scenario**: Manage, automate, and schedule fuzzing runs using Jenkins pipelines.
- **Attack Steps**: 1. Install Jenkins and create a new pipeline job.2. Define stages: checkout code, build binary, run fuzzer.3. Write shell steps to execute AFL++ with input corpus.4. Archive outputs (crashes, logs) as build artifacts.5. Schedule runs nightly or per commit.6. Integrate Slack or email for alerts.7. Visualize trends using Jenkins plugin graphs.8. Use parameterized builds for testing different modes.9. Automatically tag builds with AFL stats.10. Retain artifacts for triage pipelines.
- **Detection**: Jenkins build logs + archived crash artifacts
- **Solution**: Shift fuzzing left into development pipelines
- **Tags**: jenkins, ci/cd, automation

## Distributed Fuzzing at Scale

- **Attack Type**: Automation & Scaling
- **Target**: Linux Systems
- **Vulnerability**: Memory Corruption
- **MITRE**: T1595.002
- **Impact**: Rapid coverage and crash collection
- **Tools**: AFL++, NFS, Docker, ClusterFuzz
- **Scenario**: Run dozens of AFL++ fuzzers simultaneously across multiple systems with shared crash storage
- **Attack Steps**: 1. Set up a central file server (e.g., NFS) to share input seeds and crash outputs among multiple nodes. 2. Install AFL++ and Docker on all fuzzing nodes. 3. Use Docker to deploy identical container environments across nodes. 4. Mount the shared directory in each container for synchronized storage. 5. Launch fuzzers on each system using afl-fuzz, targeting different mutation strategies or options. 6. Monitor execution with logging and health checks. 7. Collect and deduplicate crashes for triage and prioritization.
- **Detection**: Resource usage logs, crash hash collision
- **Solution**: Use resource quotas and monitor with orchestration tools like Kubernetes
- **Tags**: #AFL #ClusterFuzz #Distributed #ZeroDay #Parallelization #CrashManagement

## Fuzzing with GCP Compute Engine

- **Attack Type**: Automation & Scaling
- **Target**: Cloud Infra
- **Vulnerability**: Stack/Heap Overflow
- **MITRE**: T1587.001
- **Impact**: Cloud-based scale fuzzing
- **Tools**: GCP, Terraform, AFL++, CrashWrangler
- **Scenario**: Scale fuzzing using Google Cloud’s VMs and automate deployment and triage
- **Attack Steps**: 1. Use Terraform scripts to provision multiple identical VM instances with fuzzing environments. 2. Preload AFL++ and dependencies using startup scripts. 3. Upload seed corpus and instrumented binaries to shared GCP storage bucket. 4. Use startup scripts to launch afl-fuzz with logging directed to Cloud Logging. 5. Set up CrashWrangler on each VM to monitor crashes and filter unique ones. 6. Sync logs and crash results regularly to centralized dashboard. 7. Deprovision or scale nodes based on usage metrics.
- **Detection**: Cloud resource metrics, billing, crash logs
- **Solution**: Set budget alerts, automate triage pipelines with crash deduplication
- **Tags**: #GCP #Terraform #Automation #FuzzingInfra #CrashTriage #ZeroDayDiscovery

## Headless Browser Fuzzing in Parallel

- **Attack Type**: Automation & Scaling
- **Target**: Browsers
- **Vulnerability**: Use-After-Free
- **MITRE**: T1203
- **Impact**: Browser crash harvesting
- **Tools**: Chromium, ClusterFuzz, NodeJS
- **Scenario**: Automate fuzzing of browser engine JS APIs using headless Chromium instances
- **Attack Steps**: 1. Install headless Chromium on multiple containers or VMs. 2. Develop JavaScript mutation templates targeting specific APIs (e.g., DOM, WebAssembly). 3. Use NodeJS scripts to generate and feed mutated JS code to headless Chromium. 4. Monitor for crashes or hangs via stderr and output logs. 5. Configure watchdogs to restart stuck instances. 6. Deduplicate crashes using ClusterFuzz backend. 7. Collect JS seeds that triggered crashes for later reproduction and debugging.
- **Detection**: Chromium crash logs, JS stack traces
- **Solution**: Use sandboxed environment, monitor memory usage with crash reporters
- **Tags**: #Chromium #JSFuzzing #ClusterFuzz #BrowserSecurity #ZeroDay

## Fuzzing CI/CD Pipeline Integration

- **Attack Type**: Automation & Scaling
- **Target**: App Binaries
- **Vulnerability**: Memory Mismanagement
- **MITRE**: T1609
- **Impact**: Early detection of regressions
- **Tools**: GitLab CI, AFL++, libFuzzer
- **Scenario**: Embed fuzzing into software CI pipelines to automatically test every build
- **Attack Steps**: 1. Modify GitLab CI pipeline to include a fuzzing stage after build. 2. Use Docker image with preinstalled AFL++ or libFuzzer. 3. Upon each commit, build the instrumented binary with sanitizers enabled. 4. Run fuzzing for a short duration (e.g., 5 minutes) during the pipeline stage. 5. Save crashes and logs as CI artifacts. 6. Notify developers with summary of crashes, reproduction input, and call stack. 7. Enable triage step in pipeline to classify severity of crashes.
- **Detection**: CI logs, Sanitizer output
- **Solution**: Automate crash handling, configure timeouts and triage triggers
- **Tags**: #CI_CD #GitLab #libFuzzer #PipelineSecurity #DevSecOps

## Azure VM Fuzzing Cluster

- **Attack Type**: Automation & Scaling
- **Target**: Windows VMs
- **Vulnerability**: Heap Overflow
- **MITRE**: T1583.004
- **Impact**: Scalable and cost-efficient fuzzing
- **Tools**: Azure CLI, WinAFL, Python Scripts
- **Scenario**: Scale fuzzing on Microsoft Azure using spot VMs and orchestration
- **Attack Steps**: 1. Use Azure CLI to spin up multiple Windows VMs with low-cost spot pricing. 2. Preconfigure WinAFL with target application and instrumentation scripts. 3. Use Python to orchestrate VM creation, fuzzer deployment, and execution. 4. Redirect output and logs to Azure Blob Storage. 5. Schedule daily snapshot and cleanup of unused data. 6. Detect and flag duplicate crashes automatically. 7. Periodically scale down cluster during off-peak hours.
- **Detection**: WinAFL logs, Azure Monitor
- **Solution**: Use orchestration for VM lifecycle and integrate crash deduplication
- **Tags**: #WinAFL #Azure #FuzzingCloud #Orchestration #ZeroDay

## Syzkaller Kernel Fuzzing Automation

- **Attack Type**: Automation & Scaling
- **Target**: Linux Kernel
- **Vulnerability**: Kernel UAF / Overflow
- **MITRE**: T1580
- **Impact**: Kernel vulnerability detection at scale
- **Tools**: syzkaller, QEMU, Kernel Build Tools
- **Scenario**: Set up automated Linux kernel fuzzing with syzkaller infrastructure
- **Attack Steps**: 1. Download syzkaller source and compile with appropriate kernel headers. 2. Build a custom kernel with debug symbols and support for coverage. 3. Set up QEMU VM image and link it to syz-manager. 4. Configure syz-manager with crash triage and metrics collection. 5. Run multiple instances of syz-executor in VMs for parallel kernel fuzzing. 6. Collect crash reports with stack traces and simplified reproducers. 7. Automatically log all coverage increases and crash trends.
- **Detection**: syz-manager crash and coverage logs
- **Solution**: Automate reboot, VM snapshotting, and patch deployment workflows
- **Tags**: #Syzkaller #KernelFuzzing #QEMU #Automation #ZeroDay

## AFLNet for Network Protocol Fuzzing at Scale

- **Attack Type**: Automation & Scaling
- **Target**: Network Daemon
- **Vulnerability**: Protocol Parsing Error
- **MITRE**: T1200
- **Impact**: Fault injection in network parsers
- **Tools**: AFLNet, Docker Swarm, Tcpdump
- **Scenario**: Use AFLNet to fuzz custom network protocol implementation in parallel
- **Attack Steps**: 1. Set up AFLNet inside multiple Docker containers managed via Swarm. 2. Provide seed pcap samples or protocol-aware templates. 3. Launch target server inside same container with logging enabled. 4. Configure AFLNet with correct network timeout and mutation options. 5. Use Tcpdump to log any malformed or anomalous packets. 6. Collect crashes across containers into a shared volume. 7. Triage packet payloads that caused service crashes.
- **Detection**: Tcpdump logs, service crash analysis
- **Solution**: Use packet fuzzer hardening and robust input validation
- **Tags**: #AFLNet #ProtocolFuzzing #NetworkSecurity #Docker #Parallelization

## Metrics Dashboard for Fuzzing Insights

- **Attack Type**: Automation & Scaling
- **Target**: Any
- **Vulnerability**: Any
- **MITRE**: T1608
- **Impact**: Observability and optimization of fuzzing
- **Tools**: Prometheus, Grafana, AFL++, log exporters
- **Scenario**: Visualize crash and performance metrics from distributed fuzzing campaigns
- **Attack Steps**: 1. Configure AFL++ to export stats and logs to Prometheus node exporter. 2. Use Prometheus server to scrape and store time-series metrics (exec/sec, crashes, coverage). 3. Set up Grafana dashboards with alerts for high crash frequency or stalls. 4. Use labels to track metrics by target binary, mutation mode, and node. 5. Monitor trends over hours/days to optimize fuzzer parameters. 6. Generate weekly crash heatmaps and bug discovery timelines.
- **Detection**: Dashboard anomaly detection, performance dips
- **Solution**: Use alerting systems and guided tuning of fuzzing parameters
- **Tags**: #Metrics #Grafana #Prometheus #AFL #FuzzingMonitoring

## Self-Healing Fuzzing Environments

- **Attack Type**: Automation & Scaling
- **Target**: Linux Targets
- **Vulnerability**: N/A
- **MITRE**: T1601
- **Impact**: Reduced downtime, increased coverage
- **Tools**: Python, Bash, systemd, AFL++, Docker
- **Scenario**: Detect and auto-restart crashed or hung fuzzing instances to maximize uptime
- **Attack Steps**: 1. Wrap fuzzer execution in watchdog scripts using bash or Python. 2. Use systemd services to monitor and restart fuzzers on failure. 3. Add crash rate tracking to detect infinite loop or mutation starvation. 4. Use cron or Prometheus alerts to reboot containers if stuck. 5. Implement self-updating fuzzers to pull latest corpus or logic improvements. 6. Store failure reason logs for postmortem. 7. Periodically snapshot container state and sync to central backup.
- **Detection**: Logs, service restarts, uptime monitors
- **Solution**: Combine systemd and container health checks to auto-recover from faults
- **Tags**: #SelfHealing #Docker #systemd #FuzzingUptime #CrashRecovery

## Hybrid Fuzzing via AFL and Symbolic Execution

- **Attack Type**: Automation & Scaling
- **Target**: App Binaries
- **Vulnerability**: Logic Bugs, Edge Case Crashes
- **MITRE**: T1591.001
- **Impact**: Unlock deeper execution paths
- **Tools**: AFL++, QSYM, angr
- **Scenario**: Combine AFL with concolic execution (e.g., angr, QSYM) for deeper path discovery
- **Attack Steps**: 1. Instrument target binary using AFL’s compiler wrappers for coverage feedback. 2. Launch AFL fuzzing with standard seed corpus. 3. Run QSYM or angr in parallel to explore rare paths using symbolic execution. 4. Feed discovered inputs from QSYM back into AFL’s queue for mutation. 5. Monitor crashes and compare fuzzing-only vs hybrid crash coverage. 6. Use dashboard to correlate symbolic exploration success rate. 7. Collect deeply nested bugs missed by pure mutation fuzzing.
- **Detection**: AFL queue comparison, QSYM logs
- **Solution**: Use combined strategy with tuning of QSYM memory and depth parameters
- **Tags**: #HybridFuzzing #AFL #QSYM #angr #SymbolicExecution #DeepPathDiscovery

## Vulnerability Report for Heap Overflow

- **Attack Type**: Heap Overflow Disclosure
- **Target**: Application
- **Vulnerability**: Heap buffer overflow
- **MITRE**: T1203
- **Impact**: Potential arbitrary code execution
- **Tools**: ASan, GDB, GitHub Issues
- **Scenario**: Reporting a heap buffer overflow found in a PDF parser binary during fuzzing with ASan
- **Attack Steps**: 1. Reproduce the heap overflow using ASan-compiled binary.2. Capture crash log and memory dump using GDB.3. Collect minimal input file that triggers the bug.4. Create a report detailing steps to reproduce, ASan output, affected binary version.5. Submit report via GitHub Issue or vendor portal.6. Follow up with maintainer and offer support for debugging.7. Wait for patch and avoid public sharing until resolution.
- **Detection**: Monitoring bug reports and vendor notifications
- **Solution**: Patch application from vendor
- **Tags**: disclosure, pdf-parser, heap-overflow

## Coordinated Disclosure via HackerOne

- **Attack Type**: Responsible Disclosure
- **Target**: Browser
- **Vulnerability**: Memory corruption
- **MITRE**: T1203
- **Impact**: Potential RCE or crash
- **Tools**: HackerOne, Burp Suite, GDB
- **Scenario**: Reporting a memory corruption vulnerability in a browser component through HackerOne
- **Attack Steps**: 1. Identify memory corruption in browser via fuzzed HTML input.2. Reproduce the crash with debugger (GDB/WinDbg).3. Minimize input HTML.4. Write detailed steps in the report with video/GIF walkthrough.5. Submit the report on HackerOne to appropriate program.6. Follow HackerOne’s coordinated disclosure policy.7. Wait for vendor validation, bounty assignment, and patch timeline.8. Do not share details externally until permitted.
- **Detection**: HackerOne disclosure portal logs and tracking
- **Solution**: Vendor patch, public advisory (if allowed)
- **Tags**: hackerone, bug-bounty, memory-corruption

## Kernel Bug Report via LKML

- **Attack Type**: Kernel Exploit Disclosure
- **Target**: OS Kernel
- **Vulnerability**: Use-after-free
- **MITRE**: T1068
- **Impact**: Kernel crash, potential privilege escalation
- **Tools**: syzkaller, kmemleak, LKML
- **Scenario**: Submitting a use-after-free bug found in Linux kernel via LKML (Linux Kernel Mailing List)
- **Attack Steps**: 1. Fuzz kernel using syzkaller until crash occurs.2. Reproduce with QEMU-based VM and extract dmesg logs.3. Identify root cause via code inspection and kmemleak tracing.4. Write PoC and include fix suggestion if possible.5. Post detailed email to LKML with proper subject and tags.6. Monitor responses and engage with kernel maintainers.7. Follow up until patch is merged.8. Do not disclose PoC externally until approved.
- **Detection**: LKML thread and CVE submission logs
- **Solution**: Kernel patch, CVE registration
- **Tags**: kernel, use-after-free, linux, coordinated-disclosure

## Vulnerability Disclosure to CERT/CC

- **Attack Type**: Multi-Vendor Coordination
- **Target**: Shared Library
- **Vulnerability**: Stack overflow
- **MITRE**: T1203
- **Impact**: Widespread exposure
- **Tools**: CERT/CC, ASan, Python Script
- **Scenario**: Reporting a vulnerability in a shared library used by multiple products via CERT
- **Attack Steps**: 1. Discover buffer overflow in libxyz.so used by various apps.2. Confirm bug across multiple products.3. Collect all affected vendors and evidence of the issue.4. Write a comprehensive advisory.5. Submit to CERT/CC including timeline and reproduction steps.6. Wait for CERT to coordinate with vendors and issue CVEs.7. Publish blog post only after all parties patched.8. Provide support and update as needed.
- **Detection**: CERT advisory tracking & vendor disclosure schedules
- **Solution**: Unified CVE assignment, vendor fixes
- **Tags**: cert, multi-vendor, buffer-overflow

## Responsible Disclosure to Adobe

- **Attack Type**: Type Confusion Disclosure
- **Target**: Application
- **Vulnerability**: Type confusion
- **MITRE**: T1203
- **Impact**: Remote code execution
- **Tools**: WinDbg, ASan, Adobe Security Portal
- **Scenario**: Disclosure of type confusion vulnerability in Adobe Reader parser
- **Attack Steps**: 1. Find crash during fuzzing of PDF files with ASan build.2. Use WinDbg to trace object access patterns.3. Identify type confusion in rendering logic.4. Prepare PoC PDF that crashes Reader.5. Create report with crash trace, binary version, system info.6. Submit via Adobe’s portal.7. Keep track of internal ticket number and wait for resolution.8. Disclose after coordinated period or CVE issuance.
- **Detection**: Adobe bug submission tracking system
- **Solution**: Apply Adobe patch as per advisory
- **Tags**: adobe, type-confusion, coordinated-disclosure

## CVE Request through MITRE

- **Attack Type**: CVE Management
- **Target**: Web App
- **Vulnerability**: Unauthenticated RCE
- **MITRE**: T1190
- **Impact**: Full takeover of server
- **Tools**: MITRE CVE Form, GitHub, GDB
- **Scenario**: Submitting CVE request after finding an unauthenticated RCE bug in open-source project
- **Attack Steps**: 1. Find unauthenticated RCE in web app through fuzzed GET parameter.2. Reproduce and confirm bug.3. Notify project maintainers via email or GitHub.4. After fix released, go to MITRE CVE request page.5. Fill in required fields including PoC, impacted versions, and patch link.6. Wait for assignment and confirmation.7. Add CVE number to blog or disclosure timeline.
- **Detection**: GitHub issue tracker, CVE database
- **Solution**: Patch deployment, CVE tracking
- **Tags**: cve, mitre, unauthenticated-rce

## Fuzzing Report Submitted via Google VRP

- **Attack Type**: Sandbox Escape
- **Target**: Browser
- **Vulnerability**: Sandbox escape
- **MITRE**: T1211
- **Impact**: Privilege escalation
- **Tools**: Chrome, GDB, Google VRP
- **Scenario**: Sandbox escape discovered via fuzzing Chrome IPC channels, disclosed via Google VRP
- **Attack Steps**: 1. Use targeted fuzzing on Chrome IPC channels.2. Trigger sandbox escape condition and reproduce with debugger.3. Write detailed repro steps, crash analysis, and PoC.4. Submit to Google’s Vulnerability Reward Program portal.5. Include affected versions and impact estimation.6. Wait for Google triage, validation, and bounty response.7. Keep PoC confidential per VRP rules.
- **Detection**: Google VRP internal review
- **Solution**: Chrome update via Google Patch Wednesday
- **Tags**: google-vrp, sandbox-escape, chrome-fuzzing

## Bugzilla-based Private Disclosure

- **Attack Type**: XSS/Injection Vulnerability
- **Target**: Extension
- **Vulnerability**: Client-side XSS
- **MITRE**: T1059
- **Impact**: Information theft or session hijack
- **Tools**: Burp Suite, Bugzilla, GDB
- **Scenario**: Fuzzing found client-side XSS in Mozilla Firefox extension; reported privately through Bugzilla
- **Attack Steps**: 1. Use input fuzzing to inject JS via extension settings.2. Confirm JavaScript executes in extension context.3. Record video proof and browser version.4. Log into Mozilla’s Bugzilla and open private bug.5. Attach report with PoC, source code snippets, and impact.6. Wait for dev response.7. Coordinate on release before making vulnerability public.
- **Detection**: Mozilla Bugzilla access logs and issue status
- **Solution**: Firefox extension patch
- **Tags**: mozilla, bugzilla, xss

## Disclosure Through Responsible AI Initiative

- **Attack Type**: Model Injection
- **Target**: ML Pipeline
- **Vulnerability**: Model poisoning
- **MITRE**: T1601
- **Impact**: Prediction manipulation
- **Tools**: Responsible AI Repo, Python, GDB
- **Scenario**: Reporting ML model poisoning risk in an AI pipeline used in public APIs
- **Attack Steps**: 1. Fuzz input to ML pipeline endpoint.2. Observe crash or poisoning indicators.3. Analyze poisoned model weights and impacts.4. Prepare responsible disclosure package.5. Submit to the model owner or open-source repo.6. Include suggested input sanitization methods.7. Wait for model retraining or patching before releasing full details.
- **Detection**: API logs, model deviation detection
- **Solution**: Model validation and retraining
- **Tags**: responsible-ai, model-poisoning

## Fuzzing Crash Disclosure to Apple Security

- **Attack Type**: Use-After-Free
- **Target**: macOS System
- **Vulnerability**: Use-after-free
- **MITRE**: T1068
- **Impact**: Privilege escalation / system crash
- **Tools**: LLDB, ASan, Apple Security Portal
- **Scenario**: Submitting a macOS use-after-free crash found via fuzzing with LLDB tracing
- **Attack Steps**: 1. Trigger use-after-free crash in system daemon with fuzzed plist file.2. Use LLDB to trace dereferenced freed pointer.3. Build PoC and include system log, crash dump, and version info.4. Submit to Apple’s product security portal.5. Keep track of case ID and correspond as needed.6. Adhere to Apple’s embargo and coordinated timeline.7. Disclose details post-fix or if Apple allows.
- **Detection**: Apple Security case portal
- **Solution**: Apple software update
- **Tags**: apple-security, macos, use-after-free

