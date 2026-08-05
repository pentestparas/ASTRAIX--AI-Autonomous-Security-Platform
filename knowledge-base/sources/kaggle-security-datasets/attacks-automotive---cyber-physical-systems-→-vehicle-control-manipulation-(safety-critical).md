# Automotive / Cyber-Physical Systems → Vehicle Control Manipulation (Safety-Critical) Attacks

## Malicious Brake Light Override

- **Attack Type**: CAN Injection
- **Target**: Passenger Vehicle
- **Vulnerability**: Insecure CAN Arbitration
- **MITRE**: T1562
- **Impact**: Traffic accidents, road confusion
- **Tools**: CANable, SavvyCAN, Wireshark
- **Scenario**: Attacker spoofs brake light activation via CAN to mislead trailing vehicles.
- **Attack Steps**: 1. Identify CAN ID responsible for brake light activation by logging while applying brakes. 2. Replay the same CAN frame with brake light signal while vehicle is idle. 3. Observe if rear lights turn on without actual brake use. 4. Time the fake signals to confuse drivers behind, potentially causing rear-end collisions.
- **Detection**: Monitor CAN bus for unexpected light commands
- **Solution**: Implement ECU-layer signal verification
- **Tags**: #CAN #BrakeSpoofing #TrafficSafety

## Sudden RPM Spike via CAN

- **Attack Type**: RPM Falsification
- **Target**: Passenger Vehicle
- **Vulnerability**: Lack of value verification in dashboard ECU
- **MITRE**: T1496
- **Impact**: Driver distraction or panic
- **Tools**: CANDump, ICSim, Vector CANoe
- **Scenario**: RPM cluster falsely shows redline while engine idles, causing panic.
- **Attack Steps**: 1. Log CAN traffic while revving engine to identify RPM ID. 2. Craft CAN packets with maximum RPM value. 3. Inject forged messages during idle condition. 4. Observe cluster's reaction and driver behavior.
- **Detection**: RPM sensor vs. CAN data mismatch
- **Solution**: Cluster-side plausibility checks
- **Tags**: #ClusterHacks #RPMFake #InfotainmentCAN

## Spoofed Gear Indicator on Dashboard

- **Attack Type**: Cluster Deception
- **Target**: Passenger Vehicle
- **Vulnerability**: Dashboard doesn’t cross-check gear ECU
- **MITRE**: T1609
- **Impact**: Collision during reversing
- **Tools**: CANalyze, Arduino + MCP2515
- **Scenario**: Gear shown as 'D' while vehicle is actually in 'R', misleading the driver.
- **Attack Steps**: 1. Identify CAN message that carries gear position. 2. Record valid gear switch from 'R' to 'D'. 3. Replay 'D' signal while driver is still in 'R'. 4. Result: dashboard displays incorrect gear.
- **Detection**: Validate cluster data via gear ECU
- **Solution**: Multi-signal validation per subsystem
- **Tags**: #GearSpoofing #DisplayHack #SafetyOverride

## Fake Speed Display While Parked

- **Attack Type**: Cluster Tampering
- **Target**: Fleet Vehicles
- **Vulnerability**: No runtime speed sensor validation
- **MITRE**: T1600
- **Impact**: Insurance fraud, data falsification
- **Tools**: SavvyCAN, CANPlayer
- **Scenario**: Show fake speed (e.g., 120km/h) while car is stationary to confuse or spoof logs.
- **Attack Steps**: 1. Monitor CAN ID for speed changes during driving. 2. Inject forged speed packets while vehicle is stationary. 3. Observe cluster needle movement or digital readout change. 4. Check implications on telemetry or black-box data.
- **Detection**: Compare GPS and wheel sensor data
- **Solution**: Require multi-sensor correlation
- **Tags**: #SpeedHack #CANInjection #FleetManipulation

## Reverse Sensor Disabling Attack

- **Attack Type**: Sensor Signal Blocking
- **Target**: Passenger Vehicle
- **Vulnerability**: Unauthenticated sensor control
- **MITRE**: T1485
- **Impact**: Collision during reversing
- **Tools**: RF Jammers, OBD-II Tool
- **Scenario**: Attack disables ultrasonic reverse sensors before driver backs up.
- **Attack Steps**: 1. Identify reverse sensor control ID. 2. Use CAN tool to send shutdown command at reverse gear trigger. 3. Driver reverses with no alert, leading to crash risk. 4. Simulate with or without vehicle alarms.
- **Detection**: Log sensor activation vs. control CAN
- **Solution**: Implement reverse-mode integrity checks
- **Tags**: #ReverseSensorHack #CAN #SafetyRisk

## Disable ESC via CAN Frame Injection

- **Attack Type**: Stability System Tampering
- **Target**: Passenger Vehicle
- **Vulnerability**: ESC lacks source authentication
- **MITRE**: T1499
- **Impact**: Loss of traction or vehicle rollover
- **Tools**: CANBus Triple, Python-CAN
- **Scenario**: Attacker disables Electronic Stability Control during high-speed turn.
- **Attack Steps**: 1. Identify ESC activation frame through logging during turns. 2. Replay 'disable' command to override ESC. 3. Test in simulation or controlled environment. 4. Observe skid risk increase.
- **Detection**: Check ESC logs and actual torque data
- **Solution**: Require digital signing for safety ECUs
- **Tags**: #ESCBypass #CANHacking #VehicleControl

## Faked Fuel Level to Mislead Driver

- **Attack Type**: Dashboard Spoofing
- **Target**: Passenger Vehicle
- **Vulnerability**: No tank-sensor consistency checks
- **MITRE**: T1585
- **Impact**: Vehicle stall in unsafe location
- **Tools**: ICSim, SocketCAN, CAN Logger
- **Scenario**: Fuel gauge always reads 'full', even if tank is empty, tricking driver.
- **Attack Steps**: 1. Capture normal fuel level CAN ID patterns while driving. 2. Inject static '100%' packet repeatedly. 3. Driver believes tank is full and may run out unknowingly.
- **Detection**: Cross-verify tank sensor vs. CAN level
- **Solution**: Implement dashboard-sensor binding
- **Tags**: #FuelSpoof #CANClusterHack #DashManipulation

## Hazard Light Falsification via CAN

- **Attack Type**: Indicator Spoofing
- **Target**: Passenger Vehicle
- **Vulnerability**: Indicator control lacks message origin verification
- **MITRE**: T1565
- **Impact**: Distracted or dangerous driving
- **Tools**: CANable Pro, Logic Analyzer
- **Scenario**: Hazard lights are triggered remotely while vehicle is moving.
- **Attack Steps**: 1. Monitor the hazard light toggle frame ID. 2. Craft and inject this signal during motion. 3. Observe driver confusion and other traffic reactions.
- **Detection**: Log hazard activations against driver input
- **Solution**: Use cryptographic tokens for critical actions
- **Tags**: #CANInjection #LightHack #SignalTamper

## Sudden Climate System Overdrive

- **Attack Type**: Cabin Environment Tampering
- **Target**: Passenger Vehicle
- **Vulnerability**: No control input verification on HVAC
- **MITRE**: T1647
- **Impact**: Driver distraction, fogged windows
- **Tools**: CANSniffer, CANBus Hack Kit
- **Scenario**: Climate control is set to max heat or cold by attacker via CAN.
- **Attack Steps**: 1. Log HVAC-related CAN traffic during normal use. 2. Identify temperature and blower level values. 3. Inject max-heat or max-cooling command via CAN. 4. Observe rapid cabin discomfort and driver distraction.
- **Detection**: Monitor HVAC changes vs. user controls
- **Solution**: Require HMI-originated command only
- **Tags**: #HVACHack #ComfortSystem #DistractionAttack

## Simulated Check Engine Light

- **Attack Type**: Warning Signal Spoof
- **Target**: Passenger Vehicle
- **Vulnerability**: CAN fault injection unverified by ECU
- **MITRE**: T1602
- **Impact**: Unnecessary servicing, driver stress
- **Tools**: CANBus Triple, obdCAN
- **Scenario**: Trigger Check Engine Light via CAN despite no fault.
- **Attack Steps**: 1. Log diagnostic fault frame when CEL appears. 2. Reproduce message without actual fault. 3. Observe dashboard lighting up and driver confusion.
- **Detection**: Correlate DTCs with actual sensor values
- **Solution**: Use digital signing for fault flags
- **Tags**: #DTCInjection #FakeCEL #VehicleMislead

