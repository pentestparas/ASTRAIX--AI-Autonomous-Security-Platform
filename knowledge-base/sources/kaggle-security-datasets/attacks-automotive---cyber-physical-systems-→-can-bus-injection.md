# Automotive / Cyber-Physical Systems → CAN Bus Injection Attacks

## Replay Door Unlock via CAN

- **Attack Type**: Replay Attack
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of encryption/authentication in CAN messages
- **MITRE**: T1642
- **Impact**: Unauthorized physical access
- **Tools**: CANtact, ICSim, SavvyCAN
- **Scenario**: Attacker captures a legitimate CAN message to unlock vehicle doors, then replays it using an injection tool.
- **Attack Steps**: 1. Connect CANtact to the OBD-II port of the target car. 2. Use SavvyCAN to monitor and capture CAN messages during legitimate door unlock operation. 3. Identify the specific CAN ID and data bytes responsible for unlocking. 4. Replay the captured message using ICSim or socketCAN utilities. 5. Observe if doors unlock without physical key/fob.
- **Detection**: Log CAN traffic, monitor replay patterns
- **Solution**: Encrypt or authenticate messages, gateway filtering
- **Tags**: replay attack, CAN injection, automotive

## Fuzz CAN Messages to Crash Dashboard

- **Attack Type**: Fuzzing
- **Target**: Dashboard ECU
- **Vulnerability**: Poor input validation in ECU firmware
- **MITRE**: T0813
- **Impact**: ECU instability or denial of visuals
- **Tools**: CANFuzz, ICSim, SocketCAN
- **Scenario**: Randomized CAN messages are sent to discover a crash condition in the vehicle's digital dashboard.
- **Attack Steps**: 1. Connect CANFuzz to the OBD-II port of a test vehicle or simulator. 2. Generate a wide range of random or malformed CAN frames. 3. Monitor the dashboard cluster for crashes, restarts, or freezing. 4. Log crash conditions to determine vulnerabilities in ECU firmware. 5. Recreate specific fuzzing sequences to identify responsible patterns.
- **Detection**: Log kernel/crash dumps from ECU
- **Solution**: Harden ECU firmware, input validation
- **Tags**: CANFuzz, dashboard crash, ECU

## Spoof Engine RPM Readings

- **Attack Type**: Spoofing
- **Target**: Dashboard ECU
- **Vulnerability**: No message authentication between ECUs
- **MITRE**: T1642
- **Impact**: Driver deception or distraction
- **Tools**: ICSim, SocketCAN, Python-CAN
- **Scenario**: An attacker injects fake engine RPM messages to the dashboard to mislead the driver.
- **Attack Steps**: 1. Tap into vehicle’s CAN bus using USB2CAN adapter. 2. Monitor real engine RPM values using ICSim. 3. Craft spoofed messages with fake high or low RPM values. 4. Inject the spoofed packets at a high frequency to override real data. 5. Observe manipulated RPM on the dashboard.
- **Detection**: Compare real sensor output with bus traffic
- **Solution**: Message signing between ECUs
- **Tags**: spoofing, RPM, CAN, automotive

## Disable Brake Lights via CAN

- **Attack Type**: Spoofing
- **Target**: Lighting Control ECU
- **Vulnerability**: Unauthenticated broadcast control
- **MITRE**: T0813
- **Impact**: Road safety hazard
- **Tools**: CANToolz, SocketCAN, USB2CAN
- **Scenario**: By injecting crafted messages, attacker suppresses the signal to brake light module.
- **Attack Steps**: 1. Connect to CAN using USB2CAN adapter. 2. Use CANToolz to monitor normal brake light signals. 3. Determine the CAN ID and pattern used for brake activation. 4. Inject neutral or invalid data on the same CAN ID at high frequency. 5. Confirm that brake lights no longer illuminate.
- **Detection**: Compare light ECU inputs with real pedal actions
- **Solution**: Secure CAN IDs, validate physical input
- **Tags**: brake spoofing, ECU, lighting

## Reboot Infotainment via CAN Injection

- **Attack Type**: Fuzzing
- **Target**: Infotainment ECU
- **Vulnerability**: Improper error handling
- **MITRE**: T0813
- **Impact**: Denial of media/UX functions
- **Tools**: CANFuzz, ICSim
- **Scenario**: Infotainment system is rebooted repeatedly using malformed CAN frames.
- **Attack Steps**: 1. Hook CANFuzz into test vehicle bus. 2. Fuzz messages with corrupted payload targeting infotainment CAN IDs. 3. Observe for abnormal behavior like rebooting, freezing. 4. Narrow down fuzz set to isolate triggering messages. 5. Attempt reliable reproduction to confirm vulnerability.
- **Detection**: Monitor infotainment logs and restarts
- **Solution**: Input validation, ECU firmware patch
- **Tags**: infotainment, crash, CAN fuzz

## Replay Throttle Acceleration

- **Attack Type**: Replay Attack
- **Target**: Powertrain ECU
- **Vulnerability**: Lack of throttle command validation
- **MITRE**: T1642
- **Impact**: Unintended acceleration
- **Tools**: ICSim, SavvyCAN
- **Scenario**: Attacker records and replays throttle input messages to simulate unintended acceleration.
- **Attack Steps**: 1. Connect to CAN bus via ICSim. 2. Drive and capture throttle-up sequences using SavvyCAN. 3. Identify throttle command message structure. 4. Replay sequence while vehicle is stationary. 5. Observe engine revving or vehicle movement.
- **Detection**: Anomaly-based sensor fusion
- **Solution**: Redundant sensor validation
- **Tags**: throttle spoof, CAN replay

## Overwrite Gear Position via CAN

- **Attack Type**: Spoofing
- **Target**: Transmission ECU
- **Vulnerability**: Unverified gear signals
- **MITRE**: T0813
- **Impact**: Safety risk, shifting logic errors
- **Tools**: CANToolz, Python-CAN
- **Scenario**: Gear position data is forged and injected into the CAN bus to mislead driver or system.
- **Attack Steps**: 1. Connect to vehicle CAN using USB2CAN. 2. Log gear change messages. 3. Forge messages indicating reverse or drive mode. 4. Inject during system idle to confuse onboard logic. 5. Validate gear indicator mismatch or ECU error.
- **Detection**: Gear sensor comparison
- **Solution**: Lock critical gear messages to origin ECU
- **Tags**: gear spoof, transmission, CAN

## Continuous CAN Flooding Attack

- **Attack Type**: Denial-of-Service
- **Target**: Whole Vehicle Bus
- **Vulnerability**: No rate limiting in CAN protocol
- **MITRE**: T0813
- **Impact**: Vehicle instability or failure
- **Tools**: SocketCAN, Python-CAN
- **Scenario**: Flooding the CAN bus with junk data to overload ECU processors and slow communication.
- **Attack Steps**: 1. Connect laptop via CAN adapter. 2. Write a Python-CAN script to generate arbitrary frames at max rate. 3. Start flooding attack. 4. Observe system lag, component timeout, or ECU crashes. 5. Use logs to assess which ECUs failed first.
- **Detection**: Detect excessive message frequency
- **Solution**: Implement gateway rate control
- **Tags**: CAN flooding, DoS, ECU

## Hijack Steering via Spoofed Packets

- **Attack Type**: Spoofing
- **Target**: Steering ECU
- **Vulnerability**: Trust between ECUs
- **MITRE**: T1642
- **Impact**: Loss of directional control
- **Tools**: ICSim, SocketCAN
- **Scenario**: Fake steering angle messages override real input in drive-by-wire systems.
- **Attack Steps**: 1. Identify steering control messages. 2. Capture steering angle from legit driving. 3. Craft spoofed messages with abnormal angles. 4. Inject messages at priority to overtake real data. 5. Observe deviation or override.
- **Detection**: Compare physical sensor and CAN data
- **Solution**: Authenticate actuator signals
- **Tags**: steering spoof, CAN attack

## Induce ABS Fault with Random Frames

- **Attack Type**: Fuzzing
- **Target**: ABS ECU
- **Vulnerability**: No sanity checks in ABS comms
- **MITRE**: T0813
- **Impact**: Reduced braking performance
- **Tools**: CANFuzz, SocketCAN
- **Scenario**: Random frame injection causes the ABS ECU to enter fault or limp mode.
- **Attack Steps**: 1. Use CANFuzz to generate and inject random messages. 2. Monitor ABS dashboard light and logs. 3. Identify crash-inducing message patterns. 4. Confirm fault state via OBD-II diagnostic. 5. Reproduce to validate finding.
- **Detection**: Real-time fault logs from ABS
- **Solution**: Input validation and ECU hardening
- **Tags**: ABS, fuzz, CAN injection

## Replay Door Unlock via CAN

- **Attack Type**: Replay Attack
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of encryption/authentication in CAN messages
- **MITRE**: T1642
- **Impact**: Unauthorized physical access
- **Tools**: CANtact, ICSim, SavvyCAN
- **Scenario**: Attacker captures a legitimate CAN message to unlock vehicle doors, then replays it using an injection tool.
- **Attack Steps**: 1. Connect CANtact to the OBD-II port of the target car. 2. Use SavvyCAN to monitor and capture CAN messages during legitimate door unlock operation. 3. Identify the specific CAN ID and data bytes responsible for unlocking. 4. Replay the captured message using ICSim or socketCAN utilities. 5. Observe if doors unlock without physical key/fob.
- **Detection**: Log CAN traffic, monitor replay patterns
- **Solution**: Encrypt or authenticate messages, gateway filtering
- **Tags**: replay attack, CAN injection, automotive

## Fuzz CAN Messages to Crash Dashboard

- **Attack Type**: Fuzzing
- **Target**: Dashboard ECU
- **Vulnerability**: Poor input validation in ECU firmware
- **MITRE**: T0813
- **Impact**: ECU instability or denial of visuals
- **Tools**: CANFuzz, ICSim, SocketCAN
- **Scenario**: Randomized CAN messages are sent to discover a crash condition in the vehicle's digital dashboard.
- **Attack Steps**: 1. Connect CANFuzz to the OBD-II port of a test vehicle or simulator. 2. Generate a wide range of random or malformed CAN frames. 3. Monitor the dashboard cluster for crashes, restarts, or freezing. 4. Log crash conditions to determine vulnerabilities in ECU firmware. 5. Recreate specific fuzzing sequences to identify responsible patterns.
- **Detection**: Log kernel/crash dumps from ECU
- **Solution**: Harden ECU firmware, input validation
- **Tags**: CANFuzz, dashboard crash, ECU

## Spoof Engine RPM Readings

- **Attack Type**: Spoofing
- **Target**: Dashboard ECU
- **Vulnerability**: No message authentication between ECUs
- **MITRE**: T1642
- **Impact**: Driver deception or distraction
- **Tools**: ICSim, SocketCAN, Python-CAN
- **Scenario**: An attacker injects fake engine RPM messages to the dashboard to mislead the driver.
- **Attack Steps**: 1. Tap into vehicle’s CAN bus using USB2CAN adapter. 2. Monitor real engine RPM values using ICSim. 3. Craft spoofed messages with fake high or low RPM values. 4. Inject the spoofed packets at a high frequency to override real data. 5. Observe manipulated RPM on the dashboard.
- **Detection**: Compare real sensor output with bus traffic
- **Solution**: Message signing between ECUs
- **Tags**: spoofing, RPM, CAN, automotive

## Disable Brake Lights via CAN

- **Attack Type**: Spoofing
- **Target**: Lighting Control ECU
- **Vulnerability**: Unauthenticated broadcast control
- **MITRE**: T0813
- **Impact**: Road safety hazard
- **Tools**: CANToolz, SocketCAN, USB2CAN
- **Scenario**: By injecting crafted messages, attacker suppresses the signal to brake light module.
- **Attack Steps**: 1. Connect to CAN using USB2CAN adapter. 2. Use CANToolz to monitor normal brake light signals. 3. Determine the CAN ID and pattern used for brake activation. 4. Inject neutral or invalid data on the same CAN ID at high frequency. 5. Confirm that brake lights no longer illuminate.
- **Detection**: Compare light ECU inputs with real pedal actions
- **Solution**: Secure CAN IDs, validate physical input
- **Tags**: brake spoofing, ECU, lighting

## Reboot Infotainment via CAN Injection

- **Attack Type**: Fuzzing
- **Target**: Infotainment ECU
- **Vulnerability**: Improper error handling
- **MITRE**: T0813
- **Impact**: Denial of media/UX functions
- **Tools**: CANFuzz, ICSim
- **Scenario**: Infotainment system is rebooted repeatedly using malformed CAN frames.
- **Attack Steps**: 1. Hook CANFuzz into test vehicle bus. 2. Fuzz messages with corrupted payload targeting infotainment CAN IDs. 3. Observe for abnormal behavior like rebooting, freezing. 4. Narrow down fuzz set to isolate triggering messages. 5. Attempt reliable reproduction to confirm vulnerability.
- **Detection**: Monitor infotainment logs and restarts
- **Solution**: Input validation, ECU firmware patch
- **Tags**: infotainment, crash, CAN fuzz

## Replay Throttle Acceleration

- **Attack Type**: Replay Attack
- **Target**: Powertrain ECU
- **Vulnerability**: Lack of throttle command validation
- **MITRE**: T1642
- **Impact**: Unintended acceleration
- **Tools**: ICSim, SavvyCAN
- **Scenario**: Attacker records and replays throttle input messages to simulate unintended acceleration.
- **Attack Steps**: 1. Connect to CAN bus via ICSim. 2. Drive and capture throttle-up sequences using SavvyCAN. 3. Identify throttle command message structure. 4. Replay sequence while vehicle is stationary. 5. Observe engine revving or vehicle movement.
- **Detection**: Anomaly-based sensor fusion
- **Solution**: Redundant sensor validation
- **Tags**: throttle spoof, CAN replay

## Overwrite Gear Position via CAN

- **Attack Type**: Spoofing
- **Target**: Transmission ECU
- **Vulnerability**: Unverified gear signals
- **MITRE**: T0813
- **Impact**: Safety risk, shifting logic errors
- **Tools**: CANToolz, Python-CAN
- **Scenario**: Gear position data is forged and injected into the CAN bus to mislead driver or system.
- **Attack Steps**: 1. Connect to vehicle CAN using USB2CAN. 2. Log gear change messages. 3. Forge messages indicating reverse or drive mode. 4. Inject during system idle to confuse onboard logic. 5. Validate gear indicator mismatch or ECU error.
- **Detection**: Gear sensor comparison
- **Solution**: Lock critical gear messages to origin ECU
- **Tags**: gear spoof, transmission, CAN

## Continuous CAN Flooding Attack

- **Attack Type**: Denial-of-Service
- **Target**: Whole Vehicle Bus
- **Vulnerability**: No rate limiting in CAN protocol
- **MITRE**: T0813
- **Impact**: Vehicle instability or failure
- **Tools**: SocketCAN, Python-CAN
- **Scenario**: Flooding the CAN bus with junk data to overload ECU processors and slow communication.
- **Attack Steps**: 1. Connect laptop via CAN adapter. 2. Write a Python-CAN script to generate arbitrary frames at max rate. 3. Start flooding attack. 4. Observe system lag, component timeout, or ECU crashes. 5. Use logs to assess which ECUs failed first.
- **Detection**: Detect excessive message frequency
- **Solution**: Implement gateway rate control
- **Tags**: CAN flooding, DoS, ECU

## Hijack Steering via Spoofed Packets

- **Attack Type**: Spoofing
- **Target**: Steering ECU
- **Vulnerability**: Trust between ECUs
- **MITRE**: T1642
- **Impact**: Loss of directional control
- **Tools**: ICSim, SocketCAN
- **Scenario**: Fake steering angle messages override real input in drive-by-wire systems.
- **Attack Steps**: 1. Identify steering control messages. 2. Capture steering angle from legit driving. 3. Craft spoofed messages with abnormal angles. 4. Inject messages at priority to overtake real data. 5. Observe deviation or override.
- **Detection**: Compare physical sensor and CAN data
- **Solution**: Authenticate actuator signals
- **Tags**: steering spoof, CAN attack

## Induce ABS Fault with Random Frames

- **Attack Type**: Fuzzing
- **Target**: ABS ECU
- **Vulnerability**: No sanity checks in ABS comms
- **MITRE**: T0813
- **Impact**: Reduced braking performance
- **Tools**: CANFuzz, SocketCAN
- **Scenario**: Random frame injection causes the ABS ECU to enter fault or limp mode.
- **Attack Steps**: 1. Use CANFuzz to generate and inject random messages. 2. Monitor ABS dashboard light and logs. 3. Identify crash-inducing message patterns. 4. Confirm fault state via OBD-II diagnostic. 5. Reproduce to validate finding.
- **Detection**: Real-time fault logs from ABS
- **Solution**: Input validation and ECU hardening
- **Tags**: ABS, fuzz, CAN injection

