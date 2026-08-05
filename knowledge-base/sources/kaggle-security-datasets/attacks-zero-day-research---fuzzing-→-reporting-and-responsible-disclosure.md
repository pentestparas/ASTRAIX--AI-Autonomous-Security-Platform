# Zero-Day Research / Fuzzing → Reporting & Responsible Disclosure Attacks

## Creating a Structured Vulnerability Report

- **Attack Type**: Reporting
- **Target**: Custom Binary
- **Vulnerability**: Heap Overflow
- **MITRE**: T1595.002
- **Impact**: Information Disclosure
- **Tools**: Text Editor, ASAN Logs, GDB
- **Scenario**: After discovering a heap overflow in a custom image parser, the researcher needs to document and report it to the vendor.
- **Attack Steps**: 1. Open a new document using a text editor and write an executive summary of the bug.2. Describe the application and version where the bug was found.3. Attach the crashing input (e.g., malformed image file).4. Include ASAN logs or GDB backtrace to support analysis.5. Provide information about the test environment: OS, compiler flags, sanitizer used.6. Clearly explain the root cause (e.g., unchecked memory allocation).7. Mention any exploitability indicators.8. Outline possible security implications (DoS, RCE).9. Format the report in sections: Summary, Steps to Reproduce, Analysis, Impact, Fix Suggestion.10. Save as PDF and archive supporting files.
- **Detection**: Manual Review
- **Solution**: Submit to vendor with clear breakdown and reproduction
- **Tags**: reporting, vulnerability, ASAN, responsible-disclosure

## Submitting a Bug Report via HackerOne

- **Attack Type**: Responsible Disclosure
- **Target**: Web Application
- **Vulnerability**: Memory Corruption
- **MITRE**: T1609
- **Impact**: Remote Crash, Bug Bounty
- **Tools**: HackerOne, Browser, Debug Logs
- **Scenario**: A security researcher wants to report a memory corruption vulnerability to a company using HackerOne.
- **Attack Steps**: 1. Log in to HackerOne and navigate to the specific vendor’s program page.2. Read the vendor's disclosure guidelines and scope.3. Click “Submit Report.”4. Fill in the vulnerability title and a brief summary.5. Write detailed steps to reproduce the crash, including file name and execution command.6. Paste ASAN output or debugger logs into the “Details” section.7. Mention any proof of concept or crafted input.8. Set the severity and mark if the issue is within scope.9. Attach supporting files (crash file, logs, screenshots).10. Submit and monitor status for triage updates.
- **Detection**: Bug Tracker Notification
- **Solution**: Follow vendor scope and format
- **Tags**: bug-bounty, hackerone, submission, coordinated-disclosure

## Reporting Vulnerability via Microsoft MSRC Portal

- **Attack Type**: Coordinated Disclosure
- **Target**: Windows Kernel
- **Vulnerability**: Use-After-Free
- **MITRE**: T1068
- **Impact**: Privilege Escalation
- **Tools**: MSRC Portal, WinDbg, PoC File
- **Scenario**: A researcher finds a Windows kernel bug and needs to report it through Microsoft Security Response Center (MSRC).
- **Attack Steps**: 1. Visit msrc.microsoft.com and sign in with a Microsoft account.2. Click “Report an Issue” and select the type (Windows, Azure, etc.).3. Fill in product details and OS version.4. Describe the crash and attach a reproducible PoC.5. Provide debugger output using WinDbg with !exploitable plugin.6. Explain how the issue could be exploited (e.g., privilege escalation).7. Mention any potential mitigation or suggestions.8. Accept the Coordinated Vulnerability Disclosure (CVD) policy.9. Submit the report and receive case number.10. Follow up for patch timeline or CVE assignment.
- **Detection**: Kernel Crash Logs
- **Solution**: Submit through official MSRC portal
- **Tags**: msrc, windows, kernel, responsible-disclosure

## Coordinating Disclosure with Google VRP

- **Attack Type**: Vulnerability Reporting
- **Target**: Browser Engine
- **Vulnerability**: Type Confusion
- **MITRE**: T1203
- **Impact**: Remote Code Execution
- **Tools**: Google VRP Portal, Chrome Canary, Crash Logs
- **Scenario**: Reporting a JavaScript engine bug found during browser fuzzing to Google’s VRP.
- **Attack Steps**: 1. Open bughunters.google.com and sign in.2. Select "New Report" and specify “Chrome” as product.3. Add details: Chrome version, platform (e.g., Windows 10).4. Write steps to reproduce using the malformed HTML/JS file.5. Attach the crashing input and debugger logs.6. Include trace from ClusterFuzz or ASAN.7. Describe the root cause (e.g., type confusion in JIT compiler).8. Provide severity assessment (RCE potential).9. Include reproduction video or screenshots.10. Submit and track via the platform for bounty eligibility.
- **Detection**: ClusterFuzz, ASAN logs
- **Solution**: Submit using VRP with PoC and analysis
- **Tags**: google-vrp, browser, javascript-engine, bug-report

## Writing a CVE-Ready Report for Open Source Project

- **Attack Type**: CVE Filing
- **Target**: Open Source Parser
- **Vulnerability**: Buffer Overflow
- **MITRE**: T1204.002
- **Impact**: DoS / Potential RCE
- **Tools**: GitHub Issues, OSS-Sec Mailing List, CVE Form
- **Scenario**: Reporting a buffer overflow in an open-source PDF parser via GitHub issues and preparing for CVE.
- **Attack Steps**: 1. Clone the affected open-source project locally.2. Test and confirm crash using fuzzed input.3. Create a minimal input file and document behavior.4. Open a GitHub issue and report respectfully.5. Include analysis, crash logs, and recommended patch (if possible).6. Notify maintainers via email or mailing list.7. Coordinate with MITRE or a CNA for CVE allocation.8. Fill CVE Request Template: Vendor, Product, Version, Description.9. Submit it to MITRE’s webform or CNA like HackerOne.10. Wait for confirmation and keep track of disclosure date.
- **Detection**: Manual testing, GitHub Issue
- **Solution**: Coordinate via GitHub and MITRE
- **Tags**: cve, github, opensource, responsible-disclosure

## Responsible Disclosure to Adobe via Security Email

- **Attack Type**: Email Disclosure
- **Target**: PDF Reader
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203
- **Impact**: Application Crash
- **Tools**: Adobe Security Email, ASAN Logs
- **Scenario**: A vulnerability in Adobe Reader is discovered; the vendor is contacted through email.
- **Attack Steps**: 1. Prepare a comprehensive report detailing the vulnerability.2. Include software version, platform, and exact reproduction steps.3. Attach crafted PDF causing the crash.4. Add stack trace or sanitizer output.5. Include explanation of security impact (e.g., heap overflow leads to RCE).6. Draft an email to PSIRT (e.g., security@adobe.com).7. Attach report and input files.8. Mention your intent to follow coordinated disclosure.9. Encrypt the email using Adobe's PGP key (if available).10. Await response and engage in follow-up as needed.
- **Detection**: Email log tracking
- **Solution**: Use PGP and vendor-sec contact
- **Tags**: adobe, email-disclosure, pdf, responsible-disclosure

## Preparing Proof-of-Concept for Disclosure

- **Attack Type**: PoC Creation
- **Target**: Media Player
- **Vulnerability**: Stack Overflow
- **MITRE**: T1204.002
- **Impact**: Application DoS
- **Tools**: Debugger, Fuzzer Output, Text Editor
- **Scenario**: A researcher prepares a PoC that triggers a crash in a media player to accompany their report.
- **Attack Steps**: 1. Identify the minimal input that causes the crash reliably.2. Reduce and clean the input using tools like afl-tmin.3. Test it across versions to confirm it still crashes.4. Create a README.txt with execution instructions.5. Mention the expected crash signature.6. Add output from ASAN or debugger.7. Zip the file with a name like PoC_crash_audio.avi.8. Create a demo video showing crash with the input.9. Reference this PoC in the vulnerability report.10. Submit all assets with your disclosure email or portal submission.
- **Detection**: Visual confirmation, logs
- **Solution**: Create easy-to-use test case for vendor
- **Tags**: poc, reproducible-input, responsible-disclosure

## Disclosing via CERT/CC for Hard-to-Reach Vendors

- **Attack Type**: Third-Party Mediation
- **Target**: Legacy Software
- **Vulnerability**: Memory Violation
- **MITRE**: T1589
- **Impact**: Third-Party Coordination
- **Tools**: CERT/CC Portal, Email, CVE Services
- **Scenario**: A legacy software vendor is unresponsive, so the researcher uses CERT/CC to coordinate disclosure.
- **Attack Steps**: 1. Prepare all vulnerability documentation (PoC, logs, analysis).2. Visit kb.cert.org and follow instructions to submit a vulnerability.3. Fill out the intake form: affected product, version, description, discovery timeline.4. Attach technical details and supporting files.5. Indicate any prior attempt to contact the vendor.6. Agree to CERT/CC coordination timeline.7. Await triage and assignment of case ID.8. CERT/CC will attempt contact with vendor.9. Follow up to request CVE if no response.10. Use CERT’s advisory if vendor remains silent.
- **Detection**: CERT reports
- **Solution**: Route via CERT for coordination
- **Tags**: cert, unresponsive-vendor, cve, coordination

## Submitting via Bugcrowd Platform

- **Attack Type**: Bug Bounty
- **Target**: Web API
- **Vulnerability**: Logic Bypass
- **MITRE**: T1190
- **Impact**: Unauthorized Access
- **Tools**: Bugcrowd Platform, Network Tools
- **Scenario**: Reporting a logic bug in a network API using Bugcrowd.
- **Attack Steps**: 1. Log in to Bugcrowd and select the target program.2. Review the scope and bounty structure.3. Create a new submission.4. Write a detailed summary of the issue.5. Include API endpoint, method, and parameters.6. Explain how logic bypass occurs (e.g., auth skipped).7. Attach screenshots, logs, or Wireshark traces.8. Suggest potential fixes.9. Submit and interact with triage team.10. Track resolution and bounty status.
- **Detection**: API logs, test cases
- **Solution**: Vendor review and fix via triage
- **Tags**: bugcrowd, api, logic-bug, reporting

## Including CVSS Metrics in Reports

- **Attack Type**: CVSS Analysis
- **Target**: Any Software
- **Vulnerability**: Any
- **MITRE**: T1592
- **Impact**: Informs Vendor Prioritization
- **Tools**: CVSS Calculator, ASAN Logs
- **Scenario**: Estimating severity using CVSS 3.1 metrics for a disclosed vulnerability.
- **Attack Steps**: 1. Visit the FIRST CVSS calculator.2. Set Attack Vector (e.g., Local or Network).3. Choose Attack Complexity (Low/High).4. Define Privileges Required and User Interaction.5. Select scope, confidentiality, integrity, and availability impact.6. View the base score (e.g., 7.8 High).7. Include vector string and score in your report.8. Explain why these choices were made.9. Help vendor understand urgency.10. Submit report with CVSS included to expedite triage.
- **Detection**: CVSS Vector Review
- **Solution**: Score supports triage decisions
- **Tags**: cvss, scoring, vulnerability-severity

## Reporting Out-of-Bounds Write in Media Parser

- **Attack Type**: Responsible Disclosure
- **Target**: Media Parser
- **Vulnerability**: Heap Overflow
- **MITRE**: T1203
- **Impact**: Remote Code Execution
- **Tools**: GDB, ASan, BinDiff
- **Scenario**: A researcher discovers a heap out-of-bounds write when fuzzing a proprietary media parser library
- **Attack Steps**: 1. Identify the crash using AddressSanitizer output while fuzzing the media parser.2. Open the binary in GDB and reproduce the crash with the input.3. Confirm memory corruption and trace the exact write location.4. Save the crashing input, ASAN log, and backtrace.5. Prepare a PDF report describing the crash, root cause analysis, and risk (e.g., potential for RCE).6. Use the vendor’s security portal to upload the bug (e.g., Adobe’s HackerOne portal).7. Communicate with the vendor’s triage team and respond to follow-up queries.8. Wait for the patch release or CVE before public disclosure.
- **Detection**: ASan + Debugger
- **Solution**: Patch issued by vendor
- **Tags**: media, bug bounty, oob-write, fuzzing

## Submitting Use-After-Free in Kernel Network Stack

- **Attack Type**: Coordinated Disclosure
- **Target**: Linux Kernel
- **Vulnerability**: Use-After-Free
- **MITRE**: T1068
- **Impact**: Kernel Panic or Escalation
- **Tools**: syzkaller, kmemleak, LKDG, GDB
- **Scenario**: Use-after-free discovered in Linux kernel via syzkaller automated fuzzing
- **Attack Steps**: 1. Collect the crash info and log from syzkaller’s dashboard.2. Confirm use-after-free by reproducing crash in a VM using same syscall sequences.3. Analyze kernel backtrace and identify freed object type.4. Document kernel version, .config file, stack trace, and memory addresses.5. Submit the issue privately to linux-distros mailing list with 7-day embargo.6. Coordinate with kernel maintainers until fix is merged.7. Request CVE if needed.8. Publicly disclose after patch is included in LTS kernels.
- **Detection**: Memory monitoring + kmemleak
- **Solution**: Vendor patch and embargo
- **Tags**: kernel, use-after-free, syzkaller, cve

## Reporting Integer Overflow in Game Engine Script Parser

- **Attack Type**: Bug Bounty Disclosure
- **Target**: Game Engine
- **Vulnerability**: Type Confusion
- **MITRE**: T1203
- **Impact**: Possible RCE
- **Tools**: libFuzzer, Ghidra, GDB
- **Scenario**: A type confusion vulnerability is found when fuzzing a Lua-based script engine in a popular game engine
- **Attack Steps**: 1. Fuzz the engine using structured Lua inputs and detect integer overflow.2. Analyze the crash path in Ghidra and note the casting operation causing type confusion.3. Verify impact by building a PoC that triggers a crash with type confusion.4. Save the test case, binary version, and analysis in a folder.5. Report the issue via the vendor’s bug bounty platform.6. Submit complete report: affected versions, crash repro, and exploitability.7. Wait for response, verify fix in next update.8. If permitted, publish vulnerability write-up post patch.
- **Detection**: PoC + dynamic trace
- **Solution**: Vendor fix in engine
- **Tags**: bug bounty, game engine, integer bug

## Disclosing Buffer Overflow in Open-Source Compression Library

- **Attack Type**: Open Source Disclosure
- **Target**: Compression Library
- **Vulnerability**: Stack Buffer Overflow
- **MITRE**: T1204
- **Impact**: Arbitrary Code Execution
- **Tools**: AFL++, Valgrind, AddressSanitizer
- **Scenario**: A buffer overflow is found in a widely-used open-source compression library during fuzzing campaign
- **Attack Steps**: 1. Use AFL++ to fuzz the decompression logic with malformed input files.2. Catch a crash using ASan or Valgrind.3. Reproduce and confirm a classic buffer overflow.4. Document the bug with affected function, faulty bounds check, and test case.5. File a GitHub issue marked as security and notify project maintainers via email.6. Suggest patch or mitigation if possible.7. Wait for maintainer to fix and tag version.8. Help coordinate disclosure timeline and CVE assignment.
- **Detection**: ASan logs + GitHub PR review
- **Solution**: Code patch + CVE
- **Tags**: open source, buffer overflow, disclosure

## Coordinated Disclosure of Sandbox Escape in PDF Reader

- **Attack Type**: Sandbox Escape
- **Target**: PDF Reader
- **Vulnerability**: Sandbox Escape
- **MITRE**: T1203
- **Impact**: Sandbox Bypass
- **Tools**: WinDbg, Hex-Rays, ProcMon
- **Scenario**: Discovered an input that leads to memory corruption escaping the PDF sandbox
- **Attack Steps**: 1. Fuzz PDF parsing logic using malformed JavaScript embedded PDFs.2. Observe a crash that spawns an unexpected system process using ProcMon.3. Use WinDbg to inspect memory write violating sandbox boundary.4. Confirm behavior in multiple PDF reader versions.5. Document in-depth report with test files, analysis, and screenshots.6. Submit report to the PDF vendor's security portal.7. Communicate securely and follow up as needed.8. Wait for patch and assign CVE before blog post or talk.
- **Detection**: Memory + behavioral logging
- **Solution**: Vendor fix and advisory
- **Tags**: sandbox, pdf, js exploit

## Reporting Format String Bug in IoT Device Firmware

- **Attack Type**: Embedded Vulnerability Disclosure
- **Target**: IoT Device
- **Vulnerability**: Format String Vulnerability
- **MITRE**: T1055
- **Impact**: Memory Leak
- **Tools**: Ghidra, Serial Monitor, UART Debugger
- **Scenario**: A format string vulnerability is found in a UART interface during manual testing of IoT firmware
- **Attack Steps**: 1. Reverse firmware using Ghidra and identify UART debug commands.2. Send crafted input with multiple %x to trigger info leak.3. Confirm vulnerability using UART interface on actual device.4. Capture full debug output, firmware version, and memory leak locations.5. Contact vendor through their security email (e.g., security@vendor.com).6. Provide PoC script and analysis of impact.7. Help coordinate fix and firmware update.8. Request CVE and wait before public disclosure.
- **Detection**: Manual fuzz + hardware debug
- **Solution**: Firmware patch
- **Tags**: iot, firmware, format string

## Submitting Null Pointer Dereference in File Parser

- **Attack Type**: Low Severity Bug Report
- **Target**: File Parser
- **Vulnerability**: Null Pointer Dereference
- **MITRE**: T1499
- **Impact**: Denial of Service
- **Tools**: libFuzzer, GDB
- **Scenario**: Null dereference bug found during file fuzzing that crashes the parser
- **Attack Steps**: 1. Run fuzzing with malformed inputs targeting parser.2. Find crash where program dereferences a NULL pointer.3. Debug and confirm the crash point.4. Save input and logs.5. Submit a low severity issue via bug bounty or public tracker.6. Explain that while not exploitable, it causes DoS.7. Provide fix suggestion or bounds check.8. Await update or patch note.
- **Detection**: libFuzzer + GDB
- **Solution**: Input validation patch
- **Tags**: null deref, dos, bug report

## Responsible Disclosure of Memory Leak in Web Server Module

- **Attack Type**: Memory Leak
- **Target**: Web Server
- **Vulnerability**: Memory Leak
- **MITRE**: T1499
- **Impact**: Performance Degradation
- **Tools**: Valgrind, Massif, GDB
- **Scenario**: Detected memory leak in request handling of HTTP server module
- **Attack Steps**: 1. Run Valgrind’s massif tool on HTTP server under repeated requests.2. Identify steadily growing heap usage.3. Trace missing free() in request cleanup logic.4. Save massif output, code pointer, and config used.5. File private issue on project tracker or email developer.6. Suggest garbage collection or memory management fix.7. Patch and verify leak is fixed.8. Credit researcher in changelog if allowed.
- **Detection**: Valgrind + request replay
- **Solution**: Leak fix in handler logic
- **Tags**: server, memory leak, triage

## Reporting Arbitrary File Write in Archiver App

- **Attack Type**: File Write Primitives
- **Target**: Archiver App
- **Vulnerability**: Path Traversal
- **MITRE**: T1006
- **Impact**: Arbitrary File Write
- **Tools**: Ghidra, WinDbg, ProcMon
- **Scenario**: Found a way to write arbitrary files outside extraction directory
- **Attack Steps**: 1. Inspect archive extraction code in Ghidra.2. Create ZIP archive with ../ path traversal payload.3. Extract and observe file written outside target folder.4. Use ProcMon to validate file system activity.5. Submit detailed report to vendor with PoC zip.6. Recommend filename sanitization logic.7. Verify fix and wait for coordinated patch date.8. Submit to CVE program if eligible.
- **Detection**: ProcMon + binary reverse
- **Solution**: Fix path sanitization
- **Tags**: zip, file write, traversal

## Submitting Bug in Secure Messaging Client

- **Attack Type**: Disclosure via HackerOne
- **Target**: Messaging App
- **Vulnerability**: Input Parsing Bug
- **MITRE**: T1134
- **Impact**: App Crash or DoS
- **Tools**: Frida, GDB, Ghidra
- **Scenario**: Researcher discovers malformed emoji string causes app crash
- **Attack Steps**: 1. Monitor crash when sending certain Unicode emoji strings.2. Debug app with GDB and confirm crash due to string parsing bug.3. Identify cause in emoji parser function.4. Document app version, payload, and backtrace.5. Submit via HackerOne or similar bounty platform.6. Await triage, confirm bug, and receive fix timeline.7. Do not disclose until vendor marks report public.8. Provide optional patch suggestion or test script.
- **Detection**: GDB + payload test
- **Solution**: Vendor fixes parser
- **Tags**: emoji, unicode, bounty

## Report Use-After-Free in PDF Reader

- **Attack Type**: Use-After-Free PoC Reporting
- **Target**: PDF Parsing Engine
- **Vulnerability**: Use-After-Free
- **MITRE**: T1203
- **Impact**: Remote Code Execution
- **Tools**: GDB, ASAN, Bugzilla
- **Scenario**: Researcher discovered a use-after-free vulnerability in a popular PDF reader using fuzzing.
- **Attack Steps**: 1. Use AFL to fuzz a popular open-source PDF reader binary. 2. Discover a crash due to use-after-free with a small PDF file. 3. Use AddressSanitizer to confirm memory issue. 4. Debug in GDB to trace pointer reuse after free. 5. Prepare a vulnerability report including test case, binary version, crash trace, and debugger output. 6. Submit via vendor's security portal with detailed description. 7. Wait for vendor triage and CVE assignment. 8. Cooperate for coordinated disclosure.
- **Detection**: Memory monitoring and crash correlation
- **Solution**: Patch vulnerable PDF parser logic
- **Tags**: fuzzing, responsible disclosure, ASAN, PDF, use-after-free

## Coordinated Disclosure of Memory Leak in Compression Library

- **Attack Type**: Memory Leak Analysis & Report
- **Target**: Compression Utility
- **Vulnerability**: Memory Leak
- **MITRE**: T1647
- **Impact**: Resource Exhaustion
- **Tools**: Valgrind, GitHub Issues
- **Scenario**: Discovered a memory leak in open-source compression library affecting embedded systems.
- **Attack Steps**: 1. Use Valgrind to analyze memory usage during fuzzing of compression functions. 2. Identify unreleased heap allocations on malformed inputs. 3. Reproduce issue and confirm leak with standalone test harness. 4. Write a comprehensive report with code snippet, repro steps, tool logs. 5. Reach out to maintainer via GitHub security advisory. 6. Respect coordinated disclosure timeline. 7. Assist maintainers with fix validation. 8. Finalize public disclosure and CVE publication post patch.
- **Detection**: Static analysis and leak detection
- **Solution**: Fix leak in memory management logic
- **Tags**: CVE, memory-leak, open source, fuzzing, Valgrind

## Disclose Integer Overflow in Video Codec

- **Attack Type**: Input Validation Vulnerability Disclosure
- **Target**: Video Codec Binary
- **Vulnerability**: Integer Overflow
- **MITRE**: T1204
- **Impact**: Heap Corruption / RCE
- **Tools**: AFL++, WinDbg, !exploitable
- **Scenario**: A fuzzed MKV file caused integer overflow in custom video codec, leading to heap overwrite.
- **Attack Steps**: 1. Fuzz the MKV file parser of the codec using AFL++. 2. Trigger a crash due to corrupted heap metadata. 3. Attach in WinDbg and use !exploitable to confirm potential RCE. 4. Prepare report including exact file, crash analysis, and suggested fix. 5. Upload via software vendor’s private portal (e.g., HackerOne). 6. Engage with vendor’s security response team for debugging. 7. Receive bounty and credit post-patch. 8. Publicly share results responsibly.
- **Detection**: Heap monitoring and code inspection
- **Solution**: Add bounds check before allocation
- **Tags**: win32, fuzzing, integer overflow, exploitability

## Chrome Extension JS Injection Disclosure

- **Attack Type**: Content-Script XSS Disclosure
- **Target**: Chrome Extension
- **Vulnerability**: DOM-Based XSS
- **MITRE**: T1059
- **Impact**: Arbitrary Code Injection
- **Tools**: Burp Suite, Chrome DevTools
- **Scenario**: A browser extension with weak input validation allowed injection into DOM via message listener.
- **Attack Steps**: 1. Identify an unescaped DOM write in a Chrome extension’s content script. 2. Craft a malicious message that triggers arbitrary JavaScript injection. 3. Verify injection works across multiple versions. 4. Capture console logs and PoC video. 5. Report via Chrome Web Store Developer Security page. 6. Share detailed report with extension source code and testing script. 7. Await action, which includes removal or patch. 8. Mark the issue on extension review platforms.
- **Detection**: DevTools trace of unsafe DOM access
- **Solution**: Patch extension to sanitize input
- **Tags**: chrome, XSS, PoC, responsible disclosure

## Sandbox Escape via Shared Memory Abuse

- **Attack Type**: Sandbox Escape Vulnerability Report
- **Target**: Chromium Browser
- **Vulnerability**: Sandbox Escape
- **MITRE**: T1087
- **Impact**: Privilege Escalation
- **Tools**: Syzkaller, GDB, Chrome Bug Tracker
- **Scenario**: Researcher found a way to escape Chrome’s renderer sandbox via shared memory side-channel.
- **Attack Steps**: 1. Use syzkaller to fuzz inter-process shared memory usage in Chromium. 2. Identify timing leak between renderer and privileged process. 3. Design a PoC to infer memory layout using race conditions. 4. Document with GDB snapshots, timeline of IPCs, and reproducer. 5. Report through Chromium’s security tracker. 6. Wait for triage and potential security impact rating. 7. Collaborate if clarification or retesting is required. 8. Disclose after sandbox fix is deployed in stable version.
- **Detection**: Timing analysis and IPC monitoring
- **Solution**: Fix race in shared memory logic
- **Tags**: chrome, sandbox, side-channel, fuzzing

## Email Vendor Buffer Overflow via Attachment

- **Attack Type**: Buffer Overflow PoC Submission
- **Target**: Email Client
- **Vulnerability**: Stack Overflow
- **MITRE**: T1068
- **Impact**: RCE via Malicious File
- **Tools**: libFuzzer, ASAN, CrashWrangler
- **Scenario**: A malformed email attachment triggered stack buffer overflow in proprietary mail client.
- **Attack Steps**: 1. Fuzz mail client’s attachment parser using libFuzzer. 2. Discover stack buffer overflow upon parsing long field in proprietary format. 3. Analyze ASAN output and control flow. 4. Use CrashWrangler to confirm exploitability. 5. Write a full report with binary version, fuzzing config, PoC file. 6. Contact vendor through security email. 7. Negotiate CVE allocation and follow up for patch timeline. 8. Disclose findings after patch release.
- **Detection**: Stack smashing logs and symbol offset analysis
- **Solution**: Add bounds checks in parser
- **Tags**: buffer overflow, mail, responsible disclosure, PoC

## Disclose XML Entity Expansion (Billion Laughs) Bug

- **Attack Type**: Denial of Service Vulnerability Disclosure
- **Target**: HR Management Software
- **Vulnerability**: XML Bomb
- **MITRE**: T1499
- **Impact**: Denial of Service
- **Tools**: xmllint, custom script
- **Scenario**: Researcher discovered a denial of service via XML bomb in enterprise HR software.
- **Attack Steps**: 1. Generate XML “billion laughs” entity expansion payload. 2. Feed it into the target HR software's XML parser. 3. Confirm system freeze or high CPU utilization. 4. Capture logs and show memory exhaustion. 5. Prepare formal report with explanation of XML bomb concept. 6. Report via enterprise vendor’s responsible disclosure program. 7. Assist in reproducing issue. 8. Monitor fix deployment before public blog post.
- **Detection**: CPU and memory usage analysis
- **Solution**: Limit XML entity parsing depth
- **Tags**: DoS, XML, billion laughs, CVE

## PoC Report: Broken ACL on Android App Logs

- **Attack Type**: Mobile App Info Leak Report
- **Target**: Android App
- **Vulnerability**: Insecure Logging
- **MITRE**: T1087
- **Impact**: Info Disclosure
- **Tools**: ADB, logcat
- **Scenario**: A popular Android app exposed sensitive logs due to improper ACLs on log files.
- **Attack Steps**: 1. Install the app on Android 11 using emulator. 2. Observe private info written to world-readable log file. 3. Pull logs using ADB and analyze sensitive tokens exposed. 4. Prepare technical report showing file path, timestamps, and impact. 5. Report via Google Play App Security form. 6. Engage with devs to help understand log rotation. 7. Disclose post-patch in Android security bulletin. 8. Request CVE and bounty if applicable.
- **Detection**: File permission inspection and log parsing
- **Solution**: Restrict file access and remove PII
- **Tags**: android, mobile, insecure logs, CVE

## Vulnerability Submission for Proprietary Archive Parser

- **Attack Type**: Archive Parsing Bug Report
- **Target**: Archive Utility
- **Vulnerability**: Null Pointer Dereference
- **MITRE**: T1546
- **Impact**: Program Crash
- **Tools**: Ghidra, AFL++, LLDB
- **Scenario**: Fuzzer identified a null pointer dereference in proprietary archive utility used by enterprises.
- **Attack Steps**: 1. Instrument proprietary .arc file parser with AFL++. 2. Fuzz input and discover crash with null pointer access. 3. Open binary in Ghidra and reverse-engineer function path. 4. Confirm missing null-check for header parsing. 5. Package PoC file and debugger trace. 6. Report via vendor’s enterprise vulnerability response center. 7. Track CVE status and patch release. 8. Add advisory to vulnerability database.
- **Detection**: Ghidra disassembly, input tracing
- **Solution**: Validate input headers properly
- **Tags**: reverse engineering, bug report, archive format

## Coordinated Reporting of Type Confusion in Browser

- **Attack Type**: Browser Type Confusion Report
- **Target**: JavaScript Engine
- **Vulnerability**: Type Confusion
- **MITRE**: T1027
- **Impact**: RCE Risk in Browser
- **Tools**: jsfunfuzz, gdb, !exploitable
- **Scenario**: During JS engine fuzzing, a type confusion was found in a major browser.
- **Attack Steps**: 1. Fuzz JS engine using jsfunfuzz. 2. Crash occurs when array and object type are misinterpreted. 3. Debug in GDB to trace wrong type cast during optimization. 4. Use !exploitable plugin to assess risk. 5. Document engine version, input, crash trace, and fix suggestion. 6. Submit via browser vendor’s bug tracker. 7. Collaborate until issue is patched. 8. Publish advisory with root cause analysis.
- **Detection**: JS engine trace and memory layout analysis
- **Solution**: Fix type inference logic
- **Tags**: browser, JS engine, fuzzing, CVE

## Submitting Exploit to Mozilla Bugzilla

- **Attack Type**: Coordinated Disclosure
- **Target**: Browser
- **Vulnerability**: Use-after-free
- **MITRE**: T1595
- **Impact**: Remote Code Execution
- **Tools**: Firefox, ASAN, Bugzilla
- **Scenario**: Researcher finds a crash in Firefox through fuzzing and needs to report it through Bugzilla responsibly.
- **Attack Steps**: 1. Identify the version of Firefox where the crash occurs and record build details.2. Save the crashing input, ASAN log, and debugger trace.3. Log in to bugzilla.mozilla.org.4. Click on "File a Bug", select "Firefox" as the product.5. Fill in the bug summary, and in the description include the crash repro steps, ASAN log, input file, and any debugger output.6. Mark the bug as "Security Sensitive" to restrict visibility.7. Choose an appropriate component (e.g., Networking, JavaScript Engine).8. Submit the bug.9. Monitor updates and be available to clarify technical details if Mozilla engineers need follow-up.10. Do not publish the crash or details until Mozilla issues a fix and discloses the bug.
- **Detection**: Bugzilla Internal Tagging
- **Solution**: Wait for fix, retest patch
- **Tags**: disclosure, browser, vendor

## Coordinated Disclosure to Linux Kernel Mailing List

- **Attack Type**: Responsible Vulnerability Disclosure
- **Target**: Kernel
- **Vulnerability**: Stack overflow
- **MITRE**: T1546.010
- **Impact**: Kernel Panic / Crash
- **Tools**: Syzkaller, GDB, kernel mailing list
- **Scenario**: Kernel crash triggered using syzkaller needs to be responsibly disclosed to Linux maintainers.
- **Attack Steps**: 1. Save the kernel version, crashing config, and syzkaller reproducer.2. Capture GDB backtrace and crash logs.3. Write a minimal but clear vulnerability report including steps to reproduce, impact, and patch suggestion if possible.4. Email the report to security@kernel.org, CC relevant maintainers (via scripts/get_maintainer.pl).5. Set the subject line clearly e.g., [SECURITY] Kernel crash in netfilter via syzkaller.6. Do not disclose the bug publicly until acknowledged and patched.7. Stay engaged to test patches or clarify if the maintainers request follow-up.8. If the bug is fixed, wait for it to be merged into mainline before public CVE request.9. Use oss-security@lists.openwall.com later for public disclosure.10. Optionally, request a CVE through MITRE or Linux distros.
- **Detection**: Kernel logs, syzkaller triage
- **Solution**: Send patch or wait for official patch
- **Tags**: linux, mailing list, kernel, fuzz

## Submitting Bugs via HackerOne

- **Attack Type**: Bug Bounty Submission
- **Target**: Web App
- **Vulnerability**: Type Confusion
- **MITRE**: T1609
- **Impact**: Service Disruption
- **Tools**: Custom fuzzers, ASAN, HackerOne
- **Scenario**: Researcher finds a crash in a popular SaaS platform and reports it via HackerOne.
- **Attack Steps**: 1. Document the fuzzing setup, payload, target endpoint, and impact.2. Save logs, reproduction steps, and screenshots if applicable.3. Log into HackerOne, find the program accepting reports for the platform.4. Click "Report a Vulnerability".5. Write a clear title and summary; paste full technical detail, including PoC, crash log, ASAN trace.6. Attach proof-of-concept files if permitted.7. Choose relevant severity level based on the scope.8. Submit the report and engage with triage team.9. Respond to clarifications and help validate the fix.10. Once patched and permitted, request public disclosure via HackerOne.
- **Detection**: Triage team logs and QA repro
- **Solution**: Submit PoC with minimal reproduction
- **Tags**: bounty, web, vendor

## Using Google's Issue Tracker for Chrome Bugs

- **Attack Type**: Coordinated Disclosure
- **Target**: Browser
- **Vulnerability**: Heap buffer overflow
- **MITRE**: T1203
- **Impact**: Remote code execution
- **Tools**: AFL++, Chrome with ASAN, Chromium Issue Tracker
- **Scenario**: Chrome renderer crash found through AFL++ is disclosed via Chromium issue tracker.
- **Attack Steps**: 1. Run fuzzing campaign with AFL++ on the Chrome rendering engine.2. Save the crashing input and stack trace.3. Visit crbug.com, click “New Issue”.4. Login with Google Account and select Chromium project.5. Fill in summary, steps to reproduce, expected/actual result, and attach ASAN logs and input files.6. Mark issue as “Security” and restrict to Google engineers.7. Choose relevant labels like "Blink>DOM" or "Security".8. Submit and track the issue.9. Wait for assignment and be ready to answer clarifications.10. Public disclosure is permitted only after patch and at Google’s discretion.
- **Detection**: Chromium Bug System
- **Solution**: Patch + vendor coordination
- **Tags**: chrome, crash, heap, google

## Creating Vulnerability Report for CVE Request

- **Attack Type**: CVE Filing
- **Target**: Any
- **Vulnerability**: Memory corruption
- **MITRE**: T1592
- **Impact**: Public Disclosure
- **Tools**: CVE Form, Vuln Reporter Tools
- **Scenario**: Researcher finds exploitable bug and prepares a formal report for CVE assignment.
- **Attack Steps**: 1. Ensure the bug is in a product eligible for CVE (public-facing, supported software).2. Prepare crash report, PoC, affected versions.3. Determine if CVE ID already exists; if not, file through MITRE's CVE Request Form.4. Include detailed write-up: description, impact, how to reproduce, severity.5. Mention whether patch exists or in progress.6. Submit via https://cveform.mitre.org/.7. Respond to MITRE’s emails to confirm details.8. Upon CVE assignment, update any public tracker or vendor reference.9. Wait for embargo to lift if vendor asked.10. Publish full advisory responsibly (e.g., on personal blog, oss-security).
- **Detection**: MITRE confirmation
- **Solution**: File CVE then sync with vendor
- **Tags**: CVE, public, exploit

## Reporting Windows Kernel Bug to MSRC

- **Attack Type**: Vendor Disclosure
- **Target**: Kernel
- **Vulnerability**: Privilege Escalation
- **MITRE**: T1068
- **Impact**: Kernel Exploit
- **Tools**: WinDbg, !exploitable, MSRC Portal
- **Scenario**: A critical bug in Windows kernel leads to crash and possible privilege escalation.
- **Attack Steps**: 1. Use WinDbg to attach to crash and run !analyze -v.2. Save crash dump, stack trace, and PoC file.3. Go to Microsoft Security Response Center (MSRC): https://msrc.microsoft.com/.4. Sign in and submit a vulnerability report.5. Attach crash report, steps to reproduce, debugger logs.6. Select “Windows Kernel” as affected component.7. Await acknowledgment and tracking ID.8. Provide clarifications or verify the patch if requested.9. Coordinate embargo with Microsoft before public release.10. Check later if bounty is rewarded (if applicable).
- **Detection**: Crash logs + MSRC ID
- **Solution**: Vendor coordinates patch
- **Tags**: windows, msrc, kernel

## Responsible Disclosure to Adobe via PSIRT

- **Attack Type**: Coordinated Disclosure
- **Target**: PDF Parser
- **Vulnerability**: Memory corruption
- **MITRE**: T1204.002
- **Impact**: Arbitrary Code Execution
- **Tools**: PDF Corpus, Adobe Reader, ASAN
- **Scenario**: Bug in Adobe Reader’s file parser found via fuzzing PDF inputs.
- **Attack Steps**: 1. Use file fuzzing on Adobe Reader with malformed PDFs.2. Capture crash logs, ASAN trace, and verify issue on multiple builds.3. Visit Adobe PSIRT: https://helpx.adobe.com/security.html.4. Submit detailed vulnerability report including PoC, trace logs.5. Mark the report as sensitive.6. Wait for triage from Adobe security team.7. Help verify any hotfix or patch if provided.8. Request CVE if Adobe agrees to file it.9. Keep all details confidential until Adobe allows disclosure.10. Publish on advisory list or blog post after patch release.
- **Detection**: Adobe PSIRT Feedback
- **Solution**: CVE and patch
- **Tags**: adobe, pdf, parser

## Filing Android Vulnerability via Google Security Portal

- **Attack Type**: Vendor Disclosure
- **Target**: Mobile OS
- **Vulnerability**: Heap overflow
- **MITRE**: T1548.002
- **Impact**: App Crash / RCE
- **Tools**: libFuzzer, Android Emulator, Google Bug Portal
- **Scenario**: Fuzzing Android system services reveals crash; researcher submits to Google.
- **Attack Steps**: 1. Set up AOSP with ASAN enabled and run fuzzing on system daemons.2. Capture crashes and logs from /data/tombstones and ASAN output.3. Reproduce and validate on emulator and device.4. Visit Google’s bughunter.withgoogle.com.5. Submit report under Android category.6. Attach input file, full log, impacted devices or versions.7. Await triage and remain responsive.8. Support patch verification if requested.9. Track CVE or bounty eligibility.10. Wait for vendor-controlled embargo lifting.
- **Detection**: Android Crash Logs
- **Solution**: Google-managed timeline
- **Tags**: android, mobile, vendor

## Reproducing and Reporting WAF Bypass

- **Attack Type**: Web Exploit Disclosure
- **Target**: Web App
- **Vulnerability**: Input Validation Bypass
- **MITRE**: T1190
- **Impact**: WAF Evasion
- **Tools**: Burp Suite, Custom Payloads
- **Scenario**: A bypass for a Web Application Firewall (WAF) is discovered and responsibly disclosed.
- **Attack Steps**: 1. Fuzz inputs against the target WAF-protected application.2. Find bypass where malicious payload is not detected (e.g., SQLi or XSS).3. Record input, response, WAF logs (if available), and payload variation.4. Prepare report with payload, expected behavior vs. actual, and impact.5. Submit directly to vendor or via coordinated disclosure platform.6. Help reproduce and confirm that bypass works across deployments.7. Wait for fix or signature update.8. Do not share publicly before confirmation.9. After fix, request coordinated CVE if major.10. Document bypass method privately for internal research.
- **Detection**: WAF Log / Response Gaps
- **Solution**: Rule update
- **Tags**: waf, bug, bypass

## Coordinated Public Advisory on OSS Bug

- **Attack Type**: Public Security Advisory
- **Target**: OSS Library
- **Vulnerability**: Integer Overflow
- **MITRE**: T1592
- **Impact**: Vulnerable Library in Use
- **Tools**: Ghidra, Debuggers, GitHub
- **Scenario**: Researcher discovers critical bug in popular OSS library and releases advisory post-patch.
- **Attack Steps**: 1. Discover crash and identify root cause in OSS repo.2. Privately email the maintainer or open a restricted GitHub issue.3. Work with the maintainer to develop and test the patch.4. Suggest CVE request if impact is security-critical.5. After patch is released and deployed, write a full advisory.6. Include affected versions, reproduction steps, root cause, and patch diff.7. Post advisory on GitHub, mailing list, or blog.8. Optionally share to oss-security.9. Use CVE ID in post title for clarity.10. Add defensive coding suggestions to help the community.
- **Detection**: OSS Patch Commits
- **Solution**: OSS maintainers patch
- **Tags**: oss, patch, blog

## Coordinated Disclosure Timeline Management

- **Attack Type**: Vulnerability Disclosure
- **Target**: Software Vendor
- **Vulnerability**: Zero-Day Bug
- **MITRE**: T1595.002
- **Impact**: Vendor Coordination Delay
- **Tools**: Email, Bug Bounty Platform, Google Project Zero template
- **Scenario**: Researcher needs to responsibly manage communication and deadlines with a vendor during the coordinated disclosure of a zero-day vulnerability.
- **Attack Steps**: 1. Identify the start date of disclosure and mark it in your tracking system (e.g., spreadsheet or project management tool).2. Send initial disclosure email to vendor with all technical details, including proof-of-concept, sanitizer traces, and binary version.3. Wait for acknowledgment; if vendor does not respond within 7 days, send a polite follow-up reminder.4. Set a 90-day maximum window for coordinated disclosure, as per common industry standards.5. If the vendor asks for more time, evaluate the reason and consider extending the deadline by 30 days.6. Keep logs of all communications for accountability.7. Prepare a public blog post or CVE writeup, but hold off until the vendor publishes the fix.8. After the fix is released, notify the vendor again before public disclosure.9. Publish your analysis responsibly, highlighting collaboration and security impact.10. Submit the CVE if applicable and update public trackers like GitHub or Exploit-DB.
- **Detection**: Tracking timelines via project tools
- **Solution**: Respect coordinated disclosure timelines
- **Tags**: Coordinated Disclosure, CVE, Vendor Contact

## Submission to Google's Bug Bounty Platform

- **Attack Type**: Bug Bounty Submission
- **Target**: Browser
- **Vulnerability**: Use-After-Free
- **MITRE**: T1592.002
- **Impact**: Security Bounty Paid
- **Tools**: Chrome, Google VRP Portal, ASAN Logs
- **Scenario**: Researcher submits a zero-day bug in Chrome browser to Google's Vulnerability Reward Program (VRP).
- **Attack Steps**: 1. Ensure the bug is reproducible on the latest version of Chrome from the Canary or Dev channel.2. Collect all crash artifacts including test input, sanitizer logs, stack trace, and debugger screenshots.3. Write a clean and structured bug report in markdown format.4. Navigate to Google VRP portal and sign in with a valid Google account.5. Select the appropriate program category (e.g., Chrome Security).6. Paste the markdown report, upload the attachments, and submit.7. Wait for triage; respond quickly to requests for clarification from Google’s security team.8. If validated, the issue will be rewarded according to severity and exploitability.9. Keep correspondence professional and transparent.10. Once resolved and made public, you can publish a writeup or discuss the bug in public forums.
- **Detection**: Portal response logs and dashboard
- **Solution**: Submit reproducible, clearly documented reports
- **Tags**: Bug Bounty, Chrome, Google VRP

## CVE Assignment Through MITRE

- **Attack Type**: CVE Assignment
- **Target**: Third-party Library
- **Vulnerability**: Heap Overflow
- **MITRE**: T1587
- **Impact**: Public Advisory with CVE
- **Tools**: MITRE CVE Portal, Email, CVE JSON format
- **Scenario**: Researcher wants to obtain a CVE ID for a critical vulnerability found in a third-party file parsing library.
- **Attack Steps**: 1. Confirm the vendor is not a CNA (CVE Numbering Authority) by checking MITRE’s CNA list.2. If the vendor is not a CNA, prepare to request a CVE directly from MITRE.3. Write a summary of the vulnerability including affected product, version, and conditions for exploitability.4. Include any public links (e.g., GitHub PoC) if available or leave private until fix is ready.5. Visit MITRE’s CVE Request form and fill out required fields with concise and accurate descriptions.6. Attach or describe the advisory and point of contact details.7. Submit the request and wait for a response (usually within 1–5 business days).8. Once the CVE ID is received, reference it in all future reports and disclosure communications.9. When the patch is released, update the CVE record with full detail.10. Publish coordinated disclosure on your blog, clearly referencing the assigned CVE.
- **Detection**: CVE portal status
- **Solution**: Request and manage CVE assignments properly
- **Tags**: CVE, MITRE, Library Bug

## Submitting to CERT for Coordination

- **Attack Type**: CERT Coordination
- **Target**: Multiple Vendors
- **Vulnerability**: Type Confusion
- **MITRE**: T1595.003
- **Impact**: Multi-party Disclosure Managed
- **Tools**: CERT Coordination Portal, Email Encryption (PGP), CVSS Calculator
- **Scenario**: Researcher discovers a zero-day affecting multiple vendors and needs help from a national CERT for responsible coordination.
- **Attack Steps**: 1. Aggregate all crash and impact data across affected products/vendors.2. Use a vulnerability scoring system (e.g., CVSSv3) to assign impact ratings for each target.3. Write an executive summary of the vulnerability with reproducible PoC for each vendor.4. Encrypt the package using PGP if required by CERT (e.g., CERT/CC or CERT-In).5. Contact the national CERT with a subject like "Multi-vendor Zero-Day Coordination Request."6. Share all technical details, including your planned public disclosure timeline.7. CERT will forward the report to affected vendors and manage follow-ups.8. Maintain contact with CERT to ensure fixes are progressing.9. Upon patching by vendors, CERT may issue a public advisory referencing your findings.10. You may then proceed to publish your writeup with the coordination credit.
- **Detection**: CERT report acknowledgements
- **Solution**: Use CERTs to coordinate responsibly
- **Tags**: CERT, Coordination, Multi-Vendor

## Drafting a Public Writeup Post-Disclosure

- **Attack Type**: Public Advisory
- **Target**: General Public
- **Vulnerability**: Exploitable Crash
- **MITRE**: T1592
- **Impact**: Public Awareness & Education
- **Tools**: Markdown, Blog Engine (Ghost, Hugo, Medium), CVE Reference
- **Scenario**: After the vendor patches the vulnerability, researcher prepares a technical blog post detailing the vulnerability.
- **Attack Steps**: 1. Confirm with vendor that the fix has been released and disclosure is now permitted.2. Gather all technical artifacts: crash logs, debugger traces, binary diffs, and screenshots.3. Outline the post with clear sections: Introduction, Discovery, Root Cause Analysis, Exploitation, Vendor Response, and Lessons Learned.4. Add visual diagrams or animations to explain memory corruption or parsing flaws.5. Reference the assigned CVE, bug bounty reward (if any), and responsible disclosure timeline.6. Review your content to avoid exposing unpatched details or 0-days.7. Publish the post on your blog or Medium with appropriate tags and categories.8. Share the post via Twitter, LinkedIn, Reddit, and researcher mailing lists.9. If applicable, submit the link to vulnerability databases (e.g., Exploit-DB, CVEDetails).10. Archive a PDF copy for long-term access and include it in your portfolio.
- **Detection**: Public blog activity, discussion threads
- **Solution**: Communicate vulnerabilities clearly post-fix
- **Tags**: Writeup, Disclosure, CVE

## Submitting to Google's VRP

- **Attack Type**: Vulnerability Reporting
- **Target**: Web Browser
- **Vulnerability**: Heap buffer overflow
- **MITRE**: T1203
- **Impact**: Remote Code Execution
- **Tools**: Google VRP portal, GDB, ASAN
- **Scenario**: A security researcher wants to report a zero-day found in Chrome to Google through its Vulnerability Reward Program.
- **Attack Steps**: 1. Gather all artifacts: crash input file, ASAN logs, GDB backtrace. 2. Record steps to reproduce including OS version, browser version, compile flags if custom build. 3. Login to Google VRP portal and create a new submission. 4. Fill in the description with vulnerability type, affected components, and how it was discovered. 5. Attach PoC, debugger output, and analysis as a ZIP file. 6. Submit report and monitor for Google’s response.
- **Detection**: Execution traces + crash logs
- **Solution**: Patch via Google’s release process.
- **Tags**: bug bounty, chrome, VRP, coordinated-disclosure

## Coordinated Disclosure with CERT

- **Attack Type**: Coordinated Disclosure
- **Target**: Protocol Stack
- **Vulnerability**: Input validation flaw
- **MITRE**: T1592
- **Impact**: Data leak or RCE depending on usage
- **Tools**: CERT/CC portal, Ghidra
- **Scenario**: Reporting a complex multi-vendor protocol parsing bug via CERT/CC.
- **Attack Steps**: 1. Analyze protocol-level vulnerability affecting multiple software vendors. 2. Prepare technical write-up with call graphs, parsing logic, and affected libraries. 3. Use Ghidra to trace logic and validate bug on various implementations. 4. Contact CERT/CC and submit a report through their portal. 5. Work with them to coordinate disclosure timelines and assist vendors if needed. 6. Wait for patch release before going public.
- **Detection**: Static analysis and crash triage
- **Solution**: Inform affected vendors, wait for fixes.
- **Tags**: CERT, multi-vendor, coordination, parser-flaw

## Submitting via HackerOne Bug Bounty

- **Attack Type**: Bug Bounty Submission
- **Target**: Web Application
- **Vulnerability**: XXE Injection
- **MITRE**: T1203
- **Impact**: Data exposure, DoS
- **Tools**: HackerOne, Burp Suite, ASAN
- **Scenario**: Reporting a bug in a web app through HackerOne platform for financial reward.
- **Attack Steps**: 1. Discover vulnerability using Burp Suite and ASAN logs (e.g., XXE injection). 2. Document the bug clearly: affected endpoint, payload, observed behavior. 3. Sign in to HackerOne and navigate to the correct program. 4. Create new report with steps to reproduce, affected URLs, logs, screenshots. 5. Add impact assessment (data disclosure, DoS). 6. Submit and communicate with triage team until resolved.
- **Detection**: Manual testing + dynamic instrumentation
- **Solution**: Patch and sanitize input parsers.
- **Tags**: bugbounty, xxe, web, responsible-disclosure

## Requesting CVE ID via MITRE

- **Attack Type**: CVE Request
- **Target**: Open-source Tool
- **Vulnerability**: Use-after-free
- **MITRE**: T1203
- **Impact**: Memory corruption
- **Tools**: MITRE CVE Form, GDB, ASAN
- **Scenario**: A researcher wants to obtain a CVE for a 0-day in a lesser-known open-source tool.
- **Attack Steps**: 1. Identify bug and validate reproducibility across different systems. 2. Collect technical details, affected versions, and PoC. 3. Visit MITRE’s CVE Request form. 4. Fill in fields: vendor, product name, vulnerability type, brief summary, and supporting references. 5. Submit form and wait for CVE assignment. 6. Once assigned, publish details responsibly and update security channels.
- **Detection**: Manual test + sanitizer
- **Solution**: Maintain reproducibility; update public advisory.
- **Tags**: cve-request, mitre, open-source, vuln-class

## Submitting to Microsoft MSRC

- **Attack Type**: Vendor Reporting
- **Target**: Windows Kernel
- **Vulnerability**: Stack overflow
- **MITRE**: T1068
- **Impact**: Local Privilege Escalation
- **Tools**: WinDbg, MSRC Portal, !exploitable plugin
- **Scenario**: Reporting a Windows kernel-mode vulnerability to Microsoft Security Response Center (MSRC).
- **Attack Steps**: 1. Discover kernel crash using WinDbg and analyze with !exploitable. 2. Extract kernel stack trace, crash offset, and input trigger. 3. Create a minimal PoC input or exploit triggering the same path. 4. Sign in to the Microsoft Security Response Center (MSRC) portal. 5. Submit a detailed report with binary, PoC, and debugger logs. 6. Engage with their security team and assist with patch validation if needed.
- **Detection**: Kernel crash logs, WinDbg
- **Solution**: Microsoft releases patch after internal validation.
- **Tags**: msrc, windows, stack-overflow, responsible-report

## Simulate Exploit via Malicious PDF

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Windows Desktop
- **Vulnerability**: PDF Reader Bug
- **MITRE**: T1203 (Exploit Public-Facing App)
- **Impact**: Code execution, stealthy delivery
- **Tools**: PoC Exploit, Metasploit, Foxit Reader
- **Scenario**: Simulate a 0-day exploit chain through a maliciously crafted PDF file.
- **Attack Steps**: 1. Choose a known vulnerable version of a PDF reader such as Foxit Reader.2. Use a crash PoC or proof-of-concept exploit for a recent zero-day affecting the reader.3. Embed shellcode or payload using a crafted PDF exploit template.4. Deliver the malicious PDF via email or download link to simulate phishing delivery.5. Open the PDF in the test environment and confirm exploit success.6. Observe if the EDR or antivirus detects shellcode execution or exploit artifacts.7. Analyze system behavior using Sysmon, logs, and memory captures.
- **Detection**: EDR logs, Sysmon, behavioral alerts
- **Solution**: Patch PDF parser, block exploit signatures
- **Tags**: #pdf #zeroday #exploit #edrtest

## Drive-By Browser Exploit Simulation

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Browser (Chrome, Firefox)
- **Vulnerability**: JS Engine Bug
- **MITRE**: T1203, T1189
- **Impact**: Remote execution, EDR evasion test
- **Tools**: Chromium PoC, exploit server, Wireshark
- **Scenario**: Simulate a browser-based zero-day exploit delivered via drive-by download.
- **Attack Steps**: 1. Select a previously fuzzed browser component (e.g., V8 JavaScript engine) with a zero-day PoC.2. Set up an exploit server hosting the payload HTML and JS.3. Craft a malicious page that triggers the browser vulnerability to achieve RCE.4. Load the target browser in a Windows VM or sandbox with EDR enabled.5. Access the page to initiate the exploit chain.6. Monitor system behavior, memory usage, and process creation.7. Capture network traffic and check EDR for browser anomaly detection.8. Validate whether endpoint solution prevented or allowed the exploit.
- **Detection**: Browser logs, EDR alerts, traffic capture
- **Solution**: Harden browser, behavior-based detection
- **Tags**: #brower #driveby #zeroday #simulation

## Exploit via Malicious Media File

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Windows/Mac
- **Vulnerability**: Media Decoder Bug
- **MITRE**: T1203
- **Impact**: Code execution or player crash
- **Tools**: FFmpeg, mp4crash PoC, VLC Player
- **Scenario**: Deliver a 0-day through a specially crafted MP4 file to test AV/EDR evasion.
- **Attack Steps**: 1. Use fuzzed MP4 file with crash or exploit behavior from a zero-day in a media decoder.2. Modify metadata or video streams to include exploit trigger.3. Create a delivery vector like social media, USB drop, or email attachment.4. Play the media file on a target with VLC or default media player.5. Observe for crash, code execution, or system instability.6. Check if antivirus detects abnormal behavior.7. Use Procmon and Volatility to analyze system-level traces and memory dumps.
- **Detection**: Media logs, EDR telemetry, crash dump
- **Solution**: Patch decoder, improve anomaly detection
- **Tags**: #media #mp4 #fuzzing #redteam

## Kernel Exploit Chain Simulation

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Windows Kernel
- **Vulnerability**: IOCTL PrivEsc Bug
- **MITRE**: T1068 (Priv Esc via Exploit)
- **Impact**: SYSTEM access, detection bypass
- **Tools**: WinDbg, kernel PoC, Process Hacker
- **Scenario**: Simulate a local privilege escalation using a zero-day in kernel driver.
- **Attack Steps**: 1. Select a crash-PoC targeting a vulnerable Windows kernel driver (e.g., IOCTL-based crash).2. Modify the exploit to elevate privileges or gain SYSTEM shell.3. Deploy the binary payload on a VM with restricted user account.4. Execute and validate SYSTEM access via process list.5. Check EDR kernel mode monitoring logs or ETW events.6. Analyze any dropped artifacts, driver communication logs.7. Verify if exploit was detected or flagged.
- **Detection**: EDR, ETW, Sysmon
- **Solution**: Patch driver, restrict IOCTLs
- **Tags**: #kernel #privesc #driver #redteam

## Email Delivery Test with 0-Day Payload

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Desktop Target
- **Vulnerability**: Client-side Exploit
- **MITRE**: T1566.001
- **Impact**: User compromise via exploit
- **Tools**: Metasploit, Thunderbird, SMTP server
- **Scenario**: Send a 0-day exploit as attachment via phishing email.
- **Attack Steps**: 1. Create a crafted exploit payload (e.g., PDF, DOCX, or ZIP) containing a fuzzed 0-day.2. Set up a fake SMTP server to simulate a phishing campaign.3. Write a social engineering email with the payload attached.4. Deliver to target VM with email client like Thunderbird or Outlook.5. Open the attachment and monitor for exploit triggering.6. Use Wireshark and EDR to monitor detection response.7. Track command execution, dropped binaries, or memory injection.
- **Detection**: Email logs, AV/EDR alerts
- **Solution**: Improve phishing & payload filters
- **Tags**: #phishing #zeroday #pdfexploit #testing

## Cross-Platform Exploit Simulation

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Linux, Windows, macOS
- **Vulnerability**: Cross-platform Parser Bug
- **MITRE**: T1203, T1059
- **Impact**: Multi-platform compromise test
- **Tools**: QEMU, Docker, VirtualBox
- **Scenario**: Test the same 0-day payload on Linux, Windows, and macOS.
- **Attack Steps**: 1. Select a fuzzed vulnerability affecting a cross-platform library (e.g., libxml2, zlib).2. Compile the crash PoC or exploit payload for each OS environment.3. Deploy VM instances running Linux, Windows, and macOS.4. Deliver the exploit via file, email, or browser as appropriate.5. Monitor for different behaviors or crash conditions per OS.6. Use strace, ETW, Console logs, and memory analysis to compare outcomes.7. Evaluate Blue Team response on each OS platform.
- **Detection**: OS-specific logs, EDR on each system
- **Solution**: Patch libraries across environments
- **Tags**: #crossplatform #testing #redteam #zeroday

## Exploit Hosting via USB Drop

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Physical Workstation
- **Vulnerability**: USB Exploit Vector
- **MITRE**: T1091 (Replication via Removable Media)
- **Impact**: Initial access via physical means
- **Tools**: Rubber Ducky, crafted exploit, USB drive
- **Scenario**: Simulate physical drop attack with zero-day exploit file on USB.
- **Attack Steps**: 1. Use a zero-day payload that runs from a removable device (e.g., autorun media file or crafted script).2. Copy to USB along with decoy documents.3. Drop USB at target location or simulate plug-in on test environment.4. Upon user interaction, verify if payload is executed.5. Track system changes, user privileges gained, and alerts triggered.6. Monitor EDR for execution from USB or suspicious behavior.7. Analyze logs, file access events, and system telemetry.
- **Detection**: USB logs, EDR alerts
- **Solution**: Disable autorun, monitor USB activity
- **Tags**: #usb #autorun #redteam #zeroday

## DLL Side-Loading Using Exploit

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Desktop System
- **Vulnerability**: DLL Side-Loading + 0-day
- **MITRE**: T1574.002
- **Impact**: Trusted app hijack via 0-day
- **Tools**: CFF Explorer, Procmon, Signed App
- **Scenario**: Simulate side-loading of a 0-day DLL to gain execution within trusted apps.
- **Attack Steps**: 1. Find a signed app vulnerable to DLL side-loading (e.g., search paths unverified).2. Compile a 0-day exploit payload into a DLL.3. Rename and place DLL next to the executable.4. Run the trusted app and confirm execution of the malicious DLL.5. Monitor behavior using Procmon and EDR.6. Capture telemetry to validate if Blue Team detects side-loading.7. Check registry, file writes, and parent-child process tree.
- **Detection**: EDR behavior logs, process tree
- **Solution**: Harden loading paths, app whitelisting
- **Tags**: #sideload #dll #redteam #zeroday

## Exploit Chain with Sandbox Escape

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Windows VM
- **Vulnerability**: Browser + Sandbox Bypass
- **MITRE**: T1211, T1068
- **Impact**: Full compromise bypassing sandbox
- **Tools**: Exploit Kit, Chrome sandbox PoC, VMs
- **Scenario**: Simulate chaining a browser exploit with sandbox escape for full compromise.
- **Attack Steps**: 1. Use a zero-day browser RCE as initial vector.2. Chain with a separate sandbox escape exploit (e.g., privilege escalation vulnerability).3. Deploy in a sandboxed environment (e.g., Chrome or Edge on Windows).4. Navigate to exploit page or open payload file.5. Observe system-level execution beyond sandbox.6. Use Procmon, Volatility, and event logs to detect escape evidence.7. Confirm if EDR or sandboxing tools detect and stop the chain.
- **Detection**: Behavioral EDR, event log, memory
- **Solution**: Strengthen sandboxing, patch chaining paths
- **Tags**: #sandboxescape #zeroday #redteam

## Application Protocol Exploit Simulation

- **Attack Type**: Red Team Simulation Using Zero-Day
- **Target**: Linux/Unix Server
- **Vulnerability**: Protocol Handler Bug
- **MITRE**: T1203, T1040
- **Impact**: Server DoS or RCE via network
- **Tools**: Custom PoC, Wireshark, EDR
- **Scenario**: Simulate exploiting a 0-day in application protocol handling (e.g., FTP, SMTP).
- **Attack Steps**: 1. Select a server with known protocol stack (e.g., vsftpd, postfix).2. Use fuzzed input or PoC that crashes on malformed input (buffer overflow, format string).3. Craft malicious network request using nc or custom script.4. Send to the server and monitor for crash or unexpected behavior.5. Observe network logs, packet traces, and server memory.6. Check if IDS/IPS or SIEM flags the anomaly.7. Determine detection gaps and propose improvement.
- **Detection**: SIEM, IDS/IPS, logs
- **Solution**: Harden protocol parsing, add rules
- **Tags**: #network #protocol #fuzzing #zeroday

