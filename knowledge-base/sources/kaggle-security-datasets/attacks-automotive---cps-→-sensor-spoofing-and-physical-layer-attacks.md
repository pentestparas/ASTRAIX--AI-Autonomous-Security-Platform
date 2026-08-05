# Automotive / CPS → Sensor Spoofing & Physical Layer Attacks Attacks

## GPS Spoofing via SDR Transmitter

- **Attack Type**: GPS Spoofing
- **Target**: Vehicle GPS Receiver
- **Vulnerability**: Unencrypted GPS signal interpretation
- **MITRE**: T1612
- **Impact**: Navigation manipulation
- **Tools**: HackRF One, GPS-SDR-SIM
- **Scenario**: An attacker misguides a vehicle’s GPS by transmitting false location signals using an SDR transmitter.
- **Attack Steps**: 1. Set up HackRF One on a Linux machine. 2. Use GPS-SDR-SIM to generate GPS signal I/Q files with fake coordinates. 3. Configure the GPS simulator with altered latitude and longitude. 4. Transmit the spoofed GPS signals over the air using HackRF. 5. Observe as the vehicle's infotainment or navigation system reports incorrect location. 6. Redirect the system to nearby wrong roads or false destinations. 7. Use in combination with ADAS to cause unintended steering behavior.
- **Detection**: Check signal strength anomalies, monitor for inconsistent GNSS satellite IDs
- **Solution**: Use authenticated GNSS signals (e.g., Galileo), integrate inertial sensors for cross-check
- **Tags**: gps-spoofing, SDR, HackRF, ADAS

## GNSS Jamming Attack on Navigation

- **Attack Type**: GPS Jamming
- **Target**: Vehicle Navigation Module
- **Vulnerability**: Lack of GPS signal authentication, vulnerable to RF interference
- **MITRE**: T1612
- **Impact**: Loss of positioning and route assistance
- **Tools**: GNSS Jammer, RF Signal Generator
- **Scenario**: A threat actor jams GPS signals around a car using RF interference, disabling navigation.
- **Attack Steps**: 1. Acquire a low-power GNSS jammer or build one using an RF signal generator. 2. Set the frequency range to match GPS L1 (1575.42 MHz). 3. Place the jammer near the vehicle. 4. Activate the jammer to disrupt GPS reception. 5. The vehicle's infotainment shows "GPS signal lost." 6. Observe impact on turn-by-turn navigation and geo-fencing systems.
- **Detection**: Monitor for loss of satellite lock, signal-to-noise ratio drops
- **Solution**: Implement anti-jamming antenna, integrate IMU for fallback
- **Tags**: gnss, jamming, rf-interference

## LIDAR Spoofing with Reflective Objects

- **Attack Type**: LIDAR Spoofing
- **Target**: LIDAR Sensor
- **Vulnerability**: Trust in reflected signal strength and timing
- **MITRE**: T1609
- **Impact**: False positives in autonomous driving
- **Tools**: Retroreflective tape, tripod
- **Scenario**: An attacker uses reflective material to simulate non-existent vehicles or obstacles in front of the car.
- **Attack Steps**: 1. Identify the LIDAR sensor location on the target vehicle. 2. Place reflective tape on a small object and position it at an angle. 3. As the LIDAR emits pulses, the tape bounces strong signals back. 4. The vehicle interprets the reflection as an object ahead. 5. Watch the car slow down, brake, or attempt to avoid the "ghost" object. 6. Repeat with multiple objects to simulate a traffic jam or barrier.
- **Detection**: Compare camera feed with LIDAR data; use AI-based object detection
- **Solution**: Fuse data from LIDAR, camera, and radar to confirm object validity
- **Tags**: lidar, spoofing, object-detection

## TPMS Spoofing to Send Low-Pressure Alerts

- **Attack Type**: TPMS Spoofing
- **Target**: Tire Pressure Monitoring System
- **Vulnerability**: Lack of authentication in TPMS protocol
- **MITRE**: T1609
- **Impact**: Driver distraction, unnecessary servicing
- **Tools**: TPMS Simulator, SDR
- **Scenario**: The attacker uses a TPMS simulator to send fake low-pressure alerts, distracting or alarming the driver.
- **Attack Steps**: 1. Analyze TPMS frequency band (315 MHz / 433 MHz). 2. Capture TPMS packet structure using SDR. 3. Use a TPMS simulator to craft low-pressure alert messages. 4. Broadcast spoofed packets near the car while it's parked or moving. 5. The dashboard displays incorrect tire warnings. 6. Monitor driver behavior—possible stop or inspection.
- **Detection**: Analyze packet origin; check sensor ID mismatches
- **Solution**: Adopt encrypted TPMS protocols with vehicle authentication
- **Tags**: tpms, rf-spoofing, tire-sensors

## Radar Spoofing with RF Reflections

- **Attack Type**: Radar Spoofing
- **Target**: Automotive Radar
- **Vulnerability**: Inability to distinguish spoofed RF returns
- **MITRE**: T1609
- **Impact**: False vehicle detection, braking triggers
- **Tools**: Corner reflectors, drones
- **Scenario**: An attacker manipulates radar signals using reflectors to simulate moving vehicles.
- **Attack Steps**: 1. Identify vehicle radar frequency (e.g., 24 GHz or 77 GHz). 2. Construct or place corner reflectors that strongly reflect radar. 3. Position reflectors on poles or flying drones to simulate oncoming cars. 4. Observe vehicle behavior: unexpected braking or swerving. 5. Move reflectors dynamically to simulate motion.
- **Detection**: Analyze radar reflections against LIDAR and camera confirmation
- **Solution**: Apply Doppler filtering, AI-based filtering on object movement
- **Tags**: radar, spoofing, adas

## Portable GPS Jammer for Fleet Confusion

- **Attack Type**: GPS Jamming
- **Target**: Fleet Vehicles
- **Vulnerability**: No GPS fallback or signal validation
- **MITRE**: T1612
- **Impact**: Disrupted logistics and asset tracking
- **Tools**: Portable GPS Jammer
- **Scenario**: A portable jammer is used during delivery vehicle movement to disable GPS tracking and fleet monitoring.
- **Attack Steps**: 1. Acquire a battery-powered GPS jammer. 2. Approach or trail the delivery vehicle. 3. Switch on jammer intermittently to confuse GPS receiver. 4. Vehicle location data disappears from central fleet dashboard. 5. Disrupt delivery optimization or geo-fence alerts.
- **Detection**: Monitor signal loss frequency; audit route anomalies
- **Solution**: Enforce geo-fencing via hybrid GPS + cellular + inertial tracking
- **Tags**: gps-jammer, logistics, fleet

## Malicious Repeater for GPS Drift

- **Attack Type**: GPS Spoofing
- **Target**: Car GPS Unit
- **Vulnerability**: Repeater signal overrides legitimate signal
- **MITRE**: T1612
- **Impact**: Navigation inconsistency and ADAS errors
- **Tools**: GPS Repeater, coax cable
- **Scenario**: A GPS repeater is used to repeat indoor signals outdoors, causing slow location drift.
- **Attack Steps**: 1. Install a GPS antenna outdoors to capture legit signals. 2. Route the signal to an indoor GPS repeater using coaxial cable. 3. Place repeater near target car. 4. Vehicle GPS starts receiving out-of-place signals. 5. Car location drifts slowly toward repeater location.
- **Detection**: Signal strength triangulation; detect sudden shift in satellite geometry
- **Solution**: GPS anti-spoofing firmware, inertial backups
- **Tags**: gps-drift, repeater, car-hack

## TPMS Packet Replay Using SDR

- **Attack Type**: TPMS Replay Attack
- **Target**: TPMS Sensors
- **Vulnerability**: Replayable, unverified RF packet protocol
- **MITRE**: T1609
- **Impact**: Undermines driver trust in alerts
- **Tools**: HackRF One, GNU Radio
- **Scenario**: Attacker captures and replays TPMS packets to simulate repeated alerts.
- **Attack Steps**: 1. Use HackRF to sniff and record TPMS packets near the target vehicle. 2. Analyze recorded packets in GNU Radio. 3. Identify packet burst timing and format. 4. Replay the captured packets periodically. 5. Vehicle displays repetitive low-pressure alerts. 6. Driver may disable or ignore TPMS—leading to real safety risks.
- **Detection**: Track repetition patterns; validate timing mismatch
- **Solution**: Implement rolling codes and encrypted messages
- **Tags**: tpms, replay-attack, rf-analysis

## Simulated Obstacle Injection with LIDAR

- **Attack Type**: LIDAR Spoofing
- **Target**: LIDAR Subsystem
- **Vulnerability**: Susceptible to timed light pulses
- **MITRE**: T1609
- **Impact**: Braking or path change due to ghost object
- **Tools**: Pulsed Laser Diode, Oscilloscope
- **Scenario**: An attacker simulates virtual objects on the road using laser injection.
- **Attack Steps**: 1. Use a pulsed laser aligned to LIDAR wavelength. 2. Synchronize pulses to LIDAR scan timing. 3. Emit pulses at expected return intervals to simulate nearby object. 4. LIDAR system detects phantom object and relays to ADAS. 5. Observe system reaction (slowdown, stop, warning).
- **Detection**: Time-domain analysis on object persistence
- **Solution**: Use secure LIDAR with redundancy & scene understanding
- **Tags**: lidar-injection, spoof, laser

## False Vehicle Detected via Radar Manipulation

- **Attack Type**: Radar Spoofing
- **Target**: Radar Sensor
- **Vulnerability**: Radar reflection used to simulate traffic
- **MITRE**: T1609
- **Impact**: Lane drift, driver confusion
- **Tools**: Metal sheet, angle frame
- **Scenario**: Use of metal structures to mislead radar into detecting false vehicles in adjacent lane.
- **Attack Steps**: 1. Identify radar field of view (typically in bumper). 2. Place angled reflective sheet in radar path on roadside. 3. Reflected signal mimics a vehicle in adjacent lane. 4. Watch as car shifts lanes or alerts driver of proximity. 5. Can be used to force lane departure or slow driving.
- **Detection**: Cross-reference radar objects with LIDAR & camera
- **Solution**: Radar object verification & redundant sensors
- **Tags**: radar-fake, adjacent-vehicle, automotive

