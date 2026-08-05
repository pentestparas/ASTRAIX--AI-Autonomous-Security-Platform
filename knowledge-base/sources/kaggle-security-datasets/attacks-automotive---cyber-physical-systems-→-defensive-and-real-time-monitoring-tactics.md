# Automotive / Cyber-Physical Systems → Defensive & Real-Time Monitoring Tactics Attacks

## Deploy CANShield for ECU Monitoring

- **Attack Type**: Defensive Countermeasure
- **Target**: Automotive Fleet
- **Vulnerability**: CAN Message Injection
- **MITRE**: T0861
- **Impact**: Early Detection of CAN Attacks
- **Tools**: CANShield, Raspberry Pi, SocketCAN
- **Scenario**: A fleet of commercial vehicles integrates CANShield to detect abnormal messages on the CAN bus.
- **Attack Steps**: 1. Install a Raspberry Pi with CAN interface on the vehicle’s OBD-II port. 2. Load CANShield onto the device and configure it to listen passively on the CAN bus. 3. Train the IDS by recording normal traffic over a few days to establish a baseline. 4. Enable detection rules that flag unexpected arbitration IDs or malicious message patterns. 5. Simulate injection of invalid frames to validate alert generation. 6. Use logs to review incidents and escalate to security teams.
- **Detection**: Alerts from CANShield
- **Solution**: Deploy IDS at each endpoint
- **Tags**: #CANIDS #FleetSecurity #CANShield

## Hash Verification on Firmware Boot

- **Attack Type**: Firmware Integrity Verification
- **Target**: Automotive ECU
- **Vulnerability**: Unsigned / Modified Firmware
- **MITRE**: T1601.001
- **Impact**: Block Tampered Firmware Execution
- **Tools**: Secure Bootloader, SHA256, HSM
- **Scenario**: A car manufacturer wants to ensure firmware is not tampered with before booting.
- **Attack Steps**: 1. Modify the bootloader to include a SHA256 hash verification routine. 2. When updating firmware, generate and store hash in a secure HSM or TPM. 3. On vehicle startup, the bootloader computes the hash of loaded firmware. 4. Compare against the trusted hash stored in the secure enclave. 5. If mismatch is found, trigger boot failure and alert the maintenance console. 6. Log verification results for telemetry upload to central server.
- **Detection**: Secure Boot Logs
- **Solution**: Use cryptographic verification on every boot
- **Tags**: #SecureBoot #FirmwareCheck #HSM

## Detect Braking Spoof via Behavioral Model

- **Attack Type**: Anomaly Detection
- **Target**: CAN Bus Signals
- **Vulnerability**: Braking Signal Injection
- **MITRE**: T0883
- **Impact**: Detect Control Manipulation
- **Tools**: TensorFlow, Keras, CAN Decoder
- **Scenario**: A CAN IDS uses learned vehicle dynamics to detect unusual braking signals injected by attackers.
- **Attack Steps**: 1. Collect CAN logs for real-world braking and acceleration under normal conditions. 2. Use ML frameworks to train a behavioral model (e.g., LSTM) on time-series of throttle, brake, and speed data. 3. Deploy the model into an embedded device with real-time inference capability. 4. When live CAN data deviates from learned patterns (e.g., sudden full brake without speed reduction), flag anomaly. 5. Log the event and send telemetry to central server. 6. Simulate attacks for tuning sensitivity.
- **Detection**: Behavioral deviation alerts
- **Solution**: Train anomaly detection model on normal data
- **Tags**: #CANIDS #MLDetection #BrakingAttack

## Monitor Fuel Gauge Tampering

- **Attack Type**: Cluster Manipulation Detection
- **Target**: IVI Cluster
- **Vulnerability**: Gauge Spoofing
- **MITRE**: T0881
- **Impact**: Prevent Misinformation to Driver
- **Tools**: UDS Diagnostic Tool, CANLogger
- **Scenario**: Driver dashboard shows fake fuel level, confusing operators.
- **Attack Steps**: 1. Use UDS (Unified Diagnostic Services) to poll the actual fuel sensor reading from the BMS or fuel system ECU. 2. Cross-check this raw sensor data with dashboard gauge output. 3. If discrepancies exceed ±5% consistently, flag as potential cluster manipulation. 4. Log such incidents and cross-correlate with service logs. 5. Simulate CAN injection of fake gauge data to test detection effectiveness.
- **Detection**: Cross-sensor comparison
- **Solution**: Compare raw sensor data with cluster output
- **Tags**: #ClusterAttack #SensorIntegrity

## Secure OTA Update Pipeline

- **Attack Type**: Secure Firmware Distribution
- **Target**: Cloud OTA + ECU
- **Vulnerability**: MiTM during Firmware Delivery
- **MITRE**: T1601
- **Impact**: Prevent Firmware Tampering
- **Tools**: TLS, Code Signing, AWS IoT
- **Scenario**: A remote update is intercepted during OTA and replaced with malicious firmware.
- **Attack Steps**: 1. Configure OTA backend with TLS 1.3 and enforce mutual authentication. 2. Require firmware binaries to be signed with vendor’s private key. 3. On vehicle, ensure bootloader verifies firmware signature before writing. 4. Maintain an OTA manifest with firmware hashes and sizes to detect tampering. 5. If mismatch or unsigned firmware is detected, abort the update and log incident.
- **Detection**: TLS logs, signature verification
- **Solution**: Use code signing and secure OTA channels
- **Tags**: #FOTA #TLS #CodeSigning

## SIEM Dashboard for Fleet Security

- **Attack Type**: Centralized Fleet Monitoring
- **Target**: Fleet of Vehicles
- **Vulnerability**: Undetected ECU Compromise
- **MITRE**: T0886
- **Impact**: Fleet-wide Incident Detection
- **Tools**: ELK Stack, Splunk, MQTT Broker
- **Scenario**: A SIEM collects data from thousands of vehicles and detects large-scale anomalies.
- **Attack Steps**: 1. Configure ECUs to send telemetry to a local gateway that pushes data via MQTT to cloud. 2. Ingest logs into SIEM (e.g., ELK or Splunk) and parse fields like frame ID, speed, gear, GPS. 3. Create alerts for high-frequency abnormal frames, missing heartbeats, or ECU reboots. 4. Visualize timelines of events, showing bursty or late-night traffic from specific vehicles. 5. Correlate logs with service ticket data to detect potential compromises.
- **Detection**: SIEM Dashboards & Alerts
- **Solution**: Centralized monitoring with real-time alerting
- **Tags**: #FleetSIEM #VehicleLogs #ELK

## Detect IVI Malware via Prefetch Monitoring

- **Attack Type**: Suspicious Process Detection
- **Target**: Infotainment Unit
- **Vulnerability**: Sideloaded Malware
- **MITRE**: T1055
- **Impact**: Prevent Unauthorized Code Execution
- **Tools**: Sysmon, Prefetch Parser, Volatility
- **Scenario**: Infotainment system shows lag and errors due to sideloaded app.
- **Attack Steps**: 1. Extract Prefetch files from Android-based IVI system or infotainment OS. 2. Parse entries to identify unusual executable launch patterns (e.g., apps not in trusted list). 3. Correlate with Sysmon logs for parent-child process chains. 4. Use Volatility on memory dumps to find injected or hollowed processes. 5. Set up alert rule if new unsigned binary runs or replaces default apps.
- **Detection**: Prefetch logs + Memory Forensics
- **Solution**: Monitor binary execution history and memory artifacts
- **Tags**: #IVISecurity #MalwareDetection #Sysmon

## Jamming Detection on RF Bands

- **Attack Type**: Signal Disruption Alerting
- **Target**: RKE RF Channels
- **Vulnerability**: Key Fob Jamming
- **MITRE**: T0816
- **Impact**: Detect Physical-Layer Disruption
- **Tools**: SDR, GNURadio, HackRF
- **Scenario**: A car experiences radio jamming preventing unlock via remote.
- **Attack Steps**: 1. Use an SDR (e.g., HackRF) with GNURadio to monitor 315/433/868 MHz bands used for remote keyless entry. 2. Record background RF noise levels during normal operation. 3. Set a threshold for sustained high noise or unmodulated carriers (indicative of jamming). 4. If detected, log event and alert driver through dashboard warning. 5. Optionally, geotag the event and report to SOC.
- **Detection**: RF Signal Analysis
- **Solution**: SDR-based continuous band monitoring
- **Tags**: #Jamming #RFMonitoring #HackRF

## Validate Gear Shift Integrity

- **Attack Type**: Gear Position Spoofing Detection
- **Target**: Powertrain System
- **Vulnerability**: Gear Spoofing
- **MITRE**: T0885
- **Impact**: Prevent Unsafe Gear Changes
- **Tools**: CANalyzer, Gear Sensor Logs
- **Scenario**: Malicious ECU changes gear state unexpectedly during driving.
- **Attack Steps**: 1. Read real-time gear sensor position using CANalyzer. 2. Compare against ECU-reported gear state to check for mismatch. 3. Flag discrepancies, especially during high-speed travel or while braking. 4. Maintain a log of abnormal transitions (e.g., N→R at >40kmph). 5. Simulate spoofed commands for test vehicles to calibrate detection.
- **Detection**: Sensor vs. ECU comparison
- **Solution**: Use redundancy between physical and reported values
- **Tags**: #GearAttack #CANspoofing

## Train Fleet Behavior Profiles with ML

- **Attack Type**: Fleet-Wide Anomaly Detection
- **Target**: Vehicle Fleet
- **Vulnerability**: Unknown/Zero-Day Behavior
- **MITRE**: T0886
- **Impact**: Catch Rare / Coordinated Anomalies
- **Tools**: Scikit-learn, Timeseries DB, K-Means
- **Scenario**: Detect unusual behavior across multiple vehicles with shared patterns.
- **Attack Steps**: 1. Log vehicle parameters (speed, GPS, CAN ID activity, brake events) into a timeseries DB. 2. Use unsupervised ML like K-Means to cluster normal driving patterns across fleet. 3. Identify outliers such as abnormal idle duration, fuel usage, or ECU frame bursts. 4. Retrain models periodically to account for seasonal shifts. 5. Integrate anomaly scores into SIEM or dashboard for SOC visibility.
- **Detection**: ML anomaly scores + SIEM integration
- **Solution**: Leverage ML to learn "normal" and spot deviations
- **Tags**: #FleetAnomaly #MLIDS #FleetSOC

## Deploying CANShield to Detect Malicious Frames

- **Attack Type**: Intrusion Detection
- **Target**: Embedded ECU
- **Vulnerability**: Lack of CAN authentication
- **MITRE**: T0872
- **Impact**: Early detection of frame injection
- **Tools**: CANShield, Vehicle Spy, CANtact Pro
- **Scenario**: Deploy CANShield IDS to detect suspicious CAN messages injected by rogue ECUs or external tools.
- **Attack Steps**: 1. Connect CANShield to vehicle’s CAN bus via diagnostic port or inline with ECU wiring. 2. Configure normal message timing and allowed message IDs during a baseline driving session. 3. Launch a CAN fuzzing attack from a test node using CAN tools. 4. Observe CANShield flagging anomalies in timing, message frequency, or invalid message formats. 5. Log and review flagged data for signs of injection or spoofing.
- **Detection**: CAN IDS alerts, anomaly logs
- **Solution**: Install CANShield, define rules for legitimate traffic
- **Tags**: CAN, IDS, Real-time Monitoring

## Anomaly Detection Using K-Means Clustering on CAN Logs

- **Attack Type**: ML-based Detection
- **Target**: Vehicle CAN Bus
- **Vulnerability**: Predictable CAN patterns
- **MITRE**: T0829
- **Impact**: Detects injected commands or unexpected ECU activity
- **Tools**: Scikit-learn, CAN-Logger, Python
- **Scenario**: Use unsupervised learning to detect unusual CAN behavior across sessions.
- **Attack Steps**: 1. Collect raw CAN traffic logs from several normal driving sessions. 2. Convert logs into features like message frequency, timing, and ID types. 3. Train a k-means model to group data into clusters representing normal behavior. 4. Replay a simulated attack (e.g., throttle spoofing) and extract features. 5. Observe the attack cluster being flagged as an anomaly by distance from cluster centroid.
- **Detection**: Cluster deviation alerts
- **Solution**: Use anomaly-based ML detection on raw CAN data
- **Tags**: CAN, ML, Anomaly Detection

## Firmware Integrity Check on ECU Startup

- **Attack Type**: Firmware Validation
- **Target**: ECU Firmware
- **Vulnerability**: Unsigned firmware
- **MITRE**: T1601.001
- **Impact**: Prevents booting of compromised firmware
- **Tools**: U-Boot, Hashing Libraries, Secure Boot
- **Scenario**: Add a boot-time check to detect tampered or replaced firmware images.
- **Attack Steps**: 1. Modify the ECU bootloader to include a SHA-256 hash check of firmware stored in flash memory. 2. On ECU startup, calculate the hash of firmware in memory. 3. Compare against a known-good hash stored in read-only memory (ROM). 4. If the hashes don’t match, trigger a warning or safe-mode boot. 5. Attempt to boot with modified firmware to confirm detection.
- **Detection**: Hash mismatch at boot
- **Solution**: Secure Boot, Trusted Platform Modules
- **Tags**: Firmware, Secure Boot

## Real-Time Logging of Gear Position to Detect Spoofing

- **Attack Type**: Sensor Validation
- **Target**: Transmission ECU
- **Vulnerability**: CAN spoofing
- **MITRE**: T0872
- **Impact**: Detect dangerous manipulation of gear position
- **Tools**: CAN Logger, OBD-II Adapter, Python Script
- **Scenario**: Detect if gear positions reported by ECU don’t match physical state.
- **Attack Steps**: 1. Continuously log gear status messages from transmission ECU during drive. 2. Cross-reference logged data with camera footage or physical gear position sensor. 3. Simulate a spoofed message attack to report “Neutral” while in “Drive.” 4. Log mismatch and time of spoofing. 5. Use pattern matching to alert on similar deviations.
- **Detection**: Telemetry vs physical mismatch
- **Solution**: Add sensor verification redundancy
- **Tags**: Gear, ECU, Spoof Detection

## OTA Hash Verification before Update Execution

- **Attack Type**: FOTA Defense
- **Target**: IVI System / TCU
- **Vulnerability**: Man-in-the-middle update injection
- **MITRE**: T1601
- **Impact**: Prevents unauthorized update deployment
- **Tools**: Custom FOTA server, SHA256 tools
- **Scenario**: Prevent execution of malicious OTA firmware by checking hash before flashing.
- **Attack Steps**: 1. Receive OTA firmware via secure HTTPS from backend server. 2. Validate update metadata includes hash and digital signature. 3. Before update, calculate local hash and compare with metadata hash. 4. If mismatch, discard update and log the incident. 5. For testing, modify firmware and attempt hash bypass to confirm check failure.
- **Detection**: Log of hash verification failure
- **Solution**: Add hash + signature verification pipeline
- **Tags**: OTA, Firmware Integrity

## ECU Behavioral Baseline Model Using LSTM

- **Attack Type**: Behavior Anomaly Detection
- **Target**: CAN Bus
- **Vulnerability**: Lack of message order enforcement
- **MITRE**: T0829
- **Impact**: Spot time-sequence anomalies in live traffic
- **Tools**: TensorFlow, CAN logs
- **Scenario**: Use LSTM networks to learn time-based sequence of CAN IDs from ECUs.
- **Attack Steps**: 1. Gather time-series CAN logs from normal driving behavior. 2. Train an LSTM model to predict next valid sequence of CAN messages. 3. Introduce an attack message like speed spoofing or invalid RPM. 4. Model flags deviation from expected sequence. 5. Use deviation thresholding to trigger alerts.
- **Detection**: LSTM deviation trigger
- **Solution**: Use temporal prediction for behavioral learning
- **Tags**: LSTM, Behavioral IDS

## Using CANary to Monitor for Invalid Checksum Packets

- **Attack Type**: Protocol Monitoring
- **Target**: CAN Bus
- **Vulnerability**: Frame-level injection
- **MITRE**: T0847
- **Impact**: Detects malformed or fuzzed messages
- **Tools**: CANary Tool, Arduino CAN
- **Scenario**: Detect and alert on packets with invalid CRCs or format errors.
- **Attack Steps**: 1. Set up CANary device on the diagnostic port. 2. Define valid message format and CRC patterns. 3. Replay messages with altered payloads or missing bits. 4. Observe alerts from CANary indicating invalid frames. 5. Analyze logs to identify attempted fuzzing or corruption.
- **Detection**: CRC error alerts
- **Solution**: Use frame validators in CAN pipeline
- **Tags**: CANary, CAN Bus

## Integration of CAN Alerts with SIEM (Fleet Scale)

- **Attack Type**: Fleet Monitoring
- **Target**: Fleet CAN Logs
- **Vulnerability**: Lack of centralized telemetry
- **MITRE**: T1589
- **Impact**: Scalable fleet-wide anomaly detection
- **Tools**: CANShield, Elastic SIEM, Logstash
- **Scenario**: Push CAN anomaly logs to cloud-based SIEM for correlation.
- **Attack Steps**: 1. Configure CANShield to log anomalies (timing, frequency, ID mismatch). 2. Export logs to centralized log collector via MQTT or REST API. 3. Use Logstash to parse and forward logs to Elastic SIEM. 4. Create dashboards and correlation rules to detect multi-vehicle anomalies. 5. Test by injecting false speed messages into multiple fleet vehicles.
- **Detection**: Cross-vehicle anomaly correlation
- **Solution**: Centralized SIEM with CAN integration
- **Tags**: SIEM, Fleet Monitoring

## Boot-Time Remote Attestation of Vehicle Firmware

- **Attack Type**: Remote Trust Validation
- **Target**: Vehicle Controller
- **Vulnerability**: Tampered bootloader or firmware
- **MITRE**: T1601
- **Impact**: Prevents remote fleet compromise
- **Tools**: TPM 2.0, Remote Attestation Server
- **Scenario**: Verify that remote vehicle firmware hasn’t been tampered using challenge-response.
- **Attack Steps**: 1. At boot, vehicle calculates firmware measurement (hash). 2. Sends signed hash via secure channel to cloud server. 3. Server validates against known hash list and responds with attestation token. 4. Deny remote access if attestation fails. 5. For testing, simulate firmware tampering and observe denial.
- **Detection**: Attestation failure logs
- **Solution**: Use TPM + secure channel for attestation
- **Tags**: TPM, Remote Check

## CAN IDS Triggered by Rapid Message Rate Increases

- **Attack Type**: Rate-Based Anomaly Detection
- **Target**: CAN Network
- **Vulnerability**: DoS via flooding
- **MITRE**: T1499
- **Impact**: Detects high-speed message spam
- **Tools**: Custom IDS Script, Python, CANlib
- **Scenario**: Detect flood attacks or DoS conditions using frame-per-second thresholds.
- **Attack Steps**: 1. Log normal message rate for each CAN ID (e.g., 10 msg/sec). 2. Define thresholds (e.g., >15 msg/sec) for alerting. 3. Launch DoS from attacker laptop spamming engine RPM messages. 4. IDS triggers alert due to rate spike. 5. Log attacker’s message IDs and block via gateway.
- **Detection**: Message rate anomaly alert
- **Solution**: Apply thresholding in IDS logic
- **Tags**: CAN DoS, Rate Alert

## CAN Intrusion Detection with CANShield

- **Attack Type**: Defensive Monitoring
- **Target**: Vehicle CAN Network
- **Vulnerability**: No in-vehicle anomaly monitoring
- **MITRE**: T0887
- **Impact**: Early detection of ECU spoofing or injection
- **Tools**: CANShield, Raspberry Pi, SocketCAN
- **Scenario**: Install CANShield to identify malicious CAN frame injection attempts in a test vehicle
- **Attack Steps**: 1. Integrate a Raspberry Pi with a CAN transceiver and install CANShield. 2. Connect it between the OBD-II port and the vehicle’s CAN bus. 3. Capture normal driving data to build a baseline. 4. Simulate an attack by injecting malformed CAN frames using a tool like cansend. 5. Observe detection by CANShield and its anomaly logs. 6. Tune thresholds to minimize false positives and maximize attack detection accuracy. 7. Generate reports on which ECUs were potentially spoofed.
- **Detection**: Log anomalies from CANShield, analyze bus load and ECU response
- **Solution**: Implement CANShield in production environments for real-time alerting
- **Tags**: IDS, CAN bus, real-time defense

## Behavioral Model Training for ECU

- **Attack Type**: Behavioral Analysis
- **Target**: ECU behavior
- **Vulnerability**: Lack of behavior anomaly profiling
- **MITRE**: T0820
- **Impact**: Identification of ECU compromise or spoofing
- **Tools**: TensorFlow, Python, CAN logs, Keras
- **Scenario**: Use AI to model ECU behavior and detect anomalies via deviation from learned profiles
- **Attack Steps**: 1. Collect large CAN logs under varied normal driving conditions. 2. Preprocess the data by timestamping and labeling per ECU type. 3. Design a neural network using LSTM or GRU layers to capture temporal patterns in ECU messaging. 4. Train the model until it can reliably predict normal sequences. 5. Inject attack patterns (e.g., frame floods, spoofed RPM) into validation set. 6. Use model inference to flag anomalies based on low prediction confidence or timing mismatches. 7. Evaluate precision-recall to determine model robustness.
- **Detection**: Deviations from predicted patterns
- **Solution**: Deploy behavior detection as part of firmware update
- **Tags**: AI-based IDS, CAN ML, sequence modeling

## Centralized Fleet Telemetry Monitoring

- **Attack Type**: Fleet Monitoring
- **Target**: Vehicle fleet backend
- **Vulnerability**: Disconnected or isolated monitoring
- **MITRE**: T0886
- **Impact**: Enhanced incident response across all vehicles
- **Tools**: Elastic SIEM, Logstash, Telematics Gateway, MQTT
- **Scenario**: Connect all vehicles in a fleet to a central SIEM dashboard to detect and respond to anomalies
- **Attack Steps**: 1. Equip vehicles with telematics units that publish data to MQTT or HTTP endpoints. 2. Aggregate logs including speed, location, OBD codes, door states. 3. Use Logstash to normalize and forward logs to Elastic SIEM. 4. Define detection rules for things like excessive speed at odd hours, or unexpected location. 5. Enable alerts when thresholds or unusual events occur. 6. Track anomalies per vehicle or across the fleet to spot coordinated tampering. 7. Provide dashboards and timeline graphs to security staff.
- **Detection**: SIEM analytics and alert thresholds
- **Solution**: Maintain a dedicated Fleet SOC
- **Tags**: Fleet SOC, Elastic SIEM, telematics monitoring

## Firmware Boot Hash Validation

- **Attack Type**: Integrity Verification
- **Target**: Infotainment Firmware
- **Vulnerability**: Missing signature/hash validation
- **MITRE**: T1608
- **Impact**: Prevent firmware tampering or backdooring
- **Tools**: UBoot, SHA256, Secure Boot, Flash Tools
- **Scenario**: Implement hash-based validation to ensure no unauthorized firmware loads
- **Attack Steps**: 1. Modify the bootloader (e.g., U-Boot) to verify firmware hashes before executing. 2. Generate a secure SHA-256 hash for the verified firmware and store it in secure flash. 3. Ensure that each boot reads the firmware, hashes it, and compares it with the stored value. 4. If mismatch occurs, halt boot process and send alert to backend. 5. Attempt to tamper the firmware (e.g., inject backdoor in IVI binary) and test system’s refusal to boot. 6. Log events of failed verifications for auditing. 7. Add rollback prevention to disallow loading old, vulnerable firmware.
- **Detection**: Secure boot logs and hash mismatches
- **Solution**: Enable Secure Boot and signed images
- **Tags**: Firmware integrity, bootloader defense

## ECU Whitelist Enforcement

- **Attack Type**: Command Validation
- **Target**: Gateway CAN Router
- **Vulnerability**: Unfiltered message routing
- **MITRE**: T0887
- **Impact**: Prevent external device injection
- **Tools**: CAN Gateway, Filtering Logic, Linux SocketCAN
- **Scenario**: Allow only pre-approved ECU message IDs and block suspicious ones at the gateway
- **Attack Steps**: 1. Capture and document all legitimate CAN message IDs during vehicle startup and operation. 2. Deploy a gateway module that enforces a whitelist of allowed message IDs. 3. Block any unexpected or malformed messages from relays or foreign devices. 4. Simulate an attack using a rogue CAN injector sending random IDs. 5. Verify that unauthorized messages are discarded silently. 6. Monitor logs to trace dropped messages and the attack vector. 7. Tune the filter to allow dynamic vehicle modes (e.g., sport mode adds new messages).
- **Detection**: Message ID blocking logs
- **Solution**: Hard-code message whitelist
- **Tags**: CAN Gateway, whitelist, secure messaging

## ECU Clock Drift Detection

- **Attack Type**: Timing Anomaly Detection
- **Target**: CAN ECUs
- **Vulnerability**: Clock skew not checked
- **MITRE**: T0820
- **Impact**: Spot fake ECU responses or flooding
- **Tools**: CAN Logger, Python Scripts, NTP
- **Scenario**: Use timestamp-based anomaly checks to spot manipulated ECUs or injected traffic
- **Attack Steps**: 1. Log CAN traffic over extended drives to capture time intervals of normal ECU messages. 2. Use timestamp deltas to compute expected ranges for each ECU (e.g., 50ms ± 5ms). 3. Inject fake ECU messages using a delay or acceleration outside of this range. 4. Detect anomalies when drift or jitter exceeds thresholds. 5. Build alerts into dashboard when drift is consistent with injection or spoofing. 6. Correlate with driver behavior and GPS to improve accuracy. 7. Fine-tune detection to reduce false positives due to terrain or network lag.
- **Detection**: Timing-based anomaly graphs
- **Solution**: Deploy drift checks in IDS module
- **Tags**: Clock drift, CAN injection defense

## Dashboard Warning Light Alerting

- **Attack Type**: In-Cabin Monitoring
- **Target**: Instrument Cluster
- **Vulnerability**: Cluster signals blindly trusted
- **MITRE**: T1556
- **Impact**: Mislead drivers about vehicle health
- **Tools**: OBD-II Logger, Instrument Cluster Tester
- **Scenario**: Detect when attackers spoof or suppress warning lights like ABS or airbags
- **Attack Steps**: 1. Connect to OBD-II to record all warning light CAN frames under normal conditions. 2. Observe expected frequency and signal patterns for lights like seatbelt, ABS, and airbags. 3. Simulate an attack where these signals are suppressed or overwritten with false “OK” messages. 4. Compare actual vehicle state (e.g., disabled ABS sensor) to cluster status. 5. Trigger alerts if lights are missing or appear out of sync. 6. Provide maintenance technicians and fleet managers with logs showing tampering. 7. Add verification logic during diagnostic routines.
- **Detection**: Compare expected vs actual light signals
- **Solution**: Add diagnostic parity checks
- **Tags**: Cluster spoofing, sensor fraud

## Remote ECU Fingerprinting

- **Attack Type**: Profiling
- **Target**: ECU components
- **Vulnerability**: No profiling of hardware behavior
- **MITRE**: T0820
- **Impact**: Spot fake or tampered ECUs
- **Tools**: CANScope, Power Profiler Kit, Oscilloscope
- **Scenario**: Identify each ECU’s unique timing and power signature to detect unauthorized devices
- **Attack Steps**: 1. Monitor CAN bus traffic and measure timing characteristics like message periodicity. 2. Record current draw patterns from each ECU using high-precision profiler. 3. Build a signature profile for each ECU. 4. Introduce a counterfeit ECU or injector tool into the system. 5. Detect anomalies in power draw, voltage ripple, or timing jitter. 6. Alert vehicle system when deviation exceeds set threshold. 7. Repeat for cold start and long-drive scenarios to ensure accuracy.
- **Detection**: Profile-based anomaly detection
- **Solution**: Use during quality assurance and inspection
- **Tags**: Hardware fingerprinting, ECUs

## IVI Application Whitelist Enforcement

- **Attack Type**: Application Control
- **Target**: Infotainment System
- **Vulnerability**: App execution not restricted
- **MITRE**: T0853
- **Impact**: Prevent rogue code or malware
- **Tools**: Linux AppArmor, SystemD, IVI Firmware
- **Scenario**: Allow only authorized apps to run in Infotainment System and block others at startup
- **Attack Steps**: 1. Use Linux AppArmor to define which binaries are allowed to execute on the IVI. 2. Define profiles for media players, navigation, and OEM apps. 3. Simulate installation of rogue APK or binary to test protection. 4. Verify denial messages in logs and UI failure to launch. 5. Configure logs to report attempts to bypass profiles or tamper with AppArmor. 6. Alert OEM backend if a rogue process is detected. 7. Use firmware update to push updated profiles as needed.
- **Detection**: AppArmor logs and process block
- **Solution**: Harden runtime with strict profiles
- **Tags**: IVI lockdown, AppArmor

## GPS Spoof Detection using Movement Anomalies

- **Attack Type**: Anomaly Analysis
- **Target**: GPS + IMU + Wheel Speed
- **Vulnerability**: No cross-sensor validation
- **MITRE**: T0884
- **Impact**: Detect navigation spoofing
- **Tools**: GPS Logger, IMU, CAN Speed, Python
- **Scenario**: Detect GPS spoofing by correlating with wheel speed and IMU sensor data
- **Attack Steps**: 1. Record GPS position, CAN speed, and IMU readings during real driving. 2. Build a correlation model—e.g., when GPS says 100km/h, wheel speed and IMU should match. 3. Simulate spoofed GPS data (e.g., fake rapid teleporting). 4. Alert when GPS and physical sensors deviate beyond tolerance. 5. Use a Kalman filter or anomaly scoring to detect subtle drift attacks. 6. Visualize route on map to highlight implausible segments. 7. Feed alerts into SIEM for fleet-scale review.
- **Detection**: Sensor fusion inconsistency
- **Solution**: Use GPS + IMU correlation
- **Tags**: GPS spoofing defense

## CAN Bus Entropy-Based IDS Deployment

- **Attack Type**: Defensive Technique
- **Target**: CAN Bus
- **Vulnerability**: CAN traffic predictability
- **MITRE**: T0812
- **Impact**: Detects spoofing and replay attacks
- **Tools**: Custom Python Scripts, CANalyzer, CANShield
- **Scenario**: Deploy an IDS that uses entropy variations of CAN traffic to detect anomalies like replay or injection attacks.
- **Attack Steps**: 1. Capture baseline CAN traffic under normal driving conditions using CANalyzer or SocketCAN. 2. Measure the entropy (randomness) of ID fields and payloads to build a profile. 3. Develop or configure an IDS to monitor real-time traffic and detect statistically significant entropy deviations. 4. When entropy drops (indicating repeated or injected messages), trigger alerts or isolate the affected ECU. 5. Regularly update the entropy model with new baseline profiles as vehicles evolve.
- **Detection**: Anomaly-based entropy triggers
- **Solution**: Train baseline models, implement blocking response
- **Tags**: #CANIDS #Entropy #AnomalyDetection #ECUSecurity

## Secure OTA Verification via TPM

- **Attack Type**: Defensive Technique
- **Target**: ECU
- **Vulnerability**: Unsigned or malicious firmware
- **MITRE**: T0803
- **Impact**: Blocks unauthorized firmware installs
- **Tools**: TPM 2.0, Secure Boot, UEFI, Infineon tools
- **Scenario**: Use Trusted Platform Module (TPM) to verify firmware signature before applying over-the-air (OTA) updates.
- **Attack Steps**: 1. Integrate a TPM chip into the vehicle’s ECU system to secure cryptographic operations. 2. During OTA, download the firmware into a staging area. 3. Verify the firmware’s digital signature using public key stored in TPM. 4. If signature verification fails, block update and log anomaly. 5. If passed, proceed with atomic firmware swap and reboot with integrity check on boot using TPM PCR registers.
- **Detection**: TPM logs and Secure Boot errors
- **Solution**: Enforce TPM-based verification and rollback
- **Tags**: #TPM #OTA #FirmwareSecurity #TrustedComputing

## Behavioral Fingerprinting for ECUs

- **Attack Type**: Defensive Technique
- **Target**: ECU
- **Vulnerability**: Impersonated/spoofed ECUs
- **MITRE**: T0851
- **Impact**: Detects ECU spoofing and impersonation
- **Tools**: CANvas, K-Means Clustering, Python
- **Scenario**: Create behavioral fingerprints of ECUs based on message frequency and pattern to detect spoofed devices.
- **Attack Steps**: 1. Monitor each ECU’s CAN message ID, frequency, timing, and payload structure during normal operation. 2. Create statistical and timing-based fingerprints (e.g., ECU A sends ID 0x201 every 50ms). 3. Use machine learning (e.g., K-Means) to cluster and identify abnormal deviations. 4. When spoofed ECUs try to mimic real ones, timing irregularities or inconsistent payloads are flagged. 5. Alert the driver or disable unverified ECUs based on fingerprint mismatch.
- **Detection**: Deviations from fingerprint pattern
- **Solution**: Dynamic model updates & policy enforcement
- **Tags**: #BehavioralDetection #ECUFingerprint #CANsecurity

## Digital Forensics Logging in IVI

- **Attack Type**: Defensive Technique
- **Target**: IVI System
- **Vulnerability**: Lack of audit trails
- **MITRE**: T0830
- **Impact**: Supports investigation & detection
- **Tools**: Android Debug Bridge (ADB), syslog, journald
- **Scenario**: Enable IVI logging features to retain data on Bluetooth/Wi-Fi pairing, system changes, and application execution.
- **Attack Steps**: 1. Enable full system logging on IVI (Infotainment) platforms—especially those running Android Automotive. 2. Log all system-level events including user logins, app launches, network access, and USB insertions. 3. Sync logs to cloud or fleet SIEM backend regularly. 4. Enable tamper-evident logs using hash chaining or secure logging APIs. 5. Use forensic logs during post-incident investigations or for anomaly correlation in real-time.
- **Detection**: Log aggregation and hash-check
- **Solution**: Forensic-grade logging policy
- **Tags**: #IVI #Forensics #Logging #TamperEvident

## Anomaly-Based Brake Control Detection

- **Attack Type**: Defensive Technique
- **Target**: Brake System
- **Vulnerability**: CAN injection or spoofed signals
- **MITRE**: T0812
- **Impact**: Detects braking spoof or override
- **Tools**: CANshield, Brake Sensor, AI Model
- **Scenario**: Detect malicious braking commands by correlating brake messages with driver foot sensor and road conditions.
- **Attack Steps**: 1. Collect and correlate data from brake pedal sensors, road condition inputs (e.g., ABS), and CAN brake commands. 2. Build a behavior model of legitimate braking behavior across scenarios. 3. Use this model to detect anomalies like sudden full brake without pedal press. 4. Trigger alerts or override the braking signal with a safe fallback mode. 5. Use historical data to improve detection accuracy over time.
- **Detection**: Mismatch between sensor & CAN data
- **Solution**: Sensor cross-validation logic
- **Tags**: #BrakeSpoofing #CANInjection #SafetyIDS

## Secure Logging Gateway (SLG) in Telematics

- **Attack Type**: Defensive Technique
- **Target**: Telematics Unit
- **Vulnerability**: Log tampering or spoofing
- **MITRE**: T0830
- **Impact**: Preserves forensic log integrity
- **Tools**: OpenSSL, secure enclave chip, HSM
- **Scenario**: Deploy a centralized secure logging gateway (SLG) in the telematics unit to sign, timestamp, and encrypt vehicle logs.
- **Attack Steps**: 1. Integrate a logging component within the telematics unit that collects system and CAN logs. 2. Sign logs digitally and timestamp using GPS time or a secure clock. 3. Encrypt the logs before local storage or transmission to the cloud. 4. Ensure logs are stored in append-only format and periodically offloaded to SIEM. 5. Use signed logs for post-breach forensics and real-time anomaly validation.
- **Detection**: Log signature verification
- **Solution**: Deploy HSM or secure enclave for logging
- **Tags**: #SLG #Telematics #SecureLogging

## Fleet-Wide Threat Intelligence Correlation

- **Attack Type**: Defensive Technique
- **Target**: Fleet (Multiple Vehicles)
- **Vulnerability**: Distributed attacks across vehicles
- **MITRE**: T0851
- **Impact**: Detects campaign-level attacks
- **Tools**: Elastic SIEM, Zeek for Vehicle Networks
- **Scenario**: Collect threat intel from multiple vehicles and correlate at fleet SOC to identify common indicators of compromise.
- **Attack Steps**: 1. Enable endpoint telemetry in IVI and telematics units to report events to fleet SOC. 2. Ingest logs such as failed connections, Bluetooth pairing attempts, USB usage. 3. Correlate across fleet to identify repeated IOCs or suspicious IPs targeting many vehicles. 4. Enrich detections with threat intel feeds and geo-IP databases. 5. Trigger fleet-wide rules or alerts when multi-vehicle indicators match.
- **Detection**: Cross-vehicle event correlation
- **Solution**: Build fleet-wide SOC rulesets
- **Tags**: #FleetSOC #ThreatIntel #Correlation #ElasticSIEM

## CAN Rate Limiting via ECU Throttle

- **Attack Type**: Defensive Technique
- **Target**: ECU
- **Vulnerability**: Flooding or spamming CAN frames
- **MITRE**: T0812
- **Impact**: Mitigates CAN DoS
- **Tools**: UDS config tools, ECU firmware patching
- **Scenario**: Implement rate limiting on ECUs to avoid flood-based CAN DoS or command spamming.
- **Attack Steps**: 1. Modify ECU firmware to limit how often it can transmit high-priority CAN frames. 2. Configure rules such that repeated identical commands (e.g., brake or steering) within X ms are dropped. 3. Track timestamps and frequency of outbound messages inside ECU logic. 4. If messages exceed limits, temporarily block transmission and log incident. 5. Helps stop flooding attacks or ECU misbehavior from dominating CAN.
- **Detection**: Frequency analysis or ECU counters
- **Solution**: Rate control policies at firmware level
- **Tags**: #ECUthrottle #RateLimiting #DoSMitigation

## Telematics Access Control Enforcement

- **Attack Type**: Defensive Technique
- **Target**: Telematics Cloud API
- **Vulnerability**: Weak access control
- **MITRE**: T0813
- **Impact**: Prevents remote vehicle abuse
- **Tools**: OAuth2.0, API Gateway, AWS IAM
- **Scenario**: Enforce strict RBAC and access tokens in telematics cloud API to prevent unauthorized vehicle commands.
- **Attack Steps**: 1. Configure API gateway to enforce OAuth 2.0 tokens and access scopes for telematics actions (e.g., start, unlock). 2. Assign per-user and per-device role-based permissions. 3. Deny access to privileged operations unless verified and authorized (e.g., based on user device fingerprinting). 4. Log every API call with timestamp and geolocation. 5. Auto-revoke sessions if suspicious access is detected.
- **Detection**: API log analysis & auth failures
- **Solution**: Strong RBAC + anomaly alerts
- **Tags**: #RBAC #CloudTelematics #APISecurity

## Dynamic Honeypots in Vehicle Testbeds

- **Attack Type**: Defensive Technique
- **Target**: Testbed Vehicle
- **Vulnerability**: Recon or exploit attempts
- **MITRE**: T1595
- **Impact**: Intelligence on attacker behavior
- **Tools**: ICSim, CANToolz, Fake ECUs
- **Scenario**: Deploy honeypot ECUs or IVI systems that mimic vulnerable systems to lure attackers in testbed environments.
- **Attack Steps**: 1. Simulate ECUs with default credentials, weak firmware, or open ports in controlled testbed. 2. Log all unsolicited CAN commands or connections made to honeypot. 3. Use CANToolz to simulate responses and lure attackers deeper into fake systems. 4. Analyze attacker behavior and tools based on CAN traffic and payloads. 5. Use findings to improve production IDS rules and detection thresholds.
- **Detection**: Honeypot traffic logs
- **Solution**: Tune detection rules with real tactics
- **Tags**: #VehicleHoneypot #CANToolz #ICSim #ThreatIntel

