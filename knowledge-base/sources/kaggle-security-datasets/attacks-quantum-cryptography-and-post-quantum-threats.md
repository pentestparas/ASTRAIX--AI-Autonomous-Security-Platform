# Quantum Cryptography & Post-Quantum Threats Attacks

## Intercept-Resend Attack on BB84 QKD Protocol

- **Attack Type**: QKD Implementation Attack
- **Target**: Quantum Communication Channel
- **Vulnerability**: Poor authentication of quantum states
- **MITRE**: T1020 (Automated Exfiltration)
- **Impact**: Partial key exposure; bit error increase
- **Tools**: Quantum Emulator, Polarizer Filter, QKD Lab Sim, Wireshark
- **Scenario**: An attacker attempts to eavesdrop on the quantum channel by measuring and resending photons during a BB84 key exchange.
- **Attack Steps**: Step 1: Set up a QKD simulator running BB84 protocol. Step 2: Configure a “man-in-the-middle” device to intercept the photon stream. Step 3: Measure each intercepted photon with a random basis. Step 4: Resend a photon with the same measured state to the receiver. Step 5: Analyze the resulting bit errors and detect rate of detection by legitimate users.
- **Detection**: QBER (Quantum Bit Error Rate) Monitoring
- **Solution**: Use decoy states and authentication for quantum states
- **Tags**: BB84, MITM, Quantum Attack

## Detector Blinding Attack on Single-Photon Detectors

- **Attack Type**: QKD Side-Channel Attack
- **Target**: QKD Receiver
- **Vulnerability**: Vulnerable photon detectors
- **MITRE**: T1595 (Active Scanning)
- **Impact**: Full key compromise in worst-case
- **Tools**: Laser Diode, QKD Device Emulator, Power Meter
- **Scenario**: The attacker uses strong light pulses to blind avalanche photodiodes (APDs) and manipulate their behavior to control bit values.
- **Attack Steps**: Step 1: Emulate a QKD device with exposed APD-based detectors. Step 2: Direct strong classical light pulses toward the detector to force linear behavior. Step 3: Send your own light pulses during blinded state to force output. Step 4: Analyze the public key reconciliation process to extract bits. Step 5: Compare manipulated vs expected key to demonstrate successful intrusion.
- **Detection**: Optical power anomaly detection
- **Solution**: Replace APDs with secure detectors; use watchdog circuits
- **Tags**: QKD, Side-Channel, Blinding Attack

## Time-Shift Attack on QKD Timing Window

- **Attack Type**: Timing-Based Side-Channel
- **Target**: QKD Timing Interface
- **Vulnerability**: Unprotected timing bias in detector window
- **MITRE**: T1001.003 (Data Obfuscation: Protocol Impersonation)
- **Impact**: Partial leakage of key bits
- **Tools**: QKD Timing Analyzer, Oscilloscope, Python QKD Sim
- **Scenario**: Exploiting timing mismatches in detection windows to bias bit detection and leak information about key bits.
- **Attack Steps**: Step 1: Analyze timing specs of a basic QKD setup. Step 2: Observe the detection window on the receiver end. Step 3: Shift the arrival time of photons (± a few ns) using a fiber delay. Step 4: Observe if receiver favors certain bit values depending on timing. Step 5: Calculate information leakage from biased detections.
- **Detection**: Timing irregularity logging
- **Solution**: Equalize detector sensitivity; use randomization
- **Tags**: QKD, Timing Leak, Side-Channel

## Trojan-Horse Attack via Fiber Reflection

- **Attack Type**: Optical Injection Attack
- **Target**: QKD Transmitter Module
- **Vulnerability**: Lack of isolation on optical ports
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Secret leakage through reflections
- **Tools**: Bright Pulse Generator, Optical Reflectometer, Fiber Taps
- **Scenario**: The attacker injects bright light into the quantum channel and analyzes back-reflected light to infer internal device states.
- **Attack Steps**: Step 1: Create a bright light pulse using laser diode. Step 2: Inject this pulse into the QKD system via optical fiber interface. Step 3: Capture reflected light signals from the device's internal modulators. Step 4: Analyze back-reflected signals to determine encoding settings. Step 5: Use this info to deduce future key bits.
- **Detection**: Optical port shielding logs
- **Solution**: Use optical isolators; monitor for unusual reflections
- **Tags**: Fiber Attack, QKD, Trojan-Horse

## Fake State Injection in Weak Coherent Pulse Protocol

- **Attack Type**: Fake Quantum State Injection
- **Target**: QKD Optical Receiver
- **Vulnerability**: Insecure weak coherent source handling
- **MITRE**: T1562.001 (Impair Defenses: Disable or Modify Tools)
- **Impact**: Key poisoning; bit flipping
- **Tools**: Low-Intensity Laser, Pulse Generator, QKD Receiver Emulator
- **Scenario**: Attacker crafts classical signals that mimic weak quantum pulses to trick receiver into accepting falsified key bits.
- **Attack Steps**: Step 1: Configure a test QKD system using Weak Coherent Pulse (WCP) method. Step 2: Send classical low-energy laser pulses at the expected quantum rate. Step 3: Adjust pulse intensity to mimic single-photon levels. Step 4: Inject pulses with known polarization to bias bit values. Step 5: Compare accepted key values at the receiver to assess bit control success.
- **Detection**: Compare photon stats vs expected threshold
- **Solution**: Use decoy states and randomness tests
- **Tags**: QKD, Fake State, Signal Injection

## Phase Remapping Attack on QKD Modulators

- **Attack Type**: Modulation Timing Exploit
- **Target**: Phase-Based QKD Transmitter
- **Vulnerability**: Lack of timing calibration on phase modulator
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Partial key recovery
- **Tools**: Optical Delay Line, Phase Modulator Analyzer, QKD Simulator
- **Scenario**: An attacker alters phase encoding timing to mislead phase detection during BB84 execution.
- **Attack Steps**: Step 1: Emulate a QKD system with phase encoding (e.g., BB84 variant).Step 2: Introduce a delay in the phase modulator using an optical delay line.Step 3: Shift encoded photon phase slightly from its expected state.Step 4: Measure how the receiver misinterprets bit values.Step 5: Use public reconciliation info to recover bits from the manipulated state.
- **Detection**: Phase state logs
- **Solution**: Add phase-locking mechanisms & verification checks
- **Tags**: QKD, Phase Attack, Delay Exploit

## Calibration Attack via Fake Feedback Pulses

- **Attack Type**: Feedback Spoofing
- **Target**: QKD Alignment Feedback Loop
- **Vulnerability**: Trust in unverified calibration pulses
- **MITRE**: T1565.002 (Data Manipulation: Stored Data)
- **Impact**: Undetected key compromise
- **Tools**: Optical Pulse Generator, QKD Lab Environment
- **Scenario**: Attacker sends fake calibration pulses that manipulate alignment of photon sources.
- **Attack Steps**: Step 1: During the calibration phase, introduce fake pulses that imitate legitimate calibration signals.Step 2: Slightly shift these fake pulses to cause misalignment in polarization or phase.Step 3: Allow system to complete key generation using misaligned references.Step 4: Use known misalignment to infer correct bits.Step 5: Compare eavesdropped bits with reconciled key bits.
- **Detection**: Monitor calibration feedback frequency
- **Solution**: Authenticate calibration source signals
- **Tags**: QKD, Fake Pulse, Calibration Exploit

## Exploiting Dead Time in Photon Detectors

- **Attack Type**: Detector Timing Abuse
- **Target**: Single-Photon Detector
- **Vulnerability**: No randomization in detection timing
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Biased key bit generation
- **Tools**: Photon Source, Oscilloscope, Detector Emulation Software
- **Scenario**: Attacker manipulates timing to send photons when detectors are inactive (dead time), influencing which bit gets registered.
- **Attack Steps**: Step 1: Observe detector dead time behavior (duration when it's unresponsive after detection).Step 2: Intentionally send photons just outside the normal detection window.Step 3: Reduce chances of one detector firing, biasing the other.Step 4: Monitor public discussion between parties to guess bit outcomes.Step 5: Demonstrate impact of timing manipulation on key bias.
- **Detection**: Detector dead time monitoring
- **Solution**: Add randomized dead-time variation
- **Tags**: Timing Attack, Detector Bias

## Saturation Attack on Quantum Channel

- **Attack Type**: Denial-of-QKD Attack
- **Target**: QKD Optical Channel
- **Vulnerability**: No filtering of excess photon injection
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: QKD key generation halt
- **Tools**: High-Power Laser, Beam Splitter
- **Scenario**: Overloads QKD system by flooding quantum channel with fake photons, making it unusable.
- **Attack Steps**: Step 1: Identify the wavelength range used by the quantum channel.Step 2: Continuously inject high-frequency fake photon pulses.Step 3: Monitor QKD system's quantum bit error rate (QBER).Step 4: Observe system aborting key generation due to overload.Step 5: Prove DoS (Denial-of-Service) via complete key disruption.
- **Detection**: QBER logging system
- **Solution**: Use narrowband filters and overload detectors
- **Tags**: QKD, Denial of Service, Photon Flood

## Beam Splitter Ratio Manipulation

- **Attack Type**: Hardware Manipulation Attack
- **Target**: Optical Receiver
- **Vulnerability**: Beam splitter sensitivity to ratio shifts
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Weak keys due to imbalance
- **Tools**: Beam Splitter Kit, Optical Tuner, Calibration Logs
- **Scenario**: Attacker slightly alters beam splitter ratio in the receiver to bias detection probability.
- **Attack Steps**: Step 1: Access receiver hardware and slightly alter the beam splitter (e.g., 50:50 to 60:40).Step 2: Observe bias in the number of 0s vs 1s generated in key.Step 3: Use this imbalance to infer certain bit values.Step 4: Validate bit bias using reconciliation logs.Step 5: Show how small changes can break key randomness.
- **Detection**: Bit parity deviation monitoring
- **Solution**: Calibrate splitters periodically & seal hardware
- **Tags**: QKD, Hardware Exploit

## Finite-Key Exploit via Session Truncation

- **Attack Type**: Statistical Weakness Exploit
- **Target**: QKD Protocol Session
- **Vulnerability**: Weak finite-key estimation model
- **MITRE**: T1565.001 (Data Manipulation: Transmitted Data)
- **Impact**: Undetected partial key compromise
- **Tools**: Network Interceptor, QKD Software Simulator
- **Scenario**: Ends key exchange early, before enough bits are exchanged to detect eavesdropping.
- **Attack Steps**: Step 1: Set up a session using a finite-key QKD protocol.Step 2: Send a TCP RST packet or simulate dropout to end exchange prematurely.Step 3: Receiver assumes valid key if minimal bits match.Step 4: Eavesdrop and compare leaked vs generated key bits.Step 5: Demonstrate attack bypassed threshold error detection.
- **Detection**: Monitor session length thresholds
- **Solution**: Enforce minimum bits per session before key finalization
- **Tags**: QKD, Short Session Exploit

## Exploiting Polarization Drift Without Compensation

- **Attack Type**: Drift Exploit Attack
- **Target**: Fiber-Based QKD Setup
- **Vulnerability**: No dynamic polarization compensation
- **MITRE**: T1609 (Lateral Movement)
- **Impact**: Gradual key corruption; leakage
- **Tools**: Fiber Rotator Kit, Polarization Analyzer
- **Scenario**: Attacker slowly rotates fiber over time, exploiting systems without polarization compensation.
- **Attack Steps**: Step 1: Run a long-duration QKD session over fiber.Step 2: Slowly rotate the optical fiber to cause gradual drift.Step 3: Observe whether the system detects increase in QBER.Step 4: Drift creates bit-flip patterns attacker can use to guess bits.Step 5: Log drift rate vs recovered bit accuracy.
- **Detection**: QBER vs drift correlation
- **Solution**: Install dynamic polarization compensators
- **Tags**: QKD, Drift Attack

## Entangled Photon Substitution Attack

- **Attack Type**: Entanglement Exploit
- **Target**: Entangled Photon Channel
- **Vulnerability**: Poor entanglement source authentication
- **MITRE**: T1637 (Data Manipulation: Protocol Tunneling)
- **Impact**: Predictable bits in shared key
- **Tools**: Entangled Photon Source, Polarization Monitor
- **Scenario**: Attacker introduces fake entangled photons in place of legitimate ones to insert bias.
- **Attack Steps**: Step 1: Intercept photon pair being sent via entanglement-based QKD (e.g., E91).Step 2: Replace with attacker-generated entangled pair, preset with known values.Step 3: Allow receiver to measure incoming fake photon.Step 4: Extract bit values from attacker’s entanglement base.Step 5: Compare intercepted and final keys.
- **Detection**: Verify entanglement correlation
- **Solution**: Authenticate quantum sources
- **Tags**: QKD, Entanglement, Fake Source

## Classical Channel Metadata Exploitation

- **Attack Type**: Metadata Analysis
- **Target**: Classical Network Interface
- **Vulnerability**: No obfuscation of classical meta-data
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Partial key reconstruction
- **Tools**: Wireshark, TCP Dump, QKD Lab Software
- **Scenario**: Attacker sniffs classical channel metadata to derive timing or bit inference.
- **Attack Steps**: Step 1: Monitor classical communication between QKD parties (public discussion phase).Step 2: Analyze message timing, bit rejection ratios, etc.Step 3: Infer which bases are more common or rejected.Step 4: Use side-channel info to reconstruct partial key.Step 5: Simulate multiple sessions to prove key pattern leakage.
- **Detection**: Secure channel metadata logging
- **Solution**: Add padding/random delay in metadata traffic
- **Tags**: QKD, Metadata Exploit, Side Channel

## Fake Basis Announcement Replay Attack

- **Attack Type**: Classical Protocol Exploit
- **Target**: QKD Public Channel
- **Vulnerability**: No replay protection on classical messages
- **MITRE**: T1001.001 (Data Obfuscation: Junk Data)
- **Impact**: Bit mismatch; denial of valid key
- **Tools**: TCP Replay Tool, QKD Public Channel Logger
- **Scenario**: Replays previously recorded basis announcements to confuse QKD parties during reconciliation.
- **Attack Steps**: Step 1: Record a valid session’s basis reconciliation messages.Step 2: Replay them during a different QKD session.Step 3: Force parties to accept incorrect basis info.Step 4: Cause key mismatch or bias in accepted bits.Step 5: Show resulting key errors and proof of tampering.
- **Detection**: Message ID & nonce mismatch detection
- **Solution**: Use session nonce & digital signatures
- **Tags**: Replay Attack, Classical Protocol

## Quantum Channel Switching Delay Attack

- **Attack Type**: Protocol Timing Exploit
- **Target**: QKD Relay Node or Router
- **Vulnerability**: Delay variance between photon streams
- **MITRE**: T1498.001 (Network Denial of Service)
- **Impact**: Partial key prediction via time analysis
- **Tools**: QKD Switch Emulator, Timing Logger, Network Delay Injector
- **Scenario**: Exploiting delay introduced during switching between different quantum channels to guess timing-based key info.
- **Attack Steps**: Step 1: Set up a QKD system with multi-channel photon routing (e.g., satellite-ground).Step 2: Measure delay differences during channel switching phases.Step 3: Introduce additional delay packets between channel hops.Step 4: Record when receiver accepts or discards bits.Step 5: Correlate delays with accepted bits and reconstruct portions of the key.
- **Detection**: Log latency across sessions
- **Solution**: Equalize switching time using synchronized buffers
- **Tags**: QKD, Delay Injection, Channel Timing

## Basis-Dependent Efficiency Attack

- **Attack Type**: Detection Bias Exploit
- **Target**: Photon Detection Module
- **Vulnerability**: Efficiency bias in polarization detectors
- **MITRE**: T1071.001 (Application Layer Protocol: Web Protocols)
- **Impact**: Reduced randomness and key leakage
- **Tools**: Polarization Analyzer, QKD Detector Emulator, Light Source
- **Scenario**: Exploits the fact that some QKD detectors have higher sensitivity to certain polarizations, allowing attacker to bias measurement.
- **Attack Steps**: Step 1: Set up a polarized photon stream using a calibrated light source.Step 2: Measure detection efficiency of QKD system across all four BB84 polarizations.Step 3: Identify which polarization yields higher detection rates.Step 4: Bias your injected photon pulses toward that polarization.Step 5: Confirm if more bits are accepted when using biased polarization and infer leaked bits.
- **Detection**: Compare bit frequency against ideal uniform distribution
- **Solution**: Use uniform-efficiency detectors or post-selection techniques
- **Tags**: Polarization Attack, Detector Bias

## After-Gate Attack on Gated APD Detectors

- **Attack Type**: Timing Exploit on Detectors
- **Target**: APD-based Detector in QKD
- **Vulnerability**: Residual sensitivity after gate window
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Hidden bit injection outside detection window
- **Tools**: Pulsed Laser Diode, Gated Detector Emulator
- **Scenario**: Sends faint light pulses right after detector gate closes, taking advantage of residual sensitivity.
- **Attack Steps**: Step 1: Emulate a QKD system with APD detectors gated in time windows.Step 2: Carefully time light pulses to arrive just after the detector gate closes.Step 3: Observe if detector still occasionally registers those as valid photons.Step 4: Use this loophole to slowly insert bits known to attacker.Step 5: Analyze final keys to detect any matching bits with injected sequence.
- **Detection**: Temporal anomaly detection in logs
- **Solution**: Enforce hard shutoff and gate time extensions
- **Tags**: QKD, After-Gate Injection

## Local Oscillator (LO) Manipulation in CV-QKD

- **Attack Type**: Continuous Variable Exploit
- **Target**: CV-QKD Systems
- **Vulnerability**: Unsecured LO transmission
- **MITRE**: T1583.006 (Acquire Infrastructure: Web Services)
- **Impact**: Incorrect key reconstruction; signal injection
- **Tools**: CV-QKD Emulator, Laser Source, LO Analyzer
- **Scenario**: Manipulating the local oscillator used in homodyne detection in CV-QKD to alter measurement results.
- **Attack Steps**: Step 1: Set up a CV-QKD system simulation using homodyne detection.Step 2: Inject noise or altered signals into the local oscillator (LO) sent along with signal.Step 3: Cause a drift in the measurement quadrature by misaligning LO phase.Step 4: The altered LO leads to wrong interpretation of Gaussian modulation.Step 5: Use public reconciliation messages to recover Gaussian key distribution.
- **Detection**: Compare LO phase with internal reference
- **Solution**: Use LO-independent detection (e.g., pilot-aided schemes)
- **Tags**: CV-QKD, Local Oscillator Attack

## Weak Random Number Generator Attack

- **Attack Type**: RNG Exploit
- **Target**: QKD Transmitter Logic
- **Vulnerability**: Weak PRNG or poor entropy source
- **MITRE**: T1027.006 (Obfuscated Files or Information: HTML Smuggling)
- **Impact**: Full key prediction if PRNG is compromised
- **Tools**: PRNG Analyzer, RNG Weakness Checker, QKD Simulator
- **Scenario**: Exploits poorly seeded random number generator (RNG) used for basis or key selection in QKD.
- **Attack Steps**: Step 1: Access or simulate a QKD setup that uses classical PRNG for basis selection.Step 2: Analyze entropy or seed reuse in PRNG through output analysis.Step 3: Reconstruct PRNG internal state using known seed patterns.Step 4: Predict next set of basis choices and synchronize eavesdropping.Step 5: Match leaked bits to final key and prove prediction accuracy.
- **Detection**: RNG entropy test and output analysis
- **Solution**: Use hardware-based TRNGs (True RNGs)
- **Tags**: PRNG, RNG, QKD Weakness

## EM Radiation Leakage from Quantum Key Distribution (QKD) Device

- **Attack Type**: Side-Channel via EM Emanation
- **Target**: QKD Transmitter
- **Vulnerability**: EM radiation emissions not shielded
- **MITRE**: T1208 - Hardware Fault Injection
- **Impact**: Quantum key recovery
- **Tools**: Software-defined radio (SDR), EM probe, GNU Radio
- **Scenario**: Attacker sets up an EM probe near a QKD transmitter to pick up radiation leakage revealing qubit state patterns.
- **Attack Steps**: Step 1: Set up an EM probe (e.g., Langer RF-U 5-2) within 50 cm of the QKD transmitter. Step 2: Connect the probe to an SDR (e.g., HackRF or USRP). Step 3: Use GNU Radio or SDR# to tune into high-frequency EM emissions. Step 4: Log EM spikes during qubit state generation (timed with known test transmission). Step 5: Analyze repeated patterns to infer qubit polarization angles.
- **Detection**: RF anomaly monitoring, shielding, and EM leakage audit
- **Solution**: Add EM shielding, use TEMPEST-rated enclosures
- **Tags**: EM Leakage, QKD, SDR

## Acoustic Cryptanalysis on Superconducting Qubits

- **Attack Type**: Acoustic Side-Channel Attack
- **Target**: Quantum Processor (Cryogenic)
- **Vulnerability**: Acoustic leaks from switching hardware
- **MITRE**: T1040 - Network Sniffing (Audio Interpretation variant)
- **Impact**: Quantum gate sequence leakage
- **Tools**: High-sensitivity microphone, parabolic dish, audio analysis tools
- **Scenario**: Attacker places a parabolic microphone near a dilution refrigerator housing quantum processor and detects mechanical sounds correlating with gate operations.
- **Attack Steps**: Step 1: Place a parabolic dish mic aimed at cryostat from 2–3 meters away. Step 2: Record background audio during controlled gate operations. Step 3: Use tools like Audacity to isolate time-domain pulse patterns. Step 4: Train a classifier on noise profiles of each type of quantum gate (X, H, CNOT). Step 5: During normal operation, classify leaked sounds to infer running gates.
- **Detection**: Anomalous audio spectrum detection
- **Solution**: Noise isolation + acoustic dampening inside cryostat housing
- **Tags**: Acoustic, Qubits, Cryostat

## Power Analysis on Quantum Random Number Generator (QRNG)

- **Attack Type**: Power Side-Channel
- **Target**: QRNG device
- **Vulnerability**: Power fluctuation reveals internal state
- **MITRE**: T1203 - Exploitation for Client Execution (QRNG leak variant)
- **Impact**: RNG prediction
- **Tools**: Oscilloscope, power tap, ChipWhisperer Lite
- **Scenario**: An attacker analyzes subtle fluctuations in power usage of a QRNG device to distinguish between quantum and pseudo-random outputs.
- **Attack Steps**: Step 1: Install a power tap (low-res shunt resistor) inline with QRNG power supply. Step 2: Connect to oscilloscope or ChipWhisperer. Step 3: Trigger power traces during QRNG output cycles. Step 4: Analyze amplitude/phase shifts in power draw to distinguish entropy sources. Step 5: Predict or bias output by manipulating known noisy states.
- **Detection**: Inline power draw monitoring
- **Solution**: Add power line noise filtering, randomized delay injection
- **Tags**: QRNG, Power, Side Channel

## RF Injection to Influence Quantum Interference

- **Attack Type**: RF Injection / EMI Attack
- **Target**: QKD Receiver
- **Vulnerability**: Susceptibility to high-frequency RF noise
- **MITRE**: T1496 - Resource Hijacking (via induced error)
- **Impact**: Degraded QKD performance, denial of service
- **Tools**: Signal generator, RF antenna, Faraday probe
- **Scenario**: Attacker transmits malicious RF interference to disrupt superposition state stability in a nearby QKD receiver.
- **Attack Steps**: Step 1: Place a directional RF antenna within 2 meters of QKD receiver. Step 2: Transmit high-frequency burst (e.g., 5 GHz) timed with photon arrival. Step 3: Observe increased bit error rate in QKD link. Step 4: Adjust frequency to identify resonant interference range. Step 5: Log disruption level vs. signal strength for repeatability.
- **Detection**: Signal-to-noise monitoring, QKD error rate audit
- **Solution**: Hardened shielding, real-time error correction tuning
- **Tags**: EMI, QKD, RF Interference

## Timing Analysis of Photonic Gates in Quantum Chips

- **Attack Type**: Timing Side-Channel
- **Target**: Photonic Quantum Chip
- **Vulnerability**: Timing leak via light emission delay
- **MITRE**: T1003 - OS Credential Dumping (adapted to logic timing)
- **Impact**: Leak of gate design or QKD mode
- **Tools**: High-speed photodiodes, logic analyzer, timing capture software
- **Scenario**: Attacker measures external timing signals (e.g., clock jitter or light pulse timing) to reconstruct photon-gate combinations in photonic processors.
- **Attack Steps**: Step 1: Place high-speed photodiode near photonic chip with transparent casing. Step 2: Use a logic analyzer (e.g., Saleae) to record timestamped light pulses. Step 3: Analyze gate delay differences to map which logic gates were activated. Step 4: Repeat analysis to predict optical quantum circuit layout. Step 5: Use that layout to infer potential QKD protocol or algorithm running.
- **Detection**: Timing jitter baseline comparison
- **Solution**: Add timing randomization, light masking on chip
- **Tags**: Photonic, Timing, Logic

## Laser Fault Injection on Quantum RAM (qRAM)

- **Attack Type**: Optical Fault Injection
- **Target**: Quantum RAM
- **Vulnerability**: Photonic fault injection vulnerability
- **MITRE**: T1601 - Modify System Image (modified for hardware injection)
- **Impact**: Memory corruption and data exfiltration
- **Tools**: Low-power laser, microscope stage, camera
- **Scenario**: Attacker directs a laser at specific points of a qRAM circuit to induce computation errors and observe abnormal behavior.
- **Attack Steps**: Step 1: Place qRAM chip under a microscope with camera. Step 2: Identify the area of the chip where quantum memory access circuits are active. Step 3: Use a laser with precise targeting (~405nm, <5mW) to pulse the circuit during read/write operations. Step 4: Monitor deviations in quantum memory outputs after pulse injections. Step 5: Log and correlate specific injection patterns with observed read/write faults.
- **Detection**: Real-time monitoring of logic gates and error rates
- **Solution**: Shield qRAM with photonic isolation, use fault injection detectors
- **Tags**: Laser Injection, qRAM, Hardware

## Cold Boot Attack on Cryo-Control Board

- **Attack Type**: Cryo-Hardware Attack
- **Target**: Cryo-Controller Unit
- **Vulnerability**: Data remanence in RAM post-shutdown
- **MITRE**: T1005 - Data from Local System (Cold Boot Variant)
- **Impact**: Partial gate reconstruction, cloning
- **Tools**: Liquid nitrogen, screwdriver, RAM reader, gloves
- **Scenario**: By rapidly power-cycling and freezing the cryo-controller of a quantum computer, attacker attempts to recover residual configuration data.
- **Attack Steps**: Step 1: Shut down the quantum cryo-controller quickly via physical switch-off. Step 2: Spray liquid nitrogen on the cryo-board to preserve volatile memory. Step 3: Remove the RAM module and insert it into a cold-compatible reader. Step 4: Extract configuration bits related to quantum gate alignment or bias. Step 5: Reconstruct part of the quantum logic state initialization.
- **Detection**: RAM activity audit, boot-time integrity check
- **Solution**: Encrypt volatile RAM contents, instant zeroing on shutdown
- **Tags**: Cold Boot, Cryogenic, Config Leak

## EMI-Based Crosstalk on Superconducting Qubit Wires

- **Attack Type**: EMI Interference Side-Channel
- **Target**: Qubit PCB Lines
- **Vulnerability**: Inadequate shielding, signal bleeding
- **MITRE**: T1148 - Hardware Additions
- **Impact**: Leakage of active qubit states
- **Tools**: Coil-based RF injector, spectrum analyzer, oscilloscope
- **Scenario**: Attacker places electromagnetic source near chip wiring to analyze crosstalk between adjacent qubit control lines.
- **Attack Steps**: Step 1: Locate wiring traces of adjacent superconducting qubits on PCB. Step 2: Place a high-frequency coil injector (1-10 MHz) near the traces. Step 3: Induce subtle EMI signals and observe crosstalk using spectrum analyzer. Step 4: Log interference behavior during specific qubit operations (e.g., X or H gates). Step 5: Map the crosstalk leakage to identify qubit state transitions.
- **Detection**: EMI signature monitoring
- **Solution**: Redesign PCB layout to isolate qubit lines; add ground shielding
- **Tags**: EMI, Crosstalk, Qubit State

## Heat-Induced Decoherence in Ion Trap Qubits

- **Attack Type**: Thermal Side-Channel
- **Target**: Ion Trap Qubit Device
- **Vulnerability**: Heat sensitivity of ion-trap stability
- **MITRE**: T1499.004 - Endpoint Denial of Service: Resource Exhaustion
- **Impact**: Quantum decoherence, data corruption
- **Tools**: IR lamp, temperature sensor, EM field reader
- **Scenario**: Attacker uses an IR heat lamp or EM heater to introduce thermal noise into ion-trap systems, increasing decoherence rates.
- **Attack Steps**: Step 1: Aim a controlled IR heater at the ion trap vacuum chamber. Step 2: Gradually increase ambient temperature by 2-5°C during operations. Step 3: Monitor qubit coherence time using standard test circuits (e.g., Ramsey sequence). Step 4: Measure decline in interference fringes, indicating decoherence. Step 5: Log thermal gradient vs. decoherence correlation.
- **Detection**: Temperature drift sensors, qubit coherence watchdogs
- **Solution**: Thermal insulation, feedback cooling systems
- **Tags**: Ion Trap, Heat Leak, Decoherence

## Bluetooth-Based EM Sniffing of FPGA-Based Quantum Control

- **Attack Type**: Wireless EM Eavesdropping
- **Target**: Quantum Control FPGA
- **Vulnerability**: Emission of wireless side-band signals
- **MITRE**: T1422 - Indirect Command Execution (side-band control analysis)
- **Impact**: Control signal leakage, reverse engineering
- **Tools**: Bluetooth SDR, directional antenna, BLE sniffer tool
- **Scenario**: A modified Bluetooth sniffer picks up leakage from unshielded FPGAs driving quantum operations.
- **Attack Steps**: Step 1: Set up BLE sniffer tool (e.g., Ubertooth One) near FPGA controller. Step 2: Use a directional antenna to focus signal detection near circuit. Step 3: Scan for unintended EM or RF emissions synchronized with quantum pulses. Step 4: Record trace and analyze pulse patterns for input-output mappings. Step 5: Match emission fingerprints to gate instructions or control bits.
- **Detection**: RF emission sweep monitoring
- **Solution**: Harden FPGA board with ground planes and shielding
- **Tags**: Bluetooth, FPGA, EM Leak

## Sound Leakage through Resonance in Fiber QKD Setup

- **Attack Type**: Acoustic Side-Channel via Fiber
- **Target**: Fiber QKD Cable
- **Vulnerability**: Resonant vibration revealing modulated info
- **MITRE**: T1071.001 - Application Layer Protocol: Web Protocols (adapted)
- **Impact**: Partial key disclosure
- **Tools**: Laser mic, spectrogram software, QKD setup
- **Scenario**: Subtle resonant frequencies cause the optical fiber to vibrate under laser modulation, producing audible leakage.
- **Attack Steps**: Step 1: Place a laser microphone or vibration sensor near fiber optic cable. Step 2: Capture sound modulated by fiber vibrations during QKD pulses. Step 3: Perform time-frequency analysis using spectrogram tools. Step 4: Detect timing info correlating with key bit modulation (polarization/phase). Step 5: Estimate timing data to reconstruct transmitted key bits.
- **Detection**: Acoustic emission auditing
- **Solution**: Use vibration-dampening mounts and dual-layer shielding
- **Tags**: Acoustic, Fiber, QKD

## Cache Timing Analysis in Hybrid Quantum-Classical Systems

- **Attack Type**: Cache-Timing Side-Channel
- **Target**: Hybrid Classical-Quantum Controller
- **Vulnerability**: Cache reuse vulnerability
- **MITRE**: T1120 - Peripheral Device Discovery
- **Impact**: Leak of authentication secrets
- **Tools**: Flush+Reload script, Linux cache probe toolkit
- **Scenario**: Attacker uses cache timing attacks on classical CPU co-processor handling pre/post quantum operations.
- **Attack Steps**: Step 1: Launch Flush+Reload attack from a VM or local process. Step 2: Flush shared memory regions linked to classical computation. Step 3: Measure reload times during QKD authentication handshake. Step 4: Correlate delays with key handling subroutines. Step 5: Recover timing-sensitive memory access patterns indicating private key usage.
- **Detection**: Cache access timing detection tools
- **Solution**: Avoid shared memory, constant-time operations
- **Tags**: Cache Attack, Hybrid Quantum

## Fault Injection via Focused Magnetic Field

- **Attack Type**: Magnetic Side-Channel
- **Target**: Superconducting Qubit Gate
- **Vulnerability**: Susceptibility to magnetic disruption
- **MITRE**: T0812 - Hardware Fault Injection (adapted)
- **Impact**: Induced gate errors, QKD key corruption
- **Tools**: Helmholtz coil, magnetometer, oscilloscope
- **Scenario**: An attacker uses a handheld magnetic coil to induce gate-level faults in a superconducting quantum processor.
- **Attack Steps**: Step 1: Build a small directional magnetic coil (~200 mT range). Step 2: Position near superconducting gate circuit while running operations. Step 3: Pulse the magnetic field briefly during gate execution. Step 4: Measure anomalies in output qubit states. Step 5: Correlate gate malfunctions with coil pulse intensity.
- **Detection**: Output qubit state error tracking
- **Solution**: Use magnetic shielding, gate-level error correction
- **Tags**: Magnetic Coil, Fault Injection

## Visible Light Leakage during Photon Emission

- **Attack Type**: Optical Side-Channel
- **Target**: Photon Emitter in QKD Device
- **Vulnerability**: Optical emission timing leakage
- **MITRE**: T1123 - Audio Capture (visual variant)
- **Impact**: Partial QKD key recovery
- **Tools**: High-speed camera, darkroom, photodiode array
- **Scenario**: Visible light may leak unintentionally during photon generation in some QKD setups, observable from outside.
- **Attack Steps**: Step 1: Operate QKD device in darkroom. Step 2: Aim high-speed low-light camera at photon emitter housing. Step 3: Record emission intervals. Step 4: Compare visible light intensity variation with qubit transmission states. Step 5: Infer bit encoding timing and potential key bits.
- **Detection**: Light spectrum monitoring in darkroom
- **Solution**: Seal emitter with opaque coating; use IR-only emitters
- **Tags**: Visible Light, QKD

## Unintentional RF Modulation of Qubit Readout Circuits

- **Attack Type**: RF Leakage Side-Channel
- **Target**: Qubit Readout Circuit
- **Vulnerability**: Emission during qubit collapse/readout
- **MITRE**: T1408 - Exploit Public-Facing Application (timing variant)
- **Impact**: Post-measurement data leakage
- **Tools**: RTL-SDR, RF analyzer, GNU Radio
- **Scenario**: Readout circuitry of superconducting qubits may unintentionally emit RF signals during measurement.
- **Attack Steps**: Step 1: Set up an SDR (e.g., RTL-SDR) near qubit measurement hardware. Step 2: Monitor spectrum in the 100 MHz – 3 GHz range. Step 3: Identify periodic RF bursts matching readout timing. Step 4: Decode amplitude/pulse-width information to infer state collapse results. Step 5: Log RF profiles for different known qubit states.
- **Detection**: RF burst monitoring
- **Solution**: Design RF-filtered output stages
- **Tags**: RF Modulation, Qubit Readout

## Machine Learning Reconstruction of Power Side-Channels

- **Attack Type**: ML-Augmented Side-Channel
- **Target**: QKD Controller Circuit
- **Vulnerability**: Statistical correlation of leaked signals
- **MITRE**: T1602 - Data from Configuration Repository
- **Impact**: Partial or full recovery of quantum key material
- **Tools**: ChipWhisperer, oscilloscope, Python ML libraries (scikit-learn, TensorFlow)
- **Scenario**: Attacker uses AI to train a model that predicts QKD circuit behavior based on leaked power traces, even with noisy environments.
- **Attack Steps**: Step 1: Use ChipWhisperer to capture hundreds of power traces during repeated QKD circuit operation. Step 2: Label trace samples based on known operations (like qubit entanglement, polarization shifts). Step 3: Feed labeled data into a neural network for classification. Step 4: Train the model to recognize patterns in trace spikes. Step 5: Use the model to interpret new traces during actual QKD sessions, inferring bit patterns or key entropy.
- **Detection**: ML trace anomaly analysis, model inversion monitoring
- **Solution**: Introduce noise randomization, fake operations (decoys)
- **Tags**: Power Analysis, Machine Learning, QKD

## TEMPEST Attack on Quantum-Classical Interface

- **Attack Type**: Electromagnetic Eavesdropping
- **Target**: Quantum-Classical Workstation
- **Vulnerability**: Monitor cable radiates readable EM emissions
- **MITRE**: T1010 - Application Window Discovery (via EM)
- **Impact**: QKD key disclosure via video leak
- **Tools**: TEMPEST-grade EM probe, Faraday-locked analyzer, RF shield
- **Scenario**: Attacker captures electromagnetic radiation from a classical display connected to a quantum system (e.g., to extract keys during output display).
- **Attack Steps**: Step 1: Position EM probe outside secure room but near monitor cable path. Step 2: Capture radiated signals during key or result display from classical interface. Step 3: Analyze leaked signal patterns using software-defined radio interface. Step 4: Reconstruct screen content (e.g., base64 QKD key segments or ciphertext). Step 5: Log decoded content and determine impact on confidentiality.
- **Detection**: RF field monitoring, signal power anomaly detection
- **Solution**: Replace VGA/HDMI with fiber or shielded DVI; Faraday shielding
- **Tags**: EM Leak, TEMPEST, QKD Output

## Timing Desynchronization Exploit in Quantum-Classical Gate Control

- **Attack Type**: Clock Drift Timing Attack
- **Target**: Quantum-Classical Timing Bus
- **Vulnerability**: Sensitive to classical-clock skew
- **MITRE**: T1499.001 - DoS via Clock Manipulation
- **Impact**: Causes decoherence, logic failure, or wrong key generation
- **Tools**: Precision timer, software-inserted delay loop, oscilloscope
- **Scenario**: Attacker introduces intentional delays into the classical control unit, causing subtle drift between expected and actual gate timings.
- **Attack Steps**: Step 1: Identify the interface between quantum gate control hardware and classical CPU. Step 2: Modify classical CPU software or inject delay via timing loop (milliseconds). Step 3: Use scope to monitor gate pulse deviations. Step 4: Observe how delay alters entanglement gate precision or causes decoherence. Step 5: Collect quantum error metrics and correlate with delay values.
- **Detection**: Gate operation delay tracking
- **Solution**: Harden timing with quartz sync; watchdog timers
- **Tags**: Timing Attack, Clock Drift, Decoherence

## Residual Magnetic Signature Exploit in Superconducting Loops

- **Attack Type**: Magnetic Remanence Attack
- **Target**: Superconducting Qubit Loop
- **Vulnerability**: Magnetic memory of previous gate current
- **MITRE**: T1208 - Hardware Fault Injection (remanence variant)
- **Impact**: Leakage of gate patterns or logic sequences
- **Tools**: Fluxgate magnetometer, liquid helium shield bypass, vibration isolation
- **Scenario**: After quantum operations, superconducting circuits may retain weak magnetic states detectable by sensitive magnetometers.
- **Attack Steps**: Step 1: Let QKD device complete a session and cool to rest. Step 2: Carefully bring magnetometer near control chip (cryostat surface). Step 3: Capture residual magnetic field patterns. Step 4: Compare field lines with known qubit configurations or gate usage. Step 5: Reconstruct possible gate history or key-related paths from magnetic footprint.
- **Detection**: Magnetic sweep post-operations
- **Solution**: Auto-zeroing of circuits post-op, physical magnetic shielding
- **Tags**: Residual Field, Superconducting, Magnetometer

## Optical Probing of Integrated Photonic Circuits

- **Attack Type**: Light Injection Side-Channel
- **Target**: Photonic Integrated QKD Chip
- **Vulnerability**: Internal light path modulation visible from outside
- **MITRE**: T1610 - Exploitation via Optical Channel
- **Impact**: Partial optical circuit reconstruction
- **Tools**: Low-power fiber laser, photodiode array, darkroom
- **Scenario**: Attacker injects low-level external light through semi-transparent chip casing and observes how internal reflections vary with gate usage.
- **Attack Steps**: Step 1: Place photonic QKD chip under low-power near-IR laser probe. Step 2: Shine light from different angles into casing with IR reflectivity coating. Step 3: Place photodiode sensors to detect outgoing reflection intensity. Step 4: Map reflection changes to internal gate activity. Step 5: Infer internal waveguide activation patterns (phase, polarization) to guess key behavior.
- **Detection**: Optical reflectometry audit
- **Solution**: Use opaque casing, limit light entry points
- **Tags**: Photonic Chip, Optical Side-Channel

## Spoofing Entangled Qubits in Free-Space Quantum Link

- **Attack Type**: Fake Entanglement Injection
- **Target**: Free-space Quantum Transmitter/Receiver
- **Vulnerability**: Absence of real-time entanglement verification
- **MITRE**: T1562.009
- **Impact**: Full compromise of one-time pad key
- **Tools**: Quantum random number generator, Pulse laser, Phase modulator, SDR
- **Scenario**: An attacker near a free-space quantum communication link between Alice and Bob injects spoofed photons that imitate entangled pairs.
- **Attack Steps**: Step 1: Identify the physical location of the line-of-sight quantum free-space link.Step 2: Deploy an optical receiver to synchronize with the transmitted photon stream.Step 3: Use a phase modulator to imitate entanglement by injecting photons with predictable phase correlations.Step 4: Randomize timing of injection to avoid detection by simple time checks.Step 5: Intercept classical key reconciliation process to validate fake photon matches.Step 6: Record all matched key bits accepted by Bob as valid.Step 7: Use SDR to jam or delay legitimate photon pulses when needed.
- **Detection**: Check Bell inequality violation on random samples
- **Solution**: Use real-time entanglement verification tests, switch to fiber for sensitive applications
- **Tags**: quantum, wireless, spoof, entanglement, fake photon

## Mimicking Entangled Qubits in RF-Controlled Quantum Lab Setup

- **Attack Type**: Fake Entanglement Injection
- **Target**: Internal QKD Lab Setup
- **Vulnerability**: Unauthenticated RF command channels
- **MITRE**: T1557
- **Impact**: Key generation with fake entanglement
- **Tools**: Wi-Fi Pineapple, SDR (HackRF), Python script to simulate QKD behavior
- **Scenario**: An internal wireless device is used to inject fake data in a lab-based QKD protocol setup by mimicking entanglement over radio controls.
- **Attack Steps**: Step 1: Connect to internal lab Wi-Fi or compromise IoT device in lab (e.g., a smart camera).Step 2: Listen to RF-based control messages exchanged between QKD control units.Step 3: Inject synthetic “successful entanglement” messages at the same timing as the actual entanglement events.Step 4: Feed manipulated data to Bob’s system using MQTT or API endpoint spoofing.Step 5: Let Bob confirm a fake Bell test, believing the photons were entangled.Step 6: Log key data as it is accepted as genuine.Step 7: Erase injection traces after session completes.
- **Detection**: Cross-check quantum state logs with classical channel logs
- **Solution**: Use secure/authenticated communication for RF control channels
- **Tags**: wireless-lab, QKD, insider, MQTT, spoof

## Injecting Fake Photons in a Satellite-Based QKD

- **Attack Type**: Fake Entanglement Injection
- **Target**: Satellite-ground QKD system
- **Vulnerability**: No physical authentication of photons
- **MITRE**: T1608
- **Impact**: Partial compromise of key exchange
- **Tools**: Drone with directional photon emitter, GPS jammer, polarization modulator
- **Scenario**: An attacker deploys a drone carrying a directional quantum emitter to inject signals mimicking photons from a satellite-based QKD system.
- **Attack Steps**: Step 1: Use a telescope to align with the ground station receiving quantum signals from the satellite.Step 2: Fly drone to optimal injection height, avoiding LOS obstruction.Step 3: Emit single photons with pre-calculated polarization values aligned with the satellite’s modulation scheme.Step 4: Use GPS jammer to temporarily interfere with satellite sync timing.Step 5: Monitor classical channel to match Bob’s basis choices and inject suitable responses.Step 6: Collect accepted key bit sequences from reconciliation.Step 7: Exit flight path before satellite scan re-aligns.
- **Detection**: Check polarization error rates and sync mismatches
- **Solution**: Use decoy-state protocols and photon origin verification
- **Tags**: satellite, drone, injection, entanglement, GPS

## Entanglement Signal Tampering via BLE Relay Attack

- **Attack Type**: Fake Entanglement Injection
- **Target**: BLE-based QKD Device
- **Vulnerability**: Insecure BLE pairing & lack of data validation
- **MITRE**: T1557.001
- **Impact**: Full key compromise via spoofed entanglement signals
- **Tools**: BLE relay (Nordic dev kits), Custom Android App, MITM Proxy
- **Scenario**: Exploiting BLE-based synchronization in a commercial QKD device, attacker relays and manipulates signals to simulate entanglement patterns.
- **Attack Steps**: Step 1: Identify BLE channel used between control app and QKD hardware.Step 2: Place two BLE relays – one near app, one near hardware.Step 3: Use MITM proxy to relay BLE packets in real-time, altering timestamps/data.Step 4: Change photon pattern identifiers to match predictable sequences.Step 5: Intercept classical transmission to validate fake qubit matches.Step 6: Continuously log accepted keys by Bob.Step 7: Maintain relay until entire session ends.
- **Detection**: BLE signal integrity and timing checks
- **Solution**: Enforce BLE secure pairing with session authentication
- **Tags**: BLE, QKD, wireless relay, spoofed quantum

## Hijacking Quantum Channel Negotiation via Rogue Access Point

- **Attack Type**: Fake Entanglement Injection
- **Target**: Wi-Fi based QKD controller
- **Vulnerability**: Trust in unauthenticated initial handshake
- **MITRE**: T1185
- **Impact**: Key leakage via fake entanglement logs
- **Tools**: Rogue AP, Wireshark, Ettercap, DNS spoof
- **Scenario**: During initial setup, attacker creates a rogue Wi-Fi AP mimicking QKD router, injecting false entanglement status updates.
- **Attack Steps**: Step 1: Set up rogue access point with same SSID and stronger signal than QKD control AP.Step 2: Redirect Alice/Bob devices to attacker’s server during key negotiation.Step 3: Send false logs showing successful entanglement events.Step 4: Allow continuation of classical key exchange with manipulated data.Step 5: Drop or modify validation packets that would detect mismatch.Step 6: Log and store final symmetric keys exchanged.Step 7: Shutdown AP once session finishes.
- **Detection**: Analyze network logs for rogue AP connections
- **Solution**: Use secure out-of-band verification of QKD setup phase
- **Tags**: WiFi, rogue AP, QKD, quantum hijack

## Man-in-the-Middle Injection of Simulated Qubits in Air-Gapped QKD Lab

- **Attack Type**: Fake Entanglement Injection
- **Target**: Air-gapped QKD Testbed
- **Vulnerability**: Physical security breach; insecure signal domain
- **MITRE**: T1205
- **Impact**: Undetected falsification of QKD state
- **Tools**: SDR (e.g., HackRF), QKD lab emulator, Raspberry Pi, PIR sensors
- **Scenario**: Attacker places a wireless relay inside an air-gapped lab environment to manipulate the photon exchange phase.
- **Attack Steps**: Step 1: Attacker physically enters the environment (e.g., during maintenance).Step 2: Places a hidden Raspberry Pi with Wi-Fi/SDR to passively monitor entangled photon sequences.Step 3: Sets SDR to emit simulated photon signals with matched polarization angles.Step 4: Aligns signal to interfere only during entanglement verification.Step 5: Replaces half of actual qubits with generated values.Step 6: Attacker collects classical channel data via remote Wi-Fi link.Step 7: Simulates Bell test compliance using matched injection pattern.
- **Detection**: Real-time comparison with out-of-band monitoring
- **Solution**: Physical hardening and tamper-detection of lab
- **Tags**: airgap, QKD lab, RF injection, MITM, physical attack

## Remote QKD Session Hijack via Wi-Fi Command Channel Fuzzing

- **Attack Type**: Fake Entanglement Injection
- **Target**: Wi-Fi Controlled QKD Device
- **Vulnerability**: Unauthenticated device control interface
- **MITRE**: T1211
- **Impact**: Key material generated from fake entangled signals
- **Tools**: Wi-Fi Deauther, Fuzzing tool (boofuzz), Fake photon emitter
- **Scenario**: Fuzzing commands of a Wi-Fi controlled quantum transceiver, attacker injects fake photon timing logs.
- **Attack Steps**: Step 1: Scan for exposed Wi-Fi APs labeled for QKD device management.Step 2: Use deauth attacks to disconnect legitimate controller briefly.Step 3: Fuzz command interface to identify input formats.Step 4: Reconnect and send fake timing and polarization data via fuzzed commands.Step 5: Insert matched photon ID logs to simulate successful transmission.Step 6: Allow QKD system to reconcile and form key.Step 7: Log key content via spoofed management logs.
- **Detection**: Cross-reference photon detection logs
- **Solution**: Lock down command interface using secure APIs
- **Tags**: fuzzing, spoof, QKD hijack, Wi-Fi

## Entangled Photon Stream Redirection Using Signal Amplification

- **Attack Type**: Fake Entanglement Injection
- **Target**: Free-space Optical QKD Setup
- **Vulnerability**: Lack of signal source authentication
- **MITRE**: T1595
- **Impact**: Side-channel duplication of entanglement stream
- **Tools**: Optical signal amplifier, Reflective mirrors, SDR
- **Scenario**: Attacker uses a wireless optical amplifier to redirect weak entangled photon stream into fake receiver.
- **Attack Steps**: Step 1: Identify outdoor optical QKD link near a university research facility.Step 2: Set up signal mirror to reflect part of the photon stream.Step 3: Use amplifier to maintain photon intensity.Step 4: Introduce a fake detector near original receiver to absorb photons.Step 5: Inject own photons to the receiver with synchronized delay.Step 6: Listen to classical reconciliation to guess bit patterns.Step 7: Manipulate polarization basis with feedback loop.
- **Detection**: Validate photon origin using TOF analysis
- **Solution**: Add decoy photons with known positions
- **Tags**: optical, redirection, QKD beam, hijack

## Injection of Pre-Programmed Photon Pairs via Embedded SDR

- **Attack Type**: Fake Entanglement Injection
- **Target**: Internal Receiver Device
- **Vulnerability**: Embedded firmware injection & SDR misuse
- **MITRE**: T1209
- **Impact**: Full compromise of final shared key
- **Tools**: Embedded SDR chip, Custom photon schedule injector, Tampered firmware
- **Scenario**: Using a compromised embedded device with SDR, attacker preloads photon sequences that mimic entangled states.
- **Attack Steps**: Step 1: Physically implant tampered SDR device inside Bob’s QKD receiver.Step 2: Load device with fake entangled photon time-series, matching standard bases.Step 3: Activate during active QKD session and mask logs with timestamps.Step 4: Listen to basis announcement over classical channel.Step 5: Match fake responses in real-time.Step 6: Final key is partially or wholly constructed from injected photon records.Step 7: Attacker retrieves key via hidden BLE/LoRa module.
- **Detection**: Periodic firmware integrity checks
- **Solution**: Hardware root-of-trust with secure boot
- **Tags**: embedded, SDR, firmware, QKD compromise

## Replay Attack on Quantum Control Channel Using Wi-Fi Sniffer

- **Attack Type**: Fake Entanglement Injection
- **Target**: QKD Controller via Wi-Fi
- **Vulnerability**: Session replay due to insecure transport layer
- **MITRE**: T1639
- **Impact**: Spoofing of valid key generation
- **Tools**: Wireshark, Replay script (Scapy), Photon emitter
- **Scenario**: Captured photon timing and alignment data from Wi-Fi stream is replayed in next session to simulate successful QKD.
- **Attack Steps**: Step 1: Sniff Wi-Fi data during an active QKD handshake session.Step 2: Extract timestamps and alignment patterns for each entanglement.Step 3: Store and catalog event sequence as a replay file.Step 4: In a future session, pose as legitimate client and resend matching control data.Step 5: Emit synchronized photon pulses using matched sequence.Step 6: Replay correct classical bit-matching logs.Step 7: Final key appears valid but is attacker-controlled.
- **Detection**: Log session IDs and timestamps securely
- **Solution**: Use TLS + time-stamped quantum logs
- **Tags**: replay, spoof, quantum handshake

## BLE-Controlled Photon Generator Fake Injection via IoT Smart Plug

- **Attack Type**: Fake Entanglement Injection
- **Target**: Nearby IoT BLE Device
- **Vulnerability**: EM-based interference and signal confusion
- **MITRE**: T1203
- **Impact**: False photon detection, key contamination
- **Tools**: BLE smart plug, SDR, Pulsed LED
- **Scenario**: Smart plug near QKD controller is hijacked to emit EM signals that affect photon detectors, simulating photon arrival.
- **Attack Steps**: Step 1: Identify BLE smart plug used near photon detector for power management.Step 2: Gain access using default password or BLE sniffing.Step 3: Modify firmware to pulse LEDs during specific timing intervals.Step 4: Direct pulses toward photon detector to mimic weak photon arrival.Step 5: Sync with reconciliation protocol to match known base.Step 6: Allow system to accept photon events as real.Step 7: Remove plug remotely after key generation.
- **Detection**: Shielded photon paths and BLE device audit
- **Solution**: Disable BLE near sensitive lab optics
- **Tags**: IoT, EM, BLE, side-channel

## Exploiting Fast Basis Switching Lag to Inject Fake Photons

- **Attack Type**: Fake Entanglement Injection
- **Target**: High-speed QKD Device
- **Vulnerability**: Timing side-channel on polarization switching
- **MITRE**: T1621
- **Impact**: Partial key leakage through lag-timed injection
- **Tools**: Fast switch-lag analysis tool, Pulse laser, Polarization filter
- **Scenario**: Exploits timing delay in QKD basis switching mechanism to insert photons with predictable base.
- **Attack Steps**: Step 1: Analyze basis switching response delay in QKD system (e.g., 10 ns).Step 2: Craft a photon stream that emits during predictable switching periods.Step 3: Align laser pulse to hit detector during transition lag.Step 4: Use matching polarization filter to ensure bit acceptance.Step 5: Repeat to introduce multiple valid-looking photons.Step 6: Capture accepted bits from logs.Step 7: Exit without altering legitimate sessions.
- **Detection**: Real-time jitter analysis of basis switching
- **Solution**: Random delay added to basis transitions
- **Tags**: timing, lag injection, basis switch

## Wi-Fi AP Clone Tricking Remote Entangled Photon Source

- **Attack Type**: Fake Entanglement Injection
- **Target**: Remote-controlled QKD Device
- **Vulnerability**: No Wi-Fi AP origin verification
- **MITRE**: T1557
- **Impact**: Creation of fully spoofed key stream
- **Tools**: Rogue Wi-Fi AP, MAC address spoofer, Cloud API fuzzer
- **Scenario**: Creates cloned Wi-Fi AP to deceive cloud-controlled photon emitter, sending fake triggers to photon generator.
- **Attack Steps**: Step 1: Clone QKD controller’s Wi-Fi AP with identical SSID and MAC spoof.Step 2: Jam original AP using directional interference.Step 3: Redirect photon emitter control signals to fake AP.Step 4: Send fake API trigger via cloud spoof.Step 5: Photon emitter generates sequences based on fake inputs.Step 6: Intercept classical channel logs to reconcile keys.Step 7: Disconnect before authentication system flags session.
- **Detection**: Authenticate APs with fingerprinting
- **Solution**: Use out-of-band control signaling
- **Tags**: rogue AP, spoof, photon cloud

## Localized Microwave Burst to Simulate Quantum Channel Noise

- **Attack Type**: Fake Entanglement Injection
- **Target**: Fiber or open QKD link
- **Vulnerability**: Physical degradation masking attack
- **MITRE**: T1610
- **Impact**: Hidden injection in "noisy" channel
- **Tools**: Microwave gun, Polarization-adjusted photon source, SDR
- **Scenario**: A targeted microwave burst is used to cause errors in photon path, enabling attacker to sneak in matched photons.
- **Attack Steps**: Step 1: Identify photon transmission line and wavelength.Step 2: Generate short bursts of microwaves causing signal degradation.Step 3: Time photon injection during burst periods.Step 4: Emit matched polarization photons into degraded stream.Step 5: Let QKD system attribute loss to channel noise.Step 6: Inject predictable bits into final key.Step 7: Exit without sustained interference.
- **Detection**: Analyze loss patterns with source markers
- **Solution**: Increase resilience to physical degradation
- **Tags**: microwave, noise, photon masking

## Laser Injection via HVAC Vent to Tamper with Photon Measurement

- **Attack Type**: Fake Entanglement Injection
- **Target**: Physical Photon Receiver
- **Vulnerability**: Indirect optical signal path access
- **MITRE**: T1200
- **Impact**: Key material contamination via false detection
- **Tools**: Laser diode, HVAC duct probe, Pulse controller
- **Scenario**: Sends modulated laser pulses via building vents into lab to skew photon measurement outcome.
- **Attack Steps**: Step 1: Map HVAC system to lab room housing photon receiver.Step 2: Insert thin laser-emitting probe inside duct.Step 3: Fire pulses in sync with expected photon arrival window.Step 4: Pulse frequency matches polarization decoding threshold.Step 5: Receiver interprets false pulse as real photon.Step 6: Match polarization with attacker-controlled key.Step 7: Withdraw probe and seal duct.
- **Detection**: Air quality + light monitoring inside lab
- **Solution**: Secure HVAC paths and indirect optics
- **Tags**: laser, HVAC, lab penetration, spoof

## Wi-Fi Beacon Injection to Falsify QKD Entanglement Logs

- **Attack Type**: Fake Entanglement Injection
- **Target**: Wi-Fi-based QKD Controller
- **Vulnerability**: No authentication on beacon/frame layer
- **MITRE**: T1557.001
- **Impact**: Fake keys generated using forged system state
- **Tools**: Wi-Fi Deauther, Beacon spoofer (mdk3), Log forger script (Python)
- **Scenario**: An attacker spoofs Wi-Fi beacons and command-response cycles to falsify logs showing successful entanglement in QKD session initialization.
- **Attack Steps**: Step 1: Use a Wi-Fi sniffer to identify beacon patterns from QKD system’s control AP.Step 2: Launch a deauthentication attack to force reconnects from the QKD client device.Step 3: Use mdk3 or similar to broadcast fake beacon frames that mimic entanglement success triggers.Step 4: Respond to QKD handshake queries with pre-scripted success messages.Step 5: Modify local log files using Python scripts to insert timestamps and entangled bit info.Step 6: Let system proceed to key exchange phase with fabricated data.Step 7: Exfiltrate the forged logs for key recovery.
- **Detection**: Validate against external quantum event timestamps
- **Solution**: Cryptographic signing of entanglement event logs
- **Tags**: Wi-Fi spoof, logs, QKD forgery

## SDR Signal Collision to Override Quantum State in Photon Channel

- **Attack Type**: Fake Entanglement Injection
- **Target**: Open-air or fiber-based quantum channel
- **Vulnerability**: Weak signal collision handling
- **MITRE**: T1602
- **Impact**: Quantum state tampered, leading to key compromise
- **Tools**: HackRF One, Directional antenna, Polarization modulator
- **Scenario**: SDR is used to inject strong, polarized pulses that collide with legitimate photon stream to override quantum states received.
- **Attack Steps**: Step 1: Scan for operating quantum channel frequency and polarization encoding method.Step 2: Tune SDR to a precise frequency and adjust modulation to match photon polarization.Step 3: Inject timed signal bursts during photon transmission intervals.Step 4: Amplify signal power to ensure override of weak legitimate photons.Step 5: Monitor basis alignment from classical channel to fine-tune injections.Step 6: Override qubit readings and allow attacker-generated values to form the key.Step 7: Terminate injection before entropy tests are performed.
- **Detection**: Cross-check polarization error patterns
- **Solution**: Power-level normalization and noise analysis
- **Tags**: SDR, signal collision, polarization injection

## EM Resonance Attack via Wi-Fi Router Near Entangled Source

- **Attack Type**: Fake Entanglement Injection
- **Target**: Quantum photon generator near EM emitter
- **Vulnerability**: EM resonance susceptibility
- **MITRE**: T1200
- **Impact**: Entanglement timing compromised
- **Tools**: Custom RF generator, Modified Wi-Fi router, Oscilloscope
- **Scenario**: Exploiting EM resonance near entangled photon generator to cause timing misalignment and create room for injection.
- **Attack Steps**: Step 1: Place a modified Wi-Fi router with open firmware near the entangled photon source.Step 2: Modify firmware to emit high-frequency bursts aligned with system clock.Step 3: Measure resulting timing distortion using an oscilloscope.Step 4: Inject fake photons during distorted timing windows.Step 5: Monitor entanglement logs to confirm injected events were accepted.Step 6: Replay classical bits based on known injection times.Step 7: Shut down Wi-Fi emissions after key formation completes.
- **Detection**: Monitor for out-of-spec timing fluctuations
- **Solution**: Shield photon generation from RF interference
- **Tags**: EM injection, resonance, photon distortion

## BLE Command Injection into Mobile-Controlled QKD Device

- **Attack Type**: Fake Entanglement Injection
- **Target**: Mobile-BLE QKD Kit
- **Vulnerability**: Lack of BLE command authentication
- **MITRE**: T1631
- **Impact**: Key generated without any true entangled state
- **Tools**: Android BLE sniffer (nRF Connect), BLE packet injector, Fake event simulator
- **Scenario**: A mobile app connected via BLE to a QKD kit is spoofed to inject commands simulating quantum success without actual entanglement.
- **Attack Steps**: Step 1: Use BLE sniffer to scan for the QKD device during an active pairing.Step 2: Connect using same UUID and impersonate the mobile app.Step 3: Send command to “simulate entanglement success” using pre-crafted payloads.Step 4: Generate fake entanglement logs inside the device using command injection.Step 5: Allow system to proceed to final key stage with falsified values.Step 6: Capture logs via BLE notification channel for offline analysis.Step 7: Disconnect and block original app from re-pairing.
- **Detection**: BLE log mismatch analysis
- **Solution**: Encrypt BLE channels and whitelist controller app
- **Tags**: BLE spoof, mobile, command injection

## FPGA Firmware Manipulation to Broadcast Fake Photon States

- **Attack Type**: Fake Entanglement Injection
- **Target**: QKD FPGA-Controlled Transmitter
- **Vulnerability**: Firmware integrity not verified
- **MITRE**: T1542.001
- **Impact**: Full session hijack with attacker-owned photons
- **Tools**: FPGA dev board (e.g., Xilinx), Firmware flasher, JTAG debugger
- **Scenario**: FPGA inside the QKD transmitter is modified to broadcast synthetic qubits mimicking entanglement without actual photon interaction.
- **Attack Steps**: Step 1: Gain physical access to FPGA controlling the QKD photon source.Step 2: Connect via JTAG and extract existing firmware image.Step 3: Modify logic to skip real photon generation and instead output predefined polarization data.Step 4: Flash new firmware into FPGA and reboot device.Step 5: Allow system to transmit “fake entangled qubits” during QKD sessions.Step 6: Attacker records outgoing sequence since it’s known in advance.Step 7: Recover full key as the receiver accepts the manipulated states.
- **Detection**: Firmware checksums, side-channel checks
- **Solution**: Use signed firmware and secure boot chains
- **Tags**: FPGA, firmware spoof, photon emulator

## RF Interference in QKD Classical Channel

- **Attack Type**: MITM in QKD via Wireless Jamming
- **Target**: Wireless Classical Link in QKD
- **Vulnerability**: Weak RF interference protection; reliance on open-air classical channels
- **MITRE**: T1464 (Signal Interference), T1583 (Compromise Infrastructure)
- **Impact**: Loss of quantum key generation session integrity, denial of service
- **Tools**: HackRF One, SDR#, Kali Linux
- **Scenario**: An attacker uses RF jamming to disrupt the classical communication channel (used alongside the quantum channel) in a QKD system. This causes repeated key negotiation and increases the chance to insert MITM devices.
- **Attack Steps**: Step 1: Identify the frequency range used for classical channel communications in the QKD system using SDR scan.Step 2: Use HackRF to monitor the traffic and pinpoint control packet timing.Step 3: Generate RF noise at the classical communication frequency (e.g., Wi-Fi or LTE bands used for key negotiation between nodes).Step 4: Maintain intermittent jamming to force key renegotiation multiple times.Step 5: Set up a rogue access point imitating the quantum-classical hub controller.Step 6: Wait for one side to re-establish connection through the rogue point.Step 7: Relay messages while logging all classical key negotiation attempts.
- **Detection**: Monitor RF spectrum for anomalies, use spectrum analyzers
- **Solution**: Shield RF communication lines, use directional antennas, enable jamming detection
- **Tags**: QKD, RF Jamming, Wireless MITM, HackRF

## Fake QKD Hub Injection via Evil Twin AP

- **Attack Type**: Wireless Evil Twin MITM
- **Target**: Wi-Fi APs of QKD classical control layer
- **Vulnerability**: Lack of AP authentication, weak rogue detection
- **MITRE**: T1557.002 (Rogue Wireless Access Point)
- **Impact**: Potential metadata leakage, session hijack risk
- **Tools**: Aircrack-ng, Fluxion, Wireshark
- **Scenario**: A fake quantum key exchange hub (classical node) is set up via an Evil Twin Access Point to capture classical packets in a QKD protocol like BB84.
- **Attack Steps**: Step 1: Identify SSID and BSSID of the legitimate QKD control hub using airodump-ng.Step 2: Use Fluxion to create a fake AP using the same SSID and better signal strength.Step 3: Launch a deauthentication attack on legitimate users to force reconnection.Step 4: Intercept the classical packets sent during BB84 key sifting.Step 5: Relay messages to the actual hub after slight delay to avoid detection.Step 6: Log timing and bit-matching info for possible pattern prediction.Step 7: Repeat across multiple exchanges to accumulate metadata.
- **Detection**: Monitor for multiple APs with same SSID, validate AP certificates
- **Solution**: Use AP whitelisting and mutual certificate-based authentication
- **Tags**: QKD, Evil Twin, BB84, Wi-Fi MITM

## Laser Injection in Free-Space QKD Link

- **Attack Type**: Physical-layer MITM via Beam Injection
- **Target**: Optical Free-space QKD Systems
- **Vulnerability**: Lack of physical beam shielding or tamper alert
- **MITRE**: T1491 (Resource Hijacking), T1499 (Endpoint Denial of Service)
- **Impact**: Increased QBER, failure in key exchange, fallback to insecure methods
- **Tools**: 532nm Laser Pointer (tuned), Optical Filter, Telescope, QKD testbed
- **Scenario**: In free-space QKD (e.g., satellite or rooftop link), attacker uses a laser to subtly inject noise photons into the beam, altering quantum bit error rates (QBER) to cause disruption or force fallbacks.
- **Attack Steps**: Step 1: Set up line-of-sight to the QKD sender or receiver device (e.g., rooftop fiber-free-space link).Step 2: Align telescope to the beam path to locate optical receiver.Step 3: Fire controlled pulses of weak laser light (same wavelength) to cause collision with quantum signals.Step 4: Monitor the QBER from public classical channel (e.g., if system reports it).Step 5: Force the system to fall back to classical encryption due to persistent QBER.Step 6: During fallback, perform MITM via classical traffic interception.Step 7: Record timestamps of disturbances and verify alignment effectiveness.
- **Detection**: Monitor QBER trends for sudden spikes, analyze optical logs
- **Solution**: Beam enclosures, intrusion detection via photo diodes
- **Tags**: QKD, Laser MITM, Free-Space Quantum Comm

## Replay Attack on Classical QKD Channel via SDR

- **Attack Type**: Wireless Replay Attack in QKD Network
- **Target**: Wireless Classical QKD Control Channel
- **Vulnerability**: Replay acceptance, protocol lacks nonce or time-check
- **MITRE**: T1557 (Man-in-the-Middle), T1001.003 (Protocol Impersonation)
- **Impact**: Key generation fails, trust in session degrades
- **Tools**: SDR (HackRF), GNURadio, Scapy
- **Scenario**: Classical negotiation messages from a QKD session are recorded using SDR and replayed in later sessions to confuse participants or degrade key quality.
- **Attack Steps**: Step 1: Capture classical channel (e.g., ZigBee, Wi-Fi) using HackRF and GNURadio.Step 2: Identify QKD session control messages (usually tagged packets during sifting or error correction).Step 3: Store multiple full session packet sets with timestamps.Step 4: Replay old sessions at low rates to blend with real-time traffic.Step 5: Observe whether endpoints accept replayed info or if errors increase.Step 6: Trigger repeated errors to reduce trust in generated key.Step 7: Exploit errors to induce reconfiguration where attacker can inject a rogue controller.
- **Detection**: Analyze session message integrity and timing
- **Solution**: Timestamped sessions, use quantum-resistant hash checks
- **Tags**: QKD, Replay, SDR, GNURadio, MITM

## MAC Spoofing Attack on QKD Gateway Node

- **Attack Type**: MITM via MAC Spoofing over Wireless
- **Target**: Wireless LAN attached to QKD node
- **Vulnerability**: MAC-based identity assumption, no session token verification
- **MITRE**: T1557.003 (Spoofing)
- **Impact**: Session disruption, forced protocol downgrade
- **Tools**: Macchanger, Wireshark, Ettercap
- **Scenario**: Attacker spoofs the MAC address of a QKD gateway node on a wireless LAN, intercepting and relaying classical session messages to mimic legitimate communication.
- **Attack Steps**: Step 1: Use Wireshark to capture legitimate MAC address of QKD gateway.Step 2: Disable the legitimate device using deauthentication or RF jamming.Step 3: Set attacker system’s MAC to the gateway’s MAC using macchanger.Step 4: Join the network and mimic classical QKD negotiation protocol (using proxy scripts).Step 5: Relay captured messages between two endpoints while logging all.Step 6: Gradually inject manipulated parity or error-corrected messages.Step 7: Observe how endpoints react to mismatched bits and negotiate retries.
- **Detection**: ARP inspection, MAC-to-cert binding
- **Solution**: Implement EAP-TLS, MACsec, anomaly detection
- **Tags**: QKD, MAC Spoofing, MITM, Wireshark

## Rogue Access Point for QKD Classical Channel Hijack

- **Attack Type**: Wireless MITM using Fake Control Node
- **Target**: Wi-Fi AP in QKD Network
- **Vulnerability**: Lack of AP verification or mutual authentication
- **MITRE**: T1557.002 (Rogue Access Point)
- **Impact**: Session data leakage, metadata compromise
- **Tools**: Fluxion, Kali Linux, Wireshark
- **Scenario**: An attacker deploys a rogue access point configured as a fake QKD classical control node and tricks the QKD client into connecting to it, capturing session control packets.
- **Attack Steps**: Step 1: Use airodump-ng to identify the SSID, BSSID, and channel of the QKD control AP.Step 2: Create a rogue AP using hostapd or Fluxion with same SSID.Step 3: Use a signal amplifier or proximity to ensure stronger signal than the legitimate AP.Step 4: Launch a continuous deauthentication attack to disconnect the client.Step 5: When client reconnects to the fake AP, capture handshake and all classical session control messages.Step 6: Relay messages to real AP using a second NIC to perform MITM.Step 7: Store metadata including timestamps, session hashes, and negotiation messages for later analysis.
- **Detection**: Wireless IDS, AP whitelist validation
- **Solution**: Use WPA3-EAP with client certificates, periodic AP signature validation
- **Tags**: QKD, Rogue AP, MITM, BB84

## Optical Tap on QKD Receiver Node (Wireless Relay Variant)

- **Attack Type**: MITM via Optical Tap + Wireless Relay
- **Target**: Fiber-connected QKD Receiver
- **Vulnerability**: No intrusion detection in fiber optics; unsecured physical access
- **MITRE**: T1200 (Hardware Additions), T1040 (Network Sniffing)
- **Impact**: Partial exposure of quantum states; privacy amplification failure
- **Tools**: Fiber Tap, Raspberry Pi, WiFi Adapter
- **Scenario**: Physical MITM using an optical tap placed between QKD receiver and the classical node. The captured session is transmitted over a wireless link to attacker’s remote analysis tool.
- **Attack Steps**: Step 1: Physically access fiber optic cable running between QKD receiver and control computer.Step 2: Install a non-disruptive fiber tap or beam splitter.Step 3: Connect output to a photodetector wired to Raspberry Pi.Step 4: Use Wi-Fi module to relay quantum pulse arrival times and polarization states over a hidden AP.Step 5: At remote system, log all timings and pulse properties.Step 6: Correlate classical and quantum data for analysis.Step 7: Compare received keys over multiple sessions to infer reuse or error correction patterns.
- **Detection**: Optical power monitoring, time-of-flight analysis
- **Solution**: Fiber encasement, intrusion alarms, power-level thresholding
- **Tags**: QKD, Optical Tap, MITM, Raspberry Pi

## SDR-Based Signal Spoofing in QKD Control Layer

- **Attack Type**: Wireless Signal Injection Attack
- **Target**: Classical Channel (Wireless)
- **Vulnerability**: Lack of strong protocol verification, weak replay resistance
- **MITRE**: T1557 (Man-in-the-Middle), T1001.003 (Protocol Spoofing)
- **Impact**: Desynchronization of key negotiation; possible fallback to weaker encryption
- **Tools**: HackRF, GNURadio, QKD test scripts
- **Scenario**: The attacker uses SDR to transmit forged control signals that mimic valid QKD protocol messages, attempting to desynchronize key sifting or error correction.
- **Attack Steps**: Step 1: Use SDR to capture classical control packets used in QKD protocols.Step 2: Analyze packet timing, sequence, and payload using GNURadio flowgraphs.Step 3: Reconstruct similar packets with slight modifications in parity/error bits.Step 4: Begin injecting packets during active session from attacker’s SDR device.Step 5: Observe endpoint behavior: forced retransmissions or dropped sessions.Step 6: Repeat injections with adaptive changes based on response timing.Step 7: Attempt to maintain session desynchronization, which leads to key negotiation failure or protocol fallback.
- **Detection**: Monitor packet structure and timing, use authenticated protocol layers
- **Solution**: Enforce authenticated key management messages and channel segregation
- **Tags**: SDR, GNURadio, QKD, Protocol Spoofing

## Quantum Signal Cloning Disruption via RF Proxy

- **Attack Type**: MITM via Physical Layer Timing Disruption
- **Target**: Quantum Channel (Free Space or Fiber)
- **Vulnerability**: Physical-layer timing vulnerabilities; lack of quantum signal integrity verification
- **MITRE**: T1499.004 (Signal Delay), T1491.001 (Timing Manipulation)
- **Impact**: Increased QBER, session failure
- **Tools**: RF Relay Setup, Delay Line Hardware
- **Scenario**: Although quantum signals cannot be cloned, attacker introduces subtle timing offsets using a RF proxy device to confuse photon detection at the QKD receiver.
- **Attack Steps**: Step 1: Set up a near-field RF relay to intercept signals between QKD source and receiver in free-space or open-fiber scenario.Step 2: Introduce minor signal delay using RF switches and delay circuits.Step 3: Transmit modified signal to QKD receiver slightly offset in time.Step 4: Monitor classical channel to observe QBER spikes due to missed/misplaced photon arrival.Step 5: Cause session to abort due to high error rate or generate fallback.Step 6: Simultaneously record classical key sifting messages.Step 7: Repeat process under different timing profiles to analyze patterns.
- **Detection**: Analyze QBER spikes, implement time-of-flight validation
- **Solution**: Quantum pulse integrity verification, delay-resilient sync
- **Tags**: QKD, Delay Attack, Timing Shift, MITM

## Compromised Classical Auth Channel in QKD VPN

- **Attack Type**: MITM via VPN Key Replay
- **Target**: VPN Transport Layer in QKD Network
- **Vulnerability**: Key reuse in VPN, no handshake token validation
- **MITRE**: T1557.001 (Protocol Downgrade), T1040 (Traffic Interception)
- **Impact**: Session failure, encrypted key mismatch
- **Tools**: Wireshark, Scapy, OpenVPN Logs
- **Scenario**: In hybrid QKD systems using VPN for classical transport, attacker captures and replays VPN key negotiation to confuse key sync across distributed QKD sites.
- **Attack Steps**: Step 1: Monitor wireless classical transport (VPN tunnel) used in QKD network.Step 2: Use Wireshark to extract VPN handshake (e.g., TLS-based key exchange).Step 3: Replay old handshake packets during new QKD session.Step 4: Observe if VPN connection gets stuck in inconsistent sync or re-establishes with reused keys.Step 5: Use Scapy to modify handshake values to try and align with attacker’s rogue endpoint.Step 6: Analyze logs from VPN and QKD sync systems to observe timing gaps.Step 7: Attempt MITM via spoofed VPN gateway injected on wireless layer.
- **Detection**: VPN logging, unusual handshake retry detection
- **Solution**: Implement perfect forward secrecy, dynamic session tokens
- **Tags**: QKD, VPN, Replay, MITM

## Wi-Fi Deauthentication Flood to Disrupt QKD Sync

- **Attack Type**: MITM Disruption via Deauth
- **Target**: Wireless Classical QKD Channel
- **Vulnerability**: Unprotected Wi-Fi control channel, deauth not blocked
- **MITRE**: T1565.001 (Network Denial of Service)
- **Impact**: Repeated sync failure, denial of key generation
- **Tools**: Aireplay-ng, Airmon-ng, Wireshark
- **Scenario**: Attacker targets the classical wireless control channel with a continuous deauthentication attack to block QKD control sync between nodes.
- **Attack Steps**: Step 1: Enable monitor mode and scan for classical QKD network SSIDs.Step 2: Identify target node MAC addresses.Step 3: Launch aireplay-ng --deauth targeting both client and QKD control server.Step 4: Maintain attack for several minutes, observing if QKD session errors appear.Step 5: Periodically let the devices reconnect and restart deauth to trigger re-syncs.Step 6: Record handshake attempts and timestamps using Wireshark.Step 7: Repeat over multiple sessions to observe system’s fault tolerance.
- **Detection**: IDS/IPS, connection failure logs
- **Solution**: Use 802.11w (Protected Management Frames), switch to wired control
- **Tags**: QKD, Deauth Attack, MITM, Aireplay

## Session Downgrade via Rogue Software Update Server

- **Attack Type**: MITM via Fake Update over Wireless
- **Target**: Wireless-connected QKD Nodes
- **Vulnerability**: Unverified update server, HTTP-based updates
- **MITRE**: T1195.002 (Compromise Software Update), T1557 (MITM)
- **Impact**: Downgrade to insecure protocol version
- **Tools**: Rogue DHCP, Fake Update Server, Ettercap
- **Scenario**: An attacker sets up a rogue wireless AP broadcasting a fake update server address to QKD nodes, triggering them to download outdated or insecure QKD firmware versions.
- **Attack Steps**: Step 1: Spoof DHCP server in wireless range of QKD node using dnsmasq.Step 2: Redirect all HTTP traffic to attacker’s fake update server.Step 3: Offer firmware manifest listing older QKD control node software.Step 4: Wait for node to fetch and install firmware.Step 5: During installation, restart QKD session.Step 6: Inject malformed or reduced-protection packets via SDR.Step 7: Capture session messages and compare behavior to standard version.
- **Detection**: Update hash mismatch, unauthorized server logs
- **Solution**: Enforce HTTPS with certificate pinning, signed binaries
- **Tags**: QKD, Firmware Downgrade, MITM, DNS Spoof

## Drone-Assisted Relay for QKD MITM in Free-Space

- **Attack Type**: Wireless Relay Using Drone
- **Target**: Free-space QKD, Rooftop Urban Network
- **Vulnerability**: No aerial protection, uncontrolled optical path
- **MITRE**: T1499.003 (Traffic Hijacking), T1600 (Hardware Manipulation)
- **Impact**: Signal degradation, session abort
- **Tools**: Drone, Repeater Node, Laser Diode, SDR
- **Scenario**: Using a drone as a passive relay platform, attacker intercepts and delays both classical and quantum signals in free-space QKD network across buildings.
- **Attack Steps**: Step 1: Mount SDR module and optical receiver/transmitter on drone.Step 2: Fly drone to hover in path between QKD nodes on building rooftops.Step 3: Align optics to capture quantum light beams (without decoding).Step 4: Relay beam with slight delay to receiver.Step 5: Use SDR to capture classical negotiation below (e.g., Wi-Fi)Step 6: Record latency variations and QBER fluctuations.Step 7: Analyze whether session fails or proceeds under degraded quality.
- **Detection**: Optical signal power logs, drone detection systems
- **Solution**: Use enclosed beam paths, anti-drone nets, LIDAR detection
- **Tags**: QKD, Drone MITM, Laser Relay

## DNS Spoofing of Quantum Cloud Platform Access

- **Attack Type**: MITM via DNS Spoof Over Wireless
- **Target**: Wireless QKD Clients
- **Vulnerability**: No DNSSEC, no cert pinning, cloud trust assumption
- **MITRE**: T1565.002 (DNS Spoofing), T1557 (MITM)
- **Impact**: Session token theft, fake key injection
- **Tools**: DNSChef, Wireshark, Fake Web Server
- **Scenario**: Attacker spoofs DNS responses in the wireless network used to connect QKD client to a cloud-based QKD key manager, redirecting traffic to attacker-controlled node.
- **Attack Steps**: Step 1: Use ARP spoofing or become rogue DHCP to direct client to attacker’s DNS.Step 2: Respond to quantumcloud.example.com queries with fake IP.Step 3: Host a clone of the QKD key management UI.Step 4: Record submitted session IDs, auth tokens, and keys.Step 5: Relay fake success messages to keep user unaware.Step 6: Extract session metadata and use to preempt future sessions.Step 7: Try injecting modified keys if upload feature is available.
- **Detection**: DNS query validation, TLS cert pinning failure alerts
- **Solution**: DNSSEC, host validation, cloud-side key attestation
- **Tags**: QKD, Cloud MITM, DNS Attack

## Bluetooth-based MITM in Hybrid QKD Device

- **Attack Type**: Wireless MITM via BLE Proxy
- **Target**: BLE in QKD Diagnostic/Control
- **Vulnerability**: No BLE pairing security, exposed characteristics
- **MITRE**: T1557.002 (BLE Proxy), T1010 (Application Layer Protocol Abuse)
- **Impact**: Diagnostic session hijack, false reporting
- **Tools**: Btlejack, Ubertooth, BLEAH
- **Scenario**: Hybrid QKD nodes using Bluetooth for control or diagnostics can be attacked using BLE proxy tools to intercept key sync messages and diagnostic logs.
- **Attack Steps**: Step 1: Scan for BLE devices using btlejack or hcitool.Step 2: Capture pairing attempts and device info.Step 3: Use BLEAH to impersonate a known QKD control device.Step 4: Intercept GATT characteristics related to QKD session.Step 5: Log diagnostic or session messages.Step 6: Try injecting spoofed GATT data causing desync or fault reporting.Step 7: Maintain connection while masquerading as legitimate control system.
- **Detection**: BLE logs, unexpected GATT writes
- **Solution**: Use BLE whitelisting, pairing verification, disable debug mode
- **Tags**: QKD, BLE, Hybrid Device MITM

## Fake Time Server Injection via NTP Spoof

- **Attack Type**: Wireless MITM via NTP Spoof
- **Target**: Wireless NTP Communication in QKD
- **Vulnerability**: Lack of NTP authentication, time spoofing allowed
- **MITRE**: T1602.001 (Time Synchronization Attack)
- **Impact**: QKD protocol desync, invalid or mismatched keys
- **Tools**: NTP Spoofer, Wireshark, ntpd
- **Scenario**: Attacker exploits the QKD node's reliance on wireless NTP for time synchronization by spoofing a fake NTP server, causing desynchronized key generation and degraded system performance.
- **Attack Steps**: Step 1: Monitor network to identify NTP requests broadcast from QKD control node.Step 2: Use a rogue device to respond faster to those requests with manipulated timestamps.Step 3: Slightly skew time to introduce drift without immediate detection.Step 4: Repeat the process regularly to build time discrepancy over hours.Step 5: Observe effects on quantum bit synchronization, error correction misalignments.Step 6: Cause key mismatches between parties, forcing retries and lowering trust in keys.Step 7: Capture repeated classical traffic due to retries and analyze for timing patterns or leaks.
- **Detection**: NTP logs, mismatch between device/system clocks
- **Solution**: Use NTS (Network Time Security), signed time sources, local clock fallback
- **Tags**: QKD, NTP Spoof, Time Desync, MITM

## Packet Fragmentation Attack on QKD Sync Packets

- **Attack Type**: MITM via Wireless Packet Fragmentation
- **Target**: Wireless Classical QKD Channel
- **Vulnerability**: Fragmentation handling flaw; no reassembly validation
- **MITRE**: T1001.001 (Data Obfuscation - Fragmentation), T1499.001 (Protocol Abuse)
- **Impact**: Broken sync, repeated session restarts
- **Tools**: Scapy, Wireshark, Fragment Injector Tool
- **Scenario**: Attacker manipulates packet fragmentation in wireless QKD classical channels to inject malicious fragments, resulting in corrupted key negotiations.
- **Attack Steps**: Step 1: Capture classical wireless control packets of QKD using Wireshark.Step 2: Identify synchronization frames or packets related to key reconciliation.Step 3: Use Scapy to craft overlapping or partial fragments with mismatched payloads.Step 4: Inject these crafted fragments just before real packets are reassembled by QKD software.Step 5: Watch as the receiving node constructs malformed session data.Step 6: Repeat to consistently corrupt QKD sync or error correction negotiations.Step 7: Measure retry attempts or fallback to insecure protocol.
- **Detection**: Analyze fragment logs, checksum mismatches
- **Solution**: Reassembly validation, enforce anti-fragmentation firewall rules
- **Tags**: QKD, Fragmentation Attack, MITM

## RF Jamming & Channel Switching Trick

- **Attack Type**: RF-based MITM with Forced Channel Switch
- **Target**: Wireless Classical Communication (Wi-Fi)
- **Vulnerability**: Channel fallback mechanism exploited
- **MITRE**: T1464 (Signal Interference), T1557.002 (Rogue AP)
- **Impact**: Forced channel switch, full session interception
- **Tools**: HackRF One, Jammer Device, Hostapd
- **Scenario**: Attacker uses RF jamming to force QKD control devices to switch to alternate channels where a rogue AP is waiting to intercept classical traffic.
- **Attack Steps**: Step 1: Use SDR or HackRF to detect the current channel of QKD classical AP.Step 2: Launch focused jamming on that channel (e.g., 2.4 GHz channel 6).Step 3: Simultaneously set up a rogue AP on a different channel (e.g., channel 11) using the same SSID.Step 4: Once jamming begins, legitimate clients will try to reconnect on alternate channels.Step 5: Client connects to rogue AP on channel 11.Step 6: Relay classical QKD negotiation traffic while logging all sifting, reconciliation, and privacy amplification messages.Step 7: Repeat to accumulate session metadata across retries.
- **Detection**: Monitor BSSID/channel mismatches in Wi-Fi logs
- **Solution**: Restrict auto-channel switch, enable AP fingerprinting
- **Tags**: QKD, Channel Switch MITM, Rogue AP

## Side-channel Timing Attack via Wi-Fi Latency Monitoring

- **Attack Type**: Wireless MITM via Timing Inference
- **Target**: Wireless QKD Classical Channel
- **Vulnerability**: Timing leakage from traffic bursts
- **MITRE**: T1592.002 (Traffic Analysis), T1040 (Packet Capture)
- **Impact**: Leakage of session structure, statistical data
- **Tools**: Wireshark, Passive Timing Logger, Latency Monitor
- **Scenario**: Without direct packet injection, attacker infers QKD session events by passively measuring Wi-Fi latency and traffic timing patterns.
- **Attack Steps**: Step 1: Passively monitor the classical control Wi-Fi channel using Wireshark or tcpdump.Step 2: Use scripts to log packet sizes, timestamps, and delays between transmissions.Step 3: Correlate bursts of activity with key sifting, error correction, and final key confirmation phases.Step 4: Over many sessions, infer timing patterns linked to key length, success rate, or system faults.Step 5: Attempt traffic modeling to detect vulnerable sync windows.Step 6: Use this intel for optimized future MITM placement.Step 7: Maintain passive-only role for stealth, avoiding detection.
- **Detection**: Network flow analysis, traffic pattern alerts
- **Solution**: Add random padding, use traffic shaping and cover traffic
- **Tags**: QKD, Passive Timing Attack, Wi-Fi

## ARP Poisoning of QKD Key Management Node

- **Attack Type**: Wireless MITM via ARP Spoof
- **Target**: LAN over Wireless (QKD Classical Layer)
- **Vulnerability**: ARP table can be spoofed in unsecured network
- **MITRE**: T1557.001 (ARP Poisoning), T1040 (MITM Packet Capture)
- **Impact**: Full classical channel compromise, session metadata loss
- **Tools**: Ettercap, arpspoof, Wireshark
- **Scenario**: Attacker poisons ARP tables over wireless to position themselves between QKD client and key manager, logging and modifying classical session data.
- **Attack Steps**: Step 1: Identify IP and MAC of QKD key management server.Step 2: Use arpspoof or Ettercap to send forged ARP responses to QKD client mapping your MAC to server IP.Step 3: Do the same in reverse to the server.Step 4: Begin capturing all traffic flowing between them using Wireshark.Step 5: Optionally modify packets on-the-fly (e.g., delay, strip bits, change parity data).Step 6: Log complete session metadata and session ID references.Step 7: Maintain this position for multiple sessions to observe key derivation patterns.
- **Detection**: ARP table monitoring, detection of duplicate IP-MAC
- **Solution**: Implement dynamic ARP inspection, enable mutual auth
- **Tags**: QKD, ARP Spoof, MITM, Ettercap

## Exploiting PQ VPN Key Exchange Over Compromised Wi-Fi

- **Attack Type**: Wireless - Man-in-the-Middle
- **Target**: VPN Clients over Wi-Fi
- **Vulnerability**: Timing leakage in PQ handshake
- **MITRE**: T1040
- **Impact**: Potential key disclosure or downgrade
- **Tools**: Wireshark, Bettercap, FakeAP, Spectre
- **Scenario**: Attacker compromises a public Wi-Fi AP and targets a post-quantum VPN (e.g., using Kyber) during key exchange to analyze flaws in side-channel timing via wireless sniffing.
- **Attack Steps**: Step 1: Set up a rogue Wi-Fi hotspot mimicking a known public Wi-Fi name (SSID).Step 2: Wait for the target device to connect automatically.Step 3: Use Bettercap to capture initial handshake packets and monitor traffic during post-quantum key exchange.Step 4: Log timing and response behaviors from the VPN client that uses PQ algorithms.Step 5: Use offline analysis to detect timing leakage or response anomalies that might hint at flawed key scheduling or predictability.
- **Detection**: Monitor VPN handshake anomalies; alert on unknown AP connections
- **Solution**: Enforce VPN mutual certificate verification and DNS pinning
- **Tags**: PQC, Wi-Fi, Side-Channel, Timing Analysis

## Wi-Fi Downgrade of PQC Secure Protocol to Legacy for Traffic Interception

- **Attack Type**: Wireless - Downgrade
- **Target**: Post-Quantum TLS-enabled Clients
- **Vulnerability**: Fallback to legacy TLS on connection error
- **MITRE**: T1557.002
- **Impact**: Intercepted communications or credentials
- **Tools**: Aireplay-ng, SSLstrip2, MITMProxy, EvilAP
- **Scenario**: The attacker forces devices to fallback from a PQC-secure TLS implementation to legacy TLS over Wi-Fi, making it easier to eavesdrop.
- **Attack Steps**: Step 1: Deploy an Evil Twin AP matching the SSID of a legitimate PQ-secure network.Step 2: Deauthenticate the victim from their current connection using Aireplay-ng.Step 3: Once the victim connects to the Evil AP, proxy all TLS traffic using SSLstrip2 and MITMProxy.Step 4: Intercept any fallback attempts to older TLS versions if PQ-TLS fails or isn’t verified.Step 5: Capture decrypted traffic or weaker cryptographic exchanges.
- **Detection**: Alert if legacy cipher suite is used over PQ network
- **Solution**: Disable all legacy TLS versions; enforce strict PQ-TLS policies
- **Tags**: TLS Downgrade, Evil Twin, PQC, WPA2 Enterprise

## Exploiting Faulty Post-Quantum Firmware Updates via Wi-Fi Injection

- **Attack Type**: Wireless - Injection
- **Target**: IoT Devices using PQ Firmware Signing
- **Vulnerability**: Improper PQ signature validation
- **MITRE**: T1542.001
- **Impact**: Full device compromise
- **Tools**: Aircrack-ng, FakeDNS, ESP32 OTA Tools
- **Scenario**: Attacker uses Wi-Fi to deliver a corrupted post-quantum signed firmware file exploiting poor signature verification logic.
- **Attack Steps**: Step 1: Set up a rogue access point to serve as a fake firmware server.Step 2: Redirect firmware update requests using DNS spoofing.Step 3: Create a malicious firmware update with a malformed post-quantum signature.Step 4: Use OTA (Over-The-Air) update tools to serve this update over the rogue AP.Step 5: If the verification logic in the firmware is poorly implemented, the device installs the malicious update.
- **Detection**: Firmware validation logs; checksum mismatch
- **Solution**: Strict firmware validation, rollback prevention, proper PQ signature parsing
- **Tags**: IoT, OTA, PQC, Signature Bypass

## Side-Channel Attacks on PQ Key Gen over Wi-Fi using Power-Aware SDR

- **Attack Type**: Wireless - Side Channel
- **Target**: PQ-enabled Mobile Devices or Routers
- **Vulnerability**: EM and power-based side channels
- **MITRE**: T1200
- **Impact**: PQ key extraction or pattern leakage
- **Tools**: HackRF, GNU Radio, Side-Channel Toolkit
- **Scenario**: SDR device captures power fluctuations during PQ key generation over a wireless-connected device, correlating them to key patterns.
- **Attack Steps**: Step 1: Place a power-aware SDR (e.g., HackRF) near the device generating PQ keys.Step 2: Use Wi-Fi communication to trigger key generation (e.g., secure session init).Step 3: Record RF emissions and power fluctuation signatures.Step 4: Analyze collected data using Side-Channel Toolkit to find correlations with key material.Step 5: Attempt to extract key characteristics or flaw patterns.
- **Detection**: RF signature scanning in sensitive areas
- **Solution**: Shielded enclosures, constant-time implementations
- **Tags**: EM Analysis, SDR, PQC, Side Channel

## Exploiting PQ Key Exchange via Wi-Fi Packet Fragmentation Replay

- **Attack Type**: Wireless - Fragmentation Attack
- **Target**: Laptops or Gateways with PQ TLS
- **Vulnerability**: Inadequate packet validation and reassembly logic
- **MITRE**: T1499.004
- **Impact**: Downgrade, crash, or DoS
- **Tools**: Scapy, Aircrack-ng, Fragmentation Toolkit
- **Scenario**: An attacker fragments and replays PQ key exchange packets during a handshake to induce misinterpretation or crash in the cryptographic library.
- **Attack Steps**: Step 1: Monitor a PQ-secured Wi-Fi handshake using Aircrack-ng.Step 2: Capture PQ key exchange packets (Kyber, etc.) during TLS handshake.Step 3: Use Scapy to fragment the packets abnormally.Step 4: Replay malformed fragments during another session or inject mid-handshake.Step 5: Observe device behavior for crashes, handshake retries, or logic faults due to incorrect reassembly.
- **Detection**: Log reassembly failures or malformed packet alerts
- **Solution**: Patch libraries for robust parsing; enforce packet checks
- **Tags**: Fragmentation, PQC, TLS, Replay

## PQ Handshake Downgrade via Captive Portal Hijack

- **Attack Type**: Wireless - Downgrade via Interception
- **Target**: Laptops, Mobile Devices
- **Vulnerability**: Lack of proper validation before PQ handshake
- **MITRE**: T1557
- **Impact**: Downgraded encryption, possible data exfiltration
- **Tools**: EvilAP, Captive Portal Tools, Burp Suite, SSLsplit
- **Scenario**: Captive portal is used to hijack initial connection and redirect traffic before PQ handshake completes, forcing fallback to legacy cryptography.
- **Attack Steps**: Step 1: Create a rogue Wi-Fi hotspot with the same SSID as a known PQ-enabled public Wi-Fi.Step 2: Configure a captive portal that forces the client to accept a login page before internet is granted.Step 3: Intercept all HTTPS connections and block access to PQ-TLS servers initially.Step 4: Force the client to fallback to less secure cipher suites to proceed.Step 5: Use SSLsplit to analyze and potentially decrypt non-PQ traffic.Step 6: Log and analyze client reactions to forced downgrade.
- **Detection**: Monitor for unusual cipher negotiation
- **Solution**: Block fallback in TLS config; use DNS-over-HTTPS with validation
- **Tags**: Captive Portal, TLS Downgrade, PQ, Evil Twin

## Replay of Post-Quantum Key Exchange in Wi-Fi Mesh

- **Attack Type**: Wireless - Replay
- **Target**: Mesh Routers or IoT Devices
- **Vulnerability**: Inadequate replay protection
- **MITRE**: T1001.003
- **Impact**: Session confusion, loss of integrity
- **Tools**: Scapy, Wireshark, Kismet
- **Scenario**: In mesh networks using PQC-enabled protocols, an attacker replays captured handshake packets to disrupt or confuse nodes.
- **Attack Steps**: Step 1: Capture initial PQ key exchange messages between mesh nodes using Wireshark.Step 2: Save and analyze these messages for timing, length, and response behaviors.Step 3: Reinject these packets using Scapy at randomized intervals.Step 4: Observe if receiving nodes reset sessions, crash, or accept malformed messages.Step 5: Repeat replay with slightly altered fields to test robustness.
- **Detection**: Alert on handshake frequency anomalies
- **Solution**: Enforce strict sequence validation and nonces
- **Tags**: Mesh, PQ Replay, Session Injection

## Exploiting Wi-Fi 6 (OFDMA) Channel Leaks in PQ Keygen

- **Attack Type**: Wireless - Side Channel via Wi-Fi 6
- **Target**: Wi-Fi 6 Enabled Devices
- **Vulnerability**: OFDMA channel timing correlation
- **MITRE**: T1200
- **Impact**: Potential key timing leak
- **Tools**: WiFi6 Adapter, Airtool-ng, Custom Python Timers
- **Scenario**: Uses OFDMA-based channel allocations in Wi-Fi 6 to indirectly measure timing behavior during PQ key generation.
- **Attack Steps**: Step 1: Connect to the same Wi-Fi 6 AP as the victim device.Step 2: Monitor dynamic OFDMA resource unit (RU) allocations while triggering PQ keygen from victim (e.g., initiating VPN).Step 3: Record delays and resource usage shifts linked to PQ operations.Step 4: Analyze repeated patterns indicating timing leaks.Step 5: Build correlation models to predict keygen time intervals.
- **Detection**: Look for abnormal timing footprints
- **Solution**: Use constant-time PQ keygen and obfuscate timing
- **Tags**: OFDMA, PQ Timing Leak, Side-Channel

## Fake AP Inducing PQ Certificate Chain Validation Bypass

- **Attack Type**: Wireless - Certificate Spoof
- **Target**: PQ-enabled Browsers or Clients
- **Vulnerability**: PQ certificate chain validation flaw
- **MITRE**: T1557.004
- **Impact**: Trust bypass, phishing success
- **Tools**: EvilAP, FakeDNS, PQCertGen, Wireshark
- **Scenario**: An attacker hosts a fake AP and tricks a client into accepting a PQ certificate chain that lacks proper trust anchors.
- **Attack Steps**: Step 1: Host a rogue AP with SSID matching a secure network.Step 2: Set up DNS spoofing to redirect target to a fake HTTPS endpoint.Step 3: Present a server certificate signed with a PQ algorithm (e.g., Dilithium) but missing root CA chaining.Step 4: Observe if the client accepts the certificate.Step 5: Attempt to establish encrypted sessions using this untrusted cert.
- **Detection**: Scan certificate chain depth in client logs
- **Solution**: Enforce strict CA checks, pinning
- **Tags**: PQ Certificates, Trust Chain, Wi-Fi Spoof

## Exploiting Quantum-Resistant DNS Over Wi-Fi Using DNS Rebinding

- **Attack Type**: Wireless - DNS Rebinding
- **Target**: PQ DoH clients (Laptop, Mobile)
- **Vulnerability**: DoH client trusting rebinding
- **MITRE**: T1071.004
- **Impact**: DNS cache poisoning or phishing
- **Tools**: FakeDNS, DoH Manipulation Toolkit, Pi-hole
- **Scenario**: Attacker performs DNS rebinding to target PQ DNS-over-HTTPS (DoH) clients and capture traffic via Wi-Fi redirection.
- **Attack Steps**: Step 1: Set up rogue AP and redirect DNS requests to fake DNS server.Step 2: Serve malicious DNS entries pointing to attacker-controlled server.Step 3: Use JavaScript to perform rebinding attacks on client side.Step 4: Attempt to bypass client-side DNS-over-HTTPS protections.Step 5: Log whether PQ DNS protocol (e.g., PQ-DNSSEC) fails to detect change.
- **Detection**: Check for DNS rebinding or multiple A-records
- **Solution**: Block non-standard DNS entries; enforce DoH pinning
- **Tags**: PQ DNS, Rebinding, DoH

## Manipulating PQ Key Agreement via Wi-Fi Frame Injection

- **Attack Type**: Wireless - Frame Injection
- **Target**: Routers or PQ-aware clients
- **Vulnerability**: PQ handshake parser not verifying sequence integrity
- **MITRE**: T1565
- **Impact**: Corrupted session keys
- **Tools**: Scapy, Aircrack-ng, Frameforge
- **Scenario**: Attacker injects custom frames mid PQ handshake over Wi-Fi, corrupting key agreement.
- **Attack Steps**: Step 1: Capture legitimate PQ handshake packets over Wi-Fi.Step 2: Use Scapy to craft forged packets mimicking handshake response.Step 3: Inject packets mid-handshake using monitor mode interface.Step 4: Observe victim device behavior (e.g., reset handshake or accept corrupted data).Step 5: Analyze logs for key negotiation inconsistencies.
- **Detection**: Alert on out-of-order or duplicate handshake messages
- **Solution**: Validate sequence numbers in crypto handshake
- **Tags**: Frame Injection, PQ Session Hijack

## Exploiting PQC Firmware Updates via Wi-Fi Beacon Spoofing

- **Attack Type**: Wireless - Beacon Spoofing
- **Target**: IoT Devices with OTA
- **Vulnerability**: Beacon logic manipulation bypassing secure update flow
- **MITRE**: T1070
- **Impact**: Firmware compromise or remote control
- **Tools**: Beacon Flood, Airbase-ng, ESPOTA
- **Scenario**: Beacons are spoofed to manipulate devices into triggering firmware updates over insecure channels.
- **Attack Steps**: Step 1: Use Airbase-ng to send spoofed beacon frames advertising outdated firmware version.Step 2: Trigger device firmware update behavior expecting to find new PQ-certified firmware.Step 3: Intercept and serve malicious firmware from rogue HTTP server.Step 4: Log whether PQ signature is verified before installation.Step 5: Check for success or failure via console or logs.
- **Detection**: Detect mismatched firmware version advertisements
- **Solution**: Require encrypted OTA and firm cryptographic chain
- **Tags**: Beacon, Firmware, PQ, IoT

## Bluetooth Low Energy + Wi-Fi Cross Protocol PQC Leak

- **Attack Type**: Wireless - Cross Protocol Attack
- **Target**: BLE-enabled Wi-Fi clients
- **Vulnerability**: Cross-protocol timing correlation
- **MITRE**: T1040
- **Impact**: Partial key leakage via correlation
- **Tools**: Ubertooth, BLEAH, Wireshark, WiFi Sniffer
- **Scenario**: Attacker leverages BLE channel leakage during Wi-Fi PQ handshake to correlate behaviors.
- **Attack Steps**: Step 1: Pair BLE-enabled device and sniff BLE traffic.Step 2: Simultaneously sniff Wi-Fi handshake where PQ key exchange occurs.Step 3: Observe BLE response delays that coincide with PQ operations.Step 4: Attempt to correlate those delays with cryptographic activity.Step 5: Reconstruct possible PQ key characteristics.
- **Detection**: Compare BLE and Wi-Fi traffic overlap
- **Solution**: Time-randomized crypto operations
- **Tags**: BLE, PQC, Side-Channel

## PQ Key Misuse in Public Wi-Fi via Misconfigured TLS-SIG

- **Attack Type**: Wireless - Crypto Misuse
- **Target**: PQ TLS Clients
- **Vulnerability**: Improper key reuse
- **MITRE**: T1600
- **Impact**: Forged identity, signature reuse
- **Tools**: Wireshark, TLS Test Suite, Mitmproxy
- **Scenario**: TLS implementation with PQ support uses same key material for both signature and encryption over Wi-Fi.
- **Attack Steps**: Step 1: Monitor PQ TLS sessions on public Wi-Fi.Step 2: Extract and analyze key usage from handshake.Step 3: Identify cases where the same public key is reused for both signing and encryption.Step 4: Attempt to replay or forge signatures using this misuse.Step 5: Observe client-server behavior and try MITM insertion.
- **Detection**: Alert on duplicate key usage in handshake
- **Solution**: Use different key pairs for each function
- **Tags**: TLS, PQC, Key Reuse

## Wi-Fi Probe Request Poisoning for PQ Session Downgrade

- **Attack Type**: Wireless - Probe Injection
- **Target**: Any PQ-aware Wi-Fi Clients
- **Vulnerability**: Misleading probe responses redirecting clients
- **MITRE**: T1595
- **Impact**: PQ session downgrade
- **Tools**: ProbeSniper, Aircrack-ng, EvilAP
- **Scenario**: Attacker sends poisoned probe responses to client devices looking for PQ-safe networks, redirecting them to unsafe ones.
- **Attack Steps**: Step 1: Listen for probe requests from devices searching for known SSIDs.Step 2: Send spoofed responses advertising PQ-insecure versions of those networks.Step 3: Host EvilAP with poor or no PQ support.Step 4: Log if devices connect and initiate downgraded session.Step 5: Use MITM to intercept connections.
- **Detection**: Monitor client SSID behavior
- **Solution**: Filter SSID probes, pin trusted PQ networks
- **Tags**: Probe Attack, PQ Downgrade

## PQ Crypto Handshake Interference via Wi-Fi Signal Jamming

- **Attack Type**: Wireless - Jamming + Timing Attack
- **Target**: PQ VPN Clients, Browsers, IoT Devices
- **Vulnerability**: PQ key handshake timing inconsistency
- **MITRE**: T1200 (Side-Channel), T1599 (Jamming)
- **Impact**: Partial key exposure, connection disruption
- **Tools**: WiFi-Jammer.py, Aircrack-ng, Wireshark, RF Analyzer
- **Scenario**: Attacker jams specific packets during the post-quantum handshake, forcing retransmissions that expose timing inconsistencies.
- **Attack Steps**: Step 1: Use a Wi-Fi sniffer to identify the handshake packets from a client device initiating a PQC VPN or secure connection.Step 2: Set up a jammer (e.g., WiFi-Jammer.py) to selectively interfere with those packets based on their MAC address and port (e.g., 443 for HTTPS).Step 3: Allow partial transmission of initial key exchange packets and then selectively drop specific fragments mid-handshake.Step 4: Observe how often the client retries and if timing gaps or differences in retransmission behavior appear.Step 5: Log handshake retransmissions and analyze side-channel timing leaks that might occur due to PQ implementation inconsistencies.Step 6: Use RF analyzer to capture fine-grained RF signal behavior to correlate with software logs.
- **Detection**: Monitor handshake retries and retransmission delays
- **Solution**: Implement constant-time PQ operations and packet randomization
- **Tags**: PQ Timing Leak, Side Channel, RF Jamming

## PQ VPN Spoof with Corrupted Certificate Chain via Open Wi-Fi

- **Attack Type**: Wireless - Certificate Chain Spoofing
- **Target**: VPN clients with PQ-cert support
- **Vulnerability**: PQ certificate trust misconfiguration
- **MITRE**: T1557.004
- **Impact**: VPN interception, loss of confidentiality
- **Tools**: OpenVPN, EvilAP, FakePQCertTool, mitmproxy
- **Scenario**: Over open Wi-Fi, attacker sends forged VPN certificates using fake PQ root/intermediate certificates, testing client validation.
- **Attack Steps**: Step 1: Set up a fake open Wi-Fi AP using hostapd or airbase-ng.Step 2: Host a fake VPN endpoint that uses self-generated post-quantum certificates (e.g., Dilithium or SPHINCS+) that appear valid but use a non-trusted root CA.Step 3: Redirect all VPN traffic from victims connected to the open Wi-Fi to this fake server using DNS spoofing.Step 4: Monitor if the VPN client accepts the corrupted certificate chain and connects without warning.Step 5: If successful, MITM traffic and analyze the weaknesses in certificate validation logic.Step 6: Record if the victim app logs errors or silently accepts the cert.
- **Detection**: Detect unexpected PQ cert chains in logs
- **Solution**: Enforce strict CA pinning, OCSP validation
- **Tags**: PQC, VPN, Certificate Spoof, Evil Twin

## PQC Cryptographic DoS via Fragmented Wi-Fi Packet Flood

- **Attack Type**: Wireless - Fragmentation DoS
- **Target**: PQC VPNs, TLS Servers, IoT Devices
- **Vulnerability**: Poor parsing of fragmented PQ packets
- **MITRE**: T1499.004 (DoS via Application Layer)
- **Impact**: Memory exhaustion, crash
- **Tools**: Scapy, Fragmentation Toolkit, Aircrack-ng
- **Scenario**: Attacker floods a device with fragmented packets mimicking PQ handshake messages to exhaust CPU or memory during parsing.
- **Attack Steps**: Step 1: Use Wireshark to observe the structure of legitimate PQ key exchange packets.Step 2: Create thousands of fragmented handshake-like packets using Scapy and Fragmentation Toolkit.Step 3: Inject these into the wireless channel targeting a specific device (identified via MAC address).Step 4: The device attempts to reassemble or parse the malformed fragments, causing CPU and memory spikes.Step 5: Monitor device response—many will slow down or crash if not hardened against malformed PQ packets.Step 6: Analyze memory usage and logs to confirm DoS conditions.
- **Detection**: Monitor for memory spikes and malformed packet floods
- **Solution**: Apply strict limits and sanity checks on packet fragments
- **Tags**: Fragmentation, PQC, DoS, Wi-Fi

## Post-Quantum Client Confusion via Rogue Wi-Fi DHCP Option Injection

- **Attack Type**: Wireless - DHCP Manipulation
- **Target**: PQ VPN/TLS Clients
- **Vulnerability**: Trust in DHCP-provided insecure config
- **MITRE**: T1557.002 (Man-in-the-Middle via Network Config)
- **Impact**: Certificate expiry bypass, misrouting
- **Tools**: DHCPig, FakeDHCP, RogueAP, Wireshark
- **Scenario**: DHCP server sends malicious options (e.g., incorrect time or DNS) to PQC clients, leading to broken crypto validation or misrouting.
- **Attack Steps**: Step 1: Set up a rogue DHCP server on a fake AP.Step 2: Serve DHCP options that provide invalid NTP servers, redirect DNS to a malicious server, or spoof time zones (e.g., 1970).Step 3: Client devices that use time-sensitive PQ algorithms (e.g., expiry on certificates) may fail to validate.Step 4: Attempt to initiate VPN or TLS PQ handshake—observe if time-based certificate expiry or validation fails.Step 5: Use the DNS option to redirect software updates or secure DNS traffic.Step 6: Log all malformed handshakes and client behaviors.Step 7: If successful, proceed with MITM injection.
- **Detection**: Log DHCP options and clock inconsistencies
- **Solution**: Use static NTP and DNS; verify system clock validity
- **Tags**: DHCP Attack, PQ TLS, Time Injection

## Wi-Fi QR Code Injection Triggering PQ Vulnerability in Auto Connect

- **Attack Type**: Wireless - Social Engineering / Auto-Connect
- **Target**: Smartphones, Laptops with PQ VPN
- **Vulnerability**: Auto-connect logic trusting QR config
- **MITRE**: T1566.001 (Phishing via QR) + T1557
- **Impact**: PQ VPN redirection, fallback
- **Tools**: EvilAP, QRGen, DNSPoison, PQVPN Proxy
- **Scenario**: QR code scanned by victim adds a rogue Wi-Fi that triggers PQ handshake exploitation through forced redirection.
- **Attack Steps**: Step 1: Generate a QR code that contains a Wi-Fi network SSID, password, and security type (WPA2).Step 2: Distribute the QR code (e.g., printed flyers or phishing emails pretending to offer free Wi-Fi).Step 3: Once scanned, the device auto-connects to the rogue network.Step 4: Use DNS spoofing to redirect VPN clients to a proxy PQ VPN server with altered key exchange flow.Step 5: Force handshake retries using malformed responses to induce fallback or timing differences.Step 6: Log the PQ session behavior to identify exploitable patterns.Step 7: If successful, record the weakened or misconfigured session.Step 8: Disconnect the victim automatically to avoid suspicion.
- **Detection**: Detect unexpected SSID connections via logs
- **Solution**: Educate on QR phishing; disable auto-connect
- **Tags**: QR Attack, PQ VPN, Auto-Join Exploit

## Wi-Fi Downgrade to Legacy Cipher During PQ-Hybrid VPN Login

- **Attack Type**: Wireless Downgrade
- **Target**: Hybrid VPN Client
- **Vulnerability**: Downgrade to Legacy Wi-Fi
- **MITRE**: T1499.001 (Endpoint Denial), T1557 (Adversary-in-the-Middle)
- **Impact**: Compromised VPN Key Negotiation
- **Tools**: Wireshark, Aireplay-ng, Hostapd, OpenVPN
- **Scenario**: Attacker forces a user's device to connect to an access point using legacy WPA2 while the VPN is configured to use hybrid RSA + PQC. The older cipher exposes the initial handshake to interception.
- **Attack Steps**: Step 1: Setup a rogue Wi-Fi access point with the same SSID as the organization's network, but only allow WPA2 (not WPA3). Step 2: Use Aireplay-ng to deauthenticate the victim from their current network. Step 3: Victim reconnects to the rogue AP using WPA2. Step 4: Start VPN connection using hybrid (RSA + PQC) handshake. Step 5: Capture handshake using Wireshark. Step 6: Replay captured handshake to analyze whether the RSA portion was exposed.
- **Detection**: Wi-Fi Authentication Logs, VPN logs
- **Solution**: Enforce WPA3-Enterprise, Strict cipher enforcement
- **Tags**: hybrid-migration, wpa2-downgrade, rogue-ap

## Wireless PKI Credential Interception During Hybrid Enrollment

- **Attack Type**: Wireless Interception
- **Target**: Enterprise Laptop
- **Vulnerability**: Legacy PKI used in wireless cert issuance
- **MITRE**: T1557.002 (DHCP Spoofing), T1040 (Network Sniffing)
- **Impact**: PKI Credential Replay or Forgery
- **Tools**: Responder, Wireshark, Fake AP
- **Scenario**: Exploiting the lack of full PQC support in wireless certificate enrollment via Wi-Fi, attacker captures legacy PKI exchange.
- **Attack Steps**: Step 1: Setup a rogue Wi-Fi access point with captive portal functionality. Step 2: Spoof the organization's certificate enrollment server (e.g., Windows AD CS) via Responder. Step 3: When victim connects, trigger a certificate auto-enrollment (common in corporate networks). Step 4: Capture PKCS#10 request and server reply. Step 5: Analyze if legacy crypto was used (e.g., RSA-2048) despite PQC in place.
- **Detection**: Monitoring certificate templates & request logs
- **Solution**: Enforce PQC-compliant cert templates and mutual TLS
- **Tags**: wireless-pki, rogue-ap, hybrid-migration

## BLE-Based Man-in-the-Middle During PQ Key Negotiation

- **Attack Type**: BLE MITM
- **Target**: BLE-enabled Crypto Key Device
- **Vulnerability**: Insecure BLE pairing used in hybrid crypto
- **MITRE**: T1557.003 (Bluetooth MITM), T1010 (Application Layer Protocol)
- **Impact**: Exposure of key exchange
- **Tools**: gattacker, BLEah, Wireshark BLE plugin
- **Scenario**: Exploiting BLE channel hopping weaknesses to insert malicious node during a post-quantum hybrid handshake for key distribution.
- **Attack Steps**: Step 1: Scan for nearby Bluetooth LE devices pairing with a crypto token or HSM. Step 2: Use gattacker to clone legitimate BLE services and advertise with higher signal. Step 3: Device initiates pairing with attacker, not realizing it. Step 4: Intercept and relay key material exchange (RSA + PQ). Step 5: Forward to real HSM after viewing RSA portion. Step 6: Log and analyze intercepted legacy RSA components.
- **Detection**: BLE pairing logs, anomalous pairing MACs
- **Solution**: Use Secure Connections Only, BLE channel hardening
- **Tags**: ble, hybrid-handshake, mitm, pqc

## Legacy Wi-Fi Captive Portal Leaks PQ Token Bootstrap Info

- **Attack Type**: Captive Portal Interception
- **Target**: PQ Token Provisioning System
- **Vulnerability**: Token provisioning via HTTP or legacy TLS
- **MITRE**: T1557.001 (LLMNR/NBT-NS Poisoning), T1041 (Exfil via Web)
- **Impact**: PQ token hijacking
- **Tools**: EvilPortal (WiFi-Pumpkin3), Burp Suite
- **Scenario**: Hybrid crypto token bootstraps over Wi-Fi captive portal that still uses HTTP or legacy TLS for initial auth, leaking token secrets.
- **Attack Steps**: Step 1: Clone public Wi-Fi with captive portal (e.g., guest Wi-Fi onboarding). Step 2: Use EvilPortal to inject a fake token bootstrap form using JavaScript. Step 3: Victim connects and enters token or provisioning code. Step 4: Intercept that info using Burp proxy. Step 5: Replay the token provisioning on real service to clone auth.
- **Detection**: Network HTTP logs, user-agent anomalies
- **Solution**: Use TLS 1.3+ only, captive portal certificate pinning
- **Tags**: captive-portal, token-leak, pq-onboarding

## Hybrid Crypto Key Synchronization Over Insecure Wi-Fi Mesh

- **Attack Type**: Mesh Wi-Fi Exploit
- **Target**: Wireless Mesh Nodes
- **Vulnerability**: No E2E encryption on mesh control packets
- **MITRE**: T1021.004 (Remote Services: SMB), T1071.001 (Web Protocols)
- **Impact**: Key exposure or routing table poisoning
- **Tools**: Aircrack-ng, Kismet, Bettercap
- **Scenario**: Exploit misconfigured mesh nodes exchanging hybrid crypto keys over legacy WPA2 links with no end-to-end crypto.
- **Attack Steps**: Step 1: Identify mesh Wi-Fi environment using Kismet. Step 2: Use Bettercap to sniff for OLSR or Babel routing protocol messages. Step 3: Inject rogue mesh node into the network. Step 4: Intercept key sync packets (e.g., key transport with PQ + RSA). Step 5: Capture and analyze if keys use legacy wrapping method (e.g., PKCS#1).
- **Detection**: Mesh routing log anomalies
- **Solution**: Enforce IPsec or WPA3 on mesh links
- **Tags**: mesh-wifi, key-sync, hybrid-pqc

## WPA2 Replay Attack During Hybrid VPN Bootstrap

- **Attack Type**: Wi-Fi Replay
- **Target**: Enterprise Wi-Fi Users
- **Vulnerability**: WPA2 session replay, fallback crypto
- **MITRE**: T1557, T1040, T1600
- **Impact**: Bypassing PQC via fallback
- **Tools**: Wireshark, Aireplay-ng, Reaver
- **Scenario**: An attacker captures a WPA2 handshake used during a hybrid VPN connection setup and replays it to trick systems that fall back to RSA key exchange.
- **Attack Steps**: Step 1: Set up a Wi-Fi sniffer using Wireshark near the victim's workspace. Step 2: Use Aireplay-ng to deauthenticate the user. Step 3: Capture WPA2 handshake when the user reconnects. Step 4: Replay this captured handshake with Reaver to simulate re-authentication. Step 5: Monitor VPN setup — if the system retries with legacy RSA, capture key material. Step 6: Extract the non-PQC (legacy) portions for analysis.
- **Detection**: Wi-Fi handshake re-auth logs
- **Solution**: Disable RSA fallback, enforce TLS 1.3 with PQC-only suites
- **Tags**: replay, wpa2, hybrid-downgrade

## Wi-Fi 6 Management Frame Injection During Hybrid Auth

- **Attack Type**: Frame Injection
- **Target**: Wi-Fi 6 Device
- **Vulnerability**: Downgradable auth frames
- **MITRE**: T1600, T1562.008
- **Impact**: Key downgrade to legacy cipher
- **Tools**: Scapy, Airbase-ng, MDK4
- **Scenario**: Attackers inject fake management frames (like beacons or probes) during hybrid crypto negotiation between device and authentication server over Wi-Fi 6.
- **Attack Steps**: Step 1: Use a laptop with a compatible Wi-Fi card to run Scapy. Step 2: Inject spoofed beacon frames advertising a fake WPA3-enabled AP. Step 3: Force the device to scan and attempt connection. Step 4: During initial EAP-based authentication, introduce legacy cipher suite in reply. Step 5: Victim unknowingly completes handshake using RSA+PQC, exposing RSA to sniffers.
- **Detection**: Frame anomaly detection
- **Solution**: 802.11w frame protection, suite pinning
- **Tags**: 80211-frame-injection, hybrid-pqc

## Post-Quantum Smartcard Key Leak via Unencrypted NFC Bootstrapping

- **Attack Type**: NFC Sniffing
- **Target**: PQ Smartcards
- **Vulnerability**: No encryption on NFC provisioning
- **MITRE**: T1056.004, T1110.003
- **Impact**: Smartcard cloning, key leakage
- **Tools**: Proxmark3, NFC Sniffer, Smartcard Emulator
- **Scenario**: Attacker intercepts key initialization from smartcards during hybrid crypto provisioning via unencrypted NFC.
- **Attack Steps**: Step 1: Use Proxmark3 to sniff NFC traffic between smartcard and device. Step 2: Trigger key enrollment on the device (e.g., a secure messaging app). Step 3: Record hybrid key (PQC + RSA) initialization traffic. Step 4: Analyze if RSA portion is transmitted in plaintext. Step 5: Replay session using smartcard emulator to gain access.
- **Detection**: NFC traffic monitoring
- **Solution**: Enforce mutual NFC key wrapping
- **Tags**: nfc, smartcard, pqc-leak

## Wi-Fi Timing Side-Channel Leak During Hybrid Handshake

- **Attack Type**: Side-Channel (Timing)
- **Target**: Laptop, Router
- **Vulnerability**: RSA not constant-time during PQ hybrid
- **MITRE**: T1040, T1069.002
- **Impact**: Partial RSA key recovery
- **Tools**: Python (time-based logger), Wireshark
- **Scenario**: Exploiting microsecond timing differences in hybrid key negotiation over Wi-Fi to infer RSA key segments.
- **Attack Steps**: Step 1: Observe multiple key exchanges from target system over Wi-Fi using Wireshark. Step 2: Log time between each message, especially RSA+PQC steps. Step 3: Analyze slight delays indicating RSA computation delays (non-constant-time). Step 4: Correlate delay patterns with key bits. Step 5: Use known timing attack tools to infer key bytes.
- **Detection**: Anomalous handshake timing
- **Solution**: Use constant-time crypto libraries
- **Tags**: sidechannel, rsa-leak, timing-attack

## Bluetooth Crypto Token Hijacking During Hybrid Seed Sync

- **Attack Type**: BLE Injection
- **Target**: PQ Crypto Token
- **Vulnerability**: Unauthenticated BLE entropy transfer
- **MITRE**: T1557.003, T1600
- **Impact**: Seed poisoning, key compromise
- **Tools**: BLEah, gattacker, hciconfig
- **Scenario**: A BLE-based post-quantum crypto token transmits seed entropy over unsecured BLE; attacker spoofs seed and injects rogue entropy.
- **Attack Steps**: Step 1: Scan for BLE crypto tokens nearby (like Ledger, Trezor). Step 2: Use gattacker to clone advertised service. Step 3: On victim’s device, force reconnection to rogue BLE peripheral. Step 4: During seed sync, inject fake entropy to compromise hybrid key. Step 5: Save session key material and log for analysis.
- **Detection**: BLE pairing & entropy logs
- **Solution**: Secure entropy with mutual auth
- **Tags**: crypto-token, ble, entropy-attack

## Misconfigured IoT Gateway Downgrades PQ Traffic on Wi-Fi Backhaul

- **Attack Type**: IoT Gateway Exploit
- **Target**: IoT Gateway Device
- **Vulnerability**: Legacy TLS fallback on cloud route
- **MITRE**: T1040, T1600, T1071.001
- **Impact**: Hybrid key sniffed on gateway uplink
- **Tools**: Wireshark, Mitmproxy, Aircrack-ng
- **Scenario**: IoT gateway converts PQ traffic to legacy TLS over its Wi-Fi backhaul due to legacy firmware.
- **Attack Steps**: Step 1: Identify IoT Gateway device using nmap and device fingerprinting. Step 2: Connect to the same Wi-Fi backhaul. Step 3: Use Wireshark to monitor traffic from gateway to cloud. Step 4: Spot downgrade to TLS 1.1 or weak ciphers. Step 5: Use Mitmproxy to intercept legacy TLS. Step 6: Capture and analyze hybrid key session (RSA/PQC).
- **Detection**: Gateway firmware logging
- **Solution**: Enforce E2E PQ-TLS across mesh
- **Tags**: iot, gateway, downgrade, pqc

## LoRa PHY Sniffing of Hybrid Key Exchange in Sensor-to-Gateway Comm

- **Attack Type**: LoRa Eavesdropping
- **Target**: LoRa Sensors
- **Vulnerability**: No PHY-layer encryption
- **MITRE**: T1600, T1040
- **Impact**: Partial key interception
- **Tools**: HackRF, GNU Radio, LoRaTap
- **Scenario**: During PQ key distribution between field sensor and gateway using LoRa, unencrypted metadata or partial key exposed.
- **Attack Steps**: Step 1: Use HackRF with LoRaTap to sniff LoRaWAN frequencies. Step 2: Record physical-layer packets containing handshake info. Step 3: Parse metadata and hybrid crypto key headers. Step 4: Replay or analyze headers to retrieve RSA components.
- **Detection**: LoRaWAN analyzer + CRC errors
- **Solution**: Use end-to-end PQ encryption
- **Tags**: lora, pqc, wireless-sniff

## Fake Wi-Fi Firmware Update Triggers RSA Fallback in PQ Router

- **Attack Type**: Firmware Backdoor
- **Target**: PQ Wi-Fi Router
- **Vulnerability**: No firmware authenticity check
- **MITRE**: T1203, T1542.001
- **Impact**: Downgrade to legacy crypto
- **Tools**: Evilgrade, MITMf, DNS Spoof
- **Scenario**: Attacker injects malicious firmware to downgrade PQ router's crypto suite via wireless update over web UI.
- **Attack Steps**: Step 1: DNS spoof vendor’s firmware server address. Step 2: Create and serve fake firmware with RSA-only suite. Step 3: Push update via captive portal or phishing email. Step 4: Monitor device reboot and handshake with downgraded cipher. Step 5: Intercept hybrid connections and capture legacy keys.
- **Detection**: Syslog monitoring, unexpected version
- **Solution**: Enforce signed firmware with PQ hashes
- **Tags**: router, firmware-attack, rsa-fallback

## Quantum-Enabled SDR Replay of Wi-Fi Handshake with Crypto Bias Detection

- **Attack Type**: SDR-Based Analysis
- **Target**: Wi-Fi Hybrid Crypto Device
- **Vulnerability**: Radio-layer bias in PQ handshake
- **MITRE**: T1040, T1600
- **Impact**: Key prediction or downgrade
- **Tools**: RTL-SDR, GQRX, GNURadio, SigMF
- **Scenario**: Attackers use Software Defined Radios to record and analyze hybrid crypto handshake waveforms for anomalies or key bias.
- **Attack Steps**: Step 1: Use SDR (like RTL-SDR) to record handshake waveforms on 2.4GHz. Step 2: Replay handshake using SigMF or GQRX. Step 3: Feed handshake into GNURadio pipeline for entropy detection. Step 4: Detect key bias or repeated patterns. Step 5: Correlate bias with RSA fallback logic.
- **Detection**: SDR entropy logs, waveform analysis
- **Solution**: Use verified entropy sources
- **Tags**: sdr, hybrid-crypto, waveform-analysis

## Wi-Fi PMF (Protected Management Frames) Disabled During PQ Device Pairing

- **Attack Type**: PMF Disable Exploit
- **Target**: Secure Email Clients
- **Vulnerability**: PMF not enforced by device
- **MITRE**: T1531, T1557.001
- **Impact**: Key hijack via rogue AP
- **Tools**: MDK4, Wireshark, Airgeddon
- **Scenario**: Attacker disables Protected Management Frames during pairing, allowing deauth and rogue AP replay to hijack hybrid key exchange.
- **Attack Steps**: Step 1: Scan Wi-Fi networks for PQ-enabled devices (e.g., secure email clients). Step 2: Use MDK4 to flood deauth frames. Step 3: Device reconnects to a rogue AP. Step 4: Rogue AP offers downgraded key suite (RSA). Step 5: Capture and log handshake for key reconstruction.
- **Detection**: Frame integrity check logs
- **Solution**: Enforce WPA3 + PMF-only
- **Tags**: pmf, deauth, pq-fallback

## Wi-Fi EAP Downgrade Attack During PQ VPN Authentication

- **Attack Type**: Wireless Downgrade
- **Target**: Enterprise Laptop
- **Vulnerability**: Misconfigured EAP settings, RSA fallback
- **MITRE**: T1557.001 (Adversary-in-the-Middle), T1040 (Network Sniffing)
- **Impact**: Legacy key exposure during authentication
- **Tools**: hostapd-wpe, Airgeddon, Wireshark
- **Scenario**: An attacker exploits misconfigured WPA2-Enterprise (EAP) settings to force the victim to use legacy RSA authentication instead of hybrid PQ+RSA handshake.
- **Attack Steps**: Step 1: Setup a rogue Wi-Fi access point using hostapd-wpe with the same SSID as the victim's enterprise Wi-Fi. Step 2: Configure the AP to use WPA2-Enterprise and support only weak EAP types like EAP-MD5 or EAP-TTLS, which favor RSA. Step 3: Use Airgeddon to send deauthentication packets, disconnecting the victim from the real AP. Step 4: The victim connects to the rogue AP, thinking it's the legitimate one. Step 5: During VPN bootstrapping, the victim authenticates using EAP + RSA (instead of PQ+RSA hybrid), and the attacker captures this exchange using Wireshark. Step 6: Replay and analyze the handshake to extract legacy RSA portions for brute-force simulation or offline cracking.
- **Detection**: Wi-Fi log analysis, authentication failures
- **Solution**: Enforce EAP-TLS with strict PQC handshake verification
- **Tags**: wireless, EAP, RSA-downgrade, pq-vpn

## SDR Injection into Quantum Satellite Receiver Using Legacy Crypto Signal

- **Attack Type**: SDR Spoofing
- **Target**: Satellite Receiver
- **Vulnerability**: No validation of PQC presence, legacy fallback
- **MITRE**: T1600 (Weaken Encryption), T1583.001 (Spoof Application Layer)
- **Impact**: Successful signal spoofing and key compromise
- **Tools**: HackRF, GNURadio, SatNOGS, GQRX
- **Scenario**: Exploiting satellite link fallback by injecting legacy RSA-based signal during hybrid key sync using an SDR, misleading the receiver.
- **Attack Steps**: Step 1: Use satellite monitoring tools like SatNOGS and GQRX to identify a quantum-resistant satellite broadcast band in use. Step 2: Analyze the modulation and signal pattern used for key distribution. Step 3: Use GNURadio and HackRF to craft a spoofed message that mimics legitimate satellite hybrid key sync (RSA + PQC). Step 4: Remove PQ component from the crafted message and retain only legacy RSA. Step 5: Transmit this message using HackRF toward the satellite receiver (a ground station or secure modem). Step 6: The receiver mistakenly uses RSA-only key material, assuming it was a valid hybrid message. Step 7: Attacker captures responses to analyze encrypted data using the weaker RSA component.
- **Detection**: Radio signal spectrum anomalies
- **Solution**: Strict message validation with PQC checksum
- **Tags**: sdr, satellite, rsa-injection, hybrid-attack

## 5G Authentication Slice Hijack Leading to PQ Credential Downgrade

- **Attack Type**: Wireless Slice Spoofing
- **Target**: 5G Devices
- **Vulnerability**: Slice configuration mismatch, downgrade possible
- **MITRE**: T1557, T1071.001
- **Impact**: Capturing credentials under downgraded policy
- **Tools**: Open5GS, srsRAN, USRP, Wireshark
- **Scenario**: In 5G networks, the attacker spoofs the authentication slice using weak crypto settings and captures credentials meant for PQC-hardened systems.
- **Attack Steps**: Step 1: Deploy a fake gNodeB (5G base station) using srsRAN or Open5GS with a software radio like USRP. Step 2: Broadcast a legitimate-looking 5G network using the same MCC/MNC as the real one, but enable a lower-security slice (e.g., one that only supports RSA). Step 3: Wait for a victim device (like a mobile PQC app) to connect for authentication. Step 4: Capture the authentication and key negotiation messages. Step 5: Observe if the client uses a hybrid handshake (PQ+RSA) or only RSA due to slice policy. Step 6: If RSA is used, replay and analyze for key compromise opportunities.
- **Detection**: Mobile logs, slice mismatch detection
- **Solution**: Enforce PQC-only slices for secure use cases
- **Tags**: 5g, slice-hijack, rsa-downgrade

## Wi-Fi Supply Chain Backdoor Causes PQ Protocol Replacement

- **Attack Type**: Firmware Downgrade
- **Target**: IoT or Wi-Fi Device
- **Vulnerability**: Firmware integrity not verified
- **MITRE**: T1600 (Downgrade Attack), T1542.001 (System Firmware)
- **Impact**: Complete fallback to legacy crypto
- **Tools**: Binwalk, Firmware-Mod-Kit, Wireshark
- **Scenario**: Wi-Fi module with a compromised firmware update silently replaces hybrid crypto libraries with RSA-only variants during initialization.
- **Attack Steps**: Step 1: Use Binwalk to extract firmware from the Wi-Fi module of a target IoT device. Step 2: Analyze the crypto libraries being loaded during handshake initiation. Step 3: Replace hybrid crypto library (e.g., liboqs + OpenSSL) with a backdoored RSA-only variant. Step 4: Flash the modified firmware using UART or JTAG interface. Step 5: Connect the device to the network and initiate crypto handshake. Step 6: Use Wireshark to verify that the device is only performing RSA handshakes instead of hybrid PQ handshakes. Step 7: Capture handshake data for offline RSA cracking attempts.
- **Detection**: Monitor firmware hash & load behavior
- **Solution**: Use signed PQC-hardened firmware with verification
- **Tags**: supply-chain, firmware, rsa-patch

## Captive Portal Triggers Forced Legacy TLS Tunnel in PQ VPN App

- **Attack Type**: Captive Portal Manipulation
- **Target**: VPN Applications
- **Vulnerability**: Poor handling of captive portal fallback
- **MITRE**: T1557, T1071.001
- **Impact**: Legacy TLS tunnel with exposed RSA
- **Tools**: EvilPortal (WiFi-Pumpkin3), Burp Suite, tcpdump
- **Scenario**: Attacker delays VPN connection behind captive portal, forcing the app to retry using TLS 1.0 + RSA fallback due to timeout.
- **Attack Steps**: Step 1: Setup a fake Wi-Fi network with a captive portal using WiFi-Pumpkin3. Step 2: Block all external ports temporarily using iptables rules, allowing only HTTP traffic. Step 3: Force user to authenticate through the captive portal before internet access is allowed. Step 4: Meanwhile, let their PQ VPN app retry key exchange. Step 5: Because of delay or poor handling, VPN app falls back to RSA-only TLS 1.0 to complete the tunnel. Step 6: Capture and inspect the legacy handshake using tcpdump or Wireshark.
- **Detection**: VPN logs, TLS version mismatch alerts
- **Solution**: Enforce minimum TLS 1.3, captive-aware VPNs
- **Tags**: tls-fallback, captive-portal, hybrid-vpn

## Breaking WEP Encrypted Legacy Wi-Fi

- **Attack Type**: Wireless Attack on Legacy Crypto
- **Target**: Industrial Access Point
- **Vulnerability**: WEP Cryptographic Weakness
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Unauthorized Access, Data Breach
- **Tools**: aircrack-ng, Wireshark, Alfa AWUS036NHA
- **Scenario**: An attacker targets a legacy access point using outdated WEP encryption still in use in older industrial IoT systems.
- **Attack Steps**: Step 1: Identify the WEP-encrypted network using airodump-ng. Step 2: Monitor traffic and collect enough Initialization Vectors (IVs). Step 3: Use aireplay-ng to inject ARP packets to speed up IV collection. Step 4: Once enough IVs are collected, use aircrack-ng to crack the WEP key. Step 5: Decrypt network traffic or join the network using the cracked key.
- **Detection**: Anomaly in packet injection patterns; Increased ARP requests
- **Solution**: Upgrade to WPA3 or disable legacy WEP networks
- **Tags**: WEP, Legacy Wi-Fi, Cryptanalysis

## Brute Forcing Legacy WPA-Personal with Weak Passphrase

- **Attack Type**: Wireless Credential Cracking
- **Target**: Home Routers or Legacy Enterprise Routers
- **Vulnerability**: Weak Key Management
- **MITRE**: T1110 (Brute Force)
- **Impact**: Full Network Access
- **Tools**: hcxdumptool, hashcat, wordlists
- **Scenario**: Exploiting legacy WPA (pre-WPA2) with short dictionary-based passphrase using wireless capture and offline cracking.
- **Attack Steps**: Step 1: Use hcxdumptool to capture PMKID handshake from the AP. Step 2: Transfer .pcapng file to system with GPU cracking capability. Step 3: Use hashcat with rockyou.txt or custom wordlist to brute-force the passphrase. Step 4: Access network once correct password is found.
- **Detection**: WPA handshake capture logs; Multiple auth attempts
- **Solution**: Enforce strong passphrases; Migrate to WPA3-Enterprise
- **Tags**: WPA1, PMKID, Brute Force

## Eavesdropping Legacy Bluetooth Encryption (v1.0/1.1)

- **Attack Type**: Bluetooth Eavesdropping
- **Target**: Legacy Bluetooth Devices
- **Vulnerability**: Weak Encryption Protocol
- **MITRE**: T1421 (Bluetooth Discovery)
- **Impact**: Credential Theft, Info Disclosure
- **Tools**: Ubertooth One, Wireshark-Bluetooth plugin
- **Scenario**: Intercepting communication between two devices using outdated Bluetooth protocol that lacks key diversification.
- **Attack Steps**: Step 1: Bring Ubertooth One near target devices using Bluetooth 1.0/1.1. Step 2: Start sniffing packets with ubertooth-btle and Wireshark. Step 3: Analyze key exchange if pairing occurs; extract static key. Step 4: Replay or decrypt messages if predictable key is reused.
- **Detection**: Bluetooth logs with static key usage
- **Solution**: Disable Bluetooth 1.0/1.1 support; upgrade firmware
- **Tags**: Bluetooth, Pre-Quantum Risk

## Cracking RFID Using Weak Legacy Encryption (MIFARE Classic)

- **Attack Type**: RFID Crypto Attack
- **Target**: Access Control Systems
- **Vulnerability**: Weak RFID Crypto (Crypto-1)
- **MITRE**: T1056.001 (Input Capture)
- **Impact**: Unauthorized Physical Access
- **Tools**: Proxmark3, mfoc, mfcuk
- **Scenario**: Attack on a smart card system still using MIFARE Classic (Crypto-1) vulnerable to pre-quantum brute-force.
- **Attack Steps**: Step 1: Use Proxmark3 to identify MIFARE Classic tag. Step 2: Run mfcuk to recover access keys using nested attack. Step 3: Use mfoc to dump the card content. Step 4: Clone card or analyze access patterns.
- **Detection**: RFID reader log anomalies; duplicate card IDs
- **Solution**: Upgrade to DESFire EV3 or NFC-based tokens
- **Tags**: RFID, Legacy Crypto

## Cracking Early Zigbee Traffic with No Encryption

- **Attack Type**: Zigbee Legacy Weakness Exploit
- **Target**: Home IoT Systems
- **Vulnerability**: No or Weak Zigbee Crypto
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Device Takeover
- **Tools**: KillerBee, ZBOSS Sniffer
- **Scenario**: Some older Zigbee-based home automation devices used plaintext communication or weak pre-shared keys.
- **Attack Steps**: Step 1: Use KillerBee’s zbstumbler to identify Zigbee channels and PANs. Step 2: Capture traffic with zbdump or ZBOSS sniffer. Step 3: If no encryption, decode messages directly. Step 4: Replay messages or issue spoofed commands using zbconsole.
- **Detection**: Increased Zigbee traffic; Command anomalies
- **Solution**: Use Zigbee 3.0 with encrypted link keys
- **Tags**: Zigbee, Weak Crypto

## Breaking Legacy VPN Over Wi-Fi Using Weak Pre-Shared Keys

- **Attack Type**: Wireless VPN Exploitation
- **Target**: Legacy Enterprise VPN Access
- **Vulnerability**: Weak VPN Cipher / Pre-shared Keys
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Full VPN Access, Info Disclosure
- **Tools**: Wireshark, aircrack-ng, hashcat
- **Scenario**: A company uses an old VPN setup (e.g., PPTP or L2TP with pre-shared key) for Wi-Fi access. The attacker leverages sniffing and offline dictionary attacks.
- **Attack Steps**: Step 1: Identify the target Wi-Fi network and capture VPN negotiation using airodump-ng. Step 2: Use Wireshark to isolate PPTP/L2TP handshake packets. Step 3: Extract MS-CHAPv2 handshake data. Step 4: Use tools like chapcrack and asleap to recover or brute-force the weak pre-shared key offline. Step 5: Connect to VPN using cracked key or decrypt captured traffic.
- **Detection**: VPN logs, Unusual access, Repeated handshakes
- **Solution**: Migrate to IKEv2/IPSec or SSL-VPN with certs
- **Tags**: PPTP, Wi-Fi VPN, Legacy Encryption

## Intercepting Legacy Wireless SCADA Comms (Proprietary RF)

- **Attack Type**: RF Protocol Sniffing
- **Target**: Industrial RF-based SCADA
- **Vulnerability**: No Encryption in Legacy RF
- **MITRE**: T1608 (Develop Capabilities)
- **Impact**: Unauthorized Equipment Control
- **Tools**: RTL-SDR, Universal Radio Hacker (URH)
- **Scenario**: Targeting SCADA systems that use unencrypted proprietary RF for command transmission in remote industrial environments.
- **Attack Steps**: Step 1: Identify the frequency used by legacy SCADA using RTL-SDR spectrum analyzer. Step 2: Use URH to capture and visualize protocol packets. Step 3: Replay and analyze signal patterns to identify start/end bits and repeating structure. Step 4: Reverse-engineer the protocol to mimic command structure. Step 5: Transmit spoofed control messages to SCADA using signal replay.
- **Detection**: RF spectrum anomalies; duplicate commands
- **Solution**: Upgrade to encrypted, modern SCADA RF stacks
- **Tags**: SCADA, RF Protocol, Legacy

## Exploiting Bluetooth Pairing with Legacy Static PIN

- **Attack Type**: Bluetooth Passive Key Capture
- **Target**: Bluetooth Devices (Old Phones, Cars)
- **Vulnerability**: Static PIN Vulnerability
- **MITRE**: T1421 (Bluetooth Discovery)
- **Impact**: Device Hijack, File Transfer Access
- **Tools**: Ubertooth One, Wireshark
- **Scenario**: Legacy Bluetooth (pre-v2.1) used static PINs like “0000” or “1234” which can be easily brute-forced during pairing sniffing.
- **Attack Steps**: Step 1: Monitor nearby Bluetooth traffic with Ubertooth One. Step 2: Identify pairing attempts between devices. Step 3: Capture PIN exchange protocol packets. Step 4: Use a brute-force tool to test static PINs like “0000”, “1111”. Step 5: Access or impersonate device after successful pairing.
- **Detection**: Bluetooth logs with rapid PIN retries
- **Solution**: Use Secure Simple Pairing (SSP) or BLE
- **Tags**: Bluetooth, Static PIN

## Attacking GSM A5/1 Encrypted Traffic from Legacy Phones

- **Attack Type**: GSM Interception
- **Target**: GSM 2G Phones
- **Vulnerability**: Weak GSM Encryption
- **MITRE**: T1422 (Wi-Fi Interception)
- **Impact**: Call/SMS Snooping
- **Tools**: USRP SDR, Kraken, Airprobe
- **Scenario**: GSM A5/1 is a weak stream cipher used in many 2G mobile calls and SMS. Attackers can intercept and decrypt traffic using rainbow tables.
- **Attack Steps**: Step 1: Use USRP SDR and gr-gsm to capture GSM downlink and uplink. Step 2: Extract TMSI and call/session keys. Step 3: Use Kraken tool and precomputed tables to break A5/1 stream cipher. Step 4: Decode call audio or SMS contents using Airprobe.
- **Detection**: SIM log analysis; SDR detection
- **Solution**: Use 3G/4G fallback blocking or encrypted comms apps
- **Tags**: GSM, A5/1, SDR, Quantum Risk

## Replay Attack on LoRaWAN v1.0.2 without MIC Protection

- **Attack Type**: LoRaWAN Protocol Exploit
- **Target**: IoT Environmental Sensors
- **Vulnerability**: No MIC / Replay Protection
- **MITRE**: T1609 (Data Manipulation)
- **Impact**: Sensor Data Corruption
- **Tools**: HackRF, GNURadio, LoRa packetsniffer
- **Scenario**: In LoRaWAN v1.0.2, lack of robust MIC (message integrity check) verification enables replay of captured sensor messages.
- **Attack Steps**: Step 1: Identify frequency and SF (spreading factor) using LoRa spectrum analysis. Step 2: Capture unencrypted uplink message using HackRF. Step 3: Analyze message for absence of MIC or nonce reuse. Step 4: Replay same packet multiple times to base station. Step 5: Cause data spoofing or actuator response.
- **Detection**: Discrepancies in repeated sensor readings
- **Solution**: Upgrade to LoRaWAN 1.1+ with MIC protection
- **Tags**: LoRa, MIC Weakness, Replay

## Decrypting Legacy WPA2 Enterprise using MSCHAPv2 Weakness

- **Attack Type**: Wi-Fi Enterprise Credential Downgrade
- **Target**: Enterprise Wi-Fi
- **Vulnerability**: Weak Auth Protocol
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Credential Theft
- **Tools**: FreeRADIUS-WPE, Responder, hashcat
- **Scenario**: Older WPA2-Enterprise networks using MSCHAPv2 are vulnerable to credential capture and offline cracking.
- **Attack Steps**: Step 1: Set up fake RADIUS server using FreeRADIUS-WPE. Step 2: Trick a device to connect using rogue AP and capture challenge-response. Step 3: Extract challenge hashes from logs. Step 4: Use hashcat to brute-force or dictionary attack the user credentials. Step 5: Use cracked credentials to log into network or VPN.
- **Detection**: Unusual RADIUS traffic; duplicate AP logs
- **Solution**: Use EAP-TLS or strong mutual authentication
- **Tags**: MSCHAPv2, WPA2, Wi-Fi, Legacy

## Passive Sniffing of IrDA Infrared Legacy Transmissions

- **Attack Type**: Infrared Comm Exploit
- **Target**: Legacy Infrared Devices
- **Vulnerability**: No Encryption in IR Transfers
- **MITRE**: T1420 (Data from Removable Media)
- **Impact**: Credential Leakage, File Theft
- **Tools**: IrDA USB Adapter, IrSniff
- **Scenario**: Older legacy systems use infrared (IrDA) for device syncing or data transfer which can be captured silently.
- **Attack Steps**: Step 1: Set up IrDA receiver near legacy system (e.g., printer or Palm device). Step 2: Wait for communication event (file send, print job). Step 3: Capture raw data packets using IrSniff. Step 4: Extract human-readable info or credentials. Step 5: Attempt replay or data injection via IrDA emulator.
- **Detection**: Noisy IR port usage; unusual pairing
- **Solution**: Disable IrDA; Replace with encrypted USB/BLE
- **Tags**: Infrared, Legacy, IrDA

## Intercepting Legacy IEEE 802.15.4 Wireless Sensor Data

- **Attack Type**: 802.15.4 Crypto Weakness
- **Target**: Wireless Sensor Networks
- **Vulnerability**: No/Weak AES Keys
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Sensor Spoofing, Privacy Breach
- **Tools**: KillerBee, ZBOSS
- **Scenario**: Older IEEE 802.15.4-based sensors often omit AES encryption or use default keys, exposing data in transit.
- **Attack Steps**: Step 1: Use KillerBee to scan for 802.15.4 beacons. Step 2: Capture data frames from specific PAN ID. Step 3: Analyze frame content to check for unencrypted payloads. Step 4: Reconstruct sensor data stream (e.g., temp, motion). Step 5: Optionally send spoofed control messages.
- **Detection**: Excessive 802.15.4 traffic in logs
- **Solution**: Enable AES-128 encryption; use PAN whitelisting
- **Tags**: 802.15.4, Zigbee, Quantum Crypto

## Attack on Legacy Wi-Fi WPS PIN Bruteforce (Pixie Dust)

- **Attack Type**: Wi-Fi PIN Bruteforce
- **Target**: Home Wi-Fi Routers
- **Vulnerability**: WPS PIN Predictability
- **MITRE**: T1110 (Brute Force)
- **Impact**: Network Access, Key Disclosure
- **Tools**: Reaver, PixieWPS, Wash
- **Scenario**: Older routers with WPS enabled are vulnerable to offline PIN attacks even without being physically near.
- **Attack Steps**: Step 1: Scan for WPS-enabled devices using wash. Step 2: Launch Pixie Dust attack with reaver -K on vulnerable router. Step 3: Extract public keys, nonces, and hashes from M1/M2 messages. Step 4: Calculate WPS PIN offline using PixieWPS tool. Step 5: Retrieve WPA2 password using cracked WPS PIN.
- **Detection**: Failed WPS attempts in logs
- **Solution**: Disable WPS or use push-button only
- **Tags**: Wi-Fi, WPS, Quantum Threat

## Cracking Legacy Wireless Industrial Protocols (MODBUS RF)

- **Attack Type**: MODBUS RF Protocol Attack
- **Target**: Industrial Control Systems
- **Vulnerability**: No Auth in MODBUS RF
- **MITRE**: T1609 (Data Manipulation)
- **Impact**: Industrial Sabotage
- **Tools**: HackRF, GNURadio, MODBUS toolkit
- **Scenario**: Older MODBUS over RF lacks encryption or authentication, allowing command injection to industrial controllers.
- **Attack Steps**: Step 1: Capture RF communication between PLC and sensors using HackRF. Step 2: Decode MODBUS RTU commands (e.g., Read Register, Write Coil). Step 3: Replay captured write commands or inject new values. Step 4: Observe actuator/PLC behavior changes. Step 5: Optional: simulate malicious override of equipment.
- **Detection**: Unexpected register writes in logs
- **Solution**: Replace with encrypted industrial protocol (e.g., OPC UA)
- **Tags**: MODBUS, RF, ICS, Quantum Risk

## Exploiting Legacy Telnet over Wireless for Config Capture

- **Attack Type**: Wireless Telnet Session Hijack
- **Target**: Industrial Gateways, Routers
- **Vulnerability**: Unencrypted Remote Access
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Credential Theft, Config Manipulation
- **Tools**: Wireshark, aircrack-ng
- **Scenario**: Many legacy industrial devices use Telnet over Wi-Fi for configuration access. These sessions are unencrypted, allowing attackers to read or hijack sessions via sniffing.
- **Attack Steps**: Step 1: Use airodump-ng to scan for target Wi-Fi traffic and identify the access point and client using Telnet. Step 2: Use airmon-ng to switch the wireless card to monitor mode and start capturing packets. Step 3: Open Wireshark and apply a filter for Telnet (port 23) to view plaintext login and commands. Step 4: Read credentials and configuration commands in real-time, such as usernames, passwords, or firmware commands. Step 5: Optionally, inject packets or spoof session responses if required, although this can destabilize the system.
- **Detection**: Unusual Telnet session patterns in logs
- **Solution**: Disable Telnet and use SSH or VPN tunnels
- **Tags**: Telnet, Legacy Protocol, Wi-Fi

## Hijacking Legacy BLE Connection Without Authentication

- **Attack Type**: BLE Legacy Link Hijacking
- **Target**: BLE Devices (Sensors, Health Trackers)
- **Vulnerability**: No Authentication
- **MITRE**: T1557.003 (Bluetooth)
- **Impact**: Data Theft, Device Control
- **Tools**: nRF Connect, Btlejack
- **Scenario**: Older BLE devices sometimes skip authentication and allow plaintext read/write without verifying paired devices, exposing them to session hijacking.
- **Attack Steps**: Step 1: Use Btlejack to scan nearby BLE devices and identify the target’s MAC address and services. Step 2: Monitor BLE advertisements and establish a connection with the device using a tool like nRF Connect. Step 3: Explore readable characteristics and permissions. Identify writable attributes like control commands or settings. Step 4: Inject values into writable characteristics (e.g., control commands or status flags). Step 5: Read and log private data like sensor states, battery level, or location (if exposed).
- **Detection**: BLE log mismatch; unauthorized GATT writes
- **Solution**: Use BLE 5.x with secure pairing methods
- **Tags**: BLE, Legacy Crypto, GATT

## Cracking Weak Encrypted Zigbee Firmware Updates

- **Attack Type**: Zigbee Firmware Update Manipulation
- **Target**: Zigbee Smart Devices
- **Vulnerability**: Static Key in Firmware
- **MITRE**: T1601.001 (Modify System Firmware)
- **Impact**: Device Tampering, Code Injection
- **Tools**: ZBOSS Sniffer, Ghidra, KillerBee
- **Scenario**: Older Zigbee devices receive firmware updates over-the-air using AES keys hardcoded in firmware. Attackers can intercept and decrypt these updates.
- **Attack Steps**: Step 1: Use ZBOSS or KillerBee to sniff Zigbee traffic during a firmware update session. Step 2: Extract the encrypted firmware payload and locate the AES key segment if reused across devices. Step 3: Decompile a physical device’s firmware using Ghidra to find AES key or update validation routine. Step 4: Decrypt captured payload and analyze the update logic. Step 5: Modify update contents (e.g., disable sensor, change thresholds) and replay with modified payload.
- **Detection**: Mismatched firmware hash or behavior
- **Solution**: Use per-device keys and signed firmware updates
- **Tags**: Zigbee, AES Key Reuse, Firmware

## Exploiting Legacy Wireless Barcode Scanners (Proprietary RF)

- **Attack Type**: RF Protocol Spoofing
- **Target**: Retail/Inventory Systems
- **Vulnerability**: RF Channel Spoofing
- **MITRE**: T1609 (Data Manipulation)
- **Impact**: Inventory Tampering
- **Tools**: HackRF One, URH, GNURadio
- **Scenario**: Legacy barcode scanners use proprietary 433MHz/900MHz RF with weak or no encryption. Attackers can intercept and inject data into the system.
- **Attack Steps**: Step 1: Use HackRF and URH to monitor RF communication between barcode scanner and its base station. Step 2: Identify consistent transmission patterns—barcode contents are often in plaintext. Step 3: Decode protocol and format by replaying captured signal with timing tweaks. Step 4: Transmit modified codes (e.g., fake product ID or inventory code) using GNURadio replay block. Step 5: Confirm data injection on POS system or inventory software.
- **Detection**: Repeated barcodes; incorrect logs
- **Solution**: Use encrypted BLE or QR scanning devices
- **Tags**: Barcode, RF, Legacy Device

## Interception of 2.4GHz Analog Video Feeds from Legacy Cameras

- **Attack Type**: Analog Wireless Signal Capture
- **Target**: Legacy CCTV Systems
- **Vulnerability**: No Signal Encryption
- **MITRE**: T1123 (Audio Capture) & T1113 (Screen Capture)
- **Impact**: Privacy Violation, Recon
- **Tools**: RTL-SDR, AV Receiver, TV Tuner Card
- **Scenario**: Legacy CCTV cameras transmit analog video over 2.4GHz without encryption. Anyone with a matching receiver can view the footage.
- **Attack Steps**: Step 1: Use RTL-SDR or analog video receiver to scan 2.4GHz frequencies used by CCTV systems. Step 2: Adjust gain, frequency offset, and bandwidth to lock onto the analog video signal. Step 3: Display live feed using compatible tuner software or composite input card. Step 4: Record footage or take snapshots for later analysis or surveillance mapping. Step 5: Optionally, replay feed or jam signal with analog transmitter (for educational use only).
- **Detection**: Signal overlap detection; unknown viewer alerts
- **Solution**: Replace with encrypted IP-based CCTV systems
- **Tags**: CCTV, Analog, 2.4GHz

## Downgrade via Wi-Fi Negotiation Interception

- **Attack Type**: Cryptographic Downgrade via Wi-Fi Handshake Hijack
- **Target**: PQC-enabled Wi-Fi Routers or Clients
- **Vulnerability**: Lack of strong enforcement of PQC-only mode
- **MITRE**: T1584.001 (Compromise Infrastructure: Domains)
- **Impact**: Confidentiality breach; user assumes PQC security but is vulnerable
- **Tools**: Wireshark, aireplay-ng, Scapy
- **Scenario**: During PQC protocol negotiation over Wi-Fi, an attacker intercepts the handshake and forces the device to fall back to classical cryptography.
- **Attack Steps**: Step 1: Set up a rogue Wi-Fi access point mimicking the original network name (SSID).Step 2: Use aireplay-ng to send deauthentication packets to disconnect the legitimate device.Step 3: When the target reconnects, intercept the handshake using Wireshark.Step 4: Modify handshake packets using Scapy to strip PQC extensions.Step 5: Forward modified packets to server, forcing fallback to classical cryptographic algorithms.Step 6: Record entire session for later cryptanalysis of classical cipher.
- **Detection**: Monitor handshake negotiation logs; detect lack of PQC extension
- **Solution**: Enforce PQC-only negotiation policy and certificate pinning
- **Tags**: downgrade, PQC, Wi-Fi, handshake manipulation

## Bluetooth-Based PQC Downgrade via Forced Legacy Pairing

- **Attack Type**: Cryptographic Downgrade via Bluetooth Legacy Pairing
- **Target**: PQC Bluetooth Devices (e.g., IoT or Wearables)
- **Vulnerability**: Backward compatibility with classical SSP
- **MITRE**: T1477 (Bluetooth Discovery)
- **Impact**: Key compromise through weak crypto fallback
- **Tools**: Ubertooth One, Bluetoothctl, hcitool
- **Scenario**: An attacker forces a Bluetooth device transitioning to PQC back into legacy SSP (Secure Simple Pairing), exposing keys to future quantum decryption.
- **Attack Steps**: Step 1: Use Ubertooth to scan for PQC-transitioning Bluetooth devices.Step 2: Send crafted Bluetooth pairing requests using hcitool to force legacy SSP fallback.Step 3: Initiate pairing while suppressing PQC-based options.Step 4: Capture key exchange in plaintext or weak classical format.Step 5: Store session keys for quantum-cracking simulation.
- **Detection**: Compare pairing protocol versions in logs
- **Solution**: Disable legacy pairing modes, enforce PQC handshakes
- **Tags**: bluetooth, downgrade, legacy compatibility

## Wi-Fi Hotspot Downgrade with Captive Interstitial Injection

- **Attack Type**: Downgrade Attack via Captive Portal Rewrite
- **Target**: PQC TLS-enabled Browsers or Mobile Clients
- **Vulnerability**: User trust in captive portals and no PQC enforcement
- **MITRE**: T1557.003 (Adversary-in-the-Middle: LLMNR/NBT-NS Poisoning)
- **Impact**: Users believe their traffic is PQC-protected; attacker harvests sessions
- **Tools**: Fluxion, EvilAP, Bettercap, mitmproxy
- **Scenario**: Captive portal interstitials used in public Wi-Fi environments are manipulated to prevent PQC-enabled TLS from being completed, falling back to classical cipher suite.
- **Attack Steps**: Step 1: Set up EvilAP with the same SSID as public Wi-Fi.Step 2: Use captive portal tools (e.g., Fluxion) to serve a fake authentication page.Step 3: Intercept client's HTTPS request and strip PQC cipher list using mitmproxy.Step 4: Rewrite TLS handshake forcing downgrade to classical RSA.Step 5: Log all user credentials and session keys.Step 6: Relay altered request to real server after downgrade succeeds.
- **Detection**: TLS handshake inspection; validate PQC negotiation
- **Solution**: Use HTTPS with PQC-only cipher suite enforcement and DoH
- **Tags**: captive portal, TLS downgrade, Wi-Fi, mitm

## Forced Downgrade via RF Jamming and Retry Induction

- **Attack Type**: Active Jamming-Induced Protocol Fallback
- **Target**: PQC Wi-Fi or 5G Communication Devices
- **Vulnerability**: Retry logic not secure; allows downgrade
- **MITRE**: T1498.001 (Network Denial of Service)
- **Impact**: Forced downgrade via denial of PQC channel
- **Tools**: HackRF, GNURadio, Wireshark
- **Scenario**: By actively jamming PQC handshake signals and allowing only classical protocols through, the attacker causes retry attempts to use fallback algorithms.
- **Attack Steps**: Step 1: Use HackRF with GNURadio to identify PQC negotiation frequencies.Step 2: Emit continuous interference (jamming) over PQC handshake channel.Step 3: Observe that device retries negotiation using classical channel.Step 4: Capture handshake with Wireshark.Step 5: Analyze resulting session to confirm fallback to RSA or ECC.Step 6: Store data for quantum decryption attempt.
- **Detection**: Spectrum analysis; check retry pattern for anomalies
- **Solution**: Employ PQC-only communication retry logic
- **Tags**: jamming, fallback, handshake, RF, downgrade

## LoRaWAN Join Request Downgrade via Protocol Manipulation

- **Attack Type**: Downgrade of LoRaWAN PQC Key Join Procedure
- **Target**: PQC-enabled LoRa/LPWAN Devices
- **Vulnerability**: Unauthenticated Join Request modification
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Long-range IoT traffic exposed to crypto attacks
- **Tools**: SDR, LoRaWAN Forwarder, Scapy, Wireshark
- **Scenario**: PQC enhancements in LoRaWAN Join Request messages are stripped via MITM relay using a rogue gateway.
- **Attack Steps**: Step 1: Set up rogue LoRaWAN gateway using SDR and modified forwarder code.Step 2: Capture Join Request from end-device.Step 3: Strip PQC-specific key exchange options from message using Scapy.Step 4: Forward manipulated message to real LoRaWAN network server.Step 5: Allow session to proceed using classical keys.Step 6: Log entire session and simulate quantum decryption.
- **Detection**: Analyze join procedure for key size and cipher suite used
- **Solution**: Enforce signed join requests with PQC validation
- **Tags**: lora, join request, PQC bypass, LPWAN

## Zigbee Link Key Downgrade via Custom Radio Injection

- **Attack Type**: Cryptographic Downgrade via Zigbee Join Request
- **Target**: Smart Home Zigbee Devices
- **Vulnerability**: Weak enforcement of PQC join security
- **MITRE**: T1557.002 (Adversary-in-the-Middle: ARP Cache Poisoning)
- **Impact**: Loss of PQC protection in home automation
- **Tools**: KillerBee, RZ Raven USB Stick, Scapy-radio
- **Scenario**: A Zigbee device supporting PQC key exchange is tricked into accepting a default link key through a spoofed join request with no PQC negotiation.
- **Attack Steps**: Step 1: Use Zigbee sniffer (KillerBee) to monitor for Zigbee device association requests.Step 2: Intercept and analyze any PQC-capable handshake.Step 3: Jam association message and send forged join request to coordinator with classical link key.Step 4: Allow session to proceed under classical encryption.Step 5: Log key material from default key usage.Step 6: Replay or analyze session for downgrade proof.
- **Detection**: Analyze join logs for key mismatch
- **Solution**: Enforce PQC-only link key use and white-listing
- **Tags**: zigbee, downgrade, join, wireless

## LTE IMSI Catcher Downgrade to Classical Crypto

- **Attack Type**: Crypto Downgrade via Rogue eNodeB
- **Target**: LTE Smartphones & Modems
- **Vulnerability**: Cipher suite fallback in EPS-AKA
- **MITRE**: T1646 (Impersonation)
- **Impact**: Reduced confidentiality of mobile traffic
- **Tools**: srsLTE, OpenLTE, USRP, Wireshark
- **Scenario**: A fake LTE tower forces the victim device to connect without PQC enhancements, using outdated cipher suites for authentication.
- **Attack Steps**: Step 1: Deploy a rogue LTE eNodeB using OpenLTE or srsLTE on a USRP device.Step 2: Broadcast the same MCC/MNC as the real network with higher signal strength.Step 3: Intercept UE’s connection attempt and force downgrade of encryption algorithm (e.g., AES to KASUMI).Step 4: Record initial authentication and challenge exchanges.Step 5: Relay requests to real network to maintain covertness.Step 6: Store weak session key for later quantum decryption.
- **Detection**: Check for known rogue towers and weak algorithms
- **Solution**: Implement PQC constraints in UE firmware
- **Tags**: lte, imsi, rogue tower, downgrade

## WPA3 Transition Downgrade via PMF Bypass

- **Attack Type**: Downgrade to WPA2 using Protected Management Frame Misuse
- **Target**: WPA3 Wi-Fi Clients
- **Vulnerability**: WPA2 fallback enabled in transition mode
- **MITRE**: T1557.004 (Adversary-in-the-Middle: DHCP Spoofing)
- **Impact**: PQC handshake is avoided completely
- **Tools**: aireplay-ng, hcxdumptool, Bettercap
- **Scenario**: WPA3 handshake with PQC elements is interrupted, and WPA2 fallback is triggered via frame manipulation.
- **Attack Steps**: Step 1: Use hcxdumptool to capture WPA3 handshake attempt.Step 2: Send spoofed PMF frames to confuse the client about the AP’s PQC support.Step 3: Force disconnection using aireplay-ng.Step 4: Client reconnects using WPA2 as fallback.Step 5: Capture WPA2 4-way handshake.Step 6: Store session data for cracking simulation.
- **Detection**: Analyze PMF behavior during connections
- **Solution**: Disable WPA2 fallback; enforce strict WPA3+PQC
- **Tags**: wpa3, downgrade, wireless, pmf

## SDR-Based Interference of PQC Beacon Advertisements

- **Attack Type**: Beacon Frame Tampering to Suppress PQC Options
- **Target**: PQC-enabled Wi-Fi Clients
- **Vulnerability**: Lack of beacon validation or prioritization
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Rogue AP causes downgrade to classic crypto
- **Tools**: GNURadio, HackRF, Scapy
- **Scenario**: A rogue AP broadcasts identical SSID but omits PQC advertising fields, misleading clients to downgrade.
- **Attack Steps**: Step 1: Monitor beacon frames of legitimate AP and note PQC support field.Step 2: Clone SSID using HackRF with crafted beacon frames that omit PQC capability.Step 3: Flood the environment with modified beacons using GNURadio.Step 4: Client device associates with rogue AP that supports only classical TLS.Step 5: Perform MitM to intercept and downgrade cryptographic negotiation.Step 6: Relay modified connection to real AP or simulate access.
- **Detection**: Compare beacon fields with expected PQC flags
- **Solution**: Prioritize PQC indicators in beacon processing
- **Tags**: beacon, tls, mitm, downgrade

## BLE Advertising Downgrade via PHY Disruption

- **Attack Type**: Crypto Downgrade through PHY-level Disruption in BLE
- **Target**: BLE IoT Devices
- **Vulnerability**: BLE PHY mode fallbacks allow PQC bypass
- **MITRE**: T1647 (Protocol Impersonation)
- **Impact**: BLE session does not gain PQC security
- **Tools**: BTLEJack, Ubertooth One, BLEAH
- **Scenario**: BLE device forced to fall back to classical crypto due to PHY failure during PQC exchange advertisement.
- **Attack Steps**: Step 1: Monitor BLE advertisement packets to detect PQC mode support.Step 2: Use BTLEJack to inject malformed packets that cause PQC-related PHY mode to fail.Step 3: Force the device to switch to legacy PHY mode (1M vs Coded PHY).Step 4: Initiate connection using downgraded PHY.Step 5: Observe handshake and ensure only classical crypto options are used.Step 6: Capture session data for later cryptanalysis.
- **Detection**: Monitor PHY mode used during advertising
- **Solution**: Reject non-PQC PHY handshakes; enable alerts
- **Tags**: ble, downgrade, advertisement

## 5G SUCI Downgrade to IMSI Exposure via Base Station Trick

- **Attack Type**: SUCI Downgrade via Weak gNB
- **Target**: 5G Smartphones
- **Vulnerability**: PQC-based SUCI not enforced in all networks
- **MITRE**: T1583.006 (Acquire Infrastructure: Web Services)
- **Impact**: Permanent identity exposure on air
- **Tools**: srsRAN 5G, USRP B210, Wireshark
- **Scenario**: 5G device is forced to expose IMSI directly by pretending the network doesn’t support PQC SUCI encryption.
- **Attack Steps**: Step 1: Deploy rogue 5G gNB using srsRAN 5G.Step 2: Broadcast parameters that indicate lack of PQC SUCI support.Step 3: UE falls back to sending IMSI unencrypted.Step 4: Capture full NAS registration request using Wireshark.Step 5: Replay session to real network if needed.Step 6: Log and analyze impact of missing SUCI protection.
- **Detection**: Check whether SUCI was sent or not
- **Solution**: Make SUCI mandatory in UE policy
- **Tags**: 5g, suci, downgrade, imsi

## RF Injection Downgrade in Quantum-Ready RFID Systems

- **Attack Type**: RFID Reader Downgrade via RF Noise Injection
- **Target**: RFID Tags (e.g., smart ID, access cards)
- **Vulnerability**: Retry logic lacks PQC integrity check
- **MITRE**: T1134.002 (Access Token Manipulation)
- **Impact**: RFID can be cloned using classical methods
- **Tools**: Proxmark3, Signal Generator
- **Scenario**: PQC handshake between RFID tag and reader is disrupted, forcing use of classical AES-based authentication.
- **Attack Steps**: Step 1: Identify RFID system supporting PQC-authentication.Step 2: Use signal generator to emit narrow-band interference during key negotiation.Step 3: Reader retries using fallback AES protocol.Step 4: Capture RFID session using Proxmark3.Step 5: Replay or analyze classical authentication.Step 6: Demonstrate how fallback enables cloning attack.
- **Detection**: Detect handshake failures and protocol switch
- **Solution**: Disable fallback modes, enforce retry lockout
- **Tags**: rfid, pqc, downgrade, replay

## Hidden SSID PQC Suppression via Wi-Fi Profile Injection

- **Attack Type**: Crypto Downgrade via SSID Spoofing and Profile Hijack
- **Target**: Wi-Fi Clients with Saved Network Profiles
- **Vulnerability**: Connection priority logic abused
- **MITRE**: T1185 (Browser Session Hijacking)
- **Impact**: Silent downgrade due to hidden SSID
- **Tools**: Kismet, aireplay-ng, Bettercap
- **Scenario**: Devices are lured to hidden networks that use same SSID but no PQC support, using saved profiles and connection priority abuse.
- **Attack Steps**: Step 1: Set up rogue AP with hidden SSID matching a saved profile (without PQC).Step 2: Use aireplay-ng to deauth user from legitimate network.Step 3: Device auto-connects to hidden network using saved credentials.Step 4: Observe connection using only classical cryptography.Step 5: Intercept traffic using Bettercap to monitor downgrade.Step 6: Relay or alter data to simulate MITM.
- **Detection**: Detect profile priority mismatches
- **Solution**: Enforce profile fingerprinting with PQC labels
- **Tags**: wifi, profile, hidden ssid, downgrade

## Secure Email over Wi-Fi Downgrade via SMTP Cipher Truncation

- **Attack Type**: Downgrade TLS in Wi-Fi-based Email Apps
- **Target**: Email Clients on Wi-Fi
- **Vulnerability**: STARTTLS downgrade not validated
- **MITRE**: T1557.001 (Adversary-in-the-Middle: ARP Spoofing)
- **Impact**: Email confidentiality breach
- **Tools**: mitmproxy, dnschef, EvilAP
- **Scenario**: On a public network, SMTP communication is intercepted and PQC cipher list is removed, forcing classical encryption.
- **Attack Steps**: Step 1: Create EvilAP that redirects email traffic.Step 2: Use dnschef to spoof MX records to attack server.Step 3: Use mitmproxy to intercept and modify SMTP STARTTLS.Step 4: Truncate PQC ciphers and only allow classical algorithms.Step 5: Forward email with weak crypto.Step 6: Log credentials and messages.
- **Detection**: SMTP logs with STARTTLS downgrade patterns
- **Solution**: Enable MTA-STS and DANE with PQC constraints
- **Tags**: smtp, email, downgrade, tls

## QR Code Over Wi-Fi Downgrade in Device Provisioning

- **Attack Type**: Downgrade in Device Onboarding via Wi-Fi QR Code
- **Target**: IoT Devices (Smart Cameras, etc.)
- **Vulnerability**: No PQC validation in QR-based onboarding
- **MITRE**: T1056.001 (Input Capture: Keylogging)
- **Impact**: Device begins life with weak crypto settings
- **Tools**: Wireshark, RogueAP, QR Code Spoof Generator
- **Scenario**: IoT device being provisioned via Wi-Fi QR code gets intercepted, and provisioning is redone without PQC encryption.
- **Attack Steps**: Step 1: Set up rogue AP mimicking SSID from QR code.Step 2: Generate fake QR code for test lab with similar SSID but no PQC support.Step 3: Trick user into scanning fake QR code.Step 4: IoT device connects to rogue AP and is provisioned via classical TLS.Step 5: Log provisioning handshake and credentials.Step 6: Replay session or decrypt provisioning traffic.
- **Detection**: Check provisioning logs and AP PQC capabilities
- **Solution**: Use digitally signed QR codes and validate PQC on connect
- **Tags**: onboarding, qr, downgrade, iot

## Forced TLS Downgrade in Wi-Fi Mesh via Broadcast Injection

- **Attack Type**: PQC Downgrade via Mesh Control Frame Spoofing
- **Target**: Wi-Fi Mesh Clients and Routers
- **Vulnerability**: Mesh management protocols not integrity-checked for PQC
- **MITRE**: T1565.002 (Data Manipulation: Transmitted Data Manipulation)
- **Impact**: Traffic on the mesh network loses post-quantum protection
- **Tools**: Scapy, Wireshark, aireplay-ng, mesh-toolkit
- **Scenario**: Attacker manipulates mesh Wi-Fi control frames to mimic nodes not supporting PQC, causing secure TLS to be re-negotiated using only classical cipher suites.
- **Attack Steps**: Step 1: Use Wireshark to monitor mesh Wi-Fi control frames and discover node IDs that support PQC TLS during handshake.Step 2: Build a spoofed mesh control frame (with Scapy) that simulates a low-capability node not supporting PQC.Step 3: Send repeated spoofed frames to the target mesh client using aireplay-ng.Step 4: The client adjusts its TLS handshake preferences based on mesh topology information and retries using classical TLS (e.g., RSA-based handshake).Step 5: Capture the new handshake with Wireshark and confirm that PQC ciphers are missing.Step 6: Log session keys or credentials for potential quantum-cracking simulation.
- **Detection**: Monitor mesh control frame consistency and validate cipher suite changes
- **Solution**: Implement PQC-only mesh policies and signed control frame enforcement
- **Tags**: mesh, tls, downgrade, spoofing

## PQC VPN Tunnel Downgrade via Mobile Hotspot Manipulation

- **Attack Type**: Crypto Downgrade in VPN Initiation
- **Target**: Laptops or Phones with PQC-VPN Clients
- **Vulnerability**: VPN clients allow cipher suite fallback without warning
- **MITRE**: T1557.001 (Adversary-in-the-Middle: ARP Spoofing)
- **Impact**: VPN traffic believed to be PQC is exposed
- **Tools**: mitmproxy, dnsmasq, EvilAP, strongSwan
- **Scenario**: A user connecting through a mobile hotspot is intercepted using a rogue hotspot, which strips PQC capabilities from VPN negotiation (IPSec/IKEv2).
- **Attack Steps**: Step 1: Configure a rogue mobile hotspot using EvilAP broadcasting same SSID as user’s known network.Step 2: Use dnsmasq to reroute VPN endpoint resolution to a local fake gateway.Step 3: Initiate mitmproxy to modify IKEv2 negotiation messages, stripping PQC cipher proposals (e.g., CRYSTALS-Kyber).Step 4: Allow connection to complete using fallback classical ciphers like RSA or DH.Step 5: Log session keys and VPN configuration.Step 6: Replay session or simulate post-quantum cracking attempt.
- **Detection**: Log analysis of IKEv2 negotiation shows missing PQC algorithms
- **Solution**: Enforce strict PQC-only cipher suite in VPN client config
- **Tags**: vpn, pqc, ikev2, downgrade

## PQC Cipher Suite Downgrade in HTTP/3 over QUIC via AP Injection

- **Attack Type**: HTTP/3 Downgrade via Fake QUIC Negotiation
- **Target**: Modern Browsers Using HTTP/3 over Wi-Fi
- **Vulnerability**: Lack of QUIC parameter integrity check in early packets
- **MITRE**: T1565.003 (Data Manipulation: Stored Data Manipulation)
- **Impact**: HTTP/3 sessions become susceptible to post-quantum cracking
- **Tools**: Wireshark, mitmproxy, EvilAP, QUIC injector script
- **Scenario**: QUIC packets are intercepted in public Wi-Fi, and PQC cipher negotiation in HTTP/3 is altered using a rogue AP, leading to downgrade.
- **Attack Steps**: Step 1: Set up a rogue Wi-Fi AP (EvilAP) mimicking the public network.Step 2: Capture and analyze QUIC handshake (UDP/443) using Wireshark.Step 3: Inject a modified Initial QUIC packet with altered cipher suites using QUIC injector script (remove PQC proposals).Step 4: Client accepts modified handshake assuming PQC not supported.Step 5: Connection proceeds under classical TLS 1.3 without PQC layer.Step 6: Monitor encrypted traffic assuming it's quantum-safe when it is not.
- **Detection**: Monitor negotiated cipher suites and validate against expected PQC
- **Solution**: Enable signed QUIC negotiation and enforce PQC cipher preference
- **Tags**: http3, quic, downgrade, tls

## Post-Quantum Key Exchange Downgrade via SDR-Controlled Zigbee Hub

- **Attack Type**: Zigbee Hub Downgrade with Fake Capability Broadcast
- **Target**: Zigbee Home Automation Devices
- **Vulnerability**: No authentication of controller capability announcements
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Zigbee clients downgrade and become vulnerable
- **Tools**: KillerBee, SDR (HackRF), Scapy-radio
- **Scenario**: A rogue Zigbee controller emits modified beacon and capability announcements that simulate older devices lacking PQC support, triggering legacy keying.
- **Attack Steps**: Step 1: Use SDR or KillerBee to intercept Zigbee capability announcements.Step 2: Forge and emit new hub announcement frames that indicate no PQC support.Step 3: PQC-capable Zigbee clients connect assuming hub lacks support and initiate classical AES-based key exchange.Step 4: Capture full key exchange and session with Wireshark.Step 5: Demonstrate how false capability data causes fallback.Step 6: Replay attack in educational lab to demonstrate protocol weakness.
- **Detection**: Compare controller capability fields and network info hashes
- **Solution**: Enforce controller validation and PQC key negotiation constraints
- **Tags**: zigbee, hub, capability, downgrade

## BLE GATT Profile Downgrade in Post-Quantum Pairing

- **Attack Type**: BLE Profile Downgrade Attack via GATT Spoofing
- **Target**: PQC-enabled BLE Devices (Fitness Bands, etc.)
- **Vulnerability**: Device trusts first GATT profile it sees
- **MITRE**: T1477 (Bluetooth Discovery)
- **Impact**: Pairing done under legacy crypto; user misled
- **Tools**: BLEAH, btlejack, Scapy
- **Scenario**: A BLE client is tricked into establishing a secure channel using legacy AES instead of PQC-enhanced key exchange through spoofed GATT service advertisement.
- **Attack Steps**: Step 1: Scan nearby BLE devices for PQC GATT services using BLEAH.Step 2: Use btlejack to broadcast fake GATT profile indicating only legacy crypto support.Step 3: Client connects, unaware that the PQC profile is absent.Step 4: Pairing is completed using AES legacy pairing method.Step 5: Capture traffic and demonstrate loss of post-quantum strength.Step 6: Replay or analyze session to demonstrate downgrade success.
- **Detection**: Profile validation during pairing can detect mismatch
- **Solution**: Lock pairing to verified GATT profile UUIDs with PQC flags
- **Tags**: ble, gatt, spoof, pairing, downgrade

## EM Pulse Injection on Quantum Processor

- **Attack Type**: Wireless EM Pulse Fault Injection
- **Target**: Quantum Processor
- **Vulnerability**: Shield Leakage, Poor Isolation
- **MITRE**: T1603 (Hardware Fault Injection)
- **Impact**: Decoherence, Miscomputation
- **Tools**: EMP Generator, SDR Receiver, Shield Analyzer
- **Scenario**: An attacker uses high-frequency EM pulses to create computational faults in a quantum chip operating inside a Faraday cage with known weaknesses.
- **Attack Steps**: Step 1: Identify the target lab using a mobile EM signal scanner.Step 2: Use a spectrum analyzer to find weaknesses in the shielding.Step 3: Set up a portable EMP generator with directional EM emission.Step 4: Position it near the weak point in shielding.Step 5: Fire controlled pulses during quantum computation.Step 6: Record interference patterns and compare with control outputs to detect induced fault patterns.
- **Detection**: Quantum Error Logs, Spectrum Anomaly Detection
- **Solution**: Upgrade shielding, monitor for EM activity, use tamper alarms
- **Tags**: #Quantum #EMP #WirelessInjection #FaultInjection

## RF Signal Injection into Cryogenic Control Lines

- **Attack Type**: RF Fault Injection
- **Target**: Cryogenic Qubit System
- **Vulnerability**: Exposed RF Control Lines
- **MITRE**: T0812 (Signal Interference)
- **Impact**: Quantum decoherence, silent errors
- **Tools**: HackRF One, Directional Antenna, Oscilloscope
- **Scenario**: Exploiting weakly shielded RF lines leading into the cryostat of a superconducting quantum system to disrupt qubit states.
- **Attack Steps**: Step 1: Locate the lab housing the quantum cryostat.Step 2: Use a directional antenna and SDR to locate exposed RF control lines (e.g., I/O ports not fully shielded).Step 3: Use HackRF to craft low-noise RF signals matching control frequencies.Step 4: Inject these signals into the exposed lines intermittently.Step 5: Monitor computation output for bit flip anomalies.Step 6: Use oscilloscope to verify waveform distortion inside the line.
- **Detection**: RF waveform analysis, signal integrity checks
- **Solution**: Hardened RF cabling, shielding, internal signal validation
- **Tags**: #Cryostat #QubitFault #RFInjection #WirelessAttack

## Bluetooth Fault Induction in Quantum Device Monitor

- **Attack Type**: Wireless Protocol Abuse
- **Target**: Qubit Monitoring System
- **Vulnerability**: Debug Port Exposure, Unencrypted Bluetooth
- **MITRE**: T0807 (Wireless Exploitation)
- **Impact**: False monitoring data, leading to QPU damage
- **Tools**: Bluetooth Sniffer (Ubertooth), Bluetooth Jammer, Laptop
- **Scenario**: Exploiting Bluetooth debug interfaces left active on quantum monitoring systems to remotely cause faults.
- **Attack Steps**: Step 1: Scan for Bluetooth signals from quantum monitoring hardware.Step 2: Use Ubertooth to identify debug channels and paired devices.Step 3: Jam active Bluetooth signals causing packet loss.Step 4: If debug port exposed, inject malformed control packets.Step 5: Observe crash or misreporting in temperature/current logs used by qubit controller.Step 6: Record fault logs and validate against normal behavior.
- **Detection**: Monitoring interface audit, Bluetooth traffic log
- **Solution**: Disable Bluetooth interfaces, whitelist MACs, isolate via firewall
- **Tags**: #Bluetooth #QubitMonitor #DebugExploitation

## Wi-Fi Interference in Quantum Timing Circuits

- **Attack Type**: Wi-Fi Interference Fault Injection
- **Target**: Quantum Clocking Subsystem
- **Vulnerability**: Unprotected Wireless Sync
- **MITRE**: T1599.001 (Network Denial of Service)
- **Impact**: Gate timing issues, invalid quantum operations
- **Tools**: Wi-Fi Jammer, Deauther, Signal Analyzer
- **Scenario**: A quantum timing sync device using internal Wi-Fi is jammed to create timing faults in quantum gate operation.
- **Attack Steps**: Step 1: Identify target device using Wi-Fi signals (SSID fingerprinting).Step 2: Use Wireshark or Kismet to analyze timing packets.Step 3: Deploy a Wi-Fi jammer near the quantum timing device.Step 4: Use a deauthentication flood to force frequent resyncs.Step 5: Monitor for quantum gate desync or timing jitter.Step 6: Log outcomes and compare to standard cycle outputs.
- **Detection**: Packet loss, high jitter in sync logs
- **Solution**: Switch to wired or secure quantum time sync protocol
- **Tags**: #WiFi #TimingAttack #QuantumDesync #WirelessDOS

## SDR-Based Clock Glitching in Wireless-Controlled Qubit System

- **Attack Type**: SDR Clock Glitch Injection
- **Target**: Wireless FPGA Control Module
- **Vulnerability**: Wireless Timing Control, SDR Spoofing
- **MITRE**: T0832 (Timing-Based Side Channel)
- **Impact**: Incorrect gate operations, qubit errors
- **Tools**: BladeRF, Signal Generator, Clock Analyzer
- **Scenario**: A wireless-controlled FPGA interface for a quantum setup is subjected to SDR-based clock glitching to cause miscomputation.
- **Attack Steps**: Step 1: Identify wireless control link via SDR scan.Step 2: Determine control frequency and waveform pattern.Step 3: Use BladeRF to inject brief timing glitches into the RF signal.Step 4: Observe unexpected behavior in FPGA-driven control of qubit pulses.Step 5: Log deviations in gate duration and outcomes.Step 6: Correlate injected glitch patterns with logic errors on output.
- **Detection**: Clock jitter monitoring, FPGA output checks
- **Solution**: Harden control protocols, RF shielding, glitch detectors
- **Tags**: #SDR #ClockGlitch #FPGAInjection #QuantumFault

## Directed Acoustic Injection on Quantum Chip

- **Attack Type**: Ultrasonic Fault Injection
- **Target**: Superconducting Quantum Chip
- **Vulnerability**: Acoustic Vibration Sensitivity
- **MITRE**: T1603.003 (Acoustic Fault Injection)
- **Impact**: Qubit instability, calculation failure
- **Tools**: Ultrasonic Transducer, Laser Vibrometer, Thermal Camera
- **Scenario**: A high-frequency directional speaker is used to emit ultrasonic waves targeting a quantum processor's cooling assembly, inducing vibrations that impact qubit coherence.
- **Attack Steps**: Step 1: Identify lab window or vent access points where acoustic leakage is possible.Step 2: Place a directional ultrasonic transducer aligned toward the target device.Step 3: Calibrate the frequency between 20–40 kHz (beyond human hearing).Step 4: Begin low-level pulses to identify resonant frequencies that cause vibration.Step 5: Use a laser vibrometer to confirm vibrations at the cryogenic interface.Step 6: Intensify pulses during critical quantum operations to induce decoherence.Step 7: Observe and record gate error patterns.
- **Detection**: Thermal fluctuation logs, vibration detection
- **Solution**: Acoustic insulation, vibration monitoring
- **Tags**: #AcousticAttack #QuantumChip #FaultInjection

## Near-Field RF Fault Injection through Lab Wall

- **Attack Type**: Near-Field Electromagnetic Fault Injection
- **Target**: Shielded Quantum Chamber
- **Vulnerability**: Poor near-field EM shielding
- **MITRE**: T0831 (Electromagnetic Interference)
- **Impact**: Controlled computation disruption
- **Tools**: RF Injection Coil, SDR Controller, Wall Scanner
- **Scenario**: Attacker places a concealed RF injection antenna near a wall adjacent to the quantum hardware to introduce EM faults in short bursts.
- **Attack Steps**: Step 1: Survey the environment to identify wall areas closest to quantum processing unit.Step 2: Use a wall scanner to locate power lines or conduits acting as waveguides.Step 3: Embed a compact RF coil on the wall with directional shielding.Step 4: Use SDR to generate high-frequency bursts at 500 MHz to 1.5 GHz.Step 5: Synchronize bursts with known quantum task intervals (if known).Step 6: Log induced qubit faults and measure wall EM leakage post-attack.
- **Detection**: EM field monitors, RF noise detectors
- **Solution**: EM dampening paint, wall shielding
- **Tags**: #NearField #QuantumFault #EMInjection

## Infrared Control Signal Injection on Qubit Interface

- **Attack Type**: Infrared Signal Fault Injection
- **Target**: Ion Trap Processor
- **Vulnerability**: Optical Line Exposure
- **MITRE**: T1203 (IR Optical Interface Abuse)
- **Impact**: Misentanglement, state transition errors
- **Tools**: IR LED Array, Signal Modulator, IR Camera
- **Scenario**: Attacker targets IR-based optical interfaces used in controlling ion trap quantum processors to disrupt state preparation.
- **Attack Steps**: Step 1: Identify whether the target device uses IR interfaces via technical documentation or external sensors.Step 2: Set up a high-power IR LED array with narrow focus.Step 3: Use a modulator to mimic or interfere with control pulses.Step 4: Direct the beam through a glass panel or opening near the quantum device.Step 5: Gradually introduce out-of-phase IR pulses to disrupt entanglement.Step 6: Capture behavior changes on ion state logs and photon detection graphs.
- **Detection**: Qubit control logs, IR heat map
- **Solution**: Optical isolators, disable unused IR ports
- **Tags**: #IRInjection #OpticalFaults #QuantumControl

## Microwave Flooding on Quantum Memory Module

- **Attack Type**: Microwave Saturation Fault
- **Target**: Quantum Memory Module
- **Vulnerability**: EM Susceptibility at Microwave Band
- **MITRE**: T1603.001 (Microwave Interference)
- **Impact**: Memory corruption, instability
- **Tools**: Microwave Generator, Parabolic Reflector, EM Shield Tester
- **Scenario**: Using a microwave generator, attacker floods the lab with EM in the GHz range, disrupting coherence in quantum memory operations.
- **Attack Steps**: Step 1: Survey lab area to locate air vents or window slits where microwave energy may penetrate.Step 2: Deploy a parabolic reflector dish to focus the microwave beam.Step 3: Use spectrum scanner to detect quantum memory control bands.Step 4: Flood the area with GHz range signals (e.g., 2.4 GHz, 5.8 GHz).Step 5: Monitor impact via spike in error correction frequency or bit flip rates.Step 6: Shut down flooding and measure post-attack recovery.
- **Detection**: EM spectrum analysis, ECC spike detection
- **Solution**: Use waveguides, microwave-blocking enclosures
- **Tags**: #MicrowaveAttack #QuantumMemory #RFInjection

## SDR Spoofing of Quantum Key Distribution Receiver

- **Attack Type**: Wireless Protocol Spoofing
- **Target**: QKD Receiver Interface
- **Vulnerability**: Unauthenticated Classical Channel
- **MITRE**: T1603.002 (Protocol Spoofing)
- **Impact**: Compromised quantum key
- **Tools**: HackRF, QKD Protocol Analyzer, Decryption Monitor
- **Scenario**: An attacker mimics the behavior of a QKD receiver using SDR to inject corrupted key negotiation packets into the quantum channel’s classical side.
- **Attack Steps**: Step 1: Monitor the classical communication channel between quantum sender (Alice) and receiver (Bob).Step 2: Use SDR to mimic the receiver's handshake response.Step 3: Interleave false responses during QKD key exchange negotiation.Step 4: Log acceptance of corrupted or partial key.Step 5: Trigger failure in final key validation phase.Step 6: Measure key bit integrity and error threshold anomalies.
- **Detection**: Key validation logs, authentication mismatch
- **Solution**: Secure QKD stack, out-of-band key confirmation
- **Tags**: #QKD #ProtocolInjection #KeyTampering

## EMI Spike on Dilution Refrigerator Controller

- **Attack Type**: EMI Fault Injection
- **Target**: Cryogenic Cooling System
- **Vulnerability**: Power Line EMI Path
- **MITRE**: T0861 (Hardware Fault Injection)
- **Impact**: Loss of quantum coherence
- **Tools**: EMI Emitter, Cryo Sensor, Signal Logger
- **Scenario**: The dilution refrigerator used to cool quantum hardware is targeted using high-energy EMI bursts to cause thermal anomalies.
- **Attack Steps**: Step 1: Locate external power lines or conduits connected to cryo-controller.Step 2: Attach clamp-style EMI injector on the line (simulated via shield breach).Step 3: Emit short, intense EMI pulses during cooling operations.Step 4: Monitor controller logs for temperature fluctuation or reboot events.Step 5: Track qubit error correlation with temperature changes.Step 6: Compare thermal maps before/after injection.
- **Detection**: Thermal log deviation, voltage dips
- **Solution**: EMI filters, backup cooling logic
- **Tags**: #CryoEMI #ThermalFault #QuantumDisruption

## RF Desynchronization of Quantum Clock Signals

- **Attack Type**: RF Desync Fault
- **Target**: Quantum Control Board
- **Vulnerability**: External Clock Injection
- **MITRE**: T1603 (Hardware Timing Fault)
- **Impact**: Faulty operations, wrong gate outputs
- **Tools**: RF Generator, Clock Analyzer, SDR
- **Scenario**: Using a timed RF interference pulse, attacker desynchronizes clock signals used in driving universal quantum gates.
- **Attack Steps**: Step 1: Identify the master clock system’s RF-driven control signal frequency.Step 2: Use an RF generator to emit timed bursts slightly offset from original frequency.Step 3: Introduce pulses during qubit gate initiation.Step 4: Record gate malfunction patterns or failure in superposition stability.Step 5: Repeat with varying amplitudes to identify thresholds.Step 6: Review synchronization logs for jitter or lag.
- **Detection**: Clock cycle analysis, time drift detection
- **Solution**: Clock hardening, PLL-based sync recovery
- **Tags**: #DesyncAttack #QuantumTiming #GateDisruption

## SDR-Based Sideband Attack on Quantum Transducer

- **Attack Type**: Sideband Injection Attack
- **Target**: Quantum Transducer
- **Vulnerability**: Signal Conversion Weakness
- **MITRE**: T1202 (Radio Frequency Sideband Attack)
- **Impact**: Bit loss during conversion
- **Tools**: BladeRF, Signal Analyzer, Waveform Editor
- **Scenario**: A sideband RF attack is launched against transducers that convert between electrical and optical signals for quantum hardware.
- **Attack Steps**: Step 1: Determine frequency band used by transducer for signal conversion.Step 2: Use BladeRF to generate sideband noise in adjacent frequencies.Step 3: Inject noise during signal conversion window.Step 4: Observe quantum state conversion failure or signal corruption.Step 5: Track bit integrity loss and spectrum anomalies.Step 6: Re-run conversion with noise off to confirm impact.
- **Detection**: Spectrum overlap detection
- **Solution**: Use bandpass filters, isolate transducer
- **Tags**: #SidebandAttack #TransducerFault #QubitControl

## Remote Laser Fault Injection via Line-of-Sight Port

- **Attack Type**: Optical Laser Fault Injection
- **Target**: Quantum Chamber
- **Vulnerability**: Optical Panel Exposure
- **MITRE**: T1203.001 (Optical Injection)
- **Impact**: Momentary decoherence
- **Tools**: Infrared Laser, Tripod Mount, Light Sensor
- **Scenario**: A quantum device with line-of-sight optical diagnostics is exposed to a brief laser pulse to introduce fault at a key moment.
- **Attack Steps**: Step 1: Locate vent, window, or diagnostic glass panel on quantum chamber.Step 2: Use a precise IR laser with narrow beam.Step 3: Time the pulse during quantum gate setup (based on leaked schedule).Step 4: Emit a sub-second pulse through the panel.Step 5: Observe fluctuations in qubit activity or coherence logs.Step 6: Confirm by repeating and observing consistent fault.
- **Detection**: Gate log analysis, IR detection sensors
- **Solution**: IR pulse blockers, panel blackout films
- **Tags**: #LaserAttack #IRInjection #QuantumOptics

## RFID Interference on Smart Access to Quantum Lab

- **Attack Type**: Wireless Physical Fault Vector
- **Target**: Smart Access System
- **Vulnerability**: RFID Jamming Susceptibility
- **MITRE**: T1600.001 (Access Disruption)
- **Impact**: Delayed response to quantum fault
- **Tools**: RFID Jammer, Access Control Logger
- **Scenario**: Indirectly targets quantum lab via RFID jamming of smart access points to lock out monitoring staff during critical computation.
- **Attack Steps**: Step 1: Identify RFID badge system frequency (usually 125kHz or 13.56MHz).Step 2: Deploy RFID jammer outside the lab perimeter.Step 3: Initiate jamming to prevent access during critical quantum operation windows.Step 4: Observe monitoring delays or inability to react to quantum computation issues.Step 5: Confirm by reviewing access logs and computation output timing.Step 6: Validate by controlled lab simulation.
- **Detection**: Access logs, user lockout events
- **Solution**: Upgrade RFID to NFC with jamming resistance
- **Tags**: #RFIDJamming #LabAccess #TimingDisruption

## Thermal Fault Injection via Infrared Heat Beaming

- **Attack Type**: Directed Thermal Fault
- **Target**: Quantum Processor & Controller
- **Vulnerability**: Poor thermal shielding, open lab ports
- **MITRE**: T0861 (Thermal Fault Injection)
- **Impact**: Miscomputation due to heating
- **Tools**: IR Heat Lamp, Thermal Camera, Laser Pointer for Alignment
- **Scenario**: Attacker uses a focused IR heat beam to cause localized heating on a quantum chip’s packaging or its control circuitry, inducing decoherence or logic faults.
- **Attack Steps**: Step 1: Conduct external reconnaissance to find a vent, opening, or thin-glass area where IR can enter the quantum lab.Step 2: Position an IR heat lamp on a tripod aligned via a laser pointer to ensure precision.Step 3: Use a thermal camera to confirm that heat is reaching the target area (typically on control electronics).Step 4: Activate the IR lamp to gradually raise the surface temperature by ~10–20°C.Step 5: Monitor logs from qubit control modules or coherence data for thermal drift errors.Step 6: Shut down the lamp and measure recovery time and fault duration.Step 7: Simulate multiple timings to identify vulnerability windows (e.g., during quantum gate initialization).
- **Detection**: Temperature logs, coherence dip graphs
- **Solution**: Thermal shielding, active IR detection
- **Tags**: #ThermalAttack #IRInjection #QuantumFault

## Low-Power EMP Injection via Compromised IoT Device

- **Attack Type**: Electromagnetic Pulse Injection
- **Target**: Quantum Device Controller
- **Vulnerability**: Internal hardware compromise
- **MITRE**: T0806 (Compromise of Peripheral Device)
- **Impact**: Random decoherence or logic error
- **Tools**: Modified IoT Camera, Small EMP Coil, Microcontroller (Arduino)
- **Scenario**: An IoT device (e.g., smart camera) inside the quantum lab is modified to emit low-power EMP pulses to interfere with quantum control electronics.
- **Attack Steps**: Step 1: Introduce a tampered IoT camera inside the lab (or simulate it in lab environment).Step 2: Connect a small EMP coil to the camera's internal microcontroller.Step 3: Program the coil to emit a brief pulse (1–5 ms) every few minutes.Step 4: During simulation, position the coil near quantum device control circuitry.Step 5: Observe resulting errors in gate sequencing or timing irregularities.Step 6: Log faults and correlate them with coil activation timestamps.Step 7: Gradually increase frequency or pulse strength to test error thresholds.
- **Detection**: Hardware health monitor, EMP sensor
- **Solution**: Physical security, disable non-critical IoT
- **Tags**: #EMPInjection #IoTThreat #HardwareAttack

## Acoustic Resonance Fault on Cryogenic Pump

- **Attack Type**: Sonic Resonance Injection
- **Target**: Cryogenic Subsystem
- **Vulnerability**: Acoustic coupling to vibration-sensitive pump
- **MITRE**: T1603.003 (Mechanical Injection)
- **Impact**: Reduced cooling efficiency, decoherence
- **Tools**: Function Generator, Directional Subwoofer, Microphone Array
- **Scenario**: Using a directional speaker, attacker emits a tone that matches the mechanical resonance of the lab's cryogenic pump, causing vibration faults that alter quantum system cooling.
- **Attack Steps**: Step 1: Identify the model of the cryogenic pump used (simulate or mock in lab).Step 2: Research its mechanical resonance frequency (typically 30–200 Hz).Step 3: Use a function generator and subwoofer to emit a gradually sweeping tone toward the lab wall or floor.Step 4: Monitor vibration using a microphone array or accelerometer near the pump.Step 5: Identify frequency that causes maximum vibration.Step 6: Sustain this tone during quantum computation to reduce cooling efficiency.Step 7: Review logs of qubit decoherence, thermal drift, and error rate spike.
- **Detection**: Cryo pump logs, thermal drift stats
- **Solution**: Soundproofing, vibration dampening
- **Tags**: #SonicAttack #VibrationInjection #CryoDisruption

## SDR-Based Interference on Optical Clock Sync

- **Attack Type**: Optical Protocol Distortion
- **Target**: Optical Sync Module
- **Vulnerability**: Weak filtering on optical-electrical interface
- **MITRE**: T1599.002 (Clock Fault Injection)
- **Impact**: Gate misalignment, invalid calculations
- **Tools**: SDR (e.g., HackRF), Spectrum Analyzer, Pulse Generator
- **Scenario**: An attacker uses a software-defined radio to inject noise into the frequency band used for optical clock synchronization, affecting gate timing.
- **Attack Steps**: Step 1: Identify optical sync system used (usually low-power laser pulses for clock).Step 2: Identify the classical band frequency used for synchronization (e.g., MHz-GHz range).Step 3: Configure SDR to emit weak noise near those frequencies, modulated with random pulses.Step 4: Begin injection during active quantum gate operations.Step 5: Monitor clock signal logs for drift, missed ticks, or cycle resets.Step 6: Confirm fault by repeating pattern and observing errors in quantum computation logs.Step 7: Gradually increase the interference power to test fail-safe threshold.
- **Detection**: Optical clock jitter tracking, sync error logs
- **Solution**: Stronger clock filters, error correction loops
- **Tags**: #ClockInjection #OpticalSync #SDRInjection

## Inductive Coupling Attack via External Coil

- **Attack Type**: Magnetic Induction Fault
- **Target**: External Power-Coupled Lab Infrastructure
- **Vulnerability**: Magnetic field propagation via structure
- **MITRE**: T0808 (Magnetic Fault Injection)
- **Impact**: Quantum gate errors, decoherence
- **Tools**: Induction Coil (e.g., copper loop), Power Amplifier, Gaussmeter
- **Scenario**: A high-current external coil is placed near power lines or metallic infrastructure connected to the lab to inject magnetic fields causing computation errors.
- **Attack Steps**: Step 1: Identify power lines, ventilation ducts, or metal beams entering the lab that act as unintended antennas.Step 2: Wind a large copper induction coil and connect to an amplifier to generate a magnetic field.Step 3: Place coil against wall or ground near suspected coupling point.Step 4: Inject a 50–200 Hz magnetic field for several seconds.Step 5: Use Gaussmeter to measure induced magnetic fields near lab entry points.Step 6: Log quantum gate or state initialization faults.Step 7: Simulate different frequencies and duty cycles to evaluate impact.
- **Detection**: Magnetic field logs, operation mismatch
- **Solution**: Ground shielding, magnetic field suppression
- **Tags**: #MagneticInjection #InductiveFault #QuantumLab

## EM Side-Channel Leakage of QRNG via SDR

- **Attack Type**: Wireless (SDR RF Emission Capture)
- **Target**: QRNG Modules
- **Vulnerability**: EM Leakage
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Predictable randomness
- **Tools**: HackRF, GNURadio, Faraday Bag, QRNG simulator
- **Scenario**: An attacker uses a Software Defined Radio (SDR) to capture electromagnetic radiation from a quantum random number generator module to reconstruct its output.
- **Attack Steps**: Step 1: Set up the QRNG module (e.g., ID Quantique QRNG chip) in a Faraday-isolated test environment. Step 2: Place a HackRF device 1-3 meters away to capture RF emissions. Step 3: Use GNURadio to filter and extract side-channel patterns. Step 4: Analyze waveform correlation between QRNG outputs and captured emissions. Step 5: Reconstruct probable random bit patterns using known signal models. Step 6: Demonstrate repeatability and entropy reduction.
- **Detection**: Anomaly in entropy pool; Side-channel RF signal spikes
- **Solution**: Use TEMPEST shielding; add active noise masking to QRNGs
- **Tags**: qrng, sdr, side-channel, wireless

## QRNG Interference via Intentional RF Injection

- **Attack Type**: Wireless (RF Injection)
- **Target**: QRNG Devices
- **Vulnerability**: RF Susceptibility
- **MITRE**: T0807 (Radio Signal Interference)
- **Impact**: Weak random number generation
- **Tools**: RF Signal Generator, Laser QRNG, SDR, Shielded Room
- **Scenario**: An attacker nearby introduces targeted radio interference to affect the photonic components of a QRNG system, degrading entropy.
- **Attack Steps**: Step 1: Set up a laser-based QRNG (e.g., beam-splitter based) in a lab. Step 2: Place an RF signal generator tuned to interfere with the QRNG’s power or control line harmonics. Step 3: Begin injecting RF noise bursts during QRNG operation. Step 4: Monitor entropy pool using diagnostic APIs. Step 5: Collect and compare statistical bias before and after interference. Step 6: Validate entropy degradation through NIST SP800-90 tests.
- **Detection**: Deviation in entropy tests
- **Solution**: Harden circuits, apply RF shielding, add randomness auditing
- **Tags**: rf-injection, qrng, entropy

## QRNG Spoofing via Bluetooth Device Sensor Injection

- **Attack Type**: Wireless (Bluetooth Low Energy Injection)
- **Target**: IoT/Embedded QRNGs
- **Vulnerability**: Insecure entropy input path
- **MITRE**: T1557.001 (Bluetooth Device Impersonation)
- **Impact**: Cryptographic key compromise
- **Tools**: nRF52 Dongle, Custom BLE firmware, Entropy harvesting chip
- **Scenario**: A compromised BLE device sends fake entropy readings to the quantum RNG subsystem in an IoT device to inject low-entropy or precomputed randomness.
- **Attack Steps**: Step 1: Identify target IoT device that uses BLE-connected QRNG entropy sensors. Step 2: Flash nRF52 dongle with custom BLE firmware mimicking sensor characteristics. Step 3: Initiate spoof pairing with QRNG host system. Step 4: Begin transmitting precomputed entropy values over BLE. Step 5: Observe if QRNG module accepts and uses spoofed data. Step 6: Attempt weak key generation using poisoned entropy.
- **Detection**: Monitor entropy source changes; audit BLE connections
- **Solution**: Validate BLE sensor IDs; use secure QRNG sourcing
- **Tags**: qrng, ble, spoofing

## Exploiting QRNG via Wi-Fi-Induced Thermal Variance

- **Attack Type**: Wireless (Wi-Fi Interference)
- **Target**: Consumer QRNG
- **Vulnerability**: Thermo-optical Instability
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Degraded randomness from environmental effects
- **Tools**: Wi-Fi router (802.11ac), Thermal camera, QRNG device
- **Scenario**: Repeated Wi-Fi bursts are used to induce thermal changes in a quantum hardware RNG, influencing the optical components used for randomness.
- **Attack Steps**: Step 1: Set up the QRNG in a closed environment with external thermal monitoring. Step 2: Place Wi-Fi router close to the device; repeatedly transmit large packets (e.g., video stream). Step 3: Use thermal camera to observe temperature fluctuations on QRNG hardware. Step 4: Log entropy degradation during thermal stress events. Step 5: Correlate QRNG bias with Wi-Fi activity levels. Step 6: Demonstrate entropy reduction and predictability.
- **Detection**: NIST Entropy Test Failures
- **Solution**: Use temperature-controlled enclosures and monitoring
- **Tags**: thermal, wifi, qrng

## QRNG Electromagnetic Jamming via NFC

- **Attack Type**: Wireless (NFC/EM Interference)
- **Target**: QRNG-embedded Smart Tokens
- **Vulnerability**: NFC susceptibility
- **MITRE**: T1421 (Hardware Tampering)
- **Impact**: Weak cryptographic keys
- **Tools**: NFC Signal Injector, Smart Card Reader with QRNG, EM analyzer
- **Scenario**: A malicious NFC emitter is used to inject high-frequency fields into a consumer QRNG embedded in a smart card reader, causing bias or instability.
- **Attack Steps**: Step 1: Set up the smart card reader with built-in QRNG (e.g., hardware token). Step 2: Build a looped NFC signal injector using Arduino/NFC shield. Step 3: Place injector in close proximity to smart card reader. Step 4: Transmit strong NFC signals at various modulated frequencies. Step 5: Observe impact on QRNG behavior using entropy audit tools. Step 6: Attempt to reproduce low-entropy output or repeat values.
- **Detection**: Anomalous NFC activity; entropy warnings
- **Solution**: Shield NFC reader; verify QRNG health at runtime
- **Tags**: nfc, qrng, smartcard, interference

## Passive Wi-Fi Packet Reflection to Corrupt QRNG Optical Paths

- **Attack Type**: Wireless (Passive Interference)
- **Target**: Optical QRNG
- **Vulnerability**: Environmental interference
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Noise in randomness signal
- **Tools**: Wi-Fi AP, Reflective Foil Sheets, Beam-splitter QRNG
- **Scenario**: Wi-Fi signal reflections in lab environments introduce subtle noise into the optical beam-splitters used by quantum random number generators.
- **Attack Steps**: Step 1: Set up a QRNG with an optical beam splitter in a controlled room. Step 2: Add reflective foil or mirrored surfaces around the QRNG. Step 3: Use a nearby Wi-Fi router to generate heavy 802.11ac traffic. Step 4: Monitor entropy levels during peak traffic hours. Step 5: Use network signal analyzers to map standing wave zones. Step 6: Detect if optical jitter increases in correlation with Wi-Fi reflections.
- **Detection**: Deviations in QRNG entropy plot
- **Solution**: Minimize reflections, use enclosed light paths
- **Tags**: wifi, optics, qrng, noise

## RF Proximity Amplification to Access Internal QRNG Debug Interfaces

- **Attack Type**: Wireless (RF Field Amplification)
- **Target**: Evaluation QRNGs
- **Vulnerability**: RF-triggered debug paths
- **MITRE**: T1409 (Signal Spoofing)
- **Impact**: Internal RNG bypass
- **Tools**: RF Amplifier, SDR, QRNG evaluation board
- **Scenario**: Attackers boost RF signals near a QRNG device to activate internal debugging interfaces meant only for testing purposes.
- **Attack Steps**: Step 1: Obtain QRNG development kit with exposed debug interfaces (e.g., SPI, I2C). Step 2: Use an RF amplifier to generate strong field around the device. Step 3: Slowly modulate the RF power to probe state transitions. Step 4: SDR captures electromagnetic responses from QRNG. Step 5: Use frequency sweeps to identify debug port activation patterns. Step 6: Log unintended data leakage or entropy bypasses.
- **Detection**: Unusual debug interface response
- **Solution**: Block debug ports, RF shielding
- **Tags**: debug, rf, qrng, devboard

## QRNG Bitstream Prediction via Wi-Fi Clock Drift Injection

- **Attack Type**: Wireless (Clock Skew Induction)
- **Target**: QRNG-on-Chip
- **Vulnerability**: Clock instability
- **MITRE**: T1495 (Data Corruption)
- **Impact**: Predictable entropy intervals
- **Tools**: Wi-Fi Device, Oscilloscope, Entropy Logger
- **Scenario**: Repetitive wireless transmissions cause induced thermal shifts in oscillator clocks affecting the randomness generation rate of a QRNG.
- **Attack Steps**: Step 1: Connect a QRNG chip to a high-precision entropy logger. Step 2: Place a Wi-Fi router close to the chip and transmit video streams continuously. Step 3: Monitor chip clock via oscilloscope for drift patterns. Step 4: Correlate clock skew with entropy anomalies. Step 5: Repeat under controlled temperature variation to confirm influence. Step 6: Attempt to reconstruct parts of the QRNG output from skewed intervals.
- **Detection**: Drift detection in oscillator clock
- **Solution**: Use temperature-compensated oscillators
- **Tags**: wifi, clock, qrng

## QRNG Entropy Injection via Fake Wireless Entropy Beacon

- **Attack Type**: Wireless (Spoofed Wireless Entropy Broadcast)
- **Target**: IoT Entropy Consumers
- **Vulnerability**: Trust in external entropy
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Biased or injected entropy
- **Tools**: ESP32, Custom Firmware, QRNG-using IoT system
- **Scenario**: A fake wireless beacon broadcasts high-entropy looking data to confuse or inject data into systems that source entropy from nearby wireless sensors.
- **Attack Steps**: Step 1: Create a Wi-Fi access point with an ESP32 broadcasting fake entropy packets. Step 2: Configure packets to simulate real entropy beacons used by IoT devices. Step 3: Place this near a target system sourcing entropy from environmental beacons. Step 4: Monitor if entropy data is logged or used by the QRNG-based system. Step 5: Attempt multiple pattern injections to skew randomness. Step 6: Validate outcome by key predictability testing.
- **Detection**: Beacon fingerprint mismatch
- **Solution**: Validate entropy sources
- **Tags**: wireless, spoof, entropy

## Bluetooth Denial-of-Service Causing QRNG Fallback to Weak PRNG

- **Attack Type**: Wireless (Bluetooth DoS)
- **Target**: Mobile or Wearable QRNGs
- **Vulnerability**: No error handling in entropy failure
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Switch to weak PRNG source
- **Tools**: BLE Flooder (nRF Sniffer), Smartphone QRNG app
- **Scenario**: An attacker floods Bluetooth channels to force a device’s QRNG entropy path offline, causing fallback to weaker pseudorandom number generators.
- **Attack Steps**: Step 1: Identify a device that uses BLE-linked QRNG entropy sensors. Step 2: Set up BLE flooder tool (e.g., nRF Sniffer with flooding firmware). Step 3: Continuously spam BLE advertisement channels near the device. Step 4: Monitor device logs to detect fallback or errors in entropy collection. Step 5: Confirm if fallback PRNG is used. Step 6: Use output logs to measure entropy quality.
- **Detection**: Logs showing fallback; entropy drop
- **Solution**: Harden BLE stack; block entropy fallback
- **Tags**: qrng, dos, ble

## Spoofed Quantum Entropy Packets Over Zigbee in Mesh Networks

- **Attack Type**: Wireless (Zigbee Protocol Abuse)
- **Target**: Sensor Networks
- **Vulnerability**: Unauthenticated entropy exchange
- **MITRE**: T1557.003 (Protocol Impersonation)
- **Impact**: Predictable keys in sensor mesh
- **Tools**: Zigbee dongle, Custom Firmware, QRNG-integrated Mesh Nodes
- **Scenario**: A spoofed Zigbee node in a mesh network feeds fake entropy packets into a QRNG-based encryption scheme used for secure sensor communication.
- **Attack Steps**: Step 1: Identify mesh network where nodes share entropy via Zigbee. Step 2: Build a fake Zigbee node using a dongle and firmware mimicking a trusted peer. Step 3: Inject entropy packets with predictable values. Step 4: Observe packet acceptance and key derivation failures. Step 5: Analyze encryption keys generated during attack. Step 6: Reproduce attack under different key exchanges.
- **Detection**: Entropy outliers in logs
- **Solution**: Use signed entropy exchanges
- **Tags**: zigbee, spoof, qrng

## QRNG Timing Skew via Proximity-Based Inductive Charging

- **Attack Type**: Wireless (Inductive Power Noise)
- **Target**: QRNG-Integrated Devices
- **Vulnerability**: Power fluctuation influence
- **MITRE**: T1496 (Resource Hijacking)
- **Impact**: Faulty or biased entropy
- **Tools**: Qi Charger, Oscilloscope, QRNG-enabled IoT Board
- **Scenario**: A wireless charging pad placed under the QRNG hardware subtly shifts internal voltage rails, creating entropy skew.
- **Attack Steps**: Step 1: Connect a QRNG-enabled IoT board powered over USB. Step 2: Place a Qi wireless charger beneath the board. Step 3: Begin inductive charging and monitor system voltage using oscilloscope. Step 4: Observe fluctuations during charge cycles. Step 5: Analyze QRNG output before and during induced shifts. Step 6: Record statistical entropy changes.
- **Detection**: Voltage rail noise patterns
- **Solution**: Shield from EM charging pads
- **Tags**: qrng, inductive, power

## Side-Channel Exploitation via Wi-Fi Audio Intermodulation

- **Attack Type**: Wireless (Audio Intermodulation)
- **Target**: Photonic QRNG
- **Vulnerability**: Mixed-signal noise
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Subtle degradation of entropy
- **Tools**: Audio Generator, Wi-Fi Router, QRNG Device
- **Scenario**: Wi-Fi and nearby sound sources produce intermodulated noise that may interfere with photodetectors used in QRNG.
- **Attack Steps**: Step 1: Set up QRNG system using optical photon detectors. Step 2: Place a Wi-Fi router and a high-frequency speaker near device. Step 3: Play tones that overlap with RF harmonics. Step 4: Measure photodetector jitter using oscilloscope. Step 5: Log entropy and jitter correlation during audio bursts. Step 6: Simulate bias and verify with randomness tests.
- **Detection**: Signal cross-pattern detection
- **Solution**: Isolate QRNG from audio sources
- **Tags**: audio, qrng, intermodulation

## QRNG Entropy Leak via Unintentional RF Backscatter

- **Attack Type**: Wireless (RF Backscatter Analysis)
- **Target**: QRNG Lab System
- **Vulnerability**: Backscatter EM leakage
- **MITRE**: T1592 (Compromise of Hardware Supply Chain)
- **Impact**: Partial QRNG state reconstruction
- **Tools**: HackRF, EM Reflector Panels, Spectrum Analyzer
- **Scenario**: QRNG’s internal operations leak information due to reflective EM waves bouncing off internal shielding surfaces.
- **Attack Steps**: Step 1: Place QRNG in semi-open EM-reflective enclosure. Step 2: Set up HackRF to capture reflected emissions. Step 3: Use spectrum analyzer to pinpoint modulated signal patterns. Step 4: Correlate signal variance with known entropy outputs. Step 5: Attempt reverse-engineering of entropy states. Step 6: Validate using entropy reconstruction attempts.
- **Detection**: EM pattern leak signatures
- **Solution**: EM-safe shielding design
- **Tags**: rf, leak, qrng

## QRNG Attack via Sub-Carrier Injection over FM Radio Bands

- **Attack Type**: Wireless (FM Sub-Carrier Abuse)
- **Target**: QRNG Systems
- **Vulnerability**: Wireless band overlap
- **MITRE**: T1430 (Transmit Malicious Signals)
- **Impact**: Distorted random numbers
- **Tools**: FM Transmitter, QRNG, AM/FM Receiver
- **Scenario**: A compromised FM broadcaster injects sub-carrier signals designed to induce voltage instability in nearby quantum hardware.
- **Attack Steps**: Step 1: Set up QRNG hardware near FM radio receiver. Step 2: Transmit FM signals with specific sub-carrier noise profiles. Step 3: Monitor system behavior via logging entropy output. Step 4: Increase power or adjust modulation to cause jitter. Step 5: Run entropy bias tests during signal injection. Step 6: Attempt to show repeatable entropy disruption.
- **Detection**: QRNG stats anomalies
- **Solution**: Radio-frequency filtering and zoning
- **Tags**: fm, radio, qrng

## QRNG Jitter Injection via Bluetooth Audio Crosstalk

- **Attack Type**: Wireless (Bluetooth Audio Interference)
- **Target**: Consumer QRNG
- **Vulnerability**: Crosstalk from wireless audio devices
- **MITRE**: T0807 (Signal Interference)
- **Impact**: Unstable or degraded entropy
- **Tools**: Bluetooth speaker, Audio modulator app, QRNG test setup, Oscilloscope
- **Scenario**: An attacker uses Bluetooth speakers to emit modulated signals that cause electrical crosstalk in nearby QRNG components, affecting timing jitter in entropy generation.
- **Attack Steps**: Step 1: Place a QRNG device (preferably one using photodetectors or jitter-based entropy sources) near a Bluetooth speaker. Step 2: Connect the speaker to an attacker-controlled phone or computer. Step 3: Use a tone generator app to emit fluctuating high-frequency audio signals, modulated at intervals. Step 4: Observe the QRNG’s output bitstream using an entropy testing tool or oscilloscope. Step 5: Introduce rapid shifts in modulation and volume to simulate crosstalk. Step 6: Analyze whether entropy output shows patterns or jitter irregularities. Step 7: Repeat with varying distances to confirm RF-audio induced interference.
- **Detection**: QRNG jitter analyzer logs
- **Solution**: Shielded enclosures and audio filtering
- **Tags**: bluetooth, audio, qrng

## Temperature-Based QRNG Bias via Infrared Remote Emissions

- **Attack Type**: Wireless (Infrared Environmental Manipulation)
- **Target**: Photonic QRNG
- **Vulnerability**: IR-sensitive optical components
- **MITRE**: T1421 (Hardware Signal Disruption)
- **Impact**: Partial predictability of entropy
- **Tools**: Universal IR remote, QRNG with light sensors, IR camera, Entropy logger
- **Scenario**: A nearby IR remote control floods the environment with infrared bursts, causing photonic QRNGs to absorb unintended energy and shift randomness characteristics.
- **Attack Steps**: Step 1: Identify a QRNG device that utilizes photonic sources (e.g., beam splitters or photon detectors). Step 2: Set up the QRNG on a lab bench and point a programmable IR remote toward it. Step 3: Use a script or universal remote to emit pulses at various intensities and frequencies. Step 4: Monitor temperature around photodetectors with an IR camera. Step 5: Collect entropy output while IR emissions are active. Step 6: Compare entropy logs against IR emission patterns to detect correlation. Step 7: Validate with repeatable input sequences.
- **Detection**: Entropy deviation during IR exposure
- **Solution**: Use optical shielding or wavelength filters
- **Tags**: qrng, ir, temperature, entropy

## QRNG Bias via Smart Light Flicker Injection

- **Attack Type**: Wireless (Zigbee/BLE Light Control)
- **Target**: Optical QRNGs in Smart Buildings
- **Vulnerability**: Light-sensitive entropy generation
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Light-based entropy interference
- **Tools**: Zigbee/BLE smart bulb, App controller, Light sensor, QRNG
- **Scenario**: Attacker uses a smart light to generate flicker patterns that interfere with optical QRNG components sensitive to ambient light.
- **Attack Steps**: Step 1: Identify a QRNG device placed in an environment with smart lighting (e.g., office lab). Step 2: Install a smart bulb (Philips Hue, etc.) near the QRNG. Step 3: Use the controller app to produce intentional flicker patterns (vary brightness rapidly). Step 4: At the same time, log the QRNG output using entropy analysis tools. Step 5: Introduce repeatable flicker patterns with known frequency modulation. Step 6: Observe entropy stream for biases matching flicker modulation. Step 7: Attempt weak cryptographic key generation using manipulated QRNG output.
- **Detection**: Light/entropy cross-correlation logs
- **Solution**: Shield QRNG optics from environmental light
- **Tags**: qrng, smart light, flicker

## EM Pulse Injection from Drone Near Secure QRNG Facility

- **Attack Type**: Wireless (EM Field Attack via UAV)
- **Target**: QRNG in Critical Infrastructure
- **Vulnerability**: Susceptibility to remote EM injection
- **MITRE**: T1430 (Transmit Malicious Signals)
- **Impact**: Remote entropy manipulation attempt
- **Tools**: RF Transmitter Drone, Pulse generator, QRNG inside building, Spectrum analyzer
- **Scenario**: A drone flies near a secure facility and emits controlled electromagnetic pulses that target QRNG devices through walls or windows.
- **Attack Steps**: Step 1: Set up a small drone equipped with a low-power RF pulse emitter (e.g., 400–800 MHz). Step 2: Fly the drone near a building housing a QRNG system located close to windows. Step 3: Emit pulsed RF signals at intervals designed to induce switching noise. Step 4: Inside the lab, monitor QRNG entropy using onboard diagnostic APIs. Step 5: Synchronize drone pulses with QRNG output logs to identify timing correlation. Step 6: Evaluate impact using entropy statistical tests. Step 7: Verify repeatability of the effect during multiple flights.
- **Detection**: Spectrum anomaly + QRNG entropy logs
- **Solution**: RF dampening windows, drone detection
- **Tags**: qrng, drone, emf, physical-layer

## Wireless Glitching of QRNG Input Registers via NFC Fields

- **Attack Type**: Wireless (Glitch Attack via NFC Induction)
- **Target**: Embedded QRNG Microcontrollers
- **Vulnerability**: Input register glitch vulnerability
- **MITRE**: T1495.001 (Data Manipulation via Glitching)
- **Impact**: Faulty or repeated entropy values
- **Tools**: NFC Field Emitter, Arduino w/NFC Shield, QRNG-enabled MCU, Logic analyzer
- **Scenario**: By placing a high-frequency NFC emitter near a QRNG microcontroller, attacker induces glitches in entropy collection buffers.
- **Attack Steps**: Step 1: Set up a QRNG-enabled microcontroller (e.g., STM32) on a breadboard. Step 2: Place an NFC antenna emitting continuous signals directly next to the MCU. Step 3: Use a logic analyzer to monitor the QRNG data input registers. Step 4: Emit NFC bursts with varying frequencies and pulse widths. Step 5: Record timing faults or race conditions introduced in entropy sampling. Step 6: Compare randomness output before and during glitching events. Step 7: Attempt to cause entropy drops or repeats in random outputs.
- **Detection**: Register access timing analysis
- **Solution**: Shield logic circuitry from strong NFC fields
- **Tags**: glitching, qrng, nfc

## Fiber-based Quantum Trojan Horse with Reflected Light

- **Attack Type**: Quantum Trojan Horse via Fiber Channel
- **Target**: Quantum Key Distribution Node
- **Vulnerability**: Lack of monitoring for injected light signals
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Partial recovery of secret key bits; QKD protocol compromise
- **Tools**: Tunable laser, optical circulator, photodetector, polarization analyzer
- **Scenario**: An attacker injects invisible light into a fiber-optic QKD channel to gather key information via reflected signals.
- **Attack Steps**: Step 1: Set up a tunable laser source matching the operating wavelength of the target QKD system.Step 2: Connect the laser output to the QKD fiber link using a tap or circulator.Step 3: Inject weak coherent light pulses during the QKD key transmission phase.Step 4: Collect any back-reflected or scattered light using a photodetector.Step 5: Analyze polarization or phase changes in the reflected signal to infer key states.Step 6: Attempt to correlate findings with known key bit patterns.Step 7: Repeat across multiple rounds to refine accuracy.
- **Detection**: Optical intrusion monitoring; QBER analysis
- **Solution**: Use optical isolators, intrusion detection filters, and monitor QBER deviation
- **Tags**: #quantum #qkd #trojanhorse #optical

## Wireless Control Signal Injection in Quantum Modulators

- **Attack Type**: Quantum Trojan Horse via Wireless Side-Channel
- **Target**: Quantum Optical Transmitter
- **Vulnerability**: EMI shielding gaps in hardware
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Indirect leakage of key material; protocol breakdown
- **Tools**: SDR (e.g., HackRF), directional antenna, RF amplifier
- **Scenario**: The attacker emits wireless signals to manipulate or desynchronize electro-optic modulators used in quantum devices.
- **Attack Steps**: Step 1: Identify location of electro-optic modulators using EMI leakage and RF scanning.Step 2: Use a directional antenna to emit modulated RF signals that can influence the modulator driver.Step 3: Time RF bursts during qubit encoding operations.Step 4: Introduce desynchronization or subtle signal alterations.Step 5: Monitor downstream key rates or bit error rates to confirm impact.Step 6: Repeat with varying frequencies/amplitudes to refine disruption.Step 7: Infer key structure from system's error correction feedback.
- **Detection**: RF spectrum monitoring; increased QBER detection
- **Solution**: Shield enclosures; monitor power/RF anomalies; RF filters
- **Tags**: #wireless #quantumdevice #emi #rfattack

## Backdoor Implant in Wireless Quantum RNGs

- **Attack Type**: Quantum Trojan Horse via RNG
- **Target**: Wireless Quantum RNG
- **Vulnerability**: Embedded wireless chip exposed; lack of firmware validation
- **MITRE**: T1027.002 (Obfuscated Files or Information)
- **Impact**: Total key compromise due to leaked entropy
- **Tools**: Compromised firmware, Wi-Fi/Bluetooth interface, microcontroller
- **Scenario**: Wireless access to quantum-based RNG allows stealth implant to send entropy readings externally.
- **Attack Steps**: Step 1: Deploy modified firmware in a quantum RNG device with built-in wireless module.Step 2: Encode random number output into Wi-Fi/BLE beacons.Step 3: Continuously transmit entropy bits via disguised packets (e.g., hidden SSID names or timing intervals).Step 4: Adversary collects beacons using packet sniffers.Step 5: Reconstruct raw entropy pool remotely.Step 6: Predict or replicate private key material generated using this RNG.Step 7: Validate through side-channel monitoring of key usage.
- **Detection**: Passive wireless sniffing; firmware hash integrity checks
- **Solution**: Use air-gapped RNGs; disable wireless interfaces
- **Tags**: #quantumrng #entropy #firmware #wirelessbackdoor

## RF-Injected Photon Detector Blinding

- **Attack Type**: Quantum Trojan Horse via Detector Manipulation
- **Target**: Quantum Key Receiver Node
- **Vulnerability**: RF susceptibility of photodiodes; absence of shielding
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Full control over detector outcomes, key compromise
- **Tools**: SDR, high-power directional antenna, attenuators
- **Scenario**: Radio signals are used to blind or spoof the photon detectors in QKD receivers, forcing classical detection.
- **Attack Steps**: Step 1: Identify frequency bands where photon detectors are vulnerable to RF interference.Step 2: Aim high-gain antenna toward QKD receiver location.Step 3: Inject controlled RF noise to saturate or overload photon detectors.Step 4: Observe transition from quantum detection to classical saturation.Step 5: Use classical spoofing signals to manipulate outcomes.Step 6: Repeat during QKD key exchange sessions.Step 7: Analyze key error rate and timing changes to infer bits.
- **Detection**: RF emission logs; anomaly in QBER values
- **Solution**: Harden detectors; apply optical filters and RF shielding
- **Tags**: #detectorblinding #rfspoofing #qkdattack

## Quantum Channel Mapping via Wireless Signal Reflection

- **Attack Type**: Quantum Trojan Horse via Spatial Reflection
- **Target**: QKD Infrastructure
- **Vulnerability**: Exposed fiber layout; no channel obfuscation
- **MITRE**: T1595.002 (Active Scanning)
- **Impact**: Reconnaissance aiding future physical compromise
- **Tools**: mmWave radar, parabolic dish, signal analyzer
- **Scenario**: The attacker uses radar-like methods to map physical QKD fiber layouts and vulnerabilities.
- **Attack Steps**: Step 1: Scan QKD facility perimeter using mmWave radar or UWB tools.Step 2: Capture reflected signals from embedded optical fiber channels.Step 3: Construct a 3D spatial map of channel routing.Step 4: Locate bends, taps, or vulnerable access points.Step 5: Use this map to plan future fiber-injection or tapping attacks.Step 6: Simulate physical proximity attacks in controlled lab.Step 7: Measure feasibility of Trojan injection timing windows.
- **Detection**: Radar signature analysis; EM field monitoring
- **Solution**: Conceal fiber layout; randomized pathing and shielding
- **Tags**: #qkdmap #fiberoptics #radar #trojanhorse

## Optical Pulse Injection via Laser Leakage in Wireless-Controlled QKD

- **Attack Type**: Quantum Trojan Horse via Laser Pulses
- **Target**: Wireless-Controlled QKD Transmitter
- **Vulnerability**: Weak authentication on wireless admin panels
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Data leakage and corrupted key exchange
- **Tools**: Laser diode, Wi-Fi deauth tool, remote access tools
- **Scenario**: Exploiting open wireless control interfaces to inject rogue optical pulses into QKD transmitters.
- **Attack Steps**: Step 1: Identify a QKD transmitter with wireless admin interface for system diagnostics.Step 2: Use Wi-Fi scanner to detect exposed SSIDs or misconfigured access points.Step 3: Launch a deauthentication attack to disrupt active wireless sessions.Step 4: Gain access to web UI or API interface and inject rogue system commands.Step 5: Force laser diode to emit abnormal optical pulses during key exchange.Step 6: Use photodetector to collect reflections or analyze interference caused by rogue pulses.Step 7: Correlate timing and signal patterns with key generation cycles.
- **Detection**: Monitor abnormal pulse patterns; Wi-Fi intrusion logs
- **Solution**: Disable wireless admin panels; use out-of-band control
- **Tags**: #laserattack #qkd #wirelessinjection

## Bluetooth Low Energy (BLE) Beacon Spoofing on Quantum Device Controllers

- **Attack Type**: Quantum Trojan Horse via BLE Spoofing
- **Target**: BLE-controlled Quantum Node
- **Vulnerability**: Weak BLE pairing; unverified beacon payloads
- **MITRE**: T1001.003 (Protocol Impersonation)
- **Impact**: Remote manipulation of QKD configuration
- **Tools**: BLE beacon spoofer, smartphone with BLE sniffer
- **Scenario**: Attacker sends spoofed BLE signals to interfere with or confuse mobile-controlled QKD operations.
- **Attack Steps**: Step 1: Identify QKD systems with BLE-enabled mobile configuration apps.Step 2: Capture legit beacon signals using BLE sniffer to understand UUID and payload format.Step 3: Use BLE spoofer to replay beacon signals with altered parameters.Step 4: Observe if spoofed devices redirect user input to attacker-controlled interfaces.Step 5: Simultaneously inject rogue settings (e.g., reduce isolation, increase pulse rates).Step 6: Attempt to trigger quantum key drift or synchronization failure.Step 7: Analyze logs for tampering or forced key renegotiation patterns.
- **Detection**: BLE pairing logs; application integrity checks
- **Solution**: Pairing confirmation, beacon whitelisting
- **Tags**: #ble #spoofing #quantumcontrol

## Wi-Fi Signal Modulation to Influence Thermo-Optic Phase Shifters

- **Attack Type**: Quantum Trojan Horse via Indirect Thermal Effects
- **Target**: QKD Phase Modulator
- **Vulnerability**: No shielding against EM or thermal coupling
- **MITRE**: T1562.009 (Impair Process Control)
- **Impact**: Phase errors, key leakage during rekey events
- **Tools**: High-gain Wi-Fi antenna, thermal imager, SDR
- **Scenario**: Wi-Fi signals used to subtly heat internal optical components to cause phase drift.
- **Attack Steps**: Step 1: Map the target QKD device's external vents and thermally sensitive regions.Step 2: Use high-gain directional Wi-Fi antenna to continuously transmit high-power data.Step 3: Focus energy toward thermo-optic components like phase shifters.Step 4: Monitor internal temperature using thermal imager.Step 5: Correlate temperature rise with phase drift or QBER increase.Step 6: Time attack during key modulation to cause desynchronization.Step 7: Force re-initiation of key exchange with attacker-present timing window.
- **Detection**: Unexpected QBER spike with Wi-Fi traffic
- **Solution**: Apply RF/thermal shielding to optical casing
- **Tags**: #thermalattack #qkd #phasedrift

## Wi-Fi-based Clock Drift Attack on Quantum Synchronizers

- **Attack Type**: Quantum Trojan Horse via Timing Disruption
- **Target**: Quantum Timing Module
- **Vulnerability**: Dependence on Wi-Fi NTP sync; no secure fallback
- **MITRE**: T1498.002 (Network Denial of Service - Wireless)
- **Impact**: Sync error → unusable or leaked quantum keys
- **Tools**: SDR, NTP packet flooder, Wi-Fi jammer
- **Scenario**: Wireless signals affect timing modules, causing clock drift between quantum devices.
- **Attack Steps**: Step 1: Identify QKD components relying on NTP sync via Wi-Fi or wireless-GPS.Step 2: Jam primary sync channels or flood NTP traffic with altered timestamps.Step 3: Monitor system logs to identify desync behavior.Step 4: Exploit misaligned timebases to cause key mismatches.Step 5: Repeatedly trigger rekeying protocols to observe patterns.Step 6: Correlate changes in sync jitter with key exchange attempts.Step 7: Use info to predict or hijack re-initiation timing.
- **Detection**: Analyze system clock drift patterns
- **Solution**: Use wired sync methods and GPS fallback
- **Tags**: #clockattack #syncdrift #qkdsabotage

## Exploiting Side Reflections from Plastic Optical Fiber in Short-range QKD

- **Attack Type**: Quantum Trojan Horse via Signal Leakage
- **Target**: Short-range Fiber-based QKD
- **Vulnerability**: Imperfect end-face polish; weak reflection isolation
- **MITRE**: T1120 (Peripheral Device Discovery)
- **Impact**: Partial key recovery from back-reflected light
- **Tools**: Photodiode sensor, oscilloscope, fiber tap clamp
- **Scenario**: Reflected photons from imperfect fiber ends picked up by local sensors.
- **Attack Steps**: Step 1: Identify locations using plastic optical fiber (POF) for quantum transmission.Step 2: Use clamp-on tap to non-destructively collect reflections near connector.Step 3: Analyze reflection timing and shape to infer bit patterns.Step 4: Use photodiode to measure backscatter during transmission.Step 5: Repeat at multiple angles to improve signal fidelity.Step 6: Use oscilloscope to align reflected waveforms with key intervals.Step 7: Reconstruct partial key from amplitude/timing data.
- **Detection**: Monitor fiber integrity and tap attempts
- **Solution**: Replace with hardened connectors or add isolators
- **Tags**: #qkdleak #reflectionattack #fibersecurity

## Wi-Fi Controlled Firmware Downgrade on QKD Control Panel

- **Attack Type**: Quantum Trojan Horse via Wireless Firmware Downgrade
- **Target**: QKD Control Interface
- **Vulnerability**: No firmware signing or downgrade prevention
- **MITRE**: T1600 (Develop Capabilities)
- **Impact**: Full compromise of QKD trust chain
- **Tools**: Rogue AP, firmware repo mirror, MITM tool
- **Scenario**: Wireless vulnerability exploited to downgrade firmware to version with known flaws.
- **Attack Steps**: Step 1: Identify QKD systems with over-the-air firmware update capability.Step 2: Clone manufacturer’s firmware server using rogue Wi-Fi hotspot.Step 3: Use MITM tool to intercept firmware request and respond with older version.Step 4: Install firmware with built-in Trojan allowing passive key logging.Step 5: Monitor system logs for key material being exposed via API/debug.Step 6: Extract key fragments from debug channels.Step 7: Validate success via sync with intercepted traffic.
- **Detection**: Check firmware hash, logs of unexpected reboots
- **Solution**: Enforce signed firmware updates only
- **Tags**: #firmwaredowngrade #wirelessupdate #trojan

## Wireless Inductive Injection into QKD Power Lines

- **Attack Type**: Quantum Trojan Horse via Power Injection
- **Target**: Quantum Processing Module
- **Vulnerability**: Poor shielding on power lines; no surge protection
- **MITRE**: T1496 (Resource Hijacking)
- **Impact**: Corruption of key state generation
- **Tools**: Inductive coil, signal generator, EM probe
- **Scenario**: Inductive EM attack sends signals via power cable to interfere with internal quantum logic.
- **Attack Steps**: Step 1: Identify power cables leading to quantum processing units.Step 2: Place induction coil nearby (non-contact) and connect to waveform generator.Step 3: Inject waveforms designed to resonate at logic chip frequencies.Step 4: Observe disruption in photon generation or modulation timings.Step 5: Measure QBER or error correction behavior during attack.Step 6: Reconstruct attack effect from error logs and EM signatures.Step 7: Adjust frequency/amplitude for maximum non-destructive effect.
- **Detection**: Analyze error correction logs; EM probes
- **Solution**: Shield power lines; use surge isolators
- **Tags**: #inductiveattack #powerline #quantumlogic

## Radio Interference with Superconducting Qubits in Cryogenic Labs

- **Attack Type**: Quantum Trojan Horse via Cryo Interference
- **Target**: Cryogenic QKD Systems
- **Vulnerability**: RF shielding flaws in cryostats
- **MITRE**: T1203 (Exploit Physical Flaws)
- **Impact**: Qubit decoherence and operation loss
- **Tools**: High-frequency RF jammer, RF signal injector
- **Scenario**: RF signals injected into shielding flaws of cryogenic labs cause decoherence.
- **Attack Steps**: Step 1: Survey lab architecture for unshielded access points (vents, seams).Step 2: Inject narrow-band RF at GHz range matching qubit resonance frequencies.Step 3: Observe decoherence or logic gate failures during quantum ops.Step 4: Time injection during known logic gate pulses.Step 5: Use waveform disruption logs to correlate impact.Step 6: Repeat at different angles/frequencies to optimize.Step 7: Confirm attack by measuring drop in fidelity or key generation rate.
- **Detection**: RF sensors, qubit fidelity monitors
- **Solution**: Multi-layer shielding; RF trap design
- **Tags**: #cryointerference #rfattack #qubit

## Zigbee Interference Causing Quantum Lockout in IoT-QKD Gateways

- **Attack Type**: Quantum Trojan Horse via Zigbee Collision
- **Target**: IoT-QKD Smart Gateway
- **Vulnerability**: Weak Zigbee jamming protection
- **MITRE**: T1498.002 (Wireless DoS)
- **Impact**: Forced downgrade or unsafe key reuse
- **Tools**: Zigbee jammer, signal analyzer, Zigbee sniffer
- **Scenario**: Zigbee jamming causes control interface to stall, leading to unsafe key renegotiation.
- **Attack Steps**: Step 1: Detect QKD-integrated smart devices using Zigbee.Step 2: Flood control channels with Zigbee signals using jammer.Step 3: Observe if control panel crashes or resets due to channel congestion.Step 4: Trigger forced rekey operation due to reset.Step 5: Monitor new key negotiation and error correction exchange.Step 6: Exploit unvalidated fallback to default protocol.Step 7: Predict key or inject preconfigured fallback values.
- **Detection**: Zigbee radio analysis; fallback event logs
- **Solution**: Harden Zigbee stack; use secure fallback logic
- **Tags**: #zigbee #iot #qkd

## Wireless Malware Dropper in Quantum Device Debug Interface

- **Attack Type**: Quantum Trojan Horse via Debug Channel
- **Target**: Debug Port on QKD Node
- **Vulnerability**: Exposed debug interface, no auth
- **MITRE**: T1556.001 (Input Capture)
- **Impact**: Full capture of generated quantum keys
- **Tools**: ESP32 board, firmware dropper, UART-over-BLE bridge
- **Scenario**: Wireless debug port exploited to upload key-logging malware.
- **Attack Steps**: Step 1: Locate BLE/UART debug interface on QKD device.Step 2: Connect using ESP32 device mimicking debug controller.Step 3: Drop minimal firmware package with keylogging Trojan.Step 4: Restart QKD unit via soft reboot or BLE command.Step 5: Trojan records all key exchanges into flash memory.Step 6: Periodically broadcast logs over BLE.Step 7: Adversary listens from nearby location to retrieve key data.
- **Detection**: UART/BLE sniffers, firmware hash monitor
- **Solution**: Disable debug ports in production
- **Tags**: #wirelessmalware #debugport #qkd

## Wi-Fi Exploit on Quantum Device Mobile Companion App

- **Attack Type**: Quantum Trojan Horse via App Hijack
- **Target**: Mobile App to QKD System over Wi-Fi
- **Vulnerability**: Insecure mobile API traffic; lack of validation
- **MITRE**: T1185 (Browser Session Hijacking)
- **Impact**: Malicious reconfiguration causes partial quantum key exposure
- **Tools**: Fake Access Point (EvilAP), MITMproxy, Burp Suite
- **Scenario**: An attacker exploits a poorly secured mobile app that configures QKD systems over Wi-Fi, injecting commands to alter quantum channel settings.
- **Attack Steps**: Step 1: The attacker sets up a fake Wi-Fi access point with the same SSID as the QKD device's known network.Step 2: They lure the operator's mobile device into connecting to this rogue AP.Step 3: Using MITMproxy or Burp Suite, they intercept and inspect app traffic to extract API patterns used to send commands.Step 4: The attacker crafts malicious API requests (e.g., altering pulse amplitude or removing delay filters).Step 5: These changes subtly affect the way photons are encoded, introducing predictable patterns.Step 6: The attacker remotely listens to leaked information via optical reflection or timing analysis.Step 7: Finally, the attacker restores original settings to avoid suspicion.
- **Detection**: Traffic inspection, unexpected config changes
- **Solution**: Encrypt app traffic, enforce Wi-Fi certificate pinning
- **Tags**: #wifi #mobileapp #qkdhack

## Wireless Side-Channel Exploit Using TEMPEST on QKD Control Units

- **Attack Type**: Quantum Trojan Horse via Electromagnetic Leakage
- **Target**: QKD Control Unit
- **Vulnerability**: EM leakage due to insufficient shielding
- **MITRE**: T1020 (Automated Exfiltration)
- **Impact**: Side-channel recovery of secret quantum key data
- **Tools**: Directional TEMPEST antenna, RF spectrum analyzer, Faraday cage bypass tools
- **Scenario**: The attacker captures unintended EM emissions from QKD equipment using directional antennas to reconstruct internal operations.
- **Attack Steps**: Step 1: Attacker surveys the room containing the QKD control unit to locate any weak points in electromagnetic shielding (like vents or plastic panels).Step 2: Using a high-gain TEMPEST antenna, they place themselves within line of sight at a safe distance (e.g., nearby hallway).Step 3: The attacker begins monitoring the RF spectrum to find specific frequencies leaking emissions during key exchange.Step 4: They record the signal using an RF analyzer and apply filtering to isolate relevant emissions.Step 5: With the help of EM analysis tools, they reconstruct approximate timing, bit transitions, or control logic of quantum operations.Step 6: Over multiple sessions, they match emissions to known QKD states to infer key bits.Step 7: The attacker uses the leaked data to simulate a key and verify alignment with transmitted ciphertext.
- **Detection**: RF spectrum audits; detect shielding breaches
- **Solution**: Harden enclosures, install RF traps
- **Tags**: #TEMPEST #sidechannel #qkdhardware

## Remote Trigger of Quantum Key Buffer Leak via Wireless Debug Console

- **Attack Type**: Quantum Trojan Horse via Buffer Access
- **Target**: Debug Console on Quantum Device
- **Vulnerability**: Debug access left active; undocumented commands
- **MITRE**: T1552.001 (Credentials in Files)
- **Impact**: Full compromise of quantum session keys
- **Tools**: ESP32 with BLE/UART bridge, custom firmware
- **Scenario**: A backdoor in the QKD debug console is triggered via wireless signal, causing stored quantum keys to be transmitted in plaintext.
- **Attack Steps**: Step 1: The attacker scans for BLE-enabled debug consoles left active on QKD components.Step 2: They connect to the console using a microcontroller (like an ESP32) running custom firmware to emulate legitimate debug behavior.Step 3: Once connected, they send a hidden trigger string (e.g., "dump_keys#") known to unlock a debug mode.Step 4: The console responds by dumping recent quantum key material stored in the buffer (used for re-synchronization or troubleshooting).Step 5: The attacker receives the data wirelessly and stores it in a log.Step 6: The attacker disconnects and wipes any connection evidence.Step 7: They attempt to decrypt recorded traffic using stolen quantum keys.
- **Detection**: BLE session monitoring; audit of debug commands
- **Solution**: Disable debug in production; monitor BLE ports
- **Tags**: #qkd #wirelessdebug #bufferleak

## Interference Attack on Quantum Channel Calibration using RF Pulses

- **Attack Type**: Quantum Trojan Horse via Calibration Desync
- **Target**: QKD Modulation Hardware
- **Vulnerability**: Vulnerable DACs to EMI during calibration
- **MITRE**: T1602 (Data Manipulation)
- **Impact**: Partial quantum key inference due to predictable calibration errors
- **Tools**: Signal generator, RF emitter, oscilloscope
- **Scenario**: RF pulses subtly shift internal voltage levels during QKD calibration, leading to attacker-predictable bit errors.
- **Attack Steps**: Step 1: Identify the QKD system's calibration schedule, usually during idle hours or on reboot.Step 2: Deploy an RF signal generator and tune it to the control logic’s frequency (often MHz range).Step 3: Emit short, well-timed RF pulses during calibration to create voltage fluctuations inside the DAC (Digital-to-Analog Converter).Step 4: These fluctuations cause the modulator to improperly align with the quantum state generation.Step 5: The QKD system generates quantum bits (qubits) that are slightly offset or desynchronized.Step 6: The attacker observes these slight inconsistencies in ciphertext delivery and reconstructs patterns from the errors.Step 7: Over time, the attacker refines the attack to align with specific bit positions in the key.
- **Detection**: EMI logging during calibration routines
- **Solution**: Shield DAC components, schedule secure calibration
- **Tags**: #calibrationattack #rfinterference #qkd

## Drone-Based Wireless Interception of Entangled Photon Metadata

- **Attack Type**: Quantum Trojan Horse via Proximity RF
- **Target**: Satellite-Ground QKD Uplink
- **Vulnerability**: Auxiliary metadata over open wireless links
- **MITRE**: T1595.003 (Wireless Sniffing)
- **Impact**: Leakage of quantum session timing, aiding interception
- **Tools**: Commercial drone, high-gain Wi-Fi and BLE receiver, GPS logger
- **Scenario**: A drone flying near a quantum satellite uplink captures leaked metadata and synchronization beacons via wireless eavesdropping.
- **Attack Steps**: Step 1: The attacker configures a drone with long-range Wi-Fi/BLE sniffers and flies it close to the ground station performing QKD via satellite.Step 2: The attacker records broadcasted metadata like timing beacons, session IDs, and handshakes from unsecured auxiliary channels.Step 3: This metadata is correlated with entangled photon transmission windows.Step 4: Using timing analysis, the attacker predicts the approximate quantum bit alignment.Step 5: If weak or legacy protocols are used for metadata exchange, the attacker may replay or forge beacon sequences.Step 6: This causes synchronization issues, forcing the QKD system to resend portions of the key.Step 7: The attacker stores multiple key cycles and attempts to correlate drifted key segments with original data.
- **Detection**: Drone detection, metadata encryption
- **Solution**: Secure beacon exchange; encrypt metadata
- **Tags**: #droneattack #satelliteqkd #wirelessmetadata

## Jamming the Free-Space Quantum Channel with RF Noise

- **Attack Type**: Wireless RF Interference
- **Target**: Free-space QKD system
- **Vulnerability**: Optical Receiver Susceptibility to RF
- **MITRE**: T0813 - Jamming
- **Impact**: Disruption of key exchange process
- **Tools**: RF Jammer, Directional Antenna, SDR
- **Scenario**: Attacker disrupts quantum key distribution by overwhelming the free-space optical link with directed RF interference.
- **Attack Steps**: Step 1: Set up two systems simulating QKD endpoints using free-space lasers. Step 2: Place an RF jammer with directional antenna near the receiver station. Step 3: Aim the jammer towards the photodetector at the receiver. Step 4: Gradually increase RF output while monitoring QBER (quantum bit error rate). Step 5: Observe that the QBER rises beyond threshold, causing protocol abortion. Step 6: Log how the quantum key exchange fails under continuous jamming.
- **Detection**: Monitor QBER; Check environmental RF logs
- **Solution**: Shielding & relocation of quantum detectors; RF spectrum monitoring
- **Tags**: QKD, RF, Jamming, Quantum DoS, SDR

## Wi-Fi Flood Near QKD Control Channel

- **Attack Type**: Wireless Protocol Flooding
- **Target**: QKD over Hybrid Wireless
- **Vulnerability**: Wi-Fi Control Channel Congestion
- **MITRE**: T0814 - Wireless Protocol Manipulation
- **Impact**: Disruption of classical coordination
- **Tools**: Wi-Fi Pineapple, Aireplay-ng, Laptop
- **Scenario**: Overloads classical communication control channel of QKD with 802.11 flooding, preventing coordination between endpoints.
- **Attack Steps**: Step 1: Set up a lab QKD environment where quantum channel and classical channel are separated. Step 2: Identify the Wi-Fi network used for classical sync (public/shared SSID). Step 3: Use Aireplay-ng to launch a deauthentication or beacon flood attack. Step 4: Flood the channel continuously, observe that QKD fails due to unacknowledged messages. Step 5: Monitor CPU/network logs on QKD controller for packet drop rates. Step 6: Log the resulting denial of service in key generation.
- **Detection**: Wi-Fi traffic anomaly detection; Packet loss monitoring
- **Solution**: Use wired out-of-band control channels or hardened wireless
- **Tags**: QKD, Wi-Fi, DoS, Aireplay, Flooding

## GPS Spoofing to Misalign QKD Antennas

- **Attack Type**: Wireless GPS Spoofing
- **Target**: Free-space QKD system with GPS
- **Vulnerability**: GPS Dependence for Alignment
- **MITRE**: T0854 - GPS Spoofing
- **Impact**: Quantum channel fails due to alignment errors
- **Tools**: GPS Spoofer (TX capable SDR), GNSS-SDR
- **Scenario**: Attacker sends spoofed GPS signals to misalign free-space QKD system’s telescopes relying on geolocation alignment.
- **Attack Steps**: Step 1: Create a controlled testbed with GPS-based auto-aligning QKD transmit and receive stations. Step 2: Place an SDR close to the QKD receiver with GPS spoofing software. Step 3: Generate fake GPS signals shifting position slightly. Step 4: Observe telescope misalignment as the system tries to auto-adjust. Step 5: Continue spoofing until link fails and no photons are received. Step 6: Record the impact on photon counts and link downtime.
- **Detection**: GNSS anomaly logging; photon loss pattern
- **Solution**: Remove GPS auto-alignment; use inertial sensors
- **Tags**: QKD, GPS Spoof, DoS, SDR, Telescopic

## Fake Entangled Photon Flood

- **Attack Type**: Entanglement Spoofing Over Wireless
- **Target**: Entanglement-based QKD System
- **Vulnerability**: Lack of Photon Source Authentication
- **MITRE**: T0803 - Signal Interference
- **Impact**: QKD protocol abort due to QBER spike
- **Tools**: SPDC-based Entangled Source, Laser Emitter
- **Scenario**: Attacker uses wireless photon emitter to flood receiver with fake entangled photons, causing authentication failure.
- **Attack Steps**: Step 1: Simulate QKD using entangled photon pairs between Alice (sender) and Bob (receiver). Step 2: Set up a fake emitter near Bob that generates single photons with random polarization. Step 3: Emit photons synchronized to confuse timing window of Bob's receiver. Step 4: Bob receives both legitimate and attacker photons, causing mismatch. Step 5: Alice and Bob notice rising QBER and abort protocol. Step 6: Repeat to demonstrate how fake photons disrupt entangled key exchange.
- **Detection**: QBER spike; timing analysis of photon arrivals
- **Solution**: Use authenticated timing sync, filtering lens
- **Tags**: QKD, Entanglement, Photon Flood, DoS

## RFID Denial-of-Service Near Quantum Device Access Cards

- **Attack Type**: RFID Wireless Interference
- **Target**: Physical Access to QKD Nodes
- **Vulnerability**: RFID Reader Flooding
- **MITRE**: T0816 - RFID Interference
- **Impact**: Indirect DoS by delaying critical access
- **Tools**: RFID Emulator (Proxmark3), RFID Jammer
- **Scenario**: Jamming or spamming RFID access to delay physical access to quantum equipment, indirectly disrupting critical timing for QKD.
- **Attack Steps**: Step 1: Identify lab setting where access to quantum devices is secured with RFID. Step 2: Use Proxmark3 to continuously send spoofed invalid RFID signals near the reader. Step 3: Observe that valid cards are ignored due to reader overload. Step 4: As access is blocked, QKD time-sensitive maintenance or calibration is delayed. Step 5: Repeat the interference over a long session to simulate denial impact. Step 6: Document effect on QKD system stability and access delay.
- **Detection**: RFID activity logs; physical entry delay logs
- **Solution**: Secure RFID channel; shielded readers
- **Tags**: QKD, RFID, DoS, Access Control

## BLE Beacon Overload Near Quantum Device Sync Modules

- **Attack Type**: BLE Beacon Flooding
- **Target**: Portable QKD Node with BLE Sync
- **Vulnerability**: BLE Channel Saturation
- **MITRE**: T0804 - Bluetooth Flooding
- **Impact**: QKD sync failure, no key generated
- **Tools**: ESP32 with custom firmware, BLE spammer
- **Scenario**: Attacker overloads BLE-based time-sync modules used in portable QKD devices to disrupt key generation.
- **Attack Steps**: Step 1: Simulate a compact QKD device that uses BLE beaconing for synchronization with base. Step 2: Load custom BLE spamming script onto ESP32 device. Step 3: Position ESP32 near the QKD receiver. Step 4: Start broadcasting hundreds of fake BLE advertisements per second. Step 5: Observe the QKD sync module becoming unresponsive or rejecting true beacons. Step 6: Resulting in aborted QKD sessions due to sync failure.
- **Detection**: BLE sniffer logs, missing sync packets
- **Solution**: Use wired sync or BLE whitelist + filtering
- **Tags**: QKD, BLE, DoS, Beacon Flood, Sync Attack

## Wi-Fi Deauth Attack on Post-Quantum VPN Router

- **Attack Type**: Wireless Management Frame Attack
- **Target**: PQ VPN Gateway (Wi-Fi)
- **Vulnerability**: Open management frames
- **MITRE**: T0812 - Deauthentication Attack
- **Impact**: PQ VPN key negotiation fails
- **Tools**: Kali Linux, Aireplay-ng, Monitor-mode Adapter
- **Scenario**: Prevents PQC VPN session initiation via continuous Wi-Fi deauthentication.
- **Attack Steps**: Step 1: Set up PQC-enabled VPN router using Wi-Fi uplink to exchange post-quantum keys. Step 2: Connect target system to router via WPA2. Step 3: Use Aireplay-ng to perform --deauth flood attack on client MAC address. Step 4: Observe VPN tunnel failing to establish due to constant reconnects. Step 5: Repeat for extended period to simulate full denial. Step 6: Capture logs showing handshake failures and no PQ key exchange.
- **Detection**: Wi-Fi disconnect logs, WPA handshake failures
- **Solution**: Use WPA3 + MFP (Management Frame Protection)
- **Tags**: PQC, VPN, Wi-Fi, Deauth, DoS

## SDR Pulse Injection to Disturb Single-Photon Detectors

- **Attack Type**: Electromagnetic Pulse via SDR
- **Target**: Optical QKD Detector
- **Vulnerability**: RF Susceptibility in SPADs
- **MITRE**: T0860 - Hardware Signal Injection
- **Impact**: Detector blinding, false positives
- **Tools**: HackRF One, GNU Radio, Directional Antenna
- **Scenario**: Injecting sharp, directed RF pulses that blind or saturate SPAD photon detectors in QKD receivers.
- **Attack Steps**: Step 1: Set up a lab QKD system using SPAD (single-photon avalanche diodes). Step 2: Connect HackRF One and build a pulse generator in GNU Radio. Step 3: Aim the directional antenna at the detector module. Step 4: Emit RF pulses (nanosecond scale) at intervals matching expected photon arrival. Step 5: Observe detector saturation or false clicks. Step 6: QKD aborts due to high QBER or detector timeouts.
- **Detection**: Detector log anomaly (click burst), temperature logs
- **Solution**: RF shielding and filtered casing
- **Tags**: QKD, SDR, SPAD, Detector DoS

## Wi-Fi Beacon Spoofing of QKD Sync Channel

- **Attack Type**: Beacon Spoofing
- **Target**: Wireless-Synced QKD System
- **Vulnerability**: Beacon spoofing vulnerability
- **MITRE**: T0810 - Wi-Fi Beacon Flooding
- **Impact**: QKD coordination disruption
- **Tools**: Scapy, Kali Linux, Wireless NIC
- **Scenario**: Disrupting Wi-Fi-based timing coordination for QKD by spoofing the AP beacon with false SSIDs.
- **Attack Steps**: Step 1: Deploy QKD testbed using Wi-Fi-based time sync (custom implementation). Step 2: Use Scapy to craft spoofed beacon frames with similar SSID. Step 3: Start broadcasting these beacons with strong signal. Step 4: QKD client confuses beacon source and syncs with incorrect timing. Step 5: Observe QKD protocol timing failure. Step 6: Record failed synchronization sessions and errors.
- **Detection**: Wi-Fi packet logs; signal strength monitoring
- **Solution**: Use beacon authentication or fixed sync
- **Tags**: QKD, Beacon, Wi-Fi Spoof, Timing Attack

## Signal Reflection Disruption Using Directional Antenna

- **Attack Type**: Indirect Jamming via RF Reflection
- **Target**: Free-space Polarized QKD
- **Vulnerability**: Path alignment disruption via EM noise
- **MITRE**: T0806 - Electromagnetic Interference
- **Impact**: Polarization mismatch, QBER spike
- **Tools**: Parabolic Reflector, Signal Generator
- **Scenario**: Causing multiple reflection paths to distort QKD channel polarization alignment.
- **Attack Steps**: Step 1: Set up an open-air free-space QKD link with polarization encoding. Step 2: Use a parabolic reflector to bounce RF signals into QKD beam path. Step 3: Generate modulated signals at matching photon wavelength frequency. Step 4: Observe interference patterns altering polarization at the receiver. Step 5: Track spike in error rates and QKD shutdown. Step 6: Log correlation between RF pulses and QKD error metrics.
- **Detection**: Polarization analyzer, alignment check
- **Solution**: Use closed optical path or Faraday isolator
- **Tags**: QKD, Reflection, RF Noise, DoS

## Zigbee Packet Storm Affecting QKD Peripheral Devices

- **Attack Type**: Zigbee DoS on QKD Environmental Controls
- **Target**: Environmental Support for QKD
- **Vulnerability**: Weak Zigbee security
- **MITRE**: T0830 - Zigbee Flooding
- **Impact**: QKD auto-shutdown from missing sensor data
- **Tools**: Zigbee dongle (CC2531), KillerBee
- **Scenario**: Overwhelming Zigbee-based devices (cooling, timing sensors) to destabilize QKD.
- **Attack Steps**: Step 1: Build a small-scale QKD testbed relying on Zigbee environmental modules (temp, alignment). Step 2: Use KillerBee tools to flood Zigbee coordinator with random packets. Step 3: Disable legitimate sensor data transmission. Step 4: Observe QKD abort due to out-of-range temperature or missing alignment data. Step 5: Repeat flooding for continuous disruption. Step 6: Log failure timestamps and QKD controller response.
- **Detection**: Zigbee packet monitor; sensor health logs
- **Solution**: Use wired sensors or Zigbee mesh redundancy
- **Tags**: QKD, Zigbee, Sensor Attack, DoS

## Wi-Fi Probe Request Bomb to Confuse QKD Time Sync

- **Attack Type**: Probe Request Flooding
- **Target**: QKD over Wi-Fi
- **Vulnerability**: Probe request exhaustion
- **MITRE**: T0815 - Wireless Request Flood
- **Impact**: QKD timing sync fails
- **Tools**: Scapy, Python Script
- **Scenario**: Attacker floods QKD Wi-Fi interface with probe requests to delay sync packets.
- **Attack Steps**: Step 1: Build a script using Scapy to send random Wi-Fi probe requests. Step 2: Identify QKD Wi-Fi channel and device MAC. Step 3: Execute the script continuously near QKD receiver. Step 4: Observe increase in dropped or delayed sync packets. Step 5: Monitor QKD session failures due to timing window mismatch. Step 6: Analyze sync delay logs to correlate with flood activity.
- **Detection**: Wi-Fi packet inspection; sync retries
- **Solution**: Use probe filtering and MAC whitelist
- **Tags**: QKD, Wi-Fi, Probe Flood, Sync DoS

## RFID Jammer Delaying Access to Portable QKD Kit

- **Attack Type**: RFID Access Denial
- **Target**: Portable QKD Case with RFID Lock
- **Vulnerability**: RFID Unprotected Channel
- **MITRE**: T0816 - RFID Jamming
- **Impact**: Missed QKD sync due to delayed access
- **Tools**: RFID Jammer, SDR
- **Scenario**: Blocking technician access to portable QKD system by RFID reader jamming.
- **Attack Steps**: Step 1: Assume technician needs to authenticate via RFID to start QKD calibration. Step 2: Place jammer near RFID reader. Step 3: Emit continuous noise at 13.56 MHz. Step 4: Observe authentication failures or delay in logging in. Step 5: Missed calibration window causes QKD session abort. Step 6: Record delay and access failure impact on overall QKD.
- **Detection**: RFID logs, authentication retries
- **Solution**: Hardened readers; EMI-resistant enclosures
- **Tags**: QKD, RFID, Jammer, Physical Delay

## 5GHz Wi-Fi Radar Interference with QKD Overlap

- **Attack Type**: DFS-based Radar Spoof
- **Target**: Wi-Fi-based QKD
- **Vulnerability**: DFS vulnerability
- **MITRE**: T0837 - Wireless Interference
- **Impact**: Unstable QKD session
- **Tools**: Wi-Fi Adapter, DFS Radar Pattern Generator
- **Scenario**: Triggering Dynamic Frequency Selection (DFS) to force QKD Wi-Fi out of critical band.
- **Attack Steps**: Step 1: Setup QKD using 5GHz Wi-Fi as sync/control channel. Step 2: Use SDR or modified adapter to send radar-like signals. Step 3: Trigger DFS, causing Wi-Fi to jump to another channel. Step 4: Observe QKD session drop due to loss of sync. Step 5: Repeatedly trigger DFS to keep session in unstable state. Step 6: Log frequency changes and QKD error patterns.
- **Detection**: DFS logs, frequency hopping reports
- **Solution**: Use DFS-immune spectrum or wired sync
- **Tags**: QKD, DFS, Radar Spoof, Wi-Fi DoS

## Narrowband FM Carrier Injection to QKD Receiver

- **Attack Type**: Narrowband Interference
- **Target**: QKD Receiver Electronics
- **Vulnerability**: Narrowband RF leak vulnerability
- **MITRE**: T0806 - RF Signal Injection
- **Impact**: QKD link corruption
- **Tools**: FM Signal Generator, Frequency Analyzer
- **Scenario**: Inserting FM carriers at vulnerable frequencies to degrade QKD receiver electronics.
- **Attack Steps**: Step 1: Tune into internal frequency of QKD receiver circuitry (testbed). Step 2: Inject FM carrier near that frequency using signal generator. Step 3: Observe distortion in signal processing module. Step 4: Monitor increase in QBER due to analog interference. Step 5: Repeat at different frequencies to identify vulnerable bands. Step 6: Log error increase and session abort.
- **Detection**: RF spectrum analysis
- **Solution**: Use filters, shielding, tuned circuits
- **Tags**: QKD, Narrowband, FM Injection, DoS

## Overpowering the Quantum Channel with IR Noise

- **Attack Type**: Infrared Flooding
- **Target**: Free-space Optical QKD Receiver
- **Vulnerability**: No shielding from ambient IR
- **MITRE**: T0817 - Optical Channel Disruption
- **Impact**: QKD session fails due to detection interference
- **Tools**: Infrared LED Array, Power Supply, Optical Alignment Rig
- **Scenario**: Attacker introduces high-intensity infrared light into the QKD optical channel to overwhelm the photodetectors and cause quantum bit error rate (QBER) to rise.
- **Attack Steps**: Step 1: Build a basic QKD setup with a free-space optical path between sender (Alice) and receiver (Bob). Step 2: Place a powerful IR LED array near the optical receiver (Bob) and align it toward the incoming optical beam. Step 3: Gradually increase the intensity of the IR floodlight while observing Bob’s detection rate. Step 4: As photodetectors saturate or misfire, QBER will increase significantly. Step 5: Monitor QKD controller until protocol aborts due to error threshold breach. Step 6: Log the effect of IR light on photon reception quality and session termination.
- **Detection**: QBER spike detection, IR sensor logs
- **Solution**: Use band-pass filters and optical isolators
- **Tags**: QKD, IR Jamming, Free-space, Detector Overload

## LoRa Signal Collision to Disrupt Quantum Sensor Communication

- **Attack Type**: LoRa Interference
- **Target**: LoRa-based QKD Monitoring
- **Vulnerability**: Unprotected LoRa channel
- **MITRE**: T0853 - Wireless Collision Flooding
- **Impact**: QKD aborts from missing environmental sync
- **Tools**: LoRaWAN Transmitter (Heltec, RFM95), Arduino IDE
- **Scenario**: LoRa signals used for monitoring environmental parameters in QKD systems are disrupted by signal collision flooding, leading to denial of key generation.
- **Attack Steps**: Step 1: Simulate a QKD device that receives temperature and alignment data via LoRa sensor nodes. Step 2: Build a LoRa interference device using a Heltec WiFi LoRa board. Step 3: Program the board to transmit random LoRa packets at same frequency and spreading factor as target. Step 4: Deploy near the QKD base station and begin continuous transmission. Step 5: Sensor data packets begin colliding and getting dropped. Step 6: QKD controller halts operation due to missing environmental inputs. Step 7: Document logs showing packet loss and session failure.
- **Detection**: LoRa gateway logs, packet loss rate
- **Solution**: Use frequency-hopping LoRa and CRC filtering
- **Tags**: QKD, LoRa, Collision, IoT DoS

## Ultrasonic Soundwave Interference with Quantum Receiver Stabilizer

- **Attack Type**: Acoustic Channel Attack
- **Target**: Mechanically Stabilized QKD Receiver
- **Vulnerability**: Acoustic resonance vulnerability
- **MITRE**: T0851 - Acoustic Signal Disruption
- **Impact**: Optical misalignment halts QKD key gen
- **Tools**: Ultrasonic Transducer, Function Generator
- **Scenario**: Uses ultrasonic sound waves to vibrate or desynchronize mechanical stabilizers in the QKD receiver, breaking alignment.
- **Attack Steps**: Step 1: Set up a stabilized optical QKD receiver using a mount or gimbal system for precise beam alignment. Step 2: Place a directional ultrasonic transducer near the stabilizer platform. Step 3: Generate an ultrasonic tone (~20–25 kHz) and aim at the stabilizer assembly. Step 4: Observe mechanical resonance or jitter causing misalignment of the receiver optics. Step 5: Track degradation in photon reception and subsequent protocol failure. Step 6: Log error spikes, vibration sensor outputs, and stabilization failures.
- **Detection**: Stabilization sensor logs; QKD key rate logs
- **Solution**: Use vibration-absorbing casing and isolation
- **Tags**: QKD, Ultrasonic, Stabilizer, Mechanical DoS

## Zigbee-Based Remote Shutdown of QKD Cooling System

- **Attack Type**: Wireless Device Command Spoofing
- **Target**: Temperature-Sensitive QKD System
- **Vulnerability**: No Zigbee frame authentication
- **MITRE**: T0844 - Protocol Message Injection
- **Impact**: Detector failure from overheating
- **Tools**: Zigbee Transmitter (CC2531), KillerBee
- **Scenario**: Sends malicious Zigbee control frames to power off QKD cooling units, causing detector overheating.
- **Attack Steps**: Step 1: Set up a simulated QKD device with temperature-sensitive detectors (e.g., SPAD) and a Zigbee-connected cooling system. Step 2: Use KillerBee with a Zigbee dongle to scan for the cooling unit’s network address. Step 3: Craft a spoofed control frame mimicking a valid shutdown command. Step 4: Transmit the packet and verify the cooling system powers off. Step 5: Observe the detector module heating up and eventual QKD failure due to thermal noise. Step 6: Log detector temperatures, QBER increase, and shutdown timestamp.
- **Detection**: Cooling logs; Zigbee command logs
- **Solution**: Use secure Zigbee firmware or manual override
- **Tags**: QKD, Cooling, Zigbee Spoof, Thermal DoS

## Smart Antenna Spoofing to Mislead Auto-Tracking QKD Telescopes

- **Attack Type**: Directional Beam Spoof
- **Target**: Free-space QKD with Smart Tracking
- **Vulnerability**: Spoofable AoA logic in tracking systems
- **MITRE**: T0870 - Signal Source Deception
- **Impact**: Receiver points to fake source; no key formed
- **Tools**: SDR (HackRF), Smart Reflectors, GPS Spoofer
- **Scenario**: Spoofs position data using signal strength tricks to redirect auto-tracking QKD telescope away from the actual sender.
- **Attack Steps**: Step 1: Set up an auto-tracking free-space QKD receiver with angle-of-arrival (AoA) sensing. Step 2: Deploy a fake reflector emitting dummy sync signals from a slightly different angle. Step 3: Use SDR to mimic sync tones or fake signal strength peaks from the wrong direction. Step 4: Observe the telescope adjusting to incorrect path. Step 5: Real QKD photons are missed or scattered, increasing error rate. Step 6: Track QKD log showing sync drops, misalignment, and key gen failure.
- **Detection**: AoA logs, missed sync events, QBER spikes
- **Solution**: Use multiple validation beacons, manual override
- **Tags**: QKD, Telescope, Smart Beam, AoA Spoof

## AI-Guided Side-Channel Attack via Bluetooth Leakage

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum Device using Bluetooth
- **Vulnerability**: Bluetooth side-channel leaks during computation
- **MITRE**: T1203 (Exploitation for Client Execution), T1040 (Network Sniffing)
- **Impact**: Partial key recovery
- **Tools**: Ubertooth One, AI Model (e.g., LSTM), Wireshark, TensorFlow
- **Scenario**: Using an AI model to identify post-quantum decryption patterns via Bluetooth signal fluctuations during key exchanges.
- **Attack Steps**: Step 1: Place a Bluetooth sniffer (Ubertooth One) near the quantum device that uses Bluetooth for occasional telemetry.Step 2: Capture multiple sessions of encrypted post-quantum key exchanges over Bluetooth.Step 3: Feed signal timing and amplitude metadata into a trained LSTM AI model trained to recognize signal leakage patterns.Step 4: Correlate repeated patterns with known PQ algorithm behaviors (e.g., keygen time or CPU power signatures).Step 5: Use output from the model to predict specific key fragments and reconstruct partial keys.
- **Detection**: Detect nearby Bluetooth sniffers and excessive signal noise during exchanges
- **Solution**: Use Bluetooth shielding and limit telemetry over wireless
- **Tags**: ai-assisted, bluetooth, side-channel, post-quantum

## Wi-Fi Metadata Analysis with AI to Predict PQ Algorithm Type

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ-enabled Wi-Fi Routers or Laptops
- **Vulnerability**: Metadata leakage from Wi-Fi
- **MITRE**: T1040 (Network Sniffing), T1596.003 (Search Open Websites/Domains)
- **Impact**: Reveals type of PQ algorithm
- **Tools**: Wireshark, Scapy, AI Classifier (CNN), Raspberry Pi
- **Scenario**: AI model analyzes Wi-Fi packet metadata (timing, packet sizes) to determine the type of post-quantum algorithm in use.
- **Attack Steps**: Step 1: Deploy a Raspberry Pi near the target to capture all Wi-Fi traffic using monitor mode.Step 2: Use Wireshark to record packet timestamps and sizes, without decrypting any payload.Step 3: Train an AI model (e.g., CNN) on known PQ algorithms' metadata fingerprints.Step 4: Feed captured metadata to the AI model to classify which PQ algorithm is being used.Step 5: Use that algorithm-specific knowledge to prepare for more focused side-channel or cryptanalysis attacks.
- **Detection**: Wireless traffic monitoring, anomaly-based detection
- **Solution**: Add random timing padding; obfuscate PQ algorithm signature
- **Tags**: ai, wifi, side-channel, pqc

## AI-Powered RFID Eavesdropping for PQ Key Timing Analysis

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: RFID-using PQ Authentication Devices
- **Vulnerability**: Signal timing leakage during RFID authentication
- **MITRE**: T1010 (Application Window Discovery), T1040
- **Impact**: PQ implementation classification
- **Tools**: Proxmark3, AI Model (RNN), Oscilloscope, SDR
- **Scenario**: Using an AI model to analyze timing variations in RFID responses that reveal post-quantum crypto usage characteristics.
- **Attack Steps**: Step 1: Place an RFID sniffer (Proxmark3 or SDR) near a PQ smart badge reader.Step 2: Capture repeated RFID transaction sessions, focusing on timing and signal energy.Step 3: Train a recurrent neural network (RNN) to find delays or timing artifacts linked to PQ decryption (e.g., for lattice-based crypto).Step 4: Use the AI's predictions to distinguish between standard and PQ RFID implementations.Step 5: Craft further targeted electromagnetic or timing-based attacks to extract keys.
- **Detection**: Detect abnormal RFID reads or erratic read timing
- **Solution**: Shielded readers; constant-time crypto operations
- **Tags**: ai-rfid, side-channel, pqc, rfid-timing

## Drone-Based AI Recon to Map PQ IoT Device Activity

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ IoT Sensors
- **Vulnerability**: Unencrypted metadata in wireless beacons
- **MITRE**: T1592.002 (Gather Victim Host Information), T1595
- **Impact**: Maps out PQ device behavior
- **Tools**: Drone + RTL-SDR, YOLOv5 AI Model, GPS Mapper
- **Scenario**: Using AI-enabled drones to passively map the behavior and crypto routines of PQ IoT devices through wireless activity signatures.
- **Attack Steps**: Step 1: Launch a drone fitted with RTL-SDR and AI camera over a secure campus with PQ IoT sensors.Step 2: Passively collect wireless signals (Zigbee, Wi-Fi, BLE) over several sessions.Step 3: Feed signal bursts, timing, and strength into an AI model trained to detect PQ crypto cycles (based on signal noise or beacon timings).Step 4: Overlay activity heatmaps with AI-analyzed traffic patterns to identify which zones/devices are running PQ algorithms.Step 5: Use findings to prioritize physical or logical attacks on PQ devices.
- **Detection**: RF signal triangulation, device motion analysis
- **Solution**: Randomize beacon intervals, encrypt metadata
- **Tags**: drone, pq-iot, recon, ai

## AI Exploitation of Quantum Key Distribution Over RF Relay

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum RF Key Distribution Nodes
- **Vulnerability**: Photon timing leakage via RF medium
- **MITRE**: T1600 (Weaken Encryption), T1586.001 (Compromise Infrastructure)
- **Impact**: Partial QKD key recovery
- **Tools**: SDR, AI Regression Model, RF Amplifier, GNU Radio
- **Scenario**: Simulating RF-based man-in-the-middle on a QKD link by analyzing photon timing leaks using AI models trained on past key exchanges.
- **Attack Steps**: Step 1: Position an SDR-equipped device between two QKD-capable quantum nodes communicating over RF.Step 2: Use GNU Radio to demodulate photon timing signals in real-time.Step 3: Feed recorded timing variations into an AI regression model trained to correlate these with key bit positions.Step 4: Simulate man-in-the-middle interference using RF relays to induce deliberate errors.Step 5: Extract useful entropy patterns from the AI model’s prediction and simulate partial key reconstruction.
- **Detection**: Monitoring of QKD timing error rates
- **Solution**: RF shielding, time-jitter countermeasures
- **Tags**: qkd, rf-relay, ai-assisted, wireless

## AI-Guided Zigbee Packet Delay Profiling

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Zigbee-based IoT Device
- **Vulnerability**: Timing metadata not encrypted
- **MITRE**: T1040, T1595.002
- **Impact**: Identifies when and where crypto operations happen
- **Tools**: Zigbee Sniffer (TI CC2531), LSTM Model, Wireshark
- **Scenario**: Leveraging AI to analyze packet timing delays in Zigbee mesh networks to infer PQ cryptographic computations.
- **Attack Steps**: Step 1: Deploy a Zigbee sniffer near a PQ-enabled smart device (e.g., smart lock or light).Step 2: Passively record Zigbee traffic over several days without decrypting the content.Step 3: Extract timestamps between packets and calculate delays between transmissions.Step 4: Train an AI model (LSTM) to detect anomalies where delay patterns suggest intensive PQ key generation (e.g., larger keys = more delay).Step 5: Use this model to identify cryptographic operations and predict where the most critical keys reside.
- **Detection**: Time-based anomaly detection
- **Solution**: Encrypt Zigbee metadata and add timing jitter
- **Tags**: ai, zigbee, pqc, timing-analysis

## AI-Facilitated BLE Traffic Clustering for PQ Usage Profiling

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: BLE-enabled PQ Devices
- **Vulnerability**: Behavior fingerprinting via RF metadata
- **MITRE**: T1592.002, T1596
- **Impact**: Isolates PQ devices in a crowd
- **Tools**: BLE Sniffer (nRF52840), K-Means Clustering (Python), Jupyter Notebook
- **Scenario**: Grouping Bluetooth Low Energy (BLE) device behaviors using AI to detect PQ-enabled devices in a mixed environment.
- **Attack Steps**: Step 1: Position a BLE sniffer near an office with mixed legacy and PQ-enabled devices.Step 2: Capture BLE advertisements, connection intervals, and signal strength.Step 3: Extract key metrics: packet length, response delays, connection frequency.Step 4: Feed metrics into a clustering AI algorithm (e.g., k-means) to group similar device behavior.Step 5: Identify outlier clusters that match behavior of PQ encryption devices (e.g., longer key exchanges, fewer broadcasts).
- **Detection**: BLE signal baseline fingerprinting
- **Solution**: Obfuscate packet sizes and timing
- **Tags**: ble, ai, clustering, pq-fingerprinting

## AI-Powered Signal Reflection Mapping of PQ IoT Networks

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Smart PQ-Enabled Building Devices
- **Vulnerability**: RF energy leaks from crypto processing
- **MITRE**: T1595.002, T1600
- **Impact**: Reveals crypto operation zones
- **Tools**: SDR (HackRF), AI Spatial Mapper, GNURadio, AI Heatmap Model
- **Scenario**: Mapping RF signal reflections to locate and characterize PQ crypto hotspots using AI-assisted spatial analysis.
- **Attack Steps**: Step 1: Walk or fly with an SDR device collecting RF signal strength and reflection data from walls and objects.Step 2: Use AI model trained to recognize signal "echoes" from PQ crypto activity (typically more intense bursts).Step 3: Generate a heatmap of signal density and likely crypto processing zones inside the building.Step 4: Correlate signal maps with time-of-day crypto operations for targeted attacks later.Step 5: Identify vulnerable PQ key exchange times to deploy secondary attacks.
- **Detection**: Passive RF scan alerts
- **Solution**: Limit emissions; use Faraday rooms
- **Tags**: ai, sdr, heatmap, pq-analysis

## AI-assisted Packet Shaping Detection on Post-Quantum VPNs

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ-enabled VPN Clients
- **Vulnerability**: Predictable shaping behaviors
- **MITRE**: T1040, T1600
- **Impact**: Fingerprints PQ traffic
- **Tools**: Wireshark, Deep Learning Classifier (PyTorch), Python Scripts
- **Scenario**: Detecting and profiling PQ-VPN traffic via Wi-Fi using AI to identify deliberate padding and traffic shaping.
- **Attack Steps**: Step 1: Set Wi-Fi adapter to monitor mode and capture encrypted traffic of the target PQ VPN client.Step 2: Focus only on packet sizes, frequency, burst patterns—no need to decrypt.Step 3: Train an AI model to distinguish between PQ VPN and traditional VPN patterns.Step 4: Use classifier to flag PQ-VPN traffic and analyze shaping strategy (e.g., constant-length or randomized).Step 5: Determine shaping weakness and target moments when actual payload leaks occur.
- **Detection**: Traffic baseline deviation
- **Solution**: Obfuscate shaping with randomness
- **Tags**: pqvpn, ai-traffic, packet-shaping

## AI-Guided RF Timing Reconstruction in Lattice-based PQ Devices

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Lattice-based PQ Routers
- **Vulnerability**: Unintentional RF timing jitter
- **MITRE**: T1595.002, T1040
- **Impact**: Enables fault-based key recovery
- **Tools**: RTL-SDR, RNN Timing Predictor, Scikit-learn, GNURadio
- **Scenario**: Using AI to detect subtle timing shifts in radio signals caused by lattice-based encryption processes.
- **Attack Steps**: Step 1: Use an RTL-SDR device to record raw RF signals from a lattice-PQ router or device.Step 2: Record signals during idle, regular, and encrypted transmissions.Step 3: Train an RNN to learn timing "signatures" of lattice crypto, focusing on millisecond-level jitter.Step 4: Compare live traffic against model to identify exact time of crypto usage.Step 5: Plan precise timing-based fault injection or key inference techniques.
- **Detection**: RF jitter analytics
- **Solution**: Implement constant-time crypto
- **Tags**: ai, timing, rf-lattice, pqc

## AI-aided Side-Lobe Leakage Analysis in RF PQ Transmitters

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: RF-based PQ Transmitters
- **Vulnerability**: Side-lobe RF emissions
- **MITRE**: T1600, T1595
- **Impact**: Identifies timing of key exchange
- **Tools**: SDR Array, CNN (TensorFlow), Spectrum Analyzer
- **Scenario**: AI-driven detection of side-lobe RF signals generated during PQ encryption transmissions.
- **Attack Steps**: Step 1: Surround a PQ transmitter with multiple SDR antennas in a circular configuration.Step 2: Capture RF emissions from all directions during various states (idle, handshake, encrypt).Step 3: Train a convolutional neural network to identify side-lobe emissions unique to encryption phases.Step 4: Use side-lobe patterns to determine which RF bursts carry key exchange events.Step 5: Correlate with encryption cycles to infer potential leakage windows.
- **Detection**: 360° RF signal capture
- **Solution**: Shield RF components; use directional antennas
- **Tags**: ai, sdr-array, pq-rf, side-lobe

## AI-assisted Anomaly Detection in Mesh PQ Wireless Nodes

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Zigbee Mesh PQ Devices
- **Vulnerability**: Unsecured routing metadata
- **MITRE**: T1592.002, T1595
- **Impact**: Detects crypto events without decrypting
- **Tools**: Mesh Analyzer, Autoencoder AI, Zigbee Sniffer
- **Scenario**: Identifying abnormal traffic in a mesh of PQ IoT devices using AI anomaly detection.
- **Attack Steps**: Step 1: Deploy passive sniffers to monitor mesh network behavior across multiple PQ-enabled IoT nodes.Step 2: Record routing paths, frequency of hops, transmission delays.Step 3: Train an autoencoder-based AI to learn normal patterns.Step 4: Detect deviations that indicate crypto key rotation or PQ handshake failures.Step 5: Use anomaly timing to trigger deeper probes or physical access attempts.
- **Detection**: Anomaly-based mesh monitoring
- **Solution**: Secure routing; obfuscate paths
- **Tags**: ai, mesh, anomaly, pq-network

## Quantum Traffic Behavior Modeling using AI and Wi-Fi Metadata

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wi-Fi PQ Devices
- **Vulnerability**: Predictable broadcast cycles
- **MITRE**: T1040, T1595.002
- **Impact**: Enables timed surveillance
- **Tools**: Wi-Fi Sniffer, AI Time Series Predictor, Scikit-learn
- **Scenario**: Building predictive models of PQ communication routines based on broadcast timing and packet length.
- **Attack Steps**: Step 1: Capture beacon and broadcast packets from suspected PQ devices.Step 2: Extract metadata like beacon intervals, packet size variance, and signal strength.Step 3: Build a time series model using AI (e.g., LSTM) to predict periodic behaviors.Step 4: Identify unusual spikes which may indicate cryptographic handshakes.Step 5: Use these windows for focused traffic or physical interception.
- **Detection**: Pattern-based beacon analysis
- **Solution**: Randomize beacons; introduce noise
- **Tags**: pqc, wifi, ai-timing, prediction

## AI-based Man-in-the-Middle Simulation using RF Replay

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ Key Exchange Systems
- **Vulnerability**: Predictable retry logic
- **MITRE**: T1557.002, T1595.002
- **Impact**: Exploits retries in key exchange
- **Tools**: HackRF, RF Replay Toolkit, AI Sequence Model
- **Scenario**: AI predicts PQ key retransmission patterns, enabling precise RF replay at key intervals.
- **Attack Steps**: Step 1: Record RF packets between two PQ devices performing key exchange.Step 2: Use AI to analyze sequence and timing of retransmissions (common in PQ fallback systems).Step 3: Reconstruct likely retry window and build a replay packet library.Step 4: Replay captured packets during retry to simulate MiTM without full compromise.Step 5: Log server/client response for anomalies and fingerprint failure behaviors.
- **Detection**: Retry anomaly detection
- **Solution**: Introduce randomized retry behavior
- **Tags**: ai, replay, rf, pq-exchange

## Voice-Controlled AI-Driven RF Recon in PQ Networks

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Mixed PQ Wireless Networks
- **Vulnerability**: Human-AI interaction speeds recon
- **MITRE**: T1595.002, T1592
- **Impact**: Human-speed recon & filtering
- **Tools**: SDR Drone, AI Voice Assistant (Offline), Signal Classifier
- **Scenario**: Using voice command and AI to dynamically control RF reconnaissance of PQ systems.
- **Attack Steps**: Step 1: Operate a drone-mounted SDR tool in a building with PQ communication nodes.Step 2: Use voice commands to instruct AI model to scan, isolate, or log frequencies.Step 3: AI classifier sorts live signal types (BLE, Zigbee, Wi-Fi) and stores only PQ-targeted ones.Step 4: Voice-activate recording during periods of high signal density (e.g., crypto use windows).Step 5: Review logs offline for PQ protocol characteristics and build attacker recon database.
- **Detection**: SDR signal signature profiling
- **Solution**: Limit signal types, jam drone ops
- **Tags**: voice, ai, drone, pq-recon

## AI-driven Identification of PQ Cryptographic Patterns via Wi-Fi Handshake Timing

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ-enabled Wi-Fi Routers or Clients
- **Vulnerability**: Distinct timing in handshake packet exchange
- **MITRE**: T1040 (Network Sniffing), T1600
- **Impact**: Enables profiling of PQC usage
- **Tools**: Wireshark, Python (Pandas, scikit-learn), AI Regression Model
- **Scenario**: An attacker uses AI to monitor Wi-Fi handshake timings and detect whether a device is using post-quantum cryptographic algorithms.
- **Attack Steps**: Step 1: Set a laptop or Raspberry Pi with a Wi-Fi adapter to "monitor mode" to passively listen to all Wi-Fi traffic.Step 2: Focus only on the handshake process during device connections — this is where key exchanges happen.Step 3: Record timing between packets (milliseconds between each stage of handshake).Step 4: Use a regression model trained on known PQ handshake delays (e.g., PQC TLS vs. classic TLS) to analyze the captured data.Step 5: If timing aligns with PQ signatures (usually slower/more steps), mark the device as PQ-enabled for further cryptanalysis.
- **Detection**: Behavioral timing analysis
- **Solution**: Add dummy timing or use consistent-speed handshake protocols
- **Tags**: ai, pqc, wifi, timing-profiling

## Predictive AI Model to Forecast PQ Key Rotation via Wireless Traffic Patterns

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wireless PQ Systems
- **Vulnerability**: Predictable key lifecycle timing
- **MITRE**: T1595, T1589
- **Impact**: Predicts and targets key transitions
- **Tools**: Wi-Fi/Zigbee Sniffer, Time-Series Forecasting (LSTM), CSV Logging
- **Scenario**: AI is used to predict when a post-quantum key will be rotated in wireless PQ systems based on previous transmission habits.
- **Attack Steps**: Step 1: Capture wireless traffic (e.g., Zigbee, BLE, Wi-Fi) over several days from a PQ-enabled system.Step 2: Log and timestamp packets, focusing on regularity of encryption events (e.g., when encrypted traffic spikes).Step 3: Feed timestamps into a long short-term memory (LSTM) time-series model trained to forecast periodic events.Step 4: AI predicts windows when future PQ key rotations are likely (e.g., every 6 hours).Step 5: Attacker prepares targeted eavesdropping or replay just before predicted rotation for maximum exposure.
- **Detection**: Unexpected periodic traffic
- **Solution**: Add jitter/random delays to key rotations
- **Tags**: ai, key-forecasting, pqc, time-prediction

## AI-Automated Signal Strength Analysis to Map Cryptographic Load in RF PQ Devices

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: RF-enabled PQ IoT Device
- **Vulnerability**: Electromagnetic emission side effects
- **MITRE**: T1592.002, T1040
- **Impact**: Infers PQ crypto events through signal shifts
- **Tools**: SDR (RTL-SDR), AI Analyzer (SciKit-learn), Signal Logger
- **Scenario**: AI monitors RF signal strength variations to detect crypto operations that increase CPU power usage, indirectly modifying signal strength.
- **Attack Steps**: Step 1: Place an SDR device near a PQ-enabled IoT or embedded device (e.g., smart meter).Step 2: Record the strength and fluctuation of its RF signal continuously.Step 3: Train an AI model to learn correlations between RF fluctuation spikes and cryptographic load events (e.g., CPU spike = crypto execution).Step 4: Use live signal data to infer when encryption or key exchange is occurring.Step 5: Trigger focused attacks (e.g., timing or fault injection) exactly during high-load crypto periods.
- **Detection**: RF signal analysis
- **Solution**: Add signal dampening; distribute crypto load
- **Tags**: ai, rf-signal, pqc, cpu-load

## Adversarial AI Injects Noisy Packets to Confuse PQ Protocol Parsers over Wireless

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ Key Exchange via Wireless
- **Vulnerability**: Poor parser validation in PQ protocols
- **MITRE**: T1210, T1557.002
- **Impact**: Causes fallback to insecure crypto
- **Tools**: Packet Injector (Scapy), GAN-based Packet Generator, Wi-Fi Adapter
- **Scenario**: AI generates pseudo-random malformed wireless packets to test parser robustness in PQ implementations.
- **Attack Steps**: Step 1: Capture legitimate wireless packets during PQ key exchange between two devices.Step 2: Use a generative adversarial network (GAN) to mutate fields (length, flags, sequence number) in a way that appears valid but stresses the parser.Step 3: Inject these "semi-valid" packets into the air during next exchange using a packet injection-capable Wi-Fi card.Step 4: Observe whether devices crash, time out, or fall back to insecure modes.Step 5: Log any error-handling behaviors to plan further PQ cryptanalysis or replay.
- **Detection**: Monitor error responses to malformed packets
- **Solution**: Harden protocol parsing and sanitize inputs
- **Tags**: ai, fuzzing, pqc-protocol, wireless

## AI-Enabled Beam Pattern Recognition for PQ Antenna Fingerprinting

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ-enabled Wireless Base Stations
- **Vulnerability**: Unique beam emissions during PQ encryption
- **MITRE**: T1595.002, T1600
- **Impact**: Device fingerprinting and behavior inference
- **Tools**: Directional SDR Array, AI Beam Classifier (CNN), RF Reflector
- **Scenario**: AI is used to recognize unique beamforming patterns of antennas used during PQ crypto transmission.
- **Attack Steps**: Step 1: Place multiple directional SDR receivers around a PQ wireless antenna (e.g., router or base station).Step 2: Log signal amplitude, direction, and phase during PQ crypto transmissions.Step 3: Train a convolutional neural network (CNN) to associate signal shapes with PQ crypto actions (e.g., key generation vs handshake).Step 4: Use the CNN to fingerprint devices based on their beamforming signature.Step 5: Classify targets for further RF surveillance or electromagnetic injection during critical windows.
- **Detection**: Directional RF signal analysis
- **Solution**: Use rotating keys and random beamform delays
- **Tags**: ai, rf, beam-analysis, pq-crypto

## Firmware Backdoor via Infected Zigbee Dongle

- **Attack Type**: Wireless Supply Chain Attack
- **Target**: PQC Crypto Hardware
- **Vulnerability**: Infected firmware with wireless trigger
- **MITRE**: T1195.002 (Supply Chain: Compromised Hardware)
- **Impact**: Full remote access to PQC processor or secure enclave
- **Tools**: Zigbee2MQTT, HackRF, SDR#, Custom Firmware, Kali Linux
- **Scenario**: A compromised Zigbee module used in PQC hardware is exploited via wireless commands to activate a backdoor placed during manufacturing.
- **Attack Steps**: Step 1: Obtain a Zigbee-enabled cryptographic hardware device used in PQC labs.Step 2: Simulate a scenario where the hardware’s Zigbee chip was compromised during supply chain.Step 3: Use HackRF with SDR# to identify Zigbee frequency (usually 2.4GHz band).Step 4: Transmit custom Zigbee packets from Zigbee2MQTT that match the backdoor activation sequence.Step 5: Monitor the device's serial or LED activity for proof of command execution.Step 6: Extract any unauthorized responses or system changes indicating remote control.
- **Detection**: SDR anomaly detection, device telemetry
- **Solution**: Validate firmware with checksum, disable unused Zigbee features
- **Tags**: #Zigbee #PQC #SupplyChainBackdoor

## Bluetooth Driver Exploit in PQC Library Installation via Rogue Peripheral

- **Attack Type**: Wireless Driver Injection
- **Target**: PQC Development Laptop
- **Vulnerability**: Trust in input devices during setup
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Full compromise of PQC environment
- **Tools**: USB Rubber Ducky (BT variant), Bluetooth sniffer, BlueZ stack, MITMproxy
- **Scenario**: A malicious Bluetooth keyboard delivers exploit payload during initial PQC library setup on air-gapped laptops.
- **Attack Steps**: Step 1: Prepare a Bluetooth keyboard emulator (like a programmable Ducky device).Step 2: Embed command injection payload in key sequence that executes silently.Step 3: Pair the rogue device to the target system used for PQC library dev/testing.Step 4: Wait for user to initiate PQC software install or firmware update.Step 5: Trigger payload that opens system shell and downloads malicious library version via secondary wireless link (like tethered LTE dongle).Step 6: Confirm library hash differs from original; inspect logs for command execution.
- **Detection**: Device logs, integrity mismatch alerts
- **Solution**: Use only wired keyboards, verify install hashes
- **Tags**: #Bluetooth #SupplyChain #LibraryInfection

## Wi-Fi Beacon Spoofing to Redirect PQC Update Requests

- **Attack Type**: Wireless Network Spoofing
- **Target**: PQC Update Utility (Laptop or IoT Device)
- **Vulnerability**: Blind trust in wireless SSID and endpoint
- **MITRE**: T1557.001 (Adversary-in-the-Middle: Wireless)
- **Impact**: Remote firmware infection
- **Tools**: Aircrack-ng, Wireshark, FakeAP, Python HTTP Server
- **Scenario**: PQC firmware update tool looks for vendor SSID to download patches; attacker spoofs this SSID to deliver malicious patch.
- **Attack Steps**: Step 1: Analyze PQC hardware firmware update protocol and expected SSID (e.g., "QuantumUpdateNet").Step 2: Use airmon-ng to scan for target SSID and record its beacon properties.Step 3: Set up a fake AP with same SSID and stronger signal using FakeAP.Step 4: Start a malicious HTTP server mimicking vendor’s update endpoint.Step 5: When PQC device connects, deliver infected firmware with added telemetry leak.Step 6: Observe via packet sniffing that device requests and accepts malicious firmware.
- **Detection**: Wi-Fi probe packet monitoring, firmware validation
- **Solution**: Enforce signed updates, avoid wireless firmware fetches
- **Tags**: #WiFiSpoofing #PQC #FakeAP

## RFID Tag Tampering for PQC Device Access Alteration

- **Attack Type**: RFID Access Manipulation
- **Target**: Shipped PQC Hardware
- **Vulnerability**: RFID config embedded during shipping
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Compromised device config pre-delivery
- **Tools**: Proxmark3, RFID Cloner, Tamper-Detection Tool
- **Scenario**: An attacker tampers with RFID-tagged PQC devices (used for quantum hardware shipping) to alter their configuration or unlock hidden debug mode.
- **Attack Steps**: Step 1: Identify PQC hardware inventory items tagged with RFID for shipping logs.Step 2: Use Proxmark3 to clone original tag and analyze data sectors.Step 3: Replace or reprogram tag with configuration that unlocks device debug mode.Step 4: Place altered tag back on device during delivery.Step 5: At destination, the hardware boots with altered config allowing remote debug port access.Step 6: Connect wirelessly (e.g., via BLE) to that debug port and extract cryptographic info.
- **Detection**: RFID scan mismatch, shipping log mismatch
- **Solution**: Use tamper-evident RFID tags, verify config hashes
- **Tags**: #RFID #SupplyChainTampering #QuantumHardware

## Wireless JTAG Bridge to Inject Faulty Instructions in PQC Secure Boot

- **Attack Type**: Wireless Fault Injection
- **Target**: Quantum Bootloader Device
- **Vulnerability**: Hidden wireless debug trigger
- **MITRE**: T1608 (Develop Capabilities: Malware)
- **Impact**: Bypass secure boot, allow malware injection
- **Tools**: JTAGulator, RF Transceiver, GQRX, Antenna Array
- **Scenario**: A hidden wireless JTAG interface is activated via RF signal, allowing PQC hardware bootloader to be overwritten.
- **Attack Steps**: Step 1: Simulate scenario where PQC chip contains a hidden JTAG-over-wireless backdoor.Step 2: Scan RF spectrum near device for known debug trigger frequencies.Step 3: Use RF transmitter to send activation pulse pattern.Step 4: Confirm debug interface is activated (e.g., LED status or UART output).Step 5: Connect via JTAGulator to overwrite secure boot region with known-vulnerable PQC bootloader.Step 6: Reboot device and verify compromised boot path via altered behavior or telemetry beacon.
- **Detection**: Bootloader integrity checks, RF anomaly monitoring
- **Solution**: Disable wireless debug interfaces in final firmware
- **Tags**: #WirelessJTAG #SecureBootBypass #QuantumChip

## Wireless Firmware Injection in PQC IoT Devices via BLE OTA

- **Attack Type**: BLE Firmware Replacement
- **Target**: BLE-enabled PQC Sensor
- **Vulnerability**: Insecure OTA Update Process
- **MITRE**: T1542.001 (Boot or Logon Autostart)
- **Impact**: Cryptographic leakage or device hijack
- **Tools**: nRF Connect, Ubertooth One, BLEah, Custom Firmware Bin
- **Scenario**: A PQC-capable device (e.g., quantum IoT sensor) is configured to accept BLE OTA (Over-the-Air) updates. An attacker uses spoofed BLE beacon to upload malicious firmware.
- **Attack Steps**: Step 1: Identify BLE-enabled PQC device accepting OTA updates.Step 2: Use Ubertooth One to scan and log BLE advertising packets from the device.Step 3: Clone the update signature format using BLEah.Step 4: Modify the firmware with a payload that leaks internal entropy pool or cryptographic constants.Step 5: Rebroadcast BLE update beacon with nRF Connect as if from the official source.Step 6: Device accepts update and reboots into compromised firmware.Step 7: Validate infection by initiating BLE request and analyzing returned data for anomalies.
- **Detection**: BLE OTA hash check mismatch, firmware diffing
- **Solution**: Enforce signed updates only, disable OTA in production
- **Tags**: #BLEOTA #PQCDeviceAttack

## LoRa Injection During Warehouse Transit of PQC Devices

- **Attack Type**: LoRa-based Supply Chain Interference
- **Target**: LoRa-enabled PQC Devices
- **Vulnerability**: Blind Trust in LoRa Config Commands
- **MITRE**: T1195.002 (Compromised Hardware)
- **Impact**: Device boot config tampering
- **Tools**: LoRa Module (SX1278), Arduino, LoRaSniff, Custom Firmware Commands
- **Scenario**: Attacker injects commands via LoRa while PQC devices are in transit, modifying internal configs before final delivery.
- **Attack Steps**: Step 1: Identify that PQC devices transmit or receive LoRa for configuration tracking during warehouse transit.Step 2: Use LoRaSniff to capture transmission frequency and protocol structure.Step 3: Build a malicious Arduino+LoRa payload that issues a hidden debug-enable command.Step 4: Transmit modified payload while the devices are idle in packaging.Step 5: After delivery, test device in lab and notice unauthorized debug interfaces or altered entropy usage.Step 6: Monitor communication logs to confirm unplanned LoRa command execution.
- **Detection**: LoRa traffic analysis, device hash mismatch
- **Solution**: Encrypt config channels, physically isolate in transit
- **Tags**: #LoRaInjection #SupplyChain

## Compromised NFC Tap on PQC Hardware Setup Assistant

- **Attack Type**: NFC Configuration Hijack
- **Target**: PQC Config Workstation
- **Vulnerability**: NFC scripting without confirmation
- **MITRE**: T1556.001 (Input Prompt)
- **Impact**: Unauthorized modification of PQC environment
- **Tools**: NFC Tag Writer, Android Phone, libnfc, Bash Payloads
- **Scenario**: An attacker places a pre-programmed NFC tag near the workstation used to configure PQC devices. The tag modifies environment variables or downloads altered libraries.
- **Attack Steps**: Step 1: Program an NFC tag with a malicious NDEF record that runs a shell command on tap (e.g., opens terminal and downloads a malicious Python PQC library).Step 2: Discreetly place tag on desk or device label.Step 3: When technician configures the device using NFC-enabled tool, accidental tag scan triggers payload.Step 4: Tag opens a terminal or autostarts a hidden install.Step 5: Confirm library is altered and system PATH includes rogue binaries.Step 6: Capture audit logs showing unverified shell execution from NFC source.
- **Detection**: NFC event logs, process audit trail
- **Solution**: Disable NFC during config; scan tags before use
- **Tags**: #NFCAttack #WorkstationSetup

## RFID Spoofing to Redirect PQC Device Authentication in Warehouse

- **Attack Type**: RFID Impersonation
- **Target**: PQC Inventory in Transit
- **Vulnerability**: Lack of inventory verification on chip level
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Replacement with backdoored devices
- **Tools**: Proxmark3, RFID Reader/Writer, Tag Cloner
- **Scenario**: PQC chips stored in bins with RFID tags for access control. Attacker clones tag and swaps chips during loading to insert altered units.
- **Attack Steps**: Step 1: Identify warehouse PQC inventory bins using RFID access gates.Step 2: Clone a valid employee RFID tag using Proxmark3.Step 3: Use the clone to gain physical access to PQC hardware stock.Step 4: Swap several PQC chips with counterfeit chips that have debug interfaces enabled.Step 5: Allow these devices to proceed through normal delivery.Step 6: At endpoint, use BLE or Wi-Fi to connect to debug ports and extract secrets.
- **Detection**: RFID mismatch logs, inventory scans
- **Solution**: Use multi-factor asset tracking
- **Tags**: #RFIDSwap #SupplyChainHardware

## Wi-Fi Pineapple Intercepting PQC Update Scripts

- **Attack Type**: Wi-Fi Rogue AP
- **Target**: PQC Testing Workstation
- **Vulnerability**: Unauthenticated script delivery over Wi-Fi
- **MITRE**: T1557.001 (Adversary-in-the-Middle: Wireless)
- **Impact**: Backdoored update script execution
- **Tools**: Wi-Fi Pineapple, EvilAP, MITMproxy, DNS Spoof
- **Scenario**: PQC testbed pulls update scripts via Wi-Fi from a central server. A rogue AP serves modified update with altered parameters.
- **Attack Steps**: Step 1: Set up Wi-Fi Pineapple as a rogue access point mimicking the target SSID (e.g., "PQCUpdates").Step 2: Set up MITMproxy and DNS spoof to redirect all update script URLs to attacker’s server.Step 3: Create a modified shell script that changes key PQC compiler flags to disable randomness validation.Step 4: PQC testbed connects automatically to rogue AP due to SSID preference.Step 5: Device downloads and runs the update script silently.Step 6: Compile logs show change in entropy behavior; attacker now knows how key generation behaves.
- **Detection**: Proxy logs, script integrity check
- **Solution**: Enforce script signing, disable open Wi-Fi
- **Tags**: #WiFiPineapple #UpdateHijack

## Zigbee Mesh Injection to Override PQC Boot Parameters

- **Attack Type**: Zigbee Protocol Exploit
- **Target**: PQC Embedded Controller
- **Vulnerability**: No Zigbee packet-level validation
- **MITRE**: T1211 (Exploitation via External Remote Services)
- **Impact**: Predictable keygen due to forced entropy sync
- **Tools**: Zigbee2MQTT, Custom Zigbee Frame Builder, Wireshark
- **Scenario**: PQC-powered industrial module uses Zigbee mesh to sync boot configs. Attacker injects custom Zigbee packet into mesh to override boot randomness sources.
- **Attack Steps**: Step 1: Identify Zigbee mesh structure and locate PQC-enabled node (e.g., in manufacturing robot controller).Step 2: Capture boot config sync packets using Zigbee2MQTT sniffer.Step 3: Construct a malicious Zigbee frame with altered entropy settings.Step 4: Broadcast it into the mesh during boot time.Step 5: Device syncs to malicious boot entropy, weakening cryptographic setup.Step 6: Confirm weakened entropy by measuring repeated key patterns.
- **Detection**: Mesh packet inspection
- **Solution**: Validate config with digital signatures
- **Tags**: #ZigbeeMeshAttack #EntropyHijack

## Wireless Signal Replay to Bypass PQC Device Self-Test

- **Attack Type**: Signal Replay
- **Target**: BLE-enabled PQC Chip
- **Vulnerability**: Unauthenticated debug signal stream
- **MITRE**: T1110.003 (Credential Stuffing)
- **Impact**: Supply chain testing bypass
- **Tools**: Ubertooth One, BLE Sniffer, Replay Script, RF Amplifier
- **Scenario**: PQC devices broadcast startup logs over BLE for QA. Attacker replays captured "pass" logs during inspection to mask issues.
- **Attack Steps**: Step 1: Observe BLE debug output from PQC chip during boot.Step 2: Record clean boot logs using Ubertooth One.Step 3: Simulate a faulty device booting with errors.Step 4: Use RF amplifier to replay the clean boot logs to QA tool during test.Step 5: QA system sees the clean replayed signal and passes device.Step 6: Faulty PQC unit enters field deployment with hidden issues.
- **Detection**: BLE fingerprint mismatch, QA desync
- **Solution**: Use encrypted debug logs, timestamp validation
- **Tags**: #BLEReplay #QABypass

## Wireless Keyboard Injection to Modify PQC Compiler Flags

- **Attack Type**: HID Injection
- **Target**: PQC Workstation
- **Vulnerability**: Lack of input validation during compile
- **MITRE**: T1059.001 (Command and Scripting Interpreter)
- **Impact**: Weakened compiled library
- **Tools**: Rubber Ducky (Wireless), Ducky Script, Compilation Logs
- **Scenario**: A rogue wireless keyboard injects malicious flags during compilation of PQC library to weaken key generation.
- **Attack Steps**: Step 1: Prepare Ducky Script to type altered flags into terminal (--disable-checks or --seed=knownval).Step 2: Connect rogue keyboard to PQC workstation during idle period.Step 3: Wait for compile process to begin.Step 4: Script triggers and injects flags in terminal.Step 5: Monitor resulting library hash and cryptographic behavior.Step 6: Confirm generated keys are weak or predictable.
- **Detection**: Compile logs, flag mismatch
- **Solution**: Physical access control, flag whitelist
- **Tags**: #HIDAttack #CompilerAbuse

## Wi-Fi Broadcasted Fake NTP to Alter PQC Timing Entropy

- **Attack Type**: Wireless Time Manipulation
- **Target**: PQC-Embedded NTP Clients
- **Vulnerability**: Unsigned NTP, no time validation
- **MITRE**: T1565.002 (Data Manipulation)
- **Impact**: Reduced entropy, predictable keys
- **Tools**: NTPMITM, Wireshark, DNSSpoof, EvilAP
- **Scenario**: PQC device derives entropy from system clock synced via NTP. Attacker spoofs NTP over Wi-Fi to bias entropy pool.
- **Attack Steps**: Step 1: Set up rogue AP and spoof NTP server (e.g., time.vendor.com).Step 2: DNSSpoof to redirect legitimate NTP requests.Step 3: Serve malicious time with fixed offsets.Step 4: PQC device accepts altered time during entropy generation phase.Step 5: Capture entropy pool and observe patterns or predictability.Step 6: Confirm time-based entropy is skewed.
- **Detection**: NTP sync logs, entropy review
- **Solution**: Use authenticated NTP, local entropy pools
- **Tags**: #WiFiNTP #EntropyManipulation

## BLE Beacon Spoofing to Trigger Legacy PQC Boot Mode

- **Attack Type**: Wireless Beacon Manipulation
- **Target**: PQC Bootloader
- **Vulnerability**: Blind trust in BLE UUID triggers
- **MITRE**: T1542.004 (Boot or Logon Initialization Scripts)
- **Impact**: Firmware downgrade to vulnerable state
- **Tools**: BLEBeacon Spoofer, nRF Connect, BLEAH
- **Scenario**: PQC chips listen for BLE beacon to enter legacy boot mode. Attacker spoofs beacon to trigger legacy mode and exploit older code.
- **Attack Steps**: Step 1: Reverse-engineer BLE beacon UUID and properties used for legacy boot.Step 2: Use nRF Connect to craft a spoofed BLE beacon.Step 3: Broadcast beacon in lab near target PQC chip.Step 4: Chip enters legacy boot mode expecting authorized debug.Step 5: Attacker connects and uploads unsigned legacy firmware.Step 6: Confirm older firmware exposes vulnerable interface or backdoor.
- **Detection**: Boot mode log mismatch
- **Solution**: Disable legacy triggers in final builds
- **Tags**: #BLEBeacon #BootDowngrade

## Wi-Fi Supply Chain Sniffing to Harvest PQC Keys During Initial Boot

- **Attack Type**: Wi-Fi Intercept Attack
- **Target**: PQC IoT Device (in assembly)
- **Vulnerability**: Unsecured first boot network exposure
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Exposure of private keys or seed entropy
- **Tools**: Wireshark, airmon-ng, tcpdump, Pineapple Nano
- **Scenario**: Attacker sniffs Wi-Fi communications from PQC device during first-time boot post-assembly, capturing cryptographic keys if transmitted in plaintext.
- **Attack Steps**: Step 1: Set up a Wi-Fi sniffer near the area where PQC-enabled IoT devices are first powered and connected to internal network.Step 2: Enable monitor mode on the attacker’s laptop using airmon-ng.Step 3: Use Wireshark or tcpdump to capture any unencrypted HTTP/S or MQTT traffic.Step 4: Identify transmissions related to device registration, firmware verification, or entropy sharing.Step 5: Extract plaintext keys or entropy samples that were transmitted insecurely.Step 6: Replay or reuse this data later to compromise the cryptographic process.
- **Detection**: Network traffic auditing
- **Solution**: Ensure encrypted onboarding, isolate boot process
- **Tags**: #WiFiSniffing #PQCKeyLeak

## Exploiting Wireless Sensor Config Updates in PQC Environmental Chambers

- **Attack Type**: Sensor Hijack via RF
- **Target**: Quantum-safe Processor
- **Vulnerability**: Trust in environmental RF sensors
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Forced downgrade of cryptographic state
- **Tools**: RTL-SDR, RFSignalGen, Python RF Script, Temp Emulator
- **Scenario**: PQC hardware often relies on RF environmental sensors (e.g., temperature) to trigger safe modes. Attacker injects fake RF signals to alter logic.
- **Attack Steps**: Step 1: Identify the specific RF spectrum used by PQC temperature/humidity sensors (e.g., 433 MHz or 868 MHz).Step 2: Use RTL-SDR to observe normal data bursts from sensors to the PQC system.Step 3: Create RF bursts mimicking those messages but with extreme values (e.g., high temperature).Step 4: Broadcast these fake readings to trick the PQC device into triggering fallback or bypass cryptographic logic.Step 5: Monitor device logs and sensor readings for evidence of false environment states.Step 6: Analyze downstream effects—such as bypassing secure boot or disabling keygen routines.
- **Detection**: Sensor validation checks
- **Solution**: Use wired sensors or digital signing
- **Tags**: #SensorSpoofing #PQCBypass

## RFID-enabled PQC Inventory Tampering via Wireless Signal Injection

- **Attack Type**: RFID Logic Attack
- **Target**: PQC Device Tagging System
- **Vulnerability**: Blind trust in RFID content
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Poisoned supply with rogue PQC devices
- **Tools**: Proxmark3, RFID Reader, Hex Editor, RFID Emulator
- **Scenario**: Attacker modifies RFID control logic to manipulate inventory authentication of PQC hardware at supplier warehouse.
- **Attack Steps**: Step 1: Clone RFID tag from a real PQC inventory item.Step 2: Use Hex Editor to alter data sectors to impersonate a high-trust device or shipment.Step 3: Replay this modified tag using an RFID emulator near the receiving scanner.Step 4: Trigger warehouse system into accepting counterfeit PQC hardware (e.g., containing malware-loaded PQC chips).Step 5: Monitor inventory system to ensure rogue devices are now in the delivery pipeline.Step 6: At customer site, attacker remotely activates backdoors via BLE or Wi-Fi.
- **Detection**: RFID audit logs, checksum mismatch
- **Solution**: Use cryptographic tags and cross-checking
- **Tags**: #RFIDTampering #PQCInventoryAttack

## BLE-Based Injection of Fake Entropy Into PQC Initialization Routine

- **Attack Type**: BLE Entropy Injection
- **Target**: PQC Bootloader/Keygen Unit
- **Vulnerability**: Blindly accepting external entropy
- **MITRE**: T1608.001 (Subvert Entropy Source)
- **Impact**: Cryptographically weak or predictable keys
- **Tools**: nRF Sniffer, BLEah, Entropy Logger, Custom BLE Payload
- **Scenario**: Attacker connects to PQC system via BLE during entropy pool initialization to introduce known values.
- **Attack Steps**: Step 1: Identify PQC device that accepts entropy over BLE (e.g., for distributed entropy collection).Step 2: Use nRF Sniffer to analyze the format of entropy packets.Step 3: Craft BLE packets with precomputed or weak entropy values using BLEah.Step 4: Broadcast them at boot time when the device pools external entropy.Step 5: Observe that PQC initialization uses attacker’s weak randomness values.Step 6: Try regenerating keys using the injected entropy and validate key match.
- **Detection**: Entropy pool analysis, BLE packet validation
- **Solution**: Disable external entropy sources or validate them
- **Tags**: #BLEEntropyAttack #KeyInjection

## Wi-Fi Beacon Triggered Debug Port Activation in Post-Quantum Module

- **Attack Type**: Covert Debug Backdoor
- **Target**: PQC Embedded Chip
- **Vulnerability**: Wireless-triggered hidden debug mode
- **MITRE**: T1557.002 (Broadcast Traffic Interception)
- **Impact**: Full access to internal firmware via backdoor
- **Tools**: Kismet, FakeAP, Custom Wi-Fi Beacon Script
- **Scenario**: An attacker identifies that a PQC module activates debug mode if it detects a special Wi-Fi beacon signature during boot.
- **Attack Steps**: Step 1: Use Kismet to sniff beacon frames during normal PQC module operation.Step 2: Discover specific beacon SSID + MAC combo that triggers debug mode (e.g., “PQCDebugNet”).Step 3: Set up FakeAP with matching SSID and transmit the beacon continuously near the PQC chip.Step 4: Reboot the PQC module near the rogue beacon.Step 5: Confirm debug UART or JTAG is activated post-boot.Step 6: Connect via terminal and interact with otherwise inaccessible firmware layers.
- **Detection**: Boot log review, unexpected beacon presence
- **Solution**: Burn debug triggers in final firmware
- **Tags**: #WiFiDebugBackdoor #FirmwareAbuse

## Redundant Node Injection via Wireless Relay

- **Attack Type**: Wireless Fault Injection
- **Target**: Quantum Repeater Network
- **Vulnerability**: Weak node verification in mesh-based QKD topologies
- **MITRE**: T0851
- **Impact**: Qubit path corruption, potential key leakage
- **Tools**: GNU Radio, Raspberry Pi with SDR dongle
- **Scenario**: Attacker injects a fake quantum relay node using wireless hardware, exploiting fault-tolerant design to misroute entangled qubits.
- **Attack Steps**: Step 1: Set up a Raspberry Pi with an SDR (Software Defined Radio) dongle and GNU Radio. Step 2: Use GNU Radio to mimic the wireless quantum repeater signal protocol. Step 3: Place the device near a real quantum relay station. Step 4: Broadcast a fake repeater signal that claims to be a valid node with minimal error rates. Step 5: Monitor if neighboring nodes accept it into the fault-tolerant mesh. Step 6: If accepted, begin redirecting qubit paths through the malicious relay.
- **Detection**: Entanglement verification tests show inconsistencies
- **Solution**: Use authenticated quantum node verification; introduce physical fingerprinting
- **Tags**: fault injection, quantum mesh, spoofing, wireless relay

## Wireless Entanglement Disturbance via Targeted Noise Burst

- **Attack Type**: Wireless Noise Injection
- **Target**: Quantum Channel Endpoint
- **Vulnerability**: Exploitable tolerance thresholds for decoherence
- **MITRE**: T1203
- **Impact**: Forces fallback or session abortion
- **Tools**: HackRF One, RF Signal Generator
- **Scenario**: The attacker disrupts fault-tolerant QKD by injecting bursts of wireless RF noise at timing-sensitive entanglement phases.
- **Attack Steps**: Step 1: Identify the entanglement pulse timing using side-channel observation. Step 2: Place RF signal generator near quantum channel endpoint. Step 3: Emit precisely timed RF bursts during qubit entanglement pulses. Step 4: Cause just enough decoherence to be masked by fault tolerance. Step 5: Observe increased error correction overhead. Step 6: Continue subtle disruption until key agreement fails or attacker forces fallback to classical mode.
- **Detection**: Higher-than-normal quantum bit error rate (QBER)
- **Solution**: Adaptive noise filtering, shielding, and stricter QBER abort policies
- **Tags**: decoherence, QBER spike, entanglement disturbance

## Exploiting Wireless Clock Skew to Cause Phase Drift

- **Attack Type**: Wireless Timing Exploit
- **Target**: Quantum Networking Clock Infrastructure
- **Vulnerability**: Tolerance thresholds not calibrated for gradual clock skew
- **MITRE**: T1499
- **Impact**: Invalid key generation or protocol desync
- **Tools**: SDR, Clock Drift Analyzer
- **Scenario**: By injecting wireless signals that subtly affect atomic clock timing, attacker introduces phase drift across quantum nodes.
- **Attack Steps**: Step 1: Identify the local timing references of the quantum system using passive RF sniffing. Step 2: Use SDR to send continuous low-level wireless interference on timing channels. Step 3: Simulate heat or electromagnetic drift to influence atomic clocks. Step 4: Track phase shift across nodes using drift analyzer. Step 5: Observe if fault tolerance masks the initial drift. Step 6: Continue until synchronization breaks or results in invalid entanglement phase measurements.
- **Detection**: Cross-check node timing signatures
- **Solution**: Quantum-level NTP sync and physical shielding
- **Tags**: quantum phase, timing attack, wireless drift

## Wireless Injection of Fabricated Syndrome Data in Fault Correction

- **Attack Type**: Wireless Data Injection
- **Target**: QKD Control Plane
- **Vulnerability**: Lack of strong integrity on error-correction metadata
- **MITRE**: T1609
- **Impact**: Introduces undetected key bias or session failure
- **Tools**: Wi-Fi Pineapple, Custom Script
- **Scenario**: Attacker wirelessly injects fake syndrome data into error-correction routines of fault-tolerant QKD systems.
- **Attack Steps**: Step 1: Identify the Wi-Fi channel used by control plane of QKD system. Step 2: Capture traffic to analyze syndrome correction packets. Step 3: Reconstruct the format of syndrome messages used in quantum error correction. Step 4: Use Wi-Fi Pineapple to inject fabricated syndrome values during the transmission window. Step 5: Ensure injected values are subtle to avoid threshold detection. Step 6: Monitor for key inconsistencies or mismatched reconciliation.
- **Detection**: Syndrome parity mismatch detection
- **Solution**: Use digital signatures on correction data
- **Tags**: quantum syndrome, metadata injection, wireless fault

## Multi-Hop Wireless Entanglement Spoofing in Fault-Tolerant Mesh

- **Attack Type**: Wireless Relay Spoofing
- **Target**: Quantum Mesh Network
- **Vulnerability**: Mesh join authentication bypassed via low-latency spoof
- **MITRE**: T1090
- **Impact**: Causes corruption in distributed QKD trust network
- **Tools**: Two Raspberry Pis with SDR, Mesh Routing Software
- **Scenario**: Using portable wireless nodes, attacker fakes entanglement hops in multi-node fault-tolerant mesh to inject false quantum paths.
- **Attack Steps**: Step 1: Set up two Raspberry Pis configured to act as spoofed quantum nodes with SDR. Step 2: Mimic routing metadata and present fabricated entanglement confirmation messages. Step 3: Join the wireless quantum mesh by responding faster than real nodes. Step 4: Divert entanglement routing through the attacker's mesh path. Step 5: Introduce timing errors to degrade QKD reliability. Step 6: Monitor if legitimate users receive altered keys due to mesh corruption.
- **Detection**: Latency and path audit logs
- **Solution**: Mesh entry whitelist and latency anomaly detection
- **Tags**: wireless mesh, quantum spoof, routing attack

## RF-Induced Memory Fault in Quantum Router

- **Attack Type**: Wireless Fault Induction
- **Target**: Quantum Router Node
- **Vulnerability**: Radiation-unprotected memory elements in routers
- **MITRE**: T1491
- **Impact**: Faulty routing, increased QBER
- **Tools**: RF Signal Injector, Faraday Cage
- **Scenario**: Attacker induces bit-flips in volatile memory of a quantum router node using high-frequency RF pulses during error-correcting cycles.
- **Attack Steps**: Step 1: Identify the physical location of a quantum router node through observation or network maps. Step 2: Set up an RF signal injector device near the node, outside the shielding boundary. Step 3: Use high-frequency pulses (GHz range) targeted at DRAM timing cycles. Step 4: Emit short bursts during the router’s quantum error correction (QEC) processing intervals. Step 5: Observe for anomalous routing or failed correction. Step 6: Repeat injection to cause unrecoverable error masked under fault tolerance.
- **Detection**: Temperature spikes, RAM parity errors
- **Solution**: EM shielding and radiation-hardened quantum control units
- **Tags**: rf memory fault, wireless radiation, qec bypass

## Wireless Spoofing of Quantum State Validation Beacons

- **Attack Type**: Wireless Beacon Spoof
- **Target**: QKD System Validator
- **Vulnerability**: Lack of timestamp and integrity check on beacons
- **MITRE**: T1557
- **Impact**: Acceptance of corrupted quantum states
- **Tools**: SDR, Beacon Cloning Script
- **Scenario**: Attack leverages spoofed state-validation signals to fool fault-tolerant checks into accepting compromised qubit states.
- **Attack Steps**: Step 1: Monitor wireless signals exchanged during qubit state verification using SDR. Step 2: Capture timing and modulation patterns of beacons. Step 3: Clone validation messages and replay them slightly earlier than legitimate source. Step 4: Introduce minor changes to validation payload to embed bias. Step 5: Confirm if the system accepts spoofed beacon due to early arrival. Step 6: Track downstream QKD inconsistencies due to faulty validation.
- **Detection**: Beacon mismatch logs or double-validation alerts
- **Solution**: Use secure timestamps and hashed beacon payloads
- **Tags**: spoofing beacon, state validation hack, early injection

## Wireless Denial of Synchronization Attack

- **Attack Type**: Wireless DoS on Sync Signals
- **Target**: QKD Sync Module
- **Vulnerability**: Sync channel lacks anti-jamming redundancy
- **MITRE**: T1498
- **Impact**: Session failure or protocol fallback
- **Tools**: Jammer, SDR
- **Scenario**: Attacker jams synchronization pulses wirelessly, forcing fault-tolerant QKD to repeatedly restart or abort.
- **Attack Steps**: Step 1: Analyze the frequency and modulation of synchronization pulses used by the QKD control system. Step 2: Place a directional antenna aimed at the control signal path. Step 3: Emit low-power jamming signals to block sync pulse reception. Step 4: Observe how fault tolerance attempts to recover sync via redundancy. Step 5: Continue disruption until QKD session fails due to max retries. Step 6: Log timing of system fallback or timeout.
- **Detection**: Repeated resync logs or timing mismatch
- **Solution**: Frequency hopping or optical backup for sync
- **Tags**: sync attack, wireless dos, qkd abort

## Exploiting Overcorrection Thresholds via Induced Errors

- **Attack Type**: Wireless Fault Amplification
- **Target**: Fault-Tolerant QKD Protocol
- **Vulnerability**: Correction threshold tuned too low
- **MITRE**: T1562
- **Impact**: Key corruption via miscorrection
- **Tools**: HackRF, Low-Noise Generator
- **Scenario**: Attacker injects minimal wireless noise to push error rates just beyond the correction limit, causing the system to overcorrect and misinterpret data.
- **Attack Steps**: Step 1: Monitor the normal quantum bit error rate (QBER) of the QKD system. Step 2: Estimate the threshold beyond which fault tolerance applies stronger correction. Step 3: Emit wireless interference to introduce controlled decoherence just above threshold. Step 4: Observe system overcorrecting and introducing incorrect syndrome data. Step 5: Track key agreement inconsistencies. Step 6: Escalate errors gradually to avoid detection.
- **Detection**: Unexpected QBER drops or parity mismatch
- **Solution**: Use adaptive correction logic with entropy validation
- **Tags**: fault amplification, qber manipulation, overcorrect

## Wireless Tampering with Qubit Loss Notification Frames

- **Attack Type**: Wireless Frame Injection
- **Target**: QKD Error Notification Channel
- **Vulnerability**: No cryptographic auth on metadata
- **MITRE**: T1001
- **Impact**: Key waste, denial-of-service
- **Tools**: Wi-Fi Adapter in Monitor Mode
- **Scenario**: An attacker inserts false “qubit loss” frames into the classical channel, tricking fault tolerance to discard valid keys.
- **Attack Steps**: Step 1: Capture classical error channel using monitor mode on wireless adapter. Step 2: Reconstruct format of QKD qubit loss notification frames. Step 3: Inject spoofed “loss” frames into the communication stream during session. Step 4: Ensure injected frames match timing of real packet structure. Step 5: Observe key negotiation dropping valid data unnecessarily. Step 6: Repeat at intervals to waste key material and force resync.
- **Detection**: Excessive key discard logs
- **Solution**: Authenticate classical control frames
- **Tags**: wireless inject, metadata spoofing, discard logic

## Wireless Bitflip Injection During Syndrome Exchange

- **Attack Type**: Wireless Bitflip Fault Injection
- **Target**: Quantum-Classical Interface
- **Vulnerability**: No ECC/auth on syndrome bits
- **MITRE**: T1006
- **Impact**: Invalid or biased key derivation
- **Tools**: RF Injector, Logic Analyzer
- **Scenario**: Fault-tolerant QKD uses classical error messages to correct data; attacker injects flips into this via timed wireless interference.
- **Attack Steps**: Step 1: Observe syndrome exchange format using packet sniffer. Step 2: Set up a logic analyzer to detect bit encoding at transmission layer. Step 3: Emit short-range RF bursts aligned with syndrome packet timing. Step 4: Flip select bits by targeting EM bursts near the classical receiver. Step 5: Track error correction and verify if invalid key is derived. Step 6: Repeat over multiple sessions to simulate impact.
- **Detection**: Syndrome mismatch or entropy drop
- **Solution**: Encode syndrome over authenticated channel
- **Tags**: syndrome flip, bit fault wireless, QKD ECC abuse

## Wireless Fuzzing of Quantum Error Response Handlers

- **Attack Type**: Wireless Protocol Fuzzing
- **Target**: QKD Protocol Stack
- **Vulnerability**: No fuzz-tested parser on error channel
- **MITRE**: T1211
- **Impact**: Protocol crash or silent data corruption
- **Tools**: Fuzzing Toolkit, Wireshark, SDR
- **Scenario**: Attacker wirelessly fuzzes quantum protocol's fault-handling handlers via malformed frame injection to crash or misbehave.
- **Attack Steps**: Step 1: Sniff protocol-specific wireless exchanges involved in QEC reporting. Step 2: Generate malformed variations of expected error report messages. Step 3: Replay malformed messages wirelessly via SDR. Step 4: Observe crash, hang, or incorrect behavior in error recovery logic. Step 5: Test different encoding combinations and lengths. Step 6: Document effects on key integrity and state.
- **Detection**: Core dumps or unexpected resets
- **Solution**: Harden input parsers with QEC fuzz test suites
- **Tags**: fuzzing qec, malformed syndrome, wireless error testing

## Wireless Entanglement Spoof via Delayed Echo Replay

- **Attack Type**: Wireless Echo Replay
- **Target**: Entanglement Confirm Channel
- **Vulnerability**: Timing margin not authenticated
- **MITRE**: T1640
- **Impact**: Mismatched entanglement, invalid key
- **Tools**: SDR with Delay Buffer
- **Scenario**: Attacker replays old entangled state confirmations with precise delay to fool timing-tolerant QKD sessions.
- **Attack Steps**: Step 1: Record valid entanglement state confirmations between nodes. Step 2: Use an SDR to delay and replay them at a slight offset. Step 3: Exploit tolerance window in protocol’s response time. Step 4: Observe system accepting old responses due to fault margin. Step 5: Induce state mismatch between source and receiver. Step 6: Confirm impact via inconsistent key material.
- **Detection**: Echo timing deviation logs
- **Solution**: Tighten replay window and timestamp sync
- **Tags**: replay attack, delayed state confirm, wireless entanglement spoof

## Wireless Power Analysis on Fault Recovery Timing

- **Attack Type**: Side-Channel Wireless Power Sniffing
- **Target**: QKD Power Emission Profile
- **Vulnerability**: EM leakage from unshielded hardware
- **MITRE**: T1422
- **Impact**: Leakage of internal state, error maps
- **Tools**: RF Sniffer, Spectrum Analyzer
- **Scenario**: Attack observes timing and power bursts of fault recovery logic via RF sniffing to infer internal error events.
- **Attack Steps**: Step 1: Place RF sniffer near QKD node and observe power bursts. Step 2: Use spectrum analyzer to correlate bursts with error correction activity. Step 3: Note timing patterns during normal vs fault-triggered sessions. Step 4: Build model to estimate error state transitions. Step 5: Use insights to predict fault behavior or optimize attacks. Step 6: Compare power bursts to entangled event correlation.
- **Detection**: Power burst logging and session correlation
- **Solution**: Shielding, randomized task scheduling
- **Tags**: wireless power sniff, side-channel timing fault

## Wireless Redundancy Race Exploit in Fault Tolerance

- **Attack Type**: Wireless Redundancy Bypass
- **Target**: Quantum Redundancy Protocol
- **Vulnerability**: Latency-based priority with no auth
- **MITRE**: T1632
- **Impact**: False redundancy acceptance, silent data loss
- **Tools**: Dual SDR Setup, Packet Cloning Tool
- **Scenario**: Attacker sends faster redundant frame than real node, hijacking redundancy-based recovery in quantum mesh.
- **Attack Steps**: Step 1: Clone the redundancy recovery frame format from a real node. Step 2: Use two SDRs to inject the clone milliseconds earlier than real one. Step 3: Repeat at redundancy decision window. Step 4: Force system to accept attacker’s correction over legitimate one. Step 5: Introduce incorrect recovery data to cause state deviation. Step 6: Observe shift in mesh routing or key drift.
- **Detection**: Frame origin checks or latency mismatch
- **Solution**: Enforce frame integrity and origin proofs
- **Tags**: quantum race condition, redundancy spoof, timing exploit

## Wireless Phase Drift Injection via Heat Induction

- **Attack Type**: Wireless Environmental Exploit
- **Target**: Quantum Node Hardware
- **Vulnerability**: Physical environment affects qubit phase stability
- **MITRE**: T1203
- **Impact**: QKD session destabilized due to excessive drift
- **Tools**: Portable IR Heater, Thermal Camera
- **Scenario**: Attacker induces local heating near quantum relay to introduce phase drift errors in the entangled state, masked by fault tolerance.
- **Attack Steps**: Step 1: Place a portable infrared (IR) heater near the quantum node hardware, ideally near exposed optical or superconducting elements.Step 2: Monitor the node using a thermal camera to ensure temperature increases gradually (~2–5°C).Step 3: Observe the optical signal quality and qubit phase changes over time.Step 4: Continue warming until small phase drifts begin causing QKD errors. These will be absorbed at first by fault-tolerant algorithms.Step 5: Escalate heat slightly to increase phase misalignment.Step 6: Measure the point where fault tolerance fails or error correction overhead becomes excessive, leading to aborted sessions.
- **Detection**: QBER gradually increases; thermal sensor anomalies
- **Solution**: Thermal shielding, internal environment monitoring
- **Tags**: thermal attack, quantum drift, phase instability

## Wireless Spoofing of Quantum Mesh Join Requests

- **Attack Type**: Wireless Mesh Spoofing
- **Target**: Quantum Mesh Router
- **Vulnerability**: Join requests not cryptographically authenticated
- **MITRE**: T1090
- **Impact**: Corrupts fault-tolerant routing; possible man-in-the-middle
- **Tools**: SDR with Mesh Protocol Emulator
- **Scenario**: The attacker wirelessly sends fake mesh-join packets pretending to be a legitimate node, corrupting the redundancy-aware quantum mesh topology.
- **Attack Steps**: Step 1: Capture legitimate mesh join requests using SDR while passive sniffing the quantum mesh’s control channel.Step 2: Reverse-engineer the packet format and create a spoofed join request with attacker-controlled identifiers.Step 3: Use SDR to send this fake join request to the mesh during low-traffic periods.Step 4: Confirm that the quantum mesh registers the attacker as a backup or redundant path.Step 5: Begin rerouting some QKD packets through attacker’s spoofed node, creating opportunity to degrade fault tolerance.Step 6: Monitor routing behavior to verify successful injection and observe for performance degradation or key failures.
- **Detection**: Mesh logs show irregular node joins
- **Solution**: Authenticate all mesh join requests with challenge-response
- **Tags**: mesh join spoof, wireless relay corruption, redundancy failure

## Wireless Flip of Redundant Qubit Result Tags

- **Attack Type**: Wireless Metadata Manipulation
- **Target**: Redundant Classical Channel
- **Vulnerability**: Redundancy data not protected by digital signatures
- **MITRE**: T1565
- **Impact**: Causes silent key corruption, bypassing detection
- **Tools**: Wi-Fi Pineapple, Packet Modifier
- **Scenario**: Attacker modifies classical result metadata (e.g., parity check tags) in redundant fault-tolerant messages over Wi-Fi.
- **Attack Steps**: Step 1: Use a Wi-Fi Pineapple or similar tool to enter monitor mode and capture classical packets related to QKD redundancy parity checks.Step 2: Identify the metadata that carries redundant validation results or parity tags.Step 3: Inject crafted packets with flipped bits in parity metadata, mimicking natural bit flips.Step 4: Inject the crafted packet slightly earlier than the authentic one to win race conditions.Step 5: Confirm that the fault-tolerant protocol processes the spoofed tag and accepts corrupted redundancy.Step 6: Observe if this misleads the correction logic and ultimately results in key mismatches.
- **Detection**: Reconciliation audit logs show discrepancies
- **Solution**: Sign and timestamp all redundancy-related metadata
- **Tags**: parity metadata spoof, redundancy injection, race attack

## Inducing Latency Fluctuation in Redundant Channel via Wireless Interference

- **Attack Type**: Wireless Latency Injection
- **Target**: Redundancy Path Control Layer
- **Vulnerability**: Fault logic assumes latency == failure
- **MITRE**: T1498
- **Impact**: Misdirected traffic, degraded key reliability
- **Tools**: SDR, Latency Logger
- **Scenario**: Attacker targets the classical redundancy channel with timed interference to skew latency and break synchronization assumptions in fault-tolerant routing.
- **Attack Steps**: Step 1: Identify the channel used for redundant path selection (typically Wi-Fi or Zigbee for auxiliary QKD control).Step 2: Emit short-duration wireless interference (pulses of 10–50ms) during key moments of control frame exchange.Step 3: Repeat pulses at irregular intervals to artificially increase latency between two valid nodes.Step 4: Observe fault-tolerant mechanism assuming node failure and rerouting traffic via alternate paths.Step 5: Confirm path change and note if fallback introduces security downgrade or higher error rate.Step 6: Record how long interference needs to persist before rerouting occurs.
- **Detection**: Latency monitoring tools detect path shift
- **Solution**: Use multi-metric health check, not just latency
- **Tags**: wireless latency, reroute spoof, fault misdirection

## Spoofed Quantum Reconnect Request Loop via Wireless Relay

- **Attack Type**: Wireless Session Loop DoS
- **Target**: QKD Session Handler
- **Vulnerability**: Reconnect requests not rate-limited or validated
- **MITRE**: T1499
- **Impact**: Causes exhaustion of QKD resources, denial-of-service
- **Tools**: SDR with Scripted Repeater
- **Scenario**: Attacker wirelessly initiates rapid spoofed reconnect signals to fault-tolerant nodes, exhausting session capacity.
- **Attack Steps**: Step 1: Analyze QKD handshake process between nodes and identify reconnect sequence signaling.Step 2: Build a replay script that sends fake reconnect packets via SDR, mimicking source ID of a valid node.Step 3: Send burst of 20–50 reconnect requests with varying fake timing and slight differences in parameters.Step 4: Observe the target node struggling to handle simultaneous reconnects while still maintaining previous session.Step 5: If fault tolerance enables multiple retries, the node may freeze or reset.Step 6: Log session state before and after attack to measure effectiveness and exhaustion level.
- **Detection**: Spike in session state resets and retries
- **Solution**: Limit reconnect attempts per node and require crypto-auth
- **Tags**: reconnect spam, wireless flood, session exhaustion

## Downgrade Attack via Dual-Stack Quantum/Legacy Router

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Dual-Stack Quantum Routers
- **Vulnerability**: Protocol fallback from PQC to legacy
- **MITRE**: T1600 - Protocol Downgrade
- **Impact**: Loss of quantum-level security, possible full network compromise
- **Tools**: Wireshark, Aircrack-ng, hcxdumptool
- **Scenario**: A quantum-safe router supporting both legacy and PQC algorithms is targeted using a Wi-Fi-based downgrade attack, forcing fallback to weak legacy encryption.
- **Attack Steps**: Step 1: Identify router supporting dual-mode (quantum-safe + legacy WPA2).Step 2: Set up Wi-Fi monitor mode using a wireless adapter.Step 3: Capture initial handshake using hcxdumptool.Step 4: Inject disassociation packets to force reconnect.Step 5: During reconnection, block PQC handshake packets using crafted DoS.Step 6: Force router to fall back to WPA2.Step 7: Capture WPA2 handshake and crack using Aircrack-ng.Step 8: Access network using recovered legacy credentials.
- **Detection**: Check for unexpected protocol downgrade in handshake logs
- **Solution**: Disable legacy mode, enforce PQC-only communication
- **Tags**: interoperability, WPA2, PQC downgrade, DoS

## Beacon Spoofing Legacy-Only Signal

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum Wi-Fi Clients
- **Vulnerability**: SSID spoofing with legacy-only support
- **MITRE**: T1557.001 - Adversary-in-the-Middle: Wireless
- **Impact**: Client downgrade, session hijack, data theft
- **Tools**: MDK4, Bettercap, Kali Linux
- **Scenario**: Attacker transmits a spoofed Wi-Fi beacon mimicking a legacy-only network with the same SSID as a PQC-secured network, tricking devices into connecting insecurely.
- **Attack Steps**: Step 1: Scan for target network using airodump-ng.Step 2: Identify SSID and BSSID of PQC-enabled network.Step 3: Use mdk4 to transmit fake beacon with same SSID but legacy WPA2 security.Step 4: Nearby clients auto-connect thinking it’s the known network.Step 5: Intercept traffic using Bettercap.Step 6: Extract sensitive session data or redirect to malicious server.
- **Detection**: Monitor for mismatched BSSID/SSID combinations
- **Solution**: Authenticate based on certificates, disable legacy protocol fallback
- **Tags**: SSID spoofing, Beacon injection, WPA2

## Forced Legacy Handshake via Signal Jamming

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC-enabled Wi-Fi Clients
- **Vulnerability**: RF-level signal disruption
- **MITRE**: T1496 - Resource Hijacking
- **Impact**: Forced fallback, privacy breach
- **Tools**: HackRF, GNURadio, Scapy
- **Scenario**: By jamming PQC handshake signals at the RF level, an attacker forces devices to revert to a legacy fallback protocol over Wi-Fi.
- **Attack Steps**: Step 1: Identify quantum Wi-Fi communication handshake pattern using Wireshark.Step 2: Use HackRF to monitor spectrum and locate handshake signal.Step 3: Deploy GNURadio flowgraph to jam specific PQC frequency.Step 4: Trigger re-handshake from client by deauth attack.Step 5: Client retries handshake, PQC fails due to interference.Step 6: Device switches to WPA2 handshake.Step 7: Capture and crack legacy handshake using Aircrack-ng.Step 8: Rejoin and monitor network using compromised session.
- **Detection**: RF anomaly monitoring, client logs
- **Solution**: Spectrum hardening, use of multiple-channel PQC handshake
- **Tags**: jamming, PQC, signal interference

## Dual-Mode Device Identity Spoofing

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Dual-Mode Clients
- **Vulnerability**: Identity spoofing, MAC clone
- **MITRE**: T1585.001 - Spoofing: MAC Address
- **Impact**: Impersonation of legitimate device, data theft
- **Tools**: Macchanger, Scapy, Wireshark
- **Scenario**: The attacker clones the MAC and device fingerprint of a dual-mode device to trick the network into thinking it’s a trusted legacy-compatible endpoint.
- **Attack Steps**: Step 1: Use airodump-ng to scan for dual-mode devices.Step 2: Capture handshake traffic and note MAC, vendor info, capabilities.Step 3: Use macchanger to spoof same MAC address.Step 4: Recreate device fingerprint using Scapy to mimic advertised protocols.Step 5: Connect to network as a legacy-compatible device.Step 6: Trigger fallback on access point side by broadcasting only legacy protocol support.Step 7: Start MITM session by intercepting data.Step 8: Exfiltrate login and config info.
- **Detection**: Look for duplicate MAC addresses
- **Solution**: Use MAC whitelisting with physical device IDs, reject legacy connections
- **Tags**: MAC spoof, dual-stack, impersonation

## Legacy VPN Tunnel Injection via Rogue AP

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC VPN Clients
- **Vulnerability**: Legacy VPN protocol fallback
- **MITRE**: T1135 - Network Sniffing
- **Impact**: Traffic compromise, privacy loss
- **Tools**: hostapd, Wireshark, OpenVPN (legacy config)
- **Scenario**: A rogue access point mimicking a quantum-safe VPN endpoint is deployed to intercept connections and offer a legacy VPN fallback tunnel (e.g., PPTP) for MITM.
- **Attack Steps**: Step 1: Set up a rogue AP with same SSID as PQC VPN endpoint.Step 2: Configure hostapd with legacy VPN capability (e.g., PPTP or weak IPsec).Step 3: Deploy rogue AP in close proximity to target users.Step 4: Wait for client devices to auto-connect to stronger signal.Step 5: Capture VPN connection request and serve legacy configuration.Step 6: Intercept and log all VPN traffic.Step 7: Replay or analyze traffic offline.Step 8: Exfiltrate sensitive data sent through compromised VPN tunnel.
- **Detection**: Monitor unexpected VPN tunnel protocols
- **Solution**: Enforce PQC-only VPN policies, monitor endpoint behavior
- **Tags**: Rogue AP, VPN fallback, tunnel hijack

## Legacy Cipher Injection in PQC Wi-Fi Exchange

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wi-Fi devices with PQC stack
- **Vulnerability**: Cipher suite manipulation
- **MITRE**: T1600 - Protocol Downgrade
- **Impact**: Breaks confidentiality of PQC-enabled session
- **Tools**: Scapy, Wireshark, Aireplay-ng
- **Scenario**: Attacker injects fake cipher suite advertisement to fool PQC Wi-Fi devices into accepting legacy AES-based handshake.
- **Attack Steps**: Step 1: Use airodump-ng to capture ongoing PQC-based handshake. Step 2: Identify cipher suite negotiation frame (e.g., RSN or vendor-specific element). Step 3: Use Scapy to craft a forged handshake initiation frame that includes legacy cipher suites (e.g., TKIP/AES). Step 4: Inject the forged frame using aireplay-ng. Step 5: Device interprets as preferred cipher and responds with fallback.Step 6: Record legacy handshake and attempt decryption. Step 7: Access encrypted traffic via cracked session key.
- **Detection**: Deep packet inspection, cipher suite analysis
- **Solution**: Enforce strict cipher suite validation, disable legacy suites
- **Tags**: cipher spoof, RSN, PQC Wi-Fi

## Dual-Band Redirection to Legacy AP

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Dual-band Wi-Fi clients
- **Vulnerability**: Band steering misdirection
- **MITRE**: T1496, T1557.002
- **Impact**: Legacy protocol access, phishing or MITM
- **Tools**: Hostapd, Airgeddon, Fluxion
- **Scenario**: Forces client to connect to a 2.4GHz AP (legacy WPA2) instead of the 5GHz (PQC-secured) AP using band steering manipulation.
- **Attack Steps**: Step 1: Survey target dual-band PQC network.Step 2: Clone SSID with rogue AP on 2.4GHz using hostapd.Step 3: Jam 5GHz band using targeted deauth packets (Airgeddon).Step 4: Clients reconnect to 2.4GHz legacy network.Step 5: Capture handshake and redirect DNS to rogue web server.Step 6: Collect credentials or inject malware payloads.Step 7: Log all intercepted communication.
- **Detection**: Detect abnormal band connection or downgrade logs
- **Solution**: Disable legacy bands, enforce 5GHz-only policies for PQC
- **Tags**: 2.4GHz, downgrade, SSID spoof

## QR Code-based Onboarding with Legacy Fallback

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC-ready IoT Devices
- **Vulnerability**: Human-in-the-loop onboarding exploit
- **MITRE**: T1204 - User Execution
- **Impact**: Full device takeover via trust abuse
- **Tools**: QR Code Generator, FakeAP, Wireshark
- **Scenario**: Targets IoT onboarding via QR code, tricks user into connecting to a fake legacy-secured onboarding hotspot.
- **Attack Steps**: Step 1: Identify IoT device supporting QR code onboarding.Step 2: Analyze QR code structure to extract expected SSID and key.Step 3: Generate fake QR code pointing to attacker’s legacy WPA2 AP.Step 4: Print/overlay code in packaging/online listing.Step 5: User scans and connects to rogue AP.Step 6: Attacker simulates onboarding process.Step 7: Capture initial setup credentials and cloud tokens.Step 8: Gain remote access to device.
- **Detection**: Check QR-to-SSID mapping during onboarding
- **Solution**: Use digitally signed onboarding QR codes
- **Tags**: IoT, QR code, WPA2 spoof

## Legacy Probe Request Response Attack

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Legacy-mode-capable clients
- **Vulnerability**: Auto-connect logic flaw
- **MITRE**: T1071.001 - Application Layer Protocol
- **Impact**: Device connection to attacker AP
- **Tools**: Kismet, Airbase-ng, Wireshark
- **Scenario**: Exploits auto-connect behavior of clients sending out legacy probe requests, responding with a fake legacy AP.
- **Attack Steps**: Step 1: Capture probe requests from clients using Kismet.Step 2: Identify requests for legacy networks.Step 3: Set up rogue AP with same SSID using airbase-ng.Step 4: Broadcast legacy WPA2-only beacon.Step 5: Client auto-connects.Step 6: Intercept traffic and analyze unencrypted metadata.Step 7: Extract session cookies or credentials if available.Step 8: Log and replay data in controlled environment.
- **Detection**: Analyze probe request behavior
- **Solution**: Disable auto-connect to known SSIDs
- **Tags**: auto-connect, probe abuse

## PQC-Legacy Translation Layer Abuse

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC-Legacy Interoperable Gateways
- **Vulnerability**: Input validation failure in proxy
- **MITRE**: T1203 - Exploitation for Client Execution
- **Impact**: Bypass PQC protections entirely
- **Tools**: Scapy, tcpdump, Python Socket Scripts
- **Scenario**: An attacker targets the translation proxy layer that bridges PQC and legacy systems to inject malformed packets and force fallback.
- **Attack Steps**: Step 1: Identify network topology where PQC gateway translates to legacy systems.Step 2: Monitor translation packets using tcpdump.Step 3: Craft malformed legacy-compatible handshake response using Scapy.Step 4: Inject crafted response via wireless access point.Step 5: PQC client fails to verify and downgrades to legacy.Step 6: Attacker intercepts decrypted payload in legacy format.Step 7: Replay or manipulate traffic to escalate access.
- **Detection**: Monitor for malformed packets at proxy edge
- **Solution**: Harden translation layers with strict filtering
- **Tags**: PQ proxy, translation hijack

## Fake Firmware Update over Legacy Channel

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: IoT Devices with fallback update modes
- **Vulnerability**: Weak OTA fallback authentication
- **MITRE**: T1542.001 - Firmware
- **Impact**: Full device compromise
- **Tools**: Fake AP, DNS Spoof, Binwalk, Wireshark
- **Scenario**: Devices auto-switch to legacy protocol during low-signal firmware updates — attacker abuses this to serve malicious update.
- **Attack Steps**: Step 1: Monitor OTA firmware update process of PQC IoT device.Step 2: Degrade signal artificially using signal jammer.Step 3: Device falls back to legacy update channel (e.g., HTTP over WPA2).Step 4: Deploy rogue AP mimicking manufacturer.Step 5: DNS spoof firmware URL to attacker server.Step 6: Serve malicious firmware (create with binwalk).Step 7: Device installs update, attacker gains full control.
- **Detection**: Monitor firmware channel integrity
- **Solution**: Use signed PQC firmware over secure channel
- **Tags**: firmware, OTA, fallback

## PQC Device Whitelist Evasion via Legacy Mode

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC Wireless Access Points
- **Vulnerability**: Inconsistent enforcement across protocols
- **MITRE**: T1557 - Adversary in the Middle
- **Impact**: Access policy bypass
- **Tools**: Macchanger, Aircrack-ng
- **Scenario**: Bypasses MAC-based whitelisting enforced only in PQC mode by reconnecting as legacy-only device.
- **Attack Steps**: Step 1: Identify PQC-enabled device enforcing MAC whitelist.Step 2: Monitor accepted MAC addresses using airodump-ng.Step 3: Spoof valid MAC using macchanger.Step 4: Attempt to connect using legacy WPA2 protocol.Step 5: Device accepts due to missing policy enforcement in legacy mode.Step 6: Establish session and inject test payloads.Step 7: Log device response and potential access.
- **Detection**: Compare MAC lists across protocol types
- **Solution**: Enforce MAC policies on all stacks
- **Tags**: MAC bypass, WPA2 vs PQC

## SSID Cloaking for Legacy-Only Devices

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Hidden SSID Legacy Devices
- **Vulnerability**: SSID cloaking mishandling
- **MITRE**: T1036.003 - Named Pipe Impersonation
- **Impact**: Legacy network spoofing
- **Tools**: Kismet, Airdecap-ng
- **Scenario**: Exploits cloaked SSID behavior in legacy devices to target hidden networks using legacy-only mode.
- **Attack Steps**: Step 1: Use Kismet to find hidden SSIDs from legacy-mode clients.Step 2: Analyze traffic for EAPOL handshake.Step 3: Decrypt handshake using airdecap-ng if known key is used.Step 4: Reconstruct cloaked network parameters.Step 5: Clone SSID and set up rogue AP.Step 6: Target other hidden devices expecting legacy security.Step 7: Log and analyze access attempts.
- **Detection**: Unusual hidden SSID behavior
- **Solution**: Migrate to visible PQC SSID
- **Tags**: Hidden SSID, WPA2, legacy only

## Authentication Relay to Legacy Gateway

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC Clients with Legacy Gateways
- **Vulnerability**: Relay attack opportunity
- **MITRE**: T1557.003 - Network Sniffing & Relay
- **Impact**: Full session compromise
- **Tools**: Bettercap, EvilAP, Scapy
- **Scenario**: Performs an authentication relay from PQC client to a legacy gateway, fooling client into accepting insecure session.
- **Attack Steps**: Step 1: Intercept PQC authentication attempt with Bettercap.Step 2: Relay initial request to legacy gateway with modified headers.Step 3: Legacy gateway accepts and issues token.Step 4: Relay token back to PQC client.Step 5: Client proceeds under false security assumptions.Step 6: MITM session established.Step 7: Extract credentials and session info.
- **Detection**: Monitor for mismatched authentication headers
- **Solution**: Use signed authentication tokens tied to PQC channels
- **Tags**: relay, gateway abuse

## Weak Device Pairing in Mixed Quantum Legacy Mesh

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Zigbee mesh networks
- **Vulnerability**: Insecure legacy pairing logic
- **MITRE**: T1600 - Protocol Downgrade
- **Impact**: Unauthorized device access
- **Tools**: Zigbee2MQTT, KillerBee, Scapy
- **Scenario**: Exploits weak pairing of devices in mixed security mesh (e.g., Zigbee) to spoof device identity and join network.
- **Attack Steps**: Step 1: Scan Zigbee mesh with Zigbee2MQTT.Step 2: Identify legacy device accepting new peers.Step 3: Use KillerBee to forge association request.Step 4: Spoof device fingerprint to appear quantum-capable.Step 5: Pair with legacy device, bypassing quantum verification.Step 6: Relay traffic to attacker.Step 7: Use Scapy to craft custom payloads.Step 8: Analyze mesh data and propagate fake data packets.
- **Detection**: Monitor mesh logs for pairing anomalies
- **Solution**: Enforce quantum handshake pairing
- **Tags**: Zigbee, pairing, spoof

## Legacy Responder Replay Attack on PQC Wi-Fi

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC Wi-Fi APs with fallback
- **Vulnerability**: Replay of weak legacy handshakes
- **MITRE**: T1003.001 - Credential Dumping
- **Impact**: Unauthorized session injection
- **Tools**: Wireshark, Aircrack-ng, Scapy
- **Scenario**: The attacker records a successful legacy-mode handshake and replays it to trick the system into authenticating an unauthorized device.
- **Attack Steps**: Step 1: Monitor PQC Wi-Fi devices that support legacy fallback.Step 2: Use Wireshark to capture a successful legacy WPA2 4-way handshake.Step 3: Use Aircrack-ng to identify and save key handshake frames (ANonce, SNonce, MICs).Step 4: Build a fake client using Scapy to replay captured handshake.Step 5: Simulate a new connection using same MAC address and timing.Step 6: Bypass reauthentication due to replayed valid session keys.Step 7: Intercept traffic or inject packets from rogue device.Step 8: Use tcpdump to confirm data capture from victim network.
- **Detection**: Check for handshake replays from same MAC
- **Solution**: Use per-session nonce randomization, disable legacy mode
- **Tags**: replay, WPA2, MIC spoofing

## Side-by-Side SSID Trap for Mixed-Mode PQC Devices

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC-capable client devices
- **Vulnerability**: SSID ambiguity with legacy-only rogue
- **MITRE**: T1557.002 - Rogue Wi-Fi
- **Impact**: Credential theft, MITM
- **Tools**: Hostapd, Bettercap, Fluxion
- **Scenario**: A rogue AP mimics a PQC device’s SSID but operates only in WPA2 mode. Devices accidentally connect due to stronger signal.
- **Attack Steps**: Step 1: Use airodump-ng to identify SSID and BSSID of PQC-secured AP.Step 2: Clone SSID using hostapd but configure it with WPA2 only.Step 3: Boost signal strength using physical proximity or Wi-Fi amplifier.Step 4: Targeted clients automatically connect to stronger rogue AP.Step 5: Use Bettercap to intercept or inject traffic.Step 6: Launch phishing page using Fluxion to collect credentials.Step 7: Log all client activity.Step 8: Disconnect client after credential capture to prevent suspicion.
- **Detection**: Watch for duplicate SSIDs on different BSSIDs
- **Solution**: Enforce certificate-based AP trust
- **Tags**: rogue AP, WPA2 fallback

## PQC BLE Pairing Downgrade in Dual-Mode Devices

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: BLE-enabled PQC IoT Devices
- **Vulnerability**: Fallback from LE Secure Connection
- **MITRE**: T1600 - Protocol Downgrade
- **Impact**: Eavesdropping and device manipulation
- **Tools**: Btlejack, GATTacker, Wireshark
- **Scenario**: Targets Bluetooth Low Energy (BLE) pairing process in dual-mode IoT devices by blocking PQC pairing and forcing legacy STK method.
- **Attack Steps**: Step 1: Use Btlejack to sniff initial pairing attempts.Step 2: Identify when device tries PQC pairing (e.g., using PQC-certified LE Secure Connections).Step 3: Jam pairing frame using BLE jamming tool or timing interference.Step 4: Device retries pairing using legacy STK (Short Term Key) method.Step 5: Use GATTacker to intercept legacy pairing.Step 6: Log key exchange and derive encryption key.Step 7: Intercept future communication between device and controller.Step 8: Optionally, inject fake commands to the BLE device.
- **Detection**: Check pairing method version logs
- **Solution**: Force LE Secure Connections only; reject legacy STK
- **Tags**: BLE, STK fallback, jamming

## Rogue Legacy Mesh Node Injection

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Hybrid Mesh Networks (PQC + legacy)
- **Vulnerability**: Unvalidated route joins
- **MITRE**: T1557 - Adversary in the Middle
- **Impact**: Route poisoning, traffic capture
- **Tools**: OpenThread, Wireshark, Scapy
- **Scenario**: The attacker adds a fake legacy node to a hybrid mesh network to poison route tables and intercept traffic.
- **Attack Steps**: Step 1: Map out mesh topology using OpenThread sniffer.Step 2: Identify mesh nodes still accepting legacy protocols.Step 3: Configure rogue node using same mesh ID and channel.Step 4: Send crafted “Hello” and route advertisement packets using Scapy.Step 5: Other nodes begin routing traffic through rogue node.Step 6: Log and manipulate passing packets.Step 7: Optionally drop or delay certain traffic to disrupt network.Step 8: Observe device behavior to simulate DoS or MITM.
- **Detection**: Compare expected node MACs and signatures
- **Solution**: Only allow PQC-authenticated route updates
- **Tags**: mesh, Zigbee, route poisoning

## Interoperability Layer Scan and Memory Dump

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC APs and Gateways
- **Vulnerability**: Legacy library leakage
- **MITRE**: T1211 - Exploitation for Privilege Escalation
- **Impact**: Memory leak, key theft
- **Tools**: Nmap, Ghidra, BLEah, Wireshark
- **Scenario**: Scans PQC-enabled APs for hidden legacy libraries still running for compatibility, then leaks memory via side-channel BLE or Wi-Fi.
- **Attack Steps**: Step 1: Use Nmap to detect open ports and fingerprint firmware/services.Step 2: Identify presence of legacy libraries or TLS 1.2 fallback handlers.Step 3: Analyze firmware (if accessible) using Ghidra for legacy hooks.Step 4: Connect via BLE/Wi-Fi using BLEah and send malformed input.Step 5: Leak memory content that reveals precomputed keys or session data.Step 6: Dump and parse the memory contents to extract valuable info.Step 7: Replay leaked credentials to gain access to higher-privilege session.Step 8: Document leak sources and develop mitigation for students.
- **Detection**: Memory scan monitoring, firmware audit logs
- **Solution**: Remove unused legacy libraries completely
- **Tags**: BLE side-channel, memory dump

## RF Injection to Desynchronize QKD Messaging

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: QKD-Based Messaging Systems
- **Vulnerability**: Poor RF shielding, unsynchronized fallback handling
- **MITRE**: T0810 (Signal Interference)
- **Impact**: Fallback to classical insecure channel
- **Tools**: SDR (HackRF/USRP), GNURadio, RF Jammer
- **Scenario**: Attacker exploits RF interference to desynchronize QKD-based messaging sessions by interfering with time synchronization between quantum endpoints.
- **Attack Steps**: Step 1: Identify the target devices using Quantum Secure Messaging (QSM) protocols (e.g., BB84 QKD terminals).Step 2: Use a software-defined radio (like HackRF) to scan for synchronization pulses between QKD transmitters and receivers.Step 3: Analyze timing intervals of beacon frames using GNURadio.Step 4: Transmit precisely timed RF interference (noise bursts) to interrupt clock synchronization.Step 5: Confirm messaging desynchronization and fallback to insecure classical channels.
- **Detection**: RF spectrum anomaly detection, time sync checks
- **Solution**: Use directional antennas, RF shielding, authenticated fallback mechanisms
- **Tags**: QKD, RF Injection, Desync Attack, Timing Attack

## Bluetooth Injection to Hijack QSM Mobile Apps

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum Messaging Mobile App
- **Vulnerability**: Weak BLE authentication during pairing
- **MITRE**: T1557.001 (Bluetooth Impersonation)
- **Impact**: Data theft, session hijack
- **Tools**: Bluetooth Sniffer, hcitool, BtleJack, Android Debug Bridge
- **Scenario**: Hijacking secure quantum messaging apps that rely on Bluetooth-based key authentication handshake by injecting rogue keys.
- **Attack Steps**: Step 1: Locate a target using a QSM-enabled mobile app with Bluetooth pairing (e.g., post-quantum mobile messaging).Step 2: Use BtleJack or hcitool to sniff Bluetooth pairing process.Step 3: Identify key exchange packets over BLE and inject rogue packets during pairing.Step 4: Use modified rogue keys to impersonate one of the endpoints.Step 5: Extract messages or manipulate content in transit.
- **Detection**: Bluetooth handshake logs, rogue pairing alerts
- **Solution**: Enforce QR-based pairing, out-of-band key exchange
- **Tags**: Bluetooth, Mobile QSM, Rogue Key Injection

## Zigbee Relay Attack on Quantum IoT Messaging Nodes

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum-IoT Devices (Smart Lock)
- **Vulnerability**: No physical proximity validation
- **MITRE**: T1557.002 (Relay via Wireless)
- **Impact**: Device hijack, access bypass
- **Tools**: Zigbee Sniffer (ZBOSS, KillerBee), 2x Zigbee USB dongles, Laptop
- **Scenario**: Bypassing QSM-based IoT device security (e.g., smart locks) by relaying commands over Zigbee while impersonating a trusted controller.
- **Attack Steps**: Step 1: Identify a smart device (lock, sensor) using Zigbee and supporting quantum-encrypted messaging.Step 2: Use Zigbee sniffer to capture legitimate QSM key authentication.Step 3: Deploy two Zigbee dongles—one near the controller, one near the target device.Step 4: Relay signals with minimal latency to impersonate the controller.Step 5: Unlock or manipulate the device without breaking encryption.
- **Detection**: Behavioral anomaly detection, signal path triangulation
- **Solution**: Use UWB-based distance bounding or quantum proximity proofs
- **Tags**: Zigbee, Relay Attack, Smart Lock

## Wi-Fi Deauthentication to Force QSM Session Reset

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wi-Fi PQC Messaging Devices
- **Vulnerability**: Weakness in session fallback logic
- **MITRE**: T1565.001 (Protocol Downgrade)
- **Impact**: Downgrade to vulnerable session
- **Tools**: aireplay-ng, Wireshark, Pineapple Wi-Fi, Kali Linux
- **Scenario**: Disrupting ongoing quantum secure messaging over Wi-Fi by deauthenticating users, forcing session reinitialization that may revert to legacy protocols.
- **Attack Steps**: Step 1: Identify target devices using QSM over Wi-Fi (e.g., laptops or access points with PQC secure chat).Step 2: Use Wireshark to confirm session establishment and capture MAC addresses.Step 3: Launch deauth attacks using aireplay-ng to disconnect both parties.Step 4: Monitor reconnection behavior—if devices fallback to classical (e.g., TLS) messaging, intercept or modify.Step 5: Log and analyze session reset logs to confirm downgrade.
- **Detection**: Deauth logs, protocol downgrade alerts
- **Solution**: Disable fallback, enforce strict quantum session resume
- **Tags**: Wi-Fi, QSM Downgrade, Deauth Attack

## RFID-Based Spoofing of Quantum Key Cards

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: RFID-Based Secure Messaging Access
- **Vulnerability**: Replayable signals, lack of physical quantum tagging
- **MITRE**: T1557.003 (RFID Spoofing)
- **Impact**: Physical access breach
- **Tools**: Proxmark3, RFID Cloner, Signal Analyzer, EM Shield
- **Scenario**: Cloning and replaying quantum-encrypted keycard signals used for secure message room access using RFID replay attacks.
- **Attack Steps**: Step 1: Identify environment using quantum keycards (e.g., secure comms room).Step 2: Use Proxmark3 to scan and capture RFID signals from a valid card (at range or when presented).Step 3: Analyze signal for quantum-tag characteristics (QKD-tagged or post-quantum encrypted ID).Step 4: Replay signal at access reader to impersonate user.Step 5: Access secure messaging room or system, simulate unauthorized access.
- **Detection**: RFID reader logs, access pattern anomaly
- **Solution**: Use dynamic, non-replayable quantum tags
- **Tags**: RFID, Spoofing, Access Attack

## Side-Channel Leakage via Electromagnetic Eavesdropping

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: QSM Terminals
- **Vulnerability**: EM radiation leakage
- **MITRE**: T1204 (Side-Channel Attack)
- **Impact**: Partial key inference, metadata leak
- **Tools**: EM Probe, Oscilloscope, Faraday Cage, RF Shielding Tools
- **Scenario**: Attacker extracts message timing and key exchange data from QSM terminals via passive EM analysis.
- **Attack Steps**: Step 1: Place a sensitive electromagnetic probe near a quantum messaging device.Step 2: Monitor side-channel EM radiation patterns during message encryption or key negotiation.Step 3: Use oscilloscope to record and visualize variations.Step 4: Analyze waveform patterns for key timing or entropy leakage.Step 5: Correlate EM data with known traffic to extract potential message timing or crypto behavior.
- **Detection**: EM monitoring, anomaly-based waveform analysis
- **Solution**: Use EM shielding, Faraday enclosures
- **Tags**: EM Leakage, Side-Channel, RF Monitoring

## Wi-Fi Evil Twin Attack on PQ Messaging Servers

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ Messaging Wi-Fi
- **Vulnerability**: Weak Wi-Fi auth, no SSID validation
- **MITRE**: T1557.004 (Evil Twin)
- **Impact**: Credential theft, session hijack
- **Tools**: Fluxion, Wireshark, Aircrack-ng, Rogue AP Setup
- **Scenario**: Attacker creates a rogue Wi-Fi AP mimicking a trusted QSM network to intercept credentials.
- **Attack Steps**: Step 1: Scan for the legitimate Wi-Fi SSID used by the PQ messaging server.Step 2: Create a rogue AP with the same SSID using Fluxion or similar.Step 3: Deauthenticate users from real AP to force reconnection.Step 4: Capture handshake or force captive login page for credentials.Step 5: Use credentials to access QSM services and analyze session negotiation.
- **Detection**: MAC-based anomaly detection, multiple AP SSID alerts
- **Solution**: Enforce certificate pinning, MAC whitelisting
- **Tags**: Evil Twin, Wi-Fi Trap, QSM Hijack

## Interfering Quantum Light Transmission in Wireless Optical QSM

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Free-space QSM Devices
- **Vulnerability**: Susceptibility to photonic noise
- **MITRE**: T1583.003 (Optical Channel Attack)
- **Impact**: Session denial, quantum key rejection
- **Tools**: Laser Diode, Light Sensor, IR Modulator, Lens System
- **Scenario**: In optical wireless QKD, attacker introduces artificial light pulses to create interference in QSM signals.
- **Attack Steps**: Step 1: Identify line-of-sight between QKD transmitter and receiver (e.g., free-space optical QSM links).Step 2: Use light sensor to measure transmission strength and frequency of quantum photons.Step 3: Calibrate a low-powered laser to match the wavelength.Step 4: Emit modulated pulses during key exchanges to introduce noise.Step 5: Cause communication to abort or fallback to classical insecure modes.
- **Detection**: Monitor QBER (Quantum Bit Error Rate) thresholds
- **Solution**: Align-based channel filtering, laser anomaly sensors
- **Tags**: QKD, Optical Attack, Free-Space Channel

## Signal Reflection Spoofing for PQ Device Impersonation

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: QSM-Compatible Devices
- **Vulnerability**: Trust in timing-only validation
- **MITRE**: T1584.001 (Signal Replay)
- **Impact**: Unauthorized device spoofing
- **Tools**: RF Reflectors, Parabolic Dish, SDR, Delay Line
- **Scenario**: Attacker captures and reflects QSM initialization signals to impersonate a device.
- **Attack Steps**: Step 1: Monitor quantum device discovery and pairing signals.Step 2: Capture signals using SDR and delay them using signal processing tools.Step 3: Reflect back the same signal with minor delay, imitating a valid device.Step 4: Allow handshake process to proceed with the attacker acting as the other endpoint.Step 5: Relay or record session initialization for future misuse.
- **Detection**: Signal delay detection, endpoint fingerprinting
- **Solution**: Timestamp validation, session challenge-response
- **Tags**: QSM, Replay, RF Reflection

## NFC Injection in QSM Contactless Smartcards

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: QSM Smartcards
- **Vulnerability**: Lack of strict protocol validation
- **MITRE**: T1557.005 (NFC Injection)
- **Impact**: Messaging bypass, access hijack
- **Tools**: NFC Reader, Proxmark3, Android NFC Tools
- **Scenario**: Exploiting QSM NFC smartcards by injecting malformed commands to bypass secure messaging initialization.
- **Attack Steps**: Step 1: Locate target smartcard with PQ messaging ID authentication (e.g., access cards).Step 2: Use NFC reader to interact and extract ATR (Answer to Reset) response.Step 3: Inject non-standard command sequences designed to force fallback logic.Step 4: Capture the system’s reaction and observe if it defaults to classical communication.Step 5: Use card replay to impersonate or access secure messaging zones.
- **Detection**: NFC traffic auditing, smartcard logging
- **Solution**: Hardened firmware, error-state handling
- **Tags**: Smartcard, NFC Exploit, Fallback Attack

## LoRa-Based Key Relay Bypass in Quantum Mesh Messaging

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: LoRa QSM Devices
- **Vulnerability**: Trust in mesh node forwarding
- **MITRE**: T1565.003 (Mesh Interference)
- **Impact**: Communication failure or interception
- **Tools**: LoRa Sniffer, SDR, Mesh Relay, Packet Injector
- **Scenario**: Attacker targets QSM mesh nodes (e.g., LoRa devices) and reroutes key packets to intercept or drop them.
- **Attack Steps**: Step 1: Monitor LoRa mesh network used for quantum secure comms.Step 2: Capture key distribution packets using a LoRa sniffer.Step 3: Deploy a rogue mesh relay node between two valid devices.Step 4: Reroute or delay key packets.Step 5: Cause failure or downgrade to insecure messaging.
- **Detection**: Node trust scoring, mesh audit logs
- **Solution**: Device attestation, path diversity
- **Tags**: LoRa, Mesh, Key Routing Attack

## Zigbee Beacon Spoofing to Hijack Post-Quantum Group Messaging

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Zigbee QSM Devices
- **Vulnerability**: Unverified beacon acceptance
- **MITRE**: T1557.006 (Beacon Injection)
- **Impact**: Message interception, trust poisoning
- **Tools**: KillerBee Toolkit, ZBOSS Sniffer, Zigbee Dongle
- **Scenario**: Attacker spoofs Zigbee group beacons to redirect devices to rogue post-quantum controller.
- **Attack Steps**: Step 1: Capture Zigbee beacons for group controller initiation in QSM network.Step 2: Replay beacon frames with altered controller IDs.Step 3: New devices join rogue group and share keys assuming it’s secure.Step 4: Intercept keys or control messages.Step 5: Simulate fake messages to confuse participants.
- **Detection**: Beacon signature checks
- **Solution**: Group controller validation, key pinning
- **Tags**: Zigbee, Beacon Spoof, PQ Hijack

## Bluetooth-Based Downgrade Attack in Quantum Chat App

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum Chat Mobile App
- **Vulnerability**: Fallback without strong downgrade protection
- **MITRE**: T1562.001 (Protocol Manipulation)
- **Impact**: Message confidentiality breach
- **Tools**: BtleJack, Bluetooth Logger, MITM Proxy
- **Scenario**: Forcing downgrade of quantum-secure Bluetooth-based messaging app to classical mode via handshake manipulation.
- **Attack Steps**: Step 1: Monitor Bluetooth handshake during QSM session setup.Step 2: Intercept initial handshake and inject packets causing negotiation error.Step 3: Observe device falling back to classical mode (e.g., AES-256 instead of PQC).Step 4: Use classic crypto proxy to capture message contents.Step 5: Replay or decrypt captured message traffic.
- **Detection**: Bluetooth handshake anomalies
- **Solution**: Enforce-only mode, disable insecure fallback
- **Tags**: Bluetooth, Downgrade, PQ Messaging

## Drone-Based RF Sniffing of QSM RF Keys in Transit

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: QSM Base Stations
- **Vulnerability**: RF exposure during key exchange
- **MITRE**: T1583.006 (Over-the-Air Key Leak)
- **Impact**: RF signal misuse, weak fallback exposure
- **Tools**: Drone, SDR (HackRF One), Signal Logger, GPS Tracker
- **Scenario**: Drone equipped with RF sniffer captures over-the-air quantum secure key transmission.
- **Attack Steps**: Step 1: Fly drone over campus or testbed where QSM devices are active.Step 2: Use SDR on drone to scan RF frequencies used by QSM devices.Step 3: Log and geo-tag all bursts related to key distribution.Step 4: Replay signals in lab to analyze entropy and patterns.Step 5: Simulate targeted attacks using captured keys (if weak fallback observed).
- **Detection**: Geo-anomaly detection, RF spectrum alerts
- **Solution**: Use directional antennas, key-in-motion hardening
- **Tags**: Drone, SDR, Key Capture, QSM

## Infrared Pulse Injection on Optical QSM Terminals

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Optical QSM Systems
- **Vulnerability**: No IR filtering or hardening
- **MITRE**: T1582.002 (Optical Signal Manipulation)
- **Impact**: QSM disruption, fallback trigger
- **Tools**: IR LED Gun, Timing Controller, Camera, Target Terminal
- **Scenario**: IR pulses from a distance are used to trigger protocol errors in optical QSM terminals.
- **Attack Steps**: Step 1: Observe terminal using IR-sensitive camera to identify optical receiver.Step 2: Align IR LED emitter toward receiver with appropriate lens.Step 3: Pulse modulated IR at specific timing intervals.Step 4: Induce false start conditions or timing violations in quantum protocol.Step 5: Observe system reverting to error-handling or fallback.
- **Detection**: IR beam detection, camera-based intrusion detection
- **Solution**: Use wavelength filters, time-gating in optics
- **Tags**: IR Attack, Optical QKD, Protocol Abuse

## Jamming-Based Denial of Quantum Secure Messaging Service

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: QSM Network Devices
- **Vulnerability**: Lack of robust anti-jamming measures and insecure fallback logic
- **MITRE**: T1499.001 (Jamming DoS)
- **Impact**: Service outage or insecure fallback
- **Tools**: RF Jammer, Spectrum Analyzer, Directional Antenna
- **Scenario**: Attacker uses RF jamming to prevent QSM devices from establishing quantum key agreement, causing repeated session failures and forcing insecure fallback.
- **Attack Steps**: Step 1: Use a spectrum analyzer to identify the exact frequency band used by QSM devices (often in RF or optical spectrum).Step 2: Set up a narrowband RF jammer to target only the identified QSM channel.Step 3: Gradually increase jamming strength until packet loss occurs during key negotiation.Step 4: Observe behavior of QSM terminals—if improperly configured, they may revert to classical key exchange (e.g., RSA).Step 5: Once fallback is triggered, monitor for classical session keys and attempt MITM (man-in-the-middle) or passive interception.Step 6: Stop jamming intermittently to simulate unpredictable network failure.
- **Detection**: Monitor QBER, packet retransmission spikes
- **Solution**: Frequency hopping, QSM-only enforcement, anti-jam filters
- **Tags**: Jamming, Denial, Fallback Trigger

## BLE Advertisement Spoofing for QSM Peer Discovery Poisoning

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Mobile QSM Applications
- **Vulnerability**: No advertisement authentication or MAC address verification
- **MITRE**: T1557.001 (Bluetooth Spoofing)
- **Impact**: Device impersonation and peer poisoning
- **Tools**: BtleJack, BLE Advertiser, Android with nRF Connect
- **Scenario**: Attacker spoofs Bluetooth Low Energy (BLE) advertising packets of QSM-capable peers to mislead discovery and pair with rogue device.
- **Attack Steps**: Step 1: Use BtleJack or nRF Connect app to scan for BLE advertisements from QSM-capable devices.Step 2: Record the advertising structure (UUIDs, service data) from the legitimate peer.Step 3: Re-broadcast this advertisement from a rogue BLE device, changing the MAC address slightly.Step 4: When a QSM peer scans and detects this rogue advertisement, it attempts to pair.Step 5: Complete pairing with the rogue device and simulate the quantum messaging setup.Step 6: Log any exchanged messages or keys and analyze them if fallback crypto is used.
- **Detection**: BLE logs, repeated unknown MAC connection attempts
- **Solution**: Use advertisement signatures and MAC binding
- **Tags**: BLE, Spoofing, QSM Peer Injection

## Exploiting Line-of-Sight Optical Quantum Messaging Links via Reflection

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Free-Space QSM Optical Links
- **Vulnerability**: Vulnerability to physical redirection attacks
- **MITRE**: T1583.004 (Reflected Signal Capture)
- **Impact**: Eavesdropping or protocol failure
- **Tools**: Mirror Array, Light Sensor, IR Receiver, Tripod Mounts
- **Scenario**: Using highly reflective surfaces (mirrors) to bounce and intercept free-space quantum messaging beams, attacker attempts to observe photon states passively.
- **Attack Steps**: Step 1: Identify physical locations where optical QSM links are used (e.g., rooftop to rooftop secure comms).Step 2: Place mirrors strategically to redirect the quantum beam path to a sensor without disturbing the receiver.Step 3: Use high-sensitivity light sensor or IR camera to monitor the reflected signals.Step 4: Record arrival times and beam fluctuations, while avoiding polarization or phase interference.Step 5: Analyze whether QBER (Quantum Bit Error Rate) rises, indicating potential leak.Step 6: Repeat with alternate mirror placements to simulate multiple angles of interception.
- **Detection**: Monitor alignment errors and QBER deviation
- **Solution**: Optical path validation, beam fencing, environment scanning
- **Tags**: Reflection Attack, Free-Space, QKD Interference

## Wi-Fi Probe Request Injection to Disrupt QSM Chat Initialization

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wi-Fi QSM Chat Clients
- **Vulnerability**: Lack of DoS protection during peer discovery
- **MITRE**: T1464.002 (Wireless Channel Flood)
- **Impact**: Denial or downgrade of QSM sessions
- **Tools**: Scapy, Kali Linux, Aireplay-ng, Wireshark
- **Scenario**: By injecting fake Wi-Fi probe requests, attacker overloads QSM messaging clients during peer discovery phase, delaying secure channel creation.
- **Attack Steps**: Step 1: Identify the SSID and channel used by the QSM chat system (e.g., via Wireshark).Step 2: Craft multiple fake probe requests with spoofed MAC addresses using Scapy.Step 3: Broadcast these probe requests rapidly in the target channel.Step 4: QSM chat clients attempt to respond or filter through the excess requests.Step 5: Observe increased latency or failed peer initialization.Step 6: Monitor for fallback messages over legacy TCP or HTTP channels, indicating success.
- **Detection**: Excess probe detection, MAC address entropy analysis
- **Solution**: Peer rate-limiting, probe filter lists
- **Tags**: Wi-Fi Flooding, Probe Injection, PQ Messaging

## Wireless Keystroke Injection to Modify QSM App Settings

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: QSM Desktop Clients
- **Vulnerability**: Insecure wireless peripheral channels
- **MITRE**: T1056.004 (HID Injection)
- **Impact**: Secure mode bypass, covert setting change
- **Tools**: Wireless HID Injector (Rubber Ducky), SDR, Laptop
- **Scenario**: Attacker sends keystrokes wirelessly to a laptop running a QSM app (e.g., via Rubber Ducky dongle) to disable secure mode.
- **Attack Steps**: Step 1: Identify if the target device (e.g., Windows laptop) uses wireless USB keyboard/mouse or unencrypted HID dongle.Step 2: Deploy a wireless HID injection tool like a Rubber Ducky programmed with malicious keystrokes.Step 3: Script the attack to open QSM app settings and navigate to security preferences.Step 4: Insert keystrokes to disable quantum mode or toggle insecure fallback settings.Step 5: Close the window and allow app to run normally while using weaker crypto.Step 6: Monitor app traffic to confirm insecure session is established.
- **Detection**: System logs, unauthorized input audit
- **Solution**: Use encrypted USB, disable HID over RF
- **Tags**: Keystroke Injection, Settings Tampering, QSM Exploit

## Spoofing Quantum Authentication Token via Bluetooth Bridge

- **Attack Type**: Wireless - Bluetooth Spoofing
- **Target**: Quantum-Enabled Wireless Access Device
- **Vulnerability**: Weak authentication bridging in Bluetooth protocol
- **MITRE**: T1557.001
- **Impact**: Unauthorized access to quantum-secured systems
- **Tools**: Ubertooth One, HC-05, Custom BLE App, Laptop
- **Scenario**: Attacker spoofs a legitimate user's quantum token by exploiting insecure Bluetooth bridge used for token communication
- **Attack Steps**: Step 1: Place a Bluetooth sniffer (Ubertooth One) near the user interacting with a quantum-secure device.Step 2: Capture device discovery and pairing signals (especially MAC and service UUIDs).Step 3: Replay pairing attempts from attacker laptop using spoofed Bluetooth identity (same MAC).Step 4: Use a custom BLE app to simulate token handshake mimicking legitimate quantum token timing and sequence.Step 5: If accepted, attacker gains access as the quantum token owner.
- **Detection**: Monitor for MAC address collision or duplicate pairings
- **Solution**: Enforce cryptographic validation at quantum layer, not Bluetooth level
- **Tags**: Bluetooth, Spoofing, Quantum Token, Replay

## Quantum NFC Token Emulation Attack

- **Attack Type**: Wireless - NFC Emulation
- **Target**: NFC-Enabled Quantum Security Device
- **Vulnerability**: Insecure reliance on classical NFC interface for quantum authentication
- **MITRE**: T1557.002
- **Impact**: Physical access bypass
- **Tools**: Android Phone with NFC, NFC Tools Pro, Termux
- **Scenario**: A malicious actor emulates a legitimate user’s quantum cryptographic token using a rooted phone and NFC tools
- **Attack Steps**: Step 1: Observe a user tapping their token to a quantum-secured entry point (e.g., access door).Step 2: Clone NFC token data using the attacker phone in close proximity.Step 3: Use “NFC Tools Pro” to replay the cloned data with matching timing characteristics.Step 4: Mimic quantum state handshake using time-based triggers and predefined responses.Step 5: Access is granted due to incorrect reliance on NFC layer rather than true quantum verification.
- **Detection**: Detect repeated or abnormal NFC UID usage
- **Solution**: Quantum handshake verification should include randomness and physical entropy
- **Tags**: NFC, Clone, Emulate, Quantum, Token

## Wi-Fi Replay Attack on Quantum Token Proxy Server

- **Attack Type**: Wireless - Wi-Fi Replay
- **Target**: Wi-Fi Enabled Quantum Token Proxy
- **Vulnerability**: Token validation server fails to implement nonce or time constraints
- **MITRE**: T1631
- **Impact**: Unauthorized authentication / system access
- **Tools**: Wireshark, Scapy, Kali Linux
- **Scenario**: Attacker replays intercepted Wi-Fi quantum token packets from client to the backend validation server
- **Attack Steps**: Step 1: Place Wi-Fi sniffer near the user device communicating with quantum token validation server.Step 2: Capture handshake packets or encrypted token payloads.Step 3: Analyze packet timing and payload structure.Step 4: Use Scapy to replay the same packets mimicking timing patterns.Step 5: Server accepts replay as legitimate due to poor nonce handling, granting access.
- **Detection**: Monitor duplicate token requests with identical payloads
- **Solution**: Enforce per-request nonce, timestamp, and origin verification
- **Tags**: Wi-Fi, Replay, Packet Injection, Quantum

## Signal Jamming & Replacement of Quantum Token Radio Beacon

- **Attack Type**: Wireless - RF Jamming and Injection
- **Target**: RF-Enabled Quantum Receiver
- **Vulnerability**: Lack of signal origin authentication and timing-based validation
- **MITRE**: T1461
- **Impact**: Token forgery and unauthorized system access
- **Tools**: HackRF One, GNU Radio, Band-pass filter
- **Scenario**: An attacker jams the legitimate quantum token signal and replaces it with a fake one that mimics the expected handshake over a short-range radio
- **Attack Steps**: Step 1: Use HackRF to detect frequency of legitimate short-range quantum token broadcast (e.g., 2.4GHz ISM band).Step 2: Transmit noise to jam original signal for a brief window.Step 3: During silence, inject a fake signal matching the timing, power, and encoding characteristics of a legitimate token.Step 4: Receiver accepts the fake broadcast as the valid token signal.Step 5: Access granted or command executed.
- **Detection**: RF spectrum anomaly detection, directional antenna analysis
- **Solution**: Use directional antennas and quantum-encoded authentication
- **Tags**: RF, Jamming, Injection, Signal Spoof

## Quantum Token Spoof via MAC Address Impersonation in Wi-Fi Mesh

- **Attack Type**: Wireless - MAC Spoofing
- **Target**: Wi-Fi Mesh Quantum Authentication Network
- **Vulnerability**: MAC spoofing with lack of beacon validation
- **MITRE**: T1586.001
- **Impact**: Misidentification of physical token presence
- **Tools**: Aircrack-ng, macchanger, Raspberry Pi, Wireshark
- **Scenario**: Attacker impersonates a quantum token’s MAC on Wi-Fi mesh to spoof token presence and trick proximity-based access systems
- **Attack Steps**: Step 1: Use Wireshark to identify the MAC address of the quantum token communicating over mesh.Step 2: Use macchanger on attacker device to spoof the MAC address.Step 3: Replay traffic patterns or beacon intervals resembling original device.Step 4: Use timing patterns (e.g., beacon intervals) and SSID presence to mimic token's behavior.Step 5: Proximity-based system believes token is present and grants access.
- **Detection**: Monitor for MAC duplication and timing anomalies
- **Solution**: Implement physical-layer fingerprinting or quantum proof-of-presence
- **Tags**: Wi-Fi, MAC Spoof, Token Simulation, Mesh

## BLE Quantum Token Spoof using GATT Profile Emulation

- **Attack Type**: Wireless - BLE Emulation
- **Target**: BLE-Based Quantum Device
- **Vulnerability**: Insecure GATT profile validation, no quantum signature checks
- **MITRE**: T1583.007
- **Impact**: Token forgery and system compromise
- **Tools**: NRF Connect App, Android BLE Peripheral Emulator, Wireshark
- **Scenario**: Attacker mimics the Generic Attribute Profile (GATT) of a legitimate quantum cryptographic token device to bypass authentication
- **Attack Steps**: Step 1: Use BLE sniffer to capture GATT services and characteristics exposed by the real quantum token.Step 2: Analyze UUIDs, value types, and characteristic read/write behaviors.Step 3: On Android phone, launch BLE Peripheral Emulator to replicate these services.Step 4: Advertise identical device name and MAC prefix.Step 5: Victim reader device connects and mistakenly validates attacker’s fake token as authentic.
- **Detection**: Monitor BLE UUID anomalies and MAC spoofing
- **Solution**: Add quantum handshake after GATT pairing
- **Tags**: BLE, GATT Spoof, Token, Emulator

## Quantum Token Downgrade via Wi-Fi Captive Portal Redirection

- **Attack Type**: Wireless - Wi-Fi MITM
- **Target**: Wi-Fi Quantum Auth Gateway
- **Vulnerability**: Lack of enforced quantum-only cryptographic layers
- **MITRE**: T1557.002
- **Impact**: Decryption of quantum credentials using classical fallback
- **Tools**: Wi-Fi Pineapple, EvilAP, Bettercap
- **Scenario**: User is redirected to a fake access point which downgrades token encryption to a legacy fallback system
- **Attack Steps**: Step 1: Set up a rogue access point with same SSID as the legitimate quantum token portal.Step 2: Deauth nearby users to force reconnection.Step 3: Redirect the user to a fake captive portal (identical to the real one).Step 4: Instruct user to “reinitialize token” in degraded mode (RSA or ECC).Step 5: Capture classical token credentials and use them to spoof later sessions.
- **Detection**: Analyze TLS downgrade in portal logs
- **Solution**: Enforce strict quantum protocol handshake only
- **Tags**: MITM, Captive Portal, Downgrade, Wi-Fi

## NFC Token Signal Amplification & Relay Spoof

- **Attack Type**: Wireless - NFC Relay
- **Target**: NFC-based Quantum Authentication
- **Vulnerability**: Relayed authentication without token proximity checks
- **MITRE**: T1021.004
- **Impact**: Proximity-based bypass and token hijack
- **Tools**: Proxmark3, NFC Relay Android App, SDR
- **Scenario**: Attacker uses signal amplification to relay token signals from a distance and bypass proximity restrictions
- **Attack Steps**: Step 1: Set up relay with attacker A near the reader and attacker B near the victim token (e.g., in backpack).Step 2: Capture and relay NFC signals in real-time using Android apps or Proxmark.Step 3: Maintain timing integrity so reader doesn’t detect the delay.Step 4: Reader believes token is nearby and grants access.Step 5: Attacker A gains unauthorized entry while victim is unaware.
- **Detection**: Analyze time delay in NFC transactions
- **Solution**: Use challenge-response with quantum randomness
- **Tags**: NFC, Relay Attack, Amplification, Quantum

## Quantum Token Response Prediction via Signal Timing

- **Attack Type**: Wireless - RF Timing Analysis
- **Target**: RF-Based Quantum Token System
- **Vulnerability**: Predictable quantum token response timing
- **MITRE**: T1595.003
- **Impact**: False token recognition due to timing spoof
- **Tools**: RTL-SDR, Spectrum Analyzer, Python Script
- **Scenario**: Attacker predicts valid token response by analyzing RF signal response times to bypass authentication
- **Attack Steps**: Step 1: Collect multiple successful token interactions using SDR.Step 2: Use spectrum analyzer to track response timing down to microseconds.Step 3: Identify deterministic delays in token response time.Step 4: Simulate a device that responds within the same timing window.Step 5: System accepts the attacker signal due to predictable response latency.
- **Detection**: Monitor timing irregularities and jitter
- **Solution**: Introduce random delays in token RF layer
- **Tags**: RF, Timing Attack, Prediction, Spoof

## Replay of Quantum Token Authentication Over Zigbee

- **Attack Type**: Wireless - Zigbee Replay
- **Target**: Zigbee Smart Lock with Quantum Token Proxy
- **Vulnerability**: Lack of nonce or session freshness in Zigbee implementation
- **MITRE**: T1071.001
- **Impact**: Unauthorized physical access
- **Tools**: Zigbee Sniffer (CC2531), ZBOSS Sniffer Tool, Scapy
- **Scenario**: Zigbee-based smart lock with quantum token relay is fooled using a captured handshake from a previous session
- **Attack Steps**: Step 1: Use CC2531 to passively sniff Zigbee network where token is used.Step 2: Identify successful unlock event and capture packet sequence.Step 3: Replay same packet sequence at a later time.Step 4: Smart lock accepts spoofed sequence due to lack of freshness validation.Step 5: Attacker enters secured area with fake token session.
- **Detection**: Enable per-use tokens and sequence validation
- **Solution**: Zigbee, Replay, Smart Lock, Token Spoof
- **Tags**: Simulated

## Injection of False Quantum Token Over RFID Gateway

- **Attack Type**: Wireless - RFID Injection
- **Target**: RFID Token-Based Quantum Entry
- **Vulnerability**: No physical-layer fingerprinting of tag signals
- **MITRE**: T1203
- **Impact**: Access control failure via forged waveforms
- **Tools**: Proxmark3, RFID Writer, Oscilloscope
- **Scenario**: Attacker injects a forged quantum token ID over RFID by replicating signal waveform of valid tag
- **Attack Steps**: Step 1: Use Proxmark3 to clone legitimate token’s waveform signature.Step 2: Record amplitude, modulation, and duration of authentication signal.Step 3: Reproduce signal using signal generator or RFID writer.Step 4: Present fake token near RFID quantum gateway.Step 5: Gateway accepts signal as valid due to poor waveform verification.
- **Detection**: RF waveform comparison with baseline templates
- **Solution**: Introduce quantum fingerprinting layer post-RFID
- **Tags**: RFID, Injection, Signal, Quantum Token

## Drone-based Relay of Quantum Tokens Over Shortwave RF

- **Attack Type**: Wireless - Remote Relay via Drone
- **Target**: Quantum Token System with Location Assumption
- **Vulnerability**: Insecure assumption of physical proximity
- **MITRE**: T1021.006
- **Impact**: Bypass of location-based authentication
- **Tools**: Drone, SDR, Directional Antenna, Raspberry Pi
- **Scenario**: A drone relays quantum token traffic from a target location to a remote attacker device in real time
- **Attack Steps**: Step 1: Equip drone with SDR and microcontroller for relay.Step 2: Hover drone near location of quantum token (e.g., lab, warehouse).Step 3: Capture token handshake and relay it over extended RF to attacker.Step 4: Attacker device mimics proximity using relayed data.Step 5: Target system grants access to attacker due to false presence.
- **Detection**: Directional signal triangulation, flight path logs
- **Solution**: Use quantum token with GPS validation & challenge
- **Tags**: Drone, Relay, Proximity Spoof, RF

## Side-Channel Signal Leakage from Quantum Token Antenna

- **Attack Type**: Wireless - Side-Channel RF Analysis
- **Target**: Quantum Token Device with RF Antenna
- **Vulnerability**: Electromagnetic leakage revealing operational data
- **MITRE**: T1200
- **Impact**: Key leakage via side-channels
- **Tools**: HackRF One, Side-Channel Analyzer, MATLAB
- **Scenario**: Attacker deduces token secrets by measuring unintended RF emissions during authentication
- **Attack Steps**: Step 1: Monitor RF leakage while token authenticates.Step 2: Analyze side-channel noise and emissions patterns.Step 3: Use machine learning to correlate emissions to specific operations or keys.Step 4: Replicate similar emissions with spoofing device.Step 5: Target system accepts attacker due to mimicked RF leakage signature.
- **Detection**: Monitor ambient emissions during operations
- **Solution**: Shielded token design with randomized pulse timing
- **Tags**: RF, Side-Channel, Emissions, Leakage

## Inductive Coupling to Hijack Quantum Token Signal

- **Attack Type**: Wireless - Inductive Interference
- **Target**: Inductive Quantum Token Transmitter
- **Vulnerability**: Poor shielding and signal tamper protection
- **MITRE**: T1495
- **Impact**: False token response, device spoofing
- **Tools**: Induction Coil, Signal Amplifier, EM Pulse Emitter
- **Scenario**: Attacker generates a nearby EM field to manipulate token transmission via inductive coupling
- **Attack Steps**: Step 1: Identify location and frequency of quantum token emissions.Step 2: Use induction coil to couple EM energy to token transmission line.Step 3: Alter data encoding on-the-fly by injecting modulated interference.Step 4: Target system receives altered token signal.Step 5: Attacker’s own device completes handshake as if token responded.
- **Detection**: Monitor signal distortion and power levels
- **Solution**: Shield RF path and implement EM-hardening
- **Tags**: Inductive, Signal Hijack, Coupling, Spoof

## Bluetooth Mesh Token Collision Attack

- **Attack Type**: Wireless - Mesh Collision
- **Target**: Bluetooth Mesh Quantum Framework
- **Vulnerability**: Lack of collision mitigation in mesh handshake logic
- **MITRE**: T1499
- **Impact**: Spoofed token wins authentication arbitration
- **Tools**: Bluetooth Mesh Simulator, Kali Linux, Python Script
- **Scenario**: Multiple fake tokens flood mesh network creating collision and race conditions in quantum handshake timing
- **Attack Steps**: Step 1: Create multiple spoofed Bluetooth mesh nodes.Step 2: Send overlapping authentication requests with fake quantum signatures.Step 3: Exploit race conditions in mesh token arbitration logic.Step 4: System validates the wrong (attacker) token due to timing collision.Step 5: Access granted or logic manipulation achieved.
- **Detection**: Monitor for rapid join/disjoin cycles
- **Solution**: Add transaction ID & random delay logic
- **Tags**: Bluetooth, Mesh, Collision, Race Condition

## Fake Quantum Token via Wi-Fi Beacon Injection

- **Attack Type**: Wireless - Beacon Injection
- **Target**: Wi-Fi Quantum Token Auth Gateway
- **Vulnerability**: Token recognition based solely on SSID and beacon presence
- **MITRE**: T1583.006
- **Impact**: Unauthorized access or handshake hijack
- **Tools**: Wireshark, Airbase-ng, Scapy, Kali Linux
- **Scenario**: Attacker crafts malicious beacon frames simulating a quantum token’s presence on a Wi-Fi network, triggering false validation
- **Attack Steps**: Step 1: Use Wireshark to capture beacon frames broadcasted by the real quantum token device on Wi-Fi.Step 2: Extract SSID, BSSID, beacon interval, and supported capabilities from the legitimate token device.Step 3: Launch Airbase-ng or Scapy script to inject beacon frames mimicking the token's identity.Step 4: Ensure beacon intervals and timestamps match the real token.Step 5: Target system recognizes spoofed beacon as a trusted token and begins authentication with attacker.Step 6: Attacker completes handshake with generic response or delays it to simulate quantum randomness.
- **Detection**: Monitor beacon flood anomalies and duplicate BSSIDs
- **Solution**: Enforce quantum handshake with signature verification
- **Tags**: Beacon, Wi-Fi, Token Spoofing, Injection

## Passive Audio Leakage of Quantum Token Handshake

- **Attack Type**: Wireless - Acoustic Side-Channel
- **Target**: Desktop Quantum Token Device
- **Vulnerability**: Audio emissions not shielded; predictable sound patterns
- **MITRE**: T1592
- **Impact**: Acoustic leak-based token impersonation
- **Tools**: High-sensitivity microphone, Audacity, Python Audio Toolkit
- **Scenario**: Attacker records the sound emissions of a quantum token’s handshake process to replicate timing and sequence for spoofing
- **Attack Steps**: Step 1: Place a directional microphone near the target during token operation (e.g., on a table or access point).Step 2: Record multiple authentication handshakes for 10–15 minutes.Step 3: Use Audacity or Python to visualize waveform spikes corresponding to quantum challenge-response cycles.Step 4: Extract timing and pulse patterns from sound data.Step 5: Build a fake token device (Raspberry Pi or microcontroller) to emit same acoustic or electromagnetic pulses with identical timing.Step 6: Present spoofed signal to access system, which interprets it as valid due to matching temporal profile.
- **Detection**: Sound pattern baseline deviation detection
- **Solution**: Implement acoustic shielding and randomized timing
- **Tags**: Side-channel, Acoustic, Timing Attack, Spoof

## Dual-Signal Injection on NFC-Based Quantum Entry

- **Attack Type**: Wireless - NFC Collision Attack
- **Target**: NFC Entry Systems with Quantum Token Back-end
- **Vulnerability**: Poor handling of simultaneous token collisions
- **MITRE**: T1557.003
- **Impact**: Authentication redirection or bypass
- **Tools**: Proxmark3, NFC Antenna, Collision Test Script
- **Scenario**: Two NFC devices (attacker and real token) simultaneously interact with a reader, causing confusion that leads to spoof acceptance
- **Attack Steps**: Step 1: Position the attacker’s NFC antenna near the access reader, close to the real user token.Step 2: Time the fake token to respond microseconds before the real one (based on protocol timings).Step 3: Inject pre-crafted partial token response to “pre-fill” the buffer of the NFC reader.Step 4: The reader begins validating based on the attacker’s input and ignores or drops the real token’s response.Step 5: Access is granted to attacker.Step 6: Real user is unaware their token was overridden.
- **Detection**: NFC timing error logging and detection of dual signals
- **Solution**: Use time-synchronized challenge that’s uniquely tied to quantum layer
- **Tags**: NFC, Collision, Race Condition, Spoof

## Quantum Token Impersonation using Thermal Emission Profiling

- **Attack Type**: Wireless - Infrared/Thermal Profiling
- **Target**: Quantum Token with Thermal-based Presence Verification
- **Vulnerability**: Blind trust in thermal signature without cryptographic confirmation
- **MITRE**: T1200
- **Impact**: Unauthorized presence emulation
- **Tools**: FLIR Thermal Camera, Raspberry Pi with heating element, Python Thermostat Script
- **Scenario**: Attacker records thermal profile of token interaction to simulate presence using a dummy device with similar heat signature
- **Attack Steps**: Step 1: Observe real token being used near target device (e.g., access panel).Step 2: Use FLIR camera to measure thermal emission over time during handshake (temperature curve, decay rate).Step 3: Note the duration and intensity of IR radiation corresponding to successful authentication.Step 4: Build attacker device that emits same IR profile using heating element and timed control script.Step 5: Present spoofed thermal signature to access point's thermal detection module.Step 6: System assumes presence of real token and initiates session.
- **Detection**: Compare thermal shape with token serial patterns
- **Solution**: Add cryptographic check tied to physical layer signature
- **Tags**: Thermal, Spoof, IR, Profile Attack

## Bluetooth Long-Range Injection for Remote Token Spoof

- **Attack Type**: Wireless - Long-Range Bluetooth Injection
- **Target**: BLE-Based Quantum Token Access Device
- **Vulnerability**: Acceptance based only on MAC and UUID presence
- **MITRE**: T1585.003
- **Impact**: Remote access without presence of token
- **Tools**: Long-range BLE Adapter, Yagi Antenna, Bluetooth Frame Injector
- **Scenario**: Using directional antennas and signal boosters, attacker injects spoofed BLE frames from outside the premises to impersonate a quantum token
- **Attack Steps**: Step 1: Identify BLE frequency and advertising channel used by target quantum token.Step 2: Use a Yagi antenna and a long-range BLE adapter to test signal reach to the access point.Step 3: Craft BLE advertising frames that match token’s MAC, name, and UUIDs.Step 4: Transmit spoofed BLE frames from a distant rooftop or vehicle.Step 5: Target access point receives fake frames and believes token is in proximity.Step 6: Handshake completes if system doesn’t validate signal strength or physical proximity.
- **Detection**: Signal triangulation and BLE RSSI pattern analysis
- **Solution**: Enforce minimum RSSI and movement-based handshake validation
- **Tags**: BLE, Long-Range, Directional Attack, UUID Spoof

## Wi-Fi Entropy Side-Channel Exploit

- **Attack Type**: Wireless Attack via Entropy Monitoring
- **Target**: PQ-enabled IoT Device
- **Vulnerability**: Entropy Reuse + Side-Channel Leakage
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Partial Key Exposure
- **Tools**: Wireshark, ESP32 Sniffer, Side-Channel Logger
- **Scenario**: Attacker uses Wi-Fi proximity access to observe timing and energy patterns during key generation in post-quantum crypto hardware using reused entropy
- **Attack Steps**: Step 1: Place an ESP32-based Wi-Fi sniffer near the PQ crypto device (e.g., laptop, router with PQ update).Step 2: Start monitoring Wi-Fi energy fluctuations and channel timings during PQ key generation.Step 3: Repeated key generation with reused entropy shows timing consistency.Step 4: Extract timing patterns and match against public key values to infer bit positions.Step 5: Reconstruct partial or full secret key using timing correlation and leakage models.
- **Detection**: Anomalous timing during crypto operations
- **Solution**: Use hardware entropy generator, prevent key regeneration loops
- **Tags**: wireless, entropy, PQC, timing attack

## BLE Key Reuse Profiling

- **Attack Type**: Wireless BLE Attack
- **Target**: BLE-enabled PQ Device
- **Vulnerability**: Key Reuse in BLE PQ Handshakes
- **MITRE**: T1557.003 (Adversary-in-the-Middle: Bluetooth)
- **Impact**: Session Hijack
- **Tools**: nRF Sniffer, BLEah, GATTacker
- **Scenario**: An attacker profiles key reuse patterns in BLE-based authentication in a PQC testbed using similar session randomness
- **Attack Steps**: Step 1: Identify a BLE-enabled PQ communication device (e.g., secure wearable prototype).Step 2: Capture multiple pairing attempts using nRF Sniffer.Step 3: Analyze similarity in handshake payloads.Step 4: Detect key reuse patterns by comparing session keys and response similarities.Step 5: Reconstruct keys or exploit known values for spoofing session.Step 6: Replay or MITM the connection.
- **Detection**: BLE handshake similarity logs
- **Solution**: Rotate session keys per use, increase entropy pool
- **Tags**: BLE, PQC, key reuse, wireless, replay

## Zigbee Key Stream Reuse Attack

- **Attack Type**: Zigbee Wireless Replay Exploit
- **Target**: PQ-enabled Zigbee Device
- **Vulnerability**: Ciphertext Reuse with Identical Stream
- **MITRE**: T1420 (Encrypt Network Traffic)
- **Impact**: Message Injection / Replay
- **Tools**: KillerBee, zbSniffer, Scapy
- **Scenario**: A poorly implemented PQC Zigbee stack reuses the same encryption key stream during multiple transmissions
- **Attack Steps**: Step 1: Identify PQ-enabled Zigbee sensor network (e.g., smart meters or smart switches).Step 2: Use zbSniffer to capture multiple encrypted Zigbee transmissions.Step 3: Detect identical ciphertext blocks indicating key stream reuse.Step 4: XOR two ciphertexts with same key stream to recover plaintext.Step 5: Inject crafted messages using replay or partial key guess.Step 6: Trigger unauthorized command or state manipulation.
- **Detection**: Zigbee payload XOR analysis
- **Solution**: Use nonce per message and key rotation
- **Tags**: zigbee, PQC, replay, key reuse, IoT

## Fast-Transition Replay on PQ Wi-Fi

- **Attack Type**: Wi-Fi 802.11r Key Replay
- **Target**: PQC-enabled Wi-Fi AP/Client
- **Vulnerability**: 802.11r Key Derivation Reuse
- **MITRE**: T1557.002 (Adversary-in-the-Middle: Wi-Fi)
- **Impact**: Unauthorized Access
- **Tools**: hcxdumptool, Aircrack-ng, Wireshark
- **Scenario**: Exploiting 802.11r (fast roaming) in PQ Wi-Fi networks where key derivation is reused during transitions
- **Attack Steps**: Step 1: Setup attacker laptop with hcxdumptool near the roaming PQ Wi-Fi network.Step 2: Capture fast BSS transitions between APs.Step 3: Look for reuse of cryptographic material in fast-transition handshake.Step 4: Replay earlier handshake to trick AP into granting access.Step 5: If successful, hijack session or inject malicious packets.Step 6: Analyze packets to extract entropy reuse pattern.
- **Detection**: Handshake sequence review
- **Solution**: Force unique session derivation per roam
- **Tags**: wifi, PQC, 802.11r, key reuse, replay

## NFC Entropy Collision on PQ Pairing

- **Attack Type**: NFC-Based Entropy Reuse Attack
- **Target**: NFC-enabled PQ Auth Device
- **Vulnerability**: Poor entropy in NFC handshakes
- **MITRE**: T1110.003 (Brute Force: Credential Stuffing)
- **Impact**: Predictive Key Derivation
- **Tools**: NFC reader, proxmark3, entropy analyzer script
- **Scenario**: An attacker targets NFC key exchange protocol on a PQ-enabled authentication device reusing poor entropy
- **Attack Steps**: Step 1: Place Proxmark3 near PQ-enabled NFC device (e.g., badge reader or mobile payment prototype).Step 2: Initiate multiple pairing/communication attempts.Step 3: Capture transmitted initialization vectors or public handshake values.Step 4: Detect repeating patterns suggesting entropy reuse.Step 5: Use entropy analyzer script to find low-variation seeds.Step 6: Predict future keying material and forge access.
- **Detection**: Entropy variance audit tool
- **Solution**: Enforce secure random generation with hardware RNG
- **Tags**: nfc, entropy, PQC, credential brute-force

## Wi-Fi Beacon Entropy Leak via Signal Strength Variations

- **Attack Type**: RF-Based Side-Channel
- **Target**: PQ Wi-Fi Router
- **Vulnerability**: RF Side-Channel from Entropy Reuse
- **MITRE**: T1595.002 (Active Scanning: Wireless)
- **Impact**: Partial Key Leakage
- **Tools**: Wireshark, SDR (Software Defined Radio), GNU Radio
- **Scenario**: An attacker analyzes Wi-Fi beacon signal strength during key generation to infer entropy leakages in a PQC chip
- **Attack Steps**: Step 1: Setup a low-cost SDR (e.g., RTL-SDR) within range of a PQC-enabled access point.Step 2: Passively record Wi-Fi beacon frames and monitor signal strength patterns using GNU Radio.Step 3: Initiate multiple connection attempts by forcing deauthentication.Step 4: Track minute RF variations linked to energy usage during PQC key generation.Step 5: Correlate RF leakage patterns with known entropy weaknesses.Step 6: Use data to predict randomness seeds.
- **Detection**: RF signature tracking
- **Solution**: Shield PQ chip RF emissions
- **Tags**: PQC, entropy, Wi-Fi, RF, SDR

## Reused PQ Session Key in LoRaWAN IoT Transmission

- **Attack Type**: LoRaWAN Wireless Replay
- **Target**: PQ LoRaWAN Sensor
- **Vulnerability**: Key Stream Reuse
- **MITRE**: T1001.003 (Data Obfuscation: Protocol Impersonation)
- **Impact**: Data Spoofing
- **Tools**: LoRaSniff, Lorawan-packet-sniffer, PyLoRa
- **Scenario**: PQC encryption scheme for LoRaWAN incorrectly reuses session keys for multiple telemetry packets
- **Attack Steps**: Step 1: Identify PQC-enabled LoRaWAN smart sensor (e.g., agriculture node).Step 2: Use LoRaSniff to capture multiple uplink packets.Step 3: Analyze packet structure and look for repeated cipher patterns.Step 4: XOR ciphertexts with same key stream to extract plaintext telemetry.Step 5: Construct spoofed payloads with valid MAC.Step 6: Replay or manipulate data to fake sensor readings.
- **Detection**: Duplicate MAC in packets
- **Solution**: Ensure per-session key generation
- **Tags**: LoRaWAN, PQC, replay, entropy

## PQ Certificate Reuse Exploit via Bluetooth Probe

- **Attack Type**: Bluetooth Certificate Replay
- **Target**: BLE PQ Device
- **Vulnerability**: Certificate Reuse
- **MITRE**: T1649 (Steal or Forge Authentication Certificates)
- **Impact**: Device Impersonation
- **Tools**: nRF Sniffer, Bluetoothctl, BLEah
- **Scenario**: PQC digital certificates for secure pairing are reused in multiple BLE sessions, enabling spoofing
- **Attack Steps**: Step 1: Monitor PQ BLE communication between device and phone using nRF Sniffer.Step 2: Capture and extract digital certificate during pairing.Step 3: Observe reuse of same certificate in future sessions.Step 4: Reuse captured certificate to initiate pairing as spoofed device.Step 5: Use spoofed device to request access or send commands.Step 6: Log device response and authentication acceptance.
- **Detection**: BLE pairing logs
- **Solution**: Rotate and validate certs per session
- **Tags**: BLE, certificate, PQC, reuse, spoof

## PQ Wi-Fi Entropy Starvation via Battery Drain

- **Attack Type**: Energy-based Wireless Attack
- **Target**: Battery-Powered PQ IoT
- **Vulnerability**: Low-Entropy due to Power Starvation
- **MITRE**: T1495 (Firmware Corruption)
- **Impact**: Predictable Crypto
- **Tools**: Custom Wi-Fi Deauth script, ESP8266, Aircrack-ng
- **Scenario**: An attacker causes entropy starvation by repeatedly draining battery on IoT devices relying on low-power PQC
- **Attack Steps**: Step 1: Deploy an ESP8266 module near PQC IoT device running on battery (e.g., camera).Step 2: Send continuous deauthentication frames to force reconnections.Step 3: Monitor battery decline, forcing device to regenerate keys with limited entropy.Step 4: Capture repeated PQ handshakes.Step 5: Compare randomness between attempts.Step 6: Exploit predictable key reuse in handshake or session.
- **Detection**: PQ handshake similarity logs
- **Solution**: Use secure battery-powered entropy generator
- **Tags**: entropy, power, PQC, battery, wireless

## Zigbee IV Reuse Attack in PQ-Enabled Devices

- **Attack Type**: Zigbee IV Collision
- **Target**: PQ Zigbee Smart Device
- **Vulnerability**: IV Reuse
- **MITRE**: T1609 (Lateral Tool Transfer)
- **Impact**: Control of Remote Device
- **Tools**: KillerBee, zbSniff, Scapy
- **Scenario**: Improper initialization vector (IV) handling in PQ-enabled Zigbee modules leads to data recovery
- **Attack Steps**: Step 1: Deploy zbSniff to capture Zigbee frames between PQ controller and device.Step 2: Extract encrypted payloads with identical IVs.Step 3: Detect cipher text collision using XOR differential.Step 4: Reconstruct partial or full plaintext commands.Step 5: Send unauthorized device control packets using replay.Step 6: Observe device behavior confirming command acceptance.
- **Detection**: Zigbee IV pattern monitor
- **Solution**: Enforce random IV per session
- **Tags**: Zigbee, IV reuse, PQC, IoT

## Wi-Fi Mesh Entropy Bleed via Channel Saturation

- **Attack Type**: Wi-Fi Mesh Timing Attack
- **Target**: PQ Mesh Router
- **Vulnerability**: Entropy Bleed during Overload
- **MITRE**: T1599.003 (Network Denial of Service: Wireless)
- **Impact**: Cross-node Hijack
- **Tools**: Aircrack-ng, Wireshark, mesh-sat-tool
- **Scenario**: Attacker overwhelms Wi-Fi mesh routing, causing PQ devices to reuse key derivation entropy due to resource limits
- **Attack Steps**: Step 1: Identify PQ mesh-enabled router system (e.g., home mesh with PQ handshake).Step 2: Generate saturation traffic to force constant routing updates.Step 3: Monitor key handshakes between nodes using Wireshark.Step 4: Detect similar key derivation sequences.Step 5: Analyze timing and key material leakage.Step 6: Forge session or replay keys across nodes.
- **Detection**: Routing logs, repeated keys
- **Solution**: Apply entropy guardrails in firmware
- **Tags**: mesh, wireless, PQC, entropy

## NFC Replay of Weak PQ Auth Token

- **Attack Type**: Wireless NFC Key Replay
- **Target**: PQ Smartcard / NFC Auth Device
- **Vulnerability**: Replayable PQ Auth Tokens
- **MITRE**: T1212 (Exploitation for Credential Access)
- **Impact**: Unauthorized Entry
- **Tools**: Proxmark3, NFCLogger, APDU Monitor
- **Scenario**: A PQ NFC access system reuses challenge-response tokens allowing an attacker to replay the same session
- **Attack Steps**: Step 1: Use Proxmark3 to record PQC-based NFC handshake from smartcard to reader.Step 2: Capture and extract the response token.Step 3: Detect reuse of the same challenge-response pair.Step 4: Replay token to gain unauthorized access.Step 5: Monitor reader’s response confirming session acceptance.Step 6: Log access breach.
- **Detection**: NFC session log audit
- **Solution**: Use nonce-based response, enable token freshness
- **Tags**: NFC, replay, PQC, token

## BLE Entropy Interference via Jamming

- **Attack Type**: BLE Jamming for Entropy Disruption
- **Target**: PQ BLE Device
- **Vulnerability**: Entropy Reuse under Disruption
- **MITRE**: T1557.003 (Adversary-in-the-Middle: Bluetooth)
- **Impact**: Session Hijacking
- **Tools**: BLE Jammer (e.g., HackRF), Ubertooth, BLEah
- **Scenario**: BLE jamming affects timing of PQ keygen processes, causing reuse of similar entropy in reconnections
- **Attack Steps**: Step 1: Use HackRF to create targeted BLE jamming around PQ device.Step 2: Force repeated reconnection attempts due to signal disruption.Step 3: Capture new handshakes using Ubertooth.Step 4: Compare handshake messages for similarity.Step 5: Detect entropy reuse due to rushed PQ key generation.Step 6: Exploit similar responses for spoof or MITM.
- **Detection**: BLE entropy delta analyzer
- **Solution**: Introduce secure reconnection entropy pool
- **Tags**: BLE, entropy, PQC, jamming

## Radio Proximity Attack for PQ RNG Desync

- **Attack Type**: RF Induced RNG Failure
- **Target**: PQ IoT Gateway
- **Vulnerability**: RNG Desync via RF Field
- **MITRE**: T1565.002 (Stored Data Manipulation)
- **Impact**: RNG Output Predictability
- **Tools**: SDR, Faraday Cage, EMF Emitter
- **Scenario**: Strong RF fields near PQ-enabled devices cause minor desync in hardware RNGs, leading to entropy reuse
- **Attack Steps**: Step 1: Place a radio emitter device near a PQ IoT gateway.Step 2: Flood the area with high-intensity RF signals.Step 3: Observe system behavior during key generation.Step 4: Check logs or intercept traffic showing similar randomness.Step 5: Replay partial key sequences in handshake.Step 6: Use entropy modeling to predict future keys.
- **Detection**: RF activity logs
- **Solution**: Harden RNGs with shielding
- **Tags**: RF, entropy, PQC, RNG, IoT

## 802.15.4-Based Entropy Injection

- **Attack Type**: Wireless Injection Attack
- **Target**: 802.15.4 PQ Sensor
- **Vulnerability**: External Entropy Injection
- **MITRE**: T1602 (Data from Information Repositories)
- **Impact**: Predictable Key Generation
- **Tools**: Scapy-radio, HackRF, KillerBee
- **Scenario**: Attacker injects crafted entropy-manipulating frames in IEEE 802.15.4 protocol to influence PQC keygen outcome
- **Attack Steps**: Step 1: Capture 802.15.4 traffic from PQ crypto sensor network.Step 2: Craft and send timing-sensitive frames that reset internal counters or entropy pool.Step 3: Force multiple key generations during attack.Step 4: Observe entropy pool reusing prior values.Step 5: Predict generated PQ keys based on timing model.Step 6: Impersonate or decrypt secure messages.
- **Detection**: Frame timing analytics
- **Solution**: Protect entropy functions from input triggers
- **Tags**: 802.15.4, PQC, entropy injection, wireless

## PQ Wi-Fi Key Reuse through Forced Handshake Flooding

- **Attack Type**: Wi-Fi Entropy Exhaustion Attack
- **Target**: PQ-enabled Wi-Fi AP
- **Vulnerability**: Entropy pool exhaustion
- **MITRE**: T1110.003 (Brute Force: Credential Stuffing)
- **Impact**: Predictable PQ handshake
- **Tools**: Scapy, Aireplay-ng, Wireshark, Python script
- **Scenario**: The attacker forces repeated PQ handshake generations by flooding the AP with fake clients, exhausting the entropy pool and causing key reuse
- **Attack Steps**: Step 1: Set up a laptop with Aireplay-ng and Wi-Fi adapter in monitor mode.Step 2: Continuously send deauthentication frames to the AP to cause clients to reconnect frequently.Step 3: Simultaneously use Scapy or Python scripts to simulate many fake client connection requests to the same AP.Step 4: Capture all PQ handshake messages using Wireshark.Step 5: Analyze handshake randomness, especially in the key exchange phase.Step 6: After entropy exhaustion, repeated sessions will start showing similar cryptographic parameters.Step 7: Match patterns and predict or replay session key components.
- **Detection**: Duplicate handshake randomness
- **Solution**: Rate-limit handshakes, add entropy entropy health monitor
- **Tags**: Wi-Fi, PQC, key reuse, handshake, entropy exhaustion

## BLE Entropy Corruption via Battery Glitch

- **Attack Type**: Power-Based Wireless Disruption
- **Target**: BLE-enabled PQ Token
- **Vulnerability**: Entropy corruption due to unstable power
- **MITRE**: T1581 (Resource Hijacking)
- **Impact**: Weak or reused crypto session
- **Tools**: EM Pulse Generator, BLEah, Oscilloscope
- **Scenario**: A BLE-based PQ authentication device is subjected to sudden power glitches via EM-based attack, causing internal entropy corruption
- **Attack Steps**: Step 1: Position a BLE device under test on a table with a small EM pulse generator placed next to its power regulator (simulate with lab-safe EM coil).Step 2: Induce a rapid battery fluctuation (simulate power dip/glitch) during BLE pairing attempt.Step 3: Use BLEah to capture handshake packets.Step 4: Repeat power glitch process several times while comparing PQ handshake entropy.Step 5: Observe pattern repetition or reused PQ key elements.Step 6: Extract data to spoof or manipulate future sessions.Step 7: Try replaying handshake using earlier entropy fingerprint.
- **Detection**: EM/power stability monitor
- **Solution**: Design for power-failure-safe entropy generation
- **Tags**: BLE, entropy, power fault, PQC

## LoRa Entropy Pattern Profiling via Timed Collision

- **Attack Type**: Timing-Based Collision Attack
- **Target**: PQ LoRa Device
- **Vulnerability**: Timed entropy collision delay
- **MITRE**: T1498.002 (Network Denial of Service: Wireless)
- **Impact**: Data spoof or key inference
- **Tools**: PyLoRa, HackRF, GNURadio
- **Scenario**: LoRa PQ implementations with poorly timed key rotation schedules can be targeted using RF collision bursts to induce delayed entropy use
- **Attack Steps**: Step 1: Use PyLoRa to send periodic data from a PQ-enabled LoRa device (e.g., telemetry sensor).Step 2: Set up a HackRF or SDR to monitor uplink packets and transmit timed interference (collisions) during PQ keygen intervals.Step 3: Force the device to delay or reuse entropy due to collision-induced transmission failures.Step 4: Capture multiple packets and analyze structure/timing.Step 5: Identify patterns or reused entropy bits in encrypted payloads.Step 6: Use partial recovery techniques to infer plaintext or derive session key.Step 7: Replay or modify messages in uplink.
- **Detection**: Timing log comparison across transmissions
- **Solution**: Randomize key rotation, protect keygen process from RF conditions
- **Tags**: LoRa, entropy delay, collision, PQC

## Reused PQ Parameters in Wireless Mesh Handoff

- **Attack Type**: Mesh Roaming Key Reuse
- **Target**: PQ Wi-Fi Mesh Router
- **Vulnerability**: Entropy pool not reset across mesh nodes
- **MITRE**: T1583.006 (Acquire Infrastructure: Web Services)
- **Impact**: Session hijacking across mesh
- **Tools**: Wireshark, hcxtools, mesh-topo-sim
- **Scenario**: Wireless mesh PQ routers reuse session key material during rapid handoff between nodes when entropy pool isn't refilled
- **Attack Steps**: Step 1: Simulate a home or enterprise PQ mesh setup with multiple AP nodes.Step 2: Use a mobile client to roam rapidly between APs.Step 3: Capture PQ handshake messages during every handoff with Wireshark.Step 4: Analyze handshake fields for repeated entropy artifacts (e.g., same nonce or salt values).Step 5: Identify reused parameters between AP transitions.Step 6: Replay captured handshakes to initiate spoofed connections.Step 7: Use session reuse to inject false client traffic.
- **Detection**: Mesh topology entropy pool check
- **Solution**: Enforce independent entropy pools per node
- **Tags**: mesh, Wi-Fi, PQC, entropy, session reuse

## Zigbee Beacon Injection for Predictable Key Negotiation

- **Attack Type**: Beacon Spoof for Entropy Distortion
- **Target**: Zigbee PQ Endpoint
- **Vulnerability**: Beacon spam causes PQ entropy pattern reuse
- **MITRE**: T1599.003 (Network Denial of Service: Wireless)
- **Impact**: Forced predictable key negotiation
- **Tools**: KillerBee, Scapy-radio, Zigpy
- **Scenario**: Attacker injects fake Zigbee beacons to induce poorly randomized PQ key negotiation on endpoint devices
- **Attack Steps**: Step 1: Identify Zigbee-based PQ crypto devices (e.g., smart bulb or lock).Step 2: Use KillerBee or Scapy-radio to create and inject fake Zigbee beacon frames with high frequency.Step 3: Force the device to repeatedly reinitiate the PQ handshake process due to spoofed network change.Step 4: Capture the resulting handshakes with zbSniff.Step 5: Analyze handshake entropy values and look for repeating segments.Step 6: Infer bits or values of keying material.Step 7: Replay handshake or send manipulated control messages.
- **Detection**: Beacon timing pattern logs
- **Solution**: Filter spoofed beacons, slow retry logic
- **Tags**: Zigbee, entropy, spoof, PQC, beacon

## ZKP Protocol Downgrade via Wi-Fi Deauthentication

- **Attack Type**: Wireless – Wi-Fi Protocol Exploitation
- **Target**: Wi-Fi-enabled ZKP client
- **Vulnerability**: Lack of downgrade protection
- **MITRE**: T1621 – Multi-Factor Authentication Request Generation
- **Impact**: Bypasses quantum-safe authentication
- **Tools**: Wireshark, Aireplay-ng, Router with ZKP module
- **Scenario**: Attacker forces the device running ZKP over Wi-Fi to downgrade to a weaker or non-ZKP-based authentication mode using deauthentication flooding.
- **Attack Steps**: Step 1: Set up a test Wi-Fi access point that supports ZKP-based authentication. Step 2: Connect a client device to the access point using ZKP-based authentication. Step 3: Use Aireplay-ng to continuously send deauthentication packets targeting the client. Step 4: Monitor client behavior—device may fall back to a legacy authentication method (e.g., WPA2-PSK). Step 5: Capture the legacy handshake using Wireshark and perform offline brute-force or dictionary attack. Step 6: Highlight how downgrade attack bypasses ZKP protections.
- **Detection**: Monitoring auth protocol switches; alert on downgrade
- **Solution**: Enforce strict protocol pinning, block downgrade fallback
- **Tags**: ZKP, Wi-Fi, Downgrade Attack, Aireplay-ng

## Signal Reflection Spoofing in Wireless ZKP Exchange

- **Attack Type**: Wireless – RF Relay Attack
- **Target**: Wireless ZKP-based access control system
- **Vulnerability**: Protocol unaware of time-of-flight anomalies
- **MITRE**: T1557 – Man-in-the-Middle
- **Impact**: ZKP spoofed despite lack of key knowledge
- **Tools**: HackRF One, GNURadio, ZKP Protocol Emulator
- **Scenario**: Exploits RF relays to reflect authentication responses in ZKP systems, tricking verifier into trusting a cloned prover.
- **Attack Steps**: Step 1: Emulate a ZKP authentication exchange between two devices. Step 2: Place attacker between prover and verifier using two HackRF One devices. Step 3: Use GNURadio to relay signals from prover to verifier with a slight delay. Step 4: Ensure timing is managed to make the relay seem legitimate. Step 5: Show verifier successfully authenticates the attacker-controlled device. Step 6: Demonstrate impact of relay-based spoofing in distance-bounding protocols.
- **Detection**: Monitor time delays and RF fingerprints
- **Solution**: Implement distance bounding checks and RF anomaly detection
- **Tags**: Relay Attack, RF Spoofing, Zero-Knowledge Proof

## Side-Channel Leakage via Bluetooth Frequency Drift

- **Attack Type**: Wireless – Bluetooth Interference
- **Target**: BLE IoT device with ZKP auth
- **Vulnerability**: No side-channel protection in proof generation
- **MITRE**: T1040 – Network Sniffing
- **Impact**: Partial secret disclosure
- **Tools**: BLE Sniffer, SDR, Power Analyzer
- **Scenario**: Exploits minor power fluctuations in Bluetooth Low Energy (BLE) devices implementing ZKP to infer secret bits during proof generation.
- **Attack Steps**: Step 1: Set up a BLE-enabled device performing ZKP-based access control. Step 2: Use SDR and BLE sniffer to passively monitor frequency shifts during ZKP responses. Step 3: Use power analyzer to correlate slight energy use fluctuations with computational steps. Step 4: Reconstruct partial secrets from timing and power signatures. Step 5: Validate if secret recovery helps forge ZKP responses.
- **Detection**: Analyze RF spectrum + power profiles
- **Solution**: Harden ZKP protocol with noise/random delays
- **Tags**: BLE, Side-channel, Zero-Knowledge

## Zigbee-Based ZKP Tampering via Packet Injection

- **Attack Type**: Wireless – Zigbee Interception
- **Target**: Zigbee-enabled smart devices
- **Vulnerability**: Lack of ZKP packet structure validation
- **MITRE**: T1557 – Man-in-the-Middle
- **Impact**: Verifier crash or false acceptance
- **Tools**: KillerBee, ZBOSS Sniffer, Custom ZKP Handler
- **Scenario**: Injects malformed ZKP responses in a Zigbee network to manipulate verifier behavior and force authentication failure or crash.
- **Attack Steps**: Step 1: Set up a Zigbee-based smart lock that uses ZKP for identity verification. Step 2: Use KillerBee and ZBOSS sniffer to capture normal proof exchanges. Step 3: Modify the captured packet structure to inject faulty ZKP responses. Step 4: Replay these packets during authentication and observe verifier response. Step 5: Repeated faulty responses may crash the verifier or make it accept invalid proofs.
- **Detection**: Protocol-level anomaly detection
- **Solution**: Strict packet structure validation
- **Tags**: Zigbee, Packet Injection, Zero-Knowledge

## Rogue Access Point Performing ZKP Bypass with Fake Beacon Frames

- **Attack Type**: Wireless – Wi-Fi Rogue AP
- **Target**: Wi-Fi clients relying on advertised ZKP
- **Vulnerability**: Trusting unauthenticated beacons
- **MITRE**: T1557.002 – Rogue Wireless Access Point
- **Impact**: Users misled into insecure network
- **Tools**: WiFi Pineapple, Hostapd, Custom ZKP Emulator
- **Scenario**: A rogue AP advertises fake support for ZKP authentication but silently bypasses it by accepting any proof input.
- **Attack Steps**: Step 1: Set up a rogue AP using WiFi Pineapple and hostapd, mimicking a legitimate ZKP-enabled network. Step 2: Create fake beacon frames advertising ZKP support. Step 3: Allow any client ZKP input as "valid" to establish trust. Step 4: Log all client proofs and attempt offline analysis to identify implementation flaws. Step 5: Use the trust established by the rogue AP to inject malicious commands or redirect traffic.
- **Detection**: Wireless beacon monitoring, ZKP challenge-response logs
- **Solution**: Enforce AP certificate pinning and challenge validation
- **Tags**: Rogue AP, Wi-Fi Beacon, ZKP Bypass

## ZKP Replay Attack over Wi-Fi Mesh Network

- **Attack Type**: Wireless – Replay
- **Target**: Wi-Fi Mesh with ZKP service
- **Vulnerability**: No freshness (timestamp) checks in ZKP
- **MITRE**: T1003 – Credential Replay
- **Impact**: Unauthorized access without password
- **Tools**: Wireshark, Scapy, Mesh-capable Wi-Fi router
- **Scenario**: Attacker captures a valid ZKP exchange over a mesh network and replays it to gain access to a secure service.
- **Attack Steps**: Step 1: Set up a Wi-Fi mesh network with a ZKP-authenticated service (e.g., door access). Step 2: Use Wireshark to passively sniff the authentication traffic between a user and the access point. Step 3: Identify the ZKP challenge-response pairs in the traffic. Step 4: Use Scapy to replay the exact same response back to the AP. Step 5: Observe if the AP accepts the repeated proof. If not, replay older challenges to simulate re-use. Step 6: Demonstrate access without knowing the secret, showing poor nonce management.
- **Detection**: Look for duplicate challenges in logs
- **Solution**: Use nonces, timestamps, and challenge uniqueness
- **Tags**: Replay Attack, Mesh Wi-Fi, ZKP

## Cross-Protocol ZKP Confusion via Bluetooth Stack

- **Attack Type**: Wireless – Bluetooth
- **Target**: Bluetooth Smart Lock / IoT Device
- **Vulnerability**: Dual-protocol fallback not protected
- **MITRE**: T1621 – Protocol Downgrade
- **Impact**: ZKP bypass with legacy pairing
- **Tools**: Bluetooth Debugger, ZKP Emulator, Packet Sniffer
- **Scenario**: Mixing ZKP and legacy authentication in the Bluetooth stack leads to bypasses.
- **Attack Steps**: Step 1: Set up a Bluetooth server that accepts ZKP-based and legacy pairing. Step 2: Start legitimate pairing via ZKP on a test client. Step 3: At mid-handshake, interrupt the ZKP exchange and inject a legacy pairing request. Step 4: Observe if the device completes legacy pairing instead of ZKP. Step 5: Log the downgrade and bypass event. Step 6: Simulate a user tricked into accepting a fake connection.
- **Detection**: Monitor Bluetooth pairing protocols
- **Solution**: Enforce strict protocol preference
- **Tags**: Bluetooth, Protocol Confusion, ZKP

## Timing Analysis Attack on ZKP via Zigbee

- **Attack Type**: Wireless – Zigbee Timing Leak
- **Target**: Zigbee-based ZKP device
- **Vulnerability**: Variable proof-gen time reveals secrets
- **MITRE**: T1046 – Timing Side Channel
- **Impact**: Secret key partial leak
- **Tools**: Zigbee Analyzer, Timing Logger, ZKP Test App
- **Scenario**: By analyzing time taken to generate ZKP proofs, attacker infers bits of secret.
- **Attack Steps**: Step 1: Set up a Zigbee smart meter that uses ZKP for authentication. Step 2: Send multiple ZKP challenges and measure exact response times for each. Step 3: Use statistical tools to correlate timing differences with proof complexity. Step 4: Infer bits of the prover’s secret. Step 5: Reconstruct the full secret or impersonate the prover. Step 6: Show how hardware processing time leaks data unintentionally.
- **Detection**: Constant-time implementation detection
- **Solution**: Implement time-equalizing countermeasures
- **Tags**: Zigbee, Timing Leak, Side-Channel

## NFC Relay Attack Against ZKP Terminal

- **Attack Type**: Wireless – NFC Relay
- **Target**: NFC-enabled Authentication System
- **Vulnerability**: No distance/time verification
- **MITRE**: T1557.003 – NFC Relay
- **Impact**: Bypasses location-bound authentication
- **Tools**: 2x Android Phones w/ NFC Tools, Relay App
- **Scenario**: A wireless relay forwards authentication from a distant device to bypass ZKP locality.
- **Attack Steps**: Step 1: Set up a ZKP authentication terminal using NFC (e.g., access gate). Step 2: Use two Android phones placed far apart – one near the terminal, one near the legitimate user. Step 3: Install NFC relay app to forward all communication between phones over Wi-Fi or 4G. Step 4: Simulate the authentication process – remote phone collects ZKP, forwards it, and vice versa. Step 5: Access terminal thinks the user is physically present and unlocks. Step 6: Discuss implications for physical access control systems.
- **Detection**: NFC timing + relay detection
- **Solution**: Use distance-bounding or proximity sensors
- **Tags**: NFC, ZKP, Relay, Physical Bypass

## Fault Injection Over RF to Alter ZKP Output

- **Attack Type**: Wireless – Fault Injection via RF
- **Target**: Embedded device using ZKP
- **Vulnerability**: No hardware shielding or RF filter
- **MITRE**: T1600 – Induced Faults
- **Impact**: Proof integrity failure or crash
- **Tools**: SDR (HackRF), Signal Jammer, Faraday Cage
- **Scenario**: By injecting RF pulses at specific times, attacker causes miscalculations in proof generation.
- **Attack Steps**: Step 1: Set up a testbed with a device performing a ZKP operation inside a controlled Faraday cage. Step 2: Use SDR to emit controlled EM pulses near the device during computation. Step 3: Observe changes in ZKP output—errors, bit flips, or reboots. Step 4: Repeat pulses at key cycles to corrupt the proof. Step 5: Use corrupted proofs to forge acceptance or crash the verifier. Step 6: Demonstrate how wireless EM fault injection weakens ZKP integrity.
- **Detection**: EMI monitoring + shielding
- **Solution**: Add shielding, software fault tolerance
- **Tags**: RF Fault Injection, Side-Channel, ZKP

## MiTM Injection Attack on Wi-Fi-based ZKP Voting System

- **Attack Type**: Wireless – Wi-Fi Injection
- **Target**: ZKP-secured e-Voting Terminal
- **Vulnerability**: Lack of ZKP proof integrity checks
- **MITRE**: T1557 – MiTM Data Injection
- **Impact**: ZKP-based votes altered in transit
- **Tools**: Evil Twin AP, SSLStrip, Proxy Server, Packet Editor
- **Scenario**: Wireless man-in-the-middle modifies ZKP-based ballots before being sent to backend.
- **Attack Steps**: Step 1: Create a rogue access point mimicking the official voting Wi-Fi network. Step 2: Capture voting terminal traffic using SSLStrip + proxy to view ZKP ballot data. Step 3: Intercept and slightly modify the proof (e.g., change a vote bit). Step 4: Forward the altered proof to the backend server. Step 5: Show how backend wrongly accepts manipulated ZKP proof. Step 6: Explain real-world risk in e-voting and ZKP transport.
- **Detection**: Proof hash or MAC check failure
- **Solution**: Use integrity check (MAC) for proof
- **Tags**: ZKP, E-Voting, MiTM, Wi-Fi

## Jamming-Based Denial of Service During ZKP Auth

- **Attack Type**: Wireless – RF Jamming
- **Target**: ZKP-authenticated Wi-Fi service
- **Vulnerability**: No jamming detection or fallback
- **MITRE**: T1499 – DoS via RF
- **Impact**: ZKP authentication fails or crashes
- **Tools**: RF Jammer, ZKP Test Service, Monitoring Console
- **Scenario**: Wireless jammer disrupts ZKP exchange, preventing completion of authentication.
- **Attack Steps**: Step 1: Set up ZKP authentication between client and server over Wi-Fi. Step 2: Use a directional RF jammer to block Wi-Fi channel during ZKP proof exchange. Step 3: Monitor how devices fail to complete ZKP handshake. Step 4: Jam selectively during proof-response to simulate DoS. Step 5: Repeat to deny access repeatedly. Step 6: Show need for jamming-resilient communication.
- **Detection**: Monitor signal strength anomalies
- **Solution**: Use frequency hopping + detection logic
- **Tags**: RF Jamming, Denial-of-Service, ZKP

## SDR Spoofing of ZKP Certificate Broadcast over BLE

- **Attack Type**: Wireless – BLE Broadcast Spoofing
- **Target**: BLE Mesh IoT Device
- **Vulnerability**: Unverified broadcast spoofing
- **MITRE**: T1557 – Wireless Spoofing
- **Impact**: Impersonation of trusted entity
- **Tools**: HackRF, GNURadio, BLE Beacons Emulator
- **Scenario**: Spoofs ZKP-based identity broadcast to impersonate a trusted node in BLE mesh.
- **Attack Steps**: Step 1: Identify a BLE beacon device broadcasting ZKP certificate or public key. Step 2: Use HackRF and GNURadio to clone the broadcast. Step 3: Modify broadcast content to point to attacker’s ZKP identity. Step 4: Replay modified signal to surrounding nodes. Step 5: Other nodes now trust the spoofed broadcast. Step 6: Inject fake messages or proofs accepted as trusted.
- **Detection**: BLE broadcast fingerprinting
- **Solution**: Secure broadcasts with signed keys
- **Tags**: BLE, Spoofing, ZKP Broadcast

## Rogue Drone Intercepting ZKP Auth from IoT Sensors

- **Attack Type**: Wireless – Drone Surveillance
- **Target**: Smart IoT deployment
- **Vulnerability**: Open-air wireless ZKP without encryption
- **MITRE**: T1602 – Data from Network Sniffing
- **Impact**: Remote monitoring and proof theft
- **Tools**: Wi-Fi Sniffer, Raspberry Pi Drone, Directional Antenna
- **Scenario**: Drone acts as a relay/sniffer to intercept and analyze ZKP transactions from smart devices.
- **Attack Steps**: Step 1: Equip a drone with Raspberry Pi, Wi-Fi card, directional antenna, and sniffing tools. Step 2: Fly near a smart agriculture field or smart city sensor hub using ZKP-authentication. Step 3: Capture authentication traffic between sensors and controller. Step 4: Analyze proof challenges and responses. Step 5: Attempt replay or timing attack based on intercepted data. Step 6: Use drone logs to simulate remote adversary.
- **Detection**: RF triangulation + signal noise detection
- **Solution**: Encrypt ZKP transport layer
- **Tags**: Drone, Surveillance, ZKP Intercept

## Wi-Fi Side-Channel via Signal Strength in ZKP Exchange

- **Attack Type**: Wireless – Signal Strength Leak
- **Target**: ZKP-enabled Wi-Fi IoT devices
- **Vulnerability**: Signal fluctuations not normalized
- **MITRE**: T1592 – Signal-Based Side Channel
- **Impact**: Leaks ZKP timing and behavior
- **Tools**: Wi-Fi Analyzer, Signal Logger, Custom Client
- **Scenario**: Fluctuations in signal strength during ZKP exchange give away proof timing.
- **Attack Steps**: Step 1: Set up a ZKP exchange between client and server over Wi-Fi. Step 2: Log signal strength (RSSI) patterns during proof-response phase. Step 3: Observe repetitive dips/spikes correlating with certain computations. Step 4: Map signal variance to expected operations. Step 5: Build side-channel profile to infer secret values. Step 6: Show how proximity + RF monitoring gives insight into proof logic.
- **Detection**: Monitor RSSI + correlate with timing
- **Solution**: Add noise + equalize signal emission
- **Tags**: Signal Analysis, Wi-Fi ZKP, Side Channel

## Wi-Fi Beacon Manipulation to Bypass ZKP

- **Attack Type**: Wireless – Wi-Fi Spoofing
- **Target**: Wi-Fi clients expecting ZKP authentication
- **Vulnerability**: Clients trust advertised metadata
- **MITRE**: T1557.002 – Rogue Wireless Access Point
- **Impact**: Bypasses ZKP with fake network
- **Tools**: Aircrack-ng Suite, Wireshark, Beacon Frame Generator
- **Scenario**: Attacker forges Wi-Fi beacon frames to falsely indicate ZKP support, tricking users to connect to an insecure AP.
- **Attack Steps**: Step 1: Set up a rogue Wi-Fi access point using Aircrack-ng or Hostapd.Step 2: Use a beacon frame generator to continuously broadcast fake beacon frames advertising support for ZKP-based authentication.Step 3: Ensure the rogue AP has no real ZKP implementation — it accepts any authentication.Step 4: A client device scans for networks and connects to the rogue AP, believing it supports secure ZKP.Step 5: Log all authentication attempts, including user credentials or attempted proofs.Step 6: Explain how attackers can bypass ZKP by forging metadata rather than breaking the protocol itself.
- **Detection**: Monitor SSID/Beacon inconsistencies
- **Solution**: Authenticate network origin using certificates
- **Tags**: Beacon Spoofing, ZKP Metadata, Wi-Fi

## ZKP Entropy Weakness via Wireless Entropy Injection

- **Attack Type**: Wireless – RF Interference
- **Target**: Devices using wireless ZKP with HRNG
- **Vulnerability**: Hardware RNG susceptible to RF bias
- **MITRE**: T1600 – Hardware Manipulation
- **Impact**: Nonce reuse enables impersonation
- **Tools**: SDR (HackRF), Entropy Logger, Hardware RNG Sensor
- **Scenario**: Attacker emits deliberate RF noise to influence the hardware random number generator (HRNG) used in ZKP.
- **Attack Steps**: Step 1: Deploy a test system using a ZKP protocol that depends on hardware-generated random numbers (nonces).Step 2: Position an SDR near the device and emit low-frequency RF noise aimed at the HRNG.Step 3: Observe a reduction in randomness using entropy-logging tools.Step 4: Repeated ZKP proofs begin to show patterns or reuse of nonces.Step 5: Capture the weakened proof values using Wireshark or a sniffer.Step 6: Replay or brute-force the responses, leveraging the entropy weakness to impersonate the prover.
- **Detection**: Monitor entropy levels and randomness logs
- **Solution**: Use shielded RNG and TRNG over HRNG
- **Tags**: RNG, Entropy Injection, ZKP Attack

## Bluetooth Pairing Confusion Attack Against ZKP Devices

- **Attack Type**: Wireless – Bluetooth Confusion
- **Target**: BLE smart locks or wearables
- **Vulnerability**: Overlapping signals during ZKP pairing
- **MITRE**: T1621 – Multi-Protocol Interference
- **Impact**: ZKP pairing can be bypassed or aborted
- **Tools**: Bluetooth Interceptor App, BLE Sniffer, ZKP Emulator
- **Scenario**: Attacker uses a nearby Bluetooth device to interfere and confuse ZKP-based Bluetooth pairing with unexpected pairing signals.
- **Attack Steps**: Step 1: Set up a ZKP-secured Bluetooth smart lock and a legitimate user device initiating pairing.Step 2: Attacker device starts broadcasting repeated fake pairing requests during the ZKP handshake.Step 3: The target lock receives overlapping signals from both legitimate and rogue devices.Step 4: Device either resets the pairing session or accepts a partial ZKP proof from the wrong device.Step 5: Log how this forces pairing fallback or temporary pairing with a non-ZKP device.Step 6: Explain implications in environments with multiple BLE devices and insufficient protocol isolation.
- **Detection**: Pairing anomalies, scan for rogue requests
- **Solution**: Filter & isolate pairing during ZKP handshake
- **Tags**: BLE Confusion, Pairing Bypass, ZKP

## Smartwatch Impersonation Attack Using ZKP Cloning via RF

- **Attack Type**: Wireless – Impersonation
- **Target**: Wearable devices using ZKP
- **Vulnerability**: BLE data not encrypted or signed
- **MITRE**: T1557.001 – Wireless Sniffing & Injection
- **Impact**: Full impersonation without user
- **Tools**: BLE Sniffer (Ubertooth), Scapy-BLE, ZKP Logger
- **Scenario**: Smartwatch transmits ZKP authentication proof over BLE; attacker captures and clones proof to gain access.
- **Attack Steps**: Step 1: Set up a smartwatch that performs ZKP authentication to unlock a paired phone or door lock.Step 2: Using a BLE sniffer (e.g., Ubertooth), capture the outgoing proof from the smartwatch.Step 3: Analyze the structure of the ZKP proof (public parameters and nonce).Step 4: Use Scapy-BLE to craft a cloned response mimicking the original proof.Step 5: Send the cloned proof to the verifier while original watch is inactive.Step 6: Watch how the system accepts the proof and grants access, showing clone vulnerability.
- **Detection**: BLE encryption monitoring + nonce check
- **Solution**: Always encrypt ZKP payload and verify freshness
- **Tags**: BLE Cloning, Smartwatch Spoofing, ZKP

## Denial of Service via Proof Flooding in Zigbee Mesh

- **Attack Type**: Wireless – Zigbee Flooding
- **Target**: Zigbee-based ZKP mesh nodes
- **Vulnerability**: No rate limiting or proof validation
- **MITRE**: T1499.002 – Service Exhaustion
- **Impact**: ZKP system unusable due to load
- **Tools**: KillerBee, ZBOSS, Zigbee ZKP Emulator
- **Scenario**: Floods Zigbee ZKP authenticator with continuous proof requests to exhaust resources.
- **Attack Steps**: Step 1: Set up a Zigbee mesh network with ZKP authentication for devices (e.g., smart lights).Step 2: Use KillerBee to identify the coordinator node or ZKP verifier.Step 3: Send a barrage of randomized or malformed ZKP challenges at high frequency.Step 4: Verifier attempts to process all proofs, consuming CPU and memory.Step 5: Eventually verifier becomes unresponsive or resets.Step 6: Demonstrate how even secure authentication can be targeted with availability attacks.
- **Detection**: Spike in authentication requests
- **Solution**: Enforce rate limits, challenge verification
- **Tags**: ZKP DoS, Zigbee Mesh, Proof Flooding

## Wavelength Attack via Multi-Wavelength Injection

- **Attack Type**: Multi-Wavelength Channel Attack
- **Target**: QKD Optical Receiver
- **Vulnerability**: Poor wavelength filtering tolerance
- **MITRE**: T1211 (Exploitation for Defense Evasion)
- **Impact**: Subtle bias in photon detection, hidden eavesdropping
- **Tools**: Tunable Laser Source, Wavelength Analyzer, QKD Filter Emulator
- **Scenario**: Sends photons at different wavelengths than expected to manipulate filters and detection logic, bypassing wavelength-specific filters.
- **Attack Steps**: Step 1: Simulate a QKD system that uses specific wavelength (e.g., 1550nm).Step 2: Generate and inject photons at slightly different wavelengths (e.g., 1540nm, 1560nm).Step 3: Analyze how receiver filters respond—some filters allow off-spectrum photons due to hardware tolerances.Step 4: Use this to inject crafted photons that interfere with or bias key generation.Step 5: Measure altered key distribution and demonstrate attack efficacy.
- **Detection**: Monitor spectral deviation and apply filtering logs
- **Solution**: Use narrowband wavelength filters and reject outliers
- **Tags**: Wavelength Attack, Filter Bypass

## Dark Count Exploit in Low-Quality Detectors

- **Attack Type**: Detector Noise Exploit
- **Target**: Single Photon Detectors
- **Vulnerability**: Lack of dark count calibration or shielding
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Partial key poisoning, undetectable errors
- **Tools**: QKD Detector Emulator, Background Light Source, Statistical Logger
- **Scenario**: Exploits "dark counts"—false positives in photon detection when no actual photon is received—to inject noise and bias key agreement.
- **Attack Steps**: Step 1: Set up QKD receiver with a low-cost or unshielded photon detector.Step 2: Introduce low-level light or RF noise in the environment.Step 3: Observe how these stimuli increase the dark count rate.Step 4: During key generation, the system registers these false detections as legitimate bits.Step 5: Use public reconciliation logs to map dark count patterns and extract probable key bits.
- **Detection**: Compare dark count rates to baseline
- **Solution**: Use temperature-controlled and shielded detectors
- **Tags**: QKD, Noise Injection, Dark Count

## Phase Reference Attack in Differential QKD

- **Attack Type**: Reference Frame Manipulation
- **Target**: Differential QKD System
- **Vulnerability**: No tracking of phase drift over time
- **MITRE**: T1003.003 (OS Credential Dumping: NTDS)
- **Impact**: Misaligned key generation, unnoticed bit errors
- **Tools**: Phase Modulator, Drift Generator, Reference Laser Analyzer
- **Scenario**: Attacker introduces phase drift in the reference laser used for phase-encoded differential QKD, causing bit flip misinterpretation.
- **Attack Steps**: Step 1: Simulate differential phase QKD using reference pulse technique.Step 2: Slowly drift the phase reference using controlled interference.Step 3: Let receiver measure incoming pulses based on drifted phase.Step 4: This causes misinterpretation of encoded bits.Step 5: Reconcile keys and extract matching attacker-known bit values.
- **Detection**: Phase variance monitoring & correction
- **Solution**: Apply phase feedback loops or reference locking
- **Tags**: Phase Drift, Reference Attack

## Classical Control Signal Tampering in QKD Systems

- **Attack Type**: Embedded Control Exploit
- **Target**: QKD Modulator Firmware
- **Vulnerability**: No secure boot or firmware validation
- **MITRE**: T1542.001 (Pre-OS Boot: System Firmware)
- **Impact**: Covert backdoor in quantum state generation
- **Tools**: Hardware Debugger (JTAG), Firmware Dump Tool, Logic Analyzer
- **Scenario**: Attacker targets the microcontroller/firmware responsible for modulating photon properties in QKD devices.
- **Attack Steps**: Step 1: Access QKD device hardware and identify control board (MCU).Step 2: Dump firmware via JTAG or UART using debugger tools.Step 3: Modify code responsible for modulating photon polarization or phase.Step 4: Implant code that slightly biases state selection (e.g., more 0s).Step 5: Observe final key having predictable statistical imbalance matching implanted bias.
- **Detection**: Check firmware hash, use secure boot chain
- **Solution**: Employ digitally signed firmware and attestation
- **Tags**: Firmware Exploit, MCU Injection

## Side-Channel Acoustic Eavesdropping on QKD Hardware

- **Attack Type**: Acoustic Side-Channel Attack
- **Target**: Physical QKD Hardware
- **Vulnerability**: Acoustic emissions from modulator switches
- **MITRE**: T1010 (Application Window Discovery)
- **Impact**: Acoustic leakage of secret key bits
- **Tools**: Sensitive Microphone, Acoustic Analyzer, Isolation Chamber
- **Scenario**: Microphones pick up tiny vibrations from QKD equipment (e.g., phase modulators) to infer internal states or timing.
- **Attack Steps**: Step 1: Place a high-sensitivity microphone near QKD device (e.g., on casing).Step 2: Record acoustic patterns during key generation, especially modulator activity.Step 3: Analyze signal frequencies using Fourier transform to isolate switching patterns.Step 4: Correlate patterns with key bit generation (0s vs 1s).Step 5: Reconstruct bit patterns from consistent acoustic leaks and validate accuracy.
- **Detection**: Acoustic profiling & shielding monitoring
- **Solution**: Encapsulate hardware; use vibration isolation
- **Tags**: Acoustic Side Channel, QKD

## Photonic Leakage through Quantum Phase Shifters

- **Attack Type**: Optical Side-Channel
- **Target**: Photonic QKD Phase Modulator
- **Vulnerability**: Optical emission during phase encoding
- **MITRE**: T1055 - Process Injection (optical process info leak variant)
- **Impact**: Phase encoding leakage leading to partial key recovery
- **Tools**: Infrared camera, fiber tap coupler, photodiode array
- **Scenario**: Phase shifters in photonic QKD chips may emit faint secondary light patterns during operation, detectable with sensitive photodetectors.
- **Attack Steps**: Step 1: Set up a low-noise IR camera or photodiode near the photonic chip. Step 2: Initiate a QKD session where phase modulation is expected (e.g., BB84 protocol). Step 3: Use a fiber tap coupler to capture side-reflected photons. Step 4: Observe and record IR emission patterns or faint side-beam reflections. Step 5: Match light intensity variance with specific phase shifts used for encoding key bits.
- **Detection**: Infrared emission analysis during idle and active states
- **Solution**: Use blackened, opaque casing with internal optical damping
- **Tags**: Photonic, Phase Shifter, Side-Channel

## Correlated Thermal Signature Mapping of Qubit Transitions

- **Attack Type**: Infrared Thermal Mapping Attack
- **Target**: Qubit Control Chip
- **Vulnerability**: Heat emission during quantum operations
- **MITRE**: T1600 - Weaken Encryption (by exploiting implementation weaknesses)
- **Impact**: Logical gate inference, reverse engineering
- **Tools**: FLIR-grade IR thermal camera, QKD test rig, thermal lens
- **Scenario**: Attacker maps the minute thermal outputs of qubit transitions by using high-precision IR sensors to deduce when and how qubits change state.
- **Attack Steps**: Step 1: Calibrate a sensitive thermal imaging camera to detect sub-degree changes. Step 2: Position the camera near the qubit housing or control substrate. Step 3: Start QKD operation and simultaneously record thermal activity. Step 4: Analyze the thermal variance at different chip regions, especially during expected entanglement or rotation gates. Step 5: Correlate the rise/fall patterns to specific logical operations and map qubit transition points.
- **Detection**: Baseline thermal pattern comparisons
- **Solution**: Add passive heat spreaders and randomized idle gating
- **Tags**: Thermal Imaging, Qubit Logic

## Audio-Based Timing Analysis via Relay Hum

- **Attack Type**: Acoustic Relay Hum Side-Channel
- **Target**: Legacy QKD Hardware
- **Vulnerability**: Acoustic relay sounds leaking operation timing
- **MITRE**: T1420 - Audio Capture
- **Impact**: Timing-based key reconstruction or inference
- **Tools**: Contact microphone, audio analyzer, FFT software (Audacity, MATLAB)
- **Scenario**: Old-style quantum hardware often uses relays for switching; these produce low-frequency hums or clicks which can reveal the timing of operations.
- **Attack Steps**: Step 1: Attach a contact microphone to the chassis of the QKD hardware. Step 2: Begin audio recording during a complete QKD cycle. Step 3: Isolate low-frequency hums or relay clicks using FFT and filter analysis. Step 4: Use audio peaks to measure timing of bit transitions or protocol handshakes. Step 5: Estimate which sections of the quantum circuit are active during the captured audio signals.
- **Detection**: Spectrogram and frequency profile analysis
- **Solution**: Replace relays with solid-state switching and dampen case vibrations
- **Tags**: Relay Click, Audio, Timing Leak

## Bitrate Variation Attack on Quantum-Enhanced VPN Devices

- **Attack Type**: Bandwidth Side-Channel
- **Target**: Quantum-Enabled VPN Router
- **Vulnerability**: Bandwidth correlates with quantum key activity
- **MITRE**: T1046 - Network Service Scanning (timing-based key phase inference)
- **Impact**: Indirect key exhaustion attack, replay possibility
- **Tools**: Wireshark, traffic sniffer, custom traffic generator
- **Scenario**: A quantum-VPN hybrid router encrypts traffic using QKD keys, but shows variable bandwidth patterns based on key agreement phase.
- **Attack Steps**: Step 1: Connect a passive sniffer on the network segment linked to the quantum-VPN router. Step 2: Observe the device's bandwidth usage and timing over several key cycles. Step 3: Inject synthetic traffic and measure latency and jitter around key negotiation phases. Step 4: Use these patterns to determine when a key is successfully generated or not. Step 5: Use statistical analysis to infer entropy availability or possible key reuse.
- **Detection**: Monitor bandwidth variance and entropy lag
- **Solution**: Use dummy traffic padding and randomized throughput control
- **Tags**: VPN, QKD, Bandwidth Leak

## RF Probe Leakage from Quantum Control Line Drivers

- **Attack Type**: RF Side-Channel via Driver Amplifiers
- **Target**: Quantum Gate Driver Circuit
- **Vulnerability**: RF signal leakage through poorly shielded amplifiers
- **MITRE**: T1216 - System Script Proxy Execution (RF interpreted as logic)
- **Impact**: Active gate detection, timing reconstruction
- **Tools**: Near-field RF probe, spectrum analyzer, directional antenna
- **Scenario**: Driver amplifiers used in qubit control circuits may emit unintended RF noise that reflects gate transitions.
- **Attack Steps**: Step 1: Place a near-field RF probe near the amplifier driving qubit control lines. Step 2: Activate test circuits to cycle through quantum gates (e.g., H, X, CZ). Step 3: Record RF emissions using a spectrum analyzer across GHz ranges. Step 4: Identify frequency-domain signatures unique to each gate type. Step 5: Use the RF fingerprints to guess active gate types during normal execution.
- **Detection**: RF sweep tests across all operational states
- **Solution**: RF filters, improved shielding, power line chokes
- **Tags**: RF Probe, Qubit Driver, Signal Leak

## Inducing Quantum Entropy Deviation via Nearby RFID Fields

- **Attack Type**: Wireless (RFID Interference)
- **Target**: Photonic QRNGs
- **Vulnerability**: High-frequency energy leakage
- **MITRE**: T1421 (Hardware Signal Disruption)
- **Impact**: Biased or partially predictable output
- **Tools**: RFID Reader (13.56 MHz), QRNG evaluation board, Entropy logger
- **Scenario**: RFID readers placed near QRNG devices unintentionally emit high-frequency energy that causes entropy deviation in quantum sensors or photon detectors.
- **Attack Steps**: Step 1: Set up a tabletop QRNG system with open optical sensing components (e.g., photonic QRNG). Step 2: Place an active RFID reader near the QRNG hardware (~10–30 cm). Step 3: Power the RFID reader and perform repeated scanning cycles. Step 4: Use an entropy logger or built-in QRNG diagnostic interface to monitor randomness output. Step 5: Analyze if bitstream shows reduced variability or temporal patterns. Step 6: Vary distance and scanning rate to evaluate effect consistency.
- **Detection**: Entropy test suite (NIST SP800-90B)
- **Solution**: Use RFID-shielded enclosures for QRNGs
- **Tags**: qrng, rfid, interference

## Exploiting Quantum RNG via Wi-Fi Router Firmware Exploit and Remote Clock Skewing

- **Attack Type**: Wireless (Wi-Fi-based clock skew manipulation)
- **Target**: IoT QRNG-integrated Systems
- **Vulnerability**: Time-based entropy skew
- **MITRE**: T1070.006 (Time Stomping)
- **Impact**: Predictable entropy generation
- **Tools**: Compromised Wi-Fi router, QRNG using system clock, NTP emulator
- **Scenario**: A malicious actor exploits a smart router to alter NTP timing for nearby QRNG devices dependent on time synchronization, causing entropy skew.
- **Attack Steps**: Step 1: Set up a QRNG system (e.g., IoT device) that relies on system time for randomness sampling or seeding. Step 2: Connect device to a Wi-Fi router with custom firmware that can control NTP responses. Step 3: Force the device to sync with attacker-controlled NTP server. Step 4: Skew time by injecting micro-offsets at defined intervals. Step 5: Monitor the QRNG’s entropy sampling timestamps and bitstream quality. Step 6: Detect reduced randomness or phase-aligned entropy due to clock manipulation.
- **Detection**: Entropy analysis + NTP log mismatch
- **Solution**: Secure NTP source validation
- **Tags**: qrng, wifi, time-attack

## Quantum RNG Response Delay Attack via BLE Latency Injection

- **Attack Type**: Wireless (Bluetooth Latency Manipulation)
- **Target**: BLE-Connected QRNGs
- **Vulnerability**: Trust in real-time entropy timing
- **MITRE**: T1557.002 (BLE MITM)
- **Impact**: Distorted entropy integration
- **Tools**: Two BLE dongles (one attacker-controlled), QRNG BLE sensor, Latency Injector
- **Scenario**: A Bluetooth man-in-the-middle attacker adds variable delays to entropy communication between QRNG sensor and host system, affecting randomness behavior.
- **Attack Steps**: Step 1: Set up QRNG module that transmits entropy over BLE to a host controller. Step 2: Place attacker device between QRNG and host, acting as a proxy. Step 3: Forward BLE packets with intentional delays introduced (in milliseconds). Step 4: Record how timing manipulation affects host's entropy gathering. Step 5: Inject longer delays intermittently to simulate unstable entropy. Step 6: Observe application of flawed random keys in encryption logs.
- **Detection**: Monitor BLE packet timings
- **Solution**: Validate entropy freshness and timestamping
- **Tags**: ble, latency, qrng

## QRNG Tampering via Wireless Power Injection in Smart Devices

- **Attack Type**: Wireless (Wireless Power Transfer Interference)
- **Target**: Mobile/Smart Devices with QRNG
- **Vulnerability**: Wireless energy field instability
- **MITRE**: T1496 (Resource Hijacking)
- **Impact**: Degraded entropy reliability
- **Tools**: Qi Charger, Smart device with QRNG chip, Oscilloscope, Power logger
- **Scenario**: Wireless power pads beneath or near smart devices with embedded QRNGs induce voltage and frequency instability in entropy circuits.
- **Attack Steps**: Step 1: Place a smartphone or tablet with QRNG chip on a Qi wireless charger. Step 2: Observe power and voltage fluctuations using an oscilloscope on the QRNG VCC line. Step 3: Simultaneously activate high-power wireless charging cycles. Step 4: Measure entropy stream for irregularities and bias. Step 5: Use apps that generate keys or tokens to inspect randomness impact. Step 6: Run repeat cycles with variable charger distances.
- **Detection**: Internal power fluctuation logs
- **Solution**: Improve EMI filtering and voltage regulation
- **Tags**: qrng, wireless power, interference

## Side-Channel RF Echo Mapping of QRNG Optical Paths

- **Attack Type**: Wireless (RF Echo Imaging)
- **Target**: Optical QRNG Hardware
- **Vulnerability**: Structural EM leakage
- **MITRE**: T1200 (Hardware Probing)
- **Impact**: Partial entropy state disclosure
- **Tools**: HackRF or RTL-SDR, Directional Antenna, RF Echo Analyzer
- **Scenario**: Attackers map internal structure of QRNGs using reflected radio waves to determine operational entropy states.
- **Attack Steps**: Step 1: Position a directional antenna near QRNG device in an open lab setup. Step 2: Transmit low-powered RF pulses (e.g., 2.4 GHz range) toward the QRNG hardware. Step 3: Capture echoes and reflections with HackRF or SDR device. Step 4: Analyze signal variations as the QRNG operates in real-time. Step 5: Attempt to correlate changes in optical path or mirrors to entropy output. Step 6: Build RF image maps of QRNG internal structure.
- **Detection**: Unusual RF echo pattern shifts
- **Solution**: Physical QRNG isolation or RF-proof casing
- **Tags**: side-channel, rf-mapping, qrng

## Acoustic Induction of Quantum RNG Instability via Modulated Ultrasound

- **Attack Type**: Wireless (Ultrasonic Signal Injection)
- **Target**: Jitter-based QRNG
- **Vulnerability**: Mechanical vibration sensitivity
- **MITRE**: T1200 (Hardware Additions)
- **Impact**: Entropy instability under acoustic load
- **Tools**: Ultrasonic speaker (40kHz), QRNG with jitter-based entropy, Entropy analyzer
- **Scenario**: Ultrasonic pulses aimed at a QRNG casing vibrate sensitive internal parts, affecting entropy extraction from jitter sources.
- **Attack Steps**: Step 1: Set up QRNG based on oscillator jitter or Johnson noise in a quiet room. Step 2: Place an ultrasonic speaker (emitting 40kHz+) ~10–20 cm from the casing. Step 3: Emit modulated ultrasonic pulses with controlled frequency sweeps. Step 4: Monitor vibration or mechanical resonance using microphone or accelerometer. Step 5: Log entropy output for patterns during ultrasonic bursts. Step 6: Compare random bitstream with and without ultrasonic attack.
- **Detection**: Frequency-pattern entropy shift
- **Solution**: Soundproofing or ultrasound filtering
- **Tags**: acoustic, ultrasonic, qrng

## Polarization Pattern Spoof via Wi-Fi Controlled Emitter

- **Attack Type**: Fake Entanglement Injection
- **Target**: Lab-based Wi-Fi QKD setup
- **Vulnerability**: Pattern assumption and poor Wi-Fi security
- **MITRE**: T1584
- **Impact**: Fake photon data forms valid key bits
- **Tools**: Wi-Fi photon emitter, ESP32, Python controller
- **Scenario**: Attacker spoofs photon polarization patterns using a modified Wi-Fi-controlled emitter to trick QKD devices.
- **Attack Steps**: Step 1: Identify the polarization pattern used by the real QKD device.Step 2: Modify Wi-Fi photon emitter to match this pattern.Step 3: Place the device close to the receiver in a test lab.Step 4: Emit photons with synchronized polarization to match expected values.Step 5: Monitor classical reconciliation to confirm acceptance.Step 6: Steal shared key generated using fake photon data.Step 7: Power off emitter and disconnect from Wi-Fi before detection.
- **Detection**: Analyze pattern similarity in accepted photons
- **Solution**: Randomize polarization and add challenge-based auth
- **Tags**: polarization, spoof, Wi-Fi, quantum

## Side-channel Leakage via LED Indicator Timing

- **Attack Type**: Fake Entanglement Injection
- **Target**: QKD Controller with LED output
- **Vulnerability**: Visible side-channel leak
- **MITRE**: T1216
- **Impact**: Side-channel enabled photon spoofing
- **Tools**: Camera, LED timing analyzer, Photon injector
- **Scenario**: LED timing from QKD controller leaks photon base switch timing, used to fake entangled state.
- **Attack Steps**: Step 1: Place high-speed camera facing the LED indicators of QKD device.Step 2: Record the timing pattern between LED flashes and photon base switches.Step 3: Analyze the delay to find pattern correlation.Step 4: Inject fake photons during the known switch window.Step 5: Sync injection with base alignment.Step 6: Use classical channel to confirm matching key bits.Step 7: Withdraw setup and erase logs.
- **Detection**: Mask LED patterns and delay timing
- **Solution**: Shield indicators or use random flashing
- **Tags**: LED, side-channel, timing leak

## Timing Delay Injection via Bluetooth Keyboard Attack

- **Attack Type**: Fake Entanglement Injection
- **Target**: Bluetooth-based input system
- **Vulnerability**: Delay manipulation in operator input
- **MITRE**: T1542
- **Impact**: Subtle command timing spoofing
- **Tools**: Bluetooth sniffer, USB injector, Timing manipulator
- **Scenario**: Bluetooth keyboard delay is used to influence QKD command timings, allowing photon injection at critical time.
- **Attack Steps**: Step 1: Pair with Bluetooth keyboard used in QKD control system.Step 2: Introduce slight delay during photon transmission commands.Step 3: Sync own photon pulses with the delayed transmission.Step 4: Emit fake entangled photons matching delayed base.Step 5: Observe successful bit acceptance via logs.Step 6: Intercept final symmetric key.Step 7: Disconnect from Bluetooth to avoid forensic detection.
- **Detection**: Monitor Bluetooth latency statistics
- **Solution**: Use wired keyboards in critical systems
- **Tags**: Bluetooth, keyboard, delay, photon sync

## QRNG (Quantum RNG) Signal Spoofing with SDR

- **Attack Type**: Fake Entanglement Injection
- **Target**: Quantum Random Number Generator
- **Vulnerability**: Lack of QRNG signal verification
- **MITRE**: T1631
- **Impact**: Predictable photon base, partial key leakage
- **Tools**: SDR (BladeRF), Pulse replicator, Antenna array
- **Scenario**: Uses SDR to spoof QRNG pulses to force predictable photon polarization generation.
- **Attack Steps**: Step 1: Locate antenna used to transmit QRNG output.Step 2: Use SDR to receive real QRNG signal pattern.Step 3: Replay a crafted predictable pulse stream using same frequency.Step 4: Sync it with QKD photon generator.Step 5: Photon generation follows attacker’s predictable pattern.Step 6: Observe classical bit reconciliation to confirm success.Step 7: Withdraw SDR unit after session.
- **Detection**: Monitor entropy and randomness score
- **Solution**: Use offline QRNG with physical entropy test
- **Tags**: QRNG, spoof, SDR, randomness

## Laser Interference via Roof Opening to Inject Synchronized Photons

- **Attack Type**: Fake Entanglement Injection
- **Target**: Free-space photon lab
- **Vulnerability**: Physical light path exposed
- **MITRE**: T1612
- **Impact**: Physical interference for key stealing
- **Tools**: Green laser (532nm), Timer circuit, Pulse controller
- **Scenario**: Sends laser pulses through rooftop openings into lab to interfere with photon stream and insert fake data.
- **Attack Steps**: Step 1: Survey rooftop area for ventilation or glass openings.Step 2: Position laser with angle to reach receiver optics.Step 3: Time laser pulses to arrive in sync with actual photon stream.Step 4: Emit matched photons with controlled polarization.Step 5: Allow detection as valid photons.Step 6: Use classical communication leak to observe accepted bits.Step 7: Remove gear once session ends.
- **Detection**: Install optical noise monitors
- **Solution**: Secure ceiling paths and cover all openings
- **Tags**: laser, injection, rooftop, optics

## Smartwatch BLE Injection to Modify Entanglement Log Data

- **Attack Type**: Fake Entanglement Injection
- **Target**: Wearable device connected to QKD logs
- **Vulnerability**: BLE data stream manipulation
- **MITRE**: T1565
- **Impact**: Tampered photon event records
- **Tools**: Smartwatch with BLE support, Custom app, BLE sniffer
- **Scenario**: Uses smartwatch to intercept and modify BLE control logs during photon transmission process.
- **Attack Steps**: Step 1: Wear BLE-enabled smartwatch paired with QKD controller.Step 2: Use custom app to listen to photon timestamp updates.Step 3: Intercept and alter timestamps to match attacker's injected photon timings.Step 4: Match injected photons to expected base using log manipulation.Step 5: Allow key reconciliation to proceed.Step 6: Store full key within smartwatch app.Step 7: Erase app data post-session.
- **Detection**: BLE session integrity check
- **Solution**: Restrict BLE to admin-only during QKD
- **Tags**: BLE, smartwatch, log spoof, wearable

## Predictive Photon Injection Based on Fixed Measurement Pattern

- **Attack Type**: Fake Entanglement Injection
- **Target**: Repetitive QKD pattern environments
- **Vulnerability**: Lack of entropy in base selection
- **MITRE**: T1611
- **Impact**: Key generated using attacker-predicted photons
- **Tools**: Photon emitter, Pattern analyzer tool, Log archive
- **Scenario**: Predicts measurement pattern from previous sessions and uses fixed photon injections for future key generation.
- **Attack Steps**: Step 1: Collect logs of previous QKD sessions over weeks.Step 2: Analyze bit acceptance and basis pattern trends.Step 3: Identify recurring polarization or time-of-flight patterns.Step 4: Build a photon injection model based on prediction.Step 5: Emit photons matching predicted acceptance.Step 6: Observe successful matches via classical reconciliation.Step 7: Validate prediction success with stolen keys.
- **Detection**: Pattern analysis mismatch alert
- **Solution**: Increase QKD base entropy and session randomization
- **Tags**: pattern, prediction, photon repeat, QKD logs

## Modulated EM Pulse Injection into QKD Lab via Smart Bulb

- **Attack Type**: Fake Entanglement Injection
- **Target**: Smart Lighting near QKD receiver
- **Vulnerability**: Optical interference via environmental devices
- **MITRE**: T1203.002
- **Impact**: Indirect spoofing of photon reception
- **Tools**: Smart bulb (Zigbee/Wi-Fi), Modulation app, SDR
- **Scenario**: Attacker uses smart bulb’s light pulses to subtly interfere with photon reception system.
- **Attack Steps**: Step 1: Connect to smart bulb used in lab environment.Step 2: Program bulb to flash at specific frequency that interferes with photon detector sensitivity.Step 3: During flashes, inject fake photons matching expected polarization.Step 4: Detector misreads light as real photon.Step 5: Allow attacker to insert known key bits.Step 6: Review logs to validate bit acceptance.Step 7: Reset bulb to normal mode post-session.
- **Detection**: Light-based anomaly detection
- **Solution**: Use shielded optics and restrict smart IoT
- **Tags**: IoT, bulb, optical spoof, lab

## Acoustic-Based Polarization Detection via Microphone Array

- **Attack Type**: Fake Entanglement Injection
- **Target**: Physical QKD modulator
- **Vulnerability**: Acoustic signature leak
- **MITRE**: T1562.001
- **Impact**: Predictive photon injection from acoustic side-channel
- **Tools**: Microphone array, Audio-to-polarization map, Pulse laser
- **Scenario**: Detects polarization switch via sound and uses timing to inject photons.
- **Attack Steps**: Step 1: Deploy microphone array close to polarization modulator.Step 2: Capture acoustic signals of modulator switching.Step 3: Map sounds to basis values over training period.Step 4: Time photon injection with matching polarization.Step 5: Emit photons during matched sound events.Step 6: Use logs to confirm accepted bits.Step 7: Remove recording device post-lab session.
- **Detection**: Sound profile anomaly detection
- **Solution**: Acoustic shielding around modulator
- **Tags**: acoustic, microphone, side-channel

## Drone-Based Photon Injection via Rooftop Entry Port

- **Attack Type**: Fake Entanglement Injection
- **Target**: Physical lab with open ventilation
- **Vulnerability**: Unsecured building access point
- **MITRE**: T1200
- **Impact**: Full or partial key injection using drone
- **Tools**: Mini drone, Photon emitter, GPS sync controller
- **Scenario**: Drone delivers photon emitter through rooftop opening to directly inject fake photons during session.
- **Attack Steps**: Step 1: Prepare mini drone with photon emitter mounted.Step 2: Identify ventilation port or skylight.Step 3: Navigate drone into room using GPS and line-of-sight camera.Step 4: Time photon emissions to match base alignment phase.Step 5: Inject photons into receiver optics.Step 6: Observe classical channel to verify bit acceptance.Step 7: Exit drone and erase flight log.
- **Detection**: Monitor for unexpected physical activity
- **Solution**: Restrict rooftop access and monitor airspace
- **Tags**: drone, rooftop, QKD injection

## Fake QKD Gateway using MAC & SSID Cloning

- **Attack Type**: Wireless MITM via Full Node Emulation
- **Target**: Wireless QKD Control Network
- **Vulnerability**: Lack of mutual authentication, client trusts first responder
- **MITRE**: T1557.002 (Rogue Access Point), T1071.001 (Application Protocol Abuse)
- **Impact**: Full MITM, compromised session setup
- **Tools**: Macchanger, Hostapd, dnsmasq, Scapy
- **Scenario**: Attacker clones MAC address and SSID of the QKD gateway access point, tricking clients to connect to a fully emulated rogue QKD node.
- **Attack Steps**: Step 1: Use airodump-ng to discover the QKD gateway's MAC address, SSID, and channel.Step 2: Set your Wi-Fi interface MAC using macchanger to match the real AP.Step 3: Configure Hostapd to broadcast same SSID on same or nearby channel.Step 4: Use higher transmission power or directional antenna to override the signal.Step 5: Launch deauth attack to disconnect clients from real AP.Step 6: Clients reconnect to rogue AP; use dnsmasq to issue valid-looking IPs.Step 7: Intercept and relay classical QKD control traffic while logging session metadata.
- **Detection**: Duplicate MAC detection, unusual DHCP logs
- **Solution**: Certificate pinning, AP whitelisting, MACsec
- **Tags**: QKD, MAC Cloning, Rogue AP, MITM

## Beacon Flood Attack to Overload QKD Clients

- **Attack Type**: Wireless Denial via Beacon MITM
- **Target**: QKD Client Devices (Wi-Fi)
- **Vulnerability**: Beacon scanning not filtered, SSID filtering disabled
- **MITRE**: T1557.002 (Beacon Flood), T1498.001 (Service Denial)
- **Impact**: Sync failure, false association, service instability
- **Tools**: MDK3, Aircrack-ng, Wireshark
- **Scenario**: An attacker floods the air with multiple fake QKD gateway beacons to confuse or mislead the QKD classical control device into connecting to incorrect or unstable nodes.
- **Attack Steps**: Step 1: Scan for legitimate QKD AP beacon characteristics (SSID, channel, BSSID).Step 2: Use mdk3 in beacon flood mode to broadcast thousands of fake APs using slight variations of the legitimate SSID.Step 3: Ensure beacon signal strength is higher than that of the real AP.Step 4: Wait for QKD clients to scan and pick one of the fake beacons.Step 5: If client tries to associate, log the connection attempt.Step 6: Optionally relay session negotiation messages with corrupted timing.Step 7: Cause session negotiation to timeout or fallback to insecure sync.
- **Detection**: Monitor beacon counts, validate BSSID integrity
- **Solution**: Filter BSSIDs, enforce AP allow-lists
- **Tags**: QKD, Beacon Flood, MITM, MDK3

## Wi-Fi Karma Attack on QKD Mobile Sync App

- **Attack Type**: Wireless Probe Response MITM
- **Target**: QKD Mobile Apps
- **Vulnerability**: Auto-connect behavior; no server-side pinning
- **MITRE**: T1557.002 (Rogue AP), T1110.003 (Credential Capture)
- **Impact**: Compromised key sync, app-level MITM
- **Tools**: Karmetasploit, Bettercap, Roguehostapd
- **Scenario**: Using a Karma attack, attacker tricks QKD mobile app into connecting to a rogue AP by responding to its probe requests, enabling session hijack of app-based key sync.
- **Attack Steps**: Step 1: Monitor probe requests sent by mobile QKD app for previously connected networks.Step 2: Configure Roguehostapd to automatically respond to any probe with matching SSID.Step 3: Start a Karma attack using Bettercap or Karmetasploit.Step 4: Mobile device auto-connects to rogue AP.Step 5: Host fake key synchronization API endpoint.Step 6: Log all key sync requests and token headers.Step 7: Relay some requests to real QKD server to maintain false trust.
- **Detection**: Unusual mobile connection logs, strange token failures
- **Solution**: Disable auto-connect, enforce TLS with pinned certs
- **Tags**: QKD, Karma, Mobile MITM, Roguehostapd

## Sideband Emissions Eavesdropping on QKD Receiver

- **Attack Type**: Passive Wireless Side-channel MITM
- **Target**: QKD Hardware Receivers
- **Vulnerability**: Electromagnetic emissions (unintentional)
- **MITRE**: T1592.001 (EM Analysis), T1120 (Hardware Information Collection)
- **Impact**: Leakage of physical process, timing metadata
- **Tools**: RTL-SDR, TEMPEST Shielding Test Kit, EM Probe
- **Scenario**: An attacker places a sensitive RF probe near a QKD receiver and uses sideband electromagnetic emissions to infer internal clocking and session events.
- **Attack Steps**: Step 1: Place EM probe (antenna or loop) in close proximity to QKD receiver or control hardware.Step 2: Use RTL-SDR to scan for periodic emissions or electromagnetic "leaks" from hardware.Step 3: Record the spectrum and analyze frequency components using FFT.Step 4: Correlate frequency spikes with known QKD event timings like photon arrival, key sync, etc.Step 5: Repeat across multiple sessions to build an emission profile.Step 6: Attempt to infer internal logic or device response during specific QKD phases.Step 7: Analyze emission amplitude change to predict session success/failure.
- **Detection**: Use spectrum analyzers, EM shielding audit
- **Solution**: Shielded rooms, reduce emissions, watchdogs
- **Tags**: QKD, TEMPEST, EM Side-Channel, MITM

## Delayed Quantum Acknowledgement Injection

- **Attack Type**: Wireless MITM via Classical Timing Trick
- **Target**: Wireless Classical Communication
- **Vulnerability**: Tight QKD timing expectations not verified
- **MITRE**: T1499.001 (Protocol Manipulation), T1600.002 (Timing Exploits)
- **Impact**: Corrupted keys, high QBER, session abort
- **Tools**: Wireshark, Scapy, Netfilter Queue
- **Scenario**: Attacker delays acknowledgement packets in classical channel (e.g., ACKs to photon pulses) to disrupt session timing, leading to misaligned key generation and error bursts.
- **Attack Steps**: Step 1: Place attacker in MITM position via ARP spoof or rogue AP.Step 2: Monitor classical traffic, identify QKD control ACK packets by size and pattern.Step 3: Redirect all classical packets into netfilter queue.Step 4: Program script to introduce microsecond-level delay in ACK packets.Step 5: Send ACKs late to disrupt quantum-classical sync.Step 6: Analyze QBER and session logs for failed keys or higher entropy noise.Step 7: Adjust delay dynamically to evade static timing filters.
- **Detection**: Session timer mismatch, logs of delay-induced failures
- **Solution**: Add tolerance windows, log exact ACK timings
- **Tags**: QKD, ACK Delay, Timing Attack, MITM

## Free-space Quantum Relay with Time-Split Attack

- **Attack Type**: Physical-layer MITM with Optical Beam Splitting
- **Target**: Free-space Quantum Channel
- **Vulnerability**: Lack of timing verification, exposed beam
- **MITRE**: T1200 (Hardware Additions), T1592.003 (Optical Signal Manipulation)
- **Impact**: Quantum sync disruption, potential photon loss
- **Tools**: Optical Beam Splitter, Delay Line, Telescope
- **Scenario**: A free-space QKD session is intercepted using a beam-splitter relay, introducing a delay so attacker can act as relay between source and destination via two different paths.
- **Attack Steps**: Step 1: Position a precise beam splitter in the free-space optical path between sender and receiver.Step 2: Split photon stream: send one to attacker’s delay circuit, another directly to receiver.Step 3: Inject short delay (ns–µs) so receiver receives legitimate pulses at slightly wrong times.Step 4: Route attacker-captured pulses to custom detector for analysis.Step 5: Adjust delay such that legitimate receiver syncs with attacker-supplied timing instead.Step 6: Collect photon timing and attempt pattern inference.Step 7: Repeat with different splitting ratios and delays for optimization.
- **Detection**: Optical signal power deviation, sync mismatch
- **Solution**: Optical watchdogs, QBER tolerance validation, beam filters
- **Tags**: QKD, Beam Split, Optical MITM, Free-space

## PQ VPN Session Cloning via MAC Spoofing on Public Wi-Fi

- **Attack Type**: Wireless - MAC Spoofing
- **Target**: PQ VPN clients
- **Vulnerability**: Weak session tie to MAC rather than cryptographic identity
- **MITRE**: T1557.002 (Session Hijack)
- **Impact**: VPN hijack or duplicate session
- **Tools**: macchanger, Wireshark, Bettercap, PQ VPN Tools
- **Scenario**: Attacker clones a MAC address of a PQ VPN client on public Wi-Fi and attempts to hijack or mimic its cryptographic session.
- **Attack Steps**: Step 1: Monitor a public Wi-Fi network for active devices using Wireshark.Step 2: Identify a device initiating a PQ VPN session and record its MAC address.Step 3: Use macchanger to spoof the victim’s MAC on the attacker’s machine.Step 4: Disconnect the original device using deauthentication packets via aireplay-ng.Step 5: Attempt to establish a PQ VPN session using the stolen MAC.Step 6: Observe if the VPN server improperly resumes or allows session establishment based on the spoofed address.Step 7: Log success or failure and collect all certificate validation data.Step 8: Analyze whether session integrity is tied to MAC address (an insecure practice).
- **Detection**: Monitor MAC session overlap or duplicate handshakes
- **Solution**: Enforce cryptographic binding to session, not MAC
- **Tags**: MAC Spoofing, PQ VPN, Hijack

## Exploiting Misconfigured PQ Key Rotation over Wi-Fi with Timing Probes

- **Attack Type**: Wireless - Timing Exploit
- **Target**: PQ VPN Gateways
- **Vulnerability**: Predictable or reused key rotation
- **MITRE**: T1497.003 (Time-Based Evasion)
- **Impact**: Weak forward secrecy, key reuse
- **Tools**: Nmap, Bettercap, Wireshark, Timing Script
- **Scenario**: Attacker times the key rotation intervals on a PQ-enabled VPN and predicts when old keys are reused or rotated improperly.
- **Attack Steps**: Step 1: Connect to or observe a PQ VPN session over Wi-Fi (e.g., Kyber-based).Step 2: Use Nmap and Wireshark to probe the client periodically while it is active.Step 3: Log key exchange times and note if there are consistent time-based patterns.Step 4: If key rotation is periodic and predictable (e.g., every 60s), attempt a probe exactly before and after.Step 5: Compare handshake structures to infer if a reused key or flawed rotation logic is being used.Step 6: Attempt to exploit reuse by capturing older session fragments and injecting them during new handshakes.Step 7: Analyze response logs for errors or acceptance.
- **Detection**: Detect predictable handshake intervals
- **Solution**: Enforce non-periodic key rotation; bind to entropy
- **Tags**: PQC, Key Rotation, Timing Attack

## PQ Key Material Exposure via Wi-Fi Debug Console Left Enabled

- **Attack Type**: Wireless - Misconfiguration / Debug Access
- **Target**: IoT Devices, PQ VPN Routers
- **Vulnerability**: Debug interfaces exposing key material
- **MITRE**: T1047, T1082
- **Impact**: Full compromise of cryptographic confidentiality
- **Tools**: Telnet, netcat, Wireshark, Developer Console Tools
- **Scenario**: Developer leaves debug interface enabled over Wi-Fi, which leaks PQ key material during testing or handshake logs.
- **Attack Steps**: Step 1: Scan the local Wi-Fi network for open ports (e.g., port 23 or 2323 for telnet).Step 2: Connect to the debug interface using telnet or netcat.Step 3: Check for verbose logging that includes PQ handshake logs, key material, or internal entropy pool values.Step 4: Capture logs of any key generation activity in real time.Step 5: Attempt to reuse logged keys in a separate PQ TLS session.Step 6: Use Wireshark to verify if the reused keys successfully decrypt observed traffic.Step 7: Log full system response and whether any alerts are triggered.
- **Detection**: Scan for debug port exposure
- **Solution**: Disable debug interfaces in production
- **Tags**: PQ Debug Leak, Wi-Fi, Key Exposure

## PQ Handshake Packet Duplication via Wi-Fi Broadcast Spoof

- **Attack Type**: Wireless - Packet Duplication
- **Target**: PQ VPN and TLS Clients
- **Vulnerability**: Improper caching or key duplication handling
- **MITRE**: T1027.006 (Duplicate Packets)
- **Impact**: Spoofed session keys, session desync
- **Tools**: Scapy, PacketForge, Wireshark
- **Scenario**: Attacker duplicates legitimate PQ handshake messages over broadcast to confuse client devices into accepting spoofed responses.
- **Attack Steps**: Step 1: Sniff the network for legitimate PQ TLS or VPN handshake packets (e.g., PQ KEM initiations).Step 2: Copy and slightly modify the timing or payload of those packets.Step 3: Broadcast multiple versions of the same handshake response across the Wi-Fi channel.Step 4: If the client accepts multiple versions or caches one improperly, analyze which one gets stored.Step 5: Check if spoofed key material influences session key generation.Step 6: Monitor device memory, handshake cache, or crash logs.Step 7: Attempt MITM based on the cached incorrect key.
- **Detection**: Monitor duplicate packet entries and cache conflicts
- **Solution**: Enforce strict one-time handshake caching
- **Tags**: PQ TLS, Broadcast Spoof, Wi-Fi

## Fake Wi-Fi Update Redirect to PQ Algorithm Downgrade Firmware

- **Attack Type**: Wireless - Firmware Downgrade
- **Target**: IoT Devices, PQ Routers
- **Vulnerability**: No verification of firmware origin or downgrade detection
- **MITRE**: T1542.001
- **Impact**: PQ crypto downgrade, firmware compromise
- **Tools**: EvilAP, DNS Spoof, Fake Update Page Generator, OTA Tools
- **Scenario**: Attacker simulates a firmware update alert over captive portal and installs older firmware with weakened PQ implementation.
- **Attack Steps**: Step 1: Set up a fake AP with a captive portal using DNS spoofing.Step 2: When a PQ device connects, redirect it to a portal that looks like a legitimate firmware update page.Step 3: Present an “important security update” and link it to a PQ firmware version that uses older PQ algorithms with known flaws.Step 4: If the device does not validate the firmware source properly, the update proceeds.Step 5: Log device responses, errors, or success messages.Step 6: Observe whether future TLS handshakes now rely on downgraded PQ algorithms.Step 7: Attempt to break the downgraded crypto or MITM the connection.
- **Detection**: Monitor firmware version and update logs
- **Solution**: Enforce signed and version-locked updates
- **Tags**: OTA Firmware, Downgrade, PQ Algorithm Weakness

## PQ VPN Decryption via Wi-Fi Traffic Pattern Learning

- **Attack Type**: Wireless - Traffic Analysis
- **Target**: PQ VPN Users
- **Vulnerability**: Metadata leaks via timing and traffic patterns
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Behavioral privacy loss without breaking encryption
- **Tools**: Wireshark, TrafficFlowAnalyzer, Tshark, Matplotlib
- **Scenario**: Without breaking PQ encryption, attacker learns usage patterns via traffic size/timing and infers sensitive behavior.
- **Attack Steps**: Step 1: Passively capture encrypted PQ VPN traffic over Wi-Fi using Wireshark or Tshark.Step 2: Use TrafficFlowAnalyzer to identify patterns in packet size, frequency, and response timing.Step 3: Train a machine learning model (e.g., decision tree) using sample behavioral data from controlled PQ VPN sessions (e.g., logging into banking site vs. social media).Step 4: Apply the trained model to live captures.Step 5: Infer possible user actions (e.g., password login, video streaming) even though data is encrypted.Step 6: Validate in lab if behavioral inferences align with real activity.Step 7: Document privacy leakage from metadata despite PQ encryption.
- **Detection**: Look for traffic patterns consistent with behavior
- **Solution**: Use traffic padding or uniform timing in VPN
- **Tags**: PQ VPN, Metadata Leak, ML Analysis

## BLE Mesh Replay Attack on Hybrid Key Sync for Secure IoT

- **Attack Type**: BLE Mesh Replay
- **Target**: IoT BLE Mesh Devices
- **Vulnerability**: No freshness validation in hybrid provisioning
- **MITRE**: T1557.003 (Bluetooth MITM), T1600 (Downgrade Attack)
- **Impact**: Legacy key reuse, unauthorized device control
- **Tools**: Btlejack, BLEah, Nordic Sniffer
- **Scenario**: Attacker records hybrid key sync messages on BLE Mesh (used in smart homes or industry) and replays them to inject legacy key material.
- **Attack Steps**: Step 1: Use a Nordic BLE sniffer or Btlejack to passively monitor BLE Mesh traffic during key provisioning. Step 2: Identify provisioning packets that include hybrid key material (PQC + RSA). Step 3: Capture the message exchange and save it. Step 4: Disconnect the provisioning device (use BLE jamming if needed). Step 5: Replay the original messages using BLEah or a script to simulate a valid provisioning. Step 6: If the provisioning device does not enforce freshness checks, it accepts and installs the legacy key. Step 7: Attacker uses the installed key to control or monitor IoT nodes.
- **Detection**: BLE mesh logs, timestamp mismatches
- **Solution**: Enforce nonce/freshness tokens in key sync
- **Tags**: ble-mesh, replay, hybrid-downgrade

## Drone Wi-Fi Link Hijack During PQ Remote Signing Session

- **Attack Type**: Drone Command Injection
- **Target**: Drone using Hybrid PKI
- **Vulnerability**: Crypto validation disabled for control packets
- **MITRE**: T1040 (Network Sniffing), T1600
- **Impact**: Command hijack, RSA key spoof
- **Tools**: Bettercap, Scapy, Drone SDK
- **Scenario**: PQ-controlled drones use hybrid crypto for remote signing/auth. An attacker breaks into its Wi-Fi channel and injects commands using spoofed RSA packets.
- **Attack Steps**: Step 1: Identify the drone’s Wi-Fi frequency and protocol using tools like airodump-ng. Step 2: Deauthenticate the legitimate controller using aireplay-ng. Step 3: Connect a fake controller device to the drone's Wi-Fi. Step 4: Use Scapy or the drone's SDK to craft command packets, embedding RSA-only signatures. Step 5: Send commands (e.g., GPS override or camera disable) and monitor the drone’s response. Step 6: If the drone accepts the RSA-only commands, this confirms failure to enforce hybrid cryptographic checks.
- **Detection**: Drone telemetry & handshake logs
- **Solution**: Enforce crypto verification at protocol level
- **Tags**: drone-hijack, rsa-command-injection

## Wi-Fi Chipset Fault Injection Causes PQ Stack Bypass

- **Attack Type**: Fault Injection
- **Target**: IoT Wi-Fi Device
- **Vulnerability**: Fault-injection leads to crypto bypass
- **MITRE**: T1600 (Weaken Encryption), T1203 (Exploitation for Privilege Escalation)
- **Impact**: Crypto bypass, key spoofing
- **Tools**: EMFI rig, ChipWhisperer, Serial Monitor
- **Scenario**: Attacker causes memory glitches in Wi-Fi chips using voltage pulses or electromagnetic pulses to bypass hybrid crypto stack validation.
- **Attack Steps**: Step 1: Open the IoT device housing the Wi-Fi chipset (e.g., ESP32). Step 2: Connect a fault injection device (e.g., ChipWhisperer or EMFI rig) to the board. Step 3: Trigger faults during the handshake process where hybrid (PQC + RSA) keys are being validated. Step 4: Bypass integrity checks or force fallback to RSA-only validation. Step 5: Intercept resulting network traffic using Wireshark to confirm the fallback. Step 6: Replay session and exploit with legacy key reuse.
- **Detection**: Analyze handshake behavior under fault
- **Solution**: Use hardened chips with PQ validation
- **Tags**: wifi-chip, fault-injection, crypto-bypass

## Hybrid Handshake Leak via Side-Channel on Wi-Fi RF Spectrum

- **Attack Type**: RF Side-Channel
- **Target**: PQ-enabled Wi-Fi Device
- **Vulnerability**: No RF shielding leads to side-channel leakage
- **MITRE**: T1592.002 (Hardware Information), T1600
- **Impact**: Partial RSA key recovery via emissions
- **Tools**: HackRF, SigMF, GNURadio, RFtap
- **Scenario**: An attacker places spectrum analyzers near a PQ device during hybrid handshake and records RF fluctuations to infer RSA bits.
- **Attack Steps**: Step 1: Place HackRF near the PQ-capable router or laptop. Step 2: Use SigMF and GNURadio to record physical RF spectrum during hybrid handshake. Step 3: Zoom into 2.4GHz or 5GHz frequency changes with millisecond precision. Step 4: Analyze transmission patterns for timing or power-level variations during RSA vs PQ encryption computation. Step 5: If identifiable patterns are found, correlate with potential RSA key bits. Step 6: Simulate brute-force offline guessing using leaked timing patterns.
- **Detection**: Spectrum anomaly monitoring
- **Solution**: Use hardware with constant-power RF shielding
- **Tags**: rf-sidechannel, hybrid-crypto-leak

## Wi-Fi Captive Portal Forces TLS Version Downgrade Before PQ App Launch

- **Attack Type**: Downgrade via Captive Delay
- **Target**: PQ-enabled App
- **Vulnerability**: TLS fallback triggered due to captive delay
- **MITRE**: T1071.001 (Web Protocols), T1600
- **Impact**: Legacy RSA tunnel established
- **Tools**: WiFi-Pumpkin3, tcpdump, Burp Suite
- **Scenario**: A captive portal delays internet access, forcing early-launch PQ apps to retry using legacy TLS (v1.0/1.1), bypassing PQ handshake.
- **Attack Steps**: Step 1: Create a rogue Wi-Fi access point with captive portal using WiFi-Pumpkin3. Step 2: Block outbound traffic (except HTTP/port 80) using iptables. Step 3: The victim connects and opens a PQ-enabled app (e.g., secure messenger). Step 4: The app tries to initiate a hybrid handshake, fails due to portal delay. Step 5: The app automatically falls back to legacy TLS 1.0 + RSA handshake. Step 6: Capture and analyze this handshake using tcpdump.
- **Detection**: TLS version mismatch in logs
- **Solution**: Require TLS 1.3 or PQ-TLS, detect captive
- **Tags**: tls-downgrade, captive-portal, pq-handshake-bypass

## BLE-Based Key Wrapping Library Downgrade in PQ Device Pairing

- **Attack Type**: BLE Exploit
- **Target**: BLE Pairing Devices
- **Vulnerability**: PQ wrapping not enforced during BLE sync
- **MITRE**: T1557.003, T1600
- **Impact**: Legacy crypto reuse, device compromise
- **Tools**: gattacker, BLEAH, hcitool
- **Scenario**: An attacker intercepts BLE-based PQ device pairing and forces it to use a legacy key-wrapping library (e.g., AES or RSA), bypassing PQ-safe options.
- **Attack Steps**: Step 1: Use hcitool to scan BLE-enabled devices (e.g., smart locks, tokens). Step 2: Clone a BLE pairing service using gattacker. Step 3: The victim device attempts to pair, believing the attacker’s device is legitimate. Step 4: During the pairing, the attacker advertises support for only AES or RSA-based key wrapping. Step 5: If the victim device lacks strict PQ enforcement, it completes the handshake with legacy key wrapping. Step 6: Attacker logs and reuses the shared secret for unauthorized access.
- **Detection**: BLE logs & handshake analysis
- **Solution**: Require PQ-wrapping or ECDH/PQC enforcement
- **Tags**: ble, key-wrapping-downgrade, hybrid-handshake

## Brute-Forcing Weak Drone Wi-Fi Pre-Shared Keys

- **Attack Type**: Drone Wi-Fi Attack
- **Target**: Consumer/Commercial Drones
- **Vulnerability**: Weak WPA2 PSK
- **MITRE**: T1110 (Brute Force)
- **Impact**: Drone Takeover, Surveillance
- **Tools**: hcxdumptool, hashcat, rockyou.txt
- **Scenario**: Consumer and commercial drones often rely on legacy WPA/WPA2-PSK networks with weak passwords. Attackers can capture the handshake and brute-force the key.
- **Attack Steps**: Step 1: Scan Wi-Fi networks using hcxdumptool to identify the drone’s SSID and BSSID (e.g., "Drone_Camera_01"). Step 2: Capture PMKID or 4-way handshake from the drone controller or app connection. Step 3: Use hcxpcapngtool to convert the capture to Hashcat format. Step 4: Launch dictionary-based brute-force using hashcat and a wordlist like rockyou.txt. Step 5: On success, connect to the drone’s Wi-Fi and intercept control or video data.
- **Detection**: Unusual logins; deauth packets in logs
- **Solution**: Use strong passphrases or certificate-based auth
- **Tags**: Drone, Wi-Fi, WPA2, Quantum Risk

## Cracking Legacy Wireless Mesh Networks Using Static AES Keys

- **Attack Type**: Wireless Mesh Cryptanalysis
- **Target**: Wireless Mesh Nodes
- **Vulnerability**: Static Symmetric Key
- **MITRE**: T1609.002 (Protocol Impersonation)
- **Impact**: Eavesdropping, Network Manipulation
- **Tools**: Kismet, Wireshark, Meshalyzer
- **Scenario**: Older mesh networks (e.g., military or municipal) used static AES keys shared across nodes, which are vulnerable to packet capture and key recovery.
- **Attack Steps**: Step 1: Use Kismet to detect and capture traffic on the mesh protocol (e.g., 802.11s or proprietary). Step 2: Analyze captured packets in Wireshark to identify data and management frames. Step 3: Extract and attempt brute-force or dictionary attack on static AES key used to encrypt payloads. Step 4: Use recovered key to decrypt real-time mesh traffic and inject false routing or data packets. Step 5: Simulate node impersonation by spoofing MAC and sending control messages.
- **Detection**: Route anomalies; excessive routing updates
- **Solution**: Rotate keys periodically; use TLS tunnels in mesh
- **Tags**: Mesh Network, AES, Legacy

## Sniffing Proprietary Medical Wireless Protocols with No Encryption

- **Attack Type**: Medical RF Protocol Exploit
- **Target**: Medical IoT Devices
- **Vulnerability**: Unencrypted Proprietary RF
- **MITRE**: T1609.001 (Data Intercept)
- **Impact**: Health Data Leakage, Misleading Monitors
- **Tools**: RTL-SDR, URH, SigDigger
- **Scenario**: Legacy medical devices like infusion pumps and monitors may transmit over 400–900 MHz using proprietary, unencrypted protocols.
- **Attack Steps**: Step 1: Use SigDigger or RTL-SDR spectrum analyzer to locate active medical device frequencies. Step 2: Capture RF signals using URH and analyze timing and modulation (e.g., FSK, ASK). Step 3: Identify known header patterns and decode sensor values (e.g., heart rate, IV levels). Step 4: Replay or alter values to simulate false readings (educational simulation only). Step 5: Log timestamps and build a decoded stream of medical data for training.
- **Detection**: RF interference logs; checksum mismatch
- **Solution**: Migrate to encrypted BLE or Wi-Fi Medical IoT
- **Tags**: Medical, RF, Quantum Risk

## Decrypting Traffic in Legacy Home Automation over 433MHz

- **Attack Type**: 433MHz Signal Replay Attack
- **Target**: Home RF Devices
- **Vulnerability**: Fixed Code Protocols
- **MITRE**: T1609 (Data Manipulation)
- **Impact**: Unauthorized Access, Replay
- **Tools**: RTL-SDR, rc-switch, Arduino
- **Scenario**: Many early home automation devices (e.g., remotes, door sensors) use 433 MHz RF with fixed codes and no encryption.
- **Attack Steps**: Step 1: Use RTL-SDR to monitor 433 MHz frequency and capture remote control commands (e.g., garage door open/close). Step 2: Use rc-switch Arduino library to decode pulse patterns and repeatable signal IDs. Step 3: Analyze the pulse width and convert the waveform into binary to identify ON/OFF patterns. Step 4: Re-broadcast the captured binary code using Arduino RF transmitter. Step 5: Observe successful control over the device (e.g., triggering alarm, opening door).
- **Detection**: Duplicate signals in logs; excessive triggering
- **Solution**: Use rolling-code or encrypted RF protocols
- **Tags**: 433MHz, RF, Home IoT

## Eavesdropping Smart Meters with Legacy Zigbee Profiles

- **Attack Type**: Zigbee Energy Monitor Attack
- **Target**: Smart Meters (Zigbee)
- **Vulnerability**: Weak Link Key / No Encryption
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Privacy Breach, Profiling
- **Tools**: KillerBee, zbdump, ZBOSS
- **Scenario**: Smart meters using early Zigbee Smart Energy Profile (SEP 1.x) transmit usage data in plaintext or with static keys, vulnerable to eavesdropping.
- **Attack Steps**: Step 1: Use zbstumbler to detect Zigbee Smart Energy PAN ID and associated endpoints. Step 2: Capture traffic with zbdump and isolate payloads containing consumption or billing data. Step 3: If encryption exists, test for use of default link keys (e.g., ZigbeeAlliance09). Step 4: Decrypt messages or observe plaintext traffic to map user behavior (e.g., appliance usage). Step 5: Demonstrate how data could be harvested for profiling or energy theft scenarios.
- **Detection**: Zigbee log anomalies; endpoint enumeration
- **Solution**: Upgrade to SEP 2.0+ with key rotation
- **Tags**: Zigbee, Smart Energy, Legacy

## Cracking Encrypted Walkie-Talkie Voice with Known Key Leakage

- **Attack Type**: Digital Voice Decryption
- **Target**: Encrypted Walkie-Talkies
- **Vulnerability**: Static/Leaked Keys
- **MITRE**: T1123 (Audio Capture)
- **Impact**: Voice Interception, Espionage
- **Tools**: RTL-SDR, DSDPlus, Radioreference DB
- **Scenario**: Some encrypted walkie-talkies (e.g., DMR or NXDN) from early models used static keys or leaked factory test keys. Attackers can intercept and decode audio.
- **Attack Steps**: Step 1: Identify digital voice transmission on UHF band using RTL-SDR. Step 2: Use DSDPlus to decode digital audio streams (e.g., DMR Tier I). Step 3: Test static encryption keys from factory defaults or online leaked sources. Step 4: If successful, extract cleartext voice communication from the signal. Step 5: Log conversations and time stamps for replay or auditing simulations.
- **Detection**: Interference or unauthorized decoding alerts
- **Solution**: Use rotating AES keys and key loaders
- **Tags**: Radio, Voice, Digital

## Wi-Fi WPS Downgrade Exploit in PQC-Enabled Devices

- **Attack Type**: WPS Downgrade via Protocol Fallback
- **Target**: PQC-ready routers with WPS fallback
- **Vulnerability**: WPS forces fallback to WPA2-Personal with classical crypto
- **MITRE**: T1210 (Exploitation of Remote Services)
- **Impact**: PQC security bypassed by legacy WPS weakness
- **Tools**: Reaver, Wifite, Airgeddon
- **Scenario**: PQC-enabled routers with legacy WPS still active can be exploited to fall back to non-PQC key exchanges.
- **Attack Steps**: Step 1: Identify Wi-Fi APs with PQC support and WPS enabled using Wifite.Step 2: Use Reaver to brute-force the WPS PIN.Step 3: During PIN negotiation, observe that router disables PQC for backward compatibility.Step 4: Capture WPA handshake and decrypt with classical methods.Step 5: Log credentials and establish a non-PQC session.Step 6: Demonstrate risk to students through replays.
- **Detection**: Monitor for WPS PIN usage and log downgrade events
- **Solution**: Disable WPS, enforce WPA3-SAE with PQC-only TLS
- **Tags**: downgrade, WPS, WPA2, brute-force

## Zigbee-Based Home Automation Downgrade via PAN ID Spoofing

- **Attack Type**: Downgrade via PAN ID Hijack
- **Target**: Zigbee smart devices (lights, thermostats)
- **Vulnerability**: Devices do not verify PQC key before rejoining network
- **MITRE**: T1557.004 (Protocol Downgrade)
- **Impact**: Users believe PQC is active, but traffic is not encrypted post-rejoin
- **Tools**: KillerBee, ZBOSS Sniffer, Zigbee Rejoin Flood
- **Scenario**: An attacker spoofs the PAN ID and forces devices into rejoining the network with classical encryption only.
- **Attack Steps**: Step 1: Scan for Zigbee networks and PAN IDs using ZBOSS.Step 2: Use KillerBee to send spoofed rejoin requests with false PAN IDs.Step 3: Device interprets the network as new and reverts to default classical crypto.Step 4: Capture key exchange traffic.Step 5: Log session key for further use.Step 6: Run simulation to show downgrade vulnerability.
- **Detection**: Log rejoin events and validate cipher level
- **Solution**: Bind PAN ID to cryptographic identity with signed rejoin tokens
- **Tags**: zigbee, downgrade, PAN spoof, automation

## PQC Tunnel Downgrade Over Wireless VPN via TLS Strip

- **Attack Type**: TLS Strip on PQC VPN Over Wi-Fi
- **Target**: VPN Clients over Wi-Fi
- **Vulnerability**: PQC not enforced on server side during cipher negotiation
- **MITRE**: T1557.002 (SSL Strip)
- **Impact**: PQC VPNs become vulnerable to passive collection and future decryption
- **Tools**: Bettercap, mitmproxy, EvilAP
- **Scenario**: A MITM attacker strips PQC VPN TLS extensions during connection, forcing client to connect using RSA or classical ECDSA.
- **Attack Steps**: Step 1: Create an EvilAP that mimics the organization's Wi-Fi SSID.Step 2: Use Bettercap to intercept traffic and mitmproxy to rewrite TLS handshakes.Step 3: Remove PQC cipher suites from the client hello.Step 4: Forward modified packets to VPN endpoint.Step 5: VPN negotiates fallback using classical TLS.Step 6: Log keys and session for quantum analysis.Step 7: Simulate post-session quantum decryption.
- **Detection**: Detect missing PQC suites in TLS negotiation
- **Solution**: Enforce strict PQC-only cipher list on client and server
- **Tags**: vpn, downgrade, TLS strip, PQC

## Wi-Fi 7 Fast Initial Link Setup (FILS) PQC Downgrade

- **Attack Type**: Downgrade during FILS Handshake
- **Target**: Wi-Fi 7 routers and devices
- **Vulnerability**: FILS doesn't validate PQC policy enforcement
- **MITRE**: T1584.005 (Compromise Infrastructure: Wireless)
- **Impact**: Next-gen Wi-Fi connections compromised via fallback
- **Tools**: Hostapd, Wireshark, Scapy
- **Scenario**: Wi-Fi 7 devices using PQC FILS handshake can be tricked into using classical handshake via malformed handshake packets.
- **Attack Steps**: Step 1: Configure rogue Wi-Fi 7 AP with FILS.Step 2: Use Scapy to intercept and modify handshake frames.Step 3: Remove PQC extensions and forward them to the client.Step 4: Client falls back to classical handshake.Step 5: Log negotiation session and analyze in Wireshark.Step 6: Replay in lab to simulate attack result.
- **Detection**: Monitor FILS messages for PQC capability flags
- **Solution**: Add PQC enforcement field in FILS negotiation
- **Tags**: downgrade, FILS, Wi-Fi 7, handshake spoof

## Bluetooth Mesh PQC Downgrade via Relay Node Impersonation

- **Attack Type**: Mesh Network Downgrade via Node Spoofing
- **Target**: Bluetooth mesh IoT systems
- **Vulnerability**: Mesh devices don’t validate PQC fingerprint on peers
- **MITRE**: T1071.001 (Application Layer Protocol)
- **Impact**: Full mesh comms downgraded; messages logged in plaintext
- **Tools**: bt-mesh-devkit, Ubertooth, Mesh Flooding Tool
- **Scenario**: Bluetooth mesh nodes using PQC key exchange are impersonated, causing key renegotiation using classical crypto.
- **Attack Steps**: Step 1: Scan and identify Bluetooth mesh topology.Step 2: Spoof a mesh relay node using bt-mesh-devkit.Step 3: Flood with rekeying requests containing classical parameters.Step 4: Other nodes accept and rekey using classical algorithms.Step 5: Capture traffic during mesh sync.Step 6: Demonstrate in lab how trust in rogue node causes fallback.
- **Detection**: Log mesh rekey events and cipher type
- **Solution**: Mesh whitelisting with PQC-cert fingerprint enforcement
- **Tags**: mesh, Bluetooth, PQC fallback, impersonation

## Wi-Fi Management Frame Downgrade via Beacon Tampering

- **Attack Type**: Beacon Spoof Attack to Force Downgrade
- **Target**: Wi-Fi clients (mobile, laptops)
- **Vulnerability**: Clients do not verify PQC capability via multiple APs
- **MITRE**: T1566.001 (Spearphishing via Service)
- **Impact**: Unaware fallback to classical WPA2 session
- **Tools**: mdk4, Wireshark, Hostapd
- **Scenario**: An attacker crafts Wi-Fi beacon frames indicating classical-only support, tricking PQC-capable clients into legacy mode.
- **Attack Steps**: Step 1: Identify target AP and client pairing.Step 2: Use mdk4 to flood the client with spoofed beacon frames with altered capabilities (no PQC advertised).Step 3: Client connects assuming PQC unsupported.Step 4: Log connection and observe fallback to WPA2.Step 5: Demonstrate in classroom how beacon spoofing controls encryption choice.
- **Detection**: Log beacon content and PQC advertisement flags
- **Solution**: Require user confirmation or validation of PQC beacon
- **Tags**: spoofing, beacon, downgrade, Wi-Fi

## NFC-Based Access Control Downgrade via Proximity Emulator

- **Attack Type**: PQC Fallback via Range-Based Handshake Injection
- **Target**: NFC smartcards and readers
- **Vulnerability**: Protocol preference based on proximity or power
- **MITRE**: T1557.001 (Man-in-the-Middle)
- **Impact**: Physical presence results in silent fallback
- **Tools**: Proxmark3, NFCTools, Android NFC Emulator
- **Scenario**: A smart card using PQC attempts is forced to classical by an attacker who simulates low-power legacy readers nearby.
- **Attack Steps**: Step 1: Emulate a legacy reader with low PQC capacity using NFC emulator.Step 2: Position emulator close to the card while approaching real PQC reader.Step 3: Card gets confused by signal priority and falls back to classical handshake.Step 4: Log handshake using Proxmark3.Step 5: Replay for educational simulation.Step 6: Show power-based handshake priority effect.
- **Detection**: Audit handshake origin and priority
- **Solution**: Force PQC-only handshake even in weak signal
- **Tags**: downgrade, proximity, NFC, spoof reader

## LoRaWAN OTAA Join Downgrade Using Timing Mismatch

- **Attack Type**: Downgrade via Join-Accept Delay Exploit
- **Target**: LoRaWAN devices with OTAA
- **Vulnerability**: Retry logic does not prioritize PQC-only attempts
- **MITRE**: T1498.002 (Communication Delay)
- **Impact**: Key exchange in LPWAN becomes non-PQC without user knowledge
- **Tools**: SDR, GNURadio, LoRa Repeater, Scapy
- **Scenario**: By delaying PQC handshake responses, attacker forces OTAA clients to retry with classical keys.
- **Attack Steps**: Step 1: Set up rogue LoRaWAN gateway with SDR.Step 2: Let Join Request go through with PQC extensions.Step 3: Delay Join-Accept reply until timeout.Step 4: Device retries using fallback classical Join.Step 5: Log handshake and use in decryption demo.Step 6: Repeat to show reliability of attack.
- **Detection**: Check timing of Join-Accept vs key type used
- **Solution**: Enforce retry with PQC-or-abort logic
- **Tags**: lora, downgrade, OTAA, timing

## Zigbee OTA Update Downgrade via PQC Extension Removal

- **Attack Type**: Downgrade via Update Payload Tampering
- **Target**: Zigbee smart home devices
- **Vulnerability**: PQC update signature not enforced or validated
- **MITRE**: T1601.001 (Modify System Firmware)
- **Impact**: Firmware signed classically instead of PQC
- **Tools**: Zigbee OTA tool, Wireshark, Zigpy
- **Scenario**: OTA update packets are intercepted and modified to remove PQC support, tricking devices to accept classical-only update.
- **Attack Steps**: Step 1: Identify Zigbee OTA update packets using sniffer.Step 2: Use a Zigbee OTA relay or proxy to modify packets in transit.Step 3: Strip PQC signature field and change to legacy checksum.Step 4: Device accepts and installs update with classical crypto.Step 5: Verify firmware downgrade and demonstrate breach.Step 6: Show how attacker gains long-term access.
- **Detection**: Log firmware update source and hash type
- **Solution**: Require PQC signature validation on firmware updates
- **Tags**: firmware, OTA, downgrade, Zigbee

## PQC VoWiFi Downgrade via SIP Re-invite Injection

- **Attack Type**: SIP Header Manipulation to Drop PQC Cipher
- **Target**: SIP over Wi-Fi (VoWiFi clients)
- **Vulnerability**: SIP sessions renegotiate without validating PQC preference
- **MITRE**: T1071.001 (Application Protocol Exploitation)
- **Impact**: PQC-secure voice degraded to classical
- **Tools**: SIPp, Wireshark, mitmproxy
- **Scenario**: VoWiFi over SIP using PQC is downgraded by injecting a re-INVITE header that strips PQC ciphers.
- **Attack Steps**: Step 1: Intercept SIP session between client and VoWiFi server.Step 2: Inject a re-INVITE message with modified crypto attributes.Step 3: Strip PQC cipher options from SDP.Step 4: Session renegotiates with classical cipher.Step 5: Capture and store voice packets.Step 6: Replay and analyze loss of PQC.
- **Detection**: Log SIP INVITE headers and attribute changes
- **Solution**: Enforce PQC cipher lock in SIP policies
- **Tags**: VoWiFi, SIP, downgrade, PQC bypass

## PQC IoT Drone Comm Downgrade via GPS Spoof Redirection

- **Attack Type**: Downgrade by Forcing Device to Enter Fail-Safe Mode
- **Target**: PQC drone telemetry systems
- **Vulnerability**: Fail-safe mode assumes lowest crypto for reliability
- **MITRE**: T1499.001 (Data Encrypted for Impact)
- **Impact**: Flight and control logs exposed to future decryption
- **Tools**: GPS-SDR-sim, HackRF, Drone Telemetry Analyzer
- **Scenario**: Drone with PQC encrypted telemetry enters legacy comms mode upon spoofed GPS coordinates triggering fail-safe.
- **Attack Steps**: Step 1: Identify drone model and PQC firmware.Step 2: Use GPS-SDR-sim with HackRF to broadcast spoofed coordinates.Step 3: Trigger geo-fencing or fail-safe fallback mode.Step 4: Observe telemetry comms switch to classical encryption.Step 5: Intercept and log data stream.Step 6: Show how critical systems fallback under perceived threat.
- **Detection**: Audit comms during mode switches
- **Solution**: Require PQC even in fail-safe states
- **Tags**: drone, GPS spoofing, fallback, PQC

## Laser Speckle Fault Injection on Quantum Optics

- **Attack Type**: Optical Speckle Attack
- **Target**: Optical Quantum System
- **Vulnerability**: Photonic sensor susceptibility to light interference
- **MITRE**: T1603.001 (Optical Fault Injection)
- **Impact**: Photonic decoherence, misread states
- **Tools**: Laser Diode, Diffuser Lens, IR Filter, Beam Stabilizer
- **Scenario**: A laser is directed through an air vent or window onto an optical quantum device, generating speckle patterns that interfere with photonic qubit readouts.
- **Attack Steps**: Step 1: Identify a line-of-sight path into the quantum optics lab (e.g., a vent or untreated window).Step 2: Set up a laser diode with a rotating diffuser lens to generate dynamic speckle patterns.Step 3: Focus the beam using a stabilizer to ensure precision and avoid lab sensors.Step 4: Activate the laser during photon-based quantum operations (e.g., readout or entanglement phase).Step 5: Monitor for flickers, misread photons, or alignment errors in quantum state readings.Step 6: Record any inconsistencies in the Bell test or quantum tomography results.Step 7: Adjust lens patterns to tune intensity and observe threshold of tolerance.
- **Detection**: Photon detector logs, light noise analysis
- **Solution**: Anti-reflection film, photonic filtering
- **Tags**: #LaserSpeckle #OpticalQuantum #PhotonFault

## Wireless Glitch Injection During Cryostat Reinitialization

- **Attack Type**: Radio Timing Glitch Injection
- **Target**: Cryogenic Rebooted Qubit System
- **Vulnerability**: Reinitialization logic susceptible to timing faults
- **MITRE**: T1599.002 (Initialization Phase Glitching)
- **Impact**: Misconfigured logic, unstable gate patterns
- **Tools**: SDR (HackRF), Clock Glitch Injector, EM Probe
- **Scenario**: During the cooldown reboot of a dilution refrigerator, RF noise is injected to cause configuration faults in FPGA-controlled qubit modules.
- **Attack Steps**: Step 1: Monitor lab operation schedule to time the reinitialization phase of the cryogenic system (cooling after maintenance).Step 2: Deploy an SDR or RF generator nearby and observe clock and configuration transmission frequencies.Step 3: Inject precisely timed bursts of RF or glitches into the control band used by FPGAs to initialize gate logic.Step 4: Log any anomalies such as FPGA misconfiguration, stuck bits, or logic skips.Step 5: Compare final quantum gate behavior against standard performance post-cooling.Step 6: Repeat injection at different phases to identify weakest moment in reboot.Step 7: Simulate recovery via firmware reflash and monitor result.
- **Detection**: FPGA register dump, control signal validation
- **Solution**: Add startup integrity checks, clock stabilizers
- **Tags**: #CryostatGlitch #FPGAError #QuantumStartup

## Bluetooth-Based Fault Trigger on Lab Monitoring Sensors

- **Attack Type**: Bluetooth Exploitation Fault
- **Target**: Bluetooth Sensor System
- **Vulnerability**: Lack of Bluetooth authentication
- **MITRE**: T0807 (Wireless Protocol Abuse)
- **Impact**: Gate correction error, miscompensated noise
- **Tools**: Bluetooth Sniffer, Packet Injector, Blue Hydra
- **Scenario**: A quantum lab’s environmental sensors (temperature, humidity) use unsecured Bluetooth and are flooded with malicious packets, corrupting the readings used for quantum error compensation.
- **Attack Steps**: Step 1: Scan for Bluetooth-enabled environmental monitors inside or near the lab.Step 2: Identify MAC addresses, firmware version, and pairing status using Blue Hydra or Ubertooth.Step 3: Use a Bluetooth packet injector to send malformed packets or cause buffer overflow (e.g., flood GATT read/write).Step 4: During quantum execution, inject noise to confuse environmental compensation models.Step 5: Observe whether gate correction algorithms malfunction due to false sensor data.Step 6: Capture logs from the sensors and compare with normal readings.Step 7: Simulate emergency reboot and verify restoration behavior.
- **Detection**: Compare raw sensor data with lab metrics
- **Solution**: Disable Bluetooth, switch to wired telemetry
- **Tags**: #BluetoothFault #SensorDisruption #QuantumError

## Long-Range EM Reflection via Building Infrastructure

- **Attack Type**: Indirect EM Injection
- **Target**: Indirect-Path EM Coupling to Quantum Lab
- **Vulnerability**: Structural EM reflection vulnerability
- **MITRE**: T0810 (EM Signal Injection via Reflection)
- **Impact**: Faulty computation due to indirect EM
- **Tools**: High-Gain Yagi Antenna, Signal Generator, EM Reflector Map
- **Scenario**: Attacker uses a microwave antenna to bounce EM off nearby metal structures (rooftop beams, HVAC units) to reach quantum hardware indirectly.
- **Attack Steps**: Step 1: Map metallic infrastructure near the quantum facility using drone imagery or architectural plans.Step 2: Position a high-gain directional antenna aimed at a rooftop or external metal beam that reflects toward the quantum lab.Step 3: Send pulsed microwave energy at 2.4–3.5 GHz with timed intervals.Step 4: Measure reflected EM intensity at the lab entrance or near hardware if accessible.Step 5: Observe if quantum operations show glitches, increased gate error rates, or increased heat signatures.Step 6: Repeat with different angles to maximize EM exposure.Step 7: Compare results against baseline runs.
- **Detection**: Field strength logs, thermal rise near hardware
- **Solution**: Architectural shielding, ground-plane isolation
- **Tags**: #EMReflection #IndirectFault #QuantumLabAttack

## Wireless Voltage Spike Induction on Qubit Control Rails

- **Attack Type**: Power Line Fault Injection
- **Target**: Power Rails of Qubit Controller
- **Vulnerability**: No surge filters or EM isolation
- **MITRE**: T1603.001 (Power Fault Injection)
- **Impact**: Spontaneous restarts, state collapse
- **Tools**: Inductive Coil, SDR, Oscilloscope
- **Scenario**: By transmitting high-frequency signals near power lines, attacker induces transient voltage spikes in qubit control rails.
- **Attack Steps**: Step 1: Identify external power lines or control cable entries into the quantum lab.Step 2: Wrap a copper induction coil around an exposed conduit outside (e.g., server room entry).Step 3: Connect to SDR and emit strong high-frequency bursts (10–50 MHz).Step 4: Use oscilloscope on control rail (in lab simulation) to observe voltage ripple.Step 5: Note any response from power stabilization unit, including overvoltage events.Step 6: Execute quantum gate operation while continuing bursts and log faults.Step 7: Use EM probe to ensure leakage path is feasible.
- **Detection**: Power fluctuation logs, EM trace logs
- **Solution**: Use surge protectors, RF-isolated power inputs
- **Tags**: #PowerSpike #VoltageInjection #QuantumFault

## Smartwatch RF Emission Exploit During Lab Visit

- **Attack Type**: RF Leakage Attack
- **Target**: Quantum Execution Lab
- **Vulnerability**: Insider RF source, no RF screening
- **MITRE**: T0806 (Internal Wireless Interference)
- **Impact**: Subtle but repeatable logic errors
- **Tools**: Modified Smartwatch App, BLE Beacon Monitor, RF Sniffer
- **Scenario**: An insider enters the lab with a smartwatch programmed to emit silent RF bursts, causing silent, small-scale interference during computation.
- **Attack Steps**: Step 1: Deploy a custom smartwatch app that emits silent BLE/RF pulses at 2.4 GHz intermittently.Step 2: Have the user enter the quantum lab as a visitor (simulate via insider role).Step 3: Time the app to emit stronger pulses during critical computation windows.Step 4: Use RF sniffer in lab to detect unexpected traffic.Step 5: Log quantum computation failures and match timestamps.Step 6: After visitor leaves, repeat computation and compare with prior results.Step 7: Correlate smartwatch emissions with induced computation noise.
- **Detection**: BLE monitor logs, RF spectrum analyzer
- **Solution**: Enforce RF-free zone, visitor scans
- **Tags**: #SmartwatchExploit #BLEAttack #QuantumLab

## Wi-Fi Interference to Skew Quantum Randomness

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum IoT Device
- **Vulnerability**: EM Interference Susceptibility
- **MITRE**: T1401 (Electromagnetic Interference)
- **Impact**: Predictable encryption keys
- **Tools**: HackRF One, Wi-Fi jammer, SDR#
- **Scenario**: Attacker uses targeted Wi-Fi interference to influence EM-sensitive quantum RNGs used in nearby quantum-secure devices.
- **Attack Steps**: Step 1: Identify a device using QRNG via electromagnetic (EM) emissions using an SDR scanner. Step 2: Analyze the frequency ranges QRNG operates in. Step 3: Use a Wi-Fi jammer configured to broadcast interference on those frequencies. Step 4: Monitor QRNG output over time using entropy analysis tools. Step 5: Confirm pattern deviation from ideal randomness. Step 6: Launch entropy-reduction exploit on target quantum encryption relying on QRNG output.
- **Detection**: EM emission anomaly detection tools
- **Solution**: Harden shielding, filter EM bands, relocate devices
- **Tags**: Quantum RNG, Wi-Fi, EM Attacks, Side-channel

## Bluetooth Beacon Saturation for RNG Fault Injection

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum-Comms Gateway
- **Vulnerability**: Entropy fault via spectrum flooding
- **MITRE**: T1461 (Signal Interference)
- **Impact**: Compromised encryption
- **Tools**: BlueZ, Bluetooth beacon spammer, QKD analyzer
- **Scenario**: Attacker floods Bluetooth spectrum near a QRNG-equipped device, causing timing disruptions and entropy faults.
- **Attack Steps**: Step 1: Identify quantum RNG-based device operating near Bluetooth channels. Step 2: Deploy multiple BLE beacon spam devices around the target. Step 3: Monitor timing jitter and entropy response of the QRNG. Step 4: Inject specific signal patterns to cause correlation in RNG output. Step 5: Use correlation analysis to predict bits used in quantum keys. Step 6: Capture and decrypt encrypted communications based on flawed QRNG.
- **Detection**: Entropy deviation detectors, time jitter logs
- **Solution**: Channel hopping, beacon filters, RNG fault protection
- **Tags**: BLE Flood, RNG Timing, Signal Faults

## Zigbee Signal Collision to Induce Randomness Bias

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Zigbee-enabled Quantum Edge Devices
- **Vulnerability**: RF-induced RNG bias
- **MITRE**: T1422 (RF Jamming)
- **Impact**: Reduced entropy in keys
- **Tools**: KillerBee, ZigbeeSniffer, EntropyPlot
- **Scenario**: Zigbee collisions are used to create statistical bias in nearby QRNGs that depend on RF-based triggers.
- **Attack Steps**: Step 1: Scan for Zigbee networks using ZigbeeSniffer. Step 2: Analyze time/frequency slot utilization. Step 3: Begin injecting crafted Zigbee collisions near QRNG sensors. Step 4: Collect and analyze QRNG outputs for distribution skew. Step 5: Determine bias pattern and adapt signal injection accordingly. Step 6: Exploit predictable bits in QKD to eavesdrop on sessions.
- **Detection**: Statistical randomness tests
- **Solution**: Secure Zigbee stack, EM shielding, watchdogs
- **Tags**: Zigbee, RNG Bias, Signal Collision

## Directional EM Pulse Injection via Parabolic Wi-Fi

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum Testbed Device
- **Vulnerability**: Poor shielding on RNG
- **MITRE**: T1401 (EM Injection)
- **Impact**: Cryptographic bypass
- **Tools**: TP-Link directional antenna, WiFiPumpkin3, SDR#
- **Scenario**: Attacker uses directional Wi-Fi antenna to induce EM pulses into a QRNG circuit causing biased entropy.
- **Attack Steps**: Step 1: Calibrate a parabolic antenna to beam high-power Wi-Fi signals at the target lab/device. Step 2: Fire controlled pulse bursts matching QRNG sampling windows. Step 3: Use SDR to capture QRNG signal response and entropy fluctuations. Step 4: Iterate and fine-tune pulses to induce predictable biases. Step 5: Record resulting RNG values and use for key inference. Step 6: Demonstrate encrypted traffic decryption.
- **Detection**: EM pulse spectrum logging
- **Solution**: Hardened cases, RF filters, monitoring
- **Tags**: Wi-Fi Pulse, EM Injection, Parabolic

## RFID-Based RNG Injection via Near-Field Crosstalk

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: RFID-Enabled Security Chip
- **Vulnerability**: RFID Crosstalk
- **MITRE**: T1421 (Signal Spoofing)
- **Impact**: Predictable encryption patterns
- **Tools**: Proxmark3, RFID emulator, entropy auditor
- **Scenario**: RFID signals injected near QRNG components cause cross-talk and influence random bit generation patterns.
- **Attack Steps**: Step 1: Locate target device using RFID reader near a quantum RNG chip. Step 2: Replay and amplify RFID signals near the RNG circuits. Step 3: Use electromagnetic crosstalk to alter quantum bit behavior. Step 4: Record QRNG output and analyze for statistically repeating segments. Step 5: Validate bias using entropy auditor tools. Step 6: Launch predictable key generation exploit.
- **Detection**: Side-channel logging, crosstalk analyzers
- **Solution**: Physical isolation, RFID filtering circuits
- **Tags**: RFID, RNG Fault, Quantum Bit Bias

## Wi-Fi Beacon Interval Exploit to Sync RNG Sampling

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum RNG Module in Embedded Device
- **Vulnerability**: Timing sync vulnerabilities
- **MITRE**: T1499.004 (Resource Hijacking)
- **Impact**: RNG predictability
- **Tools**: Wireshark, WiFiJammer, RNG timing logger
- **Scenario**: Exploiting the beacon timing from a Wi-Fi AP to synchronize with RNG sampling cycles and induce deterministic entropy.
- **Attack Steps**: Step 1: Sniff beacon interval and timestamp information from nearby access points using Wireshark. Step 2: Identify overlap with QRNG sampling clock. Step 3: Modify beacon transmission intervals using spoofed AP. Step 4: Sync malicious beacon pulses with RNG timing edge. Step 5: Observe entropy drift using RNG timing logger. Step 6: Correlate and reconstruct parts of the QRNG output for cryptanalysis.
- **Detection**: Entropy/time correlation tools
- **Solution**: Desync mitigation, random delay injection
- **Tags**: Wi-Fi Beacon Attack, RNG Clock Hijack

## Wi-Fi-Based Entropy Injection into Quantum RNG Buffers

- **Attack Type**: Quantum Trojan Horse via Wireless Entropy Pollution
- **Target**: Quantum RNG in QKD
- **Vulnerability**: Susceptibility of entropy sources to wireless noise
- **MITRE**: T1601 (Modify System Image)
- **Impact**: Predictable entropy → weak key generation
- **Tools**: Wi-Fi SDR, environmental EM probe, entropy monitor
- **Scenario**: An attacker wirelessly injects signals that influence environmental sensors (e.g., temperature, noise) feeding into quantum RNGs, polluting the entropy source.
- **Attack Steps**: Step 1: Identify quantum RNGs relying on environmental noise sources (e.g., thermal noise, jitter, ambient EM radiation).Step 2: Set up a Wi-Fi SDR to generate controlled electromagnetic pulses (e.g., high-speed packet bursts).Step 3: Aim these signals at the RNG sensor enclosure.Step 4: Monitor entropy output via any available diagnostics or logs.Step 5: Observe whether entropy becomes predictable or significantly deviates from random baselines.Step 6: Capture affected key output and use statistical analysis tools (e.g., NIST STS) to check degradation.Step 7: Replay attack in controlled rounds to extract patterns and reconstruct entropy states.
- **Detection**: RNG entropy monitor, deviation logs
- **Solution**: Shield RNGs; use quantum sources isolated from EM
- **Tags**: #entropyinjection #rngattack #wirelessinterference

## Covert Channel Creation via LED Flickering on QKD Units

- **Attack Type**: Quantum Trojan Horse via Wireless Light Modulation
- **Target**: Front panel of QKD device
- **Vulnerability**: LED controlled by firmware; no light shielding
- **MITRE**: T1027.002 (Covert Channel)
- **Impact**: Physical side-channel leak of private key
- **Tools**: BLE-enabled microcontroller, light sensor (e.g., LDR), oscilloscope
- **Scenario**: Compromised QKD unit uses status LEDs to transmit key material in Morse-like code via LED brightness or flickering, picked up wirelessly by a light sensor.
- **Attack Steps**: Step 1: Implant malware in the QKD firmware to control front-panel status LEDs.Step 2: During or after key generation, convert the key data into timed LED pulses.Step 3: Use a nearby wireless microcontroller with a light sensor (ESP32 + LDR) to record the LED patterns through walls or windows.Step 4: Use BLE to transmit recorded light patterns back to the attacker’s phone.Step 5: Decode LED pulses (e.g., ON = 1, OFF = 0, or PWM patterns) to recover binary key.Step 6: Simulate decryption of traffic using stolen key to validate accuracy.Step 7: Replay full process in a low-light lab setting to show exfiltration.
- **Detection**: Light intensity monitor; firmware audit
- **Solution**: Shield LEDs; disable unused indicators in production
- **Tags**: #covertchannel #ledexfil #lightattack

## Passive Acoustic Eavesdropping on Quantum Logic Control

- **Attack Type**: Quantum Trojan Horse via Wireless Microphone
- **Target**: QKD System Chassis
- **Vulnerability**: Lack of acoustic shielding or noise masking
- **MITRE**: T1040 (Network Sniffing via Acoustic Channel)
- **Impact**: Key phase timing inference via acoustic signals
- **Tools**: Parabolic mic, wireless bug transmitter, acoustic analyzer
- **Scenario**: Attacker places wireless acoustic bug near control electronics to capture timing signals from mechanical/electrical components.
- **Attack Steps**: Step 1: Place a parabolic microphone or a small wireless acoustic bug near QKD logic board or cooling fans.Step 2: Record high-frequency mechanical vibrations and clicking noises produced during QKD logic operations.Step 3: Transmit audio over BLE or LoRa to an off-site receiver.Step 4: Use acoustic analysis tools to identify patterns corresponding to key operations (e.g., laser pulses, modulator triggers).Step 5: Time-correlate these sounds with quantum exchange sequences.Step 6: Attempt to predict when key transitions occur to infer entropy and state.Step 7: Validate findings by comparing sound-timing to protocol logs (in simulation).
- **Detection**: Audio monitoring of secure zones
- **Solution**: Soundproof QKD enclosures; noise injection
- **Tags**: #acousticsidechannel #soundleak #qkdtiming

## BLE Debug Console Exploitation on Mobile Quantum Wallet

- **Attack Type**: Quantum Trojan Horse via Wireless Mobile Access
- **Target**: Quantum Mobile Wallet
- **Vulnerability**: Debug BLE service left enabled in production
- **MITRE**: T1518.001 (Application Layer Protocol Abuse)
- **Impact**: Key leakage from mobile QKD interface
- **Tools**: Android BLE exploit tool, smartphone, BLE debugger
- **Scenario**: Attacker connects to a BLE-enabled mobile quantum wallet and activates a debug console to leak stored quantum keys.
- **Attack Steps**: Step 1: Discover BLE advertisement from the quantum wallet device.Step 2: Use Android BLE tools to initiate connection and enumerate GATT services.Step 3: Detect a hidden or undocumented debug console characteristic.Step 4: Write to the debug service to activate a response mode.Step 5: Request key logs or entropy buffer contents.Step 6: Save logs or stream them live to attacker device.Step 7: Replay the attack using simulation wallet software in lab conditions to prove exploit.
- **Detection**: BLE GATT service audits
- **Solution**: Disable debug service in production firmware
- **Tags**: #mobileqkd #bledump #quantumwallet

## Drone-Based Directed Wi-Fi Pulse Injection

- **Attack Type**: Quantum Trojan Horse via Airborne RF Injection
- **Target**: QKD Facility (Physical)
- **Vulnerability**: Open-air access; no RF shielding near vents
- **MITRE**: T1590.004 (Gather Victim Org Info via Aerial Recon)
- **Impact**: Timing desync and key degradation
- **Tools**: Drone, Wi-Fi jammer/transmitter, GPS, SDR receiver
- **Scenario**: Attacker uses a drone equipped with a directional Wi-Fi transmitter to inject pulse-modulated RF signals into an unprotected QKD facility.
- **Attack Steps**: Step 1: Program drone with GPS waypoints to hover near QKD node windows or vent areas.Step 2: Equip drone with directional Wi-Fi pulse jammer or modulator (ESP8266-based payload).Step 3: Inject short RF bursts timed to disrupt photon detection pulses.Step 4: From a distance, use an SDR to monitor changes in QKD protocol behavior (increased error rates, restarts).Step 5: Correlate drone timing logs with captured QKD metadata.Step 6: Confirm if timing-based desynchronization or fallback protocol was triggered.Step 7: Simulate full attack in an enclosed Faraday cage lab using an RF drone and test QKD setup.
- **Detection**: GPS + SDR timing correlation; flight path monitoring
- **Solution**: Harden perimeter with RF shielding; use RF intrusion detection
- **Tags**: #droneattack #qkddesync #wirelesspulse

## Bluetooth Audio Flooding Near QKD Control Console

- **Attack Type**: Bluetooth Audio Flood
- **Target**: Human-in-the-loop QKD Console
- **Vulnerability**: Bluetooth channel abuse
- **MITRE**: T0846 - Peripheral Disruption
- **Impact**: Operator delays lead to QKD timeout
- **Tools**: Smartphone, BT Speaker, Audio Flood App
- **Scenario**: Bluetooth speakers spammed with continuous signals to interfere with QKD operator coordination and time-critical decision-making.
- **Attack Steps**: Step 1: In a QKD simulation lab, connect a Bluetooth speaker to the control room console. Step 2: Use a smartphone and Bluetooth spam/flooding app to connect and repeatedly send junk audio streams. Step 3: The speaker is bombarded with sound output or repeated connect-disconnects. Step 4: Observe QKD operators' delay in manually authorizing key confirmations or managing logs due to audio confusion. Step 5: Log the time-based mismatch between human confirmation and QKD channel timing window. Step 6: Track how QKD key exchange fails due to timeouts or missed confirmations.
- **Detection**: BT log analysis, human error correlation
- **Solution**: Disable BT or isolate QKD control room devices
- **Tags**: QKD, Bluetooth, Audio DoS, Operator Disruption

## QRNG Device Interference via Electromagnetic Pulse

- **Attack Type**: EM Injection Attack
- **Target**: QKD System with Integrated QRNG
- **Vulnerability**: EM susceptibility in RNG hardware
- **MITRE**: T0871 - Entropy Disruption
- **Impact**: RNG fails → QKD protocol invalid
- **Tools**: Signal Generator, Coiled EM Transmitter, Oscilloscope
- **Scenario**: Attacker emits targeted electromagnetic pulses at QRNG (Quantum Random Number Generator) to degrade randomness and cause protocol resets.
- **Attack Steps**: Step 1: Use a lab-based QRNG module in a testbed integrated with a QKD system. Step 2: Build a simple EM pulse injector using a signal generator and coil (e.g., Tesla coil or Helmholtz coil). Step 3: Position it near the QRNG’s hardware. Step 4: Emit periodic bursts of EM signals targeting the RNG circuitry. Step 5: Observe entropy readings from QRNG showing anomalies or drop in randomness. Step 6: QKD protocol halts due to non-compliant entropy source. Step 7: Log entropy readings, QKD abort reason, and time of EM exposure.
- **Detection**: QRNG entropy logs, shielding test
- **Solution**: Faraday shielding, tamper-resistant RNGs
- **Tags**: QKD, QRNG, EM Pulse, Entropy Attack

## RFID Replay Attack to Stall Secure Lab Entry

- **Attack Type**: RFID Clone Looping
- **Target**: Lab with RFID-based Access
- **Vulnerability**: Weak replay protection
- **MITRE**: T0857 - RFID Signal Replay
- **Impact**: Physical delay disrupts quantum key window
- **Tools**: Proxmark3, Cloned RFID Card, Loop Script
- **Scenario**: Attacker replays cloned RFID signals in loops, keeping the lab entrance system locked in denial state.
- **Attack Steps**: Step 1: Simulate a lab with secure access to QKD equipment using RFID door locks. Step 2: Clone a previously used RFID tag with Proxmark3. Step 3: Launch a continuous loop of fake card scans with incorrect timing. Step 4: The access system locks out legitimate users due to repeated attempts. Step 5: Access to time-sensitive QKD calibration is blocked. Step 6: Record time delay in accessing equipment, QKD session failure due to missed window.
- **Detection**: RFID logs, door access analytics
- **Solution**: Use OTP-based tags or time-lock entries
- **Tags**: QKD, RFID, Replay, Entry Denial

## Targeted Microwave Beam to Heat QKD Optical Path

- **Attack Type**: Directed Microwave Heating
- **Target**: Free-space Optical QKD
- **Vulnerability**: Refractive index sensitivity
- **MITRE**: T0819 - Directed Energy Attack
- **Impact**: Optical misalignment → session abort
- **Tools**: Directional Microwave Emitter, Heat Sensor, Thermocouple
- **Scenario**: Attacker uses a microwave source to subtly heat the air along the free-space quantum path, changing beam alignment or refractive index.
- **Attack Steps**: Step 1: Set up a free-space QKD system with long-range optical transmission between sender and receiver. Step 2: Aim a microwave emitter near the beam path (not on hardware directly). Step 3: Emit steady microwave energy to slightly heat the surrounding air. Step 4: The temperature difference alters the air’s refractive index, subtly distorting the beam. Step 5: Photon arrival patterns at the detector become misaligned. Step 6: QBER increases due to beam divergence and session is aborted. Step 7: Use thermal sensors to log temperature changes near the beam path.
- **Detection**: Beam monitoring sensors, QBER log
- **Solution**: Use fiber instead of free-space, thermal shielding
- **Tags**: QKD, Microwave, Heating Attack, Beam Path

## Drone-Based Interference on QKD Line-of-Sight

- **Attack Type**: Airborne Obstruction DoS
- **Target**: Line-of-Sight QKD Channel
- **Vulnerability**: Open-air beam path
- **MITRE**: T0850 - Physical Channel Obstruction
- **Impact**: Key generation halted intermittently
- **Tools**: Commercial Drone (DJI, Parrot), GPS Logger
- **Scenario**: Using a drone to interrupt the line-of-sight in a free-space QKD link, simulating intermittent jamming.
- **Attack Steps**: Step 1: Establish a QKD free-space test with clear line-of-sight between two buildings. Step 2: Fly a small drone along the photon path using pre-programmed GPS coordinates. Step 3: Periodically block or partially obscure the beam. Step 4: Observe temporary drops in photon reception and rising QBER. Step 5: Repeat to create frequent outages and simulate unpredictable obstructions. Step 6: Log the correlation between drone proximity and QKD aborts.
- **Detection**: Lidar + photon count logs, visual monitoring
- **Solution**: Use beam redundancy or mesh QKD nodes
- **Tags**: QKD, Drone, LOS Attack, Aerial Interference

## RF Desynchronization of QKD Clock Signal

- **Attack Type**: Clock Drift Induction via RF
- **Target**: QKD Receiver with Oscillator
- **Vulnerability**: Susceptibility to EM coupling
- **MITRE**: T0861 - Clock Drift Manipulation
- **Impact**: Timing mismatch aborts QKD
- **Tools**: HackRF, SDR#, Function Generator
- **Scenario**: RF signal targeting QKD timing circuitry causes misalignment in photon detection timing.
- **Attack Steps**: Step 1: Set up a QKD environment using clock synchronization between sender and receiver (shared or public clock). Step 2: Identify frequency range of clock oscillator used. Step 3: Use HackRF to emit a continuous low-amplitude RF signal tuned to that frequency. Step 4: The receiver’s clock experiences minor timing drift over time. Step 5: Photon detection windows start desynchronizing, increasing QBER. Step 6: Eventually, QKD protocol fails due to clock mismatch. Step 7: Analyze clock logs and sync errors.
- **Detection**: Clock sync logs, timing histogram
- **Solution**: Use shielded oscillators, sync over fiber
- **Tags**: QKD, Clock Drift, RF Desync, Timing DoS

## AI-Driven Cross-Correlation Attack via Dual-Wireless Interfaces

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: BLE + Wi-Fi PQ Devices
- **Vulnerability**: Multi-protocol interference leaks
- **MITRE**: T1592, T1600
- **Impact**: Reveals optimal attack windows
- **Tools**: Wi-Fi & BLE Sniffers, TensorFlow AI Classifier, Dual Radio Receiver
- **Scenario**: Using AI to correlate activity across two wireless interfaces (e.g., BLE and Wi-Fi) to reconstruct cryptographic timing patterns.
- **Attack Steps**: Step 1: Deploy a system with two wireless sniffers: one capturing BLE traffic, the other capturing Wi-Fi signals from a target PQ-enabled device.Step 2: Record timestamps and packet density across both channels during normal and key exchange activities.Step 3: Train an AI classifier to correlate spikes in one band with latency dips in the other (e.g., CPU contention during encryption causes response delay).Step 4: The model identifies combined activity patterns that suggest key processing times.Step 5: Use that knowledge to launch synchronized attacks (e.g., EM analysis or RF injection) at precise windows.
- **Detection**: Detect abnormal cross-protocol timings
- **Solution**: Randomize communication intervals across protocols
- **Tags**: ai, cross-protocol, timing-correlation, wireless

## AI-Powered Signal Fingerprinting of PQ Devices Using Frequency Drift

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wi-Fi/BLE PQ Devices
- **Vulnerability**: Thermal shift affects frequency accuracy
- **MITRE**: T1592.002, T1040
- **Impact**: Reveals cryptographic load moments
- **Tools**: RTL-SDR, Temperature-Aware AI Model, GNURadio
- **Scenario**: Using AI to track minute frequency shifts caused by cryptographic load-induced temperature changes in device transmitters.
- **Attack Steps**: Step 1: Use an SDR to monitor the wireless frequency of a PQ device (e.g., 2.4GHz band).Step 2: Record small frequency drifts during idle and heavy crypto operations (such as key exchange).Step 3: Train an AI model to associate specific drift patterns with specific PQ crypto algorithms or workloads.Step 4: Use real-time drift monitoring to infer when a key is being generated or used.Step 5: Trigger active surveillance or RF injection during those identified windows.
- **Detection**: Frequency spectrum anomaly detection
- **Solution**: Stabilize hardware oscillators; use shielding
- **Tags**: ai, frequency-drift, crypto-load, fingerprint

## Adversarial AI Induces Faults in PQ Encryption via Wi-Fi Jamming

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wi-Fi-based PQ Key Exchange Devices
- **Vulnerability**: Poor error handling under fault
- **MITRE**: T1600, T1557.002
- **Impact**: Fallback to insecure protocols
- **Tools**: Wi-Fi Jammer, AI Timing Model (RNN), Scapy
- **Scenario**: Using AI-guided timing to jam key packets during PQ handshake, introducing errors to exploit fallback or fault-based analysis.
- **Attack Steps**: Step 1: Passively record Wi-Fi traffic during a PQ handshake between client and server.Step 2: Feed timing and sequence data into an RNN model to identify the critical moments of key transmission.Step 3: At the predicted moment, use a directional Wi-Fi jammer to interrupt just a few key packets.Step 4: If the device retries or falls back to a non-PQ mode, capture the degraded traffic.Step 5: Analyze captured data for weak modes, timing errors, or unintentional leakage.
- **Detection**: Retry-pattern monitoring
- **Solution**: Harden retry mechanisms, add failure randomness
- **Tags**: ai, jamming, pqc-fault, handshake-attack

## Machine Learning-based Packet Length Sequence Analysis on PQ Crypto Protocols

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wireless PQ Communication Devices
- **Vulnerability**: Packet-size fingerprinting
- **MITRE**: T1040, T1595.002
- **Impact**: Protocol identification without decryption
- **Tools**: Wireshark, AI Sequence Classifier, Python
- **Scenario**: AI detects specific PQ cryptographic protocols by observing the sequence of packet lengths during wireless communications.
- **Attack Steps**: Step 1: Capture packet sizes and timing from Wi-Fi or BLE communications, ignoring content (fully encrypted).Step 2: Label different PQ crypto protocols (e.g., Kyber, Dilithium) based on their characteristic packet size patterns.Step 3: Train a machine learning model (e.g., random forest or LSTM) to classify the protocol used just from this size sequence.Step 4: Use output to focus next-stage cryptanalysis or fault testing based on the identified protocol's known weaknesses.Step 5: Refine the model with additional data from test lab PQ protocol runs.
- **Detection**: Monitor for abnormal length patterns
- **Solution**: Pad/encrypt packet length, randomize exchanges
- **Tags**: ai, packet-size, protocol-detection, pqc

## Reinforcement Learning Agent to Optimize RF Signal Positioning for Crypto Leaks

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ Device using Wireless Protocol
- **Vulnerability**: EM emissions vary by direction and proximity
- **MITRE**: T1592.002, T1600
- **Impact**: Locates ideal attack position automatically
- **Tools**: SDR, Reinforcement Learning Model (OpenAI Gym), Stepper Motor Mount
- **Scenario**: AI agent moves SDR antennas around a room and learns the optimal location to capture leakage signals during PQ crypto use.
- **Attack Steps**: Step 1: Place an SDR on a movable mount controlled by motors (can be manually simulated with markers in lab).Step 2: During key exchanges on a PQ device, move the SDR slightly and record signal quality and anomalies.Step 3: Reward the AI agent when it records stronger or more detailed leakage signals (e.g., small bursts of unintended emissions).Step 4: The agent learns which angles or positions give the clearest crypto-related emissions.Step 5: Use optimal position to capture further signal for cryptanalysis.
- **Detection**: RF mapping around device
- **Solution**: EM shielding, test in RF-quiet chambers
- **Tags**: ai, reinforcement-learning, signal-leak, pqc

## AI-Aided Multi-Protocol Recon to Build PQ Device Usage Graph

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ Devices using Multiple Protocols
- **Vulnerability**: Protocol coordination reveals usage graph
- **MITRE**: T1592, T1595
- **Impact**: Temporal recon of crypto activity
- **Tools**: Wi-Fi, BLE, Zigbee Sniffers, Graph AI (Neo4j + Python), NetworkX
- **Scenario**: Building an AI-generated graph of PQ device behavior across multiple wireless protocols to uncover usage schedules.
- **Attack Steps**: Step 1: Use multiple sniffers to simultaneously capture Wi-Fi, BLE, and Zigbee traffic in a PQ test environment.Step 2: Log time, source device ID, and packet counts from each protocol into a central CSV.Step 3: Feed this data into a graph AI model that links devices and actions (e.g., “Device A sends Zigbee before Wi-Fi PQ key exchange”).Step 4: From graph relationships, AI finds repeating behavioral sequences (e.g., 8 AM crypto burst, 5 PM logout).Step 5: Attacker uses schedule predictions to time future attacks or network probing.
- **Detection**: Multi-protocol timing correlation
- **Solution**: Randomize usage times and use decoys
- **Tags**: ai, graph-modeling, multi-protocol, pqc

## Side-channel Harvesting via RF Signal Leakage in PQC Devices

- **Attack Type**: RF Side-Channel Eavesdropping
- **Target**: PQC Crypto Processor
- **Vulnerability**: Unintended RF emissions
- **MITRE**: T1207 (Hardware Input Capture)
- **Impact**: Extraction of private keys via emission analysis
- **Tools**: RTL-SDR, GNU Radio, Faraday Cage, Custom RF Filter Script
- **Scenario**: Attacker captures unintended RF emissions from PQC hardware to reverse cryptographic operations.
- **Attack Steps**: Step 1: Place PQC hardware in a test environment lacking RF shielding (no Faraday cage).Step 2: Use RTL-SDR and GNU Radio to capture electromagnetic emissions during PQC key generation and signing.Step 3: Isolate repetitive waveform patterns during cryptographic computation.Step 4: Compare emissions against known timing operations to infer bits of secret keys.Step 5: Reconstruct partial keys based on leaked signals.Step 6: Validate by testing decrypted data against known plaintext.
- **Detection**: RF signal monitoring, abnormal waveform detection
- **Solution**: Use Faraday cage shielding and hardware filters
- **Tags**: #RFLeakage #SideChannelAttack #QuantumChip

## Wi-Fi SSID Trigger for PQC Debug Interface Unlock

- **Attack Type**: Covert SSID-Based Backdoor
- **Target**: PQC Embedded Module
- **Vulnerability**: Hidden SSID debug trigger
- **MITRE**: T1557.001 (Wireless AP Impersonation)
- **Impact**: Firmware compromise via debug exposure
- **Tools**: ESP8266, aircrack-ng, FakeAP, Serial Monitor
- **Scenario**: Attacker broadcasts a specific SSID that triggers PQC device debug mode during startup.
- **Attack Steps**: Step 1: Analyze PQC device’s firmware or documentation to find hidden SSID that triggers debug mode (e.g., “PQCBETA_99”).Step 2: Program ESP8266 or use FakeAP to broadcast matching SSID.Step 3: Position Wi-Fi transmitter near the PQC unit during startup phase.Step 4: Device detects SSID and automatically opens a debug port or reduces security levels.Step 5: Connect via UART or USB to access system functions.Step 6: Dump memory or modify boot config via debug interface.
- **Detection**: Monitor boot logs and wireless SSID environment
- **Solution**: Disable hidden triggers in final release
- **Tags**: #SSIDTrigger #DebugUnlock #PQCModule

## NFC Tag with Boot-Time Exploit for PQC Hardware

- **Attack Type**: NFC Boot Exploit
- **Target**: PQC Bootloader
- **Vulnerability**: Auto-read NFC at boot without authentication
- **MITRE**: T1564.001 (Hidden Artifacts: Boot Modification)
- **Impact**: Hidden boot override for permanent compromise
- **Tools**: NFC Tag Writer, Android w/NFC Tools, Custom Bash Payload
- **Scenario**: Malicious NFC tag placed near PQC chipboard configures alternate boot path leading to backdoored OS.
- **Attack Steps**: Step 1: Write a malicious NFC tag containing a command sequence or config directive (e.g., alternate boot URL or drive path).Step 2: Place tag under PQC hardware’s chassis where it won't be visually noticed.Step 3: During the device’s startup, it reads the nearby NFC tag for boot parameters.Step 4: The bootloader follows alternate path and loads backdoored firmware.Step 5: Attacker later connects via BLE or USB to extract data or plant more malware.Step 6: Use log analysis to identify alternate boot entry or deviation in checksums.
- **Detection**: NFC scans, boot config diffing
- **Solution**: Disable boot commands via NFC; sanitize input
- **Tags**: #NFCBootHack #SupplyChainThreat

## BLE Authentication Downgrade to Push Weak PQC Firmware

- **Attack Type**: BLE Auth Bypass
- **Target**: PQC BLE-Enabled Device
- **Vulnerability**: BLE pairing downgrade without alert
- **MITRE**: T1608 (Develop Capabilities)
- **Impact**: Downgrade firmware crypto to break future security
- **Tools**: BLEAH, nRF Toolbox, Burp BLE Proxy
- **Scenario**: Attacker downgrades BLE pairing mode to "Just Works" and sends firmware with weak crypto routines.
- **Attack Steps**: Step 1: Scan for BLE devices using nRF Toolbox and identify target PQC hardware.Step 2: Force BLE connection drop and initiate re-pairing.Step 3: Spoof re-pair request using "Just Works" mode (no confirmation).Step 4: Send update request with malicious firmware blob replacing PQC libraries.Step 5: Wait for reboot and use BLE service to query device functions for altered key lengths or algorithms.Step 6: Validate if firmware now uses non-post-quantum-safe key sizes.
- **Detection**: Monitor firmware signature logs
- **Solution**: Enforce secure pairing and signed updates
- **Tags**: #BLEDowngrade #FirmwareExploit #PQC

## Wi-Fi Management Frame Injection to Alter PQC Config Profiles

- **Attack Type**: Wi-Fi Management Exploit
- **Target**: PQC Configuration Dashboard
- **Vulnerability**: Blind acceptance of wireless config links
- **MITRE**: T1557 (Adversary-in-the-Middle)
- **Impact**: Push of insecure PQ profiles without notice
- **Tools**: Scapy, aircrack-ng, Python Wi-Fi Injector
- **Scenario**: An attacker injects spoofed 802.11 management frames to PQC setup laptops to switch to rogue PQC profiles.
- **Attack Steps**: Step 1: Identify Wi-Fi setup tools used during PQC configuration (e.g., open-source dashboards that sync via SSID).Step 2: Craft spoofed beacon or probe response packets with altered PQC profile links.Step 3: Inject packets into the Wi-Fi channel using Scapy and aircrack-ng.Step 4: The target laptop connects and downloads rogue PQC policy with altered cryptographic defaults.Step 5: Analyze configuration file for signs of unsafe defaults or exposed entropy seeds.Step 6: Observe system behavior for reduction in security level or change in encryption method.
- **Detection**: Monitor beacon/probe injection attempts
- **Solution**: Pin configuration updates to secure endpoints
- **Tags**: #WiFiMgmtHack #PQCConfig

## Wireless UART Trigger via RF to Bypass PQC Boot Signing

- **Attack Type**: RF-Based UART Wake
- **Target**: PQC Secure Boot Chip
- **Vulnerability**: RF-sensitive boot triggers without protection
- **MITRE**: T1059.004 (Unix Shell)
- **Impact**: Bypass cryptographic validation at boot
- **Tools**: RF Pulse Transmitter, Logic Analyzer, UART-to-USB Cable
- **Scenario**: Attacker sends RF signal that triggers UART console during PQC chip boot to bypass signed firmware checks.
- **Attack Steps**: Step 1: Identify that the PQC chip has UART console accessible during the boot stage.Step 2: Locate RF-trigger line (e.g., through EMI-sensitive pin or debug jumper).Step 3: Send a precisely timed RF pulse while device boots to activate UART shell.Step 4: Connect via UART-to-USB adapter and interrupt normal boot.Step 5: Input commands to bypass signature check or load unsigned OS blob.Step 6: Confirm device boots with modified firmware and debug output.
- **Detection**: Boot UART logs, firmware signature alert
- **Solution**: Disable RF debug inputs post-manufacturing
- **Tags**: #UARTTrigger #BootBypass #QuantumSecurity

## Wireless Flip of Entanglement Confirmation Bit

- **Attack Type**: Wireless Bit Manipulation
- **Target**: Entanglement Handshake Frame
- **Vulnerability**: Entanglement confirmation not protected against tampering
- **MITRE**: T1557
- **Impact**: Causes false failure or success, derailing protocol flow
- **Tools**: Wi-Fi Pineapple, Packet Editor
- **Scenario**: Attacker flips a single-bit value used to confirm successful entanglement exchange in fault-tolerant QKD, misleading protocol state.
- **Attack Steps**: Step 1: Identify the classical communication packet that carries entanglement success confirmation (usually a 1-bit or small flag).Step 2: Use Wi-Fi Pineapple to enter monitor mode and capture this packet in transit.Step 3: Craft a modified packet where the entanglement confirmation bit is flipped from “1” (success) to “0” (fail) or vice versa.Step 4: Reinject the modified packet slightly earlier than the original to trigger processing.Step 5: Observe that fault-tolerant QKD logic either retries unnecessarily or continues under false assumption.Step 6: Record QKD session logs to analyze error correction overhead or final key mismatch.
- **Detection**: Unexpected retries or key anomalies
- **Solution**: Use message authentication codes (MACs) for even small fields
- **Tags**: wireless flip, quantum flag tampering, confirmation spoof

## Timing Skew Attack on Redundant QKD Nodes via Wireless Clock Drift

- **Attack Type**: Wireless Timing Manipulation
- **Target**: Redundant QKD Nodes
- **Vulnerability**: Clocks not shielded or authenticated in sync
- **MITRE**: T1492
- **Impact**: Phase misalignment leads to session desync or key failure
- **Tools**: RF Signal Generator, Clock Skew Logger
- **Scenario**: Attacker wirelessly causes asynchronous timing between redundant QKD nodes, disrupting fault-tolerant synchronization.
- **Attack Steps**: Step 1: Monitor synchronization frequency (e.g., RF or NTP-equivalent signals) used by QKD nodes to stay in phase.Step 2: Use RF generator to emit periodic low-power EM interference targeted at one of the nodes.Step 3: This interference should subtly impact timing-sensitive crystals or internal clocks.Step 4: Over time, clock skew accumulates and introduces timestamp mismatches across redundant nodes.Step 5: Fault tolerance begins compensating using incorrect offsets, causing misaligned key segments.Step 6: Log and compare time delta between nodes before and after attack using internal clock skew loggers.
- **Detection**: Skew logs show increasing desync; retries escalate
- **Solution**: Shield timing hardware; use authenticated clock sync
- **Tags**: skew injection, wireless timing, redundant drift

## Interleaved QKD Session Disruption via Wireless Packet Merging

- **Attack Type**: Wireless Packet Race Exploit
- **Target**: QKD Classical Communication Layer
- **Vulnerability**: Weak session isolation and tag validation
- **MITRE**: T1212
- **Impact**: Misapplied correction logic, key corruption
- **Tools**: SDR with Packet Splicer Script
- **Scenario**: Attacker merges packet identifiers from two sessions, causing fault-tolerant logic to misapply correction data.
- **Attack Steps**: Step 1: Observe two parallel QKD sessions over classical wireless channel.Step 2: Capture packet headers that identify session ID and correction data.Step 3: Use SDR to craft a packet where session ID of one QKD session is mixed with correction data from another.Step 4: Inject the merged packet at a carefully chosen time during reconciliation.Step 5: Observe if fault-tolerant logic applies wrong corrections due to session mix-up.Step 6: Monitor system logs and key agreement results to confirm inconsistency or failure.
- **Detection**: Session ID mismatch logs or dual collision events
- **Solution**: Enforce session ID validation and segregation
- **Tags**: wireless merge, qkd interleaving, session collision

## Exploiting Frame Resend Behavior via Wireless Drop Simulation

- **Attack Type**: Wireless Reliability Exploit
- **Target**: Wireless QKD Control Channel
- **Vulnerability**: Retry logic not rate-limited or protected
- **MITRE**: T1499
- **Impact**: Causes protocol hang or resource starvation
- **Tools**: SDR Dropper, Packet Logger
- **Scenario**: Attacker uses controlled packet drops to manipulate the QKD system’s frame resend behavior and trigger fault-recovery flooding.
- **Attack Steps**: Step 1: Monitor normal packet resend behavior using a wireless packet sniffer.Step 2: Use an SDR to selectively jam acknowledgment (ACK) packets, simulating drops.Step 3: Cause the QKD system to believe frames were lost and resend them.Step 4: Carefully repeat this during reconciliation frames to force repeated retransmissions.Step 5: Exploit the system’s fault tolerance to overwhelm it, leading to memory/resource exhaustion or timeout.Step 6: Track how many retries occur before fail-safe kicks in and sessions are aborted.
- **Detection**: Excessive retry count in logs
- **Solution**: Introduce retry limits and detect repeated failure loops
- **Tags**: resend abuse, wireless drop spoof, fault retry loop

## Wireless Transmission Delay Injection During Redundant Error Correction

- **Attack Type**: Wireless Delay Injection
- **Target**: QKD Error Correction Layer
- **Vulnerability**: No protection against delayed but valid-looking packets
- **MITRE**: T1498
- **Impact**: Key mismatch or failure to finalize session
- **Tools**: Packet Delay Injector, SDR
- **Scenario**: Attacker introduces delay in error correction frames sent via wireless links, desynchronizing fault-tolerant consensus.
- **Attack Steps**: Step 1: Identify the time-critical reconciliation or error correction frame exchanges between two nodes.Step 2: Use an SDR-based delay injector to intercept and replay the packet with a controlled delay (e.g., 200ms).Step 3: The delayed frame reaches the second node out of the expected timing window.Step 4: Fault-tolerant logic either retries or wrongly assumes path failure.Step 5: As more delayed frames accumulate, consensus drifts between nodes.Step 6: Final key material becomes mismatched across endpoints.
- **Detection**: Out-of-window logs show frame misalignment
- **Solution**: Timestamp verification and max delay window enforcement
- **Tags**: delayed replay, timing fault, wireless desync

## Quantum Mesh Desynchronization via Wireless Entropy Perturbation

- **Attack Type**: Wireless Entropy Attack
- **Target**: Fault-Tolerant Mesh QKD
- **Vulnerability**: Metadata integrity not entropy-checked
- **MITRE**: T1001
- **Impact**: Validated session results in unusable or mismatched keys
- **Tools**: Noise Injector, SDR Analyzer
- **Scenario**: Attacker injects noise into mesh metadata to introduce entropy inconsistency during key reconciliation in a fault-tolerant mesh QKD setup.
- **Attack Steps**: Step 1: Observe classical metadata shared among mesh nodes for key reconciliation (like parity segments).Step 2: Use a noise injection tool to emit low-power EM interference during metadata exchange windows.Step 3: Inject slight bit errors that do not cause frame failure but alter entropy.Step 4: Fault tolerance may accept the altered metadata due to redundancy, masking the attack.Step 5: Nodes derive mismatched keys even though sessions are marked successful.Step 6: Analyze final key hashes across nodes to confirm inconsistency.
- **Detection**: Post-session key mismatch hashes
- **Solution**: Entropy checksums and authenticated metadata
- **Tags**: entropy attack, wireless noise, reconciliation fault

## PHY Layer Legacy Signature Spoofing

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Quantum-capable Wireless Gateways
- **Vulnerability**: Physical-layer trust assumptions
- **MITRE**: T1600 - Protocol Downgrade
- **Impact**: Device misidentification, unauthorized access
- **Tools**: HackRF, GNURadio, Wireshark
- **Scenario**: The attacker spoofs a legacy physical-layer (PHY) signature so that the PQC wireless system mistakenly classifies the rogue device as a legacy-trusted one.
- **Attack Steps**: Step 1: Monitor PHY-layer communication of a known legacy-trusted device using HackRF and Wireshark.Step 2: Extract waveform pattern and modulation settings.Step 3: Use GNURadio to replicate the signal behavior of the legacy PHY signature (e.g., OFDM frame timing).Step 4: Replay modified waveform from the attacker’s device.Step 5: PQC gateway classifies signal as a trusted fallback device.Step 6: Connection is allowed on legacy channel.Step 7: Attacker joins network and starts passive sniffing.Step 8: Log sensitive data and demonstrate misclassification.
- **Detection**: Monitor waveform anomalies using SDR
- **Solution**: Require PHY + logical handshake fingerprinting
- **Tags**: PHY spoof, HackRF, fallback

## AP Repeater Hijack via Legacy Bridging

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC Mesh Clients
- **Vulnerability**: Repeater backhaul mismatch
- **MITRE**: T1557.002 - Rogue Infrastructure
- **Impact**: Traffic hijack, downgrade to insecure AP
- **Tools**: Aircrack-ng, Hostapd, Mitmproxy
- **Scenario**: A rogue repeater advertises itself as part of the PQC mesh, but bridges only to a legacy WPA2 AP, downgrading all client traffic.
- **Attack Steps**: Step 1: Clone SSID and BSSID of the PQC mesh AP using hostapd.Step 2: Set up a rogue repeater that receives client connection attempts.Step 3: Configure the backhaul to connect only to a legacy WPA2 AP.Step 4: Clients unknowingly connect to rogue repeater thinking it's part of the mesh.Step 5: All traffic is forwarded to the legacy AP.Step 6: Use mitmproxy to log and modify traffic.Step 7: Demonstrate credential and session hijack possibilities.Step 8: Analyze and educate on wireless mesh repeater behavior.
- **Detection**: Monitor AP-repeater link quality & encryption strength
- **Solution**: Enforce signed mesh repeater handshakes
- **Tags**: rogue repeater, WPA2 bridge

## Hidden Legacy Capability Exposure via OTA Beacon

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQC APs
- **Vulnerability**: Legacy compatibility advertisement
- **MITRE**: T1600 - Protocol Downgrade
- **Impact**: Traffic exposure over insecure protocol
- **Tools**: Wireshark, Beacon Flooder, Airmon-ng
- **Scenario**: Exposes hidden legacy capability in PQC-enabled devices that mistakenly broadcast legacy support in over-the-air beacons.
- **Attack Steps**: Step 1: Use Airmon-ng and Wireshark to passively scan beacon frames from PQC-enabled APs.Step 2: Inspect Information Elements (IEs) for backward compatibility flags like support for WPA2.Step 3: Confirm presence of optional legacy protocol descriptors.Step 4: Trigger client connections to the AP using only WPA2.Step 5: Establish connection and log legacy handshake.Step 6: Capture session data from WPA2-based exchange.Step 7: Educate learners on the danger of unnecessary legacy IEs.Step 8: Repeat using beacon flooder to simulate multiple legacy-capable clients.
- **Detection**: Log beacon frame contents and protocol support flags
- **Solution**: Remove legacy IE tags from device firmware
- **Tags**: beacon inspection, WPA2 element, compatibility

## Dual-Stack Device Desync with Timed Legacy Reconnect

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Dual-mode clients
- **Vulnerability**: Race condition between stacks
- **MITRE**: T1499 - Endpoint Denial of Service
- **Impact**: Legacy fallback wins connection race
- **Tools**: PacketCrafter, Scapy, Python Wi-Fi Scripts
- **Scenario**: Creates intentional delay between PQC and legacy interfaces on a dual-mode client to force legacy interface to connect first.
- **Attack Steps**: Step 1: Scan for a dual-stack device that supports both quantum-safe Wi-Fi and fallback WPA2.Step 2: Create a packet delay injector using Scapy and Python to interfere with PQC handshake frames.Step 3: Simultaneously allow unfiltered WPA2 handshake to succeed.Step 4: Client completes connection on legacy mode.Step 5: Log all data transferred and demonstrate false sense of security.Step 6: Redirect data using packet redirection.Step 7: Track how desynchronization occurred and validate attack logic.Step 8: Use this to explain race condition issues in security negotiations.
- **Detection**: Detect timing anomalies between parallel interfaces
- **Solution**: Use single secure interface per device or delay legacy port activation
- **Tags**: dual-stack, handshake race

## Fake IoT Firmware Beacon Trigger

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: IoT devices with PQC OTA modules
- **Vulnerability**: OTA triggers via unauthenticated beacon
- **MITRE**: T1542.001 - Firmware
- **Impact**: Firmware hijack, persistent compromise
- **Tools**: Binwalk, Hostapd, Scapy
- **Scenario**: Sends fake OTA firmware beacon over legacy Wi-Fi that causes IoT device to connect insecurely and request firmware.
- **Attack Steps**: Step 1: Identify IoT devices that support OTA firmware checks over Wi-Fi.Step 2: Monitor beacon trigger pattern using Wireshark.Step 3: Recreate beacon with fake vendor ID and firmware revision using Scapy.Step 4: Set up rogue AP with matching SSID in legacy WPA2 mode.Step 5: Wait for IoT device to connect and request update.Step 6: Serve fake firmware using HTTP server.Step 7: Log device response and control channel.Step 8: Use this to explain weak OTA validation logic.
- **Detection**: Check source of firmware beacon IDs
- **Solution**: Use PQC-signed firmware and authenticated OTA triggers
- **Tags**: OTA beacon spoof, WPA2, firmware hijack

## Signal Strength Deception to Prefer Legacy Channel

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Any client with Wi-Fi signal-based preference
- **Vulnerability**: Signal-based trust of connection
- **MITRE**: T1557.002 - Rogue Wireless
- **Impact**: Unauthorized access, MITM
- **Tools**: Wi-Fi Amp, Hostapd, Airgraph-ng
- **Scenario**: Uses RF amplifier to create artificial high signal strength on a legacy AP, tricking clients into preferring it over PQC channels.
- **Attack Steps**: Step 1: Set up legacy AP with same SSID but different BSSID.Step 2: Use a Wi-Fi amplifier or directional antenna to boost its signal beyond PQC AP.Step 3: Monitor client association preferences using Airgraph-ng.Step 4: Observe clients choosing stronger legacy signal.Step 5: Capture and analyze handshake data.Step 6: Route traffic through rogue AP.Step 7: Log client activity and credentials.Step 8: Use scenario to explain RF-level trust flaws and preferred signal selection mechanisms.
- **Detection**: Signal strength anomaly detection
- **Solution**: Use certificate-pinned AP authentication, ignore signal preference
- **Tags**: signal spoofing, RF trust, WPA2

## Infrared Backdoor Trigger in QSM Optical Devices

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Optical QSM Devices
- **Vulnerability**: Undocumented debug or IR ports
- **MITRE**: T1552.001 (Backdoor Activation)
- **Impact**: Shutdown or fallback trigger
- **Tools**: IR Remote Emitter, Universal IR Remote App, IR Camera
- **Scenario**: Attacker uses hidden IR backdoor channel left unintentionally open in QSM optical receivers to trigger hidden debug commands or disable QKD.
- **Attack Steps**: Step 1: Identify QSM terminal using infrared-based or free-space QKD.Step 2: Use IR camera or sensor to find active receivers and hidden IR ports.Step 3: Test with universal IR remote signals to find any reaction (e.g., LED blink, screen toggle).Step 4: Trigger manufacturer-default debug mode (often left in test units).Step 5: Issue a silent shutdown or mode-change command via IR pulses.Step 6: Verify the device enters insecure messaging or restarts in fallback mode.
- **Detection**: IR traffic logging, debug log monitoring
- **Solution**: Remove debug ports, use physical IR shielding
- **Tags**: Infrared, Optical QKD, Backdoor Channel

## Wi-Fi Signal Reflection Attack on QSM Relay Nodes

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: QSM Mesh Relay Devices
- **Vulnerability**: No protection against signal reflection or path confusion
- **MITRE**: T1499.003 (Signal Confusion)
- **Impact**: Downgrade or message duplication
- **Tools**: Reflective Panel, Wireshark, Directional Antenna
- **Scenario**: Using metallic surfaces, attacker reflects QSM relay Wi-Fi signals to create ghost signals, confusing the protocol stack.
- **Attack Steps**: Step 1: Identify location of relay node in a mesh-based QSM network (using Wireshark scans).Step 2: Place large reflective panels (e.g., metal sheets) behind the node to bounce signals.Step 3: Adjust angles to create multi-path signal interference.Step 4: Capture resulting interference using Wireshark and observe if multiple handshake sessions are triggered.Step 5: Observe if device retries protocol using classical crypto due to confusion.Step 6: Record fallback sessions for later analysis.
- **Detection**: RSSI anomalies, multiple session logs
- **Solution**: Use beamforming antennas, validate signal paths
- **Tags**: Reflection Attack, Wi-Fi, QSM Relay

## Zigbee Command Flood to Induce QSM Session Error

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Zigbee QSM Nodes
- **Vulnerability**: Poor error handling on malformed packets
- **MITRE**: T1464.001 (Protocol Abuse)
- **Impact**: DoS or insecure reboot fallback
- **Tools**: Zigbee Packet Crafter, KillerBee, USB Dongle
- **Scenario**: Flooding Zigbee-based QSM endpoints with malformed commands forces error states that trigger insecure reboot routines.
- **Attack Steps**: Step 1: Identify Zigbee network channel using a Zigbee sniffer (ZBOSS, KillerBee).Step 2: Craft invalid command packets that conform to Zigbee headers but contain junk payloads.Step 3: Send a flood of these to the QSM device’s Zigbee address.Step 4: Monitor device behavior—many will restart into safe mode.Step 5: Observe whether secure messaging is suspended or if device falls back to default key settings.Step 6: Intercept any insecure traffic or simulate legitimate connections.
- **Detection**: Packet logging, malformed command alerts
- **Solution**: Hardened firmware, strict packet validation
- **Tags**: Zigbee Flood, QSM Fallback

## Wireless Power Induction to Glitch QSM Device Boot Sequence

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Embedded QSM Devices
- **Vulnerability**: Susceptibility to voltage or timing glitches
- **MITRE**: T0811 (Hardware Fault Injection)
- **Impact**: Startup failsafe mode, insecure state
- **Tools**: EM Induction Coil, Signal Generator, Oscilloscope
- **Scenario**: Using high-frequency EM pulses, attacker induces timing errors during QSM device boot, disabling quantum encryption temporarily.
- **Attack Steps**: Step 1: Identify a target device that uses a bootable QSM stack (e.g., embedded PQ crypto module).Step 2: Place a small high-frequency EM coil near the power line or board.Step 3: Trigger short electromagnetic pulses during the power-on boot window.Step 4: Observe via oscilloscope if boot timing or watchdog timer misfires.Step 5: Force the device to enter safe/recovery mode with encryption disabled.Step 6: Reconnect device and try classical message session hijacking.
- **Detection**: Boot sequence logs, hardware watchdog flags
- **Solution**: Shielded PCB design, hardened boot firmware
- **Tags**: Hardware Glitching, Boot Attack

## NFC Spoof to Force Quantum Key Reuse in Mobile Devices

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Mobile QSM Apps using NFC
- **Vulnerability**: Lack of strict key freshness validation
- **MITRE**: T1557.003 (Key Reuse Exploit)
- **Impact**: Confidentiality breach via key reuse
- **Tools**: NFC Emulator, Android w/ LibNFC, MITM Proxy
- **Scenario**: Attacker uses spoofed NFC signals to trick mobile QSM apps into reusing previous quantum keys instead of generating fresh ones.
- **Attack Steps**: Step 1: Identify target QSM app using NFC to exchange or derive shared quantum keys.Step 2: Use NFC emulator to mimic previous device UID and exchange timestamp.Step 3: Replay the same token or key handshake used in an earlier session.Step 4: App, believing the session is recent, reuses the quantum key.Step 5: Capture and decrypt ongoing session since key is known.Step 6: Validate message consistency and perform MITM to modify payloads.
- **Detection**: NFC handshake monitoring, nonce repeat checks
- **Solution**: Enforce key uniqueness, key expiration limits
- **Tags**: NFC, Key Reuse, Mobile QSM Exploit

## Wi-Fi SSID Cloning for Quantum Gateway Redirection

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wi-Fi QSM Clients & Gateways
- **Vulnerability**: Trust in SSID alone, no endpoint validation
- **MITRE**: T1557.004 (Gateway Spoofing)
- **Impact**: MITM key exchange, traffic hijack
- **Tools**: PineAP, Rogue AP, Wireshark, ARP Spoof Tools
- **Scenario**: Attacker clones the SSID of a QSM gateway and intercepts traffic to redirect it through a fake relay node.
- **Attack Steps**: Step 1: Use Wireshark to monitor and identify the gateway SSID of a QSM chat network.Step 2: Set up a rogue AP using PineAP or hostapd with the same SSID and stronger signal.Step 3: Wait for clients to connect, then assign them an IP from your own DHCP pool.Step 4: Forward traffic through a proxy while logging and analyzing key exchange behavior.Step 5: Redirect packets to a real gateway after key agreement to minimize detection.Step 6: Inject fake traffic or modify messages before relaying back.
- **Detection**: Rogue AP detection, DHCP fingerprinting
- **Solution**: Use gateway pinning, DNSSEC, cert validation
- **Tags**: Wi-Fi Clone, MITM, QSM Redirection

## Quantum Token Spoof via BLE Advertisement Injection

- **Attack Type**: Wireless - BLE Broadcast Injection
- **Target**: BLE Beacon-Based Token System
- **Vulnerability**: Weak validation of advertising packets and source
- **MITRE**: T1583.004
- **Impact**: False presence leads to unauthorized access
- **Tools**: BLEah, Raspberry Pi, hcitool, Wireshark
- **Scenario**: The attacker injects forged BLE advertisement packets impersonating the quantum token’s unique broadcast ID to trick proximity systems
- **Attack Steps**: Step 1: Use BLEah tool to scan and identify advertisement packets from the real quantum token.Step 2: Record advertising interval, payload data (UUID, MAC, signal strength).Step 3: Use hcitool and a BLE adapter on Raspberry Pi to transmit forged advertisement packets with same identity.Step 4: Ensure timing matches the real device using crontab or precise scripts.Step 5: Proximity-based system accepts fake token presence.
- **Detection**: Scan for BLE ID conflicts or packet clones
- **Solution**: Cryptographically sign BLE advertisements
- **Tags**: BLE, Spoof, Beacon Injection, Token

## Spoofing Quantum Token on Ultra-Wideband (UWB) Channel

- **Attack Type**: Wireless - UWB Spoofing
- **Target**: UWB-based Quantum Access Systems
- **Vulnerability**: UWB pulse replay without quantum integrity check
- **MITRE**: T1020
- **Impact**: Distance spoofing and unauthorized entry
- **Tools**: Decawave DWM1001, UWB Sniffer, Custom Python Scripts
- **Scenario**: Attacker crafts UWB pulses that mimic those from a quantum token to fool ranging-based systems
- **Attack Steps**: Step 1: Place UWB sniffer to capture ranging pulses from token during authentication.Step 2: Analyze timestamps, pulse intervals, and phase shifts.Step 3: Use Decawave module to recreate the same ranging behavior and UWB ID.Step 4: Replay spoofed pulses during authentication phase.Step 5: UWB system calculates false distance and grants access.
- **Detection**: Compare ToF (Time of Flight) against predicted patterns
- **Solution**: Add quantum signature validation to ToF check
- **Tags**: UWB, Spoof, Distance Hijack, Ranging

## Quantum Token Spoof using RFID Emulator over ISO-14443

- **Attack Type**: Wireless - RFID Emulation
- **Target**: RFID Quantum Token Readers
- **Vulnerability**: Classical interface spoofed without quantum validation
- **MITRE**: T1207
- **Impact**: Access granted to spoofed token
- **Tools**: ChameleonMini, RFID Spy, Android NFC Tools
- **Scenario**: A low-cost RFID emulator is used to spoof the presence of a quantum-authenticated token relying on ISO-14443 interface
- **Attack Steps**: Step 1: Use RFID Spy tool or ChameleonMini to sniff ISO-14443 handshake of real quantum token.Step 2: Record UID, command sequence, and anti-collision behavior.Step 3: Replay exact sequence using emulator with correct timing.Step 4: Present emulator to reader.Step 5: Reader validates the spoofed UID as authentic.
- **Detection**: Compare UID timings, EM patterns
- **Solution**: Perform secondary quantum-layer validation
- **Tags**: RFID, UID Clone, ISO-14443, Emulator

## Fake Quantum Token in NFC HCE Mode

- **Attack Type**: Wireless - NFC Host Card Emulation
- **Target**: NFC Quantum Token Interface
- **Vulnerability**: Classical fallback trusted without entropy verification
- **MITRE**: T1110.003
- **Impact**: System grants access to fake tokens
- **Tools**: Android Studio, HCE Service, NFC Tools Pro
- **Scenario**: Android phone emulates the exact behavior of a quantum cryptographic token using Host Card Emulation
- **Attack Steps**: Step 1: Monitor NFC token interactions during authentication.Step 2: Reverse engineer APDU command sequences.Step 3: Develop a custom Android HCE app that responds identically.Step 4: Deploy the app and tap phone to reader.Step 5: System authenticates the spoofed token from phone.
- **Detection**: Use entropy tests during authentication
- **Solution**: Combine quantum randomness with APDU response
- **Tags**: NFC, HCE, Android Emulation, Token Spoof

## Quantum Token Cloning using Electromagnetic Field Recording

- **Attack Type**: Wireless - EM Field Analysis
- **Target**: EM-Sensitive Quantum Token Device
- **Vulnerability**: Electromagnetic signature replayable via physical capture
- **MITRE**: T1592.002
- **Impact**: Replay of EM field leading to fake token authentication
- **Tools**: EM Probe, Oscilloscope, Signal Generator, Proxmark
- **Scenario**: Attacker captures the electromagnetic field emitted during token transmission and replays it with a spoofing device
- **Attack Steps**: Step 1: Place EM probe near legitimate token during transaction.Step 2: Record waveform and energy modulation.Step 3: Reconstruct signal using signal generator.Step 4: Replay EM pattern to reader.Step 5: Reader accepts EM signature and authenticates the spoofed token.
- **Detection**: Measure ambient field strength and noise correlation
- **Solution**: Shield token and add real-time entropy layers
- **Tags**: EM, Field Capture, Signal Replay, Token

## Signal Reflection Attack using Wi-Fi Mirror Relay

- **Attack Type**: Wireless - Signal Reflection Relay
- **Target**: Wi-Fi Quantum Token Proxy Network
- **Vulnerability**: Reflected communications trusted without mutual quantum handshake
- **MITRE**: T1040
- **Impact**: Man-in-the-middle data injection and spoofing
- **Tools**: Wireshark, Rogue AP, Bettercap, IPTables NAT
- **Scenario**: A fake AP reflects encrypted token communication through a real client to avoid detection
- **Attack Steps**: Step 1: Set up rogue AP identical to the quantum network.Step 2: Redirect token’s client traffic to real AP via NAT reflection.Step 3: Observe and manipulate session timing.Step 4: Inject altered packets mimicking token origin.Step 5: Server falsely validates spoofed packet chain as legitimate.
- **Detection**: Detect routing anomalies, TTL mismatch
- **Solution**: Implement session-bound cryptographic link
- **Tags**: Reflection, Relay, NAT Spoof, Token

## Wi-Fi Beacon Flood with Fake Quantum Token SSIDs

- **Attack Type**: Wireless - Wi-Fi Beacon Spoof
- **Target**: Wi-Fi Quantum Broadcast Devices
- **Vulnerability**: Beacon-based token detection vulnerable to confusion
- **MITRE**: T1565.002
- **Impact**: Session hijack or token misidentification
- **Tools**: mdk3, airodump-ng, Aircrack-ng Suite
- **Scenario**: Flooding the network with SSIDs mimicking quantum token identifiers to confuse or spoof device detection
- **Attack Steps**: Step 1: Use airodump-ng to identify SSID and MAC of quantum token SSID beacon.Step 2: Use mdk3 to flood beacon frames with similar names and MAC patterns.Step 3: Introduce timing delays to match legitimate broadcasts.Step 4: Proximity readers lock on fake SSIDs.Step 5: Authentication hijacked due to SSID confusion.
- **Detection**: Beacon fingerprinting and SSID validation
- **Solution**: Use secure token-broadcast channel, not SSID-based
- **Tags**: SSID, Beacon Flood, Token Confusion

## Quantum Token Spoofing via Zigbee Fake Cluster Injection

- **Attack Type**: Wireless - Zigbee Cluster Emulation
- **Target**: Zigbee Quantum Security Devices
- **Vulnerability**: Insecure cluster field validation during token handshake
- **MITRE**: T1071.002
- **Impact**: Bypassed authentication via field emulation
- **Tools**: Zigbee2MQTT, CC2530 Sniffer, Node-RED
- **Scenario**: Attacker injects fake Zigbee cluster attributes matching quantum token handshake data
- **Attack Steps**: Step 1: Sniff token’s Zigbee communication and record attribute cluster IDs.Step 2: Inject fake cluster with matching fields (UUID, timestamp).Step 3: Replay with spoofed MAC address.Step 4: Smart controller processes the fake token as valid.Step 5: Authentication bypassed via spoofed cluster attributes.
- **Detection**: Monitor Zigbee cluster field consistency
- **Solution**: Harden attribute parsing and entropy-based challenge
- **Tags**: Zigbee, Cluster Injection, Token Spoof

## IR Signal Injection on Optical Quantum Token Gateway

- **Attack Type**: Wireless - Infrared Injection
- **Target**: Infrared Quantum Token Receiver
- **Vulnerability**: IR input trusted without quantum-proof authentication
- **MITRE**: T1055.001
- **Impact**: Token signal spoof and unauthorized access
- **Tools**: IR Blaster, Arduino, Logic Analyzer
- **Scenario**: IR pulses simulating quantum token signals are injected to mimic authentication
- **Attack Steps**: Step 1: Capture IR pattern from original token using logic analyzer.Step 2: Convert pulse into modulation script (NEC/SIRC format).Step 3: Program IR blaster to send recorded pattern.Step 4: Target system receives fake IR signal.Step 5: Access granted if signal not cryptographically verified.
- **Detection**: Infrared entropy measurement
- **Solution**: Add secure time-based challenge to IR signals
- **Tags**: IR, Pulse Spoofing, Optical Injection

## Bluetooth Token Spoof via Paired Device Session Hijack

- **Attack Type**: Wireless - Session Hijack
- **Target**: Bluetooth-Connected Token Systems
- **Vulnerability**: Session hijack possible if identity not verified via quantum signature
- **MITRE**: T1563.002
- **Impact**: Token bypass and fake session acceptance
- **Tools**: BTstack, hcitool, L2CAP Monitor, MITM Proxy
- **Scenario**: Attacker hijacks an existing paired session to spoof token response
- **Attack Steps**: Step 1: Monitor paired connection between quantum token and reader.Step 2: Disconnect token and immediately reconnect with same MAC.Step 3: Use BTstack to simulate token's session parameters (L2CAP, encryption).Step 4: Inject spoofed response to pending challenge.Step 5: Reader mistakenly accepts spoofed session.
- **Detection**: Session monitoring and behavior baseline
- **Solution**: Perform quantum key validation at each reconnect
- **Tags**: Bluetooth, Session Hijack, Token, L2CAP

## Multi-Vector Token Spoof Using Coordinated SDR Attacks

- **Attack Type**: Wireless - Coordinated SDR Emulation
- **Target**: Multi-Protocol Quantum Token Gateways
- **Vulnerability**: Trusting cross-protocol consistency without cryptographic sync
- **MITRE**: T1557.003
- **Impact**: High-assurance token bypass via coordinated spoof
- **Tools**: HackRF x3, GNU Radio, Clock Sync Scripts
- **Scenario**: A coordinated team uses multiple SDR devices to emulate a quantum token over multiple channels (BLE + UWB + Zigbee) to mimic a sophisticated token
- **Attack Steps**: Step 1: Deploy 3 SDRs emulating BLE, UWB, Zigbee interfaces.Step 2: Sync SDRs via NTP or external clock.Step 3: Replay multi-protocol token traffic mimicking real sequence.Step 4: Align responses to appear in authentic order.Step 5: System sees coordinated inputs and accepts spoofed token.
- **Detection**: Analyze cross-channel timing & identity correlation
- **Solution**: Require cross-channel key fusion and entropy sync
- **Tags**: SDR, Multi-Vector, Timing Sync, Token

## PQ Device Pairing Loop via Weak Entropy Reset on Reboot

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: BLE IoT Device
- **Vulnerability**: Static Entropy Seed
- **MITRE**: T1602 (Static Seed Replay)
- **Impact**: Predictable identity spoofing
- **Tools**: BLE Sniffer, BLEAH, Wireshark
- **Scenario**: Device generates same PQ key after each reboot due to static entropy seed
- **Attack Steps**: Step 1: Configure a PQ-enabled BLE device to reset entropy seed to a fixed value on reboot (educational setting). Step 2: Sniff pairing attempts with BLEAH over multiple reboots. Step 3: Notice identical public PQ keys generated every time. Step 4: Emulate an attacker precomputing private response. Step 5: Reuse that private key to impersonate legitimate device. Step 6: Observe pairing success and log attacker’s session.
- **Detection**: Identical key reuse after reboot
- **Solution**: Use secure entropy initialization
- **Tags**: BLE, KeyReuse, PQSeedFail

## Wi-Fi KEM Key Replay via Shared MAC & Predictable PQ Derivation

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wi-Fi IoT Devices
- **Vulnerability**: Predictable KEM Derivation
- **MITRE**: T1605 (MAC Key Derivation Flaw)
- **Impact**: Cross-device key collisions
- **Tools**: Aircrack-ng, PQSessionLogger
- **Scenario**: Multiple Wi-Fi devices use MAC as PQ derivation salt, enabling session collision
- **Attack Steps**: Step 1: Configure multiple devices to derive PQ keys using static MAC as salt. Step 2: Capture key exchange packets using Aircrack-ng. Step 3: Log PQ session keys across different devices. Step 4: Observe identical keys in cases where MAC address is reused. Step 5: Replay session handshake from one device to another. Step 6: Confirm server accepts duplicate key as valid.
- **Detection**: Matching session keys in logs
- **Solution**: MAC-free PQ key derivation
- **Tags**: WiFiKEM, PQMACReuse, EntropyMisuse

## Zigbee Replay Attack via Static Key Caching in PQ Device Memory

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Zigbee Controller
- **Vulnerability**: Static Key Cache in Memory
- **MITRE**: T1200 (Firmware-Level Key Reuse)
- **Impact**: Replay injection, device spoof
- **Tools**: Zigbee2MQTT, KillerBee, Firmware Debugger
- **Scenario**: Zigbee device caches PQ keys in firmware for reuse, attacker replays key exchange
- **Attack Steps**: Step 1: Flash firmware into a Zigbee PQ device that stores public/private keys between sessions. Step 2: Use KillerBee to capture initial handshake. Step 3: Reboot device and capture again—observe identical key data. Step 4: Replay handshake from the first session. Step 5: Simulate attacker establishing connection with server using old keys. Step 6: Inject false Zigbee commands using forged session.
- **Detection**: Firmware logging, key cache trace
- **Solution**: Enforce volatile key storage
- **Tags**: ZigbeeReplay, PQFirmwareKeyReuse

## Wireless RF Side-Channel Attack Reveals PQ Entropy Quality

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wireless PQ Transmitter
- **Vulnerability**: RF Timing Pattern from Reused Entropy
- **MITRE**: T1425.001 (RF Side Channel Timing)
- **Impact**: Entropy-level fingerprinting
- **Tools**: HackRF, GQRX, RFAnalyzer
- **Scenario**: RF fingerprint of PQ handshake shows repeated timing patterns caused by entropy reuse
- **Attack Steps**: Step 1: Monitor multiple PQ key exchanges using HackRF. Step 2: Record timing and amplitude of RF bursts for each session. Step 3: Use RFAnalyzer to identify microsecond-level timing overlaps. Step 4: Link identical handshake timings to reused entropy sources. Step 5: Correlate timing with specific key reuse patterns. Step 6: Demonstrate that attacker can flag predictable devices.
- **Detection**: Identical RF pulse spacing
- **Solution**: Add noise/random jitter
- **Tags**: RFPattern, EntropyTimingLeak

## PQ Handshake Injection in BLE via Predictable Session Initiation

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: BLE PQ Device
- **Vulnerability**: Clock-Based Seed Reuse
- **MITRE**: T1603.002 (Time-Based Key Reuse)
- **Impact**: Authentication spoofing
- **Tools**: BLEAH, BLESeedWatcher, Clock Drift Tool
- **Scenario**: BLE device uses time-based predictable seed, attacker predicts when key is reused
- **Attack Steps**: Step 1: Set BLE PQ device’s seed based on system clock (e.g., time since power-on). Step 2: Monitor clock offset and PQ keys over time. Step 3: Use BLESeedWatcher to log the times keys repeat. Step 4: Simulate attacker syncing clock and precomputing valid key. Step 5: Replay that key during actual handshake. Step 6: Successfully inject PQ-authenticated BLE message.
- **Detection**: Sync in PQ handshake logs
- **Solution**: Use external entropy sources
- **Tags**: BLE, ClockSeed, PQTimeInjection

## Wireless Replay of PQ TLS Session from Captured Initial Key Exchange

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ-TLS Server
- **Vulnerability**: PQ Session Key Reuse
- **MITRE**: T1611 (TLS Session Replay)
- **Impact**: Session injection, data snoop
- **Tools**: Wireshark, Scapy, PQSessionReplay
- **Scenario**: Server doesn’t check key uniqueness in PQ TLS handshakes, attacker reuses old session
- **Attack Steps**: Step 1: Connect to a PQ-enabled TLS server over Wi-Fi and complete handshake. Step 2: Save the complete key exchange packets. Step 3: Disconnect and reconnect using same key from file. Step 4: Observe that server allows replayed key for session resumption. Step 5: Simulate MITM attacker inserting stale key session. Step 6: Log access and replayed message acknowledgment.
- **Detection**: Session key reuse in server logs
- **Solution**: Enforce one-time session IDs
- **Tags**: WiFiTLS, PQReplay, KeyResend

## Low Entropy PQ Auth in IoT Wi-Fi Setup Wizard Enables Hijack

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wi-Fi IoT Device Wizard
- **Vulnerability**: PQ Auth with Weak Entropy
- **MITRE**: T1643 (Provisioning Weakness)
- **Impact**: Unauthorized provisioning access
- **Tools**: SetupWizard, Wireshark, PQEntropyAnalyzer
- **Scenario**: PQ-auth Wi-Fi provisioning tool generates weak keys due to low-entropy source
- **Attack Steps**: Step 1: Initiate Wi-Fi provisioning using IoT setup wizard with PQ handshake. Step 2: Log key material via Wireshark at each pairing step. Step 3: Notice high similarity in public key values between devices. Step 4: Simulate attacker device sending identical public key and pass authentication. Step 5: Access control dashboard or admin panel as trusted device. Step 6: Demonstrate low entropy flaw allowing key reuse spoof.
- **Detection**: Key similarity in setup logs
- **Solution**: Add dedicated entropy chip for setup
- **Tags**: WiFiSetup, PQProvisionWeak

## Wireless PQ Pairing Abuse via Reused Ephemeral Keys in Broadcast

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Wireless PQ Device
- **Vulnerability**: Broadcast Ephemeral Key Reuse
- **MITRE**: T1625 (Ephemeral Key Replay)
- **Impact**: Hijacked sessions
- **Tools**: SDR (HackRF), GQRX, PQEphemeralValidator
- **Scenario**: Devices broadcast PQ keys without freshness validation; attacker reuses them
- **Attack Steps**: Step 1: Capture broadcast handshake from test device using SDR. Step 2: Log ephemeral key contents broadcast by device. Step 3: Use PQEphemeralValidator to check for repeat across time. Step 4: Replay ephemeral key to server without session timestamp. Step 5: Gain connection using broadcast key from past session. Step 6: Simulate data access with old session ID.
- **Detection**: Reuse detection in SDR logs
- **Solution**: Use time-bound ephemeral keys
- **Tags**: EphemeralReuse, PQWireless, SDRHack

## RF Harvesting of Entropy Leakage via Side-Channeled PQ Noise

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: PQ Device with Wireless Comm
- **Vulnerability**: RF Noise Leak from Entropy Source
- **MITRE**: T1203 (Side-Channel via EMF)
- **Impact**: Key prediction via leakage
- **Tools**: HackRF, SideNoiseMonitor
- **Scenario**: Improper shielding leaks PQ handshake noise via RF, enabling entropy prediction
- **Attack Steps**: Step 1: Monitor RF emissions during PQ handshake via HackRF. Step 2: Observe frequency drift and power fluctuation. Step 3: Correlate noise levels to entropy source activation. Step 4: Build a model to predict handshake key behavior. Step 5: Simulate attacker predicting PQ key material from RF emissions. Step 6: Log false connections built on predicted key patterns.
- **Detection**: RF amplitude mapping
- **Solution**: Use shielded casing, filter circuits
- **Tags**: RFLeakage, PQEntropyNoise, SideChannel

## Zigbee Device Factory Key Reuse via Insecure Production RNG

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: Zigbee IoT Device Batch
- **Vulnerability**: Factory RNG Entropy Reuse
- **MITRE**: T1215 (Supply Chain PQ Flaw)
- **Impact**: Large-scale impersonation
- **Tools**: KillerBee, FactoryKeyDump, PQBatchCollisionScanner
- **Scenario**: Factory-generated PQ key material uses batch-seeded RNG, leading to device collisions
- **Attack Steps**: Step 1: Simulate factory configuration of multiple Zigbee PQ devices. Step 2: Flash devices using same entropy batch source (educational). Step 3: Use KillerBee to extract key material from each. Step 4: Compare and observe recurring keys across units. Step 5: Simulate attacker using one device to impersonate others. Step 6: Demonstrate mass collision of identities on network.
- **Detection**: Key overlap across batches
- **Solution**: Individual device entropy seeding
- **Tags**: ZigbeeFactory, PQBatchReuse

## BLE Mesh Trust Injection via Weak PQ Group Key Rotation

- **Attack Type**: Wireless Attacks (Advanced)
- **Target**: BLE Mesh Devices
- **Vulnerability**: Predictable Group Key Rotation
- **MITRE**: T1504 (Group Key Compromise)
- **Impact**: Full mesh access
- **Tools**: BLEAH, PQGroupKeyPredictor
- **Scenario**: BLE mesh rotates PQ group key based on weak timer entropy, attacker predicts future keys
- **Attack Steps**: Step 1: Configure BLE Mesh to rotate PQ group key every 10 min using system time entropy. Step 2: Log key changes over time and derive key rotation logic. Step 3: Use PQGroupKeyPredictor to simulate future keys. Step 4: Inject attacker node into mesh with next key. Step 5: Gain trust of mesh without invitation. Step 6: Log traffic and confirm attacker has access to encrypted mesh data.
- **Detection**: Mesh entropy timer logs
- **Solution**: Use random-based key rotation
- **Tags**: PQGroupKeyLeak, BLEMeshTrustHack

## ZKP Beacon Spoofing in Smart Campus Wi-Fi

- **Attack Type**: Wireless – Wi-Fi SSID Spoofing
- **Target**: Wi-Fi client devices in campus
- **Vulnerability**: Client-side trust on SSID & beacon alone
- **MITRE**: T1557.002 – Rogue Wireless Access Point
- **Impact**: Bypass secure Wi-Fi by deception
- **Tools**: WiFi Pineapple, Airbase-ng, Hostapd
- **Scenario**: Attacker creates a rogue AP in a smart campus that spoofs ZKP-enforced Wi-Fi SSID to attract devices and bypass authentication.
- **Attack Steps**: Step 1: Deploy a rogue access point (e.g., WiFi Pineapple) with the same SSID as the official ZKP-enforced campus network.Step 2: Broadcast identical beacon frames claiming support for advanced authentication.Step 3: Clients auto-connect assuming it's a secure AP.Step 4: Accept all authentication requests with dummy proofs to mimic successful ZKP processing.Step 5: Redirect client data through attacker’s system, capturing traffic.Step 6: Explain how spoofed SSIDs and fake beacon ZKP flags can undermine trust in wireless environments.
- **Detection**: Compare signal source + beacon signature
- **Solution**: Validate network origin using cryptographic verification
- **Tags**: SSID Spoofing, ZKP Bypass, Campus Wi-Fi

## Interleaved BLE ZKP Race Condition Attack

- **Attack Type**: Wireless – Bluetooth Timing Attack
- **Target**: BLE wearable or device using ZKP
- **Vulnerability**: No sequence check in challenge-response
- **MITRE**: T1036 – Protocol Abuse
- **Impact**: Forced invalid proof acceptance
- **Tools**: BLE Sniffer (Ubertooth), GATT Tool, Custom BLE Script
- **Scenario**: Attacker injects ZKP messages out of order during BLE pairing, exploiting lack of sequence verification.
- **Attack Steps**: Step 1: Set up BLE device performing ZKP-based secure pairing.Step 2: Monitor and capture normal challenge-response sequences via Ubertooth.Step 3: Create a custom BLE script that sends out-of-order or delayed ZKP responses.Step 4: Interleave spoofed responses with genuine messages.Step 5: Verifier becomes confused and may accept mismatched or malformed proofs.Step 6: Demonstrate how race condition breaks protocol logic.
- **Detection**: Monitor for unexpected packet order
- **Solution**: Enforce strict sequencing & timestamping
- **Tags**: BLE Race Condition, Out-of-Order Attack

## RF Power Surge Inducing ZKP Calculation Errors

- **Attack Type**: Wireless – Power Fault via RF
- **Target**: Embedded ZKP-enabled security device
- **Vulnerability**: Hardware lacks RF shielding/filtering
- **MITRE**: T1600 – Induced Faults
- **Impact**: Faulty or incorrect ZKP output
- **Tools**: RF Amplifier, HackRF, ZKP Device Monitor
- **Scenario**: Strong RF energy disrupts hardware processing ZKP, leading to faulty outputs or crashes.
- **Attack Steps**: Step 1: Place target device (e.g., ZKP-authenticated badge reader) near an RF amplifier.Step 2: Trigger proof computation using a legitimate challenge.Step 3: At the moment of response generation, transmit high-energy RF pulses.Step 4: Observe output proof for bit errors, timing shifts, or miscomputation.Step 5: In some cases, faulted proofs can pass weak verification or cause reboot.Step 6: Explain how wireless interference acts as a fault injection mechanism.
- **Detection**: Monitor device behavior under RF load
- **Solution**: Add hardware shielding and computation checks
- **Tags**: RF Fault Injection, Hardware Disruption

## Zigbee Firmware Downgrade to Disable ZKP Auth

- **Attack Type**: Wireless – Zigbee OTA Exploit
- **Target**: Zigbee IoT Device
- **Vulnerability**: OTA process allows signed older firmware
- **MITRE**: T1601 – Firmware Downgrade Attack
- **Impact**: ZKP removed via firmware rollback
- **Tools**: Zigbee OTA Tool, KillerBee, Older Firmware Image
- **Scenario**: Exploits OTA firmware update process to downgrade to a ZKP-less version of firmware.
- **Attack Steps**: Step 1: Identify a Zigbee device (e.g., ZKP-secured thermostat) supporting over-the-air (OTA) updates.Step 2: Capture OTA packets using KillerBee during a legitimate firmware update.Step 3: Modify captured packets to inject an older, signed firmware that doesn’t support ZKP.Step 4: Re-broadcast the OTA image to the device.Step 5: Device accepts the downgrade, reverting to insecure auth method.Step 6: Access system using legacy (non-ZKP) authentication methods.
- **Detection**: Monitor firmware versions and update logs
- **Solution**: Implement anti-downgrade protections
- **Tags**: Zigbee, OTA, Firmware Reversion, ZKP

## SDR Replay of Distance-Bounding ZKP Challenge

- **Attack Type**: Wireless – Distance Replay
- **Target**: ZKP-based proximity verification system
- **Vulnerability**: No hard limit on timing margin
- **MITRE**: T1557.001 – Timing Relay Spoofing
- **Impact**: Proximity assumptions violated
- **Tools**: 2x HackRF, GNURadio, ZKP Distance Emulator
- **Scenario**: Distance-bounding ZKP protocol is undermined via SDR-based replay that masks timing delay.
- **Attack Steps**: Step 1: Set up a ZKP system that authenticates users based on physical proximity (distance bounding).Step 2: Place two SDR devices – one near the verifier, one near the actual prover.Step 3: Relay challenges/responses in real-time using GNURadio to simulate short distance.Step 4: Because of SDR speed, verifier doesn’t detect extra delay.Step 5: Verifier wrongly assumes prover is nearby and accepts proof.Step 6: Explain importance of enforcing strict time-bound proof validation.
- **Detection**: Time-drift and RF pattern anomaly detection
- **Solution**: Apply strict timing constraints with hardware
- **Tags**: SDR Relay, Proximity ZKP Attack

## Wi-Fi Authentication Collision to Bypass ZKP Timing

- **Attack Type**: Wireless – Collision Injection
- **Target**: ZKP-authenticated Wi-Fi access point
- **Vulnerability**: Inadequate request queuing and validation
- **MITRE**: T1499 – Protocol Abuse
- **Impact**: ZKP authentication bypass or denial
- **Tools**: Aireplay-ng, Wireshark, Custom ZKP Flood Script
- **Scenario**: Attacker floods ZKP verifier with overlapping proof attempts, causing authentication confusion.
- **Attack Steps**: Step 1: Set up a ZKP-authentication-enabled Wi-Fi access point.Step 2: Legitimate user starts ZKP handshake to connect.Step 3: At the same time, attacker script sends multiple spoofed proofs to the AP with slight timing overlaps.Step 4: The verifier gets confused — may accept a spoofed proof, drop valid ones, or allow fallback.Step 5: Analyze access logs to identify proof mismatches or skipped challenge validation.Step 6: Explain how timing-based collisions can bypass ZKP logic.
- **Detection**: Detect overlapping challenge IDs and timestamps
- **Solution**: Add proof queueing, timing guardrails
- **Tags**: Wi-Fi Collision, ZKP Proof Injection

