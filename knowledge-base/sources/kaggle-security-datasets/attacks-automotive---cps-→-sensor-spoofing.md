# Automotive / CPS → Sensor Spoofing Attacks

## Radio Interference with Parking Sensors

- **Attack Type**: RF Interference
- **Target**: Embedded Sensor
- **Vulnerability**: Lack of sensor shielding
- **MITRE**: T0810 (Signal Interference)
- **Impact**: False readings may lead to minor collisions or system disablement
- **Tools**: SDR, RF Jammers
- **Scenario**: Attacker uses a modified RF transmitter to interfere with ultrasonic parking sensors, causing the vehicle to misdetect nearby obstacles.
- **Attack Steps**: 1. Locate the vehicle's ultrasonic parking sensors, typically on the rear and front bumpers. 2. Use an SDR device (like HackRF) or a wideband RF jammer tuned to interfere with ultrasonic frequencies (40kHz). 3. Transmit jamming or echo-mimicking signals to confuse the parking sensors. 4. Observe the in-car display showing false proximity warnings or lack of obstacle detection. 5. In extreme cases, use amplified directional emitters to affect sensors from a distance.
- **Detection**: Cross-check with camera feeds, measure sensor anomalies
- **Solution**: Implement cross-sensor validation and signal integrity checks
- **Tags**: spoofing, RF, automotive, ultrasonic

## False Emergency Braking Trigger via Radar Reflection

- **Attack Type**: Radar Spoofing
- **Target**: ADAS (Radar)
- **Vulnerability**: Lack of scene understanding in radar
- **MITRE**: T0811 (Sensor Spoofing)
- **Impact**: Vehicle brakes unnecessarily, may cause accidents
- **Tools**: Corner Reflector, Metallic Plates
- **Scenario**: Simulating an approaching vehicle to trigger automatic emergency braking (AEB)
- **Attack Steps**: 1. Understand the radar frequency used by the vehicle (typically 77 GHz or 24 GHz). 2. Set up a large flat metal surface or specialized radar corner reflector on the road. 3. Position the reflector to bounce radar waves directly back to the radar system, simulating a fast-approaching vehicle. 4. The vehicle misinterprets the return signal as a potential collision threat. 5. Automatic braking is triggered even though no real vehicle exists.
- **Detection**: Correlate with camera/LiDAR input
- **Solution**: Radar-camera fusion with AI validation
- **Tags**: radar, spoofing, ADAS, AEB

## Blind Spot Monitoring Manipulation via LIDAR Reflection

- **Attack Type**: LIDAR Spoofing
- **Target**: Blind Spot Sensors
- **Vulnerability**: LIDAR lacks spoof detection
- **MITRE**: T0811
- **Impact**: Disruption of driver awareness
- **Tools**: IR Reflectors, Spinning Mirrors
- **Scenario**: Reflecting false signals into LIDAR sensors to simulate vehicles in blind spot
- **Attack Steps**: 1. Identify where the LIDAR is mounted and its field of view. 2. Position IR-reflective materials (e.g., mirror or retroreflectors) at the right angle to reflect LIDAR pulses back to the sensor. 3. Use a rotating mirror system or timed reflectors to simulate movement. 4. The system detects phantom vehicles in the blind spot. 5. Driver receives false warnings, preventing lane change.
- **Detection**: Compare with radar/camera views
- **Solution**: Sensor fusion and anomaly filtering
- **Tags**: lidar, spoofing, blind spot

## GPS Rollback to Mislead OTA Time Validation

- **Attack Type**: GPS Time Spoofing
- **Target**: Infotainment/Update System
- **Vulnerability**: Reliance on GPS time without authentication
- **MITRE**: T0805 (Time Spoofing)
- **Impact**: Bypass update validation, timeline confusion
- **Tools**: GPS-SDR, GPS Jammer
- **Scenario**: Overwriting GPS time to bypass time-based OTA verification or disrupt logs.
- **Attack Steps**: 1. Setup a GPS simulator (like GPS-SDR-SIM) with a fake GPS date/time broadcast. 2. Jam authentic GPS briefly to allow takeover with the spoofed signal. 3. Transmit coordinates along with an outdated UTC timestamp to vehicle GPS. 4. The vehicle accepts the spoofed signal and updates system time. 5. OTA updates relying on timestamp validation may get bypassed or logging becomes inaccurate.
- **Detection**: Cross-check with NTP or internal RTC
- **Solution**: Multi-source time validation
- **Tags**: gps, spoofing, OTA, updates

## Headlight Auto-Level Spoofing Using Light Interference

- **Attack Type**: Optical Sensor Spoofing
- **Target**: Optical Sensors
- **Vulnerability**: Lack of shielding for ambient sensors
- **MITRE**: T0850
- **Impact**: Reduced visibility, nighttime hazard
- **Tools**: Laser Pointer, Light Source
- **Scenario**: Mislead auto-leveling headlight system by altering light sensor input
- **Attack Steps**: 1. Determine the location of ambient light sensors used for headlight auto-leveling. 2. Shine a high-lumen flashlight or modulated laser beam directly into the sensor. 3. The sensor interprets the false light as increased brightness from surroundings. 4. Headlight angle is automatically adjusted downwards, reducing visibility. 5. This may lead to unsafe night driving or driver confusion.
- **Detection**: Log light input levels, verify via camera
- **Solution**: Sensor shielding, fusion with camera input
- **Tags**: light spoofing, sensor, headlights

## Tampering Yaw Sensor for Steering Misinterpretation

- **Attack Type**: Sensor Tampering
- **Target**: IMU/Yaw Sensor
- **Vulnerability**: Susceptible to EM interference
- **MITRE**: T0851 (Sensor Distortion)
- **Impact**: Erroneous vehicle control, VSC triggers
- **Tools**: Magnet, EM Pulse
- **Scenario**: Mislead the system about vehicle's rotational motion via magnetic/electrical disturbance
- **Attack Steps**: 1. Locate yaw rate sensor typically mounted on vehicle center axis. 2. Bring a strong rare-earth magnet or EM pulse generator near the sensor enclosure. 3. Induce interference or shift sensor reading artificially. 4. Steering and stability control interpret fake rotational motion. 5. Vehicle may apply incorrect steering adjustments or show warning.
- **Detection**: Cross-check with wheel sensors
- **Solution**: Shielding and redundancy
- **Tags**: sensor, yaw, steering spoofing

## Sudden Brake Warning via Tail Light Sensor Spoof

- **Attack Type**: Optical Signal Spoofing
- **Target**: Optical Sensors
- **Vulnerability**: Misidentification of patterns
- **MITRE**: T0811
- **Impact**: Unwarranted slowdown, traffic disruption
- **Tools**: LED Matrix, Strobe
- **Scenario**: Fake the brake lights of a vehicle ahead to trigger automatic braking
- **Attack Steps**: 1. Use a programmable LED panel or high-frequency strobe to simulate flashing brake light patterns. 2. Place it on a stationary object or even wear it on a following bike. 3. Vehicle behind interprets it as real brake lights via optical sensors. 4. Adaptive systems may reduce speed or initiate soft braking. 5. Can be used to manipulate vehicle flow or create congestion.
- **Detection**: Camera confirmation, cross-check behavior
- **Solution**: Image pattern validation via AI
- **Tags**: brake light spoof, optical trick

