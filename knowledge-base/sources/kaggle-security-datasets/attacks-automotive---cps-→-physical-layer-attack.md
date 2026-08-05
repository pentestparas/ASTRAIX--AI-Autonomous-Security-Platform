# Automotive / CPS → Physical Layer Attack Attacks

## Inducing TPMS Warning Using RF Injection

- **Attack Type**: TPMS Spoofing
- **Target**: TPMS System
- **Vulnerability**: No encryption/authentication on TPMS
- **MITRE**: T0850 (Wireless Spoofing)
- **Impact**: Driver distraction, false maintenance
- **Tools**: TPMS Emulator, SDR
- **Scenario**: Attacker fakes a low-pressure alert on the Tire Pressure Monitoring System using RF injection.
- **Attack Steps**: 1. Identify the TPMS frequency used by the target vehicle (typically 315 MHz or 433 MHz). 2. Use a TPMS signal emulator or SDR (e.g., Yard Stick One) to craft and transmit low-pressure TPMS frames. 3. Broadcast the signal near the vehicle while it is idle or moving slowly. 4. The vehicle receives the spoofed signal, believing the tire pressure is dangerously low. 5. Dashboard warning is triggered, potentially distracting the driver or prompting unnecessary actions.
- **Detection**: Check tire pressure manually, correlate multiple sensors
- **Solution**: Use authenticated TPMS signals
- **Tags**: spoofing, RF, TPMS, safety

## Adaptive Cruise Control Jam via Radar Jamming

- **Attack Type**: Radar Interference
- **Target**: Radar System
- **Vulnerability**: Radar unprotected from jamming
- **MITRE**: T0810
- **Impact**: ACC disabled, driver caught off-guard
- **Tools**: RF Jammer, SDR
- **Scenario**: Disrupt adaptive cruise control by denying accurate radar returns.
- **Attack Steps**: 1. Identify radar frequency band used by vehicle (e.g., 77GHz). 2. Use a directional jammer emitting continuous wave signals in that band. 3. Aim at the front bumper area where radar sensors reside. 4. The system fails to detect vehicles ahead and either disables itself or switches to manual. 5. This may cause abrupt deactivation or risk of rear-end collision.
- **Detection**: Alert on loss of signal, radar error logs
- **Solution**: Radar error mitigation, fallback systems
- **Tags**: radar, jamming, adaptive cruise

## Lane Departure Warning Manipulation via Paint/Decals

- **Attack Type**: Optical Deception
- **Target**: Lane Detection Cameras
- **Vulnerability**: Poor validation of road lines
- **MITRE**: T0850
- **Impact**: False lane correction, driver mistrust
- **Tools**: Paint, Stickers
- **Scenario**: Trick camera-based lane detection by painting false lines or adding road decals
- **Attack Steps**: 1. Identify the lane detection camera (often front-facing, near windshield). 2. Place white or yellow tape/paint on the road surface mimicking lane markers. 3. Ensure spacing and curvature matches typical road lines. 4. The vehicle camera interprets the false lines as legitimate, triggering unwanted lane warnings. 5. This may cause false corrections or disablement of lane-keeping assist.
- **Detection**: Scene validation with map/GPS
- **Solution**: Advanced AI validation of road context
- **Tags**: spoofing, lane markings, camera attack

