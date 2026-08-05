# Zero-Day Research / Fuzzing → Reverse Engineering the Binary Attacks

## Static Binary Analysis Using Ghidra

- **Attack Type**: File Format Analysis
- **Target**: Linux ELF
- **Vulnerability**: Lack of bounds checking in parser
- **MITRE**: T1045 - Software Packing
- **Impact**: Information Disclosure
- **Tools**: Ghidra
- **Scenario**: Analyst loads an unknown binary suspected to contain a crash due to malformed input and investigates the file parsing logic
- **Attack Steps**: 1. Launch Ghidra and create a new project. 2. Import the suspicious binary into the project. 3. Allow Ghidra to analyze the binary with default options. 4. Locate the main function and navigate through the control flow graph. 5. Trace through function calls related to file parsing. 6. Identify memory allocation functions and check bounds or validation checks. 7. Document any logic paths that lead to unsafe operations. 8. Correlate these with known crash points from fuzzing. 9. Highlight portions responsible for unsafe object handling. 10. Export notes and disassembly findings for triage.
- **Detection**: Static analysis of binary structure and logic
- **Solution**: Add proper bounds checks, sanitize input parsing
- **Tags**: reverse engineering, ghidra, fuzzing, file parser

## Crash Path Tracing in IDA Pro

- **Attack Type**: Crash Debugging
- **Target**: Windows PE
- **Vulnerability**: Buffer Overflow
- **MITRE**: T1203 - Exploitation for Client Execution
- **Impact**: Potential RCE
- **Tools**: IDA Pro
- **Scenario**: Reverse engineer traces the crash path in IDA Pro to isolate faulty memory handling logic
- **Attack Steps**: 1. Open the crashed binary in IDA Pro. 2. Run auto-analysis and wait for cross-references and function names to populate. 3. Use the stack trace from the crash (e.g., from GDB or ASan logs) to locate crash address. 4. Set bookmarks and follow call graph backwards to find the function that triggered the issue. 5. Use xrefs and string references to locate related data structures. 6. Identify buffer copy operations (e.g., memcpy, strcpy). 7. Check conditions under which these functions execute. 8. Verify if proper length or format checks exist. 9. Annotate functions and variables of interest. 10. Export findings as a crash trace map.
- **Detection**: Stack trace, crash logs
- **Solution**: Implement input validation; restrict data copies
- **Tags**: ida, crash tracing, buffer overflow

## Memory Analysis of Object Parser

- **Attack Type**: Memory Corruption
- **Target**: Linux ELF
- **Vulnerability**: Heap Overflow
- **MITRE**: T1068 - Exploitation for Privilege Escalation
- **Impact**: Denial of Service
- **Tools**: Binary Ninja
- **Scenario**: Researcher analyzes how malformed object files are parsed and how memory is allocated for objects
- **Attack Steps**: 1. Open the binary in Binary Ninja and let it analyze the control flow. 2. Locate object parsing functions using strings or known offsets. 3. Track heap allocations (e.g., malloc/calloc) related to object fields. 4. Use binary-level data flow analysis to observe how memory is copied or transformed. 5. Identify patterns of unsafe reallocations or pointer arithmetic. 6. Compare to crash-inducing input to find the root allocation that fails. 7. Check whether there’s logic to reject oversized or malformed fields. 8. Export analysis notes and graphical CFG for reporting. 9. Attempt minimal PoC reproduction from this analysis. 10. Suggest how allocation logic should be hardened.
- **Detection**: Memory tracking, heap inspection
- **Solution**: Use size-limited allocators and type checks
- **Tags**: reverse engineering, memory analysis, binary ninja

## Reverse Engineering with LLDB Debugging

- **Attack Type**: Controlled Debugging
- **Target**: macOS Mach-O
- **Vulnerability**: Use-After-Free
- **MITRE**: T1574.002 - DLL Side-Loading
- **Impact**: Crash Reproduction
- **Tools**: LLDB, Ghidra
- **Scenario**: Reproduce and trace a crash using LLDB, while reverse engineering the crash origin in disassembler
- **Attack Steps**: 1. Launch LLDB with the crashing binary and PoC file. 2. Reproduce the crash with a minimal crashing input. 3. Identify the exact instruction causing the fault. 4. Load the binary into Ghidra and match the offset to function names. 5. Follow data and control flow backward to locate logic flaws. 6. Examine how the binary parses file structure from header to body. 7. Use LLDB watchpoints to monitor corrupted data. 8. Cross-reference these memory operations in Ghidra. 9. Develop an understanding of corrupted structures. 10. Document the vulnerability origin and potential fix.
- **Detection**: Debug output + disassembler mapping
- **Solution**: Harden memory cleanup, pointer invalidation
- **Tags**: crash reproduction, LLDB, triage

## Understanding File Format Validation Failure

- **Attack Type**: File Format Tampering
- **Target**: Windows PE
- **Vulnerability**: Improper Input Validation
- **MITRE**: T1203 - Exploitation for Client Execution
- **Impact**: Exploitable Parsing Logic
- **Tools**: IDA Pro, Hex Editor
- **Scenario**: Analyze how a crafted input bypasses format validation and leads to crash
- **Attack Steps**: 1. Open the crashing input in a hex editor and review header structure. 2. Load the target binary in IDA Pro and locate parsing functions. 3. Trace header field access (e.g., size, type) in binary logic. 4. Compare values in crash input with expected values. 5. Identify code locations where input is not verified. 6. Observe which field(s) are directly used in allocations or loops. 7. Set breakpoints and test same input under debugger. 8. Confirm unsafe execution path with specific malformed data. 9. Record parsing failure and logic bypass. 10. Suggest input constraints to patch logic.
- **Detection**: Input comparison, manual parsing logic
- **Solution**: Enforce field validation and strict parsing
- **Tags**: input fuzzing, reverse, hex analysis

## Reverse Engineering Custom Protocol Parser

- **Attack Type**: Protocol-Level Fuzzing
- **Target**: Linux ELF
- **Vulnerability**: Invalid Length Field
- **MITRE**: T1040 - Network Protocol Analysis
- **Impact**: Remote Crash via Network
- **Tools**: Ghidra, Wireshark
- **Scenario**: Researcher investigates protocol handling logic to find crash cause
- **Attack Steps**: 1. Use Wireshark or logger to capture the crashing input/protocol message. 2. Identify which field structure triggers crash. 3. Load the binary in Ghidra and analyze protocol parsing code. 4. Search for constants or magic bytes used to recognize packet types. 5. Follow function that processes these fields. 6. Check pointer dereference or memory write operations. 7. Locate parsing assumptions about length or alignment. 8. Compare these assumptions with crafted input. 9. Document logical mismatch and exact crash path. 10. Suggest safe protocol parsing guidelines.
- **Detection**: Network capture + disassembly
- **Solution**: Safe parsing rules and boundary checks
- **Tags**: protocol fuzzing, parsing logic

## Tracing Logic Chains in Ghidra

- **Attack Type**: Control Flow Hijacking
- **Target**: Windows PE
- **Vulnerability**: Control Flow Corruption
- **MITRE**: T1055 - Process Injection
- **Impact**: Arbitrary Code Execution
- **Tools**: Ghidra
- **Scenario**: Researcher maps vulnerable logic path that leads to PC overwrite
- **Attack Steps**: 1. Load the binary and enable full control flow analysis. 2. Locate entry point for file parsing or network handling. 3. Trace all function calls and variables affecting control transfer. 4. Identify the point where attacker input affects registers or return address. 5. Use Ghidra’s decompiler to understand high-level logic. 6. Mark all variables tied to user input. 7. Check if input ever influences EIP/RIP directly or via structure offset. 8. Record possible gadgets or indirect jumps used. 9. Mark the instruction address range affected. 10. Correlate with crash stack to identify exploitable state.
- **Detection**: Stack frame analysis, register flow
- **Solution**: Enforce input type/length bounds
- **Tags**: ghidra, stack overwrite, logic tracing

## Comparative Binary Diff for Vulnerability Patch

- **Attack Type**: Binary Diffing
- **Target**: Linux ELF
- **Vulnerability**: Logic Bug
- **MITRE**: T1601.001 - Patch Analysis
- **Impact**: CVE Understanding
- **Tools**: BinDiff, Ghidra
- **Scenario**: Compare vulnerable and patched binaries to understand root cause
- **Attack Steps**: 1. Obtain original (vulnerable) and patched binary. 2. Load both in Ghidra and run BinDiff plugin. 3. Let the tool match functions by similarity and symbol names. 4. Focus on functions with high delta/change score. 5. Manually inspect changed logic (e.g., added checks, bounds validation). 6. Look for newly inserted branches or size comparisons. 7. Use this to infer what the vulnerability was. 8. Go back to original binary and confirm missing logic. 9. Recreate minimal input that would crash unpatched version. 10. Document difference and write triage report.
- **Detection**: Binary-level diff
- **Solution**: Implement same check in older versions
- **Tags**: bindiff, patch diffing, vuln trace

## File Format Reverse Engineering with No Docs

- **Attack Type**: Format Discovery
- **Target**: Custom Binary Format
- **Vulnerability**: Unknown Format Handling
- **MITRE**: T1587.003 - Custom Command and Control Protocol
- **Impact**: Vulnerability Discovery
- **Tools**: Binary Ninja
- **Scenario**: Analyze a proprietary file format and reverse engineer parser logic
- **Attack Steps**: 1. Open sample files (normal and crash-triggering) in hex editor. 2. Compare field layout, identify patterns. 3. Load the binary in Binary Ninja. 4. Search parsing functions by following string references or offset jumps. 5. Use scripting API to mark repeating structures. 6. Trace how each field is interpreted, length checks, and pointer usage. 7. Cross-check crash-causing input’s deviation from normal behavior. 8. Label unknown fields with type assumptions. 9. Determine structure layout and logic dependency. 10. Document and attempt minimal crash PoC from layout.
- **Detection**: Manual field reverse engineering
- **Solution**: Create open format spec and validators
- **Tags**: reverse file formats, binary parsing

## Recovering Execution Path from Corrupted Dump

- **Attack Type**: Post-Crash Analysis
- **Target**: Windows PE
- **Vulnerability**: Memory Access Violation
- **MITRE**: T1003.001 - LSASS Memory
- **Impact**: Memory Leak or Control Hijack
- **Tools**: WinDbg, IDA Pro
- **Scenario**: Use crash dump to reconstruct control flow and determine exact faulty branch
- **Attack Steps**: 1. Load the crash dump into WinDbg. 2. Use !analyze -v to locate crash address and call stack. 3. Note register values and parameters passed to crashing function. 4. Load same binary in IDA Pro. 5. Navigate to crash offset and backtrack through logic. 6. Compare parameter usage with corrupted values. 7. Identify origin of those corrupted variables. 8. Use this to map the execution path leading to crash. 9. Confirm with test input if logic replicates. 10. Export triage report and suggested fix location.
- **Detection**: Debugger + disassembler correlation
- **Solution**: Fix validation logic on input path
- **Tags**: post-crash reverse, windbg

## Analyzing JPEG Parser with Ghidra

- **Attack Type**: Input Parsing Flaw
- **Target**: Linux Binary
- **Vulnerability**: Buffer Overflow in JPEG decoding logic
- **MITRE**: T1203
- **Impact**: Potential Remote Code Execution
- **Tools**: Ghidra, GDB, AFL++
- **Scenario**: Researcher analyzes crash in custom JPEG image parser used in a proprietary imaging tool
- **Attack Steps**: 1. Open the target binary in Ghidra and start auto-analysis.2. Identify the file parsing logic by locating functions related to "jpeg" or "decode".3. Review stack trace from fuzzing crash using GDB and note the crash location.4. Correlate crash function in Ghidra and use decompiled code to understand buffer allocation.5. Follow data flow from file input to the vulnerable memory write.6. Annotate findings and document buffer overflow in image block size logic.
- **Detection**: Compare crash addresses with disassembly, monitor heap corruption
- **Solution**: Patch image size validation logic, add bounds checks
- **Tags**: reverse engineering, jpeg, memory corruption

## Understanding TLS Record Handling Bug

- **Attack Type**: Protocol Handling Flaw
- **Target**: Cross-platform TLS Library
- **Vulnerability**: Out-of-Bounds Write
- **MITRE**: T1203
- **Impact**: Data leakage, crash, or code execution
- **Tools**: IDA Pro, GDB, afl-cmin
- **Scenario**: Fuzzer finds crash in custom TLS library—researcher must reverse record parsing code
- **Attack Steps**: 1. Load the TLS binary into IDA Pro and analyze strings and functions related to "record".2. Use GDB with the crashing input to reproduce and breakpoint at crash site.3. In IDA, trace the call graph from entry point to crash function.4. Inspect how record length is processed and whether length checks are enforced.5. Identify a missing bounds check on record length.6. Highlight the field that leads to OOB write and document the vulnerability.
- **Detection**: Monitor TLS handshake with malformed input
- **Solution**: Enforce record length limits, update TLS parser
- **Tags**: tls, reverse, oob, record bug

## Tracing Use-After-Free in PDF Library

- **Attack Type**: Memory Mismanagement
- **Target**: Linux PDF Parser
- **Vulnerability**: Use-After-Free
- **MITRE**: T1203
- **Impact**: Heap memory corruption, crash
- **Tools**: Ghidra, AddressSanitizer, PDF corpus
- **Scenario**: A fuzzed PDF file causes a use-after-free during parsing—researcher reverse engineers the cause
- **Attack Steps**: 1. Launch Ghidra and import the PDF parser binary.2. Use AddressSanitizer crash report to identify the freed object.3. In Ghidra, locate the deallocation and subsequent usage of the same pointer.4. Identify the parsing loop that fails to nullify freed object.5. Follow call stack to understand which PDF structure triggers the flaw.6. Extract minimal PoC file and document how the UAF occurs.
- **Detection**: ASan report and symbol offset mapping
- **Solution**: Fix dangling pointer usage after free
- **Tags**: pdf, uaf, binary analysis

## Investigating a GZip Header Crash

- **Attack Type**: File Format Malformation
- **Target**: Windows CLI Utility
- **Vulnerability**: Buffer Overflow
- **MITRE**: T1203
- **Impact**: Application crash, DOS
- **Tools**: Binary Ninja, afl-cmin, WinDbg
- **Scenario**: Binary crashes when processing malformed GZip headers—reverse engineer the root cause
- **Attack Steps**: 1. Load binary in Binary Ninja and perform control flow analysis.2. Reproduce crash using WinDbg and capture stack trace.3. Look for header parsing code in disassembly by searching for magic bytes or size constants.4. Identify function reading header and analyze the input assumptions.5. Find logic flaw when header length exceeds buffer size.6. Document crash trigger and recommend safer buffer allocations.
- **Detection**: Memory watchpoint + GZip input tracking
- **Solution**: Validate header fields and lengths before parsing
- **Tags**: gzip, overflow, reverse engg

## Mapping Control Flow for DLL Hijack Path

- **Attack Type**: Control Flow Hijack
- **Target**: Windows Binary
- **Vulnerability**: DLL Path Hijacking
- **MITRE**: T1574.001
- **Impact**: Arbitrary code execution
- **Tools**: IDA Pro, Procmon, GDB
- **Scenario**: Researcher maps crash in DLL loading path triggered by crafted environment input
- **Attack Steps**: 1. Attach Procmon to target and observe DLL search paths.2. Use IDA to reverse main binary and locate LoadLibrary calls.3. Identify environment variable or config file affecting DLL name/path.4. Analyze call stack and memory before crash using GDB.5. Reconstruct how malformed config leads to unintended DLL path.6. Recommend mitigation steps to restrict DLL load behavior.
- **Detection**: API call analysis + Procmon logging
- **Solution**: Use full DLL paths, code signing
- **Tags**: dll hijack, reverse, windows

## Locating Heap Overflow in ImageMagick

- **Attack Type**: Heap Memory Corruption
- **Target**: Linux Imaging Tool
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203
- **Impact**: App crash, potential RCE
- **Tools**: Ghidra, gdb, ImageMagick
- **Scenario**: Researcher finds crash in ImageMagick when parsing crafted BMP image
- **Attack Steps**: 1. Open ImageMagick binary in Ghidra and locate BMP processing routines.2. Use GDB to run the tool with crashing BMP file and find instruction pointer.3. Trace back to input buffer that overflows allocated heap.4. Review Ghidra decompilation to spot faulty memory copy with unchecked input.5. Isolate specific BMP field triggering bug (e.g., pixel data size).6. Propose patch for secure buffer usage.
- **Detection**: Monitor memory allocations during crash
- **Solution**: Rewrite logic with size-limited copies
- **Tags**: image parsing, heap, overflow

## Debugging Integer Overflow in Argument Parser

- **Attack Type**: Integer Overflow
- **Target**: Linux CLI Tool
- **Vulnerability**: Integer Overflow
- **MITRE**: T1203
- **Impact**: App crash, logic failure
- **Tools**: Ghidra, GDB, libFuzzer
- **Scenario**: Argument parser accepts extremely large value, causing logic error in loop control
- **Attack Steps**: 1. Run libFuzzer to identify crashing argument pattern.2. Launch binary in GDB with same arguments and breakpoint at crash.3. Use Ghidra to disassemble parsing logic and identify type casts.4. See how unsigned int wraps around during multiplication or addition.5. Validate crash occurs due to integer overflow controlling loop iteration.6. Recommend input validation against max argument size.
- **Detection**: Monitor inputs and inspect variable types
- **Solution**: Limit input size, switch to safe math ops
- **Tags**: integer overflow, input parsing

## Reverse Engineering Stack Smashing in Web Daemon

- **Attack Type**: Stack Buffer Overflow
- **Target**: Embedded Linux Server
- **Vulnerability**: Stack Buffer Overflow
- **MITRE**: T1203
- **Impact**: Stack corruption, potential RCE
- **Tools**: Binary Ninja, Valgrind, curl
- **Scenario**: Web daemon crashes due to overlong POST request payload—analyze using disassembler
- **Attack Steps**: 1. Use curl to replay crashing POST payload to web server.2. Run Valgrind to log stack overflows.3. Load binary in Binary Ninja and trace input processing from HTTP handler.4. Examine stack buffer allocations and identify strcpy or unsafe memcpy.5. Correlate payload size with vulnerable stack function.6. Recommend bounds enforcement for user inputs.
- **Detection**: Stack trace + input fuzzing
- **Solution**: Replace unsafe functions, sanitize inputs
- **Tags**: web fuzzing, stack bug

## Locating Pointer Confusion in File Parser

- **Attack Type**: Pointer Confusion
- **Target**: Linux Binary
- **Vulnerability**: Pointer Confusion
- **MITRE**: T1203
- **Impact**: Invalid memory access, crash
- **Tools**: IDA Pro, gdb exploitable, afl-fuzz
- **Scenario**: Binary crashes after misinterpreting input type, leading to invalid dereference
- **Attack Steps**: 1. Fuzz file format using AFL to generate crash sample.2. Reproduce in GDB and trigger crash at dereference site.3. Use IDA to reverse the parser and locate dispatch logic.4. See how input type or flag leads parser down wrong logic path.5. Note unsafe type casting or dereferencing of uninitialized pointer.6. Document type confusion risk and propose input-type checks.
- **Detection**: Pointer analysis, trace fuzz path
- **Solution**: Add type-checking logic before use
- **Tags**: type confusion, deref, binary

## Tracing Exception in Audio Decoder

- **Attack Type**: Logic Bug
- **Target**: Cross-platform Audio Tool
- **Vulnerability**: Arithmetic Logic Bug
- **MITRE**: T1203
- **Impact**: Crash, possible DoS
- **Tools**: Ghidra, GDB, afl-cmin
- **Scenario**: Crashing MP3 file causes arithmetic exception during decode loop
- **Attack Steps**: 1. Minimize crashing MP3 file with afl-cmin.2. Load decoder binary in Ghidra and find decode loop.3. Reproduce crash in GDB and locate arithmetic instruction failing (e.g., divide-by-zero).4. Follow input-controlled variable back through decoding logic.5. Determine MP3 metadata causes malformed parameters.6. Propose additional checks on decoded frame size/bitrate.
- **Detection**: Watch for arithmetic errors in logs
- **Solution**: Add validation on parsed values
- **Tags**: mp3, decode, crash

## Static Analysis of Embedded Parser

- **Attack Type**: File Parser Analysis
- **Target**: Embedded System
- **Vulnerability**: Lack of bounds checking
- **MITRE**: T1595.002
- **Impact**: Memory corruption potential
- **Tools**: Ghidra, binwalk
- **Scenario**: A researcher analyzes an embedded file parser to understand how image files are handled internally
- **Attack Steps**: 1. Extract the binary firmware using binwalk.2. Load the binary into Ghidra and analyze the disassembly.3. Identify parsing routines responsible for handling .bmp files.4. Trace function calls from file read operations to memory write points.5. Observe if bounds checks are in place.6. Note use of memcpy or custom loops for buffer handling.7. Investigate control flow to see if malformed images could alter parsing logic.8. Isolate key parsing logic for fuzzing inputs.9. Comment and document crash-prone segments.10. Export the binary slicing for targeted fuzzing.
- **Detection**: Binary diffing & control-flow analysis
- **Solution**: Harden parser & add input validation
- **Tags**: #binary-analysis #firmware #parsing #reverse-engineering

## Reverse Engineering TLS Handshake Logic

- **Attack Type**: Protocol Handler Analysis
- **Target**: Application
- **Vulnerability**: Malformed input handling
- **MITRE**: T1609
- **Impact**: Client crash on crafted TLS message
- **Tools**: IDA Pro, Wireshark
- **Scenario**: An analyst reviews TLS handshake logic to trace a crash found in a fuzzed client
- **Attack Steps**: 1. Reproduce crash in client using malformed TLS handshake packet.2. Open binary in IDA Pro and set up function symbols.3. Identify TLS packet handler functions via string references (e.g., "ClientHello").4. Cross-reference handshake stages and trace control flow.5. Use Wireshark logs to map network events to function entry points.6. Identify where malformed field leads to crash (e.g., pointer dereference).7. Check for dynamic memory allocations for each field.8. Analyze whether field length checks exist.9. Use IDA’s decompiler view to visualize high-level logic.10. Mark the vulnerable path for patch development.
- **Detection**: Network trace + symbolic references
- **Solution**: Add length checks and error fallback
- **Tags**: #tls #reverse #protocol #gdb

## Identifying Heap Overflow in Legacy Game Engine

- **Attack Type**: Heap Corruption
- **Target**: Game Engine
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203
- **Impact**: Memory corruption & RCE
- **Tools**: Ghidra, Valgrind
- **Scenario**: A game engine crash is traced to an old asset loading function vulnerable to heap overflow
- **Attack Steps**: 1. Load the vulnerable engine into Ghidra.2. Focus on asset loading functions (LoadAsset, ReadChunk).3. Trace parameters passed to malloc or new operators.4. Analyze loop conditions that write into allocated buffers.5. Use Valgrind on a fuzzed input that causes crash.6. Note heap write out-of-bounds logs from Valgrind.7. Cross-reference with decompiled logic to isolate faulty array writes.8. Comment faulty logic and inspect memory allocation flow.9. Identify missing bounds or size validation before loops.10. Propose rewrite using secure memory handling functions.
- **Detection**: Heap instrumentation with Valgrind
- **Solution**: Sanitize asset loading routines
- **Tags**: #heap-overflow #gameengine #memcorruption

## Reverse Tracing of Null Pointer Crash in PDF Parser

- **Attack Type**: Null Dereference
- **Target**: Desktop App
- **Vulnerability**: Input sanitization flaw
- **MITRE**: T1499
- **Impact**: Application crash
- **Tools**: Binary Ninja, pdftohtml
- **Scenario**: A crafted PDF causes the parser to crash due to a null dereference in object handling
- **Attack Steps**: 1. Open crash-triggering PDF in pdftohtml to visualize object layout.2. Load the parser binary into Binary Ninja.3. Identify the function handling PDF object references (resolve_object).4. Trace all conditional checks for object pointers.5. Reproduce crash and attach debugger.6. Observe that null object is passed into rendering logic.7. Check decompiler view for type confusion or missing null checks.8. Comment the logic and prepare patch location.9. Extract crashing PDF object and test with modified inputs.10. Create PoC + explanation of logical flaw.
- **Detection**: PDF structure + binary trace
- **Solution**: Add null checks in parsing logic
- **Tags**: #pdf-parser #binary-ninja #null-deref

## Understanding Parsing Logic in Audio File Handler

- **Attack Type**: Input Validation Bypass
- **Target**: Media Player
- **Vulnerability**: Bitfield parsing flaw
- **MITRE**: T1204
- **Impact**: Decoder crash
- **Tools**: Ghidra, ffmpeg, audacity
- **Scenario**: Audio fuzzing yields crash on malformed MP3; researcher must understand format parsing
- **Attack Steps**: 1. Use Audacity to craft malformed MP3 with corrupted header.2. Load binary of the audio player into Ghidra.3. Locate parsing logic via strings like "MP3", "Bitrate".4. Use cross-references to trace format verification code.5. Step through header reading functions.6. Identify places where corrupted fields affect memory access.7. Reproduce crash and trace execution path.8. Check whether bitmasking operations were improperly validated.9. Identify if frame sync or bitrate parsing leads to invalid pointers.10. Document findings and suggest strict format enforcement.
- **Detection**: Header offset validation
- **Solution**: Harden header parsing logic
- **Tags**: #audio-fuzz #binary-tracing #ghidra

## Tracing File Handling Logic in Embedded Bootloader

- **Attack Type**: Buffer Overflow
- **Target**: Embedded Bootloader
- **Vulnerability**: Stack buffer overflow
- **MITRE**: T1542.001
- **Impact**: Boot crash / firmware overwrite
- **Tools**: IDA Pro
- **Scenario**: A bootloader crashes when receiving overlong update filenames
- **Attack Steps**: 1. Dump and load the bootloader into IDA Pro.2. Identify update-related logic (LoadFirmware).3. Trace filename copy function (e.g., strcpy).4. Confirm lack of buffer length checks in bootloader.5. Create malformed update filename using fuzzer.6. Observe crash on long input.7. Cross-reference crash location with disassembly.8. Use function graph to identify buffer allocation.9. Highlight affected memory regions and registers.10. Document overflow and propose fix using strncpy.
- **Detection**: Function call mapping
- **Solution**: Replace unsafe functions
- **Tags**: #embedded #strcpy #bootloader #reversing

## Deep Inspection of Input Object Constructor

- **Attack Type**: Constructor Vulnerability
- **Target**: Desktop App
- **Vulnerability**: Uninitialized field usage
- **MITRE**: T1609
- **Impact**: Runtime crash or memory leak
- **Tools**: IDA Pro, C++ RTTI analysis
- **Scenario**: A crash occurs inside a C++ object constructor when loading malformed configuration
- **Attack Steps**: 1. Reproduce crash with malformed config file.2. Load binary into IDA Pro and enable RTTI parsing.3. Identify constructor of crashing object via stack trace.4. Analyze constructor logic: file reading, object field initialization.5. Identify memory allocations and exception handling.6. Look for uninitialized pointer usage.7. Trace how malformed input affects constructor logic.8. Comment field-by-field handling and vulnerability flow.9. Generate PoC input and suggest safe constructor logic.10. Export relevant assembly snippet for disclosure.
- **Detection**: RTTI + constructor trace
- **Solution**: Add field checks & guards
- **Tags**: #cpp #constructor #ida #config

## Bytecode Reverse Engineering of Script Engine

- **Attack Type**: Bytecode Interpreter Abuse
- **Target**: Scripting Engine
- **Vulnerability**: Opcode mishandling
- **MITRE**: T1547.009
- **Impact**: Interpreter crash or code exec
- **Tools**: Ghidra, custom disassembler
- **Scenario**: Fuzzing exposes crash in embedded script engine interpreter
- **Attack Steps**: 1. Isolate crash-triggering script.2. Load binary into Ghidra.3. Locate bytecode interpreter function via opcode dispatch table.4. Trace handler logic for crashing opcode.5. Compare valid vs malformed bytecode structure.6. Identify illegal jump or memory access due to crafted opcode.7. Step through interpreter loop in debugger.8. Analyze register contents at time of crash.9. Comment opcode handling logic.10. Propose validation for bytecode range and jumps.
- **Detection**: Opcode pattern matching
- **Solution**: Input opcode range validation
- **Tags**: #bytecode #interpreter #ghidra #vm

## Manual Rebuild of Stripped Binary Call Graph

- **Attack Type**: Call Graph Reverse Engineering
- **Target**: Any
- **Vulnerability**: Missing symbol reverse engineering
- **MITRE**: T1614.001
- **Impact**: Manual RE required
- **Tools**: Binary Ninja, Radare2
- **Scenario**: A stripped binary requires manual call graph reconstruction for analysis
- **Attack Steps**: 1. Load the stripped binary into Binary Ninja.2. Identify all functions using function detection heuristics.3. Label known string operations or file I/O via cross-references.4. Use Radare2 to identify indirect jump tables.5. Manually link function calls to reconstruct high-level call graph.6. Apply symbols based on usage pattern.7. Mark crash path traced from fuzzer input.8. Map data flow between handlers.9. Validate call flow against known logic.10. Document and export the reconstructed call tree.
- **Detection**: Manual graph tracing
- **Solution**: Build annotated symbol map
- **Tags**: #strippedbinary #callgraph #reversing

## Reverse Engineering of Input State Machine

- **Attack Type**: State Machine Abuse
- **Target**: Application
- **Vulnerability**: State transition flaw
- **MITRE**: T1601.001
- **Impact**: Logic error or crash
- **Tools**: Ghidra
- **Scenario**: Malformed input crashes the app by disrupting its internal state machine
- **Attack Steps**: 1. Load the target binary in Ghidra.2. Locate input state machine by searching for large switch-case constructs.3. Trace transitions between states based on input byte triggers.4. Reproduce crash and identify last known state before crash.5. Analyze memory or logic errors between transitions.6. Isolate input that causes invalid state.7. Confirm that no default fallback case exists in state handler.8. Document state logic flaw.9. Suggest design for transition validation.10. Generate input-state mapping chart for devs.
- **Detection**: Switch analysis + input testing
- **Solution**: Add default handler state
- **Tags**: #statemachine #crash #ghidra

## Static Reverse Engineering of PDF Parser

- **Attack Type**: Static Analysis
- **Target**: Application
- **Vulnerability**: Input Validation
- **MITRE**: T1595
- **Impact**: Memory Corruption
- **Tools**: Ghidra, Hex-Rays, GDB
- **Scenario**: An analyst attempts to understand how a custom PDF parser processes embedded JavaScript to trace a crash.
- **Attack Steps**: 1. Open the PDF parser binary in Ghidra. 2. Analyze the binary's strings and function names for file parsing logic. 3. Navigate to the JavaScript evaluation functions. 4. Load the crashing input into a debugger and reproduce the crash. 5. Match disassembly functions with the execution path. 6. Observe that malformed JavaScript objects cause out-of-bounds access. 7. Note missing bounds checks in object parsing. 8. Confirm root cause using GDB and conditional breakpoints. 9. Trace variable propagation from input buffer to crash. 10. Document the vulnerable function and affected memory regions.
- **Detection**: ASan, Ghidra analysis
- **Solution**: Add bounds checks, restrict embedded object length
- **Tags**: reverse engineering, binary, Ghidra, PDF

## Identify Buffer Overflow in Game Engine

- **Attack Type**: Crash Path Analysis
- **Target**: Application
- **Vulnerability**: Buffer Overflow
- **MITRE**: T1203
- **Impact**: Arbitrary Code Execution
- **Tools**: IDA Pro, x64dbg
- **Scenario**: Fuzzing reveals a crash in a game engine when parsing level files. The researcher reverse-engineers to locate the faulty logic.
- **Attack Steps**: 1. Load the game engine binary in IDA Pro. 2. Use the crash report to identify the crashing address. 3. Trace the call stack to the file parser module. 4. Follow the logic for reading object arrays from level files. 5. Identify unguarded loop indexing when reading geometry. 6. Use x64dbg to test crafted file and step through instructions. 7. Set memory watchpoints to capture overwrite. 8. Map overwritten memory to in-game object structure. 9. Determine root cause: attacker can cause arbitrary memory write. 10. Propose patch and safe bounds checking.
- **Detection**: Debugger, ASan
- **Solution**: Enforce bounds, validate array size from input
- **Tags**: game engine, IDA, overflow

## Reverse Engineering Firmware Parser

- **Attack Type**: Static Disassembly
- **Target**: Firmware Tool
- **Vulnerability**: Integer Overflow
- **MITRE**: T1068
- **Impact**: Heap Corruption
- **Tools**: Binary Ninja, GDB
- **Scenario**: Researcher investigates firmware unpacking utility used in routers for crash triggered during fuzzing.
- **Attack Steps**: 1. Open the utility in Binary Ninja. 2. Perform linear sweep and identify high-level functions. 3. Locate the segment handling firmware headers. 4. Load the crashing input into GDB and break on malloc. 5. Step through memory allocation and memcpy calls. 6. Compare structure size in header vs allocated buffer. 7. Discover the size field can be attacker-controlled. 8. Confirm memory corruption when parsing large sizes. 9. Mark this as an integer overflow + heap overwrite. 10. Document root cause with sample input and fix logic.
- **Detection**: GDB, crash input, static RE
- **Solution**: Validate header fields strictly
- **Tags**: reverse engineering, firmware, heap

## Explore Image Parsing Logic

- **Attack Type**: Input Analysis
- **Target**: Application
- **Vulnerability**: Memory Corruption
- **MITRE**: T1203
- **Impact**: Data Disclosure, DoS
- **Tools**: Ghidra, Valgrind
- **Scenario**: Analyst studies how a proprietary photo app parses EXIF metadata that led to memory corruption.
- **Attack Steps**: 1. Load the application in Ghidra and identify EXIF-related strings. 2. Trace code referencing EXIF parsing and JPEG markers. 3. Observe reading of EXIF tags into dynamic structures. 4. Review loop parsing logic for tag length and type. 5. Discover missing tag type validation. 6. Run corrupted image file in Valgrind. 7. Validate invalid read and memory leak caused by unchecked pointer arithmetic. 8. Identify exact struct layout expected by app. 9. Trace tag handler function using disassembler control flow graph. 10. Confirm exploitable out-of-bounds write vulnerability.
- **Detection**: Valgrind logs, struct review
- **Solution**: Enforce strict tag verification
- **Tags**: EXIF, image, memory, reverse engineering

## Reverse Engineer Custom Archive Format

- **Attack Type**: File Format Discovery
- **Target**: Application
- **Vulnerability**: File Parsing
- **MITRE**: T1565.001
- **Impact**: Out-of-bounds Write
- **Tools**: Ghidra, AFL-cmin, ltrace
- **Scenario**: Fuzzer found a crash in a custom archive extractor. Analyst reverse-engineers how the proprietary file format is processed.
- **Attack Steps**: 1. Run the binary with crafted crashing file using ltrace to log system calls. 2. Identify magic bytes and offset patterns. 3. Load binary in Ghidra and follow parsing logic. 4. Observe how archive table is read into structs. 5. Trace struct field used for buffer allocations. 6. Discover attacker-controlled offset leads to out-of-bounds write. 7. Use AFL-cmin to minimize PoC input. 8. Highlight offset and file index mismatch vulnerability. 9. Document file format fields and expected behavior. 10. Suggest input bounds enforcement to mitigate issue.
- **Detection**: Ghidra + ltrace
- **Solution**: Limit offsets in index tables
- **Tags**: reverse engineering, file format

## Trace JSON Parser Exploit Path

- **Attack Type**: Execution Flow Tracing
- **Target**: Application
- **Vulnerability**: Stack Overflow
- **MITRE**: T1203
- **Impact**: DoS / Potential RCE
- **Tools**: IDA Pro, PEDA
- **Scenario**: After a crash was found in a JSON config loader, the researcher traces through the logic to identify unsafe behavior.
- **Attack Steps**: 1. Load binary into IDA Pro and find the config parsing logic. 2. Observe how the keys and values are parsed using recursive descent. 3. Use PEDA inside GDB to reproduce crash with crashing config file. 4. Trace back to pointer dereference in nested value handler. 5. Identify improper handling of deeply nested values. 6. Document the recursive call depth and stack overflow risk. 7. Check for input depth limit enforcement. 8. Confirm vulnerability with reduced PoC. 9. Create control flow graph of function calls. 10. Propose limiting nesting depth and recursion control.
- **Detection**: Debugger, CFG tracing
- **Solution**: Restrict nesting depth in parser
- **Tags**: JSON, recursion, binary

## Reverse Engineer Audio File Handler

- **Attack Type**: Binary Dissection
- **Target**: Application
- **Vulnerability**: Buffer Overflow
- **MITRE**: T1203
- **Impact**: Crash, DoS
- **Tools**: Ghidra, GDB, binwalk
- **Scenario**: Analyst investigates crash in an old media player triggered by malformed MP3 tags.
- **Attack Steps**: 1. Use binwalk to inspect MP3 file structure. 2. Load binary in Ghidra and locate MP3 metadata parsing routines. 3. Observe ID3 tag handling without length validation. 4. Load crafted input in GDB to trigger crash. 5. Identify strcpy call leading to buffer overflow. 6. Map input offset to vulnerable function. 7. Confirm the crash occurs when string length > buffer size. 8. Document input vs buffer size mismatch. 9. Suggest bounds checks and safer string copy methods. 10. Recommend using strncpy or sanitizer-backed builds.
- **Detection**: GDB, binwalk, string tracing
- **Solution**: Enforce string length caps
- **Tags**: MP3, media, overflow

## Trace Vulnerable XML Parsing Logic

- **Attack Type**: File Parser Review
- **Target**: Application
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203
- **Impact**: Heap Corruption
- **Tools**: Ghidra, xmlstarlet
- **Scenario**: XML parser crashes on crafted file; researcher dissects binary to find vulnerable code.
- **Attack Steps**: 1. Load parser binary into Ghidra. 2. Find references to XML node handling routines. 3. Match them with observed tags in crashing input. 4. Discover tag size is read from input without validation. 5. Note heap buffer allocated based on tag length. 6. Use test input to trigger crash and capture stack trace. 7. Identify heap corruption from oversized tag length. 8. Trace back to vulnerable malloc pattern. 9. Document root cause and expected XML structure. 10. Recommend hard tag size caps and input schema verification.
- **Detection**: ASan, Ghidra trace
- **Solution**: Validate length fields in tag handling
- **Tags**: XML, parsing, heap

## Reverse Engineer ImageMagick-Like Tool

- **Attack Type**: Crash Debugging
- **Target**: Application
- **Vulnerability**: NULL Dereference
- **MITRE**: T1499
- **Impact**: App Crash
- **Tools**: GDB, Ghidra, ImageMagick
- **Scenario**: Open-source image converter crashes on specific PNG files. Analyst studies the tool’s behavior.
- **Attack Steps**: 1. Load binary into Ghidra to find PNG decoder module. 2. Use GDB to reproduce crash on crafted PNG. 3. Observe stack trace leads to color profile reader. 4. Identify unchecked pointer dereference after reading chunk. 5. Map crashing input chunk to code in disassembler. 6. Discover attacker can trigger NULL pointer dereference. 7. Add conditional breakpoint to validate pointer nullness. 8. Confirm issue is triggered by malformed chunk size. 9. Minimize input to isolate issue. 10. Recommend validation before pointer use.
- **Detection**: GDB, input chunk analysis
- **Solution**: Pointer null-checking before usage
- **Tags**: PNG, image, bug

## Analyze Malware Payload in Obfuscated Binary

- **Attack Type**: Malware Behavior Analysis
- **Target**: Malware
- **Vulnerability**: Code Injection
- **MITRE**: T1055
- **Impact**: Remote Code Execution
- **Tools**: IDA Pro, Ghidra, x64dbg
- **Scenario**: Security researcher reverse engineers an obfuscated binary found during fuzzing to uncover embedded payload logic.
- **Attack Steps**: 1. Load obfuscated binary in IDA Pro. 2. Identify anti-disassembly techniques (e.g., opaque predicates). 3. Rename functions and constants where possible. 4. Follow API calls to resolve behavior dynamically. 5. Use x64dbg to dump decrypted strings at runtime. 6. Discover shellcode embedded in decrypted section. 7. Trace shellcode loading and execution logic. 8. Break on VirtualAlloc/WriteProcessMemory to monitor injection. 9. Document full payload execution path. 10. Recommend IOC-based detection and AV signature development.
- **Detection**: Runtime analysis, memory dumps
- **Solution**: AV signature, runtime monitoring
- **Tags**: shellcode, reverse engineering, malware

