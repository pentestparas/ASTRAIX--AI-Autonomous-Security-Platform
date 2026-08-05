# Zero-Day Research / Fuzzing → Automation and Scaling Attacks

## Running Multiple AFL Instances in Parallel

- **Attack Type**: Fuzzing Infrastructure Optimization
- **Target**: Linux Binary
- **Vulnerability**: Uncaught memory exceptions
- **MITRE**: T1595
- **Impact**: Increased fuzzing throughput
- **Tools**: AFL++, tmux
- **Scenario**: Fuzzing a binary using multiple CPU cores by launching multiple AFL instances in parallel using tmux
- **Attack Steps**: 1. Start by identifying the number of CPU cores on your system using lscpu. 2. Choose a target binary that has already been instrumented for fuzzing. 3. Create a shared input corpus folder (/inputs) and an output sync directory (/outputs). 4. Open multiple tmux panes and for each one, launch AFL in a different mode: one master (afl-fuzz -M fuzzer01) and multiple slaves (afl-fuzz -S fuzzer02, fuzzer03, etc.). 5. All instances should point to the same input and output directories. 6. Let the fuzzers run in parallel, effectively utilizing system resources. 7. Monitor crashes and hangs reported in the output folder.
- **Detection**: Observe AFL sync logs and queue sizes
- **Solution**: Use clusters or tmux screen to split and maximize CPU core usage
- **Tags**: fuzzing, parallel, AFL, performance

## Automating Cluster-Based Fuzzing with ClusterFuzzLite

- **Attack Type**: Cloud-Based Parallel Fuzzing
- **Target**: Open-Source Project
- **Vulnerability**: Logic Bugs, Input validation flaws
- **MITRE**: T1587
- **Impact**: Continuous crash discovery and triage
- **Tools**: ClusterFuzzLite, GitHub Actions
- **Scenario**: Using ClusterFuzzLite on GitHub Actions to continuously fuzz a target project
- **Attack Steps**: 1. Fork a target open-source project on GitHub. 2. Integrate ClusterFuzzLite by adding fuzzing workflows in .github/workflows. 3. Define your fuzzing targets using build.sh and fuzz_targets inside the repo. 4. Commit and push the changes to GitHub. 5. ClusterFuzzLite will automatically start fuzzing via GitHub Actions. 6. Check results under GitHub Actions for any crashes and logs. 7. Enable persistent storage if you want to retain and download corpus and crash data.
- **Detection**: GitHub Action Logs, crash diffs
- **Solution**: Monitor GitHub CI, configure sanitizers for richer crash data
- **Tags**: automation, CI/CD, clusterfuzz

## Using Docker to Scale LibFuzzer Campaigns

- **Attack Type**: Containerized Fuzzing
- **Target**: Linux Binary
- **Vulnerability**: Heap corruption, overflow
- **MITRE**: T1499
- **Impact**: Container-based scale-out fuzzing
- **Tools**: Docker, LibFuzzer
- **Scenario**: Scaling fuzzing by launching isolated LibFuzzer containers
- **Attack Steps**: 1. Create a Dockerfile that compiles your target binary with Clang and links it with LibFuzzer. 2. Include the fuzz target and sanitize it with AddressSanitizer. 3. Build the Docker image. 4. Use a shell script to launch multiple containers in parallel, each with a different seed corpus. 5. Limit memory and CPU for each container to avoid resource contention. 6. Mount volumes to persist crash outputs. 7. Monitor containers for crashes and collect logs systematically.
- **Detection**: Docker stats, libFuzzer logs
- **Solution**: Cleanup and isolate crash logs per container
- **Tags**: docker, containers, libfuzzer

## Monitor Execs per Second and Crash Rate

- **Attack Type**: Fuzzing Metrics Tracking
- **Target**: Native Binary
- **Vulnerability**: Memory safety bugs
- **MITRE**: T1602
- **Impact**: Improved operational visibility
- **Tools**: AFL++, Prometheus
- **Scenario**: Tracking key metrics like executions/sec and crash count over time
- **Attack Steps**: 1. Launch AFL fuzzers using master-slave mode. 2. Use afl-whatsup periodically to see all fuzzers’ stats. 3. Note metrics such as execs/sec, unique crashes, unique hangs. 4. Install Prometheus node exporter to expose system resource metrics. 5. Scrape AFL stats and system metrics into Prometheus. 6. Visualize data on a Grafana dashboard. 7. Set alerts for low exec rates or spikes in crash counts.
- **Detection**: Metric graphs, alerting via Prometheus
- **Solution**: Automate monitoring via dashboards
- **Tags**: metrics, grafana, prometheus

## Integrating Dr. Memory with Fuzz Output

- **Attack Type**: Memory Leak Analysis
- **Target**: Windows Binary
- **Vulnerability**: Use-after-free, Heap corruption
- **MITRE**: T1611
- **Impact**: Accurate memory error validation
- **Tools**: Dr. Memory, AFL++
- **Scenario**: Using Dr. Memory to validate memory errors found during fuzzing
- **Attack Steps**: 1. Identify a crashing input from AFL’s output folder. 2. Take the input and run the target binary under Dr. Memory using drmemory -- target input_file. 3. Let Dr. Memory inspect runtime for memory leaks, buffer overflows, etc. 4. Review the detailed HTML or log reports generated. 5. Compare Dr. Memory findings with AFL crash output. 6. Use this info to confirm or rule out exploitability.
- **Detection**: Dr. Memory log output
- **Solution**: Automate input replay through script
- **Tags**: crash triage, memory tools

## Crash Minimization with afl-cmin

- **Attack Type**: Input Corpus Optimization
- **Target**: ELF Binary
- **Vulnerability**: Faulty file parsing logic
- **MITRE**: T1491
- **Impact**: Smaller inputs for reproducibility
- **Tools**: AFL++, afl-cmin
- **Scenario**: Shrinking fuzz input size to isolate critical crash-causing bytes
- **Attack Steps**: 1. Identify a crash-triggering input file in AFL’s queue. 2. Use afl-cmin with the original target binary to minimize that input. 3. Provide the crashing input as the seed and use -- to denote the binary to run. 4. The tool will try different trimmed inputs that still trigger the same behavior. 5. Output is a minimized input of smallest length that reproduces the crash. 6. Save the minimized input for future crash analysis.
- **Detection**: afl-cmin logs
- **Solution**: Store and archive minimized crashes
- **Tags**: input minimization, AFL

## Using Tmux + Screen for Interactive Fuzzing Farm

- **Attack Type**: Terminal Multiplexing for Scale
- **Target**: Linux Binary
- **Vulnerability**: Boundary condition flaws
- **MITRE**: T1082
- **Impact**: Easier manual control over fuzzing
- **Tools**: tmux, AFL++
- **Scenario**: Managing many simultaneous fuzzing sessions using tmux
- **Attack Steps**: 1. Launch tmux from terminal. 2. Create multiple windows/panes with Ctrl+B, then % or ". 3. In each pane, start an AFL slave or master instance. 4. Sync all fuzzers to the same input/output folder. 5. Rename sessions and panes using Ctrl+B + ,. 6. Reattach anytime using tmux attach -t session_name. 7. Monitor logs and queue size directly from each pane.
- **Detection**: Visual tmux interface
- **Solution**: Persistent monitoring across sessions
- **Tags**: fuzzing farm, CLI management

## Scaling Fuzzing with Kubernetes

- **Attack Type**: Orchestrated Fuzzing Campaign
- **Target**: Cloud Native Targets
- **Vulnerability**: File parsing bugs, Race conditions
- **MITRE**: T1496
- **Impact**: Horizontally scaled fuzzing power
- **Tools**: Kubernetes, AFL++, Helm
- **Scenario**: Running fuzzers in a scalable Kubernetes cluster
- **Attack Steps**: 1. Package your instrumented binary and fuzz target into a Docker image. 2. Create a Kubernetes deployment YAML for your fuzzer. 3. Use Helm charts or manually define CPU and memory limits. 4. Spin up multiple replicas of fuzzers across worker nodes. 5. Mount shared volumes for synchronized output. 6. Use Prometheus and Grafana for observability. 7. Automatically rotate or restart fuzzer pods on crash.
- **Detection**: Kubernetes pod logs, Prometheus
- **Solution**: Auto-scaling based on fuzz load
- **Tags**: devops, kubernetes, fuzzing

## Automate Crash Replay in GDB

- **Attack Type**: Crash Debugging Automation
- **Target**: Linux Executable
- **Vulnerability**: Heap overflows, logic bugs
- **MITRE**: T1611
- **Impact**: Fast and repeatable crash diagnostics
- **Tools**: GDB, AFL++, bash
- **Scenario**: Writing GDB scripts to replay crashes found by fuzzer
- **Attack Steps**: 1. Identify crashing input from fuzzing output. 2. Create a small bash script to run: gdb --args ./binary inputfile. 3. Automate breakpoints (b main, run) and commands (bt, info registers). 4. Save commands in .gdbinit or as a custom script. 5. Collect output for each crash file in logs. 6. Use loops to process all crashes in output/crashes/. 7. Store backtraces for triage and correlation.
- **Detection**: GDB scripted logs
- **Solution**: Batch mode GDB for triage automation
- **Tags**: crash triage, gdb, replay

## Measuring Code Coverage Growth Over Time

- **Attack Type**: Fuzzing Quality Evaluation
- **Target**: C/C++ Target
- **Vulnerability**: Incomplete test coverage
- **MITRE**: T1203
- **Impact**: Feedback-driven fuzzing success
- **Tools**: libFuzzer, llvm-cov
- **Scenario**: Tracking code coverage delta across fuzzing sessions
- **Attack Steps**: 1. Compile fuzz target with coverage flags (-fprofile-instr-generate, -fcoverage-mapping). 2. Start fuzzing with libFuzzer. 3. Periodically stop fuzzing and collect .profraw files. 4. Convert them to .profdata using llvm-profdata merge. 5. Use llvm-cov show to view which lines of code were exercised. 6. Repeat over time to see improvements. 7. Visualize and archive reports to measure progress.
- **Detection**: Coverage delta reports
- **Solution**: Guide input mutation with coverage insight
- **Tags**: fuzzing, coverage, llvm

## Scaling AFL++ with Screen Sessions

- **Attack Type**: Fuzzing Infrastructure
- **Target**: Linux Binaries
- **Vulnerability**: Memory corruption
- **MITRE**: T1595.003 (Data from Local System)
- **Impact**: Efficient input space exploration
- **Tools**: AFL++, GNU Screen
- **Scenario**: Multiple AFL++ sessions are launched in parallel using GNU Screen
- **Attack Steps**: 1. Prepare the target binary by instrumenting it with AFL++. 2. Create multiple input queues with initial test cases. 3. Open several screen sessions using screen -S fuzz1, screen -S fuzz2, etc. 4. In each session, run afl-fuzz -i input_dir -o output_dir -M fuzzer1, -S fuzzer2, etc. 5. Let them run in parallel, ensuring system resources are sufficient. 6. Monitor individual screens for crashes.
- **Detection**: Check resource usage and screen logs
- **Solution**: Use tmux/screen for lightweight fuzzing scale-up
- **Tags**: fuzzing, scaling, screen, AFL++

## Automating Triage via syz-manager

- **Attack Type**: Crash Triage Automation
- **Target**: Linux Kernel
- **Vulnerability**: Kernel Bugs
- **MITRE**: T1203 (Exploitation for Client Execution)
- **Impact**: Kernel crash detection and classification
- **Tools**: syzkaller, syz-manager, QEMU
- **Scenario**: Automate triage of Linux kernel crashes using syzkaller's manager
- **Attack Steps**: 1. Set up a Linux kernel and QEMU image for fuzzing. 2. Configure syz-manager with your kernel build and image. 3. Start the manager using ./syz-manager -config=config.cfg. 4. The manager continuously launches VMs, executes syscalls, and captures crashes. 5. Crashes are automatically triaged and logged. 6. Use the dashboard to view crash trends and statistics.
- **Detection**: Review syz-manager logs and web UI
- **Solution**: Integrate with syz-ci for scalable triage automation
- **Tags**: syzkaller, automation, crash triage, kernel

## Tracking Fuzzing Stats with Prometheus

- **Attack Type**: Observability Metrics
- **Target**: Any Instrumented
- **Vulnerability**: None
- **MITRE**: T1082 (System Info Discovery)
- **Impact**: Real-time monitoring of fuzzing performance
- **Tools**: AFL++, Prometheus, Grafana
- **Scenario**: Collect performance metrics from fuzzers and export to Grafana dashboard
- **Attack Steps**: 1. Modify your fuzzing setup to expose metrics (e.g., execs/sec, crashes). 2. Install Prometheus node exporter. 3. Write a custom Python or Go exporter script to parse AFL stats. 4. Run Prometheus and configure a scrape job for your exporter. 5. Visualize execution speed and crash rate on Grafana. 6. Use alerts for anomalous crash spikes.
- **Detection**: Monitor Prometheus/Grafana dashboards
- **Solution**: Alert on unusual behavior or crash density
- **Tags**: metrics, grafana, prometheus, fuzzing

## Distributed Fuzzing Using Docker Swarm

- **Attack Type**: Distributed Fuzzing
- **Target**: Multi-host Linux
- **Vulnerability**: Memory corruption
- **MITRE**: T1046 (Network Service Scanning)
- **Impact**: Massively parallel fuzzing across network
- **Tools**: Docker, AFL++, Swarm
- **Scenario**: Docker Swarm orchestrates fuzzers across multiple hosts
- **Attack Steps**: 1. Containerize the AFL++ fuzzing setup in a Docker image. 2. Initialize Docker Swarm using docker swarm init. 3. Deploy multiple AFL instances as services using a docker-compose.yml file. 4. Distribute services across swarm nodes. 5. Mount shared output directories (e.g., via NFS). 6. Monitor and collect crash data across nodes.
- **Detection**: Monitor Docker logs and shared volumes
- **Solution**: Leverage Docker Swarm for easy scaling of AFL setup
- **Tags**: docker, swarm, parallel fuzzing

## Parallel Fuzzing with QEMU Snapshotting

- **Attack Type**: Performance Optimization
- **Target**: Linux Kernel
- **Vulnerability**: Race Conditions
- **MITRE**: T1499 (Endpoint Denial of Service)
- **Impact**: Reduces reboots, boosts coverage rate
- **Tools**: QEMU, AFL++, libFuzzer
- **Scenario**: Run multiple fuzzers from a QEMU snapshot to reduce boot time overhead
- **Attack Steps**: 1. Configure a base QEMU VM with the fuzz target. 2. Save a snapshot after boot and target setup. 3. Use qemu-system-x86_64 -loadvm snapshot to quickly boot. 4. Launch multiple fuzzers in parallel using different cores. 5. Collect crashes from shared AFL output directory. 6. Use AFL's -M and -S options for synchronized fuzzing.
- **Detection**: Use crash monitor with timestamped output
- **Solution**: Use snapshotting to optimize fuzz loop throughput
- **Tags**: qemu, snapshots, fuzzing, speed

## Monitoring Execs/Sec via InfluxDB

- **Attack Type**: Metric Logging
- **Target**: Local or Cluster
- **Vulnerability**: None
- **MITRE**: T1602 (Data Staged)
- **Impact**: Helps detect stalled or idle fuzzers
- **Tools**: InfluxDB, Telegraf, AFL++
- **Scenario**: Collect execution performance metrics into InfluxDB
- **Attack Steps**: 1. Create a script that reads AFL++'s fuzzer_stats. 2. Configure Telegraf with a custom input plugin. 3. Send data into InfluxDB at intervals. 4. Create Grafana panels to display fuzz rate, crashes over time. 5. Use alerts to identify fuzzer stalls. 6. Automate alerts if exec/sec drops below threshold.
- **Detection**: InfluxDB logs and Grafana dashboards
- **Solution**: Use Telegraf as efficient metric collector
- **Tags**: influxdb, telegraf, fuzz monitoring

## Scheduling Fuzz Jobs with cron

- **Attack Type**: Job Scheduling
- **Target**: Local Server
- **Vulnerability**: None
- **MITRE**: T1053.003 (Scheduled Task)
- **Impact**: Automation of fuzz jobs post-reboot
- **Tools**: cron, bash, AFL++
- **Scenario**: Automatically restart or rotate fuzzing jobs using cron
- **Attack Steps**: 1. Write a shell script to start or restart your fuzzers. 2. Schedule it in crontab -e with @reboot or hourly. 3. Use a loop in the script to relaunch on crash. 4. Rotate logs to avoid disk saturation. 5. Redirect outputs to crash triage tool (e.g., CrashWrangler). 6. Use cron mail alerts for failures.
- **Detection**: Check logs and cron email notifications
- **Solution**: Simple method to keep fuzzers alive persistently
- **Tags**: cron, automation, scheduling

## Using ClusterFuzzLite in CI Pipelines

- **Attack Type**: CI-integrated Fuzzing
- **Target**: Open Source Software
- **Vulnerability**: Memory bugs
- **MITRE**: T1203
- **Impact**: Catches bugs before merge to main branch
- **Tools**: ClusterFuzzLite, GitHub Actions
- **Scenario**: Run OSS-Fuzz's ClusterFuzzLite in GitHub Actions to fuzz during CI
- **Attack Steps**: 1. Set up ClusterFuzzLite in your repo following Google’s guide. 2. Create a Dockerfile to build your instrumented binary. 3. Use GitHub Actions workflow to run fuzz targets in parallel. 4. On PR submission, fuzzers run and log crashes. 5. Crashes are stored in CI artifacts. 6. Triage and fix before merging code.
- **Detection**: Monitor CI logs, review crash artifacts
- **Solution**: Use ClusterFuzzLite for OSS-compatible fuzz pipelines
- **Tags**: oss-fuzz, CI/CD, GitHub Actions, ClusterFuzz

## Collecting Code Coverage via llvm-cov

- **Attack Type**: Coverage Analysis
- **Target**: C/C++ Applications
- **Vulnerability**: Input Handling Gaps
- **MITRE**: T1601 (Archive Collected Data)
- **Impact**: Shows gaps in input test space
- **Tools**: llvm-cov, Clang, libFuzzer
- **Scenario**: Use LLVM coverage tooling to evaluate fuzzing effectiveness
- **Attack Steps**: 1. Compile target with -fsanitize=fuzzer -fprofile-instr-generate -fcoverage-mapping. 2. Run fuzzing for a fixed time with libFuzzer. 3. Use llvm-profdata merge to consolidate .profraw files. 4. Run llvm-cov show and llvm-cov report to get coverage stats. 5. Identify uncovered functions/paths. 6. Tune corpus based on results.
- **Detection**: Review HTML or CLI coverage reports
- **Solution**: Use coverage feedback to improve fuzz effectiveness
- **Tags**: llvm-cov, coverage-guided fuzzing

## Remote Crash Collection via rsync

- **Attack Type**: Centralized Crash Triage
- **Target**: Multi-node Fuzzing
- **Vulnerability**: None
- **MITRE**: T1020 (Automated Exfiltration)
- **Impact**: Enables scalable triage of distributed fuzz
- **Tools**: rsync, SSH, AFL++
- **Scenario**: Sync crash directories from multiple nodes to one system
- **Attack Steps**: 1. Ensure all fuzzing nodes output to a local crash directory. 2. On central server, create a sync script using rsync -avz user@node:/crash_dir /central_crash_dir. 3. Automate this with cron or systemd timers. 4. Add deduplication logic using hashes. 5. Triaged crashes can now be analyzed centrally. 6. Back up periodically to external drive.
- **Detection**: Check rsync logs and compare checksums
- **Solution**: Maintain a reliable sync of crash output across systems
- **Tags**: rsync, centralized, automation, triage

