# Physical / Hardware Attacks Attacks

## Unauthorized USB Malware Injection via Reception PC

- **Attack Type**: Physical Access Exploit
- **Target**: Desktop Computer (Reception)
- **Vulnerability**: Lack of USB port control, unattended workstation
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Backdoor access, data leakage
- **Tools**: USB Rubber Ducky, Malware Payload
- **Scenario**: Attacker pretends to be a job applicant and inserts a malware-laced USB drive into the receptionist’s unlocked computer.
- **Attack Steps**: Step 1: Dress formally and enter the company as if attending an interview.Step 2: Wait until the receptionist is distracted or steps away.Step 3: Plug in the USB Rubber Ducky which executes hidden malware scripts automatically.Step 4: The script creates a backdoor or logs keystrokes silently.Step 5: Remove USB and leave the building as if nothing happened.
- **Detection**: USB scanning tools, unusual process monitoring
- **Solution**: Block USB devices, implement endpoint protection, staff awareness
- **Tags**: USB, Rubber Ducky, Social Engineering, Physical Entry

## BIOS Password Reset via CMOS Jumper

- **Attack Type**: Hardware Tampering
- **Target**: Workstation or Server
- **Vulnerability**: Weak physical security, unmonitored access
- **MITRE**: T1110.004 - Password Cracking: BIOS
- **Impact**: Full control of machine boot options
- **Tools**: Screwdriver, Technical manual
- **Scenario**: Attacker gains physical access to server room and resets BIOS password by shorting the CMOS jumper on the motherboard.
- **Attack Steps**: Step 1: Wear an official-looking ID and ask to inspect the server room citing a fake maintenance reason.Step 2: Once inside, power down the PC or server.Step 3: Open the case using a screwdriver.Step 4: Locate the CMOS jumper near the motherboard battery.Step 5: Move the jumper to the reset position and wait 10 seconds.Step 6: Move jumper back, close case, power on — BIOS password is reset.Step 7: Attacker can now enter BIOS and disable protections or boot from USB.
- **Detection**: BIOS logs, internal inspection
- **Solution**: Lock server rooms, BIOS password + chassis locks
- **Tags**: BIOS, CMOS, Physical Tampering

## Booting Live OS to Bypass OS Login

- **Attack Type**: Unauthorized Boot Access
- **Target**: Windows PC
- **Vulnerability**: BIOS boot order unlocked, no disk encryption
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Credential theft, file access
- **Tools**: Kali Linux Live USB, Laptop
- **Scenario**: Attacker boots into Linux Live OS via USB on unattended machine to extract files or change passwords.
- **Attack Steps**: Step 1: Insert bootable Kali Linux USB into the target PC.Step 2: Restart the machine and enter BIOS/boot menu (by pressing F2/F10/Delete).Step 3: Select USB as boot device.Step 4: Once Kali boots, access local drive to copy sensitive files.Step 5: Optionally, use chntpw to reset Windows user passwords.Step 6: Remove USB and reboot to cover traces.
- **Detection**: BIOS logs, USB history
- **Solution**: Set BIOS password, disable boot from USB, use BitLocker
- **Tags**: USB, Live Boot, Linux

## HID Spoofing with Malicious Keyboard

- **Attack Type**: HID Injection
- **Target**: Office Desktop
- **Vulnerability**: Poor hardware inventory checks
- **MITRE**: T1056.001 - Input Capture: Keylogging
- **Impact**: Credential compromise, data theft
- **Tools**: MalDuino, Lookalike Keyboard
- **Scenario**: Attacker replaces keyboard with one that looks identical but has a hidden chip to record or transmit keystrokes.
- **Attack Steps**: Step 1: Buy a keyboard with hidden keylogger chip (MalDuino).Step 2: Tailgate or distract a user and swap their keyboard silently.Step 3: The malicious keyboard starts recording all keystrokes.Step 4: Data is stored on the chip or sent wirelessly.Step 5: Retrieve the keyboard later or collect data remotely.
- **Detection**: Sudden keyboard changes, radio scans
- **Solution**: Asset tagging, frequent physical audits
- **Tags**: HID, Hardware Keylogger, Swap Attack

## Internal Threat – Planting Raspberry Pi for Network Sniffing

- **Attack Type**: Device Implantation
- **Target**: Corporate LAN
- **Vulnerability**: Open network jacks, no NAC controls
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Long-term data exfiltration
- **Tools**: Raspberry Pi, Ethernet Cable, Power Bank
- **Scenario**: Insider or fake visitor plants a Raspberry Pi on a live network port to sniff traffic or create a backdoor.
- **Attack Steps**: Step 1: Enter office as delivery agent or temp intern.Step 2: Find an unused Ethernet port (e.g., under desk, meeting room).Step 3: Connect Raspberry Pi loaded with sniffing tools to port.Step 4: Power it via hidden power bank or wall adapter.Step 5: Pi captures packets or connects to remote server for reverse shell.Step 6: Exit building unnoticed; access data remotely.
- **Detection**: Port scan, traffic monitoring tools
- **Solution**: Use NAC (Network Access Control), block unused ports
- **Tags**: Network, Raspberry Pi, IoT

## Power Strip-Based Hardware Keylogger

- **Attack Type**: Concealed Logging
- **Target**: Desktop Area
- **Vulnerability**: User trust, unchecked devices
- **MITRE**: T1056 - Input Capture
- **Impact**: Continuous password theft
- **Tools**: Modified Power Strip with Logging Chip
- **Scenario**: Attacker hides a keylogger device inside a modified power strip at workstation.
- **Attack Steps**: Step 1: Bring a power strip with built-in keylogging chip.Step 2: Replace user’s existing power strip or offer it as an “upgrade”.Step 3: User connects devices normally — logger starts recording keyboard inputs.Step 4: Periodically retrieve or connect wirelessly to download logs.Step 5: Leave no visible signs of tampering.
- **Detection**: Physical inspection of devices
- **Solution**: Only allow IT-provided accessories
- **Tags**: Power Strip, Hardware Hacking

## BIOS Boot Order Tampering

- **Attack Type**: Boot Manipulation
- **Target**: Any Bootable PC
- **Vulnerability**: Unlocked BIOS settings
- **MITRE**: T1542.003 - Boot or Logon Autostart
- **Impact**: Bypass OS login, install rootkits
- **Tools**: None (BIOS Access)
- **Scenario**: Attacker changes BIOS boot order to load external OS or malware.
- **Attack Steps**: Step 1: Gain physical access to the machine.Step 2: Reboot and press BIOS key (F2/DEL) on startup.Step 3: Change boot order to prioritize USB/CD.Step 4: Insert bootable malware or live OS.Step 5: Reboot — external system loads first, bypassing OS login.Step 6: Remove media and revert boot order to avoid detection.
- **Detection**: BIOS audit logs (if enabled)
- **Solution**: BIOS passwords, disable external boot
- **Tags**: BIOS, Bypass, Boot Order

## Laptop Theft from Unlocked Desk

- **Attack Type**: Device Theft
- **Target**: Laptop
- **Vulnerability**: No lock cable, no full-disk encryption
- **MITRE**: T1025 - Data from Removable Media
- **Impact**: Data loss, breach of proprietary info
- **Tools**: None
- **Scenario**: Attacker walks away with unlocked or sleeping laptop left on unattended desk.
- **Attack Steps**: Step 1: Monitor a corporate or co-working space for unattended devices.Step 2: Walk in during break hours or as visitor.Step 3: Identify an unlocked laptop with no surveillance nearby.Step 4: Grab the laptop, place in bag, and exit casually.Step 5: Later, access files or reset passwords using bootable tools.
- **Detection**: CCTV review, device inventory
- **Solution**: Use lock cables, auto-lock screens, disk encryption
- **Tags**: Theft, Lost Device

## RFID Cloning of Access Badge

- **Attack Type**: RFID Spoofing
- **Target**: Access Control System
- **Vulnerability**: No RFID encryption, badge not shielded
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Physical access, tampering opportunity
- **Tools**: Proxmark3, RFID Cloner
- **Scenario**: Attacker clones an employee's RFID badge to gain unauthorized entry.
- **Attack Steps**: Step 1: Stand close to victim in cafeteria or elevator.Step 2: Activate Proxmark3 — it silently captures RFID signal.Step 3: Save the badge data into memory.Step 4: Use blank RFID card and clone the captured data.Step 5: Use the cloned badge to enter restricted area undetected.
- **Detection**: RFID scan logs (if used), surveillance
- **Solution**: RFID shielding pouches, badge audits
- **Tags**: RFID, Access Card, Cloning

## Tailgating Through Secure Door

- **Attack Type**: Social Engineering Entry
- **Target**: Physical Premises
- **Vulnerability**: No anti-tailgating measures
- **MITRE**: T1078 - Valid Accounts (Physical Entry)
- **Impact**: Access to internal network or hardware
- **Tools**: None
- **Scenario**: Attacker enters secured building by following behind a legitimate employee.
- **Attack Steps**: Step 1: Dress professionally and hold papers or ID badge.Step 2: Wait outside secured entrance.Step 3: When employee opens the door, walk in right behind them while chatting or pretending to be in a rush.Step 4: Access restricted floors or offices.Step 5: Perform internal reconnaissance or plug in malicious devices.
- **Detection**: Security camera, employee reports
- **Solution**: Use turnstiles, train employees to challenge tailgaters
- **Tags**: Tailgating, Social Engineering

## Screen Peeking for Passwords

- **Attack Type**: Shoulder Surfing
- **Target**: Laptop or Desktop
- **Vulnerability**: No screen privacy filters
- **MITRE**: T1056.002 - Input Capture (Visual)
- **Impact**: Credential compromise
- **Tools**: None (Good Eyesight)
- **Scenario**: Attacker watches user entering login credentials over shoulder or from side.
- **Attack Steps**: Step 1: Sit or stand near user during login (e.g., café, coworking space).Step 2: Observe keystrokes and screen silently.Step 3: Memorize or quickly note down username/password.Step 4: Use credentials later to log in remotely.Step 5: Cleanly exit without raising suspicion.
- **Detection**: Shoulder surfing prevention, screen filters
- **Solution**: Use privacy screens, awareness training
- **Tags**: Shoulder Surf, Visual Hacking

## Surveillance Camera Blind Spot Plug-In

- **Attack Type**: Covert Device Installation
- **Target**: Office Network
- **Vulnerability**: Blind spots, open network jacks
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Persistent internal foothold
- **Tools**: Raspberry Pi Zero, Ethernet Cable, Power Adapter
- **Scenario**: Attacker installs a small device in surveillance camera blind spot to attack internal systems.
- **Attack Steps**: Step 1: Study CCTV coverage to find blind spots.Step 2: Carry a small device like Raspberry Pi Zero in bag.Step 3: Go to unmonitored area (under desk, behind cabinet).Step 4: Plug into open network port and power source.Step 5: The device runs persistent scripts or opens a reverse shell.Step 6: Control it remotely from outside.
- **Detection**: Periodic network scans, unusual traffic alerts
- **Solution**: Cover all blind spots, restrict unused jacks
- **Tags**: Raspberry Pi, Covert Device

## BIOS Password Reset via Battery Removal

- **Attack Type**: BIOS Bypass
- **Target**: Workstation or Server
- **Vulnerability**: Unsecured hardware, no BIOS security chip
- **MITRE**: T1110.004 - Password Cracking: BIOS
- **Impact**: Full access to BIOS, bypass of boot security
- **Tools**: Screwdriver, Antistatic Gloves
- **Scenario**: Attacker removes the CMOS battery to reset BIOS password and gain boot access.
- **Attack Steps**: Step 1: Power off the computer and unplug it.Step 2: Open the case using a screwdriver.Step 3: Locate the round silver CMOS battery on the motherboard.Step 4: Carefully remove the battery and wait for 5–10 minutes.Step 5: Reinsert the battery, close the case, and power on the device.Step 6: BIOS password is cleared; attacker can now access BIOS freely.
- **Detection**: BIOS logs, physical audit
- **Solution**: Use tamper-proof BIOS chips, case intrusion detection
- **Tags**: BIOS, Battery, Hardware Reset

## Security Camera Redirection with Laser Pointer

- **Attack Type**: Surveillance Evasion
- **Target**: CCTV
- **Vulnerability**: Weak surveillance controls, no anti-glare shield
- **MITRE**: T1562.007 - Indicator Blocking: Disable or Modify Tools
- **Impact**: Camera blindness, undetected access
- **Tools**: Laser Pointer (1mW–5mW)
- **Scenario**: Attacker points a laser to blind or redirect security cameras and perform covert actions.
- **Attack Steps**: Step 1: Scout the building and identify camera positions.Step 2: Approach under the blind spot or far enough.Step 3: Aim laser pointer at camera lens to temporarily blind it.Step 4: While camera is blinded, enter the area and plant/modify devices.Step 5: Leave the scene quickly before laser use is detected.
- **Detection**: Visual review, AI-based motion detection
- **Solution**: Anti-laser camera shields, intelligent IR filters
- **Tags**: CCTV, Laser, Covert Access

## Fake Fire Drill Distraction for Device Theft

- **Attack Type**: Social Engineering Entry
- **Target**: Office Premises
- **Vulnerability**: No device lockdown during evacuation
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Theft of unguarded hardware and data
- **Tools**: Lighter, Smoke Bomb (non-lethal), Knowledge of fire panel
- **Scenario**: Attacker triggers fake fire alarm to clear area and steal unattended assets.
- **Attack Steps**: Step 1: Plan visit during busy hours.Step 2: Set off smoke bomb in bathroom or trigger manual fire alarm.Step 3: During evacuation, enter offices disguised as safety official.Step 4: Locate high-value devices (laptops, drives) left behind.Step 5: Exit the building before staff returns.
- **Detection**: Evacuation logs, missing asset tracking
- **Solution**: Lock devices during drills, secure backup locations
- **Tags**: Fire Drill, Social Engineering

## Booting Encrypted System via Cold Boot Attack

- **Attack Type**: Cold Boot Exploit
- **Target**: Laptop/PC
- **Vulnerability**: No RAM clearing on shutdown
- **MITRE**: T1003.005 - OS Credential Dumping: Security Account Manager
- **Impact**: BitLocker bypass, key theft
- **Tools**: Cold Boot Toolkit, Freezer Spray, USB Tools
- **Scenario**: Attacker restarts encrypted machine and accesses RAM to extract encryption keys.
- **Attack Steps**: Step 1: Gain access to a computer with encrypted disk (BitLocker etc.).Step 2: Force shutdown or cold reboot.Step 3: Immediately reboot with bootable USB to read RAM content.Step 4: RAM still holds encryption keys temporarily.Step 5: Extract keys and use to decrypt drive.Step 6: Exit without leaving hardware traces.
- **Detection**: Specialized memory forensics
- **Solution**: Use TPM with PIN + RAM wipe on shutdown
- **Tags**: Cold Boot, Memory Attack

## Fake Electrician Installs Keylogger in Server Room

- **Attack Type**: Insider Impersonation
- **Target**: Server Room PC
- **Vulnerability**: Poor identity validation, unmanaged ports
- **MITRE**: T1056.001 - Input Capture
- **Impact**: High-privilege credential theft
- **Tools**: Clipboard, ID Badge, Small USB Logger
- **Scenario**: Attacker enters data center disguised as technician to install logging device.
- **Attack Steps**: Step 1: Dress like a facility technician and carry basic tools.Step 2: Request access to server room for “electrical inspection”.Step 3: Once alone, plug USB logger into a keyboard port of critical workstation.Step 4: Device silently logs inputs.Step 5: Exit normally and retrieve device later.
- **Detection**: Camera logs, unusual USB activity
- **Solution**: Verify staff via two-factor ID, escorted access
- **Tags**: Impersonation, USB Logger

## Physically Modifying a Mouse to Include Keylogger

- **Attack Type**: Hardware Implant
- **Target**: Office Desktop
- **Vulnerability**: No endpoint validation, blind hardware trust
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Silent input capture
- **Tools**: Modified Mouse, Logging Chip
- **Scenario**: Attacker replaces user’s mouse with one that contains an embedded logging chip.
- **Attack Steps**: Step 1: Prepare a mouse that looks exactly like the target’s brand.Step 2: Embed a hardware chip inside to record keystrokes or mouse movements.Step 3: Tailgate or sneak in to swap the mouse.Step 4: The fake mouse operates normally but records/logs data internally.Step 5: Retrieve mouse later and extract data.
- **Detection**: Sudden device swap alerts, inventory logs
- **Solution**: Use asset tagging, security audits
- **Tags**: Mouse, Keylogger, Hardware Hack

## MicroSD Implant in Printer USB Port

- **Attack Type**: Data Capture Device
- **Target**: Network Printer
- **Vulnerability**: Unsecured peripherals, USB exposed
- **MITRE**: T1005 - Data from Local System
- **Impact**: Document exfiltration
- **Tools**: MicroSD Logger Device
- **Scenario**: Attacker places a disguised MicroSD logger in printer’s USB port to capture scanned documents.
- **Attack Steps**: Step 1: Approach common-use printer/scanner in office.Step 2: Insert MicroSD logger disguised as USB extension or charger.Step 3: Logger captures all scanned/uploaded documents in print queue.Step 4: Retrieve later or remotely download files.Step 5: Remove device before discovery.
- **Detection**: Audit USB access logs, review print history
- **Solution**: Lock USB ports, only allow approved accessories
- **Tags**: Printer, USB Hack

## Access Point Impersonation in Office

- **Attack Type**: Evil Twin Wi-Fi
- **Target**: Wireless Network
- **Vulnerability**: No AP validation, same SSID reuse
- **MITRE**: T1557.002 - Adversary-in-the-Middle: Wireless
- **Impact**: Internal access, data theft
- **Tools**: Laptop, Wi-Fi Adapter, Karma Tool
- **Scenario**: Attacker sets up a fake Wi-Fi AP with same SSID as office to capture credentials.
- **Attack Steps**: Step 1: Use a laptop or Raspberry Pi with wireless adapter.Step 2: Set up rogue AP with same SSID as company Wi-Fi.Step 3: Position near reception or cafeteria.Step 4: Victims unknowingly connect; credentials and traffic are logged.Step 5: Use stolen credentials for internal system access.
- **Detection**: Detect duplicate SSIDs, signal triangulation
- **Solution**: Enable WPA3, AP certificates
- **Tags**: Wi-Fi, Evil Twin

## USB Fan Drops Trojan Payload

- **Attack Type**: Trojan via Gadget
- **Target**: Employee Laptop
- **Vulnerability**: Trusting unknown devices
- **MITRE**: T1204.002 - User Execution: Malicious File
- **Impact**: Remote access, malware deployment
- **Tools**: USB Fan with Hidden Storage, Payload Script
- **Scenario**: Attacker gifts or drops a USB fan device in the office that executes malware when plugged in.
- **Attack Steps**: Step 1: Leave promotional USB fan on front desk or break room.Step 2: Wait for someone to plug it into a PC.Step 3: Fan works, but hidden USB executes a malware payload silently.Step 4: Creates backdoor or exfiltrates files.Step 5: Attacker accesses compromised system remotely.
- **Detection**: USB control logs, endpoint monitoring
- **Solution**: Employee training, block USB storage
- **Tags**: USB, Trojan Gadget

## Malicious Label Printer Drops Credential Stealer

- **Attack Type**: Peripherals Exploit
- **Target**: Workstation
- **Vulnerability**: Unsigned drivers, plug-n-play trust
- **MITRE**: T1193 - Exploit Public-Facing Application
- **Impact**: Credential theft, internal access
- **Tools**: Compromised Printer, Malicious Driver File
- **Scenario**: Compromised label printer is installed to spread credential-stealing malware via driver or print job.
- **Attack Steps**: Step 1: Plug in pre-infected label printer into system.Step 2: Install its drivers — attacker modified them to contain spyware.Step 3: Driver installs keylogger or beacon for remote control.Step 4: Victim uses printer unaware it’s infected.Step 5: Credentials and documents are exfiltrated silently.
- **Detection**: Driver audit, antivirus logs
- **Solution**: Use signed drivers, restrict USB installs
- **Tags**: Peripheral, Malicious Driver

## Mobile Charger with Hidden Keylogger

- **Attack Type**: HID Injection
- **Target**: Workstation/Laptop
- **Vulnerability**: Trust in USB charging devices
- **MITRE**: T1056.001 - Input Capture
- **Impact**: Silent malware drop, backdoor
- **Tools**: USB Charger with HID Chip
- **Scenario**: Attacker offers a free mobile charger that acts as a HID device, injecting keystrokes when plugged into a PC.
- **Attack Steps**: Step 1: Leave charger labeled "Free – Take Me!" in common office area.Step 2: Target plugs it into PC expecting to charge phone.Step 3: Inside the charger, HID chip emulates keyboard and injects malicious keystrokes.Step 4: It may open terminal, download malware, or create backdoor silently.Step 5: Attacker connects remotely later to compromise the machine.
- **Detection**: Endpoint monitoring, USB device logs
- **Solution**: Disable USB HID devices, employee awareness
- **Tags**: HID, Charger, Physical Payload

## Stolen ID Badge Used for Server Room Entry

- **Attack Type**: Badge Misuse
- **Target**: Secure Server Room
- **Vulnerability**: Badge reuse without PIN, no photo verification
- **MITRE**: T1078 - Valid Accounts (Physical)
- **Impact**: Internal data compromise
- **Tools**: Stolen Access Badge
- **Scenario**: Attacker picks up lost employee ID badge and uses it to access secured server room.
- **Attack Steps**: Step 1: Find or steal employee access badge from cafeteria or washroom.Step 2: Wait for low traffic hours.Step 3: Walk confidently to server room and scan badge.Step 4: Enter without challenge if staff assumes legitimacy.Step 5: Perform malicious actions — plug in USB logger or sniffing device.
- **Detection**: Access logs, CCTV
- **Solution**: Combine badge with PIN or biometric auth
- **Tags**: Badge, Social Engineering

## Sticky Note Password Harvest

- **Attack Type**: Visual Reconnaissance
- **Target**: Office Desktops
- **Vulnerability**: Users writing down passwords visibly
- **MITRE**: T1056.002 - Input Capture (Visual)
- **Impact**: Credential theft, unauthorized access
- **Tools**: Camera or Mobile Phone
- **Scenario**: Attacker searches desks during breaks for passwords written on sticky notes.
- **Attack Steps**: Step 1: Roam office during lunch or cleaning hours.Step 2: Look for sticky notes or papers stuck to monitors or under keyboards.Step 3: Take photo or note down usernames and passwords.Step 4: Use captured credentials to log into systems later.Step 5: Erase traces if anything is touched.
- **Detection**: Random desk audits
- **Solution**: Promote password managers, enforce clean desk policy
- **Tags**: Sticky Note, Password Leak

## Keyboard Overload – Fake Update Prompt

- **Attack Type**: Visual Phishing
- **Target**: Office PC
- **Vulnerability**: Visual trick, no lockout policies
- **MITRE**: T1056.001 - Input Capture
- **Impact**: Credential harvesting
- **Tools**: Wallpaper File, Dummy Login Script
- **Scenario**: Attacker changes monitor wallpaper to show "Windows Update" message and logs credentials.
- **Attack Steps**: Step 1: Gain access to workstation (e.g., janitor shift or tailgating).Step 2: Change background image to look like Windows Update screen.Step 3: Add script to auto-launch fake login screen when PC wakes.Step 4: User sees prompt and re-enters password.Step 5: Credentials logged and sent to attacker.
- **Detection**: Boot check, screen inspection
- **Solution**: Use lock screen, limit script permissions
- **Tags**: Phishing, Visual Deceit

## Dropped USB Cable Trap

- **Attack Type**: USB Drop Attack
- **Target**: Laptop / Workstation
- **Vulnerability**: Trust in accessories, no HID restrictions
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Remote command execution
- **Tools**: Modified USB Cable (O.MG Cable)
- **Scenario**: Attacker leaves an authentic-looking USB cable that contains payload to execute when plugged in.
- **Attack Steps**: Step 1: Drop seemingly regular charging cable in meeting room or lobby.Step 2: Victim plugs it into PC to charge phone.Step 3: Cable executes pre-loaded payload via HID emulation.Step 4: Attacker connects wirelessly and exfiltrates data.Step 5: Victim remains unaware due to lack of visible programs.
- **Detection**: Unusual traffic logs
- **Solution**: Disable HID input, train staff
- **Tags**: O.MG Cable, USB HID

## Laptop Bag Swap Attack

- **Attack Type**: Device Swap
- **Target**: Portable Devices
- **Vulnerability**: Physical access, unattended bags
- **MITRE**: T1025 - Data from Removable Media
- **Impact**: Loss of corporate assets
- **Tools**: Identical Laptop Bag
- **Scenario**: Attacker swaps similar-looking laptop bag at café or conference to steal target's laptop.
- **Attack Steps**: Step 1: Observe victim place laptop bag unattended briefly.Step 2: Bring a visually identical bag with decoy laptop inside.Step 3: Swap the bags discreetly.Step 4: Leave the area with real laptop containing sensitive data.Step 5: Victim realizes swap much later.
- **Detection**: Reported loss, CCTV
- **Solution**: Keep devices locked, use tracking tags
- **Tags**: Theft, Physical Swap

## Reverse Tailgating During Fire Drill

- **Attack Type**: Entry Without Exit
- **Target**: Corporate Premises
- **Vulnerability**: No one monitors who enters during drill
- **MITRE**: T1078 - Valid Accounts (Physical)
- **Impact**: Unauthorized physical access
- **Tools**: None
- **Scenario**: Attacker enters building as everyone exits for fire drill.
- **Attack Steps**: Step 1: Monitor building with fire drill scheduled.Step 2: As employees evacuate, walk in unnoticed through exit doors.Step 3: Move toward unlocked internal sections.Step 4: Plant malicious hardware (e.g., Wi-Fi Pineapple, USB logger).Step 5: Exit later as building returns to normal.
- **Detection**: Review access footage
- **Solution**: Station guards during drills, badge scan to re-enter
- **Tags**: Tailgating, Entry Exploit

## Magnetic Door Bypass via Internal Handle

- **Attack Type**: Door Exploit
- **Target**: Server Room, Labs
- **Vulnerability**: Magnetic locks with poor physical seals
- **MITRE**: T1068 - Exploitation for Privilege Escalation
- **Impact**: Physical perimeter breach
- **Tools**: Thin Wire, Plastic Wedge
- **Scenario**: Attacker wedges open magnetic door slightly, then uses wire to pull inside handle.
- **Attack Steps**: Step 1: Identify magnetic lock door with glass pane or side gap.Step 2: Wedge open door by a centimeter using plastic card or wedge.Step 3: Slide wire inside to hook internal handle.Step 4: Pull handle to open door fully.Step 5: Enter restricted area undetected.
- **Detection**: Door sensors, camera logs
- **Solution**: Reinforce doors, use motion sensors
- **Tags**: Door Bypass, Entry Attack

## Fake IT Staff Collecting "Old Equipment"

- **Attack Type**: Impersonation Theft
- **Target**: Offices, Schools
- **Vulnerability**: No IT asset validation
- **MITRE**: T1005 - Data from Local System
- **Impact**: Loss of devices, potential data breach
- **Tools**: Fake ID Badge, Pickup Sheet
- **Scenario**: Attacker pretends to be IT staff collecting old devices for disposal and walks out with functional assets.
- **Attack Steps**: Step 1: Dress in generic IT attire and carry a fake clipboard.Step 2: Visit department claiming old PCs or printers are being collected.Step 3: Staff assumes it's scheduled; allows access.Step 4: Attacker collects real working devices.Step 5: Walks out without raising suspicion.
- **Detection**: Inventory mismatch
- **Solution**: Maintain asset logs, disposal tags
- **Tags**: Impersonation, Theft

## Lock Pick Attack on IT Cabinet

- **Attack Type**: Physical Lock Bypass
- **Target**: Switch Cabinets
- **Vulnerability**: Simple locks, no tamper detection
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Switch tampering, network compromise
- **Tools**: Lock Pick Set, Gloves
- **Scenario**: Attacker picks lock of IT equipment cabinet to tamper with switches or storage devices.
- **Attack Steps**: Step 1: Identify location of network/IT cabinet in hallway or office.Step 2: Wait for quiet hours or during shift change.Step 3: Use lock pick tools to unlock standard cabinet lock.Step 4: Access switch ports, plug rogue device or remove hard drives.Step 5: Lock back and leave, leaving no trace unless logs are reviewed.
- **Detection**: Cabinet sensors, physical audit
- **Solution**: Use tamper-evident seals and CCTV
- **Tags**: Lock Picking, Network Attack

## Wall Jack MAC Spoofing for Internal Access

- **Attack Type**: Network Spoofing
- **Target**: Office LAN
- **Vulnerability**: Poor port control, no dynamic NAC
- **MITRE**: T1040 - Network Sniffing
- **Impact**: Lateral movement, internal recon
- **Tools**: Laptop, MAC Spoofing Tool
- **Scenario**: Attacker plugs into LAN port in public area and spoofs MAC address of legitimate device.
- **Attack Steps**: Step 1: Locate unused LAN jack in meeting room or hallway.Step 2: Plug in attacker’s laptop.Step 3: Use MAC address spoofing tool (like macchanger) to impersonate known authorized device.Step 4: Bypass Network Access Control (NAC) and gain LAN access.Step 5: Explore internal network silently.
- **Detection**: Switch logs, MAC audit
- **Solution**: Implement 802.1X NAC, disable unused ports
- **Tags**: MAC Spoofing, Ethernet Port

## Hidden Camera Behind Whiteboard

- **Attack Type**: Surveillance Device
- **Target**: Conference Room
- **Vulnerability**: No visual inspection or EM scan
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Theft of sensitive internal info
- **Tools**: Mini Spy Cam with Wi-Fi
- **Scenario**: Attacker installs micro camera behind conference room whiteboard to record screen shares and meeting notes.
- **Attack Steps**: Step 1: Enter meeting room early or as cleaning staff.Step 2: Peel back whiteboard or pin surface slightly.Step 3: Mount spy cam aimed at screen or whiteboard.Step 4: Leave it recording or stream over Wi-Fi.Step 5: Collect device later or download video remotely.
- **Detection**: Hidden device scan, radio analysis
- **Solution**: Perform periodic bug sweeps, limit access
- **Tags**: Camera, Espionage, Surveillance

## BIOS Flash Using External Programmer

- **Attack Type**: Firmware Tampering
- **Target**: Desktop PC
- **Vulnerability**: Unsecured firmware chip
- **MITRE**: T1542.001 - Pre-OS Boot: BIOS
- **Impact**: Persistent control of device
- **Tools**: SOIC8 Clip, CH341A Programmer
- **Scenario**: Attacker reprograms BIOS chip using clip-on programmer to install persistent rootkit.
- **Attack Steps**: Step 1: Open case of powered-off target PC.Step 2: Clip SOIC8 connector onto BIOS chip on motherboard.Step 3: Connect to CH341A programmer and re-flash with rootkitted BIOS.Step 4: Remove clip, reboot system.Step 5: Rootkit survives OS reinstall, hidden from antivirus.
- **Detection**: BIOS hash comparison
- **Solution**: Use firmware protection, tamper locks
- **Tags**: BIOS, Rootkit, Firmware Hack

## Elevator Floor Hold for Unauthorized Entry

- **Attack Type**: Physical Entry Trick
- **Target**: Office Building
- **Vulnerability**: No escort requirement on secure floors
- **MITRE**: T1078 - Valid Accounts (Physical)
- **Impact**: Unauthorized internal access
- **Tools**: None
- **Scenario**: Attacker uses elevator hold button to stop at restricted floor without keycard.
- **Attack Steps**: Step 1: Enter elevator with authorized employee.Step 2: Wait until restricted floor is selected.Step 3: Secretly press “Door Hold” or jam button.Step 4: Exit at restricted floor without credentials.Step 5: Begin physical attack or plug device into unlocked PC.
- **Detection**: Elevator logs, camera review
- **Solution**: Require escorts or PIN at exit
- **Tags**: Elevator, Social Engineering

## Laptop Sleep Mode Data Theft

- **Attack Type**: Session Hijack
- **Target**: Laptop
- **Vulnerability**: Sleep mode with no auto-lock, no encryption
- **MITRE**: T1005 - Data from Local System
- **Impact**: Quick data exfiltration
- **Tools**: USB Stick, Laptop
- **Scenario**: Attacker accesses data on a laptop left in sleep mode (not shut down) with unlocked disk.
- **Attack Steps**: Step 1: Find unattended laptop in sleep mode (e.g., cafeteria).Step 2: Wake device — many stay unlocked.Step 3: Plug in USB and copy files silently.Step 4: Optionally install malware.Step 5: Close lid and walk away.
- **Detection**: Screen lock policies, USB audits
- **Solution**: Enforce lock-on-sleep, enable encryption
- **Tags**: Session Hijack, Laptop Access

## Keypad Entry Brute Force via Overlay Device

- **Attack Type**: Access Code Harvest
- **Target**: Keypad-Protected Rooms
- **Vulnerability**: No overlay detection, no input logging
- **MITRE**: T1056.001 - Input Capture
- **Impact**: Physical security bypass
- **Tools**: 3D-Printed Overlay with Storage
- **Scenario**: Attacker places a fake keypad overlay to log PINs at doors or cabinets.
- **Attack Steps**: Step 1: Design fake keypad identical to the original.Step 2: Attach it over real one when area is empty.Step 3: Device logs all key presses (user PINs).Step 4: Retrieve overlay later to extract codes.Step 5: Use PINs to gain real access.
- **Detection**: Physical inspection, tamper alerts
- **Solution**: Use anti-overlay tech, camera monitoring
- **Tags**: PIN Pad, Overlay Attack

## Fire Extinguisher Cabinet as Implant Hideout

- **Attack Type**: Hidden Device Strategy
- **Target**: Office LAN
- **Vulnerability**: Unmonitored safety fixtures
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Persistent covert access
- **Tools**: Raspberry Pi, Ethernet Cable
- **Scenario**: Attacker hides small Raspberry Pi behind or inside a fire cabinet connected to network.
- **Attack Steps**: Step 1: Locate rarely accessed fire safety cabinet.Step 2: Open and conceal Pi behind or inside.Step 3: Connect to nearby Ethernet jack or hidden switch.Step 4: Power via power bank or PoE injector.Step 5: Access remotely via reverse shell or VPN.
- **Detection**: Network scans, unusual traffic alerts
- **Solution**: Seal safety fixtures, inspect regularly
- **Tags**: Raspberry Pi, Physical Covert Access

## Vending Machine USB Implant

- **Attack Type**: Public Device Exploit
- **Target**: Smart Kiosk / Vending Machine
- **Vulnerability**: No USB lockdown, public-facing device
- **MITRE**: T1200 - Hardware Additions
- **Impact**: VLAN pivoting, lateral attack
- **Tools**: USB Implant, Rubber Ducky
- **Scenario**: Attacker plugs implant into USB port on smart vending machine to pivot into internal network.
- **Attack Steps**: Step 1: Find smart vending/kiosk with exposed USB port.Step 2: Insert USB implant disguised as normal drive.Step 3: Payload opens reverse shell to attacker.Step 4: Use this access to pivot into internal VLAN.Step 5: Remove evidence or leave as backdoor.
- **Detection**: Kiosk logs, endpoint alerts
- **Solution**: Disable unused ports, isolate VLANs
- **Tags**: Kiosk, Public USB Attack

## Badge Cloning at Gym Locker Room

- **Attack Type**: RFID Badge Theft
- **Target**: RFID Entry System
- **Vulnerability**: No badge shielding, unattended assets
- **MITRE**: T1078 - Valid Accounts
- **Impact**: Physical access escalation
- **Tools**: RFID Cloner (Proxmark3), Blank Cards
- **Scenario**: Attacker clones RFID badge left in bag or locker at on-site gym.
- **Attack Steps**: Step 1: Enter company gym pretending to be member.Step 2: Wait for employees to leave bags in lockers.Step 3: Scan badges inside bag using hidden cloner.Step 4: Clone badge to blank RFID card.Step 5: Use cloned badge to access secure areas later.
- **Detection**: Locker room camera, access mismatch logs
- **Solution**: Encourage RFID pouches, alert employees
- **Tags**: Badge, Gym, RFID

## Visual Pattern Unlock Bypass

- **Attack Type**: Shoulder Surf + Smudge Attack
- **Target**: Mobile Devices
- **Vulnerability**: No biometric lock, visible pattern
- **MITRE**: T1056.002 - Input Capture (Visual)
- **Impact**: Phone data compromise
- **Tools**: Eyes, Flashlight
- **Scenario**: Attacker observes Android lock pattern or recovers it via smudge on screen.
- **Attack Steps**: Step 1: Watch target draw unlock pattern on phone.Step 2: If missed, wait for them to leave the device.Step 3: Use flashlight to highlight fingerprint smudge trail.Step 4: Try likely patterns to unlock phone.Step 5: Access messages, VPNs, email apps.
- **Detection**: Use of smudge-resistant screen guards
- **Solution**: Encourage biometrics, rotate unlock method
- **Tags**: Phone, Visual Exploit

## Fake Job Interviewer Steals Laptop

- **Attack Type**: Social Engineering Theft
- **Target**: Laptops
- **Vulnerability**: Trust, unattended belongings
- **MITRE**: T1025 - Data from Removable Media
- **Impact**: Theft of device with personal and business data
- **Tools**: Business Attire, Fake Badge
- **Scenario**: Attacker pretends to be a company interviewer and asks candidate to leave device behind, then steals it.
- **Attack Steps**: Step 1: Set up fake interview booth in shared office space.Step 2: Invite target candidate and create urgent excuse mid-interview.Step 3: Ask candidate to leave bag/laptop momentarily.Step 4: Leave with stolen device before candidate returns.Step 5: Extract data from device later.
- **Detection**: CCTV review
- **Solution**: Conduct interviews in verified rooms only
- **Tags**: Social Engineering, Theft

## Bricking Device via Power Surge Injection

- **Attack Type**: Hardware Destruction
- **Target**: Laptops, IoT Devices
- **Vulnerability**: Open access to ports, no surge protection
- **MITRE**: T1495 - Firmware Corruption
- **Impact**: Device bricked, potential permanent loss
- **Tools**: Charged Capacitor, Modified Cable
- **Scenario**: Attacker injects a high voltage signal into device’s power port to destroy components.
- **Attack Steps**: Step 1: Carry cable with internal capacitor charged with high voltage.Step 2: Plug into target device’s USB-C or power port.Step 3: Capacitor discharges, frying motherboard or logic board.Step 4: Device becomes unusable; attacker walks away.
- **Detection**: Damage inspection
- **Solution**: Surge arresters, port locking caps
- **Tags**: Destruction, Surge, USB Kill

## Fake Donation Box with Camera and Card Skimmer

- **Attack Type**: Covert Collection
- **Target**: Door Access Cards, ID Cards
- **Vulnerability**: Human trust, unattended physical access
- **MITRE**: T1056.001 - Input Capture
- **Impact**: Clone access cards or steal identity
- **Tools**: Hidden Cam, Card Skimmer
- **Scenario**: Attacker places a fake charity box with hidden skimmer and camera in a common area.
- **Attack Steps**: Step 1: Design fake box labeled for donations with visible slot and reader.Step 2: Place on reception or lunch table with pamphlets.Step 3: Hidden skimmer reads swipe card; camera records PIN.Step 4: Collect device at day’s end to harvest credentials.
- **Detection**: Card reader logs
- **Solution**: Supervise donation/collection boxes
- **Tags**: Card Skimming, Covert Surveillance

## Exploiting Smart Coffee Machine Wi-Fi

- **Attack Type**: Smart Device Exploit
- **Target**: IoT Appliance
- **Vulnerability**: Open ports, weak credentials
- **MITRE**: T1190 - Exploit Public-Facing Application
- **Impact**: Internal access via IoT pivot
- **Tools**: Laptop, Wi-Fi Adapter
- **Scenario**: Attacker connects to poorly secured smart coffee machine to pivot into internal network.
- **Attack Steps**: Step 1: Scan for open Wi-Fi networks in breakroom.Step 2: Connect to coffee machine’s network.Step 3: Access web interface (often no password).Step 4: Exploit firmware vulnerability or escalate to internal VLAN.Step 5: Use foothold to scan or attack other devices.
- **Detection**: Network scan, alert rules
- **Solution**: Segregate IoT on VLAN, change defaults
- **Tags**: Coffee Machine, IoT Pivot

## Credit Card-Sized PC Behind Monitor

- **Attack Type**: Stealth Device Plant
- **Target**: Office Desktop
- **Vulnerability**: Lack of device inventory and monitoring
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Long-term access for data theft
- **Tools**: Raspberry Pi, Velcro, USB Power
- **Scenario**: Attacker hides Raspberry Pi-sized PC behind display to gain persistent internal access.
- **Attack Steps**: Step 1: Enter during maintenance hours or impersonate IT.Step 2: Attach Pi behind monitor with Velcro.Step 3: Connect to power via USB hub and plug into network.Step 4: Pi initiates reverse shell to attacker’s server.Step 5: Operate remotely undetected.
- **Detection**: Port scans, unusual DNS traffic
- **Solution**: Monitor unknown MAC addresses, use NDR
- **Tags**: Hardware Implant, Raspberry Pi

## Ethernet Drop Cable Under Carpet

- **Attack Type**: Hidden Network Tapping
- **Target**: Desktop PC, IP Phones
- **Vulnerability**: Physical network exposure
- **MITRE**: T1040 - Network Sniffing
- **Impact**: Data leakage, credential capture
- **Tools**: Flat Ethernet Cable, Tap
- **Scenario**: Attacker lays Ethernet splitter or tap under carpet between wall jack and device.
- **Attack Steps**: Step 1: Observe cable layout between wall and PC.Step 2: Temporarily lift carpet or mat.Step 3: Install Ethernet tap/splitter with outbound cable hidden.Step 4: Connect logger or sniffing laptop remotely.Step 5: Collect data over time or live monitor traffic.
- **Detection**: Cable audit, physical inspections
- **Solution**: Lock cabling trays, port authentication
- **Tags**: Tap, Ethernet, Covert Device

## Whiteboard Marker Embedded with Mic

- **Attack Type**: Audio Espionage
- **Target**: Conference Room
- **Vulnerability**: Trusted shared office supplies
- **MITRE**: T1056.003 - Input Capture: Audio Capture
- **Impact**: Confidential meeting leaks
- **Tools**: Spy Mic Pen
- **Scenario**: Attacker places a marker pen with embedded audio mic in meeting room.
- **Attack Steps**: Step 1: Modify whiteboard marker to contain audio mic and storage.Step 2: Leave it in shared meeting room pen tray.Step 3: It records voices during meetings.Step 4: Attacker collects it after hours and extracts audio.Step 5: Use information for social engineering or data leak.
- **Detection**: Sweep for hidden mics
- **Solution**: Monitor unauthorized stationery
- **Tags**: Audio Spy, Meeting Leak

## Remote Mouse Jamming via RF Dongle

- **Attack Type**: RF Interference
- **Target**: Wireless Mouse
- **Vulnerability**: No RF pairing validation
- **MITRE**: T1056.001 - Input Capture
- **Impact**: Short-term chaos, distraction attack
- **Tools**: RF Mouse Dongle, Jammer
- **Scenario**: Attacker disrupts wireless mouse using RF jammer or clone dongle to confuse user.
- **Attack Steps**: Step 1: Sit near victim using wireless mouse.Step 2: Use duplicate USB dongle to pair with victim’s mouse.Step 3: Interfere with commands or control cursor remotely.Step 4: Use chaos to distract or move user from PC.Step 5: Plug in malicious USB or launch payload.
- **Detection**: Peripheral logs
- **Solution**: Use Bluetooth or wired input devices
- **Tags**: Mouse Hijack, RF Exploit

## Using Lost USB to Deliver Ransomware

- **Attack Type**: USB Drop
- **Target**: Office Workstation
- **Vulnerability**: Curiosity, no USB execution restrictions
- **MITRE**: T1204.002 - User Execution: Malicious File
- **Impact**: Encryption of local and shared files
- **Tools**: USB with Payload
- **Scenario**: Attacker drops USB marked "Salary Info" or "Confidential" to bait user into plugging it in.
- **Attack Steps**: Step 1: Prepare USB with ransomware payload set to auto-run.Step 2: Label it attractively and drop in parking lot or break room.Step 3: Victim plugs into work PC.Step 4: Payload executes, encrypts files, and demands ransom.Step 5: Attacker contacts via email or onion site.
- **Detection**: Antivirus, SIEM alerts
- **Solution**: Disable auto-run, train employees
- **Tags**: Ransomware, USB Bait

## Hard Drive Swap in Docking Station

- **Attack Type**: Hardware Swap
- **Target**: Docking Workstation
- **Vulnerability**: Lack of asset tags, easy hardware swap
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Compromise of system boot & data
- **Tools**: Screwdriver, Malicious Drive
- **Scenario**: Attacker swaps physical hard drive in docking station with compromised one.
- **Attack Steps**: Step 1: Locate docking station in shared IT room.Step 2: Swap real hard drive with attacker’s preloaded drive.Step 3: Victim boots into modified OS with backdoor.Step 4: Data gets copied silently to attacker’s drive.Step 5: Attacker swaps drives back before anyone notices.
- **Detection**: Boot hash mismatch, BIOS logs
- **Solution**: Lock HDDs, implement secure boot
- **Tags**: HDD Swap, Insider Exploit

## USB Debug Port Abuse on Router

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Router / IoT
- **Vulnerability**: Exposed UART Interface
- **MITRE**: T1204.002 (Hardware Additions)
- **Impact**: Root access, firmware dump
- **Tools**: UART-to-USB cable, terminal software (Putty)
- **Scenario**: Attacker abuses USB debug port left exposed on a home/office router to gain shell access.
- **Attack Steps**: Step 1: Look at the back or underside of the router for unlabelled or small pin headers.Step 2: Use a USB-to-UART cable and connect to TX, RX, GND pins (never connect VCC).Step 3: Open Putty on your PC, set correct baud rate (commonly 115200), and connect.Step 4: Reboot the router and observe the boot process logs.Step 5: Press key (like Enter or Esc) when prompted to interrupt bootloader.Step 6: Type commands to gain root shell or dump firmware.
- **Detection**: Physical inspection, serial line monitoring
- **Solution**: Disable unused ports, epoxy over debug headers
- **Tags**: UART, Debug, Router Exploit, Education

## JTAG Extraction of Smart TV Firmware

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart TV
- **Vulnerability**: Exposed JTAG debug headers
- **MITRE**: T1129 (Hardware Reverse Engineering)
- **Impact**: Firmware theft, reverse engineering
- **Tools**: JTAGulator, OpenOCD, soldering kit
- **Scenario**: Attacker connects to JTAG pins of a Smart TV motherboard and extracts firmware for analysis.
- **Attack Steps**: Step 1: Open back panel of Smart TV using screwdriver.Step 2: Locate JTAG pins on the main board (may be labeled TDI, TDO, TCK, TMS).Step 3: Connect JTAGulator to these pins with jumper wires.Step 4: Power on the device and run auto-detect from JTAGulator to verify signal.Step 5: Use OpenOCD or UrJTAG to dump memory.Step 6: Analyze the firmware offline for credentials, APIs, hardcoded keys.
- **Detection**: Power/current irregularities, tamper sensors
- **Solution**: Obfuscate/debug fuse disable, conformal coating
- **Tags**: JTAG, Firmware Dump, Reverse Engineering

## SPI Flash Chip Cloning from CCTV

- **Attack Type**: Hardware Interface Exploitation
- **Target**: CCTV Camera
- **Vulnerability**: Accessible SPI flash memory
- **MITRE**: T1003.003 (Credential Dumping - Firmware)
- **Impact**: Extract passwords, surveillance bypass
- **Tools**: SOIC8 clip, CH341A programmer, flashrom
- **Scenario**: Attacker reads the CCTV's SPI flash memory chip using clip-based reader to extract firmware or modify it.
- **Attack Steps**: Step 1: Power off CCTV and open the casing.Step 2: Locate the SPI flash chip (usually 8-pin, labeled 25xxx).Step 3: Attach SOIC8 clip onto the chip, connect to CH341A USB programmer.Step 4: Plug into computer and use flashrom to read and backup firmware.Step 5: Optionally modify and reflash to implant malicious config.Step 6: Reassemble the device and boot normally.
- **Detection**: Boot checksum failure, boot loop
- **Solution**: Encrypt firmware, glue chips, checksum validation
- **Tags**: SPI, CCTV, Firmware, Education

## EEPROM Data Dump on Access Control Device

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Access Control Panel
- **Vulnerability**: Unencrypted EEPROM storage
- **MITRE**: T1555.004 (Credential Storage)
- **Impact**: PIN and biometric leak
- **Tools**: EEPROM reader (MiniPro), clip adapter
- **Scenario**: Attacker accesses EEPROM of a biometric access device to retrieve stored PINs and fingerprints.
- **Attack Steps**: Step 1: Identify EEPROM chip (often 24Cxx series) on PCB inside access device.Step 2: Connect clip adapter to the chip without desoldering.Step 3: Use MiniPro software to detect and read data from EEPROM.Step 4: Export hex dump and convert into readable form using hex editor.Step 5: Look for plaintext credentials, IDs, or fingerprint data patterns.Step 6: Reflash original dump to avoid detection.
- **Detection**: Access logs mismatch, audit failure
- **Solution**: Encrypt EEPROM, detect tampering
- **Tags**: EEPROM, Physical Access, Access Control

## HDMI-CEC Exploitation for Remote Control

- **Attack Type**: Hardware Interface Exploitation
- **Target**: cec-client -s -d 1` to power on the TV.Step 4: Send keypress sequences to navigate settings remotely.Step 5: Reconfigure network settings or install unauthorized apps.Step 6: Power off TV after changes to avoid suspicion.
- **Vulnerability**: Smart TV
- **MITRE**: Unrestricted HDMI-CEC access
- **Impact**: T0886 (Remote Control Interface Abuse)
- **Tools**: Raspberry Pi with HDMI-CEC lib
- **Scenario**: Attacker uses HDMI-CEC protocol to send malicious commands to Smart TV via HDMI input.
- **Attack Steps**: Step 1: Connect Raspberry Pi via HDMI cable to target Smart TV.Step 2: Install cec-utils on Raspberry Pi.Step 3: Use command like `echo "on 0"
- **Detection**: TV compromise, data leak
- **Solution**: TV logs, abnormal remote use
- **Tags**: Disable HDMI-CEC or restrict devices

## I2C Bus Sniffing on Printer

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Printer
- **Vulnerability**: Exposed I2C communication lines
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Info leak from device communication
- **Tools**: Logic Analyzer (e.g., Saleae), hook probes
- **Scenario**: Attacker connects to I2C lines inside a printer to sniff data like print job contents and credentials.
- **Attack Steps**: Step 1: Open the printer and look for SDA and SCL lines (I2C).Step 2: Attach hook probes from logic analyzer to those lines.Step 3: Start capturing data while printing is active.Step 4: Decode I2C traffic using analyzer software.Step 5: Identify useful info like print content or credentials.Step 6: Save logs and restore printer casing.
- **Detection**: Anomalous device activity
- **Solution**: Shield I2C lines or encrypt communication
- **Tags**: I2C, Logic Analyzer, Printer Exploit

## Debug Access on POS Machine

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Point-of-Sale (POS)
- **Vulnerability**: Debug port left active
- **MITRE**: T1204.002
- **Impact**: Transaction tampering, data access
- **Tools**: UART cable, Putty, Screwdriver
- **Scenario**: Gaining control over a Point-of-Sale machine via exposed debug interface on its board.
- **Attack Steps**: Step 1: Open POS machine using screwdriver.Step 2: Locate UART pins (marked TX, RX, GND).Step 3: Connect UART-to-USB cable.Step 4: Open terminal (Putty) and observe boot logs.Step 5: Interrupt boot and drop into debug shell.Step 6: View or modify transaction data.
- **Detection**: Shell access logs
- **Solution**: Disable debug ports in production
- **Tags**: POS, UART Debug, Retail Attack

## Serial Console Root Access in Industrial HMI

- **Attack Type**: Hardware Interface Exploitation
- **Target**: HMI Device
- **Vulnerability**: Active serial console with no auth
- **MITRE**: T1056.001
- **Impact**: Modify PLC settings, shutdown plant
- **Tools**: Serial-to-USB cable, Putty
- **Scenario**: Using serial console on Human Machine Interface to bypass authentication.
- **Attack Steps**: Step 1: Open HMI panel physically.Step 2: Connect serial cable to console pins (TX, RX, GND).Step 3: Launch Putty and configure correct baud rate.Step 4: Observe boot logs and interrupt if needed.Step 5: Drop to root shell or default menu.Step 6: List/edit critical config files.
- **Detection**: Console access logs
- **Solution**: Console auth, hardware disable switch
- **Tags**: HMI, SCADA, Serial Console

## NAND Flash Dump of Mobile Phone

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Mobile Phone
- **Vulnerability**: Unencrypted NAND storage
- **MITRE**: T1005
- **Impact**: Full data theft
- **Tools**: Hot air gun, NAND reader (Z3X, Easy JTAG), tweezers
- **Scenario**: Extracting entire data from NAND chip by removing and reading it directly.
- **Attack Steps**: Step 1: Remove back panel of mobile phone.Step 2: Desolder NAND chip using hot air gun carefully.Step 3: Place chip into NAND reader.Step 4: Use reader software to clone data.Step 5: Browse contents for files, photos, apps.Step 6: Restore chip and close phone if needed.
- **Detection**: No boot, tamper evidence
- **Solution**: Encrypt NAND, physical epoxy seal
- **Tags**: NAND, Mobile, Chip Dump

## SPI Bus Injection on Smart Meter

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart Meter
- **Vulnerability**: Unprotected SPI interface
- **MITRE**: T0838
- **Impact**: Fraudulent billing
- **Tools**: Logic analyzer, SPI injector, wires
- **Scenario**: Injecting fake data into SPI bus between microcontroller and memory to manipulate readings.
- **Attack Steps**: Step 1: Open smart meter carefully.Step 2: Identify SPI lines (MOSI, MISO, CLK, CS).Step 3: Connect injector inline on SPI bus.Step 4: Capture live traffic and analyze packet format.Step 5: Craft and inject spoofed data.Step 6: Observe meter display changes.
- **Detection**: Unusual traffic patterns
- **Solution**: Secure memory & checksum validation
- **Tags**: SPI, Meter Hacking, Power Theft

## Unsecured CAN Bus Hijack in Automotive

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Vehicle
- **Vulnerability**: Unauthenticated CAN Bus access
- **MITRE**: T0884
- **Impact**: Unsafe control (lights, brakes, etc.)
- **Tools**: CANtact, SavvyCAN, Laptop
- **Scenario**: Attacker plugs into OBD-II port and injects CAN messages to control car systems.
- **Attack Steps**: Step 1: Locate OBD-II port under the dashboard.Step 2: Plug in CANtact device via USB to laptop.Step 3: Use SavvyCAN to read CAN messages.Step 4: Identify message IDs for steering, lights, etc.Step 5: Replay or inject spoofed messages.Step 6: Observe physical response in the car.
- **Detection**: Event logs, unusual CAN IDs
- **Solution**: Gateway/firewall between OBD-II and CAN
- **Tags**: CAN Bus, Car, OBD Exploit

## BMC Console Exploit on Server

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Server
- **Vulnerability**: Active BMC port with no auth
- **MITRE**: T0859
- **Impact**: Root-level remote control
- **Tools**: Serial cable, IPMI tool
- **Scenario**: Exploiting Baseboard Management Controller (BMC) via physical serial port to control server remotely.
- **Attack Steps**: Step 1: Locate physical access to BMC serial port.Step 2: Connect serial cable.Step 3: Access BMC console using IPMI commands.Step 4: Reboot or reflash BIOS settings.Step 5: Install persistent malware.Step 6: Exit and cover tracks.
- **Detection**: Unusual reboots, BIOS checksum fail
- **Solution**: BMC auth, serial disablement
- **Tags**: Server, BMC, IPMI Exploit

## LCD Test Interface Hijack on ATM

- **Attack Type**: Hardware Interface Exploitation
- **Target**: ATM
- **Vulnerability**: Exposed debug/test pins
- **MITRE**: T0866
- **Impact**: UI manipulation, unauthorized access
- **Tools**: GPIO injector, screwdriver
- **Scenario**: Using LCD test pins to inject input into ATM UI during boot.
- **Attack Steps**: Step 1: Open ATM maintenance hatch.Step 2: Locate test pins near LCD or keypad.Step 3: Connect GPIO controller like Raspberry Pi.Step 4: Inject fake input signals during ATM boot.Step 5: Trigger test mode or bypass screen lock.Step 6: Capture logs or access features.
- **Detection**: ATM boot logs, service logs
- **Solution**: Disable test ports in production units
- **Tags**: ATM, LCD Hack, GPIO Interface

## SD Card Bootloader Modification on Embedded Device

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Controller
- **Vulnerability**: Writable boot media
- **MITRE**: T1059.004
- **Impact**: Boot-time malware or persistence
- **Tools**: SD card reader, Hex editor
- **Scenario**: Modifying bootloader on device that boots from microSD to run attacker code.
- **Attack Steps**: Step 1: Remove SD card from target device.Step 2: Insert into your computer via reader.Step 3: Open card contents in hex editor.Step 4: Modify boot script or binary.Step 5: Reinsert SD into device and reboot.Step 6: Verify custom code executes.
- **Detection**: Boot-time logs, tamper flags
- **Solution**: Use read-only boot media, secure boot
- **Tags**: SD Boot, Embedded, Bootloader Hack

## RFID Debug Interface Overload

- **Attack Type**: Hardware Interface Exploitation
- **Target**: RFID Reader
- **Vulnerability**: Debug mode accessible externally
- **MITRE**: T0887
- **Impact**: Unauthorized area access
- **Tools**: RFID dev board, RFID tool (Proxmark3)
- **Scenario**: Abusing RFID device’s debug mode to manipulate reader behavior.
- **Attack Steps**: Step 1: Open RFID reader casing.Step 2: Find debug or dev-mode jumper pads.Step 3: Activate dev mode by shorting pads or holding button.Step 4: Use Proxmark3 to emulate valid tag or issue debug commands.Step 5: Unlock access or reset config.Step 6: Close and restore physical state.
- **Detection**: Reader log anomalies
- **Solution**: Disable dev/debug access physically
- **Tags**: RFID, Debug Mode, Proxmark

## Debug UART Backdoor on Set-Top Box

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Set-Top Box
- **Vulnerability**: UART debug shell not disabled
- **MITRE**: T1204.002
- **Impact**: Free channel access, root takeover
- **Tools**: UART-to-USB cable, Putty
- **Scenario**: Exploiting exposed UART header to get root shell on cable TV set-top box.
- **Attack Steps**: Step 1: Unscrew and open set-top box case.Step 2: Identify UART pins labeled on board (TX, RX, GND).Step 3: Connect TX to RX and RX to TX on UART cable.Step 4: Launch Putty, set baud rate (usually 115200).Step 5: Watch boot logs and interrupt boot with Enter key.Step 6: If shell prompt appears, type commands like id, cat /etc/passwd.
- **Detection**: Serial activity logs
- **Solution**: Disable UART or password-protect
- **Tags**: UART, Cable TV, Backdoor Shell

## JTAG Override on Secure Boot Device

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded System
- **Vulnerability**: Debug access not locked down
- **MITRE**: T0857
- **Impact**: Secure boot bypass, code injection
- **Tools**: JTAG programmer (OpenOCD), Soldering tools
- **Scenario**: Attacker uses JTAG to bypass secure boot validation and run unsigned code.
- **Attack Steps**: Step 1: Open casing of the embedded device.Step 2: Locate JTAG pins (TDI, TDO, TCK, TMS).Step 3: Solder wires or attach header.Step 4: Connect to JTAG programmer.Step 5: Use OpenOCD to halt CPU and overwrite memory.Step 6: Bypass signature checks and load attacker payload.
- **Detection**: Debug status register logs
- **Solution**: Fuse JTAG post-manufacture
- **Tags**: JTAG, Secure Boot Bypass

## SOIC Clip Attack on Smart Lock

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart Lock
- **Vulnerability**: Unencrypted flash memory
- **MITRE**: T1003.003
- **Impact**: Unlock door, modify auth logic
- **Tools**: SOIC8 clip, CH341A, flashrom
- **Scenario**: Reading flash contents of smart lock MCU to extract PINs or override logic.
- **Attack Steps**: Step 1: Unscrew smart lock and expose circuit board.Step 2: Locate the 8-pin flash memory chip (e.g., 25Q32).Step 3: Attach SOIC clip securely to chip.Step 4: Connect to CH341A and open flashrom.Step 5: Dump contents to file and open with hex editor.Step 6: Look for PIN or firmware logic to modify.
- **Detection**: Access failure logs
- **Solution**: Encrypt flash, epoxy coating
- **Tags**: Smart Lock, Flash Dump

## VGA Firmware Injection on Thin Client

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Thin Client / Workstation
- **Vulnerability**: Writable BIOS SPI chip
- **MITRE**: T1542.003
- **Impact**: Firmware-level persistence
- **Tools**: SPI flasher, screwdriver, flashrom
- **Scenario**: Injecting malware into VGA/BIOS firmware of a thin client for persistence.
- **Attack Steps**: Step 1: Open thin client case.Step 2: Locate BIOS/VGA SPI chip.Step 3: Connect flasher tool (e.g., CH341A).Step 4: Dump firmware using flashrom.Step 5: Modify boot logo region or shellcode section.Step 6: Reflash and boot device.Step 7: Malware runs at startup.
- **Detection**: Firmware integrity checks
- **Solution**: Signed firmware, TPM boot validation
- **Tags**: BIOS, VGA Exploit, Persistence

## GPIO Trigger Exploit on Industrial Panel

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Industrial Panel
- **Vulnerability**: Unauthenticated GPIO access
- **MITRE**: T0886
- **Impact**: Force shutdown or disable alarms
- **Tools**: Raspberry Pi GPIO, jumper wires
- **Scenario**: Manipulating GPIO lines on a panel controller to trigger unsafe actions.
- **Attack Steps**: Step 1: Open panel controller and locate GPIO test headers.Step 2: Connect Pi GPIO pins to device's GPIO input.Step 3: Use script to toggle GPIO high/low.Step 4: Monitor panel reaction (e.g., fan off, alarm reset).Step 5: Trigger functions bypassing software interface.
- **Detection**: Behavior logs, fault lights
- **Solution**: Restrict GPIO debug access
- **Tags**: GPIO, Industrial, Trigger Abuse

## USB HID Payload Injection via Debug Port

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Desktop/Server
- **Vulnerability**: USB HID device trusted by system
- **MITRE**: T1056.001
- **Impact**: Reverse shell, user compromise
- **Tools**: Digispark or Rubber Ducky, microUSB cable
- **Scenario**: Sending keystroke payload to headless systems via internal USB debug port.
- **Attack Steps**: Step 1: Open target device and locate internal USB port.Step 2: Plug in Digispark with preloaded keystroke payload.Step 3: Device boots and runs payload as keyboard input.Step 4: Payload opens terminal and downloads backdoor.Step 5: Remove device and close case.
- **Detection**: Unexpected input, USB logs
- **Solution**: Block HID by VID/PID filter
- **Tags**: USB HID, Rubber Ducky

## PCI Debug Interface Exploit

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Workstation / Server
- **Vulnerability**: Exposed PCIe debug/test pins
- **MITRE**: T0880
- **Impact**: Total system compromise
- **Tools**: PCIe debugger, clip, laptop
- **Scenario**: Attacker connects to PCI debug interface (e.g., LPC/PCIe) to control CPU and memory.
- **Attack Steps**: Step 1: Power off system and open case.Step 2: Connect PCIe debugger to exposed test pads or debug header.Step 3: Use software to pause CPU and dump memory.Step 4: Inject commands directly into system.Step 5: Extract secrets, modify live code.Step 6: Resume execution and clean up.
- **Detection**: Hardware monitor tools
- **Solution**: Disable or physically block debug pads
- **Tags**: PCIe, LPC, Debug Exploit

## MIPI Interface Eavesdropping on Touchscreen

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Touchscreen Device
- **Vulnerability**: Unprotected MIPI signal lines
- **MITRE**: T1056.001
- **Impact**: PIN theft, screen data spying
- **Tools**: Logic analyzer, fine probes
- **Scenario**: Tapping into MIPI (display/touch) lines to record user activity.
- **Attack Steps**: Step 1: Open device (tablet or HMI) gently.Step 2: Locate MIPI data lines from touchscreen.Step 3: Attach fine probes to CLK and D0 lines.Step 4: Record signals and decode finger touches.Step 5: Reconstruct passcodes or gestures.Step 6: Remove probes and reseal.
- **Detection**: Video artifact anomalies
- **Solution**: Secure physical enclosure
- **Tags**: MIPI, Touchscreen Spy

## SPI NOR Flash Override on Medical Device

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Medical Reader
- **Vulnerability**: Writable SPI firmware
- **MITRE**: T1565.002
- **Impact**: Fake results, medical data fraud
- **Tools**: Flash programmer, hex editor
- **Scenario**: Reflashing firmware on medical reader device via SPI port to spoof results.
- **Attack Steps**: Step 1: Identify and open the target medical device (e.g., glucose reader).Step 2: Locate SPI NOR flash chip (typically Winbond, Macronix).Step 3: Connect SPI programmer and dump original firmware.Step 4: Modify calibration or output logic.Step 5: Reflash with altered firmware and reboot.Step 6: Device now gives manipulated results.
- **Detection**: Calibration mismatch logs
- **Solution**: Firmware signing and tamper protection
- **Tags**: SPI, Medical Hack

## EmMC Chip Swap on Android Device

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Android Phone
- **Vulnerability**: Physical chip tampering possible
- **MITRE**: T1005
- **Impact**: Bypass FRP and access user data
- **Tools**: Hot air rework station, emMC reader
- **Scenario**: Swapping encrypted emMC chip with cloned one to access another phone’s data.
- **Attack Steps**: Step 1: Power off and open target Android device.Step 2: Carefully desolder emMC chip (using tweezers + hot air).Step 3: Replace with cloned chip from same model.Step 4: Power on device and extract user data.Step 5: Revert to original chip after use.Step 6: Clean board and reassemble.
- **Detection**: Boot logs, hardware ID change
- **Solution**: Encrypt with hardware binding
- **Tags**: eMMC, Chip Swap, Mobile Hack

## LVDS Tap Attack on Laptop Display

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Laptop
- **Vulnerability**: Exposed LVDS signal lines
- **MITRE**: T1056.001
- **Impact**: Visual data leak (passwords, chats)
- **Tools**: Logic Analyzer, Fine Probes, Screwdriver
- **Scenario**: Attacker taps into LVDS cable between motherboard and screen to eavesdrop display data.
- **Attack Steps**: Step 1: Unscrew laptop bezel and locate LVDS cable.Step 2: Use fine probes to tap into differential pairs.Step 3: Connect to logic analyzer to capture screen frames.Step 4: Decode and reconstruct data using software.Step 5: View display content in real time.Step 6: Remove probes and close panel.
- **Detection**: Screen artifacts, loose cable logs
- **Solution**: Encrypt screen output or shield cables
- **Tags**: LVDS, Laptop Spy, Display Tap

## UART Root Access on Wi-Fi Camera

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Wi-Fi Camera
- **Vulnerability**: Unlocked UART shell
- **MITRE**: T1204.002
- **Impact**: Surveillance control, credential reset
- **Tools**: UART cable, Putty
- **Scenario**: Gaining shell access to a Wi-Fi surveillance camera via UART debug port.
- **Attack Steps**: Step 1: Open camera casing.Step 2: Identify UART pins (often near antenna or SoC).Step 3: Connect UART-to-USB cable to TX, RX, GND.Step 4: Launch Putty and observe boot logs.Step 5: Press Enter when prompted, drop to root shell.Step 6: View camera recordings or reset password.
- **Detection**: Serial console logs
- **Solution**: Lock UART post-production
- **Tags**: Camera, UART Exploit

## Ethernet Debug Port Injection on IoT Hub

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Gateway / Hub
- **Vulnerability**: Unauthenticated Ethernet debug
- **MITRE**: T0869
- **Impact**: Full remote control via LAN
- **Tools**: Laptop, Ethernet cable, Packet crafter (Scapy)
- **Scenario**: Exploiting unfiltered Ethernet debug port to inject admin commands.
- **Attack Steps**: Step 1: Locate unused Ethernet port marked “DEBUG” or unlabeled.Step 2: Connect laptop and run Wireshark to capture traffic.Step 3: Send crafted admin commands using Scapy.Step 4: Trigger firmware upgrade or config dump.Step 5: Extract or manipulate settings.Step 6: Disconnect and restore physical condition.
- **Detection**: Debug packet logs
- **Solution**: Block/disable debug ports physically
- **Tags**: IoT, Ethernet Debug, Network Injection

## I2C EEPROM Clone Attack on RFID Card Reader

- **Attack Type**: Hardware Interface Exploitation
- **Target**: RFID Card Reader
- **Vulnerability**: Unencrypted EEPROM cloneable
- **MITRE**: T1555.004
- **Impact**: Credential clone, unauthorized access
- **Tools**: I2C clip reader, EEPROM programmer
- **Scenario**: Copying I2C EEPROM chip of a reader to create a clone with the same authentication logic.
- **Attack Steps**: Step 1: Unscrew reader and find EEPROM chip (e.g., 24C64).Step 2: Connect clip to reader.Step 3: Use software to dump contents.Step 4: Flash dump onto new EEPROM.Step 5: Insert EEPROM into clone reader device.Step 6: Test authentication success.
- **Detection**: Cloning logs, serial mismatch
- **Solution**: Encrypt EEPROM, bind to hardware ID
- **Tags**: EEPROM, RFID Clone

## Capacitive Touch I2C Injection

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Mobile Device / Tablet
- **Vulnerability**: Unprotected I2C touch interface
- **MITRE**: T1056.001
- **Impact**: Screen unlock, fake UI input
- **Tools**: Raspberry Pi, I2C sniffer/spoofer
- **Scenario**: Injecting fake touch events by spoofing I2C messages to a touchscreen controller.
- **Attack Steps**: Step 1: Access touch controller board.Step 2: Disconnect real touch sensor or place device inline.Step 3: Use Pi to sniff real traffic first.Step 4: Replay or craft I2C messages mimicking touch.Step 5: Unlock screen or press virtual buttons.Step 6: Power off and restore original config.
- **Detection**: Gesture anomalies
- **Solution**: Validate touch source, secure channel
- **Tags**: I2C, Touch Injection, Replay

## SATA Debug Access on Workstation

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Workstation
- **Vulnerability**: Active debug jumper
- **MITRE**: T0857
- **Impact**: Deep system reconfiguration
- **Tools**: Jumper pins, BIOS config tool
- **Scenario**: Using SATA debug jumper to access hidden manufacturer functions.
- **Attack Steps**: Step 1: Power off workstation and open case.Step 2: Locate SATA debug jumper (check label or documentation).Step 3: Short debug jumper pins.Step 4: Power on system and access hidden BIOS/debug menu.Step 5: Modify settings or flash debug firmware.Step 6: Reboot and remove jumper.
- **Detection**: Boot logs, POST errors
- **Solution**: Disable debug boot or fuse permanently
- **Tags**: SATA Debug, BIOS Hack

## Unsecured FPGA JTAG Interface

- **Attack Type**: Hardware Interface Exploitation
- **Target**: FPGA Device
- **Vulnerability**: Unlocked JTAG interface
- **MITRE**: T0859
- **Impact**: Circuit-level logic manipulation
- **Tools**: JTAG debugger (Xilinx), JTAG cable
- **Scenario**: Accessing and modifying FPGA behavior using JTAG pins.
- **Attack Steps**: Step 1: Open FPGA-powered device.Step 2: Identify JTAG port (TDI, TDO, TCK, TMS).Step 3: Connect JTAG cable.Step 4: Use Xilinx tools to read logic configuration.Step 5: Modify or inject new logic (e.g., bypass logic gate).Step 6: Apply and reboot device.
- **Detection**: Logic pattern mismatch
- **Solution**: Fuse JTAG or password-protect
- **Tags**: FPGA, Logic Gate Exploit

## NAND Chip Reader Attack on Smartwatch

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smartwatch
- **Vulnerability**: Unencrypted NAND memory
- **MITRE**: T1005
- **Impact**: User data leak
- **Tools**: Hot air gun, NAND reader, tweezers
- **Scenario**: Dumping NAND memory of a smartwatch to extract app data and saved credentials.
- **Attack Steps**: Step 1: Carefully open the smartwatch using prying tool.Step 2: Locate NAND memory chip and desolder it using hot air.Step 3: Place chip in NAND reader and use software to dump data.Step 4: Browse through data to find SMS, login tokens, or app data.Step 5: Store dump, reattach chip, and reassemble device.
- **Detection**: Boot loop, touch failure
- **Solution**: Encrypt NAND, secure boot
- **Tags**: NAND, Smartwatch Dump

## Unlocked Debug Port in Electronic Voting Machine

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Voting Machine
- **Vulnerability**: Accessible debug shell
- **MITRE**: T0887
- **Impact**: Tampering with voting records
- **Tools**: UART cable, terminal software
- **Scenario**: Attacker accesses system via serial debug port on EVM to view and manipulate stored votes.
- **Attack Steps**: Step 1: Open machine casing and find debug serial port.Step 2: Connect UART to USB adapter and open terminal.Step 3: Monitor output logs during boot.Step 4: Access menu or shell if presented.Step 5: Read stored vote data or trigger reset.Step 6: Close and repackage EVM.
- **Detection**: Boot mismatch or data audit
- **Solution**: Disable debug, audit trail logs
- **Tags**: EVM, UART Debug, Election Security

## JTAG Injection on Consumer Drone

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Consumer Drone
- **Vulnerability**: Firmware not encrypted or signed
- **MITRE**: T1565.002
- **Impact**: Bypass safety and geo-fencing
- **Tools**: JTAG programmer, solder kit, OpenOCD
- **Scenario**: Injecting new firmware to bypass flight restrictions (e.g., no-fly zones).
- **Attack Steps**: Step 1: Disassemble drone body to reveal PCB.Step 2: Locate and solder wires to JTAG pins.Step 3: Connect programmer and use OpenOCD.Step 4: Dump firmware and patch restrictions.Step 5: Flash modified firmware and reboot drone.Step 6: Test bypassed restrictions (e.g., fly in restricted area).
- **Detection**: GPS log anomalies
- **Solution**: Enforce signed firmware, fuse JTAG
- **Tags**: Drone, No-Fly Zone Bypass

## BIOS Password Reset via CMOS Chip Flashing

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Laptop
- **Vulnerability**: BIOS password stored insecurely
- **MITRE**: T1552.004
- **Impact**: Unauthorized BIOS/UEFI access
- **Tools**: SPI flasher, screwdriver, clip
- **Scenario**: Resetting BIOS password on laptop by reflashing CMOS memory using external flasher.
- **Attack Steps**: Step 1: Open laptop and locate CMOS chip (8-pin near battery).Step 2: Connect clip to chip and flasher tool.Step 3: Dump firmware and look for password hash.Step 4: Replace or blank password region.Step 5: Reflash firmware and reboot system.Step 6: BIOS loads without password prompt.
- **Detection**: BIOS boot log audit
- **Solution**: Hash BIOS settings or TPM tie-in
- **Tags**: BIOS, CMOS, Password Bypass

## Wi-Fi Credential Extraction from Flash on IoT Plug

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart Plug
- **Vulnerability**: Plaintext Wi-Fi storage
- **MITRE**: T1555.004
- **Impact**: Credential leakage
- **Tools**: SOIC clip, CH341A programmer
- **Scenario**: Extracting Wi-Fi credentials from IoT smart plug's SPI flash.
- **Attack Steps**: Step 1: Open smart plug shell and locate SPI flash chip.Step 2: Clip SOIC onto chip and connect to CH341A.Step 3: Use flashrom to dump contents.Step 4: Search dump for SSID and password strings.Step 5: Save data and remove clip.Step 6: Reassemble device for stealth.
- **Detection**: Unusual Wi-Fi access logs
- **Solution**: Store creds encrypted, use secure enclave
- **Tags**: IoT, SPI Flash, Wi-Fi Leak

## SPI Flash Swap Attack on Router

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Router
- **Vulnerability**: Firmware not signed
- **MITRE**: T1542.003
- **Impact**: Remote control of network
- **Tools**: Hot air rework station, pre-flashed chip
- **Scenario**: Replacing router's SPI flash chip with one containing a custom backdoored OS.
- **Attack Steps**: Step 1: Power off router and open enclosure.Step 2: Desolder SPI flash and remove.Step 3: Solder custom chip with malicious firmware.Step 4: Reboot router and check for access.Step 5: Confirm attacker remote shell works.Step 6: Close case and hide modification.
- **Detection**: Router config logs
- **Solution**: Enforce secure boot and chip lock
- **Tags**: Router, SPI Swap, Firmware Hack

## IR Debug Interface Abuse on TV Remote

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart TV
- **Vulnerability**: Exposed IR service commands
- **MITRE**: T0886
- **Impact**: Device configuration manipulation
- **Tools**: Universal IR remote, code list
- **Scenario**: Abusing undocumented IR commands to access hidden service modes.
- **Attack Steps**: Step 1: Power on TV and point universal IR remote.Step 2: Enter service mode key combo (e.g., Mute > 1 > 8 > 2 > Power).Step 3: Menu opens with diagnostic access.Step 4: Change region, reset PINs, enable hidden settings.Step 5: Exit mode and power cycle TV.Step 6: Store remote or discard logs.
- **Detection**: Event logs, OSD flags
- **Solution**: Restrict service access, secure remote codes
- **Tags**: IR, Service Mode, TV Exploit

## Bypass via Magnet Trigger on Sensor Device

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Magnetic Sensor
- **Vulnerability**: Easy spoofing via magnet
- **MITRE**: T0866
- **Impact**: Physical security bypass
- **Tools**: Small neodymium magnet
- **Scenario**: Using external magnet to trick reed/magnetic sensor into unauthorized states.
- **Attack Steps**: Step 1: Identify sensor (e.g., door/window sensor).Step 2: Place magnet near sensor area.Step 3: Watch LED or alert status switch (open → closed).Step 4: Leave door open while sensor reports it as closed.Step 5: Remove magnet when needed.Step 6: Sensor logs remain unchanged.
- **Detection**: Rare discrepancy reports
- **Solution**: Shield sensor, detect magnetic tampering
- **Tags**: Magnetic, Reed Sensor, Bypass

## UART Access to Medical Infusion Pump

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Medical Device
- **Vulnerability**: Unauthenticated serial CLI
- **MITRE**: T0887
- **Impact**: Patient harm, data fraud
- **Tools**: UART cable, Putty
- **Scenario**: Direct access to infusion pump console via UART to modify dosage logs.
- **Attack Steps**: Step 1: Carefully unscrew the pump casing.Step 2: Locate UART headers.Step 3: Connect TX/RX/GND to USB converter.Step 4: Launch terminal and observe logs.Step 5: Interrupt boot or access CLI.Step 6: Alter dosage settings/logs and exit.
- **Detection**: Medical audit trail mismatch
- **Solution**: Disable UART, use logging controller
- **Tags**: UART, Medical, Infusion Exploit

## Open Debug Port on Industrial HVAC Controller

- **Attack Type**: Hardware Interface Exploitation
- **Target**: HVAC / PLC
- **Vulnerability**: Active debug UART not disabled
- **MITRE**: T0880
- **Impact**: Environmental sabotage or manipulation
- **Tools**: UART cable, logic analyzer
- **Scenario**: Gaining root access on HVAC PLC via open debug port to modify temperature setpoints.
- **Attack Steps**: Step 1: Open HVAC controller panel.Step 2: Connect UART cable to exposed debug pins.Step 3: Observe startup logs and drop to shell.Step 4: Access config files or system binaries.Step 5: Change temp thresholds or schedules.Step 6: Reboot and reseal panel.
- **Detection**: Maintenance audit trails
- **Solution**: Disable debug in production
- **Tags**: HVAC, PLC, Debug Port

## eMMC Dump from Damaged Smartphone

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smartphone
- **Vulnerability**: Physical memory can be removed
- **MITRE**: T1005
- **Impact**: User privacy violation
- **Tools**: Heat gun, tweezers, eMMC reader
- **Scenario**: Attacker salvages user data by reading eMMC chip from a broken smartphone.
- **Attack Steps**: Step 1: Open broken phone and locate eMMC chip.Step 2: Use heat gun to safely remove chip.Step 3: Insert into eMMC reader and dump memory.Step 4: Search for SMS, images, or app data.Step 5: Store results and preserve chip for chain of custody.Step 6: Properly dispose of or reseal phone.
- **Detection**: Physical tamper detection (if any)
- **Solution**: Full-disk encryption, epoxy cover
- **Tags**: eMMC, Data Recovery, Smartphone

## CAN Bus Reprogramming via OBD-II

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Vehicle ECU
- **Vulnerability**: OBD-II allows reprogram without auth
- **MITRE**: T0890
- **Impact**: Malicious vehicle control
- **Tools**: OBD-II adapter, UDS software
- **Scenario**: Gaining access to internal car ECUs via OBD-II and reprogramming control logic.
- **Attack Steps**: Step 1: Connect laptop to car OBD-II port.Step 2: Launch UDS tool to send diagnostic sessions.Step 3: Unlock reprogramming mode on ECU.Step 4: Upload new firmware or modify parameters.Step 5: Confirm functionality (e.g., disable seatbelt alert).Step 6: Disconnect and restart vehicle.
- **Detection**: ECU firmware mismatch logs
- **Solution**: Secure ECU with re-auth & firewall
- **Tags**: CAN Bus, ECU Hack, Automotive

## Passive Tap on Audio Codec I2S Bus

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart Speaker / Mic Device
- **Vulnerability**: Unencrypted audio transmission
- **MITRE**: T1056.001
- **Impact**: Eavesdropping on private speech
- **Tools**: Logic analyzer, I2S decoder
- **Scenario**: Tapping into I2S bus between MCU and codec chip to eavesdrop audio.
- **Attack Steps**: Step 1: Open casing of device with mic/speaker (e.g., smart speaker).Step 2: Locate I2S signals (SCK, WS, SD).Step 3: Attach probes to lines and record data.Step 4: Decode captured I2S to extract raw audio.Step 5: Play or analyze conversation.Step 6: Remove probes and close device.
- **Detection**: Noises, power draw increase
- **Solution**: Encrypt or scramble audio bus
- **Tags**: I2S, Audio Spy, Codec Exploit

## RFID Key Emulator via Flash Dump

- **Attack Type**: Hardware Interface Exploitation
- **Target**: RFID Access Reader
- **Vulnerability**: Stored UID not encrypted or randomized
- **MITRE**: T1557
- **Impact**: Unauthorized area entry
- **Tools**: Flash reader, Proxmark3
- **Scenario**: Extracting key ID from RFID reader’s flash and emulating authorized tag.
- **Attack Steps**: Step 1: Open RFID reader and locate flash chip.Step 2: Dump memory using SOIC clip and flashrom.Step 3: Search for access key UID.Step 4: Program Proxmark3 with that UID.Step 5: Emulate card and test door access.Step 6: Remove traces and reseal reader.
- **Detection**: Access logs mismatch with physical ID
- **Solution**: Randomize UID per session
- **Tags**: RFID, UID Emulation, Flash Dump

## USB Debug Mode on Android TV Box

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Android TV Box
- **Vulnerability**: USB debug left enabled
- **MITRE**: T1059.004
- **Impact**: Persistent remote control
- **Tools**: OTG cable, ADB tool, Laptop
- **Scenario**: Exploiting USB OTG port to enable debug mode and gain root shell.
- **Attack Steps**: Step 1: Plug OTG cable into TV box.Step 2: Connect to laptop and detect ADB interface.Step 3: If enabled, use adb shell to get terminal.Step 4: Check for root and install payload.Step 5: Leave malware running in background.Step 6: Hide traces and disconnect.
- **Detection**: System log audit
- **Solution**: Disable ADB or require auth keys
- **Tags**: ADB, Android Box, USB Exploit

## EEPROM Tamper on Digital Thermostat

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Digital Thermostat
- **Vulnerability**: EEPROM not write-protected
- **MITRE**: T0886
- **Impact**: Environmental manipulation
- **Tools**: EEPROM writer, Hex editor
- **Scenario**: Changing target temperature range stored in EEPROM chip.
- **Attack Steps**: Step 1: Open thermostat case.Step 2: Connect EEPROM clip to chip.Step 3: Dump memory and look for temp limits.Step 4: Modify value in hex editor and reflash.Step 5: Confirm changes by rebooting thermostat.Step 6: Reset device log if necessary.
- **Detection**: Data out of range logs
- **Solution**: Protect EEPROM with CRC and fuse
- **Tags**: HVAC, EEPROM Exploit

## U-Boot Modification via SD Boot

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Linux Device
- **Vulnerability**: Bootloader writable and accessible
- **MITRE**: T1542.004
- **Impact**: Kernel-level control
- **Tools**: SD card, Hex editor, Boot image
- **Scenario**: Changing U-Boot bootloader on SD-booted device to load attacker kernel.
- **Attack Steps**: Step 1: Extract SD card from embedded device.Step 2: Mount on laptop and locate U-Boot file.Step 3: Modify bootargs to load custom kernel.Step 4: Save and reinsert card into device.Step 5: On boot, payload kernel is executed.Step 6: Reverse shell or access portal opens.
- **Detection**: Boot log analysis
- **Solution**: Lock boot args and use secure boot
- **Tags**: U-Boot, Kernel Injection

## SoC Boundary Scan Interface Attack

- **Attack Type**: Hardware Interface Exploitation
- **Target**: SoC-Based Device
- **Vulnerability**: Boundary scan not disabled
- **MITRE**: T0857
- **Impact**: Arbitrary hardware control
- **Tools**: Boundary scan tool, JTAG connector
- **Scenario**: Using JTAG boundary scan to read or write internal SoC registers.
- **Attack Steps**: Step 1: Identify JTAG port on SoC-based device.Step 2: Attach tool and detect pinout.Step 3: Use scan software to probe registers.Step 4: Modify register controlling GPIO or memory.Step 5: Test response, e.g., LED blink or file dump.Step 6: Remove tool and seal.
- **Detection**: Activity trace in scan logs
- **Solution**: Fuse or disable scan after QA
- **Tags**: JTAG, Boundary Scan

## HDMI CEC Injection for TV Hijack

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart TV
- **Vulnerability**: No CEC filtering or auth
- **MITRE**: T0880
- **Impact**: Denial of service, annoyance, takeover
- **Tools**: CEC tool (Pulse-Eight), HDMI cable
- **Scenario**: Sending crafted CEC commands via HDMI to control a connected smart TV.
- **Attack Steps**: Step 1: Connect CEC device to HDMI of target TV.Step 2: Use software to send commands like “Power Off”, “Source Change”, etc.Step 3: Observe behavior and capture screen data.Step 4: Loop malicious command (e.g., reset volume, disrupt streaming).Step 5: Disconnect after attack.Step 6: TV remains misconfigured.
- **Detection**: HDMI logs, remote logs
- **Solution**: Disable unused CEC commands
- **Tags**: HDMI CEC, TV Exploit

## Firmware Extraction from USB Flash Drive

- **Attack Type**: Hardware Interface Exploitation
- **Target**: USB Flash Drive
- **Vulnerability**: Unsigned controller firmware
- **MITRE**: T1027.002
- **Impact**: Stealth malware deployment
- **Tools**: Chip-off tools, NAND reader, hex editor
- **Scenario**: Extracting firmware from controller chip of USB flash to understand behavior or implant backdoor.
- **Attack Steps**: Step 1: Break open USB flash and remove controller chip.Step 2: Use NAND reader to dump firmware.Step 3: Analyze firmware for hidden partitions, malware.Step 4: Optionally inject new boot sector with payload.Step 5: Reassemble USB and test.Step 6: Use USB as covert tool.
- **Detection**: Unusual behavior, AV alerts
- **Solution**: Signed firmware, hardware-based trust
- **Tags**: USB Firmware, Chip-Off Attack

## Malicious USB HID Payload Injection

- **Attack Type**: Removable Media - HID Attack
- **Target**: Workstations, PCs
- **Vulnerability**: Unlocked USB ports, no endpoint protection
- **MITRE**: T1204.002 - Malicious USB Device
- **Impact**: Full compromise of system, backdoor installation
- **Tools**: Rubber Ducky, MalDuino
- **Scenario**: An attacker uses a USB device that acts like a keyboard to inject commands into a target system
- **Attack Steps**: Step 1: Buy a USB Rubber Ducky or MalDuino online. Step 2: Use its software to write a script. Example: open Notepad and type commands. Step 3: Plug the USB into a victim’s unattended computer. Step 4: The device automatically types commands like opening a terminal, downloading malware, or stealing files. Step 5: Device finishes and ejects like nothing happened.
- **Detection**: USB activity logging, endpoint monitoring
- **Solution**: Disable unused USB ports, use USB whitelisting
- **Tags**: USB HID, Rubber Ducky, Physical Access

## Data Exfiltration via Modified USB Drive

- **Attack Type**: Removable Media - Data Theft
- **Target**: Laptops, Office PCs
- **Vulnerability**: AutoRun enabled, lack of USB monitoring
- **MITRE**: T1056 - Input Capture
- **Impact**: Unauthorized file theft
- **Tools**: USBDriveby, Bash Bunny
- **Scenario**: A USB stick automatically copies files when inserted into a PC, without needing user interaction
- **Attack Steps**: Step 1: Modify a USB using tools like Bash Bunny to act like both a keyboard and storage. Step 2: Write a payload script to silently copy Documents folder. Step 3: Insert USB into victim machine. Step 4: The script runs automatically and copies files to hidden folder. Step 5: Remove USB and leave – data is exfiltrated.
- **Detection**: Monitor file access logs, DLP tools
- **Solution**: Disable AutoRun, encrypt sensitive files
- **Tags**: Data Theft, USB, Exfiltration

## JTAG Interface Debugging Exploit

- **Attack Type**: Hardware Debug Port Exploit
- **Target**: Routers, Smart Devices
- **Vulnerability**: Exposed debug interfaces, no protection
- **MITRE**: T1602 - Data from Local System
- **Impact**: Reverse engineering, firmware tampering
- **Tools**: JTAGulator, OpenOCD, Bus Pirate
- **Scenario**: Attacker gains physical access to JTAG interface and dumps memory or modifies firmware
- **Attack Steps**: Step 1: Identify device’s board and look for JTAG pinout (may be labeled or not). Step 2: Connect a JTAG debugger like JTAGulator or Bus Pirate. Step 3: Use OpenOCD software to connect and scan memory. Step 4: Dump firmware from the device and analyze it on PC. Step 5: Modify firmware or search for credentials in dump.
- **Detection**: Hardware probes, anomaly firmware hash
- **Solution**: Disable or fuse debug ports
- **Tags**: IoT, Firmware, JTAG, Dump

## UART Serial Access for Admin Shell

- **Attack Type**: Serial Console Attack
- **Target**: Embedded Devices
- **Vulnerability**: Exposed UART, weak/default creds
- **MITRE**: T1059 - Command and Scripting
- **Impact**: Root shell access, device takeover
- **Tools**: UART to USB Cable, PuTTY
- **Scenario**: A hacker uses exposed UART pins on device PCB to get a root shell on embedded Linux system
- **Attack Steps**: Step 1: Open the device and identify UART pins (usually 3 or 4 pins labeled TX, RX, GND). Step 2: Connect USB-UART cable (correctly connect TX to RX, RX to TX, GND to GND). Step 3: Open terminal software (e.g., PuTTY) and connect at right baud rate (often 115200). Step 4: On boot, the console shows Linux boot logs and may offer a login prompt. Step 5: Try common usernames/passwords (like root, admin, 1234) to gain access.
- **Detection**: Serial line monitoring (rare)
- **Solution**: Disable UART, use secure boot
- **Tags**: UART, Linux, Serial Access

## Evil Maid Attack with USB Firmware Reflash

- **Attack Type**: BIOS Firmware Implant
- **Target**: Laptops, Desktops
- **Vulnerability**: Unprotected BIOS flashing, no firmware validation
- **MITRE**: T1542.001 - System Firmware
- **Impact**: Persistent root access
- **Tools**: FlashROM, SPI Programmer
- **Scenario**: An attacker reflashes laptop BIOS using USB stick with malicious firmware to gain stealthy persistence
- **Attack Steps**: Step 1: Build or download a malicious BIOS firmware. Step 2: Use SPI flasher tool (like CH341A) to read original BIOS chip and backup. Step 3: Flash the modified BIOS using hardware clip on motherboard SPI chip. Step 4: Reboot the system – BIOS now has backdoor/rootkit that survives reinstall. Step 5: Attacker now has stealthy access whenever needed.
- **Detection**: UEFI/BIOS integrity monitoring
- **Solution**: BIOS lock, firmware signing
- **Tags**: Evil Maid, BIOS, Firmware

## Keystroke Logging via USB Charger Adapter

- **Attack Type**: USB Data Interception
- **Target**: Office PCs, Kiosks
- **Vulnerability**: Untrusted USB peripherals
- **MITRE**: T1056.001 - Keylogging
- **Impact**: Credential theft, privacy breach
- **Tools**: KeySweeper, ESP8266
- **Scenario**: Malicious USB charger that logs keyboard input when plugged into the same system
- **Attack Steps**: Step 1: Attacker places a fake USB charger (KeySweeper) in a public area or victim’s desk. Step 2: Victim plugs in their keyboard through the charger unknowingly. Step 3: The adapter silently records keystrokes (e.g., passwords, emails). Step 4: Logs are stored internally or sent wirelessly to attacker. Step 5: Attacker retrieves data physically or remotely.
- **Detection**: USB traffic monitoring (rare)
- **Solution**: Use only trusted USB chargers
- **Tags**: USB charger, HID log, KeySweeper

## PCI Express (PCIe) DMA Attack

- **Attack Type**: Direct Memory Access
- **Target**: Desktop Workstations
- **Vulnerability**: Unrestricted DMA access
- **MITRE**: T1048 - Exfiltration over Alternate Protocol
- **Impact**: Memory dump, credential theft
- **Tools**: PCILeech, Screamer
- **Scenario**: PCIe device used to inject code or read memory via DMA from RAM bypassing OS
- **Attack Steps**: Step 1: Get access to unattended desktop/laptop with PCIe slot. Step 2: Insert PCILeech-compatible device (Screamer, FPGA). Step 3: Connect device to attack laptop. Step 4: Run PCILeech software to read memory, dump credentials, inject shellcode. Step 5: Remove device without any trace.
- **Detection**: DMA logging, BIOS lockdown
- **Solution**: Disable external DMA, use IOMMU
- **Tags**: PCIe, DMA, RAM Read

## HDMI Keylogger via EDID Exploit

- **Attack Type**: Display Interface Abuse
- **Target**: Work PCs, Laptops
- **Vulnerability**: HDMI EDID not validated
- **MITRE**: T1113 - Screen Capture
- **Impact**: Credential theft via screen spying
- **Tools**: Modified HDMI Tap
- **Scenario**: HDMI cable with modified EDID captures keystrokes displayed on screen overlays
- **Attack Steps**: Step 1: Replace user’s HDMI cable with malicious HDMI cable (or dongle) with modified EDID. Step 2: Cable captures screen buffer overlays showing typed passwords (like browser autofills, login fields). Step 3: Extract image data from HDMI tap. Step 4: Use OCR tools to recover keystrokes. Step 5: Use data to gain access to accounts.
- **Detection**: Monitor for unknown HDMI dongles
- **Solution**: Use secured cabling, EDID lockdown
- **Tags**: HDMI, EDID, Visual Exfil

## EEPROM Dump via I2C Interface

- **Attack Type**: Memory Dump
- **Target**: Smart Devices, POS
- **Vulnerability**: Exposed memory interface
- **MITRE**: T1005 - Data from Local System
- **Impact**: Secret leakage, device tampering
- **Tools**: Bus Pirate, Logic Analyzer
- **Scenario**: Attacker extracts configuration or secrets from I2C EEPROM chip on embedded board
- **Attack Steps**: Step 1: Open device and identify EEPROM chip connected via I2C. Step 2: Connect Bus Pirate or logic analyzer to SDA/SCL pins. Step 3: Use I2C sniffing commands to dump EEPROM content. Step 4: Analyze the dump on PC – may contain credentials, WiFi keys, license keys. Step 5: Optionally write back modified values.
- **Detection**: PCB interface shielding
- **Solution**: Encrypt EEPROM contents
- **Tags**: I2C, EEPROM, Key Extraction

## USB Network Adapter Spoofing

- **Attack Type**: USB-to-Ethernet MITM
- **Target**: Laptops, Desktops
- **Vulnerability**: Auto-configured network adapters
- **MITRE**: T1557.001 - Adversary-in-the-Middle
- **Impact**: Session hijack, malware delivery
- **Tools**: USB Armory, PoisonTap
- **Scenario**: USB device impersonates network adapter to do man-in-the-middle
- **Attack Steps**: Step 1: Plug USB device (PoisonTap or USB Armory) into victim’s system. Step 2: The OS installs it as a network adapter. Step 3: Device routes all network traffic through itself. Step 4: It intercepts or redirects HTTP requests, injects cookies. Step 5: Attacker gets access to session data or injects malware.
- **Detection**: Monitor new interfaces
- **Solution**: Block unknown USB NICs
- **Tags**: USB NIC, MITM, Cookie Hijack

## Fake USB Mass Storage Attack

- **Attack Type**: Storage Emulation Attack
- **Target**: Office PCs
- **Vulnerability**: User curiosity, misleading file icons
- **MITRE**: T1204.001 - Malicious File
- **Impact**: Remote access, ransomware
- **Tools**: Arduino, Digispark
- **Scenario**: USB stick that pretends to be a hard drive but contains payloads
- **Attack Steps**: Step 1: Build or buy a Digispark-based USB with preloaded payload. Step 2: Insert it into the target system. Step 3: Appears as a USB drive, user opens file like invoice.pdf.exe. Step 4: File executes malware and connects back to attacker. Step 5: Attacker controls target remotely.
- **Detection**: AV logs, EDR alerts
- **Solution**: Block executables on USB
- **Tags**: USB, Payload, Autorun

## Modified Wireless Mouse Dongle Attack

- **Attack Type**: HID Injection via RF
- **Target**: PCs using wireless mouse
- **Vulnerability**: Unencrypted wireless HID
- **MITRE**: T1557 - Adversary-in-the-Middle
- **Impact**: Command injection, malware
- **Tools**: Crazyradio PA
- **Scenario**: Inject keystrokes via unencrypted RF dongle (MouseJack)
- **Attack Steps**: Step 1: Identify victim using wireless mouse with USB dongle. Step 2: Use Crazyradio PA and MouseJack script to pair with dongle. Step 3: Send fake keystrokes to open terminal, download malware. Step 4: Hide terminal, attacker gains access. Step 5: Victim unaware mouse dongle was exploited.
- **Detection**: HID scan tools
- **Solution**: Use encrypted HID devices
- **Tags**: MouseJack, RF HID

## Supply Chain Backdoored USB Cable

- **Attack Type**: Implanted Hardware
- **Target**: Mobile Phones, PCs
- **Vulnerability**: Unverified cables
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Stealth remote control
- **Tools**: O.MG Cable, WiFi implant
- **Scenario**: USB cable that functions normally but has backdoor implant
- **Attack Steps**: Step 1: Buy or plant malicious cable (e.g., O.MG) with WiFi chip inside. Step 2: Victim uses it to charge phone or transfer files. Step 3: Attacker connects to WiFi module in cable remotely. Step 4: Executes commands, transfers files without user noticing. Step 5: Cable continues functioning normally.
- **Detection**: RF monitoring, USB activity
- **Solution**: Buy cables from trusted sources
- **Tags**: O.MG Cable, Supply Chain

## RFID Skimming via USB Reader

- **Attack Type**: Proximity Credential Theft
- **Target**: Access Card Systems
- **Vulnerability**: Unprotected RFID protocols
- **MITRE**: T1557.002 - Wireless Sniffing
- **Impact**: Unauthorized access
- **Tools**: Proxmark3, RFIDler
- **Scenario**: USB RFID reader clones contactless card via proximity access
- **Attack Steps**: Step 1: Connect Proxmark3 to laptop. Step 2: Approach victim with card in pocket or badge. Step 3: Use command hf 14a sniff to read UID. Step 4: Clone UID to blank card using hf clone. Step 5: Use cloned card to access door/building.
- **Detection**: Physical security, RFID audit
- **Solution**: Use encrypted RFID tech
- **Tags**: RFID, Proxmark, Skim

## Malicious Firmware Flash via USB Blaster

- **Attack Type**: FPGA/CPLD Reprogramming
- **Target**: Industrial Devices, Custom Hardware
- **Vulnerability**: Unlocked JTAG/SPI interfaces
- **MITRE**: T1601 - Modify System Firmware
- **Impact**: Device hijack or sabotage
- **Tools**: USB Blaster, Quartus
- **Scenario**: USB Blaster used to reprogram FPGAs with malicious logic
- **Attack Steps**: Step 1: Connect USB Blaster to FPGA development board. Step 2: Use Quartus Programmer to read and save current config. Step 3: Modify logic or load malicious bitstream. Step 4: Write the modified firmware to the chip. Step 5: Device now behaves with hidden backdoor or modified logic.
- **Detection**: Firmware hash mismatch
- **Solution**: Secure boot, signed bitstreams
- **Tags**: FPGA, USB Blaster

## Keystroke Injection via Bluetooth Dongle

- **Attack Type**: HID Injection via BT
- **Target**: PCs with BT dongles
- **Vulnerability**: Insecure Bluetooth pairing
- **MITRE**: T1557 - MITM
- **Impact**: Command execution, malware injection
- **Tools**: BlueMaPa, Ubertooth
- **Scenario**: Attacker connects to insecure Bluetooth keyboard dongle and injects keystrokes
- **Attack Steps**: Step 1: Scan for Bluetooth keyboards using Ubertooth. Step 2: Identify dongle with weak pairing (no authentication). Step 3: Connect using spoofed device ID. Step 4: Send malicious keystrokes (open terminal, run malware). Step 5: Disconnect — victim remains unaware.
- **Detection**: Bluetooth traffic analysis
- **Solution**: Use BT with secure pairing
- **Tags**: Bluetooth HID, Keystroke, MITM

## SD Card Payload via Hidden Partition

- **Attack Type**: Storage Abuse
- **Target**: Laptops, Cameras
- **Vulnerability**: Hidden partitions go unnoticed
- **MITRE**: T1204.001 - Malicious File
- **Impact**: Stealth malware installation
- **Tools**: DiskPart, Hidden Partition Creator
- **Scenario**: SD card with hidden malware in unused partitions, triggered when inserted
- **Attack Steps**: Step 1: Use DiskPart to create a hidden partition on SD card. Step 2: Place malicious script (autorun.inf, payload.bat). Step 3: Insert SD card into target device. Step 4: Hidden partition mounts automatically or trick user into opening. Step 5: Script runs silently and infects system.
- **Detection**: Disk monitor tools
- **Solution**: Disable autorun, scan all partitions
- **Tags**: SD Card, Hidden Payload

## Malicious USB Fan Attack

- **Attack Type**: USB HID Disguised Device
- **Target**: Office PCs
- **Vulnerability**: Trust in functional USB gadgets
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Malware delivery via gift
- **Tools**: Digispark, USB Rubber Ducky
- **Scenario**: Attacker gifts or drops a USB desk fan with hidden attack chip
- **Attack Steps**: Step 1: Modify small USB fan to include Digispark board. Step 2: Write script to open terminal and download malware. Step 3: Victim plugs in fan to USB port for cooling. Step 4: Payload runs as keyboard input. Step 5: Malware installed — fan works normally.
- **Detection**: Monitor new USB devices
- **Solution**: Use USB device control policies
- **Tags**: Fan, Office Gadget, Social Engineering

## Reverse Shell via USB Tethered Android

- **Attack Type**: ADB Interface Exploit
- **Target**: Windows/Linux PCs
- **Vulnerability**: Enabled USB Debugging
- **MITRE**: T1059 - Command & Script
- **Impact**: Full system shell access
- **Tools**: ADB, Termux, Netcat
- **Scenario**: Android phone connected via USB with debugging enabled gives shell access to attacker
- **Attack Steps**: Step 1: Connect your phone to victim PC via USB. Step 2: Enable USB Debugging on the phone. Step 3: On victim PC, install ADB and detect connected phone. Step 4: Use ADB to execute reverse shell payload. Step 5: Attacker gains shell access to PC via phone link.
- **Detection**: USB debugging alerts
- **Solution**: Disable ADB on mobile
- **Tags**: ADB, Android, Reverse Shell

## Bootloader Unlock via UART & SD Card

- **Attack Type**: Firmware Bypass
- **Target**: IoT Gateways, IP Cameras
- **Vulnerability**: Open UART, unprotected bootloader
- **MITRE**: T1542.001 - System Firmware
- **Impact**: Full system control, bypass vendor lock
- **Tools**: UART Cable, MicroSD
- **Scenario**: Using UART interface and SD card to unlock and modify bootloader
- **Attack Steps**: Step 1: Open device casing and identify UART pins. Step 2: Connect to UART using USB-to-Serial cable. Step 3: Insert SD card with custom bootloader script. Step 4: Reboot device — script intercepts boot via UART. Step 5: Access bootloader menu, unlock, and flash custom firmware.
- **Detection**: Monitor UART ports
- **Solution**: Secure boot enforcement
- **Tags**: Bootloader, UART, Flash

## USB Device That Bypasses Air-Gapped Systems

- **Attack Type**: Covert Data Channel
- **Target**: Air-gapped PCs
- **Vulnerability**: Signal-based side channels
- **MITRE**: T1020 - Automated Exfiltration
- **Impact**: Leaks from isolated systems
- **Tools**: USBee, PowerHammer
- **Scenario**: A USB device writes hidden messages into system logs for later extraction
- **Attack Steps**: Step 1: Connect USB that sends electromagnetic signals via USB bus. Step 2: On compromised air-gapped system, use hidden script to encode data (e.g., keylogs) into system voltage changes. Step 3: Attacker reads signals from nearby device (like radio or oscilloscope). Step 4: Decode into readable text. Step 5: No internet/USB file transfer required.
- **Detection**: Unusual EMI emissions
- **Solution**: Shielded rooms, no USB policy
- **Tags**: Air-gap Bypass, USBee

## USB-to-SATA Disk Cloning via Live Linux

- **Attack Type**: Physical Data Theft
- **Target**: Desktops, Laptops
- **Vulnerability**: Physical access to drives
- **MITRE**: T1005 - Data from Local System
- **Impact**: Full disk clone
- **Tools**: Live Kali, Clonezilla
- **Scenario**: Attacker clones full disk using USB-to-SATA adapter and bootable USB
- **Attack Steps**: Step 1: Attacker plugs in bootable USB with Linux. Step 2: Boot into Linux without touching local OS. Step 3: Connect USB-to-SATA adapter to victim's internal drive. Step 4: Run Clonezilla to copy full disk to external drive. Step 5: Shutdown — target system looks untouched.
- **Detection**: Physical access logs (BIOS audit)
- **Solution**: BIOS boot password
- **Tags**: Disk Cloning, SATA USB

## Data Theft via USB Phone Charging Port

- **Attack Type**: Juice Jacking
- **Target**: Mobile Phones
- **Vulnerability**: USB data lines exposed
- **MITRE**: T1029 - Scheduled Transfer
- **Impact**: Contact and file theft
- **Tools**: USB Sniffer, JuiceJack Cable
- **Scenario**: Attacker modifies public phone charging port to exfiltrate data from phones
- **Attack Steps**: Step 1: Install malicious USB charger in public location. Step 2: Victim plugs in phone to charge. Step 3: Charger’s hidden data lines activate. Step 4: Copies images, contacts, and messages from phone. Step 5: Attacker retrieves data later via storage module.
- **Detection**: Charge-only USB cables
- **Solution**: USB data blocker
- **Tags**: Juice Jacking, Public USB

## Custom Microcontroller-Based Keylogger

- **Attack Type**: Inline USB Keylogging
- **Target**: Office PCs
- **Vulnerability**: Lack of inline device monitoring
- **MITRE**: T1056.001 - Keylogging
- **Impact**: Credential leakage
- **Tools**: ATtiny85, USB Sniffer
- **Scenario**: Small microcontroller captures keystrokes between keyboard and PC
- **Attack Steps**: Step 1: Build a small inline USB device using ATtiny85. Step 2: Plug keyboard into this device, then into PC. Step 3: Device captures and logs all keystrokes to flash memory. Step 4: Remove device after a few hours. Step 5: Plug into attacker's PC to extract keystrokes.
- **Detection**: USB inline scanning
- **Solution**: Secure keyboards, monitor chains
- **Tags**: Inline USB, Microcontroller

## USB Wi-Fi Adapter for Rogue AP Attack

- **Attack Type**: Network Impersonation
- **Target**: Laptops, Phones
- **Vulnerability**: Unsecured WiFi auto-connect
- **MITRE**: T1557.003 - Rogue Access Point
- **Impact**: Credential theft, phishing
- **Tools**: Alfa WiFi, Airbase-ng
- **Scenario**: A USB Wi-Fi adapter sets up fake hotspot to steal credentials
- **Attack Steps**: Step 1: Plug in WiFi USB adapter to attacker laptop. Step 2: Use airbase-ng to create fake access point (same SSID as trusted network). Step 3: Victim unknowingly connects. Step 4: Capture login credentials via phishing page. Step 5: Disconnect victim or redirect to real site.
- **Detection**: WiFi probe detection
- **Solution**: Disable auto-connect, use WPA3
- **Tags**: Rogue AP, Evil Twin, WiFi USB

## SPI Flash Memory Dump Attack

- **Attack Type**: Firmware Dump
- **Target**: IoT Devices, Routers
- **Vulnerability**: Unprotected SPI interface
- **MITRE**: T1005 - Data from Local System
- **Impact**: Firmware theft or tampering
- **Tools**: CH341A Programmer, SOIC Clip
- **Scenario**: Extract firmware from SPI flash chip via clip-on reader to reverse engineer device
- **Attack Steps**: Step 1: Open the device casing and locate the SPI flash chip (usually 8-pin). Step 2: Attach SOIC clip to the chip without desoldering. Step 3: Connect the clip to CH341A USB programmer. Step 4: Use software like Flashrom to read and save firmware. Step 5: Analyze firmware for secrets, passwords, or vulnerabilities.
- **Detection**: Firmware hash change
- **Solution**: Use encrypted, locked flash
- **Tags**: SPI, CH341A, Dump

## SDR-Based Wireless Signal Injection

- **Attack Type**: Signal Spoofing
- **Target**: Smart Locks, Alarms
- **Vulnerability**: Unencrypted RF communication
- **MITRE**: T1421 - Spoof Command Message
- **Impact**: Unauthorized access
- **Tools**: HackRF One, GNURadio
- **Scenario**: Use Software-Defined Radio to spoof remote commands to unlock or start IoT devices
- **Attack Steps**: Step 1: Record legitimate RF signals from target remote/key fob using SDR. Step 2: Analyze signal characteristics using GNURadio. Step 3: Replay signal using HackRF with adjusted power. Step 4: Observe device response (e.g., door unlocks). Step 5: Repeat or modify signal to trigger other actions.
- **Detection**: RF signal anomaly tools
- **Solution**: Use rolling codes, encryption
- **Tags**: SDR, RF Replay, IoT

## USB-C Cable with Embedded Controller

- **Attack Type**: Stealth Interface Control
- **Target**: Smartphones, Laptops
- **Vulnerability**: Cable trust, embedded controller
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Full control via cable
- **Tools**: O.MG Cable C2, ESP32
- **Scenario**: Modified USB-C cable contains programmable chip to inject keystrokes or read data
- **Attack Steps**: Step 1: Get or build a USB-C cable with embedded ESP32 chip. Step 2: Configure payload via web-based C2 panel. Step 3: Give or plug into victim’s device. Step 4: Activate payload remotely (e.g., open browser, download malware). Step 5: Log and control victim device silently.
- **Detection**: USB traffic logging
- **Solution**: Validate cable origins, USB restrictions
- **Tags**: USB-C, Hardware Backdoor

## NFC Smart Card Emulator Attack

- **Attack Type**: Credential Clone
- **Target**: Access Control Systems
- **Vulnerability**: Unencrypted NFC data
- **MITRE**: T1557.002 - Wireless Sniffing
- **Impact**: Physical intrusion
- **Tools**: Flipper Zero, NFC Tools Pro
- **Scenario**: Clone and emulate a smart card or NFC badge using mobile phone or card emulator
- **Attack Steps**: Step 1: Use Flipper Zero to scan target NFC badge at close distance. Step 2: Store badge data in memory. Step 3: Switch to "Emulate" mode to replicate original badge. Step 4: Use Flipper at access point to unlock doors or login. Step 5: Exit without leaving trace.
- **Detection**: NFC audit logs
- **Solution**: Use secure NFC protocols
- **Tags**: NFC, Emulation, Flipper

## Fake USB Battery Pack Keylogger

- **Attack Type**: Power+Keylog Combo
- **Target**: Laptops, Mobile Devices
- **Vulnerability**: Trusted power accessories
- **MITRE**: T1056.001 - Keylogging
- **Impact**: Password theft
- **Tools**: Custom PCB, Flash Storage
- **Scenario**: USB power bank modified to also capture keyboard strokes
- **Attack Steps**: Step 1: Modify USB power bank to include USB keylogger circuit inline with power delivery. Step 2: Victim uses power bank to charge phone/laptop. Step 3: Device silently captures USB keyboard traffic. Step 4: Retrieve keylogs by connecting to attacker PC. Step 5: Use extracted passwords for access.
- **Detection**: Hard to detect physically
- **Solution**: Use trusted accessories only
- **Tags**: USB, Power Bank, Covert Log

## Visual Hacking with Thermal Camera

- **Attack Type**: PIN Inference
- **Target**: ATMs, Electronic Locks
- **Vulnerability**: Residual heat on keypads
- **MITRE**: T1110 - Brute Force
- **Impact**: PIN code guess, access
- **Tools**: FLIR One, Android App
- **Scenario**: Use thermal camera to read residual heat from keypad to guess PIN
- **Attack Steps**: Step 1: Wait for user to leave ATM or keypad lock. Step 2: Quickly aim thermal camera at keypad. Step 3: View heat signature — warmer keys were pressed recently. Step 4: Try different PIN combinations based on order of fading heat. Step 5: Bypass lock or gain access.
- **Detection**: Use randomized keypads
- **Solution**: Thermal masking, delay retry
- **Tags**: PIN, Thermal, Visual

## Keyboard Implant via Hardware Tap

- **Attack Type**: Physical Keylogger
- **Target**: Office Workstations
- **Vulnerability**: No tamper-evident hardware
- **MITRE**: T1056 - Input Capture
- **Impact**: Keylogging of credentials
- **Tools**: KeyGrabber USB, WiFi Logger
- **Scenario**: Physically implant a device inside a keyboard to intercept keys
- **Attack Steps**: Step 1: Open keyboard casing carefully. Step 2: Insert USB keylogger device inline between keyboard controller and cable. Step 3: Reassemble keyboard and connect to PC. Step 4: Device logs every keystroke to flash or sends via WiFi. Step 5: Later retrieve or receive data remotely.
- **Detection**: Rarely checked physically
- **Solution**: Tamper seals, USB audits
- **Tags**: Hardware Implant, USB Keylog

## Fake USB Ethernet Adapter with MITM Proxy

- **Attack Type**: Network Spoof
- **Target**: Office PCs
- **Vulnerability**: Unrestricted USB Ethernet install
- **MITRE**: T1557 - MITM
- **Impact**: Traffic hijack, phishing
- **Tools**: Bash Bunny, mitmproxy
- **Scenario**: USB device acts as Ethernet adapter and proxies traffic to inject payloads
- **Attack Steps**: Step 1: Load Bash Bunny with script that configures device as USB Ethernet gadget. Step 2: Insert into victim PC. Step 3: Routes traffic through onboard proxy (mitmproxy). Step 4: Injects malicious JavaScript or credential-stealing forms. Step 5: Disconnects silently.
- **Detection**: Interface anomaly alerts
- **Solution**: USB restriction policies
- **Tags**: USB NIC, Bash Bunny

## Exploiting Debug Access via SWD Interface

- **Attack Type**: Debug Port Abuse
- **Target**: Embedded Controllers
- **Vulnerability**: Unprotected debug access
- **MITRE**: T1601 - Modify System Firmware
- **Impact**: Logic tampering, memory theft
- **Tools**: ST-Link, OpenOCD
- **Scenario**: Use SWD (Serial Wire Debug) interface to pause, read, or modify microcontroller
- **Attack Steps**: Step 1: Identify SWD pins on microcontroller board. Step 2: Connect ST-Link or compatible debugger. Step 3: Use OpenOCD to halt CPU and dump memory. Step 4: Modify variables or firmware in real-time. Step 5: Resume program — attacker changes take effect.
- **Detection**: Hardware interface scanning
- **Solution**: Lock debug ports, fuse bits
- **Tags**: SWD, MCU, Debug Hack

## QR Code Injection via External Display

- **Attack Type**: Visual Payload Attack
- **Target**: PCs, Public Screens
- **Vulnerability**: User trust in QR codes
- **MITRE**: T1204.001 - Malicious Link
- **Impact**: Credential theft, remote access
- **Tools**: QRGen, Social Engineering
- **Scenario**: External monitor displays malicious QR code to fool user into scanning
- **Attack Steps**: Step 1: Attach external HDMI screen or change desktop background to QR code. Step 2: QR code links to phishing site or fake login portal. Step 3: Victim scans QR using phone thinking it's from legit source. Step 4: Enters credentials or grants access. Step 5: Attacker logs in using stolen data.
- **Detection**: URL logs, phishing analysis
- **Solution**: Educate users, QR scanners with preview
- **Tags**: QR, Display, Visual Phish

## Infrared (IR) Remote Command Replay

- **Attack Type**: Signal Replay
- **Target**: Smart TVs, Set-top Boxes
- **Vulnerability**: No IR authentication
- **MITRE**: T1542 - System Manipulation
- **Impact**: Device abuse, DoS
- **Tools**: IR Receiver + Transmitter, LIRC
- **Scenario**: Replay IR signals to control smart TVs, ACs, or devices
- **Attack Steps**: Step 1: Use IR receiver (like USB dongle) to record commands from victim’s remote (e.g., power, menu). Step 2: Save signals using LIRC software. Step 3: Point IR LED toward device and replay commands. Step 4: Modify TV settings, reboot systems, or inject input. Step 5: Loop actions or cause confusion.
- **Detection**: Unusual remote activity logs
- **Solution**: Disable IR or use RF remotes
- **Tags**: IR, Replay, Home IoT

## Covert Wi-Fi Key Extraction via Side USB

- **Attack Type**: Config Theft
- **Target**: Windows Laptops
- **Vulnerability**: Autorun scripts, trusted USB
- **MITRE**: T1552 - Unsecured Credentials
- **Impact**: Steal Wi-Fi credentials
- **Tools**: Hidden PowerShell Script
- **Scenario**: USB drive reads Wi-Fi config from system and stores it silently
- **Attack Steps**: Step 1: Load USB with autorun.inf and PowerShell script. Step 2: Plug into victim PC. Step 3: Script silently reads stored Wi-Fi credentials using command: netsh wlan show profile key=clear. Step 4: Save results in hidden text file on USB. Step 5: Remove USB — credentials extracted.
- **Detection**: Endpoint logging tools
- **Solution**: Disable autorun, block PS
- **Tags**: Wi-Fi, USB Script

## Keyboard Matrix Glitch Injection

- **Attack Type**: Key Mapping Exploit
- **Target**: Keyboards, ATMs
- **Vulnerability**: No matrix input validation
- **MITRE**: T1556 - Input Manipulation
- **Impact**: Input hijacking
- **Tools**: Thin Wires, PCB Pins
- **Scenario**: Interfere with hardware keyboard matrix to inject custom keys
- **Attack Steps**: Step 1: Open target keyboard and identify matrix layout (row/column pins). Step 2: Bridge two pin combinations with wire or switch. Step 3: Create false keypresses when power is on. Step 4: System detects phantom keystrokes (e.g., Alt+F4, Ctrl+T). Step 5: Use for annoyance, DoS, or distraction.
- **Detection**: Keystroke logs, alerts
- **Solution**: Shield circuits, debounce filters
- **Tags**: Keyboard, Matrix Hack

## USB MIDI Device Payload Injection

- **Attack Type**: USB Protocol Abuse
- **Target**: Creative Workstations
- **Vulnerability**: Trusted multimedia peripherals
- **MITRE**: T1204 - User Execution
- **Impact**: Remote access setup
- **Tools**: Teensy Board, Arduino
- **Scenario**: MIDI device acts as HID to trigger input or malware execution
- **Attack Steps**: Step 1: Program Teensy to emulate MIDI + Keyboard. Step 2: Insert into victim’s USB port (disguised as music gadget). Step 3: Plays audio and then injects keystrokes to open terminal. Step 4: Executes payload silently. Step 5: Victim thinks it’s just a music device.
- **Detection**: MIDI logs (rare)
- **Solution**: Use device control software
- **Tags**: MIDI, Teensy, Trick

## HID Proxy Attack using USB Switcher

- **Attack Type**: Device Swap
- **Target**: Office Desktops
- **Vulnerability**: Unlocked USB access
- **MITRE**: T1056.001 - Input Capture
- **Impact**: Covert script injection
- **Tools**: USB Switch, Bash Bunny
- **Scenario**: Switch attacker’s HID device with victim’s using a hidden USB switch
- **Attack Steps**: Step 1: Set up a USB switch that toggles between real keyboard and Bash Bunny. Step 2: Switch activated when victim leaves desk. Step 3: Bash Bunny injects payload (open cmd, exfil data). Step 4: Switch back to real keyboard. Step 5: Victim unaware—everything works normally.
- **Detection**: USB logs, motion sensors
- **Solution**: Secure ports, USB lock
- **Tags**: Switcher, HID, Bash Bunny

## Smartwatch Bluetooth HID Spoof

- **Attack Type**: BLE Keyboard Attack
- **Target**: Laptops, Tablets
- **Vulnerability**: Auto-accept BT pairing
- **MITRE**: T1557.001 - MITM
- **Impact**: Keystroke injection
- **Tools**: WearOS, GATT Profile Tool
- **Scenario**: Use smartwatch to spoof a Bluetooth keyboard and send payloads
- **Attack Steps**: Step 1: Enable developer mode on smartwatch. Step 2: Set GATT profile to emulate HID Keyboard. Step 3: Pair with victim’s unlocked laptop. Step 4: Inject keystrokes to download malware. Step 5: Disable HID profile remotely.
- **Detection**: BT pairing log, BT stack alerts
- **Solution**: Disable BT pairing by default
- **Tags**: Smartwatch, BLE HID

## Exploit via Exposed HDMI-CEC Commands

- **Attack Type**: Remote CEC Control
- **Target**: Smart TVs, Consoles
- **Vulnerability**: HDMI-CEC enabled by default
- **MITRE**: T1546.012 - External Remote Services
- **Impact**: UI spoofing, control hijack
- **Tools**: CEC Injector, Raspberry Pi
- **Scenario**: Use HDMI-CEC to control TV or devices, issue silent commands
- **Attack Steps**: Step 1: Connect Raspberry Pi to victim device’s HDMI port. Step 2: Send cec-client commands like input change, shutdown. Step 3: Trick user by launching phishing UI (e.g., fake Netflix login). Step 4: Collect input via HDMI. Step 5: Control resumes to normal.
- **Detection**: HDMI activity logs
- **Solution**: Disable CEC or monitor
- **Tags**: HDMI-CEC, Input Hijack

## Plug and Tap USB Audio Jack Exploit

- **Attack Type**: Covert Recording
- **Target**: PCs, Call Centers
- **Vulnerability**: Trust in audio devices
- **MITRE**: T1123 - Audio Capture
- **Impact**: Eavesdropping, data theft
- **Tools**: USB Audio Tap, Mini Recorder
- **Scenario**: Use fake headphone jack to record conversations or system audio
- **Attack Steps**: Step 1: Modify USB headset with mini-recorder inside. Step 2: Plug into victim PC — system assumes it's a regular headset. Step 3: Audio feed sent to hidden internal storage or streamed live. Step 4: Attacker retrieves the device later. Step 5: Conversations compromised.
- **Detection**: USB audio monitoring
- **Solution**: Enforce trusted USB IDs
- **Tags**: Audio, Tap, Espionage

## Fake USB Mass Storage with Firmware Upgrade

- **Attack Type**: Vendor Exploit
- **Target**: Enterprise Laptops
- **Vulnerability**: Trust in update utilities
- **MITRE**: T1204.002 - Malicious USB Device
- **Impact**: Rootkit install
- **Tools**: STM32, Fake MSC
- **Scenario**: Device pretends to be updatable mass storage, loads backdoor via firmware update
- **Attack Steps**: Step 1: Program microcontroller to show up as a storage device. Step 2: User opens USB and sees "FirmwareUpdate.exe". Step 3: Clicking runs disguised malware. Step 4: Malware adds persistence and backdoor. Step 5: USB appears normal with no real storage.
- **Detection**: Endpoint protection alert
- **Solution**: Block executable on USB
- **Tags**: Firmware Trap, USB

## Radio Frequency (RFID) Denial of Service

- **Attack Type**: Wireless Jammer
- **Target**: RFID Readers
- **Vulnerability**: No anti-spam or signal validation
- **MITRE**: T1498 - Network Denial of Service
- **Impact**: Entry prevention, delay
- **Tools**: RFID Emulator, Signal Jammer
- **Scenario**: Flood RFID reader with junk tags or jamming signal to prevent valid scan
- **Attack Steps**: Step 1: Approach RFID scanner in secure area. Step 2: Use tool like Flipper Zero or RFID Jammer to flood with repeated tags. Step 3: Reader becomes unresponsive or fails to read real cards. Step 4: Delay or block user access. Step 5: Withdraw without being noticed.
- **Detection**: Access log anomalies
- **Solution**: Use RFID anti-jam firmware
- **Tags**: RFID DoS, Flooding

## BIOS Malware Flash via SPI Programmer

- **Attack Type**: BIOS Tampering
- **Target**: Desktop PCs
- **Vulnerability**: Unprotected SPI flash
- **MITRE**: T1542.003 - Bootkit
- **Impact**: Persistent root access
- **Tools**: CH341A, Flashrom
- **Scenario**: Use SPI flasher to overwrite BIOS with malicious firmware
- **Attack Steps**: Step 1: Open victim's PC case and locate BIOS chip. Step 2: Attach SOIC clip from CH341A SPI programmer. Step 3: Dump original BIOS firmware using Flashrom. Step 4: Modify or replace with malicious BIOS image. Step 5: Flash it back and reboot — implant now persists.
- **Detection**: BIOS hash mismatch
- **Solution**: Secure Boot, BIOS write-protect
- **Tags**: BIOS, SPI, Rootkit

## PS/2 Keyboard Tap using Microcontroller

- **Attack Type**: Inline Keylogger
- **Target**: Legacy PCs
- **Vulnerability**: PS/2 has no encryption
- **MITRE**: T1056.001 - Keylogging
- **Impact**: Password theft, espionage
- **Tools**: ATmega32, PS/2 Logger
- **Scenario**: Place microcontroller inline between PS/2 keyboard and PC
- **Attack Steps**: Step 1: Identify PS/2 keyboard cable between PC and keyboard. Step 2: Cut and reconnect using ATmega32-based logger. Step 3: Monitor and store key presses in EEPROM. Step 4: Recover logs via USB or serial later. Step 5: Victim experiences no change in behavior.
- **Detection**: Very hard to detect
- **Solution**: Use USB keyboards only
- **Tags**: PS/2, ATmega, Keylog

## Wi-Fi Probe Request Harvesting

- **Attack Type**: Wireless Recon
- **Target**: Smartphones, Laptops
- **Vulnerability**: Probe requests not masked
- **MITRE**: T1430 - Wireless Sniffing
- **Impact**: Credential theft, tracking
- **Tools**: Wireshark, Kismet
- **Scenario**: Use tool to collect Wi-Fi SSIDs a device probes for, revealing past connections
- **Attack Steps**: Step 1: Set up Wi-Fi sniffer in monitor mode near victim. Step 2: Capture probe requests from victim’s device. Step 3: Analyze requests to reveal SSID history. Step 4: Create fake APs with same SSID to trick victim. Step 5: Harvest credentials via phishing portal.
- **Detection**: Monitor for rogue APs
- **Solution**: Use MAC randomization
- **Tags**: Probe, Wi-Fi, Metadata

## Device Bricking via USB Power Surge

- **Attack Type**: Hardware Kill
- **Target**: Laptops, Desktops
- **Vulnerability**: No overcurrent protection
- **MITRE**: T1499 - Endpoint Denial of Service
- **Impact**: Hardware destruction
- **Tools**: USB Killer
- **Scenario**: Deliver high-voltage burst through USB line to destroy internal circuits
- **Attack Steps**: Step 1: Insert USB Killer (special device with capacitor bank) into victim’s USB port. Step 2: Device charges from power line briefly. Step 3: Discharges 200V+ back into data/power lines. Step 4: Motherboard and USB controller damaged. Step 5: System no longer boots — permanent damage.
- **Detection**: Physical port check
- **Solution**: USB port surge protection
- **Tags**: USB Killer, DoS

## NFC Payment Skimmer via Phone

- **Attack Type**: Payment Intercept
- **Target**: Contactless Cards
- **Vulnerability**: No encryption on old cards
- **MITRE**: T1557.002 - Wireless Sniffing
- **Impact**: Financial theft
- **Tools**: NFC Tools Pro, Android
- **Scenario**: Attacker pretends to tap phone on terminal but steals card data using NFC
- **Attack Steps**: Step 1: Load NFC sniffing app on phone. Step 2: Approach victim with tap-to-pay card. Step 3: Fake a friendly bump or pass-by. Step 4: App captures unencrypted data from NFC tag. Step 5: Later used to clone or analyze card data.
- **Detection**: NFC logs, payment fraud alerts
- **Solution**: Use RFID-blocking wallets
- **Tags**: NFC, Payment, Skim

## USB Thumb Drive Overheat Attack

- **Attack Type**: Denial via Heat
- **Target**: Office PCs
- **Vulnerability**: USB power not current-limited
- **MITRE**: T1499.004 - USB DoS
- **Impact**: Port failure, physical damage
- **Tools**: Modified USB, Resistor Circuit
- **Scenario**: USB contains resistor circuit that heats and melts port or internals
- **Attack Steps**: Step 1: Modify USB stick to include a low-resistance resistor circuit. Step 2: Insert into USB port — draws high current. Step 3: Device heats up rapidly. Step 4: Melts internal port plastic, or disables controller. Step 5: Causes physical DoS.
- **Detection**: Port temperature monitoring
- **Solution**: Use USB current limiters
- **Tags**: USB, Heat Attack

## Barcode Scanner Buffer Overflow

- **Attack Type**: Input Overflow
- **Target**: POS Systems
- **Vulnerability**: No input sanitization
- **MITRE**: T1203 - Exploitation for Privilege
- **Impact**: Code exec or crash
- **Tools**: Custom Barcode Generator
- **Scenario**: Specially crafted barcode overflows memory in USB barcode scanner
- **Attack Steps**: Step 1: Use barcode tool to generate a long input (e.g., 10,000 chars). Step 2: Print and scan using USB barcode scanner connected to PC. Step 3: Scanner overflows buffer and crashes or executes code. Step 4: If vulnerable, attacker gets access. Step 5: Use for privilege escalation.
- **Detection**: Device behavior logs
- **Solution**: Firmware input limits
- **Tags**: Barcode, Overflow

## Printer USB Exploit to Internal Network

- **Attack Type**: Pivot via USB
- **Target**: Office Printers
- **Vulnerability**: No file execution sandbox
- **MITRE**: T1210 - Exploitation of Remote Services
- **Impact**: Lateral movement
- **Tools**: Bash Bunny, Printer Exploit Kit
- **Scenario**: Attacker inserts USB with script to printer that connects to network
- **Attack Steps**: Step 1: Create script that runs when printer reads file (e.g., job.inf). Step 2: Insert USB into multifunction printer. Step 3: Printer executes script silently, sends ping or backdoor to attacker. Step 4: Use printer as foothold into network. Step 5: Move laterally.
- **Detection**: Printer logs, IDS
- **Solution**: Secure printer USB config
- **Tags**: USB, Printer, Pivot

## Magnetic Stripe Clone with Custom Reader

- **Attack Type**: Card Clone
- **Target**: Magstripe Access Cards
- **Vulnerability**: Unencrypted magstripe
- **MITRE**: T1557 - Adversary in the Middle
- **Impact**: Unauthorized access
- **Tools**: MSR605X, MagStriper
- **Scenario**: Use reader to clone magstripe cards like hotel keys or access cards
- **Attack Steps**: Step 1: Swipe card on custom MSR reader. Step 2: Store stripe data (track 1, 2). Step 3: Write to blank magnetic card. Step 4: Use cloned card at door lock or POS. Step 5: Discard after use.
- **Detection**: Card audit logs
- **Solution**: Move to chip/RFID
- **Tags**: Clone, Magstripe, Swipe

## Tampered HDMI Cable Data Leak

- **Attack Type**: Video Exfiltration
- **Target**: Secure PCs
- **Vulnerability**: Unmonitored display path
- **MITRE**: T1113 - Screen Capture
- **Impact**: Visual data theft
- **Tools**: HDMI Tap, FPGA
- **Scenario**: HDMI cable modified with tap to capture video frames from source device
- **Attack Steps**: Step 1: Build or buy HDMI tap with HDMI-IN and HDMI-OUT. Step 2: Place in between PC and monitor. Step 3: Capture video frames as data passes through. Step 4: Store or transmit to attacker. Step 5: Monitor screen exfiltrated in real-time.
- **Detection**: Screen mirroring alerts
- **Solution**: Use encrypted display paths
- **Tags**: HDMI Tap, Visual Leak

## Malicious USB Autorun with Social Engineering

- **Attack Type**: Removable Media Attack
- **Target**: Employee Workstation
- **Vulnerability**: Human curiosity + Autorun
- **MITRE**: T1204.001 (Malicious Link / File)
- **Impact**: Malware infection, data theft
- **Tools**: Normal USB drive, Autorun.inf generator, Malware EXE
- **Scenario**: An attacker drops USB drives in public locations (baiting) that auto-run malware when inserted by a curious user.
- **Attack Steps**: Step 1: Prepare a USB with a file like "Salary_Slip_2025.pdf.exe" and an autorun.inf file that opens it. Step 2: The file may appear as a normal PDF to the victim. Step 3: Drop the USB in a parking lot or cafeteria. Step 4: A curious user plugs it in. The file auto-executes (if auto-run is enabled) or user opens it manually. Step 5: Malware is installed silently.
- **Detection**: Antivirus logs, endpoint alerts, GPO logs
- **Solution**: Disable autorun, educate users not to trust unknown USBs
- **Tags**: social engineering, autorun, malware bait

## USB Keylogger Implant

- **Attack Type**: Removable Media Attack
- **Target**: Desktop computer
- **Vulnerability**: Unrestricted physical access to I/O ports
- **MITRE**: T1056.001 (Input Capture: Keylogging)
- **Impact**: Stolen credentials, data exfiltration
- **Tools**: Hardware USB keylogger
- **Scenario**: A USB keylogger is physically installed between the keyboard and PC to record keystrokes, including passwords.
- **Attack Steps**: Step 1: Buy a USB keylogger online (tiny device that logs keyboard data). Step 2: Find unattended system (e.g., office workstation). Step 3: Plug the keylogger between the keyboard USB cable and the PC USB port. Step 4: After a few hours or days, retrieve the device. Step 5: Connect it to your own PC and read logs (most devices save keystrokes in .txt format).
- **Detection**: Physical inspection, USB logging tools
- **Solution**: Lock PCs, restrict access, regular inspection
- **Tags**: keylogger, physical device, credential theft

## USB Data Theft Using Raspberry Pi Zero

- **Attack Type**: Removable Media Attack
- **Target**: Personal or corporate PC
- **Vulnerability**: USB auto-mount and device trust
- **MITRE**: T1129 (Shared Modules) + T1030 (Data Transfer Size Limits)
- **Impact**: Theft of credentials, PII, or corporate data
- **Tools**: Raspberry Pi Zero, Python, Bash scripts
- **Scenario**: A Raspberry Pi Zero disguised as a USB stick is used to steal files or login tokens when connected.
- **Attack Steps**: Step 1: Program Raspberry Pi Zero with a script that copies specific files (e.g., browser cookies, document folder). Step 2: Plug it into victim's USB port. Step 3: Pi Zero emulates USB Ethernet or HID to interact with OS. Step 4: It silently executes scripts to pull data and save it on the SD card. Step 5: Retrieve the device and read stolen files.
- **Detection**: Monitor file system and USB activity
- **Solution**: Lock USB ports, use device authentication
- **Tags**: usb theft, raspberry pi, stealth attack, data exfiltration

## USB Power Surge to Damage Port

- **Attack Type**: Removable Media Attack
- **Target**: Laptop, Desktop
- **Vulnerability**: USB power regulation vulnerability
- **MITRE**: T1561.001 (Disk Wipe / Destruction)
- **Impact**: Hardware damage, device bricking
- **Tools**: USB Killer, DIY voltage spike USB
- **Scenario**: Attacker uses modified USB device to overload and damage the USB port or motherboard power rail.
- **Attack Steps**: Step 1: Purchase or build a USB Killer (device that rapidly discharges high voltage). Step 2: Plug the USB into the victim PC. Step 3: Device sends voltage spikes into the USB power lines. Step 4: This damages internal circuits, rendering USB ports or even the motherboard dead.
- **Detection**: BIOS logs, hardware diagnostics
- **Solution**: Use USB data blockers, restrict access
- **Tags**: power surge, hardware damage, usb killer

## HID Injection with Arduino Leonardo

- **Attack Type**: Removable Media Attack
- **Target**: Windows/Linux/macOS
- **Vulnerability**: HID trust assumption
- **MITRE**: T1059 (Command and Scripting Interpreter)
- **Impact**: Full system access, new user created
- **Tools**: Arduino Leonardo/Micro
- **Scenario**: An Arduino board mimics a keyboard to run malicious scripts when plugged in.
- **Attack Steps**: Step 1: Buy Arduino Leonardo (or Digispark) which supports HID emulation. Step 2: Install Arduino IDE on your computer. Step 3: Write a script in Arduino to open terminal and run malicious commands (e.g., add new admin user). Step 4: Upload code to board and plug it into victim machine. Step 5: The device types automatically like a keyboard.
- **Detection**: Monitor sudden window focus shifts, input rate anomalies
- **Solution**: Block HID USBs unless signed, policy restrictions
- **Tags**: arduino, hid, scripting, physical hack

## USB Mass Storage Hidden Partition

- **Attack Type**: Removable Media Attack
- **Target**: Workstation
- **Vulnerability**: File system mount trust
- **MITRE**: T1204.002
- **Impact**: Malware execution via USB
- **Tools**: WinHex, USB tools, Python
- **Scenario**: A USB with a hidden partition contains malware which executes when accessed via script.
- **Attack Steps**: Step 1: Take a normal USB drive and use tools like WinHex to create a hidden partition. Step 2: Store malicious EXE file there. Step 3: Create a front-facing “innocent” file like a resume PDF. Step 4: Share USB with victim. Step 5: Use a batch script to mount hidden partition silently and execute the file when USB is inserted.
- **Detection**: File system monitoring, AV alerts
- **Solution**: Disable USB mounting or use signed-only drives
- **Tags**: hidden partition, stealth, autorun, exfiltration

## USB Network Adapter MITM

- **Attack Type**: Removable Media Attack
- **Target**: Laptop
- **Vulnerability**: Auto trust of USB network adapters
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Credential theft, DNS hijack
- **Tools**: LAN Turtle, Bash Bunny, Pi Zero
- **Scenario**: USB acts as a fake network adapter and intercepts or redirects traffic.
- **Attack Steps**: Step 1: Program device (LAN Turtle or Pi Zero) to act as USB network adapter. Step 2: Configure it to act as DHCP server and redirect DNS. Step 3: Plug into target system. Step 4: System auto connects to it, assuming it's a trusted LAN. Step 5: All traffic is now intercepted or redirected.
- **Detection**: Monitor for rogue NICs, new IP range
- **Solution**: Disable auto-trust for USB network cards
- **Tags**: mitm, lan turtle, pi zero, usb adapter

## USB Auto Boot via BIOS

- **Attack Type**: Removable Media Attack
- **Target**: PC/Laptop
- **Vulnerability**: BIOS unlocked, boot order not secured
- **MITRE**: T1078.001 (Valid Accounts via OS Access)
- **Impact**: Total system takeover
- **Tools**: Bootable USB with Kali or payload
- **Scenario**: An attacker boots a device using malicious USB if BIOS boot order allows it.
- **Attack Steps**: Step 1: Create a bootable USB using Rufus with Linux or custom OS payload. Step 2: Find an unlocked PC (no BIOS password). Step 3: Reboot it and enter BIOS. Step 4: Set USB as first boot device. Step 5: Insert malicious USB and reboot – attacker now has full OS access.
- **Detection**: BIOS boot logs, reboot trace
- **Solution**: BIOS password, disable USB boot
- **Tags**: bios, bootloader, usb boot attack

## USB HID for Screenlocker Bypass

- **Attack Type**: Removable Media Attack
- **Target**: Windows systems
- **Vulnerability**: Unattended, active sessions
- **MITRE**: T1563.002 (Remote Desktop Hijack)
- **Impact**: Bypass session lock, file access
- **Tools**: Digispark/Arduino HID
- **Scenario**: HID device mimics a keyboard to open locked session when left unattended.
- **Attack Steps**: Step 1: Wait for user to lock system but leave session active. Step 2: Plug in HID USB programmed to press Win key, type commands to disable lock screen or reset password. Step 3: Run payload or exfiltrate files.
- **Detection**: Activity logs, physical surveillance
- **Solution**: Use timed logout, USB port control
- **Tags**: screen unlock, HID, usb bypass

## USB as Keystroke Replayer

- **Attack Type**: Removable Media Attack
- **Target**: Desktop/terminal systems
- **Vulnerability**: Keystroke memory vulnerability
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Credential reuse, privilege gain
- **Tools**: USB Keystroke Recorder
- **Scenario**: A USB is used to record and replay exact keystrokes to repeat a victim’s login or command.
- **Attack Steps**: Step 1: Install USB recorder device between keyboard and PC. Step 2: Let it passively log all inputs (e.g., password, commands). Step 3: Later, switch mode to “replay”. Step 4: Plug into same system – it automatically types stored keys. Step 5: This re-logs user or runs prior commands.
- **Detection**: Input logging alerts, USB input logs
- **Solution**: Use smartcards, restrict physical access
- **Tags**: key replayer, usb logger, credential replay

## USB Webcam Injection via UVC

- **Attack Type**: Removable Media Attack
- **Target**: Laptops, desktops
- **Vulnerability**: USB camera trust
- **MITRE**: T1125 (Video Capture)
- **Impact**: Privacy breach, surveillance
- **Tools**: UVC-compatible Raspberry Pi cam
- **Scenario**: A USB device pretends to be a webcam and captures frames without user consent.
- **Attack Steps**: Step 1: Flash a Raspberry Pi Zero to act as a UVC (USB Video Class) device. Step 2: Add script to activate cam and store images or stream them. Step 3: Plug into victim PC. Step 4: Victim sees a generic webcam device – camera silently records.
- **Detection**: AV webcam blocking, device audit
- **Solution**: Disable unknown USB cams
- **Tags**: usb webcam, uvc injection, spy cam

## Malicious File on USB Shortcut

- **Attack Type**: Removable Media Attack
- **Target**: Any OS with GUI
- **Vulnerability**: File icon spoofing
- **MITRE**: T1204.002
- **Impact**: Silent malware infection
- **Tools**: .lnk file creator, malware dropper
- **Scenario**: A USB contains a shortcut file disguised as a folder, launching malware.
- **Attack Steps**: Step 1: Create a folder icon shortcut .lnk file. Step 2: Link it to launch malware.exe + open real folder. Step 3: Copy it to USB and rename as “Holiday Pics”. Step 4: Share it with victim. Step 5: Victim double-clicks thinking it's a folder – malware executes.
- **Detection**: AV alert, shortcut analysis
- **Solution**: Show full file extensions, disable shortcut trust
- **Tags**: shortcut, .lnk, malware, usb bait

## USB RFID/NFC Cloner

- **Attack Type**: Removable Media Attack
- **Target**: Access Control Systems
- **Vulnerability**: Poor RFID encryption or UID-only validation
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Unauthorized physical entry
- **Tools**: USB RFID/NFC Cloner (e.g., Proxmark3)
- **Scenario**: An attacker uses USB RFID/NFC device to clone access badges and copy to duplicate cards.
- **Attack Steps**: Step 1: Connect Proxmark3 to USB port. Step 2: Use it to scan victim’s RFID badge (e.g., office entry). Step 3: Save the captured UID and data. Step 4: Write the data onto a blank RFID/NFC card. Step 5: Use the cloned card for unauthorized access.
- **Detection**: RFID logs, card collision alerts
- **Solution**: Upgrade to encrypted RFID/NFC tech
- **Tags**: rfid, nfc, card cloning, access bypass

## USB Hidden File Auto Copy

- **Attack Type**: Removable Media Attack
- **Target**: Windows
- **Vulnerability**: Auto-execution and file access
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Unauthorized file theft
- **Tools**: USB, batch scripts
- **Scenario**: A USB is scripted to silently copy files from the target computer.
- **Attack Steps**: Step 1: Create a script (e.g., copy C:\Users\Documents\* D:\Hidden) and save it as .bat. Step 2: Place it inside USB and configure it to auto-execute. Step 3: Plug into target PC. Step 4: Files get copied into a hidden folder on the USB. Step 5: Remove USB and view stolen files later.
- **Detection**: USB monitoring tools
- **Solution**: Disable USB write, monitor scripts
- **Tags**: file copy, auto script, data theft

## Juice Jacking via Public Charging USB

- **Attack Type**: Removable Media Attack
- **Target**: Phones, laptops
- **Vulnerability**: Data-over-power lines
- **MITRE**: T1052 (Exfiltration Over USB)
- **Impact**: Malware installation, backdoor
- **Tools**: USB cable with chip, public kiosk
- **Scenario**: A charging port is modified to act as a USB data interface and inject malware.
- **Attack Steps**: Step 1: Buy/modify a USB charging cable to include a chip (like ESP32). Step 2: Program chip to act like a keyboard and run malicious commands. Step 3: Leave cable at airport/public charger. Step 4: Victim plugs into laptop → attack runs silently.
- **Detection**: USB activity logs, alerting USB profiles
- **Solution**: Use charge-only cables, block USB data
- **Tags**: juice jacking, usb power, charging exploit

## USB Mouse with Embedded Payload

- **Attack Type**: Removable Media Attack
- **Target**: Desktop systems
- **Vulnerability**: Trusting input peripherals
- **MITRE**: T1200, T1059
- **Impact**: Silent compromise
- **Tools**: Mouse shell + USB board
- **Scenario**: A real mouse is modified to carry a secondary USB inside, running hidden payloads.
- **Attack Steps**: Step 1: Take a regular USB mouse. Step 2: Open the mouse and embed a secondary USB HID (e.g., Digispark). Step 3: Program it to inject keystrokes. Step 4: Connect it to target machine – appears as normal mouse but also types commands in background.
- **Detection**: Dual device detection, HID logs
- **Solution**: Block multi-HID devices, monitor USBs
- **Tags**: dual usb, mouse payload, stealth hack

## USB Sound Card to Record Audio

- **Attack Type**: Removable Media Attack
- **Target**: Laptops
- **Vulnerability**: Input device trust
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Espionage, privacy breach
- **Tools**: USB Audio Adapter, Recording script
- **Scenario**: USB emulates sound card and records mic audio from target system.
- **Attack Steps**: Step 1: Buy USB sound card device (cheap online). Step 2: Write script to record system mic input and save .WAV files. Step 3: Plug into target PC – acts as microphone. Step 4: Record passively in background. Step 5: Retrieve device to listen to audio.
- **Detection**: Mic detection tools, audio monitoring
- **Solution**: Disable USB mic input, user education
- **Tags**: usb mic, audio hack, spy listening

## USB Data Diode Bypass via Flip Switch

- **Attack Type**: Removable Media Attack
- **Target**: Air-gapped PCs
- **Vulnerability**: Physical bypass of data diode
- **MITRE**: T1567.002
- **Impact**: Air-gap breach
- **Tools**: Arduino switch, USB Y-split
- **Scenario**: Attacker creates a modified USB switch to bypass unidirectional data diodes.
- **Attack Steps**: Step 1: Create a physical USB switch with a Y-splitter and microcontroller. Step 2: Set one side to read-only, one to write. Step 3: Switch between them physically using a toggle. Step 4: Access secured air-gapped machine and extract files. Step 5: Reconnect to attacker system and toggle switch to send files.
- **Detection**: USB audit logs, air-gap control
- **Solution**: Use unpowered diodes, air-gapped vaults
- **Tags**: data diode, airgap, usb switch

## USB Shortcut Spread via File Explorer

- **Attack Type**: Removable Media Attack
- **Target**: Windows
- **Vulnerability**: Folder spoofing via shortcuts
- **MITRE**: T1204
- **Impact**: Virus spread, credential theft
- **Tools**: .lnk virus, batch script
- **Scenario**: USB with shortcut virus spreads to every folder opened.
- **Attack Steps**: Step 1: Place a .lnk virus that replicates itself on USB. Step 2: The shortcut links back to malicious scripts. Step 3: When victim browses USB, it gets copied to system folders. Step 4: Clicking folders triggers malware.
- **Detection**: AV, file extension monitoring
- **Solution**: Block .lnk files, scan USB on insert
- **Tags**: shortcut, virus, autorun, usb worm

## Bootkit Installation via USB ISO

- **Attack Type**: Removable Media Attack
- **Target**: BIOS/UEFI systems
- **Vulnerability**: Insecure boot sequence
- **MITRE**: T1542.002
- **Impact**: Persistent malware, full control
- **Tools**: Malicious ISO, Rufus
- **Scenario**: Bootable USB loads a rootkit into the system firmware or bootloader.
- **Attack Steps**: Step 1: Build or download malicious ISO file with rootkit. Step 2: Use Rufus to create bootable USB. Step 3: Reboot target machine with USB inserted. Step 4: If boot order allows, system loads from USB. Step 5: Rootkit installs into bootloader/MBR.
- **Detection**: BIOS boot logs, integrity checks
- **Solution**: Use Secure Boot, BIOS password
- **Tags**: rootkit, bootkit, mbr, firmware

## USB Phishing via Encrypted Document

- **Attack Type**: Removable Media Attack
- **Target**: Corporate PCs
- **Vulnerability**: Icon deception, file extensions hidden
- **MITRE**: T1566
- **Impact**: Malware execution
- **Tools**: PDF icon changer, malware binder
- **Scenario**: A USB holds a file named like "Encrypted_Invoice.pdf.exe" that tricks users into launching malware.
- **Attack Steps**: Step 1: Rename malware file to “.pdf.exe”. Step 2: Change icon to look like PDF. Step 3: Put on USB and hand it to target. Step 4: Victim double-clicks thinking it’s legit. Step 5: Malware runs, infects system.
- **Detection**: Endpoint AV alerts, file signature mismatch
- **Solution**: Enable full extension visibility
- **Tags**: pdf.exe, phishing, usb bait

## USB Powerline Communication Sniffing

- **Attack Type**: Removable Media Attack
- **Target**: Smart buildings
- **Vulnerability**: Powerline-based sniffing
- **MITRE**: T1040
- **Impact**: Data snooping
- **Tools**: USB Powerline Adapter
- **Scenario**: A USB-based powerline device is used to sniff data via building power cables.
- **Attack Steps**: Step 1: Insert USB powerline adapter in system. Step 2: It communicates over AC wiring. Step 3: Attacker places second device on same power circuit. Step 4: Sniffs data transferred over LAN or shared systems.
- **Detection**: Monitor abnormal network bridges
- **Solution**: Don’t allow untrusted PLC adapters
- **Tags**: usb, powerline, network sniff

## USB Wireless Dongle Replay Attack

- **Attack Type**: Removable Media Attack
- **Target**: Wireless keyboards
- **Vulnerability**: Lack of encryption in wireless dongles
- **MITRE**: T1056.001
- **Impact**: Credential theft, remote control
- **Tools**: MouseJack Tools, NRF24L01
- **Scenario**: USB dongle records wireless keyboard/mouse signals and replays them.
- **Attack Steps**: Step 1: Use MouseJack-compatible USB with wireless chip. Step 2: Record victim’s keystrokes remotely. Step 3: Replay commands later by broadcasting same signals. Step 4: No physical access needed after pairing.
- **Detection**: Use encrypted input devices
- **Solution**: Ban vulnerable dongles
- **Tags**: mousejack, wireless hijack, replay

## USB-C Alternate Mode Exploit

- **Attack Type**: Removable Media Attack
- **Target**: Modern laptops, phones
- **Vulnerability**: Unlocked alternate modes
- **MITRE**: T1548
- **Impact**: Debug access, firmware mods
- **Tools**: USB-C breakout board, serial console
- **Scenario**: USB-C is abused to access hidden interfaces like DisplayPort or Serial Debug.
- **Attack Steps**: Step 1: Connect USB-C debug tool. Step 2: Force it into alternate mode to expose internal debugging port. Step 3: Get low-level device access like console or firmware.
- **Detection**: Disable alt-mode, firmware security
- **Solution**: usb-c, alt mode, debug port
- **Tags**: Newer USB Attacks

## USB with Dangerous Capacitor Burst

- **Attack Type**: Removable Media Attack
- **Target**: Office PC
- **Vulnerability**: USB voltage access
- **MITRE**: T1491.002
- **Impact**: Distraction, physical theft
- **Tools**: DIY USB bomb, capacitor
- **Scenario**: A USB is rigged to burst small capacitor causing smoke/spark distraction.
- **Attack Steps**: Step 1: Install high voltage capacitor inside USB shell. Step 2: Connect to USB 5V rail. Step 3: When powered, capacitor bursts creating smoke/pop. Step 4: While people are distracted, attacker steals system or plants bug.
- **Detection**: Forensic inspection
- **Solution**: Ban unknown USBs
- **Tags**: distraction, physical theft, prank

## USB Backdoor through BIOS Update Tool

- **Attack Type**: Removable Media Attack
- **Target**: Firmware/UEFI
- **Vulnerability**: Fake firmware update
- **MITRE**: T1542.002
- **Impact**: Root-level persistence
- **Tools**: BIOS mod, signed fake tool
- **Scenario**: USB contains fake BIOS update utility which runs at boot and installs backdoor.
- **Attack Steps**: Step 1: Create a USB with “BIOS_Update.exe” file. Step 2: Trick admin/user to run it. Step 3: Installs payload into BIOS using firmware vulnerability.
- **Detection**: BIOS integrity checker
- **Solution**: Allow signed updates only
- **Tags**: bios update, usb backdoor

## USB Memory Overload Crash

- **Attack Type**: Removable Media Attack
- **Target**: Embedded systems
- **Vulnerability**: Memory handling flaw
- **MITRE**: T1499
- **Impact**: Denial of Service
- **Tools**: USB with huge invalid files
- **Scenario**: A USB floods the memory buffer of a system causing it to crash.
- **Attack Steps**: Step 1: Format USB and fill it with fake large files. Step 2: Place corrupted EXE or massive zeroed files. Step 3: Plug into low-RAM system. Step 4: When system tries to read, crashes or freezes.
- **Detection**: Log crash dumps
- **Solution**: Patch buffer handlers
- **Tags**: memory crash, overflow, usb bomb

## USB Barcode Scanner Command Injection

- **Attack Type**: Removable Media Attack
- **Target**: POS terminals, PCs
- **Vulnerability**: Trust in barcode scanners
- **MITRE**: T1059
- **Impact**: Command execution
- **Tools**: Programmable barcode scanner
- **Scenario**: An attacker uses a programmable barcode scanner to inject terminal commands when plugged into USB.
- **Attack Steps**: Step 1: Get a scanner that allows custom payloads. Step 2: Program it with barcodes that type terminal commands. Step 3: Connect it to PC via USB. Step 4: Scan the malicious barcode – it runs commands as if typed.
- **Detection**: Input behavior monitoring
- **Solution**: Restrict scanner input modes
- **Tags**: barcode, input injection, usb device

## USB Debug UART Exploit

- **Attack Type**: Removable Media Attack
- **Target**: IoT/Embedded Systems
- **Vulnerability**: Exposed debug UART port
- **MITRE**: T1040
- **Impact**: Unauthorized access, firmware dump
- **Tools**: USB to UART adapter
- **Scenario**: Using a USB-UART converter, attacker connects to debug interface on embedded device.
- **Attack Steps**: Step 1: Open embedded device case (router, IoT). Step 2: Locate UART pins (TX, RX, GND). Step 3: Connect USB-UART adapter to these pins. Step 4: Use terminal (PuTTY, minicom) to access root shell. Step 5: Dump firmware or modify settings.
- **Detection**: Hardware inspection
- **Solution**: Disable UART or use password/auth
- **Tags**: uart, debug port, serial hack

## USB Rubber Ducky in Power Strip

- **Attack Type**: Removable Media Attack
- **Target**: Office or public spaces
- **Vulnerability**: Tampered physical USB hub
- **MITRE**: T1204.002
- **Impact**: Command injection, malware drop
- **Tools**: USB Rubber Ducky, power hub
- **Scenario**: Attacker hides a USB payload device inside a power extension box with open USB ports.
- **Attack Steps**: Step 1: Embed USB payload inside a USB port of a power extension. Step 2: Leave the extension near victim. Step 3: Victim plugs into USB for charging. Step 4: Device injects keystrokes automatically.
- **Detection**: Device behavior logging
- **Solution**: Use data blockers, inspect hubs
- **Tags**: hidden device, power hub, ducky

## USB Voice Command Device

- **Attack Type**: Removable Media Attack
- **Target**: Smart homes, voice assistants
- **Vulnerability**: No authentication on voice
- **MITRE**: T1059
- **Impact**: Unauthorized command execution
- **Tools**: USB speaker + pre-recorded voice
- **Scenario**: A USB audio device issues voice commands to a smart assistant (e.g., Alexa).
- **Attack Steps**: Step 1: Program a USB speaker with voice commands (e.g., "Alexa, unlock door"). Step 2: Plug it into PC near smart assistant. Step 3: Audio plays commands to assistant. Step 4: Assistant performs actions without user knowing.
- **Detection**: Voice logs, mic alerts
- **Solution**: Use voiceprint auth, mute mic
- **Tags**: voice hack, usb speaker, assistant

## USB Drive with Fractal Partitioning

- **Attack Type**: Removable Media Attack
- **Target**: Windows systems
- **Vulnerability**: Limited AV scan depth
- **MITRE**: T1027
- **Impact**: Obfuscated malware delivery
- **Tools**: USB, partitioning tools
- **Scenario**: A USB is set up with recursive nested partitions to bypass scanners.
- **Attack Steps**: Step 1: Use Linux tools to create nested partitions (partition inside partition). Step 2: Store payload deep inside. Step 3: Share USB – regular scanners miss deep files. Step 4: Script accesses hidden location and runs malware.
- **Detection**: Deep scan tools
- **Solution**: Block recursive mount points
- **Tags**: partitions, obfuscation, stealth

## USB-C Docking Station Exploit

- **Attack Type**: Removable Media Attack
- **Target**: Corporate laptops
- **Vulnerability**: Docking station trust
- **MITRE**: T1200
- **Impact**: Command injection, persistence
- **Tools**: Tampered dock, Ducky payload
- **Scenario**: Modified docking station with USB-C adds hidden attack modules.
- **Attack Steps**: Step 1: Modify a USB-C dock to include Rubber Ducky or BLE chip. Step 2: Plug dock into victim laptop. Step 3: Payload runs as soon as dock is detected.
- **Detection**: Monitor docking devices
- **Solution**: Lock docks to users/devices
- **Tags**: usb-c, dock, stealth implant

## USB Steganography Payload

- **Attack Type**: Removable Media Attack
- **Target**: Any OS
- **Vulnerability**: Hidden payloads in media
- **MITRE**: T1027
- **Impact**: Obfuscated command delivery
- **Tools**: Stego tools (steghide), USB
- **Scenario**: Files hidden within images on USB avoid detection and carry commands.
- **Attack Steps**: Step 1: Use steghide to embed payload (like script) inside an image. Step 2: Store image on USB. Step 3: Victim opens image unaware. Step 4: Script extracts hidden data and executes it.
- **Detection**: Analyze image entropy
- **Solution**: Prevent stego tools, scan media
- **Tags**: stego, payload, hidden data

## USB-to-HDMI Keylogger

- **Attack Type**: Removable Media Attack
- **Target**: Conference room PCs
- **Vulnerability**: Trust in display devices
- **MITRE**: T1056.002
- **Impact**: Visual keylogging
- **Tools**: USB-HDMI adapter, microcontroller
- **Scenario**: A USB cable pretending to be HDMI captures screen and logs activity.
- **Attack Steps**: Step 1: Build a fake HDMI-to-USB adapter with sniffer chip. Step 2: Replace real cable. Step 3: When user uses screen, frames or logs are captured. Step 4: Logs stored on internal memory or sent via BLE.
- **Detection**: AV or HDMI device monitor
- **Solution**: Monitor USB display outputs
- **Tags**: usb-hdmi, visual tap, stealth cam

## USB Write Once Self-Destruct Drive

- **Attack Type**: Removable Media Attack
- **Target**: Secure endpoints
- **Vulnerability**: Anti-forensic behavior
- **MITRE**: T1070
- **Impact**: No trace of compromise
- **Tools**: WORM USB, custom chip
- **Scenario**: USB writes data once, then destroys its memory cells or erases content.
- **Attack Steps**: Step 1: Use special Write-Once USB or controller chip. Step 2: Copy files onto it – malware or payload. Step 3: On use, USB erases itself or burns NAND. Step 4: Prevents forensic analysis.
- **Detection**: USB audit, block WORM types
- **Solution**: Forensic USB scanning
- **Tags**: worm, usb burn, antiforensics

## USB Mass Email Payload via Outlook Script

- **Attack Type**: Removable Media Attack
- **Target**: Employee PCs
- **Vulnerability**: Email automation vulnerability
- **MITRE**: T1566.001
- **Impact**: Mass phishing from internal user
- **Tools**: VBA script, USB drive
- **Scenario**: USB auto-runs a script that launches Outlook and sends phishing emails.
- **Attack Steps**: Step 1: Write a VBScript to open Outlook and send email with malware attached. Step 2: Store it on USB. Step 3: Use Rubber Ducky to auto-run the script. Step 4: Victim’s system becomes unwitting sender.
- **Detection**: Email logs, anti-spam alert
- **Solution**: Limit scripting in email clients
- **Tags**: outlook, phishing, auto script

## USB with Fake Audio File Attack

- **Attack Type**: Removable Media Attack
- **Target**: Windows
- **Vulnerability**: Exploitable media parsing
- **MITRE**: T1204
- **Impact**: Media-based exploit
- **Tools**: Audio stego, mp3 payload
- **Scenario**: Audio file that plays nothing but carries embedded shellcode.
- **Attack Steps**: Step 1: Embed shellcode in ID3 tag of MP3 using tool. Step 2: Script extracts and executes payload from MP3 tag. Step 3: Victim plays “silent” audio.
- **Detection**: Media scanner alerts
- **Solution**: Block malformed media
- **Tags**: audio tag, shellcode, steganography

## USB-Based Secure Token Spoof

- **Attack Type**: Removable Media Attack
- **Target**: MFA systems
- **Vulnerability**: Weak token validation
- **MITRE**: T1111
- **Impact**: MFA Bypass
- **Tools**: Digispark, token emulator
- **Scenario**: USB device emulates secure token (like YubiKey) but provides attacker’s credentials.
- **Attack Steps**: Step 1: Emulate a security token USB. Step 2: When plugged in, it provides attacker’s keys instead of victim's. Step 3: Used in phishing or login bypass.
- **Detection**: Token signature checks
- **Solution**: Use strong cryptographic tokens
- **Tags**: mfa bypass, token spoof

## USB E-Book Trap

- **Attack Type**: Removable Media Attack
- **Target**: PDF readers
- **Vulnerability**: Reader vulnerabilities
- **MITRE**: T1203
- **Impact**: Exploit-based code execution
- **Tools**: Exploit PDF, USB stick
- **Scenario**: Malicious eBook file auto-opens when plugged in and runs macros or exploits reader bugs.
- **Attack Steps**: Step 1: Craft PDF using exploit kit (targeting Adobe Reader bug). Step 2: Name file like "Top10_Resume_Tips.pdf". Step 3: Place on USB. Step 4: When user opens, exploit runs.
- **Detection**: Patch monitoring
- **Solution**: Block unknown PDFs, sanitize
- **Tags**: pdf exploit, macro, ebook attack

## USB Thermal Attack on BIOS Sensor

- **Attack Type**: Removable Media Attack
- **Target**: Desktops
- **Vulnerability**: BIOS thermal override
- **MITRE**: T1491.001
- **Impact**: Hardware control bypass
- **Tools**: USB heating coil
- **Scenario**: USB heats up BIOS temperature sensor triggering shutdown or bypass.
- **Attack Steps**: Step 1: Insert USB with heating element. Step 2: Heat reaches BIOS thermal sensor. Step 3: System either shuts down or disables fan/sensors. Step 4: Use moment to access system or reset settings.
- **Detection**: Thermal logging
- **Solution**: Isolate thermal sensors
- **Tags**: hardware trick, heat sensor

## USB Disguised as Keyboard with Voice Typing

- **Attack Type**: Removable Media Attack
- **Target**: Windows 10/11
- **Vulnerability**: Voice typing abuse
- **MITRE**: T1059.003
- **Impact**: Scripted command execution
- **Tools**: USB mic, voice file
- **Scenario**: A USB mic triggers system’s voice typing, bypassing keystroke detection.
- **Attack Steps**: Step 1: Insert USB mic with pre-recorded voice commands. Step 2: Launch Windows Voice Typing with hotkey. Step 3: Playback voice script to type and execute commands.
- **Detection**: Voice activity logs
- **Solution**: Disable voice typing feature
- **Tags**: voice input, audio exploit

## USB Webcam Trigger via Motion

- **Attack Type**: Removable Media Attack
- **Target**: Personal or public PC
- **Vulnerability**: No webcam permissions
- **MITRE**: T1125
- **Impact**: Privacy breach
- **Tools**: USB webcam, PIR sensor
- **Scenario**: USB device activates webcam when motion is detected nearby.
- **Attack Steps**: Step 1: Build webcam device with motion sensor. Step 2: Configure it to start recording on movement. Step 3: Plug into victim machine. Step 4: Silent recording begins whenever user walks in.
- **Detection**: Webcam indicators, logs
- **Solution**: Enforce webcam policies
- **Tags**: webcam, motion record, spy cam

## USB Wireless Signal Jammer

- **Attack Type**: Removable Media Attack
- **Target**: Offices, IoT homes
- **Vulnerability**: Wireless interference
- **MITRE**: T1498
- **Impact**: DoS, network blackout
- **Tools**: USB jammer (e.g., Yard Stick One)
- **Scenario**: USB emits jamming signals that disrupt local Wi-Fi/Bluetooth.
- **Attack Steps**: Step 1: Plug jammer into USB power source. Step 2: Start script to broadcast constant signal on 2.4GHz. Step 3: Local wireless signals get disrupted.
- **Detection**: RF detection tools
- **Solution**: Shielded cables, Wi-Fi diversity
- **Tags**: wifi jam, ble block, usb rf

## USB Ethernet Adapter Spoof with Fake DHCP

- **Attack Type**: Removable Media Attack
- **Target**: PCs
- **Vulnerability**: DHCP auto-trust
- **MITRE**: T1040
- **Impact**: Traffic redirection, phishing
- **Tools**: USB LAN adapter + DHCP
- **Scenario**: USB adapter acts as rogue DHCP server to redirect victim traffic.
- **Attack Steps**: Step 1: Modify adapter to serve DHCP IP + DNS. Step 2: Victim plugs into USB – system believes it’s LAN. Step 3: Traffic is routed to attacker-controlled IP.
- **Detection**: Network alerting, rogue IPs
- **Solution**: Restrict DHCP to specific interfaces
- **Tags**: dhcp, spoof lan, traffic hijack

## USB Dock with Integrated GSM Bug

- **Attack Type**: Removable Media Attack
- **Target**: Offices, conference rooms
- **Vulnerability**: Docking trust, audio access
- **MITRE**: T1123
- **Impact**: Espionage, surveillance
- **Tools**: USB dock, GSM module (SIM800L)
- **Scenario**: USB dock is modified with a GSM module that transmits audio or data remotely.
- **Attack Steps**: Step 1: Open USB dock and hide GSM module with microphone. Step 2: Insert SIM card and set auto-dial to attacker phone number. Step 3: Plug dock into victim laptop. Step 4: Microphone picks up nearby audio and dials attacker silently. Step 5: Attacker listens live from remote mobile.
- **Detection**: Audio spike analysis
- **Solution**: Inspect dock internals, disable audio
- **Tags**: gsm, surveillance, hardware tap

## USB Overvoltage for System Bypass

- **Attack Type**: Removable Media Attack
- **Target**: Security monitoring PCs
- **Vulnerability**: Power line protection flaw
- **MITRE**: T1491.002
- **Impact**: Bypass sensors, log suppression
- **Tools**: USB voltage booster, relay
- **Scenario**: Modified USB delivers high voltage to momentarily disable monitoring hardware.
- **Attack Steps**: Step 1: Modify USB with voltage boosting circuit. Step 2: Trigger brief surge on insertion to overload sensors. Step 3: While system resets sensors, attacker gains access. Step 4: Surge disappears; hardware appears normal.
- **Detection**: Voltage fluctuation logs
- **Solution**: Use surge protectors, USB firewalls
- **Tags**: overvoltage, log bypass, power glitch

## USB GPS Spoofing Device

- **Attack Type**: Removable Media Attack
- **Target**: GPS-based tracking systems
- **Vulnerability**: GPS data trust
- **MITRE**: T1602.001
- **Impact**: Fake tracking, compliance fraud
- **Tools**: GPS emulator, GPS-SDR
- **Scenario**: USB presents as a GPS device and feeds fake location data.
- **Attack Steps**: Step 1: Flash microcontroller to simulate NMEA GPS data. Step 2: Send coordinates to simulate fake travel or movements. Step 3: Plug into GPS-tracked system. Step 4: Tracking software believes fake location is real.
- **Detection**: Cross-check GPS with IP/time
- **Solution**: Use dual-source location validation
- **Tags**: gps spoof, tracking evasion

## USB-Based CPU Fan Speed Exploit

- **Attack Type**: Removable Media Attack
- **Target**: Desktops
- **Vulnerability**: Fan control via firmware
- **MITRE**: T1499
- **Impact**: Denial of Service, thermal damage
- **Tools**: Custom USB device, low-level API access
- **Scenario**: USB triggers firmware call that disables or stalls CPU fan.
- **Attack Steps**: Step 1: Create firmware exploit to talk to ACPI/SMBus. Step 2: Store it on USB Rubber Ducky. Step 3: Inject payload that disables fan temporarily. Step 4: CPU overheats → thermal trip → shutdown.
- **Detection**: Hardware logs, temp sensors
- **Solution**: Fan control hardening, firmware lock
- **Tags**: cpu fan, acpi, thermal dos

## USB Hidden Wi-Fi Beacon for Exfil

- **Attack Type**: Removable Media Attack
- **Target**: Air-gapped or isolated PCs
- **Vulnerability**: Wi-Fi beacon abuse
- **MITRE**: T1020
- **Impact**: Stealth exfil over wireless
- **Tools**: USB Wi-Fi stick, beacon script
- **Scenario**: USB sends stolen data over Wi-Fi from a hidden SSID broadcast.
- **Attack Steps**: Step 1: Program USB Wi-Fi dongle to act as beacon host. Step 2: Encode stolen data into SSID strings. Step 3: Nearby device captures SSID broadcast and decodes data. Step 4: No formal connection needed; just signal exposure.
- **Detection**: Wi-Fi anomaly detection
- **Solution**: Block rogue Wi-Fi signals, RF shielding
- **Tags**: wifi beacon, data leak, covert

## USB Human Interface Fuzzer

- **Attack Type**: Removable Media Attack
- **Target**: Workstations
- **Vulnerability**: Input stack vulnerability
- **MITRE**: T1499.004
- **Impact**: Crash, remote execution
- **Tools**: HID fuzzer firmware, Teensy/Arduino
- **Scenario**: USB injects fuzzed (random) keyboard/mouse inputs to crash system or exploit input handlers.
- **Attack Steps**: Step 1: Flash USB device with random keystroke generator. Step 2: Insert into target machine. Step 3: Device injects random/long strings or mouse moves. Step 4: May crash input driver, buffer overflow, or UI freeze.
- **Detection**: HID activity logging
- **Solution**: Harden input APIs
- **Tags**: hid, fuzz, crash injection

## USB Drive with Timed Payload Execution

- **Attack Type**: Removable Media Attack
- **Target**: Windows, Mac, Linux
- **Vulnerability**: AV timing evasion
- **MITRE**: T1027.002
- **Impact**: Stealthy malware delivery
- **Tools**: Rubber Ducky, time-delay script
- **Scenario**: USB waits a set amount of time before running its payload, evading detection.
- **Attack Steps**: Step 1: Script delay into payload (e.g., wait 3 minutes). Step 2: Insert USB into target. Step 3: No activity → bypasses sandbox or AV checks. Step 4: Executes payload after delay.
- **Detection**: Behavior over time monitoring
- **Solution**: Use behavioral AI AVs
- **Tags**: payload delay, sandbox bypass

## USB-C to Thunderbolt Privilege Escalation

- **Attack Type**: Removable Media Attack
- **Target**: Thunderbolt-enabled PCs
- **Vulnerability**: Thunderbolt DMA trust
- **MITRE**: T1018
- **Impact**: Full memory access, kernel exploit
- **Tools**: Thunderbolt device, DMA tool
- **Scenario**: USB-C device escalates to DMA (Direct Memory Access) via Thunderbolt.
- **Attack Steps**: Step 1: Plug USB-C device with Thunderbolt into unlocked system. Step 2: Access memory directly using DMA tool. Step 3: Inject code into kernel or extract passwords.
- **Detection**: BIOS DMA logs, hardware isolation
- **Solution**: Disable Thunderbolt in firmware
- **Tags**: dma, thunderbolt, memory attack

## USB Video Frame Injection

- **Attack Type**: Removable Media Attack
- **Target**: Security monitoring systems
- **Vulnerability**: Video spoofing via USB
- **MITRE**: T1601
- **Impact**: Surveillance bypass
- **Tools**: UVC cam mod, video file
- **Scenario**: USB cam sends pre-recorded video instead of live feed to fool surveillance.
- **Attack Steps**: Step 1: Modify webcam firmware to play looped video feed. Step 2: Plug into surveillance station or laptop. Step 3: Viewer sees fake "live" footage while real activity is hidden.
- **Detection**: Video feed integrity check
- **Solution**: Trusted UVC device verification
- **Tags**: video injection, fake cam

## USB-to-SATA Data Skimmer

- **Attack Type**: Removable Media Attack
- **Target**: Forensics or disk imaging setups
- **Vulnerability**: Trust in physical cable
- **MITRE**: T1005
- **Impact**: Stealth data extraction
- **Tools**: USB-to-SATA bridge + logger
- **Scenario**: USB converter cable skims hard disk data when plugged inline.
- **Attack Steps**: Step 1: Modify USB-SATA adapter to include logging chip. Step 2: Plug target hard drive into modified adapter. Step 3: Extract and store data on internal flash silently.
- **Detection**: Monitor data access logs
- **Solution**: Use sealed forensic hardware
- **Tags**: sata, disk clone, usb tap

## UART Debug Console Access

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Device
- **Vulnerability**: Exposed debug interface
- **MITRE**: T1040 (Access Console Interface)
- **Impact**: Root shell access
- **Tools**: USB-to-TTL serial adapter, jumper wires, terminal software (PuTTY, minicom)
- **Scenario**: Attacker connects to exposed UART (Universal Asynchronous Receiver/Transmitter) pins on an embedded device to access console or shell
- **Attack Steps**: Step 1: Open the target device and locate UART pins usually marked TX, RX, GND on the board. Step 2: Connect USB-to-TTL adapter to these pins (TX to RX, RX to TX, GND to GND). Step 3: Plug the adapter into your computer and open a terminal program like PuTTY. Step 4: Try common baud rates (115200, 57600, etc.) until you get readable text. Step 5: If the terminal shows login prompt or shell, try default credentials like root or admin. Step 6: If login successful, explore system using commands like ls, cat /etc/passwd, etc.
- **Detection**: Monitor for physical tampering and unexpected UART traffic
- **Solution**: Disable UART in production, or password-protect access
- **Tags**: UART, Debugging, Firmware

## JTAG Chip Memory Dump

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Microcontroller
- **Vulnerability**: Enabled debug port with no authentication
- **MITRE**: T1055 (Process Injection), T1600 (Hardware Reverse Engineering)
- **Impact**: Full firmware dump and possible code injection
- **Tools**: JTAGulator, OpenOCD, J-Link, PC
- **Scenario**: Attacker accesses the JTAG interface to dump memory or modify firmware on a microcontroller
- **Attack Steps**: Step 1: Open device casing and locate JTAG header/pins (often labeled TDI, TDO, TCK, TMS, GND, VCC). Step 2: Use JTAGulator or datasheet to identify correct pinout. Step 3: Connect a JTAG debugger (e.g., Segger J-Link) to the interface. Step 4: Use software like OpenOCD to connect and halt CPU. Step 5: Issue command to dump memory or read firmware image. Step 6: Analyze dumped firmware to extract secrets or insert backdoor.
- **Detection**: Hardware probe detection or case tamper switch
- **Solution**: Disable JTAG in production or use secure JTAG
- **Tags**: JTAG, Firmware Dump, Reverse Engineering

## SPI Flash Dump via Clip

- **Attack Type**: Hardware Interface Exploitation
- **Target**: SPI Flash Chip
- **Vulnerability**: Unencrypted SPI firmware
- **MITRE**: T1600, T1027.002 (Firmware Extraction)
- **Impact**: Dump and offline analysis of firmware
- **Tools**: SOIC8/SOIC16 clip, Flashrom, Raspberry Pi or Bus Pirate
- **Scenario**: Attacker reads firmware from SPI flash chip using a SOIC clip without desoldering
- **Attack Steps**: Step 1: Identify the SPI flash chip on the board (e.g., Winbond W25Q64). Step 2: Attach SOIC clip to the chip carefully while powering the board. Step 3: Connect clip to a Raspberry Pi using GPIO or use a Bus Pirate. Step 4: Use Flashrom software to detect and read the chip: flashrom -p linux_spi:dev=/dev/spidev0.0 -r dump.bin. Step 5: Save the dump.bin file and analyze it using a hex editor or Binwalk. Step 6: Extract filesystems or hardcoded credentials from firmware.
- **Detection**: Monitor for device opening or case tampering
- **Solution**: Encrypt firmware and glue chip to board
- **Tags**: SPI, Flash Dump, Firmware Analysis

## I2C EEPROM Credential Dump

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Device
- **Vulnerability**: Unprotected EEPROM data
- **MITRE**: T1600, T1005 (Data from Local System)
- **Impact**: Disclosure of stored credentials
- **Tools**: EEPROM reader, Arduino/Raspberry Pi, I2C scanning code
- **Scenario**: Attacker extracts passwords or configurations stored in I2C EEPROM chips
- **Attack Steps**: Step 1: Find the I2C EEPROM on board (e.g., 24C02, 24C64). Step 2: Connect Arduino or Pi to SDA, SCL, GND pins of the EEPROM. Step 3: Upload I2C scanner code to Arduino to detect device address. Step 4: Use I2C read commands to dump the content byte by byte. Step 5: Save data to a text or binary file. Step 6: Look for readable strings or credentials in dumped content.
- **Detection**: Hardware probe alert or checksum errors
- **Solution**: Store sensitive data in encrypted formats
- **Tags**: EEPROM, Credential Dump, I2C

## USB Debug Interface Abuse

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Device / Mobile
- **Vulnerability**: USB Debug Mode left enabled
- **MITRE**: T1518.001 (Software Discovery), T1600
- **Impact**: Root access or firmware overwrite
- **Tools**: USB cable, ADB tools / dfu-util / custom scripts
- **Scenario**: Attacker abuses open USB debug mode (like ADB on Android or DFU on IoT) to gain shell or flash firmware
- **Attack Steps**: Step 1: Plug USB into the target device and connect to computer. Step 2: Run adb devices to check if device is in debug mode. Step 3: If found, run adb shell to get command access. Step 4: Run commands like ls, cat, or pm list packages to explore device. Step 5: Optionally, install APK or download data. Step 6: If device is in DFU mode, use dfu-util -l and dfu-util -U firmware.bin to dump or flash firmware.
- **Detection**: Monitor USB port activity
- **Solution**: Disable USB debug or require auth
- **Tags**: ADB, DFU, USB Abuse

## UART Root Shell via Boot Interrupt

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded System
- **Vulnerability**: Bootloader lacks authentication
- **MITRE**: T1542.001 (Pre-OS Boot)
- **Impact**: Shell access bypassing login
- **Tools**: USB-to-TTL adapter, PuTTY/minicom, jumper wires
- **Scenario**: Attacker uses UART to interrupt the bootloader process and gain shell access without credentials
- **Attack Steps**: Step 1: Connect UART to embedded board using TX, RX, GND. Step 2: Start terminal and reboot device. Step 3: Watch output; if bootloader says "Press any key to interrupt boot", press key quickly. Step 4: Gain access to bootloader console. Step 5: Type bootargs or printenv to check configuration. Step 6: Try to boot with parameters like init=/bin/sh for direct shell access.
- **Detection**: Monitor bootlog interrupts
- **Solution**: Disable boot console or add password
- **Tags**: UART, U-Boot, Boot Bypass

## Unprotected I2C Touchscreen Backdoor

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Touchscreen Controller
- **Vulnerability**: Insecure I2C configuration
- **MITRE**: T1600, T1202
- **Impact**: Control over user input system
- **Tools**: I2C sniffer (logic analyzer), Arduino, Pi
- **Scenario**: I2C touchscreen controller gives access to configuration via bus probing
- **Attack Steps**: Step 1: Locate the I2C interface near display on device PCB. Step 2: Connect SDA/SCL to Arduino or logic analyzer. Step 3: Use I2C tools (i2cdetect, i2cdump) to read register map. Step 4: Access configuration bytes that control behavior (e.g., gestures). Step 5: Modify registers to simulate inputs or disable touch security.
- **Detection**: No tamper alert or bus integrity check
- **Solution**: Implement I2C authentication or secure overlays
- **Tags**: Touch Interface, I2C Abuse

## SWD Interface Access for Firmware Dump

- **Attack Type**: Hardware Interface Exploitation
- **Target**: ARM MCU
- **Vulnerability**: Unlocked SWD debug interface
- **MITRE**: T1600
- **Impact**: Firmware reverse engineering
- **Tools**: ST-Link, OpenOCD, Raspberry Pi
- **Scenario**: Attacker uses Serial Wire Debug (SWD) interface to dump flash from ARM Cortex MCU
- **Attack Steps**: Step 1: Locate SWD pins (SWDIO, SWCLK, GND, VCC) on the PCB. Step 2: Connect ST-Link or Pi SWD interface. Step 3: Use openocd to interface with the MCU. Step 4: Halt MCU and use dump_image command to save firmware to local file. Step 5: Analyze image for hardcoded passwords or logic.
- **Detection**: Hardware probe detection, debugging lock
- **Solution**: Lock SWD after development
- **Tags**: SWD, Debug, ARM

## Exploiting USB OTG with Rogue Peripheral

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Device
- **Vulnerability**: OTG port allows HID peripherals
- **MITRE**: T1204.002, T1059.001
- **Impact**: Arbitrary command execution
- **Tools**: USB Rubber Ducky, USB OTG cable
- **Scenario**: A rogue USB device like Rubber Ducky is used via OTG to execute commands on an IoT device
- **Attack Steps**: Step 1: Prepare Rubber Ducky payload (e.g., open terminal, run wget malicious.sh). Step 2: Plug Rubber Ducky into OTG port of target device. Step 3: Device thinks it's a keyboard and executes commands as input. Step 4: Payload executes with user or root permissions.
- **Detection**: Monitor OTG events
- **Solution**: Disable OTG, whitelist USB devices
- **Tags**: USB HID, Rubber Ducky

## Logic Analyzer on SPI Bus

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Device
- **Vulnerability**: Unencrypted SPI traffic
- **MITRE**: T1040 (Network Sniffing - Bus)
- **Impact**: Credential or config leakage
- **Tools**: Saleae Logic Analyzer, PulseView
- **Scenario**: Attacker uses logic analyzer to sniff SPI traffic and extract sensitive data
- **Attack Steps**: Step 1: Identify SPI pins (MISO, MOSI, CLK, CS) near flash or display. Step 2: Attach logic analyzer probes to the pins. Step 3: Start capture software like PulseView. Step 4: Trigger capture during device operation. Step 5: Decode traffic using SPI protocol decoder to find plaintext data.
- **Detection**: Hardware anomaly detection
- **Solution**: Encrypt SPI communication
- **Tags**: Logic Analyzer, SPI Sniffing

## HDMI EDID Spoofing for Video Injection

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Media Player / CCTV / Kiosk
- **Vulnerability**: No validation of EDID
- **MITRE**: T1203, T1600
- **Impact**: Visual data leakage or manipulation
- **Tools**: EDID emulator, HDMI splitter
- **Scenario**: Attacker spoofs EDID (Extended Display Identification Data) via HDMI to make device trust rogue display
- **Attack Steps**: Step 1: Connect HDMI emulator to a device between real display. Step 2: Configure EDID spoof to advertise false resolutions or capabilities. Step 3: When device boots, it reads the false EDID and adapts display output. Step 4: Use this to mirror, distort, or redirect visual output.
- **Detection**: Monitor HDMI link or signal profile
- **Solution**: Lock to known EDID values
- **Tags**: EDID, HDMI, Spoofing

## Exploit Test Points on PCB

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Any PCB-based Device
- **Vulnerability**: Exposed unlabelled test pads
- **MITRE**: T1600
- **Impact**: Access to internals, signals, buses
- **Tools**: Multimeter, Logic analyzer, Soldering tools
- **Scenario**: Test points (tiny gold pads) on PCB give internal access to power, buses, or debug lines
- **Attack Steps**: Step 1: Visually identify test points marked as TP1, TP2, etc. Step 2: Use multimeter in continuity mode to trace where they connect. Step 3: Probe with logic analyzer to detect signals. Step 4: If signal is UART/SPI/I2C, connect appropriate tools. Step 5: Use decoded data or inject custom signal.
- **Detection**: PCB shielding, potting
- **Solution**: Remove unused test points in final design
- **Tags**: Test Points, PCB, Reverse Engineering

## NFC Debug Interface Hijack

- **Attack Type**: Hardware Interface Exploitation
- **Target**: NFC Reader
- **Vulnerability**: Debug port not locked or filtered
- **MITRE**: T1203, T1600
- **Impact**: Unauthorized NFC command injection
- **Tools**: NFC Debug Probe, Logic Analyzer
- **Scenario**: NFC controller exposes internal registers via debug protocol like I2C or UART
- **Attack Steps**: Step 1: Identify NFC chip on board (e.g., NXP, ST). Step 2: Locate debug lines connected to chip. Step 3: Attach logic analyzer and capture signals during use. Step 4: Replay captured NFC commands or modify them. Step 5: If registers are writable, inject custom command to modify NFC behavior.
- **Detection**: NFC behavior anomaly alerts
- **Solution**: Disable debug mode after development
- **Tags**: NFC, Debug Interface

## Glitching via Voltage Control

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Device
- **Vulnerability**: No brown-out or fault detection
- **MITRE**: T1600, T1499.004
- **Impact**: Bypass authentication or secure boot
- **Tools**: ChipWhisperer, Adjustable Power Supply
- **Scenario**: Power glitching is used to cause timing faults to bypass secure boot or password checks
- **Attack Steps**: Step 1: Connect ChipWhisperer to target power line (e.g., VCC). Step 2: Program it to momentarily drop or spike voltage during boot. Step 3: Reboot device and time glitch near check (e.g., secure boot). Step 4: If timing successful, device skips password or executes unsigned code. Step 5: Use result to extract data or install custom firmware.
- **Detection**: Power signal anomaly monitoring
- **Solution**: Add voltage fault detection
- **Tags**: Power Glitch, Secure Bypass

## SD Card Sniffing on Exposed SPI

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Device with SD card
- **Vulnerability**: SPI mode unencrypted file access
- **MITRE**: T1040, T1005
- **Impact**: Data exfiltration via bus sniff
- **Tools**: Logic analyzer, SD tap adapter
- **Scenario**: SD cards in SPI mode leak file I/O; attacker taps into bus to observe file access or extract data
- **Attack Steps**: Step 1: Identify microSD interface in SPI mode on board. Step 2: Connect logic analyzer to CLK, CMD, DAT0. Step 3: Capture traffic while device reads/writes SD card. Step 4: Decode protocol using analyzer software. Step 5: Extract file names, content, or credentials in plaintext.
- **Detection**: Monitor SD traffic or use encryption
- **Solution**: Use full-disk SD encryption or eMMC
- **Tags**: SD Sniff, SPI, File Access

## SOIC Clip Firmware Injection

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Device / Router
- **Vulnerability**: Writable SPI flash with no protection
- **MITRE**: T1542.001, T1600
- **Impact**: Full control over device
- **Tools**: SOIC clip, Flashrom, Custom firmware, Raspberry Pi
- **Scenario**: Using a clip on flash chip, attacker writes modified firmware without desoldering
- **Attack Steps**: Step 1: Locate flash chip and attach SOIC clip. Step 2: Connect clip to Raspberry Pi GPIO or USB programmer. Step 3: Backup original firmware using flashrom. Step 4: Modify firmware (e.g., add a backdoor shell). Step 5: Use flashrom -w to write new firmware back. Step 6: Reboot device and test modified behavior.
- **Detection**: Flash checksum or boot validation
- **Solution**: Sign firmware & enforce secure boot
- **Tags**: SOIC Clip, Firmware Injection

## BMC UART Hijack

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Data Center Server
- **Vulnerability**: UART interface not disabled
- **MITRE**: T1059, T1600
- **Impact**: Remote server control
- **Tools**: USB-to-TTL, terminal (minicom, PuTTY)
- **Scenario**: Attacker connects to UART port of a Baseboard Management Controller (BMC) on a server
- **Attack Steps**: Step 1: Open server chassis and locate BMC debug header. Step 2: Connect USB-to-TTL adapter (TX, RX, GND). Step 3: Reboot server, observe UART output. Step 4: Try known default login creds (e.g., admin/admin). Step 5: If successful, gain control over power, fans, firmware.
- **Detection**: Tamper detection or audit logs
- **Solution**: Secure UART with login or disable
- **Tags**: BMC, UART, IPMI

## Exploiting PCIe Debug Header

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Workstation / Industrial PC
- **Vulnerability**: Open PCIe debug with DMA
- **MITRE**: T1600, T1040
- **Impact**: Read/write arbitrary host memory
- **Tools**: FPGA board, PCIe adapter
- **Scenario**: Using PCIe debug header to access host memory or bus
- **Attack Steps**: Step 1: Find mini PCIe debug headers on the board. Step 2: Connect PCIe interface to FPGA. Step 3: Use logic or script to snoop memory access. Step 4: Read configuration space, DMA memory, or sniff secrets. Step 5: Optionally inject crafted packets.
- **Detection**: Monitor PCIe activity
- **Solution**: Disable debug features post manufacturing
- **Tags**: PCIe, DMA Attack

## I2C Real-Time Clock (RTC) Tampering

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Controller / DVR
- **Vulnerability**: No protection of RTC interface
- **MITRE**: T1565.002
- **Impact**: Log manipulation or time bypass
- **Tools**: I2C writer (Arduino, Pi), i2cset
- **Scenario**: Attacker modifies date/time via I2C to disrupt logs or timed actions
- **Attack Steps**: Step 1: Locate I2C RTC chip (e.g., DS1307). Step 2: Connect SDA/SCL to Raspberry Pi or Arduino. Step 3: Use i2cdetect to find the device address. Step 4: Use i2cset to change time registers. Step 5: Logs now show false timestamps or scheduled tasks shift.
- **Detection**: Timestamp integrity validation
- **Solution**: Battery-backed secure clock
- **Tags**: RTC, I2C, Time Manipulation

## Open Debug USB on MCU

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Consumer Device / Smart Gadget
- **Vulnerability**: USB debug not disabled
- **MITRE**: T1542.001
- **Impact**: Arbitrary code execution
- **Tools**: ST-Link, dfu-util, USB cable
- **Scenario**: Microcontroller exposes DFU or SWD via USB, allowing attacker to overwrite code
- **Attack Steps**: Step 1: Connect device via USB. Step 2: Use dfu-util -l to detect device in DFU mode. Step 3: Use dfu-util -U backup.bin to dump firmware. Step 4: Modify firmware (e.g., bypass password check). Step 5: Use dfu-util -D modded.bin to flash altered code.
- **Detection**: USB forensic analysis
- **Solution**: Lock bootloader or disable DFU
- **Tags**: DFU, USB Exploit

## CPLD/FPGA Bitstream Interception

- **Attack Type**: Hardware Interface Exploitation
- **Target**: FPGA / CPLD Board
- **Vulnerability**: Bitstream not encrypted
- **MITRE**: T1600, T1203
- **Impact**: IP theft, logic injection
- **Tools**: JTAG cable, ChipWhisperer, Flash reader
- **Scenario**: Bitstream for FPGA or CPLD is read directly to reverse logic
- **Attack Steps**: Step 1: Locate JTAG header or bitstream interface. Step 2: Connect programmer and halt device. Step 3: Dump bitstream using tools like iMPACT or xc3sprog. Step 4: Analyze logic to understand circuit or inject Trojan.
- **Detection**: Checksum mismatch or active logic protection
- **Solution**: Encrypt bitstream
- **Tags**: FPGA, Reverse Engineering

## LCD SPI Bus Snooping

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Any device with SPI LCD
- **Vulnerability**: SPI data not encrypted
- **MITRE**: T1040, T1005
- **Impact**: UI data exfiltration
- **Tools**: Logic analyzer, PulseView
- **Scenario**: Attack captures data on LCD SPI line to reveal UI content or passwords
- **Attack Steps**: Step 1: Identify SPI pins to LCD (CLK, MOSI). Step 2: Connect analyzer probes and capture screen data. Step 3: Decode binary stream into bitmaps or text. Step 4: Use image tools to recreate visuals. Step 5: If login screen is shown, extract typed passwords.
- **Detection**: Visual data anomaly monitoring
- **Solution**: Encrypt screen data or use secure bus
- **Tags**: LCD, SPI, Info Leak

## Fault Injection via EM Pulse

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Secure MCU / Smartcard
- **Vulnerability**: Lacks EM shielding
- **MITRE**: T1499.004
- **Impact**: PIN bypass, secure mode entry
- **Tools**: EM probe, ChipWhisperer, oscilloscope
- **Scenario**: Use of electromagnetic pulse to skip security checks in chip
- **Attack Steps**: Step 1: Position EM probe near target chip. Step 2: Use oscilloscope to find timing of password check. Step 3: Trigger EM pulse at precise moment to flip logic. Step 4: Device may skip PIN check or crash into boot mode.
- **Detection**: EM noise monitoring
- **Solution**: Use shielding & tamper detection
- **Tags**: EM Injection, Fault Attack

## RAM Bus Probing

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Board with DRAM
- **Vulnerability**: RAM bus unencrypted
- **MITRE**: T1040
- **Impact**: Real-time data leak
- **Tools**: Logic analyzer (32+ channels), Oscilloscope
- **Scenario**: Attacker probes parallel RAM buses to capture plaintext data
- **Attack Steps**: Step 1: Locate DRAM chip and trace address/data pins. Step 2: Connect logic analyzer to bus. Step 3: Record during power-on or operation. Step 4: Decode address/data cycles to extract values. Step 5: Filter for sensitive keywords, e.g., password.
- **Detection**: Signal line tamper detection
- **Solution**: Encrypt memory or use secure RAM
- **Tags**: RAM, Bus Probing

## Backdoor via Debug Serial EEPROM

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Consumer Electronics
- **Vulnerability**: Boot flags stored in EEPROM
- **MITRE**: T1600, T1542
- **Impact**: Secure boot disable, debug unlock
- **Tools**: EEPROM reader, i2c-tools
- **Scenario**: Hidden serial EEPROM stores boot override options
- **Attack Steps**: Step 1: Locate EEPROM chip (e.g., 24LC256) near MCU. Step 2: Dump EEPROM using i2cdump or reader. Step 3: Modify byte that disables secure boot or enables debug. Step 4: Write back altered data using i2cset. Step 5: Reboot device and gain boot bypass or shell.
- **Detection**: Boot log verification
- **Solution**: Lock EEPROM access post production
- **Tags**: EEPROM, Boot Flags, Debug Unlock

## Serial Port Bootloader Access

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Device
- **Vulnerability**: Open bootloader with no auth
- **MITRE**: T1542.001
- **Impact**: Firmware overwrite, full access
- **Tools**: USB-TTL adapter, TeraTerm / PuTTY
- **Scenario**: Bootloader interface exposed via UART allows firmware overwrite without login
- **Attack Steps**: Step 1: Locate UART pins and connect to computer via adapter. Step 2: Power on device and press key to stop autoboot. Step 3: Use bootloader command (like loadb, loady, update) to send firmware. Step 4: Upload custom firmware and reboot. Step 5: Firmware with added backdoor now runs on device.
- **Detection**: Monitor firmware changes
- **Solution**: Lock bootloader, use signed images
- **Tags**: UART, Bootloader, Firmware

## GPIO Abuse via Headers

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded System
- **Vulnerability**: Exposed GPIO with no protection
- **MITRE**: T1600
- **Impact**: State manipulation or bypass
- **Tools**: Jumper wires, multimeter, Raspberry Pi
- **Scenario**: Attacker manipulates exposed GPIO headers to alter device logic or bypass protections
- **Attack Steps**: Step 1: Identify GPIO header on board. Step 2: Refer to datasheet or measure voltages to find useful pins. Step 3: Pull reset pin low to reboot, or data pin high to trigger unlock. Step 4: In some cases, toggle pins to enter maintenance/debug mode. Step 5: Combine with other interfaces for access.
- **Detection**: Electrical monitoring or watchdogs
- **Solution**: Disable unused GPIOs, use pull resistors
- **Tags**: GPIO, Header Hack

## RS-232 Serial Console Access

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Industrial Controller / Legacy System
- **Vulnerability**: No password or weak auth on console
- **MITRE**: T1059, T1600
- **Impact**: Full system access
- **Tools**: RS-232 cable, DB9-to-USB converter, terminal software
- **Scenario**: Exploiting legacy RS-232 ports to access system terminal
- **Attack Steps**: Step 1: Plug RS-232 cable into device and connect to PC. Step 2: Use software like TeraTerm with common settings (9600 8N1). Step 3: Observe output for login shell. Step 4: Try default credentials or brute-force password if allowed. Step 5: Explore file system or modify config via shell.
- **Detection**: Console audit logging
- **Solution**: Use secure shell and disable serial console
- **Tags**: RS232, Legacy Access

## SPI Bus Injection with Arduino

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Device
- **Vulnerability**: No message signing on SPI
- **MITRE**: T1600
- **Impact**: Unauthorized command injection
- **Tools**: Arduino, SPI jumper wires, SPI library
- **Scenario**: Use Arduino to send fake commands over SPI to trick the device
- **Attack Steps**: Step 1: Connect Arduino’s MOSI/SCK/GND to target’s SPI interface. Step 2: Write script to send specific command (e.g., unlock or config update). Step 3: Power device and run Arduino script during boot. Step 4: If command accepted, device behavior changes (e.g., unlocks features).
- **Detection**: SPI command logging
- **Solution**: Verify commands via signatures
- **Tags**: Arduino, SPI Inject

## Debug Interface on USB Device Controller

- **Attack Type**: Hardware Interface Exploitation
- **Target**: USB Device Controller
- **Vulnerability**: Debug port not disabled
- **MITRE**: T1600, T1518.001
- **Impact**: Firmware extraction or control
- **Tools**: USB cable, OpenOCD or vendor SDK
- **Scenario**: Device controller exposes debug interface for developers, left open in production
- **Attack Steps**: Step 1: Connect USB to host PC. Step 2: Use vendor SDK or OpenOCD to scan for debug interface. Step 3: If detected, halt CPU and read memory or logs. Step 4: Dump firmware or inject debug instructions.
- **Detection**: USB behavior anomaly
- **Solution**: Disable debug in release builds
- **Tags**: USB Debug Port, Open Access

## Unused Ethernet Port for Shell

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT/Router/Sensor
- **Vulnerability**: Open network service via hardware port
- **MITRE**: T1059.003
- **Impact**: Backdoor access
- **Tools**: Ethernet cable, Nmap, Netcat
- **Scenario**: Ethernet port on device opens shell on specific port or trigger
- **Attack Steps**: Step 1: Connect to Ethernet port on device. Step 2: Use nmap to scan open ports (e.g., 23, 2323, 8080). Step 3: Connect using Netcat or Telnet. Step 4: Try commands or default credentials. Step 5: Gain shell or backdoor control if vulnerable.
- **Detection**: Network port monitoring
- **Solution**: Close unused services and ports
- **Tags**: Ethernet Port Shell, Telnet

## Reset Pin Hold for Boot Skip

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Microcontroller
- **Vulnerability**: Boot pin exposed
- **MITRE**: T1542.001
- **Impact**: Security bypass at boot
- **Tools**: Jumper wire or test hook
- **Scenario**: Holding the reset or boot pin alters boot sequence to unlock device
- **Attack Steps**: Step 1: Locate reset or boot mode pin near microcontroller. Step 2: Hold pin low or high (based on datasheet) during power on. Step 3: Device enters recovery or maintenance mode. Step 4: Gain shell or firmware upload interface without login.
- **Detection**: Boot logs or mode check
- **Solution**: Disable boot mode access via GPIO
- **Tags**: Reset Pin Hack, Mode Jump

## Exploiting USB Mass Storage Emulation

- **Attack Type**: Hardware Interface Exploitation
- **Target**: USB Peripheral
- **Vulnerability**: Logs/configs stored in accessible storage
- **MITRE**: T1005, T1203
- **Impact**: Data leak or manipulation
- **Tools**: USB cable, PC, file explorer
- **Scenario**: USB interface emulates storage and leaks logs or credentials
- **Attack Steps**: Step 1: Plug device into computer via USB. Step 2: If detected as USB mass storage, browse files. Step 3: Look for log.txt, config.ini, or secrets.txt. Step 4: Copy data for analysis. Step 5: Attempt re-upload of modified file to alter behavior.
- **Detection**: USB activity log or checksum
- **Solution**: Store sensitive info outside USB mount
- **Tags**: USB Storage Leak, Config Dump

## Reprogramming via SD Boot

- **Attack Type**: Hardware Interface Exploitation
- **Target**: SBC / IoT Device
- **Vulnerability**: No secure boot on external media
- **MITRE**: T1542.001
- **Impact**: Firmware override without soldering
- **Tools**: SD card, PC, prebuilt firmware image
- **Scenario**: Device boots from SD card and executes attacker’s firmware
- **Attack Steps**: Step 1: Download or create firmware that grants shell or bypass. Step 2: Format SD card with bootloader-recognized format. Step 3: Copy firmware image and insert into device. Step 4: Power on device — it boots from SD instead of flash. Step 5: Access debug shell or control interface.
- **Detection**: Secure boot logs or flags
- **Solution**: Restrict boot source in hardware
- **Tags**: SD Card Boot Override

## EEPROM Corruption via I2C Write

- **Attack Type**: Hardware Interface Exploitation
- **Target**: EEPROM-using Device
- **Vulnerability**: No write-protection or CRC
- **MITRE**: T1600
- **Impact**: Crash/reset leading to exploit path
- **Tools**: Raspberry Pi / Arduino, i2cset
- **Scenario**: Injecting invalid or null values into EEPROM to crash or reset device
- **Attack Steps**: Step 1: Connect to I2C EEPROM chip (SDA/SCL) on board. Step 2: Use i2cdetect to find address. Step 3: Send invalid or zero values to config memory: i2cset -y 1 0x50 0x00 0x00. Step 4: Device may crash or reset to defaults. Step 5: Exploit reset state for easier access.
- **Detection**: Memory integrity check
- **Solution**: Use write-protected EEPROM or checksum
- **Tags**: I2C Corruption, EEPROM

## Logic Analyzer on I2C Touchpad

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Touch-based IoT Device
- **Vulnerability**: Unencrypted I2C communication
- **MITRE**: T1040, T1005
- **Impact**: Privacy leakage (e.g., keystroke logging)
- **Tools**: Logic Analyzer (Saleae), PulseView
- **Scenario**: Capturing touchpad data through I2C to track gestures or keystrokes
- **Attack Steps**: Step 1: Identify SDA/SCL lines from touchpad IC to MCU. Step 2: Attach logic analyzer probes to lines. Step 3: Start capture during use and decode I2C signals. Step 4: Observe coordinate data or gesture patterns. Step 5: Correlate with physical movements.
- **Detection**: Electrical monitoring
- **Solution**: Encrypt or obfuscate sensor data
- **Tags**: Touchpad, Keystroke Leak, I2C

## EMMC Chip-Off Data Extraction

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smartphones, DVRs
- **Vulnerability**: No storage encryption
- **MITRE**: T1005, T1600
- **Impact**: Total data exfiltration
- **Tools**: Hot air gun, eMMC reader, tweezers
- **Scenario**: Removing eMMC chip and reading full device memory for offline analysis
- **Attack Steps**: Step 1: Open device and locate eMMC chip. Step 2: Use hot air gun to desolder chip carefully. Step 3: Clean and place in socket adapter. Step 4: Use eMMC reader tool to dump raw data. Step 5: Analyze partitions for credentials, images, config.
- **Detection**: Tamper-evident seals, glue
- **Solution**: Use full disk encryption
- **Tags**: eMMC, Chip-off, Data Dump

## Custom Payload via HID Emulator

- **Attack Type**: Hardware Interface Exploitation
- **Target**: PC / Thin Client
- **Vulnerability**: Accepts arbitrary HID input
- **MITRE**: T1059.001
- **Impact**: Remote code execution
- **Tools**: Digispark USB board, Arduino IDE
- **Scenario**: Using microcontrollers like Digispark/Teensy to inject commands as fake keyboard
- **Attack Steps**: Step 1: Write Arduino sketch to send keystrokes (e.g., open terminal, run malware). Step 2: Upload sketch and connect Digispark to target PC. Step 3: It runs pre-programmed keystrokes silently. Step 4: Payload runs with user or admin rights if session is open.
- **Detection**: USB device whitelist
- **Solution**: Disable untrusted USB HID
- **Tags**: Digispark, Teensy, HID Attack

## NAND Flash Dump via TSOP Clip

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Set-top Box / Router
- **Vulnerability**: Unprotected NAND content
- **MITRE**: T1005, T1600
- **Impact**: Raw memory and logs access
- **Tools**: TSOP-48 clip, NAND reader (e.g., GQ-4X), Software
- **Scenario**: Dumping NAND flash using TSOP-48 clip for offline analysis
- **Attack Steps**: Step 1: Identify NAND flash (e.g., K9F1G08U0D) on PCB. Step 2: Attach TSOP clip without desoldering. Step 3: Connect to reader and read memory. Step 4: Use NAND analysis tools to reconstruct file system. Step 5: Extract logs, images, code.
- **Detection**: Glue chip or case tamper detection
- **Solution**: Encrypt NAND or obfuscate data
- **Tags**: NAND Dump, TSOP Clip

## Firmware Dump via SWIM Interface

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded MCU (STM8)
- **Vulnerability**: Debug port not locked
- **MITRE**: T1600
- **Impact**: Extract firmware and behavior
- **Tools**: ST-Link V2, STVP software
- **Scenario**: Using STMicroelectronics’ SWIM interface to access code in ST chips
- **Attack Steps**: Step 1: Identify SWIM pin on ST MCU (e.g., STM8S). Step 2: Connect ST-Link V2 to SWIM, GND, VCC. Step 3: Use STVP to detect chip and read flash. Step 4: Save and analyze firmware dump.
- **Detection**: Firmware hash verification
- **Solution**: Lock debug port post-production
- **Tags**: SWIM, STVP, Firmware Dump

## Boot Delay Exploitation via UART

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Linux Device
- **Vulnerability**: No bootloader protection
- **MITRE**: T1542.001
- **Impact**: Shell access without login
- **Tools**: UART adapter, PuTTY
- **Scenario**: Exploit long boot delays to send commands before OS loads
- **Attack Steps**: Step 1: Connect UART pins and start terminal. Step 2: Power on device and observe boot log. Step 3: During delay, press enter or escape to access bootloader. Step 4: Input boot commands or environment changes (e.g., init=/bin/sh). Step 5: Device drops into root shell after reboot.
- **Detection**: Boot console detection
- **Solution**: Password-protect or disable boot console
- **Tags**: UART, Boot Delay Hack

## SPI Replay Attack with Logic Analyzer

- **Attack Type**: Hardware Interface Exploitation
- **Target**: SPI-Controlled Hardware
- **Vulnerability**: SPI commands unauthenticated
- **MITRE**: T1600, T1056
- **Impact**: Replay command injection
- **Tools**: Logic analyzer, SPI injection tool
- **Scenario**: Record SPI commands to replay them and trigger same behavior
- **Attack Steps**: Step 1: Connect logic analyzer and record known command (e.g., unlocking SPI EEPROM). Step 2: Save waveform or command bytes. Step 3: Use Arduino or Pi to replay those SPI bytes. Step 4: Device responds as if command was issued by main MCU.
- **Detection**: Timing or CRC mismatch alerts
- **Solution**: Add challenge-response in protocol
- **Tags**: SPI Replay, Logic Injection

## Exploiting Open CAN Bus

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Automotive / Industrial PLC
- **Vulnerability**: No authentication in CAN traffic
- **MITRE**: T1600, T1210
- **Impact**: Control/Disrupt device operations
- **Tools**: USB2CAN adapter, cansniffer, can-utils
- **Scenario**: Sending custom packets on open Controller Area Network (CAN) bus to manipulate behavior
- **Attack Steps**: Step 1: Connect USB2CAN to diagnostic CAN port. Step 2: Use candump to listen to traffic. Step 3: Replay command using cansend (e.g., cansend can0 123#112233...). Step 4: Target may unlock door, reboot, or show error.
- **Detection**: CAN anomaly detection
- **Solution**: Message filtering and auth on CAN
- **Tags**: CAN Bus Exploit, Replay

## Physical Memory Dump via Cold Boot

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Laptop / PC
- **Vulnerability**: DRAM remanence post-power
- **MITRE**: T1003.001
- **Impact**: Password or key recovery
- **Tools**: Cold spray, USB boot drive, RAM dumper
- **Scenario**: RAM retains charge after power-off for a few seconds; attacker captures data
- **Attack Steps**: Step 1: Power off system forcefully. Step 2: Spray RAM chip with cold spray to retain charge. Step 3: Boot into forensic OS from USB. Step 4: Dump memory using tools like LiME or memdump. Step 5: Analyze RAM for passwords, keys.
- **Detection**: BIOS memory wipe on boot
- **Solution**: Encrypt keys in TPM
- **Tags**: Cold Boot, RAM Dump

## HDMI Capture Device to Record Output

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Kiosks / CCTV / ATMs
- **Vulnerability**: HDMI not encrypted
- **MITRE**: T1110.003
- **Impact**: Visual data theft
- **Tools**: HDMI splitter, capture card (Elgato, UVC), OBS Studio
- **Scenario**: HDMI output is recorded using capture card to steal sensitive content
- **Attack Steps**: Step 1: Plug HDMI splitter between device and display. Step 2: Connect one output to capture card, then to PC. Step 3: Record HDMI stream using OBS Studio. Step 4: Extract screenshots, documents, videos.
- **Detection**: EDID or signal monitoring
- **Solution**: Use HDCP encryption
- **Tags**: HDMI Capture, Video Leak

## Exploiting JTAG with OpenOCD

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Any JTAG-enabled device
- **Vulnerability**: Unprotected JTAG
- **MITRE**: T1600, T1003
- **Impact**: Full memory access
- **Tools**: JTAG cable, OpenOCD, Raspberry Pi
- **Scenario**: Attacker accesses JTAG port on PCB and halts CPU to dump memory or bypass auth
- **Attack Steps**: Step 1: Locate JTAG pinout using multimeter or datasheet. Step 2: Connect JTAG cable to target and Pi. Step 3: Launch OpenOCD and connect to device. Step 4: Use commands like mdw, dump_image to read memory. Step 5: Dump firmware or bypass password by modifying memory.
- **Detection**: JTAG activity detection or locks
- **Solution**: Disable JTAG after manufacturing
- **Tags**: JTAG, OpenOCD, Debug Memory

## MicroSD AutoRun Payload

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Laptops, DVRs
- **Vulnerability**: AutoRun enabled for media
- **MITRE**: T1204.002, T1059.005
- **Impact**: Remote code execution
- **Tools**: MicroSD card, Autorun.inf, malicious .exe
- **Scenario**: MicroSD card configured with payload and AutoRun file for initial execution
- **Attack Steps**: Step 1: Format MicroSD card with FAT32. Step 2: Create autorun.inf to point to malicious executable. Step 3: Insert MicroSD into device with AutoRun enabled. Step 4: Payload automatically executes upon card mount. Step 5: Gathers data or creates backdoor.
- **Detection**: Disable AutoRun, scan new devices
- **Solution**: Block AutoRun via registry/GPO
- **Tags**: MicroSD Payload, AutoRun

## EEPROM Reset via Clip Writer

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Routers / DVR / IoT
- **Vulnerability**: Password in external EEPROM
- **MITRE**: T1003, T1600
- **Impact**: Login bypass/reset
- **Tools**: SOIC clip, CH341A programmer, AsProgrammer
- **Scenario**: Reset device credentials by overwriting EEPROM using clip-on programmer
- **Attack Steps**: Step 1: Connect SOIC clip to EEPROM (e.g., 24C02). Step 2: Use AsProgrammer to read existing config. Step 3: Identify and zero out password bytes. Step 4: Write modified config to EEPROM. Step 5: Reboot device — login credentials reset.
- **Detection**: EEPROM checksum or tamper logs
- **Solution**: Encrypt or store in internal flash
- **Tags**: EEPROM Reset, SOIC Clip

## Side Channel via LED Blink Pattern

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Routers / Servers / Appliances
- **Vulnerability**: LED status leaks timing info
- **MITRE**: T1201
- **Impact**: Indirect info leakage
- **Tools**: High-speed camera, photodiode, oscilloscope
- **Scenario**: Status LEDs leak internal state or process timing which can be measured
- **Attack Steps**: Step 1: Record LED blinking using camera or photodiode. Step 2: Correlate blink pattern with activity (e.g., login attempt). Step 3: Use timing to infer password length, system state. Step 4: Replay exact inputs and measure LED response for brute-force.
- **Detection**: Analyze for optical emissions
- **Solution**: Use diffused LEDs or logic filter
- **Tags**: LED Leak, Side Channel

## Serial Bus Injection Using USB-to-TTL

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Unlocked embedded devices
- **Vulnerability**: Unauthenticated serial console
- **MITRE**: T1059.003, T1600
- **Impact**: Immediate root command execution
- **Tools**: USB-to-TTL converter, PuTTY/minicom
- **Scenario**: Send raw commands directly to serial console to control system
- **Attack Steps**: Step 1: Connect TX/RX/GND to serial header. Step 2: Open serial terminal and observe login prompt. Step 3: Send commands like reboot, rm -rf /etc/shadow. Step 4: If no login required, system immediately processes input.
- **Detection**: Console logging or lock
- **Solution**: Enforce login shell on serial
- **Tags**: Serial Bus Inject, UART

## Reverse Engineering via NOR Flash Dump

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Device
- **Vulnerability**: Unencrypted firmware
- **MITRE**: T1600, T1005
- **Impact**: Source code and secrets leak
- **Tools**: CH341A programmer, Flashrom
- **Scenario**: Dump NOR flash to extract firmware, hardcoded secrets, or file systems
- **Attack Steps**: Step 1: Identify flash chip (e.g., W25Q64) on PCB. Step 2: Connect clip or solder wires to pins. Step 3: Use Flashrom: flashrom -r backup.bin. Step 4: Analyze dump using binwalk to extract data. Step 5: Look for hardcoded credentials or script logic.
- **Detection**: Monitor for firmware access
- **Solution**: Encrypt or obfuscate firmware
- **Tags**: NOR Flash Dump, Binwalk

## Temperature Sensor Override via I2C

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Safety Devices / HVAC
- **Vulnerability**: Sensor trust without validation
- **MITRE**: T1203
- **Impact**: Safety system bypass
- **Tools**: Arduino with I2C, jumper wires
- **Scenario**: Modify temp sensor readings to trick device (e.g., suppress alarm)
- **Attack Steps**: Step 1: Identify temperature sensor on I2C bus. Step 2: Connect Arduino and scan with i2c-scanner. Step 3: Use Wire.write() to override temp register. Step 4: Device now thinks temperature is safe and doesn’t trigger alerts.
- **Detection**: Cross-check sensor input with redundancy
- **Solution**: Secure sensor with CRC / bus auth
- **Tags**: I2C Temp Sensor Spoof

## Exploiting USB Debug Console on Development Boards

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Dev Boards (ESP32, STM32)
- **Vulnerability**: Unlocked debug interface
- **MITRE**: T1600, T1059.003
- **Impact**: Full OS access via USB
- **Tools**: USB cable, terminal
- **Scenario**: Dev board exposes console via USB CDC; attacker uses it to gain shell
- **Attack Steps**: Step 1: Plug dev board into PC. Step 2: Open serial port using PuTTY/minicom. Step 3: If auto-login or root shell is enabled, explore file system or add users. Step 4: Upload malware or reset configuration.
- **Detection**: Require serial auth or fuse settings
- **Solution**: Lock console before deployment
- **Tags**: USB Debug Shell, Dev Board

## Keyboard Controller Reflash Attack

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Laptops / POS
- **Vulnerability**: Reflashable keyboard firmware
- **MITRE**: T1056.001
- **Impact**: Keylogging without OS detection
- **Tools**: SPI flasher, dump tool, firmware editor
- **Scenario**: Reflashing embedded keyboard controller to intercept keystrokes
- **Attack Steps**: Step 1: Locate keyboard MCU and connect to SPI pins. Step 2: Dump firmware using flasher. Step 3: Modify to add logging function. Step 4: Flash back modified firmware. Step 5: Logged keystrokes saved to memory or sent over channel.
- **Detection**: Firmware hash check
- **Solution**: Lock keyboard MCU firmware
- **Tags**: Keyboard Hack, Firmware Reflash

## Side Channel via Power Consumption (Simple Power Analysis)

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smartcards / Crypto MCUs
- **Vulnerability**: Power draw correlates to operations
- **MITRE**: T1592.001
- **Impact**: PIN/key recovery via analog signal
- **Tools**: Oscilloscope, resistor probe, software
- **Scenario**: Analyzing power draw during operations to infer processed data
- **Attack Steps**: Step 1: Place small resistor on VCC line to measure voltage drop. Step 2: Connect oscilloscope to measure current spikes. Step 3: Trigger device operations (e.g., PIN entry). Step 4: Analyze patterns to determine PIN length or logic branches. Step 5: Replay brute-force based on timing profile.
- **Detection**: Voltage monitoring anomaly
- **Solution**: Use constant-power logic design
- **Tags**: SPA, Power Side Channel

## Exploiting UART Debug Port to Access Root Shell

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Device
- **Vulnerability**: Exposed UART Port
- **MITRE**: T1040 – Peripheral Device Discovery
- **Impact**: Full device control, credential theft
- **Tools**: UART-to-USB Adapter, Terminal Software (PuTTY, Tera Term)
- **Scenario**: Attacker gains physical access to an IoT device like a smart camera and uses exposed UART debug pins to access a root shell, bypassing authentication.
- **Attack Steps**: Step 1: Open the device casing using a screwdriver.Step 2: Locate the UART pins on the PCB (usually labeled TX, RX, GND).Step 3: Connect UART-to-USB adapter to the pins using jumper wires (TX to RX, RX to TX, GND to GND).Step 4: Plug the adapter into your laptop and open a terminal software.Step 5: Try various baud rates (start with 115200) and reboot the device to observe boot logs.Step 6: Wait for the login prompt or shell access (some devices auto-login).Step 7: If access is granted, explore the filesystem, extract credentials, or modify firmware.
- **Detection**: Physical inspection, bootlog monitoring
- **Solution**: Disable UART in production, epoxy over debug ports
- **Tags**: UART, IoT, Root Access, Shell

## JTAG Access for Firmware Dump

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Routers, PLCs
- **Vulnerability**: Unprotected JTAG Interface
- **MITRE**: T1602 – Data from Local System
- **Impact**: Unauthorized access, reverse engineering
- **Tools**: JTAGulator, OpenOCD, Bus Blaster
- **Scenario**: Attacker uses JTAG interface on a router or PLC to dump firmware and reverse engineer it to find backdoors or credentials.
- **Attack Steps**: Step 1: Open the hardware casing to expose the main PCB.Step 2: Identify JTAG pinout using JTAGulator or datasheets.Step 3: Connect JTAG device (e.g., Bus Blaster) to the pins.Step 4: Use OpenOCD or similar tools to detect the chip and connect to it.Step 5: Dump the entire firmware memory to a file.Step 6: Analyze the dumped firmware using Binwalk or strings command to look for passwords, scripts, or backdoors.Step 7: Use findings to gain unauthorized remote or local access.
- **Detection**: Firmware checksum changes, debug lockout
- **Solution**: Disable JTAG in production or fuse it
- **Tags**: JTAG, Reverse Engineering, Firmware

## SPI Flash Dumping to Extract Secrets

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Systems
- **Vulnerability**: Unencrypted Flash Memory
- **MITRE**: T1005 – Data from Removable Media
- **Impact**: Secret exposure, lateral movement
- **Tools**: SOIC8 Clip, CH341A Programmer, Flashrom
- **Scenario**: Attacker accesses an SPI flash chip on a PCB to read the memory contents and extract sensitive data like firmware or passwords.
- **Attack Steps**: Step 1: Power off the device and locate the SPI flash chip (often labeled 25Qxx or similar).Step 2: Attach SOIC8 clip carefully to the chip without damaging it.Step 3: Connect the clip to CH341A programmer and plug into your computer.Step 4: Use Flashrom to detect the chip and read the contents into a file.Step 5: Analyze the binary file using tools like Binwalk to extract firmware, file systems, or secrets.Step 6: Look for hardcoded keys, passwords, or SSH credentials.Step 7: Use credentials to attack other devices or escalate access.
- **Detection**: Chip tamper detection, integrity checks
- **Solution**: Encrypt sensitive sections, epoxy chips
- **Tags**: SPI Flash, Firmware, Secret Dump

## I2C Bus Snooping for Data Interception

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart Locks, Sensors
- **Vulnerability**: Unencrypted I2C Traffic
- **MITRE**: T0842 – Capture Sensor Data
- **Impact**: Leakage of sensor data, replay attacks
- **Tools**: Logic Analyzer (Saleae), Jumper Wires, PulseView
- **Scenario**: By tapping into the I2C bus, an attacker can listen to communication between sensors and microcontrollers to capture sensitive data.
- **Attack Steps**: Step 1: Open the device enclosure and locate I2C lines (SCL and SDA).Step 2: Connect the logic analyzer probes to SCL, SDA, and GND lines.Step 3: Use software like PulseView to capture the data.Step 4: Observe data packets and decode them in real-time.Step 5: Interpret values like sensor readings, access logs, or commands.Step 6: Identify sensitive information that may be misused (e.g., door unlock signals).Step 7: Replay or modify traffic if active attack is possible.
- **Detection**: EM monitoring, data anomaly detection
- **Solution**: Encrypt bus traffic or obfuscate it
- **Tags**: I2C, Sensor Exploitation, Logic Analyzer

## Exploiting Debug Interfaces Over USB (DWC2 Gadget Mode)

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Single-board Computers
- **Vulnerability**: Exposed USB Debug Mode
- **MITRE**: T1055 – Process Injection
- **Impact**: Remote control, malware installation
- **Tools**: USB Cable, Kali Linux, USB Gadget Scripts
- **Scenario**: When USB debug interfaces are left enabled on a device like Raspberry Pi Zero, attackers can use them to gain shell access or upload malware.
- **Attack Steps**: Step 1: Connect a USB cable from the device (e.g., Raspberry Pi Zero) to a laptop.Step 2: If the device supports USB gadget mode, it may appear as an Ethernet or Serial device.Step 3: Use dmesg or ifconfig to detect the interface.Step 4: Use tools like screen or minicom to open a serial connection.Step 5: If terminal access appears, try common usernames/passwords or wait for auto-login.Step 6: Once inside, check system info, upload malware, or change configs.Step 7: The attacker can now maintain persistent access via USB or network.
- **Detection**: USB monitoring, disable gadget mode
- **Solution**: Disable USB gadget drivers, set OTP lock
- **Tags**: USB, Raspberry Pi, Debug Mode

## EEPROM Dumping for Password Recovery

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Industrial Devices
- **Vulnerability**: Unprotected EEPROM
- **MITRE**: T1552 – Unsecured Credentials
- **Impact**: Credential theft
- **Tools**: EEPROM Reader (e.g., TL866II), SOIC Clip
- **Scenario**: Attacker removes or taps into EEPROM chip to recover stored passwords and system configurations.
- **Attack Steps**: Step 1: Power off the device and find the EEPROM chip labeled 24Cxx.Step 2: Attach SOIC8 clip to the chip carefully.Step 3: Connect the clip to EEPROM programmer.Step 4: Use provided software to read the chip memory.Step 5: Save the dump and open it in a hex editor.Step 6: Look for readable strings, like usernames, passwords, IP addresses.Step 7: Use recovered credentials to access the system or escalate access.
- **Detection**: Physical inspection, config anomaly
- **Solution**: Encrypt or externalize credentials
- **Tags**: EEPROM, Credential Dump, Hex Editor

## SPI Flash Reprogramming for Malware Injection

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Devices
- **Vulnerability**: Writable SPI Flash
- **MITRE**: T1546 – Boot or Logon Autostart
- **Impact**: Persistent malware access
- **Tools**: CH341A, Flashrom, Modified Firmware Image
- **Scenario**: An attacker reprograms the firmware via SPI to include a persistent backdoor or malware.
- **Attack Steps**: Step 1: Extract the original firmware using flash dump (as done in HWINT-003).Step 2: Modify the firmware image (e.g., add reverse shell or bypass auth script).Step 3: Use Flashrom to reflash the modified firmware back to the chip.Step 4: Boot the device and verify malware runs on startup.Step 5: Connect to the device remotely or via USB to control it.Step 6: Use persistence tricks like cron jobs or startup scripts.Step 7: Monitor device for confirmation of backdoor access.
- **Detection**: Boot hash comparison, code analysis
- **Solution**: Secure boot, firmware signing
- **Tags**: SPI, Malware, Firmware Mod

## SD Card Firmware Replacement in Cameras

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Surveillance Cameras
- **Vulnerability**: Removable Storage Attack
- **MITRE**: T1036 – Masquerading
- **Impact**: Spyware injection, config hijack
- **Tools**: SD Card Reader, Hex Editor, Custom Firmware
- **Scenario**: Modify firmware on removable SD card of a security camera to inject custom logging or malware.
- **Attack Steps**: Step 1: Remove the SD card from the camera.Step 2: Insert it into a laptop using a card reader.Step 3: Locate firmware or config files (common in /config, /firmware).Step 4: Replace it with modified firmware or script (e.g., remote uploader).Step 5: Reinsert SD card and reboot the camera.Step 6: Observe behavior, confirm malware or access logs are now exfiltrated.Step 7: Maintain access through modified configs/scripts.
- **Detection**: File integrity check, SD lockout
- **Solution**: Write-protect SD, secure boot
- **Tags**: SD Card, Camera Hack, Config Bypass

## Using GPIO Pins for Covert Exfiltration

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Boards
- **Vulnerability**: Misused GPIO Function
- **MITRE**: T1020 – Automated Exfiltration
- **Impact**: Covert data theft
- **Tools**: Raspberry Pi GPIO, Logic Analyzer
- **Scenario**: By abusing General Purpose I/O pins, an attacker can create side-channel data leaks or covert signals.
- **Attack Steps**: Step 1: Gain physical access to the embedded device.Step 2: Attach logic analyzer to GPIO pins.Step 3: Reboot device and record any data pulses.Step 4: Analyze captured patterns to extract binary data.Step 5: If attacker can modify the firmware, create custom GPIO toggling routines to send data (e.g., Morse code style).Step 6: Listen externally with RF receiver or wired probe.Step 7: Use this channel to exfiltrate secret keys or logs silently.
- **Detection**: GPIO logic monitoring
- **Solution**: Disable unused GPIOs, glue mask
- **Tags**: GPIO, Side Channel, Data Leak

## Exploiting I2C EEPROM Emulators

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Medical Devices, POS Systems
- **Vulnerability**: Trusted EEPROM Assumption
- **MITRE**: T0830 – Configuration Injection
- **Impact**: Config tampering, license abuse
- **Tools**: Arduino/ESP32 with EEPROM emulator sketch
- **Scenario**: Use a malicious I2C EEPROM emulator to respond to read/write commands and inject altered config data.
- **Attack Steps**: Step 1: Locate the I2C EEPROM connected to the microcontroller.Step 2: Disconnect original EEPROM (or solder intercept lines).Step 3: Connect Arduino running EEPROM emulation firmware.Step 4: Respond to read/write requests with tampered data (e.g., bypass license check, enable debug mode).Step 5: Boot the system and verify it accepts injected config.Step 6: Maintain control by modifying data at runtime.Step 7: Reverse engineer protocol for further abuse.
- **Detection**: Bus protocol logging, device mismatch
- **Solution**: Harden I2C interface, secure boot
- **Tags**: I2C, EEPROM, Emulator Hack

## USB-Based Cold Boot Key Extraction

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Laptops, Desktops
- **Vulnerability**: Residual Memory in DRAM
- **MITRE**: T1003.001 – LSASS Memory
- **Impact**: Disk decryption, credential theft
- **Tools**: USB Dumper Tool, Cold Boot Toolkit
- **Scenario**: Using USB tool after brief power interruption to extract encryption keys from RAM.
- **Attack Steps**: Step 1: Power off target system without removing power source entirely.Step 2: Quickly boot from custom USB stick.Step 3: Dump memory using RAM forensic tools.Step 4: Search for encryption keys, credentials in the dump.Step 5: Use keys to decrypt disk or intercept data.Step 6: If successful, clone disk for offline analysis.Step 7: Wipe traces from USB.
- **Detection**: BIOS lockdown, boot order lock
- **Solution**: Cold boot mitigation, full shutdown
- **Tags**: USB, Cold Boot, Memory Dump

## Exploiting Test Points for Firmware Injection

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Industrial Controllers
- **Vulnerability**: Exposed Test Pads
- **MITRE**: T1542.001 – Bootkits
- **Impact**: Persistent access, device hijack
- **Tools**: Multimeter, Soldering Kit, Programmer
- **Scenario**: Test points are used in manufacturing but can be hijacked to inject firmware or commands.
- **Attack Steps**: Step 1: Open the device and locate unlabeled test pads.Step 2: Use multimeter continuity check to map pads to microcontroller pins.Step 3: Solder jumper wires to pads (e.g., Reset, SWDIO, SWCLK).Step 4: Connect programmer and identify chip.Step 5: Use programmer tool to flash backdoored firmware.Step 6: Reassemble device and test for hidden access.Step 7: Use backdoor for command injection or telemetry capture.
- **Detection**: PCB inspection, tamper paint
- **Solution**: Remove or obfuscate test pads
- **Tags**: SWD, Test Pads, Firmware Hack

## HID Spoofing via USB Rubber Ducky

- **Attack Type**: Hardware Interface Exploitation
- **Target**: PCs, Servers
- **Vulnerability**: Unlocked USB Ports
- **MITRE**: T1204.002 – Malicious File Execution
- **Impact**: Quick access, malware drop
- **Tools**: USB Rubber Ducky, Ducky Script
- **Scenario**: A USB device emulating a keyboard types payload commands when plugged in, automating exploitation.
- **Attack Steps**: Step 1: Program USB Rubber Ducky with payload (e.g., open terminal and create user).Step 2: Plug device into target computer.Step 3: It acts like a keyboard and types commands instantly.Step 4: The payload may download malware, open a backdoor, or steal data.Step 5: Payload finishes in seconds and device is removed.Step 6: Attacker now has access via created user or reverse shell.Step 7: Cleanup or repeat on other machines.
- **Detection**: USB restrictions, input device lock
- **Solution**: Disable USB HID or whitelist
- **Tags**: Rubber Ducky, HID, Automation

## Remote Reflash via SPI Bus Hijack

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart Appliances
- **Vulnerability**: Insecure SPI Access
- **MITRE**: T1542 – Pre-OS Boot
- **Impact**: Firmware-level persistence
- **Tools**: FlashcatUSB, SPI Probe, SPI Hook Board
- **Scenario**: An attacker taps into the SPI bus and reflashes firmware while the device is powered, injecting malicious code.
- **Attack Steps**: Step 1: Identify the SPI lines (CS, CLK, MISO, MOSI, GND, VCC).Step 2: Use hook wires or SPI breakout board to tap into those lines.Step 3: Use FlashcatUSB or similar to initiate SPI communication.Step 4: Dump existing firmware and analyze it.Step 5: Inject malicious shell or remote control code.Step 6: Reflash modified firmware into chip.Step 7: Restart the device and check persistence.
- **Detection**: Boot validation checks
- **Solution**: SPI bus lockdown, firmware signing
- **Tags**: SPI, Firmware, Live Flashing

## Physical Keylogger Implant via USB

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Desktop Workstations
- **Vulnerability**: Physical USB Tampering
- **MITRE**: T1056.001 – Input Capture
- **Impact**: Credential Theft
- **Tools**: USB Keylogger Dongle
- **Scenario**: A malicious USB device placed between keyboard and PC logs keystrokes and stores or sends them.
- **Attack Steps**: Step 1: Unplug the keyboard and plug the keylogger dongle between PC and keyboard.Step 2: The user continues to use the computer normally.Step 3: All keystrokes (including passwords) are logged inside the device.Step 4: After a while, attacker retrieves the device.Step 5: Plug into their own laptop and open saved text log.Step 6: Read captured credentials.Step 7: Use data to access victim accounts.
- **Detection**: Unusual USB devices, physical inspection
- **Solution**: Use USB cable locks, encrypt keyboard data
- **Tags**: Keylogger, USB, Credential Theft

## Exploiting SWD Interface for Debug Access

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Industrial Controllers
- **Vulnerability**: Unlocked SWD Interface
- **MITRE**: T1557 – Adversary-in-the-Middle
- **Impact**: Live memory extraction
- **Tools**: ST-Link, OpenOCD, Jumper Wires
- **Scenario**: By accessing SWD (Serial Wire Debug) lines, an attacker can read memory or halt CPU to inject payloads.
- **Attack Steps**: Step 1: Locate SWDIO and SWCLK pads on PCB (2-pin debug interface).Step 2: Connect ST-Link programmer to those pins.Step 3: Use OpenOCD to detect the chip and dump memory.Step 4: Pause CPU execution if needed.Step 5: Read RAM/Flash for credentials or firmware.Step 6: Modify memory (e.g., change flags, bootloader options).Step 7: Resume execution with attacker-controlled state.
- **Detection**: PCB-level inspection
- **Solution**: Disable SWD or protect with fuses
- **Tags**: SWD, Debug Access, ARM

## EEPROM Swapping for Device ID Spoofing

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Medical Equipment, POS Terminals
- **Vulnerability**: Identity tied to EEPROM
- **MITRE**: T1036.005 – Masquerading
- **Impact**: License abuse, device spoofing
- **Tools**: EEPROM Programmer, SOIC Clip
- **Scenario**: Swapping EEPROM chips to impersonate another device (with license or higher privileges).
- **Attack Steps**: Step 1: Identify the EEPROM chip containing device serial info.Step 2: Use programmer to clone EEPROM from another device.Step 3: Write that clone into a blank chip.Step 4: Replace original chip with modified one (soldering).Step 5: Boot device – now it is impersonating the other.Step 6: Bypass license checks or access restrictions.Step 7: Use device for privileged operations.
- **Detection**: EEPROM comparison, license mismatch
- **Solution**: Digital signatures, tamper seal
- **Tags**: EEPROM, Clone, ID Spoofing

## JTAG Shell via Boundary Scan Abuse

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded SOC Boards
- **Vulnerability**: Open Boundary Scan Chain
- **MITRE**: T1211 – Exploitation for Defense Evasion
- **Impact**: Extract secrets, memory abuse
- **Tools**: JTAGulator, BScan Tools
- **Scenario**: Using boundary scan commands, attackers interact with device registers and memory without full JTAG access.
- **Attack Steps**: Step 1: Identify JTAG port pins and connect JTAGulator.Step 2: Use boundary scan software to detect accessible functions.Step 3: Read/write I/O register states.Step 4: Dump RAM in small chunks through scan chains.Step 5: Extract strings, environment variables, or kernel params.Step 6: Use info to escalate or build targeted firmware.Step 7: Maintain persistence through partial memory patches.
- **Detection**: Debug line trace, boot log alerts
- **Solution**: Disable boundary scan post-production
- **Tags**: Boundary Scan, JTAG Lite

## Exploiting Unused M.2 Debug Pins

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Laptops, Thin Clients
- **Vulnerability**: Exposed debug lines in M.2
- **MITRE**: T1010 – Application Window Discovery
- **Impact**: Boot bypass, hidden interface abuse
- **Tools**: Logic Analyzer, Multimeter, SPI Tool
- **Scenario**: M.2 SSD slots often expose debug/test lines that can be hijacked for low-level attacks.
- **Attack Steps**: Step 1: Remove cover from device with M.2 SSD.Step 2: Inspect connector pins for undocumented lines.Step 3: Use multimeter to trace unused pins to SPI or UART.Step 4: Connect logic analyzer or SPI debugger.Step 5: Listen to communication or inject boot-level commands.Step 6: Extract secrets or force debug boot mode.Step 7: Use data to pivot deeper into system.
- **Detection**: Signal monitoring, pin disablement
- **Solution**: Physically block unused pins
- **Tags**: M.2, Debug Line, SSD

## HDMI CEC Command Injection

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart TVs
- **Vulnerability**: Over-permissive CEC Control
- **MITRE**: T1548.002 – Abuse Elevation Control
- **Impact**: Remote manipulation
- **Tools**: Raspberry Pi, CEC-Client Tool
- **Scenario**: HDMI CEC allows devices to control each other; malicious CEC commands can be used to manipulate TVs, media boxes.
- **Attack Steps**: Step 1: Connect Raspberry Pi to TV using HDMI.Step 2: Use cec-client to send crafted CEC commands.Step 3: Commands like volume, source change, shutdown can be abused.Step 4: Send loop commands to disable remote usage.Step 5: Exploit auto-play features to launch content.Step 6: If TV runs smart OS, trigger app launch remotely.Step 7: Maintain control via boot-on-CEC.
- **Detection**: HDMI logs, CEC request alerts
- **Solution**: Disable CEC, whitelist devices
- **Tags**: HDMI, CEC, Remote Injection

## Unsecured Debugging Pads on Wearables

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smartwatches, Fitness Bands
- **Vulnerability**: Open Debug Pads
- **MITRE**: T0851 – Sensor Manipulation
- **Impact**: Data privacy leak
- **Tools**: SWD/JTAG Debugger, Logic Probe
- **Scenario**: Smartwatches or wearables often expose debug pads that provide unrestricted memory access.
- **Attack Steps**: Step 1: Open wearable casing carefully.Step 2: Locate unpopulated test pads (tiny golden circles).Step 3: Solder wires or use fine clips to connect debugger.Step 4: Identify protocol (SWD, UART, I2C).Step 5: Use tools like ST-Link, Bus Pirate, or Saleae.Step 6: Dump memory and search for personal data or GPS history.Step 7: Export logs for analysis or exfiltrate via USB.
- **Detection**: Hardware audit, RF shielding
- **Solution**: Epoxy coating, secure boot
- **Tags**: Wearable, Debug, GPS Data

## RFID Debug Line Hijacking for Tag Cloning

- **Attack Type**: Hardware Interface Exploitation
- **Target**: RFID Readers
- **Vulnerability**: No tamper protection on debug lines
- **MITRE**: T1078 – Valid Accounts
- **Impact**: Physical access bypass
- **Tools**: Proxmark3, Logic Analyzer
- **Scenario**: Attacker connects to debug/test lines on RFID reader to capture or inject tag data directly.
- **Attack Steps**: Step 1: Open casing of RFID reader.Step 2: Identify and connect to internal debug pins.Step 3: Use Proxmark3 to emulate or record legitimate tag communication.Step 4: Clone tag data or modify it slightly to spoof another identity.Step 5: Reprogram blank tag with modified UID/data.Step 6: Test cloned tag on original reader.Step 7: Repeat for other RFID systems.
- **Detection**: Physical seal, debug pad lockout
- **Solution**: Secure debug channel, alert logs
- **Tags**: RFID, Clone, Spoofing

## HDMI EDID Spoofing for Screen Hijack

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Laptops, Kiosks
- **Vulnerability**: Trusting EDID from any display
- **MITRE**: T1056 – Input Capture
- **Impact**: Screen mirroring, data leakage
- **Tools**: EDID Emulator, HDMI Capture Dongle
- **Scenario**: Attacker emulates a display device and manipulates EDID data to hijack video feed or trick system behavior.
- **Attack Steps**: Step 1: Plug EDID emulator into the HDMI port of the computer.Step 2: Modify EDID file to declare a fake display with different resolution or properties.Step 3: System reads false EDID and reconfigures screen output.Step 4: Connect HDMI capture tool to record or view video feed.Step 5: Potentially inject overlays or false display.Step 6: Use captured data for surveillance or social engineering.Step 7: Remove emulator to avoid detection.
- **Detection**: Unusual resolution change
- **Solution**: Validate display with whitelists
- **Tags**: EDID, HDMI, Display Hack

## PCIe Debug Port Hijack on Motherboard

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Desktop Motherboards
- **Vulnerability**: Unused PCIe debug port
- **MITRE**: T1600 – Data Leakage
- **Impact**: Hardware manipulation
- **Tools**: PCIe Analyzer, PCIe Interposer Board
- **Scenario**: Exposed PCIe test points on a motherboard are hijacked to monitor or manipulate device activity.
- **Attack Steps**: Step 1: Open the target system casing.Step 2: Locate PCIe debug headers or test points on motherboard.Step 3: Connect PCIe analyzer to the header.Step 4: Passively capture PCIe traffic.Step 5: Analyze for disk I/O, memory requests, device configs.Step 6: Inject spoofed configuration frames.Step 7: Hijack or disable connected hardware like NICs or GPUs.
- **Detection**: Monitor bus error logs
- **Solution**: Disable or hide debug headers
- **Tags**: PCIe, Motherboard, Side Channel

## Debug UART on Smart Meters

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart Energy Meters
- **Vulnerability**: Open debug interface
- **MITRE**: T1496 – Resource Hijacking
- **Impact**: Energy theft, usage spoofing
- **Tools**: USB-UART Converter, PuTTY
- **Scenario**: Exposed UART interface on digital meters can be abused to alter usage data or unlock premium features.
- **Attack Steps**: Step 1: Unscrew and open smart meter casing (may void warranty).Step 2: Locate UART pins labeled TX, RX, GND.Step 3: Connect USB UART adapter.Step 4: Open PuTTY terminal and watch boot logs.Step 5: If login prompt appears, attempt common credentials.Step 6: Modify internal counters or disable billing flags.Step 7: Save changes and close the device.
- **Detection**: Meter reading mismatch
- **Solution**: Lock/debug-disable in production
- **Tags**: UART, Smart Meter, Energy Hack

## Tampering via Unprotected Expansion Slot

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Laptops, Industrial Controllers
- **Vulnerability**: Open expansion ports
- **MITRE**: T1200 – Hardware Additions
- **Impact**: Backdoor via peripheral
- **Tools**: Custom PCIe Board, Laptop with Slot
- **Scenario**: Attacker inserts a rogue PCIe or miniPCIe card with malware or debug code.
- **Attack Steps**: Step 1: Power off target machine.Step 2: Open access panel and insert custom PCIe or M.2 card.Step 3: The card runs malicious firmware or connects attacker wirelessly.Step 4: Upon boot, card is detected as legitimate hardware.Step 5: It may keylog, redirect traffic, or open remote shell.Step 6: Attack persists across reboots.Step 7: Card is removed after exfiltration.
- **Detection**: Hardware change logs, asset scan
- **Solution**: BIOS-level slot disable
- **Tags**: PCIe, Rogue Card, Implant

## SATA Bus Sniffing for File Access

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Desktop Systems
- **Vulnerability**: Unencrypted SATA traffic
- **MITRE**: T1006 – Direct Volume Access
- **Impact**: Data leakage or theft
- **Tools**: SATA Logic Analyzer, Tap Board
- **Scenario**: Tapping SATA lines allows attacker to spy on file transfers and read/write operations in real-time.
- **Attack Steps**: Step 1: Open target desktop or server case.Step 2: Disconnect SATA cable and attach it to tap board.Step 3: Connect analyzer to tap output.Step 4: Power on system and monitor traffic.Step 5: Capture data read/writes to/from disk.Step 6: Identify and extract file contents.Step 7: Remove setup without detection.
- **Detection**: SATA anomaly detection
- **Solution**: Use full-disk encryption
- **Tags**: SATA, Sniffing, File Capture

## Device Bricking via Serial Console Command

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Industrial Controllers
- **Vulnerability**: Open bootloader commands
- **MITRE**: T1499 – Endpoint Denial of Service
- **Impact**: Device destruction
- **Tools**: UART Cable, Serial Terminal
- **Scenario**: Some serial interfaces allow low-level firmware erasure or reset commands that brick devices.
- **Attack Steps**: Step 1: Connect to device via UART.Step 2: Reboot and interrupt bootloader menu.Step 3: Enter command like erase all or reset env.Step 4: Confirm execution.Step 5: Device fails to boot on next start.Step 6: Leave hardware looking intact.Step 7: Attack useful for sabotage.
- **Detection**: Boot message logging
- **Solution**: Lock bootloader access
- **Tags**: UART, Bricking, Reset Command

## EM Side Channel via Debug Headers

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Devices, ATMs
- **Vulnerability**: Unshielded debug headers
- **MITRE**: T1592 – Peripheral Discovery
- **Impact**: PIN leakage, surveillance
- **Tools**: EM Probe, Oscilloscope, Debug Port Access
- **Scenario**: By connecting probes to debug headers, attacker reads electromagnetic emissions to infer keypresses or secrets.
- **Attack Steps**: Step 1: Connect EM probe near debug lines (UART, I2C, etc.).Step 2: Record signal with oscilloscope during device operation.Step 3: Identify signal pattern during keypad press or data exchange.Step 4: Train model or observe waveform differences.Step 5: Match signal peaks to characters.Step 6: Derive PIN or password from timing.Step 7: Use extracted data to gain access.
- **Detection**: EMI spectrum detection
- **Solution**: Shielding, encryption
- **Tags**: Side Channel, EM Leak, Oscilloscope

## BIOS Debug Port Over SPI Flash

- **Attack Type**: Hardware Interface Exploitation
- **Target**: PCs, Workstations
- **Vulnerability**: Unlocked BIOS Flash Interface
- **MITRE**: T1542.003 – Bootkit
- **Impact**: Persistent high privilege access
- **Tools**: SPI Programmer, Chip Clip
- **Scenario**: Some motherboards expose BIOS debug mode through SPI flash pads, allowing firmware rewrite.
- **Attack Steps**: Step 1: Identify BIOS chip near motherboard battery (often 8-pin SOIC).Step 2: Clip on SPI programmer with SOIC clip.Step 3: Dump current BIOS image.Step 4: Modify BIOS with backdoor or password bypass.Step 5: Flash modified BIOS back.Step 6: Boot system and confirm elevated access.Step 7: Cleanup and unclip programmer.
- **Detection**: Firmware integrity checker
- **Solution**: Use write-protect BIOS jumper
- **Tags**: BIOS, SPI Flash, Firmware Mod

## Glitching Microcontroller via Voltage Fault Injection

- **Attack Type**: Fault Injection
- **Target**: Microcontroller-based IoT Device
- **Vulnerability**: Voltage tolerance not enforced; lacks brown-out protection
- **MITRE**: T1495 – Firmware Corruption
- **Impact**: Bypass Authentication / Memory Dump
- **Tools**: Adjustable lab power supply, multimeter, oscilloscope
- **Scenario**: An attacker tampers with a microcontroller’s voltage supply to glitch its behavior and bypass security checks.
- **Attack Steps**: Step 1: Power off the target device and identify its main chip (microcontroller).Step 2: Use a datasheet (search online using chip's number) to find Vcc and GND pins.Step 3: Connect a lab power supply to Vcc and GND using jumper wires.Step 4: Slowly reduce voltage from normal (e.g., 3.3V) to just below threshold while observing behavior (e.g., system crashes, skips auth).Step 5: Trigger boot-up and repeatedly apply brief voltage dips until the chip behaves abnormally (e.g., skips login code).Step 6: Log behavior and try to access protected functions during the glitch.
- **Detection**: Boot integrity check, voltage sensors
- **Solution**: Use secure boot, brown-out detectors
- **Tags**: glitching, voltage fault, microcontroller, tamper

## SPI Flash Dump via Clip-on Interface

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Device / Router
- **Vulnerability**: Exposed SPI flash, no encryption
- **MITRE**: T1003 – Credential Dumping
- **Impact**: Extract firmware or passwords
- **Tools**: SOIC8 Test Clip, Flashrom, Bus Pirate/Raspberry Pi
- **Scenario**: Dumping firmware from SPI flash using clip-on probes to bypass encrypted interfaces.
- **Attack Steps**: Step 1: Open device casing and locate SPI Flash chip (typically 8-pin SOIC chip near microcontroller).Step 2: Note chip number and orientation; search datasheet online.Step 3: Attach SOIC8 clip gently to chip with proper pin alignment.Step 4: Connect clip wires to a programmer (Bus Pirate/RPi GPIOs).Step 5: Power target device if flash requires onboard voltage or use 3.3V from programmer.Step 6: Run flashrom and dump chip content using command line.Step 7: Save binary dump and analyze in hex editor or reverse engineer firmware.
- **Detection**: Chip-read detection, case tamper switch
- **Solution**: Encrypt flash, epoxy protection, disable external read
- **Tags**: SPI, firmware dump, flash, reverse

## UART Console Backdoor via Test Points

- **Attack Type**: Interface Tampering
- **Target**: IoT Devices, CCTV, Modems
- **Vulnerability**: Exposed UART with root shell or weak login
- **MITRE**: T1059.004 – Unix Shell
- **Impact**: Root access, firmware tamper
- **Tools**: USB-to-TTL adapter (FTDI), jumper wires
- **Scenario**: Accessing root shell through UART debug interface by soldering wires to test points.
- **Attack Steps**: Step 1: Open target device casing and visually locate test points or headers (labeled TX, RX, GND).Step 2: If not labeled, identify using multimeter and datasheet (usually near microcontroller).Step 3: Solder wires to TX, RX, and GND (or use test hook clips if no soldering).Step 4: Connect to USB-TTL adapter, then to PC.Step 5: Open terminal software (PuTTY/minicom), set baud rate (e.g., 115200), and power on device.Step 6: Observe boot log and press Enter if login prompt appears.Step 7: If root shell appears without login or weak/default credentials work – attacker gains control.
- **Detection**: UART activity logging, login alerts
- **Solution**: Disable debug ports in production
- **Tags**: UART, console, backdoor, TTL

## I2C EEPROM Manipulation via Debug Port

- **Attack Type**: Tampering / Fault Injection
- **Target**: I2C-based Embedded Devices
- **Vulnerability**: No EEPROM write protection or integrity check
- **MITRE**: T1565 – Stored Data Manipulation
- **Impact**: Change config, reset password
- **Tools**: I2C scanner tool (Bus Pirate, Arduino), EEPROM programmer
- **Scenario**: Reading or modifying EEPROM content over I2C interface to change configurations or credentials.
- **Attack Steps**: Step 1: Open device and identify EEPROM chip (often 24Cxx series, 8-pin).Step 2: Note chip label and search for datasheet to find SDA/SCL/GND/VCC pins.Step 3: Connect wires to I2C programmer or microcontroller.Step 4: Use scanning script (Python with smbus or Arduino) to verify EEPROM address.Step 5: Dump EEPROM content and analyze with hex editor.Step 6: Modify specific addresses (e.g., password location, config flags).Step 7: Write modified data back and reboot device to test result.
- **Detection**: Checksum validation, write-locks
- **Solution**: Lock EEPROM writes, use hashed values
- **Tags**: EEPROM, I2C, tamper, config edit

## Fault Injection via Laser on Chip Surface

- **Attack Type**: Advanced Fault Injection
- **Target**: Smartcards, Secure Microcontrollers
- **Vulnerability**: Lack of fault detection on logic level
- **MITRE**: T1495 – Fault Injection
- **Impact**: Bypass auth, extract secrets
- **Tools**: IR Laser Diode, Focus Lens, Microscope Stand
- **Scenario**: Using focused laser beam to induce temporary faults on silicon die, bypassing logic like password check.
- **Attack Steps**: Step 1: Decap chip using acid or heat (or use chips with no epoxy coating).Step 2: Mount chip under microscope with clear view of die.Step 3: Focus laser onto specific part of the chip using manual trial or reference image.Step 4: Power device and run login operation while pulsing laser.Step 5: Observe if glitching allows skipping password checks.Step 6: Repeat at various chip locations to find vulnerable area.Step 7: Once bypass achieved, record exact coordinates and timing.
- **Detection**: Light sensors, side-channel detectors
- **Solution**: Tamper sensors, logic checks, epoxy layer
- **Tags**: laser, chip, glitch, advanced

## JTAG Access for Full Memory Dump

- **Attack Type**: Debug Interface Exploitation
- **Target**: Microcontroller, IoT Devices
- **Vulnerability**: Unprotected JTAG left active in production
- **MITRE**: T1040 – Network Sniffing (side) / T1003 – Dumping
- **Impact**: Full memory extraction
- **Tools**: JTAGulator, OpenOCD, Multimeter
- **Scenario**: Attacker accesses internal memory of device using JTAG debug port and dumps secrets.
- **Attack Steps**: Step 1: Open device casing and locate debug headers or labeled JTAG pins (TCK, TMS, TDI, TDO, GND).Step 2: If unlabeled, use JTAGulator or multimeter to map pins.Step 3: Connect JTAG pins to PC via debugger or USB-JTAG adapter.Step 4: Use OpenOCD to scan and connect to device.Step 5: Issue commands to halt processor, then read flash/RAM.Step 6: Save memory dump and analyze firmware.Step 7: Look for hardcoded credentials or security keys.
- **Detection**: Monitor JTAG lines, tamper-proof resin
- **Solution**: Disable JTAG, set fuses, lock bits
- **Tags**: JTAG, memory dump, debug, OpenOCD

## Fault Injection via Clock Glitch

- **Attack Type**: Fault Injection
- **Target**: Secure microcontrollers, Smartcards
- **Vulnerability**: No clock glitch protection
- **MITRE**: T1495 – Fault Injection
- **Impact**: Authentication bypass
- **Tools**: Signal Generator, Logic Analyzer
- **Scenario**: Inducing faults in chip logic by sending malformed clock signals, skipping logic checks.
- **Attack Steps**: Step 1: Identify the clock input pin (CLK) of the microcontroller using datasheet.Step 2: Disconnect external oscillator and connect signal generator.Step 3: Set base frequency matching original clock (e.g., 16 MHz).Step 4: Inject faulty signal — e.g., short glitches, faster spikes.Step 5: Power on device and observe if timing faults occur (e.g., skipping password check).Step 6: Adjust glitch timing to target specific logic windows.Step 7: Log successful fault behavior and extract benefit.
- **Detection**: Frequency anomaly detection
- **Solution**: Use secure clock, glitch filters
- **Tags**: glitch, clock, bypass, logic

## Firmware Replacement via USB Bootloader

- **Attack Type**: Interface Tampering
- **Target**: Microcontrollers with USB DFU
- **Vulnerability**: Bootloader left open in release version
- **MITRE**: T1601.001 – Modify System Firmware
- **Impact**: Custom firmware upload
- **Tools**: USB cable, Firmware hex/bin file, Flashing tool (e.g., STM32CubeProg)
- **Scenario**: Overwriting firmware by abusing USB bootloader left enabled in production.
- **Attack Steps**: Step 1: Power off target device and connect USB to PC.Step 2: Enter bootloader mode (e.g., hold button while powering on).Step 3: Detect device using official flashing tool (e.g., STM32CubeProg, Atmel Studio).Step 4: Read current firmware and save backup.Step 5: Load custom or modified firmware image.Step 6: Flash new firmware using tool interface.Step 7: Reboot device and verify modified behavior.
- **Detection**: Bootloader lock detection
- **Solution**: Disable bootloader post-debug
- **Tags**: USB DFU, firmware flash

## GPIO Pin Tampering to Trigger Debug Mode

- **Attack Type**: Pin-Level Exploitation
- **Target**: Routers, IoT Gateways
- **Vulnerability**: GPIO not secured; hidden boot modes
- **MITRE**: T1542.001 – Boot Process Injection
- **Impact**: Enter debug state, access shell
- **Tools**: Jumper wires, Multimeter
- **Scenario**: Altering GPIO pin state during boot to trigger hidden debug or recovery mode.
- **Attack Steps**: Step 1: Identify GPIO pins on bootloader config via datasheet (e.g., BOOT0, BOOT1).Step 2: Locate exposed test pads or headers connected to those pins.Step 3: Connect GND and short GPIO pin to logical HIGH/LOW using jumper wire.Step 4: Power on device with pin held in target state.Step 5: Observe behavior – some devices enter debug/diagnostic modes.Step 6: Once in debug mode, use UART/JTAG/USB to access system.Step 7: Remove jumper and reboot normally.
- **Detection**: GPIO pin state monitor
- **Solution**: Secure boot config, boot fuse lock
- **Tags**: GPIO, debug, boot bypass

## Side-Channel Power Analysis for Key Extraction

- **Attack Type**: Power Fault Injection
- **Target**: Smartcards, Crypto Devices
- **Vulnerability**: Lacks power analysis countermeasures
- **MITRE**: T1203 – Exploitation for Privilege Escalation
- **Impact**: Secret key theft
- **Tools**: Oscilloscope, Shunt Resistor, ChipWhisperer
- **Scenario**: Extracting encryption keys by analyzing power consumption during crypto operations.
- **Attack Steps**: Step 1: Identify Vcc and GND pins of target microcontroller.Step 2: Insert small resistor (e.g., 1 ohm) between Vcc and supply to measure current.Step 3: Connect oscilloscope probes across resistor.Step 4: Run known encryption operation on device (e.g., login attempt).Step 5: Capture power traces during operations.Step 6: Analyze traces using ChipWhisperer or similar tool to correlate with key bits.Step 7: Extract full key via statistical attack.
- **Detection**: Power fluctuation monitor
- **Solution**: Add noise, power balancing, shield
- **Tags**: DPA, side-channel, crypto

## Debug Shell via HDMI/DisplayPort Interface

- **Attack Type**: Hidden Interface Exploitation
- **Target**: Set-top Boxes, Dev Boards
- **Vulnerability**: Debug display not disabled
- **MITRE**: T1056.001 – Input Capture
- **Impact**: Configuration leak or dev options
- **Tools**: HDMI Capture Card or Monitor
- **Scenario**: Accessing boot-time debug logs or hidden menus via HDMI connected to PC.
- **Attack Steps**: Step 1: Connect target device’s HDMI/DP port to monitor or capture card.Step 2: Power on the device and observe boot log or hidden menus.Step 3: If debug shell or dev menu is accessible, navigate using keyboard.Step 4: Attempt to change settings, enable verbose/debug options.Step 5: Use screenshot or recording to analyze messages.Step 6: Look for version info, kernel dumps, developer shortcuts.Step 7: Combine with UART/JTAG for deeper access.
- **Detection**: Display output monitoring
- **Solution**: Disable debug console on production builds
- **Tags**: HDMI debug, dev console

## Direct NAND Flash Dump via BGA Pad Access

- **Attack Type**: Chip-Off Attack
- **Target**: Smartphones, Embedded Boards
- **Vulnerability**: Unencrypted NAND flash
- **MITRE**: T1005 – Data from Local System
- **Impact**: Recover files, bypass lock
- **Tools**: Hot air gun, NAND adapter, Probing station
- **Scenario**: Extracting data by accessing NAND flash pads using probing station.
- **Attack Steps**: Step 1: Remove NAND chip using hot air gun (BGA format).Step 2: Clean pads and mount chip on BGA adapter.Step 3: Connect to NAND reader or flash programmer.Step 4: Dump NAND flash content using dedicated software.Step 5: Analyze dump for partitions (e.g., user data, system files).Step 6: Recover deleted files or credentials.Step 7: Flash modified dump back (optional).
- **Detection**: NAND integrity check
- **Solution**: Full disk encryption
- **Tags**: chip-off, NAND, data recovery

## Tampering Internal Sensors via External Magnet

- **Attack Type**: Sensor Tampering
- **Target**: Laptops, Phones
- **Vulnerability**: No sensor shielding or redundancy
- **MITRE**: T1556 – Spoofing
- **Impact**: Bypass lid-close or sleep detection
- **Tools**: Neodymium magnet, compass
- **Scenario**: Manipulating internal sensor readings (e.g., hall sensor, compass) using a magnet.
- **Attack Steps**: Step 1: Identify sensor in target device (e.g., hall effect for lid detection).Step 2: Power on device and slowly bring strong magnet near sensor area.Step 3: Observe screen or system behavior (e.g., suspend, brightness drop).Step 4: Use magnet to trick sensor during boot or sleep transition.Step 5: If attacker wants to disable sensor-triggered lockdowns, use magnet consistently.Step 6: Log impact and reset to normal after attack.
- **Detection**: Multiple sensor verification
- **Solution**: Sensor fusion logic
- **Tags**: magnet, spoof, sensor, trick

## SDR-Based EM Fault Injection

- **Attack Type**: Electromagnetic Fault Injection
- **Target**: Secure microcontrollers
- **Vulnerability**: Lacks EM shielding
- **MITRE**: T1495 – Fault Injection
- **Impact**: Code execution, bypass
- **Tools**: HackRF, EM Probe, Signal Generator
- **Scenario**: Disrupting processor timing using electromagnetic pulses to cause logic errors.
- **Attack Steps**: Step 1: Place EM probe close to target chip.Step 2: Generate high-frequency pulse bursts via HackRF or signal generator.Step 3: Synchronize pulse with operation (e.g., decryption, login).Step 4: Monitor for abnormal behavior – e.g., bypass login.Step 5: Tune frequency and timing to increase success.Step 6: Log result and repeat for reliable exploit.Step 7: Use to trigger race conditions or corrupt memory.
- **Detection**: EM sensors, timing watchdogs
- **Solution**: Harden with EM shielding, detect anomalies
- **Tags**: EMFI, SDR, hackRF

## Boot Code Corruption via EEPROM Overwrite

- **Attack Type**: Persistent Tamper
- **Target**: Routers, Dev Boards
- **Vulnerability**: Boot config in writable EEPROM
- **MITRE**: T1542.003 – Boot Loader Mods
- **Impact**: Disable security checks
- **Tools**: EEPROM programmer (CH341A), SOIC8 clip
- **Scenario**: Altering boot sequence by modifying EEPROM config to disable protection.
- **Attack Steps**: Step 1: Locate EEPROM near CPU and attach SOIC8 clip.Step 2: Connect to programmer (e.g., CH341A).Step 3: Use software (e.g., AsProgrammer) to read EEPROM.Step 4: Modify boot flag (e.g., disable secure boot, enable dev mode).Step 5: Write back to EEPROM.Step 6: Reboot device to observe behavior (e.g., unlock, verbose log).Step 7: Reverse if needed by restoring backup.
- **Detection**: Checksum comparison
- **Solution**: Lock critical boot config
- **Tags**: EEPROM, secure boot, tamper

## SPI Bus Interception for Live Data Sniffing

- **Attack Type**: Bus Snooping
- **Target**: Smartcards, IoT Controllers
- **Vulnerability**: SPI bus unencrypted
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Credentials/data leakage
- **Tools**: Logic Analyzer (Saleae), Test clips
- **Scenario**: Intercepting SPI communication between MCU and peripheral to sniff data like keystrokes or sensor values.
- **Attack Steps**: Step 1: Open device and identify the SPI bus lines: MOSI, MISO, CLK, CS.Step 2: Refer to datasheet to locate those pins on the flash or MCU.Step 3: Clip logic analyzer probes to each line (non-invasive).Step 4: Connect analyzer to PC and open its software.Step 5: Start recording while device is in use (e.g., logging in).Step 6: Observe captured data in hex – analyze for plaintext, credentials.Step 7: Optionally export log and decode protocol manually.
- **Detection**: SPI line activity, data rate checks
- **Solution**: Encrypt SPI traffic, isolate buses
- **Tags**: SPI, sniffing, credentials, Saleae

## Chip Reset Pin Bypass via Forced High

- **Attack Type**: Pin-Level Tampering
- **Target**: Dev Boards, IoT Kits
- **Vulnerability**: No reset pin protection
- **MITRE**: T1495 – Fault Injection
- **Impact**: Interrupt boot logic
- **Tools**: Jumper wire, Power supply, Datasheet
- **Scenario**: Forcing reset pin to HIGH using external power to prevent normal boot behavior.
- **Attack Steps**: Step 1: Locate microcontroller reset (RST) pin using datasheet.Step 2: Identify test pad or exposed trace connected to RST.Step 3: Connect 3.3V supply to RST pin using jumper.Step 4: Keep pin HIGH during boot cycle.Step 5: Observe whether firmware fails to start or enters test mode.Step 6: Analyze device response — some enter waiting or fail-safe state.Step 7: Use UART/JTAG in this mode to extract info.
- **Detection**: Boot failure log, GPIO monitor
- **Solution**: Pull-down RST, boot delay
- **Tags**: reset pin, logic glitch

## Optical Fault Injection Using Camera Flash

- **Attack Type**: Fault Injection
- **Target**: Phones, IR-Gated Systems
- **Vulnerability**: Optical sensor unshielded
- **MITRE**: T1562.001 – Sensor Manipulation
- **Impact**: Login spoofing, false triggers
- **Tools**: Camera phone flash, Laser pointer
- **Scenario**: Blinding or glitching optical sensors using sudden flash of high-intensity light.
- **Attack Steps**: Step 1: Locate optical sensor (IR, proximity) on target device.Step 2: Power on device and aim camera flash directly at sensor.Step 3: Trigger flash repeatedly during critical operation (e.g., login, unlock).Step 4: Observe if sensor glitches or behaves abnormally.Step 5: Try using colored laser (red/green) to alter response.Step 6: Combine with action like proximity spoofing.Step 7: Log results and analyze if protection fails.
- **Detection**: Sensor sanity check
- **Solution**: Sensor fusion, physical shields
- **Tags**: optical, sensor spoof, flash

## eMMC Dump via Test Pads on PCB

- **Attack Type**: Interface Exploitation
- **Target**: Phones, Tablets, Cameras
- **Vulnerability**: Test pads not masked or encrypted
- **MITRE**: T1005 – Local Data Access
- **Impact**: Full file access
- **Tools**: eMMC reader, Soldering iron, Test clips
- **Scenario**: Dumping internal storage from eMMC chip using test pads under PCB.
- **Attack Steps**: Step 1: Open device and flip PCB to locate tiny test pads.Step 2: Use continuity test to map pads to CMD, CLK, DAT0, VCC, GND.Step 3: Solder ultra-fine wires or use pogo-pins.Step 4: Connect to SD/eMMC reader.Step 5: Use software to mount or dump partition.Step 6: Analyze content using forensic tools.Step 7: Extract logs, firmware, user data.
- **Detection**: Watchdog logs, integrity hash
- **Solution**: Encrypt eMMC and cover pads
- **Tags**: eMMC, raw dump, chip tap

## Glitch Bootloader Timing via Manual Power Cycle

- **Attack Type**: Boot Timing Fault
- **Target**: DIY Dev Boards, Routers
- **Vulnerability**: Bootloader does not handle glitchy input
- **MITRE**: T1542 – Boot Process Injection
- **Impact**: Debug mode abuse
- **Tools**: Power switch, Stop watch
- **Scenario**: Exploiting bootloader timeout by rapidly cycling power to enter debug mode.
- **Attack Steps**: Step 1: Read online documentation to find bootloader timeout (e.g., 5s window).Step 2: Power on device and immediately cut off power before timeout.Step 3: Repeat power cycles until device halts or fails into safe/debug mode.Step 4: Once in halted mode, try UART or USB connection.Step 5: Access boot options or serial console.Step 6: Log behavior and analyze boot flow.Step 7: Use debug port to explore system.
- **Detection**: Boot logs, cycle count
- **Solution**: Harden timeout code
- **Tags**: boot glitch, timing bug

## I2C Clock Stretching to Desync Sensor

- **Attack Type**: Bus Fault Injection
- **Target**: Embedded Controllers, BMS
- **Vulnerability**: No validation of I2C timing
- **MITRE**: T1565.001 – Sensor Manipulation
- **Impact**: False sensor readings
- **Tools**: Arduino, Logic analyzer
- **Scenario**: Exploiting I2C timing flaw by slowing down SCL line to desync devices.
- **Attack Steps**: Step 1: Tap into I2C bus connecting sensor and controller.Step 2: Use microcontroller to act as malicious I2C device.Step 3: Implement clock stretching (holding SCL LOW for long).Step 4: Introduce timing shifts during critical data transfers.Step 5: Analyze controller response – may misread or skip data.Step 6: Use logic analyzer to verify desync.Step 7: Trigger incorrect values or override sensor data.
- **Detection**: Timing violation alerts
- **Solution**: Validate timings in firmware
- **Tags**: I2C glitch, sensor tamper

## OTP Lock Bits Bypass via Voltage Brute Force

- **Attack Type**: Memory Protection Tamper
- **Target**: MCUs with OTP Lock
- **Vulnerability**: No voltage threshold detection
- **MITRE**: T1203 – Exploit Protection Mechanism
- **Impact**: Firmware dump or unlock
- **Tools**: Adjustable PSU, Oscilloscope
- **Scenario**: Applying variable voltage levels to bypass One-Time-Programmable (OTP) lock bits.
- **Attack Steps**: Step 1: Power down device and identify VCC pin of MCU.Step 2: Connect PSU and ramp voltage near max range (e.g., 3.6–4.0V for 3.3V chip).Step 3: Monitor system behavior while attempting firmware read.Step 4: Log any unexpected data leakage.Step 5: Reattempt read multiple times with variations.Step 6: Capture dump if read protection fails.Step 7: Verify OTP bits in hex dump.
- **Detection**: Voltage log, access log
- **Solution**: Enforce voltage clamps
- **Tags**: OTP, voltage bypass, dump

## USB HID Injection via Modified Cable

- **Attack Type**: Interface Backdoor
- **Target**: Desktops, Laptops
- **Vulnerability**: USB allows automatic HID
- **MITRE**: T1056.001 – Input Capture
- **Impact**: System compromise, backdoor
- **Tools**: MalDuino / Digispark / Rubber Ducky
- **Scenario**: Using modified USB cable to inject keyboard commands silently.
- **Attack Steps**: Step 1: Obtain Digispark or HID-injection board and program it with payload.Step 2: Embed device inside USB cable.Step 3: Connect to target system.Step 4: Device appears as keyboard and types pre-loaded script (e.g., open CMD, add user).Step 5: Payload executes automatically.Step 6: Disconnect and analyze results.Step 7: Clean traces if needed.
- **Detection**: USB whitelist, behavioral alert
- **Solution**: Disable HID class for USB ports
- **Tags**: USB, rubber ducky, keystroke

## RTC Tampering to Invalidate Certificates

- **Attack Type**: Time Fault Injection
- **Target**: Network Devices, Web Cams
- **Vulnerability**: RTC not authenticated
- **MITRE**: T1600 – Manipulate System Clock
- **Impact**: Fake certs accepted
- **Tools**: RTC Jumper Pins, Software
- **Scenario**: Changing Real Time Clock (RTC) to bypass time-bound certificate validation.
- **Attack Steps**: Step 1: Identify RTC chip or battery (coin cell) on board.Step 2: Short reset pin or remove battery to reset time.Step 3: Boot device and verify system time.Step 4: Manually set time to pre-certificate expiry date.Step 5: Restart device and access time-sensitive services.Step 6: If system allows outdated certs, access is granted.Step 7: Restore battery to keep false time.
- **Detection**: Time drift check
- **Solution**: Sync with NTP, secure RTC
- **Tags**: RTC spoof, TLS cert bypass

## Fault Injection Using Peltier-Induced Thermal Shock

- **Attack Type**: Thermal Fault Injection
- **Target**: Secure ICs, Crypto Chips
- **Vulnerability**: No thermal regulation or watchdog
- **MITRE**: T1495 – Fault Injection
- **Impact**: Bit flips, auth failure
- **Tools**: Peltier Module, Thermal Paste, Thermometer
- **Scenario**: Rapidly cooling and heating chip to cause timing instability or memory corruption.
- **Attack Steps**: Step 1: Mount Peltier cooler on chip with thermal paste.Step 2: Power on module to cool chip below 0°C.Step 3: Quickly reverse polarity to heat chip up.Step 4: Monitor chip behavior during temperature stress.Step 5: Observe glitches like bit-flips, boot hangs, logic errors.Step 6: Trigger operations like login or encryption during shock.Step 7: Record results and attempt data extraction.
- **Detection**: On-chip temperature sensors
- **Solution**: Add thermal watchdog & auto reset
- **Tags**: thermal glitch, bit error

## Capacitor Discharge to Induce Power Glitch

- **Attack Type**: Power Fault Injection
- **Target**: Microcontrollers
- **Vulnerability**: Inadequate power surge protection
- **MITRE**: T1495 – Fault Injection
- **Impact**: Skip auth, logic errors
- **Tools**: Large capacitor (470uF+), Jumper wires
- **Scenario**: Discharging a capacitor into the power line to cause glitches and bypass security routines.
- **Attack Steps**: Step 1: Locate the VCC line going to the main chip on PCB.Step 2: Charge a capacitor by briefly connecting it to 3.3V supply.Step 3: Disconnect power, then connect the charged capacitor to VCC line.Step 4: Reconnect power and observe if boot routine is glitched (e.g., skips checks).Step 5: Repeat process with varied discharge timing.Step 6: Try accessing privileged features during glitch.Step 7: Log any successful bypass.
- **Detection**: Voltage loggers, boot monitors
- **Solution**: Add filtering caps, power regulators
- **Tags**: capacitor, surge, logic glitch

## Overclocking Exploit via External Crystal Swap

- **Attack Type**: Timing Fault Injection
- **Target**: Embedded Boards
- **Vulnerability**: No clock integrity validation
- **MITRE**: T1600 – Hardware Timing Exploit
- **Impact**: Bypass logic, corruption
- **Tools**: Higher-frequency crystal, Soldering iron
- **Scenario**: Replacing the system clock with higher frequency crystal to trigger logic failure.
- **Attack Steps**: Step 1: Identify system clock crystal (usually near MCU, e.g., 8MHz).Step 2: Desolder the original and replace it with a 16MHz one.Step 3: Power on device with new clock.Step 4: Observe if firmware or bootloader malfunctions due to speed mismatch.Step 5: Try exploiting failures to access secure functions.Step 6: Record crashes, command skips, or corrupted values.Step 7: Revert back original crystal if needed.
- **Detection**: Frequency watchdogs
- **Solution**: Clock lock or PLL check
- **Tags**: overclock, timing, glitch

## Thermal Delay Exploit via Hairdryer

- **Attack Type**: Thermal Fault Injection
- **Target**: Embedded Devices
- **Vulnerability**: No thermal throttling
- **MITRE**: T1495 – Fault Injection
- **Impact**: Bypass or crash via heat
- **Tools**: Hairdryer, Thermometer
- **Scenario**: Using a hairdryer to slowly heat a device until timing or logic faults occur.
- **Attack Steps**: Step 1: Power on target and run normal operation.Step 2: Slowly blow warm air using hairdryer on chip or board.Step 3: Observe for signs of heat-induced glitches (e.g., delayed login, reboot).Step 4: Gradually increase heat to push chip beyond limits.Step 5: Log any access bypass or timing issue.Step 6: Use cooling spray after to restore function.Step 7: Repeat for multiple runs to identify vulnerable zones.
- **Detection**: Onboard temp sensors
- **Solution**: Add heat sinks, watchdogs
- **Tags**: heat, glitch, timing fault

## Ethernet PHY Debug Port Exploitation

- **Attack Type**: Hidden Interface Abuse
- **Target**: IP Cameras, Gateways
- **Vulnerability**: Debug port enabled in production
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Network impersonation
- **Tools**: Ethernet Debugger, PHY datasheet
- **Scenario**: Using PHY debug access to alter MAC or sniff boot-time network config.
- **Attack Steps**: Step 1: Identify Ethernet PHY chip and its debug pins (MIIM, MDIO).Step 2: Solder wires to debug port.Step 3: Connect to PHY debugger or dev board via MDIO protocol.Step 4: Read registers and monitor during boot.Step 5: Try altering MAC address or link settings.Step 6: Reboot and observe network misbehavior.Step 7: Use for MITM or network masking.
- **Detection**: Monitor MAC/memory changes
- **Solution**: Lock PHY config, disable debug
- **Tags**: Ethernet, PHY, MAC spoof

## Crystal Resonance Fault via Piezo Sound

- **Attack Type**: Acoustics-Based Glitching
- **Target**: IoT, Embedded Sensors
- **Vulnerability**: Crystal not isolated from vibration
- **MITRE**: T1495 – Fault Injection
- **Impact**: Logic corruption, crash
- **Tools**: Piezo speaker, Audio generator app
- **Scenario**: Using sound vibration to destabilize clock crystal, affecting chip timing.
- **Attack Steps**: Step 1: Power on the target device.Step 2: Place piezo speaker near crystal oscillator.Step 3: Play tone at resonant frequency (try 20kHz–30kHz).Step 4: Monitor for logic faults or timing errors.Step 5: Try accessing login or secure operations during this period.Step 6: Record repeatable fault if found.Step 7: Stop tone and check for normal behavior restoration.
- **Detection**: Vibration monitoring
- **Solution**: Shielding, dampening pads
- **Tags**: acoustic, oscillator, glitch

## Fault Injection by Ground Loop Creation

- **Attack Type**: Power Fault Injection
- **Target**: Industrial Controllers
- **Vulnerability**: No protection against GND instability
- **MITRE**: T1495 – Fault Injection
- **Impact**: Device instability, boot loop
- **Tools**: Jumper wires, Multimeter
- **Scenario**: Forcing unstable ground reference to corrupt system behavior.
- **Attack Steps**: Step 1: Identify GND pin on MCU or power rail.Step 2: Connect GND from an external USB source with slight offset voltage.Step 3: This creates a ground loop with minor voltage difference.Step 4: Boot device and observe anomalies (e.g., random reboot, logic flip).Step 5: Attempt sensitive actions (e.g., auth or encryption).Step 6: Remove connection and compare behavior.Step 7: Repeat with altered connections to test fault regions.
- **Detection**: Ground loop detection, logging
- **Solution**: Use isolated GND, ESD guard
- **Tags**: ground loop, power fault

## Backdoor Trigger via GPIO Jumper

- **Attack Type**: Hidden Debug Trigger
- **Target**: IoT Products
- **Vulnerability**: Hidden debug triggers not removed
- **MITRE**: T1542 – Boot Modification
- **Impact**: Dev access or bypass
- **Tools**: Jumper wire, Datasheet
- **Scenario**: Exploiting a debug backdoor left in firmware, triggered via GPIO state.
- **Attack Steps**: Step 1: Use datasheet to identify unused GPIOs.Step 2: Power off device and connect jumper wire to pull GPIO high or low.Step 3: Power on device with wire attached.Step 4: If firmware has debug backdoor, you may enter root shell or dev menu.Step 5: Use UART or display to verify access.Step 6: Remove jumper and reboot normally.Step 7: Try different GPIOs to test behavior.
- **Detection**: GPIO trigger monitor
- **Solution**: Disable debug logic in prod
- **Tags**: GPIO, debug, backdoor

## Sensor Data Injection via I2C Spoofing

- **Attack Type**: Bus Spoofing
- **Target**: Smart Thermostats, Controllers
- **Vulnerability**: I2C bus trust with no integrity check
- **MITRE**: T1565.001 – Sensor Manipulation
- **Impact**: Force false alarms or triggers
- **Tools**: Arduino/RPi, Logic analyzer
- **Scenario**: Faking sensor data using malicious I2C slave to feed false readings.
- **Attack Steps**: Step 1: Identify I2C address of sensor using scanner.Step 2: Detach original sensor or block data line.Step 3: Connect Arduino acting as fake sensor at same address.Step 4: Program Arduino to return controlled values (e.g., temp = 20°C).Step 5: Reboot target and observe if it accepts fake data.Step 6: Log behavior based on spoofed input.Step 7: Optionally modify spoof in real-time.
- **Detection**: Sensor sanity test
- **Solution**: Use signed sensor data, fusion
- **Tags**: spoof sensor, I2C inject

## Memory Corruption via Button Debounce Abuse

- **Attack Type**: Firmware Logic Fault
- **Target**: Consumer Electronics
- **Vulnerability**: Poor button input handling
- **MITRE**: T1203 – Input Validation Failure
- **Impact**: Access bypass, crash
- **Tools**: Finger or auto-clicker
- **Scenario**: Exploiting poor debounce logic by pressing buttons in rapid succession.
- **Attack Steps**: Step 1: Power on device and reach login/menu screen.Step 2: Rapidly press hardware button (e.g., reset or select) multiple times.Step 3: Observe if system glitches, crashes or skips logic.Step 4: Time presses with bootup to potentially bypass checks.Step 5: If system reboots or unlocks, log event.Step 6: Use repeat pattern for consistent behavior.Step 7: Stop and allow system to stabilize.
- **Detection**: Input rate monitoring
- **Solution**: Add debounce filters
- **Tags**: logic fault, rapid press

## Faulty Peripheral Behavior via USB-Powered Sensor

- **Attack Type**: Power Tampering
- **Target**: Laptops, Dev Kits
- **Vulnerability**: No USB input voltage protection
- **MITRE**: T1496 – Resource Hijacking
- **Impact**: USB crash or bypass
- **Tools**: USB sensor, Multimeter
- **Scenario**: Connecting poorly regulated sensor to USB causes fault cascade.
- **Attack Steps**: Step 1: Plug low-cost or modded USB sensor into target device.Step 2: Ensure sensor pulls more current or provides unstable voltage.Step 3: Monitor device behavior during sensor detection.Step 4: Observe for crashes, I/O errors, or reset.Step 5: Reproduce and analyze fault logs.Step 6: Use as denial or entry vector.Step 7: Disconnect and power cycle device.
- **Detection**: USB voltage monitor
- **Solution**: Use overcurrent protection ICs
- **Tags**: USB, sensor crash, power

## Firmware Corruption via Incomplete Update

- **Attack Type**: Update Process Tampering
- **Target**: IoT, Routers, DVRs
- **Vulnerability**: No protection against update interruption
- **MITRE**: T1542.003 – Bootloader Corruption
- **Impact**: Recovery mode abuse
- **Tools**: Power switch, Firmware updater
- **Scenario**: Interrupting a firmware update to corrupt image and trigger recovery/debug mode.
- **Attack Steps**: Step 1: Initiate firmware update via official method (USB/OTA).Step 2: During flashing (observe progress bar), power off the device abruptly.Step 3: Wait 5 seconds, then power it back on.Step 4: Check if device enters recovery/debug mode.Step 5: If yes, explore available options (e.g., shell, re-flash, logs).Step 6: Try multiple timing variations to identify vulnerability.Step 7: Restore proper firmware using update tool.
- **Detection**: Boot logs, flash integrity
- **Solution**: Use atomic updates, rollback check
- **Tags**: firmware crash, update glitch

## Fault Induced Bypass via Power Button Abuse

- **Attack Type**: Input Timing Exploit
- **Target**: Embedded UI Systems
- **Vulnerability**: Faulty input parsing logic
- **MITRE**: T1600 – Boot Timing Abuse
- **Impact**: Bypass to debug/hidden mode
- **Tools**: Finger, Power toggle
- **Scenario**: Rapidly toggling power button to induce boot faults and bypass bootloader.
- **Attack Steps**: Step 1: Press and hold power button for 5 seconds to boot.Step 2: While booting, press power button rapidly (on-off) multiple times.Step 3: Device may boot into alternate or safe mode due to misinterpreted input.Step 4: Try accessing hidden menus or bypass screens.Step 5: Record if boot proceeds to shell without full auth.Step 6: Repeat timing to increase success.Step 7: Reboot and verify system state.
- **Detection**: Input timing logs
- **Solution**: Input debounce, startup lock
- **Tags**: power button glitch, boot abuse

## Force Reflash via USB-Auto Recovery Exploit

- **Attack Type**: Firmware Tampering
- **Target**: Smart Displays, Routers
- **Vulnerability**: USB recovery not protected
- **MITRE**: T1542.001 – Boot Process Injection
- **Impact**: Firmware overwrite
- **Tools**: USB drive, Firmware image
- **Scenario**: Forcing a USB-based auto-recovery mode to overwrite firmware without access.
- **Attack Steps**: Step 1: Obtain original or custom firmware file (check vendor site).Step 2: Format USB to FAT32, and place firmware with correct name (e.g., firmware.bin).Step 3: Power off device and insert USB.Step 4: Hold specific button (Reset or Boot) and power on.Step 5: Device should auto-detect firmware and start reflashing.Step 6: If firmware is accepted, attacker can modify device logic.Step 7: Remove USB and verify changed behavior.
- **Detection**: Boot process logs
- **Solution**: Require signed firmware
- **Tags**: usb firmware overwrite

## Desoldering Protection Resistor to Disable Logging

- **Attack Type**: Logging Tamper
- **Target**: Dev Boards, IoT Dev Kits
- **Vulnerability**: Lack of tamper detection
- **MITRE**: T1565.002 – Data Removal
- **Impact**: No forensic trace of attack
- **Tools**: Soldering iron, Tweezers
- **Scenario**: Removing resistor that enables UART or log tracing to prevent monitoring of attacks.
- **Attack Steps**: Step 1: Identify series resistor on UART TX line via PCB silkscreen or datasheet.Step 2: Heat and remove resistor carefully using tweezers.Step 3: Reboot device and check that logging is disabled.Step 4: Conduct attack with reduced chance of trace capture.Step 5: Optionally replace resistor to hide tampering.Step 6: Monitor behavior – no logs should be stored.Step 7: Use alternate method to re-enable logs if needed.
- **Detection**: Log error alerts, self-check
- **Solution**: Secure resistor path, tamper seal
- **Tags**: UART disable, logging tamper

## Fault Injection via Static Charge Discharge

- **Attack Type**: ESD Fault
- **Target**: Touch Panels, Dev Kits
- **Vulnerability**: No ESD filtering or protection
- **MITRE**: T1495 – Fault Injection
- **Impact**: Boot skip, auth glitch
- **Tools**: Wool cloth, Plastic rod
- **Scenario**: Using body-static or fabric-generated static to disrupt device boot or behavior.
- **Attack Steps**: Step 1: Rub plastic rod with wool to generate static.Step 2: Approach device while touching ground or plastic.Step 3: Lightly discharge near sensor or metal ports (e.g., USB, GPIO).Step 4: Monitor for any glitches (boot loops, login skip).Step 5: Repeat at different components and power states.Step 6: Use known static sources like plastic chairs or acrylic.Step 7: Reboot and verify behavior.
- **Detection**: ESD monitor, watchdog
- **Solution**: Add TVS diodes, shielding
- **Tags**: ESD fault, plastic trick

## Boot Skip via SD Card Insertion Trick

- **Attack Type**: Interface Exploitation
- **Target**: Embedded Linux Devices
- **Vulnerability**: Unprotected SD boot logic
- **MITRE**: T1542.001 – Boot Process Hijack
- **Impact**: Debug shell or bypass
- **Tools**: SD Card, Firmware tools
- **Scenario**: Triggering bootloader to skip checks or enter test mode when SD card is detected.
- **Attack Steps**: Step 1: Format SD card and place empty or modified config file.Step 2: Power off device and insert SD.Step 3: Power on while pressing Boot or Select button.Step 4: Device may enter firmware write/test/diags mode.Step 5: If root shell or verbose log is accessible, explore further.Step 6: Reboot without SD and check persistent effects.Step 7: Test with various card formats and file names.
- **Detection**: SD access monitor
- **Solution**: Require signed recovery configs
- **Tags**: SD boot, shell access

## Weak Pull-up Abuse to Crash Boot

- **Attack Type**: Circuit Fault Injection
- **Target**: Routers, IoT Boards
- **Vulnerability**: Weak electrical isolation
- **MITRE**: T1600 – Hardware Manipulation
- **Impact**: Halt, alternate boot state
- **Tools**: Jumper wire, Multimeter
- **Scenario**: Exploiting weak pull-up resistor on boot GPIO to force incorrect logic level.
- **Attack Steps**: Step 1: Locate boot-mode GPIO with weak pull-up resistor.Step 2: Connect GPIO to ground directly via jumper.Step 3: Power on device and observe boot behavior.Step 4: System may enter wrong mode, crash, or halt.Step 5: Record which state causes safe/debug entry.Step 6: Try various resistors to simulate voltage levels.Step 7: Remove jumper and restore normal boot.
- **Detection**: GPIO value logger
- **Solution**: Strengthen pull-up/pull-down
- **Tags**: pull-up glitch, boot crash

## Hidden Serial Shell via HDMI-CEC Command

- **Attack Type**: Interface Tampering
- **Target**: Smart TV boxes, HDMI dev boards
- **Vulnerability**: Debug triggers via CEC left active
- **MITRE**: T1056.001 – Interface Access
- **Impact**: Root shell, log access
- **Tools**: TV or HDMI-CEC injector
- **Scenario**: Sending HDMI-CEC commands to trigger hidden serial debug shell.
- **Attack Steps**: Step 1: Connect HDMI-CEC capable device (e.g., TV with CEC enabled).Step 2: Send CEC message (like standby, record on, or vendor-specific debug ID).Step 3: Monitor if target device outputs shell or logs over serial/UART.Step 4: Try sending commands in early boot.Step 5: If root/debug shell appears, interact via console.Step 6: Document success commands and timing.Step 7: Disable CEC after test.
- **Detection**: CEC message audit
- **Solution**: Block unused CEC functions
- **Tags**: HDMI, serial debug

## Glitching Memory Read via Improper Grounding

- **Attack Type**: Fault Injection
- **Target**: Microcontrollers
- **Vulnerability**: No GND reference watchdog
- **MITRE**: T1495 – Fault Injection
- **Impact**: Data leakage, auth skip
- **Tools**: Jumper wire, Breadboard
- **Scenario**: Disconnecting ground while keeping VCC to force partial memory operation.
- **Attack Steps**: Step 1: Connect power supply where GND line can be toggled.Step 2: Power on device, then temporarily disconnect GND for a few milliseconds.Step 3: Observe if memory read functions skip bytes or output gibberish.Step 4: Log dump contents.Step 5: If data is dumped, look for secrets.Step 6: Reboot device to verify if corruption is permanent.Step 7: Repeat with longer or shorter GND cuts.
- **Detection**: Power/ground pin sensor
- **Solution**: Redundant GND monitoring
- **Tags**: glitch ground, VCC error

## Reading eMMC via Test Pads

- **Attack Type**: Chip-Level Interface Abuse
- **Target**: eMMC Storage
- **Vulnerability**: Exposed debug pads
- **MITRE**: T1120 (Peripheral Device Discovery)
- **Impact**: Full disk image, bypass OS-level protections
- **Tools**: Multimeter, SD/eMMC reader adapter, USB microscope
- **Scenario**: eMMC chips have hidden test pads exposed on PCB which can be tapped for data access.
- **Attack Steps**: Step 1: Power off the device and open it with tools. Step 2: Use USB microscope or magnifying glass to locate small test points on PCB near eMMC chip. Step 3: Use a multimeter in continuity mode to trace pads to eMMC pinouts (CMD, CLK, DAT0-DAT3, VCC, GND). Step 4: Solder thin wires (e.g. 30AWG) to these pads carefully. Step 5: Connect wires to an SD-to-USB adapter (wired to eMMC standard). Step 6: Plug into computer; the eMMC might mount as a normal storage device. Step 7: Use dd or disk imaging tool to create full dump. Step 8: Search dump for sensitive files or config data.
- **Detection**: Physical trace of soldering, broken PCB coating
- **Solution**: Epoxy chip coating, test pad removal, eMMC encryption
- **Tags**: eMMC, Chip-Off, Data Recovery, Digital Forensics

## UART Root Shell Access

- **Attack Type**: Debug Port Exploitation
- **Target**: Microcontroller or Linux SoC
- **Vulnerability**: Exposed UART with no authentication
- **MITRE**: T1056.001 (Input Capture)
- **Impact**: Root access, bypass all authentication
- **Tools**: USB-to-UART adapter (FTDI), Serial terminal (Putty/minicom)
- **Scenario**: Exposing a UART port allows direct terminal access to a Linux shell, often running as root.
- **Attack Steps**: Step 1: Open the device casing and inspect the PCB. Step 2: Look for a 3- or 4-pin header labeled TX/RX/GND or test pads. Step 3: Use a multimeter to identify GND, then TX/RX by probing while device boots (TX sends data). Step 4: Connect TX of device to RX of adapter, and RX to TX, plus GND to GND. Step 5: Plug adapter into your laptop and open serial terminal (e.g. Putty) with baud rate 115200. Step 6: Power on the device; observe boot log in terminal. Step 7: If a login prompt appears, try pressing Enter or typing commands — sometimes no login required.
- **Detection**: Physical UART header exposed, console logs
- **Solution**: Disable UART in firmware, authentication on console
- **Tags**: UART, Embedded Linux, Debugging

## I2C EEPROM Dump for Passwords

- **Attack Type**: Memory Dump
- **Target**: EEPROM Memory
- **Vulnerability**: Unprotected I2C interface
- **MITRE**: T1003.001 (Credential Dumping: LSASS Memory)
- **Impact**: Leak of plaintext config and secrets
- **Tools**: I2C reader like Bus Pirate or Arduino, EEPROM software
- **Scenario**: Small I2C EEPROMs store system config including passwords in plaintext.
- **Attack Steps**: Step 1: Open device and find 8-pin EEPROM chip (usually marked 24Cxx). Step 2: Use a chip datasheet to identify pins: SDA, SCL, VCC, GND. Step 3: Wire Bus Pirate or Arduino accordingly. Step 4: Power the chip (3.3V/5V depending on chip). Step 5: Use i2cdump or EEPROM reader sketch to extract memory contents. Step 6: Save contents into file and search using text or hex viewer. Step 7: Look for stored keys, IP addresses, admin credentials.
- **Detection**: Visible solder joints, altered I2C signals
- **Solution**: Secure boot, encryption, I2C bus hardening
- **Tags**: EEPROM, I2C, Config Extraction

## JTAG Unlock for Firmware Debugging

- **Attack Type**: Debug Port Abuse
- **Target**: Microcontroller / SoC
- **Vulnerability**: Enabled JTAG port
- **MITRE**: T1040 (Behavior Analysis)
- **Impact**: Full memory dump, persistent malware implant
- **Tools**: JTAGulator or OpenOCD with FTDI adapter, OpenOCD
- **Scenario**: Attackers use JTAG to halt CPU and dump memory directly even if OS is locked.
- **Attack Steps**: Step 1: Locate JTAG pins using datasheet or test-point analysis. Step 2: Solder wires or connect headers to TDI, TDO, TCK, TMS, GND. Step 3: Connect to a JTAG interface (e.g., JTAGulator or FTDI). Step 4: Use OpenOCD to connect: configure target using chip specs. Step 5: Use commands like dump_image or mdw to read memory. Step 6: Pause execution (halt), analyze instruction flow, or set breakpoints. Step 7: Dump memory for analysis or inject payloads.
- **Detection**: Triggered watchdogs, debug halts
- **Solution**: Disable JTAG or lock via fuses
- **Tags**: JTAG, Reverse Engineering, OpenOCD

## SPI Flash Overwrite with Malicious Firmware

- **Attack Type**: Firmware Tampering
- **Target**: SPI Flash
- **Vulnerability**: No integrity checks on flash
- **MITRE**: T1561.001 (Disk Content Manipulation)
- **Impact**: Persistent malware, rootkit installation
- **Tools**: SOIC8 clip, Raspberry Pi, flashrom, hex editor
- **Scenario**: Attacker rewrites SPI flash memory with a modified image to implant persistent malware.
- **Attack Steps**: Step 1: Use SOIC8 clip to connect to SPI flash as in CHIP-INTF-001. Step 2: Dump original firmware using flashrom. Step 3: Edit dump using a hex editor (add backdoor, bypass check). Step 4: Save modified image as firmware_mod.bin. Step 5: Use flashrom -w firmware_mod.bin to overwrite chip. Step 6: Reboot device and verify implant is functional.
- **Detection**: Firmware checksum errors (if any)
- **Solution**: Enforce secure boot, firmware signature
- **Tags**: SPI, Flash Patch, Malware

## Glitching SoC to Bypass Secure Boot

- **Attack Type**: Fault Injection
- **Target**: Microcontroller / SoC
- **Vulnerability**: Voltage glitch vulnerability
- **MITRE**: T1499.004 (System Shutdown: OS Crash)
- **Impact**: Boot bypass, unsigned code execution
- **Tools**: ChipWhisperer, crowbar circuit, oscilloscope
- **Scenario**: Attacker induces voltage glitches during boot to skip authentication.
- **Attack Steps**: Step 1: Identify boot point (e.g., via UART) when device loads firmware. Step 2: Connect glitching device (like ChipWhisperer) to power supply rail. Step 3: Set timing to inject brief voltage drop during boot check. Step 4: Trigger glitch while device starts — retry until boot is bypassed. Step 5: Access system with backdoor if secure boot skipped.
- **Detection**: Glitch signatures, failed boots
- **Solution**: Hardware watchdogs, voltage filter caps
- **Tags**: Fault Injection, ChipWhisperer

## Dumping BIOS Flash via LPC Interface

- **Attack Type**: Legacy Interface Abuse
- **Target**: BIOS/UEFI
- **Vulnerability**: Accessible LPC lines
- **MITRE**: T1003.002 (OS Credential Dumping: Security Account Manager)
- **Impact**: BIOS modification, password recovery
- **Tools**: Logic analyzer, BeagleBone, flashrom
- **Scenario**: Reading BIOS firmware via LPC pins even when protected in software.
- **Attack Steps**: Step 1: Identify LPC pins on BIOS chip using datasheet. Step 2: Solder wires to LCLK, LAD0–LAD3, VCC, GND. Step 3: Connect to logic analyzer or LPC dumper setup. Step 4: Capture LPC traffic or read directly using flashrom + BeagleBone. Step 5: Analyze BIOS dump for passwords or bootloader logic.
- **Detection**: Unusual bus activity
- **Solution**: BIOS Lock, LPC line isolation
- **Tags**: LPC, BIOS hacking

## Fusing Bits to Disable Security

- **Attack Type**: Fuse Tampering
- **Target**: MCU/SoC
- **Vulnerability**: Modifiable security fuses
- **MITRE**: T1600.002 (Hardware Additions)
- **Impact**: Full access to chip functions
- **Tools**: Heat gun, microscope, laser or high voltage source
- **Scenario**: Attacker disables chip security by blowing or shorting fuse bits manually.
- **Attack Steps**: Step 1: Open chip packaging using decapsulation. Step 2: View internal fuse layout under microscope. Step 3: Use micro-laser or high-voltage zap to blow fuse bits. Step 4: Power on chip — security features like JTAG lock disabled. Step 5: Connect to chip with debugger to extract memory.
- **Detection**: Unusual fuse config, chip damage
- **Solution**: Lockdown fuses, tamper detection
- **Tags**: Chip Fuse, Debug Unlock

## Cold Boot RAM Data Extraction

- **Attack Type**: RAM Residue Attack
- **Target**: DRAM
- **Vulnerability**: Data remanence in RAM
- **MITRE**: T1003.005 (Credential Dumping: Cached Domain Credentials)
- **Impact**: Decryption key recovery
- **Tools**: Freezer spray, RAM reader device
- **Scenario**: Residual data in RAM can be recovered by quickly transferring it after power off.
- **Attack Steps**: Step 1: Turn off system and remove RAM immediately. Step 2: Spray RAM stick with freeze spray to preserve data. Step 3: Insert RAM into forensic PC with RAM dumper. Step 4: Run tool to dump memory to file. Step 5: Analyze for passwords, encryption keys.
- **Detection**: Physical RAM move trace, logs
- **Solution**: Full memory encryption
- **Tags**: Cold Boot, RAM Forensics

## EEPROM Lock Bypass Using Voltage

- **Attack Type**: EEPROM Manipulation
- **Target**: EEPROM
- **Vulnerability**: Voltage-unlocked access
- **MITRE**: T1112 (Modify Registry)
- **Impact**: EEPROM overwrite, access elevation
- **Tools**: Variable power supply, EEPROM programmer
- **Scenario**: Applying higher voltage temporarily unlocks write/erase functions.
- **Attack Steps**: Step 1: Identify EEPROM part and datasheet. Step 2: Note unlock voltage (e.g., Vpp = 12V). Step 3: Power chip with normal Vcc and apply Vpp to unlock pin. Step 4: Use programmer to read/write EEPROM contents. Step 5: Dump full memory or modify access settings.
- **Detection**: Sudden EEPROM data loss
- **Solution**: Lock bits, disable Vpp pad
- **Tags**: EEPROM hacking, voltage tricks

## Side-Channel Timing Attack on PIN

- **Attack Type**: Timing Side-Channel
- **Target**: SoC or keypad MCU
- **Vulnerability**: Input timing leaks
- **MITRE**: T1201 (Password Policy Discovery)
- **Impact**: PIN extraction
- **Tools**: Oscilloscope, logic analyzer
- **Scenario**: Measuring timing differences during input comparison reveals correct PIN digits.
- **Attack Steps**: Step 1: Identify pin entry subroutine in firmware or SoC. Step 2: Use oscilloscope to monitor power or pin activity during input. Step 3: Input incorrect PINs and measure processing time. Step 4: Use timing patterns to guess correct digits one by one. Step 5: Eventually extract full PIN via deduction.
- **Detection**: Repeated access pattern
- **Solution**: Constant-time comparison code
- **Tags**: Side-channel, PIN cracking

## Uncovering Hidden Test Firmware

- **Attack Type**: Hidden Debug Firmware
- **Target**: Embedded Flash
- **Vulnerability**: Hidden dev/test routines
- **MITRE**: T1546.001 (Boot or Logon Autostart Execution: Registry Run Keys/Startup Folder)
- **Impact**: Debug shell or bypass
- **Tools**: UART/JTAG, firmware scanner
- **Scenario**: Manufacturers leave test/debug firmware in chips which can be reactivated.
- **Attack Steps**: Step 1: Dump full firmware as in CHIP-INTF-001. Step 2: Use string search or binwalk to locate hidden code sections. Step 3: Identify test commands or backdoor users. Step 4: Send activation command via UART or serial. Step 5: Gain higher access or extra debug features.
- **Detection**: Unusual logs or features
- **Solution**: Strip test firmware before release
- **Tags**: Debug, Test Mode, UART

## Reverse-Engineering Fused Logic via Imaging

- **Attack Type**: Optical RE
- **Target**: ROM / ASIC
- **Vulnerability**: No encryption, visible logic
- **MITRE**: T1600.001 (Add Controller)
- **Impact**: Secret key or logic recovery
- **Tools**: Acid decapsulation tools, SEM microscope
- **Scenario**: Attacker removes chip layers and takes microscopic images to reverse logic.
- **Attack Steps**: Step 1: Use nitric acid to remove chip casing carefully. Step 2: Polish internal die using micro-sandpaper. Step 3: Take high-res images under SEM (Scanning Electron Microscope). Step 4: Manually trace logic gates and ROM patterns. Step 5: Reconstruct circuit logic and extract firmware/hardcoded keys.
- **Detection**: Physical damage evident
- **Solution**: Use encrypted ROM logic
- **Tags**: RE, Visual Analysis

## Chip-Off Attack on Android eMMC

- **Attack Type**: Memory Dump
- **Target**: Android Phone
- **Vulnerability**: No encryption or key in TEE
- **MITRE**: T1552.004 (Unsecured Credentials)
- **Impact**: Full data exfiltration
- **Tools**: Hot air rework station, chip reader
- **Scenario**: Removing eMMC chip from Android device and reading it directly for data recovery.
- **Attack Steps**: Step 1: Use heat gun to remove eMMC chip from PCB. Step 2: Place chip in eMMC socket adapter. Step 3: Connect to PC using eMMC reader. Step 4: Use data recovery tools to dump and mount partitions. Step 5: Browse user data, messages, images.
- **Detection**: Physical chip damage
- **Solution**: Enable full disk encryption
- **Tags**: Chip-Off, Mobile Forensics

## Power Analysis to Reveal Encryption Keys

- **Attack Type**: Side-Channel Power Attack
- **Target**: Crypto Chip
- **Vulnerability**: Power leaks during operations
- **MITRE**: T1207 (Rogue Software)
- **Impact**: AES or RSA key theft
- **Tools**: Oscilloscope, shunt resistor, cryptographic target
- **Scenario**: Attacker measures tiny power differences during encryption to extract keys.
- **Attack Steps**: Step 1: Insert shunt resistor (low ohm) in power line of encryption chip. Step 2: Connect oscilloscope probes across resistor. Step 3: Send known plaintexts repeatedly to chip. Step 4: Record power usage traces. Step 5: Use differential power analysis (DPA) tools to extract AES keys.
- **Detection**: Anomalous power patterns
- **Solution**: Power masking, randomized S-box
- **Tags**: DPA, Side-Channel, Cryptanalysis

## Exploiting Secure Elements via ISO7816 Interface

- **Attack Type**: Smartcard Interface Hack
- **Target**: TPM / Smartcard
- **Vulnerability**: Weak PIN or command access
- **MITRE**: T1552 (Unsecured Credentials)
- **Impact**: Key exfiltration, identity spoofing
- **Tools**: Smart card reader, APDU scripting tool
- **Scenario**: Using standard ISO7816 protocol to interact with secure chips like TPM or payment cards.
- **Attack Steps**: Step 1: Insert secure chip or card into reader. Step 2: Use APDU command set to interact with chip functions. Step 3: Send info-gathering commands like GET DATA. Step 4: Attempt default PINs or bruteforce short ones. Step 5: If unlocked, dump certificate chains, keys, or configurations.
- **Detection**: Logging of access attempts
- **Solution**: Long PINs, attempt lockouts
- **Tags**: Smartcard, TPM, ISO7816

## Bus Snooping with Logic Analyzer

- **Attack Type**: Passive Interface Monitoring
- **Target**: Flash, Config EEPROM
- **Vulnerability**: Unencrypted bus traffic
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Exfiltrate sensitive configs
- **Tools**: Logic analyzer (e.g., Saleae), protocol decoder
- **Scenario**: Reading data from internal buses like SPI or I2C to capture credentials.
- **Attack Steps**: Step 1: Identify SPI/I2C data lines on PCB using datasheet or visual trace. Step 2: Clip logic analyzer probes to CLK, MOSI, MISO (or SDA/SCL). Step 3: Start protocol decoder in logic analyzer software. Step 4: Power on target — observe bus activity. Step 5: Look for readable strings, passwords, commands.
- **Detection**: Logic probe marks
- **Solution**: Encrypt inter-chip comms
- **Tags**: Bus tapping, Logic Sniffing

## NAND Flash Dump Using TSOP Adapter

- **Attack Type**: Direct Chip Dump
- **Target**: NAND Flash
- **Vulnerability**: No encryption or ECC
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Recover deleted or hidden files
- **Tools**: Hot air gun, TSOP adapter, NAND reader
- **Scenario**: NAND flash chips removed and dumped to extract full filesystem image.
- **Attack Steps**: Step 1: Use heat gun to carefully remove TSOP NAND chip. Step 2: Insert into TSOP-to-USB adapter. Step 3: Connect to PC and run NAND reader software. Step 4: Dump chip contents to .bin file. Step 5: Analyze using file carving tools for deleted data, configs.
- **Detection**: Physical chip tamper
- **Solution**: NAND encryption
- **Tags**: Chip-Off, NAND Dump, Forensics

## Reversing Security Fuses via X-Ray Imaging

- **Attack Type**: Fuse Analysis
- **Target**: MCU
- **Vulnerability**: X-ray visible fuse layout
- **MITRE**: T1592.002 (Hardware Information)
- **Impact**: Security bypass strategy planning
- **Tools**: X-ray scanner, imaging software
- **Scenario**: Using X-ray imaging to check fuse states in OTP or security bits.
- **Attack Steps**: Step 1: Place chip in high-resolution X-ray machine. Step 2: Capture multiple angles of internal structure. Step 3: Analyze which fuses are blown (dark spots). Step 4: Reconstruct security configuration of chip. Step 5: Use to deduce which interfaces (JTAG, boot modes) are still active.
- **Detection**: Imaging record logs
- **Solution**: Fuse encryption or fuse masking
- **Tags**: X-ray, RE, Fuses

## BGA Chip Tap via Interposer

- **Attack Type**: Interposer Probing
- **Target**: BGA SoC
- **Vulnerability**: Exposed signals via interposer
- **MITRE**: T1120 (Peripheral Device Discovery)
- **Impact**: Intercept internal commands
- **Tools**: Custom interposer PCB, logic analyzer
- **Scenario**: Using a custom interposer board to access hidden BGA pads on mounted chips.
- **Attack Steps**: Step 1: Design or buy interposer matching BGA footprint. Step 2: Desolder chip and mount it onto interposer. Step 3: Mount interposer onto original PCB. Step 4: Attach logic analyzer to exposed pads. Step 5: Monitor internal communication of BGA device.
- **Detection**: PCB mod visible
- **Solution**: Shielded BGA layouts
- **Tags**: BGA, Interposer, Tap

## Exploiting Weak Random Number Generators in Chips

- **Attack Type**: RNG Attack
- **Target**: SoC or MCU
- **Vulnerability**: Poor entropy source
- **MITRE**: T1600.003 (Brute Force)
- **Impact**: Predictable encryption or access
- **Tools**: Firmware dump, PRNG analysis tools
- **Scenario**: Analyzing weak RNG seeds to predict crypto keys or session tokens.
- **Attack Steps**: Step 1: Dump firmware or memory using flash attack. Step 2: Locate RNG seed initialization code. Step 3: If seed is timestamp or static, simulate RNG locally. Step 4: Generate same key sequence offline. Step 5: Use to impersonate, decrypt, or predict session behavior.
- **Detection**: Anomalous crypto reuse
- **Solution**: True RNG or hardware entropy
- **Tags**: PRNG, Key Cracking, Firmware

## Using Boot ROM Failover via SPI Flash

- **Attack Type**: Boot Failover Abuse
- **Target**: Microcontroller / SoC
- **Vulnerability**: Boot fallback to attacker device
- **MITRE**: T1542.004 (Abuse Elevation Control Mechanism)
- **Impact**: Privilege escalation, data theft
- **Tools**: SPI flash, jumper wires, oscilloscope
- **Scenario**: Some MCUs fall back to external SPI flash if internal ROM fails or is missing — this behavior is abused to boot malicious code.
- **Attack Steps**: Step 1: Read datasheet to identify boot modes and fallback behavior. Step 2: Set boot pins to enable fallback boot from external SPI flash. Step 3: Load malicious bootloader onto SPI flash using flashrom. Step 4: Connect SPI flash to the chip’s SPI pins. Step 5: Power on — the MCU will boot from attacker flash. Step 6: Execute memory dump or open UART shell.
- **Detection**: Unexpected boot logs
- **Solution**: Disable boot fallback in fuses
- **Tags**: SPI, Boot Fallback, MCU Abuse

## SPI Flash Chip Swap on IoT Device

- **Attack Type**: Chip Replacement Attack
- **Target**: SPI Flash
- **Vulnerability**: No firmware validation
- **MITRE**: T1561.001 (Disk Content Manipulation)
- **Impact**: Persistent device compromise
- **Tools**: Hot air gun, SPI flasher
- **Scenario**: Attacker swaps original SPI flash chip with an identical but modified one containing backdoor firmware.
- **Attack Steps**: Step 1: Power off and disassemble IoT device. Step 2: Use hot air gun to desolder SPI flash chip. Step 3: Flash backdoor firmware on an identical chip. Step 4: Solder new chip onto PCB. Step 5: Boot device — firmware runs backdoor code. Step 6: Connect via UART or trigger remote access.
- **Detection**: Firmware hash mismatch (if checked)
- **Solution**: Use secure boot and signing
- **Tags**: Flash Swap, Firmware Mod

## Leveraging Bootloader UART Access

- **Attack Type**: Bootloader Exploitation
- **Target**: Embedded SoC
- **Vulnerability**: Unlocked bootloader over UART
- **MITRE**: T1056.001 (Input Capture)
- **Impact**: Full system takeover
- **Tools**: USB-to-UART adapter, serial terminal
- **Scenario**: Some devices leave bootloader UART interface open, allowing firmware dumping or root shell.
- **Attack Steps**: Step 1: Connect UART TX, RX, GND to USB adapter. Step 2: Power device while watching terminal (115200 baud). Step 3: Interrupt boot process by pressing key. Step 4: Use bootloader commands like dump, flash, loadb to inspect or modify flash. Step 5: Extract flash contents or load custom kernel.
- **Detection**: Serial boot logs
- **Solution**: Lock bootloader, disable UART
- **Tags**: Bootloader UART, Dumping

## Triggering Factory Reset via Hidden GPIO

- **Attack Type**: GPIO Exploit
- **Target**: IoT Device
- **Vulnerability**: Accessible debug GPIO
- **MITRE**: T1546.003 (Registry Run Keys/Startup Folder)
- **Impact**: Password bypass, system reset
- **Tools**: GPIO header, jumper wire
- **Scenario**: Hidden GPIO pin, when grounded at boot, forces factory or debug mode enabling attacker access.
- **Attack Steps**: Step 1: Open casing and inspect for unmarked GPIO pads. Step 2: Use datasheet or boot log to identify reset or debug mode pin. Step 3: Ground the pin using jumper wire during boot. Step 4: Device enters debug/factory mode (shell access or web reset). Step 5: Bypass credentials or reset config.
- **Detection**: Physical access logs
- **Solution**: Remove debug GPIO at production
- **Tags**: GPIO, Debug Access

## Eavesdropping On QSPI Bus for Secrets

- **Attack Type**: QSPI Snooping
- **Target**: Flash Memory
- **Vulnerability**: Unencrypted traffic over QSPI
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Extract firmware in transit
- **Tools**: High-speed logic analyzer, probe hooks
- **Scenario**: Attacker taps high-speed QSPI flash bus to capture sensitive firmware traffic.
- **Attack Steps**: Step 1: Locate QSPI lines: CLK, CS, IO0–IO3. Step 2: Clip logic analyzer probes to those pins. Step 3: Power on device and record bus data. Step 4: Use QSPI decoder to extract read operations. Step 5: Reconstruct firmware or search for keys/passwords.
- **Detection**: Line capacitance changes
- **Solution**: QSPI encryption, access control
- **Tags**: Bus Monitoring, QSPI, Secrets

## Shorting Test Pads to Activate Debug Mode

- **Attack Type**: Debug Mode Exploit
- **Target**: Embedded PCB
- **Vulnerability**: No debug lock mechanism
- **MITRE**: T1600.001 (Hardware Additions)
- **Impact**: Bypass login or root shell
- **Tools**: Tweezers, multimeter
- **Scenario**: Debug/test modes can be activated by shorting specific test pads.
- **Attack Steps**: Step 1: Identify unlabeled test pads near MCU. Step 2: Use datasheet or forum to guess boot/debug combinations. Step 3: During power-up, short two pads using tweezers. Step 4: Device boots into hidden debug mode. Step 5: Access UART, JTAG, or bypass user authentication.
- **Detection**: Visible tampering
- **Solution**: Disable test pads in production
- **Tags**: Test Pads, Debug Mode, Boot Pins

## NAND Flash Intercept on Shared Bus

- **Attack Type**: Shared Bus Interception
- **Target**: NAND Flash
- **Vulnerability**: No bus encryption
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Transparent data theft
- **Tools**: Logic analyzer, NAND decoder
- **Scenario**: On shared NAND buses, attackers can tap signals and monitor communication between CPU and flash.
- **Attack Steps**: Step 1: Identify NAND chip and shared bus layout. Step 2: Probe shared lines (ALE, CLE, WE, RE, D0–D7, CE). Step 3: Record read/write transactions using analyzer. Step 4: Reconstruct file structure or sensitive config. Step 5: Save captured data for further analysis.
- **Detection**: Line voltage anomalies
- **Solution**: Secure NAND interface
- **Tags**: NAND Sniffing, Shared Bus

## Abuse of MCU ROM Bootloader for Dump

- **Attack Type**: ROM Bootloader Abuse
- **Target**: MCU (e.g. STM32)
- **Vulnerability**: ROM bootloader access
- **MITRE**: T1543.003 (Create or Modify System Process)
- **Impact**: Firmware extraction without OS boot
- **Tools**: Serial/USB tool, ROM tool from vendor
- **Scenario**: Many MCUs include a ROM-based bootloader accessible via UART or USB for firmware update.
- **Attack Steps**: Step 1: Identify if ROM bootloader exists (e.g., STMicro, NXP). Step 2: Hold specific boot pins low/high to enable ROM mode. Step 3: Connect to tool via UART or USB. Step 4: Use vendor tool to dump flash memory. Step 5: Analyze dumped firmware for secrets.
- **Detection**: Device may show DFU or boot ROM mode
- **Solution**: Disable bootloader via fuse
- **Tags**: DFU, STM32 ROM Exploit

## Triggering Backdoor via Power Sequence

- **Attack Type**: Power-Based Backdoor
- **Target**: Embedded Device
- **Vulnerability**: Backdoor triggered by power toggling
- **MITRE**: T1211 (Exploitation for Defense Evasion)
- **Impact**: Hidden access, no login
- **Tools**: Power controller, stopwatch
- **Scenario**: Some test backdoors are activated by a precise timing or power toggle sequence.
- **Attack Steps**: Step 1: Research or fuzz timing patterns for power cycles. Step 2: Toggle power in sequences (e.g., on-off-on within 1 sec). Step 3: Device enters debug/test mode after boot. Step 4: Observe UART or LED behavior indicating backdoor mode. Step 5: Access special commands or shell.
- **Detection**: Unusual LED flashes or UART logs
- **Solution**: Remove backdoors pre-production
- **Tags**: Timing Attack, Power Sequence

## SDR-Based Capture of Wireless Debug Interfaces

- **Attack Type**: Wireless Debug Interface Exploit
- **Target**: Wireless-Enabled MCU
- **Vulnerability**: Exposed wireless DFU/OTA
- **MITRE**: T1430 (Location Tracking)
- **Impact**: Remote firmware takeover
- **Tools**: SDR (HackRF), protocol analyzer
- **Scenario**: Some chips expose debugging or configuration over wireless debug channels (e.g., Zigbee OTA, BLE DFU).
- **Attack Steps**: Step 1: Scan for OTA/DFU packets using SDR and protocol decoder. Step 2: Capture update or debug traffic. Step 3: Replay or modify firmware transmission. Step 4: Cause firmware overwrite or data leak. Step 5: Dump updated memory from intercepted device.
- **Detection**: Wireless interference logs
- **Solution**: Secure DFU, OTA signing
- **Tags**: SDR, OTA Hacking, BLE DFU

## Inducing Bit Flips Using Laser Fault Injection

- **Attack Type**: Laser-Induced Fault
- **Target**: Microcontroller / Memory
- **Vulnerability**: Susceptibility to laser energy
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Modify logic or bypass checks
- **Tools**: Infrared laser setup, microscope, open chip
- **Scenario**: Using focused laser to flip bits in protected memory cells for bypass or code change.
- **Attack Steps**: Step 1: Remove chip casing using acid decapsulation. Step 2: Use microscope to align laser with target memory cell. Step 3: Fire pulses during execution or boot time. Step 4: Induce bit flip to skip password check or alter code. Step 5: Observe output or change in behavior via UART.
- **Detection**: Irregular logic behavior
- **Solution**: Silicon shielding or detection mesh
- **Tags**: Fault Injection, Laser Hack

## Faking I2C Slave to Hijack Config

- **Attack Type**: Bus Spoofing
- **Target**: I2C Bus
- **Vulnerability**: No authentication on slave device
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Boot with manipulated configs
- **Tools**: Custom I2C slave (Arduino), logic analyzer
- **Scenario**: Attacker places fake I2C slave chip to respond with malicious config during boot.
- **Attack Steps**: Step 1: Identify I2C lines and address of config EEPROM. Step 2: Disconnect real EEPROM or isolate with switch. Step 3: Connect Arduino or fake slave at same address. Step 4: Program Arduino to respond with attacker-chosen values. Step 5: Device boots using malicious config (e.g., debug enabled).
- **Detection**: Conflicting I2C responses
- **Solution**: Secure config with signing
- **Tags**: I2C, Spoofing, Config Hijack

## Exposing Chip Secrets with Heat Variation

- **Attack Type**: Thermal Fault Injection
- **Target**: MCU or Secure Element
- **Vulnerability**: Temp-sensitive behavior
- **MITRE**: T1499.002 (System Shutdown: Thermal)
- **Impact**: Side-channel or bypass
- **Tools**: Heat gun, freeze spray, thermal camera
- **Scenario**: Overheating or cooling a chip can change timing or behavior to bypass security checks.
- **Attack Steps**: Step 1: Identify security function (e.g., password validation). Step 2: Apply extreme heat or cold to chip region. Step 3: Observe timing shifts in UART or power trace. Step 4: Exploit glitch to bypass check or dump RAM. Step 5: Extract altered memory or shell access.
- **Detection**: Device overheating or rebooting
- **Solution**: Heat sensors, shutdown protection
- **Tags**: Thermal Attack, Fault Injection

## Exploiting Weak PUF for Device ID Spoofing

- **Attack Type**: Clone Weak Physically Unclonable Function
- **Target**: MCU with PUF
- **Vulnerability**: Predictable entropy or weak bias
- **MITRE**: T1587.001 (Develop Capabilities)
- **Impact**: Clone device or defeat licensing
- **Tools**: Firmware dumper, PUF emulator
- **Scenario**: Weak entropy in PUF allows predicting chip identity bits.
- **Attack Steps**: Step 1: Dump firmware where PUF-based ID is stored or referenced. Step 2: Analyze code to understand how ID is derived. Step 3: Simulate PUF circuit or match based on bias pattern. Step 4: Clone or spoof device ID in emulator or FPGA.
- **Detection**: Repeated ID collisions
- **Solution**: Use stronger randomness or secure fuses
- **Tags**: PUF, Device ID, Clone

## DMA Attack Using FPGA as Bus Master

- **Attack Type**: Direct Memory Access Exploit
- **Target**: RAM or Bus
- **Vulnerability**: No IOMMU or DMA restriction
- **MITRE**: T1029 (Scheduled Transfer)
- **Impact**: Extract sensitive live memory
- **Tools**: FPGA board (e.g., Nexys), custom DMA logic
- **Scenario**: FPGA acts as bus master to read system RAM without CPU intervention.
- **Attack Steps**: Step 1: Identify memory bus (e.g., AXI, AMBA) on device PCB. Step 2: Connect FPGA lines to bus signals (address, data, control). Step 3: Load custom bitstream on FPGA to perform DMA reads. Step 4: Extract RAM contents while CPU runs normally. Step 5: Analyze for secrets or code injection.
- **Detection**: Timing anomalies or watchdog triggers
- **Solution**: Use IOMMU, block unauthorized DMA
- **Tags**: FPGA, DMA Hack, RAM Read

## Reverse-Engineering Obfuscated Boot ROM

- **Attack Type**: ROM RE
- **Target**: SoC with Boot ROM
- **Vulnerability**: Obfuscated but not encrypted ROM
- **MITRE**: T1036.005 (Masquerading: Match Legitimate Name)
- **Impact**: Gain control over secure boot path
- **Tools**: Logic analyzer, firmware tools
- **Scenario**: ROM contents are not encrypted but hard to trace — attacker dumps and reconstructs boot logic.
- **Attack Steps**: Step 1: Dump flash and monitor ROM behavior via UART/logs. Step 2: Map execution flow via fuzzing or boot traces. Step 3: Rebuild boot logic structure using disassembler. Step 4: Identify hooks for debug or backdoor access. Step 5: Exploit vulnerable logic to load unsigned code.
- **Detection**: Unexpected boot behavior
- **Solution**: ROM encryption, integrity checks
- **Tags**: Bootloader, ROM, RE

## Exploiting Die-Level Test Pads

- **Attack Type**: IC Internal Pad Exploit
- **Target**: ASIC or SoC
- **Vulnerability**: Accessible internal pads
- **MITRE**: T1600.001 (Hardware Additions)
- **Impact**: Access internal state or diagnostics
- **Tools**: Microprobing station, datasheet, oscilloscope
- **Scenario**: Test pads used for wafer testing are left exposed and connected.
- **Attack Steps**: Step 1: Locate internal test pads on chip die or PCB. Step 2: Use datasheet or RE to understand their function. Step 3: Use microprobes to interact with pads. Step 4: Trigger diagnostic or maintenance functions. Step 5: Dump internal states or bypass protections.
- **Detection**: Probe marks or unexpected logs
- **Solution**: Disable pads at packaging or fuse level
- **Tags**: Wafer Pads, Internal Probing

## USB Debug Port Enumeration on SoC

- **Attack Type**: Debug Enumeration
- **Target**: USB Debug Port
- **Vulnerability**: Debug exposed over USB
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Device control or memory access
- **Tools**: USB sniffer (e.g., Wireshark), laptop
- **Scenario**: Many SoCs expose USB debug endpoints (e.g., vendor tools) when connected to PC.
- **Attack Steps**: Step 1: Connect USB port to PC and observe enumeration. Step 2: Use tools like lsusb or USBView to identify vendor debug class. Step 3: If debug mode found, use vendor tool or fuzz endpoint. Step 4: Access logs, memory, or trigger firmware updates.
- **Detection**: USB device ID patterns
- **Solution**: Lock USB debug with eFuses
- **Tags**: USB, Debug Mode, Fuzzing

## Sideband Covert Channel via Power Line Modulation

- **Attack Type**: Sideband Data Exfiltration
- **Target**: Embedded SoC
- **Vulnerability**: Power side-channel not filtered
- **MITRE**: T1002.001 (Data Compressed)
- **Impact**: Leak secrets without network
- **Tools**: Oscilloscope, filter, recording PC
- **Scenario**: Secret data is encoded in power consumption patterns and read externally.
- **Attack Steps**: Step 1: Infect target firmware with covert data encoder. Step 2: Let device run and leak data via power fluctuation. Step 3: Tap VCC line and connect oscilloscope. Step 4: Decode power fluctuation into bits using pattern analysis. Step 5: Reconstruct exfiltrated secret.
- **Detection**: Unusual power ripple
- **Solution**: Use voltage regulators with filters
- **Tags**: Covert Channel, Sideband

## Partial Firmware Update Injection via I2C

- **Attack Type**: Firmware Manipulation
- **Target**: Embedded Device
- **Vulnerability**: No firmware integrity validation
- **MITRE**: T1542 (Pre-OS Boot)
- **Impact**: Persistent backdoor
- **Tools**: I2C sniffer/injector (e.g., Beagle I2C), firmware updater
- **Scenario**: During partial I2C firmware update, attacker injects own code mid-update.
- **Attack Steps**: Step 1: Wait for legitimate I2C firmware update to start. Step 2: Use sniffer to monitor firmware chunks being written. Step 3: Interrupt I2C line with custom injector. Step 4: Replace certain sections with attacker shellcode. Step 5: Let update continue — device runs attacker’s code.
- **Detection**: Firmware mismatch or crash
- **Solution**: Signed firmware and I2C CRC
- **Tags**: Partial Update, Firmware Injection

## Forcing Boot into Test ROM via Pin Float

- **Attack Type**: Boot Configuration Abuse
- **Target**: SoC
- **Vulnerability**: Unsecured boot pin configuration
- **MITRE**: T1542.004 (Abuse Elevation Control Mechanism)
- **Impact**: Unauthorized firmware access
- **Tools**: Jumper wires, datasheet
- **Scenario**: Leaving specific boot configuration pins floating triggers entry into internal test ROM.
- **Attack Steps**: Step 1: Read chip datasheet to identify boot pin functionality. Step 2: Remove pull-up/down resistor from boot config pin. Step 3: Leave pin floating or pull high/low to force entry into test ROM. Step 4: Power on — device enters test/debug interface. Step 5: Use serial terminal to access diagnostics or dump flash.
- **Detection**: Boot mode logs
- **Solution**: Lock boot mode with OTP fuses
- **Tags**: Boot ROM, Debug Bypass

## Bit-Banging I2C to Replay Config

- **Attack Type**: Bus Replay Attack
- **Target**: Config EEPROM
- **Vulnerability**: No validation of I2C source
- **MITRE**: T1071.001 (Application Layer Protocol: Web Protocols)
- **Impact**: Remote reprogramming
- **Tools**: Raspberry Pi / Arduino, GPIO jumper wires
- **Scenario**: Reconstruct I2C traffic manually via GPIO and replay to reprogram a device.
- **Attack Steps**: Step 1: Record working I2C config dump using logic analyzer. Step 2: Extract data packets and addresses. Step 3: Write script on Raspberry Pi to toggle GPIOs mimicking SDA/SCL. Step 4: Replay traffic to target device. Step 5: Modify device config without official tools.
- **Detection**: Unknown write source in logs
- **Solution**: I2C authentication or write lock
- **Tags**: Bit-Banging, I2C Replay

## Reverse EEPROM via UV Light Erasure

- **Attack Type**: EEPROM Erase Attack
- **Target**: EPROM
- **Vulnerability**: UV-sensitive chip with clear casing
- **MITRE**: T1490 (Inhibit System Recovery)
- **Impact**: Firmware wipe or config reset
- **Tools**: UV EPROM eraser or sunlight
- **Scenario**: Some chips (especially older) allow EEPROM to be erased via UV light through quartz window.
- **Attack Steps**: Step 1: Identify EEPROM with UV-erasable window (visible on top). Step 2: Place under UV lamp for 10–20 minutes. Step 3: Verify if data has been erased via programmer. Step 4: Rewrite or read now-unlocked EEPROM. Step 5: Bypass software protection relying on EEPROM values.
- **Detection**: EEPROM empty or corrupted
- **Solution**: Replace with flash; remove UV access
- **Tags**: UV Erasure, EEPROM, Retro Hacking

## JTAG Password Brute Force on Unprotected Interface

- **Attack Type**: Interface Brute Force
- **Target**: SoC / MCU
- **Vulnerability**: Weak JTAG access control
- **MITRE**: T1110.001 (Brute Force: Password Guessing)
- **Impact**: Total device takeover
- **Tools**: JTAG debugger (Segger, OpenOCD), brute-force tool
- **Scenario**: Unlocked JTAG interface uses weak or short password → brute-force is feasible.
- **Attack Steps**: Step 1: Identify JTAG pinout via datasheet. Step 2: Connect debugger to TDI, TDO, TCK, TMS. Step 3: Try brute-force tool to test common JTAG unlock sequences. Step 4: If accepted, gain full memory and register access. Step 5: Dump firmware or write custom code.
- **Detection**: Brute-force logs (if logged)
- **Solution**: Lock JTAG with OTP fuses
- **Tags**: JTAG, Password, Brute

## Exploiting JTAG Lock Flaws in Production Chips

- **Attack Type**: JTAG Lock Bypass
- **Target**: Embedded Chip
- **Vulnerability**: Lock can be overwritten or reset
- **MITRE**: T1600.002 (Hardware Additions)
- **Impact**: JTAG access after production
- **Tools**: Debugger, datasheet
- **Scenario**: Devices incorrectly lock JTAG (e.g., via software only) allowing it to be re-enabled.
- **Attack Steps**: Step 1: Identify lock mechanism (e.g., lock bit in EEPROM). Step 2: Use flash dump or EEPROM tool to change bit. Step 3: Reboot device — JTAG now enabled. Step 4: Connect debugger and access chip. Step 5: Dump memory or modify logic.
- **Detection**: JTAG activity logs
- **Solution**: Use fuse-based JTAG disable
- **Tags**: Lock Flaw, JTAG, EEPROM

## Exploiting Watchdog Timer Reset Behavior

- **Attack Type**: Reset Glitch Exploit
- **Target**: IoT Device
- **Vulnerability**: Debug fallback after reset
- **MITRE**: T1562.004 (Disable or Modify System Firewall)
- **Impact**: Recover access to protected system
- **Tools**: Multimeter, UART cable
- **Scenario**: Devices auto-reboot using watchdog; some reset into debug-safe state if config is corrupt.
- **Attack Steps**: Step 1: Use tool to write invalid config via serial. Step 2: Let watchdog reset system. Step 3: Observe boot logs — check if debug mode activated. Step 4: Use UART shell or default password access. Step 5: Dump flash or change login settings.
- **Detection**: Log analysis post-reset
- **Solution**: Harden watchdog behavior
- **Tags**: Watchdog, Reset Exploit

## Audio Port Used for Data Exfiltration

- **Attack Type**: Audio Side Channel
- **Target**: IoT Device
- **Vulnerability**: Audio output controllable by attacker
- **MITRE**: T1002.002 (Data Encrypted)
- **Impact**: Covert data theft
- **Tools**: Audio recorder, signal decoder (Audacity)
- **Scenario**: Microcontroller encodes data as audio tones through speaker or buzzer.
- **Attack Steps**: Step 1: Trigger attacker code or script. Step 2: Listen to tones produced by speaker output. Step 3: Record signal via phone or mic. Step 4: Analyze tone frequency or pulse to extract binary data. Step 5: Decode into file or password.
- **Detection**: Strange tones, system logs
- **Solution**: Filter audio or limit freq
- **Tags**: Audio Covert Channel, Sound

## Monitoring eMMC Traffic to Recover Deleted Files

- **Attack Type**: Passive Memory Monitoring
- **Target**: Android / Embedded
- **Vulnerability**: No encryption at eMMC interface
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Data recovery or surveillance
- **Tools**: eMMC probe adapter, logic analyzer
- **Scenario**: Tapping eMMC lines to observe internal read/write operations.
- **Attack Steps**: Step 1: Identify eMMC CLK, CMD, DAT0–DAT7 lines. Step 2: Solder wires or use eMMC test point adapter. Step 3: Connect logic analyzer and capture traffic during normal use. Step 4: Extract block addresses of interest. Step 5: Rebuild files or search for deleted artifacts.
- **Detection**: eMMC power/use spikes
- **Solution**: Use hardware encryption or TEE
- **Tags**: eMMC Forensics, Traffic Capture

## UART Interface Dump via Device Disassembly

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Device
- **Vulnerability**: Exposed UART Debug Ports
- **MITRE**: T1040 - Peripheral Device Discovery
- **Impact**: Full device access
- **Tools**: Screwdriver set, Multimeter, USB-to-TTL converter, Serial Terminal (PuTTY)
- **Scenario**: Attacker opens a consumer IoT device to find UART pins and extract boot logs or shell access.
- **Attack Steps**: Step 1: Power off the device completely. Step 2: Use a screwdriver to gently open the device casing. Step 3: Look for small labeled pins on the board marked "TX", "RX", "GND". Step 4: Use a multimeter in continuity mode to confirm pin paths. Step 5: Connect USB-to-TTL wires to the pins: TX to RX, RX to TX, GND to GND. Step 6: Plug the USB into your computer and open PuTTY with baud rate 115200. Step 7: Power the device and watch boot logs or login shell appear.
- **Detection**: Log review for unknown UART activity
- **Solution**: Remove debug headers post-manufacturing
- **Tags**: UART, Reverse Engineering, PuTTY

## Dumping Flash Memory via SPI Pins

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Consumer Electronics (e.g., Router)
- **Vulnerability**: Unprotected SPI Flash
- **MITRE**: T1005 - Data from Local System
- **Impact**: Firmware theft, vulnerability discovery
- **Tools**: Flashrom, SOIC8 clip, CH341A Programmer, Computer
- **Scenario**: By finding SPI flash chip and connecting a reader, attacker can dump firmware and reverse engineer it.
- **Attack Steps**: Step 1: Open device and locate flash chip with 8 legs (usually near the processor). Step 2: Use a magnifier to read chip ID like “25Q64...”. Step 3: Connect SOIC8 clip to the chip legs without powering the device. Step 4: Connect clip wires to CH341A and plug into PC. Step 5: Install and open "Flashrom" software. Step 6: Run Flashrom to detect chip and read memory: flashrom -p ch341a_spi -r backup.bin. Step 7: You now have a binary copy to reverse or analyze.
- **Detection**: Device integrity hash check
- **Solution**: Secure boot + chip encryption
- **Tags**: SPI Flash, Firmware Dump, CH341A

## Debug Access via SWD Port

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Controller
- **Vulnerability**: Unlocked Debug Interface
- **MITRE**: T1602 - Data from Device
- **Impact**: Code/data leakage
- **Tools**: ST-Link debugger, OpenOCD, PC
- **Scenario**: Attacker accesses SWD debug port on a microcontroller to pause execution and extract memory.
- **Attack Steps**: Step 1: Disassemble the device carefully to expose the PCB. Step 2: Identify SWDIO and SWCLK pins (labeled near MCU or on test pads). Step 3: Connect ST-Link debugger to those pins: SWDIO to SWDIO, SWCLK to SWCLK, GND to GND. Step 4: Plug ST-Link to your PC and install OpenOCD. Step 5: Use OpenOCD to connect: openocd -f interface/stlink.cfg -f target/stm32f1x.cfg. Step 6: Dump memory using GDB commands. Step 7: Analyze memory dump for secrets or firmware.
- **Detection**: Electrical signal monitoring
- **Solution**: Lock SWD in firmware post-deployment
- **Tags**: SWD, ST-Link, GDB

## EEPROM Content Dump using I2C Interface

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart Locks, Access Devices
- **Vulnerability**: Unencrypted I2C EEPROM
- **MITRE**: T1005 - Data from Local System
- **Impact**: Credential theft
- **Tools**: I2C Sniffer, Arduino/Bus Pirate, EEPROM reader script
- **Scenario**: EEPROM chip content like credentials can be read by attaching to I2C bus.
- **Attack Steps**: Step 1: Open the device and locate small 8-pin EEPROM marked like “24C02”. Step 2: Connect SDA and SCL lines to Arduino/Bus Pirate. Also connect GND. Step 3: Upload EEPROM dump script or use Bus Pirate I2C mode. Step 4: Read EEPROM content to terminal or dump file. Step 5: Analyze output for stored credentials or secrets.
- **Detection**: Unusual I2C traffic during testing
- **Solution**: Encrypt EEPROM or use secure elements
- **Tags**: I2C, EEPROM, Credential Dump

## JTAG Exploitation via Boundary Scan Access

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Industrial Controller
- **Vulnerability**: Enabled JTAG interface
- **MITRE**: T1518.001 - Hardware Enumeration
- **Impact**: Full device control
- **Tools**: JTAGulator, OpenOCD, PC
- **Scenario**: Attacker identifies and connects to JTAG interface to debug or dump device memory.
- **Attack Steps**: Step 1: Open the target device and expose the circuit board. Step 2: Use a multimeter to identify test points. Step 3: Connect JTAGulator to all test points (up to 24). Step 4: Run JTAGulator to auto-detect JTAG pinout. Step 5: Use OpenOCD with detected pinout to halt CPU and access memory. Step 6: Dump memory or insert breakpoints. Step 7: Analyze for credentials, keys, or modify code.
- **Detection**: Power-on JTAG signal probing
- **Solution**: Fuse or lock JTAG in production
- **Tags**: JTAG, Boundary Scan, OpenOCD

## Exposing Hidden Test Pads with Magnification

- **Attack Type**: Hardware Interface Exploitation
- **Target**: IoT Device
- **Vulnerability**: Unlabeled Debug Pads
- **MITRE**: T0847 - Test Point Discovery
- **Impact**: Access to internal interfaces
- **Tools**: Magnifying lens/microscope, Multimeter
- **Scenario**: Discovering unmarked debug pads using a microscope and continuity testing.
- **Attack Steps**: Step 1: Gently open the device casing to reveal the PCB. Step 2: Use a magnifier to closely inspect tiny golden or silver dots near chip areas. Step 3: Use a multimeter to trace pads connected to main chip. Step 4: Identify functions using known pinout patterns (GND usually connects to ground plane). Step 5: Mark and log the pads for further testing.
- **Detection**: Manual PCB inspection
- **Solution**: Remove or obfuscate test points
- **Tags**: PCB, Debug Pads, Discovery

## SPI Flash Hot-Air Removal for Forensics

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Router, IoT Device
- **Vulnerability**: Physically accessible SPI Flash
- **MITRE**: T1005 - Firmware Extraction
- **Impact**: Secure firmware dumping
- **Tools**: Hot air gun, Flux, Tweezer, CH341A, SOIC adapter
- **Scenario**: Detaching flash chip with hot air gun to extract firmware externally.
- **Attack Steps**: Step 1: Open device and apply flux around the flash chip. Step 2: Use hot air gun at ~250°C to slowly heat the chip. Step 3: Carefully lift the chip with tweezers when solder melts. Step 4: Clean the chip legs and solder to SOIC adapter. Step 5: Connect to CH341A and read using Flashrom.
- **Detection**: Chip absence/absence alerts
- **Solution**: Conformal coating or chip encryption
- **Tags**: Hot Air, Chip Removal

## Reverse Engineering Firmware using Binwalk

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Flash Memory
- **Vulnerability**: No firmware encryption
- **MITRE**: T1005 - Data Extraction
- **Impact**: Access to device logic/data
- **Tools**: Binwalk, Terminal, PC
- **Scenario**: Analyzing dumped firmware with Binwalk to extract file systems and configs.
- **Attack Steps**: Step 1: Take the binary file dumped from SPI chip (e.g., firmware.bin). Step 2: Install binwalk on your computer. Step 3: Run binwalk -e firmware.bin to extract embedded files. Step 4: Review extracted folders for configuration files, login credentials, or file systems. Step 5: Modify and repackage for testing (optional).
- **Detection**: Binary pattern detection
- **Solution**: Enable secure boot and crypto signatures
- **Tags**: Binwalk, Firmware Analysis

## Reading BGA Flash using Socket Adapter

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Game Console, Smart TV
- **Vulnerability**: Unprotected flash, exposed chip
- **MITRE**: T1005 - Memory Dumping
- **Impact**: Extraction of internal secrets
- **Tools**: BGA Socket Programmer, PC
- **Scenario**: Dumping flash from BGA (Ball Grid Array) using socket adapter without soldering.
- **Attack Steps**: Step 1: Open the device and gently remove the BGA flash chip (optional pre-removal step). Step 2: Place the BGA chip into a compatible socket adapter. Step 3: Connect the socket to a flash programmer like Dediprog. Step 4: Use software to read the contents to a .bin file. Step 5: Analyze or reverse the file as needed.
- **Detection**: Secure boot and read protection
- **Solution**: Epoxy/Shielding or encrypted flash
- **Tags**: BGA Flash, Reverse Engineering

## Glitching Boot Sequence with External Clock

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Microcontroller
- **Vulnerability**: Boot timing vulnerability
- **MITRE**: T1495 - Firmware Manipulation
- **Impact**: Device unlock/root access
- **Tools**: Clock glitcher, Arduino, Oscilloscope
- **Scenario**: Interfering with the boot process using a modified clock input to access debug shell.
- **Attack Steps**: Step 1: Identify clock input pin of microcontroller using datasheet. Step 2: Use Arduino or signal generator to send abnormal clock signals. Step 3: Connect power and begin booting while injecting glitch signal. Step 4: Observe using oscilloscope when bootloader behaves unusually. Step 5: When glitch succeeds, you may get root shell or bypass checks.
- **Detection**: Power boot logs with UART
- **Solution**: Harden bootloader against timing attacks
- **Tags**: Clock Glitching, Arduino

## Password Extraction from Unsecured NVRAM

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Routers, Modems
- **Vulnerability**: Stored plaintext creds
- **MITRE**: T1003.004 - Credential Dumping
- **Impact**: Credential leakage
- **Tools**: EEPROM Reader, I2C tools
- **Scenario**: Accessing plaintext passwords from NVRAM chip using i2c/sniffers.
- **Attack Steps**: Step 1: Open the device casing and locate NVRAM chip. Step 2: Identify SDA and SCL pins and connect to I2C reader. Step 3: Use i2cdetect to find address, then dump with i2cdump. Step 4: Review output for plaintext data.
- **Detection**: Memory monitoring
- **Solution**: Encrypt config files
- **Tags**: EEPROM, NVRAM

## Intercepting Serial Console for Root Access

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Embedded Device
- **Vulnerability**: Console left in dev mode
- **MITRE**: T1548.002 - Bypass Auth
- **Impact**: Root access
- **Tools**: USB to Serial Converter, PuTTY
- **Scenario**: Serial console sometimes provides root access with no login due to debug leftover.
- **Attack Steps**: Step 1: Find UART (TX/RX) pins. Step 2: Connect USB converter as done in earlier case. Step 3: Open PuTTY and power on the device. Step 4: Observe console. If prompt appears without login, access is gained.
- **Detection**: Serial console logs
- **Solution**: Disable shell or use password
- **Tags**: UART, Serial, Root

## SPI Bus Sniffing with Logic Analyzer

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart Appliances
- **Vulnerability**: SPI exposed during runtime
- **MITRE**: T1040 - Peripheral Monitoring
- **Impact**: Intercept secret keys or data
- **Tools**: Logic Analyzer (Saleae), PulseView
- **Scenario**: Monitoring SPI traffic live to analyze command structure and extract secrets.
- **Attack Steps**: Step 1: Attach probe clips to SPI lines: MOSI, MISO, CLK, CS. Step 2: Launch PulseView and select proper voltage level. Step 3: Begin recording and trigger on chip select (CS) signal. Step 4: Decode SPI protocol and extract transmitted data.
- **Detection**: Analyze bus at runtime
- **Solution**: Use encrypted protocols
- **Tags**: Logic Analyzer, SPI

## Dumping NAND Flash using TSOP Adapter

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smart TV, DVR
- **Vulnerability**: Exposed NAND without secure erase
- **MITRE**: T1005 - Data Extraction
- **Impact**: Firmware cloning
- **Tools**: TSOP56 Adapter, Flash Programmer
- **Scenario**: Dump large flash content (Linux images, FS) from NAND chips using special adapter.
- **Attack Steps**: Step 1: Desolder NAND chip from PCB (use hot air station carefully). Step 2: Insert chip into TSOP adapter. Step 3: Connect to programmer and dump NAND content. Step 4: Use tools like Binwalk or dd to analyze Linux FS.
- **Detection**: Missing memory wipe at shutdown
- **Solution**: Secure erase + crypto
- **Tags**: NAND, TSOP Adapter

## Reverse Engineering via LED Blinking Debug

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Home Appliances
- **Vulnerability**: Visible debug signals via LED
- **MITRE**: T1120 - Peripheral Behavior
- **Impact**: Leak internal state or errors
- **Tools**: Camera, Slow-Mo Recording, LED Decoder
- **Scenario**: Some devices blink LEDs based on internal events — can be decoded to infer actions.
- **Attack Steps**: Step 1: Record device LED behavior during boot. Step 2: Use slow-motion camera or frame-by-frame to observe blink patterns. Step 3: Match patterns to possible status messages (e.g., error codes). Step 4: Use trial and error to manipulate input (e.g., remove USB) and re-test. Step 5: Map device behavior to blinking feedback.
- **Detection**: Monitor blinking under testing
- **Solution**: Disable debug LED in production
- **Tags**: LED, Visual Debugging

## Finding UART via Oscilloscope Signal Analysis

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Routers, Dev Boards
- **Vulnerability**: No label on debug pads
- **MITRE**: T0847 - Test Point Discovery
- **Impact**: Enables further exploitation
- **Tools**: Oscilloscope, Test Probes
- **Scenario**: Using an oscilloscope to find which test pad is TX by spotting boot signal spikes.
- **Attack Steps**: Step 1: Open device and identify a group of small test pads. Step 2: Connect oscilloscope ground to device ground. Step 3: Touch each pad with probe while powering on. Step 4: Observe waveform; the one with repeating square spikes is likely UART TX. Step 5: Connect serial adapter and verify with terminal.
- **Detection**: Unusual electrical probing
- **Solution**: Obfuscate test points or remove pads
- **Tags**: Oscilloscope, UART Discovery

## IC Identification via Logo and Package Decoding

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Any PCB
- **Vulnerability**: Unknown components
- **MITRE**: T1592 - Gather Device Info
- **Impact**: Enables custom exploitation paths
- **Tools**: Magnifier, Google, IC Databases
- **Scenario**: Identifying unknown ICs using their printed codes and online databases.
- **Attack Steps**: Step 1: Use magnifier to read part numbers and manufacturer logos on chips. Step 2: Search datasheets online using part number (e.g., “W25Q64 datasheet”). Step 3: Confirm pinout and voltage ratings. Step 4: Use this info to plan safe probing or dump methods.
- **Detection**: Bill of Materials mismatch
- **Solution**: Use obfuscation or epoxy resin
- **Tags**: IC Markings, Datasheet Recon

## Bootloader Mode Activation via GPIO Trigger

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Dev Boards, IoT Chips
- **Vulnerability**: Unprotected bootloader trigger
- **MITRE**: T1602.002 - Boot Mode Bypass
- **Impact**: Allows firmware flashing or unlock
- **Tools**: Jumper Wires, USB Serial
- **Scenario**: Using a jumper wire on GPIO pin to force the device into debug/bootloader mode.
- **Attack Steps**: Step 1: Find datasheet of the main chip to identify BOOT or GPIO pins. Step 2: Locate the pin on the PCB. Step 3: Hold the pin LOW or HIGH using jumper wire and GND (depending on datasheet). Step 4: Power the device while holding jumper in place. Step 5: Device enters bootloader (e.g., ST boot, ESP flash mode).
- **Detection**: Detects on power boot
- **Solution**: Disable bootloader in production
- **Tags**: GPIO Trigger, Boot Unlock

## Analyzing eMMC Chip for Data Partitioning

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Android Devices, DVRs
- **Vulnerability**: Exposed eMMC
- **MITRE**: T1005 - Full Disk Dump
- **Impact**: Data extraction from device
- **Tools**: eMMC Reader, Adapter Board
- **Scenario**: Removing and dumping eMMC memory to analyze Android or Linux partitions.
- **Attack Steps**: Step 1: Desolder eMMC chip using hot air. Step 2: Clean pins and insert into BGA adapter. Step 3: Connect to eMMC reader and dump full image. Step 4: Use fdisk or parted to inspect partition layout. Step 5: Mount partitions and extract user data or configs.
- **Detection**: Unusual BGA desoldering
- **Solution**: Full disk encryption
- **Tags**: eMMC, Partitioning, Recovery

## Logic-Level Shifting to Match Interface Voltages

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Smartphones, Sensors
- **Vulnerability**: Voltage mismatch risks
- **MITRE**: T1207 - Interface Probing
- **Impact**: Prevents damage during probing
- **Tools**: Logic Level Shifter, USB TTL, Jumper Wires
- **Scenario**: Using logic level converter to safely read signals from 1.8V or 2.5V devices.
- **Attack Steps**: Step 1: Identify signal voltage using datasheet or multimeter. Step 2: Use logic level shifter between 3.3V/5V USB-TTL and target pins. Step 3: Connect TX/RX/GND through level shifter. Step 4: Open terminal and safely interact without damaging device.
- **Detection**: Signal strength logs
- **Solution**: Design with voltage tolerance
- **Tags**: Logic Level, Safe Debugging

## Exploiting Test Backdoors via AT Commands

- **Attack Type**: Hardware Interface Exploitation
- **Target**: GSM Modems, Smart Modules
- **Vulnerability**: Legacy debug command support
- **MITRE**: T1552.001 - Command Injection
- **Impact**: Configuration access or root
- **Tools**: USB to UART, Terminal
- **Scenario**: Sending undocumented AT commands over serial to activate debug features.
- **Attack Steps**: Step 1: Connect to serial UART as usual. Step 2: Type AT and press Enter to check if it responds. Step 3: Try extended commands like AT+DEBUG, AT+TESTMODE=1. Step 4: If accepted, may reveal extra menus or system internals.
- **Detection**: Monitor for AT traffic
- **Solution**: Remove debug command handlers
- **Tags**: AT Commands, UART Exploit

## Board Layer Mapping using Light and Camera

- **Attack Type**: Hardware Interface Exploitation
- **Target**: Multi-layer Boards
- **Vulnerability**: Visible trace leakage
- **MITRE**: T1592.003 - PCB Mapping
- **Impact**: Aids in reverse engineering
- **Tools**: Bright Flashlight, Smartphone, Photo Editor
- **Scenario**: Mapping PCB traces using backlight and camera to reveal internal routing.
- **Attack Steps**: Step 1: Hold the PCB against a strong flashlight. Step 2: Take high-resolution photo from opposite side. Step 3: Enhance contrast in editing software to make internal copper traces visible. Step 4: Use trace info to identify signal paths and test points.
- **Detection**: Optical detection alerts
- **Solution**: Use opaque boards or ground fill
- **Tags**: PCB Reverse, Trace Mapping

## Live Debug Hook via Test Clip without Soldering

- **Attack Type**: Hardware Interface Exploitation
- **Target**: EEPROMs, Flash Chips
- **Vulnerability**: Physical access without resistance
- **MITRE**: T1005 - EEPROM Access
- **Impact**: Silent, fast data access
- **Tools**: SOIC Test Clip, USB Programmer
- **Scenario**: Using hook/test clips to connect to IC pins without removing device or soldering.
- **Attack Steps**: Step 1: Open casing and locate chip (e.g., 8-pin EEPROM). Step 2: Carefully attach SOIC clip onto chip without bending pins. Step 3: Connect clip leads to programmer. Step 4: Use software like Flashrom to interact with chip directly. Step 5: Can be used to modify or dump contents.
- **Detection**: No logs, no soldering signs
- **Solution**: Secure ICs or potting
- **Tags**: Clip-on, Live Dump

## SIM Card Swapping via Physical Theft

- **Attack Type**: SIM Swap
- **Target**: Mobile Phone
- **Vulnerability**: Unsecured SIM access
- **MITRE**: T1585.002
- **Impact**: Account takeover, SMS interception
- **Tools**: SIM ejector tool, another phone
- **Scenario**: Attacker steals the mobile phone, replaces the SIM with a new one in another phone to take control of messages and OTPs.
- **Attack Steps**: Step 1: Identify a target whose SIM activity you want to hijack.Step 2: Physically steal or borrow their phone temporarily.Step 3: Use a SIM ejector tool (or a pin) to remove the SIM card.Step 4: Insert the SIM into your own phone.Step 5: Wait for OTPs or messages for bank/2FA to arrive.Step 6: Use this to reset passwords or take over accounts.
- **Detection**: Sudden SIM disconnect alerts, login anomaly detection
- **Solution**: Use SIM PIN lock, enable eSIM, 2FA apps
- **Tags**: sim swap, sms, mobile theft

## Physical Installation of Keylogger App via USB

- **Attack Type**: USB-Based Malware Injection
- **Target**: Android Smartphone
- **Vulnerability**: USB Debugging Enabled
- **MITRE**: T1476
- **Impact**: Credential theft, privacy breach
- **Tools**: USB cable, Laptop with ADB (Android Debug Bridge)
- **Scenario**: Attacker physically connects mobile device to a laptop and installs a keylogger app to record inputs.
- **Attack Steps**: Step 1: Gain temporary access to the mobile phone.Step 2: Connect it to your laptop using a USB cable.Step 3: Enable developer mode on the phone (search “About Phone” → tap “Build Number” 7 times).Step 4: Enable “USB Debugging” in developer settings.Step 5: Use ADB commands on your laptop to install a keylogger APK.Step 6: The app silently records inputs and uploads them to an attacker server or stores locally.
- **Detection**: Unusual background app activity, battery drain
- **Solution**: Disable USB debugging, app whitelisting
- **Tags**: keylogger, usb injection

## Rogue Charging Station Data Theft (Juice Jacking)

- **Attack Type**: Juice Jacking
- **Target**: Mobile Devices
- **Vulnerability**: USB data lines active by default
- **MITRE**: T0842
- **Impact**: Data theft, spyware installation
- **Tools**: Rogue charging station, malware payload
- **Scenario**: Public charging port used to steal phone data or install malware via USB cable.
- **Attack Steps**: Step 1: Set up a public-looking charging kiosk with hidden data connection hardware.Step 2: Place it in a public place (café, airport) where people may plug in their phones.Step 3: When someone plugs their phone, the rogue device silently accesses data or installs malware.Step 4: Extract data such as contacts, messages, or photos remotely or when device is connected.Step 5: Disconnect after a few minutes to avoid suspicion.
- **Detection**: Phone alert, suspicious USB access prompt
- **Solution**: Use USB data blockers, charge-only cables
- **Tags**: juice jacking, rogue charging

## Bluetooth Sniffing via Close Proximity Device

- **Attack Type**: Bluetooth Eavesdropping
- **Target**: Bluetooth-enabled phones
- **Vulnerability**: Insecure Bluetooth protocol
- **MITRE**: T1420
- **Impact**: Privacy breach, profiling
- **Tools**: Ubertooth One, Laptop
- **Scenario**: Attacker uses Bluetooth sniffer to intercept unencrypted Bluetooth traffic in public.
- **Attack Steps**: Step 1: Buy or borrow a Bluetooth sniffer (e.g., Ubertooth One).Step 2: Install required software like Wireshark with Bluetooth plugins.Step 3: Go to a public area like a coffee shop.Step 4: Power on the device and set it to scanning mode.Step 5: Capture broadcast data or unencrypted Bluetooth connections (such as file transfers or pairing info).Step 6: Analyze the packets to reconstruct messages or device behavior.
- **Detection**: Packet inspection tools, anomaly logs
- **Solution**: Turn off Bluetooth, avoid unknown pairing
- **Tags**: bluetooth sniffing, wireless leak

## SIM Cloning using SIM Reader Hardware

- **Attack Type**: SIM Card Duplication
- **Target**: SIM Card
- **Vulnerability**: Unencrypted SIM data
- **MITRE**: T1417
- **Impact**: Identity theft, account hijack
- **Tools**: SIM reader/writer, SIM cloning software
- **Scenario**: Attacker accesses and clones SIM card using a physical SIM reader/writer.
- **Attack Steps**: Step 1: Acquire a SIM card reader/writer (easily available online).Step 2: Borrow or steal the victim's SIM card for a short time (a few minutes).Step 3: Insert the SIM into the reader and run SIM cloning software on a laptop.Step 4: Extract the IMSI and authentication key (Ki) from the SIM.Step 5: Program a blank SIM card with the same credentials.Step 6: Use the cloned SIM in another phone to receive calls, SMS, and data meant for the victim.
- **Detection**: SIM activity monitoring, multiple device detection
- **Solution**: Modern SIMs with encryption, eSIM use
- **Tags**: sim clone, identity theft

## NFC Spoofing via Custom Tag Injection

- **Attack Type**: NFC Tag Spoofing
- **Target**: NFC-enabled smartphones
- **Vulnerability**: Lack of NFC prompt/validation
- **MITRE**: T1477
- **Impact**: Credential theft, device compromise
- **Tools**: Blank NFC tags, NFC writer app
- **Scenario**: Attacker creates a fake NFC tag that mimics a real payment or login tag to redirect users.
- **Attack Steps**: Step 1: Buy blank NFC tags and install any free NFC writer app.Step 2: Program the tag with a malicious URL or fake payment info.Step 3: Stick the tag near real NFC-enabled terminals (e.g., contactless payment, login gates).Step 4: When user taps phone, they are redirected or data is logged.Step 5: If it's a malicious login page, steal credentials or trick into downloading malware.
- **Detection**: URL redirection detection
- **Solution**: Disable NFC or confirm URLs before tapping
- **Tags**: NFC spoofing, social engineering

## Wi-Fi Pineapple Attack at Cafés

- **Attack Type**: Rogue Wi-Fi Hotspot
- **Target**: Mobile phones, laptops
- **Vulnerability**: Auto-connect to known SSIDs
- **MITRE**: T1557.001
- **Impact**: Traffic interception, data theft
- **Tools**: Wi-Fi Pineapple device, Laptop
- **Scenario**: Attacker sets up a fake Wi-Fi AP to intercept user data.
- **Attack Steps**: Step 1: Buy a Wi-Fi Pineapple or use a laptop with special software.Step 2: Set up an open Wi-Fi network named similarly to nearby trusted networks.Step 3: Place the device in a public place (e.g., café, airport).Step 4: Users auto-connect thinking it's the real Wi-Fi.Step 5: Intercept their traffic, capture login credentials, session cookies.Step 6: Use data to hijack sessions or collect private information.
- **Detection**: DNS spoof detection tools, Wi-Fi anomalies
- **Solution**: Disable auto-connect, use VPN
- **Tags**: rogue wifi, man in the middle

## Mobile Sensor Abuse via Physical Access

- **Attack Type**: Motion Sensor Hijack
- **Target**: Android Phones
- **Vulnerability**: Sensor data not protected
- **MITRE**: T1512
- **Impact**: PIN leakage, behavior profiling
- **Tools**: Android smartphone, custom app
- **Scenario**: Attacker installs an app that abuses motion/light sensors to infer PINs or keystrokes.
- **Attack Steps**: Step 1: Gain brief access to the target's phone (e.g., during charging or lending situation).Step 2: Install a seemingly harmless app (e.g., flashlight, wallpaper) from an APK file.Step 3: The app silently logs accelerometer, gyroscope data while user types.Step 4: Analyze patterns to infer typed PINs or behavior.Step 5: Send the data back to attacker for analysis.
- **Detection**: Anomalous battery drain or sensor use
- **Solution**: Sensor permission control
- **Tags**: motion tracking, pin leak

## SIM Card Trap via Mobile Device Distraction

- **Attack Type**: SIM Swap via Distraction
- **Target**: Mobile Phones
- **Vulnerability**: Physical SIM access
- **MITRE**: T1586
- **Impact**: SIM hijacking, data theft
- **Tools**: Fake phone, duplicate SIM tray
- **Scenario**: Attacker distracts target in public, swaps SIM with a duplicate.
- **Attack Steps**: Step 1: Approach the victim under the pretense of needing help with their phone.Step 2: Hand over a phone (with pre-loosened tray) and ask for a SIM check or help.Step 3: While target checks your phone, quickly eject their phone’s SIM.Step 4: Insert a fake SIM back into their phone so they don't realize.Step 5: Leave with the original SIM and use it to intercept OTPs or login codes.
- **Detection**: SIM disconnection alerts
- **Solution**: Use eSIM or SIM tray lock
- **Tags**: social trick, SIM switch

## Over-the-Air (OTA) Update Spoofing via Physical Debug Cable

- **Attack Type**: Fake Firmware Injection
- **Target**: Android Devices
- **Vulnerability**: No firmware signature validation
- **MITRE**: T1601.002
- **Impact**: Total device compromise
- **Tools**: USB debug cable, ADB tool
- **Scenario**: Attacker injects fake firmware using debug cable on rooted phone.
- **Attack Steps**: Step 1: Gain physical access to a rooted Android phone or enable root access.Step 2: Connect the device via USB cable to a laptop with ADB tool.Step 3: Push a fake firmware update (.zip or .img) to the device.Step 4: Use recovery mode or fastboot commands to flash the firmware.Step 5: Reboot phone — it now runs compromised OS that can send data or log activities.
- **Detection**: Secure boot failure, signature check
- **Solution**: Use locked bootloaders, verified boot
- **Tags**: OTA spoof, rooted attack

## Wireless Mouse/Keyboard Dongle Injection

- **Attack Type**: HID Injection Attack
- **Target**: Phones/tablets with OTG
- **Vulnerability**: Unlocked OTG input
- **MITRE**: T1056.001
- **Impact**: Silent data theft, malware download
- **Tools**: USB Rubber Ducky, wireless dongle
- **Scenario**: Attacker connects a rogue USB dongle pretending to be a keyboard to send malicious commands.
- **Attack Steps**: Step 1: Borrow the victim's mobile/tablet with USB-OTG enabled.Step 2: Connect a USB Rubber Ducky or malicious HID device via USB OTG.Step 3: The device is recognized as a keyboard.Step 4: It types pre-programmed commands silently, e.g., opening browser, downloading malware.Step 5: Disconnect and leave no trace.
- **Detection**: App permission logs, command audit
- **Solution**: Disable OTG or use OTG whitelisting
- **Tags**: HID, OTG injection

## SIM Toolkit (STK) Abuse via Pre-loaded Card

- **Attack Type**: SIM Toolkit Attack
- **Target**: Phones with SIM Toolkit support
- **Vulnerability**: Unrestricted STK permissions
- **MITRE**: T1422
- **Impact**: Financial loss, surveillance
- **Tools**: STK-capable SIM, SIM loader
- **Scenario**: Attacker supplies a malicious SIM that can run commands via STK.
- **Attack Steps**: Step 1: Attacker creates a malicious SIM with STK scripts (can send SMS, access contacts).Step 2: Replace user’s SIM card temporarily (e.g., in shared phone scenarios).Step 3: The STK executes commands silently — sends SMS, access GPS or calls premium numbers.Step 4: Revert to original SIM unnoticed.Step 5: Attacker receives data or profit from premium SMS.
- **Detection**: Bill anomalies, STK alerts
- **Solution**: Use SIMs from trusted sources
- **Tags**: SIM Toolkit, premium scam

## Smartphone Battery Swap to Implant Tracker

- **Attack Type**: Battery-Based Implant
- **Target**: Phones with removable battery
- **Vulnerability**: No battery integrity checks
- **MITRE**: T1470
- **Impact**: Location tracking, surveillance
- **Tools**: Modified battery with chip
- **Scenario**: Attacker replaces a phone battery with modified one containing GPS/GSM tracker.
- **Attack Steps**: Step 1: Obtain a modified battery with GPS/GSM tracker hidden inside.Step 2: Access victim’s phone during charging or unattended time.Step 3: Replace the original battery with the modified one.Step 4: Tracker starts sending GPS location or audio logs silently.Step 5: Attacker monitors location remotely.
- **Detection**: Unusual battery size or heating
- **Solution**: Use sealed phones or inspect repairs
- **Tags**: gps tracker, implant

## Physical Backdoor via USB-C Expansion Port

- **Attack Type**: Port-Based Backdoor Implant
- **Target**: Phones/Tablets/Laptops
- **Vulnerability**: Trusted peripheral assumption
- **MITRE**: T1203
- **Impact**: Long-term data exfiltration
- **Tools**: USB-C hub with chip implant
- **Scenario**: Attacker hides a spy chip inside USB-C expander or dongle used by victim.
- **Attack Steps**: Step 1: Purchase or modify a USB-C dongle/hub with a spy chip (like keystroke logger or sniffer).Step 2: Gift or lend it to target claiming it’s a multi-functional charger.Step 3: When victim uses it, chip records inputs, screen data or taps network.Step 4: Data is stored or transmitted when attacker regains access.Step 5: Victim unknowingly uses compromised device daily.
- **Detection**: Forensic hardware check
- **Solution**: Buy accessories only from trusted brands
- **Tags**: usb implant, covert access

## Physical Cloning of eSIM Profile using QR Code

- **Attack Type**: eSIM Hijack
- **Target**: Phones with eSIM
- **Vulnerability**: eSIM QR code exposure
- **MITRE**: T1585.001
- **Impact**: SIM duplication, SMS hijack
- **Tools**: Phone camera, printed QR
- **Scenario**: Attacker clones eSIM profile by accessing victim’s setup QR code.
- **Attack Steps**: Step 1: Victim receives an eSIM setup QR code via email or paper.Step 2: Attacker takes a quick photo or scans the QR code.Step 3: Using a second phone, attacker adds the same eSIM profile.Step 4: Now both phones can receive calls/SMS intended for victim.Step 5: Use for intercepting OTPs, hijack accounts.
- **Detection**: Device login anomaly
- **Solution**: Secure QR delivery or delete after use
- **Tags**: esim, qr attack

## Public Docking Station with Keylogger Function

- **Attack Type**: Dock-Based Keylogging
- **Target**: Smartphones
- **Vulnerability**: Untrusted charging docks
- **MITRE**: T1056.001
- **Impact**: PIN theft, pattern leak
- **Tools**: Malicious phone dock, microcontroller
- **Scenario**: Attacker plants a malicious docking station in public places to log keyboard inputs.
- **Attack Steps**: Step 1: Modify a public charging dock or make your own with internal keylogger chip.Step 2: Leave it in coworking space, airport, or cafe.Step 3: Victim connects phone, thinking it's just a charger.Step 4: The dock records touch gestures, unlock patterns, or keystrokes (on-screen typing).Step 5: Retrieve dock later and extract logs from memory chip.
- **Detection**: Unusual dock behavior, unexpected permissions
- **Solution**: Use personal chargers, block data lines
- **Tags**: keylogger dock, mobile

## SDR-Based Mobile Call Interception (Fake BTS)

- **Attack Type**: IMSI Catching / Fake BTS
- **Target**: Mobile Phones (2G/3G)
- **Vulnerability**: Weak cellular encryption
- **MITRE**: T1430
- **Impact**: Call tapping, location tracking
- **Tools**: RTL-SDR, OpenBTS, laptop
- **Scenario**: Attacker creates a fake base station using SDR to capture mobile call data.
- **Attack Steps**: Step 1: Set up a laptop with OpenBTS or YateBTS software.Step 2: Connect an SDR (Software Defined Radio) device.Step 3: Configure it to mimic a local telecom tower.Step 4: Wait as phones in the vicinity connect to your fake tower.Step 5: Intercept metadata, messages or calls, especially if encryption is weak.Step 6: Use filters to target specific numbers.
- **Detection**: Sudden drop to 2G, IMSI detection apps
- **Solution**: Use LTE-only mode, IMSI catcher detection
- **Tags**: fake BTS, SDR, telecom exploit

## Mobile Speaker Port Audio Tapping

- **Attack Type**: Passive Audio Surveillance
- **Target**: Smartphones
- **Vulnerability**: No audio protection on speaker
- **MITRE**: T1429
- **Impact**: Audio data leak, espionage
- **Tools**: Mini directional mic, audio recorder
- **Scenario**: Spy device placed near mobile speaker captures audio passively.
- **Attack Steps**: Step 1: Sit near the victim’s workspace or place hidden mic near their phone.Step 2: Wait for them to receive or make calls using speaker mode.Step 3: Record the conversation using mic connected to audio recorder.Step 4: Later, filter and analyze audio to extract useful information.Step 5: Use transcription software if needed.
- **Detection**: Noise detection, mic sweeps
- **Solution**: Avoid speaker mode, shielded workspace
- **Tags**: spy mic, audio leak

## Overheating Mobile via Malicious Fast Charger

- **Attack Type**: Charger Overload Attack
- **Target**: Any USB-C/Lightning Phone
- **Vulnerability**: Lack of voltage regulation check
- **MITRE**: T1495
- **Impact**: Hardware damage, denial of service
- **Tools**: Modified fast charger, soldering tools
- **Scenario**: Charger with modified output overheats and damages phone or causes DoS.
- **Attack Steps**: Step 1: Open a standard fast charger and tamper with output regulation.Step 2: Slightly increase voltage/amperage to dangerous levels.Step 3: Replace the victim’s charger or leave it in a shared space.Step 4: When victim plugs in, the phone overheats or battery swells.Step 5: In worst case, internal components may fail.
- **Detection**: Thermal logs, unexpected heat
- **Solution**: Use certified chargers only
- **Tags**: charger attack, overload

## Charging Cable with Hidden Memory Logger

- **Attack Type**: Cable-Based Keylogger
- **Target**: Phones/Tablets
- **Vulnerability**: Cable trust issue
- **MITRE**: T1056.001
- **Impact**: Full compromise, persistent access
- **Tools**: O.MG Cable or clone, Laptop
- **Scenario**: USB cable looks normal but contains chip that logs and stores input data.
- **Attack Steps**: Step 1: Replace target’s charging cable with an O.MG cable (malicious USB).Step 2: The cable functions normally (charges and transfers).Step 3: While connected, it logs keypresses, URLs, or opens hidden backdoors.Step 4: Data is stored or sent via Wi-Fi module inside the cable.Step 5: Attacker retrieves info later or connects remotely.
- **Detection**: Unusual traffic or overheating
- **Solution**: Buy cables from trusted sources
- **Tags**: OMG cable, usb hack

## Tampered Wireless Charger with RF Sniffer

- **Attack Type**: Wireless Sniffing Implant
- **Target**: Qi-enabled phones
- **Vulnerability**: EM leakage
- **MITRE**: T1592
- **Impact**: Side-channel info leak
- **Tools**: Qi pad with RF board
- **Scenario**: Wireless charging pad modified to sniff electromagnetic signals.
- **Attack Steps**: Step 1: Modify a wireless charging pad by adding a radio frequency (RF) sniffer.Step 2: Leave the charger in a public spot or gift it.Step 3: When the phone is placed, RF activity around screen or CPU is analyzed.Step 4: Some side-channel info like PIN attempts, screen unlock time captured.Step 5: Store or stream data to attacker.
- **Detection**: EM inspection gear
- **Solution**: Use own wireless chargers
- **Tags**: RF attack, wireless hack

## Mobile Battery Charger with GSM Spy

- **Attack Type**: Covert GSM Spy Device
- **Target**: Phones using power banks
- **Vulnerability**: Mic inside external hardware
- **MITRE**: T1429
- **Impact**: Audio surveillance, stalking
- **Tools**: Modified power bank with mic + SIM
- **Scenario**: Attacker gives a power bank that doubles as GSM eavesdropper.
- **Attack Steps**: Step 1: Build or buy a modified power bank with built-in GSM module and mic.Step 2: Gift or lend it to the victim.Step 3: When victim charges phone, power bank also powers up GSM mic.Step 4: Attacker can call the SIM inside and hear surroundings.Step 5: Battery silently recharges phone while spying.
- **Detection**: GSM call logs, RF scan
- **Solution**: Avoid third-party power banks
- **Tags**: powerbank mic, gsm spy

## Physically Injecting Malicious QR Code Sticker

- **Attack Type**: QR Code Phishing
- **Target**: Any QR-scanning phone
- **Vulnerability**: No QR verification
- **MITRE**: T1566.002
- **Impact**: Phishing, financial theft
- **Tools**: Printed QR code, glue
- **Scenario**: QR sticker with malicious link is placed over legitimate QR on poster.
- **Attack Steps**: Step 1: Create a phishing site that looks like a login or payment page.Step 2: Generate a QR code for the site using any QR generator.Step 3: Print and stick it over real QR codes on posters (e.g., pay signs, menu scans).Step 4: Victim scans the fake QR and enters sensitive data.Step 5: Attacker collects credentials or payments.
- **Detection**: URL check, domain alerts
- **Solution**: Scan QR only from trusted sources
- **Tags**: qr phishing, visual tampering

## Smartphone Bricking via Malicious Charging Pad

- **Attack Type**: Induced Device Failure
- **Target**: Wireless-charging phones
- **Vulnerability**: No voltage filter in Qi pads
- **MITRE**: T1495
- **Impact**: Denial of service, data loss
- **Tools**: Modified Qi charger
- **Scenario**: Attacker modifies a wireless charger to fry circuits via power spikes.
- **Attack Steps**: Step 1: Buy a Qi wireless charger.Step 2: Open it and rewire it to push unstable voltage or pulses.Step 3: Place it in a public charging area or gift it.Step 4: When victim charges phone, the unstable voltage causes overheating and damages internal chips.Step 5: Phone may fail to boot or become completely unresponsive.
- **Detection**: Sudden shutdown or boot loop
- **Solution**: Use certified chargers, test pads
- **Tags**: qi attack, hardware kill

## Malicious Smartwatch as Bluetooth Backdoor

- **Attack Type**: Wearable Device Backdoor
- **Target**: Smartphones
- **Vulnerability**: Trusted Bluetooth pairing
- **MITRE**: T1426
- **Impact**: Private data leak
- **Tools**: Infected smartwatch
- **Scenario**: Smartwatch paired to victim’s phone used to monitor notifications and audio.
- **Attack Steps**: Step 1: Give victim a smartwatch (gift, trial, or shared use).Step 2: Pair it to their phone via Bluetooth.Step 3: Install malware app on watch that forwards notifications, call audio, or GPS.Step 4: Data is sent to attacker’s server.Step 5: Victim assumes it's a normal fitness device.
- **Detection**: Unrecognized watch activity
- **Solution**: Review paired devices often
- **Tags**: wearable backdoor, bt spy

## Fake Power Button Implant

- **Attack Type**: Button-Level Hardware Attack
- **Target**: Smartphones
- **Vulnerability**: Hardware integrity unverified
- **MITRE**: T1608.001
- **Impact**: Behavior profiling, unlock tracking
- **Tools**: Modified button module
- **Scenario**: Modified power button with data tap placed during repair logs interactions.
- **Attack Steps**: Step 1: Replace victim’s power button with a tampered one (e.g., during screen repair).Step 2: The button has microtap circuit that logs interaction patterns or voltage spikes.Step 3: These logs can reveal usage behavior or timing.Step 4: Attacker retrieves logs later.Step 5: Can be used to deduce unlock attempts.
- **Detection**: Inconsistent tactile response
- **Solution**: Use trusted repair vendors
- **Tags**: button implant, tap logger

## Covert Thermal Camera PIN Detection

- **Attack Type**: PIN Inference via Heat
- **Target**: Any touchscreen phone
- **Vulnerability**: Heat residue on glass
- **MITRE**: T1110
- **Impact**: PIN/code recovery
- **Tools**: FLIR thermal cam
- **Scenario**: Use of thermal camera to detect screen heat traces from recent PIN entry.
- **Attack Steps**: Step 1: Wait until victim unlocks phone in public.Step 2: Within a few seconds, point thermal camera at screen.Step 3: Finger heat residues reveal order of touch points.Step 4: Replay pattern or guess PIN using thermal image.Step 5: Attempt brute-force PIN from inferred pattern.
- **Detection**: Infrared footage, screen clean
- **Solution**: Use gesture unlock or fingerprint
- **Tags**: thermal pin hack, heatmap

## NFC-Enabled Business Card Exploit

- **Attack Type**: Auto-Execute NFC Payload
- **Target**: NFC phones
- **Vulnerability**: Auto-NFC trigger without confirmation
- **MITRE**: T1204.001
- **Impact**: Phishing, malware download
- **Tools**: NFC tag, business card
- **Scenario**: Business card contains NFC chip to auto-open phishing page.
- **Attack Steps**: Step 1: Embed programmable NFC chip inside business card.Step 2: Set URL to phishing site or fake app page.Step 3: Hand it to target during networking.Step 4: As soon as phone touches the card, page auto-opens.Step 5: Victim may enter credentials thinking it's legit.
- **Detection**: NFC logging or popup analysis
- **Solution**: Disable auto-NFC launch
- **Tags**: nfc phishing, social exploit

## Silent Bluetooth Pairing via Device Cloning

- **Attack Type**: Clone-and-Pair Attack
- **Target**: Smartphones
- **Vulnerability**: Weak pairing verification
- **MITRE**: T1421
- **Impact**: Audio capture, device control
- **Tools**: Laptop with Bluetooth MAC spoofing tool
- **Scenario**: Attacker clones MAC of a paired Bluetooth device to hijack pairing.
- **Attack Steps**: Step 1: Identify MAC address of victim’s paired headset/speaker.Step 2: Use a tool to spoof MAC on attacker device.Step 3: Power off victim’s original device briefly (e.g., distract them to switch it off).Step 4: Attacker’s device now receives connection from the phone.Step 5: Capture audio or inject commands.
- **Detection**: Device name/MAC conflicts
- **Solution**: Use verified, encrypted pairing
- **Tags**: bt spoof, MAC clone

## Physical SIM Reprogramming via SIM Jack

- **Attack Type**: SIM File Rewrite
- **Target**: SIM-enabled phones
- **Vulnerability**: Editable SIM file system
- **MITRE**: T1422
- **Impact**: Surveillance, data leak
- **Tools**: SIM Jack tool, PC
- **Scenario**: Attacker modifies SIM apps to silently send SMS/data.
- **Attack Steps**: Step 1: Obtain victim SIM temporarily (1–2 mins).Step 2: Connect SIM to SIM Jack reader.Step 3: Modify SIM Toolkit files to auto-send SMS with location/data.Step 4: Reinsert SIM in victim’s phone.Step 5: SIM now acts as covert info exfil tool.
- **Detection**: SMS logs, unknown messages
- **Solution**: Use secure SIMs, operator lock
- **Tags**: sim edit, stk inject

## Mobile Flashlight as Covert Audio Recorder

- **Attack Type**: App-Level Spyware via Flashlight
- **Target**: Android Smartphones
- **Vulnerability**: No mic permission prompts (pre-Android 10)
- **MITRE**: T1412
- **Impact**: Audio surveillance, data theft
- **Tools**: Infected flashlight APK
- **Scenario**: Attacker installs flashlight app that secretly records audio.
- **Attack Steps**: Step 1: Download a flashlight APK with hidden audio recording functionality.Step 2: Gain brief access to victim’s phone.Step 3: Install the APK and hide it from the home screen.Step 4: App runs in background, silently recording mic audio.Step 5: Files are sent to attacker's cloud or stored locally for later retrieval.
- **Detection**: Background activity logs
- **Solution**: Avoid side-loaded APKs
- **Tags**: spyware app, audio bug

## MicroSD Card with Pre-Loaded Malware

- **Attack Type**: Storage-Based Infection
- **Target**: Phones with microSD slot
- **Vulnerability**: File auto-access or poor permission checks
- **MITRE**: T1204.002
- **Impact**: App hijack, data leak
- **Tools**: Infected microSD, payload APK
- **Scenario**: Malicious SD card inserted into phone auto-executes malware.
- **Attack Steps**: Step 1: Prepare a microSD card and preload it with malicious APKs or scripts.Step 2: Insert into the victim’s smartphone or gift it in a device.Step 3: User accesses card, accidentally opens malware-laced files.Step 4: Malware installs silently or after user grant.Step 5: It sends data back to attacker or opens remote access.
- **Detection**: Unusual files or hidden folders
- **Solution**: Avoid untrusted SD cards
- **Tags**: sd card attack, file injection

## Physically Attached GSM Skimmer in Case

- **Attack Type**: Phone Case Exploit
- **Target**: Any mobile phone
- **Vulnerability**: Trusted external accessories
- **MITRE**: T1429
- **Impact**: Covert eavesdropping
- **Tools**: Modified phone case, SIM card, mic
- **Scenario**: Case with hidden SIM, mic, and GSM module used to eavesdrop on user.
- **Attack Steps**: Step 1: Buy or build a custom phone case with embedded GSM module and mic.Step 2: Gift the case to the victim or swap it unnoticed.Step 3: GSM module powers on and transmits audio live when called.Step 4: Attacker can call the number anytime to listen in.Step 5: Victim never suspects because case looks normal.
- **Detection**: RF signal scanning
- **Solution**: Use OEM cases only
- **Tags**: covert case bug, gsm mic

## Magnetic Sensor Manipulation (Hall Sensor Bypass)

- **Attack Type**: Sensor Trick for Unauthorized Unlock
- **Target**: Phones with magnetic cases
- **Vulnerability**: Improper lock screen security
- **MITRE**: T1490
- **Impact**: Bypass authentication
- **Tools**: Strong neodymium magnet
- **Scenario**: Attacker uses a magnet to trick phone into thinking it's docked or open.
- **Attack Steps**: Step 1: Identify if victim's phone uses a magnetic sensor (Hall sensor) for auto unlock when opened (e.g., flip cases).Step 2: Use a magnet to simulate case opening.Step 3: If phone is configured improperly, it may auto-unlock.Step 4: Gain access to notifications or unlocked home screen.Step 5: Exploit access to collect data quickly.
- **Detection**: Check logs, fingerprint mismatch
- **Solution**: Disable auto-unlock by case
- **Tags**: hall sensor, magnetic hack

## Earpiece Replacement with Audio Tap

- **Attack Type**: Internal Audio Surveillance
- **Target**: Smartphones
- **Vulnerability**: Unsuspected hardware modifications
- **MITRE**: T1470
- **Impact**: Call audio capture, surveillance
- **Tools**: Custom earpiece module with mic
- **Scenario**: Earpiece is replaced with one containing a mic connected to a transmitter.
- **Attack Steps**: Step 1: Gain access to phone during screen repair or battery replacement.Step 2: Replace earpiece with a module that also includes a covert mic/transmitter.Step 3: Whenever user makes a call, the mic records or transmits conversation.Step 4: Attacker retrieves data over time.Step 5: Victim believes their phone is repaired normally.
- **Detection**: EMI test, teardown inspection
- **Solution**: Use authorized repair only
- **Tags**: earpiece mic tap, bug implant

## Wireless Charging Stand with Built-in Wi-Fi Sniffer

- **Attack Type**: Wi-Fi Passive Interception
- **Target**: Wi-Fi phones
- **Vulnerability**: Unencrypted Wi-Fi traffic
- **MITRE**: T1430
- **Impact**: Traffic sniffing, passive recon
- **Tools**: Modified wireless stand, ESP8266
- **Scenario**: Charging stand captures unencrypted Wi-Fi traffic while charging.
- **Attack Steps**: Step 1: Embed Wi-Fi sniffer chip (ESP8266) inside a Qi charging stand.Step 2: Place stand in common area (e.g., office desk).Step 3: Victim places phone on stand to charge.Step 4: While phone connects to Wi-Fi, sniffer logs nearby network traffic.Step 5: Extract traffic or forward it later to attacker.
- **Detection**: Network anomaly detection
- **Solution**: Use own chargers, encrypted Wi-Fi
- **Tags**: wifi charger spy, packet capture

## Fake Wireless Earbuds with Voice Relay

- **Attack Type**: Audio Relay via Earbuds
- **Target**: Smartphones
- **Vulnerability**: Malicious peripheral trust
- **MITRE**: T1426
- **Impact**: Voice spy, call data breach
- **Tools**: Modified earbuds, GSM chip
- **Scenario**: Wireless earbuds with built-in microphone and GSM used to relay audio.
- **Attack Steps**: Step 1: Modify wireless earbuds to include GSM relay circuit.Step 2: Pair them with victim’s phone or gift them.Step 3: Earbuds transmit everything user says or hears in calls.Step 4: Attacker receives live audio via GSM or Bluetooth.Step 5: Can be remotely activated or continuous.
- **Detection**: RF signal or GSM activity
- **Solution**: Use known brand accessories
- **Tags**: audio bug, earbuds hack

## Inductive Keylogger under Table for Phone Typing

- **Attack Type**: Magnetic Field Logger
- **Target**: Smartphones
- **Vulnerability**: Magnetic field leakage
- **MITRE**: T1056
- **Impact**: Keystroke inference
- **Tools**: Magnetometer array
- **Scenario**: Magnetic field sensor under table logs touch typing from phone placed above.
- **Attack Steps**: Step 1: Install sensitive magnetic field sensors under a desk or cafe table.Step 2: Wait for victims to use their phone by placing it flat on table.Step 3: As they type on soft keyboard, the tiny magnetic pulses are detected.Step 4: Map touch patterns to common keyboard layouts.Step 5: Infer typed content from proximity signals.
- **Detection**: Signal pattern analysis
- **Solution**: Don’t type over metal desks
- **Tags**: magnetic logger, inductive tap

## Fake SIM Tray That Records PIN Entry

- **Attack Type**: Hardware Implant in SIM Tray
- **Target**: Phones with PIN-protected SIMs
- **Vulnerability**: Physical SIM tray access
- **MITRE**: T1056.001
- **Impact**: SIM PIN compromise
- **Tools**: SIM tray with micro-circuit
- **Scenario**: SIM tray includes thin sensor that records SIM unlock PIN entries.
- **Attack Steps**: Step 1: Replace victim’s SIM tray with a modified one (can happen during repair).Step 2: Circuit detects physical vibration or signal as user enters SIM PIN.Step 3: Data is stored on a flash chip or sent via RF.Step 4: Attacker later retrieves or intercepts the data.Step 5: Use PIN to hijack or clone SIM later.
- **Detection**: SIM PIN retry logs
- **Solution**: Don’t use 4-digit SIM PINs
- **Tags**: hardware PIN trap, sim tray

## Spy Chip Inside Stylus (S-Pen / Pencil)

- **Attack Type**: Stylus-Embedded Logger
- **Target**: Phones/tablets with stylus support
- **Vulnerability**: Trust in accessories
- **MITRE**: T1474
- **Impact**: Input tracking, privacy breach
- **Tools**: Modified stylus, BLE chip
- **Scenario**: Stylus with added chip logs screen touches and sends data to attacker.
- **Attack Steps**: Step 1: Modify a smart stylus by embedding a BLE chip and small storage.Step 2: Gift or swap stylus used on victim’s tablet or phone.Step 3: Stylus logs touch coordinates and pressure data.Step 4: Later sync with attacker’s phone or laptop to extract info.Step 5: Can reveal written passwords or drawings.
- **Detection**: BLE scan tools
- **Solution**: Use factory accessories
- **Tags**: stylus hack, pen logger

## USB Microphone Implant in Office PC

- **Attack Type**: Surveillance Implant
- **Target**: Desktop Computer
- **Vulnerability**: Physical USB Access
- **MITRE**: T1055 (Process Injection)
- **Impact**: Espionage, Privacy Breach
- **Tools**: USB microphone module, open case tools
- **Scenario**: Attacker installs a USB device that silently records audio from nearby conversations in an office PC.
- **Attack Steps**: Step 1: Buy a USB microphone that looks like a pen drive.Step 2: Wait for the target to leave their desk.Step 3: Plug the USB mic into the back USB port of their PC.Step 4: Hide the cable or plug among other devices.Step 5: Let the USB mic record audio silently; retrieve it later or configure it to auto-upload using a hidden script.
- **Detection**: Manual inspection, Endpoint scan
- **Solution**: USB port lockdown, Regular physical inspections
- **Tags**: surveillance, espionage, usb implant

## Keyboard Bug Implant

- **Attack Type**: Keystroke Surveillance
- **Target**: Keyboard
- **Vulnerability**: Physical Device Swap
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Credential Theft, Data Leak
- **Tools**: Hardware keylogger inside keyboard
- **Scenario**: A bugged keyboard is swapped with the target’s keyboard to capture all typed information.
- **Attack Steps**: Step 1: Purchase a keyboard with built-in hardware keylogger.Step 2: Wait for a time when the user isn’t at the desk.Step 3: Unplug their keyboard and replace it with the bugged one.Step 4: The keylogger inside logs all key presses.Step 5: After some time, retrieve the keyboard and extract the logged data.
- **Detection**: Forensics on USB devices
- **Solution**: Supply only trusted peripherals
- **Tags**: hardware keylogger, credential theft

## Hidden Camera in Power Adapter

- **Attack Type**: Optical Surveillance
- **Target**: Office / Conference Room
- **Vulnerability**: Unsecured Power Sockets
- **MITRE**: T1123 (Audio Capture), T1125 (Video Capture)
- **Impact**: Privacy Violation, Data Theft
- **Tools**: Spy cam adapter, microSD card
- **Scenario**: Spy camera hidden inside a fake power adapter records video of a private space.
- **Attack Steps**: Step 1: Buy a spy camera built into a working USB power adapter.Step 2: Plug it into a power outlet in the target room (e.g., near desk or conference room).Step 3: Ensure it has a microSD card or Wi-Fi for auto-upload.Step 4: Let it record silently.Step 5: Retrieve footage later from SD card or Wi-Fi panel.
- **Detection**: Physical sweeps, RF scanners
- **Solution**: Conduct regular hardware audits
- **Tags**: surveillance, optical bug

## GSM Bug Under Desk

- **Attack Type**: Covert Audio Surveillance
- **Target**: Office / Meeting Room
- **Vulnerability**: Lack of physical device scanning
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Eavesdropping, Corporate Espionage
- **Tools**: GSM bug, prepaid SIM card
- **Scenario**: GSM audio bug is placed under a desk to live-stream conversations via mobile network.
- **Attack Steps**: Step 1: Purchase a GSM bug that transmits audio over mobile network.Step 2: Insert a SIM card with enough balance.Step 3: Charge the device fully.Step 4: Stick it under a desk with double tape.Step 5: Call the bug's SIM number anytime to hear live conversation.
- **Detection**: RF signal sweepers
- **Solution**: RF shielding, physical check routines
- **Tags**: gsm bug, spying, audio tap

## Smart Lightbulb Spy Implant

- **Attack Type**: IoT Espionage Device
- **Target**: Smart Office Devices
- **Vulnerability**: Unmonitored IoT installations
- **MITRE**: T1123, T1124 (Remote Surveillance)
- **Impact**: Continuous monitoring, Privacy breach
- **Tools**: Smart bulb w/ microphone, IoT app
- **Scenario**: Modified smart lightbulb used to secretly record and exfiltrate conversations.
- **Attack Steps**: Step 1: Modify a smart lightbulb to contain a microphone and Wi-Fi module.Step 2: Install the bulb in the office where people regularly talk.Step 3: Connect the bulb to Wi-Fi and control it via mobile app.Step 4: Use the hidden mic to stream or record audio.Step 5: Transfer data over the network when unnoticed.
- **Detection**: Network traffic analysis, RF scan
- **Solution**: Network segmentation, whitelist IoT devices
- **Tags**: iot espionage, smart bulb, mic

## Pen Recorder Left on Desk

- **Attack Type**: Covert Audio Surveillance
- **Target**: Meeting Room
- **Vulnerability**: Unattended Physical Items
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Data Leakage, Espionage
- **Tools**: Voice recorder pen
- **Scenario**: A voice recorder disguised as a pen records conversations in meeting rooms.
- **Attack Steps**: Step 1: Buy a pen with built-in audio recorder.Step 2: Turn on the recording switch and leave it casually on a desk before a meeting.Step 3: Let it record the entire session silently.Step 4: Pick it up later and download the recording using USB cable.Step 5: Listen and analyze captured data.
- **Detection**: Sweep meetings for devices
- **Solution**: Ban external gadgets during meetings
- **Tags**: spy pen, meeting surveillance

## Modified Mouse with Audio Logger

- **Attack Type**: Audio Surveillance Implant
- **Target**: Desktop Workstation
- **Vulnerability**: Device Replacement
- **MITRE**: T1123
- **Impact**: Confidential Data Leak
- **Tools**: Modified USB mouse, mic module
- **Scenario**: A normal-looking mouse is altered to record ambient audio via an internal mic.
- **Attack Steps**: Step 1: Open a USB mouse and insert a small microphone and voice recorder chip.Step 2: Seal the mouse back properly to look untouched.Step 3: Replace user’s mouse with this one when they’re away.Step 4: The mic will silently record while user works.Step 5: Retrieve mouse later and access stored audio.
- **Detection**: Endpoint behavior analysis
- **Solution**: Use only trusted, sealed accessories
- **Tags**: audio implant, mouse, espionage

## Wi-Fi Tap on Printer

- **Attack Type**: Network Espionage Device
- **Target**: Network Printer
- **Vulnerability**: Unsecured Internal Ports
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Document Theft
- **Tools**: Raspberry Pi Zero W, USB adapter
- **Scenario**: Tiny Wi-Fi tap is planted inside a network printer to sniff or relay printed documents.
- **Attack Steps**: Step 1: Get a Raspberry Pi Zero W and configure it to act as a packet sniffer.Step 2: Open the printer casing and connect it to the internal USB hub or network cable.Step 3: Power it via printer USB.Step 4: Let it silently capture documents being printed.Step 5: Connect remotely and download data via Wi-Fi.
- **Detection**: Unusual network traffic
- **Solution**: Restrict internal port access
- **Tags**: printer tap, packet sniff

## Fake Smoke Detector with Camera

- **Attack Type**: Optical Surveillance
- **Target**: Office Room / Bedroom
- **Vulnerability**: Fake Safety Devices
- **MITRE**: T1125 (Video Capture)
- **Impact**: Visual Espionage
- **Tools**: Dummy smoke detector cam
- **Scenario**: Spy camera is hidden inside a fake smoke detector in a room ceiling.
- **Attack Steps**: Step 1: Purchase a dummy smoke detector with hidden camera.Step 2: Install it on the ceiling using regular screws.Step 3: Power it using internal battery or nearby line.Step 4: Camera silently records video from above.Step 5: Collect recordings using SD card or Wi-Fi.
- **Detection**: Physical check of ceiling fixtures
- **Solution**: Use certified safety devices
- **Tags**: spy cam, fake detector

## Bluetooth Beacon in Bag

- **Attack Type**: Location Surveillance
- **Target**: Personal Belongings
- **Vulnerability**: Unmonitored Objects
- **MITRE**: T1430 (Location Tracking)
- **Impact**: Privacy Violation
- **Tools**: BLE beacon, tracking app
- **Scenario**: Attacker places a tracking Bluetooth beacon in victim’s bag to follow them.
- **Attack Steps**: Step 1: Buy a BLE beacon with long battery life.Step 2: Pair it with your tracking phone app.Step 3: Slip it into the side pocket of victim’s backpack when unattended.Step 4: Track their location in real-time using BLE proximity.Step 5: Remove once enough movement data collected.
- **Detection**: BLE scans, location anomalies
- **Solution**: Awareness training, anti-tracking apps
- **Tags**: BLE tracker, stalking

## SIM-Based GPS Tracker Under Car

- **Attack Type**: Physical Tracking
- **Target**: Vehicle
- **Vulnerability**: External Access
- **MITRE**: T1430
- **Impact**: Physical Movement Surveillance
- **Tools**: Magnetic GPS tracker with SIM
- **Scenario**: A small GPS tracking device is magnetically attached under a car to follow movement.
- **Attack Steps**: Step 1: Buy a GPS tracker with SIM and live tracking support.Step 2: Charge the device and insert a working SIM card.Step 3: Stick it under the car’s metal frame using magnet.Step 4: Use the vendor app to monitor car’s movement in real-time.Step 5: Remove device after collecting location patterns.
- **Detection**: Physical inspection under vehicle
- **Solution**: Use anti-tracking sweepers
- **Tags**: car tracking, sim gps

## Smart TV with Hidden Surveillance App

- **Attack Type**: IoT Espionage
- **Target**: Smart TVs
- **Vulnerability**: Unlocked Firmware / App Store
- **MITRE**: T1123, T1125
- **Impact**: Audio & Visual Espionage
- **Tools**: Smart TV, hidden app APK
- **Scenario**: Attacker installs a hidden surveillance app in a smart TV to record voice and screen.
- **Attack Steps**: Step 1: Get physical access to the smart TV (e.g., break room).Step 2: Install a hidden Android-based spy app via USB or OTA.Step 3: Enable mic and camera access in settings.Step 4: Let the TV silently listen or capture visual data.Step 5: Connect remotely and download logs.
- **Detection**: Network traffic monitoring
- **Solution**: Disable unknown apps, lockdown firmware
- **Tags**: smart tv spying

## Keyboard with RF Transmitter

- **Attack Type**: Remote Keylogging
- **Target**: Desktop System
- **Vulnerability**: Hardware Replacement
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Credential Theft
- **Tools**: RF bugged keyboard, SDR receiver
- **Scenario**: A keyboard with RF transmitter sends typed keystrokes to attacker’s receiver nearby.
- **Attack Steps**: Step 1: Replace target's keyboard with a modified one with RF transmitter.Step 2: Place an SDR receiver within range (e.g., next office room).Step 3: Collect keystrokes wirelessly as user types.Step 4: Decode data using SDR software.Step 5: Analyze for sensitive data like passwords or chats.
- **Detection**: RF sweep, USB activity logs
- **Solution**: Supply chain vetting
- **Tags**: rf keylogger, wireless bug

## Flash Drive with Auto Recorder

- **Attack Type**: Audio Bug
- **Target**: Workstation
- **Vulnerability**: USB Physical Access
- **MITRE**: T1123
- **Impact**: Audio Surveillance
- **Tools**: Dual-function USB recorder
- **Scenario**: Flash drive that works normally also has hidden mic that activates on plug-in.
- **Attack Steps**: Step 1: Purchase a flash drive with built-in audio recorder.Step 2: Plug it into the target’s computer when unattended.Step 3: The mic starts recording once plugged in (auto-activation).Step 4: After some time, retrieve it and listen to recording.Step 5: Repeat if needed.
- **Detection**: USB port audits
- **Solution**: Disable unauthorized USBs
- **Tags**: usb bug, covert recorder

## Bugged Power Bank

- **Attack Type**: Covert Surveillance Power
- **Target**: Public/Shared Room
- **Vulnerability**: Unmonitored Devices
- **MITRE**: T1123
- **Impact**: Privacy Invasion
- **Tools**: Power bank with hidden mic
- **Scenario**: Power bank with mic is left charging in shared space to record conversations.
- **Attack Steps**: Step 1: Get a power bank with hidden audio recorder.Step 2: Charge it and switch on mic recording mode.Step 3: Leave it on a table or near a couch where people chat.Step 4: Pick it up later and access the recordings.Step 5: Replay and analyze conversation.
- **Detection**: RF scans, visual inspection
- **Solution**: Restrict unknown devices
- **Tags**: power bank spy

## Surveillance Smartwatch Left Behind

- **Attack Type**: Covert Audio/Location Surveillance
- **Target**: Office / Personal Bag
- **Vulnerability**: Unattended Gadget Left Behind
- **MITRE**: T1123, T1430
- **Impact**: Audio capture, Location leakage
- **Tools**: Smartwatch with recorder
- **Scenario**: Smartwatch with hidden recorder is left on a desk or in a bag to record meetings or track movements.
- **Attack Steps**: Step 1: Configure the smartwatch to auto-record audio.Step 2: Place the watch in an office drawer, desk, or victim’s bag.Step 3: Leave it on recording for hours.Step 4: Return later to retrieve and access files.Step 5: Alternatively, use Bluetooth tethering to download files.
- **Detection**: Device search, BLE sweep
- **Solution**: Restrict unregistered gadgets
- **Tags**: smartwatch spying, location tracking

## Hidden Mic in Office Chair

- **Attack Type**: Audio Surveillance
- **Target**: Office Furniture
- **Vulnerability**: Physical Planting Opportunity
- **MITRE**: T1123
- **Impact**: Internal audio leak
- **Tools**: Small mic module, battery
- **Scenario**: A tiny mic is hidden inside a chair cushion to record sensitive discussions.
- **Attack Steps**: Step 1: Take a small recorder module with battery.Step 2: Zip open the seat cushion and place it deep inside.Step 3: Ensure it is powered and on.Step 4: Let it record full workday of conversations.Step 5: Retrieve the mic and listen to files later.
- **Detection**: Manual chair inspection
- **Solution**: Physical device inspection policy
- **Tags**: hidden mic, seat bug

## Modified Phone Charger Bug

- **Attack Type**: USB Spy Charger
- **Target**: Work Room / Study
- **Vulnerability**: Device Acceptance Without Checks
- **MITRE**: T1123
- **Impact**: Audio surveillance, Privacy risk
- **Tools**: Audio-recording charger
- **Scenario**: A phone charger that records audio or acts as a listening device is planted in a room.
- **Attack Steps**: Step 1: Buy a charger that works normally but contains hidden mic.Step 2: Plug it into a wall socket or desk power point.Step 3: Leave it in the room for extended periods.Step 4: Retrieve charger later and download recordings.Step 5: Repeat when needed.
- **Detection**: Charger checks, RF scan
- **Solution**: Allow only verified accessories
- **Tags**: spy charger, usb mic

## Compromised Docking Station

- **Attack Type**: Data Exfiltration Device
- **Target**: Laptop / Office Desk
- **Vulnerability**: Hardware Supply Chain Risk
- **MITRE**: T1125, T1056.001
- **Impact**: Full surveillance, data leak
- **Tools**: Bugged docking station, microcontroller
- **Scenario**: Modified docking station logs keystrokes and records webcam/audio feeds.
- **Attack Steps**: Step 1: Use a modified docking station with built-in logger and camera/mic module.Step 2: Swap user’s docking station when they are away.Step 3: The implant captures webcam and mic feeds.Step 4: Stores to hidden flash storage or streams via LAN.Step 5: Access the logs remotely or collect device later.
- **Detection**: Internal audits of hardware
- **Solution**: Issue hardware from secured stock only
- **Tags**: bugged dock, cam mic logger

## Wall Clock with Wi-Fi Spy Cam

- **Attack Type**: Visual Surveillance
- **Target**: Private Office
- **Vulnerability**: Visible Trusted Fixtures
- **MITRE**: T1125
- **Impact**: Visual recording, behavioral spying
- **Tools**: Wall clock camera
- **Scenario**: A clock with an integrated Wi-Fi spy cam is installed on a wall in private office.
- **Attack Steps**: Step 1: Purchase a working wall clock with hidden spy cam.Step 2: Mount it in a visible area of the room.Step 3: Configure it to stream over Wi-Fi to remote phone.Step 4: Monitor office activity silently.Step 5: Periodically change battery or SD card.
- **Detection**: Inspect wall-mounted devices
- **Solution**: Use only approved clocks/furnishings
- **Tags**: wifi clock cam

## Eyeglasses with Camera

- **Attack Type**: Body-Worn Surveillance
- **Target**: Meeting Room / One-on-One
- **Vulnerability**: Inconspicuous Recording Devices
- **MITRE**: T1125
- **Impact**: Visual Data Theft
- **Tools**: Spy camera glasses
- **Scenario**: Eyeglasses with hidden camera used to record confidential discussions unnoticed.
- **Attack Steps**: Step 1: Wear glasses with built-in micro-camera.Step 2: Activate video recording before entering room.Step 3: Engage in conversation while it records.Step 4: After leaving, connect to PC and download footage.Step 5: Analyze any sensitive data captured.
- **Detection**: Surveillance camera reviews
- **Solution**: No personal devices in secure zones
- **Tags**: glasses spy cam

## Trash Bin Mic Implant

- **Attack Type**: Long-Term Surveillance
- **Target**: Office Trash Bin
- **Vulnerability**: Commonly Ignored Object
- **MITRE**: T1123
- **Impact**: Audio surveillance
- **Tools**: Small voice recorder, Velcro
- **Scenario**: Audio bug placed in office trash bin to monitor conversations.
- **Attack Steps**: Step 1: Prepare a voice recorder with long battery life.Step 2: Stick it under the trash bin lid using Velcro or tape.Step 3: Activate mic recording mode.Step 4: Leave bin in high-discussion area.Step 5: Recover device after a day to extract recordings.
- **Detection**: Manual check of surroundings
- **Solution**: Avoid placing bins in private areas
- **Tags**: trash bug, audio recorder

## HVAC Vent Camera

- **Attack Type**: Hidden Surveillance
- **Target**: Office / Lab Room
- **Vulnerability**: Hidden in Infrastructure
- **MITRE**: T1125
- **Impact**: Visual surveillance, privacy invasion
- **Tools**: Mini cam, adhesive, battery
- **Scenario**: Mini camera is mounted inside the air vent to monitor room activity.
- **Attack Steps**: Step 1: Choose a small wireless camera with battery or USB.Step 2: Open an air vent grill in the room.Step 3: Stick the camera inside facing the room.Step 4: Ensure connection via Wi-Fi.Step 5: Monitor footage remotely or save to SD card.
- **Detection**: HVAC vent audits, camera scanning
- **Solution**: Block line-of-sight inside vents
- **Tags**: hvac cam, room spying

## Laptop Webcam Overlay Capture

- **Attack Type**: Overlay Surveillance
- **Target**: Laptop
- **Vulnerability**: Optical Reflection Abuse
- **MITRE**: T1125
- **Impact**: Screen spying without access
- **Tools**: Clear acrylic overlay, camera
- **Scenario**: Transparent plastic placed over webcam to collect light reflections and reconstruct screen.
- **Attack Steps**: Step 1: Attach clear plastic overlay in front of target’s webcam lens.Step 2: Let user operate laptop normally.Step 3: Reflected light from screen creates patterns.Step 4: Retrieve overlay and analyze with camera frame-matching software.Step 5: Attempt screen reconstruction.
- **Detection**: Webcam tape, lens check
- **Solution**: Disable webcam or block lens physically
- **Tags**: overlay hack, webcam reflection

## Surveillance Drone Peek from Vent

- **Attack Type**: Remote Surveillance
- **Target**: Meeting Room / Bedroom
- **Vulnerability**: Physical Gaps (Vents, Windows)
- **MITRE**: T1125
- **Impact**: Surveillance without entry
- **Tools**: Mini drone with camera
- **Scenario**: Mini drone flies near open vent to record room activity from outside.
- **Attack Steps**: Step 1: Prepare mini drone with quiet propellers and camera.Step 2: Fly it near window or vent opening where the room is visible.Step 3: Record audio and video of activities inside.Step 4: Control remotely to exit after few minutes.Step 5: Store and review captured footage.
- **Detection**: Visual anomaly monitoring
- **Solution**: Seal external vents, use blinds
- **Tags**: drone surveillance, vent spying

## Power Strip with Hidden Recorder

- **Attack Type**: Long-Term Audio Bug
- **Target**: Office / Living Room
- **Vulnerability**: Trusted power accessories
- **MITRE**: T1123
- **Impact**: Ambient audio capture
- **Tools**: Recorder power strip
- **Scenario**: Power strip contains a hidden audio recording module and looks completely normal.
- **Attack Steps**: Step 1: Buy a power strip with built-in voice recorder.Step 2: Replace an existing strip in target’s room.Step 3: Ensure it's functional so it won’t raise suspicion.Step 4: Retrieve audio later from hidden internal storage.Step 5: Recharge and repeat if needed.
- **Detection**: Unplug & test unknown power strips
- **Solution**: Limit to certified power devices
- **Tags**: power strip bug

## Tampered Charging Cable Logger

- **Attack Type**: Data Theft via USB Cable
- **Target**: Phone / Laptop
- **Vulnerability**: Cable not checked for authenticity
- **MITRE**: T1056.001, T1204
- **Impact**: Credential & command theft
- **Tools**: O.MG cable clone
- **Scenario**: An ordinary-looking charging cable that logs keystrokes or injects malware when plugged in.
- **Attack Steps**: Step 1: Buy or build a malicious USB cable (O.MG clone).Step 2: Replace victim's normal phone or device charger.Step 3: When plugged in, it silently logs keystrokes or can open payloads.Step 4: Download logs remotely via Wi-Fi or retrieve cable.Step 5: Reset logs or reuse on new victim.
- **Detection**: Endpoint behavior scan, USB logs
- **Solution**: Block unauthorized USB cables
- **Tags**: omg cable, usb exploit

## Hidden Recorder in Desk Plant Pot

- **Attack Type**: Passive Audio Recorder
- **Target**: Office Desk
- **Vulnerability**: Ignored decorations
- **MITRE**: T1123
- **Impact**: Environmental spying
- **Tools**: Mini recorder, fake plant
- **Scenario**: A tiny audio recorder is placed in a decorative plant pot to capture room conversations.
- **Attack Steps**: Step 1: Hide a small recorder inside the base of a decorative pot.Step 2: Place the plant in a room where sensitive discussions occur.Step 3: Activate recorder; battery lasts for hours.Step 4: Retrieve the pot later and access the files.Step 5: Replace or reuse as needed.
- **Detection**: Visual + device inspection
- **Solution**: Avoid placing personal items
- **Tags**: pot mic, decor bug

## Magnetic GPS Tag on Metal Locker

- **Attack Type**: Employee Movement Tracking
- **Target**: Locker / Cabinet
- **Vulnerability**: External surface access
- **MITRE**: T1430
- **Impact**: Behavioral surveillance
- **Tools**: GPS tracker, magnet base
- **Scenario**: A tiny GPS tag is magnetically attached to an employee’s locker to track entry/exit habits.
- **Attack Steps**: Step 1: Prepare a small magnetic GPS tracker.Step 2: Attach it underneath or behind a locker door.Step 3: Let it log movements when locker opens/moves.Step 4: Retrieve or connect via app to see timeline.Step 5: Use data for pattern surveillance.
- **Detection**: Inspect external surfaces
- **Solution**: Internal locker check policy
- **Tags**: gps locker track

## Pen Drive That Acts as Covert Audio Tap

- **Attack Type**: Multi-Function Spy Device
- **Target**: Desktop Computer
- **Vulnerability**: USB port not monitored
- **MITRE**: T1123
- **Impact**: Ambient audio theft
- **Tools**: Audio recorder USB stick
- **Scenario**: Flash drive that records audio as soon as it's inserted into any USB port.
- **Attack Steps**: Step 1: Get a USB stick with audio recorder module.Step 2: Plug into target’s PC without their noticing.Step 3: The stick will silently record surrounding sounds.Step 4: Retrieve and plug into your PC to extract audio.Step 5: Reset or reuse as needed.
- **Detection**: USB usage logs, port blockers
- **Solution**: Limit external USB access
- **Tags**: covert usb mic

## Mini Audio Bug Hidden in Wall Clock Battery Slot

- **Attack Type**: Embedded Audio Bug
- **Target**: Office Wall Clock
- **Vulnerability**: Clock not examined closely
- **MITRE**: T1123
- **Impact**: Meeting eavesdropping
- **Tools**: Mic module, clock, tape
- **Scenario**: A battery-powered voice recorder is inserted behind the battery of a wall clock.
- **Attack Steps**: Step 1: Remove clock battery and place a flat mic behind it.Step 2: Place battery back in, sealing the mic.Step 3: Start recording and hang clock as normal.Step 4: After recording period, remove and retrieve mic.Step 5: Extract files on computer.
- **Detection**: Inspect object interiors
- **Solution**: Use tamper-proof items
- **Tags**: battery slot mic

## Drone Audio Relay at Window

- **Attack Type**: Remote Audio Surveillance
- **Target**: Office/Home Window
- **Vulnerability**: Open perimeter
- **MITRE**: T1123
- **Impact**: Privacy invasion
- **Tools**: Quiet drone with audio mic
- **Scenario**: A drone hovers quietly outside an open window and records conversations using its mic.
- **Attack Steps**: Step 1: Choose a silent drone with good audio capture.Step 2: Fly it to hover near an open office or home window.Step 3: Record audio during conversations.Step 4: Fly away and store or stream recording.Step 5: Edit and analyze the data collected.
- **Detection**: Motion detection camera
- **Solution**: Close windows, use curtains
- **Tags**: drone mic spy

## RFID Keylogger Embedded in Access Card Reader

- **Attack Type**: RFID Surveillance Implant
- **Target**: Office Door
- **Vulnerability**: Reader not physically monitored
- **MITRE**: T1557.002
- **Impact**: Unauthorized physical access
- **Tools**: Dummy RFID overlay
- **Scenario**: A fake RFID reader is placed over the real one to capture employee access card data.
- **Attack Steps**: Step 1: Create or buy a fake RFID reader shell.Step 2: Place it over the original reader at office entrance.Step 3: When employees swipe cards, it stores card ID info.Step 4: Retrieve it later to extract cloned data.Step 5: Use this data to clone access cards.
- **Detection**: Physical inspection of card readers
- **Solution**: Tamper-proof readers
- **Tags**: rfid keylog, access clone

## Smart Speaker Eavesdropping Exploit

- **Attack Type**: IoT Voice Command Capture
- **Target**: Smart Home Device
- **Vulnerability**: Misconfigured Smart Devices
- **MITRE**: T1123
- **Impact**: Voice command theft, audio spy
- **Tools**: Smart speaker with open mic access
- **Scenario**: An attacker uses vulnerable smart speaker to silently record conversations.
- **Attack Steps**: Step 1: Gain temporary access to the device.Step 2: Enable developer/debugging mode or custom skill.Step 3: Configure it to listen and log all audio.Step 4: Link it to attacker’s remote account.Step 5: Retrieve or stream logs remotely.
- **Detection**: Device logs, app permissions
- **Solution**: Disable unknown skills, secure setup
- **Tags**: alexa/google spy

## Mini Camera Hidden in Air Freshener

- **Attack Type**: Concealed Optical Surveillance
- **Target**: Office/Bedroom
- **Vulnerability**: Common item misuse
- **MITRE**: T1125
- **Impact**: Private video spying
- **Tools**: Fake air freshener cam
- **Scenario**: Spy cam hidden inside a room air freshener silently records people.
- **Attack Steps**: Step 1: Purchase an air freshener with built-in hidden cam.Step 2: Place it in a meeting room or bedroom.Step 3: Power it on and record silently.Step 4: Access data via SD card or Wi-Fi.Step 5: Replace regularly if battery-operated.
- **Detection**: Visual + RF scanning
- **Solution**: Ban unverified décor devices
- **Tags**: air freshener spycam

## Covert Audio Bug in Coffee Mug

- **Attack Type**: Ambient Recording Device
- **Target**: Personal Desk
- **Vulnerability**: No check on desk items
- **MITRE**: T1123
- **Impact**: Low-profile surveillance
- **Tools**: Modified mug with mic
- **Scenario**: A coffee mug is modified to contain an audio recorder and left on the desk.
- **Attack Steps**: Step 1: Insert small mic with battery under the mug base.Step 2: Seal it to look like normal mug.Step 3: Leave it on target's desk.Step 4: Record all ambient conversations.Step 5: Retrieve mug and extract data.
- **Detection**: Object inspection
- **Solution**: Don’t allow external gifts/items
- **Tags**: bugged mug, desk spy

## Car Charger with Listening Device

- **Attack Type**: Mobile Audio Tap
- **Target**: Vehicle Interior
- **Vulnerability**: Unchecked accessories
- **MITRE**: T1123
- **Impact**: Eavesdropping on travel talk
- **Tools**: Car charger bug
- **Scenario**: A car charger is used as a tool to capture and transmit audio while driving.
- **Attack Steps**: Step 1: Buy a car charger with embedded microphone.Step 2: Plug it into target’s vehicle power socket.Step 3: The bug records in-car conversations.Step 4: Data is stored or transmitted via GSM.Step 5: Attacker listens remotely or retrieves later.
- **Detection**: Physical scan of electronics
- **Solution**: Use only trusted gear
- **Tags**: car charger bug, gsm mic

## Tapped Power Cord Extension

- **Attack Type**: Audio Bug Embedded
- **Target**: Conference Room
- **Vulnerability**: Unverified extension cords
- **MITRE**: T1123
- **Impact**: Meeting data leak
- **Tools**: Audio tap power cable
- **Scenario**: Power extension cord with mic inside collects data from boardroom discussions.
- **Attack Steps**: Step 1: Use a power cord with audio recorder hidden inside.Step 2: Install it in boardroom with laptops connected.Step 3: Recorder activates upon connection or timer.Step 4: After hours/days, retrieve cord.Step 5: Listen and analyze data.
- **Detection**: Check cabling & plug sources
- **Solution**: Centralized cord issuing
- **Tags**: power bug cord

## Whiteboard Marker with Mic

- **Attack Type**: Passive Classroom Spy Tool
- **Target**: Meeting Room / Class
- **Vulnerability**: Disguised everyday items
- **MITRE**: T1123
- **Impact**: Lecture or plan leakage
- **Tools**: Spy marker with mic
- **Scenario**: Modified whiteboard marker records class or meeting sessions from up close.
- **Attack Steps**: Step 1: Use a whiteboard marker that includes a tiny mic.Step 2: Leave it on the table before meeting.Step 3: Enable recording with switch or motion sensor.Step 4: Pick it up after session ends.Step 5: Extract audio using USB port.
- **Detection**: Check odd-looking tools
- **Solution**: Lock sensitive supplies
- **Tags**: mic marker, board spy

## Compromised Laptop Stand

- **Attack Type**: Integrated Mic Logger
- **Target**: Office Desk
- **Vulnerability**: Physical workspace implants
- **MITRE**: T1123
- **Impact**: Long-term audio bugging
- **Tools**: Bugged laptop stand
- **Scenario**: Laptop stand has mic and small recorder built into the frame.
- **Attack Steps**: Step 1: Modify laptop stand to include mic.Step 2: Place in target’s work desk.Step 3: Enable continuous recording mode.Step 4: Retrieve device after hours or days.Step 5: Review recording.
- **Detection**: Check physical device specs
- **Solution**: Use issued peripherals
- **Tags**: mic stand, laptop bug

## RFID Tag Under Car Floor Mat

- **Attack Type**: Long-Term Location Surveillance
- **Target**: Personal Vehicle
- **Vulnerability**: Physical RFID exposure
- **MITRE**: T1430
- **Impact**: Tracking movement pattern
- **Tools**: Passive RFID tag
- **Scenario**: Passive RFID tag under floor mat is used to track car presence via RFID sensors.
- **Attack Steps**: Step 1: Buy small passive RFID tag.Step 2: Stick it under driver-side floor mat.Step 3: Use external scanner to detect entry/exit.Step 4: Map car behavior based on log time.Step 5: Remove when enough data collected.
- **Detection**: Passive RFID scans
- **Solution**: Limit car RFID zones
- **Tags**: rfid mat tag

## Reversing Using Open Firmware Dumps

- **Attack Type**: Static Firmware Reverse Engineering
- **Target**: Router/IoT
- **Vulnerability**: Unencrypted Firmware
- **MITRE**: T1204: User Execution (binary patch)
- **Impact**: Discover secrets or vulnerabilities
- **Tools**: Ghidra, Binwalk, Strings, Hex editor
- **Scenario**: Attacker downloads publicly leaked firmware or dumps it from the device and reverse-engineers it.
- **Attack Steps**: Step 1: Get a firmware image from online source or dump it using PH-FWRE-001.Step 2: Run binwalk to list embedded files and structure.Step 3: Extract file system using binwalk -e.Step 4: Analyze files for passwords, config files, binaries.Step 5: Load extracted binaries into Ghidra to view code logic.Step 6: Look for hardcoded credentials, command injection points.
- **Detection**: Firmware hash & integrity monitor
- **Solution**: Encrypt + obfuscate firmware
- **Tags**: reverse, binwalk, ghidra

## JTAG Exploitation for Firmware Access

- **Attack Type**: Debug Interface Abuse
- **Target**: Industrial Controller
- **Vulnerability**: Open JTAG Interface
- **MITRE**: T1068: Exploitation for Privilege Escalation
- **Impact**: Root firmware access
- **Tools**: JTAGulator, OpenOCD, GDB, Soldering kit
- **Scenario**: Attacker uses JTAG interface to dump memory or halt execution for analysis.
- **Attack Steps**: Step 1: Open device and search for JTAG pins (usually 4-5 in row).Step 2: Use JTAGulator to identify correct pinout.Step 3: Solder jumper wires to identified JTAG pins.Step 4: Connect pins to debugger (e.g., Segger J-Link) and interface with OpenOCD.Step 5: Use GDB to halt the processor and dump memory.Step 6: Save dumped image and analyze using Ghidra.
- **Detection**: Power-on memory integrity check
- **Solution**: Disable JTAG in production
- **Tags**: jtag, openocd, firmware

## Microcontroller Firmware Cloning

- **Attack Type**: Firmware Cloning
- **Target**: Smart Device
- **Vulnerability**: Unlocked Microcontroller
- **MITRE**: T1601: Data Staged
- **Impact**: IP Theft, Clone Devices
- **Tools**: ChipProg+, ISP connector, Programmer software
- **Scenario**: Attacker copies firmware directly from microcontroller if protection fuses are not set.
- **Attack Steps**: Step 1: Identify microcontroller part number on chip.Step 2: Connect programmer to microcontroller using ISP/SWD interface.Step 3: Use programmer software to read firmware from chip.Step 4: Save the firmware binary on local system.Step 5: Use hex editor to examine the contents.Step 6: Flash it into a duplicate chip to create a working clone.
- **Detection**: MCU Readout Protection Bit
- **Solution**: Set read protection bits
- **Tags**: mcu, clone, isp, ip-theft

## Dumping Firmware via SPI Bus Snooping

- **Attack Type**: Bus Interception
- **Target**: IoT Board
- **Vulnerability**: Unprotected SPI bus
- **MITRE**: T1040: Network Sniffing
- **Impact**: Partial or full firmware leak
- **Tools**: Logic Analyzer (e.g., Saleae), SPI probes, PulseView
- **Scenario**: Attacker taps into the SPI bus lines during boot to capture firmware being loaded into RAM.
- **Attack Steps**: Step 1: Open the device and locate the SPI chip (e.g., Flash IC).Step 2: Identify clock (CLK), chip select (CS), MOSI, and MISO pins.Step 3: Attach logic analyzer probes to these pins.Step 4: Use PulseView to capture SPI communication during power-up.Step 5: Save and reconstruct firmware from captured binary stream.
- **Detection**: Monitor SPI bus activity
- **Solution**: Shield SPI or encrypt data
- **Tags**: spi, sniffing, firmware

## EEPROM Configuration Dump

- **Attack Type**: EEPROM Extraction
- **Target**: Access Control Board
- **Vulnerability**: EEPROM with plaintext
- **MITRE**: T1552: Unsecured Credentials
- **Impact**: Config leak, bypass device
- **Tools**: EEPROM Reader (MiniPro TL866), Chip clip, Hex Editor
- **Scenario**: Attacker extracts configuration or secrets from EEPROM chips.
- **Attack Steps**: Step 1: Locate the EEPROM chip (usually 8-pin, labeled 24Cxx).Step 2: Attach a chip clip without desoldering.Step 3: Connect clip to MiniPro programmer.Step 4: Use programmer software to read EEPROM data.Step 5: Analyze config, credentials, or serials in hex editor.
- **Detection**: EEPROM checksum validation
- **Solution**: Encrypt EEPROM contents
- **Tags**: eeprom, dump, config, 24c

## NAND Flash Dumping and Filesystem Extraction

- **Attack Type**: NAND Dump & Analysis
- **Target**: Smart TV / Router
- **Vulnerability**: Unencrypted NAND
- **MITRE**: T1005: Local Data Exfiltration
- **Impact**: Gain firmware and user data
- **Tools**: NAND reader, Flash extractor, Binwalk
- **Scenario**: Attacker reads raw NAND flash, reconstructs file system.
- **Attack Steps**: Step 1: Desolder NAND flash chip carefully.Step 2: Place chip in NAND flash reader.Step 3: Dump raw image and save to PC.Step 4: Use binwalk and tools like ubi_reader to extract filesystem.Step 5: Analyze config files, firmware blobs, passwords.
- **Detection**: File structure diff tool
- **Solution**: Encrypt NAND + disable read
- **Tags**: nand, binwalk, ubi, reverse

## Extracting Bootloader via NOR Flash

- **Attack Type**: Bootloader Dump
- **Target**: Embedded Bootloader Chip
- **Vulnerability**: Unlocked NOR Flash
- **MITRE**: T1542: Boot or Logon Autostart
- **Impact**: Boot-level exploit
- **Tools**: NOR Flash Reader, Flashrom, Hex Editor
- **Scenario**: Attacker copies bootloader from NOR flash to analyze how device boots.
- **Attack Steps**: Step 1: Open device, locate NOR flash (marked e.g., MX29GLxxx).Step 2: Connect chip to flash reader (or use test clip).Step 3: Use Flashrom to read binary.Step 4: Use hex editor to isolate bootloader region.Step 5: Analyze bootloader logic for bypass or exploits.
- **Detection**: Monitor bootloader checksums
- **Solution**: Bootloader signing + secure boot
- **Tags**: bootloader, nor, flashrom

## Cold Boot Attack for Memory Dump

- **Attack Type**: Cold RAM Dump
- **Target**: Laptop, Embedded PC
- **Vulnerability**: RAM remanence
- **MITRE**: T1003: OS Credential Dumping
- **Impact**: Leak secrets in RAM
- **Tools**: USB Boot Stick, RAM Dumper Tool
- **Scenario**: Attacker rapidly reboots a device and accesses residual RAM content.
- **Attack Steps**: Step 1: Freeze device memory using compressed air upside-down.Step 2: Reboot device into USB live system with RAM dump utility.Step 3: Use tools to extract RAM data.Step 4: Analyze for credentials, keys, or firmware sections.Step 5: Correlate with firmware structure.
- **Detection**: Memory scrub on shutdown
- **Solution**: Full disk encryption + secure RAM clear
- **Tags**: coldboot, ramdump, keys

## Reverse Engineering BIOS Firmware

- **Attack Type**: BIOS Firmware Analysis
- **Target**: Desktop / Laptop
- **Vulnerability**: Unlocked BIOS
- **MITRE**: T1542.001: Bootkits
- **Impact**: Boot process hijack
- **Tools**: BIOS Programmer, UEFITool, Ghidra
- **Scenario**: Attacker extracts BIOS chip and reverse-engineers startup routines.
- **Attack Steps**: Step 1: Locate BIOS chip (e.g., Winbond 25Q64).Step 2: Use SOIC clip and connect to BIOS programmer.Step 3: Read firmware image.Step 4: Open image with UEFITool to browse structure.Step 5: Use Ghidra to analyze key binaries for backdoors.
- **Detection**: BIOS signature mismatch
- **Solution**: Enable Secure Boot
- **Tags**: bios, uefi, ghidra, dump

## Firmware Backdoor Discovery via Reversing

- **Attack Type**: Static Firmware Backdoor Analysis
- **Target**: Any Smart Device
- **Vulnerability**: Hardcoded Backdoor
- **MITRE**: T1059: Command and Scripting Interpreter
- **Impact**: Full unauthorized access
- **Tools**: Ghidra, Binwalk, Strings, Cutter
- **Scenario**: Attacker identifies hardcoded backdoors in firmware using reverse engineering.
- **Attack Steps**: Step 1: Obtain firmware image using previous methods.Step 2: Run strings to search for keywords like “root”, “admin”, “telnet”.Step 3: Load binaries into Ghidra.Step 4: Analyze authentication and networking routines.Step 5: Identify hidden credentials or debug services.
- **Detection**: Firmware behavior anomaly
- **Solution**: Remove debug code in release build
- **Tags**: backdoor, strings, root

## Reverse Engineering Device Logic with Logic Analyzer

- **Attack Type**: Functional Logic Capture
- **Target**: Embedded Controller
- **Vulnerability**: Exposed Bus Signals
- **MITRE**: T1602: Data from Information Repositories
- **Impact**: Protocol reverse, behavior mimic
- **Tools**: Logic Analyzer, PulseView
- **Scenario**: Attacker uses a logic analyzer to understand device communication and firmware behavior.
- **Attack Steps**: Step 1: Identify communication pins (e.g., SPI, I2C, UART).Step 2: Attach logic analyzer probes.Step 3: Power on device and record communication.Step 4: Analyze data flow to understand firmware response.Step 5: Use timing and values to infer logic or firmware flaws.
- **Detection**: Bus signal monitoring
- **Solution**: Obfuscate protocol and timing
- **Tags**: logic, reverse, pulseview

## Glitching MCU for Firmware Bypass

- **Attack Type**: Voltage Fault Injection
- **Target**: Microcontroller-based Device
- **Vulnerability**: No voltage fault mitigation
- **MITRE**: T1600: Hardware Additions
- **Impact**: Bypass secure boot or fuse
- **Tools**: ChipWhisperer, Power Glitcher
- **Scenario**: Attacker injects glitch during boot to bypass security check.
- **Attack Steps**: Step 1: Connect glitching tool to microcontroller's Vcc line.Step 2: Setup tool to inject glitch during specific boot cycle.Step 3: Reboot device; timing must hit security check.Step 4: If successful, access protected firmware zone.Step 5: Dump or modify firmware.
- **Detection**: Glitch detection circuit
- **Solution**: Add voltage watchdog
- **Tags**: glitch, fault, bootbypass

## Wireless Firmware Update Hijack

- **Attack Type**: OTA Firmware Abuse
- **Target**: Smart Light / IoT
- **Vulnerability**: Unverified OTA updates
- **MITRE**: T1557.001: Man-in-the-Middle
- **Impact**: Remote takeover
- **Tools**: Wi-Fi Sniffer, Rogue AP, Packet Injector
- **Scenario**: Attacker intercepts and replaces firmware during Over-The-Air (OTA) update.
- **Attack Steps**: Step 1: Setup rogue AP mimicking official firmware server.Step 2: Jam real signal to force device switch to rogue AP.Step 3: Host malicious firmware image.Step 4: Device downloads and installs attacker’s firmware.Step 5: Control gained on reboot.
- **Detection**: Firmware hash or TLS inspection
- **Solution**: Signed and encrypted OTA
- **Tags**: ota, mitm, rogue, update

## Reversing USB Device Firmware via Extraction

- **Attack Type**: USB Firmware Analysis
- **Target**: USB Thumb Drive / HID
- **Vulnerability**: Firmware not locked
- **MITRE**: T1059.005: Visual Basic
- **Impact**: Spread malware via modified USB
- **Tools**: USB disassembly kit, Flash reader, Hex Editor
- **Scenario**: Attacker extracts firmware from USB device flash chip to find malware or modify.
- **Attack Steps**: Step 1: Disassemble USB device and locate flash IC.Step 2: Read firmware using flash reader.Step 3: Analyze firmware in hex editor or binwalk.Step 4: Search for signatures of hidden partitions or payloads.Step 5: Modify, reflash, and test behavior.
- **Detection**: USB access monitoring
- **Solution**: Lock firmware after production
- **Tags**: usb, firmware, hid, hack

## Extracting Wi-Fi Credentials from Dumped Firmware

- **Attack Type**: Config Disclosure via Reverse Engineering
- **Target**: Smart Device
- **Vulnerability**: Plaintext credential storage
- **MITRE**: T1552.001: Credentials in Files
- **Impact**: Network access
- **Tools**: Binwalk, Strings, Hex Editor
- **Scenario**: Attacker finds stored Wi-Fi keys inside firmware image.
- **Attack Steps**: Step 1: Obtain firmware from flash or download site.Step 2: Use binwalk -e to extract file system.Step 3: Search config files (e.g., wpa_supplicant.conf).Step 4: Copy SSID and password.Step 5: Use Wi-Fi credentials to access local network.
- **Detection**: Config file scan alerts
- **Solution**: Encrypt stored credentials
- **Tags**: wifi, firmware, extract

## Reverse Engineering Proprietary Firmware Protocols

- **Attack Type**: Protocol Mapping via Firmware
- **Target**: Industrial Controller
- **Vulnerability**: Obscure proprietary protocol
- **MITRE**: T1040: Network Protocol Manipulation
- **Impact**: Unauthorized control
- **Tools**: Ghidra, Packet capture, Logic analyzer
- **Scenario**: Attacker studies firmware code to replicate or hijack proprietary protocols.
- **Attack Steps**: Step 1: Obtain and decompile firmware.Step 2: Identify protocol routines (e.g., functions calling UART or I2C).Step 3: Reconstruct message formats and commands.Step 4: Simulate communication using Python or terminal.Step 5: Use protocol knowledge to control device.
- **Detection**: Protocol fingerprinting
- **Solution**: Use TLS or signed commands
- **Tags**: reverse, protocol, custom

## Dumping MCU Firmware via SWD Interface

- **Attack Type**: Debug Port Firmware Extraction
- **Target**: STM32 Device
- **Vulnerability**: ROP Bit Not Set
- **MITRE**: T1005: Local Data from MCU
- **Impact**: Firmware clone or analysis
- **Tools**: ST-Link debugger, OpenOCD
- **Scenario**: Attacker connects to SWD interface and dumps firmware if not locked.
- **Attack Steps**: Step 1: Identify SWD (Serial Wire Debug) pins on PCB.Step 2: Solder wires and connect ST-Link debugger.Step 3: Use OpenOCD or ST-Link Utility to read flash.Step 4: Save firmware for analysis.Step 5: Confirm if Read-Out Protection (ROP) was disabled.
- **Detection**: MCU ROP fuse check
- **Solution**: Always enable read protection
- **Tags**: swd, stm32, dump

## Injecting Persistent Keylogger in Firmware

- **Attack Type**: Malicious Firmware Injection
- **Target**: USB Keyboard
- **Vulnerability**: Writable HID firmware
- **MITRE**: T1056.001: Keylogging
- **Impact**: Credential theft
- **Tools**: Firmware mod tools, USB reflash tool
- **Scenario**: Attacker embeds keylogger into firmware of HID device like keyboard.
- **Attack Steps**: Step 1: Obtain firmware image of keyboard.Step 2: Modify USB descriptor to log keystrokes.Step 3: Flash modified firmware into keyboard controller.Step 4: Device silently records user input.Step 5: Logs sent via hidden USB channel.
- **Detection**: Monitor for unexpected USB traffic
- **Solution**: Lock HID firmware at factory
- **Tags**: keylogger, usb, firmware

## Firmware Signature Forgery for Bypass

- **Attack Type**: Signature Tampering
- **Target**: IoT Gateway
- **Vulnerability**: Weak signature scheme
- **MITRE**: T1553.003: Subvert Trust Controls
- **Impact**: Malicious firmware load
- **Tools**: Hex Editor, Firmware unpacker
- **Scenario**: Attacker modifies firmware and forges or disables signature checks.
- **Attack Steps**: Step 1: Extract signed firmware and locate signature block.Step 2: Modify firmware binary in hex editor.Step 3: Patch or remove the signature verification code.Step 4: Repack firmware and flash it.Step 5: Device loads tampered code.
- **Detection**: Signature verification log
- **Solution**: Use public/private key pairs
- **Tags**: signature, bypass, forgery

## Reversing Sensor Calibration Routines

- **Attack Type**: Firmware Behavior Mapping
- **Target**: Sensor-Driven Device
- **Vulnerability**: No input integrity checks
- **MITRE**: T1565.002: Stored Data Manipulation
- **Impact**: False data leads to bad output
- **Tools**: Ghidra, Oscilloscope
- **Scenario**: Attacker analyzes how firmware calibrates sensor data and manipulates it.
- **Attack Steps**: Step 1: Extract and reverse firmware to locate sensor logic.Step 2: Observe calibration behavior through serial/log.Step 3: Alter input data to observe processing.Step 4: Modify firmware to skip or falsify calibration.Step 5: Use result to trick or confuse target system.
- **Detection**: Data outlier detection
- **Solution**: Validate sensor input range
- **Tags**: calibration, spoofing

## Reversing Touchscreen Controller Firmware

- **Attack Type**: Peripheral Firmware Reverse
- **Target**: Mobile Device
- **Vulnerability**: Writable peripheral firmware
- **MITRE**: T1600.002: Component Firmware
- **Impact**: Unauthorized input injection
- **Tools**: Firmware dump tools, Logic analyzer, Ghidra
- **Scenario**: Attacker analyzes the firmware in touch controller IC to inject gesture commands.
- **Attack Steps**: Step 1: Identify touchscreen controller on PCB.Step 2: Extract firmware using test clip and reader.Step 3: Use Ghidra to reverse engineer the firmware logic.Step 4: Modify gestures or inputs at firmware level.Step 5: Flash modified firmware to inject inputs.
- **Detection**: Monitor unexpected gestures
- **Solution**: Secure firmware update & verify
- **Tags**: touchscreen, gesture, injection

## Reversing LED Controller Firmware

- **Attack Type**: Low-Level Hardware Logic Mapping
- **Target**: LED Strip Controller
- **Vulnerability**: Firmware allows reprogramming
- **MITRE**: T1001.001: Data Encoding
- **Impact**: Data exfiltration via light
- **Tools**: Firmware tools, Oscilloscope
- **Scenario**: Attacker modifies firmware of LED controller to embed blinking signals as covert channel.
- **Attack Steps**: Step 1: Dump LED controller firmware using clip or SWD.Step 2: Analyze binary to find LED toggle code.Step 3: Modify timing or insert Morse-code style blinking.Step 4: Reflash controller.Step 5: LED blinks secret messages.
- **Detection**: Optical behavior anomalies
- **Solution**: Verify firmware hash on boot
- **Tags**: led, covert, blink

## Cloning Wi-Fi Chipset Firmware

- **Attack Type**: Wireless Stack Duplication
- **Target**: IoT Device
- **Vulnerability**: No unique firmware binding
- **MITRE**: T1606: Forge Device Identity
- **Impact**: Device spoofing on network
- **Tools**: Flash reader, Ghidra
- **Scenario**: Attacker dumps and clones Wi-Fi chipset firmware to emulate device behavior.
- **Attack Steps**: Step 1: Disassemble Wi-Fi chipset board.Step 2: Locate and read firmware chip (e.g., SPI flash).Step 3: Dump firmware and analyze for MAC address or stack.Step 4: Flash to another Wi-Fi module.Step 5: Clone now behaves as original device.
- **Detection**: MAC address duplication alert
- **Solution**: Bind firmware to chip IDs
- **Tags**: wifi, clone, spoof

## Identifying Sensor Drivers in Firmware

- **Attack Type**: Driver Mapping
- **Target**: Industrial Sensor
- **Vulnerability**: Drivers not obfuscated
- **MITRE**: T1602.001: Sensor Manipulation
- **Impact**: Spoof or mimic sensor behavior
- **Tools**: Ghidra, Firmware dump, PulseView
- **Scenario**: Attacker extracts and maps driver code to understand sensor operation.
- **Attack Steps**: Step 1: Extract firmware from sensor device.Step 2: Search for driver code regions related to I2C or SPI calls.Step 3: Analyze routines to reverse sensor timing and control.Step 4: Simulate sensor behavior externally.Step 5: Exploit weaknesses in calibration or logic.
- **Detection**: Sensor data log comparison
- **Solution**: Validate sensor source
- **Tags**: drivers, sensor, spoof

## Injecting Command Execution into Firmware

- **Attack Type**: Firmware Command Injection
- **Target**: Admin Console Device
- **Vulnerability**: No command whitelist
- **MITRE**: T1059: Command Execution
- **Impact**: Undocumented control access
- **Tools**: Ghidra, Firmware Mod Kit
- **Scenario**: Attacker adds hidden command interface in firmware logic.
- **Attack Steps**: Step 1: Analyze firmware to find command parser.Step 2: Add new hidden command (e.g., unlock_all).Step 3: Patch parser to handle and execute command.Step 4: Repack and flash modified firmware.Step 5: Use interface to execute injected command.
- **Detection**: Monitor command logs
- **Solution**: Whitelist only allowed commands
- **Tags**: command, inject, parser

## Reconstructing File System from NAND Dump

- **Attack Type**: File System Reconstruction
- **Target**: Linux-based IoT Device
- **Vulnerability**: NAND not encrypted
- **MITRE**: T1005: Local Data Access
- **Impact**: Full OS layer extracted
- **Tools**: Binwalk, UBIReader, Flash reader
- **Scenario**: Attacker reads and reconstructs full Linux file system from raw NAND firmware.
- **Attack Steps**: Step 1: Dump raw NAND firmware using desolder and reader.Step 2: Use UBIReader or binwalk to mount file system.Step 3: Browse directories, extract files.Step 4: Find root passwords, logs, configs.Step 5: Use findings for access or cloning.
- **Detection**: NAND hash comparison
- **Solution**: Encrypt NAND FS and mount with key
- **Tags**: fs, ubi, dump, extract

## Modifying Firmware Update Server URL

- **Attack Type**: Update Redirection Attack
- **Target**: IoT Device
- **Vulnerability**: Hardcoded update path
- **MITRE**: T1565.001: Firmware Manipulation
- **Impact**: Persistent backdoor injection
- **Tools**: Binwalk, Hex Editor
- **Scenario**: Attacker edits firmware to change official update server URL to malicious one.
- **Attack Steps**: Step 1: Extract firmware image using previous methods.Step 2: Search for known update server URLs in string section.Step 3: Replace with attacker-controlled domain.Step 4: Repack and flash firmware.Step 5: Device contacts malicious server for updates.
- **Detection**: Network anomaly detection
- **Solution**: Validate firmware origin via DNS pinning
- **Tags**: update, firmware, redirect

## Office Laptop Theft by Janitor

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Corporate Laptop
- **Vulnerability**: Unattended hardware, poor access control
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Data Theft
- **Tools**: Screwdriver, USB stick
- **Scenario**: A janitor with access to the office steals an unattended laptop after hours to extract sensitive files.
- **Attack Steps**: Step 1: Insider observes unattended laptops during cleaning time. Step 2: Waits until office is empty. Step 3: Unplugs and hides laptop in cleaning trolley. Step 4: Takes it home and extracts files using USB stick.
- **Detection**: Physical inventory audit, CCTV
- **Solution**: Lock away unattended devices; enforce clean desk policy
- **Tags**: laptop, insider, theft, janitor

## Plugging Malicious USB During Office Visit

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Desktop PC
- **Vulnerability**: USB Auto-Run Enabled
- **MITRE**: T1204 (User Execution)
- **Impact**: Malware Infection
- **Tools**: Malicious USB payload (Rubber Ducky or similar)
- **Scenario**: An employee pretends to "charge phone" but secretly plugs a malicious USB into a company system to infect it.
- **Attack Steps**: Step 1: Insider enters with USB in disguise as a charger. Step 2: Claims device needs charging. Step 3: Inserts USB into unattended desktop. Step 4: USB auto-runs a script to steal files or create a backdoor.
- **Detection**: USB monitoring logs, security camera
- **Solution**: Disable USB ports or restrict access
- **Tags**: usb, insider, payload, rubber ducky

## Access Badge Sharing to External Attacker

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Network Room
- **Vulnerability**: Lack of visitor tracking
- **MITRE**: T1071 (Application Layer Protocol)
- **Impact**: Surveillance, IP Theft
- **Tools**: Employee badge, small camera, microphone
- **Scenario**: An insider shares their ID badge with a friend who enters the facility and installs spying devices.
- **Attack Steps**: Step 1: Insider gives badge to external friend. Step 2: Friend enters office as a fake visitor. Step 3: Installs hidden mic under a desk and mini camera above a cabinet. Step 4: Leaves undetected with badge returned.
- **Detection**: Badge logs, physical sweep
- **Solution**: Implement biometric + RFID and visitor escort policy
- **Tags**: surveillance, badge abuse, visitor attack

## Insider Installs Hidden Wi-Fi Camera

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Server Room
- **Vulnerability**: Lack of visual inspection
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Surveillance, Insider Monitoring
- **Tools**: Mini spy cam, power bank
- **Scenario**: An employee hides a mini Wi-Fi camera in the server room to spy on access patterns.
- **Attack Steps**: Step 1: Insider brings camera hidden in a tissue box. Step 2: Places it near server racks. Step 3: Connects to mobile hotspot or internal Wi-Fi. Step 4: Streams video to remote device.
- **Detection**: Radio frequency scans, physical sweep
- **Solution**: Ban personal items, routine physical checks
- **Tags**: spycam, server room, insider espionage

## Insider Allows Attacker to Clone Access Card

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: RFID Access Entry
- **Vulnerability**: No anti-cloning protection
- **MITRE**: T1078 (Valid Accounts)
- **Impact**: Physical Breach
- **Tools**: RFID reader/cloner (Proxmark3)
- **Scenario**: Insider hands over access card to a third-party briefly for RFID cloning.
- **Attack Steps**: Step 1: Insider lends access card to friend at a cafe. Step 2: Friend scans card using RFID cloner. Step 3: Duplicates card within minutes. Step 4: Uses clone to enter restricted office later.
- **Detection**: Monitor RFID logs, detect duplicate IDs
- **Solution**: Use encrypted RFID and anti-clone tech
- **Tags**: RFID, access card clone, insider

## Insider Installs Rogue Device Inside Printer

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Printer
- **Vulnerability**: Unsecured internal ports
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Data Leakage
- **Tools**: Raspberry Pi, micro USB cable
- **Scenario**: Insider opens office printer and installs a Raspberry Pi to intercept scanned documents.
- **Attack Steps**: Step 1: Opens side panel of shared printer. Step 2: Connects Pi between network cable and printer board. Step 3: Device stores or forwards data. Step 4: Insider accesses logs remotely.
- **Detection**: Monitor unusual traffic, scan ports
- **Solution**: Lock printer access, tamper seals
- **Tags**: printer, raspberry pi, rogue device

## Insider Takes Photo of Confidential Screen

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Desktop Monitor
- **Vulnerability**: Shoulder surfing
- **MITRE**: T1110.003 (Credential Dumping)
- **Impact**: IP Leak, Data Theft
- **Tools**: Smartphone
- **Scenario**: A trusted staff member quietly photographs confidential emails from another employee’s screen.
- **Attack Steps**: Step 1: Walks behind employee. Step 2: Pretends to use phone. Step 3: Takes silent photo of screen showing sensitive data. Step 4: Emails photo to outside contact.
- **Detection**: Screen filters, CCTV
- **Solution**: Use privacy filters, desk privacy zones
- **Tags**: shoulder surfing, screen spy, insider

## Insider Swaps Office Mouse with Malicious One

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Employee Workstation
- **Vulnerability**: USB trust assumptions
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Keystroke Theft
- **Tools**: Modified USB mouse with keylogger
- **Scenario**: Insider brings a lookalike USB mouse with malware and swaps it during lunch break.
- **Attack Steps**: Step 1: Insider brings identical mouse. Step 2: Waits for user to leave desk. Step 3: Swaps mouse silently. Step 4: Mouse logs input and sends via Wi-Fi.
- **Detection**: USB scan, device ID logging
- **Solution**: Mark devices, port restrictions
- **Tags**: usb mouse, swap attack, insider

## Insider Uses Maintenance Access to Drop Beacon

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Building Infrastructure
- **Vulnerability**: Blind spot in ceiling inspection
- **MITRE**: T1132 (Data Encoding)
- **Impact**: Location Tracking, Breach Timing
- **Tools**: BLE Beacon (Tile, AirTag), double-sided tape
- **Scenario**: Insider enters HVAC duct area during scheduled maintenance and drops a BLE beacon for internal tracking.
- **Attack Steps**: Step 1: Insider accesses HVAC area during work. Step 2: Tapes beacon near network cables or ceiling. Step 3: Beacon transmits location or pings insider's phone. Step 4: Used to track movement or trigger malware.
- **Detection**: RF detection, mobile app scans
- **Solution**: Ban personal trackers, conduct ceiling sweeps
- **Tags**: BLE, beacon, insider maintenance

## Insider Hides MicroSD Sniffer in Keyboard

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Desktop Workstation
- **Vulnerability**: No inventory tracking
- **MITRE**: T1056.001 (Keylogging)
- **Impact**: Credential/Info Theft
- **Tools**: MicroSD logger, modified keyboard
- **Scenario**: A MicroSD logger is secretly installed in a keyboard to capture keystrokes and store them offline.
- **Attack Steps**: Step 1: Insider modifies a keyboard at home. Step 2: Brings it into office in a bag. Step 3: Swaps with real keyboard during off-hours. Step 4: Retrieves it after collecting data.
- **Detection**: Input device scanning, usage logs
- **Solution**: Secure hardware inventory
- **Tags**: keylogger, MicroSD, insider keyboard

## Insider Disables Security Camera by Unplugging

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Surveillance
- **Vulnerability**: Unsecured camera cables
- **MITRE**: T1562.001 (Disable Security Tools)
- **Impact**: No evidence/log gaps
- **Tools**: None (just unplugging)
- **Scenario**: An insider unplugs a security camera briefly to perform malicious activity off-record.
- **Attack Steps**: Step 1: Insider identifies a blind spot near camera wiring. Step 2: During night shift, unplugs the camera. Step 3: Performs unauthorized actions like accessing server. Step 4: Reconnects camera.
- **Detection**: Missing footage detection
- **Solution**: Secure camera wires, alerts on disconnect
- **Tags**: camera unplug, surveillance bypass

## Insider Leaks Blueprints via Scanned Document

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Scanner
- **Vulnerability**: No email/data DLP
- **MITRE**: T1081 (Credentials in Files)
- **Impact**: IP/Data Leak
- **Tools**: Scanner, email client
- **Scenario**: Insider scans confidential blueprints using office scanner and emails them out.
- **Attack Steps**: Step 1: Insider brings blueprint to office scanner. Step 2: Scans and saves file to PC. Step 3: Attaches file to personal email. Step 4: Sends to third party or cloud drive.
- **Detection**: Email DLP, scan audit logs
- **Solution**: Restrict email access, DLP software
- **Tags**: blueprint leak, insider, scan misuse

## Insider Uses Office Lockbox to Store Spy Tools

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Storage/Lockers
- **Vulnerability**: Lack of locker audits
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Espionage / Persistent Access
- **Tools**: USB drop tools, spy cam, BLE beacons
- **Scenario**: Insider hides spy gadgets inside shared office lockers for use during night shift.
- **Attack Steps**: Step 1: Brings tools during regular hours. Step 2: Stores them inside office cabinet or locker. Step 3: Uses them during night shift to carry out spying. Step 4: Returns them or hides again.
- **Detection**: Physical sweep, locker logs
- **Solution**: Restrict locker access, audit policies
- **Tags**: insider locker, spy gadgets, persistence

## Insider Alters Firmware of Display Screens

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Display Device
- **Vulnerability**: No firmware auth control
- **MITRE**: T1542.001 (Firmware Modification)
- **Impact**: Misinformation or exfiltration
- **Tools**: Firmware flasher, USB, laptop
- **Scenario**: Insider injects malicious firmware into an office screen used for display or digital signage.
- **Attack Steps**: Step 1: During maintenance, connects USB flasher to screen. Step 2: Loads custom firmware. Step 3: Screen now displays false data or sends info to attacker. Step 4: Firmware remains persistent.
- **Detection**: Monitor screen behavior, firmware checks
- **Solution**: Use signed firmware, restrict updates
- **Tags**: firmware attack, signage screen, insider

## Insider Installs Keypad Camera in Server Room

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Server Room Door
- **Vulnerability**: Blind spots, uninspected entry
- **MITRE**: T1056 (Input Capture)
- **Impact**: Door PIN Theft, Access Gained
- **Tools**: Mini camera, adhesive
- **Scenario**: An insider secretly mounts a micro camera above a keypad to capture entry PIN codes.
- **Attack Steps**: Step 1: Attaches camera above keypad entrance using tape. Step 2: Ensures view of PIN pad. Step 3: Records entries over days. Step 4: Retrieves video or streams it remotely.
- **Detection**: Camera sweep, motion sensors
- **Solution**: Shield keypads, inspect surroundings
- **Tags**: pin camera, keypad spy, insider access

## Insider Distributes Malicious USB via Reception Bowl

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Desktops
- **Vulnerability**: Human curiosity, no USB control
- **MITRE**: T1204.002 (Malicious File)
- **Impact**: Malware Infection
- **Tools**: USB drives with payload
- **Scenario**: Insider places USB sticks loaded with malware in a giveaway bowl at reception.
- **Attack Steps**: Step 1: Loads malware onto several USBs. Step 2: Labels as "Free Storage Drives". Step 3: Places them at reception area. Step 4: Curious staff plug into PCs. Malware activates.
- **Detection**: Endpoint protection, behavior alerts
- **Solution**: Educate staff, disable USB ports
- **Tags**: usb bait, giveaway, insider seeding

## Insider Enables Remote SSH Access on Printer

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Printer
- **Vulnerability**: Default credentials, no monitoring
- **MITRE**: T1021.004 (SSH)
- **Impact**: Persistent Remote Access
- **Tools**: SSH script, terminal, printer interface
- **Scenario**: Insider enables SSH on the office printer and adds a reverse shell script.
- **Attack Steps**: Step 1: Logs into printer admin page. Step 2: Enables SSH or Telnet. Step 3: Uploads a script that connects back to attacker's PC. Step 4: Uses it for future remote access.
- **Detection**: Monitor config changes
- **Solution**: Change defaults, restrict web access
- **Tags**: insider, printer ssh, reverse shell

## Insider Shares Floor Plan for Physical Bypass

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Facility
- **Vulnerability**: No policy on physical info
- **MITRE**: T1081 (Credential / Info Exposure)
- **Impact**: Targeted Intrusion
- **Tools**: Camera/phone
- **Scenario**: Insider leaks detailed office floor plan to outsider for planning a break-in.
- **Attack Steps**: Step 1: Clicks photo of floor plan from wall/desk. Step 2: Sends it via personal phone to third-party. Step 3: Attacker uses it to locate server room or blind spots. Step 4: Uses knowledge for intrusion.
- **Detection**: Limit document access
- **Solution**: Remove public floor plans
- **Tags**: insider blueprint, floorplan exposure

## Insider Hides Mobile Hotspot in Ceiling

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Network
- **Vulnerability**: No wireless monitoring
- **MITRE**: T1133 (External Remote Services)
- **Impact**: Wireless Breach
- **Tools**: Mobile hotspot, battery pack
- **Scenario**: Insider hides a mobile Wi-Fi hotspot in ceiling tiles to provide remote access to attackers.
- **Attack Steps**: Step 1: Insider brings hotspot during lunch. Step 2: Opens ceiling tile in meeting room. Step 3: Places hotspot with battery. Step 4: External attacker connects to it from outside.
- **Detection**: Wi-Fi scan, physical inspection
- **Solution**: RF detection, restrict ceiling access
- **Tags**: rogue hotspot, ceiling hack

## Insider Uses Voice Assistant to Trigger Commands

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Smart Devices
- **Vulnerability**: Unrestricted voice access
- **MITRE**: T1010 (Application Window Discovery)
- **Impact**: Voice Command Exploit
- **Tools**: Voice assistant, smartphone
- **Scenario**: Insider exploits always-on voice assistants (Alexa, Google Home) to run malicious commands.
- **Attack Steps**: Step 1: Waits for area to be empty. Step 2: Says voice command: “Send email to…”, “Unlock door” etc. Step 3: Device executes it due to poor config. Step 4: Logs/data are transmitted.
- **Detection**: Audio log review
- **Solution**: Disable voice triggers or lock them
- **Tags**: smart device, voice hack, insider

## Insider Installs Covert LTE Router

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Office Network
- **Vulnerability**: No rogue device detection
- **MITRE**: T1090.001 (Internal Proxy)
- **Impact**: Data Exfiltration
- **Tools**: LTE Wi-Fi router
- **Scenario**: Insider connects an LTE router to office network to tunnel data out bypassing firewall.
- **Attack Steps**: Step 1: Brings small 4G router. Step 2: Plugs into network switch in unattended area. Step 3: Routes internal traffic via mobile network. Step 4: Attacker connects via LTE.
- **Detection**: Rogue device detection, netflow logs
- **Solution**: Network NAC, physical audits
- **Tags**: LTE, rogue router, bypass

## Insider Uses Document Shred Bin to Hide Devices

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Document Disposal Area
- **Vulnerability**: No physical check
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Covert Persistence
- **Tools**: USB drop device (Rubber Ducky)
- **Scenario**: Insider hides a USB drop device in locked shred bin assuming no one checks inside.
- **Attack Steps**: Step 1: Drops device inside bottom of shred bin. Step 2: Retrieves it later after installing spyware. Step 3: Uses access gained to exfiltrate data. Step 4: Leaves no trace.
- **Detection**: Sweep shred bins, physical inspections
- **Solution**: Secure shredding procedures
- **Tags**: shred bin, stealth, insider

## Insider Taps Audio Line in Conference Phone

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Conference Equipment
- **Vulnerability**: No tamper detection
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Call Eavesdropping
- **Tools**: Line tap tool, soldering gear
- **Scenario**: Insider opens office conference phone and adds a line tap to monitor calls.
- **Attack Steps**: Step 1: Unscrews conference phone during non-use. Step 2: Installs tap between mic and circuit. Step 3: Re-assembles device. Step 4: Monitors calls via external receiver.
- **Detection**: Monitor conference call metadata
- **Solution**: Tamper-proof phone gear
- **Tags**: conference tap, insider bug

## Insider Loops CCTV Footage via HDMI Splitter

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Security DVR / CCTV
- **Vulnerability**: No real-time verification
- **MITRE**: T1562.001 (Disable Security Tools)
- **Impact**: Camera Loop Attack
- **Tools**: HDMI loop kit
- **Scenario**: Insider connects a looping HDMI splitter to play old CCTV footage while performing malicious acts.
- **Attack Steps**: Step 1: Connects splitter to DVR/CCTV. Step 2: Plays recorded footage of empty room. Step 3: Performs activity (e.g. file theft) unseen. Step 4: Removes device.
- **Detection**: Sync camera logs, timestamp check
- **Solution**: Secure DVR, tamper-proof HDMI
- **Tags**: cctv loop, dvr spoof, insider

## Insider Drops Beacon in CEO's Bag for Tracking

- **Attack Type**: Insider-Enabled Physical Access
- **Target**: Executive Personnel
- **Vulnerability**: No device scans
- **MITRE**: T1020.001 (Automated Exfiltration)
- **Impact**: Location Espionage
- **Tools**: Apple AirTag / Tile
- **Scenario**: Insider secretly hides an AirTag in a VIP’s bag to track movements outside the office.
- **Attack Steps**: Step 1: Drops device in side pouch of CEO’s bag. Step 2: Tracks real-time location via mobile app. Step 3: Uses data for extortion or espionage. Step 4: Retrieves or lets device run out.
- **Detection**: Scan for Bluetooth devices
- **Solution**: Alert-based beacon scanners
- **Tags**: tracking tag, air tag, insider spy

