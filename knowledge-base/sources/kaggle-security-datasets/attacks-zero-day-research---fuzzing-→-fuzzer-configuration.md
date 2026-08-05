# Zero-Day Research / Fuzzing → Fuzzer Configuration Attacks

## AFL++ File-based Fuzzing for PDF Parser

- **Attack Type**: File-based fuzzing
- **Target**: File Parser
- **Vulnerability**: Input validation flaws
- **MITRE**: Fuzzing (T1595)
- **Impact**: Potential denial of service or RCE
- **Tools**: AFL++, pdftohtml
- **Scenario**: Use AFL++ to fuzz a PDF parser using a corpus of valid PDF files.
- **Attack Steps**: 1. Choose a PDF parsing binary (e.g., pdftohtml) as the fuzz target. 2. Instrument the target using afl-clang-fast for AFL++ compatibility. 3. Download or collect 10–20 valid PDF files to serve as the seed corpus. 4. Place them in an inputs/ folder. 5. Create an outputs/ folder to store crashing testcases. 6. Run AFL++: afl-fuzz -i inputs -o outputs -- ./pdftohtml @@. 7. Monitor AFL++ stats for crashes or hangs. 8. Triage crashes with afl-showmap and gdb.
- **Detection**: AFL crash logs, sanitizer output
- **Solution**: Fix input validation and improve bounds checks
- **Tags**: afl++, file-based fuzzing, PDF, seed corpus

## Argument-Based Fuzzing Using LibFuzzer

- **Attack Type**: Argument-based fuzzing
- **Target**: CLI Tool
- **Vulnerability**: Argument parsing logic
- **MITRE**: Fuzzing (T1595)
- **Impact**: Crashes via invalid args
- **Tools**: libFuzzer, imagemagick
- **Scenario**: Fuzz an image conversion utility by passing malformed arguments.
- **Attack Steps**: 1. Clone ImageMagick from GitHub. 2. Build it with -fsanitize=address,fuzzer and -g flags. 3. Write a simple fuzz harness that takes input as arguments (e.g., convert image.jpg output.png). 4. Link against libFuzzer. 5. Compile with clang++. 6. Prepare a seed corpus of valid filenames and formats. 7. Run the fuzzer: ./fuzzer -runs=100000 corpus/. 8. Monitor for crashes and analyze stack traces for vulnerabilities.
- **Detection**: ASAN, logs, debugger
- **Solution**: Harden argument validation logic
- **Tags**: libFuzzer, CLI, ImageMagick

## Honggfuzz with Stdin-Based CLI Fuzzing

- **Attack Type**: Stdin fuzzing
- **Target**: CLI Binary
- **Vulnerability**: Std input mishandling
- **MITRE**: Fuzzing (T1595)
- **Impact**: Memory corruption or crash
- **Tools**: Honggfuzz, file(1)
- **Scenario**: Use Honggfuzz to fuzz a command-line tool that accepts input via stdin.
- **Attack Steps**: 1. Choose a tool like file that reads from stdin. 2. Compile it with honggfuzz compiler wrapper. 3. Prepare a directory of sample input files. 4. Run the fuzzer: honggfuzz -f corpus/ -- ./file. 5. Observe crash or timeout indicators. 6. Use gdb or lldb to inspect memory corruption on crashes. 7. Optionally use --rlimit_rss to force memory constraints. 8. Log crash files for triage.
- **Detection**: stderr, crash file logs
- **Solution**: Validate stdin before processing
- **Tags**: honggfuzz, stdin, CLI tools

## WinAFL Fuzzing a Windows Media Player Plugin

- **Attack Type**: Windows-based fuzzing
- **Target**: Windows Binary
- **Vulnerability**: File parsing bugs
- **MITRE**: Fuzzing (T1595)
- **Impact**: Plugin crash or DoS
- **Tools**: WinAFL, DynamoRIO, Windows 10
- **Scenario**: Use WinAFL to fuzz a proprietary Windows media plugin that accepts file input.
- **Attack Steps**: 1. Identify the plugin DLL or EXE to target. 2. Set up WinAFL with DynamoRIO. 3. Write a simple harness that loads files into the plugin in memory. 4. Use a file corpus (e.g., .avi or .mp4) as input. 5. Use the command: afl-fuzz.exe -i inputs -o outputs -D <DynamoRIO dir> -t 2000 -- target.exe @@. 6. Enable persistent mode if possible for efficiency. 7. Monitor for crashes and analyze using WinDbg. 8. Use !analyze -v to get root cause.
- **Detection**: WinDbg crash triage
- **Solution**: Patch file parser component
- **Tags**: WinAFL, Windows fuzzing

## AFL++ Persistent Mode on JSON Parser

- **Attack Type**: File-based fuzzing
- **Target**: File Parser
- **Vulnerability**: JSON handling flaws
- **MITRE**: Fuzzing (T1595)
- **Impact**: High-speed bug discovery
- **Tools**: AFL++, jsmn
- **Scenario**: Use AFL++ persistent mode for fuzzing a C-based JSON parser.
- **Attack Steps**: 1. Choose a lightweight C JSON parser like jsmn. 2. Modify the target to loop inside a persistent function. 3. Build with afl-clang-fast and define __AFL_LOOP(1000) in main loop. 4. Use valid JSON files as seeds. 5. Run: afl-fuzz -i inputs -o outputs -- ./jsonfuzz @@. 6. Let AFL++ mutate inputs more efficiently due to persistence. 7. Check crashes with afl-cmin and afl-tmin. 8. Analyze behavior under malformed JSON.
- **Detection**: Crash minimization logs
- **Solution**: Add fallback handling for missing fields
- **Tags**: afl++, persistent mode, JSON

## libFuzzer with Dictionary for PNG Headers

- **Attack Type**: File-based fuzzing
- **Target**: File Parser
- **Vulnerability**: PNG file handling
- **MITRE**: Fuzzing (T1595)
- **Impact**: Heap buffer overflows
- **Tools**: libFuzzer, pngcheck
- **Scenario**: Use libFuzzer with a dictionary to fuzz a PNG parser.
- **Attack Steps**: 1. Download pngcheck and build with -fsanitize=address,fuzzer. 2. Create a fuzz harness that reads PNG input from argv. 3. Write a dictionary file with PNG magic bytes: "\\x89PNG", "IHDR", "IDAT", "IEND". 4. Run: ./fuzzer -dict=png.dict corpus/. 5. libFuzzer will use the dictionary for better mutations. 6. Let it run with -max_total_time=300. 7. Monitor ASAN for crashes. 8. Validate crash inputs with pngcheck.
- **Detection**: ASAN crash log
- **Solution**: Fix buffer indexing code
- **Tags**: libFuzzer, PNG, dictionary

## Network Fuzzing a TCP Daemon using AFL++

- **Attack Type**: Network fuzzing
- **Target**: Network Daemon
- **Vulnerability**: Socket input parsing
- **MITRE**: Fuzzing (T1595)
- **Impact**: Remote DoS or code exec
- **Tools**: AFL++, netcat, custom daemon
- **Scenario**: Use AFL++ to fuzz a custom TCP daemon via socket redirection.
- **Attack Steps**: 1. Set up a local TCP daemon that echoes back data. 2. Write a harness using afl-net or socket wrapper. 3. Use socat or netcat to bridge fuzzer to TCP socket. 4. Feed fuzzer input as TCP payload. 5. Run: afl-fuzz -i in -o out -- ./socket_wrapper @@. 6. Monitor daemon for memory issues, hangs. 7. Capture crash logs via syslog or dmesg. 8. Optionally apply ASAN or Valgrind.
- **Detection**: Log file parsing, memory logs
- **Solution**: Harden socket input handlers
- **Tags**: afl++, TCP fuzzing, sockets

## Seed Corpus Minimization with afl-cmin

- **Attack Type**: Corpus Optimization
- **Target**: Web Input Parser
- **Vulnerability**: Redundant parsing
- **MITRE**: Fuzzing (T1595)
- **Impact**: Efficient fuzzing setup
- **Tools**: AFL++, afl-cmin
- **Scenario**: Minimize seed inputs using afl-cmin before fuzzing.
- **Attack Steps**: 1. Collect a large corpus of sample .html files. 2. Use afl-cmin to reduce unnecessary duplicates: afl-cmin -i large_corpus -o minimized -- ./target @@. 3. Ensure target is built with AFL instrumentation. 4. The minimized set will maximize code coverage with fewer inputs. 5. Use this optimized corpus in future fuzzing. 6. Saves time and CPU cycles. 7. Re-validate reduced corpus before use.
- **Detection**: Code coverage delta
- **Solution**: Rebuild corpus periodically
- **Tags**: afl++, corpus reduction

## Dictionary Setup for HTML Fuzzing

- **Attack Type**: Mutation Enhancement
- **Target**: Web Parser
- **Vulnerability**: Tag parsing flaws
- **MITRE**: Fuzzing (T1595)
- **Impact**: Render logic bypass
- **Tools**: libFuzzer, HTML parser
- **Scenario**: Use dictionary to inject HTML tags during fuzzing.
- **Attack Steps**: 1. Create a dictionary file html.dict with keywords: "<script>", "</div>", "<!--", "&nbsp;". 2. Build the HTML parser target with libFuzzer. 3. Provide a valid HTML seed corpus. 4. Run: ./fuzzer -dict=html.dict corpus/. 5. Dictionary helps fuzzer explore deeper logic. 6. Observe crashes or render logic bugs. 7. Analyze faulty HTML structure in crash inputs. 8. Consider coverage-based triage.
- **Detection**: Fuzzer crash stats
- **Solution**: Fix DOM tree validation
- **Tags**: dictionary, HTML, libFuzzer

## Instrumenting Fuzzing Target with MSAN

- **Attack Type**: Sanitizer usage
- **Target**: File Parser
- **Vulnerability**: Uninitialized memory
- **MITRE**: Fuzzing (T1595)
- **Impact**: Memory corruption discovery
- **Tools**: LLVM, MSAN, libFuzzer
- **Scenario**: Compile target with MemorySanitizer for advanced fuzzing.
- **Attack Steps**: 1. Clone the fuzzing target's source (e.g., XML parser). 2. Compile with -fsanitize=memory,fuzzer using clang++. 3. Ensure all dependencies are MSAN-compatible. 4. Run the binary with a valid input corpus. 5. MSAN will detect uninitialized memory reads. 6. Observe crash trace on access violations. 7. Use -track_origins=2 for better debug output. 8. Patch the code paths identified by MSAN.
- **Detection**: MSAN trace output
- **Solution**: Initialize memory before use
- **Tags**: msan, sanitizer, LLVM

## Fuzzing Win32 Binary with WinAFL Using Dynamic Instrumentation

- **Attack Type**: Local Binary Fuzzing
- **Target**: Windows Binary
- **Vulnerability**: Input parsing flaw
- **MITRE**: T1203
- **Impact**: Application crash or memory corruption
- **Tools**: WinAFL, DynamoRIO
- **Scenario**: Setting up WinAFL to fuzz a custom Windows binary using DynamoRIO-based instrumentation.
- **Attack Steps**: 1. Identify the target Windows binary (e.g., a small image processing tool). 2. Ensure it accepts a file as input or processes data via arguments. 3. Download and set up WinAFL with DynamoRIO. 4. Locate the function in the binary that handles file parsing using static analysis (e.g., IDA, Ghidra). 5. Configure WinAFL to attach to the binary with proper target function offset. 6. Prepare a seed corpus of valid input files in a dedicated folder. 7. Launch the fuzzing campaign using afl-fuzz.exe with options for instrumentation, corpus path, timeout, and coverage reporting. 8. Monitor crashes in the output directory and triage using a debugger.
- **Detection**: Crash logs, exception handlers
- **Solution**: Patch vulnerable binary logic
- **Tags**: WinAFL, Windows, DynamoRIO, Reverse Engineering

## Using AFL++ with Persistent Mode on a Lightweight C Parser

- **Attack Type**: Persistent Fuzzing
- **Target**: Linux CLI App
- **Vulnerability**: Memory mismanagement
- **MITRE**: T1203
- **Impact**: Heap corruption or crash
- **Tools**: AFL++
- **Scenario**: Targeting a lightweight open-source C-based parser using AFL++'s persistent mode.
- **Attack Steps**: 1. Select an open-source target like a JSON, CSV, or INI parser written in C. 2. Modify the main function to loop over input parsing without exiting (persistent mode). 3. Instrument the source using afl-clang-fast to compile with coverage. 4. Compile with -fsanitize=address to capture memory-related bugs. 5. Create a valid seed corpus with a few minimal config files. 6. Run AFL++ with persistent mode flags to reduce exec overhead and boost performance. 7. Set environment variables such as AFL_NO_FORKSRV=1 if needed. 8. Run the fuzzer and collect coverage and crash data over time.
- **Detection**: ASAN output, AFL crash logs
- **Solution**: Harden code, improve bounds checking
- **Tags**: AFL++, Persistent Fuzzing, JSON, Config Parser

## libFuzzer Argument-Based Fuzzing for Image Tool

- **Attack Type**: Argument-Based Fuzzing
- **Target**: Linux Binary
- **Vulnerability**: Input parsing error
- **MITRE**: T1203
- **Impact**: Memory corruption, DoS
- **Tools**: libFuzzer
- **Scenario**: Configuring libFuzzer to fuzz a C++ image converter that takes command-line arguments.
- **Attack Steps**: 1. Choose a target such as an open-source image-to-bitmap converter written in C++. 2. Modify the code to expose the argument-parsing logic in a test harness function. 3. Instrument with clang++ -fsanitize=fuzzer,address. 4. Prepare an array of seed arguments that simulate real user inputs. 5. Use libFuzzer’s main() to drive argument-based fuzzing. 6. Run the fuzzer with various fuzzed inputs passed as argv[] replacements. 7. Monitor ASAN output and crash logs for invalid memory access. 8. Isolate test cases that cause issues and analyze using gdb or lldb.
- **Detection**: Sanitizer output, crash reproducibility
- **Solution**: Improve input handling logic
- **Tags**: libFuzzer, CLI, Argument Fuzzing, Sanitizer

## Fuzzing with AFLnet for Custom TCP Server

- **Attack Type**: Network Protocol Fuzzing
- **Target**: Network Service
- **Vulnerability**: Protocol parsing flaw
- **MITRE**: T1203
- **Impact**: Daemon crash, RCE risk
- **Tools**: AFLnet
- **Scenario**: Setting up AFLnet to fuzz a custom TCP socket-based protocol daemon.
- **Attack Steps**: 1. Download and set up AFLnet, a fork of AFL designed for protocol fuzzing. 2. Select a target: a simple TCP server that reads data from the client. 3. Ensure the server can be launched headlessly and auto-restarted. 4. Create a seed corpus of minimal valid protocol messages. 5. Set the AFLnet environment for delay, handshake, and replay mode. 6. Configure a persistent input-to-socket mechanism in the server if needed. 7. Run AFLnet with fuzzing loop targeting the server port and IP. 8. Use Wireshark or tcpdump to monitor test case patterns. 9. Crash inputs are collected in the AFL output directory for analysis.
- **Detection**: Network logs, AFLnet crash detection
- **Solution**: Input validation, protocol hardening
- **Tags**: AFLnet, Network Fuzzing, TCP

## Dictionary Injection for Structured PDF Fuzzing

- **Attack Type**: File Format Fuzzing
- **Target**: File Parser
- **Vulnerability**: PDF structure parsing
- **MITRE**: T1203
- **Impact**: Memory leaks, denial of service
- **Tools**: AFL++, PDF Dictionary
- **Scenario**: Using custom dictionaries to improve coverage for structured PDF fuzzing with AFL++.
- **Attack Steps**: 1. Choose a PDF parser (like Poppler or PDFium) as the fuzz target. 2. Build the target with AFL++ and -fsanitize=address. 3. Prepare a small seed corpus of PDFs. 4. Analyze PDF structure (headers like %PDF-1.5, objects, xref, obj) to build a dictionary. 5. Create a .dict file with common tokens: /Page, /Obj, %EOF, etc. 6. Launch AFL++ with -x dictionary.dict to enable dictionary mutation. 7. Run the fuzzer and inspect coverage improvements. 8. Crash triage focuses on object parsing and cross-reference handling.
- **Detection**: ASAN logs, mutated PDF crashes
- **Solution**: Fix object handling logic
- **Tags**: PDF, Dictionary Fuzzing, File Format

## Honggfuzz with Linux Daemon Using Stdin-Based Fuzzing

- **Attack Type**: Daemon Fuzzing via Stdin
- **Target**: Linux Daemon
- **Vulnerability**: Input parsing flaw
- **MITRE**: T1203
- **Impact**: DoS or code execution
- **Tools**: Honggfuzz
- **Scenario**: Fuzzing a CLI daemon tool that reads from stdin using Honggfuzz.
- **Attack Steps**: 1. Pick a Linux daemon tool (e.g., cupsfilter) that reads input from stdin. 2. Instrument using hfuzz-clang with sanitizers. 3. Create a simple stdin test harness to pass fuzzed input. 4. Build and test the binary to verify it can consume data via stdin. 5. Prepare a few seed files representing valid input. 6. Launch Honggfuzz with --input and --stdin flags. 7. Use --sanitizers and --threads to parallelize fuzzing. 8. On crash, analyze the minimized crashing input and run with ASAN to verify issue.
- **Detection**: Crash files, sanitizer trace
- **Solution**: Input hardening, secure parsing
- **Tags**: Honggfuzz, Stdin, Linux Daemon

## Configuring Timeout & Crash Limits in libFuzzer Campaign

- **Attack Type**: Controlled Fuzzing
- **Target**: CLI Tool
- **Vulnerability**: Hangs or infinite loop
- **MITRE**: T1499
- **Impact**: Fuzzer resource starvation
- **Tools**: libFuzzer
- **Scenario**: Fine-tuning crash timeout and limits for safer libFuzzer fuzzing sessions.
- **Attack Steps**: 1. Select a target binary and compile with libFuzzer instrumentation. 2. Use -fsanitize=fuzzer,address and prepare test harness. 3. Set flags like -timeout=10 to abort long hangs. 4. Use -max_total_time=3600 to limit total runtime. 5. Use -runs=500000 to control number of executions. 6. Provide a curated seed corpus and monitor mutation progress. 7. Capture and triage crashes after reaching limits. 8. Prevent hang-ups or infinite loops from stalling fuzzing efforts.
- **Detection**: Fuzzer timeout logs
- **Solution**: Use fuzzing limits and retry strategy
- **Tags**: libFuzzer, Timeout, Crash Limit

## Fuzzing OpenSSL PEM Parser via AFL++ with Seed Minimization

- **Attack Type**: Cryptographic Parser Fuzzing
- **Target**: Cryptographic Tool
- **Vulnerability**: PEM parsing flaw
- **MITRE**: T1203
- **Impact**: Denial of service, logic flaw
- **Tools**: AFL++, OpenSSL
- **Scenario**: Using AFL++ and minimized seed files to fuzz the OpenSSL PEM parser.
- **Attack Steps**: 1. Download and build OpenSSL with AFL++ instrumentation. 2. Identify PEM parser entry point and expose via fuzz harness. 3. Compile with afl-clang-fast and enable AddressSanitizer. 4. Prepare a set of PEM-encoded certificate files. 5. Use afl-cmin to minimize the corpus and eliminate redundancy. 6. Launch AFL++ with minimized corpus and monitor mutation patterns. 7. Triage any detected crashes using debugger and logs. 8. Analyze structural bugs in PEM header or footer handling.
- **Detection**: Sanitizer trace, debugger
- **Solution**: Fix PEM validation
- **Tags**: OpenSSL, AFL++, PEM, Minimization

## Dictionary-Based Fuzzing of HTML Parsers

- **Attack Type**: Structured Input Fuzzing
- **Target**: HTML Parser
- **Vulnerability**: Tag parsing issue
- **MITRE**: T1203
- **Impact**: Browser crash, RCE vector
- **Tools**: AFL++, Dictionary
- **Scenario**: Enhancing HTML parser fuzzing by injecting DOM tags via dictionaries.
- **Attack Steps**: 1. Choose an HTML parser (e.g., Gumbo, libxml2). 2. Instrument with afl-clang-fast and compile with ASAN. 3. Prepare a few HTML snippets as seed corpus. 4. Create a dictionary with common HTML tags and attributes: <div>, <script>, onclick=, etc. 5. Run AFL++ with -x dict.dict to enhance mutation quality. 6. Monitor for crashes around DOM parsing logic. 7. Use minimized crash cases for detailed triage. 8. Analyze tag-related logic for potential overflow or injection flaws.
- **Detection**: Sanitizer, DOM log analysis
- **Solution**: Harden tag parser logic
- **Tags**: HTML, Dictionary Fuzzing

## Configuring Network Fuzzing Retry Mechanism in AFLnet

- **Attack Type**: Network Protocol Fuzzing
- **Target**: Network Daemon
- **Vulnerability**: Socket crash / denial
- **MITRE**: T1203
- **Impact**: Network service crash
- **Tools**: AFLnet
- **Scenario**: Ensuring AFLnet retries connection failures gracefully during fuzzing.
- **Attack Steps**: 1. Modify a small TCP server to handle socket timeouts gracefully. 2. Configure AFLnet to restart the server on crash using a restart script. 3. Enable retry flags like -R to force reconnection during fuzzing failures. 4. Prepare a resilient protocol handler in the target. 5. Use Wireshark to validate the handshake sequence and expected test case structure. 6. Start fuzzing with corpus targeting key protocol commands. 7. Collect crash outputs and cross-check with connection logs. 8. This setup ensures uninterrupted fuzzing even after partial failures.
- **Detection**: Network log, AFLnet retry stats
- **Solution**: Graceful handling & retry logic
- **Tags**: AFLnet, Network Resilience

