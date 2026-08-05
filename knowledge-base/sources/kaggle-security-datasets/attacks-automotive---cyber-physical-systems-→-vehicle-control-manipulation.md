# Automotive / Cyber-Physical Systems → Vehicle Control Manipulation Attacks

## CAN Injection to Simulate Braking

- **Attack Type**: CAN Bus Injection
- **Target**: ECU / CAN Network
- **Vulnerability**: Lack of CAN message authentication
- **MITRE**: T1609 (Command and Control over Vehicle Bus)
- **Impact**: Sudden braking, risk of rear-end collisions
- **Tools**: CANtact, SavvyCAN, ICSim
- **Scenario**: Attacker injects spoofed CAN messages to simulate a brake pedal press without actual driver input
- **Attack Steps**: 1. Connect a CAN interface (e.g., CANtact) to the vehicle’s OBD-II port. 2. Use a sniffer tool like SavvyCAN to log CAN traffic while the brake is pressed. 3. Identify the CAN ID and payload corresponding to brake signal. 4. Replay this message in a loop while the vehicle is moving, causing the ECU to interpret it as a brake input. 5. Monitor driver confusion or automated braking system activation.
- **Detection**: CAN anomaly detection, timestamp mismatch
- **Solution**: Implement message authentication and gateway filtering
- **Tags**: CAN spoofing, Safety-critical, Braking

## Acceleration Spoof via CAN

- **Attack Type**: CAN Message Injection
- **Target**: Powertrain ECU
- **Vulnerability**: Insecure message control via CAN
- **MITRE**: T1609
- **Impact**: Unsafe acceleration, potential crash
- **Tools**: CANBus Triple, Wireshark CAN Plugin
- **Scenario**: Attacker sends fake throttle messages causing sudden acceleration
- **Attack Steps**: 1. Connect CAN injector to vehicle network. 2. Record throttle-related messages during driver acceleration. 3. Identify and modify payload to max throttle value. 4. Replay message repeatedly while parked or idling. 5. Observe engine revving or sudden movement depending on safety interlocks.
- **Detection**: Monitor sudden RPM spikes, throttle logging
- **Solution**: Secure firmware, driver input validation
- **Tags**: CAN, Acceleration, Throttle

## Gear Shift Manipulation

- **Attack Type**: Gear Command Spoofing
- **Target**: Transmission Control Unit
- **Vulnerability**: Unauthenticated control messages
- **MITRE**: T1609
- **Impact**: Risk of transmission damage or accident
- **Tools**: SocketCAN, ICSim
- **Scenario**: Attacker tricks gear control ECU into switching to reverse while moving forward
- **Attack Steps**: 1. Connect to the vehicle’s CAN network. 2. Identify gear shift command CAN IDs by shifting gear during sniffing. 3. Inject reverse gear message while vehicle is moving forward. 4. ECU may reject or accept based on safety controls—older ECUs often lack logic validation.
- **Detection**: ECU diagnostic logs, gear mismatch alerts
- **Solution**: Logic-level safety interlocks, software validation
- **Tags**: Gear spoof, CAN, Transmission

## Fake Fuel Level Display

- **Attack Type**: Cluster Spoofing
- **Target**: Instrument Cluster
- **Vulnerability**: CAN display data tampering
- **MITRE**: T1609
- **Impact**: Deceptive display, safety risk
- **Tools**: CANalyze, Kayak
- **Scenario**: Attacker manipulates CAN to falsely show full or empty fuel tank
- **Attack Steps**: 1. Sniff CAN data while refueling or draining fuel. 2. Log CAN IDs and payloads that update fuel gauge. 3. Replay "full tank" message even when empty. 4. Causes driver to falsely believe enough fuel is present, potentially stranding them.
- **Detection**: Correlate sensor values with gauge
- **Solution**: Data verification from multiple ECUs
- **Tags**: Cluster, Fuel gauge, CAN Injection

## Turn Signal Override

- **Attack Type**: Message Injection
- **Target**: Indicator ECU / Body Control Module
- **Vulnerability**: CAN spoofing
- **MITRE**: T1609
- **Impact**: May cause nearby drivers to react inappropriately
- **Tools**: SavvyCAN, CAN Bus Tools
- **Scenario**: Inject false turn signal activation to confuse other drivers
- **Attack Steps**: 1. Monitor CAN traffic while activating turn signals. 2. Isolate the message responsible for left/right blinker. 3. Inject left-blinker message continuously. 4. Vehicle appears to signal turn even when going straight.
- **Detection**: Signal mismatch analysis
- **Solution**: Cross-check driver inputs
- **Tags**: Signal spoof, CAN trick, Safety hazard

## ABS Sensor Spoofing

- **Attack Type**: Sensor Spoofing via CAN
- **Target**: Brake Controller / ABS ECU
- **Vulnerability**: Sensor signal trust assumptions
- **MITRE**: T1609
- **Impact**: Misleading brake control system
- **Tools**: CANtact Pro, ICSim
- **Scenario**: Fake ABS signals to mislead braking logic
- **Attack Steps**: 1. Capture ABS-related messages during braking. 2. Inject spoofed sensor data suggesting wheel lock. 3. Forces ECU to activate ABS unnecessarily. 4. Repeated misuse can wear brakes or create skid risks.
- **Detection**: ABS module logs and pressure sensor cross-checks
- **Solution**: Multi-sensor validation
- **Tags**: ABS spoof, CAN hack

## Fake Speedometer Readings

- **Attack Type**: Display Tampering
- **Target**: Instrument Cluster
- **Vulnerability**: Insecure CAN message handling
- **MITRE**: T1609
- **Impact**: Legal, safety violations
- **Tools**: ICSim, CANalyze
- **Scenario**: Manipulate speedometer to show false speed values
- **Attack Steps**: 1. Capture real-time speedometer data on CAN bus. 2. Modify value to show much lower speed. 3. Replay modified message continuously. 4. Driver may overspeed unknowingly.
- **Detection**: OBD-based speed validation
- **Solution**: Instrumentation firewall, cross-validation
- **Tags**: Speed spoof, Cluster attack

## Emergency Brake Activation

- **Attack Type**: Command Injection
- **Target**: AEB System, RADAR Sensor
- **Vulnerability**: Sensor spoofing, lack of validation
- **MITRE**: T1609
- **Impact**: Unexpected braking, rear-end collision
- **Tools**: OpenGarages Tools, RADAR Emulator
- **Scenario**: Force emergency brake application by faking obstacle detection
- **Attack Steps**: 1. Emulate a RADAR/LIDAR object ahead using spoofing tools. 2. Trigger automatic emergency braking system (AEB). 3. Vehicle suddenly brakes assuming collision risk.
- **Detection**: Visual sensor verification
- **Solution**: Sensor fusion algorithms
- **Tags**: AEB, RADAR spoofing, Safety

## Wiper System Hijack

- **Attack Type**: CAN Injection
- **Target**: BCM (Body Control Module)
- **Vulnerability**: Command spoofing
- **MITRE**: T1609
- **Impact**: Driver distraction, vision interference
- **Tools**: CAN Bus Tools, Wireshark
- **Scenario**: Randomly activate windshield wipers at high speed
- **Attack Steps**: 1. Record wiper control messages during manual activation. 2. Replay messages repeatedly. 3. Disorients driver, especially in clear weather.
- **Detection**: Compare driver input vs wiper activity
- **Solution**: Driver-verified control relays
- **Tags**: CAN hijack, Wipers, Visual interference

## Lane Keep Assist Spoof

- **Attack Type**: Sensor Injection
- **Target**: Camera-based LKA
- **Vulnerability**: Visual sensor vulnerability
- **MITRE**: T1609
- **Impact**: Unsafe steering changes
- **Tools**: OpenPilot, Fake Road Projection
- **Scenario**: Falsify lane markings to cause steering adjustment
- **Attack Steps**: 1. Use projector or paint to create false lane markings. 2. Vehicle’s camera system interprets markings as legitimate. 3. LKA system activates and adjusts steering incorrectly.
- **Detection**: Driver camera validation, sensor fusion
- **Solution**: AI model hardening, adversarial detection
- **Tags**: LKA spoof, Lane marking attack

