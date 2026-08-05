# Automotive / Cyber-Physical Systems → Infotainment System Hacking Attacks

## Exploiting MP4 Parsing Bug in Car Media Player

- **Attack Type**: Media File Exploit
- **Target**: Car Infotainment System
- **Vulnerability**: MP4 Media Parsing
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: System crash, potential remote code execution
- **Tools**: Custom MP4 file generator, CrashMonitor, ICSim
- **Scenario**: A specially crafted MP4 file is loaded into the infotainment system to exploit a parsing vulnerability and crash the media service or gain control.
- **Attack Steps**: 1. Identify a vulnerability in the MP4 file parsing module used by the car's infotainment unit (e.g., via open-source decoder or CVE info).2. Create a malformed MP4 file using a fuzzing or manual editing tool that targets vulnerable structures like ‘moov’ or ‘mdat’.3. Load this file on a USB and insert it into the vehicle's infotainment USB port.4. Play the file using the media player to trigger the bug.5. Observe for crash, screen freeze, or code execution.6. Use CrashMonitor or debug console to confirm system compromise.
- **Detection**: System logs, crash dumps, USB access logs
- **Solution**: Patch media parser, disable auto-play for untrusted USB media
- **Tags**: mp4, infotainment, parser, media exploit

## Malformed JPEG Crashes Infotainment Renderer

- **Attack Type**: Media File Exploit
- **Target**: Car Display UI
- **Vulnerability**: JPEG Parsing Overflow
- **MITRE**: T1203
- **Impact**: DoS or exploit entrypoint
- **Tools**: Custom JPEG payload, AFL++, GDB
- **Scenario**: A malformed JPEG image is used to trigger a buffer overflow in the infotainment system's image viewer, causing instability or allowing exploit payload.
- **Attack Steps**: 1. Study the JPEG decoder (e.g., libjpeg or car-specific library) for known parsing bugs.2. Use AFL++ to fuzz valid JPEGs and generate crashing inputs.3. Save the crashing file on an SD card or USB stick.4. Display the image via infotainment’s photo viewer.5. Observe crash or unintended behavior.6. If debugger access is available, attach and triage exploitability.
- **Detection**: Event logs, visual glitches, debugger output
- **Solution**: Update parsing libraries, validate input formats
- **Tags**: jpeg, fuzzing, overflow, infotainment

## Audio Codec Exploit via FLAC File

- **Attack Type**: Media File Exploit
- **Target**: Media Engine
- **Vulnerability**: Audio File Parsing Bug
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Audio system crash, potential shell access
- **Tools**: Custom FLAC mutator, Ghidra, AFL
- **Scenario**: Exploit a memory corruption vulnerability in the FLAC audio decoder by playing a malicious audio file.
- **Attack Steps**: 1. Analyze the FLAC decoder binary from the car's firmware using Ghidra or reverse engineering.2. Craft a FLAC file that violates spec (e.g., overly long metadata block).3. Inject shellcode or crash payload into the file.4. Load via USB or Bluetooth file transfer.5. When audio is played, monitor memory for abnormal behavior.6. Confirm control using debugging output or shell access.
- **Detection**: Decoder debug logs, memory dump
- **Solution**: Secure FLAC decoder, input validation
- **Tags**: audio exploit, flac, infotainment

## Corrupt Album Art Image Triggers Heap Overflow

- **Attack Type**: Media File Exploit
- **Target**: Car Music Player
- **Vulnerability**: Heap Overflow via Metadata
- **MITRE**: T1203
- **Impact**: Application instability, crash loop
- **Tools**: MP3 container editor, HexFiend, AFL
- **Scenario**: An embedded corrupt image (album art) within an MP3 container triggers a heap overflow when read by the infotainment system.
- **Attack Steps**: 1. Prepare a valid MP3 file using a music editor.2. Embed a malformed PNG or JPEG album art into its metadata.3. Use a hex editor to inject values causing heap corruption.4. Play the MP3 in the vehicle's system.5. Observe abnormal behavior, audio glitches, or app crash.6. Analyze logs for memory corruption evidence.
- **Detection**: Crash logs, memory dump, playback failures
- **Solution**: Sanitize embedded image parsing
- **Tags**: metadata, heap overflow, infotainment

## Subtitles Injection via Malformed SRT File

- **Attack Type**: Media File Exploit
- **Target**: Infotainment Video Player
- **Vulnerability**: Subtitle Parsing Error
- **MITRE**: T1203
- **Impact**: Subtitle crash or memory error
- **Tools**: Subtitle injector, VLC for testbed
- **Scenario**: A malicious SRT subtitle file embedded with script triggers parsing error in the infotainment’s media player.
- **Attack Steps**: 1. Identify media players in car that support subtitles.2. Create a malicious SRT file with malformed index, overlapping timestamps, or invalid tags.3. Add it alongside a video file and copy to USB.4. Play video in the car and enable subtitles.5. Trigger parser error or crash.6. Record if playback fails or control is hijacked.
- **Detection**: Playback logs, crash reports
- **Solution**: Remove SRT support or validate syntax strictly
- **Tags**: subtitles, srt, media, infotainment

## Video Playback Overflow via AVI Container

- **Attack Type**: Media File Exploit
- **Target**: Car Media Player
- **Vulnerability**: AVI Format Misuse
- **MITRE**: T1499
- **Impact**: Temporary denial of video playback
- **Tools**: AVI editor, VideoFuzz, Valgrind
- **Scenario**: Overflow in parsing the index table of AVI video containers crashes the video player.
- **Attack Steps**: 1. Use an AVI editor to tamper with the index chunk size and number of streams.2. Create an inconsistent structure (e.g., mismatch between declared and actual size).3. Play the file in the car’s infotainment system.4. Trigger crash when it tries to seek frames.5. Monitor for segmentation fault or UI freeze.6. Capture error using onboard diagnostics.
- **Detection**: Video app logs, memory exception
- **Solution**: Harden parser, enforce max size/stream checks
- **Tags**: avi exploit, media crash

## Malicious PNG Triggers Code Path via Zlib Chunk

- **Attack Type**: Media File Exploit
- **Target**: Infotainment UI Thread
- **Vulnerability**: zlib parsing bug
- **MITRE**: T1203
- **Impact**: UI rendering crash
- **Tools**: PNGStructEditor, zlib-modifier
- **Scenario**: Malformed PNG crafted with abnormal zlib chunk crashes infotainment's background renderer.
- **Attack Steps**: 1. Study car’s PNG parsing flow and zlib chunk handling.2. Create a PNG with invalid zlib deflate block.3. Save on a USB stick.4. Set the image as background or album art.5. Wait for renderer to crash or go into loop.6. Validate using diagnostic log or reboot behavior.
- **Detection**: System renderer logs
- **Solution**: Patch libpng/zlib versions
- **Tags**: png, zlib, crash

## Embedded TIFF in Playlist Crashes App

- **Attack Type**: Media File Exploit
- **Target**: Playlist Engine
- **Vulnerability**: Image Decoder Weakness
- **MITRE**: T1203
- **Impact**: Application DoS
- **Tools**: M3U playlist editor, ImageMagick
- **Scenario**: A TIFF file referenced in a corrupted playlist crashes the infotainment when resolving linked files.
- **Attack Steps**: 1. Create an M3U playlist with broken entries and one link to a malformed TIFF.2. Include unexpected tags or long path references.3. Load on USB or SD card.4. Open playlist from infotainment.5. Crash occurs when resolving TIFF header.6. Observe for repeated reboot or UI lag.
- **Detection**: M3U debug logs, image decoder errors
- **Solution**: Restrict playlist file formats
- **Tags**: tiff exploit, playlist, infotainment

## Auto-Thumbnail Crash via Corrupt WebP

- **Attack Type**: Media File Exploit
- **Target**: File Explorer / Preview Engine
- **Vulnerability**: WebP decoder vulnerability
- **MITRE**: T1499
- **Impact**: File explorer crash
- **Tools**: WebP-Fuzzer, File Explorer
- **Scenario**: Corrupt WebP image causes auto-thumbnail service to crash on file browsing in infotainment.
- **Attack Steps**: 1. Generate a WebP with broken VP8 frame headers.2. Place on USB root directory.3. Use infotainment file browser to list images.4. Auto-thumbnailer tries to parse file and crashes.5. System may freeze or reboot.6. Capture crash dump or thumbnailer logs.
- **Detection**: Auto-thumbnail logs
- **Solution**: Sanitize image decoding, cap recursion
- **Tags**: webp, infotainment, file crash

## Corrupted MKV File Causes Infinite Loop

- **Attack Type**: Media File Exploit
- **Target**: Video Processing Engine
- **Vulnerability**: MKV metadata bug
- **MITRE**: T1499
- **Impact**: Complete UI hang, media unusable
- **Tools**: mkvmerge, MKVEditor, ICSim
- **Scenario**: Malformed MKV container leads to infinite loop in media processing thread.
- **Attack Steps**: 1. Create an MKV with invalid timecodes and infinite cluster tags.2. Place file on USB stick.3. Play in car’s video player.4. App enters infinite loop trying to parse metadata.5. System hangs until hard reboot.6. Observe looping via logs or response delay.
- **Detection**: App watchdog, response latency
- **Solution**: Enforce file format spec adherence
- **Tags**: mkv, infinite loop, infotainment

## Malicious APK Over CarPlay

- **Attack Type**: Application Exploit
- **Target**: Infotainment System
- **Vulnerability**: Weak app permission enforcement
- **MITRE**: T1476 - Deliver Malicious App via USB
- **Impact**: Remote code execution within vehicle OS
- **Tools**: Android Studio, Frida, USB Debugging, Custom CarPlay emulator
- **Scenario**: Attacker abuses the car's CarPlay integration to deploy a malicious Android APK when the phone is tethered
- **Attack Steps**: 1. Create a malicious APK file with embedded reverse shell payload using msfvenom.2. Tether an Android device to the vehicle's infotainment unit through USB.3. Exploit weak CarPlay or Android Auto permission policies to deliver the APK silently.4. Use Frida or similar tools to hook into CarPlay activity and allow the APK to execute in the background.5. Establish a reverse connection to the attacker’s listener, gaining control over infotainment functionalities and potentially GPS, media, or mic access.
- **Detection**: Monitor app installations, USB activity
- **Solution**: Enforce app signing and user consent for installations
- **Tags**: infotainment, android auto, usb, carplay, reverse shell

## Malicious Subtitles in Media Playback

- **Attack Type**: Media Exploit
- **Target**: Infotainment System
- **Vulnerability**: Subtitle parsing flaws
- **MITRE**: T1203 - Exploitation for Client Execution
- **Impact**: Infotainment compromise, potential lateral movement
- **Tools**: VLC modified builds, Subtitle Edit, CANBus Replay Toolkit
- **Scenario**: Infotainment system plays media from USB with a booby-trapped subtitle file that causes RCE
- **Attack Steps**: 1. Prepare a malicious .srt subtitle file crafted to exploit parsing flaws in the infotainment’s media subsystem.2. Copy this subtitle file along with a movie to a USB stick.3. Plug the USB into the vehicle’s infotainment port.4. On playback, the system parses the .srt, which triggers a buffer overflow.5. Payload gives attacker control of infotainment UI or background services.
- **Detection**: Monitor USB file types and parsing logs
- **Solution**: Patch infotainment media parsers, disable unknown subtitle support
- **Tags**: media exploit, subtitle, usb attack, rce

## USB HID Spoof to Control Infotainment

- **Attack Type**: USB Exploitation
- **Target**: Infotainment System
- **Vulnerability**: Unrestricted HID input acceptance
- **MITRE**: T1204 - User Execution
- **Impact**: Full infotainment manipulation
- **Tools**: Rubber Ducky, Digispark, Arduino Leonardo
- **Scenario**: Attacker plugs in a USB device that mimics a Human Interface Device to issue commands
- **Attack Steps**: 1. Program a USB Rubber Ducky or Digispark to emulate a keyboard.2. Script sequences that navigate the infotainment system to enable developer mode or Wi-Fi debugging.3. Plug the device into the vehicle's USB port.4. The spoofed HID injects keystrokes rapidly and invisibly.5. Gains access to settings, connectivity options, or starts background scripts for data exfiltration.
- **Detection**: Monitor USB HID device types and activity
- **Solution**: Restrict USB HID types, enforce whitelisting
- **Tags**: usb spoofing, hid attack, rubber ducky, infotainment

## Exploiting Wi-Fi Auto-Connect in Infotainment

- **Attack Type**: Wireless Exploit
- **Target**: Infotainment System
- **Vulnerability**: Unsecured Wi-Fi auto-connect feature
- **MITRE**: T1557 - Adversary-in-the-Middle
- **Impact**: Remote firmware or browser compromise
- **Tools**: Bettercap, WiFi Pineapple, Kali Linux
- **Scenario**: Vehicle connects to rogue Wi-Fi hotspot automatically, leading to MITM attack
- **Attack Steps**: 1. Set up a rogue Wi-Fi access point that mimics previously connected SSIDs.2. Park near a targeted vehicle; its infotainment auto-connects to known SSID.3. Use Bettercap to perform ARP spoofing and launch DNS poisoning.4. Redirect infotainment browser or apps to malicious firmware or update payloads.5. Gain access to infotainment root shell or user interface manipulation.
- **Detection**: Monitor network SSIDs and DNS requests
- **Solution**: Disable auto-connect, enforce certificate pinning
- **Tags**: wifi spoofing, MITM, rogue AP, infotainment

## Attack via Malformed JPEG Album Art

- **Attack Type**: Media Parsing Exploit
- **Target**: Infotainment System
- **Vulnerability**: JPEG parser flaw
- **MITRE**: T1203 - Exploitation of Client Applications
- **Impact**: System crash or remote access
- **Tools**: AFL++, GDB, JPEGdump, CANlib
- **Scenario**: Malicious JPEG file used as album art causes memory corruption in image parser
- **Attack Steps**: 1. Use AFL++ to fuzz the JPEG parser of the infotainment’s album-art display engine.2. Discover crash case with specific JPEG markers.3. Embed the malformed JPEG as album art inside an MP3 using TagLib or exiftool.4. Load the MP3 on a USB stick and insert into the car’s media system.5. On parsing the JPEG, the system crashes or allows remote payload execution.
- **Detection**: Monitor crash logs and media parsing behavior
- **Solution**: Patch JPEG parser, limit embedded metadata handling
- **Tags**: jpeg exploit, media fuzzing, album art, memory corruption

## Custom App OTA Abuse

- **Attack Type**: Application Exploit
- **Target**: Infotainment System
- **Vulnerability**: Poor OTA validation
- **MITRE**: T1071 - Application Layer Protocol
- **Impact**: Persistent access via custom app
- **Tools**: Burp Suite, APKTool, OTA Debugging Tools
- **Scenario**: Infotainment accepts over-the-air (OTA) updates for apps, attacker uploads modified version
- **Attack Steps**: 1. Reverse-engineer a legitimate infotainment app using APKTool.2. Insert a reverse shell or unauthorized telemetry feature.3. Host the app update on a spoofed OTA server.4. Trick the vehicle into connecting to the spoofed server or exploit weak validation checks.5. App installs silently, giving control to the attacker or leaking data.
- **Detection**: Monitor OTA endpoints, app hashes
- **Solution**: Enforce HTTPS + app signature checks
- **Tags**: OTA abuse, app modification, reverse engineering

## Voice Assistant Command Injection

- **Attack Type**: Audio-Based Exploit
- **Target**: Infotainment System
- **Vulnerability**: Unauthenticated voice commands
- **MITRE**: T1204 - User Execution
- **Impact**: Unauthorized action execution
- **Tools**: Text-to-Speech Tools, Ultrasonic Attack Toolkit
- **Scenario**: Use malicious voice commands to inject navigation or settings commands into infotainment
- **Attack Steps**: 1. Craft a voice command audio payload using TTS or ultrasonic injection tools.2. Transmit the command near a parked or idling vehicle.3. Infotainment system accepts command like “Call attacker” or “Open Wi-Fi settings”.4. May trigger further payload delivery or expose services.5. Exploit works even if user doesn’t notice due to stealthy injection.
- **Detection**: Analyze microphone input and command logs
- **Solution**: Voice model authentication or disable voice input when idle
- **Tags**: voice command, ultrasonic, infotainment, injection

## Exploiting Update Over Bluetooth

- **Attack Type**: Wireless Exploit
- **Target**: Infotainment System
- **Vulnerability**: Insecure Bluetooth update mechanism
- **MITRE**: T1496 - Resource Hijacking
- **Impact**: Full system compromise
- **Tools**: Bluetooth Stack Tools, BlueZ, BT Sniffer
- **Scenario**: Infotainment system receives updates over Bluetooth; attacker hijacks update
- **Attack Steps**: 1. Capture the Bluetooth communication using a sniffer during infotainment OTA update.2. Replay or tamper with the update using BlueZ utilities.3. Inject malicious firmware or backdoor payload.4. Infotainment accepts update due to lack of proper signing or validation.5. Leads to complete system compromise.
- **Detection**: Log Bluetooth update sessions, validate update size
- **Solution**: Enforce digital signature on all BT updates
- **Tags**: bluetooth, ota, firmware injection, infotainment

## Info Theft via Infotainment Logs

- **Attack Type**: Information Disclosure
- **Target**: Infotainment System
- **Vulnerability**: Lack of log sanitization
- **MITRE**: T1552 - Unsecured Credentials
- **Impact**: User privacy breach
- **Tools**: Log Parser, USB Forensics Toolkits
- **Scenario**: Logs stored by infotainment leak user data when extracted via USB
- **Attack Steps**: 1. Gain brief access to the car and insert USB drive with script to extract logs.2. Parse the infotainment logs for contact info, call logs, GPS coordinates, or Wi-Fi credentials.3. Exfiltrate data silently and leave no trace.4. Attacker analyzes stolen logs later to profile target or craft further attacks.
- **Detection**: Monitor log access events
- **Solution**: Encrypt and rotate logs, block external extraction
- **Tags**: infotainment logs, info theft, usb extraction

## Browser Exploit in Infotainment Webview

- **Attack Type**: Web Exploit
- **Target**: Infotainment System
- **Vulnerability**: Outdated WebView components
- **MITRE**: T1189 - Drive-by Compromise
- **Impact**: Code execution via captive portal
- **Tools**: Browser Exploit Framework (BeEF), DNSMasq, WiFi Pineapple
- **Scenario**: Outdated browser/WebView in infotainment exploited via captive portal
- **Attack Steps**: 1. Set up Wi-Fi AP with captive portal using DNSMasq.2. Vehicle connects and loads portal page in embedded WebView browser.3. Use BeEF to exploit WebView XSS or RCE vulnerability.4. Gain access to browser context, cookies, or device sensors.5. Possibly pivot into vehicle systems if integrations exist.
- **Detection**: Monitor captive portal access logs
- **Solution**: Patch browser, disable portal auto-load
- **Tags**: webview, browser exploit, captive portal, infotainment

