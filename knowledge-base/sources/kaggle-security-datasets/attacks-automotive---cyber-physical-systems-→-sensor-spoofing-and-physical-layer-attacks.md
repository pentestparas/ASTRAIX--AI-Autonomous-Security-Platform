# Automotive / Cyber-Physical Systems → Sensor Spoofing & Physical Layer Attacks Attacks

## Ultrasonic Sensor Spoofing

- **Attack Type**: Physical Layer Manipulation
- **Target**: Vehicle Sensors
- **Vulnerability**: Lack of sensor authentication
- **MITRE**: T1557.001 (Adversary-in-the-Middle: Wireless)
- **Impact**: Driver distraction or false alerts
- **Tools**: Ultrasonic Generator, SDR
- **Scenario**: An attacker uses ultrasonic emitters to interfere with parking assist systems or collision detection
- **Attack Steps**: 1. Set up an ultrasonic emitter capable of emitting signals in the 40 kHz+ range.2. Place the device near the rear or front bumper of a vehicle.3. Emit continuous or pulsed signals to mimic the presence of an obstacle.4. Monitor the infotainment display to confirm that proximity warnings are triggered.5. Tune signal strength and direction to maintain effect without detection.
- **Detection**: Cross-sensor correlation, unexpected parking assist activation
- **Solution**: Shielding, multi-sensor verification
- **Tags**: ultrasonic, spoofing, driver assist

## Ambient Light Sensor Exploitation

- **Attack Type**: Sensor Confusion
- **Target**: Vehicle Sensors
- **Vulnerability**: No validation for sensor input source
- **MITRE**: T1565.002 (Stored Data Manipulation)
- **Impact**: Improper headlight activation, safety risks at night
- **Tools**: High-lumen flashlight
- **Scenario**: Exploit automatic headlight adjustment based on ambient light sensor values
- **Attack Steps**: 1. Identify the position of the ambient light sensor (usually on the dashboard or near the windshield).2. Shine a high-lumen flashlight to simulate bright ambient light.3. Observe whether the automatic headlight system turns off or adjusts incorrectly.4. Sustain or pulse the light to create flickering or system confusion.5. Exploit timing (e.g., tunnels) to disorient the driver.
- **Detection**: Discrepancy between sensor and external camera feeds
- **Solution**: Use of verified ambient sensors with shielding
- **Tags**: sensor spoof, headlight, driver safety

## Microphone Hijack in Voice Assistant

- **Attack Type**: Audio Injection
- **Target**: Infotainment System
- **Vulnerability**: No filtering of inaudible frequency ranges
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Unauthorized commands, privacy risks
- **Tools**: DolphinAttack setup, ultrasonic modulator
- **Scenario**: Exploit voice assistants via inaudible commands or hidden audio
- **Attack Steps**: 1. Use an ultrasonic modulator to embed voice commands above the human hearing range.2. Record commands like “navigate to...” or “call...” into the ultrasonic stream.3. Broadcast the signal toward the infotainment mic.4. Observe if the voice assistant responds to hidden commands.5. Chain with navigation or phone features for privacy compromise.
- **Detection**: Logging of voice assistant activity
- **Solution**: Filter input frequency range
- **Tags**: audio injection, voice control, dolphin attack

## Temperature Sensor Tampering

- **Attack Type**: Physical Tampering
- **Target**: Environment Sensors
- **Vulnerability**: No hardware verification of sensor readings
- **MITRE**: T1562.007 (Impair Defenses: Sensor Manipulation)
- **Impact**: System inefficiencies, battery damage in EVs
- **Tools**: Heat gun, ice spray
- **Scenario**: Attack climate control or battery cooling systems by spoofing temperature sensors
- **Attack Steps**: 1. Locate external temperature sensor ports under the hood or bumper.2. Apply heat or cold via tools (heat gun or ice spray).3. Observe HVAC behavior—e.g., max cooling engaged unnecessarily.4. For EVs, may impact battery thermal management.5. Monitor system logs for anomalies or overrides.
- **Detection**: Abnormal temperature deltas across sensors
- **Solution**: Sensor validation through software/firmware
- **Tags**: thermal spoofing, battery abuse, EV

## Infrared Key Fob Signal Flooding

- **Attack Type**: Wireless Signal Abuse
- **Target**: Entry Systems
- **Vulnerability**: Lack of signal validation or authentication
- **MITRE**: T1608.002 (Develop Capabilities: Signal Spoofing)
- **Impact**: Unauthorized entry, lockout
- **Tools**: IR LED array, microcontroller
- **Scenario**: Disrupt infrared sensor on older cars by continuously sending IR signals
- **Attack Steps**: 1. Assemble a powerful IR LED array and program it with generic unlock signal patterns.2. Flood the IR receiver on the vehicle with rapid pulses.3. Observe whether the vehicle unlocks or disables due to confusion.4. This is often used on older IR-based remote entry systems.5. Repeat with varying codes to bypass weak signal validation.
- **Detection**: Signal timing logs, physical camera verification
- **Solution**: Upgrade to RF encrypted systems
- **Tags**: IR, spoof, signal abuse

## Wi-Fi Deauthentication to Force App Reconnect

- **Attack Type**: Wireless Network Interruption
- **Target**: Infotainment System
- **Vulnerability**: Weak Wi-Fi authentication or session persistence
- **MITRE**: T1499.001 (Endpoint Denial of Service)
- **Impact**: Navigation disruption, app injection
- **Tools**: Aireplay-ng, Wireshark
- **Scenario**: Disconnect car's infotainment or navigation app from cloud for downgrade
- **Attack Steps**: 1. Use a wireless adapter to monitor Wi-Fi traffic between vehicle and hotspot.2. Identify MAC address of car's interface.3. Send deauth frames using Aireplay-ng to interrupt connection.4. Observe if fallback app versions or cached maps are activated.5. Chain this with DNS spoofing for further control.
- **Detection**: Monitor for repeated deauth frames
- **Solution**: Use WPA3 + deauth protection
- **Tags**: wifi spoof, DoS, app hijack

## Audio Frequency Jam on Proximity Sensors

- **Attack Type**: Frequency Interference
- **Target**: Driver Assist Sensors
- **Vulnerability**: No interference resistance in sensor design
- **MITRE**: T1498.001 (Network Denial of Service: Physical Layer)
- **Impact**: Sensor blackout during maneuvering
- **Tools**: Signal generator, speaker array
- **Scenario**: Emit noise to jam acoustic parking or blind-spot detection sensors
- **Attack Steps**: 1. Tune a signal generator to 40–50 kHz (used in ultrasonic sensors).2. Direct signal toward vehicle sensors while reversing or turning.3. The jamming signal overwhelms echo pulses.4. Driver sees sensor failure or no alert for real obstacles.5. Exploit this to cause parking collisions or evade detection.
- **Detection**: Sensor health diagnostics
- **Solution**: Add redundancy and shielding
- **Tags**: sensor jam, proximity, ultrasonic

## TPM Sensor Frame Replay

- **Attack Type**: RF Replay
- **Target**: TPMS
- **Vulnerability**: No anti-replay protection in sensor comm
- **MITRE**: T1636.001 (Manipulate Sensor Data)
- **Impact**: Tire burst risk, driver unaware
- **Tools**: HackRF, Universal Radio Hacker
- **Scenario**: Replay old tire pressure RF packets to hide a real deflation event
- **Attack Steps**: 1. Capture tire pressure sensor RF signals during normal driving.2. Save valid packets and associated timing.3. During a real leak or flat, replay those frames using HackRF.4. Vehicle displays incorrect "normal" tire pressure.5. This can lead to unawareness of critical tire conditions.
- **Detection**: Sudden pressure drop with no alert
- **Solution**: Use secure TPM comm (rolling code)
- **Tags**: TPMS, replay, HackRF

## Accelerometer Spoof via Vibrations

- **Attack Type**: Mechanical Induction
- **Target**: IMU Sensors
- **Vulnerability**: Susceptibility to vibrational spoofing
- **MITRE**: T1562.007 (Impair Defenses)
- **Impact**: Safety feature misfires
- **Tools**: Vibration motor, Arduino
- **Scenario**: Trick accelerometer readings by applying vibrational patterns
- **Attack Steps**: 1. Identify area near vehicle IMU (Inertial Measurement Unit).2. Attach or place vibration motor with programmable frequency.3. Emit vibrations in ranges that affect MEMS accelerometers.4. Cause fake readings, e.g., sudden deceleration.5. Could trigger false crash or anti-lock brake logic.
- **Detection**: Inertial reading vs GPS/gyro mismatch
- **Solution**: Sensor fusion validation
- **Tags**: accelerometer, MEMS, spoof

## Head-Up Display (HUD) Light Interference

- **Attack Type**: Visual Disruption
- **Target**: Display Systems
- **Vulnerability**: No protection from directed light interference
- **MITRE**: T1499.002 (Display Denial of Service)
- **Impact**: Visual disorientation, missed navigation cues
- **Tools**: Laser pointer, LED array
- **Scenario**: Blind or distort HUD with targeted light, especially at night
- **Attack Steps**: 1. Determine angle of driver’s HUD reflection from outside.2. Use laser pointer or powerful LED to interfere with light path.3. Create glares or make HUD unreadable during driving.4. Can be synchronized with curve turns for max disruption.5. Can affect navigation and alerts while driving.
- **Detection**: Eye movement tracking or alert mismatch
- **Solution**: Add glare-resistant optics
- **Tags**: HUD, laser, DoS

